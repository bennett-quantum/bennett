# bennett-plugin quality audit 2026-11-07

## Verdict
- **Code B-** (baseline C-): contextual failures, immutable sibling selection and guarded host replacement improve the floor; two large semantic functions and intertwined publication logic remain.
- **Tests B** (baseline B-): published object/result oracles and real-module mutation checks are substantial; broad whole-driver functions and uneven measured coverage limit confidence.
- **Build C** (baseline C): one LLVM-linked module per major, with no Analysis translation-unit split; cold instrumentation timing is not comparable to the baseline's warm touch.
- Grades are independently re-derived on the baseline A–F scale; this is a focused audit, not a full-gate acceptance claim.

Audited **6ff4b010e3ef6ee39018c5b5bbe43e54ece9c7b1**, initially clean `main == origin/main` in /home/tobias/Projects/bennett-workspace/bennett-plugin.
The checkout subsequently advanced to `81273430616ba3e6395250208eacd8c35b1fd03c` (beads export only); the audit remains on the requested initial SHA.
Tracked source/test files were copied into /home/tobias/Projects/bennett-workspace/bennett-plugin/.tmp/reaudit-2026-11-07/mirror and compared byte-for-byte with the audited Git tree; only the concurrently changed beads export needed replacement from that tree.
All audit writes are under /home/tobias/Projects/bennett-workspace/bennett-plugin/.tmp/reaudit-2026-11-07 or this report. Existing main-checkout libraries predate remediation (LLVM 18: November 5; LLVM 23: November 3) and are excluded from current-source evidence.
Timestamp: 2026-11-07T11:59:29Z.

## Composition

Measured with `cloc --list-file=/home/tobias/Projects/bennett-workspace/bennett-plugin/.tmp/reaudit-2026-11-07/tracked.txt --force-lang=C++,inc --by-file --json --out=/home/tobias/Projects/bennett-workspace/bennett-plugin/.tmp/reaudit-2026-11-07/cloc-inc.json`; 170 tracked paths, 165 recognized/countable files.
The explicit `.inc` mapping avoids cloc treating C++ includes as Pascal. Counts include historical verification JSON and reviews; they exclude untracked builds/caches.

| Language | Files | Code lines |
|---|---:|---:|
| C++ including .inc | 21 | 10,147 |
| C/C++ headers | 5 | 179 |
| Python | 60 | 11,329 |
| LLVM IR | 43 | 2,536 |
| C | 2 | 104 |
| JSON | 7 | 18,062 |
| Markdown | 18 | 1,482 |
| CMake / TOML | 1 / 3 | 63 / 137 |
| Shell / text / YAML | 5 | 68 |

| Directory | Counted files | Code lines |
|---|---:|---:|
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src | 25 | 10,266 |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests | 104 | 13,405 |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/scripts | 8 | 702 |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/docs | 18 | 19,133 |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/worklog / .beads / root | 1 / 4 / 5 | 170 / 210 / 221 |

Module map (physical lines; includes/comments count here, unlike cloc):

| Module under /home/tobias/Projects/bennett-workspace/bennett-plugin/src | Lines | Purpose |
|---|---:|---|
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp | 2,897 | CC entries, descriptors, object/link/hash construction, native launch stubs |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Analysis.cpp | 2,220 | abstract values, memory slots, fixpoint, tiers, handles and region checks |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Scalar.cpp | 1,293 | scalar lprocs, wrappers, layout and canonical object publication |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Normalise.cpp | 704 | LLVM normalization and logical-stack proof/preparation |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/NativeComparison.cpp | 509 | native bridge and comparison layout/target integration |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/BennettPlugin.cpp | 471 | pass options, recognition, version/attribute validation and dispatch |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/SoftFloat.cpp | 369 | floating normalization and pinned arithmetic linking |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Wide.cpp | 363 | wide arithmetic and ABI normalization |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Integer.cpp | 140 | integer intrinsic/runtime materialization |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Residual.cpp | 102 | residual IR validation |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Snapshot.cpp | 71 | snapshot replay preparation |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Memory.cpp | 23 | memory runtime materialization |
| Eight .inc files | 1,363 | CC SCC linking, reversible/runtime code and embedded IR |
| Five headers | 195 | shared declarations, layout, byte order and analysis clock |

