# Worklog chunk 002

## Session log - 2026-11-02 - orchestration shifts 1-3: runner death, push backlog, network outage, pinned-sibling gate, Muse policy

Orchestrators (Opus) ran the work in shifts via `.tmp/orchestrator/shift-N.md`; the advisor (Fable) ruled between them
(`.tmp/orchestrator/advisor-notes.md`). Children: Codex sol xhigh runners (`tools/codex_job.py`), Opus and Sonnet delegates.
Timestamps below are UTC; runner.log and git commit dates print local time (UTC+1), so a runner's "01:45" is 00:45Z.

- Shift 1 (2026-11-01 21:05Z to 23:35Z limit). Eleven sol runners and Opus delegates produced: bennett-targets ISA 0.9
  section 8 (5113d9a), the conformance checker, harness and rung-4 gate, dialect 0.3 draft (e7168bb e12a6f3), arith
  circuits/QROM (aab308f pushed), reference-interpreter named-interface K82 (isa-spec 03a7584), and VM review beads
  (db0ec49). K82 was ACCEPTED in council round 10 (run `isa-09-k82-2026-11-01`, sol + codex accept, 0 blocking, mean 4.75;
  75ba4d9); the Muse advisory vote stayed pending. The advisor retired shift 1 at 05:35Z: it had declared handoff at
  23:35Z but kept running 37 reactive turns on child wakeups.
- Root cause, runners dead for ~5 h: every `codex_job.py run` process died at ~00:45Z (last checkpoints 00:37-00:45Z; runner.log
  printed 01:37-01:45 local) while `status.json` still said `running` (sol-estimate, sol-plugin-queue, sol-sched, sol-vm-queue). Presumed
  cause: they were started from the orchestrator's shell and died with its turn/sandbox. Rule since: launch detached
  (`setsid nohup python3 .../codex_job.py run ... > <state>/launch.log 2>&1 < /dev/null &`), verify with `pgrep -af
  codex_job`, resume with `--thread <id from status.json>` (`.tmp/orchestrator/resume_job.py NAME`).
- Runner bug fixed (d500277, 2026-11-01 22:36Z): `git add` of owned paths in one command failed when any path was missing or
  ignored, so plugin, sched, circuits and the checker lost every checkpoint; paths are now staged one by one. Stranded
  work was committed by hand (plugin db2e9e7, sched 0428570, circuits 0a963c6).
