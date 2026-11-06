# bennett-dialect-spec quality audit 2026-11-05 (tooling only)

## Verdict
- Code: C+. Working but monolithic Python (dialect_check.py 3125 lines, functions up to 295 lines), progressive monkey-patching of modules, and the "validator/" Rust crate is an 11-line stub.
- Tests: B-. 84 + ~60 unit tests have hand-written expectations and mutation-style negative cases; the headline "2943 checks" is ~80% bookkeeping (xref, parse, coverage), only ~470 are semantic.
- Build/gate: C. No build; the v02 gate takes 572 s on a loaded machine, unit tests 177 s; neither is runnable without sibling repos, clang/opt 18/20/23, and a Rust ISA interpreter build.
- Biggest finding: expected labels are spec-prose annotations, so the gate checks "spec text agrees with checker", not "checker agrees with an independent oracle", except for ISA-interpreter-backed families (~70 checks).

## Composition
Scope: tooling. reference-interpreter/ is an EMPTY directory (the interpreter lives in ../bennett-isa-spec/reference-interpreter and is built into scripts/.isa-ref snapshots by the checker). No cargo/Rust code to speak of. `validator/` = Cargo.toml (no deps) + src/lib.rs (11 lines: `version()` plus a test asserting it returns "0.0.0"). The actual "validator" is Python: `Analysis02`, `validate()` in scripts/dialect_check_v02.py:330-466 over dialect_flow.py.

