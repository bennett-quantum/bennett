# bennett-meta quality audit 2026-11-07

Audited **d3c459227143522c10cfcd71d25a3dc4a853e335**, `main` = local `origin/main`, in `/home/tobias/Projects/bennett-workspace/bennett`.
Scope: tracked `tools/`, `scripts/`, and their tests; documentation and local hook configuration read as evidence.
No fetch, source edits, commits, beads, hook installation, gate execution, or external model calls.
Only this report and permitted scratch files under `/home/tobias/Projects/bennett-workspace/bennett/.tmp/reaudit-2026-11-07/` were written.
Two unrelated untracked plugin council paths were present before the audit and left alone.

## Verdict

- Code **B-**: compact, explicit validation and cleanup; retained runner fallbacks and inconsistent council admission checks remain.
- Tests **B-**: useful new packet and hook regressions; 38 permitted tests pass, but retry failures lack tests and the default hook omits the gate-runner suite.
- Build **n/a**: interpreted Python/shell; safe suite wall time **0.87 s**, with no compilation or dependency-resolution build.
- Scripts **B-**: the effective installed hook reaches real tests, but validates the working tree rather than the pushed commits.
- Litter **A**: zero tracked generated files matching the baseline's litter categories; historical process references remain in source prose.

## Composition

`cloc --by-file --json /home/tobias/Projects/bennett-workspace/bennett/tools /home/tobias/Projects/bennett-workspace/bennett/scripts`:

| Language / directory group | Files | Code LOC | Physical lines |
|---|---:|---:|---:|
| Python production tools | 4 | 1,484 | 1,794 |
| Python `tools/tests/` (nonempty files) | 6 | 594 | 689 |
| Python standalone gate selftests | 1 | 416 | 504 |
| Shell `scripts/` | 4 | 88 | 102 |
| Shell gate template | 1 | 17 | 20 |
| Markdown tool documentation | 1 | 116 | 147 |
| Total counted by cloc | 17 | 2,715 | 3,256 |

The empty test-package initializer is tracked but contributes no cloc file/LOC; Python has 12 tracked files, 2,494 code LOC, 2,987 physical lines.

| Module | Physical lines / AST functions | Purpose and test reach |
|---|---:|---|
| [council.py](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:1) | 831 / 34 | review schemas, prompts, member execution, collection, aggregation; 32 council test methods |
| [gate_run.py](/home/tobias/Projects/bennett-workspace/bennett/tools/gate_run.py:1) | 629 / 40 | pinned sibling materialization, isolation, process cleanup, push records; 50 standalone tests |
| [codex_job.py](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:1) | 262 / 10 | retired retry/checkpoint runner; no tests |
| [review_packet.py](/home/tobias/Projects/bennett-workspace/bennett/tools/review_packet.py:23) | 72 / 1 | ordered, excluded, hashed source packets; 3 subprocess tests |
| [gate_selftest.py](/home/tobias/Projects/bennett-workspace/bennett/tools/gate_selftest.py:1) | 504 / 63 | scratch Git repositories, isolation/build/ref/hook assertions; outside ordinary discovery |
| [tools/tests](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/__init__.py) | 689 / 60 | 45 methods: council 32, packet 3, scripts/ignore 10; shared scratch fixture |
| [scripts](/home/tobias/Projects/bennett-workspace/bennett/scripts/pre-push:1) | 102 / shell | clone/update, remote publication, effective-hook installer, unittest push check |

Dependencies: **0 third-party Python imports**, **26 distinct stdlib import roots**, two local import roots (`tools`, `test_council_schema`), no Cargo manifest/lock in scope.
External runtime commands include Git, Bash, Python, `bwrap`, `strace`, `quota`, `gh`, and the model CLIs; availability was not mistaken for an installed Python dependency.
Authorship measured at the audited SHA with `git -C /home/tobias/Projects/bennett-workspace/bennett log <sha> --format='%H%x1f%an%x1f%s%x1f%B%x1e' -- tools scripts`:

| Commit set | Codex-marked | Claude-marked | Unattributed / possible human |
|---|---:|---:|---:|
| Scoped history, 28 commits | 4 (14.3%) | 21 (75.0%) | 3 (10.7%) |
| Whole repository, 311 commits | 7 (2.3%) | 228 (73.3%) | 76 (24.4%) |

Classification: `wip(codex` subject or `Agent: gpt` trailer; otherwise Claude/Opus/Sonnet/Anthropic coauthor trailer; otherwise unattributed.
All Git author names are `tobiasosborne`; an author name alone does not establish human authorship. This corrects the baseline's attribution method.

## Build and test times

All commands were headless with `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR=/home/tobias/Projects/bennett-workspace/bennett/.tmp/reaudit-2026-11-07/tmp`.
Test commands used `systemd-run --user --scope -q --unit=bennett-build-meta-reaudit-<UTC-HHMMSS>`, `timeout 600`, `ulimit -v 8000000`, and `/usr/bin/time -f 'wall_seconds=%e'`.
Python unittest ran serially; `-j3`/Rust test-thread flags do not apply. No target cache applies; bytecode writing was disabled, but existing bytecode may have been read.
The scratch runner selects all council and packet modules plus `test_scripts.CommandTests` and `test_scripts.IgnoreTests`.

| Measurement | Command after environment/scope wrapper | Result |
|---|---|---|
| Warm incremental build / touched source | n/a; no build graph, and source touching prohibited | Not fabricated |
| Syntax compilation | `python3 -I -` compiling all 12 Python files in memory | 0.08 s wall; no bytecode output |
| Test collection (`--no-run` analogue) | `python3 -I /home/tobias/Projects/bennett-workspace/bennett/.tmp/reaudit-2026-11-07/run_safe_tests.py --collect-only` | 38 collected; 0.13 s wall |
| Permitted test subset | same runner, without `--collect-only` | 38 passed; 0.789 s unittest, **0.87 s wall** |
| Instrumented subset | same runner `--trace`, `AUDIT_TRACE=1`, scratch `PYTHONPATH` | 38 passed; 1.344 s unittest, 1.46 s wall |
| Shell syntax | `bash -n` separately on four scripts and the template | All five exit 0; no script executed |
| Full default discovery / hook / gate selftest | Not run: explicit audit prohibition | 7 hook tests + 50 gate selftests excluded |

At collection/run/tracing admission, available RAM was 20 GiB and 1-minute loads were 10.90 / 10.75 / 10.61, satisfying the then-binding `<12` rule.
Earlier load readings above 12 caused admission to be deferred; no test started at those readings.
The later orchestrator update requires `<8`, no `bennett-heavy` scope, and a 30-minute slot limit for runs over about one minute; no such run was started after that update.
The scratch slot wrapper was updated to that rule. No measurement was skipped for exhausting the slot timeout.

Inventory: **95 test methods** = 45 ordinary + 50 standalone; **38 executed**, **57 not executed by audit policy**.
Executed subset: **0 failures, 0 errors, 0 skips, 0 expected failures**. The optimized council command additionally runs 32 council methods in a subprocess; these are repeat executions, not extra unique tests.
The 50 standalone tests include five conditional skips (four `bwrap`, one `strace`); their actual outcomes are unmeasured.
The default suite's complete outcome and time are therefore **not verified**, despite the passing permitted subset.

## Coverage

`python3 -I -m coverage --version` failed: `No module named coverage`. No installation was performed.
Fallback: `sys.settrace`/`threading.settrace` line and call events, including child Python processes via a scratch `sitecustomize.py`.
Executable-line denominators use stdlib `trace._find_executable_linenos`, discarding synthetic line 0; no branch percentage is claimed.
Reproduce summarization: `python3 -I /home/tobias/Projects/bennett-workspace/bennett/.tmp/reaudit-2026-11-07/coverage_summary.py`.

