# bennett-targets quality audit 2026-11-07

Audited origin/main: `a8f5089d6ed3ed2ce6fd9f4e0844c563971554b5`.
Main-checkout HEAD: `ccb29c5fa2c9298c178763213bd7642ca2f4c508` (one commit ahead).
`git diff --stat origin/main HEAD` shows only `.beads/issues.jsonl`; audited source, tests, fixtures and configuration are identical.
Recorded: 2026-11-07T10:38:46Z. No source edits, commits, Beads operations, full gates or consumer engine runs.

## Verdict

- Code **B+**: exact arithmetic and contextual rejection are sound in the exercised paths; JSON-based dispatch and five large functions retain maintenance cost.
- Tests **B+**: 83 Rust tests exercise published witnesses, independent simulations, negative paths and real importer samples; pinned native-model conformance remains incomplete.
- Build **A-**: cold build 8.11 s, fresh mirrored default 0.28 s; one integration binary and bounded memory make the default loop practical.
- Target provenance **B**: every numeric path has an exact ledger check, but all four target models remain illustrative (`targets/ideal-all-to-all.provenance.md:3`).
- External adapters **B**: sourced concrete samples complement synthetic tests; complete QEC/hierarchy reports remain explicit unsupported inputs (`validator/src/importers.rs:45`).

## Composition

Tracked files only, excluding `.beads/`; `cloc --list-file` measured 69 recognized files, 8,581 code/data/document lines.
Three additional listed files are ignored by cloc. Generated caches and audit scratch are excluded.

| Language | Files | cloc code lines |
|---|---:|---:|
| Rust | 23 | 4,978 |
| Python | 8 | 764 |
| Markdown | 18 | 1,728 |
| JSON | 15 | 1,022 |
| TOML | 3 | 66 |
| Shell (two dialects) | 2 | 23 |

| Directory | Files recognized | cloc code/data/document lines |
|---|---:|---:|
| validator/src | 10 | 2,281 |
| validator/tests | 13 | 2,697 |
| scripts | 10 | 787 |
| targets | 9 | 511 |
| importers | 11 | 686 |
| docs | 10 | 1,397 |
| worklog | 1 | 57 |
| root files + validator/Cargo.toml | 5 | 165 |

Module map; LOC below are cloc code lines, including in-file unit tests where present:

| Source module | LOC | Purpose |
|---|---:|---|
| target.rs | 515 | Closed schema, canonical load, native matching, arity and resolved bindings |
| runtime.rs | 418 | Template expansion, quantity conversion, scheduled occupancy/count/time accounting |
| model.rs | 388 | Native-model schema and exact Gaussian-rational verification |
| importers.rs | 304 | Qualtran counts and Azure legacy hardware projection |
| expr.rs | 218 | Exact decimal/rational AST validation and evaluation |
| topology.rs | 171 | Vertex/edge schema, placement, adjacency and vertex limits |
| json.rs | 149 | Duplicate-rejecting JSON parser, RFC 8785 serialization, SHA-256 |
| main.rs | 61 | CLI parsing, file I/O, JSON results and exit codes |
| query.rs | 40 | CLI expression and adjacency queries |
| lib.rs | 17 | Module exports and two public entry points |

Dependencies: six direct Rust crates (`validator/Cargo.toml:8`); 28 Cargo.lock packages including this crate, hence 27 external packages.
Python imports are standard-library/local modules except the optional capture recipe's Qualtran dependency (`scripts/capture_importer_samples.py:17`).
Authorship measured over all 43 commits: all name `tobiasosborne`; trailers/checkpoint subjects identify 11 Codex-only (25.6%),
22 Claude-only (51.2%), one both (2.3%), nine unmarked (20.9%). Unmarked is not evidence of human-only implementation.
Overlapping marker totals: Codex 12/43 (27.9%), Claude 23/43 (53.5%); no claim about generated LOC follows from commit counts.

## Build and test times

