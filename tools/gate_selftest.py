#!/usr/bin/env python3
"""Self-test for tools/gate_run.py. Builds throwaway repos, never touches a real one.

Run: TMPDIR=<project-local dir> python3 -I tools/gate_selftest.py
"""
import hashlib
import json
import os
import shutil
import signal
import stat
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
TOOL = TOOLS / "gate_run.py"
STUB = TOOLS / "gate_pre-push.template"
ZERO = "0" * 40
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(
    GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
    GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null",
)


def bwrap_works():
    if not shutil.which("bwrap"):
        return False
    return subprocess.run(["bwrap", "--dev-bind", "/", "/", "true"], capture_output=True).returncode == 0


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True, env=ENV).stdout.strip()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="gate-selftest-")).resolve()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.ws = self.tmp / "ws"
        self.ws.mkdir()
        self.tool_sha = "1" * 40
        self.sib = self.repo("sib", {"data.txt": "pinned\n", "build.sh": "#!/bin/sh\necho x >> \"$COUNT\"\nmkdir -p out\necho built-$(cat data.txt) > out/bin\n"})
        self.pin = git(self.sib, "rev-parse", "HEAD")
        # The live sibling then moves on and has a dirty tree: a concurrent job.
        self.commit(self.sib, {"data.txt": "moved\n"})
        (self.sib / "data.txt").write_text("dirty\n")
        self.me = self.repo("me", {"README": "me\n", ".gitignore": ".tmp/\n"})

    def repo(self, name, files):
        r = self.ws / name
        r.mkdir()
        git(r, "init", "-q", "-b", "main")
        self.commit(r, files)
        return r

    def commit(self, r, files):
        for path, text in files.items():
            p = r / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
            if text.startswith("#!"):
                p.chmod(p.stat().st_mode | stat.S_IXUSR)
        git(r, "add", "-A")
        git(r, "commit", "-qm", "c")
        return git(r, "rev-parse", "HEAD")

    def toml(self, checks, extra="", sib=None, tool_sha=None):
        sib = sib if sib is not None else f'[siblings.sib]\nsha = "{self.pin}"\n'
        text = f'schema = 1\nrepo = "me"\ntool_sha = "{tool_sha or self.tool_sha}"\n{extra}\n'
        for argv in checks:
            text += f"[[check]]\nname = {json.dumps(argv[0])}\nargv = {json.dumps(argv)}\n"
        return text + sib

    def adopt(self, checks, files=None, **kw):
        return self.commit(self.me, {"gate.toml": self.toml(checks, **kw), **(files or {})})

    def run_tool(self, *args, stdin=None, env=None, cmd="run"):
        full = dict(ENV, BENNETT_GATE_WORKSPACE=str(self.ws), **(env or {}))
        return subprocess.run(
            ["python3", "-I", str(TOOL), cmd, "--repo", str(self.me), *args],
            input=stdin if stdin is not None else "", capture_output=True, text=True, env=full, timeout=300,
        )

    def assertRan(self, z, code=0):
        self.assertEqual(z.returncode, code, z.stdout + z.stderr)


