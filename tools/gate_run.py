#!/usr/bin/env python3
"""Bennett push gate: a repo's own checks, on the pushed sha, against siblings at pinned shas.

See tools/gate_README.md. Python stdlib only. Exit codes of `run`:
  0  every [[check]] passed (blockers and consumer evidence are reported, never an exit code)
  1  a [[check]] failed
  3  the gate could not be set up honestly: missing or mismatched pin, unbuildable sibling, tool error
"""
import argparse
import fcntl
import hashlib
import json
import os
import platform
import re
import select
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import tomllib
from pathlib import Path

PIN_FILE = "gate.toml"
SHA = re.compile(r"^[0-9a-f]{40}$")
ZERO = "0" * 40
EXIT_FAIL, EXIT_SETUP = 1, 3
PROBE_VAR = "BENNETT_GATE_HOOK_PROBE"
PROBE_LINE = "bennett-gate-hook-chained"
HEADLESS = ("DISPLAY", "WAYLAND_DISPLAY", "DBUS_SESSION_BUS_ADDRESS", "BROWSER")
WIDTH_ENV = (
    "CARGO_BUILD_JOBS", "CARGO_MAKEFLAGS", "MAKEFLAGS", "MFLAGS", "RUST_TEST_THREADS",
    "RAYON_NUM_THREADS", "CMAKE_BUILD_PARALLEL_LEVEL", "CTEST_PARALLEL_LEVEL", "NINJAFLAGS",
    "OMP_NUM_THREADS", "OMP_THREAD_LIMIT", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS", "GOMAXPROCS",
)
TOP_KEYS = {"schema", "repo", "tool_sha", "timeout_s", "env", "check", "report", "siblings", "scan_exclude"}
CMD_KEYS = {"name", "argv", "env", "cwd"}
SIB_KEYS = {"sha", "repo", "files", "build", "note"}
BUILD_KEYS = {"name", "argv", "cwd", "outputs", "needs", "env"}
SCAN_EXCLUDE = (
    ":!docs", ":!worklog", ":!.beads", ":!vendor", ":!*.md", ":!*.lock", ":!*.ll", ":!*.json", ":!*.jsonl",
    ":!*.log", ":!*.txt", ":!*.bisa", ":!*.bennett", ":!*.stderr", ":!*.diff", ":!*.toml", ":!scripts/pre-push",
)


class GateError(Exception):
    """The gate cannot be set up honestly. Never swallowed: maps to exit 3."""


class Interrupted(BaseException):
    """SIGTERM/SIGHUP/SIGINT. Unwinds through every finally, so the running command's process group is killed and
    the run worktree removed; no record is written. Exit 128+signal."""

    def __init__(self, signum):
        super().__init__(signum)
        self.signum = signum


INTERRUPTS = (signal.SIGTERM, signal.SIGHUP, signal.SIGINT)


def on_interrupt(signum, _frame):
    for s in INTERRUPTS:  # a second signal must not cut the cleanup short
        signal.signal(s, signal.SIG_IGN)
    raise Interrupted(signum)


def say(msg):
    print(f"gate: {msg}", file=sys.stderr, flush=True)


def receipt_unavailable(name, error):
    reason = f"{type(error).__name__}: {error}"
    say(f"receipt {name} unavailable: {reason}")
    return {"unavailable": reason}


def receipt_probe(name, collect):
    """Optional evidence cannot affect execution; interrupts still unwind normally."""
    try:
        value = collect()
        # Reject unsupported evidence here, before it can break receipt writing.
        json.dumps(value, allow_nan=False)
        return value
    except Exception as error:
        return receipt_unavailable(name, error)


def elapsed_seconds(name, started):
    if isinstance(started, dict):
        return started
    return receipt_probe(name, lambda: time.monotonic() - started)


def width_env(env):
    return {k: env[k] for k in WIDTH_ENV if k in env}


def git_env():
    return {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}


def git(repo, *args, check=True):
    # The hook path is blanked so a sibling's beads post-checkout never runs in the gate's caches.
    z = subprocess.run(
        ["git", "-c", "core.hooksPath=/dev/null", "-C", str(repo), *args],
        capture_output=True, text=True, env=git_env(), stdin=subprocess.DEVNULL,
    )
    if check and z.returncode != 0:
        raise GateError(f"git -C {repo} {' '.join(args)}: {z.stderr.strip()}")
    return z.stdout.strip() if check else z


