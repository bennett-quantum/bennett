# Quality floor remediation (2026-11-06)

Maintainer direction (2026-11-06): raise the quality floor across the ecosystem; Codex quota is plentiful and
gpt-6.1-sol xhigh is to be used extensively; run a few rounds until the audit grades improve.
Baseline: `docs/quality/2026-11-05-audit/SYNTHESIS.md` and the thirteen per-repo reports beside it, produced by
Sonnet/Haiku auditors from `docs/quality/2026-11-05-audit/BRIEF.md`. The same brief, run by the same kind of auditor,
is the measurement after every round. Nothing in this plan changes a published contract, so no council round is needed.

## Targets (exit criteria for the programme)

| metric | baseline (2026-11-05) | target after round 2 |
|---|---|---|
| repos with a red `main` (default test run) | 7 of 11 | 0 |
| tests that read a live sibling instead of the gate pin | 5 repos | 0 |
| repos with a measured coverage number recorded | 3 | all 12 code repos (Rust: cargo llvm-cov; Python: coverage.py) |
| default `cargo test` (or repo equivalent) wall time | 112 s to 600 s in the large crates; isa-spec unusable | under 180 s in every crate, slow tests tagged and run by the gate |
| audit test grade | C to B | no repo below B |
| audit code grade | C- to B | no repo below B- |
| functions over 300 lines in semantics-bearing code | about 25 | 0 in files touched by a P0/P1 fix; the rest listed with an owner |
| bead or job identifiers in source, error strings, emitted output | 6 repos | 0 (codes may stay in test names and review docs) |
| tracked pycache, logs, locks, backups, LAST-RUN files | 6 repos | 0 |

Coverage is recorded as one number per repo in `<repo>/docs/quality.md` with the command that produced it. No
threshold, no dashboard (policy rule 8): the number only needs to exist and be re-measured each round.

## Principles

1. Root causes before symptoms. Two causes make seven mains red; fix them in round 0, once each.
2. A test must be able to see the bug class it names. Tolerance, fixture size and oracle independence are checked
   for every test a job touches (the arith 4-ulp lesson).
3. Function splitting rides along with correctness fixes in the same change by the same implementer; no separate
   refactoring campaign, no file is split twice.
4. One implementer per repo at a time. The remediation job for a repo supersedes that repo's stopped queue runner
   and inherits its round-2 P0/P1 list as item 1, so there is one stream, not two.
5. No narrowing. Deleting a tautological test or a stub is honest; deleting a capability is not. Red-by-design tests
   for promised capabilities (driver `classes`, `device_models`) stay red and visible under a named switch.
6. Review as policy: Codex implements, Claude reviews (Sonnet bug hunt plus Opus read for semantics-bearing code),
   three rounds max, only P0/P1 block, one document per round in `docs/reviews/`.

## Round 0: ecosystem prerequisites (meta repo, one sol job, then two cross-repo jobs)

R0.1 `quality-meta` (bennett/tools, bennett/scripts). Red-first:
- `tools/codex_job.py`: every job works on branch `job/<name>` cut from the repo's main at launch; checkpoints and
  attempt-end commits go to that branch and are backed up to `wip/<job>` as today; nothing is ever committed to
  `main` by a runner. Merging to main is the orchestrator's act after the review round (fast-forward or merge, gate
  green). This amends git policy 9 and needs the maintainer's ratification (decision D5 below).
- Pace guard fails closed: a quota read failure stops the runner after the current bead and logs why
  (`codex_job.py:77-78`, `196-199`). Honour the maintainer's 2026-11-06 direction by a `--pace-margin` large enough
  for this programme, set per launch, never by disabling the guard.
- Commit routine: skip owned paths with nothing tracked and nothing untracked (the sched `pathspec 'examples'`
  failure); add a `stop` subcommand that does what `winddown.py` does for one job.
- Tests for `codex_job.py` and `review_packet.py` (pace parsing, branch creation, owned-path commit, backup, exclude
  globs): unittest, about 150 lines, run by the meta repo's pre-push.