Dependencies: two CMake discovery dependencies, LLVM and Python3 (/home/tobias/Projects/bennett-workspace/bennett-plugin/CMakeLists.txt:20,39); no vendored C++ package graph.
Eight gate sibling aliases name seven distinct sibling repositories (/home/tobias/Projects/bennett-workspace/bennett-plugin/gate.toml:22), including the native-runtimes alias for runtimes.
AST inspection of tests/scripts finds 31 standard-library import roots and zero third-party Python roots. Python files are primarily integration drivers, not an application package.
Authorship through the audited SHA: 245 commits. Exclusive provenance classes: Codex 44 (18.0%), Claude 52 (21.2%), both trailers 13 (5.3%), unattributed 136 (55.5%).
Classification uses commit bodies (`Agent: gpt`, `wip(codex job`, Codex/Claude coauthor trailers), not the shared `tobiasosborne` author name; unattributed cannot honestly be called human.

## Build and test times

| Step / selected invocation | Wall seconds | Result |
|---|---:|---|
| LLVM 18 CMake configure | 0.57 | pass |
| LLVM 18 cold build, -O1 -g1 --coverage | 74.89 | pass; 12 translation units |
| LLVM 23 CMake configure | 0.68 | pass |
| LLVM 23 cold build, -O1 -g1 | 71.68 | pass; 12 translation units |
| contract_policy.py | 0.18 | pass; versions, commit, bytes and both arith publications |
| recognition.py --major 18 | 1.21 | 79/79 |
| analysis_edges.py --major 18 | 0.33 | 20/20 |
| validation.py --major 18 | 0.74 | 49/49 |
| scalars.py --major 18 | 1.32 | 21/21 published objects; C inc8 equal; 5/5 indirect objects |
| wide.py --major 18 | 1.98 | 110/110 |
| integer_intrinsics.py --major 18 | 1.33 | 602/602 |
| memory_runtime.py --major 18 | 1.82 | 33/33 |
| normalisation_scope.py --major 18 | 1.37 | 5/5 real-module mutations rejected |
| scalars.py --major 18 --step-check (five selected cases) | 6.83 | 5/5; each exhausts 512 inputs; duplicate-label mutation rejected |
| review_regressions.py --major 18 (three selected families) | 3.76 | 26/26: 13 shared-state guards, 8 byte-order observations, 5 missing-import witnesses |
| recognition.py --major 23 | 1.49 | 80/80 |
| scalars.py --major 23 | 1.96 | 21/21 published objects; C inc8 equal; 5/5 indirect objects |

Selected scalar cases: two-calls, three-calls, two-calls-switch, three-calls-switch, missing-callee. Selected review families: global-diagnostic, byte-order, unresolved-call.
All **13 focused test invocations passed**, with zero observed red tests or deferred published scalar objects. Repeated/generated cases overlap; no summed headline test count is claimed.
The optional supplemental policy/entry-runtime/build-default checks were not run. No broad LLVM 23 numerical, full default, slow snapshot or corpus suite was executed.

