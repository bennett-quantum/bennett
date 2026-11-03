# HANDOFF — Bennett ecosystem (bennett-quantum)

Current state only; rewritten at session end 2026-11-03 (shift 7 wind-down, maintainer order ~13:10Z). Narrative: top
blocks of `worklog/002_2026-11-02_orchestration.md`. Detail: `.tmp/orchestrator/shift-4.md` … `shift-7.md` (Landed,
Decisions, every child's result), advisor rulings `.tmp/orchestrator/advisor-notes.md` (D1-D4, R1-R24 and the wind-down
order bind). Rules: each repo's CLAUDE.md; review policy `docs/decisions/2026-11-02-code-quality-policy.md` (IN FORCE);
council policy `docs/council/README.md`; plan `docs/plan/2026-10-29-path-to-north-star.md`. Clock: `date -u`.

## State in one paragraph

Every repo except dialect has had its first batched review (`<repo>/docs/reviews/2026-11-03-*.md`); every one is BLOCK or
waiting on a round-2 check, so under R12 + policy rule 1 NO code main was pushable at wind-down. Only meta and dialect
pushed today. ISA 0.9 K85-K93 are applied (in-version K track, D2); K94-K97 (pe1, adg, 0jq+cfr) are accepted and queued
for the editor. Dialect 0.2.13 is published; 0.2.14 (brt-vbi + the R23 console-close sentence) is committed locally (22f9ed6), checked, unpushed.
Rung 4's critical path is the exact factored points-to engine: its design review came back REVISE (P0 bp-6rz in existing
code). Codex is ahead of linear pace (R17: no launches while ahead); Claude weekly resets 2026-11-03 17:00Z.

## Mains (origin/main at wind-down; `git -C <repo> rev-list --left-right --count origin/main...HEAD`)

| repo | origin/main | local ahead | why not pushed |
|---|---|---|---|
| bennett | (this commit) | 0 | |
| bennett-isa-spec | 9825c42 | 72 | isaref review BLOCK (P0 opnq, P1 7cvg; two red crate tests x6to); K91 editor's note 4cc6ac5 |
| bennett-dialect-spec | e0456ee | 5 | 0.2.14 draft 22f9ed6 (Opus) verified at wind-down (v02 2944/2944; v03 same 89+6 qbu non-pass set) but needs a sol fidelity read before publication (queue 7b); new b-dialect-spec-ac7 (smul/umul_with_overflow type for W>128) |
| bennett-conformance | 6e6a6f1 | 25 | checker P0/P1 890 gm5 37u + xcheck P1 eq2 caq |
| bennett-vm | c26a4fd | 34 | round-2 P0/P1 all CLOSED (0m5 wyg 79y 1pz ket d1y): needs the Claude round-2 check; gate pin fd626d3 needs isa-spec main pushed |
| bennett-arith | 5e9b450 | 11 | round 2 rn8 gdg rhn + xcheck P0 ufr 8eb, P1 yuk |
| bennett-runtimes | 248e468 | 16 | xcheck P1 brt-mab |
| bennett-driver | 54d32fa | 34 | xcheck P1 6bl 7cc + re-graded P1 tbc |
| bennett-plugin | 0ac6180 | 23 | round 3 bp-0xt, P1 bp-mqp bp-ok6, D4 interim bp-acm |
| bennett-sched | 7f9ceb5 | 34 | review BLOCK: P0 fdu, P1 jez b08 (+ xzv 2u4 kbc a0v ark vt8 nsy) |
| bennett-estimate | 54f2c1c | 19 | re-graded P1 7zd fn5 |
| bennett-circuits | 9ef99d8 | 9 | gate repair d2fd693 (Opus) needs its sol review (rule 1); 677266c was review-clear |
| bennett-targets | dd03671 | 9 | round-2 fixes (Opus) need the sol round-2 check rev-targets-r2c |

Worktree branches (not mains): rung4-plugin 33ff4be (bennett-plugin-rung4), bjm-dense 432d4ff (bennett-vm-bjm, merge
blocked on P1 bennett-vm-d2j), vm-fixes 3075153 (merged into vm main). Everything unpushed is backed up gate-free at
`wip/session-end-2026-11-03` (mains) and `wip/session-end-2026-11-03-<branch>` (rung4-plugin, bjm-dense); Codex jobs also
back up to `wip/<job>`.

## Stopped at session end

Nothing launches without the maintainer. Codex sol runners stopped 13:11Z by `.tmp/orchestrator/winddown.py` plus SIGTERM
of their codex children (mid-attempt; each tree committed and pushed to `wip/<job>`; state `stopped-session-end`; log
`~/.local/state/bennett-codex-jobs/winddown.log`): sol-checker, sol-estimate, sol-ref09, sol-sched, sol-vm-queue. Their
interrupted attempts wrote no final message: READ EACH PROGRESS FILE FIRST on resume. Already ended earlier (blocked):
sol-plugin-queue, sol-arith-softfloat, sol-driver-queue, sol-runtimes-queue. No council, heavy or Muse job running.
Claude delegates: none alive. opus-dialect-0214 committed 22f9ed6 and stopped before closing q06/9rd (open until push);
opus-notefix-ns stopped before writing (see 3c). Their cross-repo requests: bennett-dialect-spec/.tmp/opus-dialect-0214/cross-repo-beads.md.
Resume with `python3 /home/tobias/Projects/bennett-workspace/bennett/.tmp/orchestrator/resume_job.py NAME ["NOTE"]`
(systemd --user scope, OOMPolicy=continue, MemoryMax=14G; never plain `setsid nohup`), under R17 (only while Codex is
BEHIND linear pace, one at a time, `quota` row first).

