# Main health
`python3 tools/main_health.py seed --once --bead BEAD` runs pushed mains and seeds `health/known-reds.toml`; review and commit it.
Seed preserves existing entries; ladder report beads are used when `--bead` is omitted. Never seed incomplete evidence.
`python3 tools/main_health.py run --tier full --fresh [--once]` snapshots all mains, runs changed repos/rungs concurrently through gate_launch, and polls for moves.
Use `--meta`, `--state-dir`, `--baseline`, `--repos R,...`, `--ladder rung-1,...` to narrow or relocate; `--force` reruns unchanged mains.
Every source needs cited `short`/`eternal` classes in `tests/timeouts.toml` or its owner's `.tmp/main-health/hang-guards.toml` (guard >=10x measurement).
Baseline `[[red]]` fields: `scope` (repo or `ladder/rung-N`), `check`, full `sha`, `bead`, optional `shas` revision table.
Repo identities are gate record check names; ladder identities are `stage/<report path>` and `case/<report path>` including language/LLVM/case/stage.
Results: PASS, KNOWN-RED, NEW-RED, FIXED; absent/guarded evidence is UNKNOWN, infrastructure failures ERROR. FIXED never deletes an entry.
Events are atomic `bennett/.tmp/gates/events/main-health-*.json` objects with per-scope SHA vectors, check classifications, new reds, culprits, and logs.
Attribution retains per-check last greens, lists first-parent merges, and bisects persistent regressions using full fresh runs; probe bounds/counts/logs are in events. A `gate_run --check NAME` filter would reduce cost and avoid short-circuit gaps.
`python3 tools/revert_landing.py --repo R --merge M` reverts a first-parent merge on a clean main equal to origin/main and pushes;
the push hook starts the fast tier behind it. Every non-pass gate adds a line to `bennett/.tmp/gates/reds.log` (NEW or KNOWN).
Consumer pins name immutable commits that still exist after the revert.
Consumers keep building and gating against those commits until their pins are bumped.
A revert leaves consumers on the old content; it does not invalidate their pins.