class Layout(Base):
    def test_sibling_relative_path_resolves_to_pin_not_live(self):
        script = "#!/bin/sh\ntest \"$(cat ../sib/data.txt)\" = pinned\ntest \"$(cat tracked.txt)\" = clean\n"
        sha = self.adopt([["./check.sh"]], {"check.sh": script, "tracked.txt": "clean\n"})
        (self.me / "tracked.txt").write_text("dirty\n")  # never the working tree
        self.assertRan(self.run_tool("--sha", sha))

    def test_own_check_failure_is_exit_one(self):
        sha = self.adopt([["./check.sh"]], {"check.sh": "#!/bin/sh\nexit 7\n"})
        self.assertRan(self.run_tool("--sha", sha), 1)

    def test_later_check_not_run_after_failure(self):
        sha = self.adopt([["./a.sh"], ["./b.sh"]], {"a.sh": "#!/bin/sh\nexit 1\n", "b.sh": f"#!/bin/sh\ntouch {self.tmp}/ran-b\n"})
        self.assertRan(self.run_tool("--sha", sha), 1)
        self.assertFalse((self.tmp / "ran-b").exists())

    def test_alias_names_another_repo(self):
        sib = f'[siblings.sib-review]\nsha = "{self.pin}"\nrepo = "sib"\n'
        sha = self.adopt([["./check.sh"]], {"check.sh": "#!/bin/sh\ntest \"$(cat ../sib-review/data.txt)\" = pinned\n"}, sib=sib)
        self.assertRan(self.run_tool("--sha", sha))

    def test_worktrees_are_removed_but_sibling_cache_kept(self):
        sha = self.adopt([["true"]])
        self.assertRan(self.run_tool("--sha", sha))
        self.assertFalse((self.me / ".tmp/gate/runs" / sha).exists())
        self.assertTrue((self.me / f".tmp/gate/cache/sib@{self.pin[:12]}/sib/data.txt").exists())
        self.assertNotIn(sha, git(self.me, "worktree", "list"))

    def test_record_names_the_pins_used(self):
        sha = self.adopt([["true"]])
        self.assertRan(self.run_tool("--sha", sha))
        rec = json.loads((self.me / ".tmp/gate/records" / f"{sha}.json").read_text())
        self.assertEqual(rec["siblings"]["sib"]["sha"], self.pin)
        self.assertEqual(rec["result"], "pass")

    def test_cached_sibling_tampering_is_rematerialised_loudly(self):
        sha = self.adopt([["./check.sh"]], {"check.sh": "#!/bin/sh\ntest \"$(cat ../sib/data.txt)\" = pinned\n"})
        self.assertRan(self.run_tool("--sha", sha))
        (self.me / f".tmp/gate/cache/sib@{self.pin[:12]}/sib/data.txt").write_text("tampered\n")
        z = self.run_tool("--sha", sha)
        self.assertRan(z)
        self.assertIn("rematerialis", z.stderr)


    def test_terminated_gate_kills_its_running_command_tree(self):
        # An orchestrator kill (R3, host memory) must not orphan the build or test tree under the gate.
        pidfile = self.tmp / "grandchild.pid"
        script = f"#!/bin/sh\nsh -c 'echo $$ > {pidfile}; exec sleep 300' &\nwait\n"
        sha = self.adopt([["./check.sh"]], {"check.sh": script})
        full = dict(ENV, BENNETT_GATE_WORKSPACE=str(self.ws))
        log = open(self.tmp / "gate.log", "w+")
        self.addCleanup(log.close)
        proc = subprocess.Popen(["python3", "-I", str(TOOL), "run", "--repo", str(self.me), "--sha", sha],
                                stdin=subprocess.DEVNULL, stdout=log, stderr=log, env=full)
        for _ in range(600):
            if pidfile.exists() and pidfile.read_text().strip():
                break
            time.sleep(0.05)
        else:
            proc.kill()
            self.fail("check never started")
        grandchild = int(pidfile.read_text())
        self.addCleanup(lambda: subprocess.run(["kill", "-9", str(grandchild)], capture_output=True))
        proc.terminate()
        proc.wait(timeout=60)
        err = (self.tmp / "gate.log").read_text()
        self.assertEqual(proc.returncode, 128 + signal.SIGTERM, err)
        self.assertIn("INTERRUPTED", err)
        for _ in range(100):
            try:
                os.kill(grandchild, 0)
            except ProcessLookupError:
                break
            time.sleep(0.05)
        else:
            os.kill(grandchild, signal.SIGKILL)
            self.fail(f"grandchild {grandchild} outlived the terminated gate")
        self.assertFalse((self.me / ".tmp/gate/runs" / sha).exists())
        self.assertFalse((self.me / ".tmp/gate/records" / f"{sha}.json").exists())


