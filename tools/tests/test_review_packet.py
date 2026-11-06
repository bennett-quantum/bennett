"""Review packet ordering, exclusion boundaries, binary files and content fences."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "review_packet.py"


class ReviewPacketTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def write(self, name, data=b"fixture\n"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def packet(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root),
                               "--title", "Review", *args], capture_output=True, text=True, timeout=5)

    def test_exclude_globs_and_directory_boundaries(self):
        for name in ("target/bin", "target_notes.md", "keep.py", "a.log", "nested/b.log",
                     "secret/token", "secretary.py", "nested/__pycache__/x.pyc"):
            self.write(name)
        result = self.packet("--exclude", "*.log", "--exclude", "secret")
        self.assertEqual(result.returncode, 0, result.stderr)
        for present in ("target_notes.md", "keep.py", "secretary.py"):
            self.assertIn(f"## `{present}`", result.stdout)
        for absent in ("target/bin", "a.log", "nested/b.log", "secret/token", "nested/__pycache__/x.pyc"):
            self.assertNotIn(f"`{absent}`", result.stdout)

    def test_first_order_binary_hash_and_fenced_text(self):
        self.write("a.py", b"print('a')\n")
        self.write("z.md", b"inside ```` fence\n")
        self.write("image.bin", b"\xff\x00")
        result = self.packet("--first", "z.md", "--commit", "fixture-sha")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLess(result.stdout.index("## `z.md`"), result.stdout.index("## `a.py`"))
        self.assertIn("`````markdown", result.stdout)
        self.assertIn("image.bin` binary, 2 bytes, sha256", result.stdout)
        self.assertNotIn("## `image.bin`", result.stdout)
        self.assertIn("fixture-sha", result.stdout)

    def test_missing_or_excluded_first_file_fails(self):
        self.write("hidden.log")
        for name in ("missing", "hidden.log"):
            result = self.packet("--exclude", "*.log", "--first", name)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--first paths not found", result.stderr)
