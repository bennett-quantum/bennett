# bennett-circuits quality audit 2026-11-07

## Verdict
- Code **B-**: clear semantic boundaries and explicit failures; six large semantic functions and string-based contracts still concentrate risk.
- Tests **B+**: 210 passing default tests, independent reference comparisons and external syntax checks; some acceptance-only checks and shared simulator code limit independence.
- Build **B+**: cold test compilation 72.93 s, default tests 11.71 s; the approximately 7 GB oracle tests are now separate.
- Coverage **85.15% lines / 77.83% functions**, measured on the default suite; no new product correctness defect established by this audit.

Audited origin/main **5d10d65275106ca2a63e73e179bd02fe42e8de6d**. Main checkout HEAD is **16efee53285ff814e5d3d4a5f558e79e1c3e736c**; `git diff --stat origin/main HEAD` shows only `.beads/issues.jsonl` (17 changed lines). The tracked working tree was clean before/after inspection. No fetch, commit, Beads operation, source edit or full gate was performed.
Tests ran on an exact `git archive` of origin/main inside permitted scratch, since several tests write below `CARGO_MANIFEST_DIR/.tmp`. The scratch `.git` pointer supplies read-only tracked-file inventory; the additional main commit changes no inventoried path. Pinned sibling inputs and binary were read, never rebuilt. UTC completion: 2026-11-07 10:41:54 UTC.

## Composition

Measured with `cloc --skip-uniqueness --list-file=/home/tobias/Projects/bennett-workspace/bennett-circuits/.tmp/reaudit-2026-11-07/tracked.txt --by-file --json`. The list was generated from absolute paths returned by `git -C /home/tobias/Projects/bennett-workspace/bennett-circuits ls-files`.

| Language / directory | Files | Code LOC |
|---|---:|---:|
| Rust source | 31 | 21,327 |
| Rust tests/support | 21 | 6,233 |
| Python scripts | 5 | 489 |
| Shell scripts and Beads hooks | 9 | 269 |
| Markdown docs/worklog/root/agent metadata | 21 | 1,894 |
| JSON | 5 | 152 |
| TOML | 4 | 51 |
| YAML | 2 | 6 |
| **Total classified** | **98** | **30,421** |

There are 102 tracked files; four are unclassified by cloc. Rust totals 27,560 code lines. Default cloc deduplicates one identical 303-code-line module and reports 30,118 total instead; `--skip-uniqueness` preserves both physical copies. Cargo.lock contains **one package, zero third-party crates** ([Cargo.toml:5](/home/tobias/Projects/bennett-workspace/bennett-circuits/Cargo.toml:5)). Python tooling uses stdlib plus the external QASM/Quil parser environment (four explicitly pinned package versions at [tests/exporters.rs:155](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/exporters.rs:155)); LLVM 18 and uv are required test tools, not linked crate dependencies.

Top-level module map: code LOC, excluding comments/blank lines. Each row corresponds to one source file.

| Module | Purpose | Code LOC |
|---|---|---:|
| [amplitude](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/amplitude.rs:1) | exact dyadic/phase arithmetic | 303 |
| [borrow](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/borrow.rs:1) | borrow-frame certificate checks | 234 |
| [certificate](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/certificate.rs:1) | certificate generation/replay/composition | 1,248 |
| [checker](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/checker.rs:1) | schema/liveness/cleanup proofs | 2,839 |
| [classical](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/classical.rs:1) | CC/R diagnostic interpreter | 1,203 |
| [coverage](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/coverage.rs:1) | source trap coverage records | 68 |
| [export](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/export.rs:1) | export metadata codec | 96 |
| [flatten](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/flatten.rs:1) | hierarchy to flat gates/events | 419 |
| [frame](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/frame.rs:1) | typed draft resource frames | 357 |
| [history](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/history.rs:1) | symbolic instruction histories | 2,029 |
| [ir](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/ir.rs:1) | hierarchical circuit types | 314 |
| [ir_codec](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/ir_codec.rs:1) | IR JSON codec | 358 |
| [json](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/json.rs:1) | canonical/object and target JSON | 406 |
| [lib](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/lib.rs:1) | module/API/error root | 64 |
| [linking](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/linking.rs:1) | closure registry and proof linking | 435 |
| [lower](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/lower.rs:1) | action specialisation/lowering | 1,364 |
| [main](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/main.rs:1) | CLI parsing and dispatch | 1,091 |
| [metadata](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/metadata.rs:1) | metadata schemas/bindings | 1,068 |
| [object](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/object.rs:1) | text object parsing/signatures/identity | 1,897 |
| [oracle](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/oracle.rs:1) | bounded reversible oracle materialisation | 1,555 |
| [placement](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/placement.rs:1) | lifetime/class/resource placement | 849 |
| [proof](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/proof.rs:1) | finite-domain proof simulation | 240 |
| [qasm](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/qasm.rs:1) | OpenQASM export/import | 433 |
| [qir](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/qir.rs:1) | QIR export/import | 403 |
| [quil](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/quil.rs:1) | Quil export/import | 126 |
| [selectors](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/selectors.rs:1) | selector immutability validation | 132 |
| [sha256](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/sha256.rs:1) | SHA-256 identity implementation | 106 |
| [simulation](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/simulation.rs:1) | sparse exact diagnostic simulation | 132 |
| [step_check](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/step_check.rs:1) | row diagnostic execution checks | 377 |
| [target](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/target.rs:1) | target costs/templates/expressions | 972 |
| [translation](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/translation.rs:1) | borrow translation witnesses | 209 |

