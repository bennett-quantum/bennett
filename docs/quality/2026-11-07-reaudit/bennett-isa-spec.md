# bennett-isa-spec quality audit 2026-11-07

## Verdict

- Code **B-**: certificate admission, pair applicability and token lifetime checks are substantially stronger; eight oversized semantic functions and deferred cleanup still limit maintainability.
- Tests **B**: useful exhaustive and negative oracles, with both historical failures now covered by strengthened regressions; whole-suite greenness is outside this bounded audit.
- Build **C+**: optimisation and line-table debug information improve the local loop and cap the former OOM path, but 63 integration binaries and a default suite over 180 seconds remain.
- These are independent grades on the baseline A–F scale, not automatic increments for merged fixes.

Audited main/origin/main: `3b1090790d82a00ac95d30b8da6b42d1d7a9f5d1`; checkout initially clean.
All code evidence refers to the main checkout; measurements use its exact `git archive HEAD` snapshot under the permitted scratch directory. This permits touching **only the scratch copy** of sha256.rs for incremental timing. No main-checkout file was touched.

## Composition

Tracked-tree measurement: `cloc --git --exclude-dir=.git,.tmp,target --json /home/tobias/Projects/bennett-workspace/bennett-isa-spec`. 1,023 recognised text files, 134,199 code lines; source-generated caches and audit scratch are excluded.

| Language | Files | Code LOC |
|---|---:|---:|
| Rust | 177 | 69,613 |
| Markdown | 161 | 35,046 |
| JSON | 617 | 19,858 |
| diff | 1 | 4,621 |
| Python | 47 | 4,578 |
| Shell (both dialects) | 10 | 291 |
| Headers / TOML / YAML | 10 | 192 |

| Directory | Code LOC (all recognised languages) | Composition |
|---|---:|---|
| /home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src | 30,907 | execution, parser, verification, CLI |
| /home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests | 28,141 | 63 top-level integration binaries plus helpers/fixtures |
| /home/tobias/Projects/bennett-workspace/bennett-isa-spec/conformance/src | 4,685 | independent expansion/simulation and case harness |
| /home/tobias/Projects/bennett-workspace/bennett-isa-spec/conformance/tests | 7,327 | 37 integration binaries plus Python witness |
| /home/tobias/Projects/bennett-workspace/bennett-isa-spec/conformance/cases | 18,160 | 557 case.json records and associated data |
| /home/tobias/Projects/bennett-workspace/bennett-isa-spec/conformance/tools | 845 | catalog/fixture derivation tools |
| /home/tobias/Projects/bennett-workspace/bennett-isa-spec/spec | 13,711 | published 0.8/0.9 text, catalog, migration diff |
| /home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs | 20,996 | reviews, derivations, briefs and quality record |

Module map below uses **physical Rust lines**, including each module's descendants; these do not use cloc's code-only denominator.

| Top-level interpreter module | Lines | Purpose |
|---|---:|---|
| action | 1,201 | reversible action execution and workspace ownership |
| bits | 390 | arbitrary-width bit vectors |
| borrow | 2,322 | static borrowed-workspace soundness |
| call_discipline | 393 | call-interface alias/ownership checks |
| certificate | 948 | certificate admission and binding validation |
| claims | 2,911 | claim replay, inverse pairs and applicability |
| classical | 2,241 | CC/R execution, effects, token and qreg transitions |
| controls | 19 | effective-control normalisation |
| exact | 1,170 | exact arithmetic and measurement |
| handle_validation | 102 | qreg view validation |
| identity | 482 | interface/closure/object hashing |
| instances | 329 | fixed-binding invocation instances |
| json | 500 | JSON parsing and canonicalisation |
| lib | 204 | exports, errors and fallible allocation helpers |
| linking | 411 | imports, pins and object linking |
| machine | 1,414 | literal reversible oracle step machine |
| main | 2,606 | CLI parsing, execution and JSON output |
| metadata | 1,755 | schedule selection and source paths |
| metadata_schema | 1,081 | schema admission and unit regressions |
| metadata_types | 54 | metadata types |
| object | 1,964 | textual object parser/model |
| oracle | 1,270 | sequential oracle semantics and program preparation |
| quantum | 918 | exact sparse quantum state and gates |
| r23_transaction | 303 | unit-test fault-injection suite |
| ref_library | 716 | published library binding and source expansion |
| registers | 332 | qreg lifetime and ownership |
| retained | 197 | shared retained buffers and fallible growth |
| schema | 247 | metadata schema definitions |
| sha256 | 89 | SHA-256 |
| source_constructor | 2,426 | source-to-reference-gate construction |
| tokens | 459 | budget handles, identity partitions and mint validity |
| validation | 2,630 | instruction, cleanup and register admission |

