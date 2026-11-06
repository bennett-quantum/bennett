# bennett-sched quality audit 2026-11-05

## Verdict
- Code: C+. Large semantic surface, fail-loud error style, but several 300-745 line functions and one 2277-line `source.rs` carrying the open P0 area.
- Tests: B. 228 integration tests, many checked against the sibling spec's conformance cases and reference interpreter; 3 red (1 stale pin, 2 mid-TDD fixture bug), and the cost model is checked against hand-derived spec values rather than only against itself.
- Build: C. 76 s warm incremental rebuild for a one-file touch, 283 s `--no-run`, 550 s full test run (a 600 s timeout is nearly hit; one test binary takes 310 s).
- Coverage not measured (llvm-cov would exceed the 600 s budget); structural estimate only.

## Composition
cloc (excl. target/.tmp/.git):

| Lang | files | code |
|---|---|---|
| Rust | 80 | 27169 (src 15.5k incl. subdirs, tests ~9.8k) |
| JSON (data/ref-0.9.json, k83-target, docs/conformance-report.json) | 11 | 6329 |
| Markdown | 11 | 1139 |
| Shell/Bash | 9 | 271 |
| Python (scripts/conformance.py) | 1 | 141 |
| C + header (ABI link tests) | 3 | 143 |

Module map (src, LOC): `source.rs` 2277 (source trace: invoke/adjoint/lifetimes), `expansion.rs` 1897 (recipe library compile/simulate), `oracle.rs` 1297 (+ `oracle_{pairs,calls,memory,state,activation}.rs` 1659), `engine.rs` 1151 (+ `engine/error_bounds.rs` 116; class/vertex search, certificate), `object.rs` 1067 (.bisa parser), `target.rs` 842 (cost-AST eval, target loader), `cleanup.rs` + `cleanup/{raw,replay}.rs` 1434, `source/{qinplace,oracle_call,call_graph}.rs` 821, `lproc.rs` 519, `admission.rs` 444, `schedule.rs` 388, `layout.rs` 296, `source_ir/registry` 613, `resources.rs` 198 (peak/qubit-second), `canonical.rs`/`decimal.rs` 376 (JCS, exact decimals), `ffi.rs` 204 (C ABI), `borrow.rs`, `qinplace.rs`, `request.rs`, `ref_contract.rs`, `token_aliases.rs`.
Dependencies: 28 crates in Cargo.lock (serde, serde_json, sha2, ryu-js, num-bigint/rational/traits + transitive). Crate type cdylib+rlib.
Authorship (52 commits, all by one git identity): 32 (62%) `wip(codex job ...)` Codex-authored; 20 (38%) orchestrator/review/beads/gate commits. No human-written source commits identifiable.

## Build and test times
Target cache was warm (existing target/debug). Run with `-j3`, `ulimit -v 8000000`, `timeout 600`.

| Step | Wall |
|---|---|
| Warm incremental build (touch src/lib.rs, `cargo build`) | 76 s |
| `cargo test --no-run` (after that build; test profile opt-level 1) | 283 s |
| `cargo test --no-fail-fast` (all 45 binaries) | 550 s (exit 101) |

Tests: 228 run (225 passed, 3 failed, 0 ignored, 0 `#[ignore]` in tree). There are 0 unit tests in src/; all tests are integration. Slowest binaries: `lifted_regions` 310 s, `normative_objects` 42 s, `lifted_cleanup` 41 s, `oracle_lproc` 33 s, `oracle_allocator` 30 s, `oracle_memory` 22 s. `lifted_regions` alone is 56% of runtime (exhaustive Boolean simulation). Pre-push gate uses `-j4`, 7200 s timeout.

## Red tests: mid-TDD (fdu) vs pre-existing
Working tree is clean; HEAD 95aaca9 is a Codex "session wind-down" checkpoint.

| Test | Cause | Class |
|---|---|---|
| `tests/source_adjoint.rs::self_adjoint_memory_dispatch_keeps_forward_address_and_bit_order` | `trace()` at :59 `unwrap()`s `Err(Arg "§7.2: memoryless objects cannot contain lprocs or interface regions")`: the new test's fixture object is invalid, so the scheduler behaviour is never reached | fdu mid-TDD (red for the wrong reason) |
| `tests/source_adjoint.rs::copy_and_load_replacements_expand_forward_before_source_order_is_reversed` | same fixture error at :59 | fdu mid-TDD (red for the wrong reason) |
| `tests/conformance_inventory.rs:44` `conformance_inventory_records_every_case_and_portable_manifest_without_stale_hashes` | sibling `../bennett-isa-spec` has 557 `case.json`, `docs/conformance-report.json` records 536; the sibling moved past the pin | pre-existing / unrelated to fdu |

