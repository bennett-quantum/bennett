# bennett-sched quality audit 2026-11-07

## Verdict
- Code: **B-** (baseline C+). Phase extraction and conflict tracking improve maintainability; materialized construction/proof limits and string-dispatched semantics remain substantial debt.
- Tests: **B+** (baseline B). Exact/spec-backed checks, independent occupancy enumeration, pinned reference execution and measured coverage; complete scheduled execution/certificate replay remain unverified.
- Build: **B+** (baseline C). Warm root rebuild 0.80 s, test compilation 50.62 s, default run 23.18 s; one integration binary replaces the old link/runtime bottleneck.
- Audited main checkout `/home/tobias/Projects/bennett-workspace/bennett-sched`, HEAD = origin/main = `3fc4d7bdc399a5c6e3df4cd51ce01c4a040eb2fc`; clean before/after. No code edits, commits, beads or full gates.
- Evidence below is this audit unless explicitly labelled inherited; 2026-11-07T17:13:38Z.

## Composition
All source references below are relative to the absolute repository path above.
`cloc 1.98 --list-file=/home/tobias/Projects/bennett-workspace/bennett-sched/.tmp/reaudit-2026-11-07/tracked-absolute.txt --json --quiet` counted tracked regular files:

| Language | Files | Code LOC |
|---|---:|---:|
| Rust | 82 | 28,215 |
| JSON | 8 | 6,537 |
| Markdown | 14 | 1,303 |
| Python | 6 | 586 |
| Shell/Bash | 9 | 271 |
| C/header | 3 | 143 |
| TOML/YAML | 6 | 74 |
| Total recognized | 128 | 37,129 |

Directory code LOC: `src/` 16,915 Rust; `tests/` 11,300 Rust + 260 Python + 107 C;
`scripts/` 326 Python + 37 shell; `docs/` 6,396 JSON + 929 Markdown.
The 219-recipe catalog is vendored specification data, not authored executable implementation (`src/expansion.rs:205`).
Module map uses physical lines, including comments/blanks; small sibling files are grouped:

| Top-level module(s) | Lines | Purpose |
|---|---:|---|
| source + source/{call_graph,oracle_call,qinplace} | 3,221 | Typed binding, calls, adjoints, lifetime/cleanup checks |
| expansion + expansion_env | 2,049 | Constructor compiler, lexical capture, inverse traces, basis interpreter |
| oracle + oracle_{activation,calls,memory,pairs,state} | 3,187 | Full-history source adapters, byte layout, call proof and projection |
| engine + engine/error_bounds | 1,452 | Conflict-guided class/vertex search, resource and certificate production |
| object | 1,067 | Object/source/signature/hash parsing |
| target | 851 | Cost AST, target entries, topology and schemes |
| cleanup + cleanup/{raw,replay} | 1,432 | Cleanup partition, replay, fresh invocation rebinding |
| lproc | 519 | Canonical local-procedure instances and bindings |
| admission | 444 | Bound schedule path/occurrence validation |
| schedule | 388 | Schedule schema, selector parsing/resolution |
| source_ir + source_registry | 613 | Semantic event views and linked source constructors |
| layout | 296 | Checked symbolic memory layout |
| ffi + request + lib | 414 | C ownership/status boundary and Rust request API |
| resources | 198 | Exact occupancy, peak and ordered lifetime aggregation |
| canonical + decimal | 376 | JCS and exact/upward-rounded decimals |
| borrow + qinplace | 378 | Translation-lemma and finite-domain inverse-pair proofs |
| ref_contract + token_aliases | 285 | Published helper interfaces and token identity partitions |

The existing, ignored/untracked Cargo.lock has 28 packages including this crate (27 dependency packages); 7 direct dependencies (`Cargo.toml:7`).
Output is `rlib` + `cdylib` (`Cargo.toml:16`), one explicit integration binary (`Cargo.toml:5,27`).
All 83 commits use one Git author identity. Provenance markers classify 57 (68.7%) as explicit Codex,
24 (28.9%) as explicit Claude and 2 (2.4%) as unattributed; this counts commit metadata, not source authorship.
Query: `git -C /home/tobias/Projects/bennett-workspace/bennett-sched log --format=%H%x09%an%x09%s%x09%b%x00`;
Codex = `wip(codex job...)`/GPT agent or coauthor trailer; Claude = explicit Claude coauthor trailer.
Human implementation share cannot be derived from the shared author identity. The synthesis's near-zero-dependency generalization does not describe this crate.

