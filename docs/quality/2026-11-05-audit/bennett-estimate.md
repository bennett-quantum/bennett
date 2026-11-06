# bennett-estimate quality audit 2026-11-05

## Verdict
- Code: C+. Correctness-minded and fail-loud at the edges, but 4742 lines in one Python file with a 1630-line class and 250-460-line functions.
- Tests: B. 216 tests, all green, none ignored. Many assert hand-derived literals and one differential runs against the VM. The differential is narrow, and the gate would catch a wrong result in only a few areas.
- Build: A, but nearly meaningless. The "Rust" crate is a 56-line launcher that pipes Python to `python3 -I -`. Real cost is test time (3-4 min).
- Coverage could not be measured (no Python `coverage`; cargo-llvm-cov only sees 56 Rust lines). The structural estimate is below.
- Key answer: estimates ARE checked against independent values. See "Test quality".

## Composition
cloc excludes `target`, `.tmp` and `.git`. Tracked files: 87.

| Language | files | code LOC |
|---|---|---|
| Python | 6 | 7149 (src/estimate.py 4742, tests 3006 incl. runner) |
| Markdown | 13 | 1145 |
| Bourne/Bash shell | 9 | 272 |
| JSON | 11 | 143 (data/ref-0.9.json catalog, 11 files total) |
| TOML/YAML | 6 | 69 |
| Rust | 3 | 56 (src/lib.rs 21, src/main.rs 9, tests/python.rs 32) |

Module map. The estimator is one file, `/home/tobias/Projects/bennett-workspace/bennett-estimate/src/estimate.py`. The line ranges below are from `ast` class extents and the review's section map.

| Piece | LOC | Purpose |
|---|---|---|
| numbers/JCS/expressions/Profile (:1-315) | ~315 | exact rational numbers, canonical JSON, resource algebra |
| Target (:315) | 228 | target description reader/matcher |
| Catalog (:739) | 630 | recipe binding and dispatch from ref-0.9.json |
| Object (:1522) | 448 | `.bisa` reader, identity hashes |
| Schedule (:2023) | 179 | schedule certificate reader |
| Ledger (:2204) | 285 | resource accounting |
| Source (:2538) | 1630 | oracle/classical/action construction |
| Certificate + `estimate` + CLI (:4170-4742) | ~570 | certificate read/check/produce, entry point |
| src/lib.rs, main.rs | 30 | `run()` spawns `python3 -I -`, stdin = catalog + estimate.py |

- Dependencies: Cargo.lock lists 1 crate (self). Rust deps: none. Python: stdlib only. `python3` is a hard runtime requirement, so the Rust shell adds nothing except `include_str!` packaging.
- Siblings read at test time: `bennett-targets`, `bennett-isa-spec`, `bennett-conformance` and the `bennett-vm` binary. They are resolved via `ROOT.parent`.
- Authorship, 55 commits: 35 `wip(codex job ...)` (64%, all by the one git user), 20 other (36%, Claude-written beads, reviews, worklogs). Zero commits carry an `Agent: gpt-*` trailer. The review (docs/reviews/2026-11-03-estimate-batch.md) notes the same.

## Build and test times
The existing `target/` (15 MB) was NOT used. I built into `.tmp/audit-target`, so it is cold for this repo.

| Step | Wall | Note |
|---|---|---|
| Cold `cargo build -j3` | 1.14 s | no dependencies, one tiny crate |
| Warm build after `touch src/lib.rs` | 0.46 s | |
| `cargo test --no-run -j3` | 0.90 s | |
| `cargo test -j3 -- --test-threads=4` (full) | 178 s | run 1 of 2 |

Caveat on the 178 s figure: my first full `cargo test` was backgrounded and still running when I started a second one. The two overlapped for part of the time. The 178 s run was the second; the first took 259 s under contention. Treat roughly 3 min as a standalone estimate, not a clean measurement.

- Four parallel groups, wall per group: objects 75 tests/122 s, accounting 123 tests/176 s, selectors 16 tests/97 s, other 2 tests/0.07 s. So tests dominate; the cargo layer is nothing.
- 216 Python tests (test_schedule 139, test_estimate 75, test_gate 2) plus 4 Rust wrappers. All 216 pass. Ignored: 0. Skipped: 0. Red: 0.
- `scripts/check` also runs `cargo fmt --check` and clippy; I did not run them (only rustfmt-able lines are the 56-line shell).

## Coverage
Not measured. There is no `coverage` module for Python, and `cargo llvm-cov` would report only 56 Rust lines, which is meaningless here. This is a structural estimate, and it is an estimate.

