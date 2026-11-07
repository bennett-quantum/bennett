"""Post-merge health checks against local Git remotes and deterministic lock probes."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "main_health.py"
# Subprocess hang guards (20/30s) exceed 10x this whole suite's measured 1.3s
# on the shared 12-core / 30 GiB workstation, 2026-11-07; never test verdicts.


def load_tool():
    spec = importlib.util.spec_from_file_location("main_health", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HealthTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.meta = self.root / "bennett"
        self.meta.mkdir()
        self.repo = self.root / "fixture"
        self.repo.mkdir()
        self.state = self.root / "state"
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                        GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid")
        self.git("init", "-qb", "main")
        (self.repo / "scripts").mkdir()
        (self.repo / "gate.toml").write_text('schema = 1\n')
        stub = self.repo / "scripts/pre-push"
        stub.write_text('#!/bin/sh\nset -eu\n'
                        'test "$(git rev-parse HEAD)" = "$2"\n'
                        'test "$1" = --sha\n'
                        'printf "detached=%s\\n" "$(git symbolic-ref -q HEAD || echo yes)"\n'
                        'test -z "${BENNETT_GATE_HOOK_PROBE:-}"\n'
                        'exit "$(cat verdict)"\n')
        stub.chmod(0o755)
        (self.repo / "verdict").write_text('0\n')
        self.commit("green")
        self.green = self.git("rev-parse", "HEAD")
        self.remote = self.root / "remote.git"
        self.git("clone", "-q", "--bare", str(self.repo), str(self.remote))
        self.git("remote", "add", "origin", str(self.remote))
        (self.meta / "manifest.toml").write_text('[repos.fixture]\npath = "fixture"\n')
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.executable("systemctl", 'print("")\n')
        self.executable("pgrep", 'raise SystemExit(1)\n')
        self.executable("systemd-run", 'import os, sys\na = sys.argv[1:]\n'
                        'while a and a[0].startswith("-"): a.pop(0)\n'
                        'os.execvp(a[0], a)\n')
        self.env["PATH"] = str(self.bin) + os.pathsep + self.env["PATH"]
        self.env["BENNETT_GATE_HOOK_PROBE"] = "1"  # Must not turn a real check into a probe.

    def executable(self, name, body):
        target = self.bin / name
        target.write_text(f'#!{sys.executable}\n{body}')
        target.chmod(0o755)

    def git(self, *args):
        return subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-C", str(self.repo),
                               *args], env=self.env, capture_output=True, text=True,
                              check=True, timeout=20).stdout.strip()

    def commit(self, message):
        self.git("add", ".")
        self.git("commit", "-qm", message)

    def run_health(self, *args):
        # CLI Git/status behavior is real; the host's changing load is not a test input.
        bootstrap = ('import importlib.util, sys\n'
                     'path = sys.argv.pop(1)\n'
                     'spec = importlib.util.spec_from_file_location("health_fixture", path)\n'
                     'module = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n'
                     'module.heavy_blocker = lambda: None\nraise SystemExit(module.main())\n')
        return subprocess.run([sys.executable, "-I", "-c", bootstrap, str(SCRIPT), "run", "--once",
                               "--meta", str(self.meta), "--state-dir", str(self.state),
                               *args], env=self.env, text=True, capture_output=True, timeout=30)

    def rows(self):
        return json.loads((self.state / "status.json").read_text())["rows"]

    def test_changed_sha_history_and_detached_stub(self):
        first = self.run_health("--repos", "fixture")
        self.assertEqual(first.returncode, 0, first.stderr)
        row = self.rows()["fixture"]
        self.assertEqual((row["sha"], row["result"]), (self.green, "PASS"))
        self.assertIn("detached=yes", Path(row["log"]).read_text())
        second = self.run_health("--repos", "fixture")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(self.rows()["fixture"]["delta"], "unchanged")
        self.assertEqual(len((self.state / "history.jsonl").read_text().splitlines()), 1)
        forced = self.run_health("--repos", "fixture", "--force")
        self.assertEqual(forced.returncode, 0, forced.stderr)
        self.assertEqual(len((self.state / "history.jsonl").read_text().splitlines()), 2)

    def test_red_names_merges_since_last_green_even_on_repeat(self):
        self.assertEqual(self.run_health("--repos", "fixture").returncode, 0)
        self.git("switch", "-qc", "regression")
        (self.repo / "verdict").write_text('1\n')
        self.commit("bad gate")
        self.git("switch", "-q", "main")
        self.git("merge", "--no-ff", "-m", "Merge regression lane", "regression")
        merge = self.git("rev-parse", "HEAD")
        self.git("push", "-q", "origin", "main")
        # A dirty live checkout must not change the fetched-main verdict.
        (self.repo / "verdict").write_text('0\n')
        red = self.run_health("--repos", "fixture")
        self.assertEqual(red.returncode, 1, red.stderr)
        row = self.rows()["fixture"]
        self.assertEqual(row["result"], "FAIL")
        self.assertEqual(row["last_green_shas"], {"fixture": self.green})
        self.assertIn(merge, json.dumps(row["merges"]))
        self.assertIn("Merge regression lane", (self.state / "status.md").read_text())
        self.assertEqual(self.run_health("--repos", "fixture").returncode, 1)
        self.assertIn(merge, json.dumps(self.rows()["fixture"]["merges"]))

    def test_missing_stub_and_unknown_selection_are_tool_errors(self):
        unknown = self.run_health("--repos", "absent")
        self.assertEqual(unknown.returncode, 2)
        self.assertIn("manifest", unknown.stderr)
        (self.repo / "scripts/pre-push").unlink()
        self.commit("missing stub")
        self.git("push", "-q", "origin", "main")
        missing = self.run_health("--repos", "fixture")
        self.assertEqual(missing.returncode, 2, missing.stderr)
        self.assertEqual(self.rows()["fixture"]["result"], "ERROR")
        self.assertIn("scripts/pre-push", (self.state / "status.md").read_text())

    def test_unselected_rows_are_unknown(self):
        (self.meta / "manifest.toml").write_text(
            '[repos.fixture]\npath = "fixture"\n[repos.other]\npath = "missing"\n')
        result = self.run_health("--repos", "fixture")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.rows()["other"]["result"], "UNKNOWN")
        self.assertEqual(self.rows()["ladder/rung-1"]["result"], "UNKNOWN")

    def test_timeout_exit_is_not_a_gate_failure_and_is_retried(self):
        self.executable("systemd-run", 'raise SystemExit(124)\n')
        result = self.run_health("--repos", "fixture")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(self.rows()["fixture"]["result"], "TIMEOUT")
        self.assertIn("TIMEOUT", (self.state / "status.md").read_text())
        self.executable("systemd-run", 'import os, sys\na = sys.argv[1:]\n'
                        'while a and a[0].startswith("-"): a.pop(0)\n'
                        'os.execvp(a[0], a)\n')
        self.assertEqual(self.run_health("--repos", "fixture").returncode, 0)
        self.assertEqual(self.rows()["fixture"]["result"], "PASS")

    def test_ladder_freezes_every_main_and_keeps_major_table(self):
        module = load_tool()
        revisions = {name: str(index) * 40 for index, name in enumerate(module.LADDER_REPOS, 1)}
        options = {"--" + name.removeprefix("bennett-") + "-rev" for name in revisions}
        argv = module.ladder_argv(self.repo / "gate.sh", revisions, " ".join(options), self.state)
        for name, sha in revisions.items():
            flag = "--" + name.removeprefix("bennett-") + "-rev"
            self.assertEqual(argv[argv.index(flag) + 1], sha)
        with self.assertRaisesRegex(module.HealthError, "runtimes-rev"):
            module.ladder_argv(self.repo / "gate.sh", revisions,
                               "--plugin-rev --vm-rev", self.state)

    def test_ladder_records_all_revisions_and_major_table(self):
        module = load_tool()
        ladder = self.repo / "ladder/rung-1/gate.sh"
        ladder.parent.mkdir(parents=True)
        options = " ".join("--" + name.removeprefix("bennett-") + "-rev" for name in module.LADDER_REPOS)
        ladder.write_text('#!/bin/sh\nset -eu\n'
                          f'if [ "$1" = --help ]; then echo "{options}"; exit 0; fi\n'
                          'test "$1" = --output\noutput=$2\nshift 2\n'
                          'test "$1" = --jobs\nshift 2\ncount=0\n'
                          'while [ "$#" -gt 0 ]; do\n'
                          'test "$2" = "$(git rev-parse HEAD)"\n'
                          'count=$((count+1))\nshift 2\ndone\ntest "$count" = 5\n'
                          'mkdir -p "$output/evidence"\n'
                          'printf "| LLVM | Result |\\n|---|---|\\n| 18 | PASS |\\n| 23 | FAIL |\\n" > "$output/evidence/table.md"\n'
                          'exit 1\n')
        self.commit("ladder")
        self.git("push", "-q", "origin", "main")
        (self.meta / "manifest.toml").write_text(''.join(
            f'[repos."{name}"]\npath = "fixture"\n'
            for name in ("bennett-conformance", *module.LADDER_REPOS)))
        result = self.run_health("--ladder", "rung-1")
        self.assertEqual(result.returncode, 1, result.stderr)
        row = self.rows()["ladder/rung-1"]
        self.assertEqual(len(row["shas"]), 6)
        self.assertEqual(row["result"], "FAIL")
        self.assertIn("| 23 | FAIL |", row["table"])
        self.assertIn("| 18 | PASS |", (self.state / "status.md").read_text())

    def test_failed_scope_start_is_error_not_red(self):
        self.executable("systemd-run", 'raise SystemExit(1)\n')
        result = self.run_health("--repos", "fixture")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(self.rows()["fixture"]["result"], "ERROR")
        self.assertIn("without a child exit record", self.rows()["fixture"]["detail"])

    def test_slot_wait_guard_writes_timeout_row(self):
        module = load_tool()
        args = type("Args", (), dict(meta=self.meta, state_dir=self.state, repos="fixture",
                    ladder=None, force=False, max_wait=100, command_timeout=100))()
        with patch.dict(os.environ, self.env, clear=True), \
                patch.object(module, "wait_for_slot", side_effect=TimeoutError("busy scope guard")):
            runner = module.Runner(args)
            self.assertEqual(runner.cycle(), 2)
        row = self.rows()["fixture"]
        self.assertEqual(row["result"], "TIMEOUT")
        self.assertIn("busy scope guard", (self.state / "status.md").read_text())

    def test_nested_cache_isolation_keeps_only_detached_root(self):
        module = load_tool()
        self.executable("bwrap", 'import json,sys\nprint(json.dumps(sys.argv[1:]))\n')
        checkout = self.root / "cache/repo"
        checkout.mkdir(parents=True)
        wrapper = module.cache_isolation(checkout)
        prefix = ["--dev-bind", "/", "/", "--die-with-parent", "--tmpfs", str(self.meta),
                  "--bind-try", str(self.meta / ".git"), str(self.meta / ".git")]
        result = subprocess.run([wrapper, *prefix, "true"], env=self.env,
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [*prefix, "--bind", str(checkout), str(checkout), "true"])
        build_command = ["--chdir", str(checkout), "--", "cargo", "build", "--offline"]
        build = subprocess.run([wrapper, *prefix, *build_command], env=self.env,
                               capture_output=True, text=True, timeout=20)
        self.assertEqual(build.returncode, 0, build.stderr)
        self.assertEqual(json.loads(build.stdout), [*prefix, "--bind", str(checkout), str(checkout), *build_command])
        unknown = subprocess.run([wrapper, "--unrecognized", "true"], env=self.env,
                                 capture_output=True, text=True, timeout=20)
        self.assertNotEqual(unknown.returncode, 0)
        self.assertIn("unsupported", unknown.stderr)

    def test_default_state_anchors_to_main_checkout_from_worktree(self):
        module = load_tool()
        worktree = self.root / "linked-meta"
        self.git("worktree", "add", "--detach", str(worktree), "HEAD")
        self.assertEqual(module.main_checkout(worktree), self.repo)

    def test_ladder_refetches_after_repo_gate(self):
        module = load_tool()
        (self.meta / "manifest.toml").write_text(''.join(
            f'[repos."{name}"]\npath = "fixture"\n'
            for name in ("bennett-conformance", *module.LADDER_REPOS)))
        args = type("Args", (), dict(meta=self.meta, state_dir=self.state, repos="bennett-plugin",
                    ladder="rung-1", force=False, max_wait=100, command_timeout=100))()
        before, after = "1" * 40, "2" * 40
        with patch.object(module, "fetch_main", side_effect=[before, *([after] * 6)]), \
                patch.object(module.Runner, "gate", return_value=(module.Result.PASS, 0)), \
                patch.object(module.Runner, "ladder", return_value=(module.Result.PASS, 0)), \
                patch("builtins.print"):
            self.assertEqual(module.Runner(args).cycle(), 0)
        rows = self.rows()
        self.assertEqual(rows["bennett-plugin"]["sha"], before)
        self.assertEqual(rows["ladder/rung-1"]["shas"]["bennett-plugin"], after)


class LockTests(unittest.TestCase):
    def test_scope_and_legacy_process_probes_block_before_resource_reads(self):
        module = load_tool()
        scope = subprocess.CompletedProcess([], 0, "bennett-heavy-other.scope loaded active running", "")
        with patch.object(module, "control", return_value=scope) as control:
            self.assertIn("bennett-heavy-other.scope", module.heavy_blocker())
        self.assertEqual(control.call_count, 1)
        idle = subprocess.CompletedProcess([], 0, "", "")
        process = subprocess.CompletedProcess([], 0, "1234", "")
        with patch.object(module, "control", side_effect=[idle, process]):
            self.assertIn("1234", module.heavy_blocker())

    def test_resource_thresholds_with_mocked_proc_data(self):
        module = load_tool()
        idle = subprocess.CompletedProcess([], 1, "", "")
        # Hand-derived KiB conversion: 6 GiB = 6 * 1024 * 1024 KiB.
        for available, load, blocked in ((6, 11, False), (5, 0, True), (6, 12, True)):
            with self.subTest(available=available, load=load), \
                    patch.object(module, "control", return_value=idle), \
                    patch.object(module.Path, "read_text", side_effect=[
                        f"MemAvailable: {available * 1024 * 1024} kB\n", f"{load} 0 0 1/1 1\n"]):
                self.assertEqual(module.heavy_blocker() is not None, blocked)

    def test_wait_uses_mocked_probe_and_clock(self):
        module = load_tool()
        with patch.object(module, "heavy_blocker", side_effect=["bennett-heavy-busy", "memory", None]) as probe, \
                patch.object(module.time, "monotonic", return_value=0), \
                patch.object(module.time, "sleep") as sleep:
            module.wait_for_slot(100)
        self.assertEqual(probe.call_count, 3)
        self.assertEqual(sleep.call_count, 2)

    def test_wait_limit_is_timeout_without_starting_work(self):
        module = load_tool()
        with patch.object(module, "heavy_blocker", return_value="bennett-heavy-busy"), \
                patch.object(module.time, "monotonic", side_effect=[0, 101]), \
                patch.object(module.time, "sleep") as sleep:
            with self.assertRaisesRegex(TimeoutError, "bennett-heavy-busy"):
                module.wait_for_slot(100)
        sleep.assert_not_called()


if __name__ == "__main__":
    unittest.main()
