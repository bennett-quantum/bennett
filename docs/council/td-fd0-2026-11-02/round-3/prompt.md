# Council

You are a member of a two-model council (sol, astra) grading the document below, fd0 target/cert 0.10 import and hierarchical-estimate text, round 3 revision resolving R2-1 (sol-rev4). This is ROUND 3: the document is a full, self-contained revised proposal (docs/notes/2026-11-02-rev4/ in bennett-isa-spec) that supersedes the round-1 note (round-1 snapshot: `../bennett/docs/council/td-fd0-2026-11-02/round-1/doc.md`; the round-2 snapshot it revises is `../bennett/docs/council/td-fd0-2026-11-02/round-2/doc.md`; member outputs beside it). Its section "Round-1 blocking items and resolution" (and any round-2 section) is the editor's response; its mixed-fat-object section cites the shared scoping statement `docs/notes/2026-11-02-rev2/fat-object-scope.md` (in bennett-isa-spec; also attached below) and answers the rubric's standing check. The document is the second derivation for bead b-isa-spec-fd0 (imported QEC models, parameters and hierarchical estimates). Unlike the first-pass note `docs/notes/2026-11-02-contract-fd0.md` (read it; it states the defect and alternatives), this note proposes field-level normative text for **target/certificate 0.10**, a full-version publication, and does not amend 0.9. Grade the proposed normative text (its §8.5 and §12.3 insertions), the worked serialized import, the conformance vectors and the consumer/release analysis, against the rubric on the absolute scale. ISA 0.9 is accepted text and is not under review, except where the proposal interacts with it. Be exacting and skeptical. Verify every technical premise against your own knowledge and against the actual spec text. Name any premise that is false, including a misquoted or misnumbered clause.

You run read-only in `bennett-isa-spec`. The normative text the diff amends is `spec/Bennett-ISA-Spec-0.9.md`. It is NOT attached because of its size. Read the clauses the note cites, and every clause the diff touches, before grading. Other files you can read:
- `docs/notes/2026-11-02-contract-fd0.md` is the first-pass derivation (also attached below); `docs/notes/2026-11-02-textdefects/` holds this note; `docs/notes/2026-11-02-contract-verification.md` is the first pass's verification index.
- `reference-interpreter/` is the reference interpreter.
- `.beads/issues.jsonl` holds the beads the notes cite.
- `../bennett/docs/Bennett-NorthStar.md` is the north star, also attached below.
- `../bennett/docs/council/` holds earlier council rounds, including `isa-09-k82-2026-11-01` (K82).

A blocking issue is one that would make the project build the wrong thing if the diff were applied as written, or if it were left unapplied while the note's defect is real. Everything else is a suggestion. Return `accept` only if the blocking list is empty. `accept` means that the editor may adopt this text (with your suggestions at their discretion) as the fd0 section of target/cert 0.10. Also grade the route: deferring to 0.10 may postpone mechanics only (rule 10 of the north star policy); if routing fd0 to 0.10 removes, refuses or makes inert a capability that 0.9 users must have now (resource estimates for the north star's demo ladder), that is blocking, and the fix must say what 0.9 must state in the meantime.

Be constructive, always. The editor must be able to act on your output without asking you anything. For every blocking issue, the `fix` field must give:
- the section;
- the sentence or rule the diff should state (write it out);
- where an example is involved, the corrected example or expected value.

Each blocking item carries either `steps` (step 1 the spec clause, a later step a reproducible witness) or a precise `problem`, and a `kind`: `implementation` when the note's diff is wrong, `spec-gap` when the spec is silent in a way the note does not repair. Where two viable ways out exist, name both and say which you would take. Every `suggestions` entry and every criterion's `change` field follows the same rule. In `path_to_accept`, state the minimal ordered set of changes that would make you return `accept`. If you already accept, say what would raise the lowest-scoring criterion by one point.

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
3. This is round 3. Fill `previous_status` for every blocking issue of round 2 (listed under "Previous round" below, from both members, by id) with resolved | partially | unresolved | regressed and a one-line note. List in `regressions` anything that was correct in the round-2 snapshot and is wrong now. Re-raise a round-2 item in `blocking` only if it is not resolved; then re-read the whole document for new S0 issues, including the bennett-4ht standing check.
4. Give `verdict_core` (accept/revise/reject) for the core scope alone, and `verdict` for the whole proposal.
5. Check hash and catalog claims: if the note says no canonical bytes or hashes change, verify that the diff really leaves them unchanged. If they do change, the note must say so and say how consumers move.
6. Formal correctness is pursued after practical revisions: correct *statements* with explicit hypotheses are required, proofs are not. Demands for proof formats, mechanisation or checker algorithms are S1 as long as the obligation and a default procedure are stated.