Authorship: `git -C /home/tobias/Projects/bennett-workspace/bennett-circuits log origin/main --format=%an%x1f%s%x1f%B%x1e` yields **85 commits**, all author `tobiasosborne`. Classifying `Agent: gpt...` or `wip(codex job` first, then Claude coauthor markers: **24 Codex-marked (28.2%), 30 Claude-marked (35.3%), 31 unmarked (36.5%)**. Unmarked does not establish human authorship; underlying implementation authorship cannot be inferred from merge/orchestrator commit authors alone.

## Build and test times

All Cargo runs used a user systemd scope, headless environment, `timeout 600`, `ulimit -v 8000000`, `-j3`, and test threads 4. Each start checked available memory >=6 GB and load <12 under the initial brief; after the binding update, starts require load <8 and no `bennett-heavy` scope, polling every 60 s for at most 30 min. Resource wait time is excluded from compiler/test wall times. The initial dev build waited for an active heavy scope to end, and the warm rebuild waited for load to fall below 8; all requested timing measurements obtained a slot within the 30-minute limit. Baseline measurements were taken under a different, higher machine load; these are not controlled compiler-speed comparisons.
Scratch is `/home/tobias/Projects/bennett-workspace/bennett-circuits/.tmp/reaudit-2026-11-07`; all generated fixtures, copied uv cache, targets and logs stayed there. Original source timestamps were not touched. Re-hashing all 102 snapshot tracked files against origin/main Git blob IDs found zero content differences after the measurements. The copied uv cache avoids writes to the user's shared cache.

| Measurement | Wall seconds | Peak KiB | Result / cache |
|---|---:|---:|---|
| `cargo test --offline --no-run -j3` | 72.93 | 722,244 | pass; initially empty audit target |
| Default `cargo test --offline -j3 -- --test-threads=4` | 11.71 | 128,828 | 210 passed, 0 failed, 3 ignored; compiled target warm |
| `cargo llvm-cov --offline --summary-only -j3 -- --test-threads=4` | 77.52 | 750,184 | pass; separate initially empty coverage target, including compilation |
| Initial dev-profile `cargo build --offline -j3` | 32.05 | 995,604 | pass; test profile existed, dev profile not yet built |
| Touch snapshot `src/json.rs`; dev `cargo build --offline -j3` | 1.99 | 300,752 | pass; warm incremental rebuild |
| Touch snapshot `src/json.rs`; `cargo test --offline --no-run -j3` | 1.98 | 349,760 | pass; warm test-compilation rebuild |

Exact measured commands (the saved runner checks the slot and installs the limits above):

```sh
scratch_dir=/home/tobias/Projects/bennett-workspace/bennett-circuits/.tmp/reaudit-2026-11-07
source_manifest=/home/tobias/Projects/bennett-workspace/bennett-circuits/.tmp/reaudit-2026-11-07/source/Cargo.toml
audit_run() { env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER TMPDIR="$scratch_dir/tmp" python3 "$scratch_dir/run.py" "$@"; }
audit_run no-run cargo test --offline --manifest-path "$source_manifest" --no-run -j3
audit_run default-test cargo test --offline --manifest-path "$source_manifest" -j3 -- --test-threads=4
audit_run coverage cargo llvm-cov --offline --manifest-path "$source_manifest" --summary-only -j3 -- --test-threads=4
audit_run build-initial cargo build --offline --manifest-path "$source_manifest" -j3
touch "$scratch_dir/source/src/json.rs"
audit_run build-warm cargo build --offline --manifest-path "$source_manifest" -j3
touch "$scratch_dir/source/src/json.rs"
audit_run no-run-warm cargo test --offline --manifest-path "$source_manifest" --no-run -j3
```