- `scripts/install-hooks.sh` installs `tools/gate_pre-push.template`; the meta repo's hook fails when it finds nothing
  to run. `council.py` selftest asserts become tests under `tools/tests/`; `|| true` in `create-remotes.sh` removed.
- Untrack `docs/council/**/*.log`; `.gitignore` for `__pycache__/`, `*.pyc`, `*.log`, `.beads/**/LOCK`, `*.darc` in
  every repo (each repo's job applies its own copy; the pattern list lives in `tools/gate_README.md`).

R0.2 Pin discipline, one small job per affected repo (driver, arith, plugin, sched, circuits), each red-first:
- Every test or script that reaches a sibling resolves it through the repo's `gate.toml` pin: either the gate's
  checkout under `.tmp/gate-siblings/<repo>@<sha>` or a fail with one message naming the pin and the sibling's actual
  HEAD. No default to `../<sibling>`. Driver's `unwrap_or(ws.join(..))` defaults go; plugin `contract_policy.py`
  compares against the pinned registry via `git show`; sched `conformance_inventory` reports the SHA it ran against;
  circuits' eleven test files read the pinned checkout; arith's three K91 failures are resolved by re-pinning or by
  fixing the objects, whichever the pinned run shows is right.
- No shared code: each repo carries its own 30-line resolver (rule 5 of CLAUDE.md). The convention, not code, is
  documented in `bennett/tools/gate_README.md`.

R0.3 Audit brief becomes the standing measurement: `docs/quality/2026-11-05-audit/BRIEF.md` is the template; each
round's reports land in `docs/quality/<date>-audit/`. Auditors are Sonnet (Haiku for targets and meta), never the
implementer's model family.

Round 0 exit: meta hook real and tested; codex_job branch mode verified on a scratch repo; the five pin jobs merged
after Claude review; `cargo test` green in driver (except the two red-by-design), arith circuits tests, plugin
`contract_policy`, sched inventory, circuits.

## Round 1: per-repo remediation jobs (sol xhigh, one per repo, run concurrently)

Common work list for every job, in this order, each item red-first and committed separately:
1. The repo's open round-2 P0/P1 list from `bennett/HANDOFF.md` and `docs/reviews/2026-11-03-*.md` (unchanged
   content; this is where the queue runners stopped).
2. Red tests at HEAD: fix the cause or, where the test is for unimplemented promised behaviour, move it behind a
   named `slow`/`promised` switch with the bead named in the test, never delete it.
3. Fast/slow split: default `cargo test` under 180 s; slow tests get `#[ignore]` plus a `--ignored` run in `gate.toml`,
   or a `tests/slow/` binary the gate runs. `[profile.test] debug = "line-tables-only"`. Integration binaries merged
   where there are more than ten.
4. Coverage: one `cargo llvm-cov` (or `coverage.py`) run with the gate environment on the pinned siblings, number and
   command recorded in `docs/quality.md`; the five least-covered modules get tests or a reason.
5. Test quality pass over the files touched in items 1-2 and the auditor's "weak" list: tolerances tightened to what
   the oracle allows; string-grep and inequality-only checks replaced by executed or spec-derived checks; tests with
   no assertion given one or deleted; fixture sizes that cannot exercise the branch enlarged.
6. Function splits in files touched by items 1-2 and every function over 300 lines in semantics-bearing code
   (executors, lowering, checker, scheduler core, soft-float): named phases, each with a unit test, behaviour
   byte-identical (differential against the reference interpreter where one applies).
7. Fail-fast sweep: silent fallbacks found by the auditor (list per repo below) become errors with a test.
8. Litter: bead and job identifiers out of source, error strings and emitted output (test names and review docs may
   keep them); tracked pycache/logs/locks removed; README and SPEC_VERSIONS pins made true.

Per-repo specifics (from the audit; the job reads the full report first):

