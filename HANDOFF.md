# HANDOFF — Bennett ecosystem

Current-state checkpoint: 2026-11-09. Recheck live Beads and local shift state before resuming work.

Bennett aims to compile unmodified LLVM-language programs into classical, reversible and coherent
quantum execution, including Grover search over SQLite. The plugin infers the required execution tier;
the driver links published runtime/arithmetic libraries and emits launchable objects. Independent
consumers implement two published contracts: the dialect and virtual ISA. Scope and acceptance are
in [the North Star](docs/Bennett-NorthStar.md), especially §§3–5 and the §8 demo ladder; unfinished
mechanics never reduce that scope.

## Workspace and repositories

Use sibling checkouts under `bennett-workspace/`. `bennett/` is the meta repository: manifest, tools,
cross-repo documentation and this handoff. The twelve active `bennett-quantum` component repos are:

| Repository | Role |
|---|---|
| `bennett-isa-spec` | Virtual ISA, object/launch/scheduling/certificate contracts, reference interpreter and conformance vectors |
| `bennett-dialect-spec` | LLVM marker ABI, normalisation, legality rules and reference semantics to the ISA |
| `bennett-plugin` | LLVM pass plugin: analysis, outlining, reversible/coherent lowering and ISA production |
| `bennett-driver` | Link-time orchestration, plugin invocation, fat-object/launch interfaces and comparison receipts |
| `bennett-vm` | Device execution, reversal, histories, effect tapes, simulation and launch/schedule consumption |
| `bennett-sched` | Scheduling, source expansion, resource accounting and certificate production |
| `bennett-circuits` | Bounded circuit specialisation, placement, proof-carrying output and exporters |
| `bennett-estimate` | Resource estimates from objects, schedules/certificates and named targets |
| `bennett-targets` | Target descriptions, independent validation and hardware-model importers |
| `bennett-runtimes` | Ordinary runtime C/LLVM bitcode: allocator, libc/musl helpers and device models |
| `bennett-arith` | Arithmetic bitcode and ISA circuit libraries with certificates |
| `bennett-conformance` | Demo ladder, independent certificate checker and differential/conformance harnesses |

[manifest.toml](manifest.toml) also lists `Bennett.jl`, the Julia frontend/research lab, as an
information-only personal repository. It is outside the twelve component repos and clone/update set.
Repos communicate through published specs and versioned binary interfaces; each `gate.toml` pins its
inputs. A live sibling checkout is not a substitute for a pin.

## Contract and implementation checkpoint

ISA 0.9 is published alongside 0.8; reference and consumer migration remains partial. The dialect's
classical R profile `0.3-r1` was accepted for rung 3 (`bennett-dialect-spec` merge `4bca41b`). That
acceptance does not establish the coherent profile needed for function pointers inside lifted oracles.
Check each producer's version declaration and gate pins before combining publications.

Verified main ancestry includes ISA reference CLI memory-file support and K93 (`f7cb01b`), plugin
analysis counters and vector production work (`abe5557`), VM sparse pages/journals (`99f938c`),
estimator terminal-recompute work (`923f185`), arithmetic pooled publication receipts (`cd245bc`),
and explicit ladder revision selection (`bennett-conformance` `12134af`). These landings are partial
capabilities, not acceptance of a whole rung or completion of their umbrella beads.

## Demo ladder

Recorded acceptance below is tied to its recorded inputs; no ladder run was performed for this edit.
Evidence lives in `bennett-conformance/ladder/rung-N/RESULTS.md`, associated reports and `blockers.json`.

| Rung | Demo | Verified recorded status |
|---|---|---|
| 1 | Scalar C, Rust, Julia | Full-domain acceptance remains blocked in committed evidence: `bp-75y`, `bp-xb8`, `bp-zeg`; input-only diagnostic passes do not establish full D. |
| 2 | Pointers, structs, byte memory | Recorded COMPLETE on 2026-11-01: hashtable forward equals native, then byte-exact reversal, both executors and LLVM majors. See that run's frozen pins. |
| 3 | musl hello-world | Acceptance outstanding (`bennett-conformance-7bx`); formatted-musl production, native agreement, reset and strict replay remain unmeasured in the latest committed results. |
| 4 | Grover over unmodified SQLite | Acceptance outstanding (`bennett-conformance-tmb`). The November 8 main-snapshot run failed on arithmetic publication/pin compatibility; estimator schema and checker CLI diagnostics also failed. |
| 5 | Julia shim runtime | Acceptance requirement only; rung directory contains a README, no executable gate/results. |
| 6 | xv6, then Linux | Acceptance requirement only; rung directory contains a README, no executable gate/results. |
| 7 | Quantum kernel fuzzing | Acceptance requirement only; rung directory contains a README, no executable gate/results. |
| 8 | C Monte Carlo amplitude estimation | Acceptance requirement only; rung directory contains a README, no executable gate/results. |

Rung 4 still requires all three North Star clauses: exhaustive oracle checks through N ≤ 2^10,
Grover simulation through N ≤ 2^8, and a budgeted, padded estimate at N = 2^20. Reduced controls,
measured-basis diagnostics and a small fixture estimate cannot satisfy those clauses.

