# HANDOFF — Bennett ecosystem (bennett-quantum)

Current state only. History is in `worklog/` and `docs/process-watch.md`; per-repo state in
each repo's `HANDOFF.md`. Rules: each repo's `CLAUDE.md`; council: `docs/council/README.md`.

## 2026-10-31, ~14:30Z

**Running**: isa-ref round 18 (astra alone; first round on structured `steps` blockers, proofs as
context); ISA 0.9 editorial pass (sol; folds the 4 proof-derived defect beads and the 15-gap task
into the draft with `[deps:]` markers); ISA main gate push (background, >10 min); statement-layer
build in bennett-conformance (opus). Process watcher every 8 h (next 14:50Z).

**Landed today**: interpreter rounds 12-16 (353 -> 390 tests; single declarative metadata schema);
ISA main pushed through its gate (1b6e3cb; both crates green); §11.1 complete: 219 recipes, library hash fcb2f1e6…f5ce bound in §11.1, Rust = Python
(independently re-run by the orchestrator), all 8 REF beads + parent 8r4 closed; K21-K28; bennett-conformance clause graph, neutral suite, pre-push gate, four structured
proofs (4 refuted 0.8 steps filed as beads in bennett-isa-spec); process watcher + first entry, all
7 verdicts applied; council: one reviewer on fix rounds, one commit per round, severity dropped,
Lamport-structured blocking items (`steps`, ASSUMED step 1 = spec gap), proofs as standing
`--context`.

**Next**: collect round 18 (astra alone; first round on the structured schema, add
`--context ../bennett-conformance/proofs/INDEX.md` and `proofs/INV-*.md`); if accept -> sol
acceptance vote -> interpreter leaves the loop; then re-import suite cases from the accepted
snapshot. Verify the §11.1 completion (library hash Rust = Python; §11.1 marker written). Dialect:
muse's 0.2.10 vote waits on the maintainer; the 0.1-narrowing epic (b-dialect-spec-8wf) is the
next new material. Held: circuits M4, plugin M1 third pass, north-star round 7, targets gate.

**Quota**: Codex unconstrained (banked resets). Claude-side children Opus/Sonnet/Haiku; Fable lean.

**Push state**: bennett main, ISA main (gate green; hook >10 min, run in background), dialect main,
conformance main all pushed.
