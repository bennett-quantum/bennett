# Pinned-sibling push gate

Problem: repo gates read live sibling trees, so they go red whenever a sibling job is mid-edit, and a green result
says nothing about which sibling it held for. This tool runs a repo's own checks on the pushed sha with every sibling
at a commit the repo pinned.

Files: `gate_run.py` (the tool), `gate_pre-push.template` (the per-repo `scripts/pre-push`), `gate_selftest.py`.
Selftest: `TMPDIR=<local dir> python3 -I tools/gate_selftest.py`.

## Tool or template: an installed tool, reached through a pinned stub

A copied template would be 13 diverging copies, which is the problem as it stands today (every `scripts/pre-push` was a
drifted copy). Non-negotiable 5 forbids sharing code across a *contract* boundary. This tool is not on one: no product
code or test imports it, and repos only run it, as they run `cargo` or `bd`. What a repo depends on is the `gate.toml`
format and environment variables, documented here. A repo's tests stay ignorant of the tool: they read a sibling path or
an env var.

Calling `../bennett/tools/gate_run.py` directly would itself be a live sibling read, so the stub extracts the tool from
the meta repo's objects at `tool_sha` in `gate.toml` (`git show <tool_sha>:tools/gate_run.py`) into `.tmp/gate/tool/`.
A tool upgrade is a deliberate one-line commit per repo. The stub reads `tool_sha` from HEAD's `gate.toml`; a pushed sha
whose `gate.toml` pins an *ancestor* of that tool runs under the newer one (announced; the record keeps `tool_sha` and
`tool_sha_ran`), so a walk-back push gets tool fixes. A pushed pin that is newer than, or unrelated to, the running tool
is refused (exit 3). The stub's own job is that fetch and the hook probe.

## What a run does

1. Reads refs from stdin as git supplies them (HEAD when run directly; deletion-only pushes gate nothing), and `gate.toml`
   **at the pushed sha**, never the working tree.
2. Materialises each pinned sibling as a detached worktree: `.tmp/gate/cache/<name>@<sha12>/<name>`. Reused across runs;
   rematerialised, with a notice, if its HEAD moved or tracked files changed. Beads hooks are blanked during `git worktree add`.
3. Verifies `files` hashes on every run. Builds declared `build` steps once per sha (stamped; a failed build is not stamped).
4. Creates `.tmp/gate/runs/<sha>/<repo>` (clean detached worktree of the pushed sha) with a symlink per sibling beside it,
   so `../bennett-isa-spec` and `../../bennett-isa-spec` resolve to the pin with no test change. A pin named `bennett` needs
   only objects from the meta repo.
5. Runs each `[[check]]` in order under bwrap, in which **every other top-level directory of the workspace is an empty
   tmpfs** except its `.git`. The workspace is rescanned before every command, so a sibling worktree created or removed mid-run is followed. An absolute or unpinned read of a live sibling gets ENOENT and the check goes red: that is the
   fail-loud for unpinned reads, and it cannot be bypassed by a path the static scan misses. Inherited `BENNETT_*`,
   `CARGO_TARGET_DIR`, `GIT_*` and display variables are scrubbed.
6. Runs each `[[report]]` (milestone and blocker status); its exit is printed and never decides anything.
7. Writes `.tmp/gate/records/<sha>.json`: pins used, `pushed` per pin, tool pinned and tool run, command measurements,
   setup time, machine profile, sibling cache state and result (receipt fields below).

The existing nonblocking lock at `.tmp/gate/locks/run-<sha>` rejects another attempt on the same SHA immediately with
setup exit 3. Its error names the holder's PID and UTC lock-acquisition time. Different SHAs retain their existing
per-sibling cache/build locks.

### Receipt measurements

Each entry in `checks` and `reports` retains `name`, `exit` and the compatible rounded `seconds` field, and adds:

- `wall_seconds`: unrounded monotonic elapsed seconds for that command, including launch and isolation overhead.
- `cpu_seconds`: user + system CPU seconds from Linux `wait4`, including descendants reaped by the command's process
  tree. Detached descendants that outlive their parents are not accounted for.