| job | repo | first items beyond the common list |
|---|---|---|
| quality-isaref | isa-spec reference-interpreter | fix qinplace:286 and r21:29 (§3.3); exclude the 23.8 GB test from the default run and give it a bounded fixture; merge 70 test binaries; split `source_constructor::oracle` (1089), `validate_action_sequence`, `action_sequence`, `step_prepared`; remove test-only no-op hooks from production (`main.rs:2414`, `lib.rs:158`) |
| quality-vm | vm | implement or remove `--mem-file` (memory_files.rs); `enum Op` parsed once at load; engine selection via `OnceLock`; JIT cache keyed by object hash; split `walk`, `body`, `exec_row`; `unwrap_or_default` at `cc.rs:2296` and siblings; coordinate with the bjm-dense branch: no splits in files that branch touches until it merges |
| quality-sched | sched | fix the `source_adjoint.rs:59` fixture so the two fdu tests fail for the right reason, then fdu; re-pin `docs/conformance-report.json`; split `lifted_regions` (310 s); split `source.rs::nodes` (745), `oracle.rs::build/row`, `expansion.rs::compile`; strengthen the four parse-only E vectors and `gate.rs`; brute-force differential for the peak/qubit-second sweep |
| quality-plugin | plugin | `Scalar.cpp:866` `.at()` abort becomes a diagnostic with a test; shared test harness `tests/contracts.py` and unminified drivers; string-grep tests replaced (`wide.py:59`, `integer_intrinsics.py:54`, `review_regressions.py:87`); gcov/llvm-cov build for one major; NO split of `Analysis::step` or `normaliseScalar` until rung4-plugin merges (that branch adds 3.9k lines to Analysis.cpp); 55 bead sites |
| quality-driver | driver | typed `Options` parsed once; `compare()` (574) and `execute()` (377) into stages; one differential for merged-module behaviour (`postlink.bc` under lli vs native) so a wrong merge is detectable without the blocked rung-2 fixture; red-by-design tests behind a named switch |
| quality-checker | conformance | fix `resource_contexts.rs:476` first (checker certifies too much); `cargo fmt`; split `check_replay_inner` (682), `exec_row`, `check_certificate`; mutation sweep mutates values (wrong hashes, shifted rows) not just types; tag tests with clause ids and feed `clausegraph.py coverage`; `fault.rs` (50 %) and CLI exit codes tested; 2.1 GB per test run of temp output cleaned |
| quality-estimate | estimate | `estimate.py:1121` catch-all removed; split `Source.classical`, `execute`, `action_nodes`; `coverage.py` number; derivation recorded for the 132 literal expectations (hand-derived or regenerated and marked as such); brute-force ledger as a third implementation for the summary path; bead IDs out of emitted output |
| quality-runtimes | runtimes | brt-mab (host write failure to exit 125); VLA in `integer_core.c` bounded; `free()` in `bump.c:86` loud; `tests/common.py` for the twenty `run()` copies; incremental build mode; xfail manifest for `eh_match`/`fiber_switch`/`poll`; a real host-libc differential for stdio and allocator (round 2 if large) |
| quality-arith | arith | exact rounding against the MPFR bracket in the five tolerance sites; directed-mode sweep (five modes, all `_rm` ops, tiny/large/near-1); ufr, 8eb, rn8 (`mulmod_const` k >= m); `softfloat/test_*.py` into the gate or deleted; `exact`-flag chain in `trans.h:246-256` to a per-op table; `trans_eval` into domain/core/pack |
| quality-dialect | dialect-spec tooling | unit tests into `gate.toml`; `validator/` stub deleted or filled and README made true; `dialect03_rehash.py` stops rewriting expected hashes in place (hand-pinned anchor subset); check report separates xref/parse/coverage from semantic counts; split `dialect_check.py` (3125); progress files untracked |
| quality-targets | targets | provenance test parses sidecars and asserts every JSON number appears; sidecars cite 0.9; one real Qualtran and one real Azure sample with source and date; `runtime.rs` unwraps to errors; locks and `.darc` untracked |
| quality-circuits | circuits | 14 assertion-free tests given assertions or deleted; QIR check fails loudly when `llvm-as` is missing; QASM and Quil validated by an external parser where one is installable, else the differential is named as the oracle; `differential.rs` hard-coded "2 spec examples" derived from the pin; split `history::evaluate_body` (1157); 43 bead sites |