class Pins(Base):
    def test_missing_pin_file_fails_loud(self):
        z = self.run_tool("--sha", git(self.me, "rev-parse", "HEAD"))
        self.assertRan(z, 3)
        self.assertIn("gate.toml", z.stderr)

    def test_unknown_sha_fails_loud(self):
        sha = self.adopt([["true"]], sib=f'[siblings.sib]\nsha = "{"a" * 40}"\n')
        z = self.run_tool("--sha", sha)
        self.assertRan(z, 3)
        self.assertIn("not in", z.stderr)

    def test_abbreviated_sha_refused(self):
        sha = self.adopt([["true"]], sib=f'[siblings.sib]\nsha = "{self.pin[:12]}"\n')
        self.assertRan(self.run_tool("--sha", sha), 3)

    def test_missing_sibling_repo_fails_loud(self):
        sha = self.adopt([["true"]], sib=f'[siblings.absent]\nsha = "{self.pin}"\n')
        z = self.run_tool("--sha", sha)
        self.assertRan(z, 3)
        self.assertIn("absent", z.stderr)

    def test_file_hash_mismatch_fails_loud(self):
        sha = self.adopt([["true"]], sib=f'[siblings.sib]\nsha = "{self.pin}"\n[siblings.sib.files]\n"data.txt" = "{"0" * 64}"\n')
        z = self.run_tool("--sha", sha)
        self.assertRan(z, 3)
        self.assertIn("data.txt", z.stderr)

    def test_file_hash_match_passes(self):
        good = hashlib.sha256(b"pinned\n").hexdigest()
        sha = self.adopt([["true"]], sib=f'[siblings.sib]\nsha = "{self.pin}"\n[siblings.sib.files]\n"data.txt" = "{good}"\n')
        self.assertRan(self.run_tool("--sha", sha))

    def test_unknown_key_refused(self):
        sha = self.adopt([["true"]], extra='checks_are_optional = true')
        z = self.run_tool("--sha", sha)
        self.assertRan(z, 3)
        self.assertIn("checks_are_optional", z.stderr)

    def test_no_checks_refused(self):
        sha = self.adopt([])
        self.assertRan(self.run_tool("--sha", sha), 3)

    def test_tool_sha_mismatch_refused(self):
        sha = self.adopt([["true"]])
        z = self.run_tool("--sha", sha, "--tool-sha", "2" * 40)
        self.assertRan(z, 3)
        self.assertIn("tool_sha", z.stderr)

    def test_unpushed_pin_is_noted_not_fatal(self):
        sha = self.adopt([["true"]])
        z = self.run_tool("--sha", sha)
        self.assertRan(z)
        self.assertIn("not reachable from origin/main", z.stderr)


class Isolation(Base):
    @unittest.skipUnless(bwrap_works(), "bwrap unavailable")
    def test_absolute_live_read_fails(self):
        script = f"#!/bin/sh\ncat {self.sib}/data.txt\n"
        sha = self.adopt([["./check.sh"]], {"check.sh": script})
        self.assertRan(self.run_tool("--sha", sha), 1)

    @unittest.skipUnless(bwrap_works(), "bwrap unavailable")
    def test_workspace_changes_between_commands_are_followed(self):
        # 2026-11-02: a sibling worktree removed mid-run made every later bwrap fail ("Can't find source path .git"),
        # and a directory created mid-run would have stayed visible. Isolation is recomputed per command.
        gone = self.repo("gone-wt", {"x": "x\n"})
        ready, go = self.tmp / "ready", self.tmp / "go"
        wait = f"#!/bin/sh\ntouch {ready}\nwhile [ ! -e {go} ]; do sleep 0.05; done\n"
        later = "#!/bin/sh\ntest ! -e ../born/secret\n"
        sha = self.adopt([["./wait.sh"], ["./later.sh"]], {"wait.sh": wait, "later.sh": later})
        full = dict(ENV, BENNETT_GATE_WORKSPACE=str(self.ws))
        log = open(self.tmp / "gate.log", "w+")
        self.addCleanup(log.close)
        proc = subprocess.Popen(["python3", "-I", str(TOOL), "run", "--repo", str(self.me), "--sha", sha],
                                stdin=subprocess.DEVNULL, stdout=log, stderr=log, env=full)
        self.addCleanup(lambda: proc.poll() is None and proc.kill())
        for _ in range(1200):
            if ready.exists():
                break
            time.sleep(0.05)
        else:
            self.fail("first check never started")
        shutil.rmtree(gone)
        self.repo("born", {"secret": "live\n"})
        go.touch()
        proc.wait(timeout=120)
        self.assertEqual(proc.returncode, 0, (self.tmp / "gate.log").read_text())

    @unittest.skipUnless(bwrap_works(), "bwrap unavailable")
    def test_unpinned_sibling_is_absent(self):
        self.repo("other", {"x": "x\n"})
        sha = self.adopt([["./check.sh"]], {"check.sh": "#!/bin/sh\ncat ../other/x\n"})
        self.assertRan(self.run_tool("--sha", sha), 1)

    @unittest.skipUnless(bwrap_works(), "bwrap unavailable")
    def test_git_in_sibling_still_reads_pinned_objects(self):
        script = f"#!/bin/sh\ntest \"$(git -C ../sib rev-parse HEAD)\" = {self.pin}\n"
        sha = self.adopt([["./check.sh"]], {"check.sh": script})
        self.assertRan(self.run_tool("--sha", sha))

    def test_no_isolate_is_announced(self):
        sha = self.adopt([["true"]])
        z = self.run_tool("--sha", sha, "--no-isolate")
        self.assertRan(z)
        self.assertIn("ISOLATION OFF", z.stderr)

    def test_missing_bwrap_fails_loud(self):
        sha = self.adopt([["true"]])
        z = self.run_tool("--sha", sha, env={"BENNETT_GATE_BWRAP": str(self.tmp / "no-bwrap")})
        self.assertRan(z, 3)
        self.assertIn("bwrap", z.stderr)


