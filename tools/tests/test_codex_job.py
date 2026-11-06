"""Runner regressions using local git repositories and executable Codex/quota fixtures."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from tools import codex_job as job


class RunnerFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.env = dict(os.environ, HOME=str(self.root), GIT_CONFIG_NOSYSTEM="1",
                        GIT_CONFIG_GLOBAL=os.devnull, GIT_AUTHOR_NAME="Fixture",
                        GIT_AUTHOR_EMAIL="fixture@example.invalid", GIT_COMMITTER_NAME="Fixture",
                        GIT_COMMITTER_EMAIL="fixture@example.invalid")
        for key in tuple(self.env):
            if key.startswith("GIT_") and key not in {"GIT_CONFIG_NOSYSTEM", "GIT_CONFIG_GLOBAL",
                    "GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL", "GIT_COMMITTER_NAME", "GIT_COMMITTER_EMAIL"}:
                del self.env[key]
        self.patch_env = patch.dict(os.environ, self.env, clear=True)
        self.patch_env.start()
        self.addCleanup(self.patch_env.stop)
        self.git("init", "-q", "-b", "main")
        self.git("config", "core.hooksPath", str(self.root / "no-hooks"))
        (self.repo / "owned").mkdir()
        (self.repo / "owned" / "source.txt").write_text("initial\n")
        self.git("add", ".")
        self.git("commit", "-qm", "initial")
        self.initial = self.git("rev-parse", "main").strip()
        self.remote = self.root / "backup.git"
        self.git("init", "--bare", "-q", str(self.remote))
        self.git("remote", "add", "origin", str(self.remote))
        self.bin = self.root / "bin"
        self.bin.mkdir()
        os.environ["PATH"] = str(self.bin) + os.pathsep + os.environ["PATH"]
        reset = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=84)).isoformat()
        self.quota = [{"vendor": "codex", "windows": [{"kind": {"kind": "weekly"},
                      "resets_at": reset, "length": "PT168H", "used": 0.1}]}]
        self.executable("quota", "import json\nprint(" + repr(json.dumps(self.quota)) + ")\n")
        self.executable("codex", """import json, pathlib, sys