- Method: grep and read test names against class extents in estimate.py.
- Schedule, Ledger, Catalog.recipe, Target, JCS/decimal_up and the summary-vs-ledger paths are hit by named tests (75 + 139 test names map onto them).
- The five weakest or least-evidenced areas:
  1. `Source.classical` (:3272-3733, 461 lines, 24 nesting levels counted by ast, containing nested dataclasses). The Opus review skimmed it, "Skimmed or not read: `Source.classical` (3139-3600)". Its branch fan-out (`budget.mint`, `qreg.new`, ...) cannot all be covered by 216 tests; no per-op test list exists.
  2. `Source.execute` (:3395-3729, 334 lines) and `action_nodes` (:3864-4168, 304 lines). The review skimmed both. A sampled test (`test_while_summary_counts_scheme_workspace_borrow_and_accuracy`) reaches only part of the control forms.
  3. `Object.read`/`identities` (:1522-1972). Trusted to the §16.3 hash tests, which are few.
  4. The CLI error paths and exit codes (:4720-4742). One `except (ContractError,OSError,...)` handler maps errors to exit codes, and the only test is `test_deterministic_and_failure` (one bad-params case). The review found `--budget` omitted silently estimates B=0 (nit 4).
  5. `oracle_stream`/`oracle_state` and table/global-delivery summaries (:980-1100). Skimmed by the review. Tests exist (`test_global_delivery_summary_matches_literal_mixed_groups_and_inverse`) but are literal-vs-summary only.
- Dead-code scan: no unreferenced top-level class found. I did not run vulture.

## Test quality
Key question: are estimates checked against hand-derived or external values?
Answer: yes, in three ways, and one weakness.

- **Hand-derived literal expectations.** About 132 `assertEqual` lines compare against hard-coded string values (resource rows such as `"gate_count":"7","time":"7","peak_qubits[data]":"4","qubit_second[data]":"26"`). Spec-derived values include the §10.1 decimal_up witnesses, the catalog hash `5de4e49...` and 219 recipes. These are oracle-backed unless the literals were copied from the estimator's output; I cannot tell which, and the commit history does not record where the numbers came from.
- **External differential.** `scripts/differential.py:10-` runs the real `bennett-vm` binary (`run-cc`, `run-program`, `run-oracle`) and compares steps, time and gate count with the estimator. It covers the rung-3 `sum` fixture for n in {0,1,3,7,255}, three fault rows, two history rows and one native action pair. It is an independent implementation, so it is the strongest check in the repo. It covers about 10 fixtures, all classical-step or native-pair, not the quantum resource accounting at large.
- **Weakness.** The summary path versus the ledger path are two code paths of the same estimator, compared with each other by the review's ad hoc probe. That is self-consistency, not an oracle.
- Property-based or exhaustive tests: none. No fuzzing; no randomised domains.
- test_gate.py is repo plumbing (checks gate.toml shape and pre-push text), not estimator semantics.

Sampled tests (21):

| # | test | verdict | why |
|---|---|---|---|
| 1 | test_estimate.py:33 jcs large integer/UTF-16 order | useful | exact literals, specific edge cases |
| 2 | test_estimate.py:~39 test_upward_34 | useful | spec witness values `0.33..34`, 10^40 boundary |
| 3 | test_estimate.py:~47 expression_epsilon_decades | useful | boundary table, also error cases |
| 4 | test_estimate.py:250 implicit_length_width_changes_exact_cost | weak | only `assertGreater` between two runs, no numeric value |
| 5 | test_estimate.py:~338 large_stack_summary_does_not_scan_cells | weak | checks it runs fast, not the value |
| 6 | test_estimate.py:130 global_delivery_summary_matches_literal | self-referential | compares the summary algorithm with the literal algorithm of the same file |
| 7 | test_estimate.py:~272 published_identity | useful | pinned catalog hash and recipe count |
| 8 | test_estimate.py:~275 k82_named_interfaces | useful | negative tests plus `time==1` |
| 9 | test_estimate.py:872 vm_admits_contract_witnesses | useful | external VM computes `(x+arg)%2` for all four inputs |
| 10 | test_estimate.py:~883 deterministic_and_failure | weak | only run-twice equality plus `gate_count=="4"` for one fixture |
| 11 | test_estimate.py:~896 differential_rung3 | useful | VM-backed, but 23 asserted constants only partly cross-checked |
| 12 | test_schedule.py:74 decimal_string_entry_positions | weak | no assertion, only "does not raise" |
| 13 | test_schedule.py:~100 captured_record_arrays_reuse_validation | weak | counts internal bind calls, tests implementation structure |
| 14 | test_schedule.py:255 decimal_fields_are_decimal_text | useful | rejects `"1/3"` |
| 15 | Accounting k80_primitive_terminal_chain_recompute | useful | hand-countable circuit (4 CX): 7 gates, 26 qubit-seconds |
| 16 | test_schedule.py:1978 loop_iteration_coordinates_select_one_start | useful | start 0.5 gives 4.5 and 13.5, derivable by hand |
| 17 | test_schedule.py:~2020 disjoint_overlap_resource_and_dependent_start | useful | two disjoint X gates: time 1, 2 gates, 2 qubit-seconds |
| 18 | test_schedule.py:881 reader_rejects_empty_blocks | useful | negative grammar case |
| 19 | test_schedule.py:699 classical_minted_token_validity | not read in detail; name-based "useful" guess | |
| 20 | test_schedule.py:1027 while_summary_counts_scheme_workspace | not read in detail | name-based |
| 21 | test_gate.py:10 pinned_sibling_hook_configuration | weak for the product | checks gate plumbing text |

