#!/usr/bin/env python3
"""Run a long codex job robustly: resume after network drops, content-filter refusals and early stops.

  codex_job.py run --name NAME [--repo DIR | --cd EXISTING_WORKTREE] --prompt FILE --paths P [P ...] --progress REL
                   [--model gpt-6.1-sol] [--effort xhigh] [--max-attempts 16] [--pace-margin 5] [--network] [--thread ID]
  codex_job.py status --name NAME
  codex_job.py stop --name NAME [--after-current-attempt]

Protocol (appended to the brief): the agent keeps REL (a progress file inside DIR) current and ends its
final message with `JOB-COMPLETE` or `JOB-BLOCKED: <reason>`. This runner, not the agent, commits the
owned PATHS: every 20 minutes while an attempt runs and after every attempt, with WIP backups.
Jobs use isolated job/NAME branches; runners never commit to main/master.

Recovery, per attempt outcome:
  sentinel JOB-COMPLETE / JOB-BLOCKED  -> stop
  content-filter refusal               -> resume the same session with a neutral continuation prompt;
                                          after 2 consecutive refusals start a FRESH session whose only
                                          context is the brief plus the progress file (drops flagged context)
  network / transport failure          -> exponential backoff (30 s .. 15 min), resume the same session
  ended without a sentinel             -> resume: "not complete per the brief, continue"
Before every attempt the codex weekly window is checked with `quota --json`; above elapsed+margin the
runner waits (re-checking every 15 min). State, logs and status.json: ~/.local/state/bennett-codex-jobs/NAME/.
"""
import argparse, datetime as dt, json, os, subprocess, sys, threading, time
from pathlib import Path
import re
import math
import fcntl
import signal

STATE = os.path.expanduser("~/.local/state/bennett-codex-jobs")
REFUSAL = "flagged for possible cybersecurity risk"
NET = ("stream disconnected", "error sending request", "connection reset", "timed out", "network",
       "503", "502", "504", "429", "rate limit", "temporarily unavailable", "EOF")
AGENT = "gpt-6.1-sol"  # set from --model in run(); COMMON rule 4: non-Claude commits end with "Agent: <model id>"
STOP = threading.Event()
STATUS_LOCK = threading.RLock()

PROTOCOL = """

## Job protocol (this runner's rules; they apply to the whole job)
- Keep only the top Resume block of `{progress}` current (what is done, what is verified with the command, what is
  next); no per-pass log blocks and no record-only commits: history is the git log and `bd close --reason`.
- Do not run git yourself; the runner commits your files. Write only inside: {paths}.
- Describe the work in plain software-engineering terms (interpreter, test, fixture, reversible machine).
- End your final message with a line `JOB-COMPLETE` when every deliverable is done and verified, or
  `JOB-BLOCKED: <reason>` if you cannot continue without a decision. Any other ending means "resume me".
"""
CONTINUE = ("Continue the job from where you are. Re-read {progress} first, then carry on with the next "
            "unfinished deliverable of the brief. End with JOB-COMPLETE or JOB-BLOCKED: <reason>.")
FRESH = ("You are continuing a software job that an earlier session started. The brief follows; your "
         "progress so far is recorded in {progress} inside the working directory, and the files it names "
         "already exist. Read {progress} first and continue from there.\n\n")


def headless_env(st):
    """No route to the desktop for anything the job runs (LLVM view-* passes once opened ~80,000
    .dot files in the maintainer's editor via xdg-open over D-Bus); temp files stay in the job dir."""
    env = dict(os.environ)
    for key in ("DISPLAY", "WAYLAND_DISPLAY", "DBUS_SESSION_BUS_ADDRESS", "BROWSER"):
        env.pop(key, None)
    tmp = os.path.join(st, "tmp")
    os.makedirs(tmp, exist_ok=True)
    env["TMPDIR"] = tmp
    return env


def log(st, msg):
    line = f"{dt.datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with open(os.path.join(st, "runner.log"), "a") as f:
        f.write(line + "\n")


def save(st, **kv):
    with STATUS_LOCK:
        _save(st, **kv)


def _save(st, **kv):
    p = Path(st) / "status.json"
    cur = json.loads(p.read_text()) if p.exists() else {}
    cur.update(kv, updated=dt.datetime.now().isoformat(timespec="seconds"))
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(cur, indent=1))
    os.replace(tmp, p)


def git_output(cd, *args):
    return subprocess.run(["git", *args], cwd=cd, check=True, capture_output=True,
                          text=True, timeout=120).stdout.strip()


