"""Gate receipts from tiny local repositories; no ecosystem gate is run."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest


TOOL = Path(__file__).resolve().parents[1] / "gate_run.py"
# Meta has no guard table yet. Follow test_clone_all.py / test_main_health.py:
# Git 20s, CLI 30s, machine factor 1 on the shared 12-core / 30 GiB host.
# These are hang guards, never performance assertions; a trip is UNKNOWN.
# Whole fixture suite measured 1.78s here on 2026-11-08; both exceed 10x.
GIT_HANG_GUARD_SECONDS = 20
CLI_HANG_GUARD_SECONDS = 30
# Synthetic clock advance, not a delay or a performance limit.
SETUP_CLOCK_OFFSET_SECONDS = 1000


def load_tool():
    spec = importlib.util.spec_from_file_location("gate_receipt_fixture", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
        self.repo.mkdir()
        self.git(self.repo, "init", "-qb", "main")

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

    def run_gate(self, sha, bootstrap=None, extra_env=None):
        invocation = ([sys.executable, "-I", "-c", bootstrap, str(TOOL)] if bootstrap
                      else [sys.executable, "-I", str(TOOL)])
        return subprocess.run([*invocation, "run", "--repo", str(self.repo), "--sha", sha,
                               "--no-isolate"], env=dict(self.env, **(extra_env or {})),
                              capture_output=True, text=True, timeout=CLI_HANG_GUARD_SECONDS)

    def receipt(self, sha):
        return json.loads((self.repo / ".tmp/gate/records" / f"{sha}.json").read_text())

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
        result = self.run_gate(sha)
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
                self.assertGreaterEqual(receipt["checks"][0]["cpu_seconds"], 0)

    def test_existing_lock_error_names_holder(self):
        tool = load_tool()
        path = self.workspace / "lock"
        with tool.Lock(path, blocking=False):
            with self.assertRaisesRegex(tool.GateError, rf"pid={os.getpid()}.*started_utc=\S+"):
                with tool.Lock(path, blocking=False):
                    self.fail("existing flock unexpectedly admitted another holder")
