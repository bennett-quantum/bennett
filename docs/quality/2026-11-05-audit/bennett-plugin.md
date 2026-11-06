# bennett-plugin quality audit 2026-11-05

## Verdict
- Code: C-. Correct-looking and fail-loud in spirit, but 528-line and 499-line functions, 531-column lines, and an uncaught `.at()` abort on a tracked probe.
- Tests: B-. Many are oracle-backed (spec fixtures, reference interpreter, Python integer models), but they are minified one-file scripts and two of the six I ran are red on a clean tree.
- Build: C. A one-line touch of Analysis.cpp costs 107 s per LLVM major; nothing is split.

## Composition
cloc (excluding build/.tmp/.git/.beads):

| Language | files | code |
|---|---|---|
| C++ (src) | 12 | 8538 |
| C/C++ headers | 5 | 179 |
| Python (tests, scripts) | 48 | 3381 |
| LLVM IR (probes) | 41 | 2506 |
| JSON (verification.json etc.) | 4 | 13509 |
| Markdown | 13 | 1058 |
| other (TOML, sh, CMake, C) | | ~330 |

Plus 7 `.inc` files under src (CCCalls, Reversible, ResidualIntrinsics, Varargs-less on main, WideRuntime, runtime/).

Module map (src, wc -l):
- Production.cpp 2782: object/host-stub emission, native ABI, linking (the biggest file).
- Analysis.cpp 2220: points-to / region analysis (`Analysis::step`, `run`, `composite`).
- Scalar.cpp 1186: lift of scalars to ISA rows, wrapper emission.
- Normalise.cpp 704: LLVM-level normalisation (`normaliseScalar` is one function).
- ResidualIntrinsics.inc 523, NativeComparison.cpp 509, BennettPlugin.cpp 471 (pass entry).
- SoftFloat.cpp 369, Wide.cpp 363, Reversible.inc 153, Integer.cpp 140, Residual.cpp 102, Snapshot.cpp 71, Memory.cpp 23.
- 12 .cpp files all in one MODULE library (CMakeLists.txt:17), built twice (LLVM 18, 23).

Dependencies: LLVM 18 and 23 system installs only (no CMake find_package beyond LLVM). Python imports stdlib only (ctypes, subprocess, tomllib). Siblings consumed by pin: bennett-isa-spec (reference interpreter), bennett-dialect-spec (read via `git show <pin>`), bennett-arith and bennett-runtimes (bitcode).

Authorship (198 commits, all authored as tobiasosborne): 17 `wip(codex job` (8.6%), 4 with `Agent: gpt` trailer, 59 with `Co-Authored-By: Claude` (30%). The rest carry no trailer (human or older sessions); mix is approximate.

## Build and test times
Build dir: build/ is warm, Unix Makefiles, ExternalProject per major (llvm18, llvm23), RelWithDebInfo. No reconfigure done. Driven via `make -C build/llvm18 -j3`.

| Step | wall |
|---|---|
| Incremental, touch Memory.cpp (LLVM 18 only) | 6.7 s |
| Incremental, touch Analysis.cpp (LLVM 18 only) | 107.3 s (x2 for both majors, ~215 s) |
| smoke.py | 5.1 s |
| gate_policy.py | 0.7 s |
| contract_policy.py | 1.6 s (RED) |
| recognition.py --major 18 | 8.1 s (79/79 pass) |
| analysis_edges.py --major 18 | 3.3 s |
| validation.py --major 18 | 4.9 s |
| scalars.py --major 18 | 9.2 s (RED, 19 lowered/passed, 1 crash) |

`cargo` n/a. Full `scripts/gate` not run (hours; per brief). The gate runs ~50 python drivers x 2 majors (scripts/gate:20-50). Test count: 48 Python drivers, 246 `assert` statements, ~79 recognition cases plus ~20 scalar lifts, plus many internal loops; no pytest/lit, so no per-test ignored/skip count. Red in my run: contract_policy.py, scalars.py (entry-stack). No ignored tests found (grep for skip/xfail: none).