Build/test protocol: headless environment; /home/tobias/Projects/bennett-workspace/bennett-plugin/.tmp/reaudit-2026-11-07/tmp for TMPDIR; /home/tobias/Projects/bennett-workspace/bennett-plugin/.tmp/reaudit-2026-11-07/target for CARGO_TARGET_DIR; 8,000,000 KiB virtual-address limit; timeout 600; CMake builds -j3.
Every configure/build/test invocation uses a separate `systemd-run --user --scope -q --unit=bennett-build-reaudit-plugin-*` scope after checking >=6 GiB available, load <8 and no `bennett-heavy` scope.
The stricter shared build-slot load limit was used. Scope waiting is excluded from command wall time; the frozen-source waiter recorded five minutes before building, one minute after LLVM 18 compilation, then thirteen minutes before LLVM 23 tests. Measurements and exact argument arrays: /home/tobias/Projects/bennett-workspace/bennett-plugin/.tmp/reaudit-2026-11-07/receipts.json; command output: /home/tobias/Projects/bennett-workspace/bennett-plugin/.tmp/reaudit-2026-11-07/*.log.
The fixture mirror keeps hard-coded driver output directories inside permitted scratch; immutable published siblings are read through the checked gate cache.
Build object directories were fresh; installed tools, filesystem pages and sibling artifacts were already warm.
Warm source-touch measurement was deliberately omitted: this is read-only, and a second build of a major is prohibited. No `scripts/test` end-to-end, full gate, pre-push, corpus matrix or slow snapshot suite was run.
`cargo test --no-run` is inapplicable to this C++/Python repository; there is no analogous unified test-binary build step.
Default inventory is 6 policies plus (37 drivers + 1 selected-regression driver) per major = **82 commands**, not 82 unit tests (/home/tobias/Projects/bennett-workspace/bennett-plugin/scripts/test:16,17,83,143).
There are 55 Python test/support files, 22 unittest-named methods, and 251 literal `assert` AST nodes; none is a defensible total execution-case count.
No skip/xfail markers were found. Shared globals and configured-class execution remain named opt-in promised checks (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/review_regressions.py:237; /home/tobias/Projects/bennett-workspace/bennett-plugin/docs/quality.md:331).

## Coverage

Fresh measurement on the audited source: **60.83% executable lines (4,238/6,967)**, and **65.70% gcov functions (272/414)**, LLVM 18, GCC 13, `-O1 -g1 --coverage`.
Function counts include the inline/lambda instances gcov emits; they are not public-API or dialect-clause coverage. Counters start at zero in the fresh scratch build and cover exactly the LLVM 18 invocations in the timing table.
Reproduction: configure/build/test argument arrays are in /home/tobias/Projects/bennett-workspace/bennett-plugin/.tmp/reaudit-2026-11-07/receipts.json; `python3 -B /home/tobias/Projects/bennett-workspace/bennett-plugin/.tmp/reaudit-2026-11-07/collect_coverage.py` runs `gcov --json-format` for all 12 note files and merges source-line counts under the audited mirror's src directory.
Raw JSON and per-file totals: /home/tobias/Projects/bennett-workspace/bennett-plugin/.tmp/reaudit-2026-11-07/coverage/summary.json. Counter summarization reads completed counters and took under one second; it does not execute tests or rebuild anything.
This workload omits the complete soft-float, reversible, production/budget and snapshot suites. Its smaller numerator is **not evidence of regression** from the preceding remediation workload.

The recorded remediation sample is **66.86% executable lines (4,646/6,949)**, GCC/gcov 13 with LLVM 18; /home/tobias/Projects/bennett-workspace/bennett-plugin/docs/quality.md:170 records instrumentation, commands, reset and exclusions.
That sample predates the expanded 82-command default workload; do not present it as coverage of the current complete default suite, both majors or all promised mechanics.
No percentage is inferred from test count or module reachability. Published sidecar `coverage.json` counts ISA instruction metadata, not C++ test coverage (/home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp:2251).

The five largest missing-line areas in the fresh focused run are listed in the final coverage summary. Driver mappings identify reach, not exhaustive rule coverage.

| Area / entry point | Covered / executable lines | Missing lines | Focused-sample limitation |
|---|---:|---:|---|
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp:1763 | 907/2171 | 1264 | descriptors, unified linking, inverse/budget and broad CC/native launch paths; selected byte-order/import/state cases only |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Analysis.cpp:1232 | 1199/1524 | 325 | FP/composite and rare provenance/rejection transfers beyond selected exact-atom examples |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/SoftFloat.cpp:79 | 58/269 | 211 | FP carrier/helper/rounding paths; integer/memory drivers do not exercise the full FP suite |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/NativeComparison.cpp:261 | 148/355 | 207 | native finalization, target/address and launch adapters beyond selected shared-state preparation |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Normalise.cpp:14 | 285/465 | 180 | unselected intrinsics, stack and normalization branches |

The preceding recorded sample also had Snapshot.cpp 0/57, NativeComparison.cpp 15/355 and SoftFloat.cpp 58/269; its weakest-file list is at /home/tobias/Projects/bennett-workspace/bennett-plugin/docs/quality.md:198.
Snapshot replay remains wholly outside this sample. The one-line embedded NativeComparison/SingleFrame runtime includes also remain 0/1: plugin line instrumentation does not measure execution inside emitted guest code.

Varargs/load-delta/vector-lane/CC-marker rung4 work is still absent from this audited main; do not claim branch-only capability coverage.

## Test quality

Reproducible random sample: seed **20261107**, choose 18 without replacement from the 40 Python test/driver functions containing a literal assert, in sorted file/AST order.
This deliberately includes test phases and whole `main` drivers because most tests are script-style; assertion-free `check()`/result-accumulator drivers and unittest assertion methods are outside this sample frame.
The files read include the three largest test files: review_regressions.py (1,082 physical lines), softfloat.py (846), corpus_gate.py (496). The corpus driver was read, not executed.

| Sampled function | Class | Reason |
|---|---|---|
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/review_regressions.py:230 main | useful | source-native/state guards, hand-derived results, independent interpreter and reversal checks |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/native_link.py:39 build | weak | asserts linker symbol-layout stability; alone gives no runtime result oracle |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/normalisation_scope.py:42 check_case | useful | accepts pristine actual output, restores real residue, then requires precise verifier rejection |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/allocator_closure.py:23 main | useful | independently derived allocator accounting, exact results, fault boundaries and reversal |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/cc_switch.py:33 check | useful | native source execution supplies results; ISA reversal and memory restoration checked |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/native_fixtures.py:16 main | useful | pinned C source baseline compared with lowered native output |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/entry_snapshot.py:71 stack_witness | weak | validates fixture shape only; runtime payload assertions belong to its caller |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/dialect_version.py:15 main | useful | positive/negative version negotiations and a frozen prior-object hash |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/budget_stage.py:9 main | useful | published exact objects/results plus all 316 step-budget prefixes |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/native_checked.py:50 main | useful | exact native/interpreter results and structured fault-code agreement |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/review_regressions.py:159 run_global_case | useful | first executes source-native expectations, then checks generated-host behavior |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/softfloat.py:125 evidence | weak | verifies parseable host/device bitcode and computes hashes, not numeric correctness |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/production_records.py:8 main | useful | recomputes artifact hashes and independently enumerates emitted instruction coverage; metadata scope explicit |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/build_defaults.py:14 main | useful | loads actual plugin from unrelated cwd and executes three hand-derived FP sums |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/corpus_gate.py:392 main | useful | pinned fixture matrix compares pre/post native traces and fails on divergences; limited properties described below |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/scalars.py:62 indirect_cases | useful | generated indirect objects checked/executed against hand-derived inputs, with inverse/duplicate-label checks |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/production.py:16 main | useful | published scalar byte comparison, exact interpreter output, budget edge and launch protocol |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/budget_stage.py:64 oracle | weak | CLI success/JSON adapter; semantic equality is checked by main |

Ratio: **14 useful / 4 weak / 0 tautological (77.8% useful)**, versus baseline 11/19 useful; different random frames prevent a statistical before/after claim.
Weak helper phases are not defective merely because callers own the semantic assertions; they show why function-level test counts can overstate evidence.
Strongest independent oracles: scalar published bytes/hashes/results (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/scalars.py:184), Python big integers and byte arrays (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/wide.py:116; /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/memory_runtime.py:80), source-native switch/fixture results, exhaustive inverse sweeps and residue mutations.
The gate would catch wrong scalar objects, many numeric/memory results and reintroduced intrinsic/vector residue: /home/tobias/Projects/bennett-workspace/bennett-plugin/scripts/gate:26 delegates to the bounded default suite, whose /home/tobias/Projects/bennett-workspace/bennett-plugin/scripts/test:17 inventory includes the repaired drivers.
Limits: corpus L6 currently checks candidate-list type, not candidate-set correctness (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/corpus_gate.py:248); L4 compares the plugin with its rerun, while printed scope admits stock-pipeline identity remains pending (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/corpus_gate.py:273).
Soft-float transport still contains string checks and a completion-only production witness (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/softfloat.py:333,557); the separate exact native/published numerical checks mitigate this, but do not make each structural check numerical.

## Code quality

The three largest source files were inspected: Production.cpp (2,897 lines), Analysis.cpp (2,220), Scalar.cpp (1,293), including changed failure/closure/host-replacement paths.

1. **P2, remaining semantic hotspots:** /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Analysis.cpp:1232 is 529 physical lines and /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Normalise.cpp:14 is 500. A transfer-rule edit must track many mutable domains and nested cases. They have a named owner/disposition at /home/tobias/Projects/bennett-workspace/bennett-plugin/docs/quality.md:314; no new wrong-result claim is made.
2. **P2, test maintenance:** /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/review_regressions.py:230 is 849 lines and /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/softfloat.py:63 is 780; branching, fixture generation, execution and result bookkeeping stay interleaved. Main's regression function was already large; new witnesses increase the maintenance surface.
3. **P2, weak semantic proxies:** candidate-list type checking and self-rerun identity do not establish S2 precision or cross-pipeline semantic identity (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/corpus_gate.py:248,266). Existing independent exact-atom recognition tests cover only their published cases.
4. **Target exception, not a new blocker:** two process identifiers remain together in a product diagnostic (/home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp:2329). /home/tobias/Projects/bennett-workspace/bennett-plugin/docs/quality.md:324 explicitly records maintainer-required retention; that exception does not satisfy the plan's literal zero target.
5. **P2, duplicated publication machinery:** sorted JSON serialization appears in /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Scalar.cpp:33 and /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp:30; recursive SCC/reference-envelope construction is independently maintained at /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Scalar.cpp:878 and /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp:1909. This duplicates contract bookkeeping and needs differential tests when either changes.

Complexity was measured using the repository lexical/AST reader (/home/tobias/Projects/bennett-workspace/bennett-plugin/scripts/quality.py:28), which masks strings/comments. Its brace-weighted mass is a local proxy, not a standard cognitive-complexity score; lambda/operator recognition is incomplete.

| File | Longest function | Lines | Complexity proxy | Max brace depth |
|---|---|---:|---:|---:|
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Analysis.cpp | step:1232 | 529 | 6,021 | 10 |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Normalise.cpp | normaliseScalar:14 | 500 | 1,947 | 7 |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp | lowerProduction:2602 | 295 | 7,736 | 16 |
| /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Scalar.cpp | lowerScalar:997 | 296 | 2,485 | 8 |

Other largest Production functions: launchObject:1959, 291 lines; lower:1497, 252. Analysis::run is 232 and composite 217.
The same scan finds exactly two production functions >300 and four test functions >300. Full per-file distribution and wrapper counts: /home/tobias/Projects/bennett-workspace/bennett-plugin/.tmp/reaudit-2026-11-07/metrics.json; all comparisons against the recorded quality baseline are non-regressing.
Line-width evidence remains real: Normalise.cpp max 531 columns; Analysis.cpp 3 lines >200; Scalar.cpp 7; Production.cpp 12. Embedded generated C in CallerSnapshot.inc reaches 1,102 columns; do not confuse raw-string size with C++ function complexity.
Fail-fast improvements: module flags and missing entry-runtime definitions get contextual diagnostics (/home/tobias/Projects/bennett-workspace/bennett-plugin/src/Scalar.cpp:713,747); declaration dispatch emits the specified fault rather than an absent-map lookup (/home/tobias/Projects/bennett-workspace/bennett-plugin/src/Scalar.cpp:341).
Shared-global dependencies are frozen before replacing any host entry and include indirect candidates (/home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp:2280,2525); the interim exits 125 rather than silently resetting state (/home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp:2325).
No tracked pycache, logs, locks, backups or progress files were found; root HANDOFF.md is retired. Beads exports, historical reviews and the worklog are intentional records, not executable-code defects.
No demonstrated dead production module was found. Unused subprocess imports noted in /home/tobias/Projects/bennett-workspace/bennett-plugin/docs/reviews/2026-11-06-quality-plugin-r2.md remain low-value cleanup; no dead-code percentage is invented.
Historical correctness findings are already recorded in /home/tobias/Projects/bennett-workspace/bennett-plugin/docs/reviews/2026-11-03-plugin-batch.md and the three quality reviews; this audit checks the baseline disposition below rather than re-filing them.

## Against the 2026-11-05 baseline

Read the per-repository report and ecosystem SYNTHESIS.md at /home/tobias/Projects/bennett-workspace/bennett/docs/quality/2026-11-05-audit.

| Grade | Baseline -> now | One step upward requires |
|---|---|---|
| Code | C- -> B- | isolate the two remaining semantic hotspots after rung4 merges, with direct transfer/phase invariants |
| Tests | B- -> B | broaden comparable C++ coverage and execute independent oracles for the remaining structural-only witnesses |
| Build | C -> C | split the Analysis translation unit and demonstrate a materially faster same-configuration warm rebuild |

Every numbered baseline code finding:

| Baseline finding | Status | Evidence / disposition |
|---|---|---|
| 1. Scalar entry-stack map::at abort | fixed | closure retention and missing-helper diagnostics /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Scalar.cpp:721,747,786; focused result in timing table |
| 2. Long Analysis/Normalise functions | not fixed | /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Analysis.cpp:1232 / /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Normalise.cpp:14; 529/500 inclusive, baseline 528/499 used a different line-count convention |
| 3. Minification / long lines | partly | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/scalars.py:94 now named phases; /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Normalise.cpp:14 still reaches 531 columns and numerical drivers retain dense generated text |
| 4. 55 broad process/rule-label grep hits | partly | measured two actual process identifiers at /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp:2329, retained by explicit approved diagnostic |
| 5. return-false/catch candidate fallbacks | partly | helper/declaration failures repaired at /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Scalar.cpp:747,786,336; boolean recognizers such as /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Analysis.cpp:953 legitimately return false to continue dispatch; baseline's raw grep was not proof of 40 bugs |
| 6. contract_policy reads live registry | fixed | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/contracts.py:79,90 uses git show at gate pin; /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/pinned_siblings.py:30 refuses moved/missing selected checkout |
| 7. README dialect version skew | fixed | /home/tobias/Projects/bennett-workspace/bennett-plugin/README.md:7 matches /home/tobias/Projects/bennett-workspace/bennett-plugin/SPEC_VERSIONS.toml:2, both 0.2.13 |
| 8. Tracked WIP litter / HANDOFF | partly | `git -C /home/tobias/Projects/bennett-workspace/bennett-plugin ls-tree -r --name-only 6ff4b01` + litter regex: zero; root HANDOFF absent; review probes/worklog/beads are retained evidence |
| 9. Repeated test scaffolding | partly | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/contracts.py:24,56 centralizes run/plugin command; /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/recognition.py:55 and /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/analysis_edges.py:253 still construct commands directly |

Every baseline recommendation:

| Recommendation | Status | Evidence |
|---|---|---|
| 1. Diagnose missing runtime helper / resolve entry-stack | fixed | /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Scalar.cpp:747; scalar published entry-stack comparison/execution in focused run |
| 2. Pin-only contract_policy | fixed | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/contracts.py:79,90 and contract_policy result below |
| 3. Split Analysis/Normalise and Analysis TU | not fixed | /home/tobias/Projects/bennett-workspace/bennett-plugin/CMakeLists.txt:24; /home/tobias/Projects/bennett-workspace/bennett-plugin/docs/quality.md:314 expressly defers both functions to the rung4 owner |
| 4. Shared harness and readable drivers | partly | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/contracts.py:24,56; scalar phases extracted; review main still 849 lines |
| 5. Executed/spec checks instead of grep/inequality | fixed for named witnesses | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/wide.py:101,213; /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/integer_intrinsics.py:152,400; /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/review_regressions.py:404; actual-module verifier /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/normalisation_check.cpp:27 |
| 6. One-major native coverage | fixed | /home/tobias/Projects/bennett-workspace/bennett-plugin/docs/quality.md:170; /home/tobias/Projects/bennett-workspace/bennett-plugin/CMakeLists.txt:25; fresh sample described above |
| 7. Remove identifiers and update README | partly | README fixed; two approved diagnostic identifiers remain /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp:2329 |

Baseline coverage and weak-test observations, with explicit disposition:

| Baseline observation | Status | Current evidence |
|---|---|---|
| Production hostStub/linkReferences reach | partly | /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp:1763: fresh Production coverage 907/2171; selected paths execute, broad integration remains outside sample |
| Rung4-only varargs/load-delta/vector/CC facilities | not fixed | /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Analysis.cpp:1232: audited main remains the pre-rung4 analysis implementation; branch coverage is not credited |
| Unindexed error/diagnostic paths | partly | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/validation.py:1: 49/49 selected validation cases pass; no exhaustive diagnostic-to-spec coverage demonstrated |
| LLVM 23-specific paths | partly | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/scalars.py:94: fresh build, 80 recognition cases and 21 exact objects pass; full numerical/native matrix unrun |
| entry-stack coverage/crash | fixed | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/scalars.py:120: published entry-stack object is among 21/21 exact accepted/executed fixtures |
| wide/integer intrinsic-residue greps | fixed | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/normalisation_scope.py:42: real generated modules and helper bodies checked; five mutations rejected |
| wide identity/trivial inputs | partly | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/wide.py:208: bitcast identity still uses one byte pattern; pointer basis/seeded vectors and executed constant shifts add stronger observations |
| integer division fault exit-only witness | fixed | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/integer_intrinsics.py:400: structured ISA fault 5 plus nonfault payloads 16, 8, 0 are checked |
| memory key inequality only | fixed | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/memory_runtime.py:247: key assertions paired with executed helper/global payloads 42, 7, 8 |
| mixed-native IR substring only | fixed | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/review_regressions.py:404: emitted host function executes all 256 byte inputs plus exact native FP sums; this driver read, not run in this sample |
| analysis additive-copy-cycle empty wants | fixed | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/analysis_edges.py:275: TOP and convergence below ten rounds are explicit; selected driver passes 20/20 |
| contract-policy brittle live-registry guard | fixed | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/contracts.py:79: immutable registry/text reads and corruption checks; focused command passes |
| gate-policy self-reference concern | partly | /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/gate_policy.py:19: policy classification and receipt-revision rejection cases are useful guards; they do not establish program numeric correctness |

Additional baseline coverage/test concerns: hostStub/linkReferences are still broad integration paths (/home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp:2305,1773); rung4-only facilities remain absent; diagnostic coverage is not exhaustive; LLVM 23 evidence is the focused recognition/scalar sample, not its full numerical or integration suites.
The old hard-coded live debug interpreter is now a gate-selected debug binary (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/scalars.py:9). Remaining literal dialect flags still exist, but pin/version checks prevent accepting drift.
The additive-copy-cycle witness now checks both TOP and convergence <10 rounds (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/analysis_edges.py:275), so the baseline's empty-wants criticism no longer describes its complete assertion.
The old memory key inequality is now paired with executed results 42/7/8 (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/memory_runtime.py:247); pointer round trips test every basis bit plus seeded samples (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/wide.py:213).
The baseline's broad `N##` matches also include legitimate published normalization-rule labels; they are not directly comparable to the current process-ID regex.
The synthesized ecosystem concerns that apply here therefore improve in pin isolation, numeric oracles, source litter and recorded coverage; large Analysis rebuilds and deferred mechanics remain.

## Plan targets

Targets are checked literally against /home/tobias/Projects/bennett-workspace/bennett/docs/plan/2026-11-06-quality-floor-remediation.md:10. "Not met (unverified)" does not assert a failing implementation.

| Applicable target | Result | Command / result and source evidence |
|---|---|---|
| No red default main | not met (unverified here) | full equivalent scripts/test is forbidden by this audit; focused baseline failures have the outcomes in the timing table |
| Zero live-sibling-reading tests | met structurally | inspected /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/pinned_siblings.py:30 + contracts.py:83; all publication readers resolve gate aliases, then immutable spec/manifest blobs; live HEAD appears only in diagnostics |
| Coverage number + command recorded | met | read /home/tobias/Projects/bennett-workspace/bennett-plugin/docs/quality.md:170: 66.86%, reset/workload/compiler commands and weakest files recorded |
| Default run <180 s | not met (unverified here) | docs claim 82 commands / 132.057 s at /home/tobias/Projects/bennett-workspace/bennett-plugin/docs/quality.md:4; full runner explicitly excluded, so no fresh end-to-end number claimed |
| Test grade >=B | met | current independently derived B, sampled functions and numerical/mutation evidence above |
| Code grade >=B- | met | current independently derived B-, with remaining semantic complexity explicitly retained in grading |
| No >300-line function in fixed files; remaining owner list | met for scoped remediation | script metrics: touched Scalar/Production <=300; remaining Analysis/Normalise are 529/500, owned/deferred at /home/tobias/Projects/bennett-workspace/bennett-plugin/docs/quality.md:314 |
| Zero product process identifiers | not met | quality.py identifier scan =2, both /home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp:2329; approved exception recorded, not zero |
| Zero tracked pycache/log/lock/backup/LAST-RUN | met | audited tree's tracked-path regex =0; /home/tobias/Projects/bennett-workspace/bennett-plugin/scripts/quality.py:18 defines the full categories |

Additional round-one deliverables: shared harness, native coverage configuration, default/slow inventories, quality ratchet, README alignment and HANDOFF retirement are present (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/contracts.py:1; /home/tobias/Projects/bennett-workspace/bennett-plugin/CMakeLists.txt:5; /home/tobias/Projects/bennett-workspace/bennett-plugin/scripts/test:17; /home/tobias/Projects/bennett-workspace/bennett-plugin/gate.toml:12).
The ratchet's recorded baseline admits the two identifiers and long-function deferral; a passing ratchet is not proof that the programme's final absolute targets have all been met.

## What is good

- Published scalar objects are compared as bytes, hashes and execution observations; this can reject a plausible but wrong object (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/scalars.py:184).
- Actual numerical output is inspected before clang can hide a missed normalization; five mutation classes test the test's sensitivity (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/contracts.py:63; /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/normalisation_scope.py:42).
- Pinned publication resolution fails with selected SHA/actual HEAD context instead of borrowing a live sibling (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/pinned_siblings.py:30).
- Host shared-state dependencies are computed before rewriting, and unavailable transport stays visible as a named promise (/home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp:2525).

## Recommendations

1. Finish the already-owned Analysis/Normalise split when rung4 merges, adding transfer/phase tests and an identical-configuration warm rebuild measurement (/home/tobias/Projects/bennett-workspace/bennett-plugin/docs/quality.md:314).
2. Remeasure native line/function coverage with a fixed, recorded focused workload; add independent witnesses for Snapshot/native-adapter gaps without promoting slow suites to every edit (/home/tobias/Projects/bennett-workspace/bennett-plugin/docs/quality.md:198).
3. Separate the 849/780-line regression/softfloat driver phases while retaining independent expected results and real-output mutations (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/review_regressions.py:230; /home/tobias/Projects/bennett-workspace/bennett-plugin/tests/softfloat.py:63).
4. Strengthen corpus L6 candidate semantics and cross-pipeline identity beyond list type and plugin rerun equality (/home/tobias/Projects/bennett-workspace/bennett-plugin/tests/corpus_gate.py:248,266).
5. Retire the two approved diagnostic identifiers when the sharing contract lands; distinguish that exception from achieving the zero target (/home/tobias/Projects/bennett-workspace/bennett-plugin/src/Production.cpp:2329).

JOB-COMPLETE
