"""Exercise installed hooks in scratch repositories; never install into this checkout."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

from tools.tests.fixtures import RunnerFixture

SOURCE = Path(__file__).resolve().parents[2]


class HookTests(RunnerFixture):
    def setUp(self):
        super().setUp()
        (self.repo / "scripts").mkdir()
        for name in ("install-hooks.sh", "pre-push"):
            shutil.copy2(SOURCE / "scripts" / name, self.repo / "scripts" / name)
        self.tests = self.repo / "tools/tests"
        self.tests.mkdir(parents=True)

    def run_script(self, path):
        return subprocess.run(["bash", str(path)], cwd=self.repo, capture_output=True,
                              text=True, timeout=10)

    def test_gate_fails_with_zero_tests(self):
        result = self.run_script(self.repo / "scripts/pre-push")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("no tests", result.stderr.lower())

    def test_gate_fails_with_only_skipped_tests(self):
        (self.tests / "test_fixture.py").write_text(
            "import unittest\n@unittest.skip('deferred')\n"
            "class Fixture(unittest.TestCase):\n"
            "    def test_fails(self): self.fail('must execute')\n")
        result = self.run_script(self.repo / "scripts/pre-push")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("no tests ran and passed", result.stderr)

    def test_gate_fails_with_only_expected_failures(self):
        (self.tests / "test_fixture.py").write_text(
            "import unittest\nclass Fixture(unittest.TestCase):\n"
            "    @unittest.expectedFailure\n"
            "    def test_fails(self): self.fail('known failure')\n")
        result = self.run_script(self.repo / "scripts/pre-push")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("no tests ran and passed", result.stderr)

    def test_gate_fails_with_only_skipped_subtests(self):
        (self.tests / "test_fixture.py").write_text(
            "import unittest\nclass Fixture(unittest.TestCase):\n"
            "    def test_subtests(self):\n"
            "        for value in (1, 2):\n"
            "            with self.subTest(value=value): self.skipTest('deferred')\n")
        result = self.run_script(self.repo / "scripts/pre-push")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("no tests ran and passed", result.stderr)

    def test_gate_accepts_pass_and_skip_with_one_discovery_and_run(self):
        (self.tests / "test_fixture.py").write_text(
            "import unittest\nfrom pathlib import Path\n"
            "with Path('executions').open('a') as log: log.write('import\\n')\n"
            "class Fixture(unittest.TestCase):\n"
            "    @unittest.skip('deferred')\n"
            "    def test_deferred(self): self.fail('must skip')\n"
            "    def test_passes(self):\n"
            "        with Path('executions').open('a') as log: log.write('pass\\n')\n")
        result = self.run_script(self.repo / "scripts/pre-push")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Ran 2 tests", result.stderr)
        self.assertEqual((self.repo / "executions").read_text(), "import\npass\n")

    def test_gate_runs_tests_and_propagates_failures(self):
        test = self.tests / "test_fixture.py"
        for expected, assertion in ((0, "True"), (1, "False")):
            test.write_text("import unittest\nclass Fixture(unittest.TestCase):\n"
                            f"    def test_fixture(self): self.assertTrue({assertion})\n")
            # Avoid timestamp/size based bytecode reuse when changing this tiny fixture.
            shutil.rmtree(self.tests / "__pycache__", ignore_errors=True)
            result = self.run_script(self.repo / "scripts/pre-push")
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
            self.assertIn("Ran 1 test", result.stderr)

    def test_installer_honours_hooks_path_and_worktrees(self):
        for hooks_path in (None, ".beads/hooks", str(self.root / "custom-hooks")):
            with self.subTest(hooks_path=hooks_path):
                if hooks_path:
                    self.git("config", "core.hooksPath", hooks_path)
                else:
                    self.git("config", "--unset", "core.hooksPath")
                result = self.run_script(self.repo / "scripts/install-hooks.sh")
                self.assertEqual(result.returncode, 0, result.stderr)
                hook = Path(self.git("rev-parse", "--git-path", "hooks/pre-push").strip())
                if not hook.is_absolute():
                    hook = self.repo / hook
                probe = subprocess.run([str(hook)], cwd=self.repo,
                    env=dict(os.environ, BENNETT_GATE_HOOK_PROBE="1"), capture_output=True, text=True)
                self.assertEqual(probe.returncode, 0, probe.stderr)
                self.assertIn("bennett-gate-hook-chained", probe.stdout)
                self.assertNotEqual(self.run_script(hook).returncode, 0)
        wt = self.root / "hook-worktree"
        self.git("add", "scripts", "tools")
        self.git("commit", "-qm", "hook fixture")
        self.git("worktree", "add", "-qb", "job/hook", str(wt))
        result = subprocess.run(["bash", "scripts/install-hooks.sh"], cwd=wt,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


class CommandTests(RunnerFixture):
    def test_council_selftest_runs_unittest_under_optimization(self):
        result = subprocess.run([sys.executable, "-O", str(SOURCE / "tools/council.py"), "selftest"],
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Ran ", result.stderr)
        self.assertIn("tests", result.stderr)

    def test_create_remotes_reports_hook_install_failure(self):
        meta = self.root / "bennett"
        (meta / "scripts").mkdir(parents=True)
        (meta / ".git").mkdir()
        (meta / "manifest.toml").write_text("[repos]\n")
        shutil.copy2(SOURCE / "scripts/create-remotes.sh", meta / "scripts/create-remotes.sh")
        install = meta / "scripts/install-hooks.sh"
        install.write_text("#!/bin/sh\necho 'broken hook install' >&2\nexit 23\n")
        install.chmod(0o755)
        self.executable("gh", "raise SystemExit(0)\n")
        self.executable("git", "raise SystemExit(0)\n")
        result = subprocess.run(["bash", str(meta / "scripts/create-remotes.sh")],
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 23, result.stdout + result.stderr)
        self.assertIn("broken hook install", result.stderr)


class IgnoreTests(RunnerFixture):
    def test_ecosystem_litter_patterns_preserve_beads_source(self):
        shutil.copy2(SOURCE / ".gitignore", self.repo / ".gitignore")
        for name in ("tools/__pycache__/module.pyc", "module.pyc", "run.log", "a/b/run.log",
                     ".beads/LOCK", ".beads/dolt/bennett/LOCK", "archive.darc"):
            with self.subTest(name=name):
                result = subprocess.run(["git", "check-ignore", "-q", "--", name], cwd=self.repo)
                self.assertEqual(result.returncode, 0, name)
        result = subprocess.run(["git", "check-ignore", "-q", "--", ".beads/issues.jsonl"], cwd=self.repo)
        self.assertEqual(result.returncode, 1)
