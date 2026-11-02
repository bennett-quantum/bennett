# Path to the north star — plan and real blockers (2026-10-29)

Recorded at the maintainer's request after the legality spike and dialect draft 0.1.
Living document: update it when a phase completes or a risk is resolved.

## Standing rule: no narrowings

**The maintainer accepts no narrowing of north-star scope of any kind.** If reaching
the north star needs more work, the work gets done. Grover over unmodified SQLite
(north star §8 rung 4) is the core value proposition. A deferral may postpone
*mechanics* while keeping the capability; a default of "reject", "none" or "fault"
for something the north star promises is a narrowing and comes to the maintainer as
a blocker with the work needed to remove it. When a contract truly lacks what the
north star needs, that is a blocker to raise, never a reason to shrink a spec.

Why this is written down: dialect draft 0.1 (`../../bennett-dialect-spec/spec/`,
commit 255b0f4) deferred lifting of memory, calls, floating point and vectors in
oracles to what its scalar-only pre-flight checker could execute (its D4), although
ISA 0.8 provides `lift.load/store/alloc/free/call` and a lifted memory model
(ISA §4.2, §7.2). That excluded rungs 2, 4, 7 and 8. Root cause: the only executable
ISA model (`isa_check.py`) covers a scalar subset, and the drafting brief asked for
"a default plus a deferral rather than a sketch" without stating the north star as
hard scope.

## Real blockers and risks

Nothing known makes any rung impossible. **Rung 4 (Grover over unmodified SQLite) is shown
feasible on ISA 0.8 with no ISA change** (phase 2, 2026-10-29); what remains is dialect, plugin,
runtimes, arith, driver and executor work, plus structure recovery for a meaningful 2^20 estimate.
Open risks:

| # | Risk | Kind | State |
|---|---|---|---|
| R1 | Coherent lifting of classical code under `ctrl` (taint-inferred outlining into lifted oracles, copy management) | hardest design problem | ISA 0.8 permits it (actions call oracles); unspecified; draft 0.1 dodged it (D17) |
| R2 | Function pointers inside lifted oracles (address encoding + compare-and-branch dispatch to static `lift.call`) | design | `qjumpr` is intra-function and `lift.call` is static (ISA §4.2); likely no ISA change; unverified |
| R3 | The 11 ISA open items of draft 0.1 (ISA-1..ISA-11: handle tables in device memory, host memory by reference, non-consuming measure, …) | possible ISA gaps | unverified; ISA-4 (`qreg` only in the classical environment, ISA §3.2) looks genuine and blocks handle tables in memory, not rung 4 |
| R4 | Measurement-based uncomputation under control (north star §9.6) | research | open; unitary uncomputation is the stated fallback |
| R5 | Step-machine cost on SQLite-sized closures (dispatch over every row per step) | performance | rung 4 (a)/(b) use branch enumeration and avoid it; (c) estimates need structure recovery (ISA open item I2) |
| R6 | ISA "settled" while R3 may require ISA 0.9 | maintainer decision | ISA I1–I8 already filed |
| R7 | Codex content filter on security-adjacent work (rung 7 is kernel fuzzing; the legality harness was stopped once) | tooling | assume no Daybreak access (maintainer, 2026-10-29). Mitigation: `tools/codex_job.py` resume/fresh-session recovery, neutral engineering wording in briefs, and security-adjacent workstreams (rung 7 oracle, sanitiser-style harnesses) run on Claude agents rather than codex |
| P1 | Pre-flight checking limited to the scalar subset | process | fixed by phase 1 |
| R8 | **Mixed fat object lock-out.** The selective-module experience (ordinary native binary, only marked modules become VM objects, north star §2, §3.3, §4.4 launch ABI) is the star to follow but far off; every rung today runs the whole program on the device against a separately built native binary, no launch ABI is defined, no host shim gives markers classical semantics. **Maintainer 2026-11-02: no early architecture decision may lock it out.** Object format, certificates, launch API, budgets, handles, effect tape and host-memory decisions must state how a mixed binary would use them or name the change needed; nothing may assume the device object is the whole binary | design constraint | standing; bead bennett-4ht; council rubric check for ISA and dialect rounds |