Dependency count: interpreter Cargo.lock **2 packages**, conformance lock **1**: both local crates, **zero external Rust crates**.
Python static imports have **26 distinct roots**: 24 standard-library roots, local r15_pins and SymPy in [a historical algebraic proof script](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/notes/2026-11-02-rev3/verify_l2p.py:15); the gated scripts use stdlib. The baseline's blanket “Python stdlib only” statement was too broad. Rust implements JSON, SHA-256, exact arithmetic and RNG itself.
The 557 case records divide into **483 available / 74 explicitly unavailable**; unavailable is a distinct harness outcome, not semantic coverage ([harness contract](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/conformance/src/lib.rs:11)).

Authorship measurement: `git -C /home/tobias/Projects/bennett-workspace/bennett-isa-spec log --format=%H%x1f%an%x1f%s%x1f%B%x1e`, classify Codex markers before trailers.
**442 commits**, all author `tobiasosborne`; **90 explicit Codex (20.4%)**, **142 explicit Claude (32.1%)**, **210 unattributed (47.5%)**. These are provenance markers, not a reliable human/AI partition; unattributed is not “human.” History still contains **64** `wip(codex job` commits; audited HEAD is a merge.

## Build and test times

Scratch root `S=/home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/reaudit-2026-11-07`; manifest `M=$S/reference-interpreter/Cargo.toml`.
The scratch target started empty; subsequent ordinary runs reused it. Coverage uses a separate target. All runs are headless, offline, `-j3`, four test threads, `timeout 600`, `ulimit -v 8000000`, core dumps disabled. Each run is a `systemd-run --user --scope -q --unit=bennett-build-reaudit-isaref-...` scope with TMPDIR=$S/tmp and CARGO_TARGET_DIR=$S/target. The initial runs used the original load<12 rule; subsequent runs obey the binding update: available>=6 GB, load<8, no bennett-heavy scope, poll 60 s, maximum wait 30 min. GNU time measures command wall seconds and maximum child RSS; slot waiting is excluded. Shared-host results are not isolated benchmarks.

| Measured command suffix (after cargo) | Wall seconds | Peak RSS KiB | Result |
|---|---:|---:|---|
| test --offline -j3 --manifest-path "$M" --lib --no-run (cold private target) | 80.18 | 932,080 | compiled |
| touch "$S/reference-interpreter/src/sha256.rs"; same --lib --no-run | 2.07 | 447,144 | warm incremental rebuild |
| test --offline -j3 --manifest-path "$M" --lib -- --test-threads=4 | 11.39 | 69,768 | 32 passed, 0 failed/ignored |
| test --offline -j3 --manifest-path "$M" --test isa09_qinplace --no-run | 66.83 | 931,504 | compiled integration binary and CLI |
| test --offline -j3 --manifest-path "$M" --test isa09_qinplace -- --test-threads=4 | 29.83 | 62,580 | 42 passed |
| same, --test r21_resources | 4.03 | 206,624 | 9 passed; former §3.3 failure fixed |
| same, --test isa09_certificate | 2.38 | 204,136 | 6 passed |
| same, --test isa09_budget_mint | 3.63 | 206,244 | 13 passed |
| same, --test isa09_forwarding | 39.05 | 668,620 | 11 passed / 1 named slow ignore |
| llvm-cov --offline -j3 --manifest-path "$M" --lib --json --summary-only --output-path "$S/cov-lib.json" -- --test-threads=4 | 68.73 | 949,252 | 32 passed; cold coverage target |
| same, --test isa09_qinplace --no-clean; output cov-combined.json | 88.45 | 984,560 | 42 passed; retained lib profiles |

