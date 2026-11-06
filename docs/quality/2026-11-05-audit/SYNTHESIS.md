# Bennett ecosystem quality audit, synthesis (2026-11-05, advisor)

Source: 13 per-repo reports (12 repos + meta) in this directory (Sonnet auditors, Haiku for targets + meta), read-only, heavy gates not run.
Grades are the auditors'; numbers are measured unless marked estimate.

## Scorecard

| repo | code | tests | build | red at HEAD | measured coverage | notable |
|---|---|---|---|---|---|---|
| isa-spec (ref. interpreter) | C+ | B- | C | 2 tests (qinplace:286, r21:29) | 42.6% line, --lib only (floor) | HEAD is a Codex WIP commit; 70 test bins x 110 MB; gate runs the 23.8 GB OOM test |
| vm | C+ | B- | C | 2/3 in memory_files.rs (WIP, no impl) | none | 73 fns >100 lines; op dispatch on strings; env var read per arithmetic op |
| sched | C+ | B | C | 3 (2 mid-TDD fixture bug, 1 stale pin) | none | source.rs 2277 lines, nodes() ~745; full test 550 s, one binary 310 s |
| plugin | C- | B- | C | 2 of 6 run (1 drift, 1 `.at()` abort Scalar.cpp:866) | none | Analysis.cpp touch = 107 s per LLVM major; step() 528 lines |
| driver | C+ | C | A- | 9/28 binaries (7 sibling drift, 2 red by design) | none | compare() 574 lines; silent sibling-path defaults; 10-min suite |
| conformance | C+ | B- | B | 1 (checker certifies a cleanup it should not, resource_contexts.rs:476) | 83.4% line (checker) | ~75 negative tests; clause coverage 36% = proofs only, tests untagged |
| circuits | C+ | B | B- | 0 | 84.9% line (oracles bin excluded) | 11 test files read the live sibling; QASM/Quil validated only by own parser; QIR check skips silently if llvm-as missing; evaluate_body ~1157 lines |
| estimate | C+ | B | A (meaningless) | 0 | none (Python) | "Rust crate" is a 56-line launcher; estimate.py 4742 lines, one 1630-line class |
| runtimes | B- | B | B+ | 0 | none | byte-reproducible build; "native differential" compares against a self-written twin |
| arith | C- | C+ | B | 3 (K91 drift) | none | 280k assertions at 1-4 ulp cannot see a wrong rounding side; ufr/8eb reproduce at HEAD |
| dialect-spec tooling | C+ | B- | C | 0 | none | "2943 checks" ~80% xref/parse bookkeeping, ~470 semantic; labels are spec prose by the same agent; rehash tool is circular |
| targets | B | B- | n/a | 0 | none | importer fixtures all hand-written; sidecars cite ISA 0.8 |
| meta tools | C | C- | n/a | 0 | 86% council.py (trace) | installed pre-push hook is a no-op; codex pace guard fails open; codex_job/review_packet untested |

Test sampling across repos: ~210 tests classified by hand; roughly 65% useful, 30% weak, <5% tautological.

## What the tests actually measure

Good, and worth protecting: the oracle layer is real. The ISA reference interpreter, published conformance cases,
exhaustive small-domain sweeps with hand-derived expectations, a Fraction/MPFR oracle (arith test_edge), an
independent simulator for circuit tests, a Python big-int oracle for 217k runtime integer cases, byte-diffs against
the reference interpreter (vm), and ~75 negative certificate tests (conformance). Spec-conformance tests are present
in sched, vm, targets, plugin and conformance. No repo has only self-referential tests.

Weak, in order of consequence:
1. Tolerances that blind a test to the bug class it names: arith transcendental tests accept 1-4 ulp although the
   observed max error is 0.5000 ulp; the two open P0s pass all 280k assertions. Directed modes checked at one point.
2. Oracles that are the author's own reading: runtimes "native" side is src/native/heap.c (self-authored twin, not host
   libc); dialect recognise/normalise labels are spec annotations written by the same agent; dialect03_rehash.py
   rewrites expected interface_hash values from the interpreter under test; estimate's ~132 literal expectations have
   no recorded derivation (hand or copied from output).
3. Inflated headline counts: dialect 2943/2943 is mostly cross-ref and parse checks; conformance 36% clause coverage
   counts proofs, no test is tagged; driver's only wrong-merge detector (frozen rung-2 fixture) cannot run.
4. Weak structural checks: string-grep/inequality-only tests in plugin, parse-only "E" vectors in sched (4),
   mutation sweep in conformance replaces fields with null/true, never plausible wrong values; targets importer tests
   against hand-written fixtures only.

## Why mains are red (7 of 11 code repos)

Two root causes, not seven:
- Codex "wip(codex job ...)" attempt-end checkpoints land on main (isa-spec HEAD, vm memory_files.rs with no
  implementation, sched mid-TDD). Codex WIP is 23-62% of commits per repo.