## Codex queue, in order (R17-gated), with resume notes

1. sol-checker (bennett-conformance checker/): round 2 P0/P1 890 gm5 37u (after 2hl zlo 30g) + Claude cross-check P1s
   eq2 (§16.1 token spelling in bodies) and caq (K89 borrow_frame claim rejected E_CERT_SCHEMA).
2. sol-vm-queue (bennett-vm): round 2 DONE (0m5 wyg 79y 1pz ket d1y CLOSED; i63 pin committed fffc277). FIRST a
   Claude round-2 check (Claude work, not Codex); then resume for 47t-c3 (needs one exclusive dual-engine slot, R3) and
   its queue.
2b. sol-bjm-5vj (bennett-vm-bjm, bjm-dense): fix P1 bennett-vm-d2j red-first (Runtime::equals vs Log::record seq,
   review docs/reviews/2026-11-03-bjm-dense-premerge.md); Claude check; merge after one heavy dual-engine run.
2i. sol-ref09 (isa-spec reference-interpreter/): round 2 of docs/reviews/2026-11-03-isaref-batch.md: P0 b-isa-spec-opnq,
   P1 b-isa-spec-7cvg red-first; the two red crate tests (x6to) green or attributed before any push.
2s. sol-sched: round 2 of docs/reviews/2026-11-03-sched-batch.md: P0 fdu (IN PROGRESS at the stop: sched 95aaca9 holds
   src/source.rs + tests/source_adjoint.rs mid-TDD), P1 jez b08, xzv (in progress) + 2u4 kbc a0v ark vt8 nsy.
2e. sol-estimate: round 2 of docs/reviews/2026-11-03-estimate-batch.md: P1 7zd (--budget default 0) and fn5 (K86
   realisation_model), red-first.
2r. sol-runtimes-queue: brt-mab P1 red-first; brt-4dk stays blocked on brt-4dk.1 / brt-vbi (0.2.14).
3. sol-driver-queue: 6bl 7cc tbc red-first; 9zg/ppz stay blocked on cross-repo publications.
3b. sol-plugin-queue: ROUND 3 bp-0xt first, then bp-mqp bp-ok6, bp-ylb (0.2.13 adoption; close bp-usp), bp-acm D4
   interim (loud failure naming bp-acm, b-dialect-spec-6u6, "promised and pending"), bp-mq6 (arith + runtimes re-pin).
3d. sol-arith-softfloat: owns adders/ and tests/; rn8 gdg rhn, then ufr (P0) 8eb (P0) yuk (P1) red-first (tighten _rm
   tests to the exact directed-rounding side against MPFR), then 4yg.1 parity migration.
3c. native-sharing round 2 (sol+astra) after the revision is written: opus-notefix-ns stopped at wind-down BEFORE writing anything
   (resume block bennett-isa-spec/.tmp/opus-notefix-ns/PROGRESS.md, local; brief .tmp/orchestrator/briefs/opus-notefix-ns.md;
   round-1 task file .tmp/opus-council-s3d/task-d4-native-sharing.md; check script derive4/verify.py per INDEX.md); Muse R13 call 2 only after it accepts and the
   advisor confirms. P0 route for bp-acm / b-dialect-spec-6u6 (publishes first in ISA 0.10, D4).
3c'. sol-notefix-b3ui (READY, briefs/sol-notefix-b3ui.md): K91 loader capability negotiation text -> sol+astra round ->
   editorial K91 completion.
3e. sol review of circuits d2fd693 (Opus gate repair), then the circuits push gate (heavy slot).
4'. sol-rung4-ipp resume on rung4-plugin: fix P0 bp-6rz red-first (src/Analysis.cpp loadPair residue slot stride <
   width; probe .tmp/opus-rev-fpt/probe), revise docs/design/factored-points-to.md for bp-9g8 bp-eiq bp-m7h (review
   33ff4be), then a Claude round-2 check. Rung-4 critical path.
5. sol-isa-k94: fidelity fixes h7l7 wk0k, then K94 pe1, K95 adg, K96/K97 0jq + cfr (R18, R19).
6. rev-targets-r2c: sol round-2 check of the Opus targets round 2.
7b. sol fidelity read of the dialect 0.2.14 draft (Opus-applied), then push dialect.
8. rev-dialect (sol batched review of dialect tooling, Claude-authored).
9. Council rounds: derive4 notes beyond native-sharing (INDEX order). 10. Rung-3 rerun (heavy) after bp-mq6.
Claude work when quota allows: round-2 checks of each Codex fix as it lands (templates briefs/sonnet-r2check-*.md);
cross-repo bead requests still unfiled in `<repo>/.tmp/<job>/cross-repo-beads.md` / checker/.tmp/CROSS_REPO_BEADS.md
(bead clerk, template briefs/sonnet-beadclerk-s6.md).

## Waiting on the advisor / maintainer

- R13: Muse call 1 of 2 used (batch 3). Call 2 reserved for native-sharing after its round 2 accepts; ask first.
- Contract escalations from earlier runner attempts that may still be open (sched-enz and b-isa-spec-z4c are closed):
  estimate bennett-estimate-bph.4 (ISA source-to-wire / implicit-length binding, docs/CONTRACT_GAPS.md), checker
  (resource aggregation across repeated invocation contexts; realised-operator bindings for approximate native gates,
  checker/.tmp/CROSS_REPO_BEADS.md). Route through the bead clerk to isa-spec, then council if contract.
- Deferred by design, nobody starts: F30 mixed-binary rung (bennett-4ht), bennett-p2i optimising specialiser/scheduler.