| Production module | Executed / executable lines | Line coverage | Invoked / defined functions |
|---|---:|---:|---:|
| council | 530 / 637 | **83.20%** | 32 / 34 (94.1%) |
| review packet | 57 / 58 | **98.28%** | 1 / 1 |
| retired Codex runner | 0 / 193 | **0%**; no tests | 0 / 10 |
| gate runner | 0 / 511 | **Unmeasured by policy**; observed 0 in this subset | 0 / 40 |

Combined observed production-line execution is **587 / 1,399 = 42.0%**; this is a subset floor, not the coverage of all 95 tests.
Council plus packet alone: **84.5%**. The baseline's approximate 86% council trace used a different executable-line estimate and included the old in-module selftest.
The 86 → 83.2 comparison does not establish a regression: 131 physical council lines were removed and the denominator method differs.
No repository-owned `/home/tobias/Projects/bennett-workspace/bennett/docs/quality.md` coverage record exists.

Five largest untested or weakly tested areas:

1. Gate runner: 511 executable lines not run here; its 50-test suite is also absent from default `tools/tests` discovery ([pre-push:26](/home/tobias/Projects/bennett-workspace/bennett/scripts/pre-push:26), [gate_selftest:80](/home/tobias/Projects/bennett-workspace/bennett/tools/gate_selftest.py:80)).
2. Retired runner: all 193 executable lines; no test imports it ([codex_job:74](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:74), [plan:59](/home/tobias/Projects/bennett-workspace/bennett/docs/plan/2026-11-06-quality-floor-remediation.md:59)).
3. Member execution: successful persistence, timeout, retry/backoff, and subprocess failure paths are missed ([council:554](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:554), [council:565](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:565), [council:576](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:576)); existing test mocks one invalid result.
4. Previous-round prompting and preparation: round 2 context and diff/precheck paths are missed ([council:290](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:290), [council:296](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:296), [council:426](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:426)).
5. Status and incomplete/invalid aggregation: no `status_cmd` invocation; missing-member, invalid-output and regression rendering paths missed ([council:655](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:655), [council:690](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:690), [council:735](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:735)).

## Test quality

Read the three largest production sources (council, gate runner, retired runner), the three largest test sources (gate selftest, council steps, migrated selftest), and all remaining scoped sources/tests.
Random sample: sort Python test-file paths, traverse their AST functions, select 20 from the 45 ordinary methods with `random.Random(20261107).sample(population, 20)`; no hand substitution.
`S` = executed safe subset; `R` = read only because it invokes a prohibited hook.