def repo_paths(repo):
    root = Path(git(repo, "rev-parse", "--show-toplevel")).resolve()
    common = Path(git(root, "rev-parse", "--path-format=absolute", "--git-common-dir")).resolve()
    workspace = os.environ.get("BENNETT_GATE_WORKSPACE")
    return root, Path(workspace).resolve() if workspace else common.parent.parent


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def reject_unknown(table, allowed, where):
    extra = set(table) - allowed
    if extra:
        raise GateError(f"{PIN_FILE}: unknown key {sorted(extra)} in {where}")


def check_command(cmd, where, keys):
    if not isinstance(cmd, dict):
        raise GateError(f"{PIN_FILE}: {where} must be a table")
    reject_unknown(cmd, keys, where)
    argv = cmd.get("argv")
    if not cmd.get("name") or not isinstance(argv, list) or not argv or not all(isinstance(a, str) for a in argv):
        raise GateError(f"{PIN_FILE}: {where} needs name and a non-empty argv list")


def load_config(root, sha):
    z = git(root, "show", f"{sha}:{PIN_FILE}", check=False)
    if z.returncode != 0:
        raise GateError(f"{sha} has no {PIN_FILE}: a gated repo must commit its pin file (tools/gate_README.md)")
    try:
        cfg = tomllib.loads(z.stdout)
    except tomllib.TOMLDecodeError as e:
        raise GateError(f"{PIN_FILE} at {sha}: {e}") from e
    reject_unknown(cfg, TOP_KEYS, "top level")
    if cfg.get("schema") != 1:
        raise GateError(f"{PIN_FILE}: schema must be 1, got {cfg.get('schema')!r}")
    if not cfg.get("repo"):
        raise GateError(f"{PIN_FILE}: repo is required")
    if not SHA.match(str(cfg.get("tool_sha", ""))):
        raise GateError(f"{PIN_FILE}: tool_sha must be a full 40-hex commit of the meta repo")
    if not cfg.get("check"):
        raise GateError(f"{PIN_FILE}: at least one [[check]] is required; a gate that checks nothing is not a gate")
    for i, c in enumerate(cfg["check"]):
        check_command(c, f"check[{i}]", CMD_KEYS)
    for i, c in enumerate(cfg.get("report", [])):
        check_command(c, f"report[{i}]", CMD_KEYS)
    for name, pin in cfg.get("siblings", {}).items():
        reject_unknown(pin, SIB_KEYS, f"siblings.{name}")
        if not SHA.match(str(pin.get("sha", ""))):
            raise GateError(f"{PIN_FILE}: siblings.{name}.sha must be a full 40-hex commit, got {pin.get('sha')!r}")
        for i, b in enumerate(pin.get("build", [])):
            check_command(b, f"siblings.{name}.build[{i}]", BUILD_KEYS)
            for need in b.get("needs", []):
                if need not in cfg["siblings"]:
                    raise GateError(f"{PIN_FILE}: siblings.{name}.build needs unpinned sibling {need}")
    return cfg


def expand(text, ctx):
    def one(m):
        key = m.group(1)
        if key in ctx:
            return str(ctx[key])
        raise GateError(f"{PIN_FILE}: unknown placeholder {{{key}}} (is that sibling pinned?)")
    return re.sub(r"\{([^{}]+)\}", one, text)


def base_env(tmpdir):
    env = {}
    scrubbed = []
    for k, v in os.environ.items():
        if k in HEADLESS or k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "CARGO_TARGET_DIR"):
            continue
        if k.startswith("BENNETT_") and not k.startswith("BENNETT_GATE_"):
            scrubbed.append(k)
            continue
        env[k] = v
    if scrubbed:
        say(f"scrubbed inherited {sorted(scrubbed)}: pins in {PIN_FILE} are the only sibling source")
    Path(tmpdir).mkdir(parents=True, exist_ok=True)
    env["TMPDIR"] = str(tmpdir)
    return env


class Isolation:
    """bwrap argv hiding every live working tree in the workspace; each .git stays for object reads.

    The workspace is rescanned for every command: sibling worktrees come and go while a gate runs for hours (a
    vanished one made every later bwrap fail; a new one would have stayed visible)."""

    def __init__(self, workspace, own_roots):
        self.bwrap = os.environ.get("BENNETT_GATE_BWRAP", "bwrap")
        if not shutil.which(self.bwrap):
            raise GateError(f"isolation needs bwrap ({self.bwrap} not found); --no-isolate only with the omission recorded")
        self.workspace, self.own = Path(workspace), {Path(r).resolve() for r in own_roots}
        z = subprocess.run([*self.argv(), "true"], capture_output=True, text=True)
        if z.returncode != 0:
            raise GateError(f"isolation probe failed: {z.stderr.strip()}; --no-isolate only with the omission recorded")

    def argv(self):
        prefix = [self.bwrap, "--dev-bind", "/", "/", "--die-with-parent"]
        for entry in sorted(self.workspace.iterdir()):
            try:
                if entry.is_symlink() or not entry.is_dir() or entry.resolve() in self.own or entry.name.startswith("."):
                    continue
            except FileNotFoundError:
                continue  # removed while scanning
            prefix += ["--tmpfs", str(entry)]
            # --bind-try: a worktree removed between this scan and bwrap's start is absent, not a setup failure.
            prefix += ["--bind-try", str(entry / ".git"), str(entry / ".git")]
        return prefix


