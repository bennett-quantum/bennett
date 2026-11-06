# Quality audit brief (2026-11-05, read-only)

You audit ONE repository of the Bennett ecosystem (named in your task) and write ONE report to
`/home/tobias/Projects/bennett-workspace/bennett/.tmp/quality-audit-2026-11-05/<repo>.md`.
Nothing else is written anywhere. No commits, no beads, no edits to the repo. Treat every claim in the
repo's docs, HANDOFF.md, worklog and review documents as a claim to verify, not a fact.

The maintainer's questions, which your report must answer for this repo:
1. Code quality (real, not stylistic).
2. Test coverage: what fraction of the code the tests exercise, and which parts are untested.
3. Do the tests measure anything useful? (vs. tautological, self-oracle, "runs without error", snapshot-only,
   tests that duplicate the implementation's arithmetic, tests with trivial inputs only, ignored/red tests.)
4. Build times and test times.
5. Composition: what the repo is made of and how it is structured.

Context: `/home/tobias/Projects/bennett-workspace/bennett/README.md` (ecosystem), the repo's own README.md and
CLAUDE.md, `bennett/docs/decisions/2026-11-02-code-quality-policy.md` (rule 9 names the slop patterns to look for:
silent fallbacks, validation theatre, lonely interfaces, trivial wrappers and single-use helpers, duplicated cleanup
paths, flags where a state enum belongs, long &&/|| chains, bead/session references left in source, tracked WIP litter).
Existing review documents under `<repo>/docs/reviews/` tell you what was already found; do not repeat them, cite them.

## Hard rules
- Use absolute paths everywhere; never `cd`. Use `git -C <repo>` and `cargo --manifest-path`/`--target-dir` as needed.
- Headless: run every command with `env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER TMPDIR=<repo>/.tmp/audit-tmp`
  (create that dir). Never run LLVM `-view-*` passes.
- Resource budget (other auditors run in parallel on 12 cores / 21 GB): at most ONE cargo/cmake/make process at a time,
  `-j3` (`cargo build -j3`, `cargo test -j3`), and skip any single step that would exceed 10 minutes wall clock
  (use `timeout 600`). If a step is skipped, say so and why.
- NEVER run: `scripts/pre-push`, `gate_run*`, anything named gate/ladder/dual-engine/heavy, the full conformance or
  arith gates (hours), or any test the repo's docs flag as memory-hungry. If `cargo test` of the whole crate is known
  or likely to be heavy, run `cargo test --no-run` for timing and then a subset (e.g. `--lib`, or individual
  test binaries) under `timeout 600` and `ulimit -v 8000000`.
- Coverage: if `cargo llvm-cov --version` works, you may run `cargo llvm-cov --summary-only -j3` (same timeout/ulimit
  rules; use `--target-dir <repo>/.tmp/audit-cov-target` so you do not disturb the repo's incremental cache). If it is
  too heavy or unavailable, estimate coverage structurally: list public functions/modules and which test files reach
  them (grep), and say it is an estimate.
- Measure, don't guess: `cloc` is installed for LOC; `git -C <repo> log --format=%an%x09%s | sort | uniq -c` style
  queries for authorship mix (commits with `wip(codex job` or trailer `Agent: gpt-6.1-sol` are Codex-authored).
- Timings: report wall clock (`/usr/bin/time -f %e`) for: warm incremental build (touch one file), `cargo test --no-run`,
  and the test run you actually did. Note whether the existing target/ cache was warm.
- Read the real code. Pick the 3 largest/most central source files and the 3 largest test files and read them.
  Sample at least 15 individual test functions at random and classify each (useful / weak / tautological), with
  file:line, and say WHY in one clause.

## Report format (Markdown, concise, measured numbers in tables, file:line for every finding)
# <repo> quality audit 2026-11-05
## Verdict (5 lines max): overall quality grade A-F for code, tests, build; one sentence each.
## Composition: LOC table by language/dir (cloc), module map (one line per top-level module: purpose, LOC),
   dependency count (Cargo.lock crates / CMake deps / python imports), authorship mix (Codex vs Claude vs human, % of commits).
## Build and test times: table with the measurements above; number of tests; number ignored/skipped/red.
## Coverage: measured % (line/function) or structural estimate; the 5 largest untested or weakest-tested areas.
## Test quality: the 15+ sampled tests classified; the overall ratio; which tests are oracle-backed
   (spec conformance suite, differential against native/reference interpreter, exhaustive domains, property-based)
   vs self-referential; whether the gate (gate.toml, scripts/) would actually catch a wrong result.
## Code quality: top findings against policy rule 9 patterns and fail-fast, each with file:line and a one-line
   failure scenario or cost; complexity hotspots (longest functions, deepest nesting, measured by a quick script);
   duplication; dead code; WIP litter tracked in git.
## What is good: 3-5 specific things worth keeping.
## Recommendations: at most 7, ordered by value/cost, each one line.
Target length 150-300 lines. Numbers over adjectives. No praise padding.
