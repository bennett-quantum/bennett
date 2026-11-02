# Council

You are the Muse seat of the Bennett council, grading the document below, acceptance dossier batch 2 (Muse seat, advisor R9): 17 contract proposals accepted by sol and astra incl. the bennett-4ht check: lpe, xv4, checker-native-model, checker-resource-contexts, 0jq, 4ta, 7s0, v2v, ysw, 2cg (dialect), l2p (0.10), checker-fault-rate, fd0 (0.10), pe1, 2qc, sqr, 4yg.1 (dialect). The document is a dossier of 17 contract-repair proposals (lpe, xv4, checker-native-model, checker-resource-contexts, 0jq, 4ta, 7s0, v2v, ysw, 2cg, l2p, checker-fault-rate, fd0, pe1, 2qc, sqr, 4yg.1) that the two other members (sol, astra) have each accepted in their latest round, including the bennett-4ht mixed-fat-object check. This is the final acceptance seat before the spec editor applies them. Grade EACH proposal independently, meaning its proposed spec diff and the claims supporting it, against the rubric on the absolute scale. The published specs are accepted text and are not under review, except where a diff interacts with them. Be exacting and skeptical. Verify every technical premise against your own knowledge and against the actual spec text. Name any premise that is false, including a misquoted or misnumbered clause. Do not defer to the other members' acceptance; their outputs are available for reference only.

Your workspace is `bennett-isa-spec` (read-only). Each dossier part names the spec it amends: the ISA text is `spec/Bennett-ISA-Spec-0.9.md`; dialect proposals amend `../bennett-dialect-spec/spec/`. They are NOT attached because of their size: read the clauses each proposal cites and every clause its diff touches before grading. Other files you can read:
- `docs/notes/` holds the proposal notes of 2026-11-02 and `docs/notes/2026-11-02-contract-verification.md`, the author's verification index with reproduction scripts.
- `reference-interpreter/` is the reference interpreter; `.beads/issues.jsonl` holds the cited beads.
- `../bennett/docs/Bennett-NorthStar.md` is the north star, also attached below.
- `../bennett/docs/council/<run>/round-<N>/` (run named in each part) hold the earlier rounds on these proposals, with both members' outputs; `isa-09-k82-2026-11-01` is K82.

A blocking issue is one that would make the project build the wrong thing if a diff were applied as written, or if it were left unapplied while its defect is real. Everything else is a suggestion. Prefix every blocking `id` with the proposal id (e.g. `lpe-M1`, `2cg-M1`); a block reopens only that proposal. Return `accept` only if the blocking list is empty for all 17. The `summary` must begin with one line per proposal of the form `<id>: ACCEPT` or `<id>: BLOCK (<blocking ids>)`. `accept` for a proposal means the editor may apply its diff (with your suggestions at their discretion) through the publication route the proposal states (a 0.9 K repair, or the 0.10 release where the proposal says so). Do not block on the route itself unless it would make two conformant implementations of the same declared version compute different results.

Be constructive, always. The editor must be able to act on your output without asking you anything. For every blocking issue, the `fix` field must give the section; the sentence or rule the diff should state (write it out); and where an example is involved, the corrected example or expected value. Each blocking item carries either `steps` (step 1 the spec clause, a later step a reproducible witness) or a precise `problem`, and a `kind`: `implementation` when the proposal's diff is wrong, `spec-gap` when the spec is silent in a way the proposal does not repair. Where two viable ways out exist, name both and say which you would take. Every `suggestions` entry follows the same rule; prefix suggestions with the proposal id too. In `path_to_accept`, state per blocked proposal the minimal ordered set of changes that would make you accept it; if you accept all, say what would raise the lowest-scoring criterion by one point. Score criteria for the dossier as a whole (the lowest-scoring proposal sets each score).

Answer only with JSON matching the schema.

Convergence rules for this council (read before grading):
1. Blocking means S0 only. That is any one of:
   - two conformant implementations built from the amended text would compute different results;
   - the semantics is unsound or self-contradictory;
   - a normative decision needed to build is missing;
   - the amended text narrows north-star scope. This means it rejects, refuses, faults, declares inert or omits a capability the north star promises, including any rung of its demo ladder. It counts even when the narrowing is disclosed, labelled deferred or given a default; a default only closes an S1 item if it keeps the capability.

   Also block if the note claims a defect that does not exist in the cited text, or claims that existing text covers something it does not. Tag every blocking issue with `scope`:
   - `core` = machine model, instruction set, regions, validity, memory, formal model, examples;
   - `contract` = targets, objects/identity, launch, scheduling, certificate, coverage, grammar.

   S1 items (an implementer would have to choose, but any choice yields a conformant machine) belong in `suggestions`.
2. Implementation will expose frictions; that is expected and acceptable. Do not block on field-level completeness of C headers, JSON schemas, numerical procedures or encodings when the normative obligation is stated and a default is given. List such gaps as suggestions. Do block on anything that would make an executor, checker or scheduler compute a different function or verdict.
3. This is the acceptance seat for these proposals. Leave `previous_status` and `regressions` empty.
4. Give `verdict_core` (accept/revise/reject) for the core scope alone, and `verdict` for the whole proposal.
5. Check hash and catalog claims: if the note says no canonical bytes or hashes change, verify that the diff really leaves them unchanged. If they do change, the note must say so and say how consumers move.
6. Formal correctness is pursued after practical revisions: correct *statements* with explicit hypotheses are required, proofs are not. Demands for proof formats, mechanisation or checker algorithms are S1 as long as the obligation and a default procedure are stated.


Blocking items: `steps` are optional; use them (3 to 6 objects {"n": "<1>1", "claim": "...", "by": "..."}) for implementation findings with a reproducible witness, else give a free-text `problem`; leave the other empty.
Steps: <1>1 what the spec requires (`by`: `clause:<ID>` or `ASSUMED: <why the spec is silent>`); <1>2 what the implementation does (`witness:<path or command>`); <1>3 an input where they differ; last step cites earlier ones (`step:<1>1`).
`OPEN: <what is missing>` marks an unjustified step; several `by` parts are separated by `; `.
If the spec is silent (step 1 or `problem` begins `ASSUMED:`) set `kind` to `spec-gap` (otherwise `implementation`); a spec gap goes to the spec owner,
is not an editor blocker and does not count against `accept`.


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

### Standing check: the mixed fat object stays reachable (maintainer 2026-11-02, bennett-4ht)
Apply to every ISA and dialect round, under C7. Does this contract change keep the mixed fat object reachable (native host binary + only marked modules as VM ISA objects, north star §2, §3.3, §4.4; bennett-4ht)? A change that decides object format, certificate layout, launch API, budgets, handle representation, effect tape or host memory by reference must state how a mixed fat object would use it or name the exact change needed; nothing may assume the device object is the whole binary (entry points, argv/envp, libc closure, native comparison, certificate inventory). Silence on these topics is a revise. Report a failure of this check as a blocking item (scope `contract`, unless the change is core) whose `fix` names the statement the document must add; return `revise`, never `accept`, while it stands. The check asks only that the fat object stays reachable. It does not ask for the launch ABI or a host shim to be implemented now.

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

**Shape of a blocking item.** `steps` are optional (a free-text `problem` is also accepted; steps are preferred for
implementation findings with a reproducible witness). When given they are 3 to 6 numbered steps
`{"n": "<1>1", "claim": "...", "by": "..."}`. Step 1 is what the spec requires (`by`
starts with `clause:<ID>`, a clause or section id from the clause graph, or with
`ASSUMED: <why the spec is silent>`); then what the document or implementation does, with a `witness:<path or
command>` that reproduces it; then an input on which the two differ; the last step is the
conclusion, citing earlier steps with `step:<n>`. `OPEN: <what is missing>` marks a step you
cannot justify. If step 1 is `ASSUMED:` the item is a spec gap: set `"kind": "spec-gap"`; it is
reported to the spec owner and is neither an editor blocker nor counted against `accept`.
The `fix` field is unchanged.


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


# Background (not graded): `fat-object-scope.md`

# Mixed fat object — shared contract scope

Proposal for every revision in this directory; not a published ISA amendment.
Clause references are to [ISA 0.9](../../../spec/Bennett-ISA-Spec-0.9.md),
[the North Star](../../../../bennett/docs/Bennett-NorthStar.md), and, where
qualified, the maintained dialect 0.2/0.3 texts. This is the shared statement
required by bennett-4ht and the council rubric's standing mixed-fat-object check.

## Citable scoping statement

> A mixed fat object retains an ordinary native host binary and embeds ISA
> objects for marked device modules and their linked device closures (North
> Star §§2, 3.3, 4.4). ISA §§9.1–9.3 identify each device object and selected
> root; §12.3 certificates, owner records and reports cover that closure,
> with a separate binding/context set per device root and [] relative to
> that root (§12.1). Native entry, argv/envp and host-only libc need no ISA
> region, frame or certificate record; native comparison binds the selected
> materialised closure, not the whole host. Today §10 launches a device CC
> entry with copied arguments/entropy; §5.4 budgets bind device invocations,
> §3.3/§10 handles belong to a loaded program/run, and §7.3/§10 tapes cover
> device R effects. These require explicit container-to-object/root/certificate
> association, host-entry-to-device-entry bindings, budget/handle lifetime
> negotiation and tape/run association in a versioned mixed-launch contract.
> ISA §7.1 defines device memory but §10 defines no general host-memory-by-reference
> launch ABI: that contract must add address/layout mapping, range/liveness,
> aliasing, ownership/synchronisation, writeback and reversal rules, preserving
> dialect §§6.6, 8.5, 19.4–19.5. Until published, these are explicit
> bennett-4ht boundary obligations, not grounds to require whole-binary
> lowering or omit mixed execution.

## Present assumptions and exact publication changes

| Contract object | Assumption today | Exact change needed for mixed use |
|---|---|---|
| Object and linking (§§9.1–9.3) | One ISA object's closed sections and linked symbols; no native-container schema. | Publish a versioned inventory associating embedded/linked ISA object bytes and object_hash with selected device roots and certificates. A native-container hash, if used, is a separate identity. |
| Certificates/inventory (§§12.1–12.3) | Closure-keyed device-region records; current text does not explicitly delimit native inventory. | Insert the shared scoping rule in §12.3, cross-reference from §9.2, and require complete device-owner/link-proof coverage per root. Multiple device roots can share static closures without merging root-relative contexts. |
| Launch/entry (§10) | bennett_run(program, cc_entry, args, entropy) starts device CC; it is not native main. | Publish a host call/return shim and container/root selection/feature negotiation. Define native argument/result marshalling, including ptr (whose host binding §10 does not specify), status/fault propagation, suspend/reverse/close and ownership. Do not invent a current general launch shim. |
| Budgets (§5.4; §§10–11) | Validated token tuples and identity scoped to a program/run; action_call has no primary token (§4.7). | Bind selected device invocation budgets and token equality to the launch request; charge actual device/replay work. State host/shim accounting separately; a native process has no invented global B. |
| Handles (§3.3; §10; dialect §6.6) | Register ids refer to the loaded program's ledger; run ownership and token validity are explicit. | Map host-visible opaque handles to that program/ledger with validity and cross-launch ownership checks; preserve class vectors and token identities. Do not serialize native pointers as device ids or token tuples as identities. |
| Effect tape (§7.3; §10) | Run-associated R effects and explicit copied hostcall requests; no implicit log of native host I/O. | Associate each device run and tape with the launched root and define host effect/proxy ordering and replay at the boundary, preserving §7.4 reversal. Saved-journal interchange needs its own versioned replay profile. |
| Host memory by reference (§§7.1–7.2; dialect §§8.5, 17.1, 19.4–19.5) | Device layout plus dialect snapshot/replay and boundary-address/promotion rules; copied hostcall bytes do not provide general shared pointers. | Publish the mapping and lifetime protocol named in the statement, including allocator metadata/history and pointer-rich layouts, so ordinary host memory can be supplied safely without universal host promotion. Retain existing snapshot/replay as a construction, not the sole eventual capability. |

For example native main can call marked roots A and B in distinct ISA objects.
Each has its own object/root certificate and root context []; neither
certificate inventories main or host-only libc. A shared linked device
callee is checked in each root's actual invocation tree. A native comparison
executes the corresponding materialised region/callee closure under its
recorded layout, input and tool configuration (dialect §§17.7, 19.5, 19.9).

These notes specify boundary scope and exact remaining contract work; they
implement no container, host shim or memory registration. The existing
bennett-4ht issue tracks that publication/implementation obligation. Current
device contracts and their complete estimate/proof requirements remain in
force; an unimplemented boundary is not evidence that mixed execution works.


# The document under review (round 1 snapshot)

# Acceptance dossier (Muse seat, batch 2): lpe, xv4, checker-native-model, checker-resource-contexts, 0jq, 4ta, 7s0, v2v, ysw, 2cg, l2p, checker-fault-rate, fd0, pe1, 2qc, sqr, 4yg.1

Scope (advisor ruling R9, 2026-11-02T10:55Z): each proposal below was ACCEPTED by both other council members (sol, astra) in its latest round (empty blocking lists, consensus agree) and satisfied the rubric's standing bennett-4ht check (mixed fat object stays reachable) in that round. This is the final acceptance seat: grade each proposal independently on its own merits. Each part names its run, accepted round and the spec it amends. Several parts cite the shared scoping statement `docs/notes/2026-11-02-rev2/fat-object-scope.md`; it is reproduced once in the appendix. Parts are separated by horizontal rules.

---

## Dossier part: lpe (run contract-lpe-2026-11-02; accepted by sol, codex in round 2; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-02-rev/lpe.md)

# lpe — classical width families with explicit call shapes

Full revised proposal for council review, 2026-11-02; `b-isa-spec-lpe`.
Supersedes the proposal in `2026-11-02-contract-lpe.md`; no spec edits or
council acceptance are implied.

## Defect classification and North Star scope

ISA 0.9 §3.3 provides qreg[*], qreg.width and checked transfer into fixed
slots; §§5.1/9.1 give region slots literal widths. Dialect 0.3 draft
§8.4 can construct a fixed-shape oracle for each valid width/extent and
CC-dispatch between them. Its §24 D34 prohibits interpreting emission
order as a runtime validity restriction; §25.3 G-17 requests a compact
representation. This remains an efficiency/interface extension, not a
proved lack of denotational expressiveness in 0.9.

A dispatch table of up to 2^64−1 positive runtime widths is not a practical
completed build. A finite emitted prefix cannot certify an unrestricted
program. North Star §§0/3.3/4.2 retains arbitrary defined, bounded
programs and classical runtime budgets. Missing specializations cannot
become T-IFACE, an invalid-width fault or a required source rewrite.
Literal-width 0.9 programs and their unlimited mathematical wire/region
widths remain available; this compact runtime family mechanism adds no
new cap to them.

## Alternatives and worked witnesses

| Construction | Consequence |
|---|---|
| Complete static dispatch | Existing 0.9 semantics; an emitted prefix remains unfinished. |
| Finite load-time instance list | Suitable when the source program itself has that finite domain; cannot restrict an unrestricted program. |
| Symbolic family, instantiated classically on demand | Recommended; one linkable family, with a fixed shape during each coherent invocation. |

The memoryless family `xor_width[n]` has input/target widths n, fault
width 4 and body `lift.retval x`. At B≥1 it maps
`(x,t,f) -> (x,t XOR x,f)`; at B=0 it maps
`(x,t,f) -> (x,t,f XOR 1)`. A false outer control is identity. Thus n=1
maps (1,0,0) to (1,1,0), and n=3 maps (5,3,0) to (5,6,0). The target,
fault and control values are quantified, not initialized conveniently.

The ledger width of an eight-wire register does not choose its memory
shape. `width_args=["1","4"]` for a memory family with parameters [A,W]
selects region[1,4]; `["2","2"]` selects region[2,2]. Both occupy eight
wires. A legal qstore XORing integer 1 into cell 1 of the zero image
produces flattened integer 16 in the first shape and 4 in the second.
The address/value operands have the corresponding resolved widths in
each access. This packing witness does not infer either shape from 8.
For six wires, [0,6] and [1,3] similarly remain distinct. A=0 is legal
for a region and retains K79's empty address actual `()`, never wire[0].

Finally, one fixed root action can call xor_width[1] and xor_width[3]
on disjoint operands with two explicit token arguments, then return.
The child signatures must have widths [1,1,4] and [3,3,4] in the same
certificate, with one forward call occurrence apiece. Their common
family closure hash cannot be the sole certificate record key.

## Recommended exact spec changes

Publish as ISA/object/launch/sched/cert/coverage 0.10; amend §§3.3, 4.7,
5.1, 9.1–9.4, 10–12 and 16.2 together. The following is normative
replacement/addition text for that release.

### Family signature and substitution (§§5.1, 9.1, 16.2)

```text
A region header MAY declare [n,...] immediately after its symbol name.
Parameters are distinct unsigned-i64 classical shape values, in a
separate width namespace. signature.width_params lists, in header order,
{name,bind:{group,slot,axis?}}. A wire binding names a wire slot; an extent
binding names a mem slot and axis "A" or "W". A symbolic size is
{param:name}, or the existing literal integer. Parameter occurrences are
permitted in wire[N], reg[N], region[A,W], size-bearing opcode suffixes,
allocation dimensions, and loop/bounds counts. Substitution is
capture-free and precedes all ordinary type, range and opcode checks;
all other integer positions retain their existing literal rules. This
adds no implicit arithmetic, inferred formula or quantum-dependent size.

A signature admits exactly shape values satisfying its declared size
constraints: wire/cell widths are positive, region A may be zero, and
existing per-opcode constraints still apply after substitution. Only the
signature determines the admitted shape set; body validation cannot
silently remove a shape from it. The producer must supply a
well-formed substituted body for every shape the signature admits.
An ill-formed body at an admitted shape is an invalid family, not an
invalid caller width. The resolved denotation is exactly the literal
substitution, including full-domain, control, adjoint, prefix-reversal,
borrow-frame and local-restoration obligations.
```

### Explicit call-shape channel (§§3.3, 4.7, 10, 16.2)

```text
Every family call has a separate ordered width_args vector, not part of
ordinary args. Text syntax puts [s0,...] immediately after @callee in
all region-call forms, including lifted calls and both qinplace callees;
a family header uses the same brackets for parameter declarations.
At CC/R entry, si is a literal unsigned-i64 or a classical i64 value read
as unsigned. Every parameter has exactly one supplied value. Wire-bound
values MUST equal the actual's ledger width. Memory-axis values are
supplied explicitly: substitute them into the callee mem signature and
require width(q)=2^A*W for every qreg memory actual. Compute this equality
in mathematical integers without wrapping. No A or W is inferred from
total register width, and no pre-existing caller descriptor is presumed.

Check all values, role constraints, disjointness, ledger states and
resolved shapes before any effect, including consuming a view. A bad
CC/R binding is CC trap / R fault FAULT_UB_TRAP under the existing rules.
In coherent callers, shape arguments are literals or already resolved
classical shape parameters, never coherent data. Their memory actuals
are declared interface/local regions: the substituted A and W must each
equal the caller region's resolved A and W, not just its total size.
Adjoint, matched uncall and R history retain the same vector. Nested
body/template/argument forwarding preserves each callee's vector just
as it preserves the invocation-token context.

A host launch, scheduling request or estimate for a family supplies
width_args explicitly, independently of params_jcs/ordinary args and
without needing live register ids to estimate it. Launch and estimator
validation use E_ARG for invalid request bindings before ownership or
execution; nested CC/R calls use the trap/fault rule above.
```

The launch 0.10 request structure gains `width_args_jcs` and its byte
length: a copied JCS array of the canonical decimal strings described
below. The family entry and its ordinary args/token/register slots are
selected explicitly by that request. Existing non-family entry requests
use an empty vector. This also provides a concrete transport for A/W at
the native-host boundary.

### Identity, expansion and schedules (§§9.2, 10.1, 11–11.1)

```text
interface_hash covers the symbolic signature, parameter order and bind
sites. closure_hash identifies the symbolic source and dependencies.
width_args is the header-ordered array of canonical unsigned decimal
strings, no leading zeros except "0". Define:
instance_hash = SHA-256(UTF-8("width-instance\n" +
  lowercase-64-hex-family-closure-hash + "\n" + JCS(width_args) + "\n"))
Here \n denotes one LF byte, and the family hash is ASCII hexadecimal,
not raw digest bytes. No trailing bytes follow the last LF.

Concrete executables, schedules, estimates, certificate subjects and
invocation contexts carry closure_hash, width_args and instance_hash.
Consumers recompute and validate instance_hash before expansion/replay.
Binding equality adds these fields to all existing budget, params_hash,
variant, controls, accuracy, target and expansion bindings; params_hash
continues to hash only ordinary args. A callee context retains its own
instance, not the root's instance. Captured templates and matched
forward/reverse occurrences retain that instance as well.

The expansion default for resolved 0.10 instances is the unchanged
ref@0.9 library, expansion hash
5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197,
unless a different library is explicitly bound. Its descriptors receive
literal substituted sizes. A cache key includes instance_hash, target,
expansion identity and every existing schedule binding. Imports compare
symbolic signatures including parameter order/bind sites.

A supported family implements every admitted shape. Caching, lazy
materialisation and finite warm-up lists are implementation choices;
a miss is not invalid source input. Executor resource exhaustion follows
the existing executor-resource contract (§17 item 16), not a new source
fault. A finite instance inventory is not a claim of family completeness.
```

### Concrete certificate records and frames (§§9.4, 12.1–12.3)

```text
regions is keyed by closure_hash for non-family regions and by
instance_hash for concrete family instances. A family instance record
carries closure_hash, instance_hash and width_args; each has its own
substituted signature, bounds, domains, required frame and verification
records. There is no abstract family record standing in for these
concrete records. Width substitution precedes §9.4 frame construction;
slot widths are resolved literal widths, with c remaining the only
frame-expression variable as before.

Family claim subjects and g/ginv inverse-pair references explicitly
identify closure_hash, width_args and instance_hash. An expected.program
or library-claim reference to a family likewise uses an explicit
{closure_hash,width_args,instance_hash} reference instead of a bare family
hash, with resolved signature compatibility checked. Composition keys
use instance_hash in the hash position for a family, including error
multiplicities. A concrete claim or inverse proof for one instance
cannot discharge another. A width-uniform structural claim may cover
several records only with explicit shape quantification and checked side
conditions over its entire admitted domain; each use records its shape
substitution. The default is separate concrete claims. Region-context
reports distinguish full callee instance identity in addition to variant,
controls, parameters, budget and semantic call occurrence.
```

For the mixed-width root, `regions[H1]` has
`closure_hash=F,width_args=["1"],instance_hash=H1` and input/target/fault
widths [1,1,4]; `regions[H3]` has the corresponding ["3"] and [3,3,4].
Their required slot frames have those widths, with separately derived
scratch/history descriptors at each invocation. Composition has one
`H1:forward:0` and one `H3:forward:0`. F is the common actual family hash.
H1/H3 below use a synthetic all-zero F solely to test hash bytes.

Append to dialect §8.4's 0.10 map: "A classical shape not finitely
enumerated by compiler value analysis lowers to this width family.
Shape-width lists affect instantiation order only." Formula-based layout
beyond direct substitution requires an explicit expression contract;
existing literal specialization remains a valid construction meanwhile.

## Mixed fat object (bennett-4ht)

Add to §§9/10: "The native host binary may contain only marked modules
as embedded VM objects. A host dispatch manifest selects a VM module,
exported family symbol and launch 0.10 request; its classical shim supplies
width_args from host sizes and qreg handles before coherent entry.
Certificate inventory covers the selected VM closure and all its reached
instances, not every host function. Ordinary main, argv/envp handling,
unmarked libc and unrelated host code remain native. A marked module's
required dependencies are linked into its VM closure through published
imports; this does not require translating the whole binary. A native
comparison calls the corresponding materialized host entry with the same
shape, args, image and budget conventions, rather than comparing an
unrelated whole-program entry. Shape identity is independent of native
addresses and process-local qreg/token ids."

## Round-1 blocking items and resolution

| Item | Change and concrete witness |
|---|---|
| sol LPE-1 / astra B1: CC/R has no descriptor for A/W | Separate explicit call/launch width_args; pre-effect axis/width checks. Eight wires with [1,4] versus [2,2] produce flattened cell-1 values 16 versus 4. |
| sol LPE-2 / astra B2: one closure record cannot hold several instances | Instance-keyed concrete records, resolved frames, subjects, inverse references and composition; preserved nested shape captures. One root contains [1,1,4] and [3,3,4] child records. |

## Hashes, release and consumer work

This is a 0.10 extension, not an incompatible 0.9 K repair. Every symbol
re-emitted with isa=0.10, including non-family symbols, receives its new
§9.2 version-envelope identity. New interchange versions carry the shape
channel and instance records; target 0.9 is reused when otherwise
unchanged. Published 0.9 object/catalog bytes remain frozen. The catalog
default above explicitly avoids inventing an unprovided ref@0.10.
VM, linker, scheduler, estimator, plugin and checker must publish matching
0.10 grammar/ABI/schema vectors before adoption. G-17/lpe implementation
work remains open; these proposals do not certify complete emission.

## Conformance vectors and verification

Besides the witnesses above: mismatched operand widths or false
instance hashes fail before effects/replay; n=0 fails a positive wire
signature. Different n invalidates a cached schedule; distinct qreg ids
with equal shapes share instance identity. Test imports with swapped bind
sites, nested forwarding, control/adjoint, A=0 empty address, a valid
uncached shape, and uniform proofs whose side conditions fail at another
shape. Preserve arbitrary target/fault/dirty systems and full-D checks.

The following independently executable script checks finite mathematical
witnesses, not an implementation of the proposed 0.10 certificate schema.
Run it by extracting this note's Python block with `python3 -I -B -`.

```python
import hashlib
import itertools
import json

family = '0' * 64

def instance(values):
    a = [str(v) for v in values]
    data = 'width-instance\n' + family + '\n' + json.dumps(a, separators=(',', ':')) + '\n'
    return hashlib.sha256(data.encode()).hexdigest()

h1, h3 = instance([1]), instance([3])
assert h1 == '3486e3dc5d4e3a80a35d4338f5ff126b787ded89baaee9f66aca083e7025cf6e'
assert h3 == '9ae5c34acce5452f6c24f31e97baa9ddfc027a44c609a5e77f4eb54759feacd3'
assert h1 != h3
records = {h1: (family, ['1'], [1, 1, 4]), h3: (family, ['3'], [3, 3, 4])}
assert len(records) == 2 and records[h1][2] != records[h3][2]
assert (1 ^ 0, 5 ^ 3) == (1, 6)
assert 2**1 * 4 == 2**2 * 2 == 8
assert (1 << (1*4), 1 << (1*2)) == (16, 4)
assert 2**0 * 6 == 2**1 * 3 == 6
cases = 0
for n in (1, 3):
    for x, t, f, c, b in itertools.product(range(2**n), range(2**n), range(16), range(2), range(2)):
        payload, code = (x, 0) if b else (0, 1)
        after = (x, t ^ payload, f ^ code) if c else (x, t, f)
        back = (after[0], after[1] ^ payload, after[2] ^ code) if c else after
        assert back == (x, t, f)
        if not c:
            assert after == (x, t, f)
        cases += 1
assert cases == 4352
print('PASS lpe: 4352 width/control/budget tuples; two instance keys; explicit memory shapes')
```

---

## Dossier part: xv4 (run contract-xv4-2026-11-02; accepted by sol, codex in round 2; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-02-rev/xv4.md)

# xv4 — an exclusive proof verdict for a fixed classical image

Full revised proposal for council review, 2026-11-02; `b-isa-spec-xv4`.
Supersedes `2026-11-02-contract-xv4.md`; proposed contract text only.

## Defect classification and North Star scope

ISA 0.9 §5.2 includes every interface-region cell value in D. §12.2
K69–K74 gives `proof` only for componentwise full D; successful exhaustive
strict slices receive `evidence`. Dialect 0.3 draft §§19.9/25.2 correctly
requests that existing evidence label. Assigning it is not a checker bug.

North Star §5.1 calls exhaustive verification on a declared finite domain
a proof, while §8 rung 4(a) fixes the SQLite database classically and
varies all rows and all target values. This is a certificate terminology
and scope mismatch, not missing SQLite execution semantics. The proposal
adds a conditional proof without asserting correctness on other images.
It retains all varying input, target, fault, dirty-system and inherited
control components; neither sampling nor source edits replace the rung.

## Alternatives and complete tiny witness

| Choice | Consequence |
|---|---|
| Keep K74 | Current conformance; document the terminology mismatch. |
| Call an image slice unqualified proof | Unsoundly promotes correctness to every database image. |
| Checked image-relative proof | Recommended; the image is an explicit precondition. |
| Put the database in a local image | Existing full-external-D proof for a different specialized closure and preparation route; does not relabel the original interface-region claim. |

Let an exact, fault-free oracle at a sufficient bound have one input bit
x, one target bit t, four fault bits f and one `in` region[1,8] db, with
payload `db[x] & 1`. Its complete tuple relation is
`(x,t,f,db) -> (x,t XOR (db[x]&1),f,db)`, workspace clean.

For image `0102`, x=0 flips t and x=1 preserves it: payload `1 XOR x`.
For `0201`, payload is x. Each image slice has 64 tuples; unrestricted D
has 2^22 tuples, so coverage is exactly 1/65536. An implementation
hardcoding `0102` passes the first 64 and fails all 64 for the swapped
image. Fresh bindings and replay can prove the second image separately;
its mere difference is not malformed input.

An ordinary one-bit X action with no regions has domain t=0,1 and table
0→1, 1→0. Its full-D exhaustive check must receive only `proof`, whether
fixed_regions is absent or empty. This witness catches the first note's
vacuously true image-relative condition.

At A=16,W=8, with x width 10, t width 1 and f width 4, there are 15
varying bits and 524288 fixed image bits. Coverage against unrestricted D
is exactly 1/2^524288, never floating-point zero. Prepared cells remain
interface components even though the experiment fixes them.

## Recommended exact spec changes

Extend the §12.2 domain schema and the certificate label-request/checker
outcome enumerations; add a §0.2 K entry. Replace BOTH the introductory
"otherwise evidence" rule in §12.2 and K74's blanket strict-slice
classification with the exclusive classifier below. This is a proposed
in-version certificate extension; no instruction or domain D changes.

```text
A domain MAY contain fixed_regions:[{name,A,W,image,sha256}]. An absent
field is an empty list. name resolves by the existing component rules to
an in-role interface region, with precisely the subject's A and W.
Each resolved fixed region occurs exactly once and MUST NOT also occur
in domain.regions. A mut-role region cannot be fixed by this mechanism.

image is exactly ceil(2^A*W/8) raw bytes encoded as lowercase hexadecimal;
unused high bits in the final byte MUST be zero. Cell i consists of bits
[iW,(i+1)W) in the little-endian byte image. sha256 is SHA-256 of the raw
bytes, not the hexadecimal text. The checker hashes independently and
uses those cells on every replay. Fixed cells participate in domain
validity and tuple/output checks, but each contributes one choice to n.
The full unrestricted |D| remains unchanged. This metadata introduces no
operation for inspecting unknown coherent state.

After every §12.1 replay obligation succeeds, an exhaustive
table/program/oracle claim receives exactly one outcome, in this order:
(1) proof iff its domain equals unrestricted D component by component;
(2) otherwise proof_relative_to_image iff fixed_regions is nonempty,
    every image binding is valid, every fixed region is accounted for,
    and every remaining component occurs exactly once with its full
    range (all interface bundles/cells, borrowed positions and prepended
    inherited controls included);
(3) otherwise evidence.
Successful sampled claims always receive evidence, including when their
distinct draws cover the whole domain. Malformed domains, stale hashes
and mismatches reject, rather than receiving any successful verdict.
Omission-at-zero remains a strict slice unless the original component
is thereby genuinely at its full range under the existing rules.

Coverage remains exact n/|D| against unrestricted D, with distinct-draw
coverage for sampling. The checker report identifies closure_hash,
claims-array index, invocation/context key, and ordered resolved
(region identity,A,W,image hash) bindings. A supplied label is a request,
not a producer assertion. Requested proof rejects unless the computed
outcome is proof; requested proof_relative_to_image rejects unless the
computed outcome is proof_relative_to_image. An evidence request may
accompany a stronger independently computed outcome, as before.

K75's host-limit handling remains: unchecked (host limit) discharges no
proof obligation and does not invalidate a legal domain or shrink it.
```

This deliberately preserves full-D K74 proofs and evidence for ordinary
strict slices. The sole new successful classification is a nonempty,
valid image binding with all other components fully quantified.

```text
A proof_relative_to_image theorem is conditional on the stated image.
Using it to discharge an executable invocation additionally requires
checked preparation/binding establishing that this in-region contains
exactly those classical bytes and is factorised from other systems at
entry, and that its exit image is restored. Establish preparation from
declared bytes and logical preparation operations, never inspection of
unknown coherent data. Without that preparation evidence the theorem
remains conditional and does not discharge the invocation.

This verdict cannot discharge an unrestricted borrow-frame, inverse-pair
or other full-D obligation, and cannot be reused for another image,
invocation, target realisation or schedule by discarding its bindings.
All §12.1 exact +1 basis-phase, full-tuple, clean-workspace and
external-reference obligations remain in force. A basis table cannot
prove a non-permutation realisation; its numerical/channel obligations
are unchanged. Target matching, resource accounting and error
composition are not relaxed by conditional correctness.
```

For fixed image I, write J_I for the image-preparation isometry including
prescribed clean workspace. The permutation assertion is `V J_I = P J_I`,
also after tensoring with identity on an arbitrary external reference.
When a process claim is needed, compare
`E_real ∘ Ad_J_I` and `E_ref ∘ Ad_J_I` with the complete output interface.
Controlled-unitary comparison retains a phase-sensitive bound on
`||U J_I − V J_I||`; equal uncontrolled channels alone cannot discharge it.
Numerical/channel acceptance procedures remain those of §12.1.

## Mixed fat object (bennett-4ht)

Add to §§9/10/12: "A native binary may carry VM objects only for marked
modules. The host launch manifest selects a VM entry and records the
classical image preparation/copy into its in-region, with resolved shape
and raw-byte hash. The certificate inventory is that entry's selected VM
closure and reached contexts, not the whole native executable. Image
preparation may come from host database construction or a declared
snapshot. Host bytes are bound to device cells using the declared packing,
not host pointer identity. Unmarked main, argv/envp, libc and unrelated
code remain native. The native comparison invokes the corresponding
materialized marked entry over the same image and varying domain; it
need not treat the entire binary as the oracle. Runtime shims and build
configuration are recorded as required by the North Star."

A preparation witness for this note is a host buffer `01 02` copied to
the selected two-cell VM in-region before entry and retained unchanged
through the oracle's return. Preparing an entangled region does not meet
that classical-image precondition. This says how a mixed object uses the
contract; a physical launch shim need not be implemented by this note.

## Round-1 blocking items and resolution

| Item | Change and concrete witness |
|---|---|
| sol XV4-B01: new rule overlaps full-D proof and K74 strict-slice evidence | Replace both blanket rules with one ordered, exclusive classifier; require nonempty fixed_regions. Full-D X receives proof, the 64-tuple 0102 slice receives proof_relative_to_image with 1/65536 coverage, sampling receives evidence. |

The additional round-1 suggestions are retained: a complete oracle
relation, stale-versus-fresh image mutations, explicit preparation-isometry
comparison, and separation of requested labels from checker outcomes.

## Hashes, publication and consumers

Fixed images and requested labels change certificate bytes; assigned
verdicts and resolved bindings are checker-report data. Under an
authorized 0.9 K extension retaining the semantic envelope, §9.2 excludes
certificate sections from object_hash, so source/interface/closure/object
identities, targets, schedules and ref catalog remain unchanged. A full
version bump instead requires regenerating version-envelope identities
and dependent pins. This note authorizes neither publication choice.

Producers/checkers must publish schema and verdict vectors together;
legacy schemas must not silently treat the qualified spelling as proof.
Until acceptance retain current evidence labels and exact fractions.
The SQLite rung still requires unmodified SQLite, real SQL, quantum
addressing, all rows/targets at N≤2^10, Grover at N≤2^8 and the named-target
N=2^20 estimate. Conditional correctness does not replace those gates.
xv4 remains open for acceptance and implementation.

## Conformance vectors and verification

In addition to the three exclusive-verdict cases: swapping 0102 to 0201
while retaining the old digest, expected relation or preparation binding
rejects reuse. Updating all bindings permits a fresh check, never reuse
of the old theorem. Test hashing hex text instead of bytes, wrong A/W,
nonzero padding, duplicate region identities, omitted target/fault/dirty
ranges, partial controls, a requested unqualified proof and a mut-region
binding. Identical image strings for two distinct resolved region slots
remain separate bindings. Test outer controls 0/1, arbitrary dirty states
and external references; sampled full coverage remains evidence.

This exact finite witness checks hashes, the complete 64-tuples relations,
exclusive classification premises and coverage. It is not execution of a
new checker/schema, a SQLite run or council acceptance.

```python
from fractions import Fraction as F
import hashlib
import itertools

images = (bytes([1, 2]), bytes([2, 1]))
hashes = [hashlib.sha256(i).hexdigest() for i in images]
assert hashes == [
    'a12871fee210fb8619291eaea194581cbd2531e4b23759d225f6806923f63222',
    '25dfd29c09617dcc9852281c030e5b3037a338a4712a42a21c907f259c6412a0']
assert hashes[0] != hashlib.sha256(b'0102').hexdigest()
rows = list(itertools.product(range(2), range(2), range(16)))
assert len(rows) == 64 and F(len(rows), 2**22) == F(1, 65536)
for image in images:
    for x, t, f in rows:
        payload = image[x] & 1
        after = (x, t ^ payload, f, image)
        assert (after[0], after[1] ^ payload, after[2], after[3]) == (x, t, f, image)
assert sum((images[0][x] & 1) != (images[1][x] & 1) for x, t, f in rows) == 64
assert all((images[0][x] & 1) == (1 ^ x) for x in range(2))
assert all((images[1][x] & 1) == x for x in range(2))
# Full-D X: empty image set cannot satisfy the qualified predicate.
full, fixed, remaining_full = True, [], True
assert full and not (bool(fixed) and remaining_full)
# Fixed-image slice: not full D, but every other component is full.
full, fixed, remaining_full = False, [hashes[0]], True
assert not full and bool(fixed) and remaining_full
# Omit a target range: neither proof predicate holds.
remaining_full = False
assert not full and not (bool(fixed) and remaining_full)
assert 2**16 * 8 == 524288
assert F(2**15, 2**(15 + 524288)) == F(1, 2**524288)
print('PASS xv4: two 64-tuple image relations; 64 swapped-image failures; exclusive proof predicates; exact coverage')
```

---

