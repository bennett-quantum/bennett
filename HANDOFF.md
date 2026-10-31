# HANDOFF — Bennett ecosystem (bennett-quantum)

Current state only. History is in `worklog/` and `docs/process-watch.md`; per-repo state in
each repo's `HANDOFF.md`. Rules: each repo's `CLAUDE.md`; council: `docs/council/README.md`.

## 2026-10-31, ~21:30Z

**Running**: isa-ref round 22 (two-seat acceptance vote on 9851a9c after the R21 fixes and the 24-path
cardinality/length sweep; 436 tests); ISA main gate push (background).

**Landed today**: interpreter rounds 12-16 (353 -> 390 tests; single declarative metadata schema);
ISA main pushed through its gate (1b6e3cb; both crates green); §11.1 complete: 219 recipes, library hash fcb2f1e6…f5ce bound in §11.1, Rust = Python
(independently re-run by the orchestrator), all 8 REF beads + parent 8r4 closed; K21-K28; bennett-conformance clause graph, neutral suite, pre-push gate, four structured
proofs (4 refuted 0.8 steps filed as beads in bennett-isa-spec); process watcher + first entry, all
7 verdicts applied; council: one reviewer on fix rounds, one commit per round, severity dropped,
Lamport-structured blocking items (`steps`, ASSUMED step 1 = spec gap), proofs as standing
`--context`.

**Landed since 14:30Z**: interpreter rounds 17-18 (403 -> 412 tests; §17 defaults table; per-invocation
schedule domains); 0.9 editorial passes I-II (K29-K61: every INV-1..5 refuted/ASSUMED step closed
except two NAD-open beads 8ka/23g needing library-facing design; `[deps:]` on all 49 changed
statements; JCS-array envelope paths); INV-5 (schedule selection; 4 refuted steps; proof
arbitrated the R18 fix); statement layer (ISA-0.9-draft 1,537 statements, 91 declared markers);
proofs cite statement IDs (strong coverage 150/541 on 0.8).

**Since 17:00Z**: isa-ref round 19 ACCEPT (astra, core accept); round 20 sol acceptance vote returned one
new S0 (const_literal allocates N+1 bits; fix running); isa-09 round 1 both seats core accept, one
blocker each (K62 canonical action adjoint, K63 invocation-edge identity), spec gaps 8ka/23g
drafted as K64/K65 **pending maintainer ratification**, library hash rebound to 5de4e499…d197
(219 recipes, Rust = Python); watcher pass 2 (6 verdicts; orchestrator view: take 2, 3, 4 and part
of 1; hold 5 and 6 one round); ISA main pushed through its gate (f59cb86 + docs); draft diff
witness now uses stable labels.

**Draft 0.9 ACCEPTED by sol (r3) and codex (r2)** on snapshot 59eee9ad0d96, 0 blocking; **K64/K65 await
maintainer ratification**; muse seat held. Interpreter round 21: both seats found host-resource
aborts (same class as R20); fix running; round 22 = two-seat acceptance vote.

**Dialect outline-0.3 is ready for rulings** (`bennett-dialect-spec/spec/outline-0.3.md`, 1,266 lines, 45
items mapped, 22 numbered decisions D01-D22 with recommendations, rulings section empty; pushed 967db73).

**Waiting on the maintainer**: K64/K65 ratification (ISA 0.9); D01-D22 rulings (dialect 0.3); muse's votes.

**Next**: collect round 22 -> if both accept, the interpreter leaves the loop and suite cases are re-imported
from the accepted snapshot; after rulings, draft 0.2.11 then 0.3 from the outline (astra alone; first round on the structured schema, add
`--context ../bennett-conformance/proofs/INDEX.md` and `proofs/INV-*.md`); if accept -> sol
acceptance vote -> interpreter leaves the loop; then re-import suite cases from the accepted
snapshot. Verify the §11.1 completion (library hash Rust = Python; §11.1 marker written). Dialect:
muse's 0.2.10 vote waits on the maintainer; the 0.1-narrowing epic (b-dialect-spec-8wf) is the
next new material. Held: circuits M4, plugin M1 third pass, north-star round 7, targets gate.

**Quota**: Codex unconstrained (banked resets). Claude-side children Opus/Sonnet/Haiku; Fable lean.

**Push state**: bennett main, ISA main (gate green; hook >10 min, run in background), dialect main,
conformance main all pushed.
