# bennett-circuits quality audit 2026-11-05

Repo HEAD a698276, clean tree. Read-only audit; nothing committed.

## Verdict
- Code: C+. Zero dependencies and fail-loud errors, but 1000+ line functions, minified CLI dispatch in `src/main.rs`, and bead/milestone tags in error strings.
- Tests: B. 200 tests, all green. The core is oracle-backed (differential against the ISA reference interpreter, exhaustive basis columns, hand-derived exact amplitudes). About 8% only check "does not error".
- Build: B-. A cold or stale `cargo test --no-run` took 313 s; incremental rebuilds are 12 to 32 s; one test binary needs 6.7 GB RSS.
- Coverage: 84.9% lines measured (excludes the `oracles` test binary, which adds some of `oracle.rs`).

## Composition
| Language / dir | files | code LOC |
|---|---|---|
| Rust `src/` (31 files, 29 modules + main) | 31 | ~18,000 |
| Rust `tests/` (14 files + 5 support) | 18 | ~8,700 |
| Rust total (cloc) | 49 | 26,701 |
| Markdown (docs, worklog, handoff) | 16 | 2,170 |
| Shell (pre-push, hooks) | 9 | 269 |
| JSON/TOML/YAML (beads, config) | 14 | 211 |

Tracked files: 90, of which 17 are tooling litter (`.beads/*` with `pre-push.backup`, `.agents`, `.codex`, `.cursor`). `.tmp/` is gitignored, so the roughly 100 ad hoc `.tmp/*.log`, `.bisa` and `.py` files on disk are untracked and not committed. `target/` is 1.9 GB.

Dependencies: Cargo.lock has 1 crate (the package itself). The JSON codec, SHA-256, bignum and exact dyadic arithmetic are all hand-written (`json.rs` 446, `sha256.rs`, `tests/support/exact.rs`).

Module map (LOC, `wc -l`):
| module | purpose | LOC |
|---|---|---|
| checker.rs | static checker for the ISA object (schema, handles, cleanup) | 2915 |
| object.rs | `.bisa` parse, hashing, symbols | 2054 |
| history.rs | symbolic history / proof-carrying evaluation | 1597 |
| oracle.rs | oracle specialisation and certificate rows | 1571 |
| lower.rs | ISA object to circuit IR | 1436 |
| certificate.rs | certificate replay and verification | 1283 |
| classical.rs | classical (CC/R tier) interpreter | 1212 |
| metadata.rs | certificate and frame metadata | 1076 |
| target.rs | target description parser and expansion | 986 |
| main.rs | CLI | 960 |
| placement.rs | qubit and time placement | 808 |
| linking, flatten, ir, ir_codec, frame, step_check | link / flatten / IR / codec | 359 to 452 each |
| qasm, qir, quil, export | exporters and parsers (OpenQASM 3, QIR, Quil) | 448 / 409 / ~220 / ~180 |
| borrow, amplitude, selectors, translation, coverage, simulation, sha256, json, proof | helpers | 100 to 450 each |

Authorship (59 commits, all authored as `tobiasosborne`): 28 carry a `Co-Authored-By: Claude` trailer (12 name Opus 5.5), 1 carries `Agent: gpt…`, 2 are `wip(codex job` backups, 28 have no marker. Reviews say the unmarked ones are largely Codex (docs/reviews/2026-11-03-circuits-batch.md, "Provenance/R14"). So roughly 47% Claude-marked, 5% Codex-marked, 48% unknown.

## Build and test times
Existing `target/` was warm for most crates, but stale for the test profile.
| step | wall |
|---|---|
| `cargo test --no-run -j3` (first, after stale target) | 313.3 s |
| touch `src/json.rs`, `cargo test --no-run -j3` | 12.4 s |
| touch `src/json.rs`, `cargo build -j3` (dev) | 32.1 s |
| `cargo test -j3 --test-threads=3`, `ulimit -v 8000000` | 160 s, OOM in `oracles` (see below) |
| `oracles` alone, `ulimit -v 14000000`, 1 thread | 98.6 s, max RSS 6.75 GB, 5 passed |
| `cargo llvm-cov` (separate target dir, cold, 14 binaries) | 110.6 s |

