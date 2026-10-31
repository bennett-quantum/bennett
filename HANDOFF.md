# HANDOFF — Bennett ecosystem (bennett-quantum)

Current state only; rewritten at session end. History: `worklog/`, `docs/process-watch.md`, per-repo HANDOFF.md.
Rules: each repo's CLAUDE.md; council policy: `docs/council/README.md` (tail = rulings of 2026-10-31).
Clock: read `date -u` before any timestamp (orchestrator drifted earlier today).

## 2026-10-31T21:42Z (session 2026-10-31, started 07:30Z; written before a context compaction)

**Accepted today**: reference interpreter (isa-ref round 24, sol + codex, snapshot ad84e75, 461 tests);
ISA draft 0.9 by **all three seats** (sol r3, codex r2/r4, muse r5 = muse's one meeting; K1-K75; K64/K65 ratified);
dialect draft 0.2.11 (round 10, sol + codex; gate 2834/2834). Plugin M1 declared on the plan's definition.

**Running (Codex sol, one job each; collect each from its task notification, verify, then push):**
1. ISA 0.9 **editorial pass IV** (muse's 4 S1 suggestions: §16.3 hashes, §5.5 wording, §6.1 dependency-set test,
   §11.1 publish `spec/ref-0.9.json` + §17 item 7 fixture; status header "accepted by all three seats").
   After it lands: run `conformance/tests/draft_witnesses.py`, push ISA main through its gate (background, >10 min).
   **No further muse round** unless a structural blocker appears (maintainer). Then the **publication step**:
   publish 0.9 **alongside** 0.8 (the dialect gate reads `spec/Bennett-ISA-Spec.md` live and 0.2.11 grades against
   0.8) — e.g. `spec/Bennett-ISA-Spec-0.9.md` + README; do not replace the 0.8 file.
2. bennett-plugin **M2 pass 9** (bp-jx3 N27 expansions, then bp-w2b N26 memmove closure; soft-float production
   stops there per major). Push with plain `git -C <plugin> push origin main` (hook gates a clean worktree of the
   pushed sha; ~6 min). Then next M2 beads one per pass: bp-7ni closure, an9 (N21), yen (N24), 365 (N25), pnt/26l/wek
   (PT images), cbg/f9j/y56/qsx (platform N-rules), 96j/lct; M3: rbl, 65x, qql; M4: o7f.
3. bennett-vm **M5** (first 0.9 consumer: 47t ref library, hsd, clw, cxg, 47i; files 0.9 gaps as beads in
   bennett-isa-spec with label consumer,vm). Push VM main through its gate when it lands.
4. **Rung 2 end-to-end** (bennett-conformance `ladder/rung-2/`: hashtable.c from BennettVM.jl/test/reference/c
   through plugin -> reference interpreter + VM -> native comparison -> reversal; expected to fail; deliverable is
   the ordered blocker list as beads). Its blocker list is the work plan for the plugin/VM/estimate/driver next
   (maintainer 2026-10-31: "drive one real slice end to end; the consumer chooses the next pass").

**Landed today, all pushed**: bennett-arith M1 (606 soft-float exports, both majors, 1.03M checks; dist/llvm18|23/
bennett-arith.bc, SHAs in its HANDOFF); plugin M2 passes 1-8 (kv5, 311, piq, 3w4-accounting, 2mg, 7ni partial, 9m8;
gate 66/66/0/0/0 both majors, 264 cross-major pairs, 45 published matches); conformance: clause graph + statement
layer, 6 proofs (INV-1..6), neutral suite re-imported from ad84e75; council schema: steps optional, kind kept;
watcher daily (next 2026-11-01 15:46Z), 4 passes, all verdicts applied; rule 12 withdrawn.

**Policies in force** (docs/council/README.md): one reviewer on fix rounds; sweep before revote; consumer-chosen
spec passes; one pass per bead with one gate; milestones mean what PLAN says; HANDOFF at session end only;
muse advisory for patch tracks, required for new contracts.

**Waiting on the maintainer**: nothing. **Held**: circuits M4, north-star round 7, targets gate decision, dialect 0.3
track (after 0.9 publication), dialect oxs evidence closures (33 rows).

**Quota at 2026-10-31T21:42Z**: see `quota`; Codex unconstrained today (banked resets); Fable 2x Opus on the Claude side.
