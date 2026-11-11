> **SUPERSEDED 2026-11-11** by [COMMON.md](../process/COMMON.md) rules 9-12 (land on the fast tier, detect after, review after
> landing in at most two rounds, trial exception). Kept as the historical record; it binds nothing.

# Code quality policy

**Status:** IN FORCE. Ratified by the maintainer on 2026-11-03 (advisor-notes D1: rule 5 Muse seat when quota is readable and the advisor confirms, otherwise sol xhigh plus Sonnet stand in). Proposed by the advisor on 2026-11-02; originally: the maintainer ratifies at the
start of the next session, then law 2 in each CLAUDE.md points here. Deliberately short: the maintainer wants no
administrivia, process theatre or review paranoia. If a rule here needs a form, a tracker or a ceremony, delete it.

**Amendment, maintainer 2026-11-08:** Rules 2 and 4 record the practised evidence-first review and the precedence
of the no-narrowing rule.

## Review

1. **Code gets reviewed before it is pushed to `main`.** One writer per path set (CLAUDE.md non-negotiable 2); review is batched over
   what the stream has landed since its last review. The orchestrator launches the review when a stream's batch is
   done, not per commit and not on a timer.
2. **Evidence-first review.** One fresh gpt-6.1-sol xhigh review starts from the implementer's evidence
   (PROGRESS.md, gate log and red-first test) and re-runs its claims, reading the diff where the evidence is thin.
   Claude or Muse may serve as an occasional second eye.
3. **Two rounds, then merge or revert** (amended 2026-11-07, was three). Round 1 reviews, round 2 checks the fixes.
   After round 2 the batch merges with every remaining finding filed as a P2 bead, unless a blocking finding (rule 4)
   is still open; then the offending commit is reverted and re-landed later, not iterated a third time.
4. **Only P0 and P1 block, and only on the ladder route** (amended 2026-11-07). A finding is P0/P1 only if it
   (a) produces a wrong result or a silent fallback on a product path that a north-star §8 rung exercises, (b) makes
   an oracle unsound (reference interpreter, checker verdicts, certificates), or (c) breaks a build, link, gate or
   push hook. The reviewer names the rung affected; a finding that names no rung is P2 unless the no-narrowing
   rule below applies. Linters, test-harness hygiene, edge cases outside the ladder route (overflow at usize::MAX,
   relative paths through PATH, hash drift with unchanged observables), pre-existing gaps and narrowings of
   unpromised paths no rung uses are P2 by definition: one bead, never a repair round. A new rejection or omission
   of a north-star-promised capability is a blocker under CLAUDE.md non-negotiable 10, never P2, even if no current
   rung uses it. Everything else is a nit.
5. **Stakes pick the seat** (amended 2026-11-07). Routine code: one sol review. Councils (sol + astra + Muse) only
   where the oracle lives: the reference interpreter, checker verdict logic, certificates, and published contracts.
   Plugin lowering, soft-float, scheduler core and gates get one sol review; a council may still be convened there
   as a one-round advisory whose findings become beads, never a fix cycle. Astra is a review and council seat only,
   never an implementer (R31).
6. **Output is one short document** in `docs/reviews/`: verdict, P0/P1 findings with file, line, failure scenario
   and what was run, beads filed. That is the whole record.

## Slop

7. **Loops, not prompts.** The maintainer's 2026-10-31 study (SlopCodeBench, 287 master refactors) found anti-slop
   prompting cuts slop by a third without changing the rate it accrues, and that quality prompting can cost
   correctness. So: tests and conformance stay the gate; review is the loop; CLAUDE.md prose is not relied on.
8. **One measured ratchet, when it is cheap.** If a repo gets a quality metric in its gate, it is cognitive complexity
   mass (not mean, not function length, not worst-function, which penalises legitimate flat dispatchers), ratcheted
   only against its own measured baseline, paired with a trivial-wrapper count so splitting cannot game it. No
   baselines, no meters, no dashboards before someone needs one.
9. **Reviewers look for the named patterns**, nothing more elaborate: silent fallbacks, validation theatre, lonely
   interfaces, trivial wrappers and single-use helpers, duplicated cleanup paths, flags where a state enum belongs,
   long `&&`/`||` chains where data or a `match` belongs, bead or session references left in source, tracked WIP
   litter. The vocabulary for fixes is the eight moves masters make: turn a defensive check into an assert and delete
   the branch; change the representation so a special case disappears; give each rule one owner; separate mechanism
   from protocol; reduce what the reader tracks; name the idea; read in one linear pass; delete honestly.

## Next session, first

Review debt is real: about 700 commits in 48 hours, seven review documents, none for plugin, runtimes, driver,
conformance, arith, circuits or targets. First task: one batched review per repo under rules 2 to 6, plugin first.
Then new work resumes with rule 1 in force. Nothing else from this document needs building.

## Amendment 2026-11-07 (maintainer): velocity over repair cycles

Tally after 25 review rounds of the quality-floor programme: about 20 of 33 blocking findings met the strict test in
rule 4 (eight were soundness holes in the reference interpreter, the rest concrete rung-3 blockers); about 13 did not
(three successive lexical holes in a regex linter, four rounds on an estimator path no rung uses, overflow at
usize::MAX). Roughly a third of review effort bought no velocity. Hence the amendments to rules 3, 4 and 5 above and:

10. **Prototype mode.** The workspace is modular and every boundary is a published contract; the dialect already says an
    unavailable mechanic fails loud with its section number. A prototype may therefore land on `main` behind the gate
    after one review round with its known gaps filed as P2 beads, in the expectation of being replaced. Replacement is
    cheap because the contract is fixed. What may not land: a silent fallback, a narrowing of a rung path, or an
    unsound oracle (rule 4 a-c).
11. **Old unreviewed commits ride with the next job.** Commits already on a main without a review are covered by the
    review of the next job that touches that repo, in the same round, not by a separate main-branch review series.
12. **Gate before review, gate before push.** Unchanged and not relaxed: every job head runs the repo's full gate
    before its review is launched, and the push hook re-gates. The gate has caught what review missed three times.