| Path | Lang | Files tracked | Lines |
|---|---|---|---|
| scripts/*.py (checker, 54 tracked files incl. .c/.json) | Python | ~45 | 10799 (incl. tests) |
| scripts/dialect_check.py (0.1 base) | Python | 1 | 3125 |
| scripts/dialect_flow.py / normalise / map / check_v02 | Python | 4 | 920 / 692 / 489 / 891 |
| scripts/test_*.py | Python | 6 | ~1035 in test_dialect_check.py + 4 small |
| tools/ (v03 pre-flight via import-hook patching) | Python+JSON | 8 | ~ 0.3 kLOC |
| corpus/legality/harness/run.py + 8 test files | Python | 9 | run.py 2079 |
| corpus/legality/cases | .ll (55) / .c (7) | 63 | - |
| emission/ (checked-in generated IR for c/cpp/julia/rust) | .ll etc. | 112 | 15643 |
| spec/*.md (not audited) | md | 35 | 29901 |
| validator/ | Rust | 3 | 11 |

Dependencies: Cargo.lock 1 crate (self); Python stdlib only; external tools clang/opt/llc 18,20,23, rustc, julia, and cargo (to build the sibling ISA interpreter).
Authorship: 190 commits, all author `tobiasosborne` (git cannot separate agent from human); 15 commit-message lines mention Agent:/codex. Treat as nearly entirely agent-authored (tool-heavy, round2..round8 naming).
Tracked litter: scripts/dialect_check.LAST-RUN.json, scripts/dialect_check.PROGRESS.md, spec/*.PROGRESS.md (3), .agents/.codex/.cursor/.claude dirs, .beads (11). `__pycache__` present on disk (untracked, fine).

## Build and test times
Cache: scripts/.isa-ref snapshots were warm; machine load average was 17 (other auditors), so times are inflated.

| Step | Wall | Result |
|---|---|---|
| `python3 scripts/dialect_check_v02.py --json` (CARGO_BUILD_JOBS=3) | 572 s (just under timeout 600) | OK 2943/2943, 0 failed, 0 blocked |
| `python3 -m unittest test_dialect_check` (scripts/) | 177 s | 84 tests OK |
| `cargo test` validator | 0.23 s | 1 test (asserts version string) |
| Not run: tools/dialect_check_v03.py, corpus harness tests (cross-compile LLVM 18/20/23 matrix), test_dialect_021x | skipped, budget | - |
Test counts (def test_): test_dialect_check 84, 0211:8, 0212:4, 0213:8, 0214:7, snapshot:1, tools:3, harness 50 (checks 16, fixes_v3 21, runtime 7, others 6). Ignored/red: none found (grep for skip/xfail gave none in what I read). Note the brief says 2944 cases; the live run says 2943.

## What a "case passing" checks (the 2943)
Per-family counts from the run; checks are built from the spec's fenced blocks (spec/Bennett-Dialect-Spec.md, 1036 fence lines, 155 `llvm example`, 46 normalise pairs, ...). They are NOT corpus/legality/cases (63 files, separately harnessed).

| Family | n | What passing means | Oracle |
|---|---|---|---|
| xrefs | 1459 | each "§N" cross-reference in the prose resolves (dialect_meta.xrefs, v02:610) | structural; bookkeeping |
| parse | 809 | `opt -passes=verify` accepts the block on LLVM 18/20/23 (v02:476) | LLVM (independent), but only "it parses" |
| coverage | 203 | each normative rule has >=1 example (`equal(r,'P-1',True,ok)`, v02:615) | bookkeeping |
| recognise | 155 | Python recogniser verdict == `verdict=` attribute in spec (v02:491-504); optional candidate/callee/shape sets | hand/LLM-written label in prose vs checker; not independent |
| state | 86 | JSON scenario run by dialect_driver/round8 vs expected in block | semi-independent |
| normalise | 46 | Python `normalise()` output == `normalise-out` block text (collapsed), then validator accepts, then opt verify; v02:560 | expected text is in spec; the spec text was written to match the normaliser (or vice versa), self-referential unless authored first |
| native, frontend, cc-run, run-program | 65 | compile+run C/Rust/Julia against native driver; check trace/exit | real execution, independent |
| run-oracle, step-check, check, hash | 59 | ISA reference interpreter (Rust, sibling) executes object; compare to numbers in spec | independent oracle, except hash |
| blocker | 19 | verdict + BLK code present | label vs checker |
Labels are hand/agent-written in the spec; they are not generated by the validator at run time. However tools/dialect03_rehash.py:5-30 rewrites the spec's `interface_hash` values FROM the reference interpreter, and then the `hash` family (9) checks the interpreter against them: circular by construction (the stated "P-3" design; still catches later drift).
Effective independent semantic checks: roughly 65 (execution) + 59 (ISA oracle) + 155 (recognise, label-based) + 46 + 86 ~ 410-470; the other ~2470 are structural.

## Coverage
No coverage tool run (Python tooling; no coverage.py wired). Structural estimate: the 3125-line base checker is exercised end-to-end by the gate but branch-level coverage is unknown. Rust validator: 1 of 1 function covered, but it is a stub. Weakest areas:
1. validator/src/lib.rs: no validator exists in Rust; README/CLAUDE.md describe a "residual-poison validator" (unverified claim, the Python Analysis02 is it).
2. corpus/legality/harness/run.py (2079 lines, `report` 295 lines at :1713): matrix reporting only tested through 50 harness unit tests on helpers; the 170k-cell matrix is not re-run by any gate.
3. emission/ (112 checked-in generated files): consumed by no test that I found (SUMMARY.md only); freshness unchecked.
4. scripts/dialect_check.py `legacy_main` (:2830, 251 lines) and 0.1 paths kept for 0.2/0.3 import-hook patching; legacy paths appear unreachable from the v02 gate.
5. tools/dialect_check_v03.py: 3 unit tests of patch mechanics only; the v03 gate itself was not run here.

## Test quality (sampled)
| Test | Class | Why |
|---|---|---|
| test_dialect_check.py:715 test_wrong_verdict_is_a_failure | useful | proves mismatch raises and verdict is reject:BD-E-OPERAND (negative control) |
| :87 test_round8_bitcast_arithmetic | useful | hand-computed 257 result of insertelement/bitcast |
| :100 test_round8_bitcast_transfer | useful | explicit enumerated value sets, both byteorders |
| :20 test_round8_zero_execution | useful | mutates widths and asserts failure |
| :779 test_blockers_are_distinct_from_rejections | useful (not read fully) | distinctness assertion |
| :1022 test_handle_comparison_is_identity_only | useful | tiny single-case, checks one reject code |
| :727 test_unknown_effect_does_not_crash | weak | name says "does not crash", asserts verdict from spec attribute with conditional block lookup |
| :735 test_first_region_candidates | useful | exact set + negative v.equal |
| test_dialect_0213.py:19 test_full_version_guard | useful | accepts 0.2.14, rejects five older tokens |
| :29 test_publication_and_matching_contract | weak | checks spec against checker contract; spec-derived |
| :35 test_old_tie_rule_is_detected | useful | mutates spec text, expects failure |
| tools/test_dialect_v03.py:8 test_exact_hit_count_is_enforced | useful | positive+two negatives |
| :13 test_every_listed_module_exists_and_patches_apply | weak | only asserts text changed |
| :20 test_blocker_verdicts_map_to_isa09_rows | tautological | asserts a constant equals an identical literal |
| validator/src/lib.rs:7 version_is_draft | tautological | asserts CARGO_PKG_VERSION == "0.0.0" |
| harness/test_fixes_v3.py:96 canonicalize_resolves_unresolved | useful | hand traces in/out |
| :102 canonicalize_rejects_unexpected_raw_spelling | useful | fail-loud negative |
| :106 l4_alias_set_needs_a_definition | useful | positive and negative |
| :114 internal_region_resolves... | useful (integration) | real compile + assertIn on trace text; assertIn is loose |
| harness/test_checks.py:12 declaration_group_forbidden | useful | exact attribute sets |
| harness/test_seeds.py:6 all_seeds_keep_trace_through_o3 | useful | real opt O3 on 3 LLVM majors, trace compare |
Ratio of the 21 sampled: 16 useful, 3 weak, 2 tautological. The unit tests are the strongest layer: expected values are written by hand, with negative controls. Weakness: the same author (an agent) wrote spec label, checker and test; a shared misreading of the spec passes everywhere. The only independent ground truth is LLVM (opt/verify, native runs) and the ISA Rust interpreter.
Would the gate catch a wrong result? Yes for a checker regression or spec edit (labels pinned). No for a wrong label that the checker was tuned to agree with (e.g. `recognise` verdicts at 155 examples and the normalise pairs); no for the 1459 xrefs beyond "target exists". gate.toml runs cargo test (trivial) + dialect_check_v02 only; it does not run the v03 gate, the 84 unit tests, or the harness tests. So the 144 unit tests are not in the push gate.

## Code quality
1. Silent-ish catch-all in the check loop: scripts/dialect_check_v02.py:482-486 catches (Fail, Reject, OSError, ValueError, KeyError, IndexError, TypeError, AttributeError) and records the row as `failed`. It does not hide failure (the row is counted and exit code is 1), but it merges checker bugs (KeyError) with contract violations; cost: debugging by detail string.
2. Import-hook / regex-patching of frozen modules (tools/dialect03_patches.py, `sys.modules.setdefault("dialect_check_v02", ...)` at v02:34): v03 is "v02 with edited source text"; hit counts catch drift but the pattern is fragile and reads as technical debt. Version token in 0.3 gate depends on string replacement.
3. Lonely interface: validator/src/lib.rs `version()` (policy rule 9). The crate is wired into gate.toml "cargo test (every crate)".
4. Bead references in source: scripts/dialect_check_v02.py:37 (`CLI_BEAD = 'b-isa-spec-xam'`), :615, :621, :674, :729 (8 matches across scripts and tools). They are used as runtime strings in "Unavailable" reports; policy says no bead refs in source.
5. `Unavailable` exits as `blocked`, which is counted as failure; good. But `check` still turns "bug in checker" into 'failed' with a generic message.
6. Functions >100 lines: run.py:1713 report (295), dialect_check.py:2830 legacy_main (251), :2108 lift (230), dialect_map.py:209 lproc (219), dialect_check.py:1287 prov_step (168), round3 check_state (159), round2 check_state (156, near-duplicate name/role with round3), :1787 normalise (156), dialect_native.py:30 cases (134), run.py:1093 evaluate (133). 722 functions total.
7. Naming/structure debt: dialect_round2..round8, dialect_0211..0214: files named after work sessions, not concepts. dialect_round2.check_state and dialect_round3.check_state duplicate.
8. Dense unformatted style: semicolon-chained statements and no spacing (`rows.append(row)`, `d.MARKERS.clear();...`), and a `run()` that is a 70-line chain of ifs (v02:617-660, tag-by-tag dispatch), making reviewing hard.
9. Tracked WIP: scripts/dialect_check.LAST-RUN.json, scripts/dialect_check.PROGRESS.md, three spec/*.PROGRESS.md; emission/ generated IR (15.6k lines) checked in.
10. reference-interpreter/ empty dir tracked/exists in the tree; the gate refers to sibling repo at pinned SHA (gate.toml), and checker reads ../bennett-isa-spec directly: a build-time cross-repo coupling, contradicting CLAUDE.md rule 5 ("coupled only through published specs"), though via a binary rather than shared code.

## What is good
- Fail-loud design: every "unsupported" tag becomes a counted `blocked` row; exit code non-zero on any blocked (v02:482, 700-716). No family can vanish silently (v02:662 registry).
- Real executors where it matters: opt verify on three LLVM majors, native build+run with fault probes, and a Rust ISA interpreter pinned by SHA-256 (v02 header, PinnedExecutable).
- Negative controls in unit tests (mutate input, assert Fail) at test_dialect_check.py:20, :715, test_dialect_0213.py:35.
- Rule 11 enforced in code: command() refuses `-view-*` passes (v02:103-110) and strips DISPLAY etc.
- Gate output records interpreter commit and SHA, source file hashes (dialect_check.LAST-RUN.json), so results are reproducible.

## Recommendations
1. Add the 144 unit tests (scripts, tools, harness) to gate.toml; today the push gate runs only the spec-example run.
2. Delete or fill validator/ (stub crate with a tautological test); if Python is the validator, say so in README.
3. Add independent labels: differential-test the recognise verdicts against a second implementation or the corpus/legality execution results, so spec labels are not the only oracle.
4. Split dialect_check.py (3125 lines) and rename roundN/021x files by concept; remove legacy_main if unreachable.
5. Stop `dialect03_rehash.py` from rewriting expected hashes in place, or add a hand-pinned subset of hashes as a non-circular anchor.
6. Replace bead strings in source with codes; drop tracked LAST-RUN/PROGRESS files (or move to .tmp).
7. Report xrefs/parse/coverage separately from semantic checks so "2943/2943" is not read as 2943 semantic passes.
