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


TOOL = Path(__file__).resolve().parents[1] / "gate_run.py"
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


class ContentReceiptTests(RunnerFixture):
    def setUp(self):
        super().setUp()
        self.env["BENNETT_GATE_WORKSPACE"] = str(self.root)
        (self.repo / ".gitignore").write_text(".tmp/\n")
        (self.repo / ".tmp").mkdir()
        self.marker = self.repo / ".tmp/executed"

    def config(self, fail_once=False):
        command = ("from pathlib import Path; "
                   f"p = Path({str(self.marker)!r}); "
                   "p.open('a').write('run\\n'); "
                   f"raise SystemExit({fail_once!r} and len(p.read_text().splitlines()) == 1)")
        (self.repo / "gate.toml").write_text(
            'schema = 1\nrepo = "repo"\ntool_sha = "' + "1" * 40 + '"\n'
            '\n[[check]]\nname = "marker"\n' +
            f'argv = {json.dumps([sys.executable, "-c", command])}\n')
        self.git("add", ".")
        self.git("commit", "-qm", "gate fixture")
        return self.git("rev-parse", "HEAD").strip()

    def run_gate(self, sha, *options, repo=None, isolated=False):
        return subprocess.run(
            [sys.executable, "-I", str(TOOL), "run", "--repo", str(repo or self.repo),
             "--sha", sha, *([] if isolated else ["--no-isolate"]), *options],
            env=self.env, capture_output=True, text=True, timeout=CLI_HANG_GUARD_SECONDS)

    def receipt_path(self, sha, isolated=False):
        tree = self.git("rev-parse", f"{sha}^{{tree}}").strip()
        key = hashlib.sha256(json.dumps([tree, "1" * 40, isolated], sort_keys=True).encode()).hexdigest()
        return self.repo / ".tmp/gate/receipts" / f"{key}.json"

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
        # Zero represents an already-expired guard; the child waits for a signal,
        # not a timed sleep. The outer CLI guard bounds a broken cleanup path.
        sha = self.config([[sys.executable, "-c", "import signal; signal.pause()"]],
                          extra="timeout_s = 0\n")
        result = self.run_gate(sha)
        self.assertEqual(result.returncode, 1, result.stderr)
        command = self.receipt(sha)["checks"][0]
        self.assertEqual(command["exit"], 124)
        self.assertGreater(command["cpu_seconds"], 0)
        self.assertGreater(command["peak_rss_kib"], 0)

    def test_existing_lock_error_names_holder(self):
        tool = load_tool()
        path = self.workspace / "lock"
        with tool.Lock(path, blocking=False):
            with self.assertRaisesRegex(tool.GateError, rf"pid={os.getpid()}.*started_utc=\S+"):
                with tool.Lock(path, blocking=False):
                    self.fail("existing flock unexpectedly admitted another holder")