- `peak_rss_kib`: Linux `wait4` peak resident memory in KiB, the largest individual process peak in that tree,
  rather than the sum of simultaneous process memory. Each command is measured independently of earlier commands/builds.
- `width_env`: the width-related variables actually present in that command's environment, after expansion and overrides.
  No width is inferred from command arguments or tool defaults. The observed keys are `CARGO_BUILD_JOBS`,
  `CARGO_MAKEFLAGS`, `MAKEFLAGS`, `MFLAGS`, `RUST_TEST_THREADS`, `RAYON_NUM_THREADS`, `CMAKE_BUILD_PARALLEL_LEVEL`,
  `CTEST_PARALLEL_LEVEL`, `NINJAFLAGS`, `OMP_NUM_THREADS`, `OMP_THREAD_LIMIT`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`,
  `NUMEXPR_NUM_THREADS` and `GOMAXPROCS`. A command that cannot be launched retains exit 127 and records unavailable CPU/RSS.

Receipt probes are optional evidence and cannot change which checks/reports execute, their statuses, or the gate's
verdict/exit. A failed probe records `{"unavailable": "<exception class>: <message>"}` at the affected field and emits
a named `receipt <field> unavailable` diagnostic. Memory, CPU count, load, machine label, timing, CPU/RSS, cache state
and width observations are isolated; independent fields remain available. A label depending on unavailable machine
inputs is also explicitly unavailable. If `wait4` accounting fails, ordinary process waiting still obtains the real
command exit status; CPU/RSS are marked unavailable. Failed samples never supply a default number or empty environment.

Run-level `setup_seconds` measures configuration, isolation preparation, sibling materialisation/builds and creation
of the run worktree, ending before the first check. It excludes checks, reports and final worktree cleanup. The
run-level `width_env` records the common check environment; command entries include their individual overrides.
`machine` is sampled before setup: `nproc` (CPUs available through process affinity), `mem_total_kib` and
`mem_available_kib` from `/proc/meminfo`, `load1`, and `label`. The hostname-free label is `machine-<12 hex>` from a
SHA-256 fingerprint of architecture, available CPU count and total memory. It identifies a hardware profile;
identical profiles share a label.

Each `siblings` entry adds `cache_state`: `hit` when the pin and all declared build stamps/outputs were reused,
`materialised` when its worktree was created or repaired without running a build, or `built` when this run executed
at least one build step (including after materialisation). These fields are evidence only: they introduce no limits,
thresholds or changes to gate decisions. Repositories adopt this receipt format only when they bump their `tool_sha` pin.

SIGTERM, SIGHUP or SIGINT (an orchestrator kill under memory pressure) kills the running command's whole process group,
removes the run worktree and writes no record; exit 128+signal. Kill the gate's python process, never only the bwrap
below it. Tool c698ce1 (adopted everywhere on 2026-11-02) orphans the running build or test tree on SIGTERM and fails every later
command once a workspace worktree it saw at start is removed; both fixed since.

Exit: **0 iff every check passed**, 1 a check failed, 3 setup failed (missing or mismatched pin, absent commit, hash
mismatch, unbuildable sibling, unknown key or placeholder, no bwrap). `--no-isolate` is announced and means the run is not
a push gate. A pin not yet on `origin/main` is a noted fact in the record, not a failure, since a push order can make it true.

## gate.toml

```toml
schema = 1
repo = "bennett-plugin"          # directory name inside the layout
tool_sha = "<40 hex meta commit>"
timeout_s = 28800                # per command; optional

[env]                            # placeholders: {wt} {root} {layout} {sibling:NAME}; unknown ones are an error
BENNETT_SIBLINGS = "{layout}"
CARGO_TARGET_DIR = "{root}/.tmp/gate-target"

[[check]]                        # also: env = {...}, cwd = "subdir"
name = "repo gate"
argv = ["scripts/gate"]

