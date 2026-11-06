# bennett-targets quality audit 2026-11-05

Scope: `targets/` (data), `validator/` (Rust), `importers/` (fixtures + README). No cargo was run (brief pass
restriction for this audit); all test and build numbers below are static counts, not measurements. Git HEAD read at audit time.

## Verdict
- Code: **B.** Validator is tidy and spec-cited; fail-fast is the norm. A few `unwrap()` on input-derived JSON and one loud-but-misleading `unwrap_or(0)`.
- Tests: **B-.** 49 tests, none ignored, several are oracle-backed (ISA conformance cases, published witnesses, exact rationals) and two are regression tests for the 2026-11-03 P0s. Negative tests exist. Weak spots: provenance check and importer tests.
- Target data provenance: **C+.** Numbers are explicitly "illustrative", and the sidecars match the JSON (checked by hand, not by a test), but nothing is sourced and the sidecars cite the wrong ISA version on 3 of 4 files.
- Importers vs external formats: **D.** No fixture is a real Qualtran or Azure output; all are hand-written. Field mapping is tested against the author's own reading of the docs.
- Build: not measured (cargo excluded). Dependency surface is small (28 packages in Cargo.lock; 6 direct deps).

## Composition
cloc on `git ls-files` (tracked, excluding `.beads/`; 49 files): Rust 20 files / 3,651 code lines (validator src 2,182
+ tests 1,629 raw lines); Markdown 14 files / 737; JSON 9 files / 428 (4 targets, 4 fixtures, 1 lock-like); Python 1 file
/ 315 (`scripts/verify.py`); TOML 3 files; shell 2 files. A cloc run on the working tree is polluted by untracked `.tmp/`
and `validator/target/`, so these tracked numbers are the ones to use. 31 commits on HEAD.

Module map (validator/src):
- `target.rs` 490 - schema, load, canonical-bytes check (§8.1), `native()` leaf matching.
- `runtime.rs` 392 - `expand`, `aggregate` (§8.2/§8.4), import quantity conversion.
- `expr.rs` 222 - exact rational expression evaluator and decimal parser.
- `model.rs` 299 - unitary models for native ops (ideal matrices, `ideal()` at model.rs:118).
- `topology.rs` 188 - §8.3 adjacency, default placement, vertex limits.
- `importers.rs` 316 - `qualtran()` and `azure()` adapters.
- `json.rs` 150 - parser and RFC 8785 canonicaliser. `query.rs` 46 and `main.rs` 61 are the CLI surface.

Authorship (`git log`, 31 commits): 1 human author on every commit. 23/31 (74%) carry `Co-Authored-By: Claude`.
1 commit is a `wip(codex job` checkpoint (3%). No `Agent: gpt` trailers.

## Build and test times
| Step | Result |
|---|---|
| warm incremental build (touch one file) | not measured (cargo excluded by brief for this pass) |
| `cargo test --no-run` | not measured |
| test run | not run; static count below |
| `#[test]` functions | 49 in `validator/tests/*.rs`; 0 in `validator/src` (no unit tests) |
| ignored / skipped | 0 `#[ignore]`. By design, 21 of 38 ISA suite-E cases are "published unavailable" (HANDOFF.md, "Suite E: 17 executed, 21 published unavailable"); `suite_e.rs:249` asserts each has a reason and a bead |
| red | none marked red. The 2026-11-03 review (docs/reviews/2026-11-03-targets-batch.md) recorded 6 failing probes; they were turned into `review_round2.rs` regression tests (5 tests) that the current HEAD should pass. Not verified by running |
| gate | `gate.toml` runs fmt, clippy -D warnings, test, build, verify.py. Not run |

## Coverage
Not measured (no llvm-cov run; cargo excluded). Structural estimate:
- Every src module is reached by at least one test file (importers, expr, topology, runtime, target, model, json, canonical through the test binaries).
- Five largest untested or weakly tested areas:
  1. Azure Majorana path: one test (`importers.rs:142`) plus one rejection test (`importers.rs:187`). `importers.rs` 316 lines, `azure()` at 239 is 78 lines.
  2. Qualtran adapter: one happy-path test and four rejections (`importers.rs:10`). Fractional/negative are tested; symbolic values and the 7-field mapping are not tested against a real GateCounts dump.
  3. `runtime.rs:200` `aggregate()` (193 lines): tested by one fixture (`runtime.rs:85`, events.json) and one capacity case. No property or differential test.
  4. `model.rs:118` `ideal()` (175-line matrix table): exercised only for the 3-wire ccx scheme (`models.rs:66`). Single-qubit and cz/swap matrices get no direct check beyond that.
  5. `query.rs` (46 lines): no direct test; reached only through the `query` helper in `cli.rs:63`.

## Test quality
Sampled 20 tests, chosen by hand across all 10 test files (not random; file:line given):

