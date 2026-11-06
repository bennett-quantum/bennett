# bennett-driver quality audit 2026-11-05

## Verdict
- Code: C+. Fail-loud error codes are consistent, but `compare()` is a 574-line function and `execute()` 377 lines, and defaults are silently resolved against sibling-repo paths.
- Tests: C. Tests are real end-to-end runs against real clang/opt/plugin, but 9 of 28 test binaries are red against the live sibling plugin (version drift), and only 5 Rust unit tests cover `src/` directly.
- Build: A-. No dependencies, 2.5 s incremental, 12.7 s test build. Full suite is slow (about 10 min) because of two arithmetic tests.
- Coverage was not measured (see Coverage). Estimated structurally.

## Composition
cloc (excluding target, .tmp, .git):

| Language | files | code |
|---|---|---|
| Rust | 41 | 2789 |
| Python (tests/ and scripts/) | 33 | 1715 |
| Markdown | 14 | 953 |
| C++ (mode-preparation.cpp, process-entry.cpp) | 2 | 406 |
| JSON/TOML/C/sh/yaml | 12 | ~190 |
| Total | 103 | 6058 |

Rust split: `src/` 2853 lines (wc), of which `tests/*.rs` are 6-line wrappers (28 files, 30 `#[test]` fns, 2 files hold extra tests).

Modules (src/, wc -l):

| Module | Lines | Purpose |
|---|---|---|
| main.rs | 1010 | option parsing, input admission, link, opt, plugin invocation, build.json (`execute` 377 lines) |
| native.rs | 624 | native comparison; `compare()` is lines ~50-624 |
| classifier.rs | 213 | UBSan/ASan diagnostic source classifier |
| process.rs | 106 | process-entry preparation |
| report.rs / json.rs / native_adapter.rs / output_paths.rs / mode_preparation.rs / arith.rs / native_host.rs / llvm_utility.rs | 95/90/130/78/83/89/75/39 | reports, hand-rolled JSON, adapter, output-path aliasing guard, mode prep, arith instances, native-only host build, tool cache |

Dependencies: 1 crate in Cargo.lock (the package itself); zero network deps by design. Python tests use stdlib only. External: clang, llvm-link, opt, llvm-as, llvm-nm, readelf, sha256sum, python3, hard-coded `/usr/lib/llvm-{18,23}/bin`.

