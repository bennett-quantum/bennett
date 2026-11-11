The maintainer owns root `dial.toml`: each vendor's `pace` multiplies its weekly uniform line.
`1.0` implements “Please work up to but never exceeding pace”; `1.2` permits 20% ahead; `0` pauses.
Run `python3 tools/admit.py launch --vendor codex --kind implementer` (`claude|muse`, `review|gate|council` also work).
It prints `ADMIT <reason>` / `WAIT <reason>` and exits 0/1; every kind spends quota equally.
Launches require memory/load/disk headroom including running gate reservations, and weekly use below the dial line.
At the line, wait: a fresh launch spends beyond it. Reasons give each vendor's distance in percentage points.
Resource history and the dial come from this tool's meta checkout; linked worktrees share one quota cache.
The quota CLI's USED minus signed PACE gives the uniform line; no weekly row or failed probe means WAIT for that vendor.
CLI results and failures are locked/cached for five minutes in the meta repo's common `.tmp/admit/`; failed probes never invent values.
Legacy `gate --repo PATH` and `assess()` retain resource-only admission for `gate_launch.py`.