Runner sets `CARGO_TARGET_DIR` to scratch `target`, or `cov-target` for coverage, and `BENNETT_GATE_LAYOUT=/home/tobias/Projects/bennett-workspace/bennett-circuits/.tmp/gate/cache/bennett-isa-spec@ecaaac060c44`. Tool: cargo-llvm-cov 0.9.1. An initial `llvm-cov --target-dir ...` attempt failed immediately (0.01 s, unsupported option); the successful command uses the environment. This was an auditor invocation error, not a repository failure.
Counts: **31 library + 176 integration + 3 oracle/support tests passed**; no binary/doc tests. Three ignores: two large oracle tests ([tests/oracles.rs:14](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/oracles.rs:14)), one promised symbolic-object test ([tests/static_checker.rs:1024](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/static_checker.rs:1024)). Heavy/slow oracle tests, conformance harness and push gate were deliberately not run. The default integration run also executes **11 Python resolver tests and 10 metrics self-tests**, not additional Rust test cases. The promised test was not executed in this audit; its source assertion still conflicts with the explicit symbolic-count rejection at [src/checker.rs:1450](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/checker.rs:1450). It is excluded from the observed zero default failures, not counted as passing.

## Coverage

LLVM source totals: **18,565 lines, 2,757 missed (85.15%)**; **1,633 functions, 362 missed (77.83%)**; **36,280 regions, 6,518 missed (82.03%)**. Includes source unit tests/closures and the CLI; branches are not instrumented. The two ignored large oracle tests and promised test are excluded. This measures exercised lines, not verified specification clauses or supported capability breadth.

| Five lowest-covered source areas | Line coverage | Missed / total lines | What is missing or weak |
|---|---:|---:|---|
| [src/main.rs:718](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/main.rs:718) | 60.06% | 407 / 1,019 | option/error combinations and schedule/target-launch refusal paths; only 49.04% functions executed |
| [src/step_check.rs:32](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/step_check.rs:32) | 72.25% | 96 / 346 | direct diagnostic row/domain errors beyond the small conformance corpus |
| [src/ir.rs:1](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/ir.rs:1) | 72.79% | 40 / 147 | malformed construction/geometry; valid circuits receive much stronger execution coverage |
| [src/linking.rs:1](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/linking.rs:1) | 73.55% | 96 / 363 | malformed/transitive closure conflicts and certificate claim composition combinations |
| [src/target.rs:331](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/target.rs:331) | 76.77% | 200 / 861 | malformed templates/expressions and unsupported target features |

The large oracle engine still misses **309/1,397 lines** (77.88%, [src/oracle.rs:534](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/oracle.rs:534)); its broad independent oracle sweep is deliberately outside the default run. Checker misses **359/2,575 lines** (86.06%, [src/checker.rs:181](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/checker.rs:181)), so the headline percentage is not a soundness proof. SHA-256 is 100% lines; placement 95.77%, flattening 95.76%, history 88.79%. The measured totals exactly reproduce [docs/quality.md:40](/home/tobias/Projects/bennett-workspace/bennett-circuits/docs/quality.md:40).

## Test quality

Random sample: sorted `tests/**/*.rs`, select individual `#[test]` declarations with Python `random.Random(20261107).sample(..., 20)` from **180 declarations** (includes the three ignored tests in the sampling population). All selected tests ran in the default suite. Classification uses the complete body and helper assertions, not a grep of the body alone.

| Sampled test, declaration line | Class | Why |
|---|---|---|
| [symbolic_angles_validate_exact_adjoint_histories_for_all_arguments](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/static_checker.rs:591) | useful | mutates angle bindings and requires §6.2 rejection |
| [scheme_expansion_is_exact_accounts_leaves_and_reuses_ancilla_frames](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/target.rs:213) | useful | literal gate/time/occupancy values plus capacity rejection |
| [pending_obligations_follow_transitive_calls_and_replay_the_linked_body](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:1581) | useful | pending→proved linking plus bad leaf body must reject |
| [classical_counts_angles_and_call_arguments_specialise](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/specialisation.rs:45) | useful | count/angle substitution reaches execution and literal identity states |
| [suite_c_action_reversal_and_subbyte_memory](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/diagnostics.rs:33) | useful | helper checks pinned expected exit and output, not count alone |
| [resolver_and_conformance_script_obey_pins](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/pinned_siblings.rs:14) | useful | executes 11 pin resolver/script regressions with failure assertions |
| [symbolic_workspace_spanning_calls_is_universal](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/static_checker.rs:798) | useful | wrong uncopy operand must reject |
| [interface_only_symbolic_loops_are_checked_by_composition_not_unrolled](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:1096) | weak | positive trillion-trip acceptance/status only; no semantic or negative partner here |
| [translation_witnesses_bind_source_points_and_wire_sets](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:601) | useful | tampered wire set must reject a translation witness |
| [full_domain_borrow_factorisation_is_not_a_zero_borrow_test](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:280) | useful | full borrowed domain and leaking counterexample |
| [zero_time_does_not_erase_scheme_capacity_requirement](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/target.rs:514) | useful | zero-duration scheme still must reject insufficient capacity |
| [missing_external_validator_is_a_failure](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/exporters.rs:149) | useful | test runner requires a missing-validator panic |
| [imported_region_contracts_bind_cc_handles_without_a_body](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/static_checker.rs:559) | weak | positive unlinked acceptance only; no malformed contract partner in this function |
| [executable_mutations_are_seen_without_ir_metadata](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/exporters.rs:75) | useful | mutates executable text and checks metadata/state disagreement |
| [full_tuple_certificate_roundtrip_and_tamper_rejection](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:215) | useful | tampered tuple/invocation and absent draft opt-in must reject |
| [source_cannot_forge_internal_history_annotations](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:1708) | useful | forged internal annotation must reject |
| [external_qasm_and_quil_parsers_accept_exported_syntax](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/exporters.rs:155) | useful | independent grammar parsers accept output and reject malformed controls |
| [history_versions_cover_predicated_copies_and_oracle_reads](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:881) | useful | changed quantum/control read versions must reject |
| [local_region_image_wires_are_pinned_and_validation_cannot_be_bypassed](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/placement.rs:166) | useful | pinned lifetime geometry and corrupted cleanup rejection |
| [oracle_reference_program_hash_is_checked_before_claim_replay](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:1210) | useful | mutated reference-program hash must reject |

