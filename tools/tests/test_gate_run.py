"""Gate receipts from tiny local repositories; no ecosystem gate is run."""
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

from fixtures import RunnerFixture


TOOL = Path(os.environ.get("GATE_TEST_TOOL", Path(__file__).resolve().parents[1] / "gate_run.py"))
# Meta has no guard table yet. Follow test_clone_all.py / test_main_health.py:
# Git 20s, CLI 30s, machine factor 1 on the shared 12-core / 30 GiB host.
# These are hang guards, never performance assertions; a trip is UNKNOWN.
# Initial five-fixture suite measured 1.78s here on 2026-11-08. Guards bound
# individual Git/CLI commands, not the expanded suite's cumulative duration.
GIT_HANG_GUARD_SECONDS = 20
CLI_HANG_GUARD_SECONDS = 30
# Synthetic clock advance, not a delay or a performance limit.
SETUP_CLOCK_OFFSET_SECONDS = 1000


def load_tool():
    spec = importlib.util.spec_from_file_location("gate_receipt_fixture", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ContentReceiptFixture(RunnerFixture):
    def setUp(self):
        super().setUp()
        self.env["BENNETT_GATE_WORKSPACE"] = str(self.root)
        (self.repo / ".gitignore").write_text(".tmp/\n")
        (self.repo / ".tmp").mkdir()
        self.marker = self.repo / ".tmp/executed"
        self.meta = self.root / "bennett"
        (self.meta / "tools").mkdir(parents=True)
        self.git("init", "-q", "-b", "main", cd=self.meta)
        (self.meta / "tools/gate_run.py").write_bytes(TOOL.read_bytes())
        self.git("add", "tools/gate_run.py", cd=self.meta)
        self.git("commit", "-qm", "gate tool fixture", cd=self.meta)
        self.tool_sha = self.git("rev-parse", "HEAD", cd=self.meta).strip()

    def config(self, fail_once=False, tool_sha=None):
        command = ("from pathlib import Path; "
                   f"p = Path({str(self.marker)!r}); "
                   "p.open('a').write('run\\n'); "
                   f"raise SystemExit({fail_once!r} and len(p.read_text().splitlines()) == 1)")
        (self.repo / "gate.toml").write_text(
            'schema = 1\nrepo = "repo"\ntool_sha = "' + (tool_sha or self.tool_sha) + '"\n'
            '\n[[check]]\nname = "marker"\n' +
            f'argv = {json.dumps([sys.executable, "-c", command])}\n')
        self.git("add", ".")
        self.git("commit", "-qm", "gate fixture")
        return self.git("rev-parse", "HEAD").strip()

    def run_gate(self, sha, *options, repo=None, isolated=False, tool=TOOL):
        return subprocess.run(
            [sys.executable, "-I", str(tool), "run", "--repo", str(repo or self.repo),
             "--sha", sha, *([] if isolated else ["--no-isolate"]), *options],
            env=self.env, capture_output=True, text=True, timeout=CLI_HANG_GUARD_SECONDS)

    def receipt_path(self, sha, isolated=False, tool_sha=None):
        tree = self.git("rev-parse", f"{sha}^{{tree}}").strip()
        key = hashlib.sha256(json.dumps([tree, tool_sha or self.tool_sha, isolated], sort_keys=True).encode()).hexdigest()
        return self.repo / ".tmp/gate/receipts" / f"{key}.json"


class ContentReceiptTests(ContentReceiptFixture):
    def test_identical_tree_is_covered_across_worktrees_before_preparation(self):
        sha = self.config()
        job = self.root / "repo-job"
        self.git("worktree", "add", "--detach", str(job), sha)
        first = self.run_gate(sha, repo=job)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(self.marker.read_text(), "run\n")
        self.git("commit", "--allow-empty", "-qm", "same tree, new commit")
        other = self.git("rev-parse", "HEAD").strip()
        self.assertNotEqual(sha, other)
        linked = self.root / "health/cache/repo"
        self.git("worktree", "add", "--detach", str(linked), other)
        # A receipt hit must not call prepare, even for a different checkout/SHA.
        bootstrap = '''import runpy, sys
path = sys.argv.pop(1)
tool = runpy.run_path(path)
def unexpected(*args, **kwargs):
    raise AssertionError("receipt hit prepared a worktree")
tool["gate_one"].__globals__["prepare"] = unexpected
raise SystemExit(tool["main"]())
'''
        covered = subprocess.run(
            [sys.executable, "-I", "-c", bootstrap, str(TOOL), "run", "--repo", str(linked),
             "--sha", other, "--no-isolate"], env=self.env, capture_output=True, text=True,
            timeout=CLI_HANG_GUARD_SECONDS)
        self.assertEqual(covered.returncode, 0, covered.stderr)
        receipt_path = self.receipt_path(sha)
        receipt = json.loads(receipt_path.read_text())
        self.assertEqual(covered.stderr, f"gate: PASS {other} covered by receipt {receipt_path}: "
                         f"tree {receipt['tree'][:12]} gated as {sha[:12]} at {receipt['finished_utc']}\n")
        self.assertEqual(self.marker.read_text(), "run\n")
        record = json.loads((linked / ".tmp/gate/records" / f"{other}.json").read_text())
        self.assertEqual((record["sha"], record["result"]), (other, "pass"))
        self.assertEqual(record["covered_by"], {"sha": sha, "receipt": str(receipt_path)})
        self.assertNotIn("checks", record)
        self.assertEqual(receipt["sha"], sha)
        self.assertEqual(receipt["key"], receipt_path.stem)
        self.assertIn("covered by receipt", self.run_gate(other).stderr)
        self.assertEqual(self.marker.read_text(), "run\n")

    def test_failed_run_writes_no_receipt_and_next_run_executes(self):
        sha = self.config(fail_once=True)
        failed = self.run_gate(sha)
        self.assertEqual(failed.returncode, 1, failed.stderr)
        self.assertFalse(self.receipt_path(sha).exists())
        passed = self.run_gate(sha)
        self.assertEqual(passed.returncode, 0, passed.stderr)
        self.assertEqual(self.marker.read_text(), "run\nrun\n")
        self.assertEqual(json.loads(self.receipt_path(sha).read_text())["result"], "pass")

    def test_tree_change_runs_checks_and_writes_distinct_receipt(self):
        sha = self.config()
        self.assertEqual(self.run_gate(sha).returncode, 0)
        (self.repo / "source").write_text("changed\n")
        self.git("add", "source")
        self.git("commit", "-qm", "changed tree")
        other = self.git("rev-parse", "HEAD").strip()
        result = self.run_gate(other)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("covered by receipt", result.stderr)
        self.assertEqual(self.marker.read_text(), "run\nrun\n")
        self.assertNotEqual(self.receipt_path(sha), self.receipt_path(other))
        for commit in (sha, other):
            self.assertEqual(json.loads(self.receipt_path(commit).read_text())["sha"], commit)

    def test_fresh_executes_and_replaces_receipt(self):
        sha = self.config()
        self.assertEqual(self.run_gate(sha).returncode, 0)
        self.git("commit", "--allow-empty", "-qm", "fresh commit")
        other = self.git("rev-parse", "HEAD").strip()
        fresh = self.run_gate(other, "--fresh")
        self.assertEqual(fresh.returncode, 0, fresh.stderr)
        self.assertNotIn("covered by receipt", fresh.stderr)
        self.assertEqual(self.marker.read_text(), "run\nrun\n")
        receipt = json.loads(self.receipt_path(other).read_text())
        record = json.loads((self.repo / ".tmp/gate/records" / f"{other}.json").read_text())
        self.assertTrue(record["fresh"])
        self.assertEqual(receipt, dict(record, tree=self.git("rev-parse", f"{other}^{{tree}}").strip(),
                                       key=self.receipt_path(other).stem))
        self.assertIn("covered by receipt", self.run_gate(sha).stderr)
        self.assertEqual(self.marker.read_text(), "run\nrun\n")

    def test_isolation_modes_do_not_cover_each_other_in_either_direction(self):
        sha = self.config()
        for isolated in (False, True):
            with self.subTest(first_isolated=isolated):
                if self.marker.exists():
                    self.marker.unlink()
                if isolated:
                    (self.repo / "source").write_text("another tree\n")
                    self.git("add", "source")
                    self.git("commit", "-qm", "second isolation order")
                    sha = self.git("rev-parse", "HEAD").strip()
                for mode in (isolated, not isolated):
                    result = self.run_gate(sha, isolated=mode)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertNotIn("covered by receipt", result.stderr)
                self.assertEqual(self.marker.read_text(), "run\nrun\n")
                self.assertIn("covered by receipt", self.run_gate(sha, isolated=isolated).stderr)
                self.assertEqual(self.marker.read_text(), "run\nrun\n")
                for mode in (False, True):
                    self.assertEqual(json.loads(self.receipt_path(sha, mode).read_text())["isolated"], mode)

    def test_invalid_receipts_are_reported_and_ignored(self):
        sha = self.config()
        self.assertEqual(self.run_gate(sha).returncode, 0)
        path = self.receipt_path(sha)
        good = json.loads(path.read_text())
        invalid = ("{", "[]", json.dumps(dict(good, key="wrong")), json.dumps(dict(good, sha=int("1" * 40))),
                   json.dumps(dict(good, result="fail")), json.dumps({"key": path.stem, "result": "pass"}))
        for index, content in enumerate(invalid, start=2):
            with self.subTest(content=content):
                path.write_text(content)
                result = self.run_gate(sha)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(f"receipt {path}", result.stderr)
                self.assertNotIn("covered by receipt", result.stderr)
                self.assertEqual(self.marker.read_text(), "run\n" * index)
                self.assertEqual(json.loads(path.read_text())["key"], path.stem)

    def test_unreadable_receipt_is_reported_and_replaced_after_checks(self):
        sha = self.config()
        self.assertEqual(self.run_gate(sha).returncode, 0)
        path = self.receipt_path(sha)
        path.chmod(0)
        result = self.run_gate(sha)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"receipt {path} unreadable:", result.stderr)
        self.assertNotIn("covered by receipt", result.stderr)
        self.assertEqual(self.marker.read_text(), "run\nrun\n")
        self.assertEqual(json.loads(path.read_text())["result"], "pass")


