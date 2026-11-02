# HANDOFF — Bennett ecosystem (bennett-quantum)

Current state only; rewritten at session end 2026-11-02T13:45Z (shift 3 wind-down, maintainer order 11:12Z). Narrative:
top block of `worklog/002_2026-11-02_orchestration.md`. Detail: `.tmp/orchestrator/shift-3.md` (landed, decisions, every
child's result), advisor rulings `.tmp/orchestrator/advisor-notes.md` (R1-R11 and the 11:12Z wind-down bind). Rules: each
repo's CLAUDE.md; council policy `docs/council/README.md`; plan `docs/plan/2026-10-29-path-to-north-star.md`. Clock: `date -u`.

## Next, in order

1. Maintainer ratifies docs/decisions/2026-11-02-code-quality-policy.md; then its §5 adoption order (baseline meter, review debt per repo starting with plugin, law 2 + gate.toml + gate_run.py).
2. Maintainer decisions on the contract queue: authorise (or not) in-version 0.9 K-entries for the council-accepted notes
   (incl. b-isa-spec-0jq, HELD FOR MAINTAINER); decide the ISA 0.10 publication for l2p (north-star gap b-isa-spec-bwm),
   fd0, lpe, sqr (b-isa-spec-56j) and dialect 0.2.13 for 2cg, 4yg.1 (b-dialect-spec-ek3). Accepted list with run dirs:
   `.tmp/orchestrator/opus-council-s3d-PROGRESS.md`; applied so far: ISA K83 (z4c), K84 (checker-diagnostics), dialect 5u3.
3. Turn the red heads green and push: bennett-isa-spec (b-isa-spec-500, `tests/source_constructor.rs:134` stack overflow;
   46 commits ahead incl. K83/K84), bennett-vm (gate.toml isa-spec pin lacks the K83 fixture), bennett-driver (runtimes pin
   ec52032 lacks scripts/native-check), bennett-sched (adopt the gate_run stub, bennett-sched-68k; old hook reads live
   isa-spec). Gate-template follow-ups: bennett-estimate-m6p, bennett-driver-3j4, gate_run sandbox fails when a sibling's
   temporary worktree vanishes from the workspace root.
4. Merges (all on wip/ branches, see below): vm-fixes (review CLEAR on (a)(b)(c); run the pinned dual-engine set against
   isa-spec ecaaac0 first, setup in bennett-vm-fixes/.tmp/review/pinned); bjm-dense (after bennett-vm-5vj is fixed and test
   d1b un-ignored); rung4-plugin (not mergeable yet: bp-fj1 open; the 5u3 early-closing flag stays off by default).
5. Contract follow-ups (council commands in opus-council-s3d-PROGRESS.md "NOT RUN"): adg round 3 (device-model ownership),
   0jq + checker-fault-rate joint revision (shared fault_rate paragraph from Muse), pe1 one-line fix + Muse re-seat,
   derive3 brt-vbi round 1; plugin bp-fj1 evidence (dialect §14.2 ⊤ function pointers blow up the spec-K analysis) to council;
   sol-derive4 notes (docs/notes/2026-11-02-derive4/, advisor R10 queue F04 F08 F23 F14 F11, then the 29 contract beads).
6. Rung-3 pins.json refresh + rerun against plugin 0ac6180 (brief `.tmp/orchestrator/briefs/sonnet-rung3.md` step 2).
   Checker P1 bugs bennett-conformance-2hl, zlo, 30g (sol-checker). Dialect 0.3 to council after b-isa-spec-fuk.7
   (S0 fixes d4s/fa8 drafted; pre-flight has 89 stale-hash failures, b-dialect-spec-qbu).
7. Deferred by design: F30 mixed-binary rung (file when rung 3 or 4 lands, bennett-4ht); bennett-p2i (optimising
   specialiser/scheduler, triggered by the first cost-red rung clause).

## Mains (origin/main at 13:40Z; `git -C <repo> rev-list --left-right --count origin/main...HEAD`)

| repo | origin/main | local ahead | note |
|---|---|---|---|
| bennett | (this commit) | 0 | |
| bennett-isa-spec | 9825c42 | 46 | HEAD red: b-isa-spec-500 |
| bennett-dialect-spec | 9a452b9 | 0 | |
| bennett-conformance | 6e6a6f1 | 0 | |
| bennett-vm | c26a4fd | 3 | HEAD red: K83 fixture at pin |
| bennett-arith | 5e9b450 | 0 | |
| bennett-runtimes | 248e468 | 0 | brt-fyv green here |
| bennett-driver | 54d32fa | 14 | HEAD red: runtimes pin |
| bennett-plugin | 0ac6180 | 1 | bead export only |
| bennett-sched | 7f9ceb5 | 16 | HEAD red: old hook, live isa-spec |
| bennett-estimate | 54f2c1c | 1 | bead export only |
| bennett-circuits | 9ef99d8 | 0 | |
| bennett-targets | dd03671 | 0 | |
Everything unpushed is backed up gate-free at `wip/session-end-2026-11-02` (mains) and `wip/session-end-2026-11-02-<branch>`
(worktree branches vm-fixes, bjm-dense, rung4-plugin); codex jobs also back up to `wip/<job>`.

## Stopped at session end

Nothing launches without the maintainer. Claude delegates: all finished (results in shift-3.md Landed).
Codex sol runners (bennett/tools/codex_job.py), stopped after their current attempt by `.tmp/orchestrator/winddown.py`
(log `~/.local/state/bennett-codex-jobs/winddown.log`; state `stopped-session-end`); some may still be finishing that
attempt: check `systemctl --user list-units 'bennett-codex-*'`. Resume any with
`python3 /home/tobias/Projects/bennett-workspace/bennett/.tmp/orchestrator/resume_job.py NAME ["NOTE"]`
(systemd --user scope, OOMPolicy=continue, MemoryMax=14G, `--thread` from status.json; never plain `setsid nohup`):
- sol-vm-queue (bennett-vm; 47t-c3 needs a dual-engine slot), sol-plugin-queue (bennett-plugin), sol-sched (3k1 first),
  sol-estimate (bst first), sol-ref09 (isa-spec reference; bound the isa09_forwardin memory runaway; vectors in 3w4, ezl),
  sol-checker (2hl zlo 30g first), sol-derive4 (R10 contract queue).
- Blocked, resume only when unblocked: sol-arith-softfloat (bennett-arith-4yg.1 PPC tie parity, accepted in council
  derive3, needs publication), sol-driver-queue (no ready beads: 3j4, fgv, cyg.2/.3, i0v upstream).
- Complete today: sol-runtimes-queue, sol-contract, sol-contract-pass2, sol-contract-rev/rev2/rev4, sol-derive3, sol-bwm,
  sol-adg-rev, sol-4ht-audit, sol-isa-textdefects, sol-dialect-s0, sol-dialect03-s0fix, sol-bjm.

## Waiting on the maintainer

Items 1 and 2 above. Watcher daily (next 2026-11-02 15:46Z).