Absolute path aliases used below:
`R=/home/tobias/Projects/bennett-workspace/bennett-targets`, `S=$R/.tmp/reaudit-2026-11-07`, `M=$S/mirror/validator/Cargo.toml`.
The original build cache was not reused: audit target directories start empty; Cargo registry/download caches were already available offline.
A byte-identical tracked-file mirror confines checkout-relative test temporary writes to scratch (`validator/tests/cases/cli.rs:64`, `suite_e.rs:262`).
Pinned inputs are supplied by `$S/layout`, symlinked to the main checkout's existing exact-SHA caches; no sibling source code was copied.
The warm rebuild touches only the scratch copy of `validator/src/query.rs`, preserving the main checkout.

| Measurement | Wall seconds | Result / cache state |
|---|---:|---|
| Main-checkout `cargo build --offline --manifest-path "$R/validator/Cargo.toml" -j3` | 8.11 | pass; empty audit target; max RSS 289,776 KiB |
| Main-checkout `cargo test --offline --manifest-path "$R/validator/Cargo.toml" -j3 --no-run` | 19.38 | pass; dev build warm, test-profile dependencies cold |
| Scratch-mirror cold build | 13.88 | pass; empty independent mirror-target |
| Warm build after touching scratch query.rs | 0.19 | pass; dependency cache warm; source recompiled |
| Scratch-mirror cargo test --no-run | 7.86 | pass; dev profile warm; test profile cold |
| Scratch-mirror default cargo test | 0.28 | pass; 83 passed; 4 unit + 79 integration |
| cargo llvm-cov --json | 12.85 | pass; separate initially empty cov-target |
| Python unittest discovery | 2.71 | pass; 18 tests |

All builds/tests used `ulimit -v 8000000`, one Cargo at a time, `-j3`, `--test-threads=4`, `timeout 600`,
headless environment, scratch TMPDIR/CARGO_TARGET_DIR and `systemd-run --user --scope -q --unit=bennett-build-reaudit-targets-<UTC>`.
Each start checks `free -g` available >=6 GB and load <12 initially; after the binding update, load <8 and no `bennett-heavy` scope.
Resource waits are excluded from wall times; updated waits poll every 60 seconds and stop after 30 minutes.
The mirror build and remaining measurements waited for the heavy gate; all completed after a permitted slot opened.
A preliminary warm relocated invocation reused main-checkout Cargo artifacts and their embedded test paths; it is excluded from isolated timing claims.
Its 83 tests passed; checkout-relative temporary files were test-managed. Subsequent isolation uses a distinct target cache.

83 Rust tests: four library unit tests, 79 integration tests, zero main-unit/doc tests; no `#[ignore]`, failures or filtered tests in the full run.
Python discovery passed all 18 tests in 2.71 s (seven pin, nine ratchet, two stable-report tests).
Suite E executes 17 scenarios from the pinned 38-case inventory; 21 are classified published-unavailable, not passes (`validator/tests/cases/suite_e.rs:220`).
The negative marker test checks absent/blank/untracked reasons (`suite_e.rs:260`); all 38 files having upstream unavailable metadata does not mean all 38 are skipped.
Full gate, `scripts/verify.py` and sibling engines were deliberately not run; no present-day consumer agreement or acceptance completion is claimed.

## Coverage

Fresh LLVM executable-line coverage: **94.23% (1879/1994)**; function coverage **90.23% (157/174)**; regions **90.42%**.
Command: `cargo llvm-cov --offline --manifest-path "$M" -j3 --json --output-path "$S/coverage.json" -- --test-threads=4`, through the resource wrapper above.
LLVM totals include in-file unit tests; external integration/support test source is excluded by the tool. Executed lines do not establish all branches or semantic cases.

| Module | Lines covered / total | Line % | Uncovered lines |
|---|---:|---:|---:|
| expr.rs | 192 / 198 | 96.97 | 6 |
| importers.rs | 217 / 236 | 91.95 | 19 |
| json.rs | 121 / 127 | 95.28 | 6 |
| lib.rs | 9 / 9 | 100.00 | 0 |
| main.rs | 45 / 49 | 91.84 | 4 |
| model.rs | 323 / 351 | 92.02 | 28 |
| query.rs | 33 / 33 | 100.00 | 0 |
| runtime.rs | 350 / 372 | 94.09 | 22 |
| target.rs | 434 / 455 | 95.38 | 21 |
| topology.rs | 155 / 164 | 94.51 | 9 |

