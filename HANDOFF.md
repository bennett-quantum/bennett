# HANDOFF — Bennett ecosystem

Current-state checkpoint: 2026-11-11 (workflow reform; product lanes as of 2026-11-09). Beads triaged 2026-11-11: deferred
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
| 3 | musl hello-world | Acceptance outstanding (`bennett-conformance-7bx`). Latest run (conformance `84f8ecb`, pushed mains, arith `5e9b450` = the plugin's pinned arith): 21 PASS / 3 FAIL / 20 BLOCKED per LLVM major. Driver now accepts 0.3-r1/ISA 0.9; remaining stops are plugin `bennett-plugin-7qi` (G1-to-native-symbol association), `bennett-driver-s59` (R argv/envp storage, a plugin gap) and `bp-owg` (printf analysis budget). |
| 4 | Grover over unmodified SQLite | Acceptance outstanding (`bennett-conformance-tmb`). The November 8 main-snapshot run failed on arithmetic publication/pin compatibility; estimator schema and checker CLI diagnostics also failed. |
| 5 | Julia shim runtime | Acceptance requirement only; rung directory contains a README, no executable gate/results. |
| 6 | xv6, then Linux | Acceptance requirement only; rung directory contains a README, no executable gate/results. |
| 7 | Quantum kernel fuzzing | Acceptance requirement only; rung directory contains a README, no executable gate/results. |
| 8 | C Monte Carlo amplitude estimation | Acceptance requirement only; rung directory contains a README, no executable gate/results. |

Rung 4 still requires all three North Star clauses: exhaustive oracle checks through N ≤ 2^10,
Grover simulation through N ≤ 2^8, and a budgeted, padded estimate at N = 2^20. Reduced controls,
measured-basis diagnostics and a small fixture estimate cannot satisfy those clauses.

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
