# bennett (meta repo)

The Bennett ecosystem compiles unmodified programs (C, Rust, Julia, any LLVM language) into reversible and quantum programs.
An LLVM pass plugin infers which code must be reversible and emits marker-based IR; a link-time driver produces fat objects.
A public virtual ISA (with a formal model and conformance suite) sits beneath, targeted by a VM, a scheduler and circuit exporters.
Everything is split into small independent repositories that talk only through two published contracts: the dialect spec and the ISA spec.
This repo is a thin index: the manifest, clone scripts and cross-repo docs. It holds no shared code.

## Repositories

| Repository | Role |
|---|---|
| `bennett-dialect-spec` | LLVM dialect contract: marker ABI, handles, normalisation, residual-poison validator, legality corpus |
| `bennett-isa-spec` | Virtual ISA: formal model, object/launch/sched/cert formats, conformance suite |
| `bennett-sched` | Scheduler and cost model behind the ISA scheduling interface |
| `bennett-plugin` | C++ LLVM pass plugin; built per LLVM major |
| `bennett-driver` | Link-time driver: bitcode merge, plugin invocation, fat objects, launch, coverage reports |
| `bennett-vm` | Rust device runtime: classical-control tier, history layers, effect tape, device models, simulation, JIT |
| `bennett-circuits` | Bounded specialiser: hierarchical circuit IR, placement, proof-carrying output, exporters (OpenQASM 3, QIR, Quil) |
| `bennett-estimate` | Resource estimation from ISA objects, certificates and target descriptions; no gates materialised |
| `bennett-targets` | Target descriptions per hardware model, contributed by vendors; importers for existing resource-model formats |
| `bennett-runtimes` | Allocator, libc/musl shims, device models, Julia shim runtime, language-runtime bitcode builds, compiled to ISA objects |
| `bennett-arith` | Adders, multipliers, QROM, soft-float as ISA library objects with certificates |
| `Bennett.jl` | Julia quantum language: when, oracles, in-place regions, certificate kinds, simulators as VM targets, REPL, @cost |
| `bennett-conformance` | Demo ladder gates, certificate checker, legality corpus runner, differential harness; consumer of everything |

Machine-readable form: `manifest.toml`. Clone everything: `BENNETT_REMOTE_BASE=<url-base> scripts/clone-all.sh`.

## Build / staffing order

specs -> sched / vm / circuits / estimate / targets -> plugin -> driver -> runtimes / arith -> Bennett.jl -> conformance

Source of truth: Bennett-NorthStar.md section 6.1 (currently in the Bennett.jl repo).

## Documents and process

- `docs/Bennett-NorthStar.md` — the vision (iteration 7, council consensus 2026-10-28). Change only with a reason that would survive the council.
- The ISA specification lives in `bennett-isa-spec/spec/Bennett-ISA-Spec.md` (draft 0.8, accepted by the council 2026-10-28, round 8).
- `tools/council.py` + `docs/council/` — the three-model review council (codex / muse / opus), its rubrics (`rubric.md` for visions, `rubric-isa.md` for specs), process (`docs/council/README.md`) and every graded round of both documents. Any revision of a published contract goes back through it.