Facts checked in ISA 0.8 for this plan: run-time budgets exist through the launch
API (`bennett_budget(...)`, ISA §10); oracle memory starts as zero plus global
images with mapped input interface regions (ISA §3.7, §7.2), so a database prepared
before entry is either built inside the oracle (cost, not narrowing) or needs a
layout/launch mechanism (phase 2 decides).

## Phases

**Phase 0 — audit dialect 0.1 for narrowings.** Every §1.4 departure and every
deferred decision D1–D25 classified: mechanics-only deferral (keep) vs capability
narrowing (remove, with the mechanism needed). Known narrowings beyond D4: D2, D6,
D10, D11, D16, D17, D19, D21, D23. Output: `bennett-dialect-spec/docs/audit/`.

**Phase 1 — full ISA reference interpreter (Rust, `bennett-isa-spec/reference-interpreter`).**
ISA §14.1 for all tiers and rows, lifted memory, calls, alloctab, budgets, faults,
prefix reversal, Q-tier state; red-green against §16.3 and `isa_check.py`. Implements
the ISA, does not change it. Critical path for every later pre-flight checker and
for VM differential testing.

**Phase 2 — rung-4 feasibility spike (SQLite).** Unmodified SQLite (build flags
recorded), in-memory database, a real SQL predicate over a superposed `rowid` as the
oracle. Inventory of the oracle's whole callee closure by construct (memory, direct
and indirect calls, FP, vectors, varargs, setjmp, libc, effects), each mapped to ISA
rows or recorded as a gap. Output: `bennett-dialect-spec/docs/spikes/sqlite/`.

**Phase 3 — dialect 0.2, no narrowings.** Full lifted subset, indirect-call dispatch,
function-address encoding, soft-float, vector scalarisation, effect virtualisation,
taint-driven outlining under `ctrl` (R1), dirty borrowing, budget tables, mixed-major
links. Pre-flight against the phase-1 interpreter. Council rounds to acceptance.

**Phase 4 — ISA 0.9, only on evidence and with the maintainer's go.** Verified R3
items plus I1–I8, through the council. **Evidence done 2026-10-29**
(`../../bennett-isa-spec/docs/notes/2026-10-29-isa-09-evidence.md`): no proved ISA gap blocks any rung at its
fixed demo width; the four BLK items plus ISA-7/ISA-8 and an observable zero fault code are genuine gaps
against the north star's general promises; the rest is wording or efficiency. **Maintainer 2026-10-29: draft 0.9
now, alongside 0.8** (`spec/Bennett-ISA-Spec-0.9-draft.md`, 0.8 untouched), one combined council dossier;
**grade it only after** (a) the reference interpreter is council-accepted (trusted precheck) and (b) dialect 0.2
has had its first council round. Dialect 0.2 stays graded against 0.8 with `blocked:` verdicts; a dialect 0.3
round follows 0.9 acceptance.

**Phase 5 — north star iteration 8.** A1 + A2 (+ anything phases 2–4 force), council.

**Phase 6 — implementation** in north star §6.1 order: sched / vm / circuits /
estimate / targets → plugin → driver → runtimes / arith → Bennett.jl → conformance.
The demo ladder is the acceptance gate: rungs 1 → 2 → 3 → 4, then 5–8.

## Execution (started 2026-10-29)

| Phase | Agent | Repo / output |
|---|---|---|
| 0 audit | Opus | `bennett-dialect-spec/docs/audit/` |
| 1 interpreter | codex gpt-6.1-sol xhigh via `tools/codex_job.py` | `bennett-isa-spec/reference-interpreter/` |
| 4 evidence | codex gpt-6.1-sol xhigh | **done 2026-10-29**: `bennett-isa-spec/docs/notes/2026-10-29-isa-09-evidence.md` |
| 4 draft 0.9 | Opus | in progress 2026-10-29: `bennett-isa-spec/spec/Bennett-ISA-Spec-0.9-draft.md` |
| 1 council loop | council fable/astra/muse; Opus implementer | round 1 2026-10-29: 30 blockers, no consensus; loop until acceptance |
| 2 SQLite spike | Opus | **done 2026-10-29**: `bennett-dialect-spec/docs/spikes/sqlite/REPORT.md` — rung 4 needs **no ISA change**; database as SQLite file image in an oracle `in` region (memdb VFS); B ≈ 2.9e5 rows/call, flat in N; ≥ 92 % rowid-invariant; 13 ranked work items |

