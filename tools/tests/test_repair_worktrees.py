"""repair_worktrees.py re-points linked worktrees after the workspace directory moves (scratch repos only)."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[1] / "repair_worktrees.py"
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
GIT_ENV.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.invalid",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.invalid")


def git(cwd, *args, check=True):
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True,
                          env=GIT_ENV, check=check, timeout=60)


class RepairWorktreesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(dir=os.environ.get("TMPDIR")))
        self.old = self.tmp / "old" / "bennett-workspace"
        self.old.mkdir(parents=True)
        self.repo = self.old / "bennett-x"
        git(self.old, "init", "-q", "-b", "main", str(self.repo))
        (self.repo / "f").write_text("1\n")
        git(self.repo, "add", "f")
        git(self.repo, "commit", "-q", "-m", "c")
        git(self.repo, "worktree", "add", "-q", "-b", "job/a", str(self.old / "bennett-x-job-a"))
        nested = self.old / "bennett-x-job-a" / ".tmp" / "cache" / "bennett-x@abc"
        git(self.repo, "worktree", "add", "-q", "--detach", str(nested), "main")
        self.new = self.tmp / "new" / "bennett-workspace"
        self.new.parent.mkdir()
        os.rename(self.old, self.new)

    def tool(self, *args):
        return subprocess.run([sys.executable, "-I", str(TOOL), *args], capture_output=True, text=True,
                              env=GIT_ENV, timeout=120)

    def test_moved_workspace_is_broken_then_repaired(self):
        job = self.new / "bennett-x-job-a"
        self.assertNotEqual(git(job, "rev-parse", "HEAD", check=False).returncode, 0)
        result = self.tool("--workspace", str(self.new))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(git(job, "branch", "--show-current").stdout.strip(), "job/a")
        nested = job / ".tmp" / "cache" / "bennett-x@abc"
        self.assertEqual(git(nested, "rev-parse", "HEAD").returncode, 0)
        admin = (self.new / "bennett-x/.git/worktrees/bennett-x-job-a/gitdir").read_text().strip()
        self.assertEqual(admin, str(job / ".git"))
        self.assertIn("repaired 2", result.stdout)

    def test_unfindable_worktree_is_reported_not_pruned(self):
        os.rename(self.new / "bennett-x-job-a", self.tmp / "elsewhere")
        result = self.tool("--workspace", str(self.new))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("bennett-x-job-a", result.stdout + result.stderr)
        self.assertTrue((self.new / "bennett-x/.git/worktrees/bennett-x-job-a").is_dir())

    def test_second_run_is_a_no_op(self):
        self.assertEqual(self.tool("--workspace", str(self.new)).returncode, 0)
        again = self.tool("--workspace", str(self.new))
        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
        self.assertIn("repaired 0", again.stdout)


if __name__ == "__main__":
    unittest.main()