def isolation_prefix(workspace, own_roots):
    return Isolation(workspace, own_roots)


class ResourceProcess(subprocess.Popen):
    """Keep Popen's POSIX wait/timeout semantics, collecting usage at its waitpid hook.

    Linux wait4 includes descendants reaped by the child. ru_maxrss is the largest
    individual process peak in that tree (KiB), not a sum of concurrent RSS.
    """

    def _try_wait(self, wait_flags):
        if hasattr(self, "usage_error"):
            return super()._try_wait(wait_flags)
        try:
            pid, status, usage = os.wait4(self.pid, wait_flags)
        except Exception as error:
            # wait4 is an optional probe. Ordinary Popen waiting owns the status
            # when accounting is unavailable; do not kill or skip this command.
            self.usage_error = error
            return super()._try_wait(wait_flags)
        if pid:
            self.usage = usage
        return pid, status


def run_cmd(argv, cwd, env, prefix, timeout, metrics=None):
    """Run in its own session; on timeout or interruption kill the whole group. Returns the exit status."""
    full = argv
    if prefix:
        full = [*prefix.argv(), "--chdir", str(cwd), "--", *argv]
    try:
        process_class = ResourceProcess if metrics is not None else subprocess.Popen
        proc = process_class(full, cwd=cwd, env=env, stdin=subprocess.DEVNULL, start_new_session=True)
    except OSError as e:
        say(f"cannot run {argv}: {e}")
        if metrics is not None:
            for field in ("cpu_seconds", "peak_rss_kib"):
                metrics[field] = receipt_unavailable(field, e)
        return 127
    try:
        return proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        say(f"TIMEOUT after {timeout} s: {argv}")
        return 124
    finally:
        # Do not poll: Popen.poll() reaps via waitpid without preserving wait4 usage.
        if proc.returncode is None:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait()
        if metrics is not None:
            if hasattr(proc, "usage_error"):
                for field in ("cpu_seconds", "peak_rss_kib"):
                    metrics[field] = receipt_unavailable(field, proc.usage_error)
            else:
                metrics.update(
                    cpu_seconds=receipt_probe("cpu_seconds", lambda: proc.usage.ru_utime + proc.usage.ru_stime),
                    peak_rss_kib=receipt_probe("peak_rss_kib", lambda: proc.usage.ru_maxrss))


class Lock:
    def __init__(self, path, blocking=True):
        self.path, self.blocking = Path(path), blocking

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.f = open(self.path, "a+")
        flags = fcntl.LOCK_EX | (0 if self.blocking else fcntl.LOCK_NB)
        try:
            fcntl.flock(self.f, flags)
        except BlockingIOError as e:
            self.f.seek(0)
            holder = self.f.read().strip()
            self.f.close()
            raise GateError(f"another gate holds {self.path} ({holder})") from e
        self.f.seek(0)
        self.f.truncate()
        self.f.write(f"pid={os.getpid()} started_utc={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n")
        self.f.flush()
        return self

    def __exit__(self, *exc):
        self.f.close()


def remove_worktree(owner, wt):
    git(owner, "worktree", "remove", "--force", str(wt), check=False)
    shutil.rmtree(wt, ignore_errors=True)
    git(owner, "worktree", "prune", check=False)


def link(path, target):
    tmp = path.with_name(path.name + f".tmp{os.getpid()}")
    if tmp.is_symlink():
        tmp.unlink()
    tmp.symlink_to(target)
    os.replace(tmp, path)