Counts: 200 tests (14 lib, 186 integration), 0 ignored, 0 red. Slowest binaries: `oracles` 99 s, `differential` 10 to 13 s, `diagnostics` 2 to 3 s; everything else under 1 s.
`tests/oracles.rs` aborts with `memory allocation of 100663296 bytes failed` under `ulimit -v 8000000`. HANDOFF.md:75 says "roughly 5GB RAM", measured 6.75 GB. This is an environment cap hit, not a defect, but the 5 GB claim is low.
`gate.toml` runs plain `cargo test --offline`, with `CARGO_TARGET_DIR` set to `.tmp/gate-target`.

## Coverage (measured, cargo llvm-cov 0.9.1, src files only)
Lines 84.86% (18,021 total, 2,729 missed). Functions 77.2% (1,588 total, 362 missed). Regions 81.2%. This excludes the `oracles` binary (OOM-capped, not run under llvm-cov), so `oracle.rs` is slightly understated.

| file | line cover | note |
|---|---|---|
| main.rs | 65.4% | CLI, 1718 regions; run-program, schedule, target paths |
| linking.rs | 72.8% | |
| ir.rs | 72.8% | |
| step_check.rs | 73.6% | |
| oracle.rs | 74.3% | (w/o `oracles` test) |
| target.rs | 76.8% | target parser |
| simulation.rs | 78.9% | |
| json.rs | 79.8% | hand-written codec |
The five weakest by line cover are main.rs, linking.rs/ir.rs, step_check.rs, oracle.rs, target.rs. Well covered: sha256 100%, amplitude 96.9%, selectors 96.8%, placement 95.4%, flatten 95.8%, quil 94.6%.

## Test quality
All 172 `#[test]` fns scanned; 14 have no assert/unwrap_err/is_err at all (they pass if nothing panics): `tests/proof_output.rs` (5: `interface_only_symbolic_loops…`, `symbolic_while_flags…`, `borrow_frame_domains…`, `existing_exact_quantum_cancellation…`, `program_relation_compatibility…`), `tests/static_checker.rs` (4, e.g. `matched_cleanup_crosses_cfg_edges…`), `tests/diagnostics.rs` (4 suite_*), `tests/exporters.rs` (1). Some of these assert inside helper functions, so 14 is an upper bound.

Sampled tests (file:line, class, why):
| test | class | why |
|---|---|---|
| tests/proof_output.rs:30 `legacy_certificate_must_replay_false_program` | useful | regression for a P0 false-certificate acceptance, asserts exact error |
| tests/proof_output.rs:39 `legacy_certificate_replays_valid_programs…` | useful | positive plus per-field tamper loop |
| tests/proof_output.rs:598 `symbolic_histories_include_control_contexts…` | useful | good/bad ordering mutation must raise "§6.2" |
| tests/proof_output.rs:1084 `interface_only_symbolic_loops…` | weak | `.hash().unwrap()` only; shows no wrong result would be caught |
| tests/proof_output.rs:1420 `symbolic_while_flags_keep_indexed_selectors_current` | weak | `.hash().unwrap()` only; name promises more than checked |
| tests/classical.rs:25 `signed_const_must_execute_modulo_width` | useful | literal expected values, widths 1 to 128, both directions |
| tests/simulator.rs `exact_cancellation_and_tiny_support` | useful | exact dyadic algebra, tiny-angle nonzero |
| tests/simulator.rs `matrices_and_relative_global_phase` | weak | f64 tolerance 1e-15 against 1/sqrt2, trivial 1-qubit |
| tests/placement.rs:56 `sequential_clean_lifetimes_reuse_one_slot…` | useful | hand-derived exact phase, asserts slot map and determinism |
| tests/lowering.rs:107 `qloop_unrolls_and_bell_adjoint_reverses` | useful | structural, expected gate lists hand-written |
| tests/lowering.rs `every_fixture_action_lowers` | weak | "lowers without error" over fixtures |
| tests/exporters.rs:57 `all_gates_controls_polarities…roundtrip` | useful | export, parse, simulate, compare exact states, but self-consistency |
| tests/exporters.rs:73 `executable_mutations_are_seen…` | useful | mutates text, expects parse failure or gate change |
| tests/exporters.rs:120 `external_llvm_assembler_and_verifier_accept_qir` | oracle-backed, soft | runs `llvm-as-18` and `opt-18 -passes=verify`; both installed here so it ran; if absent it returns Ok silently |
| tests/exporters.rs `every_gate_every_control_polarity…` | weak | no assert in the body; asserts live in `same_states` |
| tests/qasm.rs:6 `fixture_roundtrips_and_executable_text_agrees` | mixed | roundtrips own parser; `assert_eq!(actions, 18)` pins corpus size |
| tests/differential.rs:84 `every_action_every_basis_matches_run_action` | oracle-backed | all bases, all exporters, vs `bennett-isa-ref run-action` |
| tests/oracles.rs:63 `every_oracle_matches_cli_on_basis_tuples` | oracle-backed | vs reference CLI |
| tests/check_agreement.rs | oracle-backed | checker verdicts vs `bennett-isa-ref check` |
| tests/static_checker.rs | oracle-backed | ISA conformance cases A to H, version-selected |