pathlib.Path('owned/result.txt').write_text('from fixture\\n')
pathlib.Path(sys.argv[sys.argv.index('-o') + 1]).write_text('JOB-COMPLETE\\n')
print(json.dumps({'type': 'thread.started', 'thread_id': 'fixture-thread'}))
print(json.dumps({'type': 'turn.completed'}))
""")
        self.prompt = self.root / "brief.txt"
        self.prompt.write_text("Fixture job")
        self.state = self.root / ".local/state/bennett-codex-jobs"
        self.state.mkdir(parents=True)
        self.state_patch = patch.object(job, "STATE", str(self.state))
        self.state_patch.start()
        self.addCleanup(self.state_patch.stop)

    def git(self, *args, cd=None):
        return subprocess.run(["git", *args], cwd=cd or self.repo, check=True,
                              capture_output=True, text=True).stdout

    def executable(self, name, body):
        path = self.bin / name
        path.write_text(f"#!{sys.executable}\n" + body)
        path.chmod(0o755)

    def args(self, **overrides):
        data = dict(name="sample", cd=None, repo=str(self.repo), worktree=None,
                    prompt=str(self.prompt), paths=["owned"], progress=".tmp/progress.md",
                    model="fixture-model", effort="low", max_attempts=1, pace_margin=5,
                    network=False, thread=None)
        data.update(overrides)
        return argparse.Namespace(**data)

    def status(self):
        return json.loads((self.state / "sample" / "status.json").read_text())


class BranchTests(RunnerFixture):
    def test_branch_mode_end_to_end_and_resume(self):
        self.assertEqual(job.run(self.args()), 0)
        wt = self.root / "repo-job-sample"
        self.assertTrue((wt / "owned/result.txt").is_file())
        self.assertEqual(self.git("rev-parse", "main").strip(), self.initial)

        self.assertEqual(self.git("branch", "--show-current", cd=wt).strip(), "job/sample")
        self.assertEqual(self.git("rev-parse", "job/sample^1").strip(), self.initial)
        self.assertEqual(self.git("rev-parse", "refs/heads/wip/sample", cd=self.remote).strip(),
                         self.git("rev-parse", "HEAD", cd=wt).strip())
        for field in ("cd", "worktree"):
            self.assertEqual(self.status()[field], str(wt))
        self.assertEqual(self.status()["branch"], "job/sample")
        self.assertEqual(job.run(self.args()), 0)
        self.assertEqual(self.status()["cd"], str(wt))

    def test_existing_cd_on_main_is_refused_before_attempt(self):
        with self.assertRaisesRegex((ValueError, RuntimeError), "main|master"):
            job.run(self.args(cd=str(self.repo), repo=None))
        self.assertFalse((self.repo / "owned/result.txt").exists())
        self.assertEqual(self.git("rev-parse", "main").strip(), self.initial)

    def test_existing_job_worktree_is_supported(self):
        wt = self.root / "existing"
        self.git("worktree", "add", "-qb", "job/sample", str(wt), "main")
        self.assertEqual(job.run(self.args(cd=str(wt), repo=None)), 0)
        self.assertEqual(self.status()["worktree"], str(wt))
        self.assertEqual(self.git("rev-parse", "main").strip(), self.initial)

    def test_concurrent_jobs_get_distinct_worktrees_cut_from_main(self):
        self.assertEqual(job.run(self.args()), 0)
        self.assertEqual(job.run(self.args(name="second")), 0)
        second = self.root / "repo-job-second"
        self.assertEqual(self.git("rev-parse", "HEAD^1", cd=second).strip(), self.initial)
        self.assertNotEqual(self.status()["cd"], str(second))

    def test_cli_defaults_to_branch_mode(self):
        result = subprocess.run([sys.executable, job.__file__, "run", "--name", "cli",
                                 "--repo", str(self.repo), "--prompt", str(self.prompt),
                                 "--paths", "owned", "--progress", ".tmp/progress.md"],
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "repo-job-cli/owned/result.txt").exists())
        self.assertEqual(self.git("rev-parse", "main").strip(), self.initial)


    def test_launch_uses_main_even_from_feature_checkout(self):
        self.git("switch", "-qc", "feature")
        (self.repo / "feature-only").write_text("feature")
        self.git("add", "feature-only")
        self.git("commit", "-qm", "feature commit")
        self.assertEqual(job.run(self.args()), 0)
        self.assertEqual(self.git("rev-parse", "job/sample^1").strip(), self.initial)

    def test_master_checkout_is_refused_and_master_source_is_supported(self):
        self.git("branch", "-m", "main", "master")
        with self.assertRaisesRegex(RuntimeError, "main/master"):
            job.run(self.args(cd=str(self.repo), repo=None))
        self.assertEqual(job.run(self.args()), 0)
        self.assertEqual(self.git("rev-parse", "master").strip(), self.initial)


    def test_failed_resume_cannot_reuse_old_completion_message(self):
        self.assertEqual(job.run(self.args()), 0)
        self.executable("codex", "raise SystemExit(1)\n")
        with patch.object(job, "wait_between"):
            self.assertNotEqual(job.run(self.args()), 0)
        self.assertEqual(self.status()["state"], "gave-up")


class PaceTests(RunnerFixture):
    def test_weekly_pace_parsing(self):
        used, elapsed = job.codex_pace()
        self.assertAlmostEqual(used, 10)
        self.assertAlmostEqual(elapsed, 50, places=2)

    def test_bad_quota_is_unknown(self):
        for output, code in (("not json", 0), ("{}", 0), ("null", 0), ("[]", 0),
                             (json.dumps(self.quota), 1),
                             ('[{"vendor":"codex","windows":[{"kind":{"kind":"weekly"}}]}]', 0)):
            with self.subTest(output=output, code=code):
                self.executable("quota", f"import sys\nprint({output!r})\nsys.exit({code})\n")
                self.assertIsNone(job.codex_pace())

    def test_unknown_pace_stops_before_any_attempt(self):
        self.executable("quota", "print('invalid quota')\n")
        self.assertNotEqual(job.run(self.args()), 0)
        self.assertEqual(self.status()["state"], "stopped-pace-unknown")
        self.assertFalse((self.root / "repo-job-sample/owned/result.txt").exists())
        self.assertIn("quota", (self.state / "sample/runner.log").read_text())

    def test_quota_failure_after_attempt_prevents_next_attempt(self):
        with patch.object(job, "codex_pace", side_effect=[(10, 50), None]), \
                patch.object(job, "attempt", return_value=("early-stop", "t", "")) as attempt:
            self.assertNotEqual(job.run(self.args(max_attempts=2)), 0)
        self.assertEqual(attempt.call_count, 1)
        self.assertEqual(self.status()["state"], "stopped-pace-unknown")

    def test_over_pace_waits_and_uses_per_launch_margin(self):
        with patch.object(job, "codex_pace", side_effect=[(60, 50), (52, 50)]), \
                patch.object(job, "wait_between") as sleep:
            self.assertEqual(job.run(self.args(pace_margin=3)), 0)
        sleep.assert_called_once_with(str(self.state / "sample"), 900)

    def test_quota_command_timeout_or_missing_binary_is_unknown(self):
        for error in (FileNotFoundError("quota missing"), subprocess.TimeoutExpired("quota", 60)):
            with self.subTest(error=error), patch.object(job.subprocess, "run", side_effect=error):
                self.assertIsNone(job.codex_pace())

    def test_stop_request_interrupts_pace_wait(self):
        def request_stop(st, seconds):
            (Path(st) / "stop-request").touch()
        with patch.object(job, "codex_pace", return_value=(90, 50)), \
                patch.object(job, "wait_between", side_effect=request_stop):
            self.assertEqual(job.run(self.args()), 0)
        self.assertEqual(self.status()["state"], "stopped")
        self.assertFalse((self.root / "repo-job-sample/owned/result.txt").exists())

    def test_stop_during_last_backoff_preserves_stopped_state(self):
        with patch.object(job, "codex_pace", return_value=(10, 50)), \
                patch.object(job, "attempt", return_value=("network", "t", "")), \
                patch.object(job, "wait_between", side_effect=lambda *_: job.STOP.set()):
            self.assertEqual(job.run(self.args(max_attempts=1)), 0)
        self.assertEqual(self.status()["state"], "stopped")

    def test_nonfinite_margin_is_rejected(self):
        for margin in (float("inf"), float("nan")):
            with self.subTest(margin=margin), self.assertRaisesRegex(ValueError, "finite"):
                job.run(self.args(pace_margin=margin))


class CommitTests(RunnerFixture):
    def setUp(self):
        super().setUp()
        self.git("switch", "-qc", "job/sample")
        self.st = self.state / "sample"
        self.st.mkdir()

    def test_empty_missing_ignored_and_untracked_paths_do_not_lose_commit(self):
        (self.repo / "examples").mkdir()
        (self.repo / ".gitignore").write_text("ignored/\n")
        (self.repo / "ignored").mkdir()
        (self.repo / "ignored/cache").write_text("cache")
        (self.repo / "new").mkdir()
        (self.repo / "new/file").write_text("new content")
        (self.repo / "owned/source.txt").write_text("changed\n")
        (self.repo / "outside").write_text("another job staged this")
        self.git("add", "outside")
        job.commit(str(self.st), str(self.repo), ["examples", "missing", "ignored", "new", "owned"], "test")
        self.assertEqual(self.git("show", "HEAD:owned/source.txt"), "changed\n")
        self.assertEqual(self.git("show", "HEAD:new/file"), "new content")
        self.assertEqual(self.git("diff", "--cached", "--name-only").strip(), "outside")
        self.assertEqual(self.git("rev-parse", "main").strip(), self.initial)
        self.assertEqual(self.git("rev-parse", "wip/sample", cd=self.remote).strip(),
                         self.git("rev-parse", "HEAD").strip())

    def test_one_failing_add_still_commits_other_owned_paths(self):
        (self.repo / "bad").write_text("bad")
        (self.repo / "owned/source.txt").write_text("kept\n")
        real_run = subprocess.run

        def failing_add(cmd, **kwargs):
            if cmd[:2] == ["git", "add"] and cmd[-1] == "bad":
                raise subprocess.CalledProcessError(128, cmd, stderr="bad pathspec")
            return real_run(cmd, **kwargs)

        with patch.object(job.subprocess, "run", side_effect=failing_add):
            job.commit(str(self.st), str(self.repo), ["bad", "owned"], "test")
        self.assertEqual(self.git("show", "HEAD:owned/source.txt"), "kept\n")
        self.assertIn("bad", (self.st / "runner.log").read_text())

    def test_deleted_tracked_file_is_committed(self):
        (self.repo / "owned/source.txt").unlink()
        job.commit(str(self.st), str(self.repo), ["owned/source.txt"], "delete")
        self.assertEqual(self.git("ls-tree", "-r", "--name-only", "HEAD"), "")

    def test_commit_refuses_main_even_if_checkout_changed_after_launch(self):
        self.git("switch", "-q", "main")
        (self.repo / "owned/source.txt").write_text("must not commit")
        job.commit(str(self.st), str(self.repo), ["owned"], "unsafe")
        self.assertEqual(self.git("rev-parse", "main").strip(), self.initial)


    def test_already_staged_deletion_is_committed(self):
        self.git("rm", "-q", "owned/source.txt")
        job.commit(str(self.st), str(self.repo), ["owned/source.txt"], "staged delete")
        self.assertEqual(self.git("ls-tree", "-r", "--name-only", "HEAD"), "")

    def test_branch_change_during_staging_cannot_commit_main(self):
        (self.repo / "owned/source.txt").write_text("must not land on main")
        real_run = subprocess.run

        def change_branch(cmd, **kwargs):
            result = real_run(cmd, **kwargs)
            if cmd[:2] == ["git", "add"]:
                real_run(["git", "switch", "-q", "main"], cwd=self.repo, check=True)
            return result

        with patch.object(job.subprocess, "run", side_effect=change_branch):
            job.commit(str(self.st), str(self.repo), ["owned"], "branch moved")
        self.assertEqual(self.git("rev-parse", "main").strip(), self.initial)

    def test_backup_failure_is_recorded(self):
        self.git("remote", "remove", "origin")
        self.assertFalse(job.backup(str(self.st), str(self.repo)))
        self.assertFalse(self.status()["backup_ok"])
        self.assertTrue(self.status()["backup_error"])


class StopTests(RunnerFixture):
    def launch(self, body):
        self.executable("codex", body)
        self.runner = subprocess.Popen([sys.executable, job.__file__, "run", "--name", "sample",
            "--repo", str(self.repo), "--prompt", str(self.prompt), "--paths", "owned",
            "--progress", ".tmp/progress.md", "--max-attempts", "4"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.addCleanup(self.cleanup_runner)
        self.await_condition(lambda: (self.root / "repo-job-sample/owned/started").exists())

    def cleanup_runner(self):
        if self.runner.poll() is None:
            self.runner.terminate()
            try:
                self.runner.wait(timeout=12)
            except subprocess.TimeoutExpired:
                self.runner.kill()
                self.runner.wait(timeout=3)

    def await_condition(self, condition):
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            if condition():
                return
            time.sleep(0.02)
        self.fail("fixture condition timed out")

    def stop_cli(self, *flags):
        result = subprocess.run([sys.executable, job.__file__, "stop", "--name", "sample", *flags],
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_immediate_stop_terminates_child_commits_backs_up_and_exits(self):
        self.launch("""import os, pathlib, signal, time
