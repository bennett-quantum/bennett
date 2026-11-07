# Worklog chunk 002

## Session log - 2026-11-07 - local post-merge main health runner
- Added the local runner, detached fetched-main gate caches, persistent status/history and merge attribution.
  Existing repo stubs retain their pinned tool/sibling selection; no push hook or remote automation is added.
- Heavy checks mirror qgate scope/load/memory waits. R40: hang guards produce TIMEOUT/UNKNOWN, not red.
  Tests use local Git remotes and mocked lock probes/clock, with no elapsed-time assertions.
- Found a contract gap: rungs 1/2 accept plugin/vm revisions but cannot select runtimes/driver/ISA revisions;
  recorded bennett-t9r. The runner fails loud on unsupported selectors rather than claim current-main coverage.
- Validation and bounded real-run evidence are recorded in the job progress file for orchestrator review.

## Session log - 2026-11-07 - shift 13 (Opus orchestrator): rung-3 preparation lane; dialect 0.3-r1 council-accepted and pushed
- Second orchestrator lane beside shift 12 (R33b). Six sol jobs on job/r3-* worktrees + read-only re-auditors. Landed:
  runtimes main d6a4f80 (integer printf fixtures with hand-derived bytes incl. the no-newline return-time flush, native
  goldens LLVM 18/23); dialect main 4bca41b (classical R profile 0.3-r1 for ISA 0.9: typed R faults, producer identity,
  console lifecycle, saved-tape-v1; council round 1 ACCEPT unanimous sol/astra/muse, meta 21bccf6; bare 0.3 stays ungraded);
  meta f3337d2/d14de7d (2026-11-07 re-audit: 7 sol reports, Sonnet SPOTCHECK, SYNTHESIS).
- Handed to shift 12: job/r3-gate (conformance ladder/rung-3: formatted workload, parametrised dialect/ISA contract row,
  multi-stage native receipt audit; r1 BLOCK -> r2 CLEAR). Conformance main's own gate is red (bennett-conformance-mnr:
  checker/tests/published_certificates.rs reads ../../bennett-isa-spec live); it never had a PASS record at e39501e.
- Plugin N23 varargs integrated into R production (job/r3-varargs, gated + CLEAR): reference forward = native and exact
  reversal on both majors. Step T (typed R faults) running on a disjoint branch; joint review pending (R31e).
- Gotcha: this lane's builds pushed load to 14 and shift 12's plugin push-hook gate timed out (120 s per-command limit, bp-1zr).
  Fix: prep-lane builds wait for load < 8 AND no bennett-heavy scope (briefs/r3-common.md). Heavy gates have priority.
- Gotcha: the quality ratchets (dialect, plugin, driver) fail any job that adds files; every r3 job needed a baseline fixup.
  Brief the ratchet into the first job round next time.
- Surprise (rung-3 risk): the VM never finishes a 225956-step produced R object that the reference interpreter runs in 1.86 s;
  stepping looks superlinear (bennett-vm-8f3, P1). Formatted musl through the driver's native comparison faults 7 inside
  musl pop_arg (brt-9yk); full vfprintf R analysis exhausts its allowance (bp-owg).
- Surprise: the Sonnet spot-check found sol re-audit grades ~0.3 step generous and a reference-interpreter CC-tier ashr
  mutation that survives 152 tests (b-isa-spec-cj6e). SYNTHESIS calls for Round 3 on dialect-spec, runtimes, meta, isa-spec.

## Session log - 2026-11-07 - shift 12 (Opus orchestrator): isa-spec 0.9 reference interpreter pushed; R31/R32 cut the review cycle
- Pushed isa-spec main 9825c42..3b10907 (merge --no-ff job/quality-isaref). Council round 3 (sol + astra; sol joined because the
  fix reached pairs09.rs) resolved CODEX-R2-B1 but both seats found one new member of the same family: with imported pair bodies
  unavailable, decidable K91 partition checks are deferred to Unverified instead of rejecting. Re-graded P2 under R32 (the oracle
  never certifies the malformed pair, no rung named) -> b-isa-spec-qf44; merged. Third round in a row of "check placed after the
  missing-body deferral": the bead asks for a generated imported-vs-local differential family, not another round.
