# Code quality policy

**Status:** PROPOSED by the advisor on 2026-11-02 from the maintainer's instructions; the maintainer ratifies at the
start of the next session, then law 2 in each CLAUDE.md points here. Deliberately short: the maintainer wants no
administrivia, process theatre or review paranoia. If a rule here needs a form, a tracker or a ceremony, delete it.

## Review

1. **Code gets reviewed before it is pushed to `main`.** One implementer per change as before; review is batched over
   what the stream has landed since its last review. The orchestrator launches the review when a stream's batch is
   done, not per commit and not on a timer.
2. **Opposite model reviews.** Codex work is reviewed by Claude; Claude work by gpt-6.1-sol xhigh, the best reviewer.
   Sonnet is good at bug hunting and may run alongside. The reviewer gets the diff and the repo's laws, not the
   implementer's conclusions, and re-runs what is cheap.
3. **Three rounds, maximum.** Round 1 reviews, round 2 checks the fixes, round 3 is final. Anything still open after
   that is a decision for the advisor or maintainer, not a fourth round.
4. **Only P0 and P1 block.** P0: wrong result, silent fallback, spec violation, data loss. P1: a bug on a reachable
   path, a narrowing, a claimed behaviour without a test. Everything else is a nit: one bead labelled `nit`, swept
   later, never argued in-round.
5. **Stakes pick the seat.** Routine code: rule 2. Semantics-bearing code (executors, reference interpreter, plugin
   lowering, checker, certificates, scheduler core, soft-float): rule 2 plus one Muse call on the round that claims
   CLEAR, under the Muse quota policy. Published contracts, the gate itself, the scheduling interface, certificate
   schema and launch ABI: the council.
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
