# The council

A loop in which three models grade a document against
`docs/council/rubric.md`, the maintainer's editor
revises the document on their blocking issues, and the loop repeats until
every member accepts, or three rounds have run. The loop shape is borrowed
from the `council` skill in t3dotgg/tstack ("gets review from three models
from different providers, and loops until they agree") and from the design
council in `../sublimite/docs/design/council.md`. The rubric and the
resumable runner are ours.

Scores are advisory. The maintainer decides.

## Members

| Member | Call | Notes |
|---|---|---|
| Sol (`sol`) `gpt-6.1-sol`, reasoning `xhigh` | `codex exec -m gpt-6.1-sol -c model_reasoning_effort=xhigh -s read-only --ephemeral --output-schema … -o …` | Substitutes for the Opus/Fable seat in the current council. Same CLI construction as `codex`; the prompt goes on stdin. |
| Codex (`codex`) `gpt-6-astra`, reasoning `xhigh` | `codex exec -m gpt-6-astra -c model_reasoning_effort=xhigh -s read-only --ephemeral --output-schema … -o …` | The runner sends the prompt on stdin and closes it. Run from the repo so the read-only sandbox can read it. |
| Muse `muse-wonder-full-1.0`, reasoning `high` | `muse exec --model muse-wonder-full-1.0 --reasoning-effort high --output-schema … --prompt-file …` | Prints status lines before the JSON; the runner takes the last JSON object. |
| Claude Opus 5.5 (`opus`, legacy) | `claude -p --model opus --output-format json --json-schema … --allowedTools Read Grep Glob` with the prompt on stdin | Nested inside a Claude Code session, so the runner unsets `CLAUDECODE*` in the child's environment. The prompt goes on stdin because `--allowedTools` is variadic and swallows a trailing prompt argument. |
| Claude Fable (`fable`, legacy) | `claude -p --model fable --output-format json --json-schema … --allowedTools …` with the prompt on stdin | Also permits the existing implementation-review test commands. |

Each member may read the repository (read-only) to check the document's
claims; the document itself is embedded verbatim in the prompt so a member
that reads nothing still grades the right text.

### Members run as T3 subagents

The current council is `sol,codex,muse`. An orchestrator launches one T3 Code
subagent per member using the model and reasoning effort above. `council.py`
prepares and collects their work; the orchestrator does not invoke `run`.
The CLI calls in the table remain available for legacy subprocess rounds;
the default member list is unchanged, so pass `--members sol,codex,muse`.

Use this sequence (set `repo` to the absolute checkout path):

```sh
repo=/absolute/path/to/bennett
mkdir -p "$repo/.tmp"
unset DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER
export TMPDIR="$repo/.tmp"
python3 "$repo/tools/council.py" prepare --run external-review --round 1 \
        --doc "$repo/docs/Bennett-NorthStar.md" --members sol,codex,muse --cwd "$repo"
python3 "$repo/tools/council.py" prompt-path --run external-review --round 1
# Line 1 is the absolute prompt.md path; line 2 is the subagents' cwd.
# Orchestrator: launch one T3 Code subagent each for sol, codex and muse.
# Give each prompt.md and the adjacent schema.json, using the printed cwd.
# Tell each to review read-only and write only its JSON result to its own file:
# sol -> $TMPDIR/sol.json; codex -> $TMPDIR/codex.json; muse -> $TMPDIR/muse.json.
# Wait for all three files, then collect sequentially:
python3 "$repo/tools/council.py" collect --run external-review --round 1 --member sol --file "$TMPDIR/sol.json"
python3 "$repo/tools/council.py" collect --run external-review --round 1 --member codex --file "$TMPDIR/codex.json"
python3 "$repo/tools/council.py" collect --run external-review --round 1 --member muse --file "$TMPDIR/muse.json"
python3 "$repo/tools/council.py" aggregate --run external-review --round 1
```

`collect` uses the same output parser and validation as `run`, including the
round's saved `schema.json`. Each collection records `raw-<member>-<attempt>.txt`
with an external-source note, atomically publishes valid `out-<member>.json`,
and updates `state.json` (start time from the source file's mtime, elapsed
seconds to collection, update time now). Invalid input fails loudly and is
recorded as a failed attempt; any previously valid output remains intact.

## Resumability

Everything lives under `docs/council/<run>/round-<N>/` inside the
repository, never in a session-scoped temp directory, so a crashed Claude
session, a dropped network, or a provider capacity failure loses nothing:

- `prepare` snapshots the document (`doc.md` plus its SHA-256 in
  `state.json`), writes `prompt.md` and `schema.json`. Re-running `prepare`
  on a round that already has member output refuses unless `--force`.
- `run` launches every member that has no valid `out-<member>.json`, in
  parallel, each with a wall-clock timeout, retrying on failure with
  backoff (60 s, 180 s, 420 s) up to four attempts. Every attempt's stdout
  and stderr are kept (`raw-<member>-<attempt>.txt`). Output is validated
  against the schema before it counts; an invalid answer is a failed
  attempt. `state.json` is rewritten atomically after every state change,
  so `status` always tells the truth and `run` is safe to invoke again at
  any time.
- `aggregate` validates all outputs, writes `report.md` and
  `consensus.json` (`{"agree": bool, "verdicts": …, "blocking": …}`).
- `status` prints the state of every round of a run.

## Run

```sh
python3 tools/council.py selftest
python3 tools/council.py prepare --run northstar-2026-10-28 --round 1 --doc Bennett-NorthStar.md
python3 tools/council.py prepare --run isa-2026-10-28 --round N --doc Bennett-ISA-Spec.md \
        --rubric docs/council/rubric-isa.md --context Bennett-NorthStar.md \
        --subject "..." --precheck "python3 tools/isa_check.py"
python3 tools/isa_check.py        # the pre-flight on its own
python3 tools/council.py run     --run northstar-2026-10-28 --round 1 [--member codex …] [--dry-run]
python3 tools/council.py status  --run northstar-2026-10-28
python3 tools/council.py aggregate --run northstar-2026-10-28 --round 1
```

## Convergence process (adopted 2026-10-28 after ISA rounds 1–4)

The north star converged in six rounds; the ISA spec oscillated (2.12 →
2.83 → 3.04 → 2.83) because each round was a full rewrite that introduced
new mechanical errors, and because members were grading field-level
completeness of contracts as blockers. The process is now:

1. **Surgical edits between rounds, never rewrites.** Accepted text does
   not move. The editor applies each blocker's fix in place and records
   it in `round-<N>/response.md`.
2. **Pre-flight before every round.** `prepare --precheck` runs
   `tools/isa_check.py`: the spec's example objects must parse per the
   grammar, their hashes must reproduce from the spec's own envelope rule,
   their layouts must be disjoint, and their stated results must hold on
   a reference interpreter. A round is not prepared if the check fails.
   Add every new example or claim to the check before grading it.
3. **Diff attached.** `prepare` attaches the unified diff from the previous
   snapshot; members confirm fixes there first, then hunt new S0 issues.
4. **S0 only blocks.** The rubric defines blocking as "two conformant
   implementations would differ, or unsound, or contradictory, or a
   missing normative decision". S1 (implementer must choose, any choice
   conformant; enumeration gaps with a stated default) goes to
   suggestions. The spec carries a deferred-decisions section with
   defaults so S1 items can be closed by stating a default.
