# HANDOFF — Bennett ecosystem (bennett-quantum)

Current state only; rewritten at session end. The narrative is the top block of `worklog/002_2026-11-02_orchestration.md`.
Rules: each repo's CLAUDE.md; council policy and rulings: `docs/council/README.md` (tail); ladder status and the ISA 0.9
adoption decision: `docs/plan/2026-10-29-path-to-north-star.md`. Orchestration state: `.tmp/orchestrator/shift-3.md` (running
table, queued work, decisions), advisor rulings `.tmp/orchestrator/advisor-notes.md` (07:55Z R1-R5 bind). Clock: read `date -u`
before any timestamp. Written 2026-11-02T08:05Z (shift 3, sonnet-docs-s3); rows move quickly, so re-run the commands below.

## Running (shift 3, from shift-3.md; check `pgrep -af codex_job` and `.tmp/orchestrator/tick.sh SECONDS`)

Codex sol xhigh, detached runners (resume a dead one with `python3 .tmp/orchestrator/resume_job.py NAME`): sol-vm-queue
(bennett-vm), sol-plugin-queue (bennett-plugin), sol-sched, sol-estimate, sol-ref09 (isa-spec reference interpreter),
sol-arith-softfloat, sol-runtimes-queue, sol-checker (bennett-conformance), sol-driver-queue, plus three new at
08:01-08:03Z: sol-isa-textdefects (isa-spec `docs/notes/2026-11-02-textdefects/`: fd0 and 0h4), sol-contract-pass2
(`docs/notes/2026-11-02-pass2/`), sol-dialect03-s0fix (dialect 0.3 draft, P0 beads d4s fa8). 12 runners.
Opus/Sonnet delegates (progress files named in shift-3.md): opus-vmfixes-review (branch vm-fixes), opus-design-reviews
(sched, estimate, vm-bjm), opus-checker-replay, opus-plugin-rung4, opus-gate-template, opus-council-s3 (l2p report first, then
contract-note rounds), sonnet-pushwave, sonnet-docs-s3 (this file and the worklogs).
In-flight push gate (owned by sonnet-pushwave): bennett-plugin 2aba17a with pinned roots (`bennett-plugin/.tmp/push-main.log`). Council: K82 Muse vote running (`tools/council.py`, log `.tmp/k82-muse/run.log`, run
`docs/council/isa-09-k82-2026-11-01`; a block reopens the round).
Heavy-gate rule (R3, binding): one full-width plugin CC gate or VM dual-engine run at a time; read `free -g` and `uptime`
first; children run no gates unless told.

## Main per repo (origin/main sha, then `git rev-list --left-right --count origin/main...HEAD`; at 2026-11-02T08:54Z)

| repo | origin/main | ahead | note |
|---|---|---|---|
| bennett | b6b4bb5 | 3 | pushed 08:47Z (gate tool, chunk-002 worklog); council rounds since are local |
| bennett-isa-spec | ecaaac0 | 18 | pushed 08:06Z (a3222b7..ecaaac0) |
| bennett-dialect-spec | 3e73596 | 2 | pushed 08:22Z via `gate_run`, interpreter pinned c1d1320 |
| bennett-targets | 4a74c62 | 3 | pushed by shift 2; gate.toml, stub, worklog local |
| bennett-conformance | b077ae2 | 14 | pushed 05:43Z; checker-replay, gate adoption, sol-checker wip local |
| bennett-arith | aab308f | 10 | not started in the push wave |
| bennett-circuits | 0ac4973 | 1 | pushed 08:35Z via `gate_run` |
| bennett-runtimes | ec52032 | 21 | gate RED again at ae7854f (`test_sqlite_memdb` query 18, runtime fault 7, deterministic; bead brt-fyv); not pushed |
| bennett-plugin | 157d4bd | 51 | push of 2aba17a gate still running |
| bennett-vm | d9cb684 | 15 | not started in the push wave |
| bennett-driver | 54d32fa | 7 | pushed 08:41Z, walk-back sha with artifact pins; `cd9219c..` waits on a runtimes publication |
| bennett-sched | 7f9ceb5 | 7 | pushed 08:04Z |
| bennett-estimate | d32ef4f | 6 | pushed 08:03Z |

Off-machine copy of everything unpushed: advisor's `wip/pre-outage-2026-11-02` branches in all 13 repos (and -bjm, -vmfixes,
-rung4). Newer wip commits from codex jobs are local only until pushed.

## Next, in order

1. Finish the push wave (R3 staggered): plugin (running), vm, arith, then runtimes (red at ae7854f on a deterministic SQLite
   memdb fault: needs the job's fix or an orchestrator ruling; the earlier green shas predate `gate.toml`, so `gate_run` exits 3),
   and driver `cd9219c..` after the runtimes publication. Read `tools/gate_README.md` before gating repos that have a `gate.toml`.
2. K82 Muse vote: when the call ends, `python3 tools/council.py aggregate --run isa-09-k82-2026-11-01 --round 1`, record the quota
   rows after, commit the run dir.
3. l2p (possible north-star gap: ISA §6.2 refuses the 4-T AND): the Opus report goes to the advisor before any council round.
   Then contract-note rounds (sol + astra), z4c first; fd0 and 0h4 after sol-isa-textdefects; the pass-2 notes
   after sol-contract-pass2. Dialect 0.3 to council after b-isa-spec-fuk.7.
4. Rung-3 `pins.json` refresh and rerun (brief sonnet-rung3 step 2) once plugin main lands.
5. Merges, each after review: vm-fixes after opus-vmfixes-review CLEAR (reference is the oracle at 0.8 where the text is silent);
   bjm-dense when green; rung4-plugin minus the 5u3 solver narrowing (b-dialect-spec-5u3, advisor ruling: not into main).
6. Beads left by the gate work: bennett-sched-68k, bennett-estimate-m6p, bennett-driver-3j4; b-dialect-spec-abf (120 s interpreter
   build on a cold cache). Remove the `*-muse2wt` worktrees (opus-design-reviews does it).

## Waiting on the maintainer

Nothing blocking. Standing decisions needed before they bite: the Muse seat for new contracts (the 2026-10-31 rule says a new
contract publishes only with the Muse vote; Muse is rationed to one call per contract after a quota reading and advisor
confirmation, so dialect 0.3 needs a substitute or a waiver); l2p, if the reader confirms a north-star gap.
