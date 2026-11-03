# Council

You are the Muse seat of the Bennett council, grading the document below, acceptance dossier batch 3: 0jq, checker-fault-rate, brt-vbi, adg, pe1. The document is a dossier of 5 contract-repair proposals (0jq, checker-fault-rate, brt-vbi, adg, pe1; pe1 is a re-seat of a proposal your previous seat blocked) that the two other members (sol, astra) have each accepted in their latest round, including the bennett-4ht mixed-fat-object check. This is the final acceptance seat before the spec editor applies them. Grade EACH proposal independently, meaning its proposed spec diff and the claims supporting it, against the rubric on the absolute scale. The published specs are accepted text and are not under review, except where a diff interacts with them. Be exacting and skeptical. Verify every technical premise against your own knowledge and against the actual spec text. Name any premise that is false, including a misquoted or misnumbered clause. Do not defer to the other members' acceptance; their outputs are available for reference only.

Your workspace is `bennett-isa-spec` (read-only). Each dossier part names the spec it amends: the ISA text is `spec/Bennett-ISA-Spec-0.9.md`; dialect proposals amend `../bennett-dialect-spec/spec/`. They are NOT attached because of their size: read the clauses each proposal cites and every clause its diff touches before grading. Other files you can read:
- `docs/notes/` holds the proposal notes of 2026-11-02 and `docs/notes/2026-11-02-contract-verification.md`, the author's verification index with reproduction scripts.
- `reference-interpreter/` is the reference interpreter; `.beads/issues.jsonl` holds the cited beads.
- `../bennett/docs/Bennett-NorthStar.md` is the north star, also attached below.
- `../bennett/docs/council/<run>/round-<N>/` (run named in each part) hold the earlier rounds on these proposals, with both members' outputs; `isa-09-k82-2026-11-01` is K82.

A blocking issue is one that would make the project build the wrong thing if a diff were applied as written, or if it were left unapplied while its defect is real. Everything else is a suggestion. Prefix every blocking `id` with the proposal id (e.g. `lpe-M1`, `2cg-M1`); a block reopens only that proposal. Return `accept` only if the blocking list is empty for all 5. The `summary` must begin with one line per proposal of the form `<id>: ACCEPT` or `<id>: BLOCK (<blocking ids>)`. `accept` for a proposal means the editor may apply its diff (with your suggestions at their discretion) through the publication route the proposal states (a 0.9 K repair, or the 0.10 release where the proposal says so). Do not block on the route itself unless it would make two conformant implementations of the same declared version compute different results.

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


Notes for this batch (binding). 0jq and checker-fault-rate are a JOINT repair of ISA §12.3 verification.fault_rate: they now carry one byte-identical harmonised paragraph (your batch-2 items 0jq-M1 / checker-fault-rate-M1; sha256 b34376b04d0d2e295018245c1f7f3ce36b4f55ad5ed18e8f127119e36b9685b0 recorded in both); grade them together for satisfiability. The previous Muse seat's outputs are in `../bennett/docs/council/accept-muse-batch2-2026-11-02/round-1/out-muse.json`. Give `previous_status` entries for 0jq-M1, checker-fault-rate-M1, pe1-M1 and adg-M1.


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

# Acceptance dossier (Muse seat, batch 3): 0jq, checker-fault-rate, brt-vbi, adg, pe1

Scope (advisor ruling R13, 2026-11-03; maintainer decision D2: 0jq is routed as an in-version 0.9 K once this seat accepts): each proposal below was ACCEPTED by both other council members (sol, astra) in its latest round (empty blocking lists, consensus agree) and satisfied the rubric's standing bennett-4ht check (mixed fat object stays reachable) in that round. This is the final acceptance seat: grade each proposal independently on its own merits. Each part names its run, accepted round and the spec it amends. Several parts cite the shared scoping statement `docs/notes/2026-11-02-rev2/fat-object-scope.md`; it is reproduced once in the appendix. Parts are separated by horizontal rules.

---

## Dossier part: 0jq (run pass2-0jq-2026-11-02; accepted by sol, codex in round 3; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-03-notefix/0jq.md)

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
null encoding preserves each capability and every remaining obligation.

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
+verification: { oracle: i | null, ... fault_rate: null | { ... } }
```

Append to §12.3:

```text
verification.oracle is null when this record makes no oracle/table/
program comparison claim. A non-null index must name an applicable
exhaustive or sampled comparison claim in this record's claims array;
its explicit expected relation determines its meaning. A structural
adjoint-table or translation claim is not such a comparison claim.

<!-- muse-fault-rate-paragraph -->
verification.fault_rate is required and has type null | RATE. For action and perm_action records it MUST be null and fault_rate_contexts MUST be absent. For an oracle record it MUST be a RATE whenever a fault census is asserted or is required to discharge an executable or scheduled acceptance claim; it MAY be null only when the record asserts no fault census, and null discharges no fault-rate obligation.
<!-- /muse-fault-rate-paragraph -->

For kind=oracle, verification.fault_rate MUST be a RATE whenever a fault census is asserted or is required to discharge an executable or scheduled acceptance claim (including every oracle in the complete invocation tree of a bound schedule, via fault_rate_contexts); it MAY be null only when the record asserts no fault census, and null discharges no fault-rate obligation and satisfies no zero-fault gate.

An action
has no fault outcome of its own; a nested oracle's census belongs to
that oracle and its resolved invocation. Applicable oracle-correctness,
fault-rate, borrowed-system and realisation obligations remain required
before an executable or algorithm acceptance claim can use them.
A non-null fault_rate must be validated even when no acceptance claim requires it.

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

