# bennett-isa-spec quality audit 2026-11-05
## Verdict
- Code: C+. A careful, fail-loud reference interpreter, but 55 functions exceed 100 lines (one is 1089) and the tree has several dead or parked 0.9 paths.
- Tests: B-. About 650 oracle-flavoured tests with real exhaustive domains and hand-derived expectations, but the suite is red (2 failures verified) and several tests cost minutes each.
- Build: C. Debug test binaries are about 110 MB each across 70 binaries, `--no-run` takes 62-187 s, and the repo's own gate runs the whole suite (OOM hazard).
- The `main` HEAD be109bd is a Codex "attempt end" WIP checkpoint, so the red state is committed.

## Composition
Measured with cloc, excluding target, .tmp and .git (1016 files).

| Language | Files | Code LOC |
|---|---|---|
| Rust | 177 | 67,375 |
| Markdown | 155 | 34,316 (spec, worklog, docs) |
| JSON | 617 | 19,840 (conformance cases) |
| diff | 1 | 4,621 |
| Python | 47 | 4,578 |
| Shell, TOML, YAML, header | 13 | about 460 |

Rust split: reference-interpreter/src about 31.2k at depth 2, plus subdirs. reference-interpreter/tests has 63 top-level files and 24.5k lines. conformance/src has 4.7k lines and conformance/tests has 38 files.

