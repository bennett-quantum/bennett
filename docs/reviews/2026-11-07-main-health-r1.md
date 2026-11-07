# Main-health review, round 1 — 2026-11-07

Verdict: **CLEAR**. No confirmed P0/P1 findings.

Reviewed `main..job/main-health`: commits `3aff4c3`, `5ea389e`;
base `f0353fecb322afb816dd444f821e9d29496f06e5`,
head **`5ea389e554b315b189a99413c6dc0073c39eafd3`**.
Provenance: implementer gpt-6.1-sol; reviewer gpt-6.1-sol, fresh session (D9).

Verification:
- `timeout 120 python3 -I -m unittest discover -s tools/tests -p test_main_health.py -v`: **16 PASS**, headless, with
  `TMPDIR=$PWD/.tmp/rev-main-health-r1/tmp` and job-local Cargo target. Log: `.tmp/rev-main-health-r1/focused.log`.
- Independent fixture assertions under `timeout 60 python3 -I -`: fetch failure replaces a previous PASS with ERROR;
  a second state lock is refused and the lock releases; modified tracked cache files are refused; real nested bwrap
  exposes the detached cache while hiding live sibling files and retaining Git metadata. All PASS;
  log: `.tmp/rev-main-health-r1/adversarial.log`. No actual gate or health run started.
- `git diff --check main...job/main-health`: PASS. Main-side tool/tests are absent (`git ls-tree main`);
  the missing-tool red-first evidence would fail there. The later isolation regression exercises the actual
  `--chdir ... --` prefix and passed at head. No weakened or skipped tests or elapsed-time verdict assertions found.

P0/P1 ids: none.
P2+ nits: **bennett-zpf** — remove orchestration rule/shift identifiers from source comments
(`tools/main_health.py:18,56,83`); existing **bennett-t9r** tracks unsupported ladder revision selectors, which correctly
produce ERROR rather than a false PASS.

Bounded acceptance completed during review: shared status, child exit record and the isolated pinned-gate JSON
independently agree on scheduler **PASS**, SHA `3fc4d7bdc399a5c6e3df4cd51ce01c4a040eb2fc`, exit 0,
2026-11-07T17:36:50Z. All four configured checks exited 0 (including slow exhaustive simulations).
Evidence: main checkout `.tmp/main-health/logs/bennett-sched-1794072409242209999.log` and its `.exit`;
gate record under `.tmp/main-health/bennett-sched/<sha>/bennett-sched/.tmp/gate/records/<sha>.json`.
The concurrent acceptance-only commit `65b6edce4c9a0756324f6643052012dbdd1fa05b` changes the worklog only;
that diff was checked and the reviewed tool/tests/docs remain unchanged. Other repos and both ladders are UNKNOWN;
no full unfiltered or ladder success is claimed. The unfiltered acceptance remains the orchestrator's.

Coverage: read closely all 407 tool lines, all 308 test lines, docs and worklog diff; checked every anti-slop rule,
revision/exit propagation, state/history, merge attribution and lock/resource behavior. Read the pinned gate's
stub/config/isolation/execution interfaces and ladder selector definitions; skimmed unrelated gate internals.
Plan items 9–11 checked: this job explicitly forbids gate.toml changes, and the retained meta HANDOFF is the central
ecosystem handoff that per-repo retirement points to; neither is a scope violation.
