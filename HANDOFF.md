# HANDOFF — Bennett ecosystem (bennett-quantum)

Current state only; rewritten at session end (watcher pass 5, ruling 7: this file is the running-jobs list plus a
pointer; the narrative lives in the worklog top block). Rules: each repo's CLAUDE.md; council policy and rulings:
`docs/council/README.md` (tail); ladder status and the ISA 0.9 adoption decision: `docs/plan/2026-10-29-path-to-north-star.md`.
Clock: read `date -u` before any timestamp.

## Session 2026-11-01 (ended ~17:20Z; worklog block "Session log - 2026-11-01" in `worklog/` is the narrative)

**Nothing is running.** The last four Codex passes reported at wind-up and were landed; the gated pushes started at
17:14Z should have left each `main` at the sha below (check `git -C <repo> rev-list --left-right --count origin/main...HEAD`
is `0 0`; if a push failed, its log is `<repo>/.tmp/push-main.log`):
- bennett-isa-spec a3222b7: reference 0.9 milestone (bead b-isa-spec-fuk) slices .1/.2 closed, .3 in progress (K77 capture
  API, typed expander, K79-K81 vector byte locks; the unmodified controlled fixture still rejects), .4-.7 open. 524 tests.
- bennett-vm 5ae125c: 47t-c2 and c2.1 closed; c3, c5, c4 (unblocked by K81), d, b, hsd, clw open. 292/0 both engines, differential 18/0.
- bennett-dialect-spec c775e6d: draft 0.2.12 accepted (sol, round 11, 0 blocking), four S1s adopted, gate 2902/2902;
  seven consumer gaps stay open as implementation blockers (12 follow-up beads in plugin/runtimes/arith/driver).
- bennett-runtimes ec52032 (bead export only; M2 + native + UBSan closures at 88f5958).
- bennett-plugin: main at 157d4bd. Passes 14-16 are on origin/wip/m2-pass14..16-2026-11-01 (HEAD 78d5c11; gate green
  against live arith) and cannot push until the runtimes pin is refreshed (bead: RUNTIME_SHA in tests/allocator_closure.py
  to 6c1741c4.../a63f0421...). First plugin pass next session: that re-pin, then bp-ozp, bp-xyn, bp-xv0, bp-is0 (hello's
  BD-B-ISA7 trigger is R entry `main` needing typed budget fault F(1): ISA 0.9 only), bp-xms/7ni, rung-1 bp-xb8/zeg/75y.
  Bead filed at wind-up: full-width CC launch 464/276 s -> 1677/1640 s after the arith re-pin.

**Next, in order:** plugin re-pin -> push -> rung-3 rerun (`bennett-conformance/ladder/rung-3/gate.sh`); reference 0.9
slices .3-.7 -> one acceptance round at the pin move (ruling 2); VM 47t-d/b (0.9 execution); plugin `-bennett-isa=0.9`
producer mode; dialect 0.3 track (grading target ISA 0.9); rung-1 plugin beads; rung 4 gate. Deferred: watcher verdict 4
(one gate template in `bennett/tools/`); circuits hook commit (its gate fails on re-imported fixtures; held track);
brt-nuu.2 full ASan; b-dialect-spec-oxs (33 evidence rows).

**Waiting on the maintainer:** nothing. Watcher daily (next 2026-11-02 15:46Z).