Ratio over the 18 tests I read: useful 11, weak 5, self-referential 1, plumbing 1. Items 19-20 are unread guesses, excluded. Tests are dense and long (test_schedule.py is 2043 lines for 139 tests, average 15 lines, `Accounting` tests built by `estimate(...)["effective_schedule"]` then re-fed to `estimate` as the "expected" schedule: partly self-feeding).

Would the gate catch a wrong result? `scripts/check` runs these unit tests, so a regression in any asserted literal fails. A wrong value in an unasserted area (most of `classical`, `execute`, `action_nodes`) would pass. Wrong spec interpretation is caught only where `bennett-vm` disagrees. The VM is itself maintained by the same ecosystem.

## Code quality
Measured with an `ast` script on estimate.py (244 functions). Longest: `classical` 461 lines (:3272), `execute` 334 (:3395), `action_nodes` 304 (:3864), `oracle` 252 (:2898), `_body` 176 (:1193), `estimate` 163 (:4170). Max line length 401 chars; 126 lines exceed 160. 17 lines have 4 or more `and`/`or`.

Findings against policy rule 9:

1. Silent fallback: `src/estimate.py:1121-1123` wraps a whole visitor in `except (ValueError,TypeError,KeyError,ContractError): return False`. A malformed recipe node (TypeError or KeyError from a bug) makes the predicate return False instead of failing loudly. Failure scenario: a catalog bug turns into a wrong "not a given shape" result rather than an error.
2. Swallowed validation at `:3551-3552`: `try:validate_budget(...) except ContractError:return p,steps,[],True`. Probably the semantic "budget.mint fault", but the exception text is dropped and the fault arm cannot be distinguished from a bug.
3. Bead references in source: `:4734` carries `"bead":{"EST-CONTEXT-03":"bennett-estimate-bph.5",...}` inside the emitted pending report, and `:4196` has the scheduler name `bennett-estimate-default`. Product output depends on bead IDs.
4. Tracked litter: `src/__pycache__/estimate.cpython-312.pyc` and `tests/__pycache__/test_schedule.cpython-312.pyc` are committed (`.gitignore` only has `target/`). Also tracked: `.cursor/`, `.codex/`, `.agents/skills/beads` tooling copies, and 4 beads hook copies.
5. Single-use nested types: `classical()` defines `MintedToken`, `HostToken`, `RegisterRef` dataclasses inside the function body (:3283-). Each call re-creates the classes. Cost: untestable in isolation, 461-line function.
6. Flag proliferation: `Ledger.__init__` (:2206) takes `exact`, `count_only` booleans and tracks `nonexact_native_operations`, `error`; the mode is a state enum candidate.
7. Duplication: the summary path and ledger path each re-derive the same row (the review's own probe compared them). Two implementations of one accounting concept double the surface.
8. Architecture: Rust shell is a trivial wrapper. `python3 -I -` plus the Python source and JSON catalog on stdin is a launcher; `run()` ignores `catalog` if the include path changes, there is no schema check at build time. This is a "lonely" crate whose only job is to give `cargo test` something to call.
9. Python file style: statements joined by `;`, `if ...: return` on one line, no type hints; nothing a linter would pass. `cargo fmt/clippy` run on 56 lines only.

Duplication and dead code: not measured by tool. No TODO/FIXME comments found in estimate.py.

## What is good
- Exact rational arithmetic (`Fraction`) with `decimal_up` rounding, tested against the spec's published witness values (`tests/test_estimate.py:39`).
- Fail-fast error type `ContractError` with exit code 3 for pending contract gaps, and the CLI is deterministic (tested twice-equal).
- `scripts/differential.py` uses the real VM as an oracle and never imports its code, consistent with rule 5.
- Hand-countable accounting tests (items 15-17) that anyone can verify on paper.
- `docs/CONTRACT_GAPS.md` states open spec questions with proposed text rather than choosing silently. This follows the no-narrowing rule.

## Recommendations
1. Add property tests or an independent brute-force "ledger" (replay gates, count by hand) to verify the summary path against a third implementation, not itself.
2. Delete the two tracked `.pyc` files and add `__pycache__/` to `.gitignore` (one commit, zero risk).
3. Replace the catch-all at `src/estimate.py:1121-1123` with specific exceptions, or let it propagate.
4. Split `Source.classical`, `execute` and `action_nodes` (each 300-460 lines); lift the nested dataclasses to module level.
5. Measure Python coverage (`pip install coverage` in a venv) and gate on it; there is none today.
6. Strengthen weak tests: #4 and #5 above should assert numbers, #12 should assert the parsed result.
7. Remove bead IDs from emitted product output (`:4734`) or move them to a doc.