Coverage reaches every Rust source module. Structural mapping independently confirms expression tests -> expr, canonical tests -> json/lib,
contract/native tests -> target/model, runtime tests -> expansion/conversion/aggregation, target09 -> topology, importers -> adapters,
and subprocess CLI tests -> main/query (`validator/tests/cases/cli.rs:112`, `cli.rs:151`).
Largest Rust gaps by uncovered executable lines: model 28, runtime 22, target 21, importers 19, topology 9.
Zero-count regions include duplicate-scheme-name diagnostics (`validator/src/target.rs:219`) and malformed leaf class-count diagnostics (`validator/src/topology.rs:118`).
LLVM function totals include closures/generated functions and differ from the source-level declaration count below; branch coverage was not measured.
Python `coverage.py` is unavailable; Python scripts are excluded from the Rust percentage, not silently counted as covered.

Five areas needing broader tests or an external oracle:

1. Native-model transcendental/positive-error semantics: structural admission and parameter propagation are tested, but sin/cos/sqrt/exp return undecided in the rational evaluator (`validator/src/model.rs:108`, `model.rs:297`); checker reconstruction is explicitly outside this validator.
2. Azure Majorana and hardware variants: one synthetic Majorana success/rejection test (`validator/tests/cases/importers.rs:154`); the sourced Azure sample is GateBased only (`importers.rs:261`).
3. Adversarial aggregation: the 32-schedule quarter-second oracle is real (`validator/tests/cases/runtime.rs:345`), but rejection branches for overlapping gates, malformed coverage and duplicate ownership remain less broadly sampled (`validator/src/runtime.rs:315`, `runtime.rs:340`, `runtime.rs:361`).
4. Consumer verifier: 359 raw lines and multiple executor comparisons (`scripts/verify.py:78`); only pin/report helpers are unit-tested, and audit rules exclude the consumer run.
5. Capture/retrieval and unsupported importer envelopes: capture is 56 raw lines without a default execution test (`scripts/capture_importer_samples.py:15`); three real fixtures cover one Qualtran workload and one Azure report, not the whole upstream schema.

## Test quality

Reproducible random sample: `random.Random(20261107).sample(all_rust_tests, 20)`, enumerated by `git ls-files` order and source order.
Locations below name function declarations; all were read. Useful includes assertion-backed positive admission tests, not only rejection tests.

