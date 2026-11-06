# bennett-conformance quality audit 2026-11-05

## Verdict
- Code: C+. The Rust checker is functionally rich but built from 300-680-line functions, and test code is minified into 300-500 char lines; the checker is a single self-consistent implementation validated mostly against fixtures.
- Tests: B-. Many negative tests (about 75 reject/exhaustive-mutation tests) and one genuinely independent oracle (Python checker-replay, ISA reference interpreter), but one test is red at HEAD and clause coverage is only 36% (proof-tags only; tests are not tagged).
- Build: B. Cold full test build 106 s at -j3, incremental ~5 s, full checker suite 167 s; Python suites 16-38 s each. 21 GB of untracked .tmp.
- Not run (as ordered): ladder gates, differential harness runs, neutral-suite-with-heavy binaries. The cheap neutral suite (16 cases) was run.

## Composition
cloc (excluding target, .tmp, .git; tracked files 1304):

| Language | files | code LOC |
|---|---|---|
| JSON (clause graphs, fixtures, witnesses) | 159 | 408,525 |
| Rust | 69 | 28,851 |
| Markdown | 69 | 18,974 |
| Python | 59 | 13,868 |
| LLVM IR | 33 | 4,510 |
| C | 12 | 632 |
| Shell/TOML/other | ~40 | ~800 |

Top-level modules (non-comment code is less than the wc numbers below):

| Module | Purpose | LOC |
|---|---|---|
| checker/src (30 files) | Rust `bennett-cert-checker` (ISA §12): eval.rs 4597, cert.rs 1860, numeric.rs 1786, object.rs 1711, realisation.rs 1655 | ~21,800 src + ~11,500 tests (36 test files) |
| checker-replay/ | Independent Python replay of exhaustive claims (replay.py 893, action.py 678, oracle.py 529) | 3,625 + 8 test files, 12 witnesses |
| harness/ | Black-box executor differential `bdiff.py` (generate.py 997, engine, shrink, compare) | ~2,500 |
| suite/ | Neutral conformance runner `run.py` + 16 case dirs | 302 + cases |
| clauses/ | Spec clause graph + statement layer (clausegraph.py 2556) | 2,556 + 3 specs of JSON |
| proofs/ | INV-1..6 markdown proofs + tags.json | md only |
| ladder/ | Demo-ladder gates rungs 1-3 (4-8 text only, rung-4 has gate.py) | not run |

Dependencies: checker Cargo.lock has 7 crates (num-bigint, num-rational, num-traits, ryu-js and transitive); Python stdlib only (run with `-I`).
Authorship (134 commits): 103 by the human account (Claude sessions commit under it, not separable), 31 `wip(codex job ...)` checkpoint commits (23%), 2 with `Agent: gpt` trailer. Codex WIP checkpoints sit in main history (e39501e, a8b097d, c690506 are the three newest).

