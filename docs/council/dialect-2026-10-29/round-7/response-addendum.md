# Round-7 response addendum — plugin relays, draft 0.2.9

Both relays resolved before round 8. ISA grading target stays 0.8; no north-star
capability narrows and no corpus program changes. Dialect implementation:
`2c718bd6e1931a8ac02eaa8d9e0d82a5842feab9`; final receipts: `aa0f72e`.

- **b-dialect-spec-uxi — resolved (§12.2, §16.3, §23).** Keep G1, G2, … in
  link order, explicitly 1-based. Atomic-nand's lone global becomes G1.
  ISA §9.2 includes the data name and layout leaves in the semantic envelope,
  so the dependent lproc/oracle hashes change too. Regenerated with the Rust
  reference binary, then checked and executed by the checker. The result stays
  code=0, payload=63, steps=16 (0xf0 & 0xcc = 0xc0; complement = 0x3f).
  Internal driver and staged-budget fixtures now follow the same numbering;
  their affected staged identity vectors were regenerated as well.
- **b-dialect-spec-566 — resolved (§21.1, Appendix A/B, corpus runtime/harness).**
  The runtime defaults to the normative ABI 0.2 header; the harness builds and
  selects v0/0.2 variants by module marker signatures, with separate cache keys
  including the normative header. ADJ/COMPUTE receive budget and env in their
  correct positions. Budget traces contain record values, never host addresses.
  Historical corpus cases retain their ABI v0 execution. The unchanged
  descriptor oracle/inplace trace diagnostics still require the ISA executor.

Regenerated interface hashes:

```text
atomic-nand ref 21917fb6f3a0cc9bd14651126bb3fecaadcdccbed30b854170c7ba10741adac4
atomic-nand L1  4b300c0de9ef64684ae9d5e3e010b6c4888d0e60504c9dd95861d02f753e5e5c
atomic-nand G1  e2076ae22078cd264795a96c18f893aff94ffc100ec1480568616b5226a115a7
budget-stage selection_identity 4162aa7c5cf3b7bed36162dd7c0f123e26e0606a8bc118184d9f7acaab0786ce
budget-stage final identity     7486a0aa9e6711325475ffce67d6ec1bb3d4d4ec981eb3b755e171ba04819365
```

| Corpus case | LLVM | llc O0/O3 exit | P2 L1–L6 |
|---|---:|---|---|
| spec-sem2-adj | 18 | 0 / 0 | 11/11 pass/noop |
| spec-sem2-adj | 23 | 0 / 0 | 9/9 supported pass/noop |
| spec-sem2-compute | 18 | 0 / 0 | 11/11 pass/noop |
| spec-sem2-compute | 23 | 0 / 0 | 9/9 supported pass/noop |

All 69 baselines rerun on both majors; the other 67 cases retain byte-identical
O0/O3 canonical traces and unchanged exits/issues. All 1,386 stored P2 outcomes
match (1,518 total cells); LLVM 23's existing Os/Oz refusals and intentional
negative controls remain unchanged. Historical P1/P3 tables were retained.
Corpus machine receipt: `corpus/legality/results/abi-0.2-relays.json`.

**Freeze 2731 → 2732; 2732/2732 passed, zero failed or unavailable.**
76 checker unit tests and 49 non-viewer harness tests pass. Both PROGRESS files
and `scripts/dialect_check.LAST-RUN.json` contain the spec/source/interpreter
fingerprints and full family table. No LLVM view pass, ISA edit or push.
