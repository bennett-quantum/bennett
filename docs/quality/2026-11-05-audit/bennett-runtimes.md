# bennett-runtimes quality audit 2026-11-05

## Verdict
- Code: B-. Small (1.6k LOC of handwritten C), commented against spec sections, fail-loud on faults; but a few fall-through paths, a VLA sized by user width, and a 4 KiB mmap per tracked object.
- Tests: B. Mostly oracle-backed (Python big-int oracle, byte-set reference, Python sqlite3, hard-coded goldens, fault code+stderr asserted exactly); weak spots are structural/regex checks of the .bc text and some trivially-sized fixtures. No coverage tooling.
- Build: B+. Deterministic and byte-reproducible (verified: my build of LLVM 18 equals dist/ bit for bit), 59 s per major, no incremental build (always full).
- Not a native differential against the host libc: see "Test quality".

## Composition
Excluded: vendor/ (4.1 MB on disk: musl 1.2.5 archive/sources, compiler-rt ubsan archives, upstream headers; not counted). dist/ (3.6 MB, 34 tracked generated .bc/.json files, 20.6k LOC of headers+JSON copied musl include) is committed build output, counted separately.

| Area (cloc, vendor+dist+.tmp excluded) | files | code LOC |
|---|---|---|
| src/ (C, .h, .S, .ll) | 27 | 1,632 |
| allocator/, device-models/, julia-shim/, libc-shims/ | 5 | 367 (mostly README; julia-shim/alloc.c is 44 lines of code) |
| scripts/ (py, bash, one 305-line native-check.cpp) | 12 | 656 |
| tests/ (35 py, 27 C/C++ fixtures) | 59 | 3,042 |
| docs/ | | small |
| dist/ (generated, tracked) | 232 | 20,579 |
| whole repo minus vendor | | 25,609 (cloc, includes dist) |

Handwritten non-test code is about 2.3k LOC; tests are 1.3x the code.

| Module | Purpose | LOC (wc) |
|---|---|---|
| src/allocator | bump.c (malloc/aligned/realloc over ISA primitive), language.c (Rust/C++/Julia entry points) | 109 + 52 |
| src/musl | syscall.c (syscall dispatch to device transports), vfs.c (in-memory VFS), context.c | 143 + 328 + 43 |
| src/runtime | integer_core/arithmetic (arbitrary-width limb kernels), shadow.c (shadow stack), control.c/.ll (EH/jumpbuf) | 90 + 160 + 87 + 18 + 38 |
| src/native | comparison-only native twin: heap.c (history, bounds checker), syscall, start | 215 + 42 + 30 |
| src/device | console/clock/entropy/block models, transports | 35 + 80 + 17 |
| src/fenv, src/libc | fenv record, memset/memmove, UTC | 81 + 27 + 17 |
| scripts | build.py (IR text rewriting, manifest), musl.py (extract + compile musl closure), integer_helpers.py (IR generator), native-check*(link drivers) | 217 / 84 / 62 / 305 |

Dependencies: no Cargo/CMake. Python stdlib only; LLVM 18 and 23 toolchains at /usr/lib/llvm-{18,23}/bin, GNU readelf, plus sibling repos bennett-conformance (ladder corpus) and bennett-arith (dist bitcode), pinned in gate.toml. Python `sqlite3` module plus a sqlite3.c amalgamation for the sqlite tests.

Authorship (71 commits, all committed as tobiasosborne): 40 with Co-Authored-By Claude Opus 5.5, 7 Sonnet 5.5, 2 Fable 5.1, 32 subjects `wip(codex job ...)` (45%, Codex runner commits; 24 of the reviewed ones also carry Claude trailers), remaining ~22 unmarked. Pure-Claude is under 50%; Codex share is at least 45%.

## Build and test times
Toolchain warm (LLVM installed, no target/ cache concept). `scripts/build` always rebuilds everything, no incremental mode; run via the offline script, output to a scratch dir.