Blocking items: `steps` are optional; use them (3 to 6 objects {"n": "<1>1", "claim": "...", "by": "..."}) for implementation findings with a reproducible witness, else give a free-text `problem`; leave the other empty.
Steps: <1>1 what the spec requires (`by`: `clause:<ID>` or `ASSUMED: <why the spec is silent>`); <1>2 what the implementation does (`witness:<path or command>`); <1>3 an input where they differ; last step cites earlier ones (`step:<1>1`).
`OPEN: <what is missing>` marks an unjustified step; several `by` parts are separated by `; `.
If the spec is silent (step 1 or `problem` begins `ASSUMED:`) set `kind` to `spec-gap` (otherwise `implementation`); a spec gap goes to the spec owner,
is not an editor blocker and does not count against `accept`.


# Previous round (2)

Verdicts: sol: revise, codex: accept

Blocking issues raised last round:
- [sol] R2-1 (§8.5 Objective input binding; inherited §§10–10.1 default launch-estimate contract): <1>1 Launch estimates support every well-typed resolved argument vector, use §11 defaults when no embedded schedule matches, and return an explicit effective schedule even for a default-only realisation. (clause:ISA 0.9 §10.1 Resolved request and Certificate binding, inherited by the proposed full-version publication) <1>2 The new rule requires ModelInputs in schedule.bindings whenever the target objective has model-resource terms. Missing required inputs permit no completed concrete schedule. The only new input transport is a setter on bennett_sched_request_t; bennett_estimate_run has no such input, and no default-estimate exception is stated. (witness:docs/notes/2026-11-02-rev2/fd0.md:156; witness:docs/notes/2026-11-02-rev2/fd0.md:193; clause:ISA 0.9 §10, bennett_estimate_run signature) <1>3 Use the worked resolved surface target with objective weighted model_cycle:1 and selector {model:"surface",node:"algorithm",metric:"duration"}. Request an otherwise supported launch estimate with no matching embedded schedule. Its operational fields are concrete, but the launch request cannot supply the required ModelInput. Legal explicit N=1 and N=3 inputs would select respectively 3/100000000 and 9/100000000 seconds. (witness:docs/notes/2026-11-02-rev2/fd0.md, Worked serialized import; witness:spec/Bennett-ISA-Spec-0.9.md:2283) <1>4 The inherited obligation requires a default-schedule estimate, while the new binding rule prohibits completing that schedule without an input this request cannot carry. Returning incomplete-model-objective and returning the required default estimate are conflicting obligations. This needs a semantic request/default decision, beyond C-header enumeration. (step:<1>1; step:<1>2; step:<1>3) Fix proposed: In §10.1 add: “A launch 0.10 estimate request additionally carries model_inputs JCS bytes governed by §8.5. The implementation MUST copy and validate them. A default-only effective schedule MUST serialize exactly those inputs in bindings.model_inputs. An embedded schedule is applicable only when its ModelInputs also match the request after JCS. Every complete, well-typed resolved request, including its required ModelInputs, MUST be supported. Missing required ModelInputs produce incomplete-model-objective before an estimate is returned; no parameter or reservation is inferred.” Expose these bytes through a versioned launch-estimate request or bennett_estimate_run_with_model_inputs, and update §10.1's completeness statement accordingly. Add vectors: supplied N=3 → model objective 9/100000000 seconds and a schedule hash covering that input; supplied N=1 → 3/100000000 and a distinct hash; missing required input → incomplete-model-objective; conflicting embedded input → use a correctly bound default schedule. Alternatively, explicitly exempt non-optimizing §10.1 scheduled-leaf estimates from the ModelInput requirement, retaining their complete §8.2 rows and checked certificate while leaving model objectives unresolved. I recommend explicit launch input transport. The ordinary scalar 0.9 API and its required demo estimates remain unchanged.

