#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
# --git-path honours core.hooksPath, including Beads' .beads/hooks, and linked worktrees.
hook="$(git rev-parse --git-path hooks/pre-push)"
mkdir -p "$(dirname "$hook")"
staged_hook="$(mktemp "$hook.XXXXXX")"
trap 'rm -f "$staged_hook"' EXIT
cat >"$staged_hook" <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
root="$(git rev-parse --show-toplevel)"
exec "$root/scripts/pre-push" "$@"
HOOK
chmod +x "$staged_hook"
mv -f "$staged_hook" "$hook"
echo "installed pre-push hook: $hook -> scripts/pre-push"
