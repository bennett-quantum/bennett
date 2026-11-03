# Worklog chunk 002

## Session log - 2026-11-03 (morning) - shifts 4-5: code-quality policy in force, first batched reviews (all BLOCK), Codex pacing, Muse batch 3, native-sharing route

Written by sonnet-docs-s5 at 2026-11-03T11:36Z for the orchestrator; covers work up to ~11:20Z, a later block covers the rest. Records: `.tmp/orchestrator/shift-4.md` (Opus, 09:00:32Z-10:00:28Z, context handoff), `shift-5.md` (Opus, from 10:02:18Z), `advisor-notes.md` D1-D4 and R12-R20. Git prints local time (UTC+1); times below are UTC.
- Session start 08:57Z, nothing running (winddown complete). Quota 08:46Z: Claude weekly 84 % (resets 16:59Z), Codex 10 %, Muse unreadable. Maintainer decisions (via advisor), binding: D1 the code-quality policy (`docs/decisions/2026-11-02-code-quality-policy.md`) ratified as written, with the rule-5 qualifier that the Muse seat on a semantics-bearing CLEAR round is taken when Muse quota is readable and the advisor confirms (35ccf3a); law 2 of every repo's CLAUDE.md points at it (committed ~09:05Z in 13 repos: b4c15fc here; each sibling's sha is in its own worklog). D2 an in-version ISA 0.9 K track for nine council-accepted repairs (K85-K93), l2p/fd0/lpe to 0.10. D3 dialect 0.2.13 publishes now. D4 (10:50Z) native-sharing publishes at ISA 0.10 as the FIRST item of the 0.10 draft; interim the plugin fails loudly (never silent per-launch global reset), text "promised and pending", never "unsupported".
- Advisor rulings: R12 (code written before 08:57Z may push on a green gate; policy rule 1, review before push, binds a repo from its first batched review document), R13 (Muse: council seats only, batched, at most two calls, `--attempts 1`, quota rows before and after), R14 (until 16:59Z implementation and review run on Codex sol xhigh; Claude only where Codex cannot), R15 (driver-116 stays open P1 under 4ht, outside round 2; round-2 checks make sure the refusal is loud and nothing assumes every module is marked), R16 (bp-fj1: Option A, the exact factored points-to engine is the rung-4 critical path; bp-ipp the unauthorised 4096-offset widening is a P1), R17 (below), R18 (pe1/adg as in-version 0.9 K94/K95, brt-vbi as dialect 0.2.14; bp-acm routes to council), R19 (checker-fault-rate jointly with 0jq as K96/K97), R20 (11:07Z: the after-reset Claude list opens now, Claude 8 behind pace, one or two delegates at a time, ~2 points/hour).
- R17 CODEX PACING (09:52Z, maintainer: "we are already over pace with codex"): no new Codex job of any kind (runner, resume, review, council round with sol/astra seats) while `quota` shows Codex at or ahead of linear pace; refill ONE job only when a runner ends AND Codex is behind pace; the banked reset is NOT for planning (earlier "use it up" guidance withdrawn); nothing running is killed. Consequence in this session: Codex 10 % (3.6 behind) at 09:00Z -> 15.0 % (+0.9) at 09:52Z -> 19 % (+4.2) at 11:07Z with 9-11 runners alive, so the queued launches (sol-targets-r2, sol-isa-k94, sol-dialect-0214, rev-fpt, reviews wave 2, sol-notefix-ns and its round 2, a circuits job for l2t/dzo) were held; see "Next queued" in shift-5.md.
- Wave 1 (09:04Z): 12 Codex runners (4 batched reviews: plugin, runtimes, driver, conformance; spec editor K85-K93; dialect 0.2.13; note fixes; 5 resumes) plus reviews of arith, circuits, targets, vm. FIRST BATCHED REVIEW OUTCOME: every one of the 8 reviewed repos (plugin, runtimes, driver, conformance, arith, circuits, targets, vm) came back BLOCK with at least one P0 (`docs/reviews/2026-11-03-<repo>-batch.md`, details in each repo's worklog). Round 2 fixes go to the repo's Codex queue runner (policy wants the original implementer's family; the reviewed ranges mix Codex and Claude); the round-2 CHECK is Claude (opposite model). Round-2 checks done by 11:17Z (sonnet-r2check): circuits CLEAR, conformance CLEAR (43o, b8z), plugin CLEAR (kem, ie6). Circuits is review-clear but its gate is red at base (l2t, dzo).
- Dialect 0.2.13 published and pushed (786e8a1, the only sibling pushed today; meta pushed b4c15fc and later 3f153d2). K85-K93 applied in isa-spec (57151aa) and read by an Opus fidelity reviewer (1c53235): three meaning-changing deviations (K85 h7l7, K86 wk0k, K91 b3ui), because the council graded notes, not the applied text. Rung-3 gate ran twice (heavy slot); true first red is bp-mq6 (plugin/arith digest mismatch). Details in the conformance and isa-spec blocks.
- Councils and Muse: plugin-bpfj1 r1 (76eb573) sol revise / astra revise, both reject Option B (a narrowing) and accept A; brt-vbi r1 accept/accept (fb9dfe9); checker-fault-rate r4 (3bb4de1) and 0jq r3 (96ac508) accept/accept, adg r3 accept/accept (3f153d2); MUSE BATCH 3 (R13 call 1 of 2, dossier .tmp/opus-council-s3d/muse-dossier.md, 09:59:32Z launch, exit ~10:05Z, 78c7b9b): ACCEPT all five (0jq, checker-fault-rate, brt-vbi, adg, pe1), 0 blocking, 13 S1; Muse 5-hour 0.0 % -> 2.0 %, weekly 6.0 % unchanged. derive4 native-sharing r1 (9492606): sol REVISE (B1 implicit shared globals unbound, B2 native failure carrier undecided), astra REVISE (NS1 = B1), 0.10 route judged correct; revision job sol-notefix-ns and a round 2 are queued; R13 call 2 is reserved for it (ask the advisor first). sol-derive4 produced INDEX.md for all 30 rows of the F-findings and contract beads (bennett-isa-spec docs/notes/2026-11-02-derive4/).
- TOOL FIXES AND GOTCHAS. (1) `tools/codex_job.py` hardcoded `Co-Authored-By: Claude Opus 5.5` on every Codex runner commit (misattribution that the opposite-model rule of the policy depends on) and committed the whole shared index; fixed in 769a2f6: trailer is now `Agent: <model>` and the commit is pathspec-limited (scratch-repo test: foreign staged file stays staged, trailer `Agent: gpt-6.1-sol`). Runners launched before 09:29Z keep the old code until resumed, so treat every "wip(codex job X)" commit as Codex-authored regardless of trailer. (2) The `gate_run` stub pre-push hook gates EVERY pushed ref, `wip/` included: a wip push started the 8 h arith gate (killed at 09:10Z); gate-free backups need `git push --no-verify origin HEAD:refs/heads/wip/<name>` (done as `wip/shift4-start` in all 12 siblings). (3) `resume_job.py` now also LAUNCHES new jobs (no status.json -> no thread; it creates the progress file); `s4/mkrev.py` generates review briefs; `s4/waitev.py` hit the 30-minute harness limit at 10:37Z with no event because a council EXIT already present at start was the baseline: restart with 1700 s and treat an EXIT seen at start as an event. (4) Detached runners must stay under `systemd-run --user --scope` (see the 11-02 block). (5) bd is read-only inside the Codex worktree sandbox, so cross-repo beads go to `<job>/cross-repo-beads.md` and the Sonnet bead clerk files them (36 from sol-isa-k85 alone; isa-spec 11, vm 12, circuits 9, conformance 14, driver 1, plugin 1, plus b-dialect-spec-6u6, ledger `.tmp/orchestrator/filed-cross-repo.md`). (6) The vm-fixes merge (bda07e1) hit one conflict: main's empty qif arm in `tests/cleanup_fresh09.rs` is rejected by the 0.9 parser (§16.2); verified by running, took vm-fixes' version.
- Orchestrator-reproduced results (COMMON rule 11, trust but verify): `draft_witnesses.py` exit 0 and `ref_catalog.py --check` exit 0 for K85-K93; `dialect_check_v02.py` 2920/2920 (the job claimed 2921); rung4-plugin `tests/reference_k.py --major 18` 22/22; vm-fixes pinned dual-engine run 342/0/0 per engine (39 suites).
- Not pushed at ~11:20Z: isa-spec (61+ ahead, only the fixed `500` and no full gate since), vm, driver, sched, plugin, conformance, estimate, runtimes, arith, circuits, targets: all behind R12 rule 1 (review BLOCK, round-2 check pending after the 16:59Z Claude reset) or a red/unrun gate. Meta is 2 ahead. HANDOFF.md is rewritten at session end (not here).

## Session log - 2026-11-02 - shift 3 and session wind-down: cgroup runner deaths, council acceptance path, K83/K84, push wave

Shift 3 (Opus orchestrator, 07:56Z to 13:40Z; record `.tmp/orchestrator/shift-3.md`, rulings R1-R11 and the 11:12Z wind-down in `.tmp/orchestrator/advisor-notes.md`).
- ROOT CAUSE, runner deaths (08:37Z): `setsid nohup` does not leave the launching Claude session's systemd cgroup scope
  (`t3code-claude-<id>.scope`); when that session ended, systemd stopped the scope and killed 9 sol runners and the 2aba17a
  plugin push gate with no runner.log entry. Fix: launch under `systemd-run --user --scope --collect -q -p OOMPolicy=continue
  -p MemoryMax=14G --unit bennett-codex-<name>-<HHMMSS>` (`.tmp/orchestrator/resume_job.py` does this).
- Second gotcha: a scope's default OOMPolicy=stop killed the whole sol-ref09 runner when its test isa09_forwardin hit 23.8 GB
  (global OOM, 09:02Z). OOMPolicy cannot be changed on a live scope; MemoryMax can.
- `tools/codex_job.py` has no stop command. Session wind-down used `.tmp/orchestrator/winddown.py`: SIGSTOP the runner
  (its codex child keeps running the current attempt, stdout goes to a file), and when the child exits do the runner's
  own end-of-attempt commit + wip backup, set state=stopped-session-end, kill the runner. Log
  `~/.local/state/bennett-codex-jobs/winddown.log`. Worth adding a real `stop` subcommand.
- Council: K82 Muse seat cast (accept). Contract notes (sol derivations, docs/notes/2026-11-02-* in bennett-isa-spec) went
  through round 1, revisions, an astra-only bennett-4ht (mixed fat object) re-check and two batched Muse calls. Applied to
  spec: ISA 0.9 K83 (z4c) be71d03, K84 (checker-diagnostics) 2f8e1d5, dialect 5u3 da61f93 (0.3 draft + errata-0.2.12).
  14 more ACCEPTED FOR SPEC but not applied: 0.9-route ones need maintainer authorisation of in-version K, l2p/fd0/lpe/sqr
  need 0.10 (b-isa-spec-56j), 2cg/4yg.1 need dialect 0.2.13 (b-dialect-spec-ek3). l2p accepted as a north-star gap
  (b-isa-spec-bwm). Run dirs under docs/council/; tables in `.tmp/orchestrator/opus-council-s3*-PROGRESS.md`.
- New maintainer constraints: bennett-4ht (mixed fat object must stay reachable; rubric check 84a6fcf; fat-object audit
  bennett-isa-spec docs/notes/2026-11-02-4ht-audit/, beads F01-F29 filed, F30 mixed-binary rung deferred); plan R8;
  bennett-p2i (optimising specialiser/scheduler, trigger-driven); proposed code-quality policy (not in force).
- Gate template (`tools/gate_run.py`, pinned siblings) is the pre-push hook in 9 repos; sched, estimate, driver pending
  (beads 68k, m6p, 3j4). Mains pushed this session: meta, conformance, targets, isa-spec (walk-back 9825c42), dialect,
  circuits, driver (walk-back 54d32fa), arith, runtimes, vm, plugin 0ac6180, estimate. Red heads: isa-spec (b-isa-spec-500),
  vm (K83 fixture at pinned isa-spec), driver (runtimes pin lacks scripts/native-check), sched (old hook reads live isa-spec).
- Findings: checker replay found 3 P1 checker bugs (bennett-conformance-2hl zlo 30g); bjm dense engine decided cleanliness
  within its error bound (yt9, ykb fixed on bjm-dense; 5vj open); plugin bp-fj1: dialect §14.2 makes the spec-K analysis
  blow up on SQLite (OOM 13.7 GB), evidence note in bennett-plugin-rung4 docs/notes/2026-11-02-bp-fj1-reference-k-evidence.md.

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