Incorporate [the shared scoping statement](../2026-11-02-rev2/fat-object-scope.md#citable-scoping-statement).
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
need change under an authorized in-version repair. Replacing an inapplicable
fault report with null changes certificate bytes. Linkers,
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
[check_rev2.py](../2026-11-02-rev2/check_rev2.py). The originating note cites:
`../bennett-circuits/docs/design/2026-11-01-m5-contract-requests.md`,
“Structural-only packets”. No new packet checker is implemented here. A composed root packet may
contain inner's correctly keyed owner record; packet containment does not
move the entry into the outer region record. For the published controlled-action
fixture migration, the root table claim at index 0 gives verification.oracle:0;
the numerical-only flip record retains null, and both action fault-rate
placeholders become null. These are proposed certificate changes only.

## Release and route

Recommend a **0.9 K applicability/hash-definition repair**. The owner rule
needs clarification and link/consumer tests, not a new proof mechanism.
Keep 0jq open for council acceptance and producer/checker implementation.
Maintainer D2 (2026-11-03) authorizes this in-version 0.9 K route only
after the joint 0jq/checker-fault-rate revision passes sol+astra and a
Muse seat accepts. Until both conditions hold, 0jq remains HELD and is
not ACCEPTED FOR SPEC. The publication rules below apply.

## Publication and validation boundary

This is a revision proposal, not council acceptance or a consumer implementation.
The default publication rule in spec/README.md requires a full version bump
for semantic changes. The recommended 0.9 K route has conditional maintainer
authorization under D2; it still requires the joint sol+astra round and
Muse acceptance stated above. This note grants no council acceptance. All unchanged-hash claims assume unchanged header/source
and catalog envelopes. A full version publication recomputes affected symbol,
object, target, schedule, certificate and versioned ref-library identities and
consumer pins even when recipe bodies stay fixed. Published 0.9 bytes remain
available; older closed-schema readers require an upgrade for new fields.

The reproducible finite and document checks are in [check_rev2.py](../2026-11-02-rev2/check_rev2.py):
`timeout 120 python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/notes/2026-11-02-rev2/check_rev2.py`.
Executed for this revision: exit 0, all eight PASS result lines.
These finite checks verify witnesses and revision structure; they implement
no proposed-format checker or host shim. No full repository gate or sibling gate is claimed: scripts/pre-push
uses git/worktree writes, forbidden by this runner, and its setup changes paths
outside this job. Underlying beads remain open for publication and consumers.

## Muse blocking items and resolution

This joint revision starts from the latest graded notes: 0jq round 2
(`19ffcda5e44a87d0878c89e357fa4ccea163d50883e031aff781fb3e43bd923e`)
and checker-fault-rate round 3
(`71a74c494872f94fa40271dd0d81ef140fa01d6095006ad859400a5b5037a189`).
It proposes resolutions, not council verdicts. Both notes carry the same
Muse paragraph above and the same conditional oracle sentence, copied
verbatim from [out-muse.json](../../../../bennett/docs/council/accept-muse-batch2-2026-11-02/round-1/out-muse.json).
RATE abbreviates `{invocation:{args,budget},domain,faults_by_code,
undefined_excluded,layout_dependent_excluded,exclusion_evidence?}`.
A non-null RATE binds its own exact invocation and full oracle domain;
it never inherits a convenient claim's budget. For a bound schedule,
every complete-tree oracle context, including defaults and predicated-off
calls, needs its recount; the legacy field is the first canonical
context's projection. Exclusions do not shrink the reference census.
The complete context and evidence contract is retained in
[checker-fault-rate.md](checker-fault-rate.md); these requirements neither
invent a census for a structural-only packet nor relax acceptance gates.

| Blocking item | Resolution and concrete witness |
|---|---|
| 0jq-M1 | The closed schema requires `fault_rate: null | RATE`; actions use null and omit `fault_rate_contexts`. Both action fault-rate placeholders become null. A missing key is malformed, and null proves no zero-fault result. The reference_program_hash definition and owner-local inverse-pair rules are unchanged. |
| checker-fault-rate-M1 | Oracle RATE is conditional on an asserted/required census, including every oracle context in a bound schedule. A structural-only oracle may use null; it discharges no census or zero-fault gate. All accepted recount, deterministic context projection and classifier-bundle rules remain. |

There are no other Muse blocking items for these two proposals. The
accepted mixed-fat-object scope, hash conditions and prior-round fixes
remain. Relative witness links now point to their original directories;
historical verification reports above remain historical.

### Structural-only oracle conformance vector

Take a standalone oracle with body `r = lift.add x a; lift.retval r` and
a checked structural `adjoint_table`/translation claim only, no comparison
claim, no asserted census and no bound schedule. Supply all ordinary
identity, signature, frame and claim fields as required. The following
JSON is the verification fragment under test, not a complete certificate
or a newly introduced certificate field:

<!-- structural-only-oracle -->
```json
{"kind":"oracle","verification":{"oracle":null,"fault_rate":null}}
```

| Request for the same structurally valid packet | Expected result |
|---|---|
| Standalone structural validation, no census asserted | Accept as a structural packet. |
| Executable acceptance requiring a fault census | Reject that acceptance claim: null discharges no census obligation. |
| Scheduled acceptance requiring all oracle contexts, or a zero-fault gate | Reject that acceptance claim: no RATE/context coverage is supplied. |
| Remove fault_rate instead of using null | Reject schema validation: required key missing. |
| Assert a census while retaining null | Reject the asserted census. |

With the same body, args=["1"] and B=1, a verified RATE counts
256 code-1 faults over the full 4×4×16 domain; with B=2 it counts zero.
Those are actual census results and cannot be inferred from the null
packet. The focused script checks these applicability outcomes, action
null versus omitted keys, the fixture migration, unchanged owner rules
and the retained recount/bundle text. It is a finite contract test,
not an implementation of the proposed production certificate checker.

### Paragraph byte identity and verification

Extract exactly the UTF-8 bytes between the two `muse-fault-rate-paragraph`
markers, excluding the marker lines and the paragraph's terminating LF.
There is no line reflow or Unicode normalization. These are the paragraph
bytes quoted by Muse in 0jq-M1; the extra conditional oracle sentence
is copied verbatim from checker-fault-rate-M1 in both notes.

| Note | Shared paragraph SHA-256 |
|---|---|
| 0jq.md | `b34376b04d0d2e295018245c1f7f3ce36b4f55ad5ed18e8f127119e36b9685b0` |
| checker-fault-rate.md | `b34376b04d0d2e295018245c1f7f3ce36b4f55ad5ed18e8f127119e36b9685b0` |

Verification: `timeout 30s python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/check_notes.py joint`
exited 0. Both extracted hashes equal the values above and Muse's exact
paragraph. No source, fixture, spec or catalog was edited.

Every producer and closed-schema reader using these amended 0.9
certificate bytes must upgrade together for the required nullable field
and context/evidence fields; older readers cannot silently accept them.
Remaining council work: joint sol+astra review, then a Muse acceptance
seat. D2 keeps 0jq HELD until those conditions pass. Publication and
producer/checker implementation follow acceptance; this revision performs
none of those steps and reserves no K number.

---

## Dossier part: checker-fault-rate (run contract-checker-fault-rate-2026-11-02; accepted by sol, codex in round 4; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-03-notefix/checker-fault-rate.md)

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
<!-- muse-fault-rate-paragraph -->
verification.fault_rate is required and has type null | RATE. For action and perm_action records it MUST be null and fault_rate_contexts MUST be absent. For an oracle record it MUST be a RATE whenever a fault census is asserted or is required to discharge an executable or scheduled acceptance claim; it MAY be null only when the record asserts no fault census, and null discharges no fault-rate obligation.
<!-- /muse-fault-rate-paragraph -->

For kind=oracle, verification.fault_rate MUST be a RATE whenever a fault census is asserted or is required to discharge an executable or scheduled acceptance claim (including every oracle in the complete invocation tree of a bound schedule, via fault_rate_contexts); it MAY be null only when the record asserts no fault census, and null discharges no fault-rate obligation and satisfies no zero-fault gate.
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

The files [checker-fault-rate.bisa](../2026-11-02-rev4/checker-fault-rate.bisa) and
[oracle_witness.rs](../2026-11-02-rev4/oracle_witness.rs) exercise this exact two-row oracle
through the read-only reference interpreter library. For B=0,1,2 and each
x=0..3, the witness compares the independent reference outcome with the
literal reversible machine, calls its actual commit method for all 4 target
words and 16 incoming fault words, and then inverses every executed step.
It checks the entire initial machine snapshot and clean frames. This covers
768 full interface tuples: 256 faults at each short budget, zero at B=2.

[check_rev4.py](../2026-11-02-rev4/check_rev4.py) supplies two fixed, serialized raw blobs in
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
timeout 300s python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/run_witnesses.py
```

The script unsets GUI/browser variables, sets TMPDIR and CARGO_TARGET_DIR
under .tmp/sol-notefix-s4, bounds processes at 6 GiB, uses -j4 and applies
timeouts. It runs no full gate or git command and changes no interpreter
source. It runs the retained finite CFR-3 checker in memory against this
revision, redirecting only the job artifact paths. The current run exited
0: all 768 oracle tuples and classifier-bundle positive/negative cases
passed. Historical outcomes remain in
[the shared verification results](../2026-11-02-rev4/verification.md). The earlier inline
hand model remains an independently understandable counting example; the
actual interpreter/machine witness above supplies execution evidence.

## Muse blocking items and resolution

This joint revision starts from the latest graded notes: 0jq round 2
(`19ffcda5e44a87d0878c89e357fa4ccea163d50883e031aff781fb3e43bd923e`)
and checker-fault-rate round 3
(`71a74c494872f94fa40271dd0d81ef140fa01d6095006ad859400a5b5037a189`).
It proposes resolutions, not council verdicts. Both notes carry the same
Muse paragraph above and the same conditional oracle sentence, copied
verbatim from [out-muse.json](../../../../bennett/docs/council/accept-muse-batch2-2026-11-02/round-1/out-muse.json).
RATE abbreviates `{invocation:{args,budget},domain,faults_by_code,
undefined_excluded,layout_dependent_excluded,exclusion_evidence?}`.
A non-null RATE binds its own exact invocation and full oracle domain;
it never inherits a convenient claim's budget. For a bound schedule,
every complete-tree oracle context, including defaults and predicated-off
calls, needs its recount; the legacy field is the first canonical
context's projection. Exclusions do not shrink the reference census.
The complete context and evidence contract is retained in
[checker-fault-rate.md](checker-fault-rate.md); these requirements neither
invent a census for a structural-only packet nor relax acceptance gates.

| Blocking item | Resolution and concrete witness |
|---|---|
| 0jq-M1 | The closed schema requires `fault_rate: null | RATE`; actions use null and omit `fault_rate_contexts`. Both action fault-rate placeholders become null. A missing key is malformed, and null proves no zero-fault result. The reference_program_hash definition and owner-local inverse-pair rules are unchanged. |
| checker-fault-rate-M1 | Oracle RATE is conditional on an asserted/required census, including every oracle context in a bound schedule. A structural-only oracle may use null; it discharges no census or zero-fault gate. All accepted recount, deterministic context projection and classifier-bundle rules remain. |

There are no other Muse blocking items for these two proposals. The
accepted mixed-fat-object scope, hash conditions and prior-round fixes
remain. Relative witness links now point to their original directories;
historical verification reports above remain historical.

### Structural-only oracle conformance vector

Take a standalone oracle with body `r = lift.add x a; lift.retval r` and
a checked structural `adjoint_table`/translation claim only, no comparison
claim, no asserted census and no bound schedule. Supply all ordinary
identity, signature, frame and claim fields as required. The following
JSON is the verification fragment under test, not a complete certificate
or a newly introduced certificate field:

<!-- structural-only-oracle -->
```json
{"kind":"oracle","verification":{"oracle":null,"fault_rate":null}}
```

| Request for the same structurally valid packet | Expected result |
|---|---|
| Standalone structural validation, no census asserted | Accept as a structural packet. |
| Executable acceptance requiring a fault census | Reject that acceptance claim: null discharges no census obligation. |
| Scheduled acceptance requiring all oracle contexts, or a zero-fault gate | Reject that acceptance claim: no RATE/context coverage is supplied. |
| Remove fault_rate instead of using null | Reject schema validation: required key missing. |
| Assert a census while retaining null | Reject the asserted census. |

With the same body, args=["1"] and B=1, a verified RATE counts
256 code-1 faults over the full 4×4×16 domain; with B=2 it counts zero.
Those are actual census results and cannot be inferred from the null
packet. The focused script checks these applicability outcomes, action
null versus omitted keys, the fixture migration, unchanged owner rules
and the retained recount/bundle text. It is a finite contract test,
not an implementation of the proposed production certificate checker.

### Paragraph byte identity and verification

Extract exactly the UTF-8 bytes between the two `muse-fault-rate-paragraph`
markers, excluding the marker lines and the paragraph's terminating LF.
There is no line reflow or Unicode normalization. These are the paragraph
bytes quoted by Muse in 0jq-M1; the extra conditional oracle sentence
is copied verbatim from checker-fault-rate-M1 in both notes.

| Note | Shared paragraph SHA-256 |
|---|---|
| 0jq.md | `b34376b04d0d2e295018245c1f7f3ce36b4f55ad5ed18e8f127119e36b9685b0` |
| checker-fault-rate.md | `b34376b04d0d2e295018245c1f7f3ce36b4f55ad5ed18e8f127119e36b9685b0` |

Verification: `timeout 30s python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/check_notes.py joint`
exited 0. Both extracted hashes equal the values above and Muse's exact
paragraph. No source, fixture, spec or catalog was edited.

Every producer and closed-schema reader using these amended 0.9
certificate bytes must upgrade together for the required nullable field
and context/evidence fields; older readers cannot silently accept them.
Remaining council work: joint sol+astra review, then a Muse acceptance
seat. D2 keeps 0jq HELD until those conditions pass. Publication and
producer/checker implementation follow acceptance; this revision performs
none of those steps and reserves no K number.

---

## Dossier part: brt-vbi (run derive3-brt-vbi-2026-11-02; accepted by sol, codex in round 1; amends the Bennett dialect spec (../bennett-dialect-spec/spec/); source note bennett-isa-spec/docs/notes/2026-11-02-derive3/brt-vbi.md)

# brt-vbi — delivery of arbitrary-width runtime helper bodies

Council proposal, not a specification or runtime implementation. Origin:
`brt-vbi` (blocked decision), blocking `brt-zct` in bennett-runtimes.
References: [dialect 0.2.12](../../../../bennett-dialect-spec/spec/Bennett-Dialect-Spec.md)
§§12.1, 12.7–12.8, 13.1, 19.1, and the corresponding
[0.3 draft](../../../../bennett-dialect-spec/spec/Bennett-Dialect-Spec-0.3-draft.md).

## Exact defect and North Star scope

§12.7 names width-specific ordinary runtime bodies for wide multiply,
divide, remainder and shifts. §12.8 similarly names integer intrinsic
helpers, including slot-based wide forms. §19.1 requires matching-major
runtime bitcode before materialisation. §13.1 publishes an offline
instance-request protocol for arith, but none of these clauses publishes
a runtime-integer request/response contract or a collection procedure for
helpers introduced during normalisation. A consumer cannot depend on
the runtime producer's private generator interface.

This is a **dialect delivery/interoperability gap**, alongside an actual
missing-implementation obligation. It is not a new ISA arithmetic
instruction or launch ABI gap. Naming an ordinary helper already makes
its body required; a finite default library failing to contain i257
does not make that LLVM width unsupported. The gap matters to North Star
§§3.2–3.3, 5.1's whole materialised LLVM and reproducible comparison.
It does not justify narrowing widths, trapping valid arithmetic, omitting
libc/Julia/SQLite closure, or declaring the broader brt-zct work complete.

## Alternatives and concrete witness

Read-only source witness:
`../bennett-runtimes/.tmp/sol-runtimes-queue/tmp/runtime-width-request.ll`.
It loads two i257 values, multiplies, calls `llvm.ctpop.i257`, stores i257.
Both LLVM 18 and 23 `opt -passes=verify -disable-output` accept it.
Both live `dist/llvm<M>/bennett-runtimes.bc` lack definitions for
`__bennett_rt_i257_mul` and `__bennett_rt_i257_ctpop`, confirmed with
matching-major `llvm-nm --defined-only`. These are current observations,
not an inference from the producer's progress report.

For a concrete numerical vector, a=2^256+3, b=2. Modulo 2^257 the product
is 6 and its population count is 2. A five-limb input slot has widths
[64,64,64,64,1]; ctpop writes [2,0,0,0,0]. Dropping the top input limb
can be caught separately by ctpop(a)=3. This requires actual ordinary
bodies, not a declaration that merely passes LLVM verification.

| Alternative | Assessment |
|---|---|
| Publish an offline request/manifest protocol in the dialect | Producer-independent, analogous to arith; recommended. |
| Prebuild every admitted width and operation | A possible complete distribution, but costly; a common-width subset is only a cache. |
| Publish a separate runtime ABI note | Viable only if versioned and normatively incorporated by the dialect; a producer README alone cannot bind competitors. |
| Add ISA primitives or a private driver-generator API | Unnecessary machine extension or unpublished coupling. |

## Recommended exact dialect/ABI text

Insert the following titled subsection at the end of §12.8 before the
examples, and cross-reference it from §19.1. Mirror it in both tracks.
The executable name below is a proposed public interface, not a claim
that today's runtimes supplies it.

```text
Runtime integer instance delivery v1.

The runtimes distribution MUST supply an offline executable interface:
  bennett-runtimes-instantiate --request REQUEST --bitcode OUTPUT_BC
                             --manifest OUTPUT_JSON
The driver may configure the executable path. Exit zero means both
outputs are complete; nonzero means no output is usable. Generation
must not require network access, a host runtime service or private
consumer knowledge. The distribution MUST identify its version.

REQUEST is UTF-8 JSON with exactly schema, llvm_major, target_triple,
data_layout and entries. schema is "bennett-runtimes-instantiations-1";
llvm_major is the link's integer LLVM major; target_triple and
data_layout are the link's effective LLVM strings. Each entries element
has exactly op (string) and width (integer, not boolean).

The op set is mul, udiv, sdiv, urem, srem, shl, lshr, ashr from §12.7;
and bswap, bitreverse, ctpop, ctlz, cttz, fshl, fshr, sshl_sat,
ushl_sat, smul_fix, umul_fix, smul_fix_sat, umul_fix_sat, sdiv_fix,
udiv_fix, sdiv_fix_sat, udiv_fix_sat, pdep, pext, clmul,
smul_with_overflow and umul_with_overflow from §12.8. Dots in an
intrinsic name become underscores. width is the original integer
operand width W, not a limb width or result aggregate size. The
operation and width must be admitted by the link's LLVM major and the
corresponding published row; §12.7 requests require W>128, and the
overflow-helper requests require W>64. Unknown fields/operations,
nonintegral/out-of-range widths and target/major/layout mismatches are
errors. Every valid request remains an implementation obligation.

Duplicates denote one instance. Canonical request bytes are UTF-8 JCS,
without a trailing LF, with unique entries sorted by op's unsigned
UTF-8 bytes then ascending numeric width. request_sha256 is the
lowercase hexadecimal SHA-256 of those bytes. A supplied width list
or prebuilt cache MUST NOT become a capability limit.

OUTPUT_BC is ordinary matching-major bitcode whose triple and
DataLayout equal the request. For each requested (op,W), provide the
exact public definition, type, scalar flags, result convention and
fault behavior of §§12.7–12.8. In particular, wide mul is
void @__bennett_rt_i<W>_mul(ptr dst,ptr a,ptr b), and wide ctpop is
void @__bennett_rt_i<W>_ctpop(ptr dst,ptr a). The existing shadow-stack
slot layout, partial top limb and push/store/call/load/pop order are
unchanged. All reachable implementation bodies must be supplied or
resolved through the published matching-major base runtime/arith
distributions and their published instance protocols. No unresolved
instance placeholder, trap stub or hidden host implementation counts
as delivery.

OUTPUT_JSON is JCS with exactly schema, request_sha256,
bitcode_sha256 and exports. schema is "bennett-runtimes-instances-1";
bitcode_sha256 hashes the exact OUTPUT_BC bytes. exports lists every
externally visible definition in that module, sorted by unsigned UTF-8
symbol bytes, each with exactly symbol and function_type; function_type
is LLVM's printed function type for the requested major, without the
function name or attributes. Every requested public symbol must occur
exactly once and have its published type. Generation with identical
canonical request and producer version must reproduce both output
byte strings regardless of output paths. The driver verifies hashes,
triple, layout, definitions and types before using the output.

Collection is a link-preparation fixed point. Starting from the selected
device entries and their conservatively reachable bitcode closure,
include calls already naming these helpers and all helpers that the
published normalisation rules will introduce, including vector
scalarisation, N27 and the N22 applications after N27/N32. Collect
arith instances by §13.1 as well. Resolve runtime/arith requests and
their dependencies until no new (provider,instance) is required and
every required body is linked. Include all possible device call
targets; do not select just one runtime input path. Declarations alone
do not satisfy the fixed point. A provider cycle must resolve to actual
linked definitions; repeated unresolved requests are a loud failure.

This discovery is a non-emitting analysis using the published rules;
it does not rerun or change §12.1's normative rule order. Link the
complete collected bodies before final materialisation, identically
in the lifted and native comparison inputs. If later optimisation or
materialisation reveals a new required helper, restart preparation
with the enlarged request and rebuild both outputs; never patch only
one build or silently leave it unresolved. Failure to generate a
valid instance is an implementation blocker, not an unsupported-width
verdict, narrower substitute or permitted fault of the device program.
```

Add to §19.1 after the bitcode-source paragraph:

```text
Before final materialisation the driver MUST complete the runtime
integer instance-delivery fixed point of §12.8 and the arith requests
of §13.1, using the same resolved closure in both builds. Whole-program
device mode uses its entire device closure; selective-module mode
collects the union required by its marked device roots. Neither mode
requires host-only code to become a device region.
```

## Hashes, catalog and consumers

Request and output hashes are different identities; neither is an ISA
`object_hash` or the arith/ref catalog hash. Provider-version changes
invalidate the generation cache even when the request is identical.
Generated bitcode changes materialised closures, costs, stack use and
the resulting object/schedule/certificate bindings. Drivers, plugins,+runtimes, numerical providers and conformance owners must coordinate
publication and repin. No ISA `ref@0.9` recipe change is necessary.

## Conformance vectors and actual verification

The bounded command in [INDEX](INDEX.md) ran both major-specific LLVM
verifiers and symbol audits: exit 0, both missing-definition assertions
passed. This establishes the delivery witness, not helper implementation
or whole-program execution. No sibling gate was run.

After publication require: i129/i192/i257 partial-top-limb values;
mul and ctpop together; large admitted widths with a resource-bounded
generation test; narrow intrinsic helpers; scalar flags and overflow
aggregate types; all helper families with published fault behavior.
Check reordered/duplicate requests canonicalise identically, unknown
op/invalid width/major/layout reject loudly, manifests cannot omit or
mis-type a requested definition, and changed request/bitcode hashes fail.
Test a helper introduced only by scalarisation, one after N32/repeated
N22, a transitive dependency and a discovery restart. Verify byte
reproduction in relocated directories and link/execute both materialised
builds. Merely passing opt verification is insufficient.

## K entry and publication route

**No ISA 0.9/0.10 K entry:** this is a dialect/tool-distribution contract.
Proposed dialect decision row: `RUNTIME-INSTANCES-1 | §§12.8,19.1 |
offline request/manifest and complete device-closure fixed point |
brt-vbi | additive versioned delivery protocol`. Recommend the next
published 0.2 patch and the corresponding 0.3 draft text. A separate
ABI note is acceptable only with a normative versioned dialect reference.
Leave brt-vbi/brt-zct open for ratification and implementation; publication
of a proposal does not unblock a consumer's unpublished interface.

## Mixed fat object

[fat-object-scope.md](../2026-11-02-rev2/fat-object-scope.md) binds this
proposal (North Star §§2, 3.3, 4.4). Collect helpers for marked modules and
their linked device closures. Multiple roots may share generated bodies;
each device root retains its own certificate/context association. The
ordinary native host binary, host entry/argv/envp and host-only libc stay
outside that inventory. Native comparison binds the matching materialised
device closure. Request manifests are build inputs, not a new launch,
budget, handle or effect-tape protocol. Container/root association and
host-memory mapping still need the exact mixed-launch additions named in
the shared scope note; this delivery decision keeps them reachable.

---

## Dossier part: adg (run contract-adg-2026-11-02; accepted by sol, codex in round 3; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-03-notefix/adg.md)

# adg — loaded-device-program state across launches

Full revised proposal for council review; `b-isa-spec-adg`. This replaces
the [first-pass note](../2026-11-02-contract-adg.md) as a review document;
it does not edit the published spec or interpreter. Clause numbers refer
to [ISA 0.9](../../../spec/Bennett-ISA-Spec-0.9.md).

Round 1 accepted the memory/ledger rule (sol and astra); the round-2
bennett-4ht re-check accepted the added device-instance scoping statement.
Muse subsequently blocked the proposal on **adg-M1**, a core §7.3/§10
lifetime omission. This revision retains those accepted decisions and
chooses Muse's recommended program-lifetime device state, with per-run
entropy position and effect tape. It still requires renewed sol/astra
review and a later Muse seat; it is not yet ACCEPTED FOR SPEC.
Round 2 then raised adg-R2-1/adg-R2-B1: persistent device models also
need exclusive ownership. This revision adopts launch-time acquisition
and adds overlapping-run witnesses; no other contract fix is made.

## Defect and North Star scope

ISA §7.1 defines initial memory, allocation table and bump pointer without
saying whether initialization occurs at load or every run. **§3.3 places
the register ledger at program scope; §3.2 lists it among machine-state
components.** §10 gives a run exclusive ownership only until CLOSED;
§7.4 and T4 restore a run's entry state on eligible reversal. These support
program-lifetime state but do not explicitly settle classical-memory
initialization.

The same omission affects §7.3's initially empty console, clock `c=0`
and block sector map. The original §10 addition's unqualified
“initialization is never repeated merely to start a run” could also
incorrectly carry entropy position `p` into the next run, although §10
copies a new entropy tape at each `bennett_run`. A persistence-reading
executor and a reset-reading executor would still return different clock
and block results on the second entry. This is adg-M1's observable S0
contract defect, not an instruction or allocator change.

Dialect 0.3 draft §§6.5–6.6 requires a persistent qreg table in device
memory and parameter/result identities across entries. North Star §3.1's
register handles and §5's REPL/library device model require this lifetime;
its block-device uses require a disk that survives repeated entries. A
reset on every entry loses the table while registers remain live.
Persistence preserves repeated SQLite/kernel invocations and every demo
rung. No capability is rejected or made inert by this repair. Oracle-local
workspace initialization and cleanup remain governed by §5.2.

## Chosen lifetime rule and alternatives

| State | Established | Later run / reversal |
|---|---|---|
| CC/R memory bytes, allocation table, bump pointer (§7.1) | Once per loaded device program | Inherit preceding CLOSED run's state; eligible reversal restores entry values. |
| Register ledger and live identities (§3.3) | Program instance; entries created by the existing operations | Survive CLOSED unless consumed/freed; ownership is released at CLOSED. Ids remain subject to §3.3's non-reuse rule, including reversal. |
| Console bytes, clock `c`, block sector map (§7.3) | At device-program load; block map from `layout.block_image` under K10, else empty | Persist; effects and their reversal change them; CLOSED does not reset them. |
| Copied entropy tape and position `p` (§§7.3/10) | Each `bennett_run`, with `p=0` | Bound to that run; undo restores that run's position, never a previous run's cursor. |
| Active effect tape, dynamic environments and run history (§§7.3–7.4/10) | Each run | Record that run's effects/history; no inheritance into the next run. Saved journals remain a separately versioned tool interface. |
| Host-minted / device-minted budget tokens (§5.4) | Program / minting run respectively | Host token valid until unload; device token invalid after its run is CLOSED (or revoked by reversal). |

Program-lifetime memory and devices are the recommendation: they match the
ledger, T4's entry-state restoration and the existing persistent-table
consumer. Explicitly resetting *all* devices on each run is Muse's other
possible contract decision, but would require different cross-entry disk
assumptions and would not preserve the selected persistence rule. An
implicit reset when no register is live still changes classical/device
results and has no supporting clause. The recommendation changes none of
§7.1's heap/table limits or `free` semantics.

## Concrete lifecycle witnesses

### Classical memory retained from round 1

Use `ptr_width=16, H=16, A_tab=2, S_cells=0, null_size=1,
heap_base=16, heap_limit_max=16` and one global `g` at base 1, size 1,
image `00`. Run A allocates one byte (address 16), stores 7 in `g`,
completes and is CLOSED. Run B loads `g`, allocates one byte and completes.
The results and full allocation state after B are:

| A disposition before B | B result `(g, allocation)` | Bump | Table `(base,size,live,pinned)` |
|---|---|---|---|
| COMPLETED → CLOSED | `(7,17)` | 18 | `[(1,1,1,1),(16,1,1,0),(17,1,1,0)]` |
| COMPLETED → REVERSED → CLOSED | `(0,16)` | 17 | `[(1,1,1,1),(16,1,1,0)]` |

All heap bytes are zero in this witness; `g` is respectively `07` or
`00`, and every other logical byte is zero. A reset-reading executor would
return `(0,16)` even without reversal, distinguishing the interpretations.
If A also frees 16, B still allocates 17: the dead entry remains and
storage is not reclaimed. After allocations at 16, 17 and 18 across CLOSED
runs, a fourth heap allocation faults with code 2, with bump still 19 and
no table/byte mutation: the global plus three heap entries fill the table.
A FAILED R call whose completed prefix allocated 16 and stored 7 leaves
those mutations in place on close; explicit eligible reversal removes
them. Closing is never implicit rollback.

### Device witness resolving adg-M1

Use one loaded instance, sequential device CC launches whose bodies call
R helpers. The layout has disjoint live globals: `src` at 16, size 512,
all bytes `a5`; `dst` at 528, size 512, zero; `clk` at 1040, size 8,
zero; `ent` at 1048, size 1, zero. Set `ptr_width=16, H=12, A_tab=3,
S_cells=0, null_size=1, heap_base=2048, heap_limit_max=64`.
`block_image` contains sector 0 = 512 zero bytes and sector 1 = 512
`ff` bytes, so sector 2 is initially **absent**.

Run A's R helper executes, in order: `clock.read(clk)`,
`block.write(2,src)`, `console.write(src,1)`, `entropy.read(ent,1)`.
Its copied entropy tape is `[11]` (hex bytes). It writes clock value 0,
leaves `c=1`, creates sector 2 with 512 `a5` bytes, appends console byte
`a5`, consumes its entropy byte and has four effect-tape entries.

Run B's R helper executes `clock.read(clk)`, `block.read(2,dst)` and
`entropy.read(ent,1)`, with its own copied tape `[33]`. It returns
`(load.i64 clk, load.i8 dst, load.i8 ent)`:

| A disposition before B | B result (decimal) | Device state after B | Tape belonging to B |
|---|---|---|---|
| COMPLETED → CLOSED | `(1,165,51)` | `c=2`, console=`a5`, sector 2 present with 512 `a5` bytes | Three entries, beginning with B's clock read of 1; entropy entry is byte `33`. |
| COMPLETED → REVERSED → CLOSED | `(0,0,51)` | `c=1`, console empty, sector 2 absent; B reads all 512 zero bytes | Three entries, beginning with B's clock read of 0; entropy entry is byte `33`. |

In either case B starts with `p=0`, ends with `p=1`, and its tape never
contains A's four entries. Closing A releases its record; reversal first
removes its active effects. Saved journals do not become B's tape. Inspect
all 512 bytes of `dst`, not only the returned first byte. Sectors 0 and 1 remain present
with their initial bytes; reversal must preserve the distinction between
present-zero sector 0 and absent sector 2. A FAILED after the four effects
has the same retained device prefix until reversed. Reversal restores the
modeled console sequence; T4 does **not** retract externally observed output.
Fresh loading restores the initial clock/console/block map and memory.

### Overlapping open runs: adg-R2-1 / adg-R2-B1

Use disjoint live buffers, no quantum registers and one loaded device
instance initially at clock 0 and empty console. A's entry calls an R
helper that reads the clock and appends `a5`; B's entry calls a different
R helper that reads the clock and appends `5a`. Both transitive call
closures reference the same clock and console despite disjoint buffers.

Without device ownership, A completes open at `c=1`, console=`a5`;
B completes and closes at `c=2`, console=`a55a`. Reversing A decrements
the clock and pops one byte, leaving `c=1`, console=`a5`, rather than
A's entry `c=0`, empty console. B's byte is popped. This is the reported
T4 counterexample, including A reversing after B touched both models.

Under the proposed fix, A acquires both models before execution and
retains them after COMPLETED. B's attempted launch returns
`E_INVALID_STATE`, with no run effects, entropy consumption, memory
mutation or ownership acquisition; `c=1`, console=`a5` remain. Now A
can reverse while still owning both: `c=0`, console empty and A's own
buffers/entropy cursor/effect tape restore their entry state. T4 holds.
Ownership remains A's while REVERSED, so another B attempt still
conflicts until A is CLOSED.

| A disposition, then retry B | B reads | State after B |
|---|---|---|
| A CLOSED without reversal | 1 | `c=2`, console=`a55a` |
| A REVERSED then CLOSED | 0 | `c=1`, console=`5a` |

B has its own new entropy position and tape. Reversing B, if eligible,
restores B's entry values (respectively `c=1`, console=`a5`, or `c=0`,
empty console). A cannot reverse after it is CLOSED. The same launch
conflict applies while A is FAILED, including its retained effect prefix.
For block, A writes previously absent sector 2; a B closure that reads
that block model conflicts until A closes. After unreversed A, retry B
reads all 512 `a5` bytes; after reversed A, it reads 512 zero bytes and
sector 2 remains absent. Present-zero sectors retain their presence.

A run using only the clock and a run using only the console can remain
concurrent if their existing register/memory ownership is also disjoint.
Reversing the clock run restores its clock and own buffers and leaves the
other run's console bytes unchanged. A launch needing clock plus block
while another run owns block acquires neither model: acquisition is atomic.
An effect hidden in an R helper is in the transitive footprint even when
its branch is not taken in this execution. This schedules conflicting
device use across CLOSED boundaries and preserves disjoint concurrency,
all existing sequential programs and the mixed-fat-object path.

The finite contract witness in
[ownership_witness.py](../../../.tmp/sol-notefix-s4/ownership_witness.py)
checks these outcomes and every pair of the eight model subsets. It is
a small model of the proposed ownership rule, not a repeated-launch ABI
implementation. The separate read-only interpreter witness below checks
the actual clock, console, block, entropy and inverse operations.

## Recommended exact spec diff

These are the complete additions to the published 0.9 text, superseding
the first-pass diff. They are not a patch to that unpublished proposal.

Insert after §7.1's Initial state sentence:

```diff
 Initial state: bump = `heap_base`, table = the pre-entries in layout
 order, memory zero except images.
+That state is established once when the program is loaded. These
+persistence rules concern CC/R classical memory, allocation-table entries
+and the bump pointer. These components belong to the loaded program and
+persist across runs. For sequential launches, a new run inherits these
+components from the preceding CLOSED run. Closing a run does not restore
+its entry state. If the preceding run was successfully REVERSED before
+being CLOSED, these classical components have their restored entry values
+(§7.4, §10, T4); quantum-state restoration retains T4's exactness
+hypotheses and error bounds. A FAILED run otherwise leaves its completed
+prefix mutations in place. Register-ledger entries and live register
+identities likewise persist under §3.3; ownership ends at CLOSED, not the
+register lifetime. Unloading and loading a program creates a new program
+instance with initial state; register ids of the old instance are not
+imported into it.
```

Insert immediately after §7.3's device table, before **BLOCK-IMAGE**.
The following paragraph is Muse's requested wording verbatim:

```diff
+Device-model state belongs to the loaded program like classical memory (§7.1): the console byte sequence, the clock counter c and the block sector map are established at load from their initial values (the block map from layout.block_image, K10) and persist across runs, changed only by effect execution and by reversal (§7.4, T4); closing a run does not reinitialise them. The entropy position p is per-run state: it starts at 0 over the entropy tape copied at that bennett_run (§10). The effect tape is per-run.
+The console sequence, clock counter and block sector map are exclusive
+program-state resources subject to the run ownership rules of §10.
```

Append to §10's **States** paragraph, after its final §3.3 reference:

```diff
+Persistence does not relax exclusive ownership of touched registers or
+memory while a run is not CLOSED. Separate loaded program instances have
+separate state; the §7.1/§7.3 program-lifetime state is never reinitialised
+merely to start a run. This persistence rule does not prohibit disjoint
+concurrent runs with disjoint model ownership sets as well as the
+existing register/memory conditions.
+At bennett_run, the run atomically acquires exclusive ownership of every console, clock and block model referenced by its entry's transitive CC/R call closure. Ownership lasts until CLOSED, including while COMPLETED, FAILED or REVERSED. If any required model is owned by another non-CLOSED run, bennett_run returns E_INVALID_STATE before executing the entry or acquiring ownership. Entropy positions and effect tapes remain per-run. Disjoint concurrent runs require disjoint model ownership sets as well as the existing register/memory conditions.
```

The §10 sentence deliberately names only program-lifetime state. §7.3
positively defines the separate per-run entropy and effect-tape lifetimes;
the amendment does not inherit dynamic environments, history or oracle
workspace into later runs. The original witnesses use sequential CLOSED runs. The overlap vectors
now add explicit device ownership; no concurrent memory merge is assumed.

Append to §14.3 T4, retaining its existing reversal eligibility,
quantum exactness/error bounds, audit and observed-event qualifications:

```text
Restoration concerns the run-owned state; state belonging exclusively to disjoint runs is unaffected.
```

Here run-owned state includes the §7.3 models acquired by the transitive
closure at launch; it never includes unrelated native host state.
The §10 restoration wording is read with this same run-owned scope.

Add after the §15 suite table (a suite G requirement):

```diff
+**Suite G — loaded-program lifetime (K-new).** Execute successive CC
+launches A and B in one loaded device program, each CLOSED before the
+next launch. With ptr_width=16, H=16, A_tab=2, S_cells=0, null_size=1,
+heap_base=16, heap_limit_max=16 and global g at base 1, size 1, image 00,
+let A allocate one byte and store 7 in g; let B return g and a new
+one-byte allocation. Without A reversal B returns (7,17), bump=18 and
+table=[(1,1,1,1),(16,1,1,0),(17,1,1,0)]; with successful A reversal
+before close B returns (0,16), bump=17 and
+table=[(1,1,1,1),(16,1,1,0)], in (base,size,live,pinned) order.
+Check every logical byte and table entry. Closing a FAILED A preserves
+its completed stores and allocations unless explicitly reversed.
+Bytes in the following device vector are hexadecimal. Use live, disjoint
+buffers and an initial block image with sector 0 all zero and sector 1
+all ff (512 bytes each), so
+sector 2 is absent. A reads clock 0, writes 512 a5 bytes to sector 2,
+appends a5 to the console and consumes byte 11 from its copied entropy
+tape. B reads the clock and sector 2 and consumes byte 33 from a new
+one-byte entropy tape. After unreversed A, B reads clock 1 and 512 a5
+bytes; after reversed A, B reads clock 0 and 512 zero bytes, with sector
+2 absent. Check sector presence, console persistence/restoration and
+unchanged sectors 0 and 1. In both cases B starts p=0, reads entropy
+byte 33 and has its own three-entry effect tape without A's entries.
+Repeat with A FAILED after its effects, with and without eligible
+reversal. Fresh load restores the initial program state. Check that
+CLOSED releases register ownership without destroying live identities,
+that host-minted tokens remain valid until unload, and that a device-
+minted token passed after its run is CLOSED returns E_ARG.
+**Suite G — overlapping device ownership.** With disjoint live buffers,
+let A read clock 0 and append a5, complete and remain open. A B entry
+whose transitive CC/R closure reads that clock and appends 5a returns
+E_INVALID_STATE at launch; c stays 1, console stays a5, and B has no
+effects or ownership. After A closes unreversed, retry B reads 1 and
+leaves c=2, console=a55a. After eligible A reversal then close, retry B
+reads 0 and leaves c=1, console=5a. While A is REVERSED but not CLOSED,
+B still conflicts; repeat while A is FAILED. Include transitive helper
+effects, a conflicting block read after A creates sector 2, and a launch
+requesting one free and one owned model: no partial acquisition.
+Disjoint clock-only and console-only runs may execute concurrently under
+the existing register/memory rules; reversing either restores its owned
+state and leaves the other's state intact. Check separate entropy
+positions/tapes, all bytes and block presence, not only scalar results.
```

Add to §0.2, assigning the next available K number when applied:

```text
K-new | §7.1, §7.3, §10, §14.3, §15 | LOADED-PROGRAM-LIFETIME: CC/R memory,
allocation table, bump pointer and console/clock/block state persist
across runs in one loaded device instance; entropy position and effect
tape are per-run; referenced console/clock/block models exclusively
owned from launch through CLOSED; CLOSED does not reverse. | b-isa-spec-adg | S | –
```

## Hashes, catalog and consumers

Under the **council-authorized in-version 0.9 K repair**, canonical source,
semantic envelope, target and catalog bytes remain unchanged; no hash
re-pin is needed. A full ISA-version bump would change §9.2 envelopes and
require new pins. This note changes neither `ref-0.9.json` nor expansion
recipes, charges, resources or target capabilities; no catalog check is
claimed here. Published 0.8 text is untouched.

A consumer resetting §7.1 memory or console/clock/block on each run must
separate its load and run lifecycles. The plugin's persistent qreg table
needs no redesign. Bindings/certificates replaying a later entry must
record its actual device entry-state/preparation assumptions; one fresh
load does not establish coverage of all histories. Entropy buffers remain
copied at launch; tape access remains associated with the particular run.
Existing `E_ARG` and `E_INVALID_STATE` suffice; no status number is added.

### Accepted bennett-4ht statement (verbatim)

In a mixed fat object, 'loaded program' means a loaded device program instance, not the native host process or entire fat binary. The native host may retain that instance and repeatedly invoke its device CC entries; the specified memory, allocation-table, bump-pointer and register-ledger persistence applies to that instance, with separate state for separate loaded instances. Loading a device program or closing or reversing a device run does not initialize or roll back unrelated native host state. This rule does not require moving native main, argv/envp handling or host-only libc into the device object. Later-entry certificate replay records the actual device entry-state preparation assumptions, without presuming a fresh native process.

That is the adg paragraph accepted in
[the round-2 4ht dossier](../../../../bennett/docs/council/accept-4ht-recheck-2026-11-02/round-2/doc.md).
The new console/clock/block rule has the same device-instance scope;
its per-run tapes cover device R effects, not unrelated native host I/O.
The ordinary native host binary and only marked device modules plus their
linked device closures remain reachable (North Star §§2, 3.3, 4.4).

The [shared fat-object scope](../2026-11-02-rev2/fat-object-scope.md) supplies
the remaining bennett-4ht publication obligations: a versioned
container-to-device-object/root/certificate inventory, native-call to device
entry bindings, budget and opaque-handle lifetime negotiation, and
device-run/tape association with effect-proxy ordering and replay. A general
host-memory-by-reference ABI must also specify address/layout mapping,
range/liveness, aliasing, ownership/synchronization, writeback and reversal.
The current copied-argument/hostcall ABI does not supply those mechanics.
They remain explicit boundary work, never grounds to require whole-binary
lowering or omit mixed execution. Certificates and native comparison retain
the selected materialised device closure as their subject.

## Read-only interpreter witness and reproduction

The public reference `ClassicalMachine` creates initial memory/devices in
its constructor; the CLI's `run_program` is explicitly one-shot. There is
no public API for transferring all program-owned state to a second run.
Thus the following **executed instruction/reversal witness** checks the
device primitives and their observable values, not a multi-launch ABI.
The cross-launch CLOSED transitions, separate tapes while retaining
devices, ownership and token vectors remain explicit suite G obligations.

The harness builds an ISA 0.9 object, computes and checks every interface
hash, and invokes the unmodified library through a job-local Cargo package.
`keep` calls A then executes B's operations in the same run. `undo` first
uncalls A, then executes B. Their one copied entropy tape is `[11,22]`:
B reads `22` without uncall and `11` with uncall, as it must **within one
run**. A fresh B-only machine supplied `[33]` reads `33` at position 0.
This intentionally differs from the two-launch vector's B entropy `33`
and separate three-entry tape. No reset or fake close is inserted into
the reference machine.

Both completed and FAILED A are also executed and whole-run reversed.
Complete snapshot equality checks memory, device state (including sector
presence), ledger, control, dynamic instances and fault/result state; the
initialized block map includes the present-zero sector. It does not inspect
retained audit-history layout or establish cross-run ledger/token lifetimes.
`keep` and `undo` check all 512 read bytes and tape counts, then verify
whole-run restoration too.

```rust
use bennett_isa_ref::{json::Json, ClassicalMachine, ClassicalValue, Object};
use std::collections::BTreeMap;

fn json(s: &str) -> Json { Json::parse(s).unwrap() }

fn object() -> Object {
    let a = "fn r @a () () () () ()\n^entry():\n\
        s = const.i16 16\np = inttoptr s\n\
        k = const.i16 1040\nc = inttoptr k\n\
        e = const.i16 1048\nep = inttoptr e\n\
        sector = const.i64 2\none = const.i16 1\n\
        effect clock.read c\neffect block.write sector p\n\
        effect console.write p one\neffect entropy.read ep one\nret";
    let b = "k = const.i16 1040\nc = inttoptr k\n\
        d = const.i16 528\ndp = inttoptr d\n\
        e = const.i16 1048\nep = inttoptr e\n\
        sector = const.i64 2\none = const.i16 1\n\
        effect clock.read c\neffect block.read sector dp\n\
        effect entropy.read ep one\n\
        cv = load.i64 c\nbv = load.i8 dp\nev = load.i8 ep\nret cv bv ev";
    let mut functions = vec![
        ("a", a.to_string()),
        ("failed", a.replace("@a ", "@failed ").replace("\nret", "\nfault 2")),
        ("b", format!("fn r @b () (cv:i64, bv:i8, ev:i8) () () ()\n^entry():\n{b}")),
    ];
    for (name, prefix) in [
        ("keep", "call @a\n"),
        ("undo", "call @a\nuncall @a () ()\n"),
        ("read", ""),
    ] {
        functions.push((name, format!(
            "fn cc @{name} () (cv:i64, bv:i8, ev:i8) () () ()\n^entry():\n{prefix}(cv, bv, ev) = call @b\nret cv bv ev"
        )));
    }
    let data = [
        ("src", "a5".repeat(512)), ("dst", "00".repeat(512)),
        ("clk", "00".repeat(8)), ("ent", "00".to_string()),
        ("disk", format!("{}{}", "00".repeat(512), "ff".repeat(512))),
    ];
    let mut symbols = BTreeMap::new();
    for (name, body) in &functions {
        let kind = if body.starts_with("fn r ") { "r" } else { "cc" };
        let results = if matches!(*name, "a" | "failed") { "[]" } else { "[\"i64\",\"i8\",\"i8\"]" };
        let sig = json(&format!(
            r#"{{"abi":"0.9","kind":"{kind}","params":[],"results":{results},"tier":"{kind}"}}"#
        ));
        symbols.insert(symbols.len().to_string(), json(&format!(
            r#"{{"name":"{name}","kind":"{kind}","signature":{},"interface_hash":"{}"}}"#,
            sig.canonical(), "0".repeat(64)
        )));
    }
    for (name, hex) in &data {
        symbols.insert(symbols.len().to_string(), json(&format!(
            r#"{{"name":"{name}","kind":"data","signature":{{"abi":"0.9","kind":"data","size":{},"tier":"-"}},"interface_hash":"{}"}}"#,
            hex.len()/2, "0".repeat(64)
        )));
    }
    let tail = r#"
section devices
{"models":{"block":{"version":"0.9"},"clock":{"version":"0.9"},"console":{"version":"0.9"},"entropy":{"version":"0.9"}},"services":{}}

section layout
{"A_tab":3,"H":12,"S_cells":0,"block_image":"disk","globals":{"src":{"base":16,"size":512,"image":"src"},"dst":{"base":528,"size":512,"image":"dst"},"clk":{"base":1040,"size":8,"image":"clk"},"ent":{"base":1048,"size":1,"image":"ent"}},"heap_base":2048,"heap_limit_max":64,"interface_regions":{},"null_size":1,"ptr_width":16}
"#;
    let render = |symbols: BTreeMap<String, Json>| {
        let mut text = format!(
            "bennett-object isa=0.9 object=0.9 launch=0.9 sched=0.9 cert=0.9 coverage=0.9 target=0.9 ptr_width=16\n\nsection symbols\n{}\n\nsection functions\n",
            Json::Object(symbols).canonical()
        );
        for (_, body) in &functions { text.push_str(&format!("{body}\n")); }
        text.push_str("\nsection data\n");
        for (name, hex) in &data { text.push_str(&format!("{name} {hex}\n")); }
        for line in tail.lines() {
            let line = if line.starts_with('{') { json(line).canonical() } else { line.into() };
            text.push_str(&format!("{line}\n"));
        }
        text
    };
    let parsed = Object::parse(&render(symbols.clone())).unwrap();
    let hashes = parsed.identity().unwrap().interface_hashes;
    for symbol in symbols.values_mut() {
        let name = symbol.get("name").unwrap().string().unwrap().to_string();
        let Json::Object(fields) = symbol else { panic!("symbol is not an object") };
        fields.insert("interface_hash".into(), Json::String(hashes[&name].clone()));
    }
    let object = Object::parse(&render(symbols)).unwrap();
    object.check_hashes().unwrap();
    object
}

fn main() {
    let o = object();
    for (name, fault) in [("a", None), ("failed", Some(2))] {
        let mut m = ClassicalMachine::new(&o, name, &[], &[0x11]).unwrap();
        let entry = m.snapshot();
        let outcome = m.run(100).unwrap();
        assert_eq!(outcome.fault, fault);
        assert!(!m.is_running());
        assert_eq!(m.clock(), 1);
        assert_eq!(m.console(), &[0xa5]);
        assert_eq!(m.effect_tape_len(), 4);
        assert_eq!(&*m.effect_tape()[0].bytes, &[0; 8]);
        assert_eq!(&*m.effect_tape()[1].bytes, &[0xa5; 512]);
        assert_eq!(&*m.effect_tape()[3].bytes, &[0x11]);
        m.reverse().unwrap();
        assert_eq!(m.snapshot(), entry, "complete restoration of {name}");
        println!("{name}: clock=1 console=a5 tape=4; reverse=entry");
    }
    for (name, entropy, clock, byte, ent, tape, console) in [
        ("keep", vec![0x11,0x22], 1, 0xa5, 0x22, 7, vec![0xa5]),
        ("undo", vec![0x11,0x22], 0, 0, 0x11, 3, vec![]),
        ("read", vec![0x33], 0, 0, 0x33, 3, vec![]),
    ] {
        let mut m = ClassicalMachine::new(&o, name, &[], &entropy).unwrap();
        let entry = m.snapshot();
        let out = m.run(100).unwrap();
        assert_eq!(out.fault, None);
        assert!(!m.is_running());
        assert_eq!(&*out.values, &[
            ClassicalValue::Int(64,clock), ClassicalValue::Int(8,byte),
            ClassicalValue::Int(8,ent),
        ]);
        assert_eq!(m.memory_bytes(528,512).unwrap(), vec![byte as u8;512]);
        assert_eq!(m.clock() as u128, clock+1);
        assert_eq!(m.console(), console.as_slice());
        assert_eq!(m.effect_tape_len(), tape);
        assert_eq!(&*m.effect_tape()[tape-1].bytes, &[ent as u8]);
        m.reverse().unwrap();
        assert_eq!(m.snapshot(), entry, "complete restoration of {name}");
        println!("{name}: ({clock},{byte},{ent}) block=512 checked bytes tape={tape}; reverse=entry");
    }
}
```

Run this exact command from any directory. All generated files and Cargo
outputs stay under `.tmp/sol-notefix-s4/`; the dependency source is read-only.
There are four Cargo jobs, a 4 GiB per-process address-space bound (in
addition to the runner's 14 GiB scope), no core dumps and a 240-second
timeout. This is one small witness executable, not a repository gate.

```sh
env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER \
  TMPDIR=/home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/tmp \
  CARGO_TARGET_DIR=/home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/target \
  python3 - <<'PY'
import os, pathlib, resource, subprocess
repo = pathlib.Path('/home/tobias/Projects/bennett-workspace/bennett-isa-spec')
job = repo / '.tmp/sol-notefix-s4'
(job / 'tmp').mkdir(parents=True, exist_ok=True)
crate = job / 'witness'
(crate / 'src').mkdir(parents=True, exist_ok=True)
note = (repo / 'docs/notes/2026-11-03-notefix/adg.md').read_text()
(crate / 'src/main.rs').write_text(note.split('```rust\n', 1)[1].split('\n```', 1)[0] + '\n')
(crate / 'Cargo.toml').write_text('''[package]
name = "adg-device-witness"
version = "0.0.0"
edition = "2021"
[workspace]
[dependencies]
bennett-isa-ref = { path = "../../../reference-interpreter" }
[profile.dev]
debug = 0
incremental = false
codegen-units = 4
''')
resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3,) * 2)
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
subprocess.run(['timeout', '240s', 'cargo', 'run', '--offline',
                '--manifest-path', str(crate / 'Cargo.toml'), '--bin', 'adg-device-witness', '-j4', '--quiet'], check=True)