The changed qinplace executable is **46,053,448 bytes (43.92 MiB)**, versus baseline ~110 MB; the current lib harness is 36.28 MiB and CLI 39.46 MiB. This is one rebuilt binary, not a measured size for all targets. Profiles are [opt-level=1, line-tables-only](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/Cargo.toml:10). The baseline 61.7/186.9-second timings rebuilt all test targets; my 2.07/80.18 timings select the library, so they are **not directly comparable**.

Static inventory: **654 top-level integration #[test] attributes + 5 included support tests + 35 in src = 694 tests**, comprising 688 active and six ignored. The five support tests are in [r20_extremes.rs](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/support/r20_extremes.rs:65); a standalone fixture probe's attribute is not an active test. Conformance has **127 integration + 2 unit attributes**. The complete crate results in [quality.md](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/quality.md:395) claim **688 pass / 6 ignored** and **129 pass / 0 ignored**; these full runs were not repeated here.
This audit ran **113 distinct test functions: 113 passed, zero failed, one selected binary ignore**; the coverage runs repeat 74 of those functions. The remaining 575 active reference tests and all conformance test harnesses were not run.
Ignored: five old exhaustive sweeps plus the new wide forwarding witness; only the latter has an explicit gate check ([gate configuration](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/gate.toml:23)). No full reference suite, full conformance suite, push hook, gate runner, ignored sweep or heavy/ladder/dual-engine test was run. The source-touch timing changed only a scratch mtime; all tracked checkout bytes remain unchanged.

## Coverage

Measured with cargo-llvm-cov **0.9.1**, CARGO_LLVM_COV_TARGET_DIR=$S/coverage and the two explicit single-target commands above.
Initial --target-dir syntax was rejected (exit 1, 0.03 s); the installed helper uses that environment variable. The successful fresh-target run also warned that cargo clean found no CACHEDIR.TAG, then compiled and exported successfully; no earlier profiles existed.
Raw summaries: [library JSON](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/reaudit-2026-11-07/cov-lib.json), [retained library + qinplace JSON](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/reaudit-2026-11-07/cov-combined.json).

| Scope | Line coverage | Function coverage | Region coverage |
|---|---:|---:|---:|
| lib only, 48 interpreter files | 10,264/24,434 = **42.01%** | 984/2,475 = **39.76%** | **38.20%** |
| lib + qinplace, same library files | 13,639/24,434 = **55.82%** | 1,281/2,475 = **51.76%** | **50.44%** |
| combined export including unexecuted CLI | 13,639/26,597 = **51.28%** | 1,281/2,665 = **48.07%** | **46.87%** |

These are bounded-subset floors for the interpreter, **not full-suite or whole-repository coverage**: conformance source is excluded; compiled main.rs contributes 2,163 lines at 0%. Some cfg(test) source is included. LLVM function counts include closures and differ from the lexical named-function census.
The comparable lib floor is slightly below baseline 42.6%/40.2%; the line denominator grew from 23,971 to 24,434. New integration-only semantics explain why this is not evidence of lost test assertions.

