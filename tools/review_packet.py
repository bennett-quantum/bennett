#!/usr/bin/env python3
"""Freeze a source tree into one markdown document for a council round.

  review_packet.py --root DIR --title T [--commit C] [--first F ...] [--exclude GLOB ...] > packet.md

Every text file under DIR (sorted; --first files first) is embedded verbatim in a fenced
block headed by its path and line count. Binary files and excluded globs are listed, not
embedded. The header records the commit and a sha256 per file, so a later round's diff is
exactly the code diff.
"""
import argparse
import fnmatch
import hashlib
import os
import sys
from pathlib import Path

FENCE = {".rs": "rust", ".py": "python", ".md": "markdown", ".toml": "toml", ".json": "json",
         ".bisa": "", ".comments": "", ".txt": "", ".sh": "bash", ".h": "c", ".c": "c"}
DEFAULT_EXCLUDE = ["target/*", "target", "__pycache__/*", "*.lock", ".git/*"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--commit", default="")
    ap.add_argument("--first", action="append", default=[], help="paths (relative to root) to place first")
    ap.add_argument("--exclude", action="append", default=[], help="globs relative to root, added to the defaults")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    if not root.is_dir():
        sys.exit(f"not a directory: {root}")
    excl = DEFAULT_EXCLUDE + a.exclude
    files = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if any(fnmatch.fnmatch(rel, g) or rel.startswith(g.rstrip("*")) for g in excl):
            continue
        files.append(rel)
    order = [f for f in a.first if f in files] + [f for f in files if f not in a.first]
    missing = [f for f in a.first if f not in files]
    if missing:
        sys.exit(f"--first paths not found: {missing}")
    out = [f"# {a.title}", "",
           f"Snapshot of `{root.name}/` at commit `{a.commit or 'unspecified'}`. "
           f"{len(order)} files; each embedded verbatim below. Line counts and sha256 per file:", ""]
    embedded, total = [], 0
    for rel in order:
        data = (root / rel).read_bytes()
        sha = hashlib.sha256(data).hexdigest()[:12]
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            out.append(f"- `{rel}` binary, {len(data)} bytes, sha256 {sha} (not embedded)")
            continue
        n = text.count("\n") + (0 if text.endswith("\n") or not text else 1)
        total += n
        out.append(f"- `{rel}` {n} lines, sha256 {sha}")
        embedded.append((rel, text, n))
    out += ["", f"Total embedded: {total} lines.", ""]
    for rel, text, n in embedded:
        lang = FENCE.get(Path(rel).suffix, "")
        fence = "`" * (max([len(m) for m in __import__("re").findall(r"`{3,}", text)] + [3]) + 1)
        out += [f"## `{rel}` ({n} lines)", "", f"{fence}{lang}", text.rstrip("\n"), fence, ""]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