Sample ratio: **18 useful (90%), 2 weak (10%), 0 tautological**. This is a sample, not a measured population rate. A whole-test-source scan finds just two bodies without inline assertion/error checks, both external-parser tests; both call `require_validator`, which asserts subprocess success ([tests/exporters.rs:133](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/exporters.rs:133)). No default assertion-free no-op test was identified. Some newly added `proof_status == "proved"` assertions only restate the success path of `Object::hash` ([src/object.rs:1921](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/object.rs:1921)); they do not independently test proof soundness.

Independent oracles: [tests/differential.rs:101](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/differential.rs:101) compares every action/basis in pinned fixtures/spec examples plus synthetic cases against the reference CLI, also checking QIR, Quil and three target placements. Its reference amplitudes use **absolute 2e-12 tolerance**, with exact support/workspace checks; this cannot certify errors below that tolerance. [tests/static_checker.rs:5](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/static_checker.rs:5) checks published verdicts/rule citations; [tests/diagnostics.rs:79](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/diagnostics.rs:79) checks pinned expected exit/stdout/stderr; [tests/proof_output.rs:354](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:354) checks certificate table rows against reference execution. External LLVM assembler/verifier and QASM/Quil grammar parsers run in the default suite; malformed controls are required to fail ([scripts/validate_exporters.py:11](/home/tobias/Projects/bennett-workspace/bennett-circuits/scripts/validate_exporters.py:11)).
The test arithmetic file is **byte-identical** to production ([tests/support/exact.rs:1](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/support/exact.rs:1) and [src/amplitude.rs:1](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/amplitude.rs:1)); test and production simulators differ only in their two import lines ([tests/support/sim.rs:1](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/support/sim.rs:1) and [src/simulation.rs:1](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/simulation.rs:1), `diff -u`). Those are shared-implementation checks, not independent simulators. The independent reference CLI and hand-derived literal witnesses remain essential. No property-testing framework/dependency exists; exhaustive finite basis domains and directed mutations supply the strongest evidence.
The configured gate would catch wrong results in exercised lowering/placement/certificate paths: it runs the same default suite plus both ignored oracle tests ([gate.toml:14](/home/tobias/Projects/bennett-workspace/bennett-circuits/gate.toml:14)). It now catches missing validators and malformed external syntax too. It still cannot establish grammar semantics of a real QASM/Quil backend, numerical/channel certificate validity, or promised symbolic-loop acceptance. Gate configuration was read; this audit did not execute the gate or claim its slow step green.

## Code quality

Read in full the three largest source files (checker 2,911, history 2,063, object 2,054 physical lines) and three largest test files (proof_output 1,822, static_checker 1,029, target 629), then inspected CLI, exporters, pin/metrics scripts, differential and supporting code. Findings below are maintenance/testing limitations; none establishes a new P0/P1 product-path failure.