| Previously weak path | lib line % → retained lib + qinplace line % | Classification |
|---|---:|---|
| [pair theorem](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/claims/pairs09.rs:382) | 0 → **80.41** | live, substantively integration-covered |
| [applicability](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/claims/qinplace09.rs:85) | 5.71 → **86.12** | live, static and dynamic obligation tests |
| [ordinary replay](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/claims/replay09.rs:337) | 0 → **11.73** | reached, most ordinary replay still absent from this instrumented subset |
| [literal machine](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/machine.rs:1) | 0 → **35.24** | live; pair proofs exercise reversal |
| [linking](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/linking.rs:6) | 0 → **58.31** | live; imported positive controls link bodies |
| [oracle constructor](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/source_constructor.rs:81) | 0 → **39.46** | live; many branches unexercised here |
| [qinplace constructor](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/source_constructor/action/qinplace.rs:5) | 0 → **91.38** | direct allocation/order/arithmetic witness |
| [token resolution](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/tokens.rs:328) | 12.43 → **71.27** | qinplace contexts cover shared token mechanics |
| [schedule domains](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/metadata/schedule_domains.rs:1) | 1.52 → **1.52** | effectively absent from this subset |
| [dynamic registers](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/classical/registers09.rs:1) | 0 → **0** | dedicated isa09_registers tests exist; not classified dead |
| [source events](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/metadata/source_events.rs:1) | 0 → **0** | selected expansion does not cover this metadata path |

Five largest residual coverage risks:

1. CLI [run](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/main.rs:1981) and output/error paths: 2,606 physical lines; library-only coverage excludes the binary; the combined export has 0% because the selected integration suite does not launch the CLI.
2. [oracle constructor](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/source_constructor.rs:81): 1,088-line body; selected integration reaches 39.46%, leaving most expansion branches unmeasured.
3. [borrow compiler](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/borrow.rs:656) and [action execution](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/action.rs:413): bounded checks do not replace the five ignored sweeps.
4. [linking](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/linking.rs:6) / [0.9 dynamic registers](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/classical/registers09.rs:1): linking is measured at 58.31%; dynamic registers remain 0% here despite dedicated tests, so lib 0% never established dead code.
5. [scheduled replay](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/claims/replay09.rs:354) and interval/target execution remain explicitly unverified; tests prove honest refusal, not the missing mechanics.

## Test quality

Random sample: Python Random(20261107), 18 selections without replacement from sorted top-level Rust integration test functions in both crates; classifications follow helper/child assertions.
Line numbers below point to the test function or immediately preceding attribute.

| Sample | Classification | What it can detect |
|---|---|---|
| [reference-interpreter/tests/r1_certificates.rs:857](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/r1_certificates.rs:857) | useful | sampler default/count verdict and malformed metadata, with immutable object text |
| [reference-interpreter/tests/r1_widths.rs:91](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/r1_widths.rs:91) | useful | 256-bit addition/high-bit carry and budget boundaries in two engines; one expected value uses shared BitVector subtraction |
| [reference-interpreter/tests/isa09_review.rs:41](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/isa09_review.rs:41) | weak | parse-only unwrap; no assertion that the five imported groups were preserved |
| [reference-interpreter/tests/metadata.rs:361](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/metadata.rs:361) | useful | frame sizes 0–3, exactly-two positive control and pinned identity |
| [conformance/tests/ref_catalog.rs:8](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/conformance/tests/ref_catalog.rs:8) | weak | closing-byte and nonempty-kinds checks do not establish canonical JSON |
| [reference-interpreter/tests/cli_xam.rs:75](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/cli_xam.rs:75) | useful | hand-derived sum=6, 21 steps and exact register deltas |
| [reference-interpreter/tests/step_machine.rs:122](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/step_machine.rs:122) | useful | closed-form fault/payload over 5,120 contexts plus commit/reversal |
| [reference-interpreter/tests/r1_fuzz_discipline.rs:1160](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/r1_fuzz_discipline.rs:1160) | useful | independent HXXH identity and dirty control at 2^40 trips; static admission only |
| [reference-interpreter/tests/isa09_forwarding.rs:199](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/isa09_forwarding.rs:199) | useful | helper requires HostResource and exact leaf-budget diagnostic at 1,024 leaves |
| [reference-interpreter/tests/frame_domain.rs:57](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/frame_domain.rs:57) | useful | independent frame inputs cannot cancel by copied SSA name |
| [reference-interpreter/tests/cli_xam.rs:2116](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/cli_xam.rs:2116) | useful | malformed table rows/cells reject and positive bytes retain a fixed hash |
| [reference-interpreter/tests/r22_retention.rs:153](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/r22_retention.rs:153) | useful | child checks payload sharing/equality under 128 MiB; follows guarded(cow) assertions |
| [conformance/tests/ref_examples.rs:222](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/conformance/tests/ref_examples.rs:222) | useful | BDD compares full pointer domain against explicit pinned-address interval |
| [reference-interpreter/tests/r1_certificates.rs:478](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/r1_certificates.rs:478) | useful | crossed-name slot mapping and a changed mutable output negative |
| [reference-interpreter/tests/isa09_forwarding.rs:97](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/isa09_forwarding.rs:97) | useful | source token bindings, two x values, five memory cells and exact reversal |
| [conformance/tests/ref_descriptors.rs:194](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/conformance/tests/ref_descriptors.rs:194) | useful | overlap positive control versus private scratch LIFO rejection; error reason unpinned |
| [reference-interpreter/tests/cli_xam.rs:114](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/cli_xam.rs:114) | useful | literal entropy, tape, console and memory deltas |
| [reference-interpreter/tests/cli_xam.rs:2022](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/cli_xam.rs:2022) | useful | five nonstring versions reject, valid control retains pinned object hash |

