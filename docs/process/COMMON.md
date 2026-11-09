# READ FIRST: live rulings that changed since the rulebook was consolidated (edited in place; newest first; each line dies
# when its precondition does; the next shift deletes dead lines). Everything in advisor-notes.md and shift files is history.
- 2026-11-09 SINGLE SEAT. The laptop is retired; Spiral (64 threads, 62 GB) is the only machine and the only orchestrator
  seat. Every "laptop keeps X", lane split, relay ("wait for the relayed line"), hand-over hold and two-seat ownership
  line is void. All repos and paths belong to this seat's children under rule 3.
- 2026-11-09 NO HEAVY SLOT (maintainer, decided 2026-11-08T09:54Z, rulebook not edited until today: a heresy). Rule 5 below
  is the replacement: concurrent gates per repo, resource-guarded. Any brief, script or note that queues a gate behind
  another repo's gate, or speaks of "the slot", is wrong; fix it or report it.
- 2026-11-09 ONE GATE PER TREE, ENFORCED BY RECEIPTS. gate_run on meta main (>= e25f3aa) skips a tree that already holds a
  PASS receipt. It is live in a repo only when gate.toml tool_sha pins a meta commit at or after e25f3aa. Until the re-pin
  wave lands in all 12 repos, note in the shift file every gate that re-ran a receipted tree (that is waste to count,
  not a procedure to follow).