The third test in `source_adjoint.rs` (`self_adjoint_bundle_instructions_keep_forward_bit_ordinals`, :116) passes, so the qxor/qexch reverse-order case already holds at HEAD. The P0 in `docs/reviews/2026-11-03-sched-batch.md` (`src/source.rs` `events.reverse()`) is therefore at least partly fixed for the bundle ops; the memory and copy/load cases are untested because the fixtures are broken. Also stale: the review's red `token_aliases` finding (`tests/token_aliases.rs:78`) now passes. The conformance-inventory red is a product of running against a sibling checkout newer than the committed report; the review (`nsy`) already lists the pin disagreement.

## Coverage
Not measured. `cargo llvm-cov 0.9.1` is installed, but an instrumented rebuild plus a 550 s test run cannot fit in the 600 s step limit at -j3 (skipped). Structural estimate: roughly 70-80% of lines reached, since nearly all code runs through `Request::schedule`, `Trace::build`, `Object::parse`, `simulate_basis`. The largest untested or weakest-tested areas:
1. `src/ffi.rs` error and panic paths (204 LOC; 2 test files, `c_link.rs` and `ffi.rs`, happy path plus link check).
2. `engine.rs` search pathologies: exponential class-choice enumeration (`:55-69`, `:290-322`) has no test; the review's P1 `jez` repro is not in the tree.
3. `oracle.rs`/`oracle_pairs.rs` cap-rejection branches (64 MiB, 8192-state): a "narrowing" that tests do not pin either way.
4. `source/call_graph.rs`, `source/oracle_call.rs`: noted "not read" in the existing review; only reached via end-to-end tests.
5. `admission.rs` (444 LOC) has a 127-line test file; the recompute+`call_index` refusal at `:248` is untested as an intended behaviour.
Per-module test-file mapping by grep is unreliable here because most modules are reached through the public API.

## Test quality
Sampled 17 tests:

| # | Test | Class | Why |
|---|---|---|---|
| 1 | canonical_cost.rs:6 `jcs_uses_ecmascript_numbers...` | useful | literal JCS outputs from RFC 8785 rules, including UTF-16 ordering |
| 2 | canonical_cost.rs:~22 `decision_decimals_preserve_all_digits...` | useful | exact digit strings plus property `share*3 <= tiny` |
| 3 | canonical_cost.rs:~35 `published_k12_upward_34_digit_encodings_are_exact` | useful | hand-written 34-digit expected strings (1/3 rounds up to ...334) from the spec |
| 4 | canonical_cost.rs:~62 `expansion_envelope_is_the_published_complete_catalog` | weak | pins a SHA-256 and count 219 of the data file: detects drift, checks nothing semantic |
| 5 | canonical_cost.rs:80 `host_nesting_exhaustion_is_distinct...` | useful | boundary at 258 nesting asserting a specific status |
| 6 | published_vectors.rs:~14 `published_cost_ast_vectors_match_their_exact_outcomes` | useful (external oracle) | evaluates the isa-spec `E-ast-*` case files against `target::eval` |
| 7 | published_vectors.rs:~55 `published_target_hash_and_topology_vectors_are_checked_directly` | weak | per review `b08`, only parses/adjacency; passes with inverted expectations |
| 8 | resources.rs:14 `k12_exact_per_class_rows...` | useful | hand-derived rational (1/3) rows, escape of `%[é]` |
| 9 | resources.rs:52 `scheduled_overlap_sums_demands...` | useful | half-open reuse vs overlap, fixed integer answers |
| 10 | layout.rs:46 `layout_loader_checks_schema...` | useful | table of mutated inputs each with a specific error substring |
| 11 | layout.rs:116 `unsigned_endpoints_are_checked...` | useful | boundary arithmetic |
| 12 | structure.rs:9 `adjoint_calls_preserve_caller_loop_coordinates...` | weak | expected coordinates computed with the same loop shape as the implementation |
| 13 | source_adjoint.rs:116 `self_adjoint_bundle...` | useful | adjoint trace must equal forward trace; relation oracle |
| 14 | source_adjoint.rs:139,170 (2 red) | not evaluable | fixture invalid |
| 15 | admission.rs:~30 (malformed table -> `ScheduleInfeasible`) | weak | asserts status only, not why |
| 16 | gate.rs:15 `push_gate_declares_pinned_siblings...` | weak | tests the config file shape (hex SHA length), not behaviour |
| 17 | differential.rs:~20 `emitted_09_schedule_and_certificate_pass_reference_metadata_admission` | useful (external oracle) | schedules the sibling's fixture and runs the reference binary `bennett-isa-ref check` on the output |

Ratio: 11 useful, 5 weak, 0 purely tautological, 1 not evaluable.