- Maintainer R31: astra never codes (review/council only); estimate stops its fix cycle: estimate-revert reverted the two
  unreviewed recompute checkpoints + four fix rounds (10 revert commits, kept separable measurement support from 5062ee2), gate
  PASS a66610d, review running; recompute re-lands spec-first (bennett-estimate-e9a). driver v4f -> P2, tokenizer bead
  bennett-driver-tlg; driver merges after plugin main.
- Maintainer R32 (velocity): P0/P1 only with a named rung / oracle / gate; 2 rounds then merge-with-P2 or revert; councils only for
  oracle code and contracts. Plugin and arith council round 2 dropped; bp-trh (prior-object hash drift, unchanged observables)
  -> P2.
- plugin: gatefix2 found the duplicate __bennett_rt_ss_push (pruning dropped implicit init while keeping push/pop) and moved every
  bounded gate driver into scripts/test (82 cmds, ~140 s); gatefix3 traced the remaining receipt failure to deliberate layout
  commits 6231c2d/6091986 and re-recorded 16 objects through the writer (312 kept, 74 oracle vectors agree): full gate PASS
  c085c2e. Lesson repeated: the gate, not the suite, found both.
- quality-vm round 1 done (8bc9d78; 359 tests 53 s; cov 82 %); its gate waits for the heavy queue. arith re-pin to 3b10907 running.
- After handoff: estimate main pushed 54f2c1c..f0add8a (revert candidate, rev CLEAR 47aead7); plugin main pushed 0ac6180..6ff4b01
  after the push-hook gate failed twice on load-sensitive 120 s per-command limits in mixed-native device-fp (gatefix4 a4f7708:
  release checker, 480 s from a measured 204.5 s worst case; bp-1zr); driver main pushed 54d32fa..2bd06fe. arith re-pin to
  3b10907 admits token_aliases but 37 adjoint_table claims stay Unverified and 3 receipts time out (JOB-BLOCKED, successor decides).
  Lesson: with two orchestrator lanes the push hook's wall-clock limits are the weak point; s4/qpush.sh waits for load < 8.
- Gotchas: council.py --context takes one path per flag (repeat the flag); gatefix children run gate_run in-process (no scope), so
  new s4/qgate.sh waits on both bennett-heavy scopes and gate_run processes; s4/mkpacket.sh rebuilds council packets.

## Session log - 2026-11-07 - shift 11 (Opus orchestrator): first three implementation councils, two mains pushed, gates keep finding what suites miss
- Pushed dialect main e0456ee..b6a6e46 (quality-dialect r2 CLEAR + 0.2.14 spec, fidelity CLEAR) and circuits main ee20847..5d10d65
  (quality-circuits r1 BLOCK drw -> r2 BLOCK n0p -> r3 CLEAR). Both worktrees removed.
- Councils (sol gpt-6.1-sol + astra gpt-6-astra on codex, Muse muse-wonder-full-1.0), all run as T3 seat children over a frozen
  detached worktree per round: isaref r1 REVISE (3 S0) -> fix -> r2 split (2 accept; astra CODEX-R2-B1, an early `continue` added by
  the r1 fix skips the mandatory K92 rejection) -> fix running, r3 = astra fix round. plugin r1 split (indirect-call guard bypass,
  duplicate labels, declaration abort). arith r1 REVISE (PPC sin tiny-argument low part in every mode; token_aliases rejected by
  the pinned ISA reader). New task files docs/council/task-impl-plugin.md, task-impl-arith.md (task-impl.md is isa-ref specific).
