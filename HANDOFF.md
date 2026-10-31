# HANDOFF — Bennett ecosystem (bennett-quantum)

Current state only. History is in `worklog/` and `docs/process-watch.md`; per-repo state in
each repo's `HANDOFF.md`. Rules: each repo's `CLAUDE.md`; council: `docs/council/README.md`.

## 2026-10-31, ~08:30Z

**Running** (orchestrator thread): isa-ref council round 13, acceptance vote, sol + astra on
snapshot 932f19b (365 tests, 5 sweeps); ISA 0.9 §11.1 contract completion + ref-catalog
resume (sol editor, `spec/` + `conformance/`); Opus proofs child seeding
`bennett-conformance/proofs/` (INV-1..4 against clause IDs). Process watcher scheduled every
8 h (next 14:50Z); verdicts are relayed verbatim, acted on only on the maintainer's word.

**Landed today**: interpreter round-12 fixes (76714aa, 054bb7e, b76c6a9; 353→365 tests);
`bennett-conformance`: clause graph (`clauses/`, ISA-0.8/0.9-draft/DLT-0.2.10, anchored
closure default), neutral suite (`suite/`, 16 cases, 314 runs), pre-push gate running both,
housekeeping; process watcher agent (`.claude/agents/process-watcher.md`) and first entry;
council fix-round policy (`docs/council/README.md`).

**Quota**: Codex unconstrained (banked resets; maintainer 2026-10-31). Claude weekly 42%;
Fable drains 2x Opus, so Claude-side children are Opus/Sonnet/Haiku and Fable turns stay lean.

**Next, in order**: collect round 13 (sol, astra) → if both accept, interpreter leaves the
council loop; embed response; re-import suite cases from the accepted snapshot. Then remove
the `severity` field from `tools/council.py` (policy). Verify the §11.1/catalog editor (harness
445/0, `ref_call_flag.rs` green through the contract, library hash Rust = Python). Dialect:
muse's 0.2.10 vote waits on the maintainer; the 0.1-narrowing epic (b-dialect-spec-8wf, 11 P0
children) is the next new material and gets a two-seat round. Held: circuits M4 (3a12d9e),
plugin M1 third pass (re-pin to dialect 0.2.10), north-star round 7, targets gate decision.

**Push state**: bennett main pushed after each milestone; ISA goes to
`wip/ref-library-2026-10-30` with `--no-verify` while `conformance/tests/ref_call_flag.rs` is
red by design; dialect main through its gate; conformance main through its pre-push.
