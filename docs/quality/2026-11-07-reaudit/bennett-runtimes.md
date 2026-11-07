# bennett-runtimes quality audit 2026-11-07

## Verdict
- **Code: B.** Correctness boundaries improved; large valid stack scratch, expensive native metadata and dense VFS dispatch remain.
- **Tests: B+.** Independent integer, byte-range and now host-glibc oracles check results; measured coverage still covers only a narrow harness.
- **Build: A-.** Offline publication reproduces exactly; content caching makes the measured warm rebuild 1.71 s.
- No new P0/P1 failure reproduced in the exercised paths. Full default and push-suite success are not established by this audit.

## Scope and method
Audited origin/main **6c7a588e4cd3ee102182f229ab8953217ebebabe** in the main checkout.
Checkout HEAD was **6893225a90d29661becba195282ecd0dbee19d7f**; `git diff --stat origin/main HEAD` showed only `.beads/issues.jsonl` (3 insertions, 2 deletions).
All source, tests, configuration and publications therefore match origin/main. The checkout was clean before and after measurement.
Recorded at **2026-11-07 10:20:40 UTC**. Auditor: gpt-6.1-sol, xhigh; read-only except this report and repository-local audit scratch.

Read the binding briefs, ecosystem README, policy, remediation plan, baseline report/synthesis, repository laws/README and all three existing reviews.
Closely read the three largest source files (`src/musl/vfs.c`, `src/native/heap.c`, `src/runtime/integer_arithmetic.c`) and three largest test files (`tests/test_native_byval.py`, `tests/test_integer_helpers.py`, `tests/devices_history.c`), plus changed boundaries and tooling.
Paths below are relative to `/home/tobias/Projects/bennett-workspace/bennett-runtimes`.
Scratch: `/home/tobias/Projects/bennett-workspace/bennett-runtimes/.tmp/reaudit-2026-11-07`.

## Composition
Measured with `cloc --json --quiet <absolute-area-path>` (1.98); code LOC excludes blanks/comments.
Cloc deduplicates identical files: the dist row is unique text, not the sum of both identical sysroots. Archives and bitcode are not text LOC.

| Area | Counted text files | Code LOC | Main languages |
|---|---:|---:|---|
| src/ | 27 | 1,635 | C 1,450; headers 95; LLVM IR 35; assembly 10; Markdown 45 |
| scripts/ | 16 | 951 | Python 676; C++ 157; shell 118 |
| tests/ | 76 | 3,467 | Python 1,792; C 1,521; C++ 148; TOML 6 |
| julia-shim/ | 2 | 46 | C 30; Markdown 16 |
| allocator/, device-models/, libc-shims/ | 3 | 321 | Markdown only |
| dist/ | 233 unique text files | 20,649 | Headers 16,445; JSON 3,050; copied sources/other text 1,154 |
| vendor/ | 4 counted text files | 56 | Archive inputs excluded from LOC |

Handwritten implementation/tool code: **2,571 LOC** (src without its README + scripts + Julia C); tests contain **3,461 executable-language LOC**, about 1.35 times that.
`git ls-files dist`: **496 tracked files, 2,167,403 bytes**; each major publishes 248 files.
Generated and vendored content is kept separate from handwritten quality judgments.

| Top-level source module | Purpose | Physical lines, including headers/comments |
|---|---|---:|
| src/allocator | C ownership/alignment/realloc; C++/Rust allocation ABIs | 162 |
| src/device | Lifted console/clock/entropy/block state and effect transports | 132 |
| src/fenv | Shared rounding/flag record and libc fenv mapping | 81 |
| src/libc | Memory helpers and UTC calendar bridge | 44 |
| src/musl | Process context, syscall routing, data-image VFS | 535 |
| src/native | Comparison-only Linux primitives, range metadata, startup/diagnostics | 334 |
| src/runtime | Limb arithmetic, shadow stack, control helpers, internal headers | 503 |

