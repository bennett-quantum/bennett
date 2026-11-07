# bennett-dialect-spec quality audit 2026-11-07 (tooling)

## Verdict
- **Code B-:** the checker now has concept modules, explicit publication composition and specific defect diagnostics; dense analysis and an untested legacy chain remain.
- **Tests B:** 156 prepared default tests pass, with useful negative controls and native/ISA observations; independent recognise/normalise labels remain missing.
- **Build B-:** the prepared default suite takes 29.18 s, but the documented command fails on a fresh tree without its scratch directory; the full gate was not run.
- Audited **b6a6e46f3abdce65d5a173e63b4d27b8375e4e3b**, equal to local `origin/main`; the main checkout was clean before inspection. This is a tooling audit, not contract acceptance.

## Scope and method

Repository: `/home/tobias/Projects/bennett-workspace/bennett-dialect-spec`. Scratch: `/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07`.
Read the standing brief, COMMON rules, build-slot amendment, baseline report and synthesis, remediation plan, repository laws, README, quality policy and all four existing review documents.
The three largest production Python files were read: harness/run.py (2079 physical lines), dialect_analysis.py (1152), dialect_flow.py (920).
The three largest test files were read: test_dialect_check.py (1076), test_fixes_v3.py (346), test_dialect_v03.py (145).
IR/parser, version composition, runner, rehasher, pin resolver and ratchet code were also inspected.

Tests write into repository-relative paths ([harness fixtures:69](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/harness/test_fixes_v3.py:69), [checker scratch:36](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:36)).
To preserve the read-only checkout, all 380 tracked paths were copied under scratch `source/`; byte comparison reported **0 differences** before execution.
Apart from the designated report, this auditor changed only the copy and scratch artifacts; a concurrent .beads/issues.jsonl export modification appeared in the main checkout during inspection and was left untouched. Final HEAD/origin-main remained the audited SHA; final byte comparison found that export was the only differing tracked path. Its .git pointer permits read-only index queries against the original repository.
Four layout symlinks select the existing pinned checkouts; `git rev-parse HEAD` and `git diff --quiet HEAD --` confirmed every pin and clean tracked content.
The one matching immutable ISA snapshot was reused read-only; build.lock/BUILD.json updates went into the scratch copy. No real Cargo build was needed.
Snapshot fingerprint: `f6512ca17682d9f66a56e00b52e583012a31f3240154ac20ba6ba9c57a08a914`, source pin `c1d13200acb08af4922535f5a15a1ab872b78b41`.

Every executed suite used a systemd user scope, `timeout 600`, `ulimit -v 8000000`, CARGO_BUILD_JOBS=3, RUST_TEST_THREADS=4 and the headless environment.
Initial suite launch: 20 GiB available, load 11.07, within the then-binding load<12 rule.
Prepared rerun: 23 GiB available, load 7.51, no heavy scope. Later measurements obey load<8/no bennett-heavy and the 30-minute slot limit.
No push gate, full spec checker, full legality matrix, heavy/ladder test or sibling gate was executed.

## Composition

`cloc --list-file=/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/tracked.list --by-file --json --out=/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/cloc.json --quiet` measured tracked files only.
Cloc recognized 368/380 paths (normal exclusions/deduplication); LOC below means nonblank, noncomment code, not physical lines.

| Directory | Counted files | Code LOC | Main content |
|---|---:|---:|---|
| scripts | 67 | 11250 | Python checker, tests and C execution witnesses |
| tools | 8 | 647 | Draft 0.3 composition, witnesses, rehasher and tests |
| corpus | 88 | 146947 | Harness, IR/C cases, controls and retained JSON/Markdown results |
| emission | 108 | 12557 | Frontend emission examples and generated LLVM IR |
| spec | 30 | 25552 | Published/draft contracts, marker header and seed sources |
| docs | 45 | 17470 | Audits, reviews, spike evidence |
| Remaining counted files | 22 | 979 | Repository/process configuration and history |
| **Total** | **368** | **215402** | JSON results dominate; this is not 215k LOC of implementation |