- Tests read the live sibling checkout instead of the gate pin (driver: 7 binaries; arith: 3 K91 failures; plugin
  contract_policy; sched conformance_inventory 536 vs 557; circuits still reads the live sibling in 11 files, d2fd693 made it tolerant, not pinned).
Plus one real regression: conformance checker grants `verified` where the test expects `unchecked` (resource_contexts.rs:476).

## Build and test times

| repo | incremental build | test --no-run | full/sampled test |
|---|---|---|---|
| isa-spec | 62 s (--no-run after touch) | 187 s cold-ish | --lib 109 s; metadata bin 219 s; full suite = OOM hazard |
| sched | 76 s | 283 s | 550 s (lifted_regions 310 s) |
| vm | 37 s | 166 s | --lib 112 s; oracle_cleanup09 >300 s; dual-engine = hours |
| plugin | 6.7 s (Memory.cpp) / 107 s per major (Analysis.cpp) | n/a | 48 python drivers, unmeasured as a whole |
| driver | 2.5 s | 12.7 s | ~600 s (arith_instances 274 s) |
| conformance checker | 5.5 s | 106 s cold | 167 s; python suites 4-38 s |
| circuits | 12 s (--no-run) / 32 s build | 313 s cold | 200 tests pass; oracles bin needs 6.75 GB |
| runtimes | none (always full, 59 s/major) | n/a | 2.5-279 s per script |
| arith | 54-85 s per major, no cache | n/a | 0.3-163 s per file; full gate ~8 h |
| dialect | n/a | n/a | v02 gate 572 s; unit tests 177 s (not in gate) |
| estimate | 1.1 s cold | 0.9 s | ~180 s (Python) |
Machine was loaded (load 17-20) during most measurements; treat as upper bounds.
Debug test binaries at 110 MB x 70 (isa-spec) are the single largest build-time sink; the per-crate "whole suite in
one gate" pattern makes the ordinary `cargo test` loop unusable in isa-spec, sched, vm and driver.

## Composition and structure

- Rust crates have zero or near-zero third-party dependencies (good; also means everything is hand-rolled).
- God functions are the norm: 1157 (circuits history::evaluate_body), 1089 (isa source_constructor::oracle), ~745 (sched nodes), 682 (conformance
  check_replay_inner), 602 (vm), 574 (driver compare), 528/499 (plugin step/normaliseScalar), 250-460 (estimate.py),
  295 (dialect run.py). 43-73 functions over 100 lines per large crate.
- Composition misrepresentations: estimate's Rust is a launcher for 4.7k lines of Python; dialect validator/ is an
  11-line stub with a tautological test and reference-interpreter/ is an empty dir; targets importers have no real
  external samples.
- Litter and provenance: tracked __pycache__/.pyc in isa-spec, conformance, arith, estimate; tracked logs, locks,
  .darc backups, LAST-RUN/PROGRESS files; bead IDs in source comments, error strings and emitted product output in
  at least six repos; READMEs stale on the accepted dialect version in plugin, driver, runtimes.
- Fail-fast violations found: estimate.py:1121 catch-all returns False; bump.c:86 free() returns silently on unknown
  pointer; vm unwrap_or_default (cc.rs:2296); driver unwrap_or(ws.join(..)) sibling defaults; runtimes failed host
  write reported as dialect fault 8; codex_job.py pace guard returns None and proceeds.

## Recommendations, ecosystem level, by value over cost

1. Keep Codex attempt-end checkpoints off main: run queue jobs on a branch (they already back up to wip/<job>) and
   merge only after the review round; or reject `wip(` commits in the pre-push gate. Fixes the main cause of red mains.
2. Pin discipline: any test that reaches a sibling repo reads the gate.toml pin and fails with one message naming
   the pin when the sibling differs. Driver, arith, plugin, sched, circuits today.
3. Arith: exact rounding comparison against the MPFR bracket (one function) plus a directed-mode sweep. Catches two
   open P0s immediately.
4. Fast/slow split in every Rust crate so default `cargo test` is under ~3 min; `[profile.test] debug = "line-tables-only"`;
   merge isa-spec's 70 test binaries. This is the only build-time fix with ecosystem-wide payoff.
5. One measured coverage baseline per crate (cargo llvm-cov on a quiet machine, Python coverage for estimate/dialect/arith),
   recorded as a number in the repo, no dashboard (policy rule 8).
6. Independent oracles where the oracle is self-authored: runtimes vs host libc build; dialect labels vs a second
   implementation or the legality-corpus execution results; estimate summary vs a brute-force ledger; conformance
   mutation sweep with plausible wrong values; targets importers vs one real sample each.
7. Split the god functions as part of each repo's round-2 fixes (same implementer, same review), not as a campaign.
8. Meta one-liners: install the real pre-push template; make the pace guard fail closed; untrack pycache/logs/locks.
