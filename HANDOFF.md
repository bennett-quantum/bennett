# HANDOFF — Bennett ecosystem (bennett-quantum)

**Read this first in any new session.** Date: 2026-10-28. Workspace:
`~/Projects/bennett-workspace/` (13 repos, each cloned from
`github.com/bennett-quantum/<name>`, all on `main`, all pushed, all
clean). Bennett.jl v1 at `~/Projects/Bennett.jl` is the deprecated
reference implementation and differential oracle; its worklog chunks
121–123 hold the reboot's history up to this point.

**Orchestrator session block (2026-10-30 05:50Z, written for a successor session).** Operating rules: Claude usage minimal; all
implementation on codex `gpt-6.1-sol` xhigh via T3 Code `delegate_task`; muse `muse-wonder-full-1.0` reviews specs only
(dialect rounds, ISA 0.9 council) until its usage reset; interpreter rounds run with sol + codex (`gpt-6-astra`); keep
Codex weekly PACE (the `quota` CLI) within +3% of linear; commit after every verified milestone and push (the ISA repo's
pre-push gate tests the working tree, so push only when reference-interpreter/ is clean); `BEADS_HOOK_TIMEOUT=20` for
git commits; every job gets a brief with owned paths and a progress file, commits its own paths, never pushes; the
orchestrator verifies test counts itself and writes the worklog entries. Council loop per stream: collect each seat's
JSON with `tools/council.py collect`, `aggregate`, commit, push; no consensus → one sol editor (dialect: spec + checker
together; interpreter: the crate) with a response file → next round prepared with the precheck gate (dialect) or a
fresh detached worktree + `tools/review_packet.py` (interpreter; `--no-diff` when the diff is large; tell muse to read
the prompt in bounded slices). Streams and their state: **interpreter** round 5 aggregated (muse accept; sol/codex
revise, 7 blockers; mean 4.08), first fix pass pushed (71c1d6e, 253 tests), second pass (codex's 3) running; then freeze
round 6 and launch sol + codex. **dialect** round 4 aggregated (all revise, 5 blockers, mean 4.08), round-4 editor
running (spec + checker); then gate, push, round 5 with sol + codex + muse. **VM** at the 0.8 frontier (849f7f7, 101
tests, conformance parity); nothing to do until 0.9 or a sibling repo. **circuits** M2 closed by disposition (design
note), M3 placement running. **targets** M1 running (brief docs/briefs/2026-10-30-targets-milestone-1.md). **ISA repo**
0.9-draft mirror of VM beads hsd/clw running. Hold: bennett-estimate (needs hsd contracts), bennett-sched (needs the §11
library), plugin/driver (dialect acceptance). Running T3 child task IDs at 05:50Z (poll with `task_status` from a new
session; completion notices go to the launching thread only): interpreter second pass
`node:delegated-task:command%3Amcp%3Ac1e0be84-52fa-4cb7-9840-049cfe011045%3Adelegate-task%3Af1c0cc7d-935f-4a79-befc-469566b53f56`;
dialect round-4 editor `...%3Adelegate-task%3Ac25f1868-87cf-4156-8ceb-c1e5b9d8b47f`; circuits M3
`...%3Adelegate-task%3Ab097153b-9aa3-4627-9355-5a5833b76aff`; ISA 0.9 mirror
`...%3Adelegate-task%3A3ffa2f10-a3de-4b2b-90ab-0579f2565e1a`; targets M1
`...%3Adelegate-task%3Ad17390e5-095a-4846-96fa-1e628c4a2ef6` (prefix identical to the first id). Known failure modes:
muse network drops / quota 429 / OOM on >1.4 MB prompts (retry once, then close the round without it); T3 "workspace
routing discovery timed out" kills every child (relaunch from committed state + progress file); the beads pre-commit
hook can stall 300 s.

**Maintainer decisions pending (orchestrator, 2026-10-29 evening, unattended run):**
- **ISA §11 reference library `ref` (bennett-vm-47t).** ISA 0.8 §11/§17 name the library the ISA repository "publishes" but define neither its serialization, hash rule, ordinals nor gate decompositions. Nothing was invented for 0.8: a sol agent is drafting the contract into `../bennett-isa-spec/spec/Bennett-ISA-Spec-0.9-draft.md` (item ISA-REF-LIB) with the decision points stated in the mirrored bead. VM scheduled execution and the suite-E/G schedule cases stay `unavailable` until 0.9 is accepted. Decide: the decomposition set and the hash rule.
- **Circuits M2 proof contracts (bennett-circuits, 2026-10-30).** `docs/design/2026-10-30-m2-open-proofs.md` in that repo: two design choices (proof-IR / action-CFG representation, bead 7bu; opaque workspace proof summaries, z9r) and three ISA 0.9 publication items (certificate replay tuple encoding 4pf, frame schema JSON encoding 4fa, operation-identity publication for §6.4 recompute matching yz8, the last depending on the §11 library). Each states the alternatives and costs; the specialiser refuses those paths with the bead id until decided.
- **Q14 reading** (lproc token/classical params) applied to the 0.9 draft from the worklog wording; overrule if wrong.
- **Council seats:** sol (gpt-6.1-sol) substitutes for opus/fable; muse is council-only; isa-ref rounds 2-3 closed with two seats after the muse provider outage, muse rejoined at round 4.

## State in one table

| Repo | State | Next concrete step |
|---|---|---|
| `bennett` (this) | north star (consensus; amendments A1, A2 pending), council runner + rubrics (narrowing = S0), plan `docs/plan/2026-10-29-path-to-north-star.md`, `tools/codex_job.py`, bd | see "Open items" below |
| `bennett-isa-spec` | spec 0.8 council-accepted, settled until dialect 0.2 is accepted; Rust reference interpreter in progress (codex job stopped, resumable; `wip/isa-ref-interpreter`) | resume the interpreter job (its HANDOFF has the command); then CLI b-isa-spec-xam; ISA 0.9 after dialect acceptance |
| `bennett-dialect-spec` | legality spike done; draft 0.1 rejected (narrowings); SQLite rung-4 spike done (no ISA change); 0.2 outline ratified | write 0.2 full text (brief in `docs/briefs/`), extend the precheck, council |
| `bennett-sched`, `-vm`, `-circuits`, `-plugin`, `-driver`, `-estimate`, `-targets`, `-runtimes`, `-arith`, `-conformance` | skeletons (LICENSE, CLAUDE.md, pre-push hook, one passing Rust test where applicable) | blocked on the dialect spec for plugin/driver; `-vm` and `-circuits` can start from the ISA spec now (§3–§7, §14, §16 are the accepted core) |

Nothing in the toolchain is implemented yet (spike harnesses and the reference interpreter aside). Process: vision (done) → design (ISA 0.8 done; dialect 0.2 in progress) → spikes → code.

## Documents and their status

- `docs/Bennett-NorthStar.md`, iteration 7. Council consensus 2026-10-28
  (round 6, all accept, mean 4.46). Settled; change only for a reason
  that would survive the council.
- `../bennett-isa-spec/spec/Bennett-ISA-Spec.md`, draft 0.8. Council
  **accepted** 2026-10-28 (round 8, all accept, no blockers, mean 4.17;
  core consensus from round 7). Trajectory 2.12 → 2.83 → 3.04 → 2.83 →
  3.12 → 3.92 → 4.12 → 4.17 over eight rounds in one day. Change rules in
  `../bennett-isa-spec/spec/README.md`: surgical edits; any semantic
  change bumps the full version string and the four example hashes
  (`isa_check.py --repatch`); new examples go into the checker before
  grading; §17 holds every deferred decision with its default; revisions
  go back through the council.
- Council records: `docs/council/northstar-2026-10-28/round-{1..6}/` and
  `docs/council/isa-2026-10-28/round-{1..8}/`, each with `report.md`,
  `out-<member>.json`, the editor's `response.md`, the prompt and the
  document snapshot. Process: `docs/council/README.md`.

## How to run a council round (from this repo)

```
python3 tools/council.py selftest
# precheck for the ISA: python3 ../bennett-isa-spec/reference-interpreter/isa_check.py
# (the dialect spec has no precheck yet: write one that executes its examples before round 1)
python3 tools/council.py prepare --run <run> --round N --doc <path> \
    --rubric docs/council/rubric-isa.md --context docs/Bennett-NorthStar.md \
    --subject "<one phrase>" [--precheck "<cmd that must exit 0>"]
python3 tools/council.py run --run <run> --round N --timeout 3600 --attempts 6
python3 tools/council.py aggregate --run <run> --round N   # -> round-N/report.md, consensus.json
```

Members: codex `gpt-6-astra` xhigh (8–31 min), muse `muse-wonder-full-1.0`
(2–9 min), Claude Opus via nested `claude -p` (2–6 min). Zero retries in
14 rounds. Gotchas: codex blocks forever unless stdin is the prompt or
closed; `--allowedTools` is variadic and swallows a trailing prompt arg;
the runner unsets `CLAUDECODE*` for the nested claude. Members read the
repo read-only from cwd = this repo, so reference a document in another
repo by relative path (`../bennett-isa-spec/spec/...`); the document is
embedded verbatim in the prompt regardless. State is written to
`docs/council/<run>/round-N/` atomically; `run` is safe to re-invoke and
`--member X` resumes one member.

What made the ISA rounds converge (apply to the dialect spec):
S0-only blocking with core/contract scope; literal, printed inverse
lists instead of grouped prose; sketched mechanisms replaced by a
stated default and a deferral (§17); a pre-flight that executes every
example and stated result before anyone grades it. Every rewrite
introduced a mechanical error; every editor-invented numerical rule was
caught by the council within a round. Write derivations out first.

## Open items, in order

**Start here (2026-10-29): `docs/plan/2026-10-29-path-to-north-star.md`** — the plan to
the north star, its real blockers (R1–R6), phases 0–6, and the standing rule that **no
narrowing of north-star scope is accepted** (Grover over unmodified SQLite is the core
value proposition). The items below predate the plan; the plan's phase order
supersedes them where they conflict.

**State at 2026-10-29 afternoon (second session, wound up by the maintainer; see the three repos' HANDOFFs for detail):**
- **Reference interpreter**: council run `docs/council/isa-ref-2026-10-29` round 1 (fable/astra/muse, `rubric-impl.md`, `task-impl.md`,
  `tools/review_packet.py`, worktree `../bennett-isa-spec-review`): 30 blockers, no consensus. Opus implementer reached milestone 1
  at `bennett-isa-spec` e8629de (all 30 resolved/declined/staged; 152 tests + 5 sweeps green). **Round 2 not run**: instructions in
  `../bennett-isa-spec/HANDOFF.md`. The codex interpreter job is stopped for good.
- **Dialect 0.2**: full text written (`../bennett-dialect-spec`, ac32fa7, 7,341 lines). Council run `docs/council/dialect-2026-10-29`
  round 1 DONE (`task-spec.md`, `rubric-isa.md`): no consensus, all three revise, 32 blockers (fable 6, astra 22, muse 4), mean 3.21;
  `round-1/report.md`. Next: an Opus editor fixes them with a response file (`round-1/response.md`), then round 2.
  The 0.2 pre-flight checker (codex job dialect-check-0.2) is checkpointed and resumable (that repo's HANDOFF).
- **ISA 0.9**: evidence note done (no rung blocked at fixed widths); **draft 0.9 written alongside 0.8** (`../bennett-isa-spec/spec/
  Bennett-ISA-Spec-0.9-draft.md`, 9861107); maintainer accepted all open questions Q1-Q14; the Q14 edit (lproc token/classical
  params) is still to be made. Grading gate: interpreter accepted AND dialect round 1 done.
- Council tooling: `fable` member, `--members`, `--task`, `--cwd` (see worklog). Pace at wind-up: Claude weekly +5% ahead of linear.

**State at 2026-10-29 morning (session ended by the maintainer; everything committed and pushed):**
- Phase 0 (narrowing audit of dialect 0.1) and phase 2 (SQLite: **rung 4 feasible on ISA 0.8
  with no ISA change**, `../bennett-dialect-spec/docs/spikes/sqlite/REPORT.md`) are done.
- Phase 1 (full Rust ISA reference interpreter): codex job **stopped** after attempt 2, all seven
  deliverables partial with green tests at the last checkpoint. Resume command and state in
  `../bennett-isa-spec/HANDOFF.md`; at session end tests were green and main (98f9c20) is pushed;
  `wip/isa-ref-interpreter` points at the same commit. Follow-up: CLI commands b-isa-spec-xam.
- Phase 3: dialect 0.2 outline **ratified** (`../bennett-dialect-spec/spec/outline-0.2.md`, rulings at
  its end: E1–E14 ratified, riscv64 platform). The full-text agent was stopped before writing;
  its brief is `../bennett-dialect-spec/docs/briefs/2026-10-29-dialect-0.2-fulltext.md`. Then extend
  `scripts/dialect_check.py` to every 0.2 example against the Rust interpreter; then **council rounds
  on dialect 0.2** (rubric-isa.md now makes any narrowing S0).
- **ISA 0.9 (revised 2026-10-29):** evidence note done (`../bennett-isa-spec/docs/notes/2026-10-29-isa-09-evidence.md`:
  no rung blocked at fixed widths; BLK-1..4, ISA-7, ISA-8 and the zero fault code are real gaps against the north
  star). Maintainer: **draft 0.9 now alongside 0.8** (`../bennett-isa-spec/spec/Bennett-ISA-Spec-0.9-draft.md`, Opus,
  brief `docs/briefs/2026-10-29-isa-09-draft.md`); **grade only after** the reference interpreter is council-accepted
  and dialect 0.2 has had round 1. Dialect 0.2 stays graded against 0.8 with `blocked:` verdicts.
- **Reference interpreter under council review** (run `docs/council/isa-ref-2026-10-29`, members fable/astra/muse,
  rubric `docs/council/rubric-impl.md`, `tools/review_packet.py` + a detached worktree per round): round 1 no
  consensus (30 blockers); Opus is the sole implementer (`../bennett-isa-spec/docs/briefs/2026-10-29-isa-ref-council-fixes.md`);
  loop until all three accept.
- Codex jobs: always via `tools/codex_job.py` (resume after refusals / network drops, pace check,
  commits every 20 min, wip-branch backup, headless). No Daybreak access: assume refusals.
- Issues live in bd in this repo, `bennett-dialect-spec` and `bennett-isa-spec` (`bd ready`).

0. **Read `../bennett-isa-spec/docs/notes/2026-10-28-budgets-loops-variable-time.md`** before touching budgets, loops or the step machine: the two Collatz problems (R-tier per-input trace vs Q-tier one circuit), the wrapper pattern, and the reading of Jeffery et al. arXiv:2605.07518 (loop composition, variable-time search). It files open items I1–I8 in bennett-isa-spec's worklog; I5 (idle steps as identities) and I1 (pebbled realisations) are the first candidates for an ISA 0.9 council round.
1. **Legality spike** (dialect): the gate on freezing the dialect spec.
   Build the marker corpus in `bennett-dialect-spec/corpus/`, run it
   through every stock LLVM pass at O3 and native codegen, record what
   survives; collect emission examples from clang, rustc and Julia.
2. **Dialect spec draft** from north star §3, through the council.
3. **`bennett-isa-spec`**: Rust reference interpreter from `isa_check.py`;
   suites B and C; C headers of §10/§11 compiled once (never done); file
   the 16 round-8 suggestions (codex 5, muse 5, opus 6; `docs/council/isa-2026-10-28/round-8/out-*.json`, field `suggestions`)
   as the repo's first issues.
4. **`bd init`** in each repo when its first code lands (CLAUDE.md rule
   7); until then open items live in HANDOFF/worklog.
5. **Bennett.jl**: `v1` branch / `v1-final` tag when Bennett.jl v2 (the
   Julia quantum language) starts in that repo; BennettVM.jl archive
   read-only when the maintainer says so; `bd dolt push --force` for the
   flattened beads history (maintainer); bead v4iy (ULP wording) pending.
6. North star §7 landscape: **amendment A1 drafted** (`docs/council/northstar-amendments/A1-…md`): sourced comparison on control flow under one budget, clause (e) in "What is new", one §4.2 sentence. Apply surgically as iteration 8 and run `northstar-2026-10-28` round 7 when the maintainer says go.

## Facts worth not re-deriving

- `bennett-lang` on GitHub is not ours; ignore it. Orgs are web-only;
  `gh repo create bennett-quantum/<repo>` works with `repo` scope.
- Basis-state differential testing plus clean ancillae is complete for
  the exact-permutation tier (ISA T3); phase matters only for ε > 0.
- "Equals native" determinism: deterministic soft-float in both builds
  plus a driver-controlled layout; `freeze` is not deterministic; do not
  reopen without a new counterexample.
- The ISA's segment `uncall` is restricted (pure suffix, no `measure`
  inside) rather than checked; MBU is deferred (§17 item 6); schedules
  bind an expansion library (`ref` default) rather than carrying the
  realised gate graph. Each was the lighter of two council-approved
  alternatives; revisit when a scheduler or a cleanup certificate exists.

See `worklog/001_2026-10-28_bootstrap.md` for the session log.