| Language | Counted files | Code LOC |
|---|---:|---:|
| JSON | 18 | 143915 |
| Markdown | 46 | 38446 |
| LLVM IR | 152 | 15231 |
| Python | 68 | 12884 |
| C / C++ / headers | 49 | 3614 |
| Rust | 2 | 150 |
| Julia | 6 | 202 |
| Shell / TOML / text / YAML | 27 | 960 |

Tooling contains **10177 production Python LOC in 41 files**, **2018 test LOC in 22 files**, plus the 10-LOC snapshot build recorder.
Another 679 Python LOC are documentation/spike witnesses outside the tooling coverage scope.
There is no tracked Cargo.toml/Cargo.lock, no validator crate, and no in-repo reference interpreter implementation.
The two Rust files are emission examples, not a validator. [README:13](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/README.md:13) correctly names the Python validator.

Module map (cloc Python LOC; related small witness modules grouped by responsibility):

| Module(s) | LOC | Purpose |
|---|---:|---|
| dialect_check / dialect_ir | 26 / 492 | Public facade, LLVM parsing, ABI/type tables |
| dialect_analysis / dialect_flow | 1067 / 810 | Legacy/shared analysis and current points-to/provenance fixpoint |
| dialect_rewrite / dialect_normalise / dialect_wide / dialect_atomic | 309 / 652 / 84 / 23 | Materialisation and scalar/vector/atomic lowering |
| dialect_execution / dialect_map | 680 / 461 | Trace/lifting helpers and reference-object construction |
| dialect_check_v02 | 773 | Published recognition, residual validation, executor snapshots and row dispatch |
| dialect_bounds / dialect_meta / dialect_driver | 245 / 158 / 161 | Lifetime bounds, contract coverage and driver scenarios |
| dialect_native / dialect_cc / dialect_state / dialect_tdl | 249 / 116 / 81 / 367 | Native, classical and coherence execution witnesses |
| dialect_initialisation / scalar_witnesses / atomic_witnesses / memory_witnesses / interprocedural / boundaries / lifetimes | 47 / 74 / 79 / 21 / 31 / 158 / 140 | Focused state families |
| dialect_0211 / 0211_contract / 0212_contract / 0212_vectors / 0213 / 0214 / arith_request | 46 / 52 / 30 / 78 / 150 / 124 / 30 | Publication-specific checks and canonical requests |
| dialect_pins / dialect_profile / dialect_report | 26 / 46 / 11 | Input resolution, scoped ISA selection, semantic/bookkeeping totals |
| quality / run_tests | 119 / 45 | Structural ratchet and test partition/discovery |
| tools/dialect_check_v03 / dialect03_witnesses / dialect03_rehash | 71 / 194 / 102 | Draft runner, ISA09 evidence and anchored hash refresh |
| corpus/legality/harness/run | 1749 | LLVM matrix execution, attribution, reduction and reporting |

Dependency measurement: AST import scan of all tooling found **0 third-party Python imports**; Cargo dependencies **0** after stub deletion.
External dependencies remain LLVM 18/20/23, system C toolchain, Rust/Cargo for uncached ISA executors and Rust frontend, Julia for frontend cases, and four pinned sibling inputs.
[toolchains.toml:3](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/toolchains.toml:3) embeds host-specific absolute tool directories; this is still a configured developer environment, not a portable install.

Authorship: `git -C /home/tobias/Projects/bennett-workspace/bennett-dialect-spec log --format=%aN%x1f%B%x1e`, classified by explicit Agent/Co-Authored-By/WIP markers:
**213 commits**, all Git author `tobiasosborne`; **28 explicit Codex (13.15%)**, **86 explicit Claude (40.38%)**, **99 unattributed (46.48%)**.
Unattributed is not a measured human fraction. The baseline's “nearly entirely agent-authored” inference cannot be established from Git author names alone.

## Build and test times

All timings use `/usr/bin/time -f %e`. Logs and timing files are under the scratch path above.
The first run had cold local harness outputs but a warm pinned ISA executable; the prepared rerun reused generated harness/runtime caches.
Python bytecode writes were disabled to preserve owned paths.

