# HANDOFF — Bennett ecosystem

Current-state checkpoint: 2026-11-12 (laptop session; see "2026-11-12 session" below). Workflow reform 2026-11-11; product lanes as of 2026-11-09 unless that section says otherwise. Beads triaged 2026-11-11: deferred
beads carry label `triage-2026-11-11`; `bd ready` shows what blocks a rung. Recheck live Beads.

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
| 1 | Scalar C, Rust, Julia | Blocked in committed evidence: `bp-75y` (C native comparison; plugin fix on `job/75y`, consumer `bennett-conformance-fki`), `bp-xb8`, `bp-zeg`. main-health re-runs it on pushed mains; input-only diagnostic passes do not establish full D. |
| 2 | Pointers, structs, byte memory | Recorded COMPLETE on 2026-11-01: hashtable forward equals native, then byte-exact reversal, both executors and LLVM majors. See that run's frozen pins. |
| 3 | musl hello-world | Acceptance outstanding (`bennett-conformance-7bx`). Last complete gate run 2026-11-12 (conformance `4432021`, plugin `5a9d8a2`, loaded host): LLVM 18 34 PASS / 3 FAIL / 8 BLOCKED, LLVM 23 35 / 2 / 8. Hello passes forward/native equality, reversal, reset, saved-tape replay and corrupt-tape rejection on both executors, but its native-comparison PASS is unverified for acceptance (§17.7 source classification missing, see below). printf_fmt compiles on both majors; its executor and native rows hit the gate's 300 s limit (UNKNOWN, not verdicts). No gate run yet on plugin `f7ea5ad` (varargs) or conformance `cabc240` (process preparation). |
| 4 | Grover over unmodified SQLite | Acceptance outstanding (`bennett-conformance-tmb`). The November 8 main-snapshot run failed on arithmetic publication/pin compatibility; estimator schema and checker CLI diagnostics also failed. 2026-11-12: the plugin analysis has never completed on full SQLite; investigation findings 14-21 are on plugin branch `wip/sqsize` (see below). |
| 5 | Julia shim runtime | Acceptance requirement only; rung directory contains a README, no executable gate/results. |
| 6 | xv6, then Linux | Acceptance requirement only; rung directory contains a README, no executable gate/results. |
| 7 | Quantum kernel fuzzing | Acceptance requirement only; rung directory contains a README, no executable gate/results. |
| 8 | C Monte Carlo amplitude estimation | Acceptance requirement only; rung directory contains a README, no executable gate/results. |

Rung 4 still requires all three North Star clauses: exhaustive oracle checks through N ≤ 2^10,
Grover simulation through N ≤ 2^8, and a budgeted, padded estimate at N = 2^20. Reduced controls,
measured-basis diagnostics and a small fixture estimate cannot satisfy those clauses.

## 2026-11-12 session (laptop seat; the usual host was offline)

Process: COMMON.md rule 14 now reads "a persistent advisor ... launches targeted orchestrations". Two ran today: rung 3 to
acceptance, and sizing the full-SQLite analysis. No bead was written on this host (its bead databases are stale against
origin): everything bead-worthy is listed here and must be filed. Post-landing review ran for four landings (below); the
others are unreviewed.

**Landed and pushed.** Plugin: `034a8da` (bp-owg, PT9 byval snapshot), `aeb688f` (regression test for the classical-call
marker crash), `b120196` (single-pass address relocation at link), `4884eee` (exit-zero widening uses zext, ISA §3.3),
`5a9d8a2` (analysis work reduction, results identical), `f7ea5ad` (analysis models varargs per dialect §14.3; UNREVIEWED,
and printf CPU against the 30 s allowance must be re-measured on it). Conformance: `bbc0644` (isolated hosted native
provider), `335244a` (argv launch replies), `cabc240` (gate produces through the driver's §19.2 process preparation, so
`exit` flushes stdio; UNREVIEWED), pin bumps `d40f4ef`, `4432021`, `2146ef5`.

