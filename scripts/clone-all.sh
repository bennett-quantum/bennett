#!/usr/bin/env bash
# Clone or update every repo listed in manifest.toml. Safe to re-run.
set -euo pipefail
: "${BENNETT_REMOTE_BASE:?set BENNETT_REMOTE_BASE, e.g. git@host:org}"
here="$(cd "$(dirname "$0")/.." && pwd)"
parent="$(dirname "$here")"
names=$(python3 - "$here/manifest.toml" "$BENNETT_REMOTE_BASE" <<'PY'
import sys
import tomllib

with open(sys.argv[1], "rb") as source:
    repos = tomllib.load(source)["repos"]
for name, repo in repos.items():
    remote = repo.get("remote", f"{sys.argv[2].rstrip('/')}/{name}.git")
    print(name, repo["path"], remote, str(repo.get("info_only", False)).lower(), sep="\t")
PY
)
summary=()
failed=0
while IFS=$'\t' read -r name path remote info_only; do
  if [[ "$info_only" == true ]]; then
    summary+=("skipped info-only $name")
    continue
  fi
  dest="$parent/$path"
  if [ -e "$dest/.git" ]; then
    echo "update $name"
    action=updated
    command=(git -C "$dest" pull --ff-only)
  else
    echo "clone  $name"
    action=cloned
    command=(git clone "$remote" "$dest")
  fi
  if output=$(LC_ALL=C "${command[@]}" 2>&1); then
    printf '%s\n' "$output"
    summary+=("$action $name")
  else
    printf '%s\n' "$output" >&2
    error_line="${output%%$'\n'*}"
    while IFS= read -r line; do
      case "$line" in
        fatal:*|error:*) error_line="$line"; break ;;
      esac
    done <<< "$output"
    summary+=("FAILED $name: $error_line")
    failed=1
  fi
done <<< "$names"
printf '\nSummary:\n'
printf '  %s\n' "${summary[@]}"
exit "$failed"