## Open critical path

- **SQLite analysis:** the `job/s2-gai-fix` / `job/s2-9cy` stack remains outside main. Resolve
  `bennett-plugin-4zi` (TOP/mask provenance), `bennett-plugin-ge7` (sound external-state premises)
  and `bennett-plugin-9cy` (ICmp monotonicity). Fixpoint evidence must agree under original,
  reversed-function and reversed-basic-block order. Remaining work includes `bp-6rz` and SQLite
  vector/fixpoint umbrellas `bp-1bb` / `bp-fj1`; counters/production landings did not close them.
- **ISA checker contracts and consumers:** K85 `b-isa-spec-qrc` is unfinished; its repaired candidate
  is on `job/isa-k85-land`, awaiting the resumed council disposition and landing. K86
  `b-isa-spec-0ib` is partial. K89 `b-isa-spec-t9l` blocks the scheduler's parked
  `job/sched-vt8` reader/adoption work. Track the remaining K85–K92 work in ISA Beads.
- **K91 and coherent function pointers:** `b-isa-spec-b3ui` and `bennett-0vi` remain open. The
  accepted direction is explicit per-role `token_aliases/1` negotiation inside ISA 0.9 K91, plus
  explicit coherent dialect 0.3 acceptance and pin migration. Identity/ABI fixtures and executed
  unreachable-site evidence are required; classical R-profile acceptance is insufficient.
- **musl/native comparison:** `brt-yz5` remains open in runtimes. The parked varargs repair
  needs a spec-first re-land using each LLVM major's own layout, before further printf promotion.
- **Rung-4 checking and cost:** `bennett-conformance-51d` covers the real fixed-image verdict and
  gate/checker CLI mismatch; `bennett-estimate-b8o` still needs the full SQLite ISA launch. Report
  padded cost using an ideal quantum circuit with ideal logical qubits, implementing the standard
  quantum circuit model; report the illustrative superconducting target's capacity shortfall
  separately. Target publication and estimator/ladder re-pins must agree.
- **VM:** `bennett-vm-o7n` remains open for launch/estimate ABI correctness; do not advertise alias
  support before it works. Slice 4 (`bennett-vm-4pj`, prepared commits) and slice 5
  (`bennett-vm-p7f`, interval locks), then the dense engine (`bennett-vm-bjm`), remain unfinished.
- **Evidence and infrastructure:** `bennett-wa1` tracks the outstanding independent review of
  strict-order landings; `bennett-b78` tracks machine-derived parallelism. Remaining hang-guard
  sweeps and consumer gaps stay in each repo's Beads; `bennett-cbj` tracks an intermittent receipt
  CPU-accounting test failure. Recompute proof extensions remain open as
  `bennett-estimate-e9a.1`. Keep the future mixed native/device boundary reachable (`bennett-4ht`).

## Orchestration and durable state

Spiral is the single orchestrator seat (64 hardware threads, about 62 GB RAM); the laptop retired
on 2026-11-09. Old seat ownership, relay and gate-slot instructions have expired. Read the target
repo's `CLAUDE.md` / `AGENTS.md`, then the local rulebook
`bennett/.tmp/orchestrator/briefs/COMMON.md` including its READ FIRST block. Children also read
`briefs/T3CHILD.md`. COMMON is the rulebook; historical advisor/shift notes are evidence.

Live issue state is `bd` in each repo's **main checkout**, not an old JSONL export. Use `bd ready`,
`bd show <id>` and `bd note`/`bd create`; the orchestrator exports Beads when landing. Current local
operations are in `bennett/.tmp/orchestrator/spiral-2.md` (Running, Decisions, Landed); earlier
handoffs are in `spiral-1.md` and `shift-16.md`. A child's resume point is its assigned
`.tmp/<job>/PROGRESS.md` plus git history. Recheck these changing records instead of reviving an old queue.

All `bennett-quantum/*` repos are public. Keep transcripts, logs, memory, orchestrator records and
`.tmp` artifacts out of commits and public backup branches; reference local records by path only.

## Landing work

Work in the assigned `job/<name>` worktree and owned paths. Commit explicit paths at green
checkpoints, back up code to `wip/<name>` as authorised, and hand the head to the orchestrator;
children do not push main. The orchestrator obtains the required review/council disposition,
merges `--no-ff`, exports Beads, and pushes. Preserve review and gate evidence for the same content.

There is **one full gate per content tree**. `tools/gate_run.py` reuses a PASS receipt keyed by tree,
actual gate-tool SHA and isolation mode; a changed tree/pin needs a new gate, and FAIL has no PASS
receipt. Receipt support starts at meta `e25f3aa`; all twelve local component mains now pin tool
`3779522`. Check the live shift file for their gate/push outcomes rather than assuming deployment.
The meta gate is `scripts/pre-push`; the orchestrator runs it at merge.

Gates/pushes run detached in their own systemd units. Different repos may gate concurrently when
resources permit; never run two gates of the same repo. Admission, machine-derived widths and
hang-guard classes follow COMMON and the repo profile. A hang-guard trip means UNKNOWN, not PASS.
