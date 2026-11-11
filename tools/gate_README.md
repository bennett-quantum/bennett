# Pinned-sibling push gate

The gate runs a repository's checks on a committed input, with siblings pinned by that
commit's `gate.toml`. Python stdlib only; isolated runs require Linux bwrap. A component's
`scripts/pre-push` extracts `tools/gate_run.py` from the meta commit pinned by `tool_sha`.
Tool upgrades require a deliberate pin bump. The existing stubs forward all arguments.

```sh
python3 tools/gate_run.py run --repo R [--sha S] [--tier pre-merge|full] [--fresh]
python3 tools/gate_run.py verify --repo R --sha S
python3 tools/gate_launch.py start --repo R [--sha S] [--tier pre-merge|full]
python3 tools/gate_launch.py wait <unit>
python3 tools/gate_launch.py status
python3 tools/admit.py gate --repo R --tier full
```

Without `--sha`, run reads Git's pre-push ref stream, or HEAD with empty stdin; deletions
gate nothing. Config is read from the selected commit, never the dirty checkout.
`verify` materialises/hashes/builds pins without running checks. `hook-check --repo R`
verifies that the effective executable pre-push hook reaches the stub (including
`core.hooksPath`), using its `BENNETT_GATE_HOOK_PROBE=1` handshake.

## Config

```toml
schema = 1
repo = "example"                    # layout directory / owning main checkout
tool_sha = "<40 hex meta commit>"   # pinned tool identity
timeout_s = 28800                  # optional per-command hang guard

[receipt]                          # optional; no implicit exclusions
non_product = ["worklog/", "HANDOFF.md"]

[env]                              # {wt}, {root}, {layout}, {sibling:NAME}
CARGO_TARGET_DIR = "{root}/.tmp/gate-target"

[[check]]                          # default tier: pre-merge
name = "tests"
argv = ["scripts/test"]
# cwd = "subdir"
# env = {RUST_TEST_THREADS = "2"}

[[check]]
name = "expensive regression"
argv = ["scripts/slow"]
tier = "post-merge"
inputs = ["src/", "tests/", "Cargo.toml"]  # optional early-warning trigger

[[report]]                         # optional; exits never decide the gate verdict
                                   # reports alone get BENNETT_GATE_SHA, the real gated commit
name = "blockers"
argv = ["scripts/blockers"]

[siblings.library]
sha = "<40 hex>"
# repo = "source-directory"        # alias; defaults to sibling name
# note = "reason for pin"
[siblings.library.files]
"dist/library.bc" = "<sha256>"
[[siblings.library.build]]
name = "library"
argv = ["cargo", "build", "--offline"]
cwd = "crate"
outputs = ["crate/target/debug/library"]
needs = []                         # other pinned siblings needed by this build
```

Unknown keys/placeholders, abbreviated pins, invalid tiers, and a config with no checks
are setup errors. `inputs` requires a post-merge check and a nonempty relative path list;
directory inputs accept a trailing slash or a directory name. Missing inputs are part of
the content identity, so creation/deletion changes it. Pins, command configuration and
environment templates also enter the input key.

`non_product` accepts exact relative paths or directory prefixes ending in `/`, without
globs, absolute paths, `..`, empty paths or Git metadata. Configuration load refuses an
entry covering `gate.toml`, `scripts/pre-push`, any check/report executable or cwd, or a
path named in a global or command environment template. Diagnostics name the entry.
There is no automatic documentation exclusion: baselines/specs may be test inputs.

## Receipts and tiers

With `[receipt]`, the content identity is SHA-256 of Git's NUL-delimited recursive tree
listing (`ls-tree -rtz`) after exclusions, including every remaining entry's mode, type,
object ID and path. Directory IDs are recomputed after filtering. The receipt key hashes
`json.dumps([content, tool_sha_ran, isolated, tier], sort_keys=True)`. `gate.toml` always
remains product, so exclusion-policy, check and pin changes invalidate coverage.

Before any build/check/report runs, the run checkout uses a parentless synthetic commit
with exactly that filtered tree. Excluded paths are absent from the filesystem, index
and HEAD; `cat excluded` and `git show HEAD:excluded` fail. This avoids leaving excluded
index entries behind after deleting files. When `non_product` is declared, the gating checkout's own working tree is hidden inside bwrap (an empty tmpfs) and
only its `.git` and `.tmp` (gate state, run tree, caches, `CARGO_TARGET_DIR`) are bound back. Excluded paths are
therefore uniformly absent: their bytes, symlink text and existence cannot reach a check through `{root}`, an env
template or a tracked symlink, so a fresh gate's verdict cannot depend on them. A config that keeps state in the
checkout outside `.tmp` must move it under `{root}/.tmp/` when it adopts `non_product`; entries under `.tmp/` or
`.git/` are refused. Git objects remain available for pinned
worktree operation; arbitrary historical-object reads are not sandboxed. A check must
use its run input, rather than deliberately fetching historical excluded objects.