PY
```

Expected stdout (the verification result below records whether reproduced):

```text
a: clock=1 console=a5 tape=4; reverse=entry
failed: clock=1 console=a5 tape=4; reverse=entry
keep: (1,165,34) block=512 checked bytes tape=7; reverse=entry
undo: (0,0,17) block=512 checked bytes tape=3; reverse=entry
read: (0,0,51) block=512 checked bytes tape=3; reverse=entry
```

Verification result: the exact bounded command above exited **0** and
reproduced all five stdout lines. Every assertion passed, including full
512-byte comparisons and complete entry-snapshot restoration for all five
cases. The reference interpreter and conformance sources were not edited.
No full gate or actual repeated-launch ABI test was run.

The bounded document self-check also passed: Muse's §7.3 paragraph and the
accepted 4ht statement match verbatim, §10 has the scoped lifetime phrase,
the citation is corrected, all four spec insertions apply at their stated
anchors in an in-memory dry run, fences balance and all six links resolve.

## Additional conformance obligations

At publication, suite G must exercise the **actual** two-launch sequences
above, comparing complete memory/table/bump, ledger and device state,
token validity and run-associated tapes. An executed `qreg.from_id` of
another open run's register produces terminal fault code 4; supplying that
register as a conflicting host launch argument returns `E_INVALID_STATE`
before effects. After A is CLOSED, its stored live id can be recovered by
`qreg.from_id` in B. A device-minted token passed after A is CLOSED returns
`E_ARG`; a host-minted token remains valid until unload. Separate loaded
instances have separate state. A native host invoking a retained device
instance must also check that device reversal leaves unrelated host state
unchanged. These vectors are requirements, not tests claimed to have run
through the current one-shot interpreter.

## Round-2 blocking items and resolution

The [round-2 report](../../../../bennett/docs/council/contract-adg-2026-11-02/round-2/report.md)
and both reviewer outputs agree on the device-ownership defect. This
revision adopts the complete launch-time rule verbatim from sol's
adg-R2-B1 fix, which also resolves codex's adg-R2-1. These are proposed
resolutions pending round 3 and a Muse seat.

| Item | Resolution and witness |
|---|---|
| adg-R2-1 / adg-R2-B1 | §§7.3/10 exclusively acquire every referenced console/clock/block model atomically at launch through CLOSED, including COMPLETED, FAILED and REVERSED. Conflict returns E_INVALID_STATE before effects or any acquisition. The clock/console overlap now blocks B before A reverses, preserving A's entry state. |
| T4 interaction | §14.3 restores run-owned state; disjoint runs' state is unaffected. The clock-only/console-only concurrent witness exercises this distinction. |
| Required §15 vectors | Both clock and console retry outcomes, block presence, FAILED/REVERSED retention, transitive helper footprint, no partial acquisition and independent entropy/tapes are specified. |

All other round-2 content is retained, including the exact Muse adg-M1
paragraph, accepted bennett-4ht paragraph, memory/allocator/token rules,
sequential device vectors and interpreter witness source. Only the
ownership/T4/vector additions, their necessary explanatory wording and
job-local reproduction paths change. No unrelated suggestion is applied.

## Muse blocking items and resolution

| Review item | Resolution in this proposal | Evidence / remaining validation |
|---|---|---|
| **adg-M1 (core), §7.3 lifetime missing** | Add Muse's paragraph verbatim after the device table: console/clock/block established at load and persistent; `p=0` and effect tape per run. | Concrete two-launch vector: B clock 1 / sector a5 without A reversal; clock 0 / absent sector 2 and 512 zero bytes with reversal. Real interpreter effects and complete reversal are checked by the bounded witness; actual multi-launch API conformance remains to implement. |
| **adg-M1 (core), §10 initialization too broad** | Replace the original unqualified phrase with “the §7.1/§7.3 program-lifetime state is never reinitialised merely to start a run”. | B's new one-byte tape `[33]` always yields `33` at `p=0`, and B owns exactly three effects. The within-run harness explicitly retains its cursor, distinguishing run boundaries from calls. |
| **adg-M1 required conformance vectors** | Add the clock/block vectors to §15 suite G, including reversal, FAILED-prefix retention, present-zero versus absent sectors, console and independent entropy/tapes. | Exact full byte patterns and state transitions are specified above; no lifecycle implementation pass is inferred from a scalar assignment or one-shot execution. |
| **adg-4HT-1, previously resolved** | Preserve the accepted paragraph verbatim in “Hashes, catalog and consumers”; extend the same instance scope to the new devices. | Native host binary, marked device modules, later-entry replay and unrelated host state remain separated as in the accepted re-check and shared scope. |
| **Round-1 citation correction** | Attribute program scope to §3.3; §3.2 only lists machine state. | Corrected in the defect paragraph and the complete spec diff. |

Muse's `suggestions` array is empty; its report's S1/S2 items address
z4c, 5u3 or checker-diagnostics, not adg. There is no unaddressed adg S1.
The source is
[out-muse.json](../../../../bennett/docs/council/accept-muse-batch-2026-11-02/round-1/out-muse.json)
and its [report](../../../../bennett/docs/council/accept-muse-batch-2026-11-02/round-1/report.md).
Round-1 optional refinements are also retained here: explicit T4 quantum
qualifications, full scalar table states, free/table-capacity boundary,
token/ownership distinctions and the in-version hash condition.

## Release and after acceptance

Recommend a **0.9 K wording repair to §§7.1, 7.3 and 10**, with the §15
lifecycle vectors. The core change must return to sol and astra and then a
later Muse seat, as the convenor requires. Once accepted and authorized,
the spec editor assigns the K number, applies the complete additions plus
the accepted 4ht statement, and regenerates the relevant indexes/diffs.
Reference/VM owners then implement and test repeated-launch lifetimes;
the dialect updates its cross-reference. Keep `b-isa-spec-adg` open until
the contract decision and its required follow-through land. `bennett-4ht`
continues to track the mixed-launch boundary. No full gates, spec edits,
interpreter changes, commits or remote operations are part of this job.

## Ownership revision verification and council follow-through

`timeout 30s python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/check_notes.py adg`
checks the exact reviewer wording, preserved adg-M1/4ht bytes, T4 and
§15 insertions, complete original Rust witness and links. The finite
ownership model command is
`timeout 30s python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/ownership_witness.py`.
Both exited 0. The job-local interpreter build reproduced the five
recorded stdout lines with complete machine-snapshot restoration; see
`timeout 300s python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/run_witnesses.py`.
The interpreter has no multi-launch ownership API, so the overlap rule
has finite-model evidence and required suite G vectors, not an actual
multi-launch implementation pass. No full repository gate was run.

Open council work is acceptance of the launch-time ownership rule in
adg round 3, then a Muse seat; publication and actual ABI conformance
follow. The existing adg and bennett-4ht obligations remain open. This
revision makes no new contract choice beyond the reviewers' requested
ownership repair and reserves no K number.

---

## Dossier part: pe1 (RE-SEAT. run derive3-pe1-2026-11-02; accepted by sol, codex (astra) in round 1; your batch-2 seat (accept-muse-batch2-2026-11-02 round 1) blocked it on pe1-M1 (the §0.2 K67 ledger row still says 25-bit / 1/33554432); this revision adds exactly your pe1-M1 replacement text and nothing else; convenor ruling: no further sol+astra round because the change is your verbatim text; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-03-notefix/pe1.md)

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

## Muse blocking items and resolution

**pe1-M1 — §0.2 K67 ledger row.** This revision adds exactly one
spec edit to the original proposal: replace K67's witness sentence in
the same erratum as the existing §12.1 repair. Nothing else changes;
every byte of the original note above is retained. This is a proposed
resolution, pending the Muse re-seat or the convenor's ruling that the
verbatim replacement suffices; it is not a new acceptance verdict.

The replacement text copied verbatim from
[Muse pe1-M1](../../../../bennett/docs/council/accept-muse-batch2-2026-11-02/round-1/out-muse.json)
is:

```text
LEGAL-REPLAY-WITNESS. F=4 and W=8 with legal unused mapping give a 24-bit domain; witness: four singleton draws cover 1/16777216 with unchanged XOR outcomes.
```

Checked against the current published §0.2 K67 row at **line 203**, the
line cited by Muse. These are the complete before/after UTF-8 row bytes,
excluding the terminating LF; retain all other columns and dependency
markers. The old bold label becomes the exact plain label Muse supplied.

```diff
-| K67 | §12.1 | **LEGAL-REPLAY-WITNESS**. F=4 and W=8 with legal unused mapping give a 25-bit domain; witness: four singleton draws cover 1/33554432 with unchanged XOR outcomes. [deps: ISA-5.4, ISA-7.1, ISA-7.2, ISA-12.1-P8, ISA-12.2] | COD S03 | E | – |
+| K67 | §12.1 | LEGAL-REPLAY-WITNESS. F=4 and W=8 with legal unused mapping give a 24-bit domain; witness: four singleton draws cover 1/16777216 with unchanged XOR outcomes. [deps: ISA-5.4, ISA-7.1, ISA-7.2, ISA-12.1-P8, ISA-12.2] | COD S03 | E | – |
```

Before row SHA-256: `ad71cdb6cdfbf9b2b56b0aeaa9f65dea6173df80d92cd208f9fac94152a552c3`.
After row SHA-256: `c020b85859bb1ade45b2d47ad24c956a791b85d9372ed08d50b5338267fb8a5b`.
The numeric substitutions are ASCII `25-bit` → `24-bit` and
`1/33554432` → `1/16777216`; the XOR outcomes are unchanged.

The focused check applies the original §12.1 edits and this new row edit
to an in-memory copy of the published text. It checks all six tuple
repairs, empty borrowed widths, the 24-bit count and singleton fraction,
and requires no remaining `25-bit` or `33554432` occurrence in that copy.
The on-disk spec is unchanged. The four draws of the singleton consume
no random words and have one distinct tuple. This does not publish the
complete bound 2-bit-layout certificate requested by the original note;
that remains a conformance publication obligation.

Verification: `timeout 30s python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/check_notes.py pe1`
exited 0 with the pe1 PASS line. The inherited `INDEX.md` references
above refer to [the originating INDEX](../2026-11-02-derive3/INDEX.md);
the original note's historical test report is retained, not reclassified
as a fresh interpreter or full-repository test.

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