| Measurement | Wall s | Result |
|---|---:|---|
| Warm incremental build after touching one source | N/A | Interpreted tooling; no crate/build target remains; no main source was touched |
| Cargo test --no-run | N/A | No Cargo manifest remains |
| Python equivalent: discovery without execution | 0.27 | 156 default + 33 slow; 189 unique IDs |
| Documented default command, fresh scratch copy | 30.93 | 156 run: 152 pass, **4 errors**, missing scripts/.tmp |
| Same command after mkdir of scratch copy's scripts/.tmp | **29.18** | **156 passed**, unittest body 28.642 s |
| Instrumented prepared default | 44.32 | 156 passed; unittest body 43.588 s |
| Full push gate / full v02 / --slow / full corpus matrix | Not run | Prohibited full gate/matrix; slow suite not needed for the bounded default measurement |

Reproduce the prepared default with the following command, launched in working directory `/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/source` (no shell cd):
```sh
env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER TMPDIR=/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/tmp PYTHONDONTWRITEBYTECODE=1 BENNETT_GATE_LAYOUT=/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/pins CARGO_TARGET_DIR=/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/target CARGO_BUILD_JOBS=3 RUST_TEST_THREADS=4 systemd-run --user --scope -q --unit=bennett-build-reaudit-dialect-ready-$(date -u +%H%M%S) bash -c 'ulimit -v 8000000; /usr/bin/time -f %e timeout 600 python3 /home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/source/scripts/run_tests.py'
```

No unittest skip/expected-failure outcomes were reported. The 33 slow tests are deferred by explicit selection, not skipped tests.
The 191 static test_ definitions include two nested selection sentinels ([test_test_runner.py:8](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_test_runner.py:8)); runtime discovery correctly counts 189.
The first four errors are test_dialect_0211's callee-summary/native-graph cases and test_dialect_0212's two carrier verifications.
[run_tests.py:42](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/run_tests.py:42) does not prepare scratch, while [dialect_bounds.py:15](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_bounds.py:15) writes there before calling the directory-creating command wrapper.
The gate avoids this through [gate.toml:14](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/gate.toml:14). This is a reproducible standalone bootstrap defect, not evidence of a red prepared push gate.

## Coverage

Fresh independent prepared-default measurement: **47.713301% combined**, matching the repository's recorded 47.71% exactly. Coverage scope is **41 production modules**.
The slot opened after 9 minutes at 21 GiB available/load 6.29/no heavy scope; instrumented execution passed 156 tests in 44.32 s wall.

| Metric | Covered / total | Measured % |
|---|---:|---:|
| Executable Python statements | 4942 / 9699 | **50.9537%** |
| Branch exits | 2121 / 5104 | **41.5556%** |
| Combined coverage.py metric | 7063 / 14803 | **47.7133%** |

Command below used the same scoped resource envelope as the prepared default, with `PYTHONPATH=/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/coverage-lib` and `COVERAGE_FILE=/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/coverage.data`:
```sh
python3 -m coverage run --branch --source=/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/source/scripts,/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/source/tools,/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/source/corpus/legality/harness --omit='*/test_*,*/interpreter_test_support.py' /home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/source/scripts/run_tests.py
```
JSON receipt: `/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/coverage.json`; **4757 statements and 2983 branch exits remain unexercised** in this default-only measurement.

The repository records **47.71% combined statement/branch coverage** at [docs/quality.md:52](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/docs/quality.md:52), with its producing command at line 59.
That historical number is a fast-suite measurement, not full-gate or contract-clause coverage.
Coverage.py 7.17.2 was installed only under scratch; the system Python initially had no coverage module.
Instrumentation includes scripts/, tools/, corpus/legality/harness/ and omits test_* and interpreter_test_support.py.
C witnesses, generated IR, the sibling Rust interpreter and separately spawned Python processes are outside this denominator.

The five largest uncovered statement populations are measured below (combined percentages include branches):

| Area | Combined % | Missing statements | Unexercised behavior / evidence |
|---|---:|---:|---|
| [dialect_analysis.py:262](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_analysis.py:262) | 21.10 | 804 / 1059 | Legacy compute_bases, s2, s4 and prov_step bodies have no hits |
| [harness/run.py:1389](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/harness/run.py:1389) | 50.32 | 742 / 1597 | Matrix orchestration and 295-line report body have no hits; helper/native paths do run |
| [dialect_execution.py:21](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_execution.py:21) | 6.68 | 605 / 660 | Legacy lift/classify bodies have no hits |
| [dialect_check_v02.py:598](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:598) | 56.13 | 291 / 732 | Full run/main dispatch has no hits despite direct recognition/validation tests |
| [dialect_native.py:30](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_native.py:30) | 3.33 | 231 / 244 | Most native/frontend execution families are deferred to spec/slow runs |