Without `[receipt]`, pre-merge retains the exact legacy key:
SHA-256 of `json.dumps([original_tree_id, tool_sha_ran, isolated], sort_keys=True)`.
Existing verified receipts remain valid. Full-tier receipts have distinct keys. Before
receipt use, the executing tool blob must match its full meta commit claim (the config
pin or `--tool-sha`); otherwise `PASS RECEIPTS DISABLED` names the reason and checks still
run. A newer running tool may replace an ancestor pin; unrelated/newer pins are refused.

Pre-merge runs default checks. A post-merge check with `inputs` also runs when its
(inputs content, pins, command/env, tool, isolation) key has no PASS; otherwise the record
says `deferred to post-merge, inputs unchanged since <sha>`. Without inputs it defers.
This trigger is an early warning only. **Main-health runs `--tier full` on every pushed
main**; full always runs post-merge checks unless the complete content already passed
full. It can reuse a same-content pre-merge receipt and run just post-merge checks.
A full PASS also covers pre-merge. Records name `tier`, `tiers_ran`, `tiers_covered` and
`deferred`. A full content hit writes `covered_by` without preparing siblings/checks.
`--fresh` bypasses every receipt. Failures and interruptions publish no tier PASS.

PASS receipts remain shared under the owning main checkout's `.tmp/gate/receipts/`,
atomically replaced. Records are local `.tmp/gate/records/<sha>.json`; successive tiers
replace that SHA's latest record, while distinct receipts retain tier evidence.

## Worktrees, isolation and evidence

Each supplied checkout has real local `.tmp/gate/{cache,locks,runs,records}` directories.
The old shared-cache symlink is unlinked (including dangling links) with a diagnostic;
its target is never followed. Other symlinked mutable state is refused. Use `--repo`
**the job worktree** for job gates and pin preparation. Concurrent worktrees have separate
pin builds, target dirs and locks; same-SHA runs within one checkout fail immediately,
with the holder PID/UTC time. Shared immutable pin caches are not implemented.

Pins live in `cache/<name>@<sha12>/<name>`; dirty/moved tracked cache contents are
rematerialised. Declared hashes are verified each run; successful builds are stamped
with their command/pin/dependency identity. The run is `runs/<sha>/<repo>` with sibling
links beside it. Hooks are disabled while creating Git worktrees. Bwrap hides other
workspace checkouts while preserving their `.git` object directories, including linked
worktree common directories. It rescans before every command. Unpinned live reads fail.
Inherited `BENNETT_*`, Git overrides, cargo target and display variables are scrubbed;
`--no-isolate` is explicitly announced and is not a push gate.

A byte-for-byte second copy of one real `bennett-runtimes` cache cost **42,225,664 bytes
(40.27 MiB)** allocated disk (`cp -a --reflink=never`, `du -s -B1`, both copies equal).
This measures duplication, not a new component build; real costs vary with pins/outputs.

Records retain command exits, wall/CPU seconds, largest-process peak RSS (KiB), effective
width variables, setup time, machine profile and sibling cache states. Failed optional
probes report an explicit `unavailable` diagnostic/value without changing command exits.
Reports are evidence only. SIGTERM/SIGHUP/SIGINT kill the command group and clean the run
worktree; setup failures are loud. `--keep` retains a run for inspection.
Exit: 0 PASS, 1 check failure (including a recorded command hang guard 124), 3 setup error,
128+signal interruption. Detached events promote a recorded hang guard to gate exit 124.

## Detached completion and admission

`start` serializes resource assessment/reservation, then uses `systemd-run --user` to
create a detached **service**, never a scope. A content-addressed snapshot of the three
Python modules keeps execution/completion available after caller checkout edits/removal. Unit identity includes checkout path, SHA12
and tier. ExecStopPost atomically writes one object to
`<workspace>/bennett/.tmp/gates/events/<unit>.json`, including pass/fail/setup error,
hang guard, signal or wrapper crash, SHA/tier, record path, UTC start/finish, peak RSS and
disk use when measurable (otherwise explicit unavailability). The cgroup MemoryPeak is
preferred over process accounting. `wait` blocks on that event and returns its exit;
`status` lists admitted running and completed units. Launch failures also publish events.
The user systemd manager must be available; no shell-background fallback is used.

Admission requires MemAvailable minus all running reservations
`max(0, expected peak - current RSS)` (conservative cgroup anon + shmem) >= expected peak + **6 GiB**, load1 < nproc/**2**,
and free disk >= expected disk + **20 GiB**. Expected peak/disk use latest same-tier
records/events. Missing history uses explicit conservative defaults **8 GiB peak / 16
GiB disk**; the reason prints those numbers. Constants and sources are in `admit.py`.
Probe failures print `WAIT` with the error; there are no fabricated resource samples.

`report-live --repo R [--sha S] [--run [--trace]]` reports pin drift and tracked sibling
references; optional checks read live siblings unisolated. Completed reports exit 0;
they never supply a push receipt. `--trace` reports absolute live reads with strace.

Validation: `scripts/pre-push` runs the meta unit tests. Run
`TMPDIR=<local scratch> python3 -I tools/gate_selftest.py` for scratch-repo integration
checks. Unit tests inject launch/probe functions and never start real systemd services.
