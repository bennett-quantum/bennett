# Children: read [COMMON.md](COMMON.md); rule 15 is the child protocol and rules 1-9 bind you.
Mechanics only: commit with `git -C <worktree> commit -m "<what>" -- <paths>` (message ends `Agent: <model id>`, or
`Co-Authored-By: <name> <noreply@anthropic.com>` for Claude); back up with `git -C <worktree> push --no-verify -q origin
HEAD:refs/heads/wip/<name>`; run `bd` from the repo's main checkout and do not commit .beads/ on your branch.
Pinned siblings: your worktree has its own gate cache. Materialise pins with `python3 -I <tool> verify --repo <worktree> --sha
$(git -C <worktree> rev-parse HEAD)`, where <tool> is `git -C <workspace>/bennett show <tool_sha>:tools/gate_run.py` saved to
<worktree>/.tmp/gate/tool/gate_run-<tool_sha>.py. A brief may name one `git merge <main sha>` into your branch; list conflicts in PROGRESS.
