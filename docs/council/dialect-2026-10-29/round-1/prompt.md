# Council

You are a member of a three-model council grading the document below, the Bennett LLVM dialect specification draft 0.2 (the bennett-dialect-spec contract of the north star, section 3 and 6.1), rewritten from the ratified outline after draft 0.1 was rejected for narrowing north-star scope; graded against ISA 0.8 with blocked verdicts for the four named ISA gaps. Grade it against the rubric on the absolute scale. Be exacting and skeptical: verify every technical premise against your own knowledge and against the ISA specification and north star attached as background; name any that is false. A blocking issue is one that would make the project build the wrong thing if uncorrected; everything else is a suggestion. Return `accept` only if the blocking list is empty.

Be constructive, always: the editor must be able to act on your output without asking you anything. For every blocking issue the `fix` field must give the section, the sentence or rule the document should state (write it), and, where an example is involved, the corrected example or expected value; `problem` carries the witness (the quoted text and why it is wrong, or the two readings that diverge). Where two viable ways out exist, name both and say which you would take. Every `suggestions` entry and every criterion's `change` field follows the same rule. In `path_to_accept`, state the minimal ordered set of changes that would make you return `accept`; if you already accept, say what would raise the lowest-scoring criterion by one point.

You may read the repository you are running in (read-only): it is `bennett-dialect-spec`, whose `spec/Bennett-Dialect-Spec.md` is the document (identical to the snapshot below), `spec/bennett_markers.h` its C header, `spec/outline-0.2.md` the ratified outline it was written from (with the maintainer's rulings at its end), `spec/Bennett-Dialect-Spec-0.2.PROGRESS.md` the editor's record of what was verified and what could not yet be (read it: the families it lists as unverifiable are graded on the text, not on executed results), `docs/spikes/` the legality and SQLite spike evidence, `docs/audit/` the narrowing audit of the rejected draft 0.1, and `corpus/` the legality corpus. The ISA specification is at `../bennett-isa-spec/spec/Bennett-ISA-Spec.md` and the north star at `../bennett/docs/Bennett-NorthStar.md`; both are also attached below. Reading is optional; the snapshot below is what you grade.

Answer only with JSON matching the schema.

Convergence rules for this council (read before grading):
1. Blocking means S0 only: two conformant implementations built from the text would compute different results, the semantics is unsound or self-contradictory, a normative decision is missing where one is needed to build, or the document narrows north-star scope (rejects, refuses, faults, declares inert or omits a capability the north star promises, including any rung of its demo ladder, even when disclosed, labelled deferred or given a default; a default only closes an S1 item if it keeps the capability). Tag every blocking issue with `scope` (`core` = machine model, instruction set, regions, validity, memory, formal model, examples; `contract` = targets, objects/identity, launch, scheduling, certificate, coverage, grammar) and `severity` (`S0` as defined; `S1` = an implementer would have to choose, but any choice yields a conformant machine). S1 items belong in `suggestions`, not `blocking`, unless the document fails to state a default for them.
2. Implementation will expose frictions; that is expected and acceptable. Do not block on field-level completeness of C headers, JSON schemas, numerical procedures or encodings when the normative obligation is stated and a default is given; list such gaps as suggestions. Do block on anything that would make an executor compute a different function.
3. Fill `previous_status` for every blocking issue of the previous round (by id) with resolved | partially | unresolved | regressed and a one-line note. List in `regressions` anything that was correct in the previous snapshot and is wrong now.
4. Give `verdict_core` (accept/revise/reject) for the core scope alone, and `verdict` for the whole document. Core consensus is reached when every member returns verdict_core = accept with no core-scoped blocking issue.
5. A diff from the previous snapshot is attached when one exists: confirm fixes there first, then re-read the whole document for new S0 issues.
6. Formal correctness is pursued after practical revisions, by the maintainer's decision: in this phase the specification needs correct *statements* with explicit hypotheses, not proofs. Demands for proof formats, mechanisation, rigorous numerical or SDP witness schemas, or checker algorithms are S1 (suggestions) as long as the obligation and a default procedure are stated. Block only on a statement that is false, unsound or ambiguous.


# Rubric

# ISA-specification rubric — the council's scale

The rubric the council (`docs/council/README.md`) uses to grade
`Bennett-ISA-Spec.md`, the founding draft of the Bennett virtual ISA
specification (the `bennett-isa-spec` contract of `Bennett-NorthStar.md`
§4.4 and §6.1). Eight criteria, each scored 1–5 on an absolute scale, plus
blocking issues, a path to accept, and verdicts. Scores are advisory; the
maintainer decides.

## What is being graded, and the goal

A **specification**, at the level of a first normative draft: the
document a VM author, a circuit-specialiser author, a plugin author, a
scheduler author and a hardware vendor would each implement against,
independently, and be conformance-tested on. The maintainer's stated
goal is **an accepted spec that is likely correct**; implementation is
expected to expose frictions afterwards, and that is acceptable. So the
question is not "is every detail enumerated" but "would two independent
implementers build the same machine, and is that machine sound".

## Blocking, S0 and S1, scope

A **blocking** issue is **S0**: uncorrected, two conformant
implementations built from the text would compute different results;
or the semantics is unsound (irreversible where reversibility is
claimed, unphysical, phase-unsafe, dependent on inspecting superposed
data); or the text contradicts itself; or a normative decision is
missing where one is needed to build at all; **or the document narrows
north-star scope**: it rejects, refuses, faults, declares inert or
omits a capability that `Bennett-NorthStar.md` promises (its thesis,
§3–§5 and every rung of the §8 demo ladder), whatever reason it gives.
A narrowing is blocking even when it is disclosed, labelled deferred,
or given a default; the fix is the mechanism, or, where a contract the
document depends on truly lacks something, an explicit blocker naming
the exact change that contract needs.

**S1** issues are ones where an implementer would have to choose, but
any choice yields a conformant machine, or where the normative
obligation is stated and only its enumeration is incomplete (field-
level completeness of C headers, JSON schemas, numerical procedures,
encodings). S1 items are **suggestions**, not blockers, **unless the
document fails to state a default for them**; the document carries a
section of decisions deferred to implementation, each with a default,
and an S1 item with a stated default is closed **only if the default
keeps the capability**. A deferral may postpone mechanics (an encoding,
a table layout, an optimisation); a default of "reject", "refuse",
"none", "fault" or "no effect" for something the north star promises
is a narrowing, hence S0, not a closed S1.

Every blocking issue is tagged with a **scope**: `core` (machine model,
instruction set, regions, uncomputation validity, memory and effects,
formal model, the example objects) or `contract` (targets, objects and
identity, launch, scheduling, certificate, coverage, grammar).
**Acceptance is staged**: core consensus (every member's `verdict_core`
= accept with no core blocking issue) is the first milestone; the
contracts follow. Members give both verdicts.

## The standard

The PTX ISA document, the JVM specification, the RISC-V unprivileged spec,
the LLVM language reference: a stranger implements from the text alone,
and two strangers get the same machine. Precision within full scope:
the scope is fixed by the north star and is not the document's to
trade; within it, a mechanism defined exactly scores above one defined
loosely, and a document never buys precision by cutting scope (that is
a narrowing, S0 above). Skepticism is required: check the quantum semantics
and the reversible-ABI claims against your own knowledge; when the
document ships example objects with hashes and stated results, they are
normative test vectors and have been executed before this round.

### Scale

- **5:** implementable by strangers with no questions; sound; complete for
  its declared scope; nothing superfluous.
- **4:** implementable with one gap an implementer names at once.
- **3:** a competent draft; the shape is right but several rules need an
  author's clarification before implementation.
- **2:** aspirational; semantics sketched, not pinned.
- **1:** inconsistent or unphysical at the core.

## Criteria

### C1 Machine model
Tiers, state, types, the step relation: unambiguous? Could two
implementers draw the same state diagram?

### C2 Instruction set
Every instruction with form, operands, well-formedness, semantics, cost
hook; closed and sufficient for what the dialect must lower; nothing
underdetermined.

### C3 Coherent semantics
The predicated step machine, the oracle interface F_B, the action
interface, nesting, exit synchronisation, the prefix-reversal invariant,
the fault register, the budget unit, in-place bijections, the
uncomputation-validity invariant, borrow frames: checkable rules, nothing
irreversible, phase-unsafe or dependent on inspecting superposed data.

### C4 Resources and targets
Resource vector, qubit classes, the target-description format, matching
and cost rules: complete enough that a vendor could write one and the
scheduler consume it, with defaults where the spec defers.

### C5 Contracts
Object format, identity, linking, reversible ABI, launch ABI, scheduling
interface, certificate schema, coverage: each **decided** to the level the
north star promises, so the repositories can be developed independently;
S1 enumeration gaps with stated defaults do not lower this score below 4.

### C6 Formal model and conformance
Abstract semantics an implementer can check against; theorems stated
with explicit hypotheses; a conformance suite derivable from the text.
**Formal correctness is pursued after practical revisions** (maintainer
decision, 2026-10-28): proof formats, mechanisation, rigorous numerical
or SDP witness schemas and checker algorithms are S1 in this phase. A
false or unsound statement is S0; a missing proof is not.

### C7 Consistency with the north star and prior art
No contradiction with `Bennett-NorthStar.md`; established forms used
where they exist.

### C8 Implementability and clarity
Could a VM author and a specialiser author each start tomorrow? Are the
deferred items genuinely non-semantic, each with a default?

## What the council returns

Per criterion: a score 1–5, evidence pointing at the text, the single
change that would most raise it. Then `blocking` (id, section, scope,
severity S0, problem, and the concrete rule the spec should state),
`previous_status` (every previous-round blocker: resolved / partially /
unresolved / regressed, with a note), `regressions`, `suggestions`
(S1 and nits), `path_to_accept`, `verdict_core`, `verdict`, `summary`.
Consensus is reached when every member returns `accept` with an empty
blocking list; core consensus when every member returns `verdict_core`
= accept with no core-scoped blocker.


# Background (not graded): `Bennett-NorthStar.md`

# Bennett — North Star (reboot vision, iteration 7 — council consensus)

**Date:** 2026-10-28. **Status:** vision settled at the level of "what it
truly looks like"; technical design NOT started. Iteration 6 after council
rounds 1–5 (`docs/council/northstar-2026-10-28/round-*/report.md`; the
editor's responses are in `round-*/response.md`). Round 5: one accept, two
revise at mean 4.42/5, every earlier blocker confirmed resolved, one new
one (residual LLVM nondeterminism after poison/undef removal: NaN bits,
`fmuladd`, addresses), folded in here as a complete determinism contract.
Round 6: **all three members accept, no blocking issues, mean 4.46**; the
council loop on this document is closed, and this iteration applies only
wording fixes from that round. Nothing here is
implemented, and no code is to be written on the strength of this
document alone (maintainer process rule: vision, then design, then
spikes, then code).

**Provenance.** Written up from maintainer/agent design discussions on
2026-10-28. The maintainer's position on the quantum VM (§4) was formed
over a year of discussion across the quantum-information community; the
document states that position and the reasons, and asks to be judged on
the reasons.

**Relation to earlier documents.** Supersedes `Bennett-Reboot-Blueprint.md`
§3.1–§3.4 (its standalone "BIR" is dropped: the IR is LLVM IR with a
dialect inside it). The blueprint's §5 keep/kill list, §6 ladder and §7
risks carry over where they do not conflict. `Bennett-V2-PRD.md` remains
parked. `Bennett-VISION-PRD.md`'s Enzyme analogy turns out to be literal.

**Ground truth this was checked against** (2026-10-28 read-only survey of
both repos, the Astra reviews, BENCHMARKS.md, and the checkout of the now-
sunset Sturm.jl at `~/old/Projects/Sturm.jl`): worklog chunk 121, session
2026-10-28. The
current Bennett.jl / BennettVM.jl are deprecated as designs; their research
assets (arithmetic generators, soft-float with its test conventions, gate
algebra, scaling-relation regressions, the 6502 native-oracle harness) are
the only things carried forward.

---

## 0. Thesis

**Every program is already a quantum program.** The user never writes a
circuit, never declares a subset, never learns a new language. They write
C, Rust, Julia, anything LLVM eats, and the toolchain decides at every
instruction whether it runs classically, reversibly, or coherently. The
only thing a quantum programmer adds to a classical codebase is a handful
of marker calls: allocate qubits, rotate by theta, measure, and a way to
condition a region on a qubit. Everything else is inferred.

Tagline: **controlled-anything.** If it compiles with clang, you can put it
under a qubit. "Unmodified" means **no source edits**; build-configuration
flags and runtime shims are allowed and are recorded in the certificate.

Stated precisely, because precision is what makes the slogan true rather
than a slogan: *every execution of any LLVM program that is defined under
the reference semantics of §3.2, effect-bounded, and within a classical
resource budget can be run coherently under a qubit; executions that the
reference machine can see are outside that domain produce a named fault
outcome that is part of the result (§4.2), never a silent wrong answer
and never a crash of the region.* Source-level undefined behaviour that
the optimiser has already erased is not detectable by anyone after the
fact; it is covered by an explicit definedness assumption recorded in the
certificate, not by a fault guarantee (§3.2).

**The project is predicated on the hardware getting good enough:**
scalable logical quantum computation with plentiful logical qubits and
**logical gate times on the order of nanoseconds**. Every cost in this
document is counted in that regime; a kernel boot of billions of steps is
a design target only because of it. Efficiency is pursued hard;
universality is never traded for it.

## 1. Decisions (settled 2026-10-28, refined after council rounds 1–2)

1. **Bennett is the LLVM of quantum.** Language designers introduce quantum
   constructs *as they please*, the way LLVM lets anyone design a classical
   language. We provide the target and the optimiser, never the language.
2. **The IR is LLVM IR. We never fork LLVM.** Forking is the disaster
   scenario. Decades of classical optimisation are kept by sitting inside
   the ecosystem through mechanisms an out-of-tree plugin can actually rely
   on (§3). Where an upstream change would help, it is proposed upstream
   as a patch, never carried as a fork.
3. **Delivery is a pass plugin, a driver, and a runtime.** The plugin runs
   at **link time over whole-program bitcode** (§3.3): optimise, reverse,
   optimise. Any front end that can emit bitcode is supported; per-front-
   end integration is a driver concern, named per front end with its
   costs, never a language change.
4. **Three execution tiers, one program.** Classical (host, native code,
   never ours), reversible (device, deterministic forwards and backwards,
   effects on a tape), coherent (device, closed and effect-free, every
   control decision predicated, every region total with a fault output,
   §4.2). The quantum VM is the device, in the sense a GPU is a device.
5. **One virtual ISA, one target description per hardware.** The PTX move.
   The ISA is a versioned public specification with a conformance suite;
   the formal model is of the spec, not of any implementation.
6. **The VM is a scheduler over an extensible resource vector**, and its
   run-time policy depends only on classical data. Compile-time and run-
   time scheduling are the same optimiser, implemented once
   (`bennett-sched`) behind an interface the ISA spec owns (§4.4).
7. **Correctness is defined by a theorem, two oracles, and a fault
   outcome, never by a reversibility check** (§5.1). Certificates say
   which parts are proof and which are evidence.
8. **QIR, OpenQASM 3, Quil, and MLIR quantum dialects are edge formats**,
   read and written at the boundary. Never the semantics (§7).
9. **Languages: the right tool for the job, taste excluded** (§6).
10. **Many small repositories, published contracts, no monolith** (§6.1).

## 2. The architecture, in one picture

```
  Front ends     clang (C/C++)   rustc   Julia (Bennett.jl)   QIR / Quil / MLIR-dialect importers
                     └──────────────┴────────┴───────────────────────┘
                         emit LLVM bitcode + __bennett_* marker calls (the dialect, §3)
                                              │
  Link time      bennett-driver: whole-program bitcode (LTO) ─► LLVM's own optimiser (unmodified)
                                              │
                 bennett-plugin (C++, the only LLVM-linked component):
                   taint over the resolved call graph → region outlining → controlled/adjoint
                   body generation → lowering to the virtual ISA → bennett-sched (cost, schedule)
                                              │
  Objects        fat object: native host code + ISA object(s) + certificate (ISA spec, §4.4)
                                              │
  Executors       ┌───────────────────────────┴───────────────────────────┐
                  ▼                                                       ▼
        bennett-vm (device runtime)                         bennett-circuits (bounded specialiser)
        reversible + coherent tiers, history layers,        hierarchical circuit IR, placement,
        effect tape, branch-enumeration simulation,         proof-carrying output, exporters
        launch-time lowering to the target alphabet
                  └───────────────────────────┬───────────────────────────┘
                                              ▼
  Backends     Bennett.jl simulators   OpenQASM 3   QIR   Quil   bennett-estimate   hardware via bennett-targets
```

One semantics: the ISA spec's formal model and conformance suite. Two
executors, in separate repositories, each conformant to that spec, and
permanently differentially tested against each other and against native
execution of the same bitcode.

## 3. The dialect: what an out-of-tree plugin can rely on

This section lists only mechanisms that exist for a plugin today, states
what each does and does not guarantee, and names the legality spike that
gates freezing the spec.

### 3.1 Mechanisms

| Need | Mechanism (out-of-tree, stock LLVM) | What it does NOT give, and what covers the gap |
|---|---|---|
| Quantum operations: allocate (clean / dirty / class), release, gate, rotate(θ), measure, quantum-addressed load and store | **Declared external marker functions** `__bennett_*` with fixed signatures, exactly as Enzyme's `__enzyme_autodiff`. Not `llvm.*` intrinsics (a plugin cannot register them). The plugin recognises them by name and signature at link time. **Positive legality requirement:** a marker is declared as an external function that may read and write memory and may not return (no `readnone`, `readonly`, `speculatable`, `willreturn`, `nounwind`-only combinations that would license elimination, commoning or speculation). Stock passes then preserve the *dynamic sequence* of marker calls on every executed path. | Containing functions may be inlined, cloned, unrolled or versioned, so the *static* count of marker call sites is not preserved; the external declaration itself is never inlined. *Explicit quantum registers* are accessed only through markers, never through LLVM `load`/`store`, so no alias-analysis or forwarding pass can touch them. The ordinary loads and stores of lifted classical code (all of SQLite's) are not quantum-register accesses: they are lifted coherently according to the incoming memory model, as classical memory whose contents happen to be superposed. This legality is a property of ordinary effectful external calls, not of any attribute we invent; the legality corpus (§3.2) tests it. |
| Qubit handles | **Portable handles**: an ordinary `ptr` in address space 0 (or an integer handle) returned by `__bennett_qalloc`, which every front end can emit from unmodified source: clang, rustc, Julia. Never dereferenced by host code. The plugin normalises recognised handles into its internal representation after outlining, respecting the incoming target's pointer size. **Reference semantics at the dialect level.** | LLVM cannot enforce linearity; SSA uses are free to duplicate. Linearity is a fail-loud verifier obligation after outlining, plus the ISA's value semantics below. Collections of handles are supported through a **handle table**: an aggregate or array of handles indexed by a classical value (a compile-time constant or a classical-tier value) is lowered to table lookups; a handle that flows through memory at a superposed address, or through an `inttoptr`/`ptrtoint` round trip, is **rejected fail-loud** in v1 of the dialect; any handle use that survives into host native code is rejected likewise. Any code that touches handles or measurement results runs in the device's classical-control tier, never as host native code. This is the point on which QIR is faulted in §7, and the answer is to be explicit about it. |
| Qubit values in the ISA | **Linear value semantics in the virtual ISA** (wire form, as in Quake's wire dialect and QSSA): each use consumes, each definition produces. The plugin converts handles to wires after outlining and verifies the conversion. | Both forms exist, at named pipeline stages, for the same reason CUDA-Q keeps both. |
| Coherent memory and in-place update | **Copy-on-read, XOR-on-write, total-bijection-for-in-place** (§4.2): `__bennett_qload` is a CNOT copy of the register onto fresh wires (source preserved, copy is retained workspace until uncomputed under the validity invariant); `__bennett_qstore` XORs into its target, so a store into a known-clean register is a copy and a store into a register not known to be clean is a **compile-time error** (this source-level restriction is distinct from the oracle ABI, whose targets may hold any value); an in-place update x ← g(x) is written `__bennett_inplace(@g, @ginv, …)` and is admitted **only when g and ginv are mutually inverse total bijections on a declared finite encoding**, with budgets sufficient for forward evaluation and inverse cleanup, and is lowered compute-out-of-place, swap, uncompute-with-g⁻¹; library bijections (add a constant, xor, rotate, modular add, modular multiply with its coprimality condition and its treatment of unused encodings stated) carry their inverses and their g∘ginv = id certificates in `bennett-arith`. | A fallible or budget-limited computation cannot be in-place: it uses the out-of-place oracle interface (§4.2). A declared inverse is a correctness obligation: g∘ginv = id is checked by §5.1 part 1 at exhaustive small widths or carried as a library certificate, and a wrong inverse is caught because swap-then-uncompute leaves the scratch register non-clean. An in-place update with no inverse fails loud at compile time. Front ends may instead compose two compute regions and a swap themselves. This is what makes `when(q) do x += a end`, the founding use case of the Julia language (§6), work as written. |
| Taint: classical vs reversible vs coherent | **Analysis, not types**: a context-sensitive interprocedural analysis over data dependence, control dependence and memory effects, from marker results and region entries, over the whole-program call graph, with polyvariant specialisation when one function is used both classically and coherently. | No per-value attribute survives optimisation and none is needed. "Untainted" is defined relative to the resolved call graph, never per translation unit. |
| Control as structure: adjoint, controlled-by-qubit, compute-with-uncompute, reversible-tier entry | **Function granularity**: a region is outlined to a function (LLVM's `CodeExtractor`) and entered through a marker call `__bennett_ctrl(q, @f, budget, args…)`, `__bennett_adj(@f, …)`, `__bennett_compute(@f, …)`, or `__bennett_reversible(@f, budget, …)` for the reversible tier. The plugin generates controlled and adjoint bodies on demand from one source body. **Well-formedness:** a `ctrl`/`adj`/`compute` region is unitary: user measurement inside it is refused (or, when the front end asks for it, deferred by the deferred-measurement principle, which the certificate states); allocations inside are released clean or borrowed and restored; the compiler's own measurement-based uncomputation is the sole exception, and until its controlled form is fixed in the language's certificate kinds (§9.6) **unitary uncomputation is the fallback under control**. Exceptions and unwinding (`invoke`/`landingpad`, Rust panics, C++ `throw`) inside a region are step-machine control flow where the handler is in the region, and a fault code where it is not. | Front ends that want `when`-style syntax do the outlining themselves (Julia macro, clang attribute, Rust proc-macro) and emit the marker call; the dialect does not require it. Generating a body needs the callee's IR, which is why the plugin runs at link time (§3.3). |
| Bounds for coherent regions | **A region-level classical budget**: dynamic steps, heap bytes and recursion depth, passed as ordinary integer operands of the region-entry marker or supplied out of band by the host or driver (a project-wide default, a per-function table), and applied by the plugin after outlining. **No per-loop source annotation is ever required**, so unmodified SQLite, Linux and the Monte Carlo compile as they are. Per-loop bounds from scalar evolution, and optional per-loop markers, are *refinements* that let the specialiser tighten padding; they are not needed for correctness and no loop identity has to survive O3. | A region whose budget is exhausted on some basis input produces a fault outcome on that input (§4.2); it is never a compile error and never a truncated result. |
| Garbage and uncomputation | **Liveness analysis** on the outlined region plus the compute/uncompute marker; no lifetime intrinsics. | The scheduler decides when to pay to free a dead value; the dialect only has to make deadness computable. |
| Measurement and classical feedback | Marker call returning `i1`, flowing into ordinary `br` / `select` / `phi`, outside unitary regions. | Branching on a measurement result is classical control (§4.2). |
| Effects | Marker calls on the device side for the effects the device models (console, clock, entropy, block device); everything else is a host call. | Effect semantics per tier are in §4.2; an unvirtualisable effect inside a coherent region is a fault code on the executions that reach it, and a coverage-report line at compile time. |

### 3.2 Pipeline placement and the cost of staying in-tree

- **Correctness is invariant under LLVM's optimiser; cost is not.** Any
  semantics-preserving optimisation of the classical part is lowered as it
  stands, so differential testing (§5.1) is against the native binary
  built from the *same* optimised bitcode. Optimisations that erase or
  duplicate intermediate values change gate counts, so tainted regions get
  a curated region pipeline after outlining.
- **Definedness.** Source-level undefined behaviour cannot be "concretised"
  after an optimiser has exploited it (`clang -O3` turns `int y = 10/x;
  return 0;` into `return 0`, and nothing remains to fault on), so the
  document does not claim that. The contract, stated once and referenced
  by §0, §4.2, §5.1 and §8: **the reference semantics is the ISA formal-
  model interpreter run on the *materialised* optimised bitcode of the
  outlined region**, mapped by the dialect's reference semantics, before
  the curated region pipeline. **Materialised normalisation**, not
  `freeze`: LLVM's `freeze` yields an arbitrary fixed value that codegen
  lowers to whatever the register holds, so it cannot define one meaning
  shared by native code and the device. Instead the normaliser rewrites
  the region's optimised bitcode into a **poison-free, undef-free form**:
  poison-generating flags (`nsw`, `nuw`, `exact`, `inbounds` and kin) are
  stripped; partial operations are totalised with a stated result (a
  shift by ≥ width yields 0 through a `select`; division by zero and
  `sdiv`/`srem` of INT_MIN by −1 become faults, below); memory first
  touched inside the region (alloca and heap contents, and the padding
  of region-local objects) is zero-filled; any remaining `undef` operand
  is replaced by a stated constant; `llvm.objectsize`, `llvm.is.constant`
  and similar query intrinsics are lowered before both builds. Region
  inputs are **not** zero-initialised: they are the bytes the host
  supplies.

  Poison and undef are not the only choices LLVM leaves open, and the
  reference semantics **fixes every remaining one** so that the native
  comparison binary and the device implement the same function:

  - **Floating point is deterministic soft-float in both builds.** The
    normaliser rewrites every floating-point operation of lifted code
    into calls to the project's bit-exact soft-float library
    (`bennett-arith`, IEEE 754 binary64, round-to-nearest-even, a single
    canonical NaN with fixed sign and payload produced by *arithmetic*
    operations only, while `fneg`, `fabs`, `copysign`, loads, stores,
    `bitcast`, `select` and `phi` stay bit-exact as LangRef requires; no
    fused multiply-add unless the source wrote `fma` explicitly;
    `llvm.fmuladd` is rewritten to `fmul` + `fadd`; out-of-range
    `fptosi`/`fptoui` and the `minnum`/`maxnum` NaN cases have stated
    results); fast-math flags are stripped. Formats: binary64 and
    binary32 are covered; `half`, `bfloat`, `x86_fp80` and `fp128` are
    coverage-report lines until the library covers them, never silent
    widening. Hardware floating point never executes in either build, so
    NaN bits, fusion and intermediate rounding are identical by
    construction, including through `bitcast` and branches. The native
    comparison binary is the materialised region plus its entire
    materialised callee closure, linked against the same
    `bennett-runtimes` and `bennett-arith`, never against the host libc
    or libm.
  - **Addresses follow a deterministic layout model.** The heap is laid
    out by the same `bennett-runtimes` allocator shim linked into both
    builds at a fixed base with no ASLR; globals and functions are placed
    by a driver-controlled comparison link (non-PIE, fixed section
    addresses, constant merging and identical-code folding disabled) whose
    link map the device loader replicates. Region allocas are rewritten
    by the normaliser onto a shim-managed shadow stack in both builds
    where possible, which shrinks the remaining class: executions in
    which absolute *native stack* address bits still influence the
    payload or the fault are classified by the reference interpreter's
    **address-provenance** tracking as *layout-dependent*, excluded from
    native comparison, counted like the undefined class, validated
    against the reference interpreter instead, and recorded in the
    certificate.
  - **Faulting memory access is defined** by an object-bounds model in the
    reference semantics: a lifted load or store outside any live
    allocation is `FAULT_UB_MEMFAULT`. The artefact may therefore fault
    where native silently reads adjacent memory; "equals native, or is
    flagged" permits this, and the fault rate reports it.
  - **Atomics and volatile** in lifted code are sequentialised in program
    order (the single-thread assumption recorded in the certificate);
    concurrency is §9.11.

  After this the materialised bitcode has **one defined meaning**, which
  native codegen and the ISA interpreter both implement, and the native
  comparison binary is built from that materialised bitcode. Only
  immediate undefined behaviour that the reference machine encounters
  (traps, `unreachable`, faulting memory access, division by zero) remains,
  and it is a fault code (§4.2); compiled artefacts must never fault where
  the reference does not; native execution supplies success values, and
  fault *causes* come from the reference interpreter, since a native trap
  cannot tell division by zero from `unreachable`. Source UB that
  optimisation erased before this point is **not detectable** and is
  covered by an explicit definedness assumption recorded in the
  certificate, together with the LLVM version, the pipeline and the
  normaliser version, since the fault set and the materialised program
  depend on them. The normalisation rules are normative text in
  `bennett-dialect-spec`, enumerating every source they remove (poison
  literals, `nsw`/`nuw`/`exact`/`inbounds`, fast-math `nnan`/`ninf`,
  `!range`/`!nonnull`/`!noundef` metadata and the matching attributes,
  `llvm.assume`, undef vector lanes) and shipping a residual-poison
  validator implemented independently by the plugin and by
  `bennett-conformance`. The conformance
  harness classifies inputs with instrumented builds (UBSan, ASan, MSan)
  or a checked reference interpreter, as a separate build from the
  comparison binary; these are **supplementary classifiers**, not a
  complete decision procedure for source definedness, and inputs they
  flag are reported as *undefined* and excluded from comparison.
- **Regions are functions.** Every `when`, adjoint, compute and
  reversible-tier block outlines first. Enzyme lives with this.
- **Per-LLVM-major builds** of the plugin, as Enzyme is built. A mixed-
  language link (bitcode from different LLVM majors, different front-end
  IR idioms, one target datalayout) is supported only within a **tested
  compatibility envelope** published with each driver release: bitcode-
  reader versions, target layouts and ABIs, front-end pairs.
- **The legality spike** (§9.1) is a conformance corpus, not a design
  question: marker-bearing bitcode through every stock pass at O3, plus
  native code generation of fat objects, must preserve the dynamic
  sequence of marker calls on every path and must leave no handle use in
  host code. Freezing `bennett-dialect-spec` is gated on it passing, and
  on actual emission examples from clang, rustc and Julia.

### 3.3 Compilation model: link time, whole program, fat objects

Taint and controlled bodies depend on the calling context across the whole
program, and generating a controlled body needs the callee's IR. So:

- Front ends emit **bitcode** (clang `-flto`, rustc `--emit=llvm-bc` or
  `-Clinker-plugin-lto`, Julia through LLVM.jl). This is the one universal
  thing every LLVM front end does. No front end loads our plugin; pre-link
  per-TU optimisation sees markers only as unknown external calls, which
  is exactly the legality contract.
- **`bennett-driver`** merges the bitcode, runs LLVM's optimiser, loads the
  plugin at the LTO pipeline extension point (or runs it through `opt`),
  resolves taint over the whole call graph, and produces a **fat object**:
  native host code for the classical tier, ISA object(s) for the device
  tiers, and a certificate. clang's offload model (outlining, fat
  binaries, a launch runtime) is the **model**, not a reused mechanism: a
  middle-end pass cannot conjure clang's driver machinery, so we own ours.
- **Host-triple IR is what the device lowering accepts**: datalayout, ABI-
  lowered calls, target intrinsics and inline asm arrive as the host front
  end produced them. Target intrinsics and asm are classified *lowered /
  trapped / shimmed* in the coverage report. There is no `bennett` triple,
  because a plugin cannot add a clang target and we do not fork.
- **Stated coverage constraints:** a tainted call needs the callee's
  bitcode. Rust's distributed `std` normally carries embedded LLVM bitcode
  in its rlibs; the driver extracts it where present and compatible, and
  a rebuild (`-Zbuild-std`) is needed only where it is missing or from an
  incompatible LLVM major. The Julia runtime and precompiled native
  libraries need bitcode builds or shims (`bennett-runtimes`). Calls with
  no bitcode are coverage-report lines (*trapped*), never silent.
- **Per-front-end integration is named work**: clang needs only `-flto`
  and the driver; rustc goes through bitcode emission because its in-
  process plugin path is nightly-only; Julia goes through LLVM.jl and the
  same driver in-process. Bennett.jl is the Julia integration.
- A per-TU invocation remains available as a **fast path** for programs
  closed within one unit (the REPL case), with the same semantics.

## 4. The virtual ISA and the device

### 4.1 Why the VM is the revolution

The circuit model is to quantum programming what bare-metal machine code
was to classical programming before virtual machines, virtual memory and
portable ISAs: every program welded to one machine, every vendor with its
own toolchain, no dynamic allocation, no loops beyond what you unrolled by
hand, no portability, no way to ship one artefact to many machines. The
classical world escaped through abstraction layers *between* program and
hardware: virtual memory, the process, the JVM, LLVM, PTX.

Quantum programming has had abstract machines before: Knill's QRAM model
(1996), Quil's Quantum Abstract Machine, eQASM, and the circuit-plus-
classical-controller model every SDK ships. What none of them has is the
*rest* of the classical escape: virtual allocation with classes and
garbage as a resource, bounded coherent control over arbitrary programs
rather than hand-built circuits, separate compilation and linking, a
resource vector in the specification, and a program model that any LLVM
language targets without being rewritten. That combination is the layer
quantum programming lacks. The mistakes of the pre-VM era are listed so
the design never repeats them:

- **No program is written against a machine.** Programs target the virtual
  ISA; hardware implements the ISA through a target description.
- **Memory is virtual.** Qubits are allocated and released through the VM,
  never addressed physically. Clean, dirty and class are properties of an
  allocation request, not of a wire index.
- **Loops and recursion are instructions, not unrolling.** Budgets are
  values the VM enforces.
- **Resource accounting is part of the architecture**, in the ISA spec.
- **The spec is public and versioned.** Governance: PTX and the JVM each
  had a steward and a conformance regime; this ISA has a published spec, a
  conformance suite, and a steward who accepts target descriptions and
  revisions through a recorded process. A vendor implements it before an
  ecosystem exists for the reason vendors implemented PTX: the programs
  are written against it, not against them.

### 4.2 Execution semantics by tier

Two control disciplines, kept apart by name in the ISA:

- **Classical control** (host data, measurement results, run-time
  budgets): genuinely dynamic, an instruction pointer, data-dependent trip
  counts, real allocation. This is where run-time scheduling, history
  layers, checkpointing and pebbling policy live, and **every such
  decision may inspect only classical data**: an architectural invariant.
  Classical checkpointing never copies quantum state; a checkpoint of a
  coherent region is a point from which it is *recomputed*, which the
  scheduler may choose only where the region's own semantics permit.
- **Coherent control** (a decision that depends on a qubit): **predicated
  execution under a classical budget**, in both executors. The general
  construction, for an arbitrary and possibly irreducible post-O3 CFG, is
  a **predicated step machine**: a superposed block counter, stepped for
  the budget, every block executed under the predicate "the counter names
  me"; structured `pred { }` and `loop { }` blocks are optimisations of it
  that the specialiser applies where the CFG is structured. A branch on a
  qubit pays for both arms. An allocation whose size depends on a qubit is
  padded to its bound. The budget is classical and fixed before entry;
  run-time budgets come from the host or from measurement results, never
  from superposed data. **Nothing about the VM makes superposed trip
  counts observable or cheap; what it makes possible is choosing the
  budget at run time from classical data instead of at compile time.**

**Two region interfaces, kept apart by name.** Every coherent region is
one of:

- a **lifted classical oracle**: classical code that the plugin
  reversibilises. It computes one deterministic bounded result F_B(x),
  success or fault, with the interface and the XOR/involution properties
  below. Control is control of the XOR; adjoint is the same region.
- a **quantum action**: a region whose body contains non-permutation
  operations (rotations, Hadamards) or in-place bijections, acting as a
  unitary U on its **declared mutable wires**, with borrowed inputs
  preserved and workspace restored. Control means controlled-U, adjoint
  means U†. It need not be an involution and does not XOR; in-place
  bijections belong here, and because they are total bijections with
  bounded inverses (§3.1) a quantum action has no fault outcome of its
  own: any fallible computation it needs is a lifted oracle it calls,
  whose fault register it declares among its outputs. A quantum action
  whose body contains coherent internal control is, by definition, its
  bounded padded unitary under the declared bound, and that bound is
  part of the action's content identity and certificate entry (the same
  body under two bounds is two unitaries); the budget-fault guarantees
  of this section describe lifted oracles only.

Lifted oracles and quantum actions nest freely; the plugin classifies
each outlined region by its contents and the verifier checks the
declared interface. The step machine records, per step, which
predecessor it came from, which is what makes block-counter transitions
injective at control-flow joins; and at region exit it synchronises: all
branches pad to a common halt counter before control workspace is
restored (the Quantum Control Machine injectivity and synchronisation
conditions, §7).

**Totality of lifted oracles: F_B(x), success or fault.** The oracle's
interface is: inputs (preserved), a caller-supplied output target (any
value), a caller-supplied **fault register**, and workspace. The **budget
unit** is steps of the ISA formal-model interpreter on the materialised
outlined region (§3.2), so the fault set is a property of program plus
budget plus recorded LLVM version and pipeline, never of Bennett's own
lowering; compiled artefacts pad internally as needed and never fault
where the reference does not. On success, F_B(x) = (f(x), 0): the output
target is XORed with f(x) and the fault register is unchanged. On failure,
F_B(x) = (0, code): the output target is XORed with the **canonical zero
payload** (left unchanged) and the fault register is XORed with a distinct
code per cause (budget exhausted: steps, heap, recursion; immediate
undefined behaviour reached; unmodelled effect reached), the code chosen
by the reference semantics. Because both halves are XORs, the region is
an involution on its targets: repeated, controlled and adjoint invocation
compose by XOR accumulation, which is what Grover-style iteration needs.
Inputs are preserved, dirty registers are unchanged and clean workspace is
restored on *every* basis input, faulted or not, by the **prefix-reversal
invariant**: on a faulted branch the step machine continues to the budget
with the fault predicate off, and its recorded history is reversed exactly
as on a clean branch. Two implementations that return the same fault code
therefore return the same quantum state, not merely the same flag. The
fault register is part of the oracle's interface: algorithms test it,
resource estimates report it, and the acceptance tests of §8 require its
rate to be zero on their declared domains, because a nonzero fault code on
some basis inputs entangles the fault register with x and degrades the
interference an algorithm such as Grover relies on. Both executors
implement exactly this; the circuit specialiser is the VM's semantics
under a fixed budget, no more and no less.

**Coherent memory and the region interface.** Classical code acting on
quantum state that outlives a region has exactly these meanings (mirrored
in the dialect, §3.1): a read is a CNOT copy onto fresh workspace, the
source preserved; a write XORs into its target, so writing a known-clean
register is a copy and writing a register not known to be clean is a
compile-time error; region inputs are preserved and declared outputs are
XORed into caller-supplied targets, every other write being restored
workspace; an in-place update x ← g(x) requires a total bijection with a
bounded inverse (a declared `__bennett_inplace(@g, @ginv)` or a library
bijection, §3.1) and is lowered as compute-out-of-place, swap, uncompute-
with-g⁻¹, else it fails loud; a fallible computation is never in-place.
This is the rule that makes controlled modular arithmetic, and `when(q)
do x += a end`, compile from unmodified code.

**Uncomputation validity (the Silq `qfree`/`const` and Unqomp
condition).** Garbage is a cost choice inside a correctness envelope, not
free policy. Each garbage value records its dependency set and was
computed by a `qfree` (classical, permutation-tier) computation; both
halves of the Silq discipline apply. It may be uncomputed by reversal or
recomputation only while that set is unmodified since its computation,
and it **must** be cleaned before any non-permutation operation
(Hadamard, non-diagonal rotation, measurement) or in-place update acts on
a wire in its dependency set, and before the end of the enclosing unitary
region. Measurement-based uncomputation with phase fixup is the
sanctioned alternative where that window has closed, with the fixup
computed for the actual schedule: after an intervening U the correction
D becomes U D U†, and §5.1 part 2 verifies the fixup as scheduled, never
an assumed one.
Compile-time and run-time schedulers choose **only among schedules that
satisfy this invariant**; the handle→wire verifier rejects violations;
conformance exercises them with interference tests (§5.1 part 2). A
scheduler that deferred uncomputation past an interfering operation
would compute the wrong state while every ancilla still returned to zero,
which is exactly the class of bug the invariant exists to make
unrepresentable.

Effects by tier:

| Tier | Where | Effects | Undefined values |
|---|---|---|---|
| classical | host, native | real | real |
| reversible | device | recorded on the effect tape forwards, replayed backwards; the device models console, clock, entropy, block storage as reversible device models; entered through `__bennett_reversible` or a driver mode | refined by the materialised normalisation of §3.2; immediate UB is a fault, recorded |
| coherent | device | **closed and effect-free**: no external effect may occur inside a coherent region. Devices the program touches are virtualised as reversible state inside the device (an in-memory VFS, a console register, a device model) and become part of the oracle's state. Classical inputs are fixed before entry; outputs leave through measurement after exit. An effect the device cannot virtualise is a fault code on the executions that reach it. | refined by the materialised normalisation of §3.2; immediate UB is a fault code |

What the VM physically *is* at run time: a classical runtime that
schedules quantum operations. Coherent regions are lowered to predicated
blocks; the classical runtime decides when to run them, with what
resources, and how to uncompute their garbage, using only classical
information; at launch it lowers predicated ISA blocks to the target's
declared gate alphabet using `bennett-targets` capability declarations
(the specialiser does the same ahead of time). On a simulator target the
VM executes a **permutation segment** by **branch enumeration**: a
permutation applied to a state vector is a permutation of amplitudes, so
the segment is run once per basis configuration of the superposed inputs,
tracking the full configuration including garbage and virtualised device
state. Non-permutation gates between segments (rotations, Hadamards,
measurement-based fixups) are applied to amplitudes and may increase the
branch count. This is what makes small-instance end-to-end demos (§8)
checkable without a state vector the size of SQLite's memory.

### 4.3 Resources

- **The resource vector.** Qubit-time by qubit class is the base. Qubit
  classes are register classes: a target declares tiers with costs, and
  allocation chooses a class the way a register allocator does. Garbage
  carries an occupancy cost per qubit-second. Targets may add energy,
  routing, T, Clifford, measurement, or anything else; the ISA does not
  enumerate resources, the target description does. **Decision rule:** a
  target description supplies either a scalarisation (weights) or a
  lexicographic order over its resources; the scheduler optimises that
  objective and reports every component; conformance tests check the
  accounting of each declared resource against the target's own units.
- **Honest costs of superposition**: a coherent branch pays for both arms;
  a quantum-addressed memory access costs O(N) gates through QROM/QRAM
  circuits unless the target provides QRAM; coherent allocation is padded
  to its bound; dirty ancillae are cheaper to borrow and more expensive to
  use; a predicated step machine over an unstructured CFG costs the budget
  times the block count unless the specialiser recovers structure.
- **Allocation classes:** clean |0⟩ allocation, **dirty borrowing** (a
  first-class resource with no analogue in the current code), and release, with clean release and restored correlations as
  **semantic obligations** checked by simulation (§5.1), since they cannot
  be decided statically in general.

### 4.4 What the ISA spec owns

The ISA spec is one of the two contracts (§6.1). It owns, by name, every
format or interface two repositories exchange across the device boundary:

- the instruction set and its formal model (abstract semantics, the fault
  register, the round-trip theorem);
- the resource vector and the **target-description format**, including
  capability declarations (gate alphabet, QRAM, measurement) beyond costs;
- the **object format** for ISA programs and the **link format** for
  separate compilation, with a call/uncall convention and shared ancilla
  frames (the reversible ABI);
- the **host–device launch ABI**: how a host program starts, suspends,
  reverses, and reads back a device program, budgets and fault registers
  included;
- the **scheduling interface**: scheduling problem in (ISA program, target
  description, objective), schedule and certificate out, with the C ABI,
  objective semantics and versioning, so a competitor's scheduler is
  substitutable and a competitor's VM cannot invalidate compile-time
  schedules;
- the **certificate schema** that `bennett-circuits`, `bennett-arith`,
  `bennett-estimate` and `Bennett.jl` all consume, including the proof-
  versus-evidence labels of §5.1;
- the **coverage-report format** the driver emits;
- serialisation and versioning rules, and the conformance suite.

### 4.5 An illustrative sketch (non-normative)

Instruction classes, not encodings:

```
  region   budget={steps,heap,depth} outputs=… → outputs, fault   ; coherent region entry
  qalloc   class=<name> n=<classical>            → wires           ; clean
  qborrow  class=<name> n=<classical>            → wires           ; dirty
  qfree    wires                                                   ; verifier: clean / restored
  gate     op=<X|CX|CCX|MCX|RZ(θ)|…> wires       → wires           ; linear: consumes, produces
  qload    addr=<wires> mem=<region>             → wires           ; O(N) unless target QRAM
  qstore   addr=<wires> val=<wires> mem=<region>
  step     pc=<wires> blocks=…                                      ; predicated step machine
  pred     p=<wire> { … }                                           ; structured optimisation of step
  loop     bound=<classical> { … }                                  ; structured optimisation of step
  fault    code=<const>                                             ; sets the region's fault register
  measure  wires                                 → classical bits   ; outside unitary regions
  br / call / ret / alloc / load / store                            ; classical control, host data only
  effect   dev=<model> …                                            ; reversible tier only; taped
```

A target description names its qubit classes with costs, its native gate
alphabet, whether it provides QRAM, and its resource scalarisation:

```
  target: surface-code-d17-example
  classes: { logical: {qubit_second: 1.0}, dirty_pool: {qubit_second: 0.3} }
  gates:   { CX: {t: 0}, CCX: {t: 7, depth: 3}, RZ: {t: "synth(ε)"}, measure: {time: 1} }
  qram:    none
  objective: weighted { t: 1.0, qubit_second: 0.05 }
```

## 5. Scenes from the finished thing, and what "correct" means

**The REPL.** Define a Julia function. Do not compile it. Write
`when(q) do f(x) end` and it runs, in a simulator or on hardware, because
compilation is invisible, incremental, cached by world age, composable.
Quantum registers are REPL values with lexical lifetime. `@cost f(x)`
prints T-count, T-depth, logical qubits, and wall time on a named target,
the way `@time` prints allocations. Redefine `f` and everything downstream
recompiles. Hand a compiled function to another function as an ordinary
callee. The Lisp image, holding reversible objects with certificates.

**The toolchain.** `-flto` plus our driver beside clang. Point it at a
mature codebase: one fat object per link, a coverage report honest to the
instruction (lowered / trapped / shimmed), and a resource estimate. Partial
compilation is a region marker, and the toolchain is provably the identity
on everything outside the tainted call graph. The kernel compiles, boots on
the VM in the reversible tier with its devices modelled, writes a serial
console to the tape, and un-boots to the reset vector.

**The device.** The quantum VM of §4, as a device runtime the way a GPU
runtime is: host code at native speed, only device tiers pay for
reversibility.

**The compiler is optimal within what it claims.** Optimality is defined
against a target description and a declared search space. Optimal
reversible pebbling is PSPACE-complete, so: small kernels are exactly
synthesised, and *minimality* is claimed only with a checkable lower-bound
or exhaustive-search certificate (an exact-synthesis witness alone shows
attainability); large programs carry closed-form cost bounds and a
certificate of the gap between the schedule found and the best bound
known. The compiler chooses adders, pebbling, measurement-based versus
unitary uncomputation, QROM versus QRAM, under a space budget.

**The ecosystem.** A registry of reversible libraries with certificates:
libc, libm, zlib, crypto, SQLite, published as linkable ISA objects so
nobody compiles them twice. Arithmetic is library code too (§6).

### 5.1 Correctness

Ancilla-zero is not correctness: every historical S0 defect in this
project passed a reversibility check. Correctness is defined in three
parts, and every certificate labels each claim as **proof** (exhaustive
over a declared finite domain, or compositional/structural) or
**evidence** (sampled, with seeds and counts), never blurring the two.

1. **Permutation tier, by theorem.** Define the permutation tier *after
   decomposition into the gates actually emitted*: a circuit over
   {X, CX, CCX, exact MCX} is a permutation matrix. Relative-phase Toffoli
   decompositions and measurement-based fixups are **not** in this tier.
   A permutation is determined by its action on basis states. Therefore,
   for a region whose declared interface specifies an expected
   permutation P, over a declared finite domain D: if on every element
   of D the artefact's **entire final register tuple** equals P applied
   to that element, then its restriction to D is exactly P, with no
   relative phase and no residual entanglement. For a lifted oracle, D is
   every input x, every output-target value t, every fault-register value
   e, every value of every borrowed dirty ancilla d, clean ancillae in
   their declared state, and P is |x⟩|t⟩|e⟩|d⟩|0⟩ ↦ |x⟩|t ⊕
   payload(F_B(x))⟩|e ⊕ code(F_B(x))⟩|d⟩|0⟩, where F_B is the bounded
   reference result of §4.2 (native execution supplies f(x); the embedding
   specification supplies the rest). For an in-place bijection, P is
   |x⟩|0⟩ ↦ |g(x)⟩|0⟩ on the mutable wires with workspace clean, and the
   same check establishes g∘ginv = id. Input preservation is a
   hypothesis of the theorem and an acceptance check, not a consequence:
   an artefact that flipped an input bit after an otherwise correct oracle
   would pass every output-only check. **Exhaustive agreement on D is
   complete for D. Sampled differential testing above exhaustive widths is
   evidence, labelled as such.** Clean release and dirty restoration are
   checked by this simulation, not statically.
2. **Non-permutation lowerings, by channel comparison.** Measurement-based
   uncomputation is a channel (an instrument where outcomes are exposed),
   not a unitary on the data; rotations and synthesised gates are unitaries
   with an approximation budget ε. Every such lowering is verified against
   its reference by **process comparison at exhaustive small widths**: the
   induced channel (Choi-state comparison, including a reference system to
   catch lost correlations) for measurement-assisted implementations, and
   unitary equivalence plus **controlled-interference tests** (the artefact
   run controlled and inside an interferometer) for unitaries, with ε and
   its **composition rule** stated per artefact: the metric is the diamond
   norm for channels and a phase-sensitive operator-norm bound for
   unitaries under control, budgets add along a sequence, and the
   certificate carries the sum. Floating-point matrix agreement counts as
   proof only with a rigorous numerical error bound; otherwise it is
   evidence. This is proof for the widths tested and evidence above them.
3. **Algorithms, compositionally.** Grover, amplitude estimation and
   friends are verified by state-vector simulation at small instance size
   with the compiled oracle applied by branch enumeration over its
   permutation segments (§4.2), and resource estimates are produced from
   the oracle's certificate without materialising gates.

**Equivalence is "equals native, or is flagged".** On every element of a
rung's declared domain the artefact must return either the native result
or a fault code; the fault rate over the domain is reported and must be
zero on the rung's acceptance instances; inputs the instrumented
classifiers of §3.2 report as *undefined*, and executions the reference
interpreter classifies as *layout-dependent*, are excluded from native
comparison, validated against the reference interpreter, and counted
separately, with each rung reporting and bounding both excluded
fractions. One outcome table governs §3.2, §5.1 and §8: native-
comparable success, reference fault, layout-dependent reference
validation, classifier-flagged undefined. Domain D stays finite and tractable when large dirty pools
are borrowed by a structural lemma: borrowed wires are used only inside
verified compute–use–uncompute frames, so their restoration is proved per
frame; where that lemma does not apply, dirty restoration above small
widths is labelled evidence.

**What a certificate asserts:** the ISA object, the target, the objective,
the claimed resource vector, the tier and budget of each region, the
definedness assumption, the verification performed (parts 1–3, with
domains, widths, seeds and counts, each labelled proof or evidence), the
fault rate per declared domain, and for small kernels an exact-synthesis
witness and, where minimality is claimed, its lower-bound certificate. A
checker in `bennett-conformance` validates a certificate against the
object without trusting the compiler; replayable validation records are
not proofs and are labelled evidence.

## 6. The right language for each job

| Component | Language | Why (taste excluded) |
|---|---|---|
| Pass plugin (taint, outlining, body generation, lowering to the ISA) | **C++** | The only component of the compiler core that links LLVM (Bennett.jl, as a front end, uses LLVM.jl). `llvmGetPassPluginInfo` has C linkage, but registering a new-PM pass and every analysis the plugin needs (loop info, dominators, scalar evolution for bound refinement, alias analysis, MemorySSA, `CodeExtractor`) are C++ API only. v1 is the evidence of avoiding this: it reimplements loop analysis in `src/lowering/cfg.jl` and parses MemorySSA out of printed text in `src/memssa.jl`. Enzyme is C++ for the same reason. Built per LLVM major. Kept narrow: it does not contain the scheduler. |
| Scheduler and cost model (`bennett-sched`) | **Rust**, C ABI owned by the ISA spec | Linked by the plugin (compile time) and the VM (run time); it is what makes decision 6 literally true. No LLVM dependency. |
| ISA spec tooling, VM / device runtime, circuit specialiser, estimator | **Rust** | None touch LLVM: they consume the ISA's serialised form. Embeddable device library with no runtime; memory safety in a component that must never crash a host; usable without std near kernels; a JIT tier available without LLVM. Rust ownership is affine, not linear, so it models qubit ownership well with a leak check, not natively. |
| Driver | **Rust**, invoking LLVM tools (`opt`, `lld`) as external processes and the plugin through them | The driver orchestrates bitcode but does not link LLVM itself; that keeps the "C++ only where LLVM is linked" rule true. |
| **The Julia quantum language**, REPL, research laboratory | **Julia (Bennett.jl)** | Bennett is the family name: Bennett.jl *is* the Julia quantum language (`when`, oracles, in-place regions, certificates, `@cost`), the first front end built on the dialect, and the product's face. The former Sturm.jl is sunset; its surface constructs and its MCX kernel are absorbed here. Bennett.jl orchestrates the driver in-process through LLVM.jl while the LLVM tools themselves run out of process; new lowerings and arithmetic are prototyped here against the spec. |
| Arithmetic and runtime libraries (adders, multipliers, QROM, soft-float, allocator shims, libc, device models) | **Any** | Ordinary code compiled through the same pipeline and shipped as ISA objects with certificates. "Runtimes are libraries" applies to arithmetic too; the specialiser links them. |

Consequence: the centre of gravity leaves Julia. Bennett.jl is the front
door of Bennett, not the whole of it. The maintainer has stated this is
acceptable; the north star outranks language preference.

### 6.1 Many small repositories, two contracts, fully enumerated

**A monolith will grind to a halt** (maintainer, 2026-10-28). Independent
repositories, each developable, versioned, tested, and released on its
own, communicating only through **two published contracts**:

- **`bennett-dialect-spec`**: the marker-function ABI (names, signatures,
  the positive legality requirement), the portable handle convention, the
  outlining, budget and region well-formedness conventions, the legality
  conformance corpus, the driver's plugin-invocation interface,
  versioning.
- **`bennett-isa-spec`**: everything in §4.4: instruction set and formal
  model, resource vector and target-description format with capabilities,
  object and link format with the reversible ABI, host–device launch ABI
  (including how host code that interleaves genuine host effects with
  handle or measurement manipulation is split from the device's
  classical-control tier), scheduling interface, certificate schema,
  coverage-report format, serialisation, conformance suite. Its sub-
  artefacts (ISA, object format, launch ABI, certificate schema) are
  versioned independently.

Nothing shares code across a contract boundary; anything that needs to is
a sign the boundary is wrong. **One semantics comes from the ISA spec's
formal model and conformance suite, never from shared code.** The dialect
spec additionally carries a **reference semantics** from marker programs
to the ISA formal model (including the copy, store and in-place rules of
§4.2), so a competing plugin is conformance-tested at spec level and not
only by native differential. **Binary edges are versioned too:** a
`bennett-sched` built against ISA spec vN is replaceable without
rebuilding the plugin, and a plugin is replaceable without rebuilding the
driver; the substitutability test covers binary edges as well as document
edges.

| Repository | Owns | Depends on |
|---|---|---|
| `bennett-dialect-spec` | as above, plus the normalisation rules and residual-poison validator | ISA spec (its reference semantics targets the ISA formal model) |
| `bennett-isa-spec` | as above | nothing |
| `bennett-sched` | scheduler and cost model behind the ISA spec's scheduling interface | ISA spec |
| `bennett-plugin` | the C++ LLVM pass plugin; built per LLVM major | dialect spec, ISA spec, sched (binary) |
| `bennett-driver` | link-time driver: bitcode merge, plugin invocation, fat objects, launch, coverage reports; per-front-end integration | dialect spec, ISA spec, plugin (binary) |
| `bennett-vm` | the Rust device runtime: classical-control tier, history layers, effect tape, device models, branch-enumeration simulation, launch-time lowering to the target alphabet, JIT tier | ISA spec, sched |
| `bennett-circuits` | the bounded specialiser: hierarchical circuit IR, placement, proof-carrying output, exporters (OpenQASM 3, QIR, Quil) | ISA spec, sched |
| `bennett-estimate` | resource estimation from ISA objects, certificates and target descriptions, no gates materialised | ISA spec |
| `bennett-targets` | target descriptions per hardware model, contributed by vendors; importers for existing resource-model formats | ISA spec |
| `bennett-runtimes` | allocator, libc/musl shims, device models, Julia shim runtime, bitcode builds of language runtimes, as ordinary code compiled to ISA objects | dialect spec; driver (build tool) |
| `bennett-arith` | adders, multipliers, QROM, soft-float, as ISA library objects with certificates | dialect spec; driver (build tool) |
| `Bennett.jl` | the Julia quantum language: `when`, oracles, in-place regions, certificate kinds, simulators as VM targets, REPL, `@cost`, research lab | driver (binary), ISA spec |
| `bennett-conformance` | the demo ladder as executable gates, the certificate checker, the legality corpus runner, the differential harness with the instrumented classifiers of §3.2 | everything, as a consumer only |

The test of the split: every repository can be replaced by a competitor's
implementation of the same spec without the rest noticing.

## 7. Landscape: what is taken, what is rejected, what is new

| System | What Bennett takes | What it does differently |
|---|---|---|
| **Enzyme** | The delivery model: an LLVM plugin, marker calls, optimise–transform–optimise, LTO for cross-TU bodies, per-LLVM-major builds; activity analysis as the precedent for taint analysis. | Reversibilisation instead of differentiation; the output is a program for a second executor, not more LLVM IR. |
| **PTX / CUDA, OpenMP offload** | Virtual ISA with per-hardware target descriptions; host/device split; fat objects; a launch runtime. | We own the driver and launch runtime; nothing is reused from clang's offload machinery. |
| **Quil / QAM, eQASM, Knill's QRAM model** | The idea of a public abstract machine with a classical controller; Quil as an import/export format. | Those machines execute hand-built circuits with classical control; none has virtual allocation classes, garbage as a resource, bounded coherent control over arbitrary programs, linking, or a resource vector. |
| **QIR** (QIR Alliance) | LLVM as the carrier; profiles as a warning. Its adaptive profile and memory-management spec exist and are read on import. | Stated precisely: qubits are opaque pointers with no ownership discipline (they do participate in SSA dataflow); adjoint and controlled bodies are emitted by the front end as separate functions, so the IR carries no structural algebra over them; no uncomputation, garbage, resource model, or oracle abstraction; the profiles mix "program the host runs" with "circuit the device executes". Bennett keeps control and adjoint structural, keeps ownership explicit in the ISA, and puts resources in the spec. |
| **OpenQASM 3** | `ctrl@` / `inv@` modifiers and its dynamic classical control as the export target's expectations. | OpenQASM 3's dynamic control is classical control (§4.2); it is a circuit language, not a program model with memory, linking, or resources. Export only. |
| **CUDA-Q / Quake** | Quantum kernels as device code; `cudaq::control` / `cudaq::adjoint` at function granularity; the ref-vs-wire distinction, adopted as dialect-vs-ISA. | Not a new language or kernel annotation: taint is inferred over unmodified C, Rust, Julia. The carrier is LLVM bitcode, because that is what every front end emits; MLIR lowering paths are an import door. |
| **Catalyst, MLIR quantum dialects, Qrisp** | Import path for programs already in those dialects; precedent for a JIT tier; Qrisp's automatic uncomputation over Python-level programs. | Arbitrary LLVM programs, not a Python-hosted language. |
| **Q#** | Adj+Ctl specialisation from one body. | Specialisation in the plugin over any language's IR, not in one language's compiler. |
| **Quipper** | Oracle synthesis from classical code; `with_computed`. | Any LLVM language; a VM and ISA beneath. |
| **Silq, Unqomp, Reqomp, SQUARE** | Automatic and budgeted uncomputation; garbage as a resource with a budget; **the uncomputation-validity condition of §4.2 is Silq's `qfree`/`const` discipline and Unqomp's criterion, adopted as an ISA invariant.** | Uncomputation scheduled at run time by the VM as well as at compile time, under a target's resource vector, inside that invariant. |
| **Quantum Control Machine (Yuan, Villanyi, Carbin 2023)** | The injectivity and synchronisation analysis of quantum control flow, which the step machine of §4.2 must satisfy. | Bennett's embedding preserves classical inputs through the oracle interface and cleans control state at region exit, rather than lifting unrestricted quantum control flow. |
| **QCOR / XACC, Qiskit classical-function compiler, tweedledum / RevKit, ProjectQ Compute/Uncompute, REVS (Parent–Roetteler–Svore)** | C++ quantum kernels through a clang plugin with compute/action/uncompute and automatic ctrl/adjoint; oracle synthesis from classical functions; the compute/uncompute idiom. | Whole programs in any LLVM language rather than annotated kernels or small classical-function languages; a VM and ISA beneath. |
| **Tower, Spire** | Superposed pointers and classically bounded recursion as the right semantics for coherent data structures; Spire's accounting of the cost of padded coherent control. | The same semantics, for programs nobody rewrote; the step machine of §4.2 is the general case. |
| **Qualtran, Azure RE** | Symbolic, hierarchical resource counting without materialised gates; target models as data. | Certificates attached to linkable objects; the target-description format accepts imported models, converting units where they align with the target's declared resources and otherwise importing them as new named resources. |
| **QSSA, QIRO, HUGR / Guppy / tket2** | Linear SSA for quantum values; HUGR's hierarchical hybrid graph and Guppy's Python-embedded typed quantum language as the closest contemporary program-level IR. | Used in the ISA, not imposed on LLVM IR; HUGR is an import/export door. |
| **ReVerC** | Verified reversible compilation of a small language. | Correctness by theorem plus oracle (§5.1) for arbitrary LLVM input. |
| **Reversible pebbling (Bennett 89, Knill 95, PRS15, Chan et al.)** | The space-time trade-off theory and its hardness result. | Pebbling as run-time policy over a resource vector, not only a compile-time choice. |

**What is new**, claimed narrowly: (a) inferred-taint reversibilisation of
unmodified programs in any LLVM language, delivered as a link-time plugin,
with total coherent regions and a fault outcome; (b) a public virtual ISA
for quantum programs with virtual qubits, allocation classes, bounded
coherent control of arbitrary CFGs, garbage as a scheduled resource, a
resource vector, linking, and a host–device ABI; (c) one scheduler used at
compile time and run time behind a published interface; (d) correctness
defined by the permutation theorem plus channel-comparison oracles,
attached to linkable objects as certificates that separate proof from
evidence. Everything else is adopted from the systems above with
attribution.

## 8. Demo ladder (success criteria, each with its acceptance test)

| Rung | Demo | Acceptance test |
|---|---|---|
| 1 | Scalar C, Rust, Julia functions | Exhaustive at Int8 over the full domain D of §5.1 part 1, both executors equal to native; fault rate zero. |
| 2 | Pointers, structs, byte memory | A C hashtable (the existing 258-line corpus): forward result equal to native on every tested input (independent check), then reversed byte-exactly, both executors. |
| 3 | musl hello-world | Forward output equal to native; run in the reversible tier with a console device model; un-run to the reset state; tape replay deterministic. |
| 4 | **Grover over SQLite** | SQLite compiled unmodified to the coherent tier under a region budget, with an in-memory VFS over quantum-addressed memory. Database of N rows fixed classically before entry; the predicate is a real SQL query parameterised by a `rowid` bound from the superposed register; the oracle bit is the query's match for that row. (a) Oracle verified by §5.1 part 1 over all rows and all target values for N ≤ 2¹⁰, fault rate zero. (b) End-to-end Grover by state-vector simulation with branch enumeration at N ≤ 2⁸. (c) A resource estimate for N = 2²⁰ under a named target, reporting the budget and the padded cost. Nobody rewrote SQLite. |
| 5 | Julia on a shim runtime | `push!` and `Dict` work because the allocator works, with zero compiler awareness of either; forward results equal to native Julia; reversal exact. |
| 6 | xv6, then Linux `tinyconfig` | Serial console output equal to a native (QEMU) run of the same image (independent forward check); boots in the reversible tier with device models; un-boots to the reset vector; tape replay byte-identical. |
| 7 | **Quantum fuzzing of the kernel** | Kernel state snapshot fixed classically after boot; a step budget; syscall arguments as the superposed input over a declared small space; devices virtualised; the oracle bit is the panic flag. The contract is the optimised-IR reference semantics of §3.2 under a recorded definedness assumption; the kernel's own source UB is not detected after optimisation and is not claimed to be. (a) Oracle verified by §5.1 part 1 against native execution of the same snapshot per basis input, with classifier-flagged inputs reported, fault rate zero on the declared space. (b) Amplitude amplification by state-vector simulation at a toy argument space. (c) A resource estimate under a named target. The oracle is Linux. |
| 8 | **Amplitude estimation on a Monte Carlo in plain C** | Written by someone who has never heard of a Toffoli gate. The entropy device is replaced by a superposed register; everything else is fixed classically before entry. (a) Oracle by §5.1 part 1; (b) estimation by simulation at small precision; (c) resource estimate. |

Rungs 1–3 and 5–6 are the blueprint's; 4, 7, 8 define success for the
vision; nobody promises 6–8 on a schedule.

## 9. Open technical questions (deferred by the maintainer's rule: vision first)

In the order the next iteration should take them. Items the council
promoted from "detail" to "load-bearing" are now answered at vision level
above and appear here only for their mechanics.

1. **The legality spike** (§3.2): the marker corpus against every stock
   pass at O3 and through native codegen; emission examples from clang,
   rustc and Julia; gate on freezing the dialect spec.
2. **Handle → wire conversion**: the verifier, what it rejects (including
   the uncomputation-validity invariant and the copy/store/in-place rules
   of §4.2), the leak check.
3. **Compilation model mechanics** (§3.3): LTO extension point vs `opt`;
   fat-object layout; the launch ABI; host-triple intrinsic and asm
   classification tables; bitcode builds of language runtimes.
4. **Budget mechanics**: out-of-band budget tables; scalar-evolution
   refinement; how the specialiser recovers structure from the step
   machine; the exact fault-code set.
5. **Effect virtualisation**: which device models exist (VFS, console,
   clock, entropy, block device, network as a recorded peer), how they are
   expressed as reversible state, what is refused.
6. **Measurement-based uncomputation under control**: the v1
   `PermClean`-style certificate (inherited from the sunset Sturm.jl)
   cannot express it; the certificate kind with classical fixup and its
   controlled form, fixed in Bennett.jl's language before any gate record
   freezes.
7. **Reversible ABI and linking**: call/uncall convention, shared ancilla
   frames, structural symbol resolution, content-addressed objects.
8. **Run-time scheduling policy**: history layers, checkpoint interval,
   delta quality, recomputation of coherent regions, as resource policy
   under the vector of §4.3.
9. **ISA serialisation and versioning**; conformance suite; the formal
   model's scope.
10. **Per-LLVM-major builds**; Julia in-process invocation through LLVM.jl.
11. Concurrency (sequentialised with a recorded schedule; the single-
    thread assumption of §3.2 is the v1 contract), self-modifying code,
    signals, setjmp. Floating point is decided in §3.2 (deterministic
    soft-float in both builds) and is no longer open.
12. Repository hosting and release mechanics for §6.1.

## 10. Process

Vision first (this document), iterate with the council, then design, then
spikes, then code. The current Bennett.jl and BennettVM.jl are frozen as
the v1 reference and differential oracle. No reboot code is written on the
strength of this document. Worklog, beads, red-green, exhaustive
verification, no remote CI carry over unchanged.


# Background (not graded): `Bennett-ISA-Spec.md`

# Bennett Virtual ISA — Specification, draft 0.8

**Date:** 2026-10-28. **Status:** draft 0.8, **accepted by the council
in round 8** (codex, muse and opus all accept with no blocking issue;
core consensus from round 7; mean 4.17/5; reports and the editor's
responses under `docs/council/isa-2026-10-28/round-{1..8}/` in the
`bennett` meta repository). Implementation is expected to expose
frictions; revisions go back through the council. Founding text of
`bennett-isa-spec` (`Bennett-NorthStar.md` §4.4, §6.1); the north star
governs where this draft is silent. Nothing is implemented. MUST, MUST
NOT, SHOULD, MAY are normative; *(non-normative)* explains; *(deferred)*
names items left open; every deferred decision that an implementer must
take carries a **default** in §17, which implementers follow until the
item is revised.

**Versioning.** ISA 0.8, object 0.8, launch 0.8, sched 0.8, cert 0.8,
coverage 0.8, target 0.8. The **full version string** (`0.8`) is part of
every semantic envelope (§9.2): drafts are not compatible with each
other.

---

## 1. Scope and conformance

### 1.1 What the ISA is

A program model for classical, reversible and coherent computation with
one semantics, executed by the VM (`bennett-vm`) and the circuit
specialiser (`bennett-circuits`), produced by the plugin
(`bennett-plugin`) through the dialect's reference semantics, scheduled
through §11, described for hardware by target descriptions (§8). Nothing
here refers to LLVM.

### 1.2 Conformance classes

| Class | Who | Obligation |
|---|---|---|
| Executor | VM, specialiser, hardware stacks | §3–§7, §14 exactly; suites A–E, H |
| Producer | plugin, library compilers | well-formed objects (§9, §16) and regions (§5, §6); suite F |
| Scheduler | `bennett-sched` and competitors | §11; only schedules valid under §6; suite H |
| Checker | `bennett-conformance` | validates certificates (§12) without trusting producers |
| Target author | vendors | target descriptions (§8); suite E |

### 1.3 Deferred *(asserted non-semantic)*

Binary encodings (§16 text is the interchange form); mechanisation of
§14; device models beyond §7.3; the gate-name registry process; the
memory layout of the opaque C objects of §10–§11 (every constructor,
accessor and destructor is listed). **Minimality claims** (north star
§5) are not supported by cert 0.8 and MUST NOT appear in a certificate.
Decisions deferred to implementation, each with its default, are listed
in §17.

## 2. Terminology

- **Tier.** CC, R, Q. **Wire**, **bundle** `wire[N]` (little-endian).
- **Location** `reg[N]`: a named mutable cell of an oracle or lproc
  register file. **Pseudo-location**: an oracle interface input or
  classical argument, readable in the oracle body only, never written.
- **Region**: a Q function with a declared interface: **lifted oracle**
  (§5.2) or **quantum action** (§5.3); **permutation action** (§5.3).
- **lproc**: a lifted procedure with its own params and locations; it
  resolves names only to its own params and locations (§3.7).
- **Budget**: classical (B, heap_limit, stack_limit, depth_limit).
- **Frame**: per machine step: `old_pc`, slots (assignment, capture and
  delivery slots, §3.6), `flag`, `succ`.
- **Basis configuration**: classical values on every component of D.
- **Gate classes.** Permutation: `x cx ccx mcx swap`. Diagonal: `s sdg t
  tdg cz rz`. Non-diagonal: `h rx ry`.
- **Effective control context** at a point: the set of wires on the
  active predicate stack plus the inherited control context (the control
  wires of every enclosing `ctl` and predicate stack of every enclosing
  invocation, transitively); duplicates count once. Its size is the
  **effective control count**.

## 3. Machine model

### 3.1 Tiers and the control invariant

```
  CC ──calls──▶ R functions (call/uncall)       CC ──calls──▶ Q regions
  R  ──calls──▶ R functions, Q regions          Q  ──calls──▶ Q regions (§5.5); oracle bodies call lprocs
```

CC runs on the device's classical-control processor; the host reaches
the device only through §10. **No instruction in any tier makes a
control or scheduling decision that depends on the value of a wire**
except through predication (§3.5). Gate angles are finite `f64` literals
or classical arguments fixed at region entry.

### 3.2 State

| Component | Tier | Contents |
|---|---|---|
| classical environment | CC, R | dynamic SSA instances (§7.4), block parameters, activation stack, **quantum-register handles** (`qreg[n]`, §3.3) |
| classical memory | CC, R | byte-addressed, little-endian, sparse; allocation table (§7.1) |
| effect tape, entropy tape | R | §7.3 |
| run history | CC, R | one frame per executed instruction (§7.4) |
| wire store | Q (CC via `qreg`) | live wires with roles `input target fault borrowed mutable workspace location cell` |
| quantum memory | Q | regions of `wire[W]` cells: local (§4.6) or interface (§5.1) |
| register file | Q | locations of the active oracle and its lproc closure (§3.7) |
| predicate stack | Q | wires; the active predicate is their conjunction |
| oracle step state | Q | `pc, pc' : wire[P]`; `faulted : wire`; `code : wire[F]`; `result_val : wire[T]`; counters (§3.7); B frames |
| budget | Q | classical: B, heap_limit, stack_limit, depth_limit |

### 3.3 Types, ownership, operand schema

```
  iN (1 ≤ N ≤ 128)   ptr (width ptr_width)   f64   token   qreg[n]   region[A,W]
  wire   wire[N]      linear values in structured code and interfaces
  reg[N]              a location (oracle bodies, lprocs); not linear
```

**Linear SSA with implicit versioning** (structured code and CC region
calls): a `wire`/`wire[N]` value is produced once and consumed once;
mode `in` consumes and re-produces a successor of the same name;
`consume` consumes; `produce` creates; a name is not used after
`consume`. **Regions are threaded the same way.** **Indexed operand**
`w[i]` (literal i) borrows wire i for one instruction.

**Disjointness.** The wire operands of one instruction are pairwise
distinct; **every wire of the effective control context is distinct from
every target and from every consumed or produced operand** of an
instruction executed under it (so `qpred p; x p` is ill-formed); a
predicate wire is not modified between its push and its matching pop; a
`qif`/`qloop … while` selector is not modified inside its arms or body.
A region's interface bundles and regions are pairwise disjoint.

**Per-opcode operand schema** (§4.8): every opcode has a tier set, a
fixed arity, operand kinds and a result type; results are written first
(`w = op a b`), modes are never written, and **result types that are not
determined by the operands are written as a suffix** (`r = const.i32 5`,
`r = zext.i64 a`, `r = trunc.i8 a`, `r = ptrtoint.i64 p`, `p = inttoptr
a`). Width rules: `binop`/`icmp` operands equal width; `select` arms equal
width; `zext`/`sext` strictly widen, `trunc` strictly narrows; `load.iN`
and `lift.load.iN` require N ∈ {8, 16, …, 128}; `measure` of `qreg[n]`
with n ≤ 128 yields `in`; signed division truncates toward zero.

**Lifted width rules** (suite F; a mismatch is ill-formed, never a
truncation or an extension). Every address operand (`a` of `lift.load`/
`lift.store`, `p` of `lift.boundscheck`/`lift.free`) and every address
result (`w` of `lift.addr`/`lift.alloc`) is `reg[ptr_width]`; the length
`n` of `lift.alloc`/`lift.boundscheck` is a location of any width or a
literal in [0, 2^ptr_width); `inrange` and every prospective sum are
computed at width max(widths of the operands involved) + 1 with no wrap.
The destination of `lift.label` and the operand of `qjumpr` have any
width N with 2^N > n (the index-space size). `lift.call` arguments have
exactly the callee's parameter widths and its destination the callee's
result width; `lift.ret v` has the containing lproc's result width;
`lift.oracle_call`/`lift.oracle_uncall`/`lift.perm_call` operands have
exactly the callee signature widths, and `mem` operands name caller
regions whose `[A,W]` equal the callee's and whose role is `in` for an
`in` slot (an `in` region is never passed to a `mut` slot); `fault C` and
`lift.faultif p C` require the literal C < 2^F; the width rules above
for `binop`, `icmp`, `select`, `zext`, `sext`, `trunc` apply verbatim to
their `lift.*` counterparts; the destinations of one `lift.parmov` are
pairwise distinct.

**Quantum registers in CC.** `qreg[n]` names n device-resident wires. A
handle is in exactly one state: **live**, **viewed** (one slice of it is
live) or **consumed**; an instruction whose precondition fails is a CC
trap. **Handle transitions:**

| Instruction | Precondition | Effect |
|---|---|---|
| `q = qreg.new cls n` | – | q live, clean |
| `qreg.free q` | q live, not a view, clean on every basis configuration (a simulator checks and reports `E_QREG_NOT_CLEAN`; hardware records a program error in the run) | q consumed |
| `q2 = qreg.slice q lo len` | q live, not a view, lo + len ≤ n | q2 live (wires [lo, lo+len) of q), q viewed; q2 MUST be the operand of exactly one region call and of nothing else; after that call q2 is consumed and q is live again; any use of q while viewed is ill-formed (suite F) |
| `q = qreg.concat q1 q2` | q1, q2 live, not views | q1, q2 consumed; q live over the wires of q1 then q2 |
| region call (§4.7) with q as operand | q live (a view included) | q unchanged |
| `r = measure q` | q live, not a view | q consumed, its wires released |
| reversal of a `qreg.*` frame (§7.4, §10) | – | the handle states before that frame. A `measure` frame is **never reversed**: a segment containing one cannot be uncalled (§7.4) and a run containing one is not reversible (§10) |

**Binding**: a `qreg[n]` argument fills a `wire[n]` slot bit for bit (bit
0 ↔ wire 0); it fills a `region[A,W]` slot iff n = 2^A·W with cell i =
bits [iW, (i+1)W). Host-supplied register ids are `qreg` values of the
same type.

### 3.4 Execution in CC and R

Sequential small-step execution with an instruction pointer, block
parameters instead of phi nodes, dynamic control flow and allocation;
every executed instruction pushes a run-history frame (§7.4).

### 3.5 Predication

Every Q instruction with unitary semantics executes controlled on the
active predicate. `qpred w` pushes, `qunpred w` pops the same wire; the
stack is empty at region entry and exit. Allocation, borrowing, release,
region creation and image gates are **unconditional**; only gates
(including those inside copy/XOR/exchange/memory instructions) are
controlled.

### 3.6 The predicated step machine

**Index space.** `I[0..n)` = the oracle's blocks in text order, each
contiguous; then the blocks of every lproc in its **lproc closure**
(transitively reachable through `lift.call`, linked ones included),
lprocs ordered by closure hash with SCC members in SCC index order, each
lproc's blocks in text order. `HALT = n`; 2^P > n. Branch and call
targets are labels; `w = lift.label ^b` is the only way a location
obtains an index value; executors MAY re-index dispatch extensionally
**provided every label value observable through `lift.label` keeps its
canonical numeric value**. **Terminators**: `qjump qbranch qjumpr lift.
ret lift.retval fault`; every block ends in one; no label names HALT;
**only `lift.retval` reaches HALT with success**.

**Row classes.** Each §4.2 row is an **assignment** (A: written
locations/cells receive values computed out of place into frame slots
`disp_j`, then exchanged in, so `disp_j` retains the displaced old
value), a **direct** row (D: a controlled permutation in place), or
**mixed** (A+D) with an explicit ordered list of **elementary
sub-operations** printed in §3.7. **Slot kinds.** An **assignment slot**
receives a value computed out of place and is then exchanged with its
destination (it retains the displaced old value). A **capture slot**
receives a value computed out of place and is never exchanged (it
retains that value as history: the arguments of `lift.call`). The
**delivery slot** of `lift.ret` is a capture slot that is subsequently
exchanged, under a condition, with the destination location. Rows with
a **flag** compute it into `frame.flag` from the old state before any
effect; rows with a data-dependent successor compute it into `frame.
succ` before any effect; conditional-fault rows perform `faulted ^=
flag`, `code ^= flag·C` after their other effects.

**Frame layout** (fixed per oracle): `(old_pc : wire[P], disp_1..disp_
{k_max}, flag : wire, succ : wire[P])`, `k_max` and widths `W_j` from the
widest write sets used (§4.2 lists each row's slot use).

**Forward machine step** t (1 ≤ t ≤ B), reads referring to the state at
the start of the step:

1. **Dispatch.** `at_k = (pc == k)` for k = 0..n into clean scratch.
2. **Execute.** For each k < n in index order: push `at_k`; run `I[k]`'s
   row: (a) compute `flag` into `frame_t.flag` if the row has one; (b)
   compute `succ` into `frame_t.succ` if data-dependent; (c) for A rows,
   compute **every** written value into its slot, then exchange **every**
   slot with its destination (all computes precede all exchanges); for D
   rows apply the row's permutation; for A+D rows follow the row's listed
   order; (d) apply the fault writes; pop `at_k`.
3. **Successor.** For each k < n, under `at_k`: XOR the row's successor
   into `pc'` (a label index under `flag`/`¬flag` as stated, or
   `frame_t.succ`). Under `at_HALT`: XOR `HALT` into `pc'`.
4. **Commit pc.** `qexch pc pc'`; `qexch pc' frame_t.old_pc` (now `pc` is
   the next index, `pc'` is clean, `old_pc` holds the old index).
5. **Clean dispatch.** Uncompute every `at_k` from `frame_t.old_pc`.
6. Decrement the classical step counter.

**Inverse machine step** (prefix reversal runs it for t = B..1), in
this order:

1. Recompute every `at_k` from `frame_t.old_pc`.
2. `qexch pc' frame_t.old_pc`; `qexch pc pc'` (restores the old `pc`;
   `pc'` again holds the successor value; `old_pc` is clean).
3. For each k < n under `at_k`: XOR the row's successor into `pc'` again,
   using `frame_t.flag` / `frame_t.succ`; under `at_HALT`: XOR `HALT` into
   `pc'` (`pc'` is now clean).
4. For each k < n in **reverse index order** under `at_k`: undo the fault
   writes (`faulted ^= flag`, `code ^= flag·C`); then undo the row's
   effects. **D row**: its sub-operations in reverse order, each by its
   own inverse (`lift.perm_call` by the callee's adjoint; XORs,
   controlled flips and exchanges by themselves). **A row**: exchange
   every assignment slot back with its destination **in the reverse of
   the forward exchange order** (the forward order is the row's listed
   slot order; every destination address, forward and inverse, is
   evaluated from the state current at that exchange, so an indexed
   destination such as `alloctab[atop]` is addressed with the counter
   value that the earlier inverse exchanges have already restored), then
   **uncompute every slot from the restored old state** (the same
   out-of-place computation, applied again as XOR, clears it).
   **A+D row**: **the exact reverse of its complete §3.7 sub-operation
   list**, each elementary sub-operation inverted at its reversed
   position: a direct sub-operation by its own inverse; an assignment
   sub-operation by exchanging its slot back and then uncomputing the
   slot; a capture sub-operation by uncomputing the slot (its source has
   been restored by the sub-operations already undone); the delivery
   sub-operation by the same conditional exchanges. **Every address and
   condition is evaluated from the state current at that position of the
   inverse** (so the `lift.ret` stack addresses and delivery condition
   use the callee `fp` restored one position earlier, and the `lift.call`
   record base uses the restored `sp`); §3.7 prints both inverse lists.
   Finally uncompute `frame_t.succ` and `frame_t.flag` from the restored
   old state.
5. Uncompute every `at_k` from `pc` (which now equals the old index).

After the inverse step every frame field is clean. *(non-normative)* The
forward step is a permutation Π_t; the inverse step is Π_t⁻¹ written
out; T2 relies on nothing else. B = 0 is legal: the oracle commits
`FAULT_BUDGET_STEPS` on every input.

### 3.7 Register files, procedures, counters, stack

**Name resolution.** A read operand of a lifted row in an **oracle body**
is a location of the oracle or a pseudo-location (an interface input or
a classical argument). A read operand in an **lproc** is a param or
location of that lproc; nothing else. A written operand is a location of
the containing function. Globals and mapped interface regions are
reached only by address: `w = lift.addr @g`. Lprocs receive everything
else as parameters.

An oracle declares `regs { … }`; each lproc declares `params`, `result`
width and `regs`. All locations are clean at entry. The oracle's
`result_val : wire[T]` (T = the `tgt` width) is step state, initially 0.

**Counters and sizes.** Size exponents: `mem` 2^H byte cells, `alloctab`
2^A_tab entries, stack 2^S_cells cells. Counter widths: `heap_used :
wire[Hc]`, Hc ≥ H + 2; `atop : wire[Ac]`, Ac ≥ A_tab + 1; `sp, fp :
wire[Sc]`, Sc ≥ S_cells + 1; `depth : wire[Dc]`, Dc ≥ ⌈log₂(depth_limit +
2)⌉. Every prospective sum (`heap_used + max(n,1)`, `sp + R_f`, `depth +
1`) is computed at width max(operand widths) + 1 before comparison, with
no wrap. `bennett_budget` rejects limits that do not fit (§5.4).

**Initial allocator state** (oracle entry): `heap_used = 0`, bump =
`heap_base`, `atop` = number of pre-entries, `sp = fp = 0`, `depth = 0`,
`alloctab[0..atop)` = one pinned live entry per global in `layout.
globals` order then per mapped interface region in `layout.interface_
regions` order, storage of `mem` all zero except global images.

**Locations and the result name.** Locations of a function are numbered
in declaration order: an oracle's `regs`; for an lproc its `params`,
then its **result name** (`(r:reg[8])` declares a location `r` of the
lproc, written like any location and read by `lift.ret`), then its
`regs`. Every location of the oracle and its closure has a global id
(Did bits: index-space order of functions, then declaration order).
`L_f` = all locations of `@f`, m′ = |L_f| (params + 1 + regs for an
lproc); **R_f = 3 + m′** cells; cell width W_cell = max(P, Sc, Did,
W_max) with W_max the widest location width in the closure. A location
of width N exchanged with a cell exchanges the cell's low N bits; the
cell's remaining bits stay clean.

**`w = lift.call @f (a_1..a_m)`.** flag := (depth + 1 > depth_limit) ∨
(sp + R_f > stack_limit), C = `FAULT_BUDGET_DEPTH`, computed first into
`frame.flag`; the elementary sub-operations C1–C5, in this order, run
under ¬flag:

1. **C1 capture**: `disp_i ^= a_i` for i = 1..m (capture slots; every
   `a_i` is read where it is, before any location moves);
2. **C2 push locations**: exchange `L_f` (each padded to one cell) with
   the clean cells `stack[sp+3 .. sp+3+m′)`;
3. **C3 record**: `stack[sp] ^= k+1` (ret index), `stack[sp+1] ^= fp`,
   `stack[sp+2] ^= id(w)` (direct XORs into clean cells);
4. **C4 bind**: `param_i(@f) ^= disp_i` for i = 1..m (the params are among
   L_f and clean after C2);
5. **C5 counters** (assignment): `disp_{m+1} ^= sp`, `disp_{m+2} ^= sp +
   R_f`, `disp_{m+3} ^= depth + 1` (all computed from the old counters),
   then `qexch disp_{m+1} fp`, `qexch disp_{m+2} sp`, `qexch disp_{m+3}
   depth` (now `fp` = old `sp`; the slots hold the old `fp`, `sp`, `depth`).

Successor: the entry label of `@f`. **Inverse** (§3.6 step 4, after the
fault-write undo): C5⁻¹ `qexch disp_{m+3} depth; qexch disp_{m+2} sp;
qexch disp_{m+1} fp` (the old counters are back), then `disp_{m+3} ^=
depth + 1; disp_{m+2} ^= sp + R_f; disp_{m+1} ^= sp` (slots clean); C4⁻¹
`param_i ^= disp_i`; C3⁻¹ `stack[sp+2] ^= id(w); stack[sp+1] ^= fp;
stack[sp] ^= k+1` at the restored `sp`, `fp`; C2⁻¹ exchange `L_f` back
with `stack[sp+3 .. sp+3+m′)`; C1⁻¹ `disp_i ^= a_i` (the `a_i` are
restored by C2⁻¹ even when they are locations of `@f` itself, as in a
recursive call).

**`lift.ret v`** (in an lproc `@f`; flag := (depth = 0), C = `FAULT_UB_
TRAP`; R1–R5 run under ¬flag):

1. **R1 succ**: `frame.succ ^= stack[fp]` (ret index);
2. **R2 capture result**: `disp_1 ^= v` (delivery slot);
3. **R3 pop locations**: exchange `L_f` with `stack[fp+3 .. fp+3+m′)` (the
   locations regain the caller's view; the cells hold the callee's final
   values as history);
4. **R4 deliver**: for every location ℓ of the closure, under `(stack[fp+2]
   == id(ℓ))`: `qexch disp_1 ℓ` (exactly one condition holds; the slot
   retains ℓ's old value);
5. **R5 counters** (assignment): `disp_2 ^= stack[fp+1]`, `disp_3 ^= depth
   − 1`, then `qexch disp_2 fp`, `qexch disp_3 depth`.

Successor: `frame.succ`. **Inverse**: R5⁻¹ `qexch disp_3 depth; qexch
disp_2 fp` (the callee `fp` is back), then `disp_3 ^= depth − 1; disp_2 ^=
stack[fp+1]` (slots clean); R4⁻¹ the same conditional exchanges, their
condition and addresses at the restored `fp` (ℓ regains its old value,
`disp_1` again holds v); R3⁻¹ exchange `L_f` back with `stack[fp+3 ..
fp+3+m′)` (the callee's values are back); R2⁻¹ `disp_1 ^= v`; R1⁻¹ `frame.
succ ^= stack[fp]` (this is the generic `succ` uncompute that ends §3.6
step 4).

The stack is monotonic (`sp` only grows; records are history). Callee
rows are charged to the caller's budget; `lift.call` and `lift.ret` are
one step each. Executors MAY inline extensionally. Suite B runs one
forward `lift.call` step and one forward `lift.ret` step of a recursive
call, each followed by its inverse, and asserts that the complete
pre-step tuple is restored and every frame field is clean.

## 4. Instruction set

### 4.1 Classical control (CC, R)

| Instruction | Form | Semantics |
|---|---|---|
| `const` | `r = const.iN c` | |
| `add sub mul and or xor shl lshr ashr` | `r = op a b` | wrap; shift ≥ N → 0 |
| `udiv urem sdiv srem` | `r = op a b` | divisor 0 or signed MIN/−1: CC trap; R fault record |
| `icmp` | `r = icmp.{eq,ne,ult,ule,slt,sle} a b` | |
| `select` | `r = select p a b` | |
| `zext sext trunc` | `r = op.iM a` | |
| `ptrtoint` / `inttoptr` | `r = ptrtoint.iM p` / `p = inttoptr a` | zero-extend/truncate to M / to ptr_width |
| `load` / `store` | `r = load.iN addr` / `store.iN addr v` | N/8 bytes little-endian, unaligned; outside every live allocation: CC trap / R fault record |
| `alloc` / `free` | `p = alloc n` / `free p` | §7.1 |
| `br` | `br ^b(args)` / `br p ^b1(args) ^b2(args)` | parallel block-parameter assignment |
| `call` / `ret` | `results = call @f args` / `ret vals` | |
| `uncall` | `uncall @f (args) (results)` | **segment uncall** (§7.4): the most recent completed call segment of the history MUST be a call of `@f` whose recorded boundary argument and result values equal the current operand values, and every frame after it MUST be pure (§7.4); otherwise CC trap / R fault `FAULT_UB_TRAP` with no state change. The segment's frames are reversed in LIFO order (nested segments included) and marked reversed; the `uncall` itself pushes a frame naming the segment |
| `trap` | `trap` | CC trap; R fault record |
| `qreg.new/free/slice/concat` | §3.3 | CC only |
| `measure` | `r = measure q` | CC only; Born rule (§14.2); consumes q |
| `effect` | `effect dev.op args` | R only (§7.3); results are written to memory operands |
| `hostcall` | `rlen = hostcall service ptr len` | CC only (§10) |

### 4.2 Lifted rows (oracle bodies and lprocs)

Columns: **Class**, **Reads**, **Writes / slots** (A: displaced values in
slot order; D: the permutation), **Flag / fault** (C = code), **Succ**.
Every row is one budget step; `k` is its own index.

| Row | Form | Class | Reads | Writes / slots | Flag / fault | Succ |
|---|---|---|---|---|---|---|
| `lift.const` | `w = lift.const.iN c` | A | – | w | – | k+1 |
| `lift.binop` | `w = lift.{add,…,ashr} a b` | A | a, b | w | – | k+1 |
| `lift.div` | `w = lift.{udiv,urem,sdiv,srem} a b` | A | a, b | w (under ¬flag) | flag = (b=0) ∨ (signed ∧ a=MIN ∧ b=−1); C = `FAULT_UB_DIV0` / `FAULT_UB_SDIV_OVERFLOW` | ¬flag: k+1; flag: HALT |
| `lift.icmp` | `w = lift.icmp.{pred} a b` | A | a, b | w:reg[1] | – | k+1 |
| `lift.select` | `w = lift.select p a b` | A | p, a, b | w | – | k+1 |
| `lift.cast` | `w = lift.{zext,sext,trunc}.iM a` | A | a | w | – | k+1 |
| `lift.mov` | `w = lift.mov a` | A | a | w | – | k+1 |
| `lift.parmov` | `(w_1..w_m) = lift.parmov (a_1..a_m)` | A | a_i | w_1..w_m (m slots) | – | k+1 |
| `lift.label` | `w = lift.label ^b` | A | – | w | – | k+1 |
| `lift.addr` | `w = lift.addr @g` | A | – | w = layout base of global or mapped region g | – | k+1 |
| `lift.boundscheck` | `lift.boundscheck p n` | D | p, alloctab | – | flag = ¬inrange(p, n); C = `FAULT_UB_MEMFAULT` | ¬flag: k+1; flag: HALT |
| `lift.load` | `w = lift.load.iN a` | A | the N/8 cells at a.. (§7.2) | w (under ¬flag) | flag = ¬inrange(a, N/8); C = `FAULT_UB_MEMFAULT` | ¬flag: k+1; flag: HALT |
| `lift.store` | `lift.store.iN a v` | A | v | the N/8 cells at a.. (under ¬flag; one slot of N bits) | flag = ¬inrange(a, N/8); C = `FAULT_UB_MEMFAULT` | ¬flag: k+1; flag: HALT |
| `lift.alloc` | `w = lift.alloc n` | A | n, heap_used, atop | under ¬flag, slots in this order: w ← heap_base + heap_used; alloctab[atop] ← (heap_base + heap_used, n, 1, 0); heap_used ← heap_used + max(n,1); atop ← atop + 1 (4 slots, all computed from the old state, then exchanged in this order, `alloctab[atop]` at the old `atop`). **Inverse exchanges**: atop, heap_used, alloctab[atop] (at the restored `atop`), w; then clear the four slots | flag = (heap_used + max(n,1) > heap_limit) ∨ (atop ≥ 2^A_tab); C = `FAULT_BUDGET_HEAP` | ¬flag: k+1; flag: HALT |
| `lift.free` | `lift.free p` | D | p, alloctab | match_i = (i < atop) ∧ (base_i = p) into scratch; under ¬flag: live_i ^= match_i for all i; scratch uncomputed | flag = ¬∃ i: match_i ∧ live_i ∧ ¬pinned_i; C = `FAULT_UB_MEMFAULT` | ¬flag: k+1; flag: HALT |
| `lift.faultif` | `lift.faultif p code` | D | p | – | flag = p; C = code | ¬flag: k+1; flag: HALT |
| `lift.call` | `w = lift.call @f (a_1..a_m)` | A+D | §3.7 | §3.7 (slots: m capture slots `disp_1..disp_m`, then assignment slots for fp, sp, depth) | flag per §3.7; C = `FAULT_BUDGET_DEPTH` | ¬flag: entry of @f; flag: HALT |
| `lift.ret` | `lift.ret v` | A+D | §3.7 | §3.7 (slots: the delivery slot `disp_1`, then assignment slots for fp, depth) | flag = (depth = 0); C = `FAULT_UB_TRAP` | ¬flag: `succ`; flag: HALT |
| `lift.retval` | `lift.retval v` | D | v | result_val ^= v | – | HALT |
| `lift.oracle_call` | `lift.oracle_call @o tk (ins..) tgt fr (mem..) (args..)` | D | ins, tgt, fr, mem | tgt ^= payload; fr ^= code (callee contract) | – | k+1 |
| `lift.oracle_uncall` | same form | D | as above | the matched inverse (§5.5): the identical permutation | – | k+1 |
| `lift.perm_call` | `lift.perm_call @a (mut..) (ins..) (mem..) (args..)` | D | ins, mut, mem | mut ← P(mut, ins, mem); inverse = `adj` of @a | – | k+1 |
| `qjump` | `qjump ^b` | D | – | – | – | ^b |
| `qbranch` | `qbranch p ^b1 ^b2` | D | p | – | – | p: ^b1; ¬p: ^b2 |
| `qjumpr` | `qjumpr a` | D | a | succ ← a | flag = (a < first_f) ∨ (a ≥ first_f + n_f), where `[first_f, first_f + n_f)` are the indices of the containing function's blocks (contiguous, §3.6); C = `FAULT_UB_TRAP` | ¬flag: `succ`; flag: HALT |
| `fault` | `fault C` | D | – | code ^= C; faulted ^= 1 | – | HALT |

**`inrange(p, n)`** = ∃ i < atop: live_i ∧ base_i ≤ p ∧ p + n ≤ base_i +
size_i, every comparison computed at width max(ptr_width, width(n)) + 1
(no wrap; §3.3); `lift.load`/`lift.store` carry this check
**inherently** on their own address and length, so the reference
function is total for every well-formed body; `lift.boundscheck` is an
explicit assertion row the dialect emits before each access (after it
the access's own flag is never set, so dialect-produced bodies' step
counts are unchanged). Rules: `lift.retval` is ill-formed in an lproc;
`lift.ret` is ill-formed outside lprocs; `tk` is a classical argument of
the calling oracle. `lift.oracle_call`/`uncall`/`perm_call` carry the
complete callee interface; `mem` operands name the caller's mapped
interface regions. `lift.addr @g` names a global anywhere; it names an
interface region **only in the body of the oracle that declares it**
(lprocs are shared between oracles and receive region bases as
parameters, as in §16.3 example 2). Label values obtained by `lift.
label` denote blocks of the containing function; `qjumpr` to any other
index faults, so control never leaves a function except through `lift.
call`/`lift.ret`.

**Reference body and binding.** Every oracle carries its **reference
body**: the stream the dialect's versioned mapping produced from the
materialised source; hashed into `interface_hash` (§9.2). F_B and the
budget unit are defined solely by the reference interpreter (§14.1) on
it; the object holds only the reference body; every executor
optimisation is extensionally equal on D (T6).

### 4.3 Allocation

| Instruction | Form | Rules |
|---|---|---|
| `qalloc` | `w = qalloc cls n` | n clean wires of class `cls` or `any`; unconditional |
| `qborrow` | `w = qborrow cls n` | n wires in unknown state; usable only inside a borrow frame (§5.6) |
| `qfree` | `qfree w` | release a `qalloc`ed bundle clean on every basis configuration |
| `qreturn` | `qreturn w` | matched inverse of `qborrow` after its frame |

### 4.4 Gates

```
  x = [[0,1],[1,0]]   h = (1/√2)[[1,1],[1,-1]]   s = diag(1,i)   sdg = diag(1,-i)
  t = diag(1,e^{iπ/4})  tdg = diag(1,e^{-iπ/4})   cz = diag(1,1,1,-1)
  rx(θ) = exp(-iθX/2)   ry(θ) = exp(-iθY/2)   rz(θ) = exp(-iθZ/2) = diag(e^{-iθ/2}, e^{iθ/2})
  cx, ccx, mcx(k): X on the target iff all controls are |1⟩ (exact, no phase)    swap: exact exchange
```

Forms: `x a`, `cx c t`, `ccx c1 c2 t`, `mcx (c_1..c_k) t`, `swap a b`,
`h a`, `s a`, `sdg a`, `t a`, `tdg a`, `cz a b`, `rx θ a`, `ry θ a`, `rz θ
a`; all controlled on the active predicate. **Realisation**: permutation
status is a property of the realised unitary at the gate boundary;
conformant iff equal to the specified unitary exactly including global
phase (ε = 0) or within declared ε in operator norm. **Oracles and
permutation actions require ε = 0** for every gate; actions MAY use ε > 0
(§12). A relative-phase Toffoli is never a conformant `ccx`.

### 4.5 Copy, XOR, exchange, in-place

| Instruction | Form | Semantics |
|---|---|---|
| `qcopy` | `d = qcopy s` | d allocated clean; `cx s[i] d[i]` under the predicate |
| `quncopy` | `quncopy s d` | `cx s[i] d[i]` under the predicate; `qfree d` |
| `qxor` | `qxor s t` | `cx s[i] t[i]` |
| `qexch` | `qexch a b` | `swap a[i] b[i]` |
| `qinplace` | `qinplace @g @ginv tk x` | `@g`, `@ginv` total permutation oracles on the n-bit encoding with certificates that under `tk` the fault code is `FAULT_NONE` on every input and `g∘ginv = ginv∘g = id`. Sem: `t = qalloc any n; f = qalloc any F; oracle_call @g tk (x) t f; qexch x t; oracle_call @ginv tk (x) t f; qfree t; qfree f` |

### 4.6 Quantum memory, predication, structure

| Instruction | Form | Rules |
|---|---|---|
| `qregion` | `qregion name A W [@image]` | function-local region of 2^A cells of `wire[W]`, created at function entry (unconditional allocation, X gates from the data image, default zero), back at its image before exit, image gates reversed, cells released clean; scope is the function. `@image` is a `data` symbol reference (size 2^A·W/8 bytes, cell i = bits [iW, (i+1)W) of the little-endian image) and is part of the function's identity (§9.2) |
| `qload` | `d = qload name a` | d clean; for each cell i: under `a == i`, `qxor cell_i d` |
| `qunload` | `qunload name a d` | inverse |
| `qstore` | `qstore name a v` | for each i: under `a == i`, `qxor v cell_i` |
| `qexchm` | `qexchm name a v` | for each i: under `a == i`, `qexch v cell_i` |
| `qpred`/`qunpred` | | §3.5 |
| `qif` | `qif w { then } { else }` | `qpred w; then; qunpred w; x w; qpred w; else; qunpred w; x w` |
| `qloop` | `qloop n { body }` | body n times |
| `qloop … while` | `qloop n while cond { body }` | `cond : wire[n]` permutation-provenance wires computed before the loop from wires the body does not modify; flags `c_1..c_n` clean; `cx cond[0] c_1`; iteration i under `qpred c_i`; after iteration i < n: `ccx c_i cond[i] c_{i+1}`; flags uncomputed in reverse and freed |

### 4.7 Region calls (structured code, CC and R)

`oracle_call @o tk (ins..) tgt fr (mem..) (args..)`; `action_call @a
(mut..) (ins..) (mem..) (args..)`; `adj action_call …`; `adj oracle_call
…` ≡ `oracle_call …`; `ctl w <call>` ≡ the call under `qpred w`. In CC
and R, wire and region slots are filled by `qreg` operands per §3.3
(§3.1: R functions call Q regions exactly as CC does; the call is one
frame of the R history, §7.4).

### 4.8 Opcode table (tier, operands, result)

| Opcode family | Tiers | Operands | Result |
|---|---|---|---|
| `const.iN` | CC R Q(lift) | literal | iN / reg[N] |
| `add..ashr`, `udiv..srem`, `icmp.*`, `select` | CC R Q(lift) | values of equal width (select: i1, a, b) | same width (icmp: i1) |
| `zext.iM sext.iM trunc.iM` | CC R Q(lift) | value | iM |
| `ptrtoint.iM`, `inttoptr` | CC R | ptr / integer | iM / ptr |
| `load.iN store.iN` | CC R | ptr [, value] | iN / – |
| `alloc free` | CC R | iN / ptr | ptr / – |
| `br call ret uncall trap` | CC R | per §4.1 | – |
| `qreg.new qreg.free qreg.slice qreg.concat measure` | CC | per §3.3 | qreg / – / qreg / qreg / iN |
| `effect` | R | device op, ptr/len operands | – |
| `hostcall` | CC | service literal, ptr, len | iN (rlen, width ptr_width) |
| `lift.*`, `qjump qbranch qjumpr fault` | Q (oracle bodies, lprocs) | locations, pseudo-locations, labels, literals | locations |
| gates, `qalloc qborrow qfree qreturn qcopy quncopy qxor qexch qinplace qregion qload qunload qstore qexchm qpred qunpred qif qloop` | Q (actions) | wires, bundles, regions, literals | wires / – |
| `oracle_call action_call adj ctl` | Q, CC, R | per §4.7 | – |

## 5. Regions

### 5.1 Interfaces and common well-formedness

Signatures list roles: `oracle @o (in a: wire[8]) (tgt t: wire[8]) (fault
f: wire[4]) (mem db: region[10,8] in) (args n: i64)`. **Interface
regions** are caller-owned, passed by name, role `in` (returned to entry
contents on every basis configuration) or `mut` (actions only). A region
MUST NOT contain `measure effect br call uncall trap hostcall qreg.*` or
classical memory instructions, nor lifted rows outside oracle bodies.
Predicate stack empty at entry and exit. Every `qalloc` matched by a
`qfree` of a clean bundle, every `qborrow` by a `qreturn` after its
frame, every local `qregion` restored, by **explicit cleanup
instructions**; the schedule chooses only realisations. **`in` wires in
actions** appear only as controls, as targets of diagonal gates, as
`qcopy`/`qxor` sources, or as `in` arguments of calls. Action call
graphs are acyclic; recursion exists only through `lift.call`.

### 5.2 Lifted oracle

**Body**: lifted and control rows over its locations and lproc closure;
**exact-permutation only** (ε = 0 everywhere, transitively).

**Contract** on every x ∈ D: `ins` unchanged; `tgt` final = initial ⊕
payload(F_B(x)); `fr` final = initial ⊕ code(F_B(x)); `in` regions
unchanged; borrowed bundles returned (§5.6); workspace, locations, local
regions, step state clean / at image. **F_B(x)** = `(f(x), 0)` if the
reference interpreter reaches `lift.retval` within B steps without a
fault (f(x) = the XOR-accumulated `result_val`), else `(0, code)` with
`code` the first fault in sequential order, or `FAULT_BUDGET_STEPS` if
not halted after B steps. The oracle is an **involution** on `(ins, tgt,
fr)` and its own adjoint.

**Construction**: (1) allocate step state (`result_val` included),
locations, local regions, `alloctab` pre-entries, B frames; (2) run B
forward steps; (3) **commit**: `at_HALT = (pc == HALT)`; under `at_HALT ∧
¬faulted`: `qxor result_val tgt`; under `faulted`: `qxor code fr`; under
`¬at_HALT`: XOR the constant `FAULT_BUDGET_STEPS` into `fr`; uncompute
`at_HALT`; (4) **prefix reversal**: run the inverse step for t = B..1,
then release (1). The commit writes persist.

**Domain D**: every value of each `ins`, of `tgt`, of `fr`, of every cell
of every `in` region, of every borrowed bundle; `qalloc`ed wires at 0;
local regions at image.

### 5.3 Quantum action

**Semantics.** The body denotes a unitary U on mut ⊗ ins ⊗ mem_mut ⊗
(borrowed), block-diagonal in the computational basis of `ins` and of
`in`-region cells, identity on borrowed and external reference systems
(§5.6), workspace returned clean. No fault outcome. Coherent internal
control yields the padded unitary under declared bounds, part of the
action's identity. **Permutation action**: realised unitary a
permutation matrix (ε = 0, permutation gates only, transitively).

**Body**: gates; `qcopy quncopy qxor qexch qinplace`; `qload qunload
qstore qexchm`; `qpred qunpred qif qloop`; `oracle_call action_call`;
`qalloc qborrow qfree qreturn`; `qregion`.

**Bounds.** The `bounds { … }` list of an action's `regs` line and the
`bounds` array of its signature hold, in text order, the trip count `n`
of every `qloop` and `qloop … while` in the body (nested loops
included, outer before inner); the list MUST equal the body (suite F)
and is empty for a body without loops. It is part of the action's
identity because the padded unitary of coherent internal control
depends on it.

**Adjoint table** (reverse order, instruction replaced, versions
renumbered):

```
  rx/ry/rz(θ) ↦ (−θ)   s ↔ sdg   t ↔ tdg   x cx ccx mcx swap h cz: self-adjoint
  qalloc ↔ qfree   qborrow ↔ qreturn   qregion creation ↔ release   qcopy ↔ quncopy   qload ↔ qunload
  qxor qexch qstore qexchm: self-adjoint   qinplace @g @ginv ↦ qinplace @ginv @g   oracle_call ↦ oracle_call
  action_call @b ↦ adj action_call @b   qpred/qunpred pairs reversed as a whole
  qif w {A}{B} ↦ qif w {adj A}{adj B}   qloop n {A} ↦ qloop n {adj A}
  qloop n while cond {A} ↦ flags computed forward as §4.6; adj A for i = n..1 under c_i; flags uncomputed
```

**Control.** `ctl w @a` is controlled-U: workspace, regions and flags
allocated unconditionally; every gate of the body and its cleanup runs
under `w` in addition to the active predicate.

### 5.4 Budgets and fault codes

Budget = (B, heap_limit, stack_limit, depth_limit), classical. `bennett_
budget` validates: `heap_limit ≤ layout.heap_limit_max`, `stack_limit ≤
2^S_cells`, `depth_limit < 2^Dc − 1`; for a memoryless object (§7.2)
`heap_limit = stack_limit = depth_limit = 0`. B is enforced by running
exactly B steps; heap, stack and depth are wire counters.

```
  0 FAULT_NONE            4 FAULT_UB_TRAP            8 FAULT_EFFECT_UNMODELLED
  1 FAULT_BUDGET_STEPS    5 FAULT_UB_DIV0            9 FAULT_CALLEE
  2 FAULT_BUDGET_HEAP     6 FAULT_UB_SDIV_OVERFLOW  10 FAULT_ENTROPY_EXHAUSTED (R only)
  3 FAULT_BUDGET_DEPTH    7 FAULT_UB_MEMFAULT
```

F ≥ 4.

### 5.5 Nesting and matched cleanup

A `lift.oracle_call` supplies a caller location `fr'`, clean when
computing a fresh outcome. No automatic propagation: the dialect emits `p
= lift.icmp.ne fr' zero; lift.faultif p FAULT_CALLEE` (with `zero` a
`lift.const` location) where the source requires it. To clear `fr'`, the
producer emits `lift.oracle_uncall @o` with the same token, callee, `ins`
and `mem` values (no intervening row writes those locations or cells:
suite F) and the successor versions of `tgt` and `fr'`; the pair shares a
dynamic invocation identity. Alternatively `fr'` is retained until the
prefix reversal.

### 5.6 Borrowed systems and borrow frames

**Requirement.** A region's completed operation equals its declared
operation ⊗ identity on every borrowed bundle and on any external system
entangled with it.

**Rule (suite F).** Borrowed wires (set B) are touched (as control or
target) only inside **borrow frames**: maximal contiguous permutation-
only subcircuits from the first to the last instruction touching B. The
frame's realised permutation P_F on its wires MUST factor as `P_F = P' ⊗
I_B`, established by a T3 claim over the frame's full domain
(exhaustive, or a library certificate, §12 `borrow_frames`) or
**structurally by the translation lemma**: the frame is `V; W; V⁻¹; W`
where

- (i) every gate of V is an X-family flip (`x cx ccx mcx`) whose **target
  is in B** and whose **controls are all in a set X with X ∩ B = ∅**; V
  touches no other wire; hence V maps b ↦ b ⊕ v(X);
- (ii) every gate of W is an X-family flip whose **target is outside X,
  outside B, and outside the set of all controls of W** (as sets, over
  the whole of W), and W writes no wire of X;
- (iii) every gate of W has **at most one control in B**;
- (iv) V⁻¹ is the exact reverse sequence of V; no `swap` appears in the
  frame.

Then W's effect is affine in b, the net map is t ⊕= Σ_g c_g(Y)·v_{j(g)}(X),
independent of b, and b is restored (the dirty-ancilla MCX pattern).
Suite F contains the negative tests `cx b y; cx y z; cx b y` (V;W;V⁻¹),
`V = cx b2 b1, W = cx b1 t` (b2 ∈ B, violates X ∩ B = ∅), `V = cx b x`
(target outside B), and `W = swap y z; cx b y` (swap excluded). Oracles
are one frame verified by their own T3 claim over D.

### 5.7 Executor transformations

Inlining, structure recovery, dispatch re-indexing and simplification
MUST produce on every x ∈ D the same final interface tuple as §5.2's
construction on the reference body (T6).

## 6. Uncomputation validity (static discipline)

### 6.1 Provenance and transfer

Every workspace bundle version, location version and cell version has
provenance `perm` (computed by permutation gates from its **dependency
set** S of versions) or `other`. Cell versions `(region, i, v)` advance on
every write. Π is the effective control context at the instruction.

| Instruction | Effect |
|---|---|
| `qalloc` | perm, S = ∅ |
| `d = qcopy s` | d: perm, S = {s} ∪ Π |
| `d = qload r a` | d: perm, S = {a} ∪ cells(r) ∪ Π |
| `qxor s t` | t: perm with S_t ∪ S_s ∪ Π if both perm, else other |
| `qexch a b` | each output: perm with S_a ∪ S_b ∪ Π if both perm, else other |
| `qstore r a v` | each cell (r,i): version advances; perm with S_cell ∪ S_v ∪ {a} ∪ Π if both perm, else other |
| `qexchm r a v` | v and every cell: perm with S_v ∪ ⋃S_cells ∪ {a} ∪ Π if all perm, else other; cell versions advance |
| permutation gate, controls C, target t | t: perm with S_t ∪ C ∪ ⋃S_c ∪ Π iff t was perm, else other |
| diagonal gate on u | unchanged |
| non-diagonal gate on u | u: other; closes the window of every value whose S contains u |
| `oracle_call @o (ins) tgt fr (mem)` | tgt, fr: perm with S = ins ∪ {tgt, fr} ∪ cells(every region passed) ∪ Π; `in` regions unchanged |
| `lift.perm_call` / permutation `action_call` | each mut: perm with S = mut ∪ ins ∪ cells(regions passed) ∪ Π; `mut`-region cells advance with the same S |
| non-permutation `action_call` | every mut and every `mut`-region cell: other |
| `qinplace @g @ginv x` | x: perm with S_x ∪ Π |
| lifted rows | each written location/cell: perm with the union of its read operands' sets ∪ Π; written cells' versions advance |

### 6.2 Window and obligations

A perm value g with set S is **in its window** from its computation
until the first of: a non-diagonal gate on a wire in S or in g; a version
advance of a cell in S; a non-permutation action call touching a wire in
S; a permutation change to a wire in S not undone before g's cleanup.
Each cleanup is bound to its exact computing sequence and requires the
versions that sequence read to be current. Every perm value MUST be
cleaned within its window and before its region exits; otherwise the
region is **ill-formed** (closed-window measurement-based cleanup is not
admitted). `other` values are released only by the adjoint of the
sequence that produced them.

### 6.3 T5

Cleaning g within its window returns g's wires to |0⟩ and factorises
them from the remaining state; diagonal uses of g or of its dependencies
have applied the corresponding diagonal phases to the remainder, which
is part of the program's declared semantics.

### 6.4 Effective control and cleanup realisations

Every cleanup in this version is **unitary**: realisation `reverse`
(the adjoint of g's exact computing sequence, §6.2) or `recompute`
(legal for `perm` values only: recompute g into a fresh clean bundle by
the same sequence, `qxor` it into g's wires, uncompute the fresh bundle
by the adjoint). **Measurement-based cleanup is not admitted in sched/
cert 0.8**: a schedule naming any other realisation is invalid, the
target capability `mbu` is reserved and MUST be `false`, and no cleanup
produces a `channel` claim. *(non-normative)* The fixup after an X-basis
measurement of g with outcome m is the phase (−1)^{m·g(x)}, a function
of g's computing sequence and not of the target; its normative form,
its controlled variant and its certificate kind are deferred (§17 item
6; default: unitary cleanup). Schedules and certificate cleanup entries
are keyed by `(region hash, variant, inherited control count)`; a region
reachable under a non-empty control context MUST have a cleanup
schedule for that key.

## 7. Memory and effects

### 7.1 Classical memory (CC, R)

Byte-addressed, little-endian, sparse. `layout` partitions the address
space: a **null region** `[0, null_size)` never allocated (null_size ≥
1); globals at fixed bases with images; the heap `[heap_base, heap_base +
heap_limit_max)`, all disjoint, `heap_base + heap_limit_max ≤ 2^ptr_
width`, and the number of globals ≤ 2^A_tab, all validated at load. `p =
alloc n` **fails before any mutation** when bump + max(n, 1) > heap_base
+ heap_limit_max or the table holds 2^A_tab entries (CC trap / R fault
`FAULT_BUDGET_HEAP`); otherwise it returns the bump pointer, records
`(base, size = n, live = 1, pinned = 0)` and advances by `max(n, 1)`;
globals have pre-entered pinned live entries; an access is valid iff its
whole byte range lies in one live entry; `free p` marks the unique live
entry with base p dead (pinned entries cannot be freed; no such entry:
CC trap / R fault `FAULT_UB_MEMFAULT`); storage is never reclaimed.
Initial state: bump = `heap_base`, table = the pre-entries in layout
order, memory zero except images.

### 7.2 Lifted memory of an oracle

`mem` has 2^H byte cells (H ≤ ptr_width); `alloctab` 2^A_tab entries
`(base, size, live, pinned)`; the stack 2^S_cells cells. The `layout`
fixes `null_size`, each global's base and image, `heap_base`, `heap_
limit_max`, and for each **interface region** of the oracle (W = 8
required) a base address; all ranges disjoint and within `[0, 2^H)`, and
for every oracle the number of pre-entries (globals plus its interface
regions) ≤ 2^A_tab, checked at load. `lift.load`/`lift.store` dispatch
by address range to `mem` or to the mapped interface region (role `in`
preserved by the construction). The low H bits address cells; `inrange`
guarantees the range lies in a live entry, hence within `[0, 2^H)`.

**Memoryless objects.** An object without a `layout` section MUST
contain no lprocs, no `lift.addr lift.boundscheck lift.load lift.store
lift.alloc lift.free lift.call lift.ret` rows, no `mem` interface slots
and no CC/R `alloc free load store`; H = A_tab = S_cells = 0, no `mem`,
`alloctab`, stack or counters are allocated, and `bennett_budget`
requires `heap_limit = stack_limit = depth_limit = 0` (§5.4). Example 1
of §16.3 is memoryless.

### 7.3 Device models and tapes (R)

Every device operation takes classical-memory operands and writes its
results to memory; each `effect` is **atomic**: validated (operands in
range, tape available) before any change, and a failing validation is a
fault record with no partial delta.

| Device | State (initial) | Operations | Failure | Frame records / reversal |
|---|---|---|---|---|
| `console` | byte sequence (empty) | `write(ptr, len)` | – | `len`; pop |
| `clock` | `c: u64` (0) | `read(ptr)`: writes c (8 bytes LE) at ptr, then c += 1 | – | overwritten 8 bytes; c −= 1 |
| `entropy` | position `p` (0) into the entropy tape (§10) | `read(ptr, len)`: copies tape[p..p+len) to ptr; p += len | p + len > length: fault `FAULT_ENTROPY_EXHAUSTED` | overwritten bytes; p −= len |
| `block` | sector map from the `block_image` (else empty), 512-byte sectors; absent sectors read as zero | `read(sector, ptr)`; `write(sector, ptr)` | – | read: overwritten 512 bytes; write: the old sector contents **and a presence bit** (absent sectors are removed again on reversal) |

Each `effect` appends `(dev, op, args)` to the effect tape.

### 7.4 Run history and the dynamic SSA model (CC, R)

The classical environment holds **dynamic instances**: every executed
defining instruction creates a new instance retained in the run history
until reversal; a name denotes its most recent instance. Frames:

| Instruction | Frame |
|---|---|
| any defining instruction | its defined instance |
| `br` | predecessor block, prior block-parameter instances |
| `store` | address, width, overwritten bytes |
| `alloc` | old bump pointer, the table entry written, the zero-filled range |
| `free` | the entry's old live bit |
| `call` | invocation boundary (callee, argument values) |
| `ret` | result values, the callee's activation and the frame link |
| `uncall` | the reversed segment's id (skipped by whole-run reversal, below) |
| `effect` | tape index plus the device-specific record of §7.3 |
| `hostcall` | payload bytes and reply bytes |
| `qreg.*`, `measure` | handle created/freed/consumed and the measured bits |
| `oracle_call` / `action_call` | (region hash, variant, inherited control count, classical args, register ids): reversed by re-application / adjoint, exactly once, by this frame |
| fault record | cause code (§5.4) and location; terminal faulted state, reversed like any prefix |

**Pure frames.** A frame is **pure** iff it belongs to `br` or to a
defining instruction among `const`, the binops, `udiv..srem`, `icmp`,
`select`, `zext sext trunc`, `ptrtoint inttoptr`, `load`: it changes
only the set of instances. Every other frame (`store alloc free call ret
uncall trap effect hostcall qreg.* measure`, region calls, fault
records) is impure.

**History traversal** (the one reversal procedure, used by segment
`uncall` and by whole-run reversal). A range of frames is **reversed**
by visiting its frames in LIFO order; a frame already marked reversed
and an `uncall` frame are **skipped**; every other frame is undone by
its row of the table above and then marked reversed. Reversed frames
stay in the history, marked, and are never undone again (a reversed
segment's `uncall` marker is retired with it).

**Segment uncall** (`uncall @f (args) (results)`). Let S be the most
recent completed call segment of the history (a `call` frame, its
matching `ret` frame and every frame between them). The `uncall` is
legal iff S is a call of `@f`, S's recorded boundary argument and result
values equal the operand values, **every frame after S is pure**, and S
contains, at any nesting depth, **no `measure` frame** and no `qreg.
free` frame whose cleanliness was not verified (hardware, §17 item 14);
otherwise it is a CC trap / R fault `FAULT_UB_TRAP` and changes nothing.
Execution reverses S by the history traversal (nested segments are
undone; nested segments already cancelled by an inner `uncall`, and that
inner `uncall` frame, are skipped), and pushes an `uncall` frame naming
S. The instances defined inside S no longer exist; using such a name
before it is redefined is a CC trap / R fault `FAULT_UB_TRAP`.
**Whole-run reversal** (§10) is the history traversal over the whole
history: S's effects on memory, the allocation table, devices and
handles were undone by the `uncall`, and the frames between S and the
`uncall` are pure, so at the `uncall` frame every component except the
retained instances already equals its value before S. T4 is stated over
these frames. *(non-normative)* S is never re-executed and never redone;
the compute–copy–`uncall` idiom derives what it keeps through pure
instructions before the `uncall`. Suite A contains: `f` calls `g`,
uncalls `g`, returns; `g` performs one `clock.read`; `call f; uncall f`
leaves the clock at its entry value; and `uncall` of a segment that
measured is a trap.

## 8. Target descriptions (target 0.8)

### 8.1 Format and expressions

A target is a JSON document in RFC 8785 canonical form; `target_hash` =
SHA-256 of those bytes; numbers are exact rationals from their decimal
text. Cost expressions are a closed JSON AST:

```
  expr := number | {"var": v} | {"op": o, "args": [expr, …]} | {"table": name, "index": "k" | "eps_decade"}
  v    := "k" | "c" | "eps" | "a" | "w" | "i" | "theta"
  o    := "+" (2) | "-" (2) | "*" (2) | "/" (2) | "max" (2) | "min" (2) | "ceil" (1) | "log2inv_eps" (0)
```

`log2inv_eps` = the exact integer min{ j ≥ 0 : eps · 2^j ≥ 1 } for 0 <
eps ≤ 1; eps outside (0, 1] is a load-time error; an entry with
`epsilon` 0 MUST NOT reference `eps` or `log2inv_eps`. Division by zero
and a table index outside the array are load-time errors. Costs MUST be
nonnegative and finite.

**Variable binding** by evaluation context; referencing a variable that
the context does not bind is a load-time error:

| Context | Bound variables |
|---|---|
| a `gates` entry's `epsilon` and `cost` | `k` = the gate's own control count; `c` = its total control count (`k` + effective control count, §8.3); `eps` = the operation's `epsilon_share` from the schedule (§11) |
| a scheme's `ancillae.count`, template wire subscripts and `repeat` bounds | `k`, `c` as above; `i` inside a `repeat`; `theta` for a parametric scheme |
| a template gate's `params` | `theta`, `i` |
| `qram` costs | `a` = the region's address width A; `w` = its cell width W; `c` |
| a frame descriptor (§9.4) | `c` only |
| `classes.*`, `capabilities.*`, `resources.*.rate` | none (numbers only) |

**Requested versus achieved accuracy.** `eps` is the `epsilon_share`
the schedule assigns to the operation (§11; the default share is the
region's `epsilon` divided by its number of ε > 0 operations). A `gates`
entry whose `epsilon` expression evaluates to a value > `eps` does not
match the operation and matching continues with the next entry; the
error charged to a matched operation is the entry's evaluated `epsilon`;
an entry with `epsilon` 0 is exact and matches every `eps`.

### 8.2 Resources, aggregation, timing

```
  "resources": { "<name>": { "kind": "count"|"time"|"occupancy"|"peak", "unit": "<string>", "rate"?: { "<cls>": n } } }
```

Mandatory: `qubit_second` (occupancy, per class), `time`, `peak_qubits`
(peak, per class). Aggregation from the **scheduled event list** (every
**leaf event** — a native gate after scheme expansion, a classical step,
an effect — with its start time and duration, every wire with its live
interval): `count` sums the per-event costs, each leaf exactly once (a
scheme contributes only its expanded template, never a cost of its own);
`time` is the makespan; `occupancy` integrates, per class, the number of
live wires times the class rate over time (a class absent from `rate`
has rate 1); `peak` is the maximum over time of the number of
concurrently live wires per class (concurrent demands sum). Classical
instructions and effects take `classical_step_time`. Sequential in
program order unless the schedule assigns start times; a gate occupies
its wires for its `time`; gates on disjoint wires MAY overlap unless
`max_parallel` or a topology is declared; all-to-all over logical wires.
Interface wires are charged to the caller for the call's duration;
borrowed wires to the borrower at `dirty_rate`, replacing the owner's
charge.

### 8.3 Classes, gates, schemes, capabilities

```
  "ptr_widths_supported": [32, 64],
  "classes": { "<cls>": { "qubit_second": n, "dirty_rate": n, "capacity": n | "unbounded" } },
  "gates":   [ { "op": "<gate>", "classes": ["<cls>"|"*", …], "controls": {"min": n, "max": n | "unbounded"},
                 "params": ["theta"]?, "epsilon": expr, "cost": { "<resource>": expr, "time": expr } }, … ],
  "schemes": [ { "name": "<name>", "realises": { "op": "<gate>", "controls": {"min": n, "max": n | "unbounded"}, "params": ["theta"]? },
                 "ancillae": { "count": expr, "state": "clean" | "dirty", "class": "<cls>" },
                 "template": [ { "gate": "<op>", "wires": [ "c[<expr>]" | "t" | "t2" | "a[<expr>]", … ], "params": [expr]?,
                                 "repeat": { "var": "i", "from": expr, "to": expr }? }, … ] }, … ],
                 /* from inclusive, to exclusive; a scheme has no cost or epsilon of its own (§8.2) */
  "qram": null | { "load": { "cost": {…} }, "store": { "cost": {…} }, "exch": { "cost": {…} } },
  "capabilities": { "measurement": {"mid_circuit": bool, "feedforward_latency": n}, "mbu": false,     /* reserved, §6.4 */
                    "max_parallel": n | "unbounded", "max_predicate_depth": n | "unbounded", "classical_step_time": n },
  "objective": { "weighted": { "<resource>": n } } | { "lexicographic": [ "<resource>", … ] },
  "tables": { "<name>": [ n, … ] },
  "imports": { "<model>": { "version": "...", "map": { "<quantity>": ["<resource>", factor] } } }
```

**Matching.** An executed gate with opcode o, operand classes, **total
control count c** (own controls + effective control count) and
parameters matches the first `gates` entry in array order whose `op`,
class pattern and inclusive `controls` range cover it and whose
`epsilon` ≤ `eps` (§8.1); else the first `schemes` entry whose
`realises` covers it; else load-time error. Template wires: `c[e]` the
e-th control (0-based, e an expr over k, c and i) in the operation's
control order (own controls in operand order, then the effective control
context in predicate-stack order, outermost first), `t` the target (`t`
and `t2` the two wires of `swap`/`cz` in operand order), `a[e]` the e-th
ancilla; `params` expressions may use `theta`; `repeat` binds `i` over
[from, to). Every template gate MUST itself match a `gates` entry
(schemes do not nest) and is a leaf event; the scheme's error is the sum
of its template gates' charged errors. Scheme ancillae add to the frame
descriptor. A scheme's correctness is the target author's obligation
(suite E: T3 for permutation schemes, suite D for ε > 0).

### 8.4 Space budget

The capacity constraint is peak live qubits per class.

## 9. Objects, identity, linking, reversible ABI (object 0.8)

### 9.1 Sections and schemas

Order fixed: `symbols imports functions data devices layout schedule
certificate coverage`; each at most once; unknown sections or fields are
errors. Metadata sections are one JCS line each, an object:

```
  symbols:  { "<local index>": { "name", "kind": "cc"|"r"|"oracle"|"action"|"perm_action"|"lproc"|"data", "signature": <sig>, "interface_hash" } }
  imports:  { "<name>": { "signature": <sig>, "pinned_closure_hash"?: hex } }
  devices:  { "models": { "<dev>": { "version": "0.8" } }, "services": { "<reverse-dns id>": { "version": "…" } } }
  layout:   { "ptr_width", "H", "A_tab", "S_cells", "null_size", "heap_base", "heap_limit_max",
              "globals": { "<name>": { "base", "size", "image": "<data name>" } },
              "interface_regions": { "<oracle>": { "<region>": { "base" } } }, "block_image"?: "<data name>" }
  schedule: §11      certificate: §12      coverage: { "entries": [ §13 ] }
  <sig>:    kind "oracle": { "tier":"q", "kind", "in":[w…], "tgt":w, "fault":F, "mem":[{"A","W","role"}], "args":[types], "abi":"0.8" }
            kind "action"/"perm_action": { "tier":"q", "kind", "mut":[w…], "in":[w…], "mem":[…], "args":[types], "bounds":[…], "abi" }
            kind "lproc": { "tier":"q", "kind", "params":[w…], "result":w, "abi" }
            kind "cc"/"r": { "tier", "kind", "params":[types], "results":[types], "abi" }
            kind "data": { "tier":"-", "kind", "size", "abi" }
```

Integers that may exceed 2^53 are decimal strings. `data` lines are
`NAME SP HEX`.

### 9.2 Identity

**Canonical function bytes**: the text from the function's header line
through its last instruction line, lines joined by LF, no trailing LF.
**Semantic envelope** of a symbol (byte-exact; every part ends with LF):

```
  (1) "isa=" <full version string, e.g. 0.8>
  (2) "ptr_width=" INT
  (3) the JCS signature
  (4) the canonical function bytes (with reference tokens replaced, below); for a data symbol: its data line NAME SP HEX
  (5a) for every data entry in the closure set, sorted by name bytewise:        "data " NAME " " HEX
  (5b) for every layout leaf in the closure set, sorted by dotted path bytewise: "layout " <dotted path> " " <JCS value>
  (5c) for an R/CC function, for every device model and service it uses, sorted: "device " <name> " " <JCS entry>
  (6) for every referenced symbol outside the symbol's SCC, in order of first reference: its 64-hex hash
```

**Closure set**, by symbol kind. **Oracle**: **all** `layout` leaves of
the object except `interface_regions` entries of other oracles (every
global's pre-entry affects its allocation faults), its own `interface_
regions.<oracle>.*` leaves, and every data image those leaves name.
**Lproc**: the leaves and images of every global `@g` it names in `lift.
addr`. **Action / permutation action**: no layout leaves; the `@image`
of each `qregion` is an ordinary symbol reference (replaced in part (4),
listed in part (6)). **CC / R function**: all `layout` leaves, every
data image they name, and in (5c) every device model and `hostcall`
service it uses. **Data symbol**: parts (5)–(6) are empty. A layout leaf
is a scalar or an object at the deepest level the schema lists (`globals.
<name>` and `interface_regions.<oracle>.<region>` are leaves; `ptr_
width`, `H`, … are leaves); a scalar's JCS value is its decimal text.
**Globals are data symbols**: every global `g` in `layout.globals` MUST
have `image` = `g` and the object MUST define a `data` symbol named `g`
of that size, so the token `@g` in `lift.addr` is both the global and a
symbol reference (replaced by the data symbol's hash; the global's
`base` and `size` enter through the layout leaf). An `@name` naming an
interface region (in `lift.addr`) is not a symbol reference and is left
unchanged. **Reference replacement**: in parts
(4)–(5) every `@name` symbol-reference token is replaced by `@` followed
by the referenced symbol's 64-hex hash (the symbol's own name in its
header line is a definition, not a reference, and is left unchanged); the **interface hash** uses
interface hashes of defined symbols and `SHA-256(name ‖ 0x00 ‖ JCS
signature)` (hex) for unresolved imports; the **closure hash** uses
closure hashes. **SCCs**: members ordered by name bytewise; every intra-
SCC `@name` token (parts (4)–(5)) is replaced by `@$<decimal index>`;
intra-SCC references contribute no part-(6) line; `scc_hash` = SHA-256
over the concatenation of the members' envelopes in that order; member
hash = SHA-256 over the ASCII bytes of `<scc_hash hex>:<decimal index>`.
**object_hash** = SHA-256 of the canonical object text with the
`schedule`, `certificate` and `coverage` sections deleted together with
the blank line preceding each. `reference_program_hash` = the oracle's
interface hash. `params_hash` = SHA-256 of the JCS array of classical
parameter values; `schedule_hash` = SHA-256 of the schedule's JCS bytes.
**Program-point id** = `(symbol interface hash, block name, instruction
ordinal within the block counting nested lines in text order)`.
Executable certificates and caches bind to **closure hashes** (required,
§12).

### 9.3 Linking

Imports resolve by name + signature (mismatch: link error; pinned hash:
equality required); resolved closure hashes are recorded in the linked
certificate. Equal-closure-hash duplicates deduplicate; unequal under one
name, or conflicting `devices`/`layout`/`data` entries: link error.
Linking = resolution, validation, certificate composition (§12.3),
rebinding to closure hashes.

### 9.4 Reversible ABI

- CC/R calls: classical frame; callee frames follow the call boundary;
  `uncall` reverses segments (§7.4).
- Region calls: interface bundles and regions passed in declared order,
  caller-owned; callee owns its workspace, returns it clean, local regions
  at image, borrowed bundles returned.
- **Frame descriptor** (certificate): interface slots (role, width,
  class), scratch by class and cleanliness **as a function of the
  inherited control count c** (an expression in `c` of §8.1's language),
  retained history (oracles: B × frame width), borrow requirement, scheme
  ancillae. Shared frames only with disjoint live ranges (suite F);
  callees `qborrow` only from the caller's designated idle set.

## 10. Launch ABI (launch 0.8)

**Model.** A run executes a device CC entry; the host passes classical
arguments, register ids and the entropy tape, receives classical
results, fault codes and declared measurements; host services are
reached by `hostcall`. **Positional binding**: argument i of `bennett_
run` binds to parameter i of the entry's signature: `INT(width, bytes)`
to `iN` with width = N (else `E_ARG`), `F64` to `f64`, `QREG` to `qreg[n]`
with the register's n, `TOKEN` to `token`. Arguments and the entropy tape
are **copied** at `bennett_run`; the caller may free its buffers
afterwards. Tokens are scoped to the program and destroyed at unload.
Accessor-returned pointers are valid until the owning object is freed.
`bennett_unload` with a run not CLOSED: `E_INVALID_STATE`.

**Invocation tree.** A run record is a tree (CC segments, R calls, Q
calls); an R call's subtree is owned by its R history; `bennett_reverse`
reverses post-order: CC segments by their run history, R calls by LIFO
reversal of their history (§7.4, reversed segments and `uncall` frames
skipped), top-level Q calls by re-application / adjoint.

**States.** `CREATED → RUNNING → (SUSPENDED ⇄ RUNNING) → (HOST_REQUEST ⇄
RUNNING) → COMPLETED | FAILED`; `COMPLETED → REVERSED`; any of
`COMPLETED/FAILED/REVERSED → CLOSED` (`bennett_run_close` releases the
record; register ids created by the run remain valid unless measured or
freed). A run owns the registers and memory it touches exclusively while
not CLOSED. **Reverse eligibility**: `COMPLETED`; no `measure`; no
register it touched has been prepared, freed, sliced or used by another
run since; else `E_NOT_REVERSIBLE`. `bennett_qreg_prepare` and `bennett_
qreg_free` require a clean register (`E_QREG_NOT_CLEAN` otherwise); there
is no reset and no trace-out: a register in unknown state is released by
a `measure` inside a run, which consumes its handle (§3.3).

**Results.** `bennett_result_get` writes value i and sets `*kind` and
`*width`: `INT` as ⌈N/8⌉ little-endian bytes, `*width` = N; `F64` as the
8 IEEE 754 binary64 little-endian bytes, `*width` = 64; `QREG` and
`TOKEN` as the 8-byte little-endian id, `*width` = 64. A `cap` smaller
than that byte count is `E_ARG` and nothing is written. Fault records
are read by `bennett_result_nfaults` / `bennett_result_fault` (codes of
§5.4, in order of occurrence; a `COMPLETED` run has none, a `FAILED` run
has at least one and exposes no values).

**Waiting.** `bennett_wait` blocks until the run leaves `RUNNING` and
returns `OK` with exactly one outcome: `HOST_REQUEST` (`*request_out`
set, `*result_out` NULL; `bennett_reply` answers it and the run is
`RUNNING` again) or `COMPLETED` / `FAILED` (`*result_out` set, `*request_
out` NULL). Waiting on a `SUSPENDED`, `REVERSED` or `CLOSED` run is `E_
INVALID_STATE`.

**`hostcall`.** `rlen = hostcall service ptr len`: `[ptr, ptr + len)` MUST
lie in one live allocation (else CC trap and no request is made); those
bytes are copied into the request; the run enters `HOST_REQUEST`; the
reply payload is written to `[ptr, ptr + min(len, reply length))` and
`rlen` = the full reply length (so truncation is detectable); the frame
records the request bytes, the overwritten bytes and the reply bytes.
Every `service` is declared in `devices.services`; an undeclared one is
a load error.

**Tape.** `bennett_tape_next` yields each `effect` in tape order; `args`
holds the operation's operands in the order of §7.3, each an unsigned
64-bit little-endian field (pointers zero-extended from `ptr_width`), so
`*alen` = 8 × arity.

```c
/* launch 0.8. All objects opaque. A function that returns an object transfers ownership to the caller,
   released with the matching *_free. Status 0 = BENNETT_OK. */
typedef enum { BENNETT_OK=0, BENNETT_E_VERSION, BENNETT_E_PTR_WIDTH, BENNETT_E_DEVICE_MISSING, BENNETT_E_GATE_UNSUPPORTED,
  BENNETT_E_TARGET, BENNETT_E_BUDGET, BENNETT_E_QREG_NOT_CLEAN, BENNETT_E_INVALID_STATE, BENNETT_E_NOT_REVERSIBLE,
  BENNETT_E_SCHEDULE_INFEASIBLE, BENNETT_E_ARG, BENNETT_E_NOMEM } bennett_status;
typedef struct bennett_program_t bennett_program_t;     typedef struct bennett_args_t bennett_args_t;
typedef struct bennett_result_t bennett_result_t;       typedef struct bennett_request_t bennett_request_t;
typedef struct bennett_estimate_t bennett_estimate_t;   typedef struct bennett_coverage_t bennett_coverage_t;
typedef struct bennett_tape_iter_t bennett_tape_iter_t;
typedef uint64_t bennett_qreg; typedef uint64_t bennett_token; typedef uint64_t bennett_run_id;
typedef enum { BENNETT_ARG_INT, BENNETT_ARG_F64, BENNETT_ARG_QREG, BENNETT_ARG_TOKEN } bennett_arg_kind;

bennett_status bennett_load(const uint8_t* object, size_t len, const uint8_t* target_jcs, size_t tlen, bennett_program_t** out);
bennett_status bennett_unload(bennett_program_t*);
bennett_status bennett_budget(bennett_program_t*, const char* region, uint64_t steps, uint64_t heap, uint64_t stack, uint64_t depth, bennett_token* out);
bennett_status bennett_qreg_new(bennett_program_t*, const char* cls, uint32_t n, bennett_qreg* out);
bennett_status bennett_qreg_prepare(bennett_program_t*, bennett_qreg, const uint8_t* bits, size_t nbits);
bennett_status bennett_qreg_free(bennett_program_t*, bennett_qreg);
bennett_status bennett_args_new(size_t n, bennett_args_t** out);
bennett_status bennett_args_set_int(bennett_args_t*, size_t i, uint32_t width, const uint8_t* le_bytes);
bennett_status bennett_args_set_f64(bennett_args_t*, size_t i, double);
bennett_status bennett_args_set_qreg(bennett_args_t*, size_t i, bennett_qreg);
bennett_status bennett_args_set_token(bennett_args_t*, size_t i, bennett_token);
void           bennett_args_free(bennett_args_t*);
bennett_status bennett_run(bennett_program_t*, const char* cc_entry, const bennett_args_t*, const uint8_t* entropy, size_t entropy_len, bennett_run_id* out);
bennett_status bennett_wait(bennett_program_t*, bennett_run_id, bennett_result_t** result_out, bennett_request_t** request_out);
bennett_status bennett_reply(bennett_program_t*, bennett_run_id, const uint8_t* payload, size_t len);
bennett_status bennett_suspend(bennett_program_t*, bennett_run_id);
bennett_status bennett_resume(bennett_program_t*, bennett_run_id);
bennett_status bennett_reverse(bennett_program_t*, bennett_run_id);
bennett_status bennett_run_close(bennett_program_t*, bennett_run_id);
size_t         bennett_result_nvalues(const bennett_result_t*);
bennett_status bennett_result_get(const bennett_result_t*, size_t i, bennett_arg_kind* kind, uint32_t* width, uint8_t* le_bytes_out, size_t cap);
size_t         bennett_result_nfaults(const bennett_result_t*);   uint64_t bennett_result_fault(const bennett_result_t*, size_t i);
size_t         bennett_result_nmeasurements(const bennett_result_t*);
bennett_status bennett_result_measurement(const bennett_result_t*, size_t i, bennett_qreg* reg, uint8_t* bits_out, size_t cap, size_t* nbits);
uint64_t       bennett_result_tape_length(const bennett_result_t*);   void bennett_result_free(bennett_result_t*);
const char*    bennett_request_service(const bennett_request_t*);
const uint8_t* bennett_request_payload(const bennett_request_t*, size_t* len);   void bennett_request_free(bennett_request_t*);
bennett_status bennett_tape_open(bennett_program_t*, bennett_run_id, bennett_tape_iter_t** out);
bennett_status bennett_tape_next(bennett_tape_iter_t*, const char** dev, const char** op, const uint8_t** args, size_t* alen);
void           bennett_tape_free(bennett_tape_iter_t*);
bennett_status bennett_estimate_run(bennett_program_t*, const char* region, bennett_token, bennett_estimate_t** out);
size_t         bennett_estimate_nresources(const bennett_estimate_t*);
bennett_status bennett_estimate_get(const bennett_estimate_t*, size_t i, const char** name, const char** value_decimal);
const uint8_t* bennett_estimate_certificate(const bennett_estimate_t*, size_t* len);   void bennett_estimate_free(bennett_estimate_t*);
bennett_status bennett_coverage_get(bennett_program_t*, bennett_coverage_t** out);
const uint8_t* bennett_coverage_jcs(const bennett_coverage_t*, size_t* len);   void bennett_coverage_free(bennett_coverage_t*);
```

## 11. Scheduling interface (sched 0.8)

```c
typedef struct bennett_sched_request_t bennett_sched_request_t;   typedef struct bennett_sched_response_t bennett_sched_response_t;
bennett_status bennett_sched_request_new(bennett_sched_request_t** out);
bennett_status bennett_sched_request_set_object(bennett_sched_request_t*, const uint8_t*, size_t);
bennett_status bennett_sched_request_set_target(bennett_sched_request_t*, const uint8_t* jcs, size_t);
bennett_status bennett_sched_request_set_region(bennett_sched_request_t*, const char* closure_hash_hex, const char* variant, uint32_t inherited_controls);
bennett_status bennett_sched_request_set_budget(bennett_sched_request_t*, uint64_t steps, uint64_t heap, uint64_t stack, uint64_t depth);
bennett_status bennett_sched_request_set_params(bennett_sched_request_t*, const uint8_t* params_jcs, size_t);
bennett_status bennett_sched_request_set_accuracy(bennett_sched_request_t*, const char* epsilon_decimal);
bennett_status bennett_sched_request_set_capacity(bennett_sched_request_t*, const char* cls, uint64_t peak_qubits);
void           bennett_sched_request_free(bennett_sched_request_t*);
bennett_status bennett_sched_schedule(const bennett_sched_request_t*, bennett_sched_response_t** out);
typedef enum { BENNETT_SCHED_OK, BENNETT_SCHED_INFEASIBLE, BENNETT_SCHED_UNSUPPORTED } bennett_sched_outcome;
bennett_sched_outcome bennett_sched_response_outcome(const bennett_sched_response_t*);
const char*    bennett_sched_response_reason(const bennett_sched_response_t*);
const uint8_t* bennett_sched_response_schedule(const bennett_sched_response_t*, size_t* len);
const uint8_t* bennett_sched_response_certificate(const bennett_sched_response_t*, size_t* len);
void           bennett_sched_response_free(bennett_sched_response_t*);
```

**Generated operations and the expansion library.** Every row and
instruction expands into **generated operations** (gates, allocations,
releases). Above gate level the order is fixed by §3.6, §4.2, §4.5–§4.6
and §5.2 (dispatch comparators k = 0..n in index order; a row's
sub-operations in listed order; successor XORs; commit; cleanup). Below
that level (the gate decomposition of comparators, adders, multiplexers,
`inrange` scans and their scratch) the expansion is defined by an
**expansion library**: a versioned document, identified in the
schedule's `bindings.expansion` as `{ "name", "version", "hash" }`, that
lists for every row kind and every instruction its generated operations
in order, with their **ordinals**, scratch identities and the subset it
marks removable, and that is extensionally equal to the reference (§5.7,
T6). A consumer that does not implement the bound library rejects the
schedule (`E_SCHEDULE_INFEASIBLE`); two consumers implementing it
execute and charge the same operation set. `bennett-isa-spec` publishes
the reference library `ref` (§17 item 7). §5.7 transformations under a
schedule MUST keep the ordinals of the operations they keep and MAY
remove only operations the library marks removable.

**Schedule document** (JCS):

```
  { "bindings": { "closure_hash", "target_hash", "region", "variant", "inherited_controls", "budget": [B,heap,stack,depth],
                  "params_hash", "epsilon", "expansion": { "name", "version", "hash" }, "scheduler": { "name", "version" } },
    "entries": [ { "path": [ { "symbol": hex, "point": "<block>:<ordinal>", "iteration": [n, …] | "*" }, … ],
                   "step": n | "*",  "phase": "fwd" | "rev" | "*",  "generated": n | "*",
                   "kind": "cleanup" | "gate" | "alloc" | "start",
                   "cleanup": { "realisation": "reverse" | "recompute" },
                   "gate":    { "realisation": "native" | "<scheme name>", "epsilon_share": decimal },
                   "alloc":   { "class": "<cls>" },           /* a concrete class; "any" is not allowed in a schedule */
                   "start":   { "time": decimal } } ] }
```

**Matching.** Every generated operation has an **invocation chain**: the
program points of the region calls, `lift.call`s and `lift.oracle_call`s
that led to it, outermost first, ending in its own point. `path` matches
an operation iff it is a **prefix** of that chain, element by element:
`symbol` and `point` equal, and `iteration` either `*` or equal to the
vector of 0-based dynamic repetition counts of the `qloop`s enclosing
that point (outermost first; its length is the point's loop nesting
depth, `[]` outside every loop). `step` is the forward machine step t ∈
1..B of an oracle-generated operation (`phase: rev` denotes the inverse
of step t; both are per invocation level, so a nested oracle's step is
selected by a path element for the nested call); `generated` is the
ordinal within the row's expansion in the bound library. **Specificity**
is the lexicographic tuple (path length, number of non-`*` iterations,
step non-`*`, phase non-`*`, generated non-`*`); an entry applies to a
generated operation iff all its selectors match; among matching entries
the unique maximal one applies; **two incomparable maximal matching
entries make the schedule invalid** (document order is never
significant). Selectors are resolved independently per `kind`. Defaults
for uncovered operations: `reverse`; `native` if the gate matches a
`gates` entry, else the first matching scheme; class = the first class
declared in the target's `classes` object (JCS order) that has capacity
for it; sequential timing in generated order. **Timing**: a `start` time
MUST be ≥ the end of every operation the operation depends on (data,
wire lifetime, region cell version, effect order); an entry violating
this makes the schedule invalid. **Obligations**: satisfy §6; respect
capacity; report every resource; be reproducible from the request plus
scheduler version. A consumer validates every binding and every path
against the object and executes verbatim or rejects (`E_SCHEDULE_
INFEASIBLE`).

## 12. Certificate (cert 0.8; JCS)

### 12.1 Claims

| kind | payload | checker obligation |
|---|---|---|
| `exhaustive` | `domain` (§12.2); `expected`: `"oracle"` \| `{ "table": [...] }` \| `{ "program": closure_hash }` | re-execute every domain element on the reference interpreter / expected program; compare full tuples |
| `sampled` | `domain`; `sampler`: `{ "algorithm": "xoshiro256**", "seed": [4 decimal strings, not all zero], "count": n }` | replay; **evidence** |
| `structural` | `{ "rule": "translation_lemma" \| "inverse_pair_library" \| "adjoint_table", "subclaims": [indices], "witness": … }`; for `translation_lemma`: `{ "V": [points], "W": [points], "X": [wires], "B": [wires], "frame": [first point, last point] }`; for `inverse_pair_library`: `{ "library_closure_hash", "claim_index" }`; for `adjoint_table`: `{}` | check the rule's side conditions syntactically against the object and the subclaims' results |
| `numerical` | `{ "subject": { "closure_hash", "variant", "inherited_controls", "schedule_hash" }, "metric": "operator_norm", "precision_bits": n, "bound": decimal }` | **checker-computed, for every invocation context of the subject** (below): build the realised unitary U of that invocation (the region's realisation under the root schedule at that path, with its resolved classical arguments, budget, epsilon shares and cleanup choices, and `inherited_controls` control wires prepended) and the reference unitary V (the region's §5.3 semantics with the same arguments, controlled on the same wires) at the subject's signature widths in interval arithmetic at `precision_bits` (basis order = allocation order, controls first), form interval enclosures of `V†U − I` entrywise, derive the operator-norm bound as the Frobenius-norm upper bound in interval arithmetic, and verify it is ≤ `bound`; the claim holds iff it holds for every context |
| `channel` | `{ "subject": as above, "metric": "diamond", "precision_bits", "bound", "dual": [ { "Y": interval Hermitian matrix, "mu": decimal } … ] }` | for every invocation context of the subject, in enumeration order, verify its dual witness for the **diamond-norm SDP** below in interval arithmetic and `mu` ≤ `bound` (one witness per context; too few witnesses: reject) |

**Invocation contexts.** A subject denotes the set of invocations of
the region `closure_hash`, with the given `variant` and `inherited_
controls`, in the root schedule `schedule_hash`: every path of that
schedule's region tree reaching the region, with the classical
arguments, budget, `epsilon_share`s and cleanup realisations resolved
at that path. Contexts are enumerated in path order (the schedule's
`entries` paths sorted bytewise as JCS). Every claim bound and every
`error` entry (§12.3) is a **common upper bound over all contexts** of
its key; the multiplicity composition of §12.3 is sound for that reason.

**Diamond-norm SDP** (Watrous, *Theory of Computing* 5 (2009), §4; the
Hermiticity-preserving simplification). Let Φ = Φ_real − Φ_ref be the
difference of the subject's realised channel and the reference channel
(both on the subject's interface, controls included), d_in = d_out = d
the dimension. The **Choi matrix** is J(Φ) = Σ_{i,j} |i⟩⟨j| ⊗ Φ(|i⟩⟨j|)
(input factor first, output factor second, computational basis in
allocation order, **unnormalised**). The witness is a Hermitian Y of
dimension d² and a decimal mu. The checker accepts iff, with every
matrix entry an interval and every test rigorous (an inconclusive test
rejects): Y − J(Φ) ⪰ 0, Y + J(Φ) ⪰ 0, mu·I − Tr_out(Y) ⪰ 0 (partial trace
over the output factor), and mu ≤ `bound`; then ‖Φ‖◇ ≤ mu (the dual of
Watrous's SDP with Y₀ = Y₁ = Y; this is the diamond norm itself, not
half of it). Encoding: `Y` is a row-major array of entries `[re_lo, re_
hi, im_lo, im_hi]` (decimal strings). **Positivity test.** The checker
proves each of the three matrices **positive definite** by an interval
Cholesky (or Hermitian LDL†) factorisation in which the interval lower
bound of every pivot is strictly positive, and rejects otherwise; no
other test is admitted (nonnegative leading principal minors do not
imply positive semidefiniteness: diag(0, −1)). Producers make witnesses
strictly feasible by replacing Y with Y + δI and mu with mu′ = mu + δ·(d
+ 1) for a small rational δ > 0 (any mu′ > mu + δ·d suffices): then Y ±
J(Φ) ⪰ δI ≻ 0 and, since Tr_out(Y + δI) = Tr_out(Y) + δ·d·I, mu′·I −
Tr_out(Y + δI) ⪰ δI ≻ 0; ‖Φ‖◇ ≤ mu′, which MUST be ≤ `bound`. **Interval
arithmetic** at `precision_bits`
means every operation rounds outward to `precision_bits`-bit binary
rationals; transcendental entries (`rx ry rz`) are enclosed by a Taylor
series with the Lagrange remainder bound (§17 item 8 fixes the term
count). The subject's `schedule_hash` is required: an executable claim
names the realisation it is about.

**Sampling.** For each domain component with range size R = hi − lo + 1,
assemble m = ⌈⌈log₂ R⌉/64⌉ consecutive generator words (least-significant
word first) into an integer, reduce modulo 2^⌈log₂ R⌉, reject and redraw
if ≥ R, add `lo`; components are consumed in enumeration order.

### 12.2 Domains

`"domain": { "bundles": [ { "name", "width", "lo", "hi" } ], "borrowed": [ same ], "regions": [ { "name", "cells": "all" | [ { "index", "lo", "hi" } ] } ] }`,
bounds inclusive, enumeration order as listed, last component fastest.
A `proof` label requires the domain to equal D; otherwise the claim is
`evidence` with the covered fraction.

### 12.3 Schema and composition

```
  versions; bindings { object_hash, interface_hash, closure_hash (required), reference_program_hash, dialect_mapping_version, target_hash, schedule_hash? }
  producer { name, version, materialisation { llvm_version, pipeline, normaliser_version } }
  regions { <closure_hash>: { kind, signature, bounds, frame (§9.4), resources { name: decimal }, gates_used { gate: { count, scheme?, epsilon? } },
            claims: [ <claim> … ], verification: { oracle: i, borrow_frames: [i], inverse_pairs: [ { g, ginv, claim: i } ], unitary: [i], channel: [i],
                                                   fault_rate: { domain, faults_by_code, undefined_excluded, layout_dependent_excluded } },
            cleanup: { "<variant>:<inherited_controls>": [ { path, realisation } ] },
            error:   { "<variant>:<inherited_controls>": { local: { "operator_norm"?: v, "diamond"?: v }, inclusive: { "operator_norm"?: v, "diamond"?: v } } },
            definedness_assumptions: [ids] } }
  composition { multiplicities: { "<hash>:<variant>:<inherited_controls>": n (from the realised schedule) }, epsilon_total: { "diamond": v }, method: "sum_over_multiplicities" }
```

`inclusive(R, key) = local(R, key) + Σ_callees n_c × inclusive(c, key_c)`
**per metric**, keyed like `cleanup` by `<variant>:<inherited_controls>`
(the realised error depends on both); every `local` value is a verified
common upper bound over all invocation contexts of its key in the bound
root schedule (§12.1), so multiplying by n_c is sound; an
`operator_norm` value converts
to `diamond` by ×2 once, at the point it is first combined with a
`diamond` value; `operator_norm` conclusions (T6, controlled unitary
variants) require `operator_norm` bounds throughout. A controlled
unitary variant requires a `numerical` claim; an ε > 0 realisation
compared as a channel requires a `channel` claim. Executable claims
(`numerical`, `channel`, `exhaustive` with `expected: "oracle"`) bind to
`schedule_hash` through their subject.

## 13. Coverage (coverage 0.8)

`{ "entries": [ { "point": <program-point id>, "source": "<dialect-spec stable id>", "classification": "lowered" | "trapped" | "shimmed", "reason", "fault_code"?, "shim_hash"?, "count" } ] }`.

## 14. Formal model

### 14.1 Reference interpreter *(normative)*

Executes an oracle's reference body per basis configuration: locations
and cells are bit-vectors, pseudo-locations read-only, predication is
`if`, each §4.2 row is its classical function (including the inherent
`inrange` check of loads and stores, the activation records of §3.7, the
`alloctab` and stack arrays), `fault` records the code and halts, `lift.
retval` halts with success and `f(x) = result_val`, the step counter
counts executed rows, counters are unbounded integers. It **defines** F_B
and the budget unit and rejects any body that executes a non-permutation
gate.

### 14.2 Quantum state semantics

The state of a Q region is a vector in ⊗ over live wires in allocation
order (bundles little-endian). `qalloc` tensors |0⟩; `qfree` removes
clean factors; `qborrow` introduces a factor in unknown state possibly
entangled with a reference system R, and the region's operation must be
U ⊗ I on it (§5.6); gates act by §4.4 under the active predicate;
`measure` (CC) is the projective computational-basis measurement with
Born probabilities, consuming the wires.

### 14.3 Theorems

- **T1 (totality).** For every well-formed oracle, budget and x ∈ D the
  reference interpreter halts within B + 1 rows and F_B(x) is unique.
- **T2 (prefix reversal).** For every executor whose realisation is a
  composition of ε = 0 permutation gates implementing §5.2 steps 1–4
  with the inverse step of §3.6, on every x ∈ D every non-interface wire
  is clean after step 4 and borrowed bundles hold their initial values.
- **T3 (permutation theorem).** If the realised unitary V of a circuit on
  span(D) is a permutation matrix and the final basis tuple equals P(x)
  for every x ∈ D, then V|span(D) = P.
- **T4 (round trip).** For every finite valid CC/R trace with retained
  run history and tapes, LIFO reversal per §7.4 restores the classical
  environment, memory, allocation table, device-model state and history
  to entry values; observed external events are not retracted.
- **T5.** As §6.3.
- **T6 (executor agreement).** Two executors conforming to §3–§7 on one
  target with the same schedule produce on every x ∈ D the same final
  tuple for every oracle (exact) and, for every action with `operator_
  norm` inclusive bounds e₁, e₂, unitaries within e₁ + e₂ in operator
  norm; for channels, diamond bounds d₁ + d₂.

### 14.4 Mechanisation *(deferred)*

## 15. Conformance suites

| Suite | Class | Tests |
|---|---|---|
| A | Executor | classical ISA; run history and LIFO reversal with loops, recursion, effects, segment `uncall` (impure suffix traps; nested `uncall` inside an uncalled segment; `uncall` over a `measure` traps), `hostcall`, `qreg.*`, fault records (T4) |
| B | Executor | oracle totality and prefix reversal: every fault code; B = 0; boundary halts; `lift.call`/`lift.ret` recursion with argument capture; one forward `lift.call` and one forward `lift.ret` step of a recursive call each followed by its inverse (§3.7); stack exhaustion (`sp + R_f > stack_limit`); matched `lift.oracle_uncall`; interface regions restored; pre-entries; `lift.free` on pinned entries; inherent load/store checks |
| C | Executor, Producer | T3 over full D at exhaustive widths for oracles, permutation actions, `qinplace` pairs, borrow frames; T6 agreement among VM, specialiser, transformed forms and the reference interpreter; the §16.3 examples as normative test vectors, including the stack-capacity boundary of example 2 |
| D | Executor | channel and unitary comparison for ε > 0 realisations; controlled-interference tests; checker-computed bounds; the diamond-norm SDP witness check of §12.1 |
| E | Target author, Executor | JCS parsing; AST evaluation; matching; scheme expansion and correctness; aggregation from event lists; timing model; imports |
| F | Producer | versioning, disjointness incl. control context; operand schema; row classes and frame sizing; index-space flattening; terminators; name resolution; permutation-only oracles; §6 transfer and windows; adjoint table; translation lemma side conditions with the four negative tests; `in`-wire use; acyclic action graphs; grammar; schemas; envelope and hashes; linking; frame-descriptor live ranges |
| G | Launch | every §10 entry point, state transition, binding rule, ownership rule; HOST_REQUEST/reply; reverse eligibility and tree order |
| H | Scheduler | §6 validity; capacity; reproducibility; specificity resolution; verbatim execution; INFEASIBLE/UNSUPPORTED |

## 16. Canonical textual form (normative)

### 16.1 Lexical

UTF-8; LF line endings; one instruction per line; tokens separated by
exactly one space; no trailing spaces; exactly one blank line before
each `section` line and none elsewhere. `NAME := [A-Za-z_][A-Za-z0-9_.]*`;
`INT := -?(0|[1-9][0-9]*)`; `FLOAT :=` shortest round-trip decimal with
`.` or exponent, finite; `STRING := "…"` with escapes `\"`, `\\`, `\n`;
`HEX := ([0-9a-f]{2})*`. Metadata lines are RFC 8785 canonical JSON
objects.

### 16.2 Grammar

```
  object    := header NL section*
  header    := "bennett-object" SP "isa=" VER SP "object=" VER SP "launch=" VER SP "sched=" VER SP "cert=" VER SP "coverage=" VER SP "target=" VER SP "ptr_width=" INT
  section   := NL "section" SP SECTNAME NL body
  SECTNAME  := "symbols" | "imports" | "functions" | "data" | "devices" | "layout" | "schedule" | "certificate" | "coverage"
  body      := jsonline | dataline* | function*
  jsonline  := JCS-canonical JSON object NL
  dataline  := NAME SP HEX NL
  function  := fhead NL regs? block+
  fhead     := ("fn" SP ("cc"|"r") | "oracle" | "action" | "perm_action" | "lproc") SP "@" NAME SP "(" plist ")" SP "(" plist ")" SP "(" plist ")" SP "(" plist ")" SP "(" plist ")"
               -- oracle: (in..) (tgt) (fault) (mem..) (args..) ; action: (mut..) (in..) (mem..) (args..) () ; lproc: (params..) (result) () () () ; fn: (params..) (results..) () () ()
  plist     := (param ("," SP param)*)?
  param     := NAME ":" type (SP ("in"|"mut"))?
  type      := "i" INT | "ptr" | "f64" | "token" | "wire" | "wire[" INT "]" | "reg[" INT "]" | "region[" INT "," INT "]" | "qreg[" INT "]"
  regs      := "regs" SP "{" SP (NAME ":" type ("," SP NAME ":" type)*)? SP "}" (SP "bounds" SP "{" INT ("," SP INT)* "}")? NL
  block     := "^" NAME "(" plist "):" NL instr+
  instr     := (lhs SP "=" SP)? OPCODE (SP operand)* (SP "{" NL instr+ "}" (SP "{" NL instr+ "}")?)? NL
  lhs       := NAME | "(" NAME ("," SP NAME)* ")"
  operand   := NAME | NAME "[" INT "]" | "@" NAME | "^" NAME ("(" (NAME ("," SP NAME)*)? ")")? | INT | FLOAT | STRING | "(" (NAME ("," SP NAME)*)? ")"
  OPCODE    := a mnemonic of §4 with its dotted suffix (§4.8 fixes operand count, kinds and result placement)
  VER       := INT "." INT
```

### 16.3 Example objects (normative test vectors, suite C and F)

**Example 1** (`inc8`): one oracle, no lprocs, no memory. The function
has **six** canonical lines.

```
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=32

section symbols
{"0":{"interface_hash":"8ce5e64f15830d8e596ba9b4861def6565dd567b5804300f427d8b9566d5be93","kind":"oracle","name":"inc8","signature":{"abi":"0.8","args":[],"fault":4,"in":[8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}}}

section functions
oracle @inc8 (x:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { one:reg[8], r:reg[8] }
^entry():
one = lift.const.i8 1
r = lift.add x one
lift.retval r
```

The object has no `layout` section, so the oracle's closure set is
empty and its envelope is exactly these bytes (each line LF-terminated):

```
isa=0.8
ptr_width=32
{"abi":"0.8","args":[],"fault":4,"in":[8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}
oracle @inc8 (x:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { one:reg[8], r:reg[8] }
^entry():
one = lift.const.i8 1
r = lift.add x one
lift.retval r
```

With B ≥ 3 every x yields `(x + 1 mod 256, 0)` (`result_val` = 0 ⊕ r);
with B = 2 every x yields `(0, FAULT_BUDGET_STEPS)`.

**Example 2** (`sum_db`): an oracle reading an interface region through
lifted memory with a recursive lproc that receives the base as a
parameter, and a global accessed by address.

```
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=32

section symbols
{"0":{"interface_hash":"68225d213c44812fe844cd295d8821127c3cf31682be4eb19303cb53f9b147f7","kind":"oracle","name":"sum_db","signature":{"abi":"0.8","args":[],"fault":4,"in":[8],"kind":"oracle","mem":[{"A":4,"W":8,"role":"in"}],"tgt":8,"tier":"q"}},"1":{"interface_hash":"74f110bbafde68a4785025e7e571ef871ddd83a09465ab9c1604f653a0cfcd92","kind":"lproc","name":"sum","signature":{"abi":"0.8","kind":"lproc","params":[8,8,32],"result":8,"tier":"q"}},"2":{"interface_hash":"7002ed5ea010907a0ae99065663f22fb7d18ca1d6cb171fed57e2594bd9367e6","kind":"data","name":"zero","signature":{"abi":"0.8","kind":"data","size":1,"tier":"-"}}}

section functions
oracle @sum_db (n:wire[8] in) (t:wire[8]) (f:wire[4]) (db:region[4,8] in) ()
regs { base:reg[32], acc:reg[8], r:reg[8] }
^entry():
base = lift.addr @db
acc = lift.const.i8 0
r = lift.call @sum (n, acc, base)
lift.retval r
lproc @sum (n:reg[8], acc:reg[8], base:reg[32]) (r:reg[8]) () () ()
regs { zp:reg[32], zv:reg[8], z:reg[1], one:reg[8], n2:reg[8], idx:reg[32], p:reg[32], v:reg[8], acc2:reg[8] }
^entry():
zp = lift.addr @zero
lift.boundscheck zp 1
zv = lift.load.i8 zp
z = lift.icmp.eq n zv
qbranch z ^done ^more
^more():
one = lift.const.i8 1
n2 = lift.sub n one
idx = lift.zext.i32 n2
p = lift.add base idx
lift.boundscheck p 1
v = lift.load.i8 p
acc2 = lift.add acc v
r = lift.call @sum (n2, acc2, base)
lift.ret r
^done():
lift.ret acc

section data
zero 00

section layout
{"A_tab":4,"H":13,"S_cells":9,"globals":{"zero":{"base":16,"image":"zero","size":1}},"heap_base":4112,"heap_limit_max":4080,"interface_regions":{"sum_db":{"db":{"base":4096}}},"null_size":16,"ptr_width":32}
```

Ranges: null [0,16), `zero` [16,17), `db` [4096,4112), heap [4112,8192)
within 2^13: disjoint; two pre-entries ≤ 2^4. `alloctab` starts with
pinned entries (16,1) and (4096,16), `atop = 2`. `@sum` resolves `n acc
base` to its params and everything else to its own locations; its
locations are `n acc base` (params), `r` (result name), then its nine
`regs`: m′ = 13, **R_sum = 16 cells**; `@sum_db` reads `n` as a pseudo-
location. Input n performs n + 1 nested calls (the last at depth n + 1)
and, the stack being monotonic, occupies 16(n + 1) stack cells. With
sufficient budget F_B(n) = (Σ_{i<n} db[i] mod 256, 0) for n ≤ 16 (n = 16
needs 272 cells, hence S_cells = 9 and `stack_limit ≥ 272`); for n > 16
the check at `p` faults `FAULT_UB_MEMFAULT` on the first out-of-range
byte; with small B, `FAULT_BUDGET_STEPS`; with `depth_limit ≤ n` or
`stack_limit < 16(n + 1)`, `FAULT_BUDGET_DEPTH`. Hashes by §9.2: `@zero`
is a data symbol and the `zero` global's image; `@sum` is a one-member
SCC (its self-reference is written `@$0`, its `@zero` reference is
replaced by `@` + the `zero` hash, which is its only part-(6) line; its
closure set is the `zero` global's leaf and image), so its envelope is
exactly the bytes below, its `scc_hash` is their SHA-256 and its hash
is SHA-256 of the ASCII `<scc_hash hex>:0`:

```
isa=0.8
ptr_width=32
{"abi":"0.8","kind":"lproc","params":[8,8,32],"result":8,"tier":"q"}
lproc @sum (n:reg[8], acc:reg[8], base:reg[32]) (r:reg[8]) () () ()
regs { zp:reg[32], zv:reg[8], z:reg[1], one:reg[8], n2:reg[8], idx:reg[32], p:reg[32], v:reg[8], acc2:reg[8] }
^entry():
zp = lift.addr @7002ed5ea010907a0ae99065663f22fb7d18ca1d6cb171fed57e2594bd9367e6
lift.boundscheck zp 1
zv = lift.load.i8 zp
z = lift.icmp.eq n zv
qbranch z ^done ^more
^more():
one = lift.const.i8 1
n2 = lift.sub n one
idx = lift.zext.i32 n2
p = lift.add base idx
lift.boundscheck p 1
v = lift.load.i8 p
acc2 = lift.add acc v
r = lift.call @$0 (n2, acc2, base)
lift.ret r
^done():
lift.ret acc
data zero 00
layout globals.zero {"base":16,"image":"zero","size":1}
7002ed5ea010907a0ae99065663f22fb7d18ca1d6cb171fed57e2594bd9367e6
```

`@sum_db`'s envelope includes every layout leaf, the `zero` image, `@` +
the `sum` hash in place of `@sum`, and the `sum` hash as its part-(6)
line (`@db` is an interface region, not a symbol):

```
inc8 = 8ce5e64f15830d8e596ba9b4861def6565dd567b5804300f427d8b9566d5be93
zero = 7002ed5ea010907a0ae99065663f22fb7d18ca1d6cb171fed57e2594bd9367e6
sum = 74f110bbafde68a4785025e7e571ef871ddd83a09465ab9c1604f653a0cfcd92
sum_db = 68225d213c44812fe844cd295d8821127c3cf31682be4eb19303cb53f9b147f7
```

## 17. Decisions deferred to implementation, with defaults

Each item is one an implementer must decide to build; any decision is
conformant provided two implementations agree on the default below until
the item is revised. Items 1–5 are asserted non-semantic.

1. **Binary encoding.** Default: none; §16 text is the only interchange
   form.
2. **Gate-name registry.** Default: the names of §4.4 only; an unknown
   gate name is a load error.
3. **Further device models.** Default: the four of §7.3; an `effect` on
   any other device is `FAULT_EFFECT_UNMODELLED`.
4. **Mechanisation of §14.** Default: none; the reference interpreter is
   the oracle.
5. **Memory layout of the opaque C objects.** Default: opaque; only the
   listed functions touch them.
6. **Measurement-based cleanup** (§6.4): the normative fixup, its
   controlled variant and its certificate kind. Default: unitary cleanup
   (`reverse`); `capabilities.mbu` is `false`.
7. **Expansion library** (§11): the gate-level expansion below row
   level. Default: the library `ref` published by `bennett-isa-spec`
   (ripple-carry adders and comparators, linear `inrange` scans,
   one-hot address dispatch, clean scratch released in reverse order);
   a schedule that names no `expansion` binds `ref` at the ISA's own
   version.
8. **Enclosure procedure for transcendental entries** (§12.1). Default:
   Taylor series of sin and cos to the first term whose Lagrange
   remainder bound is below 2^−(`precision_bits` + 2), argument reduced
   modulo 2π with an outward-rounded enclosure of π.
9. **Default `epsilon_share`** (§8.1, §11) when a schedule assigns none.
   Default: the region's `epsilon` divided equally among its ε > 0
   operations.
10. **`any`-class resolution** (§11). Default: the first class in JCS
    order with capacity.
11. **Occupancy rate of a class absent from `rate`** (§8.2). Default: 1.
12. **Classical step timing of CC/R instructions and effects** (§8.2).
    Default: `classical_step_time` each, sequential.
13. **Suite sizes** (§15): the exhaustive widths of suite C and the
    sample counts of `sampled` claims. Default: exhaustive for ≤ 16
    interface bits; 2^16 samples above.
14. **Hardware handling of an unclean `qreg.free`** (§3.3). Default: the
    run is marked `FAILED` with a fault record `FAULT_UB_TRAP` at the
    instruction, since cleanliness of an arbitrary state is not
    testable nondestructively.


# Background (not graded): `Bennett-Dialect-Spec-0.2.PROGRESS.md`

# Dialect 0.2 full text — progress

Job: write the normative text of dialect draft 0.2 (`spec/Bennett-Dialect-Spec.md`) from the
ratified outline `spec/outline-0.2.md`. Brief: `docs/briefs/2026-10-29-dialect-0.2-fulltext.md`.
Owned paths: `spec/Bennett-Dialect-Spec.md`, `spec/bennett_markers.h`, `spec/README.md`, this
file, `SPEC_VERSIONS.toml`, `corpus/legality/cases/spec-*`. Standing rule: no narrowing.

## Read (2026-10-29)

- [x] `spec/outline-0.2.md` in full, including the maintainer rulings (E1-E3, E5-E14 as
  recommended; E4 = riscv64; BLK-1..4 named blockers; graded against ISA 0.8)
- [x] `spec/Bennett-Dialect-Spec.md` 0.1 in full
- [x] `docs/spikes/2026-10-28-legality-findings.md` (decisions 1-4)
- [x] `docs/audit/2026-10-29-dialect-0.1-narrowing-audit.md` in full
- [x] `docs/spikes/sqlite/REPORT.md` in full
- [x] `../bennett/docs/Bennett-NorthStar.md` in full
- [x] ISA 0.8 `../bennett-isa-spec/spec/Bennett-ISA-Spec.md` in full
- [x] `../bennett/HANDOFF.md` ("What made the ISA rounds converge")
- [x] `../bennett/docs/council/rubric-isa.md`
- [x] reference interpreter README (CLI: check, hash, run-oracle, step-check)

## Tools used

- Rust ISA reference interpreter: a copy of
  `../bennett-isa-spec/reference-interpreter/target/debug/bennett-isa-ref` (built 2026-10-29
  07:40) in the job scratchpad, so that the concurrent interpreter job cannot change it under
  this job. Every `isa object=` example is checked with `check`, every `text run=` line is the
  output of `run-oracle`, every prefix-reversal claim the output of `step-check`.
- LLVM 18 (`/usr/lib/llvm-18/bin`), 20 (Julia artifact, `corpus/legality/toolchains.toml`),
  23 (`/usr/lib/llvm-23/bin` for clang; rustc llvm-tools for opt): every `llvm` block parsed and
  verified on all three, headless (CLAUDE.md rule 11).

## Sections written

- §1-§3 + header (commit 56a3eb1)
- §4-§8 (commit 85c53ab)
- §9-§12 (commit cd709ee)
- §13-§14 (commit fd30dd5)
- §15-§16 (commit 49a2100)
- §17-§18 + corpus `spec-sem2-*` (commit df9e0a5)
- §19-§25 (commit e0e5142)
- Appendices A (outline changes), B (example index), C (546 generic intrinsics); SPEC_VERSIONS
  0.2/0.8; README change rules (commit d0c4830)
- Hostile re-read under the rubric, two passes of fixes (commits eda7eb3, aa004bf), then a
  consistency pass (section cross-references by script: no dangling internal reference; the
  `markers-c` block equals the header's prototype block byte for byte; version strings `0.2`,
  `dialect-0.2;isa-0.8`, `isa=0.8 … target=0.8` checked).

Size at the end: ~7310 lines, ~59,500 words, 385 kB; 87 verdict examples (82 `llvm`, 5 `c`: 56 accept,
26 reject, 5 blocked), 17 normalisation pairs, 6 executed ISA objects.

## Verification run (final state)

- Every `llvm` block (126) parses and verifies with `opt -passes=verify` on LLVM 18, 20 and 23,
  headless (`env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER
  TMPDIR=$PWD/.tmp`).
- Every `isa object=` block passes `bennett-isa-ref check`; every `hash=` line equals `hash`;
  every `run=` line is the output of `run-oracle`; every `step-check=` claim is the output of
  `step-check` (scratch tool `checkruns.py`: 0 failures).
- Normalisation pairs with `native=` lines: input and output modules compiled with clang 18/23
  and the job's seed implementations, the stated values computed by running them.
- `cc-run=` native statuses (sjlj 77, fiber 98, exit 3) computed by native builds (clang 18 and
  23, -O2); the R-tier `run:`/`reverse:` lines need `run-cc`/`reverse` (b-isa-spec-xam).
- Header: compiles as C and C++ on clang 18/20/23; static asserts on record layouts; IR
  signatures of all 23 prototypes identical across majors and equal to §3.2.
- Corpus: `spec-sem2-ctrl`, `spec-sem2-adj`, `spec-sem2-compute` are byte-equal to §18.8. Baseline
  on a scratch copy of `corpus/legality` with `python3 harness/run.py baseline --majors 18,20,23
  --cases 'cases/spec-sem2-*'` (headless): ctrl agrees on all majors; adj and compute report
  `BASELINE PROBLEM … L1 baseline exit=87` on all majors, because the trace runtime is still at
  ABI v0 (2-argument adj, 3-argument compute); this is bd `-566` (trace runtime at ABI 0.2).

## Decisions taken while writing (not in the outline)

- Primitives `__bennett_nz_alloc` / `__bennett_nz_free` (ISA alloc/free, lift.alloc/lift.free)
  added next to `__bennett_nz_fault`: the runtimes allocator needs a way to reach `lift.alloc`.
- Reserved-name rules apply to *producer inputs* (driver checks before link); runtimes/arith
  bitcode may use `__bennett_rt_/dev_/sf_/nz_` names.
- §5: abstract value = (atom set, TOP flag); TOP never stands for a ROOT atom; K = 4096 cap is
  normative (decides verdicts). Residue classes carry an extent [lo, hi) from array types (B-27).
- §5: `inttoptr` constants are TOP for function pointers (A(F) is fixed only after the
  comparison link); a Julia `@cfunction` constant traps unless it equals an A(F) at run time;
  Bennett.jl's `ptr @f` route keeps the capability.
- §6.5: two realisations: *direct* (handle never stored in memory: CC qreg SSA values, no bound)
  and *static register file* (stored handles; reference instance bound; infinite -> BLK-1).
- §6.6: device-entry pointer parameters get a candidate ROOT(E,i) atom that survives only if it
  reaches a marker handle operand (decides QREG binding).
- §7.5(b): R-tier allocation hoisting uses the reference instance bound; BLK-4 only when infinite.
- §8.1: descriptor layout = LLVM struct {H,[n x Bind],[m x DevBind]} under the datalayout.
- §8.5: snapshot register released by `measure` (unentangled basis state).
- §8.6: wide outputs are the `wide` event: copy-out pairs issued as CC-level region calls
  (`qreg.slice` views, `@xor<w>` action), temporaries freed with the ISA §3.3 dynamic check.
- §8.7: in-place verification computes B_min; run-time budgets checked at the marker (`T-BUDGET`).
- §9.2: budget table JSON schema and precedence (identity > region key > symbol glob > default).
- §9.5 example `budget-device-computed` uses a 64-bit value assembled from 64 measurements, so no
  launch-time token set covers it (a value set like {5, n+5} would be launch-mintable).
- §10: Cl/M/Co object states; slices with classical twins; events applied as CC-level region
  calls (ISA §6 per-region coarse windows make a static action unable to uncompute a slice after
  an arena write); per-slice fault registers retained and combined by `@firstfault`.
- §12.1: N33 runs immediately before N32 (its fpext/fptrunc pairs are FP that N32 rewrites).
- §14.9: blockaddress values are bytes of a driver-added data object `__bennett_rt_blk.<f>`, so
  they never collide with A(F) or other objects.
- §15.2: the default `cpuid` table is read on the build machine and recorded in the build record.
- §16: reference object = wrapper `@ref` + lprocs; layout restricted to closure-reachable
  globals; A_tab chosen so allocation-table overflow never precedes heap exhaustion.
- §18.4: `T-LEAK` outside generations is checked at program end (§6.6's REPL lifetime).
- §19.5: `text_base` rises above the device ranges when they pass 0x400000 (native binary must
  map heap/arena/regions disjointly from its code); §20.1 RAM placed by the profile's linker
  script at 0x80000000 after the other data.

## Departures from the outline

All are in the spec's Appendix A (A1-A23), each with its reason; every one keeps or widens the
outline's capability. Summary: A1 wide outputs by 2k-1 copy-out calls (outline's qxor cleanup is
ill-formed under ISA §6); A2 snapshot release by measure; A3 direct handle realisation without a
bound; A4 exact reference instance bound; A5 Cl/M/Co; A6 slices without stores/markers + classical
twins; A7 one XOR of c ⊕ v; A8 CC-level event application; A9 retained per-slice fault registers;
A10 effects in action regions are fault 8; A11 history as declared outputs measured at the
epilogue; A12 two more primitives; A13 `@cfunction` constants dispatched by value; A14 thunk cycles
resolve to themselves (BD-E-REGION-THUNK deleted); A15 N0 (LLVM's own lowering passes); A16 N34
marks as metadata; A17 wrapper/lproc form and layout rules; A18 compare-tree block names; A19
blockaddress/indirectbr, seven FP formats, exit via hostcall, B_min/T-BUDGET; A20 two more wording
items; A21 `__bennett_rt_platform_ram`; A22 `spec-sem2-*` beside `spec-sem-*`; A23 N33 before N32.

## Examples and checker requirements

The full index is the spec's Appendix B. Capabilities per example family:

| Examples | Checker capability | Executor / CLI |
|---|---|---|
| markers-ir, markers-c | parse, header | LLVM 18/20/23, clang 18/20/23 |
| operand-*, recog-*, attr-*, unwind-invoke, julia-jlplt, effect-lie, pt-variable-index, handle-* (20), qstore-twice, region-* (18), oracle-*, budget-*, indirect-*, asm-musl-syscall, version-flag | parse, recognise | LLVM; Python reference recogniser (to be written in dialect_check.py) |
| inplace-* (4) | parse, recognise, run-oracle | isa-ref `run-oracle` (exists) for the inverse check |
| budget-table=rung4-mini | driver | Python |
| tdl, tdl-overwrite, tdl-effect, tdl-angle (+ tdl=, state=) | parse, recognise, tdl, run-action | Python TDL; isa-ref `run-action` (b-isa-spec-xam, requested) |
| effect-console-r, effect-console-cc; sjlj-two-frames, fiber-pingpong, exit-status (cc-run=) | frontend, run-cc, reverse | isa-ref `run-cc`, `reverse` (requested); native statuses computed |
| 17 normalise-in/out pairs, 10 native= | parse, normalise, native | LLVM; Python normaliser; clang + spec/seeds (not yet created) |
| residual-nsw, residual-clean | validate | Python |
| inc8, add2, rung4-mini, rung8-mini, listsum, switch5 (lift=, linkmap=, object=, hash=, run=, step-check=) | map, check, hash, run-oracle, step-check | isa-ref `check`, `hash`, `run-oracle`, `step-check` (exist; all lines verified) |
| rung4-minidb, rung4-grover-tu (+ native=) | frontend, recognise, native | clang 18/20/23 |
| sem2-ctrl, sem2-adj, sem2-compute (events=, state=) | trace, run-action | trace runtime at ABI 0.2 (bd -566); isa-ref `run-action` (requested) |

Blocked examples (one per BLK): `operand-width-host` and `handle-vec-unbounded` (BD-B-ISA4,
BLK-1), `budget-device-computed` (BD-B-ISA1, BLK-2), `inplace-param-quantum` (BD-B-ISA3, BLK-3),
`region-reversible-qalloc-dynamic` (BD-B-ISA12, BLK-4); each has a `text blocker=` report line.

## Open questions

- Rule ids without an example (P-1 fails on them until added; Appendix B lists them): N0, N12,
  N15, N25, N34, N35; V2-V16; PT12; the OUT binding's object; BLOCK, CLOCK, CONSOLE device
  bindings; entry-state transfer (§8.5); indirectbr; §19.3-§19.8; §20.
- `spec/seeds/` (checker seeds named in §21.4) and `spec/asm/<arch>.toml` (§15.1) are not owned
  paths of this job and do not exist yet.
- ISA wording items raised in §25.2: certificate fields (build record, budget table, deferred
  measurement); ISA §12.2 domains with a fixed classical region (rung 4(a)); `qreg` across CC
  call/ret/br; code 10 "(R only)".
- TDL: event application as CC-level region calls is exact but not one ISA action; an ISA 0.9
  per-cell window rule would allow static actions (efficiency, not capability).

## Issues filed (bd)

- `b-dialect-spec-566`: note added (spec-sem2-adj/compute baseline exit 87; trace runtime to ABI 0.2).
- `b-dialect-spec-d4k`: checker seeds `spec/seeds/` (§21.4) do not exist.
- `b-dialect-spec-gvr`: rule ids without a checked example (P-1 list of Appendix B).
- `b-dialect-spec-rq0`: publish `spec/asm/<arch>.toml` from §15.
- `b-dialect-spec-gwf`: ISA 0.9 wording items raised by §25.2.

`.beads/issues.jsonl` was rewritten by `bd` and is left uncommitted (not an owned path).


# The document under review (round 1 snapshot)

# Bennett LLVM Dialect — Specification, draft 0.2

**Date:** 2026-10-29. **Status:** draft 0.2 of `bennett-dialect-spec` (`Bennett-NorthStar.md`
§3, §6.1), written from the ratified outline `spec/outline-0.2.md` (maintainer rulings of
2026-10-29 at its end) for the first council round on 0.2; not yet graded. It replaces draft
0.1, which the narrowing audit (`docs/audit/2026-10-29-dialect-0.1-narrowing-audit.md`) found
to narrow north-star scope in 40 distinct places. Nothing is implemented. It targets the
Bennett virtual ISA **draft 0.8** (`bennett-isa-spec/spec/Bennett-ISA-Spec.md`, council
accepted 2026-10-28), cited "ISA §n", and is graded against ISA 0.8. MUST, MUST NOT, SHOULD and
MAY are normative; *(non-normative)* explains. Mechanics this draft does not settle carry a
**default** in §24; capabilities that ISA 0.8 cannot express in some case are **blockers** in
§25, each with the exact ISA change.

**Versioning.** Dialect 0.2: markers 0.2, handles 0.2, regions 0.2, oracle-abi 0.2, tdl 0.2,
effects 0.2, norm 0.2, map 0.2, asm 0.2, platform 0.2, driver 0.2, corpus 0.2; targets ISA 0.8.
The **full version string** (`0.2`) is the compatibility unit (§23): drafts are not compatible
with each other.

**Standing rule (CLAUDE.md rule 10; council rubric S0).** This document narrows no capability
that the north star promises (its thesis, §3–§5 and every rung of the §8 demo ladder; Grover
over unmodified SQLite is the core). It rejects at compile time only what the north star itself
requires to be rejected or what a maintainer decision settles; every such rejection is a row of
§22.1 citing the clause or decision. A deferral (§24) postpones mechanics only and states the
capability it keeps. Where ISA 0.8 cannot express a promised capability in some case, the
dialect still specifies the whole mechanism, states the ISA 0.8 realisation that exists for the
other cases, and names a blocker (§25) whose verdict is `blocked:`, never `reject:`.

**Sources.** North star §0, §3, §4, §5, §8; the legality spike and its findings
(`docs/spikes/2026-10-28-legality-findings.md`, decisions 1–4); the narrowing audit (row ids
D1–D25, B-01–B-55, O-01–O-08, G-12–G-16, ISA-1–ISA-11 are cited unchanged); the rung-4 spike
(`docs/spikes/sqlite/REPORT.md`, cited "SQLite §n"); the outline (cited "outline", decisions
B1–B17, questions E1–E14).

---

## 1. Scope and conformance

### 1.1 What the dialect is

The dialect is the contract between **front ends** that emit LLVM IR containing calls to
`__bennett_*` marker functions and the **plugin** that, at the final link of a whole program,
recognises those calls, analyses and normalises the code they reach, and maps it onto the ISA
(ISA §1.1). It fixes:

- the marker ABI, operand encodings and C header (§3);
- the processing order, execution tiers, polyvariant variants and function addresses (§4);
- the device analysis: points-to, value sets and every question answered from them (§5);
- the handle convention, provenance, comparison and collections of handles (§6);
- regions: kinds, candidate sets, dispatch, identity, well-formedness (§7);
- the oracle interface: the descriptor, parameter and device bindings, entry state, wide outputs
  and in-place updates (§8);
- budgets (§9);
- taint-driven lifting of classical code under control (§10);
- effects and device models per tier (§11);
- the materialised normalisation and the residual-poison validator (§12), floating point
  (§13), calls and control transfer (§14), inline asm and target intrinsics (§15);
- the lifting map from materialised LLVM to ISA objects (§16);
- the device classical memory model, CC and R lowering rules and fault outcomes (§17);
- a reference semantics from marker programs to the ISA formal model (§18);
- the driver's modes and plugin-invocation interface (§19);
- the platform profile `riscv64-bennett-virt` (§20);
- the legality corpus and conformance suites (§21); diagnostics (§22); versioning (§23);
  deferred mechanics (§24); blockers and ISA items (§25).

It does not fix the plugin's optimisation pipeline after normalisation, the plugin's device
objects beyond the constraints of §18.7, or any format the ISA owns.

### 1.2 Conformance classes

| Class | Who | Obligation |
|---|---|---|
| Producer | front ends (clang, rustc, Bennett.jl, importers) | emit modules that satisfy §3 and the outlining conventions of §7.6; never emit a reserved name of §3.1 other than a marker |
| Plugin | `bennett-plugin` and competitors | the processing order of §4.1; give every module the verdict the rules give it, with the diagnostics of §22; produce ISA objects whose execution equals the reference semantics (§18.7); suites DA–DX (§21.3) |
| Driver | `bennett-driver` | §19; links `bennett-runtimes` and `bennett-arith` bitcode of the link's LLVM major (§19.1); builds the comparison link and the native comparison binary (§17.7); emits blocker reports (§25) |
| Validator | the plugin's validator and `bennett-conformance` | the residual-poison validator (§12.4) and the reference recogniser (§3, §5, §6, §7), implemented independently; suites DA–DN |
| Runtime | `bennett-runtimes` and `bennett-arith` | define every entry point that §11, §13, §14, §17 and §20 name (prefixes `__bennett_rt_`, `__bennett_dev_`, `__bennett_sf_`, §3.1) with the semantics stated there, as ordinary bitcode compiled by the same pipeline; suites DR and DF |
| Platform | a platform profile of §20 | a board model plus shims satisfying §20; suite DP |

`scripts/dialect_check.py` in this repository is the seed of the pre-flight checker (§1.5). It
never bounds this document: an example it cannot yet execute fails the check (rule P-2, §1.5).

### 1.3 Relation to the ISA specification

The ISA is settled; this document never redefines it. Every ISA notion used here (tiers, wires,
`qreg` handles, oracles, actions, permutation actions, lprocs, F_B, budgets, tokens, fault
codes, the reference interpreter, interface and closure hashes, layouts, the launch ABI) has
exactly the meaning ISA §2–§17 give it. Where the dialect needs a construct ISA 0.8 lacks, this
document states (a) the full dialect mechanism, (b) its realisation on ISA 0.8 where one exists,
which may be a longer construction (an **efficiency item**, §25.3), and (c) otherwise a
**blocker** (§25.1) naming the exact ISA change. The dialect never shrinks to fit the ISA and
never extends the ISA unilaterally.

### 1.4 Departures from the north star

Only these remain. Every row of 0.1 §1.4 that narrowed scope (1.4-d, 1.4-e, 1.4-f) is deleted;
its replacement is §10, §9 and §8.7 respectively.

| North star | Dialect 0.2 | Why |
|---|---|---|
| §3.1 handle row: a handle through an `inttoptr`/`ptrtoint` round trip is rejected | Provenance flows through bitwise copies (§6.2) | Spike F1; maintainer decision 2; north-star amendment A2 (drafted with A1, bd `-25h`) |
| §3.1: regions entered as `__bennett_ctrl(q, @f, …)` with a constant `@f` | Region operands are classical data dispatched over a candidate set bounded by the program (§7.2) | Spike F3; maintainer decision 3 |
| Region named by symbol | Region identity is by content (§7.3) | Spike F2; maintainer decision 1 |
| §3.1 handle row is silent on comparison | `icmp eq/ne` of handles is identity (§6.3) | Maintainer decision 4 (2026-10-29; legality findings §3); a superset |
| §3.1, §4.2: a `qstore` into a register not known to be clean is a compile-time error | `qstore` is the ISA's XOR store; the compile-time rule is an optional warning `BD-W-QSTORE-UNCLEAN` (§6.7) | A register-granularity rule forbids the uncomputing second store; a superset of the north star (audit 1.4-g, D7) |
| §3.2: normalisation of "the outlined region" | Normalisation applies to every device variant (§12.1) | Device CC code is lowered to ISA CC, whose semantics differs from LLVM's poison semantics (ISA §4.1); a superset (audit 1.4-h) |

### 1.5 Notation and checked examples

LLVM IR is LLVM's textual form with opaque pointers, as accepted by LLVM 18, 20 and 23. `pw` is
the pointer width in bits of address space 0 in the module's datalayout (64 when the module has
no datalayout). Numbers are decimal unless written `0x…`. A(F) is the function address of §4.4.

**Process rules** (also in `spec/README.md`):

- **P-1.** Every mechanism rule id (the steps S1–S9, rules N1–N35, V1–V16, TDL-1–TDL-12, the
  points-to rules PT1–PT12, the binding kinds of §8.2, the transforms of §14, the map rows of
  §16.4) has at least one checked `accept` example; every compile-time rejection of §22.1 has
  one `reject` example; every blocker of §25.1 has one `blocked` example. Appendix B is the
  index, and the checker derives it from the text: a rule id with no example fails the check.
- **P-2.** An example that the checker cannot yet execute **fails** the check with
  `checker-unimplemented: <capability>`. It is never skipped, and this document never removes
  or weakens an example to make the checker pass. The freeze gate is an all-green check.
- **P-3.** Every executed result comes from an independent executor: LLVM tools, natively built
  binaries, or the Rust ISA reference interpreter `bennett-isa-ref`. Python computes only
  *expected* artefacts (recogniser verdicts, normaliser output, map output, TDL events), and is
  never both producer and judge of one example.

Every fenced block whose info string starts with `llvm`, `isa`, `c`, `rust`, `julia`, `json` or
`text` followed by a tag below is a **checked example**. Its attributes are `key=value` pairs.
The last column names the checker capability (Appendix B) and, where the ISA reference
interpreter is the executor, the `bennett-isa-ref` command (`check`, `hash`, `run-oracle`,
`step-check` exist; `run-cc`, `reverse`, `run-action`, `run-program` are requested,
bd `b-isa-spec-xam`).

| Tag | Meaning; what the checker does | Capability / command |
|---|---|---|
| `llvm markers-ir` | the marker list of §3.2; compared with the C view | `parse`, `header` |
| `c markers-c` | the prototypes of the C header; byte-equal to `spec/bennett_markers.h` between its BEGIN/END PROTOTYPES lines | `header` |
| `llvm example=ID verdict=V` | a module; it parses and verifies on LLVM 18, 20 and 23 and the reference recogniser gives verdict `V` (`accept`, `reject:<code>` or `blocked:<code>`, §1.6). Optional attributes: `candidates=f,g` (the resolved candidate set of the first region operand, §7.2), `callees=f,g` (the candidate set of the first indirect call, §14.2), `shapes=N` (the number of compiled oracle shapes, §8.4), `mode=validate` (validator only, §12.4), `rmode=@f` (compiled in the whole-program R mode with entry f, §19.2) | `parse`, `recognise` |
| `llvm normalise-in=ID` / `llvm normalise-out=ID` | the normaliser (§12) applied to the first gives the second, lines compared after collapsing runs of blanks; both verify on the three majors; the second passes the validator | `parse`, `normalise` |
| `text native=ID` | inputs and outputs of the native differential of a normalisation pair or a lifted example: both modules (or the C source and the module) built natively with the seeds of `spec/seeds/` (§21.4), run on the listed inputs, outputs equal to the listed values | `native` |
| `llvm lift=ID` | a materialised module; attribute `region=@f` names the region function and `desc=` the binding shape: the parameters' bindings in order (`IN(n,zext)`, `IN(n,sext)`, `ARG(W)`, `MEM_IN(A)`, `OUT(size)`), then `;dev=` device bindings (`ENTROPY(A)`, …) and `;tgt=` n(tgt) | `parse`, `map` |
| `text linkmap=ID` | the comparison-link facts the map of `lift=ID` reads (§19.5): `null_size`, `heap_base`, `heap_limit_max`, the globals with their bases, the A(F) of address-taken functions, and the budget table's largest `heap` and `stack` | `map` |
| `isa object=ID` | the reference object (§16.2) that the map produces from `lift=ID`, as complete ISA text; byte-equal to the map output; `bennett-isa-ref check` accepts it | `map`, `check` |
| `text hash=ID` | the interface hashes of the object's symbols (`bennett-isa-ref hash`) | `hash` |
| `text run=ID` | lines `input=… [mem=name:hex] [arg=…] budget=s,h,st,d -> code=C payload=P steps=N`; each line is the output of `bennett-isa-ref run-oracle <object> ref` with those options | `run-oracle` |
| `text step-check=ID` | a prefix-reversal claim; the output of `bennett-isa-ref step-check <object> ref --exhaustive` with the stated options | `step-check` |
| `llvm semantics=ID corpus=NAME` | a marker program; byte-equal to `corpus/legality/cases/NAME.ll`; run through the trace runtime and the reference semantics (§18) | `trace`, `run-action` |
| `text events=ID` / `text state=ID` | the event list (§18.2) of a marker program on an input, and the state vector before event `at` | `trace`, `run-action` |
| `text tdl=ID` | the TDL partition (§10, TDL-3) and generated event list of an action region invocation | `tdl`, `run-action` |
| `text cc-run=ID` | a CC or R run: results, fault records, tape, and the state after `bennett_reverse` | `run-cc`, `reverse` |
| `text blocker=ID` | the blocker report (§25.1) the plugin emits for a `blocked:` example | `recognise` |
| `json budget-table=ID` | a budget table (§9.2); parsed and resolved against the example it names | `driver` |
| `c example=ID`, `rust example=ID`, `julia example=ID` | a source file compiled by the toolchains of `corpus/legality/toolchains.toml` (`clang -O2 -flto` on 18, 20, 23, with `-I spec`; with `rmode=` against the `bennett-runtimes` musl sysroot, for which the checker's seeds stand in; `rustc --emit=llvm-bc`; Julia `code_llvm`) and then `lto<O3>`; the result is recognised with verdict `verdict=V` | `frontend`, `recognise` |

A module example that calls a marker or a primitive without declaring it implicitly contains
its declaration (§3.2, §3.1). **Section references**: `§n` is a section of this document, `ISA
§n` of the ISA specification, `NS §n` of `Bennett-NorthStar.md`; a reference that continues a
list (`ISA §4.7, §5.3`) names the same document as the reference before it. Fenced blocks
without a tag are illustrations and are non-normative; an `llvm` or `isa` block without a tag is
an error of this document.

### 1.6 Diagnostics and verdicts

A module's **verdict** is one of:

- `accept`: the plugin produces its objects;
- `reject:<code>`: a compile-time rejection of §22.1. The plugin MUST fail the compilation
  (nonzero exit, no output object) and report at least the first diagnostic in the processing
  order of §4.1;
- `blocked:<code>`: the module is accepted by the dialect, but at least one program point needs
  a capability that ISA 0.8 cannot express (§25.1). The plugin MUST produce its objects with
  every such point lowered to a **blocker trap** (§25.1: a run-time fault on exactly the
  executions that reach the point), MUST emit the blocker report of §25.1 and MUST exit with the
  distinct status 3. The code is the first blocker report in processing order.

A module that would be rejected and blocked is rejected. Warnings (`BD-W-*`, §22.4) never change
a verdict.

## 2. Terminology

- **Marker**: one of the 23 functions of §3.2. **Marker call**: a `call` or `invoke` whose
  callee is a marker (§3.5). **Effect marker**: one of the five `__bennett_effect_*` markers.
- **Primitive**: a reserved function with prefix `__bennett_nz_` that the map lowers to an ISA
  instruction directly (§3.1, §16.4): `__bennett_nz_fault`, `__bennett_nz_alloc`,
  `__bennett_nz_free`. **Runtime entry point**: a function with prefix `__bennett_rt_`,
  `__bennett_dev_` or `__bennett_sf_` that `bennett-runtimes` or `bennett-arith` defines in
  bitcode (§3.1).
- **Handle**: the `ptr` value a `__bennett_qalloc` or `__bennett_qborrow` call returns; it
  denotes a **register** of n qubits, the ISA's `qreg[n]` (ISA §3.3). Qubit `i` of a handle is a
  **wire**. **Register tag**: the opaque value (nonzero, below 2^pw) that represents a handle in
  device memory and in integers; at the host–device boundary a handle is an ISA launch register
  id (§6.1).
- **Root**: an allocation of a register, identified by its allocation site and dynamic instance
  index (§6.5). **Handle-derived**: a value whose provenance (§6.2) contains a root.
- **Region function**: a function a region-entry marker receives. **Region operand**: the marker
  operand that names it. **Candidate set**: the functions a region operand can denote (§7.2).
- **Action region**: a candidate of a `ctrl`, `adj` or `compute` operand; its interface is a
  quantum action (ISA §5.3). **Oracle region**: a candidate of an `oracle` or `inplace` operand;
  its interface is a lifted oracle (ISA §5.2). **Reversible region**: a candidate of a
  `reversible` operand, or the whole-program entry of §19.2; R-tier code (ISA §3.1).
- **Tier** of a function variant: **H** (host, native), **CC** (device classical control, ISA
  §3.1), **R** (reversible, ISA §3.1), **L** (lifted: an lproc or oracle body, ISA §3.7). A
  **variant** is a (function, tier, coherence signature) triple (§4.3); host code keeps the
  original function, every device tier gets a clone.
- **Device program**: every variant of tier CC, R or L. **Device entry**: a device variant
  called by an H function (a launch, ISA §10).
- **Function address** A(F): the address of F in the driver's comparison link (§4.4).
- **Abstract object**, **slot**, **value set**: §5. ⊤ is the unbounded value set.
- **Descriptor**: the in-memory oracle interface record of §8.1. **Binding**: one parameter or
  device entry of a descriptor. **Shape**: a tuple of binding kinds, modes and widths (§8.4).
- **Budget record**: the in-memory record `bennett_budget` of §9.1. **Budget table**: the driver
  input of §9.2.
- **Coherence state**: Cl (classical) or Co (coherent) of a value or object instance (§10,
  TDL-2). **Coherent slice**: an outlined maximal region of Co instructions (TDL-3).
  **Arena**: the coherent memory of §10 TDL-4. **Generation**: the classical execution of an
  action region that records its events (§18.4).
- **Device model**: one of `console`, `clock`, `entropy`, `block` (ISA §7.3), realised per tier
  by §11.
- **Coverage classes** (ISA §13): **lowered** (the construct has an ISA realisation),
  **shimmed** (it is replaced by a runtime or platform shim with a recorded `shim_hash`),
  **trapped** (it faults with code 8, `FAULT_EFFECT_UNMODELLED`, on the executions that reach it,
  and has a coverage line).
- **Driver mode**: one of the invocation modes of §19.2–§19.7. **Platform profile**: §20.
- **Materialised module**: the module after normalisation (§12). **Reference object**: the ISA
  object the map produces for one oracle shape (§16.2); its oracle `@ref` defines F_B.
- **Blocker**: a capability with no ISA 0.8 realisation in a stated case (§25.1), BLK-1 to
  BLK-4.

## 3. The marker ABI (markers 0.2)

### 3.1 Reserved names

Every function or global name that starts with `__bennett_` is reserved. The reserved names
other than the markers of §3.2 are:

| Prefix | Who defines | Who may reference it |
|---|---|---|
| `__bennett_nz_` | nobody: **primitives**, lowered by the map (§16.4) and the CC/R lowering (§17.4) | the normaliser (§12) and runtimes bitcode |
| `__bennett_sf_` | `bennett-arith` bitcode (§13) | the normaliser and runtimes bitcode |
| `__bennett_rt_` | `bennett-runtimes` bitcode (§11, §14, §17, §20); the driver's layout objects `__bennett_rt_blk.<f>` (§14.9) | the normaliser, the driver's synthesised code (§19) and runtimes bitcode |
| `__bennett_dev_` | `bennett-runtimes` bitcode: device-model entry points and device state (§11.3) | the plugin's L lowering of effect markers and runtimes bitcode |

The primitives are exactly:

```
declare void @__bennett_nz_fault(i64 %code)    ; fault with code C (§12.3)
declare ptr  @__bennett_nz_alloc(i64 %n)       ; ISA alloc / lift.alloc (§17.1)
declare void @__bennett_nz_free(ptr %p)        ; ISA free / lift.free
```

A **producer input** is a bitcode file given to the driver other than `bennett-runtimes` and
`bennett-arith` bitcode. A producer input:

1. MUST NOT define (`define`) a function whose name is a marker or a reserved name
   (`BD-E-MARKER-DEFINED`);
2. MUST NOT declare, define or reference a reserved name that is not a marker
   (`BD-E-MARKER-UNKNOWN`);
3. MUST NOT use a marker other than as the callee of a call or invoke (`BD-E-MARKER-ADDRESS`):
   no stored, compared, passed or cast marker address, so that no marker is ever called
   indirectly.

The driver checks rules 1–3 on every producer input before linking; the plugin checks rules 1
and 3 on the linked module, and, in closed-unit mode (§19.7), all three on its input. Checked
examples are producer inputs. `__bennett_ctrl_v`, the variadic probe of the spike ABI v0, is
not a marker; it is rejected by rule 2. *(non-normative)* The legality corpus's trace runtime
defines markers; it is a test harness, never a production link input (§19.9).

### 3.2 The marker list

The normative IR signatures (return type, name, parameter types; parameter names are
documentation):

```llvm markers-ir
declare ptr @__bennett_qalloc(i64 %cls, i64 %n)
declare ptr @__bennett_qborrow(i64 %cls, i64 %n)
declare void @__bennett_qfree(ptr %h)
declare void @__bennett_gate(i32 %op, ptr %h, i64 %i)
declare void @__bennett_gate2(i32 %op, ptr %a, i64 %i, ptr %b, i64 %j)
declare void @__bennett_gate3(i32 %op, ptr %a, i64 %i, ptr %b, i64 %j, ptr %c, i64 %k)
declare void @__bennett_rot(i32 %op, ptr %h, i64 %i, double %theta)
declare i1 @__bennett_measure(ptr %h, i64 %i)
declare void @__bennett_qload(ptr %dst, ptr %mem, ptr %addr)
declare void @__bennett_qstore(ptr %mem, ptr %addr, ptr %val)
declare void @__bennett_qprep(ptr %h, ptr %src, i64 %nbytes)
declare void @__bennett_observe(ptr %p, i64 %len)
declare void @__bennett_ctrl(ptr %q, i64 %qi, ptr %f, ptr %budget, ptr %env)
declare void @__bennett_adj(ptr %f, ptr %budget, ptr %env)
declare void @__bennett_compute(ptr %f, ptr %use, ptr %budget, ptr %env)
declare void @__bennett_reversible(ptr %f, ptr %budget, ptr %env)
declare void @__bennett_oracle(ptr %f, ptr %budget, ptr %desc)
declare void @__bennett_inplace(ptr %g, ptr %ginv, ptr %budget, ptr %desc)
declare void @__bennett_effect_console_write(ptr %p, i64 %len)
declare void @__bennett_effect_clock_read(ptr %p)
declare void @__bennett_effect_entropy_read(ptr %p, i64 %len)
declare void @__bennett_effect_block_read(i64 %sector, ptr %p)
declare void @__bennett_effect_block_write(i64 %sector, ptr %p)
```

Operand roles, by marker (positions are 0-based). "Dispatched" operands are classical values
whose value set (§5.3) selects among compiled alternatives (§3.4); "memory" operands point into
classical memory.

| Marker | Handle operands | Region operands (kind) | Dispatched operands | Budget | Descriptor | Other |
|---|---|---|---|---|---|---|
| `qalloc`, `qborrow` | – | – | 0 `cls`, 1 `n` | – | – | – |
| `qfree` | 0 | – | – | – | – | – |
| `gate` | 1 | – | 0 `op` | – | – | 2 index |
| `gate2` | 1, 3 | – | 0 `op` | – | – | 2, 4 indices |
| `gate3` | 1, 3, 5 | – | 0 `op` | – | – | 2, 4, 6 indices |
| `rot` | 1 | – | 0 `op` | – | – | 2 index, 3 angle |
| `measure` | 0 | – | – | – | – | 1 index |
| `qload`, `qstore` | 0, 1, 2 | – | – | – | – | – |
| `qprep` | 0 | – | – | – | – | 1 memory (source bytes), 2 byte count |
| `observe` | – | – | – | – | – | 0 memory, 1 byte count |
| `ctrl` | 0 | 2 (action) | – | 3 | – | 1 index, 4 env |
| `adj` | – | 0 (action) | – | 1 | – | 2 env |
| `compute` | – | 0, 1 (action) | – | 2 | – | 3 env |
| `reversible` | – | 0 (reversible) | – | 1 | – | 2 env |
| `oracle` | (in the descriptor) | 0 (oracle) | – | 1 | 2 | – |
| `inplace` | (in the descriptor) | 0, 1 (oracle) | – | 2 | 3 | – |
| `effect_console_write` | – | – | – | – | – | 0 memory, 1 length |
| `effect_clock_read` | – | – | – | – | – | 0 memory (8 bytes) |
| `effect_entropy_read` | – | – | – | – | – | 0 memory, 1 length |
| `effect_block_read`, `effect_block_write` | – | – | – | – | – | 0 sector, 1 memory (512 bytes) |

Changes from 0.1 and from the spike ABI v0 (`corpus/legality/markers.h`): `qalloc`, `qborrow`,
`qfree`, `gate`, `gate2`, `rot`, `measure`, `qload` and `qstore` keep their v0 signatures, so
the spike evidence applies to them unchanged; `gate3` is unchanged from 0.1; every region-entry
marker now takes a budget record (§9.1); `oracle` and `inplace` take a descriptor (§8.1) in
place of 0.1's handle operands; `qprep`, `observe` and the five effect markers are new. The
positive legality requirement (§3.6) is a property of unknown external calls, not of a
signature, but every changed or new marker gets legality corpus cases before this version
freezes (§21.2, bd `-566`).

**Meaning in brief** (the rules are in the sections named):

- `qprep(h, src, n)`: for every k < n and j < 8, wire 8k + j of h ⊕= bit j of byte `src[k]`;
  n ≤ n(h)/8 (else `T-SIZE`). A copy when h is clean; self-inverse. It is how data "fixed
  classically before entry" (NS §4.2, §8 rung 4) reaches a register (§8.5, §17.4); one `gate`
  per set bit would need about 1.3·10^8 marker calls for the rung-4 image.
- `observe(p, len)`: a computational-basis measurement of the classical bytes [p, p + len)
  whose coherence state is Co (§10, TDL-11); afterwards they are Cl and hold the outcome. It is
  the only way superposed classical memory reaches classical code (NS §4.2: "outputs leave
  through measurement after exit"). On Cl bytes it does nothing.
- the effect markers: one per ISA device-model operation (ISA §7.3), realised per tier by §11.
  `bennett-runtimes` calls them from its musl, Julia and platform shims; ordinary programs may
  call them directly.

### 3.3 C header view

`spec/bennett_markers.h` is the normative C and C++ header. Its prototypes (in C++ each carries
`noexcept`, which makes clang add `nounwind`, a permitted attribute, and emit `call` rather than
`invoke`):

```c markers-c
bennett_q __bennett_qalloc(uint64_t cls, uint64_t n) BENNETT_NOEXCEPT;
bennett_q __bennett_qborrow(uint64_t cls, uint64_t n) BENNETT_NOEXCEPT;
void __bennett_qfree(bennett_q h) BENNETT_NOEXCEPT;
void __bennett_gate(uint32_t op, bennett_q h, uint64_t i) BENNETT_NOEXCEPT;
void __bennett_gate2(uint32_t op, bennett_q a, uint64_t i, bennett_q b, uint64_t j) BENNETT_NOEXCEPT;
void __bennett_gate3(uint32_t op, bennett_q a, uint64_t i, bennett_q b, uint64_t j, bennett_q c, uint64_t k) BENNETT_NOEXCEPT;
void __bennett_rot(uint32_t op, bennett_q h, uint64_t i, double theta) BENNETT_NOEXCEPT;
bool __bennett_measure(bennett_q h, uint64_t i) BENNETT_NOEXCEPT;
void __bennett_qload(bennett_q dst, bennett_q mem, bennett_q addr) BENNETT_NOEXCEPT;
void __bennett_qstore(bennett_q mem, bennett_q addr, bennett_q val) BENNETT_NOEXCEPT;
void __bennett_qprep(bennett_q h, const void *src, uint64_t nbytes) BENNETT_NOEXCEPT;
void __bennett_observe(void *p, uint64_t len) BENNETT_NOEXCEPT;
void __bennett_ctrl(bennett_q q, uint64_t qi, bennett_region f, const bennett_budget *budget, void *env) BENNETT_NOEXCEPT;
void __bennett_adj(bennett_region f, const bennett_budget *budget, void *env) BENNETT_NOEXCEPT;
void __bennett_compute(bennett_region f, bennett_region use, const bennett_budget *budget, void *env) BENNETT_NOEXCEPT;
void __bennett_reversible(bennett_region f, const bennett_budget *budget, void *env) BENNETT_NOEXCEPT;
void __bennett_oracle(const void *f, const bennett_budget *budget, const bennett_oracle_desc *desc) BENNETT_NOEXCEPT;
void __bennett_inplace(const void *g, const void *ginv, const bennett_budget *budget, const bennett_oracle_desc *desc) BENNETT_NOEXCEPT;
void __bennett_effect_console_write(const void *p, uint64_t len) BENNETT_NOEXCEPT;
void __bennett_effect_clock_read(void *p) BENNETT_NOEXCEPT;
void __bennett_effect_entropy_read(void *p, uint64_t len) BENNETT_NOEXCEPT;
void __bennett_effect_block_read(uint64_t sector, void *p) BENNETT_NOEXCEPT;
void __bennett_effect_block_write(uint64_t sector, const void *p) BENNETT_NOEXCEPT;
```

The header also defines:

- `typedef struct bennett_q_opaque *bennett_q;` and `typedef void (*bennett_region)(void *env);`;
- `bennett_budget` (§9.1), `bennett_bind`, `bennett_devbind` and `bennett_oracle_desc` (§8.1),
  and the macros `BENNETT_ORACLE_DESC(NP, ND)`, `BENNETT_ORACLE_DESC_P(NP)` and
  `BENNETT_ORACLE_DESC_D(ND)` that declare a descriptor with NP ≥ 1 parameter bindings and ND ≥ 1
  device bindings, parameters only, or devices only;
- `bennett_oracle_desc_init(d, np, nd, tgt, fault)` and `bennett_bind_set(b, kind, mode, q,
  value, size)`, macros that set the fields by plain stores, so that producers build descriptors
  by constant stores (§8.1);
- the operation codes of §3.4 and the constants of §8 and §9.

Clang lowers C `bool` to `zeroext i1`, which §3.6 admits. The checker compiles the header with
clang 18, 20 and 23 and compares every prototype's IR signature with §3.2.

### 3.4 Operand encodings

**Operation codes** (`op`):

| Marker | Code | Operation | ISA realisation (ISA §4.4) |
|---|---|---|---|
| `gate` | 1 | X | `x` |
| `gate` | 2 | H | `h` |
| `gate` | 3 | S | `s` |
| `gate` | 4 | S† | `sdg` |
| `gate` | 5 | T | `t` |
| `gate` | 6 | T† | `tdg` |
| `gate` | 7 | Z | `s` then `s` (S² = Z exactly) |
| `gate` | 8 | Y | `sdg` then `x` then `s` (S·X·S† = Y exactly) |
| `gate2` | 1 | CX, `a` control, `b` target | `cx` |
| `gate2` | 2 | CZ | `cz` |
| `gate2` | 3 | SWAP | `swap` |
| `gate3` | 1 | CCX, `a`, `b` controls, `c` target | `ccx` |
| `rot` | 1 | RX(θ) | `rx θ` |
| `rot` | 2 | RY(θ) | `ry θ` |
| `rot` | 3 | RZ(θ) | `rz θ` |

"Then" is time order. The realisations are exact including global phase, so Z and Y stay exact
under control.

**Classes** (`cls`). `cls` = 0 denotes the ISA class `any` (ISA §4.3). `cls` = k ≥ 1 denotes
entry k (1-based) of the link's **class-name table**: the names of the module flags
`!"bennett.classes"` (behaviour `AppendUnique`, a list of strings) of every input, in order of
first appearance in the driver's link order, followed by the names given with
`--bennett-class=<name>` (§19.9) that are not already present. The driver writes the table into
the object's class references (ISA §4.3 `qalloc cls n`, §3.3 `qreg.new cls n`); a name the
target does not declare is an ISA load error (ISA §8.3 `classes`), not a dialect error.

**Width** (`n`): the number of qubits, ≥ 1. **Indices**: classical values; an index ≥ n(h)
traps (`T-INDEX`, §18.3). **Angle**: a classical `double` (soft-float bits, §13); a non-finite
angle traps (`T-THETA`).

**Constant and run-time operands.** A dispatched operand (role table, §3.2) is classical data.
Its value set VS(v) is computed by §5.3. The plugin compiles one alternative per member of the
**dispatch domain** and selects among them at run time with the compare tree of §14.2:

- `op`: the dispatch domain is VS(op) when it is finite, else the marker's whole code table.
  A run-time value outside the table traps (`T-OP`).
- `cls`: VS(cls) when finite, else {0} ∪ every index of the class-name table. A value outside
  traps (`T-CLASS`).
- `n`: VS(n) when finite (constants, `range` attributes and metadata, masks, `select`, `phi`,
  loads from constant tables, §5.3). A value 0 at run time traps (`T-SIZE`). When VS(n)
  is ⊤, ISA 0.8 has no register of run-time width: the verdict is `blocked:BD-B-ISA4` (BLK-1,
  §25.1) and the blocker report names the value.

A **constant** operand outside its table (an `op` code not in the table, a constant `cls`
beyond the class-name table, a constant `n` = 0) is `BD-E-OPERAND`: the program traps at that
marker on every execution that reaches it, so the rejection is fail-fast for an always-failing
call (§22.1). Under coherent control (a Co operand, §10 TDL-10) the same domains apply.

The `cfg-switch-op-table` shape (`default<O3>` sinks seven gate calls into one with a phi of
operation codes) is accepted, as are operation codes loaded from a constant table (SimplifyCFG's
switch-to-lookup on the `op` operand):

```llvm example=operand-phi-codes verdict=accept
define void @top(i1 %c) {
entry:
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  br i1 %c, label %a, label %b

a:
  br label %j

b:
  br label %j

j:
  %op = phi i32 [ 2, %a ], [ 7, %b ]
  call void @__bennett_gate(i32 %op, ptr %h, i64 0)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

```llvm example=operand-code-table verdict=accept
@switch.table.ops = private unnamed_addr constant [3 x i32] [i32 1, i32 2, i32 5]

define void @top(i64 %i) {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  %k = urem i64 %i, 3
  %p = getelementptr [3 x i32], ptr @switch.table.ops, i64 0, i64 %k
  %op = load i32, ptr %p
  call void @__bennett_gate(i32 %op, ptr %h, i64 0)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

A gate-list interpreter that reads its operation codes from host input is accepted: the code
is dispatched over the whole `gate` table, and a code outside it traps (`T-OP`) on that
execution only:

```llvm example=operand-runtime-op verdict=accept
define void @interp(i32 %op) {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @__bennett_gate(i32 %op, ptr %h, i64 0)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

```llvm example=operand-bad-code verdict=reject:BD-E-OPERAND
define void @top() {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @__bennett_gate(i32 99, ptr %h, i64 0)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

A class named by the module flag is entry 2 of this module's class-name table:

```llvm example=operand-class verdict=accept
define void @top() {
  %h = call ptr @__bennett_qalloc(i64 2, i64 3)
  call void @__bennett_qfree(ptr %h)
  ret void
}

!llvm.module.flags = !{!0}
!0 = !{i32 6, !"bennett.classes", !1}
!1 = !{!"fast", !"slow"}
```

A width bounded by a mask has a finite value set: `and` with 7 gives {0, …, 7} and the `add`
gives VS(%n) = {1, …, 8}; the plugin compiles one static register per member and dispatches
(§6.5). A width from host input with no bound is blocked (BLK-1):

```llvm example=operand-width-masked verdict=accept
define void @top(i64 %m) {
  %k = and i64 %m, 7
  %n = add i64 %k, 1
  %h = call ptr @__bennett_qalloc(i64 0, i64 %n)
  call void @__bennett_gate(i32 2, ptr %h, i64 0)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

```llvm example=operand-width-host verdict=blocked:BD-B-ISA4
define void @top(i64 %n) {
  %h = call ptr @__bennett_qalloc(i64 0, i64 %n)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

```text blocker=operand-width-host
BD-B-ISA4 @top %h: qalloc operand n has value set TOP (parameter of an externally visible function); ISA 0.8 qreg[n] needs a literal n; BLK-1 (ISA-4) qreg[*]
```

### 3.5 Recognition

A call or invoke instruction is a **marker call** iff its callee operand is the function itself
(not a loaded or cast value) and that function's name is exactly a marker name. Names are
compared byte for byte; no prefix, suffix or demangled match is made. A marker call is accepted
iff all of the following hold; otherwise `BD-E-MARKER-SIGNATURE`:

1. the declaration's function type is exactly the marker's IR signature, **or** is the
   unprototyped form `R (...)` with R the marker's return type (a C declaration without a
   prototype, spike case `c-unprototyped-decl`);
2. the call instruction's function type is exactly the marker's IR signature, **or**, only when
   the declaration is unprototyped, the marker's parameter list followed by `...`;
3. the call passes exactly as many arguments as the signature has parameters;
4. the calling convention is the default C convention and the call has no operand bundles.

Attributes and metadata are not part of the comparison; they are governed by §3.6.

```llvm example=recog-unprototyped verdict=accept
declare ptr @__bennett_qalloc(...)
declare void @__bennett_gate(...)
declare void @__bennett_qfree(...)

define void @kr() {
  %h = call ptr (i64, i64, ...) @__bennett_qalloc(i64 0, i64 1)
  call void (i32, ptr, i64, ...) @__bennett_gate(i32 2, ptr %h, i64 0)
  call void (ptr, ...) @__bennett_qfree(ptr %h)
  ret void
}
```

The same program passing an `int` index without a cast gives an `i32` argument and is
rejected:

```llvm example=recog-unprototyped-wrong-type verdict=reject:BD-E-MARKER-SIGNATURE
declare ptr @__bennett_qalloc(...)
declare void @__bennett_gate(...)
declare void @__bennett_qfree(...)

define void @kr() {
  %h = call ptr (i64, i64, ...) @__bennett_qalloc(i64 0, i64 1)
  call void (i32, ptr, i32, ...) @__bennett_gate(i32 2, ptr %h, i32 0)
  call void (ptr, ...) @__bennett_qfree(ptr %h)
  ret void
}
```

```llvm example=recog-measure-i8 verdict=reject:BD-E-MARKER-SIGNATURE
declare i8 @__bennett_measure(ptr, i64)

define i8 @m() {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  %b = call i8 @__bennett_measure(ptr %h, i64 0)
  call void @__bennett_qfree(ptr %h)
  ret i8 %b
}
```

A 0.1-style `ctrl` with an `i64` budget no longer has the marker's signature:

```llvm example=recog-ctrl-01 verdict=reject:BD-E-MARKER-SIGNATURE
declare void @__bennett_ctrl(ptr, i64, ptr, i64, ptr)

define internal void @body(ptr %e) {
  ret void
}

define void @top(ptr %e) {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @__bennett_ctrl(ptr %h, i64 0, ptr @body, i64 -1, ptr %e)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

```llvm example=recog-ctrl-v verdict=reject:BD-E-MARKER-UNKNOWN
declare void @__bennett_ctrl_v(ptr, i64, ptr, i64, ...)

define void @v(ptr %e) {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void (ptr, i64, ptr, i64, ...) @__bennett_ctrl_v(ptr %h, i64 0, ptr null, i64 8, i32 1)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

```llvm example=recog-address-taken verdict=reject:BD-E-MARKER-ADDRESS
@table = global ptr @__bennett_gate
```

```llvm example=recog-defined verdict=reject:BD-E-MARKER-DEFINED
define void @__bennett_qfree(ptr %h) {
  ret void
}
```

A producer input may not reference a runtime entry point:

```llvm example=recog-runtime-name verdict=reject:BD-E-MARKER-UNKNOWN
declare void @__bennett_rt_memmove(ptr, ptr, i64)

define void @f(ptr %d, ptr %s) {
  call void @__bennett_rt_memmove(ptr %d, ptr %s, i64 8)
  ret void
}
```

### 3.6 The positive legality requirement and attributes

A marker is an external declaration that may read and write any memory, may unwind and may not
return: exactly an unknown external function to LLVM. Stock passes then preserve the dynamic
sequence of marker calls on every executed path (spike findings §1: every standard pipeline of
LLVM 18, 20 and 23, all 50 legal cases; the four negative controls are detected). No attribute
is needed and none may be added that licenses elimination, commoning, speculation or motion.

Every attribute, keyword and calling convention on a marker declaration or marker call site is
in exactly one of three lists:

- **Forbidden** (`BD-E-MARKER-ATTRIBUTE`): attributes that license motion or elimination:
  `memory(...)` in any form, `readnone`, `readonly`, `writeonly`, `argmemonly`,
  `inaccessiblememonly`, `inaccessiblemem_or_argmemonly`, `willreturn`, `speculatable`,
  `noreturn`, `returned`, `nocapture`, `captures(...)`, `dereferenceable(...)`,
  `dereferenceable_or_null(...)`, `align`, `nofpclass(...)`, `byval`, `sret`, `writable`,
  `initializes(...)`, `dead_on_unwind`, `nosync`, `nofree`, `norecurse`, `mustprogress`,
  `musttail`, any non-default calling convention, `extern_weak` linkage. *(non-normative)* The
  first eight are the spike's L2 forbidden set; `noreturn` would delete the code after a marker;
  `returned` would replace a marker result by an argument; the parameter-effect attributes would
  let LLVM move stores to an environment across a region call; `dereferenceable` would let it
  speculate loads through a handle.
- **Benign** (ignored): function position `nounwind`, `nonlazybind`, `uwtable` (any form),
  `strictfp`, `cold`, `hot`, `nomerge`, `noinline`, `convergent`, `builtin`, `nobuiltin`,
  `optsize`, `minsize`, `optnone`, and every string attribute; return and parameter position
  `noundef`, `nonnull`, `range(...)`, `zeroext`, `signext`; declaration linkage and keywords
  external linkage, `dso_local`, `dso_preemptable`, `unnamed_addr`, `local_unnamed_addr`, any
  visibility; call-site keywords `tail`, `notail`; instruction metadata of any kind. The first
  group is the spike's L2 evidence (findings §1, §4: front ends add `nounwind`, `nonlazybind`,
  `uwtable`, `noundef`, `nonnull`, `zeroext` and string attributes; passes add
  `local_unnamed_addr`, `nonnull`, `noundef`, `range`, `tail`). `strictfp` through `optnone`
  are added by build flags NS §0 allows (`-ffp-model=strict`, `-Os`, `-O0`) or restrict
  motion; none licenses elimination, commoning, speculation or motion of an unknown call.
  Before this version freezes, a corpus run confirms each of them on the three majors (§21.2,
  bd `.21`).
- **Unknown**: every other attribute is `BD-E-MARKER-ATTRIBUTE` until corpus evidence moves it
  to one of the lists above with a version change. This is required by NS §3.1 (the positive
  legality requirement: an attribute the dialect has not classified may license motion).

Attribute groups (`#N`) are resolved before the check.

```llvm example=attr-rust-style verdict=accept
declare ptr @__bennett_qalloc(i64 noundef, i64 noundef) unnamed_addr #0
declare void @__bennett_gate(i32 noundef, ptr noundef, i64 noundef) unnamed_addr #0
declare void @__bennett_qfree(ptr noundef) unnamed_addr #0

define void @prep() unnamed_addr #1 {
  %h = tail call noundef nonnull ptr @__bennett_qalloc(i64 noundef 0, i64 noundef 1) #2
  tail call void @__bennett_gate(i32 noundef 2, ptr noundef nonnull %h, i64 noundef 0) #2
  tail call void @__bennett_qfree(ptr noundef nonnull %h) #2
  ret void
}

attributes #0 = { nounwind nonlazybind uwtable "probe-stack"="inline-asm" "target-cpu"="x86-64" }
attributes #1 = { nounwind nonlazybind uwtable }
attributes #2 = { nounwind }
```

Call sites under `-ffp-model=strict` carry `strictfp`; a `cold` declaration is benign too:

```llvm example=attr-strictfp-cold verdict=accept
declare void @__bennett_rot(i32, ptr, i64, double) #0

define void @r(double %t) #1 {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @__bennett_rot(i32 3, ptr %h, i64 0, double %t) #1
  call void @__bennett_qfree(ptr %h)
  ret void
}

attributes #0 = { cold nounwind }
attributes #1 = { strictfp }
```

```llvm example=attr-memory-none verdict=reject:BD-E-MARKER-ATTRIBUTE
declare void @__bennett_gate(i32, ptr, i64) #0

define void @g() {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  call void @__bennett_qfree(ptr %h)
  ret void
}

attributes #0 = { nounwind willreturn memory(none) }
```

```llvm example=attr-callsite-read verdict=reject:BD-E-MARKER-ATTRIBUTE
define void @g() {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @__bennett_gate(i32 1, ptr %h, i64 0) #0
  call void @__bennett_qfree(ptr %h)
  ret void
}

attributes #0 = { memory(read) }
```

### 3.7 Unwinding of markers

Markers never unwind. Before any other analysis (§4.1 step S1) the plugin rewrites every
`invoke` of a marker into a `call` with the same operands followed by `br label %normal`,
removes the invoking block from the phi nodes of the unwind destination, and then deletes every
block not reachable from the function's entry. *(non-normative)* This is Enzyme's practice
(enzyme survey §1.1); C++ with `-fexceptions` and Rust `extern "C-unwind"` produce such invokes
(emission summary item 3). Front ends SHOULD declare markers non-unwinding (`noexcept`, Rust
`extern "C"`). Unwinding through every other call of device code is the explicit-propagation
transform of §14.4; 0.1's `BD-E-EH` is deleted.

```llvm example=unwind-invoke verdict=accept
declare i32 @__gxx_personality_v0(...)

define void @eh() personality ptr @__gxx_personality_v0 {
entry:
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  invoke void @__bennett_gate(i32 2, ptr %h, i64 0)
          to label %ok unwind label %lp

ok:
  call void @__bennett_qfree(ptr %h)
  ret void

lp:
  %e = landingpad { ptr, i32 } cleanup
  resume { ptr, i32 } %e
}
```

### 3.8 Front-end emission routes

- **clang (C, C++)** and **rustc** emit markers as direct calls to the declaration (emission
  summary). Rust MUST declare each marker with one ABI per crate (`extern "C"`); mixed
  `"C"`/`"C-unwind"` declarations are merged by rustc into one declaration with `invoke` call
  sites, which §3.7 accepts.
- **Julia** MUST emit markers with `ccall("extern __bennett_<name>", llvmcall, …)` or with
  `Base.llvmcall((module_ir, "entry"), …)` whose module contains the `declare`. Both give a
  direct call to an attribute-free declaration; `ccall("extern __bennett_measure", llvmcall,
  Bool, …)` gives `declare i1 @__bennett_measure(ptr, i64)`, exactly the §3.2 signature
  (verified with Julia 1.13.3). A plain `ccall(:__bennett_x, …)` or `@ccall` is an indirect call
  through a `jlplt` GOT global and is not a marker call. The plugin MUST reject a module
  containing a global variable whose name matches `jlplt___bennett_<name>_<digits>_got` or that
  carries the attribute `"julia.fname"="__bennett_<name>"` (`BD-E-JULIA-CCALL`), so that this
  mistake fails at compile time instead of at a lazy binding at run time; the `llvmcall` route
  keeps the full capability (audit B-13, L).
- **Region functions** are passed as `ptr @f` or as any value whose value set §7.2 resolves.
  Bennett.jl emits `ptr @f` in its own module (LLVM.jl), which keeps the full capability (audit
  B-14). A Julia `@cfunction` pointer is an `inttoptr` constant of an address of the Julia
  process; like every region pointer with value set ⊤ it is dispatched by value against the
  address-taken functions of the required type (§7.2), and an execution on which it equals no
  A(F) traps (`T-REGION`).
- **Descriptors and budget records** are built by plain stores into an `alloca` or global
  (C: the header macros; Rust: `#[repr(C)]` structs; Julia: `Ref` of an `isbits` struct), which
  survive `default<O3>` as constant stores that §5.3 reads (corpus cases, §21.2).
- **Source effect lies** (spike F5). A device function definition carrying any of
  `memory(none)`, `memory(read)` (any `memory(...)` whose effects exclude a write to any
  location), `readnone`, `readonly`, `willreturn` or `speculatable`, from which a marker call is
  reachable through the call graph of §4.1 (the function itself included), is
  `BD-E-EFFECT-LIE`. *(non-normative)* LLVM cannot infer these attributes for a function that
  reaches an unknown external call, so they come from the source; the front end's own optimiser
  may already have deleted marker calls on their strength, which is why this is a diagnostic and
  not a guarantee (definedness assumption, NS §3.2).

```llvm example=julia-jlplt verdict=reject:BD-E-JULIA-CCALL
@jlplt___bennett_gate_528_got = external global ptr #0

define void @j(ptr %h) {
  %f = load atomic ptr, ptr @jlplt___bennett_gate_528_got unordered, align 8
  call void %f(i32 1, ptr %h, i64 2)
  ret void
}

attributes #0 = { "julia.fname"="__bennett_gate" "julia.libidx"="0" }
```

```llvm example=effect-lie verdict=reject:BD-E-EFFECT-LIE
define internal void @kick(ptr %h) #0 {
  call void @__bennett_gate(i32 2, ptr %h, i64 0)
  ret void
}

define void @top() {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @kick(ptr %h)
  call void @__bennett_qfree(ptr %h)
  ret void
}

attributes #0 = { willreturn }
```

## 4. Processing order, device program, tiers, variants, function addresses

### 4.1 Processing order

A plugin processes the whole-program module (after the driver's link and post-link pipeline,
§19.1) in this order; the first failing rule gives the verdict (§1.6):

| Step | Rules |
|---|---|
| S1 | §3.1 reserved names; §3.5 recognition; §3.6 attributes; §3.8 Julia check; §3.7 marker invokes; §3.8 effect lies; §19.9 version checks |
| S2 | the device analysis (§5): one fixpoint for points-to, value sets, region candidates (§7.2), indirect-call candidates (§14.2), handle provenance (§6.2) and descriptor kinds (§8.4) |
| S3 | tier assignment and variants (§4.2–§4.4); calls out of the device program (§4.5) |
| S4 | handle rules (§6) |
| S5 | region well-formedness (§7.5) |
| S6 | the TDL partition and the may-Co analysis (§10) |
| S7 | normalisation of every device variant (§12) and the residual-poison validator (§12.4); dispatch domains (§3.4) |
| S8 | lifting (§16) of every oracle shape and coherent slice; in-place verification (§8.7) |
| S9 | lowering to ISA objects (§17; plugin-defined, constrained by §18.7); blocker reports (§25.1) |

Within a step, rules apply in the order listed; within a rule, to instructions in module text
order. Blocker reports are collected during S2–S8 and issued in S9 in that order.

The **call graph** has an edge F → G when F contains a direct `call` or `invoke` of G (after
resolving aliases), an edge F → R for every candidate R of every region operand of a marker
call in F (a **region edge**), and an edge F → C for every candidate C of every indirect call in
F (§14.2). Only functions with a definition are nodes. The **closure** of a function is the set
of functions reachable from it by direct and indirect-candidate edges (region edges start a new
region and are not followed).

### 4.2 Tier assignment

Every defined function reachable from the program's roots gets a set of tiers. The **host
roots** are the functions with non-local linkage and the functions whose address host code
uses; the **device roots** are the region candidates and the whole-program entry of §19.2.

- **CC**: a function that contains a marker call, receives a handle (a parameter or a loaded
  value whose provenance contains a root, §6.2), is a candidate of an action region operand
  (its classical part is the generation, §18.4), is a device entry, is in the CC closure of
  one of these, or is promoted by §19.4.
- **R**: a function in the closure of a `reversible` region operand, or every function under
  `--bennett-tier=reversible` (§19.2).
- **L**: a function in the closure of an oracle or in-place region operand, or of a coherent
  slice (§10, TDL-3).
- **H**: every other function reachable from a host root, and every function reachable from a
  host root through host code only. A function in no device tier stays H only.

A function may get several tiers; it then has one variant per tier (§4.3). *(non-normative)*
SQLite in the rung-4 program is H (the host builds and serialises the database) and L (the
oracle runs the query), so it has two variants and one set of globals (SQLite §5.2(i)).

### 4.3 Polyvariant cloning

A **variant** is a (function, tier, coherence signature) triple, where the coherence signature
is the tuple of coherence states of the function's parameters and of the may-Co objects it
reads (§10, TDL-2) and is empty outside TDL. The H variant is the original function; every
device variant is a clone. **Clones share every global: data is never cloned.** There is one
classical memory (NS §3.2), shared by H, CC, R and the entry state of every L invocation
(§8.5). Calls inside a variant call the variant of the callee with the caller's tier and the
coherence signature at the call. 0.1's `BD-E-DEVICE-ADDRESS` is deleted: a host function may
take the address of any function (audit B-16).

### 4.4 Function addresses

Every function whose address is used has the **function address** A(F): its address in the
driver's **comparison link** (§19.5: non-PIE, fixed section addresses, identical-code folding and
constant merging off; NS §3.2, SQLite §5.2(ii)). A(F) is the value of `ptr @F` in every tier:

- in host code, by linking the production host image with the comparison layout whenever an
  address may cross the host–device boundary (§19.5);
- in CC and R code, as `const` plus `inttoptr` (ISA §4.1);
- in lifted code, as `lift.const` (ISA §4.2);
- in every data image: global initialisers, vtables, function tables (SQLite's `aBuiltinFunc`,
  VFS and pcache method tables).

So `ptrtoint`, comparison, hashing and storage of function pointers equal native execution.
Each tier maps A(F) to its own variant of F by the dispatch of §14.2. Two functions never have
equal A(F) (identical-code folding is off), so the map is well defined. A `blockaddress`
constant is §14.9.

### 4.5 Calls out of the device program

A call in a device variant of a function with no definition resolves, in this order:

1. a marker (§3.2) or a primitive (§3.1);
2. a **runtime shim**: a definition of the symbol in `bennett-runtimes` or `bennett-arith`
   bitcode, which the driver links before S2 (§19.1): libc and libm (musl-derived), libpthread
   with one thread, the Julia shim runtime, Rust's `core::panicking::*` targets and the platform
   shims of §20. The shim is an ordinary device function (coverage class `shimmed`, with its
   `shim_hash`, ISA §13);
3. in a CC variant only, a **host call** through `hostcall` (§11.4);
4. otherwise **trapped**: the call is replaced by F(8) (§12.3) and the coverage report has a
   `trapped` line for it (NS §3.3: "Calls with no bitcode are coverage-report lines (*trapped*),
   never silent").

An R or L variant never makes a host call (ISA §4.1: `hostcall` is CC only; NS §4.2: coherent
regions are closed). *(non-normative)* Item 4 is the only fault the dialect introduces for a
call, and it occurs only on the executions that reach the call; it is the north star's own rule.

## 5. The device analysis (one fixpoint)

The device analysis is a whole-program, flow-insensitive, inclusion-based (Andersen-style),
field-sensitive points-to and value-set analysis over every device variant and every host
function that exchanges data with one (passes it a pointer, or shares a global it accesses). It
is specified exactly: **every verdict, candidate set and dispatch domain of this document is
computed from the reference analysis below.** A plugin MAY use a more precise analysis to shrink
dispatch domains or arena placement in its lowering, never to change a verdict (the run-time
value is always a member of the reference set, so the results are unchanged).

### 5.1 Abstract objects and atoms

The **abstract objects** are:

- each `alloca` instruction;
- each global variable;
- each **allocation site**: a call of a function that carries `allockind("alloc")` or
  `allocsize(...)`, or whose name is one of `malloc`, `calloc`, `realloc`, `aligned_alloc`,
  `posix_memalign` (the object is the one written through its first argument), `memalign`,
  `strdup`, `strndup`, `_Znwm`, `_Znam`, `_ZnwmRKSt9nothrow_t`, `_ZnamRKSt9nothrow_t`,
  `_ZnwmSt11align_val_t`, `_ZnamSt11align_val_t`, `__rust_alloc`, `__rust_alloc_zeroed`,
  `__rust_realloc`, `julia.gc_alloc_obj`, `ijl_gc_alloc_typed`, `jl_gc_alloc`,
  `ijl_gc_small_alloc`, `ijl_gc_big_alloc`, or `__bennett_nz_alloc`;
- the pseudo-object `EXT` (memory of unknown provenance: host memory reached through a pointer
  the analysis did not create).

Heap objects are context-insensitive: one object per allocation-site instruction of the variant
in which it occurs. The list above is the reference list; `bennett-runtimes` declares its
allocator entry points with `allockind("alloc")` so that they are covered by the first rule.

An **offset** is an integer byte offset, a **residue class** (r mod s)[lo, hi) with s ≥ 2 (every
offset o with o ≡ r (mod s) and lo ≤ o < hi), or `*` (any offset). An **atom** is one of:

- `(X, o)`: a pointer into object X at offset o;
- `FN(F)`: the address A(F) of a defined function F;
- `ROOT(r)`: a handle with root r (the allocation site of a `qalloc`/`qborrow` call, §6.5);
- `INT(c)`: the integer constant c (of the value's width).

Every SSA value v (per lane for vectors, per index path for aggregates) has an **abstract
value** AV(v) = (A, t): a finite set A of atoms and a flag t; t = ⊤ means "and any other integer
or address". ⊤ never stands for a `ROOT` atom (handle provenance is always explicit); for a
function-pointer operand it stands for "any function of the operand's type whose address is
used" (§7.2, §14.2). Every slot (X, o) of memory has a content AV(X, o) of the same form. When A
holds more than **K = 4096** `INT` atoms they are dropped and t is set (a normative constant: it
decides dispatch and blocker verdicts, so §24 does not defer it). "AV(v) = ⊤" below means t is
set; unions and inclusions are taken component-wise.

### 5.2 Rules

The analysis is the least fixpoint of the following rules over AV. "Copies" means AV(result) ⊇
AV(operand) lane by lane; ⊤ absorbs.

| Rule | Instruction or source | Effect |
|---|---|---|
| PT1 | `alloca`, global `@G`, allocation-site call | AV ∋ (X, 0) |
| PT2 | `getelementptr T, ptr p, idx…` | for each (X, o) ∈ AV(p), indices in order: a constant index adds its byte offset under the datalayout (to an exact offset, or to r, lo and hi of a class); a non-constant index with element size s into an array type `[N x E]` that starts at byte offset b of the indexed position turns the offset into the class (b mod s)[b, b + N·s), and into (b mod s)[lo′, hi′) with the union of the extents if it is already a class with the same s; a non-constant index of the GEP's first (pointer) operand, or into a class with a different stride s′, gives (o mod gcd(s, s′)) over the whole object; a class with stride 1 is `*`; `*` stays `*` |
| PT3 | `phi`, `select` (value operands), `freeze`, `bitcast`, `addrspacecast` | copies (union) |
| PT4 | `ptrtoint`, `inttoptr`, `zext`/`sext`/`trunc` of a pointer-width integer to pointer width | copies |
| PT5 | `add`/`sub` of a value with pointer atoms and an `INT` set | shifts each pointer atom's offset by each constant (classes and `*` stay); any other integer operation on a pointer atom gives (X, `*`) for each X; on finite `INT` sets, every LLVM integer operation, cast and `icmp` is evaluated elementwise; with x ⊤ and a constant m, `and x, m` gives the submasks of m and `urem x, m` gives {0, …, m−1} (each still subject to K); a `range(lo, hi)` attribute or `!range` metadata (read before N3 removes it) restricts ⊤ to [lo, hi) |
| PT6 | `load T, ptr p` | for each (X, o) ∈ AV(p): the union of AV(X, o′) over the slots o′ that overlap [o, o + size(T)); for a global X declared `constant`, the atoms of its initialiser at those offsets (`FN(F)` for `ptr @F`, `(G, c)` for a pointer into G, `INT(c)` for integers); for X = EXT, ⊤ |
| PT7 | `store v, ptr p` | AV(X, o + d_k) ⊇ AV(v_k) for each (X, o) ∈ AV(p) and each lane or field k at byte offset d_k |
| PT8 | memory copy (`llvm.memcpy`/`memmove`/`memcpy.inline`, `__bennett_rt_memmove`) of (dst, src, len); memory fill (`llvm.memset`, `__bennett_rt_memset`) of (dst, v, len) | copy: for each slot (Y, s) of each (Y, o_s) ∈ AV(src) and (Z, o_d) ∈ AV(dst): when the offsets and len are constants and [s, s + 1) lies in the copied range, AV(Z, o_d + s − o_s) ⊇ AV(Y, s); else AV(Z, `*`) ⊇ AV(Y, s). Fill: every slot in [o_d, o_d + len) of each (Z, o_d) ∈ AV(dst) (all of Z when an offset or len is not constant) gets the `INT` atoms of the byte v repeated to the slot's width (⊤ when v is not constant) |
| PT9 | direct call of G, or indirect call with candidate G (§14.2) | AV(parameter i of G) ⊇ AV(argument i); AV(result) ⊇ the union of AV over G's `ret` operands; `byval` arguments copy the pointee's slots into the callee's copy object |
| PT10 | `insertelement`/`extractelement`/`shufflevector`/`insertvalue`/`extractvalue` | atoms move with constant lanes and index paths; a non-constant lane index moves the union of all lanes (a handle-table read, audit B-23) |
| PT11 | a parameter of a function with a host caller, a device entry, or a function whose address host code uses | AV ⊇ {(EXT, `*`)} for `ptr` parameters, ⊤ for integer parameters, plus the atoms of the device-side arguments by PT9; for a pointer parameter i of a device entry E, also the candidate atom ROOT(E, i) of §6.6 |
| PT12 | a `qalloc`/`qborrow` call; a call of a function with no definition that resolves to a host call (§4.5) or is trapped; an `atomicrmw`/`cmpxchg` (before N9) | `qalloc`/`qborrow`: AV ∋ ROOT(site) (§6.5). An undefined callee: the result is ⊤ and every slot reachable from its pointer arguments gets ⊤. `atomicrmw`/`cmpxchg`: a load plus a store (PT6, PT7) |

An `inttoptr` of a constant gives (EXT, `*`) and, for function-pointer purposes, ⊤: function
addresses are symbolic `FN` atoms during the analysis, and their numeric values A(F) are fixed
only by the comparison link (§19.5), after normalisation (S7) and before lifting (S8).

### 5.3 Value sets

The **value set** VS(v) of an integer or pointer operand is the set of its `INT` and `FN` atoms
(pointer atoms denote addresses that are not compile-time constants and make VS(v) = ⊤ for
dispatch purposes), or ⊤. A value set is a precision tool only:

- an operand with a finite VS is dispatched over it (§3.4, §14.2);
- an operand with VS = ⊤ is dispatched over its type's whole valid domain where that domain is
  finite: operation codes and classes (§3.4), binding kinds (§8.4), the function addresses of a
  type (§7.2, §14.2);
- otherwise it is a blocker case of §25.1: widths (BLK-1), budgets computed on the device
  (BLK-2), parameters of in-place pairs (BLK-3).

### 5.4 Uses

| Result | Read by |
|---|---|
| `FN` atoms of region operands | region candidate sets (§7.2) |
| `FN` atoms of indirect callees | indirect-call candidate sets (§14.2) |
| `ROOT` atoms | handle provenance (§6.2), handle containment (§6.4), static register files (§6.5) |
| `INT` atoms of descriptor and budget fields | descriptor shapes (§8.4), budget pre-minting (§9.5) |
| slots stored under control | the may-Co analysis and arena placement (§10, TDL-2, TDL-4) |
| objects loaded by L code | the oracle read set R and entry-state transfer (§8.5) |
| `INT` atoms of `op`, `cls`, `n` | dispatch domains (§3.4) |

```llvm example=pt-variable-index verdict=accept
%struct.tab = type { [4 x ptr], i64 }

define void @t(i64 %i) {
  %s = alloca %struct.tab
  %h0 = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h0, ptr %s
  %pn = getelementptr %struct.tab, ptr %s, i64 0, i32 1
  store i64 3, ptr %pn
  %k = and i64 %i, 3
  %pk = getelementptr %struct.tab, ptr %s, i64 0, i32 0, i64 %k
  %hk = load ptr, ptr %pk
  call void @__bennett_gate(i32 1, ptr %hk, i64 0)
  %n = load i64, ptr %pn
  %n2 = add i64 %n, 1
  store i64 %n2, ptr %pn
  call void @__bennett_qfree(ptr %h0)
  ret void
}
```

*(non-normative)* In `pt-variable-index`, `%pk` has the offset class (0 mod 8)[0, 32) in `%s`
(the `[4 x ptr]` array), so the load `%hk` reads the slots 0, 8, 16, 24: AV(`%hk`) =
{ROOT(`%h0`)}. The count field is at the exact offset 32, outside the class, so AV(`%n`) holds
INT(3) and, through the store of `%n2`, INT(4), INT(5), … until it exceeds K and becomes ⊤; it
holds no `ROOT` atom, and the arithmetic on it is legal (audit B-27: 0.1 gave the load offset `*`
and rejected this program).

## 6. Handles (handles 0.2)

### 6.1 Representation

A handle is an ordinary `ptr` in address space 0. In device memory and in integers a handle is
its **register tag**: an opaque value below 2^pw that the plugin assigns to each root (§6.5),
nonzero and distinct from the tag of every other live handle. ISA 0.8 has no instruction that
reads a `qreg`'s launch id (BLK-1's `qreg.id` would add one), so tags are the plugin's. At the
host–device boundary a handle is the ISA launch register id (`bennett_qreg`, ISA §10), which the
launch binds to a `qreg` parameter or result (§6.6). Neither value may influence a result other
than through §6.3; the rules below make them unobservable. A handle
denotes a register of n wires, n the `qalloc` operand; wire i of handle h is written h.i.

### 6.2 Provenance (maintainer decision 2)

The **provenance** of a value is the set of `ROOT` atoms of its abstract value (§5). Provenance
flows through **bitwise copies** only: `ptrtoint`/`inttoptr` at width pw, integer loads and
stores of width pw, vector lanes (including dynamic lanes, PT10: a dynamically indexed vector of
handles is a handle table), aggregate fields, memory copies, `phi`, `select`, `freeze`, call
arguments and returns (PT3–PT10). A handle-derived value (any lane or field) MAY be:

1. a handle operand of a marker (§3.2);
2. copied by the rules above, including storage in any slot the analysis tracks (§6.4);
3. an operand of `icmp eq` or `icmp ne` (§6.3);
4. an argument of a direct or indirect call of a defined function, or a return value.

Every other use is `BD-E-HANDLE-USE` (maintainer decision 2: "any other use of a
handle-derived integer is rejected fail-loud"; NS §3.1 "never dereferenced"): in particular
arithmetic, bitwise operations, `icmp` with any other predicate, any cast other than the copies
above (`trunc`, `zext`, `sext`, `bitcast` to a non-pointer-width type, `ptrtoint` to a width ≠
pw), `getelementptr` with a handle as base or index, `switch` on it, use as the pointer operand of
a `load`, `store`, `atomicrmw`, `cmpxchg` or memory intrinsic (dereference), and a load of any
type whose byte range overlaps a handle-derived slot without being exactly one pw-wide lane of
it (a partial read).

A handle operand of a marker whose provenance is empty is `BD-E-HANDLE-UNTRACKED` (it cannot be
a handle of this program). *(non-normative)* A tracked value that at run time is not a live
handle (a stale copy, a freed register) traps at the marker (`T-DEAD`, §18.3).

### 6.3 Comparison (maintainer decision 4)

`icmp eq` and `icmp ne` of a handle with `null`, or with another handle-derived value, compare
**identity**: a live handle is never null, and two handles are equal iff they denote the same
register. The result is not handle-derived. In CC it lowers to `icmp` on register tags. This
covers C `if (!q)` and Rust's `Option<Handle>` niche (audit D8). *(non-normative)* A comparison
is a classical observation of identity, not of the register's content; ids are unique, so it
equals the native comparison of the two handle values.

### 6.4 Collections and containment

Handles may be stored in any slot the analysis tracks: tables, vectors, linked structures,
globals (field-sensitively), heap objects, and objects passed to indirect calls or returned by
address-taken functions (audit B-22, B-24, B-26, B-29). A handle may **escape** only where code
the analysis cannot see could read it:

- `BD-E-HANDLE-ESCAPE`: a `ROOT` atom reaches a slot of `EXT`, an argument or a reachable slot of
  a call that resolves to a host call or is trapped (§4.5), or the return value of a function
  whose callers are not all in the link, other than a device entry's `QREG` result (§6.6). NS §3.1: "any handle use that survives into host native
  code is rejected".

H functions in the link that receive launch register ids through §6.6 are analysed like device code:
they may copy, store, compare and pass them back to device entries (§6.2 items 2–4); any other
use is `BD-E-HANDLE-USE`.

### 6.5 Realisation on ISA 0.8: static register files

ISA 0.8 has no instruction that stores, loads or converts a `qreg` (ISA §3.2, §3.3, §4.1), and
`qreg[n]` types have literal widths. CC code holds `qreg` values in its classical environment
(dynamic SSA instances, block parameters, call arguments and results; ISA §3.2, §7.4). The plugin
realises each allocation site s (a `qalloc` or `qborrow` call) in one of two ways:

- **Direct.** If no `ROOT(s)` atom reaches a memory slot (PT7, PT8), the handle is a CC `qreg`
  value threaded through SSA values, block parameters, call arguments and results ("register-
  environment passing"; §25.2 records that ISA §3.3's transition table should name CC `call`,
  `ret` and `br` operands of `qreg` type). Every execution of s creates a new dynamic instance,
  so loops and recursion need no bound.
- **Static register file.** Otherwise a **root** is a pair (s, instance index k < N(s)). For
  each root the plugin keeps one CC `qreg` variable, threaded like a direct handle through every
  CC variant that may use it; `qalloc` at s picks a free instance index at run time and executes
  `qreg.new cls n` into that variable (one variable per member of the width dispatch domain,
  §3.4); the value stored in memory is the root's register tag (§6.1). A marker operand whose
  provenance holds several roots is dispatched by comparing its tag with the tags of the live
  candidate roots (compare tree, §14.2). A direct handle that is converted to an integer
  (`ptrtoint`, a store) gets a tag in the same way.

**Reference instance bound** of a site s in function F with a static register file:

1. s is **self-disjoint** iff the only memory its `ROOT(s)` atom reaches is allocas of F whose
   address does not escape F (it is not stored, returned, or passed to a call other than a marker
   call, which includes the `env` of a region-entry marker), and every CFG path of F from s to a `ret`, to s again, or to a call
   whose callee may reach F through the call graph passes through a `qfree` whose operand's
   provenance is exactly {s}. Then N(s) = 1.
2. Otherwise N(s) = E(s), the bound on executions of s per device-entry call: E(s) = TC(s) ×
   Σ_c E(c) over the device call sites c of F (E = 1 for a device entry), where TC(s) is the
   product of the constant maximum trip counts of the loops of F that contain s (LLVM's
   `ScalarEvolution::getSmallConstantMaxTripCount` on the materialised module of the major in
   use), and E(s) = ∞ when a containing loop has no constant maximum trip count or F is in a
   cycle of the call graph.
3. If N(s) = ∞, every execution of s is a **blocker point** of BLK-1 (`blocked:BD-B-ISA4`,
   §25.1): ISA 0.8 cannot name an unbounded number of registers reached through memory. The
   plugin compiles the program with a static file of `--bennett-qreg-instances` instances
   (default 64, §24) and a blocker trap (§25.1) on an execution that needs more.

A width with VS = ⊤ is BLK-1 likewise (§3.4). In R code, which cannot allocate registers on ISA
0.8, §7.5(b) applies.

### 6.6 Host–device boundary

A device entry's parameters and results of handle type bind to launch `QREG` arguments and
results (ISA §10). A `ptr` parameter of a device entry is a **handle parameter** iff its
candidate atom `ROOT(E, i)` (added by PT11 to every pointer parameter of every device entry)
reaches a marker handle operand; otherwise the candidate atom is removed before §6.2 is checked.
A handle parameter binds to `QREG`; host code may copy, store and compare launch register ids and pass
them back. Leak checking happens at program end and at `bennett_qreg_free`, not at each
device-entry return, which gives the REPL's lexical lifetime (NS §5; audit B-30). *(non-normative)*
A register returned to the host stays live across launches until the host frees it or a
`measure` consumes it (ISA §10: "register ids created by the run remain valid unless measured
or freed").

### 6.7 Copy, XOR and in-place rules

Copying a handle copies a reference. Quantum data moves only by:

- `qload(dst, mem, addr)`: XOR of cell `addr` of `mem` into `dst` (§18.3); a copy when `dst` is
  clean, the source preserved;
- `qstore(mem, addr, val)`: XOR of `val` into cell `addr` of `mem` (ISA `qstore`), whatever `mem`
  holds;
- `qprep(h, src, n)`: XOR of classical bytes into `h` (§3.2);
- `inplace(g, ginv, budget, desc)`: x ← g(x), admitted only under §8.7;
- `oracle(f, budget, desc)`: targets ⊕= outputs, fault ⊕= code, inputs preserved (§8).

The north star's compile-time rule "a store into a register not known to be clean is an error"
(NS §3.1) is the optional warning **`BD-W-QSTORE-UNCLEAN`**: under `-bennett-warn-qstore`, the
plugin warns at every `qstore` whose target is not provably clean (no event since its `qalloc`
other than a `qstore` of the same `addr` and `val`). The warning never changes the verdict, so
the uncomputing second store stays legal (§1.4).

### 6.8 Handle → wire obligations

The plugin converts handles to ISA wires (ISA §3.3 linear values) when it lowers. Its
obligations, each a property of every ISA object it emits (ISA suite F), are: every gate's wires
pairwise distinct; no wire used after its release; every `qalloc`ed bundle released by an
explicit `qfree` (ISA §5.1); every control context disjoint from the operands it controls (ISA
§3.3); the uncomputation-validity discipline of ISA §6 for every value it introduces. Where an
obligation depends on run-time data, the reference semantics checks it dynamically and the plugin
MUST include the same check (§18.3 traps `T-ALIAS`, `T-DEAD`, `T-LEAK`, `T-CTRL`); `T-CLEAN` is
checked as ISA `qreg.free` cleanliness is: by simulating executors, with hardware following ISA
§17 item 14.

### 6.9 Examples

The spike F1 shape (an 8-byte `memcpy` of a handle turned into `ptrtoint`, `store i64`, `load
i64`, `inttoptr`):

```llvm example=handle-int-roundtrip verdict=accept candidates=rg
define internal void @rg(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  ret void
}

define void @top() {
  %e = alloca i64
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  %c = ptrtoint ptr %h to i64
  store i64 %c, ptr %e
  call void @__bennett_adj(ptr @rg, ptr null, ptr %e)
  %l = load i64, ptr %e
  %h2 = inttoptr i64 %l to ptr
  call void @__bennett_qfree(ptr %h2)
  ret void
}
```

```llvm example=handle-memcpy verdict=accept candidates=rg
declare void @llvm.memcpy.p0.p0.i64(ptr, ptr, i64, i1 immarg)

define internal void @rg(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  ret void
}

define void @top() {
  %slot = alloca ptr
  %e = alloca { ptr, i64 }
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h, ptr %slot
  call void @llvm.memcpy.p0.p0.i64(ptr %e, ptr %slot, i64 8, i1 false)
  call void @__bennett_adj(ptr @rg, ptr null, ptr %e)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

```llvm example=handle-arith verdict=reject:BD-E-HANDLE-USE
define void @top() {
  %h = call ptr @__bennett_qalloc(i64 0, i64 2)
  %c = ptrtoint ptr %h to i64
  %d = add i64 %c, 8
  %h2 = inttoptr i64 %d to ptr
  call void @__bennett_gate(i32 1, ptr %h2, i64 0)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

C `if (!q)` and handle equality are identity (maintainer decision 4):

```llvm example=handle-null-check verdict=accept
define void @top() {
entry:
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  %z = icmp eq ptr %h, null
  br i1 %z, label %out, label %use

use:
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  br label %out

out:
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

```llvm example=handle-eq verdict=accept
define void @swap_if_distinct(ptr %a, ptr %b) {
entry:
  %same = icmp eq ptr %a, %b
  br i1 %same, label %out, label %two

two:
  call void @__bennett_gate2(i32 3, ptr %a, i64 0, ptr %b, i64 0)
  br label %out

out:
  ret void
}
```

*(non-normative)* In `handle-eq`, `@swap_if_distinct` is a device entry whose two `ptr`
parameters reach marker handle operands, so both are handle parameters bound to `QREG` launch
arguments (§6.6).

```llvm example=handle-deref verdict=reject:BD-E-HANDLE-USE
define i64 @top() {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  %v = load i64, ptr %h
  call void @__bennett_qfree(ptr %h)
  ret i64 %v
}
```

```llvm example=handle-truncate verdict=reject:BD-E-HANDLE-USE
define i32 @top() {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  %c = ptrtoint ptr %h to i32
  call void @__bennett_qfree(ptr %h)
  ret i32 %c
}
```

```llvm example=handle-to-external verdict=reject:BD-E-HANDLE-ESCAPE
declare void @log_handle(ptr)

define void @top() {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @log_handle(ptr %h)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

```llvm example=handle-store-host verdict=reject:BD-E-HANDLE-ESCAPE
define void @put(ptr %out) {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h, ptr %out
  ret void
}
```

A constant address is no handle of this program:

```llvm example=handle-untracked verdict=reject:BD-E-HANDLE-UNTRACKED
define void @kick() {
  call void @__bennett_gate(i32 2, ptr inttoptr (i64 4096 to ptr), i64 0)
  ret void
}
```

A host-supplied register (REPL), and a register returned to the host:

```llvm example=handle-host-param verdict=accept
define void @kick(ptr %h) {
  call void @__bennett_gate(i32 2, ptr %h, i64 0)
  ret void
}
```

```llvm example=handle-return verdict=accept
define ptr @mk() {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @__bennett_gate(i32 2, ptr %h, i64 0)
  ret ptr %h
}
```

A slot whose address is stored in an internal global is still tracked (audit B-26):

```llvm example=handle-object-tracked verdict=accept
@pp = internal global ptr null

define void @top() {
  %slot = alloca ptr
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h, ptr %slot
  store ptr %slot, ptr @pp
  %s = load ptr, ptr @pp
  %h2 = load ptr, ptr %s
  call void @__bennett_gate(i32 1, ptr %h2, i64 0)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

Aggregates carry provenance per field (Rust passes pairs this way), and vector lanes per lane
(spike F1, `load-store-vectorizer`):

```llvm example=handle-aggregate verdict=accept
define void @top(i64 %i) {
  %h = call ptr @__bennett_qalloc(i64 0, i64 2)
  %p0 = insertvalue { ptr, i64 } zeroinitializer, ptr %h, 0
  %p1 = insertvalue { ptr, i64 } %p0, i64 %i, 1
  %g = extractvalue { ptr, i64 } %p1, 0
  %j = extractvalue { ptr, i64 } %p1, 1
  %k = and i64 %j, 1
  call void @__bennett_gate(i32 2, ptr %g, i64 %k)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

```llvm example=handle-vector-lane verdict=accept
define i64 @top(i64 %x) {
  %m = alloca <2 x i64>
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  %c = ptrtoint ptr %h to i64
  %v0 = insertelement <2 x i64> zeroinitializer, i64 %x, i32 0
  %v1 = insertelement <2 x i64> %v0, i64 %c, i32 1
  store <2 x i64> %v1, ptr %m
  %p = getelementptr i8, ptr %m, i64 8
  %l = load i64, ptr %p
  %h2 = inttoptr i64 %l to ptr
  call void @__bennett_gate(i32 1, ptr %h2, i64 0)
  %l0 = load i64, ptr %m
  %y = add i64 %l0, 1
  call void @__bennett_qfree(ptr %h)
  ret i64 %y
}
```

A handle table indexed by a classical value, and a dynamically indexed vector of handles
(audit B-23):

```llvm example=handle-table verdict=accept
define void @tab(i64 %i) {
  %t = alloca [4 x ptr]
  %h0 = call ptr @__bennett_qalloc(i64 0, i64 1)
  %h1 = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h0, ptr %t
  %p1 = getelementptr [4 x ptr], ptr %t, i64 0, i64 1
  store ptr %h1, ptr %p1
  %k = and i64 %i, 1
  %pk = getelementptr [4 x ptr], ptr %t, i64 0, i64 %k
  %hk = load ptr, ptr %pk
  call void @__bennett_gate(i32 1, ptr %hk, i64 0)
  call void @__bennett_qfree(ptr %h0)
  call void @__bennett_qfree(ptr %h1)
  ret void
}
```

```llvm example=handle-dynamic-lane verdict=accept
define void @lanes(i32 %i) {
  %h0 = call ptr @__bennett_qalloc(i64 0, i64 1)
  %h1 = call ptr @__bennett_qalloc(i64 0, i64 1)
  %v0 = insertelement <2 x ptr> zeroinitializer, ptr %h0, i32 0
  %v1 = insertelement <2 x ptr> %v0, ptr %h1, i32 1
  %k = and i32 %i, 1
  %hk = extractelement <2 x ptr> %v1, i32 %k
  call void @__bennett_gate(i32 1, ptr %hk, i64 0)
  call void @__bennett_qfree(ptr %h0)
  call void @__bennett_qfree(ptr %h1)
  ret void
}
```

A vector of handles filled by a loop with a constant trip count has the instance bound
N(s) = E(s) = 8 (§6.5 rule 2); the same loop with a trip count from host input is blocked
(BLK-1):

```llvm example=handle-vec-bounded verdict=accept
define void @fill() {
entry:
  %v = alloca [8 x ptr]
  br label %loop

loop:
  %i = phi i64 [ 0, %entry ], [ %i2, %loop ]
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  %p = getelementptr [8 x ptr], ptr %v, i64 0, i64 %i
  store ptr %h, ptr %p
  %i2 = add i64 %i, 1
  %c = icmp ult i64 %i2, 8
  br i1 %c, label %loop, label %use

use:
  %p3 = getelementptr [8 x ptr], ptr %v, i64 0, i64 3
  %h3 = load ptr, ptr %p3
  call void @__bennett_gate(i32 2, ptr %h3, i64 0)
  br label %free

free:
  %j = phi i64 [ 0, %use ], [ %j2, %free ]
  %q = getelementptr [8 x ptr], ptr %v, i64 0, i64 %j
  %hq = load ptr, ptr %q
  call void @__bennett_qfree(ptr %hq)
  %j2 = add i64 %j, 1
  %d = icmp ult i64 %j2, 8
  br i1 %d, label %free, label %out

out:
  ret void
}
```

```llvm example=handle-vec-unbounded verdict=blocked:BD-B-ISA4
declare ptr @malloc(i64)
declare void @free(ptr)

define void @fill(i64 %n) {
entry:
  %z = icmp eq i64 %n, 0
  br i1 %z, label %out, label %alloc

alloc:
  %bytes = shl i64 %n, 3
  %v = call ptr @malloc(i64 %bytes)
  br label %loop

loop:
  %i = phi i64 [ 0, %alloc ], [ %i2, %loop ]
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  %p = getelementptr ptr, ptr %v, i64 %i
  store ptr %h, ptr %p
  %i2 = add i64 %i, 1
  %c = icmp ult i64 %i2, %n
  br i1 %c, label %loop, label %free

free:
  %j = phi i64 [ 0, %loop ], [ %j2, %free ]
  %q = getelementptr ptr, ptr %v, i64 %j
  %hq = load ptr, ptr %q
  call void @__bennett_qfree(ptr %hq)
  %j2 = add i64 %j, 1
  %d = icmp ult i64 %j2, %n
  br i1 %d, label %free, label %done

done:
  call void @free(ptr %v)
  br label %out

out:
  ret void
}
```

```text blocker=handle-vec-unbounded
BD-B-ISA4 @fill %h: qalloc site has no instance bound (stored into a heap object, loop trip count not constant: E = infinity); ISA 0.8 has no qreg in memory; BLK-1 (ISA-4) qreg.id/qreg.from_id; compiled with 64 static instances and a blocker trap beyond them
```

A handle passed to an indirect call reaches every candidate's parameter (audit B-22):

```llvm example=handle-indirect verdict=accept callees=hx,hz
@ops = internal constant [2 x ptr] [ptr @hx, ptr @hz]

define internal void @hx(ptr %q) {
  call void @__bennett_gate(i32 1, ptr %q, i64 0)
  ret void
}

define internal void @hz(ptr %q) {
  call void @__bennett_gate(i32 7, ptr %q, i64 0)
  ret void
}

define void @apply(i64 %k) {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  %i = and i64 %k, 1
  %p = getelementptr [2 x ptr], ptr @ops, i64 0, i64 %i
  %f = load ptr, ptr %p
  call void %f(ptr %h)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

`qstore` twice is the identity on `mem`, so every register is released clean:

```llvm example=qstore-twice verdict=accept
define void @top() {
  %mem = call ptr @__bennett_qalloc(i64 0, i64 4)
  %addr = call ptr @__bennett_qalloc(i64 0, i64 1)
  %val = call ptr @__bennett_qalloc(i64 0, i64 2)
  call void @__bennett_qstore(ptr %mem, ptr %addr, ptr %val)
  call void @__bennett_qstore(ptr %mem, ptr %addr, ptr %val)
  call void @__bennett_qfree(ptr %val)
  call void @__bennett_qfree(ptr %addr)
  call void @__bennett_qfree(ptr %mem)
  ret void
}
```

## 7. Regions (regions 0.2)

### 7.1 Region-entry markers and region kinds

| Marker | Region operand(s) | Interface kind | Required type of a candidate | ISA counterpart |
|---|---|---|---|---|
| `ctrl(q, qi, f, budget, env)` | `f` | action | `void (ptr)` | `ctl w action_call` (ISA §4.7, §5.3) |
| `adj(f, budget, env)` | `f` | action | `void (ptr)` | `adj action_call` |
| `compute(f, use, budget, env)` | `f`, `use` | action | `void (ptr)` | `action_call`; `action_call`; `adj action_call` |
| `reversible(f, budget, env)` | `f` | reversible | `void (ptr)` | a call of an R function (ISA §3.1, §7.4) |
| `oracle(f, budget, desc)` | `f` | oracle | any function type (§8) | `oracle_call @ref tk (ins..) tgt fr (mem..) (args..)` (ISA §4.7, §5.2) |
| `inplace(g, ginv, budget, desc)` | `g`, `ginv` | oracle pair | any function type whose INOUT parameter and result have equal widths (§8.7) | `qinplace @g @ginv tk x` (ISA §4.5) |

The marker fixes the region's **interface** (TDL-1, §10). The body is partitioned by content
(§10) and never rejected for containing classical code; the plugin outlines coherent slices of
action bodies (TDL-3). An **oracle region** is a lifted classical oracle with output targets and
a fault register (ISA §5.2); an **action region** is a quantum action on the wires its events
name (ISA §5.3) with no fault outcome of its own: a fault of an oracle it calls lands in a fault
register the action declares (§10, TDL-8).

### 7.2 Candidate sets and dispatch (maintainer decision 3)

The candidate set RR(v) of a region operand v is computed from its abstract value (§5):

- every `FN(F)` atom of AV(v), resolved by `resolve` below;
- if AV(v) has the ⊤ flag: in addition every function of the required type of §7.1 (for
  `oracle`/`inplace`: every function) whose address is used anywhere in the linked program,
  resolved (decision 3 read literally: "every function whose address can reach a region marker";
  audit B-33). The set is therefore always bounded by the program.

`resolve(F)` follows aliases to their aliasee and **forwarding thunks** to their target: F is a
forwarding thunk of G iff F's body is one block holding exactly a call of G (optionally
`tail`/`musttail`/`notail`, default calling convention, no operand bundles) whose arguments are
F's parameters in order and whose function type equals F's, followed by `ret void` or `ret` of
that call's result; then `resolve(F) = resolve(G)`, except that a thunk on a cycle of thunks
resolves to itself (it is an ordinary defined function whose execution recurses until a budget or
the host stops it; 0.1's `BD-E-REGION-THUNK` is deleted).

**Dispatch.** The region operand is classical data. The plugin compiles a body for every
candidate. At run time the operand's value is compared, by the compare tree of §14.2 over the
sorted keys, with A(S) of every **source** S (every function or alias that resolves into the
candidate set and whose address reaches v, plus every candidate itself); on equality the region
`resolve(S)` is entered. No match is the run-time trap `T-REGION` (fault code 4). A candidate
with no definition (an external declaration, a function without bitcode) is entered as a
trapped call: F(8) with a coverage line (§4.5 item 4).

**Ill-formed candidates.** A candidate that is not well-formed for the marker's kind (a type
other than §7.1's, or a violation of §7.5) is compiled as a **trap body** (`T-REGION-INVALID`,
fault code 4) with a coverage line: it may never be dispatched, so it is not a compile-time
error. It is rejected (`BD-E-REGION-TYPE`, `BD-E-REGION-MEASURE`, `BD-E-REVERSIBLE-MEASURE`)
only when it is the **unique** candidate, because then every execution of the marker fails
(outline E14).

0.1's `BD-E-REGION-UNBOUNDED` and `BD-E-REGION-EXTERNAL` are deleted.

### 7.3 Region identity (maintainer decision 1)

A region is identified by its content, never by its symbol. Candidates that resolve to the same
function are one region. The semantic identity of an **oracle region** in a shape (§8.4) is the
interface hash (ISA §9.2) of `@ref` in its reference object (§16.2): every lproc, data image and
layout leaf of the closure is part of it, and `@ref`, `@L<n>`, `@G<n>` are fixed names, so two
functions with equal materialised bodies have equal identity whatever their source names. Symbol
names, linkage, aliases and thunks are non-normative: diagnostics and coverage entries MAY print
them.

The **region key** of any region is the SHA-256 of the text printed by the LLVM printer of the
major in use for a module that contains the materialised region function and its closure, after
`strip` (local names), with the functions renamed `f0, f1, …` in depth-first preorder from the
region along direct calls in instruction order, and without datalayout, triple and module
metadata. It keys the budget table (§9.2) and is recorded in the certificate and coverage
entries. It depends on the LLVM major, which the certificate records (§24, D13).

### 7.4 Kinds by content

NS §4.2: "the plugin classifies each outlined region by its contents and the verifier checks the
declared interface". After the TDL partition (§10):

- an action region whose generated events are all permutation events (X-family gates, `qload`,
  `qstore`, `qexch`, oracle calls, permutation actions) is emitted as an ISA `perm_action`
  (ISA §5.3), which certificates can verify by T3; otherwise as an `action`;
- an oracle region stays an oracle;
- a `reversible` marker call reached from an action region's generation or from an L closure is
  not an R entry: its operand is treated as a direct call of the region function, partitioned by
  TDL inside actions and lifted inside oracles, with the call's budget record governing its
  slices (§9.3; audit B-37). 0.1's `BD-E-REGION-TIER` and `T-TIER` are deleted.

### 7.5 Static well-formedness

Only the rules the north star requires:

- **(a) Measurement in a unitary region.** A `measure` call in the closure of an action region
  is `BD-E-REGION-MEASURE` (NS §3.1: "user measurement inside it is refused"), unless the module
  requests **deferred measurement** with the module flag `!{i32 1,
  !"bennett.measure_in_unitary", !"defer"}` (NS §3.1: "or, when the front end asks for it,
  deferred by the deferred-measurement principle, which the certificate states"). Then a
  `measure(h, i)` inside a generation becomes a `qcopy` of `h.i` onto a fresh wire w (ISA §4.5),
  the call's `i1` result is a Co value whose wire is w (§10, TDL-2 seed), and w is released by
  `quncopy` after its last use while its window is open (ISA §4.5, §6.2), else it is retained
  history (TDL-7). The coverage report has a
  `lowered` entry with source `dialect-0.2:7.5a` for every such call, and the certificate lists
  the id `deferred_measurement` in the region's `definedness_assumptions` (ISA §12.3; §25.2
  records the wording item).
- **(b) Reversible regions.** The closure of a reversible region MAY contain gate and region
  markers on handles received through `env`: they lower to R-tier `action_call`/`oracle_call`
  (ISA §3.1, §4.7), recorded in the R history and reversed by re-application or adjoint (ISA
  §7.4). A `measure` call in the closure is `BD-E-REVERSIBLE-MEASURE` (ISA §10: a run that
  measured is not reversible; ISA §3.3: a `measure` frame is never reversed). A `qalloc`,
  `qborrow` or `qfree` in the closure is **hoisted** (ISA 0.8 has `qreg.new` in CC only): when
  every such site s has a finite reference instance bound N(s) (§6.5 rules 1 and 2, applied to
  every site whether or not it reaches memory, with the reversible entry in place of the device
  entry), the CC caller allocates N(s) clean registers per site before the R call, passes them as
  `qreg` arguments, and frees them after it returns; `qalloc` in R selects a free one, `qfree`
  checks that it is clean (`T-CLEAN`) and returns it to the free set. Otherwise the site is a
  blocker point of BLK-4 (`blocked:BD-B-ISA12`, §25.1).
- **(c) In-place pairs** are verified by §8.7.

### 7.6 Outlining conventions

- Regions are functions on arrival: the front end outlines (a Julia macro, a clang attribute, a
  Rust closure trampoline); the dialect imposes no source syntax. The plugin additionally
  outlines coherent slices (TDL-3), which is not observable beyond §18.
- Action and reversible regions have type `void (ptr env)`. `env` points to classical memory the
  front end owns (an `alloca` or heap object) that is live for the duration of the marker call;
  the region reads and writes it as classical memory (§18.4). Handles reach a region through
  `env` (PT9 binds a region's parameter to the marker's env argument).
- Oracle regions are arbitrary functions bound by a descriptor (§8); no packing wrapper is
  needed (audit D21).
- A region body MUST be referenced by the region operand (directly or through §7.2); a body
  referenced only from a side-table global is not a region (enzyme survey implication 5).
- Region functions SHOULD have internal linkage, so that they are not device entries. C++
  lambdas pass their static `__invoke` thunk and Rust closures an `extern "C"` trampoline; both
  are ordinary region functions whose closure contains the closure body.

### 7.7 Examples

```llvm example=region-select verdict=accept candidates=ra,rb
define internal void @ra(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  ret void
}

define internal void @rb(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 2, ptr %h, i64 0)
  ret void
}

define void @top(i1 %c) {
  %e = alloca ptr
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h, ptr %e
  %f = select i1 %c, ptr @ra, ptr @rb
  call void @__bennett_adj(ptr %f, ptr null, ptr %e)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

The SimplifyCFG switch-to-lookup shape (`region-switch-fnptr-table` after `default<O3>`):

```llvm example=region-switch-table verdict=accept candidates=ra,rb,rc,rd
@switch.table.top = private unnamed_addr constant [3 x ptr] [ptr @ra, ptr @rb, ptr @rc]

define internal void @ra(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  ret void
}

define internal void @rb(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 2, ptr %h, i64 0)
  ret void
}

define internal void @rc(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 3, ptr %h, i64 0)
  ret void
}

define internal void @rd(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 4, ptr %h, i64 0)
  ret void
}

define void @top(i64 %i) {
entry:
  %e = alloca ptr
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h, ptr %e
  %in = icmp ult i64 %i, 3
  br i1 %in, label %look, label %dflt

look:
  %p = getelementptr [3 x ptr], ptr @switch.table.top, i64 0, i64 %i
  %ft = load ptr, ptr %p
  br label %join

dflt:
  br label %join

join:
  %f = phi ptr [ %ft, %look ], [ @rd, %dflt ]
  call void @__bennett_adj(ptr %f, ptr null, ptr %e)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

The `reg2mem` shape (a region pointer in a stack slot):

```llvm example=region-stack-slot verdict=accept candidates=ra,rb
define internal void @ra(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  ret void
}

define internal void @rb(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 2, ptr %h, i64 0)
  ret void
}

define void @top(i1 %c) {
entry:
  %slot = alloca ptr
  %e = alloca ptr
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h, ptr %e
  br i1 %c, label %a, label %b

a:
  store ptr @ra, ptr %slot
  br label %join

b:
  store ptr @rb, ptr %slot
  br label %join

join:
  %f = load ptr, ptr %slot
  call void @__bennett_adj(ptr %f, ptr null, ptr %e)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

Merged twins resolve to one region (spike F2; `mergefunc` makes `@k2` a forwarding thunk,
`-mergefunc-use-aliases` makes an alias):

```llvm example=region-twins verdict=accept candidates=k1
@k3 = internal alias void (ptr), ptr @k1

define internal void @k1(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  ret void
}

define internal void @k2(ptr %0) {
  tail call void @k1(ptr %0)
  ret void
}

define void @top(i1 %c) {
  %e = alloca ptr
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h, ptr %e
  %f = select i1 %c, ptr @k2, ptr @k3
  call void @__bennett_adj(ptr %f, ptr null, ptr %e)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

A region pointer from host input (a parameter of an externally visible function) has AV = ⊤,
so its candidates are every address-taken `void (ptr)` function of the program: here `@ra` and
`@rb`, whose addresses `@menu` returns to the host (audit B-33, decision 3):

```llvm example=region-host-param verdict=accept candidates=ra,rb
define internal void @ra(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  ret void
}

define internal void @rb(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 2, ptr %h, i64 0)
  ret void
}

define ptr @menu(i1 %c) {
  %f = select i1 %c, ptr @ra, ptr @rb
  ret ptr %f
}

define void @top(ptr %f) {
  %e = alloca ptr
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h, ptr %e
  call void @__bennett_adj(ptr %f, ptr null, ptr %e)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

An `inttoptr` constant is dispatched the same way, and traps (`T-REGION`) on an execution where
it equals neither A(`@ra`) nor A(`@rb`); an external declaration is entered as a trapped call
(F(8)):

```llvm example=region-inttoptr verdict=accept candidates=ra
define internal void @ra(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  ret void
}

@keep = internal global ptr @ra

define void @top() {
  %e = alloca ptr
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h, ptr %e
  call void @__bennett_adj(ptr inttoptr (i64 127079231243584 to ptr), ptr null, ptr %e)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

```llvm example=region-external verdict=accept candidates=elsewhere
declare void @elsewhere(ptr)

define void @top() {
  %e = alloca ptr
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h, ptr %e
  call void @__bennett_adj(ptr @elsewhere, ptr null, ptr %e)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

A unique ill-formed candidate is rejected; one ill-formed member of a larger set is a trap body:

```llvm example=region-wrong-type verdict=reject:BD-E-REGION-TYPE
define internal i8 @inc(i8 %x) {
  %r = add i8 %x, 1
  ret i8 %r
}

define void @top() {
  %e = alloca ptr
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h, ptr %e
  call void @__bennett_adj(ptr @inc, ptr null, ptr %e)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

```llvm example=region-mixed-types verdict=accept candidates=inc,ra
define internal i8 @inc(i8 %x) {
  %r = add i8 %x, 1
  ret i8 %r
}

define internal void @ra(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  ret void
}

define void @top(i1 %c) {
  %e = alloca ptr
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h, ptr %e
  %f = select i1 %c, ptr @inc, ptr @ra
  call void @__bennett_adj(ptr %f, ptr null, ptr %e)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

Measurement inside `ctrl` is refused, unless the module asks for deferral:

```llvm example=region-measure-in-ctrl verdict=reject:BD-E-REGION-MEASURE
define internal void @body(ptr %e) {
  %h = load ptr, ptr %e
  %m = call i1 @__bennett_measure(ptr %h, i64 0)
  ret void
}

define void @top() {
  %e = alloca ptr
  %c = call ptr @__bennett_qalloc(i64 0, i64 1)
  %t = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %t, ptr %e
  call void @__bennett_ctrl(ptr %c, i64 0, ptr @body, ptr null, ptr %e)
  call void @__bennett_qfree(ptr %t)
  call void @__bennett_qfree(ptr %c)
  ret void
}
```

```llvm example=region-measure-deferred verdict=accept candidates=body
define internal void @body(ptr %e) {
entry:
  %h = load ptr, ptr %e
  %p = getelementptr i8, ptr %e, i64 8
  %t = load ptr, ptr %p
  %m = call i1 @__bennett_measure(ptr %h, i64 0)
  br i1 %m, label %flip, label %out

flip:
  call void @__bennett_gate(i32 1, ptr %t, i64 0)
  br label %out

out:
  ret void
}

define void @top() {
  %e = alloca [2 x ptr]
  %c = call ptr @__bennett_qalloc(i64 0, i64 1)
  %a = call ptr @__bennett_qalloc(i64 0, i64 1)
  %t = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %a, ptr %e
  %p = getelementptr i8, ptr %e, i64 8
  store ptr %t, ptr %p
  call void @__bennett_ctrl(ptr %c, i64 0, ptr @body, ptr null, ptr %e)
  call void @__bennett_qfree(ptr %t)
  call void @__bennett_qfree(ptr %a)
  call void @__bennett_qfree(ptr %c)
  ret void
}

!llvm.module.flags = !{!0}
!0 = !{i32 1, !"bennett.measure_in_unitary", !"defer"}
```

*(non-normative)* In `region-measure-deferred` the branch on `%m` is a Co branch (TDL-2), so the
gate on `%t` is issued under `qpred` of the copy wire (TDL-10): the action is
`ctl c (qcopy a.0 → w; cx w t.0)` with w released by the region's uncomputation, which is the
deferred-measurement principle.

A `reversible` call inside an action is a direct call of its body (§7.4); gate markers inside a
reversible closure act on handles from `env` (§7.5b); measurement there is refused:

```llvm example=region-reversible-in-action verdict=accept candidates=body
define internal void @classical(ptr %e) {
  %p = getelementptr i8, ptr %e, i64 8
  %v = load i64, ptr %p
  %v2 = add i64 %v, 1
  store i64 %v2, ptr %p
  ret void
}

define internal void @body(ptr %e) {
  call void @__bennett_reversible(ptr @classical, ptr null, ptr %e)
  ret void
}

define void @top() {
  %e = alloca { ptr, i64 }
  call void @__bennett_adj(ptr @body, ptr null, ptr %e)
  ret void
}
```

```llvm example=region-reversible-marker verdict=accept candidates=body
define internal void @body(ptr %e) {
  %h = load ptr, ptr %e
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  ret void
}

define void @top() {
  %e = alloca ptr
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h, ptr %e
  call void @__bennett_reversible(ptr @body, ptr null, ptr %e)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

```llvm example=region-reversible-measure verdict=reject:BD-E-REVERSIBLE-MEASURE
define internal void @body(ptr %e) {
  %h = load ptr, ptr %e
  %m = call i1 @__bennett_measure(ptr %h, i64 0)
  ret void
}

define void @top() {
  %e = alloca ptr
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %h, ptr %e
  call void @__bennett_reversible(ptr @body, ptr null, ptr %e)
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

A register allocated in R and freed before the next allocation is hoisted to the CC caller
(self-disjoint, N = 1); one allocated per activation of a recursion whose depth comes from host
data has no bound and is BLK-4 (the same function in CC is realised directly, §6.5):

```llvm example=region-reversible-qalloc-static verdict=accept candidates=body
define internal void @body(ptr %e) {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  call void @__bennett_qfree(ptr %h)
  ret void
}

define void @top() {
  %e = alloca i64
  call void @__bennett_reversible(ptr @body, ptr null, ptr %e)
  ret void
}
```

```llvm example=region-reversible-qalloc-dynamic verdict=blocked:BD-B-ISA12
define internal void @rec(i64 %d) {
entry:
  %z = icmp eq i64 %d, 0
  br i1 %z, label %out, label %more

more:
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  %d2 = sub i64 %d, 1
  call void @rec(i64 %d2)
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  call void @__bennett_qfree(ptr %h)
  br label %out

out:
  ret void
}

define internal void @body(ptr %e) {
  %d = load i64, ptr %e
  call void @rec(i64 %d)
  ret void
}

define void @top(i64 %n) {
  %e = alloca i64
  store i64 %n, ptr %e
  call void @__bennett_reversible(ptr @body, ptr null, ptr %e)
  ret void
}
```

```text blocker=region-reversible-qalloc-dynamic
BD-B-ISA12 @rec %h: qalloc in a reversible closure with no instance bound (recursive, live across the recursive call: E = infinity); cannot be hoisted to the CC caller; ISA 0.8 qreg.new is CC only; BLK-4 (new ISA-12) qreg.* in R
```

## 8. The oracle interface (oracle-abi 0.2)

`__bennett_oracle(f, budget, desc)` applies the lifted oracle of region function f, under the
budget of §9, to the registers and classical values that the **descriptor** `desc` binds to f's
parameters, result and device models. `__bennett_inplace(g, ginv, budget, desc)` applies an
in-place bijection (§8.7). The descriptor is classical data in the caller's memory, built by
plain stores (§3.8); its kinds are classical values dispatched over their finite domains (§8.4).

### 8.1 Descriptor layout

The descriptor is the LLVM struct `{ H, [nparam x Bind], [ndev x DevBind] }` laid out by the
module's datalayout, where (C view in `bennett_markers.h`, §3.3):

| Type | LLVM | Fields (C names) |
|---|---|---|
| H | `{ i32, i32, i32, i32, ptr, ptr }` | `version` (= 2), `nparam`, `ndev`, `flags` (= 0), `tgt`, `fault` |
| Bind | `{ i32, i32, ptr, i64, i64 }` | `kind`, `mode`, `q`, `value`, `size` |
| DevBind | `{ i32, i32, ptr, i64 }` | `model`, `mode` (= 0), `q`, `value` |

On x86-64, AArch64 and RISC-V64 (pw = 64) H is 32 bytes, Bind 32 bytes (`kind` at 0, `mode` 4,
`q` 8, `value` 16, `size` 24) and DevBind 24 bytes, so `param[i]` is at 32 + 32i and `dev[j]` at
32 + 32·nparam + 24j. The plugin reads the descriptor at the marker call, in the caller's tier,
with ordinary loads. `nparam` MUST equal the number of IR parameters of the dispatched region
function (after ABI lowering: the IR signature). A descriptor whose `version`, `flags`, `nparam`
or any kind, mode or model is not one this section defines, or whose binding does not fit the
parameter's type (below), traps (`T-IFACE`, fault code 4) when the marker is called.

### 8.2 Parameter bindings

Let the dispatched region function have IR parameters p_0 … p_{m−1} and return type R (`void`
or a first-class type of at most 128 bits after N25, §12.2). `param[i]` binds p_i:

| Kind | Code | Parameter type | Register | Meaning | ISA lowering (§16.2) |
|---|---|---|---|---|---|
| `IN` | 1 | `iW` or `ptr` (W = pw) | q with n(q) ≤ W | the parameter's value is the basis value of q, zero-extended (`mode` = ZEXT 0) or sign-extended (`mode` = SEXT 1) to W; a `ptr` parameter may be `IN` (a superposed pointer) | an `ins` bundle `x<k>:wire[n(q)]` (a pseudo-location, ISA §3.7), extended by `lift.zext`/`lift.sext` in the wrapper |
| `ARG` | 2 | `iW` (W ≤ 128) or `ptr` | none (`q` ignored) | a classical value: bits 0–63 from `value`, bits 64–127 from `size`; a `ptr` ARG is an address in the caller's classical memory, which the oracle reads through its entry state (§8.5) | an `args` entry `a<k>:i<W>` (W = pw for `ptr`; ISA §4.7, §5.1) |
| `MEM_IN` | 3 | `ptr` | q with n(q) = 8·2^A, `size` = 2^A | the parameter is the base address of an interface region of 2^A bytes whose cell i is byte i of q (bits [8i, 8i + 8)); its contents may be superposed; role `in` (restored on every basis configuration, ISA §5.1). This is the quantum-addressed memory of NS §8 rung 4 | a `mem` region `m<k>:region[A,8] in`; the argument is `lift.addr @m<k>` |
| `OUT` | 4 | `ptr` | q with n(q) = 8·`size` | the parameter points to a fresh zero-filled buffer of `size` bytes in the oracle's memory; at exit its final bytes are XORed into q, byte k into wires [8k, 8k + 8) (a declared output, NS §4.2) | `lift.alloc size` in the wrapper; the bytes are part of the payload (§8.6) |
| `INOUT` | 5 | `iW` | q with n(q) = W | `inplace` only (§8.7): the in-place register x | `qinplace … x` |

The **result**: a non-null `tgt` register receives the return value: payload bits = the return
value zero-extended to n(tgt) if n(tgt) ≥ R's width; if n(tgt) is narrower, the dropped bits are
checked and an execution on which they are nonzero faults with code 4 (`FAULT_UB_TRAP`); the
retained bits are the low n(tgt). A null `tgt` discards the return value. For `oracle`, the
**fault register** `fault` MUST be a register of exactly 4 wires (ISA §5.4: F = 4) and MUST NOT
be null (`T-IFACE`).
Every register named by the descriptor MUST be live and pairwise distinct (`T-DEAD`, `T-ALIAS`).
A width mismatch in the table above is `T-SIZE`.

### 8.3 Device bindings

`dev[j]` binds a device model for the lifted (coherent) tier (§11.3):

| Model | Code | Register | Meaning |
|---|---|---|---|
| `ENTROPY` | 1 | q with n(q) = 8·2^A | an `in` region `e0:region[A,8]` holding the entropy tape, possibly superposed (NS §8 rung 8: "the entropy device is replaced by a superposed register") |
| `BLOCK` | 2 | q with n(q) = 8·512·2^A′ | an `in` region `k0` holding the disk image of 2^A′ sectors; writes go to a lifted copy-on-write overlay in the oracle's heap |
| `CLOCK` | 3 | none | the clock model's initial value is `value` |
| `CONSOLE` | 4 | q with n(q) = 8·L, or null | the first L bytes the oracle writes to the console are XORed into q as an output (payload, §8.6); with a null q console bytes are discarded with the oracle's other writes |

At most one binding per model. A model without a binding is **unbound**: an effect on it in L
code faults with code 8 on the executions that reach it (§11.3; NS §4.2).

### 8.4 Shapes and dispatch

A **shape** is the tuple (region candidate F; for each parameter its kind, mode, register width
n(q) and `size`; n(tgt) or "none"; for each device binding its model and n(q)). The kind, mode,
model, `size` and `value` fields have value sets (§5.3); register widths come from the register
file (§6.5), whose roots have known widths. The plugin compiles one reference object (§16.2) per
shape that the value sets allow, taking every unbounded kind or mode field over its finite
domain (5 kinds, 2 modes, 4 models), so the number of shapes is always bounded. At run time the
caller's tier reads the descriptor and selects the compiled shape with the compare tree of
§14.2; a descriptor that matches no compiled shape traps (`T-IFACE`), which happens only for a
field outside its table. `value` and `size` of `ARG` bindings are the oracle's classical
arguments and are not part of the shape. *(non-normative)* With constant stores every field has
a singleton value set and there is one shape per candidate.

The marker then issues, in the caller's tier, one **oracle invocation** (§8.6) whose operands are
the static registers the descriptor's handles denote (§6.5), the budget token (§9.5) and the
classical arguments.

### 8.5 Entry state

**Reference semantics.** The region function runs on a **private copy of the caller's whole
classical memory at the call**, with the bound inputs; its writes are discarded except through
`OUT`, `tgt` and the bound device outputs (NS §4.2: "every other write being restored
workspace"). Constant globals, and mutable globals that only the oracle's own L closure writes,
equal their initialisers at every call.

**Realisation on ISA 0.8.** Let R be the abstract objects the oracle closure may load (§5.4),
minus constant globals, minus mutable globals written by no function outside the L closure. If
R is empty, nothing is transferred: the oracle's globals start at their data images (ISA §3.7).
This is rung 4 route A (SQLite §5.2(i)). Otherwise the plugin emits an **entry-state transfer**:

1. **Snapshot.** At the call the caller's tier forms the byte string
   S = k ‖ (size_i ‖ live_i)_{i<k} ‖ G ‖ Hb, where k is the number of heap allocations in the
   caller's allocation table (in allocation order, ISA §7.1), `size_i` and `live_i` are 8-byte
   little-endian fields, G is the bytes of the mutable globals in R in `layout.globals` order,
   and Hb is the bytes of every live heap allocation in allocation order if R contains a heap
   object (else empty). S is zero-padded to 2^A_s bytes, where A_s is the smallest exponent with
   2^A_s ≥ 8 + 16·N_alloc + Σ|G| + `heap_limit_max` (N_alloc the allocation-table capacity of
   the layout, §19.5); A_s is static.
2. **Register.** The CC tier builds a register of 8·2^A_s wires holding S with a **concat
   tree** of A_s − 3 static-width CC functions `B_j` (j = 4, …, A_s): `B_4(p)` executes
   `qreg.new any 128`, loads the 16 bytes at p as two `i64` values and makes the `oracle_call`
   of the runtime oracle `@xor128` (§16.5) that XORs them into the register (with a token minted
   at launch for budget (6, 0, 0, 0) and a fresh 4-wire fault register, which stays clean and is
   freed); `B_j(p)` (j > 4)
   returns `qreg.concat B_{j−1}(p) B_{j−1}(p + 2^{j−1})`. Every type is static and the cost is
   2^(A_s−4) region calls. The register is bound as an extra `in` region `s0:region[A_s,8]`.
3. **Replay.** The wrapper prologue (§16.2) calls the runtimes function
   `__bennett_rt_entry_replay(s0)`, which for i < k executes `__bennett_nz_alloc(size_i)` (ISA
   `lift.alloc`) and, if `live_i` = 0, `__bennett_nz_free` of the result. ISA §4.2 `lift.alloc`
   and ISA §7.1 `alloc` share the rule "bump + max(n, 1) from `heap_base`", so the replay
   reproduces the caller's heap addresses exactly (audit O-07). It then copies G into the
   globals (by the driver-generated table `__bennett_rt_entry_table` of their addresses and
   sizes) and Hb into the replayed live allocations.
4. **Release.** The snapshot register holds the basis state |S⟩ and is unentangled after every
   oracle call (an `in` region is unchanged on every basis configuration, ISA §5.2). The caller
   keeps it for later calls while no store to an object of R has executed since it was built,
   and releases it by `measure` (its outcome is S with probability 1 and is discarded) before
   the next build or at the end of the caller's run. *(non-normative)* A run that measures is not
   reversible (ISA §10); a CC program that calls oracles is not a whole-run reversal candidate.

The replay's rows, allocations and calls are part of the reference body and count against the
budget (§9.4). Entry-state transfer from R-tier code needs registers allocated in R (BLK-4,
§25.1); no rung uses it. **Build-time snapshots** (rung 7, §19.6) rewrite the initialisers of
the mutable globals to snapshot values at link time, so R is empty and nothing is transferred.
Efficiency: G-12 (§25.3).

### 8.6 Oracle invocations and wide outputs

The **outputs** of a shape are, in order: `tgt` (if non-null), each `OUT` parameter in parameter
order, and the `CONSOLE` register (if bound). Each output register is split into **slices** of
at most 128 bits from its low end (ISA §3.3: payloads are `iN` with N ≤ 128); the slices of all
outputs are numbered 0, 1, …, k − 1 in that order. Every slice j has an oracle **variant** W_j:
the same reference body (§16.2) whose `lift.retval` delivers slice j of the payload. All variants
compute the same fault code, so code(F_B) is one function of the inputs.

- **k = 1** (every output fits 128 bits in one register): the invocation is `oracle_call @W_0
  tk (ins..) tgt fault (mem..) (args..)`.
- **k > 1** (the `wide` event, §18.2): the caller's tier issues, for j = k − 1, …, 1, with
  slice j at bits [lo_j, lo_j + w_j) of output register o_j:

  ```
  t_j = qreg.new any w_j ; f_j = qreg.new any 4
  oracle_call @W_j tk (ins..) t_j f_j (mem..) (args..)
  s_j = qreg.slice o_j lo_j w_j
  action_call @xor<w_j> (s_j) (t_j) () ()
  oracle_call @W_j tk (ins..) t_j f_j (mem..) (args..)
  qreg.free f_j ; qreg.free t_j
  ```

  followed by `s_0 = qreg.slice o_0 lo_0 w_0` and `oracle_call @W_0 tk (ins..) s_0 fault (mem..)
  (args..)`. `@xor<w>` is the permutation action `(mut s:wire[w]) (in t:wire[w]) () ()` with body
  `qxor t s`; each slice view is the operand of exactly one region call (ISA §3.3).

  Each copy-out pair computes slice j into fresh wires, XORs it into the target and uncomputes it
  by the identical self-adjoint call, whose inputs no call in between modifies, so `t_j` and `f_j`
  are clean when freed (ISA §5.2 involution; the ISA §3.3 cleanliness check of `qreg.free`);
  slice 0 and the fault code are delivered by the last call. The effect is exactly NS's F_B with a
  wide payload: slice_j ⊕= payload_j(F_B(x)) for every j and fault ⊕= code(F_B(x)). Cost: 2k − 1
  oracle calls (efficiency item G-15, §25.3). Under a `ctrl` every region call is `ctl`-prefixed
  (§18.2).

### 8.7 In-place updates

`inplace(g, ginv, budget, desc)` binds the in-place register x as `INOUT` (exactly one
parameter of each candidate pair is `INOUT`, of type `iN` with N = n(x); the result type is
`iN`). g and ginv are oracles in the sense of §8.2 with a **payload equal to the new value of
x**: their reference objects (§16.2) bind x as an `in` bundle and have an n(x)-bit target. The
descriptor's `tgt` MUST be null and its `fault` is ignored (`T-IFACE` otherwise): an in-place
update has no fault outcome (NS §4.2), and the `qinplace` expansion allocates its own clean
scratch (ISA §4.5).

- **No other bindings**: the call lowers to ISA `qinplace @g @ginv tk x` (ISA §4.5) with @g,
  @ginv the reference oracles of the pair.
- **Classical `ARG`s with finite value sets**: one `qinplace` per tuple of argument values, each
  with the pair specialised to those constants (the arguments become `lift.const` in the
  reference bodies), dispatched by §14.2.
- **Library bijections**: when the pair is a `bennett-arith` library bijection (add or subtract
  a value, xor, rotate, negate, byte swap, modular addition, modular multiplication by a unit,
  each with its stated conditions and its g∘ginv = id certificate, NS §3.1), the call lowers to
  the library's permutation action with `IN`, `MEM_IN` and `ARG` bindings as its `in`, `mem` and
  `args` operands, which ISA 0.8 expresses directly (ISA §4.7 `action_call`). This is also the
  TDL-5(b) mechanism (§10).
- **User pairs with `IN` or `MEM_IN` bindings, or `ARG`s with unbounded value sets**: ISA 0.8's
  `qinplace` has no parameter lists. The verdict is `blocked:BD-B-ISA3` (BLK-3, §25.1): the full
  mechanism is specified here and needs the ISA change of §25.1.

**Verification.** For every compiled pair and every argument tuple, when N ≤ the configured
width (driver option `-bennett-inplace-exhaustive-bits`, default 24, §24), the plugin MUST run
the reference interpreter on both reference bodies with an unbounded budget and check that for
every x ∈ [0, 2^N), F^g(x) = (y, 0) and F^ginv(y) = (x, 0); it records the **minimal budget**
B_min, the componentwise maximum over all those runs of (rows, heap bytes, stack cells, depth).
Above that width it MUST record a `sampled` evidence claim (ISA §12.1) of the same check and
B_min over the sample, and the dynamic net applies: a wrong inverse leaves the scratch register
of the `qinplace` expansion non-clean, which `T-CLEAN` catches (NS §3.1). F_B is monotone in
the budget (a run that completes within B completes identically within every B′ ≥ B), so the
pair is valid for exactly the budgets B ≥ B_min. A pair that fails the check, or whose budget
is static and below B_min in some component, is `BD-E-INPLACE-NOT-INVERSE` (NS §3.1: "an
in-place update with no inverse fails loud at compile time"; "a fallible or budget-limited
computation cannot be in-place"); a run-time budget (§9.5) below B_min traps at the marker
(`T-BUDGET`). *(non-normative)* On a finite set, ginv∘g = id makes g injective, hence a
bijection, so g∘ginv = id and ginv is fault-free on every input, as ISA `qinplace` requires.
0.1's `BD-E-INPLACE-UNVERIFIED` is deleted.

### 8.8 Examples

`inc8` bound by a descriptor with one `IN`, called twice (the oracle is an involution, so every
register is released clean). The descriptor and budget record are built by merged constant
stores, as `default<O3>` emits them; the budget record asks for 5 steps, no heap, 7 stack cells
and depth 1 (§9.1; §16.6 computes these numbers):

```llvm example=oracle-inc8 verdict=accept candidates=inc8 shapes=1
define internal i8 @inc8(i8 %x) {
  %r = add i8 %x, 1
  ret i8 %r
}

define void @top() {
  %d = alloca [64 x i8], align 8
  %b = alloca [40 x i8], align 8
  %x = call ptr @__bennett_qalloc(i64 0, i64 8)
  %t = call ptr @__bennett_qalloc(i64 0, i64 8)
  %f = call ptr @__bennett_qalloc(i64 0, i64 4)
  store <4 x i64> <i64 5, i64 0, i64 7, i64 1>, ptr %b, align 8
  %bf = getelementptr i8, ptr %b, i64 32
  store ptr null, ptr %bf, align 8
  store <4 x i32> <i32 2, i32 1, i32 0, i32 0>, ptr %d, align 8
  %dt = getelementptr i8, ptr %d, i64 16
  store ptr %t, ptr %dt, align 8
  %df = getelementptr i8, ptr %d, i64 24
  store ptr %f, ptr %df, align 8
  %p0 = getelementptr i8, ptr %d, i64 32
  store <2 x i32> <i32 1, i32 0>, ptr %p0, align 8
  %p0q = getelementptr i8, ptr %d, i64 40
  store ptr %x, ptr %p0q, align 8
  %p0v = getelementptr i8, ptr %d, i64 48
  store <2 x i64> zeroinitializer, ptr %p0v, align 8
  call void @__bennett_oracle(ptr @inc8, ptr %b, ptr %d)
  call void @__bennett_oracle(ptr @inc8, ptr %b, ptr %d)
  call void @__bennett_qfree(ptr %f)
  call void @__bennett_qfree(ptr %t)
  call void @__bennett_qfree(ptr %x)
  ret void
}
```

A two-argument function needs no packing wrapper (audit D21): two `IN` bindings, one 9-bit
target (the `zext` to `i9` makes the sum exact):

```llvm example=oracle-two-in verdict=accept candidates=add shapes=1
define internal i9 @add(i8 %a, i8 %b) {
  %a9 = zext i8 %a to i9
  %b9 = zext i8 %b to i9
  %s = add i9 %a9, %b9
  ret i9 %s
}

define void @top() {
  %d = alloca [96 x i8], align 8
  %qa = call ptr @__bennett_qalloc(i64 0, i64 8)
  %qb = call ptr @__bennett_qalloc(i64 0, i64 8)
  %t = call ptr @__bennett_qalloc(i64 0, i64 9)
  %f = call ptr @__bennett_qalloc(i64 0, i64 4)
  store <4 x i32> <i32 2, i32 2, i32 0, i32 0>, ptr %d, align 8
  %dt = getelementptr i8, ptr %d, i64 16
  store ptr %t, ptr %dt, align 8
  %df = getelementptr i8, ptr %d, i64 24
  store ptr %f, ptr %df, align 8
  %p0 = getelementptr i8, ptr %d, i64 32
  store <2 x i32> <i32 1, i32 0>, ptr %p0, align 8
  %p0q = getelementptr i8, ptr %d, i64 40
  store ptr %qa, ptr %p0q, align 8
  %p0v = getelementptr i8, ptr %d, i64 48
  store <2 x i64> zeroinitializer, ptr %p0v, align 8
  %p1 = getelementptr i8, ptr %d, i64 64
  store <2 x i32> <i32 1, i32 0>, ptr %p1, align 8
  %p1q = getelementptr i8, ptr %d, i64 72
  store ptr %qb, ptr %p1q, align 8
  %p1v = getelementptr i8, ptr %d, i64 80
  store <2 x i64> zeroinitializer, ptr %p1v, align 8
  call void @__bennett_oracle(ptr @add, ptr null, ptr %d)
  call void @__bennett_oracle(ptr @add, ptr null, ptr %d)
  call void @__bennett_qfree(ptr %f)
  call void @__bennett_qfree(ptr %t)
  call void @__bennett_qfree(ptr %qb)
  call void @__bennett_qfree(ptr %qa)
  ret void
}
```

A kind chosen at run time gives two shapes, `ARG` and `IN` for the second parameter; a classical
value read by the caller from host input is the `ARG` value:

```llvm example=oracle-two-shapes verdict=accept candidates=add shapes=2
define internal i9 @add(i8 %a, i8 %b) {
  %a9 = zext i8 %a to i9
  %b9 = zext i8 %b to i9
  %s = add i9 %a9, %b9
  ret i9 %s
}

define void @top(i1 %quantum_b, i64 %bval) {
  %d = alloca [96 x i8], align 8
  %qa = call ptr @__bennett_qalloc(i64 0, i64 8)
  %qb = call ptr @__bennett_qalloc(i64 0, i64 8)
  %t = call ptr @__bennett_qalloc(i64 0, i64 9)
  %f = call ptr @__bennett_qalloc(i64 0, i64 4)
  store <4 x i32> <i32 2, i32 2, i32 0, i32 0>, ptr %d, align 8
  %dt = getelementptr i8, ptr %d, i64 16
  store ptr %t, ptr %dt, align 8
  %df = getelementptr i8, ptr %d, i64 24
  store ptr %f, ptr %df, align 8
  %p0 = getelementptr i8, ptr %d, i64 32
  store <2 x i32> <i32 1, i32 0>, ptr %p0, align 8
  %p0q = getelementptr i8, ptr %d, i64 40
  store ptr %qa, ptr %p0q, align 8
  %p0v = getelementptr i8, ptr %d, i64 48
  store <2 x i64> zeroinitializer, ptr %p0v, align 8
  %k1 = select i1 %quantum_b, i32 1, i32 2
  %p1 = getelementptr i8, ptr %d, i64 64
  store i32 %k1, ptr %p1, align 8
  %p1m = getelementptr i8, ptr %d, i64 68
  store i32 0, ptr %p1m, align 4
  %p1q = getelementptr i8, ptr %d, i64 72
  store ptr %qb, ptr %p1q, align 8
  %p1v = getelementptr i8, ptr %d, i64 80
  store i64 %bval, ptr %p1v, align 8
  %p1s = getelementptr i8, ptr %d, i64 88
  store i64 0, ptr %p1s, align 8
  call void @__bennett_oracle(ptr @add, ptr null, ptr %d)
  call void @__bennett_oracle(ptr @add, ptr null, ptr %d)
  call void @__bennett_qfree(ptr %f)
  call void @__bennett_qfree(ptr %t)
  call void @__bennett_qfree(ptr %qb)
  call void @__bennett_qfree(ptr %qa)
  ret void
}
```

A 160-bit output (an `OUT` buffer of 20 bytes) has k = 2 slices, [0, 128) and [128, 160) of the
`OUT` register, so each invocation is the `wide` event with 2k − 1 = 3 oracle calls (§8.6):

```llvm example=oracle-wide-out verdict=accept candidates=fill20 shapes=1
define internal void @fill20(ptr %out, i8 %x) {
entry:
  br label %loop

loop:
  %i = phi i64 [ 0, %entry ], [ %i2, %loop ]
  %ti = trunc i64 %i to i8
  %v = xor i8 %x, %ti
  %p = getelementptr i8, ptr %out, i64 %i
  store i8 %v, ptr %p
  %i2 = add i64 %i, 1
  %c = icmp ult i64 %i2, 20
  br i1 %c, label %loop, label %done

done:
  ret void
}

define void @top() {
  %d = alloca [96 x i8], align 8
  %qx = call ptr @__bennett_qalloc(i64 0, i64 8)
  %qo = call ptr @__bennett_qalloc(i64 0, i64 160)
  %f = call ptr @__bennett_qalloc(i64 0, i64 4)
  store <4 x i32> <i32 2, i32 2, i32 0, i32 0>, ptr %d, align 8
  %dt = getelementptr i8, ptr %d, i64 16
  store ptr null, ptr %dt, align 8
  %df = getelementptr i8, ptr %d, i64 24
  store ptr %f, ptr %df, align 8
  %p0 = getelementptr i8, ptr %d, i64 32
  store <2 x i32> <i32 4, i32 0>, ptr %p0, align 8
  %p0q = getelementptr i8, ptr %d, i64 40
  store ptr %qo, ptr %p0q, align 8
  %p0v = getelementptr i8, ptr %d, i64 48
  store <2 x i64> <i64 0, i64 20>, ptr %p0v, align 8
  %p1 = getelementptr i8, ptr %d, i64 64
  store <2 x i32> <i32 1, i32 0>, ptr %p1, align 8
  %p1q = getelementptr i8, ptr %d, i64 72
  store ptr %qx, ptr %p1q, align 8
  %p1v = getelementptr i8, ptr %d, i64 80
  store <2 x i64> zeroinitializer, ptr %p1v, align 8
  call void @__bennett_oracle(ptr @fill20, ptr null, ptr %d)
  call void @__bennett_oracle(ptr @fill20, ptr null, ptr %d)
  call void @__bennett_qfree(ptr %f)
  call void @__bennett_qfree(ptr %qo)
  call void @__bennett_qfree(ptr %qx)
  ret void
}
```

In-place pairs (§8.7): a verified pair, a wrong inverse, a classical parameter with a finite
value set (one `qinplace` per value), and a quantum parameter (BLK-3). The descriptor of
`inplace` has `tgt` = null; the INOUT register is `param[0].q`:

```llvm example=inplace-call verdict=accept candidates=add5,sub5
define internal i8 @add5(i8 %x) {
  %r = add i8 %x, 5
  ret i8 %r
}

define internal i8 @sub5(i8 %x) {
  %r = add i8 %x, 251
  ret i8 %r
}

define void @top() {
  %d = alloca [64 x i8], align 8
  %x = call ptr @__bennett_qalloc(i64 0, i64 8)
  %f = call ptr @__bennett_qalloc(i64 0, i64 4)
  store <4 x i32> <i32 2, i32 1, i32 0, i32 0>, ptr %d, align 8
  %dt = getelementptr i8, ptr %d, i64 16
  store ptr null, ptr %dt, align 8
  %df = getelementptr i8, ptr %d, i64 24
  store ptr %f, ptr %df, align 8
  %p0 = getelementptr i8, ptr %d, i64 32
  store <2 x i32> <i32 5, i32 0>, ptr %p0, align 8
  %p0q = getelementptr i8, ptr %d, i64 40
  store ptr %x, ptr %p0q, align 8
  %p0v = getelementptr i8, ptr %d, i64 48
  store <2 x i64> zeroinitializer, ptr %p0v, align 8
  call void @__bennett_inplace(ptr @add5, ptr @sub5, ptr null, ptr %d)
  call void @__bennett_inplace(ptr @sub5, ptr @add5, ptr null, ptr %d)
  call void @__bennett_qfree(ptr %f)
  call void @__bennett_qfree(ptr %x)
  ret void
}
```

```llvm example=inplace-wrong-inverse verdict=reject:BD-E-INPLACE-NOT-INVERSE
define internal i8 @add5(i8 %x) {
  %r = add i8 %x, 5
  ret i8 %r
}

define void @top() {
  %d = alloca [64 x i8], align 8
  %x = call ptr @__bennett_qalloc(i64 0, i64 8)
  %f = call ptr @__bennett_qalloc(i64 0, i64 4)
  store <4 x i32> <i32 2, i32 1, i32 0, i32 0>, ptr %d, align 8
  %dt = getelementptr i8, ptr %d, i64 16
  store ptr null, ptr %dt, align 8
  %df = getelementptr i8, ptr %d, i64 24
  store ptr %f, ptr %df, align 8
  %p0 = getelementptr i8, ptr %d, i64 32
  store <2 x i32> <i32 5, i32 0>, ptr %p0, align 8
  %p0q = getelementptr i8, ptr %d, i64 40
  store ptr %x, ptr %p0q, align 8
  %p0v = getelementptr i8, ptr %d, i64 48
  store <2 x i64> zeroinitializer, ptr %p0v, align 8
  call void @__bennett_inplace(ptr @add5, ptr @add5, ptr null, ptr %d)
  call void @__bennett_qfree(ptr %f)
  call void @__bennett_qfree(ptr %x)
  ret void
}
```

```llvm example=inplace-arg-finite verdict=accept candidates=addk,subk
define internal i8 @addk(i8 %x, i8 %k) {
  %r = add i8 %x, %k
  ret i8 %r
}

define internal i8 @subk(i8 %x, i8 %k) {
  %r = sub i8 %x, %k
  ret i8 %r
}

define void @top(i1 %big) {
  %d = alloca [96 x i8], align 8
  %x = call ptr @__bennett_qalloc(i64 0, i64 8)
  %f = call ptr @__bennett_qalloc(i64 0, i64 4)
  store <4 x i32> <i32 2, i32 2, i32 0, i32 0>, ptr %d, align 8
  %dt = getelementptr i8, ptr %d, i64 16
  store ptr null, ptr %dt, align 8
  %df = getelementptr i8, ptr %d, i64 24
  store ptr %f, ptr %df, align 8
  %p0 = getelementptr i8, ptr %d, i64 32
  store <2 x i32> <i32 5, i32 0>, ptr %p0, align 8
  %p0q = getelementptr i8, ptr %d, i64 40
  store ptr %x, ptr %p0q, align 8
  %p0v = getelementptr i8, ptr %d, i64 48
  store <2 x i64> zeroinitializer, ptr %p0v, align 8
  %k = select i1 %big, i64 7, i64 1
  %p1 = getelementptr i8, ptr %d, i64 64
  store <2 x i32> <i32 2, i32 0>, ptr %p1, align 8
  %p1q = getelementptr i8, ptr %d, i64 72
  store ptr null, ptr %p1q, align 8
  %p1v = getelementptr i8, ptr %d, i64 80
  store i64 %k, ptr %p1v, align 8
  %p1s = getelementptr i8, ptr %d, i64 88
  store i64 0, ptr %p1s, align 8
  call void @__bennett_inplace(ptr @addk, ptr @subk, ptr null, ptr %d)
  call void @__bennett_qfree(ptr %f)
  call void @__bennett_qfree(ptr %x)
  ret void
}
```

```llvm example=inplace-param-quantum verdict=blocked:BD-B-ISA3
define internal i8 @addk(i8 %x, i8 %k) {
  %r = add i8 %x, %k
  ret i8 %r
}

define internal i8 @subk(i8 %x, i8 %k) {
  %r = sub i8 %x, %k
  ret i8 %r
}

define void @top() {
  %d = alloca [96 x i8], align 8
  %x = call ptr @__bennett_qalloc(i64 0, i64 8)
  %y = call ptr @__bennett_qalloc(i64 0, i64 8)
  %f = call ptr @__bennett_qalloc(i64 0, i64 4)
  store <4 x i32> <i32 2, i32 2, i32 0, i32 0>, ptr %d, align 8
  %dt = getelementptr i8, ptr %d, i64 16
  store ptr null, ptr %dt, align 8
  %df = getelementptr i8, ptr %d, i64 24
  store ptr %f, ptr %df, align 8
  %p0 = getelementptr i8, ptr %d, i64 32
  store <2 x i32> <i32 5, i32 0>, ptr %p0, align 8
  %p0q = getelementptr i8, ptr %d, i64 40
  store ptr %x, ptr %p0q, align 8
  %p0v = getelementptr i8, ptr %d, i64 48
  store <2 x i64> zeroinitializer, ptr %p0v, align 8
  %p1 = getelementptr i8, ptr %d, i64 64
  store <2 x i32> <i32 1, i32 0>, ptr %p1, align 8
  %p1q = getelementptr i8, ptr %d, i64 72
  store ptr %y, ptr %p1q, align 8
  %p1v = getelementptr i8, ptr %d, i64 80
  store <2 x i64> zeroinitializer, ptr %p1v, align 8
  call void @__bennett_inplace(ptr @addk, ptr @subk, ptr null, ptr %d)
  call void @__bennett_qfree(ptr %f)
  call void @__bennett_qfree(ptr %y)
  call void @__bennett_qfree(ptr %x)
  ret void
}
```

```text blocker=inplace-param-quantum
BD-B-ISA3 @top call @__bennett_inplace(@addk, @subk): parameter 1 is bound IN (register %y); ISA 0.8 qinplace has no (ins..) (mem..) (args..); BLK-3 (ISA-3) qinplace @g @ginv tk x (ins..) (mem..) (args..)
```

## 9. Budgets

NS §3.1: a region-level classical budget of "dynamic steps, heap bytes and recursion depth,
passed as ordinary integer operands of the region-entry marker or supplied out of band by the
host or driver (a project-wide default, a per-function table) … No per-loop source annotation is
ever required". Budgets are the ISA's four components (ISA §5.4).

### 9.1 The budget record

Every region-entry marker takes a `ptr` to a **budget record** (outline E1, E12), the LLVM struct
`{ i64, i64, i64, i64, ptr }` under the datalayout (C `bennett_budget`, §3.3):

| Field | Meaning |
|---|---|
| `steps` | B: reference-interpreter rows (§9.4) |
| `heap` | `heap_limit`: heap bytes (ISA §5.4) |
| `stack` | `stack_limit`: lifted stack cells (ISA §3.7) |
| `depth` | `depth_limit`: call depth |
| `fault` | action regions only: the caller's fault register (4 wires) that receives the combined fault of the region's coherent slices (§10, TDL-8), or null |

A field equal to `BENNETT_BUDGET_TABLE` (all ones) takes its value from the budget table
(§9.2). A null record means all four budget fields come from the table and `fault` is null. For
`oracle` and `inplace` the `fault` field is ignored: the descriptor names the fault register
(§8.2).

### 9.2 The budget table

The **budget table** is a driver input (`--bennett-budgets=<file>`), one JSON document in RFC
8785 canonical form:

```
{ "version": "0.2",
  "defaults": { "steps": D, "heap": D, "stack": D, "depth": D, "sstack": D },
  "entries": [ { ("identity": HEX64 | "region_key": HEX64 | "symbol": GLOB),
                 "steps"?: D, "heap"?: D, "stack"?: D, "depth"?: D, "sstack"?: D } … ] }
```

with D a decimal string. An entry matches a region by its identity (§7.3, the interface hash of
`@ref` of one shape), its region key (§7.3), or a glob over the source symbol name of the region
function (`*` and `?`). For each component a region takes, in order of precedence, the first
entry matching by identity, then by region key, then by symbol (in array order), that names the
component, else the default. Defaults absent from the table and from
`--bennett-budget-default=<s,h,st,d,ss>` are 1048576 steps, 1048576 heap bytes, 65536 stack
cells, depth 256 and `sstack` 65536 (§24). `sstack` is the shadow-stack size in bytes (§17.3),
part of the heap budget. The driver resolves every symbol entry to identities and records the
resolved table and its SHA-256 in the build record (§19.9).

```json budget-table=rung4-mini
{"defaults":{"depth":"64","heap":"0","sstack":"0","stack":"1024","steps":"100000"},"entries":[{"depth":"8","heap":"0","stack":"512","steps":"400","symbol":"q"}],"version":"0.2"}
```

*(non-normative)* This is the budget table of the reduced rung-4 link of §16.7: the entry names
the region function `q` by symbol; the defaults govern every other region of that link. Its
largest heap (0) and stack (1024) fix that link's `heap_limit_max` and `S_cells` (§16.3); the
entry's 400 steps, 512 cells and depth 8 cover the 112 steps, 126 cells and depth 4 that the
runs of §16.7 need.

### 9.3 What each budget governs

| Region | Budget | Exhaustion |
|---|---|---|
| `oracle`, `inplace` | the token of every oracle invocation (ISA §5.4, §10 `bennett_budget`) | F_B = (0, `FAULT_BUDGET_STEPS` / `_HEAP` / `_DEPTH`) on that input (ISA §5.2) |
| `ctrl`, `adj`, `compute` | the token of **every coherent slice** of the invocation, each with the full record (outline E2) | that slice's fault code, combined into the action's fault register (TDL-8) |
| `reversible`, and the whole-program R mode | an R-tier step, heap and depth counter (§17.6) | the R run ends with a budget fault record (§17.6) |
| device CC code outside regions | none: classical control is "genuinely dynamic" (NS §4.2) | – |

### 9.4 The budget unit

One step is one reference-interpreter row of the reference object (ISA §14.1): the wrapper of
§16.2 (including the entry-state replay of §8.5 and the shadow-stack setup of §17.3) and every
lproc row, so the fault set is a property of the program, the budget, the LLVM version and
pipeline, the normaliser and mapping versions and the runtimes version, never of the plugin's
lowering (NS §4.2). Heap bytes are counted by `lift.alloc` (`heap_used + max(n, 1)`), stack cells
by `lift.call` (R_f cells per call, ISA §3.7, monotonic), depth by `lift.call`/`lift.ret`. The
R-tier unit is §17.6.

### 9.5 Run-time budgets

A budget field of a record is resolved, in this order:

1. **Static**: a constant, `BENNETT_BUDGET_TABLE`, or a finite value set (§5.3). The driver's
   launch stub mints one token per (reference object, budget tuple) with `bennett_budget` (ISA
   §10) at launch and passes them to the CC entry as `TOKEN` arguments; the CC code selects one
   by the compare tree of §14.2.
2. **Launch-supplied**: a field whose abstract value is a bitwise copy of an integer parameter of
   the device entry (its atoms come only from PT11 for that parameter). The launch stub mints the
   token from the host's argument value before `bennett_run`, for every reference object the
   record may reach (a finite set), and passes it as a `TOKEN` argument. A value that
   `bennett_budget` rejects (ISA §5.4 validation) makes the stub fail the launch with that status.
3. **Device-computed**: any other field (arithmetic on inputs, values derived from measurement
   results). ISA 0.8 has no instruction that mints a token from a device value: the verdict is
   `blocked:BD-B-ISA1` (BLK-2, §25.1), naming the field.

Exhaustion is always a fault outcome on the inputs that exhaust it (NS §3.1, §4.2), never a
compile error and never a truncated result. Rounding a run-time budget to a pre-minted value is
not permitted: it would change F_B (outline B5).

```llvm example=budget-launch-arg verdict=accept candidates=inc8 shapes=1
define internal i8 @inc8(i8 %x) {
  %r = add i8 %x, 1
  ret i8 %r
}

define void @run(i64 %steps) {
  %d = alloca [64 x i8], align 8
  %b = alloca [40 x i8], align 8
  %x = call ptr @__bennett_qalloc(i64 0, i64 8)
  %t = call ptr @__bennett_qalloc(i64 0, i64 8)
  %f = call ptr @__bennett_qalloc(i64 0, i64 4)
  store i64 %steps, ptr %b, align 8
  %b1 = getelementptr i8, ptr %b, i64 8
  store <2 x i64> <i64 -1, i64 -1>, ptr %b1, align 8
  %b3 = getelementptr i8, ptr %b, i64 24
  store i64 -1, ptr %b3, align 8
  %bf = getelementptr i8, ptr %b, i64 32
  store ptr null, ptr %bf, align 8
  store <4 x i32> <i32 2, i32 1, i32 0, i32 0>, ptr %d, align 8
  %dt = getelementptr i8, ptr %d, i64 16
  store ptr %t, ptr %dt, align 8
  %df = getelementptr i8, ptr %d, i64 24
  store ptr %f, ptr %df, align 8
  %p0 = getelementptr i8, ptr %d, i64 32
  store <2 x i32> <i32 1, i32 0>, ptr %p0, align 8
  %p0q = getelementptr i8, ptr %d, i64 40
  store ptr %x, ptr %p0q, align 8
  %p0v = getelementptr i8, ptr %d, i64 48
  store <2 x i64> zeroinitializer, ptr %p0v, align 8
  call void @__bennett_oracle(ptr @inc8, ptr %b, ptr %d)
  call void @__bennett_oracle(ptr @inc8, ptr %b, ptr %d)
  call void @__bennett_qfree(ptr %f)
  call void @__bennett_qfree(ptr %t)
  call void @__bennett_qfree(ptr %x)
  ret void
}
```

```llvm example=budget-device-computed verdict=blocked:BD-B-ISA1
define internal i8 @inc8(i8 %x) {
  %r = add i8 %x, 1
  ret i8 %r
}

define void @run() {
entry:
  %d = alloca [64 x i8], align 8
  %b = alloca [40 x i8], align 8
  %c = call ptr @__bennett_qalloc(i64 0, i64 64)
  br label %coin

coin:
  %i = phi i64 [ 0, %entry ], [ %i2, %next ]
  %acc = phi i64 [ 0, %entry ], [ %acc2, %next ]
  call void @__bennett_gate(i32 2, ptr %c, i64 %i)
  %m = call i1 @__bennett_measure(ptr %c, i64 %i)
  %mz = zext i1 %m to i64
  %sh = shl i64 %mz, %i
  %acc2 = or i64 %acc, %sh
  br i1 %m, label %reset, label %next

reset:
  call void @__bennett_gate(i32 1, ptr %c, i64 %i)
  br label %next

next:
  %i2 = add i64 %i, 1
  %more = icmp ult i64 %i2, 64
  br i1 %more, label %coin, label %go

go:
  %steps = add i64 %acc2, 5
  %x = call ptr @__bennett_qalloc(i64 0, i64 8)
  %t = call ptr @__bennett_qalloc(i64 0, i64 8)
  %f = call ptr @__bennett_qalloc(i64 0, i64 4)
  store i64 %steps, ptr %b, align 8
  %b1 = getelementptr i8, ptr %b, i64 8
  store <2 x i64> <i64 -1, i64 -1>, ptr %b1, align 8
  %b3 = getelementptr i8, ptr %b, i64 24
  store i64 -1, ptr %b3, align 8
  %bf = getelementptr i8, ptr %b, i64 32
  store ptr null, ptr %bf, align 8
  store <4 x i32> <i32 2, i32 1, i32 0, i32 0>, ptr %d, align 8
  %dt = getelementptr i8, ptr %d, i64 16
  store ptr %t, ptr %dt, align 8
  %df = getelementptr i8, ptr %d, i64 24
  store ptr %f, ptr %df, align 8
  %p0 = getelementptr i8, ptr %d, i64 32
  store <2 x i32> <i32 1, i32 0>, ptr %p0, align 8
  %p0q = getelementptr i8, ptr %d, i64 40
  store ptr %x, ptr %p0q, align 8
  %p0v = getelementptr i8, ptr %d, i64 48
  store <2 x i64> zeroinitializer, ptr %p0v, align 8
  call void @__bennett_oracle(ptr @inc8, ptr %b, ptr %d)
  call void @__bennett_oracle(ptr @inc8, ptr %b, ptr %d)
  call void @__bennett_qfree(ptr %f)
  call void @__bennett_qfree(ptr %t)
  call void @__bennett_qfree(ptr %x)
  call void @__bennett_qfree(ptr %c)
  ret void
}
```

```text blocker=budget-device-computed
BD-B-ISA1 @run call @__bennett_oracle(@inc8): budget field steps = 5 + a 64-bit value assembled from 64 measurement outcomes (value set TOP); ISA 0.8 mints tokens only at launch; BLK-2 (ISA-1) CC tk = budget.mint @region s h st d
```

*(non-normative)* In `budget-device-computed` the oracle's budget depends on measurement outcomes:
NS §4.2 "run-time budgets come from the host or from measurement results". `%acc2` is a loop phi
over 64 measured bits, so its value set is ⊤ (it has 2^64 possible values, beyond K = 4096 atoms);
it is neither static nor a bitwise copy of a launch argument, and no launch-time set of tokens
covers it. Each wire of `%c` measured 1 is reset by an `x`, so `%c` is clean at its `qfree`
(ISA §3.3).

## 10. Taint-driven lifting under control (tdl 0.2)

NS §0: "a way to condition a region on a qubit. Everything else is inferred"; NS §3.1 taint row:
a context-sensitive interprocedural analysis "over data dependence, control dependence and
memory effects, from marker results and region entries … with polyvariant specialisation". This
section replaces 0.1's generation-only semantics, in which classical stores of a `ctrl` body
happened on both branches of the control (audit 1.4-d, R1). Rule ids TDL-1 to TDL-12 are
normative anchors. ISA 0.8 expresses every construct below: actions call oracles (ISA §5.3,
§4.7) and CC issues controlled region calls (ISA §4.7 `ctl w <call>`).

**TDL-1 Interface vs body.** The marker fixes the interface: `ctrl`, `adj` and `compute` give an
action; `oracle` and `inplace` give an oracle. The body of an action region is partitioned by
content (TDL-3) and is never rejected for containing classical code.

**TDL-2 Coherence states.**

- **Object state.** Every instance of an abstract object X has a dynamic state K(X) ∈ {Cl, M,
  Co}, kept by the CC tier (a runtimes table for globals, the coherent allocator's bookkeeping
  for heap objects; §11, §17): Cl (the CC **shadow** holds X's bytes; X's arena cells are |0⟩),
  M (materialised: the arena cells hold the same bytes as a basis state; both are valid), Co
  (the arena is the truth and may be superposed; the shadow is invalid). Every instance starts
  Cl. Transitions: Cl → M by **materialisation** (an uncontrolled XOR of the shadow into the
  arena cells, TDL-4); M → Cl by the same XOR (dematerialisation, before a CC store to X); M or
  Cl → Co when an event is applied (§18.2) that writes X's cells with a non-empty control set or
  with a Co value; Co → Cl by `__bennett_observe` of all of X's bytes (TDL-11) or by its release
  (free, end of lifetime).
- **Value state.** During a generation (§18.4) every executed SSA value instance is Cl or Co:
  Co iff it is a deferred measurement result (§7.5a), a load of a byte whose **view** (below) is
  Co, the result of an instruction with a Co operand, or a `phi` at the join of a Co branch.
- **View.** A generation sees outliving memory through a **view**: a byte of object X has view
  Co if K(X) = Co, or if the generation's recorder (or a recorder of an enclosing generation of
  the same invocation) holds an event that writes it with a non-empty control set or with a Co
  value; otherwise its view is Cl and its value is the shadow updated by the recorder's own
  classical events. *(non-normative)* Inside `ctrl(q, f)` the body's own stores are recorded
  without q (q is added when the generation ends, TDL-6), so f sees its own writes classically,
  as the q = 1 branch must; an inner `ctrl(q2, g)` records g's writes with q2, so f's later reads
  of them are Co.
- **Static may-Co analysis MC** (decides partitions, arena placement and the verdict rules
  below; flow-sensitive, interprocedural over the CC call graph with one summary per (function,
  coherence signature), merge by union, least fixpoint):
  - MC1: the state at a program point is the set of abstract objects that may have K = Co there;
  - MC2: after an action region invocation (`ctrl`, `adj`, `compute`, or a `reversible` call
    reached from a generation, §7.4), add every outliving object (TDL-5) that a store in the
    closure of a candidate may write, if the invocation is `ctrl` or the store may be under an
    inner control, may store a may-Co value, or may be control-dependent on a may-Co branch;
  - MC3: `__bennett_observe(p, len)` removes an object X when AV(p) = {(X, 0)} and len is a
    constant ≥ size(X); otherwise no change;
  - MC4: a value may be Co if an operand may be Co, it is a load whose AV(p) contains a may-Co
    object, or it is control-dependent on a may-Co branch; an object that a may-Co value is
    stored into is may-Co after the store;
  - MC5: calls bind the coherence signature of the callee (which parameters may be Co, and the
    may-Co set at entry); every distinct signature is a variant (§4.3).
- **Interprocedural and context-sensitive** by coherence signature (MC5; NS §3.1).

**TDL-3 Partition.** For each variant of an action region and of its CC callees:

- **G (generation)**: the instructions MC does not mark may-Co. G runs in CC, once per
  invocation (§18.4).
- **Slices**: every maximal single-entry single-exit region of may-Co instructions other than
  stores to outliving objects and marker calls is outlined (LLVM `CodeExtractor`) into a
  **slice function** S_k, with: classical live-ins → `ARG` parameters; Co live-ins → `IN`
  parameters; may-Co objects it loads → the arena, bound as a `MEM_IN` region `coh`; Co
  live-outs → outputs (§8.6). An irreducible may-Co region is outlined as a whole function. S_k
  is normalised (§12) and lifted (§16) like any oracle region; its entry state is the
  generation's view (§8.5: the arena for may-Co objects, the shadow for the rest). Each slice
  also keeps its original instructions as a **classical twin** in G.
- At run time the generation runs the classical twin when every live-in of the slice is Cl and
  every object it may load has view Cl; otherwise it records a **slice invocation**: before it,
  every live instance of a may-Co object the slice may load whose state is Cl is materialised
  (Cl → M); the invocation computes the Co live-outs into fresh registers (`compute` events,
  §18.2).
- **Stores to outliving objects** and **marker calls** are never inside slices: they become
  events (TDL-5, TDL-10). A store or marker call that is control-dependent on a Co branch is
  recorded under the branch's condition wire (TDL-10). A Co branch is if-converted: the
  generation executes both arms (each arm's Cl instructions classically, its events predicated on
  the condition or its negation) and the join's `phi`s become slice-computed selects.

**TDL-4 Coherent arena.**

- The objects in any may-Co set of MC are placed in the **arena**: a static address range
  [A_coh, A_coh + 2^A) of the layout, disjoint from CC globals and heap (ISA §7.1, §7.2; G-13
  would lift the restriction). Globals in the set are relocated into the arena by the layout
  (§19.5) in both builds, so their addresses stay native-equal; heap objects of may-Co allocation
  sites are allocated by the runtimes' **coherent allocator** in the arena range in both builds.
- The arena's contents are a CC-held register of 8·2^A wires, bound to every slice and arena
  action as `region[A,8]` (ISA §3.3 binding); cell i is the byte at address A_coh + i.
- The **shadow** of the arena is the CC global `__bennett_rt_shadow` of 2^A bytes at
  A_coh + Δ_sh (a layout constant); CC loads and stores whose abstract address may lie in the
  arena are rewritten to address + Δ_sh when the object's state is Cl or M, after
  dematerialising an M object for a store; when the state is Co, TDL-11 applies.
- **Writing at a run-time address.** A cell write of a classical mask m at a classical run-time
  address a (an `xmask` event, a materialisation) lowers to an action that calls the runtime
  oracle `@xorargs` (§16.5) to XOR the classical `args` (a, m) into fresh wires a_w, m_w, then
  `qstore coh a_w m_w` (ISA §4.6: XOR into the addressed cell; O(2^A) gates unless the target has
  QRAM, NS §4.3), then `@xorargs` again to uncompute a_w and m_w. Objects at static offsets MAY
  use a static slice (`qreg.slice` with a literal `lo`) and X gates instead.

**TDL-5 Stores to outliving objects (the store rule).** An object **outlives** an invocation if
it is live after it: a global, an object reachable from `env`, or a heap object not freed in the
invocation. A store `store v, ptr p` executed during a generation to an outliving object X is
realised by cases on the view of the bytes it writes:

- **(a) View Cl** (the old bytes c are known to CC).
  - v and p Cl: the event `xmask X+o, c ⊕ v` (o = p − X's base).
  - v or p Co: a slice invocation O computes the address and the mask c ⊕ v into fresh
    registers (c is a classical argument of O); the event `xstore coh a_w m_w` XORs the mask
    into the addressed cells (`qstore`); a second identical invocation of O uncomputes the
    registers. O never loads X's written bytes from the arena (their view is Cl, so O receives
    them as arguments), and no instruction between the two invocations writes anything O reads,
    so the second invocation cleans them exactly (ISA §5.2 involution).
  - Exact; no history.
- **(b) View Co, and the update is a library bijection** in the old value: the materialised IR
  is `x = load X+o; y = op(x, k…); store y, X+o` with no intervening store to X, where op is one
  of: add or sub of k (wrapping at the access width), xor with k, rotate by a constant, negate,
  `bswap`, add of k modulo a constant m (with x < m), multiply by a constant k modulo m with
  gcd(k, m) = 1 (with x < m); or a declared `inplace` pair (§8.7). k may be Cl or Co (an
  `IN` binding of a slice output); k MUST NOT depend on X's written bytes. The event is the
  `bennett-arith` permutation action for op on the arena cells X+o with k as `in` or `args`
  (ISA §4.7), preceded by the slice invocation that computes a Co k and followed by its
  uncomputation. Exact.
- **(c) View Co, inside the `f` part of `compute(f, use, budget, env)`**: history. A slice
  invocation computes the new bytes into a fresh register t; the event `xchg coh a t` exchanges t
  with the cells (`qexchm`); t now holds the displaced bytes and is kept until adjoint(E_f)
  replays the events in reverse (`xchg` again, then the slice invocation again), which cleans it
  (NS §3.1 compute-with-uncompute; Bennett). `use` MUST NOT write bytes that f wrote by case (c)
  (`BD-E-COHERENT-OVERWRITE` otherwise: the replay would not restore them).
- **(d) Otherwise**: `BD-E-COHERENT-OVERWRITE`, decided statically: a store to an outliving
  object that MC says may be Co at the store, and that is neither (b) nor (c). NS §4.2: "writing
  a register not known to be clean is a compile-time error … an in-place update x ← g(x) requires
  a total bijection with a bounded inverse … else it fails loud". The diagnostic names the store
  and the object.

Stores to objects that do not outlive the invocation are workspace: G runs them on the
generation's view; slices run them in their private memory (§8.5); at exit the objects are
released. Allocation in a generation is unconditional, like every allocation in the ISA (ISA
§3.5); the release of an object that outlives the invocation is TDL-12.

**TDL-6 Control and adjoint.** `ctrl(q, qi, …)` adds wire q.qi to every event's control set
(ISA §4.7 `ctl w`). `oracle_call`, `qexch`, `qexchm`, `qstore`, X and `xmask` are self-adjoint
(ISA §5.3 adjoint table); `adj(f)` generates f from the current classical state and applies the
adjoint of the event list; `compute` reuses the recording E_f for its uncompute, so masks and
history match exactly.

**TDL-7 History.** The registers an invocation keeps beyond its own events (displaced bytes of
case (c), the condition flags of a Co loop (TDL-10), Co values whose computing slice cannot be
replayed before the invocation ends because an intervening event wrote something it read, and
the per-slice fault registers of TDL-8) are **declared mutable outputs** of the invocation (NS
§4.2: an action with coherent internal control is its padded unitary on its declared wires).
Inside `compute`'s f they are released by adjoint(E_f). Otherwise the plugin allocates them,
reports them in the certificate's frame descriptor (ISA §9.4 "retained history") and with the
warning `BD-W-COHERENT-HISTORY`, and releases them by `measure` in the CC epilogue of the run.
Every other Co value register is cleaned right after its last use by replaying its computing
slice invocation.

**TDL-8 Faults.** NS §4.2: "a quantum action has no fault outcome of its own: any fallible
computation it needs is a lifted oracle it calls, whose fault register it declares among its
outputs". Every slice invocation k gets a fresh 4-wire fault register f_k; the uncomputing
invocation uses a second fresh register f′_k, which is then cleaned by `qxor f_k f′_k` (both hold
the same code) and freed, so f_k holds the slice's code and is retained (TDL-7). At the end of
the invocation a runtime combine oracle `@firstfault` (§16.5) XORs the first nonzero code of
f_1, …, f_K in invocation order into the action's **declared fault register** Φ: the budget
record's `fault` field (§9.1), or, when that is null, a register the plugin allocates and
retains (TDL-7); the CC epilogue's `measure` of a plugin-allocated Φ records the outcome in the
run's fault statistics, and the certificate reports the rate (`fault_rate`, ISA §12.3). On a
faulting basis input a slice's payload is the canonical 0 (ISA §5.2), so the events it feeds
leave the arena unchanged there. A nonzero rate is a reported quantity (NS §4.2), not an error.

**TDL-9 Budget.** Every slice invocation's token comes from the region-entry marker's budget
record, each field completed from the budget table (§9); each slice gets the full record
(outline E2). Exhaustion is that slice's `FAULT_BUDGET_*` and reaches TDL-8.

**TDL-10 Co control of quantum operations and stores.**

- A marker call or outliving store that is control-dependent on a Co branch, or a marker call
  with a Co index or op code: a slice invocation computes the condition (and the index or code)
  into fresh wires; the event is issued under `qpred` of the condition wire, once per member of
  the index or code dispatch domain under the predicate "value = member" (ISA §3.5, §4.6); then
  the wires are uncomputed.
- A Co rotation angle is predicated per value when its value set is finite. Otherwise it is
  `BD-E-COHERENT-ANGLE`: NS promises predication, not superposed parameters, and ISA §3.1 "angles
  are literals or classical arguments fixed at region entry".
- A loop whose trip count is Co is unrolled in the event list up to N = the `steps` field of the
  budget record: iteration i is predicated on the flag c_i (c_1 = the first continuation
  condition, c_{i+1} = c_i ∧ condition_i, computed by `ccx` into fresh wires); the flags are
  history (TDL-7); if c_{N+1} may be 1 the invocation records `FAULT_BUDGET_STEPS` under c_{N+1}
  into Φ. G-14 (§25.3) is the efficient form.
- A `qalloc`/`qborrow` whose n is Co allocates the maximum of n's value set, padded to its bound
  (NS §4.2: "an allocation whose size depends on a qubit is padded to its bound"); gates on wires
  at or beyond the run-time n are predicated off. An unbounded value set is BLK-1 (§25.1).

**TDL-11 After the region.**

- Code that reads an object whose state is Co, inside the closure of a later region entry, is
  part of that region's slices (TDL-3).
- Code outside every region that may read a may-Co object is compiled in two variants (Cl and
  Co signatures, §4.3), selected by the object's dynamic state. Its Co variant at host or CC
  level traps (`T-TAINT-HOST`, fault code 4), and statically the plugin warns
  (`BD-W-TAINT-HOST`, naming `__bennett_observe`): NS §4.2, classical outputs of coherent memory
  leave only through measurement.
- `__bennett_observe(p, len)` makes bytes Cl by measurement. On ISA 0.8 `measure` consumes a
  whole live non-view register (ISA §3.3), so it lowers to: an action that `qload`-copies the
  addressed cells into a fresh register r of 8·len wires; `measure r`, which collapses the arena
  cells identically (a computational-basis measurement of a CNOT copy equals one of the source);
  the outcome written to the shadow; an `xmask` of the outcome out of the arena cells, returning
  them to |0⟩; K := Cl for every object whose bytes are all observed. Bytes whose state is Cl or M
  are left as they are (an M object is dematerialised).

**TDL-12 Effects in action regions.** An action region is coherent (NS §4.2: "closed and
effect-free"). An effect marker, a host call (§11.4), or the release of an object that outlives
the invocation, reached in the generation of an action region (in G or in a slice), cannot be
recorded as a unitary event. On the executions that reach it the effect does not occur and the
event `fault 8` (`FAULT_EFFECT_UNMODELLED`) is recorded: at application it XORs 8 into a fresh
retained fault register f_k under the event's control set, which TDL-8 combines into Φ like a
slice's (NS §4.2: "an effect the device cannot virtualise is a fault code on the executions
that reach it"). The coverage report has a
`trapped` line for it. Effects inside oracle regions are §11.3.

## 11. Effects and device models per tier (effects 0.2)

### 11.1 Tier table

NS §4.2's effects table, made concrete. The four device models are the ISA's (ISA §7.3):
`console`, `clock`, `entropy`, `block`.

| Tier | Realisation of an effect marker (§3.2) | Other effects |
|---|---|---|
| H | – (host code calls its own libc; markers are never called from H) | real |
| CC | `hostcall bennett.dev.<model>.<op>` (ISA §10): a genuine host effect, since ISA `effect` is R-only (ISA §4.1); the host's reply carries the bytes a read returns | host functions by `hostcall` (§11.4) |
| R | ISA `effect <model>.<op>` on the effect tape, reversed by whole-run reversal (ISA §7.3, §10) | – (R makes no host calls) |
| L | the lifted device model of §11.3 over state bound by the descriptor (§8.3) | – |
| action regions | `fault 8` into the action's fault register (TDL-12) | same |
| unmodelled | F(8) with a `trapped` coverage line (§4.5) | same |

### 11.2 Effect markers in the R tier

`__bennett_effect_<model>_<op>(…)` lowers to ISA `effect <model>.<op> …` with the operands in
ISA §7.3 order: `console.write(ptr, len)`, `clock.read(ptr)`, `entropy.read(ptr, len)`,
`block.read(sector, ptr)`, `block.write(sector, ptr)`. A failing ISA validation (operands out of
range, entropy tape exhausted) is the ISA's fault record (ISA §7.3, code 10 for entropy). The
driver declares the models in `devices.models` (ISA §9.1) and supplies `block_image` from
`--bennett-disk=<file>` (§19.2). `bennett-runtimes`' musl maps system calls onto the markers:

| musl | Effect |
|---|---|
| `write(1, …)`, `write(2, …)`, `writev` on fds 1 and 2 | `console.write` |
| `clock_gettime`, `gettimeofday`, `time` | `clock.read`: the 8-byte counter c; `CLOCK_REALTIME` and `CLOCK_MONOTONIC` both give tv_sec = c / 10^9, tv_nsec = c mod 10^9 |
| `getrandom`, reads of `/dev/urandom` and `/dev/random` | `entropy.read` |
| block-device reads and writes (the platform's virtio-blk, §20.3) | `block.read`, `block.write` |
| files | a runtimes VFS over the block device, or over a data-image file system linked as a global |

Device models beyond the four arrive with an ISA version (ISA §17 item 3, a mechanics
deferral, §24): until then an effect on another device is `FAULT_EFFECT_UNMODELLED`.

### 11.3 Coherent tier: lifted device models

In an L variant, an effect marker call becomes a call of the runtimes function
`__bennett_dev_<model>_<op>` with the same operands. These are ordinary C functions of
`bennett-runtimes`, lifted like any code, over the **device state**: runtimes globals
`__bennett_dev_<model>_*` that the oracle wrapper's prologue (§16.2) initialises from the
descriptor's device bindings (§8.3) before the region function runs. Their contract:

| Model | State set by the prologue | Operation |
|---|---|---|
| `entropy` | base = `lift.addr @e0`, size = 2^A bytes, pos = 0 | `read(p, len)`: if len > size − pos, `__bennett_nz_fault(10)` (`FAULT_ENTROPY_EXHAUSTED`); else copy [base + pos, base + pos + len) to p and pos += len |
| `block` | base = `lift.addr @k0`, nsect = 2^A′; an empty overlay | `read(s, p)`: the overlay's 512 bytes for sector s if present, else sector s of the region if s < nsect, else 512 zero bytes (ISA §7.3: absent sectors read as zero); `write(s, p)`: copy 512 bytes into the overlay entry for s (a heap allocation by `malloc`, lifted to `lift.alloc`) |
| `clock` | c = `value` | `read(p)`: store c (8 bytes, little-endian) at p, then c += 1 |
| `console` | L = n(q)/8 (0 for a null q), a buffer of L bytes in the oracle's heap, n = 0 | `write(p, len)`: copy the first min(len, L − n) bytes to buffer[n…], n += that count; further bytes are discarded with the oracle's other writes |

A model without a binding is unbound: every operation on it is `__bennett_nz_fault(8)` on the
executions that reach it (NS §4.2). The `entropy` fault code 10 in an oracle: ISA §4.2 admits
`fault C` for every C < 2^F; ISA §5.4 labels code 10 "(R only)", which §25.2 records as a wording
item. The bound console buffer's bytes are output slices (§8.6).

### 11.4 Host calls from CC

A CC variant's call of an H function (§4.5 item 3) becomes `hostcall bennett.call/<h>` where
`<h>` is the hex SHA-256 of the callee's symbol name: the argument block holds the scalar
arguments (little-endian, in order) and, for each pointer argument whose pointee the analysis
proves pointer-free (no slot holds a pointer atom, §5), the pointee's byte range as an
(offset, length) pair and the bytes themselves. The host-side stub calls the function on a copy,
writes back the bytes of pointer arguments, and replies with the result and the written bytes.
A pointer argument whose pointee may contain pointers read by device code does not become a host
call: the callee is **promoted** to a CC variant (§19.4; ISA-11 would let it stay native, an
efficiency item). Every service is declared in `devices.services` (ISA §9.1, §10).

### 11.5 Fault codes reported from CC

ISA 0.8 does not say which code a CC trap reports (ISA-7, §25.2). `__bennett_nz_fault(C)` in CC
therefore lowers to `hostcall bennett.fault` with the 8-byte payload C, then `trap`: the driver's
host stub records C as the run's fault code. In R it lowers to `trap`; the R fault record's code
is the ISA's until ISA-7 is settled (§25.2).

### 11.6 Examples

The R-tier console: a whole program in the reversible tier writes three bytes and returns 0;
the tape holds one `console.write`; whole-run reversal restores the entry state:

```llvm example=effect-console-r verdict=accept
@msg = private unnamed_addr constant [3 x i8] c"hi\0A"

define i32 @main() {
  call void @__bennett_effect_console_write(ptr @msg, i64 3)
  ret i32 0
}
```

```text cc-run=effect-console-r
driver: --bennett-tier=reversible --bennett-entry=main
run: status=COMPLETED results=[INT(32):0] faults=[]
tape: console write args=[A(@msg), 3] bytes=68690a
reverse: status=REVERSED console=empty memory=entry
```

The same marker in a CC device function is a host effect:

```llvm example=effect-console-cc verdict=accept
@msg = private unnamed_addr constant [3 x i8] c"ok\0A"

define void @report() {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @__bennett_qfree(ptr %h)
  call void @__bennett_effect_console_write(ptr @msg, i64 3)
  ret void
}
```

```text cc-run=effect-console-cc
run: status=COMPLETED results=[] faults=[]
hostcall: service=bennett.dev.console.write payload=6f6b0a reply=empty
```

The ENTROPY-bound oracle of rung 8 is §16.8.

## 12. Materialised normalisation (norm 0.2)

### 12.1 Scope, order and naming

The normaliser rewrites every device variant (§4.3) and the initialisers of every global a
device variant references; H variants are untouched. It applies the rules of §12.2 in table
order, each to the whole module before the next, with one exception: N33 is applied immediately
before N32, because the `fpext`/`fptrunc` pairs it creates around libm calls (§13.4) are
floating-point instructions that N32 rewrites. The result is the **materialised module**: the
reference semantics (§18), the lifting map (§16) and the native comparison build (§17.7) are all
defined on it (NS §3.2: "the native comparison binary is built from that materialised bitcode").

**Naming.** A rule that introduces a value names it `%nz.<tag>.<r>`, where `<r>` is the name of
the instruction being rewritten without its `%` (a number for an unnamed value). For a rewritten
instruction without a result (a `void` call, a `store`, an `invoke` of a `void` function), `<r>`
is `<f>.<k>`: f the enclosing function's name and k the 0-based count, in instruction order, of
the result-less instructions of f that the same rule rewrites. A value introduced once per
function is `%nz.<tag>.<f>`. A constant global a rule needs is `@nz.<tag>.<f>.<r>`. A
declaration a rule needs is appended at the end of the module, and a global after the module's
globals, in order of first use. Each rule
states its tags.

### 12.2 The rules

**Fault replacement F(C)** (§12.3) and the 35 rules. N13, N17, N18 and N20 are 0.1 ids whose
rules are replaced (outline §12.2); they are kept as anchors.

| Id | Source | Replacement |
|---|---|---|
| N0 | the intrinsic families that LLVM defines by its own lowering passes: `llvm.coro.*`; `llvm.matrix.*`; `llvm.type.test`, `llvm.public.type.test`, `llvm.type.checked.load`, `llvm.type.checked.load.relative`, `llvm.icall.branch.funnel`; `llvm.instrprof.*`; `llvm.alloc.token.id`; `llvm.experimental.guard`, `llvm.experimental.widenable.condition` | the normaliser runs, only when the module contains one of them, the passes of the major in use, in this order: `coro-early`, `cgscc(coro-split)`, `coro-cleanup`; `lower-matrix-intrinsics`; `lowertypetests`; `instrprof`; `alloc-token`; `lower-guard-intrinsic`; `lower-widenable-condition` (which gives `true`). Their output is then normalised by N1–N35 |
| N1 | instruction flags `nsw`, `nuw`, `exact`, `inbounds`, `nusw`, `nneg`, `disjoint`, `samesign`, `inrange` (and `inrange(...)`) | removed: wrapping, inexact, out-of-bounds address arithmetic and the unflagged operation are defined |
| N2 | fast-math flags `nnan`, `ninf`, `nsz`, `arcp`, `contract`, `afn`, `reassoc`, `fast` | removed |
| N3 | instruction metadata other than `!dbg` (`!range`, `!nonnull`, `!noundef`, `!align`, `!dereferenceable`, `!dereferenceable_or_null`, `!tbaa`, `!tbaa.struct`, `!alias.scope`, `!noalias`, `!invariant.load`, `!invariant.group`, `!llvm.loop`, `!nontemporal`, `!prof`, `!alloc_token`, …) | removed (after §5 has read `!range`, PT5) |
| N4 | attributes on device function definitions, their parameters and returns, and on every call site in a device function: `noundef`, `nonnull`, `range(...)`, `align` (except together with `byval`, `byref`, `sret`, `inalloca`, `preallocated`), `dereferenceable(...)`, `dereferenceable_or_null(...)`, `nofpclass(...)`, `noalias`, `nocapture`, `captures(...)`, parameter `readnone`/`readonly`/`writeonly`, `returned`, `writable`, `dead_on_unwind`, `initializes(...)`, `allocalign`, `allocptr`; function attributes `memory(...)`, `readnone`, `readonly`, `writeonly`, `argmemonly`, `inaccessiblememonly`, `inaccessiblemem_or_argmemonly`, `willreturn`, `mustprogress`, `nosync`, `nofree`, `norecurse`, `speculatable`, `personality` (after N28) | removed (attribute groups are rewritten; a group shared with an H function is first duplicated) |
| N5 | calls with no semantic effect: `llvm.assume`, `llvm.sideeffect`, `llvm.donothing`, `llvm.pseudoprobe`, `llvm.fake.use`, `llvm.dbg.*`, `llvm.experimental.noalias.scope.decl`, `llvm.codeview.annotation`, `llvm.var.annotation`, `llvm.reloc.none`, `llvm.prefetch`, `llvm.pcmarker`, `llvm.clear_cache`, `llvm.experimental.convergence.*`, `llvm.seh.*`, `llvm.xray.*`, `llvm.experimental.stackmap`, `llvm.eh.unwind.init`, `llvm.asan.check.memaccess`, `llvm.hwasan.check.memaccess*` | deleted (a token result is never used after deletion of its users) |
| N5 | calls that return an operand: `llvm.expect`, `llvm.expect.with.probability`, `llvm.annotation`, `llvm.ptr.annotation`, `llvm.launder.invariant.group`, `llvm.strip.invariant.group`, `llvm.ssa.copy`, `llvm.arithmetic.fence`, `llvm.threadlocal.address`, `llvm.protected.field.ptr`, `llvm.ptrauth.sign`, `llvm.ptrauth.auth`, `llvm.ptrauth.resign`, `llvm.ptrauth.auth.with.pc.and.resign`, `llvm.ptrauth.strip` | every use replaced by operand 0; deleted. *(non-normative)* Pointer authentication is a target feature with no device counterpart; the identity is one deterministic choice, made identically in both builds |
| N6 | `llvm.lifetime.start`, `llvm.lifetime.end`, `llvm.invariant.start`, `llvm.invariant.end` | deleted (a frame is live for its whole activation, §17.3) |
| N7 | `undef` and `poison` constants: whole operands, vector lanes, aggregate elements, `shufflevector` mask elements, global initialisers | the zero of the type: `0`, `+0.0`, `null`, `zeroinitializer` for a wholly undefined vector or aggregate; mask element `0` |
| N8 | `%x = freeze T v` | deleted; every use of `%x` replaced by v |
| N9 | `atomic` and `volatile` on loads and stores; `fence`; `atomicrmw`; `cmpxchg` | plain load/store; fence deleted; `atomicrmw op ptr p, T v` → `%nz.l.r = load T, ptr p`, `%nz.v.r = <op> T %nz.l.r, v` (for `xchg`: v; `min`/`max`/`umin`/`umax`: `icmp` + `select` named `%nz.k.r`, `%nz.v.r`; FP ops: their N32 form), `store T %nz.v.r, ptr p`, uses of `%r` → `%nz.l.r`; `cmpxchg ptr p, T c, T n` → `%nz.l.r = load`, `%nz.e.r = icmp eq T %nz.l.r, c`, `%nz.s.r = select i1 %nz.e.r, T n, T %nz.l.r`, `store T %nz.s.r, ptr p`, `%nz.a.r = insertvalue { T, i1 } zeroinitializer, T %nz.l.r, 0`, `%r = insertvalue { T, i1 } %nz.a.r, i1 %nz.e.r, 1` (single-thread assumption, recorded in the certificate, §24 D24). Volatile accesses in platform-profile code are first routed by N35 (§20.3) |
| N10 | `llvm.is.constant.*` | `false` |
| N10 | `llvm.objectsize.*(p, min, nullunknown, dynamic)` | `-1` (all ones) if `min` is `false`, else `0` |
| N10 | `llvm.allow.runtime.check`, `llvm.allow.ubsan.check` | `true` (checks stay; a failing check is a fault) |
| N10 | `llvm.allow.sanitize.address`, `.hwaddress`, `.memory`, `.thread` | `false` (no sanitizer runtime exists in either build) |
| N10 | `llvm.get.dynamic.area.offset` | `0` |
| N10 | `llvm.vscale` | the constant V of §12.5 |
| N11 | calls of `llvm.trap`, `llvm.debugtrap`, `llvm.ubsantrap`, `llvm.looptrap` | F(4) |
| N11 | `llvm.cond.loop(c)` | the block is split after the call; `br i1 c, label %nz.spin.<f>.<k>, label <rest>`; the new block `nz.spin.<f>.<k>` is `br label %nz.spin.<f>.<k>` (the infinite loop LangRef defines; budgets bound it, §9) |
| N12 | `llvm.abs.*(x, i1 true)`, `llvm.ctlz.*(x, i1 true)`, `llvm.cttz.*(x, i1 true)` | the flag becomes `i1 false` |
| N13 | (0.1: `memcpy` → `memmove`) | replaced by N26 |
| N14 | `%r = shl/lshr/ashr iW a, b` with b not a constant | `%nz.c.r = icmp uge iW b, W`; `%nz.s.r = <op> iW a, b`; `%r = select i1 %nz.c.r, iW 0, iW %nz.s.r` (every shift by ≥ W gives 0, as the ISA's shifts do, ISA §4.1) |
| N14 | the same with b a constant ≥ W | every use of `%r` replaced by `0`; deleted |
| N15 | `extractelement`/`insertelement` with a non-constant index i on L lanes | `%nz.c.r = icmp uge iK i, L`; `%nz.e.r = <the original instruction>`; `%r = select i1 %nz.c.r, T Z, T %nz.e.r` with Z = the zero element (extract) or the unchanged vector operand (insert) |
| N16 | `%r = call T @llvm.fmuladd.*(a, b, c)` | `%nz.m.r = fmul T a, b`; `%r = fadd T %nz.m.r, c` (no fusion; explicit `llvm.fma` keeps fusion through §13) |
| N17 | (0.1: FP formats and transcendentals → F(8)) | replaced by §13 (N32, N33): no floating-point construct faults |
| N18 | (0.1: external calls in oracle and reversible closures → F(8)) | replaced by §4.5: shims first; trapped only without bitcode |
| N19 | floating-point arithmetic, comparison and conversion of `float` and `double` | the soft-float rewrite of §13.1 (applied by N32) |
| N20 | (0.1: alloca + memset) | replaced by N24 |
| N21 | **vector scalarisation**: every instruction of vector type, every vector intrinsic (`llvm.vector.*`, `llvm.experimental.vector.*`, `llvm.vp.*`, `llvm.experimental.vp.*`, `llvm.masked.*`, `llvm.stepvector`, `llvm.experimental.stepvector`, `llvm.get.active.lane.mask`, `llvm.experimental.get.vector.length`, `llvm.experimental.cttz.elts`, `llvm.vp.cttz.elts`, `llvm.loop.dependence.raw.mask`, `llvm.loop.dependence.war.mask`), vector parameters and results of internal device functions | per-lane scalar instructions in lane order, by the rules of §12.6 |
| N22 | **wide integers and non-byte memory**: an integer type iN with N > 128 in an instruction; a load or store of iN with N not a multiple of 8 or of an aggregate type | iN with N > 128 becomes L = ⌈N/64⌉ i64 limbs (limb 0 the least significant; the top limb is i(N − 64(L−1))) with the expansions of §12.7; a load or store of iN with N mod 8 ≠ 0 becomes a load or store of i(8⌈N/8⌉) with a `trunc` after the load and a `zext` before the store (fixing LangRef's unspecified extra bits as zero); a load or store of an aggregate becomes one access per element in element order at its offset (`%nz.e<k>.<r>`) |
| N23 | **varargs** | §14.3 |
| N24 | **allocas → shadow stack**: every `alloca`; `llvm.stacksave`, `llvm.stackrestore`; `llvm.frameaddress`, `llvm.sponentry`, `llvm.addressofreturnaddress`, `llvm.stackaddress`, `llvm.returnaddress`, `llvm.swift.async.context.addr`, `llvm.localescape`, `llvm.localrecover`, `llvm.localaddress`, `llvm.eh.recoverfp`, `llvm.eh.dwarf.cfa`; `llvm.structured.alloca` | §17.3 |
| N25 | `byval`, `inalloca` and `preallocated` arguments; `llvm.call.preallocated.*`; aggregate returns wider than 128 bits | an explicit caller copy into a shadow-stack slot of the caller's frame (`%nz.bv<j>.<r>` for argument j) passed as a plain `ptr`, and the attribute removed from the callee and the call; a return of a first-class aggregate wider than 128 bits is demoted to a hidden first parameter `ptr %nz.ret` in which the callee stores the value (`sret` semantics) |
| N26 | **memory intrinsics**: `llvm.memcpy.*`, `llvm.memcpy.inline.*`, `llvm.memmove.*`, `llvm.memset.*`, `llvm.memset.inline.*`, `llvm.memcpy/memmove/memset.element.unordered.atomic.*`, `llvm.experimental.memset.pattern.*` | `call void @__bennett_rt_memmove(ptr d, ptr s, i64 n)`, `call void @__bennett_rt_memset(ptr d, i8 v, i64 n)` (the `i1` volatile flag and element-size operand dropped; a constant length becomes an `i64` constant; a narrower non-constant length is first `%nz.n.<r> = zext … to i64`); `memset.pattern(d, v: T, count)` → a loop storing v at d + i·size(T) for i < count (blocks `nz.mp.<r>.*`) |
| N27 | **integer intrinsics** | the fixed expansions of §12.8 |
| N28 | **unwinding: explicit propagation** | §14.4 |
| N29 | **setjmp/longjmp** | §14.5 |
| N30 | **rewindable frames** (fibers) | §14.6, only in the functions §14.6 selects |
| N31 | **inline asm and target intrinsics** | the §15 tables |
| N32 | **floating point** | the soft-float rewrite of §13.1–§13.2 (after N21) |
| N33 | **extended FP formats and libm intrinsics** | §13.3–§13.5 |
| N34 | **R-tier budget instrumentation points** | a call of `__bennett_rt_rstep()` is *not* inserted; N34 marks the R variants' function entries and loop latches with the metadata `!bennett.rstep` (kept by N3) for the R lowering's counters (§17.6) |
| N35 | **platform hooks** | §20.3 (MMIO routing), §20.4 (interrupt poll points), only under a platform profile |

The other generic intrinsics are rows of §12.8 (integer), §13 (floating point), §14 (control
transfer) and §15 (target intrinsics). **Completeness obligation:** Appendix C lists every
generic (target-independent) intrinsic name of LLVM 18, 20 and 23 (546 names) with its rule. No
generic intrinsic is `trapped`.

*(non-normative)* Division by zero and `sdiv`/`srem` of INT_MIN by −1 are not rewritten: they are
faults of the reference semantics (§17.5), the ISA's `lift.div` and CC division fault on them
directly (ISA §4.1, §4.2), and the native comparison build traps (§17.7).

### 12.3 Fault replacement F(C)

F(C): the instruction is replaced by `call void @__bennett_nz_fault(i64 C)` followed by
`unreachable`; the instructions after it in its block are deleted, and the block is removed from
the incoming lists of the phi nodes of its former successors. `__bennett_nz_fault` is a primitive
(§3.1): `bennett-runtimes` defines it for the native comparison build (record C and end the
device entry with fault C); the map gives it the row `fault C` (§16.4); CC and R lower it by
§11.5.

### 12.4 The residual-poison validator

The validator inspects the materialised device variants and rejects (`BD-E-RESIDUAL`) any of:

| Id | Residue |
|---|---|
| V1 | a flag of N1 or N2 |
| V2 | instruction metadata other than `!dbg` and `!bennett.rstep` |
| V3 | an attribute N4 removes, on a device function, its parameters or return, or a call site in a device function |
| V4 | a call of an intrinsic that N0, N5, N6, N10, N11, N16, N21, N24, N26, N27, N32 or N33 removes, or of `llvm.abs`/`ctlz`/`cttz` with a `true` flag |
| V5 | an `undef` or `poison` constant in a device function or in the initialiser of a global a device function references |
| V6 | `freeze`, `fence`, `atomicrmw`, `cmpxchg`, an atomic or volatile load or store |
| V7 | a shift whose amount is not a constant < W, unless the shift's only use is as the false operand of a `select` whose true operand is 0 and whose condition is `icmp uge` of the same amount and the constant W |
| V8 | `extractelement`/`insertelement` with a non-constant index outside the N15 pattern (only before N21; after N21 no vector remains, V13) |
| V9 | a floating-point instruction other than `fneg`, `bitcast`, `load`, `store`, `select` and `phi` of a floating-point value, or a call of a floating-point intrinsic other than `llvm.fabs` and `llvm.copysign` (after N32/N33; 0.1's V9 is inverted) |
| V10 | an operand or result of type `half`, `bfloat`, `x86_fp80`, `fp128` or `ppc_fp128` other than in `bitcast`, `load`, `store`, `select` and `phi` (after N33) |
| V11 | an `alloca` (after N24; replaces 0.1's V11) |
| V12 | in an L or R variant, a call of a function without a definition other than a primitive, a runtime entry point defined in the link, or a trapped call already replaced by F(8) |
| V13 | a value of vector type |
| V14 | a value of type iN with N > 128 |
| V15 | `va_start`, `va_end`, `va_copy`, `va_arg`, `invoke`, `landingpad`, `resume`, `cleanuppad`, `catchpad`, `catchswitch`, `cleanupret`, `catchret`, a call of `setjmp`, `_setjmp`, `sigsetjmp` or `__sigsetjmp` |
| V16 | inline `asm` or a call of a target intrinsic (`llvm.<target>.*`) |

The plugin's validator and `bennett-conformance`'s are implemented independently (NS §3.2); a
disagreement on any input is a conformance failure of one of them.

### 12.5 Scalable vectors

A scalable vector type `<vscale x L x T>` has L·V lanes, where V is the constant `vscale` of the
link: the function attribute `vscale_range(V, V)` when every device function that uses scalable
vectors carries it with equal bounds, else the driver option `--bennett-vscale=<V>` (default: the
minimum of the `vscale_range` bounds, §24). The native comparison build is compiled for the same
V (`-msve-vector-bits=128·V` or `-mrvv-vector-bits`). N10 replaces `llvm.vscale` by V and N21
scalarises the L·V lanes. *(non-normative)* x86-64 has no scalable vectors; the rule exists so
that AArch64 SVE and RISC-V V code is liftable.

### 12.6 Vector scalarisation (N21)

For a value `%v` of type `<L x T>`, lane k is the scalar `%nz.l<k>.v` (k = 0 … L − 1). Rules, in
lane order k = 0, 1, …:

- elementwise instructions (binary, bitwise, `icmp`, `fcmp`, casts, `select` with a vector or
  scalar condition, unary `fneg`, `freeze`, calls of elementwise intrinsics): one scalar
  instruction per lane, `%nz.l<k>.r = <op> T %nz.l<k>.a, %nz.l<k>.b`;
- `load <L x T>, ptr p` → `%nz.p<k>.r = getelementptr T, ptr p, i64 k` and `%nz.l<k>.r = load T,
  ptr %nz.p<k>.r` with alignment min(original, abi-align(T)); `store` likewise in lane order;
- `insertelement`, `extractelement`, `shufflevector` with constant indices: lane renaming; with a
  non-constant index (after N15): a `select` chain over the L lanes in lane order;
- `llvm.vector.reduce.<op>(v)` with op ∈ {add, mul, and, or, xor, smax, smin, umax, umin, fadd,
  fmul, fmax, fmin, fmaximum, fminimum}: a **left fold** in lane order: `%nz.f1.r = <op> lane0,
  lane1`, `%nz.f<k>.r = <op> %nz.f<k−1>.r, lane k`, the last named `%r`; the ordered `fadd`/`fmul`
  forms take the start value as the first operand. Exact for floating point once N2 has removed
  `reassoc`;
- `llvm.vp.*` (vector-predicated) and `llvm.masked.*`: lane k is active iff k < evl and mask[k];
  an active lane executes the scalar operation, an inactive lane yields the passthrough operand
  (masked loads) or 0 (N7: LangRef's poison), and a masked or predicated store, scatter or
  compress-store writes only active lanes, each under a conditional branch (blocks
  `nz.ml<k>.<r>`); gathers and scatters use the lane's pointer;
- `llvm.stepvector` lane k is k; `llvm.get.active.lane.mask(base, n)` lane k is base + k < n
  (unsigned); `llvm.experimental.get.vector.length(cnt, vf, scalable)` is umin(cnt, vf·(V if
  scalable else 1)); `cttz.elts` is the index of the first nonzero lane (L if none, or the
  poison-free 0 of N7 when the flag says zero is poison); `loop.dependence.raw/war.mask(a, b,
  size)` lane k follows LangRef's definition;
- `vector.extract`, `vector.insert`, `vector.reverse`, `vector.splice*`, `vector.interleave<n>`,
  `vector.deinterleave<n>`, `experimental.vector.compress`, `experimental.vector.histogram.*`,
  `experimental.vector.match`, `experimental.vector.extract.last.active`,
  `vector.partial.reduce.*`: lane permutations and folds by their LangRef definitions;
- a vector parameter or result of an internal device function becomes L scalar parameters or an
  aggregate of L scalars in lane order; a vector that crosses an external boundary (a device
  entry's signature, a call of a function without a definition) is rebuilt with `insertelement`
  at that boundary, which only H code and the native build see.

### 12.7 Wide integers (N22)

With limbs a_k, b_k (k = 0 … L − 1, i64, the top limb of width N − 64(L − 1)):

- `add`: `%nz.m0.r = add a_0, b_0`, `%nz.c0.r = icmp ult %nz.m0.r, a_0`; for k ≥ 1:
  `%nz.t<k>.r = add a_k, b_k`, `%nz.z<k>.r = zext i1 %nz.c<k−1>.r to i64`, `%nz.m<k>.r = add
  %nz.t<k>.r, %nz.z<k>.r` and, for k < L − 1, `%nz.u<k>.r = icmp ult %nz.t<k>.r, a_k`,
  `%nz.v<k>.r = icmp ult %nz.m<k>.r, %nz.t<k>.r`, `%nz.c<k>.r = or i1 %nz.u<k>.r, %nz.v<k>.r`;
- `sub`: the same with `sub` and borrows `icmp ult a_k, b_k`;
- `and`, `or`, `xor`: per limb; `icmp`: lexicographic from the top limb (signed on the top
  limb only for signed predicates); `select`, `phi`: per limb; `zext`, `sext`, `trunc`: limb
  copies with the sign limb `ashr a_top, 63` for `sext`;
- `mul`, `udiv`, `sdiv`, `urem`, `srem`, `shl`, `lshr`, `ashr`: calls of the runtimes entry points
  `__bennett_rt_i<N>_<op>(ptr r, ptr a, ptr b)` on shadow-stack slots holding the limbs (division
  by zero calls `__bennett_nz_fault(5)`, signed MIN / −1 `__bennett_nz_fault(6)`, shifts by ≥ N
  give 0 as N14);
- loads and stores: per limb at offsets 8k, little-endian targets (`%nz.p<k>.r` / `%nz.q<k>.r`
  for the addresses);
- a wide parameter or result of an internal device function becomes L limb parameters or an
  aggregate of limbs.

### 12.8 Integer intrinsics (N27)

| Intrinsic | Expansion |
|---|---|
| `smax`, `smin`, `umax`, `umin` (a, b) | `%nz.c.r = icmp sgt/slt/ugt/ult a, b`; `%r = select i1 %nz.c.r, a, b` |
| `abs(a, false)` | `%nz.c.r = icmp slt a, 0`; `%nz.n.r = sub 0, a`; `%r = select i1 %nz.c.r, %nz.n.r, a` |
| `scmp`, `ucmp` (a, b) → iM | `%nz.g.r = icmp sgt/ugt a, b`; `%nz.l.r = icmp slt/ult a, b`; `%nz.z.r = zext i1 %nz.g.r to iM`; `%nz.s.r = sext i1 %nz.l.r to iM`; `%r = or iM %nz.z.r, %nz.s.r` |
| `uadd/usub.with.overflow` (a, b) | `%nz.s.r = add/sub a, b`; `%nz.c.r = icmp ult %nz.s.r, a` (add) or `icmp ult a, b` (sub); `%nz.a.r = insertvalue { T, i1 } zeroinitializer, T %nz.s.r, 0`; `%r = insertvalue { T, i1 } %nz.a.r, i1 %nz.c.r, 1` |
| `sadd/ssub.with.overflow` | `%nz.s.r = add/sub a, b`; `%nz.x.r = xor a, %nz.s.r`; `%nz.y.r = xor b, %nz.s.r` (add) or `xor a, b` (sub); `%nz.w.r = and %nz.x.r, %nz.y.r`; `%nz.c.r = icmp slt %nz.w.r, 0` (overflow iff the result's sign differs from a's while the operands' signs agree (add) or differ (sub)); then the two `insertvalue`s |
| `umul/smul.with.overflow` on iW, W ≤ 64 | the product at width 2W (`zext`/`sext`, `mul`, `trunc`); overflow iff the high half differs from 0 (unsigned) or from the sign extension of the low half (signed); W > 64: `__bennett_rt_<name>_i<W>` |
| `uadd/usub/sadd/ssub.sat` | the `.with.overflow` expansion and a `select` of the saturated bound (unsigned: all ones / 0; signed: MAX if the operand a is non-negative, else MIN) |
| `ptrmask(p, m)` | `%nz.i.r = ptrtoint p to iW`; `%nz.a.r = and iW %nz.i.r, m`; `%r = inttoptr iW %nz.a.r to ptr` |
| `load.relative(p, off)` | `%nz.p.r = getelementptr i8, ptr p, off`; `%nz.o.r = load i32, ptr %nz.p.r`; `%nz.e.r = sext i32 %nz.o.r to i64`; `%r = getelementptr i8, ptr p, i64 %nz.e.r` |
| `bswap`, `bitreverse`, `ctpop`, `ctlz`, `cttz`, `fshl`, `fshr`, `sshl.sat`, `ushl.sat`, `smul.fix`, `umul.fix`, `smul.fix.sat`, `umul.fix.sat`, `sdiv.fix`, `udiv.fix`, `sdiv.fix.sat`, `udiv.fix.sat`, `pdep`, `pext`, `clmul` | `%r = call iW @__bennett_rt_<name>_i<W>(…)` with the same operands (`<name>` with `.` replaced by `_`), defined by `bennett-runtimes` with the LangRef semantics (division by zero in the `.fix` forms: `__bennett_nz_fault(5)`) |
| `read_register`, `read_volatile_register`, `write_register`, `write_volatile_register` (named register) | a load or store of the runtimes global `__bennett_rt_reg_<name>` (the platform register file, §20.1); the name `sp` (and its target spellings) reads the shadow-stack pointer (§17.3) |
| `thread.pointer` | the address of the runtimes global `__bennett_rt_tls` (one thread) |
| `stackguard`, `stackprotector(g, slot)` | a load of the runtimes global `__stack_chk_guard`; a store of g into slot |
| `set.loop.iterations(n)`, `start.loop.iterations(n)`, `test.set.loop.iterations(n)`, `test.start.loop.iterations(n)`, `loop.decrement(k)`, `loop.decrement.reg(c, k)` (hardware loops; only the code generator's HardwareLoops pass emits them) | the counter in a shadow-frame slot of the function: `set`/`start` store n (`start` also returns n); the `test` forms also return n ≠ 0; `loop.decrement(k)` stores counter − k and returns counter − k ≠ 0; `loop.decrement.reg(c, k)` returns c − k |
| `preserve.array.access.index`, `preserve.struct.access.index`, `preserve.union.access.index`, `preserve.static.offset` (BPF CO-RE) | the `getelementptr` they describe (the union form and `preserve.static.offset` return their pointer operand) |
| `ptrauth.resign.load.relative(p, k1, d1, k2, d2, add)` (i64 values) | p + sext(the i32 loaded at p + add), as `load.relative`, with signing and authentication the identity of N5 |
| `ptrauth.blend(a, d)` | `(a & 0xFFFFFFFFFFFF) | (d << 48)` in i64 |
| `ptrauth.sign.generic(v, d)` | `0` |
| `objc.*` | `llvm.objc.<name>` becomes a call of the Objective-C runtime function `objc_<name>` with the same operands (resolved by §4.5); `objc.clang.arc.use`, `objc.clang.arc.noop.use` and `objc.arc.annotation.*` are deleted |
| `experimental.gc.statepoint(id, n, f, args…)` | a plain call `f(args…)`; `gc.result` → its result; `gc.relocate(token, base, derived)` → the derived pointer of the statepoint's argument list (a non-moving collector); `gc.get.pointer.base(p)` → p; `gc.get.pointer.offset(p)` → 0; `gcroot` deleted; `gcread(o, p)` → `load ptr, ptr p`; `gcwrite(v, o, p)` → `store ptr v, ptr p` |
| `experimental.patchpoint*(id, n, target, nargs, args…)` | an indirect call of target with the first nargs arguments (§14.2); a null target: nothing |
| `experimental.deoptimize(args…)` | a call of the runtimes function `__llvm_deoptimize` with the arguments (resolved by §4.5) and `ret` of its result |
| `init.trampoline`, `adjust.trampoline` | §14.2 (trampolines) |
| `eh.typeid.for`, `eh.exceptionpointer`, `eh.exceptioncode`, `eh.return.*`, `eh.sjlj.*` | §14.4, §14.5 |
| `callbr.landingpad` | §15.2 |

### 12.9 Examples

```llvm normalise-in=n-flags
define internal i32 @f(i32 noundef %a, ptr nonnull align 4 %p) #0 {
  %s = add nsw i32 %a, 1
  %q = getelementptr inbounds i32, ptr %p, i64 1
  %v = load i32, ptr %q, align 4, !range !0, !noundef !1
  %c = icmp sgt i32 %v, 0
  call void @llvm.assume(i1 %c)
  %r = mul nuw nsw i32 %s, %v
  ret i32 %r
}

declare void @llvm.assume(i1 noundef)

attributes #0 = { mustprogress nounwind willreturn memory(argmem: read) }

!0 = !{i32 0, i32 100}
!1 = !{}
```

```llvm normalise-out=n-flags
define internal i32 @f(i32 %a, ptr %p) #0 {
  %s = add i32 %a, 1
  %q = getelementptr i32, ptr %p, i64 1
  %v = load i32, ptr %q, align 4
  %c = icmp sgt i32 %v, 0
  %r = mul i32 %s, %v
  ret i32 %r
}

declare void @llvm.assume(i1 noundef)

attributes #0 = { nounwind }

!0 = !{i32 0, i32 100}
!1 = !{}
```

```llvm normalise-in=n-shift
define internal i32 @sh(i32 %a, i32 %b) {
  %r = shl i32 %a, %b
  %k = lshr i32 %a, 3
  %z = ashr i32 %a, 40
  %t = add i32 %r, %z
  %u = add i32 %t, %k
  ret i32 %u
}
```

```llvm normalise-out=n-shift
define internal i32 @sh(i32 %a, i32 %b) {
  %nz.c.r = icmp uge i32 %b, 32
  %nz.s.r = shl i32 %a, %b
  %r = select i1 %nz.c.r, i32 0, i32 %nz.s.r
  %k = lshr i32 %a, 3
  %t = add i32 %r, 0
  %u = add i32 %t, %k
  ret i32 %u
}
```

```llvm normalise-in=n-undef
define internal i64 @u(i64 %a, i1 %c) {
  %f = freeze i64 undef
  %s = select i1 %c, i64 %a, i64 poison
  %v = insertelement <2 x i64> poison, i64 %a, i32 0
  %w = extractelement <2 x i64> %v, i32 1
  %r = add i64 %f, %s
  %t = add i64 %r, %w
  ret i64 %t
}
```

The vector in `n-undef` is then scalarised by N21: lane 0 is `%a`, lane 1 is the zero of N7, so
`%w` is `0`:

```llvm normalise-out=n-undef
define internal i64 @u(i64 %a, i1 %c) {
  %s = select i1 %c, i64 %a, i64 0
  %r = add i64 0, %s
  %t = add i64 %r, 0
  ret i64 %t
}
```

```llvm normalise-in=n-query
define internal i64 @q(ptr %p, i64 %x) {
  %s = call i64 @llvm.objectsize.i64.p0(ptr %p, i1 false, i1 true, i1 false)
  %k = call i1 @llvm.is.constant.i64(i64 %x)
  %z = zext i1 %k to i64
  %r = add i64 %s, %z
  ret i64 %r
}

declare i64 @llvm.objectsize.i64.p0(ptr, i1 immarg, i1 immarg, i1 immarg)
declare i1 @llvm.is.constant.i64(i64)
```

```llvm normalise-out=n-query
define internal i64 @q(ptr %p, i64 %x) {
  %z = zext i1 false to i64
  %r = add i64 -1, %z
  ret i64 %r
}

declare i64 @llvm.objectsize.i64.p0(ptr, i1 immarg, i1 immarg, i1 immarg)
declare i1 @llvm.is.constant.i64(i64)
```

```llvm normalise-in=n-trap
define internal i32 @t(i32 %a) {
  %c = icmp eq i32 %a, 0
  call void @llvm.trap()
  %r = add i32 %a, 1
  ret i32 %r
}

declare void @llvm.trap()
```

```llvm normalise-out=n-trap
define internal i32 @t(i32 %a) {
  %c = icmp eq i32 %a, 0
  call void @__bennett_nz_fault(i64 4)
  unreachable
}

declare void @llvm.trap()

declare void @__bennett_nz_fault(i64)
```

Vector scalarisation and an ordered reduction (N21):

```llvm normalise-in=n-vector
define internal i32 @v(ptr %pa, ptr %pb) {
  %a = load <4 x i32>, ptr %pa, align 4
  %b = load <4 x i32>, ptr %pb, align 4
  %s = add <4 x i32> %a, %b
  %r = call i32 @llvm.vector.reduce.add.v4i32(<4 x i32> %s)
  ret i32 %r
}

declare i32 @llvm.vector.reduce.add.v4i32(<4 x i32>)
```

```llvm normalise-out=n-vector
define internal i32 @v(ptr %pa, ptr %pb) {
  %nz.p0.a = getelementptr i32, ptr %pa, i64 0
  %nz.l0.a = load i32, ptr %nz.p0.a, align 4
  %nz.p1.a = getelementptr i32, ptr %pa, i64 1
  %nz.l1.a = load i32, ptr %nz.p1.a, align 4
  %nz.p2.a = getelementptr i32, ptr %pa, i64 2
  %nz.l2.a = load i32, ptr %nz.p2.a, align 4
  %nz.p3.a = getelementptr i32, ptr %pa, i64 3
  %nz.l3.a = load i32, ptr %nz.p3.a, align 4
  %nz.p0.b = getelementptr i32, ptr %pb, i64 0
  %nz.l0.b = load i32, ptr %nz.p0.b, align 4
  %nz.p1.b = getelementptr i32, ptr %pb, i64 1
  %nz.l1.b = load i32, ptr %nz.p1.b, align 4
  %nz.p2.b = getelementptr i32, ptr %pb, i64 2
  %nz.l2.b = load i32, ptr %nz.p2.b, align 4
  %nz.p3.b = getelementptr i32, ptr %pb, i64 3
  %nz.l3.b = load i32, ptr %nz.p3.b, align 4
  %nz.l0.s = add i32 %nz.l0.a, %nz.l0.b
  %nz.l1.s = add i32 %nz.l1.a, %nz.l1.b
  %nz.l2.s = add i32 %nz.l2.a, %nz.l2.b
  %nz.l3.s = add i32 %nz.l3.a, %nz.l3.b
  %nz.f1.r = add i32 %nz.l0.s, %nz.l1.s
  %nz.f2.r = add i32 %nz.f1.r, %nz.l2.s
  %r = add i32 %nz.f2.r, %nz.l3.s
  ret i32 %r
}

declare i32 @llvm.vector.reduce.add.v4i32(<4 x i32>)
```

```text native=n-vector
v([1, 2, 3, 2147483647], [10, 20, 30, 1]) = -2147483582
v([-5, 7, 0, 100], [5, -7, 9, 1]) = 110
```

*(non-normative)* 11 + 22 + 33 + (2147483647 + 1 mod 2^32 = −2^31) = 66 − 2147483648 =
−2147483582; 0 + 0 + 9 + 101 = 110.

A 256-bit addition in four limbs (N22):

```llvm normalise-in=n-wideint
define internal void @w(ptr %pa, ptr %pb, ptr %pr) {
  %a = load i256, ptr %pa, align 8
  %b = load i256, ptr %pb, align 8
  %s = add i256 %a, %b
  store i256 %s, ptr %pr, align 8
  ret void
}
```

```llvm normalise-out=n-wideint
define internal void @w(ptr %pa, ptr %pb, ptr %pr) {
  %nz.p0.a = getelementptr i64, ptr %pa, i64 0
  %nz.m0.a = load i64, ptr %nz.p0.a, align 8
  %nz.p1.a = getelementptr i64, ptr %pa, i64 1
  %nz.m1.a = load i64, ptr %nz.p1.a, align 8
  %nz.p2.a = getelementptr i64, ptr %pa, i64 2
  %nz.m2.a = load i64, ptr %nz.p2.a, align 8
  %nz.p3.a = getelementptr i64, ptr %pa, i64 3
  %nz.m3.a = load i64, ptr %nz.p3.a, align 8
  %nz.p0.b = getelementptr i64, ptr %pb, i64 0
  %nz.m0.b = load i64, ptr %nz.p0.b, align 8
  %nz.p1.b = getelementptr i64, ptr %pb, i64 1
  %nz.m1.b = load i64, ptr %nz.p1.b, align 8
  %nz.p2.b = getelementptr i64, ptr %pb, i64 2
  %nz.m2.b = load i64, ptr %nz.p2.b, align 8
  %nz.p3.b = getelementptr i64, ptr %pb, i64 3
  %nz.m3.b = load i64, ptr %nz.p3.b, align 8
  %nz.m0.s = add i64 %nz.m0.a, %nz.m0.b
  %nz.c0.s = icmp ult i64 %nz.m0.s, %nz.m0.a
  %nz.t1.s = add i64 %nz.m1.a, %nz.m1.b
  %nz.z1.s = zext i1 %nz.c0.s to i64
  %nz.m1.s = add i64 %nz.t1.s, %nz.z1.s
  %nz.u1.s = icmp ult i64 %nz.t1.s, %nz.m1.a
  %nz.v1.s = icmp ult i64 %nz.m1.s, %nz.t1.s
  %nz.c1.s = or i1 %nz.u1.s, %nz.v1.s
  %nz.t2.s = add i64 %nz.m2.a, %nz.m2.b
  %nz.z2.s = zext i1 %nz.c1.s to i64
  %nz.m2.s = add i64 %nz.t2.s, %nz.z2.s
  %nz.u2.s = icmp ult i64 %nz.t2.s, %nz.m2.a
  %nz.v2.s = icmp ult i64 %nz.m2.s, %nz.t2.s
  %nz.c2.s = or i1 %nz.u2.s, %nz.v2.s
  %nz.t3.s = add i64 %nz.m3.a, %nz.m3.b
  %nz.z3.s = zext i1 %nz.c2.s to i64
  %nz.m3.s = add i64 %nz.t3.s, %nz.z3.s
  %nz.q0.w.0 = getelementptr i64, ptr %pr, i64 0
  store i64 %nz.m0.s, ptr %nz.q0.w.0, align 8
  %nz.q1.w.0 = getelementptr i64, ptr %pr, i64 1
  store i64 %nz.m1.s, ptr %nz.q1.w.0, align 8
  %nz.q2.w.0 = getelementptr i64, ptr %pr, i64 2
  store i64 %nz.m2.s, ptr %nz.q2.w.0, align 8
  %nz.q3.w.0 = getelementptr i64, ptr %pr, i64 3
  store i64 %nz.m3.s, ptr %nz.q3.w.0, align 8
  ret void
}
```

```text native=n-wideint
w(limbs a = [0xffffffffffffffff, 0xffffffffffffffff, 5, 1], b = [1, 0, 0xffffffffffffffff, 2]) -> r = [0, 0, 5, 4]
w(limbs a = [all ones x 4], b = [1, 0, 0, 0]) -> r = [0, 0, 0, 0]
```

*(non-normative)* Limbs are least significant first. Limb 0: 2^64 − 1 + 1 = 0, carry 1; limb 1:
2^64 − 1 + 0 + 1 = 0, carry 1; limb 2: 5 + 2^64 − 1 + 1 = 5, carry 1; limb 3: 1 + 2 + 1 = 4.

Allocas move to the shadow stack (N24, §17.3); the frame is zero-filled, so the read of
`b[2]`, undefined in the input, is 0:

```llvm normalise-in=n-shadow-stack
define internal i64 @a(i64 %x) {
  %b = alloca [3 x i64], align 8
  %p = getelementptr [3 x i64], ptr %b, i64 0, i64 1
  store i64 %x, ptr %p, align 8
  %q = getelementptr [3 x i64], ptr %b, i64 0, i64 2
  %v = load i64, ptr %q, align 8
  %w = load i64, ptr %p, align 8
  %r = add i64 %v, %w
  ret i64 %r
}
```

```llvm normalise-out=n-shadow-stack
define internal i64 @a(i64 %x) {
  %nz.fp.a = call ptr @__bennett_rt_ss_push(i64 24, i64 8)
  %b = getelementptr i8, ptr %nz.fp.a, i64 0
  %p = getelementptr [3 x i64], ptr %b, i64 0, i64 1
  store i64 %x, ptr %p, align 8
  %q = getelementptr [3 x i64], ptr %b, i64 0, i64 2
  %v = load i64, ptr %q, align 8
  %w = load i64, ptr %p, align 8
  %r = add i64 %v, %w
  call void @__bennett_rt_ss_pop(ptr %nz.fp.a)
  ret i64 %r
}

declare ptr @__bennett_rt_ss_push(i64, i64)

declare void @__bennett_rt_ss_pop(ptr)
```

```text native=n-shadow-stack
a(5) = 5 (output module; the input module's read of b[2] is undefined: the documented choice of N24)
a(-9) = -9 (output module)
```

Memory intrinsics (N26) and integer intrinsics (N27):

```llvm normalise-in=n-memintrinsics
define internal void @cp(ptr %d, ptr %s, i32 %n) {
  call void @llvm.memcpy.p0.p0.i64(ptr %d, ptr %s, i64 16, i1 false)
  call void @llvm.memset.p0.i32(ptr %d, i8 7, i32 %n, i1 false)
  ret void
}

declare void @llvm.memcpy.p0.p0.i64(ptr, ptr, i64, i1 immarg)

declare void @llvm.memset.p0.i32(ptr, i8, i32, i1 immarg)
```

```llvm normalise-out=n-memintrinsics
define internal void @cp(ptr %d, ptr %s, i32 %n) {
  call void @__bennett_rt_memmove(ptr %d, ptr %s, i64 16)
  %nz.n.cp.1 = zext i32 %n to i64
  call void @__bennett_rt_memset(ptr %d, i8 7, i64 %nz.n.cp.1)
  ret void
}

declare void @llvm.memcpy.p0.p0.i64(ptr, ptr, i64, i1 immarg)

declare void @llvm.memset.p0.i32(ptr, i8, i32, i1 immarg)

declare void @__bennett_rt_memmove(ptr, ptr, i64)

declare void @__bennett_rt_memset(ptr, i8, i64)
```

```text native=n-memintrinsics
cp(d, s = [100, 101, …, 115], 3) -> d = [7, 7, 7, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115]
```

```llvm normalise-in=n-intrinsics
define internal i32 @k(i32 %a, i32 %b) {
  %m = call i32 @llvm.smax.i32(i32 %a, i32 %b)
  %o = call { i32, i1 } @llvm.uadd.with.overflow.i32(i32 %a, i32 %b)
  %ov = extractvalue { i32, i1 } %o, 1
  %p = call i32 @llvm.ctpop.i32(i32 %m)
  %z = zext i1 %ov to i32
  %r = add i32 %p, %z
  ret i32 %r
}

declare i32 @llvm.smax.i32(i32, i32)

declare { i32, i1 } @llvm.uadd.with.overflow.i32(i32, i32)

declare i32 @llvm.ctpop.i32(i32)
```

```llvm normalise-out=n-intrinsics
define internal i32 @k(i32 %a, i32 %b) {
  %nz.c.m = icmp sgt i32 %a, %b
  %m = select i1 %nz.c.m, i32 %a, i32 %b
  %nz.s.o = add i32 %a, %b
  %nz.c.o = icmp ult i32 %nz.s.o, %a
  %nz.a.o = insertvalue { i32, i1 } zeroinitializer, i32 %nz.s.o, 0
  %o = insertvalue { i32, i1 } %nz.a.o, i1 %nz.c.o, 1
  %ov = extractvalue { i32, i1 } %o, 1
  %p = call i32 @__bennett_rt_ctpop_i32(i32 %m)
  %z = zext i1 %ov to i32
  %r = add i32 %p, %z
  ret i32 %r
}

declare i32 @llvm.smax.i32(i32, i32)

declare { i32, i1 } @llvm.uadd.with.overflow.i32(i32, i32)

declare i32 @llvm.ctpop.i32(i32)

declare i32 @__bennett_rt_ctpop_i32(i32)
```

```text native=n-intrinsics
k(7, -3) = 4
k(-1, -1) = 33
k(2147483647, 1) = 31
```

*(non-normative)* k(7, −3): smax = 7, ctpop(7) = 3, and 7 + 0xFFFFFFFD overflows 32 bits, so 3 +
1 = 4. k(−1, −1): ctpop(0xFFFFFFFF) = 32, overflow, 33. k(2^31 − 1, 1): ctpop = 31, no unsigned
overflow, 31.

Atomics are sequentialised (N9):

```llvm normalise-in=n-atomic
define internal i32 @at(ptr %p, i32 %v) {
  %old = atomicrmw add ptr %p, i32 %v seq_cst, align 4
  %ok = cmpxchg ptr %p, i32 %old, i32 0 seq_cst seq_cst, align 4
  %f = extractvalue { i32, i1 } %ok, 1
  %z = zext i1 %f to i32
  %r = add i32 %old, %z
  ret i32 %r
}
```

```llvm normalise-out=n-atomic
define internal i32 @at(ptr %p, i32 %v) {
  %nz.l.old = load i32, ptr %p, align 4
  %nz.v.old = add i32 %nz.l.old, %v
  store i32 %nz.v.old, ptr %p, align 4
  %nz.l.ok = load i32, ptr %p, align 4
  %nz.e.ok = icmp eq i32 %nz.l.ok, %nz.l.old
  %nz.s.ok = select i1 %nz.e.ok, i32 0, i32 %nz.l.ok
  store i32 %nz.s.ok, ptr %p, align 4
  %nz.a.ok = insertvalue { i32, i1 } zeroinitializer, i32 %nz.l.ok, 0
  %ok = insertvalue { i32, i1 } %nz.a.ok, i1 %nz.e.ok, 1
  %f = extractvalue { i32, i1 } %ok, 1
  %z = zext i1 %f to i32
  %r = add i32 %nz.l.old, %z
  ret i32 %r
}
```

```text native=n-atomic
at(p -> 5, 3) = 5, *p = 8
at(p -> 5, 0) = 6, *p = 0
```

The validator (§12.4) on a residue and on clean code:

```llvm example=residual-nsw verdict=reject:BD-E-RESIDUAL mode=validate
define internal i32 @f(i32 %a) {
  %s = add nsw i32 %a, 1
  ret i32 %s
}
```

```llvm example=residual-clean verdict=accept mode=validate
define internal i32 @f(i32 %a) {
  %s = add i32 %a, 1
  ret i32 %s
}
```

## 13. Floating point (arith contract)

NS §3.2: "Floating point is deterministic soft-float in both builds … Hardware floating point
never executes in either build." Every floating-point construct of every format has a row
here; none faults.

### 13.1 Soft-float rewrite (rules N19, N32)

**Formats and carriers:**

| LLVM type | Suffix | Carrier |
|---|---|---|
| `half` | `f16` | `i16` |
| `bfloat` | `bf16` | `i16` |
| `float` | `f32` | `i32` |
| `double` | `f64` | `i64` |
| `x86_fp80` | `f80` | `i80` |
| `fp128` | `f128` | `i128` |
| `ppc_fp128` | `ppcf128` | `i128` |

The rewrite of an instruction `%r` with floating-point operands or result is: first, for each
floating-point operand k (value or constant, in operand order), `%nz.<k>.r = bitcast <T>
<operand> to <carrier>`; then the call below, named `%nz.i.r`; then, for a floating-point result,
`%r = bitcast <carrier> %nz.i.r to <T>`. The entry points are defined by `bennett-arith` and are
part of its bitcode the driver links. B below is the format's suffix, C its carrier.

| Instruction | Call (carrier operands in order) | Result |
|---|---|---|
| `fadd`, `fsub`, `fmul`, `fdiv`, `frem` | `C @__bennett_sf_{add,sub,mul,div,rem}_B(C, C)` | bitcast |
| `fcmp <p>` | `i1 @__bennett_sf_cmp_B(C, C, i32 P)`, P the LLVM predicate number: `false` 0, `oeq` 1, `ogt` 2, `oge` 3, `olt` 4, `ole` 5, `one` 6, `ord` 7, `ueq` 8, `ugt` 9, `uge` 10, `ult` 11, `ule` 12, `une` 13, `uno` 14, `true` 15 | `%r` is the call itself |
| `fptosi`/`fptoui` to iM, `llvm.fptosi.sat`/`llvm.fptoui.sat` to iM | `i128 @__bennett_sf_{fptosi,fptoui}_B(C, i32 M)` | `%r = trunc i128 %nz.i.r to iM` (the call is `%r` when M = 128) |
| `sitofp`/`uitofp` from iM | `%nz.x.r = sext`/`zext iM a to i128` (omitted when M = 128), `C @__bennett_sf_{sitofp,uitofp}_B(i128)` | bitcast |
| `fpext`, `fptrunc` from format S to format D; `llvm.convert.to.fp16`, `llvm.convert.from.fp16` | `D_carrier @__bennett_sf_{fpext,fptrunc}_S_D(S_carrier)` | bitcast |
| `llvm.fptrunc.round(x, mode)` | `D_carrier @__bennett_sf_fptrunc_S_D_rm(S_carrier, i32 R)`, R from the mode (§13.5) | bitcast |
| `llvm.sqrt`, `llvm.floor`, `llvm.ceil`, `llvm.trunc`, `llvm.round`, `llvm.roundeven`, `llvm.rint`, `llvm.nearbyint`, `llvm.canonicalize` | `C @__bennett_sf_<name>_B(C)` | bitcast |
| `llvm.minnum`, `llvm.maxnum`, `llvm.minimum`, `llvm.maximum`, `llvm.minimumnum`, `llvm.maximumnum` | `C @__bennett_sf_<name>_B(C, C)` | bitcast |
| `llvm.fma` | `C @__bennett_sf_fma_B(C, C, C)` | bitcast |
| `llvm.is.fpclass(x, mask)` | `i1 @__bennett_sf_isfpclass_B(C, i32 mask)` | the call |
| `llvm.ldexp(x, e)`, `llvm.frexp(x)` | `C @__bennett_sf_ldexp_B(C, i32 e)`; `{ C, i32 } @__bennett_sf_frexp_B(C)` | bitcast (for frexp: of field 0) |
| `llvm.lround`, `llvm.llround`, `llvm.lrint`, `llvm.llrint` to iM | `i128 @__bennett_sf_{lround,llround,lrint,llrint}_B(C, i32 M)` | `trunc` to iM |
| `llvm.convert.to.arbitrary.fp`, `llvm.convert.from.arbitrary.fp` (format named by metadata) | `@__bennett_sf_convert_to_<fmt>_B` / `@__bennett_sf_convert_from_<fmt>_B` with LLVM APFloat's semantics of the named format | bitcast |
| `fneg`, `llvm.fabs`, `llvm.copysign`, `bitcast`, `load`, `store`, `select`, `phi` | unchanged: bit-exact operations (LangRef) | – |

**Semantics of the entry points** (the contract with `bennett-arith`): IEEE 754-2019 for
binary16 (`half`), binary32, binary64 and binary128; `bfloat` is the IEEE-style format with 8
exponent and 7 fraction bits; `x86_fp80` is the 80-bit x87 extended format (64-bit significand
with explicit integer bit; encodings with exponent ≠ 0 and integer bit 0, the unnormals, and
pseudo-denormals and pseudo-infinities are treated as NaN inputs, as modern x87 hardware does);
`ppc_fp128` is double-double with the operations of LLVM's APFloat `PPCDoubleDouble` semantics of
the major in use. For all formats: round to nearest ties to even, subnormals supported, no
observable flags or exceptions (except §13.5); **every NaN result is the format's canonical NaN**
(sign 0, quiet bit set, other payload bits 0: `0x7E00` f16, `0x7FC0` bf16, `0x7FC00000` f32,
`0x7FF8000000000000` f64, `0x7FFFC000000000000000` f80, `0x7FFF8000…0` f128, and for ppcf128
the f64 canonical NaN in the high double and +0 in the low); `rem` is C `fmod` (exact, the sign of
the dividend); `cmp` is LLVM's `fcmp` for the predicate; `fptosi`/`fptoui` and the `.sat` forms
truncate toward zero, map NaN to 0 and saturate values outside the range of iM to its bounds,
returned sign-extended (`fptosi`) or zero-extended (`fptoui`) in i128; `sitofp`/`uitofp` round to
nearest even; `minnum`/`maxnum` are IEEE 754-2008 minNum/maxNum (one NaN operand: the other
operand; two: the canonical NaN) with −0 < +0; `minimum`/`maximum` are IEEE 754-2019 (either NaN:
the canonical NaN) with −0 < +0; `minimumnum`/`maximumnum` are IEEE 754-2019 minimumNumber/
maximumNumber; `sqrt`, `fma` and every rounding function are correctly rounded (`round` ties
away from zero, `rint` and `nearbyint` to nearest even); `fpext` is exact; `fptrunc` rounds to
nearest even; `canonicalize` maps every NaN to the canonical NaN and is the identity otherwise;
`is.fpclass` tests LangRef's ten classes on the bit pattern; `ldexp`/`frexp` are exact up to
rounding of a subnormal `ldexp` result; `lround`/`llround` round half away from zero and `lrint`/
`llrint` to nearest even, saturating like `fptosi`. *(non-normative)* `fneg`, `fabs` and
`copysign` stay bit-exact, so a NaN's sign bit set by `fneg` survives, as LangRef requires; an
implementation of `half` and `bfloat` + − × ÷ √ in binary32 followed by one rounding is
correctly rounded, since 24 ≥ 2p + 2 for p = 11 and p = 8 (Figueroa's double-rounding bound), but
the contract is correct rounding, so `fma` needs its own implementation.

### 13.2 Vector floating point

After N21 every vector floating-point operation is scalar: §13.1 applies lane by lane, and
`vector.reduce.fadd`/`fmul` are the ordered left folds of §12.6 (exact once N2 has removed
`reassoc`).

### 13.3 Formats beyond binary32 and binary64

All seven formats of §13.1 are covered by the same table and contract (NS §3.2: "coverage-report
lines until the library covers them"; `bennett-arith` covers them, so they are `lowered`). musl's
`fmt_fp` (`printf("%Lf")`, rung 3) uses `x86_fp80` on x86-64 and `fp128` on AArch64 and RISC-V64.

### 13.4 Transcendentals and libm intrinsics (N33)

`llvm.sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sinh`, `cosh`, `tanh`, `exp`, `exp2`,
`exp10`, `log`, `log2`, `log10`, `pow`, `powi`, `sincos`, `sincospi` and `modf` become calls of
the **runtimes libm**: `@<name>` for `double`, `@<name>f` for `float`, `@<name>l` for the
target's `long double` (`x86_fp80` or `fp128`), and for `half`, `bfloat` and the other
`fp128`/`ppc_fp128` cases the call of the `float`, respectively `long double`, function on the
`fpext`ed value followed by `fptrunc`; `powi(x, n)` becomes `__bennett_rt_powi_B(x, n)` (the
repeated squaring of compiler-rt's `__powidf2`); `sincos(x)` becomes the pair (sin x, cos x),
`sincospi(x)` the pair (sinpi x, cospi x), `modf(x)` the pair (fractional, integral). The runtimes
libm is musl-derived and compiled through this pipeline, so it is soft-float code itself and the
same function runs in both builds; calls of `sin`, `exp`, … in source resolve to it by §4.5. The
certificate records the runtimes version. No correct-rounding claim is required; bit-exact
determinism is (NS §3.2).

### 13.5 Constrained intrinsics, `strictfp` and the floating-point environment

`llvm.experimental.constrained.<op>(…, metadata <rounding>, metadata <except>)` becomes the
soft-float call of §13.1 with the suffix `_rm` and an extra `i32 R` operand: R = 0 for
`round.tonearest`, 1 `round.downward`, 2 `round.upward`, 3 `round.towardzero`, 4
`round.tonearestaway`, and for `round.dynamic` the value loaded from the runtimes global
`__bennett_rt_fenv` (field `round`); when `<except>` is not `fpexcept.ignore`, the entry point
ORs the IEEE flags it raises (invalid 1, divbyzero 2, overflow 4, underflow 8, inexact 16) into
`__bennett_rt_fenv` (field `flags`). `llvm.get.rounding`, `set.rounding`, `get.fpenv`,
`set.fpenv`, `reset.fpenv`, `get.fpmode`, `set.fpmode`, `reset.fpmode` read and write that state;
musl's `<fenv.h>` functions in `bennett-runtimes` do the same. Unconstrained operations use round
to nearest and raise no flags, as LLVM assumes of the default environment. A `strictfp` call-site
attribute on a marker is benign (§3.6).

### 13.6 Examples

```llvm normalise-in=n-fmuladd
define internal double @fm(double %a, double %b, double %c) {
  %r = call double @llvm.fmuladd.f64(double %a, double %b, double %c)
  ret double %r
}

declare double @llvm.fmuladd.f64(double, double, double)
```

```llvm normalise-out=n-fmuladd
define internal double @fm(double %a, double %b, double %c) {
  %nz.0.nz.m.r = bitcast double %a to i64
  %nz.1.nz.m.r = bitcast double %b to i64
  %nz.i.nz.m.r = call i64 @__bennett_sf_mul_f64(i64 %nz.0.nz.m.r, i64 %nz.1.nz.m.r)
  %nz.m.r = bitcast i64 %nz.i.nz.m.r to double
  %nz.0.r = bitcast double %nz.m.r to i64
  %nz.1.r = bitcast double %c to i64
  %nz.i.r = call i64 @__bennett_sf_add_f64(i64 %nz.0.r, i64 %nz.1.r)
  %r = bitcast i64 %nz.i.r to double
  ret double %r
}

declare double @llvm.fmuladd.f64(double, double, double)

declare i64 @__bennett_sf_mul_f64(i64, i64)

declare i64 @__bennett_sf_add_f64(i64, i64)
```

```text native=n-fmuladd
fm(1.5, 2.0, 0.25) = 3.25 (0x400a000000000000), input and output modules
fm(0.1, 10.0, -1.0) = 0.0 (0x0000000000000000), output module on every target; input module: 0.0 for -march=x86-64, 5.551115123125783e-17 (0x3c90000000000000) for -march=haswell
```

*(non-normative)* The double nearest 0.1 is 0x3FB999999999999A = 0.1 + 2^−54/10 exactly, so its
exact product with 10 is 1 + 2^−54. Unfused, the product rounds to 1.0 (2^−54 is below half an
ulp of 1, 2^−53) and adding −1.0 gives 0.0; fused, the exact 1 + 2^−54 − 1 = 2^−54 is returned.
`llvm.fmuladd` lets the code generator choose, so the input module's result depends on the CPU;
N16 fixes the unfused meaning in both builds (spike F4).

Extended precision and libm intrinsics (N33):

```llvm normalise-in=n-fp80
define internal x86_fp80 @l(x86_fp80 %a, double %d) {
  %e = fpext double %d to x86_fp80
  %r = fadd x86_fp80 %a, %e
  ret x86_fp80 %r
}
```

```llvm normalise-out=n-fp80
define internal x86_fp80 @l(x86_fp80 %a, double %d) {
  %nz.0.e = bitcast double %d to i64
  %nz.i.e = call i80 @__bennett_sf_fpext_f64_f80(i64 %nz.0.e)
  %e = bitcast i80 %nz.i.e to x86_fp80
  %nz.0.r = bitcast x86_fp80 %a to i80
  %nz.1.r = bitcast x86_fp80 %e to i80
  %nz.i.r = call i80 @__bennett_sf_add_f80(i80 %nz.0.r, i80 %nz.1.r)
  %r = bitcast i80 %nz.i.r to x86_fp80
  ret x86_fp80 %r
}

declare i80 @__bennett_sf_fpext_f64_f80(i64)

declare i80 @__bennett_sf_add_f80(i80, i80)
```

```llvm normalise-in=n-libm
define internal double @e(double %x, float %y) {
  %a = call double @llvm.exp.f64(double %x)
  %b = call float @llvm.sin.f32(float %y)
  %c = fpext float %b to double
  %r = fadd double %a, %c
  ret double %r
}

declare double @llvm.exp.f64(double)

declare float @llvm.sin.f32(float)
```

```llvm normalise-out=n-libm
define internal double @e(double %x, float %y) {
  %a = call double @exp(double %x)
  %b = call float @sinf(float %y)
  %nz.0.c = bitcast float %b to i32
  %nz.i.c = call i64 @__bennett_sf_fpext_f32_f64(i32 %nz.0.c)
  %c = bitcast i64 %nz.i.c to double
  %nz.0.r = bitcast double %a to i64
  %nz.1.r = bitcast double %c to i64
  %nz.i.r = call i64 @__bennett_sf_add_f64(i64 %nz.0.r, i64 %nz.1.r)
  %r = bitcast i64 %nz.i.r to double
  ret double %r
}

declare double @llvm.exp.f64(double)

declare float @llvm.sin.f32(float)

declare double @exp(double)

declare float @sinf(float)

declare i64 @__bennett_sf_fpext_f32_f64(i32)

declare i64 @__bennett_sf_add_f64(i64, i64)
```

*(non-normative)* The calls of `exp` and `sinf` pass `double` and `float` values, which are
bit-exact moves; they resolve by §4.5 to the runtimes libm, whose own floating-point code has been
normalised by §13.1. N33 runs before N32 (§12.1), so its declarations precede N32's; the libm
calls it creates are not floating-point instructions in the sense of §13.1 (they pass bit-exact
values) and N32 leaves them alone.

## 14. Calls and control transfer

### 14.1 Direct calls and recursion

Direct calls lower to CC/R `call` (ISA §4.1) and to lifted `lift.call`/`lift.ret` lprocs (ISA
§3.7), with the depth and stack faults of the budget (§9). Recursion is unrestricted.

### 14.2 Indirect calls

- **Candidate set** of an indirect call with callee value v: every `FN(F)` atom of AV(v) (§5),
  resolved through aliases; if AV(v) has the ⊤ flag, in addition every function whose LLVM
  function type equals the call's and whose address is used anywhere in the linked program
  (sound for defined C, C++ and Rust: a call through an incompatible type is undefined, and
  compatible C types lower to the same LLVM type under opaque pointers; SQLite §3). The device
  closure includes every candidate (§4.1).
- **Dispatch**: the compare tree of §16.4 over the candidates' A(F) values, sorted unsigned, with
  a static call at each leaf: CC/R `icmp eq` + `br` + `call @F_k` (ISA §4.1), lifted `lift.icmp.eq`
  + `qbranch` + `lift.call @L(F_k)` (ISA §4.2). `qjumpr` is intra-function only (ISA §4.2) and is
  not used for calls.
- **No match** (a value that is the address of no function of the program, or of a function
  without bitcode): F(4) `FAULT_UB_TRAP` (outline E13; calling through such a pointer is undefined
  or reaches code without bitcode, which the coverage report names). **Zero candidates**: F(4) at
  the site.
- **Trampolines** (`llvm.init.trampoline(t, f, nval)`, `llvm.adjust.trampoline(t)`): `init`
  stores the tag `0x42454E54` (i32), A(f) and nval in the trampoline memory t (runtimes
  `__bennett_rt_tramp_init`); `adjust` returns t. Before the compare tree, an indirect call whose
  callee value v points to a live allocation holding the tag at offset 0 calls the stored
  function with the stored nest value as its `nest` argument.
- Calls through a variadic function type use §14.3. The same compare-tree construction serves
  region operands (§7.2), handle ids (§6.5), descriptor shapes (§8.4), `switch` (§14.8) and
  `indirectbr` (§14.9).

```llvm example=indirect-table verdict=accept callees=gt,lt
define internal i32 @lt(i32 %a, i32 %b) {
  %c = icmp slt i32 %a, %b
  %r = zext i1 %c to i32
  ret i32 %r
}

define internal i32 @gt(i32 %a, i32 %b) {
  %c = icmp sgt i32 %a, %b
  %r = zext i1 %c to i32
  ret i32 %r
}

@cmps = internal constant [2 x ptr] [ptr @lt, ptr @gt]

define void @pick(i32 %which, i32 %a, i32 %b) {
entry:
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  %k = and i32 %which, 1
  %i = zext i32 %k to i64
  %p = getelementptr [2 x ptr], ptr @cmps, i64 0, i64 %i
  %f = load ptr, ptr %p
  %r = call i32 %f(i32 %a, i32 %b)
  %t = icmp ne i32 %r, 0
  br i1 %t, label %flip, label %out

flip:
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  br label %out

out:
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

A callee from host input dispatches over the address-taken functions of the call's type; here
`@lt` and `@gt` (their addresses are stored in `@cmps`), but not `@neg`, whose type differs:

```llvm example=indirect-host-pointer verdict=accept callees=gt,lt
define internal i32 @lt(i32 %a, i32 %b) {
  %c = icmp slt i32 %a, %b
  %r = zext i1 %c to i32
  ret i32 %r
}

define internal i32 @gt(i32 %a, i32 %b) {
  %c = icmp sgt i32 %a, %b
  %r = zext i1 %c to i32
  ret i32 %r
}

define internal i32 @neg(i32 %a) {
  %r = sub i32 0, %a
  ret i32 %r
}

@cmps = global [2 x ptr] [ptr @lt, ptr @gt]
@unary = global ptr @neg

define void @apply(ptr %f, i32 %a, i32 %b) {
entry:
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  %r = call i32 %f(i32 %a, i32 %b)
  %t = icmp ne i32 %r, 0
  br i1 %t, label %flip, label %out

flip:
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  br label %out

out:
  call void @__bennett_qfree(ptr %h)
  ret void
}
```

### 14.3 Varargs (N23)

- A variadic definition `R @f(P…, ...)` becomes `R @f(P…, ptr %nz.va)`; every call of it, direct
  or through a variadic function type, passes a **va block** in place of the variadic arguments.
- A call site spills its variadic arguments (as the front end promoted them) into a va block
  `%nz.vb.<r>`, an alloca of the caller's entry block (so N24 places it in the caller's shadow
  frame), in argument order: argument j at the next offset aligned to max(8, ABI alignment of its
  type), occupying its size rounded up to 8 bytes (the x86-64 System V, AAPCS64 and RISC-V LP64
  memory-argument layout); argument j ≥ 1 is addressed by `%nz.vb<j>.<r>`.
- `llvm.va_start(ptr ap)` builds the target's `va_list` so that the front end's inline `va_arg`
  takes its memory path:

  | Target | `va_list` | Fields written by `va_start` |
  |---|---|---|
  | x86-64 System V | `{ i32 gp_offset, i32 fp_offset, ptr overflow_arg_area, ptr reg_save_area }` | gp_offset = 48, fp_offset = 176, overflow_arg_area = `%nz.va`, reg_save_area = null (SQLite §5.1): every `va_arg` finds no register slot left |
  | AArch64 AAPCS64 | `{ ptr __stack, ptr __gr_top, ptr __vr_top, i32 __gr_offs, i32 __vr_offs }` | __stack = `%nz.va`, __gr_top = __vr_top = null, __gr_offs = __vr_offs = 0 |
  | RISC-V LP64 | `ptr` | the pointer `%nz.va` |

  The stores are named `%nz.vfo.<r>` (x86-64 `fp_offset` address), `%nz.vov.<r>` (overflow area
  address), `%nz.vrs.<r>` (register save area address); AArch64 and RISC-V use `%nz.vs.<r>`,
  `%nz.vgt.<r>`, `%nz.vvt.<r>`, `%nz.vgo.<r>`, `%nz.vvo.<r>` in field order.
- IR `va_arg` is expanded by the same memory layout; `llvm.va_copy(d, s)` copies the
  `va_list` record (24, 32 or 8 bytes); `llvm.va_end` is deleted.
- A call of an external variadic function without bitcode passes the va block to its host call
  (§11.4) or is trapped (§4.5). One table row per target ABI; adding a target adds a row (§24).

```llvm normalise-in=n-varargs
%struct.__va_list_tag = type { i32, i32, ptr, ptr }

define internal i32 @sum(i32 %n, ...) {
entry:
  %ap = alloca %struct.__va_list_tag, align 16
  call void @llvm.va_start(ptr %ap)
  br label %loop

loop:
  %i = phi i32 [ 0, %entry ], [ %i2, %got ]
  %s = phi i32 [ 0, %entry ], [ %s2, %got ]
  %done = icmp sge i32 %i, %n
  br i1 %done, label %out, label %arg

arg:
  %gp = load i32, ptr %ap, align 16
  %fits = icmp ult i32 %gp, 41
  br i1 %fits, label %inreg, label %inmem

inreg:
  %rsap = getelementptr %struct.__va_list_tag, ptr %ap, i64 0, i32 3
  %rsa = load ptr, ptr %rsap, align 16
  %gp64 = zext i32 %gp to i64
  %ra = getelementptr i8, ptr %rsa, i64 %gp64
  %gp2 = add i32 %gp, 8
  store i32 %gp2, ptr %ap, align 16
  br label %got

inmem:
  %ovp = getelementptr %struct.__va_list_tag, ptr %ap, i64 0, i32 2
  %ov = load ptr, ptr %ovp, align 8
  %ov2 = getelementptr i8, ptr %ov, i64 8
  store ptr %ov2, ptr %ovp, align 8
  br label %got

got:
  %addr = phi ptr [ %ra, %inreg ], [ %ov, %inmem ]
  %v = load i32, ptr %addr, align 4
  %s2 = add i32 %s, %v
  %i2 = add i32 %i, 1
  br label %loop

out:
  call void @llvm.va_end(ptr %ap)
  ret i32 %s
}

define i32 @top(i32 %x) {
  %r = call i32 (i32, ...) @sum(i32 3, i32 %x, i32 20, i32 300)
  ret i32 %r
}

declare void @llvm.va_start(ptr)

declare void @llvm.va_end(ptr)
```

```llvm normalise-out=n-varargs
%struct.__va_list_tag = type { i32, i32, ptr, ptr }

define internal i32 @sum(i32 %n, ptr %nz.va) {
entry:
  %nz.fp.sum = call ptr @__bennett_rt_ss_push(i64 24, i64 16)
  %ap = getelementptr i8, ptr %nz.fp.sum, i64 0
  store i32 48, ptr %ap, align 4
  %nz.vfo.sum.0 = getelementptr i8, ptr %ap, i64 4
  store i32 176, ptr %nz.vfo.sum.0, align 4
  %nz.vov.sum.0 = getelementptr i8, ptr %ap, i64 8
  store ptr %nz.va, ptr %nz.vov.sum.0, align 8
  %nz.vrs.sum.0 = getelementptr i8, ptr %ap, i64 16
  store ptr null, ptr %nz.vrs.sum.0, align 8
  br label %loop

loop:
  %i = phi i32 [ 0, %entry ], [ %i2, %got ]
  %s = phi i32 [ 0, %entry ], [ %s2, %got ]
  %done = icmp sge i32 %i, %n
  br i1 %done, label %out, label %arg

arg:
  %gp = load i32, ptr %ap, align 16
  %fits = icmp ult i32 %gp, 41
  br i1 %fits, label %inreg, label %inmem

inreg:
  %rsap = getelementptr %struct.__va_list_tag, ptr %ap, i64 0, i32 3
  %rsa = load ptr, ptr %rsap, align 16
  %gp64 = zext i32 %gp to i64
  %ra = getelementptr i8, ptr %rsa, i64 %gp64
  %gp2 = add i32 %gp, 8
  store i32 %gp2, ptr %ap, align 16
  br label %got

inmem:
  %ovp = getelementptr %struct.__va_list_tag, ptr %ap, i64 0, i32 2
  %ov = load ptr, ptr %ovp, align 8
  %ov2 = getelementptr i8, ptr %ov, i64 8
  store ptr %ov2, ptr %ovp, align 8
  br label %got

got:
  %addr = phi ptr [ %ra, %inreg ], [ %ov, %inmem ]
  %v = load i32, ptr %addr, align 4
  %s2 = add i32 %s, %v
  %i2 = add i32 %i, 1
  br label %loop

out:
  call void @__bennett_rt_ss_pop(ptr %nz.fp.sum)
  ret i32 %s
}

define i32 @top(i32 %x) {
  %nz.fp.top = call ptr @__bennett_rt_ss_push(i64 24, i64 8)
  %nz.vb.r = getelementptr i8, ptr %nz.fp.top, i64 0
  store i32 %x, ptr %nz.vb.r, align 8
  %nz.vb1.r = getelementptr i8, ptr %nz.vb.r, i64 8
  store i32 20, ptr %nz.vb1.r, align 8
  %nz.vb2.r = getelementptr i8, ptr %nz.vb.r, i64 16
  store i32 300, ptr %nz.vb2.r, align 8
  %r = call i32 @sum(i32 3, ptr %nz.vb.r)
  call void @__bennett_rt_ss_pop(ptr %nz.fp.top)
  ret i32 %r
}

declare ptr @__bennett_rt_ss_push(i64, i64)

declare void @__bennett_rt_ss_pop(ptr)
```

```text native=n-varargs
top(1) = 321
top(-320) = 0
top(2147483000) = 2147483320
```

*(non-normative)* The input is the shape clang's inline x86-64 `va_arg` expansion takes after
`default<O2>` (with the loop bound left as a parameter). With gp_offset = 48 the `fits` test
(gp_offset < 41) is always false, so every argument is read from `overflow_arg_area`, which is the
va block: slots at offsets 0, 8, 16 hold x, 20, 300, and the sum is x + 320.

### 14.4 Unwinding (N28: explicit propagation)

The runtimes keep the **EH state** in the global `__bennett_rt_eh` of type `{ i32 active, i32
selector, ptr object }` (active: 0 none, 1 exception, 2 longjmp, 3 fiber switch, 4 exit; §14.5–
§14.7). Every device variant is rewritten, and the native comparison build uses the same
materialised code, so the behaviour is identical in both builds:

- `invoke F(args) to label %N unwind label %U` → `call F(args)`; `%nz.ehl.<r> = load i32, ptr
  @__bennett_rt_eh`; `%nz.ehc.<r> = icmp ne i32 %nz.ehl.<r>, 0`; `br i1 %nz.ehc.<r>, label %U,
  label %N`.
- A `call` of a function that may unwind (one without `nounwind`, or an indirect call) inside a
  function that may unwind → the same check after the call, branching on a set flag to the
  function's **early-return block** `nz.ehr.<f>`, which pops the shadow frame (§17.3) and returns
  the zero of the return type.
- `%r = landingpad T clauses` → `%r = call { ptr, i32 } @__bennett_rt_eh_match(ptr P, ptr
  @nz.lp.<f>.<r>)`, where P is the function's personality and `@nz.lp.<f>.<r>` is the private
  constant `{ i64 cleanup, i64 n, [n x { i64 kind, ptr info }] }` of the clauses in order (kind 0
  `catch` with its typeinfo, kind 1 `filter` with its array). The runtimes implement the
  personality's matching: for `__gxx_personality_v0`, C++ catch by typeinfo with the C++ ABI's
  derived-class rules and filters; for `rust_eh_personality`, Rust panics; for
  `__gcc_personality_v0`, cleanups only. A matching catch or a cleanup clears `active` and
  returns (object, selector) with selector = `llvm.eh.typeid.for` of the matched typeinfo (0 for
  a cleanup); when nothing matches (or the pseudo-exception is a longjmp, switch or exit, which no
  clause handles) the flag stays set, the selector is −1, and the normaliser's check after the
  call (`%nz.ehm.<r> = extractvalue … 1`, `icmp eq … −1`) branches to the early-return block.
- `resume v` → `call void @__bennett_rt_eh_resume({ ptr, i32 } v)` (sets `active` = 1 and the
  object) and a branch to the early-return block.
- `llvm.eh.typeid.for(ti)` → `call i32 @__bennett_rt_eh_typeid(ptr ti)`; `llvm.eh.exceptionpointer`
  and `llvm.eh.exceptioncode` read the state's object.
- `__cxa_throw`, `_Unwind_RaiseException`, `_Unwind_Resume`, `__rust_start_panic` are runtimes
  functions that set the state and return; the code after their call is the check above, and the
  original `unreachable` after them is kept on the path where the flag is clear (F(4)).
- Windows funclet pads (`catchswitch`, `catchpad`, `cleanuppad`, `catchret`, `cleanupret`) use the
  same transform with the `__CxxFrameHandler3` matching rules (corpus case needed, bd `-kdj`).
- **Unwinding out of a region**: a set flag when an oracle's region function returns is `fault 4`
  in the wrapper (§16.2); in an action's generation it is TDL-12's `fault` event with code 4; at
  an R entry or a CC device entry it ends the run with code 4 (§11.5). NS §3.1: "a fault code
  where it is not [handled in the region]".

```llvm normalise-in=n-eh
declare i32 @__gxx_personality_v0(...)

declare void @may_throw(i32)

define internal i32 @eh(i32 %x) personality ptr @__gxx_personality_v0 {
entry:
  invoke void @may_throw(i32 %x)
          to label %ok unwind label %lp

ok:
  ret i32 0

lp:
  %e = landingpad { ptr, i32 }
          catch ptr null
  ret i32 1
}
```

```llvm normalise-out=n-eh
@__bennett_rt_eh = external global { i32, i32, ptr }
@nz.lp.eh.e = private constant { i64, i64, [1 x { i64, ptr }] } { i64 0, i64 1, [1 x { i64, ptr }] [{ i64, ptr } { i64 0, ptr null }] }

declare i32 @__gxx_personality_v0(...)

declare void @may_throw(i32)

define internal i32 @eh(i32 %x) {
entry:
  call void @may_throw(i32 %x)
  %nz.ehl.eh.0 = load i32, ptr @__bennett_rt_eh, align 4
  %nz.ehc.eh.0 = icmp ne i32 %nz.ehl.eh.0, 0
  br i1 %nz.ehc.eh.0, label %lp, label %ok

ok:
  ret i32 0

lp:
  %e = call { ptr, i32 } @__bennett_rt_eh_match(ptr @__gxx_personality_v0, ptr @nz.lp.eh.e)
  %nz.ehm.e = extractvalue { ptr, i32 } %e, 1
  %nz.ehn.e = icmp eq i32 %nz.ehm.e, -1
  br i1 %nz.ehn.e, label %nz.ehr.eh, label %nz.lpc.e

nz.lpc.e:
  ret i32 1

nz.ehr.eh:
  ret i32 0
}

declare { ptr, i32 } @__bennett_rt_eh_match(ptr, ptr)
```

```text native=n-eh
eh(2) = 0; eh(3) = 1; eh(-5) = 1 (input built with clang++ and a C++ may_throw that throws when x is odd; output built with the runtimes seeds, whose may_throw sets the EH state)
```

### 14.5 setjmp and longjmp (N29)

- A call of `setjmp`, `_setjmp`, `sigsetjmp` or `__sigsetjmp` with buffer b in function f
  becomes a block boundary: `call void @__bennett_rt_setjmp(ptr b, ptr %nz.fp.<f>, i32 k)` stores
  the **frame token** (f's shadow-frame address, §17.3) and the site index k (0-based among f's
  setjmp sites) in b, and the call's result becomes the phi `%r = phi i32 [ 0, <normal> ], [ v,
  %nz.sj<k>.<f> ]` at the continuation.
- `longjmp(b, v)` (and `siglongjmp`, `_longjmp`) is a runtimes function that sets the EH state to
  the longjmp pseudo-exception (`active` = 2, object = b, selector = v, with v = 0 replaced by 1)
  and returns; propagation is §14.4 (landing pads do not handle it).
- In every function containing a setjmp site, the check after each call that may unwind also
  tests `active` = 2 and the frame token and site index stored in b; on a match it clears the
  state and branches to `%nz.sj<k>.<f>`, the continuation of site k with value v. SSA values live
  into the continuation take, on that path, their values at the call after which the longjmp was
  detected (C makes non-volatile locals modified after `setjmp` indeterminate; memory is the
  shadow frame's).
- This covers `longjmp` to an active frame, the only defined case in C, and Julia's `jl_try`
  (`sigsetjmp`, rung 5). A `longjmp` to a frame that has returned reaches the device entry and
  faults (code 4, §14.4).

A `longjmp` across two frames, as a whole program in the R tier; the expected status is the
native one:

```c example=sjlj-two-frames verdict=accept rmode=@main
#include <setjmp.h>

static jmp_buf jb;

static void deep(int n) {
  if (n == 0) longjmp(jb, 7);
  deep(n - 1);
}

static int try_deep(int n) {
  int r = setjmp(jb);
  if (r) return r;
  deep(n);
  return 0;
}

int main(void) { return try_deep(2) + 10 * try_deep(0); }
```

```text cc-run=sjlj-two-frames
driver: --bennett-tier=reversible --bennett-entry=main
run: status=COMPLETED results=[INT(32):77] faults=[]
native: exit status 77 (clang 18 and 23, -O2)
reverse: status=REVERSED memory=entry
```

### 14.6 Fibers and context switches (N30: rewindable frames)

- **Switch primitives**: the runtimes' `swapcontext`, `makecontext`, `setcontext`, Julia's task
  switch (`jl_swap_fiber`, `ctx_switch`), and the platform shims `swtch` and `__switch_to` (§20.5);
  all are implemented by `__bennett_rt_fiber_switch(from, to)` over records that hold a fiber's
  shadow stack (the `makecontext` stack argument) and its saved frame chain.
- Every function on a call-graph path to a switch primitive is **instrumented**, Asyncify-style:
  its SSA values that are live across a call that may switch are spilled to its shadow frame
  before the call and reloaded after it, and it gets a resume index (the call site it was
  suspended at).
- A switch sets the EH state to `active` = 3 and propagates (§14.4): each instrumented frame on
  the way out saves its resume index and returns early, up to the fiber's base; the runtime
  records the chain, then **rewinds** the target fiber: it calls the target's base with the
  rewind state, and each instrumented frame jumps to its saved resume index, reloads its values
  and calls the next frame, until the target's switch call returns.
- This works in CC, R and L on ISA 0.8: it is ordinary code over memory. G-16 (ISA fibers,
  §25.3) is the efficient alternative.

A `swapcontext` ping-pong in the R tier: the main fiber logs 0, 1, 2 and the second fiber 100,
101, 102, alternately; the status encodes the order (digits 0 0 1 1 2 2 give 1122, and 1122 mod
256 = 98):

```c example=fiber-pingpong verdict=accept rmode=@main
#include <ucontext.h>

static ucontext_t main_ctx, fiber_ctx;
static int trace[6], n;
static char fiber_stack[16384];

static void fiber(void) {
  for (int i = 0; i < 3; i++) {
    trace[n++] = 100 + i;
    swapcontext(&fiber_ctx, &main_ctx);
  }
}

int main(void) {
  getcontext(&fiber_ctx);
  fiber_ctx.uc_stack.ss_sp = fiber_stack;
  fiber_ctx.uc_stack.ss_size = sizeof fiber_stack;
  fiber_ctx.uc_link = &main_ctx;
  makecontext(&fiber_ctx, fiber, 0);
  for (int i = 0; i < 3; i++) {
    trace[n++] = i;
    swapcontext(&main_ctx, &fiber_ctx);
  }
  int s = 0;
  for (int i = 0; i < n; i++) s = s * 10 + trace[i] % 10;
  return s % 256;
}
```

```text cc-run=fiber-pingpong
driver: --bennett-tier=reversible --bennett-entry=main
run: status=COMPLETED results=[INT(32):98] faults=[]
native: exit status 98 (clang 18 and 23, -O2)
reverse: status=REVERSED memory=entry
```

### 14.7 `exit`, `abort`, `_Exit`

- `abort` → F(4).
- musl's `exit` runs the `atexit` handlers and flushes stdio, then calls `_Exit(s)`. `_Exit(s)`
  (the runtimes' `exit_group` system call) sets the EH state to the **exit pseudo-exception**
  (`active` = 4, selector = s) and propagates.
- An R or CC whole-program entry (§19.2) catches it and returns s as the program's status; an
  oracle wrapper in "oracle from program" mode (§19.3) catches it and delivers s as the payload;
  a CC device entry of a host program catches it and makes `hostcall bennett.exit` with s, whose
  host stub calls `_Exit(s)`. Elsewhere (inside an oracle in the plain marker form, inside an
  action) it is unwinding out of the region: code 4.

```c example=exit-status verdict=accept rmode=@main
#include <stdlib.h>

int main(void) {
  exit(3);
}
```

```text cc-run=exit-status
driver: --bennett-tier=reversible --bennett-entry=main
run: status=COMPLETED results=[INT(32):3] faults=[]
native: exit status 3 (clang 18 and 23, -O2)
```

### 14.8 `switch`

`switch` lowers by the compare tree of §16.4 in L, and by the same tree of `icmp`/`br` in CC and R
(ISA has no switch instruction).

### 14.9 `blockaddress` and `indirectbr`

`blockaddress(@f, %bb)` has the device value B(f) + i, where i is the index of %bb among f's k
address-taken blocks in layout order and B(f) is the base of a k-byte object
`__bennett_rt_blk.<f>` that the driver adds to the data section of the comparison link (§19.5) and
whose address the link map records. These values are nonzero, pairwise distinct and distinct from
every A(F) and every other object's bytes, so comparisons and dispatch on them are exact. `indirectbr ptr v, [labels]` dispatches with the compare
tree over the labels' values to static branches (`qjump` in L, `br` in CC/R); no match is F(4).
*(non-normative)* LangRef permits a `blockaddress` only in `indirectbr` and in comparisons with
null; an execution in which its bits influence a result otherwise (printing, hashing) is
layout-dependent and validated against the reference interpreter (NS §3.2, §17.1).

## 15. Inline asm and target intrinsics (asm 0.2)

NS §3.3: "Target intrinsics and asm are classified *lowered / trapped / shimmed* in the coverage
report." N31 applies the tables of this section.

### 15.1 Table format

An asm **row** is keyed by (target architecture, normalised asm string, constraint string):

- the asm string with every run of whitespace (including `\n`, `\t` and `;` separators) replaced
  by one space and leading and trailing whitespace removed, operand placeholders (`$0`, `${0:w}`)
  kept;
- the constraint string exactly as LLVM prints it (clobbers included).

A row has a **class** and a **replacement** in IR. Target-intrinsic rows are keyed by the
intrinsic name. The rows of this section are normative; they are also published as data files
`spec/asm/<arch>.toml` (`asm 0.2`, one table per architecture with the fields `asm`,
`constraints`, `class`, `replacement`), generated from this section; the section prevails on a
difference. Rows are added with a version change (§23).

### 15.2 Classes

- **lowered** (an IR replacement with the same meaning on the single-threaded device):
  - an empty asm string (any constraints without outputs) → deleted (a compiler barrier);
  - `pause` (x86), `nop` (all), `yield` (AArch64), `fence`, `fence rw,rw`, `fence.i` (RISC-V) and
    the target intrinsics `llvm.x86.sse2.pause`, `llvm.aarch64.hint` → deleted;
  - `rdtsc` (x86, `={ax},={dx}`), `rdtime`/`rdcycle` (RISC-V), `mrs $0, cntvct_el0` (AArch64),
    and `llvm.x86.rdtsc`, `llvm.readcyclecounter`, `llvm.readsteadycounter` → a call of
    `__bennett_rt_cyclecounter()`, which reads the clock model (§11) in every tier;
  - `cpuid` (x86) → a lookup in the constant leaf table of the declared CPU model
    (`--bennett-cpu=<model>`; default `x86-64`, whose table is the one the driver reads on the
    build machine and records in the build record, §19.9, §24 D33), so both builds and every
    tier see the same values;
  - asm-goto (`callbr`) whose asm string is lowered → its replacement followed by a branch to the
    default destination; `llvm.callbr.landingpad` → its operand.
- **shimmed** (a call of a runtimes or platform function):
  - the system-call instructions (§15.5) → `__bennett_rt_syscall(nr, a1, …, a6)`, the runtimes'
    system-call layer, which maps calls onto device models (§11.2) and runtimes services;
  - privileged forms → platform functions (§20.2).
- **trapped**: every other row → F(8) with a coverage line naming the asm string. This is
  required by NS §3.3 ("trapped"), and it occurs only on the executions that reach the asm.

### 15.3 Module-level asm and assembly objects

Symbols defined only by `module asm` or by non-bitcode objects (`.S` files) resolve like
external functions (§4.5): to a runtime or platform shim with the same symbol, recorded with its
content hash in the certificate's coverage entries (`shim_hash`), else trapped.

### 15.4 Target intrinsics

`llvm.x86.*`, `llvm.aarch64.*`, `llvm.riscv.*` and the other target families use rows of the same
form keyed by name; the rows the rungs need are those of §15.2 and §20.2; every other target
intrinsic is trapped until a row is added (a mechanics deferral, §24).

### 15.5 Required rows for 0.2

The musl `__syscall0` … `__syscall6` asm of the three architectures (rung 3). For k arguments the
replacement is `%r = call i64 @__bennett_rt_syscall(i64 nr, i64 a1, …, i64 ak, i64 0, …)` with
the absent arguments 0; `nr` and a1 … ak are the inputs named below.

| Architecture | asm | Constraints (k = 0 … 6) | Inputs |
|---|---|---|---|
| x86-64 | `syscall` | `={ax},{ax}` then the first k of `{di},{si},{dx},{r10},{r8},{r9}`, then `~{rcx},~{r11},~{memory},~{dirflag},~{fpsr},~{flags}` | nr = `{ax}`, a1 … ak in order |
| AArch64 | `svc 0` | `={x0},{x8}` then the first k of `{x0},{x1},{x2},{x3},{x4},{x5}`, then `~{memory},~{cc}` | nr = `{x8}`, a1 … ak in order |
| RISC-V64 | `ecall` | `={x10},{x17}` then the first k of `{x10},{x11},{x12},{x13},{x14},{x15}`, then `~{memory}` | nr = `{x17}`, a1 … ak in order |

*(non-normative)* These are the strings clang 18 and clang 23 produce from musl's
`arch/*/syscall_arch.h` (the RISC-V source string `ecall\n\t` normalises to `ecall`). The
xv6-riscv and Linux `tinyconfig` rows are §20.2, fixed by the platform spike (§20.7).

```llvm example=asm-musl-syscall verdict=accept
define i64 @write3(i64 %fd, ptr %buf) {
  %a = ptrtoint ptr %buf to i64
  %r = call i64 asm sideeffect "syscall", "={ax},{ax},{di},{si},{dx},~{rcx},~{r11},~{memory},~{dirflag},~{fpsr},~{flags}"(i64 1, i64 %fd, i64 %a, i64 3)
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @__bennett_qfree(ptr %h)
  ret i64 %r
}
```

```llvm normalise-in=n-asm
define internal i64 @w(i64 %fd, i64 %a) {
  %r = call i64 asm sideeffect "syscall", "={ax},{ax},{di},{si},{dx},~{rcx},~{r11},~{memory},~{dirflag},~{fpsr},~{flags}"(i64 1, i64 %fd, i64 %a, i64 3)
  call void asm sideeffect "", "~{memory},~{dirflag},~{fpsr},~{flags}"()
  ret i64 %r
}
```

```llvm normalise-out=n-asm
define internal i64 @w(i64 %fd, i64 %a) {
  %r = call i64 @__bennett_rt_syscall(i64 1, i64 %fd, i64 %a, i64 3, i64 0, i64 0, i64 0)
  ret i64 %r
}

declare i64 @__bennett_rt_syscall(i64, i64, i64, i64, i64, i64, i64)
```

## 16. The lifting map (map 0.2)

The lifting map turns a materialised region function, a binding shape (§8.4) and the link
layout (§19.5) into the **reference object** of that shape: the ISA object whose oracle `@ref`
defines F_B and the budget unit by the reference interpreter (ISA §4.2 "Reference body and
binding", §14.1). It is a function of its inputs alone, so two plugins on the same LLVM version
and pipeline produce byte-identical reference objects. Its version (`map 0.2`) is the
certificate's `dialect_mapping_version` (ISA §12.3). The plugin's device objects (§17.4) are
plugin-defined; they MUST be extensionally equal to the reference objects (ISA §5.7, T6; §18.7).

### 16.1 Liftable means materialised, always

Every materialised function is liftable (outline B1): §12 legalises every construct into integer
SSA values of at most 128 bits, memory, calls and branches, and §16.4 has a row for each. 0.1's
`BD-E-LIFT-SUBSET` is deleted.

### 16.2 The reference object

For a shape with region function f, the reference object is the ISA text (ISA §16) with:

- the header `bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8
  target=0.8 ptr_width=<pw>`;
- `section symbols`: one JCS line, keys `"0"`, `"1"`, … in the order `@ref`, `@L1` … `@Ln`, then
  the data symbols `G…` in `section data` order, each with its kind, name, signature (ISA §9.1;
  `args` types spelled as JCS strings of the ISA §16.2 type, e.g. `"i64"`) and interface hash
  (ISA §9.2);
- `section functions`: `@ref`, then the lprocs `@L1` … `@Ln`: one per function of the L closure of
  f (direct calls and indirect-call candidates), numbered in depth-first preorder from `@ref`
  along the `lift.call` rows in text order;
- `section data`: one line `G<n> <hex>` per global of the layout below, in `layout.globals` key
  order, with the global's initialiser bytes after §12 (function addresses encoded as A(F) in
  pw-bit little-endian, §4.4; pointers to globals as their bases plus offsets);
- `section layout`: one JCS line (§16.3).

**The wrapper `@ref`.** Its header is `oracle @ref (<ins>) (tgt:wire[T]) (fault:wire[4])
(<mems>) (<args>)`:

- `<ins>`: `x<k>:wire[n] in` for the k-th `IN` binding in parameter order (n = n(q));
- T: the width of the variant's slice (§8.6), or 1 when the shape has no output;
- `<mems>`: `m<k>:region[A,8] in` for the k-th `MEM_IN` binding in parameter order, then `e0` for
  an ENTROPY binding, `k0` for a BLOCK binding, `s0` for an entry-state snapshot (§8.5);
- `<args>`: `a<k>:i<W>` for the k-th `ARG` binding in parameter order (W = pw for a `ptr`).

Its body is one block `^entry():` with, in order:

1. **Prologue** (each part only when needed): the entry-state replay `t = lift.call
   @L(__bennett_rt_entry_replay) (s)` with `s = lift.addr @s0`; the device-state stores of §11.3
   (for ENTROPY: `d0 = lift.addr @e0`, `d1 = lift.addr @G(base)`, `lift.boundscheck d1 8`,
   `lift.store.i64 d1 d0`, `d2 = lift.const.i64 <2^A>`, `d3 = lift.addr @G(size)`,
   `lift.boundscheck d3 8`, `lift.store.i64 d3 d2`; the position starts at its data image 0; the
   other models likewise in model order); the shadow-stack setup `t = lift.call
   @L(__bennett_rt_ss_init) (c)` with c = `lift.const.i64 <sstack>` when the closure contains a
   call of `__bennett_rt_ss_push` (§17.3).
2. **Arguments**, for each parameter i in order: `IN` with n = W: the pseudo-location `x<k>`
   itself; `IN` with n < W: `w<i> = lift.zext.iW x<k>` (`lift.sext` for SEXT); `ARG`: `a<k>`
   itself; `MEM_IN`: `w<i> = lift.addr @m<k>`; `OUT`: `w<i> = lift.alloc <size>`.
3. **Call**: `r = lift.call @L1 (<arguments>)` (`r:reg[R]`, R the return width, 1 for `void`).
4. **Unwind check** (only when f may unwind, §14.4): `e = lift.addr @G(__bennett_rt_eh)`,
   `lift.boundscheck e 4`, `l = lift.load.i32 e`, `z = lift.const.i32 0`, `u = lift.icmp.ne l z`,
   `lift.faultif u 4`. A function **may unwind** iff it is not `nounwind` and calls (directly or
   through a candidate) a function that may unwind, an external function without `nounwind`, or
   one of the raise functions of §14.4 (least fixpoint).
5. **Delivery** of slice j of the payload: for the `tgt` output with n(tgt) < R: `c = lift.const.iR
   <n(tgt)>`, `t = lift.lshr r c`, `z = lift.const.iR 0`, `u = lift.icmp.ne t z`, `lift.faultif
   u 4` (the dropped-bits check of §8.2, in every variant); then the slice value: from `r` by
   `lift.lshr` of its low bit position (when nonzero) and `lift.trunc`/`lift.zext` to T (when the
   widths differ); from an `OUT` buffer `w<i>` by `p = lift.add w<i> <offset>` (when nonzero),
   `lift.boundscheck p <T/8>`, `v = lift.load.i<T> p`; then `lift.retval <value>`.

Wrapper locations are `w<i>` (arguments), `r` (the call's result), `d<k>` (prologue), and `c<j>`,
`t<j>` for its constants and temporaries in emission order.

**lprocs.** Each lifted function g becomes `lproc @L<n> (a0:reg[W0], …) (r:reg[R]) () () ()`
with the parameters in order (`ptr` → `reg[pw]`; an aggregate parameter flattened into one
parameter per field in field order), the result `r` of the return width (1 for `void`, whose
`ret void` is `lift.ret r`), a `regs` line, and the blocks of §16.4.

### 16.3 Names and layout

| LLVM entity | ISA name |
|---|---|
| the i-th parameter of g | `a<i>` (fields of a flattened aggregate `a<i>_<f>`) |
| the k-th instruction of g that produces a value (0-based, in layout order, phis included) | location `v<k>` (fields of an aggregate value `v<k>_<f>`) |
| the j-th constant materialisation of g, in text order of the output | location `c<j>` |
| the j-th mapping temporary of g, in text order | location `t<j>` |
| the i-th basic block of g (0-based, layout order) | block `^b<i>` |
| a block created by a compare tree in block i (§16.4), in creation order | `^b<i>.s<j>` (j ≥ 1) |
| for the q-th indirect call of block i (q ≥ 1): the leaf of candidate k (sorted order), the default, the continuation | `^b<i>.q<q>c<k>`, `^b<i>.q<q>d`, `^b<i>.q<q>r` |
| the edge block from block i to block s | `^b<i>.e<s>` |
| the n-th global of the layout | data symbol and global `G<n>` |

The `regs` line lists every location of the function that is neither a parameter nor the result,
in order of first appearance as a destination in the text, as `name:reg[W]`, separated by `, `;
it is omitted when empty. W: a value's width (`i1` → 1, `ptr` → pw); a constant's width; a
temporary's width (1 for a compare, else its operation's width).

**Layout.** The reference object's `layout` is the device link layout (§19.5) restricted to the
globals that the L closure names in `lift.addr` and, transitively, the globals their initialisers
point to (in link order, numbered G1, G2, …), with the link's `ptr_width`, `null_size`,
`heap_base`, `heap_limit_max`, `H`, `A_tab` and `S_cells`, and `interface_regions` = { "ref": the
shape's regions } with bases assigned in `<mems>` order: each base is the smallest multiple of
the region's size that is ≥ the end of the previous range (the heap's end `heap_base +
heap_limit_max` for the first). H is the smallest value with every range inside [0, 2^H); A_tab
is the smallest value with 2^A_tab ≥ P + `heap_limit_max`, P the link's number of globals plus
the largest number of interface regions of any oracle, so that allocation-table overflow never
precedes heap exhaustion (both fault with code 2, ISA §4.2, and a reference object with fewer
pre-entries than the device object faults at the same allocation); S_cells is the smallest value
with 2^S_cells ≥ the largest `stack` of the budget table.

### 16.4 Rows

Rows of an instruction are emitted in instruction order within its block. Before the rows of an
instruction, each of its **constant operands** that is a value operand (in operand order; not an
immediate flag; for `getelementptr`, not a constant index) is materialised: an integer constant by
`c<j> = lift.const.iW <unsigned decimal>`; `null` by `lift.const.i<pw> 0`; a global `@G` by
`c<j> = lift.addr @G<n>`; a function `@F` by `c<j> = lift.const.i<pw> <A(F)>`; a constant
expression by the rows of its instructions, innermost first, into temporaries. The operand then
reads `c<j>`. A non-constant operand reads the location of its value (`a<i>` for a parameter).
`A`, `B`, `C` below are the operands so read; `v` is the instruction's location.

| LLVM | Rows |
|---|---|
| `add sub mul and or xor shl lshr ashr` | `v = lift.<op> A B` |
| `udiv sdiv urem srem` | `v = lift.<op> A B` (division faults, ISA §4.2) |
| `icmp eq/ne/ult/ule/slt/sle a, b` (integers or pointers) | `v = lift.icmp.<pred> A B` |
| `icmp ugt/uge/sgt/sge a, b` | `v = lift.icmp.{ult,ule,slt,sle} B A` (operands swapped) |
| `select c, a, b` | `v = lift.select C A B` |
| `zext/sext/trunc a to iM` | `v = lift.<op>.iM A` |
| `ptrtoint` to iM, `inttoptr` from iM | M = pw: `v = lift.mov A`; ptrtoint M < pw or inttoptr M > pw: `lift.trunc`; otherwise `lift.zext` (LangRef zero-extends) |
| `bitcast` (integer to integer of equal width, pointer to pointer), `addrspacecast` | `v = lift.mov A` |
| `getelementptr T, ptr p, idx…` | acc := P; for each non-constant index in order: `t = lift.sext.i<pw> I` (or `lift.trunc`, omitted when the index is pw wide); if its element size s ≠ 1, `c = lift.const.i<pw> s` and `t′ = lift.mul t c`; `acc′ = lift.add acc t′`; then, if the constant byte offset Δ of the constant indices (mod 2^pw) ≠ 0, `c = lift.const.i<pw> Δ` and `lift.add acc c`. The last row writes v; with no row at all, `v = lift.mov P` |
| `load T, ptr p` (T = iN with N a multiple of 8, or `ptr`; N ≤ 128 after §12) | `lift.boundscheck P <N/8>`; `v = lift.load.iN P` |
| `store v, ptr p` | `lift.boundscheck P <N/8>`; `lift.store.iN P V` |
| `insertvalue`, `extractvalue` | `lift.mov` of the field locations |
| `phi` | none at its position (edge moves) |
| direct `call @g(args)` of a defined function | `v = lift.call @L(g) (A_1 … A_m)` (flattened arguments); a `void` callee writes a temporary `t<j>:reg[1]` |
| `call @__bennett_nz_alloc(n)`, `call @__bennett_nz_free(p)` | `v = lift.alloc N`; `lift.free P` |
| `call void @__bennett_nz_fault(i64 C)`; `unreachable` | `fault C` (one row for the pair) |
| indirect call | the compare tree below over the candidates' A(F_k) (§14.2) on the callee value, leaf k `v = lift.call @L(F_k) (…)` then `qjump` to the continuation, default `fault 4`; the rows after the call continue in the continuation block |
| `ret a` | `lift.ret A` (`void`: `lift.ret r`) |
| `unreachable` | `fault 4` |
| `br label %S` | edge moves (B → S); `qjump ^S` |
| `br i1 c, label %T, label %F`, T ≠ F | `qbranch C ^T′ ^F′` |
| `br i1 c, label %S, label %S` | as `br label %S` |
| `switch iW c, label %D [k_j, label %L_j]` | the compare tree below on C, cases sorted unsigned, default D′ |
| `indirectbr` | the compare tree over the block values of §14.9, leaves `qjump` |

**Compare tree** (outline E6) over sorted distinct keys k_lo … k_hi of width W, condition C,
targets T_j and default D, emitted into the current block X by node(lo, hi, X):

- if hi − lo + 1 ≤ 3: for j = lo … hi, in block X: `c = lift.const.iW k_j`; `t = lift.icmp.eq C
  c`; `qbranch t ^T_j ^Y`, where Y is a new block `^b<i>.s<n>` for j < hi and D for j = hi; X := Y;
- otherwise, with mid = ⌊(lo + hi)/2⌋: in X: `c = lift.const.iW k_mid`; `t = lift.icmp.ult C
  c`; new blocks L then R; `qbranch t ^L ^R`; node(lo, mid − 1, L); node(mid, hi, R);
- with no key: `qjump ^D`.

**Edge moves** (B → S), S with phis φ_1 … φ_r in S's order and incoming values a_1 … a_r for B:
the constant materialisations of the a_k that are constants (in order), then `(v_φ1, …, v_φr) =
lift.parmov (A_1, …, A_r)` (ISA §4.2, parallel). None when S has no phi. For a successor X of a
conditional terminator or of a compare-tree leaf in block i, X′ is `^b<i>.e<x>` when X has a phi,
else `^b<x>`; the **edge block** `^b<i>.e<x>` holds the edge moves (i → x) and `qjump ^b<x>`.

**Block order.** For i = 0, 1, …: block `^b<i>`, then the blocks created in it (compare-tree
blocks, and per indirect call its leaves, default and continuation) in creation order, then its
edge blocks in ascending successor index.

### 16.5 Runtime oracles, identity and F_B

The CC tier's entry-state transfer (§8.5) and TDL (§10) use three families of runtime oracles,
generated per width and part of the device object:

- `@xor128`: `oracle @xor128 () (t:wire[128]) (f:wire[4]) () (lo:i64, hi:i64)` with body `a =
  lift.zext.i128 lo`, `b = lift.zext.i128 hi`, `s = lift.const.i128 64`, `h = lift.shl b s`, `v =
  lift.or h a`, `lift.retval v` (6 steps; memoryless, ISA §7.2);
- `@xorargs<A>`: payload = a mod 2^A | m · 2^A for the classical arguments (a: i64, m: i8), a
  (A + 8)-wire target (TDL-4);
- `@firstfault<K>`: `in` = K 4-wire bundles, payload = the first nonzero one in order, else 0
  (TDL-8).

An oracle region's identity (§7.3) is the interface hash of `@ref` (ISA §9.2), recorded as the
certificate's `reference_program_hash` (ISA §12.3). F_B(x) is ISA §5.2's on `@ref` with the token's
budget (B, heap, stack, depth) (§9.4): success at `lift.retval` within B steps gives (payload, 0);
a fault row, a faulting division or memory row, or a budget flag gives (0, code); otherwise (0,
1). Stated results are lines `input=<x,…> [mem=<region>:<hex>] [arg=<value>] budget=<s,h,st,d>
-> code=<C> payload=<P> steps=<N>`, each the output of `bennett-isa-ref run-oracle <object> ref`
with those options.

### 16.6 Example: rung 1 (`inc8`, two inputs)

`inc8` of §8.8, one `IN` of 8 wires, an 8-wire target. The link has no globals; the budget table
has heap 0 and largest stack 7, so `heap_limit_max` = 0, A_tab = 0, S_cells = 3, and H = 12 covers
the null region [0, 4096):

```llvm lift=inc8 region=@inc8 desc=IN(8,zext);tgt=8
define internal i8 @inc8(i8 %x) {
  %r = add i8 %x, 1
  ret i8 %r
}
```

```text linkmap=inc8
null_size=4096 heap_base=4096 heap_limit_max=0 globals=none budget-table: stack max 7, heap max 0
```

```isa object=inc8
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=64

section symbols
{"0":{"interface_hash":"151baad5625b3605eadf87005a19ea6e012e4347d6dfe096dbc4edcf2b68b94a","kind":"oracle","name":"ref","signature":{"abi":"0.8","args":[],"fault":4,"in":[8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"1":{"interface_hash":"a8c86313c60cd75a4f013bdaaa43ed5db78c444b0338a3d41d98a3871929250e","kind":"lproc","name":"L1","signature":{"abi":"0.8","kind":"lproc","params":[8],"result":8,"tier":"q"}}}

section functions
oracle @ref (x0:wire[8] in) (tgt:wire[8]) (fault:wire[4]) () ()
regs { r:reg[8] }
^entry():
r = lift.call @L1 (x0)
lift.retval r
lproc @L1 (a0:reg[8]) (r:reg[8]) () () ()
regs { c0:reg[8], v0:reg[8] }
^b0():
c0 = lift.const.i8 1
v0 = lift.add a0 c0
lift.ret v0

section layout
{"A_tab":0,"H":12,"S_cells":3,"globals":{},"heap_base":4096,"heap_limit_max":0,"interface_regions":{"ref":{}},"null_size":4096,"ptr_width":64}
```

```text hash=inc8
ref 151baad5625b3605eadf87005a19ea6e012e4347d6dfe096dbc4edcf2b68b94a
L1 a8c86313c60cd75a4f013bdaaa43ed5db78c444b0338a3d41d98a3871929250e
```

```text run=inc8
input=0 budget=5,0,7,1 -> code=0 payload=1 steps=5
input=7 budget=5,0,7,1 -> code=0 payload=8 steps=5
input=255 budget=5,0,7,1 -> code=0 payload=0 steps=5
input=7 budget=4,0,7,1 -> code=1 payload=0 steps=4
input=7 budget=5,0,6,1 -> code=3 payload=0 steps=1
input=7 budget=5,0,7,0 -> code=3 payload=0 steps=1
```

```text step-check=inc8
budget=5,0,7,1 -> status=ok cases=256 input_and_memory_bits=8
```

*(non-normative)* Five steps: `lift.call`, the three rows of `@L1` (`lift.const`, `lift.add`,
`lift.ret`) and `lift.retval`. The call needs R_L1 = 3 + m′ = 3 + 4 = 7 stack cells (m′ = one
parameter, the result and two `regs`, ISA §3.7) and depth 1: with 6 cells or depth 0 the
`lift.call` flag gives `FAULT_BUDGET_DEPTH` (3) at step 1. 0.1's memoryless `inc8` body is
replaced by this wrapper form, so its hash changes (a draft-to-draft change, §23).

Two `IN` bindings (`oracle-two-in`, §8.8):

```llvm lift=add2 region=@add desc=IN(8,zext),IN(8,zext);tgt=9
define internal i9 @add(i8 %a, i8 %b) {
  %a9 = zext i8 %a to i9
  %b9 = zext i8 %b to i9
  %s = add i9 %a9, %b9
  ret i9 %s
}
```

```text linkmap=add2
null_size=4096 heap_base=4096 heap_limit_max=0 globals=none budget-table: stack max 9, heap max 0
```

```isa object=add2
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=64

section symbols
{"0":{"interface_hash":"5b4c6624e0f20b5d60780fd8f27056f3f7efd4d27b9d47af8a70c8126100a10a","kind":"oracle","name":"ref","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":9,"tier":"q"}},"1":{"interface_hash":"ad2332d5edae1d26b1c946a0d9f033c10c6e493be11c44ef5f910f548b3b2285","kind":"lproc","name":"L1","signature":{"abi":"0.8","kind":"lproc","params":[8,8],"result":9,"tier":"q"}}}

section functions
oracle @ref (x0:wire[8] in, x1:wire[8] in) (tgt:wire[9]) (fault:wire[4]) () ()
regs { r:reg[9] }
^entry():
r = lift.call @L1 (x0, x1)
lift.retval r
lproc @L1 (a0:reg[8], a1:reg[8]) (r:reg[9]) () () ()
regs { v0:reg[9], v1:reg[9], v2:reg[9] }
^b0():
v0 = lift.zext.i9 a0
v1 = lift.zext.i9 a1
v2 = lift.add v0 v1
lift.ret v2

section layout
{"A_tab":0,"H":12,"S_cells":4,"globals":{},"heap_base":4096,"heap_limit_max":0,"interface_regions":{"ref":{}},"null_size":4096,"ptr_width":64}
```

```text run=add2
input=200,100 budget=6,0,9,1 -> code=0 payload=300 steps=6
input=255,255 budget=6,0,9,1 -> code=0 payload=510 steps=6
input=0,0 budget=6,0,9,1 -> code=0 payload=0 steps=6
input=1,2 budget=6,0,8,1 -> code=3 payload=0 steps=1
```

```text step-check=add2
budget=6,0,9,1 -> status=ok cases=65536 input_and_memory_bits=16
```

### 16.7 Example: a reduced rung 4 (route A)

The shape of the SQLite oracle of SQLite §5.2(i), route A, at toy size: a page image in a `MEM_IN`
region (the database "fixed classically before entry", loaded into the register by
`__bennett_qprep`), its classical length as an `ARG`, a superposed record key as a 3-wire `IN`
(zero-extended to `i32`, like the 20-wire rowid), and a 1-wire target that receives an `i8`
result through the dropped-bits check. The library code is ordinary C with a recursive binary
search, a function-pointer callback through a constant table (an indirect call with two
candidates) and an error path that traps. The image is: byte 0 the predicate id, byte 1 the
record count n, then n records (key, value) sorted by key.

```c example=rung4-minidb verdict=accept
/* A reduced rung-4 "database": a 16-byte page image (predicate id, record count, sorted (key, value) records) */
#include <stdint.h>

typedef uint8_t (*pred_fn)(const uint8_t *rec);
static uint8_t pred_even(const uint8_t *rec) { return (rec[1] & 1) == 0; }
static uint8_t pred_big(const uint8_t *rec) { return rec[1] >= 100; }
static pred_fn const preds[2] = { pred_even, pred_big };

static const uint8_t *find(const uint8_t *base, uint32_t lo, uint32_t hi, uint32_t key) {
  if (lo >= hi) return 0;
  uint32_t mid = (lo + hi) / 2;
  const uint8_t *rec = base + 2 * mid;
  if (rec[0] == key) return rec;
  if (rec[0] < key) return find(base, mid + 1, hi, key);
  return find(base, lo, mid, key);
}

uint8_t q(const uint8_t *img, uint64_t len, uint32_t rowid) {
  uint32_t n = img[1];
  if (len < 2 + 2 * (uint64_t)n) __builtin_trap();
  const uint8_t *rec = find(img + 2, 0, n, rowid);
  if (!rec) return 0;
  return preds[img[0] & 1](rec);
}
```

The quantum programmer's translation unit (outline §19.3: the normative route is a separate TU
naming the unmodified function) applies one Grover iteration; it is linked with the library by
`clang -O2 -flto` and the driver's `lto<O3>`, after which the module holds 4 `qalloc`, 2 `qprep`,
24 `gate`, 1 `gate3`, 1 `oracle`, 3 `measure` and 4 `qfree` calls (counted on LLVM 18):

```c example=rung4-grover-tu verdict=accept
/* The quantum programmer's translation unit: one Grover iteration over the 3-bit rowid. */
#include <stdint.h>
#include "bennett_markers.h"

extern uint8_t q(const uint8_t *img, uint64_t len, uint32_t rowid);

static void hadamards(bennett_q r) {
  for (uint64_t i = 0; i < 3; i++) __bennett_gate(BENNETT_GATE_H, r, i);
}

static void phase_oracle(bennett_q db, bennett_q row, bennett_q t, bennett_q f) {
  BENNETT_ORACLE_DESC_P(3) d;
  bennett_oracle_desc_init(&d.h, 3, 0, t, f);
  bennett_bind_set(&d.param[0], BENNETT_BIND_MEM_IN, 0, db, 0, 16);
  bennett_bind_set(&d.param[1], BENNETT_BIND_ARG, 0, 0, 16, 0);
  bennett_bind_set(&d.param[2], BENNETT_BIND_IN, BENNETT_MODE_ZEXT, row, 0, 0);
  bennett_budget b = { 400, 0, 512, 8, 0 };
  __bennett_oracle((const void *)q, &b, &d.h);
}

static void diffusion(bennett_q row) {
  hadamards(row);
  for (uint64_t i = 0; i < 3; i++) __bennett_gate(BENNETT_GATE_X, row, i);
  __bennett_gate(BENNETT_GATE_H, row, 2);
  __bennett_gate3(BENNETT_GATE3_CCX, row, 0, row, 1, row, 2);
  __bennett_gate(BENNETT_GATE_H, row, 2);
  for (uint64_t i = 0; i < 3; i++) __bennett_gate(BENNETT_GATE_X, row, i);
  hadamards(row);
}

uint32_t grover_once(const uint8_t img[16]) {
  bennett_q db = __bennett_qalloc(BENNETT_CLASS_ANY, 128);
  bennett_q row = __bennett_qalloc(BENNETT_CLASS_ANY, 3);
  bennett_q t = __bennett_qalloc(BENNETT_CLASS_ANY, 1);
  bennett_q f = __bennett_qalloc(BENNETT_CLASS_ANY, 4);
  __bennett_qprep(db, img, 16);                   /* the database, fixed classically before entry */
  hadamards(row);
  __bennett_gate(BENNETT_GATE_X, t, 0);           /* |-> target: phase kickback */
  __bennett_gate(BENNETT_GATE_H, t, 0);
  phase_oracle(db, row, t, f);
  diffusion(row);
  uint32_t r = 0;
  for (uint64_t i = 0; i < 3; i++) r |= (uint32_t)__bennett_measure(row, i) << i;
  __bennett_gate(BENNETT_GATE_H, t, 0);
  __bennett_gate(BENNETT_GATE_X, t, 0);
  __bennett_qprep(db, img, 16);                   /* XOR again: db is clean */
  for (uint64_t i = 0; i < 3; i++) if ((r >> i) & 1) __bennett_gate(BENNETT_GATE_X, row, i);
  __bennett_qfree(f);
  __bennett_qfree(t);
  __bennett_qfree(row);
  __bennett_qfree(db);
  return r;
}
```

*(non-normative)* The descriptor's kinds and the budget record's fields reach the marker as
constant stores and `memset`s (PT7, PT8), so there is one shape. The MEM_IN register is the
static register of the root `db` (it is stored in the descriptor, so it has a static register
file with N = 1 by §6.5 rule 1); `f` stays clean when the fault rate is zero, and `t` returns to
|0⟩ after H and X.

The materialised region function and its closure, written in the shape the pipeline gives them
(the recursion kept, `__builtin_trap` already replaced by N11):

```llvm lift=rung4-mini region=@q desc=MEM_IN(4),ARG(64),IN(3,zext);tgt=1
@preds = internal constant [2 x ptr] [ptr @pred_even, ptr @pred_big]

define internal i8 @q(ptr %img, i64 %len, i32 %rowid) {
b0:
  %p1 = getelementptr i8, ptr %img, i64 1
  %n8 = load i8, ptr %p1
  %n = zext i8 %n8 to i32
  %n64 = zext i8 %n8 to i64
  %twon = shl i64 %n64, 1
  %need = add i64 %twon, 2
  %short = icmp ult i64 %len, %need
  br i1 %short, label %b1, label %b2

b1:
  call void @__bennett_nz_fault(i64 4)
  unreachable

b2:
  %base = getelementptr i8, ptr %img, i64 2
  %rec = call ptr @find(ptr %base, i32 0, i32 %n, i32 %rowid)
  %none = icmp eq ptr %rec, null
  br i1 %none, label %b3, label %b4

b3:
  ret i8 0

b4:
  %h8 = load i8, ptr %img
  %h = and i8 %h8, 1
  %hi = zext i8 %h to i64
  %pp = getelementptr [2 x ptr], ptr @preds, i64 0, i64 %hi
  %f = load ptr, ptr %pp
  %r = call i8 %f(ptr %rec)
  ret i8 %r
}

define internal ptr @find(ptr %base, i32 %lo, i32 %hi, i32 %key) {
b0:
  %e = icmp uge i32 %lo, %hi
  br i1 %e, label %b5, label %b1

b1:
  %s = add i32 %lo, %hi
  %mid = lshr i32 %s, 1
  %m2 = shl i32 %mid, 1
  %off = zext i32 %m2 to i64
  %rec = getelementptr i8, ptr %base, i64 %off
  %k8 = load i8, ptr %rec
  %k = zext i8 %k8 to i32
  %eq = icmp eq i32 %k, %key
  br i1 %eq, label %b6, label %b2

b2:
  %lt = icmp ult i32 %k, %key
  br i1 %lt, label %b3, label %b4

b3:
  %mid1 = add i32 %mid, 1
  %r1 = call ptr @find(ptr %base, i32 %mid1, i32 %hi, i32 %key)
  ret ptr %r1

b4:
  %r2 = call ptr @find(ptr %base, i32 %lo, i32 %mid, i32 %key)
  ret ptr %r2

b5:
  ret ptr null

b6:
  ret ptr %rec
}

define internal i8 @pred_even(ptr %rec) {
  %p = getelementptr i8, ptr %rec, i64 1
  %v = load i8, ptr %p
  %b = and i8 %v, 1
  %z = icmp eq i8 %b, 0
  %r = zext i1 %z to i8
  ret i8 %r
}

define internal i8 @pred_big(ptr %rec) {
  %p = getelementptr i8, ptr %rec, i64 1
  %v = load i8, ptr %p
  %c = icmp uge i8 %v, 100
  %r = zext i1 %c to i8
  ret i8 %r
}
```

```text linkmap=rung4-mini
null_size=4096 heap_base=8192 heap_limit_max=0
global @preds -> G1 base=4096 size=16
function @pred_even A=0x401160 (4198752)
function @pred_big A=0x4011a0 (4198816)
budget-table=rung4-mini (largest stack 1024, largest heap 0)
```

The L closure is `@q`, `@find`, `@pred_even`, `@pred_big`; in preorder from `@ref`'s call of `@q`
(L1), `@q`'s first `lift.call` is `@find` (L2), and its indirect call's candidates sorted by A(F)
are `@pred_even` (L3) and `@pred_big` (L4). The layout: one global and one region, so P = 2 and
A_tab = 1 (2^1 ≥ 2 + 0); the region m0 (16 bytes) is placed at 8192, the end of the empty heap;
H = 14 (8208 ≤ 2^14); S_cells = 10 (2^10 ≥ 1024):

```isa object=rung4-mini
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=64

section symbols
{"0":{"interface_hash":"15c371b8e02e1bef6e9fa5220a8b128e1547fe2cf192e68a1045b3bebfeb0800","kind":"oracle","name":"ref","signature":{"abi":"0.8","args":["i64"],"fault":4,"in":[3],"kind":"oracle","mem":[{"A":4,"W":8,"role":"in"}],"tgt":1,"tier":"q"}},"1":{"interface_hash":"72b9a373406320f3ff6cb69c9edce3a4d8e1ae7a7433d88286844ab68dc4db81","kind":"lproc","name":"L1","signature":{"abi":"0.8","kind":"lproc","params":[64,64,32],"result":8,"tier":"q"}},"2":{"interface_hash":"960dd380906f87a9154040ce51d207892a46574897dc749e72c31241bfe0517f","kind":"lproc","name":"L2","signature":{"abi":"0.8","kind":"lproc","params":[64,32,32,32],"result":64,"tier":"q"}},"3":{"interface_hash":"102ebe211e15cbb57f2ff0ce761197291d2e046c46e56d205939b4444660d3e6","kind":"lproc","name":"L3","signature":{"abi":"0.8","kind":"lproc","params":[64],"result":8,"tier":"q"}},"4":{"interface_hash":"ae731d00bf437af71b684013b35ab29dcd6a4ee5ef8c974abe32d7116c89ba37","kind":"lproc","name":"L4","signature":{"abi":"0.8","kind":"lproc","params":[64],"result":8,"tier":"q"}},"5":{"interface_hash":"cd1c59e462e3c7cc7c57d38574c61e1f063375ef748567a9213952963a69ee61","kind":"data","name":"G1","signature":{"abi":"0.8","kind":"data","size":16,"tier":"-"}}}

section functions
oracle @ref (x0:wire[3] in) (tgt:wire[1]) (fault:wire[4]) (m0:region[4,8] in) (a0:i64)
regs { w0:reg[64], w2:reg[32], r:reg[8], c0:reg[8], t0:reg[8], c1:reg[8], t1:reg[1], t2:reg[1] }
^entry():
w0 = lift.addr @m0
w2 = lift.zext.i32 x0
r = lift.call @L1 (w0, a0, w2)
c0 = lift.const.i8 1
t0 = lift.lshr r c0
c1 = lift.const.i8 0
t1 = lift.icmp.ne t0 c1
lift.faultif t1 4
t2 = lift.trunc.i1 r
lift.retval t2
lproc @L1 (a0:reg[64], a1:reg[64], a2:reg[32]) (r:reg[8]) () () ()
regs { c0:reg[64], v0:reg[64], v1:reg[8], v2:reg[32], v3:reg[64], c1:reg[64], v4:reg[64], c2:reg[64], v5:reg[64], v6:reg[1], c3:reg[64], v7:reg[64], c4:reg[32], v8:reg[64], c5:reg[64], v9:reg[1], c6:reg[8], v10:reg[8], c7:reg[8], v11:reg[8], v12:reg[64], c8:reg[64], c9:reg[64], t0:reg[64], v13:reg[64], v14:reg[64], c10:reg[64], t1:reg[1], c11:reg[64], t2:reg[1], v15:reg[8] }
^b0():
c0 = lift.const.i64 1
v0 = lift.add a0 c0
lift.boundscheck v0 1
v1 = lift.load.i8 v0
v2 = lift.zext.i32 v1
v3 = lift.zext.i64 v1
c1 = lift.const.i64 1
v4 = lift.shl v3 c1
c2 = lift.const.i64 2
v5 = lift.add v4 c2
v6 = lift.icmp.ult a1 v5
qbranch v6 ^b1 ^b2
^b1():
fault 4
^b2():
c3 = lift.const.i64 2
v7 = lift.add a0 c3
c4 = lift.const.i32 0
v8 = lift.call @L2 (v7, c4, v2, a2)
c5 = lift.const.i64 0
v9 = lift.icmp.eq v8 c5
qbranch v9 ^b3 ^b4
^b3():
c6 = lift.const.i8 0
lift.ret c6
^b4():
lift.boundscheck a0 1
v10 = lift.load.i8 a0
c7 = lift.const.i8 1
v11 = lift.and v10 c7
v12 = lift.zext.i64 v11
c8 = lift.addr @G1
c9 = lift.const.i64 8
t0 = lift.mul v12 c9
v13 = lift.add c8 t0
lift.boundscheck v13 8
v14 = lift.load.i64 v13
c10 = lift.const.i64 4198752
t1 = lift.icmp.eq v14 c10
qbranch t1 ^b4.q1c0 ^b4.s1
^b4.s1():
c11 = lift.const.i64 4198816
t2 = lift.icmp.eq v14 c11
qbranch t2 ^b4.q1c1 ^b4.q1d
^b4.q1c0():
v15 = lift.call @L3 (v8)
qjump ^b4.q1r
^b4.q1c1():
v15 = lift.call @L4 (v8)
qjump ^b4.q1r
^b4.q1d():
fault 4
^b4.q1r():
lift.ret v15
lproc @L2 (a0:reg[64], a1:reg[32], a2:reg[32], a3:reg[32]) (r:reg[64]) () () ()
regs { v0:reg[1], v1:reg[32], c0:reg[32], v2:reg[32], c1:reg[32], v3:reg[32], v4:reg[64], v5:reg[64], v6:reg[8], v7:reg[32], v8:reg[1], v9:reg[1], c2:reg[32], v10:reg[32], v11:reg[64], v12:reg[64], c3:reg[64] }
^b0():
v0 = lift.icmp.ule a2 a1
qbranch v0 ^b5 ^b1
^b1():
v1 = lift.add a1 a2
c0 = lift.const.i32 1
v2 = lift.lshr v1 c0
c1 = lift.const.i32 1
v3 = lift.shl v2 c1
v4 = lift.zext.i64 v3
v5 = lift.add a0 v4
lift.boundscheck v5 1
v6 = lift.load.i8 v5
v7 = lift.zext.i32 v6
v8 = lift.icmp.eq v7 a3
qbranch v8 ^b6 ^b2
^b2():
v9 = lift.icmp.ult v7 a3
qbranch v9 ^b3 ^b4
^b3():
c2 = lift.const.i32 1
v10 = lift.add v2 c2
v11 = lift.call @L2 (a0, v10, a2, a3)
lift.ret v11
^b4():
v12 = lift.call @L2 (a0, a1, v2, a3)
lift.ret v12
^b5():
c3 = lift.const.i64 0
lift.ret c3
^b6():
lift.ret v5
lproc @L3 (a0:reg[64]) (r:reg[8]) () () ()
regs { c0:reg[64], v0:reg[64], v1:reg[8], c1:reg[8], v2:reg[8], c2:reg[8], v3:reg[1], v4:reg[8] }
^b0():
c0 = lift.const.i64 1
v0 = lift.add a0 c0
lift.boundscheck v0 1
v1 = lift.load.i8 v0
c1 = lift.const.i8 1
v2 = lift.and v1 c1
c2 = lift.const.i8 0
v3 = lift.icmp.eq v2 c2
v4 = lift.zext.i8 v3
lift.ret v4
lproc @L4 (a0:reg[64]) (r:reg[8]) () () ()
regs { c0:reg[64], v0:reg[64], v1:reg[8], c1:reg[8], v2:reg[1], v3:reg[8] }
^b0():
c0 = lift.const.i64 1
v0 = lift.add a0 c0
lift.boundscheck v0 1
v1 = lift.load.i8 v0
c1 = lift.const.i8 100
v2 = lift.icmp.ule c1 v1
v3 = lift.zext.i8 v2
lift.ret v3

section data
G1 6011400000000000a011400000000000

section layout
{"A_tab":1,"H":14,"S_cells":10,"globals":{"G1":{"base":4096,"image":"G1","size":16}},"heap_base":8192,"heap_limit_max":0,"interface_regions":{"ref":{"m0":{"base":8192}}},"null_size":4096,"ptr_width":64}
```

```text hash=rung4-mini
ref 15c371b8e02e1bef6e9fa5220a8b128e1547fe2cf192e68a1045b3bebfeb0800
L1 72b9a373406320f3ff6cb69c9edce3a4d8e1ae7a7433d88286844ab68dc4db81
L2 960dd380906f87a9154040ce51d207892a46574897dc749e72c31241bfe0517f
L3 102ebe211e15cbb57f2ff0ce761197291d2e046c46e56d205939b4444660d3e6
L4 ae731d00bf437af71b684013b35ab29dcd6a4ee5ef8c974abe32d7116c89ba37
G1 cd1c59e462e3c7cc7c57d38574c61e1f063375ef748567a9213952963a69ee61
```

The image of the runs below has 7 records with keys 0, 1, 3, 4, 5, 6, 7 (key 2 is absent) and
values 10, 101, 7, 200, 42, 99, 150; its byte 0 selects `pred_even` (value even) or `pred_big`
(value ≥ 100):

```text run=rung4-mini
input=0 mem=m0:0007000a0165030704c8052a06630796 arg=16 budget=400,0,512,8 -> code=0 payload=1 steps=107
input=1 mem=m0:0007000a0165030704c8052a06630796 arg=16 budget=400,0,512,8 -> code=0 payload=0 steps=89
input=2 mem=m0:0007000a0165030704c8052a06630796 arg=16 budget=400,0,512,8 -> code=0 payload=0 steps=91
input=3 mem=m0:0007000a0165030704c8052a06630796 arg=16 budget=400,0,512,8 -> code=0 payload=0 steps=109
input=4 mem=m0:0007000a0165030704c8052a06630796 arg=16 budget=400,0,512,8 -> code=0 payload=1 steps=71
input=5 mem=m0:0007000a0165030704c8052a06630796 arg=16 budget=400,0,512,8 -> code=0 payload=1 steps=109
input=6 mem=m0:0007000a0165030704c8052a06630796 arg=16 budget=400,0,512,8 -> code=0 payload=0 steps=91
input=7 mem=m0:0007000a0165030704c8052a06630796 arg=16 budget=400,0,512,8 -> code=0 payload=1 steps=111
input=0 mem=m0:0107000a0165030704c8052a06630796 arg=16 budget=400,0,512,8 -> code=0 payload=0 steps=108
input=1 mem=m0:0107000a0165030704c8052a06630796 arg=16 budget=400,0,512,8 -> code=0 payload=1 steps=90
input=4 mem=m0:0107000a0165030704c8052a06630796 arg=16 budget=400,0,512,8 -> code=0 payload=1 steps=72
input=7 mem=m0:0107000a0165030704c8052a06630796 arg=16 budget=400,0,512,8 -> code=0 payload=1 steps=112
input=0 mem=m0:0007000a0165030704c8052a06630796 arg=15 budget=400,0,512,8 -> code=4 payload=0 steps=16
input=4 mem=m0:0007000a0165030704c8052a06630796 arg=16 budget=70,0,512,8 -> code=1 payload=0 steps=70
input=4 mem=m0:0007000a0165030704c8052a06630796 arg=16 budget=71,0,512,8 -> code=0 payload=1 steps=71
input=7 mem=m0:0007000a0165030704c8052a06630796 arg=16 budget=400,0,125,8 -> code=3 payload=0 steps=92
input=7 mem=m0:0007000a0165030704c8052a06630796 arg=16 budget=400,0,126,8 -> code=0 payload=1 steps=111
input=7 mem=m0:0007000a0165030704c8052a06630796 arg=16 budget=400,0,512,3 -> code=3 payload=0 steps=57
```

```text step-check=rung4-mini
mem=m0:0007000a0165030704c8052a06630796 arg=16 budget=120,0,512,8 -> status=ok cases=8 input_and_memory_bits=3 fixed_regions=m0
```

```text native=rung4-mini
q(img with byte 0 = 0, 16, rowid) for rowid 0..7 = 1 0 0 0 1 1 0 1
q(img with byte 0 = 1, 16, rowid) for rowid 0..7 = 0 1 0 0 1 0 0 1
q(img, 15, 0) = __bennett_nz_fault(4)
```

*(non-normative)* Derivation of the 71 steps of rowid 4: `@ref` 3 rows to the call; `@L1`
`^b0` 12 rows; `^b2` 4 rows to the call of `@L2`; `@L2` 15 rows (lo = 0, hi = 7, mid = 3: record
3 at offset 2 + 6 has key 4, found at once); `@L1` 3 more rows of `^b2` and 14 of `^b4` to the
`qbranch`; the leaf's `lift.call` (1), `@L3`'s 10 rows, `qjump` (1), `lift.ret` (1); `@ref`'s 7
delivery rows: 3 + 12 + 4 + 15 + 3 + 14 + 1 + 10 + 1 + 1 + 7 = 71, and B = 70 is
`FAULT_BUDGET_STEPS`. Rowid 7 recurses three times (mid 3, then 5 in [4, 7), then 6 in [6, 7)):
the stack holds R_L1 = 3 + 35 = 38 cells, three R_L2 = 3 + 22 = 25 frames and R_L3 = 13, 126
cells in all, and the depth reaches 4, so 125 cells or depth 3 give `FAULT_BUDGET_DEPTH`. The
step check runs the reversible machine for B = 120 on all 8 rowids with this image fixed and
reverses every step to the entry tuple. The certificate claim of NS §8 rung 4(a) is this check
over all rows and all target values with the database fixed classically (§25.2 records how ISA
§12.2 labels a domain with a fixed region).

### 16.8 Example: a reduced rung 8 (ENTROPY binding)

NS §8 rung 8: "the entropy device is replaced by a superposed register". A Monte Carlo trial
reads one random byte through the entropy device and succeeds when it is below 77. The region
function has no parameters; the descriptor has one ENTROPY binding of 8 wires (one byte,
region[0,8]) and a 1-wire target. In L the effect marker is the runtimes function
`__bennett_dev_entropy_read` over the device state (§11.3), shown here with the runtimes' code
(a byte loop):

```llvm lift=rung8-mini region=@mc desc=dev=ENTROPY(0);tgt=1
@buf = internal global i8 0
@__bennett_dev_entropy_base = internal global ptr null
@__bennett_dev_entropy_size = internal global i64 0
@__bennett_dev_entropy_pos = internal global i64 0

define internal i8 @mc() {
  call void @__bennett_dev_entropy_read(ptr @buf, i64 1)
  %b = load i8, ptr @buf
  %c = icmp ult i8 %b, 77
  %r = zext i1 %c to i8
  ret i8 %r
}

define internal void @__bennett_dev_entropy_read(ptr %p, i64 %len) {
b0:
  %size = load i64, ptr @__bennett_dev_entropy_size
  %pos = load i64, ptr @__bennett_dev_entropy_pos
  %left = sub i64 %size, %pos
  %bad = icmp ugt i64 %len, %left
  br i1 %bad, label %b1, label %b2

b1:
  call void @__bennett_nz_fault(i64 10)
  unreachable

b2:
  %base = load ptr, ptr @__bennett_dev_entropy_base
  %src = getelementptr i8, ptr %base, i64 %pos
  br label %b3

b3:
  %i = phi i64 [ 0, %b2 ], [ %i2, %b4 ]
  %done = icmp eq i64 %i, %len
  br i1 %done, label %b5, label %b4

b4:
  %sp = getelementptr i8, ptr %src, i64 %i
  %v = load i8, ptr %sp
  %dp = getelementptr i8, ptr %p, i64 %i
  store i8 %v, ptr %dp
  %i2 = add i64 %i, 1
  br label %b3

b5:
  %pos2 = add i64 %pos, %len
  store i64 %pos2, ptr @__bennett_dev_entropy_pos
  ret void
}
```

```text linkmap=rung8-mini
null_size=4096 heap_base=8192 heap_limit_max=0
global @buf -> G1 base=4096 size=1
global @__bennett_dev_entropy_base -> G2 base=4104 size=8
global @__bennett_dev_entropy_size -> G3 base=4112 size=8
global @__bennett_dev_entropy_pos -> G4 base=4120 size=8
budget-table: largest stack 512, largest heap 0
```

The layout: four globals and one region, P = 5, A_tab = 3; e0 at 8192; H = 14; S_cells = 9. The
prologue stores the region base and its size 2^0 = 1 into the device state (G2, G3); the
position G4 starts at its image 0:

```isa object=rung8-mini
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=64

section symbols
{"0":{"interface_hash":"9513f98fe923cc96f338736dba1f2ce66150b0ad479b708a8339d648264cfa44","kind":"oracle","name":"ref","signature":{"abi":"0.8","args":[],"fault":4,"in":[],"kind":"oracle","mem":[{"A":0,"W":8,"role":"in"}],"tgt":1,"tier":"q"}},"1":{"interface_hash":"9693c26332743afbabc98e27c52354a62c784770867c31704f859a862f608ce6","kind":"lproc","name":"L1","signature":{"abi":"0.8","kind":"lproc","params":[],"result":8,"tier":"q"}},"2":{"interface_hash":"430d12d36def3a829ce790134f9d0475cc2deaf5af6400cc2c3a9d7e4c52d7e0","kind":"lproc","name":"L2","signature":{"abi":"0.8","kind":"lproc","params":[64,64],"result":1,"tier":"q"}},"3":{"interface_hash":"b50c81820686bbeffee04bef717194a246cce129dfe075cd83f7236bf6b9e02d","kind":"data","name":"G1","signature":{"abi":"0.8","kind":"data","size":1,"tier":"-"}},"4":{"interface_hash":"152c175d592378069aaf67055e1d0ae1481a51cebce1e9f4f5d2b239ef7a253e","kind":"data","name":"G2","signature":{"abi":"0.8","kind":"data","size":8,"tier":"-"}},"5":{"interface_hash":"9d3aca04351c878d6876df5bd35776f57012ffe2e47eee3cec4c6105684a9550","kind":"data","name":"G3","signature":{"abi":"0.8","kind":"data","size":8,"tier":"-"}},"6":{"interface_hash":"3879e146fc0259de6e55b6419ae04d56e91a94d01e7ac18d36b9aee8bf2ecbe5","kind":"data","name":"G4","signature":{"abi":"0.8","kind":"data","size":8,"tier":"-"}}}

section functions
oracle @ref () (tgt:wire[1]) (fault:wire[4]) (e0:region[0,8] in) ()
regs { d0:reg[64], d1:reg[64], d2:reg[64], d3:reg[64], r:reg[8], c0:reg[8], t0:reg[8], c1:reg[8], t1:reg[1], t2:reg[1] }
^entry():
d0 = lift.addr @e0
d1 = lift.addr @G2
lift.boundscheck d1 8
lift.store.i64 d1 d0
d2 = lift.const.i64 1
d3 = lift.addr @G3
lift.boundscheck d3 8
lift.store.i64 d3 d2
r = lift.call @L1 ()
c0 = lift.const.i8 1
t0 = lift.lshr r c0
c1 = lift.const.i8 0
t1 = lift.icmp.ne t0 c1
lift.faultif t1 4
t2 = lift.trunc.i1 r
lift.retval t2
lproc @L1 () (r:reg[8]) () () ()
regs { c0:reg[64], c1:reg[64], t0:reg[1], c2:reg[64], v0:reg[8], c3:reg[8], v1:reg[1], v2:reg[8] }
^b0():
c0 = lift.addr @G1
c1 = lift.const.i64 1
t0 = lift.call @L2 (c0, c1)
c2 = lift.addr @G1
lift.boundscheck c2 1
v0 = lift.load.i8 c2
c3 = lift.const.i8 77
v1 = lift.icmp.ult v0 c3
v2 = lift.zext.i8 v1
lift.ret v2
lproc @L2 (a0:reg[64], a1:reg[64]) (r:reg[1]) () () ()
regs { c0:reg[64], v0:reg[64], c1:reg[64], v1:reg[64], v2:reg[64], v3:reg[1], c2:reg[64], v4:reg[64], v5:reg[64], c3:reg[64], v6:reg[64], v7:reg[1], v8:reg[64], v9:reg[8], v10:reg[64], c4:reg[64], v11:reg[64], v12:reg[64], c5:reg[64] }
^b0():
c0 = lift.addr @G3
lift.boundscheck c0 8
v0 = lift.load.i64 c0
c1 = lift.addr @G4
lift.boundscheck c1 8
v1 = lift.load.i64 c1
v2 = lift.sub v0 v1
v3 = lift.icmp.ult v2 a1
qbranch v3 ^b1 ^b2
^b1():
fault 10
^b2():
c2 = lift.addr @G2
lift.boundscheck c2 8
v4 = lift.load.i64 c2
v5 = lift.add v4 v1
c3 = lift.const.i64 0
(v6) = lift.parmov (c3)
qjump ^b3
^b3():
v7 = lift.icmp.eq v6 a1
qbranch v7 ^b5 ^b4
^b4():
v8 = lift.add v5 v6
lift.boundscheck v8 1
v9 = lift.load.i8 v8
v10 = lift.add a0 v6
lift.boundscheck v10 1
lift.store.i8 v10 v9
c4 = lift.const.i64 1
v11 = lift.add v6 c4
(v6) = lift.parmov (v11)
qjump ^b3
^b5():
v12 = lift.add v1 a1
c5 = lift.addr @G4
lift.boundscheck c5 8
lift.store.i64 c5 v12
lift.ret r

section data
G1 00
G2 0000000000000000
G3 0000000000000000
G4 0000000000000000

section layout
{"A_tab":3,"H":14,"S_cells":9,"globals":{"G1":{"base":4096,"image":"G1","size":1},"G2":{"base":4104,"image":"G2","size":8},"G3":{"base":4112,"image":"G3","size":8},"G4":{"base":4120,"image":"G4","size":8}},"heap_base":8192,"heap_limit_max":0,"interface_regions":{"ref":{"e0":{"base":8192}}},"null_size":4096,"ptr_width":64}
```

```text run=rung8-mini
input= mem=e0:00 budget=100,0,512,4 -> code=0 payload=1 steps=61
input= mem=e0:4c budget=100,0,512,4 -> code=0 payload=1 steps=61
input= mem=e0:4d budget=100,0,512,4 -> code=0 payload=0 steps=61
input= mem=e0:ff budget=100,0,512,4 -> code=0 payload=0 steps=61
```

```text step-check=rung8-mini
budget=100,0,512,4 -> status=ok cases=256 input_and_memory_bits=8
```

*(non-normative)* 0x4c = 76 < 77 and 0x4d = 77 is not, so the payload is 1 on exactly 77 of the
256 entropy values (checked by running all 256): amplitude estimation on this oracle estimates
77/256. The step check enumerates the superposed entropy byte itself.

### 16.9 Example: rung 2 (heap, phis, a loop, `free`)

A linked list of n nodes built with `malloc` (the runtimes allocator over `lift.alloc`, shown with
its code), summed and freed. n comes from a 2-wire `IN` register zero-extended to `i8`:

```llvm lift=listsum region=@listsum desc=IN(2,zext);tgt=8
define ptr @malloc(i64 %n) {
  %p = call ptr @__bennett_nz_alloc(i64 %n)
  ret ptr %p
}

define void @free(ptr %p) {
  %z = icmp eq ptr %p, null
  br i1 %z, label %out, label %rel

rel:
  call void @__bennett_nz_free(ptr %p)
  br label %out

out:
  ret void
}

define internal i8 @listsum(i8 %n) {
b0:
  %z = icmp eq i8 %n, 0
  br i1 %z, label %b3, label %b1

b1:
  %i = phi i8 [ 0, %b0 ], [ %i2, %b1 ]
  %head = phi ptr [ null, %b0 ], [ %node, %b1 ]
  %node = call ptr @malloc(i64 16)
  store i8 %i, ptr %node
  %np = getelementptr i8, ptr %node, i64 8
  store ptr %head, ptr %np
  %i2 = add i8 %i, 1
  %more = icmp ult i8 %i2, %n
  br i1 %more, label %b1, label %b2

b2:
  %p = phi ptr [ %node, %b1 ], [ %next, %b2 ]
  %s = phi i8 [ 0, %b1 ], [ %s2, %b2 ]
  %v = load i8, ptr %p
  %s2 = add i8 %s, %v
  %nextp = getelementptr i8, ptr %p, i64 8
  %next = load ptr, ptr %nextp
  call void @free(ptr %p)
  %end = icmp eq ptr %next, null
  br i1 %end, label %b4, label %b2

b3:
  ret i8 0

b4:
  ret i8 %s2
}
```

```text linkmap=listsum
null_size=4096 heap_base=4096 heap_limit_max=64 globals=none budget-table: largest stack 512, largest heap 64
```

A_tab = 6 (2^6 ≥ 0 + 64), H = 13 (4096 + 64 ≤ 2^13), S_cells = 9:

```isa object=listsum
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=64

section symbols
{"0":{"interface_hash":"066b70a9674347f05fd4d6e727760e63fd94aa0e52ac5b457f5ea27597856a35","kind":"oracle","name":"ref","signature":{"abi":"0.8","args":[],"fault":4,"in":[2],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"1":{"interface_hash":"5240453f456b06a3dad9264c52ccdb442072398e4f48dd13ffdf9198eff14ef0","kind":"lproc","name":"L1","signature":{"abi":"0.8","kind":"lproc","params":[8],"result":8,"tier":"q"}},"2":{"interface_hash":"46b439e82f9ccea0da6ae6039e312761f884af01c09b902df20fb995f33e4c4e","kind":"lproc","name":"L2","signature":{"abi":"0.8","kind":"lproc","params":[64],"result":64,"tier":"q"}},"3":{"interface_hash":"0a525e87fd5d98e7137d23335c09d9a5a9fcf52047743ca3e0c08bf6af7ddb72","kind":"lproc","name":"L3","signature":{"abi":"0.8","kind":"lproc","params":[64],"result":1,"tier":"q"}}}

section functions
oracle @ref (x0:wire[2] in) (tgt:wire[8]) (fault:wire[4]) () ()
regs { w0:reg[8], r:reg[8] }
^entry():
w0 = lift.zext.i8 x0
r = lift.call @L1 (w0)
lift.retval r
lproc @L1 (a0:reg[8]) (r:reg[8]) () () ()
regs { c0:reg[8], v0:reg[1], c1:reg[8], c2:reg[64], v1:reg[8], v2:reg[64], c3:reg[64], v3:reg[64], c4:reg[64], v4:reg[64], c5:reg[8], v5:reg[8], v6:reg[1], c6:reg[8], v7:reg[64], v8:reg[8], v9:reg[8], v10:reg[8], c7:reg[64], v11:reg[64], v12:reg[64], t0:reg[1], c8:reg[64], v13:reg[1], c9:reg[8] }
^b0():
c0 = lift.const.i8 0
v0 = lift.icmp.eq a0 c0
qbranch v0 ^b3 ^b0.e1
^b0.e1():
c1 = lift.const.i8 0
c2 = lift.const.i64 0
(v1, v2) = lift.parmov (c1, c2)
qjump ^b1
^b1():
c3 = lift.const.i64 16
v3 = lift.call @L2 (c3)
lift.boundscheck v3 1
lift.store.i8 v3 v1
c4 = lift.const.i64 8
v4 = lift.add v3 c4
lift.boundscheck v4 8
lift.store.i64 v4 v2
c5 = lift.const.i8 1
v5 = lift.add v1 c5
v6 = lift.icmp.ult v5 a0
qbranch v6 ^b1.e1 ^b1.e2
^b1.e1():
(v1, v2) = lift.parmov (v5, v3)
qjump ^b1
^b1.e2():
c6 = lift.const.i8 0
(v7, v8) = lift.parmov (v3, c6)
qjump ^b2
^b2():
lift.boundscheck v7 1
v9 = lift.load.i8 v7
v10 = lift.add v8 v9
c7 = lift.const.i64 8
v11 = lift.add v7 c7
lift.boundscheck v11 8
v12 = lift.load.i64 v11
t0 = lift.call @L3 (v7)
c8 = lift.const.i64 0
v13 = lift.icmp.eq v12 c8
qbranch v13 ^b4 ^b2.e2
^b2.e2():
(v7, v8) = lift.parmov (v12, v10)
qjump ^b2
^b3():
c9 = lift.const.i8 0
lift.ret c9
^b4():
lift.ret v10
lproc @L2 (a0:reg[64]) (r:reg[64]) () () ()
regs { v0:reg[64] }
^b0():
v0 = lift.alloc a0
lift.ret v0
lproc @L3 (a0:reg[64]) (r:reg[1]) () () ()
regs { c0:reg[64], v0:reg[1] }
^b0():
c0 = lift.const.i64 0
v0 = lift.icmp.eq a0 c0
qbranch v0 ^b2 ^b1
^b1():
lift.free a0
qjump ^b2
^b2():
lift.ret r

section layout
{"A_tab":6,"H":13,"S_cells":9,"globals":{},"heap_base":4096,"heap_limit_max":64,"interface_regions":{"ref":{}},"null_size":4096,"ptr_width":64}
```

```text run=listsum
input=0 budget=1000,64,512,4 -> code=0 payload=0 steps=8
input=1 budget=1000,64,512,4 -> code=0 payload=0 steps=45
input=2 budget=1000,64,512,4 -> code=0 payload=1 steps=80
input=3 budget=1000,64,512,4 -> code=0 payload=3 steps=115
input=2 budget=1000,32,512,4 -> code=0 payload=1 steps=80
input=3 budget=1000,32,512,4 -> code=2 payload=0 steps=44
```

```text step-check=listsum
budget=200,64,512,4 -> status=ok cases=4 input_and_memory_bits=2
```

*(non-normative)* The payload is 0 + 1 + … + (n − 1). n = 3 allocates 3 × 16 bytes: with a heap
budget of 32 the third `lift.alloc` (`heap_used` 32 + 16 > 32) is `FAULT_BUDGET_HEAP` (2). The 45
steps of n = 1: `@ref` 2 rows to the call; `^b0` 3; `^b0.e1` 4; `^b1` 14 (including `@L2`'s 2);
`^b1.e2` 3; `^b2` 17 (including `@L3`'s 6); `^b4` 1; `lift.retval` 1.

### 16.10 Example: `switch` as a compare tree

Five cases, two of them sharing a successor, and a default with a phi (outline E6; 0.1's linear
chain is replaced). Sorted keys 1, 5, 9, 20, 40: the root compares with key 2 (mid = ⌊(0 + 4)/2⌋ =
2, the key 9) by `ult`; the left node [1, 5] is an `eq` chain in `^b0.s1` and `^b0.s3`, the right
node [9, 20, 40] in `^b0.s2`, `^b0.s4`, `^b0.s5` (creation order: L and R of the root first, then
each node's chain); the default reaches the phi through the edge block `^b0.e4`:

```llvm lift=switch5 region=@sw desc=IN(8,zext);tgt=8
define internal i8 @sw(i8 %x) {
b0:
  switch i8 %x, label %b4 [
    i8 1, label %b1
    i8 5, label %b2
    i8 9, label %b3
    i8 20, label %b1
    i8 40, label %b2
  ]

b1:
  br label %b4

b2:
  br label %b4

b3:
  br label %b4

b4:
  %r = phi i8 [ 7, %b0 ], [ 10, %b1 ], [ 20, %b2 ], [ 30, %b3 ]
  ret i8 %r
}
```

```text linkmap=switch5
null_size=4096 heap_base=4096 heap_limit_max=0 globals=none budget-table: largest stack 32, largest heap 0
```

```isa object=switch5
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=64

section symbols
{"0":{"interface_hash":"0575354a0ecceee58d8dfbcc5cb9a9b8851c5c2b3193bf543395bed13604ce80","kind":"oracle","name":"ref","signature":{"abi":"0.8","args":[],"fault":4,"in":[8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"1":{"interface_hash":"84e502d9807b1947e93d4314fab40f65bcb2a3f42735daa08cd05c8cd15ccf2c","kind":"lproc","name":"L1","signature":{"abi":"0.8","kind":"lproc","params":[8],"result":8,"tier":"q"}}}

section functions
oracle @ref (x0:wire[8] in) (tgt:wire[8]) (fault:wire[4]) () ()
regs { r:reg[8] }
^entry():
r = lift.call @L1 (x0)
lift.retval r
lproc @L1 (a0:reg[8]) (r:reg[8]) () () ()
regs { c0:reg[8], t0:reg[1], c1:reg[8], t1:reg[1], c2:reg[8], t2:reg[1], c3:reg[8], t3:reg[1], c4:reg[8], t4:reg[1], c5:reg[8], t5:reg[1], c6:reg[8], v0:reg[8], c7:reg[8], c8:reg[8], c9:reg[8] }
^b0():
c0 = lift.const.i8 9
t0 = lift.icmp.ult a0 c0
qbranch t0 ^b0.s1 ^b0.s2
^b0.s1():
c1 = lift.const.i8 1
t1 = lift.icmp.eq a0 c1
qbranch t1 ^b1 ^b0.s3
^b0.s2():
c2 = lift.const.i8 9
t2 = lift.icmp.eq a0 c2
qbranch t2 ^b3 ^b0.s4
^b0.s3():
c3 = lift.const.i8 5
t3 = lift.icmp.eq a0 c3
qbranch t3 ^b2 ^b0.e4
^b0.s4():
c4 = lift.const.i8 20
t4 = lift.icmp.eq a0 c4
qbranch t4 ^b1 ^b0.s5
^b0.s5():
c5 = lift.const.i8 40
t5 = lift.icmp.eq a0 c5
qbranch t5 ^b2 ^b0.e4
^b0.e4():
c6 = lift.const.i8 7
(v0) = lift.parmov (c6)
qjump ^b4
^b1():
c7 = lift.const.i8 10
(v0) = lift.parmov (c7)
qjump ^b4
^b2():
c8 = lift.const.i8 20
(v0) = lift.parmov (c8)
qjump ^b4
^b3():
c9 = lift.const.i8 30
(v0) = lift.parmov (c9)
qjump ^b4
^b4():
lift.ret v0

section layout
{"A_tab":0,"H":12,"S_cells":5,"globals":{},"heap_base":4096,"heap_limit_max":0,"interface_regions":{"ref":{}},"null_size":4096,"ptr_width":64}
```

```text run=switch5
input=0 budget=100,0,32,1 -> code=0 payload=7 steps=15
input=1 budget=100,0,32,1 -> code=0 payload=10 steps=12
input=5 budget=100,0,32,1 -> code=0 payload=20 steps=15
input=9 budget=100,0,32,1 -> code=0 payload=30 steps=12
input=20 budget=100,0,32,1 -> code=0 payload=10 steps=15
input=40 budget=100,0,32,1 -> code=0 payload=20 steps=18
input=41 budget=100,0,32,1 -> code=0 payload=7 steps=18
input=40 budget=17,0,32,1 -> code=1 payload=0 steps=17
```

```text step-check=switch5
budget=18,0,32,1 -> status=ok cases=256 input_and_memory_bits=8
```

*(non-normative)* x = 1 takes `lift.call` (1), `^b0` (3), `^b0.s1` (3), `^b1` (3), `lift.ret` (1)
and `lift.retval` (1): 12 steps; x = 40 visits `^b0`, `^b0.s2`, `^b0.s4`, `^b0.s5` and `^b2`:
1 + 3 + 3 + 3 + 3 + 3 + 1 + 1 = 18, the most, so B = 18 suffices for all 256 inputs. The 0.1
linear chain needed up to 5 compares; the tree needs at most 4 on this table (the `ult` at the
root and up to 3 `eq`), and O(log k) for k cases.

## 17. Device classical code: memory model, lowering, faults

### 17.1 Memory model

There is one classical memory, shared by H, CC, R and the entry state of every L invocation
(§8.5; NS §3.2):

- **Live allocations**: a shadow-stack frame from its push to its pop (§17.3); a global, always;
  a heap allocation of the runtimes allocator from its allocation to its `free` (`free` of a null
  pointer does nothing). The null region is never allocated.
- **Zero fill**: shadow-stack frames and heap allocations are zero-filled in both builds; globals
  hold their initialisers. Region inputs are not zero-filled: they are the bytes the host
  supplies (NS §3.2).
- **Bounds**: a load, store or memory-function range is valid iff all its bytes lie in one live
  allocation (an address model: the object a pointer was derived from is irrelevant; NS §3.2
  "faulting memory access is defined").
- **Addresses**: the comparison link (§19.5) places globals and functions; the runtimes
  allocator's fixed base places the heap; the shadow stack is heap memory, so native stack
  addresses never reach device results. The residue is host-stack addresses passed in by host
  code: executions in which they influence a result are *layout-dependent* (NS §3.2; §24 D12),
  validated against the reference interpreter.
- **Single thread**: atomics and volatile are sequentialised (N9; NS §3.2; §24 D24).

### 17.2 Layout

The device `layout` (ISA §9.1) replicates the comparison link (§19.5). CC and R code use ISA §7.1
memory; L code uses ISA §7.2 memory with the same `heap_base` and global bases, so addresses are
equal in every tier.

### 17.3 Shadow stack (N24)

NS §3.2: "Region allocas are rewritten by the normaliser onto a shim-managed shadow stack in both
builds where possible"; in device variants it is always possible. The runtimes provide, with
these contracts:

| Entry point | Contract |
|---|---|
| `void __bennett_rt_ss_init(i64 size)` | allocates the shadow stack, a heap block of `size` bytes (`sstack`, §9.2), by `__bennett_nz_alloc`; called by the oracle wrapper prologue (§16.2), the R entry stub and the CC entry stub when their closure uses the shadow stack |
| `ptr __bennett_rt_ss_push(i64 size, i64 align)` | pushes a frame of `size` bytes aligned to `align` and returns its base; the frame is zero-filled; overflow of the block is `__bennett_nz_fault(2)` (`FAULT_BUDGET_HEAP`) |
| `void __bennett_rt_ss_pop(ptr fp)` | pops the frame fp and every frame pushed after it |
| `ptr __bennett_rt_ss_alloca(i64 n, i64 align)` | a zero-filled dynamic allocation in the current frame, released by its pop |
| `ptr __bennett_rt_ss_save()`, `void __bennett_rt_ss_restore(ptr)` | `llvm.stacksave`/`llvm.stackrestore` |

N24 rewrites each function with allocas: `%nz.fp.<f> = call ptr @__bennett_rt_ss_push(i64 S,
i64 A)` at entry, where the static allocas of the entry block are laid out in instruction order,
each at the next offset aligned to its alignment, S is the total rounded up to A, the largest
alignment; each static alloca becomes `getelementptr i8, ptr %nz.fp.<f>, i64 <offset>` with the
alloca's name; every other alloca becomes `__bennett_rt_ss_alloca`; `call void
@__bennett_rt_ss_pop(ptr %nz.fp.<f>)` precedes every `ret` (including the early returns of
§14.4). `llvm.frameaddress(0)`, `llvm.sponentry`, `llvm.addressofreturnaddress`,
`llvm.swift.async.context.addr` and `llvm.eh.dwarf.cfa` give `%nz.fp.<f>`;
`llvm.frameaddress(n > 0)` and `llvm.returnaddress` give null (LangRef: "zero if it cannot be
identified"); `llvm.stackaddress` gives the current shadow-stack pointer; `llvm.localescape`
records the escaped allocas' offsets in a per-function table that `llvm.localrecover` reads with
the parent's frame address; `llvm.structured.alloca` is an alloca.

### 17.4 CC and R lowering

The lowering of device CC and R variants to ISA CC and R (ISA §4.1) is plugin-defined and
constrained by §18.7, with these dialect rules: LLVM integer and memory instructions map to the
ISA instructions of the same name (phis to block parameters, ISA §3.4); the primitives to `alloc`,
`free` and §11.5; multi-result calls carry aggregates; marker calls lower to the region calls
and `qreg.*` instructions of §18.3 with the handle register environment of §6.5; dispatch uses
the compare trees of §14.2; host calls are §11.4; effect markers §11.1. In R, every executed
instruction is one frame of the R history (ISA §7.4).

### 17.5 Fault outcomes

| Event | Fault code (ISA §5.4) |
|---|---|
| `udiv`, `urem`, `sdiv`, `srem` with divisor 0 | 5 `FAULT_UB_DIV0` |
| `sdiv`, `srem` of the minimum value by −1 | 6 `FAULT_UB_SDIV_OVERFLOW` |
| an access outside every live allocation; `free` of a non-null pointer that is not the base of a live heap allocation | 7 `FAULT_UB_MEMFAULT` |
| `unreachable` reached; N11; an indirect call or `indirectbr` matching no candidate (§14.2, §14.9); unwinding out of a region (§14.4); a descriptor shape mismatch (`T-IFACE`); `T-TAINT-HOST`; every other run-time check of §18.3 | 4 `FAULT_UB_TRAP` |
| `__bennett_nz_fault(C)` | C |
| steps budget exhausted | 1 `FAULT_BUDGET_STEPS` |
| heap budget or shadow stack exhausted | 2 `FAULT_BUDGET_HEAP` |
| depth or lifted stack budget exhausted | 3 `FAULT_BUDGET_DEPTH` |
| a trapped call, an unmodelled or unbound device, an effect in an action region | 8 `FAULT_EFFECT_UNMODELLED` |
| entropy exhausted (ISA §7.3; §11.3) | 10 `FAULT_ENTROPY_EXHAUSTED` |
| a blocker point (§25.1) | 4, with the blocker report |

In an oracle region a fault is the F_B outcome (ISA §5.2). In an action region it is TDL-8's. In
other device code the run ends `FAILED` with that fault record (ISA §10); CC reports the code by
§11.5; for R code the record is an R fault record (ISA §7.4; ISA-7, ISA-8 in §25.2).

### 17.6 The R tier

- The R lowering inserts a **step counter**: one step per executed materialised LLVM instruction
  other than `phi`, debug intrinsics and the N34 marks, counted at the marks of N34 (function
  entries and loop latches) by the number of instructions of the blocks executed since the
  previous mark. Heap bytes are counted by the allocator, depth at function entry. These define
  the R budget unit on the materialised module, independent of the plugin (outline B5).
- Exhaustion of the R budget (§9.3) is `__bennett_nz_fault(1)`, `(2)` or `(3)`, lowered to `trap`
  (§11.5), and the run ends `FAILED`.
- R faults end the run (ISA §4.1); §25.2 records ISA-8 (fault status to the CC caller,
  reverse-eligibility of faulted runs).

### 17.7 The native comparison build

Differential testing (NS §5.1) compares the artefact with the **native comparison binary**: the
materialised device variants, code-generated by the same LLVM major and linked with
`bennett-runtimes` and `bennett-arith` (never host libc or libm) under the comparison link of
§19.5. It is never an `-O0` build: optimisation legally changes marker operands (spike F4), and
the materialised optimised module is the one program both builds implement. The driver MUST make
division by zero and INT_MIN/−1 trap in the native build: on targets whose divide instruction does
not trap it inserts, after materialisation and outside the materialised module, a check that
calls `__bennett_nz_fault` with code 5 or 6. Results compare by the outcome table of §18.7.

## 18. Reference semantics

### 18.1 State

The reference semantics runs H functions natively and every device entry, region invocation and
whole-program entry on the materialised module over a state Σ = (C, Q, H, G, K, T):

- **C**, the classical state: LLVM's semantics of the materialised module (LangRef), with every
  remaining choice fixed by §12–§14 and the fault outcomes of §17.5; it includes the shadows of
  the arena (TDL-4);
- **Q**, the quantum state of the ISA formal model (ISA §14.2): a unit vector over the live wires
  in allocation order, including the arena's wires (TDL-4);
- **H**, the handle table: for each handle, its wires, whether it is live, and the
  generation it was allocated in, if any;
- **G**, a stack of **recorders**, one per active generation (§18.4);
- **K**, the coherence states of the object instances (TDL-2);
- **T**, the device-model states and the effect tape (§11).

Measurement and `observe` make the semantics a tree: every outcome sequence has its Born
probability (ISA §14.2) and its own continuation.

### 18.2 Events

A marker call or a TDL store produces **events**: ISA-level operations, each with a **control
set** (a set of wires, initially empty). The forms are:

- `qalloc H n`, `qfree H`; the gates `x h s sdg t tdg cx cz swap ccx` (ISA §4.4) and `rx θ`,
  `ry θ`, `rz θ` on wires; `qload D M A`, `qstore M A V`, `qprep H bytes`;
- `oracle R B (ins..) tgt fault (mem..) (args..)` and `wide R …` (§8.6), `inplace G G′ B X`;
- the TDL events of §10: `slice O (args..) (ins..) (mem..) -> regs`, `xmask X+o m`, `xstore X+a
  m`, `perm P X+a (params..)`, `xchg X+a h`, `fault C` (TDL-12), `firstfault (f..) Φ`;
- `observe X+o len`, `measure` (outside generations), `effect dev.op` (R).

When no recorder is active, an event is **applied** to Σ at once; otherwise it is appended to the
innermost recorder. Applying an event with control set S applies it only on the basis states where
every wire of S is 1 (ISA `ctl`, ISA §4.7, §5.3); `qalloc` and `qfree` are unconditional (ISA
§3.5). Applying an event that writes object X: when K(X) = Cl and S ≠ ∅ or the written value is
Co, X is first materialised (TDL-2); after an application with S ≠ ∅ or a Co value, K(X) = Co.
The plugin realises applied events as CC-level region calls in event order (ISA §4.7), whose
temporaries are released by `qreg.free` with the dynamic cleanliness check of ISA §3.3; it MAY
compile an event list into one ISA action when that action satisfies ISA §6.

**Adjoint** of an event list (ISA §5.3 adjoint table): reverse the list and replace each event:
`x h cx cz swap ccx qload qstore qprep oracle wide slice xmask xstore xchg` are self-adjoint; `s`
↔ `sdg`; `t` ↔ `tdg`; `rx θ` ↦ `rx −θ` (and `ry`, `rz`); `qalloc` ↔ `qfree` of the same wires;
`inplace G G′ B X` ↦ `inplace G′ G B X`; `perm P` ↦ the library inverse of P. Control sets are
unchanged.

### 18.3 Marker rules

Wire `h.i` is wire i of handle h; n(h) its width. A wire is **named** by an event when it is one of
the event's operand wires. The conditions are checked when the marker is called, against H, and H
is updated then; Q changes only when an event is applied. A failed condition is a run-time trap:
fault code 4 (§17.5) with the named diagnostic (§22.2).

| Marker | Conditions (trap) | Effect |
|---|---|---|
| `qalloc(cls, n)` | n ≥ 1 (`T-SIZE`); cls in the class table (`T-CLASS`) | a new live handle h of n wires; event `qalloc h n`, whose application appends the n wires to Q in state 0; h belongs to the innermost active generation, if any |
| `qborrow(cls, n)` | as `qalloc` | inside a generation compiled as an ISA action, ISA `qborrow`/`qreturn` with borrow-frame verification (ISA §5.6); otherwise as `qalloc` (a correct user of borrowed wires also works on clean wires; ISA-9, §25.3). 0.1's `T-BORROW` is deleted |
| `qfree(h)` | h live (`T-DEAD`); if a recorder is active, h belongs to it (`T-FOREIGN`); when applied, Q is the product of the all-zero state on h's wires and a state of the other wires (`T-CLEAN`) | event `qfree h` |
| `gate(op, h, i)` | h live (`T-DEAD`); i < n(h) (`T-INDEX`); op in the table (`T-OP`) | the realisation of §3.4 on `h.i` |
| `gate2(op, a, i, b, j)` | as above for both; `a.i` ≠ `b.j` (`T-ALIAS`) | `cx a.i b.j`, `cz a.i b.j` or `swap a.i b.j` |
| `gate3(op, a, i, b, j, c, k)` | as above; the three wires distinct (`T-ALIAS`) | `ccx a.i b.j c.k` |
| `rot(op, h, i, θ)` | as `gate`; θ finite (`T-THETA`) | `rx θ`, `ry θ` or `rz θ` on `h.i` |
| `measure(h, i)` | as `gate`; no recorder active unless deferred (§7.5a) (`T-MEASURE`) | projective measurement of `h.i` (ISA §14.2); outcome m with its Born probability; the wire stays live in state m (ISA: `measure` and re-preparation, ISA-6 not a gap); returns m |
| `qload(dst, mem, addr)` | the three handles live and distinct (`T-DEAD`, `T-ALIAS`); n(mem) = 2^n(addr) · n(dst) (`T-SIZE`) | event `qload`: for every cell c, on the basis states where addr holds c, `dst.b ⊕= mem.(c·W + b)` for b < W = n(dst) (ISA §4.6 cell order) |
| `qstore(mem, addr, val)` | as `qload` with W = n(val) | event `qstore`: `mem.(c·W + b) ⊕= val.b` under addr = c |
| `qprep(h, src, n)` | h live; n ≤ n(h)/8 (`T-SIZE`); [src, src + n) valid (fault 7) | event `qprep h bytes`: wire 8k + j ⊕= bit j of byte k |
| `observe(p, len)` | [p, p + len) valid (fault 7); no recorder active (`T-MEASURE`) | TDL-11 |
| `ctrl(q, qi, f, budget, env)` | q live, qi < n(q); after generation, the wire `q.qi` is named by no event of E (`T-CTRL`) | E = gen(f, env) (§18.4); each event of E with `q.qi` added to its control set; then the TDL-8 combine |
| `adj(f, budget, env)` | – | E = gen(f, env); the adjoint of E |
| `compute(f, use, budget, env)` | – | E_f = gen(f, env); the TDL-8 copies of E_f's fault registers; E_u = gen(use, env); then the events E_f, copies, E_u, adjoint(E_f) |
| `reversible(f, budget, env)` | no recorder active (else §7.4 applies) | §18.6 |
| `oracle(f, budget, desc)` | the descriptor's checks (§8.1–§8.4: `T-IFACE`, `T-SIZE`, `T-DEAD`, `T-ALIAS`) | event `oracle` or `wide` of the dispatched shape: on every basis state, outputs ⊕= payload(F_B), fault ⊕= code(F_B) (ISA §5.2), F_B from the reference object of §16 on the entry state of §8.5 |
| `inplace(g, ginv, budget, desc)` | the descriptor's checks; budget ≥ B_min (`T-BUDGET`) | event `inplace`: x ← g(x; args), the permutation that §8.7 verified (ISA `qinplace`) |
| effect markers | §11 | §11 per tier |

A region operand whose value matches no source of its candidate set traps (`T-REGION`, §7.2); a
dispatched ill-formed candidate traps (`T-REGION-INVALID`).

### 18.4 Generation of action regions

`gen(R, env)` pushes a recorder, runs `R(env)`'s CC variant under §18.1 with the TDL partition of
§10 (its G instructions run once on the generation's view; its slices, stores to outliving objects
and marker calls produce events per §10 and §18.3, nested `ctrl`, `adj` and `compute` producing
their events into this recorder), pops the recorder and returns its event list E. **Leak rule**
(`T-LEAK`): for `ctrl` and `adj`, every register allocated during the generation is freed during
it; for `compute`, every register allocated during gen(use) is freed during it, while a register
allocated during gen(f) and not freed during it is freed by adjoint(E_f), in which its `qalloc`
event becomes a `qfree` event, so gen(use) MUST NOT free it (`T-FOREIGN`). Outside generations
the check is at program end (§6.6): a register that is still live then, neither freed by device
code or the host (`bennett_qreg_free`) nor consumed by a `measure`, is `T-LEAK`. *(non-normative)* The
classical part of an action region (G) runs once per invocation; its effect on outliving memory
is the events of TDL-5, so under `ctrl` it happens exactly on the branch where the control is 1
(the audit's counterexample to 0.1). NS §4.2 requires "allocations inside released clean or
borrowed and restored": `T-LEAK` and `T-CLEAN` are those checks.

### 18.5 Oracle semantics

An `oracle` event applies, on every basis state of its operands, the permutation |x⟩|t⟩|e⟩ ↦
|x⟩|t ⊕ payload(F_B(x, S))⟩|e ⊕ code(F_B(x, S))⟩ where F_B is the reference interpreter's result on
the reference object of the dispatched shape (§16) with the token's budget, and S is the entry
state of §8.5 (the caller's classical memory at the call). It is an involution (ISA §5.2).

### 18.6 Reversible semantics

`reversible(f, budget, env)` and the whole-program R mode (§19.2) run f on the R tier (ISA §3.1):
its classical effects on memory are those of §18.1, its effects are ISA device models on the tape
(§11.2), its region calls are R-tier region calls (§7.5b), and the run history (ISA §7.4) is
retained, so the whole run is reversible by `bennett_reverse` (ISA §10). A fault ends the run
(§17.6).

### 18.7 Conformance

A plugin and an executor (ISA §1.2) together conform iff, for every module the rules accept or
block, every host input and every sequence of measurement and `observe` outcomes, outside the
executions that reach a blocker point: the probability of that sequence, every classical value
the host observes (return values of device entries, memory they write, console output), every
fault code and every trap equal those of the reference semantics; and the quantum state at every
measurement and at every device-entry return equals the reference state, exactly when the program
uses permutation gates only, and otherwise within the error bound its certificate states (ISA
§12.3). A program that reaches `T-CLEAN` in the reference semantics is erroneous; an executor that
cannot test cleanliness (hardware) need not reproduce that trap (ISA §17 item 14).

**Outcome table** (NS §5.1: "one outcome table governs §3.2, §5.1 and §8"). For every input of a
declared domain the comparison with the native comparison build (§17.7) has one of four outcomes:

| Outcome | When | Comparison |
|---|---|---|
| native-comparable success | the reference completes without fault and no layout-dependent value influences the result | the artefact's results equal native |
| reference fault | the reference faults (code ≠ 0) | the artefact reports the same code; native supplies no cause (it may trap, silently read adjacent memory or hang) |
| layout-dependent | the reference interpreter's address provenance shows a host-stack address, or a `blockaddress` value (§14.9), influencing the result | validated against the reference interpreter instead of native, counted separately |
| classifier-flagged undefined | an instrumented build (UBSan, ASan, MSan) flags the input (NS §3.2) | excluded from comparison, counted separately |

### 18.8 Worked examples

**0.1 examples at ABI 0.2.** These programs are also legality cases in the corpus. The checker
builds each with the trace runtime (`corpus/legality/runtime/`), whose `ctrl` and `adj` call the
region once and whose `compute` calls `f`, `use`, `f`; it converts the trace into events by §18.3–
§18.4 (for `compute` it keeps the first `f` recording and checks that the third equals it) and
simulates them. Wire `Hk.i` is wire i of the k-th allocated handle; basis states list wires in
allocation order, leftmost first; the state is given before event `at` (0-based).

**Control.** A `ctrl` on a control in superposition entangles; a second `ctrl` disentangles:

```llvm semantics=sem2-ctrl corpus=spec-sem2-ctrl
; CASE: spec-sem2-ctrl
; HAZARD: dialect 0.2 reference-semantics example (spec section 18.8): ctrl of an action region that flips a target read from an environment, on a control in superposition, twice
; INPUTS: 0..3
; EXPECT: legal
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

declare ptr @__bennett_qalloc(i64, i64)
declare void @__bennett_qfree(ptr)
declare void @__bennett_gate(i32, ptr, i64)
declare void @__bennett_ctrl(ptr, i64, ptr, ptr, ptr)

define void @flip(ptr %e) {
  %t = load ptr, ptr %e
  call void @__bennett_gate(i32 1, ptr %t, i64 0)
  ret void
}

define i64 @case_entry(i64 %x) {
  %e = alloca ptr
  %c = call ptr @__bennett_qalloc(i64 0, i64 1)
  %t = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %t, ptr %e
  call void @__bennett_gate(i32 2, ptr %c, i64 0)
  call void @__bennett_ctrl(ptr %c, i64 0, ptr @flip, ptr null, ptr %e)
  call void @__bennett_ctrl(ptr %c, i64 0, ptr @flip, ptr null, ptr %e)
  call void @__bennett_gate(i32 2, ptr %c, i64 0)
  call void @__bennett_qfree(ptr %t)
  call void @__bennett_qfree(ptr %c)
  ret i64 %x
}
```

```text events=sem2-ctrl input=0
qalloc H0 1
qalloc H1 1
h H0.0
x H1.0 ctrl H0.0
x H1.0 ctrl H0.0
h H0.0
qfree H1
qfree H0
```

```text state=sem2-ctrl input=0 at=4
|00> 0.70710678
|11> 0.70710678
```

**Adjoint.** `adj` replays the recording reversed and inverted:

```llvm semantics=sem2-adj corpus=spec-sem2-adj
; CASE: spec-sem2-adj
; HAZARD: dialect 0.2 reference-semantics example (spec section 18.8): a direct call of a region body applies h s t; adj of the same body applies tdg sdg h and returns the register to 0
; INPUTS: 0..3
; EXPECT: legal
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

declare ptr @__bennett_qalloc(i64, i64)
declare void @__bennett_qfree(ptr)
declare void @__bennett_gate(i32, ptr, i64)
declare void @__bennett_adj(ptr, ptr, ptr)

define void @phase(ptr %e) {
  %q = load ptr, ptr %e
  call void @__bennett_gate(i32 2, ptr %q, i64 0)
  call void @__bennett_gate(i32 3, ptr %q, i64 0)
  call void @__bennett_gate(i32 5, ptr %q, i64 0)
  ret void
}

define i64 @case_entry(i64 %x) {
  %e = alloca ptr
  %q = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %q, ptr %e
  call void @phase(ptr %e)
  call void @__bennett_adj(ptr @phase, ptr null, ptr %e)
  call void @__bennett_qfree(ptr %q)
  ret i64 %x
}
```

```text events=sem2-adj input=0
qalloc H0 1
h H0.0
s H0.0
t H0.0
tdg H0.0
sdg H0.0
h H0.0
qfree H0
```

```text state=sem2-adj input=0 at=4
|0> 0.70710678
|1> -0.5+0.5i
```

**Compute–use–uncompute.** Phase kickback through an ancilla that the uncompute returns clean:

```llvm semantics=sem2-compute corpus=spec-sem2-compute
; CASE: spec-sem2-compute
; HAZARD: dialect 0.2 reference-semantics example (spec section 18.8): compute(f, use) with f = cx onto an ancilla and use = z on the ancilla; phase kickback leaves the ancilla clean
; INPUTS: 0..3
; EXPECT: legal
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

declare ptr @__bennett_qalloc(i64, i64)
declare void @__bennett_qfree(ptr)
declare void @__bennett_gate(i32, ptr, i64)
declare void @__bennett_gate2(i32, ptr, i64, ptr, i64)
declare void @__bennett_compute(ptr, ptr, ptr, ptr)

define void @copy(ptr %e) {
  %a = load ptr, ptr %e
  %pb = getelementptr i8, ptr %e, i64 8
  %b = load ptr, ptr %pb
  call void @__bennett_gate2(i32 1, ptr %a, i64 0, ptr %b, i64 0)
  ret void
}

define void @kick(ptr %e) {
  %pb = getelementptr i8, ptr %e, i64 8
  %b = load ptr, ptr %pb
  call void @__bennett_gate(i32 7, ptr %b, i64 0)
  ret void
}

define i64 @case_entry(i64 %x) {
  %e = alloca [2 x ptr]
  %a = call ptr @__bennett_qalloc(i64 0, i64 1)
  %b = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %a, ptr %e
  %pb = getelementptr i8, ptr %e, i64 8
  store ptr %b, ptr %pb
  call void @__bennett_gate(i32 2, ptr %a, i64 0)
  call void @__bennett_compute(ptr @copy, ptr @kick, ptr null, ptr %e)
  call void @__bennett_gate(i32 2, ptr %a, i64 0)
  call void @__bennett_gate(i32 1, ptr %a, i64 0)
  call void @__bennett_qfree(ptr %b)
  call void @__bennett_qfree(ptr %a)
  ret i64 %x
}
```

```text events=sem2-compute input=0
qalloc H0 1
qalloc H1 1
h H0.0
cx H0.0 H1.0
s H1.0
s H1.0
cx H0.0 H1.0
h H0.0
x H0.0
qfree H1
qfree H0
```

```text state=sem2-compute input=0 at=8
|10> 1
```

*(non-normative)* The states are those of 0.1 §8.8. Control: after h, one controlled flip gives
(|00⟩ + |11⟩)/√2 and the second cancels it. Adjoint: h|0⟩ = (|0⟩ + |1⟩)/√2, s multiplies the |1⟩
amplitude by i and t by e^{iπ/4}, so before the adjoint it is i·e^{iπ/4}/√2 = e^{i3π/4}/√2 =
(−1 + i)/2. Compute: h, cx give (|00⟩ + |11⟩)/√2; s s = Z on the ancilla gives (|00⟩ − |11⟩)/√2;
the uncomputing cx gives (|0⟩ − |1⟩)/√2 ⊗ |0⟩, and h maps it to |10⟩; x returns a to |0⟩ before
release.

**TDL.** The following programs exercise every case of TDL-5, TDL-10 and TDL-11 on the globals
`@cnt` and `@other`, which are in the may-Co set (TDL-2) and hence in the arena. Each device
entry ends by observing both globals, so that MC's state at every device entry is empty (MC3; a
host may call the entries in any order). `text tdl=` blocks give the partition of each region and
the run's events with their control sets; a register written `-> r:w` is a fresh register of w
wires allocated by that event. `text state=` blocks list the handles in allocation order and then
the arena bytes of `@cnt` (and `@other`) in hex, as `|q…; cnt other>`. Temporary and retained
registers (TDL-7, TDL-8) hold 0 in these fault-free runs and are omitted. Every Co read is from
the arena; every slice is an oracle bound to the arena region `coh`.

```llvm example=tdl verdict=accept
@cnt = internal global i8 0
@other = internal global i8 0

; TDL-5(a), classical value
define internal void @bump(ptr %e) {
  store i8 5, ptr @cnt
  ret void
}

; TDL-5(a), Co value: the old contents of @other are Cl
define internal void @copy1(ptr %e) {
  %v = load i8, ptr @cnt
  %w = add i8 %v, 1
  store i8 %w, ptr @other
  ret void
}

; TDL-5(b): a library bijection of a Co object
define internal void @add3(ptr %e) {
  %v = load i8, ptr @cnt
  %w = add i8 %v, 3
  store i8 %w, ptr @cnt
  ret void
}

; TDL-5(c): an overwrite of a Co object inside compute's f
define internal void @set9(ptr %e) {
  store i8 9, ptr @cnt
  ret void
}

define internal void @flip(ptr %e) {
  %t = load ptr, ptr %e
  call void @__bennett_gate(i32 1, ptr %t, i64 0)
  ret void
}

; TDL-10: a gate under a Co condition
define internal void @maybe(ptr %e) {
entry:
  %v = load i8, ptr @cnt
  %z = icmp eq i8 %v, 5
  br i1 %z, label %yes, label %out

yes:
  %t = load ptr, ptr %e
  call void @__bennett_gate(i32 1, ptr %t, i64 0)
  br label %out

out:
  ret void
}

define internal void @reset(ptr %h) {
entry:
  %m = call i1 @__bennett_measure(ptr %h, i64 0)
  br i1 %m, label %one, label %done

one:
  call void @__bennett_gate(i32 1, ptr %h, i64 0)
  br label %done

done:
  call void @__bennett_qfree(ptr %h)
  ret void
}

define internal void @settle() {
  call void @__bennett_observe(ptr @cnt, i64 1)
  call void @__bennett_observe(ptr @other, i64 1)
  ret void
}

define i8 @tdl_a() {
  %c = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @__bennett_gate(i32 2, ptr %c, i64 0)
  call void @__bennett_ctrl(ptr %c, i64 0, ptr @bump, ptr null, ptr null)
  call void @settle()
  %v = load i8, ptr @cnt
  call void @reset(ptr %c)
  ret i8 %v
}

define void @tdl_b() {
  %c = call ptr @__bennett_qalloc(i64 0, i64 1)
  %c2 = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @__bennett_gate(i32 2, ptr %c, i64 0)
  call void @__bennett_gate(i32 2, ptr %c2, i64 0)
  call void @__bennett_ctrl(ptr %c, i64 0, ptr @bump, ptr null, ptr null)
  call void @__bennett_ctrl(ptr %c2, i64 0, ptr @copy1, ptr null, ptr null)
  call void @__bennett_ctrl(ptr %c2, i64 0, ptr @add3, ptr null, ptr null)
  call void @settle()
  call void @reset(ptr %c2)
  call void @reset(ptr %c)
  ret void
}

define void @tdl_d() {
  %e = alloca ptr
  %c = call ptr @__bennett_qalloc(i64 0, i64 1)
  %t = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %t, ptr %e
  call void @__bennett_gate(i32 2, ptr %c, i64 0)
  call void @__bennett_ctrl(ptr %c, i64 0, ptr @bump, ptr null, ptr null)
  call void @__bennett_compute(ptr @set9, ptr @flip, ptr null, ptr %e)
  call void @settle()
  call void @reset(ptr %t)
  call void @reset(ptr %c)
  ret void
}

define void @tdl_f() {
  %e = alloca ptr
  %c = call ptr @__bennett_qalloc(i64 0, i64 1)
  %c2 = call ptr @__bennett_qalloc(i64 0, i64 1)
  %t = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %t, ptr %e
  call void @__bennett_gate(i32 2, ptr %c, i64 0)
  call void @__bennett_gate(i32 2, ptr %c2, i64 0)
  call void @__bennett_ctrl(ptr %c, i64 0, ptr @bump, ptr null, ptr null)
  call void @__bennett_ctrl(ptr %c2, i64 0, ptr @maybe, ptr null, ptr %e)
  call void @settle()
  call void @reset(ptr %t)
  call void @reset(ptr %c2)
  call void @reset(ptr %c)
  ret void
}
```

`@tdl_a`: the store of `@bump` has view Cl(0), so it is the classical event of TDL-5(a); applied
under H0.0 it materialises `@cnt` (its shadow is 0, so the XOR changes no wire) and makes it Co;
`observe` then measures it (TDL-11):

```text tdl=tdl-a
@bump: G = { store i8 5, ptr @cnt -> xmask @cnt+0 0x05 }, slices = {}
events of @tdl_a:
qalloc H0 1
h H0.0
xmask @cnt+0 0x05 ctrl H0.0
observe @cnt+0 1
observe @other+0 1
measure H0.0
```

```text state=tdl-a at=3
|0; 00> 0.70710678
|1; 05> 0.70710678
```

*(non-normative)* `observe` gives 0x00 with probability 1/2 (H0 collapses to |0⟩) or 0x05 with
probability 1/2 (H0 to |1⟩); `@tdl_a` returns that byte, and `measure` of H0 agrees with it before
the reset. Under 0.1's semantics the store would have happened on both branches and `@tdl_a`
would return 5 with certainty.

`@tdl_b` runs `@bump` under H0, then `@copy1` and `@add3` under H1. In `@copy1` the load of `@cnt`
(state Co) is Co, so the load and the `add` form slice O1, and the store into `@other`, whose view
is Cl(0), is TDL-5(a) with a Co value. In `@add3` the three instructions are the library bijection
"add 3" of TDL-5(b):

```text tdl=tdl-b
@copy1 (signature: @cnt may-Co, @other Cl): slice O1 = { %v = load i8, ptr @cnt; %w = add i8 %v, 1 } with ARG c (the old byte of @other), MEM_IN coh, output m:8 = c xor %w; store i8 %w, ptr @other -> TDL-5(a) with a Co value
@add3 (signature: @cnt may-Co): { %v = load; %w = add i8 %v, 3; store i8 %w, ptr @cnt } -> TDL-5(b) perm add.i8 with k = 3
events of @tdl_b up to the observes:
qalloc H0 1
qalloc H1 1
h H0.0
h H1.0
xmask @cnt+0 0x05 ctrl H0.0
slice O1 args(0x00) mem(coh) -> m1:8 f1:4 ctrl H1.0
xstore @other+0 m1 ctrl H1.0
slice O1 args(0x00) mem(coh) -> m1 f1b:4 ctrl H1.0
qxor f1 f1b
qfree f1b
qfree m1
firstfault (f1) -> Phi1:4
perm add.i8 @cnt+0 k=3 ctrl H1.0
```

```text state=tdl-b at=10
|00; 00 00> 0.5
|01; 00 01> 0.5
|10; 05 00> 0.5
|11; 05 06> 0.5
```

```text state=tdl-b at=13
|00; 00 00> 0.5
|01; 03 01> 0.5
|10; 05 00> 0.5
|11; 08 06> 0.5
```

*(non-normative)* Before event 10 the copy-out pair is complete: `@other` = cnt + 1 exactly where
H1 is 1: 0 + 1 = 1 and 5 + 1 = 6. The permutation "add 3" under H1 then gives cnt = 5·H0 + 3·H1:
0, 3, 5, 8.

A second `@copy1` invocation would overwrite `@other`, whose state is then Co, with a value that
is not a bijection of its old contents, outside `compute`: TDL-5(d) (NS §4.2):

```llvm example=tdl-overwrite verdict=reject:BD-E-COHERENT-OVERWRITE
@cnt = internal global i8 0
@other = internal global i8 0

define internal void @bump(ptr %e) {
  store i8 5, ptr @cnt
  ret void
}

define internal void @copy1(ptr %e) {
  %v = load i8, ptr @cnt
  %w = add i8 %v, 1
  store i8 %w, ptr @other
  ret void
}

define void @twice() {
  %c = call ptr @__bennett_qalloc(i64 0, i64 1)
  %c2 = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @__bennett_gate(i32 2, ptr %c, i64 0)
  call void @__bennett_gate(i32 2, ptr %c2, i64 0)
  call void @__bennett_ctrl(ptr %c, i64 0, ptr @bump, ptr null, ptr null)
  call void @__bennett_ctrl(ptr %c2, i64 0, ptr @copy1, ptr null, ptr null)
  call void @__bennett_ctrl(ptr %c2, i64 0, ptr @copy1, ptr null, ptr null)
  call void @__bennett_observe(ptr @cnt, i64 1)
  call void @__bennett_observe(ptr @other, i64 1)
  ret void
}
```

`@tdl_d`: `compute(@set9, @flip)` with `@cnt` Co: the store of 9 is TDL-5(c); the new byte (a
constant) is computed by a slice invocation, exchanged into the cell, kept as history h, and
restored by the adjoint; the fault register f9 is copied into a retained g9 between E_f and E_use
(TDL-8):

```text tdl=tdl-d
@set9 inside compute f (signature: @cnt may-Co): slice O9 = { the constant 9 } output h:8; store i8 9, ptr @cnt -> TDL-5(c) xchg
events of @tdl_d up to the observes:
qalloc H0 1
qalloc H1 1
h H0.0
xmask @cnt+0 0x05 ctrl H0.0
slice O9 -> h:8 f9:4
xchg @cnt+0 h
copy f9 -> g9:4
x H1.0
xchg @cnt+0 h
slice O9 -> h f9
qfree h
qfree f9
```

```text state=tdl-d at=7
|00; 09> 0.70710678 (h = 00)
|10; 09> 0.70710678 (h = 05)
```

```text state=tdl-d at=12
|01; 00> 0.70710678
|11; 05> 0.70710678
```

*(non-normative)* Events 4–5 are E_f, 6 is the copy, 7 is E_use, 8–9 are adjoint(E_f): the
exchange puts the displaced byte back and the second slice invocation XORs 9 into h, which held 9,
so h and f9 are clean before release. During `use`, `@cnt` is 9 on both branches while h holds the
old byte: the history is entangled with H0 exactly while it must be (NS §3.1
compute-with-uncompute).

`@tdl_f`: in `@maybe` the branch on `%z` is a Co branch (the load of `@cnt` is Co), so the gate is
issued under `qpred` of the condition wire (TDL-10):

```text tdl=tdl-f
@maybe (signature: @cnt may-Co): slice Oz = { %v = load i8, ptr @cnt; %z = icmp eq i8 %v, 5 } output w:1; the gate in %yes is control-dependent on %z -> issued under qpred w
events of @tdl_f up to the observes:
qalloc H0 1
qalloc H1 1
qalloc H2 1
h H0.0
h H1.0
xmask @cnt+0 0x05 ctrl H0.0
slice Oz mem(coh) -> w:1 fz:4 ctrl H1.0
x H2.0 ctrl H1.0 w
slice Oz mem(coh) -> w fzb:4 ctrl H1.0
qxor fz fzb
qfree fzb
qfree w
firstfault (fz) -> Phi1:4
```

```text state=tdl-f at=13
|000; 00> 0.5
|010; 00> 0.5
|100; 05> 0.5
|111; 05> 0.5
```

*(non-normative)* w = (cnt = 5) = H0, so the target H2 flips exactly where H0 and H1 are 1.

An effect inside an action region (TDL-12): the console write cannot happen under control, so on
the branch where the control is 1 it is the fault code 8 in a retained register, combined into the
plugin-allocated fault register Φ (the budget record is null), and the fault rate (here 1/2) is a
reported quantity:

```llvm example=tdl-effect verdict=accept
@msg = private unnamed_addr constant [2 x i8] c"!\0A"

define internal void @loud(ptr %e) {
  %t = load ptr, ptr %e
  call void @__bennett_gate(i32 1, ptr %t, i64 0)
  call void @__bennett_effect_console_write(ptr @msg, i64 2)
  ret void
}

define void @tdl_e() {
  %e = alloca ptr
  %c = call ptr @__bennett_qalloc(i64 0, i64 1)
  %t = call ptr @__bennett_qalloc(i64 0, i64 1)
  store ptr %t, ptr %e
  call void @__bennett_gate(i32 2, ptr %c, i64 0)
  call void @__bennett_ctrl(ptr %c, i64 0, ptr @loud, ptr null, ptr %e)
  ret void
}
```

```text tdl=tdl-effect
@loud: G = { load of %t; the gate marker -> x; the effect marker -> fault 8 (TDL-12) }, slices = {}
events of @tdl_e:
qalloc H0 1
qalloc H1 1
h H0.0
x H1.0 ctrl H0.0
fault 8 -> f1:4 ctrl H0.0
firstfault (f1) -> Phi1:4
```

```text state=tdl-effect at=6
|00; f1 = 0, Phi1 = 0> 0.70710678
|11; f1 = 8, Phi1 = 8> 0.70710678
```

*(non-normative)* `@tdl_e` returns with H0 and H1 live, as a REPL keeps registers (§6.6); the run's
CC epilogue measures the retained f1 and Φ1 (TDL-8) and reports code 8 with probability 1/2. A
program that ended without freeing H0 and H1 would trap `T-LEAK` at its end.

A rotation by an angle that is superposed and has an unbounded value set cannot be predicated per
value (TDL-10): `@setang` stores a host value under control, so `@ang` is Co with value set ⊤,
and `@spin` rotates by it:

```llvm example=tdl-angle verdict=reject:BD-E-COHERENT-ANGLE
@ang = internal global double 0.0

define internal void @setang(ptr %e) {
  %x = load double, ptr %e
  store double %x, ptr @ang
  ret void
}

define internal void @spin(ptr %e) {
  %p = getelementptr i8, ptr %e, i64 8
  %t = load ptr, ptr %p
  %a = load double, ptr @ang
  call void @__bennett_rot(i32 3, ptr %t, i64 0, double %a)
  ret void
}

define void @top(double %x) {
  %e = alloca { double, ptr }
  %c = call ptr @__bennett_qalloc(i64 0, i64 1)
  %t = call ptr @__bennett_qalloc(i64 0, i64 1)
  store double %x, ptr %e
  %p = getelementptr i8, ptr %e, i64 8
  store ptr %t, ptr %p
  call void @__bennett_gate(i32 2, ptr %c, i64 0)
  call void @__bennett_ctrl(ptr %c, i64 0, ptr @setang, ptr null, ptr %e)
  call void @__bennett_adj(ptr @spin, ptr null, ptr %e)
  call void @__bennett_observe(ptr @ang, i64 8)
  ret void
}
```

## 19. The driver (driver 0.2)

### 19.1 Pipeline position and bitcode sources

Front ends emit bitcode with their stock pre-link pipelines; no Bennett code runs before the final
link (Enzyme PR #3211: "forgetting it is a loud failure"), except in the explicit closed-unit mode
(§19.7). The driver links all bitcode inputs (§19.8), links `bennett-runtimes` and `bennett-arith`
bitcode of the link's major M, runs the post-link pipeline (`lto<O3>` by default, or any envelope
pipeline of §21.1 the user selects), then runs the plugin on the whole program (NS §3.3). With
`opt`:

```
opt -load-pass-plugin=libbennett-plugin-<M>.so -passes='lto<O3>,bennett' -bennett-dialect=0.2 …
```

The plugin runs on one merged module (full LTO; §24 D23). It registers one module pass, `bennett`,
and MAY register a full-LTO last extension point for use from a linker plugin; it MUST do nothing
in a pre-link phase. **Bitcode sources** (NS §3.3): Rust `std` from the bitcode embedded in rlibs
(`.llvmbc`) where present and readable by §19.8, else `-Zbuild-std`; the Julia runtime by the
runtimes' shim bitcode; every remaining call without bitcode is a `trapped` coverage line (§4.5).

### 19.2 Mode `--bennett-tier=reversible --bennett-entry=<sym>`

The whole program is the device program in tier R (NS §4.2: "entered through
`__bennett_reversible` or a driver mode"; rungs 3, 5, 6):

- a CC **launch stub** fetches the argv and envp bytes with `hostcall bennett.argv`, initialises
  the shadow stack (§17.3), calls the R entry `<sym>` with (argc, argv, envp), catches the exit
  pseudo-exception (§14.7) and returns the status;
- effects are the ISA device models (§11.2): console, clock, entropy (the launch's entropy tape),
  block with `block_image` from `--bennett-disk=<file>`;
- un-run is `bennett_reverse` (ISA §10): whole-run reversal restores the entry state; tape replay is
  deterministic from the tape and the entropy;
- a `measure` reachable in the program is `BD-E-REVERSIBLE-MEASURE` (§7.5b).

### 19.3 Mode `--bennett-oracle=<sym>` ("oracle from program")

A convenience: the driver synthesises the translation unit a quantum programmer would write
(§16.7): a CC function that builds a descriptor binding `<sym>`'s parameters by
`--bennett-bind=<param>:<kind>:<width>[:<value>]` (kind `in`, `arg`, `mem_in`, `out`), device
bindings by `--bennett-dev=<model>:<width>[:<value>]`, and a payload: the return value, the exit
status caught by the wrapper (§14.7), or the first L bytes of console output
(`--bennett-payload=return|exit|console:<L>`), and applies the oracle once to registers it
allocates, as a device entry the host calls with those registers. The normative route is the
separate translation unit with marker calls naming the unmodified function (rungs 4, 7, 8).

### 19.4 Placement: host vs device CC

H functions stay native unless they share **pointer-rich** memory with device code: a pointer
argument of a device-entry call, or a global accessed by both, whose pointee may contain pointers
that device code reads (§5). Such H functions are **promoted** to CC variants, transitively up to
their roots (in the limit `main`, and then H is the system-call proxy only: `hostcall
bennett.syscall`). Results are equal by the materialised semantics; ISA-11 would let them stay
native (an efficiency and placement item, §25.3; outline E11).

### 19.5 Layout: the comparison link

The driver links the materialised module natively (§17.7) with a linker script that fixes the
addresses: non-PIE; identical-code folding and constant merging off; the null region [0,
`null_size`) with `null_size` = 4096; the data sections (`.rodata`, `.data`, `.bss`, in that order)
from `data_base` = 4096; the text from `text_base` = 0x400000, or, when the device ranges below
(data, heap, arena, interface regions, computed first) end above 0x400000, from the first multiple
of 0x200000 at or after their end, so that the native comparison binary maps its code disjointly
from them; the defaults are options (`--bennett-layout-data-base`, `--bennett-layout-text-base`,
§24). The link map gives A(F) for
every function and the base of every global. The device `layout` (ISA §9.1) replicates it:

- `globals`: every global of the link at its link address with its image;
- `heap_base`: the first multiple of 4096 at or after the end of the data; `heap_limit_max`: the
  largest `heap` of the budget table (which covers the shadow stack, §9.2);
- the arena (TDL-4) at the first multiple of its size 2^A at or after the heap's end, with 2^A the
  smallest power of two covering the may-Co globals and the coherent allocator's heap (its size
  from `--bennett-arena-heap`, default the largest `heap` of the table); the arena's shadow
  `__bennett_rt_shadow` is a global of the data sections;
- interface regions per oracle above the arena (§16.3); H, A_tab and S_cells by §16.3;
- the production host image is linked with the same addresses for every function and global
  whose address may cross the boundary (§4.4).

*(non-normative)* With data low and text high, H covers the data, heap and regions; function
addresses are values only and never occupy device memory.

### 19.6 Build-time snapshots

`--bennett-snapshot=<dump>` rewrites the initialisers of the mutable globals listed in the dump
(and the platform RAM global, §20.1) to the dump's bytes before the plugin runs; the data images
then carry the snapshot and R of §8.5 is empty for them (rung 7: "kernel state snapshot fixed
classically after boot"). The dump is recorded by hash in the build record.

### 19.7 Closed-unit mode

`-bennett-closed-unit` (the REPL fast path, NS §3.3: "a per-TU invocation remains available as a
fast path for programs closed within one unit, with the same semantics"): the plugin runs on one
module plus the runtimes and arith bitcode, after a **closedness check**: every device function's
callees are defined in that set or are trapped exactly as in whole-program mode; no device
function's address escapes the module; no function pointer enters through a device-entry
parameter. If the check passes, processing is identical to whole-program mode. If it fails, the
driver falls back to whole-program mode (it does not reject). Objects are content-addressed (ISA
§9.2) and linked at launch (ISA §9.3), so the REPL is incremental.

### 19.8 Mixed LLVM majors

The driver reads every bitcode input with the newest major M of the envelope (bitcode is readable
by newer majors), links with M and runs plugin M; runtimes and arith ship bitcode for each M.
Every input MUST have one target datalayout and triple (NS §3.2) (`BD-E-VERSION` otherwise: a
tool-version mismatch, not a program property). An input newer than M is `BD-E-VERSION`. The
tested (front end, major) pairs are published in the envelope; a corpus case links clang 18
bitcode with Julia's and rustc's majors (§21.2; bd `.16`).

### 19.9 Options, identity, outputs, module flag

| Option | Meaning | Default |
|---|---|---|
| `-bennett-dialect=<v>` | MUST equal the plugin's dialect version (`BD-E-VERSION`) | required |
| `-bennett-isa=<v>` | MUST equal the ISA version the plugin targets (`BD-E-VERSION`) | `0.8` |
| `--bennett-budgets=<file>`, `--bennett-budget-default=<s,h,st,d,ss>` | §9.2 | §9.2 defaults |
| `--bennett-class=<name>` | §3.4 | none |
| `--bennett-tier=reversible`, `--bennett-entry=<sym>`, `--bennett-disk=<file>` | §19.2 | – |
| `--bennett-oracle=<sym>`, `--bennett-bind=…`, `--bennett-dev=…`, `--bennett-payload=…` | §19.3 | – |
| `--bennett-snapshot=<dump>` | §19.6 | – |
| `-bennett-closed-unit` | §19.7 | off |
| `--bennett-platform=<profile>` | §20 | none |
| `--bennett-vscale=<V>`, `--bennett-cpu=<model>` | §12.5, §15.2 | §24 |
| `--bennett-qreg-instances=<n>` | §6.5 | 64 |
| `-bennett-inplace-exhaustive-bits=<n>` | §8.7 | 24 |
| `-bennett-warn-qstore` | §6.7 | off |
| `-bennett-out=<dir>` | the outputs below | required |

**Identity.** `llvmGetPassPluginInfo` returns plugin name `bennett` and version string
`dialect-0.2;isa-0.8`; the driver refuses a plugin whose string differs. One plugin build per LLVM
major (NS §3.2).

**Outputs** (in `-bennett-out`, file names plugin-defined, §24 D22): the materialised device
variants as bitcode (§17.7); the host module with device entries replaced by launch stubs; the ISA
objects (ISA §9, §16); the certificate (ISA §12) with `producer.materialisation = {llvm_version,
pipeline, normaliser_version: "0.2"}` and `bindings.dialect_mapping_version = "0.2"`; the coverage
report (ISA §13), whose `source` field is `dialect-0.2:<rule id>` (e.g. `dialect-0.2:N33`); the
blocker reports (§25.1); and the **build record**, one JCS object with the build flags, the
budget table (resolved) and its SHA-256, the runtimes, arith and asm-table hashes, the snapshot
hash, the layout options and the `cpuid` leaf table (§15.2). Its SHA-256 is recorded as the build metadata of the certificate's
`producer.version` (`<driver version>+build.<hex>`) until the ISA certificate has a field for it
(§25.2).

**A missing plugin fails loud.** No production artefact defines a marker: `bennett-runtimes`,
`bennett-arith` and the driver's link inputs define no `__bennett_*` marker symbol (test runtimes
such as the trace runtime do, and are never linked into production). A link in which the plugin
did not run therefore leaves undefined references and fails at link time; the driver MUST NOT
ignore unresolved symbols or supply weak marker definitions.

**Module flag.** A producer MAY add `!{i32 1, !"bennett.dialect", !"0.2"}` (behaviour Error, so an
LTO link of modules of two dialect versions fails); the plugin MUST reject a module whose flag
differs from its version (`BD-E-VERSION`):

```llvm example=version-flag verdict=reject:BD-E-VERSION
define void @top() {
  %h = call ptr @__bennett_qalloc(i64 0, i64 1)
  call void @__bennett_qfree(ptr %h)
  ret void
}

!llvm.module.flags = !{!0}
!0 = !{i32 1, !"bennett.dialect", !"0.1"}
```

## 20. Platform profile `riscv64-bennett-virt` (platform 0.2; rungs 6–7)

NS §5: "The kernel compiles, boots on the VM in the reversible tier with its devices modelled,
writes a serial console to the tape, and un-boots to the reset vector." This section fixes the
mechanisms (outline E4: riscv64 first); its row lists come from the platform spike of §20.7, a
mechanics deferral (§24): the capability is not in question (audit O-06).

### 20.1 Model

A virtual board, selected by `--bennett-platform=riscv64-bennett-virt`:

- RAM: one runtimes global `__bennett_rt_platform_ram` of the configured size
  (`--bennett-platform-ram`, default 128 MiB), which the profile's linker script places at the
  board's physical base 0x80000000 after the other data (the heap and the text follow it by
  §19.5), so kernel physical addresses are ordinary device addresses;
- the CSR file (privilege mode, `satp`, `stvec`, `mtvec`, `sstatus`, `mstatus`, `sie`, `sip`,
  `scause`, `sepc`, `stval`, `sscratch`, `mscratch`, `time`, …) as the runtimes global
  `__bennett_rt_csr`;
- devices: a UART 16550 (console), a CLINT and timer (clock), a PLIC, and a virtio-blk MMIO device
  (block), each a runtimes C model over the effect markers.

### 20.2 asm rows

The privileged forms are `shimmed` rows of §15: `csrr`, `csrw`, `csrs`, `csrc` (and the immediate
forms) → `__bennett_rt_csr_read(i32 csr)`, `_write(csr, v)`, `_set(csr, v)`, `_clear(csr, v)`;
`sfence.vma` → `__bennett_rt_sfence_vma(va, asid)`; `wfi` → `__bennett_rt_wfi()` (advances the
clock model to the next timer event); `ecall` in kernel mode → `__bennett_rt_sbi_call(…)` (the SBI
of the board), in user mode → the trap path of §20.4; `mret`, `sret` → `__bennett_rt_trap_return
(mode)`; `fence.i` and `fence` → deleted (lowered). The exact asm strings and constraint strings
are those the §20.7 spike inventories.

### 20.3 MMIO routing (N35)

Under the platform profile, N9 first routes every volatile load and store, and every MMIO asm
form, to `__bennett_rt_mmio_{load,store}_i<N>(addr[, v])`; these dispatch by address range to the
device models' handlers (C code in runtimes that calls the effect markers), and otherwise access
memory. A non-volatile access to an MMIO window lies outside every live allocation and faults with
code 7, as the reference semantics defines (§17.1).

### 20.4 Interrupts (N35)

Poll points at loop back edges and function entries (N35) call `__bennett_rt_poll()`, which checks
the timer model (deterministic, driven by the clock model) and the PLIC's pending bits; on
delivery it sets the CSRs (`scause`, `sepc`, `stval`, `sstatus`) and calls the trap vector
`stvec` by A(F) dispatch (§14.2). Interrupts are therefore taken at poll points only, a
deterministic choice recorded in the certificate; NS §3.2's single-thread assumption covers the
uniprocessor kernel (`CONFIG_SMP=n`, xv6 `CPUS=1`).

### 20.5 Context switch and traps

The assembly entry points (`swtch`, `trampoline`, `uservec`, `userret`, `kernelvec`, Linux
`__switch_to`, `handle_exception`, `ret_from_exception`) are platform shims by symbol (§15.3),
written in C over the fibers of §14.6: a kernel context switch is a fiber switch; a trap entry
saves the user registers into the trap frame from the platform register file and calls the
kernel's handler; a trap return restores them and resumes the user fiber.

### 20.6 User processes

User programs are built to bitcode and linked into the device program under the comparison layout
(§19.5); their ELF images on the disk image are the same link, so entry and function addresses
are A(F). `exec` and `sret` to user mode dispatch the user entry by A(F); user loads and stores go
through a **soft-MMU**: N35 instruments the functions of the user compartment with an Sv39 walk
over the modelled `satp`, page faults delivered through §20.4.

### 20.7 Platform spike (mechanics)

Build xv6-riscv and Linux `tinyconfig` riscv64 (uniprocessor, `CONFIG_SMP=n`) to bitcode with
build flags only (NS §0); inventory every asm form, `.S` symbol, MMIO site and switch path, as
SQLite §3 did; fix the row lists of §20.2 and §20.5 and the board constants of §20.1. Until then
those rows are this section's patterns (§24).

## 21. Legality corpus and conformance suites (corpus 0.2)

### 21.1 The corpus

`corpus/legality/` holds the cases (`cases/`: the 56 spike cases plus the `spec-*` cases of this
document), four negative controls (`controls/`), the harness (`harness/run.py`), the trace runtime
(`runtime/`) and the spike's results. Spike cases use the provisional ABI v0 and arbitrary
operation codes: they are **legality** cases (what LLVM passes do to marker programs), not
well-formedness cases; the legality property (§3.6) does not depend on a marker's signature. The
harness checks and their 0.2 reading:

| Check | Property | 0.2 reading |
|---|---|---|
| L1 | the dynamic marker sequence and the classical result are preserved | unchanged; for cases whose marker operands are computed from floating point or query intrinsics, the baseline is the materialised module (§17.7) |
| L2 | no pass adds a forbidden attribute | the three lists of §3.6 |
| L3 | handles stay contained (guard page, `BADHANDLE`; static review of new casts) | dynamic part unchanged; the static review is decided by §6 |
| L4 | region identity | every region operand resolves (§7.2) to candidates content-equal (§7.3) to the baseline's: aliases, forwarding thunks and merged twins pass (harness relaxation, bd `-cjb`) |
| L5 | native code generation keeps L1 and every marker an undefined external | unchanged |
| L6 | region-operand shapes | every shape resolves (§7.2: the candidate set is bounded by the program) |

**Supported envelope**: LLVM 18, 20 and 23; `default<O0>` … `default<O3>`; `default<Os>`,
`default<Oz>` on 18 and 20 (LLVM 23's `opt` rejects them); `lto-pre-link<O3>`, `lto<O3>`,
`thinlto-pre-link<O3>`, `thinlto<O3>`, `default<O3>` three times; clang `-O0` … `-O3` with
`-flto`; rustc `-C opt-level` 0, 1, 2, 3, s, z, including its MergeFunctions in aliases mode;
Julia 1.13's own pipeline; `strip`, `strip-nondebug` and `mergefunc` alone. **Unsupported**
(LLVM bugs outside the contract on every supported major; spike findings §2): the Attributor,
module and CGSCC (llvm-project #234748, #236104, and on 18 and 20 the constant-table fold fixed by
PR #151359); `normalize` without `preserve-order` (#236128); `structurizecfg` without its
prerequisites; the passes the harness classes `non-preserving` and the sanitizer and
instrumentation passes; any other single pass not run inside an envelope pipeline (§24 D20).

Work items the corpus owns for 0.2: rerun P4 (clang `-flto` end to end) and add a rustc
`-Clinker-plugin-lto` case (bd `-j88`); the trace runtime and harness at ABI 0.2 (bd `-566`);
minimise the three P3-only interactions (bd `-ape`); a `-g` variant of every `.c` case (bd
`-u6a`); Windows funclet and non-x86-64 cases (bd `-kdj`).

### 21.2 New legality cases

Before this version freezes, the corpus gains cases (each `EXPECT: legal` unless stated) for:
descriptor construction by constant stores in C, Rust and Julia surviving `default<O3>` (§3.8,
§8.1); the budget record (§9.1); every changed or new marker signature (§3.2); the effect markers
(§3.2, §11); `observe`; a cross-major link (§19.8); region pointers from host input and from a
Julia `@cfunction` (§7.2); handle `Vec`, `std::vector` and linked lists (§6.4); EH, sjlj and
varargs through the pipeline (§14); the benign attributes of §3.6 on the three majors. The
`spec-sem2-*` cases are byte-identical to the §18.8 programs; `spec-sem-*` are their 0.1-ABI
predecessors and stay as legality cases.

### 21.3 Conformance suites

| Suite | Class | Content |
|---|---|---|
| DA | Plugin, Validator | recognition, reserved names, attributes, Julia check, unwinding of markers: the §3 examples; L2 over the corpus |
| DB | Plugin, Validator | the device analysis and handles: the §5 and §6 examples; L3 over the corpus |
| DC | Plugin, Validator | candidate sets, identity, kinds, well-formedness: the §7 examples; L4, L6 over the corpus |
| DO | Plugin | descriptors, shapes, entry state, wide outputs, in-place: the §8 examples |
| DN | Plugin, Validator | normalisation pairs, native differentials and validator verdicts: the §12–§15 examples; two independent validators agree on the corpus after materialisation |
| DM | Plugin | the lifting map: the §16 objects, hashes, runs and step checks, executed on the ISA reference interpreter |
| DS | Plugin + executor | marker semantics: the §18.8 programs, events and states; differential runs against the reference semantics (§18.7) |
| DT | Plugin + executor | TDL partitions, events and states (§10, §18.8) |
| DE | Plugin + executor | effects per tier (§11): R console with reversal, CC host effects, L device models |
| DV | Plugin | varargs, EH, sjlj and fibers (§14) on the three target ABIs |
| DR, DF | Runtime | the contract rows of `bennett-runtimes` (§11, §14, §17.3, §20) and `bennett-arith` (§13): test vectors |
| DD | Driver | the driver modes (§19.2–§19.7), closed-unit equivalence, mixed majors, layouts |
| DP | Platform | the platform profile (§20) |
| DX | everything | the rung-mini programs end to end (§21.4) |
| DL | Toolchain | the legality matrix of §21.1 |

### 21.4 The pre-flight checker and rung minis

`scripts/dialect_check.py` executes every tagged example of this document (§1.5) under rules P-1
to P-3. The capabilities it needs and the executor of each are Appendix B. Its seeds live in
`spec/seeds/` (C, used only by the checker; `bennett-runtimes` and `bennett-arith` implement
independently, CLAUDE.md rule 5): a minimal allocator over the layout heap, the shadow stack,
memmove/memset/memcmp, the EH state and a personality subset, setjmp/longjmp, swapcontext,
binary64 soft-float add/mul/cmp/conversions, `exp`/`log` from musl, a console/entropy device stub
over the effect markers and the musl `__syscall` row; their semantics equal the contract rows of
§11, §13, §14 and §17.3. Suite DX holds the rung minis: R1 (an Int8 Rust function, exhaustive:
§16.6), R2 (a C hashtable; the heap example §16.9 is its kernel), R3 (a `puts` through the runtimes
seed in R, reversed: §11.6), R4 (§16.7), R8 (§16.8).

## 22. Diagnostics

### 22.1 Compile-time rejections

Every row cites the north-star clause or maintainer decision that requires the rejection; a
rejection without one may not exist (standing rule).

| Code | Rule | Required by |
|---|---|---|
| `BD-E-VERSION` | §19.8, §19.9 | NS §3.2 (per-major builds, "one target datalayout", "tested compatibility envelope"); a tool mismatch, not a program property |
| `BD-E-MARKER-DEFINED` | §3.1 rule 1 | NS §3.1 ("declared external marker functions") |
| `BD-E-MARKER-UNKNOWN` | §3.1 rule 2 | NS §3.1 (recognition by name; reserved names) |
| `BD-E-MARKER-ADDRESS` | §3.1 rule 3 | NS §3.1 ("recognises them by name and signature": a marker is never called indirectly) |
| `BD-E-MARKER-SIGNATURE` | §3.5 | NS §3.1 ("fixed signatures") |
| `BD-E-MARKER-ATTRIBUTE` | §3.6 | NS §3.1 (the positive legality requirement) |
| `BD-E-JULIA-CCALL` | §3.8 | NS §3.3 (per-front-end integration; the `llvmcall` route keeps the capability, audit B-13) |
| `BD-E-EFFECT-LIE` | §3.8 | NS §3.1 (positive legality), NS §3.2 (definedness) |
| `BD-E-OPERAND` | §3.4 (a constant outside its table) | NS §3.1 (fixed operand encodings); the marker faults on every execution that reaches it |
| `BD-E-HANDLE-USE` | §6.2 | maintainer decision 2; NS §3.1 ("never dereferenced") |
| `BD-E-HANDLE-ESCAPE` | §6.4 | NS §3.1 ("any handle use that survives into host native code is rejected") |
| `BD-E-HANDLE-UNTRACKED` | §6.2 | NS §3.1 (handles are the results of `qalloc`; linearity is a fail-loud verifier obligation) |
| `BD-E-REGION-TYPE` | §7.2 (the unique candidate) | decision 3 (candidates of the required type); the call is undefined on every execution |
| `BD-E-REGION-MEASURE` | §7.5(a) (the unique candidate, or the closure of every candidate), unless deferred | NS §3.1 ("user measurement inside it is refused") |
| `BD-E-REVERSIBLE-MEASURE` | §7.5(b) | NS §4.2 (reversible tier); ISA §10 (a run that measured is not reversible) |
| `BD-E-RESIDUAL` | §12.4 | NS §3.2 (residual-poison validator) |
| `BD-E-INPLACE-NOT-INVERSE` | §8.7 | NS §3.1 ("an in-place update with no inverse fails loud at compile time") |
| `BD-E-COHERENT-OVERWRITE` | TDL-5(d) | NS §4.2 ("writing a register not known to be clean is a compile-time error … else it fails loud") |
| `BD-E-COHERENT-ANGLE` | TDL-10 | NS §4.2 (predication, not superposed parameters); ISA §3.1 ("angles are literals or classical arguments") |

**Deleted** from 0.1 (each was a narrowing, audit §1): `BD-E-EH`, `BD-E-LIFT-SUBSET`,
`BD-E-DEVICE-ADDRESS`, `BD-E-REGION-UNBOUNDED`, `BD-E-REGION-EXTERNAL`, `BD-E-REGION-THUNK`,
`BD-E-REGION-TIER`, `BD-E-REVERSIBLE-MARKER` (except measurement), `BD-E-INPLACE-UNVERIFIED`,
`BD-E-OPERAND-UNBOUNDED`, `BD-E-HANDLE-STORE`, and `BD-E-REGION-TYPE` for oracle candidates.

### 22.2 Blocker reports

`BD-B-ISA4` (BLK-1), `BD-B-ISA1` (BLK-2), `BD-B-ISA3` (BLK-3), `BD-B-ISA12` (BLK-4), in the
format of §25.1. A blocker report is not a rejection (§1.6).

### 22.3 Run-time traps

Fault code 4 (§17.5) with the named diagnostic: `T-DEAD`, `T-FOREIGN`, `T-CLEAN`, `T-INDEX`,
`T-ALIAS`, `T-THETA`, `T-MEASURE`, `T-SIZE`, `T-CTRL`, `T-LEAK`, `T-REGION`, `T-REGION-INVALID`,
`T-OP`, `T-CLASS`, `T-IFACE`, `T-BUDGET`, `T-TAINT-HOST`. Deleted: `T-BORROW` (outside generations
`qborrow` is a clean allocation, bd `.9`), `T-TIER` (§7.4).

### 22.4 Warnings

`BD-W-QSTORE-UNCLEAN` (§6.7), `BD-W-TAINT-HOST` (TDL-11), `BD-W-COHERENT-HISTORY` (TDL-7). A
warning never changes a verdict.

## 23. Versioning

- The **full version string** of this document (`0.2`) is the unit of compatibility: a plugin
  implements exactly one dialect version and targets exactly one ISA version (§19.9); drafts are
  not compatible with each other.
- Sub-artefacts, all at `0.2`: `markers` (§3), `handles` (§6), `regions` (§7), `oracle-abi` (§8),
  `tdl` (§10), `effects` (§11), `norm` (§12–§15; the certificate's `normaliser_version`), `map`
  (§16; the certificate's `dialect_mapping_version`), `asm` (§15), `platform` (§20), `driver`
  (§19), `corpus` (§21).
- Every semantic change bumps the version; the reference objects and hashes of §16 depend on the
  ISA version string, the map and the layout, and change with any of them (0.1's hashes changed
  with the wrapper form of §16.2).
- The build record (§19.9) records the runtimes, arith and asm-table hashes and the budget-table
  hash; `SPEC_VERSIONS.toml` records `dialect` and the targeted `isa`; the change rules are in
  `spec/README.md`.

## 24. Deferred mechanics (with defaults)

Only mechanics appear here. Each row states the capability it keeps; none has a default of
reject, refuse, fault or no effect for something the north star promises.

| Id | Mechanics | Default | Capability kept |
|---|---|---|---|
| D12 | host-stack addresses passed into device code (NS §3.2 "where possible") | executions they influence are layout-dependent (§18.7) and validated against the reference interpreter | every program runs; only the comparison oracle changes |
| D13 | a region key stable across LLVM majors (§7.3) | the key depends on the major, which the certificate records | identity within a link is by content |
| D15 | the comparison-link bases (§19.5) | `null_size` 4096, data at 4096, text at 0x400000 or above the device ranges, options to change them | native-equal addresses |
| D20 | single passes outside the envelope (§21.1) | unsupported unless listed (they are LLVM bugs, spike findings §2) | every envelope pipeline |
| D22 | output file names and diagnostic text | plugin-defined; the codes of §22 are normative | – |
| D23 | ThinLTO with the plugin | full LTO: one merged module | every program merges into one module (audit D23, M) |
| D24 | multi-threaded device code (NS §9.11) | the single-thread assumption (N9), recorded in the certificate | uniprocessor programs, rung 6's configurations |
| D26 | the binary layout of descriptors and budget records beyond the C view | the LLVM struct layout under the module's datalayout (§8.1, §9.1) | every target |
| D27 | budget defaults (§9.2) | 1048576 steps, 1048576 heap bytes, 65536 stack cells, depth 256, `sstack` 65536 | every budget is overridable |
| D28 | the in-place exhaustive width (§8.7) | 24 bits; sampled evidence and the `T-CLEAN` net above | every pair is verified, as proof or evidence |
| D29 | the static register-file size for unbounded sites (§6.5) | 64 instances, then the BLK-1 blocker trap | – (the case itself is a blocker) |
| D30 | further device models (ISA §17 item 3) | the four of ISA §7.3; another device's effect is `FAULT_EFFECT_UNMODELLED` until the ISA adds it | the four modelled devices in every tier |
| D31 | target ABI rows for `va_list` (§14.3), asm (§15) and target intrinsics beyond x86-64, AArch64 and RISC-V64 | added with the target | the three targets of the rungs |
| D32 | the platform row lists and board constants (§20) | the patterns of §20.2–§20.6 until the §20.7 spike | rungs 6 and 7 |
| D33 | `vscale` (§12.5) and the declared CPU model for `cpuid` (§15.2) | `vscale_range` minimum; the `cpuid` leaves of the build machine, recorded in the build record | scalable-vector and CPU-feature code |

## 25. Blockers and ISA items

### 25.1 Blockers

A **blocker** is a capability the dialect fully specifies whose stated case has no realisation on
ISA 0.8. No rung of NS §8 depends on any of them (outline part C). The maintainer ruled
(2026-10-29) that ISA 0.9 waits until this dialect is council-accepted.

| Id | Code | NS capability | Affected case | ISA 0.8 realisation that exists | Exact ISA change |
|---|---|---|---|---|---|
| **BLK-1** = ISA-4 | `BD-B-ISA4` | NS §3.1 handle tables; §4.1, §4.2 dynamic allocation ("real allocation"); Bennett.jl vectors of qubits; adjoints of generations whose register set is known only at run time | allocation sites whose handles reach memory with no finite instance bound (§6.5); register widths with value set ⊤ (§3.4); a Co width with an unbounded value set (TDL-10) | direct `qreg` values for handles that stay out of memory; static register files with dispatch for bounded sites (§6.5) | (i) a dynamic-width type `qreg[*]`; `q = qreg.new cls n` with n an `i64` value yields `qreg[*]`; `w = qreg.width q`. (ii) Binding a `qreg[*]` to a `wire[n]` or `region[A,W]` slot checks the width at the call: CC trap, R fault `FAULT_UB_TRAP`, on a mismatch. (iii) `id = qreg.id q` (non-consuming; the §10 launch id) and `q = qreg.from_id id` (yields `qreg[*]`; a trap if the id is not live, is viewed or is consumed). History frames: `qreg.id` is pure; `qreg.from_id` records the handle reference |
| **BLK-2** = ISA-1 | `BD-B-ISA1` | NS §4.2 "run-time budgets come from the host or from measurement results" | budget fields computed on the device (§9.5 case 3) | pre-minted finite sets; stub-minted copies of launch arguments (§9.5) | a CC instruction `tk = budget.mint @region s h st d` (`i64` operands) with the ISA §5.4 validation of `bennett_budget` as a CC trap; the token is scoped to the run; an impure history frame recording the token |
| **BLK-3** = ISA-3 | `BD-B-ISA3` | NS §3.1, §4.2 parametrised in-place updates x ← g(x; y, a) from a user-declared (g, ginv) pair with quantum or unbounded classical parameters | `inplace` with `IN` or `MEM_IN` bindings, or `ARG`s with value set ⊤ (§8.7) | `qinplace` without parameters; per-value specialisation for finite `ARG` sets; library bijections as permutation actions (§8.7, TDL-5b) | `qinplace @g @ginv tk x (ins..) (mem..) (args..)`: the ISA §4.5 macro passes the lists to both `oracle_call`s; the ISA §6.1 transfer becomes `x: perm with S_x ∪ ins ∪ cells(mem) ∪ Π`; certificate obligation g∘ginv = id for every (ins, mem, args) class (exhaustive or library) |
| **BLK-4** = new ISA-12 (audit B-38) | `BD-B-ISA12` | NS §4.2 quantum allocation inside reversible-tier code | `qalloc`/`qborrow`/`qfree` in an R closure with no finite instance bound (§7.5b); entry-state transfer from R code (§8.5) | hoisting to the CC caller with a static count (§7.5b) | permit `qreg.new`, `qreg.free`, `qreg.slice` and `qreg.concat` in R; the R history records them; the reversal of `qreg.new` is `qreg.free` with the cleanliness obligation (simulator check; hardware per ISA §17 item 14); the reversal of `qreg.free` is `qreg.new` (clean); `measure` stays CC-only |

**Blocker report** (one line per blocker point, in processing order, in the outputs, §19.9):
`<code> <function> <value or call>: <reason>; <ISA 0.8 constraint>; <BLK id> (<ISA item>) <change>`.

**Blocker trap.** A blocked program is compiled (§1.6) with each blocker point lowered to the ISA
0.8 realisation that exists for the bounded cases (the static file of §6.5 with D29's size, the
pre-minted budgets of the value set, the specialised pairs) and, on an execution that falls
outside them, `hostcall bennett.fault` with code 4 and the blocker's code as payload, then
`trap` (§11.5). So only the executions the blocker affects fail, and they fail loud.

### 25.2 Wording items

No capability is lost; two implementations could differ until each is fixed in ISA 0.9:

- **ISA-7**: a table from CC/R trap cause to ISA §5.4 code (division by zero 5, MIN/−1 6, memory 7,
  `trap` 4, allocation failure 2) and a CC/R `fault C` instruction. The dialect uses `hostcall
  bennett.fault` in CC meanwhile (§11.5).
- **ISA-8**: an R call returns a fault status to its CC caller; runs ending in an R fault are
  reverse-eligible.
- **ISA-3 editorial**: the JCS spelling of `args` types: the ISA §16.2 type spelling as JSON strings
  (`"i64"`), as §16 uses.
- **`qreg.slice`**: whether `lo` may be a run-time value (§10 TDL-4 uses literal offsets only).
- **`qreg` across CC calls**: ISA §3.2 places handles in the classical environment, but the ISA
  §3.3 transition table is silent on CC `call`, `ret` and `br` block parameters of `qreg` type;
  §6.5 relies on them carrying `qreg` values unchanged.
- **ISA §5.4 code 10** "(R only)" versus `fault 10` in oracles (§11.3; ISA §4.2 admits every C <
  2^F).
- **Certificate fields** for the build record hash (§19.9), the budget-table hash and the
  `deferred_measurement` flag (§7.5a); meanwhile `producer.version` build metadata and
  `definedness_assumptions` carry them.
- **ISA §12.2 domains with a fixed classical region**: NS §8 rung 4(a) verifies the oracle "over
  all rows and all target values" with the database fixed classically before entry; ISA §12.2
  labels a domain that fixes an `in` region's cells as evidence with a covered fraction. The ISA
  should say whether an exhaustive claim over the remaining components, with the fixed region
  prepared from classical bytes (`qprep`, `bennett_qreg_prepare`), is a proof for that region
  content.

### 25.3 Efficiency items

Correct on ISA 0.8 by the stated construction; ISA 0.9 candidates on evidence only:

| Item | Construction on ISA 0.8 |
|---|---|
| ISA-5 (two simultaneous slices of one `qreg`) | per-wire registers, or a quantum-addressed gate |
| ISA-9 (borrowing outside static Q regions) | clean allocation for CC-spanning borrows (§18.3) |
| ISA-11 (host memory by reference) | promotion (§19.4) |
| G-12 (oracle entry state at native addresses) | entry-state transfer by replay (§8.5) |
| G-13 (interface-region base at call time) | a static arena (TDL-4) |
| G-14 (predicated step machine in actions) | unrolled padded events (TDL-10) |
| G-15 (payloads wider than 128 bits) | 2k − 1 oracle calls (§8.6) |
| G-16 (fibers and interrupts in CC/R) | rewindable frames (§14.6) and poll points (§20.4) |
| SQLite E1–E5 | per-function cell widths, frame width, an indirect-call row, a block-copy row, a classical-content hint for `in` regions |

ISA-2 is not a gap (the R step counter, §17.6). ISA-6 is not a gap (`measure` and re-preparation,
§18.3). ISA-10 is settled by the ISA's test vectors. **LLVM changes needed**: none; the legality
findings' LLVM bugs are outside the envelope (§21.1).

## Appendix A. Changes from the ratified outline

The text follows `spec/outline-0.2.md` and its rulings. Where it departs, the reason is below;
every departure keeps or widens the capability the outline gives.

| # | Outline | This text | Reason |
|---|---|---|---|
| A1 | §8.6: k + 2 calls, cleaning each slice's fault bundle by `qxor` from a copy computed by a separate variant W_c | 2k − 1 calls: a copy-out pair per extra slice, issued as CC-level region calls (§8.6) | the outline's `qxor` cleanup is neither `reverse` nor `recompute` of the bundle's own computing sequence (ISA §6.2, §6.4), so as an action it would be ill-formed; the copy-out pair cleans its temporaries by the oracle's involution (ISA §5.2), checked by `qreg.free` (ISA §3.3) |
| A2 | §8.5: the snapshot register's release unspecified | released by `measure` (an unentangled basis state), kept while unchanged (§8.5) | a `qreg.free` needs a clean register and no ISA 0.8 instruction un-concatenates; the measurement is deterministic and disturbs nothing |
| A3 | §6.5: every root in a static register file; unbounded instance counts are BLK-1 | a handle that never reaches memory is a direct CC `qreg` value with no bound; BLK-1 only for memory-reaching sites without a reference bound (§6.5) | ISA 0.8's dynamic SSA instances already name unboundedly many registers; the blocker's case shrinks to what ISA 0.8 truly lacks |
| A4 | §6.5, §7.5(b): "statically bounded number of live instances", "static count" | an exact reference instance bound (self-disjoint sites, constant trip counts) (§6.5) | verdicts must not depend on a plugin's analysis precision |
| A5 | TDL-2: states Cl, Co | Cl, M (materialised, both copies valid), Co (§10) | materialising an object before a slice reads it would otherwise make it Co, and later classical reads would trap (`T-TAINT-HOST`) on classical data |
| A6 | TDL-3: slices outlined; stores in slices | slices never contain outliving stores or markers (those are events); each slice keeps a classical twin selected dynamically | the event forms of TDL-5 need the stores as events; the twin avoids slice cost when the data is classical at run time |
| A7 | TDL-5(a), Co value: XOR v, then `xmask c`, then uncompute | one XOR of the mask c ⊕ v (c a classical argument of the slice) | equal effect, one event fewer |
| A8 | TDL-5(a)/§18: "the uncompute is valid (ISA §6.2)" | events are applied as CC-level region calls with dynamic cleanliness checks; a static ISA action only when it satisfies ISA §6 (§18.2) | ISA §6.1 makes an oracle's value depend on every cell of a region it reads, so a static action cannot uncompute a slice after writing any arena cell; at CC level the uncompute is exact because the slice does not read the written cells |
| A9 | TDL-8: combine into Φ; plugin register when null | per-slice fault registers retained and combined by `@firstfault`; in `compute`, copied between E_f and E_use (TDL-8) | the uncomputing call XORs the code out again, and in `compute` adjoint(E_f) would erase f's faults |
| A10 | TDL-12: Co effects follow §11.3, else F(8) | every effect in an action region is `fault 8` (TDL-12) | action regions have no descriptor, so no device model is bound to them; an effect in G under control is the same coherence problem as a store |
| A11 | TDL-7: history freed by the scheduler | history that cannot be cleaned inside the invocation is a declared output, reported (`BD-W-COHERENT-HISTORY`) and measured at the epilogue | an action must return workspace clean (ISA §5.3); NS §4.2's padded unitary on declared wires |
| A12 | §3.1: primitive `__bennett_nz_fault` | also `__bennett_nz_alloc`, `__bennett_nz_free`; reserved-name rules apply to producer inputs (§3.1) | the runtimes allocator must reach `lift.alloc`/`alloc`; runtimes bitcode uses reserved names |
| A13 | §3.8: a `@cfunction` constant "resolves whenever the body is in the link" | it is dispatched by value and traps unless it equals some A(F) (§3.8, §5.2) | A(F) is fixed by the comparison link after the analysis, and a Julia-process address never equals it; Bennett.jl's `ptr @f` route keeps the capability (audit B-14) |
| A14 | §7.2: thunk resolution as 0.1 C1 (a cycle is `BD-E-REGION-THUNK`) | a thunk on a cycle resolves to itself; the code is deleted | a rejection with no NS clause behind it |
| A15 | §12.2: N1–N35 | adds N0 (LLVM's own lowering passes for coroutines, matrices, type tests, profiling, alloc tokens, guards) and extends N10, N11 | the completeness obligation: those families are defined by LLVM through those passes |
| A16 | §12.2 N34: "point marks only" | marks are `!bennett.rstep` metadata, exempt from N3 and V2 | a mark must survive normalisation |
| A17 | §16: the wrapper form | `@ref` always calls the region function's lproc; every reference object has a layout; layout rules of §16.3 (closure-reachable globals; A_tab so that table overflow never precedes heap exhaustion) | recursion of the region function itself, and an identity that does not change with unrelated globals |
| A18 | §16.4: compare-tree blocks | names `^b<i>.s<j>` in creation order and `^b<i>.q<q>c<k>`/`d`/`r` for indirect calls | deterministic text and hashes |
| A19 | – | §14.9 `blockaddress`/`indirectbr`, §13.1 all seven formats in one table, §14.7 `exit` from a CC device entry by `hostcall bennett.exit`, §8.7 B_min and `T-BUDGET` | outline B1 ("all of materialised LLVM") and run-time budgets for in-place pairs |
| A20 | §25: wording items | adds certificate fields (build record, budget table, deferred measurement) and ISA §12.2 domains with a fixed classical region | NS §0, §5.1 require them in the certificate; NS §8 rung 4(a) is such a domain |
| A21 | §20.1 `__bennett_platform_ram` | `__bennett_rt_platform_ram` | the reserved-prefix rule of §3.1 |
| A22 | §21: corpus cases for the changed signatures | `spec-sem2-*` added beside the 0.1-ABI `spec-sem-*` | the trace runtime is still at ABI v0 (bd `-566`); the old cases stay valid legality cases |
| A23 | §12.1: rules in table order | table order except that N33 runs immediately before N32 (§12.1) | the `fpext`/`fptrunc` pairs N33 creates around libm calls are floating point that N32 must rewrite |

## Appendix B. Example index

Every checked example, the rules it exercises, and the checker capability (§1.5) and executor it
needs. "isa-ref" is the Rust ISA reference interpreter `bennett-isa-ref` (`check`, `hash`,
`run-oracle`, `step-check` exist; `run-cc`, `reverse`, `run-action`, `run-program` are requested,
bd `b-isa-spec-xam`); "trace" needs the trace runtime at ABI 0.2 (bd `-566`); Python capabilities
compute expected artefacts only (P-3).

| Examples | Rules | Capability | Executor |
|---|---|---|---|
| `markers-ir`, `markers-c` | §3.2, §3.3 | parse, header | LLVM 18/20/23, clang 18/20/23 |
| `operand-phi-codes`, `operand-code-table`, `operand-runtime-op`, `operand-bad-code`, `operand-class`, `operand-width-masked`, `operand-width-host` (+ blocker) | §3.4, §5.3, PT5, PT6, BLK-1 | parse, recognise | LLVM; Python recogniser |
| `recog-*` (8) | §3.1, §3.5 | parse, recognise | LLVM; Python |
| `attr-*` (4) | §3.6 | parse, recognise | LLVM; Python |
| `unwind-invoke` | §3.7 | parse, recognise | LLVM; Python |
| `julia-jlplt`, `effect-lie` | §3.8 | parse, recognise | LLVM; Python |
| `pt-variable-index` | §5.1, PT1, PT2, PT6, PT7 | parse, recognise | LLVM; Python |
| `handle-*` (20, incl. 1 blocker) | §6.2–§6.6, PT3, PT4, PT8–PT11, BLK-1 | parse, recognise | LLVM; Python |
| `qstore-twice` | §6.7 | parse, recognise | LLVM; Python |
| `region-*` (18, incl. 1 blocker) | §7.1–§7.5, BLK-4 | parse, recognise | LLVM; Python |
| `oracle-inc8`, `oracle-two-in`, `oracle-two-shapes`, `oracle-wide-out`, `budget-launch-arg`, `budget-device-computed` (+ blocker) | §8.1–§8.6, §9.1, §9.5, BLK-2 | parse, recognise | LLVM; Python |
| `inplace-*` (4, incl. 1 blocker) | §8.7, BLK-3 | parse, recognise, run-oracle | LLVM; Python; isa-ref `run-oracle` (verification) |
| `budget-table=rung4-mini` | §9.2 | driver | Python |
| `tdl`, `tdl-overwrite`, `tdl-effect`, `tdl-angle` with `tdl=` and `state=` blocks | TDL-1–TDL-12, §18.2–§18.4 | parse, recognise, tdl, run-action | LLVM; Python TDL; isa-ref `run-action` (requested) |
| `effect-console-r`, `effect-console-cc` | §11.1, §11.2 | parse, recognise, run-cc, reverse | isa-ref `run-cc`, `reverse` (requested) |
| `n-flags`, `n-shift`, `n-undef`, `n-query`, `n-trap` | N1–N8, N10, N11, N14 | parse, normalise | LLVM; Python normaliser |
| `n-vector`, `n-wideint`, `n-shadow-stack`, `n-memintrinsics`, `n-intrinsics`, `n-atomic` with `native=` | N9, N21, N22, N24, N26, N27 | parse, normalise, native | LLVM; Python; clang + seeds |
| `residual-nsw`, `residual-clean` | §12.4 V1 | validate | Python |
| `n-fmuladd` (+ `native=`), `n-fp80`, `n-libm` | N16, N32, N33, §13 | parse, normalise, native | LLVM; Python; clang + seeds |
| `indirect-table`, `indirect-host-pointer` | §14.2 | parse, recognise | LLVM; Python |
| `n-varargs` (+ `native=`) | N23, §14.3, N24 | parse, normalise, native | LLVM; Python; clang + seeds |
| `n-eh` (+ `native=`) | N28, §14.4 | parse, normalise, native | LLVM; Python; clang++ and clang + seeds |
| `sjlj-two-frames`, `fiber-pingpong`, `exit-status` with `cc-run=` | N29, N30, §14.5–§14.7, §19.2 | frontend, run-cc, reverse | clang; isa-ref `run-cc`, `reverse` (requested); native status computed |
| `asm-musl-syscall`, `n-asm` | N31, §15.5 | parse, recognise, normalise | LLVM; Python |
| `inc8`, `add2`, `rung4-mini`, `rung8-mini`, `listsum`, `switch5`: `lift=`, `linkmap=`, `object=`, `hash=`, `run=`, `step-check=` | §16.1–§16.5, §8.2 (IN, ARG, MEM_IN), §8.3 (ENTROPY), §9.4, §11.3, §14.2, §16.4 rows (memory, calls, recursion, alloc/free, phis, dispatch, switch) | map, check, hash, run-oracle, step-check | Python map; isa-ref `check`, `hash`, `run-oracle`, `step-check` |
| `rung4-minidb`, `rung4-grover-tu` (+ `native=rung4-mini`) | §3.3, §8, §16.7 | frontend, recognise, native | clang 18/20/23; Python; clang native |
| `sem2-ctrl`, `sem2-adj`, `sem2-compute` with `events=`, `state=` | §18.3, §18.4 | trace, run-action | trace runtime (ABI 0.2 needed for `adj` and `compute`); isa-ref `run-action` (requested) |
| `version-flag` | §19.9 | parse, recognise | LLVM; Python |

**Rule ids without an example yet** (the check fails on them, P-1, until examples land): N0, N12,
N15, N25, N34, N35; V2–V16; PT12; the `OUT` binding's object (`oracle-wide-out` is recognised
only), the BLOCK, CLOCK and CONSOLE device bindings, entry-state transfer (§8.5), `indirectbr`
(§14.9), §19.3–§19.8 (driver modes beyond §19.2), §20 (platform). Each is a task for the next
editing round (bd).

## Appendix C. Generic intrinsics of LLVM 18, 20 and 23

The completeness obligation of §12.2: every generic (target-independent) intrinsic name that
LLVM 18, 20 or 23 defines (546 names, from each major's `IntrinsicEnums.inc`, with the target
families `aarch64 amdgcn arm bpf dx hexagon loongarch mips nvvm ppc r600 riscv s390 spv ve wasm
x86 xcore` excluded; those are §15.4), with the rule that removes or realises it. A name defined
only by some majors carries them in brackets. None is `trapped`.

| Rule | Count | Intrinsics |
|---|---|---|
| N0: the coroutine passes | 38 | `coro.align`, `coro.alloc`, `coro.alloca.alloc`, `coro.alloca.free`, `coro.alloca.get`, `coro.async.context.alloc`, `coro.async.context.dealloc`, `coro.async.resume`, `coro.async.size.replace`, `coro.await.suspend.bool`[20,23], `coro.await.suspend.handle`[20,23], `coro.await.suspend.void`[20,23], `coro.begin`, `coro.begin.custom.abi`[20,23], `coro.dead`[23], `coro.destroy`, `coro.done`, `coro.end`, `coro.end.async`, `coro.end.results`, `coro.frame`, `coro.free`, `coro.id`, `coro.id.async`, `coro.id.retcon`, `coro.id.retcon.once`, `coro.is_in_ramp`[23], `coro.noop`, `coro.prepare.async`, `coro.prepare.retcon`, `coro.promise`, `coro.resume`, `coro.save`, `coro.size`, `coro.subfn.addr`, `coro.suspend`, `coro.suspend.async`, `coro.suspend.retcon` |
| N0: `lower-matrix-intrinsics` | 4 | `matrix.column.major.load`, `matrix.column.major.store`, `matrix.multiply`, `matrix.transpose` |
| N0: `lowertypetests` | 5 | `icall.branch.funnel`, `public.type.test`, `type.checked.load`, `type.checked.load.relative`, `type.test` |
| N0: `instrprof` | 9 | `instrprof.callsite`[20,23], `instrprof.cover`, `instrprof.increment`, `instrprof.increment.step`, `instrprof.mcdc.condbitmap.update`[18], `instrprof.mcdc.parameters`, `instrprof.mcdc.tvbitmap.update`, `instrprof.timestamp`, `instrprof.value.profile` |
| N0: `alloc-token` | 1 | `alloc.token.id`[23] |
| N0: `lower-guard-intrinsic`, `lower-widenable-condition` | 2 | `experimental.guard`, `experimental.widenable.condition` |
| N5: deleted | 32 | `asan.check.memaccess`, `assume`, `clear_cache`, `codeview.annotation`, `dbg.assign`, `dbg.declare`, `dbg.label`, `dbg.value`, `donothing`, `eh.unwind.init`, `experimental.convergence.anchor`, `experimental.convergence.entry`, `experimental.convergence.loop`, `experimental.noalias.scope.decl`, `experimental.stackmap`, `fake.use`[20,23], `hwasan.check.memaccess`, `hwasan.check.memaccess.fixedshadow`[20,23], `hwasan.check.memaccess.shortgranules`, `hwasan.check.memaccess.shortgranules.fixedshadow`[20,23], `pcmarker`, `prefetch`, `pseudoprobe`, `reloc.none`[23], `seh.scope.begin`, `seh.scope.end`, `seh.try.begin`, `seh.try.end`, `sideeffect`, `var.annotation`, `xray.customevent`, `xray.typedevent` |
| N5: operand 0 | 15 | `annotation`, `arithmetic.fence`, `expect`, `expect.with.probability`, `launder.invariant.group`, `protected.field.ptr`[23], `ptr.annotation`, `ptrauth.auth`, `ptrauth.auth.with.pc.and.resign`[23], `ptrauth.resign`, `ptrauth.sign`, `ptrauth.strip`, `ssa.copy`, `strip.invariant.group`, `threadlocal.address` |
| N6: deleted | 4 | `invariant.end`, `invariant.start`, `lifetime.end`, `lifetime.start` |
| N10: a constant | 10 | `allow.runtime.check`[20,23], `allow.sanitize.address`[23], `allow.sanitize.hwaddress`[23], `allow.sanitize.memory`[23], `allow.sanitize.thread`[23], `allow.ubsan.check`[20,23], `get.dynamic.area.offset`, `is.constant`, `objectsize`, `vscale` |
| N11 | 5 | `cond.loop`[23], `debugtrap`, `looptrap`[23], `trap`, `ubsantrap` |
| N16, then N32 | 1 | `fmuladd` |
| N21 (§12.6), then N27/N32 per lane | 161 | `experimental.cttz.elts`, `experimental.get.vector.length`, `experimental.stepvector`[18], `experimental.vector.compress`[20,23], `experimental.vector.deinterleave2`[18], `experimental.vector.extract.last.active`[20,23], `experimental.vector.histogram.add`[20,23], `experimental.vector.histogram.uadd.sat`[23], `experimental.vector.histogram.umax`[23], `experimental.vector.histogram.umin`[23], `experimental.vector.interleave2`[18], `experimental.vector.match`[20,23], `experimental.vector.partial.reduce.add`[20], `experimental.vector.reverse`[18], `experimental.vector.splice`[18], `experimental.vp.reverse`, `experimental.vp.splat`[20], `experimental.vp.splice`, `experimental.vp.strided.load`, `experimental.vp.strided.store`, `get.active.lane.mask`, `loop.dependence.raw.mask`[23], `loop.dependence.war.mask`[23], `masked.compressstore`, `masked.expandload`, `masked.gather`, `masked.load`, `masked.scatter`, `masked.sdiv`[23], `masked.srem`[23], `masked.store`, `masked.udiv`[23], `masked.urem`[23], `stepvector`[20,23], `vector.deinterleave2`[20,23], `vector.deinterleave3`[23], `vector.deinterleave4`[23], `vector.deinterleave5`[23], `vector.deinterleave6`[23], `vector.deinterleave7`[23], `vector.deinterleave8`[23], `vector.extract`, `vector.insert`, `vector.interleave2`[20,23], `vector.interleave3`[23], `vector.interleave4`[23], `vector.interleave5`[23], `vector.interleave6`[23], `vector.interleave7`[23], `vector.interleave8`[23], `vector.partial.reduce.add`[23], `vector.partial.reduce.fadd`[23], `vector.reduce.add`, `vector.reduce.and`, `vector.reduce.fadd`, `vector.reduce.fmax`, `vector.reduce.fmaximum`, `vector.reduce.fmin`, `vector.reduce.fminimum`, `vector.reduce.fmul`, `vector.reduce.mul`, `vector.reduce.or`, `vector.reduce.smax`, `vector.reduce.smin`, `vector.reduce.umax`, `vector.reduce.umin`, `vector.reduce.xor`, `vector.reverse`[20,23], `vector.splice`[20], `vector.splice.left`[23], `vector.splice.right`[23], `vp.abs`, `vp.add`, `vp.and`, `vp.ashr`, `vp.bitreverse`, `vp.bswap`, `vp.ceil`, `vp.copysign`, `vp.ctlz`, `vp.ctpop`, `vp.cttz`, `vp.cttz.elts`[20,23], `vp.fabs`, `vp.fadd`, `vp.fcmp`, `vp.fdiv`, `vp.floor`, `vp.fma`, `vp.fmul`, `vp.fmuladd`, `vp.fneg`, `vp.fpext`, `vp.fptosi`, `vp.fptoui`, `vp.fptrunc`, `vp.frem`, `vp.fshl`, `vp.fshr`, `vp.fsub`, `vp.gather`, `vp.icmp`, `vp.inttoptr`, `vp.is.fpclass`, `vp.llrint`[20,23], `vp.load`, `vp.load.ff`[23], `vp.lrint`[20,23], `vp.lshr`, `vp.maximum`, `vp.maxnum`, `vp.merge`, `vp.minimum`, `vp.minnum`, `vp.mul`, `vp.nearbyint`, `vp.or`, `vp.ptrtoint`, `vp.reduce.add`, `vp.reduce.and`, `vp.reduce.fadd`, `vp.reduce.fmax`, `vp.reduce.fmaximum`[20,23], `vp.reduce.fmin`, `vp.reduce.fminimum`[20,23], `vp.reduce.fmul`, `vp.reduce.mul`, `vp.reduce.or`, `vp.reduce.smax`, `vp.reduce.smin`, `vp.reduce.umax`, `vp.reduce.umin`, `vp.reduce.xor`, `vp.rint`, `vp.round`, `vp.roundeven`, `vp.roundtozero`, `vp.sadd.sat`[20,23], `vp.scatter`, `vp.sdiv`, `vp.select`, `vp.sext`, `vp.shl`, `vp.sitofp`, `vp.smax`, `vp.smin`, `vp.sqrt`, `vp.srem`, `vp.ssub.sat`[20,23], `vp.store`, `vp.sub`, `vp.trunc`, `vp.uadd.sat`[20,23], `vp.udiv`, `vp.uitofp`, `vp.umax`, `vp.umin`, `vp.urem`, `vp.usub.sat`[20,23], `vp.xor`, `vp.zext` |
| N23 (§14.3) | 3 | `va_copy`, `va_end`, `va_start` |
| N24 (§17.3) | 14 | `addressofreturnaddress`, `eh.dwarf.cfa`, `eh.recoverfp`, `frameaddress`, `localaddress`, `localescape`, `localrecover`, `returnaddress`, `sponentry`, `stackaddress`[23], `stackrestore`, `stacksave`, `structured.alloca`[23], `swift.async.context.addr` |
| N25 | 3 | `call.preallocated.arg`, `call.preallocated.setup`, `call.preallocated.teardown` |
| N26 | 9 | `experimental.memset.pattern`[20,23], `memcpy`, `memcpy.element.unordered.atomic`, `memcpy.inline`, `memmove`, `memmove.element.unordered.atomic`, `memset`, `memset.element.unordered.atomic`, `memset.inline` |
| N27 (§12.8) | 105 | `abs`, `adjust.trampoline`, `bitreverse`, `bswap`, `clmul`[23], `ctlz`, `ctpop`, `cttz`, `experimental.deoptimize`, `experimental.gc.get.pointer.base`, `experimental.gc.get.pointer.offset`, `experimental.gc.relocate`, `experimental.gc.result`, `experimental.gc.statepoint`, `experimental.patchpoint`[20,23], `experimental.patchpoint.i64`[18], `experimental.patchpoint.void`, `fshl`, `fshr`, `gcread`, `gcroot`, `gcwrite`, `init.trampoline`, `load.relative`, `loop.decrement`, `loop.decrement.reg`, `objc.arc.annotation.bottomup.bbend`, `objc.arc.annotation.bottomup.bbstart`, `objc.arc.annotation.topdown.bbend`, `objc.arc.annotation.topdown.bbstart`, `objc.autorelease`, `objc.autoreleasePoolPop`, `objc.autoreleasePoolPush`, `objc.autoreleaseReturnValue`, `objc.claimAutoreleasedReturnValue`[23], `objc.clang.arc.noop.use`, `objc.clang.arc.use`, `objc.copyWeak`, `objc.destroyWeak`, `objc.initWeak`, `objc.loadWeak`, `objc.loadWeakRetained`, `objc.moveWeak`, `objc.release`, `objc.retain`, `objc.retain.autorelease`, `objc.retainAutorelease`, `objc.retainAutoreleasedReturnValue`, `objc.retainAutoreleaseReturnValue`, `objc.retainBlock`, `objc.retainedObject`, `objc.storeStrong`, `objc.storeWeak`, `objc.sync.enter`, `objc.sync.exit`, `objc.unretainedObject`, `objc.unretainedPointer`, `objc.unsafeClaimAutoreleasedReturnValue`, `pdep`[23], `pext`[23], `preserve.array.access.index`, `preserve.static.offset`, `preserve.struct.access.index`, `preserve.union.access.index`, `ptrauth.blend`, `ptrauth.resign.load.relative`[23], `ptrauth.sign.generic`, `ptrmask`, `read_register`, `read_volatile_register`, `sadd.sat`, `sadd.with.overflow`, `scmp`[20,23], `sdiv.fix`, `sdiv.fix.sat`, `set.loop.iterations`, `smax`, `smin`, `smul.fix`, `smul.fix.sat`, `smul.with.overflow`, `sshl.sat`, `ssub.sat`, `ssub.with.overflow`, `stackguard`, `stackprotector`, `start.loop.iterations`, `test.set.loop.iterations`, `test.start.loop.iterations`, `thread.pointer`, `uadd.sat`, `uadd.with.overflow`, `ucmp`[20,23], `udiv.fix`, `udiv.fix.sat`, `umax`, `umin`, `umul.fix`, `umul.fix.sat`, `umul.with.overflow`, `ushl.sat`, `usub.sat`, `usub.with.overflow`, `write_register`, `write_volatile_register`[23] |
| N28 (§14.4) | 5 | `eh.exceptioncode`, `eh.exceptionpointer`, `eh.return.i32`, `eh.return.i64`, `eh.typeid.for` |
| N29 (§14.5) | 6 | `eh.sjlj.callsite`, `eh.sjlj.functioncontext`, `eh.sjlj.longjmp`, `eh.sjlj.lsda`, `eh.sjlj.setjmp`, `eh.sjlj.setup.dispatch` |
| N31 (§15.2) | 1 | `callbr.landingpad` |
| N31 (§15.2): the clock model | 2 | `readcyclecounter`, `readsteadycounter`[20,23] |
| N33 (§13.4): runtimes libm | 21 | `acos`[20,23], `asin`[20,23], `atan`[20,23], `atan2`[20,23], `cos`, `cosh`[20,23], `exp`, `exp10`, `exp2`, `log`, `log10`, `log2`, `modf`[23], `pow`, `powi`, `sin`, `sincos`[20,23], `sincospi`[23], `sinh`[20,23], `tan`[20,23], `tanh`[20,23] |
| N33 (§13.5) | 49 | `experimental.constrained.acos`[20,23], `experimental.constrained.asin`[20,23], `experimental.constrained.atan`[20,23], `experimental.constrained.atan2`[20,23], `experimental.constrained.ceil`, `experimental.constrained.cos`, `experimental.constrained.cosh`[20,23], `experimental.constrained.exp`, `experimental.constrained.exp2`, `experimental.constrained.fadd`, `experimental.constrained.fcmp`, `experimental.constrained.fcmps`, `experimental.constrained.fdiv`, `experimental.constrained.floor`, `experimental.constrained.fma`, `experimental.constrained.fmul`, `experimental.constrained.fmuladd`, `experimental.constrained.fpext`, `experimental.constrained.fptosi`, `experimental.constrained.fptoui`, `experimental.constrained.fptrunc`, `experimental.constrained.frem`, `experimental.constrained.fsub`, `experimental.constrained.ldexp`, `experimental.constrained.llrint`, `experimental.constrained.llround`, `experimental.constrained.log`, `experimental.constrained.log10`, `experimental.constrained.log2`, `experimental.constrained.lrint`, `experimental.constrained.lround`, `experimental.constrained.maximum`, `experimental.constrained.maxnum`, `experimental.constrained.minimum`, `experimental.constrained.minnum`, `experimental.constrained.nearbyint`, `experimental.constrained.pow`, `experimental.constrained.powi`, `experimental.constrained.rint`, `experimental.constrained.round`, `experimental.constrained.roundeven`, `experimental.constrained.sin`, `experimental.constrained.sinh`[20,23], `experimental.constrained.sitofp`, `experimental.constrained.sqrt`, `experimental.constrained.tan`[20,23], `experimental.constrained.tanh`[20,23], `experimental.constrained.trunc`, `experimental.constrained.uitofp` |
| N33 (§13.5): the fenv state | 8 | `get.fpenv`, `get.fpmode`, `get.rounding`, `reset.fpenv`, `reset.fpmode`, `set.fpenv`, `set.fpmode`, `set.rounding` |
| §13.1: bit-exact, unchanged | 2 | `copysign`, `fabs` |
| N32 (§13.1): soft-float | 30 | `canonicalize`, `ceil`, `convert.from.arbitrary.fp`[23], `convert.from.fp16`[18,20], `convert.to.arbitrary.fp`[23], `convert.to.fp16`[18,20], `floor`, `fma`, `fptosi.sat`, `fptoui.sat`, `fptrunc.round`, `frexp`, `is.fpclass`, `ldexp`, `llrint`, `llround`, `lrint`, `lround`, `maximum`, `maximumnum`[20,23], `maxnum`, `minimum`, `minimumnum`[20,23], `minnum`, `nearbyint`, `rint`, `round`, `roundeven`, `sqrt`, `trunc` |
| §16.4: `getelementptr` | 1 | `structured.gep`[23] |

Total: 546 names (the `llvm.` prefix is omitted above).