## Coverage
No gcov/llvm-cov instrumentation exists; estimate only (structural). Everything is exercised end to end through `opt -load-pass-plugin`, so function coverage of the lowering paths is plausibly high for what the spec examples reach, but I could not measure it. Weakest-tested areas (estimate):
1. Production.cpp `hostStub` (2221, 203 lines) and `linkReferences` (1711, 186 lines): only through production_*.py drivers, which I did not run (heavy).
2. Varargs, load_delta, vector_lanes, cc_markers: tests exist only on the rung4 branch, not main.
3. Error/diagnostic paths: 55 error-message strings mention bead ids; each needs a spec-derived reject case; recognition.py covers only `accept|reject|blocked` verdict examples named recog-/attr-/handle-/region-/pt*.
4. Non-x86 or LLVM 23-specific API paths: only checked by running the whole suite with --major 23 (not run here).
5. entry-stack lift path (Scalar.cpp:866): currently crashes.

## Test quality
Sample of 19 (file:line, class, why):
- recognition.py:25-31 useful: spec-published examples, verdict from spec text, not from implementation.
- recognition.py:34 useful: asserts exact atom sets for pt6-byte-width.
- smoke.py:36 useful: content keys ignore names but keep global images (two asserts on inequality and equality).
- smoke.py:50 useful: all 23 marker prototypes compiled from the pinned header through clang.
- scalars.py:~50 useful: byte-equality of produced object against the spec's fixture, hash compared, then run-oracle on the reference interpreter. Strongest oracle in the repo.
- wide.py:89 useful: arbitrary-width ops vs Python integer model (independent arithmetic, but sampled inputs, not exhaustive).
- wide.py:95 useful: compare predicates vs Python.
- wide.py:59 weak: absence-of-regex check on IR text.
- wide.py:103 weak: identity function, trivial input.
- integer_intrinsics.py:54 weak: "no llvm.* call residue" string grep.
- integer_intrinsics.py:125 useful: funnel shift vs Python expression.
- integer_intrinsics.py:133 weak: only an exit code equals 5.
- memory_runtime.py:27 useful: memmove vs bytearray model over dest/src/len grid.
- memory_runtime.py:69 weak: key inequality only, no property about the key.
- review_regressions.py:61 useful: exact reversed result 7 and no host requests.
- review_regressions.py:87 weak: substring match on emitted LLVM text (`load <8 x i1>`).
- analysis_edges.py:~7 'additive-copy-cycle' weak: expected list `[]`, i.e. only that nothing is claimed.
- contract_policy.py:7 guard, brittle: asserts sibling registry == 0.2.13 and a hard-coded SHA; red now.
- gate_policy.py: 9 assertions on the gate config itself; self-referential policy check.

Ratio: 11 useful / 7 weak / 1 guard (~60% useful). Oracle-backed: scalars (spec fixture + ISA reference interpreter), wide/integer/memory (Python models, native-run through ctypes), recognition (spec examples). Self-referential: text-grep tests, key-inequality tests. The gate (scripts/gate) would catch a wrong numeric result for wide/integer/memory ops and a wrong object for spec lifts, but not wrong Analysis precision outside the spec examples. Note scalars.py:12 hard-codes `bennett-isa-ref` debug binary; the asserted `-bennett-dialect=0.2.13` string is repeated in every driver.

