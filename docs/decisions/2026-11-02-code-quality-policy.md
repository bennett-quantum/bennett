# Code quality policy: required review and quality ratchets

**Status:** PROPOSED by the advisor on 2026-11-02 from the maintainer's instructions of 11:26Z; to be ratified by
the maintainer at the start of the next session, then adopted into every repo's CLAUDE.md (law 2) and into the
pinned-sibling gate (`tools/gate_run.py`). Nothing below is in force until ratified.

**Why now.** In the 48 hours to 2026-11-02 about 700 commits landed across the 13 repos and seven review documents
exist, none for plugin (161 commits), runtimes, driver, conformance, arith, circuits or targets; zero beads carry a
review label. Law 2 ("one implementer per change; review batched over accumulated diffs") names no trigger, no
reviewer, no bound and no exit, so review did not happen. The maintainer's words: "I do not want slop here."

## 1. Review is required

1. **Nothing reaches `main` unreviewed.** The unit of review is a *batch*: the diff between a repo's review mark
   (last reviewed sha, recorded in `docs/reviews/MARK` as `sha  date  reviewer  verdict`) and the candidate sha.
   Batching stays; the batch is bounded: the push gate refuses `main` when the unreviewed batch exceeds **25 commits
   or 2,000 changed lines of first-party code** (generated data, vendored code and fixtures excluded by the repo's
   `gate.toml`). Within the bound the orchestrator pushes green mains as today and schedules the review; past it the
   gate is the back pressure.
2. **Three rounds, then stop.** Round 1 reviews the batch. Round 2 re-reviews only the fixes to round-1 findings.
   Round 3 is final. A P0 or P1 still open after round 3 does not get a round 4: the batch is NOT CLEAR, the finding
   goes to the advisor (then the maintainer) as a decision, and the implementer may not keep iterating against the
   reviewer. This is the Zeno guard.
3. **Only P0 and P1 block.** P0: wrong result, silent fallback, spec violation, data loss, security. P1: a bug on a
   reachable path, a narrowing, a missing test for a claimed behaviour, a certificate or coverage claim that is not
   true. Everything else is a **nit**: filed as a bead with label `nit`, never discussed in-round, never a reason to
   withhold CLEAR. Nits are swept in a periodic cleanup bead per repo, not per change.
4. **Reviewers reproduce; they do not trust.** A review brief gives the reviewer the diff, the repo laws and the
   claims (tests run, gate exit, differential results). The reviewer re-runs what is cheap, reads what is not, and
   records exactly what it ran. A review that only reads is labelled `read-only` in its document.
5. **One review document per batch**: `docs/reviews/YYYY-MM-DD-<stream>-rN.md` with verdict CLEAR / NOT CLEAR,
   findings as `severity  file:line  claim  failure scenario  reproduction`, the commands run, and the beads filed.
   P0/P1 findings become beads labelled `review`; the MARK file moves only on CLEAR.

## 2. Who reviews: opposite model, stakes decide the seat

| Implementer | Default reviewer | Bug-hunt pass |
|---|---|---|
| Codex (gpt-6.1-sol, astra) | Claude: Opus for design, **Sonnet for bug hunting** | Sonnet |
| Claude (Opus, Sonnet) | **gpt-6.1-sol xhigh** (the best reviewer) | Sonnet, independently |
| Muse | sol xhigh | Sonnet |

Rules: the reviewer is never the implementer's model family; the reviewer is given the code, not the implementer's
conclusions, so it is not anchored; a Sonnet bug-hunt pass may run beside the main review and files only P0/P1.

**Stakes tiers** (by path, declared in each repo's `gate.toml`):

| Tier | What | Review seat | Example paths |
|---|---|---|---|
| T0 routine | tooling, docs, tests of existing behaviour, scripts | opposite-model review, 1 round expected | `scripts/`, `tools/`, `docs/` |
| T1 standard | ordinary implementation | opposite-model review + Sonnet bug hunt | most of `src/` |
| T2 high stakes | semantics-bearing code: executors, reference interpreter, plugin lowering and taint, checker, certificates, scheduler core, soft-float | T1 **plus one Muse call** on the round that claims CLEAR, quota-planned and advisor-confirmed per the Muse policy | `bennett-vm/src/{cc,action,oracle}.rs`, `reference-interpreter/`, `bennett-plugin/src/`, `checker/` |
| T3 highest | anything that changes a published contract or its tooling, the scheduling interface, certificate schema, launch ABI, the gate itself, security-adjacent work | **the council** (sol + astra + Muse once on the acceptance candidate), under the council README rules | `spec/`, `tools/gate_*`, `council.py`, ISA/dialect fixtures |

The three-round bound applies to every tier. T3 uses the council's existing fix-round rule (one reviewer re-grades).

## 3. Quality ratchets: measured, paired, "no worse than baseline"

Findings carried over from the maintainer's study "Code Quality Ratchets for AI Slop" (2026-10-31; SlopCodeBench
paper and `scb-check`, the *AI That Works* episode, and a pre-registered study of 287 master refactors in Lua,
SQLite, Redis and Git; study folder `~/.t3/scratch/2026-10-31-i-am-rather-stung-by-907efad9/excellence-study/`):

- **Prompts do not fix the trend; loops do.** An anti-slop prompt cut erosion by up to a third but quality still
  degraded at the same rate per step. Guidelines in CLAUDE.md are necessary, not sufficient: the ratchet lives in the
  gate. Codex runners do real work here, so the gate (not a Claude hook) is the only place every worker feels it.