Dependencies: no Cargo/CMake/package-manager dependencies; Python imports are stdlib plus local modules (26 distinct top-level import names).
Runtime/tool inputs: musl 1.2.5 plus **2 explicit patches** (`scripts/musl.py:8`), compiler-rt archives for 2 LLVM majors, SQLite amalgamation for tests, LLVM 18/23, patch/sed/readelf/system tools.
Two pinned test/link dependencies: conformance `b077ae2a22e73b2321dcfe2fccede885f47b8d89`, arith `aab308f8305e92d4946d1ea302af1ea196a27bb3` (`gate.toml:19`, `:23`).
Both cached checkouts' actual HEADs were checked with `git -C <absolute-pin-checkout> rev-parse HEAD`; both match.
No sibling source was used as implementation guidance.

Authorship: `git log origin/main --format=%an%x09%s%x09%B%x00`, 87 commits, all under the repository's common human author identity.
Non-exclusive marker counts: Codex 46/87 (**52.9%**), Claude 50/87 (**57.5%**).
Disjoint: Codex-only 14 (**16.1%**), Claude-only 18 (**20.7%**), both 32 (**36.8%**), unmarked 23 (**26.4%**).
Markers were `wip(codex job`, GPT Agent/coauthor trailers, or Claude/Opus/Sonnet/Fable/Haiku trailers; unmarked does not establish human authorship.

## Build and test times
Every measured build/test ran sequentially in a named `systemd-run --user --scope`, headless, with scratch TMPDIR, `timeout 600`, `ulimit -v 8000000`, and core dumps disabled.
The original slot rule was checked before each invocation: free -g available 20–23 GB, one-minute load 8.68–11.90 (<12).
The later load<8/no-bennett-heavy/30-minute rule applies to subsequent work; no long build/test was launched afterward.
The Python builders invoke one compiler at a time and expose no -j option; MAKEFLAGS=-j3 and CMAKE_BUILD_PARALLEL_LEVEL=3 were set; there was no Cargo invocation.
Results and exact argv are in scratch `results.json`; each time uses `/usr/bin/time -f %e`, excluding slot waits/scope setup.

| Command inside the measurement scope | Wall seconds | Result |
|---|---:|---|
| Scratch-copy scripts/build 18 <scratch>/clean18 | 8.26 | Clean publication; all 248 files equal dist/llvm18 |
| Same source, --incremental, empty audit cache | 8.36 | 0 hits / 298 misses; cache priming |
| Same --incremental after touching scratch src/libc/memory.c | 1.71 | 298 hits / 0 misses; all 248 files equal dist |
| Same --incremental after adding a comment to that scratch source | 2.10 | 297 hits / 1 miss; production bitcode unchanged |
| cargo test --no-run / compile-only suite | n/a | No Cargo; fixture compilation is included in each script |
| python3 -I tests/test_quality_ratchet.py | 0.05 | PASS |
| python3 -I tests/test_build_cache.py | 0.15 | PASS |
| python3 -I tests/test_host_libc.py | 6.09 | PASS, both majors |
| python3 -I tests/test_alignment.py | 0.64 | PASS, both majors |
| python3 -I tests/test_global_ranges.py | 0.75 | PASS, both majors |
| python3 -I tests/test_integer_helpers.py | 15.41 | PASS, 217,459 cases/major plus maximum-width count |
| python3 -I tests/test_integer_width.py | 0.97 | PASS, 9 invalid-width/operation combinations/major |
| python3 -I tests/test_free_ownership.py | 0.52 | PASS, both majors |
| python3 -I tests/test_transport_errors.py | 0.88 | PASS, both majors |
| python3 -I tests/test_control_helpers.py | 14.40 | PASS, both majors |
| python3 -I tests/test_fenv.py | 4.01 | PASS, both majors |
| python3 -I scripts/coverage | 1.99 | PASS; coverage below |

**11 fast scripts: 43.87 s combined, zero unexpected failures.** Compilation caches began empty in audit scratch; installed tools and OS page cache were warm.
The baseline's 59.3 s clean build ran under different host load. Only the present same-run clean/cached comparison supports a speedup attribution.