Ratio: **16 useful / 2 weak / 0 tautological (88.9% / 11.1% / 0%)**. This is a sample estimate, not a whole-suite assertion. Read the three largest test files: cli_xam.rs (2,414 lines), r1_fuzz_discipline.rs (1,782), isa09_qinplace.rs (1,718). Read central verifier files claims.rs, claims/pairs09.rs and claims/qinplace09.rs, plus changed token, certificate and constructor paths. Many fixtures still use global text replacement and generated hashes. Fixture setup rehashing is not itself an independent expected hash.
There are **65 single-line bare is_err assertions** under interpreter integration tests (regex lower bound); positive controls improve many, but wrong-reason failures can still pass.
Strong oracle categories: published fixed bytes/hashes, hand-derived formulas, exhaustive finite domains, BDD equivalence, sequential-versus-literal machine checks and exact restoration.
There is generated differential testing despite zero proptest dependency ([400-case default generator](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/r1_fuzz_discipline.rs:286)); the larger sweep remains ignored.

Would the gate catch a wrong result? **For covered semantics, yes in design**, through exact values and negative certificate mutants.
The gate runs both default crates, the separately bounded forwarding witness, a Python byte/semantic witness and catalog check ([checks](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/gate.toml:14)).
It still does not run the five old ignored sweeps, and a passing unavailable result is not implemented capability.
The compatibility oracle is the gate-pinned review sibling ([review pin](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/gate.toml:34)); conformance's default binary is the other crate **inside this repository** ([default_bin](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/conformance/src/lib.rs:44)).
No gate execution or global green verdict is claimed.

## Code quality

Residual debt is already consolidated in [review 3](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/reviews/2026-11-07-quality-isaref-r3.md:69) (b-isa-spec-bkqj); this baseline comparison rechecks it rather than filing duplicate findings.
The repaired correctness paths are already analysed in [quality review 3](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/reviews/2026-11-07-quality-isaref-r3.md:1) and [main review 2](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/reviews/2026-11-07-isaspec-main-r2.md:1); the following findings concern residual quality.
No new P0/P1 is claimed by this bounded audit. Existing [P2 b-isa-spec-qf44](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/.beads/issues.jsonl:111) still tracks imported-pair partition diagnostics deferred behind missing bodies; this is not a proof/execution acceptance and was not independently reprobed here.

