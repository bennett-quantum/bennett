# Sonnet spot-check of the 2026-11-07 sol re-audit (plan R0.3 outside anchor)

Auditor: claude-sonnet-5-5, read-only. Written 2026-11-07T10:58Z. Method: for each report, 3 grade-driving claims checked
against cited file:line or by re-running the cited cheap command; two repos (isa-spec, runtimes) re-graded in depth.
Re-runs used `git archive origin/main` copies and scratch targets under `<repo>/.tmp/spotcheck-2026-11-07/` (headless env,
`ulimit -v 8000000`, `-j3`, `timeout <= 300`). No tracked file in any repo was touched (`git status` clean for tracked paths).
Grade scale: baseline A-F with +/-. One "step" = one notch (C+ -> B- is +1).

## 1. Claim checks, per repo

### bennett-circuits (origin/main 5d10d65)
| Claim | Cited evidence | Verdict |
|---|---|---|
| Default suite 210 passed / 0 failed / 3 ignored | `cargo test --offline -j3` | **confirmed**: re-ran on archive copy, 210 / 0 / 3 (55 s cold incl. compile; sol 72.9 + 11.7 s) |
| `tests/support/exact.rs` byte-identical to `src/amplitude.rs`; sim twins differ only in 2 import lines | exact.rs:1, sim.rs:1 | **confirmed** (`diff -q` identical; `diff` of sim.rs vs simulation.rs = the two `use` lines) |
| Six functions >300 lines (execute 536, classical_schema 481, row 460, schema 329) | classical.rs:445, checker.rs:2379, oracle.rs:534, checker.rs:181 | **confirmed**: brace-matched 536 / 481 / 460 / 329 exactly |
| Baseline finding 7 "clone density not fixed: 136/138/130" | history/checker/oracle | **confirmed in conclusion, numbers not comparable**: baseline counted `.clone()` = 124/119/108; sol counted `.clone` tokens = 136/138/130. Strict `.clone()` now 125/119/108 (unchanged). Sol did not flag the method change. |
| Tracked litter = exactly `.beads/hooks/pre-push.backup`; 3 ignores; 180 test declarations | git ls-files, grep | **confirmed** (1 path; 3 `#[ignore`; 180 `#[test]`) |
| Weak test `interface_only_symbolic_loops...` asserts only `proof_status == "proved"` | proof_output.rs:1096 | **confirmed** (single assert; and the promised-6kc test is an ignored positive-only assertion at static_checker.rs:1025) |

### bennett-targets (origin/main a8f5089)
| Claim | Cited evidence | Verdict |
|---|---|---|
| 83 Rust tests, 0 ignored, all pass | cargo test | **confirmed**: 83 `#[test]`, 0 `#[ignore`; re-ran: 83 passed / 0 failed in 0.35 s (needs `BENNETT_GATE_LAYOUT` = the ISA cache dir; a wrong layout fails closed with the pin message, as claimed) |
| Longest production functions: schema 220, aggregate 191, expand 151, realisation_model 151; zero >300 | target.rs:88, runtime.rs:231/57, model.rs:158 | **confirmed** (brace-matched 220 / 191 / 151 / 151) |
| Baseline "missing vertex-limit defaulted to 0" fixed; 32-schedule independent occupancy oracle exists | runtime.rs:386; tests/cases/runtime.rs:345 | **confirmed**: `.ok_or_else(... "no declared vertex limit")`; oracle at :345 loops 32 scenarios with a tick-by-tick discrete simulation, independent of `aggregate` |
| Provenance sidecars all say "illustrative", no sourced hardware numbers | ideal-all-to-all.provenance.md:3 | **confirmed** (hand-derived, "not claims about a commercial device") |
| 21/38 Suite E scenarios unavailable, honestly recorded | suite_e.rs:220 | **confirmed** by code path (unavailable block must carry a non-empty reason naming a bead); the 21/17 split itself not recounted |

