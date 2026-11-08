"""Clone/update integration tests using only local bare Git repositories."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib
import unittest


SOURCE = Path(__file__).resolve().parents[2]
# No meta-wide guard class table yet: use the existing subprocess hang-guard
# mechanism in test_main_health.py (20s Git / 30s CLI), not performance limits.
# Measured suite wall time: 0.63s on tobias-ThinkPad-X1-Carbon-Gen-11,
# 2026-11-08 (machine factor 1); both guards exceed 10x that measurement.
# A guard trip is UNKNOWN and must be investigated separately from assertions.
GIT_HANG_GUARD_SECONDS = 20
SCRIPT_HANG_GUARD_SECONDS = 30


class CloneAllTests(unittest.TestCase):
    def setUp(self):
        tmpdir = SOURCE / ".tmp/meta-clone-remotes/tmp"
        tmpdir.mkdir(parents=True, exist_ok=True)
        scratch = tempfile.TemporaryDirectory(dir=tmpdir)
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.meta = self.root / "meta"
        (self.meta / "scripts").mkdir(parents=True)
        shutil.copy2(SOURCE / "scripts/clone-all.sh", self.meta / "scripts/clone-all.sh")
        self.remotes = self.root / "remotes"
        self.remotes.mkdir()
        self.seed = self.root / "seed"
        self.seed.mkdir()
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith("GIT_") and key not in {
                        "DISPLAY", "WAYLAND_DISPLAY", "DBUS_SESSION_BUS_ADDRESS", "BROWSER"}}
        self.env.update(HOME=str(self.root), TMPDIR=str(tmpdir),
                        GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_ALLOW_PROTOCOL="file", GIT_TERMINAL_PROMPT="0",
                        GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                        GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
                        BENNETT_REMOTE_BASE=str(self.remotes) + "/")
        self.git("init", "-q", "-b", "main", str(self.seed))
        self.git("commit", "--allow-empty", "-qm", "initial")

    def git(self, *args, cwd=None):
        return subprocess.run(["git", "-c", "core.hooksPath=/dev/null", *args],
                              cwd=cwd or self.seed, env=self.env, check=True,
                              capture_output=True, text=True,
                              timeout=GIT_HANG_GUARD_SECONDS).stdout.strip()

    def remote(self, name, directory=None):
        remote = (directory or self.remotes) / f"{name}.git"
        self.git("init", "-q", "--bare", "-b", "main", str(remote))
        self.git("push", "-q", str(remote), "HEAD:refs/heads/main")
        return remote

    def manifest(self, text):
        (self.meta / "manifest.toml").write_text(text)

    def clone_all(self):
        return subprocess.run(["bash", str(self.meta / "scripts/clone-all.sh")],
                              cwd=self.meta, env=self.env, capture_output=True,
                              text=True, timeout=SCRIPT_HANG_GUARD_SECONDS)

    def test_missing_remote_does_not_skip_later_repositories(self):
        self.remote("first")
        self.remote("last")
        self.manifest('[repos.first]\npath = "first"\n'
                      '[repos.missing]\npath = "missing"\n'
                      '[repos.last]\npath = "last"\n')
        result = self.clone_all()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.root / "first/.git").is_dir())
        self.assertTrue((self.root / "last/.git").is_dir(), result.stdout + result.stderr)
        self.assertIn("Summary:", result.stdout)
        self.assertIn("cloned first", result.stdout)
        self.assertIn("cloned last", result.stdout)
        self.assertIn("FAILED missing: fatal:", result.stdout)
        self.assertIn(str(self.remotes / "missing.git"), result.stdout)

    def test_override_and_default_remote_clone_then_update(self):
        self.remote("default")
        personal = self.root / "personal remotes"
        personal.mkdir()
        remote = self.remote("personal", directory=personal)
        self.manifest('[repos.default]\npath = "default"\n'
                      '[repos.personal]\npath = "personal checkout"\n'
                      f'remote = "{remote}"\n')
        first = self.clone_all()
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertEqual(self.git("remote", "get-url", "origin",
                                  cwd=self.root / "personal checkout"), str(remote))
        self.assertIn("cloned default", first.stdout)
        self.assertIn("cloned personal", first.stdout)

        (self.seed / "new-file").write_text("new upstream content\n")
        self.git("add", "new-file")
        self.git("commit", "-qm", "upstream change")
        for target in (self.remotes / "default.git", remote):
            self.git("push", "-q", str(target), "HEAD:refs/heads/main")
        second = self.clone_all()
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        for path, name in (("default", "default"), ("personal checkout", "personal")):
            self.assertEqual((self.root / path / "new-file").read_text(), "new upstream content\n")
            self.assertIn(f"updated {name}", second.stdout)

    def test_info_only_skips_absent_and_existing_repositories(self):
        self.remote("existing")
        self.manifest('[repos.existing]\npath = "existing"\n')
        first = self.clone_all()
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        original_head = self.git("rev-parse", "HEAD", cwd=self.root / "existing")
        # Removing its remote makes an accidental pull observable as a failure.
        shutil.rmtree(self.remotes / "existing.git")
        self.remote("active")
        self.manifest('[repos.absent]\npath = "absent"\ninfo_only = true\n'
                      '[repos.existing]\npath = "existing"\ninfo_only = true\n'
                      '[repos.active]\npath = "active"\ninfo_only = false\n')
        result = self.clone_all()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.root / "absent").exists())
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=self.root / "existing"), original_head)
        self.assertTrue((self.root / "active/.git").is_dir())
        self.assertIn("skipped info-only absent", result.stdout)
        self.assertIn("skipped info-only existing", result.stdout)
        self.assertIn("cloned active", result.stdout)
        self.assertNotIn("FAILED", result.stdout)

    def test_failed_update_does_not_skip_later_clone(self):
        self.remote("stale")
        self.manifest('[repos.stale]\npath = "stale"\n')
        first = self.clone_all()
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        shutil.rmtree(self.remotes / "stale.git")
        self.remote("later")
        self.manifest('[repos.stale]\npath = "stale"\n'
                      '[repos.later]\npath = "later"\n')
        result = self.clone_all()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.root / "later/.git").is_dir(), result.stdout + result.stderr)
        self.assertIn("FAILED stale: fatal:", result.stdout)
        self.assertIn("cloned later", result.stdout)

    def test_manifest_keeps_julia_personal_and_info_only(self):
        with (SOURCE / "manifest.toml").open("rb") as source:
            repo = tomllib.load(source)["repos"]["Bennett.jl"]
        self.assertEqual(repo["remote"], "https://github.com/tobiasosborne/Bennett.jl.git")
        self.assertIs(repo["info_only"], True)
