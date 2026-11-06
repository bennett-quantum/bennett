# bennett-meta quality audit 2026-11-05

Scope: `tools/` (orchestration Python: council.py, codex_job.py, review_packet.py, gate_*.py, tests/) and `scripts/`
(shell). Read-only; no repo edits, no commits. Gate tooling (`gate_run.py`, `gate_selftest.py`, `gate_pre-push.template`)
was read statically only, because the brief forbids running gate* code. Headless env used for all runs.

## Verdict
- Code: **C.** Orchestration code with real fail-fast in council.py validation, but one fail-open path that disables the pace guard, and `assert`-based checks in production code.
- Tests: **C-.** council.py has 28 unittest tests plus an in-module selftest, and its executed-line coverage is about 86%. codex_job.py and review_packet.py have zero tests (334 lines together).
- Scripts: **D.** The installed `pre-push` hook is the bootstrap cargo-only stub, not the gate template, and the meta repo has no Cargo.toml, so its push "gate" always passes.
- Build: n/a (no build). Test run for the one suite that exists: 0.15 s (wall 1.1 s).
- Litter: **C.** No tracked pycache or backup files in tools/scripts. 16 council run logs are tracked under `docs/council/`.

## Composition
Tracked Python in `tools/` (wc -l): council.py 962, gate_run.py 629, gate_selftest.py 504, codex_job.py 262,
review_packet.py 72, tests/ 271 (test_council_steps.py 212, test_council_schema.py 59). Total 2,700 lines.
cloc on tools+scripts: Python 7 files, 2,244 code lines; shell 5 files, 74 code lines; gate_README.md (Markdown).

| Module | Lines | defs | Purpose | Tests |
|---|---|---|---|---|
| council.py | 962 | 35 | multi-model review rounds: prepare, run members, validate JSON, aggregate, render | 28 unittest + in-module selftest |
| gate_run.py | 629 | 28 | push gate runner (pinned tool, sibling pins, gate.toml) | gate_selftest.py (50 test methods, not run here) |
| gate_selftest.py | 504 | 63 | self-test harness for gate_run | n/a |
| codex_job.py | 262 | 9 | Codex job runner: pace check, wip backups, checkpoint commits | **none** |
| review_packet.py | 72 | 1 | packs a repo into a review document | **none** |
| scripts/create-remotes.sh | ~40 | - | creates GitHub remotes from manifest.toml | none |
| scripts/install-hooks.sh, pre-push, clone-all.sh | ~30 | - | hook install and cargo-test stub | none |

Authorship (`git log -- tools scripts`): 25 commits, all by one human author (tobiasosborne). None carries an `Agent:`
trailer. Codex is the author of the runner's own commits: codex_job.py:107-135 writes `Agent: <model>` trailers. Repo-wide
(285 commits), 1 commit is `wip(codex` or `Agent: gpt` (0.4%).

## Build and test times
| Step | Command (headless, -I) | Result |
|---|---|---|
| tools unit tests | `python3 -I -m unittest discover -s tools/tests -t <meta>` | 28 tests, OK, 0.15 s (wall 1.08 s) |
| council selftest | `python3 -I tools/council.py selftest` | "selftest ok", wall 0.72 s |
| gate_selftest.py | not run (brief: gate* must not run) | 50 test methods |
| coverage (council.py) | `python3 -m trace --count --missing` over unit tests + selftest | ~86% of executable lines (762 est., 106 missed) |

No cargo. No build step exists; scripts are not compiled.

## Coverage
Measured with the stdlib `trace` module (executable-line estimate; not coverage.py). Unit tests and selftest together.
- council.py: ~86% of lines executed (762 executable, 106 missed).
- codex_job.py: 0% (no test imports it; 262 lines).
- review_packet.py: 0% (72 lines).
- gate_run.py, gate_selftest.py: not measured (not run).

