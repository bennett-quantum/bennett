# HANDOFF — Bennett ecosystem

Current-state checkpoint: 2026-11-09 end of day, process sections updated 2026-11-11 (rulebook rewrite). Recheck live Beads.

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

- **Plugin (rung 3 and rung 4 bottleneck):** `job/j3l` (full-SQLite PT6 round-0 blow-up; several measured causes fixed, the
  four full cells not yet accepted; memory peaked ~48 GB per cell) -> review -> land; then `bennett-plugin-ot5` (split
  `Analysis.cpp` so writers stop serialising), `bennett-plugin-eph` (arith pin), `bp-owg`, later `bp-1bb` slices. In parallel on
  disjoint files: `job/75y` (comparison layout, review round 2) -> `bennett-plugin-7qi` (G1 association) -> s59 -> `bp-xb8`/`bp-zeg`.
- **ISA spec:** local main carries the 0.9 C headers (356, council-accepted) awaiting a re-run gate; `job/isa-0cb` (mixed-launch
  transport; council + one scoped round) and `job/isa-k86` (K86-K92 reference checks; council) await disposition. Then the
  text batch `bennett-sched-r28` (P0, K25 classical pseudo-locations) and `bennett-estimate-bph.6/.7`.
- **Conformance:** `job/conf-51d` (51d + 3jt checker fixes; council), then `bennett-conformance-fki`, `-ugg`; rung 3 re-runs after
  each plugin/driver landing.
- **Circuits:** export-qasm redesign (doc landed, `bennett-circuits-8xv`); stage 1 on `job/exporter-s1` blocked by the legacy
  oracle panic `bennett-circuits-fc8` (repair job paused).
- **Driver:** `job/buq` holds a loud-failure test only; resumes after plugin 7qi.
- **VM:** dense engine (`bennett-vm-bjm`) lives only on old `wip/*bjm-dense` branches; decide land-or-park before `d2j`/`5vj`;
  `bennett-vm-o7n` now unblocked by the 0.9 headers once pushed.
- **Arith:** `bennett-arith-gdg` (release check on shipped bytes) on `job/gdg`.
- **Meta tools:** `job/9iy` (main-health concurrency + one shared same-repo gate lock), then `bennett-0v2` (class tables for 11
  repos) before re-arming main-health on the new code; `bennett-pow` (per-worktree gate cache). Disk filled to 100% once on
  2026-11-09: prune rebuildable `.tmp/*target*` caches of landed job worktrees.

## Orchestration and records

Rules: [docs/process/COMMON.md](docs/process/COMMON.md), the one rulebook (children: rule 15 and T3CHILD.md). The orchestrator seat
runs product work; there is no standing advisor seat in the product workflow. Launch admission is `tools/admit.py launch` against the
maintainer's `dial.toml`; gates run through `tools/gate_launch.py`. Live work state is beads (`bd` in each repo's main checkout) plus
this file; a job's resume point is its `.tmp/<job>/PROGRESS.md` and git history. Shift files and worklogs are historical.

Landing: fast tier (`scripts/pre-push`, gate_run pre-merge) green on the merged tree, one `--no-ff` merge, push. main-health
re-gates pushed mains with `--tier full --fresh` and attributes new reds against `health/known-reds.toml`; revert with
`tools/revert_landing.py`. PASS receipts are keyed on product content (each gate.toml's `[receipt] non_product`), so beads exports and
worklog edits do not re-gate. All bennett-quantum repos are public: no transcripts, logs or .tmp records in commits or branches.