class Siblings:
    """Detached worktrees of pinned commits under <repo>/.tmp/gate/cache/<name>@<sha12>/<name>."""

    def __init__(self, cfg, root, workspace):
        self.pins = cfg.get("siblings", {})
        self.workspace = workspace
        self.cache = root / ".tmp/gate/cache"
        self.locks = root / ".tmp/gate/locks"
        self.paths = {}
        self.notes = {}

    def owner(self, name):
        return self.workspace / self.pins[name].get("repo", name)

    def path(self, name):
        pin = self.pins[name]
        return self.cache / f"{name}@{pin['sha'][:12]}" / name

    def materialise(self, name):
        pin, sha, owner, wt = self.pins[name], self.pins[name]["sha"], self.owner(name), self.path(name)
        if not (owner / ".git").exists():
            raise GateError(f"sibling {name}: no repo at {owner}")
        if git(owner, "cat-file", "-e", f"{sha}^{{commit}}", check=False).returncode != 0:
            raise GateError(f"sibling {name}: pinned commit {sha} not in {owner}")
        with Lock(self.locks / f"{name}@{sha[:12]}"):
            cache_state = "hit"
            if wt.exists():
                head = git(wt, "rev-parse", "HEAD", check=False).stdout.strip()
                dirty = git(wt, "status", "--porcelain", "-uno", check=False).stdout.strip()
                if head != sha or dirty:
                    say(f"sibling {name}: cached worktree tampered (head {head[:12]}, dirty: {bool(dirty)}); rematerialising")
                    remove_worktree(owner, wt)
            if not wt.exists():
                wt.parent.mkdir(parents=True, exist_ok=True)
                git(owner, "worktree", "prune", check=False)
                git(owner, "worktree", "add", "--detach", str(wt), sha)
                cache_state = "materialised"
                say(f"sibling {name}: materialised {sha[:12]} at {wt}")
        for rel, want in pin.get("files", {}).items():
            f = wt / rel
            if not f.is_file():
                raise GateError(f"sibling {name}: pinned file {rel} missing at {sha[:12]}")
            got = sha256_file(f)
            if got != want:
                raise GateError(f"sibling {name}: {rel} at {sha[:12]} hashes {got}, pin says {want}")
        pushed = git(owner, "merge-base", "--is-ancestor", sha, "origin/main", check=False).returncode == 0
        if not pushed:
            say(f"note: sibling {name} pin {sha[:12]} not reachable from origin/main (not yet pushed)")
        self.notes[name] = {"sha": sha, "repo": pin.get("repo", name), "pushed": pushed,
                            "files": dict(pin.get("files", {})), "cache_state": cache_state}
        self.paths[name] = wt

    def build(self, name, prefix):
        pin, wt = self.pins[name], self.path(name)
        for b in pin.get("build", []):
            needs = sorted(b.get("needs", []))
            key = json.dumps([pin["sha"], b, [self.pins[n]["sha"] for n in needs]], sort_keys=True)
            stamp = wt.parent / f"build-{hashlib.sha256(key.encode()).hexdigest()[:20]}.json"
            with Lock(self.locks / f"{name}@{pin['sha'][:12]}.build"):
                outputs = [wt / o for o in b.get("outputs", [])]
                if stamp.exists() and all(o.exists() for o in outputs):
                    continue
                for n in needs:
                    link(wt.parent / n, self.path(n))
                say(f"sibling {name}: building {b['name']} at {pin['sha'][:12]} (once per sha)")
                env = base_env(wt.parent / "tmp")
                env.update(b.get("env", {}))
                code = run_cmd(b["argv"], wt / b.get("cwd", "."), env, prefix, None)
                if code != 0:
                    raise GateError(f"sibling {name}: build {b['name']} exited {code}")
                missing = [str(o) for o in outputs if not o.exists()]
                if missing:
                    raise GateError(f"sibling {name}: build {b['name']} did not produce {missing}")
                stamp.write_text(key + "\n")
                self.notes[name]["cache_state"] = "built"


def run_commands(cmds, wt, env, ctx, prefix, timeout, label):
    """Yield (name, exit) until a failure when label is check; all of them when it is report."""
    results = []
    for c in cmds:
        argv = [expand(a, ctx) for a in c["argv"]]
        cmd_env = dict(env)
        cmd_env.update({k: expand(v, ctx) for k, v in c.get("env", {}).items()})
        cwd = wt / c.get("cwd", ".")
        print(f"gate: {label} {c['name']}: {' '.join(argv)}", file=sys.stderr, flush=True)
        metrics = {}
        started = receipt_probe("wall_seconds", lambda: time.monotonic())
        code = run_cmd(argv, cwd, cmd_env, prefix, timeout, metrics=metrics)
        wall_seconds = elapsed_seconds("wall_seconds", started)
        seconds = wall_seconds if isinstance(wall_seconds, dict) else round(wall_seconds, 1)
        results.append({"name": c["name"], "exit": code, "seconds": seconds,
                        "wall_seconds": wall_seconds, **metrics,
                        "width_env": receipt_probe("width_env", lambda: width_env(cmd_env))})
        if label == "check" and code != 0:
            say(f"FAIL check {c['name']} exited {code}")
            break
    return results


