The one Bennett rulebook (2026-11-11). Every repo's CLAUDE.md points here; where anything else disagrees, this file wins.

# Common rules

Maintainer, verbatim: "it is *totally fine* to ship and push bugs, as long as we can find and revert/fix forward easily."
And: "Rather favour super quick bug detection and robust rollbacks." When in doubt between more certainty before a push and a
faster push with detection behind it, take the faster push.

## Correctness (these bind everyone, always)
1. NO NARROWING. Nothing may reject, refuse, fault, declare inert or omit a capability bennett/docs/Bennett-NorthStar.md promises
   (thesis, §3-5, every §8 rung; Grover over unmodified SQLite is the core). A deferral postpones mechanics only; a missing contract
   feature is a blocker bead naming the exact change. Evidence labels are honest.
2. CONTRACTS ONLY. Repos couple only through published specs and pinned binaries (gate.toml pins); never share or copy code across a
   contract boundary, never read a live sibling checkout. Running a sibling's published binary as an oracle is fine.
3. OWNED PATHS. Write only the paths your brief names; one writer per path set; whoever merges second gets the shared lines into the
   next review.
4. RED-GREEN. Write the test, see it fail, make it pass. Expected values come from the spec or an independent oracle, never from the
   code under test. Never weaken, skip or delete a test or fixture to get green. Fail fast and loud: no silent fallbacks.
5. GIT. Explicit paths only (`git add -- <paths>`, `git commit -m ... -- <paths>`); never `git add -A`, stash, reset, checkout --,
   rebase or force. Every landing is one `--no-ff` merge into main, so `git revert -m 1 <merge>` undoes it.
6. HONEST EVIDENCE. "Done" names the command you ran and its result. A hang-guard trip is UNKNOWN, not PASS. Reproduce earlier claims
   before relying on them. Write timestamps from `date -u` in the same command.
7. PUBLIC REPOS. All bennett-quantum repos are public: no transcripts, logs, memory, .tmp records or host paths in any commit or branch.
8. HEADLESS. DISPLAY, WAYLAND_DISPLAY, DBUS_SESSION_BUS_ADDRESS, BROWSER unset; TMPDIR under the repo's .tmp/<job>/; never LLVM -view-*.

## Landing, detection, rollback
9. LAND on the fast tier: `scripts/pre-push` (gate_run pre-merge tier) green on the merged tree, then push. Nothing else is required.
   Work in progress on job/wip branches carries less: focused tests the child chooses; wip backups push with --no-verify.
10. DETECT after landing: main-health runs every pushed main with `--tier full --fresh` (long-tail checks live there) and compares
   with bennett/health/known-reds.toml. A NEW red is attributed to a merge and reverted with bennett/tools/revert_landing.py, or
   fixed forward if the fix is already on the fast tier. A standing red stays in the baseline with its bead until fixed. (Baseline
   and revert tool are being built on job/health; until they land, attribute and revert by hand: `git revert -m 1 <merge>`.)
11. REVIEW happens after landing, batched; findings become beads or a revert. Round 1 is the only open review: it lists blockers,
   everything else is a bead. A blocker bites on a real path in the repo as it is, not under a constructed configuration. Round 2
   exists only if round 1 had blockers: its brief is that list, it answers fixed / not fixed per item, and new observations are beads.
   There is no round 3: land, or revert and re-plan. Only the maintainer can authorise a third round.
12. TRIAL EXCEPTION (on audition since 2026-11-11, not settled): changes to the reference interpreter, checker verdicts,
   certificates, published contract text and gate tooling get rule 11's review BEFORE landing; nothing else does. Log one line per
   trial-class landing in docs/process/trial-exception.tsv (date, repo, what the review found: real defect / nothing / low-stakes,
   how long the landing waited). A later session re-examines it and drops it unless it has paid for itself.

## Launching, records, children
13. LAUNCH only when `python3 -I bennett/tools/admit.py launch --vendor V --kind K` says ADMIT; its reason names memory, disk, load
   and quota pace. The maintainer's numbers live in bennett/dial.toml and nowhere else. Gates run detached through
   `bennett/tools/gate_launch.py start|wait` (completion events in bennett/.tmp/gates/events/). Muse Wonder Full is kept to councils.
   (`launch` and dial.toml are being built on job/dial; until they land, read `quota` and never run a vendor ahead of its pace line.)
14. RECORDS are beads plus one live state file. Beads (`bd`, from the repo's main checkout) hold work items and findings; close with
   the command that verified it. The orchestrator seat's state is bennett/HANDOFF.md; a job's state is its .tmp/<job>/PROGRESS.md
   (done / verified by which command / next). No worklogs, shift files or per-pass logs. Councils commit report.md only.
15. CHILDREN work in the worktree and branch their brief names, commit at green checkpoints, back up to wip/<name>, never push main,
   do only the brief (anything else becomes a bead), never ask questions, and end with <= 200 words naming shas, commands and
   results, last line JOB-COMPLETE or JOB-BLOCKED: <reason>. Bead requests for a sibling repo go in .tmp/<name>/cross-repo-beads.md.
   Optional help for code style: docs/process/anti-slop.md.