| Test (validator/tests/cases/) | Classification | Reason |
|---|---|---|
| target09.rs:118 exact_entry_must_not_use_eps_decade_even_through_a_table | useful | Literal and table-resolved zero distinguish schema-time and request-time epsilon rules |
| review_round2.rs:488 exact_identity_rotation_models_remain_valid_at_zero | useful | Keeps valid direct/controlled/template +I admission and exact zero parameters |
| runtime.rs:145 imported_quantity_conversion | useful | Huge heterogeneous exact factors, resource merging and three named failures |
| canonical.rs:4 suite_e_all_target_bytes_and_hashes | useful | Seven published byte fixtures and independently pinned SHA-256 anchors |
| importers.rs:42 azure_times_and_errors_are_never_silent | useful | Gate-time overlay plus field-specific out-of-range and unsupported-input rejection |
| target09.rs:223 every_operand_pair_needs_an_edge | useful | Names the missing 0-to-3 edge in a three-operand non-clique |
| review_round2.rs:227 native_operand_arity_is_checked | useful | Seven invalid arities, positive inherited controls, and invalid template CX |
| pins.rs:107 pinned_sibling_rejects_mismatched_head_in_both_layouts | useful | Real temporary commits; expected/actual SHA and both paths must appear |
| models.rs:57 models_are_canonical_and_have_provenance | useful | All four canonical models checked against exact path-keyed numeric ledgers |
| cli.rs:112 cli_queries_reject_malformed_fields_with_json_diagnostics | useful | Subprocess exit/stdout and exact JSON diagnostics for malformed queries |
| target09.rs:100 eps_decade_cost_charges_requested_share_not_achieved_epsilon | useful | Separates requested 0.01 cost from achieved 0.001 error |
| target09.rs:207 adjacency_is_the_published_outcome | useful | Published infeasibility code plus valid, duplicate and missing vertices |
| cli.rs:77 cli_reports_the_published_topology_and_eps_decade_outcomes | useful | Executes success/failure queries and exact 11/10 arithmetic through the binary |
| target09.rs:233 absent_topology_is_all_to_all | useful | Large distinct vertex indices succeed without topology; aliasing still rejects |
| target09.rs:147 published_topology_witness_loads_with_its_published_hash | useful | Fixed published digest detects canonical-byte drift |
| review_round2.rs:588 template_model_uses_the_leaf_angle_instead_of_the_scheme_angle | useful | Zero Rz leaf inside theta=3/4 scheme catches parent/leaf binding confusion |
| target09.rs:135 eps_decade_only_where_eps_is_bound | useful | Rejects epsilon-indexed table use in QRAM context without eps |
| review_round2.rs:50 placement_must_match_the_resolved_operand_class | useful | 100x fast/slow timing difference and cross-leaf placement aliasing |
| importers.rs:199 azure_qec_formula_inputs_name_the_missing_contract | useful | Unsupported real capability fails with field, QEC and ISA context |
| review_round2.rs:328 exact_resolved_model_context_does_not_bind_eps | useful | Same variable-dependent model rejects exact context and admits positive context |

Sample ratio: 20/20 useful (100%), zero weak, zero tautological under these stated test intentions; this is a sample, not a suite-wide percentage.
Additional oracle-backed tests: eight-column independent Toffoli simulator (`models.rs:141`), 16-basis routing check (`target09.rs:301`),
32-schedule discrete occupancy oracle (`runtime.rs:345`), hand-derived rational/matrix identities, real samples and 17 published E scenarios.
No randomized property-testing framework or full VM/reference differential ran in this pass.
Remaining weaker checks include `.is_some()`/`.is_none()` rather than first-entry charges in the published matching case (`suite_e.rs:113`),
and nonempty-string-only CLI argument diagnostics (`cli.rs:142`); surrounding stronger tests help, but those assertions alone do not establish semantics.

The gate's Rust/Python test entries (`gate.toml:21`, `gate.toml:29`) would catch wrong canonical hashes, eps_decade, exact imported rates,
wrong placement classes and the sampled binding/arity defects. Its separate consumer verifier (`gate.toml:37`) attempts executor checks,
but green repository checks explicitly do not imply all consumers support targets (`README.md:40`).