| Finding | Evidence | Failure scenario or cost |
|---|---|---|
| Six semantic functions remain >300 lines | hotspot table below | opcode validation/execution and error precedence require reviewing many branches together |
| Checker worklist identity uses Debug strings | [src/checker.rs:2396](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/checker.rs:2396) | repeated allocation/formatting and representation-coupled deduplication per visited state |
| Errors remain untyped strings | [src/lib.rs:44](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/lib.rs:44); [tests/static_checker.rs:921](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/static_checker.rs:921) | tests/consumers must match prose; unrelated errors can satisfy an overly broad substring assertion |
| Repeated owned state and clone traffic | [src/history.rs:565](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/history.rs:565); [src/checker.rs:2396](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/checker.rs:2396); [src/oracle.rs:534](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/oracle.rs:534) | `.clone()` counts: history 136, checker 138, oracle 130; count is a hotspot indicator, not proof clones are removable |
| Repeated object fixture constructors | [tests/classical.rs:6](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/classical.rs:6), [tests/proof_output.rs:7](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:7), [tests/placement.rs:14](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/placement.rs:14) | copied object header/symbol setup can drift; `tests/support/fixtures.rs` centralises bindings only |
| Shared test/production arithmetic and simulation | [tests/support/exact.rs:1](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/support/exact.rs:1), [tests/support/sim.rs:1](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/support/sim.rs:1) | simulator errors can agree with a same-code twin unless a CLI/literal oracle detects them |
| Tracked backup remains | [.beads/hooks/pre-push.backup:1](/home/tobias/Projects/bennett-workspace/bennett-circuits/.beads/hooks/pre-push.backup:1); [docs/quality.md:123](/home/tobias/Projects/bennett-workspace/bennett-circuits/docs/quality.md:123) | explicit zero-litter target still fails; the ratchet grandfathers it |
| Required mechanics remain unavailable | [src/main.rs:75](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/main.rs:75), [src/main.rs:928](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/main.rs:928), [src/checker.rs:1450](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/checker.rs:1450) | schedule/target launch and symbolic object validation fail explicitly; capability gaps remain despite green defaults |

Complexity was measured by the repo's masked-source function scanner plus a small brace-depth probe. **581 named functions**, length buckets **402 at 1–30 / 132 at 31–100 / 41 at 101–300 / 6 over 300**, lexical complexity mass **10,237**, **104 forwarding-wrapper candidates**. These count nested functions/source tests and are lexical proxies, not 104 proven unnecessary wrappers. Maximum body brace nesting is **8** (JSON string parser [src/json.rs:335](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/json.rs:335), checker classical schema, certificate verification); classical execute and static action validation reach 7.

| Function | Current physical LOC | Evidence |
|---|---:|---|
| classical::execute | 536 | [src/classical.rs:445](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/classical.rs:445) |
| checker::classical_schema | 481 | [src/checker.rs:2379](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/checker.rs:2379) |
| oracle::row | 460 | [src/oracle.rs:534](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/oracle.rs:534) |
| oracle::specialise_impl | 364 | [src/oracle.rs:1207](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/oracle.rs:1207) |
| checker::schema | 329 | [src/checker.rs:181](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/checker.rs:181) |
| checker::static_parameter_action (including nested prepare) | 304 | [src/checker.rs:1947](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/checker.rs:1947) |
| history::invoke / evaluate_body | 280 / 125 | [src/history.rs:1411](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/history.rs:1411) / [src/history.rs:440](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/history.rs:440) |
| certificate::verify / metadata::certificate_mode | 277 / 269 | [src/certificate.rs:999](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/certificate.rs:999) / [src/metadata.rs:736](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/metadata.rs:736) |
| placement::place_target_program / CLI run_basis | 264 / 254 | [src/placement.rs:307](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/placement.rs:307) / [src/main.rs:300](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/main.rs:300) |

`python3 -I /home/tobias/Projects/bennett-workspace/bennett-circuits/scripts/quality_metrics.py` passes. Its process-identifier count is **0**; explicit source Bead/milestone grep returns no matches. The single tracked litter path is `.beads/hooks/pre-push.backup`; agent/editor settings are configuration, not automatically WIP litter. CLI has **zero lines >200 characters**, and `rustfmt --edition 2024 --check /home/tobias/Projects/bennett-workspace/bennett-circuits/src/main.rs` passes. Thirteen >200-character source lines elsewhere are chiefly fixture strings/JSON, not minified dispatch.
Fail-fast sweep still has **89** lexical `let _ =` / `.ok()` / `unwrap_or*` matches. Reviewed uses include sparse-map empty-set defaults and optional dependency refinements; this audit establishes no hidden-error fallback from that count. `CheckReport` status/proof status are strings ([src/object.rs:216](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/object.rs:216)), while live history/maps encode distinct, simultaneously valid properties; replacing every boolean with an enum is not justified.
No dead-code fraction was established: **362 unexecuted LLVM functions/closures are not evidence of dead code**. The alleged lonely `version()` has a production certificate caller ([src/certificate.rs:726](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/certificate.rs:726)), already present at baseline. Duplication was verified for arithmetic/simulation and fixture setup; no repository-wide clone-detector percentage is claimed.

## What is good

