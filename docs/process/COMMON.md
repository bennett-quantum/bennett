The Bennett rulebook. Only the maintainer changes a line here; anyone else proposes one sentence to the maintainer.
Other files may add what is specific to one repo; they never restate or override this file.

# Common rules

## Invariants: wrong in every circumstance
1. No narrowing: nothing may reject, refuse, fault, declare inert or omit a capability bennett/docs/Bennett-NorthStar.md
   promises. A contract that lacks something gets a blocker bead naming the exact change.
2. Write only the paths you own.
3. Repos couple only through published contracts and pinned binaries: never copy code across a contract boundary, never
   read a live sibling checkout.
4. Git: name paths explicitly; never stash, reset, rebase, checkout --, force or `git add -A`.
5. Honest evidence: claim only what a command you ran showed. A timeout is UNKNOWN, not PASS.
6. Nothing private in the public repos: no transcripts, logs, memory, .tmp records or host paths.
7. A behaviour change comes with a test that fails without it.
8. Headless: DISPLAY, WAYLAND_DISPLAY, DBUS_SESSION_BUS_ADDRESS and BROWSER unset; TMPDIR under the repo's .tmp/.

## Defaults: depart from one when that keeps work moving and is reversible, and say so in one line.
## A default never blocks ready work; if it seems to, the work wins.
9. Do it directly: whoever sees a change makes it, runs the fast tier, pushes. Delegate only when the work is big
   enough or independent enough that parallelism pays.
10. Land on the fast tier (`scripts/pre-push`), one `--no-ff` merge per landing; full tiers run after landing in
   main-health; a new red is reverted (`git revert -m 1 <merge>`) or fixed forward. Maintainer: "it is *totally fine*
   to ship and push bugs, as long as we can find and revert/fix forward easily."
11. Review is after landing. One open round lists blockers (a blocker bites on a real path, not a constructed one);
   everything else is a bead. A second round only confirms those blockers are fixed. There is never a third.
12. TRIAL EXCEPTION (on audition since 2026-11-11, not settled): changes to the reference interpreter, checker
   verdicts, certificates, published contract text and gate tooling are reviewed BEFORE landing; nothing else is.
   Log each such landing in docs/process/trial-exception.tsv; a later session drops this unless it paid for itself.
13. Reasoning effort fits the task: high by default, maximum only for hard design or analysis.
14. One orchestrator talks to the maintainer directly; there is no standing advisor layer.