External sample provenance was checked separately from adapter correctness. A fresh HTTPS fetch of the
[pinned Microsoft artifact](https://raw.githubusercontent.com/microsoft/qdk/e5d6dbeabc5b4fcb557269c7aa37a03c79ae4e85/source/resource_estimator/src/system/test_report.json)
returned 33,803 bytes, byte-identical to the checked-in report; SHA-256 is `52ef97bca37dc9739b82683a2c17214dc8aecf5bdab6c74f5c8f6df9d7263f2a`.
All three fixture files match their metadata hashes. The Qualtran fixture records version 0.7.0 and a concrete QFT(8) recipe
(`importers/fixtures/qualtran-qft8-real.provenance.json:3`); its previous capture environment is absent, so this pass did not regenerate it or install dependencies.
This is stronger evidence for Azure's external origin than for independently re-executed Qualtran production; neither sample is physical hardware measurement.

## Code quality

No newly confirmed P0/P1 finding; previous native-model findings and fixes are recorded in `docs/reviews/2026-11-06-quality-targets-r1.md:13`,
`2026-11-06-quality-targets-r2.md:14`, and the CLEAR recheck `2026-11-06-quality-targets-r3.md:12`; their current regressions were included in the default run.
The pin-layout repair is recorded in `docs/reviews/2026-11-06-targets-gatefix-r1.md:5`.

| Finding / remaining cost | Evidence | Effect / status |
|---|---|---|
| P2: oracle pin predates native-model K86 | gate.toml:42; docs/quality.md:333; docs/reviews/2026-11-06-quality-targets-r3.md:64 | Native-model tests use accepted-contract handwritten fixtures; updating pin/oracle remains open |
| P2: stale tracked progress context | docs/PROGRESS.md:1, :14, :21 | Claims sixteen executable scenarios and outdated counts; current suite requires seventeen |
| P2: repeated string AST dispatch | validator/src/expr.rs:107, :190; validator/src/model.rs:75, :95 | Operators validated and redispatched during evaluation; maintenance and repeated traversal cost |
| P3: cache-only README claim | README.md:55; scripts/gate_pin.py:17 | Omits supported explicit layout; already recorded by gatefix review |
| Diagnostic/typing boundary remains mutable | validator/src/target.rs:60; validator/src/importers.rs:280, :300 | Public document can invalidate load-time guarantees; importer unwraps assume valid base, unlike hardened runtime paths; no malformed-base panic probe run |

Measured by the repo lexer/AST script plus an independent brace-span/nesting scan: 75 production Rust functions, five >100 lines, zero >300.
Whole tracked Rust/Python tree: 239 functions, complexity-proxy mass 1,518, one forwarding wrapper; Rust src mass 1,041 includes its four tests.
Maximum lexical brace depth is 10 in expand (includes closures/match braces; not a control-flow AST metric).

| Longest production function | Declaration | Lines | Max lexical brace depth |
|---|---|---:|---:|
| schema | validator/src/target.rs:88 | 220 | 6 |
| aggregate | validator/src/runtime.rs:231 | 191 | 5 |
| expand | validator/src/runtime.rs:57 | 151 | 10 |
| realisation_model | validator/src/model.rs:158 | 151 | 4 |
| parse (including nested parser methods) | validator/src/json.rs:5 | 107 | 9 |

The parser span contains nested methods; they are counted separately for function totals, matching the metric script's documented convention.
Duplication: short JSON array/object accessors recur across target/runtime/importers/topology; no substantial copied algorithm was identified.
One measured forwarding wrapper is the public `Target::native` compatibility entry (`validator/src/target.rs:378`), not evidence of an unused interface.
The multi-argument internal matcher still suppresses Clippy's argument-count lint (`target.rs:388`); resolved request data could become a struct.
No contradictory state-flag bundle or duplicated cleanup protocol was found in the central Rust paths read.
No dead Rust module was found structurally; the three formerly unreferenced illustrative fixtures are now listed in the consumer harness (`scripts/verify.py:242`).
Runtime lock/backup/cache grep is clean except legitimate Cargo.lock; the broader progress-file grep has exactly `docs/PROGRESS.md`.
Fresh `python3 -B "$R/scripts/quality_ratchet.py" --root "$R"` passes for 31 source files, one allowed legacy litter path and zero product process identifiers.

## Against the 2026-11-05 baseline

Baseline report and ecosystem SYNTHESIS both grade code B, tests B-, build unmeasured. Grades below are re-derived from this pass.

| Dimension | Baseline | Now | Evidence and one step upward |
|---|---|---|---|
| Code | B | B+ | Exact/contextual failures and bounded function sizes; A- needs a firmer validated-document boundary and typed AST/request representation |
| Tests | B- | B+ | Executed 83 tests, strong independent examples and real samples; A- needs broader Majorana/adversarial scheduling cases and published K86 oracle coverage |
| Build | unmeasured | A- | 8.11 s cold build and 0.28 s default; A needs default tests to honor TMPDIR without checkout-relative writes/mirroring |
| Target provenance | C+ | B | Path/exact-value ledger plus honest illustrative scope; B+ needs independently sourced hardware numbers |
| External adapters | D | B | Real concrete outputs, projection identity, defaults and errors tested; B+ needs another upstream model/format variant |

| Baseline finding / recommendation | Status | Current file:line evidence |
|---|---|---|
| Provenance test merely greps illustrative (recommendation 1) | fixed | validator/tests/cases/models.rs:26 parses ledgers; :57 checks all models; :76 mutates drift/missing/swapped paths |
| Three sidecars cite ISA 0.8 (recommendation 2) | fixed | targets/ideal-all-to-all.provenance.md:6; superconducting-grid-illustrative.provenance.md:6; trapped-ion-illustrative.provenance.md:6 cite 0.9; models.rs:27 enforces it |
| No sourced hardware value / incomplete numeric ledgers | partly | targets/ideal-all-to-all.provenance.md:32 now covers every numeric leaf; :3 still explicitly hand-derived, not physical measurements |
| No real Qualtran or Azure sample (recommendation 3) | fixed | validator/tests/cases/importers.rs:209, :261, :320; three real .provenance.json sidecars include URL/date/hash |
| Digit-only adjacency / vague unit check (recommendation 4) | fixed | target09.rs:223 requires exact missing pair; importers.rs:99 requires exact base-time-unit diagnostic |
| Missing vertex-limit defaulted to 0 (recommendation 5) | fixed | validator/src/runtime.rs:386 errors with class context; tests/cases/runtime.rs:334 requires exact diagnostic |
| Input-derived runtime unwraps (recommendation 6) | fixed | validator/src/runtime.rs:104, :180 return errors; tests/cases/runtime.rs:281, :298 reproduce mutated input paths |
| Tracked locks and .darc (recommendation 7) | fixed | .gitignore:21; tracked-files scan finds none of the runtime locks/backups; Cargo.lock is intentionally retained |
| Azure Majorana / Qualtran sparse adapter tests | partly | importers.rs:154 covers Majorana; :209, :261 add sourced GateBased/count cases; no sourced Majorana variant |
| Aggregate lacks independent oracle | fixed | validator/tests/cases/runtime.rs:345 quarter-second sampler differs from runtime.rs:325 endpoint sweep |
| ideal matrix table lacks direct checks | partly | validator/src/model.rs:364 verifies X/S/Sdg/CZ/SWAP basis columns; transcendental verification still outside exact fragment (:108) |
| query.rs no direct tests | fixed | validator/tests/cases/cli.rs:112 executes malformed queries; :77 covers successful eval/adjacency |
| Three illustrative fixtures dead | fixed | scripts/verify.py:242 references all four originals; default Rust tests still use inline synthetic variants |
| Trivial schema/optional-params probes | partly | validator/tests/cases/contract.rs:4, :32 retain narrow checks; :45 adds field-specific invalid-schema cases and review_round2.rs:572 checks template angle cardinality |
| Missing Qualtran default-report assertions | fixed | validator/tests/cases/importers.rs:224 checks each default flag and count |
| Trivial imported multiplication / epsilon-insensitive matching | fixed | runtime.rs:145 now uses huge/mixed rational mappings; :49 changes epsilon share and tests filtering |
| model rational parse unwraps | not fixed | validator/src/model.rs:44 retains unwraps after complete canonical integer checks at :32; no demonstrated panic, so no demanded repair |
| Importer self-built JSON unwraps | not fixed | validator/src/importers.rs:280, :300 still assume validated base; public mutability is a documented audit limit above |
| Product bead references | fixed | validator/src/model.rs:1 no old bead IDs; fresh tracked production metric reports zero |
| Long functions and matcher lint suppression | partly | five >100, zero >300; target.rs:388 internal matcher still has eight positional arguments |
| Unmeasured nesting/duplication/wrappers | fixed | Fresh span scan finds depth 10; ratchet records 239 functions/one wrapper; duplication reviewed qualitatively |
| 21/38 E scenarios unavailable | not fixed | validator/tests/cases/suite_e.rs:220 records them honestly; no disabled tests are presented as new semantic coverage |
| Source-pinned inputs (synthesis-wide concern) | fixed | validator/tests/support/pins.rs:31, :68 and scripts/gate_pin.py:17, :29 check explicit-layout/cache HEAD; no live fallback |
| Remaining stale/WIP context (synthesis-wide concern) | partly | HANDOFF.md removed and README.md:7 links ecosystem handoff; docs/PROGRESS.md:1 remains |

No baseline regression was identified. The baseline was not a reproducible timing/coverage run and did not record a SHA;
its 49-test and authorship numbers are historical claims, not a rerun of an exact baseline tree.

## Plan targets

Commands use the resource wrapper above and absolute path aliases. These are this repository's contributions to the programme targets, not ecosystem-wide completion.

| Applicable target | Met? | Command / result and evidence |
|---|---|---|
| Default main tests green | met | cargo test --offline --manifest-path "$M" -j3 -- --test-threads=4: 83 pass, zero ignored/failures |
| No test reads live sibling instead of pin | met | Source scan plus full pin regressions; actual ISA/VM cache HEADs equal gate.toml:42/:53; support/pins.rs:31 selects layout/cache only |
| Measured coverage recorded | met | docs/quality.md:345 records command and :350 records 94.23% (1879/1994); fresh rerun 94.23% line / 90.23% function |
| Default test wall <180 s | met | 0.28 s with warm mirror cache; no slow-test exclusion needed |
| Audit test grade >=B | met | B+; sampled tests and run evidence above |
| Audit code grade >=B- | met | B+; central files read, contextual errors and measured size/nesting above |
| No >300-line semantics function touched by fixes; rest owned | met | Fresh declaration/brace scan: zero production functions >300; longest schema 220 |
| No process IDs in product source/errors/output | met | Fresh quality_ratchet.measure reports process_identifiers={} with product text and filename scans (scripts/quality_ratchet.py:132) |
| No tracked pycache/logs/runtime locks/backups/LAST-RUN | met | git ls-files + metric LITTER scan: no listed artifact type; Cargo.lock is reproducible, not a runtime lock |

Additional round-1 obligations: numeric provenance, sidecar version, real samples and runtime fail-fast changes are met (baseline table).
Consolidation/profile are met (`validator/tests/integration.rs:1`, `validator/Cargo.toml:16`); HANDOFF is retired (`README.md:7`).
The single push ratchet exists and passes (`gate.toml:33`), but broader litter retirement is **not met**: docs/PROGRESS.md remains explicitly allowed.
The quality-targets review reached CLEAR (`docs/reviews/2026-11-06-quality-targets-r3.md:3`); full gate/push status is not independently re-certified here.

## What is good

1. Exact rational costs and import preservation checks reject decimal drift/underflow (`validator/src/importers.rs:16`; tests/cases/review_round2.rs:25).
2. Negative model tests distinguish global phase, evaluated epsilon and actual leaf angles (`validator/tests/cases/review_round2.rs:300`, :444, :588).
3. Provenance checks validate every number by path and detect drift rather than grepping prose (`validator/tests/cases/models.rs:26`, :76).
4. Independent occupancy and basis-state simulators check behavior, not just successful execution (`runtime.rs:345`, `models.rs:141`, `target09.rs:301` in tests/cases).
5. Pin failures name expected/actual commits and never fall back to a live checkout (`validator/tests/support/pins.rs:31`, :68; scripts/gate_pin.py:29).

## Recommendations

1. Select a published K86-bearing ISA pin and add its external vectors; keep current resolved-angle/epsilon regressions (gate.toml:42; docs/reviews/2026-11-06-quality-targets-r3.md:64).
2. Retire tracked docs/PROGRESS.md and update README.md:55 for both resolver layouts; existing review records already track these nits.
3. Broaden Majorana inputs and aggregation rejection cases using field-specific diagnostics and independent expected results (tests/cases/importers.rs:154; validator/src/runtime.rs:315).
4. Preserve valid-document invariants at the library boundary, or explicitly test mutated-base failures in importers before treating unwraps as safe (validator/src/target.rs:60; importers.rs:280).
5. Parse reused AST operators/request context once when those paths next change; do not split the five large functions solely to improve a metric (expr.rs:107, :190; target.rs:389).
6. Add focused consumer-verifier/capture tests and a Python coverage measurement when available; do not count helper-only tests as verifier execution (scripts/verify.py:78; capture_importer_samples.py:15).

JOB-COMPLETE