Ratio (sampled 20): 11 useful, 4 oracle-backed, 5 weak, 0 purely tautological.

Oracle-backed: `differential`, `oracles`, `check_agreement`, the F/D/G/H conformance suites in `static_checker` and `diagnostics`, `proof_output.rs:354` (`certificates_replayed_against_reference_cli`). Self-referential: all exporter tests except the LLVM one, since QASM and Quil are validated only by the crate's own parsers (`qasm::parse_flat`, `quil::parse_flat`). No Qiskit, pyquil or OpenQASM parser is used anywhere (qiskit is not installed). Only QIR is checked externally (`tests/exporters.rs:120`). The simulator the exporters are compared against (`tests/support/sim.rs`) is also the crate's own, but it is cross-checked against the reference interpreter in `differential`. So export fidelity is validated semantically, yet nothing proves an external tool reads the QASM or Quil.

Pin versus live (the `d2fd693` bug): tests still read the LIVE sibling by relative path (`../bennett-isa-spec/...`) in 11 test files (e.g. `tests/lowering.rs:17`, `tests/static_checker.rs:8`, `tests/differential.rs:21`). Live isa-spec is be109bd; the gate.toml pin is ecaaac0. The gate runs the pinned layout (`gate.toml` `[siblings]` plus build). What d2fd693 changed is that `tests/support/corpus.rs` selects cases by the `isa=` in the object header against `SPEC_VERSIONS.toml`. That is a tolerance fix, not a pin read, and it holds: this audit ran against live be109bd and `diagnostics` 7/7 and `static_checker` 40/40 passed. `differential.rs:46` still asserts exactly 2 spec examples, so a spec edit adding an example would fail the test. Fragile; no sign it is a P0.

Gate catches a wrong result? Yes for lowering, placement and certificates (differential on exhaustive bases plus conformance corpus). It does not catch a wrong QASM or Quil dialect interpretation, nor `oracles`-only regressions if the test runs on a machine below 7 GB (OOM, loud).

## Code quality
Complexity hotspots (longest fns, scripted brace match):
| fn | file:line | LOC |
|---|---|---|
| `evaluate_body` | src/history.rs:441 | ~1157 |
| `execute` | src/classical.rs:445 | ~538 |
| `classical_schema` | src/checker.rs:2383 | ~481 |
| `row` | src/oracle.rs:534 | ~461 |
| `specialise_impl` | src/oracle.rs:1208 | ~364 |
| `schema` | src/checker.rs:181 | ~329 |
| `static_parameter_action` | src/checker.rs:1949 | ~306 |
| `place_target_program` | src/placement.rs:249 | ~303 |
| `verify` | src/certificate.rs:999 | ~285 |
| `certificate_mode` | src/metadata.rs:736 | ~269 |