Inventory: **38 test scripts = 13 fast + 24 slow + 1 promised** (`tests/suites.toml:1`).
A separate TOML/glob inventory comparison found 38 entries, 38 unique, and exact equality with all test_*.py files.
C/C++ fixtures contain 317 CHECK tokens (including macro declarations) and 79 assert sites; these are assertion counts, not separate tests.
Missing helper inventory: 3 symbols × 2 publications; no ignored capability is counted as passing.
Two fast scripts were not executed: test_common creates a scratch Git commit (`tests/test_common.py:35`), prohibited by this brief; test_gate_selection invokes scripts/gate (`tests/test_gate_selection.py:11`).
All 24 slow scripts, the default gate wrapper, full push gate, heavy/ladder/conformance runs, and the relocation test writing outside audit scratch were excluded.
Default 171.77 s and full-gate 739.8 s are prior claims in `docs/quality.md:3` and `docs/reviews/2026-11-07-runtimes-gatefix-r1.md:34`; neither was rerun here.
Optional repeat CLI ratchet/promised-helper runs were cancelled while waiting behind a heavy scope; the completed metric comparison and llvm-nm inventory supply the evidence below. No 30-minute slot-timeout claim is made.
LLVM 23 clean/cached publication rebuild was not measured; its focused tests and all 41 manifest source digests were checked.
LLVM 18 also had all 41 manifest source digests checked with zero mismatches.

## Coverage
Fresh `python3 -I <absolute-repo>/scripts/coverage` reproduced the recorded LLVM 23 hosted profile.
It compiles every handwritten src C file and julia-shim/alloc.c, retaining unexecuted objects in the denominator (`scripts/coverage:26`).

| Metric | Executed / total | Coverage |
|---|---:|---:|
| Lines | 261 / 1,247 | **20.93%** |
| Functions | 24 / 141 | **17.02%** |
| Branch outcomes | 168 / 1,412 | **11.90%** |
| Regions | 293 / 2,138 | 13.70% |

This is **not full-suite coverage**: three hosted harnesses exercise alignment, global ranges and small unsigned integer operations (`scripts/coverage:43`).
Python tooling, native-check.cpp, LLVM IR/assembly, generated helpers and vendored musl are excluded.
The old 80–90% structural estimate is not a comparable measurement and is withdrawn as a quantitative coverage claim.
Even substantial focused execution here does not enter this profile unless the instrumented harness invokes it.

Five largest weakly represented areas, ranked by unexecuted profile lines:

| Area | Profile lines | Existing test reach / limitation |
|---|---:|---|
| VFS | 0 / 278 | file_io/libc_routes exercise namespace/sparse-file semantics; re-entry reset remains unresolved (`src/musl/vfs.c:49`) |
| Syscall/process context | 0 / 139 | process/device/file scripts exist; instrumented entry/flush boundary absent (`src/musl/syscall.c:48`, `src/musl/context.c:28`) |
| Device models/transports | 0 / 82 | Published-store undo and checked range scripts exist; no source profile integration (`tests/test_devices.py:35`) |
| Shadow stack | 0 / 68 | O0/O2 lifetime/fault matrices exist in the slow suite (`tests/test_shadow_stack.py:20`) |
| Fenv | 0 / 62 | Fresh both-major semantic/fault tests passed; coverage harness does not link them (`tests/test_fenv.py:23`) |

Also 0% here: language/Julia allocation (47 lines), native console/syscalls (35), memory/UTC (25), startup/sanitizer/control.
These are instrumentation gaps, not proof that all those lines lack tests.
Remaining unsupported mechanics are a separate absence of implementation, not missing coverage of implemented bodies (`src/runtime/README.md:47`).

## Test quality
Reproducible random sample: seed **20261107**, 18 functions sampled without replacement from 24 assertion-bearing C/C++ fixture functions recognized by a brace scanner.
This is a bounded fixture-function population, not a claim of uniform sampling across generated cases or Python top-level scripts.
Harness helpers remain in the sample and are explicitly classified; source/line references were checked against definitions.