Agents commit their own paths regularly (unstable network); nothing is pushed
without the maintainer's say-so.

**Executors:** bennett-vm gains a dense state-vector engine (bead bennett-vm-bjm, qHiPSTER-style blocking, fusion and threads, std-only, evidence-labelled `numerical`) beside the exact sparse engine, for rung 4(b), 7(b), 8(b); the exact engine stays the semantic reference.

## Ladder status (kept current by the orchestrator; evidence in `bennett-conformance/ladder/rung-N/RESULTS.md`)

| Rung | Status | Date | Evidence |
|---|---|---|---|
| 2 hashtable | **complete**: gate exit 0, every stage PASS on LLVM 18 and 23, both executors (forward = native on ten cases, byte-exact reversal) | 2026-11-01T13:06Z | `ladder/rung-2/RESULTS.md`; blockers closed in order: brt-3sa, bp-au6, bp-1us, bp-tav, bp-9fo, bp-bux, bennett-vm-ol3, b-isa-spec-n8j, bennett-vm-fw8 |
| 3 musl hello-world | gate built; blockers in pipeline order: brt-1ft musl sysroot **closed**, brt-cgb console device **closed** (runtimes M2: musl 1.2.5, console model), bp-ivy plugin R-mode integration (pass running), bennett-driver-cyg (M1 landed; cyg.3 native comparison integrating the runtimes' native closure, pass running), b-isa-spec-221 **closed** (already determined by K5/§4.9/§10; fuk tracks 0.8 migration), b-isa-spec-04d **closed** (reference `--tape-out/--replay-tape`), bennett-vm-u8m **closed** (VM matches) | 2026-11-01 | `ladder/rung-3/RESULTS.md` |
| 1 scalar C/Rust/Julia | gate built; C passes end to end on LLVM 18 and 23, both executors (659,456 executions, no mismatch or fault); Rust and Julia run on the LLVM 23 pipeline only (ruling: §19.8 accepts older IR and forbids newer; stock rustc emits 23.1.1, Julia 20.1.8; no downgrade, no language dropped) and are blocked on plugin beads bp-xb8 (Rust personality) and bp-zeg (Julia gcstack); exhaustive full-D rows blocked on bp-75y (comparison layout option) | 2026-11-01 | `ladder/rung-1/RESULTS.md` |
| 4 Grover over SQLite | gate built, red on both majors at the first true blockers: brt-dj7 (libc closure), bp-1bb (vector GEP), then bp-fj1 (analysis fixpoint on 1,218 functions), bp-vsa; native image = independent predicate up to 2^20; stages past production have never run; spike 2026-10-29 needs no ISA change | 2026-11-01 | `ladder/rung-4/RESULTS.md`, `DESIGN.md`; tracking bennett-conformance-tmb |

The consumer chooses the next pass: each rung's gate files the blockers in the owning repos, and those beads are the work
plan (maintainer 2026-10-31).

## Decision 2026-11-01T15:14Z — ISA 0.9 adoption, driven by rung 3

Rung 3's reversible tier needs the typed R faults that only ISA 0.9 defines (K5: §4.1, §4.9, §7.4, §10, T4); dialect
0.2.10 §11.5/§17.6 therefore reports BD-B-ISA7 for every R entry on 0.8, and the reference interpreter admits only 0.8
(bead b-isa-spec-fuk). The executors and the producer migrate explicitly to ISA 0.9, consumer-driven by the rung-3
gate, with 0.8 behaviour retained byte-for-byte:
- reference interpreter: admit and execute 0.9 objects (pass running: envelope dispatch, K5 typed faults, bound ref
  library with K77, K79-K81 end to end, saved-tape profile on 0.9 objects); council acceptance round after;
- bennett-vm: 47t-d schedule admission/realisation/execution (in its queue; c2 running);
- bennett-plugin: `-bennett-isa=0.9` producer mode after pass 16 (never a silent change of the 0.8 output);
- bennett-dialect-spec: 0.2.12 (consumer gaps, running) then the 0.3 track with grading target ISA 0.9;
- pins move only after verification, per repo, by their owners (no silent 0.8 mutation).