### bennett-dialect-spec (b6a6e46 = origin/main)
| Claim | Cited evidence | Verdict |
|---|---|---|
| Monolith split: `dialect_check.py` is now a facade; Analysis 1152 and harness 2079 lines remain | dialect_check.py:1 | **confirmed, small miscount**: facade is 31 lines (report says 36); 1152 and 2079 exact |
| No tracked Cargo/validator stub, no litter | git ls-files | **confirmed** (only match is a `validator/target` untracked leftover dir on disk, not tracked) |
| One bead id remains, in a spec-hashed C comment | 0214_runtime_instances.c:2 | **confirmed** (`brt-vbi`) |
| Standalone default command errors 4 of 156 on a fresh tree (no `scripts/.tmp`) | run_tests.py:42, dialect_bounds.py:15, gate.toml:14 | **confirmed statically**: gate's `prepare` step does `mkdir -p scripts/.tmp`; run_tests.py does not; dialect_bounds writes into SCRATCH first. Run not repeated |
| 156 default pass in 29.18 s; coverage 47.71% | runs | **unverifiable cheaply**: needs the 47 GB `scripts/.isa-ref` snapshot cache + four pins; not copied. The static test-def count (191 `def test_`) matches sol's 191 |
| Sampled `test_new_native_drivers` is weak ("int main" substring, never executes driver) | test_dialect_check.py:851 | **confirmed** (and it is `@slow`, so not in the default 156) |

### bennett-runtimes (origin/main 6c7a588)
| Claim | Cited evidence | Verdict |
|---|---|---|
| Measured coverage 20.93% lines / 17.02% functions / 11.90% branches | `scripts/coverage` | **confirmed exactly** (re-ran, 1.9 s: 261/1247, 24/141, 168/1412) |
| 11 fast scripts pass, both majors | tests/test_*.py | **confirmed for the 11 I ran** (integer_width, alignment, global_ranges, free_ownership, transport_errors, fenv, host_libc, integer_helpers, control_helpers, quality_ratchet, build_cache: all PASS; my times 0.06-14.3 s) |
| Valid-width scratch still large: VLAs at integer_arithmetic.c:96/:117; 24 B/heap-byte history at heap.c:106; 4 KiB mmap per object at heap.c:149 | cited lines | **confirmed** (96: `a[limbs],b[limbs],product[2*limbs]`; 117: four VLAs; MAX_WIDTH 8,388,608 bits = 128 Ki limbs; heap.c:106 maps `heap_limit_max*sizeof(*history)` with sizeof = 24; :149 maps 4096 per record) |
| Baseline finding 1 unowned free fixed | bump.c:86 | **confirmed** (`__bennett_nz_fault(7)` when no allocation owns the pointer; test_free_ownership passes) |
| Remaining VFS re-entry retention | vfs.c:49 | **confirmed**: `__bennett_rt_vfs_prepare` resets std fds only, `names`, `cwd`, `next_inode` persist |

### bennett-meta (d3c4592 = origin/main)
| Claim | Cited evidence | Verdict |
|---|---|---|
| 0 tracked pycache/log/lock/PROGRESS paths | git ls-files | **confirmed** (empty); no `docs/quality.md` (confirmed absent) |
| Pre-push validates the working tree, not the pushed SHA | scripts/pre-push:5-26 | **confirmed** (`cd $root; discover('tools/tests')`; no stdin/ref handling) |
| Retired runner pace guard still fails open | codex_job.py:76, :197 | **confirmed** (`except Exception: return None` then "quota unavailable; proceeding") |
| 35 council+packet tests pass (sol: 38 incl. 3 script tests) | unittest | **confirmed**: `PYTHONPATH=<repo> python3 -m unittest tools.tests.test_council_{schema,selftest,steps} tools.tests.test_review_packet` = 35 OK in 0.34 s. Hook tests not run (brief forbids pre-push) |
| Weak tests `test_schema_does_not_mention_severity`, `test_prompt_has_no_severity_word` | test_council_schema.py:39, :52 | **confirmed** (assertNotIn only) |