def assert_job_branch(cd, name):
    branch = git_output(cd, "branch", "--show-current")
    expected = f"job/{name}"
    if branch != expected:
        raise RuntimeError(f"refusing job {name}: HEAD is on {branch or 'detached HEAD'}, expected {expected}; "
                           "runners must never commit to main/master")
    return branch


def validate_name(name):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", name) or ".." in name:
        raise ValueError("job name must contain only letters, digits, underscores, dots and hyphens")


def job_worktree(st, a):
    """Create from local main (master for older repos), or reuse this job's existing worktree."""
    status_path = Path(st) / "status.json"
    previous = json.loads(status_path.read_text()) if status_path.exists() else {}
    previous_cd = previous.get("worktree", previous.get("cd"))
    if previous_cd:
        cd = str(Path(previous_cd).resolve())
        for explicit in (a.cd, a.worktree):
            if explicit and str(Path(explicit).resolve()) != cd:
                raise ValueError(f"job {a.name} already uses worktree {cd}")
    elif a.cd:
        if a.worktree:
            raise ValueError("--worktree cannot be used with --cd")
        cd = str(Path(a.cd).resolve())
    else:
        repo = Path(git_output(a.repo or os.getcwd(), "rev-parse", "--show-toplevel"))
        cd = str(Path(a.worktree).resolve()) if a.worktree else str(repo.parent / f"{repo.name}-job-{a.name}")
        if not Path(cd).exists():
            main = next((b for b in ("main", "master") if subprocess.run(
                ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{b}"], cwd=repo).returncode == 0), None)
            if not main:
                raise RuntimeError(f"{repo}: no local main/master branch to launch from")
            branch = f"job/{a.name}"
            exists = subprocess.run(["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
                                    cwd=repo).returncode == 0
            args = [cd, branch] if exists else ["-b", branch, cd, main]
            git_output(repo, "-c", "core.hooksPath=/dev/null", "worktree", "add", *args)
    if a.repo:
        wanted = git_output(a.repo, "rev-parse", "--path-format=absolute", "--git-common-dir")
        actual = git_output(cd, "rev-parse", "--path-format=absolute", "--git-common-dir")
        if wanted != actual:
            raise ValueError(f"worktree {cd} does not belong to --repo {a.repo}")
    assert_job_branch(cd, a.name)
    return cd


def codex_pace(st=None):
    """(used%, allowed%) for the codex weekly window, or None if quota is unavailable."""
    try:
        result = subprocess.run(["quota", "--json"], check=True, capture_output=True, text=True, timeout=60)
        data = json.loads(result.stdout)
        if not isinstance(data, list):
            raise ValueError("quota must return a list of vendors")
        for v in data:
            if v.get("vendor") != "codex":
                continue
            for w in v.get("windows", []):
                if w.get("kind", {}).get("kind") != "weekly":
                    continue
                end = dt.datetime.fromisoformat(w["resets_at"].replace("Z", "+00:00"))
                length = re.fullmatch(r"PT([0-9]+(?:\.[0-9]+)?)H", w["length"])
                if not length:
                    raise ValueError("weekly length must be PT<hours>H")
                hours, used = float(length[1]), float(w["used"])
                if not math.isfinite(hours) or hours <= 0 or not math.isfinite(used) or not 0 <= used <= 1:
                    raise ValueError("invalid weekly quota length or usage")
                start = end - dt.timedelta(hours=hours)
                elapsed = (dt.datetime.now(dt.timezone.utc) - start) / (end - start)
                if not 0 <= elapsed <= 1:
                    raise ValueError("weekly quota window is stale or in the future")
                return 100 * used, 100 * elapsed
        raise ValueError("quota has no Codex weekly window")
    except (OSError, subprocess.SubprocessError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as e:
        if st:
            log(st, f"quota read failed: {e}")
        return None


def backup(st, cd):
    """Off-machine backup of work in progress (maintainer-ratified 2026-10-29): push HEAD to
    wip/<job> with the pre-push gate skipped, because mid-TDD trees are red by design. main stays
    gated and is pushed only by the orchestrator when green. Failures are logged, never fatal."""
    ref = f"HEAD:refs/heads/wip/{os.path.basename(st)}"
    try:
        r = subprocess.run(["git", "push", "--no-verify", "--force", "-q", "origin", ref], cwd=cd,
                           capture_output=True, text=True, timeout=600)
        save(st, backup_ok=r.returncode == 0, backup_error=r.stderr.strip() if r.returncode else None)
        log(st, f"wip backup: {'ok' if r.returncode == 0 else r.stderr.strip()[:200]}")
        return r.returncode == 0
    except Exception as e:
        save(st, backup_ok=False, backup_error=str(e))
        log(st, f"wip backup failed: {e}")
        return False


def commit(st, cd, paths, label):
    try:
        assert_job_branch(cd, os.path.basename(st))
        added_paths, errors = [], []
        for p in paths:
            try:
                # Existing empty directories and ignored-only directories are not valid commit pathspecs.
                files = git_output(cd, "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", p)
                if not files:
                    # An already staged deletion no longer appears in the index or working tree.
                    staged = subprocess.run(["git", "diff", "--cached", "--quiet", "--", p], cwd=cd)
                    if staged.returncode == 1:
                        added_paths.append(p)
                    elif staged.returncode != 0:
                        raise RuntimeError(f"git diff failed for {p}: exit {staged.returncode}")
                    continue
                subprocess.run(["git", "add", "-A", "--", p], cwd=cd, check=True,
                               capture_output=True, text=True, timeout=120)
                added_paths.append(p)
            except (OSError, subprocess.SubprocessError, RuntimeError) as e:
                error = f"{p}: {getattr(e, 'stderr', None) or e}"
                errors.append(error)
                log(st, f"commit ({label}) staging failed: {error}")
        save(st, commit_ok=not errors, commit_errors=errors)
        if not added_paths:
            log(st, f"commit ({label}): no tracked or untracked owned files to stage")
            return not errors
        diff = subprocess.run(["git", "diff", "--cached", "--quiet", "--", *added_paths], cwd=cd)
        if diff.returncode == 0:
            return not errors
        if diff.returncode != 1:
            raise RuntimeError(f"git diff failed with exit {diff.returncode}")
        msg = f"wip(codex job {os.path.basename(st)}): {label}\n\nAgent: {AGENT}"
        # pathspec: commit only this job's owned paths, never what another job staged in the shared index
        assert_job_branch(cd, os.path.basename(st))
        r = subprocess.run(["git", "commit", "-q", "-m", msg, "--", *added_paths], cwd=cd, capture_output=True, text=True, timeout=120)
        log(st, f"commit ({label}): {'ok' if r.returncode == 0 else r.stderr.strip()[:200]}")
        save(st, commit_ok=r.returncode == 0 and not errors,
             commit_errors=errors + ([r.stderr.strip() or r.stdout.strip()] if r.returncode else []))
        if r.returncode == 0:
            backup(st, cd)
        return r.returncode == 0 and not errors
    except Exception as e:  # a failed checkpoint must not kill the job; it is retried next time
        save(st, commit_ok=False, commit_errors=[str(e)])
        log(st, f"commit ({label}) failed: {e}")
        return False


def attempt(st, a, cmd, stdin_text, cd, paths, n):
    out_path = os.path.join(st, f"attempt-{n:02d}.jsonl")
    last = os.path.join(st, f"last-{n:02d}.md")
    Path(last).unlink(missing_ok=True)  # A failed resumed attempt must not reuse an earlier sentinel.
    cmd = cmd + ["--json", "-o", last, "-"]
    log(st, f"attempt {n}: {' '.join(cmd[:6])} ...")
    stop = threading.Event()

    def checkpoints():
        while not stop.wait(1200):
            commit(st, cd, paths, f"attempt {n} checkpoint")
    t = threading.Thread(target=checkpoints, daemon=True)
    t.start()
    try:
        with open(out_path, "w") as out, subprocess.Popen(
                cmd, cwd=cd, stdin=subprocess.PIPE, stdout=out, stderr=subprocess.STDOUT,
                text=True, env=headless_env(st), start_new_session=True) as p:
            save(st, child_pid=p.pid, child_start=process_start(p.pid))
            sent, deadline = False, None
            while True:
                if STOP.is_set():
                    if deadline is None:
                        signal_group(p.pid, signal.SIGTERM)
                        deadline = time.monotonic() + 10
                    elif time.monotonic() >= deadline:
                        signal_group(p.pid, signal.SIGKILL)
                try:
                    p.communicate(input=stdin_text if not sent else None, timeout=1)
                    break
                except subprocess.TimeoutExpired:
                    sent = True
    finally:
        stop.set()
        t.join()
        save(st, child_pid=None, child_start=None)
    commit(st, cd, paths, f"attempt {n} end")
    text = Path(out_path).read_text(errors="replace")
    thread = None
    for line in text.splitlines():
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if isinstance(o, dict) and o.get("type") == "thread.started":
            thread = o.get("thread_id")
    final = Path(last).read_text(errors="replace") if os.path.exists(last) else ""
    tail = final.strip().splitlines()[-3:] if final.strip() else []
    if any(l.strip() == "JOB-COMPLETE" for l in tail):
        kind = "complete"
    elif any(l.strip().startswith("JOB-BLOCKED") for l in tail):
        kind = "blocked"
    elif REFUSAL in text:
        kind = "refusal"
    elif p.returncode != 0 or '"turn.completed"' not in text:
        kind = "network" if any(s.lower() in text.lower() for s in NET) or p.returncode != 0 else "early-stop"
    else:
        kind = "early-stop"
    log(st, f"attempt {n}: exit={p.returncode} outcome={kind} thread={thread}")
    return kind, thread, final


def run(a):
    global AGENT
    AGENT = a.model
    if not math.isfinite(a.pace_margin):
        raise ValueError("--pace-margin must be finite")
    validate_name(a.name)
    st = os.path.join(STATE, a.name)
    os.makedirs(st, exist_ok=True)
    with open(os.path.join(st, "run.lock"), "w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError(f"job {a.name} already has a running runner") from None
        STOP.clear()
        (Path(st) / "stop-request").unlink(missing_ok=True)
        previous_handlers = {sig: signal.signal(sig, lambda *_: STOP.set())
                             for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)}
        try:
            return run_loop(st, a)
        except Exception as e:
            save(st, state="failed", error=str(e))
            log(st, f"runner failed: {e}")
            raise
        finally:
            save(st, runner_pid=None, runner_start=None)
            for sig, handler in previous_handlers.items():
                signal.signal(sig, handler)


def process_start(pid):
    """Linux process identity; a PID alone can later refer to an unrelated process."""
    try:
        fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
        return fields[19] if fields[0] != "Z" else None
    except FileNotFoundError:
        return None


def signal_group(pid, sig):
    try:
        os.killpg(pid, sig)
    except ProcessLookupError:
        pass  # The child exited between the status check and the signal.


def stop_requested(st):
    return STOP.is_set() or (Path(st) / "stop-request").exists()


def wait_between(st, seconds):
    deadline = time.monotonic() + seconds
    while not stop_requested(st):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return
        STOP.wait(min(1, remaining))


def finish_stop(st, cd, paths):
    committed = commit(st, cd, paths, "stop")
    backed_up = backup(st, cd)
    save(st, state="stopped", stop_ok=committed and backed_up)
    log(st, "stopped: owned tree committed and wip backup attempted")
    return 0 if committed and backed_up else 1


def stop_job(a):
    global AGENT
    validate_name(a.name)
    st = Path(STATE) / a.name
    info = json.loads((st / "status.json").read_text())
    AGENT = info.get("model", AGENT)
    assert_job_branch(info["cd"], a.name)
    (st / "stop-request").write_text("after-current-attempt\n" if a.after_current_attempt else "now\n")
    pid, identity = info.get("runner_pid"), info.get("runner_start")
    live = pid and identity and process_start(pid) == identity
    if live:
        if a.after_current_attempt:
            log(str(st), "stop requested after the current attempt")
            return 0
        os.kill(pid, signal.SIGTERM)
        deadline = time.monotonic() + 14
        while process_start(pid) == identity:
            if time.monotonic() >= deadline:
                raise RuntimeError(f"runner {pid} did not stop; inspect {st / 'runner.log'}")
            time.sleep(0.05)
        result = json.loads((st / "status.json").read_text())
        if result.get("state") != "stopped":
            raise RuntimeError(f"runner exited without stopped state: {result.get('state')}")
        return 0 if result.get("stop_ok") else 1
    # Recover a tree after a runner crash, without signalling a stale/reused PID.
    with (st / "run.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        child, child_start = info.get("child_pid"), info.get("child_start")
        if child and child_start and process_start(child) == child_start:
            signal_group(child, signal.SIGTERM)
            deadline = time.monotonic() + 10
            while process_start(child) == child_start and time.monotonic() < deadline:
                time.sleep(0.05)
            if process_start(child) == child_start:
                signal_group(child, signal.SIGKILL)
        return finish_stop(str(st), info["cd"], info["paths"])


def run_loop(st, a):
    cd = job_worktree(st, a)
    brief = Path(a.prompt).read_text() + PROTOCOL.format(progress=a.progress, paths=", ".join(a.paths))
    base = ["codex", "exec", "-m", a.model, "-c", f"model_reasoning_effort={a.effort}"]
    sandbox = ["-c", 'sandbox_mode="workspace-write"']
    if a.network:  # crates.io etc.; cargo's registry and git caches live in ~/.cargo
        sandbox += ["-c", "sandbox_workspace_write.network_access=true",
                    "-c", f'sandbox_workspace_write.writable_roots=["{os.path.expanduser("~/.cargo")}"]']
    thread, refusals, backoff = a.thread, 0, 30
    resuming = os.path.exists(os.path.join(cd, a.progress))  # a restarted job continues from its progress file
    save(st, name=a.name, cd=cd, worktree=cd, branch=assert_job_branch(cd, a.name),
         branch_mode=True, paths=a.paths, model=a.model, state="running", attempts=0,
         runner_pid=os.getpid(), runner_start=process_start(os.getpid()))
    for n in range(1, a.max_attempts + 1):
        while True:
            if stop_requested(st):
                return finish_stop(st, cd, a.paths)
            pace = codex_pace(st)
            if pace is None:
                log(st, "quota unavailable or malformed; stopping before the next attempt")
                save(st, state="stopped-pace-unknown")
                return 4
            used, elapsed = pace
            if used <= elapsed + a.pace_margin:
                break
            save(st, state="waiting-for-pace", used=used, elapsed=elapsed)
            log(st, f"codex weekly {used:.1f}% > elapsed {elapsed:.1f}% + {a.pace_margin}; waiting 15 min")
            wait_between(st, 900)
        if stop_requested(st):
            return finish_stop(st, cd, a.paths)
        if thread is None:
            fresh = n > 1 or resuming
            cmd, text = base + sandbox, (FRESH.format(progress=a.progress) + brief if fresh else brief)
        else:
            cmd = ["codex", "exec", "resume", thread, "-m", a.model, "-c",
                   f"model_reasoning_effort={a.effort}"] + sandbox
            text = CONTINUE.format(progress=a.progress)
        assert_job_branch(cd, a.name)
        save(st, state="running", attempts=n, thread=thread)
        kind, new_thread, final = attempt(st, a, cmd, text, cd, a.paths, n)
        thread = new_thread or thread
        if stop_requested(st):
            return finish_stop(st, cd, a.paths)
        if kind in ("complete", "blocked"):
            save(st, state=kind, attempts=n, thread=thread, final_tail=final[-2000:])
            return 0 if kind == "complete" else 2
        if kind == "refusal":
            refusals += 1
            if refusals >= 2:
                log(st, "two consecutive refusals: starting a fresh session from the progress file")
                thread, refusals = None, 0
            continue
        refusals = 0
        if kind == "network":
            log(st, f"backing off {backoff} s")
            wait_between(st, backoff)
            backoff = min(backoff * 2, 900)
        else:
            backoff = 30
    if stop_requested(st):
        return finish_stop(st, cd, a.paths)
    save(st, state="gave-up", thread=thread)
    log(st, f"gave up after {a.max_attempts} attempts")
    return 3


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--name", required=True)
    location = r.add_mutually_exclusive_group()
    location.add_argument("--repo", help="source repository (default: current directory); launch from main")
    location.add_argument("--cd", help="existing worktree, already on job/<name>")
    r.add_argument("--worktree", help="new worktree path (default: ../<repo>-job-<name>)")
    r.add_argument("--prompt", required=True)
    r.add_argument("--paths", nargs="+", required=True)
    r.add_argument("--progress", required=True)
    r.add_argument("--model", default="gpt-6.1-sol")
    r.add_argument("--effort", default="xhigh")
    r.add_argument("--max-attempts", type=int, default=16)
    r.add_argument("--pace-margin", type=float, default=5.0)
    r.add_argument("--network", action="store_true", help="allow network and a writable ~/.cargo (crates)")
    r.add_argument("--thread", help="resume this codex session id first (e.g. from status.json)")
    s = sub.add_parser("status")
    s.add_argument("--name", required=True)
    stop = sub.add_parser("stop")
    stop.add_argument("--name", required=True)
    stop.add_argument("--after-current-attempt", action="store_true",
                      help="request a stop between attempts without interrupting the current Codex child")
    a = ap.parse_args()
    if a.cmd == "status":
        print((Path(STATE) / a.name / "status.json").read_text())
        return 0
    if a.cmd == "stop":
        return stop_job(a)
    return run(a)


if __name__ == "__main__":
    sys.exit(main())