| # | Test | Class | Why |
|---|---|---|---|
| 1 | models.rs:3 models_are_canonical_and_have_provenance | weak | Only checks that sidecar text contains "illustrative". Never checks a number against JSON |
| 2 | models.rs:66 grid_2d_ccx_scheme_is_toffoli_and_respects_adjacency | strong | Exhaustive 8-basis unitary against textbook Toffoli; own simulator, independent oracle |
| 3 | importers.rs:10 qualtran_all_fields_and_unknowns | useful | Inline inputs, 4 rejections; but only 7 synthetic fields |
| 4 | importers.rs:72 importer_rejects_unit_mismatch_and_preserves_huge_counts | useful | Huge-count round-trip is good; `contains("unit")` is loose |
| 5 | importers.rs:100 azure_nonzero_rates_are_named_resources_never_epsilon | useful | Checks own mapping against hand-written expectations; no external sample |
| 6 | contract.rs:3 schema_and_canonical_red | useful | Negative: `{}`, `[]`, duplicate key. Trivial inputs |
| 7 | contract.rs:29 optional_params_is_an_array_when_present | weak | One mutation (null params) |
| 8 | canonical.rs:60 validate_requires_exact_canonical_bytes | strong | Trailing LF rejected per §8.1, against ISA conformance bytes |
| 9 | cli.rs:6 cli_canonicalizes_all_seven_fixtures... | strong | Oracle: ISA conformance cases in sibling repo (needs bennett-isa-spec checked out) |
| 10 | suite_e.rs:19 all_seventeen_published_e_scenarios | strong | Published scenarios; 21 are skipped by design |
| 11 | target09.rs:34 eps_decade_published_witness | strong | Published witness table, exact rationals |
| 12 | target09.rs:99 eps_decade_cost_charges_requested_share_not_achieved_epsilon | strong | Distinguishes requested from achieved epsilon, a spec rule |
| 13 | target09.rs:206 adjacency_is_the_published_outcome | useful | Pins error-code strings (`E_SCHEDULE_INFEASIBLE`, "§17 item 15"): brittle to wording |
| 14 | target09.rs:222 every_operand_pair_needs_an_edge | weak | Asserts the error contains "0" and "3". Almost any message with digits passes |
| 15 | runtime.rs:85 event_aggregation_and_capacity | useful | Hand-computed sums from events.json; expectations are hand arithmetic, not a reference run |
| 16 | runtime.rs:114 imported_quantity_conversion | weak | 3 x 2 = 6; trivial input, tests a multiplication |
| 17 | runtime.rs:13 matching_and_actual_bindings | weak | Same expectation for eps in {0, 0.001, 1}; the eps-dependence is not really asserted |
| 18 | expressions.rs:7 exact_arithmetic_contexts_and_failures | useful | 123456789...125 x 8 exact; 0.1+0.2=0.3; 5 malformed exprs rejected |
| 19 | review_round2.rs:25 imported_rates_are_preserved_exactly_or_rejected | strong | Regression for P0 b-targets-c5w (0.10000000000000001 changing on serialisation) |
| 20 | review_round2.rs:201 malformed_decimal_text_rejects | strong | 15 malformed decimals, 5 good forms with exact values |

Totals: strong/oracle 8 (40%), useful 7 (35%), weak 5 (25%), tautological 0. No test duplicates the implementation's arithmetic.
Oracle-backed: ISA conformance cases (sibling `bennett-isa-spec`), published witnesses, and exact rationals. The gate
(`gate.toml`) would catch a wrong canonical hash or a wrong eps_decade value, because those are in the tests. It would not
catch a wrong Azure or Qualtran mapping, because no external sample exists to compare against.

## Target data and provenance
- Checked by hand: `superconducting-grid-2d-illustrative.json` differs from `superconducting-grid-illustrative.json` only in `topology`, as its sidecar claims. Classes match the sidecar table (data 16/1/0.5, buffer 4/0.25/0.25). Timings match (6 x two-wire = ccx 0.0012).
- Not automated: the only check is `models.rs:3` (the word "illustrative" is present). A sidecar number can drift from the JSON without any failure.
- ISA version drift: `ideal-all-to-all.provenance.md:6`, `superconducting-grid-illustrative.provenance.md:6`, `trapped-ion-illustrative.provenance.md:6` say "ISA 0.8 §8 defines all field semantics". `superconducting-grid-2d-illustrative.provenance.md:7` says 0.9. HANDOFF and README say the validator implements 0.9.
- No value has an external source. The README says "illustrative"; that is honest. The sidecars cover `classes`, `gates`, `max_parallel`, and `measurement`, but not the `objective`, `imports` or `resources` blocks (not verified; checked only by reading).
- Tracked runtime litter: `.beads/backup/*.darc` (10 files), `.beads/backup.lock`, `.beads/backup/LOCK`, `.beads/embeddeddolt/.lock`, `.beads.gate.lock`, `.beads/embeddeddolt.gate.lock`, and `.beads/embeddeddolt/b_targets/.dolt/noms/LOCK` are tracked (`git ls-files`). Lock files do not belong in git.