The two wholly uncovered modules are dialect_0212_vectors (71 statements) and dialect_0212_contract (24); lifetime/boundary modules are only 4.74%/5.26% combined.
Current Flow is better exercised: **83.91% combined / 88.08% statements**; mapping is 78.94% combined and normalisation 63.62%.

Additional scope gap: emission examples have no freshness check in [gate.toml:16](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/gate.toml:16); the obsolete Rust stub is gone rather than “100% covered.”
The unexecuted legacy chain remains callable through [dialect_execution.py:651](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_execution.py:651); its missing hits do not by themselves prove it dead.

## Test quality

Random sample: Python AST test functions, sorted by file/line, `random.Random(20261107).sample(..., 21)`; selection saved as `/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/sample.json`.
All 21 were read, including the deferred ones; classification is about what each test can detect, not a claim every sampled test executed this audit.

| Test (function name abbreviated only where clear) | Class | What it can detect / limitation |
|---|---|---|
| [test_checks.py:66 new_cast_flagged_but_not_failure](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/harness/test_checks.py:66) | Useful | Exact added-cast observation plus unchanged negative control |
| [test_controls.py:12 controls_fail_intended_checks](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/harness/test_controls.py:12) | Useful | Executes LLVM negative controls and checks intended L1/L3/L4 evidence |
| [test_execution.py:19 successful_exit_without_all_inputs_is_failure](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/harness/test_execution.py:19) | Useful | A zero-exit fake driver with incomplete protocol must fail |
| [test_fixes_v3.py:96 canonicalize_resolves_unresolved_and_alias_sets](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/harness/test_fixes_v3.py:96) | Useful | Hand-written symbol/alias/unresolved trace expectation |
| [test_fixes_v3.py:325 value_not_swallowed](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/harness/test_fixes_v3.py:325) | Useful | Parser must distinguish attribute arguments from operand values |
| [test_runtime.py:108 bad_and_freed_handles](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/harness/test_runtime.py:108) | Useful | Compiled runtime must expose use-after-free and invalid-handle observations |
| [test_dialect_0211.py:73 ruled_sentences](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_0211.py:73) | Weak | Publication wording check; no semantics or local negative control |
| [test_dialect_0211.py:82 native_and_abstract_graph](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_0211.py:82) | Useful | Native/abstract witness plus wrong root mutation |
| [test_dialect_0213.py:20 full_version_guard](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_0213.py:20) | Useful | Accepted full version and five explicitly rejected stale tokens |
| [test_dialect_0214.py:38 each_accepted_item_is_load_bearing](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_0214.py:38) | Useful | Eight distinct clause mutations must be rejected; editorial rather than execution scope |
| [test_dialect_check.py:59 round8_zero_descriptor_shapes](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_check.py:59) | Useful | Explicit expected shape counts over five nontrivial examples |
| [test_dialect_check.py:121 round8_bitcast_domains](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_check.py:121) | Weak | LLVM transforms input, but domains oracle is another annotation in the same spec |
| [test_dialect_check.py:324 round6_wrapped_gep](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_check.py:324) | Useful | Exact target/provenance plus signed/scaled/wrapping variants |
| [test_dialect_check.py:373 round5_pointer_width](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_check.py:373) | Useful | Executes mapped object against ISA, with explicit 2^32 and 2^32+1 results |
| [test_dialect_check.py:508 round4_packed_store](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_check.py:508) | Useful | Native source and materialised output must both store hand-derived 129 and preserve 170 |
| [test_dialect_check.py:851 new_native_drivers](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_check.py:851) | Weak | Checks expected data exists and “int main” appears; never executes driver |
| [test_dialect_check.py:868 binding_and_indirectbr_maps](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_check.py:868) | Useful | Exact mapping plus changed operands must fail |
| [test_dialect_check.py:978 driver_platform_scenarios](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_check.py:978) | Weak | Multiple numeric edits plus malformed obligation do not isolate numerical oracle sensitivity |
| [test_quality.py:19 new_litter_and_identifier_fail_but_deletion_passes](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_quality.py:19) | Useful | Positive and negative ratchet direction assertions |
| [test_dialect_v03.py:17 v02_state_receipt_survives_draft_import_and_scope_exit](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/tools/test_dialect_v03.py:17) | Useful | Fresh process exposes global dispatcher/profile leakage and checks full receipt equality |
| [test_rehash.py:19 executor_drift_is_refused_without_writing_spec](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/tools/test_rehash.py:19) | Useful | Corrupted executor hash must raise before changing input bytes |

