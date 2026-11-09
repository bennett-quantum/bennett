"""Host provisioning tests use fake installations, never the caller's toolchains."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[2]


class DoctorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.calls = self.root / "calls"
        self.env = dict(os.environ, PATH=str(self.bin), HOME=str(self.root),
                        PROVISION_CALLS=str(self.calls), TMPDIR=str(self.root))
        for key in ("DISPLAY", "WAYLAND_DISPLAY", "DBUS_SESSION_BUS_ADDRESS", "BROWSER"):
            self.env[key] = "must-be-unset"
        (self.bin / "python3").symlink_to(sys.executable)
        for name in ("git", "bwrap", "bd", "dolt", "bash", "systemd-run"):
            self.tool(self.bin / name, name + " 1.0")
        self.manifest = self.root / "manifest.toml"
        self.manifest.write_text('[repos.bennett-alpha]\npath="bennett-alpha"\n')
        self.repo = self.root / "bennett-alpha"
        self.repo.mkdir()
        self.gate = self.repo / "gate.toml"
        self.config()
        self.llvm = self.root / "llvm18/bin"
        for name in ("opt", "llc", "clang", "clang++", "llvm-config"):
            self.tool(self.llvm / name, "LLVM version 18.1.3")
        cmake = self.llvm.parent / "lib/cmake/llvm/LLVMConfig.cmake"
        cmake.parent.mkdir(parents=True)
        cmake.write_text("# fixture LLVM development package\n")
        self.tool(self.bin / "cmake", "cmake version 3.28.3")
        self.toolchains = self.root / "bennett-dialect-spec/corpus/legality/toolchains.toml"
        self.toolchains.parent.mkdir(parents=True)
        self.toolchains.write_text(f'[llvm18]\nbin="{self.llvm}"\nfrontend_bin="{self.llvm}"\n')

    def tool(self, path, version, status=0):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'#!{sys.executable}\nimport os, pathlib, sys\n'
                        'assert all(k not in os.environ for k in '
                        '("DISPLAY", "WAYLAND_DISPLAY", "DBUS_SESSION_BUS_ADDRESS", "BROWSER"))\n'
                        'with pathlib.Path(os.environ["PROVISION_CALLS"]).open("a") as f:\n'
                        '    f.write(repr(sys.argv) + "\\n")\n'
                        f'print({version!r})\nraise SystemExit({status})\n')
        path.chmod(0o755)

    def config(self, command='["python3", "--version"]', extra=""):
        self.gate.write_text('schema=1\nrepo="bennett-alpha"\ntool_sha="' + "a" * 40 +
                             '"\n' + extra + '\n[[check]]\nname="fixture"\nargv=' + command + '\n')

    def run_script(self, script="doctor.sh", *args):
        return subprocess.run(["/bin/bash", str(SOURCE / "scripts" / script),
                               "--workspace", str(self.root), "--manifest", str(self.manifest), *args],
                              env=self.env, capture_output=True, text=True)

    def report(self):
        result = self.run_script("doctor.sh", "--json")
        return result, json.loads(result.stdout)

    def test_complete_inventory_reports_versions(self):
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("18.1.3", result.stdout)
        self.assertIn("bennett-alpha/gate.toml", result.stdout)
        self.assertIn("PASS", result.stdout)

    def test_missing_tools_are_consolidated_and_have_install_steps(self):
        (self.bin / "bwrap").unlink()
        (self.llvm / "llc").unlink()
        result, report = self.report()
        self.assertEqual(result.returncode, 1, result.stderr)
        labels = "\n".join(gap["label"] for gap in report["gaps"])
        self.assertIn("bwrap", labels)
        self.assertIn("llc", labels)
        self.assertTrue(all("install" in gap for gap in report["gaps"]))

    def test_llvm_major_mismatch_is_a_gap(self):
        self.tool(self.llvm / "opt", "LLVM version 19.1.0")
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("expected LLVM 18", result.stdout)

    def test_failed_version_probe_is_a_gap(self):
        self.tool(self.bin / "bd", "database broken", status=9)
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("database broken", result.stdout)

    def test_unknown_gate_and_nested_keys_fail_loud(self):
        mutations = ['mystery=true\n', '[siblings.other]\nsha="' + "b" * 40 + '"\nmystery=true\n']
        for extra in mutations:
            with self.subTest(extra=extra):
                self.config(extra=extra)
                result = self.run_script()
                self.assertEqual(result.returncode, 1)
                self.assertIn("unknown key", result.stdout)
                self.assertIn("mystery", result.stdout)

    def test_unknown_command_key_and_bad_argv_fail_loud(self):
        for suffix in ('surprise=true\n', 'cwd=17\n'):
            self.config()
            with self.gate.open("a") as f:
                f.write(suffix)
            result = self.run_script()
            self.assertEqual(result.returncode, 1)
            self.assertIn("fixture", result.stdout)
        self.config(command='[]')
        self.assertEqual(self.run_script().returncode, 1)

    def test_unknown_toolchain_key_and_section_fail_loud(self):
        for text in ('[llvm18]\nbin="/absent"\nextra=true\n', '[cuda]\nbin="/absent"\n'):
            self.toolchains.write_text(text)
            result = self.run_script()
            self.assertEqual(result.returncode, 1)
            self.assertIn("unknown", result.stdout)

    def test_missing_repo_and_malformed_toml_both_reported(self):
        with self.manifest.open("a") as f:
            f.write('[repos.bennett-missing]\npath="bennett-missing"\n')
        self.gate.write_text('bad TOML [\n')
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("bennett-missing", result.stdout)
        self.assertIn("bennett-alpha", result.stdout)

    def test_ignores_job_worktrees_and_info_only_repos(self):
        job = self.root / "bennett-alpha-job-other"
        job.mkdir()
        (job / "gate.toml").write_text("invalid")
        with self.manifest.open("a") as f:
            f.write('[repos.optional]\npath="absent"\ninfo_only=true\n')
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_new_manifest_command_is_checked_without_editing_doctor(self):
        self.config(command='["new-compiler", "--flag"]')
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("new-compiler", result.stdout)
        self.tool(self.bin / "new-compiler", "compiler 7.2")
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("7.2", result.stdout)

    def test_shell_commands_are_parsed_never_executed(self):
        marker = self.root / "must-not-exist"
        command = ["sh", "-c", f"touch {marker}; mystery-cc --input fake; cargo test --offline"]
        self.config(command=json.dumps(command))
        self.tool(self.bin / "sh", "POSIX shell")
        result = self.run_script()
        self.assertFalse(marker.exists())
        self.assertEqual(result.returncode, 1)
        for name in ("mystery-cc", "cargo", "rustc"):
            self.assertIn(name, result.stdout)

    def test_local_source_path_checked_without_running_it(self):
        self.config(command='["scripts/check"]')
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("scripts/check", result.stdout)
        path = self.repo / "scripts/check"
        path.parent.mkdir()
        path.write_text("#!/bin/bash\nexit 37\n")
        path.chmod(0o755)
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_cargo_subcommands_require_rust_components(self):
        self.config(command='["cargo", "clippy", "--offline"]')
        self.tool(self.bin / "cargo", "cargo 1.99.1")
        self.tool(self.bin / "rustc", "rustc 1.99.1")
        self.tool(self.bin / "cargo-clippy", "clippy 0.1.99")
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        (self.bin / "cargo-clippy").unlink()
        self.assertEqual(self.run_script().returncode, 1)

    def test_bootstrap_default_is_dry_run_even_when_root(self):
        (self.bin / "bwrap").unlink()
        self.tool(self.bin / "sudo", "sudo called")
        self.tool(self.bin / "apt-get", "apt called")
        result = self.run_script("bootstrap-host.sh")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("sudo apt-get install -y bubblewrap", result.stdout)
        self.assertNotIn("'sudo'", self.calls.read_text())
        self.assertNotIn("'apt-get'", self.calls.read_text())

    def test_bootstrap_green_host_is_noop(self):
        result = self.run_script("bootstrap-host.sh", "--sudo")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_bootstrap_installs_then_rechecks_and_is_idempotent(self):
        (self.bin / "bwrap").unlink()
        saved = self.root / "saved-bwrap"
        self.tool(saved, "bwrap 0.9.0")
        sudo = self.bin / "sudo"
        sudo.write_text(f'#!{sys.executable}\nimport os, pathlib, shutil, sys\n'
                        f'shutil.copy2({str(saved)!r}, {str(self.bin / "bwrap")!r})\n')
        sudo.chmod(0o755)
        first = self.run_script("bootstrap-host.sh", "--sudo")
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertIn("PASS", first.stdout)
        sudo.unlink()
        second = self.run_script("bootstrap-host.sh", "--sudo")
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)

    def test_bootstrap_cannot_claim_success_when_install_did_not_fix_gap(self):
        (self.bin / "bwrap").unlink()
        self.tool(self.bin / "sudo", "pretending to install")
        result = self.run_script("bootstrap-host.sh", "--sudo")
        self.assertEqual(result.returncode, 1)
        self.assertIn("bwrap", result.stdout)

    def test_bootstrap_does_not_install_for_unknown_schema(self):
        self.config(extra='unknown=true\n')
        self.tool(self.bin / "sudo", "must not run")
        result = self.run_script("bootstrap-host.sh", "--sudo")
        self.assertEqual(result.returncode, 1)
        self.assertIn("unknown", result.stdout)
        self.assertNotIn("'sudo'", self.calls.read_text())