- Shift 2 (05:34Z): relaunched the runners and Opus delegates, filed beads from the children's
  cross-repo notes (ledger `.tmp/orchestrator/filed-cross-repo.md`, sonnet-beadclerk, 05:43Z), and pushed the two mains
  whose gates passed: bennett-conformance b077ae2 (05:43Z) and bennett-targets 4a74c62. targets needed the advisor ruling
  that a repo gate exits 0 when the repo's own checks pass and reports milestone blockers instead of encoding them in the
  exit code (its `verify.py` exited 2 unconditionally; see that repo's worklog).
- Muse policy (maintainer, via advisor). Muse quota is small; three concurrent Muse streams burned ~5 weekly points per
  17 min on 11-01 and all hit HTTP 429 by 22:00Z. 05:47Z: no more Muse; 05:53Z refinement: Muse only as a council seat
  (acceptance votes, new contracts), after a `quota` reading, a written cost plan in the shift file and advisor
  confirmation per use; no Muse implementation or review streams. The three Muse streams (checker-replay, design-reviews,
  dialect K82) were cancelled and their work moved to Opus/sol (`opus-checker-replay`, `opus-design-reviews`,
  `sol-dialect-s0`). Council ruling of 2026-10-31 (a new contract publishes only with the Muse vote) now needs a
  substitute or waiver before dialect 0.3 publishes; open question, not urgent while 0.3 waits on b-isa-spec-fuk.7. The K82
  Muse call was approved at 06:14Z but could not finish before the outage; re-approved 07:55Z and launched at 07:58Z
  (`tools/council.py run ... --member muse`, log `.tmp/k82-muse/run.log`; `muse` added to `member_list` in the run's
  `state.json`, since `council.py collect` refuses non-members). Result not in at the time of writing.
- Network outage ~06:21Z-07:36Z. Before it (advisor notice 06:14Z) backups were pushed gate-free to `wip/pre-outage-2026-11-02`
  in all 13 repos ahead of origin (plus -bjm, -vmfixes, -rung4 for the worktrees). Found afterwards (07:55Z): all 12 sol
  runners survived (sol-contract and sol-dialect-s0 finished exit 0: 13 contract notes under
  `bennett-isa-spec/docs/notes/2026-11-02-contract-*.md` and the dialect 0.3 S0 read with P0 beads b-dialect-spec-d4s, fa8);
  every Opus/Sonnet delegate had died and was relaunched from its progress file. A `tick.sh 1800` printed at 07:52Z
  although started at 06:09Z, so the machine or session paused too.
- Systemic cause of the push backlog (plugin 46, isa-spec 20, conformance 14, runtimes 14, estimate 13, targets 13 commits ahead at
  05:33Z, no off-machine copy): gates read live sibling working trees, so they went red whenever a sibling job was mid-edit
  (plugin vs runtimes dist, dialect vs the ISA interpreter, runtimes vs a rebuilt arith dist at 06:17Z), and green said nothing
  about which sibling they held for. Fix: `tools/gate_run.py` (c698ce1, selftest 46 OK as reported by opus-gate-template,
  not re-run by me), design in `tools/gate_README.md` (cd9ed73): each repo's `gate.toml` pins its siblings; the tool is
  fetched by a `scripts/pre-push` stub from meta-repo objects at `tool_sha`; the check runs under bwrap on a clean worktree
  of the pushed sha with the pinned siblings beside it and every other top-level workspace directory an empty tmpfs, so an
  unpinned or absolute read of a live sibling is ENOENT and the check goes red; exit 0 iff every check passed, milestone
  reports never decide. Adopted (stub + gate.toml) in dialect, targets, circuits, vm, arith, conformance, runtimes;
  `gate.toml` only in plugin and isa-spec until their in-flight pushes end. Gate results by opus-gate-template: targets
  c788cba PASS, circuits 0ac4973 PASS, dialect d575756 FAIL 2884/2902 (the checker's 120 s interpreter build timed out on a
  cold cache, b-dialect-spec-abf), runtimes ae7854f FAIL by `native-check-link` TimeoutExpired under load ~24, vm 7a27fc8
  FAIL (the pin lacked the conformance-harness build, fixed a319423). Left as beads: bennett-sched-68k, bennett-estimate-m6p,
  bennett-driver-3j4 (their tests pin old hook internals).
- Push wave (sonnet-pushwave, see `.tmp/orchestrator/sonnet-pushwave-PROGRESS.md`): runtimes gate RED three times (a test
  reading `ROOT.parent/bennett-arith` under a `.tmp` gate worktree; a 180 s host timeout in `test_sqlite_memdb` at load ~37; a
  SQLite 5ur draft mid-TDD faulting with SIGILL while the live arith dist was rebuilt); main unpushed. isa-spec ecaaac0 and
  plugin 2aba17a gates have run since 05:39Z / 05:51Z (isa-spec over the 7200 s ceiling but progressing in `ref_qinplace` tests).
- Shift 3 (07:57Z) rulings (advisor, 07:55Z, binding): R1 where the 0.8 text is silent the reference interpreter is the oracle,
  so the VM branch must not gate behaviour the text does not specify (draw ties); file a text-defect bead (b-isa-spec-0h4,
  isa-spec 9165f3e) and route it with fd0 to a sol derivation and council round. R2 the §6.2 arith scratch-object rejection is
  reference-consistent (the reference rejects 3 of 4 checked), not a narrowing: bead in bennett-arith, recheck `and_use`.
  R3 heavy gates: at most one full-width plugin CC gate or VM dual-engine run at a time; read `free -g` and `uptime` first;
  7200 s is the ceiling, and a gate past it is checked for progress and killed if stuck; children run no gates unless
  their brief says so. R4 the possible north-star gap l2p (ISA §6.2 refuses the 4-T AND) is read by an Opus stream and
  reported to the advisor before any council round. R5 Claude is behind pace (7.9%): raise Opus/Sonnet streams to 6-8 and
  refill Codex slots with sol derivation work. Host at 07:52Z: load 26 on 12 cores, 7 GB available of 30, swap full;
  07:57Z the orchestrator killed an orphaned vm gate_run (test at 5.4 GB) that collided with the plugin push gate.
- Council policy for new rounds (advisor 06:14Z): routine rounds sol + astra; Muse at most once per contract, on an acceptance
  candidate, after a quota reading and advisor confirmation.
- Gotchas worth keeping: `bd create --silent` prints a Dolt-remote warning after the id, so `$(... | tail -1)` captures the
  warning (two isa-spec commit subjects 12cb32a and 1c7acca carry that text); gates that read `$ROOT/../<sibling>` break when
  run in a `.tmp` worktree; "gate green" must be paired with the sibling pins it held for.