| Test and location | Class / run | Reason |
|---|---|---|
| [schema:39](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_schema.py:39) `test_schema_does_not_mention_severity` | weak / S | key/word absence only; no acceptance decision |
| [schema:52](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_schema.py:52) `test_prompt_has_no_severity_word` | weak / S | prompt word presence/absence |
| [selftest:28](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_selftest.py:28) `test_validation_and_parsing` | useful / S | invalid score and blocked acceptance rejected; noisy JSON extraction checked |
| [selftest:50](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_selftest.py:50) `test_member_commands_and_state` | useful / S | environment scrubbing, model selection and persisted attempt count |
| [steps:39](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_steps.py:39) `test_valid_structured_item` | useful / S | hand-built valid argument accepted by both validators |
| [steps:54](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_steps.py:54) `test_item_with_neither_steps_nor_problem_rejected` | useful / S | missing argument rejected |
| [steps:60](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_steps.py:60) `test_problem_only_item_missing_steps_key_rejected_by_new_schema_only` | useful / S | pins intentional legacy/new-schema distinction |
| [steps:76](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_steps.py:76) `test_legacy_item_validates_on_legacy_path` | useful / S | legacy compatibility contract, although positive-only |
| [steps:101](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_steps.py:101) `test_spec_gap_kind_requires_assumed_step_one` | useful / S | inconsistent issue classification rejected |
| [steps:127](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_steps.py:127) `test_accept_with_only_spec_gaps_is_valid` | useful / S | spec gaps do not block acceptance |
| [steps:133](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_steps.py:133) `test_accept_with_implementation_item_rejected` | useful / S | implementation finding blocks acceptance |
| [steps:166](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_steps.py:166) `test_steps_and_spec_gap_rendering` | useful / S | issue identities, routing and counts checked |
| [steps:203](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_steps.py:203) `test_legacy_rendering_unchanged_and_no_spec_gap_heading` | useful / S | compatibility output plus machine-readable gap omission |
| [packet:49](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_review_packet.py:49) `test_missing_or_excluded_first_file_fails` | useful / S | CLI fails for missing and excluded priority files |
| [scripts:31](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_scripts.py:31) `test_gate_fails_with_only_skipped_tests` | useful / R | skipped-only fixture must fail the hook |
| [scripts:40](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_scripts.py:40) `test_gate_fails_with_only_expected_failures` | useful / R | expected failures cannot constitute a passing gate |
| [scripts:49](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_scripts.py:49) `test_gate_fails_with_only_skipped_subtests` | useful / R | skipped subtests cannot satisfy success count |
| [scripts:59](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_scripts.py:59) `test_gate_accepts_pass_and_skip_with_one_discovery_and_run` | useful / R | import/body marker file checks exact execution counts |
| [scripts:73](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_scripts.py:73) `test_gate_runs_tests_and_propagates_failures` | useful / R | paired passing/failing fixtures require different exit codes |
| [scripts:111](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_scripts.py:111) `test_council_selftest_runs_unittest_under_optimization` | useful / S | actual optimized subprocess must run unittest successfully |

Sample ratio: **18 useful (90%), 2 weak (10%), 0 tautological**; 15 sampled bodies executed, five hook tests inspected only.
The unsampled prompt-shape test remains weak ([steps:145](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_steps.py:145)).
Oracle basis: explicit protocol fixtures and negative pairs; real Git repositories and subprocess exits; independently pinned binary SHA prefix ([packet:45](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_review_packet.py:45)).
No numeric tolerance, native differential, property generator, or ISA semantic oracle is relevant to these tools; council tests validate argument shape, not whether an LLM finding is true.
The separate gate suite checks genuine external facts: pinned file content, exit status, cache build count, and killed process trees ([gate_selftest:81](/home/tobias/Projects/bennett-workspace/bennett/tools/gate_selftest.py:81), [:129](/home/tobias/Projects/bennett-workspace/bennett/tools/gate_selftest.py:129), [:324](/home/tobias/Projects/bennett-workspace/bennett/tools/gate_selftest.py:324)).
Default push discovery would catch many council/packet errors; it cannot catch a wrong `gate_run.py` result through those standalone tests because it never discovers them.

## Code quality

Findings below distinguish retained baseline defects from additional static limitations; no product-rung or oracle-soundness defect was dynamically demonstrated.

