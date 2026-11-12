#!/usr/bin/env python3
"""Re-point every linked worktree of every checkout in the workspace after the workspace directory moved.

git < 2.48 records absolute worktree paths in both directions (<main>/.git/worktrees/<id>/gitdir and the
worktree's .git file), so moving or renaming the workspace breaks every linked worktree. For each main
checkout directly under --workspace, each registered worktree whose recorded path is missing is located by
the longest suffix of its old path that exists under the new workspace, then `git worktree repair` rewrites
both links. A worktree that cannot be located is reported and the run exits 1; nothing is pruned.
Usage: repair_worktrees.py [--workspace DIR]   (default: the parent of this meta checkout)
"""
import argparse
import os
from pathlib import Path
import subprocess
import sys


def git(cwd, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, env=env,
                          stdin=subprocess.DEVNULL)


def locate(old_gitfile, workspace):
    """New path of the worktree whose .git file used to be old_gitfile, or None."""
    parts = Path(old_gitfile).parent.parts
    for start in range(1, len(parts)):
        candidate = workspace.joinpath(*parts[start:])
        if (candidate / ".git").is_file():
            return candidate
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[2])
    workspace = parser.parse_args().workspace.resolve()
    repaired, lost = 0, []
    for main_checkout in sorted(p for p in workspace.iterdir() if (p / ".git").is_dir()):
        admin_root = main_checkout / ".git" / "worktrees"
        if not admin_root.is_dir():
            continue
        targets = []
        for admin in sorted(admin_root.iterdir()):
            recorded = (admin / "gitdir").read_text().strip()
            if Path(recorded).is_file():
                continue
            found = locate(recorded, workspace)
            if found is None:
                lost.append(f"{main_checkout.name}: {admin.name} (recorded {recorded})")
            else:
                targets.append(str(found))
        if targets:
            result = git(main_checkout, "worktree", "repair", *targets)
            if result.returncode:
                sys.exit(f"git worktree repair failed in {main_checkout}: {result.stderr.strip()}")
            repaired += len(targets)
    print(f"repaired {repaired} worktree link(s) under {workspace}")
    for line in lost:
        print(f"NOT FOUND {line}")
    if lost:
        print("not pruned: locate them by hand, or run `git worktree prune` in the owner once you know they are gone")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
