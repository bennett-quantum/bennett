# bennett-vm quality audit 2026-11-05

## Verdict
- Code: C+. Zero dependencies and a real x86-64 JIT, but 1,049 fns of which 73 exceed 100 lines (max 602), stringly-typed opcode dispatch, and spec-ID/bead references throughout error strings.
- Tests: B-. 424 tests, 0 `#[ignore]`, and a strong oracle layer (reference-interpreter byte diffs, published conformance harness, replay-identity checks). But 1 test file is red (committed WIP with no implementation) and oracle-backed tests run only if sibling binaries are built.
- Build: C. Incremental debug rebuild 37 s; `cargo test --no-run` 166 s; one `--lib` run of 44 tests takes 112 s; differential/conformance gate takes hours.
- Coverage was not measured (see Coverage); structural estimate only.

## Composition
Single crate `bennett-vm` (rlib+staticlib+cdylib + bin `bennett-vm`), edition 2024, **0 dependencies** (Cargo.lock has only the crate itself). std-only, including its own sha256, bigint, json, rational.

| Language | files | code LOC |
|---|---|---|
| Rust (src 34,532 lines incl. blanks; tests 15,920) | 104 | 48,895 |
| Markdown (docs, worklog, reviews) | 17 | 2,997 |
| Shell | 8 | 256 |
| JSON / C / TOML / header / YAML | 17 | ~480 |
| Total (cloc, excl. target/.tmp) | 146 | 52,627 |