Findings against rule 9 and fail-fast:
1. Minified CLI dispatch: `src/main.rs:895-909` crams parsing, I/O and error construction onto single lines of 200+ chars (22 lines over 200 chars in src, 10 in main.rs). Cost: review and edit errors are likely; rustfmt apparently excluded here.
2. Bead and milestone tags in user-facing error strings (rule 9 "bead references left in source"): `src/metadata.rs:352,955`, `src/main.rs:859,897,909`, `src/linking.rs:244`, `src/history.rs:22`, `src/proof.rs:242`. 43 such matches in src. Scenario: tag rots after bead closure.
3. `unimplemented:` errors (58 lines in src) are loud, but several guard published features: `src/main.rs:859,909` reject `schedule` and `run-program --schedule` outright, and `main.rs:897` `--target` launch. These are tracked as deferrals; `main.rs:859` and `linking.rs:244` cite an "unpublished expansion library", so the North Star (rule 10, no narrowing) depends on an external blocker. I did not verify the blocker claim.
4. Long hand-built state keys: `src/checker.rs:2398` dedups worklist by `format!("{bi}:{types:?}:{handles:?}:{viewed:?}")`. O(n) string formatting per visit, with Debug formatting as identity.
5. `let _`, `.ok()` and `unwrap_or*` in src: 89 matches (not each reviewed). Sample: none found hiding errors in the places read, but `src/main.rs` was not exhaustively read.
6. Duplicated test scaffolding: the `object(body)` helper (identical Symbol construction) is copied in `tests/classical.rs:6`, `tests/proof_output.rs:6`, `tests/placement.rs:14`; the object header string appears in 8 test files. `tests/support/` has 5 helpers but none of this.
7. Clone density: `.clone()` count history.rs 124, checker.rs 119, oracle.rs 108; the checker and history engines copy owned strings throughout (performance cost, not a defect found).
8. Tracked litter: `.beads/hooks/pre-push.backup`, `.agents/`, `.cursor/`, `.codex/` (17 files). Policy rule 9 names tracked WIP litter; these are config, not WIP, so minor.
9. Lonely interface candidates: `pub fn version()` in `src/lib.rs` has a test and (apparently) no other user; `mod metadata`, `selectors`, `translation` are private, fine. Not verified with a full callgraph.
10. `src/lib.rs` `Error(pub String)` is the sole error type: every failure is a string, so tests must match substrings ("tuple mismatch", "§6.2", `b-isa-spec-8r4`). No variant to match on. Tests at `tests/static_checker.rs:921,943` and `tests/target.rs:412` assert on a bead-ish id substring.

Dead code: none measured beyond the 362 uncovered functions (22.8%); not triaged. Duplication: not measured with a tool.

## What is good
- Zero crates: nothing to audit, offline build works, `cargo test --offline` in the gate.
- `tests/differential.rs:84`: every action x every basis column x 3 exporters x 3 target configs vs `bennett-isa-ref run-action`. A wrong result is caught.
- Exact arithmetic in tests (`tests/support/exact.rs`, dyadic amplitudes) with hand-derived phases, e.g. `tests/placement.rs:56`.
- Regression discipline: each P0/P1 from the 2026-11-03 review has a named test with literal expectations; Round 2 in the review doc verifies this and I confirmed the tests still pass.
- Corpus selection by declared isa (`tests/support/corpus.rs`) with a self-test, instead of a name list.

## Recommendations
1. Make `tests/exporters.rs:137` fail when `llvm-as-18` is missing instead of returning Ok, and add one external QASM/Quil parse (Qiskit `loads` or pyquil) as a skippable-but-reported check.
2. Replace the 14 assert-free tests (list above) with assertions on a result value or an expected error.
3. Run `cargo fmt` on `src/main.rs` and split the dispatcher in `run`; the lines at 895-909 are unreviewable.
4. Break `history::evaluate_body` (1157 lines), `classical::execute`, and `checker::classical_schema` into per-opcode functions.
5. Move the duplicated `object()` helper and header string into `tests/support/` (one place for the ISA/object versions).
6. Strip bead ids from error text (`metadata.rs:352,955`, `main.rs:859,897,909`) and move them to a stable `E_` code.
7. Update HANDOFF.md:75 (5 GB to 7 GB) and give `oracles` its own gate step with a memory note; fix `differential.rs:46` to not hardcode "2".