| Function | Class | Why |
|---|---|---|
| tests/process_apis.c:26 main | Useful | Asserts page size and errno reset against literals plus locale obligations |
| tests/sqlite_libc.c:13 main | Useful | Exact string/bounds/calendar vectors and overflow, rather than successful linking alone |
| tests/file_io.c:9 main | Useful | Asserts bytes, offsets, EOF/error/reset, truncation and sparse growth |
| tests/libc_devices.c:29 main | Useful | Fixed clock/tape/disk witnesses and effect-position checks |
| tests/allocator_history.c:16 test_record | Weak | Bounds the test journal; does not itself assert a runtime result |
| tests/checked_ranges.c:21 main | Useful | Enumerates live/dead/adjacent/zero/wrapped ranges against independent interval predicates |
| tests/devices_history.c:61 check_out_reset | Weak | Sentinel helper alone; its caller supplies the undo/re-execution assertion |
| tests/descriptor_close.c:14 main | Useful | Exact EBADF and zero-effect checks after close, including preparation reset |
| tests/coverage_integer.c:6 main | Useful | Exhaustive 1–8-bit operations compared with native arithmetic/count/reversal |
| tests/fenv.c:20 main | Useful | 5×32×32 state vectors plus independently derived halfway-rounding witness |
| tests/realloc.c:5 main | Useful | Exact retained prefix, zero tail, move policy and invalid-pointer branches |
| tests/devices_history.c:24 test_record | Weak | Validates harness capacity only; product semantics live in its callers |
| tests/wide_allocators.c:26 main | Useful | Many alignment residues, forward-size windows, overflow/error preservation |
| tests/global_ranges.c:31 probe | Useful | Actual range checker compared with a brute byte-set oracle |
| tests/allocator_history.c:39 run | Useful | Hand-pinned allocation/cursor histories and payload content |
| tests/allocator_history.c:54 main | Useful | Two executions around byte-exact reversal expose stale runtime state |
| tests/libc_differential.c:8 main | Useful | Same defined C program on host glibc and published musl; exact process/output comparison |
| tests/alignment.c:36 main | Useful | Independent heap offsets/budget histories, zero fill and overflow ordering |

Sample ratio: **15 useful / 3 weak / 0 tautological** (83.3% / 16.7% / 0%); no statistical extrapolation to all scripts.
Targeted Python checks outside that sample: integer_helpers compares 434,918 fresh cases across both majors with Python big integers and guards input/sentinel bytes (`tests/test_integer_helpers.py:125`).
Host-libc differential checks 9 allocation boundaries and 35 formatting records per major, exact exit/stdout/stderr (`tests/test_host_libc.py:16`, `tests/libc_differential.c:9`).
It does not yet cover float formatting, allocator exhaustion, all stdio error paths, or whole-program Julia.
Julia coverage is stronger than the baseline describes: actual stock-frontend boxed method is linked and executed before/after LTO (`tests/test_julia_alloc_abi.py:50`); not rerun here.
Structural fenv/device/layout checks still supplement execution; publication hashes establish integrity, not semantic correctness (`tests/test_publication.py:48`).
The journal supplies the primitive contract while testing the actual allocator/model body; this is a shared-contract risk, not an automatic tautology (`tests/devices_history.c:35`).

Would the gate catch wrong results? For the tested arithmetic, allocation histories, ranges, fault paths and byte output, yes: exact expectations make bit flips observable.
`scripts/gate:46` uses check=True, and `gate.toml:13` selects --all: all fast+slow scripts and clean reproduction remain on the push route.
It would not prove missing helper implementation or complete ISA/driver/rung acceptance; promised mode reports separately, and symbol presence alone would still need semantics (`tests/test_promised_helpers.py:25`).
One known weak diagnostic assertion remains: substring `fault 7` accepts `fault 70` (`tests/test_runtime.py:36`), already recorded in the gatefix review.

## Code quality
Existing findings/reviews are not presented as newly discovered: see `docs/reviews/2026-11-03-runtimes-batch.md`, `2026-11-06-quality-runtimes-r1.md`, `2026-11-07-runtimes-gatefix-r1.md`.

