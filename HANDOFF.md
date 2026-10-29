# HANDOFF — Bennett ecosystem (bennett-quantum)

**Read this first in any new session.** Date: 2026-10-28. Workspace:
`~/Projects/bennett-workspace/` (13 repos, each cloned from
`github.com/bennett-quantum/<name>`, all on `main`, all pushed, all
clean). Bennett.jl v1 at `~/Projects/Bennett.jl` is the deprecated
reference implementation and differential oracle; its worklog chunks
121–123 hold the reboot's history up to this point.

## State in one table

| Repo | State | Next concrete step |
|---|---|---|
| `bennett` (this) | north star (consensus), council runner + rubrics + all 14 graded rounds, manifest | run the council on the dialect spec when a draft exists; `bd init` when code lands |
| `bennett-isa-spec` | **spec 0.8 council-accepted**; `isa_check.py` = Python seed of the reference interpreter; Rust crates empty | port `isa_check.py` row by row to Rust (red-green on the two example objects); suite B then C; file the round-8 suggestions as issues |
| `bennett-dialect-spec` | skeleton; **no draft** | north star §9 item 1: **legality spike before any text** (marker corpus vs every stock pass at O3 + native codegen; emission examples from clang, rustc, Julia); then draft `spec/` from north star §3 and take it through the council with `rubric-isa.md` |
| `bennett-sched`, `-vm`, `-circuits`, `-plugin`, `-driver`, `-estimate`, `-targets`, `-runtimes`, `-arith`, `-conformance` | skeletons (LICENSE, CLAUDE.md, pre-push hook, one passing Rust test where applicable) | blocked on the dialect spec for plugin/driver; `-vm` and `-circuits` can start from the ISA spec now (§3–§7, §14, §16 are the accepted core) |

Nothing is implemented anywhere. The maintainer's process rule stands:
vision (done) → design (ISA done; dialect next) → spikes → code.

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
value proposition). The legality spike is done
(`../bennett-dialect-spec/docs/spikes/2026-10-28-legality-findings.md`); dialect draft
0.1 exists but is under audit for narrowings and is not for the council. The items
below predate the plan; the plan's phase order supersedes them where they conflict.

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