Module map (reference-interpreter/src, LOC):
- main.rs 2606: CLI (`check`, `hash`, `run-action`, ...)
- borrow.rs 2322: borrowed-qubit lifetime analysis (`compile`, 328-line function)
- classical.rs 2110: classical machine
- validation.rs 2019: object validation (+ cleanup, qinplace09, registers09)
- object.rs 1964: parser and object model
- machine.rs 1414: oracle step machine
- source_constructor.rs 1301: 0.9 source constructor
- action.rs 1201: action-sequence semantics
- claims.rs 1140: claim and certificate checking (+ claims/*09)
- oracle.rs 978, certificate.rs 933, quantum.rs 918, exact.rs 814, metadata/ about 800 each
- Smaller: json, sha256, tokens, identity, ref_library, and others.

- Dependencies: the interpreter has 2 Cargo.lock packages (itself plus the in-repo conformance crate); conformance has 1. There are zero third-party crates, including no proptest, serde or sha2 (sha256 and json are hand-written). Python is stdlib only (the `-I` runs).
- Python: 19 tool/test scripts, 999 LOC, plus isa_check.py (549 lines). scripts/ is just pre-push and install-hooks.sh.
- Authorship: 411 commits, all author "tobiasosborne". Only 1 commit carries an `Agent: gpt` trailer, and 64 are `wip(codex job` checkpoints (about 16%). Most others are Claude sessions committed under the maintainer's identity, so the mix is not recoverable from author fields.

## Build and test times
Target cache: warm, 17 GB, last built Oct 29 to Nov 3. The sha256.rs touch ran after the first `--no-run`.

| Step | Wall |
|---|---|
| `cargo test -j3 --no-run`, first (some recompile; cache not fully fresh) | 186.9 s |
| touch src/sha256.rs, then `--no-run` | 61.7 s |
| `--lib` (32 tests, all pass) | 108.6 s (85 s of that is one test, `r14_generated_metadata_schema_type_family`) |
| `--test metadata` (28) | 219 s |
| `--test isa09_lifted_cleanup` (1) | 55 s |
| `--test isa09_qinplace` (9: 8 pass, 1 FAIL) | 61 s |
| `--test r21_resources` (9: 8 pass, 1 FAIL) | 1.3 s |
| structured, r2_validation, registers, r1_rules, isa09_review | each under 0.25 s, 4+4+12+17+28... all pass |
| `cargo llvm-cov --lib` (instrumented rebuild and run) | 139 s |

Counts:
- Tests: 613 `#[test]` in tests/ plus 35 in src, so about 648. HANDOFF says 524 passed on Nov 1; the review says 639 pass + 2 fail + 5 ignored on Nov 3.
- Ignored: 5 (r1_certificates.rs:113, oracle.rs:262, r1_borrow.rs:63, r1_fuzz_discipline.rs:298, step_machine.rs:98). All are exhaustive sweeps or differential fuzz, never run by the gate.
- Red: the 2 in bead x6to are confirmed, but one is not what the bead says (details below).
- Not run, per the OOM hazard: the full suite, isa09_forwarding, cli_xam, r1_fuzz_discipline, and the conformance crate.
- Test binaries (70) by size, top 12, each about 110 MB: isa09_cleanup 111.2M, isa09_token_aliases 111.2M, isa09_forwarding 111.1M, k83_source_support 110.9M, isa09_qinplace 110.9M, isa09_memory_address 110.7M, k91_vectors 110.7M, isa09_source_schedule 110.5M, source_constructor 110.5M, isa09_lifted_cleanup 110.5M, source_addressing 110.0M, isa09_pinned_free 109.8M. Each links the whole crate plus conformance statically, so debug-info bloat is about 7 GB of binaries. Full list in /home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/audit-tmp/bins.txt.

Red tests, verified:
1. `isa09_qinplace::source_qinplace_adjoints_preserve_instruction_allocation_and_release_order` panics at tests/isa09_qinplace.rs:286 (an `.unwrap()` on `expand_action_source_with_token_aliases`). That is the fuk.7 gap, but it is a different test name than the review's "published Example 7", and the other 8 tests in the file pass.
2. `r21_resources::r21_quantum_cardinality_and_lengths` fails at tests/r21_resources.rs:29. The child process panics with "§3.3: host limit: qreg class vector allocation of 9223372036854775807 elements failed". The bead says the test expects §4.3 while registers.rs:188 cites §3.3. The message now says §3.3, so this is a stale citation in the test (a test bug, not an interpreter bug).
- HANDOFF.md is stale (Nov 1, pre-dates the Nov 3 WIP commits; it says 524 passed, 0 failed). Its claim "0 failed" is false at HEAD.

## Coverage
Measured: `cargo llvm-cov --lib` only, so it counts unit tests (35, mostly in src/) and not the 63 integration binaries, which carry the real suite. It is a floor, not the coverage. main.rs (a bin) is excluded.

| Measure | lib-only |
|---|---|
| Line | 42.6% (13,761 of 23,971 missed) |
| Function | 40.2% |
| Region | 38.8% |

0% under lib tests (exercised, if at all, only by integration tests, which I did not instrument): machine.rs (1189 lines), source_constructor.rs and its 3 submodules (about 2,180), ref_library.rs and tokens (630), claims/pairs09.rs and replay09.rs, linking.rs (355), validation/cleanup.rs, validation/qinplace09.rs, validation/registers09.rs, classical/registers09.rs, metadata/source_events.rs, schedule_domains.rs.

Structural cross-check by grep: machine.rs is reached by tests/step_machine.rs, source_constructor by tests/source_constructor.rs, and ref_library by isa09_* binaries. The review (docs/reviews/2026-11-03-isaref-batch.md, 7cvg) finds that claims/replay09.rs:337-342 rejects every `inverse_pair` claim with no test. That fits the 0% above. I did not measure integration coverage because a full instrumented build of 70 x 110 MB binaries would break the 10-minute and RAM budget.

Weakest or untested areas:
1. claims/replay09.rs and pairs09.rs (0% in lib; per review 7cvg, unreachable paths with no test).
2. claims/qinplace09.rs, validation/qinplace09.rs (about 1-4% in lib; the one qinplace expansion test is red).
3. borrow.rs 35% and action.rs 24% in lib; deferred to integration tests, which are not instrumented.
4. tokens.rs 10%, call_discipline.rs 22%.
5. main.rs (2606 lines, a bin, unmeasured) is covered only by cli_xam.rs subprocess tests.

## Test quality
Sampled 16 tests at random (seed 5):

| file:line | verdict | why |
|---|---|---|
| structured.rs:20 | useful | asserts parsed shape and rejects mutated bounds with exact section code |
| cli_xam.rs:1390 | useful | CLI end-to-end with pinned witness hashes |
| r2_validation.rs:29 | useful | loops over bad types and requires a specific §3.3 reject |
| registers.rs:44 | useful | runs a machine with two draws, checks values and fault code and irreversibility |
| r1_borrow.rs:646 | useful | table of clean and dirty frames checked against an oracle map (r6_map) |
| isa09_lifted_cleanup.rs:7 | weak | long hand-built schedule hash plumbing, see below |
| r1_rules.rs:47 | useful | hand-derived expectation (comment: t ^= bit p of a5) over all 16 inputs |
| isa09_review.rs:54 | useful | positive and negative parse (one parse, one `is_err`) |
| metadata.rs:317 | useful | compares to pinned r14 pins JSON |
| cli_xam.rs:1656 | weak | one-line wrappers over `r9_cli_identity`; assertions live in the helper |
| r1_borrow.rs:722 | weak | `if !oh.is_empty()` makes the object-hash assertion conditional |
| r23_transaction.rs:125 | useful | literal envelope files committed alongside fixtures |
| cli_xam.rs:1855 | useful | adjoint/forward loop on both inputs |
| step_machine.rs:122 | useful | exhaustive 2 x 256 x 10 domain with hand-written expected (code, payload) |
| r22_coverage.rs:4 | useful | false-proof must be rejected, full control accepted |
| isa09_forwarding.rs:36 | useful | exhaustive 4x4x256 against a closed-form formula, token budget checked |

Ratio: 13 useful, 3 weak, 0 tautological. The suite shows good habits: hand-derived expectations, negative tests that name the spec section, and exhaustive small domains. There is no property-based testing (no proptest, zero third-party crates), and the ignored fuzz sweep (r1_fuzz_discipline.rs:298) never runs.

Weak points:
- isa09_lifted_cleanup.rs:7 and similar tests build whole objects by string-replace of "=0.8" with "=0.9" (e.g. isa09_review.rs:54), which makes them depend on the fixture text.
- The 74 bare `is_err()` assertions (grep) accept any error and do not pin the spec section the way `bad(..., "§x")` does.
- Many tests re-hash their own fixtures (`rehash`) and then compare to hashes computed by the same implementation (self-oracle) unless pinned by r14_pins.json or the Python tools. The independent oracles are the Python tools (`ref_catalog.py --check`, draft_witnesses.py) and the conformance crate's expected-value tables (219 recipes, pinned envelope hash).

Would the gate catch a wrong result? gate.toml runs `cargo test` of both crates, draft_witnesses.py and the catalog check. For semantic regressions in the classical/oracle machines, yes: the exhaustive-domain tests would catch them. It runs the whole `cargo test` (including isa09_forwarding at up to 23.8 GB) with timeout_s 14400, and a red suite blocks every push. That means the gate cannot pass at HEAD be109bd, and the ignored sweeps (5) are not gated.

## Code quality
Rule 9 and fail-fast findings:
1. src/source_constructor.rs:81 `oracle()` is 1089 lines, with 621 more in validation.rs:110 `validate_action_sequence`, 497 in action.rs:413 `action_sequence`, 445 in classical.rs:1463 `step_prepared`, and 411 in main.rs:1981 `run`. 55 of 912 functions exceed 100 lines. Cost: unreviewable, and a single edit can break unrelated cases.
2. Test-hook seams in production code. main.rs:2414-2421 `cli_preparation(stage)` and lib.rs:158-166 `preparation(rule, stage)` are no-ops outside `#[cfg(test)]` (`let _ = stage;`). These are trivial wrappers that exist only to inject faults in tests, and they are called from production paths.
3. object.rs:1320 `let _ = base;` binds a value and discards it. The `strip_prefix("lift.")` filter result is not used, so it is a dead binding.
4. Bead/review/session references in source: grep finds 49 matches for codex/B14/r21/r22/fuk/Rnn in src (e.g. classical.rs:890 "(codex B09)", fixtures named `codex-store-retry.bisa`, `sol-*`, `codex-*`, included from r23_transaction.rs:222,300 and main.rs:2448). Failure scenario: names mean nothing after the job directories are deleted.
5. Silent-default patterns: 72 `unwrap_or*` in src; I did not read them all, but the reviewer's claim "7cvg: `inverse_pair` claims always error" (claims/replay09.rs:337) shows the opposite failure: stubbed branches that fail loud but unconditionally. Narrowing the K4/K92 obligation is noted in that review.
6. Parked 0.9 path: HANDOFF says .3-.7 are partial. `claims/pairs09.rs`, `replay09.rs`, `classical/registers09.rs`, and `linking.rs` show 0% under lib tests. If the integration suite also never reaches them they are dead code.
7. Tracked litter: `reference-interpreter/__pycache__/isa_check.cpython-312.pyc` and `tests/fixtures/r22/hostcall-backtrace.log` are tracked in git. 64 `wip(codex job` commits are on main history, and HEAD is a WIP checkpoint.
8. Stale docs: HANDOFF.md reports a green state (0 failed) that is false at HEAD.
9. Duplication: 1-line test wrappers (cli_xam.rs:1390-1400, 1656-1665) and many near-identical `r*_cli_*` cases; I did not quantify.
10. Complexity: the longest-function numbers above came from a brace-matching script over src/**/*.rs. Nesting depth was not measured.

## What is good
1. Zero third-party dependencies, so the oracle's trust base is auditable and the build has no supply chain risk. JSON and SHA-256 are hand-written and covered 100% (sha256.rs) and 67% (json.rs).
2. Exhaustive small-domain tests against closed forms (isa09_forwarding.rs:36, step_machine.rs:122). These measure behaviour, not mere execution.
3. Negative tests name the spec section they expect (`bad(..., "§5.3")`), so a wrong reason fails the test; r21 shows this working (it caught the §3.3 / §4.3 drift).
4. Independent Python catalog and witness checkers, with pinned envelope hash (219 recipes), gated by gate.toml.
5. An honest review (docs/reviews/2026-11-03-isaref-batch.md) that already found a real P1 (7cvg) and listed the red tests.

## Recommendations
1. Fix or `#[ignore]` with a bead the 2 red tests, and update r21_resources.rs expectation to §3.3 (one line). Until then no push can pass the gate.
2. Mark and split the slow tests: metadata (219 s), lib `r14_generated_metadata_schema_type_family` (85 s), and isa09_lifted_cleanup (55 s) deserve a faster fixture or `--release`-tested profile.
3. Cut debug info for test profile (`[profile.test] debug = 0` or `debug = "line-tables-only"`): 70 binaries at 110 MB is about 7 GB and most of the 62 s relink.
4. Merge the 70 integration binaries into a few (or a `tests/it/main.rs`), which also removes the per-binary static link of the crate.
5. Add an integration-coverage run (`cargo llvm-cov` on a chosen subset, with the OOM test excluded) so the 0% modules can be classified as dead or merely integration-covered.
6. Split `source_constructor::oracle`, `validate_action_sequence`, `action_sequence` and `step_prepared` into named phases.
7. Remove tracked litter (`__pycache__`, `hostcall-backtrace.log`), rename `codex-*`/`sol-*` fixtures and strip bead/job tags from comments, and refresh HANDOFF.md.