## Importers and external formats
- Fixtures are not samples of real output. `importers/fixtures/azure-*.json` are named "illustrative-*" and carry round numbers. `qualtran-gate-counts.json` is `{"t":1,"toffoli":2,...}`. The importers README cites Qualtran's `GateCounts.asdict()` and the Azure estimator docs ("accessed 2026-10-30"), but no test compares against an actual dump from either tool.
- Of the 4 fixtures, only `azure-qubit-params.json` is read (`tests/importers.rs:85`). `azure-majorana.json`, `azure-nonzero-error.json` and `qualtran-gate-counts.json` are referenced by no test or script: dead data. Most importer tests use inline JSON.
- Silent defaults (by design, and reported): `importers.rs:81` treats missing Qualtran fields as zero and marks them `defaulted` in the mapping report. Acceptable, but no test asserts the report marks each default.
- Azure defaults (`tGateErrorRate` defaults to `oneQubitGateErrorRate`, etc.) are reported in `mapping` (`importers.rs:100` checks one).

## Code quality
Checked against policy rule 9 and fail-fast:
- `runtime.rs:355`: `limits.get(cls).copied().unwrap_or(0)`. A class missing from `vertex_limits` gets 0 vertices, so any live wire errors with "exceed its 0 vertices". Loud, but the message is wrong when the class is simply unknown. Failure cost: misleading diagnostic.
- `runtime.rs:93` and `:150`: `s["ancillae"]["class"].as_str().unwrap()` and `g["gate"].as_str().unwrap()` panic on input-derived JSON if the schema check does not cover those fields. Whether `target.rs:88` `schema()` covers them was not verified. Failure cost: panic instead of a validation error.
- `model.rs:43-44`: `parse().unwrap()` after a canonical-decimal check at `:40`. Probably safe; flagged for review only.
- `importers.rs:280-301`: `unwrap()` on self-built JSON. Acceptable.
- Bead references in source (rule 9): `model.rs:18` ("b-targets-1wr"), `model.rs:4` ("b-isa-spec-wk0k"). `runtime.rs` and `importers.rs` carry none. Tests carry more (doc comments in `review_round2.rs` cite b-targets-9oc and 4z8). Cost: comments rot once beads close.
- Long functions: `target.rs:88` `schema()` 226 lines; `runtime.rs:200` `aggregate()` 193; `runtime.rs:46` `expand()` 131; `json.rs:5` `parse()` 107; `target.rs:378` `native()` 101. Hot spots for review.
- `target.rs:388` `#[allow(clippy::too_many_arguments)]` on `native()` (101 lines). A lint suppression on a long
  multi-argument function is a signal that the arguments want a struct. Failure cost: call sites take unnamed positional
  arguments (tests pass `1, 1, expr::decimal(...)` positionally, e.g. `runtime.rs:13`).
- Not scanned in this pass: nesting depth, duplication and trivial-wrapper counts for the Rust sources (the AST metrics
  were run on bennett `tools/` only).
- No `#[ignore]` in the tree.

## What is good
1. Exact rational arithmetic with explicit failure on any non-canonical decimal (`expr.rs`, `review_round2.rs:201`). Numbers never round silently.
2. Import rules say "preserved exactly or rejected" and are tested (`review_round2.rs:25`). The review's P0 became a regression test.
3. Errors cite spec sections (§8.1, §8.3, §8.4), so a failure can be traced to the rule it breaks.
4. Epsilon is never silently taken from an import (`importers.rs:100`), and the mapping report records every default.
5. The ISA conformance cases are consumed directly (`cli.rs:6`, `suite_e.rs:19`) rather than copied, so the validator is checked against the spec's own vectors.

## Recommendations
1. Make `models_are_canonical_and_have_provenance` parse each sidecar table and assert that every JSON number appears in it (cheap; catches drift).
2. Replace the 3 ISA "0.8" references in the sidecars with 0.9 (or state the version each value was derived from).
3. Add one real sample per importer (Qualtran `GateCounts.asdict()` dump, Azure estimator output) with source URL and retrieval date; test against it.
4. Tighten `target09.rs:222` and `importers.rs:72` to assert on the offending field name rather than a digit or the word "unit".
5. Change `runtime.rs:355` to error with "class X has no declared vertex limit" when the key is missing.
6. Replace `runtime.rs:93,150` unwraps with `ok_or` errors, or document that the schema guarantees them.
7. Untrack `.beads/**/LOCK`, `*.lock` and `backup/*.darc` (keep `.beads/issues.jsonl`); add to `.gitignore`.