- Hash/check perform semantic and certificate verification before reporting identity ([src/object.rs:1868](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/object.rs:1868)); false program relations and field tampering have direct regressions ([tests/proof_output.rs:32](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:32)).
- History phases own one state and preserve formal atoms, control/version dependencies and exit validation ([src/history.rs:440](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/history.rs:440), [src/history.rs:565](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/history.rs:565)); sixteen phase witnesses cover the extraction.
- Reference CLI comparisons and independent grammar checks complement exact/literal witnesses ([tests/differential.rs:101](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/differential.rs:101), [tests/exporters.rs:155](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/exporters.rs:155)).
- Pin resolution fails closed on missing/mismatched layouts and never falls back to a live sibling ([scripts/pinned_sibling.py:19](/home/tobias/Projects/bennett-workspace/bennett-circuits/scripts/pinned_sibling.py:19)); integration executes its negative regressions.
- Default suite is small enough for the edit loop; slow oracle domains remain in the configured gate ([Cargo.toml:5](/home/tobias/Projects/bennett-workspace/bennett-circuits/Cargo.toml:5), [gate.toml:14](/home/tobias/Projects/bennett-workspace/bennett-circuits/gate.toml:14)).

## Against the 2026-11-05 baseline

Compared with [baseline report](/home/tobias/Projects/bennett-workspace/bennett/docs/quality/2026-11-05-audit/bennett-circuits.md:1) and [ecosystem synthesis](/home/tobias/Projects/bennett-workspace/bennett/docs/quality/2026-11-05-audit/SYNTHESIS.md:1). Grades re-derived from current code, sampled assertions and measured runs, using the same A–F/subgrade scale; no baseline test suite rerun was attempted.

| Dimension | Before | After | One step up would require |
|---|---|---|---|
| Code | C+ | B- | B: reduce the remaining large semantic handlers with independent negative/positive witnesses and give typed validation states/errors clearer ownership |
| Tests | B | B+ | A-: strengthen acceptance-only checks and broaden independent semantic/error-path coverage, especially CLI/link/target and oracle paths |
| Build | B- | B+ | A-: reproduce the separately configured slow step's bounded resource/time requirements and make external test prerequisites reproducible without a prewarmed environment |

Coverage: **84.86% → 85.15% lines (+0.29 percentage points)**; functions **77.2% → 77.83%**. Both exclude large oracle execution, but refactoring changes denominators. CLI line coverage **65.4% → 60.06%** is a measured regression in coverage, not an observed result regression. Passing tests **200 → 210**, ignores **0 → 3**; the ignores are visible and the two slow tests remain gate-selected.