**Rung 3, open causes (to file as beads).**
- REVIEW BLOCKER on `bbc0644`: native comparison can PASS without the §17.7 source-definedness classification. The gate
  hands the driver only materialised bitcode; recorded classifier results are `blocked` (UBSan: original C input required;
  ASan: freestanding ASan runtime not published). Fix queued, not started: pass the original C, require the classifier
  results the text requires, and settle from §17.7 whether the ASan classifier is required (if so, a runtimes/driver gap).
- Executors do not scale to the 63 MB printf object: linear block lookup by name in the VM (`wip/r3blk`, bennett-vm) and
  in the reference interpreter (`wip/ref-blocks`, bennett-isa-spec; rule 12: independent review BEFORE landing, vectors
  byte-identical, then log in trial-exception.tsv and bump the rung-3 pin). One reference forward run with an exit path
  was killed at 12 GB after ~500 s: growth not yet measured (same job).
- The rung-3 gate builds VM/provider/driver in debug; switch to release if only the recipe chooses it.
- Analysis nondeterminism (inherited): host discovery inserts into a pointer-ordered set while traversing it, so the
  round count (4 vs 5 on soft-float) and CPU vary with allocation addresses. Not started.
- PT9 under-approximation (inherited, soundness): an 8-byte `byval` subrange of a larger filled buffer drops the fill.
  Failing input kept by the reviewer. Not started.
- The analysis CPU allowance is thread CPU time: LLVM 23 printf used 27.5 of 30 s unpinned and the verdict depends on core
  type (this host has P- and E-cores). Maintainer question: a work-count budget would be machine-independent.
- Printf object size is dominated by compare-tree dispatch (178k `fault`, 223k `icmp.eq` lines): a plugin-side lever.

**Rung 4 / SQLite analysis (plugin `wip/sqsize`, design log findings 14-21; all on a rebuilt input, the frozen one was on
the offline host).** Measured: (1) the analysis did not model varargs, so SQLite had no heap in it and every earlier
SQLite number came from an unsound model (fixed in product by `f7ea5ad`); (2) PT11 seeds unknown inputs on ~1,386
host-reachable functions where three are true roots: a spec reading question ("host caller"/"host code" are undefined);
(3) §5.1 gives SQLite one heap object, but per-call-site heap naming changed nothing measurable; (4) an exact fix exists
for a `copySlotFamily` loop of ~9.2e18 identical iterations (slot width 2^64-1 from an unknown-size allocation), not
landed; (5) SVF (field-sensitive Andersen) on the same module finishes in 3.5 min / 2.6 GB with equally coarse sets
(avg ~300 objects, 38 indirect targets per site), so coarseness is normal and the cost is not; (6) round-1 CPU is 85% one
linear family-slot scan in `Analysis::store`; widening the address domain does not buy convergence; a worklist saves
0-20% in early rounds. Next: index that scan exactly, re-profile, repeat until the profile is flat (stop rule in the
log); then a fixpoint run and the lowering measurements (candidates per indirect site, ⊤ function pointers, BLK-1
operands). Idiom micro-benchmarks (plugin `wip/idioms`): benign = direct calls, constant-index data, bounded array
walks, resolved function tables, memcpy, string tables; superlinear = malloc-linked lists/trees, struct-stored callbacks,
many-site variadics, pointer/integer round trips and subtraction. Open: classify each quadratic (output size / rounds x
re-step / per-step cost), then pairwise combinations.

**Host notes.** Two beads exist only in this host's local commits (isa-spec `8sp6` reference interpreter 26x slower on
the plugin entry-snapshot workload; dialect `29m` §5.2(ii) dispatch row-cost formula understates), unpushed with small
local merge commits in isa-spec, dialect-spec, driver and runtimes. `tools/admit.py` cannot probe quota on this host.

## Open critical path (lanes; order binds within a lane only)

