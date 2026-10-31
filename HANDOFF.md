# HANDOFF — Bennett ecosystem (bennett-quantum)

Current state only. History is in `worklog/` and `docs/process-watch.md`; per-repo state in
each repo's `HANDOFF.md`. Rules: each repo's `CLAUDE.md`; council: `docs/council/README.md`.

## 2026-10-31, ~17:00Z

**Running**: isa-ref round 19 (astra alone; re-grade of the R18 fix under INV-5 1.4.3: nested ties
deferred to resolution, SPEC-QUESTIONS 33); **isa-09 round 1** (sol + astra; first council round on
draft 0.9, K1-K61, proofs INV-1..5 and the statement view as context); ISA main gate push
(background). Process watcher every 8 h.

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

**Next**: collect isa-09 round 1 and isa-ref round 19 (astra alone; first round on the structured schema, add
`--context ../bennett-conformance/proofs/INDEX.md` and `proofs/INV-*.md`); if accept -> sol
acceptance vote -> interpreter leaves the loop; then re-import suite cases from the accepted
snapshot. Verify the §11.1 completion (library hash Rust = Python; §11.1 marker written). Dialect:
muse's 0.2.10 vote waits on the maintainer; the 0.1-narrowing epic (b-dialect-spec-8wf) is the
next new material. Held: circuits M4, plugin M1 third pass, north-star round 7, targets gate.

**Quota**: Codex unconstrained (banked resets). Claude-side children Opus/Sonnet/Haiku; Fable lean.

**Push state**: bennett main, ISA main (gate green; hook >10 min, run in background), dialect main,
conformance main all pushed.