class ToolIdentityTests(ContentReceiptFixture):
    def assert_unverified(self, result, sha, executions):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS RECEIPTS DISABLED", result.stderr)
        self.assertIn("tool identity", result.stderr)
        self.assertNotIn("covered by receipt", result.stderr)
        self.assertNotIn("an ancestor of the running None", result.stderr)
        self.assertEqual(self.marker.read_text(), "run\n" * executions)
        record = json.loads((self.repo / ".tmp/gate/records" / f"{sha}.json").read_text())
        self.assertIsNone(record["tool_sha_ran"])
        self.assertEqual(record["result"], "pass")
        self.assertEqual([c["name"] for c in record["checks"]], ["marker"])

    def test_nonexistent_tool_commit_never_publishes_or_reuses_pass(self):
        missing = "1" * 40
        sha = self.config(tool_sha=missing)
        self.assertNotEqual(subprocess.run(
            ["git", "-C", str(self.meta), "cat-file", "-e", f"{missing}^{{commit}}"],
            env=self.env, capture_output=True, timeout=GIT_HANG_GUARD_SECONDS).returncode, 0)
        path = self.receipt_path(sha, True, missing)
        self.assert_unverified(self.run_gate(sha, isolated=True), sha, 1)
        self.assertFalse(path.exists())
        # An old unidentified run may already have populated this claimed key.
        path.parent.mkdir(parents=True, exist_ok=True)
        legacy = json.dumps(dict(key=path.stem, tree=self.git("rev-parse", f"{sha}^{{tree}}").strip(),
                                 sha=sha, result="pass", finished_utc="2026-11-08T12:00:00Z"))
        path.write_text(legacy)
        self.assert_unverified(self.run_gate(sha, "--tool-sha", missing, isolated=True), sha, 2)
        self.assertEqual(path.read_text(), legacy)
        self.assert_unverified(self.run_gate(sha, "--fresh", isolated=True), sha, 3)
        self.assertEqual(path.read_text(), legacy)

    def test_mismatched_source_cannot_reuse_or_replace_verified_receipt(self):
        sha = self.config()
        self.assertEqual(self.run_gate(sha, "--tool-sha", self.tool_sha).returncode, 0)
        path = self.receipt_path(sha)
        verified = path.read_bytes()
        modified = self.root / "experimental.py"
        modified.write_bytes(TOOL.read_bytes() + b"\n# experimental copy\n")
        for executions, options in enumerate(((), ("--tool-sha", self.tool_sha)), start=2):
            with self.subTest(options=options):
                result = self.run_gate(sha, *options, tool=modified)
                self.assert_unverified(result, sha, executions)
                self.assertIn("source", result.stderr)
                self.assertEqual(path.read_bytes(), verified)
        covered = self.run_gate(sha)
        self.assertIn("covered by receipt", covered.stderr)
        self.assertEqual(self.marker.read_text(), "run\n" * 3)

    def test_existing_commit_without_tool_source_is_unverifiable(self):
        self.git("rm", "tools/gate_run.py", cd=self.meta)
        self.git("commit", "-qm", "no gate source", cd=self.meta)
        pin = self.git("rev-parse", "HEAD", cd=self.meta).strip()
        sha = self.config(tool_sha=pin)
        self.assert_unverified(self.run_gate(sha), sha, 1)
        self.assertFalse(self.receipt_path(sha, tool_sha=pin).exists())

    def test_missing_meta_checkout_is_unverifiable(self):
        sha = self.config()
        self.meta.rename(self.root / "unavailable-meta")
        self.assert_unverified(self.run_gate(sha), sha, 1)
        self.assertFalse(self.receipt_path(sha).exists())

    def test_unreadable_executing_source_is_unverifiable(self):
        sha = self.config()
        bootstrap = '''import runpy, sys
path = sys.argv.pop(1)
tool = runpy.run_path(path)
tool["gate_one"].__globals__["__file__"] = path + ".missing"
raise SystemExit(tool["main"]())
'''
        result = subprocess.run(
            [sys.executable, "-I", "-c", bootstrap, str(TOOL), "run", "--repo", str(self.repo),
             "--sha", sha, "--no-isolate"], env=self.env, capture_output=True, text=True,
            timeout=CLI_HANG_GUARD_SECONDS)
        self.assert_unverified(result, sha, 1)
        self.assertFalse(self.receipt_path(sha).exists())

    def test_unverified_tool_keeps_failed_checks_and_reports(self):
        sha = self.config(fail_once=True, tool_sha="1" * 40)
        with (self.repo / "gate.toml").open("a") as config:
            config.write('\n[[report]]\nname = "evidence"\nargv = ["sh", "-c", "exit 9"]\n')
        self.git("add", "gate.toml")
        self.git("commit", "-qm", "report fixture")
        sha = self.git("rev-parse", "HEAD").strip()
        result = self.run_gate(sha)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("PASS RECEIPTS DISABLED", result.stderr)
        record = json.loads((self.repo / ".tmp/gate/records" / f"{sha}.json").read_text())
        self.assertIsNone(record["tool_sha_ran"])
        self.assertEqual(record["checks"][0]["exit"], 1)
        self.assertEqual(record["reports"][0]["exit"], 9)
        self.assertFalse(self.receipt_path(sha, tool_sha="1" * 40).exists())

    def test_verified_distinct_tool_commits_keep_separate_receipts(self):
        sha = self.config()
        self.git("commit", "--allow-empty", "-qm", "new tool revision", cd=self.meta)
        newer = self.git("rev-parse", "HEAD", cd=self.meta).strip()
        for pin in (self.tool_sha, newer):
            result = self.run_gate(sha, "--tool-sha", pin, isolated=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("covered by receipt", result.stderr)
            path = self.receipt_path(sha, True, pin)
            self.assertEqual(json.loads(path.read_text())["tool_sha_ran"], pin)
        self.assertNotEqual(self.receipt_path(sha, True), self.receipt_path(sha, True, newer))
        self.assertEqual(self.marker.read_text(), "run\nrun\n")
        self.assertIn("covered by receipt", self.run_gate(sha, "--tool-sha", newer, isolated=True).stderr)

    def test_sibling_pin_changes_invalidate_verified_receipt(self):
        sibling = self.root / "sibling"
        sibling.mkdir()
        self.git("init", "-q", "-b", "main", cd=sibling)
        (sibling / "data").write_text("first\n")
        self.git("add", "data", cd=sibling)
        self.git("commit", "-qm", "first", cd=sibling)
        first = self.git("rev-parse", "HEAD", cd=sibling).strip()
        (sibling / "data").write_text("second\n")
        self.git("commit", "-am", "second", cd=sibling)
        second = self.git("rev-parse", "HEAD", cd=sibling).strip()
        self.config()
        config = self.repo / "gate.toml"
        original = config.read_text()
        paths = []
        for pin in (first, second):
            config.write_text(original + f'\n[siblings.sibling]\nsha = "{pin}"\n')
            self.git("add", "gate.toml")
            self.git("commit", "-qm", "sibling pin")
            sha = self.git("rev-parse", "HEAD").strip()
            result = self.run_gate(sha, isolated=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("covered by receipt", result.stderr)
            paths.append(self.receipt_path(sha, True))
            self.assertTrue(paths[-1].exists())
        self.assertNotEqual(*paths)
        self.assertEqual(self.marker.read_text(), "run\nrun\n")

    def test_hook_extracted_tool_reuses_legacy_fixture_receipt_with_unchanged_key(self):
        sha = self.config()
        tree = self.git("rev-parse", f"{sha}^{{tree}}").strip()
        # The original receipt contract: these exact JSON bytes were hashed.
        legacy_key = hashlib.sha256(f'["{tree}", "{self.tool_sha}", true]'.encode()).hexdigest()
        path = self.repo / ".tmp/gate/receipts" / f"{legacy_key}.json"
        path.parent.mkdir(parents=True)
        fixture = json.dumps(dict(key=legacy_key, tree=tree, sha=sha, result="pass",
                                  tool_sha=self.tool_sha, tool_sha_ran=self.tool_sha, isolated=True,
                                  finished_utc="2026-11-09T06:00:00Z",
                                  checks=[dict(name="marker", exit=0, seconds=0.1)])) + "\n"
        path.write_text(fixture)
        hook = self.repo / "scripts/pre-push"
        hook.parent.mkdir()
        hook.write_bytes((TOOL.parent / "gate_pre-push.template").read_bytes())
        hook.chmod(0o755)
        result = subprocess.run([str(hook), "--sha", sha], env=self.env,
                                stdin=subprocess.DEVNULL, capture_output=True, text=True,
                                timeout=CLI_HANG_GUARD_SECONDS)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("PASS RECEIPTS DISABLED", result.stderr)
        self.assertIn(f"covered by receipt {path}", result.stderr)
        self.assertFalse(self.marker.exists())
        self.assertEqual(path.read_text(), fixture)
        extracted = self.repo / f".tmp/gate/tool/gate_run-{self.tool_sha}.py"
        self.assertEqual(extracted.read_bytes(), TOOL.read_bytes())
        record = json.loads((self.repo / ".tmp/gate/records" / f"{sha}.json").read_text())
        self.assertEqual(record["covered_by"]["receipt"], str(path))
        self.assertNotIn("checks", record)


class ReceiptTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.workspace = Path(scratch.name)
        self.env = {k: v for k, v in os.environ.items()
                    if not k.startswith("GIT_") and k not in load_tool().HEADLESS
                    and k not in {"CARGO_BUILD_JOBS", "RUST_TEST_THREADS"}}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                        GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
                        BENNETT_GATE_WORKSPACE=str(self.workspace))
        self.repo = self.workspace / "fixture"
        self.probe_attempt = 0
        self.repo.mkdir()
        self.git(self.repo, "init", "-qb", "main")
        (self.repo / ".gitignore").write_text(".tmp/\n")

    def git(self, repo, *args):
        return subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-C", str(repo), *args],
                              env=self.env, capture_output=True, text=True, check=True,
                              timeout=GIT_HANG_GUARD_SECONDS).stdout.strip()

    def commit(self, repo):
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-qm", "fixture")
        return self.git(repo, "rev-parse", "HEAD")

    def config(self, checks=None, extra=""):
        text = 'schema = 1\nrepo = "fixture"\ntool_sha = "' + "1" * 40 + '"\n' + extra
        for index, check in enumerate(checks or [[sys.executable, "-c", "pass"]]):
            text += f'\n[[check]]\nname = "check {index}"\nargv = {json.dumps(check)}\n'
        (self.repo / "gate.toml").write_text(text)
        return self.commit(self.repo)

    def run_gate(self, sha, bootstrap=None, extra_env=None, fresh=False):
        invocation = ([sys.executable, "-I", "-c", bootstrap, str(TOOL)] if bootstrap
                      else [sys.executable, "-I", str(TOOL)])
        return subprocess.run([*invocation, "run", "--repo", str(self.repo), "--sha", sha,
                               "--no-isolate", *(["--fresh"] if fresh else [])], env=dict(self.env, **(extra_env or {})),
                              capture_output=True, text=True, timeout=CLI_HANG_GUARD_SECONDS)

    def receipt(self, sha):
        return json.loads((self.repo / ".tmp/gate/records" / f"{sha}.json").read_text())

    def failed_probe_gate(self, patch, extra="", check_exit=0):
        self.probe_attempt += 1
        marker = self.workspace / f"executed-{self.probe_attempt}"
        def command(letter):
            return [sys.executable, "-c", "from pathlib import Path; "
                    f"p = Path({str(marker)!r}); "
                    f"p.open('a').write({letter!r})"]
        report = command("R")
        report[-1] += "; raise SystemExit(9)"
        checks = [command("A"), command("B")]
        checks[-1][-1] += f"; raise SystemExit({check_exit})"
        sha = self.config(checks, extra=extra +
                          '\n[[report]]\nname = "evidence"\n' +
                          f'argv = {json.dumps(report)}\n')
        baseline = self.run_gate(sha)
        self.assertEqual(baseline.returncode, 1 if check_exit else 0, baseline.stderr)
        self.assertEqual(marker.read_text(), "ABR")
        marker.unlink()
        bootstrap = '''import importlib.util, sys
from pathlib import Path
path = sys.argv.pop(1)
spec = importlib.util.spec_from_file_location("gate_fixture", path)
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)
def unavailable(*args, **kwargs):
    raise OSError("fixture probe denied")
''' + patch + '\nraise SystemExit(tool.main())\n'
        result = self.run_gate(sha, bootstrap, fresh=True)
        self.assertEqual(result.returncode, baseline.returncode, result.stderr)
        self.assertIn("unavailable", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(marker.read_text(), "ABR")
        receipt = self.receipt(sha)
        self.assertEqual(receipt["result"], "fail" if check_exit else "pass")
        self.assertEqual([check["exit"] for check in receipt["checks"]], [0, check_exit])
        self.assertEqual(receipt["reports"][0]["exit"], 9)
        return receipt

    def test_meminfo_probe_failure_is_explicit_and_keeps_gate_pass(self):
        for mode, expected in [("denied", "PermissionError"), ("missing", "KeyError")]:
            with self.subTest(mode=mode):
                patch = f'''original_read = Path.read_text
def read(path, *args, **kwargs):
    if str(path) == "/proc/meminfo":
        if {mode!r} == "missing":
            return ""
        raise PermissionError("fixture meminfo denied")
    return original_read(path, *args, **kwargs)
Path.read_text = read
'''
                receipt = self.failed_probe_gate(patch)
                for field in ("mem_total_kib", "mem_available_kib", "label"):
                    self.assertIn("unavailable", receipt["machine"][field])
                self.assertIn(expected, receipt["machine"]["mem_total_kib"]["unavailable"])
                self.assertGreater(receipt["machine"]["nproc"], 0)
                self.assertIsInstance(receipt["machine"]["load1"], float)

    def test_loadavg_probe_failure_is_explicit_and_keeps_gate_pass(self):
        receipt = self.failed_probe_gate("tool.os.getloadavg = unavailable")
        self.assertEqual(receipt["machine"]["load1"], {"unavailable": "OSError: fixture probe denied"})
        self.assertGreater(receipt["machine"]["mem_total_kib"], 0)
        self.assertGreater(receipt["machine"]["nproc"], 0)

    def test_nproc_probe_failure_is_explicit_and_keeps_gate_pass(self):
        receipt = self.failed_probe_gate("tool.os.sched_getaffinity = unavailable")
        self.assertEqual(receipt["machine"]["nproc"], {"unavailable": "OSError: fixture probe denied"})
        self.assertIn("unavailable", receipt["machine"]["label"])
        self.assertGreater(receipt["machine"]["mem_total_kib"], 0)

    def test_machine_label_probe_failure_is_explicit_and_keeps_gate_pass(self):
        receipt = self.failed_probe_gate("tool.platform.machine = unavailable")
        self.assertEqual(receipt["machine"]["label"], {"unavailable": "OSError: fixture probe denied"})
        self.assertGreater(receipt["machine"]["nproc"], 0)

    def test_wait4_probe_failure_is_explicit_and_keeps_gate_pass(self):
        receipt = self.failed_probe_gate("tool.os.wait4 = unavailable")
        for command in receipt["checks"] + receipt["reports"]:
            for field in ("cpu_seconds", "peak_rss_kib"):
                self.assertEqual(command[field], {"unavailable": "OSError: fixture probe denied"})
            self.assertGreater(command["wall_seconds"], 0)

    def test_wait4_probe_failure_preserves_a_failed_check_status(self):
        receipt = self.failed_probe_gate("tool.os.wait4 = unavailable", check_exit=7)
        self.assertEqual(receipt["checks"][1]["cpu_seconds"],
                         {"unavailable": "OSError: fixture probe denied"})

    def test_cpu_and_rss_probes_fail_independently_and_keep_gate_pass(self):
        for attribute, field, other in [("ru_utime", "cpu_seconds", "peak_rss_kib"),
                                         ("ru_maxrss", "peak_rss_kib", "cpu_seconds")]:
            with self.subTest(field=field):
                patch = f'''original_wait4 = tool.os.wait4
class Usage:
    def __init__(self, usage):
        self.usage = usage
    def __getattr__(self, name):
        if name == {attribute!r}:
            return unavailable()
        return getattr(self.usage, name)
def wait4(*args):
    pid, status, usage = original_wait4(*args)
    return pid, status, Usage(usage)
tool.os.wait4 = wait4
'''
                receipt = self.failed_probe_gate(patch)
                for command in receipt["checks"] + receipt["reports"]:
                    self.assertEqual(command[field], {"unavailable": "OSError: fixture probe denied"})
                    self.assertGreater(command[other], 0)

    def test_cache_state_probe_failure_is_explicit_and_keeps_gate_pass(self):
        sibling = self.workspace / "sibling"
        sibling.mkdir()
        self.git(sibling, "init", "-qb", "main")
        (sibling / "source").write_text("fixture\n")
        pin = self.commit(sibling)
        patch = '''original_prepare = tool.prepare
def prepare(*args, **kwargs):
    result = original_prepare(*args, **kwargs)
    del result[1].notes["sibling"]["cache_state"]
    return result
tool.prepare = prepare
'''
        receipt = self.failed_probe_gate(patch, f'[siblings.sibling]\nsha = "{pin}"\n')
        self.assertEqual(receipt["siblings"]["sibling"]["cache_state"],
                         {"unavailable": "KeyError: 'cache_state'"})
        self.assertEqual(receipt["siblings"]["sibling"]["sha"], pin)

    def test_width_env_probe_failure_is_explicit_and_keeps_gate_pass(self):
        receipt = self.failed_probe_gate('''class WidthKeys:
    def __iter__(self):
        return unavailable()
tool.WIDTH_ENV = WidthKeys()
''')
        for command in [receipt, *receipt["checks"], *receipt["reports"]]:
            self.assertEqual(command["width_env"], {"unavailable": "OSError: fixture probe denied"})

    def test_clock_probe_failure_is_explicit_and_keeps_gate_pass(self):
        for mode in ("start", "end"):
            with self.subTest(mode=mode):
                patch = ("tool.time.monotonic = unavailable" if mode == "start" else '''clock = tool.time.monotonic
calls = 0
def monotonic():
    global calls
    calls += 1
    return unavailable() if calls % 2 == 0 else clock()
tool.time.monotonic = monotonic
''')
                receipt = self.failed_probe_gate(patch)
                self.assertEqual(receipt["setup_seconds"], {"unavailable": "OSError: fixture probe denied"})
                for command in receipt["checks"] + receipt["reports"]:
                    for field in ("wall_seconds", "seconds"):
                        self.assertEqual(command[field], {"unavailable": "OSError: fixture probe denied"})
                    self.assertGreater(command["cpu_seconds"], 0)

    def test_finished_time_probe_failure_is_explicit_and_keeps_gate_pass(self):
        receipt = self.failed_probe_gate('''original_prepare = tool.prepare
def prepare(*args, **kwargs):
    result = original_prepare(*args, **kwargs)
    tool.time.strftime = unavailable
    return result
tool.prepare = prepare
''')
        self.assertEqual(receipt["finished_utc"], {"unavailable": "OSError: fixture probe denied"})

    def test_metadata_and_setup_are_separate_from_check_time(self):
        sha = self.config(extra='[env]\nCARGO_BUILD_JOBS = "3"\n'
                          '\n[[report]]\nname = "status"\nargv = ["sh", "-c", "exit 9"]\n')
        bootstrap = f'''import importlib.util, sys, time
path = sys.argv.pop(1)
spec = importlib.util.spec_from_file_location("gate_fixture", path)
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)
original_prepare, clock = tool.prepare, time.monotonic
offset = 0
tool.time.monotonic = lambda: clock() + offset
def prepare(*args, **kwargs):
    global offset
    result = original_prepare(*args, **kwargs)
    offset += {SETUP_CLOCK_OFFSET_SECONDS}
    return result
tool.prepare = prepare
raise SystemExit(tool.main())
'''
        before = time.monotonic()
        result = self.run_gate(sha, bootstrap, {"RUST_TEST_THREADS": "2"})
        elapsed = time.monotonic() - before
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = self.receipt(sha)
        self.assertGreaterEqual(receipt["setup_seconds"], SETUP_CLOCK_OFFSET_SECONDS)
        self.assertLessEqual(receipt["setup_seconds"] - SETUP_CLOCK_OFFSET_SECONDS, elapsed)
        for command in receipt["checks"] + receipt["reports"]:
            self.assertLessEqual(command["wall_seconds"], elapsed)
            self.assertEqual(command["seconds"], round(command["wall_seconds"], 1))
            self.assertGreaterEqual(command["cpu_seconds"], 0)
            self.assertGreater(command["peak_rss_kib"], 0)
            self.assertEqual(command["width_env"]["CARGO_BUILD_JOBS"], "3")
            self.assertEqual(command["width_env"]["RUST_TEST_THREADS"], "2")
        profile = receipt["machine"]
        self.assertGreater(profile["nproc"], 0)
        self.assertGreater(profile["mem_total_kib"], 0)
        self.assertGreaterEqual(profile["mem_available_kib"], 0)
        self.assertGreaterEqual(profile["load1"], 0)
        self.assertRegex(profile["label"], r"^machine-[0-9a-f]{12}$")
        self.assertEqual(receipt["width_env"]["CARGO_BUILD_JOBS"], "3")
        self.assertEqual(receipt["reports"][0]["exit"], 9)
        self.assertEqual(receipt["result"], "pass")

    def test_resources_include_descendants_and_rss_is_per_command(self):
        # Child reports an independent lower bound. Its parent also consumes CPU,
        # so measuring only the shell/parent cannot satisfy the CPU assertion.
        usage = self.workspace / "usage.json"
        child = ('import json, resource; from pathlib import Path; '
                 'data = bytearray(32 * 1024 * 1024); '
                 'sum(i*i for i in range(500000)); '
                 'r = resource.getrusage(resource.RUSAGE_SELF); '
                 f'Path({str(usage)!r}).write_text(json.dumps('
                 'dict(cpu=r.ru_utime + r.ru_stime, rss=r.ru_maxrss)))')
        parent = f'import subprocess, sys; subprocess.run([sys.executable, "-c", {child!r}], check=True)'
        sha = self.config([[sys.executable, "-c", parent], [sys.executable, "-c", "pass"]])
        result = self.run_gate(sha)
        self.assertEqual(result.returncode, 0, result.stderr)
        heavy, light = self.receipt(sha)["checks"]
        independent = json.loads(usage.read_text())
        self.assertGreaterEqual(heavy["cpu_seconds"], independent["cpu"])
        self.assertGreaterEqual(heavy["peak_rss_kib"], independent["rss"])
        self.assertGreater(heavy["peak_rss_kib"], light["peak_rss_kib"])
        self.assertNotEqual(heavy["wall_seconds"], heavy["seconds"])

    def test_sibling_cache_states_and_effective_width_overrides(self):
        sibling = self.workspace / "sibling"
        sibling.mkdir()
        self.git(sibling, "init", "-qb", "main")
        (sibling / "source").write_text("fixture\n")
        pin = self.commit(sibling)
        sha = self.config(extra=f'[siblings.sibling]\nsha = "{pin}"\n')
        result = self.run_gate(sha)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.receipt(sha)["siblings"]["sibling"]["cache_state"], "materialised")
        with (self.repo / "gate.toml").open("a") as config:
            config.write('\n[[siblings.sibling.build]]\nname = "fixture build"\n'
                         'argv = ["sh", "-c", "echo built > output"]\noutputs = ["output"]\n'
                         '\n[[check]]\nname = "width override"\nargv = ["true"]\n'
                         'env = {CARGO_BUILD_JOBS = "7"}\n')
        sha = self.commit(self.repo)
        result = self.run_gate(sha)
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = self.receipt(sha)
        self.assertEqual(receipt["siblings"]["sibling"]["cache_state"], "built")
        self.assertNotIn("CARGO_BUILD_JOBS", receipt["checks"][0]["width_env"])
        self.assertEqual(receipt["checks"][1]["width_env"]["CARGO_BUILD_JOBS"], "7")
        result = self.run_gate(sha, fresh=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.receipt(sha)["siblings"]["sibling"]["cache_state"], "hit")

    def test_check_exit_and_missing_executable_keep_their_meaning(self):
        for argv, expected in [(["sh", "-c", "exit 7"], 7), (["./missing-command"], 127)]:
            with self.subTest(argv=argv):
                sha = self.config([argv, ["true"]])
                result = self.run_gate(sha)
                self.assertEqual(result.returncode, 1, result.stderr)
                receipt = self.receipt(sha)
                self.assertEqual([c["exit"] for c in receipt["checks"]], [expected])
                if expected == 127:
                    for field in ("cpu_seconds", "peak_rss_kib"):
                        self.assertIn("FileNotFoundError:", receipt["checks"][0][field]["unavailable"])
                else:
                    self.assertGreaterEqual(receipt["checks"][0]["cpu_seconds"], 0)

    def test_expired_command_guard_keeps_exit_and_records_reaped_usage(self):
        # Killing immediately after exec can legitimately yield zero CPU usage.
        # Wait for independently sampled positive usage before applying the
        # already-expired guard. No delay, and production wait/kill/reap is intact.
        usage = self.workspace / "usage.json"
        child = f'''import json, os, resource, signal
from pathlib import Path
data = bytearray(8 * 1024 * 1024)
while True:
    sum(i*i for i in range(10000))
    r = resource.getrusage(resource.RUSAGE_SELF)
    if r.ru_utime + r.ru_stime > 0:
        break
Path({str(usage)!r}).write_text(json.dumps(dict(cpu=r.ru_utime + r.ru_stime, rss=r.ru_maxrss)))
with os.fdopen(int(os.environ["GATE_USAGE_READY_FD"]), "wb") as ready:
    ready.write(b"ready")
signal.pause()
'''
        bootstrap = '''import importlib.util, os, sys
path = sys.argv.pop(1)
spec = importlib.util.spec_from_file_location("gate_fixture", path)
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)
class ReadyProcess(tool.ResourceProcess):
    def __init__(self, *args, **kwargs):
        read_fd, write_fd = os.pipe()
        with os.fdopen(read_fd, "rb") as ready:
            try:
                kwargs["env"] = dict(kwargs["env"], GATE_USAGE_READY_FD=str(write_fd))
                super().__init__(*args, **kwargs, pass_fds=(write_fd,))
            finally:
                os.close(write_fd)
            assert ready.read() == b"ready", "child did not publish its usage sample"
tool.ResourceProcess = ReadyProcess
raise SystemExit(tool.main())
'''
        sha = self.config([[sys.executable, "-c", child]], extra="timeout_s = 0\n")
        result = self.run_gate(sha, bootstrap)
        self.assertEqual(result.returncode, 1, result.stderr)
        command = self.receipt(sha)["checks"][0]
        independent = json.loads(usage.read_text())
        self.assertEqual(command["exit"], 124)
        self.assertGreater(independent["cpu"], 0)
        self.assertGreater(independent["rss"], 0)
        self.assertGreaterEqual(command["cpu_seconds"], independent["cpu"])
        self.assertGreaterEqual(command["peak_rss_kib"], independent["rss"])

    def test_existing_lock_error_names_holder(self):
        tool = load_tool()
        path = self.workspace / "lock"
        with tool.Lock(path, blocking=False):
            with self.assertRaisesRegex(tool.GateError, rf"pid={os.getpid()}.*started_utc=\S+"):
                with tool.Lock(path, blocking=False):
                    self.fail("existing flock unexpectedly admitted another holder")