| Baseline finding | Status | Current evidence |
|---|---|---|
| Code finding 1: minified CLI dispatch | fixed | readable run/launch/export handlers, [src/main.rs:703](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/main.rs:703), [src/main.rs:928](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/main.rs:928), [src/main.rs:1029](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/main.rs:1029); rustfmt check passes |
| Finding 2: 43 source Bead/milestone sites | fixed | source grep zero; metrics process count 0 ([scripts/quality_metrics.py:96](/home/tobias/Projects/bennett-workspace/bennett-circuits/scripts/quality_metrics.py:96)) |
| Finding 3: unavailable schedule/target launch | not fixed | explicit clause-cited errors remain at [src/main.rs:75](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/main.rs:75) / [src/main.rs:928](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/main.rs:928); pinned ISA §11.1 permits refusal of an unimplemented bound library, but no claim here that mechanics are complete |
| Finding 4: Debug-string worklist key | not fixed | [src/checker.rs:2396](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/checker.rs:2396) |
| Finding 5: 89 fallback-like matches | not fixed as inventory; no proven bug | still 89; sparse/optional cases inspected, no suppressed failure demonstrated |
| Finding 6: duplicated object/header setup | not fixed | [tests/classical.rs:6](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/classical.rs:6) / [tests/proof_output.rs:7](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:7) / [tests/placement.rs:14](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/placement.rs:14) |
| Finding 7: high clone density | not fixed | current counts 136 / 138 / 130; history extraction does not reduce ownership copying |
| Finding 8: tooling litter/config | partly | stale HANDOFF/PROGRESS retired; backup remains [.beads/hooks/pre-push.backup:1](/home/tobias/Projects/bennett-workspace/bennett-circuits/.beads/hooks/pre-push.backup:1); editor/agent configs are not inherently litter |
| Finding 9: lonely `version()` candidate | not fixed; premise disproved | [src/certificate.rs:726](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/certificate.rs:726) is a real production use, and `git show a698276:src/certificate.rs` contains it too |
| Finding 10: string-only errors and Bead-dependent assertions | partly | strings remain [src/lib.rs:44](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/lib.rs:44); process IDs removed and tests use clause/E_ diagnostics, e.g. [tests/static_checker.rs:921](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/static_checker.rs:921) |
| 1,157-line history evaluator; other hotspots | partly | evaluator 125, placement 264; six >300 remain with named owner at [docs/quality.md:88](/home/tobias/Projects/bennett-workspace/bennett-circuits/docs/quality.md:88) |
| Live sibling reads in eleven files; synthesis pin discipline | fixed | all readers use [scripts/pinned_sibling.py:19](/home/tobias/Projects/bennett-workspace/bennett-circuits/scripts/pinned_sibling.py:19) through Rust adapter; run-conformance also resolves the pin; full default suite succeeds from isolated scratch with explicit layout |
| QIR silent validator skip | fixed | [tests/exporters.rs:133](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/exporters.rs:133) panics on spawn error; missing-tool regression passed |
| QASM/Quil own-parser-only syntax validation | fixed for syntax | external parsers plus malformed controls at [scripts/validate_exporters.py:11](/home/tobias/Projects/bennett-workspace/bennett-circuits/scripts/validate_exporters.py:11); backend semantic independence remains a limit |
| Assertion-free tests / weak “does not error” tests | partly | inline/helper checks now cover all default test bodies; status-only assertions [tests/proof_output.rs:1096](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:1096) still add little beyond successful acceptance; lowering smoke checks [tests/lowering.rs:31](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/lowering.rs:31) remain weak |
| Trivial simulator witness / QASM fixed fixture count | not fixed | [tests/simulator.rs:38](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/simulator.rs:38) still one-qubit tolerances; [tests/qasm.rs:35](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/qasm.rs:35) still pins 18 actions, although independent corpus differential limits impact |
| Hard-coded “2 spec examples” | fixed | dynamic extraction and three-example witness [tests/differential.rs:35](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/differential.rs:35) |
| Memory-heavy default oracles / stale memory note | fixed structurally | ignores and separate gate step [tests/oracles.rs:14](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/oracles.rs:14) / [gate.toml:14](/home/tobias/Projects/bennett-workspace/bennett-circuits/gate.toml:14); README says ~7 GB [README.md:60](/home/tobias/Projects/bennett-workspace/bennett-circuits/README.md:60); current slow peak not remeasured |
| Independent simulator claim in baseline/synthesis | not fixed; assessment corrected | arithmetic is identical and simulator logic differs only in imports; independent reference execution remains real |

| Baseline recommendation | Status | Evidence |
|---|---|---|
| 1. QIR missing-tool failure + external QASM/Quil parser | fixed | all eight exporter tests passed; [tests/exporters.rs:133](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/exporters.rs:133) / [tests/exporters.rs:155](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/exporters.rs:155) |
| 2. Replace 14 assertion-free tests with meaningful assertions | partly | mechanical assertions added; proof-status-only acceptance cases remain weak ([tests/proof_output.rs:1096](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:1096), [src/object.rs:1921](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/object.rs:1921)) |
| 3. Format/split CLI | fixed | [src/main.rs:703](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/main.rs:703) / [src/main.rs:1029](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/main.rs:1029); rustfmt check exit 0 |
| 4. Split history, classical execute, checker schema | partly | history done; execute 536 and classical_schema 481 remain ([src/classical.rs:445](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/classical.rs:445) / [src/checker.rs:2379](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/checker.rs:2379)) |
| 5. Share object/header fixtures | not fixed | three constructors remain ([tests/classical.rs:6](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/classical.rs:6) / [tests/proof_output.rs:7](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:7) / [tests/placement.rs:14](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/placement.rs:14)) |
| 6. Remove Bead IDs from errors | fixed | 0 source identifiers; stable E_ and clause citations retained |
| 7. Correct memory docs, separate oracle gate, dynamic example count | fixed structurally | [README.md:60](/home/tobias/Projects/bennett-workspace/bennett-circuits/README.md:60) / [gate.toml:14](/home/tobias/Projects/bennett-workspace/bennett-circuits/gate.toml:14) / [tests/differential.rs:35](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/differential.rs:35); no heavy run in this audit |

Synthesis recommendations applicable here: pin discipline **fixed**; fast/slow split **fixed**; recorded measured coverage **fixed**; god-function reduction **partly**; zero litter **not fixed**. Attempt-end WIP ancestry is not a current red-main finding: default tests passed and the audited tip is a reviewed merge, not a WIP implementation tip. Review history is cited, not repeated: [main round 2](/home/tobias/Projects/bennett-workspace/bennett-circuits/docs/reviews/2026-11-06-circuits-main-r2.md:1), [pin review](/home/tobias/Projects/bennett-workspace/bennett-circuits/docs/reviews/2026-11-06-pin-circuits-r1.md:1), [quality final review](/home/tobias/Projects/bennett-workspace/bennett-circuits/docs/reviews/2026-11-07-quality-circuits-r3.md:1). Their historical findings were not duplicated as new defects.