**17/21 useful (80.95%), 4/21 weak (19.05%), 0 tautological.** Not statistically comparable to the baseline's purposive 21-test sample.
Oracle-backed layers include native before/after execution, LLVM verification, ISA execution, hand-derived packed arithmetic and negative corpus controls.
Examples include [pointer execution:373](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_check.py:373), [packed store:508](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_check.py:508), [incomplete protocol:19](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/harness/test_execution.py:19).
Two hash anchors have explicit §9.2 envelope transcripts ([hash-anchors.json:2](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/hash-anchors.json:2)); Python hashlib and sha256sum reproduced both recorded digests during this audit.

Would the configured gate catch a wrong result? **Yes** for mutations seen by the now-gated unit/slow suites and independent execution witnesses.
**No assurance** for a shared wrong recognise/normalise annotation: [recognition:520](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:520) compares verdict to spec `verdict=`, and [normalisation:583](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:583) compares output to spec text.
The full 2943-row result is not a fresh observation here: [docs/quality.md:24](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/docs/quality.md:24) records historical full runs.
The new [dialect_report.py:2](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_report.py:2) separates semantic from xrefs/parse/coverage/inventory; documented totals are **472 semantic (16.04%) + 2471 bookkeeping (83.96%)**, not 472 independent oracles.

## Code quality

1. **Standalone setup defect:** [run_tests.py:42](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/run_tests.py:42), [test_dialect_0211.py:87](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_0211.py:87), [test_dialect_0212.py:27](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_dialect_0212.py:27). A fresh documented invocation fails four tests before scratch creation; mkdir-only preparation changes the result to 156/156.
2. **Independent label gap remains:** [dialect_check_v02.py:536](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:520), [:583](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:583). A common mistaken interpretation encoded into both label and checker can pass. This is baseline recommendation 3 and the disclosed round-2 backlog, not a new review finding.
3. **Complexity remains concentrated:** [dialect_flow.py:538](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_flow.py:538) is 122 physical lines with nested data propagation; [report:1713](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/harness/run.py:1713) is 295 lines mixing aggregation and rendering. The split improves navigation but does not remove algorithmic review cost.
4. **Legacy analysis is retained:** [dialect_analysis.py:262](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_analysis.py:262), [:694](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_analysis.py:694), [dialect_execution.py:651](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_execution.py:651). The old classifier still owns separate bases/provenance passes while current recognition uses Flow; calling it remains possible and its semantics need coverage or an explicit compatibility owner.
5. **One process identifier remains:** [0214_runtime_instances.c:2](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/0214_runtime_instances.c:2) contains brt-vbi. Its bytes are spec-hashed; [docs/quality.md:90](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/docs/quality.md:90) records the exception. Passing a baseline ratchet with one exception does not meet the plan's literal zero target.
6. **Draft admission remains explicitly unavailable:** [dialect03_witnesses.py:40](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/tools/dialect03_witnesses.py:40) always raises SECOND-READER-PIN for unsupported rows. This is honest blocked evidence and existing backlog, not a hidden pass or a new defect.
7. **Environment portability remains limited:** [toolchains.toml:7](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/toolchains.toml:7) names one user's rustup/Julia locations; an otherwise clean machine needs configuration before it can reproduce these tests.

