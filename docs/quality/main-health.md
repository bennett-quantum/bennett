# Local main health

`python3 -I tools/main_health.py run --once` fetches every manifest repository's
`origin/main`, runs changed mains through their own `scripts/pre-push`, then checks
ladder rungs 1 and 2. It is a local evidence collector. It installs no hook, starts
no scheduler, blocks no push, sends no notification and performs no revert.

The default state directory is the **main meta checkout's** `.tmp/main-health/`,
including when invoked from a linked worktree. Override it with `--state-dir PATH`
or `BENNETT_MAIN_HEALTH_STATE_DIR`; `--meta PATH` selects another main meta checkout
and its manifest. Repo paths resolve relative to that checkout's parent.

```sh
python3 -I tools/main_health.py run --once --repos bennett-sched
python3 -I tools/main_health.py run --once --ladder rung-1
python3 -I tools/main_health.py run --once --repos bennett-sched --ladder rung-1
```

`--repos` alone runs only those repo gates; `--ladder` alone runs only those rungs.
Omitting both selects all manifest repos and both rungs. Every status snapshot has
a row for every manifest repo and both rungs; unselected, unverified rows say
`UNKNOWN`. Existing unselected evidence remains visible, with its original time.
The exit code covers the selected rows: 0 for PASS, 1 for a gate's FAIL, 2 for tool
errors, UNKNOWN, or TIMEOUT. Tool errors take precedence over failures. Missing
manifest entries, gate stubs and gate configurations are explicit errors.

Without `--once`, the same process repeats cycles after the polling interval.
`--force` repeats checks even when revisions have not changed. Otherwise PASS and
FAIL are cached by their complete revision vector; ERROR/TIMEOUT/UNKNOWN retry.
A cached failure stays red until revisions change or a forced check passes.

## Gate evidence

The runner fetches the remote main explicitly and creates detached worktrees at
`<state>/<repo>/<sha>/<repo>/`. It runs that revision's stub with `--sha <sha>`;
the stub loads that revision's pinned gate tool and siblings. A dirty local main,
an inherited hook-probe variable, or another branch's pins cannot change the
selected revision. Cached tracked files must remain clean. Git hooks are disabled
for cache materialization; normal push hooks are untouched.

The pinned tool masks live workspace directories using bwrap. Because the health
cache is nested inside the meta checkout, a generated bwrap adapter restores only
the detached gate root after those masks, including its pinned-sibling cache.
It preserves the live sibling masks and rejects unfamiliar isolation prefixes.
No `--no-isolate` option is used. Caches are retained for reuse and inspection;
the runner never prunes another job's worktrees or build outputs.

Each check writes a unique log and child exit record. `status.json` and
`status.md` are replaced atomically per file after each selected check;
`history.jsonl` appends completed observations (unchanged cache hits do not append).
Rows record revisions, PASS/FAIL/ERROR/TIMEOUT/UNKNOWN, verification time, elapsed
duration, delta, log, last green revisions and merge commits since those greens.
Merge names come from `git log --merges <green>..<current>`; they are candidates
for investigation, not a claim of causality. With no prior green, attribution is
explicitly unavailable. Repeated failures retain the original green baseline.

## Heavy slot and hang guards

Before each gate, the runner waits while any `bennett-heavy-*` systemd user scope
or legacy `gate_run-<sha>.py run --repo` process is live. It also requires at least
6 GiB available and load below 12, mirroring `.tmp/orchestrator/s4/qgate.sh` / R33
(2026-11-07). Polling is every 60 seconds, with a two-hour slot-wait guard, from
that same convention. Slot expiry writes TIMEOUT and returns 2. It never starts
work after that guard expires or signals another scope.

Actual gates run in their own `bennett-heavy-main-health-*` scope. A state-local
flock prevents overlapping health processes; other orchestrators observe the
scope convention. Like qgate, the protocol is advisory: all launchers must check
before launching. Builds retain the pinned gate's settings; inherited defaults
use three Cargo jobs and four test threads (R36, 2026-11-07).

`--command-timeout` defaults to qgate's 7000-second hang guard;
`--max-wait` changes the slot-wait guard. These are resource safeguards, never
semantic performance budgets. Guard expiry is TIMEOUT; termination without a
verdict is UNKNOWN. Both return 2, never PASS or FAIL (R40). Git/help operations
have a 60-second hang guard, mirroring the gate tool's hook-probe convention.

## Ladder integration limitation

The runner freezes the conformance main plus plugin, VM, runtimes, driver and ISA
origin/main revisions. It requires the ladder CLI to accept all five `--*-rev`
selectors and preserves its `table.md` per-major evidence beside the log and in
the status page. A successful exit without a table is a tool error.

As of 2026-11-07, both published ladder CLIs expose only `--plugin-rev` and
`--vm-rev`; runtime arguments select bitcode paths and the reference binary
defaults to a review interpreter. They cannot attest the requested five current
mains. The runner reports ERROR naming the first unsupported selector instead of
substituting moving build artifacts. This integration gap is tracked by
`bennett-t9r`; the repo-gate path is independent. No ladder success is claimed
until conformance supplies the missing revision-selecting interface.

## Deterministic tests

```sh
mkdir -p .tmp/main-health-job/tmp
TMPDIR="$PWD/.tmp/main-health-job/tmp" \
  python3 -I -m unittest discover -s tools/tests -p test_main_health.py -v
```

Tests use local Git remotes, a reversible gate verdict fixture, fake systemd
commands, and mocked slot probes/clock. They assert revision selection, command
work, status/history and merge attribution, not elapsed seconds. Test subprocess
timeouts are hang guards only.
