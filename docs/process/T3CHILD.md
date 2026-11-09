# Protocol for Codex T3 children (R26, maintainer 2026-11-06). Binding with [COMMON.md](COMMON.md); overrides any runner note.
Read [COMMON.md](COMMON.md)'s "Anti-slop rules" section (good/bad examples) before writing code; reviewers check against it.

You run as a T3 delegate child with no sandbox. There is no runner: you commit and back up your own work.
- Write ONLY inside your worktree (named in your brief) and only in your owned paths. Never write a sibling repo's
  working tree or the repo's main checkout, except `bd` (below) and the gate cache it materialises.
- Git: you are on branch job/<name> in your worktree. Commit your own paths regularly, at least every 20 minutes of
  work and at every green checkpoint: `git -C <worktree> add -- <paths>; git -C <worktree> commit -m "<what>" -- <paths>`
  (message ends with `Agent: gpt-6.1-sol`), then `git -C <worktree> push --no-verify -q origin HEAD:refs/heads/wip/<name>`.
  Never commit to or push main; never `git stash`, `reset`, `checkout --`, rebase, force-push anything but wip/<name>,
  never `git add -A` at the repo level. The orchestrator merges job/<name> into main after review.
- Beads: run `bd` from the repo's MAIN checkout (`cd <repo main checkout> && bd ...`), for findings and closures
  (`bd close <id> --reason "<what, verified by which command>"`). Do NOT commit .beads/issues.jsonl on your branch; the
  orchestrator exports beads at merge. Cross-repo bead requests: .tmp/<name>/cross-repo-beads.md in your worktree.
- Pinned siblings: tests read siblings only through the repo's gate.toml pin. The worktree's .tmp/gate/cache is a
  symlink to the main checkout's cache. To materialise or build a pin you need, run the gate tool against the MAIN
  checkout with your branch head: `python3 <main>/.tmp/gate/tool/gate_run-<tool_sha>.py verify --repo <main checkout>
  --sha $(git -C <worktree> rev-parse HEAD)` (commit gate.toml first; the tool lives in any repo's .tmp/gate/tool/,
  e.g. /home/tobias/Projects/bennett-workspace/bennett-driver/.tmp/gate/tool/gate_run-01c0314c9aaa4a37313ab530da2134efafe9cbd5.py).
  Do not run --repo <worktree>: bwrap cannot follow the symlink. Never run a repo's full push gate or `gate_run.py run`
  (the orchestrator does that at merge).
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
- Do not ask questions; no human is watching. End with a final message (<=200 words, COMMON 13) whose last line is
  `JOB-COMPLETE` or `JOB-BLOCKED: <reason>`.