Ground truth for the cost model: it is not only self-checked. Evidence of external oracles: 24 test files read `../bennett-isa-spec` (conformance cases, fixtures such as `accepted-k83-09`, `controlled-action-09`), 7 `Command::new` calls drive the reference interpreter or the C compiler, `k80/k83/published_vectors` replay spec-published vectors, and `resources.rs`/`canonical_cost.rs` use hand-computed spec rationals. The `E` vectors in published_vectors (`E-ast-*`, `E-table-index`) check `target::eval` against published values. Gaps: no property-based or randomised cross-check of the peak/qubit-second sweep against a brute-force counter, and the optimiser/search objective (`engine.rs`) is checked only by hand-built small cases. Dependency: tests panic if the sibling checkout or reference binary is missing (`differential.rs:22` panics with an instruction), so a standalone checkout cannot run the suite; and a drifted sibling already turns `conformance_inventory` red.
Would the gate catch a wrong result? `gate.toml` runs the full `cargo test` plus `cargo fmt --check` with pinned sibling SHAs, so the oracle-backed tests do catch wrong results on the covered vectors. It would not catch the 4 weak E vectors, and the gate itself currently cannot pass (3 red).

## Code quality
Longest functions (quick script over src/):

| Fn | Lines | Where |
|---|---|---|
| `nodes` | ~745 | src/source.rs:1076 |
| `build` | ~685 | src/oracle.rs:613 |
| `compile` | ~582 | src/expansion.rs:1081 |
| `row` | ~516 | src/oracle.rs:96 |
| `candidate` | ~332 | src/engine.rs:473 |
| `qinplace` | ~326 | src/source/qinplace.rs:5 |
| `from_value` | ~308 | src/target.rs:295 |
| `certificate` | ~287 | src/engine.rs:865 |
| `invoke` | ~257 | src/source.rs:671 |

Findings (existing review items not repeated; cited as 2026-11-03-sched-batch.md):
1. `src/source.rs:1076` 745-line `nodes` is untestable in pieces and the site of the K62 P0 history (review `fdu`). A single wrong arm silently changes selectors/certificates.
2. `src/oracle.rs:613`/`:96` two ~500-700 line functions; the hard caps at `:640-666` are in-line magic limits (review `2u4`, a north-star rule 10 narrowing).
3. 155 `unwrap()`/`expect(` in src/ for a library exposed through a C ABI; `ffi.rs` relies on `catch_unwind` to convert them. Fail-fast in spirit, but each one is a panic-in-library on valid-but-unusual input.
4. 10 bead/spec-id references (`bennett-sched-xxx`, `fdu`) in src comments: policy rule 9 litter, small.
5. Weak tests (rows 4, 7, 16) that look like coverage but do not constrain behaviour: "validation theatre" in tests.
6. Tracked non-source litter: `.agents/`, `.cursor/`, `.codex/`, `.claude/`, `.beads/hooks/pre-push.backup`, `.beads/` (tool config) are all committed; `worklog/` and `HANDOFF.md` carry large status prose that the review shows has gone stale (token_aliases).
7. No obvious dead code found by inspection; `cargo build` emitted no warnings in the tail I saw (not exhaustively checked).
8. Duplication: `source/qinplace.rs` and root `qinplace.rs`, `oracle_*` files share names and concerns; the split is by growth rather than design.

## What is good
- External oracles are wired in: spec conformance cases, a reference interpreter, and a C link test (tests/differential.rs, c_link.rs, published_vectors.rs).
- Exact arithmetic discipline (BigRational, upward-rounded 34-digit decimals, JCS) with literal expected strings (tests/canonical_cost.rs).
- Errors are explicit statuses with reason strings, and tests assert on reason substrings (tests/layout.rs:39).
- Test profile uses opt-level 1 with debug assertions and overflow checks, so exhaustive simulations are feasible while still checking invariants (Cargo.toml).
- One written adversarial review with reproduced P0/P1 findings in docs/reviews/.

## Recommendations
1. Fix the `source_adjoint.rs` fixture (:59, memoryless object with lprocs) so the two red tests fail on the real adjoint-order behaviour, then do the fdu change.
2. Regenerate or re-pin `docs/conformance-report.json` against the sibling (536 vs 557 cases), and make the test report the sibling SHA it ran against.
3. Split `lifted_regions` (310 s, 56% of runtime) into a fast default subset and a full run; target a sub-120 s default `cargo test`.
4. Strengthen the 4 weak E vectors (review `b08`) and `gate.rs` so inversions fail.
5. Break up `source.rs::nodes`, `oracle.rs::build`/`row`, `expansion.rs::compile` into tested units.
6. Add a brute-force differential for the peak/qubit-second sweep (`resources.rs`) with randomised intervals.
7. Run `cargo llvm-cov` on a quiet machine (about 15-20 min) to replace the structural estimate above, and prune stale claims in HANDOFF.md.