| Finding | Evidence | Failure scenario / cost |
|---|---|---|
| Default hook omits gate-runner tests | [pre-push:26](/home/tobias/Projects/bennett-workspace/bennett/scripts/pre-push:26), [gate_selftest:504](/home/tobias/Projects/bennett-workspace/bennett/tools/gate_selftest.py:504) | A gate-runner regression can pass all ordinary tests; explicit invocation is required. |
| Meta hook checks working tree, not pushed SHA | [pre-push:5](/home/tobias/Projects/bennett-workspace/bennett/scripts/pre-push:5), [:10](/home/tobias/Projects/bennett-workspace/bennett/scripts/pre-push:10), [:26](/home/tobias/Projects/bennett-workspace/bennett/scripts/pre-push:26) | Clean/passing working tree can accompany a push of another broken commit; arguments/stdin are not used. Static finding, not reproduced by running the forbidden hook. |
| Admission validation has two strengths | [council:532](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:532), [:595](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:595), [:694](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:694) | New subprocess/collected results get schema checks; cached outputs and aggregation get only legacy validation, so edited cached JSON may bypass required fields. |
| Retired pace guard still fails open | [codex_job:76](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:76), [:197](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:197) | Reusing the retired CLI after quota failure launches work anyway; R26 removes current operational dependence, not the source defect. |
| Retired checkpoint/backup failures are log-only | [codex_job:103](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:103), [:130](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:130), [:133](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:133) | Reuse can report job completion without a durable checkpoint/backup status. |
| Description fallback does not handle empty output | [create-remotes:28](/home/tobias/Projects/bennett-workspace/bennett/scripts/create-remotes.sh:28) | README with no third line produces an empty description and successful pipeline; fallback only handles nonzero status. |
| Process/session prose remains | [codex_job:28](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:28), [:95](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:95), [:110](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:110), [council:396](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:396) | Job-history comments and stale session paths occupy source and emitted prompts; dates here are process references, not contract version identifiers. |

AST measurements (production Python only; inclusive physical function length; control nesting counts `if/for/while/with/try/comprehension`):

| Metric | Result |
|---|---|
| Functions / median / maximum length | 85 / 9 / 86 lines |
| Functions >100 / >300 lines | 0 / 0 |
| Largest functions | council `aggregate_cmd` 86 at :683; retired runner `run` 56 at :179; council `validate` 54 at :147; packet `main` 46 at :23 |
| Maximum control nesting | council 6; gate runner 4; retired runner 5; packet 3 |
| Boolean nodes with >=3 direct operands | council 6; gate runner 4; other production tools 0 |
| Functions <=3 lines | 16; size proxy, not a claim all 16 are gratuitous wrappers |
| Broad `except Exception` | 3, all in retired runner (:78, :103, :133) |

One mechanically redundant wrapper remains: [gate_run:201](/home/tobias/Projects/bennett-workspace/bennett/tools/gate_run.py:201) only constructs `Isolation`; low-value cleanup, no correctness claim.
No repeated identical stripped line longer than 40 characters occurs >=3 times within any of the four production modules; this is a narrow duplication screen, not clone detection.
Separate schema and semantic validators intentionally check overlapping facts; their inconsistent use above matters more than textual duplication.
Unused import candidates: `tempfile` [gate_run:20](/home/tobias/Projects/bennett-workspace/bennett/tools/gate_run.py:20), `os` [review_packet:14](/home/tobias/Projects/bennett-workspace/bennett/tools/review_packet.py:14).
No unsupported claim of unreachable production functions: the runner is retired by policy but remains executable; dynamic CLI callbacks defeat simple textual call counts.
State dictionaries carry externally persisted protocol records; no contradictory boolean-state bug was established. Tests' stdout substrings are useful when coupled to persisted state/exits, weak when used alone.
Tracked-file screening with `git ls-files` found **0** pycache/pyc/log/LOCK/`.lock`/`.darc`/LAST-RUN/PROGRESS paths repository-wide, including **0** council `.log` files.

## Against the 2026-11-05 baseline

Re-derived from current code and measurements; old grades were not used as scoring thresholds. Build stays n/a on the baseline scale; its separate Scripts grade is retained.

| Grade | Baseline → current | What moves it up one step |
|---|---|---|
| Code | C → **B-** | Apply round schema checks consistently and close the working-tree/pushed-SHA gap. |
| Tests | C- → **B-** | Add timeout/retry and previous-round negative tests, and make gate-runner regressions part of an explicitly run default check. |
| Build | n/a → **n/a** | No grade step applies without a build; verify the complete default test time when gate execution is permitted. |
| Scripts | D → **B-** | Test the actual pushed commits and automatically include the separate gate-tool tests. |
| Litter | C → **A** | Already at the top of this generated-file scale; keep tracking clean. |

Every baseline finding/coverage concern, with current status:

| Baseline item | Status | Current evidence |
|---|---|---|
| Pace guard returns None and proceeds | **not fixed** | [codex_job:78](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:78), [:197](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:197); operationally superseded by [plan:59](/home/tobias/Projects/bennett-workspace/bennett/docs/plan/2026-11-06-quality-floor-remediation.md:59). |
| Checkpoint and backup failures only logged | **not fixed** | [codex_job:103](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:103), [:133](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:133); same retirement qualification. |
| Hook installer failure swallowed | **fixed** | [create-remotes:30](/home/tobias/Projects/bennett-workspace/bennett/scripts/create-remotes.sh:30) has no `|| true`; [test_scripts:118](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_scripts.py:118) passed with required exit 23. |
| Dead/empty remote-description fallback | **not fixed** | [create-remotes:28](/home/tobias/Projects/bennett-workspace/bennett/scripts/create-remotes.sh:28); baseline explanation was imprecise because `pipefail` can propagate earlier failures. |
| Installed cargo-only no-op hook | **fixed** | effective [Beads hook:5](/home/tobias/Projects/bennett-workspace/bennett/.beads/hooks/pre-push:5) execs current script; executable bit verified; [installer:5](/home/tobias/Projects/bennett-workspace/bennett/scripts/install-hooks.sh:5) honors hooksPath. Old Git hook is inactive. |
| Production selftest asserts vanish under -O | **fixed** | [council:775](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:775) runs unittest; optimized CLI test passed. |
| 141-line tests embedded in production | **fixed** | four migrated methods in [test_council_selftest:20](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_selftest.py:20); compatibility entrypoint is 10 lines. |
| Long functions / nesting hotspot | **partly** | max production function now 86; aggregation and validator still at [council:683](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:683) and [:147](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:147), nesting remains 6. |
| Long Boolean chains | **not fixed** | 6 council + 4 gate nodes; [council:719](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:719), [gate_run:109](/home/tobias/Projects/bennett-workspace/bennett/tools/gate_run.py:109); old count used a different AST grouping. |
| Timeout becomes recorded rc -1 | **not fixed** (accepted behavior) | [council:558](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:558); explicit timeout catch, not broad silent swallowing. |
| User-supplied shell precheck | **not fixed** (intended interface) | [council:428](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:428); no new vulnerability alleged. |
| No process references reported | **not fixed** (baseline miss) | historical comments/prompts at [codex_job:110](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:110), [council:396](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:396); no bead-ID regression demonstrated. |
| 16 tracked council logs | **fixed** | `git -C /home/tobias/Projects/bennett-workspace/bennett ls-files '*.log'` returns no paths; ignore patterns present. |
| Codex runner has zero tests | **not fixed** | no test imports it; trace 0/193; R26 explicitly supersedes further runner work. |
| Packet builder has zero tests | **fixed** | [test_review_packet:26](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_review_packet.py:26), [:37](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_review_packet.py:37), [:49](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_review_packet.py:49); all pass, 98.28% lines. |
| Council retry/failure coverage hole | **not fixed** | [council:554](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:554), [:558](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:558), [:576](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:576) missed. |
| Prompt round-state coverage hole | **not fixed** | [council:300](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:300), [:434](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:434) missed. |
| Aggregation consensus/invalid-output holes | **partly** | external happy-path consensus now exercised at [test_council_selftest:140](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_selftest.py:140); missing/invalid input paths remain missed. |
| Status and run CLI holes | **partly** | dry-run CLI covered at [test_council_selftest:126](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_selftest.py:126); status and real successful member execution remain missed. |
| Validator malformed-input holes | **not fixed** | [council:157](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:157), [:180](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:180), [:197](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:197) still missed. |
| Three prompt/schema word-only weak tests | **not fixed** | [schema:39](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_schema.py:39), [:52](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_schema.py:52), [steps:145](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_council_steps.py:145). |

Baseline recommendations, individually:

| Recommendation | Status | Evidence / qualification |
|---|---|---|
| 1. Fail closed on pace errors | **not fixed** | runner source unchanged; R26 retires its operational use, not a technical fix. |
| 2. Install real hook and reject no tests | **fixed in intent** | effective chaining hook and [pre-push:27](/home/tobias/Projects/bennett-workspace/bennett/scripts/pre-push:27), [:32](/home/tobias/Projects/bennett-workspace/bennett/scripts/pre-push:32); specialized meta unittest gate replaces literal template adoption. |
| 3. Add runner and packet tests | **partly** | three packet tests added; runner tests intentionally omitted under R26 ([plan:59](/home/tobias/Projects/bennett-workspace/bennett/docs/plan/2026-11-06-quality-floor-remediation.md:59)). |
| 4. Move assertions to tests | **fixed** | migrated unittest methods; optimized command passes. |
| 5. Remove swallowed installer failures | **fixed** | real script under stubbed Git/gh fails with installer exit 23. |
| 6. Untrack and ignore logs | **fixed** | zero tracked `.log`; [.gitignore:17](/home/tobias/Projects/bennett-workspace/bennett/.gitignore:17) ignores them. |
| 7. Split council into modules | **not fixed** | still one 831-line module; removal of embedded tests reduces size without the proposed module split. |

Synthesis recommendations affecting meta: no-main-WIP root cause is **partly addressed by policy** ([plan:59](/home/tobias/Projects/bennett-workspace/bennett/docs/plan/2026-11-06-quality-floor-remediation.md:59)); the retired CLI can still checkpoint whichever branch it is given ([codex_job:129](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:129)).
The synthesis's real-hook and log-cleanup items are fixed; its pace item is retired but not fixed in code; its measured-record item is missing for meta.
Pinning sibling product tests, numeric oracles, and Rust fast/slow splitting concern sibling repos and are not inferred from this audit.
Earlier meta reviews are [round 1](/home/tobias/Projects/bennett-workspace/bennett/docs/reviews/2026-11-06-quality-meta-r1.md:8) and [round 2](/home/tobias/Projects/bennett-workspace/bennett/docs/reviews/2026-11-06-quality-meta-r2.md:11): skipped-only success and the unpinned digest were already found and repaired there; they are not new findings here.

## Plan targets

Checks below address the Targets table and applicable R0.1 deliverables; they do not certify the other 12 repositories.

| Target | Status | Command + result / source evidence |
|---|---|---|
| Zero red default main tests | **not established** | permitted runner: 38 pass; full default test run prohibited. No observed red test, but seven default hook methods remain unexecuted. |
| Zero live-sibling test reads | **met in scope** | `git -C /home/tobias/Projects/bennett-workspace/bennett grep -n -E '\.\./bennett-|/home/.*/bennett-' -- tools/tests tools/gate_selftest.py`: exit 1, zero matches; test bodies use scratch sibling roots, no live product sibling oracle. |
| Recorded coverage number + command | **not met for meta** | `Path('/home/tobias/Projects/bennett-workspace/bennett/docs/quality.md').exists()` = false; this audit supplies trace numbers only. Literal programme target names 12 code repos, so this is not a failure claim about those repos. |
| Default test wall <180 s | **not established** | permitted subset 0.87 s; full 45-method default duration unmeasured under the audit prohibition. |
| Tests >=B | **not met** | independently re-derived B-; omitted gate-tool checks and missing council failure scenarios above. |
| Code >=B- | **met** | independently re-derived B-, with residual defects/limitations listed. |
| No >300-line semantics functions | **met** | Python AST on all four production tools: 85 functions, maximum 86; no remaining >300-line list needed. |
| Zero bead/job/process identifiers in source/output | **not met** | scoped `git grep` for `COMMON rule`, `2026-`, and process references finds [codex_job:28](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:28), [:110](/home/tobias/Projects/bennett-workspace/bennett/tools/codex_job.py:110), [council:396](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:396); no new bead-ID match established. |
| Zero tracked generated litter | **met** | `git ls-files` filtered for pycache/pyc/log/LOCK/lock/darc/LAST-RUN/PROGRESS: 0 repository-wide. |
| R0.1 packet tests, unittest selftest, installer failure propagation | **met within audit limits** | three packet tests, four migrated council methods, optimized CLI and failed-installer tests pass; effective installed wrapper verified statically. |
| R0.1 literal gate-template installation | **partly / adapted** | [installer:14](/home/tobias/Projects/bennett-workspace/bennett/scripts/install-hooks.sh:14) installs a wrapper to the specialized meta gate, not the template; intended useful-test checks are present, hook test execution prohibited. |