AST measurements reproduce the recorded ratchet: **769 functions; maximum 295 lines; 133 >25, 47 >50, 14 >100, 3 >200, 0 >300**.
Longest production functions: report 295, [lift:21](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_execution.py:21) 230, [lproc:210](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_map.py:210) 219, [prov_step:694](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_analysis.py:694) 168.
Compound-statement depth, treating elif as the same decision level and resetting at functions: Flow **9** at line 861, Analysis **7** at line 305, harness **6** at line 1410.
The largest Boolean node has six operands ([analysis:717](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_analysis.py:717)); these are review costs, not demonstrated wrong results.
The local cognitive-mass estimator reproduces **12336**, with **3 exact forwarding wrappers**; this is the repository's metric, not a standardized complexity score.

Policy-pattern assessment: no validator lonely interface remains; regex source-rewriting/import-hook patching is removed.
Explicit state selection uses Publication/ContextVar and per-runner state dispatch ([profile:20](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_profile.py:16), [Runner:466](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:466)).
Malformed constants now raise ([value_set:324](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:324)); programming exceptions are recorded separately from contract failures ([Runner.check:489](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:489)).
Conservative TOP/empty-set returns in dataflow were not automatically classified as silent errors: they are part of the abstract domain and need a soundness witness before becoming a defect.
[Flow.direct_callees:756](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_flow.py:756) and [Analysis.direct_callees:177](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_analysis.py:177) retain similar traversal owners; no whole cleanup subsystem rewrite is justified by this audit.
Tracked litter scan: **0** bytecode/cache/log/lock/backup/LAST-RUN/PROGRESS artifacts. `git ls-files` independently found no matching Cargo/litter paths.
Historical emission files are corpus artifacts, not automatically WIP litter; their unverified freshness is the relevant weakness.

Existing review findings are not reissued: [round 1](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/docs/reviews/2026-11-06-quality-dialect-r1.md:11) found emission-error masking and global dispatch leakage; [round 2](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/docs/reviews/2026-11-06-quality-dialect-r2.md:11) records both fixed.
The current default run passes their regression tests ([test_dialect_v03.py:17](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/tools/test_dialect_v03.py:17), [:106](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/tools/test_dialect_v03.py:106)).
The prior draft S0 contract review and 0.2.14 fidelity review remain separate contract evidence; this tooling audit does not re-grade them.

## What is good

- Real native/ISA observations and hand-derived results survive the fast/slow partition; expensive cases remain in [gate.toml:22](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/gate.toml:22).
- Failures distinguish checker defects, contract failures and blocked capability evidence ([Runner.check:483](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:483)); incomplete driver output cannot count as success ([execute_inputs:780](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/harness/run.py:780)).
- Pin identity and dirty-check tests replace live sibling defaults ([dialect_pins.py:13](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_pins.py:13), [test_pins.py:26](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/test_pins.py:26)).
- Explicit publication scoping prevents imported draft behavior from changing published behavior ([using_profile:57](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_profile.py:57)).
- Hand-pinned anchors refuse input/executor drift before any spec write ([rehash:81](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/tools/dialect03_rehash.py:81)); structural metrics and wrapper count are enforced by one configured ratchet.

## Against the 2026-11-05 baseline

Source baseline: [bennett-dialect-spec.md](/home/tobias/Projects/bennett-workspace/bennett/docs/quality/2026-11-05-audit/bennett-dialect-spec.md); ecosystem context: [SYNTHESIS.md](/home/tobias/Projects/bennett-workspace/bennett/docs/quality/2026-11-05-audit/SYNTHESIS.md).
Grades were re-derived from this checkout's evidence on the same A–F scale. No grade improvement is inferred merely from a review's CLEAR.

| Dimension | Baseline | This audit | One step up requires |
|---|---|---|---|
| Code | C+ | **B-** | Resolve the legacy-analysis ownership and reduce concentrated semantic review cost with behavior-backed changes |
| Tests | B- | **B** | Add independent recognise/normalise labels and exercise the low-covered execution/report paths |
| Build | C | **B-** | Make the documented default command bootstrap cleanly and document portable pinned environment setup |

Every numbered baseline code finding, coverage gap and recommendation is accounted for below; shared rows identify overlaps.