| Remaining finding / cost | Evidence and consequence |
|---|---|
| Width admission is bounded, execution stack use is still large | `src/runtime/integer_core.c:20`, `integer_arithmetic.c:96` and `:117`: at 2^23 bits core scratch is 1 MiB, product arrays 4 MiB, division arrays ~6 MiB. Small execution stacks can still fail on valid inputs; the new regression covers invalid widths only. |
| Native metadata scales with heap capacity, plus a page per object | `src/native/heap.c:106`, `:149`: 24 bytes per heap byte reserves 48 GiB for a 2 GiB configured heap; every input/stack object maps 4 KiB for a 24-byte record. Allocation failure exits loudly as infrastructure, but cost is high. |
| Linear ownership lookup and dense VFS dispatch | `src/allocator/bump.c:76`, `:92`, `src/musl/vfs.c:224`: free/realloc scan live allocations; syscall-number policies and cleanup are interleaved in one 105-line metadata function. Large allocation populations make repeated frees quadratic in aggregate. |
| Process preparation retains namespace/cwd | `src/musl/vfs.c:37`, `:49`: preparation replaces descriptors only. Existing review's re-entry concern remains; context explicitly assumes fresh static images (`src/musl/context.c:1`). |
| Publication edits depend on textual LLVM shape | `scripts/build.py:62`, `:66`, `:80`: layout replacements fail loudly with count assertions; allocator-attribute injection uses re.sub without its own count assertion. Toolchain-shape drift still needs export/attribute tests and reproducibility. |
| Some slow tests ignore caller TMPDIR | `tests/test_runtime.py:12`, `test_publication.py:18`, `test_musl.py:13`, `test_reproducibility.py:11`: hard-coded shared scratch paths defeat per-job isolation; seven test scripts have this pattern. |
| Documentation/tool override nits remain | `README.md:4` differs from the correct commit in `SPEC_VERSIONS.toml:5`; `tests/test_promised_helpers.py:14` still hard-codes LLVM paths. Already noted in quality review. |