- MERGE RULE 2 found 33 unpushed isa-spec main code commits only skimmed by r1: rev-isaspec-main-r1 BLOCK P0 dnjq (a reversed
  mint's token still ran through public oracle APIs) -> fixed -> r2 CLEAR. Lesson: "reviewed range" is not "reviewed"; read the
  Coverage line of the review doc before counting commits as covered.
- Gate before review (MERGE RULE 1) caught nothing on dialect/driver/circuits/estimate, but the plugin push gate failed twice on a
  head whose scripts/test, two sol reviews and a council were all green: production-CC soft-float records and shadow-stack link
  cases never ran in the default suite. Fix children now move each failing gate record into scripts/test.
- Review rounds on heuristic linters (driver hygiene ratchet: inline bodies -> raw strings -> stringify!) and on one scheduling
  rule (estimate K81/§6.2: adjacency -> disjointness -> restored inputs -> reads of restored inputs) did not converge within the
  round limit; both stopped for the advisor (R30 gave estimate a fourth round on astra for model diversity; it fixed tdf, r4 found w2b).
- Gotchas: a council seat's JSON failed collect on a trailing period in `step:3.`; the orchestrator removed the one character and
  kept the original beside it. Driver tests need TMPDIR set (KeyError by design). A turn that ends waiting on a bare systemd
  scope is never woken: launch gates from a background Bash.

## Session log - 2026-11-06 - shift 10 (Opus orchestrator): round-1 reviews, two mains pushed, gates found what reviews missed
- Pushed circuits main 9ef99d8..ee20847 (pin discipline + c9l fix, circuits-main r2 CLEAR) and targets main
  dd03671..a8f5089 (quality-targets r3 CLEAR + gate-layout fix ab4cd24 reviewed CLEAR). Both worktrees removed.
- Launched as T3 children (codex gpt-6.1-sol xhigh): isaref r2 (critical path, P0 jple b6ds, P1 0dq0), r1 reviews of
  arith/plugin/estimate/dialect/runtimes (one reproduction each first), round-2/3 fixes for each BLOCK, quality-sched,
  quality-driver (cut from their CLEAR pin branches), quality-circuits (from the new circuits main).
- Surprise: CLEAR reviews do not imply a green push gate. targets: the new test pin resolver ignored the gate run layout
  (BENNETT_GATE_LAYOUT), so every pinned test panicked inside gate_run; runtimes: `scripts/gate --all` (not the fast
  suite reviewers run) dies in tests/test_runtime.py allocator-18 with "bennett runtime fault 7" / SIGILL. Rule adopted:
  run `gate_run.py run --repo <main> --sha <job head>` BEFORE launching the review, not at push.
- Surprise: estimate main carried two never-reviewed sol-estimate checkpoints (5062ee2, 989dd04) outside the job review's
  main..job range; their review found a K81 narrowing (pjj), whose fix then admitted non-disjoint rows (P0 yak, exact
  label on a semantically different schedule). Rule adopted: before any push, list origin/main..main code commits after
  the last review snapshot; each gets a <repo>-main review.
- Dialect main holds the unpushed 0.2.14 spec draft 22f9ed6 (Opus-applied); a sol fidelity read is running; no dialect
  push without it.
- Gotcha: bead exports committed on each main at handoff mean job branches now merge with --no-ff (no fast-forward).
- Quota: Codex 39 -> 42 % (17-20 behind); Claude row 41 % (0.2-0.5 behind) until 13:48Z, then HTTP 429 on every read.

## Session log - 2026-11-06 - shift 9 (Opus orchestrator): round 1 continues; first merge of the programme
- Merged job/quality-meta into meta main (035f924) after a sol round-2 CLEAR; ran scripts/install-hooks.sh, so the meta
  push hook now fails unless at least one unittest actually passes (45 tests ran on the push 3517a0c..4055747).
- Launched quality-dialect and quality-runtimes as T3 children (worktrees bennett-dialect-spec-job-quality,
  bennett-runtimes-job-quality). Dialect's contract P0/P1 beads and the unpushed 0.2.14 draft are out of its scope.
- Gotcha: merging a branch that `git rm --cached` files deletes them from the main checkout's working tree; the council
  logs were restored from the first parent as ignored local copies.
- Gotcha: two live orchestrator shifts (R26: the old one idles until its children end) both react to the old shift's child
  completions. Shift 9 checks shift-8.md's log before acting; a read-only watcher over T3's statev2.sqlite
  (orchestration_v2_projection_runs) wakes the new shift when an old child finishes.
- Paused early under R28(b): Claude weekly 38 %, +0.4 % ahead of linear pace at 07:13Z. Codex children keep running.

## Session log - 2026-11-06 - shift 8 (Opus orchestrator): quality floor round 0 + start of round 1

What changed: round 0 of docs/plan/2026-11-06-quality-floor-remediation.md launched 06:24-06:28Z (quality-meta, pin-driver,
-arith, -plugin, -sched, -circuits) plus round-1 quality-checker, -estimate, -targets, each in a git worktree
`../<repo>-job-<name>` on branch `job/<name>` (D5; nothing committed to any main). At 06:50Z the maintainer retired
`codex exec` runners (R26): live runners were drained after their current attempt by .tmp/orchestrator/s4/r26_drain.py and
all follow-on work runs as T3 delegate children (codex gpt-6.1-sol xhigh). Reviews are fresh sol sessions
(s4/mkrev8.py, D9). Results so far: pin-arith CLEAR; pin-sched r1 BLOCK -> fixed (a3e36b3) -> r2 check running;
quality-meta trimmed to its non-runner parts (hook, council tests, litter) -> r1 BLOCK (bennett-dog) -> r2 running;
pin-plugin, pin-circuits complete -> reviews running; quality-targets items 1-8 done (65 validator tests reproduced);
quality-isaref batch 1 and quality-arith started. Full state: .tmp/orchestrator/shift-8.md.

Gotchas: (1) The Codex sandbox cannot create sibling worktrees, so pinned-sibling caches must be materialised by the
orchestrator: `gate_run verify --repo <MAIN checkout> --sha <job branch head>`; with --repo <worktree> bwrap cannot
chdir through the worktree's .tmp/gate/cache symlink. (2) The committed codex_job.py loops into a new attempt on its own;
"finish the current attempt" needed an external watcher (r26_drain.py) that stops the scope at the outcome log line,
which the runner writes after its attempt-end commit and wip backup.
Surprises / root causes: most consumer pins (isa-spec ecaaac0) predate fixtures and K91 token_aliases that consumer tests
already need, while the isa-spec commits that support them are unreviewed sol-ref09 WIP under a review BLOCK. So
quality-isaref batch 1 is the critical path for re-pinning sched, checker, arith (b-isa-spec-3wl9, bennett-arith-4ss).
arith's three "K91" reds were live drift (pinned run green), but its objects will break once the pin passes K91.

## Session log - 2026-11-05/06 - advisor: ecosystem quality audit and remediation plan

Advisor session (Fable), no orchestrator shift, nothing launched in any repo; Codex runners stayed stopped.
- 2026-11-05 07:56Z-08:25Z: twelve read-only auditors (ten Sonnet, one per code repo; Haiku for targets + meta tools) ran a common brief (`docs/quality/2026-11-05-audit/BRIEF.md`): composition, build/test timings, coverage where cheap, 15-20 hand-classified tests per repo, policy rule 9 patterns. Reports and synthesis under `docs/quality/2026-11-05-audit/`.
- Headline: oracle layer is real (~65 % of ~230 sampled tests useful, <5 % tautological) but 7 of 11 code repos are red at HEAD for two root causes (Codex attempt-end WIP commits landing on main; tests reading the live sibling instead of the gate pin, in driver, arith, plugin, sched and circuits), one real checker regression (conformance `resource_contexts.rs:476`), blind tolerances in arith (280k assertions at 1-4 ulp, observed max 0.5 ulp; both open P0s pass), self-authored oracles (runtimes native twin, dialect labels + rehash), build loops unusable in isa-spec/sched/vm/driver (isa-spec: 70 test binaries x 110 MB; the gate runs a 23.8 GB test), 500-1200 line functions in every large crate, bead IDs in error strings and emitted output in six repos.
- Gotchas: auditors under `ulimit -v 8 GB` OOM'd circuits `oracles` (needs 6.75 GB, HANDOFF says 5); load 17-20 during measurement so timings are upper bounds; the meta repo's installed pre-push hook is the cargo-only stub and always passes; `codex_job.py` pace guard fails open on a quota read error.
- 2026-11-06 05:25Z: maintainer direction "raise the quality floor, use Codex (sol xhigh) extensively, a couple of rounds until grades improve". Plan written: `docs/plan/2026-11-06-quality-floor-remediation.md` (round 0 root causes + pin discipline, round 1 one sol job per repo with the round-2 review debt folded in, round 2 oracle independence, re-audit with the same brief after each round; decisions D5-D8 for the maintainer). Not yet launched.

## Session log - 2026-11-03 (afternoon) - shifts 5-7: cross-checks and round-2 checks, Claude-seat reviews of Codex code, session wind-down

Written by the shift-7 orchestrator (Opus) at session end; covers ~11:20Z to the wind-down at ~13:10Z. Records: `.tmp/orchestrator/shift-5.md`, `shift-6.md`, `shift-7.md`; rulings R20-R24 and the wind-down order in `.tmp/orchestrator/advisor-notes.md`; current state in `HANDOFF.md`.
- Pacing drove routing. Codex stayed 5-6 points ahead of linear (R17: no Codex launch), Claude 4-8 behind (R20/R22: 2-3 Claude delegates). Work whose opposite-model seat is Claude moved to Claude: the sched, estimate and reference-interpreter batched reviews (Codex-authored code), the factored points-to design review (sol-authored), the bjm-dense pre-merge and rung4 bp-ipp reviews. Claude-authored fixes (targets round 2, circuits gate repair) went to Opus implementers with a sol check queued. Dialect 0.2.14 and the native-sharing note revision went to Opus at the end of shift 7.
- Policy rule 2 cross-checks (Sonnet) over Codex commits added blockers in every repo checked: runtimes brt-mab (failed host write reported as dialect fault 8, not exit 125), driver 6bl (EXDEV on cross-filesystem cache rename) and 7cc (native comparison needs C source: a narrowing for non-C front ends), conformance eq2 caq, arith P0 ufr and 8eb (directed-rounding wrong side; the existing `_rm` tests accept 4 ulp so they cannot catch it) and yuk. The orchestrator re-graded several reviewer nits to P1 under rule 4 (estimate 7zd fn5, driver tbc, plugin mqp ok6): reviewers under-grade "claimed behaviour without a test".
- Batched reviews with a Claude seat: sched BLOCK (P0 fdu: adjoint action_call reverses leaves after expansion, K62 says replace then expand), isaref BLOCK (P0 opnq: a claim naming a schedule is graded Proof against reference semantics only, even with a fabricated schedule_hash), estimate CLEAR by the reviewer but BLOCK after re-grading. bjm-dense pre-merge BLOCK (P1 d2j: Runtime::equals compares seqs that Log::record keeps across composed remaps).
- ROOT CAUSE, circuits "red gate" (opus-circuits-gate): the PINNED gate was never red; the tests read the live sibling isa-spec (71 commits past the pin, 38 cases now isa=0.9). Fix d2fd693: a case's version is its object header, out-of-version cases must be refused at load. Lesson: a red test against a live sibling is not a red gate; check what the gate pins before filing.
- Factored points-to design (rung-4 critical path, R16): Opus review REVISE (rung4-plugin 33ff4be). Core sound, no default-path widening, no 4ht lock-out; but P0 bp-6rz in EXISTING code (loadPair drops the whole-value alternative for residue slots with stride < width: a valid handle program is rejected) and design P1s bp-9g8 bp-eiq bp-m7h.
- Round 2 done by Codex runners but not yet checked by Claude: vm (0m5 wyg 79y 1pz ket d1y all closed), driver (7gi bcl 4r1 crx; checked CLEAR), runtimes (67w 34p; checked CLEAR). R23 settled console close toward native EBADF semantics (editorial sentence in 0.2.14).
- GOTCHAS. (1) `winddown.py` waits for each codex child to finish; the maintainer order wanted them stopped at once, so the orchestrator SIGSTOPped runners via winddown.py and then SIGTERMed the five `codex exec` children; commits and wip backups followed within 40 s. (2) The sol-sched wind-down commit FAILED (`pathspec 'examples' did not match`: an owned path that exists on disk but is unknown to git passes codex_job.commit's exists() check and kills the pathspec commit); the orchestrator committed the staged tree as 95aaca9. Fix in codex_job.commit: skip paths with no tracked files and no untracked content, or stage with `git add` per path and commit without a pathspec list of non-git paths. (3) Runner final_tail in status.json is from the LAST COMPLETED attempt; SIGTERMed attempts leave the previous one, so their JOB-BLOCKED text is stale (sched-enz and isa z4c were already closed). (4) The vm runner edited gate.toml outside its owned paths (i63 pin to isa-spec fd626d3, which is only on origin wip/sol-ref09); committed fffc277 with that caveat. (5) A T3 server restart (~12:49Z) cancels the harness-tracked event waiter but not the Claude delegates.
- Pushed: dialect e0456ee (worklog) only; meta at session end. Everything else is behind R12 / rule 1 (open P0/P1 or unreviewed new work) and backed up to `wip/session-end-2026-11-03`.

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