2026-11-11 product lanes in flight: plugin j3l (rung 4) and 7qi -> s59 (rung 3); conformance 51d -> fki (rung 1); isa-spec
x2n headers and k86 scoped round (trial class: reviewed before landing); circuits fc8/exporter stage 1; arith gdg. Landed:
plugin 904e534 (75y, rung 1 comparison layout). Waiting: vm-o7n (after x2n), driver buq (after 7qi), sched-r28/estimate
bph.6/.7 (ISA spec text, after x2n). The background full tier (tools/regate.py) re-gates every moved main.

- **Plugin (rung 3 and rung 4 bottleneck):** `job/j3l` (full-SQLite PT6 round-0 blow-up; several measured causes fixed, the
  four full cells not yet accepted; memory peaked ~48 GB per cell) -> review -> land; then `bennett-plugin-ot5` (split
  `Analysis.cpp` so writers stop serialising), `bennett-plugin-eph` (arith pin), `bp-owg`, later `bp-1bb` slices. In parallel on
  disjoint files: `job/75y` (comparison layout, review round 2) -> `bennett-plugin-7qi` (G1 association) -> s59 -> `bp-xb8`/`bp-zeg`.
- **ISA spec:** local main (356 0.9 C headers + 0cb mixed-launch text, both council-accepted, merged locally) does NOT pass its
  gate and is unpushed: `bennett-isa-spec-x2n` (P1). The stale `spec/isa-0.8-to-0.9.diff` is regenerated on `job/isa-x2n`; the 0.9
  launch header still lacks 0cb's mixed-launch declarations (spec inventory 59 vs header 55). origin/main moved on separately
  (re-pin, docs, beads): local main must merge origin/main. `job/isa-k86` (K86-K92 reference checks) awaits its scoped round.
  Then `bennett-sched-r28` (P0, K25) and `bennett-estimate-bph.6/.7`. Reference interpreter speed: `bennett-isa-spec-nwu`.
- **Conformance:** `job/conf-51d` (51d + 3jt checker fixes; council), then `bennett-conformance-fki`, `-ugg`; rung 3 re-runs after
  each plugin/driver landing.
- **Circuits:** export-qasm redesign (doc landed, `bennett-circuits-8xv`); stage 1 on `job/exporter-s1` blocked by the legacy
  oracle panic `bennett-circuits-fc8` (repair job paused).
- **Driver:** `job/buq` holds a loud-failure test only; resumes after plugin 7qi.
- **VM:** dense engine (`bennett-vm-bjm`) lives only on old `wip/*bjm-dense` branches; decide land-or-park before `d2j`/`5vj`;
  `bennett-vm-o7n` now unblocked by the 0.9 headers once pushed.
- **Arith:** `bennett-arith-gdg` (release check on shipped bytes) on `job/gdg`.
- **Meta tools:** main-health is not re-armed as a daemon until each repo has cited hang-guard class tables
  (`bennett-0v2`); meanwhile run `tools/gate_launch.py start --repo R --tier full` on pushed mains and seed
  `health/known-reds.toml` from the reds. `job/9iy` is superseded by job/health (not to be merged).

## Where things are

Rules: [docs/process/COMMON.md](docs/process/COMMON.md). Work items: `bd` in each repo's main checkout. A job's resume point:
its `.tmp/<job>/PROGRESS.md` and git history. Gates: `tools/gate_launch.py start|wait|status` (events in `.tmp/gates/events/`).
Launch admission: `tools/admit.py`, against the maintainer's `dial.toml`. main-health: `tools/main_health.py`. Shift files and
worklogs are historical.
Reds: every push prints its repo's open NEW-REDs (from `.tmp/gates/reds.log`); `tools/gate_launch.py reds` lists all; known
standing reds live in `health/known-reds.toml` (one bead each); revert with `tools/revert_landing.py`.
Branches: on 2026-11-11 every superseded branch was deleted (tips under `refs/archive/branches/` in each repo). The in-flight
ones are listed per lane below: j3l, 75y, plugin-arith-pin, combo-s3, isa-k86, isa 356/0cb/x2n, conf-51d, exporter-s1, buq,
sched-vt8, vm-o7n, and vm's dense engine on `wip/session-end-2026-11-03-bjm-dense`.