5. **Staged acceptance.** Every blocker is tagged `core` or `contract`;
   members give `verdict_core` and `verdict`. Core consensus first.
6. **Status accounting.** Members fill `previous_status` for every prior
   blocker and list `regressions`; the report shows them, so a regression
   is visible as such and never mistaken for new depth.
7. **Formal correctness after practical revisions.** Statements with
   hypotheses are required; proofs, mechanisation and witness formats
   are S1 until implementation has forced the revisions it will force.
8. **Executable spec as the tie-breaker.** When a round still disputes a
   core rule, the rule is implemented in `bennett-isa-spec`'s reference
   interpreter and the example extended, rather than re-worded.

Between rounds the editor revises the document on the blocking issues
(and on suggestions it agrees with), records what changed and what was
declined in `docs/council/<run>/round-<N>/response.md`, and prepares the
next round with `--precheck "python3 tools/isa_check.py"`.

## Fix-round policy (maintainer, 2026-10-31, on the process watcher's first entry)

- **Fix rounds use one reviewer**: the `codex` seat (astra) re-grades after the editor's
  fixes. `sol` sits only on acceptance votes (every blocker reported resolved) and on new
  material. Every sol blocker in isa-ref rounds 9-12 and dialect round 8 was also raised by
  astra; the second seat on fix rounds bought no finding.
- **One commit per round**: `prepare`, `collect` and `aggregate` artefacts land in a single
  `council:` commit when the round is aggregated, not three or four.
- **Severity field**: blocking means S0 by the rubric's definition; S1 belongs in
  suggestions. The per-item `severity` field was redundant and was removed on 2026-10-31
  (isa-ref round 13 reviewers were launched on the old schema; old-style JSON still validates).
- **A recurring blocker family gets a generated test, not another round**: when two rounds
  patch instances of one defect (R11-B02 and R12-B01, dotted-name layout leaves), the editor
  adds a deterministic family over the whole input class before any further review.