## Dossier part: checker-native-model (run contract-checker-native-model-2026-11-02; accepted by sol, codex in round 2; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-02-rev/checker-native-model.md)

# Checker native models — evaluated epsilon and phase-bearing unitaries

Full revised proposal for council review, 2026-11-02; checker request 1
in the existing cross-repo filing queue. Supersedes
`2026-11-02-contract-checker-native-model.md`; proposal only.

## Defect classification and North Star scope

ISA 0.9 §8.3 native entries supply opcode, classes, controls, parameters,
cost and epsilon, but no realised operator. §8.1's arithmetic expressions
are not operator definitions. §§4.4/12.1 require phase-sensitive realised
unitary/channel comparison; an advertised error bound cannot identify
which operation to reconstruct. This is an S0 contract gap for independent
native approximation verification. Assuming the ideal opcode for an
opaque approximate leaf is circular self-comparison.

North Star §§4.4/5.1 part 2 retains approximate algorithms and independent
phase/channel checks. Exact logical native gates still denote their
phase-fixed §4.4 operations. The repair supplies missing model data,
without changing accepted native-unitary semantics or mistaking a
physical stochastic failure rate for logical approximation epsilon.
Legacy unchecked reporting is migration behavior, not a replacement for
the mechanism or permission to omit approximate algorithms.

## Alternatives and concrete witnesses

| Choice | Consequence |
|---|---|
| Always substitute the ideal opcode | Does not reconstruct approximate realisation independently. |
| Trust advertised epsilon | An explicit target assumption only; cannot prove a tighter independent claim. |
| Phase-bearing hash-bound unitary model | Recommended; permits independent numerical and induced-channel checks. |
| Expand an explicit scheme into exact leaves | Already works when it describes the actual circuit; does not describe an opaque approximate native leaf. |

An X entry with advertised epsilon=2 and time=1 could realise X or −X.
Both meet the same bound/cost/class metadata, and their uncontrolled
channels are identical. Under one coherent control on |+>_q|0>_t, they
produce `(00+11)/sqrt(2)` and `(00−11)/sqrt(2)`, orthogonal states.
The phase relative to the disabled branch is observable. Without model
bytes the current target/hash cannot distinguish these implementations.
A zero-distance numerical claim against controlled X is true only for
X; a declared conservative epsilon=2 alone cannot establish it.

The evaluated-epsilon counterexample is exact X with
`epsilon={"op":"-","args":[1,1]}` and no model. §8.1 evaluates it to
zero exactly; §17 item 9's eps-independent exact-match convention applies.
It must remain exact and checkable. For `epsilon={"var":"c"}` on c=0..1,
c=0 is exact; c=1 needs a realised model for independent verification.
Expression syntax alone cannot determine that requirement.

The channel-admission counterexample has Kraus operators
`K0=X/sqrt(2), K1=ZX/sqrt(2)`. Their squared operators sum to identity,
but the channel maps |+><+| to I/2. A unitary preserves purity, so no
logical unitary represents this map. An explicit controlled dilation
does not make the reduced map unitary or supply an operator-norm epsilon
for it. In contrast, two Kraus operators both X/sqrt(2) represent Ad_X;
that representation is usable if it also binds phase-bearing U=X and
its actual controlled model.

## Recommended exact spec changes (§8.3)

Add `realisation_model?` with initial format
`bennett.native-model/1`. Extend the target schema with the following
rules; retain §§4.4/8.1 matching and §12.3's controlled numerical claims.

### Model requirements depend on evaluated epsilon

```text
Resolve the matched entry's k, c, requested eps and parameter bindings
using §8.1 before determining model requirements. At each resolved
context, if achieved epsilon evaluates exactly to zero, an omitted model
denotes precisely the §4.4 opcode, including global phase and the exact
controlled form. Positive evaluated epsilon requires a versioned
realisation_model to discharge independent realised-operation
verification. A model-complete target supplies one for every admitted
context where its epsilon can be positive. Expression syntax alone
neither requires nor exempts a model.

Any supplied model MUST agree with the exact §4.4 operation in every
zero-epsilon context and satisfy the advertised operator-norm bound
otherwise. Zero-valued expressions independent of eps retain §17 item 9's
exact matching convention. Existing legality rules for eps-dependent
expressions, log2inv_eps, eps_decade and target matching remain unchanged;
this does not make an otherwise illegal zero-epsilon expression legal.
```

### Native operation and error metric stay unitary

```text
Every native realisation model MUST identify a phase-bearing logical
unitary U for each resolved parameter/control context. Native epsilon
bounds ||U-V||op for the corresponding phase-fixed ideal §4.4 operation V.
Normalization and model identity alone do not establish accuracy, an
inverse, or phase-free permutation status.

The native model kind is unitary. Matrix, Kraus or instrument data may
be used as a representation only when their reduced logical map is
rho -> U rho U-dagger, and the phase-bearing U is supplied as part of
the same model. Kraus/instrument data alone are insufficient. Check
complete-positivity/trace preservation when applicable and equivalence
to the bound U on every matrix unit (or a checked symbolic proof of that
identity), as well as U-dagger U=I. Thus a CPTP map that mixes a pure
logical state is not a conformant native-unitary gate model under §4.4.

For every admitted total control count the model identifies the actual
controlled unitary, including phase relative to disabled branches.
Exact controlled-U construction is allowed when explicitly bound as
that actual implementation. Arbitrarily controlling a Kraus list does
not define it. Instrument/environment conventions, when present, must
reduce to the bound logical unitary in that control context.

Channel claims compare induced channels; they do not replace the
phase-bearing unitary, change epsilon to diamond error, or discharge
§12.3's required numerical claim for controlled unitary variants.
General logical measurement retains its existing CC/other published
mechanisms; stochastic hardware failures remain separate target-model
work. This repair makes no new nonunitary-native admission rule.
```

### Representation and independent reconstruction

```text
realisation_model has {version,kind,arity,basis,parameter_bindings,
control_models,data}. Its canonical target bytes enter target_hash.
After resolution, arity and basis determine the complete ordered logical
operand bits. Explicit control models give the full context matrix;
a controlled_U rule instead gives a base matrix and constructs identity
on disabled branches and that matrix on the all-enabled branch, retaining
its global phase. In that form arity/basis describe the base matrix and
control_models adds the resolved c control wires. All matrix dimensions
must match the resolved basis. No environment is silently counted as an
extra logical input or discarded from a claimed unitary interface.

parameter_bindings uses the same resolved k, c and eps as cost/error
matching and the exact angle binding (§3.1 and §11.1 K20). A finite
binary64 theta denotes exactly that binary rational, not a rounded
source decimal. An explicit operand-to-wire permutation maps the entry's
own-controls-then-effective-controls order (§8.3) to §12.1's allocation
basis, inherited controls first. Both data and control models use this
map; wrong parameter, order, dimensions or context bindings reject.

Complex matrix entries are [real,imaginary] exact expressions over
rational constants, i, pi, sqrt, exp, sin and cos with finite expression
trees; rational constants are [numerator,positive_denominator] canonical
decimal-string pairs in reduced form. Expression nodes are
{op,args}; variables name only the declared parameter/context bindings.
Data may additionally supply closed rational interval enclosures of an
identified exact operation, with independently checkable enclosure and
unitarity certificates. An unverified box alone is not an operation.

The checker independently constructs U from the exact model in each
invocation context, checks its normalization/control/accuracy obligations,
and applies §12.1's interval numerical/channel procedures to requested
claims. Inconclusive interval tests do not pass. The advertised epsilon
remains a separate matching/error obligation, never the operator's
definition. An absent approximate model never licenses ideal self-comparison.
```

For X, a concrete base model is below. Its rational/imaginary pairs are
exact; changing the two real off-diagonal numerators from "1" to "-1"
produces the −X model. `controlled_U` binds its actual controlled
implementation for every admitted c, not just equality of uncontrolled
channels. For non-parametric X, k=0, and eps is the requested share when
bound; a zero-epsilon context needs no eps-dependent model expression.

```json
{
  "version":"bennett.native-model/1",
  "kind":"unitary",
  "arity":1,
  "basis":["t"],
  "parameter_bindings":{"k":"k","c":"c"},
  "control_models":{"kind":"controlled_U","controls":"c","disabled":"identity"},
  "data":{"matrix":[
    [[["0","1"],["0","1"]],[["1","1"],["0","1"]]],
    [[["1","1"],["0","1"]],[["0","1"],["0","1"]]]
  ]}
}
```

Model-format version 1's default evaluation is exact expressions plus
§12.1 interval enclosure, without any dimensional cap. Larger matrices
may be generated symbolically from the same bindings rather than fully
materialized; finite host checking limits yield unchecked obligations,
not smaller supported algorithm domains.

## Migration, hashes and publication

Legacy targets without required models keep parse/execution compatibility.
At zero evaluated epsilon use the exact-opcode convention. At positive
epsilon, missing-model reporting leaves only the affected independent
numerical/channel obligations unchecked; it cannot yield a checked
executable certificate covering them. Unknown versions receive
unsupported-model reporting, never a guessed operation. A supplied model
that contradicts a zero-epsilon contract rejects that target claim.

Recommend an authorized 0.9 K repair with this versioned target extension.
Model bytes change target_hash and require regenerating every dependent
schedule_hash and certificate binding. Source/interface/closure/object
identities remain unchanged only under an unchanged 0.9 semantic envelope;
a full ISA-version publication requires rehashing those envelopes too.
The ref catalog is unchanged. Target authors, scheduler, simulator and
checker must agree on model resolution; an ideal-opcode simulator alone
is not native approximation verification. Existing request 1 remains open
for acceptance/implementation. No physical native checker was run here.

## Mixed fat object (bennett-4ht)

Add to §§9/10/12: "A mixed binary's native host runs main, argv/envp,
unmarked libc and ordinary code. Only marked modules are VM objects;
the launch manifest selects their exported entries. A native gate model
belongs to the target used for that VM closure and its reached native
leaves, not to the host machine instructions of the whole binary.
Certificate inventory and phase/control reconstruction cover that selected
closure's invocations. Each VM schedule pins the target/model hash even
when several modules share the target. Host qreg handles and angle values
are marshalled through the published launch bindings, not reinterpreted
as model basis indices. A native comparison uses the corresponding
materialized marked host entry and captured inputs; it does not require
every host instruction to have a quantum gate model."

Thus a marked module using controlled X distinguishes the X and −X models
while linked beside an ordinary host libc. No whole-binary VM translation
or certificate inventory is assumed.

## Round-1 blocking items and resolution

| Item | Change and concrete witness |
|---|---|
| sol B1 / astra B1: expression-valued zero both requires and omits model | Value-based, per-context requirement; 1−1 without a model is exact X. Legacy epsilon=c at c=0 is exact; c=1 is missing-model unchecked. |
| astra B2: general channel has no §4.4 unitary or controlled numerical claim | Keep native models unitary; a Kraus/instrument representation must identify phase-bearing U and prove reduced-map equivalence. X/√2, ZX/√2 mixes the plus state and fails that requirement; identical X/√2 Kraus operators with U=X can satisfy it. |

## Conformance vectors and exact verification

Keep X/−X under an outer control, all matrix units and external references;
exact X without a model, zero-valued epsilon AST, mixed-control epsilon,
missing approximate model, wrong dimensions/normalization/control or angle
bindings, target-model hash changes, malformed Kraus data, unitary-equivalent
Kraus data and rigorous inconclusive interval claims. Angle 0.1 binds
3602879701896397/36028797018963968, not 1/10.

Controlled X versus controlled −X has operator distance 2 and channel
diamond distance 2. §12.1's numerical procedure uses a Frobenius upper
bound 2√2, so its requested bound 2 rejects and bound 3 can pass at
sufficient interval precision. Controlled X versus itself can pass a
zero numerical bound. Equal uncontrolled channels do not make a zero-bound
channel SDP witness pass: retain §12.1's strict-positive-pivot rule and
strict-feasibility treatment. These distinguish mathematical distance
from the prescribed checker's acceptance procedure.

The script checks exact matrices, all uncontrolled matrix units, the
controlled phase witness, purity and rational angle/epsilon examples.
It neither evaluates the proposed model schema nor runs a numerical/SDP
checker; no new native-target implementation is claimed.

```python
from fractions import Fraction as F

I = [[1, 0], [0, 1]]
X = [[0, 1], [1, 0]]
Z = [[1, 0], [0, -1]]

def mul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]

def tr(a):
    return [list(r) for r in zip(*a)]

def neg(a):
    return [[-x for x in row] for row in a]

def ad(u, rho):
    return mul(mul(u, rho), tr(u))  # All entries in this witness are real.

assert mul(tr(X), X) == I and mul(tr(neg(X)), neg(X)) == I
for i in range(2):
    for j in range(2):
        e = [[int((a, b) == (i, j)) for b in range(2)] for a in range(2)]
        assert ad(X, e) == ad(neg(X), e)

# Basis 00,01,10,11: inherited control first.
def controlled(u):
    return [[(int(i == j) if i < 2 and j < 2 else
              u[i-2][j-2] if i >= 2 and j >= 2 else 0)
             for j in range(4)] for i in range(4)]

cx, cmx = controlled(X), controlled(neg(X))
start = [[1], [0], [1], [0]]  # sqrt(2) times |+>|0>.
a, b = mul(cx, start), mul(cmx, start)
assert a == [[1], [0], [0], [1]] and b == [[1], [0], [0], [-1]]
assert sum(a[i][0]*b[i][0] for i in range(4)) == 0
assert F(a[0][0]*a[3][0], 2) == F(1, 2)
assert F(b[0][0]*b[3][0], 2) == F(-1, 2)
# Frobenius squared of V-dagger U - I is 8; operator norm is 2.
r = mul(tr(cx), cmx)
assert r == [[1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,-1]]
frob2 = sum((r[i][j]-int(i == j))**2 for i in range(4) for j in range(4))
assert frob2 == 8 and 2**2 < frob2 < 3**2

# Kraus X/sqrt(2), ZX/sqrt(2): exact weighted-channel computation.
zx = mul(Z, X)
plus = [[F(1, 2)] * 2 for _ in range(2)]
one, two = ad(X, plus), ad(zx, plus)
mixed = [[(one[i][j]+two[i][j])/2 for j in range(2)] for i in range(2)]
assert mixed == [[F(1,2), 0], [0, F(1,2)]]
assert sum(mul(mixed, mixed)[i][i] for i in range(2)) == F(1, 2)
assert sum(mul(plus, plus)[i][i] for i in range(2)) == 1
assert [[F(mul(tr(X), X)[i][j]+mul(tr(zx), zx)[i][j], 2)
         for j in range(2)] for i in range(2)] == I
# Equivalent two-Kraus representation, with explicit U=X, on all units.
for i in range(2):
    for j in range(2):
        e = [[F(int((a,b) == (i,j))) for b in range(2)] for a in range(2)]
        u = ad(X, e)
        assert [[(u[a][b]+u[a][b])/2 for b in range(2)] for a in range(2)] == u
assert F(1)-F(1) == 0
assert [F(c) for c in range(2)] == [0, 1]
assert F.from_float(0.1) == F(3602879701896397, 36028797018963968)
assert F.from_float(0.1) != F(1, 10)
print('PASS native-model: exact zero epsilon; four matrix units; controlled phase; CPTP nonunitary/equivalent Kraus witnesses')
```

---

## Dossier part: checker-resource-contexts (run contract-checker-resource-contexts-2026-11-02; accepted by sol in round 1 and codex (astra) in round 2; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-02-rev/checker-resource-contexts.md)

# Checker resources — complete contexts and exact-rational display rules

Full revised proposal for council review, 2026-11-02; checker request 4
and `b-isa-spec-cwq`. Supersedes
`2026-11-02-contract-checker-resource-contexts.md`; proposal only.

## Defect classification and North Star scope

ISA 0.9 §12.1 enumerates complete invocation contexts, including default
coverage. §§11/12.3 permit a region under different arguments, budgets,
controls and schedule choices. Error entries already use common bounds
and explicit multiplicities. In contrast, flat region.resources and
gates_used maps do not choose an invocation or define a max/sum/common
bound. §8.2 defines event accounting but does not select the event list
for those maps. K12 binds an estimate's resources; it cannot choose the
meaning of another context's flat report.

A second gap predates this note: §12.3's resources {name:decimal} schema
has no encoding/comparison rule for non-terminating rational costs when
estimate is absent. §8.1 permits division, §8.2 aggregates rationals, and
§10.1 currently defines upward decimal encoding in the estimate contract.
The repair applies that encoding to every resources map, including old
single-context maps, while preserving exact accounting.

These are S0 contract gaps. North Star §§4.3–4.4/5.1 requires the complete
resource vector and substitutable scheduler/checker interfaces. Repeated,
controlled, default-covered and differently budgeted invocations stay
supported. Ignoring contexts, silently picking one or rejecting valid
rational costs cannot meet that scope. Unchecked reporting describes
verification status; it does not replace the repair.

## Alternatives and worked witnesses

| Choice | Consequence |
|---|---|
| Sum every child map | Misdefines peaks/makespan and double-counts nested leaves. |
| Common per-resource maximum | Could be a separately specified bound assertion; not exact event accounting. |
| Pick one context implicitly | Depends on traversal order and is not independently replayable. |
| Exact full-context records | Recommended; replay each event list and derive the root separately. |

Take `@flip(t)` with body `x t`. A root holds mutable t and in-role c
and executes these canonical instructions:

```text
action_call @flip (t) () () ()
qpred c
action_call @flip (t) () () ()
qunpred
```

At source points entry:0 and entry:2, each call contributes semantic
call_index=0 and instance=[], with no loop iterations. A native X entry
supports total controls 0..1, unit time, unit occupancy rate and sufficient
capacity in class fast. There are no other timed leaves; predicate-stack
instructions supply structural control. Its views are:

| Report | X native leaves | Time | Qubit-time | Peak |
|---|---:|---:|---:|---:|
| flip, forward, inherited controls 0 | 1 | 1 | 1 | 1 |
| flip, forward, inherited controls 1 | 1 | 1 | 2 | 2 |
| root, both interface wires live throughout | 2 | 2 | 4 | 2 |

The second child occupies root time [1,2) but reports its invocation-local
time 1. A zero-valued control still occupies its wire and scheduled gate
slot; these costs do not depend on a quantum predicate's basis value.
Summing child peaks gives 3 rather than 2; adding root and children
counts the same leaves twice. The second child includes its inherited
control in its footprint without transferring ownership from the caller.

Now set native duration to the legal expression {"op":"/","args":[1,3]}.
Child times are exactly 1/3; root time is 2/3. Child occupancies are 1/3
and 2/3; root occupancy is 4/3, with unchanged peaks. No finite decimal
can equal any of these thirds. Without estimate, exact decimal-vs-rational
equality would reject every legal time; the rule below instead compares
canonical displays of exact recomputed values.

As a borrow check, one wire lives over [0,2), borrowed during [0,1),
with owner rate 1 and dirty rate 1/4. Combined occupancy is 1/4+1=5/4,
not 9/4: borrower charges replace the owner's during that interval.

## Recommended exact spec changes (§12.3)

Add to each region record:

```text
resource_contexts?:[{context_key,resources,gates_used,estimate?}]
```

Add these normative rules, and a §0.2 repair entry RESOURCE-CONTEXTS:

```text
For exactly one invocation context, resources and gates_used report its
§8.2 scheduled event accounting. resource_contexts may be omitted; if
present it MUST have exactly one matching record. The root context_key
is []. A standalone verified resource report binds one invocation and
an effective §11 schedule, including an explicit empty-entries schedule
when defaults supply all decisions. A schedule-free reference claim
retains K13's reference-only meaning and is not target-resource evidence.

For more than one invocation context, resource_contexts MUST contain
exactly one record for every §12.1 context, in increasing bytewise order
of the JCS encodings of their complete keys. Include default-covered and
predicated-off invocations. Full identity includes resolved source
point, loop indices, fixed-binding instance, forward semantic-call
occurrence and oracle step/phase where applicable, not just variant and
inherited-control count. Resolve each context's own args, token budgets,
placements, cleanup, epsilon shares, schedule/default decisions, native
leaves and wire intervals. Recompute every declared resource and gate
count from that context. gates_used counts native leaves after scheme
expansion, each once, with existing scheme/error attribution unchanged.

For compatibility, unkeyed resources/gates_used/estimate MUST be the
first canonical context's projection. An optional estimate's presence
and value agree with that projection. The projection discharges only
that context. Missing, duplicate, reordered, foreign or mismatched
context records, or a conflicting projection, reject the requested
report. A singleton array, when present, follows the same validation.
```

### Exact arithmetic and canonical decimal comparison, even without estimate

Apply this paragraph to EVERY resources map: single-context fields,
resource_contexts entries, root maps and unkeyed projections. It repairs
the pre-existing decimal gap rather than leaving it to a separate issue.

```text
Whether or not estimate is present, accounting uses exact nonnegative
rational arithmetic. Each resources value is a canonical decimal string
using §10.1's 34-significant-digit upward encoding. For q>0, find integer
e with 10^e <= q < 10^(e+1), then display
ceil(q / 10^(e-33)) * 10^(e-33). Zero is "0". Spelling has ASCII digits,
an optional decimal point, no exponent/plus sign, leading integer zeros
except "0", trailing fractional zeros or negative zero.

The checker compares the producer's canonical string with the canonical
encoding of its independently recomputed exact rational value, not the
numeric displayed decimal with that exact rational. Noncanonical strings
or differing encodings reject. Resource-row keys and class qualification
retain §8.2/§10.1's vector and escaping requirements; no scalar sum
replaces a required per-class row. Capacity, matching, objectives and
resource calculations continue to use exact rationals. Never add rounded
child displays to compute an exact parent value.

When estimate is present, precision_digits is 34 and its reduced
exact_resources fractions MUST also equal the recomputed values, with
nonnegative numerator and positive denominator decimal strings and zero
as 0/1. K12's existing mandatory-estimate cases and complete class rows
remain mandatory. Optional estimate here does not weaken K12. Omitting
estimate elsewhere does not mean a decimal must be an exact rational
representation; it is the defined upper display enclosure.
```

Examples: 1/3 displays as
`0.3333333333333333333333333333333334`; 2/3 as
`0.6666666666666666666666666666666667`; 4/3 as
`1.333333333333333333333333333333334`.
An estimate's exact time for the first case is
`{"numerator":"1","denominator":"3"}`. These same displays are correct
when estimate is absent. Two rounded 1/3 displays sum to a different last
digit from the canonical encoding of exact 2/3; the latter is required.

### Root totals, child footprint views and time origin

```text
The root counts its realised event list once, including semantic callee
leaves. Child reports are independently checkable subtree/footprint views,
not extra costs added to the root. Measure child timing relative to that
invocation's entry, preserving internal delays in the effective schedule.
Restrict caller-owned interface and inherited-control lifetimes to that
invocation interval when displaying the child view. This neither
transfers ownership nor creates an additional charge to the root.
Within each view apply §8.2 dirty-borrow replacement: the borrower replaces
the owner's charge for that wire during the borrowed interval. There is
no second aggregation by summing child peak/time maps. Error-bound
multiplicities retain their existing separate composition rule.
```

## Concrete context/report fragment

Use a synthetic root closure hash of 64 `a` characters solely to display
context identity; it is not asserted as an actual object hash. The two
full child keys are:

```json
[
  [{"symbol":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","point":"entry:0","iteration":[],"instance":[],"call_index":0}],
  [{"symbol":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","point":"entry:2","iteration":[],"instance":[],"call_index":0}]
]
```

They sort in the displayed order. For duration 1, the corresponding
resource_contexts entries use these keys and respectively:

```json
[
  {"resources":{"peak_qubits[fast]":"1","qubit_second[fast]":"1","time":"1"},"gates_used":{"x":{"count":1}}},
  {"resources":{"peak_qubits[fast]":"2","qubit_second[fast]":"2","time":"1"},"gates_used":{"x":{"count":1}}}
]
```

The child's unkeyed projection is the first record. Root unkeyed fields
are `resources={"peak_qubits[fast]":"2","qubit_second[fast]":"4","time":"2"}`
and `gates_used={"x":{"count":2}}`; its own context key is []. These are
schema fragments, not a complete bound certificate. Actual source,
target, schedule hashes, claims and frames must be supplied before
checker execution; fabricated hashes do not verify an executable.

## Mixed fat object (bennett-4ht)

Add to §§9/10/12: "A native host binary can embed VM objects only for
marked modules. A launch manifest selects an exported VM entry and its
schedule/target; that selected VM invocation is the resource-report root,
with context_key=[]. Its certificate inventory covers its VM closure and
all generated invocation contexts, not every native entry or libc routine.
Unmarked host main, argv/envp and ordinary host work remain native. A host
shim supplies the bound handles, args, images and budgets before launch.
Only costs within the bound VM realisation, including effects/transfers
actually represented by that contract, enter its vector. Separately
reported host/launch overhead must have an explicit scope and is not
silently claimed as included. Native comparison selects the corresponding
materialized marked entry; resource reporting does not require a whole
native-binary schedule or VM certificate."

For the two-flip witness, the host calls a marked root in one module;
its report still includes both child contexts even if the surrounding
binary contains unrelated native modules. A second marked launch has its
own root binding and certificate; reports are not merged by region name.

## Round-1 blocking items and resolution

| Item | Change and concrete witness |
|---|---|
| astra RC-1: no non-terminating rational encoding without estimate | Apply §10.1 upward decimal encoding and recomputed-encoding comparison to every resources map; optional exact_resources must equal the rational too. Native duration 1/3 gives valid child/root thirds both with and without estimate. |

All accepted context/projection, root aggregation, default coverage and
error-composition rules remain. Round-1 footprint, time-origin,
singleton and borrow clarifications are made explicit above.

## Hashes, publication and consumer work

Recommend an authorized 0.9 K certificate repair alongside the distinct
fault-rate binding repair. New context/encoding bytes change certificate
and report digests. With an unchanged semantic envelope, §9.2 excludes
certificate bytes from object_hash: source/interface/closure/object,
target, schedule and ref catalog bytes/identities need not change.
A full-version publication instead regenerates version-envelope identities
and dependent pins. The note performs neither publication nor migration.

Scheduler, estimator, plugin and checker retain full keys, canonical
ordering and K12's class-qualified keys. Old repeated-context flat reports
need recomputation, never a guessed max/sum. Existing exact integer
reports can be migrated to canonical strings; non-terminating costs use
the same explicit rule regardless of estimate presence. The existing
request/cwq implementation obligation remains open; accepted source
semantics and the full demo ladder are unchanged.

## Conformance vectors and verification

Require integer and duration-1/3 cases, estimates present/absent, singleton
arrays, root [], unused target classes, borrowed intervals, repeated
semantic occurrences, lproc fixed instances, default coverage and nested
token budgets differing under one (variant,controls) pair. Swap/omit/
duplicate/relabel a context or mismatch its estimate/projection: reject.
Reject truncated thirds, noncanonical displays, wrong exact fractions,
rounded-display summation and duplicate leaf charging. Root and child
resource charges are independent of control basis values.

The script independently checks rational accounting, decimal encodings
and concrete context identities. It does not execute a new scheduler or
certificate checker, and the fragments above are not claimed as an
accepted fixture.

```python
from fractions import Fraction as F
import json

def pow10(e):
    return F(10**e) if e >= 0 else F(1, 10**(-e))

def display(q):
    q = F(q)
    assert q >= 0
    if not q:
        return '0'
    e = 0
    while q < pow10(e):
        e -= 1
    while q >= pow10(e+1):
        e += 1
    unit = pow10(e-33)
    z = q/unit
    ceiling = (z.numerator + z.denominator-1)//z.denominator
    rounded = ceiling*unit
    k = max(0, 33-e)
    n = rounded*10**k
    assert n.denominator == 1 and rounded >= q
    s = str(n.numerator)
    if k:
        s = s.zfill(k+1)
        s = (s[:-k] + '.' + s[-k:]).rstrip('0').rstrip('.')
    return s

expected = {
    F(0): '0', F(2): '2', F(1,8): '0.125',
    F(1,3): '0.3333333333333333333333333333333334',
    F(2,3): '0.6666666666666666666666666666666667',
    F(4,3): '1.333333333333333333333333333333334',
    F(1,30): '0.03333333333333333333333333333333334',
    F(10,3): '3.333333333333333333333333333333334'}
for q, encoded in expected.items():
    assert display(q) == encoded
assert F(display(F(1,3))) != F(1,3)
assert 2*F(display(F(1,3))) != F(display(F(2,3)))
for d in (F(1), F(1,3)):
    # (time, occupancy, peak), wire live intervals as declared above.
    children = [(d, d, 1), (d, 2*d, 2)]
    root = (2*d, 4*d, 2)
    assert sum(c[0] for c in children) == root[0]
    assert sum(c[2] for c in children) != root[2]
    assert root[1] == 2*root[0]
    if d == F(1,3):
        assert [display(v) for v in root] == [expected[F(2,3)], expected[F(4,3)], '2']
assert F(1,4)*1 + 1*1 == F(5,4)
assert F(5,4) != F(9,4)
keys = [[{'symbol':'a'*64, 'point':f'entry:{p}', 'iteration':[],
          'instance':[], 'call_index':0}] for p in (0, 2)]
jcs = lambda v: json.dumps(v, sort_keys=True, separators=(',', ':'))
assert keys == sorted(keys, key=lambda k: jcs(k).encode())
assert jcs(keys[0]) != jcs(keys[1])
print('PASS resources: integer/thirds context and root costs; eight canonical displays; borrow replacement; full keys')
```

---

## Dossier part: 0jq (run pass2-0jq-2026-11-02; accepted by sol, codex in round 2; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-02-rev2/b-isa-spec-0jq.md)

# 0jq — structural-only certificates and the owner of an inverse-pair proof

Council proposal for `b-isa-spec-0jq` (P1); no normative text is changed.

## Round-1 blocking items and resolution

Read the [round-1 report](../../../../bennett/docs/council/pass2-0jq-2026-11-02/round-1/report.md)
and both `out-sol.json` and `out-codex.json` in that directory. The table
maps every blocking item to this revision; it claims a proposed resolution,
not a new council verdict.

| Item | Change and witness |
|---|---|
| sol 0JQ-1; codex B1 — device-object/root inventory missing | Append the §12.3 mixed-object rule below and cross-reference it from §9.2. Witness: native main calls device A and B; the two object/root certificates inventory device owners only, with no main region. |

## Defect and North Star scope

ISA 0.9 §12.1 admits structural `adjoint_table` and `translation_lemma`
claims; §12.3 K13 explicitly admits standalone structural claims without a
schedule. However, §12.3's region schema requires `verification.oracle: i`
and `fault_rate`, without an applicability rule or a no-claim encoding.
An action has no fault outcome (§5.3), and an adjoint-table proof does not
assert an oracle relation or a fault census. In addition, §9.2 defines
`reference_program_hash` as **the oracle's** interface hash although the
required §12.3 binding also occurs in action certificates. These are
contract gaps (rubric C5/C8). The published controlled-action fixture
already uses `oracle:null`; that practice needs normative wording.

The ownership part of the request is **already substantially decided**:
§4.5 `qinplace` puts `inverse_pairs` in the certificate record of the
region whose body contains the instruction, including when that region is
nested. §9.3 requires linked certificate composition. K63's two call
occurrences and K65's private-cleanup exclusion do not move that owner to
either oracle or to an outer caller. A packet transport convention is
needed only to identify the linked owner record, not a new proof owner.

North Star §§4.2/4.4/5.1 requires general quantum actions, composable
certificates, and honest proof/evidence labels. Forcing a non-permutation
action to fabricate an oracle/T3 claim narrows that scope. The proposed
absence encoding preserves each capability and every remaining obligation.

## Alternatives and worked witness

Take an action with body `h t`. The adjoint table establishes that its
source adjoint is `h t`; H²=I follows exactly from §4.4. It does not
establish a permutation assertion: H|0>=(|0>+|1>)/sqrt(2). Putting that
structural claim's index into `verification.oracle` would change its
meaning. A fault count of zero on an invented domain also asserts a
census that was never performed.

For ownership, let `outer` call `inner`, and let only `inner` contain
`qinplace @G @H tk x`. The covering entry belongs to
`regions[closure(inner)].verification.inverse_pairs`. Its `claim:i`
indexes **inner's** claims array. A same-numbered claim in outer is not
that claim. Two visits to inner resolve their own token/argument coverage;
a proof at budget 2 does not cover an argument-token tuple 3 merely
because the outer root uses 3. The existing componentwise bound for the
instruction's primary token and exact `arg_tokens` rule still apply.

| Alternative | Result |
|---|---|
| Require a dummy oracle claim or zero fault report | Misrepresents the assertion; reject. |
| Make the two verification entries nullable/conditional | Preserves structural-only packets and existing applicable checks. Recommended. |
| Put nested entries/claims in the outer region record | Contradicts §4.5's owner and makes claim indices ambiguous. |
| Resolve linked owner records by closure hash | Uses the existing `regions` map and §9.3 composition. Recommended. |

## Recommended exact spec diff

Replace §9.2's definition and the indicated §12.3 schema fragments:

```diff
-`reference_program_hash` = the oracle's interface hash.
+`reference_program_hash` = the interface hash of the certificate's
+root reference subject, oracle or action. It is not the hash of a
+claim's separate expected program. `closure_hash` remains required.

-verification: { oracle: i, ... fault_rate: { ... } }
+verification: { oracle: i | null, ... fault_rate?: { ... } }
```

Append to §12.3:

```text
verification.oracle is null when this record makes no oracle/table/
program comparison claim. A non-null index must name an applicable
exhaustive or sampled comparison claim in this record's claims array;
its explicit expected relation determines its meaning. A structural
adjoint-table or translation claim is not such a comparison claim.
fault_rate may be absent when no oracle fault census is asserted.
Its absence asserts neither zero faults nor a checked census. For action and perm_action records, fault_rate MUST be absent. An action
has no fault outcome of its own; a nested oracle's census belongs to
that oracle and its resolved invocation. Applicable oracle-correctness,
fault-rate, borrowed-system and realisation obligations remain required
before an executable or algorithm acceptance claim can use them.
An explicitly supplied fault_rate must be validated even when optional.

The owner of a qinplace inverse-pair entry is exactly the region whose
source body contains that instruction (§4.5). After linking, select that
region's record by its exact closure hash in the composed regions map;
claim indices are local to that record. Imported proofs must be present
in the linked certificate, or reached by the existing checked
inverse_pair_library reference to its linked library certificate.
Conflicting records for one closure must not be chosen arbitrarily:
resolve them by §9.3 composition or reject the composition. An outer
record, an oracle callee record, and the two private qinplace call edges
cannot substitute for the owner. Before any effect of the enclosing CC/R region call, check coverage for
every transitively executed qinplace using its owner entry and resolved
token and classical arguments (§4.5). Failure is a CC trap or R
FAULT_UB_TRAP; validation cannot wait until after earlier effects.
```

This wording does not make an adjoint-table claim a proof of the
instruction's inverse-pair obligation, or turn numerical agreement into
an exact structural proof. `unitary` and `channel` retain their own
applicable claim types. Fault-rate invocation encoding is handled by
[jw7](../2026-11-02-pass2/b-isa-spec-jw7.md), not invented again here.

## Fat-object applicability