The five largest untested or weakly tested areas in council.py (missed lines, from the trace report):
1. `run_member()` failure path, council.py:558-580 (timeout, nonzero exit, bad output retry). The retry loop is the thing that matters most.
2. `build_prompt()` and `previous_round_context()`, council.py:300-318 and 409-438. Prompt construction is not checked against round state.
3. `aggregate_cmd()`, council.py:690-742: the consensus-branch lines at 690-696 and 738-742 are not executed by either suite.
4. `status_cmd()` and `run_cmd()`, council.py:586-609 and 656-670: the CLI surfaces.
5. `validate()` error lines, council.py:157, 180 and 197 (never executed).

## Test quality
Sampled 15 council tests and read the bodies of the two files:

| Test | Class | Why |
|---|---|---|
| test_council_steps.py:88 test_step_one_witness_rejected | useful | Pins a spec rule (step 1 needs a witness) with a concrete bad item |
| test_council_steps.py:101 test_spec_gap_kind_requires_assumed_step_one | useful | Negative pair with :94; checks both directions of the rule |
| test_council_steps.py:111 test_last_step_must_cite_steps | useful | Specific failure mode |
| test_council_steps.py:117 test_cited_step_must_exist_earlier | useful | Rejects forward citation |
| test_council_steps.py:127 test_accept_with_only_spec_gaps_is_valid | useful | Positive case paired with :133 |
| test_council_steps.py:133 test_accept_with_implementation_item_rejected | useful | Negative for the consensus rule |
| test_council_steps.py:182 test_only_spec_gaps_reaches_consensus | useful | End-to-end routing check |
| test_council_steps.py:166 test_steps_and_spec_gap_rendering | useful | Routes a spec-gap to its own section and checks the cited step lines, consensus split and the core/contract counts |
| test_council_steps.py:203 test_legacy_rendering_unchanged_and_no_spec_gap_heading | useful | Exact string for a legacy item; regression guard for old reports |
| test_council_steps.py:145 test_prompt_describes_shape_without_severity | weak | Substring needles in the prompt plus `assertNotIn("severity")`; word-presence checks |
| test_council_schema.py:39 test_schema_does_not_mention_severity | weak | Pins the absence of a key in the schema; no behaviour is exercised |
| test_council_schema.py:52 test_prompt_has_no_severity_word | weak | Word-absence check plus "S1" presence |
| test_council_schema.py:26 test_item_without_severity_validates | useful | Positive case for the current schema |
| test_council_schema.py:46 test_accept_with_blocking_rejected | useful | Negative for the verdict rule |
| council.py:804-806 selftest: env scrub (CLAUDE_CODE_*) | useful | Checks that member subprocess envs drop Claude vars; a real isolation property |

Totals over the 15 rows: 12 useful, 3 weak (all word-presence checks), 0 tautological. Several council tests use
trivial input (one-key dicts). The 15 were chosen by hand from the two files and their bodies were read; `test_council_steps.py`
has 23 tests and `test_council_schema.py` has 5, so this is a sample, not the full set. The selftest (council.py:773-913, 141 lines) lives in the production module, is run only by
its own subcommand, and mixes oracle checks (`assert validate(good) == []`, council.py:782) with fixture setup. `gate_selftest.py`
was not sampled (gate rule).

Would the tests catch a wrong result? For council validation: yes, the schema and step rules have negative tests. For
codex_job pace and commit logic: no test exists, so a regression there is caught only by use.

## Code quality
Checked against code-quality policy rule 9 and fail-fast:
- **Fail-open pace guard (high).** `codex_job.py:77-78`: `codex_pace()` wraps `quota --json` in `except Exception: return None`.
  `codex_job.py:196-199`: `None` means "quota unavailable; proceeding". Any failure (quota missing, timeout, changed JSON
  shape) silently disables the weekly pace check, which the memory rule says must stop queue runners when over pace.
  Failure cost: a runner keeps spending over-pace quota with no error.
- **Silent swallow of checkpoint and backup failures (medium).** `codex_job.py:103-104` (`wip backup failed` logged only),
  `codex_job.py:133-134` (`commit ... failed` logged, retried later). Documented as intentional, but the job reports success
  to the caller while the backup is missing. A status field would make it loud.
- **Silent hook-install failure (medium).** `scripts/create-remotes.sh:30`: `(cd "$d" && ./scripts/install-hooks.sh ... ) || true`.
  A failed hook install prints nothing.