Measured complexity via `scripts/quality.py::measure` (AST Python / lexical C proxy): **184 functions**, **23 >20 lines**, **6 >50**, **3 >100**, **0 >300**; complexity mass **1,395**, forwarding-wrapper count **34**.
Largest spans: build() **203 lines** (`scripts/build.py:33`), native-check main body **156** (`scripts/native-check.cpp:17`), VFS meta **105** (`src/musl/vfs.c:224`), integer arithmetic **87** (`src/runtime/integer_arithmetic.c:73`).
Independent comment/string-stripped brace-depth scan: VFS and native-check **6**, integer_core **5**, integer_arithmetic **4**; includes the function-body level and initializer braces, not semantic nesting.
C macro-generated ABI wrappers are not fully represented by this lexical function inventory; these measurements are reproducible proxies.
Most forwarding wrappers are required language/effect ABI adapters (`src/allocator/language.c:23`), not evidence that all 34 should be deleted.
Test runner duplication is largely removed; one nested shadowing run() remains (`tests/production_support.py:12`).
No dead production implementation identified; three promised helper bodies are absent, not dead code. Readme-only allocator/device/libc directories describe implementations located under src.
Tracked litter grep returned **0**, production process-identifier scan **0** (the metric's own detector excluded); HANDOFF.md is untracked/absent.
Fresh metric-versus-recorded-baseline comparison returned **[] regressions**; mutation tests for metric regressions passed in 0.05 s.

## Against the 2026-11-05 baseline
Grades use the same letter scale, independently re-derived from current correctness evidence, oracle independence and measured iteration cost.

| Grade | Baseline | Current | One step higher requires |
|---|---|---|---|
| Code | B- | **B** | B+: verify bounded valid-width stack/resource handling and simplify the highest-cost VFS/metadata paths |
| Tests | B | **B+** | A-: instrument the existing stdio/VFS/device/shadow/fenv tests and widen independent negative/error-path oracles |
| Build | B+ | **A-** | A: freshly verify both-major clean/cached/relocated publication and the entire bounded default within 180 s |

Every numbered baseline code finding:

| Baseline finding | Status | Current evidence |
|---|---|---|
| 1. Unowned free falls through | Fixed | `src/allocator/bump.c:86`; both-major pre-mutation fault regression passed |
| 2. Caller-width VLA | Partly | `integer_core.c:17`, `integer_arithmetic.c:75` bound admission; large valid automatic arrays remain |
| 3. 4 KiB per native object | Not fixed | `src/native/heap.c:149` still maps one page per record |
| 4. 24 B/heap-byte history and linear C ownership lookup | Not fixed | `src/native/heap.c:106`, `src/allocator/bump.c:76` |
| 5. Weak-symbol address check allegedly lacks weak declaration | Not fixed; baseline premise rejected | `src/native/layout.h:18` and `:19` declare both weak; `git show 849fa2e:src/native/layout.h` confirms this predates remediation |
| 6. Regex IR rewrites | Not fixed | `scripts/build.py:62` and `:80`; count-guarded layout edits remain |
| 7. Dense tests/long Boolean chains/20 runner copies | Partly | Shared `tests/common.py:17` replaces script-level copies; `production_support.py:12` retains a nested runner; dense top-level integer matrix and heap layout predicate remain |
| 8. Julia README bead reference | Fixed | `julia-shim/README.md:18` now points generically to issue database |
| 9. TMPDIR/LLVM hard-coding | Partly | `scripts/build:5`, `tests/common.py:14` honor overrides; seven legacy scratch paths and promised nm path remain |

Baseline coverage/test concerns: native write errors **fixed** (`src/native/syscall.c:16`, fresh error matrix); VFS re-entry **not fixed** (`vfs.c:49`); Julia ABI-only characterization **partly fixed/corrected** by actual emitted-body execution (`test_julia_alloc_abi.py:50`).
EH/fiber/poll implementation **not fixed**, visibility **fixed** (`tests/promised-helpers.toml:4`); README-only module directories and unmodelled input paths **not fixed**, with actual model code still under src.
Fenv/device structural checks **not fixed as checks**, but remain supplementary to semantic vectors (`test_fenv.py:23`, `test_devices.py:68`).
Publication self-hashes **not fixed as semantic oracles**; they remain appropriate integrity checks (`test_publication.py:48`).
The old devices primitive/journal “tautology risk” is **partly mitigated**, not eliminated: actual bodies plus independent host-libc standard-behavior checks reduce shared-reading risk; reversal still relies on a test primitive (`devices_history.c:35`).

| Baseline recommendation | Status | Evidence |
|---|---|---|
| 1. Host-write failure -> exit 125 + regression | Fixed | `tests/test_transport_errors.py:20`; fresh ENOSPC/EBADF/EPIPE/EAGAIN/invalid-write matrix passed |
| 2. Bound VLA or provide scratch; small-stack test | Partly | `tests/test_integer_width.py:13` tests invalid widths on 64 KiB stack; valid-width stack demand persists |
| 3. Real host libc stdio/allocator differential | Fixed for bounded slice | `tests/test_host_libc.py:16`; both glibc comparisons passed, 9 sizes/35 records |
| 4. Shared run/layout helpers | Fixed substantially | `tests/common.py:17`, `:33`; one nested duplication remains |
| 5. Incremental build and TMPDIR/LLVM overrides | Fixed for builder | `scripts/build.py:41`, `scripts/build:5`; 298/0 hot-cache result; scratch-source change caused one miss |
| 6. Visible promised-helper inventory | Fixed visibility; capability not fixed | `tests/promised-helpers.toml:4`; llvm-nm confirms all 3 absent on both majors |
| 7. Spec pin and stale Julia bead reference | Partly | Correct dialect 0.2.13 pin in `SPEC_VERSIONS.toml:4`; Julia reference removed; README commit typo remains |

SYNTHESIS.md's runtimes concerns (self-authored native twin, missing coverage, no incremental mode, stale pins/fail-fast) are addressed as above.
The native twin remains self-authored, but there is now an additional independent glibc comparison; neither component evidence nor 20.93% profiling is whole-rung acceptance.
No observed regression was reproduced; the lower coverage headline is a measurement-method change, not evidence of lost coverage.

## Plan targets
“Not met (unverified)” below means the audit did not establish the exit criterion; it does not assert a red default.

| Applicable Targets item | Status | Command + result / evidence |
|---|---|---|
| No red default main | Not met (unverified) | 11 scoped `python3 -I <repo>/tests/test_*.py` runs: all PASS; complete 13-script default prohibited/unrun here |
| No live sibling reads instead of pin | Met | `git -C <absolute cached sibling> rev-parse HEAD`: both pins exact; `rg -n pinned_sibling <repo>/tests <repo>/scripts` and source sweep found pin resolution for every sibling input (`scripts/pinned_sibling.py:10`) |
| Measured coverage in docs/quality.md | Met | Scoped `python3 -I <repo>/scripts/coverage`: 20.93% lines, matching `docs/quality.md:22`; function/branch values recorded above |
| Default equivalent under 180 s; slow tests assigned | Not met (complete timing unverified) | TOML/glob inventory: 13 fast/24 slow/1 promised, no omissions; 11 fast scripts total 43.87 s; documented 171.77 s not independently rerun |
| Test grade >= B | Met | 18-function classification + fresh exact-oracle tests: B+ |
| Code grade >= B- | Met | Source inspection, boundary regressions and complexity scan: B |
| No >300-line semantics functions in fixed files; others owned | Met in measured scope | `scripts/quality.py::measure`: 0 >300 across 184 detected functions; maximum 203; macro/parser limitation stated above |
| No bead/job identifiers in product source/output | Met in measured scope | Fresh `measure()` process_identifiers=[]; `scripts/quality.py:95` excludes the detector itself |
| No tracked pycache/log/lock/backup/LAST-RUN litter | Met | `git ls-files` plus LITTER regex: []; zero tracked matches |

Additional round-1 items: quality metric baseline/ratchet exists and fresh metrics match (`scripts/quality.py:107`, `gate.toml:17`); local HANDOFF retired, README links central coordination (`README.md:223`).
Repository-specific targets: host-write fault, free ownership, shared test support, incremental build and host-libc slice verified; integer-stack safety and helper implementation remain partial.

## What is good
- Actual publication bytes reproduce across source location and cache state for the measured LLVM 18 build: 248/248 files identical.
- Python integer oracle preserves exact values, overflow flags, immutable inputs and output guards (`tests/test_integer_helpers.py:147`).
- Byte-set range oracle tests overlapping/adjacent/wrapping object bounds (`tests/global_ranges.c:21`).
- Real host failure matrix distinguishes infrastructure exit 125 from dialect faults (`tests/test_transport_errors.py:47`).
- Independent host-glibc comparison is additional to the runtime-specific primitive/history tests (`tests/test_host_libc.py:26`).

## Recommendations
1. Extend the existing coverage harness to VFS/syscall, devices, shadow and fenv before using coverage to judge the whole runtime (`scripts/coverage:43`).
2. Add an explicit valid-width stack/resource contract and a small-stack valid-width witness; preserve the full admitted width range (`src/runtime/integer_arithmetic.c:117`).
3. Make the seven remaining test scratch roots honor TMPDIR so parallel audits/tests cannot overwrite one another (`tests/test_runtime.py:12`).
4. Keep the re-entry limitation visible and define/test namespace/cwd preparation behavior (`src/musl/vfs.c:49`).
5. Have orchestration freshly verify all 13 default scripts under 180 s and both-major clean/cached relocation; this audit cannot certify those aggregate targets (`tests/suites.toml:1`).
6. Tighten the existing substring fault assertion to the complete diagnostic/token (`tests/test_runtime.py:36`; already reviewed).
7. Correct README's dialect SHA and route promised-helper nm through the shared LLVM resolver (`README.md:4`, `tests/test_promised_helpers.py:14`).
