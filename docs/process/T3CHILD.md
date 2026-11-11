# Protocol for Codex T3 children (R26, maintainer 2026-11-06). Binding with [COMMON.md](COMMON.md); overrides any runner note.
Read [COMMON.md](COMMON.md)'s "Anti-slop rules" section (good/bad examples) before writing code; reviewers check against it.

You run as a T3 delegate child with no sandbox. There is no runner: you commit and back up your own work.
- Write ONLY inside your worktree (named in your brief) and only in your owned paths. Never write a sibling repo's
  working tree or the repo's main checkout, except `bd` (below) and the gate cache it materialises.
- Git: you are on branch job/<name> in your worktree. Commit your own paths regularly, at least every 20 minutes of
  work and at every green checkpoint: `git -C <worktree> add -- <paths>; git -C <worktree> commit -m "<what>" -- <paths>`
  (message ends with `Agent: gpt-6.1-sol`), then `git -C <worktree> push --no-verify -q origin HEAD:refs/heads/wip/<name>`.
  Never commit to or push main; never `git stash`, `reset`, `checkout --`, rebase, force-push anything but wip/<name>,
  never `git add -A` at the repo level. The orchestrator merges job/<name> into main after review. One merge IS allowed when
  your brief names it: `git merge <main sha>` of the repo's main INTO your job branch to resolve conflicts, as a plain merge
  commit with every conflicted file listed in PROGRESS.md; the shared lines get the review at landing (COMMON rule 3).
  (Bent twice on 2026-11-09 before it was written down; now it is the rule.)
- Beads: run `bd` from the repo's MAIN checkout (`cd <repo main checkout> && bd ...`), for findings and closures
  (`bd close <id> --reason "<what, verified by which command>"`). Do NOT commit .beads/issues.jsonl on your branch; the
  orchestrator exports beads at merge. Cross-repo bead requests: .tmp/<name>/cross-repo-beads.md in your worktree.
- Pinned siblings: tests read siblings only through the repo's gate.toml pin. Your worktree has its own gate cache
  (<worktree>/.tmp/gate/cache, a real directory; a legacy symlink there is refused). To materialise or build a pin, run
  the gate tool against your worktree: `python3 -I <worktree>/.tmp/gate/tool/gate_run-<tool_sha>.py verify --repo <worktree>
  --sha $(git -C <worktree> rev-parse HEAD)` (commit gate.toml first; scripts/pre-push extracts the tool on first use).
  Never run a repo's full push gate or `gate_run.py run` (the orchestrator does that at merge).
- Progress: keep .tmp/<name>/PROGRESS.md in your worktree current as a Resume block (done / verified with which command /
  next). If you are stopped at any moment, a successor continues from it plus the git log.
- Headless: DISPLAY, WAYLAND_DISPLAY, DBUS_SESSION_BUS_ADDRESS, BROWSER unset; TMPDIR=<worktree>/.tmp/<name>/tmp;
  CARGO_TARGET_DIR=<worktree>/.tmp/<name>/target. Parallel width comes from the repo's machine profile (beside its
  hang-guard class table; until a repo has one, nproc and MemAvailable with headroom for the other jobs), never a number
  from a brief; long runs are bounded by the class table, never a bare `timeout N`.
- SCOPE IS THE BRIEF, NOTHING MORE (maintainer 2026-11-09). You work only the task your brief states. When it is done, write the
  final message and STOP. Never pull the next bead, start a follow-on, fix an adjacent finding, widen your owned paths, or
  launch anything. Anything you notice beyond the brief becomes a bead (`bd create`, from the main checkout) or a line in
  PROGRESS.md for the orchestrator, who alone decides what is worked next. A child that keeps taking work is spending quota the
  orchestrator is pacing; that is a defect in the child, not initiative.
- BLOCKED BY A RULE? If two instructions you were given (brief, COMMON.md, T3CHILD.md, CLAUDE.md) forbid each other for the
  work in your brief, do not pick one silently: write JOB-BLOCKED naming both lines verbatim and stop. The orchestrator records it
  as BLOCKED-BY-RULE (COMMON.md, Rule conflict repair) and the advisor resolves it. (maintainer 2026-11-09)
- Do not ask questions; no human is watching. End with a final message (<=200 words, COMMON 13) whose last line is
  `JOB-COMPLETE` or `JOB-BLOCKED: <reason>`.