## Editor's response (what changed, what was declined and why)

(no response recorded)

Re-grade the revised document below from scratch on the absolute scale. For each blocking issue above, state in your summary whether it is resolved; re-raise it in `blocking` only if it is not.


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


# Background (not graded): `2026-11-02-contract-fd0.md`

# fd0 — imported QEC models, parameters and hierarchy

Proposal for council review; `b-isa-spec-fd0`, originating at
`b-targets-gyp`. No published target or spec bytes are edited.

## Defect and North Star scope

ISA 0.9 §8.3 imports maps a model quantity to `[resource,factor]`.
§8.1 has a closed expression language and binds no code distance,
hardware parameter or imported quantity. §8.2 aggregates scheduled leaf
events, not a factory hierarchy or a symbolic algorithm call graph.
There is no binding rule from an imported QEC formula to a logical gate's
time or qubit class. A numeric mapping is implemented by the supplied
bead's account; it does not supply these missing semantics.

North Star §7, **Qualtran, Azure RE**, promises symbolic hierarchical
counting and imported models as target data. §4.3 requires all declared
resources with their own units. This is an S0 contract scope gap for that
import capability, rather than permission to reject such algorithms.
Scalar materialisation is an available 0.9 path for a completely bound
instance; it is not the full symbolic contract. Keep fd0 as the explicit
blocker for that missing contract, even if the new encoding is 0.10.

