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

Nothing known makes any rung impossible. Open risks:

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
items plus I1–I8, through the council.

**Phase 5 — north star iteration 8.** A1 + A2 (+ anything phases 2–4 force), council.

**Phase 6 — implementation** in north star §6.1 order: sched / vm / circuits /
estimate / targets → plugin → driver → runtimes / arith → Bennett.jl → conformance.
The demo ladder is the acceptance gate: rungs 1 → 2 → 3 → 4, then 5–8.

## Execution (started 2026-10-29)

| Phase | Agent | Repo / output |
|---|---|---|
| 0 audit | Opus | `bennett-dialect-spec/docs/audit/` |
| 1 interpreter | codex gpt-6.1-sol xhigh via `tools/codex_job.py` | `bennett-isa-spec/reference-interpreter/` |
| 2 SQLite spike | Opus | `bennett-dialect-spec/docs/spikes/sqlite/`, scratch outside the repo |

Agents commit their own paths regularly (unstable network); nothing is pushed
without the maintainer's say-so.