def resolve_shas(args, root):
    """Pushed shas from --sha, or git's ref stream on stdin, or HEAD when there are no refs."""
    if args.sha:
        return [git(root, "rev-parse", "--verify", f"{s}^{{commit}}") for s in args.sha]
    lines = []
    if not sys.stdin.isatty():
        ready, _, _ = select.select([sys.stdin], [], [], 10)
        if ready:
            lines = [ln for ln in sys.stdin.read().splitlines() if ln.strip()]
    if not lines:
        return [git(root, "rev-parse", "--verify", "HEAD^{commit}")]
    shas = []
    for ln in lines:
        parts = ln.split()
        if len(parts) != 4 or not SHA.match(parts[1]):
            raise GateError(f"malformed pre-push ref line: {ln!r}")
        if parts[1] != ZERO:
            shas.append(git(root, "rev-parse", "--verify", f"{parts[1]}^{{commit}}"))
    return list(dict.fromkeys(shas))


def run_config(root, workspace, sha, args):
    """Resolve the pinned configuration and running tool before materialising anything."""
    cfg = load_config(root, sha)
    tool_sha = getattr(args, "tool_sha", None)
    if tool_sha and tool_sha != cfg["tool_sha"]:
        # Tool fixes go forward: a walk-back push of an older sha may run under the newer tool its HEAD pins.
        meta = Path(workspace) / "bennett"
        z = subprocess.run(["git", "-C", str(meta), "merge-base", "--is-ancestor", cfg["tool_sha"], tool_sha],
                           capture_output=True, text=True, env=git_env(), stdin=subprocess.DEVNULL)
        if z.returncode != 0:
            raise GateError(f"{sha} pins tool_sha {cfg['tool_sha']}, not an ancestor of the running {tool_sha} in {meta}"
                            f" ({z.stderr.strip() or 'git exit ' + str(z.returncode)}): push from a HEAD with that pin or a newer one")
    cfg["tool_sha_ran"] = tool_sha or cfg["tool_sha"]
    return cfg


def prepare(root, workspace, sha, args, live=False, cfg=None, prefix=None):
    """A clean detached worktree of sha with its siblings beside it. Returns everything a run needs."""
    if cfg is None:
        cfg = run_config(root, workspace, sha, args)
    if cfg["tool_sha_ran"] != cfg["tool_sha"]:
        say(f"{sha} pins tool_sha {cfg['tool_sha']}, an ancestor of the running {cfg['tool_sha_ran']}: running the newer tool")
    if prefix is None:
        prefix = [] if getattr(args, "no_isolate", False) or live else isolation_prefix(workspace, [root])
    if getattr(args, "no_isolate", False) or live:
        if not live:
            say("ISOLATION OFF: absolute reads of live sibling trees would go undetected; this run is not a push gate")
    sibs = Siblings(cfg, root, workspace)
    if not live:
        for name in sibs.pins:
            sibs.materialise(name)
        for name in sibs.pins:
            sibs.build(name, prefix)
    layout = root / ".tmp/gate/runs" / sha
    wt = layout / cfg["repo"]
    remove_worktree(root, wt)
    shutil.rmtree(layout, ignore_errors=True)
    layout.mkdir(parents=True)
    git(root, "worktree", "add", "--detach", str(wt), sha)
    ctx = {"wt": wt, "root": root, "layout": layout}
    for name in sibs.pins:
        target = sibs.owner(name) if live else sibs.path(name)
        (layout / name).symlink_to(target)
        ctx[f"sibling:{name}"] = target
    env = base_env(wt / ".tmp/gate-tmp")
    env["BENNETT_GATE_LAYOUT"] = str(layout)
    env.update({k: expand(v, ctx) for k, v in cfg.get("env", {}).items()})
    return cfg, sibs, prefix, layout, wt, ctx, env


def cleanup(root, layout, wt, keep):
    if keep:
        say(f"kept {layout}")
        return
    remove_worktree(root, wt)
    shutil.rmtree(layout, ignore_errors=True)


def machine_label(nproc, mem_total_kib):
    for name, value in (("machine.nproc", nproc), ("machine.mem_total_kib", mem_total_kib)):
        if isinstance(value, dict):
            raise ValueError(f"{name} unavailable: {value['unavailable']}")
    hardware = json.dumps([platform.machine(), nproc, mem_total_kib])
    return "machine-" + hashlib.sha256(hardware.encode()).hexdigest()[:12]


