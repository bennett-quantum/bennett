#!/usr/bin/env bash
# Create the public GitHub remotes for every repo in manifest.toml under the
# bennett-quantum organisation and push main. Idempotent: repos that already
# have an `origin` are only pushed. Requires: gh (logged in, repo scope), the
# organisation already created on github.com (web UI only; no API exists).
set -euo pipefail
ORG="${BENNETT_ORG:-bennett-quantum}"
WS="$(cd "$(dirname "$0")/../.." && pwd)"
MANIFEST="$WS/bennett/manifest.toml"
gh api "orgs/$ORG" >/dev/null 2>&1 || { echo "organisation $ORG does not exist on github.com; create it at https://github.com/organizations/plan"; exit 2; }
repos=$(python3 - "$MANIFEST" <<'PY'
import sys, tomllib
m = tomllib.load(open(sys.argv[1], "rb"))
print("\n".join(sorted(m["repos"])))
PY
)
# the meta repo itself is in the manifest under its own name if listed; add it explicitly
repos=$(printf "%s\nbennett\n" "$repos" | sort -u)
for r in $repos; do
  d="$WS/$r"
  [ -d "$d/.git" ] || { echo "skip $r: no local repo at $d"; continue; }
  if git -C "$d" remote get-url origin >/dev/null 2>&1; then
    echo "== $r: origin exists; pushing"
    git -C "$d" push -u origin main
  else
    echo "== $r: creating $ORG/$r (public) and pushing"
    gh repo create "$ORG/$r" --public --source "$d" --remote origin --push \
      --description "$(head -c 200 "$d/README.md" | sed -n '3p' | cut -c1-120 || echo "Bennett: $r")"
  fi
  if [ -x "$d/scripts/install-hooks.sh" ]; then (cd "$d" && ./scripts/install-hooks.sh >/dev/null 2>&1 && echo "   hooks installed") || true; fi
done
echo "done: $(echo "$repos" | wc -l) repos under https://github.com/$ORG"