| Baseline finding/recommendation | Status | Current evidence |
|---|---|---|
| Monolithic 3125-line dialect_check.py; recommendation 4 split/rename | **Partly** | Facade is now 36 physical lines, concept modules exist ([dialect_check.py:1](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check.py:1)); 1152-line Analysis and 2079-line harness remain |
| Legacy_main/unreachable 0.1 entry point | **Partly** | legacy_main absent; legacy classify still calls s2–s7 ([dialect_execution.py:651](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_execution.py:651)) |
| Import-hook/regex patch modules and version replacement | **Fixed** | Explicit Publication/Runner03 ([dialect_profile.py:20](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_profile.py:16), [Runner03:19](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/tools/dialect_check_v03.py:19)); patch module absent from index |
| Validator stub/lonely interface; recommendation 2/coverage gap 1 | **Fixed** | No tracked Cargo manifest or validator code; README explicitly names Python ([README:13](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/README.md:13)) |
| Mixed checker-bug and contract diagnostics; code findings 1/5 | **Fixed** | Separate checker-defect branch at [check_v02:489](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:489); default diagnostic regression passes |
| Unit/harness/v03 unit tests not in gate; recommendation 1 | **Fixed** | 156 default + 33 slow in two gate checks ([gate.toml:16](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/gate.toml:16)); draft unit tests included by discovery |
| Full v03 execution checker not gated; coverage gap 5 | **Not fixed** | Full checker command remains v02 only ([gate.toml:26](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/gate.toml:26)); unsupported draft rows still require second reader ([witnesses:40](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/tools/dialect03_witnesses.py:40)) |
| No measured Python coverage | **Fixed** | Recorded number/command ([quality.md:52](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/docs/quality.md:52)); independent rerun status in Coverage above |
| Recognise/normalise labels share spec oracle; recommendation 3, synthesis independent-oracle recommendation | **Not fixed** | Same label/text comparisons ([check_v02:520](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:520), [:583](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:583)) |
| Circular rehash; recommendation 5 | **Fixed as recommended** | Two independent pinned transcript anchors; rewriting still allowed only outside protected anchors ([rehash:81](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/tools/dialect03_rehash.py:81), [hash-anchors:2](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/hash-anchors.json:2)) |
| Inflated undifferentiated 2943 checks; recommendation 7 | **Fixed** | Separate semantic/bookkeeping summary ([dialect_report.py:2](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_report.py:2), [check_v02:717](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:717)); documented 472/2471 |
| Bead/session identifiers in runtime source; recommendation 6 identifier half | **Partly** | Capability codes replace mutable references; one spec-hashed C comment remains ([runtime_instances:2](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/0214_runtime_instances.c:2)) |
| LAST-RUN/PROGRESS and tracked WIP; recommendation 6 litter half | **Fixed** | Independent index scan empty; ratchet current litter=0 ([quality.py:80](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/quality.py:80)) |
| round2..round8 naming and duplicate lifetime roles | **Partly** | Concept-named witnesses replace roundN modules; version-specific files and separate legacy analysis remain ([check_v02.py:829](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:829)) |
| Long functions/dense statements/string dispatch; baseline code 6/8 | **Partly** | No >300, but report 295 and flow_step 122 remain ([run.py:1713](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/harness/run.py:1713), [flow:538](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_flow.py:538)) |
| Live sibling interpreter coupling; baseline code finding 10 | **Fixed for input identity** | All input pins verified; resolver rejects missing/wrong/dirty checkouts ([dialect_pins.py:13](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_pins.py:13)). Running a pinned published binary is allowed by COMMON; no shared implementation import was found |
| Matrix report weakly tested; coverage gap 2 | **Not fixed** | Long report/matrix commands remain outside default selected execution ([run.py:1388](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/harness/run.py:1389), [:1713](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/harness/run.py:1713)); no full matrix claim here |
| Emission freshness; coverage gap 3 | **Not fixed** | 112 tracked emission files; no emission freshness check ([gate.toml:16](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/gate.toml:16)) |
| Trivial v03 constant/version tests and weak unknown-effect test | **Fixed/partly** | Stub and old patch tests deleted; real scoped verdict tests replace them ([test_dialect_v03.py:60](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/tools/test_dialect_v03.py:60)); weak driver/label assertions still appear in new random sample |
| Baseline 177 s unit / 572 s spec gate, environment coupling | **Partly** | Prepared default now 29.18 s with explicit 33-test deferral; dependency paths persist ([toolchains:3](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/toolchains.toml:3)); full checker timing not remeasured |
| Baseline green-main claim | **Partly** | Prepared default 156/156; fresh standalone invocation 4 errors. Baseline did not establish clean-bootstrap behavior, so a numerical semantic regression is not inferred |