Round 1 exit per repo: default test run green and under 180 s; coverage number recorded; Claude review document
with no open P0/P1 after at most two fix rounds; main merged and pushed.

## Round 2: oracle independence and the remaining structure

Started per repo when its round-1 review is CLEAR. Items that the auditors judged real but larger:
- runtimes: differential against a host-compiled musl/glibc build for stdio, printf, allocator behaviours.
- dialect: a second implementation (or the legality-corpus execution results) as an independent label source for
  the recognise/normalise verdicts; the 2943 count reported as semantic vs bookkeeping.
- estimate: ledger-vs-summary third implementation; the VM differential widened beyond classical-step fixtures.
- conformance: tests tagged by clause so the coverage number means tests; neutral suite clause ids counted.
- isa-spec: integration-coverage run so 0 % modules (`machine.rs`, `linking.rs`, `claims/replay09.rs`, ...) are
  classified dead or covered; dead 0.9 paths deleted.
- plugin: `Analysis::step` and `normaliseScalar` split after rung4-plugin merges, with Analysis.cpp in 2-3 TUs
  (the 107 s rebuild).
- vm: remaining functions over 300 lines; `bjm-dense` merged first.
- Everywhere: the remaining over-300-line list closed or each entry given an owner and a reason.

Round 2 exit: re-audit with the standing brief; targets table above met; the audit synthesis committed under
`docs/quality/<date>-audit/`.

## Round 3 (only if the re-audit says so)

Repos still below target get one more sol job scoped to the auditor's recommendations, then a final audit. Anything
open after that is a maintainer decision, not a fourth round (policy rule 3 applied to the programme).

## Execution

- Implementer: gpt-6.1-sol xhigh via `tools/codex_job.py` on branch `job/<name>` (after R0.1), under
  `systemd-run --user --scope` (`.tmp/orchestrator/resume_job.py`), `--network` where crates are needed. Briefs in
  `.tmp/orchestrator/briefs/quality-<repo>.md`: the per-repo audit report, the common list above, owned paths, the
  stop rule "this repo's default test run, not a consumer gate", and COMMON.md.
- Concurrency: at most five Rust jobs building at once (21 GB, 12 cores; isa-spec and vm count double), Python
  jobs unconstrained. Heavy gates (arith 8 h, vm dual-engine, ladder) only at bead close, one at a time (R3).
- Reviews: Sonnet bug-hunt review on every job's batch, Opus added for isaref, vm, sched, checker, plugin lowering,
  arith soft-float (policy rule 5 semantics-bearing). Muse not used (contracts unchanged). Review briefs from
  `s4/mkrev.py`.
- Orchestration: an Opus shift per the standing protocol (`.tmp/orchestrator/shift-N.md`); the advisor sets
  direction and spawns shifts; quota row before each launch; Claude kept within pace, Codex per the maintainer's
  2026-11-06 direction.
- Order of launch: R0.1 first (one job, about half a day), then R0.2 (five small jobs) and quality-arith,
  quality-checker, quality-estimate, quality-targets in parallel (they do not depend on branch mode beyond the
  runner itself); the large crates (isaref, vm, sched, plugin, driver, circuits, dialect, runtimes) as slots free.
- Rung-4 critical path (factored points-to on rung4-plugin, bp-6rz) is NOT paused: it runs as its own job on its
  branch; quality-plugin stays out of Analysis.cpp.

## Decisions needed from the maintainer

- D5: Codex jobs commit to `job/<name>` branches, never to main; the orchestrator merges after review (amends git
  policy 9 of 2026-10-29). Recommended: yes.
- D6: R17 (no Codex launch while Codex is at or ahead of linear pace) suspended for this programme; `--pace-margin`
  set so the guard still stops a runaway. Recommended: suspend until the round-2 audit, then reinstate.
- D7: dialect `validator/`: delete the stub and state that the validator is Python, or fund a Rust validator.
  Recommended: delete the stub now (no capability is lost; the Python checker is the validator); revisit when a
  consumer needs a linkable validator.
- D8: target grades as in the table (no repo below B on tests, B- on code). Confirm or change.