| Finding | Evidence | Failure scenario / cost |
|---|---|---|
| Oversized semantic phases | [oracle](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/source_constructor.rs:81), [step_prepared](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/classical.rs:1468) | representation, resource checks and execution policy share long bodies; difficult local reasoning |
| Process references remain | [codex B09](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/classical.rs:890), [job-named fixture](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/main.rs:2448) | obsolete process names in source and fixtures persist |
| Production no-op test hooks remain | [preparation](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/lib.rs:164), [cli_preparation](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/main.rs:2415) | real fallible allocations remain separate from artificial stage faults; added review surface, not a demonstrated wrong result |
| Dead dispatch binding remains | [discarded base](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/object.rs:1320) | remove the unused binding; the strip_prefix/filter condition **does** control validation, contrary to the baseline wording |
| Silent-default sites need contextual review | [zero-fill domain](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/claims.rs:418), [optional token map](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/claims/pairs09.rs:60) | 88 unwrap_or-family sites (same scanner: baseline 87; the old report's 72 is not comparable); some encode valid omitted components, so counts alone do not establish silent failure |
| No quality ratchet/coverage record | [gate checks](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/gate.toml:14), [explicit deferral](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/quality.md:224) | pushes can enlarge complexity or retain litter without a quality check |
| Tracked scratch/litter persists | [backtrace log](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/fixtures/r22/hostcall-backtrace.log:1), [progress file](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/PROGRESS.md:1) | git ls-files also lists reference-interpreter/__pycache__/isa_check.cpython-312.pyc (binary, no line number) and four other PROGRESS files |
| Stale handoff remains linked | [README status](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/README.md:14), [old 524-pass claim](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/HANDOFF.md:44) | November 1 state is still presented as current after substantial new semantics |

Complexity scan: erase Rust comments/string/character literals, brace-match named functions; approximate lexical size/nesting, not compiler AST or cognitive complexity.
Same scanner on baseline be109bd and current HEAD: **940→951 functions; 59→64 over 100 body lines; 8→8 over 300**.
The baseline report's 912/55 used a different scanner; its numbers should not be treated as a directly comparable trend.

| Function | Body lines | Maximum brace depth |
|---|---:|---:|
| [oracle](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/source_constructor.rs:81) | 1,088 | 9 |
| [validate_action_sequence](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/validation.rs:110) | 617 | 8 |
| [action_sequence](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/action.rs:413) | 490 | 8 |
| [step_prepared](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/classical.rs:1468) | 446 | 8 |
| [run](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/main.rs:1981) | 412 | 5 |
| [classical_instruction](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/validation.rs:892) | 386 | 8 |
| [run_oracle_vectors_bound](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/oracle.rs:583) | 339 | 7 |
| [compile](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/borrow.rs:656) | 324 | 8 |

Maximum observed brace depth is 9 (oracle constructor and call_discipline::interface_targets); braces include match/closure scopes, not only condition nesting.
Duplication: CLI identity wrappers share a helper ([r9 wrappers](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/cli_xam.rs:1657)); assertions in helpers make these useful tests, not assertion-free no-ops.
Repeated fixture rewriting/certificate construction remains large; no clone percentage was measured.
Do not label all former lib-0% modules dead: machine, linking, registers09 and source expansion have explicit integration call sites.
The inverse-pair theorem route is now live ([dispatch](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/claims.rs:696), [delegation](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/claims/replay09.rs:344)); its second replay dispatcher remains redundant, as the existing review notes.

## Against the 2026-11-05 baseline

Baseline sources: [per-repo audit](/home/tobias/Projects/bennett-workspace/bennett/docs/quality/2026-11-05-audit/bennett-isa-spec.md) and [synthesis](/home/tobias/Projects/bennett-workspace/bennett/docs/quality/2026-11-05-audit/SYNTHESIS.md).
Fixed means supported by current code and, where listed above, a reproduced bounded test; “partly” preserves verification limits.

| Baseline finding / recommendation | Status | Current evidence |
|---|---|---|
| qinplace source test red (R1) | fixed | [lexical alias](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/source_constructor/action/qinplace.rs:24) and [allocation/release and arithmetic regression](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/isa09_qinplace.rs:321) |
| r21 wrong §4.3 expectation (R1) | fixed | [qreg §3.3](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/r21_resources.rs:204); dense allocation still asserts §4.3 |
| Unbounded 23.8 GB forwarding path / slow split (R2) | partly | [named ignore](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/isa09_forwarding.rs:204), 1,024-leaf default witness and [cap](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tools/test-slow-source-forwarding.sh:4); default total still above target |
| Metadata/lib/cleanup slow tests (R2) | partly | profile is now opt-level=1; observed lib 108.6→11.39 s on different shared-host loads, so not an isolated speedup; metadata/lifted-cleanup not remeasured |
| ~110 MB debug test binaries (R3) | fixed for profile; sampled | [test profile](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/Cargo.toml:10); rebuilt qinplace 43.92 MiB, no all-target size claim |
| Consolidate ~70 test binaries (R4) | not fixed | 63 top-level integration .rs targets remain; no explicit consolidated test target in Cargo.toml |
| Integration coverage / five weakest areas (R5) | partly | this audit measures 55.82% on lib+qinplace and resolves several old zeroes; full integration/CLI coverage and the repo-local record remain absent |
| Four requested god-function splits (R6) | not fixed | constructor/validation/action unchanged; step_prepared still 446 lines; all eight >300 remain |
| No-op preparation hooks | not fixed | [lib hook](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/lib.rs:164), [CLI hook](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/main.rs:2415) |
| Discarded object-parser base | not fixed | [binding](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/object.rs:1320); baseline overstated its semantic consequence |
| Process/job tags and fixtures (R7) | not fixed | [source tag](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/classical.rs:890), [fixture](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/main.rs:2448) |
| 72 unwrap_or patterns / unsound scheduled proof | partly | 88 candidate sites remain; scheduled subjects now explicitly Unverified with no coverage ([guard](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/claims/replay09.rs:354)) |
| Every inverse_pair claim rejected / parked pair path | fixed | entry-aware theorem replay ([pair verifier](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/claims/pairs09.rs:382)), exhaustive positive/negative qinplace regressions |
| Lib-only coverage floor | regressed numerically | 42.6% → 42.01% lines (23,971 → 24,434 denominator); selected integration raises the common-library floor to 55.82% |
| Other 0.9 paths called potentially dead | partly | explicit linking/qreg/machine integration call sites disprove a blanket dead-code claim; complete measured classification still owed |
| Tracked pycache/backtrace (R7) | not fixed | git ls-files still lists both; [log](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/fixtures/r22/hostcall-backtrace.log:1) |
| Stale HANDOFF and HEAD WIP checkpoint (R7) | partly | HEAD is reviewed-batch merge 3b10907; [November 1 handoff](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/HANDOFF.md:1) remains linked |
| CLI wrappers / conditional hash checks | not fixed | [conditional hash](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/cli_xam.rs:1407), shared assertion helpers remain; a wrapper is not automatically a weak test |
| Broad is_err and fixture self-oracles | partly | new semantic negatives pin reason/state; [parse-only sample](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/isa09_review.rs:41) remains weak; 65 bare single-line is_err checks |
| Five ignored sweeps ungated | not fixed | [ignored differential](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/r1_fuzz_discipline.rs:298); gate only adds the sixth forwarding witness |
| Unknown nesting | fixed as measurement | this audit records lexical depth (up to 9), with method limitations |

| Grade | Baseline → current | One change that would move current grade up one step |
|---|---|---|
| Code | C+ → B- | split the touched classical execution phase and largest constructor with phase-specific semantic checks; retire stale/litter paths |
| Tests | B- → B | measure representative integration/CLI coverage and replace parse-only/weak canonical checks with independently pinned semantics |
| Build | C → C+ | consolidate integration targets and demonstrate default execution <180 seconds on the bounded profile |

## Plan targets

Checks apply to this repository, not the other ecosystem rows. “Not met” includes an unverified target; no full suite was run to infer global green.

| Target | Status | Command + result / evidence |
|---|---|---|
| No red main default run | not met as audit-verified exit criterion | bounded selected runs 113 passed / 0 failed; complete default run intentionally prohibited; quality.md:407 claims 688/0/6, not independently reproduced |
| No live sibling instead of gate pin | met for declared gate path, static | read gate.toml:34–44 and draft_witnesses.py:272: compatibility binary is a declared exact review pin; default_bin points within this repo; gate materialisation not executed |
| Measured coverage number recorded in repo docs/quality.md | not met | rg coverage docs/quality.md reports “deferred”; auditor-only measurement does not update the repository record |
| Default tests <180 seconds, slow tests tagged/gated | not met | full run skipped by safety brief; docs/quality.md:407–408 records 278.86/481.38 s; only forwarding got a named slow gate |
| Test grade at least B | met | this audit's 18-function sample plus reproduced bounded regressions → B |
| Code grade at least B- | met | current fail-loud theorem/token/admission design → B-, with structural debt listed |
| No >300-line functions in P0/P1-touched files, others owned | not met | lexical scan: 8 remain, including classical.rs::step_prepared in a touched file; quality.md defers decomposition without per-function owner inventory |
| Zero bead/job identifiers in source/output | not met | rg codex finds classical.rs:890 and main.rs:2448; test names allowed by policy do not excuse production comments |
| Zero tracked pycache/log/lock/backup/progress litter | not met | git ls-files lists one .pyc, one .log and five PROGRESS files; Cargo.lock retained as required package metadata, not treated as scratch lock |

Additional round-1 requirements: no integration consolidation, no quality ratchet in gate.toml, HANDOFF.md not retired, and no committed coverage percentage ([deferred work](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/quality.md:224)).
The 180-second claim above is **not independently timed**; the repository's own latest recorded values already exceed it.

## What is good

1. Proof and executable applicability are separate enums/report fields; an independent unresolved root survives empty claim/record collections ([CertificateReport](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/claims.rs:48), [empty-record regression](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/isa09_qinplace.rs:1184)).
2. Entry-bound inverse-pair proofs preserve pair identity, domains, budgets and token partitions, cross-check two engines and reverse all private state ([independent run/reversal](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/claims/pairs09.rs:507)).
3. Scheduled semantics fail explicitly as Unverified instead of silently certifying reference execution ([scheduled guard](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/src/claims/replay09.rs:354)).
4. Forwarding retains published small-domain execution and a bounded source semantic witness while isolating wide capacity materialisation ([published domain](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/isa09_forwarding.rs:36), [source witness](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/isa09_forwarding.rs:97)).
5. Resource tests distinguish host allocation failure from ISA faults and assert state restoration rather than merely successful execution ([resource helper](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/r21_resources.rs:32), [nonzero reply restoration](/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/tests/r22_retention.rs:61)).

## Recommendations

1. Consolidate the 63 integration binaries and profile the remaining default runtime; keep slow semantic checks explicitly gated and bounded.
2. Record a fresh representative lib/integration/CLI coverage result in docs/quality.md, naming excluded paths instead of calling lib-0% modules dead.
3. Split classical::step_prepared and constructor::oracle into semantic phases, retaining exhaustive result/reversal checks at each boundary.
4. Replace the five-group parse-only test and weak catalog canonicality check with field assertions and independent canonical-byte expectations.
5. Retire HANDOFF.md, update README status, untrack cache/log/PROGRESS litter and remove process tags without changing contract fixtures.
6. Add the planned baseline ratchet with a wrapper-count companion; preserve total complexity measurement so extraction cannot game it.
7. Review each unwrap_or-family site against its contract, preserving specified defaults and adding wrong-result tests only where a failure can be hidden.

Final verification: HEAD and origin/main still equal the audited SHA; git diff --exit-code and git status --short are clean in the audited repository. Only this report and the explicitly permitted scratch directory were written.