Module map (src/, lines): `cc.rs` 3064 CC/R machine, history, tapes, effects; `action.rs` 2556 Q-action/oracle execution; `ref_library/` (source.rs 2554, oracle_source 716, ref_library.rs 1902 + 8 smaller) catalog consumer and source lowering; `validate.rs` 2255 + `qvalidate.rs` 1407 + `typing/coherent_typing/lifted_typing/qreg_typing` ~1400 object validation; `oracle.rs` 1606 bounded oracle interpreter; `object.rs` 1281 parser; `certificate.rs` 1158; `target.rs` 1154 target/cost model; `launch.rs` 1060 + `sched.rs` 813 + `sched_abi.rs` 264 launch/scheduler C ABI; `step.rs` 1010 step-check; `cleanup_discipline.rs` 835; `jit.rs` 671 (graph passes + mmap'd x86-64 emitter, fallback stub for non-x86); `identity.rs` 644; `json.rs`/`bigint.rs`/`rational.rs`/`exact.rs`/`interval.rs`/`sha256.rs` ~2,100 numeric+serialisation primitives. `unsafe` appears 137 times (JIT mmap, C ABI).

Tracked non-source: 17 files of `.beads/.agents/.cursor/.codex` tooling config; `include/bennett_vm.h`; `tests/launch_abi.c`, `tests/sched_abi.c`. Untracked `.tmp/` is **23 GB** (gitignored; repro litter from reviews) and `target/` is 5.0 GB.

Authorship (155 commits, 2026-10-28..11-03, all under one git author): Codex 45 (29%: 32 `wip(codex job` subjects, 13 `Agent: gpt-6.1-sol` trailers); Claude-trailered 67 (43%), of which ~20 are mislabelled Codex commits (per docs/reviews/2026-11-03-vm-batch.md); unmarked ~63 (41%); 1 Muse. No human-authored code distinguishable.

Branch `bjm-dense` (/home/tobias/Projects/bennett-workspace/bennett-vm-bjm): 16 commits ahead, 58 behind main; `git diff --shortstat main...bjm-dense` = 21 files, +6,469/-82. (Not audited.)

## Build and test times
Target cache was warm (5 GB existing target/; machine load average ~20 on 12 cores from parallel auditors, so wall clocks are inflated).

| Step | Wall |
|---|---|
| Warm incremental debug `cargo build -j3` after touching src/rational.rs | 36.7 s |
| `cargo test --no-run -j3` (47 test binaries + lib, relink after the touch) | 166 s |
| `cargo test --lib` (44 tests) | 111.8 s (one `cc::scaling_tests` set dominates) |
| 44 of 46 integration binaries, each `--test X`, 3 threads | see table below; sum about 330 s excl. timeouts |
| NOT run: `differential` (38 tests, every case x {interpreter,jit} against reference binary), `conformance` (3, published harness x 2 engines) | hours (HANDOFF.md:11 records a focused 7-test subset at ~499 s) |
| `oracle_cleanup09` (23 tests) | **timed out at 300 s**, result unknown |

Slow binaries: object09 65 s (12 tests), measurement09 59 s (5), bound_calls09 34 s (5), cleanup_fresh09 19 s (33), cleanup_partition09 16 s (16), launch_c 14 s (2). Everything else under 10 s.

Counts: 424 `#[test]` (44 in src, 380 in tests/), 0 `#[ignore]`, 0 feature-gated tests. Env-gated: sibling reference binary `BENNETT_ISA_REF` (absence = failure by design, README), `BENNETT_ISA_CONFORMANCE`, `BENNETT_FIXTURES`; tests also read sibling-repo fixtures via `../bennett-isa-spec/...` (tests/jit.rs:7-12 and others), so the crate does not test standalone.
Results of what I ran (lib + 44 binaries, 3 threads, 8 GB ulimit): everything passed except:
- **RED: `tests/memory_files.rs` 2 of 3 fail** ("unknown option --mem-file" at tests/memory_files.rs:35). Committed in eaa6ae4 (`wip(codex job sol-vm-queue)` wind-down) with the test but no implementation: `grep mem-file src/` is empty. The gate (`cargo test`) cannot be green on main as committed.
- `oracle_cleanup09`: timeout (not a failure, unknown).

## Coverage
`cargo llvm-cov` 0.9.1 is installed, but I did not run it: an instrumented rebuild of 48 binaries at load average 20 would blow the 10-minute cap, and differential/conformance (the bulk of CLI-path exercise) cannot run. **Measured coverage: none. Structural estimate only.**
Estimate: the CLI-driven differential suite plus conformance reach most of cc/action/oracle/step/validate/object/identity on the success paths; the 0.9-specific paths are reached by the `*09.rs` tests. Modules with no direct test reference and no inline tests (reached only via `load()` or CLI): `qvalidate.rs` (1407), `cleanup_discipline.rs` (835), `typing.rs`/`coherent_typing.rs`/`lifted_typing.rs`/`qreg_typing.rs` (1408 total), `qcli.rs`, `stepcli.rs`, `call_matching.rs`. `validate.rs` (2255) is referenced by 2 test files, 0 inline tests.
Five weakest areas:
1. `validate.rs` / `qvalidate.rs`: 3,662 lines of error-producing rules; negative tests exist only for a handful (coherent_typing09, validation_order has 1 test).
2. Non-x86 JIT stub (`jit.rs:652`) never executed; JIT correctness vs interpreter is checked only by running the differential twice per engine (not run here).
3. `sched_abi.rs`/`launch.rs` C ABI: 2 Rust tests (launch_c) plus 2 C consumers; 41 exported functions.
4. `estimate.rs` (67) and the estimate/E_SCHEDULE paths: explicit stubs ("unimplemented: milestone 4/5", launch.rs:895, sched.rs:252, ref_library.rs:915).
5. Error/fault branches of `cc.rs` (3064 lines, 18 inline tests) beyond the cases found by past review (P0 at cc.rs:482 in 2026-11-03-vm-batch.md shows these were not covered).

## Test quality
Sample of 18 tests (random, fixed seed), classified:

| file:line | verdict | why |
|---|---|---|
| tests/coherent_typing09.rs:70 huge_regions_type_checked_by_shape | weak | only asserts `load().unwrap()` succeeds on one input; no negative case |
| tests/coherent_typing09.rs:78 in_wires_cannot_be_modified | useful | negative plus positive twin (replace to legal form), checks diagnostic substring |
| tests/coherent_typing09.rs:97 rotation_parameters_must_be_f64 | useful | positive and 3 negatives with spec section code |
| tests/coherent_typing09.rs:163 function_wide_predicates | useful | 3 bad bodies each must be rejected |
| tests/differential.rs:1809 launch_reverse_accepts_failed_runs_at_0_9 | useful | explicit expected status per version/entry, spec-derived |
| tests/differential.rs:1211 spec_examples_are_extracted_and_diffed | useful (oracle) | extracts examples from the spec, byte-diffs vs reference binary; hard-codes name by index |
| tests/differential.rs:2244 classical_rows_and_boundary_faults | useful (oracle) | 13 ops x boundary values against reference |
| tests/differential.rs:1546 region_call_overlaps_trap_before_any_effect | useful (oracle) | 3 call forms x 3 kinds x 2 commands diffed |
| tests/differential.rs:1276 / :1281 cc_oracle_then_gate_*_{interpreter,jit} | useful but duplicated | thin wrappers over one body per engine |
| tests/differential.rs:1855 unallocatable_transfers_are_diagnostics_not_panics | useful | checks exit code 1 and "host limit" in stderr; `continue` at :1862 silently skips one combination |
| tests/differential.rs:185 check_and_hash_byte_identical_on_every_fixture | useful (oracle) | byte identity vs reference over every published fixture |
| tests/address09.rs:348 k49_fixed_rows_have_instances | useful | exact expected instance keys; but only a hand-made object |
| tests/ref09.rs:245 typed_templates_capture_records | weak/mixed | `assert_ne!(l[0].wires, l[1].wires)` and `count==2` are loose; catalog logic otherwise checked |
| tests/eps_decade.rs:10 exact_decimal_bucket_boundaries | useful | boundary decimals incl. 1e-100, hand-picked expected |
| tests/classical09.rs:266 minted_budget_rows_jit | useful | reference-backed per engine |
| tests/jit.rs:1 transformations_change_private_graph | weak | asserts stats `> 0` only (inlined_rows>0 etc.), not that output is right; object hash unchanged is a good invariant |
| tests/jit.rs:36 native_integer_kernels_match_width_arithmetic | useful | exhaustive w<=4, boundaries up to 64 vs `value::binop_reference` (second implementation; shared BigUint code) |
| src/ref_library/named_interface_tests.rs:45 published_k82_binding_cases | useful (oracle) | published vectors, count pinned to 16 |

Ratio of the 18: 13 useful (7 oracle/differential-backed), 3 weak, 0 tautological, 2 duplicates. No snapshot-only tests and no tautological self-oracle found in the sample. Test structure risks: `tests/cleanup_fresh09.rs:10` `replay_identity` is a real semantic oracle (simulates leaves on bit states and demands identity, exhaustive up to 2^5 inputs).
Oracle-backed: differential (38), conformance (3), classical09 (13), oracle_cleanup09 (23), region_alias09 (4), segment_instances09 (1), isa08_reference (6) = ~88 of 424 (21%) compare to the reference interpreter or published harness; the rest are hand-authored expectations over hand-made `.bisa` strings.
Would the gate catch a wrong result? `gate.toml` runs only `cargo test --offline` with siblings pinned to SHAs and reference/conformance binaries built, so yes for anything the reference binary and conformance cases disagree on, which is a strong external check. Caveats: (a) the reference binary and fixtures come from a sibling at a pinned commit (fine); (b) the conformance test accepts `UNAVAILABLE` cases (tests/conformance.rs:40-60) and retains them, so unimplemented spec parts do not fail; (c) the gate is red today because of memory_files; (d) no property-based tests; no fuzzing.

## Code quality
Findings (policy rule 9 and fail-fast):
1. **Committed red test with no implementation** tests/memory_files.rs:35, from `wip(codex job ...)`; README mentions binary region input and the gate cannot pass. Cost: main is not green; the 2026-11-03 review did not list it.
2. **Per-call env var read in the arithmetic hot path**: src/value.rs:149 `std::env::var("BENNETT_VM_ENGINE")` for every `binop`; src/jit.rs:79 `selection()` re-reads it per object plus builds `format!("{obj:?}")` as cache key (jit.rs:101) — a full Debug dump of the object per `for_object`. Hidden global config and O(object) key; `value.rs:149` also panics on error (`unwrap_or_else(|e| panic!)` :152) instead of returning it.
3. **Stringly-typed ISA**: instructions carry `op: String`; `oracle.rs:443-520` strips `lift.`, then `.contains(&base)` over arrays of op names for every row executed; `validate.rs:1347` does the same. A typo in an op string in any of ~400 match arms compiles silently; also slow per row.
4. **Silent defaults** (rule 9): `src/cc.rs:2296` `m.bits(...).unwrap_or_default()` computes an alloc resource key as 0 when the operand read fails (scheduler could then mis-detect conflict); `src/cc.rs:2239` `.unwrap_or_default()` drops the quantum-handle set silently; `src/step.rs:32` missing cell reads as 0 (maybe by spec). 363 `.unwrap()` and 74 `panic!/unreachable!/expect` in src.
5. **Bead and review IDs in source**: 40 spec-section/Kxx references are fine, but bead IDs in runtime error text — launch.rs:895 (`b-isa-spec-8r4; bennett-vm-47t`), launch.rs:900 (`bennett-vm-hsd`), ref_library.rs:915, :1350, sched.rs:252; tests/differential.rs:1479,:1542 (`bennett-vm-erb`, `3tx`). Policy: no bead references in source; users see these strings.
6. **Giant functions**: ref_library.rs:319 `walk` 602 lines; ref_library/oracle_source.rs:152 `body` 501; oracle.rs:438 `exec_row` 430; cc.rs:771 `exec` 415; cc.rs:1522 `command` 395; source.rs:2195 `instruction` 359; typing.rs:101 `classical` 352; qvalidate.rs:363 `sequence` 334. 73 functions over 100 lines (measured by brace matching script). `exec_row` repeats the same "destination width disagrees" block (oracle.rs:455, :482, :503, ...) 10+ times: duplicated validation with no helper.
7. **Flags where an enum belongs**: cc.rs `Frame` has `pure, reversed, marker, measured` bools (cc.rs:76-79); `Allocation {live,pinned}`, `Handle {live,viewed}` (cc.rs:24-32); `Machine.stateful, trace_enabled` (cc.rs:114-117). Combinations like pure+measured are presumably illegal but representable.
8. **Lonely interfaces / dead code**: not checked exhaustively; `Passes` has 4 independent bools (jit.rs:15) yet `selection()` only constructs 7 combinations by hand (:79-126); `pub` surface is 390 pub fns in src/*.rs for a crate whose tests go through the CLI.
9. **`jit.rs:41-50` global atomics + `audit()` env-gated eprintln** in library code (statistics via statics rather than the Stats struct).
10. **WIP litter tracked in git**: 32 `wip(codex job` commits on main; `.beads/hooks/pre-push.backup` tracked; 17 agent-tooling files (.cursor, .agents, .codex). Reviews are already in docs/reviews (cited, not repeated): P0 0m5 cc.rs:482, P1 wyg/79y/1pz/ket (2026-11-03-vm-batch.md); fixes review 2026-11-02-vm-fixes-review.md.

Fail-fast credit: JIT selection errors rather than falling back (jit.rs:74 comment and code), unsupported milestone paths return "unimplemented: ..." errors.

## What is good
- Zero external dependencies: own sha256/bigint/JSON(JCS)/rational; headless build `--offline` works.
- Independent oracle strategy: byte-diff of CLI JSON against the sibling reference interpreter on every published fixture, plus the unmodified conformance harness; absence of the binary is a hard failure (tests/differential.rs:36-43).
- Replay-identity test helper (tests/cleanup_fresh09.rs:10-50) checks cleanup semantically on bit-states instead of comparing to implementation output.
- JIT is genuine (mmap/mprotect, x86-64 emitter, jit.rs:379-520) with an exhaustive/boundary kernel test (tests/jit.rs:36) and an explicit no-fallback engine selector.
- Independent adversarial reviews have found real P0/P1 bugs and are filed with repros (docs/reviews).

## Recommendations
1. Fix or delete tests/memory_files.rs (implement `--mem-file` or remove the test) so `cargo test` is green on main.
2. Run `cargo llvm-cov` on a quiet machine with `--lib` + fast binaries, and publish a number; today there is no measured coverage.
3. Replace `op: String` with an `enum Op` parsed once at load; removes per-row string matching (oracle.rs:443, validate.rs:1347) and typo risk.
4. Cache the engine selection once (`OnceLock`) instead of `env::var` in `value::binop` (value.rs:149) and key the JIT cache by the object hash, not `format!("{obj:?}")` (jit.rs:101).
5. Split the 8 functions over 330 lines (start with `walk`, `body`, `exec_row`) and factor the repeated destination-width check into one helper.
6. Strip bead IDs from runtime error strings and tests (launch.rs:895,900; ref_library.rs:915,1350; sched.rs:252).
7. Make oracle_cleanup09 (timed out at 300 s) and object09 (65 s) cheaper or tag them as slow so a routine `cargo test --lib` plus fast set runs in a few minutes.