The synthesis's applicable pin/coverage/fast-loop/litter recommendations improved; its independent-verdict-oracle recommendation is still outstanding.
There is no substantiated new numerical wrong-result regression in the exercised prepared default suite. The fresh standalone setup failure remains open.

## Plan targets

Applicable rows from [the Targets table](/home/tobias/Projects/bennett-workspace/bennett/docs/plan/2026-11-06-quality-floor-remediation.md:13).
These are repository-local assessments; ecosystem totals cannot be inferred from one audit.

| Target | Met? | Command + result / source |
|---|---|---|
| Zero red default mains | **Not met for fresh documented invocation** | `timeout 600 python3 /home/tobias/Projects/bennett-workspace/bennett-dialect-spec/.tmp/reaudit-2026-11-07/source/scripts/run_tests.py`: 4 setup errors; after scratch preparation the same command passes 156 |
| No tests reading live siblings instead of gate pin | **Met** | `git -C <absolute pinned checkout> rev-parse HEAD` + `git diff --quiet HEAD --`: all four match/clean; default pin tests pass; resolver [dialect_pins:13](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_pins.py:13) |
| Measured coverage number and producing command recorded | **Met** | [docs/quality.md:52](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/docs/quality.md:52) records 47.71% and line 59 command; audit remeasurement separately qualified above |
| Default equivalent under 180 s; slow tests tagged/gated | **Met with preparation** | Timed default 29.18 s; discovery 156+33/189 unique; `gate.toml` has --slow ([line 22](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/gate.toml:22)) |
| Test grade at least B | **Met** | This audit's independent 21-test classification + measured default run: B |
| Code grade at least B- | **Met** | This audit's code reading + AST structure/failure-path review: B- |
| No >300-line semantics functions, or remaining owners | **Met** | Tracked-tooling AST scan / `python3 /home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/quality.py`: 769 functions, maximum 295, over_300=0 |
| Zero bead/job identifiers in source/errors/output | **Not met** | `python3 /home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/quality.py`: 1 identifier; [0214_runtime_instances.c:2](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/0214_runtime_instances.c:2) |
| Zero tracked pycache/logs/locks/backups/LAST-RUN | **Met** | `git -C /home/tobias/Projects/bennett-workspace/bennett-dialect-spec ls-files` pattern scan empty; quality scan litter=0 |

Related round-1 obligations: unit/slow suites and ratchet are configured ([gate.toml:16](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/gate.toml:16), [:28](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/gate.toml:28)); local HANDOFF is retired with [README:18](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/README.md:18) redirect.
Round-2 dialect independent-label target is **not met** ([recognition:520](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:520)); the two hash anchors solve a narrower circularity problem.
Review clearance is documented in the existing round-2 review; this audit did not rerun or endorse the full gate.

## Recommendations

1. Bootstrap scripts/.tmp in the documented test runner before discovery/execution; preserve the fresh-tree failing case as a regression ([run_tests.py:42](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/run_tests.py:42)).
2. Add independent recognizer/normalizer expectations from a second implementation or executed legality-corpus results, beginning with the 155 recognise and 46 normalize pairs ([check_v02.py:536](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py:520)).
3. Test the largest uncovered reporting/legacy paths or document and retire unreachable compatibility code; do not treat zero coverage alone as dead-code proof ([run.py:1713](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/harness/run.py:1713), [execution.py:651](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_execution.py:651)).
4. Resolve the spec-bound brt-vbi source comment through its authorized digest-update process so the literal zero-identifier target can pass ([runtime_instances.c:2](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/0214_runtime_instances.c:2)).
5. Preserve the two independent hash anchors and add a reference/layout-dependent anchor before trusting broader automated rehashing ([hash-anchors.json:2](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/hash-anchors.json:2)).
6. Document a portable toolchain/pinned-cache setup and keep emission freshness claims explicitly scoped until a check exists ([toolchains.toml:3](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/toolchains.toml:3), [gate.toml:16](/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/gate.toml:16)).

JOB-COMPLETE