## Code quality
1. src/Scalar.cpp:866 `functions.at(m.getFunction("__bennett_rt_entry_replay"))` throws std::out_of_range, aborting `opt` with a stack trace for tests/probes/entry-stack.ll (scalars.py --case entry-stack, LLVM 18). Fail-loud but as a crash, not a diagnostic. Did not bisect whether the bitcode input or the code changed.
2. src/Normalise.cpp:14 `normaliseScalar` is 499 lines; src/Analysis.cpp:1232 `Analysis::step` 528 lines; Production.cpp:2221 `hostStub` 203; Production.cpp:1711 `linkReferences` 186; Analysis.cpp:1761 `run` 231, :953 `composite` 216. Long, state-heavy; any edit risks regressions that tests reach only via end-to-end drivers.
3. Line width: 12 lines >200 cols in Analysis.cpp, 7 in Scalar.cpp, 5 in Normalise.cpp (max 531 cols). Tests are worse: tests/scalars.py is a dense minified script, with 1-space indentation and 400-col lines.
4. Bead/session references in source: 55 matches of `bd-`/`bp-xxx`/`N##` in src/*.cpp (policy rule 9 bead-reference).
5. Fixed `return false;`/`catch(...)` paths: 40 occurrences across src (Normalise.cpp 16, Analysis.cpp 10, Production.cpp 8); not all are fallbacks but each is a place to check for silent refusal. Not audited individually.
6. tests/contract_policy.py:5-7 pins the dialect version in two places (SPEC_VERSIONS.toml and the drift function) and reads the sibling working tree, so a spec bump (0.2.14 published at dialect-spec 22f9ed6) breaks the plugin test with no plugin change. Environmental coupling, red now.
7. Version skew: README says dialect 0.2.10 @ 023f5a7, SPEC_VERSIONS.toml/tests say 0.2.13 @ 95a4b8d. Stale docs claim.
8. Tracked WIP litter: .beads/issues.jsonl (24 lines churn per branch), HANDOFF.md and worklog/ tracked (1 chunk); docs/reviews/2026-11-03-ipp-repro/*.ll belongs to the rung4 branch. Not egregious. .tmp/ untracked (ok).
9. Single-use duplicated scaffolding across ~23 test drivers: the same `run()` subprocess helper and opt-plugin command line appear in each (wide.py:9, integer_intrinsics.py:9, memory_runtime.py:8, scalars.py:9). Could be one module.

Existing reviews already cover correctness findings (docs/reviews/2026-11-03-plugin-batch.md: bp-0xt open, bp-dc7 NOT RESOLVED); not repeated.

## rung4-plugin branch (not audited)
`git diff --stat main...rung4-plugin`: 23 files, +3876 / -368. Core: src/Analysis.cpp +1790 (net), Production.cpp +239, Bennett.h +132, Normalise.cpp +115, new src/Varargs.inc +148; new tests cc_markers.py (255), reference_k.py (193), vector_lanes.py (177), analysis_edges.py +140, load_delta.py (121), varargs.py (74); docs/design/factored-points-to.md (435) plus reviews. Checked out at /home/tobias/Projects/bennett-workspace/bennett-plugin-rung4.

## What is good
- Real oracles: scalars.py compares byte-for-byte to spec-published objects and runs them on the ISA reference interpreter.
- Arbitrary-width arithmetic and memory ops are checked against independent Python models via native ctypes execution (wide.py, integer_intrinsics.py, memory_runtime.py).
- Pins are checked by SHA-256 (arith bitcode, dialect text via `git show <pin>`), so inputs cannot silently drift; headless/TMPDIR rules are enforced inside the scripts.
- Incremental build for small files is fast (6.7 s), builds reproduce on both LLVM majors from one source.

## Recommendations
1. Fix the Scalar.cpp:866 `.at()` crash into a diagnostic and decide whether entry-stack is a real regression or sibling drift.
2. Make contract_policy.py compare against the pin only (git show), not the sibling working tree registry, so spec bumps do not redden the plugin.
3. Split Analysis::step and normaliseScalar into per-opcode/per-phase functions (and Analysis.cpp into 2-3 TUs) to cut the 107 s rebuild.
4. Extract the shared test harness (run/opt command/dialect flag) into tests/contracts.py and reformat the minified drivers.
5. Replace string-grep and inequality-only tests with executed or spec-derived checks (wide.py:59, integer_intrinsics.py:54, review_regressions.py:87).
6. Add llvm-cov (or gcov) coverage build for one major to get real numbers.
7. Remove bead ids from comments/messages (55 sites) and update README dialect version to 0.2.13.