Authorship (57 commits): 22 `wip(codex job` runner commits (39%), 35 committed under `tobiasosborne` (61%; these are Claude agent commits per the review's trailer table, no human/Claude split is recoverable from author name). No `Agent: gpt-` trailer in any message.

Tracked litter: `worklog/001_*.md`, `.beads/*` (by policy). No tracked `.tmp`. `target/` ignored. `.beads.gate.lock` present in tree root (untracked state not checked beyond `git status --short`, which was empty).

## Build and test times
Cache: target/ was warm (debug dir existed).

| Step | Wall |
|---|---|
| warm incremental build (touch src/report.rs) `cargo build -j3` | 2.5 s |
| `cargo test --no-run -j3` | 12.7 s |
| `cargo test -j3` stopped at first red binary (arith_production) after arith_conversions 95 s and arith_instances 274 s | 370 s |
| `--no-fail-fast` on the 26 other binaries, `--test-threads=3` | about 250 s (my wrapper `time` line was lost to a `head`; per-binary finished-in times 0.2 to 53 s) |

Counts: 5 unit + 30 integration `#[test]` = 35. Ignored: 0. Skipped: 0 (no `#[ignore]`, no skip logic anywhere in tests). Red in this run: 9 integration binaries plus 1 of 3 tests in pipeline.rs: arith_production, classes, device_models, input_headers, inputs, modes, native_host, output_paths, pipeline_metadata, and `pipeline::hashtable_pipeline_matches_recorded_objects`. Passing: unit 5, arith_conversions, arith_instances, and about 13 others.

Why red (verified from failure text):
- 7 of the red ones fail with `BD-E-VERSION: plugin identity "dialect-0.2.13;isa-0.8", expected dialect-0.2.10` because the tests default to `../bennett-plugin` (live, now 0.2.13) while they pass `-bennett-dialect=0.2.10` (e.g. `tests/inputs.py:5` pattern, `plugin_root = ... or root.parent/'bennett-plugin'`). `gate.toml` pins plugin sha `157d4bd`/`0ac6180` and sets `BENNETT_DRIVER_*_PLUGIN_ROOT`, so the gate is green only against pinned siblings; a bare `cargo test` is red. Not a skip: it fails loudly, which is correct per policy, but it means `cargo test` is not a usable local loop.
- `classes` and `device_models` fail with plugin "unimplemented: §3.4 configured register class" / "§8.4 scalar descriptor finite dispatch": red-by-design tests asserting north-star capabilities (matches review items 6 and 9zg). Intentional red tests in the default suite.
- `arith_production` and `pipeline` failures not individually diagnosed (arith_production exits 1 from the driver in 1.1 s, likely the same version drift).

External toolchain: every Python test shells out to clang/llvm-18/23 and the plugin `.so`; absence of any of them raises an assertion (loud). No silent skips found (`grep skip|SKIP|exit(0)` in tests/*.py: only `tests/process.py:188` embedded C `exit(0)`).

## Coverage
Not measured. `cargo llvm-cov 0.9.1` is installed, but the suite is about 10 min with red tests and the driver is exercised only as a subprocess of Python scripts, so I judged a run non-informative within budget and skipped it. Structural estimate:
- `src/*.rs` in-process unit tests: 5 (main.rs:4, json.rs:1). Everything else is reached only through the binary.
- Mapping: main.rs paths reached by inputs/input_headers/modes/pipeline*/reports/environment; native.rs by comparison/native_*/output_paths; classifier.rs by classifier.py; process.rs by process*/reversible; mode_preparation by preparation/classes/device_models; arith.rs by arith_*; native_host.rs by native_host.
- Estimate: line coverage of reachable paths is moderate (most modules have a named test), but with 10 binaries red against the live plugin, the success paths of main.rs plugin invocation are only verified under the pinned gate.

Weakest/untested areas:
1. `native.rs:compare()` 574 lines (native.rs:~50-624): one function, branches (layout map, strict link, record/output aliasing) exercised only by multi-assertion scripts; no unit isolation.
2. Success path of full reversible-tier plugin launch: `reversible.py` accepts `blocked` status (README: current plugins report BD-B-ISA7), so the real "complete" path is untested.
3. Option parsing in `Options` (main.rs:~224-270): only via CLI strings in scripts; no unit tests for the whitelist.
4. `tests/integration.py` (rung-2 evidence) cannot run: fixture absent in pinned conformance (review item 7, bennett-driver-ppz, blocked-honest).
5. `json.rs` hand-rolled serializer/parser (90 lines): 1 test, no escape/unicode/number edge tests.

## Test quality
Structure: every `tests/*.rs` is a 6-line wrapper calling `support::fixture("x.py")`; all logic is in Python scripts (1715 lines) that build tiny LLVM IR/C programs, run the driver and assert on outputs and exit codes. All tests have the same shape, so sampling is across scripts.

Sampled (file:line, class):

| # | Test | Class | Why |
|---|---|---|---|
| 1 | pipeline.rs:25 `version_mismatch_is_loud` | useful | wrong dialect must yield BD-E-VERSION and nonzero exit |
| 2 | pipeline.rs:41 `missing_published_fixture_names_its_dependency` | useful | asserts loud failure naming bead; no fallback |
| 3 | hook.rs:3 `gate_configuration_and_stub_are_ready` | weak | checks gate config/stub presence, not behaviour |
| 4 | modes.rs:4 `published_controls_reach_the_backend_without_false_success` | useful | asserts refusals do not certify (`modes.py:53`) |
| 5 | comparison.py:25-27 (records status/blocked_on) | useful | runs O0 and O2 native binaries and checks exit 0, no undefined symbols, no INTERP |
| 6 | comparison.py:41 argv contains `-nostdlib -static` | weak | asserts flag list of the driver's own command (self-oracle) |
| 7 | comparison.py:32 provenance string equality | weak | pins an arbitrary literal |
| 8 | classifier.py:9-36 materialised sha unchanged, binaries run, rows' coverage flags | useful | independent oracle: input hash invariance plus real execution |
| 9 | classifier.py:36-39 `coverage['general_memory'] is False` | weak | asserts constants the driver hard-codes (review P2: coverage booleans are constants) |
| 10 | inputs.py:1-25 ll+bc mixed-major produce same launch | useful | compares two input forms for identical output |
| 11 | input_headers.py:35 no `linked.bc` when header missing | useful | negative test across 5 cases x positions x majors x 2 spellings |
| 12 | output_paths.py:32 no native-O2/O0 after alias refusal | useful | regression for P0 7gi, checks input sha unchanged |
| 13 | pipeline_metadata (rs) | useful | compares executed argv vs certificate for each spelling (regression for P0 bcl) |
| 14 | reversible.py:24,35 blocked production requires build.json and files exist | weak | existence checks of artifacts, accepts blocked status |
| 15 | environment.py:15-17 child sees TMPDIR and no DISPLAY | useful | the C program prints the real env |
| 16 | native_host.py:91 no native-host in mixed refusal | useful | pins 116 refusal behaviour |
| 17 | classes.rs / device_models.rs | useful but red | assert full capability against plugin; red by design |
| 18 | src/main.rs unit tests (4) | weak-to-useful | small parsing checks only |

Ratio of 18 sampled: 11 useful, 5 weak, 0 tautological, 2 useful-but-red. Roughly 60% useful. Most assertions check driver self-reported JSON (`native-comparisons.json`, `manifest.json`, `build.json`) against values the driver computed, but the better ones add independent oracles (execute produced binaries, hash input before/after, readelf/llvm-nm).

Oracle-backed vs self-referential: no spec conformance suite, no differential against reference interpreter, no property-based or exhaustive domains in this repo. The only conformance coupling is `tests/integration.py` (frozen rung-2 recorded objects), which cannot currently run (bennett-driver-ppz). So the driver's central claim, "the merged and plugin-processed module is correct", is checked only through tiny hand-written IR programs. The gate would catch a driver crash, wrong exit code, wrong version/target/aliasing handling, and a certificate/argv mismatch; it would not catch a wrong bitcode merge result, since the rung-2 recorded-object comparison is the only check that does that and it is blocked.

Repo-level gap: `gate.toml` has one check, `cargo test`, run with pinned sibling shas; this does catch the version drift above only when pins are stale in the other direction (pins are exact). Fine, but the pin makes the gate immune to the live plugin, so integration breakage is found late.

## Code quality
Findings (policy rule 9 and fail-fast); existing review (docs/reviews/2026-11-03-driver-batch.md) items not repeated.

1. Complexity hotspots (awk function-length count): `native.rs::compare` 574 lines (native.rs:~50), `main.rs::execute` 377 (main.rs:~440-820), `main()` 169, `artifact()` 69. A single 574-line function with record/aliasing/link/layout branches is where the review's P0 7gi and the P1 7cc came from; next bug is likely here.
2. Silent defaults on sibling paths: `native.rs:62,67,234,311` and `native_adapter.rs:30-37` use `.unwrap_or(ws.join("bennett-runtimes/..."))`; main.rs:264 and llvm_utility.rs:9 fall back to `CARGO_MANIFEST_DIR/.tmp` baked in at compile time. Failure scenario: a relocated binary quietly reads the compile-time repo's artifacts; this is also why tests are red against the live plugin without the gate env. (Violates "coupled to other repos only through published specs".)
3. Hard-coded toolchain paths `/usr/lib/llvm-{18,23}/bin` in Python tests (`classifier.py:13`, `comparison.py:14`, `inputs.py:21`): machine-specific; if the toolchain moves, failure is an obscure FileNotFound.
4. Magic literals: `main.rs:22` accepts dialect `0.2.10 | 0.2.13` while README advertises 0.2.10 only (README line 2 vs HELP text). README is stale vs source; HELP says 0.2.13 required.
5. Bead references in source: `main.rs:541` ("bennett-4ht and bennett-driver-116") in an error message; this one is deliberate user-facing text. `tests/pipeline.rs:55` asserts the bead id string in the stderr (`bennett-driver-3j4`): couples test to a tracker id.
6. Flags where an enum belongs: `compare(o, b)` and `execute(o, b)` take the whole `Options` string map and re-query it by key (`o.get("bennett-layout-data-base").unwrap_or("4096")` appears at native.rs:332 and classifier.rs:94: duplicated default). Options are untyped strings throughout; typos in key literals cannot be caught by the compiler.
7. Duplicated validation: `main.rs:162-166` version check plus HELP text plus README plus finalise-build.py each restate the accepted versions.
8. Trivial wrappers: `tests/*.rs` 28 files x 6 lines (`support::fixture`) are a mechanical one-to-one wrapper; one test binary per script costs 28 link steps in `--no-run` (12.7 s) and prevents `cargo test` from filtering by Python case.
9. Review-found known issues still open per the review: 6bl (cross-device rename), 7cc (comparison refused for bitcode input), tbc, rnn. I did not re-verify them.
10. Dead code: none found by `cargo build` warnings (build finished with no warnings in the tail I saw). Not exhaustively checked.

## What is good
- Zero dependencies and stable fail-loud error codes (`BD-E-VERSION`, `BD-E-OUTPUT-PATH`, `BD-B-NATIVE-INPUT`) with blockers.json/txt; tests assert those codes.
- Negative tests matrix well: `input_headers.py` covers missing triple/datalayout across positions, spellings, and both LLVM majors; `output_paths.py` covers alias, symlink, hardlink cases.
- Several tests use an independent oracle: run the produced native binary, hash input before and after, `llvm-nm`/`readelf` on output.
- Red capability tests (`classes`, `device_models`) honestly encode the north-star requirement instead of being ignored or weakened; no `#[ignore]` and no silent skip anywhere.
- Warm build 2.5 s; test build 12.7 s.

## Recommendations
1. Split `native.rs::compare` and `main.rs::execute` into staged functions over a typed config (parse `Options` once into a struct with defaults in one place); removes 574-line function and duplicated defaults.
2. Make the tests self-contained against pins: have `cargo test` fail with one clear message when the plugin identity differs from the pin, instead of 7 opaque BD-E-VERSION traces; or set the pinned plugin root in `.cargo/config.toml [env]`.
3. Remove silent `unwrap_or(ws.join(...))` sibling defaults; require explicit `--bennett-runtimes/--bennett-arith` or an env var and error otherwise.
4. Run `cargo llvm-cov` with the gate env on the pinned siblings and record the baseline; add `LLVM_PROFILE_FILE` propagation check for subprocess tests.
5. Add one differential test that checks merged-module behaviour (execute `postlink.bc` with lli vs the native build) so a wrong merge is caught without the blocked rung-2 fixture.
6. Move the intentionally red tests (`classes`, `device_models`) behind a named feature/env switch so a default `cargo test` is meaningful, while keeping them in the gate's "known red" list.
7. Update README to state accepted dialect (0.2.13 plus explicit 0.2.10); unify the version constants into one const.