## Plan targets

Applies the [programme Targets list](/home/tobias/Projects/bennett-workspace/bennett/docs/plan/2026-11-06-quality-floor-remediation.md:9) to this repository only. Commands use the measured runner/manifest above unless given in full.

| Target | Met? | Command + result / evidence |
|---|---|---|
| No red default main | met | default Cargo command: 210 passed, 0 failed; three declared ignores |
| No live sibling test reads | met | default Cargo command with explicit gate layout from isolated scratch; [scripts/pinned_sibling.py:19](/home/tobias/Projects/bennett-workspace/bennett-circuits/scripts/pinned_sibling.py:19) checks full ecaaac060c44e317d1181345fa6b8e38c096c099; 11 resolver tests passed |
| Measured coverage recorded in docs/quality.md | met | llvm-cov command: 85.15% lines, 77.83% functions; matches [docs/quality.md:40](/home/tobias/Projects/bennett-workspace/bennett-circuits/docs/quality.md:40) |
| Default test wall <180 s, slow retained in gate | met | 11.71 s warm; even cold compile + default run is 84.64 s; [gate.toml:14](/home/tobias/Projects/bennett-workspace/bennett-circuits/gate.toml:14) selects ignored slow tests |
| Audit test grade >=B | met | B+; 20-test random sample 18 useful / 2 weak; default independent CLI/syntax checks passed |
| Audit code grade >=B- | met | B-; six remaining semantic hotspots and ownership costs keep it below B |
| No >300-line semantics in correctness-fix files; remaining functions owned | met for this batch's scope | metrics scanner finds six, all listed with owner at [docs/quality.md:88](/home/tobias/Projects/bennett-workspace/bennett-circuits/docs/quality.md:88); split history/placement max 280/264; `git diff a698276 origin/main -- src/checker.rs src/classical.rs` shows diagnostic text changes, not new semantic P0/P1 fixes in those long handlers; not a claim all six are removed |
| Zero Bead/job identifiers in product source/output | met | `python3 -I /home/tobias/Projects/bennett-workspace/bennett-circuits/scripts/quality_metrics.py`: pass; identifier count 0; source Bead/milestone grep no matches |
| Zero tracked pycache/log/lock/backup/LAST-RUN litter | **not met** | `git -C /home/tobias/Projects/bennett-workspace/bennett-circuits ls-files` filtered by metrics LITTER regex returns exactly `.beads/hooks/pre-push.backup`; already owned by orchestrator, [docs/quality.md:123](/home/tobias/Projects/bennett-workspace/bennett-circuits/docs/quality.md:123) |

## Recommendations

1. Remove the tracked hook backup to satisfy the only failed literal Targets row ([.beads/hooks/pre-push.backup:1](/home/tobias/Projects/bennett-workspace/bennett-circuits/.beads/hooks/pre-push.backup:1)).
2. Continue the owned six-function reduction with semantic witnesses, starting with checker worklist/schema and classical execute ([docs/quality.md:88](/home/tobias/Projects/bennett-workspace/bennett-circuits/docs/quality.md:88), [src/checker.rs:2396](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/checker.rs:2396)).
3. Make tests for valid proof paths pair acceptance with an invalid neighbour or independent output; avoid counting a `proved` string assertion as new soundness evidence ([tests/proof_output.rs:1096](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:1096)).
4. Keep the reference CLI differential mandatory; identify the simulator/arithmetic twin as shared code and add independent literals/cross-checks when touching it ([tests/support/exact.rs:1](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/support/exact.rs:1), [tests/support/sim.rs:1](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/support/sim.rs:1)).
5. Extend CLI/linking/target malformed-input cases into the five weakest measured areas; preserve independent expected exit/verdict assertions ([src/main.rs:718](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/main.rs:718), [src/linking.rs:1](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/linking.rs:1), [src/target.rs:331](/home/tobias/Projects/bennett-workspace/bennett-circuits/src/target.rs:331)).
6. Centralise object-header/symbol test fixture construction; retain hand-derived expectations outside the helper ([tests/classical.rs:6](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/classical.rs:6), [tests/proof_output.rs:7](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/proof_output.rs:7), [tests/placement.rs:14](/home/tobias/Projects/bennett-workspace/bennett-circuits/tests/placement.rs:14)).
7. Re-measure the separate large oracle step in an orchestrator-owned slot, record time/peak and maintain external-parser cache preparation instructions ([gate.toml:14](/home/tobias/Projects/bennett-workspace/bennett-circuits/gate.toml:14), [README.md:60](/home/tobias/Projects/bennett-workspace/bennett-circuits/README.md:60)).

JOB-COMPLETE