def machine_profile():
    """Independent start-of-run probes; a missing source never supplies a number."""
    memory = receipt_probe("machine.meminfo", lambda: dict(
        line.split(":", 1) for line in Path("/proc/meminfo").read_text().splitlines()))
    profile = {}
    for field, key in (("mem_total_kib", "MemTotal"), ("mem_available_kib", "MemAvailable")):
        profile[field] = (memory if "unavailable" in memory else
                          receipt_probe(f"machine.{field}", lambda: int(memory[key].split()[0])))
    profile["nproc"] = receipt_probe("machine.nproc", lambda: len(os.sched_getaffinity(0)))
    profile["load1"] = receipt_probe("machine.load1", lambda: os.getloadavg()[0])
    profile["label"] = receipt_probe("machine.label", lambda: machine_label(
        profile["nproc"], profile["mem_total_kib"]))
    return profile


def read_pass_receipt(path, key, tree):
    try:
        receipt = json.loads(path.read_text())
        if (not isinstance(receipt, dict) or receipt.get("key") != key or receipt.get("tree") != tree
                or receipt.get("result") != "pass" or not isinstance(receipt.get("sha"), str)
                or not SHA.fullmatch(receipt["sha"])
                or "finished_utc" not in receipt):
            raise ValueError("invalid PASS receipt or content key mismatch")
        return receipt
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as error:
        say(f"receipt {path} unreadable: {error}; ignored")
        return None


def gate_one(root, workspace, sha, args):
    with Lock(root / ".tmp/gate/locks" / f"run-{sha}", blocking=False):
        started = receipt_probe("setup_seconds", lambda: time.monotonic())
        cfg = run_config(root, workspace, sha, args)
        prefix = [] if getattr(args, "no_isolate", False) else isolation_prefix(workspace, [root])
        tree = git(root, "rev-parse", f"{sha}^{{tree}}")
        key = hashlib.sha256(json.dumps([tree, cfg["tool_sha_ran"], bool(prefix)], sort_keys=True).encode()).hexdigest()
        receipt_path = workspace / cfg["repo"] / ".tmp/gate/receipts" / f"{key}.json"
        record = {"sha": sha, "repo": cfg["repo"], "tool_sha": cfg["tool_sha"],
                  "tool_sha_ran": cfg["tool_sha_ran"], "isolated": bool(prefix)}
        records = root / ".tmp/gate/records"
        records.mkdir(parents=True, exist_ok=True)
        record_path = records / f"{sha}.json"
        if not getattr(args, "fresh", False):
            receipt = read_pass_receipt(receipt_path, key, tree)
            if receipt is not None:
                record.update(result="pass", finished_utc=receipt["finished_utc"],
                              covered_by={"sha": receipt["sha"], "receipt": str(receipt_path)})
                record_path.write_text(json.dumps(record, indent=1) + "\n")
                say(f"PASS {sha} covered by receipt {receipt_path}: tree {tree[:12]} "
                    f"gated as {receipt['sha'][:12]} at {receipt['finished_utc']}")
                return 0
        else:
            record["fresh"] = True
        machine = receipt_probe("machine", machine_profile)
        cfg, sibs, prefix, layout, wt, ctx, env = prepare(root, workspace, sha, args, cfg=cfg, prefix=prefix)
        setup_seconds = elapsed_seconds("setup_seconds", started)
        timeout = cfg.get("timeout_s")
        say(f"gating {sha} of {cfg['repo']} in {wt}")
        for name, note in sibs.notes.items():
            say(f"pin {name} = {note['sha']}")
        try:
            checks = run_commands(cfg["check"], wt, env, ctx, prefix, timeout, "check")
            passed = len(checks) == len(cfg["check"]) and all(c["exit"] == 0 for c in checks)
            reports = run_commands(cfg.get("report", []), wt, env, ctx, prefix, timeout, "report")
            for r in reports:
                print(f"gate: report {r['name']} exited {r['exit']} (evidence, never the gate's exit)", flush=True)
        finally:
            cleanup(root, layout, wt, getattr(args, "keep", False))
        record.update({
            "setup_seconds": setup_seconds, "machine": machine,
            "width_env": receipt_probe("width_env", lambda: width_env(env)),
            "siblings": {name: {**note, "cache_state": receipt_probe(
                f"siblings.{name}.cache_state", lambda: note["cache_state"])}
                for name, note in sibs.notes.items()},
            "checks": checks, "reports": reports, "result": "pass" if passed else "fail",
            "finished_utc": receipt_probe("finished_utc", lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())),
        })
        record_path.write_text(json.dumps(record, indent=1) + "\n")
        if passed:
            receipt_path.parent.mkdir(parents=True, exist_ok=True)
            pending = receipt_path.with_suffix(f".tmp{os.getpid()}")
            try:
                pending.write_text(json.dumps(dict(record, tree=tree, key=key), indent=1) + "\n")
                pending.replace(receipt_path)
            finally:
                pending.unlink(missing_ok=True)
        say(f"{'PASS' if passed else 'FAIL'} {sha}")
        return 0 if passed else EXIT_FAIL