- **Dead fallback (low).** `scripts/create-remotes.sh:28`: `$(head ... | sed -n '3p' | cut -c1-120 || echo ...)`. The `||`
  binds to `cut`, which does not fail, so the `echo` default never runs and the description can be empty.
- **Stale push hook (high).** `scripts/install-hooks.sh:4` copies `scripts/pre-push`, which is the bootstrap cargo-only stub
  (`find ... Cargo.toml`; prints "no Rust crates; nothing to test"; `exit 0`). The real gate is `tools/gate_pre-push.template`,
  which is not what gets installed. The meta repo has zero Cargo.toml files, so the hook it installs in bennett pushes
  always passes. Failure cost: no push gate on this repo.
- **Assertions in production code (medium).** `council.py:782-806` contains bare `assert`s inside `selftest()`. `python -O`
  strips them, so the selftest passes vacuously under -O. The tests belong in tools/tests.
- **Tests in the production module (low).** `selftest()` (council.py:773-913, 141 lines) is the longest function in the tree.
- **Long functions (AST).** council.py: `selftest` 141, `aggregate_cmd` 86 (line 683), `validate` 54 (line 147), `build_prompt` 46.
  codex_job.py: `run` 56 (line 179), `attempt` 40 (line 137). gate_run.py: `prepare` 41 (line 373). Deepest nesting: 6 levels in council.py `validate`.
- **Long boolean chains (rule 9).** council.py:422 (`rdir.exists() and any(...) and (not a.force)`) and :719; gate_run.py:109 and :519.
  Seven chains of three or more operands in council.py (AST count), four in gate_run.py.
- **Broad except (low).** `council.py:558-559` turns a timeout into rc -1 with a message in the raw log. Acceptable (recorded).
- **Shell with user input (low, intended).** `council.py:428` runs `a.precheck` via `shell=True`; a CLI-supplied command.
- **Bead and session references.** None in tools/ (`grep` for `b-*-NNN`, "TODO", "FIXME" returned nothing).
- **Duplication.** Not scanned in this pass.

## Tracked litter
- `tools/` and `scripts/`: none (`__pycache__` is ignored by `.gitignore`).
- `docs/council/**/*.log`: 16 run logs are tracked (for example `docs/council/isa-2026-10-28/round-1/run-1.log`,
  `docs/council/dialect-2026-10-29/round-1/runner.log`). Run output is not source. Untrack and ignore.
- `.tmp/` is ignored.

## What is good
1. council.py validation is strict and specific: schema, step-citation and accept-with-blocking rules fail with named errors (council.py:147-197).
2. council.py writes state atomically (`atomic_write`) and records raw output per attempt (`raw-<member>-<n>.txt`), so failures are inspectable (council.py:559-565).
3. council.py's selftest runs the real `run_member` path with a patched subprocess, returning the same text to the Muse path and checking it reports identical validation errors (council.py:~893-900).
4. The member subprocess environment is scrubbed of Claude variables (selftest council.py:804-806), so a council member cannot inherit the orchestrator's session.
5. review_packet.py is 72 lines with one job and explicit `--first` validation (`sys.exit` on missing paths).

## Recommendations
1. Make `codex_pace()` fail closed: on quota failure, stop the runner and log why, rather than returning None and proceeding (codex_job.py:77-78, 196-199).
2. Fix `scripts/install-hooks.sh` to install `tools/gate_pre-push.template` (or call the gate tool), and make the meta repo's push check exit non-zero when there is nothing to test. Do this before the next push.
3. Add tests for codex_job.py (pace parsing, checkpoint commit ownership, backup) and review_packet.py (exclude globs, `--first` ordering): about 150 lines of unittest, enough to cover both.
4. Move council.py `selftest` assertions into tools/tests and delete the in-module selftest, or make it raise instead of asserting.
5. Replace the `|| true` at create-remotes.sh:30 with a counted failure summary.
6. Untrack `docs/council/**/*.log` and add the pattern to `.gitignore`.
7. Split council.py (962 lines, 35 defs) into prepare / members / aggregate modules; `validate` and `aggregate_cmd` are the first to extract.