## Build and test times
All executable measurements use the main checkout and scratch targets under
`/home/tobias/Projects/bennett-workspace/bennett-sched/.tmp/reaudit-2026-11-07/`.
Four display/browser variables are unset; TMPDIR points at its `tmp/`; no sibling build or source touch.
The runner waits for >=6 GiB available, load <8 (stricter than this brief's <12), and no `bennett-heavy` scope,
then uses a `systemd-run --user --scope` unit, `ulimit -v 8000000`, `timeout 600`, `/usr/bin/time`, `-j3`, test threads 4.
The first slot wait was 14:17:48–15:16:49 UTC (59 minutes); a heavy push scope then delayed the warm rebuild until 16:24:04 UTC. A new heavy ISA scope began during test compilation; the next slot opened at 17:05:56 UTC for test execution. Coverage began at 17:06:19 UTC. Queue waits are excluded from the command timings; resource checks are at invocation start, not a promise of exclusive resources for the entire run.

| Step / actual command after wrapper | Wall seconds | Exit / result |
|---|---:|---|
| Cold scratch `cargo build --offline --locked --manifest-path /home/tobias/Projects/bennett-workspace/bennett-sched/Cargo.toml -j3` | 13.74 | 0; all dependencies/root compiled |
| Warm root-crate rebuild, same command | 0.80 | 0; root crate recompiled |
| `cargo test --offline --locked --manifest-path /home/tobias/Projects/bennett-workspace/bennett-sched/Cargo.toml -j3 --no-run` | 50.62 | 0; library and integration executables built |
| Default `cargo test --offline --locked --manifest-path /home/tobias/Projects/bennett-workspace/bennett-sched/Cargo.toml -j3 -- --test-threads=4` | 23.18 | 0; 228 passed, 10 ignored, 0 failed |
| Instrumented default suite / coverage command below | 136.31 | 0; default tests passed and source report generated |

The warm rebuild invalidates only scratch `debug/.fingerprint/bennett-sched-*/lib-bennett_sched*` files;
it forces root recompilation with warm dependencies/incremental data without touching checked-out source.
It is a read-only substitute for the baseline's one-file touch, not an identical experiment.
The synthesis reports baseline load 17–20; this audit uses the quiet-slot rule. Timing deltas are not a controlled attribution of speedup to refactoring alone.
Rust outcomes: **238 named tests: four library tests + 234 integration instances; 228 passed, 10 ignored, 0 failed**. The integration binary contains 222 explicit top-level tests plus twelve instances of the shared basis-harness test; doctests contain zero tests.
Ten ignored exhaustive tests are explicitly retained in `gate.toml:15`; the full ignored suite is outside this audit's heavy-test allowance.
The default run includes all three source_adjoint tests, conformance inventory, all four resources tests, all four published_vectors tests, five gate/harness tests, and the capacity/grid unit regressions. Its Python launchers execute 14 pin tests, eight quality-metric tests and one disposable-hook test; these subordinate counts are not added to the Rust headline. No redundant focused rerun was needed.
Build and test-compilation logs contain no compiler warnings. Raw timing/test logs are retained in the absolute scratch directory above.

## Coverage
**88.09% lines (13,223/15,011); 76.60% functions (1,031/1,346)**, measured by cargo llvm-cov over Rust source during the default suite. LLVM function counts differ from the lexical scanner's definition count. Instantiation coverage is **41.57% (1,151/2,769)** and is a separate metric. Ignored simulations and branch coverage are outside this number.
Command after the same resource/scope wrapper: `CARGO_TARGET_DIR=/home/tobias/Projects/bennett-workspace/bennett-sched/.tmp/reaudit-2026-11-07/cov-target cargo llvm-cov --offline --locked --manifest-path /home/tobias/Projects/bennett-workspace/bennett-sched/Cargo.toml -j3 --json --summary-only --ignore-filename-regex /tests/ --output-path /home/tobias/Projects/bennett-workspace/bennett-sched/.tmp/reaudit-2026-11-07/coverage.json -- --test-threads=4`. No ignore-run-fail switch was used.
The instrumented cache is separate from both ordinary scratch target and the repository's gate cache.
This measures Rust src/, including its inline unit-test scaffolding; Python scripts and C test harnesses are not instrumented.
Coverage counts execution, not truth of certificates or completeness of the ISA.

| Least-covered area | Measured source lines | Gap / evidence |
|---|---|---|
| src/ffi.rs | 139/192 (72.40%) | Status guard has a direct panic/error test (src/ffi.rs:27); null/buffer/accessor rejection alternatives remain weaker than successful C consumers. |
| src/lib.rs | 18/24 (75.00%) | Small compatibility/status surface (src/lib.rs:1); four unit tests and C consumers do not establish every status/formatting alternative. |
| src/target.rs | 575/746 (77.08%) | Cost/schema/native-entry failures and uncommon scheme combinations; published costs and exact-entry diagnostics now have literal checks (src/target.rs:295; tests/published_vectors.rs:89). |
| src/cleanup/replay.rs | 564/689 (81.86%) | General borrowed/arbitrary-interface history is still explicit unfinished work, alongside invalid history/capture alternatives (src/cleanup/replay.rs:165). |
| src/source/oracle_call.rs | 204/247 (82.59%) | Less-common binding, overlap and invocation-context rejection paths; mainly tested through complete source calls (src/source/oracle_call.rs:6). |

Largest uncovered line counts (the file summary does not identify every missed branch):

| File / central phase | Uncovered / measured lines |
|---|---:|
| src/oracle.rs:1212 | 217 / 1397 |
| src/expansion.rs:1434 | 214 / 1643 |
| src/source.rs:1636 | 204 / 2138 |
| src/target.rs:353 | 171 / 746 |
| src/cleanup/replay.rs:165 | 125 / 689 |

Lowest file-level function coverage: `src/source/call_graph.rs` 42.86% (3/7), `src/target.rs` 52.83% (28/53), `src/oracle_memory.rs` 56.25% (9/16), `src/oracle_activation.rs` 61.54% (8/13), `src/oracle_state.rs` 63.16% (36/57). These function gaps remain even where many lines are reached through integration tests.

Additional semantic gaps, already documented rather than newly reported bugs:
- General oracle construction/pair scalability: `src/oracle.rs:1102`, `src/oracle_pairs.rs:296`, `src/qinplace.rs:114,168`; resource exhaustion is explicit, but large legal domains are not implemented symbolically.
- General other-workspace cleanup and native realization models: `src/source.rs:2288`, `src/target.rs:298`; inherited review findings remain open.
- End-to-end scheduled execution and independent certificate-claim replay: `tests/differential.rs:13` validates metadata admission, not those stronger properties.
- Inventory has 18 direct fixtures, 17 equivalent witnesses, 8 rebound cases, 20 partial expansion cases, 5 unexercised scheduler vectors, 489 executor/checker vectors (`docs/conformance-report.json:1`). These counts are not a semantic coverage percentage for the scheduler.
- The normative producer audit expects 7 OK, 5 unsupported and 1 host limit among 13 regions (`tests/normative_objects.rs:109,146`); green tests do not establish completion of those capabilities.

## Test quality
Deterministic random sample: Python `random.Random(20261107).sample(pool,20)` over 222 explicit top-level Rust test functions in sorted test files.
Each selected body was read; repeated instances of the shared basis helper are outside that pool.
The sampled allocator fault test is one of the declared ignored simulations; its classification is static, not an assertion that this audit executed it.
Also read the three largest test files completely: cleanup (758 lines), qinplace (563), regions (502).

| Test (file:definition line) | Class | What its assertions can detect |
|---|---|---|
| tests/pipeline.rs:242 approximate_scheme_charges_each_native_leaf_and_composes_its_error | Useful | Literal 4 gates/time, .004 norm and .008 diamond; tighter accuracy rejects |
| tests/regions.rs:340 interface_region_shape_role_and_cell_identity_are_preserved_across_calls | Useful | Literal mem slot role, six wires and preserved wire identities; malformed alternatives reject |
| tests/oracle_allocator.rs:156 free_restores_live_bits_and_double_free_or_exhausted_table_faults_at_the_first_bad_row | Useful, ignored | Literal first-fault row/code across budgets 0–4 |
| tests/oracle_memory.rs:132 explicit_boundscheck_cleans_its_literal_and_faults_before_access_when_length_crosses_entry | Useful | Nonzero initial target/fault, boundary crossing and literal XOR results |
| tests/structure.rs:206 while_rejects_writes_to_its_conditions_and_loop_live_names_must_agree | Weak | Both fixtures only require any error; unrelated rejection could satisfy them |
| tests/canonical_cost.rs:23 decision_decimals_preserve_all_digits_and_shares_round_down | Useful | Full literal decimal precision plus nonzero/downward share bound |
| tests/expansion.rs:163 declaration_reacquisition_is_fresh_and_library_scratch_is_lifo | Useful | Fresh lifetime identities plus explicit leak/order rejection, though reasons are broad |
| tests/selectors.rs:130 published_specificity_tuple_is_lexicographic_and_default_share_is_exact | Useful | Resolver winner and literal .0025 share with published specificity order |
| tests/qinplace.rs:255 qinplace_typed_arguments_use_singleton_bit_domains_and_exact_nested_token_tuples | Useful | Literal 128-bit/sign-bit domains, aliases, budgets; contradictory identity rejected |
| tests/lproc.rs:120 resolved_instance_values_preserve_the_nested_token_tuple_and_classical_value | Useful | Literal nested tuple/value/region, overflow and memory bounds |
| tests/lifted_cleanup.rs:367 deeply_projected_invocations_retain_their_containing_oracle_coordinates | Weak | Mainly compares two producer-derived coordinates; both could be wrong together, despite count 32 |
| tests/lifted_borrow.rs:26 source_adjoint_borrow_frames_use_the_adjoint_table_over_the_forward_translation_proof | Useful | All 16 tuples, preserved borrowed bit and explicit XOR truth table; certificate rule chain |
| tests/review_regressions.rs:34 repeated_identical_scratch_calls_have_complete_distinct_dynamic_frames | Useful | 1/2/3 distinct frames, literal class/width and peak=2, occupancy=4 per call |
| tests/cleanup.rs:362 k81_call_recompute_replays_the_exact_nonzero_copy_history_without_owning_it | Useful | Preserved preparation, fresh call indices and all eight restoration tuples |
| tests/pipeline.rs:203 instantaneous_native_gates_still_report_live_interface_peak | Useful | Zero time/occupancy with literal nonzero peak=2 |
| tests/cleanup.rs:219 recompute_replay_uses_carrier_coordinates_instead_of_importing_original_loop_iterations | Useful | Literal eight fresh leaves, empty carrier iteration, retained original [0] |
| tests/layout.rs:137 enormous_symbolic_region_extents_report_host_exhaustion_before_materializing_them | Useful | Huge symbolic extent must return NoMem instead of allocation/crash/acceptance |
| tests/oracle_calls.rs:47 two_oracle_tokens_bind_distinct_constructions_independently_of_the_action_budget | Useful | Distinct token budgets/private allocations plus 512 literal XOR/fault truth-table tuples |
| tests/cleanup.rs:418 fresh_call_cleanup_selectors_apply_after_rebinding_to_the_new_carrier_edge | Useful | Nested selector must target the freshly rebound child and actually choose recompute |
| tests/linked_source.rs:316 argument_context_survives_an_additional_semantic_call_and_source_host_limits_are_explicit | Useful | Nested call-depth/budget preservation and explicit one-leaf host limit |

Sample: **18/20 useful (90%), 2/20 weak (10%), 0 tautological**. Small sample; classification is per whole test, not a claim that every assertion is independent.
The baseline's 17-row sample tally is internally inconsistent (one row represents two red tests); its claimed 11/5/1 ratio is not used as a precise delta.
Oracle-backed checks outside the sample include literal 34-digit rounding (`tests/canonical_cost.rs:36`), published K80/K83 tuples,
full small-domain constructor execution (`tests/qinplace.rs:78`), reference-binary basis comparison (`tests/differential.rs:68`),
and seeded 128 x 12-interval occupancy-grid comparison (`tests/resources.rs:112`).
The dense basis harness has its own differential against the ordinary map interpreter (`tests/common/basis.rs:154`);
that map interpreter is product code, so native algebra/spec literals and the external reference remain the stronger independent anchors.
The catalog SHA test is packaging integrity, not semantic evidence (`tests/canonical_cost.rs:63`).
Would the gate catch wrong results? Yes on these asserted domains: default semantic tests, mandatory ignored simulations,
formatting and a local quality ratchet are declared (`gate.toml:11`), and disposable-hook tests check committed pins and error propagation (`tests/gate_stub.py:15`).
No full push-gate result is claimed. Metadata admission can accept a structurally valid but semantically wrong certificate;
independent claim replay is still needed (`tests/differential.rs:13`, `README.md:47`).

## Code quality
Read all of the three largest central files: source.rs (2,390 lines), expansion.rs (1,962), oracle.rs (1,509),
plus search/conflict, FFI, resource aggregation, pin resolver and relevant tests/reviews.
Function scanner masks comments/strings and balances braces; numbers below include signatures/comments.
The repository lexical complexity proxy is not an AST cognitive-complexity implementation (`scripts/quality.py:18,65`).

| Function | Lines | Body brace nesting | Location |
|---|---:|---:|---|
| nodes | 298 | 6 | src/source.rs:1636 |
| candidate | 297 | 5 | src/engine.rs:547 |
| compile | 294 | 6 | src/expansion.rs:1434 |
| parse | 293 | 5 | src/object.rs:151 |
| qinplace | 293 | 2 | src/source/qinplace.rs:48 |
| certificate | 287 | 6 | src/engine.rs:904 |
| actual | 278 | 6 | src/expansion.rs:812 |
| oracle_call | 270 | 4 | src/source/oracle_call.rs:6 |

Across src/ and scripts/: 423 functions, 131 >30 lines, 42 >100, **0 >300**, maximum 298;
58 lexical forwarding wrappers, 0 process identifiers, 1 tracked litter path.
Deepest measured function brace nesting is 7 (`src/ref_contract.rs:35`, `src/resources.rs:48`, `src/source_ir.rs:51`, `src/target.rs:690`).
Largest lexical mass: expansion.rs 930, source.rs 834, object.rs 576; mass is a local comparison aid, not a correctness score.
Findings (P2 unless noted; no newly reproduced ladder wrong result/oracle-unsoundness/build failure):
1. **Stale operational documentation.** `README.md:39` claims the now-resolved pinned token_aliases failure; `docs/quality.md:177` retains the pre-fix slow-test failure without the subsequent fix. A maintainer cannot infer current suite status from these paragraphs. Already noted for README in `docs/reviews/2026-11-07-quality-sched-r1.md` (7jo).
2. **String dispatch duplicated across phases.** `src/expansion.rs:597,1449` separately recognize constructor keys; `src/oracle.rs:144,542` and `src/source.rs:1685` interpret raw opcode strings again. Adding an opcode requires coordinated edits and makes exhaustive handling a manual obligation; no wrong result demonstrated here.
3. **Large orchestration remains.** Phase extraction fixed >300-line functions, but nodes/candidate/compile remain 294–298 lines and actual/invoke contain six-deep brace structures. The metric cut alone does not establish low semantic coupling (`src/source.rs:679,1636`, `src/expansion.rs:812,1434`).
4. **Tracked backup remains.** `.beads/hooks/pre-push.backup:1` is the only path matching the litter scanner; legitimate .beads and agent configuration are not automatically WIP. `scripts/quality.py:139` ratchets new litter but permits this recorded baseline exception.
5. **Known algorithmic limits remain.** See 2026-11-03 batch review's 2u4/a0v/ark/vt8 and current `src/oracle.rs:1102`, `src/qinplace.rs:114,168`, `src/source.rs:2288`, `src/target.rs:298`. Explicit NoMem/unsupported avoids silent success; it does not implement the promised scalable mechanisms. No duplicate correctness finding or new repair round is requested.

There are 154 `unwrap`/`expect` occurrences outside inline cfg(test) test modules, 172 including them; raw source also has 5 unwrap_or_default and 10 unwrap_or(0).
Counts alone do not show valid-input panics: many operate on validated JSON/internal invariants; the baseline assertion that each implies a valid unusual-input bug was unsupported.
FFI status guard is directly exercised (`src/ffi.rs:14,27`); invalid non-null pointers remain caller obligations (`src/ffi.rs:3`).
Remaining zero defaults inspected represent initial source versions, unchosen search choices or optional topology;
missing placement metadata now returns InvalidState (`src/engine.rs:326`). No new silent fallback was reproduced.
`src/qinplace.rs:93` verifies inverse tables; `src/source/qinplace.rs:48` binds/emits source instructions: similar names alone are not duplicated algorithms.
No obvious dead subsystem was established; the measured build/test-compilation logs contain no compiler warnings; unused public APIs are not thereby ruled out. No tracked pycache/log/lock/darc/LAST-RUN/PROGRESS files matched.

## What is good
- Exact rational decisions and outward-only display rounding have literal spec-derived expectations (`src/decimal.rs:1`, `tests/canonical_cost.rs:36`).
- Thirty released choices no longer cause irrelevant capacity enumeration; a deterministic regression tests the search dependency (`src/engine.rs:1200`).
- Pin resolution checks both fixture checkout identity and absolute confined reference paths, including PATH-decoy regressions (`scripts/pinned_sibling.py:20`, `tests/gate.rs:51`).
- Resource sweep has an independent occupancy-grid oracle and zero-duration order tests (`tests/resources.rs:82,112`).
- Unsupported normative examples retain explicit outcomes and empty output assertions rather than disappearing from the audit (`tests/normative_objects.rs:109`).

## Against the 2026-11-05 baseline
Read both the per-repository baseline and SYNTHESIS.md; these are new grades on the same A–F scale, not automatic points for merged work.

| Grade | Before -> after | What would move it up one step |
|---|---|---|
| Code | C+ -> B- | Consolidate duplicated opcode interpretation and add independently checked scalable construction/proof paths while preserving explicit failure boundaries |
| Tests | B -> B+ | Execute and independently verify emitted schedules/certificate claims beyond metadata admission; tighten broad-error and producer-vs-producer assertions |
| Build | C -> B+ | Bring a clean test-profile build plus default execution consistently below one minute; record an uninterrupted cold default invocation at the fixed pin. |

Baseline findings/coverage gaps, with current evidence (existing review issues cited, not re-filed):

| Baseline item | Status | Evidence at audited SHA |
|---|---|---|
| Two red source-adjoint fixtures / fdu | Fixed | Valid layout in tests/source_adjoint.rs:37; replacement-forward ordering src/source.rs:825; all three source_adjoint tests pass in the default run |
| Red conformance inventory / drifting live sibling | Fixed | scripts/pinned_sibling.py:25,33; gate.toml:28; tests/conformance_inventory.rs:14; inventory test and all 14 pin-resolution tests pass through the default suite |
| 745-line nodes; 685/516-line oracle build/row; 582-line compile | Fixed | Current maximum 298; src/source.rs:1636, src/oracle.rs:513,1212, src/expansion.rs:1434 |
| Inline oracle/proof caps and magic limits | Partly | Named 64 MiB oracle cap remains src/oracle.rs:1102; straight 9,000-row proof covered tests/oracle_pairs.rs:291; join-state cap persists src/oracle_pairs.rs:297 |
| Panic/FFI exposure concern | Partly | Direct catch_unwind status regression src/ffi.rs:27; 154 occurrences outside inline test modules (172 raw), versus baseline 155; count alone establishes no valid-input crash |
| Bead/job identifiers in product source | Fixed | Scanner 0; scripts/quality.py:18,120 |
| Weak E vectors and config-only gate test | Fixed | Literal costs/reasons tests/published_vectors.rs:89,110; actual grid verdict src/engine.rs:1275; executed hook/decoy tests tests/gate.rs:9,51; published-vector, grid and hook/decoy checks all pass in the default run |
| Tracked configuration/backup/status prose | Partly | HANDOFF.md removed; README.md:3 links meta handoff; backup still tracked, README.md:39 stale; agent config is not inherently litter |
| No obvious dead code / duplication by similar qinplace names | Partly | No new dead subsystem proven; paired source/proof responsibilities are distinct, but constructor dispatch is repeated src/expansion.rs:597,1449 |
| Unmeasured coverage | Fixed | Fresh default-suite Rust line coverage 88.09% (13,223/15,011); baseline audit had no measured number. docs/quality.md retains its honestly labelled earlier 88.06% record. |
| Weak FFI error/panic paths | Partly | Guard test src/ffi.rs:27 and C consumers; 72.40% FFI line coverage; null/invalid-input branches remain candidates |
| Search pathology absent regression | Fixed for the named repro | src/engine.rs:1200 deterministic 30-choice test; capacity conflict dependency tracking; the 30-choice capacity unit regression passes in the default run |
| Oracle cap-rejection branches weakly pinned | Partly | tests/qinplace.rs:339 asserts full-domain NoMem; src/oracle.rs:1102/checkpoint caps remain, no exhaustive boundary matrix |
| source/call_graph and source/oracle_call only end-to-end | Partly | src/source/call_graph.rs:26 explicit DFS; src/source/oracle_call.rs:6; src/source/call_graph.rs 91.53% lines; src/source/oracle_call.rs 82.59% lines; little direct phase-level unit coverage |
| Recompute + call_index refusal untested | Partly | Fresh paths admitted/rejected in tests/cleanup.rs:469; fallback refusal remains src/admission.rs:245, not every general cleanup is implemented |

Each baseline recommendation:

| # | Recommendation | Status and evidence |
|---|---|---|
| 1 | Repair memory fixtures, then adjoint replacement | Fixed — tests/source_adjoint.rs:37,172,205; all three source_adjoint tests pass in the default run |
| 2 | Re-pin/regenerate inventory and report SHA | Fixed — gate.toml:28, tests/conformance_inventory.rs:14; 557 cases/eight manifests with recorded 3b10907 |
| 3 | Fast/slow split, default <120 s | Fixed — Cargo.toml:21,27; gate.toml:15; default wall time 23.18 s versus baseline 550 s; ten exhaustive cases remain declared for the gate |
| 4 | Strengthen four E vectors and gate.rs | Fixed — tests/published_vectors.rs:89,110; src/engine.rs:1275; tests/gate.rs:9,51 |
| 5 | Split source/oracle/expansion functions into tested units | Partly — 0 >300, value_row direct unit src/oracle.rs:1472; most extracted phases rely on unchanged integration witnesses, not a unit test each |
| 6 | Independent randomized peak/occupancy counter | Fixed — tests/resources.rs:112 enumerates quarter ticks/order independently, 128 seeds x 12 intervals; the independent sweep test passes in the default run |
| 7 | Measured coverage and prune stale handoff | Partly — Fresh default-suite Rust line coverage 88.09% (13,223/15,011); baseline audit had no measured number. docs/quality.md retains its honestly labelled earlier 88.06% record; HANDOFF removed, README.md:39 and docs/quality.md:177 still stale |

Synthesis-specific sched concerns: pin discipline fixed; red-default-main concern fixed for the default suite (228 pass, no failures);
slow/default binary cost reduced to 23.18 s default wall time; independent resource oracle added; god functions split;
coverage now measured at 88.09% Rust lines; litter remains one backup. Broader arith/runtimes/checker findings do not apply to this repo.
The baseline's near-600-second/red run is not evidence that today's default is heavy or red.

## Plan targets
The programme target is round 2; this table measures the applicable repo contribution now, not completion of all 12 repos.
Commands use the headless/scope/budget wrapper above when executable tests/builds are involved.

| Applicable target | Met / not met | Command + observed result |
|---|---|---|
| Zero red default mains | Met | Default cargo test command above -> 0; 228 passed, 10 ignored, 0 failed |
| Zero tests using live siblings instead of pin | Met | `python3 -I /home/tobias/Projects/bennett-workspace/bennett-sched/scripts/pinned_sibling.py /home/tobias/Projects/bennett-workspace/bennett-sched bennett-isa-spec --reference` -> checkout/binary confined to 3b10907; inventory and 14 pin tests pass; raw live-path scan has only gate test diagnostics, resolver only uses live HEAD to explain failures |
| Measured coverage number recorded in docs/quality.md | Met | Python read of docs/quality.md:141 -> 88.06%, 13,218/15,011, command recorded; Fresh default-suite Rust line coverage 88.09% (13,223/15,011); baseline audit had no measured number. docs/quality.md retains its honestly labelled earlier 88.06% record. |
| Default cargo test <180 s | Met | Timed default command above -> 23.18 seconds, 228 passed / 10 ignored / 0 failed |
| Test grade >=B | Met | This audit -> B+, 18/20 sampled useful; oracle limitations stated above |
| Code grade >=B- | Met | This audit -> B-; scanner maximum 298, no >300 functions |
| No >300-line semantics functions, or owned remainder | Met | `python3 -B /home/tobias/Projects/bennett-workspace/bennett-sched/scripts/quality.py` plus the independent masked-brace scan -> 423 functions, 0 >300; no remainder requiring owner |
| Zero product process identifiers | Met | `python3 -B /home/tobias/Projects/bennett-workspace/bennett-sched/scripts/quality.py` -> process_identifiers=0; literal source regex includes comments and strings |
| Zero tracked cache/log/lock/backup/LAST-RUN litter | Not met | `git -C /home/tobias/Projects/bennett-workspace/bennett-sched ls-files` plus `python3 -B /home/tobias/Projects/bennett-workspace/bennett-sched/scripts/quality.py` -> one litter path, .beads/hooks/pre-push.backup; allowed in recorded baseline, still violates programme zero target |

Additional round-1 mechanics: one integration binary and line-table debug are present (`Cargo.toml:5,23,27`);
mandatory ignored-suite check is present (`gate.toml:15`); inherited measured coverage is recorded with honest former-pin attribution (`docs/quality.md:11,141`);
ratchet checks length/mass/wrappers/litter (`scripts/quality.py:126`) and is in the gate (`gate.toml:23`);
per-repo HANDOFF is retired (`README.md:3`). The independently extracted metrics JSON equals the recorded baseline; the ratchet CLI itself was not separately rerun. Its eight mutation/measurement tests pass through the default launcher.

## Recommendations
1. Refresh README.md:39 and append the normative-audit fix outcome to docs/quality.md:177 so operational status matches current tests (existing 7jo covers README).
2. Remove the tracked pre-push.backup and its baseline exception; ratchet should then preserve zero litter.
3. Add independent scheduled-execution/certificate-claim replay with deliberate wrong-value mutations; metadata acceptance is insufficient.
4. Tighten the sampled broad-error fixtures and literalize deeply projected coordinate expectations (tests/structure.rs:206, tests/lifted_cleanup.rs:367).
5. Keep scalable construction, cyclic pair proofs and general cleanup explicit open work; replace materialization/exhaustive limits with independently verified mechanisms.
6. Introduce typed constructor/opcode forms when these dispatch paths next change, so validation and execution share exhaustive interpretation.
7. Cover the least-exercised FFI/target/replay failures with bounded adversarial inputs, using the fresh coverage rows to choose cases.