No meta `gate.toml`, `docs/quality.md`, or complexity-ratchet script exists (`git ls-files tools scripts gate.toml docs/quality.md`).
The common round-1 metric-ratchet/HANDOFF retirement work was explicitly excluded from this meta R0.1 prerequisite in [review-r1:53](/home/tobias/Projects/bennett-workspace/bennett/docs/reviews/2026-11-06-quality-meta-r1.md:53); central ecosystem `HANDOFF.md` is not treated as stale per-repo litter.

## What is good

1. Hook success requires an actual unittest `addSuccess`, covering skipped and expected-failure-only suites ([pre-push:18](/home/tobias/Projects/bennett-workspace/bennett/scripts/pre-push:18)); inspectable tests exercise each outcome.
2. Hook installation follows effective `core.hooksPath` and uses atomic replacement ([installer:5](/home/tobias/Projects/bennett-workspace/bennett/scripts/install-hooks.sh:5), [:17](/home/tobias/Projects/bennett-workspace/bennett/scripts/install-hooks.sh:17)).
3. Packet tests distinguish directory names from prefixes and pin a real binary digest ([test_review_packet:26](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_review_packet.py:26), [:45](/home/tobias/Projects/bennett-workspace/bennett/tools/tests/test_review_packet.py:45)).
4. Council state is atomically persisted, raw attempts are retained, and collected results use the prepared schema ([council:241](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:241), [:561](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:561), [:631](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:631)).
5. Gate runner owns process-group termination in a `finally` block ([gate_run:205](/home/tobias/Projects/bennett-workspace/bennett/tools/gate_run.py:205)); a concrete process-survival regression test exists, though not executed here.

## Recommendations

1. Add a bounded, explicitly invoked gate-tool test check to meta verification; do not leave its 50 methods outside default discovery without another automated owner ([pre-push:26](/home/tobias/Projects/bennett-workspace/bennett/scripts/pre-push:26)).
2. Make meta push verification use pushed commits, with a regression that pushes a failing commit from a passing working tree ([pre-push:5](/home/tobias/Projects/bennett-workspace/bennett/scripts/pre-push:5)).
3. Add mocked council timeout/nonzero/retry-success cases and round-2 prompt/invalid aggregation cases; current coverage misses these concrete failure decisions ([council:538](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:538)).
4. Use the prepared schema consistently for cached council outputs and aggregation, preserving explicitly tested legacy compatibility ([council:595](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:595), [:694](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:694)).
5. Remove or clearly disable the retired runner rather than spending new implementation effort on its superseded pace/checkpoint paths ([plan:59](/home/tobias/Projects/bennett-workspace/bennett/docs/plan/2026-11-06-quality-floor-remediation.md:59)).
6. When meta is included in the quality-record programme, record a reproducible coverage command and distinguish omitted gate code from tested code; no source-module split is justified merely by total file length.
7. Replace process-history comments/stale prompt paths with current task context, and give the remote-description fallback an explicit nonempty check ([council:396](/home/tobias/Projects/bennett-workspace/bennett/tools/council.py:396), [create-remotes:28](/home/tobias/Projects/bennett-workspace/bennett/scripts/create-remotes.sh:28)).
