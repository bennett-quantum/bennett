#!/usr/bin/env bash
# Clone or update every repo listed in manifest.toml. Safe to re-run.
set -euo pipefail
: "${BENNETT_REMOTE_BASE:?set BENNETT_REMOTE_BASE, e.g. git@host:org}"
here="$(cd "$(dirname "$0")/.." && pwd)"
parent="$(dirname "$here")"
names=$(python3 -c 'import tomllib,sys;[print(k,v["path"]) for k,v in tomllib.load(open(sys.argv[1],"rb"))["repos"].items()]' "$here/manifest.toml")
while read -r name path; do
  dest="$parent/$path"
  if [ -d "$dest/.git" ]; then
    echo "update $name"; git -C "$dest" pull --ff-only
  else
    echo "clone  $name"; git clone "${BENNETT_REMOTE_BASE%/}/$name.git" "$dest"
  fi
done <<< "$names"