def cmd_run(args):
    root, workspace = repo_paths(args.repo)
    for sha in resolve_shas(args, root):
        code = gate_one(root, workspace, sha, args)
        if code:
            return code
    return 0


def cmd_verify(args):
    """Preflight: materialise every pin and check its hashes and builds; run no check."""
    root, workspace = repo_paths(args.repo)
    for sha in resolve_shas(args, root):
        cfg = load_config(root, sha)
        sibs = Siblings(cfg, root, workspace)
        prefix = [] if args.no_isolate else isolation_prefix(workspace, [root])
        for name in sibs.pins:
            sibs.materialise(name)
        for name in sibs.pins:
            sibs.build(name, prefix)
        for name, note in sibs.notes.items():
            print(f"{name} {note['sha']} pushed={note['pushed']} at {sibs.paths[name]}")
    return 0


def live_scan(root, workspace, sha, cfg):
    """Static evidence: tracked non-doc text at sha naming a sibling path. Never decides a gate."""
    names = sorted(p.name for p in workspace.iterdir() if p.is_dir() and not p.name.startswith(".") and p.resolve() != root)
    pinned = set(cfg.get("siblings", {}))
    if not names:
        return []
    alt = "|".join(re.escape(n) for n in names)
    pattern = f"{re.escape(str(workspace))}/({alt})([^a-zA-Z0-9_-]|$)|(\\.\\./|parent ?/ ?[f]?[\"'])({alt})([^a-zA-Z0-9_-]|$)"
    exclude = list(SCAN_EXCLUDE) + [f":!{p}" for p in cfg.get("scan_exclude", [])]
    z = git(root, "grep", "-I", "-n", "-E", pattern, sha, "--", ".", *exclude, check=False)
    rows = []
    for line in z.stdout.splitlines():
        _, path, number, text = line.split(":", 3)
        m = re.search(pattern, text)
        absolute = str(workspace) + "/" in m.group(0)
        name = m.group(1) if absolute else m.group(4)
        kind = "absolute" if absolute else ("relative-pinned" if name in pinned else "relative-unpinned")
        rows.append((kind, name, f"{path}:{number}"))
    return rows


def pin_drift(cfg, workspace):
    rows = []
    for name, pin in cfg.get("siblings", {}).items():
        owner = workspace / pin.get("repo", name)
        z = git(owner, "rev-list", "--left-right", "--count", f"{pin['sha']}...HEAD", check=False)
        if z.returncode != 0:
            rows.append(f"{name}: pin {pin['sha'][:12]} not comparable with live HEAD: {z.stderr.strip()}")
            continue
        ahead, behind = z.stdout.split()
        status = git(owner, "status", "--porcelain", "-uno", check=False).stdout.strip()
        rows.append(f"{name}: pin {pin['sha'][:12]} behind live HEAD by {behind}, ahead by {ahead}, live tree dirty: {bool(status)}")
    return rows


TRACE_CALLS = "open,openat,openat2,execve,stat,lstat,newfstatat,access,faccessat,faccessat2,readlink,readlinkat,statx"


def traced_live_reads(log, workspace, root):
    prefix = str(workspace) + "/"
    hits = {}
    for line in Path(log).read_text(errors="replace").splitlines():
        for path in re.findall(r'"((?:[^"\\]|\\.)*)"', line):
            if path.startswith(prefix) and not path.startswith(str(root) + "/") and path != str(root):
                hits[path] = hits.get(path, 0) + 1
    return hits