Incorporate [the shared scoping statement](fat-object-scope.md#citable-scoping-statement).
Append the following proposed normative paragraph to §12.3, cross-referenced from §9.2:

```text
For a mixed fat object, object_hash identifies the embedded or linked ISA
object, and bindings.closure_hash selects its certified device root.
reference_program_hash identifies that oracle or action root's interface,
not native main or a separate expected program. The container associates
each object/root pair with its certificate; several device roots may have
separate certificates. Each composed regions map contains the required
device-region owner records and checked linked-library proofs. Native-only
host code, argv/envp and host-only libc require no region record, oracle
comparison, fault census or inverse-pair entry.
```

The shared statement lists today's assumptions and the exact remaining
container, launch, budget, handle, tape and host-memory contract changes.
This note does not assume that the device object is the entire binary.

## Hashes, catalog and consumers

No source, interface, closure, target, schedule or `ref@0.9` catalog bytes
need change under an authorized in-version repair. Removing an inapplicable
fault report or choosing null changes certificate bytes. Linkers,
specialisers and checkers must preserve owner-local claim indices and
resolve linked library proofs before use. Old ambiguous standalone action
bindings need explicit validation, not silent reinterpretation.

## Conformance vectors and verification

Require structural H and translation-only packets with `oracle:null` and
no fault census; reject a structural index masquerading as an oracle
comparison. An absent census must not satisfy a rung's zero-fault gate.
For outer→inner→qinplace, accept the covering entry in inner; reject an
outer-only entry, dangling library reference, changed G/H closure,
uncovered token argument and claim index into another record. Test two
inner contexts, swapped G/H, inherited control, and default-covered calls.

The H² and non-permutation facts are exact algebra checked by
[check_rev2.py](check_rev2.py). The originating note cites:
`../bennett-circuits/docs/design/2026-11-01-m5-contract-requests.md`,
“Structural-only packets”. No new packet checker is implemented here. A composed root packet may
contain inner's correctly keyed owner record; packet containment does not
move the entry into the outer region record. For the published controlled-action
fixture migration, the root table claim at index 0 gives verification.oracle:0;
the numerical-only flip record retains null, and both action fault-rate
placeholders are omitted. These are proposed certificate changes only.

## Release and route

Recommend a **0.9 K applicability/hash-definition repair**. The owner rule
needs clarification and link/consumer tests, not a new proof mechanism.
Keep 0jq open for council acceptance and producer/checker implementation.
The publication rules below apply.

## Publication and validation boundary

This is a revision proposal, not council acceptance or a consumer implementation.
The default publication rule in spec/README.md requires a full version bump
for semantic changes. The recommended 0.9 K route requires explicit council
and maintainer authorization of its in-version compatibility rules; this note
does not grant it. All unchanged-hash claims assume unchanged header/source
and catalog envelopes. A full version publication recomputes affected symbol,
object, target, schedule, certificate and versioned ref-library identities and
consumer pins even when recipe bodies stay fixed. Published 0.9 bytes remain
available; older closed-schema readers require an upgrade for new fields.

The reproducible finite and document checks are in [check_rev2.py](check_rev2.py):
`timeout 120 python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/notes/2026-11-02-rev2/check_rev2.py`.
Executed for this revision: exit 0, all eight PASS result lines.
These finite checks verify witnesses and revision structure; they implement
no proposed-format checker or host shim. No full repository gate or sibling gate is claimed: scripts/pre-push
uses git/worktree writes, forbidden by this runner, and its setup changes paths
outside this job. Underlying beads remain open for publication and consumers.

---

## Dossier part: 4ta (run pass2-4ta-2026-11-02; accepted by sol, codex in round 2; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-02-rev2/b-isa-spec-4ta.md)

# 4ta — one interface slot placed across several classes

Council proposal for `b-isa-spec-4ta` (P1).

## Round-1 blocking items and resolution

Read the [round-1 report](../../../../bennett/docs/council/pass2-4ta-2026-11-02/round-1/report.md)
and both `out-sol.json` and `out-codex.json` in that directory. The table
maps every blocking item to this revision; it claims a proposed resolution,
not a new council verdict.

| Item | Change and witness |
|---|---|
| sol 4ta-B1; codex B1 — §3.3 says one class per register but concat has no same-class condition | Replace the register/ledger definition and specify new/concat/slice/free/reversal and frame-binding vector equality below. Witness: new A[1], new B[1], concat yields [A,B], split maps 0 to 3; inverse execution restores original wires, classes, ids and handle states. |
| sol 4ta-B2; codex B2 — missing mixed-object descriptor scope | Append the §9.4 rule below. A native host launches a device CC wrapper that joins the two registers and calls the single split slot; host functions remain outside B5. |

## Defect and North Star scope

ISA 0.9 §11 “Topology placement” supplies one vertex **per bit**, in
§9.4 slot order, and callees inherit actual operand placements. §8.3
assigns a class to each vertex. Neither clause requires all bits of a
source interface slot to have the same class. B5 (§9.4), however, gives
each slot exactly one `class` and its full signature `width`; unknown
fields and duplicate slot identities are not an extension mechanism
(§9.1). A legal mixed placement has no truthful descriptor. This is a
contract defect under C4/C5/C8, distinct from [v2v](b-isa-spec-v2v.md):
4ta concerns different bits **within one invocation of one slot**.

North Star §§4.1/4.3/4.4 promises virtual memory, allocation classes and
target-driven placement/resource reporting. Splitting a virtual slot
must not require a user rewrite or a target with a larger homogeneous
class. Class capacities still constrain physical feasibility; no capacity
is manufactured by this repair.

## Alternatives and worked witness

An action `split(t:wire[2] mut)` applies `x t[0]` and `x t[1]`.
A target has two vertices, 0:A and 1:B, each class capacity 1, and exact
single-wire X entries of duration 1 for either class. Placement
`interface_vertices:[[0,1]]` is legal: there is no multi-wire adjacency
requirement to satisfy. Both bits stay live for two sequential slots.
For unit class rates, time=2, peak[A]=peak[B]=1 and
qubit_second[A]=qubit_second[B]=2. On the four values t=0,1,2,3, the
outputs are respectively 3,2,1,0; the adjoint restores every input.

One B5 record `class:A,width:2` lies about bit 1 and exceeds A's capacity;
class B has the symmetric problem. Two `mut:0` records lose uniqueness;
two new source slots change the interface and its hashes unnecessarily.

| Alternative | Tradeoff |
|---|---|
| Ordered per-bit class vector | Precise, but repeats one class name per bit. |
| Ordered maximal class fragments | Precise, compact for runs, retains the source slot. Recommended. |
| Require a homogeneous class or split the source signature | Removes this legal placement or changes the program interface. |

## Recommended exact spec diff

First replace §3.3's singular-class register definition and update every
ledger-frame reference to class as follows (including §10's allocation
cross-reference):

```text
A register denotes an ordered vector of n device-resident wires with a
resolved target class for each wire. The register ledger records that
class vector, width, nonzero id and live/viewed/consumed state. A single
class is shorthand for a homogeneous vector. qreg.new cls n and
bennett_qreg_new allocate n wires of cls and remain homogeneous requests.
qreg.concat accepts differing operand classes and concatenates their
wire and class vectors in operand order, with no movement, copy,
measurement or reallocation. Its existing distinct/live/non-view
preconditions and consumption/new-id transitions remain unchanged.
qreg.slice selects the corresponding wire/class subsequences, with its
existing view ownership and one-call consumption rule. A slice never
relabels a wire. Zero-width runtime registers have empty vectors.
Ledger frames retain enough information to restore the complete class
vectors, wire ordering, identities and handle states. In particular free
records/restores the vector along with the same id/width and cleanliness
status; concat reversal restores both operands and their prior vectors;
slice reversal restores the parent/view states. New-frame reversal keeps
its existing cleanliness/exclusivity hypothesis.
Binding a CC/R register to a region slot requires its ordered class
vector to equal that slot's selected, expanded §9.4 class vector, and,
with topology, its actual vertices to equal the inherited placement.
Check this with the existing width/disjointness preflight before any
effect or view consumption. Class vectors introduce no new alias or
storage-sharing permission, nor permission to relabel or move a wire.
```

Then in §9.4 replace the `slots` record production with:

```text
{id, role, width, class} |
{id, role, width, fragments:[{offset, width, class}, ...]}
```

Append:

```text
Each source slot still has exactly one record, its original id and role,
and its complete signature width. Exactly one of class and fragments
is present. class abbreviates one fragment at offset 0 covering width.
For the fragmented form, fragment offsets and widths are nonnegative
and positive integers respectively, using §9.1 integer encodings.
Fragments are in increasing offset order, start at 0, meet without gaps
or overlap, and end at the instantiated slot width. Each class is a
resolved declared target class. Adjacent equal-class fragments must be
merged; use the class form when there is only one fragment.

Flatten bundle bits LSB first, or region cells in address order and
each cell LSB first, exactly as for the existing slot. A fragment names
the class of that half-open bit interval; it is not a new source slot,
allocation, lifetime, alias or permission to share storage. Repeated
slot ids, wrong roles/widths, gaps, overlaps or out-of-range fragments
reject. Slot widths retain §8.1's c-only expression rules; fragment
widths/offsets describe the resolved fixed signature width.

With topology, every bit's fragment class must equal the class of its
§11 vertex; vertices and simultaneous live uses remain disjoint. A
callee's fragments must equal the inherited operand-class vector. In
the absence of topology, they bind that resolved vector without naming
vertices. Capacity, occupancy and peak accounting use each bit's actual
class, and charge no wire twice. Existing homogeneous records and
scratch/history/borrow/ancilla schemas retain their meanings.
```

The witness descriptor is one slot
`{id:"mut:0",role:"mut",width:2,fragments:[{offset:0,width:1,class:"A"},`
`{offset:1,width:1,class:"B"}]}`. This is proposed record notation;
the production's field names are exact. It is not accepted B5 today.

## Fat-object applicability

Incorporate [the shared scoping statement](fat-object-scope.md#citable-scoping-statement).
Append the following proposed normative paragraph to §9.4:

```text
In a mixed fat object, B5 descriptors cover device-region invocations
in the embedded or linked ISA objects, bound to their object, closure,
schedule and invocation identities. Native host functions and process
state require no ISA frame slots or certificate records. A native host
may launch a device CC entry under §10; that entry may concatenate
homogeneous A and B registers under §3.3 and bind their ordered class
vector to one source slot. The fragments describe that binding without
splitting its signature. Native main, argv/envp and host-only libc stay
outside the device-frame inventory. This rule supplies no new container
or general host-memory launch ABI.
```

The shared statement lists today's assumptions and the exact remaining
container, launch, budget, handle, tape and host-memory contract changes.
This note does not assume that the device object is the entire binary.

## Hashes, catalog and consumers

The register-class rule is a core clarification/extension requiring renewed
core council review; B5 alone cannot make the slot usable. The
slot/signature/source closure stays the same for the unchanged split body. A repaired certificate
changes bytes; its existing placement schedule and target need not.
No reference recipe, leaf ordinal or catalog hash changes. Circuits,
scheduler, estimator and checker must validate fragments against the same
bit ordering and retain class-qualified resource rows. This does not
alter the explicit class of a source `qalloc` or add routing.

## Register construction and reversal witness

In a device CC wrapper allocate a=qreg.new A 1 and b=qreg.new B 1,
then t=qreg.concat a b and action_call @split (t) () () (). The two
homogeneous allocations each fit capacity 1. Concat consumes a,b and
creates a fresh t over the same ordered wires with classes [A,B]; its
mut:0 descriptor expands to exactly that vector. From initial clean 0,
the call produces 3; on 0,1,2,3 it gives 3,2,1,0. Reverse the action,
then concat, to restore a,b live with their original ids, [A]/[B]
classes and wire order, with t no longer live; reversing allocations
then releases their clean wires under the existing ledger rule.
A slice of t inherits its selected class subsequence. A false [A,A]
frame fails before effects rather than relabelling the B wire.

## Conformance vectors and verification

Test the four outputs and inverse above, both topology and class-only
descriptors, a region[1,2] slot with four flattened bits, and a homogeneous
legacy record. Reject a gap, overlap, width zero, split duplicate id,
incorrect class for a vertex, reversed offset order and adjacent unmerged
runs. For region[1,2] use vertices/classes [A,B,A,B], capacity 2 per class;
offsets 0,1,2,3 denote cell0.bit0, cell0.bit1, cell1.bit0, cell1.bit1.
For a controlled invocation enlarge the target to vertices 0:A,1:B,2:C,
capacity 1 each, edges [0,2] and [1,2], and exact controlled-X leaves of
duration 1. The control is caller-owned, outside mut:0;
(c,t) maps to (c,t XOR (3*c)), time=2 and occupancy=2/peak=1 in each class. Exact finite arithmetic is
checked by [check_rev2.py](check_rev2.py); no target/scheduler implementation
is executed here.

The originating note cites circuits' `docs/design/2026-11-01-m5-contract-requests.md`,
“Heterogeneous interface-slot frames”. Its reported refusal records
incompleteness, not a new legality rule for source programs.

## Release and route

Recommend a **0.9 K/B5 encoding extension** alongside v2v; the gaps are
independent and both require vectors. Waiting for 0.10 leaves an explicit
blocker for complete 0.9 certificates, not permission to omit mixed
placements. Keep 4ta open for council and consumer work.

## Publication and validation boundary

This is a revision proposal, not council acceptance or a consumer implementation.
The default publication rule in spec/README.md requires a full version bump
for semantic changes. The recommended 0.9 K route requires explicit council
and maintainer authorization of its in-version compatibility rules; this note
does not grant it. All unchanged-hash claims assume unchanged header/source
and catalog envelopes. A full version publication recomputes affected symbol,
object, target, schedule, certificate and versioned ref-library identities and
consumer pins even when recipe bodies stay fixed. Published 0.9 bytes remain
available; older closed-schema readers require an upgrade for new fields.

The reproducible finite and document checks are in [check_rev2.py](check_rev2.py):
`timeout 120 python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/notes/2026-11-02-rev2/check_rev2.py`.
Executed for this revision: exit 0, all eight PASS result lines.
These finite checks verify witnesses and revision structure; they implement
no proposed-format checker or host shim. No full repository gate or sibling gate is claimed: scripts/pre-push
uses git/worktree writes, forbidden by this runner, and its setup changes paths
outside this job. Underlying beads remain open for publication and consumers.

---

## Dossier part: 7s0 (run pass2-7s0-2026-11-02; accepted by sol, codex in round 2; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-02-rev2/b-isa-spec-7s0.md)

# 7s0 — bind a restricted-domain proof to an actual borrow frame

Council proposal for `b-isa-spec-7s0` (P1).

## Round-1 blocking items and resolution

Read the [round-1 report](../../../../bennett/docs/council/pass2-7s0-2026-11-02/round-1/report.md)
and both `out-sol.json` and `out-codex.json` in that directory. The table
maps every blocking item to this revision; it claims a proposed resolution,
not a new council verdict.

| Item | Change and witness |
|---|---|
| sol B1; codex B1 — entry_products has no sampled draw/word-consumption rule | Define one union-rank rejection draw, complete B-fiber replays with no random words, and primary-tuple coverage below. Both published seeds select rank 2 / (1,1,0), which CX(c,b) fails. Overlap witness has six distinct tuples, not eight. |
| sol B2; codex B2 — missing mixed-object proof inventory | Append the §12.3 attachment rule below. Frame lifetimes/occurrences resolve in the launched device closure; native main has no borrow-frame claim. |

## Defect and North Star scope

ISA 0.9 §5.6 K76/K78 defines a borrow frame's entry domain D_F and
explicitly permits restricted-domain T3 factorisation proofs. §12.2
says to use D_F for that obligation. But K69/K70 resolves `bundles` and
`regions` only to interface components, and `borrowed` only to lifetime
positions. There is no field selecting a frame or a local workspace
entry value. §12.3 `borrow_frames:[i]` gives only claim indices.
The structural translation witness selects `frame` and B, but its special
V;W;V⁻¹;W syntax cannot represent every admitted finite T3 proof. This is
a concrete certificate expressibility gap (C3/C5/C6), not a defect in
K76's already specified analysis.

North Star §§4.3/5.1 promises dirty borrowing with restored correlations
and frame-local proofs. Neither banning these frames nor promoting a
whole-region basis check into a frame proof preserves that capability.
All interface and borrowed values remain independent and full; only the
normative entry analysis may restrict allocated local values.

## Alternatives and worked witness

Allocate clean c, borrow b, execute the single-gate frame `cx c b`, then
return b and free c. K76 establishes c=0 at frame entry. The two states
`(c,b)=(0,0),(0,1)` are unchanged with exact +1 amplitude, so on D_F
the map factorises as I_c⊗I_b, including arbitrary external entanglement.
This is not a four-part translation-lemma witness. An interface domain
cannot name c; choosing a whole-region input domain does not select
the CX frame either.

Negative prefix: `cx a c; cx x c; cx a c; cx x c` clears c by Boolean
algebra, but K76's all-operand causal stacks do not establish that
constant (the a and x events interleave on c). Thus c is unknown in
normative D_F: all four `(c,b)` values must be checked. At c=1 the
frame flips b, so the borrow proof fails. K78's `cx`/`mcx` identity
normalisation enables exact adjacent adjoint pops, not this stronger
polynomial inference. A phase depending on b would also fail identity
on its entangled reference even if printed basis values agreed.

Union witness: two visits can establish local `(c,d)=(0,0)` and `(1,1)`
respectively. The frame `cx c b; cx d b` restores arbitrary b on both
entry products, hence on their union. It flips b on `(0,1)` or `(1,0)`;
replacing that non-Cartesian union by its rectangular hull could produce
a false counterexample. Conversely checking only the first product
cannot establish the required union. A two-trip body that borrows/returns
b and then flips both initially clean locals supplies these entry facts
and restores the locals after the second trip.

| Alternative | Assessment |
|---|---|
| Strengthen entry analysis to prove the negative prefix clean | Changes K76 and conceals a failing normative frame proof. |
| Restrict proof syntax to the translation lemma | Drops valid CX(c,b) at c=0. |
| Add a selected-frame relation and local entry components | Expresses exactly the existing obligation. Recommended. |

## Recommended exact spec diff

Add to §12.1's exhaustive and sampled productions:

```text
expected:"borrow_frame",
borrow_frame:{lifetime:k,first:<resolved source occurrence>,
              last:<resolved source occurrence>,
              context_key?:<fully resolved §12.1 invocation key>}
```

Add to §12.2 domains, only for this expected relation:

```text
workspace:[{allocation:<resolved allocation occurrence>,offset:n,
            width:n,lo:n,hi:n}, ...]
```

For a non-Cartesian D_F, additionally permit
`domain:{entry_products:[<product-domain>,...]}` instead of one product;
each product has the existing component fields plus `workspace` above.

Append the following normative text:

```text
A borrow_frame claim identifies the checked borrowed lifetime k in
K69/K70 allocation order and the exact maximal §5.6 frame realisation
being checked. Source occurrences include the full
invocation chain, fixed instance and source-loop iteration; oracle
step/phase are included where applicable. They are source coordinates,
not target-scheme leaf ordinals. The first/last points must equal the
frame determined by §5.6, not a selected subinterval. A schedule-bound
claim MUST carry context_key, equal to the fully resolved §12.1 subject
invocation key ([] at the device root); first and last belong to that
invocation. A standalone claim MUST carry the complete K13 invocation
binding for all classical arguments and budget components. Missing or
conflicting bindings reject before replay.

workspace components resolve to allocated local wires live at frame
entry, including flattened local-region storage, excluding interface
and borrowed wires. allocation is the source/expansion allocation
occurrence with its current lifetime, never a reusable storage address.
Offsets/widths select nonempty disjoint intervals within that allocation.
All components use K71's exact width/range checks. In a product enumerate
bundles, borrowed, regions and then workspace in their listed order, last
component fastest; region cells retain §12.2 ordering. This order is also
the component order for Cartesian sampled borrow_frame domains.
The checker computes D_F by K76/K78, including its normative
union over repeated visits, never from the claimed constants. Correspond
local identities by their source lifetime and bit position across visits.
entry_products denotes the union of its product domains: list products
in normative visit order, enumerate each by §12.2, and skip complete
entry tuples already enumerated. It cannot be combined with top-level
product fields. To discharge the frame obligation this union must equal
the normative D_F, with every interface and
borrowed component full and independent and every local entry component
explicitly covered. A strict subset is evidence only. An omitted local
component is fixed at zero for replay and cannot silently supply full
coverage of an unknown component.

For sampled borrow_frame claims using entry_products, form the ordered,
deduplicated enumeration E above and let N=|E|. Each primary draw uses
§12.1's existing rejection sampler on one synthetic integer component
[0,N-1], then selects E[rank], with replacement. Consume no product-choice
or per-component words in addition to that rank draw; N=1 consumes no
words. This rule is exact even when a host must report K75 rather than
materialise E. It does not cap N.

For every primary draw (from a product or entry_products), fix its
non-B entry values and replay the entire B fiber of the claimed domain.
Check B restoration, exact +1 phase and identical complete non-B outputs
across the fiber. Auxiliary B replays consume no generator words and are
not additional primary draws. A changed B value or phase rejects even
before other fiber comparisons. A missing B value cannot discharge the
full-frame obligation. Record exactly sampler.count primary draws and
coverage = number of distinct primary complete tuples / |D_F|; auxiliary
fiber replays do not increase that count or fraction. Overlapping products
never count the same complete tuple twice. Sampled success is always
evidence, including coverage 1; requesting proof rejects.

Replay the selected realised permutation frame from each exhaustive entry element.
Record every surviving output and check all internal release obligations.
Locals surviving this frame need not be zero at its boundary: they are
complete non-B outputs. Region-exit cleanup remains mandatory.
For fixed non-B entry values, varying B over all its values must leave
B unchanged and produce the same complete non-B output, with exact +1
basis phase. This establishes P' tensor I_B on span(D_F); an oracle
relation, output projection or same-input self-comparison does not.
Non-permutation frames cannot discharge this T3 relation.

An exhaustive successful complete-domain claim receives proof for that
selected frame realisation; sampled claims remain evidence and cannot discharge it.
verification.borrow_frames must resolve to covering proofs for every
required maximal frame and every visit/context, or to an applicable
existing structural/library proof. Each selected realisation must pass
on the complete normative D_F, not only on the entry states reachable
at that one visit. A checker may share one verified relation between
visits only after checking equality of their realised frame operation,
wire correspondence and complete required domain. Different schedules
or effective controls are not presumed to supply that equality.
```

The checker needs no expected-output table for `expected:"borrow_frame"`:
the tensor-factor test itself defines the relation. This avoids pretending
that a reference program can receive local c through an interface slot.
Existing K13 before/after tuples for other relation kinds stay unchanged.
A host unable to complete the legal domain uses K75's unchecked outcome,
not a source restriction or a proof from fewer rows.

## Fat-object applicability

Incorporate [the shared scoping statement](fat-object-scope.md#citable-scoping-statement).
Append the following proposed normative paragraph to §12.3:

```text
In a mixed fat object, borrow_frame claims attach to the device-region
certificate records of the identified embedded or linked ISA object and
launched device-root closure. Source occurrences, allocation lifetimes
and invocation contexts resolve within that closure. Required frames of
the complete device closure remain covered, including default-covered
calls. Native main and unmarked host-only code require no ISA region or
borrow-proof inventory. The selected device launch determines the root
and invocation; it does not make the native binary an ISA object.
```

The shared statement lists today's assumptions and the exact remaining
container, launch, budget, handle, tape and host-memory contract changes.
This note does not assume that the device object is the entire binary.

## Seeded sampling witness

Use E=[(0,0,0),(0,0,1),(1,1,0),(1,1,1)] in (c,d,b) order.
For xoshiro256** seed `["0","288230376151711744","0","0"]`, first word
is 90. For seed `["1","72057594037927936","0","0"]`, the first two
words are 9223372036854775826 and 9223372036854781586. Either seed's
first union rank is 2. CX(c,b) maps selected (1,1,0) to (1,1,1), so the
claim rejects. A product-first reading would select product 0 and could
succeed on its B fiber; that reading is now explicitly excluded.

An overlap vector uses products {c=0,d∈{0,1}} and {c∈{0,1},d=0}, with
full one-bit B. Its deduplicated E has six tuples rather than eight.
One successful primary draw has coverage 1/6, even after replaying its
entire B fiber. The two-CX frame in the earlier union witness succeeds
on all four tuples of its complete D_F.

## Hashes, catalog and consumers

New claim fields change certificate bytes only. Source/closure identities,
ref catalog, K78 operation normalisation and schedule leaves stay fixed.
Checkers and producers must agree on lifetime/occurrence resolution and
the exact D_F, including repeated visits and inherited controls. Sharing
physical borrow storage never merges logical lifetimes or proof indices.

## Conformance vectors and verification

Positive: the two c=0 rows; adjacent `cx a c; mcx (a) c` restores the
entry constant by K78. Negative: the interleaved prefix above followed by
the CX frame (must include c=1); missing B value, narrower interface
domain, stale allocation occurrence, nonmaximal frame, phase-on-B and a
sampled label request. Include two loop visits with different entry facts
(both realisations must cover the normative union, not just their own slices),
the two-product c/d union above, two reused borrowed lifetimes, and an
inherited control in full range.
Verify the tensor relation on basis columns, which establishes it with
an external reference by linearity; basis probabilities alone do not.

The c/b truth tables and B-dependent phase counterexample are checked
exactly by [check_rev2.py](check_rev2.py). The originating note cites sched's
`.tmp/cross-repo-beads.md`, “exhaustive borrow-frame binding”. No new
checker, Rust borrow proof or sibling gate was executed for this proposal.

## Release and route

Recommend a **0.9 K claim-binding repair**, preserving K76/K78 semantics.
Keep 7s0 and the originating sched-awo implementation obligation open
until schema, domain resolver and positive/negative checker vectors land.

## Publication and validation boundary

This is a revision proposal, not council acceptance or a consumer implementation.
The default publication rule in spec/README.md requires a full version bump
for semantic changes. The recommended 0.9 K route requires explicit council
and maintainer authorization of its in-version compatibility rules; this note
does not grant it. All unchanged-hash claims assume unchanged header/source
and catalog envelopes. A full version publication recomputes affected symbol,
object, target, schedule, certificate and versioned ref-library identities and
consumer pins even when recipe bodies stay fixed. Published 0.9 bytes remain
available; older closed-schema readers require an upgrade for new fields.

The reproducible finite and document checks are in [check_rev2.py](check_rev2.py):
`timeout 120 python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/notes/2026-11-02-rev2/check_rev2.py`.
Executed for this revision: exit 0, all eight PASS result lines.
These finite checks verify witnesses and revision structure; they implement
no proposed-format checker or host shim. No full repository gate or sibling gate is claimed: scripts/pre-push
uses git/worktree writes, forbidden by this runner, and its setup changes paths
outside this job. Underlying beads remain open for publication and consumers.

---

## Dossier part: v2v (run pass2-v2v-2026-11-02; accepted by sol, codex in round 2; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-02-rev2/b-isa-spec-v2v.md)

# v2v — frame descriptors for every realised invocation context

Council proposal for `b-isa-spec-v2v` (P1).

## Round-1 blocking items and resolution

Read the [round-1 report](../../../../bennett/docs/council/pass2-v2v-2026-11-02/round-1/report.md)
and both `out-sol.json` and `out-codex.json` in that directory. The table
maps every blocking item to this revision; it claims a proposed resolution,
not a new council verdict.

| Item | Change and witness |
|---|---|
| sol V2V-1; codex V2V-1 — frames lack a device-root boundary | Append the §12.3 rule below. Witness: device pair's root key is []; flip contexts belong to pair's tree; native main needs no descriptor. Separate root B has its own []. |

## Defect and North Star scope

ISA 0.9 §12.1 “Invocation contexts” includes every reached invocation,
including defaults, with resolved arguments, budget and choices. §12.3
stores one region record per closure hash and requires one B5 frame.
§9.4 requires each slot's concrete target class and substitutes parameters
and budget into width constants before forming c-only expressions.
The same callee can receive A in one call and B in another; no single
descriptor can express both. A `(variant,controls)` key alone also fails
when those values agree. This is a C4/C5 contract defect.

North Star §§4.2/4.4/5.1 requires freely nested regions and independently
checkable schedules/certificates. Refusing repeated mixed-class calls
would narrow this machine. [4ta](b-isa-spec-4ta.md) describes a different
case: a single slot fragmented within one context. Both repairs compose.

## Alternatives and worked witness

Use the source from `../bennett-sched/tests/pipeline.rs`, test
`context_varying_frame_classes_are_explicitly_deferred_instead_of_misreported`:
root `pair(t,u)` calls the same one-bit `flip` on t and then u; flip is X.
Place t in A and u in B, capacity 1 each. Each call is forward with zero
inherited controls and the same closure hash. Callee frame one has
`mut:0,class:A,width:1`; callee frame two has B instead.

For all four root basis inputs, the result is `(t XOR 1,u XOR 1)`.
At unit duration/rate the root time is 2 and each root interface bit is
live for both slots: occupancy[A]=occupancy[B]=2, peaks 1 each.
The per-invocation callee views have duration 1 and just their respective
class. Neither copying A into both records nor taking a class wildcard
describes the realised placement. This witness needs no heterogeneous
slot and no nonzero epsilon.

| Alternative | Assessment |
|---|---|
| Duplicate region records or rename the callee | Breaks closure-keyed identity or unnecessarily changes the source. |
| Use one wildcard/maximal frame | Cannot verify concrete classes and actual widths. |
| Exact context-indexed frames, uniform shorthand retained | Describes both calls and keeps old uniform certificates. Recommended. |

## Recommended exact spec diff

Replace the §12.3 region `frame (required)` entry by:

```text
frame?: <§9.4 descriptor>,
frame_contexts?: [{context_key:<§12.1 key>, frame:<§9.4 descriptor>}]
```

Append:

```text
Each scheduled region record contains exactly one of frame and
frame_contexts. frame is a descriptor valid for every reached invocation
of that region in the bound root realisation, after instantiating c for
each invocation. It may be used only if all its concrete classes and
resolved non-c-dependent widths describe every invocation truthfully.
frame_contexts contains exactly one record for each reached invocation,
in increasing bytewise order of the JCS encoding of context_key. The
key is exactly §12.1's fully resolved invocation chain; no wildcard,
variant/control-only key, omitted default-covered call or repeated key
is admitted. Every supplied frame_contexts array is validated, including a single-context
array. Coverage includes predicated-off and default-covered realised calls;
frame selection never inspects the quantum predicate value. The root invocation has key []. Resolve its variant,
controls, arguments, budget, placements and expansion choices from the
bound invocation tree, never from record order or a guessed root budget.

Select the context's descriptor before substituting c and check its
slots, classes, widths, allocation identities and lifetimes against
that invocation. Inherited controls remain caller-owned and separate
from callee slots. Distinct contexts have distinct dynamic frame
identities even when their static descriptor id strings agree. Identical
descriptor bytes do not authorize shared physical storage; §9.4's
live-range and disjointness rules remain required. A uniform descriptor must also have valid allocation order, scheme identities
and live ranges in every covered invocation. A standalone reference
record uses frame for its explicitly bound invocation or a descriptor
proved uniform over its declared invocation scope.
```

Here `context_key` uses the same spelling as the first-pass resource and
fault proposals. Their arrays and `frame_contexts` must cover the same
reached context set when applicable, rather than enumerate independently.
The originating bead's field spelling `context` is superseded by this
consistent proposed spelling; neither is published yet.

## Fat-object applicability

Incorporate [the shared scoping statement](fat-object-scope.md#citable-scoping-statement).
Append the following proposed normative paragraph to §12.3:

```text
In a mixed fat object, frame and frame_contexts describe the linked
ISA regions in the certificate's bound device-root realisation. Each
device root has its own object/root bindings and complete context set;
[] denotes that device root, never the native executable entry. Native
host functions, process argv/envp and host-only libc need no frame
records. Shared linked closures retain separate root-relative contexts.
A host may reach the device through §10's device CC entry; the general
mixed-container launch shim remains the explicit boundary work described
in the shared scope statement. Native comparison binds the corresponding
materialised device region and callee closure under its recorded configuration.
```

The shared statement lists today's assumptions and the exact remaining
container, launch, budget, handle, tape and host-memory contract changes.
This note does not assume that the device object is the entire binary.

## Hashes, catalog and consumers

No callee clone, source/interface/closure hash or catalog change is
required. Certificate bytes change. Existing schedules already distinguish
the two source call points; no new call edge is invented. Schedulers,
specialisers and checkers must retain full context keys across linked and
default-covered calls. Estimator frames and resource reports must select
the same context. A uniformly valid c-expression stays usable as `frame`;
the repair must not force needless duplication of uniform certificates.

## Concrete context witness

With H_pair denoting the pair closure hash, the two context keys are
`[{symbol:H_pair,point:"entry:0",iteration:[],instance:[],call_index:0}]`
and the same key with point `entry:1`. Their complete frame descriptors
are `{slots:[{id:"mut:0",role:"mut",class:"A",width:1}],scratch:[],history:[],borrow:[],ancillae:[]}`
and the identical descriptor with class B. Replace H_pair by the bound hash
and sort by unsigned UTF-8 bytes of each key's JCS encoding. These five
arrays are all required B5 arrays. An empty schedule entries array does
not omit either default-covered call or its frame. A separate device
root's [] is independent of pair's [].

## Conformance vectors and verification

Use the pair/flip case; check both class records and all four outputs,
then inverse restoration. Reject two A records, a missing default call,
duplicate/foreign key, both `frame` and `frame_contexts`, neither field,
and a width from another token budget at the same variant/control count.
Add a homogeneous two-call control accepted with old `frame`, and combine
one context with 4ta fragments. Finite output/resource arithmetic is
checked by [check_rev2.py](check_rev2.py). The originating note reports the sibling test's `Unsupported` expectation
as gap evidence. This revision executes no sibling test and claims no
completed consumer fix.

## Release and route

Recommend a **0.9 K certificate-context repair**, coordinated with
[cwq](../2026-11-02-pass2/b-isa-spec-cwq.md) and [jw7](../2026-11-02-pass2/b-isa-spec-jw7.md). Keep v2v open until
the encoding and consumer tests are accepted. A 0.10 deferral must retain
this explicit blocker; it cannot restrict the admissible call graph.

## Publication and validation boundary

This is a revision proposal, not council acceptance or a consumer implementation.
The default publication rule in spec/README.md requires a full version bump
for semantic changes. The recommended 0.9 K route requires explicit council
and maintainer authorization of its in-version compatibility rules; this note
does not grant it. All unchanged-hash claims assume unchanged header/source
and catalog envelopes. A full version publication recomputes affected symbol,
object, target, schedule, certificate and versioned ref-library identities and
consumer pins even when recipe bodies stay fixed. Published 0.9 bytes remain
available; older closed-schema readers require an upgrade for new fields.

The reproducible finite and document checks are in [check_rev2.py](check_rev2.py):
`timeout 120 python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/notes/2026-11-02-rev2/check_rev2.py`.
Executed for this revision: exit 0, all eight PASS result lines.
These finite checks verify witnesses and revision structure; they implement
no proposed-format checker or host shim. No full repository gate or sibling gate is claimed: scripts/pre-push
uses git/worktree writes, forbidden by this runner, and its setup changes paths
outside this job. Underlying beads remain open for publication and consumers.

---

## Dossier part: ysw (run pass2-ysw-2026-11-02; accepted by sol, codex in round 2; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-02-rev2/b-isa-spec-ysw.md)

# ysw — tuple values do not encode token identity

Council proposal for `b-isa-spec-ysw`.

## Round-1 blocking items and resolution

Read the [round-1 report](../../../../bennett/docs/council/pass2-ysw-2026-11-02/round-1/report.md)
and both `out-sol.json` and `out-codex.json` in that directory. The table
maps every blocking item to this revision; it claims a proposed resolution,
not a new council verdict.

| Item | Change and witness |
|---|---|
| codex B1 — action_call has no separate invocation token (§4.7) | Replace the blanket region ordering and both ABI defaults: oracle prepends tk; action/perm_action/CC/R lists token parameters only. Witness: token-free flip has []; token-free oracle has [0]; an action(a,b) has [0,0] or [0,1]. |
| sol B1; codex B2 — missing mixed-object launch/certificate scope | Add the §§10/12.3 paragraph below. The device launch derives aliases from that program's valid token handles; native main/argv/libc have no device-alias inventory. |

## Defect and North Star scope

ISA 0.9 §5.3 matched pairs require equal token **identities and tuples**;
§5.4 mints fresh identities even at equal tuples. §4.1/§7.4 `uncall`
compares recorded boundary values. But K13 (§12.3), K12 (§10.1) and
§11 schedule bindings serialize token arguments only as tuples. They
cannot distinguish alias relations that affect execution and K81 cleanup
pair formation. This is a C3/C5 context-identity gap, separate from the
correct canonical tuple encoding and from token-to-oracle diagnostics.

North Star §§4.2/4.4/5.1 requires deterministic reversible execution,
parameterised scheduling and substitutable estimates. Requiring all equal
tuples to be one token, or banning repeated/equal token arguments, removes
currently admitted capabilities. Preserve identity semantics and encode
equality without serializing process-local handles.

## Alternatives and worked witness

Origin: `../bennett-estimate/tests/fixtures/token-alias-source-gap.bisa`
and `.tmp/sol-estimate/cross-repo-beads.md`, EST-CONTEXT-03. Its CC root
is `call @sink a; uncall @sink (b) (); ret`, with an R sink containing
only `ret`. Passing the same valid token at a and b takes four source
steps (call, sink ret, uncall, root ret). Two fresh identities with the
same tuple fault 4 at the third step. In both cases args is
`[["1","0","0","0"],["1","0","0","0"]]`, hence params_hash agrees.
These counts follow §7.4 by hand; they are not a reproduced VM run.

For an oracle estimate with its separately supplied primary token T0, the
three identities (T0,a,b) can have aliases `[0,1,1]` or `[0,1,2]` while
all tuples agree. Forwarding a preserves its class; a successful new
`budget.mint` must create a class distinct from both. In a CC entry with
no separately supplied primary token, the corresponding a/b arrays are
`[0,0]` and `[0,1]`. The bead's unconditional “position zero is primary”
must distinguish oracle invocations from actions and CC/R entries.

| Alternative | Assessment |
|---|---|
| Change token equality everywhere to tuple equality | Changes matched-pair/uncall semantics and fresh-mint meaning. Not a serialization repair. |
| Serialize process ids | Nonportable, invalid across loads and competing implementations. |
| Canonical equality partition alongside tuples | Preserves existing semantics and every alias pattern. Recommended. |
| Compute a worst-case estimate over all partitions | Useful explicitly conditional bound, not an exact estimate of a selected identity context. |

## Recommended exact spec diff

Add to §12.3 invocation bindings and §11 schedule bindings
`token_aliases:[nonnegative integer,...]`, with this rule:

```text
A resolved invocation carries a canonical token equality partition.
For an oracle invocation list its separate invocation token first, then
token-typed args in signature order. For an action, perm_action or CC/R
entry list only token-typed parameters in signature order: §4.7 action_call
has no separate invocation token. Budget fields do not create identities.
The separate token accepted by the estimation ABI supplies the budget,
but contributes an identity slot only for an oracle subject.
Equal labels denote one valid token identity and require equal tuples;
unequal labels denote distinct identities even when tuples agree.
Labels are assigned by first occurrence, starting at 0, without gaps.
An empty token list has []. A token-free oracle has [0]; a token-free
action/perm_action/CC/R entry has []. An action with a,b uses [0,0] for
one shared token identity and [0,1] for two distinct identities.
No process-local handle is serialized. params_hash remains SHA-256 of
the typed args array alone. Full invocation/schedule/cache matching
additionally compares token_aliases; params_hash alone is insufficient.

Executors derive this partition from actual live handles. Tuple-only
requests with token arguments must explicitly supply the partition;
malformed labels, wrong arity or tuple-inconsistent equality are E_ARG
before producing an estimate or performing an effect. Every consistent
partition is admitted. Source forwarding, lexical captures, lproc fixed
bindings and adjoint/inverse traversal preserve resolved identities.
A successful mint creates a fresh identity attached to that dynamic
defining occurrence; it is not reconstructed by tuple interning.
Nested contexts retain the identity mapping and canonicalize their own
ordered partition from it; equal local label numbers in two contexts
do not by themselves denote one global token.

This source-binding identity context is explicit metadata outside the
closed catalog JSON and its positional value arguments. K24's token
values and K77's exactly-one-field oracle_invocation token channel keep
their tuple encoding. Builders and captures additionally preserve the
identity context so source matching is not performed on tuple equality.

Claims used in an identity-dependent context bind its partition too.
Parameter-uniform structural proofs quantify over every consistent
partition as well as every argument vector/budget. Inverse-pair entries
bind the primary/argument token partition when relevant; coverage must
preserve it and all its tuple-equality constraints alongside the existing
primary-budget inequality and exact arg_tokens tests. A proof for one
partition cannot be reused for another merely because params_hash agrees.
```

Add an ABI entry rather than changing the existing function in place:

```c
bennett_status bennett_estimate_run_with_token_aliases(
    bennett_program_t*, const char* region, bennett_token,
    const char* variant, uint32_t inherited_controls,
    const uint8_t* params_jcs, size_t params_len,
    const uint8_t* aliases_jcs, size_t aliases_len, bennett_estimate_t** out);
bennett_status bennett_sched_request_set_token_aliases(
    bennett_sched_request_t*, const uint8_t* aliases_jcs, size_t aliases_len);
```

Both copy and validate the JCS array. Keep the old ABI callable; with no
token args infer [0] for an oracle and [] for an action/perm_action.
A legacy request with token arguments and no alias binding returns E_ARG;
the additive alias-aware function admits every consistent partition and
provides exact estimates of each resolved request. A bound over partitions
is not a K12 exact result. This request diagnostic does not make any valid
program or alias pattern illegal, and does not replace implementing the
full alias-aware capability. Publish
the extension under an explicit launch/sched ABI revision or feature
contract, including loader capability negotiation; do not change the
published C argument layout/symbol meaning silently.

## Fat-object applicability

Incorporate [the shared scoping statement](fat-object-scope.md#citable-scoping-statement).
Append the following proposed normative paragraph to §§10 and 12.3:

```text
In a mixed fat object, token_aliases binds invocations of the loaded
marked device ISA object and linked device closure. Execution derives
partitions from that program's valid live token handles and preserves
equality through device calls; tuple-based estimate/schedule requests
supply equality partitions explicitly. Serialization contains equality
classes, never host pointers or process-local handle ids. Alias-bearing
schedules and certificates bind that device object/root and invocation.
Native entry points, argv/envp and host-only libc need no device-alias
entries. The future mixed launch shim negotiates the alias-binding ABI
feature; §10 alone does not specify that shim or container interface.
```

The shared statement lists today's assumptions and the exact remaining
container, launch, budget, handle, tape and host-memory contract changes.
This note does not assume that the device object is the entire binary.

## Action and inverse-pair witnesses

The published token-free flip action's action_call has no token operand:
execution, estimates and replay all derive []. An action with token
parameters a,b has [0,0] for a=b or [0,1] for distinct equal-tuple tokens.
A CC sink wrapper has the same ordering. Only an oracle with primary T0
and token arguments a,b can use [0,1,1] versus [0,1,2].

For a Q witness use a memoryless identity oracle (`lift.retval x`) and an
action containing two consecutive oracle_call occurrences on the same
wires, with token arguments a then b. Both calls compose to identity.
The action's partition [0,0] permits the K81 matched pair and its K65
carrier at the second call; [0,1] supplies no such carrier. Each oracle
call's own context prepends its actual a or b token. No hypothetical
primary action token is introduced. A mint reversed and minted again at
the same tuple creates a new identity; it does not revive the revoked one.

An inverse-pair entry at primary budget (2,0,0,0), arg_tokens=(2,0,0,0)
and partition [0,0] does not cover primary (3,0,0,0) with that unchanged
argument tuple: [0,0] becomes tuple-inconsistent; [0,1] changes the
certified equality partition. The original componentwise budget condition
alone is insufficient when equal-token constraints also apply.

## Hashes, catalog and consumers

Canonical args and params_hash stay fixed, as do source envelopes and
catalog bytes. Alias-bearing schedule/certificate bytes change hashes;
cache keys must include the partition. A source-builder metadata repair
does not add a token formal to ref recipes or change their hash. Runtime,
estimator, scheduler, checker and circuits must independently preserve
identity through forwarding and fresh mints. ABI revision must allow old
callers/libraries to negotiate support explicitly.

## Conformance vectors and verification

Test same tuple/same handle versus same tuple/different handles, both CC
uncall and Q K81 pairing; compare identical params_hash with unequal
alias bindings. Reject `[1,1]`, `[0,2]`, negative labels, wrong arity
and equal labels at unequal tuples. Include primary/arg alias, three
tokens, forwarding through lprocs/body captures, fresh repeated mints,
reversal/revocation and reuse of a certificate from the wrong partition.
No valid consistent partition is a source error. The partition and hash
arithmetic is checked by [check_rev2.py](check_rev2.py). The originating VM object
hash is a reported pin, not a new execution result in this job.

## Release and route

Recommend a **0.9 K identity-binding repair with additive, explicitly
versioned ABI support**. If binary-interface publication waits for 0.10,
retain ysw as an exact-estimation/context blocker; conditional bounds do
not complete this capability. Coordinate fault/frame/resource bindings.

## Publication and validation boundary

This is a revision proposal, not council acceptance or a consumer implementation.
The default publication rule in spec/README.md requires a full version bump
for semantic changes. The recommended 0.9 K route requires explicit council
and maintainer authorization of its in-version compatibility rules; this note
does not grant it. All unchanged-hash claims assume unchanged header/source
and catalog envelopes. A full version publication recomputes affected symbol,
object, target, schedule, certificate and versioned ref-library identities and
consumer pins even when recipe bodies stay fixed. Published 0.9 bytes remain
available; older closed-schema readers require an upgrade for new fields.

The reproducible finite and document checks are in [check_rev2.py](check_rev2.py):
`timeout 120 python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/notes/2026-11-02-rev2/check_rev2.py`.
Executed for this revision: exit 0, all eight PASS result lines.
These finite checks verify witnesses and revision structure; they implement
no proposed-format checker or host shim. No full repository gate or sibling gate is claimed: scripts/pre-push
uses git/worktree writes, forbidden by this runner, and its setup changes paths
outside this job. Underlying beads remain open for publication and consumers.

---

## Dossier part: 2cg (run pass2-2cg-2026-11-02; accepted by sol, codex in round 2; amends the Bennett dialect spec (../bennett-dialect-spec/spec/); source note bennett-isa-spec/docs/notes/2026-11-02-rev2/b-dialect-spec-2cg.md)

# 2cg — distinguish exact primitive history from a minimal C-wrapper fixture

Council proposal/disposition for `b-dialect-spec-2cg` (dialect repository).

## Round-1 blocking items and resolution

Read the [round-1 report](../../../../bennett/docs/council/pass2-2cg-2026-11-02/round-1/report.md)
and both `out-sol.json` and `out-codex.json` in that directory. The table
maps every blocking item to this revision; it claims a proposed resolution,
not a new council verdict.

| Item | Change and witness |
|---|---|
| sol B1; codex B1 — allocator allowance lacks mixed-object applicability | Add only the fat-object paragraph below to §17.1 of both dialect 0.2 and 0.3 texts. Witness: native main keeps host-only work/libc native; the marked allocator-using device closure and its native comparison execute the stated bookkeeping, transferring shared metadata under §8.5 and addresses under §§19.4–19.5. |

## Defect and North Star scope

Both maintained dialect texts, §17.1 “C allocation alignment”, require
ISA §7.1's exact primitive bump, requested-size record and nonreclaiming
history. C payload extents are ABI-rounded; alignment padding is explicit
and minimal. Neither clause publishes a runtime query for old requested
sizes/liveness. The bead asks whether the exact three-record
`scripts/0212_allocation.c` witness also limits every production allocator.

The actual fixture calls itself an **independent primitive/wrapper trace
fixture, not a production allocator**. Runtime ordinary-bitcode bodies
are materialised on both sides (dialect §§17.7/19.1). On that reading,
ordinary charged bookkeeping is already expressible. This is a genuine
wording/conformance-boundary ambiguity worth resolving, **not evidence
that a new ISA allocation-query instruction is necessary**, and not a
remaining unimplemented realloc in the originating runtime. Its later
source/request supersedes the earlier blocked-query interpretation.

North Star §§3.2/5/6.1 and §8 rungs 4–5 requires real libc, unmodified
SQLite and allocator-based Julia collections. A fixed record cap,
native-only allocation query, copying past the old payload or dropping
realloc would narrow scope. Ordinary dynamic metadata preserves it;
actual added budget/history costs must remain visible and reversible.

## Alternatives and worked witness

The originating note inspected runtimes `.tmp/sol-runtimes-queue/cross-repo-beads.md`,
“resolve realloc size/liveness bookkeeping”, its implementation update,
and “wider allocator re-pin”; `src/allocator/bump.c` read-only. That reported body keeps requested sizes/live records in explicit 32-byte
heap records, reuses freed metadata slots as data, and uses an explicit
zero-size primitive probe before alignment. It does not reclaim payload
addresses or access the ISA's private allocation table.

With heap base 4096, alignment 16 and an initial raw `alloc(3)`:

| Program/body | Subsequent primitive requests | Payload base | Final bump | Records including raw alloc |
|---|---|---:|---:|---:|
| Minimal fixture `cmalloc(1)` | 13 padding, 16 payload | 4112 | 4128 | 3 |
| Inspected production `malloc(1)`, empty metadata pool | 0 probe, 12 padding, 16 payload, 32 metadata | 4112 | 4160 | 5 |

The zero-size primitive advances one byte but records requested size 0
(ISA §7.1). The production body therefore needs 64 heap bytes in this
fresh case, rather than 32. With a 32-byte heap its metadata allocation
faults after the successful probe/padding/payload prefix; ordinary
function calls do not imply transaction-wide rollback. Reversal restores
the prefix's records and stores by the ordinary reversible history.

The old-size information witness is also valid: allocations 16 then 32,
or 32 then 16, have the same first pointer p and final bump p+48. A
cursor alone cannot tell whether `realloc(p,48)` preserves 16 or 32
bytes. This proves a need to retain sizes, not a need for a privileged
query: a side list written at each allocation supplies the information.

| Alternative | Assessment |
|---|---|
| Treat the minimal fixture as the only allowed production trace | Requires another published metadata mechanism to retain full libc scope. |
| Publish a new allocation-size/liveness primitive | Possible larger contract change; unnecessary for the inspected implementation. |
| Permit ordinary explicit charged bookkeeping | Keeps exact primitive semantics and native/device equality. Recommended. |

## Recommended exact spec diff

In **both** maintained maps append to §17.1 after the allocation vector:

```text
The allocation vector fixes the trace of its stated thin wrapper,
not a universal trace for every implementation of malloc/calloc/realloc.
Runtime bodies may retain requested size, liveness and alignment state
in ordinary materialised memory, including dynamically allocated metadata
and explicit zero-size address probes. Every such operation, its stores,
padding and allocation history is present identically in device and
native materialisation and charged to the actual heap/step/table budgets.
The C payload request retains the rounded extent and returned-base rule
above; padding immediately before that payload is minimal from the
actual current primitive bump. No hidden header, private ISA-table query,
native-only map or fixed metadata cap is implied or permitted by this
allowance. Reusing live metadata storage as ordinary data does not reclaim
primitive payload addresses or allocation-table/history entries.

realloc preserves min(old requested size,new size) bytes of a live C
allocation, using retained ordinary metadata or another published
mechanism. Invalid/dead/interior pointers retain the materialised
memory/fault contract. Overflow preflights precede the corresponding
allocation mutation; a later primitive failure retains the successfully
executed ordinary prefix unless explicitly reversed. Both comparison
builds execute the same body, including its failure prefix. Tests of a
production runtime bind that body's identity and exact resulting trace;
they do not impose the thin fixture's record count on a different body.
```

Keep the three-record fixture and its output exactly as published. Add a
separate tagged production-body vector to the dialect/runtime acceptance
corpus, not a replacement that weakens primitive history checks. This
proposal grants no blanket memory-check exemption to runtime functions.

## Fat-object applicability

Incorporate [the shared scoping statement](fat-object-scope.md#citable-scoping-statement).
Append the following proposed normative paragraph to §17.1 in BOTH spec/Bennett-Dialect-Spec.md (0.2) and spec/Bennett-Dialect-Spec-0.3-draft.md (0.3):

```text
In a mixed fat object, this bookkeeping allowance governs the allocator
closure selected for a marked device entry and that closure's native
comparison build. The surrounding native host binary, native entry,
argv/envp and host-only libc remain outside that device object, subject
to the existing placement/promotion rules of §§4.2–4.4 and 19.4. Allocation
traces, budgets and runtime-body identities bind that selected closure.
Shared caller allocation state, including ordinary allocator metadata
bytes and primitive allocation history, is transferred and charged under
§8.5; boundary addresses and layout follow §§19.4–19.5. Neither a
whole-program device entry nor a new allocation query is required by
this clarification.
```

The shared statement lists today's assumptions and the exact remaining
container, launch, budget, handle, tape and host-memory contract changes.
This note does not assume that the device object is the entire binary.

## Hashes, catalog and consumers

ISA primitive semantics and ref catalog bytes stay fixed. Different
materialised runtime bodies change bitcode/native manifests, dialect
materialisation identity, generated ISA closures, resource costs and
consumer pins; exact addresses may change too. A dialect wording revision
must obey its full-version/mapping policy. Driver/plugin/conformance must
re-pin and budget the actual body, not transplant minimal fixture costs.
No sibling publication or tracker database is written here.

## Conformance vectors and verification

Check both traces above, min(16,48)=16 versus min(32,48)=32, shrink,
null/zero-size, dead/interior pointer, direct intervening primitive alloc,
pool-slot reuse, first stronger alignment and failures at each primitive.
Reverse all actual metadata/list stores and primitive records and replay
identically; never test only the returned payload. Exact hand arithmetic
is checked by [check_rev2.py](check_rev2.py). The runtime's reported LLVM18/23 gates
were read as originating evidence, not rerun here; this job runs no
full sibling gate and claims no SQLite/Julia rung acceptance.

## Release and route

Recommend a **current dialect §17.1 clarification**, in the 0.2 and 0.3
maps under their publication rules; no ISA 0.9 K or ISA 0.10 dependency.
Retain related jjr/0na and re-pin work with their owners as appropriate.
The orchestrator can attach this note to 2cg; no new cross-repo bead is
needed because the decision is already tracked there.

## Publication and validation boundary

This is a revision proposal, not council acceptance or a consumer implementation.
Apply the additional applicability paragraph to §17.1 in both dialect maps;
the earlier allocator clarification and vectors above are retained unchanged.
The dialect's spec/README.md and §23 require a full version bump for semantic
changes and council review. This note grants no in-version publication
exception. Mapping/body/layout changes require the corresponding identity
and consumer-pin updates. There is no new ISA primitive or catalog dependency;
existing version-specific fault/reversal dependencies remain with their
owners. This revision edits neither dialect text nor its examples.

The reproducible finite and document checks are in [check_rev2.py](check_rev2.py):
`timeout 120 python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/notes/2026-11-02-rev2/check_rev2.py`.
Executed for this revision: exit 0, all eight PASS result lines.
These finite checks verify witnesses and revision structure; they implement
no proposed-format checker or host shim. No full repository gate or sibling gate is claimed: scripts/pre-push
uses git/worktree writes, forbidden by this runner, and its setup changes paths
outside this job. Underlying beads remain open for publication and consumers.

---

## Dossier part: l2p (run contract-l2p-2026-11-02; accepted by sol, codex in round 2; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-02-rev3/l2p-amendment.md)

# l2p amendment: private measurement cleanup with checked relocation

Council-ready proposal for `b-isa-spec-bwm` (P1); publication and implementation
remain open. This note changes neither the published specification nor the
reference interpreter. The baseline is [ISA 0.9](../../../spec/Bennett-ISA-Spec-0.9.md),
through K84. Each BEFORE block below is an exact, unique span of that baseline;
each AFTER block is its complete replacement. Text outside those spans stays
as published, except the explicit version migration in §A. The checked patch
anchors make this a surgical amendment, rather than a replacement specification.

## A. Decision, release and scope

Accept the core as proposed **K85, PRIVATE-MEASUREMENT-CLEANUP**, or the next
unallocated K number at acceptance:

| Entry | Clauses | Semantic change | Tracking | Publication |
|---|---|---|---|---|
| K85 (proposed) | §§6.2, 6.4, 8.3, 11–12, 14–15, 17 | Admit uncontrolled `measure_fixup`, including delayed cleanup after its source window closes; verify the whole realised channel against legal source; bind private events, timing, resource charges and device certificate scope | b-isa-spec-bwm; council B1/B2 and L2P-1/L2P-2 | 0.10 |
| Separate optional entry | §§6.1, 11/K81, 12.1 | Exact clean-isometry boundary may establish `perm` provenance; no change to the emitted-gate permutation theorem | Efficiency only; soundness review | May accompany 0.10; not a prerequisite for K85 |

**Release choice: 0.10.** [spec/README](../../../spec/README.md) requires a full
version bump for semantic changes. Publish the core with ISA/object/sched/cert/
target `0.10`, launch/coverage `0.9` (their ABIs are unchanged), and `ref@0.10`.
The schema substitutions below are expressed against sched/cert/target 0.9 so
every old refusal and reserved `mbu` flag is accounted for. Their new fields
belong to the 0.10 schemas, never silently to an old 0.9 consumer. The new
object header carries this seven-component version vector; unchanged signature
ABI strings remain `0.9`. Section headings referring to these five changed
formats become 0.10; inherited historical examples remain explicitly 0.9.
This is the mechanical version migration, in addition to the exact semantic
replacements below. The publisher must generate actual new envelope hashes;
this note does not invent them.

A backported 0.9 semantic K repair would require an explicit council exception
to that version rule and a separately negotiated schema/expansion profile. It
is not the default proposed here. Keeping 0.9 published is compatibility, not
resolution: **b-isa-spec-bwm remains a current North Star blocker until the
repair is accepted, published and implemented by the required consumers**.
A future-version label alone does not discharge the promise or permit a
claim of complete North Star support with only 0.9.

The required capability is the uncontrolled measurement choice promised by
[North Star](../../../../bennett/docs/Bennett-NorthStar.md) §§4.2, 5 and 5.1.
The previous note overstated §9.6 (section 9, item 6): it identifies controlled
measurement cleanup as an open question. Under coherent control, unitary
cleanup remains the sanctioned fallback. This amendment preserves that
fallback and does not make controlled measurement mandatory. The optional
`perm` provenance rule below is an efficiency extension, judged on soundness;
North Star §5.1 still classifies the actually emitted H/T/measurement circuit
outside its permutation tier.

The mixed fat object remains reachable: an ordinary native host binary can
embed ISA objects for only marked modules and their linked device closures.
Sections D and E bind cleanup claims to those device closures. The standing
[shared scoping statement](../2026-11-02-rev2/fat-object-scope.md) is part of
this proposal's scope; neither this version migration nor an unimplemented
launch boundary requires whole-binary lowering.

## B. Core amendment: source validity and cleanup

### B1. §6.2: preserve legal source pairing; authorise checked relocation

Keep the first window-definition paragraph. Replace the remaining paragraphs:

<!-- before:6.2 -->
```text
Each cleanup is bound to its exact computing sequence and requires the
external input versions that sequence read (the versions in S for a
perm value), and the version of g it produced, to be current; g's
pre-computation target versions are not required to be current.
[deps: ISA-3.3-P3, ISA-6.1-P1]
A cleanup runs under the same effective control set, at the same wire
versions, as its computing sequence. [deps: ISA-2-P10, ISA-3.5, ISA-5.3-P5]
Every perm value MUST be
cleaned within its window and before its region exits; otherwise the
region is **ill-formed** (closed-window measurement-based cleanup is not
admitted). `other` values are released only by the adjoint of their
computing sequence, and only while no other live value, interface wire
or outstanding diagonal phase depends on them, as defined in §6.1.
[deps: ISA-5.3, ISA-6.1, ISA-6.4]
```

<!-- after:6.2 -->
```text
Source cleanup is bound to its exact computing sequence and requires, at
its original source point, the external input versions that sequence
read (the versions in S for a perm value), and the version of g it
produced, to be current; g's pre-computation target versions need not be
current. Source computation and cleanup have the same effective control
set and control-wire versions. Every perm workspace value has a legal
source cleanup within its window and before its region exits. An other
value's source cleanup is the exact computing adjoint and is legal only
while the §6.1 outstanding-dependence condition holds. Source programs
that fail these conditions remain ill-formed.

reverse and recompute retain these version, window and control
conditions at realisation. recompute is legal only for perm values.
measure_fixup is a checked implementation of a well-formed source pair,
not a reinterpretation of an invalid late source adjoint. K81 pairing
and the source-version checks are performed at the original legal
source point before selecting this realisation.

A measure_fixup witness MAY delay the paired physical cleanup beyond
its source window, across the explicitly identified intervening source
operations. It binds the original K65 carrier, replaced source
occurrences, later realised location, actual operand versions and
extended workspace lifetimes. Only the dependency edges explicitly
listed by the witness are replaced; all other ordering, aliasing,
control, region-cell and lifetime rules remain mandatory. Operations
other than the replacement events MUST NOT access a source-released
lifetime. The checker validates the complete realised region channel
against the original well-formed source region under §6.4 and §12.1,
with every interface wire, region cell, borrowed system and external
correlation included. A closed source window at the realised cleanup
location does not prohibit that checked implementation. Workspace MUST
be reset and released before the realised region exits.
```

### B2. §6.4: complete validity condition

<!-- before:6.4 -->
```text
Every cleanup in this version is **unitary**: realisation `reverse`
(the adjoint of g's exact computing sequence, §6.2) or `recompute`
(legal for `perm` values only: recompute g into a fresh clean bundle by
the same sequence, `qxor` it into g's wires, uncompute the fresh bundle
by the adjoint). **Measurement-based cleanup is not admitted in sched/
cert 0.9**: a schedule naming any other realisation is invalid, the
target capability `mbu` is reserved and MUST be `false`, and no cleanup
produces a `channel` claim. *(non-normative)* The fixup after an X-basis
measurement of g with outcome m is the phase (−1)^{m·g(x)}, a function
of g's computing sequence and not of the target; its normative form,
its controlled variant and its certificate kind are deferred (§17 item
6; default: unitary cleanup). Schedules and certificate cleanup entries
are keyed by `(region hash, variant, inherited control count)`; a region
reachable under a non-empty control context MUST have a cleanup
schedule for that key.
```

<!-- after:6.4 -->
```text
Cleanup realisations are reverse, recompute and measure_fixup. reverse
is the computing sequence's exact adjoint. recompute retains §6.2's
perm-only rule: recompute into fresh clean workspace, XOR into the
original, uncompute the fresh computation and release its workspace.

measure_fixup implements a source pair satisfying §6.2. It measures
only designated private allocated workspace, performs outcome-indexed
fixup, resets that workspace and releases it. It is admitted when the
effective coherent control context of the replaced pair is empty.
The algorithm's own quantum data controls (for example a and b in an
AND) are included in the channel subject; they are not an inherited
control context. Under any nonempty inherited or local coherent
predicate context, reverse or recompute remains the sanctioned fallback
until the controlled measurement contract is published. This is the
controlled-form deferral, not a deferral of uncontrolled measurement.

The default private measurement primitive is computational-basis
projective measurement of one workspace wire. X-basis measurement
expands as H followed by that primitive. For outcome m, reset is X^m
on the measured wire after any required correction. Every basis change,
measurement, conditional gate, reset and release is an explicit bound
expansion event. Outcomes are private classical bits, distinct from
quantum predicates. No outcome or record of it may enter a launch
measurement list, host result, effect tape, hostcall, source control
flow or any other externally visible output. These implementation
events do not create source-level CC measure frames.

Let A initialise all private workspace in its declared clean/image
state, V be the unchanged legal source region's reference isometry,
and K_m be the complete realised branch map after measurement, fixup,
reset and release, for outcome string m. Before deleting any workspace
factor the checker MUST establish its required clean/image restoration
and borrowed-system restoration on the entire declared input space.
Let Phi(rho) = sum_m K_m rho K_m^dagger on the complete retained
interface, including borrowed systems and inherited controls when
checking a containing region. Verify sum_m K_m^dagger K_m = I and the
§12.1 channel bound ||Phi - (rho -> V rho V^dagger)||_diamond <= e
for every actual invocation context. e is the checked channel error
charged under §12.3 and must fit the bound schedule accuracy. Exact
identity has e=0 and uses the exact route in §12.1. Restoration and
privacy are exact obligations, not consequences of an approximate
interface bound. Basis values or ancilla-zero alone are insufficient.

Every outcome string is included, including a branch of exact zero
probability. Each branch correction is checked for the actual
intervening operations and realised operand versions. In the special
case of a phase D followed by an intervening unitary U on retained
systems, the transported correction is U D^m U^dagger. This formula
does not replace channel verification for more general intervening
operations or multiple cleanups. Witnesses for several interacting
cleanups are checked in their composed region, not independently under
incompatible assumptions.

The witness MAY also bind a replacement of its owned source computing
sequence on its proved clean-input subspace. That replacement MUST have
the same exact clean-boundary isometry, including amplitude +1, on
every input column and leave all other wires unchanged. It is checked
as part of the whole-pair realisation and whole-region channel proof;
it grants no source perm provenance and is not a general target gate
scheme on dirty inputs. With no such replacement, source computation
is unchanged. No source occurrence may be replaced by two witnesses.

An adjoint invocation or reversible run uses a separately checked
realisation of the logical inverse channel with fresh private outcomes;
it does not reverse a measurement record. Exact unitary-equivalent
interface channels satisfy the reversible interface. Approximate
channels compose with their declared diamond bounds. Explicit source
measure continues to consume its register and bar reversal.

Schedules and certificate cleanup entries remain keyed by (region hash,
variant, inherited control count). Every reachable nonempty control
context has a unitary cleanup schedule for its key. A containing region
may itself be under control only if every affected cleanup is selected
for that actual context; an uncontrolled witness cannot be reused there.
```

The core can use legal permutation source `CCX(a,b;g); CX(g;y);
CCX(a,b;g); release(g)`. Its paired implementation can compute by the
four-T circuit C in §F and measure its cleanup, after the exact clean-boundary
and full-channel checks. It does not need the optional source-provenance
promotion. An implementation that keeps the source CCX compute can still use
measurement cleanup; its compute cost is the cost of that chosen CCX.

## C. Core amendment: target and schedule contract

### C1. §8.3: Boolean mbu, explicit private primitive cost

Replace the capability schema span:

<!-- before:8.3-capabilities -->
```text
  "capabilities": { "measurement": {"mid_circuit": bool, "feedforward_latency": n}, "mbu": false,     /* reserved, §6.4 */
                    "max_parallel": n | "unbounded", "max_predicate_depth": n | "unbounded", "classical_step_time": n },
```

<!-- after:8.3-capabilities -->
```text
  "capabilities": { "measurement": {"mid_circuit": bool, "feedforward_latency": n}, "mbu": bool,
                    "max_parallel": n | "unbounded", "max_predicate_depth": n | "unbounded", "classical_step_time": n },
  "private_cleanup"?: { "measure_z": { "cost": { "<resource>": n, "time": n } } },
```

Insert before the existing matching paragraph, retaining its first line:

<!-- before:8.3-matching -->
```text
**Matching.** An executed gate with opcode o, operand classes, **total
```

<!-- after:8.3-matching -->
```text
capabilities.mbu is a Boolean, default false when omitted by an older
target profile. mbu=true requires measurement.mid_circuit=true and a
private_cleanup.measure_z cost record. That record is required only
for mbu=true; unknown keys reject. Every declared resource has an
explicit nonnegative finite cost there (zero is allowed); time is
required. These costs are numeric constants, with no unbound cost
variables. measure_z is an exact private implementation event, not a
§4.4 gate and not a source measure instruction. Reset is an ordinary
reserved outcome-conditioned X gate; basis changes and fixups use
ordinary matched gates/schemes, their topology and their costs.
Private outcome dispatch is charged classical_step_time once per
measured bit, after measurement and before dependent gates. It emits
no host effect. feedforward_latency is an additional minimum delay,
not a substitute for that dispatch event or for any reset/gate cost.
A target with mbu=false still supports unitary cleanup. A schedule
requesting measure_fixup on it is E_SCHEDULE_INFEASIBLE; the executor
does not silently replace the requested implementation. mbu=true does
not itself prove the correction or enable measurement under coherent
control. Existing targets with mbu=false need no new cost record.

**Matching.** An executed gate with opcode o, operand classes, **total
```

### C2. §11 generated operations: explicit exception and expansion gate

<!-- before:11-expansion -->
```text
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
```

<!-- after:11-expansion -->
```text
**Generated operations and the expansion library.** Every row and
instruction expands into generated operations (gates, allocations,
releases). Source order is fixed by §3.6, §4.2, §4.5–§4.6 and §5.2;
only the checked measure_fixup transformation of §§6.2/6.4 may replace
the specifically recorded source-order dependencies for its owned pair.
The expansion library is a versioned document bound by
bindings.expansion = {name,version,hash}. It defines every instruction
and row expansion, its ordinals, scratch identities and removable set,
and, when supported, the private cleanup-event constructors below.
Unselected source operations retain their semantics, identities and
dependencies. A consumer lacking the exact bound library or event
profile rejects with E_SCHEDULE_INFEASIBLE. Two consumers implementing
it execute and charge the same reserved event set. Other §5.7
transformations retain ordinals and remove only library-marked leaves.
```

Replace the cleanup payload in the schedule schema:

<!-- before:11-schema -->
```text
                   "cleanup": { "realisation": "reverse" | "recompute" },
```

<!-- after:11-schema -->
```text
                   "cleanup": { "realisation": "reverse" | "recompute" | "measure_fixup", "witness"?: "<id>" },
```

Add the definition map beside interface placement in the schedule schema:

<!-- before:11-witness-map -->
```text
    "interface_vertices"?: [ [v, …], … ],
```

<!-- after:11-witness-map -->
```text
    "cleanup_witnesses"?: { "<id>": { "contexts": [ <D3 context record>, … ] } },
    "interface_vertices"?: [ [v, …], … ],
```

`witness` is required exactly for `measure_fixup` and is forbidden on the
other two kinds. It names one definition in `cleanup_witnesses` and the
matching certificate record in D3. The definition map commits all event,
placement, version, lifetime and dependency bytes to `schedule_hash`. It
contains no claim, certificate hash or channel subject. The certificate
repeats the same definition and adds its channel-claim index; the checker
requires byte-identical JCS `contexts` values. Thus the schedule fixes the
event set and the certificate can bind `schedule_hash` without a hash cycle.
The map is required for any selected `measure_fixup`; otherwise it may be
absent. Missing referenced definitions and conflicting duplicates reject.
Instantiated events derive deterministically from that bound definition and
the expansion profile and are checked before execution.

Replace Timing and Obligations:

<!-- before:11-timing -->
```text
**Timing**: a `start` time
MUST be ≥ the end of every operation the operation depends on (data,
wire lifetime, region cell version, effect order); an entry violating
this makes the schedule invalid. **Obligations**: satisfy §6; respect
capacity; report every resource; be reproducible from the request plus
scheduler version.
```

<!-- after:11-timing -->
```text
**Timing**: a start time MUST be at least the end of every predecessor
in the validated dependency graph (data, lifetime, region-cell version
and effect order). measure_fixup replaces only the explicitly bound
edges authorised by its whole-region channel check. Its graph MUST be
acyclic. A predecessor is an actual emitted event, never the
non-emitting cleanup carrier. A dependency on a measurement outcome
also requires start >= measurement end + feedforward_latency and
completion of the outcome-dispatch event. Absent explicit start
entries, emitted events execute sequentially in bound-expansion order
with those minimum delays. Invalid timing is E_SCHEDULE_INFEASIBLE.

Conditional slots are reserved events. Each retains its ordinary gate
duration, wire occupancy, resource cost and error reservation on every
outcome; a false condition performs the identity in that reserved slot.
Every private measurement and dispatch is charged, and workspace live
intervals extend through reset and release at their realised positions.
Resource counts, makespan, occupancy, peak, capacity and topology use
this padded event set and the extended lifetimes. Outcome-dependent
renumbering, early release or resource discounts are invalid.

**Obligations**: satisfy §6, every required channel check, target
capabilities and capacity; report every resource; reproduce the same
reserved events and graph from the request, scheduler version,
bound schedule definition and expansion. A missing/unverified cleanup
witness makes the requested schedule infeasible before its effects.
```

### C3. K65 and K80: ownership, coordinates and relocation

Replace K65's selection paragraph:

<!-- before:11-K65 -->
```text
Resolve the unique maximal cleanup entry or the reverse default before
expanding that cleanup, and apply its reverse/recompute realisation to
the entire paired cleanup, subject to §6's validity conditions. [deps: ISA-11-P6.S1, ISA-11-P6.S7, ISA-11-P6.S8, ISA-6.2, ISA-6.4]
```

<!-- after:11-K65 -->
```text
Resolve the unique maximal cleanup entry or the reverse default before
expansion. reverse/recompute apply to the entire K81 pair's cleanup.
measure_fixup binds that same original carrier and legal source pair;
its witness may replace the owned computing sequence on the exact
clean subspace and delay the physical cleanup under §§6.2/6.4.
Source pairing, captured source versions and inverse ownership are
unchanged by selection. The later insertion point is not another
carrier and cannot acquire the inverse occurrences a second time.
```

Replace the complete K80 normative paragraph; its existing multirow reverse/
recompute witness remains valid:

<!-- before:11-K80 -->
```text
**Cleanup leaf ownership (K80).** For `reverse`, emitted leaves retain the
written cleanup's source points and per-point ordinal and semantic-call
occurrence spaces, including the terminating release. For `recompute`,
consumers MUST assign the entire replacement's caller-level leaves and
call edges to the carrier's point and coordinates. The original
computation is unchanged; replaced inverse rows emit nothing. Materialise
fresh computation, XOR, fresh uncomputation and releases in §6.4 order;
number caller leaves contiguously from zero, excluding callee subtrees,
and number semantic-call occurrences independently from zero (§11.1/K63).
Fresh uncomputation has separate occurrences from fresh computation;
neither reuses the original computation's edges or scratch identities.
Callees retain their own source points, nested chains and ordinal/call
spaces under these fresh edges. Internal replay does not import the
original rows' source-qloop coordinates. Raw inverse traversal retains
forward paths, leaf ordinals, call occurrences and scratch identities;
step/phase follows §11 and source-adjoint formation remains K62. The carrier's ordinal 0 belongs only to
cleanup-kind matching; it does not consume emitted-leaf ordinal 0.
K64's oracle support partition is unchanged.
```

<!-- after:11-K80 -->
```text
**Cleanup leaf ownership (K80).** reverse retains the written cleanup's
source points, per-point ordinals and semantic-call occurrences.
recompute assigns all replacement caller leaves and call edges to the
original carrier's coordinates, in fresh-computation, XOR,
fresh-uncomputation, release order. Replaced inverse rows emit nothing.
Number caller leaves from zero excluding callee subtrees, and semantic
calls independently from zero. Fresh replay has fresh scratch and
call occurrences; callees retain their own points beneath those edges.
It does not import original source-qloop coordinates.

For measure_fixup, the original source computing sequence is unchanged
unless compute_events is supplied. Such replacement compute events
belong to the original computing points; their caller ordinals and
calls are numbered from zero within each replaced point in event order.
All measurement, dispatch, fixup, reset and delayed-release caller
events belong to the original cleanup carrier's chain, point,
iteration, instance, step and phase; number their leaves contiguously
from zero in declared reservation order. Their actual placement is
specified separately by after and dependencies. The carrier remains
non-emitting; its cleanup ordinal 0 does not consume emitted ordinal 0.
Outcome choice never renumbers a slot, removes its reservation or
changes a context key. Callee subtrees, if any, keep their own spaces
under fresh carrier edges. No source occurrence has multiple owners.
The unchanged K81 partition still excludes private constructor cleanup;
this amendment does not silently create carriers for those expansions.

Raw inversion of a unitary expanded trace retains forward coordinates,
call occurrences and scratch identities; step/phase follows §11 and
source-adjoint formation remains K62. A measurement trace has no raw
physical inverse. Its logical inverse is separately expanded, bound
and channel-checked under §6.4, retaining source occurrence identity
but using its own reserved events and fresh outcomes. K64 support
partitioning and all unchanged operation coordinates remain intact.
```

K81's source partition itself is unchanged in the core. In particular,
`qcopy; H; quncopy` is not made legal by a schedule selection. The permitted
source is `qcopy; quncopy; H`, with the physical cleanup delayed by this rule.

### C4. §11.1: new private-event profile, never a silent ref@0.9 edit

Keep the historical catalog statement, append the new publication contract:

<!-- before:11.1-library -->
```text
**ISA-REF-LIB** (K11; b-isa-spec-8r4, from bennett-vm-47t).
This is the decided 0.9 contract. The catalog bound as ref version 0.9
is the file `spec/ref-0.9.json` whose four-line envelope hashes to
`5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197`.
It publishes the complete 219-recipe catalog, byte-identical to the
accepted catalog snapshot.
```

<!-- after:11.1-library -->
```text
**ISA-REF-LIB** (K11; b-isa-spec-8r4, from bennett-vm-47t).
The historical ref@0.9 catalog is spec/ref-0.9.json, with 219 recipes
and envelope hash
5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197.
Its bytes, constructors and meaning are unchanged. It cannot implement
the new private cleanup events. Existing 0.9 consumers retain that
binding and reject an unimplemented expansion library.

The 0.10 publication MUST publish ref@0.10, its complete recipe catalog,
the private-cleanup event profile below and its actual envelope hash.
Use the existing four-line library envelope with isa=0.10 and
version=0.10; the event-profile definitions are part of the versioned
document's semantic contract. Its canonical document MUST include
event_profile:"private-cleanup-1". No missing hash is a wildcard.
Ordinary unitary recipes retain their existing algorithms unless a
separate accepted change explicitly replaces them.

The private-cleanup-1 event union is:
gate {op,wires,when?}; measure_z {wire,outcome};
dispatch {outcome}; release {wire}.
gate.op is a §4.4 gate with its usual parameter encoding (params is
required for a parametric gate and absent otherwise); wire operands
are ordered resolved wire/version records. measure_z has no quantum
controls, emits one exact outcome bit, and uses the target's private
measurement cost. dispatch consumes that bit and costs one
classical_step_time. when, if present, is {outcome,equals:0|1}; it
selects an ordinary gate or the identity in its fully charged slot,
and cannot gate allocation, measurement, dispatch or release.
Outcome names are unique within a witness and cannot escape it.
when is classical feedforward and adds no coherent control to target
gate matching or the region's inherited control count.
Reset is the explicit gate X with when:{outcome,equals:1}.
Allocation remains the existing clean allocation constructor and
must be declared in the ordinary frame/event stream; no undeclared
wire is created by a cleanup event. Each event has its stable id,
source coordinates and resolved operands under §11. No constructor
means source-level CC measure or changes the unitary gate registry.
Unsupported event-profile versions are E_SCHEDULE_INFEASIBLE.

The exact JSON encoding is the union above with an event discriminator
(`"gate"`, `"measure_z"`, `"dispatch"`, `"release"`) and the corresponding
fields; no additional fields except the universal `id` are allowed. `params`
is the gate-only optional field just specified. Source coordinates derive
from C3 and are not producer-selected event fields. `compute_events` below
wraps each event with its replaced source point so several computing points
can be distinguished. A release event consumes a lifetime only after its
exact reset proof succeeds. A fixup requiring a controlled gate uses that
gate's ordinary quantum controls in `wires`; `when` is solely classical.
```

## D. Core amendment: channel claims, domains and certificate layout

### D1. §12.1 channel row and exact route

<!-- before:12.1-channel -->
```text
| `channel` | `{ "subject": as above, "metric": "diamond", "precision_bits", "bound", "dual": [ { "Y": interval Hermitian matrix, "mu": decimal } … ] }` | for every invocation context of the subject, in enumeration order, verify its dual witness for the **diamond-norm SDP** below in interval arithmetic and `mu` ≤ `bound` (one witness per context; too few witnesses: reject) |
```

<!-- after:12.1-channel -->
```text
| `channel` | `{ "subject": as above, "metric":"diamond", "bound":decimal, "proof"?:"dual"|"exact", "precision_bits"?:n, "dual"?:[ {"Y":interval Hermitian matrix,"mu":decimal} … ], "witness"?:{"rule":"matrix_units"} }` | every actual invocation context: build the complete realised channel and legal source channel independently; default proof `dual` uses the existing rigorous SDP rule with required precision_bits and dual and no witness; proof `exact` requires bound 0, witness rule matrix_units, no precision_bits/dual, and the exact matrix-unit and restoration checks below; a failed or incomplete check discharges nothing |
```

Insert this exact route immediately before the existing SDP paragraph:

<!-- before:12.1-exact -->
```text
**Diamond-norm SDP** (Watrous, *Theory of Computing* 5 (2009), §4; the
```

<!-- after:12.1-exact -->
```text
**Exact channel identity.** proof:exact with witness rule matrix_units
requires the checker to construct every branch K_m and reference V
from the bound source, schedule, target and expansion, never from a
producer-supplied result matrix. On every interface matrix unit E_ij
it checks sum_m K_m E_ij K_m^dagger = V E_ij V^dagger exactly. The
matrix units range over the full interface and all borrowed systems;
workspace starts in its declared clean/image state, and its exact
restoration is checked before removal, on every branch, including
zero-probability branches on their support. Check trace preservation,
complete outcome coverage, privacy and every §6.4 side condition.
Exact arithmetic or an independently checked compositional exact
derivation must establish these equalities; floating-point agreement
is not an exact proof. This route has diamond bound zero and does not
use the strictly-positive-pivot SDP test. It checks off-diagonal as
well as diagonal matrix units, hence arbitrary external entanglement.
The rule name matrix_units denotes these obligations; an algebraic
checker may factor them compositionally without materialising them.
An uncompleted check is unchecked, never proof. The numerical dual
route remains available for nonzero error and keeps all its existing
strict positivity and interval requirements; Y=0, mu=0 still fails
that route. No exact-route permission weakens its positivity test.

**Diamond-norm SDP** (Watrous, *Theory of Computing* 5 (2009), §4; the
```

Insert device scope immediately before invocation-context enumeration:

<!-- before:12.1-scope -->
```text
**Invocation contexts.** A subject denotes the set of invocations of
```

<!-- after:12.1-scope -->
```text
**Mixed fat-object subjects.** A mixed fat object may retain a native
host binary and embed ISA objects only for marked device modules and
their linked device closures. A channel subject identifies a region
closure in one selected embedded device object; its complete device
interface and device callees, with external correlations, are covered.
Native main, argv/envp handling, unmarked native libc and ordinary host
effects stay native and require no ISA/channel certificate inventory.
The launch inventory associates the selected exported device root,
device object, schedule and certificate. A native comparison claim
uses the corresponding materialised marked entry and materialised
callee closure, layout and captured launch inputs, not unrelated host
code. Private cleanup outcomes are absent from host results and launch
measurement records. Each selected device root has its own bindings
and concrete invocation-context set, including default-only calls;
[] is relative to that root, never to native process entry.

**Invocation contexts.** A subject denotes the set of invocations of
```

### D2. §12.2: quantum claims are not basis-slice claims

<!-- before:12.2-domain -->
```text
A `proof` label requires the domain to equal D; otherwise the claim is
`evidence` with the covered fraction.
```

<!-- after:12.2-domain -->
```text
For exhaustive basis claims, a proof label requires the domain to
equal D; otherwise the claim is evidence with the covered fraction.
For channel claims the domain is the full operator space of the
declared interface, inherited controls and borrowed systems, for every
§12.1 invocation context. domain slicing, omitted-component zero
defaults and sampled basis replay do not restrict that quantum proof
obligation. Workspace retains its required clean/image initial state;
it is not an arbitrary dirty input. Every private outcome is included.
Exact matrix-unit verification assigns proof only after every equality,
restoration and context obligation succeeds. Host limits on exact or
dual checks produce unchecked (host limit), identifying the context
and limiting operation; they do not make the legal channel or target
capability ill-formed and discharge no execution/proof obligation.
```

The remaining basis-domain rules, including K69–K75, retain their existing
meaning. In particular, diagonal basis tests cannot discharge a channel claim.

### D3. §12.3 cleanup record, bindings and validation

<!-- before:12.3-cleanup -->
```text
            cleanup: { "<variant>:<inherited_controls>": [ { path, realisation } ] },
```

<!-- after:12.3-cleanup -->
```text
            cleanup: { "<variant>:<inherited_controls>": [ { path, realisation, witness? } ] },
```

Insert the following definitions before `versions`:

<!-- before:12.3-layout -->
```text
`versions` is the object `{ "isa", "object", "launch", "sched", "cert",
```

<!-- after:12.3-layout -->
```text
For reverse/recompute the cleanup entry remains {path,realisation};
witness is absent. For measure_fixup, witness is required and has:
{ id, contexts: [ { context, carrier, compute_points, cleanup_points,
                   compute_events?, after, measured, outcomes, events,
                   versions, lifetimes, dependencies } ... ], claim }.
id is a nonempty string unique within the bound root certificate and
is the schedule cleanup.witness reference. contexts MUST be identical
as JCS bytes to schedule.cleanup_witnesses[id].contexts; that definition
contains no certificate/claim/subject field. claim is a zero-based
index in this owning region record's claims array, pointing to a
channel claim also listed in verification.channel. Its subject has
this region closure, variant, inherited control count and the exact
bound root schedule_hash. One record covers each concrete carrier
selected by the schedule; wildcard schedule selections must resolve
to all of their concrete contexts before verification.

contexts is ordered by the bytewise JCS encoding of {context,carrier},
without duplicate pairs or omissions. Several carriers in one region
invocation have the same context and distinct carrier coordinates.
context is the §12.1 region invocation key,
carrier the complete terminal source coordinates with generated:0,
and compute_points/cleanup_points are the exact ordered K81-owned
source occurrences, not producer-chosen semantically similar gates.
source_point is {path,step,phase}; path is the resolved §11 source
chain with no wildcards, and step/phase are the terminal containing
invocation's concrete coordinates or null when absent. compute_points,
cleanup_points and after use source_point, before leaf expansion.
carrier adds generated:0 to its source_point. A source_leaf is
{point:source_point,generated:n}, naming a concrete bound-expansion
leaf rather than a source occurrence; the two forms are not conflated.
The checker derives this ownership and compares it before expansion.

after is the concrete unchanged source occurrence after whose emitted
events the delayed cleanup begins (or the carrier's source_point for no
delay); no placement may cross the containing region return. All
intervening source operations keep their order and identity. The
checker derives their list between the original cleanup and after.
If compute_events is present it is an ordered list of {point,event}
replacing exactly compute_points, using the private-cleanup-1 gate
events and the checked clean-boundary isometry of §6.4. If absent,
computation remains unchanged. It cannot replace allocation, region
calls with effects or another witness's source occurrences.

measured is an ordered list of {wire,outcome} with distinct private
workspace wires and distinct local outcome names. wire is
{allocation,bit,version}: allocation is {leaf:source_leaf,lifetime:n},
where n is the zero-based lifetime occurrence at that allocating leaf.
bit is the zero-based bit index. version identifies the checker-derived
current value origin: {entry:true}, {source:source_point,output:n}, or
{replacement:event_id,output:n}. output numbers modified output bits
in resolved operand order. A matched inverse restores its captured
origin rather than manufacturing a new unrelated version. Internal
static/SSA numbering is not a portable substitute for these origins.
Interface/borrowed identities instead use {group,slot,bit,version},
and region cells {group,slot,cell,bit,version}; allowed groups and
slots are the existing signature and borrow positions. These three
wire-record forms are disjoint; unknown or aliased identities reject.
outcomes lists every width-|measured| bit string exactly once in
lexicographic order, including zero-probability strings. events is
the complete ordered reservation list from basis changes through
measurement, dispatch, fixup, reset and release under §11.1. Each
event id is unique within the context. Its when clauses define the
branch gate list for each listed outcome; there is no hidden branch
or implicit reset. A bit cannot be read before its measurement and
dispatch. Each measured wire has exactly one measure_z event; its
explicit reset and release follow it. No branch may consume a source
interface, dirty borrowed or live nonworkspace wire by measurement.

versions lists {event,operands:[wire records]} for every replacement
event, in event order, with checker-derived operand versions at its
actual placement. Conditional reservation slots have fixed output
origins, even on an outcome where their gate is disabled; no outcome
renumbers them. lifetimes lists {allocation,source_release,
realised_release} for every delayed private lifetime. Each release
reference is a source_point or replacement event id as appropriate;
fresh/reused physical storage cannot alias an extended lifetime.
dependencies is {remove:[[event_ref,event_ref]...],
                 add:[[event_ref,event_ref]...]}.
event_ref is {source:source_leaf} or {replacement:event id}.
remove lists exactly the original source-derived ordering/version/
release edges made inapplicable by this replacement; edges involving
unreplaced source effects or allowing foreign access to a released
lifetime cannot be removed. add binds the complete replacement data,
outcome, timing and lifetime edges. Both lists are sorted by JCS
encoding, without duplicates, and validated against the independently
derived before/after graphs. The schedule graph is acyclic and all
remaining source edges are preserved. Whole-region channel verification
is required in addition to, not instead of, these structural checks.

The certificate schedule_hash, root invocation args/budget, target_hash
and expansion binding MUST match the schedule. Root/nested argument,
token and budget resolution uses K13 and K63, including default-only
contexts; a root binding cannot substitute for a callee binding. claim
must cover the containing region's complete realised operation, not
just the isolated correction gates. A referenced witness lacking a
completed successful check is not executable. Detached certificates
must be supplied with the schedule before validation; there is no
post-execution trust path and no certificate/schedule hash cycle.

For a mixed fat object the default layout is one device certificate
per embedded ISA object and selected-root binding, with an outer
versioned inventory mapping {module_id, object_hash, entry,
closure_hash, schedule_hash, certificate_hash}. Multiple roots in one
object have separate binding records; a shared callee is checked in
each actual root context. certificate_hash is SHA-256 of the complete
certificate JCS bytes, no trailing LF. module_id is an inventory-local
identifier, not native main; entry names the selected exported device
root. Inventory entries are sorted by module_id then entry, without
duplicates, and cover every device root claimed as executable by that
inventory. The inventory associates records; it grants no new launch
ABI. Native host entry, argv/envp, unmarked libc and ordinary host
effects need no ISA region/frame/channel record. Device owner and
link-proof coverage remains complete for each selected closure.
Native comparison covers the corresponding materialised marked
closure and captured launch inputs. A whole-host quantum certificate
is not required. Private cleanup outcomes never enter the host-visible
measurement inventory. Container identity, when supplied, is separate
from object_hash and cannot replace device closure bindings.

The mixed-launch contract still must publish container/object/root
association, host-entry-to-device-entry marshalling, budgets, opaque
handle lifetime and run/tape association. Host memory by reference
requires explicit address/layout mapping, range/liveness, aliasing,
ownership/synchronisation, writeback and reversal rules. Until that
versioned boundary exists these are bennett-4ht obligations; neither
whole-binary lowering nor omission of mixed execution is a substitute.

The outer inventory is a separate mixed-container record, not an undeclared
field inserted into the existing single-object certificate. Its version is
`"mixed-device-inventory-1"`, with a required `entries` array of exactly the
records above, optionally `container_hash` (SHA-256 of container bytes, defined
outside ISA source identity); all other fields reject. Its association can be
published independently of general host memory/launch mechanics. Certificates
for multiple roots can be grouped in a container, without merging their keys.

`versions` is the object `{ "isa", "object", "launch", "sched", "cert",
```

Replace the controlled-unitary/channel claim requirement:

<!-- before:12.3-metrics -->
```text
`operator_norm` conclusions (T6, controlled unitary
variants) require `operator_norm` bounds throughout. A controlled
unitary variant requires a `numerical` claim; an ε > 0 realisation
compared as a channel requires a `channel` claim.
```

<!-- after:12.3-metrics -->
```text
operator_norm conclusions require operator_norm bounds throughout and
are claims about measurement-free unitary realisations. A controlled
measurement-free unitary variant requires a numerical claim. Every
region containing a private measurement realisation requires a channel
claim, including at epsilon=0, on its complete interface and actual
invocation contexts; exact channel identity may use §12.1's exact
route. A channel-only proof cannot be reused as an operator_norm or
global-phase proof for a controlled unitary. Nonzero-error channel
realisations retain the dual route. Each local/inclusive value is a
verified common upper bound over its key's actual contexts; multiplicity
composition and the once-only operator_norm-to-diamond factor of two
are unchanged. No failure probability is substituted for approximation
epsilon. Reservations count their charged error on every outcome.
```

## E. Core amendment: formal model and defaults

### E1. §14.2 and T4: private outcomes and logical reversal

<!-- before:14.2 -->
```text
The state of a Q region is a vector in ⊗ over live wires in allocation
order (bundles little-endian). `qalloc` tensors |0⟩; `qfree` removes
clean factors; `qborrow` introduces a factor in unknown state possibly
entangled with a reference system R, and the region's operation must be
U ⊗ I on it (§5.6); gates act by §4.4 under the active predicate;
`measure` (CC) is the projective computational-basis measurement with
Born probabilities, consuming the wires.
```

<!-- after:14.2 -->
```text
The reference state of a Q region is a vector in the tensor product
of live wires in allocation order (bundles little-endian). qalloc
tensors |0>; qfree removes clean factors; qborrow introduces an
unknown factor possibly entangled with R, on which the operation
must be identity as in §5.6; gates act by §4.4 under the active
predicate. Source measure (CC) is projective computational-basis
measurement with Born probabilities, consuming its wires.

A private measurement-assisted implementation instead denotes the
channel rho -> sum_m K_m rho K_m^dagger after explicit fixup and
workspace reset/release. Workspace begins and ends clean/image;
private outcomes belong to the implementation environment and are
discarded. Its complete retained interface, borrowed systems and
external correlations are checked under §6.4. It creates no source
measure history frame. Logical reversal uses an independently checked
implementation of the inverse reference channel with fresh private
outcomes, not inversion of physical measurement events.
```

Replace only T4's quantum exactness hypothesis; its classical history theorem
and source-measure/unverified-free eligibility conditions remain:

<!-- before:14.3-T4 -->
```text
If, in addition, every region call is undone
  by the exact inverse of its realised forward operation (ε = 0
  realisations, or a realisation that is applied as its own adjoint),
  the quantum state of every register the run touched is restored
  exactly; otherwise to within the sum of the realisations' declared
  bounds (§12.3).
```

<!-- after:14.3-T4 -->
```text
  If every region call is undone by an exact inverse of its realised
  interface operation, or a separately verified exact channel for the
  inverse of its exact unitary-equivalent interface channel (§6.4),
  the quantum state of every register touched by the run is restored
  exactly, including external correlations; otherwise restoration is
  within the sum of the declared channel bounds (§12.3). Verified
  private cleanup events do not create a measure frame and alone do
  not remove reverse eligibility. Explicit source measure and an
  unverified free retain their existing prohibitions.
```

### E2. §17 items 2, 6, 7 and 9

<!-- before:17-2 -->
```text
2. **Gate-name registry.** Default: the names of §4.4 only; an unknown
   gate name is a load error.
```

<!-- after:17-2 -->
```text
2. **Gate-name registry.** Default: the unitary gate names of §4.4 only;
   an unknown gate name is a load error. The private measurement,
   dispatch, outcome-conditioned gate and reset events of the bound
   expansion profile are realisation events, not new source opcodes
   or additions to that gate registry.
```

<!-- before:17-6 -->
```text
6. **Measurement-based cleanup** (§6.4): the normative fixup, its
   controlled variant and its certificate kind. Default: unitary cleanup
   (`reverse`); `capabilities.mbu` is `false`.
```

<!-- after:17-6 -->
```text
6. **Cleanup policy and controlled measurement.** Uncontrolled
   measure_fixup, including checked delayed cleanup, is admitted by
   §§6.2/6.4 with private outcomes, transported correction, reset,
   target mbu=true and a complete channel claim. The scheduler may
   choose it or unitary cleanup. With no selected cleanup entry the
   deterministic default remains reverse; this is not a ban on the
   measurement alternative. mbu is a target Boolean, not universally
   false. The coherent-controlled measurement form remains open;
   until its contract is published that context uses unitary cleanup.
```

Append a new-version binding after the existing item 7's exact 0.9 binding:

<!-- before:17-7 -->
```text
   For a 0.9 object this is exactly
   `{"name":"ref","version":"0.9","hash":"5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197"}`,
   equally for omission and an explicit binding. [deps: ISA-11.1-P3, ISA-11.1-P4, ISA-11.1]
```

<!-- after:17-7 -->
```text
   For a 0.9 object this is exactly
   `{"name":"ref","version":"0.9","hash":"5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197"}`,
   equally for omission and an explicit binding. [deps: ISA-11.1-P3, ISA-11.1-P4, ISA-11.1]
   A 0.10 object instead defaults to ref@0.10 at its published complete
   envelope hash. measure_fixup requires an explicitly implemented
   private-cleanup-1 expansion profile; ref@0.9 cannot be selected for
   it. Missing publication or support is never treated as a wildcard
   hash or as permission to mutate historical catalog bytes.
```

Append deterministic conditional-slot counting to item 9:

<!-- before:17-9 -->
```text
   Omitting expansion on a 0.9 object selects the full-library hash in
   item 7, not the single-qxor witness hash. [deps: ISA-11.1-P3, ISA-11.1-P4]
```

<!-- after:17-9 -->
```text
   Omitting expansion on a 0.9 object selects the full-library hash in
   item 7, not the single-qxor witness hash. [deps: ISA-11.1-P3, ISA-11.1-P4]
   For private measurement cleanup N includes every reserved ordinary
   gate slot in the selected bound expansion, with the same exact-native
   test, whether or not that slot executes a gate on a particular
   outcome. Exact private measurement and dispatch events do not add
   to N. Error shares, charged bounds and reservation identities are
   independent of sampled outcomes.
```

## F. Exact worked witnesses and costs

All witnesses below were checked using **SymPy 1.12 exact arithmetic in
Q(sqrt(2), i)** by [verify_l2p.py](verify_l2p.py), not floating-point simulation.
The executable defines every gate, computes full columns, constructs branch
maps including reset and compares all interface matrix units. Its integer
wire order is a=0, b=1, y=2, g=3, optional diagnostic q=4; displayed kets here
use the named order `(a,b,g,y)` to match the council report.

Gidney's [primary paper](https://arxiv.org/abs/1709.06648v3) reports four T
resources for temporary AND computation and zero T resources for its erasure.
The [published article](https://doi.org/10.22331/q-2018-06-18-74) distinguishes
the controlled adder's cost. This explicit implementation is derived and
verified here; it is not asserted to be a transcription of the paper's diagram.

### F1. Four-T clean-input compute and dirty-target negative

Define C in time order:

```text
h g; t g; cx a g; tdg g; cx b g; t g;
cx a g; tdg g; h g; sdg g
```

| a | b | C on g=0 | C on g=1 |
|---|---|---|---|
| 0 | 0 | +|0> | -i|1> |
| 0 | 1 | +|0> | +i|1> |
| 1 | 0 | +|0> | -i|1> |
| 1 | 1 | +|1> | -i|0> |

Thus C restricted to clean g is exactly `|a,b,0> -> |a,b,ab>` with
amplitude +1. It is not arbitrary-target CCX. The checker verifies all eight
columns, not just the four clean columns; a general native-CCX substitution
fails. `C; CX(g,y); C†` returns g=0 and implements CCX on arbitrary y,
including coherent inputs. Its literal count is eight T/Tdg gates. That is
not an optimality claim or a count after magic-state recovery; the primary
paper's unitary resource-recovery alternative uses a different accounting.

### F2. Open-window measurement: 4 T total

Let W=CCX(a,b;y), D=CZ(a,b). Before measuring g, the encoded state is
`sum_ab,y alpha_ab,y |a,b,y XOR ab>|ab>_g`. Apply H(g), measure Z(g) with
outcome m, conditionally apply CZ(a,b) when m=1, then X(g) when m=1 and
release g. Before fixup the reduced branch map is `D^m W/sqrt(2)`.
After fixup/reset it is `K_m=W/sqrt(2)` for both m. Therefore
`sum_m K_m E_ij K_m† = W E_ij W†`, including off-diagonal matrix units;
`sum_m K_m†K_m=I`. The outcome distribution is input independent (1/2 each),
and released workspace is exactly zero. This proves preservation of any
external reference, not merely agreement on classical inputs.

The compute uses four T/Tdg gates; H, CZ, measurement, dispatch and X reset
add zero T. All their other target resources and feedforward latency remain
chargeable. For a construction with exactly W-1 independent such carry pairs
and no other T resources, widths W=1,2,3,5 give 0,4,8,16 T respectively.
These are algebraic counts of that stated construction, not an execution of
a sibling arithmetic generator or a claim about all adders.

### F3. Closed-window relocation: legal source and delayed schedule

Use the following legal source; C_src is native exact CCX(a,b;g):

```text
g = qalloc any 1
C_src
cx g y
C_src†
qfree g                     # original legal K65 carrier
h a                         # after: this concrete source occurrence
```

The source interface operation is `V=H_a W`. A core implementation can use
`compute_events` to replace C_src by C, after proving the clean-boundary
isometry. It replaces the owned source inverse/release by this delayed trace:

```text
compute C; cx g y; h a
h g; measure_z g -> m; dispatch m
when m=1: h a; cz a b; h a  # H_a D H_a, in time order H,CZ,H
when m=1: x g
release g
```

Each of the three correction gates is a reserved conditional slot. The
corrected branch maps are `K_m=H_a W/sqrt(2)`. Without the transported
correction, a stale CZ gives `D H_a D W/sqrt(2)` on m=1 and fails the channel.
For input `(a,b,g,y)=(0,1,0,0)`, the correct final vector is
`(|0,1,0,0>+|1,1,0,0>)/sqrt(2)`.

The literal sequence `C; CX(g,y); H_a; C†` is a different operation, yielding
`(|0,1,0,0>+i|1,1,1,0>)/sqrt(2)` on that input. It leaves g=1 with
probability 1/2 and is not the reference. With the optional rule in G,
the source may spell C and C† literally at the original legal points;
the late literal adjoint is still invalid. This distinction closes council
B1/L2P-1 without changing source bytes merely to mean a different ordering.

### F4. Minimal relocation without optional provenance

Legal source: `d=qcopy a; quncopy a d; h a`. Its interface operation is H.
Delayed realisation: `d=qcopy a; h a; h d; measure_z d -> m; dispatch m;
when m=1: x a; when m=1: x d; release d`. Since `H Z^m H=X^m`, each
corrected branch is `H/sqrt(2)`. Input zero yields `|+>_a|0>_d`.
Literal `qcopy; H; quncopy` instead entangles the two wires and leaves
d=1 with probability 1/2. This core example uses only existing `perm`
source rules and proves that G is not necessary for the closed-window repair.

### F5. Controlled diagnostic and logical inverse

As a diagnostic outside this amendment's admitted measurement context,
coherently controlling the compute by q encodes `q*a*b` in clean g.
The outcome-one correction would be CCZ(q,a,b), not an unconditional CZ(a,b).
Both q=0 and q=1 sectors produce random X-measurement outcomes even though
the q=0 workspace remains zero before H(g). The exact checker confirms the
CCZ branch identity on all q values and rejects missing q in the correction,
including off-diagonal q matrix units. It does not infer a zero-T controlled
CCZ correction, publish a controlled measurement contract, or treat that
diagnostic as conformance admission. Under control the implementation uses
the sanctioned unitary fallback with its separately matched costs.

For the uncontrolled open-window operation W=W†, a fresh checked measurement
implementation can implement its logical inverse. For the delayed operation
H_a W the inverse is `W H_a`, so the inverse source applies H_a first and
then the AND/use/cleanup implementation of W, with fresh outcomes. Each
inverse branch is `W H_a/sqrt(2)`; composing forward and inverse gives
`I/2` for each of four outcome pairs and exactly the identity channel.
There is no physical adjoint of a measurement trace.

## G. Optional efficiency amendment: clean-isometry provenance

Accept or defer this part independently. Deferring it cannot keep the core
measurement ban or close b-isa-spec-bwm. It does not assert that North Star
promises provenance promotion, or that a relative-phase gate becomes a
permutation on arbitrary inputs.

### G1. §6.1 insertion after the provenance definition

<!-- before:6.1-optional -->
```text
Every workspace bundle version, location version and cell version has
provenance `perm` (computed by permutation gates from its **dependency
set** S of versions) or `other`. Cell versions `(region, i, v)` advance on
every write. Π is the effective control context at the instruction.
```

<!-- after:6.1-optional -->
```text
Every workspace bundle version, location version and cell version has
provenance perm (computed by permutation gates or an exactly certified
clean-isometry boundary from its dependency set S of versions) or other.
Cell versions (region,i,v) advance on every write. Pi is the effective
control context at the instruction.

Optional clean_isometry rule: a contiguous source sequence C may be
certified as C|x,0_G,0_A> = |x,f(x),0_A>, with exact amplitude +1
on every x, where ordered x includes all read-only inputs, dependency
versions and effective coherent controls, G is allocated clean output,
and A is explicitly declared internal clean workspace. No other wire
or cell is modified. The certificate binds all concrete source points,
ordered wire/version identities, controls and clean lifetimes. All
columns on this clean-input subspace are checked exactly, with all
untouched components and internal workspace restored. For each input
column the claimed f(x) is a canonical fixed-width bit string; there
are no duplicate, missing or out-of-range columns. Finite exact checks
or independently checked compositional proofs may discharge the
equality; numerical or basis-value-only evidence cannot.

At that source boundary only, G has perm provenance with the union
of the declared input dependency sets, the input versions themselves
and effective control versions. Its source cleanup may be the exact
sequence adjoint within the resulting §6.2 window, including after
read-only uses permitted for perm values. Dirty-input behaviour is
not certified. Internal gates keep their actual classification;
process/unitary/channel claims still check their complete amplitudes.
This rule does not invoke T3 on a non-permutation emitted circuit.
```

### G2. §11/K81 sequence matching, before occurrence matching

<!-- before:11-K81-optional -->
```text
**Source cleanup-pair partition (K81).** Consumers MUST form the following
partition from the source before K65 selection and K80 expansion. Match
source operation occurrences by §5.3 and §6.2, against the most recent
```

<!-- after:11-K81-optional -->
```text
**Source cleanup-pair partition (K81).** Consumers MUST form the following
partition from the source before K65 selection and K80 expansion.
If the optional clean_isometry rule is accepted, a checked contiguous
computing boundary and its explicitly written exact sequence adjoint
are indivisible sequence occurrences for this partition. Match their
external versions and effective controls by §6.2 before considering
their internal inverse rows; those rows have no competing owners.
An unchecked boundary is not formed. Overlapping boundaries or any
double ownership of source rows are ill-formed. Every existing
intrinsic boundary and the joint-operation/first-release rules below
remain in force. This recognition establishes only the declared
clean-subspace boundary, not equality on a dirty target.
Match source operation occurrences by §5.3 and §6.2, against the most recent
```

### G3. §12.1 structural row

<!-- before:12.1-optional -->
```text
| `structural` | `{ "rule": "translation_lemma" \| "inverse_pair_library" \| "adjoint_table", "subclaims": [indices], "witness": … }`; for `translation_lemma`: `{ "V": [points], "W": [points], "X": [wires], "B": [wires], "frame": [first point, last point] }`; for `inverse_pair_library`: `{ "library_closure_hash", "claim_index" }`; for `adjoint_table`: `{}` | check the rule's side conditions syntactically against the object and the subclaims' results |
```

<!-- after:12.1-optional -->
```text
| `structural` | `{ "rule":"translation_lemma"|"inverse_pair_library"|"adjoint_table"|"clean_isometry", "subclaims":[indices], "witness":... }`; existing rule payloads unchanged; clean_isometry witness `{points,inputs,targets,internal,controls,table}` | existing rules retain their side conditions; clean_isometry checks §6.1's exact complete-column equality, lifetimes and untouched wires against source gate matrices, or a checked compositional derivation of that same equality in subclaims; table rows are `{input:"<fixed-width bits>",target:"<fixed-width bits>"}`, in lexicographic input order, exactly once per input |
```

`points` is the ordered concrete source-point list; `inputs`, `targets`,
`internal` and `controls` use D3's resolved wire/version records in declared
bit order. All are explicit arrays; inputs contain controls in their declared
positions and controls repeats their identities solely to check the context.
The exact equality restores controls unchanged on both branches, including
the disabled branch with amplitude +1. The claim binds its source closure
and K13 invocation (or proves parameter-uniform side conditions for all valid
arguments/budgets). It has no schedule-hash cycle. For C it proves only
the four clean columns in F1 and provides `perm` provenance at its endpoint.
It cannot authorise replacement of arbitrary-target CCX or stale source
versions, and supplies no channel proof for subsequent measurement cleanup.

## H. Conformance vectors and interpreter work

### H1. Required vectors (publish with the amendment)

Append before the existing Suite H/K77 paragraph:

<!-- before:15-vectors -->
```text
**Suite H / §11.1 K77 adapter vector.** Captured `oracle_invocation`
```

<!-- after:15-vectors -->
```text
**Private-cleanup conformance (K85).** Suites C/D/E/F/G/H include the
following positive and negative vectors. Exact channel checks include
zero-error private measurement realisations; suite D's old zero-pivot
SDP rejection remains a dual-route negative. Publish legal serialized
source, target, schedule, certificate, bound expansion identity,
expected reserved events/coordinates/resources and expected channel
for each executable vector. Algebra-only and adapter-generated
coordinates are labelled as such, not production-builder evidence.
Vectors include the qcopy delayed-cleanup bridge, four-T AND compute
and measurement cleanup, transported H/CZ/H closed-window correction,
inverse-channel reversal and per-root mixed-object inventory. Negative
vectors exercise phase, dirty targets, stale correction/versions,
missing outcomes/reset/claims, forbidden outcome escape, control
context reuse, conflicting ownership, illegal source and dependency
relocation, timing, capacity and hash binding. A basis-only or
host-limited result never discharges a channel execution obligation.

**Suite H / §11.1 K77 adapter vector.** Captured `oracle_invocation`
```

| Vector | Expected result and determining check | Status in this note |
|---|---|---|
| AND-8COL | Eight F1 columns, including all dirty g phases; C is not CCX | Exact replay passed |
| AND-INVERSE | 32 full C/C† columns with an independent untouched wire; eight clean compute/use/C† columns | Exact replay passed |
| AND-MBU | Eight logical input columns × two outcomes; both branches W/sqrt(2); all 64 matrix units | Exact replay passed |
| AND-DELAY | Legal source in F3; two branches H_a W/sqrt(2); all 64 matrix units; g clean | Exact replay passed |
| COPY-DELAY | Legal qcopy/quncopy/H source; delayed branches H/sqrt(2), input zero gives + with d=0 | Exact replay passed |
| LATE-INVERSE | Literal C/use/H/C† and qcopy/H/quncopy fail workspace cleanliness/source validity | Exact replay passed |
| CHANNEL-NEG | Missing CZ, stale CZ after H, and missing q on diagnostic controlled correction fail full channel | Exact replay passed |
| RESET-NEG | Omit outcome-one reset; retained private g is one | Exact replay passed |
| AND-ADJOINT | Source inverse W or W H_a; fresh outcome branches and four forward/inverse outcome pairs yield identity channel | Exact replay passed: 16 inverse branch columns, 32 round-trip branches |
| EXT-REFERENCE | Check off-diagonal E_ij for arbitrary external reference, including q coherences in diagnostic | Exact replay: 384 matrix units across the three AND contexts |
| CORE-NO-PROVENANCE | Native CCX-based legal source and qcopy-based legal source selectable without G | Contract/source fixture requirement; not interpreter-tested |
| OUTCOME-NEG | Missing/duplicate outcome string; outcome in host output, tape, hostcall or launch record; measure interface/borrowed wire | Required schema/privacy negatives; not interpreter-tested |
| PAIR-NEG | Invalid late source cleanup, wrong original carrier, reused inverse occurrence, overlapping compute replacement, implicit constructor carrier | Required production-source negatives; not interpreter-tested |
| BIND-NEG | Wrong schedule/target/expansion hash, missing nested/default-only context, wrong args/token tuple or versions | Required certificate negatives; not interpreter-tested |
| CONTROL-FALLBACK | Inherited q=0/1 and both qif polarities select unitary cleanup; uncontrolled witness reused under control fails | Required admission/fallback test; controlled channel algebra is diagnostic only |
| TIMING | Measurement ends at 2, feedforward latency 3: dependent correction starts >=5 and after dispatch; 4 rejects | Exact threshold arithmetic; scheduler vector required |
| RESERVATIONS | Both outcomes have identical reserved ordinals, padded time/resources; extended g lifetime may raise peak/capacity | Required event/resource vectors; not interpreter-tested |
| VERSION | 0.9 library/target cannot accept new events; 0.10 binds new envelope/profile; old 219 recipes unchanged | Old catalog hash/count replay passed; new publication pending |
| MIXED | Native main/libc plus marked AND root A and root B; root-relative [] and shared callee checked separately; no host quantum inventory | Required container association fixture; not interpreter-tested |
| OPTIONAL | Exact clean C table passes G; dirty-target waiver, missing phase, omitted controls, partial table and overlapping boundaries fail | F1 exact equality passed; schema/source tests pending optional acceptance |

These pending fixtures are implementation acceptance requirements, not claims
that this documentation job ran production conformance or implemented a
container. R3 forbids full gates; the focused verification here is limited to
the exact witnesses, source-anchor consistency and historical catalog identity.

### H2. sol-ref09 implementation impact (precise handoff)

The [current interpreter](../../../reference-interpreter/src/metadata_schema.rs)
enumerates cleanup as reverse/recompute and channel claims with the dual
payload. Its `tests/cleanup_partition.rs` explicitly labels its K81 carrier
formation a finite source adapter, not production Expander output.
sol-ref09 must change the following after contract acceptance;
none of these files is edited by this job:

1. Version admission: add the agreed 0.10 ISA/object/sched/cert/target vector
   and ref@0.10 hash/profile without changing 0.8/0.9 parsing or defaults.
   Keep seven-component version and signature ABI binding explicit.
2. `metadata_schema.rs`, `metadata.rs` and schedule-domain parsing: add
   measure_fixup/witness, Boolean mbu, private measurement cost record,
   event union, exact channel payload and D3's closed record schemas.
   Reject unknown fields, missing costs, aliases and wrong conditional kinds.
3. `source_constructor.rs`, `source_constructor/action.rs`, `validation.rs`
   and the production cleanup-partition path: implement/complete legal K81
   pair derivation before selection rather than importing finite-adapter
   carrier assignments. Use the source version/provenance checks and
   retain original source versions/carriers, then attach checked relocation
   and optional owned compute replacement. Do not admit literal late source
   cleanup or absorb excluded constructor cleanup. Preserve K63/K64/K80
   occurrence identities and unique ownership across every context.
4. `ref_library.rs` and `conformance/src/ref_language.rs` event expansion:
   implement the explicitly bound new
   profile; emit measure_z, dispatch, reserved conditional gates, reset and
   release with C3's coordinates; bind every operand/lifetime version and
   nested argument/token/budget from source. Outcome choice cannot renumber.
5. Scheduling/timing/resource path: validate removed/added graph edges,
   acyclicity, after placement, live versions, extended lifetimes, topology,
   capacity, padded charges, dispatch time, latency and outcome-independent
   epsilon-share population. Leave other dependency edges intact.
6. `quantum.rs`/`action.rs` and the realised-event executor: add private branch maps
   and deterministic exact verification of all outcomes, not a public CC
   measure opcode. Execution may sample with Born probabilities, while the
   verifier enumerates all branches. Reset and privacy checks happen before
   deleting workspace. Keep outcome storage separate from host/result/tape.
7. `certificate.rs` and exact arithmetic in `exact.rs`: build complete
   source and realised maps independently; add exact matrix-unit channel
   equality, trace preservation, exact restoration and context coverage;
   retain the rigorous dual route unchanged. Record host-limit checks as
   unchecked and forbid using them for executable verification. Branch
   operators are on complete interfaces, not just measured wires or basis
   populations. Channel proofs do not become operator-norm phase proofs.
8. `machine.rs` and launch/history handling: distinguish private
   cleanup from source measure frames; expand and verify the logical inverse
   with fresh private outcomes for adjoint calls, segment uncall and whole-run
   reversal. Keep explicit-source-measure and unverified-free restrictions.
9. Certificate loader/binding path: resolve schedule witness ids, require
   exact definition equality with the certificate, and bind all event bytes
   in schedule_hash without a hash cycle; require successful channel proof
   before affected effects;
   validate per-device object/root records and external inventory association
   without inventing an ISA record for native main or host libc. General
   mixed launch/host-memory mechanics remain with bennett-4ht owners.
10. If G is separately accepted, add source-bound exact clean_isometry
    proof validation, boundary transfer and indivisible sequence pairing;
    do not classify emitted H/T as permutation gates or alter T3.
11. Add H1 fixtures to the existing focused `isa09_source_schedule`,
    `cleanup_partition`, `cleanup_ownership`, `isa09_certificate`, quantum,
    version, resource and reversal tests, using the new version where
    appropriate. Confirm old-version negatives and compatibility fixtures.
    Keep adapter/algebra evidence distinct from production-builder results.

The file names above are navigation points, not permission to reuse another
repository's code across a published-spec boundary. The required behaviour,
record schemas and verification conditions are the contract.

## I. Hashes and catalog impact

The existing ref@0.9 envelope was independently recomputed from its bytes:
219 recipes, SHA-256
`5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197`.
The focused script checks both values. No catalog bytes or native gate
definition are changed by this note.

| Object | Impact when the proposal is published/used |
|---|---|
| Existing 0.9 source/object | Unchanged when left 0.9; no retroactive CCX reinterpretation |
| Same source migrated to ISA 0.10 | §9.2's `isa=` envelope line changes interface/closure hashes and their transitive callers/SCCs; regenerate canonical references and examples, never reuse the old identity |
| Signature ABI | Remains 0.9 absent a separate ABI change; this does not suppress the ISA-envelope change |
| Source cleanup relocation | Schedule/certificate implementation choice; for a fixed ISA version, no source-byte rewrite or semantic source-envelope field is added |
| Optional literal C boundary | Claims do not enter source identity; changing source from CCX to literal C does change source bytes/hashes; a source hash does not certify the boundary |
| Target | mbu/cost/profile/version byte changes alter target_hash; old mbu=false target remains valid for unitary cleanup |
| Schedule | New expansion identity, witness id, cleanup_witnesses definitions and entries change schedule_hash; every event/placement/dependency byte is committed and compared with the certificate |
| Certificate | Channel claims, cleanup records/resources/context sets and version vector change certificate bytes and certificate_hash; source identity excludes these metadata sections |
| Expansion | New ref@0.10 canonical document/profile and `isa=0.10/expansion=ref/version=0.10` envelope have a new published hash; no fabricated hash here, no mutation of ref@0.9 |
| Fat object | Device roots bind their own migrated object/closure/schedule/certificate identities; outer inventory changes separately; native-container hash is not object_hash |
| Resources | C compute four T; zero-T cleanup still charges H/CZ/X, measurement, dispatch, latency, occupancy and capacity; controlled correction has its own costs |

Acceptance requires simultaneous publication of normative clauses, the new
closed schema/profile, actual library bytes/hash, source/schedule fixtures and
focused consumer support. This note completes the amendment deliverable;
it does not close the live capability gap or the mixed-launch boundary bead.

## J. Council round-1 blocking-item disposition

The [round-1 report](../../../../bennett/docs/council/contract-l2p-2026-11-02/round-1/report.md)
exists and grades the earlier note (snapshot prefix ec16084f8a5b), with sol
and codex both requesting revision. This amendment does not claim a new
council acceptance. The user brief names sol+astra; the recorded report's
actual member labels are sol+codex, which are the labels mapped here.

| Recorded blocker | Text supplying the repair | Determining witness |
|---|---|---|
| sol B1 | B1/B2 and C2/C3/D3 bind the unchanged legal source pair at the original carrier, permit only explicit checked dependency relocation and account for actual versions/lifetimes | F3 correct source vs schedule and literal-late-inverse negative; F4 qcopy bridge independent of G |
| codex L2P-1 | Same source-to-schedule bridge; whole-region channel against the original source, no access to a source-released lifetime and no inference from the late literal adjoint | H1 AND-DELAY/COPY-DELAY/LATE-INVERSE, exact branch and matrix-unit checks |
| sol B2 | D1 and D3 delimit device channel subjects, per-object/per-root certificates, outer inventory, native host/argv/envp/libc and private measurement inventory | H1 MIXED fixture requirement; A's shared scoping statement and D3's remaining mixed-launch obligations |
| codex L2P-2 | Same device scope; selected exported root and materialised native comparison bind the marked closure and its callees, not the whole host | Native main may call ordinary libc, launch marked AND A, then continue natively; only A's device closure has this channel certificate |

The report's nonblocking corrections are also incorporated: A corrects §9.6;
B2/E1 distinguish private events and source measure; C1/C2 account for reset,
dispatch, latency and unconditional reservations; C3 fixes leaf coordinates;
D1/D2 add exact zero-error verification without weakening the SDP; C4/E2 keep
private events distinct from unitary gate names and historical library bytes.

## K. Self-check and evidence boundary

Run this focused command (2 GiB address-space cap, 90 CPU seconds, 120 seconds
wall timeout; headless; no /tmp artefacts):

```sh
env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER TMPDIR=/home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/notes/2026-11-02-rev3/.tmp prlimit --as=2147483648 --cpu=90 timeout 120s python3 -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/notes/2026-11-02-rev3/verify_l2p.py
```

The script checks the exact circuits/channels, all BEFORE spans against the
published file, required topic coverage, relative links, code fences and the
historical catalog envelope/count. It writes nothing. The resulting PASS
lines are recorded in the job Resume block after verification. No full gate,
reference-interpreter test, sibling generator or new-release catalog was run.
Those implementation/publication obligations remain open under b-isa-spec-bwm
and bennett-4ht; completing this note is not evidence they are implemented.

---

## Dossier part: checker-fault-rate (run contract-checker-fault-rate-2026-11-02; accepted by sol, codex in round 3; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-02-rev4/checker-fault-rate.md)

# Checker fault rates — oracle-only, invocation-bound recounts

Full round-4 revision for council review, 2026-11-02; checker request 3
in the existing cross-repo filing queue. Supersedes
`2026-11-02-rev/checker-fault-rate.md`; proposal only. This document
retains the complete accepted recount contract and replaces its unsupported
artifact-transport premise.

## Defect classification and North Star scope

ISA 0.9 §12.3 names fault_rate.domain, faults_by_code and two exclusion
counters but provides no invocation binding for them. K13 binds claims
individually and scheduled certificates at the root; several claims or
callee contexts can use different args/budgets. §§5.2/14.1 makes F_B
depend on those values. A flat recount is therefore ambiguous. This is
an S0 contract gap, not a change to oracle execution.

A separate gap is explicit here: §§12.1–12.3/14.1 name exclusion counters
but do not define independently replayable exclusion evidence. The first
note's assertion that this validation was already specified was wrong.
The repair below supplies that obligation and a concrete default.
North Star §§3.2/5.1 separates native-comparison exclusions from reference
validation and records source-definedness assumptions; post-optimization
classifiers do not detect source UB already erased by optimization.

North Star §5.1 requires fault-rate reporting and §8 requires zero on
its acceptance domains. Dropping rates, choosing a convenient budget,
removing excluded inputs from reference validation or treating unchecked
counts as verified would not meet that requirement. Actions remain
supported: §5.3 gives them no fault outcome of their own, so this repair
uses an explicit non-applicable value for their records.

## Alternatives and concrete witnesses

| Choice | Consequence |
|---|---|
| Take the first claim's invocation | Ambiguous and dependent on claim ordering. |
| Restrict a region to one invocation | Removes existing composition capability. |
| Bind every oracle recount explicitly | Recommended; exact standalone invocation or full scheduled context. |

The oracle has x:wire[2], target:wire[2], fault:wire[4], a:i2, and body
`r = lift.add x a; lift.retval r`. At args=["1"], budget
["1","0","0","0"] cannot reach retval: all 4×4×16=256 tuples contribute
code 1. Budget ["2","0","0","0"] succeeds on all 256 with payload
(x+1) mod 4 and code 0. Every tuple includes its arbitrary target and
fault words. Incoming f=1 becomes zero on a code-1 failure; success
leaves it one. The final accumulated fault word is not the fault event.

For a classification-count fixture flagging precisely x=0, 64 of those
256 tuples are excluded from native comparison. Even then B=1 reports
faults_by_code={"1":"256"}, with undefined_excluded="64" separately.
This fixture demonstrates counting and evidence replay; it does not
assert that the two-row reference add itself has source UB. A real UB
classifier must be identified with its materialized program/configuration.

The published controlled-action-09 certificate has `controlled` and
`flip` records of kind perm_action. Neither has an F_B. The corrected
representation puts fault_rate:null on both, without evaluating an
invented action oracle. An action containing the two oracle calls above
also uses null, while its callee records retain both bound recounts.

## Recommended exact spec changes (§12.3)

Replace verification.fault_rate's schema and add the sibling context
field inside verification. The notation RATE abbreviates this record:

```text
RATE = {invocation:{args,budget},domain,faults_by_code,
        undefined_excluded,layout_dependent_excluded,exclusion_evidence?}
verification.fault_rate: null | RATE
verification.fault_rate_contexts?:[{context_key, ...RATE}]
```

Add the following normative rules:

```text
F_B recounts and fault_rate_contexts apply only to kind=oracle records.
For kind=oracle, verification.fault_rate MUST be a RATE; null is reserved
for action and perm_action records.
For action and perm_action, verification.fault_rate MUST be null and
fault_rate_contexts MUST be absent. Null denotes no action-owned fault
outcome, not a verified zero-fault oracle. Each contained oracle
invocation remains subject to the recount obligations in its own oracle
record; no action placeholder discharges those obligations.

Every oracle RATE binds its own invocation using K13's exact typed args,
four-component budget, token-tuple encodings and validation. It inherits
no claim's invocation. Missing or conflicting bindings reject a requested
verified recount before replay; old unbound data cannot discharge it.

The rate is intrinsic to the underlying oracle's §5.2 F_B. Its domain
uses §12.2 resolution, validity, omission-at-zero and enumeration for
that oracle with zero inherited controls. Targets, fault words, inputs,
region cells and declared borrowed components each contribute as the
domain specifies; inherited control wires add no components to this
intrinsic recount. A predicate's basis value does not suppress counts.
The report is not the probability that a root execution reaches a call.

Each enumerated tuple contributes exactly once to faults_by_code[c]
when code(F_B)=c and c is nonzero. The final XOR-accumulated fault word
is never the predicate for this count. All tuples in the declared domain
are recounted, including native-comparison exclusions. Counts use
canonical nonnegative decimal integer strings; omit zero fault-code
entries. Code keys denote nonzero valid fault codes. Each count and the
sum of fault counts are at most n, the exact enumerated domain size.
Exclusion counts are separate, not subtractions from n or faults_by_code.
If limits prevent a legal recount, report unchecked (host limit),
discharging no verified fault-rate obligation; do not shrink the domain,
substitute partial counts, or declare the input domain invalid.
```

### Complete contexts and deterministic compatibility projection

```text
For an oracle present in the complete §12.1 invocation tree of a bound
schedule, including default-covered and predicated-off invocations,
report exactly one fault_rate_contexts record per context when there is
more than one. Use increasing bytewise JCS context-key order. Every
explicit invocation MUST equal that context's resolved args and budget,
including nested token tuples. Equal tuples with different process-local
token ids denote the same recount; the ids are not certificate values.

The required legacy fault_rate is the first canonical context record
with context_key removed. It MUST equal that projection and discharges
only that context. For one context the legacy RATE suffices and MUST bind
that context; an optional singleton context array, if supplied, must
match it. Missing, duplicate, reordered, foreign or conflicting context
records reject the requested report. A standalone oracle RATE binds its
own invocation and domain, with no invented root-context inheritance.
```

This keeps the required old field meaningful; a later arrays-only
interchange version could remove the projection. Claim reordering has
no effect. Full context identity, not merely (variant, control count),
distinguishes different nested token budgets and call occurrences.

### Exclusion evidence and default validation

Add this schema for RATE.exclusion_evidence:

```text
{ materialisation_hash, reference_program_hash, native_build_hash, native_entry,
  invocation:{args,budget}, domain_hash,
  classifiers:[{category,artifact_hash,version,configuration,input_map_hash}] }
```

```text
Exclusion counters MUST be independently reproduced from classification
evidence bound to the same materialized program, native build,
invocation and complete declared domain. materialisation_hash hashes
UTF-8 JCS of the recorded materialisation configuration;
reference_program_hash uses §9.2's oracle interface hash; the containing
region's closure hash and certificate object binding additionally identify
the linked reference program whose classifications are replayed;
native_build_hash identifies the corresponding comparison build, and
native_entry explicitly selects its exported comparison entry/thunk.
domain_hash hashes UTF-8 JCS of the exact domain record, without LF.
Invocation equality uses K13's resolved encodings.

Each category is undefined or layout_dependent. artifact_hash identifies
replayable classifier bytes, version and configuration identify its
semantics/options, and input_map_hash identifies the replayable mapping
from a full interface tuple to native/classifier inputs. All hashed
artifacts must be available by content for a checked result. Multiple
classifiers in one category combine their flagged sets by union; a tuple
counts once per category. Categories may overlap, so their counts must
not be added without computing their union for a native exclusion set.

Default validation replays the identified classifiers and input mapping
on every domain tuple and recomputes both counters independently. When
initial target/fault values do not feed the native program, mapping may
ignore them, but their distinct tuples still each count. A classification
flag reports an exclusion under that declared classifier; it does not
prove complete detection of source-level UB or erase the recorded
definedness assumption. This does not change F_B semantics.

Missing replayable evidence or unsupported classifier semantics makes
the exclusion report unchecked and discharges no exclusion-dependent
acceptance obligation; it MUST NOT mean zero exclusions. This includes
an asserted zero count. A complete F_B recount may still be verified
separately. Evidence that replays to different counts or has conflicting
bindings rejects the requested exclusion report. This is a new validation
contract, not a premise supplied by the pre-repair counter names.
```

ISA 0.9 defines no certificate-attachment transport. This repair introduces
a separate checker input bundle containing the certificate and the required
content-addressed artifacts. By default, classifier and input-map blobs
are supplied outside the ISA object and certificate schemas; artifact_hash
and input_map_hash are SHA-256 of their exact raw bytes. The checker verifies
those digests before replay. Missing required blobs make the exclusion
report unchecked; mismatched digests reject it. Other transports MAY supply
the identical addressed bytes. This bundle is a new checker input contract;
it adds no attachments field to either closed schema. A producer's flag list
alone is not replay evidence. All materialisation, reference-program/closure,
native-build/entry, invocation and complete-domain bindings above still apply.
Native comparison still excludes flagged inputs as the North Star
requires, while reference validation keeps every domain element.

## Mixed fat object (bennett-4ht)

Incorporate [the shared mixed-fat-object scoping statement](../2026-11-02-rev2/fat-object-scope.md#citable-scoping-statement),
including its explicit remaining launch and host-memory obligations.
Add to §§9/10/12: "A fat native binary may embed VM objects only for
marked modules. The launch manifest selects the marked VM entry, with
its actual args, budget, token tuples and image; the certificate covers
that VM closure's oracle contexts. Unmarked host main, argv/envp and
libc are not invented oracle records and need no F_B recount. Classifier
and native-comparison artifacts may be thunks calling the corresponding
materialized marked native entry with captured host state and input
mapping; native_build_hash identifies that build/entry. They need not
translate or replay the entire native binary as a VM object. Required
marked dependencies and runtime shims are recorded; host device handles
remain process-local, with only resolved shapes/tuples entering bindings."

Separate host launches of the same marked arithmetic module under B=1 and
B=2 use separate root schedule/certificate bindings and rates. The native
host binary stays native. fault_rate_contexts enumerates calls within one
bound root schedule: a device action wrapper containing both calls instead
supplies two contexts in that schedule, with distinct call-occurrence keys.
A native comparison of successful inputs uses the corresponding arithmetic
thunk, not main's exit code. Root-relative contexts never identify native
process entry. Each embedded device object/root has its own certificate
association; the external checker bundle associates artifacts with that
certificate's device closure. It introduces no whole-host certificate.

## Round-1 blocking items and resolution

| Item | Change and concrete witness |
|---|---|
| sol FR-1 / codex CFR-1: F_B applied to actions | Oracle-only recount/context rules; null for both published perm_action records. Nested oracle counts remain required. |
| codex CFR-2: unsupported exclusion premise and ambiguous recount domain | Explicit new hash-bound classifier replay default; reference recount retains all 256 tuples even with 64 separately excluded. Unavailable validation is unchecked, never assumed zero. |

## Round-2 blocking items and resolution

The [round-2 report](../../../../bennett/docs/council/contract-checker-fault-rate-2026-11-02/round-2/report.md)
and out-sol.json/out-codex.json agree that FR-1, CFR-1 and CFR-2 are resolved.
Both accept core scope; sol blocks only CFR-3. The convenor table calls the
second seat astra, while the stored report/output identifies it as codex;
this revision follows the actual outputs and claims no new council acceptance.

| Item | Exact resolution and concrete witness |
|---|---|
| sol CFR-3 — nonexistent existing attachment transport | The replacement §12.3 paragraph explicitly introduces the external checker input bundle and raw-byte SHA-256 validation. check_rev4.py supplies both blobs and reproduces 64 exclusions; removing either leaves exclusions unchecked while the independent B=1 recount remains {"1":"256"}; replacing either addressed blob with changed bytes rejects before replay. |

No prior recount or evidence-binding rule is removed. Oracle RATE typing,
reference interface versus closure binding, and separate-launch context
wording also incorporate the round's nonblocking clarifications.

## Hashes, publication and consumers

Recommend an authorized 0.9 K certificate repair. New invocation,
context, null and exclusion-evidence bytes change certificate identity.
Under an unchanged 0.9 semantic envelope, §9.2 leaves source/interface/
closure/object, target, schedule and ref catalog identities unchanged.
A full-version publication instead requires regenerating version-envelope
identities and dependent pins. No publication is performed here.

Producer, classifier harness and checker must implement the same binding
and context rules. Zero-fault rung gates select the actual oracle domain
and invocation; no budget result covers another by guessing. Monotonic
success would require its own proved statement. The existing cross-repo
request remains open for acceptance/implementation; this notes-only job
does not close it or mutate tracker/council files.

## Conformance vectors and verification

Require both 256-tuple budgets, all incoming fault values, B=0, reordered
claims, a mismatched args vector, missing budget, equal token tuples with
different ids, default/predicated-off contexts and two call occurrences.
Duplicate/omit/swap a context, conflict with its invocation or alter the
legacy projection: reject. Test overlapping classifier categories,
missing evidence (including zero counters), stale artifact/domain/native
bindings and evidence that flags 64 tuples without shrinking F_B counts.
An action without oracle callees has null; one with oracle callees still
has null and separately checked callee recounts.

This script checks exact finite reference arithmetic and the counting
witness by hand-model replay; it does not run a certificate or exclusion
checker and does not establish a real source-UB classification.

```python
from collections import Counter
import itertools
import json
import hashlib

rows = list(itertools.product(range(4), range(4), range(16)))
assert len(rows) == 256

def outcome(x, a, b):
    # Two reference rows: add, then retval. No memory or earlier fault.
    return (((x+a) % 4, 0) if b >= 2 else (0, 1))

for b, expected in [(0, {1: 256}), (1, {1: 256}), (2, {})]:
    counts = Counter()
    for x, t, f in rows:
        payload, code = outcome(x, 1, b)
        if code:
            counts[code] += 1
        after = (x, t ^ payload, f ^ code)
        assert (after[0], after[1] ^ payload, after[2] ^ code) == (x, t, f)
    assert dict(counts) == expected
assert (1 ^ outcome(0, 1, 1)[1]) == 0
assert (1 ^ outcome(0, 1, 2)[1]) == 1
# Synthetic replayable classifier fixture; not an assertion about add UB.
flagged = [row for row in rows if row[0] == 0]
assert len(flagged) == 64
assert sum(outcome(x, 1, 1)[1] != 0 for x, t, f in rows) == 256
# The exclusion predicate duplicates across 4*16 initial target/fault values.
assert len({x for x, t, f in flagged}) == 1
counters = {'faults_by_code': {'1': '256'}, 'undefined_excluded': '64',
            'layout_dependent_excluded': '0'}
assert int(counters['faults_by_code']['1']) == 256
# Null is distinct from an oracle's verified zero-fault record.
action_record = {'kind': 'perm_action', 'verification': {'fault_rate': None}}
assert json.loads(json.dumps(action_record))['verification']['fault_rate'] is None
assert 'fault_rate_contexts' not in action_record['verification']
zero_oracle = {'invocation': {'args': ['1'], 'budget': ['2','0','0','0']},
               'faults_by_code': {}}
assert zero_oracle is not None
# Binding changes cannot accidentally reuse a domain digest.
a, b = {'bundles': [0, 1]}, {'bundles': [0]}
def digest(d):
    return hashlib.sha256(json.dumps(d, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
assert digest(a) != digest(b)
print('PASS fault-rate: 768 oracle tuples; 256 faults with 64 separate exclusions; action null distinction')
```


## Round-4 executable witness and evidence boundary

The files [checker-fault-rate.bisa](checker-fault-rate.bisa) and
[oracle_witness.rs](oracle_witness.rs) exercise this exact two-row oracle
through the read-only reference interpreter library. For B=0,1,2 and each
x=0..3, the witness compares the independent reference outcome with the
literal reversible machine, calls its actual commit method for all 4 target
words and 16 incoming fault words, and then inverses every executed step.
It checks the entire initial machine snapshot and clean frames. This covers
768 full interface tuples: 256 faults at each short budget, zero at B=2.

[check_rev4.py](check_rev4.py) supplies two fixed, serialized raw blobs in
an external in-memory bundle: a version-1 synthetic classifier selecting
mapped x=0, and a version-1 input map selecting tuple component 0. Their
literal bytes and raw-byte digests are present in the checker. Replaying
all 256 tuples yields undefined_excluded="64" and
layout_dependent_excluded="0". Missing classifier, missing map and an
asserted-zero count with missing evidence are unchecked. A digest mismatch
in either blob rejects before classifier interpretation; even JSON whitespace
changes fail under the old digest. A replayed count of 63 or conflicting
invocation/domain/program binding rejects. Unsupported classifier semantics
is unchecked. All these cases preserve the independent F_B recount.

This is a finite contract witness, not a production certificate checker,
a native build, a proof of source UB detection, or a complete serialized
multi-context certificate. The latter remains the conformance publication
obligation described above: concrete §12.1 keys, B=1 map {"1":"256"}, B=2
map {}, exact first-context legacy projection, and rejection on missing
contexts or a corrupted projection. It is not claimed implemented here.
The synthetic evidence bindings identify only this fixture's recorded
configuration; no real native-comparison certification is asserted.

Run the focused build and witnesses from any working directory:

```sh
bash /home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/notes/2026-11-02-rev4/run_checks.sh
```

The script unsets GUI/browser variables, sets TMPDIR and CARGO_TARGET_DIR
under .tmp/sol-rev4, bounds build/link processes at 6 GiB and finite replay
at 512 MiB, and applies timeouts. It runs no full gate or git command and
changes no reference-interpreter source. Its recorded outcomes are in
[the shared verification results](verification.md). The earlier inline
hand model remains an independently understandable counting example; the
actual interpreter/machine witness above supplies execution evidence.

---

## Dossier part: fd0 (run td-fd0-2026-11-02; accepted by sol, codex in round 3; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-02-rev4/fd0.md)

# fd0 — round-4 exact import and hierarchical-estimate contract

For `b-isa-spec-fd0`, originating at `b-targets-gyp`. Proposal only:
**target/cert 0.10**, with full-version publication under the repository's
change rules. This self-contained revision supersedes the round-2 fd0 note.
It retains its accepted model contract and integrates launch estimates.
This does not amend 0.9, its catalog, or any consumer.

## Round-1 blocking items and resolution

Read the [round-1 report](../../../../bennett/docs/council/td-fd0-2026-11-02/round-1/report.md)
and both out-sol.json and out-codex.json there, the convenor table and
bennett-4ht ruling. These are proposed resolutions; no new acceptance is claimed.

| Item | Change and semantic witness |
|---|---|
| sol FD0-1 — operational parameter can be rebound by report/invoke | Freeze every transitive operational dependency regardless of role. N=1 gives a one-second bound gate; report/invoke N=2 under that hash rejects. A new N=2 target recomputes value 2 and its hash. |
| sol FD0-2 — standalone subject lacks variant/controls | Require explicit variant and inherited_controls in Report.subject. The same X closure at forward/0 versus forward/1 controls can cost 1 versus 2 seconds; the subjects now differ. |
| sol FD0-3; codex B2 — missing selector called unresolved | Missing objective.model_outputs selector is a validation error. Present selector with free inputs remains symbolic; present selector with concrete inputs evaluates. |
| codex B1 — objective root, parameter bindings and shared reservations unbound | Add ModelInput in request and schedule.bindings.model_inputs, hence schedule_hash; certifying reports must reproduce it. One 90 ns factory reservation of 50 versus 100 qubits gives peaks 50/100, occupancy 9/2000000 versus 9/1000000, and distinct schedule hashes. |
| sol FD0-4 — full 0.10 publication leaves default ref catalog identity wrong | Republish ref isa/version metadata and envelope at 0.10 with all 219 recipes unchanged. Hash changes from 5de4e499… to 83cc9c17…; exact full hashes and reproduction below. |
| sol FD0-5; codex B3 — missing mixed-object report inventory | Add the §12.3 attachment rule and shared-scope citation below. Native main + one device module has device-only model reports; main/argv/libc are outside them. |

## Round-2 blocking items and resolution

The [round-2 report](../../../../bennett/docs/council/td-fd0-2026-11-02/round-2/report.md)
and out-sol.json/out-codex.json confirm all eight round-1 items resolved.
Both accept core scope; sol blocks only R2-1. The convenor table names the
second seat astra, whereas the stored report/output names codex. This note
uses the stored reviewer identities and claims no round-3 acceptance.

| Item | Exact resolution and concrete witness |
|---|---|
| sol R2-1 — ModelInputs unavailable to launch/default estimates | Add the explicit launch 0.10 symbol and §10.1 normative insertion below. Copy/validate model_inputs, require canonical input equality for embedded applicability, bind the supplied map into every default schedule and its hash, and define completeness to include required ModelInputs. The executable finite witness supplies N=3 → 9/100000000 seconds, N=1 → 3/100000000 seconds and a different schedule hash; absent input gives incomplete-model-objective; an embedded N=1 schedule with an N=3 request uses a correctly bound default schedule. |

All operational freezing, selector validation, schedule-bound reservations,
standalone subject fields, versioned catalog publication and device-only
report rules remain. The source-unit coefficient clarification and a
10 ns → 1/100 microsecond invoke vector address nonblocking suggestions.

## Defect, alternatives and scope

This full revision supplies the field-level contract, serialized import,
publication route and acceptance vectors. ISA 0.9 §8.3's
`imports.{model}.{version,map}` cannot bind code distance or formulas to
logical costs, and §8.2's leaf-event aggregation cannot express a factory
hierarchy. `bd show b-isa-spec-fd0` confirms the missing exponentiation,
code-distance selection and symbolic-count questions. Both published
versions' §8.1 languages lack the required parameter/quantity bindings.

The alternatives are: (1) fully bind a model externally into a concrete
0.9 target, preserving source and hierarchy as provenance; this keeps
concrete estimates available but cannot interchange symbolic models;
(2) add parameter expressions alone, which leaves destinations, hierarchy
and resource ownership undecided; (3) the selected model-as-data plus
separately bound hierarchy report, specified completely below. Summing
all quantities or treating physical failure risk as epsilon is unsound.

Decisions in this proposal are deliberate:

- The extension is nested under `imports.<name>.model`; the old numeric
  import shape is retained. No new top-level `model_parameters` namespace
  or implicit vendor-name binding is needed.
- Source identity hashes **raw supplied bytes**, with the bytes embedded;
  a second hash identifies the canonical normalized model. Canonicalizing
  a vendor file first could lose significant numeric spelling or metadata.
- Units have dimensions and scales, not just labels. Parameters distinguish
  hardware, code distance and algorithm inputs. A code distance is positive
  integral; its declared domain chooses parity. An unconditional odd-only
  rule would wrongly exclude codes with even distance.
- A new `model` resource kind holds named non-additive outputs. A numeric
  physical/logical ratio is not summed as a qubit count, nor is per-cycle
  risk a gate epsilon. Legacy count charges keep their old meaning.
- Every numeric substitution has a JSON Pointer, unit conversion, rounding
  rule and checked resolved value. The hierarchy has an exact node grammar,
  half-open intervals and single-accounted shared-factory reservations.
- Symbolic models are valid inputs. Unresolved **operational** bindings
  prevent producing a concrete schedule, not loading/executing an otherwise
  valid object. Unsupported source expressions stay losslessly present as
  explicit obligations. That preservation is not a claim of full adapter
  implementation: fd0 remains a blocker until promised adapters work.

North Star §§4.3–4.4, §5.1 and §7's Qualtran/Azure RE row require all named
resources, independent checking, symbolic hierarchy and models as data.
All §8 demo rungs, especially Grover over unmodified SQLite with its
N=2^20 estimate, remain unchanged. A scalar-only subset, source rewrite,
mandatory gate materialization, or rejecting algorithms because a model
is symbolic would narrow that scope. The proposal below retains symbolic
models and a concrete instantiation path without making either executor
understand a vendor's implementation language.

## Publication edits

In the **new version**, extend §8.2's resource kind enumeration with
`"model"`; append `dimension` and `scale` metadata as specified below;
extend §8.3's `imports` entry with optional `model`; add §8.5 below; add
`model_estimates?` to §12.3 region records and the §12.3 paragraph below.
Add a §0 semantic entry referencing fd0/gyp and suite E/H vectors.
Extend §11 requests/schedule bindings with model_inputs and the additive
setter below. Extend §§10–10.1 with the versioned launch-estimate symbol,
complete-request definition, embedded matching and default binding specified
in the corresponding §10.1 insertion below. The text from “8.5” through “End normative insertion” is the proposed
normative insertion, including its tables. No unspecified field or
inferred default is part of it.

### 8.5 Imported models, parameters and hierarchical estimates (proposed normative text)

An import MAY retain the legacy form `{version:string,map:object}`. Such
an entry has its existing scalar import meaning; no QEC selection,
hierarchy, physical-error guarantee or new parameter is inferred from it.
An entry using this section has exactly `{version,map,model}`. `version`
is the nonempty imported-model version, not the ISA sub-version.
`model.schema` MUST equal `"bennett.import-model/1"`. All fields shown
below are required unless suffixed `?`; absent optional arrays/maps are
empty. Duplicate JSON keys, unknown fields, and unknown schema versions
are invalid model encodings, rather than instructions to ignore data.

**Scalar and unit types.** In the following schemas `S` is a nonempty
Unicode string compared bytewise, `H` is exactly 64 lowercase hexadecimal
digits, `Hex` is an even-length lowercase hexadecimal string (possibly
empty), and `Q` is a reduced rational encoded as a string: `0` or a
canonical signed decimal numerator, optionally followed by `/` and a
positive canonical denominator greater than one. No leading `+`, leading
zero, `-0`, denominator one, or reducible fraction is permitted. `Z` is
the integral subset of Q, `N` the nonnegative integers, and `P` the strictly
positive rationals. Mathematical integer ranges are unbounded; an implementation
resource limit is an explicit unfinished-operation diagnostic, not a
model-domain restriction or an executed program fault.

A `Unit` is `{dimension:{S:Q},scale:P}`. Its dimension map omits zero
exponents. Axis `s` denotes seconds; `physical_qubit` and `logical_qubit`
are distinct axes. Other axes MUST include their source format and version in the axis
identifier, unless an explicit dimension-preserving conversion is present in the normalized
formula. An axis spelling itself is its identity; there is no implicit
unit-equivalence registry.
Equal labels alone imply no equivalence. A numeric value x in this unit
has base value x*scale and the given dimension vector. Fractional
exponents are admitted. Dimensionless units have `{}`. Unit metadata is
not an approximation or an instruction to sum quantities.

A target resource participating in a typed map MUST declare
`dimension:{S:Q}` and `scale:P` in addition to its §8.2 `unit:string`.
Its `unit` remains the display label. These two fields are optional and
have no effect for resources not participating in this section. The
mandatory `time` dimension is `{s:1}`, scale 1. Ordinary logical peak is
`{logical_qubit:1}` and logical occupancy is
`{logical_qubit:1,s:1}`; physical model outputs retain physical axes.
A resource of kind `model` MUST supply this metadata; it has no automatic
§8.2 scheduled-event aggregation and is reported in `model_estimates`.
The required scheduled `time`, `peak_qubits` and `qubit_second` accounting
remains in force. An objective that references a model resource MUST supply an explicit
selector in the new optional `objective.model_outputs` map:

```text
objective = {weighted:{S:number},model_outputs?:{S:Selector}}
          | {lexicographic:[S,...],model_outputs?:{S:Selector}}
Selector = {model:S,node:S,metric:"duration"|"counts"|"occupancy"|"peak"|"quantity",
            pool?:S,resource?:S,quantity?:S}
```

Each model-resource objective term has exactly one selector keyed by that
resource name; other selector keys are invalid. A missing required selector
is a model validation error at objective.model_outputs.<resource>, not a
symbolic or unresolved expression. Model/node name the
hierarchy evaluated using the resolved target and that objective term's
explicit ModelInput below; no analytical report implicitly supplies inputs. Duration has seconds units and no optional selector field;
counts requires resource, quantity requires its local quantity name, and
occupancy/peak require pool; other optional selector fields are forbidden.
Quantity selects that model output and converts through its map, counts
selects its aggregate count, and pool metrics
select the model-qualified pool. The selected dimensions must agree with
the objective resource's and the value is converted to its scale. Existing
weighted/lexicographic rules then apply to that scalar. An unbound
objective is retained symbolically and has no silently assigned scalar
value or completed concrete optimization verdict.

**Objective input binding (§11 extension).** The scheduling request and
schedule.bindings gain optional `model_inputs:{S:ModelInput}`. When there
are model-resource objective terms, its keys MUST equal exactly their
resource names; with none, omit it or use {}. Each entry is:

```text
ModelInput = {
  root:{model:S,node:S},
  models:{S:{model_hash:H,parameters:{S:ClosedExpr|null}}},
  shared:[Shared,...]
}
```

The root MUST equal the term's selector model/node. The models map lists
exactly the transitively referenced models, their model_hash and every
parameter once, in its declared unit. Parameter resolution, domain checks,
operational freezing, invoke bindings and Shared use exactly the report
rules below. This whole entry, including root, parameter expressions and
reservations, is copied/validated by the request and serialized in
schedule.bindings; it participates in schedule_hash. ModelInput supplies
only classical model data and never coherent input values. A missing
required entry gives an explicit incomplete-model-objective diagnostic,
with no completed concrete schedule or optimization verdict. A present
well-formed input with free dependent parameters retains a symbolic
objective. The launch-estimate path carries the same ModelInput map under
the corresponding §10.1 insertion; defaults never supply omitted model
parameters or reservations. A malformed root/model/hash/selector/parameter/reservation is
an explicit validation error, not an arbitrary choice of another report.
Only a complete concrete input can support a completed concrete objective.

A report used to certify an objective MUST bind the same device subject
and context and reproduce that entry's root, models and shared values
byte-for-byte after JCS. Other analytical reports may coexist and cannot
retarget the objective. Changing only report outputs cannot change the
schedule-bound objective input. Different legal shared reservations or
algorithm bindings create different schedule identities even under one
target_hash. A template with unresolved operational bindings still needs
a newly resolved target before concrete scheduling, as specified below.

Add this symbol in the new sched 0.10 ABI; JCS bytes are copied and
validated, with the ordinary §11 ownership/status convention:

```c
bennett_status bennett_sched_request_set_model_inputs(
    bennett_sched_request_t*, const uint8_t* model_inputs_jcs, size_t len);
```

This extends an explicitly versioned interface, not an existing C layout.
The target selector identifies what to measure; ModelInput identifies the
exact inputs used to measure it. No model-input hash is supplied in place
of these bytes.

**Normalized model schema.** The import key supplies the model name.
Names of units, parameters, quantities and nodes are local to that model.
`model_hash` is SHA-256 of UTF-8 JCS bytes of the complete `model` object,
without a final LF; `source.sha256` below hashes the decoded raw bytes.

```text
model = {
  schema: "bennett.import-model/1",
  source: {format:S,version:S,media_type:S,bytes:Hex,sha256:H},
  units: {S:Unit},
  parameters: {S:Parameter},
  quantities: {S:Quantity},
  bindings: [Binding,...],
  nodes: {S:Node},
  assumptions: [S,...]
}
Parameter = {
  role: "hardware" | "code_distance" | "algorithm" | "other",
  type: "integer" | "real", unit:S, value: ClosedExpr | null,
  domain: {min:Q|null,max:Q|null,parity:"any"|"odd"|"even"}
}
Quantity = {unit:S,role:"duration"|"demand"|"risk"|"count"|"scalar",expr:Expr}
Binding = {path:S,quantity:S,factor:P,rounding:"exact"|"upper"|"lower",places:N,value:Q|null}
Expr = Q | {lit:Q,unit:S} | {param:S} | {quantity:S}
     | {op:Op,args:[Expr,...]}
     | {external:{location:S,unit:S}}
Op = "+" | "-" | "*" | "/" | "min" | "max" | "ceil" | "pow" | "sqrt"
ClosedExpr = Expr with no param, quantity or external reference
```

Every unit reference MUST resolve in `units`. `source.format` and
`source.version` identify the exact input grammar; `media_type` describes
its bytes. The normalized formulas and assumptions MUST be retained with
the original source. The import's version and source version need not be
equal, but both MUST be preserved. Hash mismatch is invalid, even if a
file with the same vendor name is otherwise available. No file path,
network fetch, mutable URL, executable host callback, or environment
variable is an implicit source or parameter binding.

`value:null` denotes a free parameter, not zero or an inferred optimum.
Bounds are inclusive, in the parameter's declared unit; null endpoints
mean unbounded, and min MUST NOT exceed max. Parity other than `any`
requires integer type. `code_distance` requires integer type,
dimensionless unit with scale 1, and domain min at least 1; the domain
MAY admit odd, even or all distances. `real` includes exact algebraic real
values expressible by ClosedExpr. A parameter value is a dimensionless numeric ClosedExpr coefficient in
its declared unit; the declared scale is applied exactly once. A bound
integer value MUST be integral in its declared unit. Bound values MUST
satisfy all domain constraints.
No generic model can infer a distance from a risk budget.

A scheduler/estimator MAY select a distance from the declared domain.
Before it uses the value in an operational target binding it MUST write
that choice into the model's parameter value and validate it, thereby
creating the resolved target identity. The target parameter value/domain and target objective identify the
chosen instance. The report records the actually searched domain, search
method and objective as model-qualified verification.assumptions strings,
with no machine-checked optimality claim inferred from that prose. A claim
of optimality requires a separately published, independently checkable
minimality/search witness format; this section introduces no such claim
kind or verdict. Hardware and code-distance values cannot
be overridden under an unchanged target_hash. Algorithm values outside
the operational dependency set may be analytically rebound as below;
Parameter.role never overrides operational dependency membership.

**Expression evaluation.** A bare Q is dimensionless; a typed literal has
its declared unit. Parameter and quantity references denote base values
with their declared dimensions. Addition, subtraction, min and max require
identical dimensions; multiplication adds dimension exponents and division
subtracts them. Binary operators have exactly two arguments, except ceil
and sqrt which have one. `pow(base,exponent)` requires a dimensionless
integral exponent; it scales the base's dimensions by that integer.
Integer exponents may be positive, zero or negative; zero to zero and
zero to a negative exponent are invalid. `sqrt` is the nonnegative
principal root, halving all dimension exponents. `ceil` accepts only a
dimensionless argument and returns a dimensionless integer. Division by
zero and a negative root are invalid. Rational operations, integer powers,
roots and their order comparisons denote exact real algebraic values;
no binary64 evaluation or floating tolerance substitutes for them.

A quantity's inferred dimensions MUST equal its declared unit's dimensions;
its reported numeric value is its base value divided by that unit's scale.
The dependency graph of quantity references MUST be acyclic; forward
references are permitted. Parameters contain no quantity dependencies.
Unknown references and cycles are invalid even if a particular invocation
would multiply their result by zero. Duration, demand and count quantities
must be nonnegative; concrete demand/count quantities must be integral in
their declared unit. Risk quantities must be dimensionless, scale 1, and
in [0,1]. Scalar quantities may be signed. All concrete results must be
finite. Parameter-dependent validity conditions remain explicit symbolic
obligations until discharged for the requested binding.

These are model expressions, not extensions of every §8.1 expression
context. No gate control count, iteration variable, theta, `eps`,
`log2inv_eps`, `eps_decade` or table context is implicitly bound here.
Their old AST spellings are invalid in a model expression. A source
formula requiring further functions is represented by `external`, whose
`location` identifies the exact expression in the preserved source using
that source format's location convention. It has no invented numeric
value. The report MUST retain that expression, identity and the unresolved
interpretation/checking obligation. A pinned adapter may translate it to
the exact AST above; an independent checker must verify that translation
before calling the result checked. Source-model correctness and physical
assumptions are distinct from verification of that translation and its
arithmetic. Unsupported functions MUST NOT disappear, become zero, or
invalidate program execution. Complete support for promised source models
remains required; an unchecked report does not discharge that requirement.

**Named outputs and conversion.** `map` has exactly one entry for every
normalized quantity, using the §8.3 pair shape `quantity:[resource,factor]`.
In this typed form factor is either P (a rational string) or a positive
finite JSON number interpreted by exact decimal text. Rational strings
allow exact conversions such as 1/3; no decimal approximation is required.
The legacy untyped form retains its existing JSON-number factor. In this typed form it MUST equal source-unit scale divided by
destination-resource scale, and dimensions MUST agree. Additional
multiplicity is expressed in the quantity formula, not hidden in this
unit conversion. Several quantities MAY map to one resource with aligned dimensions; each
remains separately identified by model and quantity name, without automatic
summation of their displayed values.
Any quantity without an existing aligned resource MUST receive a newly
declared named resource of kind `model` with the appropriate unit metadata;
it MUST NOT be silently dropped or coerced to an unrelated unit. A count
or risk quantity MAY instead map to a count resource, but is charged only
when explicitly present in a leaf's `counts`. Duration and demand are not
made additive by naming them resources. The report preserves each mapped
quantity independently of whether any target field consumes it.

**Operational bindings.** A binding path is a canonical RFC 6901 JSON
Pointer into the target document, using `~0`/`~1` escaping and canonical
nonnegative decimal array indices. It MUST name an existing field that
the target schema makes numeric or a §8.1 numeric expression. Missing
fields, duplicate paths, ancestor/descendant path conflicts and pointers
into imports themselves are invalid. Every path identifies one field;
array matching by opcode or vendor name is forbidden.

The following are the allowed destinations and their units/constraints:

| Destination | Unit and additional constraint |
|---|---|
| `gates[i].cost[r]`, each qram operation's `cost[r]` | Unit of declared resource r; r MUST NOT have kind model. Costs nonnegative. |
| `classes[c].capacity` | Logical qubits of class c; integer or existing literal unbounded. Only numeric capacities may be bound. |
| `classes[c].qubit_second`, `classes[c].dirty_rate` | Existing class occupancy multiplier, dimensionless and nonnegative. Physical/logical conversion instead uses the hierarchical interval report. |
| `resources[r].rate[c]` | Resource r unit divided by (logical_qubit·s); nonnegative; only occupancy resources have this field. |
| `capabilities.classical_step_time`, `capabilities.measurement.feedforward_latency` | Seconds, nonnegative. |
| `capabilities.max_parallel`, `capabilities.max_predicate_depth` | Dimensionless integer, subject to their existing constraints. |
| `gates[i].controls.min/max`, `schemes[i].realises.controls.min/max` | Dimensionless integer, existing inclusive-range constraints. |
| `schemes[i].ancillae.count` | Logical qubits, nonnegative integer. |

For all other quantities the named-model-output path remains available;
new numeric destination families require their own published schema and
unit rule, never an implicit substitution. This table does not authorize
binding an epsilon, boolean capability, topology, quantum operation,
interface width, source budget or certificate proof field. Imported
physical risk MUST NOT be substituted for gate epsilon, diamond norm,
operator norm, oracle fault rate, or any correctness assertion.

The binding's local `quantity` MUST resolve. Its dimensions MUST equal
the destination's; `factor` MUST equal source-unit scale divided by the
destination unit's scale. Let q be the evaluated base value divided by the
quantity's declared Quantity.unit scale; q is its numeric coefficient in
that source unit. Let x=q*factor, applying factor exactly once.
For `exact`, x MUST be rational and `value` MUST equal x. For `upper`,
`value=ceil(x*10^places)/10^places`; for `lower`,
`value=floor(x*10^places)/10^places`. These bounds use exact comparisons,
including at decimal boundaries. Nonintegral results at integral
destinations are invalid. `places` MUST be zero at such destinations.
Only exact binding is allowed for capability limits and control ranges;
capacity may use exact or lower, and cost/duration/rate fields exact or
upper. Thus rounding cannot overstate a capacity or understate a cost.

A concrete binding overrides the field at its explicit path; the original
field remains as serialized provenance, not a fallback if resolution fails.
Every nonnull `value` MUST be independently recomputed and checked against
the expression and rounding rule. Symbolic templates have `value:null`;
all operational bindings must have valid nonnull values and bound
parameters before concrete scheduling. Changing any operational parameter,
resolved value, formula, mapping, source identity or binding changes the
JCS target bytes and hence target_hash. Scheduling and launch reports bind
that resolved hash; consumers MUST NOT cache under the unresolved target's
hash or reuse a distance selected for another target instance.

Define the operational dependency set as the model-qualified parameters
transitively referenced by any operational Binding.quantity, following
the complete quantity-reference DAG. Compute it syntactically before
arithmetic simplification, including dependencies below zero factors;
external expressions retain unresolved dependency/translation obligations.
Membership is independent of Parameter.role. Every member MUST have a
valid nonnull target value before a concrete schedule is produced. Reports,
ModelInputs and cross-model invokes MUST preserve these resolved target
values; a supplied value for a member is an equality assertion checked
exactly with dimensions/units, never a replacement. A changed value
requires a newly resolved target, recomputed Binding.value and target_hash.
An unsupported external dependency analysis cannot claim operational
resolution checked. Non-operational hardware/code_distance/other values
also retain target values; only non-operational algorithm parameters may
replace defaults/null or receive analytical invoke arguments.

**Hierarchy node grammar.** `nodes` is a finite, acyclic map of reusable
node templates. Child names refer to the same map; invoking another model
is explicit. All node and reference validation precedes evaluation,
including children of a zero-count repeat.

```text
Node = {kind:"leaf",duration:Expr,counts:{S:Expr},
        intervals:[Interval,...],shared_uses:[{id:S,slots:Expr},...]}
     | {kind:"sequence"|"parallel",children:[S,...]}
     | {kind:"repeat",child:S,count:Expr}
     | {kind:"invoke",model:S,node:S,arguments:{S:Expr}}
Interval = {pool:S,unit:S,start:Expr,end:Expr,amount:Expr}
```

Leaf duration and interval endpoints have time dimensions and are
nonnegative. Each interval is half-open `[start,end)`, relative to leaf
start, with `0<=start<=end<=duration`. Amount has the interval unit's
dimensions, is nonnegative, and is integral when it measures physical or
logical qubits. Pool identifies a local accounting pool. Report pool keys are the JCS
encoding of the two-string array [model,pool], used as a JSON object key;
selector pool fields use that same qualified encoding. This avoids aliases
when either name contains punctuation or Unicode. Units
within a pool MUST have identical dimensions and convert to a common
base. Counts name declared count resources and have their dimensions;
values are converted from base units to the resource unit before summing.
Negative charges or any automatic probability composition are forbidden.
Physical risk summed as a charge is an additive model number, possibly
above one, not a declared failure probability or error guarantee.

Sequence places its children consecutively, starting at zero; parallel
places every child at zero; children may repeat and each occurrence is a
separate invocation, not memoized-away work. Empty compositions have zero
duration, counts, occupancy and peak. Repeat concatenates count copies;
count is a dimensionless nonnegative integer, with zero giving the empty
composition. Invoke instantiates the referenced model's node, retaining
its source/units/assumptions. Its arguments are evaluated in the calling model's environment and bind
the referenced model's algorithm parameters, with matching dimensions
and conversion to the callee's declared units. They must satisfy the
callee's types/domains; free caller parameters remain symbolic. Only
non-operational algorithm parameters may acquire new values. An explicit
argument for an operational algorithm parameter MUST equal its resolved
target value; it is an equality assertion. An unequal or unresolved
replacement is a validation error. Other
parameters retain resolved target values. Unspecified algorithm arguments
inherit the report's binding for that model. Dependency cycles, including
cross-model invokes, are invalid; arbitrarily large finite repeats MAY
be evaluated symbolically without materializing their leaves.

Every private interval is instantiated separately at its occurrence's
time origin. Count resources sum once per leaf occurrence. Duration is
the largest leaf end after composition. Pool occupancy is the integral of
simultaneous demand over time; pool peak is its maximum. Concurrent demands
sum, and touching half-open intervals do not overlap. The result MUST be
identical to explicit expansion at any bound finite input, but expansion
is not required. No root total is obtained by summing child peaks or by
adding parent resource totals to their child totals.

Shared resources are declared once by the report's `shared` array, in
root time coordinates. A declaration has exactly
`{id:S,model:S,pool:S,unit:S,start:Expr,end:Expr,amount:Expr,slots:P}`;
model selects the expression/unit namespace, slots is a positive integer,
and other dimensional rules match Interval. Its interval must lie within
the root duration. A leaf shared-use id names that declaration and uses
a dimensionless integral nonnegative number of slots for its full leaf duration. The
reservation must cover that use, and the simultaneous slot demand must
never exceed its slots. Its physical amount contributes **once** to
pool occupancy and peak, independent of the number of references. A
private interval and a shared declaration cannot claim the same physical
allocation; the producer MUST choose one ownership representation and
provide that ownership in its model assumptions. An idle reserved factory
may still consume physical space. Exclusive factories use slots=1;
parallel uses needing two slots are infeasible until separately reserved
capacity or serialization is supplied. No duplicate shared id is allowed.

**Reports, identity and checking.** Add optional `model_estimates:[Report,...]`
to a §12.3 region record. Existing region resources remain the §8.2
scheduled-leaf report. The additional report has this exact schema:

```text
Report = {
  schema:"bennett.model-estimate/1", target_hash:H,
  subject:{closure_hash:H,variant:S,inherited_controls:N,
           invocation:Invocation,context?:ContextKey},
  models:{S:{model_hash:H,parameters:{S:ClosedExpr|null}}},
  root:{model:S,node:S}, shared:[Shared,...],
  outputs:{duration:Result,counts:{S:Result},
           occupancy:{S:{unit:Unit,value:Result}},
           peak:{S:{unit:Unit,value:Result}},
           quantities:{S:{S:{resource:S,value:Result}}}},
  verification:{status:"checked"|"symbolic"|"unchecked",
                obligations:[{model:S,location:S,reason:S},...],
                assumptions:[{model:S,text:S},...]}
}
Result = {exact:ClosedExpr}
       | {symbolic:{model:S,node:S,metric:S,pool?:S,resource?:S,quantity?:S}}
       | {interval:{lo:Q,hi:Q,places:N}}
```

Invocation and ContextKey are the existing exact encodings of §12.3 and
§12.1; absence of context means a standalone invocation, not the first
reached context. variant is a nonempty producer string as in §12.3;
inherited_controls is a nonnegative integer encoded by §9.1. Standalone
reports explicitly bind closure_hash, variant, inherited_controls and
all invocation arguments/budget. Scheduled reports MUST match all those
values resolved at the selected actual context; none is inferred from
another report or from record order. If the alias-binding repair is
adopted, Invocation also carries its token_aliases partition: oracle
prepends its actual invocation token, action/perm_action/CC/R uses token
parameters only (§4.7), with no invented primary action identity. A scheduled report MUST carry the actual context key and
root schedule binding through its containing certificate. Repeated
contexts cannot share one result unless independently shown equal.
The models map contains exactly the transitively referenced models and
their canonical model_hash values. Its parameters map lists every parameter
exactly once in its declared unit. Hardware/code-distance/other parameters and every member of the
operational dependency set MUST equal target values. Only algorithm
parameters outside that set may replace null or algorithm defaults in
this report or ModelInput. A parameter's replacement also applies
to all direct uses of that model unless an invoke explicitly binds another
algorithm value. Such per-invoke arguments are part of the checked DAG,
not one misleading global multiplicity. No coherent state or qubit
measurement may supply a parameter during a coherent region.

Duration is reported in seconds; counts in their target resource units;
peak in the displayed Unit of the pool, occupancy in that Unit times
seconds. The quantity outputs contain, for every referenced model and
every mapped quantity keyed by its local name, its destination resource
name and converted value, in the report-level parameter environment. Locally rebound invocations are
additionally identified by their DAG occurrence when requested individually;
their aggregate contribution follows hierarchy composition, not that
report-level quantity display. Missing metric keys are zero only when
recomputation establishes there is no contribution. Foreign or additional
asserted outputs must be checked, never silently ignored.

An exact result uses a dimensionless ClosedExpr for the numeric value in
the stated output unit. Interval endpoints are rational in that same
unit, lo<=hi; at `places` the checker requires the tight outward decimal
floor and ceiling of the exact result. An interval is a bound, not an
exact point. A symbolic result is a thunk for the specified root/node
metric under the report bindings; metric is exactly `duration`, `counts`,
`occupancy`, `peak` or `quantity`. Counts requires resource, quantity
requires quantity, occupancy/peak require pool, and all other optional
selector fields are forbidden. Model and node must resolve. It retains the entire dependent expression/hierarchy and
all domain obligations, including min/max and interval overlaps; no
unsupported scalar expression is fabricated. Free parameters may stay
null in a symbolic report, including an unresolved hardware design study.
Such a report cannot discharge a concrete operational binding.

The checker verifies all hashes, typed bindings, graph references, domain
conditions, conversions, rounding, multiplicities, reservations, outputs
and context identity independently. `checked` means these obligations
succeeded for concrete parameters; it does not establish that an external
physical QEC model is true. `symbolic` means structural/unit checks
succeeded and unresolved items are exactly the free-parameter obligations.
`unchecked` is required if any translation, external-function or requested
verification obligation remains unsupported; every such obligation MUST
appear with its model, source/AST location and reason. All imported
assumptions appear in the report's assumptions, qualified by model; they
are not proof labels. A claimed checked status with a missing obligation
is invalid. Results do not become permutation proofs, channel bounds,
operator-norm bounds or oracle fault guarantees by appearing in a checked
model report.

Malformed typed input, conflicting binding or a mathematically invalid
concrete expression produces an explicit model/report validation error
with the failed location. An unresolved operational binding prevents a
concrete schedule, with the missing parameter/expression reported. A
capacity/slot-constrained candidate schedule is infeasible with
`E_SCHEDULE_INFEASIBLE` under the existing schedule interface, which permits another schedule. None of these creates
a new ISA fault code, changes F_B, rejects the program as outside the
language, erases an earlier valid loaded state, or licenses a fallback to
zero or a vendor default. An unused or unresolved analytical model does
not prevent execution under an independently valid concrete target.
Unsupported source-format interpretation yields a preserved unchecked
model plus its explicit implementation obligation; it is not a successful
estimate or permission to abandon the promised adapter capability.

End normative insertion.

### Corresponding §§10–10.1 insertion (proposed normative text)

Publish this additive symbol in **launch 0.10**, using the existing
opaque types, status and ownership conventions. It is not an amendment
to the launch 0.9 symbol, object layout or target/certificate schema:

```c
bennett_status bennett_estimate_run_with_model_inputs(
    bennett_program_t*, const char* region, bennett_token,
    const char* variant, uint32_t inherited_controls,
    const uint8_t* params_jcs, size_t params_len,
    const uint8_t* model_inputs_jcs, size_t model_inputs_len,
    bennett_estimate_t** out);
```

Add to §10.1 Resolved request:

```text
A launch 0.10 estimate request additionally carries model_inputs JCS bytes
governed by §8.5. The implementation MUST copy and validate them before
returning an estimate; length is the UTF-8 byte length excluding a NUL.
This is the model_inputs map itself, not a hash, a report, a file path,
or an addition to the signature-order params_jcs array. Subsequent changes
to the caller's buffer MUST NOT retarget the copied request/estimate.
Duplicate/unknown keys and malformed ModelInputs are validation errors.

A default-only effective schedule MUST serialize exactly those validated
inputs in bindings.model_inputs, after JCS canonicalization; they
participate in schedule_hash. The explicit empty-entries default schedule
and every existing object/interface/closure/target/root/variant/control/
accuracy/invocation/expansion binding remain required.

An embedded schedule is applicable only when every existing §5.4/§11
binding matches AND its ModelInputs match the request byte-for-byte after
JCS. An embedded schedule with different model parameters, model identity,
root or shared reservations is inapplicable to this request. Use the §11
default realisation with the requested inputs; do not borrow the embedded
schedule's inputs, silently substitute a report, or reject the complete
request merely because that embedded schedule does not match.

Every complete, well-typed resolved request, including its required
ModelInputs, MUST be supported. This replaces the inherited completeness
sentence for launch 0.10 model-resource requests: complete means the
ordinary resolved classical arguments and valid budget plus the complete
concrete objective inputs and operational target required by §8.5.
Missing required ModelInputs produce incomplete-model-objective before an
estimate is returned; no parameter or reservation is inferred. This is
E_ARG with that diagnostic and no estimate object, not an ISA fault, a
program-language restriction or E_SCHEDULE_INFEASIBLE. A present, valid
input with free dependent parameters retains §8.5's symbolic objective;
it cannot claim a completed concrete estimate/optimization. A malformed
selector remains a validation error, distinct from missing/free input.

For a target without model-resource objective terms, an omitted input map
or {} denotes the empty map and retains the existing complete estimate
path. A null pointer with zero model_inputs_len denotes omission; a null
pointer with nonzero length is E_ARG. A supplied nonempty byte string
MUST encode the map; a zero-length nonnull buffer is also omission.
The 0.10 symbol without model-input arguments is equivalent to omission,
and thus cannot infer inputs required by a model-resource objective.
The ordinary scalar launch 0.9 API and all its required demo estimates
remain unchanged. A model-input error leaves the loaded program and
independently valid execution/estimate paths available.
```

Add to §10.1 Certificate binding:

```text
The effective schedule's bindings.model_inputs MUST reproduce the request's
validated canonical input map. A certifying model report MUST reproduce
its corresponding entry under §8.5 and match the actual device subject
and context. A checker independently validates the supplied inputs,
rebuilds the bound realisation and verifies both the existing scheduled
§8.2 rows and the selected model objective. The two accounting views
remain separate; model-only outputs add no estimate_get scalar row.
Changing only a non-operational algorithm binding or shared reservation
can change schedule_hash and certificate bytes without changing target_hash.
```

The explicit transport is the selected resolution of R2-1; no default-only
exemption from ModelInput binding is introduced. The versioned C interface
and publication schemas must include this contract before claiming 0.10
consumer support. It defines an estimate of a selected device invocation;
in a mixed fat object it does not make native main an ISA entry or supply
a general host-memory-by-reference ABI.

### Corresponding §12.3 insertion (proposed normative text)

A region MAY carry `model_estimates` as specified in §8.5. Those reports
are separate, explicitly identified accounting views. They MUST NOT be
added to the region's required §8.2 scheduled-leaf resources, charged again
as parent-plus-child costs, or substituted for the region's logical error
or fault-rate obligations. An invocation's selected QEC distance, hardware binding and every other
operational dependency affect target_hash; analytical non-operational
algorithm inputs and hierarchy reports affect certificate bytes, and
objective ModelInputs additionally affect schedule_hash. Physical failure charges and all
physical-model assumptions remain separate from epsilon and correctness
claims. No model output changes the object's instruction semantics.

## Fat-object applicability

Incorporate [the shared scoping statement](../2026-11-02-rev2/fat-object-scope.md#citable-scoping-statement).
Append to §12.3, in the new version:

```text
In a mixed fat object, model_estimates attach to the certificate of the
identified embedded/linked device ISA object and selected device-root
closure. The containing certificate's object_hash and closure_hash name
that device object and root, not the enclosing native binary. The fat
inventory associates each device object/root with its certificate and
target-bound reports; multiple roots retain independent contexts and
objective inputs. Native main, argv/envp and host-only libc remain native
and need no device resource report or certificate record. Native
comparison binds the corresponding materialised outlined-region/callee
closure and recorded configuration. This report asserts no whole-native-
program resource total. Budgets, handles, tapes and host memory follow
the device scope and explicit remaining launch obligations in the shared
statement; this extension implements no host shim.
```

Example: native main performs host-only work then calls marked module M
through a device CC wrapper. M's object/root certificate carries its
surface:algorithm report. Main and host-only libc acquire no model_estimates;
a second device root obtains its own context/input/certificate binding.
General host-memory-by-reference launch mapping remains explicit
bennett-4ht contract work, not an assumption supplied by this report.

## Worked serialized import

This is the **complete** `imports.surface` entry, not a complete target
or an accepted vendor fixture. It is pretty-printed for reading; the complete target is canonicalized
with RFC 8785 before identity calculation. Its preserved source is a small illustrative
formula JSON, with explicit normalized AST. It is not an Azure document
and no vendor adapter was run. The earlier fd0 example's formulas are
retained: d=5, tau=2 ns, p=1/1000, pth=1/10. A code with even distances
would use another declared parity/domain, not change generic validation.

Required target context: a native gate at `gates[0]` has `cost.time:0`
(the explicit binding overrides this provenance value) and `epsilon:0`.
Declare `time` with dimension `{s:"1"}`, scale `"1"`;
`model_cycle` (kind model, seconds); `model_physical_ratio` (kind model,
physical_qubit/logical_qubit); and `risk_charge` (kind count, dimensionless),
all with the metadata above. Retain normal mandatory logical occupancy
and peak declarations. Model hierarchy pool `["surface","data"]` is physical;
it does not replace the logical register ledger or class capacity.

<!-- import-example -->
```json
{
  "map": {
    "cycle": [
      "model_cycle",
      1e-09
    ],
    "physical": [
      "model_physical_ratio",
      1
    ],
    "risk": [
      "risk_charge",
      1
    ]
  },
  "model": {
    "assumptions": [
      "Illustrative QEC formulas; no physical independence assertion."
    ],
    "bindings": [
      {
        "factor": "1/1000000000",
        "path": "/gates/0/cost/time",
        "places": "0",
        "quantity": "cycle",
        "rounding": "exact",
        "value": "3/100000000"
      }
    ],
    "nodes": {
      "algorithm": {
        "child": "cycle",
        "count": {
          "param": "N"
        },
        "kind": "repeat"
      },
      "cycle": {
        "counts": {
          "risk_charge": {
            "quantity": "risk"
          }
        },
        "duration": {
          "quantity": "cycle"
        },
        "intervals": [
          {
            "amount": {
              "args": [
                {
                  "quantity": "physical"
                },
                {
                  "lit": "1",
                  "unit": "logical"
                }
              ],
              "op": "*"
            },
            "end": {
              "quantity": "cycle"
            },
            "pool": "data",
            "start": {
              "lit": "0",
              "unit": "ns"
            },
            "unit": "physical"
          }
        ],
        "kind": "leaf",
        "shared_uses": []
      }
    },
    "parameters": {
      "N": {
        "domain": {
          "max": null,
          "min": "0",
          "parity": "any"
        },
        "role": "algorithm",
        "type": "integer",
        "unit": "one",
        "value": null
      },
      "d": {
        "domain": {
          "max": null,
          "min": "1",
          "parity": "odd"
        },
        "role": "code_distance",
        "type": "integer",
        "unit": "one",
        "value": "5"
      },
      "p": {
        "domain": {
          "max": "1",
          "min": "0",
          "parity": "any"
        },
        "role": "hardware",
        "type": "real",
        "unit": "one",
        "value": "1/1000"
      },
      "pth": {
        "domain": {
          "max": "1",
          "min": "0",
          "parity": "any"
        },
        "role": "hardware",
        "type": "real",
        "unit": "one",
        "value": "1/10"
      },
      "tau": {
        "domain": {
          "max": null,
          "min": "0",
          "parity": "any"
        },
        "role": "hardware",
        "type": "real",
        "unit": "ns",
        "value": "2"
      }
    },
    "quantities": {
      "cycle": {
        "expr": {
          "args": [
            {
              "args": [
                "3",
                {
                  "param": "tau"
                }
              ],
              "op": "*"
            },
            {
              "param": "d"
            }
          ],
          "op": "*"
        },
        "role": "duration",
        "unit": "ns"
      },
      "physical": {
        "expr": {
          "args": [
            {
              "lit": "2",
              "unit": "ratio"
            },
            {
              "args": [
                {
                  "param": "d"
                },
                "2"
              ],
              "op": "pow"
            }
          ],
          "op": "*"
        },
        "role": "scalar",
        "unit": "ratio"
      },
      "risk": {
        "expr": {
          "args": [
            "1/10",
            {
              "args": [
                {
                  "args": [
                    {
                      "param": "p"
                    },
                    {
                      "param": "pth"
                    }
                  ],
                  "op": "/"
                },
                {
                  "args": [
                    {
                      "args": [
                        {
                          "param": "d"
                        },
                        "1"
                      ],
                      "op": "+"
                    },
                    "2"
                  ],
                  "op": "/"
                }
              ],
              "op": "pow"
            }
          ],
          "op": "*"
        },
        "role": "risk",
        "unit": "one"
      }
    },
    "schema": "bennett.import-model/1",
    "source": {
      "bytes": "7b226379636c65223a22332a7461752a64222c22706879736963616c223a22322a645e32222c227269736b223a22302e312a28702f707468295e2828642b31292f3229227d",
      "format": "bennett.illustrative-qec",
      "media_type": "application/json",
      "sha256": "426daeed30fce3fa03234faff9d8ea543005c4681917f126b8dbaca6508c9be5",
      "version": "1"
    },
    "units": {
      "logical": {
        "dimension": {
          "logical_qubit": "1"
        },
        "scale": "1"
      },
      "ns": {
        "dimension": {
          "s": "1"
        },
        "scale": "1/1000000000"
      },
      "one": {
        "dimension": {},
        "scale": "1"
      },
      "physical": {
        "dimension": {
          "physical_qubit": "1"
        },
        "scale": "1"
      },
      "ratio": {
        "dimension": {
          "logical_qubit": "-1",
          "physical_qubit": "1"
        },
        "scale": "1"
      }
    }
  },
  "version": "1"
}
```

For a report bound to the referenced node `surface:algorithm`, bind N=3 in
`Report.models.surface.parameters`; retain every hardware/code-distance
value from the target, and set `shared:[]`. This changes the report's bytes,
not the target. N left null yields a symbolic repeat with duration
`N*30 ns`, count charge `N/10^7`, and occupancy `N*1500 physical-qubit·ns`.
Its peak is piecewise: 0 for N=0, 50 for positive N. Do not simplify it
to 50 without retaining the N>0 premise. A fixed distance selection d=3
instead creates new target bytes and requires recomputing `Binding.value`
as `9/500000000` seconds; an old 30 ns resolved value must reject.

| Bound instance / composition | Duration | Physical peak | Physical occupancy | Additive risk charge |
|---|---:|---:|---:|---:|
| One cycle, d=5 | 30 ns | 50 | 1500 qubit·ns | 1/10^7 |
| Three sequential cycles, d=5 | 90 ns | 50 | 4500 qubit·ns | 3/10^7 |
| Three independent parallel cycles, d=5 | 30 ns | 150 | 4500 qubit·ns | 3/10^7 |
| Three sequential cycles, d=3 | 54 ns | 18 | 972 qubit·ns | 3/10^5 |
| Zero repetitions | 0 | 0 | 0 | 0 |

The complete entry above converts cycle 30 ns to `3/100000000` seconds
using factor `1/1000000000`. Its physical quantity is 50
physical_qubit/logical_qubit, not 50 physical qubits until multiplied by
one logical qubit in the leaf interval. The risk formula is an illustrative
external physical-model assumption. Even when its risk is positive, the
logical gate's exact `epsilon:0` stays 0, and any checked oracle fault rate
is independently obtained from F_B and its declared domain.

For a shared-factory variant remove its private physical interval, add
`shared_uses:[{id:"factory0",slots:"1"}]` to each factory-using leaf, and
declare one typed shared reservation in the report:

```json
{"id":"factory0","model":"surface","pool":"factory","unit":"physical","start":{"lit":"0","unit":"ns"},"end":{"lit":"90","unit":"ns"},"amount":{"lit":"50","unit":"physical"},"slots":"1"}
```

Three sequential 30 ns uses fit that reservation: peak 50 and occupancy
4500 physical-qubit·ns, with no threefold factory space charge. Three
parallel uses of a one-slot factory are infeasible. A model that actually
supplies a three-slot factory may reserve 50 physical qubits for 30 ns
and assert capacity 3 as an external-model assumption; then peak 50 and
occupancy 1500 physical-qubit·ns are the checked **accounting**, not a proof
that such hardware exists. The private-data and factory pool names remain
distinct. The source and normalized model hashes are recomputed
by the read-only witnesses; they are fixture identities, not published pins.

## Conformance vectors

These are acceptance obligations for the proposed format. “Error” below
means model/report validation or requested-schedule failure as specified,
never a new source-program trap or quantum oracle fault.

| Vector | Required verdict / result |
|---|---|
| Serialized example, d=5/N=3 | Valid import; 30 ns binding; sequential totals above. |
| d=3 with updated resolved value and hash | 18 ns/cycle, 18 physical/logical, risk 1/10^5. |
| Change d without updating Binding.value | Error at stale resolved value, before concrete scheduling. |
| d=4 under this model's declared odd domain; d=0 | Domain error. Another model declaring even distance with appropriate formulas remains legal. |
| Null N; N=0; N=3 | Symbolic repeat / empty composition / three copies, respectively. |
| Null hardware parameter used by a binding | Valid symbolic template; incomplete concrete schedule, naming that parameter; unrelated object execution unaffected. |
| Forward quantity reference; quantity/invoke cycle even under repeat 0 | Forward reference valid; either cycle error. |
| Division by zero; negative root; nonintegral pow exponent; zero^zero | Exact expression error. Integer negative powers such as 2^−3=1/8 valid. |
| sqrt(9/4); sqrt(2) | Exact 3/2; exact algebraic expression or verified outward enclosure. At 3 places sqrt(2) is enclosed by [1.414,1.415]. |
| Exact unit conversion factor `"1/3"` | Preserve the rational factor without rounding or a JSON binary64 restriction. |
| 1/3 with upper/lower at 3 places | 0.334/0.333; exact rational mode retains 1/3. |
| Add time and dimensionless risk; bind physical/logical ratio into time | Unit error, no heuristic unit/name conversion. |
| Unknown target path; path into epsilon; duplicate path; bad escaping | Binding error, before any target realization is used. |
| Source byte/hash mismatch; same name with another source version | Mismatch error; distinct identity, respectively. |
| Missing mapped quantity; unaligned quantity with newly declared model resource | Missing output error; valid preserved named resource, respectively. |
| Two quantities mapped to one aligned resource | Preserve both quantity-keyed displays; charge only the explicitly composed counts. |
| Unknown expression field / `var:eps` / accuracy bucket | Invalid normalized expression, never a model epsilon binding. |
| Unsupported source expression at a retained external location | Unchecked report with complete source/obligation; no invented value or algorithm rejection. |
| Three independent sequential/parallel cycles | Same count/occupancy, different makespan and peak as above. |
| Duplicate occurrence of one DAG child | Counts and private demand multiply; DAG storage sharing does not share a physical instance. |
| Shared factory sequence / parallel with one slot | One factory charged once / infeasible simultaneous use; serialized alternative remains legal. |
| Shared interval outside root time or not covering use | Error at reservation/use. Touching intervals have no overlap. |
| Invoke 10 ns into a non-operational algorithm parameter t in microseconds, report default 1 | Local t=1/100; leaf contributes 1/100000000 seconds; the report-level quantity display retains 1 microsecond. |
| Launch estimate with N=3 / N=1 ModelInput, no matching schedule | Default schedule binds supplied input; model duration 9/100000000 / 3/100000000 seconds; distinct schedule hashes. |
| Launch estimate missing required input / malformed input | incomplete-model-objective / validation error before returning an estimate, never an invented default. |
| Embedded N=1 with launch-request N=3 / matching N=3 | Inapplicable: default with N=3 / eligible only when all other bindings also match. |
| Cross-model symbolic invoke of an algorithm argument | Convert dimensions/units, retain caller dependency, qualify identities; no hardware override. |
| Report/certificate with wrong target, context or model hash | Reject the asserted report; no first-context or old-hash cache fallback. |
| Positive physical risk with exact logical gates | Risk output/charge remains nonzero; epsilon and logical fault claims unchanged. |
| Complete selector + complete ModelInput + concrete dependencies | Checked scalar under the ordinary objective rules. |
| Complete selector + well-formed ModelInput with free non-operational dependent parameters | Symbolic unresolved objective, with no invented value. |
| Missing required model_outputs selector | Validation error at objective.model_outputs.<resource>; not a symbolic input. |
| Missing required ModelInput | Explicit incomplete-model-objective diagnostic; no completed concrete optimization. |
| Root/model parameters/shared reservations changed in a certifying report | Reject if they differ from its schedule-bound ModelInput; no report-selected objective. |
| Algorithm parameter N operationally binds time, target N=1; report/invoke N=2 | Reject the changed operational value. A newly resolved N=2 target must have value 2 and a new hash. |
| Standalone X reports with 0 and 1 inherited controls | Explicit subjects differ; 1-second and 2-second estimates cannot be interchanged. |
| 90 ns one-slot shared factory, 50 versus 100 qubits, same selector | Legal inputs give peaks 50/100 and occupancy 9/2000000 versus 9/1000000 physical-qubit seconds, with distinct schedule hashes. |

The earlier executable ../2026-11-02-rev2/check_rev2.py covers the fixture's scalar arithmetic and
unit conversions; parameter/formula negative cases; forward reference and
zero-multiplied cycle; exact rational roots/powers and rational enclosure
inequalities; sequence/parallel/repeat/shared-accounting examples; hashes;
the seeded input-identity/freeze witnesses, versioned catalog hashes,
and document structure. Cross-model invokes, actual operational target
resolution, source adapter translation, generic algebraic evaluation,
context validation and the remaining consumer acceptance vectors remain **proposed**.
A small rational example checker is not an implementation of this format.

## Objective selector and input witness

Declare factory_peak as a model resource with physical_qubit dimension
and scale 1. Use the shared-factory variant specified above (its changed
nodes require its own recomputed model_hash), N=3, and this objective:

```json
{"weighted":{"factory_peak":1},"model_outputs":{"factory_peak":{"model":"surface","node":"algorithm","metric":"peak","pool":"[\"surface\",\"factory\"]"}}}
```

Its schedule.bindings.model_inputs.factory_peak contains root
`{model:"surface",node:"algorithm"}`, complete model/parameter bindings,
and the explicit shared reservation. With one slot over [0,90 ns),
reserving 50 or 100 physical qubits gives peak 50 or 100, and occupancy
9/2000000 or 9/1000000 physical-qubit seconds. Both inputs are legal and
have the same target/selector, but distinct schedule hashes. A report
for the 100-qubit reservation cannot certify the 50-qubit schedule input.
No external report selection supplies the reservation implicitly.

For the selector-validation vector, `{"weighted":{"factory_peak":1}}`
is malformed: objective.model_outputs.factory_peak is missing. The
complete selector above with a well-formed input retaining free N is
symbolic; bind N and compatible reservation endpoints to obtain a concrete
scalar. Missing ModelInput gives the separate incomplete-input diagnostic.
These are model/scheduling outcomes, never ISA fault codes. The test uses
a finite schematic schedule envelope to witness identity sensitivity;
publication still needs complete bound production fixtures.

## Consumer impact, release and what remains for 0.10

For 0.9 every fully bound invocation retains its §10.1 estimate of the
complete padded realisation, exact mandatory rows and checked certificate,
including unmodified SQLite at N=2^20. Materialise fully resolved operational
fields into ordinary scalar 0.9 targets, retaining original source, parameter
bindings and hierarchy as external provenance. Equivalent accounting need
not materialise every gate. estimate_nresources continues to enumerate only
scheduled count/time/occupancy/peak rows; new model-only resources use
model_estimates and add no scheduled scalar row. An unused model output
still remains visible in the model report. Preserve all promised algorithm scope. This is a
compatibility path, not completion of symbolic import support. Do not
pretend a new JSON field is already admitted by 0.9's closed schema. The
reference interpreter's current declared 0.8 surface also does not gain
0.10 admission through a documentation proposal.

For 0.10, target importers parse the pinned source version, preserve raw
bytes, normalize formulas/units/domains, and supply resolved bindings.
The scheduler selects distance using classical data, creates a distinct
resolved target, and evaluates model objectives without materializing all
gates. The estimator retains symbolic hierarchies and reports intervals,
shared factories and named quantities. The VM/circuit executors preserve
the ordinary logical machine semantics and use the resolved costs;
physical simulation is not inferred from a resource-risk output. The
independent checker verifies translation where supported, target/report
identity, arithmetic, accounting and truthful obligation labels. The
conformance harness must run all format vectors with separate producers
and checker; a consumer should not share a vendor importer as its sole
verification oracle across a published contract boundary.

No reference catalog recipe body, source instruction syntax or published
0.9 envelope is edited by this proposal. Under the normal full-version 0.10 publication, affected
semantic envelopes and source hashes change because their version changes;
do not promise a global no-repin migration. Target hashes change for new
models/resolved distances; target-bound schedules and certificates must
be re-bound and checked. Algorithms' estimate parameters and hierarchy
change the report/certificate bytes, independently of source identity.
Normal full-version 0.10 publication MUST also republish the default ref
catalog with isa="0.10" and version="0.10", update its §11.1 envelope and
§17 item 7 default binding, and recompute dependent schedule/certificate
identities and pins. All 219 recipe bodies may remain unchanged. The
metadata-only in-memory transformation gives:

```text
ref@0.9:  5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197
ref@0.10: 83cc9c177bad054bd7af35dc1892645d869b9e4c0b9c968f35b8783ce2b54c42
```

These are versioned envelope hashes, not raw-file SHA-256. The 0.10
calculation uses the published JCS routine, changing exactly the catalog's
isa/version and envelope's isa/version while preserving recipes. Published
0.9 artifacts stay unchanged; this job writes no catalog and re-pins no
artifact. Unchanged recipes do not imply an unchanged versioned identity.
Non-operational objective ModelInputs change schedule_hash; every
model report remains bound to its specific device object/root in the
mixed-fat-object inventory, not a native-program aggregate.

Remaining 0.10 work is concrete: council acceptance of these new
encodings and unit/accounting rules; machine-readable target/certificate
schemas and vectors; source-format/version adapters including retained
external expressions; an independent translation checker or versioned
checkable witness mechanism for each such expression; scalable symbolic
DAG evaluation, distance-search implementation and a versioned checkable witness for
optimality claims when requested; operational-resolution and context
validation in consumers; compatibility and publication tooling. Routing,
physical pulse/noise simulation and a general proof that vendor QEC models
predict hardware are separate mechanics/assumptions, not hidden obligations
this arithmetic proposal claims to solve. It supplies no automatic
independence law for physical failures and no physical probability to
logical-norm conversion. A user may import an explicit, separately checked
risk-composition formula as model data; no such capability is prohibited.

Keep **b-isa-spec-fd0** open for that contract/adapter work and
**b-targets-gyp** open at its owning repository until the promised complete
path exists. Preserving an unchecked external obligation is honest interim
reporting, not a non-narrowing substitute for implementing it. Neither bead
was mutated by this notes-only job. The exact new mechanism is described
above; no new cross-repo issue is necessary to name the same blocker.

## Launch/default-input concrete witness

Use the complete surface import above without changing its model or target
identity; N is a non-operational algorithm parameter. Select this objective:

```json
{"weighted":{"model_cycle":1},"model_outputs":{"model_cycle":{"model":"surface","node":"algorithm","metric":"duration"}}}
```

The full supplied N=3 map (all parameters in their declared units) is:

<!-- launch-input-example -->
```json
{"model_cycle":{"root":{"model":"surface","node":"algorithm"},"models":{"surface":{"model_hash":"c69312a9d3fc53728a6554b44bae48a9fab7eaefbcca3651c75ad9a0128e022f","parameters":{"N":"3","d":"5","p":"1/1000","pth":"1/10","tau":"2"}}},"shared":[]}}
```

The N=1 request changes only parameters.N to "1". Both retain copied
signature arguments, budget, target, root, variant and inherited controls.
The model duration is respectively 9/100000000 and 3/100000000 seconds.
The default schedule includes this complete map even with entries:[];
its schedule_hash changes. Supplying an embedded N=1 schedule to N=3 is a
mismatch: the N=3 default is selected. An embedded N=3 input with
different in-memory object key ordering matches after JCS; a changed shared reservation
or model parameter does not. Missing model_cycle input yields
incomplete-model-objective before any estimate, and a wrong model hash
is a validation error. No model defaults or earlier report can fill it.

[check_rev4.py](check_rev4.py) extracts the serialized import and map from
this document. It computes source/model identities and exact typed formula
values, checks d=3/d=5 and the source-unit coefficient conversion, and
exercises supplied, missing, malformed, free, copied-buffer and conflicting-
embedded input cases. It evaluates the bound hierarchy by explicit finite
leaf expansion and separately checks N*30 ns, risk, peak and occupancy.
It computes SHA-256 of canonical **schedule fragments** containing the map
to demonstrate binding sensitivity. These finite fragments are not full
production target/schedule/certificate fixtures or published identities.
The test does not claim that a production 0.10 launch ABI exists.

The prior accepted model's source/model hashes and both versioned catalog
identities are rechecked, retaining all 219 recipe bodies. The retained round-2 finite
checks are also run read-only, with their existing limited coverage. No
claim of implementation of generic algebraic evaluation, a vendor adapter,
a full schedule solver, operational resolution, cross-model checking or
a mixed-launch shim is made. Complete production target/schedule/Report
fixtures, including wrong-context rejection, remain required for publication.

## Verification and evidence boundary

Run the focused checks from any working directory:

```sh
bash /home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/notes/2026-11-02-rev4/run_checks.sh
```

The script builds the reference interpreter read-only with CARGO_TARGET_DIR
under .tmp/sol-rev4, links [oracle_witness.rs](oracle_witness.rs) there,
and runs both new contract witnesses plus the retained finite checks.
Build/link processes are bounded at 6 GiB, finite Python/interpreter
replay at 512 MiB, with timeouts and headless environment variables.
No full repository/sibling gate or git command is run. Exact observed
results are recorded in [verification.md](verification.md).

The interpreter witness verifies the unchanged 0.9 logical oracle and
literal machine reversal; it does not accept or execute the proposed 0.10
launch API. The launch/default-input test is a finite executable contract
model. These are distinct evidence claims.

General model JCS uses RFC 8785, including UTF-16 key ordering: U+10000
sorts before U+E000. The illustrative model contains strings/ASCII keys;
the tests also check the Unicode distinction. Its map's 1e-09 number is
outside model_hash, which hashes only model.

```text
raw source: 426daeed30fce3fa03234faff9d8ea543005c4681917f126b8dbaca6508c9be5
model:      c69312a9d3fc53728a6554b44bae48a9fab7eaefbcca3651c75ad9a0128e022f
```

All changes remain proposals. Beads b-isa-spec-fd0, b-targets-gyp and
bennett-4ht remain open for acceptance, publication and implementation;
no tracker mutation, spec/catalog/header edit or sibling-revision edit
is made here. The runner handles commits. The only delivered changes are
inside this revision directory, with job progress/evidence under .tmp/sol-rev4.

---

## Dossier part: pe1 (run derive3-pe1-2026-11-02; accepted by sol, codex in round 1; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-02-derive3/b-isa-spec-pe1.md)

# b-isa-spec-pe1 — K13's extra borrowed bit

Council proposal; published text and fixtures are unchanged. References:
[ISA 0.9](../../../spec/Bennett-ISA-Spec-0.9.md) §§4.2–4.3, 5.6,
12.1 “CLAIM-REPLAY witness”, 12.2 “Component resolution (K69/K70)”.

## Exact defect and North Star scope

The §12.1 subject is exactly the two-row oracle `r = lift.add x a;
lift.retval r`, with no inherited controls and an unused interface
region. The printed tuples nevertheless contain `borrowed:["1"]`,
the widths include `borrowed:[1]`, and the prose counts a 25-bit D and
coverage `1/33554432`. The lifted opcode set in §4.2 supplies no qborrow
instruction. This subject has no checked dirty-bundle lifetime.
§12.2 K70 expressly rejects a borrowed position beyond the checked
borrow requirement. The example cannot pass the rule it illustrates.

This is an inconsistent normative example, **not a missing borrow
capability** or a reason to relax K70. §4.3/§5.6 already supplies dirty
allocation and borrowed-system preservation where applicable. North
Star §§3.1, 4.2, 5.1 remains reachable, including dirty ancillae and
entanglement with an external reference. Correct the example rather
than adding a fictitious oracle input component.

## Alternatives and concrete witnesses

For x=1, a=2, target=2, fault=3, cells=[2,1], B=2, the two rows return
payload 3 and fault code 0. The resulting complete tuple is
`bundles:["1","1","3"], borrowed:[], regions:[["2","1"]]`.
The full basis domain has 2+2+4+16 = 24 bits. A singleton declared
domain, sampled four times with replacement, covers one of 2^24 full
tuples and remains evidence. Singleton ranges consume no random words.

Changing a to 1 changes target to 0. Reducing B to 1 changes the payload
to 0 and the final fault word to 3 XOR 1 = 2. An identity expected row
fails. Dropping the borrowed coordinate changes none of these results.
An invented one-bit coordinate must still reject under K70, even if
the table preserves it perfectly or calls it the same name as a real
interface bundle.

| Alternative | Assessment |
|---|---|
| Remove the extra borrowed coordinate and adjust D/fraction | Repairs the example without changing any machine/domain rule. Recommended. |
| Replace the subject by a checked borrowing action wrapper | Possible new example, but needs its actual body, frame, lifetimes and new domains; the printed two-row oracle cannot stand in for it. |
| Invent oracle borrowed inputs or infer them from unused labels | Changes the oracle ABI and breaks K70 positional resolution; unjustified. |
| Count a lift.perm_call callee's internal scratch as this oracle's borrowed interface | Needs a separate lifetime/tuple contract; no such call exists in this witness. |

## Recommended exact spec diff

Within the single §12.1 CLAIM-REPLAY witness JSON block, replace **all
six** tuple occurrences of `"borrowed":["1"]` by `"borrowed":[]`,
and make these additional replacements:

```diff
-  "widths":{"bundles":[2,2,4],"borrowed":[1],"regions":[[8,8]]},
+  "widths":{"bundles":[2,2,4],"borrowed":[],"regions":[[8,8]]},
-  "sample_count":4,"distinct_samples":1,"covered_fraction":"1/33554432","verdict":"evidence"
+  "sample_count":4,"distinct_samples":1,"covered_fraction":"1/16777216","verdict":"evidence"
```

Replace the indicated prose immediately below that block:

```diff
-with a preserved one-bit dirty bundle and an unused two-cell,
-eight-bit `in` interface region; no inherited controls.
+with an unused two-cell, eight-bit `in` interface region; no borrowed
+lifetimes and no inherited controls.
-full 25-bit D (2+2+4+1+16 bits).
+full 24-bit D (2+2+4+16 bits).
-words and cover one of 33554432 full tuples.
+words and cover one of 16777216 full tuples.
```

Append to that witness paragraph:

```text
The empty borrowed array is required here: the two-row oracle has no
checked borrow lifetime. Adding a borrowed coordinate to this witness
rejects under K70; unchanged borrowed contents alone do not establish
that a lifetime exists.
```

The replacements operate on the exact phrases across line wrapping;
do not change the separate general tuple encoding, sampler, layout,
arguments, target/fault widths or K70 rule.

## Hashes, catalog and consumers

The witness deliberately supplies no bound object/closure hashes, so
there are no printed subject digests to recompute. No source instruction,
interface or ref catalog changes. Any concrete certificate/table fixture
based on the invalid example must change its tuple/domain bytes and
coverage report; a certificate digest consequently changes. Consumers
following K70 already reject the old example. Do not change their
component resolver or call the repair a proof over dirty inputs.

## Conformance vectors and actual verification

The read-only replay suite's `tests.test_replay.K13Witness` has four
focused tests using the repaired empty-borrowed relation, including the
changed argument, short budget, wrong row and missing-cell cases.
Ran it together with `QinplaceCoverage` using the bounded command in
[INDEX](INDEX.md): all 12 tests passed, exit 0. The replay fixture uses
ptr_width=32 rather than the printed legal 2-bit layout, so this run
checks the relation/domain behavior, not literal byte reproduction of
that layout. It is also an exhaustive singleton-slice test, not the
printed four-draw sampled packet. The finite INDEX checks independently
check the bit count, all six tuple repairs and sampling calculation.

For acceptance publish a complete bound certificate for the repaired
2-bit-layout oracle, with the exact four-draw sampler and all region
cells. Expect evidence `1/16777216`; reject the extra borrowed position,
unchanged-argument/budget rebinding, identity row and omitted cell.
Retain a separate genuine qborrow action with an entangled external
reference to test dirty preservation; it must not be folded into this
oracle's D. A small example fix does not discharge suite C's full-D T3.

## K entry and publication route

Recommend a **0.9 K13 witness erratum**, not a new oracle ABI or 0.10
deferral. Proposed decision row: `K13 erratum | §12.1 | remove nonexistent
borrowed coordinate; D=2^24, coverage=1/16777216 | pe1 | example repair`.
Council assigns any new ledger number; this proposal reserves none.
The semantic rule already belongs to accepted K70. Keep pe1 open until
the editor and conformance owners publish the repair.

## Mixed fat object

Apply [fat-object-scope.md](../2026-11-02-rev2/fat-object-scope.md) and
North Star §§2, 3.3, 4.4. This tuple belongs to one embedded device
subject and its selected root. A native host or another marked module
does not contribute a borrowed coordinate, interface cell or certificate
record to this subject. No container, launch, budget, handle or tape
change is needed; the shared note's explicit mixed-launch association
work remains. The native binary need not become an oracle to repair K13.

---

## Dossier part: 2qc (run derive3-2qc-2026-11-02; accepted by sol, codex in round 1; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-02-derive3/b-isa-spec-2qc.md)

# b-isa-spec-2qc — checker duty for qinplace coverage

Council proposal. References: [ISA 0.9](../../../spec/Bennett-ISA-Spec-0.9.md)
§4.5 K4, §§9.2–9.3, §12.1 “Invocation contexts”, §12.3 “Invocation
binding (K13)”, §16.3 example 7; related
[0jq owner proposal](../2026-11-02-pass2/b-isa-spec-0jq.md).

## Exact defect and North Star scope

§4.5 already requires an inverse-pair entry in the certificate record
of the region whose body contains qinplace. An unordered pair of exact
g/ginv closure hashes covers either orientation. Coverage also requires
entry.budget ≤ tk componentwise, exact token-argument tuples and
membership of the other arguments in the claim's args domain. The
executor must preflight every transitively executed qinplace before
any effect of a CC/R region call, or trap/fault 4.

§12.1 specifies verification of an entry's claim, and §12.3 specifies
binding resolution, but neither explicitly turns **coverage of sites**
into a checker duty. Validating a supplied inverse-pair proof and
checking that every applicable instruction has one are different tasks.
The request exposes this checker/executor responsibility ambiguity,
not a missing executor trap, inverse algorithm or proof owner. Resolving
all three questions needs static pair presence, bound applicability and
nested-context scope, rather than just “check inverse_pairs”.

North Star §§3.1, 4.2, 5.1 promises checked in-place bijections and honest
proof/evidence labels. Requiring those existing obligations at certificate
acceptance preserves that promise. A standalone proof with unresolved
call parameters may remain useful; it must not be labeled executable
acceptance or be rejected merely for lacking a schedule it never claims.

## Alternatives and concrete witnesses

Use §16.3 example 7, owner `addya`, with qinplace G/GINV, token tk and
classical argument a. The entry proves both compositions on the full
x,y domain, minimum tuple [3,0,0,0], a in 0..3.

| Case | Proposed checker result |
|---|---|
| No entry, or only {G,G} for a {G,GINV} site | Reject missing owner-local pair. |
| tk=[3,0,0,0], a=1, valid full-domain claim | Covered. |
| tk=[9,0,0,0], same a | Covered by primary-token monotonicity. |
| tk=[2,0,0,0] | Reject applicability for that bound invocation. |
| a=3 but the claim covers only 0..2 | Reject applicability. |
| G/GINV swapped in the entry | Covered by the same two-composition proof. |
| Correct entry, no resolvable standalone invocation | Report coverage unestablished; no executable-acceptance conclusion. |

For nesting, outer calls inner twice; inner owns the qinplace. Its tk
actuals are 3 then 2. An entry with minimum 3 covers the first context
and misses the second, even if both have the same variant/control count
and outer's root budget is 9. An entry in outer's claims array cannot
replace inner's. If a qinplace forwards a token argument k, an entry's
arg_tokens.k=[3,0,0,0] does not cover k=[4,0,0,0], however large tk is.

| Alternative | Consequence |
|---|---|
| Executor-only coverage | Safe execution still traps, but a checker can advertise an unusable certificate; requires an explicit limited verdict. |
| Check pair presence and root only | Catches common errors, misses the second inner context above. |
| Check owner presence plus every bound context | Aligns checker acceptance and existing preflight; recommended. |
| Require a universal proof for all possible calls of every standalone record | Unnecessarily rejects useful invocation-scoped/parameter-uniform claims. |

## Recommended exact spec diff

Insert after §12.3 Invocation binding's paragraph ending “not a target
realisation”, before CLAIM-BINDING witness:

```text
Qinplace coverage checking. For every qinplace source site in a supplied
region record, the checker MUST require an inverse_pairs entry in that
owner region's record for the exact pair of resolved g/ginv closure
hashes, in either orientation, and MUST reject a missing pair or invalid
referenced claim. Resolve imported owner records and library claims by
§9.3; indices name claims in their owner record, never in an outer caller.

When a root invocation is bound by bindings.invocation (or by a
standalone claim whose subject is that root), the checker MUST apply
§4.5's complete
covering test at every reached qinplace site in that invocation and its
transitive invocation contexts, rejecting any uncovered site. With a
schedule, use §12.1's complete realised invocation tree, including
default-covered calls, iterations and source-adjoint/control contexts;
without a schedule, use the bound reference invocation tree. Resolve
the site's tk and args from that context, not the root's tuple reused
for all callees. A disabled coherent predicate does not remove an
entered instruction's obligation. Entry claims must be established by
their specified exhaustive or linked-library rule; sampled agreement
does not cover. Do not treat two private generated oracle calls as new
owners of the containing source site's entry.

A standalone record with an entry but no resolvable invocation may
retain its established standalone claims. The checker MUST report its
qinplace applicability as unestablished and MUST NOT conclude executable
acceptance from it. Universal applicability may instead be established
by a checked parameter-uniform argument covering every admitted call.
If a required invocation, linked body or context cannot be resolved or
checked, report that obligation unestablished; an implementation work
limit is not proof of absence or applicability. Malformed bindings and
missing required pairs still reject. No successful verdict may imply
that an unestablished obligation was discharged.

These checks do not remove the executor's §4.5 pre-effect trap/fault
requirement. A verified result may be reused only for the closure,
entry proof and invocation/domain it actually covers; closure equality
alone does not establish applicability at another token/args binding.
```

“Every source site” makes the existing carried-entry requirement explicit
even for a zero-iteration source loop. Context-dependent applicability
is tested only at reached sites. This separates static inventory from
call-dependent coverage; it does not require executing an unreachable
quantum branch as a classical branch or searching all possible CC inputs.
The driver/executor supplies the actual root binding before use.

## Hashes, catalog and consumers

No source envelope, public signature, ref catalog or instruction expansion
changes. Correcting a missing entry changes certificate bytes and any
certificate digest. Wrongly accepted executable packets may now reject
or become explicitly incomplete; this is a compatibility decision, not
an invisible checker patch. Composition must retain each owner's claims
and root-relative contexts; a cache keyed only by closure cannot cache
call coverage. VM, specialiser, producer and independent checker owners
need the same applicability vectors. Fault code 4 and pre-effect timing
are already normative and do not change.

## Conformance vectors and actual verification

Ran the existing independent replay's `QinplaceCoverage` (eight tests)
with K13Witness (four), using [INDEX](INDEX.md)'s bounded command: exit 0,
12 passed. These exercise absent/wrong pairs, swapped orientation,
larger/shorter tk, args range and unbound handling. They do not exercise
the proposed complete nested traversal. The replay explicitly reports
non-root applicability unchecked. Its verdict is not a newly ratified
contract. The published checker's `docs/checker.md` separately states
that verification-index shapes do not discharge qinplace applicability.

Acceptance adds the two-inner-context witness, default-covered and
adjoint calls, qloop 0 versus repeated visits, inherited coherent control,
outer-only entry rejection, imported owner/library records, exact token
argument mismatch and sampled-claim noncoverage. For the executor check
fault 4 occurs before any region effect and preserves the reversible
prefix. A valid structural-only standalone claim must survive with
coverage explicitly unestablished. The finite INDEX predicate checks
the binding distinctions, not a new complete certificate checker.

## K entry and publication route

Recommend an explicit **0.9 K checker-obligation repair**, coordinated
with 0jq, if council authorizes the existing repair track. Proposed row:
`K(new) | §§4.5,12.3 | QINPLACE-CHECKER-COVERAGE: owner-local pair
presence plus all bound transitive contexts; unbound applicability is
unestablished; executor preflight retained | 2qc,0jq | checker semantics`.
Reserve no numeric K identifier. Under the published semantic-version
rule this belongs in **0.10** unless the council explicitly authorizes
an in-version repair; see [INDEX](INDEX.md). Keep 2qc open for that
decision and consumer implementations.

## Mixed fat object

[fat-object-scope.md](../2026-11-02-rev2/fat-object-scope.md) applies (North
Star §§2, 3.3, 4.4). Coverage begins at each selected embedded device
root, context [], and uses its linked owner records. Two native calls to
that root can bind different tk/args; neither inherits coverage merely
from the other's certificate. Native main, host-only libc and other
device roots need no artificial region inventory. The container-to-root
association, launch budget/handle negotiation and tape/run association
remain the exact boundary changes named in the shared note. This proposal
checks device invocations without requiring whole-binary lowering.

---

## Dossier part: sqr (run derive3-sqr-2026-11-02; accepted by sol, codex in round 1; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-02-derive3/b-isa-spec-sqr.md)

# b-isa-spec-sqr — mcx controls named by a bundle

Council proposal, not an ISA implementation. References:
[ISA 0.9](../../../spec/Bennett-ISA-Spec-0.9.md) §§3.3 (indexed operands,
distinctness), 4.4 (gate forms), 11.1 (resolved gate wires), 16.2 (grammar).

## Exact defect and North Star scope

§4.4 writes `mcx (c_1..c_k) t` and “X on the target iff all controls
are |1>”. It does not say whether a NAME in that list must denote one
wire or may denote a wire[N] bundle. §3.3 defines bundles and indexed
operands, but supplies no gate-specific list expansion rule. §16.2's
parenthesized list admits bare NAME entries; it does not admit indexed
entries such as `(c[0], c[1])`. Thus the usual informal advice to list
those indices is not an existing grammar solution.

This is an **operand contract ambiguity**, not evidence that the abstract
machine lacks a many-controlled X gate. Explicit `ccx c[0] c[1] p` already
expresses the two-control case. North Star §§3.1, 4.2, 5.1 requires the
operation and interoperable interpretation, not this particular shorthand.
Either precisely defined expansion or a precisely stated scalar-only
syntax can preserve the machine capability. Expansion is recommended
because it preserves the admitted bundle spelling and needs no new list
grammar. Reading only the first bit has no defensible all-controls meaning.

## Alternatives and concrete witness

Read-only witness:
`../bennett-conformance/checker-replay/witnesses/mcx-bundle-control/`.
Its action has p,q:wire mut and c:wire[2] in, then:

```text
swap p q
mcx (c) p
```

With p=q=0, c=1 (bits c[0]=1,c[1]=0), expansion leaves p=0;
first-bit execution produces p=1. With c=3 expansion produces p=1.
The complete forward map is (p,q,c) -> (q XOR [c=3],p,c).
The adjoint applies the controlled X before the swap, restoring every
input. It is generally not the same source sequence run forward twice.

| Alternative | Meaning and cost |
|---|---|
| Flatten each bundle entry in increasing bit index | All named controls participate; k is the total wire count. Recommended. |
| Require every entry to be scalar | Legal alternative if explicitly published; bundles require another spelling/construction, and indexed list syntax would need a grammar amendment. |
| Broadcast independent X operations per control | XOR of controls, not conjunction; wrong at c=1 and c=3. |
| Inspect c[0] alone | Silently loses controls; wrong at c=1. |

## Recommended exact spec diff

Insert immediately after the forms sentence in §4.4:

```text
Each NAME entry of an mcx control list may denote wire or wire[N].
It contributes every wire of that bundle, in increasing bit index;
concatenate entries in written list order. The k in mcx(k) is the
number of resulting control wires, not the number of list entries.
The target denotes exactly one wire (a scalar name or indexed operand).
Apply §3.3's pairwise distinctness to the resulting control wires and
target before execution; overlapping or repeated entries reject as
ill-formed, never deduplicate them to repair an operand list. Existing
effective predicate-context rules still apply. The empty list has
zero explicit controls and applies X under the active predicate.
Flattening determines resolved primitive operands, gate cost and
realisation arity, but does not rewrite source identity or source points.
```

Append the normative witness:

```text
For c:wire[2], mcx (c) p has the same gate semantics as
ccx c[0] c[1] p: it changes p exactly for c=3, not c=1 or c=2.
mcx (c, c) p and a target c[0] with controls (c) are ill-formed.
```

No general §16.2 list-grammar change is required. This proposal does not
add indexed entries inside parenthesized lists; use the existing indexed
operands of ccx for the scalar two-bit comparison above. It also does
not legalise a multiwire target or change cx/ccx into bundle operations.

## Hashes, catalog and consumers

Retain the written bundle operand in source envelopes. Under an explicitly
authorized same-version repair, existing object/interface/closure hashes
are unchanged; the published witness binds object
`db3d3f92a79077074901449d83532f1a0d82ef1621bd833adb7ad14d1aedd467`
and action closure
`e38d5da64f9a0ae89a66243bcbe5a321cb807a5bbabf83952b63d3465dfab346`.
They identify bytes, not an implementation's formerly mistaken unitary.
Schedules that counted one control must be regenerated and certificates
rechecked; unchanged source hashes do not validate old execution caches.

The ref catalog's existing mcx wire-list recipes already operate on
resolved wires. Their bytes need no change: source adapters must supply
all flattened controls and k. If an adapter changes generated leaves,
update its expected leaf hashes and affected schedules, not `ref@0.9`
silently. K78 primitive identity uses the complete effective control set;
no new causal-matching exception is required. A 0.10 publication changes
version-prefixed envelopes and pins as described in [INDEX](INDEX.md).

## Conformance vectors and actual verification

The recorded older published-checker result rejects the witness table
because it flips p at c=1; the stored replay result proves all 16 inputs.
Re-ran the current replay CLI with `--max-elements 16`: exit 0,
claim proof, 16 elements, covered_fraction 1. Its separate unchecked
metadata obligations remain unchecked; this is only the relation claim.

Built the current reference interpreter read-only into the job target.
Its `check` on the **original** bundle object exits 1 with
`§3.3: c must name one wire`. It does not reproduce the older checker's
first-bit result. Current validation and action execution require scalar
list entries. That is evidence for the ambiguity, not proof that the
recommended expansion is implemented.

For an executable independent comparison, changed only a scratch copy
to `ccx c[0] c[1] p` and recomputed its declared interface hash. Reference
check/hash pass; object hash is
`c785ff3f310f968e2a26f68834e99ab892cf0d1bffe816cf26b17d45c33a65af`,
interface/closure hash
`f53238499e07824b6c62385c33426d4bc56bfaf900df61264ec65e0589061f39`.
All 16 forward and 16 adjoint basis cases pass the map above, with c
preserved. An initial attempt at `(c[0], c[1])` was rejected by the
current list grammar; it is not used as a passing witness. Reproduction
is in [INDEX](INDEX.md). No source interpreter or sibling fixture changed.

Acceptance adds bundle widths 1/2/3, mixed scalar/bundle entries, list
order, c=0/1/2/3, empty-list X, target/duplicate/control alias negatives,
active predicate and adjoint cases. Check exact +1 phase and a superposed
control entangled with a reference, full flattened arity/cost, source
hash stability and K78 matching against the equivalent scalar primitive.
Suite F must distinguish an operand rejection from a replay mismatch;
suite C/T6 checks the resulting unitary.

## K entry and publication route

Proposed row: `K(new) | §§3.3,4.4,11.1 | MCX-BUNDLE-CONTROLS: ordered
bundle expansion; distinctness and k over denoted wires; scalar target |
sqr | operand/expansion semantics`. Reserve no number. Recommend a
council-authorized 0.9 K repair only if the ambiguity-repair track is
explicitly approved; otherwise publish in **0.10** under the semantic
version rule. Do not silently extend accepted 0.9 syntax or claim all
current consumers already agree. The scalar-only alternative is a valid
decision if the council instead supplies its exact operand wording and
preserves the general many-control capability. Keep sqr open meanwhile.

## Mixed fat object

[fat-object-scope.md](../2026-11-02-rev2/fat-object-scope.md) and North Star
§§2, 3.3, 4.4 apply. Flatten within each marked device module's actual
wire bindings; wires and certificate domains do not include native host
code. Gate arity and budgets belong to that device invocation. Shared
device helpers may be linked under several roots without making native
main or host-only libc certificate regions. No launch, opaque-handle or
tape format changes follow from this operand rule. The shared note's
container/root and mixed-launch boundary additions remain required.

---

## Dossier part: 4yg.1 (run derive3-bennett-arith-4yg.1-2026-11-02; accepted by sol, codex in round 1; amends the Bennett dialect spec (../bennett-dialect-spec/spec/); source note bennett-isa-spec/docs/notes/2026-11-02-derive3/bennett-arith-4yg.1.md)

# bennett-arith-4yg.1 — PPC parity where the low component becomes zero

Council proposal, not a published amendment. Owner: dialect specification;
implementation follow-up: `bennett-arith-4yg`. References are to maintained
[dialect 0.2.12](../../../../bennett-dialect-spec/spec/Bennett-Dialect-Spec.md)
§§13.1, 13.3–13.5 and the corresponding
[0.3 draft](../../../../bennett-dialect-spec/spec/Bennett-Dialect-Spec-0.3-draft.md).

## Exact defect and North Star scope

§13.1, “PPCDoubleDouble priority and rounding”, defines canonical finite
pairs by h = binary64 roundTiesToEven(h+l), with l the exact residual.
It then requires the nearest canonical sum, “with ties to the even
low-component significand, using the high significand when the low
component is zero”. Adjacent canonical candidates can both be odd under
that rule. Thus a required result is not uniquely specified for valid
FMA and incoming IEEE conversion inputs. This is a numerical contract
defect, rather than an absent softfloat feature or an ISA operand defect.

§13.1 already determines the flags: only final rounding counts; underflow
requires a tiny rounded total and inexactness. The observed FMA flags 0
and conversion flags 24 are implementation defects independently of the
tie decision. They must become 16 whichever nearest candidate is chosen.

North Star §§3.2, 5.1 requires deterministic materialised numerical
semantics and independent comparison. The missing tie decision obstructs
that contract; it is not a missing North Star machine capability. All
seven formats, full input domains, conversions, FMA and the demo ladder
remain required. §13.3 expressly forbids treating missing numerical
implementation as a supported-format restriction.

## Alternatives and concrete witnesses

Let u = 2^-1074, h = 1+2^-52 (binary64 `3ff0000000000001`). The
canonical inputs a=(h,u), b=(1/2,+0), c=(h/2,+0) have exact fused result
h+u/2. Its adjacent canonical results are L=(h,+0), U=(h,u).
Every finite binary64, hence every pair sum, is an integer multiple of u;
their separation u proves adjacency, and both distances are u/2.
L's published high fallback is odd; U's low significand is 1, also odd.

For conversion, take H with binary64 bits `0030000000000001`.
V=H+u/2 is exactly binary128 bits `3c030000000000001200000000000000`.
The adjacent pairs (H,+0), (H,u) have the same odd/odd problem. H is
normal, so this conversion cannot raise underflow merely because its
unrepresentable residual is tiny. These are two different operation paths
to the same decision, not a speculative rare input.

| Alternative | Consequence |
|---|---|
| Compare low significands for both candidates if either low is nonzero; use high only if both are zero | Zero has even low parity, selecting L in both witnesses. Recommended. |
| Always compare high significands | Both highs are the same here; fails to settle these ties. |
| Always compare low significands | Both lows are zero for adjacent small subnormal totals; needs another rule there. |
| Specify nearest ties toward zero everywhere | Deterministic, but changes existing ties with a unique even candidate unnecessarily. |
| Defer to APFloat or use a 106-bit grid | Violates the explicit exact-value priority and loses admitted values. |

The recommendation includes a deterministic fallback if both candidates
receive the same parity. It does not claim an exhaustive theorem that
such a fallback is unreachable across all canonical high-bin boundaries.
This small added policy keeps the published rule total without making
implementers invent a second tie decision.

## Recommended exact spec diff

In §13.1's finite-canonical-pair paragraph in both dialect tracks, replace:

```diff
-with ties to the even low-component significand, using the high
-significand when the low component is zero,
+with nearest ties resolved as follows. Let L and U be the adjacent
+canonical finite values bracketing the exact result. If either low
+component is nonzero, compare the parities of BOTH low-component
+integer significands, treating a zero significand as even. Otherwise
+compare the high-component integer significands. The integer
+significand is the binary64 significand including the implicit leading
+bit for a normal value and without it for a subnormal; its sign does
+not affect parity. Choose the candidate of even parity when exactly
+one is even; if the parities coincide, choose the candidate whose
+exact sum has smaller absolute value. Existing exact-zero sign and
+overflow rules apply separately. This tie rule applies wherever this
+section requires nearest-even canonical-pair rounding, including
+incoming IEEE conversions and FMA; directed and nearest-away modes
+retain their specified rules,
```

The surrounding sentence should retain its existing NaN/inf and overflow
clauses. No change to §13.5's flags table or the exact-sum conversion
paragraph is needed. Add this explicit normative witness immediately
after that paragraph:

```text
For u=2^-1074 and h=1+2^-52, fma((h,u),(1/2,+0),(h/2,+0))
in nearest-even mode returns (h,+0). Conversion of binary128 bits
0x3c030000000000001200000000000000 to PPC returns
(binary64 bits 0x0030000000000001,+0). Each constrained operation,
with initial flags zero and exceptions observed, raises exactly inexact
(16). The unconstrained operations return the same bits without
modifying the floating-point environment.
```

## Hashes, catalog and consumers

This changes numerical semantics at an unresolved tie, not carrier types
or helper names. New arith bitcode and manifest hashes must be published
and driver/plugin consumers re-pinned. Materialised device/native closure
bytes, ISA object identities and certificates can consequently change;
do not reuse old result proofs against new linked bodies. The ISA
`ref@0.9` recipe catalog needs no change. A dialect version change also
changes mapping-version bindings. Keep old publication pins reproducible.

## Conformance vectors and actual verification

Ran `timeout 30 python3 -I -B -u
../bennett-arith/tests/ppc_zero_low_witness.py`, with the 1 GiB address-space
bound and headless environment in [INDEX](INDEX.md): exit 0. Exact rational
adjacency and binary128 representability passed. Both LLVM 18 and 23
native libraries returned L with FMA flags 0 and conversion flags 24.
This successful witness run proves the defect; it is not arithmetic
conformance. Sources and native libraries were read-only.

Acceptance vectors must test both witnesses and their negatives, odd/even
highs, low=0/±u, two-zero-low subnormal neighbors, low-subnormal/normal and
high-bin transitions, exact representable values and both signs. Check
nearest-even, nearest-away and all directed modes, sticky unrelated
flags, observed versus ignored exceptions, final-total underflow and
overflow, and every named conversion route reaching PPC. Include a direct
test of the equal-parity fallback. Do not substitute host double arithmetic
for the exact midpoint. Full-domain arithmetic work remains with 4yg.

## K entry and publication route

**No ISA 0.9 or 0.10 K entry is needed:** the ISA executes the linked
integer implementation and does not own PPC value selection. Proposed
dialect decision row: `PPC-ZERO-LOW-PARITY | §13.1 | compare both lows,
including zero; high fallback only for two zero lows; deterministic
same-parity fallback | 4yg.1 | semantic repair`.
Recommend the next published 0.2 patch (0.2.13 if available) and a matching
0.3-draft amendment, through the dialect council. This proposal does not
silently modify 0.2.12 or close 4yg.1. The existing cross-repo request
already routes the decision; no duplicate blocker is needed.

## Mixed fat object

Apply [fat-object-scope.md](../2026-11-02-rev2/fat-object-scope.md), especially
its separate device-closure and native-container identities (North Star
§§2, 3.3, 4.4). Only marked modules and their required linked helpers need
the revised PPC bodies and device certificates. The corresponding native
comparison uses those same materialised bodies. An ordinary native host
binary and host-only libc need no PPC certificate inventory. No launch,
handle, budget or tape format changes are introduced; the shared note's
container/root association and mixed-launch obligations remain explicit.

---

## Appendix: shared scoping statement fat-object-scope.md (verbatim)

# Mixed fat object — shared contract scope

Proposal for every revision in this directory; not a published ISA amendment.
Clause references are to [ISA 0.9](../../../spec/Bennett-ISA-Spec-0.9.md),
[the North Star](../../../../bennett/docs/Bennett-NorthStar.md), and, where
qualified, the maintained dialect 0.2/0.3 texts. This is the shared statement
required by bennett-4ht and the council rubric's standing mixed-fat-object check.

## Citable scoping statement

> A mixed fat object retains an ordinary native host binary and embeds ISA
> objects for marked device modules and their linked device closures (North
> Star §§2, 3.3, 4.4). ISA §§9.1–9.3 identify each device object and selected
> root; §12.3 certificates, owner records and reports cover that closure,
> with a separate binding/context set per device root and [] relative to
> that root (§12.1). Native entry, argv/envp and host-only libc need no ISA
> region, frame or certificate record; native comparison binds the selected
> materialised closure, not the whole host. Today §10 launches a device CC
> entry with copied arguments/entropy; §5.4 budgets bind device invocations,
> §3.3/§10 handles belong to a loaded program/run, and §7.3/§10 tapes cover
> device R effects. These require explicit container-to-object/root/certificate
> association, host-entry-to-device-entry bindings, budget/handle lifetime
> negotiation and tape/run association in a versioned mixed-launch contract.
> ISA §7.1 defines device memory but §10 defines no general host-memory-by-reference
> launch ABI: that contract must add address/layout mapping, range/liveness,
> aliasing, ownership/synchronisation, writeback and reversal rules, preserving
> dialect §§6.6, 8.5, 19.4–19.5. Until published, these are explicit
> bennett-4ht boundary obligations, not grounds to require whole-binary
> lowering or omit mixed execution.

## Present assumptions and exact publication changes

| Contract object | Assumption today | Exact change needed for mixed use |
|---|---|---|
| Object and linking (§§9.1–9.3) | One ISA object's closed sections and linked symbols; no native-container schema. | Publish a versioned inventory associating embedded/linked ISA object bytes and object_hash with selected device roots and certificates. A native-container hash, if used, is a separate identity. |
| Certificates/inventory (§§12.1–12.3) | Closure-keyed device-region records; current text does not explicitly delimit native inventory. | Insert the shared scoping rule in §12.3, cross-reference from §9.2, and require complete device-owner/link-proof coverage per root. Multiple device roots can share static closures without merging root-relative contexts. |
| Launch/entry (§10) | bennett_run(program, cc_entry, args, entropy) starts device CC; it is not native main. | Publish a host call/return shim and container/root selection/feature negotiation. Define native argument/result marshalling, including ptr (whose host binding §10 does not specify), status/fault propagation, suspend/reverse/close and ownership. Do not invent a current general launch shim. |
| Budgets (§5.4; §§10–11) | Validated token tuples and identity scoped to a program/run; action_call has no primary token (§4.7). | Bind selected device invocation budgets and token equality to the launch request; charge actual device/replay work. State host/shim accounting separately; a native process has no invented global B. |
| Handles (§3.3; §10; dialect §6.6) | Register ids refer to the loaded program's ledger; run ownership and token validity are explicit. | Map host-visible opaque handles to that program/ledger with validity and cross-launch ownership checks; preserve class vectors and token identities. Do not serialize native pointers as device ids or token tuples as identities. |
| Effect tape (§7.3; §10) | Run-associated R effects and explicit copied hostcall requests; no implicit log of native host I/O. | Associate each device run and tape with the launched root and define host effect/proxy ordering and replay at the boundary, preserving §7.4 reversal. Saved-journal interchange needs its own versioned replay profile. |
| Host memory by reference (§§7.1–7.2; dialect §§8.5, 17.1, 19.4–19.5) | Device layout plus dialect snapshot/replay and boundary-address/promotion rules; copied hostcall bytes do not provide general shared pointers. | Publish the mapping and lifetime protocol named in the statement, including allocator metadata/history and pointer-rich layouts, so ordinary host memory can be supplied safely without universal host promotion. Retain existing snapshot/replay as a construction, not the sole eventual capability. |

For example native main can call marked roots A and B in distinct ISA objects.
Each has its own object/root certificate and root context []; neither
certificate inventories main or host-only libc. A shared linked device
callee is checked in each root's actual invocation tree. A native comparison
executes the corresponding materialised region/callee closure under its
recorded layout, input and tool configuration (dialect §§17.7, 19.5, 19.9).

These notes specify boundary scope and exact remaining contract work; they
implement no container, host shim or memory registration. The existing
bennett-4ht issue tracks that publication/implementation obligation. Current
device contracts and their complete estimate/proof requirements remain in
force; an unimplemented boundary is not evidence that mixed execution works.