Primary evidence: Microsoft's [QEC architecture model example](https://quantum.microsoft.com/en-us/insights/blogs/resource-estimation/modeling-quantum-architecture-with-azure-quantum-resource-estimator)
uses code distance and hardware timing in its cycle formula. Qualtran's
own [call graph protocol](https://qualtran.readthedocs.io/en/latest/resource_counting/call_graph.html)
admits symbolic multiplicities. Its [release notes](https://github.com/quantumlib/Qualtran/releases)
say AlgorithmSummary was removed in favor of GateCounts; adapters must pin
the input format/version, not assume the old class is current. These
sources were read as model-format evidence, not imported code.

## Alternatives and worked example

Use a declared odd code distance d=5, hardware measurement time τ=2 ns,
and **illustrative** formulas chosen for this witness:
`cycle=3τd`, `physical=2d²`, `logical_risk=(1/10)*(1/100)^((d+1)/2)`.
The results are 30 ns, 50 physical qubits per logical qubit and 1/10^7.
The first expression can be numerically precomputed; it cannot reference
d in current §8.1. The risk expression needs exponentiation. It is a
physical-model risk, not a bound on phase-sensitive operator norm.

For three sequential cycles with one logical qubit, the model gives
90 ns, peak 50 physical qubits and occupancy 4500 physical-qubit·ns.
For three simultaneous independent logical qubits held for one cycle,
time is 30 ns and peak is 150, with the same occupancy. Adding all scalar
quantities would get the parallel time or sequential peak wrong.

| Alternative | Assessment |
|---|---|
| Bind d and hardware externally; emit a scalar 0.9 target | Sound concrete compatibility path; retain the original model and bindings in provenance. No symbolic selection or hierarchy is represented in the target. |
| Add parameters and formulas only | Solves evaluation, but not where a formula is consumed, hierarchical multiplicities, concurrency or double counting. Insufficient alone. |
| Bound target model plus separate hierarchical estimate (recommended) | Fix hardware/model choices in target identity; bind symbolic algorithm inputs and model accounting to the certificate; retain §8.2 leaf accounting separately. |
| Treat failure probability as gate epsilon or sum every quantity | Unsound error semantics or wrong units/aggregation. |

## Recommended exact spec diff

For the extended target/cert version, add §8.5 and a corresponding K entry:

```text
8.5 Imported model bindings
A target MAY contain model_parameters:{name:{value:number|null,unit:string}}
and each imports entry MAY additionally contain
{source_hash, source_format, parameters:{name:expr},
 quantities:{name:{unit,expr}}, bindings:{destination:quantity_name}}.
source_hash is SHA-256 of the source model's canonical bytes; source_format
includes a format version. References {param:name} resolve model_parameters;
{quantity:name} resolves a quantity of this model. Dependencies form a DAG;
cycles, duplicate definitions and undeclared references are invalid.
Formula expressions add pow(base,exponent) for integer exponents and
sqrt(x) for the nonnegative principal root, in model context only.
Rational operations and integer powers are exact; roots are exact
algebraic quantities, converted to a reported decimal only with a stated
outward bound. Division by zero, negative roots and nonfinite concrete
outputs are errors. No eps or accuracy-bucket variable is bound here.
Integer parameters declare their integer constraint; a code-distance
parameter additionally declares its permitted parity/range.
A null parameter is symbolic: an estimate retains it as a free parameter.
It MUST be bound before concrete target scheduling or numeric evaluation,
and every concrete binding is included in the resolved target's bytes.
Only an explicit bindings entry may substitute a model quantity for a
gate cost, class quantity or other target numeric field. Its destination
must name a schema-defined numeric field and have matching units and a
valid value. Do not infer bindings from vendor quantity names.
Unmatched quantities are preserved under new named resources using map
and its unit factor. An imported physical failure-risk quantity is a
separately named model output or additive count charge, never epsilon,
an operator-norm assertion, or an automatic probability composition rule.
```

Add to §12.3 region records:

```text
model_estimates?:[{model_hash,parameters,root, nodes,outputs,verification}]
```

And add this normative paragraph:

```text
A model estimate is a finite DAG of leaf model invocations and composition
nodes {kind:sequence|parallel|repeat,children,count?}. A repeat count is a
nonnegative integer expression. Children have explicit resource units,
duration and live-interval summaries. Sequence shifts each child's time
origin to its predecessor's end; parallel aligns child origins; repeat
concatenates count copies. Count resources sum, time is makespan, and
physical occupancy and peak are computed from the resulting simultaneous
live intervals, summing simultaneous demands. Shared factories require
explicit shared intervals, not duplicated independent children. Symbolic
results retain their DAG until parameters are bound. These reports are
distinct from required §8.2 resources and MUST NOT be added to the same
leaf counts again. The checker verifies model identity, parameter and unit
bindings, multiplicities and composition, recording checked obligations
separately from external-model assumptions. Unsupported symbolic source
expressions remain preserved external model obligations; they do not
invalidate execution of the object or justify an invented numerical
estimate. A concrete requested estimate with an unresolved obligation is
reported unchecked, with the exact expression and missing model support.
```

The external obligation path preserves the full imported artifact and
symbolic report; it does not claim a checked estimate. Concrete adapter
support remains required work under fd0. Code-distance search belongs to
the estimator/scheduler; its selected value is a resolved target binding,
and its search domain/objective/physical assumptions belong in the model
estimate. The target does not silently choose an optimum.

## Hashes, catalog and consumers

Resolved parameters, formulas, input-model identity and bindings change
target_hash. Algorithm-dependent hierarchy changes certificate bytes,
not source closure hashes. No reference catalog leaf needs to change.
Targets, estimator, scheduler and checker must agree on units, exact
evaluation, outward conversion and DAG accounting. Existing count
resources and exact logical-gate epsilon keep their present meanings.
Do not reinterpret a legacy count named failure_probability as a checked
physical-error model.

## Conformance vectors and verification

Check the d=5 example above using rational arithmetic; d=3 gives cycle
18 ns, physical 18 and risk 1/100000. A seconds conversion multiplies
nanoseconds by 1/10^9. Exercise null/bound parameters, odd-distance
validation, forward quantity references, cycles, zero divisors, roots,
incompatible units, unknown binding destinations and a source-hash
mismatch. Test sequence versus parallel peaks, factory sharing and
symbolic repeats. A nonzero risk with exact logical gate epsilon=0 must
leave the logical error bound at zero. The executable arithmetic checks
are in [contract-verification](2026-11-02-contract-verification.md);
no target consumer was executed here.

## Release and after acceptance

Recommend **0.10 target/certificate extension**, with a 0.9 K entry
explicitly recording the blocker and the scalar-instance compatibility
construction. The fd0 proposal in the bead is incomplete without binding
destinations, hierarchy and identity. Do not call imported symbolic models
implemented until those vectors and consumer obligations pass. Council
acceptance precedes schema edits, adapter work and any re-pinning.


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


# The document under review (round 3 snapshot)

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