class Env(Base):
    def test_placeholders_expanded(self):
        script = '#!/bin/sh\ntest "$(cat "$SIB/data.txt")" = pinned\ntest "$(cat "$LAYOUT/sib/data.txt")" = pinned\n'
        sha = self.adopt([["./check.sh"]], {"check.sh": script}, extra='[env]\nSIB = "{sibling:sib}"\nLAYOUT = "{layout}"\n')
        self.assertRan(self.run_tool("--sha", sha))

    def test_unknown_placeholder_refused(self):
        sha = self.adopt([["true"]], extra='[env]\nSIB = "{sibling:nope}"\n')
        z = self.run_tool("--sha", sha)
        self.assertRan(z, 3)
        self.assertIn("nope", z.stderr)

    def test_inherited_bennett_env_is_scrubbed(self):
        sha = self.adopt([["./check.sh"]], {"check.sh": '#!/bin/sh\ntest -z "$BENNETT_ARITH_ROOT"\n'})
        z = self.run_tool("--sha", sha, env={"BENNETT_ARITH_ROOT": "/live"})
        self.assertRan(z)
        self.assertIn("BENNETT_ARITH_ROOT", z.stderr)

    def test_display_unset_and_tmpdir_local(self):
        script = '#!/bin/sh\ntest -z "$DISPLAY"\ncase "$TMPDIR" in "$PWD"/*) ;; *) exit 1;; esac\ntest -d "$TMPDIR"\n'
        sha = self.adopt([["./check.sh"]], {"check.sh": script})
        self.assertRan(self.run_tool("--sha", sha, env={"DISPLAY": ":0"}))


class Builds(Base):
    def spec(self, pin):
        return (
            f'[siblings.sib]\nsha = "{pin}"\n[[siblings.sib.build]]\nname = "b"\n'
            'argv = ["sh", "build.sh"]\noutputs = ["out/bin"]\n'
        )

    def test_built_once_per_sha_and_output_visible(self):
        count = self.tmp / "count"
        script = "#!/bin/sh\ntest \"$(cat ../sib/out/bin)\" = built-pinned\n"
        sha = self.adopt([["./check.sh"]], {"check.sh": script}, sib=self.spec(self.pin), extra=f'[env]\nX = "y"\n')
        env = {"COUNT": str(count)}
        self.assertRan(self.run_tool("--sha", sha, env=env))
        self.assertRan(self.run_tool("--sha", sha, env=env))
        self.assertEqual(count.read_text().count("x"), 1)
        new_pin = git(self.sib, "rev-parse", "HEAD")
        sha2 = self.adopt([["true"]], sib=self.spec(new_pin))
        self.assertRan(self.run_tool("--sha", sha2, env=env))
        self.assertEqual(count.read_text().count("x"), 2)

    def test_declared_output_missing_fails_loud(self):
        sib = f'[siblings.sib]\nsha = "{self.pin}"\n[[siblings.sib.build]]\nname = "b"\nargv = ["true"]\noutputs = ["nope"]\n'
        sha = self.adopt([["true"]], sib=sib)
        z = self.run_tool("--sha", sha)
        self.assertRan(z, 3)
        self.assertIn("nope", z.stderr)

    def test_failed_build_fails_loud_and_is_not_stamped(self):
        sib = f'[siblings.sib]\nsha = "{self.pin}"\n[[siblings.sib.build]]\nname = "b"\nargv = ["false"]\noutputs = []\n'
        sha = self.adopt([["true"]], sib=sib)
        self.assertRan(self.run_tool("--sha", sha), 3)
        self.assertRan(self.run_tool("--sha", sha), 3)

    def test_needs_places_dependency_beside_the_built_sibling(self):
        dep = self.repo("dep", {"d": "dep\n"})
        dep_sha = git(dep, "rev-parse", "HEAD")
        sib = (
            f'[siblings.dep]\nsha = "{dep_sha}"\n[siblings.sib]\nsha = "{self.pin}"\n[[siblings.sib.build]]\n'
            'name = "b"\nargv = ["sh", "-c", "cat ../dep/d > got"]\noutputs = ["got"]\nneeds = ["dep"]\n'
        )
        sha = self.adopt([["true"]], sib=sib)
        self.assertRan(self.run_tool("--sha", sha))