pathlib.Path('owned/started').write_text(str(os.getpid()))
def stop(sig, frame):
    pathlib.Path('owned/terminated').write_text('SIGTERM')
    raise SystemExit(0)
signal.signal(signal.SIGTERM, stop)
while True: time.sleep(0.05)
""")
        self.stop_cli()
        self.assertEqual(self.runner.wait(timeout=5), 0)
        self.assertEqual(self.status()["state"], "stopped")
        self.assertEqual(self.git("show", "job/sample:owned/terminated"), "SIGTERM")
        self.assertEqual(self.git("rev-parse", "wip/sample", cd=self.remote).strip(),
                         self.git("rev-parse", "job/sample").strip())
        self.assertEqual(self.git("rev-parse", "main").strip(), self.initial)

    def test_stop_after_current_attempt_does_not_interrupt_child(self):
        self.launch("""import json, pathlib, sys, time
pathlib.Path('owned/started').write_text('started')
while not pathlib.Path('owned/release').exists(): time.sleep(0.02)
pathlib.Path('owned/finished').write_text('finished')
pathlib.Path(sys.argv[sys.argv.index('-o') + 1]).write_text('continue')
print(json.dumps({'type': 'turn.completed'}))
""")
        self.stop_cli("--after-current-attempt")
        self.assertIsNone(self.runner.poll())
        wt = self.root / "repo-job-sample"
        (wt / "owned/release").touch()
        self.assertEqual(self.runner.wait(timeout=5), 0)
        self.assertEqual(self.status()["state"], "stopped")
        self.assertEqual(self.status()["attempts"], 1)
        self.assertEqual(self.git("show", "job/sample:owned/finished"), "finished")
        self.assertEqual(self.git("rev-parse", "wip/sample", cd=self.remote).strip(),
                         self.git("rev-parse", "job/sample").strip())

    def test_duplicate_runner_is_refused_and_original_keeps_running(self):
        self.launch("""import pathlib, time
pathlib.Path('owned/started').write_text('started')
while True: time.sleep(0.05)
""")
        duplicate = subprocess.run([sys.executable, job.__file__, "run", "--name", "sample",
            "--repo", str(self.repo), "--prompt", str(self.prompt), "--paths", "owned",
            "--progress", ".tmp/progress.md"], capture_output=True, text=True, timeout=5)
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertIn("already has a running runner", duplicate.stderr)
        self.assertIsNone(self.runner.poll())
        self.stop_cli()

    def test_stale_process_identity_does_not_signal_unrelated_process(self):
        self.assertEqual(job.run(self.args()), 0)
        wt = self.root / "repo-job-sample"
        (wt / "owned/source.txt").write_text("recovered tree")
        job.save(str(self.state / "sample"), runner_pid=os.getpid(), runner_start="stale")
        with patch.object(job.os, "kill") as kill:
            self.assertEqual(job.stop_job(argparse.Namespace(name="sample", after_current_attempt=False)), 0)
        kill.assert_not_called()
        self.assertEqual(self.status()["state"], "stopped")
        self.assertEqual(self.git("show", "job/sample:owned/source.txt"), "recovered tree")