## Build and test times
Warm = my own fresh target dir `.tmp/audit-target` (the repo's target/ was not reused; cold build in it).

| Step | Wall | Notes |
|---|---|---|
| `cargo test --no-run -j3` (cold, new target dir) | 106 s | compiles at HEAD (Nov-03 review noted HEAD did not; fixed since) |
| touch rat.rs, `cargo build` | 1.3 s | bin only, suspiciously fast |
| touch rat.rs, `cargo test --no-run` | 5.5 s | |
| `cargo test --no-fail-fast` full checker | 167 s | slowest binaries: one 103.6 s (2 tests), one 19.7 s, 13.8 s |
| `cargo llvm-cov` (instrumented, incl. build) | 224 s | |
| clauses/tests (113 tests) | 16 s | OK |
| harness/tests (66 tests) | 24 s | OK (fake executors) |
| checker-replay/tests (109 tests) | 38 s | OK |
| suite/tests (23 tests) | 3.8 s | 1 fail: needs `BENNETT_ISA_BINARY` env, not a defect |
| neutral suite `run.py` vs reference interpreter | 1.4 s | 16/16 PASS |

Counts: Rust 272 tests ran (271 pass, 1 FAIL, 0 ignored; `#[ignore]` count in tree: 0). Python 311 `def test_`.
RED: `checker/tests/resource_contexts.rs:476` `a_recompute_cleanup_cannot_be_certified_using_the_two_gate_reverse_trace`: expects overall `unchecked`, gets `verified`. This is a wrong-direction result: a recompute cleanup is certified. HEAD is red, and it was committed in a WIP checkpoint (consistent with the Codex WIP pattern; gate.toml would block a push). `cargo clippy`: ~108 warnings. `cargo fmt --check` is dirty.

## Coverage
Measured with cargo-llvm-cov 0.9.1 over the integration tests (report built after the red test; all test binaries ran):

| Metric | Value |
|---|---|
| Lines | 83.42% (2787 of 16808 missed fns-lines basis; regions 85.18%) |
| Functions | 81.72% |
| Regions | 85.18% |

Weakest areas (line %):
1. `src/fault.rs` 50% lines, 26.7% regions (86 LOC, the error path itself).
2. `src/domain.rs` 69% (resolve_domain is 408 lines; 184 of 594 lines missed).
3. `src/main.rs` 75% (CLI; cli.rs has only 4 tests) and `src/structural.rs` 75%.
4. `src/eval.rs` 76% lines / 74% functions: 970 missed lines in the central 4597-line file.
5. `src/object.rs` 82% (functions 75%): 258 missed lines in the parser, where the open P1 bennett-conformance-eq2 (token spelling) lives.
Python/harness/ladder coverage not measured; gates intentionally not run.

## Clause coverage (what "clauses" means here)
`clauses/` is a clause dependency graph plus a coverage query. `clausegraph.py coverage clauses/ISA-0.8.json --tags proofs/tags.json` (run by me):
- Clauses: 314 total; strong 112 (36%), weak 9, uncovered 193 (61%).
- Statements: 541 total; strong 169 (31%), weak 10, uncovered 362; requirement-kind statements 450: strong 144 (32%).
- The only tags file in the repo is `proofs/tags.json` (INV-1..6). Rust tests and python tests are NOT tagged, so the numbers measure proof coverage, not test coverage. Whole sections report zero: ISA §7.2-7.4, §8.2-8.4, §15, §16.3, §9.3, §13.
- `suite/cases/*/expect.json` carry a `clauses` list in 16 cases covering 28 distinct section-level ids (e.g. ISA-3.3, ISA-4.6); this is section-granular and not folded into the coverage figure. Combining them would still leave most §5-§8 and §12 unmapped.
- Answer: a mapping from clauses to tests exists only for 28 sections via the neutral suite and for proof tags; no per-clause test map. The 36% is an under-estimate of real test reach (the checker tests cite §numbers in names) but nobody measures it.

## Test quality
Questions asked:
- Negative tests: yes, many. `grep` finds 89 test fns named reject/invalid/bad/wrong/mutate/malformed/cannot/not_ and ~200 references to `rejected`/`E_CERT`/`Err(` across 12+ files. Notable: `mutation_sweep.rs` (5 tests), `resource_contexts.rs:378` (every field type and required removal), `control_flow.rs:175` (all sampler fields), `cert_schema.rs` (11), `token_aliases.rs`, `accounting.rs`. Approximately 75 tests deliberately feed invalid certificates and assert specific error codes.
- Is the differential two independent executors? Two separate things. (a) `harness/` `bdiff.py` runs any set of black-box executors (specified `name=path`) and compares pairwise: the recorded run `harness/runs/2026-11-01-seed1.json` has 3 executors, 29,653 JSON pairs compared, 25,797 byte-identical, 57 divergences, 12 oracle failures. So it is executor-vs-executor, not against stored output, but it differentiates ISA implementations, not the checker. Its own tests use `fake_exec.py` stubs. (b) The checker (Rust) vs `checker-replay` (Python, "shares no code") is the real independent pair: `checker/tests/replay_differential.rs` (23 tests) consumes only witness fixtures from replay (stored output, not a live run), and `checker-replay/tests/test_differential.py` goes the other way. Independence is by two implementations written by the same pipeline (Codex+Claude) from the same spec: fine for catching transcription bugs, weak for shared misreadings.
- Native differential (compiled pipeline vs native, UBSan classifiers) is NOT built (README, bead 06p).

15+ sampled tests (random seed 7 over 261 `#[test]` fns, plus python):

| # | test | verdict | why |
|---|---|---|---|
| 1 | procedures.rs:230 normative_through_forwards... | useful | loops exhaustive 4x4 inputs against a parsed normative object |
| 2 | fixed_images.rs:139 conditional_and_sampled_results_cannot_satisfy_unrestricted_proof_requests | useful | negative, label x sampled product |
| 3 | replay_differential.rs:481 table_value_mismatch_needs_realised_target | useful | negative on mutated table |
| 4 | cert_schema.rs:189 unknown_claim_kind_rejected_per_claim | weak | one mutation, hard-coded 64-hex region key |
| 5 | control_flow.rs:175 every_sampler_field_and_seed_position... | useful | exhaustive field x removal sweep |
| 6 | control_flow.rs:549 indexed_bulk_gates_preserve_other_bits... | useful | builds expected truth table from its own formula, but formula is trivial and independent of checker |
| 7 | replay_differential.rs:37 heap_store_load_witness | weak | only checks `evidence` + "16" + "1/256" on a stored fixture; no row-content check |
| 8 | cli.rs:44 cli_missing_option_value_is_usage_error | weak | exit-code smoke only |
| 9 | token_aliases.rs:370 parameter_uniform_structural_proofs... | useful | quantifies partitions; but source is patched by `replacen` at runtime, hard to read |
| 10 | jcs_rfc.rs:46 utf16_sorting... | useful | RFC 8785 vector, external oracle |
| 11 | cert_schema.rs:89 cert_unknown_field_rejected_case_f_cert_schema | useful | uses ISA-repo conformance case object (external fixture) |
| 12 | control_flow.rs:420 qif_lifetime_adjoints_reverse... | useful | regression for gm5, semantic |
| 13 | row_limits.rs:36 reference_storage_limits_precede... | weak | asserts error ordering; exact cause not oracle-checked |
| 14 | resource_contexts.rs:378 exhaust_every_field_type | useful | exhaustive mutation sweep |
| 15 | control_flow.rs:145 sampled_tables_cover_declared_domain... | weak/contradictory | pins behaviour that bead 37u (P1, review 2026-11-03) says is wrong; self-pinning a disputed rule |
| 16 | metadata.rs:231 sizes_beyond_u64_are_host_limits... | useful | boundary values 2^64, 2^128 |
| 17 | mutation_sweep.rs:~77 published_certificate_every_field_type_mutation | weak-useful | `expected()` re-derives the error code from key names (a mini re-implementation), mutation is only "replace with null/true", never a plausible wrong value; pins `assert_eq!(paths.len(),250)` so any schema growth breaks it |

Ratio: 10 useful, 6 weak, 0 purely tautological, 1 questionable (of 17). The checker tests are generally real assertions; the weakness is that most oracles are hand-written expectations or fixtures produced by the same agents, not external.
Oracle-backed: neutral suite (16 cases run against the independent reference interpreter, hashes from `reference-interpreter@ad84e75`), JCS RFC vectors, ISA-repo conformance objects, checker-replay differential, ISA published certificate (`published_certificates.rs`). Self-referential: mutation sweep code mapping, witness `evidence` count tests.
Would the gate catch a wrong result? gate.toml runs `cargo test` for every crate, clause tests, suite tests and the neutral suite against a reference interpreter pinned at a sha. It would have caught the red test above (it is red now). It does not run the ladder gates or harness (heavy). The Nov-03 review's three open checker P0/P1 (890 nested while flag, gm5, 37u) were found by an external reviewer, not by existing tests; I did not verify their current state.

## Code quality
Findings (policy rule 9 and fail-fast):
1. Giant functions: `src/eval.rs:3553 check_replay_inner` 682 lines, `eval.rs:744 exec_row` 656, `src/cert.rs:754 check_certificate` 507, `cert.rs:1284 check_region` 484, `domain.rs:356 resolve_domain` 408, `eval.rs:2049 exec_line` 389. 43 of 471 functions exceed 100 lines. Cost: the P0 found in review (shared `$loopflag` in nested loops, eval.rs:1530) is exactly the bug class these shapes hide.
2. Minified test and source code: 84 test lines and 23 src lines exceed 200 chars; `resource_contexts.rs:476` is a single ~500-char line with 4 statements and `;`. `cargo fmt --check` fails. Cost: unreviewable; review misses are likely.
3. Silent fallbacks: 223 `unwrap_or*` and 209 `unwrap()/expect()` in src. The review (eq2/qfree) already found `unwrap_or_default` giving `proof` on a no-op qfree at 847f851. Not re-audited here.
4. Red test at HEAD (above) committed via Codex `wip(...)` checkpoint; those checkpoints (31) live in main history. Rule-2 says they are only on `wip/<job>` branches: they are on main.
5. Tracked litter: `ladder/rung-4/__pycache__/check_gate.cpython-312.pyc` and `gate.cpython-312.pyc` still tracked (review nit never cleaned); untracked `clauses/DLT-0.2.11-draft.json`, `suite/tests/__pycache__/`.
6. Tests write 2.1 GB into `checker/.tmp/` (ignored by git) and 21 GB sits in repo `.tmp/`; tests leave `tmp*/` dirs, not cleaned.
7. Bead references in source: 0 in src, none found in tests apart from one provenance comment. Good.
8. `main.rs` `--help` exits 3 (nit cnf from review); `fault.rs` half-untested.
9. clippy: ~108 warnings (not categorised).
10. Duplication: `check_replay_inner`/`exec_row`/`exec_line` all dispatch ISA ops; `checker-replay/` re-implements the same logic in Python deliberately (independence), so duplication is by design.

## What is good
- Exhaustive field/type mutation sweeps (`mutation_sweep.rs`, `resource_contexts.rs:378`, `control_flow.rs:175`) give broad negative coverage.
- A genuinely independent second implementation (checker-replay, 109 tests, 12 witnesses) plus a Rust-side differential that links no shared code.
- Neutral suite runs in 1.4 s against an independently built interpreter and is pinned by sha in gate.toml.
- Black-box executor harness with shrinking and recorded run (29,653 pairs, divergences reported, skips counted).
- Measured 83% line coverage with only 7 crate dependencies and zero ignored tests.

## Recommendations
1. Fix or revert the red `resource_contexts.rs:476` test now; main must not carry a certifying-too-much regression.
2. Run `cargo fmt` over checker/ and tests, and split `check_replay_inner`, `exec_row`, `check_certificate` into per-claim/per-op functions.
3. Tag the checker/python tests with ISA clause ids (e.g. `// clause: ISA-4.6`) and feed them to `clausegraph.py coverage` so the 36% reflects tests, not just proofs.
4. Make `mutation_sweep.rs` mutate values (wrong hashes, shifted rows), not just types, and drop the literal `250` pin.
5. Remove tracked `ladder/rung-4/__pycache__/*.pyc`; stop Codex WIP checkpoints from landing on main.
6. Add tests for `fault.rs` (50%) and CLI exit codes in `main.rs` (75%); cover `object.rs` token spelling (eq2).
7. Clean test temp output: 2.1 GB per checker test run in `checker/.tmp`.