class Reports(Base):
    def test_failing_report_never_changes_exit(self):
        sha = self.adopt([["true"]], extra='[[report]]\nname = "blockers"\nargv = ["sh", "-c", "echo BLOCKED-BY-X; exit 2"]\n')
        z = self.run_tool("--sha", sha)
        self.assertRan(z)
        self.assertIn("BLOCKED-BY-X", z.stdout)

    def test_report_runs_after_a_failing_check_and_exit_stays_one(self):
        sha = self.adopt([["false"]], extra='[[report]]\nname = "blockers"\nargv = ["sh", "-c", "echo BLOCKED-BY-X"]\n')
        z = self.run_tool("--sha", sha)
        self.assertRan(z, 1)
        self.assertIn("BLOCKED-BY-X", z.stdout)

    def test_report_live_static_and_drift_exit_zero(self):
        files = {"tests/a.py": f"open('{self.sib}/data.txt')\nopen('../sib/data.txt')\n"}
        sha = self.adopt([["true"]], files)
        z = self.run_tool("--sha", sha, cmd="report-live")
        self.assertRan(z)
        self.assertIn("absolute", z.stdout)
        self.assertIn("tests/a.py:1", z.stdout)
        self.assertIn("behind", z.stdout)

    def test_report_live_run_is_evidence_only(self):
        sha = self.adopt([["./check.sh"]], {"check.sh": "#!/bin/sh\ntest \"$(cat ../sib/data.txt)\" = pinned\n"})
        z = self.run_tool("--sha", sha, "--run", cmd="report-live")
        self.assertRan(z)  # the live sibling is dirty, so the consumer check fails: reported, not an exit code
        self.assertIn("consumer check against live siblings: FAIL", z.stdout)

    @unittest.skipUnless(shutil.which("strace"), "strace unavailable")
    def test_report_live_trace_lists_absolute_reads(self):
        sha = self.adopt([["./check.sh"]], {"check.sh": f"#!/bin/sh\ncat {self.sib}/data.txt\n"})
        z = self.run_tool("--sha", sha, "--run", "--trace", cmd="report-live")
        self.assertRan(z)
        self.assertIn(f"{self.sib}/data.txt", z.stdout)


class Refs(Base):
    def test_stdin_gates_exact_pushed_sha(self):
        sha = self.adopt([["./check.sh"]], {"check.sh": "#!/bin/sh\nexit 0\n"})
        bad = self.adopt([["./check.sh"]], {"check.sh": "#!/bin/sh\nexit 1\n"})  # HEAD is red; the pushed sha is not
        self.assertRan(self.run_tool(stdin=f"refs/heads/x {sha} refs/heads/main {ZERO}\n"))
        self.assertRan(self.run_tool(stdin=f"refs/heads/x {bad} refs/heads/main {ZERO}\n"), 1)

    def test_deletion_only_push_is_a_noop(self):
        z = self.run_tool(stdin=f"(delete) {ZERO} refs/heads/gone {'a' * 40}\n")
        self.assertRan(z)

    def test_malformed_ref_line_refused(self):
        self.assertRan(self.run_tool(stdin="refs/heads/x nothex refs/heads/main 0\n"), 3)

    def test_empty_stdin_gates_head(self):
        self.adopt([["false"]])
        self.assertRan(self.run_tool(), 1)


