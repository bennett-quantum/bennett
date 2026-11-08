# Gate receipt review, round 1

Verdict: **BLOCK** — one P1 affecting the **gate** route.

Reviewed range: `1ddc1833b86c631d20df68faa396f47e55a51c2b..ff893f8673d1577340b24549387d286ed5f48732` on `job/gate-run-receipts` (`a3a99e7`, `ff893f8`). Main was the specified meta main, not a sibling main.

**P1-1 — machine metadata can stop a passing gate.** `tools/gate_run.py:468`, called unconditionally at `:481`; bead **bennett-quv** (priority 1, review). When a Linux sandbox hides/denies `/proc/meminfo`, the new profile read raises `PermissionError` before any check or receipt. On the same isolated tiny repository with a single `true` check, main exits **0/PASS**, while head exits **1/traceback**. Measurement availability now controls the gate, contrary to the receipt-only contract. Keep check/setup outcomes independent of sampling failures and report unavailable measurements explicitly with a diagnostic; do not silently invent valid-looking values.

Command run from this worktree (scratch repositories only; baseline/head sources executed in memory, no branch switching):

```sh
timeout 120s python3 - <<'PY'
import subprocess, sys
from tools.tests.test_gate_run import ReceiptTests, TOOL
t = ReceiptTests()
t.setUp()
try:
    sha = t.config(checks=[["true"]])
    for rev in ("1ddc183", "ff893f8"):
        source = subprocess.check_output(
            ["git", "show", f"{rev}:tools/gate_run.py"], text=True, timeout=20)
        boot = ("import sys; sys.argv.pop(1); exec(compile(" + repr(source)
                + ", 'gate_run.py', 'exec'), {'__name__':'__main__'})")
        z = subprocess.run(
            ["bwrap", "--dev-bind", "/", "/", "--ro-bind", "/dev/null",
             "/proc/meminfo", sys.executable, "-I", "-c", boot, str(TOOL),
             "run", "--repo", str(t.repo), "--sha", sha],
            env=t.env, capture_output=True, text=True, timeout=30)
        print(rev, z.returncode, "PASS" if f"PASS {sha}" in z.stderr else z.stderr)
finally:
    t.doCleanups()
PY
```

P2+ nits: **bennett-zgu** (priority 3, review) — `tools/gate_run.py:220` drops Popen's `ChildProcessError` handling: an inline fixture bootstrap setting `SIGCHLD=SIG_IGN` makes the old `run --no-isolate` true-check pass and head crash; its isolated baseline probe instead hit the existing 30s guard (**UNKNOWN**), so no isolated-gate regression is claimed for this edge case.

Verification: `timeout 120s python3 -m unittest discover -s tools/tests -p test_gate_run.py -v`: **6 passed** (1.064s); `timeout 120s python3 -m unittest discover tools/tests`: **72 passed** (6.639s); `timeout 120s python3 -I tools/gate_selftest.py`: **50 passed**, no skips (11.843s). `git diff --check 1ddc183...ff893f8` passed. All tests ran headless, serially, with local `TMPDIR=.tmp/rev-gate-run-receipts-r1/tmp` and local `CARGO_TARGET_DIR=.tmp/rev-gate-run-receipts-r1/target`. No real repository's full gate ran. Git20/CLI30 follow the existing meta fixture conventions; outer120 exceeds 10x the recorded suite durations, and guard trips are UNKNOWN.

Red-first assessment: read `git show 1ddc183:tools/gate_run.py` against the new fixtures: main lacks the asserted metadata keys and holder PID/start text, so those assertions fail there; all six fixtures pass at head. The setup test advances an independent clock across `prepare`; child self-usage supplies the resource lower bound. No tests were removed, weakened or skipped. Existing isolation, pin/hash/build, check-order, failure, report, hook and interruption tests pass. Check selection, PASS/FAIL expression, sibling pin resolution and isolation construction are unchanged; the profile exception above is the confirmed gate-integrity breach.

Coverage: read closely all changed production, fixture and README lines, surrounding wait/timeout/cleanup, sibling materialisation/builds, configuration/CLI and receipt code; skimmed the unchanged live-report/hook paths and legacy self-test cases. Checked every COMMON anti-slop category (dispatch, state, failure defaults, predicates, constants, altitude, wrappers, process identifiers, litter, independent assertions); the reported exception paths are the findings. No owned-path violation, new tracked litter or north-star narrowing found. Plan 9–11 checked: no meta `gate.toml`/ratchet exists, as previously exempted for meta R0.1; this metadata-only job does not expand that scope. Meta `HANDOFF.md` is the central ecosystem handoff, not a retired per-repo handoff.

Provenance: implementer gpt-6.1-sol; reviewer gpt-6.1-sol, fresh session, D9.