- 2026-11-09 PUBLIC REPOS. Every bennett-quantum/* repo is public. Code on wip/* branches is fine; transcripts, logs,
  memory, orchestrator or .tmp records never go there (private repo tobiasosborne/bennett-laptop-transfer or hand copy).
- 2026-11-08 RULINGS of 19:21Z (maintainer): b3ui = alternative A, normative inside ISA 0.9 K91, sol+astra review; rung-4(c)
  ideal target wording "an ideal quantum circuit with ideal logical qubits, implementing the standard quantum circuit
  model", never "all-to-all"; 0vi = coherent dialect 0.3 profile accepted explicitly, pins migrated, full identity/ABI
  coverage in the first fixture batch, unreachability by exhaustive small-domain execution. Items 1 and 3 share one council.

# Common rules for every Bennett child job (shift 1, 2026-11-01). Read fully; they bind.

Workspace: /home/tobias/Projects/bennett-workspace (sibling repos; meta repo `bennett/`). Project: Bennett, a compiler
and execution stack for reversible/quantum compute. Contracts: `bennett-isa-spec/spec/Bennett-ISA-Spec-0.9.md` (published
0.9, alongside 0.8), `bennett-dialect-spec/spec/`, north star `bennett/docs/Bennett-NorthStar.md`.

1. Read the CLAUDE.md of the repo you work in first. It binds. Highlights: red-green TDD; fail fast and loud (never
   silent returns or quiet fallbacks); exhaustive verification, "runs without errors" is not a pass; repos couple ONLY
   through published specs (never share or copy code across a contract boundary; running a sibling's published binary
   as a differential oracle is fine; reading the spec is the source of truth).
2. NO NARROWING of north-star scope. Nothing may reject, refuse, fault, declare inert or omit a capability the north star
   promises. A deferral postpones mechanics only. If a contract truly lacks something, file a blocker bead naming the
   exact change; never shrink scope to fit. Evidence labels must be honest.
3. Owned paths only: you write only inside the paths your brief lists. Other agents work concurrently in sibling repos and
   sometimes the same repo. Never `git add -A` at the repo level, never touch another job's paths, never `git stash`,
   `git reset`, `git checkout --`, rebase or force anything.
4. Commit your own paths regularly, at least every 30 min of work and at every green checkpoint:
   `git -C <repo> add -- <paths>; git -C <repo> commit -m "..." -- <paths>`, retrying after a few seconds on index.lock.
   End every commit message with the line: `Co-Authored-By: <your model name> <noreply@anthropic.com>` only if you are a
   Claude model; other models end with `Agent: <your model id>`. NEVER push: the orchestrator pushes `main`.
5. Progress file: keep the file your brief names current, as a Resume block only (done / verified with which command /
   next), rewritten in place after each milestone, never a per-pass log. If you are stopped at any moment, a successor
   must be able to continue from it plus the git log.
6. Headless, no /tmp: run every command with DISPLAY, WAYLAND_DISPLAY, DBUS_SESSION_BUS_ADDRESS and BROWSER unset and
   TMPDIR=<repo>/.tmp/<job>/tmp (mkdir it). Never run LLVM `-view-*` passes. Rust: CARGO_TARGET_DIR=<repo>/.tmp/<job>/target
   so concurrent jobs do not block on one another. Parallel width (build jobs, test threads, worker pools) comes from the
   repo's machine profile, kept beside its hang-guard class table; until a repo has one, derive it from nproc and
   MemAvailable with headroom for the other jobs on the host; never from a number in a brief. Long runs are bounded by the
   repo's hang-guard class table, never by a bare `timeout N`.
7. Checkpoints run focused tests; the full repo gate (`scripts/pre-push` or as your brief says) runs at bead close or
   stream end. Never run a full sibling repo's gate.
8. Stop rules: if THIS repo's gate goes red for a reason you cannot fix within your owned paths, stop and file a bead with
   the exact evidence; never revert (no "revert to green"), and never weaken, skip or delete a test or fixture to pass.
   Consumer gates in other repos are evidence, never a stop condition.
9. Beads: `bd` only, run from the repo's main checkout (no TODO files). File anything surprising or left over:
   `bd create` / `bd note`, with a determining sentence (what, where, evidence). Close with `bd close <id> --reason`.
   `bd export -o .beads/issues.jsonl` then commit that one file when you changed beads. Do not edit worklogs; the
   orchestrator writes them. A repo without beads uses the workspace rule: bd is initialised in all repos now.
10. Time: run `date -u` in the same command that writes a timestamp. Never infer time from work done.
11. Skepticism: reproduce rather than trust earlier claims, including docs in the repo; many READMEs lag the code. Your
    own "done" must name the command you ran and its result.
12. Do not ask questions; no human is watching. Make the reasonable engineering decision, record it in the progress file,
    and go on. A genuine contract decision goes in a bead and in your final message.
13. Final message (<=200 words): what landed (shas), what was verified with which exact command and result, what is open
    (bead ids), any surprise. Do not claim green without having run it.
14. Codex jobs: the sandbox cannot write sibling repos, including their bead databases. Append any cross-repo bead you need to `<repo>/.tmp/<job>/cross-repo-beads.md` (or your progress file) for the orchestrator to file, and continue. Never end JOB-BLOCKED for this alone.

## Anti-slop rules for code you write (added 2026-11-06, maintainer-ratified; from the SlopCodeBench reading)
The gate and the review are the loop; these rules are cheap help, not a substitute. Each is "bad -> good".
- Dispatch on data, not on chains. `if op == "add" {..} else if op == "sub" {..}` -> `match op { Op::Add => .., Op::Sub => .. }`
  over an enum parsed once at load. A string compared in more than one place is an enum that was never declared.
- State as one enum, not several flags. `done: bool, failed: bool, pending: bool` -> `enum State { Pending, Done, Failed }`.
- No silent defaults on failure paths. `map.get(k).unwrap_or_default()`, `.unwrap_or(0)`, `except Exception: return False`,
  `if (!p) return;` -> return an error that names the missing thing, or `assert` the invariant and delete the branch.
- Named predicates. `if a && (b || !c) && d.len() > 3 && ..` repeated -> `fn is_live_region(..) -> bool` with one owner.
- No magic numbers. `if width > 128` -> `const MAX_INLINE_WIDTH: u32 = 128;` next to the rule that needs it, with the spec section.
- One altitude per function. A function that parses bytes AND decides policy is two functions. Over 300 lines in semantics-bearing
  code is a review finding (plan target); split into named phases, each with a unit test, behaviour byte-identical.
- Delete, don't wrap. A helper called once, a wrapper that renames its callee, a `_v2` beside a `_v1`, a flag nobody sets: delete.
- No identifiers from the process in the product. Bead ids, job names, review round numbers, "shift 6", session dates: not in
  source comments, error strings, emitted output or fixture names. Test names and docs/reviews may carry them.
- No litter. Nothing under `__pycache__`, `*.pyc`, `*.log`, `LAST-RUN*`, `PROGRESS*`, lock files, `.darc` backups, scratch
  scripts or scratch markdown is ever committed. Stale markdown is polluted context for the next agent: keep HANDOFF/README
  statements true or delete them.
- A test must be able to see the bug it names. Tolerances no wider than the oracle allows; fixtures large enough to reach the
  branch; an assertion in every test; expected values hand-derived or from an independent oracle, never copied from the output
  of the code under test.

## Standing rules (consolidated 2026-11-08 from rulings R1-R42 after an independent Muse audit, rulings-review.md)
These ten rules are the whole orchestrator rulebook. Each names the PRECONDITION that justifies it; when that
precondition no longer holds as a checkable fact (spec pin, quota row, bead state, rung gate), the rule is dead:
a process-only rule (seats, pacing, slot order) is then ignored with one dated line in the shift Decisions naming
the evidence; a correctness rule (no narrowing, oracle soundness, gate integrity) is obeyed and escalated the same
turn. Two live rules in conflict: escalate, and meanwhile take the reversible branch. R-numbers in advisor-notes.md
are history, not authority; where that file and this one differ, this one wins. Adding an eleventh rule here
requires deleting or merging one in the same edit.

1. ORACLE PRECEDENCE. Where the pinned spec text is silent, the reference interpreter is the oracle and the silence is
   a text-defect bead; never gate behaviour the text does not specify. No narrowing (rule 2 above) is a repo law
   and always wins over any severity shortcut: a change that rejects or omits a promised capability is a blocker,
   not a P2, even if no current rung exercises it. [precondition: ISA 0.9 pinned; reference interpreter is the
   council-trusted executable model; expires when the text specifies the behaviour or 0.10 is pinned]
2. CHILDREN. Codex work is a `delegate_task` child (provider codex, gpt-6.1-sol, reasoningEffort xhigh) in an
   orchestrator-made worktree on `job/<name>`; it commits owned paths at green checkpoints, backs up to `wip/<name>`,
   keeps PROGRESS.md current, never pushes. The orchestrator merges `--no-ff` and pushes. [precondition: no CI
   (CLAUDE.md 6), delegate_task available; `codex exec` runners are banned]
3. ONE WRITER PER PATH SET. Parallel writers only on disjoint owned paths named in both briefs; whoever merges second
   gets the shared lines reviewed. A quality-baseline refresh (docs/quality.md or any shared ratchet file) is scoped to
   the writer's own rows, never a whole-file regeneration, with `git diff <base>..<head> -- <file>` as the pre-merge
   receipt (Spiral near-miss 2026-11-08: a regenerated baseline had tightened another lane's rows). [precondition: many
   concurrent children share one workspace]
4. ONE FULL GATE PER TREE. A tree is gated once; gate_run's tree-keyed PASS receipt makes every later run of the same
   tree (push hook, main-health, a re-run) a skip. Gating a receipted tree again is a defect to report, never a procedure.
   The job head runs the repo's full gate once before merge. Review may run before or after
   that gate; merge needs a gate PASS and a review disposition on the same head.
   The push hook is the single full gate where no pre-merge gate ran on that tree. A gate exits 0 on its own checks; milestone/blocker status is reported, never encoded as an exit code. A hang-guard trip is UNKNOWN: a distinct non-zero exit (124), neither PASS nor FAIL; the orchestrator re-runs once in a quiet slot, and a second UNKNOWN is a bead, not a gatefix. A gate or push runs DETACHED in its own systemd scope/unit (systemd-run --user), never inside an agent's background shell or chained after a waiter in one. [precondition:
   local gates cost 10 min to 8 h of one shared machine]
5. GATES RUN CONCURRENTLY, GUARDED BY RESOURCES, NOT BY A SLOT. There is no heavy slot and no slot order (maintainer
   direction, Spiral 2026-11-08T09:54Z). Gates and builds for different repos run at the same
   time, each detached in its own systemd unit; never two gates of the SAME repo at once (shared cache and target dirs).
   The only admission check is resources at launch: MemAvailable >= the gate's recorded peak RSS plus 6 GB headroom and
   load < nproc/2; a launch that fails the check waits on the condition, not on another gate. The rung-critical lane
   is never queued behind anything. [precondition: one 64-thread/62 GB host (Spiral) is the only seat; re-derive the
   two resource numbers from a receipt when the host changes]
6. SEATS. Editing children: sol xhigh only. gpt-6-astra: review and council only, never edits. Muse
   (muse-wonder-full-1.0): council seat pre-approved on every candidate rule 7 sends to council; an occasional
   ordinary review round is fine; never an implementer on main except by named maintainer exception; an erroring
   quota row is logged, not a block. After two failed sol rounds the escape is revert + spec-first re-land, not a
   different-model fixer. [precondition: maintainer findings of 2026-11-07 on sol/astra; re-read the Muse seat on 2026-11-10]
7. REVIEW: EVIDENCE-FIRST, TWO ROUNDS, RUNG-NAMED SEVERITIES. One fresh sol review that starts from the implementer's
   PROGRESS.md, gate log and red-first test, re-runs each claim, and reads the diff where evidence is thin. P0/P1 only
   for a wrong result or silent fallback on a named north-star §8 rung path, an unsound oracle (reference
   interpreter, checker verdict, certificate), or a broken build/gate/push hook; otherwise P2 = one bead, no repair
   round; at most one nit bead per review. After round 2: merge with P2 beads or revert the offending commit.
   Councils (sol + astra + Muse; blocking findings + <= 3 suggestions per seat) only for the reference interpreter,
   checker verdicts, certificates and published contracts; elsewhere one advisory round whose findings become beads.
   Gate-tightening changes: sol only. Prototypes land after one round with gaps as P2 beads, unimplemented mechanics
   failing loud. Old unreviewed main commits ride the next review of that repo. Any claim that an analysis reaches a
   least fixpoint carries an order-independence receipt: identical abstract values under original, function-reversed
   AND basic-block-reversed evaluation order (Spiral 2026-11-08: function reversal alone missed six order-dependent
   values). [precondition: the 25-round
   quality-floor tally (rounds 3+ bought little); demo-ladder stakes, no external consumers; revisit when main-health
   shows merge-attributable escapes rising]
8. LAND FAST, DETECT AFTER, REVERT WITHOUT CEREMONY. main-health (bennett/tools/main_health.py; status in
   bennett/.tmp/main-health/status.md) re-gates pushed mains and rungs 1-2 in the background and never blocks a push.
   A main or rung-1/2 red attributable to a merge for longer than one gate cycle: the owning lane reverts
   (`git revert -m 1`), pushes, files the bead, re-lands later; fix-forward only if the fix is already gated. Bugs
   may land; they must be found fast. No whole-repo graded quality re-audits (score documents); per-change evidence
   re-runs and main-health re-gates are not re-audits. One before/after table when a rung gate passes.
   [precondition: main-health actually runs each shift and its ladder rows are not ERROR; every main revertible]
9. NO BARE TIME LITERALS. Every time constant is a hang guard (per-repo class table short/moderate/long/eternal in one
   cited file, >= 10x measured on a named machine and date, machine factor in the same file, trip = UNKNOWN, per-command
   wall+CPU seconds recorded in the receipt), a performance assertion (deterministic work counts or in-process ratios,
   instruction counts where those are unavailable; regressions by change-point detection over history in main-health,
   never a threshold), or a product allowance (in the spec's unit, in spec/config, with its own fixture; a suite never
   inherits it as a cap). Tests wait on conditions, never sleep. Reviewers grade a bare literal P2, not a block. Briefs
   say "bounded by the repo's hang-guard class table", never "bounded" or "fast" alone. Orchestrator-process timers
   (commit cadence, slot windows) are exempt by name. [precondition: shared loaded machine, three documented false reds;
   per repo, the lint from the R42 sweep enforces this once landed]
10. QUOTA IS WEATHER, NOT LAW. Read `quota` before each launch wave and log the reading in the shift file; launch while
    the relevant provider is behind linear weekly pace. At or ahead of pace: launch nothing new except one named
    rung-critical child (logged as an exception), let running jobs stop after their current bead, and tell the advisor,
    who decides resumption. No quota state, cap, stream count or vendor preference is ever written into this rulebook,
    a brief or a memory as a standing fact (maintainer 2026-11-08: "a daily changing phenomenon, never a project ruling
    for all time"). [precondition: none; this is the procedure for reading weather, not a reading]

## Struck rulings (heresies: recognise and refuse them; dated when struck)
- Heavy slot / slot order / "one heavy gate at a time" / slot treaties (struck 2026-11-08, rulebook fixed 2026-11-09).
- Two-seat lane split, laptop ownership lines, advisor relay protocol (struck 2026-11-09: laptop retired).
- `codex exec` runners, codex_job.py / resume_job.py launches (struck 2026-11-06, R26).
- Gate-before-review AND push-hook re-gate of the same tree (struck 2026-11-08: tree-keyed receipts).
- "Codex banked resets are spare budget", "use up Muse before reset", Muse batching dossiers, any quota state as a rule
  (struck 2026-11-03 / 2026-11-08).
- Numbered R-rulings as authority; D9 seven-category councils; whole-repo graded re-audits (struck 2026-11-07/08).
- Bare wall-clock pass/fail limits in gates or suites (struck 2026-11-08, R42 sweep; residue is a P2 bead).
Rule-change procedure: a decision that changes a rule edits this file in the same turn (text in place, old wording struck
here), and the handoff of every shift carries a five-line rule audit: rules bent this shift, preconditions that lapsed,
lines above deleted. A rule bent twice is amended at that handoff, not excused a third time. For each rule name the
script that enforces it or mark it unenforced.

Publication note: historical host/session measurements and a provider reading were redacted;
all procedural rules and their preconditions remain. Read this file together with
[T3CHILD.md](T3CHILD.md), whose child-specific backup and Beads instructions apply to delegate jobs.