class Hooks(Base):
    def stubbed(self):
        meta = self.repo("bennett", {"tools/gate_run.py": TOOL.read_text()})
        tool_sha = git(meta, "rev-parse", "HEAD")
        stub = STUB.read_text()
        self.commit(self.me, {"gate.toml": self.toml([["true"]], tool_sha=tool_sha), "scripts/pre-push": stub})
        return tool_sha

    def check(self, code=0):
        z = self.run_tool(cmd="hook-check")
        self.assertRan(z, code)
        return z

    def hook(self, rel, text):
        p = self.me / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        p.chmod(0o755)

    def test_pushed_pin_of_an_ancestor_tool_runs_under_the_newer_tool(self):
        # A walk-back push of an older sha pinning an older tool, from a HEAD that bumped the tool (tool fixes go forward).
        old = self.stubbed()
        meta = self.ws / "bennett"
        sha = git(self.me, "rev-parse", "HEAD")
        new = self.commit(meta, {"tools/gate_run.py": TOOL.read_text() + "# fix\n"})
        z = self.run_tool("--sha", sha, "--tool-sha", new)
        self.assertRan(z)
        self.assertIn(f"pins tool_sha {old}, an ancestor of the running {new}", z.stderr)
        rec = json.loads((self.me / ".tmp/gate/records" / f"{sha}.json").read_text())
        self.assertEqual((rec["tool_sha"], rec["tool_sha_ran"]), (old, new))

    def test_pushed_pin_of_a_newer_tool_refused(self):
        self.stubbed()
        meta = self.ws / "bennett"
        older = git(meta, "rev-parse", "HEAD")
        newer = self.commit(meta, {"tools/gate_run.py": TOOL.read_text() + "# fix\n"})
        sha = self.commit(self.me, {"gate.toml": self.toml([["true"]], tool_sha=newer)})
        z = self.run_tool("--sha", sha, "--tool-sha", older)
        self.assertRan(z, 3)
        self.assertIn("not an ancestor", z.stderr)

    def test_stub_gates_through_a_real_push(self):
        self.stubbed()
        remote = self.tmp / "remote.git"
        git(self.tmp, "init", "-q", "--bare", str(remote))
        git(self.me, "remote", "add", "origin", str(remote))
        git(self.me, "config", "core.hooksPath", ".beads/hooks")
        self.hook(".beads/hooks/pre-push", '#!/bin/sh\nunset GIT_DIR\nexec "$(dirname "$0")/../../scripts/pre-push" "$@"\n')
        env = dict(ENV, BENNETT_GATE_WORKSPACE=str(self.ws))
        z = subprocess.run(["git", "-C", str(self.me), "push", "origin", "HEAD:refs/heads/main"], capture_output=True, text=True, env=env)
        self.assertEqual(z.returncode, 0, z.stderr)
        head = git(self.me, "rev-parse", "HEAD")
        self.assertTrue((self.me / ".tmp/gate/records" / f"{head}.json").exists(), z.stderr)

    def test_stub_refuses_without_pin_file(self):
        self.stubbed()
        git(self.me, "rm", "-q", "gate.toml")
        git(self.me, "commit", "-qm", "rm")
        z = subprocess.run([str(self.me / "scripts/pre-push")], capture_output=True, text=True, env=ENV, stdin=subprocess.DEVNULL)
        self.assertEqual(z.returncode, 3, z.stderr)

    def test_plain_git_hooks_symlink_chains(self):
        self.stubbed()
        (self.me / ".git/hooks/pre-push").symlink_to("../../scripts/pre-push")
        self.assertIn("chains", self.check().stdout)

    def test_beads_wrapper_chains(self):
        self.stubbed()
        git(self.me, "config", "core.hooksPath", ".beads/hooks")
        self.hook(".beads/hooks/pre-push", '#!/bin/sh\nset -e\nroot="$(dirname "$(dirname "$(dirname "$(readlink -f "$0")")")")"\nexec "$root/scripts/pre-push" "$@"\n')
        self.check()

    def test_stale_beads_copy_detected(self):
        self.stubbed()
        git(self.me, "config", "core.hooksPath", ".beads/hooks")
        self.hook(".beads/hooks/pre-push", "#!/bin/sh\ncargo test\n")
        self.assertIn("does not chain", self.check(1).stderr)

    def test_dead_git_hook_under_hookspath_detected(self):
        self.stubbed()
        (self.me / ".git/hooks/pre-push").symlink_to("../../scripts/pre-push")
        git(self.me, "config", "core.hooksPath", ".beads/hooks")
        self.assertIn("no executable", self.check(1).stderr)

    def test_old_gate_not_probed(self):
        marker = self.tmp / "ran-old"
        self.commit(self.me, {"scripts/pre-push": f"#!/bin/sh\ntouch {marker}\n"})
        (self.me / ".git/hooks/pre-push").symlink_to("../../scripts/pre-push")
        self.assertIn("not a gate stub", self.check(1).stderr)
        self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