def cmd_report_live(args):
    """Evidence, never a stop: static scan, pin drift and optionally the checks run against live siblings."""
    root, workspace = repo_paths(args.repo)
    sha = git(root, "rev-parse", "--verify", f"{args.sha[0] if args.sha else 'HEAD'}^{{commit}}")
    cfg = load_config(root, sha)
    print(f"live-sibling evidence for {cfg['repo']} at {sha} (never a stop condition)")
    print("pin drift:")
    for row in pin_drift(cfg, workspace) or ["(no siblings pinned)"]:
        print(f"  {row}")
    rows = live_scan(root, workspace, sha, cfg)
    print(f"static references ({len(rows)}):")
    for kind, name, where in sorted(rows):
        print(f"  {kind} {name} {where}")
    if not args.run:
        return 0
    with Lock(root / ".tmp/gate/locks" / f"run-{sha}", blocking=False):
        cfg, _, _, layout, wt, ctx, env = prepare(root, workspace, sha, args, live=True)
        log = root / ".tmp/gate" / f"live-trace-{sha}.log"
        try:
            checks = []
            for c in cfg["check"]:
                single = dict(c)
                if args.trace:
                    single["argv"] = ["strace", "-f", "-qq", "-e", f"trace={TRACE_CALLS}", "-o", str(log), "-A", *c["argv"]]
                checks += run_commands([single], wt, env, ctx, [], cfg.get("timeout_s"), "check")
                if checks[-1]["exit"] != 0:
                    break
        finally:
            cleanup(root, layout, wt, False)
    ok = len(checks) == len(cfg["check"]) and all(c["exit"] == 0 for c in checks)
    print(f"consumer check against live siblings: {'PASS' if ok else 'FAIL'}")
    if args.trace and log.exists():
        hits = traced_live_reads(log, workspace, root)
        print(f"traced absolute reads of live siblings ({len(hits)}, log {log}):")
        for path, count in sorted(hits.items()):
            print(f"  {path} x{count}")
    return 0


def cmd_hook_check(args):
    """Does git's effective pre-push hook reach this repo's scripts/pre-push stub? Exit 0 iff it does."""
    root = Path(git(args.repo, "rev-parse", "--show-toplevel")).resolve()
    # Not through git(): that helper blanks core.hooksPath, the very setting asked about here.
    hook = Path(subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--path-format=absolute", "--git-path", "hooks/pre-push"],
        capture_output=True, text=True, check=True, env=git_env(),
    ).stdout.strip())
    stub = root / "scripts/pre-push"
    config = subprocess.run(["git", "-C", str(root), "config", "core.hooksPath"], capture_output=True, text=True, env=git_env()).stdout.strip() or "(unset)"
    print(f"core.hooksPath={config}; effective hook {hook}")
    if not (hook.is_file() and os.access(hook, os.X_OK)):
        say(f"no executable hook at {hook}: git would push ungated (core.hooksPath={config})")
        return EXIT_FAIL
    direct = hook.resolve() == stub.resolve()
    if not direct and not re.search(r"^\s*exec\s.*scripts/pre-push", hook.read_text(errors="replace"), re.M):
        say(f"{hook} does not chain to scripts/pre-push (stale copy?): replace it by the chaining wrapper")
        return EXIT_FAIL
    if not stub.is_file() or PROBE_VAR not in stub.read_text(errors="replace"):
        say(f"{stub} is not a gate stub: chain text looks right but cannot be probed without running the full gate")
        return EXIT_FAIL
    env = dict(git_env(), **{PROBE_VAR: "1"})
    try:
        z = subprocess.run([str(hook)], capture_output=True, text=True, env=env, stdin=subprocess.DEVNULL, timeout=60, cwd=root)
    except OSError as e:
        say(f"cannot execute {hook}: {e}")
        return EXIT_FAIL
    if z.returncode != 0 or PROBE_LINE not in z.stdout:
        say(f"probe of {hook} did not reach the stub: exit {z.returncode}: {z.stdout}{z.stderr}")
        return EXIT_FAIL
    print(f"{hook} chains to {stub}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("run", cmd_run), ("verify", cmd_verify), ("report-live", cmd_report_live), ("hook-check", cmd_hook_check)):
        p = sub.add_parser(name)
        p.set_defaults(fn=fn)
        p.add_argument("--repo", required=True)
        if name != "hook-check":
            p.add_argument("--sha", action="append", default=[])
        if name in ("run", "verify"):
            p.add_argument("--no-isolate", action="store_true")
        if name == "run":
            p.add_argument("--keep", action="store_true")
            p.add_argument("--fresh", action="store_true", help="run checks even when a PASS receipt covers this tree")
            p.add_argument("--tool-sha")
            p.add_argument("hook_args", nargs="*", help="remote name and url, as git passes them")
        if name == "report-live":
            p.add_argument("--run", action="store_true")
            p.add_argument("--trace", action="store_true")
    args = ap.parse_args()
    for s in INTERRUPTS:
        signal.signal(s, on_interrupt)
    try:
        return args.fn(args)
    except GateError as e:
        say(f"SETUP ERROR: {e}")
        return EXIT_SETUP
    except Interrupted as e:
        say(f"INTERRUPTED by signal {e.signum}: running command group killed, run worktree removed, no record")
        return 128 + e.signum


if __name__ == "__main__":
    sys.exit(main())
