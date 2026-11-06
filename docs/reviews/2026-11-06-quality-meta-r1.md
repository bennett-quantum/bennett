# quality-meta review, round 1 — BLOCK

Reviewed `git log --reverse main..job/quality-meta` and `git diff main...job/quality-meta`:
`7e257d2`, `bd69b92`, `db26f33`; head **db26f33c7e74db701d791793ffd68a7d0e43caa4**.
Comparison main: `4d2fdd1c5e8a0f6efdd66aa081f15fe121a04a4a`; diff merge base:
`676ee6a50cf101fbe2e5a3051e9d629c9760c68e`. Scope: R0.1 as trimmed by R26.

**P1-1 — skipped-only suite passes the push gate** (`scripts/pre-push:17`, execution at line 20),
bead **bennett-dog**. `countTestCases()` counts skipped cases. When every discovered case is
skipped, the count guard passes and the subsequent unittest command exits 0 without executing any
test body. This misses the brief's requirement to fail when no test runs. The existing empty-directory
test does not cover it. Run the suite once, require at least one non-skipped execution as well as
success, and add a skipped-only regression. No P0 findings.

Reproduction run at head, from the review worktree (headless, review-local TMPDIR):

```bash
timeout 30s python3 - <<'PYTEST'
import unittest
from tools.tests.test_scripts import HookTests
class NoRunnableTests(HookTests):
    def test_skipped_only_suite_is_rejected(self):
        (self.tests / 'test_fixture.py').write_text("import unittest\n@unittest.skip('deferred')\nclass Fixture(unittest.TestCase):\n    def test_fails(self): self.fail('must execute')\n")
        result = self.run_script(self.repo / 'scripts/pre-push')
        self.assertNotEqual(result.returncode, 0, result.stderr)
result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([
    NoRunnableTests('test_skipped_only_suite_is_rejected')]))
raise SystemExit(not result.wasSuccessful())
PYTEST
```

Result: regression assertion **FAIL**, `0 == 0`; inner hook reports `OK (skipped=1)` and exits 0.
Only temporary fixture files were written; no implementation was changed.

P2+ nits: **bennett-kw1** (priority 3, `nit`): `tools/tests/test_review_packet.py:45` checks the
`sha256` label but no digest; an in-memory mutation replacing every digest with twelve zeroes still
passes `test_first_order_binary_hash_and_fenced_text` (`timeout 30s python3 -`, one test OK).

Verification: `timeout 90s python3 -m unittest -v tools.tests.test_scripts tools.tests.test_review_packet tools.tests.test_council_selftest tools.tests.test_council_schema tools.tests.test_council_steps`
— **41 passed**, 6.034 s. This includes the optimized council compatibility command and failed-installer
propagation. Additional `timeout 60s python3 -` scratch-repository push checks: installed Beads-path hook
accepted a passing case (exit 0), rejected a failing case (exit 1), and rejected that failure in a linked
worktree (exit 1). No full repository or sibling gate was run.

Main-side red-first assessment used `git show main:<path>` without switching branches: the old empty-test
hook returns 0, the old installer ignores hooksPath and fails in a linked worktree, the old remote script
swallows installer failure, and the old packet matcher drops `target_notes.md`/`secretary.py`; the new
corresponding tests pass at head. Every former council selftest check is retained in the migrated tests;
the optimized CLI test would reject main's assertion-free `selftest ok` output.

`git diff --check main...job/quality-meta` passes. Direct `git diff main job/quality-meta -- tools/codex_job.py`
is empty. All 16 removed council logs remain on disk; no tracked pycache/log/backup/progress litter remains.
No north-star capability was narrowed. Round-1 remediation items 9–10 do not apply to this R0.1 prerequisite;
meta's `HANDOFF.md` is the central ecosystem handoff those items reference.

Coverage: read closely every changed script, packet matcher, council selftest deletion/replacement, new test,
fixture, ignore rule and README addition; skimmed surrounding council/gate-template code and deleted log content.
Checked all COMMON Anti-slop rules: dispatch, state, failure defaults, predicates, constants, function altitude,
wrappers, process identifiers, litter and test independence; the findings above are the exceptions.
Provenance: implementer gpt-6.1-sol; reviewer gpt-6.1-sol, fresh session, D9. This sol review does not replace the
council review required for gate changes by programme principle 6.