[[report]]                       # optional; evidence only
name = "blockers"
argv = ["scripts/blockers"]

[siblings."bennett-isa-spec"]
sha = "<40 hex>"
repo = "bennett-isa-spec"        # optional alias source, e.g. name bennett-isa-spec-review
note = "why this commit"
[siblings."bennett-isa-spec".files]
"spec/ref-0.9.json" = "<sha256>"
[[siblings."bennett-isa-spec".build]]
name = "reference interpreter"
cwd = "reference-interpreter"
argv = ["cargo", "build", "--offline"]
outputs = ["reference-interpreter/target/debug/bennett-isa-ref"]
needs = []                       # pinned siblings to place beside this one for its build; part of the build key
```

Unknown keys, abbreviated shas and a file with no `[[check]]` are refused. Moving a pin is a commit in the consumer, so a
sibling's change reaches a gate only when the consumer says so; to learn whether it should, use the consumer check:

## Consumer evidence: `report-live`

`gate_run.py report-live --repo R [--sha S] [--run [--trace]]` always exits 0 on a completed report; it is never a
stop condition for R's gate. It prints pin drift against each live sibling and tracked references to sibling paths
(`absolute`, `relative-pinned`, `relative-unpinned`). `--run` runs the checks against the **live** siblings, unisolated,
and reports `consumer check against live siblings: PASS|FAIL`. `--trace` adds strace and lists the absolute live paths touched.
`verify --repo R --sha S` is the preflight: materialise, hash and build every pin, run no check.

## Hook chain

`gate_run.py hook-check --repo R` exits 0 iff git's effective pre-push hook reaches this repo's stub. It resolves the path git
would use (honouring `core.hooksPath`), requires it executable, requires it to be or `exec` `scripts/pre-push`, then runs
it with `BENNETT_GATE_HOOK_PROBE=1`, which the stub answers without gating. `bd init` sets `core.hooksPath=.beads/hooks`
and leaves a *copy* of the gate there, and `.git/hooks/pre-push` is then dead. The right file is:

```bash
#!/usr/bin/env bash
set -euo pipefail
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
hook_dir="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
root="$(dirname "$(dirname "$hook_dir")")"
exec "$root/scripts/pre-push" "$@"
```

Without `core.hooksPath`: `ln -s ../../scripts/pre-push .git/hooks/pre-push`.

In the meta repository, `scripts/install-hooks.sh` installs an executable wrapper at
`git rev-parse --git-path hooks/pre-push`, so it follows the effective `core.hooksPath` and works in linked
worktrees. The wrapper executes the current worktree's `scripts/pre-push`. This repo's own hook runs
`python3 -m unittest discover tools/tests` and fails if discovery finds zero tests. Installers and hook tests
use scratch repositories; installation into the main checkout belongs to the orchestrator.

## Ecosystem ignore convention

Every repository's quality job copies these patterns into its own `.gitignore`:

```gitignore
__pycache__/
*.pyc
*.log
.beads/**/LOCK
*.darc
```

Ignore rules do not untrack existing files. Remove tracked generated files from the index in the owning repo;
keep Beads source and its passive exports tracked. Council run logs under `docs/council/` are generated output.

Under R26, the orchestrator creates each T3 child's worktree at `../<repo>-job-<name>` on `job/<name>`.
The child commits owned paths and pushes `HEAD` to `wip/<name>` after every commit.
The orchestrator merges the job branch after review.

## Adopting a repo

1. Write `gate.toml`: the same checks the old `scripts/pre-push` ran, each sibling it reads, each binary it needs.
2. Commit it. `verify --repo R --sha HEAD`.
3. Replace `scripts/pre-push` by the template with an atomic `mv` (a running bash reads its script as it goes), and commit.
4. `hook-check`; run `scripts/pre-push </dev/null` once and record the true result.

Red under isolation with a path in the error means the test reads a live tree: point it at `../sibling` or an env var, or
add the pin. Never `--no-isolate` to get a push through.