### bennett-isa-spec (3b10907 = origin/main)
| Claim | Cited evidence | Verdict |
|---|---|---|
| Both baseline red tests are now green: r21_resources (9) and isa09_qinplace (42) | `--test r21_resources`, `--test isa09_qinplace` | **confirmed**: 9 passed in 0.49 s; 42 passed in 16.9 s; also isa09_certificate 6/6, isa09_budget_mint 13/13. Build of the two binaries 52.8 s cold (sol: 66.8 s for qinplace alone) |
| Eight functions >300 lines unchanged; `oracle` 1,088 lines | source_constructor.rs:81, classical.rs:1468 (446) | **confirmed** by reading `step_prepared` (starts :1468, one closure-dispatch chain) and the file layout; same 8 as baseline per sol's same-scanner comparison |
| Tracked litter: 1 .pyc, 1 .log, 5 PROGRESS, HANDOFF.md; process tag at classical.rs:890; dead binding at object.rs:1320 | git ls-files, grep | **confirmed** all (`let _ = base;` at :1320; `(codex B09)` at :890) |
| 781 test attributes = 654 + 127 | static count | **confirmed** (my census: 781 `#[test]` lines in both crates' `tests/`) |
| Gate "would catch a wrong result for covered semantics" | gate.toml | **partly refuted by mutation** (see 2a): a spec-violating one-token change in the CC interpreter survives 152 tests |

## 2. Grades: sol vs this spot-check

| Repo | Sol code / tests / build (baseline) | Spot-check verdict |
|---|---|---|
| circuits | B- / B+ / B+ (C+ / B / B-) | **agree all**. 2 of 3 top code findings fixed (minified CLI, bead tags); tests re-run green; build 55 s cold. |
| targets | B+ / B+ / A- (B / B- / unmeasured) | **agree all**, tests borderline (21/38 published E scenarios still unavailable, K86 oracle pin stale; I would not go above B+). |
| dialect-spec | B- / B / B- (C+ / B- / C) | code **agree**; tests **too high by 1** (B-): the top baseline finding (labels share the spec's own prose oracle, check_v02.py:520/:583) is "not fixed" in sol's own table, 4/21 weak, 47.7% combined coverage; build **too high by 1** (C+): sol marks its own target "zero red default mains: not met" (4/156 errors on the documented command). |
| runtimes | B / B+ / A- (B- / B / B+) | code **too high by 1** (B-); tests **agree** (B+); build **agree** (A-). Details in section 3. |
| meta | B- / B- / n/a (C / C- / n/a; scripts D->B-) | code **agree**; tests **too high by 1** (C+): runner 0/193 lines, council retry/timeout/round-2/validator holes all "not fixed", 50 gate tests outside default discovery, and sol itself says "Tests >= B: not met"; scripts B- **agree**. |
| isa-spec | B- / B / C+ (C+ / B- / C) | code **too high by 1** (C+); tests **agree** (B); build **agree** (C+). Details in section 3. |

Tally: 16 graded dimensions; 11 agree, 5 too high by 1 step, 0 too low.

## 3. Independent deep re-grades

### 3a. bennett-isa-spec (the reference interpreter is the oracle)
Read: `classical.rs` `step_prepared` (:1468-1620, the CC execution core), `claims/pairs09.rs` `verify_inverse_pair_claim09`
(:382-470, the new entry-aware pair proof), `classical.rs::binop` (:1921), `object.rs` :1315-1325, `Cargo.toml`, plus the layout
of `main.rs` (2606), `borrow.rs` (2322), `classical.rs` (2115), the three largest files. Not read in full: `main.rs`, `borrow.rs`
beyond structure. Ran 70 tests myself (above) and one mutation probe.

**Mutation probe (new finding, not in the sol report).** In a scratch copy I changed `classical.rs:1922`
`let shift_out = b >= w as u128;` to `b > w as u128`. Effect: `ashr` of a negative value by exactly `w` yields -1 instead of 0,
violating §4.1 ("shift >= N -> 0 for all three shifts", quoted in the code comment at :1930). Result: **survived** `--lib` (32),
`cli_xam` (80), `step_machine`, `r1_widths` (16, including `ashr_by_n_or_more_is_zero_in_every_engine`), `bitvectors`, `oracle`,
`r1_fixtures` = 152 tests in 8 binaries, 0 failures. Reason: every `ashr` test (r1_widths.rs:206, oracle.rs:148, the conformance
cases `C-arith-ashr-ge-width` / `C-arith-ashr-negative`) goes through the oracle tier (`bits.rs`), never the CC tier's `binop`;
`grep` finds no CC-tier `ashr` program anywhere in either crate. Caveat: 575 reference tests and the conformance harness were not
run, and `shl`/`lshr` off-by-one is unobservable (masked), so this is one hole, not a rate. It is the kind of hole the baseline's
"B- tests" were supposed to price in; it shows the "gate would catch a wrong result" sentence holds per engine, not per spec clause.

**Test sample (10, seed 77 over 781 `#[test]`):**
| Test | Class | Why |
|---|---|---|
| k84_diagnostics.rs:29 `k84_vectors_reject_only_the_named_mutation...` | useful | sha-pinned fixture files, full-certificate equality, CLI `check` exit; expected object built by the same `certificate()` helper (mild self-reference) |
| isa09_cleanup.rs:205 `k81_repeated_source_iterations...` | useful | literal 16 leaves, ordinal `n % 8`, iteration `[n/8]`, 4 distinct allocation ids, reversal |
| cli_xam.rs:1385 `r7_cli_restored` (via `r7_cli_identity`) | weak | `canonical().contains(h)` substring against a pinned hash; right idea, loose match |
| cli_xam.rs:1307 `r6_cli_sol_boundary_exact` (via `r6_cli_map`) | weak | same wrapper pattern, substring containment |
| isa09_budget_mint.rs:452 `device_tokens_expire_when_their_owning_run_is_dropped` | weak | two bare `is_err()`; any error satisfies it |
| cli_xam.rs:1927 `r11_cli_rounded_and_exact_phase_probes` | useful | exact float state `-6.12323823339278e-17` vs exact `{"01":[1,0]}`; distinguishes rounded/exact modes |
| isa09_qinplace.rs:1021 `bound_reference_tree_checks_transitive_owner...` | useful | 4 parameter cases, `Established` enum and exact error substring "no covering inverse-pair entry in @inner" |
| conformance/ref_qinplace_contract.rs:63 `scheduled_action_adj_consumes...` | useful | hand-built registry, expansion output compared; synthetic but explicit |
| r1_fixtures.rs:119 `published_example_objects_are_the_fixtures_byte_for_byte` | useful | spec text extracted and compared byte-for-byte to fixtures (independent source) |
| isa09_forwarding.rs:199 `source_forwarding_bounded_materialisation...` | useful | 1,024-leaf bound, asserts host-capacity error; heavy twin correctly `#[ignore]`d |

7 useful / 3 weak / 0 tautological (sol: 16 / 2 / 0 of 18, 88.9%). Difference is within sampling noise (n=10 vs 18).

**My grades.**
- **Code C+** (sol B-). Evidence: the structural findings that defined the baseline C+ are unchanged by sol's own scanner:
  >300-line functions 8 -> 8, >100-line 59 -> 64, `oracle` still 1,088 lines, no-op preparation hooks, process tag
  (classical.rs:890), discarded binding (object.rs:1320), 7 tracked litter paths, no ratchet. What genuinely improved is
  correctness design (entry-bound pair proofs, explicit `Unverified` for scheduled claims, token lifetime), which I read in
  pairs09.rs and which is careful and fail-loud. That earns the "parked 0.9 paths" finding closure, not a full step on a
  maintainability-weighted scale. Also seen: `classical.rs:1600` `steps: self.bits(&a[1])? as u64` narrows u128 to u64 without a
  check (reachable width unverified, flagged not proven).
- **Tests B** (agree). Both baseline-red tests verified green; large exhaustive/oracle-backed core; but 108 `is_err()` sites,
  the CC-tier mutant above, and five ignored sweeps ungated keep it from B+.
- **Build C+** (agree). Cold two-binary test build 52.8 s on my machine; sol's 63-binary / >180 s default (278.86 s recorded,
  docs/quality.md) is why this stays C+; the 110 -> 44 MiB binary and opt-level=1 profile (Cargo.toml:10) are real.

### 3b. bennett-runtimes
Read in full: `src/native/heap.c` (215 lines), `src/runtime/integer_arithmetic.c` (160), `src/musl/vfs.c` lines 1-120 and 215-262
(of 328), the three largest source files. Ran 11 test scripts + `scripts/coverage` (all in section 1).

**What I found beyond the report:** 10 unchecked `malloc`/`calloc` dereferences in `vfs.c` (68, 104, 135, 136, 162, 164, 177, 198,
312, 317). I checked whether this is a fail-fast gap: it is not, because the allocator it calls faults (`bump.c:42/68`,
fault 2) rather than returning NULL, so the report is right not to list it. Heap.c `find`/`check` logic is a correct
binary search plus `prefix_end` interval index (comment at heap.c:200-203 matches the code). Integer division is a
restoring loop over `2*limbs*64` iterations per call; correctness rests on the Python big-int oracle, which I ran (217,459
cases for LLVM 23 plus the 8,388,608-bit `ctpop` case).

**Test sample (10, seed 5 over 70 fixtures/scripts):**
| Test | Class | Why |
|---|---|---|
| test_wide_allocators.py | useful | required export set, `allockind("alloc")` attribute check, exact `fault 2/4/2` stderr and SIGILL |
| transport_errors.c + test_transport_errors.py | useful | real host `write` errors/short writes injected via `__bennett_rt_native_os`; exit 125 asserted |
| libc_devices.c | useful | literal clock/entropy vectors (`1234.567890123`), `errno==EINVAL` and unchanged-state checks |
| native_contract.c | useful | saturates the heap with 0-size records, asserts address = base + i and fault 2 on overflow; expected values are literals |
| test_shadow_stack.py | useful | 8 faulting cases x O0/O2 x 2 majors, exact `bennett runtime fault N` bytes |
| test_process.py + process.c | useful | exact exit codes/stdout over 4 argv0 forms x 5 modes, `NEEDED` absent, no undefined symbols |
| test_process_apis.py | weak | first half is structure (`define @localeconv`, manifest contents); behaviour is only `run(exe)==b''` |
| test_runtime.py:36 | weak | `b'fault 7' in stderr` also accepts `fault 70` (sol records this) |
| sqlite_memdb.c | useful | read-only image, UPDATE must give `SQLITE_READONLY`, query result compared by the Python driver against sqlite3 |
| process.c (`CHECK(...)` returns `__LINE__`) | useful | argc/argv/envp/errno/fenv/atexit order each asserted; failure identifies the line |

8 useful / 2 weak / 0 tautological (sol: 15 / 3 / 0 of 18). Consistent.

**My grades.**
- **Code B-** (sol B). Of the baseline's four most serious code findings, only unowned-free is fully fixed; VLA is "partly" (up to a
  1 MiB core scratch and ~4-6 MiB product/division arrays remain on the stack at the 2^23-bit limit), the 4 KiB-per-object mmap and
  24 B/heap-byte history are "not fixed" (sol's own table), VFS re-entry is "not fixed". Small, clean, well-commented C; the step
  from B- is half a notch, so I hold at B-.
- **Tests B+** (agree). I reproduced the independent oracles (Python big-int, byte-set range oracle, host-glibc differential
  9 boundaries / 35 records). Note the quantified coverage is 20.93%, which sol reports honestly while withdrawing the baseline's
  80-90% estimate; I would not credit +1 step for the new measurement itself, only for the host-libc differential and the
  write-error fix.
- **Build A-** (agree). Clean build 8 s, hot incremental 1.7 s per sol; all my script runs 0.06-14 s. The 740 s push gate and
  171.77 s default are the cost that keeps it from A.

## 4. Scale calibration

Sol grades are **systematically softer than a re-derivation from its own evidence, by about 0.3 step per dimension**, while its
prose is harsher than the 2026-11-05 reports. Evidence count: 16 graded dimensions; every one moved up (mean +1.4 steps, range
+1 to +3 excluding meta's scripts D->B- and litter C->A); I would lower 5 of 16 by one step (dialect tests, dialect build,
runtimes code, meta tests, isa code), raise 0, giving a mean of +1.1. In all five the cause is the same: the report's own
"Against the baseline" table lists the baseline's headline finding as "not fixed" (dialect: independent labels; runtimes:
4 KiB/object and 24 B/byte history; meta: council retry/runner coverage; isa: eight >300-line functions) while the grade
still moves up a notch. Sol is also more candid than the baseline reports (it corrected three baseline premises: circuits'
"independent simulator" and "lonely `version()`", runtimes' weak-symbol finding), and its measured numbers I re-ran all
reproduced (210, 83, 35, 70 tests; 20.93%/17.02%/11.90%; 781 test count; function lengths exactly). So: numbers equal or better
than baseline quality, grade deltas about one-third of a step too generous, no sign of grade harshness anywhere.
Not independently checked: dialect-spec's timings/coverage (47 GB snapshot cache), meta's hook and gate tests (brief forbids),
isa-spec/circuits coverage percentages (instrumented runs not repeated).