- **Every quality gate needs a behaviour gate.** Quality prompting cost correctness in the benchmark (strict solve
  fell 2.4 points on average). Tests, conformance and differential checks stay primary; a ratchet never trades them.
- **Ratchet only "no worse than measured".** The limit is a measured number with its baseline commit as derivation,
  recorded in `gate.toml`; it only tightens. No invented budgets.
- **Pair every ratio with its counter-metric**, because ratios are gamed: erosion (complexity mass in functions
  above the threshold) with trivial-wrapper and single-use-function counts; verbosity with absolute flagged lines and
  total LOC; complexity mass, never mean complexity. Do not ratchet worst-function complexity blindly: a flat
  `switch` dispatcher (the VM step loop, the interpreter's opcode table) is legitimately large. Use **cognitive**
  complexity, which treats flat switches fairly, over cyclomatic.
- **Masters move complexity rather than remove it.** Shorter code and lower total complexity were coin flips at
  predicting a master's refactor; lower worst-function complexity was the only mechanical signal that worked. So a
  size ratchet pushes the wrong way; the design goal is fewer tangled functions, not fewer lines.
- **An LLM judge detects direction, not polish.** Blind, a judge picked the master's version 87.5% of the time and
  caught deliberate damage 90-100%, but preferred LLM "clean code" rewrites of real master code too often. Use the
  judge **head-to-head, old against new**, as a review aid for refactor batches; never as a score to chase and never
  as the only gate. The implementer never sees the judge's benchmark set.
- **Litter is read as culture.** Tracked WIP markdown, verifier scripts and dot-folders teach agents "how we work
  here". Progress files live under `.tmp/` (untracked); `docs/notes/` carries an index and every note names the bead
  or decision it serves; worker reports are not committed.
- **Named slop patterns to check in review** (from the 45 SlopCodeBench judge criteria, adapted to our laws): silent
  fallbacks (already banned by law 1), validation theater (checks that cannot fail or whose result is ignored),
  lonely interfaces (an abstraction with one implementer), trivial wrappers and single-use helpers, duplicated
  cleanup and reject paths, flags spread across state instead of an explicit state enum, long `&&`/`||` chains that
  data or a `match` should carry, `(void)`-style result discards, bead or session references left in source.
- **The eight moves** masters make, used as the vocabulary for P2 design findings and cleanup beads: turn a
  defensive check into an assert and delete the branch; change the representation so a special case disappears;
  give each rule one owner; separate mechanism from protocol; reduce what the reader has to track; name the idea;
  make the code read in one linear pass; delete honestly.

**Three tiers of "good", for Bennett:** (1) the mechanical floor above, ratcheted in the gate; (2) evidence of
rigour, where this project is already strongest: conformance against spec fixtures, differential testing of the two
executors against native, mutation score (`cargo mutants` is installed), assert density at pointer and invariant
preconditions; (3) craft, judged head-to-head in review. Tier 2 is what makes tier 1 refactors safe.

## 4. Tooling, per language in this workspace

| Language | Repos | Meter | Already installed |
|---|---|---|---|
| Rust | vm, sched, circuits, targets, driver, conformance, estimate | `cargo clippy -D warnings` (in gates), `clippy::cognitive_complexity` as a tracked warning, `scb-check` or `rust-code-analysis` for mass, `cargo mutants` for rigour | clippy, cargo-mutants |
| C / C++ | plugin, runtimes, arith, conformance fixtures | `clang-tidy readability-function-cognitive-complexity`, `cppcheck`, `lizard` for mass | clang-tidy, cppcheck |
| Python | plugin tests, arith, conformance, driver tooling | `scb-check` (erosion, verbosity, 197 AST-grep rules, waste counts), `ruff` | neither yet |
| clones, all | all | `jscpd` over `git archive HEAD` | not yet |

One deterministic `slop-meter` script in `bennett/tools/` runs over `git archive HEAD` of a repo (so worktrees and
`.tmp/` cannot distort it), writes one JSON per repo, and says what it could not measure. The gate tool reads the
baseline from `gate.toml` and fails with the function and file named.

## 5. Adoption order (first tasks of the next session, before new feature streams)

1. Maintainer ratifies or amends this document; the decision is recorded here with the date.
2. Baseline: run the meter read-only over all 12 code repos; record per-repo numbers and the ten worst hotspots
   per repo in `docs/reviews/BASELINE-2026-11.md`. No ratchet is enforced before a baseline exists.
3. Review debt: one batched review per repo of everything since the last review or since 2026-10-29, opposite
   model, in this order: plugin, runtimes, driver, conformance checker, vm (main), sched, estimate, arith, circuits,
   targets. Each writes its review document and MARK; P0/P1 become beads.
4. Law 2 rewritten in every CLAUDE.md to point here; `gate.toml` gains `review` (bound, tiers by path) and `quality`
   (baseline metrics) tables; `gate_run.py` enforces both.
5. Orchestrator briefs: every implementation stream's brief names its tier and its reviewer family; the orchestrator
   launches the review when a stream's batch closes, and never launches round 4.

## 6. What this does not do

It does not make review per change (law 2 stands), does not ratchet size or mean complexity, does not use an LLM
judge as a gate, does not touch the council process for specs, and does not start any refactoring stream on its
own: cleanup is beads, pulled at a pace the orchestrator sets under the advisor.
