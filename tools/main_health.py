#!/usr/bin/env python3
"""Local post-merge evidence only: never a push hook, scheduler, or revert tool."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
from enum import Enum
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import tomllib

# Scope, polling, wait, memory and load convention: s4/qgate.sh / R33, 2026-11-07.
POLL_SECONDS = 60
MAX_WAIT_SECONDS = 7200
MIN_AVAILABLE_GIB = 6
MAX_LOAD = 12
# Hang guards only, never verdict budgets: s4/qgate.sh (7000s), 2026-11-07.
COMMAND_TIMEOUT_SECONDS = 7000
# Git/help hang guard mirrors gate_run.py hook probe's 60s guard, 2026-11-07.
CONTROL_TIMEOUT_SECONDS = 60
# Termination grace uses timeout's TERM/KILL convention; local guard policy, 2026-11-07.
KILL_GRACE_SECONDS = 30
LADDER_REPOS = ("bennett-plugin", "bennett-vm", "bennett-runtimes",
                "bennett-driver", "bennett-isa-spec")
RUNGS = ("rung-1", "rung-2")


class HealthError(Exception):
    pass


class Result(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"
    UNKNOWN = "UNKNOWN"


def environment(tmp=None, workspace=None):
    env = {key: value for key, value in os.environ.items()
           if key not in {"DISPLAY", "WAYLAND_DISPLAY", "DBUS_SESSION_BUS_ADDRESS", "BROWSER",
                          "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "CARGO_TARGET_DIR",
                          "PYTHONOPTIMIZE"} and not key.startswith("BENNETT_GATE_")}
    if tmp is not None:
        tmp.mkdir(parents=True, exist_ok=True)
        env["TMPDIR"] = str(tmp)
    if workspace is not None:
        env["BENNETT_GATE_WORKSPACE"] = str(workspace)
    # R36 build parallelism convention, 2026-11-07; gate.toml retains final authority.
    env.update(CARGO_BUILD_JOBS="3", RUST_TEST_THREADS="4")
    return env


def control(argv, cwd=None, env=None, allowed=(0,)):
    proc = subprocess.run([str(arg) for arg in argv], cwd=cwd, env=env or environment(),
                          stdin=subprocess.DEVNULL, capture_output=True, text=True,
                          timeout=CONTROL_TIMEOUT_SECONDS)
    if proc.returncode not in allowed:
        raise HealthError(f"{' '.join(map(str, argv))}: exit {proc.returncode}: {proc.stderr.strip()}")
    return proc


def git(repo, *args):
    return control(["git", "-c", "core.hooksPath=/dev/null", "-C", repo, *args]).stdout.strip()


def main_checkout(repo):
    return Path(git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")).parent


def heavy_blocker():
    scopes = control(["systemctl", "--user", "list-units", "--type=scope", "--no-legend"]).stdout
    heavy = [line.strip() for line in scopes.splitlines() if "bennett-heavy" in line]
    if heavy:
        return "; ".join(heavy)
    # Same legacy out-of-scope gate detection as s4/qgate.sh, 2026-11-07.
    gates = control(["pgrep", "-f", r"gate_run-[0-9a-f]*\.py run --repo"], allowed=(0, 1))
    if gates.returncode == 0:
        return f"gate processes: {gates.stdout.strip()}"
    available = None
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable:"):
            available = int(line.split()[1]) / (1024 * 1024)
    if available is None:
        raise HealthError("/proc/meminfo has no MemAvailable")
    load = float(Path("/proc/loadavg").read_text().split()[0])
    if available < MIN_AVAILABLE_GIB or load >= MAX_LOAD:
        return f"resources: {available:.1f} GiB available, load {load:.2f}"
    return None


def wait_for_slot(max_wait):
    deadline = time.monotonic() + max_wait
    while True:
        reason = heavy_blocker()
        if reason is None:
            return
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(f"heavy slot wait guard expired: {reason}")
        print(f"main-health: waiting: {reason}", file=sys.stderr, flush=True)
        time.sleep(min(POLL_SECONDS, remaining))


@contextmanager
def single_runner(state):
    with (state / "runner.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise HealthError(f"another main-health runner owns {state}/runner.lock") from exc
        yield


def detached(repo, sha, state, name):
    target = state / name / sha / name
    if target.exists():
        if git(target, "rev-parse", "HEAD") != sha or git(target, "status", "--porcelain", "--untracked-files=no"):
            raise HealthError(f"cached checkout is modified: {target}")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        git(repo, "worktree", "add", "--detach", str(target), sha)
    return target


def fetch_main(repo):
    git(repo, "fetch", "--no-tags", "origin", "+refs/heads/main:refs/remotes/origin/main")
    return git(repo, "rev-parse", "--verify", "refs/remotes/origin/main^{commit}")


def ladder_argv(stub, revisions, help_text, output):
    argv = ["bash", str(stub), "--output", str(output), "--jobs", "3"]
    for name, sha in revisions.items():
        option = "--" + name.removeprefix("bennett-") + "-rev"
        if option not in re.findall(r"--[a-z0-9-]+", help_text):
            raise HealthError(f"{stub}: missing {option}; cannot attest current origin/main {name}")
        argv.extend([option, sha])
    return argv


def cache_isolation(checkout):
    """Keep this nested cache visible after the pinned tool masks the live meta checkout.

    The pinned tool's prefix skips only top-level own_roots. Restore just the detached
    root (including its pinned-sibling cache), never the containing live checkout.
    Reject unfamiliar prefixes instead of accidentally weakening sibling isolation.
    """
    wrapper = checkout / ".tmp/main-health-bwrap"
    wrapper.parent.mkdir(parents=True, exist_ok=True)
    wrapper.write_text(f'''#!{sys.executable}
import os
import sys
args = sys.argv[1:]
if args[:4] != ["--dev-bind", "/", "/", "--die-with-parent"]:
    sys.exit("main-health: unsupported gate isolation prefix")
index = 4
while index < len(args) and args[index] == "--tmpfs":
    if args[index + 2:index + 3] != ["--bind-try"] or len(args[index:index + 5]) != 5:
        sys.exit("main-health: unsupported gate isolation mount")
    index += 5
if index >= len(args) or args[index].startswith("--"):
    sys.exit("main-health: unsupported gate isolation command")
os.execvp("bwrap", ["bwrap", *args[:index], "--bind", {str(checkout)!r}, {str(checkout)!r}, *args[index:]])
''')
    wrapper.chmod(0o755)
    return str(wrapper)


def execute(argv, cwd, log, env, max_wait, timeout):
    wait_for_slot(max_wait)
    unit = f"bennett-heavy-main-health-{os.getpid()}-{time.time_ns()}"
    exit_file = log.with_suffix(".exit")
    # Distinguish a failed scope launch from the gate's own exit 1.
    child = 'status=$1; shift; "$@"; code=$?; printf "%s\\n" "$code" > "$status"; exit "$code"'
    command = ["systemd-run", "--user", "--scope", "-q", f"--unit={unit}",
               "timeout", "--signal=TERM", f"--kill-after={KILL_GRACE_SECONDS}s", str(timeout),
               "bash", "-c", child, "main-health", str(exit_file), *argv]
    with log.open("a") as output:
        output.write(f"command: {json.dumps(command)}\n")
        output.flush()
        proc = subprocess.run(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                              stdout=output, stderr=subprocess.STDOUT)
        output.write(f"exit: {proc.returncode}\n")
    if proc.returncode == 124:
        return Result.TIMEOUT, proc.returncode
    if proc.returncode < 0 or proc.returncode in (137, 143):
        return Result.UNKNOWN, proc.returncode
    if not exit_file.is_file():
        raise HealthError(f"scope exited {proc.returncode} without a child exit record; see {log}")
    if int(exit_file.read_text()) != proc.returncode:
        raise HealthError(f"scope and child exit codes differ; see {log}")
    return {0: Result.PASS, 1: Result.FAIL}.get(proc.returncode, Result.ERROR), proc.returncode


def blank_row():
    return {"sha": "", "shas": {}, "result": Result.UNKNOWN.value, "when": "",
            "duration_s": None, "log": "", "delta": "not checked", "last_green_shas": {},
            "merges": {}, "detail": "not checked", "table": ""}


def markdown(rows):
    lines = ["# Main health", "", "| Repo / ladder | SHA(s) | Result | When (UTC) | Seconds | Delta | Log |",
             "|---|---|---|---|---:|---|---|"]
    details = []
    for name, row in rows.items():
        shas = ", ".join(f"{repo}: {sha[:12]}" for repo, sha in row["shas"].items()) or "—"
        duration = "—" if row["duration_s"] is None else f'{row["duration_s"]:.2f}'
        log = f'[log]({row["log"]})' if row["log"] else "—"
        lines.append(f'| {name} | {shas} | {row["result"]} | {row["when"] or "—"} | '
                     f'{duration} | {row["delta"].replace("|", "/")} | {log} |')
        if row["detail"]:
            details.extend(["", f'{name}: {row["detail"].replace(chr(10), " ")}', ""])
        for repo, merges in row["merges"].items():
            details.extend(["", f"{name}, {repo}: merges since last green:", "", *[f"- {merge}" for merge in merges], ""])
        if row["table"]:
            details.extend(["", f"## {name}: per-major evidence", "", row["table"], ""])
    return "\n".join(lines + details) + "\n"


def save_status(state, rows):
    for name, content in (("status.json", json.dumps({"schema": 1, "rows": rows}, indent=2) + "\n"),
                          ("status.md", markdown(rows))):
        pending = state / (name + ".new")
        pending.write_text(content)
        pending.replace(state / name)


class Runner:
    def __init__(self, args):
        self.args = args
        self.meta = args.meta.resolve()
        self.workspace = self.meta.parent
        self.state = args.state_dir.resolve() if args.state_dir else self.meta / ".tmp/main-health"
        manifest = tomllib.loads((self.meta / "manifest.toml").read_text())
        self.repos = manifest["repos"]
        for name, entry in self.repos.items():
            if not re.fullmatch(r"[A-Za-z0-9_.-]+", name) or not isinstance(entry.get("path"), str):
                raise HealthError(f"invalid manifest entry: {name}")
        self.selected = args.repos.split(",") if args.repos is not None else ([] if args.ladder else list(self.repos))
        self.rungs = args.ladder.split(",") if args.ladder is not None else ([] if args.repos else list(RUNGS))
        for name in self.selected:
            if name not in self.repos:
                raise HealthError(f"repo absent from manifest: {name}")
        for rung in self.rungs:
            if rung not in RUNGS:
                raise HealthError(f"unknown ladder rung: {rung}")
        self.state.mkdir(parents=True, exist_ok=True)
        self.shas = {}

    def source(self, name):
        if name not in self.repos:
            raise HealthError(f"repo absent from manifest: {name}")
        return (self.workspace / self.repos[name]["path"]).resolve()

    def revision(self, name):
        if name not in self.shas:
            self.shas[name] = fetch_main(self.source(name))
        return self.shas[name]

    def gate(self, name, revisions, log):
        checkout = detached(self.source(name), revisions[name], self.state, name)
        for path in ("gate.toml", "scripts/pre-push"):
            if not (checkout / path).is_file():
                raise HealthError(f"{name} origin/main lacks {path}")
        env = environment(self.state / "tmp", self.workspace)
        env["BENNETT_GATE_BWRAP"] = cache_isolation(checkout)
        return execute(["bash", str(checkout / "scripts/pre-push"), "--sha", revisions[name]],
                       checkout, log, env,
                       self.args.max_wait, self.args.command_timeout)

    def ladder(self, rung, revisions, log, row):
        name = "bennett-conformance"
        checkout = detached(self.source(name), revisions[name], self.state, name)
        stub = checkout / "ladder" / rung / "gate.sh"
        if not stub.is_file():
            raise HealthError(f"{name} origin/main lacks ladder/{rung}/gate.sh")
        env = environment(self.state / "tmp", self.workspace)
        help_text = control(["bash", stub, "--help"], cwd=checkout, env=env).stdout
        output = log.with_suffix("")
        argv = ladder_argv(stub, {name: revisions[name] for name in LADDER_REPOS}, help_text, output)
        # These are object sources for the ladder's revision selectors; never substitute HEAD.
        for name in LADDER_REPOS:
            link = checkout.parent / name
            if not link.exists():
                link.symlink_to(self.source(name), target_is_directory=True)
        result, code = execute(argv, checkout, log, env, self.args.max_wait, self.args.command_timeout)
        tables = sorted(output.rglob("table.md")) if output.exists() else []
        row["table"] = "\n\n".join(path.read_text() for path in tables)
        if not tables and result in (Result.PASS, Result.FAIL):
            raise HealthError(f"{stub}: exit {code} but no per-major table.md under {output}")
        return result, code

    def check(self, name, previous):
        row = blank_row()
        row["last_green_shas"] = previous["last_green_shas"].copy()
        started = time.monotonic()
        log = self.state / "logs" / f'{name.replace("/", "-")}-{time.time_ns()}.log'
        log.parent.mkdir(parents=True, exist_ok=True)
        row["log"] = str(log)
        try:
            names = ("bennett-conformance", *LADDER_REPOS) if name.startswith("ladder/") else (name,)
            for repo in names:
                row["shas"][repo] = self.revision(repo)
            row["sha"] = row["shas"][names[0]]
            if row["shas"] == previous["shas"] and previous["result"] in (Result.PASS, Result.FAIL) and not self.args.force:
                return dict(previous, delta="unchanged"), False
            if name.startswith("ladder/"):
                result, code = self.ladder(name.split("/")[1], row["shas"], log, row)
            else:
                result, code = self.gate(name, row["shas"], log)
            row.update(result=result.value, detail=f"exit {code}", exit=code)
        except (TimeoutError, subprocess.TimeoutExpired) as exc:
            row.update(result=Result.TIMEOUT.value, detail=str(exc))
        except (HealthError, OSError, ValueError) as exc:
            row.update(result=Result.ERROR.value, detail=str(exc))
        row["when"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        row["duration_s"] = time.monotonic() - started
        row["delta"] = f'{previous["result"]} → {row["result"]}'
        if row["shas"] != previous["shas"]:
            row["delta"] += "; revisions changed"
        if row["result"] == Result.PASS:
            row["last_green_shas"] = row["shas"].copy()
        else:
            for repo, sha in row["shas"].items():
                green = row["last_green_shas"].get(repo)
                if green and green != sha:
                    try:
                        row["merges"][repo] = git(self.source(repo), "log", "--merges", "--format=%H %s", f"{green}..{sha}").splitlines()
                    except (HealthError, OSError, subprocess.TimeoutExpired) as exc:
                        row.update(result=Result.ERROR.value, detail=f'merge attribution failed: {exc}')
                elif not green:
                    row["detail"] += f"; {repo}: no prior green SHA for merge attribution"
        with log.open("a") as output:
            output.write(row["detail"] + "\n")
        return row, True

    def cycle(self):
        self.shas.clear()
        status = self.state / "status.json"
        rows = json.loads(status.read_text())["rows"] if status.exists() else {}
        for name in (*self.repos, *(f"ladder/{rung}" for rung in RUNGS)):
            rows.setdefault(name, blank_row())
        selected = [*self.selected, *(f"ladder/{rung}" for rung in self.rungs)]
        for name in selected:
            row, changed = self.check(name, rows[name])
            rows[name] = row
            if changed:
                with (self.state / "history.jsonl").open("a") as history:
                    history.write(json.dumps({"name": name, **row}) + "\n")
            save_status(self.state, rows)
        print(markdown(rows), flush=True)
        results = {rows[name]["result"] for name in selected}
        if results & {Result.ERROR, Result.TIMEOUT, Result.UNKNOWN}:
            return 2
        return 1 if Result.FAIL in results else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["run"])
    parser.add_argument("--meta", type=Path, help="main meta checkout (default: shared Git directory's parent)")
    parser.add_argument("--state-dir", type=Path, default=os.environ.get("BENNETT_MAIN_HEALTH_STATE_DIR"))
    parser.add_argument("--repos", help="comma-separated manifest names; alone selects repo gates only")
    parser.add_argument("--ladder", help="comma-separated rungs; alone selects ladder only")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--max-wait", type=float, default=MAX_WAIT_SECONDS, help="slot-wait hang guard (seconds)")
    parser.add_argument("--command-timeout", type=float, default=COMMAND_TIMEOUT_SECONDS, help="command hang guard (seconds)")
    args = parser.parse_args()
    try:
        if args.max_wait < 0 or args.command_timeout <= 0:
            raise HealthError("wait must be nonnegative and command timeout positive")
        if args.meta is None:
            args.meta = main_checkout(Path(__file__).resolve().parents[1])
        runner = Runner(args)
        with single_runner(runner.state):
            while True:
                code = runner.cycle()
                if args.once:
                    return code
                time.sleep(POLL_SECONDS)
    except (HealthError, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        print(f"main-health: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("main-health: interrupted", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