class ReformTests(ContentReceiptFixture):
    def adopt(self, extra='', command=None):
        self.config()
        if command:
            text = (self.repo / 'gate.toml').read_text()
            text = text[:text.index('argv =')] + 'argv = ' + json.dumps(command) + '\n'
            (self.repo / 'gate.toml').write_text(text)
        with (self.repo / 'gate.toml').open('a') as f:
            f.write('\n' + extra)
        self.git('add', '.')
        self.git('commit', '--allow-empty', '-qm', 'reform config')
        return self.git('rev-parse', 'HEAD').strip()

    def record(self, sha, repo=None):
        return json.loads(((repo or self.repo) / '.tmp/gate/records' / (sha + '.json')).read_text())

    def test_filtered_receipt_covers_docs_but_not_product_byte(self):
        (self.repo / 'notes').mkdir()
        (self.repo / 'notes/a').write_text('one')
        sha = self.adopt('[receipt]\nnon_product = ["notes/"]\n')
        first = self.run_gate(sha)
        self.assertEqual(first.returncode, 0, first.stderr)
        (self.repo / 'notes/a').write_text('two')
        self.git('add', '.')
        self.git('commit', '-qm', 'notes only')
        other = self.git('rev-parse', 'HEAD').strip()
        self.assertEqual(self.run_gate(other).returncode, 0)
        self.assertEqual(self.record(other)['covered_by']['sha'], sha)
        (self.repo / 'product').write_text('x')
        self.git('add', '.')
        self.git('commit', '-qm', 'product byte')
        third = self.git('rev-parse', 'HEAD').strip()
        self.assertEqual(self.run_gate(third).returncode, 0)
        self.assertNotIn('covered_by', self.record(third))
        self.assertEqual(self.marker.read_text(), 'run\nrun\n')

    def test_excluded_file_missing_from_filesystem_and_git_head(self):
        (self.repo / 'notes').write_text('secret')
        for command in (["cat", "notes"], ['git', 'show', 'HEAD:notes']):
            sha = self.adopt('[receipt]\nnon_product = ["notes"]\n', command)
            result = self.run_gate(sha)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertNotEqual(self.record(sha)['checks'][0]['exit'], 0)

    def test_refusals_name_entry_and_exit_setup(self):
        cases = [('', ''), ('/absolute', ''), ('a/../b', ''), ('*.md', ''),
                 ('gate.toml', ''), ('scripts/', ''), ('cat', ''),
                 ('data/', 'cwd = "data/run"\n'),
                 ('data/', '[env]\nDATA = "{wt}/data/input"\n'),
                 ('data/', '[env]\nDATA = "data/input"\n')]
        for entry, extra in cases:
            with self.subTest(entry=entry, extra=extra):
                sha = self.adopt(extra + '[receipt]\nnon_product = ' + json.dumps([entry]) + '\n', ['cat', 'notes'])
                result = self.run_gate(sha)
                self.assertEqual(result.returncode, 3, result.stderr)
                self.assertIn(repr(entry), result.stderr)

    def test_tiers_reuse_premerge_and_inputs_trigger_again_on_change(self):
        (self.repo / 'input').write_text('a')
        extra = ('[[check]]\nname = "slow"\nargv = ["true"]\n'
                 'tier = "post-merge"\ninputs = ["input"]\n')
        sha = self.adopt(extra)
        first = self.run_gate(sha)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(len(self.record(sha)['checks']), 2)
        full = self.run_gate(sha, '--tier', 'full')
        self.assertEqual(full.returncode, 0, full.stderr)
        self.assertEqual([c['name'] for c in self.record(sha)['checks']], ['slow'])
        self.assertIn('pre-merge', self.record(sha)['tiers_covered'])
        (self.repo / 'product').write_text('unrelated')
        self.git('add', '.')
        self.git('commit', '-qm', 'unrelated product')
        other = self.git('rev-parse', 'HEAD').strip()
        self.assertEqual(self.run_gate(other).returncode, 0)
        self.assertEqual([c['name'] for c in self.record(other)['checks']], ['marker'])
        self.assertIn('inputs unchanged since', self.record(other)['deferred'][0]['reason'])
        (self.repo / 'input').write_text('b')
        self.git('add', '.')
        self.git('commit', '-qm', 'input changed')
        third = self.git('rev-parse', 'HEAD').strip()
        self.assertEqual(self.run_gate(third).returncode, 0)
        self.assertEqual(len(self.record(third)['checks']), 2)
        self.assertEqual(self.marker.read_text(), 'run\nrun\nrun\n')

    def test_worktrees_have_private_real_caches_and_linked_git_isolation(self):
        sha = self.adopt(command=['git', 'cat-file', '-e', 'HEAD'])
        jobs = [self.root / 'job-a', self.root / 'job-b']
        for job in jobs:
            self.git('worktree', 'add', '--detach', str(job), sha)
            (job / '.tmp/gate').mkdir(parents=True)
            (job / '.tmp/gate/cache').symlink_to(self.root / 'missing-cache')
            result = self.run_gate(sha, '--fresh', repo=job, isolated=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            for name in ('cache', 'locks', 'runs', 'records'):
                self.assertTrue((job / '.tmp/gate' / name).is_dir())
                self.assertFalse((job / '.tmp/gate' / name).is_symlink())
        self.assertTrue(all(self.record(sha, job)['isolated'] for job in jobs))

    def test_postmerge_without_inputs_defers_until_full(self):
        sha = self.adopt('[[check]]\nname = "later"\nargv = ["false"]\ntier = "post-merge"\n')
        pre = self.run_gate(sha)
        self.assertEqual(pre.returncode, 0, pre.stderr)
        self.assertEqual(self.run_gate(sha, '--tier', 'full').returncode, 1)
        self.assertEqual(self.marker.read_text(), 'run\n')

    def test_invalid_tier_inputs_configuration_is_setup_error(self):
        for suffix in ('tier = "oops"\n', 'inputs = ["input"]\n',
                       'tier = "post-merge"\ninputs = ["../escape"]\n'):
            sha = self.adopt('[[check]]\nname = "bad"\nargv = ["true"]\n' + suffix)
            result = self.run_gate(sha)
            self.assertEqual(result.returncode, 3, result.stderr)

    def test_templates_cannot_hide_protected_commands(self):
        for argv, extra, entry in [(['{wt}/data/check'], '', 'data/'),
                                    (['true'], 'cwd = "{wt}/data"\n', 'data/'),
                                    (['true'], '', '.git/')]:
            sha = self.adopt(extra + '[receipt]\nnon_product = ' + json.dumps([entry]) + '\n', argv)
            result = self.run_gate(sha)
            self.assertEqual(result.returncode, 3, result.stderr)
            self.assertIn(repr(entry), result.stderr)

    def test_inputs_directory_without_slash_detects_content_change(self):
        (self.repo / 'data').mkdir()
        (self.repo / 'data/input').write_text('a')
        sha = self.adopt('[[check]]\nname = "slow"\nargv = ["true"]\ntier = "post-merge"\ninputs = ["data"]\n')
        self.assertEqual(self.run_gate(sha).returncode, 0)
        (self.repo / 'data/input').write_text('b')
        self.git('add', '.')
        self.git('commit', '-qm', 'directory input changed')
        other = self.git('rev-parse', 'HEAD').strip()
        self.assertEqual(self.run_gate(other).returncode, 0)
        self.assertEqual(len(self.record(other)['checks']), 2)

    def test_full_pass_also_covers_subsequent_premerge(self):
        sha = self.adopt('[[check]]\nname = "slow"\nargv = ["true"]\ntier = "post-merge"\n')
        self.assertEqual(self.run_gate(sha, '--tier', 'full').returncode, 0)
        self.assertEqual(self.run_gate(sha).returncode, 0)
        self.assertIn('covered_by', self.record(sha))
        self.assertEqual(self.marker.read_text(), 'run\n')

    def test_report_commands_cwd_and_env_are_protected(self):
        for command in ('argv = ["data/report"]\n',
                        'argv = ["true"]\ncwd = "data/run"\n',
                        'argv = ["true"]\nenv = {DATA = "{root}/data/report"}\n'):
            sha = self.adopt('[[report]]\nname = "report"\n' + command + '[receipt]\nnon_product = ["data/"]\n')
            result = self.run_gate(sha)
            self.assertEqual(result.returncode, 3, result.stderr)
            self.assertIn("'data/'", result.stderr)

    def test_two_worktrees_run_concurrently_with_same_pin(self):
        sibling = self.root / 'pin'
        sibling.mkdir()
        self.git('init', '-qb', 'main', cd=sibling)
        (sibling / 'data').write_text('pin')
        self.git('add', '.', cd=sibling)
        self.git('commit', '-qm', 'pin', cd=sibling)
        pin = self.git('rev-parse', 'HEAD', cd=sibling).strip()
        # Each command announces entry and blocks until both gates are admitted.
        # Files at workspace root survive isolation, unlike live checkout directories.
        release = self.root / 'release'
        command = [sys.executable, '-c',
                   'from pathlib import Path; import time; '
                   'ready = Path("{root}").name; '
                   f'Path({str(self.root)!r}, ready + ".ready").touch(); '
                   f'exec("while not Path({str(release)!r}).exists(): time.sleep(0.01)")']
        sha = self.adopt(f'[siblings.pin]\nsha = "{pin}"\n', command)
        jobs = [self.root / 'job-one', self.root / 'job-two']
        processes = []
        try:
            (self.repo / '.tmp/gate/cache').mkdir(parents=True)
            for job in jobs:
                self.git('worktree', 'add', '--detach', str(job), sha)
                (job / '.tmp/gate').mkdir(parents=True)
                (job / '.tmp/gate/cache').symlink_to(self.repo / '.tmp/gate/cache')
                processes.append(subprocess.Popen([sys.executable, '-I', str(TOOL), 'run', '--repo', str(job),
                                                   '--sha', sha, '--fresh'], env=self.env,
                                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
            deadline = time.monotonic() + CLI_HANG_GUARD_SECONDS
            while not all((self.root / (job.name + '.ready')).exists() for job in jobs):
                if any(p.poll() is not None for p in processes) or time.monotonic() > deadline:
                    self.fail('both worktree gates did not enter their checks concurrently')
                time.sleep(0.01)
            for job in jobs:
                self.assertTrue((job / '.tmp/gate/cache' / ('pin@' + pin[:12]) / 'pin/data').is_file())
            release.touch()
            for process in processes:
                stdout, stderr = process.communicate(timeout=CLI_HANG_GUARD_SECONDS)
                self.assertEqual(process.returncode, 0, stdout + stderr)
        finally:
            release.touch()
            for process in processes:
                if process.poll() is None:
                    process.terminate()
                process.communicate(timeout=CLI_HANG_GUARD_SECONDS)