| Step | Wall |
|---|---|
| scripts/build 18 (full, incl. musl closure) | 59.3 s (output identical to dist/llvm18/bennett-runtimes.bc, `cmp` ok) |
| warm "incremental" build | n/a (same 59 s; no incremental path) |
| cargo test --no-run | n/a (no Cargo; "compile" is inside each test) |
| test_alignment | 2.8 s |
| test_global_ranges | 2.5 s |
| test_control_helpers | 6.8 s |
| test_devices | 15.0 s |
| test_fenv | 19.0 s |
| test_shadow_stack | 32.9 s |
| test_integer_helpers (217,459 cases/major, 28 widths) | 51.1 s |
| test_realloc | 83.3 s |
| test_native (needs bennett-conformance + bennett-arith; ran green, hashtable goldens + hello, 2 layouts per major) | 279.3 s |
| Estimated gate | 2 builds twice (~4 min) + 29 test scripts; maintainer pins timeout_s=28800 (gate.toml). Not run (forbidden). test_sqlite_memdb alone is documented ~1500 s; not run. |

Tests: 29 python scripts in scripts/gate (each runs both majors), driving 27 C/C++ fixtures with 291 CHECK() + 73 assert() sites plus the Python-side asserts. Each script is one process, not a case list, so "number of tests" is 29 scripts / roughly 365 C assertion sites plus 217k generated integer cases. Ignored/skipped/red: 0 (grep for skip/xfail finds nothing); the known-missing symbols (`__bennett_rt_eh_match`, `fiber_switch`, `poll`) have no red test, they live only as a bead (acknowledged in the review). Run here: 9 scripts, all green (alignment, realloc, integer_helpers, native, global_ranges, fenv, devices, control_helpers, shadow_stack). Not run: musl, publication, sqlite, process, file_io, etc. (need sibling repos or are long).

## Coverage
No gcov/llvm-cov harness (code is freestanding C compiled to bitcode, tests run on separate native twins). Structural estimate only:
- Every src file is reached by at least one gate script by name or by linkage: bump.c (alignment, realloc, allocator_history), vfs.c/syscall.c (file_io, libc_routes, descriptor_close, sqlite_*), integer_* (integer_helpers), shadow.c (shadow_stack), fenv (fenv), devices (devices), native/heap.c (global_ranges, checked_native, native). Estimated line coverage 80-90% of src, branch coverage lower.
Weakest-tested areas:
1. src/native/syscall.c:11-17 console write failure maps host errors to dialect fault 8; flagged P1 in the review (brt-mab), no test.
2. src/musl/vfs.c re-entry state (namespace/cwd not reset; brt-tci); only single-entry flows tested.
3. julia-shim/alloc.c and src/allocator/language.c: one 91-line test (test_julia_alloc_abi.py) checks offsets/attributes by regex, not behaviour under a Julia runtime.
4. Missing EH match / fiber / poll helper families: no code, no test.
5. libc-shims and device-models directories contain only READMEs; the contract is tested only via the lifted models in src/device, and `stdin` read, getdents-type paths fault 8 untested beyond that.

## Test quality
Sampled 18 functions/scripts:

| # | Location | Class | Why |
|---|---|---|---|
| 1 | tests/test_integer_helpers.py:21-69 `expected()` | useful | independent Python big-int oracle for ~50 ops; wide exhaustive for w<=4, random+boundary for the rest |
| 2 | tests/test_integer_helpers.py:~150-175 case loop | useful | also asserts input unchanged and out-of-bounds sentinels intact |
| 3 | tests/global_ranges.c:21-45 `reference`/`probe` | useful | brute byte-set oracle vs binary-search checker over 12k probes incl. wrap |
| 4 | tests/test_realloc.py:25-29 | useful | exact fault code and stderr text asserted |
| 5 | tests/realloc.c:14-26 | useful | checks prefix preserved, tail zero, move on every realloc |
| 6 | tests/test_fenv.py:10-14 | weak | regex on IR text for the one `@__bennett_rt_fenv` definition; checks syntax not behaviour |
| 7 | tests/fenv.c:25-40 | useful | 5 modes x 32 flags x 32 masks against C library semantic table (cflags is a derived mapping from the same spec) |
| 8 | tests/test_devices.py:13-26 | weak | regex checks that globals have given initialisers/alignment (structure, no behaviour) |
| 9 | tests/test_devices.py:30-60 | useful but fragile | rewrites published IR by regex to insert undo journal; checks undo exactly, but a regex mismatch is guarded by `stores >= 20` only |
| 10 | tests/devices_history.c:35-45 | tautology risk | test journal re-implements allocator history (`__bennett_nz_alloc`) used as the oracle for the real allocator wrapper |
| 11 | tests/test_native.py:19-21 GOLDEN | useful | hard-coded hashes from corpus programs (stored expected output) |
| 12 | tests/test_native.py:77-96 layout matrix | useful | 8 invalid layouts each with exact code (125/infra vs fault 2) |
| 13 | tests/test_native.py:97-107 | useful | forces RLIMIT_AS 128 MiB to prove infra-failure path |
| 14 | tests/test_musl.py:23-30 fixtures | weak | 5 tiny hello/printf programs; fine as smoke, outputs are literal strings |
| 15 | tests/test_publication.py:20-45 | weak/tautological | manifest SHA-256 checked against files the same build wrote |
| 16 | tests/test_shadow_stack.py:20-26 | useful | O0/O2, 8 fault cases each with expected code |
| 17 | tests/test_alignment.py:14-17 | useful | six named histories, exe asserts internally |
| 18 | tests/test_sqlite_memdb.py:31-36,104 | useful | Python sqlite3 builds the DB and the oracle `expected(i)`; 1,026 rowids each compared |

Ratio of the 18: useful 12, weak 4, tautological/risky 2. The suite is oracle-backed: Python integers, byte-set reference, Python sqlite3, stored goldens, and exact fault codes. It is NOT a differential against real native execution of the host libc: the "native" side is the repo's own hand-written comparison twin (src/native/heap.c, native syscall/start; "same-source native binaries" in the review). That twin and the production allocator both come from the same author and the same reading of the dialect, so shared misreadings of the spec would pass. Differentials that are genuinely external: Python sqlite3 (sqlite tests), Python int arithmetic, upstream musl source compiled unmodified.

Would the gate catch a wrong result? Yes for arithmetic, bounds checking, fault codes and byte output (asserted exactly; a flipped bit in any of 217k integer cases fails). It would not catch: spec drift (SPEC_VERSIONS pins dialect 0.2.10 while the registry is at 0.2.13 per the review), missing helper families, and host-error handling (native/syscall.c).

Gate wiring: scripts/gate rebuilds both majors, `cmp`s every artifact with dist/, then runs 29 scripts; every tests/test_*.py is listed (verified by the review and by me comparing test_ file names; test_varargs_fixture is in the list). `set -euo pipefail` so a red test fails the gate.

## Code quality
Existing review: docs/reviews/2026-11-03-runtimes-batch.md (P0 close, P1 libc routes, helper closure, console-write fault) reports CLEAR after round 2; not repeated. New findings:

1. src/allocator/bump.c:86 `free()` falls through silently when the pointer has no C record ("raw allocations can be freed without a C record"). Scenario: a double-free of a block that was recorded earlier is caught by `__bennett_nz_free` only because nz_free tracks liveness; if a pointer is valid for the primitive but not C-owned (interior alloc'd by raw rt_alloc) it is freed anyway. Intentional but undocumented in the spec link.
2. src/runtime/integer_core.c:~20 `uint64_t result[limbs]` is a stack VLA sized by width; the test exercises 8,388,608-bit (1 MiB stack). A consumer with a smaller shadow/stack budget overflows; no bound check before the VLA.
3. src/native/heap.c:149 `object()` mmaps a full 4096-byte page per tracked input/stack object (argv, each env string, every byval/alloca); 100 env vars cost 400 KiB, a loop with allocas that does not `leave` leaks pages. Cost, not correctness; loud only on mmap failure.
4. src/native/heap.c:106 per-heap-byte history (24 B per byte), a 2 GiB heap limit needs 48 GiB virtual; confirmed by review as infrastructure failure. Linear `find` in bump.c:77-84 and 91 (free/realloc walk the list): O(n) per free.
5. src/native/heap.c:36 `!&__bennett_rt_native_object_count` tests the address of a weak/extern for null (works for weak, but object_count is not declared weak in the shown lines); weak-symbol pattern repeated at heap.c:8-11, 189 as flags-by-symbol-presence ("lonely interface" smell: ss_check optional).
6. scripts/build.py:41-60 patches LLVM IR text with regexes (`re.subn` on `%struct.` types; allockind injected into .ll). Assertions on count==1 make it fail loud, but it is fragile to clang output changes across majors; each regex is a single-use helper.
7. 13 lines >200 chars in scripts/tests (e.g. test_integer_helpers.py adapter generator, build.py:20 SOURCES), long &&/|| chains in heap.c:93-95 and test_publication.py asserts. Python tests use dense one-liners with no functions; most gate scripts are straight-line top-level code (no functions, no reuse): `run()` helper is copy-pasted into ~20 scripts (tests/test_realloc.py:11, test_native.py:15, test_shadow_stack.py:12, ...), a duplication of ~6 lines each; test_integer_helpers.py is a single 120-line loop body.
8. Bead reference left in source: julia-shim/README.md:18 (brt-zct); none in .c. Only 1 hit, so policy is mostly followed (the review's brt-3fe nit covered the other).
9. build wrappers override caller TMPDIR (review nit brt-3fe), and tests hard-code `/usr/lib/llvm-{18,23}` paths with no env override.
Complexity hotspots (visual, no tool run): heap.c `__bennett_rt_native_check` (30 lines, 6 branches), vfs.c (328 lines, largest file), integer_core.c `integer_op` switch, test_integer_helpers.py main loop. No dead code found in src; all exports are referenced from the manifest checks.
WIP litter tracked in git: none outside vendor/dist (HANDOFF.md and worklog/001 are normal docs; `git ls-files` shows no .orig/.wip). dist/ is committed generated output (34 files, 3.6 MB, `git ls-files dist`), which is why every source change also needs a rebuilt dist commit and the gate cmp's it.

## What is good
- Byte-reproducible builds: scripts/gate rebuilds both majors, including from a relocated tree, and cmp's against dist; my 59 s LLVM 18 rebuild matched exactly.
- tests/test_integer_helpers.py + scripts/integer_helpers.py: 217k cases over 28 widths vs an independent Python oracle, exhaustive for w<=4, plus the 8 Mbit width.
- Faults are fail-loud with distinct, asserted exit conventions (fault N via SIGILL + stderr, 125 for infrastructure failure), not silent fallbacks (src/native/heap.c:60-88).
- tests/global_ranges.c: brute byte-set reference cross-check of the binary-search range index, with wraparound cases.
- Tiny surface: ~2.3k handwritten LOC with spec-section comments on nearly every function.

## Recommendations
1. Add a test (and fix) for native console write failure mapping to exit 125 not fault 8 (src/native/syscall.c:11, open as brt-mab).
2. Replace the VLA in src/runtime/integer_core.c with a width-bounded check or caller-provided scratch and test a smaller-stack failure.
3. Add a real differential against host clang/gcc-compiled musl or glibc for the printf/stdio and allocator behaviours (currently native twin is self-authored), so shared misreadings of the spec surface.
4. Extract the copy-pasted `run()` and layout-writing helpers in tests into one tests/common.py (about 20 copies).
5. Give scripts/build an incremental mode or per-file caching (59 s x2 majors x2 in gate) and let TMPDIR/LLVM paths be overridden.
6. Add a red-by-design (xfail) listing or manifest check for missing eh_match/fiber_switch/poll so the gap is visible in the gate, not only in a bead.
7. Update SPEC_VERSIONS.toml pins (0.2.10 vs registry 0.2.13) and the stale julia-shim/README.md bead reference.
