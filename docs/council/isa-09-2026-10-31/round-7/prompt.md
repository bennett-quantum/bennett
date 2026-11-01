# Council

You are a member of a three-model council grading the document below, Bennett ISA 0.9 (published), round 7: one-reviewer fix round on passes VI (round-6 response: §5.6 rule 1 own controls, rule 3 canonical D_F, §12.2) and VII (new oracle_invocation binding channel, K77; bead 5xm); K1-K76 otherwise unchanged. Grade it against the rubric on the absolute scale. Be exacting and skeptical: verify every technical premise against your own knowledge and against the ISA specification and north star attached as background; name any that is false. A blocking issue is one that would make the project build the wrong thing if uncorrected; everything else is a suggestion. Return `accept` only if the blocking list is empty.

Be constructive, always: the editor must be able to act on your output without asking you anything. For every blocking issue the `fix` field must give the section, the sentence or rule the document should state (write it), and, where an example is involved, the corrected example or expected value; the `steps` carry the witness (step 1 the spec clause, a later step the reproducible witness) (the quoted text and why it is wrong, or the two readings that diverge). Where two viable ways out exist, name both and say which you would take. Every `suggestions` entry and every criterion's `change` field follows the same rule. In `path_to_accept`, state the minimal ordered set of changes that would make you return `accept`; if you already accept, say what would raise the lowest-scoring criterion by one point.

You may read the repository you are running in (read-only): it is `bennett-dialect-spec`, whose `spec/Bennett-Dialect-Spec.md` is the document (identical to the snapshot below), `spec/bennett_markers.h` its C header, `spec/outline-0.2.md` the ratified outline it was written from (with the maintainer's rulings at its end), `spec/Bennett-Dialect-Spec-0.2.PROGRESS.md` the editor's record of what was verified and what could not yet be (read it: the families it lists as unverifiable are graded on the text, not on executed results), `docs/spikes/` the legality and SQLite spike evidence, `docs/audit/` the narrowing audit of the rejected draft 0.1, and `corpus/` the legality corpus. The ISA specification is at `../bennett-isa-spec/spec/Bennett-ISA-Spec.md` and the north star at `../bennett/docs/Bennett-NorthStar.md`; both are also attached below. Reading is optional; the snapshot below is what you grade.

Answer only with JSON matching the schema.

Convergence rules for this council (read before grading):
1. Blocking means S0 only: two conformant implementations built from the text would compute different results, the semantics is unsound or self-contradictory, a normative decision is missing where one is needed to build, or the document narrows north-star scope (rejects, refuses, faults, declares inert or omits a capability the north star promises, including any rung of its demo ladder, even when disclosed, labelled deferred or given a default; a default only closes an S1 item if it keeps the capability). Tag every blocking issue with `scope` (`core` = machine model, instruction set, regions, validity, memory, formal model, examples; `contract` = targets, objects/identity, launch, scheduling, certificate, coverage, grammar) and `severity` (`S0` as defined; `S1` = an implementer would have to choose, but any choice yields a conformant machine). S1 items belong in `suggestions`, not `blocking`, unless the document fails to state a default for them.
2. Implementation will expose frictions; that is expected and acceptable. Do not block on field-level completeness of C headers, JSON schemas, numerical procedures or encodings when the normative obligation is stated and a default is given; list such gaps as suggestions. Do block on anything that would make an executor compute a different function.
3. Fill `previous_status` for every blocking issue of the previous round (by id) with resolved | partially | unresolved | regressed and a one-line note. List in `regressions` anything that was correct in the previous snapshot and is wrong now.
4. Give `verdict_core` (accept/revise/reject) for the core scope alone, and `verdict` for the whole document. Core consensus is reached when every member returns verdict_core = accept with no core-scoped blocking issue.
5. A diff from the previous snapshot is attached when one exists: confirm fixes there first, then re-read the whole document for new S0 issues.
6. Formal correctness is pursued after practical revisions, by the maintainer's decision: in this phase the specification needs correct *statements* with explicit hypotheses, not proofs. Demands for proof formats, mechanisation, rigorous numerical or SDP witness schemas, or checker algorithms are S1 (suggestions) as long as the obligation and a default procedure are stated. Block only on a statement that is false, unsound or ambiguous.


Blocking items: `steps` are optional; use them (3 to 6 objects {"n": "<1>1", "claim": "...", "by": "..."}) for implementation findings with a reproducible witness, else give a free-text `problem`; leave the other empty.
Steps: <1>1 what the spec requires (`by`: `clause:<ID>` or `ASSUMED: <why the spec is silent>`); <1>2 what the implementation does (`witness:<path or command>`); <1>3 an input where they differ; last step cites earlier ones (`step:<1>1`).
`OPEN: <what is missing>` marks an unjustified step; several `by` parts are separated by `; `.
If the spec is silent (step 1 or `problem` begins `ASSUMED:`) set `kind` to `spec-gap` (otherwise `implementation`); a spec gap goes to the spec owner,
is not an editor blocker and does not count against `accept`.


# Previous round (6)

Verdicts: codex: revise

Blocking issues raised last round:
- [codex] R6-CODEX-1 (§5.6 Entry-state analysis, rule 1; §2 effective control context; §8.3 own versus total controls): <1>1 §5.6 first disables an operation when an “effective control” is known false, then makes an X-family target unknown unless all operands are known. §2 defines the effective control context as active predicates plus inherited controls, and §8.3 distinguishes these from a gate’s own controls. §5.6 forbids a stronger analysis from narrowing D_F. (clause:ISA-5.6 (entry-state rule 1 and opening paragraph); clause:ISA-2-P10; clause:ISA-8.3) <1>2 Use a perm_action with interface t:wire mut and u:wire in, no arguments, bounds or memory, and this complete body after ^entry():
z = qalloc any 1
c = qalloc any 1
ccx z u c
b = qborrow any 1
cx c b
qreturn b
ccx z u c
qfree c
qfree z
The current reference check accepted this object through /dev/stdin, returning status ok. It used the 0.8 header and signature abi under the binding erratum; the probe interface hash was eb30a43722acc6c124c4c4bea0e3649915b964ea4e08806933e96cc4c37581f6 and object hash 64de1ae460626ce409f99b798e654b3c9bf05b3a9d53ded0fdb93a0a416f019c. No file or repository modification was needed. (witness:/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/target/debug/bennett-isa-ref check /dev/stdin; witness:reference-interpreter/src/borrow.rs EntryAnalysis::condition and EntryAnalysis::apply) <1>3 On the literal contextual-control reading, ccx z u c has an empty effective control context. Since u is unknown, not all operands are known, so the rule makes c unknown. At the subsequent single-gate frame, D_F includes c=1,b=0; cx c b sends b to 1. No P′ acting independently of B can satisfy the required identity on B over that domain. The later cleanup does not repair a failed individual frame obligation. (step:<1>1; step:<1>2; clause:ISA-5.6 (Cartesian-product domain and restricted factorisation)) <1>4 The reference tests all controls, including the explicit z operand of ccx. It skips the operation because z=0, retaining c=0, and the frame is identity on its resulting domain {c=0} × {b=0,1}. This explains the observed admission and agrees with the intended known-false transfer, but is stronger than the contextual-control reading of rule 1. (step:<1>2; witness:reference-interpreter/src/borrow.rs EntryAnalysis::condition and EntryAnalysis::apply; clause:ISA-4.4) <1>5 Thus the published control terminology and the aligned reference lead to different D_F and different validity decisions for one finite object. This is an S0 normative admission ambiguity, rather than a choice of proof format or a missing optimisation; both candidate domains conservatively contain the reachable entry state. (step:<1>1; step:<1>3; step:<1>4) Fix proposed: In §5.6 rule 1, replace “An effective control known false disables the operation.” with: “If any control literal is known false, counting the operation’s own controls together with its effective control context, the operation is disabled: preserve all abstract values and record no causal event.” Keep the existing all-operands-known rule after this shortcut. Add the body in step <1>2 as a suite F/frame_domain case with expected acceptance and c=0 at frame entry. The alternative is to restrict the reference shortcut to contextual controls and require this object to fail; I recommend the text repair because it preserves the implemented, sound known-false analysis and the maintainer’s chosen admission boundary.

## Editor's response (what changed, what was declined and why)

# Editor's response after round 6 (codex seat) — passes VI and VII

R6-CODEX-1 (core S0, §5.6 rule 1 own controls vs effective control context): ADOPTED as recommended (pass VI,
commit 44ffea0). Rule 1 now reads: "If any control literal is known false, counting the operation's own controls
together with its effective control context, the operation is disabled: preserve all abstract values and record no
causal event." The reviewer's witness (ccx z u c with z = qalloc, then the cx c b frame) is a frame_domain regression
in the reference interpreter (accepted with c=0 at frame entry; its c=1 variant rejected). The reference already
behaved this way; the text was aligned to it.

S1 (rule 3 canonical D_F under acceleration): ADOPTED verbatim. S1 (§12.2 frame obligation uses D_F, with the
illustration): ADOPTED. S1 (regenerate the 0.9 statement layer): orchestrator's job in bennett-conformance, done after
this round. Pass VI gates: reference 467, conformance 113, witness and catalog check green. (74af3fe records.)

Pass VII (new material, consumer-named gap b-isa-spec-5xm from bennett-vm): oracle catalog calls did not say where the
oracle's invocation token tk binds (§16.2 header groups (in)(tgt)(fault)(mem)(args); K24 actuals in formal order; no
implicit bindings). Reading B adopted: tk is an explicit source-binding channel `oracle_invocation` outside A,
carrying the canonical four-string tuple; consumers MUST supply and validate it before concrete expansion, preserve it
through forwarding, template adapters, nested calls and inverse traversal, and reject missing, ill-typed or
source-inconsistent context. K77 is the only new row. Worked example: the same inc8 closure at B=2 and B=3 in one
expansion (two and three frames; final (x+1,1) from zero target/fault; regression over all 256 inputs with inverse
restoration). Catalog bytes and envelope unchanged; 0.8 untouched. Gates: reference 468, conformance 113. Commits
1d86f00, 4f7e18f, e0bd3a8. Exact normative text: spec/isa-0.9.PROGRESS.md pass VII block.

Nothing declined. Diff attached is round-6 snapshot (pass V) to HEAD e0bd3a8 (passes VI and VII). Material to
scrutinise: §5.6 rule 1 and rule 3, §12.2 addition, §11.1/§16.2 `oracle_invocation` channel and K77.


Re-grade the revised document below from scratch on the absolute scale. For each blocking issue above, state in your summary whether it is resolved; re-raise it in `blocking` only if it is not.


# Rubric

# Vision-document rubric — the council's scale

The rubric the council (`docs/council/README.md`) uses to grade
`Bennett-NorthStar.md`, the from-scratch reboot vision for Bennett. Eight
criteria, each scored 1–5 on an absolute scale, plus blocking issues and a
verdict. Scores are advisory; the maintainer decides.

## What is being graded

A **vision document**, not an implementation. The current Bennett.jl and
BennettVM.jl are declared deprecated as designs; the document describes
what the reboot must become. Grade the vision for being the right vision,
stated so that strangers could build it. Do not deduct for "this does not
exist yet". Do deduct, and block, for a technical premise that is false
(for example a claim about what LLVM permits without a fork), an internal
contradiction, a missing load-bearing piece, or ambition that is incoherent
rather than merely large.

## The standard

The maintainer's standard: **unreasonably ambitious, and right.** The
document should read as the founding document of the abstraction layer
quantum programming has lacked, the way the PTX ISA document, the JVM
specification, or the LLVM language reference read for their domains. The
question for each criterion is whether a hardware vendor, a language
designer, and a compiler engineer could each read this and know what to
build and why it will matter.

- **Scores are absolute**, not on a curve, and never relative to the
  current code.
- **Ambition is a virtue; vagueness is not.** A bold claim stated
  precisely scores; a bold claim that hides a contradiction does not.
- **Skepticism is required.** Verify technical premises against your own
  knowledge of LLVM, Enzyme, PTX, QIR, OpenQASM, MLIR, Catalyst, CUDA-Q,
  Silq, Q#, Quipper, Tower, and the reversible-computing and
  resource-estimation literature. Name the premise if it is wrong.
- **Blocking means blocking.** A blocking issue is one that, uncorrected,
  would make the project build the wrong thing. Everything else is a
  suggestion.

### Scale

- **5:** founding-document quality. Precise, complete for its level,
  premises verified, nothing load-bearing missing, nothing superfluous.
- **4:** right, with one gap a domain expert names at once.
- **3:** a competent plan. Sound but generic; nothing a field would rally
  around.
- **2:** aspirational. Direction is visible, but premises are unexamined or
  key pieces are missing.
- **1:** incoherent, or built on a false premise.

## Criteria

### C1 Ambition and coherence

Is the north star unreasonably ambitious *and* internally coherent? Do the
thesis, the decisions, the architecture, and the demo ladder describe one
thing, or several things stapled together?

### C2 Technical premises

Are the technical claims true? In particular: that the dialect can live in
LLVM IR through sanctioned extension points without a fork (target
extension types, address spaces, intrinsics with attribute-stated legality,
function-granularity adjoint/control, lifetime intrinsics, loop metadata);
that the Enzyme plugin model (optimise, transform, optimise) transfers; that
the GPU offload model fits the taint tiers; that the pass-plugin entry point
and the needed analyses are C++-only; the stated problems with QIR.

### C3 The quantum VM as the revolution

Is the VM articulated as the abstraction layer quantum programming lacks,
with a clear account of what it abstracts (virtual qubits, allocation
classes, bounded dynamic control flow, garbage as a scheduled resource, the
resource vector, the effect tape)? Are the pre-VM-era lessons the right
ones? Is the "circuit model as the bounded specialisation of the VM" claim
sound, and is the padded-to-maximum semantics for loops in superposition
stated honestly?

### C4 Modularity and independence

Is the split into independent repositories right? Are the two contracts
(dialect spec, ISA spec) sufficient for every pair of components to
communicate, and are they the *only* coupling? Could each repository be
replaced by a competitor's implementation of the same spec? Where is a
monolith hiding?

### C5 Universality without forking

Is "any LLVM language, invisibly, with no fork" credible as stated? Are the
costs (optimiser not reversibility-aware, regions must be functions,
per-LLVM-version builds) the real costs, and are any missing? Is the
host/device split the right place for the classical/reversible/quantum
boundary?

### C6 Verifiability and success criteria

Is the demo ladder measurable, ordered, and sufficient to define success?
Is "correct" defined as differential equivalence against native execution
rather than as a reversibility check? Is proof-carrying output and
resource estimation without materialised gates a coherent verification and
cost story?

### C7 Position in the landscape

Does the document understand prior art (QIR, OpenQASM 3, MLIR dialects,
Catalyst, CUDA-Q, Silq, Q#, Quipper, Tower, Qualtran-style resource
estimation, reversible-computing pebbling literature) and state precisely
what is new? Is anything claimed as new that is not? Is anything existing
ignored that should be built on or interoperated with?

### C8 Clarity and completeness as a document

Could the three readers (hardware vendor, language designer, compiler
engineer) each read this and know what to build? Are the open technical
questions the right ones, correctly deferred, and is anything deferred that
is actually load-bearing for the vision?

## What the council returns

Per criterion: a score 1–5, one or two sentences of evidence pointing at
the document's text, and the single change that would most raise the
score.

Then:

- **blocking**: a list (possibly empty) of blocking issues, each with a
  short id, the section it concerns, the problem, and the fix. Blocking
  means the project would build the wrong thing if uncorrected.
- **suggestions**: non-blocking improvements, ranked.
- **verdict**: `accept` (ready as the founding vision, blocking list
  empty), `revise` (right direction, blocking issues to fix), or `reject`
  (wrong direction or false premise at the core).
- **summary**: one paragraph.

Consensus is reached when every member returns `accept` with an empty
blocking list. The loop runs at most three rounds.


# Diff from the previous round's snapshot (unified)

```diff
--- round-6/doc.md
+++ round-7/doc.md
@@ -194,4 +194,5 @@
 | K75 | §12.2 | **UNCHECKED-HOST-LIMIT**. Report host exhaustion separately from labels and rejection without a domain cap; witness: region[63,1] at count 1 remains legal even when one element cannot be stored. [deps: ISA-3.3-P2.S2, ISA-3.3-P19, ISA-12.1-P2, ISA-12.2-P1, ISA-5.6-P2, ISA-14.3-P3, ISA-12.3] | INV-6 gap 12; afu | S | – |
 | K76 | §5.6 | **FRAME-ENTRY-DOMAIN**. Normative constant and causal-adjoint analysis fixes D_F; interface/borrowed components stay independent and full; checker establishes reachable-entry support before restricted T3 factorisation. Witness: CX(0,b) passes, polynomial-only prefix zero does not. | consumer 73y; pass V; SQ 20 | E | – |
+| K77 | §4.7, §11.1, §16.2 | **ORACLE-INVOCATION-CONTEXT**. Explicit typed source-call token context is captured outside the declared argument vector, forwarded through adapters and retained under inverse traversal; each linked oracle construction uses its own tuple. Witness: the same inc8 closure and arguments at B=2 and B=3 in one expansion. | consumer 5xm; pass VII | S | – |
 
 **Decided Q14 (applied 2026-10-29, confirmed 2026-10-30; b-isa-spec-7u6).** Lprocs take explicit
@@ -1020,4 +1021,7 @@
 same bit readings and may also be forwarded in `lift.call`'s classical
 list; token parameters retain their token identity and validity (§5.4).
+The invocation operand `tk` is separate from the callee's declared
+`args`; its explicit catalog context channel is `oracle_invocation`
+(§11.1, K77), including for the lifted calls of §4.2.
 
 ### 4.8 Opcode table (tier, operands, result)
@@ -1368,5 +1372,7 @@
 The transfer rules are:
 
-1. An effective control known false disables the operation. Otherwise,
+1. If any control literal is known false, counting the operation's own
+   controls together with its effective control context, the operation is
+   disabled: preserve all abstract values and record no causal event. Otherwise,
    an X-family flip or controlled swap evaluates its targets only when
    all its operands are known; any other target becomes unknown.
@@ -1391,4 +1397,8 @@
    inductive over-approximation may represent remaining visits, but may
    not establish a constant that these transfers do not establish.
+   The normative D_F is the union obtained by the stated finite transfers;
+   acceleration must preserve that domain. A coarser invariant may prove
+   the obligation on a superset, but failure on that superset is not a
+   counterexample on D_F.
    This is a decidable finite rule set; Boolean polynomial simplification
    and quantum identities beyond these exact adjoint pops supply no
@@ -2884,4 +2894,58 @@
 validation or the §9.2 linker obligation that the registry interface and
 body match the supplied closure hash.
+
+**Oracle invocation context (K77).** An oracle's catalog argument vector
+contains exactly its declared parameters, flattened in header-group order
+`in`, `tgt`, `fault`, `mem`, `args` (§16.2); empty groups add no entries.
+The invocation token is not an additional formal or vector entry.
+Before concrete expansion, consumers MUST supply and validate the
+explicit source-binding channel `oracle_invocation`, preserve it through
+the captures below, and reject missing, ill-typed or source-inconsistent
+context. The channel is a record with exactly one field, `token`, of
+K24's `value` type with `isa_type:"token"`: four canonical nonnegative
+decimal strings in §5.4 order `(B, heap_limit, stack_limit, depth_limit)`,
+resolved from that source call's `tk` and
+validated for the linked callee under §5.4. A root oracle instead binds
+the explicit launch/schedule request budget. Unresolved source parameters
+retain §11's admission/concrete-check staging.
+
+This channel is explicit input to the linked source-body builder, outside
+the catalog JSON and positional actuals, not an implicit name, default,
+new constructor key or token arithmetic inside a recipe. The registry
+binds the closure's source/interface; its builder instantiates the
+source-derived constructor body separately for each invocation, using
+this tuple and the linked source/layout to derive B, frames and every
+token-dependent limit or width supplied to `oracle.construct`.
+A registry keyed by closure hash alone cannot fix one invocation budget.
+The context is associated with the full §11 invocation identity, not
+with the closure hash or positional vector values alone.
+
+Source binding captures the channel with the corresponding `arguments`
+actual and with any body/template adapter containing that call. Forwarding
+an arguments name through `invoke` or `call`, or splicing/applying a
+captured body/template, preserves that captured channel; unrelated
+caller/apply-site context cannot replace it. The qinplace adapters capture
+the source `tk` for both calls. Each nested source oracle call resolves
+its own `tk` in its own fixed bindings, then restores the outer context.
+Source-adjoint adapters retain their captured tuples and perform §5.3
+replacements before recipe instantiation (K62). Inverse traversal retains
+each instantiated forward call's channel and forward occurrence identity
+while reversing/adjointing its operations (§11). None of these captures
+adds a leaf, ordinal, source parameter or closure-hash component.
+
+**Two-token witness.** Use §16.3 example 1's `inc8` closure and two source
+calls `oracle_call @inc8 tk2 (x) t f () ()` and
+`oracle_call @inc8 tk3 (x) t f () ()` in one action expansion, with
+`tk2=(2,0,0,0)` and `tk3=(3,0,0,0)`. Both positional vectors are `[x,t,f]`;
+their captured contexts are respectively `{"token":["2","0","0","0"]}`
+and `{"token":["3","0","0","0"]}`. The linked closure hash is identical.
+The first construction has two frames and XORs `(0,FAULT_BUDGET_STEPS)`
+into `(t,f)`; the second has three frames and XORs `(x+1 mod 256,0)`.
+Starting from `(t,f)=(0,0)`, the final pair is `(x+1 mod 256,1)`.
+Their §11 edges are distinct: separate source points each have
+`call_index=0`; two calls within a single source-row forwarding expansion
+instead have forward `call_index=0,1`. Inverse traversal retains those
+identities and tuples and restores the complete input. Neither binding
+adds a token to `inc8`'s empty signature `args` list or changes its hash.
 
 **Ordered descriptors (K25).** A `records` formal has exactly `name`,
@@ -3448,4 +3512,10 @@
 A `proof` label requires the domain to equal D; otherwise the claim is
 `evidence` with the covered fraction.
+For a borrow-frame obligation, use D_F of §5.6; a region claim over D
+does not by itself establish the frame claim. For example, with c
+allocated at zero, the single frame `CX(c,b)` over {c=0} × {b=0,1}
+is identity on b. The interleaved prefix `CX a c; CX x c; CX a c;
+CX x c` clears c only by polynomial algebra; §5.6 instead admits both
+c values at entry, so the same single-CX frame fails its obligation.
 
 **Component resolution (K69/K70).** These component-domain rules apply
@@ -3790,4 +3860,9 @@
   VER       := INT "." INT
 ```
+
+The oracle header and signature declare no invocation-token slot. Its
+catalog interface follows the five printed groups exactly; the separate
+`tk` operand binds the typed `oracle_invocation` channel of §11.1, not a
+reserved header name or an extra `args` element.
 
 Lproc groups have the types and roles of §3.7. A `token` suffix is

```

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


# Background (not graded): `errata-0.8.md`

# ISA 0.8 erratum — borrowed frame domain (§5.6)

Binding maintainer interpretation, 2026-11-01; b-isa-spec-73y, ISA 0.9
editorial pass V. The accepted 0.8 file remains byte-for-byte unchanged.

The sentence is: “The frame's realised permutation P_F on its wires MUST
factor as `P_F = P' ⊗ I_B`, established by a T3 claim over the frame's full
domain (exhaustive, or a library certificate, §12 `borrow_frames`) or
**structurally by the translation lemma**”.

Reading A takes “full domain” as the independent cube of every frame wire,
regardless of allocation or the region prefix. Reading B includes every
borrowed/interface value but admits established allocation/prefix facts
for local wires. Council intent is B: `CX(0,b)` is identity on arbitrary
b and an external entangled reference.

The binding interpretation is the precise D_F definition, normative
constant/causal-adjoint entry analysis, restricted T3 equality and checker
support obligation in [ISA 0.9 §5.6](Bennett-ISA-Spec-0.9.md#56-borrowed-systems-and-borrow-frames),
K76. That text is incorporated here: no stronger polynomial or quantum
entry analysis may narrow D_F. Exact permutation proofs inside frames
remain available; borrowed and interface components remain unrestricted.
Linearity extends equality on span(D_F) to each reachable entangled state.

Affected accepted reference fixtures (all remain accepted):
`r9-sol-oracle.bisa`, `r9-codex-oracle.bisa`, `r9-loop.bisa`, and
`r9-sol-qinplace.bisa`, in `reference-interpreter/tests/fixtures/`.
A polynomial-only interleaved CNOT prefix zero is outside this entry
analysis and now rejects with §5.6. This erratum does not admit 0.9 objects
through the reference interpreter's existing 0.8 version gate.


# Background (not graded): `isa-0.9.PROGRESS.md`

## 2026-11-01 Editorial pass VII — oracle invocation-token binding (5xm)

Reading **B** adopted. Bead 5xm remains in_progress for the orchestrator's
round 7, together with 73y. Implementation commits: 1d86f00 and
4f7e18f (source-adjoint versus inverse identity clarification).

| Item | Adopted/declined | Clauses / evidence | Commits |
|---|---|---|---|
| B: explicit invocation context outside A | adopted: typed `oracle_invocation.token`, captured per source call; source-derived body builder takes the tuple explicitly | §4.7, §11.1, §16.2; action.rs 659–699, 844 onward; claims.rs 394–415 and claim_budget | 1d86f00 |
| A: synthetic invocation-token formal | declined: no such slot in the source header/signature, and reference receives the budget separately from args | §16.2 five groups; K24; action.rs oracle_quantum signature | 1d86f00 |
| capture / forwarding / inverse traversal | adopted: context travels with A/body/templates, including qinplace adapters; nested calls resolve their own tk; retain forward identities under inverse | §11.1 K77 | 1d86f00, 4f7e18f |
| two-token inc8 witness | adopted: identical source closure and `[x,t,f]`, different captured B=2/B=3 tuples; two versus three frames | §11.1 worked example; oracle.rs 256-input regression | 1d86f00 |
| normative inventory and artifacts | one new MUST, K77 only; K1–K76 byte-identical; exact-label diff regenerated; catalog bytes unchanged | §0.2; spec/isa-0.8-to-0.9.diff | 1d86f00 |

Why B: the source grammar supplies invocation `tk` separately from the
oracle's five declared groups. `action.rs` resolves that operand in the
caller, collects declared args separately, and passes `budget` separately
to `oracle_quantum`/the oracle executor. `claims.rs` likewise obtains the
root budget from schedule binding, not a fictitious source parameter.
The constructor catalog's `oracle_call` and `lift.oracle_call` only forward
S and A. `ref_language.rs` captures the lexical environment for A and
body/template actuals; its generic fixture registry contains supplied
constructor bodies, not an ISA source-to-constructor builder. It does not
establish a source invocation budget by itself. The amendment specifies
that missing source-builder input explicitly, without claiming a complete
0.9 source expander in the conformance crate or changing a recipe.

The channel has exactly one field `token`, K24 value(token), canonical
four-string tuple in §5.4 order. It is explicit out-of-catalog source
binding metadata, not a JSON-constructor extension, added formal, default,
or closure-hash component. The builder is invocation-specific even when
the registry is keyed by one closure hash. Existing source/link checking,
control propagation, budget validity and admission/concrete-check staging
remain in force. No capability, width or legal source program is removed.

The new regression passes against the unchanged reference before the
text edit (`.tmp/pass-vii-before-text.log`), covering all 256 input x,
nonzero target/fault seeds 0x55/0xa, the combined XOR result and inverse
restoration including allocator state. This validates the source semantics
of the worked example; it does not claim a generic catalog source builder.
The bead's call_index shorthand is qualified by existing K63: two calls
within one source-row expansion have indices 0/1; calls at separate source
points each start at 0 and remain distinguished by the point. No change to
K63, call numbering or invocation-path semantics is made.

Required headless gates, all exit 0: reference **468 passed, 0 failed,
5 unchanged ignored**; conformance **113 passed, 0 failed, 0 ignored**;
`python3 -I conformance/tests/draft_witnesses.py` PASS (rerun on final
source-adjoint wording); `python3 -I conformance/tools/ref_catalog.py
--check` PASS. Both Cargo commands used `--offline` and the requested
manifest paths. All gates unset DISPLAY, WAYLAND_DISPLAY,
DBUS_SESSION_BUS_ADDRESS and BROWSER, with project-local TMPDIR.
Logs: `.tmp/pass-vii-{reference,conformance,witness,catalog}.log`.
Both touched Rust tests pass rustfmt --check; owned source/progress
whitespace checks pass. Pass VI's completed gate precedes pass VII edits.

Catalog byte SHA-256 remains
`52dbc3f8f0c91d587fd933a43080385fd5284abcfec0ce84788229fcb15c53d8`;
envelope remains
`5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197`
(219 recipes). Accepted 0.8 SHA-256 remains
`90e61d9c377c939fe9652758f61cd5ead068ef06e4e40d812d3f3c5197ab605e`.
No catalog edit, sibling write, push or remote sync. Orchestrator owns
session worklog, final 0.9 statement-layer regeneration/INV-3 citation
resolution and the pending one-reviewer council round 7.

Exact new normative text and worked example (line wrapping as published):

§4.7:

> The invocation operand `tk` is separate from the callee's declared
> `args`; its explicit catalog context channel is `oracle_invocation`
> (§11.1, K77), including for the lifted calls of §4.2.

§11.1:

**Oracle invocation context (K77).** An oracle's catalog argument vector
contains exactly its declared parameters, flattened in header-group order
`in`, `tgt`, `fault`, `mem`, `args` (§16.2); empty groups add no entries.
The invocation token is not an additional formal or vector entry.
Before concrete expansion, consumers MUST supply and validate the
explicit source-binding channel `oracle_invocation`, preserve it through
the captures below, and reject missing, ill-typed or source-inconsistent
context. The channel is a record with exactly one field, `token`, of
K24's `value` type with `isa_type:"token"`: four canonical nonnegative
decimal strings in §5.4 order `(B, heap_limit, stack_limit, depth_limit)`,
resolved from that source call's `tk` and
validated for the linked callee under §5.4. A root oracle instead binds
the explicit launch/schedule request budget. Unresolved source parameters
retain §11's admission/concrete-check staging.

This channel is explicit input to the linked source-body builder, outside
the catalog JSON and positional actuals, not an implicit name, default,
new constructor key or token arithmetic inside a recipe. The registry
binds the closure's source/interface; its builder instantiates the
source-derived constructor body separately for each invocation, using
this tuple and the linked source/layout to derive B, frames and every
token-dependent limit or width supplied to `oracle.construct`.
A registry keyed by closure hash alone cannot fix one invocation budget.
The context is associated with the full §11 invocation identity, not
with the closure hash or positional vector values alone.

Source binding captures the channel with the corresponding `arguments`
actual and with any body/template adapter containing that call. Forwarding
an arguments name through `invoke` or `call`, or splicing/applying a
captured body/template, preserves that captured channel; unrelated
caller/apply-site context cannot replace it. The qinplace adapters capture
the source `tk` for both calls. Each nested source oracle call resolves
its own `tk` in its own fixed bindings, then restores the outer context.
Source-adjoint adapters retain their captured tuples and perform §5.3
replacements before recipe instantiation (K62). Inverse traversal retains
each instantiated forward call's channel and forward occurrence identity
while reversing/adjointing its operations (§11). None of these captures
adds a leaf, ordinal, source parameter or closure-hash component.

**Two-token witness.** Use §16.3 example 1's `inc8` closure and two source
calls `oracle_call @inc8 tk2 (x) t f () ()` and
`oracle_call @inc8 tk3 (x) t f () ()` in one action expansion, with
`tk2=(2,0,0,0)` and `tk3=(3,0,0,0)`. Both positional vectors are `[x,t,f]`;
their captured contexts are respectively `{"token":["2","0","0","0"]}`
and `{"token":["3","0","0","0"]}`. The linked closure hash is identical.
The first construction has two frames and XORs `(0,FAULT_BUDGET_STEPS)`
into `(t,f)`; the second has three frames and XORs `(x+1 mod 256,0)`.
Starting from `(t,f)=(0,0)`, the final pair is `(x+1 mod 256,1)`.
Their §11 edges are distinct: separate source points each have
`call_index=0`; two calls within a single source-row forwarding expansion
instead have forward `call_index=0,1`. Inverse traversal retains those
identities and tuples and restores the complete input. Neither binding
adds a token to `inc8`'s empty signature `args` list or changes its hash.

§16.2:

> The oracle header and signature declare no invocation-token slot. Its
> catalog interface follows the five printed groups exactly; the separate
> `tk` operand binds the typed `oracle_invocation` channel of §11.1, not a
> reserved header name or an extra `args` element.

## 2026-11-01 Editorial pass VI — council round 6 response (73y)

Source: `../bennett/docs/council/isa-09-2026-10-31/round-6/report.md`
and `out-codex.json` (codex seat, astra). All requested dispositions are
adopted; 73y remains in_progress for the orchestrator's round 7.

| Item | Adopted/declined | Clauses / evidence | Commits |
|---|---|---|---|
| R6-CODEX-1, S0 | adopted: own and contextual control literals participate in the false shortcut; preserve values and record no event | §5.6 rule 1; suite F `pass_vi_own_false_control_preserves_zero_at_frame_entry` | 44ffea0 |
| S1 finite-transfer domain | adopted: acceleration preserves canonical D_F; failure on a coarser superset is inconclusive | §5.6 rule 3 | 44ffea0 |
| S1 frame versus region claim | adopted: region-D claim alone is insufficient; zero-control and polynomial-only-prefix illustration | §12.2; existing frame-domain negatives | 44ffea0 |
| S1 statement layer | adopted; regeneration and INV-3 citation resolution belong to the conformance orchestrator, after final pass VII text | final 0.9 statement layer in bennett-conformance, no sibling write here | orchestrator pending |

Exact rule-1 replacement (the following all-operands-known rule remains):
“If any control literal is known false, counting the operation's own
controls together with its effective control context, the operation is
disabled: preserve all abstract values and record no causal event.”

Exact rule-3 addition:
“The normative D_F is the union obtained by the stated finite transfers;
acceleration must preserve that domain. A coarser invariant may prove
the obligation on a superset, but failure on that superset is not a
counterexample on D_F.”

Exact §12.2 addition:
“For a borrow-frame obligation, use D_F of §5.6; a region claim over D
does not by itself establish the frame claim.” The illustration uses
single-frame CX(c,b) over {c=0} × {b=0,1}; the interleaved CNOT prefix
clears c only by polynomial algebra and therefore fails the normative
frame domain. The witness remains rejected even with valid reverse cleanup.

Lamport response: R6 <1>1–<1>3 expose a real terminology ambiguity;
<1>4 identifies the sound implemented shortcut. The replacement explicitly
counts both control sources, removing the divergent D_F in <1>5 without
strengthening the analysis. The supplied complete CCX witness is admitted
by the unchanged reference **before the text edit**, so this is a regression
lock, not a claimed red-to-green implementation fix. Its single CX frame
requires c=0 at entry; replacing both CCXs by X (valid cleanup, c=1 at
entry) rejects with §5.6. All five frame_domain tests pass, including the
polynomial-only-prefix, independent-interface and certificate negatives.
Evidence: `.tmp/pass-vi-before-text.log`.

Required headless gates, all exit 0: reference **467 passed, 0 failed,
5 unchanged ignored**; conformance **113 passed, 0 failed, 0 ignored**;
`python3 -I conformance/tests/draft_witnesses.py` PASS;
`python3 -I conformance/tools/ref_catalog.py --check` PASS.
Logs: `.tmp/pass-vi-{reference,conformance,witness,catalog}.log`.
Both Cargo commands used `--offline` and the requested manifest paths;
all four commands unset DISPLAY, WAYLAND_DISPLAY, DBUS_SESSION_BUS_ADDRESS
and BROWSER, with project-local TMPDIR. The formatted frame-domain
regression was rechecked separately, 5/5 PASS.

K1–K76 are byte-for-byte unchanged. The exact-label 0.8-to-0.9 diff is
regenerated. Accepted 0.8 and published catalog bytes are unchanged;
catalog envelope remains
`5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197`
(219 recipes). No new K row, reference implementation change, sibling
write, push or remote sync. Orchestrator owns worklog and council round.

## 2026-11-01 Editorial pass V — consumer borrow-domain gap (73y)

Maintainer selects Reading B with a normative, object-checkable entry
analysis. This amendment awaits the orchestrator's one-reviewer council
fix round; no muse round. Earlier three-seat acceptances below apply to
the pre-pass-V publication and remain history. Bead 73y stays in_progress.

| Gap / proof step | Disposition | K | Clauses / coverage | Status |
|---|---|---|---|---|
| frame-domain ambiguity / INV-3 1.5.5 | a: define D_F from constant/causal-adjoint prefix analysis; full independent interface/borrowed values; restricted factorisation plus support and linearity | K76 (K1–K75 unchanged) | ISA-5.6-P2.S2–S3, P9–P13; T3; frame_domain.rs | council fix round pending |
| 0.8 consumer binding | a: short erratum incorporating the new §5.6 interpretation; accepted 0.8 bytes unchanged | K76 in 0.9 | spec/errata-0.8.md; SQ20 | implemented |
| reference alignment | a: independent EntryAnalysis; no polynomial prefix facts; retain exact ANF frame proofs and causal matching; definite failure guard on certificate API | K76 | borrow.rs; frame_domain.rs | implemented |
| INV-3 missing premise | a: entry support in span(D_F), linearity including R, induction along the reachable prefix | K76 | sibling proof 1.5.5.1–1.5.5.3; 0.9 statement IDs explicitly versioned | committed in sibling |

Least sufficient family: allocation constants and exact causal inverse
restoration (including H/oracle-pair/H and H/qinplace-pair/H), with
constant primitive-gate transfer. No exact polynomial prefix analysis is
needed for the accepted corpus. Exact Boolean identities inside frames
remain valid. CLI admission audit: all 48 fixture/neutral .bisa objects
accepted before and after; all four named r9 cases remain accepted.
Neutral full runner: 16/16 cases, including every expected hash and run.
The polynomial-only prefix negative now rejects with §5.6; the original
checker admitted it after a valid explicit §6.2 reversed cleanup.
Interface/local correlation and whole-region-certificate bypass negatives
also reject. No fixture edits, VM edits, 0.8 edits, push or remote sync.

Spec/diff commit: 9df1541. Erratum commit: 6182d7c.
Sibling proof commit: 2095a7d (only proofs/INV-3-discipline-soundness.md).
Reference implementation commit: 1a19072 (entry analysis, SQ20 and tests).
Final headless reference suite: **466 passed, 0 failed, 5 ignored** (the
five existing opt-in exhaustive tests are unchanged); exit 0. Five tests
were added relative to 461: four integration tests and one opaque-domain
unit test. Log: `.tmp/pass-v-reference-verified.log`. The widened-domain
library guard requires a true frame-domain proof when a region-D replay
would miss values; it adds no producer-controlled domain override or new
serialized claim kind.
Final headless conformance suite: **113 passed, 0 failed, 0 ignored**;
exit 0, `.tmp/pass-v-conformance.log`. Publication witness (including
byte-exact labels/diff and 0.8 fingerprint) PASS; catalog --check PASS
(219 recipes, bound envelope unchanged); neutral runner 16/16 PASS;
fixture admission audit 48/48 PASS with zero losses. All commands unset
DISPLAY, WAYLAND_DISPLAY, DBUS_SESSION_BUS_ADDRESS and BROWSER and use
TMPDIR=/home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp.
K1–K75 verified byte-for-byte unchanged; K76 is the only addition.
Final 0.9 spec SHA-256:
7b77c96e08a1f7e40d8a70155bef703bb4e7d2e9c850a95e3579a7ee7ae288ce.
Exact-label diff SHA-256:
4f7f506018bcd46769d2711eab2e3847391d58ed575247050608c65876d4335a.
No push or remote/Dolt sync. The implementation sub-agent leaves the
session worklog and the pending council round to the orchestrator.
Detailed Lamport argument/dispositions:
`docs/briefs/2026-11-01-isa-09-pass-v-73y.md`.

## Published alongside 0.8 on 2026-11-01 06:58:38 UTC

ISA 0.9 is `spec/Bennett-ISA-Spec-0.9.md`, accepted by all three seats
on 2026-10-31 (sol r3, codex r2/r4, muse r5; K64/K65 ratified).
New consumers (bennett-vm M5 onward) implement 0.9. Accepted 0.8 remains
unchanged for dialect 0.2.x and the reference interpreter until the dialect
0.3 track moves. Catalog: `spec/ref-0.9.json`, 219 recipes, envelope
`5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197`;
redundant draft JSON removed, consumers and exact-label diff updated.
Mechanical publication; no council round. Bead b-isa-spec-fhp.
Headless gate PASS: 113 tests, 0 failed/ignored; publication witness PASS
(exact diff and forbidden-word checks retained); catalog --check PASS.
Initial gate caught the stale `Complete draft catalog` assertion; it now
expects `Complete catalog`, with no hash or semantic change. 0.8, K rows,
fenced examples, printed hashes and catalog bytes verified unchanged.
Reference-interpreter suite not run; its source is untouched.

## 2026-10-31 Final editorial pass IV — muse round 5 dispositions

Source: council isa-09-2026-10-31 round-5 out-muse.json/report.md:
accept, zero blockers, four S1 suggestions; no further muse round.
Maintainer authorizes publication of the bound catalog here; making 0.9
the current ISA remains the maintainer's next step. Bead b-isa-spec-4a4.
Surgical edits only; K1–K75 and accepted 0.8 semantics/bytes retained.

| Suggestion / proof step | Disposition | K | Clauses / existing coverage | Semantic premises | Bead status |
|---|---|---|---|---|---|
| 1 / §16.3 placeholders | a: fill all 25 symbol values, including repeated symbols and the printed SCC envelope; independent precheck reconstructs every envelope | existing §9.2 | §16.3; §0 example inventory | §9.2, §16.1–§16.2 | 4a4 CLOSED |
| 2 / §5.5 matched cleanup | a: clarify that ins writes invalidate the pair, while mem-cell writes only remove the clearing guarantee | existing E17.5 | §5.5 first paragraph | §4.2, §5.5 later paragraph | 4a4 CLOSED |
| 3 / INV-3 1.4.2–1.4.3, gaps 5–6 | a: add muse's permissive sufficient dependency-set test; failure is inconclusive | existing K41 | §6.1 outstanding dependence | §6.1 transfer, §14.2; INV-3 1.4 | 4a4 CLOSED |
| 4 / §11.1 and §17 item 7 | a: publish byte-identical bound catalog and worked ctl-X fixture; replace pending publication references | existing K11, K19–K28 | §11.1 serialization; §17.7; §0 D2 | §9.2, §9.4, §11, §11.1, §12.1–§12.3 | 4a4 CLOSED |
| 5 / final status and validation | a: record all three council acceptances and completed vote gate; current-spec publication stays with maintainer | none | opening status/history | muse r5 acceptance; maintainer K64/K65 ratification | 4a4 CLOSED |

Item commits: 1 c55743d; 2 55d15f4; 3 3466b5e; 4 5053fcd.
Item 5 also removes the stale pending-muse gate in the immediately
following status prose and makes the 0.8-to-current-publication boundary
explicit. It does not replace the accepted 0.8 file or request a council
round. All four muse S1 suggestions have a dispositions row above; no
new K row or normative capability restriction is introduced.

Additional hash cross-check: the read-only Python seed independently
agrees for examples 1, 3, 5, 6, 7 and 9 (all six memoryless envelopes).
Layout-bearing examples use K65's JCS component-array paths; no old
0.8 dotted-path identity is substituted. The pinned review binary's
SHA-256 is 7b1e6cca78d21f01793e5eeb96a5c8e780609b75bf076bbbf049861cccdb59f5.

Final headless validation (exit 0 for both required commands):
- `python3 -I conformance/tests/draft_witnesses.py`: PASS on final bytes,
  all ten objects / 25 symbol fields, both printed envelopes, exact
  system-diff byte comparison, forbidden-word scan, published catalog,
  derived fixture bytes and pinned compatibility check/hash/8 runs.
- `cargo test --offline --manifest-path conformance/Cargo.toml`: PASS,
  113 tests, 0 failed, 0 ignored. This includes the new exact ctl
  matrix witness and all retained full-domain/count/ordinal assertions.
  Run log: `.tmp/editorial-iv/cargo-test.log`.
- `python3 -I conformance/tools/controlled_action_fixture.py --check`:
  PASS; `ref_catalog.py --check`: PASS (219 recipes, bound hash above).
- K1–K75 continuous; no `<to be computed` example placeholders or
  proposal/proposed/proposes words in the draft. Owned source/progress
  whitespace checks pass; unified-diff context whitespace stays exact.
- Accepted 0.8 SHA-256 unchanged:
  90e61d9c377c939fe9652758f61cd5ead068ef06e4e40d812d3f3c5197ab605e.
- Final draft SHA-256:
  6ee2aaba780385c750a04dc13eeb186788225c434435dace9ba6c4184036eac1.
- Exact-label diff SHA-256:
  880d500df26c7495c6003771c17be6eab9f0930ec7cd54f2c2ca94e1fd1b18f8.
The artifact is regenerated with `diff -u --label
 a/spec/Bennett-ISA-Spec.md --label b/spec/Bennett-ISA-Spec-0.9.md
 <absolute accepted> <absolute draft>` (exit 1 means the expected files
 differ). Bead 4a4 closes this editorial/publication-artifact work only;
 current-spec publication remains the maintainer's next step. Beads export
 is refreshed before the fifth explicit-path commit. No push, remote/Dolt
 sync, accepted-text edit, interpreter edit, sibling write or worklog edit.

Item 4 verification/S0 check:
- `spec/ref-0.9.json` is byte-identical to `spec/ref-0.9.json`.
  Python -I ref_catalog.py --check PASS: 219 recipes, four-line envelope
  5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197.
  Rust independently agrees with that envelope hash. No recipe changes.
- `conformance/fixtures/controlled-action-09/` publishes the complete
  object, target, one leaf event, schedule, root frame and certificate;
  both root and controlled-callee region records include numerical
  zero-error claims and the required root invocation/composition. Root
  table has all four full before/after tuples. No allocation is needed;
  resources: time 1, peak_qubits 2, qubit_second 2, fast class.
- Existing conformance Expander instantiates the published ctl/action_call
  recipes through the displayed flip body. Exact matrix checker PASS:
  every basis column in both root and inherited-control-first callee
  ordering; exact global phase, zero V†U-I and Frobenius bound.
- The fixture generator's --check compares every derived byte. Pinned
  read-only review binary check/hash PASS on compat-0.8.bisa, and all
  8 forward/adjoint basis runs PASS. Its 0.8-only version gate prevents
  direct admission of controlled.bisa (0.9), just as for §16.3. The
  compatibility object has its own 0.8 identities, frame/table encoding
  and default ref binding; it never substitutes for the 0.9 catalog.
  `check` is identity/metadata admission, not certificate-claim replay;
  a scratch altered-table probe confirmed that limit. No pinned 0.9
  executor/interval-checker conformance is claimed. The fixture README
  records the scope and exact reproduction commands.
- Library-unavailable rejection remains binding. Publishing an existing
  deterministic artifact and one complete witness adds no restriction
  on source algorithms, interfaces, controls, widths or target choices.
  The old README gets only one line pointing to the published copy.
- Draft witness precheck PASS, including byte-exact diff, accepted 0.8
  fingerprint, catalog and fixture checks.

Item 3 proof/S0 check: read INV-3 in bennett-conformance read-only. Its
1.4.2 counterexample transfers d0 through d1 to interface t. Cleaning d1
and applying H to d0 cannot erase that path to t, so this sufficient test
fails there and cannot admit the refuted cleanup. Diagonal phases and
region cells are explicit sinks; transitive paths include implicit target
reads and effective controls, as the existing transfer/operation rules
require. Exact K41 M = I_G ⊗ V (every input, external entanglement and
exact global phase) remains the semantic definition. A failed syntactic
test is inconclusive, so semantic cancellations and other valid proofs
remain available. This is MAY text, not an additional acceptance gate.
Draft witness precheck PASS after exact diff regeneration.

Item 2 S0 check: this retains the existing permitted intervening store,
the identical uncall permutation, the producer clearing obligation and
prefix restoration. No new static memory prohibition or dynamic fault
is introduced. Draft witness precheck PASS after exact diff regeneration.

Item 1 verification: the new independent stdlib precheck first failed on
example 1's placeholder, then passed all ten objects and both fully
printed envelopes. It builds layout paths as JCS arrays, preserves
external-reference order, and applies SCC member wrapping only to `sum`.
The read-only pinned review interpreter's `hash` rejects 0.9 objects with
`§1: expected isa=0.8`; it cannot certify draft-version envelopes. No
interpreter is changed, no 0.8 surrogate hash is substituted for 0.9.
S0: values are determined by §9.2; no operation, interface or capability
is changed. The obsolete placeholder prose is updated with the vectors.

Filled §16.3 values (example / symbol):

| Example / symbol | Interface hash |
|---|---|
| 1 / inc8 | `ed9865300b85a519c2379de98e36e635e72b5b78d8bdfca03dccf9a09aa3df5e` |
| 2 / zero | `43e032f98d7aff20f6864d6368b20ab4ef9d810938999acff8d71ed16e6b17d7` |
| 2 / sum | `cb52102decd586b7585b5d73b90841dcec75edac5a5a2d0f43c5efb34d4cceb1` |
| 2 / sum_db | `3ad937b1cd867454989c5c5f58244681ef2c09dbabf7fce56515a68f63462ee6` |
| 3 / borrow_demo | `6f4782e9bde4267acd1afddd650093722a056d9d50ee465b79cb86a4606b2a94` |
| 4 / flip | `3860ea712b2d70fc495834586bb397656a467c85235aa069768318a06e9fa89b` |
| 4 / ones | `ff8e49307d5ec9ab32eea2406339f878630bbb4501080829200433a18d6951cb` |
| 5 / flip | `3860ea712b2d70fc495834586bb397656a467c85235aa069768318a06e9fa89b` |
| 5 / scratch | `05525834cbe5a518aa97444912254f3c12c75dd86314a98ba550f45187208a0b` |
| 5 / main | `5cebd5a72ee7873edda0d2c35afed2a5ab79eba60f2b242b2a856d5fa4074634` |
| 6 / inc8 | `ed9865300b85a519c2379de98e36e635e72b5b78d8bdfca03dccf9a09aa3df5e` |
| 6 / adaptive | `b80aed1639a9ac6a6856f02b0b3264d905e4eea3fa3f9081c01e56283ea398cf` |
| 6 / overdraw | `c0d9835844fa882c1864044acc6fa26dba3935e0d6a9d33f9cdbf1e7c877d250` |
| 7 / g | `0d65d926275688cfebf2831c1de960b03a6b8ea6400866e6d9fef8f393ca2c2e` |
| 7 / ginv | `786f1970ca3d78ef3d5de795411ee276286711c89b756872757c24f9bd569cc9` |
| 7 / addya | `5999b6d3d2362f8c1971ef6f37b404766aa5c18f6ba1880d767bfde351e47392` |
| 7 / run | `562ab7270a0f508d6a2f4a757f3f90964da0b60541bac2c5efa421bad009056a` |
| 8 / work | `d365ade0d8452d7d12b1a72c87e7106b06eef99e5958d0345133cf6eb0cbeb03` |
| 8 / main | `dbf66e749a776cbb1ceccfc8b530caf664e24fb416fdf52ccf3942f4b89fdcf2` |
| 9 / zero_cause | `badf7dd2a59afa879f092921946539dfb918cedd35f6fbbaa838c630577eaed4` |
| 9 / zero_cc | `0403d76ff065acab57cb9165cfe1d3d73bbf8dad60bbc1348fb0305ee4f37611` |
| 10 / plus_db | `c6e53733d87782414d05720d444734d9335244155518db4f60916e3d4b06dd1d` |
| 10 / flip_arg | `bfa13d9a564e3f8562098c4ea39330d947efa64521310afad6a329dc594bd671` |
| 10 / worker | `9bd5e97be1f600494476527fb2d7d088bffab607bdadac8e01f9b23d15f9dfe1` |
| 10 / through | `4ee502a2d517d53d229f2ae21346505af06a228a2f0d2967938d48683e16d9e7` |

## 2026-10-31 INV-6 editorial pass III — final dispositions

All 12 gaps: **8 a** (text changes), **4 b** (already covered by K13),
**0 NAD**. Eight new K rows, **K68–K75**, remain in the single §0.2
table. Status explicitly reopens snapshot 59eee9ad0d96 for a one-seat
re-review; that earlier sol/codex acceptance is retained as history.
The clean starting file's 01da16588c0b digest includes only 9b8e01e's
later acceptance header. This pass does not perform the re-review.

Final clause IDs are from the scratch graph; the supplied statement
catalog remains the dependency authority and is not regenerated in place.
For a rows, dependencies below are the declared semantic premises (a
clause includes its cited statements); for b rows they identify existing
coverage, not newly added markers. All rows close through afu; no new
follow-up bead or library-boundary exception is needed.

| Gap / proof step | Disposition | K | Final clauses / existing coverage | [deps:] IDs (ISA- prefix) | Bead status |
|---|---|---|---|---|---|
| 1 / 1.1.3 | a: action D includes both region roles; factor list repaired in one sentence | K68 | ISA-5.3-P1.S1 | 5.1-P1, 5.2-P4, 3.3-P19, 5.6-P1, 14.2 | afu CLOSED |
| 2 / 1.2.2 | a: header names resolve to category/group/slot/cell identities; equality to D component by component | K69 | ISA-12.2-P2.S2–S5; P4.S2–S3 | 5.1-P1, 9.4-P2, 3.3-P19, 5.2-P4, 5.3-P1, 12.1-P1, 12.1-P7, 12.1-P8, 12.2-P1, 14.3-P3 | afu CLOSED |
| 3 / 1.2.3 | a: zero-based borrow positions in checked K13 allocation order; names label-only, no interface coverage | K70 | ISA-12.2-P2.S6–S8 | 4.3-P2, 5.6-P1, 12.1-P8 | afu CLOSED |
| 4 / 1.2.4 | a: omitted components fixed at zero; n and exact n/\|D\| | K71 | ISA-12.2-P3.S2–S4 | 5.2-P4, 5.3-P1, 12.1-P8, 12.2-P1 | afu CLOSED |
| 5 / 1.2.5 | a: uniqueness after resolution, equal widths, inclusive valid ranges, valid cell indices | K72 | ISA-12.2-P3.S1 | 3.3-P2.S2, 3.3-P19, 12.2-P1 | afu CLOSED |
| 6 / 1.4.2 | b: complete K13 tuple object already fixed, including controls, every interface cell and borrowed component; no projection-only comparison | K13 | ISA-12.1-P7.S6; P8.S1–S6 | existing 12.1-P7, 12.1-P8 (P7.S6 declares 14.3-P3, 5.6) | afu CLOSED |
| 7 / 1.4.3 | a: compatible ordered roles, widths/classes, region shapes and borrow requirements; map by position, never local names | K73 | ISA-12.1-P15; non-normative P16 | 5.1-P1, 9.4-P2, 12.1-P7.S4, 12.1-P8 | afu CLOSED |
| 8 / 1.4.4 | b: K13 before/after object, canonical unsigned decimal strings, exact domain row count/order, including sampled table relations | K13 | ISA-12.1-P8.S1–S7 | existing 12.1-P8; enumeration 12.2-P1.S1 | afu CLOSED |
| 9 / 1.4.6 | b: subject already mandatory for both kinds, standalone per-claim invocation supplies all four budget values; scheduled root binding plus separately resolved nested contexts | K13 | ISA-12.1-P7.S1–S4; P11; ISA-12.3-P2/P3, P7.S3 | existing 12.1-P7, 12.1-P11, 12.3-P2, 12.3-P3, 12.3-P7 | afu CLOSED |
| 10 / 1.5.1 | a: checker report indexed by region hash / claim index / invocation or context; checked producer label request never a premise | K74 | ISA-12.2-P4.S1/S4–S6 | 1.2-P4, 12.1-P1, 12.1-P2, 12.1-P7, 12.1-P8, 12.1-P11, 12.2-P1, 12.3-P1, 12.3-P3, 5.6-P2, 14.3-P3, 12.3 | afu CLOSED |
| 11 / 1.6.5 | b: K13 uses distinct draws / \|D\|, always evidence even at fraction 1; K74 makes the separate count of replayed draws explicit | K13 (K74 report integration) | ISA-12.1-P8.S9–S10; existing witness P10/JSON; ISA-12.2-P4.S4 | existing 12.1-P8; report deps 12.1-P1, 12.1-P2, 12.1-P8.S9, 12.1-P8.S10, 12.2-P1 | afu CLOSED |
| 12 / 1.7.5–6 | a: unchecked (host limit), normal termination with cited quantity/operation, no label/count/fraction or discharged obligation, no host-imposed legality cap | K75 | ISA-12.2-P5 | 3.3-P2.S2, 3.3-P19, 12.1-P1, 12.1-P2, 12.1-P8, 12.2-P1, 1.2-P4, 5.6-P2, 14.3-P3, 12.3 | afu CLOSED |

Witnesses beside text: the CNOT zero slice, borrowed renaming, full-domain
mismatch at element 4 and full explicit reversed cell list are printed
in §12.2 P6/P7. K73's crossed-name equal-width witness is §12.1 P16.
K13/K67's existing complete before/after tuples, changed-argument and
short-budget outcomes, four draws/one distinct element and 25-bit D
remain unchanged. An action's unchanged in-region still contributes
independent cells to D; the region[63,1] count-1 witness describes a legal
action region (oracle mappings separately retain W=8).

Rejected alternatives and S0 cross-check:
- Gaps 1/2: dropping action in-region factors or deciding coverage by a
  name set makes independent systems disappear. Names are resolved only
  within their category; identities then decide equality. Do not ban
  cross-role names: borrowed t remains legal, and an explicit full cell
  list can prove full coverage just like all cells. No region, arbitrary
  width, body operation, oracle or demo-ladder capability is removed.
- Gap 3: matching borrowed labels against interface or body-local names,
  or merging distinct lifetimes on reused storage, loses positional
  identity. Checked K13 allocation order already includes the subject's
  calls/structured lifetimes; no new recipe traversal or source ordinal
  is invented. Omitted trailing borrow positions zero-fill; an earlier
  fixed-zero position is expressed by its singleton range.
- Gap 4: banning omission would discard already legal partial domains;
  unspecified or unconstrained fill would make replay ambiguous or
  inflate coverage. Select zero fill and retain all singleton/range
  slices. This fixes values on the checked slice only, never narrows D.
- Gap 5: duplicate-name counting, intersecting duplicate ranges, modular
  truncation of bounds or silently ignoring bad indices do not define
  one Cartesian product of independent coordinates. Reject those
  malformed descriptors, while preserving their well-formed equivalents.
- Gaps 6/8: replacing K13's object with a flat tuple or a §9.1 number
  encoding, accepting target/fault-only comparisons, or sample-only table
  rows would contradict the ratified full-tuple contract. Keep canonical
  decimal strings and one complete before/after row per declared domain
  element; a program expectation supplies a compact relation. Table
  enumeration follows the existing listed component order (last fastest),
  not tuple field order or signature sorting of the domain entries.
- Gap 7: matching equal-width slots or cells by local names can cross
  independent coordinates. Class/shape/role and borrow compatibility
  retains arbitrary names and arbitrary algorithms implementing the same
  relation, with classical arguments/budgets still K13-bound.
- Gap 9: adding a second budget field, defaulting to a chosen B, or
  reusing the root tuple for a different callee is unnecessary/unsound.
  K13 already requires per-claim standalone invocation, or the actual
  scheduled context's resolved budget, for all expectations and both
  exhaustive/sampled kinds. The payload table is completed by its prose.
- Gap 10: producer verdicts as premises, or writing checker labels back
  into certificate identity, would defeat independent checking. A label
  is a request and a completed evidence result rejects an overstated
  proof request. Structural/library proofs remain available: the new
  ordinary component-domain proof test expressly preserves K4's separate
  quantified two-composition relation. The host-limit result remains
  unchecked even when a label was requested.
- Gap 11: count/|D| overstates repeated draws. Retain the K13 distinct
  fraction plus replayed count; all sampled successes remain evidence.
  INV-6 1.6.8 forbids an overstrong mathematical claim that agreement on
  a slice never implies anything outside it; no such sentence is added.
- Gap 12: hard width/A/count caps, malformed-domain errors for host
  exhaustion, process aborts or proof/evidence based on incomplete replay
  are rejected. Legal large programs remain executable and claims remain
  expressible; only this host's unfinished check is unverified. Normal
  termination identifies the failing operation/quantity and §12.2.
- K13 prepends inherited controls to complete tuples. Resolving those
  first c bundles entries positionally prevents the same interface-name
  confusion for controls; a fixed control is a singleton range, so every
  zero slice and every full controlled domain remains expressible. This
  is domain metadata only, without a schedule/library/recipe change.

Validation (headless, Python -I; scratch .tmp/inv6-editorial):
- Required standalone `python3 -I conformance/tests/draft_witnesses.py`
  PASS, exit 0, including the exact system `diff -u --label
  a/spec/Bennett-ISA-Spec.md --label b/spec/Bennett-ISA-Spec-0.9.md
  <absolute accepted> <absolute draft>` byte comparison. That exact command
  generated the artifact (exit 1 means the expected files differ).
- Independent `check_witness.py`: PASS on the final draft, after the
  baseline failed at the absent new witness. Derives all 8 CNOT tuples,
  the 4-element zero slice and first full-domain mismatch at 4, checks
  five borrowed-label spellings, both explicit cell orders, crossed-name
  positional tuples, and the retained K13 budget/sampling calculations.
  This is a finite contract witness, not a claim of implemented 0.9
  checker/executor conformance; no interpreter source or test is edited.
- Scratch baseline/current clause graphs and statement catalogs: 26
  new/changed normative-classified statements, all with markers; all
  declared IDs resolve in the supplied Markdown authority; zero
  unresolved declared dependencies and zero ambiguous terms. The 15
  unresolved clause references are pre-existing external/xspec edges.
  The proof uses 0.8 positional IDs: its region-binding ISA-3.3-P14 is
  ISA-3.3-P19 in the supplied 0.9 catalog; unbounded widths are P2.S2.
  New declarations use the actual semantic premises, not the stale IDs.
- Scope audit PASS: only status header, eight §0 rows, one §5.3 sentence
  and §12 additions changed. K1–K75 continuous; all new rows have a
  witness. Forbidden-word scan PASS. Source/progress diff whitespace
  PASS; raw unified-diff context whitespace deliberately remains exact.
- Accepted 0.8 SHA-256 unchanged:
  90e61d9c377c939fe9652758f61cd5ead068ef06e4e40d812d3f3c5197ab605e.
  Entire §11.1 (including heading) unchanged, SHA-256
  f08c515b2c9fc8cc9418211c907c7cd681b30e4f5bb95c59fa9065be89d01e2e;
  full-library binding remains 219 recipes and envelope hash
  5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197.
  Entire §12.3 (including heading) unchanged, SHA-256
  60298f0f4fc04339643607134d9ef31b24487ed16e0c997faf0b4a9b4fe59547.
- Final draft SHA-256:
  3e4aa324d8b0e3ed8a9dfcc2c8312b886bfe8956160821a9207d2e701fe59e64.
  Regenerated diff SHA-256:
  424c2f75e050854a719fbaf42184753f56d438558ebc4b01c7827caf3d4c5ea6.
- afu closure note names K68–K75 and retained K13/K67; the closure is
  drafting/disposition completion, not acceptance by the re-review seat.
  Beads export refreshed before the explicit-path commit containing this
  record. No push or remote/Dolt sync; no sibling, worklog, public index,
  library or concurrent interpreter change is included by this editor.

## Earlier blocks (2026-10-30/31: REF completion, proof passes I-II, council round 1→2 items, pass III derivations)

Cut on 2026-10-31 (process watcher pass 3: they restated response.md and the K-row commits). Read them with
`git show 974a833:spec/isa-0.9.PROGRESS.md` or in the council artefacts under `bennett/docs/council/isa-09-2026-10-31/`.

# ISA 0.9 draft — progress file (resumable)

## VM certificate/estimate contract follow-up — 2026-10-30

Source: `bennett-vm` commit `849f7f7b66e11cbc8c6c56ecbefad9d879fe58ed`,
read-only `docs/PROGRESS.md` ("Implemented claims and exact obligations",
"Launch estimate and coverage behavior", and its verification limits),
and `bd show bennett-vm-hsd` / `bd show bennett-vm-clw` in that repository.
Read ISA 0.8 §8–§10 and §12, draft §0.2 and the ISA-7, Q14,
EPS-DECADE, BLOCK-IMAGE and ISA-REF-LIB additions; CLAUDE rules 1, 5,
8, 10 and 11 apply. No implementation code crosses repository boundaries.
Only the owned draft, this progress file, conformance and Beads export
are changed; the committing orchestrator owns its worklog. No interpreter
source/build, accepted 0.8 edit, ABI header edit, push or remote sync.

### K12 / LAUNCH-ESTIMATE — §10, §10.1, §12.3

Mirror **b-isa-spec-c15**, bug, label `isa-0.9`, source **bennett-vm-hsd**.
**maintainer decision required: request API, class keys and decimal policy**.

Proposed normative text adds `params_jcs, params_len` to the 0.9 estimate
request (also carrying explicit variant/inherited controls as in §11),
with every classical argument resolved in signature order and
no guessed zero/previous-run/hash default. Token arguments carry their
own tuples; the outer token fixes the request budget. Host and live
device-minted tokens are admitted, with tuples copied while valid. Scheduling uses
matching object bindings or §11 defaults, never a selected basis run in
place of the padded generated realisation. Every resource is reported:
scalar count/time and one occupancy/peak row per target class (zero rows
included), using injective UTF-8 percent-escaped keys. Rational aggregation
stays exact; display rounds upward to 34 significant digits, with a
canonical finite decimal spelling. Certificates bind the resolved request
and effective realisation, contain exact reduced rational rows, and must
recompute them and their displayed enclosures. The existing expansion
library gate remains; no end-to-end estimate implementation is claimed.

The maintainer has materially different, non-narrowing choices:

- **API/defaults:** the printed proposal changes the versioned 0.9
  signature and requires a complete explicit vector (`[]` only for no
  arguments). Alternatively keep the four-argument function and add a
  separately named bound-request function or request object carrying
  concrete parameters; the old entry must resolve a published concrete
  binding (not invert `params_hash`), or forward to the explicit entry.
  Both must support every well-typed parameter vector. Neither invents
  one basis input or drops parameterised estimates.
- **Class representation:** escaped flat keys preserve `estimate_get`'s
  pair-of-strings accessors; a class-aware accessor with resource and
  class returned separately preserves the same vector. These have
  different ABI/consumer shapes; scalar summation is not an alternative.
- **Decimal policy:** the printed proposal uses a fixed 34-digit upward
  enclosure plus exact rational certificate values. A request-selected
  precision with an explicitly bound rounding/enclosure policy is also
  sound and supports every rational cost; it produces different bytes
  and requires an extra request/certificate field. 0.8 chooses neither
  the precision nor the direction. Fixed nearest rounding would need a
  separately published error enclosure and could not serve as an upper
  bound by itself. No policy may call a finite decimal exactly 1/3.

Witness: §10.1 `LAUNCH-ESTIMATE witness` assumes independently specified
live intervals of duration 1/3: class A peak 2, class B] peak 1, idle
peak 0, occupancies 2/3, 1/3, 0; separate rows escape B] as B%5D.
The two nonterminating values round upward at the final digit only.
This is aggregation arithmetic, not a guessed padded gate count.
`G-estimate-resolved-class-decimal` records the 0.8 contract gap and is
**unavailable pending 0.9**, naming both source and mirror beads.

### K13 / CLAIM-REPLAY — §9.2, §12.1–§12.3

Mirror **b-isa-spec-9uy**, bug, label `isa-0.9`, source **bennett-vm-clw**.
**maintainer decision required: sampled default, invocation and tuple encoding**.

Proposed normative text gives sampled claims an explicit `expected`
relation (oracle, table or linked reference program) and subject; the
checker independently computes both sides and compares complete tuples,
clean workspace and permutation phase where asserted. A reference-only
claim is distinguished from a schedule-bound realised claim. Canonical
rows include every interface input/target/fault, dirty bundle and cell.
Standalone table/program/structural replay binds resolved `args` and
budget explicitly; parameter-uniform structural claims can bind
`args: "all", budget: "all"` only with every side condition checked
universally, retaining generic library/adjoint/translation proofs.
Scheduled certificates bind the root and resolve all nested contexts,
including defaults. The exact K4 inverse-pair domain /
arg_tokens binding remains authoritative and is not replaced by one
sample argument. Typed unsigned decimal bit-vectors, binary64 bit-pattern
hex and token tuples give a precise JCS params_hash preimage. Evidence
coverage counts distinct draws; sampling remains evidence at full coverage.

The maintainer has materially different, non-narrowing choices:

- **Sampled default:** the proposal requires `expected` and supplies no
  omitted-field default. Alternatively omitted `expected` can mean
  `"oracle"`, with an explicit schedule-bound subject and the same
  independent oracle comparison; explicit table/program relations remain
  available. Both retain sampling and prevent identity self-comparison;
  they differ on whether the old payload is complete without that field.
- **Invocation location/encoding:** the proposal puts a resolved invocation
  on each standalone claim (or its region) and the scheduled root in
  `bindings.invocation`, hashing the canonical args array. A shared
  invocation registry with explicit ids and validated immutable records
  would support the same invocations and avoid repeated vectors; it has
  different interchange/hash/lookup mechanics. Complete typed little-endian
  hex values are another lossless parameter encoding. Neither unresolved
  bounds nor an opaque token id can replace concrete replay bindings.
- **Tables:** the proposal uses complete positional before/after tuples
  and a row for every element of the declared domain, even for sampling;
  the independent program relation remains compact for large domains.
  Fully named complete tuples, or a keyed table limited to the distinct
  sampled inputs with mandatory total lookup for those draws, are also
  non-narrowing relations, with different size/order/coverage contracts.
  Dropping arbitrary target/fault or dirty/cell components is not sound.

Witness: §12.1 `CLAIM-REPLAY witness` uses x=1, a=2, initial target=2,
fault=3; the two-row add/retval oracle at B=2 commits payload 3, so the
final target is 1 and fault remains 3. Identity self-replay would miss
this difference. a=1 instead gives target 0; B=1 gives fault 2. One
preserved dirty bit and two preserved two-bit cells remain in the full
11-bit domain. Four singleton samples consume zero generator words,
cover one of 2048 tuples, and give evidence. §12.3's additional
`CLAIM-BINDING witness` hashes an i128 value >2^64, negative-zero f64
bits and a token tuple; +0 changes the hash, a token id cannot enter it.
`D-sampled-relation-invocation` is **unavailable pending 0.9**, naming
both beads, and invents no 0.8 replay CLI or executable certificate.

Both mirrors stay OPEN pending maintainer decisions and accepted 0.9.
These entries add capability contracts; no NorthStar certificate, @cost,
full-domain proof or padded SQLite/kernel estimate scope is removed.

Verification: the extended independent witness test failed before the
LAUNCH-ESTIMATE witness existed, then passed. Python Fraction/Decimal
checks reconstruct exact class aggregation and upward rounding (including
decade carry and a >34-digit integer), table XORs, binding-sensitive
outcomes, distinct coverage and the parameter hash without importing VM
or interpreter code. Headless offline `cargo test` passes all **25** Rust
tests; the full 0.8 harness reports **445 pass, 0 fail, 48 unavailable**
(**493** cases), exit **2**, including the two new contract-gap cases.
Exact commands and observed binary fingerprint are recorded at the top
of `conformance/PROGRESS.md`. Draft witnesses are not 0.9 executor conformance.

Accepted 0.8 SHA-256 remains
`90e61d9c377c939fe9652758f61cd5ead068ef06e4e40d812d3f3c5197ab605e`.

## VM milestone 4 follow-up — 2026-10-30

Resumed the uncommitted implementation after the infrastructure outage.
Source context: read-only `bennett-vm/docs/PROGRESS.md`, `HANDOFF.md`, and
`bd show bennett-vm-47t bennett-vm-cxg bennett-vm-clh bennett-vm-47i` from
that repository. No VM or reference-interpreter source was edited.

Draft additions, all recorded in §0.2:

- **K9 / EPS-DECADE**, §8.1, mirror **b-isa-spec-f31** (VM cxg, open):
  zero-based min{j ≥ 0: eps·10^j ≥ 1}, exact rational comparisons,
  requested share, domain (0,1], unbound/out-of-array errors, and the
  exact-entry prohibition. The six printed boundary cases give indices
  0,1,1,2,3,4. This is a proposed 0.9 definition, not a guessed 0.8 rule.
- **K10 / BLOCK-IMAGE**, §7.3, mirror **b-isa-spec-0d0** (VM 47i, open):
  decode the named data symbol's hex in textual order into contiguous
  complete 512-byte sectors, with partial images rejected at device
  initialization before execution; empty/absent images, present zero
  sectors and absent-sector reversal are explicit. The 1024-byte witness
  distinguishes present zero, present ff and absent sectors.
- **K11 / ISA-REF-LIB**, §11.1, mirror **b-isa-spec-8r4** (VM 47t, open):
  **maintainer decision required: decomposition set and hash rule**.
  Proposed JCS serialization, ISA/library-versioned LF envelope, full-payload
  SHA-256 rule, expansion order, ordinals, scratch identities, removable
  subset and decomposition families cite their motivating 0.8 sentences.
  The single two-bit qxor recipe is only a witness: its four-line envelope
  hash is `299510fd67cc626fdcbcc10adcd40730f9af294ba596d86fb25fd31be08a5c7f`.
  No complete catalog, full-library hash, `ref/` directory or 0.8 artifact
  is published. Publication waits for the maintainer decisions and accepted
  0.9; implementation/catalog correctness and full-domain T3 remain required.

**b-isa-spec-1pl** mirrors VM clh and is closed after fixture verification.
It corrects conformance data under existing 0.8 §8.1, not the rule: canonical
target bytes have no trailing LF; the invalid exact entry now actually
references eps, and a separate constant-cost exact entry must accept every
share. The expected hash already described the no-LF bytes: the old file
hashed to `52cd3dcd6ca4634f311f4ba0b15806c52763e70504f1220ef5c2d64d10676ecb`,
while the corrected file hashes to the existing expected
`71e1973c642abe3ea4ae5b4c7211fd4e2b2b7817894ca958d138c992cc321596`.
The VM report's claim that the expected hash included LF was not reproduced.
All four mirrors are bugs labeled `isa-0.9`; only clh is closed.

Verification: the added fixture, precise-probe and witness tests failed
against a copy of committed baseline files under `conformance/.tmp/resume-red/`.
The inherited parser also accepted an empty alternative; a new regression
failed before validation was added. Green: all **25** conformance Rust tests,
including independent exact-rational/sector/witness-hash and 16 forward/reverse
qxor tuple checks. No 0.9 executor conformance is claimed. Full reference run:
**445 pass, 0 fail, 46 unavailable (491 total), exit 2**. Library-dependent
cases retain unavailable reasons naming b-isa-spec-8r4. Exact headless commands,
reference binary fingerprint, staging limits and per-suite counts are in
`conformance/PROGRESS.md`. `include/README.md` records the library gate;
no ABI declarations were changed.

Accepted 0.8 SHA-256 remains
`90e61d9c377c939fe9652758f61cd5ead068ef06e4e40d812d3f3c5197ab605e`.
The older progress entries below are historical; the separate tracked
`spec/isa-0.8-to-0.9.diff` is outside this task's owned paths and is not regenerated.

Job: bead `b-isa-spec-so1` (claimed). Brief: `docs/briefs/2026-10-29-isa-09-draft.md`.
Owned paths: `spec/Bennett-ISA-Spec-0.9.md`, `spec/isa-0.8-to-0.9.diff`, this file, bd notes/creates
(label `isa-0.9-candidate`). Never touch `spec/Bennett-ISA-Spec.md`, `spec/README.md`, `reference-interpreter/`,
`docs/`, `worklog/`, `HANDOFF.md`, `CLAUDE.md`. Commit owned paths after every group
(`git commit -- <paths>`, retry on index.lock); never push. Headless.

Method: the draft started as a byte-for-byte copy of 0.8 (sha256 `90e61d9c…605e`); every change is a surgical
exact-string replacement applied by a script that asserts each old string occurs exactly once
(scripts kept in the job scratchpad; the diff `spec/isa-0.8-to-0.9.diff` is regenerated before each commit).

## Sources read in full (2026-10-29)

CLAUDE.md; spec/README.md; spec/Bennett-ISA-Spec.md (0.8, all 1,675 lines); the evidence note and its progress
file; the budgets note; reference-interpreter/SPEC-QUESTIONS.md (13 entries at reading); the interpreter council
round-1 report (fable R1-B1..B3, codex B01..B20, muse B1..B7 and all suggestions); dialect outline §6, §11, §17,
§25 and part B B-BLK; north star §0, §3.1, §4, §5, §8, §9; rubric-isa.md; HANDOFF "What made the ISA rounds
converge"; all open beads (`bd list`; I-, ISA-, G-, BLK-relevant and the 16 r8 children).

## Plan of §0 entries

Group 1 (editorial repairs, local semantics unchanged unless marked):
- V   version 0.9 everywhere (header, status, every sub-version, abi, device versions, examples).
- E1  I8 row indices (§3.6, §4.2 qjumpr, SPEC-Q 1).
- E2  SCC group ordering of the index space (§3.6; b-isa-spec-was; SPEC-Q 7).
- E3  ISA-10 direct versus cyclic hashes (§9.2; rejects zsw.11).
- E4  empty data spelling (§16.1; b-isa-spec-oim; SPEC-Q 9).
- E5  I4 logical history; active versus audit history; "retired" (§7.4; zsw.3, zsw.10).
- E6  uncall summary aligned with §7.4 (§4.1; zsw.1, zsw.9).
- E7  invocation contexts from the realised invocation tree (§12.1; zsw.2, zsw.7).
- E8  approximate SDP witnesses, δ margin (§12.1; zsw.6, zsw.12) and Tr_out convention note (zsw.13).
- E9  T4 hypotheses (§14.3; zsw.3, zsw.8) — final wording after ISA-8 (group 2).
- E10 borrow_demo positive vector (§16.3 example 3; zsw.15); suite D witness vectors (zsw.4 part).
- E11 qreg values through call/ret/br; per-register state; aliases (§3.3; dialect wording item).
- E12 qreg.slice lo literal or run-time (§3.3; ISA-5 wording).
- E13 entropy code 10 not "R only" (§5.4; dialect §11.3).
- E14 effective fault cause for literal 0 (§3.6, §4.2, §5.4; b-isa-spec-7qu) — SEMANTIC.
- E15 call-tier policy table (§3.1/§4.1; council B20).
- E16 SPEC-QUESTIONS closures 2,3,4,5,6,8,10,11,12,13 (each its own sub-entry).
- E17 council-found ambiguities: widths (R1-B1/B01/muse B1), canonical literals everywhere (R1-B2/B12/muse B2),
      region call graph acyclic incl. lifted calls and qinplace (B02), local regions as call operands (B06),
      matched uncall LIFO matching (B08), pointer args (B10), definition order independent of block text
      order (B11), load/store suffixes iN only (B12), call operand spelling (fable s2), interface-region names
      distinct from symbols (fable s9), qstore value / address operands as `in`-wire uses (fable s10, muse B4),
      param role suffixes (muse s3), lift.free matches unpinned entries only (fable s1) — the last SEMANTIC (corner).
- D   r8 suggestions deferred: zsw.4 (rest), zsw.5, zsw.14, zsw.16 → §17 with defaults.

Group 2 (capability contracts, SEMANTIC):
- K1 BLK-1 qreg[*], qreg.new run-time count, qreg.width, qreg.id, qreg.from_id, register ledger, binding checks.
- K2 BLK-4 qreg.new/free/slice/concat (and K1's ops) in R, with history and reversal.
- K3 BLK-2 budget.mint (CC and R), token rules.
- K4 BLK-3 qinplace with (ins..) (mem..) (args..), inverse-pair claim, §6.1 transfer, run-time claim check.
- K5 ISA-7 CC/R cause table (§4.9), explicit `fault C` in CC/R.
- K6 ISA-8 terminal R faults, FAILED → REVERSED, T4 eligibility.
- Examples 4–9 (one per family) + republished 1–2.

Group 3 (optional efficiency): I5, I1 → §17 with full-history default and the hook; every other `efficiency`
item recorded in §0 as considered and deferred with its 0.8 construction.

## Status

- [x] group 1   - [x] group 2   - [x] group 3   - [x] hostile reread and fixes (own + independent reviewer)   - [x] final diff + commit

## Decisions (with reasons) — appended as taken

Group 1:
- G1-a (E2, SCC order). Key of a one-member SCC = its member's closure hash (self-recursive or not); key of a
  multi-member SCC = its closure scc_hash. This is the reading SPEC-Q 7 implemented and muse round-1 s1 proposed.
  DEPARTURE from the evidence note, which keys every *cyclic* group (including a self-recursive singleton such as
  `sum`) by scc_hash: both are total; the interpreter's keeps 0.8's literal "ordered by closure hash" for every
  singleton, so no existing single-lproc object changes its labels under either reading, and it is what the
  only implementation does (brief: interpreter reading unless it contradicts the spec).
- G1-b (E16.9, const literals). SPEC-Q 12 reads every const literal modulo 2^N. DEPARTURE from SPEC-Q 12: the draft
  requires −2^(N−1) ≤ c < 2^N (value c mod 2^N), following round-1 fable R1-B2 (`lift.const.i8 257` silently became
  1). Stricter than the interpreter, not than 0.8's text (0.8 states no range); no value becomes unwritable
  (every residue has a spelling in range). North-star citation for the stricter rule: §0 "never a silent wrong
  answer"; CLAUDE.md rule 1. Open question Q2.
- G1-c (E17.9, call spelling). `call @f a b` (bare operands, the §4.1 form and the interpreter fixtures); the
  parenthesised form is ill-formed for `call` (it remains the form of `uncall`'s two lists, of `lift.call` and of
  region calls). Round-1 fable s2 found both accepted.
- G1-d (E17.5, matched uncall). LIFO matching; suite F rejects a pair only for an intervening write to an `ins`
  location. 0.8 also listed "cells" as a static check; dropping it is safe because `lift.oracle_uncall` is the same
  permutation as the call (§4.2) and prefix reversal undoes an unmatched clear. Broader than 0.8 (accepts more).
- G1-e (E17.13, lift.free). match_i gains ¬pinned_i; the flag is the same boolean as 0.8's. Derivation D4.
- G1-f (E14, fault 0). Effective cause C′ = 4 for literal 0 (evidence note proposal, verified D8). Syntax kept.
- G1-g (E15, tiers). Table: CC calls CC/R; R calls R; uncall of CC or R segments from CC, of R from R. R→CC is
  ill-formed (0.8 §3.1 draws none; the interpreter's registers.bisa relies on it: flagged to the interpreter
  agent via a bead, not edited).
- G1-h (E17.12, role suffixes). Optional on wires, equal to the group role when present; required on regions.
  The permissive reading keeps both spellings seen in the evidence note and the fixtures legal.
- G1-i (E16.8, frame descriptor JSON). Scratch is always `{clean, dirty}` per class (SPEC-Q 11 said "may separate";
  one canonical shape avoids two encodings of one descriptor).
- G1-j zsw decisions: accept .1 .2 .3 .6 .7 .8 .9 .10 .12 .13 .15; .4 accepted in part (the two witness vectors go
  into suite D; the controlled-action target/schedule/certificate fixture waits for `ref`, §17 item 7); reject .11
  (contradicts the published inc8 bytes; verified D1b); defer .5 (citation not verified here), .14 (ref library
  artefact), .16 (topology: §17 item 15).

## Derivations (written before any number is stated in the draft)

D1 (E1, inc8 indices). inc8's one block has rows const, add, retval at indices 0, 1, 2; n = 3, HALT = 3; the
smallest P with 2^P > 3 is P = 2. Each row is one step: retval executes at step 3, so B ≥ 3 succeeds and B = 2
ends with pc = 2 ≠ HALT, committing FAULT_BUDGET_STEPS (the published results, unchanged).

D1b (E3, hashing). Recomputed here with hashlib from the printed 0.8 envelopes: SHA-256(inc8 envelope) =
8ce5e64f…be93 = the published hash (direct); SHA-256(hex ‖ ":0") would be 5f3e8bcd…8ee8 (≠ published), so zsw.11
contradicts the vectors. SHA-256(sum envelope) = c6d549be…bc31 and SHA-256("c6d5…bc31:0") = 74f110bb…cd92 = published
(wrapped). zero: SHA-256("isa=0.8\nptr_width=32\n{…data sig…}\nzero 00\n") = 7002ed5e…67e6 = published (direct).

D3 (E16.3, counter widths). Reachable bounds, from the flags of §3.7/§4.2 (a counter is only advanced when its
flag is clear): heap_used ≤ heap_limit ≤ heap_limit_max, and the heap range lies in [0, 2^H) (§7.2), so
heap_used < 2^H < 2^(H+2); atop advances only while atop < 2^A_tab, so atop ≤ 2^A_tab < 2^(A_tab+1); sp + R_f ≤
stack_limit ≤ 2^S_cells, so sp ≤ 2^S_cells < 2^(S_cells+1), and fp ≤ sp; depth ≤ depth_limit, and Dc =
⌈log₂(depth_limit + 2)⌉ gives 2^Dc ≥ depth_limit + 2, so depth ≤ 2^Dc − 2 (which also makes §5.4's check
depth_limit < 2^Dc − 1 hold for the minimum Dc). Hence every value fits the minimum widths and a wider counter
holds the same value: F_B does not depend on the choice; only W_cell = max(P, Sc, Did, W_max) and the resource
count do, so the reference realisation fixes the minimum.

D4 (E17.13, lift.free). Heap entry j has base heap_base + Σ_{i<j} max(n_i, 1) (§7.1, §4.2 lift.alloc): strictly
increasing in j because max(n_i,1) ≥ 1, so heap bases are pairwise distinct. Pre-entries (globals, interface
regions) are pinned. Hence at most one unpinned entry has base p, and match_i = (i < atop) ∧ (base_i = p) ∧
¬pinned_i selects at most one i. flag = ¬∃i: match_i ∧ live_i equals 0.8's ¬∃i: (i<atop)∧(base_i=p)∧live_i∧¬pinned_i.
Under ¬flag, live_i ^= match_i flips exactly that entry. match_i reads atop, base_i, pinned_i, none of which the row
changes, so recomputing it uncomputes the scratch (the D-row inverse is the same three sub-operations reversed;
including live_i in match_i would break this, which is why the fix uses ¬pinned_i). 0.8's flip set additionally
contained every pinned live entry with base p: a size-0 global at the freed base (size-0 ranges are disjoint from
every range, §7.1) lost its live bit, after which `lift.boundscheck g 0` (inrange(g,0) needs a live entry with
base ≤ g ≤ base) faulted where it should not. No published object has a size-0 global.

D5 (E16.9). The range −2^(N−1) ≤ c < 2^N contains exactly the signed and unsigned spellings of the 2^N residues.

D6 (E10, borrow_demo). Wires (t, x, b); gates in order V = cx x b, W = cx b t, V⁻¹ = cx x b, W = cx b t.
b → b⊕x; t → t⊕(b⊕x); b → b; t → t⊕(b⊕x)⊕b = t⊕x. Final (t⊕x, x, b) for all 8 basis inputs; b restored, so by
linearity identity on any reference entangled with b. Under an inherited control w every gate is controlled by
w: b⊕wx; t⊕w(b⊕wx); b; t⊕w(b⊕wx)⊕wb = t⊕w·x (w² = w). Side conditions: V's only gate targets b ∈ B with control
x ∈ X = {x}, X ∩ B = ∅; W's gate targets t ∉ X ∪ B ∪ {b} (W's controls), W writes no wire of X; W's gate has one
control in B; V⁻¹ is V reversed; no swap. The map is an involution (applying it twice gives t⊕x⊕x = t), so the
adjoint (reverse sequence cx b t; cx x b; cx b t; cx x b: t⊕b; b⊕x; t⊕b⊕b⊕x = t⊕x; b) realises the same permutation;
its frame is not of the lemma's V;W;V⁻¹;W shape (it starts with a gate targeting t), so it is covered by the
`adjoint_table` structural rule, not by the lemma. bounds = [1] (one qloop with trip count 1).

D7 (E10, suite D witness vectors). d = 2, identical channels, J(Φ) = 0. Y = I₄/8: Y ± J = I₄/8, LDL† pivots all
1/8 > 0. Tr_out(I₂ ⊗ I₂ / 8) = (2/8)·I₂ = I₂/4. μ = 3/8: μI − Tr_out Y = (3/8 − 2/8)I₂ = I₂/8, pivots 1/8 > 0;
μ = 3/8 ≤ bound = 3/8: accept; then ‖Φ‖◇ ≤ 3/8 (true, Φ = 0). All entries are dyadic, so interval arithmetic at any
precision_bits ≥ 4 is exact. Negative: Y = 0, μ = 0: Y ± J = 0 has pivot 0, not strictly positive: reject (although
the channels agree), exactly as §12.1's strict-pivot rule requires.

D8 (E14, effective cause). Q: row writes code ^= flag·C′ with C′ = 4 when C = 0; F ≥ 4 so 4 < 2^F. The first
fault halts (successor HALT), so code holds exactly one C′ ≠ 0 on a faulted path; commit XORs it into fr. Inverse
uses the same C′, so prefix reversal is unchanged in form. Example 9 (group 2) derives its outcomes.

D9 (E8, approximate witnesses). Given certified λ_min(Y−J) ≥ −η₊, λ_min(Y+J) ≥ −η₋, λ_min(μI − Tr_out Y) ≥ −η_s and
δ > max(η₊, η₋, η_s): Y′ = Y + δI_{d²} gives Y′ ± J ⪰ (δ − η±)I ≻ 0; Tr_out(δI_{d²}) = δ·d·I_d, so with μ′ = μ +
(d+1)δ, μ′I − Tr_out Y′ = (μI − Tr_out Y) + δI ⪰ (δ − η_s)I ≻ 0. (0.8's recipe is the case η = 0.)

## Hash placeholders

Every hash in §16.3 of the draft is `<to be computed by the 0.9 precheck>`: the reference binary
(`reference-interpreter/target/debug/bennett-isa-ref`) hard-codes `0.8` in its header, signature and envelope
checks (src/object.rs:708, :975, :1017; src/identity.rs:258), so it does not accept the 0.9 version string even
for unchanged bodies, and it has no 0.9 instructions. The crate was not edited.

Placeholders are **distinct per example and symbol** (`<to be computed by the 0.9 precheck: example k, name>`),
because the seed's `--repatch` maps old string → new hash by plain replacement: one shared placeholder would map
every symbol to the last hash computed. Full list (count of occurrences in the draft):

| placeholder (example, symbol) | occurrences | where |
|---|---|---|
| 1, inc8 | 2 | ex 1 symbols line; ex 2 hash list |
| 2, zero | 4 | ex 2 symbols line, hash list, sum envelope (`@…` and part-(6) line) |
| 2, sum | 2 | ex 2 symbols line, hash list |
| 2, sum_db | 2 | ex 2 symbols line, hash list |
| 3, borrow_demo | 1 | ex 3 symbols line |
| 4, ones / 4, flip | 1 each | ex 4 symbols line |
| 5, main / 5, scratch / 5, flip | 1 each | ex 5 symbols line |
| 6, adaptive / 6, overdraw / 6, inc8 | 1 each | ex 6 symbols line |
| 7, g / 7, ginv / 7, addya / 7, run | 1 each | ex 7 symbols line (plus `<closure hash of g>`, `<closure hash of ginv>` in the prose certificate fragment, which the precheck fills when it generates the certificate) |
| 8, main / 8, work | 1 each | ex 8 symbols line |
| 9, zero_cause / 9, zero_cc | 1 each | ex 9 symbols line |
| 10, through / 10, worker / 10, plus_db / 10, flip_arg | 1 each | ex 10 symbols line (Q14 continuation) |

**Cross-check values (NOT normative, not in the draft).** Computed by importing the *unmodified* seed
`reference-interpreter/isa_check.py` (functions `extract_examples`, `parse_object`, `compute_hashes`) on the
draft text before the placeholders were made distinct; examples 2 and 10 were recomputed after Q14. The seed has no CC/R closure set and no part-(5c) device
lines, so examples 4 and 8 (CC/R functions with a layout; example 8 also a device) are omitted as unreliable;
for the others the seed's model is complete (oracle, lproc, data, action, and memoryless CC/R with no devices).
The 0.9 precheck must compute its own values; these are only for comparison.

```
ex1 inc8        ed9865300b85a519c2379de98e36e635e72b5b78d8bdfca03dccf9a09aa3df5e
ex2 zero        43e032f98d7aff20f6864d6368b20ab4ef9d810938999acff8d71ed16e6b17d7
ex2 sum         498cfae2ec3e3d3322997010572345b34be5459fb7ad69edc5c9e51e10dc1e00
ex2 sum_db      443e5ab7fd4f005efbde4664972d709b0e9c7995eb8842271aebbdc78a52570f
ex3 borrow_demo 6f4782e9bde4267acd1afddd650093722a056d9d50ee465b79cb86a4606b2a94
ex5 flip        3860ea712b2d70fc495834586bb397656a467c85235aa069768318a06e9fa89b
ex5 scratch     05525834cbe5a518aa97444912254f3c12c75dd86314a98ba550f45187208a0b
ex5 main        5cebd5a72ee7873edda0d2c35afed2a5ab79eba60f2b242b2a856d5fa4074634
ex6 inc8        ed9865300b85a519c2379de98e36e635e72b5b78d8bdfca03dccf9a09aa3df5e (= ex1, as it must be)
ex6 adaptive    b80aed1639a9ac6a6856f02b0b3264d905e4eea3fa3f9081c01e56283ea398cf
ex6 overdraw    c0d9835844fa882c1864044acc6fa26dba3935e0d6a9d33f9cdbf1e7c877d250
ex7 g           0d65d926275688cfebf2831c1de960b03a6b8ea6400866e6d9fef8f393ca2c2e
ex7 ginv        786f1970ca3d78ef3d5de795411ee276286711c89b756872757c24f9bd569cc9
ex7 addya       5999b6d3d2362f8c1971ef6f37b404766aa5c18f6ba1880d767bfde351e47392
ex7 run         562ab7270a0f508d6a2f4a757f3f90964da0b60541bac2c5efa421bad009056a
ex9 zero_cause  badf7dd2a59afa879f092921946539dfb918cedd35f6fbbaa838c630577eaed4
ex9 zero_cc     0403d76ff065acab57cb9165cfe1d3d73bbf8dad60bbc1348fb0305ee4f37611
ex10 plus_db    cab2fb72ce9ebea9f5942ca9956e4f1906535f095c6cf0a840f45bf4baa37c5a
ex10 flip_arg   bfa13d9a564e3f8562098c4ea39330d947efa64521310afad6a329dc594bd671
ex10 worker     ab885fe1ec4d35b98ddb1cfbcde0ad18e747343af5155bb2beff1aa618fc1563
ex10 through    fbd06a460dd2bf2cd6b19ab101f023f1ed2002eaf35117ac2e83c52dce4ac76c
```

Precheck notes: the seed's printed-table regex needs 64-hex values (the placeholders will fail it until
patched, as intended); its `--repatch` and its executable checks of inc8/sum_db need `0.9` acceptance; examples 4–10
need a 0.9 interpreter (new instructions) — the brief forbids changing the crate here.

## Open questions for the maintainer (each with a recommendation)

Q1 SCC order key of a self-recursive singleton (E2): its member closure hash (SPEC-Q 7, adopted) or its scc_hash
   (evidence note)? Recommend the adopted reading: it is what the interpreter does and keeps 0.8's wording.
Q2 Const literal range (E16.9): reject literals outside [−2^(N−1), 2^N) (adopted, RC fable R1-B2) or read every
   literal modulo 2^N (SPEC-Q 12)? Recommend the range; the interpreter fix loop should align.
Q3 R faults terminal (K6) versus "an R call returns a fault status to its CC caller" (DL B-BLK ISA-8 row, which
   contradicts DL §17.6). Recommend terminal now; a catch API, if ever wanted, is an addition, not a change.
Q4 budget.mint in R as well as CC (K3; departs from EN and DL). Recommend yes (BLK-4 analogue; R is classical).
Q5 qreg.from_id pure (K1; departs from EN and DL). Recommend pure: it keeps the compute–copy–uncall idiom able
   to look up handles; dangling aliases after an uncall trap deterministically.
Q6 qinplace inverse-pair check at the CC/R call (run-time trap 4) rather than "ill-formed object" (EN). Recommend
   the run-time check: tokens and args are run-time values, so applicability is only decidable at the call.
Q7 Token-to-region binding (K3, bd 8wn): any region call of the program may use any token. Recommend as drafted
   (the §5.4 checks are object-level); the alternative (trap on region mismatch) adds a check with no benefit.
Q8 Registers wider than 128 bits cannot be measured directly (bd 04w). Capability kept by copy + measure + reset;
   recommend leaving `qreg.split` / wide measurement as an efficiency item for 1.0.
Q9 §17 item 14 (K7): accept the reconciliation (hardware releases unverified, excluded from uncall/reversal)?
   Recommend yes; 0.8's default was untestable.
Q10 E17.5 drops the static "cells" check between matched lift.oracle_call/uncall (accepts more). Recommend yes
   (sound: the uncall is the same permutation; prefix reversal cleans an unmatched clear).
Q11 E17.13 lift.free/free flip only unpinned entries (semantic corner change). Recommend yes (0.8 killed a pinned
   size-0 global's entry, making a later boundscheck of length 0 fault wrongly).
Q12 Hashes: keep placeholders until the 0.9 precheck exists (as the brief says), or accept the cross-check values
   above now? Recommend placeholders: the seed lacks CC/R closure sets and device lines (examples 4, 8).
Q13 Deferred r8 items (zsw.4 rest, .5, .14, .16): recommend publishing `ref` (zsw.14) before grading 0.9,
   since the controlled-action fixture (zsw.4) depends on it.

### Group 2 decisions

- G2-a (K1). `qreg[n]` may be used where `qreg[*]` is expected; `qreg[*]` → `qreg[n]` (parameter, block parameter,
  `ret`, region slot, launch) is checked at the transfer (width = n, else trap 4, no effect). `measure` keeps the
  0.8 form for `qreg[n]`; `qreg[*]` needs `measure.iN` (width checked before measuring). Run-time width 0 is legal
  (an empty `Vec<Qubit>`); such a register can be freed, passed, concatenated, never measured (N ≥ 1) or bound to a
  slot (slot widths ≥ 1). Ids are never reassigned while the program is loaded (simplest sufficient rule for
  "reversal restores the same ids"). `qreg.slice` `len` may also be run-time (result `qreg[*]`).
- G2-b (K1). DEPARTURE from the evidence note and DL: `qreg.from_id` frames are **pure** (it changes only the
  instance set; ownership acquisition is launch bookkeeping released at CLOSED). Reason: purity lets the
  compute–copy–`uncall` idiom (§7.4) look a handle up after the call; impure would forbid it. Soundness: if the
  uncalled segment created the register, the retained alias is dangling and every use traps 4 (deterministic).
- G2-c (K2). Reversal of `qreg.new` releases without a test: the register is clean because every later frame
  touching it is undone first (LIFO) and the run owns it exclusively; simulators verify. Reversal of `qreg.free`
  re-creates it clean with the same id/class/width.
- G2-d (K3). DEPARTURE: `budget.mint` is CC **and R** (evidence note and DL: CC). Reason: the BLK-4 analogue —
  an R routine computing a budget from R data mid-run cannot hoist it to CC; R is classical, so §3.1's invariant
  holds. Mint frames are impure (they change the token ledger).
- G2-e (K3, new closure found while drafting). 0.8 never says whether a token validated for region @p may be given
  to `oracle_call @o`. The §5.4 checks depend only on the object's layout, and the evidence note's own fixtures pass
  one token to several calls. Draft: a token MAY be supplied to any region call of the program. Bead filed.
- G2-f (K4). The inverse-pair obligation is carried by a certificate claim with a budget tuple and an args domain,
  checked at the CC/R region call before any effect (trap 4 otherwise). DEPARTURE from the evidence note ("a failing
  certificate is ill-formed"): tokens and args are run-time values, so the claim's applicability can only be checked
  at the call; a run-time trap is the more permissive outcome. Monotonicity lemma D14 makes one claim cover every
  larger tuple. The short form `qinplace @g @ginv tk x` is the spelling when all three lists are empty.
- G2-g (K4). §6.1: x stays `other` if it was `other` (0.8's row gave "perm with S_x ∪ Π", undefined for other x).
- G2-h (K5). "CC trap" and "R fault record" are one event: a terminal fault record; a FAILED run has exactly one
  (0.8: "at least one"; no second can arise once the first is terminal). Every CC/R block ends in `br`, `ret`,
  `trap` or `fault` (0.8 had no CC/R terminator rule). Unclean `qreg.free` on a simulator: record 4.
- G2-i (K6). R faults are terminal (EN; DL §17.6). DL's B-BLK row for ISA-8 says "an R call returns a fault status
  to its CC caller"; that contradicts DL §17.6 and is not adopted (open question Q3).
- G2-j (K8). §17 item 14's 0.8 default ("FAILED with FAULT_UB_TRAP", for a condition hardware cannot test)
  contradicts §7.4's "qreg.free frame whose cleanliness was not verified (hardware, §17 item 14)". Reconciled: the
  hardware release proceeds unverified, its frame is marked so (no uncall, no reversal), and releasing an unclean
  register discards (traces out) its wires.

### Group 2 derivations

D10 (example 4, `ones`, n = 3). qreg.new any 3 → register R, width 3, state |000⟩, fresh id r. w = 3; id = r.
p = alloc 8 → 16 (bump starts at heap_base = 16; entry (16, 8, live, unpinned); bump 24). store.i64 16 r;
load.i64 16 → r; from_id r → q2, alias of R (live, not a view, owned by this run). Loop i = 0, 1, 2: slice [i, 1)
of R (lo run-time, len literal 1 → `qreg[1]` view), R viewed; action_call @flip flips wire i (X); view consumed,
R live. i = 3: icmp.ult 3 3 = 0 → ^done. measure.i3 q2: width 3 = N; state |111⟩ (wire i = bit i), so outcome
0b111 = 7 with probability 1; R consumed. ret m = 7: COMPLETED, one INT result of width 3 (⌈3/8⌉ = 1 byte 0x07),
one measurement record (R, bits 1 1 1). Reverse: E_NOT_REVERSIBLE (a measure frame).
n = 2: the loop flips wires 0 and 1; measure.i3 sees width 2 ≠ 3 → trap 4 before measuring: FAILED, one record 4,
no measurement, R live in |11⟩. That run is reverse-eligible (no measure frame, no free): reversal undoes the record,
then i = 1's call by adjoint (X) and slice, i = 0's likewise, from_id, load, store, alloc, the consts, width, id
and finally qreg.new (R is |00⟩ again: release). n = 0: no iteration; measure.i3 sees width 0 → FAILED, record 4.

D11 (example 5, `scratch`, R allocation). For n: R creates register Q (width n, |0…0⟩). Iteration j < n: slice
[j,1) → view, flip (wire j: 0 → 1), view consumed; slice again, flip (1 → 0). After the loop Q is |0…0⟩;
qreg.free Q: clean (simulator verifies) → consumed. ret; main ret: COMPLETED, no values. Whole-run reversal (LIFO):
main's ret; call frame boundary; @scratch's ret; qreg.free undone → Q re-created clean, same id; iteration n−1
undone: br, add, second flip's adjoint (wire n−1: 0 → 1), its slice (view gone, Q live), first flip's adjoint (1 →
0), its slice; … iteration 0 likewise; consts; qreg.new undone → Q released clean. REVERSED; ledger as at entry (Q's
id is not reused). Midway, just after the first undone flip, wire n−1 is |1⟩, which checks the order. On hardware
the free is unverified → E_NOT_REVERSIBLE. Under 0.8 the R function is ill-formed (qreg.* CC only).

D12 (example 6, `adaptive`). b = 1: select → 3; mint (3, 0, 0, 0) for @inc8: memoryless object, heap = stack =
depth = 0 required: passes. inc8 at B = 3 (D1): t ⊕= (x + 1) mod 256, f unchanged. b = 0: B = 2: (0,
FAULT_BUDGET_STEPS) → t unchanged, f ⊕= 1. Both runs COMPLETED (an oracle fault is a fault-register outcome, not a
run fault). Reverse: the region-call frame re-applies inc8 with its recorded tuple (the oracle is an involution):
t, f restored; the mint frame is undone (token revoked); select and consts removed. `@overdraw`: mint (3, 1, 0, 0)
fails heap_limit = 0 for a memoryless object → FAILED, record 4, no token.

D13 (example 7, `addya`). g: rows s = x + y, r = s + a, retval r: 3 rows, F_B = ((x+y+a) mod 4, 0) for B ≥ 3, (0, 1)
for B ≤ 2. ginv: s = x − y, r = s − a: ((x−y−a) mod 4, 0) for B ≥ 3. For fixed (y, a) both are bijections of
Z/4 and mutually inverse: (x+y+a) − y − a = x. Macro (token B ≥ 3): t = 0, f = 0; g: t = (x+y+a) mod 4, f = 0; qexch:
x' = (x+y+a) mod 4, t = x; ginv on x': t = x ⊕ ((x'−y−a) mod 4) = x ⊕ x = 0, f = 0; free t, f clean. E.g. x = 3, y =
2, a = 1: x' = 6 mod 4 = 2; ginv(2; 2, 1) = −1 mod 4 = 3; t = 3 ⊕ 3 = 0. Adjoint (pair swapped): x ← (x − y − a) mod 4.
Under an external control 0 no gate acts and scratch stays 0. Exhaustive claim: 4 · 4 · 4 = 64 elements (x, y, a),
both oracles at (3, 0, 0, 0). A token (2, 0, 0, 0) is not ≥ (3, 0, 0, 0): trap 4. Without a certificate: trap 4.

D14 (monotonicity, used by K4). Reference interpreter at tuple β₀ = (B₀, h₀, s₀, d₀) reaching `lift.retval` at
step T ≤ B₀ without a fault: the only limit-dependent decisions are the flags heap_used + max(n,1) > heap_limit,
depth + 1 > depth_limit, sp + R_f > stack_limit (all false on this trajectory) and the step bound (not reached).
For β ≥ β₀ componentwise each flag is still false (its right-hand side only grew), so the trajectory is identical
and halts at T ≤ B₀ ≤ B with the same result_val: F_β(x) = F_β₀(x) = (f(x), 0). (A faulting or exhausted run at β₀
gives no such implication, which is why claims state a minimum tuple.) Nested `lift.oracle_call`s use tokens from
classical arguments, which the claim's args domain fixes.

D15 (example 8, failed prefix). Initial: bump 16, no table entries, clock c = 0, tape empty. main: n = 8; alloc 8 →
p = 16, entry (16, 8, live, unpinned), [16, 24) zero, bump 24; call @work 16; v = 7; store.i64 16 7 → [16, 24) =
07 00 00 00 00 00 00 00 (frame keeps 00 × 8); clock.read 16 → writes c = 0 LE: 00 × 8 (frame keeps 07 00 × 7), c = 1,
tape (clock, read, 16); fault 21 → C′ = 21: terminal record, FAILED. Observable: nfaults = 1, fault 0 = 21,
nvalues = 0, [16, 24) = 00 × 8, c = 1, tape length 1; main's ret never executes. Reverse: record removed; clock.read
undone ([16, 24) = 07 00 × 7, c = 0, tape empty); store undone ([16, 24) = 00 × 8); v; the open activation of @work
and main's call frame; alloc undone (bump 16, entry removed); n. REVERSED; memory, table, clock and tape at entry.
0.8: FAILED → E_NOT_REVERSIBLE.

D16 (example 9, zero cause). `@zero_cause`: rows faultif (index 0), retval (1); n = 2, HALT = 2, P = 2 (2^2 > 2). B =
0: every x → (0, 1). B = 1: x = 0: flag 0, pc = 1, not halted → (0, 1); x = 1: flag 1, code ^= C′ = 4, faulted,
HALT → (0, 4). B ≥ 2: x = 0 → retval 0: success, result 0 → (0, 0) (t unchanged, f unchanged); x = 1 → (0, 4). In
0.8 the x = 1 outcome at B ≥ 1 was (0, 0), identical to x = 0's success. `@zero_cc`: `fault 0` → record C′ = 4,
FAILED.

Beads filed by this job: b-isa-spec-8wn (token-region binding), b-isa-spec-exc (§17 item 14 vs §7.4),
b-isa-spec-04w (measuring registers wider than 128 bits; efficiency, construction recorded).

### Group 3 derivations and decisions

D17 (I5, identity-idle variant, verified by hand before citing EN's 608-case check). Forward: a = (pc ≠ HALT);
at_k for k < n from pc (all 0 when idle); rows; successor XORs for k < n and both exchanges under a (no HALT
successor); then old_pc ^= HALT under a. Active from k: after the exchanges pc = succ, pc' = 0, old_pc = k; then
old_pc = k ⊕ HALT ≠ 0 since k ≠ HALT. Clean dispatch: at_k ^= (old_pc ⊕ HALT == k) ∧ a. Clear a: a ^= (old_pc ≠ 0) =
1 → 0. Idle: a = 0, no write, old_pc = 0, a ^= (0 ≠ 0) = 0. Inverse: a = (old_pc ≠ 0); at_k from old_pc ⊕ HALT under a;
old_pc ^= HALT under a (→ k); inverse exchanges under a (pc = k, pc' = succ, old_pc = 0); successor XOR undone (pc' =
0); rows undone as printed; at_k uncomputed from pc under a; a ^= (pc ≠ HALT) = (k ≠ HALT) = 1 → 0; idle: all zero.
A step ending in HALT (retval, fault) still leaves old_pc = k ⊕ HALT ≠ 0, so it is never confused with idle. Same
frame width (P bits), same F_B. Decision: §17 item 17 with the printed step as default (brief: no expansion fixture
with hand-derived gate-level values exists, ref unpublished).

D18 (I1). P_{j+1}(a, b) = P_j(a, c); P_j(c, b); P_j(a, c) with c clean: T(j+1) = 3T(j), T(0) = 1 → 3^k base
evaluations for k = ⌈log₂ B⌉ (after padding F to 2^k stuttering steps); one temporary configuration per level live
during the inner calls → at most k temporaries of S bits. EN's verifier checked the recurrence to level 5 on Z/4.
The bead's "polylog time" is not adopted. Decision: §17 item 18, default full history, hook in §9.4/§11.

## Verification record

- Hand derivations D1–D18 above, written before the numbers entered the draft.
- Independent hashlib check of 0.8 hashing (D1b); the printed 0.9 inc8 envelope hashes to the seed's 0.9 inc8
  value (consistency of the republished envelope).
- A small independent Python model (job scratchpad, not the interpreter) re-checked the stated results of
  examples 3 (all t, x, b, w), 4 (n = 0, 2, 3), 6 (all x, 6 target values, all f, both b, with reversal),
  7 (all x, y, a, both controls, adjoint, B = 2 failure), 8 (byte trace and reversal) and 9 (B = 0..5): PASS.
- Cross-reference check: every § reference resolves except DL §17.6 / §25 (dialect sections, labelled DL);
  §17 items 1–18 exist and every "§17 item n" reference resolves.

## Hostile review (independent reviewer agent, read-only, rubric-isa) and fixes

The reviewer re-derived every stated result of examples 1, 3–9, the suite D vector, the E8 margin algebra, the
idle-step variant, the counter widths and the lift.free match: all correct. It found 9 S0 and 13 S1 issues; each
was checked against the text and all were accepted:

- S0-1 qjumpr into a block's interior vs the kept "any other index faults" → E17.16 (range check only; interior
  rows reachable; re-indexing preserves reachable rows).
- S0-2 "ill-formed where suite F decides it" was circular → E11 now states the exact static rule.
- S0-3 inverse-pair coverage only by exhaustive claims was a narrowing (NS §3.1 promises library certificates;
  Int64 `x += a` would need ~2^128 runs) → K4 admits `inverse_pair_library` claims (no args domain = all values),
  sampled never covers.
- S0-4 monotonicity ignored nested lift.oracle_call (a nested outcome can change with its own budget) → entries
  carry exact `arg_tokens` tuples; the note now says nested rows use their own tokens.
- S0-5 orientation: adjoint `qinplace @ginv @g` would not match an entry {g, ginv} → an entry covers both.
- S0-6 minted tuples vs the single schedule line → invocations whose bindings match run the schedule, others the
  §11 defaults; tokens encoded in params_hash as their tuples (this also closes the same gap for host tokens).
- S0-7 effect memory operand out of range had no code → 7.
- S0-8 T4's quantum-state clause false for ε > 0 adjoints → exactness hypothesis stated; ledger claim restricted to
  registers the run created or touched; qreg.new reversal releases without a test (residual within bounds).
- S0-9 lifted-call args from locations would be superposed "classical" values → E17.14 (classical args only);
  consequence filed as bd 7u6 (lprocs have no token/args source); resolved by the applied Q14 edit below.
- S1s: from_id ownership not undone, host calls on owned registers E_INVALID_STATE; measure.iN on qreg[n] with
  N = n; literal qreg.new 0 ill-formed (literal n ≥ 1); slice out of range traps even when literal; executor class
  includes inverse-pair checking; "verifying executor" defined (E17.17) and used for qreg.free and host calls;
  item 16 faults before mutation; @o's role stated; ids executor-chosen; effect undo removes its tape entry;
  §0 Group 1 retitled, E11 → S, no-narrowing list completed; G-15 now realised directly (E17.1, E17.15); lifted
  suffix widths unbounded (E17.15); unmatched or path-dependent uncalls ill-formed; nits (suite letters, §3.2 wire
  store, example 4/5/8 wording).

Not changed: T1's "halts within B + 1 rows" (0.8 text, counts the halting check; no conflict with "exactly B rows
executed"); `fn` result names (0.8 convention); `bennett_qreg_new`'s `uint32_t n` (host-side allocation; device
widths are unbounded through `qreg.new`).

Q14 — **APPLIED (2026-10-29, b-isa-spec-7u6)**. The second alternative is applied: lprocs take explicit
token/classical parameters. Source: the maintainer's acceptance recorded in
`worklog/001_2026-10-28_bootstrap.md` line 26 as "the Q14 edit (lproc token/classical params)";
the orchestrator's 2026-10-29 decision selects that alternative. The draft's §0.2 now records the applied edit
and source; the earlier pseudo-location/captured-environment alternative is not the adopted mechanism.

Sections edited: §0.1 (E17.14), §0.2 (applied/source), §2 (terminology), §3.3 (argument matching),
§3.6–§3.7 (header groups, explicit forwarding, fixed binding instances, location/stack layout and charge),
§4.2 (lifted-call operands), §4.7–§4.8 (types and opcode schema), §5.1 (roles), §5.4–§5.5 (token validity,
nested budgets and matched cleanup), §9.1–§9.2 (signature, hash and link consequences), §15 (suites C/F),
§16.2–§16.3 (grammar, example 2's empty signature arrays and new example 10).

Header: `lproc @f (params..) (result) (tokens..) (classical..) (mem..)`.
Groups are `reg[N]` parameters; one `reg[T]` result; `token` parameters; `iN ptr f64` parameters;
`region[A,W] in` parameters. Optional `token` / `classical` suffixes agree with their header group.
The full call is `w = lift.call @f (a_1..a_m) (tokens..) (classical..) (mem..)`; the original one-list form
is canonical exactly when the three new groups are empty. Tokens keep their identity and validity; classical
values remain fixed before oracle entry. Instantiating each lproc for the finite set of forwarded entry-binding
keys handles different coherent call paths and recursion without selecting classical data from wire values.
The fifth group forwards mapped regions so every lifted call available to an oracle remains available in an
lproc, including calls with memory interfaces. Bindings add no rows, captures or stack cells; ordinary
`lift.call` / `lift.ret` and lifted region-call charges remain unchanged. Nested oracles use their explicit
token's tuple, not the enclosing oracle's tuple. The required signature arrays `tokens`, `args`, `mem`
(including empty arrays) and canonical operand lists enter existing identity/hash rules.

D19 (Q14, hand derivation and independent check). Example 10 has two outer rows and six worker rows:
call, nested oracle call, const, compare, faultif, permutation call, ret, retval = 8 executed outer steps.
The worker has five locations, hence R_worker = 3 + 5 = 8 cells; token/classical/region bindings add none.
Binding key [0,1,0]; HALT = 8, P = 4. The nested oracle has six rows and computes
(x + a + (d mod 4)) mod 4, and the permutation action XORs bit 0, giving that value XOR 1. Outer B = 7
misses retval (code 1); stack_limit = 7 or depth_limit = 0 faults at the first call (code 3); nested B = 5
returns code 1, propagated by faultif at outer step 5 as code 9. The two mapped bases (16, 17) alias the same
passed region cells across invocations; neither passes a location as a classical argument.

Q14 verification (headless, only the two owned Markdown paths edited):
- The independent Python row model reads example 10's printed instruction lists: all 4,096 (x,a,d) inputs
  pass eight budget/boundary cases; all 262,144 input/target/fault tuples satisfy the XOR involution.
  This checks the numerical witness, not an implemented 0.9 executor or a full circuit-level inverse.
- Recursive binding forwarding closes on a finite, deterministically ordered key set in an independent model;
  17 complete JCS metadata/envelope lines parse and are canonical; all printed lproc signatures carry the
  three new arrays. Example 10's row counts, header and forwarding lists match the derivation.
- `python3 /home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/isa_check.py`:
  PASS (two accepted 0.8 example objects, their hashes, two envelopes and stated execution).
- The unmodified seed parses all ten objects and computes their hashes as a structural cross-check;
  example 2's changed lproc/caller hashes and example 10's hashes are recorded above as non-normative values.
- Draft SHA-256: `25641147f345491a69a27208e4cbd1812011a364daf3e1821c31a8e1562233f0`.
- The 0.8→0.9 unified diff is regenerated in memory: 2103 lines, SHA-256
  `8ede5c269a6b455656f68312b9f792614246c680a69c4ce9b9ea03b386eded79`. The earlier
  job's tracked `spec/isa-0.8-to-0.9.diff` is outside this task's two owned paths and is not rewritten.
- The accepted 0.8 file's SHA-256 remains
  `90e61d9c377c939fe9652758f61cd5ead068ef06e4e40d812d3f3c5197ab605e`.
- `git diff --check -- spec/Bennett-ISA-Spec-0.9.md spec/isa-0.9.PROGRESS.md`: PASS.

Remaining lproc mechanics: none deferred by Q14. Implementation and the 0.9 precheck (including executable
conformance for example 10 and hash patching) remain pending under the draft's existing gate; this task does
not change the read-only reference interpreter. General §17 defaults (notably the unpublished `ref` expansion
bytes and optional checkpointed realisations) continue to apply to lproc rows as to other lifted rows.

## Ratified decisions applied — 2026-10-30

Binding source: the complete maintainer decision memo, Ratification section,
2026-10-30; execution brief: docs/briefs/2026-10-30-isa-09-ratified-edits.md.
This section supersedes the historical proposal/open-choice language above.
Bead b-isa-spec-2c9 tracks this sole-editor text pass. No accepted 0.8 or
interpreter files are edited; the orchestrator owns worklog updates.
Baseline: 25 Rust tests green; full 0.8 harness 445 pass / 0 fail /
48 unavailable (493 cases), exit 2.


| Memo item | Section edited | Conformance witness | Status | Commit |
|---|---|---|---|---|
| A2 / LAUNCH-ESTIMATE | §10, §10.1, §12.3 (K12) | G-estimate-resolved-class-decimal (retained) | Applied, pending accepted 0.9 | `2e3ecd2ca4d96008bedfd429fbbf2a30c8e2f8f9` |
| A3 / CLAIM-REPLAY | §9.2, §12.1–§12.3 (K13) | D-sampled-relation-invocation; CLAIM-BINDING (retained) | Applied, pending accepted 0.9 | `0e72b63adaa5ee5f446706f0ef628f1165d4e57a` |
| A1 / ISA-REF-LIB; B6 | §11.1, §17 item 7 (K11) | E-ref-09-qxor-witness; retained qxor envelope | Applied, pending accepted 0.9 | `d9922bffe31b4aa4268c59b396a1a63eb969ffb0` |
| A6 / topology | §8.2–§8.3, §11, §17 item 15 (K14/D1) | E-topology-grid-09 | Applied, pending accepted 0.9 | `679eae0b8b64dadc1b7c3105b07635058a868d85` |
| B1 / multi-block actions | §5.3 (K15) | C-multiblock-09 | Applied, pending accepted 0.9 | `23013a54b90594ba9f6acb6a951cafeee76abc09` |
| B5 / typed frame records | §9.1, §9.4, §12.3 (K16) | F-frame-records-09 | Applied, pending accepted 0.9 | `a300222603d9ca1c0ec303a3122ad896792f2db0` |
| A5 / draw ordering | §4.1 (K17) | A-measure-draw-order-09 | Applied, pending accepted 0.9 | `ed044ecb6017ecd41fb98b4f8d3271eac7c40945` |
| A4 / Q14; A5 / EPS-DECADE, BLOCK-IMAGE, ISA-7, Q1–Q13 | §0 (K9/K10/K5/K18), Q14 confirmation | F-ratified-confirmations-09; retained §16.3 examples and boundary/sector witnesses | Applied, pending accepted 0.9 | `78dd9df95ffd29abfdaa97e3c9a62185cef3811f` |
| §0 / §17 audit | §0 change list, §17 defaults; all edited clauses | All retained and added draft cases | Applied, pending accepted 0.9 | commit containing this row |

Step 1: explicit signature, complete args, escaped flat class keys, exact
reduced rationals and 34-significant-digit upward enclosure are normative.
Existing Fraction/Decimal witness checks independently reproduce every row.
Rejected alternatives (retained historically above): separate bound-request
entry, class-aware accessor, selectable precision/rounding. No alternative
remains in §10.1. No new numerical example was needed.

Step 2: expected is mandatory, standalone invocations are per claim,
scheduled roots use bindings.invocation, and complete positional tuple
arrays retain every input/target/fault/borrowed/cell component. Large
domains use the program relation. K4 quantified and universally checked
structural claims retain their scope. Existing independent checks cover
XOR outcomes, coverage, wide args, signed zero and canonical args hashes.
Rejected: omitted expected defaulting to oracle; shared invocation registry
or region-level inheritance; named or sample-only keyed tables. The
region-inheritance parenthesis was removed to match ratification literally.

Step 3: schema, envelope hash, ordinals, scratch identity, empty removable
sets and the complete deterministic decomposition families are decided.
The catalog is a separate b-isa-spec-8r4 job; no ref/ publication occurs
before acceptance. Existing independent Python checks enumerate every qxor
pair and reversal and recompute the envelope hash. New pending witness
adds one unavailable case. Rejected alternatives: a different hash rule,
optimized/CSE recipes or a different initial decomposition set; later
libraries require their own version. SPEC-QUESTIONS 21's library-related
realisation gate remains a delivery dependency, not an undecided contract.
Gate note: raw unified diffs contain space-only context lines by design;
git diff --check covers source/progress/conformance, and the diff artifact
is verified by regeneration rather than stripping its context bytes.

Step 4: optional vertices/edges with addressable classes, pairwise native
adjacency and concrete schedule placement. The memo does not enumerate
placement fields or multi-operand connectivity: §11 supplies explicit
interface/allocation vertex arrays plus deterministic defaults, and §8.3
uses pairwise adjacency for native gates with more than two operands.
These details prevent conformant consumers choosing different placements;
scheme leaves validate separately. Explicit swap sequences keep routed
computation reachable while automatic routing/cost rules wait for 0.10.
Rejected: omitting topology entirely, or deferring its presence/meaning.
Python -I JCS/hash and an independent Rust grid/byte/hash test check the
new witness. Canonical bytes have no trailing LF (b-isa-spec-1pl).

Step 5: the ratified sentence is applied. Read reference README and all
SPEC-QUESTIONS (no separate multi-block entry); action.rs flattens blocks
in text order with one shared environment. The built binary checks every
t,p pair and its adjoint against the independent expression, including
the scratch lifetime across blocks. No disagreement; no bug bead needed.
Rejected: interpreting action labels as executable CFG branch/join nodes.
The fixture's 0.8 interface hash is computed from its complete envelope
(body included), independently of the CLI; no 0.9 example hash is added.
The separate staged case is unavailable pending 0.9.

Step 6: published typed records with explicit slot/frame identities,
class/state/width rules, c-only expressions and disjoint shared lifetimes.
Independent Python and Rust checks reconstruct canonical bytes, SHA-256,
width arithmetic and half-open interval disjointness; no 0.9 executor
claim. The memo names record categories but not field spellings: §9.4
defines those plus mandatory empty arrays and identity/order rules.
Rejected: the previous interface/class-map/scheme_ancillae/retained_history
encoding, and per-class expression maps with role annotations.
SPEC-QUESTIONS 11's frame-encoding question is closed for 0.9; its 0.8
reading remains unchanged in the interpreter-owned file.

Step 7: FIFO dynamic measurement consumption, wire-first lexicographic
outcomes and strict cumulative threshold match README, --draws handling,
classical.rs VecDeque and registers.rs. The two-measurement 0.8 CLI
fixture returns bits 01 then 11 at the exact CDF ties; Python Fraction
and independent Rust integer arithmetic verify both ordering distinctions.
The fixture hashes use complete independent 0.8 envelopes; 0.9 example
hashes remain placeholders. SPEC-QUESTIONS 29 is closed for 0.9.
Rejected: reverse draw consumption and integer-order CDF enumeration.

Step 8: all confirmations marked decided. Existing operative sentences
already match ratification and stay unchanged; no new numerical values
are introduced. Q12 continues to gate draft example hashes on the 0.9
precheck. Rejected Q14 reading: a captured/readable argument environment
instead of explicit token/classical/mapped-region forwarding. Historical
Q1–Q13 choices remain applied; this pass does not reopen them. The new
staged case names the confirmation beads; independent existing witness
checks remain green.

Step 9: consolidated the K9–K18 rows and audited every ratified ISA edit
and its deferral. §17 item 7 fixes the default library and publication
dependency; item 15 fixes the routing default and preserves explicit
swap sequences. All maintainer-decision markers and rejected readings
are absent from normative text. The pre-existing §5.5 implementation
choice to retain an already identified matched frame is semantically
equivalent storage bookkeeping, not an unratified alternative reading.

Ratification scope dispositions: B2 (versioned symbolic histories), B3
(pending import obligations at linking), B4 (linked-object replay registry)
are the memo's circuits M2 proof-contract jobs, not additional ISA text
edits in this brief. Their ratification is preserved here for the circuits
implementer; no competing ISA encoding or resolver is introduced by this
text pass. B6 is satisfied by A1's decided identity contract; catalog
delivery still waits on b-isa-spec-8r4. C is a process/release decision
for the orchestrator (council round, seats, plugin/driver starts), not an
ISA semantic clause and not executed by this implementation sub-agent.

SPEC-QUESTIONS closures: 21's comparison/tuple/budget ambiguities are
closed by K13 (the old flat tuple reading is superseded only for 0.9);
11's frame format is superseded by K16; 29 closes through K17. This pass
adds no multi-block question entry, and does not edit SPEC-QUESTIONS.md.

Wording elaborations: removed K13 region-invocation inheritance to honor
per-claim binding; supplied concrete field names and identity/order rules
for the topology placements and typed frame schema; made native
multi-wire adjacency pairwise so higher-arity gates have a determinate
rule. These fill schema details the ratification leaves implicit. B1
was applied as the requested single sentence. No reference-interpreter
disagreement was found for the two behaviors checked (blocks and draws);
0.9 schema/replay/estimate implementations are not claimed.

Final observed full harness: **445 pass / 0 fail / 54 unavailable
(499 cases), exit 2**; baseline **445 / 0 / 48 (493 cases)**.
Six added cases are all unavailable pending 0.9 and name their beads.
All 28 Rust tests pass headlessly/offline; the three added Rust tests
independently check grid canonical bytes/hash/adjacency, typed-frame
bytes/hash/widths/lifetimes, and FIFO/lexicographic CDF ties. Python runs
with -I and imports no interpreter or VM implementation. Raw diff bytes
are regenerated immediately before every commit; accepted 0.8 SHA-256
remains 90e61d9c377c939fe9652758f61cd5ead068ef06e4e40d812d3f3c5197ab605e.

K19 structured witness clarification: finite nested actual syntax may invoke
the same higher-order recipe (qloop(3,qloop(2,B)) is six B occurrences).
Rejecting any repeated recipe name on the runtime expansion stack conflates
finite source nesting with recursive declared dependencies. Captured actual
expansion starts its own dependency audit; direct and mutual cycles still
reject. Structured full-domain/fixpoint tests reproduced this error before
the expander fix. No qxor witness bytes changed.

K19 validation also enforces §3.3 controls versus diagonal/swap targets,
closed formal keys, declared dependency cycles through literal actual
syntax, and scratch LIFO/balance. The six remaining source-binding/order
gaps are afi, 1a4, 3xe, lph, 1oa and 82x; details and affected rows are
recorded in ref progress and bd. No partial-library hash is inserted at
the complete-catalog marker. The arbitrary-image and qinplace-order fixes
would exceed the explicitly scoped constructor additions, so are raised
for a separate contract decision rather than guessed.


REF completion resumed 2026-10-31: K21 binds unconditional image bytes
(afi); K22 adds indexed typed body templates with explicit frame actuals
(lph); K23 documents the integer bit extractor already used by literal
recipes. Both new language tests were observed red on unknown constructors
before implementation. Rejected: controlling image X, opaque image names,
rebinding body captures by spelling, treating template application as a
callee ordinal space, and leaving bit extraction implementation-private.
The qxor witness bytes and hash remain unchanged.

The call-flag regression was reproduced: all 192 semantic configurations
passed, then the tuple-count assertion failed (43,200 actual vs 41,760
printed). Its loop/domain and semantic assertions are retained; accounting
is corrected to 192 configurations / 43,200 tuples, plus the exact §16.3
5/10-bit counter case (131,072 tuples). This is not a relaxation of the
call predicate. Baseline harness is 445/0/65, not the older 445/0/60.

Carried contract gaps: 1a4 (arbitrary heterogeneous interface argument-list
forwarding, including token/classical types), 3xe (class and output/lifetime
wire binders), 1oa (ordered mapped-region descriptors), and 82x (ratified
reverse-allocation order versus the printed qinplace sequence). Their exact
blocking sentences remain in §11.1 and the beads; no partial library is
published. In particular changing qinplace's release order or adding a
ratified-A1 exception needs a contract decision, not an expander default.

K24 adds captured closure-bound argument vectors and exact classical/token
values, including >64-bit integers and NaN payloads. Its forwarding test
failed on the missing args-name constructor before implementation. Rejected:
reinterpreting captured actual names in the forwarder's scope, word-sized
classical integers, token ids, implicit value widening, and sharing caller
ordinals with symbol calls. 1a4 is carried until source region shape/role
metadata is encoded (the vector mechanism itself is now implemented); it
shares that remaining descriptor gap with 1oa. No flattened wire shape is
misrepresented as a complete region interface.

K21 default-image clarification: absent image is the empty string and emits
no X even on non-byte-aligned regions (one to four total wires included in
the witnesses); nonempty images retain exact byte/wire length checks. K22
lexical audit reproduced and fixed legacy integer-template wire import and
cross-type shadow leakage; formal names now shadow across all captured name
maps. Remaining activation metadata is b-isa-spec-evi; afi and lph closed,
1a4/3xe/1oa/82x carried with exact changes in bd. The completed step and
qregion recipes bring the checkpoint to 195; no complete-library hash/count
is asserted and the normative marker remains untouched.

## 2026-10-31 REF completion II — K25–K27

K25 shares ordered typed record binding between mapped byte layouts and
activation locations/captures. K26 retains source region shape, role and
origin through K24 closure vectors. K27 passes exact allocation classes and
shared declarations through recipe calls, exposing output wires in the
caller after acquisition, with explicit lifetimes and adjoint metadata.
Witnesses: conformance/tests/ref_descriptors.rs; observed red for unknown
formals/constructors before implementation. K23 already resolves 4nx; its
LSB literal witness remains unchanged.

Rejected: opaque caller memory/activation body dispatchers (outsource the
catalog algorithm); flattening gaps or region shapes (loses source binding);
using any for every class (changes resource identity); copying allocation
status at invoke (breaks returned output lifetime); host ids for tokens
(K24 already preserves value tuples). No 0.8 semantics are changed.

82x is carried: §4.5 explicitly generates `qfree t; qfree f` after
allocating t then f; §11.1 and ratified A1 require all library scratch
released in reverse allocation order. Changing §4.5 would change accepted
0.8 generated order; adding an instruction-private exception here would
change the ratified A1 rule. Neither is a constructor-language extension.
Stop on qinplace; require an explicit semantic/ratification decision.
The two calls and both private bundles remain required and in scope.

K25 checker audit in the allocation family: record wire actuals evaluate
in the captured caller environment, not in an environment overwritten by
earlier wire fields. Field width expressions instead use the receiving
recipe's earlier integers plus earlier integer fields. A regression
produced coincident operands before the fix; the two scopes are now
separate. Normative text already required these scopes.

K25 field schemas also admit the existing K21 image type, with a red/green
initializer-record witness. Keeping image metadata in the shared record
vocabulary avoids a separate ad hoc initializer-list binding. Image X
semantics stay K21; no new unconditional-gate permission is introduced.

K27 follow-up audit: declaration handles cannot bypass a declared library
scratch lifetime's LIFO/clean requirement by passing through allocation
formals. A non-LIFO scratch handle regression failed before classification
was retained on the shared identity; caller-owned output lifetimes still
permit overlapping release order. This specifically preserves 82x rather
than silently treating qinplace's private scratch as caller results.
K26 origin suffix is now the exact source NAME token; occurrence identity
is the origin binding plus the already retained cell wire identities,
which disambiguate repeated invocations without an unspecified string form.

K25 construction uses the same record vocabulary: width/initial/image and
shared storage handle; a separate indexed frame list aliases exactly the
state list's B frame handles. Source formation fixes the printed §5.2
group order and the reference §3.7 widths/initial values, with byte images
remaining K21. Rejected: an opaque caller construction body, image-only
initialization of non-byte state, bytewise name sorting across declaration
order, and flattening all heterogeneous frames into caller-private circuits.
The catalog invokes its own step algorithm; only source row/successor
templates are supplied. Record acquire retains the recipe scratch mark
through K25 scope binding, so private state cannot bypass K27 LIFO.

## 2026-10-31 REF completion — K28 instruction release ruling

Maintainer ruling on b-isa-spec-82x is applied solely to §0/§11.1 as
K28 REF-INSTRUCTION-RELEASE. The reverse-allocation rule governs recipe
scratch; an instruction-defined sequence is reproduced exactly, including
qinplace's qfree t; qfree f. The one-bit identity-pair witness records
instruction ordinals 0/1/2/3/4 and separate callee ordinal zero for both
calls. conformance/tests/ref_qinplace_contract.rs was observed red before
the normative addition, then checks the exact leaf sequence and identities.
Existing scratch-LIFO/capture regressions stay binding.

Rejected alternative: changing §4.5 to qfree f; qfree t would alter accepted
0.8 generated order. Neither accepted 0.8 nor draft §4.5 is changed. Also
rejected: relaxing release order for ordinary recipe scratch or removing
either private allocation/call. K27 declarations encode the instruction's
own lifetimes under K28, not a general scratch exception. The printed qxor
witness bytes/hash are unchanged. Catalog completion and full-library
binding follow as a separate family commit; publication requires accepted
0.9.

Rule 12 addendum: K28 and every new witness sentence carry declared
dependencies. Lookups in ISA-0.8.json and ISA-0.9-draft.json identify
qinplace as ISA-4.5-P5 and the original scratch/ordinal clause as
ISA-11.1-P21. The new rule is a separate paragraph after that clause;
unchanged sentences are not retrofitted.

Ruling gate: 109 Rust tests / 0 fail (entry 108/0); fmt --check and
clippy --offline --all-targets -D warnings green; full harness unchanged
445 pass / 0 fail / 73 unavailable (518). After the dependency-marker
addendum, draft_contracts and the exact four-tuple identity-pair witness were
rerun green, as was clippy. Accepted 0.8 fingerprint and qxor unchanged.

Completion self-review corrects the small K28 witness from n=F=1 to
n=1/F=4 under §5.4 (dependency added). The fault-width assertion was red
before fixture correction and green after; instruction/callee ordinals,
release order and four-tuple domain are unchanged. The catalog's 80 shapes
and example 7 already used F=4. No accepted text or catalog hash changed.

## 2026-10-31 REF complete draft-library binding

All 31 README dispositions are bound after qinplace completion under K28.
The single §11.1 marker now records 219 recipes and complete envelope
fcb2f1e6d61aced0bf9689eab5f6d82c4ae42e9fea8d1b21ae9c7ffccda6f5ce,
computed independently in Rust and Python -I (including original qxor check).
The new binding/publication sentences carry declared dependencies too;
only K11's non-normative bead-status annotation is updated outside that
marker in this family. No other normative K11 wording is changed.
K28 correction and release rule retain accepted §4.5 bytes and ordinals.
Final gate 111 Rust/0 fail (entry108, ruling109), fmt/clippy green,
ref_call_flag green; harness445/0/74 from445/0/73, one pending-0.9 case.
82x and parent8r4 closed; all children closed; publication still requires
accepted 0.9. Full evidence and family domains are in ref-0.9-draft.PROGRESS.md.


# Background (not graded): `2026-11-01-isa-09-pass-v-73y.md`

# ISA 0.9 editorial pass V — 73y borrow-frame entry domain

Maintainer ruling: 2026-11-01, Reading B, with a normative entry analysis.
Implementation only; the orchestrator runs the one-reviewer council fix
round. No muse round, push, 0.8 source edit, VM edit or other sibling edit.

## Argument and evidence

```
<1>1. The former sentence admits two domains with different admission results.
      PROOF:
  <2>1. “P_F = P' ⊗ I_B ... frame's full domain” admits the independent
        touched-wire cube (A); §5.2's D fixes qalloc wires at zero, T3
        concludes V|span(D)=P, and §5.6 also says “over D”, admitting B.
        BY ISA-5.6-P2.S2 (accepted 0.8), ISA-5.2, ISA-14.3-P3
  <2>2. With c=0 at frame entry, CX c b is identity for every b and R;
        on the independent c,b cube it flips b when c=1.
        BY gate semantics ISA-4.4; algebra
  <2>3. The accepted reference snapshot ad84e75 implements B: initial free
        variables (borrow.rs 1958), region-prefix pass (1974), qalloc zero
        (1142), false-control skip (1523–1530), quantum forgetting (1533)
        and causal exact inverse restoration (1397–1440). Return equations
        and independence checks are 1110–1137 and 1639–1675.
        WITNESS: read-only accepted review checkout/binary; supplied
        investigation, reproduced by checking all four r9 objects.
  <2>4. Council intent agrees with B: response-round-11.md 183–184 says
        “CX(0,b) identity on arbitrary bR”. INV-6's coverage accounting
        chooses no prefix analysis. INV-3:1.5.5 had instead silently
        composed frames as full operators.
        WITNESS: ../bennett-isa-spec-review/reference-interpreter/council/
        response-round-11.md; ../bennett-conformance/proofs/
        INV-3-discipline-soundness.md before this repair.
  <2>5. QED
        BY <2>1, <2>2, <2>3, <2>4
<1>2. Constant propagation plus causal adjoint cancellation suffices for
      every accepted fixture and every neutral-suite case; polynomial
      entry tracking is unnecessary for this corpus.
      PROOF:
  <2>1. qalloc establishes c=0 in the loop fixture. H; matched oracle pair;
        H, or H; matched qinplace pair; H, restores c=0 in the other
        three fixtures. qalloc alone cannot establish those latter facts.
        BY ISA-5.6-P9–P12 (0.9 pass V); fixture instruction sequences
  <2>2. EntryAnalysis has values {0,1,unknown}, all-operand causal stacks,
        known-false disabling, constant primitive gates, opaque forgetting,
        exact matching keys and explicit lifetime barriers. It has no ANF
        expressions. Bounded visits/cycles use the same transfer. This is
        the least sufficient analysis family tested here: add allocation,
        constant transfer and causal inverse restoration, without importing
        polynomial or general quantum identities from the prefix.
        WITNESS: reference-interpreter/src/borrow.rs 1360–1546;
        EntryAnalysis::apply; Facts::begin_frame (1561 onward).
  <2>3. A before/after CLI audit checks all 48 .bisa fixture/neutral objects:
        48 accepted before, 48 after, zero losses. The neutral runner
        additionally checks all hashes and runs in its 16 cases.
        WITNESS: .tmp/pass-v-fixture-baseline.json;
        .tmp/pass-v-neutral.log; frame_domain.rs four-council-fixture test.
  <2>4. The interleaved prefix CX a c; CX x c; CX a c; CX x c clears c by
        Boolean algebra but not these causal pops. The old checker accepts
        it (red test); the aligned checker rejects its CX c b frame with
        §5.6. A reversed cleanup after return makes the test satisfy §6.2,
        so an unrelated cleanup error cannot masquerade as this rejection.
        WITNESS: .tmp/pass-v-red.log; frame_domain.rs polynomial-prefix test.
  <2>5. QED
        BY <2>1, <2>2, <2>3, <2>4
<1>3. Restricted frame equality suffices on reachable entangled states.
      PROOF:
  <2>1. The checker establishes reachable entry support in span(D_F),
        retaining only admitted local constants and freeing all interface,
        borrowed and other local components independently.
        BY ISA-5.6-P13.S1, ISA-5.6-P13.S5 (0.9)
  <2>2. T3 gives P_F|span(D_F)=(P'⊗I_B)|span(D_F). Expand an entering state
        as Σ_d |d⟩|r_d⟩, d∈D_F, and apply the equality termwise. The same
        equality tensored with I_R holds without any promise about R.
        BY ISA-5.6-P2.S3, ISA-5.6-P13.S6, ISA-14.3-P3; linearity
  <2>3. Induct along the actual prefix: every next frame again has support
        in its own span(D_F), and intervening operations do not touch B.
        BY <2>1, <2>2; INV-3:1.5.1, repaired INV-3:1.5.5.1–1.5.5.3
  <2>4. QED
        BY <2>3
<1>4. QED
      BY <1>1, <1>2, <1>3
```

## Dispositions

| Item | Disposition |
|---|---|
| 1 / normative text | §5.6 defines D_F and restricted T3 equality; constant/causal-adjoint entry rules are normative. New checker MUST is K76 in the §0 inventory; K1–K75 stay intact. Exact-label diff regenerated; witness green. |
| 2 / accepted 0.8 | New short erratum incorporates the binding 0.9 reading and names all four affected fixtures. The 0.8 file retains SHA-256 90e61d9c377c939fe9652758f61cd5ead068ef06e4e40d812d3f3c5197ab605e. |
| 3 / reference | Separate EntryAnalysis fixes the domain; exact ANF reasoning remains inside frames. Header and SQ20 updated. Definite domain failures also guard public certificate verification; unrelated opaque events cannot turn definite Boolean failures into a certificate escape. |
| 4 / INV-3 | Only the authorized proof file changes in bennett-conformance. Step 1.5.5 now establishes entry support, applies linearity including R and composes along the reachable prefix. Full-operator wording is qualified accordingly. |
| 5 / process | Pass V recorded in isa-0.9.PROGRESS.md; bead 73y stays in_progress for the orchestrator's one-reviewer fix round, with no muse round. Handoff uses the actual UTC date. |

Additional negative coverage: interface/local prefix correlations do not
restrict the interface cube. A whole-region identity claim can verify as
a region claim while its normative frame-domain obligation rejects; public
certificate verification checks the latter independently of parse admission.
The library replay guard also rejects a region-D proof if formation of D_F
forgot a touched component's prefix constraint: that replay did not cover
the expanded frame domain. No producer-supplied field can narrow D_F, and
this pass adds no new serialized claim kind. A function-specific library
proof still has to cover the actual frame domain; a whole-region identity
is insufficient evidence for that obligation.

During the session unrelated Beads-only commit bbb758d recorded a VM
oracle invocation-token question; it is retained and is not a pass V
implementation commit. No worklog is written by this implementation
sub-agent; the orchestrator owns the session worklog.

No accepted fixture changes or removals. No object version gate change:
the reference still admits 0.8 objects under the binding erratum, and does
not claim 0.9 object admission. No gate set, source algorithm, interface,
width or target capability is removed; the entry-proof boundary is now
fixed by the published contract rather than a checker-specific optimizer.

## Validation and commits

Final gates: reference 466 passed / 0 failed / 5 unchanged ignores;
conformance 113 passed / 0 failed / 0 ignored; neutral 16/16; CLI admission
48/48; witness and catalog --check PASS. All ran headless with project-local
TMPDIR. Item commits: 9df1541 (spec/diff), 6182d7c (erratum), 1a19072
(reference/SQ20/tests), 2095a7d (sibling proof only). These totals and IDs
are also recorded in the pass V block at the top of `spec/isa-0.9.PROGRESS.md` and in `HANDOFF.md`.
Headless logs: `.tmp/pass-v-reference-verified.log`,
`.tmp/pass-v-conformance.log`, `.tmp/pass-v-witness.log`,
`.tmp/pass-v-neutral.log`, `.tmp/pass-v-boundaries2.log`.
The first boundary-test draft exposed a §6.2 cleanup failure; adding its
explicit reversed cleanup isolated the intended §5.6 negative. The public
API reconstruction test initially omitted function-header lines, giving a
hash lookup error; restoring the complete source lines isolated its domain
obligation. Both final regression tests exercise the intended check.

## Exact amended §5.6 text

The modified rule paragraph and the complete new normative analysis follow
verbatim; the translation-lemma bullets and existing surrounding text stay
unchanged.

**Rule (suite F).** Borrowed wires (set B) are touched (as control or
target) only inside **borrow frames**: maximal contiguous permutation-
only subcircuits from the first to the last instruction touching B. The
frame's domain D_F contains every value of every borrowed and interface
wire, independently, and the values of its other wires admitted by the
entry-state analysis below, starting from the region's D (§5.2). The
frame's realised permutation P_F MUST satisfy
`P_F|span(D_F) = (P' ⊗ I_B)|span(D_F)` for some P' independent of B,
established by a T3 claim over all of D_F (exhaustive, or a library
certificate, §12 `borrow_frames`) or
**structurally by the translation lemma**: the frame is `V; W; V⁻¹; W`
where


**Entry-state analysis (K76, normative).** This analysis fixes D_F; a
stronger analysis cannot narrow it. Resolve classical arguments, tokens,
controls, operand identities, allocations and the acyclic local call
expansions from the object (§3.5, §4, §5.1, §5.3), for each permitted
invocation. A wire's abstract value is 0, 1 or unknown (both values).
Interface and freshly borrowed wires start unknown; `qalloc` starts 0;
image preparation uses the corresponding X gates on allocated wires.
The transfer rules are:

1. An effective control known false disables the operation. Otherwise,
   an X-family flip or controlled swap evaluates its targets only when
   all its operands are known; any other target becomes unknown.
   Read-only controls keep their values. Diagonal gates keep basis
   values; other quantum gates make their targets unknown. An opaque
   oracle or `qinplace` makes its outputs unknown; an unresolved action
   makes its modified wires unknown. Local action bodies use these same
   rules, with inherited controls.
2. Each enabled reversible operation records its exact identity and the
   preceding abstract values on **every** operand's causal stack,
   including readers. Its exact §5.3 adjoint restores those values only
   when that same event is the top event on every operand stack; pop
   that event everywhere. Identity includes operands, effective controls,
   callees, classical arguments and token identities/tuples. Disjoint
   events may interleave; nested pairs may cancel. A lifetime boundary
   or unresolved action invalidates the entire connected stack history
   reached through its operands. Allocation and release add/remove the
   corresponding abstract components.
3. Structured bodies follow §4.6, including unconditional lifetimes and
   predicated gates; bounded loops apply the transfer at each visit.
   Equal complete abstract states permit exact cycle skipping. A proved
   inductive over-approximation may represent remaining visits, but may
   not establish a constant that these transfers do not establish.
   This is a decidable finite rule set; Boolean polynomial simplification
   and quantum identities beyond these exact adjoint pops supply no
   entry facts.

At a frame entry, retain only the known constants of its allocated local
wires; every other local component independently takes both values, and
every interface and borrowed component independently takes both values
even if the prefix related or fixed them. D_F is this Cartesian product;
for repeated visits it is the union of these products. Thus `CX c b`
is identity on arbitrary b and its external reference when this analysis
establishes c = 0, whereas an interleaved CNOT prefix that clears c only
by polynomial algebra supplies no such entry fact. Exact Boolean
reasoning remains available to prove the permutation **within** a frame.
The checker MUST use this D_F for both exhaustive and library frame
claims and establish that the reachable entry states lie in span(D_F).
By linearity the restricted equality then applies to every reachable
entry state, including superpositions entangled with an external system.



# Background (not graded): `INDEX.md`

# Proof index

Spec: ISA 0.8 (`clauses/ISA-0.8.json`). Format: [`FORMAT.md`](FORMAT.md). Leaf counts are
BY / ASSUMED / OPEN inside the proof block (QED steps counted as BY).

| Theorem | Statement | Status | Leaves BY/ASSUMED/OPEN | Gaps |
|---|---|---|---|---|
| [INV-1](INV-1-matched-pairs.md) | Matched compute/uncompute pairs are the identity | proved to depth 3 except qif row | 42 / 3 / 1 (refuted) | 4 |
| [INV-2](INV-2-no-clone.md) | No clone, no alias (names, handles, states) | proved to depth 2 under readings | 22 / 4 / 0 | 4 |
| [INV-3](INV-3-discipline-soundness.md) | Soundness of the static uncomputation discipline (T5 + borrow frames) | perm and borrow proved to depth 3 under readings; `other` refuted | 30 / 7 / 2 (1 refuted) | 9 |
| [INV-4](INV-4-envelope-injective.md) | Identity envelope injective on structural layout leaves | holds except `interface_regions`; refuted for CC/R | 19 / 1 / 3 (2 refuted) + 1 outside proof | 5 |
| [INV-5](INV-5-schedule-selection.md) | Schedule selection soundness, admission exactness, §17 defaults as written values | (A), (B) proved to depth 3 for bound admission under readings; (B) refuted for unbound admission; (C) refuted for `epsilon_share` and uncovered defaults | 37 / 9 / 8 (4 refuted) | 17 |
| [INV-6](INV-6-certificate-soundness.md) | Certificate label soundness, evidence semantics, resource honesty (§12.1–12.2) | (A) proved to depth 3 under readings (name-set classifier refuted); (B) proved for exhaustive claims, sampled fraction undefined, "no conclusion outside" refuted for co-singleton bijections; (C) only as a reading: 0.8 has no host-limit outcome | 41 / 12 / 2 (1 refuted) | 12 |

## Statements cited

- **INV-1** (52, of which 1 whole): ISA-2-P9.S1, ISA-3.1-P2.S3, ISA-3.2-P8.S1, ISA-3.3-P2.S1, ISA-3.3-P2.S2, ISA-3.3-P3.S1, ISA-3.3-P3.S2, ISA-3.5-P1.S1, ISA-3.5-P1.S2, ISA-3.5-P1.S3, ISA-4.3-P1.S1, ISA-4.3-P2.S1, ISA-4.3-P3.S1, ISA-4.3-P4.S1, ISA-4.4-P1.S1, ISA-4.4-P2.S2, ISA-4.5-P1.S1, ISA-4.5-P2.S1, ISA-4.5-P3.S1, ISA-4.5-P4.S1, ISA-4.5-P5.S1, ISA-4.5-P5.S2, ISA-4.6-P1.S1, ISA-4.6-P2.S1, ISA-4.6-P3.S1, ISA-4.6-P4.S1, ISA-4.6-P5.S1, ISA-4.6-P6.S1, ISA-4.6-P7.S1, ISA-4.6-P8.S1, ISA-4.6-P9.S1, ISA-4.7-P1.S1, ISA-5.1-P1 (whole clause), ISA-5.1-P1.S7, ISA-5.2-P2.S1, ISA-5.2-P2.S2, ISA-5.2-P2.S3, ISA-5.2-P4.S1, ISA-5.3-P1.S1, ISA-5.3-P2.S1, ISA-5.3-P4.S1, ISA-5.3-P4.S2, ISA-5.3-P5.S1, ISA-5.4-P1.S4, ISA-5.5-P1.S1, ISA-5.5-P1.S3, ISA-5.6-P1.S1, ISA-5.6-P2.S1, ISA-5.6-P2.S2, ISA-6.2-P1.S2, ISA-14.2-P1.S1, ISA-14.2-P1.S2
- **INV-2** (37): ISA-2-P2.S1, ISA-2-P9.S1, ISA-3.1-P2.S3, ISA-3.2-P1.S1, ISA-3.3-P1.S1, ISA-3.3-P2.S1, ISA-3.3-P2.S3, ISA-3.3-P3.S1, ISA-3.3-P3.S2, ISA-3.3-P6.S2, ISA-3.3-P7.S1, ISA-3.3-P8.S1, ISA-3.3-P9.S1, ISA-3.3-P10.S1, ISA-3.3-P11.S1, ISA-3.3-P12.S1, ISA-3.3-P13.S1, ISA-3.3-P13.S2, ISA-3.3-P14.S2, ISA-3.5-P1.S1, ISA-3.7-P2.S1, ISA-4.3-P1.S1, ISA-4.3-P2.S1, ISA-4.4-P1.S1, ISA-4.5-P1.S1, ISA-4.6-P1.S1, ISA-4.7-P1.S2, ISA-5.1-P1.S1, ISA-5.1-P1.S3, ISA-5.1-P1.S5, ISA-5.1-P1.S6, ISA-5.2-P2.S3, ISA-5.3-P1.S1, ISA-6.1-P3.S1, ISA-6.2-P1.S3, ISA-10-P3.S2, ISA-14.2-P1.S2
- **INV-3** (42, of which 3 whole): ISA-2-P9.S1, ISA-3.3-P3.S1, ISA-3.5-P1.S1, ISA-3.5-P1.S3, ISA-4.3-P3.S1, ISA-4.4-P1.S1, ISA-4.5-P3.S1, ISA-4.6-P1.S1, ISA-5.1-P1 (whole clause), ISA-5.1-P1.S5, ISA-5.2-P2.S1, ISA-5.3-P1.S1, ISA-5.3-P5.S1, ISA-5.6-P1.S1, ISA-5.6-P2.S1, ISA-5.6-P2.S2, ISA-5.6-P3.S1, ISA-5.6-P4.S1, ISA-5.6-P5.S1, ISA-5.6-P6.S1, ISA-5.6-P7.S1, ISA-6.1 (whole section), ISA-6.1-P1.S1, ISA-6.1-P1.S2, ISA-6.1-P1.S3, ISA-6.1-P2.S1, ISA-6.1-P3.S1, ISA-6.1-P9.S1, ISA-6.1-P10.S1, ISA-6.1-P11.S1, ISA-6.1-P14.S1, ISA-6.2-P1 (whole clause), ISA-6.2-P1.S1, ISA-6.2-P1.S2, ISA-6.2-P1.S4, ISA-6.3-P1.S1, ISA-6.4-P1.S1, ISA-6.4-P1.S2, ISA-6.4-P1.S4, ISA-14.2-P1.S1, ISA-14.3-P3.S1, ISA-14.3-P5.S1
- **INV-4** (14): ISA-9.1-P1.S1, ISA-9.1-P1.S3, ISA-9.1-P2.S1, ISA-9.2-P1.S3, ISA-9.2-P2.S1, ISA-9.2-P2.S2, ISA-9.2-P2.S3, ISA-9.2-P2.S4, ISA-9.2-P2.S5, ISA-9.2-P2.S6, ISA-9.2-P2.S7, ISA-16.1-P1.S2, ISA-16.1-P1.S3, ISA-16.2-P1.S1
- **INV-5** (42): ISA-3.2-P10.S1, ISA-3.6-P1.S1, ISA-3.6-P4.S1, ISA-3.6-P6.S1, ISA-3.6-P11.S1, ISA-3.7-P20.S2, ISA-4.2-P1.S2, ISA-4.2-P21.S1, ISA-4.6-P8.S1, ISA-4.6-P9.S1, ISA-4.7-P1.S1, ISA-5.1-P1.S7, ISA-5.2-P1.S1, ISA-5.2-P2.S2, ISA-5.2-P3.S1.2, ISA-5.2-P3.S1.4, ISA-5.4-P1.S3, ISA-8.1-P1.S1, ISA-8.1-P10.S1, ISA-8.1-P10.S2, ISA-9.2-P2.S13, ISA-10-P1.S4, ISA-10-P4.S1, ISA-10-P7.S2, ISA-11-P2.S1, ISA-11-P2.S2, ISA-11-P2.S3, ISA-11-P3.S2, ISA-11-P4.S1, ISA-11-P4.S2, ISA-11-P4.S3, ISA-11-P4.S4, ISA-11-P4.S5, ISA-11-P4.S6, ISA-11-P4.S9, ISA-12.1-P2.S1, ISA-17-P7.S2, ISA-17-P8.S2, ISA-17-P10.S1, ISA-17-P10.S2, ISA-17-P11.S1, ISA-17-P14.S2
- **INV-6** (35): ISA-1.2-P4.S1, ISA-2-P1.S2, ISA-2-P7.S1, ISA-3.3-P1.S1, ISA-3.3-P3.S2, ISA-3.3-P14.S1, ISA-4.3-P2.S1, ISA-4.4-P1.S1, ISA-4.4-P2.S1, ISA-5.1-P1.S1, ISA-5.1-P1.S2, ISA-5.2-P1.S1, ISA-5.2-P2.S1, ISA-5.2-P2.S2, ISA-5.2-P2.S3, ISA-5.2-P4.S1, ISA-5.3-P1.S1, ISA-5.3-P1.S4, ISA-5.6-P1.S1, ISA-5.6-P2.S2, ISA-9.2-P1.S1, ISA-9.2-P2.S15, ISA-9.4-P2.S1, ISA-9.4-P3.S1, ISA-12.1-P1.S1, ISA-12.1-P2.S1, ISA-12.1-P5.S1, ISA-12.1-P7.S5, ISA-12.1-P8.S1, ISA-12.2-P1.S1, ISA-12.2-P1.S2, ISA-12.3-P2.S3, ISA-14.1-P1.S1, ISA-14.2-P1.S2, ISA-14.3-P3.S1

Steps cite statement ids (`ISA-5.3-P4.S2`); a clause or section id appears only where a step
needs the whole clause or section, marked `(whole clause)` / `(whole section)`. Statement ids
count as strong coverage at statement level; whole-clause ids as weak. The machine-readable form
is [`tags.json`](tags.json) (`{"INV-n": [ids]}`, generated from every id the proof cites outside
its Witnesses table). Classifier problems met while retagging (statements kept `uncertain` or
misclassified): [`STATEMENT-NOTES.md`](STATEMENT-NOTES.md).

## Coverage

```
env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER TMPDIR=$PWD/.tmp \
    python3 -I clauses/clausegraph.py coverage clauses/ISA-0.8.json --tags proofs/tags.json --statements
```

Result (2026-10-31, after INV-6, proofs only, statement level): `statements of ISA-0.8: 541; strong 169, weak (clause or section tag) 10, uncovered 362`
(clause level, same run: `314 clauses; strong 112, weak (section tag only) 9, uncovered 193`).

## Refuted steps (spec text false as written)

- INV-1 1.3.6.4: the `qif` row of the Adjoint table (`ISA-5.3-P4.S2`) is ill-formed for cross-arm lifetimes.
- INV-3 1.4.2: `other` values released by their adjoint while a reader is outstanding are not clean (`ISA-6.2-P1.S4`).
- INV-4 1.5.2: (5b) has no tie order for coincident dotted paths, so CC/R envelopes are not unique (`ISA-9.2-P1.S3`).
- INV-4 1.5.3: coincident dotted paths make the CC/R envelope non-injective even with a tie order (`ISA-9.2-P1.S3`, `ISA-16.1-P1.S2`).
- INV-5 1.1.3: the invocation chain through `lift.call` is not a function of the generated operation (`ISA-11-P4.S1`).
- INV-5 1.4.3: no admission that sees only the object and the schedule decides the maximal-match condition, because nested token budgets are unknown (`ISA-11-P4.S9`, `ISA-9.2-P2.S13`).
- INV-5 1.6.4.3: the default `epsilon_share` ε / N is in general no finite decimal, so it has no written equivalent (`ISA-17-P10.S2`).
- INV-5 1.6.7: defaults of uncovered nested operations cannot be written as entries without changing other operations (`ISA-11-P4.S3`, `ISA-11-P4.S6`); this limits the theorem, not the spec.
- INV-6 1.6.8: agreement on all but one element of D forces agreement on the last when both sides are bijections of D, so "Evidence implies nothing outside the enumerated elements" is false as mathematics (`ISA-12.2-P1.S2`); this limits the theorem, not the spec.


# Background (not graded): `INV-1-matched-pairs.md`

# INV-1: matched compute/uncompute pairs are the identity

Spec: ISA 0.8 (`clauses/ISA-0.8.json`). Format: `proofs/FORMAT.md`.

## Informal statement

Running a well-formed piece of quantum code and then its adjoint, as the adjoint
table builds it, under the same effective control, returns every wire that was
live before to its state, releases every wire the piece allocated clean, and does
nothing to borrowed bundles or to any reference system entangled with them. This
holds with opaque calls inside (an oracle is its own adjoint; `qinplace @g @ginv`
is undone by `qinplace @ginv @g`), and also when the two halves of a matched pair
are separated by code that does not touch what the pair writes. The effective
control is a set: two calls whose predicate stacks list the same wires in a
different order, or with repeats, are under the same control.

## Precise statement

DEFINE `Seg` = finite sequences of the instructions admitted in an action body
(`ISA-5.3-P2.S1`), with `ctl w <call>` and `adj action_call` (`ISA-4.7-P1.S1`).
DEFINE `adj(S)` = the adjoint of S given by the Adjoint table `ISA-5.3-P4.S1`, `ISA-5.3-P4.S2`
("reverse order, instruction replaced, versions renumbered").
DEFINE for a set Π of wires (an effective control context, `ISA-2-P9.S1`) and a fixed
assignment κ of classical arguments, tokens included, fixed at region entry
(`ISA-3.1-P2.S3`): `[[S]]_{Π,κ}` = the operator S realises on the region state of
`ISA-14.2-P1.S1`, with every gate at its specified unitary (`ISA-4.4-P1.S1`,
ε = 0 per `ISA-4.4-P2.S2`).
States are compared on named linear values (`ISA-3.3-P2.S1`): a re-allocated bundle
is identified with the name it is bound to, not with a physical wire.
DEFINE S is *closed* iff every `qreturn` in S has its matching `qborrow` in S.

THEOREM INV-1. For every S ∈ Seg such that S; adj(S) is well-formed (`ISA-3.3-P2.S1`,
`ISA-3.3-P3.S1`, `ISA-3.3-P3.S2`, `ISA-5.1-P1` (whole clause)) and S is closed, every Π, κ, every state ψ of the
wires live at entry of S, and every reference system R:

- (A) `[[S; adj(S)]]_{Π,κ} (ψ ⊗ φ_R) = ψ ⊗ φ_R`, every bundle allocated in S is
  released clean on every basis configuration, and borrowed bundles hold their
  entry values.
- (B) If A is one `oracle_call`, `qinplace` or `action_call` and A' is adj(A) with
  the same callee(s), the same κ, the same operand wires at the versions A
  produced or read, and an equal effective control *set*, and M ∈ Seg writes no
  wire A reads or writes and reads no wire A writes, then
  `[[A; M; A']] = [[M]]`.
- (C) A `lift.oracle_call` followed by its `lift.oracle_uncall` per `ISA-5.5-P1.S1`, `ISA-5.5-P1.S3`
  returns `tgt` and `fr'` to their values before the call.

## Hypotheses

ISA-2-P9.S1, ISA-3.1-P2.S3, ISA-3.2-P8.S1, ISA-3.3-P2.S1, ISA-3.3-P2.S2, ISA-3.3-P3.S1,
ISA-3.3-P3.S2, ISA-3.5-P1.S1, ISA-3.5-P1.S2, ISA-3.5-P1.S3, ISA-4.3-P1.S1,
ISA-4.3-P2.S1, ISA-4.3-P3.S1, ISA-4.3-P4.S1, ISA-4.4-P1.S1, ISA-4.4-P2.S2,
ISA-4.5-P1.S1, ISA-4.5-P2.S1, ISA-4.5-P3.S1, ISA-4.5-P4.S1, ISA-4.5-P5.S1,
ISA-4.5-P5.S2, ISA-4.6-P1.S1, ISA-4.6-P2.S1, ISA-4.6-P3.S1, ISA-4.6-P4.S1,
ISA-4.6-P5.S1, ISA-4.6-P6.S1, ISA-4.6-P7.S1, ISA-4.6-P8.S1, ISA-4.6-P9.S1,
ISA-4.7-P1.S1, ISA-5.1-P1 (whole clause), ISA-5.1-P1.S7, ISA-5.2-P2.S1, ISA-5.2-P2.S2,
ISA-5.2-P2.S3, ISA-5.2-P4.S1, ISA-5.3-P1.S1, ISA-5.3-P2.S1, ISA-5.3-P4.S1,
ISA-5.3-P4.S2, ISA-5.3-P5.S1, ISA-5.4-P1.S4, ISA-5.5-P1.S1, ISA-5.5-P1.S3,
ISA-5.6-P1.S1, ISA-5.6-P2.S1, ISA-5.6-P2.S2, ISA-14.2-P1.S1, ISA-14.2-P1.S2.

## Proof

```
<1>1. [[S]]_{Π,κ} depends on Π only as a set, and control composes:
      C_Π(U) C_Π(V) = C_Π(UV), C_Π(U)† = C_Π(U†).
      PROOF:
  <2>1. The active predicate is the conjunction of the stack wires, and every
        unitary instruction executes controlled on it; the inherited context is
        added the same way.
        BY ISA-3.2-P8.S1, ISA-3.5-P1.S1, ISA-2-P9.S1, ISA-4.7-P1.S1,
        ISA-5.3-P5.S1
  <2>2. A conjunction depends only on the set of its conjuncts (order and
        repetition irrelevant); `ISA-2-P9.S1`: "duplicates count once".
        BY <2>1, ISA-2-P9.S1; algebra
  <2>3. No instruction modifies a wire of the effective control context it
        runs under: "every wire of the effective control context is distinct
        from every target and from every consumed or produced operand".
        BY ISA-3.3-P3.S1
  <2>4. Allocation, borrowing, release and region creation are unconditional;
        only gates are controlled.
        BY ISA-3.5-P1.S3, ISA-5.3-P5.S1
  <2>5. QED
        BY <2>2, <2>3, <2>4; algebra (a projector onto Π=1 that commutes with
        both operators because neither writes Π)
<1>2. For every single non-lifetime instruction i, [[i; adj(i)]]_{Π,κ} = id.
      PROOF:
  <2>1. Gates: rx/ry/rz(θ) then (−θ), s/sdg, t/tdg, and the self-adjoint
        x cx ccx mcx swap h cz compose to I exactly (ε = 0).
        BY ISA-4.4-P1.S1, ISA-5.3-P4.S2; algebra
  <2>2. qxor, qexch: products of cx resp. swap on pairwise distinct wires;
        each factor is an involution and the factors commute.
        BY ISA-4.5-P3.S1, ISA-4.5-P4.S1, ISA-3.3-P3.S1; algebra
  <2>3. qstore, qexchm: for each basis value of the address a exactly one
        branch `a == i` is active and a is not written, so on that branch the
        instruction is one qxor resp. qexch, an involution.
        BY ISA-4.6-P4.S1, ISA-4.6-P5.S1, ISA-3.3-P3.S1, <2>2; algebra
  <2>4. qcopy;quncopy and qload;qunload: the cx fan-out applied twice is I, so
        d is clean on every basis configuration and the release is legal.
        BY ISA-4.5-P1.S1, ISA-4.5-P2.S1, ISA-4.6-P2.S1, ISA-4.6-P3.S1,
        ISA-4.3-P3.S1, ISA-14.2-P1.S2
  <2>5. oracle_call ; oracle_call (same callee, κ, operands): on every basis
        x ∈ D the oracle maps (ins, tgt, fr) to (ins, tgt ⊕ payload, fr ⊕ code)
        and leaves workspace, locations and `in` regions clean or unchanged;
        hence it is an involution, as `ISA-5.2-P2.S3` states ("an involution on
        (ins, tgt, fr) and its own adjoint"), and acts as identity on
        borrowed bundles and entangled external systems.
        BY ISA-5.2-P2.S1, ISA-5.2-P2.S3, ISA-5.2-P4.S1, ISA-4.7-P1.S1,
        ISA-5.3-P4.S2, ISA-5.6-P1.S1; algebra
  <2>6. qinplace @g @ginv tk x ; qinplace @ginv @g tk x = id, provided the
        `ISA-4.5-P5.S1` certificates hold under tk.
        PROOF:
    <3>1. Under tk with fault code FAULT_NONE (= 0) on every input, the
          expansion "t = qalloc; f = qalloc; oracle_call @g (x) t f; qexch x t;
          oracle_call @ginv (x) t f; qfree t; qfree f" maps x ↦ g(x) with t and
          f clean at release, because ginv(g(x)) = x.
          BY ISA-4.5-P5.S1, ISA-4.5-P5.S2, ISA-5.2-P2.S1, ISA-5.2-P2.S2,
          ISA-5.4-P1.S4; algebra
    <3>2. The adjoint instruction realises x ↦ ginv(x) by <3>1 with g, ginv
          exchanged; ginv ∘ g = id.
          BY <3>1, ISA-5.3-P4.S2, ISA-4.5-P5.S1
    <3>3. When tk does not make both oracles fault-free (e.g. B = 0, where the
          code is FAULT_BUDGET_STEPS), the instruction has no defined meaning.
          ASSUMED: `ISA-4.5-P5.S1` requires certificates "under tk" but says
          neither when they are checked nor what happens if they fail; we read
          the instruction as refused before any state change (SPEC-QUESTIONS 26).
    <3>4. QED
          BY <3>1, <3>2, <3>3
  <2>7. qpred w … qunpred w: the pair is reversed as a whole and does not
        change the state; it only changes Π for the enclosed code.
        BY ISA-5.3-P4.S2, ISA-3.5-P1.S2
  <2>8. QED
        BY <2>1, <2>2, <2>3, <2>4, <2>5, <2>6, <2>7, <1>1
<1>3. ASSUME S = i; T with T satisfying (A) (induction hypothesis on the
      well-founded measure (call depth, nesting depth, length), well-founded
      because "Action call graphs are acyclic" (ISA-5.1-P1.S7))
      PROVE  S satisfies (A)
      PROOF:
  <2>1. adj(i; T) = adj(T); adj(i).
        BY ISA-5.3-P4.S1
  <2>2. Case i is a non-lifetime, non-compound instruction.
        BY <2>1, <1>2, induction hypothesis; algebra
  <2>3. Case i = `d = qalloc` (or `qregion` creation, function entry only): after
        T; adj(T) = id, d is |0⟩ (resp. at its image) on every basis
        configuration, so adj(i) = qfree (resp. release with image gates
        reversed) removes a clean factor.
        BY <2>1, ISA-4.3-P1.S1, ISA-4.3-P3.S1, ISA-4.6-P1.S1,
        ISA-14.2-P1.S2
  <2>4. Case i = `qfree d`: the composite ends `qfree d; … ; d' = qalloc`;
        d was clean, d' is clean, and d' is bound to d's name.
        BY <2>1, ISA-4.3-P1.S1, ISA-4.3-P3.S1, ISA-14.2-P1.S2,
        ISA-3.3-P2.S1
  <2>5. Case i = `b = qborrow`; by closedness T = T1; qreturn b; T2.
        PROOF:
    <3>1. Between qborrow and qreturn, b is touched only inside borrow frames,
          each acting as P' ⊗ I_B; hence T1 acts as X ⊗ I_b.
          BY ISA-5.6-P2.S1, ISA-5.6-P2.S2, ISA-5.6-P1.S1
    <3>2. The composite is qborrow b; T1; qreturn b; [T2; adj(T2)]; qborrow b';
          adj(T1); qreturn b'. The bracket is id by hypothesis; b' may be other
          physical wires in another unknown state.
          BY <2>1, induction hypothesis, ISA-4.3-P2.S1, ISA-4.3-P4.S1
    <3>3. (X⁻¹ ⊗ I_b') (X ⊗ I_b) = id on everything but the borrowed pool,
          which is returned untouched.
          BY <3>1, <3>2, ISA-14.2-P1.S2; algebra
    <3>4. QED
          BY <3>3
  <2>6. Case i = `qif w {A}{B}`.
        PROOF:
    <3>1. qif is its expansion qpred w; A; qunpred w; x w; qpred w; B;
          qunpred w; x w, i.e. C_{¬w}(B) C_w(A).
          BY ISA-4.6-P7.S1, <1>1
    <3>2. The flat adjoint of that expansion satisfies (A).
          BY <3>1, <1>2, induction hypothesis (smaller nesting depth)
    <3>3. The table's row `qif w {A}{B} ↦ qif w {adj A}{adj B}` equals the flat
          adjoint of <3>2 when each arm's lifetime instructions are
          self-contained (then C_w(·) and C_{¬w}(·) act on one fixed space and
          commute).
          BY ISA-5.3-P4.S2, ISA-3.5-P1.S1; algebra
    <3>4. Otherwise the row is not even well-formed: for
          `qif p { d = qalloc any 1 } { qfree d }` it yields
          `qif p { qfree d } { d = qalloc any 1 }`, which consumes d before it
          is produced (ISA-3.3-P2.S1).
          OPEN (refuted): the qif row of `ISA-5.3-P4.S2` is wrong for cross-arm
          lifetimes; SPEC-QUESTIONS 28.
    <3>5. QED
          BY <3>2, <3>3 (the table row is valid only under <3>3's condition)
  <2>7. Case i = `qloop n {A}`: qloop is A^n and its adjoint (adj A)^n, so the
        composite is id by n uses of the hypothesis.
        PROOF:
    <3>1. [[qloop n {A}]] = [[A]]^n and adj = qloop n {adj A}.
          BY ISA-4.6-P8.S1, ISA-5.3-P4.S2
    <3>2. Each visit resolves the body's names against the bindings current at
          that visit's entry, and its successor bindings feed the next visit.
          ASSUMED: `ISA-3.3-P2.S2` says "Regions are threaded the same way" but
          nothing says how a loop body's linear names are threaded from one
          visit to the next (council R9-B02).
    <3>3. QED
          BY <3>1, <3>2, induction hypothesis; algebra
  <2>8. Case i = `qloop n while cond {A}`.
        PROOF:
    <3>1. Flags c_1 = cond[0], c_{i+1} = c_i ∧ cond[i] are functions of cond
          only, and neither the body nor anything between the forward loop
          and its adjoint writes cond.
          BY ISA-4.6-P9.S1, ISA-3.3-P3.S1
    <3>2. On each basis value of cond with k leading ones, the forward loop is
          A^k and the table's adjoint ("flags computed forward …; adj A for
          i = n..1 under c_i; flags uncomputed") is (adj A)^k; flags are clean
          after each.
          BY <3>1, ISA-5.3-P4.S2, <1>1; algebra
    <3>3. QED
          BY <3>2, induction hypothesis
  <2>9. Case i = `action_call @b` (or `ctl w`, `adj action_call`): its adjoint
        `adj action_call @b` executes adj(body of @b); the body has smaller
        call depth.
        BY ISA-4.7-P1.S1, ISA-5.3-P1.S1, ISA-5.3-P4.S2, ISA-5.3-P5.S1,
        ISA-5.1-P1.S7,
        induction hypothesis, <1>1
  <2>10. QED
        BY <2>2, <2>3, <2>4, <2>5, <2>6, <2>7, <2>8, <2>9 (cases are exhaustive
        over ISA-5.3-P2.S1; `qreturn` first is excluded by closedness)
<1>4. Part (B): [[A; M; A']] = [[M]].
      PROOF:
  <2>1. An operator that does not write a wire r is block-diagonal in r's
        computational basis: A = Σ_r |r⟩⟨r| ⊗ A_r on its read-only wires.
        BY ISA-14.2-P1.S1, ISA-4.4-P1.S1; algebra
  <2>2. Two operators whose write sets are disjoint and neither of which reads
        the other's writes commute.
        BY <2>1; algebra
  <2>3. A' = adj(A) as an operator only if the callee(s), κ, operand versions
        and effective control *set* agree.
        BY <1>1, <1>2, ISA-5.3-P4.S2
  <2>4. The spec defines such a matching key only for
        lift.oracle_call/lift.oracle_uncall (`ISA-5.5-P1.S3`: "the same token,
        callee, `ins` and `mem` values … the pair shares a dynamic invocation
        identity"); for structured oracle_call, qinplace and action_call pairs
        the key in (B) is our definition.
        ASSUMED: matching key for structured pairs (council SOL-R9-B01, R9-B01,
        R10-B02).
  <2>5. QED
        BY <2>2, <2>3, <2>4, <1>2; algebra (A M A' = M A A' = M)
<1>5. Part (C): lifted pairs restore tgt and fr'.
      PROOF:
  <2>1. The call XORs payload(F_B(x)) into tgt and code(F_B(x)) into fr'.
        BY ISA-5.2-P2.S1, ISA-5.5-P1.S1
  <2>2. The uncall uses the same token, callee, ins and mem values (no
        intervening row writes them, suite F), so F_B(x) is the same and the
        same values are XORed again.
        BY ISA-5.5-P1.S3, ISA-5.2-P2.S2; algebra
  <2>3. QED
        BY <2>1, <2>2
<1>6. QED
      BY <1>3 (with the empty S as base, trivially id), <1>4, <1>5
```

## Witnesses

| Witness | Steps |
|---|---|
| `suite/cases/r9-codex-oracle`, `suite/cases/r9-sol-oracle` (H; O; O; H then borrow/CX/return is identity) | 1.2.5, 1.3 |
| `suite/cases/r9-sol-qinplace` (B ≥ 1 identity; B = 0 refused) | 1.2.6, 1.2.6.3 |
| `suite/cases/r9-loop` (mixed loop re-allocating c) | 1.3.7, 1.3.7.2 (ASSUMED) |
| `suite/cases/actions` (load/unload, store pairs, qexchm pairs, adjoint after action is identity) | 1.2.3, 1.2.4, 1.3 |
| `suite/cases/nested` (`cancel`: call then uncall returns tgt, fr to zero) | 1.5 |
| `tests/r1_borrow.rs`: `r9_opaque_adjoint_restores_borrow_control`, `r9_matched_opaque_oracle_restores_outer_fact`, `r9_qinplace_adjoint_restores_borrow_control`, `r9_qinplace_zero_budget_rejects_before_mutation`, `r9_mixed_loop_threads_reallocated_bindings`, `r10_equivalent_control_sets_preserve_opaque_inverse` | 1.1, 1.2.5, 1.2.6, 1.3.7 |
| `tests/r1_qinplace.rs`: `b07_zero_zero_pair_is_rejected_before_mutation`, `b07_not_not_pair_executes_controlled_and_adjoint`, `r2_qinplace_explicit_adjoint_cleans_workspace` | 1.2.6 |
| `tests/r1_discipline.rs::r2_qif_cross_arm_unconditional_lifetimes_reverse_the_expansion` | 1.3.6 (OPEN 1.3.6.4) |
| `tests/quantum_control.rs::coherent_while_is_prefix_and_padding_with_an_exact_adjoint` | 1.3.8 |
| `tests/quantum.rs`: `every_gate_and_controlled_global_phase`, `bell_state_born_branches_and_adjoint` | 1.2.1, 1.1 |
| `tests/r1_fuzz_discipline.rs`: `generated_r9_opaque_histories_match_independent_identity`, `generated_r9_loop_bindings_match_independent_identity`, `generated_r10_effective_control_sets_match_independent_identity` | 1.1, 1.2.5, 1.3 |

## Council blockers as instances

The theorem is a property of the spec; the round 9–10 blockers were an
implementation (the reference checker) failing to *use* a step, so it rejected
programs that INV-1 proves are the identity.

- SOL-R9-B01, R9-B01 (matched opaque oracle pairs erase the outer H record):
  the checker did not apply 1.2.5 (oracle involution) inside 1.3. The qinplace
  half of SOL-R9-B01 is 1.2.6.
- R9-B02 (mixed loop reuses first-visit bindings): the checker violated the
  reading of 1.3.7.2.
- R10-B02 (lexical predicate stack vs effective-control set): the checker keyed
  inverses by ordered stacks, against 1.1.2.
- SOL-R11-B03 (fixture comment claimed B = 0 qinplace identity): the comment
  ignored the precondition of 1.2.6; the runtime refusal matches 1.2.6.3.

## Spec gaps

1. (1.2.6.3, next to `ISA-4.5-P5` (`ISA-4.5-P5.S1`)) ASSUMED. Needed sentence: "An executor
   checks the conditions on `@g` and `@ginv` under the call's token before any
   state change; if they do not hold the call is refused (CC/R trap) and has no
   effect."
2. (1.3.6.4, next to `ISA-5.3-P4` (`ISA-5.3-P4.S2`)) OPEN (refuted). Needed sentence: "The
   row `qif w {A}{B} ↦ qif w {adj A}{adj B}` applies when each arm's allocations
   and releases are matched within that arm; otherwise the adjoint is the
   adjoint of the complete §4.6 expansion, unconditional lifetime instructions
   included, in reverse order."
3. (1.3.7.2, next to `ISA-3.3-P2` (`ISA-3.3-P2.S2`) and `ISA-4.6-P8`
   (`ISA-4.6-P8.S1`)) ASSUMED. Needed
   sentence: "A `qloop` body is threaded like a block: each visit resolves names
   against the bindings live at its entry, and the bindings live at its exit are
   the entry bindings of the next visit; they MUST agree in names and types."
4. (1.4.4, next to `ISA-5.3-P4` (`ISA-5.3-P4.S2`) and `ISA-6.2-P1`
   (`ISA-6.2-P1.S2`)) ASSUMED. Needed sentence:
   "Two operations form a matched pair iff the second is the §5.3 adjoint of the
   first with the same callee(s), the same classical arguments (token
   included), the same operand wires at the versions the first read or
   produced, and equal effective control sets (§2); predicate-stack order and
   repetition are irrelevant."


# Background (not graded): `INV-2-no-clone.md`

# INV-2: no clone, no alias

Spec: ISA 0.8 (`clauses/ISA-0.8.json`). Format: `proofs/FORMAT.md`.

## Informal statement

The ISA never duplicates quantum state, at either level where duplication could
happen. By name: in structured code every wire belongs to exactly one live
linear value, and in CC every device wire is reachable through at most one usable
`qreg` handle, so no instruction sees a wire twice or under two names. By state:
every Q semantics is linear and isometric, so no instruction sequence maps
ψ ⊗ |0⟩ to ψ ⊗ ψ for two distinct non-orthogonal ψ. The instructions that
"copy" (`qcopy`, `qload`, oracle `tgt` writes) copy computational-basis values
only: they entangle target with source, and a copy into workspace is a `perm`
value bound to be uncomputed before the region exits.

## Precise statement

DEFINE `Seg`, `[[S]]_{Π,κ}` as in INV-1. DEFINE for a program point p of a
well-formed region body: `Live(p)` = the set of live linear wire values
(`ISA-3.3-P2.S1`), and `wires(v)` = the physical wires of value v. DEFINE for a CC
program point: a handle is *usable* iff it is live (`ISA-3.3-P6.S2`).

THEOREM INV-2.

- (A) No alias in structured code. For every well-formed region body and point
  p, the sets `wires(v)`, v ∈ Live(p), are pairwise disjoint, and every v ∈
  Live(p) has exactly one producer: an interface binding, an allocation
  (`qalloc`, `qborrow`, `qregion`), a `produce`-mode result, or the successor
  of an `in`-mode operand.
- (B) No alias inside an instruction. The wires of the wire operands of one
  instruction are pairwise disjoint and disjoint from its effective control
  context.
- (C) No alias of CC handles. At every CC point, the wire sets of usable handles
  are pairwise disjoint.
- (D) No clone. There are no S ∈ Seg, Π, κ, wires a, b (b allocated clean by S
  or a clean bundle), and states ψ1, ψ2 of a with 0 < |⟨ψ1|ψ2⟩| < 1 such that
  `[[S]](ψi ⊗ |0⟩_b ⊗ e) = ψi ⊗ ψi ⊗ e_i` for i = 1, 2.
- (E) Basis copies are entangled and obligated. `d = qcopy s` maps
  Σ_x α_x |x⟩_s |0⟩_d to Σ_x α_x |x⟩_s |x⟩_d, which equals ψ ⊗ ψ only when ψ
  is a basis state; d is a `perm` value whose dependency set contains s, and
  d must be released clean before the region exits.

## Hypotheses

ISA-2-P2.S1, ISA-2-P9.S1, ISA-3.2-P1.S1, ISA-3.3-P1.S1, ISA-3.3-P2.S1, ISA-3.3-P2.S3,
ISA-3.3-P3.S1, ISA-3.3-P3.S2, ISA-3.3-P6.S2, ISA-3.3-P7.S1, ISA-3.3-P8.S1,
ISA-3.3-P9.S1, ISA-3.3-P10.S1, ISA-3.3-P11.S1, ISA-3.3-P12.S1, ISA-3.3-P13.S1,
ISA-3.3-P13.S2, ISA-3.3-P14.S2, ISA-3.5-P1.S1, ISA-3.7-P2.S1, ISA-4.3-P1.S1,
ISA-4.3-P2.S1, ISA-4.4-P1.S1, ISA-4.5-P1.S1, ISA-4.6-P1.S1, ISA-4.7-P1.S2,
ISA-5.1-P1.S1, ISA-5.1-P1.S3, ISA-5.1-P1.S5, ISA-5.1-P1.S6, ISA-5.2-P2.S3,
ISA-5.3-P1.S1, ISA-6.1-P3.S1, ISA-6.2-P1.S3, ISA-10-P3.S2, ISA-14.2-P1.S2.

## Proof

```
<1>1. (A) holds at every point of a well-formed region body.
      PROOF:
  <2>1. At entry, Live = the interface values, and "A region's interface
        bundles and regions are pairwise disjoint".
        BY ISA-3.3-P3.S2, ISA-5.1-P1.S1
  <2>2. A value is "produced once and consumed once"; `in` mode consumes and
        re-produces a successor on the same wires; "a name is not used after
        `consume`".
        BY ISA-3.3-P2.S1
  <2>3. `qalloc` and `qborrow` add new tensor factors to the region state, so
        their wires are disjoint from every live value's wires; `qregion`
        cells likewise at function entry.
        BY ISA-14.2-P1.S2, ISA-4.3-P1.S1, ISA-4.3-P2.S1, ISA-4.6-P1.S1
  <2>4. The producers listed in (A) are the only producers; in particular a
        `regs` declaration in an action or permutation action produces no
        wire value.
        ASSUMED: `ISA-3.3-P1.S1` says `reg[N]` is "a location (oracle bodies,
        lprocs); not linear" and `ISA-3.7-P2.S1` says oracles and lprocs declare
        `regs`, but the `regs` grammar admits any type in any function and no
        clause forbids a wire-typed `regs` entry in an action (council
        SOL-R11-B01).
  <2>5. An indexed operand `w[i]` "borrows wire i for one instruction" and
        creates no new live value.
        BY ISA-3.3-P2.S3
  <2>6. QED
        BY <2>1, <2>2, <2>3, <2>4, <2>5; induction over program points
<1>2. (B) holds for every instruction of a well-formed body.
      PROOF:
  <2>1. "The wire operands of one instruction are pairwise distinct; every
        wire of the effective control context is distinct from every target
        and from every consumed or produced operand".
        BY ISA-3.3-P3.S1, ISA-2-P9.S1
  <2>2. "Distinct" is about wires, not operand spellings: a bundle `w` and its
        indexed wire `w[i]` (or two indexed operands `w[i]`, `w[i]`) in one
        instruction overlap and are excluded.
        ASSUMED: `ISA-3.3-P3.S1` does not say whether distinctness is judged on
        names or on the wires they denote; only the wire reading makes the gate
        semantics of `ISA-4.4-P1.S1` well-defined (a `cx a a`
        has no unitary).
  <2>3. A wire of the effective control context may still be read by the
        instruction as a source or `in` operand (it is neither target nor
        consumed nor produced).
        BY ISA-3.3-P3.S1
  <2>4. QED
        BY <2>1, <2>2, <2>3 (reads of control wires are not aliases: no wire
        is both written and read under two names)
<1>3. (C) holds at every CC point.
      PROOF:
  <2>1. "A handle is in exactly one state: live, viewed … or consumed"; an
        instruction whose precondition fails is a CC trap.
        BY ISA-3.3-P6.S2
  <2>2. Each transition preserves disjointness of usable wire sets:
        `qreg.new` gives fresh wires; `qreg.slice` makes the parent viewed
        (unusable: "any use of q while viewed is ill-formed") and the view
        live over a subset; after its one region call the view is consumed and
        the parent live again; `qreg.concat` consumes both parts;
        `qreg.free` and `measure` consume; a region call leaves q unchanged.
        BY ISA-3.3-P7.S1, ISA-3.3-P8.S1, ISA-3.3-P9.S1, ISA-3.3-P10.S1,
        ISA-3.3-P11.S1, ISA-3.3-P12.S1
  <2>3. Reversal of a `qreg.*` frame restores the handle states before that
        frame, where disjointness held; a `measure` frame is never reversed.
        BY ISA-3.3-P13.S1, ISA-3.3-P13.S2
  <2>4. `qreg.new` wires are distinct from the wires of every other live or
        viewed handle, and host-supplied register ids name pairwise disjoint
        registers.
        ASSUMED: `ISA-3.3-P7.S1` says only "q live, clean"; `ISA-3.3-P14.S2` makes
        host ids `qreg` values and `ISA-10-P3.S2` gives a run exclusive ownership
        of the registers it touches, but no clause says two ids passed to one
        run denote disjoint wires.
  <2>5. Handle *values* can be duplicated by classical dataflow (CC is dynamic
        SSA), so the same handle can reach two operand slots of one region
        call; this is an alias of the call's interface bundles.
        BY ISA-3.2-P1.S1, ISA-4.7-P1.S2, ISA-3.3-P11.S1
  <2>6. Such a call is a CC trap with no effect.
        ASSUMED: `ISA-3.3-P3.S2` makes overlapping interface bundles ill-formed
        in Q, and `ISA-3.3-P6.S2` traps failed handle preconditions, but the
        region-call row `ISA-3.3-P11.S1` lists only "q live (a view included)" as
        precondition; disjointness of the call's qreg operands is not stated
        as a CC precondition.
  <2>7. QED
        BY <2>1, <2>2, <2>3, <2>4, <2>6; induction over CC execution
<1>4. (D) no clone.
      PROOF:
  <2>1. [[S]] is linear and isometric on the states where every release in S
        is of a clean bundle: gates are unitary, `qalloc` tensors |0⟩,
        `qfree` removes clean factors, borrowed factors see U ⊗ I, oracle and
        action calls are unitary, and no region contains `measure`.
        BY ISA-14.2-P1.S2, ISA-4.4-P1.S1, ISA-5.2-P2.S3, ISA-5.3-P1.S1,
        ISA-5.1-P1.S3, ISA-3.5-P1.S1
  <2>2. If [[S]](ψi ⊗ 0 ⊗ e) = ψi ⊗ ψi ⊗ e_i for i = 1, 2 then
        ⟨ψ1|ψ2⟩ = ⟨ψ1|ψ2⟩² ⟨e_1|e_2⟩, so |⟨ψ1|ψ2⟩| ≤ |⟨ψ1|ψ2⟩|², i.e.
        |⟨ψ1|ψ2⟩| ∈ {0} or ≥ 1.
        BY <2>1; algebra
  <2>3. QED
        BY <2>2 (contradicts 0 < |⟨ψ1|ψ2⟩| < 1)
<1>5. (E) basis copies.
      PROOF:
  <2>1. `d = qcopy s` allocates d clean and applies `cx s[i] d[i]` under the
        predicate, giving Σ α_x |x⟩|x⟩; this is a product state iff at most
        one α_x ≠ 0.
        BY ISA-4.5-P1.S1, ISA-3.5-P1.S1; algebra
  <2>2. d has provenance perm with S = {s} ∪ Π.
        BY ISA-6.1-P3.S1
  <2>3. "Every perm value MUST be cleaned within its window and before its
        region exits", and every `qalloc` is matched by a `qfree` of a clean
        bundle; so no workspace copy survives the region.
        BY ISA-6.2-P1.S3, ISA-5.1-P1.S5, ISA-5.3-P1.S1
  <2>4. `in` wires of actions are readable only as controls, diagonal targets,
        `qcopy`/`qxor` sources or `in` call arguments, so a copy never
        modifies its source.
        BY ISA-5.1-P1.S6
  <2>5. QED
        BY <2>1, <2>2, <2>3, <2>4
<1>6. QED
      BY <1>1, <1>2, <1>3, <1>4, <1>5
```

## Witnesses

| Witness | Steps |
|---|---|
| `suite/cases/registers` (concat/free, views through region calls, unclean free traps, measurement) | 1.3 |
| `suite/cases/actions` (`flip`: d = p copied, XORed into t, uncomputed) | 1.5 |
| `tests/structured.rs`: `tier_arity_aliasing_and_input_roles`, `cleanup_windows_and_linear_lifetimes` | 1.1, 1.2, 1.5.4 |
| `tests/parser.rs`: `r11_action_regs_do_not_produce_wires`, `r11_register_types_follow_function_kind`; `tests/cli_xam.rs::r11_cli_action_regs_reject_before_execution` | 1.1.4 (ASSUMED) |
| `tests/discipline.rs::release_cannot_consume_its_effective_control` | 1.2.1 |
| `tests/registers.rs`: `register_handles_enforce_views_consumption_and_cleanliness`, `viewed_parent_and_view_only_one_call_are_static_errors`, `allocation_views_and_region_calls_reverse_with_their_frames`, `r4_dynamic_interface_alias_is_an_atomic_reversible_cc_and_r_fault`, `r4_dynamic_control_target_alias_is_an_atomic_reversible_cc_and_r_fault`, `r4_dynamic_control_can_overlap_a_readonly_input`, `r4_dynamic_oracle_input_output_alias_is_an_atomic_reversible_cc_and_r_fault` | 1.3 (1.3.6 ASSUMED), 1.2.3 |
| `tests/quantum.rs`: `actions_copy_cleanup_quantum_memory_loops_and_adjoint`, `sol_r5_b03_consumed_workspace_names_keep_their_own_widths` | 1.5, 1.1.2 |

## Council blockers as instances

- SOL-R11-B01 (an action obtains a live wire from its `regs` line with no
  producer): a direct violation of (A)'s single-producer clause, admitted
  because step 1.1.4 is not in the spec.
- R11-B01 (an action `regs` name used as a rotation angle): not an alias, but
  the same missing kind restriction as 1.1.4, on the classical side
  (`ISA-3.1-P2.S3` "classical arguments fixed at region entry").

## Spec gaps

1. (1.1.4, next to `ISA-3.7-P2` (`ISA-3.7-P2.S1`) and
   `ISA-3.3-P1` (`ISA-3.3-P1.S1`)) ASSUMED. Needed sentence: "Only
   oracles and lprocs declare locations; the `regs` list of an action, permutation
   action, CC or R function MUST be empty (it may carry `bounds`)."
2. (1.2.2, next to `ISA-3.3-P3` (`ISA-3.3-P3.S1`)) ASSUMED. Needed sentence: "Distinctness is
   judged on wires: a bundle operand and an indexed operand of it, or two
   indexed operands naming the same wire, are not distinct."
3. (1.3.4, next to `ISA-3.3-P7` (`ISA-3.3-P7.S1`) and `ISA-3.3-P14`
   (`ISA-3.3-P14.S2`)) ASSUMED. Needed sentence:
   "`qreg.new` yields wires disjoint from every live or viewed register; the
   register ids passed to one run MUST denote pairwise disjoint registers, else
   `bennett_run` fails with `E_ARG`."
4. (1.3.6, next to `ISA-3.3-P11` (`ISA-3.3-P11.S1`)) ASSUMED. Needed sentence: "A region call in CC
   or R whose `qreg` operands share a wire is a CC trap before any effect."


# Background (not graded): `INV-3-discipline-soundness.md`

# INV-3: soundness of the static uncomputation discipline

Spec: ISA 0.8 (`clauses/ISA-0.8.json`). Format: `proofs/FORMAT.md`.
Borrow-domain interpretation: the binding 2026-11-01 ISA 0.8 erratum
(`../bennett-isa-spec/spec/errata-0.8.md`) incorporates ISA 0.9 §5.6.
New `ISA-5.6-P13.S5` / `.S6` citations below name that 0.9 statement layer;
other IDs retain the 0.8 graph unless explicitly qualified.
Depends on: INV-1 (steps cited as `INV-1:1.4` etc.).

## Informal statement

If a region body passes the static checks of §5.1 (explicit cleanup), §5.6
(borrow frames) and §6 (provenance, windows, unitary cleanup), then at run time,
under any inherited control, every `qfree` releases a bundle that is |0⟩ on every
branch and factorises from the rest of the state, every borrowed bundle comes
back with the identity applied to it and to anything entangled with it, and the
region exits with clean workspace. This is the content of T5 (`ISA-14.3-P5.S1`, "As
§6.3") extended to borrowing. The result: proved for `perm` values under three
ASSUMED readings; **false for `other` values under the literal 0.8 text** (a
known counterexample); proved for borrow frames (both the T3 route and the
translation lemma) under one ASSUMED reading about controls.

## Precise statement

DEFINE `Seg`, `[[S]]_{Π,κ}` as in INV-1. DEFINE a region body Γ is *disciplined*
iff it is well-formed under `ISA-5.1-P1` (whole clause), `ISA-5.6-P2.S1`,
`ISA-5.6-P2.S2`, `ISA-5.6-P3.S1`, `ISA-5.6-P4.S1`, `ISA-5.6-P5.S1`, `ISA-5.6-P6.S1`,
`ISA-6.1` (whole section), `ISA-6.2-P1` (whole clause) and `ISA-6.4-P1.S1`,
`ISA-6.4-P1.S2` (no "ill-formed" verdict).

THEOREM INV-3. For every disciplined action or permutation-action body Γ, every
inherited control context Π, classical arguments κ, entry state ψ and reference
system R (entangled with ψ's borrowed and external parts):

- (a) at every `qfree d` executed by `[[Γ]]_{Π,κ}`, the state is |0⟩_d ⊗ χ;
- (b) at every `qreturn b`, the operator applied since the matching `qborrow`
  agrees with X ⊗ I_b ⊗ I_R on the reachable entry-state support for some X;
- (c) at exit the workspace, locations and local regions are clean / at image
  and the region's operation is its declared operation ⊗ identity on borrowed
  bundles and R (`ISA-5.3-P1.S1`, `ISA-5.6-P1.S1`).

## Hypotheses

ISA-2-P9.S1, ISA-3.3-P3.S1, ISA-3.5-P1.S1, ISA-3.5-P1.S3, ISA-4.3-P3.S1, ISA-4.4-P1.S1,
ISA-4.5-P3.S1, ISA-4.6-P1.S1, ISA-5.1-P1 (whole clause), ISA-5.1-P1.S5, ISA-5.2-P2.S1,
ISA-5.3-P1.S1, ISA-5.3-P5.S1, ISA-5.6-P1.S1, ISA-5.6-P2.S1, ISA-5.6-P2.S2,
ISA-5.6-P3.S1, ISA-5.6-P4.S1, ISA-5.6-P5.S1, ISA-5.6-P6.S1, ISA-5.6-P7.S1,
ISA-6.1 (whole section), ISA-6.1-P1.S1, ISA-6.1-P1.S2, ISA-6.1-P1.S3, ISA-6.1-P2.S1,
ISA-6.1-P3.S1, ISA-6.1-P9.S1, ISA-6.1-P10.S1, ISA-6.1-P11.S1, ISA-6.1-P14.S1,
ISA-6.2-P1 (whole clause), ISA-6.2-P1.S1, ISA-6.2-P1.S2, ISA-6.2-P1.S4, ISA-6.3-P1.S1,
ISA-6.4-P1.S1, ISA-6.4-P1.S2, ISA-6.4-P1.S4, ISA-14.2-P1.S1, ISA-14.3-P3.S1,
ISA-14.3-P5.S1. Additionally ISA-5.6-P2.S3, ISA-5.6-P13.S5 and
ISA-5.6-P13.S6 from ISA 0.9 §5.6, incorporated by the 0.8 erratum.

## Proof

```
<1>1. Every workspace bundle, location and cell version of Γ has provenance
      perm (with a dependency set S) or other.
      PROOF:
  <2>1. The §6.1 table assigns provenance to qalloc, qcopy, qload, qxor, qexch,
        qstore, qexchm, permutation/diagonal/non-diagonal gates, oracle_call,
        permutation and non-permutation action calls, qinplace and lifted rows.
        BY ISA-6.1-P1.S1, ISA-6.1-P2.S1, ISA-6.1-P3.S1, ISA-6.1-P9.S1,
        ISA-6.1-P10.S1, ISA-6.1-P11.S1, ISA-6.1-P14.S1
  <2>2. `quncopy`, `qunload` and the release instructions are cleanups, not
        computations, and need no row.
        BY ISA-6.2-P1.S2, ISA-6.4-P1.S1, ISA-5.1-P1.S5
  <2>3. A local `qregion` cell starts at version 0 with provenance perm and
        S = ∅ (its image gates are X gates on clean wires).
        ASSUMED: `ISA-4.6-P1.S1` creates the cells and `ISA-6.1-P1.S2` says "cell
        versions advance on every write", but the table has no row for
        `qregion` creation.
  <2>4. QED
        BY <2>1, <2>2, <2>3
<1>2. A perm value g computed under Π by sequence C and cleaned by the
      `reverse` realisation within its window is |0⟩ on every branch and
      factorises.
      PROOF:
  <2>1. DEFINE R = the wires of S, G = g's wires, C the exact computing
        sequence, a permutation with C|r⟩|0⟩_G = |r⟩|f(r)⟩ (controlled on Π).
        BY ISA-6.1-P1.S1, ISA-6.1-P1.S3, ISA-6.1-P2.S1, ISA-6.1-P9.S1, <1>1
  <2>2. Every operation O between C and its cleanup is block-diagonal in the
        computational basis of R ∪ G: O = Σ_{r,x} |r,x⟩⟨r,x| ⊗ O_{r,x}.
        PROOF:
    <3>1. Diagonal gates leave values unchanged; a non-diagonal gate on a wire
          of S or g closes the window.
          BY ISA-6.1-P10.S1, ISA-6.1-P11.S1, ISA-6.2-P1.S1
    <3>2. A version advance of a cell in S, or a non-permutation action call
          touching S, closes the window.
          BY ISA-6.2-P1.S1, ISA-6.1-P14.S1
    <3>3. Oracle calls and permutation action calls with wires of R ∪ G only as
          `ins` or `in` regions are block-diagonal on them ("ins unchanged";
          "block-diagonal in the computational basis of `ins`").
          BY ISA-5.2-P2.S1, ISA-5.3-P1.S1
    <3>4. A permutation change to a wire of S that is "undone before g's
          cleanup" yields, together with its undoing, a block-diagonal operator.
          ASSUMED: `ISA-6.2-P1.S1` does not define "undone"; we read it as: the
          change and its undoing form a matched pair (INV-1 (B)) with only
          R∪G-block-diagonal operations between them.
    <3>5. A permutation gate targeting a wire of g produces a new version of g;
          the cleanup of the old version requires g's current version to be the
          one C produced.
          ASSUMED: `ISA-6.2-P1.S2` requires "the versions that sequence read to be
          current", which taken literally includes g's pre-computation version
          (C reads its own targets) and can then never hold; we read it as: the
          versions of S that C read, and the version of g that C produced.
    <3>6. QED
          BY <3>1, <3>2, <3>3, <3>4, <3>5
  <2>3. The cleanup runs C† under the same effective control set Π.
        ASSUMED: `ISA-6.2-P1.S2` binds a cleanup "to its exact computing
        sequence" but does not say that the effective control set is part of
        that sequence; with Π' ≠ Π, g survives on the branch Π = 1, Π' = 0.
        (Π ⊆ S fixes the control *values*, not the control *context* of the
        cleanup.) Same gap as INV-1 gap 4.
  <2>4. C† O C |r,0⟩_G|χ⟩ = |r,0⟩_G O_{r,f(r)}|χ⟩; by linearity G is |0⟩ in
        every term, so G factorises; the remaining O_{r,f(r)} are the
        "corresponding diagonal phases" of `ISA-6.3-P1.S1`.
        BY <2>1, <2>2, <2>3, ISA-14.2-P1.S1; algebra
  <2>5. QED
        BY <2>4, ISA-6.3-P1.S1
<1>3. A perm value cleaned by the `recompute` realisation within its window is
      |0⟩ on every branch and factorises.
      PROOF:
  <2>1. `recompute` computes g' by the same sequence into a fresh clean bundle,
        `qxor`s it into g and uncomputes g' by the adjoint.
        BY ISA-6.4-P1.S1
  <2>2. Within the window R holds its computation-time values on every branch,
        so g' = f(r) = g and the qxor clears g.
        BY <1>2, ISA-4.5-P3.S1; algebra
  <2>3. The qxor is block-diagonal on R ∪ G', so the adjoint clears g' by the
        argument of 1.2.4.
        BY <2>2, <1>2
  <2>4. QED
        BY <2>2, <2>3
<1>4. An `other` value released by "the adjoint of the sequence that produced
      it" is |0⟩ on every branch.
      PROOF:
  <2>1. If no operation between the producing sequence A and adj(A) writes a
        wire A writes or reads one, adj(A) restores it.
        BY INV-1:1.4, ISA-6.2-P1.S4
  <2>2. ISA 0.8 does not require that hypothesis, and without it the claim is
        false: `h d0; ccx d0 p d1; cx d1 t; ccx d0 p d1; h d0; qfree d0`
        (t a `mut` interface wire) passes §6 literally (d0 other by
        `ISA-6.1-P11.S1`; d1 perm with d0 ∈ S by `ISA-6.1-P9.S1`, cleaned within its
        window; interface wires carry no obligation; d0 released by the adjoint
        `h d0`). For p = 1, t = 0 the state before release is
        (|0⟩(|0⟩+|1⟩) + |1⟩(|0⟩−|1⟩))/2 on (d0, t): d0 is not clean.
        OPEN (refuted): soundness for `other` values; SPEC-QUESTIONS 25.
  <2>3. Under the reading of SPEC-QUESTIONS 25 ("only while no other live value
        or outstanding diagonal phase depends on it") the hypothesis of <2>1
        holds.
        OPEN: needs a definition of "depends" that covers interface `mut`
        wires and diagonal phases; not proved here.
  <2>4. QED
        BY <2>1 (only in the case <2>1 covers)
<1>5. Every completed borrow lifetime acts as X ⊗ I_b ⊗ I_R on reachable states.
      PROOF:
  <2>1. Borrowed wires are touched only inside borrow frames, each
        permutation-only; outside frames the lifetime does not touch b.
        BY ISA-5.6-P2.S1
  <2>2. A frame established by a T3 claim over D_F (every value of b
        included) satisfies P_F|span(D_F) = (P' ⊗ I_B)|span(D_F).
        BY ISA-5.6-P2.S3 (0.9, incorporated by the 0.8 erratum),
        ISA-14.3-P3.S1; algebra
  <2>3. A frame of the form V; W; V⁻¹; W satisfying (i)–(iv) satisfies
        P_F = P' ⊗ I_B.
        PROOF:
    <3>1. V's gates are X-family flips with targets in B and controls in X,
          X ∩ B = ∅; they commute and are involutions; V maps b ↦ b ⊕ v(X) and
          leaves X fixed; V⁻¹ (exact reverse) undoes it.
          BY ISA-5.6-P3.S1, ISA-5.6-P6.S1, ISA-4.4-P1.S1; algebra
    <3>2. No target of W is a control of W, in X or in B, so W's gates
          commute, each is an involution, and every control value is constant
          during W.
          BY ISA-5.6-P4.S1; algebra
    <3>3. Each W gate g does t_g ⊕= c_g(Y, X)·b_{j(g)} (one B control) or
          t_g ⊕= c_g(Y, X) (none).
          BY ISA-5.6-P5.S1, <3>2; algebra
    <3>4. Over V; W; V⁻¹; W the net map is t_g ⊕= c_g(Y, X)·v_{j(g)}(X) (the
          terms without a B control cancel), b and X are restored, and nothing
          depends on b: the dirty-ancilla identity of `ISA-5.6-P7.S1`.
          BY <3>1, <3>2, <3>3, ISA-5.6-P7.S1; algebra
    <3>5. The active predicate and inherited control context count as controls
          of every gate of V and W in (i)–(iii), and V⁻¹ runs under the same
          effective control set as V.
          ASSUMED: `ISA-3.5-P1.S1` controls every gate on the active predicate,
          but `ISA-5.6-P3.S1`, `ISA-5.6-P4.S1`,
          `ISA-5.6-P5.S1`, `ISA-5.6-P6.S1` speak of a gate's controls without
          saying whether the predicate is included; if V⁻¹ ran under a
          different set, "exact reverse sequence" would hold lexically but not
          as operators.
    <3>6. QED
          BY <3>4, <3>5
  <2>4. Maximality of a frame inside a `qloop`/`qif` body is judged within the
        body's static instruction sequence.
        ASSUMED: "maximal contiguous" in `ISA-5.6-P2.S1` does not say whether it
        is judged on the unrolled execution or on the static sequence
        (SPEC-QUESTIONS 30); either reading gives a factorising frame, but the
        frames differ, so certificate keys must agree on one.
  <2>5. Composing the frame equalities and operators not touching b gives
        X ⊗ I_b on the reachable entry-state support, including any R.
        PROOF:
    <3>1. At each frame entry the actual state has support in span(D_F);
          D_F over-approximates the region-prefix reachable entry states and
          includes every borrowed/interface value independently.
          BY ISA-5.6-P13.S5 (0.9, incorporated by the 0.8 erratum)
    <3>2. Expand that state (including R) as Σ_d |d⟩|r_d⟩ with d ∈ D_F.
          Applying the restricted equality term by term gives the same state
          as P' ⊗ I_B ⊗ I_R; linearity requires no full-operator equality
          outside span(D_F).
          BY <2>2, <2>3, <3>1, ISA-5.6-P13.S6 (0.9); algebra
    <3>3. Induct along the actual prefix: each next frame again satisfies
          <3>1, and intervening operators do not touch b. The product of
          these equalities on the successive reachable states gives X ⊗ I_b
          ⊗ I_R for the completed lifetime.
          BY <2>1, <3>1, <3>2; algebra
    <3>4. QED
          BY <3>3
  <2>6. QED
        BY <2>2, <2>3, <2>4, <2>5
<1>6. Under an inherited control w the conclusions hold on both branches.
      PROOF:
  <2>1. In `ctl w @a`, workspace, regions and flags are allocated
        unconditionally and every gate of the body and its cleanup runs under
        w; on the branch w = 0 no gate acts, so workspace stays |0⟩ / at image.
        BY ISA-5.3-P5.S1, ISA-3.5-P1.S1, ISA-3.5-P1.S3
  <2>2. On the branch w = 1 the body runs with Π ∪ {w}; apply <1>2–<1>5.
        BY <1>2, <1>3, <1>4, <1>5, ISA-2-P9.S1
  <2>3. Cleanup schedules are keyed by inherited control count and every
        admitted realisation is unitary.
        BY ISA-6.4-P1.S1, ISA-6.4-P1.S4
  <2>4. QED
        BY <2>1, <2>2, <2>3; algebra (block-diagonal in w)
<1>7. Every `qfree d` in a disciplined body releases a bundle whose current
      version is its `qalloc` version or the output of a §6.4 cleanup.
      ASSUMED: `ISA-4.3-P3.S1` states the dynamic precondition ("clean on every
      basis configuration") and `ISA-5.1-P1.S5` requires matching by "explicit
      cleanup instructions", but no clause states how the static discipline
      decides that a particular `qfree` meets the precondition.
<1>8. QED
      BY <1>1, <1>2, <1>3, <1>5, <1>6, <1>7 for (a)–(c) on perm values and
      borrowed bundles; (a) and (c) for `other` values only in the case of
      1.4.1 (the general case is OPEN, refuted for the literal text).
```

## Witnesses

| Witness | Steps |
|---|---|
| `suite/cases/r9-codex-oracle`, `r9-sol-oracle`, `r9-sol-qinplace`, `r9-loop` (borrow/CX/return after a cleaned control; tagged ISA-5.6, ISA-6.4) | 1.5, 1.2 |
| `suite/cases/actions` (`flip`: perm copy cleaned by reverse) | 1.2 |
| `tests/discipline.rs`: `cleanup_adjoint_cannot_skip_an_entangling_reader` (the 1.4.2 counterexample, rejected under SPEC-QUESTIONS 25), `other_scratch_requires_the_exact_adjoint_but_accepts_h_h`, `cleanup_pins_predicate_versions_and_distinguishes_qif_polarity`, `local_regions_require_explicit_restoration_and_load_pins_cell_versions` | 1.4, 1.2.3, 1.1.3 |
| `tests/r1_discipline.rs`: `fable_r1_b3_predicate_flip_closes_the_window`, `codex_b03_predicate_versions_and_windows_start_at_the_computation`, `fuzz_witnesses_of_entangling_reads_are_rejected`, `r2_complementary_diagonal_phases_do_not_cancel`, `r2_exchange_inverse_must_cancel_both_outputs_together` | 1.2.2, 1.4.2 |
| `tests/r1_fuzz_discipline.rs`: `accepted_random_actions_run_exactly_clean`, `accepted_random_actions_run_exactly_clean_sweep` (every accepted program runs clean: the empirical form of (a)–(c) for the interpreter's stricter discipline) | 1.8 |
| `tests/borrow.rs`: `translation_lemma_checks_all_four_required_negative_patterns`, `translation_pattern_returns_an_entangled_borrowed_system`, `borrow_frame_exhaustion_rejects_hidden_dependence_on_borrowed_bits`, `exhaustive_borrow_identity_need_not_be_adjacent_gate_cancellation` | 1.5.2, 1.5.3 |
| `tests/r1_borrow.rs`: `borrow_frames_inside_bounded_loops_are_composed_not_unrolled`, `r4_loop_local_returns_cannot_be_restored_by_later_borrowings` | 1.5.4, 1.5.5 |
| `tests/r1_certificates.rs::muse_r5_translation_frame_maximality_is_within_its_static_sequence` | 1.5.4 |

## Council blockers as instances

Rounds 9–10 blockers (SOL-R9-B01, R9-B01, R9-B02, R10-B02) were *completeness*
failures of the reference checker: it rejected programs that are clean, because
it did not recognise matched pairs (INV-1 1.2.5, 1.2.6, 1.4) or keyed controls
by ordered stacks (INV-1 1.1.2). They do not refute INV-3; they show that the
discipline's "exact computing sequence" (1.2.3) needs the matching key of INV-1
gap 4 to be decidable the same way by every implementation. The SPEC-QUESTIONS 25
fuzz finding is the one known *soundness* failure, step 1.4.2.

## Spec gaps

1. (1.1.3, next to `ISA-6.1-P1` (`ISA-6.1-P1.S1`), `ISA-4.6-P1`
   (`ISA-4.6-P1.S1`)) ASSUMED. Needed row: "| `qregion`
   creation | every cell: version 0, perm, S = ∅ |".
2. (1.2.2.4, next to `ISA-6.2-P1` (`ISA-6.2-P1.S1`)) ASSUMED. Needed sentence: "A permutation change
   to a wire of S is undone when it and its undoing form a matched pair (§5.3)
   and every operation between them leaves the computational-basis values of S
   and g unchanged."
3. (1.2.2.5, next to `ISA-6.2-P1` (`ISA-6.2-P1.S2`)) ASSUMED. Needed sentence: "A cleanup requires
   the versions of S that the computing sequence read, and the version of g that
   it produced, to be current."
4. (1.2.3, next to `ISA-6.2-P1` (`ISA-6.2-P1.S2`)) ASSUMED. Needed sentence: "A cleanup runs under
   the effective control set (§2) of its computing sequence."
5. (1.4.2, next to `ISA-6.2-P1` (`ISA-6.2-P1.S4`)) OPEN (refuted). Needed sentence (SPEC-QUESTIONS 25):
   "An `other` value is released only by the adjoint of its computing sequence,
   and only while no other live value, interface wire or outstanding diagonal
   phase depends on it."
6. (1.4.3, next to `ISA-6.1-P1` (`ISA-6.1-P1.S1`)) OPEN. Needed: a definition of "depends on" that
   extends dependency sets to interface `mut` wires and to diagonal phases.
7. (1.5.3.5, next to `ISA-5.6-P3` (`ISA-5.6-P3.S1`)) ASSUMED. Needed sentence: "In (i)–(iii) a
   gate's controls include the effective control context; V⁻¹ runs under the
   same effective control set as V."
8. (1.5.4, next to `ISA-5.6-P2` (`ISA-5.6-P2.S1`)) ASSUMED. Needed sentence (SPEC-QUESTIONS 30):
   "Maximality of a frame inside a `qloop` or `qif` body is judged within that
   body's instruction sequence."
9. (1.7, next to `ISA-4.3-P3` (`ISA-4.3-P3.S1`), `ISA-5.1-P1`
   (`ISA-5.1-P1.S5`)) ASSUMED. Needed sentence: "`qfree d`
   is well-formed iff the current version of every wire of d is its `qalloc`
   version or the output of a §6.4 cleanup of the value that occupied it."


# Background (not graded): `INV-4-envelope-injective.md`

# INV-4: the identity envelope is injective on structural layout leaves

Spec: ISA 0.8 (`clauses/ISA-0.8.json`). Format: `proofs/FORMAT.md`.

## Informal statement

A symbol's closure hash is SHA-256 of its semantic envelope, and part (5b) of the
envelope lists the layout leaves in the symbol's closure set, one line per leaf,
sorted by dotted path. For the hash to identify what the symbol depends on, the
(5b) block must be a function of the closure set (two conforming implementations
produce the same bytes) and an injective one (different closure sets give
different bytes). **Both properties fail in ISA 0.8**, for one family of leaves
only: `interface_regions.<oracle>.<region>`, because oracle and region names may
contain `.`, so the leaves ("a", "c.db") and ("a.c", "db") render to the same
dotted path. Below we prove both properties for every other leaf family and for
every symbol kind whose closure set cannot contain two such leaves, and record
the failure as a refuted step with the sentence 0.9 needs.

## Precise statement

DEFINE for a legal `layout` object L (`ISA-9.1-P1.S1`, `ISA-9.1-P1.S3`): `Leaves(L)` = the set of
pairs (k, v) where k = (k_1, …, k_m) is the tuple of JSON keys from the root to
a leaf at "the deepest level the schema lists" and v its value (`ISA-9.2-P2.S7`).
DEFINE `dot(k)` = k_1 "." … "." k_m. DEFINE `line(k, v)` = "layout " dot(k) " "
JCS(v) LF. DEFINE for a symbol f: `CS(f) ⊆ Leaves(L)` its closure-set leaves by
kind (`ISA-9.2-P2.S1`, `ISA-9.2-P2.S2`, `ISA-9.2-P2.S3`,
`ISA-9.2-P2.S4`, `ISA-9.2-P2.S5`, `ISA-9.2-P2.S6`), and `E5b(f)` = the concatenation of line(ℓ), ℓ ∈ CS(f),
"sorted by dotted path bytewise" (`ISA-9.2-P1.S3`).

THEOREM INV-4 (as intended). For every symbol kind K and all legal objects O,
O' defining a symbol f of kind K:
- (W) `E5b(f)` is uniquely determined by `CS(f)`;
- (I) `E5b_O(f) = E5b_O'(f)` implies `CS_O(f) = CS_O'(f)`.

THEOREM INV-4' (what holds in 0.8). (W) and (I) hold whenever dot is injective
on `CS(f)` (on `CS_O(f) ∪ CS_O'(f)` for (I)); dot is injective on every leaf
family except `interface_regions.<oracle>.<region>`; hence (W) and (I) hold for
oracle, lproc, action, permutation-action and data symbols, and fail for CC/R
symbols.

## Hypotheses

ISA-9.1-P1.S1, ISA-9.1-P1.S3, ISA-9.1-P2.S1, ISA-9.2-P1.S3, ISA-9.2-P2.S1,
ISA-9.2-P2.S2, ISA-9.2-P2.S3, ISA-9.2-P2.S4, ISA-9.2-P2.S5, ISA-9.2-P2.S6,
ISA-9.2-P2.S7, ISA-16.1-P1.S2, ISA-16.1-P1.S3, ISA-16.2-P1.S1.

## Proof

```
<1>1. line is injective on leaves: line(k, v) determines (dot(k), v).
      PROOF:
  <2>1. dot(k) contains no space and no LF: schema keys are fixed identifiers
        and every free key is a NAME, `[A-Za-z_][A-Za-z0-9_.]*`.
        BY ISA-9.1-P1.S3, ISA-16.1-P1.S2
  <2>2. JCS(v) contains no raw LF (RFC 8785 escapes control characters in
        strings and emits no insignificant whitespace); for a scalar the value
        is "its decimal text", fixed per field because "Integers that may
        exceed 2^53 are decimal strings" is a per-field rule.
        BY ISA-16.1-P1.S3, ISA-9.1-P2.S1, ISA-9.2-P2.S7
  <2>3. Hence the first space after the fixed prefix "layout " ends dot(k),
        the rest up to LF is JCS(v), and JCS is a canonical serialisation, so
        v is recovered.
        BY <2>1, <2>2, ISA-16.1-P1.S3
  <2>4. QED
        BY <2>3
<1>2. dot is injective on each leaf family except interface_regions, and
      across families.
      PROOF:
  <2>1. The families are: top-level scalars (`ptr_width`, `H`, `A_tab`,
        `S_cells`, `null_size`, `heap_base`, `heap_limit_max`, `block_image`);
        `globals.<name>`; `interface_regions.<oracle>.<region>`. "Unknown
        sections or fields are errors".
        BY ISA-9.1-P1.S1, ISA-9.1-P1.S3, ISA-9.2-P2.S7
  <2>2. Top-level scalar paths are fixed, dot-free and pairwise distinct.
        BY ISA-9.1-P1.S3
  <2>3. `globals.<name>` has one free component behind a fixed prefix, so
        dot(k) = "globals." ‖ name determines name.
        BY ISA-9.1-P1.S3, ISA-16.1-P1.S2; algebra
  <2>4. Paths of different families differ in their first component, which
        is dot-free ("globals", "interface_regions", the scalar names), so the
        prefix up to the first "." identifies the family.
        BY <2>1, <2>2
  <2>5. `interface_regions.<oracle>.<region>` has two free components, each a
        NAME that may contain ".": ("a", "c.db") and ("a.c", "db") both give
        "interface_regions.a.c.db". dot is not injective on this family.
        BY ISA-9.1-P1.S3, ISA-9.2-P2.S7, ISA-16.1-P1.S2
  <2>6. QED
        BY <2>2, <2>3, <2>4, <2>5
<1>3. If dot is injective on CS(f), then (W) and (I) hold.
      PROOF:
  <2>1. Sorting by an injective key is a total order on CS(f), so E5b(f) is
        unique.
        BY ISA-9.2-P1.S3; algebra
  <2>2. E5b(f) splits at LF into lines; by <1>1 each line gives (dot(k), v);
        by injectivity of dot it gives k; hence CS(f).
        BY <1>1, <2>1; algebra
  <2>3. QED
        BY <2>1, <2>2
<1>4. dot is injective on CS(f) for f an oracle, lproc, action, permutation
      action or data symbol.
      PROOF:
  <2>1. Oracle: the closure set has all layout leaves "except
        `interface_regions` entries of other oracles", plus "its own
        `interface_regions.<oracle>.*` leaves"; all interface-region leaves in
        it share the first free component (the oracle), so only the region
        component is free.
        BY ISA-9.2-P2.S2, <1>2
  <2>2. "Its own" and "other oracles" are decided on the structural key
        k_2 = the oracle's name, not on a prefix of the rendered path.
        ASSUMED: `ISA-9.2-P2.S2` writes the selection as the path pattern
        `interface_regions.<oracle>.*`; on rendered paths, oracle "a" would
        capture the leaves of oracle "a.b" (council SOL-R11-B02, R11-B02).
  <2>3. Lproc: only `globals.<g>` leaves (and images); action, permutation
        action, data: no layout leaves.
        BY ISA-9.2-P2.S3, ISA-9.2-P2.S4, ISA-9.2-P2.S6, <1>2
  <2>4. QED
        BY <2>1, <2>2, <2>3, <1>2
<1>5. For CC and R functions, (W) and (I) fail.
      PROOF:
  <2>1. A CC/R closure set has "all `layout` leaves", so it contains every
        interface-region leaf of every oracle.
        BY ISA-9.2-P2.S5
  <2>2. (W) fails: an object with oracle "a" (region "c.db", base 32) and
        oracle "a.c" (region "db", base 48) is legal and gives a CC function
        two lines with the same dotted path; "sorted by dotted path bytewise"
        does not order them, so two envelopes (and closure hashes) conform.
        OPEN (refuted): `ISA-9.2-P1.S3` (5b) gives no tie order; council
        SOL-R12-B01, R12-B01; SPEC-QUESTIONS 31.
  <2>3. (I) fails even with any tie order: object O1 with oracle "a", region
        "c.db" and object O2 with oracle "a.c", region "db", both base 32, give
        a reference-free CC function with identical text identical (5b) lines,
        hence identical envelopes, while CS_O1 ≠ CS_O2. With a value-based tie
        order (sorting whole lines), O1 = {a/c.db: 32, a.c/db: 48} and
        O2 = {a/c.db: 48, a.c/db: 32} collide too.
        OPEN (refuted): the tie-break of SPEC-QUESTIONS 31 (by original key
        components) repairs (W) but not (I), because the line does not carry
        the components.
  <2>4. Whether a CC function's behaviour can depend on the lost distinction
        (it can address an interface region's `base` in classical memory
        without naming the oracle) is not decided here.
        OPEN: harm assessment; part (6) separates the two only when the
        function references the oracles.
  <2>5. QED
        BY <2>2, <2>3
<1>6. QED
      BY <1>3, <1>4 for INV-4' on the listed kinds; <1>5 refutes INV-4 for
      CC/R.
```

Not covered: injectivity of the whole envelope (parts (1)–(6) as one byte
string). It needs a grammar argument over `ISA-16.2-P1.S1` that no canonical function
line has the form of a (5a)/(5b)/(5c) line or of a 64-hex part-(6) line, so that
the part boundaries are recoverable. OPEN; listed as gap 4.

## Witnesses

| Witness | Steps |
|---|---|
| `suite/cases/sum_db`, `heap` (one oracle, one interface region, globals: non-colliding leaves; pinned closure hashes) | 1.3, 1.4 |
| `suite/cases/control_flow`, `classical`, `tiny_memory`, `wide`, `mutual` (CC/R and oracle symbols with layout leaves, no collisions) | 1.3 |
| `tests/identity.rs`: `r11_oracle_layout_ownership_uses_exact_names`, `r11_dotted_oracle_layout_ownership`, `r11_dotted_owner_and_region_family`; `tests/cli_xam.rs::r11_cli_exact_oracle_layout_owners` | 1.4.2 (ASSUMED) |
| `tests/identity.rs`: `r12_cc_r_colliding_dotted_leaves`, `r12_cc_r_layout_paths_preserve_colliding_leaves`, `r12_dotted_leaf_collision_family` | 1.5.2 (pins the SPEC-QUESTIONS 31 tie order) |
| `tests/identity.rs::r12_dotted_global_lproc_keeps_exact_closure_selection` | 1.2.3, 1.4.3 |

No existing witness exercises 1.5.3 (cross-object collision): every current test
compares envelopes within one object.

## Council blockers as instances

- SOL-R11-B02, R11-B02 (oracle "a" owns the leaves of oracle "a.b" by rendered
  prefix): violation of 1.4.2; the selection must be structural.
- SOL-R12-B01, R12-B01 (CC/R envelope coalesces `interface_regions["a"]["c.db"]`
  and `interface_regions["a.c"]["db"]` into one map key, dropping a leaf): an
  implementation choosing a lossy representation because 1.2.5 makes the
  rendered path a non-key; the spec-level failure is 1.5.2.

## Spec gaps

1. (1.4.2, next to `ISA-9.2-P2` (`ISA-9.2-P2.S2`)) ASSUMED. Needed sentence: "An oracle's own
   interface-region leaves, and the interface-region entries of other oracles,
   are selected by the exact JSON key under `interface_regions`, never by a
   prefix of the dotted path."
2. (1.5.2, next to `ISA-9.2-P1` (`ISA-9.2-P1.S3`) part (5b)) OPEN (refuted). Needed sentence
   (SPEC-QUESTIONS 31, sol's wording): "Emit one line for every structured layout
   leaf, including leaves with coincident dotted renderings. Sort by the rendered
   dotted path bytewise; break ties bytewise by the sequence of original JSON
   key components."
3. (1.5.3, next to `ISA-9.2-P1` (`ISA-9.2-P1.S3`) part (5b) and
   `ISA-16.1-P1` (`ISA-16.1-P1.S2`)) OPEN (refuted); gap 2
   does not close it. Needed sentence, one of: (a) "The path of a layout leaf is
   rendered as the JCS array of its key components, e.g. `layout
   ["interface_regions","a","c.db"] {"base":32}`"; or (b) "Oracle names and
   region names that appear as keys of `layout.interface_regions` MUST NOT
   contain `.`" (a narrowing of NAME, to be checked against the dialect's name
   mangling before choosing it).
4. (whole envelope, next to `ISA-9.2-P1` (`ISA-9.2-P1.S3`)) OPEN. Needed: either a lemma that
   canonical function lines (`ISA-16.2`, `ISA-16.2-P1.S1`) never begin with `data `, `layout `,
   `device ` and are never 64 hex digits, or a length prefix per part.
5. (1.5.4, next to `ISA-9.2-P2` (`ISA-9.2-P2.S5`)) OPEN. Not a missing sentence but an unfinished
   analysis: whether a CC/R function's semantics can depend on an interface
   region's `base` without a part-(6) reference to the oracle. Gap 3 makes the
   question moot.


# Background (not graded): `INV-5-schedule-selection.md`

# INV-5: schedule selection is sound, admission is exact, defaults are values

Spec: ISA 0.8 (`clauses/ISA-0.8.json`). Format: `proofs/FORMAT.md`.

## Informal statement

A schedule (§11) is a list of entries. Each entry selects generated operations
by `path`, `step`, `phase`, `iteration` and `generated`, and makes one decision of
one `kind`. Among the entries that match an operation, the most specific one
applies. Two maximal matches make the schedule invalid, and document order
never matters. Fields the schedule leaves out take their §11 / §17 defaults.
For a consumer this gives three properties:

- (A) **Selection soundness.** In an admitted schedule, each concrete operation
  has at most one maximal matching entry per kind. Here the `step` of an
  operation inside a nested oracle invocation ranges over that invocation's
  own budget, not the enclosing one.
- (B) **Admission exactness.** Admission rejects a schedule (on matching
  grounds) iff some operation that is generated under the declared budgets
  has two or more maximal matching entries of one kind. So shadowed ties are
  admitted, genuine ties are rejected, and document order plays no part.
- (C) **Defaults.** An omitted field with a §17 default is matched and resolved
  exactly as if the default had been written.

Council rounds 15 to 18 on the reference interpreter each found a violation of
one of these properties (see "Council blockers as instances"). The proof shows
which parts hold in 0.8, under which readings, and where the text is silent or
false:

- (A) and (B) hold once three readings are fixed: what a `lift.call` contributes
  to a chain, which invocation level a `step` reads, and what "incomparable"
  means. They also need the consumer to know the nested token budgets.
- (B) is false for any admission that sees only the object and the schedule
  (`params_hash`). Such an admission cannot know the nested step domains.
- (C) holds for `expansion` (except that the hash of `ref` is unstated) and for
  `sampler.count`. It is false as written for `epsilon_share`, whose default is
  in general no finite decimal. It is also false for the defaults of uncovered
  operations, which the selector language cannot always write down.

## Precise statement

Fix a well-formed object O, a schedule S with `bindings.region` = R,
`bindings.budget` = [B_0, heap, stack, depth] (`ISA-11-P3.S2`), and the
classical arguments of the run, of which S records only `params_hash`
(`ISA-9.2-P2.S13`). Let β be the map from each token argument to the budget it
was issued with (`ISA-10-P7.S2`, `bennett_budget`).

DEFINE an **invocation** as the root invocation of R, or an invocation created
by a region call (`oracle_call`, `action_call`, `ISA-4.7-P1.S1`) or a
`lift.oracle_call` (`ISA-4.2-P21.S1`) inside another invocation. An **oracle
invocation** ι runs B_ι forward steps and B_ι inverse steps
(`ISA-5.2-P3.S1.2`, `ISA-5.2-P3.S1.4`). B_root = B_0. For a nested oracle
invocation, B_ι = β(tk), where tk is the call's token.

DEFINE a **concrete operation** o = (c, τ, φ, g):
- c = (e_1, …, e_m) is its invocation chain (`ISA-11-P4.S1`). Each
  e_j = (sym_j, pt_j, it_j), where it_j is the vector of 0-based qloop
  repetition counts at pt_j (`ISA-11-P4.S2`).
- τ maps each oracle invocation level ℓ on the chain to the forward machine
  step τ(ℓ) ∈ 1..B_ℓ during which o is generated.
- φ maps the same levels to `fwd` or `rev`.
- g is o's ordinal within the expansion of the row at pt_m in the bound
  library (`ISA-11-P4.S3`).

Ω(O, S, β) is the set of concrete operations of the root invocation.

DEFINE an **entry** e = (P, s, h, γ, k, payload): P is its `path`, s its
`step`, h its `phase`, γ its `generated` and k its `kind`. Let lv(P) be the
invocation level whose step and phase the entry reads (step 1.1.8). Then
`match(e, o)` holds iff all four conditions hold (`ISA-11-P4.S2`,
`ISA-11-P4.S3`, `ISA-11-P4.S4`):
- P is an element-wise prefix of c;
- s = `*` or s = τ(lv(P));
- h = `*` or h = φ(lv(P));
- γ = `*` or γ = g.

DEFINE κ(e) ∈ ℕ^5 as the specificity tuple, ordered lexicographically.
DEFINE M_k(o) = {e ∈ S of kind k : match(e, o)} and Max_k(o) = {e ∈ M_k(o) :
κ(e) = max κ[M_k(o)]}. Entries are counted by array position.
DEFINE `Tie(S, β)` ⟺ ∃ o ∈ Ω(O, S, β), ∃ k : |Max_k(o)| ≥ 2.

THEOREM INV-5 (as intended). For every well-formed O and every S that passes
every non-matching admission check:
- (A) if S is admitted, then |Max_k(o)| ≤ 1 for all o ∈ Ω(O, S, β) and all k.
  The step coordinate τ(ℓ) of o ranges over 1..B_ℓ for its own level ℓ.
- (B) admission rejects S iff Tie(S, β). The decision depends only on the
  multiset of entries.
- (C) for every field f with a §17 default d_f, the schedule S_f that omits f
  and the schedule S[f := d_f] that writes it have the same Ω, the same
  `match` and the same resolved decision for every o and k.

THEOREM INV-5' (what holds in 0.8).
- (A) and (B) hold for **bound admission**, where the consumer knows β. They
  need the readings 1.1.4 (lift.call contributes no chain element), 1.1.7
  (step and phase on action-level operations), 1.1.8 (step level) and 1.2.2
  (equal maximal tuple), and they cover only operations generated by rows
  (1.1.6). Cleanup-kind entries are also open (1.2.4).
- (B) fails for **unbound admission**, which sees only O and S (1.4.3).
- (C) holds for `bindings.expansion` (up to the unstated hash of `ref`, 1.6.3.3)
  and for `sampler.count`. It is refuted for `epsilon_share` taken as a written
  decimal (1.6.4.3) and for uncovered-operation defaults taken as written
  entries (1.6.7).

## Hypotheses

ISA-3.2-P10.S1, ISA-3.6-P1.S1, ISA-3.6-P4.S1, ISA-3.6-P6.S1, ISA-3.6-P11.S1,
ISA-3.7-P20.S2, ISA-4.2-P1.S2, ISA-4.2-P21.S1, ISA-4.6-P8.S1, ISA-4.6-P9.S1,
ISA-4.7-P1.S1, ISA-5.1-P1.S7, ISA-5.2-P1.S1, ISA-5.2-P2.S2, ISA-5.2-P3.S1.2,
ISA-5.2-P3.S1.4, ISA-5.4-P1.S3, ISA-8.1-P1.S1, ISA-8.1-P10.S1, ISA-8.1-P10.S2,
ISA-9.2-P2.S13, ISA-10-P1.S4, ISA-10-P4.S1, ISA-10-P7.S2, ISA-11-P2.S1,
ISA-11-P2.S2, ISA-11-P2.S3, ISA-11-P3.S2, ISA-11-P4.S1, ISA-11-P4.S2,
ISA-11-P4.S3, ISA-11-P4.S4, ISA-11-P4.S5, ISA-11-P4.S6,
ISA-11-P4.S9, ISA-12.1-P2.S1, ISA-17-P7.S2, ISA-17-P8.S2, ISA-17-P10.S1,
ISA-17-P10.S2, ISA-17-P11.S1, ISA-17-P14.S2.

## Proof

```
<1>1. Ω(O, S, β) is a finite set determined by O, the bindings of S and β,
      and match(e, o) is a function of (e, o).
      PROOF:
  <2>1. Every generated operation has an invocation chain, outermost first,
        "ending in its own point"; `path` matches iff it is an element-wise
        prefix, `iteration` being `*` or the exact repetition vector.
        BY ISA-11-P4.S1, ISA-11-P4.S2
  <2>2. A `lift.call` creates no new step machine: lproc rows are rows of the
        calling oracle's index space I, every forward step runs every row of
        I under its dispatch predicate, and "callee rows are charged to the
        caller's budget".
        BY ISA-3.6-P1.S1, ISA-3.6-P6.S1, ISA-3.7-P20.S2, ISA-4.2-P1.S2
  <2>3. The literal chain is not a function of the generated operation for
        rows reached through `lift.call`. Counterexample: oracle @o has
        `lift.call @f` rows at p1 and p2 on the two arms of an input branch,
        and @f has a gate-generating row q. At step t the circuit holds one
        expansion of q under at_q (<2>2). For inputs routed through p1 its
        chain is [(o,p1),(f,q)]; for inputs routed through p2 it is
        [(o,p2),(f,q)]. Under recursion the chain also grows with the dynamic
        depth. Two equal-specificity gate entries on [(o,p1),(f,q)] and
        [(o,p2),(f,q)] that choose different realisations each match one
        "chain" of the same gate. No per-operation choice satisfies both.
        OPEN (refuted): `ISA-11-P4.S1` puts "the `lift.call`s that led to it"
        into the chain of an operation the step machine generates
        independently of any call.
  <2>4. Reading adopted: the chain contains the points of region calls and
        `lift.oracle_call`s, and then the operation's own row point. A row of
        an lproc in an oracle's closure is one generated operation per step,
        whichever `lift.call` led to it.
        ASSUMED: the only reading under which the chain is static (<2>3); the
        interpreter's chain domains behave this way (README "Design (schedule
        matching)").
  <2>5. Each oracle invocation ι has a step domain 1..B_ι of its own:
        B_root = B_0, and a nested invocation's budget is that of its token.
        PROOF:
    <3>1. The root runs exactly B_0 forward steps (t = 1..B_0) and the inverse
          steps t = B_0..1, with B_0 = `bindings.budget[0]`.
          BY ISA-11-P3.S2, ISA-5.4-P1.S3, ISA-3.6-P4.S1, ISA-5.2-P3.S1.2,
             ISA-5.2-P3.S1.4, ISA-3.6-P11.S1
    <3>2. `lift.oracle_call @o tk …` applies the callee contract F_B. B is the
          budget of the token tk, which `bennett_budget(program, region,
          steps, …)` issued for that region. Tokens are program-scoped
          classical values.
          BY ISA-4.2-P21.S1, ISA-5.2-P2.S2, ISA-10-P7.S2, ISA-10-P1.S4,
             ISA-3.2-P10.S1
    <3>3. `step` and `phase` are "per invocation level, so a nested oracle's
          step is selected by a path element for the nested call". The step
          coordinate of an operation at nested level ℓ therefore ranges over
          1..B_ℓ = 1..β(tk), and B_ℓ is not bounded by B_0. Example (council
          R18): B_0 = 2, β(tk) = 3. The nested `lift.retval` row of @inc8
          runs at nested step 3, which exists although 3 > B_0.
          BY ISA-11-P4.S3, <3>1, <3>2
    <3>4. QED
          BY <3>1, <3>2, <3>3
  <2>6. Operations generated by a step but by no row have no "own point" and
        no row ordinal: dispatch comparators, successor XORs, commit of pc,
        clean dispatch. Construction allocation, commit and release also lie
        outside every step t ∈ 1..B.
        OPEN: `ISA-11-P2.S2` lists them as generated operations, but
        `ISA-11-P4.S1` and `ISA-11-P4.S3` define the chain end and
        `generated` only for a row's expansion. No entry can select them
        with certainty, so it is unknown which defaults or entries govern
        them.
  <2>7. An operation at action level (no enclosing oracle invocation) has
        no step and no phase. Only `step: "*"` and `phase: "*"` match it.
        ASSUMED: `ISA-11-P4.S3` defines `step` only "of an oracle-generated
        operation" and does not say how a concrete `step`/`phase` treats
        other operations. The `adj` of an action call is not a `rev` phase.
  <2>8. Reading adopted for the level an entry's `step` and `phase` read:
        lv(P) is the oracle invocation entered by the last oracle-call
        element of P, or the root if P has none. A nested step is therefore
        selected exactly when the path contains the nested call. Two other
        readings fit the text: (R1) the level that owns P's last point,
        which differs only when P ends at a call point; and (R2) the
        operation's own innermost level, under which `path: []`,
        `step: 3` selects nested step 3 everywhere. All three agree on the
        R18 witness.
        ASSUMED: `ISA-11-P4.S3` says "per invocation level" but gives an
        entry one `step` and does not say which level it reads.
  <2>9. Ω is finite: oracle and action call graphs are acyclic (recursion
        only through `lift.call`, which adds no element by <2>4), qloop trip
        counts are literals, every level has finitely many steps (<2>5), and
        each row has finitely many ordinals in the bound library.
        BY ISA-5.1-P1.S7, ISA-4.6-P8.S1, ISA-4.6-P9.S1, ISA-11-P2.S3, <2>4,
           <2>5
  <2>10. QED
        BY <2>1, <2>4, <2>5, <2>8, <2>9
<1>2. For each kind, the maximal set Max_k(o) is well defined and depends
      only on the multiset of entries.
      PROOF:
  <2>1. Specificity is "the lexicographic tuple (path length, number of
        non-`*` iterations, step non-`*`, phase non-`*`, generated non-`*`)".
        Lexicographic order on ℕ^5 is total, so the maximal tuple of a
        nonempty finite M_k(o) exists and is unique.
        BY ISA-11-P4.S4; algebra
  <2>2. "Two incomparable maximal matching entries" means two distinct
        entries (array positions) with equal maximal tuple. Exact duplicates
        count as such a pair.
        ASSUMED: under the stated total order no two distinct tuples are
        incomparable, so the word "incomparable" is either void or alludes to
        the product order. Under the product order, (2,0,0,0,0) and
        (1,1,1,1,1) would both be maximal and invalidate the schedule, while
        the lexicographic order selects the first.
  <2>3. "Selectors are resolved independently per `kind`": entries of
        different kinds never tie with, nor shadow, each other.
        BY ISA-11-P4.S5
  <2>4. Which operations an entry of each kind can match: `gate` matches gate
        operations, `alloc` allocations, `start` every operation; `cleanup`
        is open.
        PROOF:
    <3>1. `gate`, `alloc`, `start`: a kind is matched only against
          operations for which it makes a decision.
          ASSUMED: `ISA-11-P4.S4` matches by selectors alone and never
          relates `kind` to the operation's class (`ISA-11-P2.S1`: gates,
          allocations, releases).
    <3>2. `cleanup`: a cleanup is a sequence of operations with one
          realisation (`reverse` or `recompute`). Per-operation selection
          can give operations of one cleanup different realisations, and
          the spec names no operation that carries the cleanup's identity.
          OPEN: which generated operation(s) a `cleanup` entry is matched
          against.
    <3>3. QED
          BY <3>1, <3>2
  <2>5. Document order: M_k(o) and Max_k(o) are defined by membership and κ,
        so they are invariant under every permutation of `entries`; "document
        order is never significant".
        BY ISA-11-P4.S4; algebra
  <2>6. QED
        BY <2>1, <2>2, <2>3, <2>5
<1>3. S is invalid on matching grounds iff Tie(S, β). The quantifier ranges
      over Ω(O, S, β), the operations generated under the declared budgets,
      not over all budgets.
      PROOF:
  <2>1. The schedule is invalid iff some generated operation has two
        maximal matching entries of one kind.
        BY ISA-11-P4.S4, ISA-11-P4.S5, <1>2
  <2>2. Operations beyond a level's budget are not generated: "B is enforced
        by running exactly B steps". An entry whose selectors meet only such
        operations is dead and creates no tie.
        BY ISA-5.4-P1.S3, <1>1
  <2>3. QED
        BY <2>1, <2>2
<1>4. (B) Admission exactness.
      PROOF:
  <2>1. A consumer must reject an invalid schedule before executing it: it
        "validates every binding and every path against the object and
        executes verbatim or rejects".
        ASSUMED: `ISA-11-P4.S9` does not list the maximal-match condition
        among the checks it names, nor fix when it is checked. We read
        "executes verbatim" as excluding any execution that has already
        begun when a tie is first met.
  <2>2. Bound admission (β known) decides Tie(S, β) exactly.
        PROOF:
    <3>1. Shadowed ties are admitted. Let A and B tie at κ and let every
          o ∈ match(A) ∩ match(B) ∩ Ω be matched by some C_o of the same kind
          with κ(C_o) > κ (one C or a union). Then A, B ∉ Max_k(o) for every
          such o, so A and B contribute no tie.
          BY <1>2.1, <1>3; algebra
    <3>2. Genuine ties are rejected. If some o ∈ match(A) ∩ match(B) ∩ Ω has
          no matching entry of its kind above κ, then {A, B} ⊆ Max_k(o) and
          Tie(S, β) holds.
          BY <1>2.1, <1>2.2, <1>3
    <3>3. A pairwise criterion ("reject iff two equal-κ entries of one kind
          have overlapping selector boxes") rejects every shadowed tie in
          <3>1, so it is sound but not complete.
          BY <3>1; algebra
    <3>4. The step coordinate must use each level's own domain (<1>1.5.3).
          Using B_0 for a nested level ℓ removes the operations with
          B_0 < τ(ℓ) ≤ B_ℓ, so ties there are admitted. It adds dead
          operations with B_ℓ < τ(ℓ) ≤ B_0, so schedules valid for the actual
          budget are rejected.
          BY <1>1.5.3, <1>3; algebra
    <3>5. Since Ω is finite and match is a function (<1>1), enumerating
          Ω × S × S, or intersecting and subtracting the selector boxes over
          each level's domain, decides Tie(S, β). The result depends only on
          the multiset of entries.
          BY <1>1, <1>2.5, <1>3; algebra
    <3>6. QED
          BY <3>1, <3>2, <3>5
  <2>3. Unbound admission, which sees only O and S, cannot decide Tie. Ω
        depends on β through the nested step domains (<1>1.5.3). S records
        only `params_hash`, "SHA-256 of the JCS array of classical parameter
        values", and a token's interchange value is "the 8-byte little-endian
        id", which carries no budget. The R18 schedule (two equal gate
        entries on nested step 3) is invalid with β(tk) = 3 and valid with
        β(tk) = 2, under the same object and bindings. If a token's JCS value
        is its id, the `params_hash` is the same too. So every procedure that
        reads only (O, S) fails (B) for one of the two runs: root-B clipping
        admits the first (R18-B01), and a symbolic "some budget" check
        rejects the second.
        OPEN (refuted for unbound admission): `ISA-11-P4.S9` and
        `ISA-9.2-P2.S13` do not say whether the matching check may be
        deferred until β is known, nor what JCS value a `token` parameter
        has in `params_hash`. Uses `ISA-10-P4.S1`.
  <2>4. QED
        BY <2>1, <2>2 for bound admission; <2>3 refutes (B) for unbound
        admission.
<1>5. (A) Selection soundness, for bound admission.
      PROOF:
  <2>1. Admitted implies ¬Tie(S, β).
        BY <1>4.2
  <2>2. Hence for every o ∈ Ω and kind k, |Max_k(o)| ≤ 1. Every τ(ℓ) is
        taken over 1..B_ℓ of its own level.
        BY <2>1, <1>3, <1>1.5
  <2>3. The decision for (o, k) is "the unique maximal one" if M_k(o) ≠ ∅,
        and the §11 default for uncovered operations otherwise. Both are
        independent of document order.
        BY ISA-11-P4.S4, ISA-11-P4.S6, <1>2.5
  <2>4. QED
        BY <2>2, <2>3
<1>6. (C) Defaults.
      PROOF:
  <2>1. Matching reads only `path`, `step`, `phase`, `generated` and `kind`,
        and Ω reads only the bindings (region, budget, expansion) and β.
        Omitting a payload field (`realisation`, `epsilon_share`, `class`,
        `time`) therefore changes neither Ω, `match`, Max_k nor Tie.
        BY ISA-11-P4.S2, ISA-11-P4.S3, ISA-11-P4.S4, <1>1; algebra
  <2>2. Defaults act per entry: if the applying maximal entry omits a field
        with a default, the default applies. The field is not inherited from
        a less specific matching entry.
        ASSUMED: `ISA-11-P4.S4` says "the unique maximal one applies" and
        does not say whether fields merge across matching entries. Under
        field-wise merging, omission would not equal writing the default.
  <2>3. `bindings.expansion` omitted.
        PROOF:
    <3>1. "A schedule that names no `expansion` binds `ref` at the ISA's own
          version". The ordinals that `generated` selects, and with them Ω
          and `match`, are those of `ref`, exactly as for a written binding
          to `ref`.
          BY ISA-17-P8.S2, ISA-11-P2.S3, ISA-11-P4.S3, <2>1
    <3>2. "The ISA's own version" is the version in the object's header,
          not the consumer's.
          ASSUMED: `ISA-17-P8.S2` does not say whose version is meant.
    <3>3. The written equivalent `{ "name": "ref", "version": "0.8",
          "hash": H }` needs H, and the spec states no hash for `ref`.
          OPEN: `ISA-11-P2.S3`, `ISA-17-P8.S2` give no hash for the default
          binding, so "as if written" names an undetermined triple.
    <3>4. QED
          BY <3>1, <3>2 for matching and resolution; <3>3 for the written
          form.
  <2>4. `gate.epsilon_share` omitted.
        PROOF:
    <3>1. When a schedule assigns no share, eps = the region's `epsilon`
          divided equally among its ε > 0 operations.
          BY ISA-17-P10.S1, ISA-17-P10.S2, ISA-8.1-P10.S1
    <3>2. Whether an operation is "ε > 0" depends on the `gates` entry it
          matches, and that match depends on eps ("a `gates` entry whose
          `epsilon` … > `eps` does not match"). The count N in the default is
          therefore defined through the default itself.
          OPEN: `ISA-8.1-P10.S1`, `ISA-8.1-P10.S2`, `ISA-17-P10.S2` give no
          eps-independent definition of an ε > 0 operation, nor say which
          region's `epsilon` and which invocations' operations are meant
          when nested regions exist.
    <3>3. ε / N is in general no finite decimal (`epsilon` "0.1", N = 3
          gives 0.0333…). No written schedule carries it, so "exactly as if
          the default were written" is false. What holds is "as if the
          rational ε / N had been assigned".
          OPEN (refuted): `ISA-17-P10.S2` (with `ISA-11-P3.S2`, a share is a
          decimal) has no written equivalent.
    <3>4. An entry that sets `gate.realisation` and omits `epsilon_share`
          "assigns none", like an operation with no gate entry at all.
          BY ISA-17-P10.S1, <2>1, <2>2
    <3>5. QED
          BY <3>1, <3>4; <3>2 and <3>3 bound what "as if written" can mean.
  <2>5. A written decimal is used by its value: `epsilon` 0, "0", "0.0" and
        "0.000" all satisfy "exact-permutation only (ε = 0 everywhere)".
        Decimals are also compared and divided by value (<2>4.1).
        ASSUMED: §11 never says that a schedule decimal denotes the exact
        rational of its text. `ISA-8.1-P1.S1` says so only for targets
        ("numbers are exact rationals from their decimal text"). Uses
        `ISA-5.2-P1.S1`.
  <2>6. Uncovered operations (M_k(o) = ∅) resolve by rule: cleanup
        `reverse` (§17 item 6); gate `native` if a `gates` entry matches,
        else the first matching scheme; class = the first class in JCS
        order with capacity (§17 item 10); sequential timing. Each rule
        reads only o and the target, never another kind's entries or
        document order.
        BY ISA-11-P4.S6, ISA-17-P7.S2, ISA-17-P11.S1, <1>2.3, <1>2.5
  <2>7. An uncovered default cannot always be written as an entry without
        changing other operations. Take root R with a `lift.oracle_call` row
        r into @g, whose row q generates gate operations. Let E be a gate
        entry with `path` [] and `step` 1 (root level, <1>1.8) and scheme X.
        The gate o of q at root step 2 and nested step 1 is uncovered. Any
        entry that matches o has `path` at least [(R,r)] and can constrain
        only the nested step. It therefore also matches o', the same gate at
        root step 1, and outranks E there (path length is the first
        component of κ). Writing the default for o moves o' from X to
        `native`.
        OPEN (refuted): defaults of uncovered operations are not "as if
        written". This limits (C), not 0.8: `ISA-11-P4.S6` states them as
        rules. The cause is that an entry has one `step` for a chain with
        several levels (`ISA-11-P4.S3`).
  <2>8. `sampler.count` omitted (§17 item 13, the certificate analogue):
        2^16 = 65536 is an integer the claim can carry, so omission and the
        written value replay identically.
        BY ISA-17-P14.S2, ISA-12.1-P2.S1; algebra
  <2>9. QED
        BY <2>1, <2>2, <2>3, <2>4, <2>5, <2>6, <2>8; <2>4.3 and <2>7 refute
        the written form for item 9 and for uncovered operations.
<1>7. QED
      BY <1>5 for (A); <1>4 for (B) (bound admission; refuted unbound,
      1.4.3); <1>6 for (C) (refuted for item 9 as a written value, 1.6.4.3).
```

## Witnesses

Interpreter tests are in `bennett-isa-spec-review/reference-interpreter` at
`be9e6d1`. They are evidence, not justification.

| Witness | Steps |
|---|---|
| `tests/metadata.rs::schedule_requires_typed_bindings_selectors_and_unique_maxima`, `::schedule_paths_bind_real_program_points_and_loop_depths` | 1.1.1, 1.1.9, 1.3 |
| `tests/metadata.rs::r15_oracle_schedule_epsilon_uses_exact_decimal_value`; `tests/cli_xam.rs::r15_cli_oracle_schedule_epsilon_is_exact_by_value` (0, "0", "0.0", "0.000" admit; "0.1" rejects) | 1.6.5 |
| `tests/metadata.rs::r16_default_expansion_preserves_witness_and_identity`, `::r16_present_expansion_still_requires_closed_descriptor`, `::r16_schedule_consumer_resolves_default_and_preserves_explicit_binding`; `tests/cli_xam.rs::r16_cli_default_expansion_check_hash_preserves_pins`, `::r16_cli_malformed_present_expansion_rejects` | 1.6.3.1, 1.6.3.2 (resolves `ref` at the object's 0.8, supplies no hash: 1.6.3.3) |
| `tests/metadata.rs::r17_default_share_and_shadowed_witness_preserve_identity`, `::r17_present_gate_share_and_missing_realisation_reject`, `::r17_equal_share_consumer_keeps_exact_and_explicit_assignments`; `tests/cli_xam.rs::r17_cli_default_share_and_shadowed_tie_check_hash_pins`, `::r17_cli_malformed_gate_share_rejects` | 1.6.1, 1.6.4.1, 1.6.4.4 (the consumer keeps ε / N symbolic: consistent with 1.6.4.3) |
| `tests/metadata.rs::r17_shadowed_tie_all_orders_and_genuine_maximum_ties` (A/B/C in six orders; A/B alone and duplicate C reject) | 1.2.2 (duplicates), 1.2.5, 1.4.2.1, 1.4.2.2 |
| `tests/metadata.rs::r17_specificity_lattice_family_matches_brute_force` (1,200 schedules, 54 partitions each) | 1.2.1, 1.4.2.5 |
| `tests/metadata.rs::r17_union_coverage_partial_coverage_and_budget_domains`, `::r17_loop_iteration_union_and_empty_domains` | 1.4.2.1 (union cover), 1.3.2 (out-of-budget, zero-trip), 1.1.9 |
| `src/metadata_schema/tests.rs::r17_section17_defaults_are_optional_and_applied`; `tests/r1_certificates.rs::r17_sample_count_default_replays_and_present_values_validate` | 1.6.2, 1.6.8 |
| Council files `bennett-isa-spec-review/.tmp/r18-nested-budget-2.bisa` (root B = 2, token B = 3, two equal gate entries on nested step 3: admitted at `be9e6d1`, should reject) and `r18-nested-budget-3.bisa` (root B = 3 control: rejects) | 1.1.5.3, 1.4.2.4; counter-witness until an R18 test lands |

No test exists yet for 1.1.3 (two `lift.call` sites), 1.1.8 (the readings
differ on `path: []` with a concrete `step` over a nested operation), 1.4.3
(the same schedule under two token budgets) or 1.6.7. The interpreter's
`resolve_schedule` takes an operation with a single `step` and `phase`. It
cannot represent the per-level vector τ of a nested operation, so reading
1.1.8 is implicit in its domain code rather than in its interface.

## Council blockers as instances

- **R15-B02** (bindings `epsilon` "0.0" rejected as non-exact): violates
  1.6.5. Admission used the spelling instead of the value, so a written zero
  was not the value zero. The determining text is `ISA-5.2-P1.S1`. The
  value reading is ASSUMED because §11 has no decimal-value sentence.
- **R16-B01** (omitted `bindings.expansion` rejected): violates 1.6.3.1. The
  omitted field was treated as missing instead of as the default binding to
  `ref`.
- **R17-B01** (omitted `gate.epsilon_share` rejected in a realisation-only
  entry): violates 1.6.4.4, and through it 1.6.1. A payload omission changed
  the admission outcome.
- **R17-B02** (pairwise rejection of the shadowed A/B tie under C): violates
  1.4.2.1, and with it the "only if" half of (B). The implementation used
  the criterion of 1.4.2.3 instead of the per-operation quantifier of 1.3.
- **R18-B01** (nested step 3 > root B = 2, tie admitted): violates 1.1.5.3,
  and through 1.4.2.4 the "if" half of (B) and (A) (1.5.2). The step domain
  was taken from the root budget instead of the nested token. The fix the
  council asks for (a symbolic nested range when β is unknown) runs into
  1.4.3: without β no procedure is exact, and the symbolic one over-rejects.

## Spec gaps

1. (1.1.3 OPEN (refuted), 1.1.4 ASSUMED, next to `ISA-11-P4` (`ISA-11-P4.S1`)). Needed
   sentence: "The invocation chain contains the program points of region calls
   and `lift.oracle_call`s, then the operation's own point. `lift.call` adds
   no element: a row of an lproc in an oracle's closure generates one
   operation per step, whichever call led to it."
2. (1.1.5.2, next to `ISA-4.2-P21` (`ISA-4.2-P21.S1`) and `ISA-5.2-P2.S2`)
   implicit. The steps B of a `lift.oracle_call` callee are those of its
   token, as issued by `bennett_budget`. This is stated only through the C
   signature (`ISA-10-P7.S2`). Suggested sentence: "A nested oracle call runs
   its callee with the budget of its token."
3. (1.1.6, next to `ISA-11-P4` (`ISA-11-P4.S1`, `ISA-11-P4.S3`)) OPEN.
   Needed: a point, step and ordinal for every generated operation that no
   row generates. For example: "Dispatch, successor, pc-commit and
   clean-dispatch operations of step t carry the chain of their oracle
   invocation, step t and ordinals assigned by the expansion library under a
   pseudo-point `step`. Construction, commit and release carry the pseudo
   points `alloc`, `commit`, `release` and match only `step: "*"`."
4. (1.1.7, next to `ISA-11-P4` (`ISA-11-P4.S3`)) ASSUMED. Needed sentence: "An
   operation not generated by an oracle step matches only `step: "*"` and
   `phase: "*"`."
5. (1.1.8, next to `ISA-11-P4` (`ISA-11-P4.S3`)) ASSUMED. Needed sentence:
   "An entry's `step` and `phase` refer to the oracle invocation entered by
   the last oracle-call element of its `path`, or to the root invocation if
   there is none." A 0.9 alternative that also closes 1.6.7: move `step` and
   `phase` into the path elements, so that each level carries its own.
6. (1.2.2, next to `ISA-11-P4` (`ISA-11-P4.S4`)) ASSUMED. Needed: replace "two
   incomparable maximal matching entries" with "two matching entries of equal
   maximal specificity (distinct array elements, even if identical)".
7. (1.2.4.1, next to `ISA-11-P4` (`ISA-11-P4.S4`, `ISA-11-P4.S5`)) ASSUMED.
   Needed sentence: "An entry of kind `gate` is matched only against gate
   operations, `alloc` only against allocations, and `start` against every
   operation."
8. (1.2.4.2, next to `ISA-11-P4` (`ISA-11-P4.S5`)) OPEN. Needed: which
   operation identifies a cleanup for selection. For example: "A `cleanup`
   entry is matched against the cleanup's first generated operation; the
   chosen realisation applies to the whole cleanup."
9. (1.4.1, next to `ISA-11-P4` (`ISA-11-P4.S9`)) ASSUMED. Needed sentence:
   "Validation includes the maximal-match condition, and is completed before
   any operation executes."
10. (1.4.3, next to `ISA-11-P4` (`ISA-11-P4.S9`) and `ISA-9.2-P2`
    (`ISA-9.2-P2.S13`)) OPEN (refuted for unbound admission). Needed, one
    of: (a) "The maximal-match condition is checked against the step domains
    of the run's tokens; a consumer that does not know them defers the check
    to binding", or (b) record each nested token's budget in the bindings,
    e.g. `"tokens": [[B,heap,stack,depth], …]` in parameter order, so that
    the schedule alone determines Ω. Either way, also define the JCS value
    of a `token` parameter in `params_hash`.
11. (1.6.2, next to `ISA-11-P4` (`ISA-11-P4.S4`)) ASSUMED. Needed sentence:
    "The applying entry supplies every field of its decision; a field it
    omits takes its default, never the value of a less specific entry."
12. (1.6.3.2, next to `ISA-17-P8` (`ISA-17-P8.S2`)) ASSUMED. Needed: "the
    ISA version of the object" in place of "the ISA's own version".
13. (1.6.3.3, next to `ISA-11-P2` (`ISA-11-P2.S3`) and `ISA-17-P8.S2`) OPEN.
    Needed: the hash of `ref` for each ISA version, or the sentence "the
    default binding has no hash and is never equal to a written binding".
14. (1.6.4.2, next to `ISA-8.1-P10` (`ISA-8.1-P10.S1`, `ISA-8.1-P10.S2`) and
    `ISA-17-P10.S2`) OPEN. Needed sentence: "An operation is ε > 0 iff no
    `gates` entry with `epsilon` 0 matches it. N counts such operations over
    every invocation of the root region in the schedule, and the region's
    `epsilon` is `bindings.epsilon`."
15. (1.6.4.3, next to `ISA-17-P10` (`ISA-17-P10.S2`)) OPEN (refuted). Needed
    sentence: "The default share is the exact rational ε / N; it need not be
    expressible as a decimal and is never written into the schedule."
16. (1.6.5, next to `ISA-11-P3` (`ISA-11-P3.S2`)) ASSUMED. Needed sentence:
    "Decimal strings in a schedule denote the exact rational of their text;
    spelling is not significant."
17. (1.6.7, next to `ISA-11-P4` (`ISA-11-P4.S6`, `ISA-11-P4.S3`)) OPEN
    (refuted) as a property of (C), not a defect. No sentence is needed
    unless 0.9 wants every resolved decision to be writable. In that case,
    see the alternative in gap 5.


# Background (not graded): `INV-6-certificate-soundness.md`

# INV-6: certificate labels are sound, evidence is exact, host limits are honest

Spec: ISA 0.8 (`clauses/ISA-0.8.json`). Format: `proofs/FORMAT.md`.

## Informal statement

An `exhaustive` claim (§12.1) compares a region R, on every element of a
`domain` (§12.2), with an expected program or table. A `sampled` claim replays
draws from a domain. §12.2 says: "A `proof` label requires the domain to equal
D; otherwise the claim is `evidence` with the covered fraction." The checker's
verdict feeds T3 (§14.3), borrow frames (§5.6) and composition (§12.3), so the
classifier that decides "the domain equals D" is load-bearing. INV-1 to INV-5
take it for granted. INV-3 1.5.2 assumes a T3 claim over the full domain and
does not prove that the label means what it says. INV-6 states and proves the
missing theorem:

- (A) **Label soundness.** If a conformant checker returns `Proof` for an
  exhaustive claim comparing R with an expected program Q (or a table), then
  the full output tuples agree on every element of R's full domain D. In
  particular, `Proof` implies that the enumerated domain equals D component by
  component. Components are identified by role and position (interface bundle
  (group, slot), region cell (group, slot, index), borrowed bundle k), never
  by name alone, and a `borrowed` entry covers no interface component.
- (B) **Evidence semantics.** A claim whose domain is a strict subset of D, or
  a `sampled` claim, yields at most `Evidence`, with the exact number of
  replayed elements. The verdict depends only on R and Q restricted to those
  elements. It licenses no conclusion about the rest of D.
- (C) **Resource honesty.** A checker that cannot materialise or enumerate a
  legal domain reports a host limitation. It does not abort, does not reject
  the domain as ill-formed, and does not label the claim `Proof` or `Evidence`.

Council rounds 21 and 22 on the reference interpreter found one violation of
(C) and one of (A) (see "Council blockers as instances"). The proof shows:

- (A) holds in 0.8 under readings, because §12.2 does not say what an entry's
  `name` refers to. It never says that coverage is by name. It never says that
  coverage is by component either: the text compares "the domain" with D and
  leaves the map from entries to components implicit. Once a `bundles` or
  `regions` name is read as naming an interface slot, and a `borrowed` entry
  as naming a borrowed system by position, the label is sound (1.5). A name-set
  classifier is unsound under every reading (1.5.5).
- (B) holds, with the exact count derived from the domain (1.6.3), except
  that the "covered fraction" of a sampled claim is undefined (1.6.5). The
  phrase "licenses no conclusion" is true of the label. It is refuted as a
  statement about mathematics: for bijective subjects, agreement on all but
  one element forces agreement on the last (1.6.8). That limits the theorem,
  not the spec.
- (C) has no basis in 0.8. The spec names no checker outcome for a legal
  claim that cannot be checked on the host (1.7.5). What 0.8 does fix is what
  a checker must not do: reject a legal domain (1.7.2) or issue a label for
  elements it did not replay (1.7.3).

## Precise statement

Fix a well-formed object O and a region R of O with closure hash h
(`ISA-9.2-P2.S15`). R is a lifted oracle (§5.2) or a permutation action
(§5.3). Fix a claim c in R's `claims` of kind `exhaustive` (domain d, expected
`{program: h_Q}` or `{table: T}`) or `sampled` (domain d, sampler σ).

DEFINE comp(R), the **components** of R, each with an identity and a width w ≥ 1:
- interface bundle: (g, j), with g the role group and j the slot index within g
  in declared order. The groups are `in`, `tgt`, `fault` for an oracle and `mut`,
  `in` for an action;
- interface region cell: (g, j, i) for cell i < 2^A of the j-th region of group
  g (`region[A,W]`, width W). The groups are `in` regions for an oracle and
  `mut` and `in` regions for an action;
- borrowed bundle: (`borrowed`, k), the k-th borrowed bundle of R.

DEFINE D(R) = Π_{γ ∈ comp(R)} {0, …, 2^{w_γ} − 1}, the set of basis
configurations (`ISA-2-P7.S1`). Workspace is at 0 and local regions are at
their image, so neither is a component.

DEFINE res(e), the **resolution** of a domain entry e, as the component (or,
for `cells: "all"`, the set of cells) the entry denotes (readings 1.2.2,
1.2.3). DEFINE ⟦d⟧ ⊆ D as the set of configurations x with x(res e) ∈
[lo_e, hi_e] for every entry e, and x(γ) = z_γ for every γ ∉ img(res). Here
z_γ is the fill value of an omitted component (reading 1.2.4).

DEFINE covers(d) ⟺ res is injective, img(res) = comp(R), and every entry has
lo = 0 and hi = 2^{w} − 1.

DEFINE tup_R(x) as the full output tuple of R on x: the final value of every
component, in comp(R) order (reading 1.4.2).

DEFINE a **checker outcome** as one of `Proof`, `Evidence(n)` (n replayed
elements), `Reject(rule)` (a stated rule of §12 is violated: ill-formed claim
or tuple mismatch) and `HostLimit(clause)` (reading 1.7.6). A checker is
**conformant** if it meets the §12.1 obligations and §12.2 under the readings
of this proof.

THEOREM INV-6. For every conformant checker K, every such c, and every R, Q:
- (A) K(c) = `Proof` ⇒ c is exhaustive, covers(d), and tup_R(x) = tup_Q(x)
  (resp. the row of T for x) for every x ∈ D. A `borrowed` entry is never in
  res⁻¹ of an interface component, whatever its name.
- (B) ¬covers(d) or c sampled ⇒ K(c) ∈ {`Evidence(n)`, `Reject`, `HostLimit`}.
  For exhaustive c, n = |⟦d⟧| = Π_e (hi_e − lo_e + 1) and the covered fraction
  is n / |D|. For sampled c, n = `count`. K(c) is a function of R and Q
  restricted to the replayed elements.
- (C) If d is legal and K cannot materialise an element of ⟦d⟧ or enumerate
  ⟦d⟧, then K(c) = `HostLimit(§12.2)`. K terminates normally and never returns
  `Reject` on a legality ground, `Proof` or `Evidence` for that claim.

THEOREM INV-6' (what holds in 0.8).
- (A) holds under readings 1.1.3 (action D), 1.2.2 to 1.2.5 (entry resolution,
  borrowed position, fill, duplicates), 1.4.2 to 1.4.4 and 1.4.6 (tuple,
  program correspondence, table order, oracle budget) and 1.5.1 (label is the
  checker's verdict). The name-set classifier is refuted outright (1.5.5).
- (B) holds for exhaustive claims. For sampled claims the fraction is
  undefined (1.6.5). "No conclusion outside ⟦d⟧" is refuted as a mathematical
  statement when |D ∖ ⟦d⟧| = 1 and both sides are bijections of D (1.6.8).
- (C) holds only as a reading (1.7.6). 0.8 has no outcome for it (1.7.5 OPEN).
  Its negative half, never reject a legal domain and never label unreplayed
  elements, is proved (1.7.2, 1.7.3).

## Hypotheses

ISA-1.2-P4.S1, ISA-2-P1.S2, ISA-2-P7.S1, ISA-3.3-P1.S1, ISA-3.3-P3.S2,
ISA-3.3-P14.S1, ISA-4.3-P2.S1, ISA-4.4-P1.S1, ISA-4.4-P2.S1, ISA-5.1-P1.S1,
ISA-5.1-P1.S2, ISA-5.2-P1.S1, ISA-5.2-P2.S1, ISA-5.2-P2.S2, ISA-5.2-P2.S3,
ISA-5.2-P4.S1, ISA-5.3-P1.S1, ISA-5.3-P1.S4, ISA-5.6-P1.S1, ISA-5.6-P2.S2,
ISA-9.2-P1.S1, ISA-9.2-P2.S15, ISA-9.4-P2.S1, ISA-9.4-P3.S1, ISA-12.1-P1.S1,
ISA-12.1-P2.S1, ISA-12.1-P5.S1, ISA-12.1-P7.S5, ISA-12.1-P8.S1,
ISA-12.2-P1.S1, ISA-12.2-P1.S2, ISA-12.3-P2.S3, ISA-14.1-P1.S1,
ISA-14.2-P1.S2, ISA-14.3-P3.S1.

## Proof

```
<1>1. D(R) is the product over comp(R) of full ranges, and components with
      different identities are different systems.
      PROOF:
  <2>1. For an oracle, D is "every value of each `ins`, of `tgt`, of `fr`, of
        every cell of every `in` region, of every borrowed bundle; `qalloc`ed
        wires at 0; local regions at image".
        BY ISA-5.2-P4.S1
  <2>2. An action body denotes a unitary U on "mut ⊗ ins ⊗ mem_mut ⊗
        (borrowed)", block-diagonal in `ins` and in `in`-region cells and the
        identity on borrowed systems; a permutation action's U is a
        permutation matrix.
        BY ISA-5.3-P1.S1, ISA-5.3-P1.S4
  <2>3. Reading adopted: an action's D is every value of each `mut` and `in`
        bundle, of every cell of every `mut` and `in` region and of every
        borrowed bundle, with workspace at 0 and local regions at image.
        ASSUMED: §5.3 defines no D, although T3, T6, §5.7 and §12.2 use it
        for actions; the factor list "mem_mut" omits `in` regions that the
        same sentence calls block-diagonal; the reading takes the oracle
        pattern of <2>1 and the full factor list of <2>2.
  <2>4. Interface components are identified by role and position:
        signatures list roles, interface bundles and regions are "passed in
        declared order", and the frame descriptor lists interface slots by
        (role, width, class). A region[A,W] slot holds 2^A cells of W bits.
        BY ISA-5.1-P1.S1, ISA-5.1-P1.S2, ISA-9.4-P2.S1, ISA-9.4-P3.S1,
           ISA-3.3-P1.S1, ISA-3.3-P14.S1
  <2>5. Distinct interface components are distinct wires: "A region's
        interface bundles and regions are pairwise disjoint."
        BY ISA-3.3-P3.S2
  <2>6. A borrowed bundle is a tensor factor of its own: `qborrow` gives "n
        wires in unknown state" and "introduces a factor ... possibly
        entangled with a reference system R", and the region's operation is
        U ⊗ I on it. No interface component is that factor.
        BY ISA-4.3-P2.S1, ISA-14.2-P1.S2, ISA-5.6-P1.S1
  <2>7. QED: D(R) = Π_{γ ∈ comp(R)} {0..2^{w_γ} − 1}, |D| = 2^{Σ w_γ}, and a
        basis configuration assigns each component independently.
        BY <2>1, <2>3, <2>4, <2>5, <2>6, ISA-2-P7.S1; algebra

<1>2. A domain d denotes the set ⟦d⟧ ⊆ D, and
      |⟦d⟧| = Π_e (hi_e − lo_e + 1).
      PROOF:
  <2>1. The domain lists `bundles` and `borrowed` entries {name, width, lo,
        hi} and `regions` entries {name, cells: "all" | [{index, lo, hi}]},
        "bounds inclusive, enumeration order as listed, last component
        fastest".
        BY ISA-12.2-P1.S1
  <2>2. Reading adopted: the name of a `bundles` entry denotes the interface
        bundle of R that has that local name in R's header, and the entry
        resolves to its identity (g, j). The name of a `regions` entry likewise
        resolves to an interface region (g, j). `cells: "all"` resolves to
        its 2^A cells (g, j, i), and a list entry to cell (g, j, index). A name
        that matches no interface bundle (resp. region) of R makes the claim
        ill-formed.
        ASSUMED: §12.2 gives the field `name` and nothing else. It says
        neither that names are R's header names nor what they resolve to.
        Header names are fixed by h (canonical function bytes, ISA-9.2-P1.S1),
        so the reading is well defined; the identity it yields is positional
        (<1>1.4).
  <2>3. Reading adopted: the k-th `borrowed` entry denotes the borrowed
        bundle (`borrowed`, k) of R, in the order of R's borrow requirement
        (first `qborrow` in canonical text order). Its `name` refers to
        nothing and is never looked up among interface names.
        ASSUMED: §12.2 does not say what a `borrowed` name refers to, nor
        that it may or may not coincide with an interface name. A borrowed
        system has no interface name to match (`w = qborrow cls n` binds
        only a body-local value, <1>1.6).
  <2>4. Reading adopted: a component of comp(R) that no entry resolves to
        holds one fixed value z_γ on every element that is replayed (the
        reference interpreter's choice is z_γ = 0).
        ASSUMED: §12.2 does not say what an omitted component holds, or
        whether a domain may omit one. The theorem depends on z only through
        ⟦d⟧ ⊆ D.
  <2>5. Reading adopted: an entry whose `width` differs from its component's
        width, an index ≥ 2^A, hi ≥ 2^w, lo > hi, or two entries that resolve
        to one component make the claim ill-formed (`Reject`).
        ASSUMED: §12.2 states none of these conditions.
  <2>6. QED: under <2>2 to <2>5 res is an injective partial map into comp(R)
        (cells counted singly), ⟦d⟧ is the product of the entry ranges with the
        omitted components fixed at z, and the enumeration of <2>1 lists each
        element once.
        BY <1>1, <2>1, <2>2, <2>3, <2>4, <2>5; algebra

<1>3. ⟦d⟧ = D iff covers(d). Coverage is a property of resolved
      identities and ranges, never of entry names.
      PROOF:
  <2>1. If covers(d), then ⟦d⟧ = D.
        BY <1>1, <1>2; algebra
  <2>2. If some γ ∈ comp(R) is not in img(res), then
        ⟦d⟧ ⊆ {x : x(γ) = z_γ}, a strict subset of D because w_γ ≥ 1.
        BY <1>1, <1>2.4, <1>2.6; algebra
  <2>3. If some entry has lo > 0 or hi < 2^w − 1, then ⟦d⟧ ⊊ D.
        BY <1>2.6; algebra
  <2>4. A `borrowed` entry resolves to a borrowed identity, which differs
        from every interface identity; so it never puts an interface
        component into img(res), whatever it is called.
        BY <1>1.6, <1>2.3
  <2>5. Two domains with the same resolved entries and ranges have the same
        ⟦d⟧ whatever their names. In particular, renaming a `borrowed` entry
        never changes ⟦d⟧ or covers(d).
        BY <1>2.6, <2>4
  <2>6. QED
        BY <2>1, <2>2, <2>3, <2>4, <2>5

<1>4. For every x ∈ ⟦d⟧ that a conformant checker replays for an
      exhaustive claim, it has compared tup_R(x) with tup_Q(x) (resp. the row
      of T for x).
      PROOF:
  <2>1. The obligation of an `exhaustive` claim is: "re-execute every
        domain element on the reference interpreter / expected program;
        compare full tuples".
        BY ISA-12.1-P1.S1
  <2>2. Reading adopted: the full tuple of x is the final value of every
        component of comp(R), in comp(R) order. This includes the borrowed
        bundles, whose final value must equal their initial value.
        ASSUMED: §12.1 does not define the tuple or its encoding
        (interpreter SPEC-QUESTIONS 21).
  <2>3. Reading adopted: `expected: {program: h_Q}` names a region with the
        same interface slots (role, width, class) and the same borrow
        requirement, and tup_Q(x) is read slot by slot: (g, j) of R against
        (g, j) of Q, borrowed k against borrowed k, never by local name.
        ASSUMED: §12.1 says neither that Q's signature equals R's nor how
        their components correspond; the positional reading follows the ABI
        (ISA-9.4-P2.S1).
  <2>4. Reading adopted: row k of `table` is the expected tuple of the k-th
        element in the enumeration order of ISA-12.2-P1.S1, and a table with
        a row count other than |⟦d⟧| is ill-formed.
        ASSUMED: §12.1 fixes no table encoding or correspondence.
  <2>5. Each x ∈ D has one final basis tuple: an oracle is exact-permutation
        and an involution on (ins, tgt, fr), and its contract fixes every
        other component; a permutation action's unitary is a permutation
        matrix.
        BY ISA-5.2-P1.S1, ISA-5.2-P2.S1, ISA-5.2-P2.S3, ISA-5.3-P1.S4,
           ISA-14.1-P1.S1
  <2>6. Reading adopted: an oracle claim is replayed at one fixed budget B
        (F_B depends on B), namely B of the root schedule bound by the
        certificate.
        ASSUMED: an exhaustive claim has no `subject`, but ISA-12.3-P2.S3
        says that `exhaustive` claims with `expected: "oracle"` "bind to
        `schedule_hash` through their subject"; for `program` and `table`
        expectations no budget is named at all (ISA-5.2-P2.S2 makes the
        tuple depend on it).
  <2>7. QED
        BY <2>1, <2>2, <2>3, <2>4, <2>5, <2>6

<1>5. (A) If a conformant checker returns `Proof` for c, then c is
      exhaustive, covers(d), and tup_R(x) = tup_Q(x) for every x ∈ D.
      PROOF:
  <2>1. Reading adopted: "A `proof` label" in §12.2 is the checker's
        verdict on the claim. A producer-written `label` field, if present,
        is a request that the checker validates, never a premise.
        ASSUMED: the §12.1 payloads contain no `label` field, and §12.2 does
        not say who assigns the label. ISA-1.2-P4.S1 ("validates
        certificates (§12) without trusting producers") rules out taking a
        producer's label on trust.
  <2>2. `Proof` ⇒ ⟦d⟧ = D ⇒ covers(d).
        BY <2>1, ISA-12.2-P1.S2, <1>3
  <2>3. `Proof` ⇒ c is exhaustive: a `sampled` claim is "replay;
        **evidence**".
        BY ISA-12.1-P2.S1
  <2>4. `Proof` ⇒ every element of ⟦d⟧ = D was replayed and its tuples were
        equal. A mismatch is a failed obligation, so the outcome is `Reject`,
        not `Proof`.
        BY <2>2, <2>3, <1>4
  <2>5. A classifier that decides coverage from names, i.e. N(d) ⟺ every
        interface name of R occurs among the names of all entries of d and
        all ranges are full, is unsound: N(d) holds while ⟦d⟧ ≠ D, and a
        checker using it issues a false `Proof`.
        PROOF:
    <3>1. Let R = `action @a (t:wire mut, u:wire mut)` with body
          `b = qborrow any 1; cx t u; qreturn b`, and Q = `@identity` with
          the same signature and body `b = qborrow any 1; x u; x u;
          qreturn b`. comp(R) = {(mut,0)=t, (mut,1)=u, (borrowed,0)=b},
          |D| = 8.
          BY <1>1, ISA-4.3-P2.S1
    <3>2. Let d = {bundles: [{u,1,0,1}], borrowed: [{t,1,0,1}],
          regions: []}. The names {u, t} include every interface name and
          every range is full, so N(d) holds.
          BY ISA-12.2-P1.S1; algebra
    <3>3. res(u-entry) = (mut,1) and res(t-entry) = (borrowed,0), so
          (mut,0) ∉ img(res), ⟦d⟧ = {x : x(t) = z} has 4 elements and
          ⟦d⟧ ≠ D.
          BY <1>2.3, <1>3.2, <1>3.4
    <3>4. On ⟦d⟧ with z = 0, `cx t u` is the identity, so all 4 compared
          tuples agree. At (t,u,b) = (1,0,0), R gives (1,1,0) and Q gives
          (1,0,0).
          BY ISA-4.4-P1.S1, ISA-4.4-P2.S1; algebra
    <3>5. QED: a checker that uses N replays the 4 elements, finds no
          mismatch and returns `Proof`, which contradicts <2>2 and the
          conclusion of (A).
          BY <3>2, <3>3, <3>4, <2>2
  <2>6. For a permutation-valued R, `Proof` against a permutation P (table
        or Q) supplies the premise of T3, "the final basis tuple equals P(x)
        for every x ∈ D", hence V|span(D) = P. This is the premise that
        INV-3 1.5.2 assumes for borrow frames ("established by a T3 claim
        over the frame's full domain").
        BY <2>4, ISA-14.3-P3.S1, ISA-5.6-P2.S2
  <2>7. QED
        BY <2>2, <2>3, <2>4, <1>3.4

<1>6. (B) If ¬covers(d) or c is sampled, the outcome is at most
      `Evidence(n)` with the exact n, and it depends only on the replayed
      elements.
      PROOF:
  <2>1. ¬covers(d) ⇒ ⟦d⟧ ≠ D ⇒ the claim is "`evidence` with the covered
        fraction", never `Proof`.
        BY <1>3, ISA-12.2-P1.S2, <1>5.1
  <2>2. A sampled claim is evidence.
        BY ISA-12.1-P2.S1
  <2>3. For exhaustive c, the replayed elements are exactly ⟦d⟧, so
        n = |⟦d⟧| = Π_e (hi_e − lo_e + 1), where a `cells: "all"` entry
        contributes 2^{W·2^A}. Since ⟦d⟧ ⊆ D, the covered fraction n / |D|
        is at most 1. It is less than 1 iff ¬covers(d).
        BY <1>2.6, <1>1.7, <1>3; algebra
  <2>4. A sampled claim's draws are elements of ⟦d⟧: each component of the
        domain is drawn in [lo, hi], "components are consumed in enumeration
        order", and omitted components keep z. So n = `count` replayed
        draws, of which at most `count` are distinct.
        BY ISA-12.1-P8.S1, ISA-12.1-P2.S1, <1>2.4
  <2>5. Reading adopted: a sampled claim reports n = `count` (draws
        replayed). If a fraction is reported, it is (distinct draws) / |D|.
        ASSUMED: §12.2 asks for "the covered fraction", which is undefined
        for draws with repetition, and §12.1 says only "replay; evidence".
  <2>6. The outcome is a function of tup_R and tup_Q (or T) restricted to
        the replayed elements. The checker executes nothing else.
        BY ISA-12.1-P1.S1, ISA-12.1-P2.S1, <1>4
  <2>7. So `Evidence` licenses no conclusion about D ∖ ⟦d⟧ beyond what
        agreement on ⟦d⟧ implies by itself. Instance: the pair of 1.5.5
        agrees on its 4 elements and differs at (1,0,0).
        BY <2>6, <1>5.5
  <2>8. The literal clause "never implies agreement outside the enumerated
        elements" is false in one corner. Let |D ∖ ⟦d⟧| = 1, say
        D ∖ ⟦d⟧ = {x₀}, and let R and Q be bijections of D: an oracle (an
        involution with its other components fixed) or a permutation action
        against a permutation Q. Agreement on ⟦d⟧ forces
        tup_R(x₀) = tup_Q(x₀), the only value left. The label is still
        `Evidence`.
        OPEN (refuted): limits the theorem, not the spec. With
        |D ∖ ⟦d⟧| ≥ 2, or with a table, agreement outside ⟦d⟧ is not
        forced in general (<2>7).
  <2>9. QED
        BY <2>1, <2>2, <2>3, <2>4, <2>5, <2>6, <2>7

<1>7. (C) A checker that cannot materialise or enumerate a legal domain
      reports a host limitation.
      PROOF:
  <2>1. The domain schema has no cap on `width`, on A of a region[A,W], on
        the length of a cell list or on `count`. So a claim over a
        region[63,1] with `cells: "all"` and `count` 1 is legal.
        BY ISA-12.2-P1.S1, ISA-12.1-P2.S1, ISA-3.3-P1.S1
  <2>2. Hence `Reject` on a legality ground (an "invalid domain", an
        out-of-range region, a width cap) is false for such a claim.
        BY <2>1, <1>2.5
  <2>3. Neither label may be issued for elements that were not replayed:
        `Proof` needs every element of D (<1>5.4), and `Evidence(n)` counts
        replayed elements (<1>6.3, <1>6.4).
        BY <1>5.4, <1>6.3, <1>6.4, ISA-12.1-P1.S1
  <2>4. A single element of a domain over region[A,W] carries 2^A·W bits,
        and |D| can reach 2^{W·2^A}. So whether a legal claim can be checked
        depends on the host, even at `count` 1.
        BY ISA-3.3-P14.S1, <1>1.7; algebra
  <2>5. 0.8 names no checker outcome for "legal, but not checkable on this
        host". The outcomes it names are `proof` and `evidence`
        (ISA-12.2-P1.S2) and rejection ("too few witnesses: reject",
        ISA-12.1-P5.S1; "an inconclusive test rejects", ISA-12.1-P7.S5).
        OPEN: the missing outcome. By analogy with ISA-12.1-P7.S5, an
        inconclusive check rejects the claim, which is honest only if a
        reject never reads as "the certificate is ill-formed" (<2>2).
  <2>6. Reading adopted: such a checker returns `HostLimit(§12.2)`, which
        is distinct from `Reject` and from both labels, names the quantity
        that does not fit, and terminates normally (no abort, no panic). The
        claim then counts as unverified for T3, §5.6 and §12.3.
        ASSUMED: needs <2>5's sentence; the repository rule "fail fast,
        fail loud" and the interpreter's R21 design take this reading.
  <2>7. Under <2>6, a host-limited claim supplies no T3 premise (1.5.6)
        and no evidence count.
        BY <2>3, <2>6, <1>5.6
  <2>8. QED
        BY <2>2, <2>3, <2>6, <2>7

<1>8. QED: (A) by <1>5; (B) by <1>6, limited by <1>6.8; (C) by <1>7 under
      reading <1>7.6.
      BY <1>5, <1>6, <1>7
```

## Witnesses

Interpreter tests are in `bennett-isa-spec-review/reference-interpreter` at
`9851a9c` (the round-22 snapshot). They are evidence, not justification.

| Witness | Steps |
|---|---|
| `tests/r1_certificates.rs::sol_r4_b03_expected_program_uses_signature_positions_for_renamed_bundles` (renamed and reordered bundles: `Proof`; one bundle omitted: `Evidence { elements: 2 }`; borrowed entries `z`, `b` do not affect coverage) | 1.2.2, 1.2.4, 1.3.2, 1.4.3, 1.6.3 |
| `::sol_r4_b03_expected_program_maps_renamed_region_cells_positionally` (`cells: "all"`: `Proof`; one listed cell: `Evidence { elements: 8 }`) | 1.2.2, 1.3.3, 1.6.3 |
| `::sol_r4_b03_positions_distinguish_same_width_slots_and_crossed_names` (crossed local names; wrong slot fails §12.1) | 1.1.4, 1.4.3 |
| `::b14_checked_borrow_claim_and_altered_or_incomplete_claims` (full domain with borrowed `b`: `Proof`; one wrong table row: §12.1; t up to 7, or no borrowed entry: not a §5.6 proof) | 1.3.3, 1.4.4, 1.5.4, 1.5.6, 1.6.1 |
| `::r17_sample_count_default_replays_and_present_values_validate` (sampled: `Evidence` with the replayed count) | 1.6.2, 1.6.4, 1.6.5 |
| `tests/r21_resources.rs::r21_b01_claims_public_consumers` → `r21_resource_child` family `claims` (all-cells and explicit-list region domains at A ∈ {0,1,3,62,63,64,127,128} through `verify_claim` and `verify_certificate` under RLIMIT_AS; A < 4 give `Evidence { elements: 1 }`, larger A a §12.2 host-limit error, no abort; the small all-cells exhaustive control is `Proof`) | 1.7.1, 1.7.2, 1.7.4, 1.7.6 |
| `tests/r21_resources.rs::r21_independent_witness_pins` (the reviewer objects, including `sol-claim-region-all-sampled.bisa`, keep their hashes) | 1.7.1 |
| `tests/r21_resources.rs::r21_cli_cardinality_and_sparse_output` (huge sample counts are entered lazily and stop at a reported storage error) | 1.7.3, 1.7.6 |
| Council files `bennett-isa-spec-review/.tmp/r22-sol/false-cnot-proof.bisa` (`Proof` at `9851a9c`, should be `Evidence { elements: 4 }`), `false-cnot-renamed-control.bisa` (borrowed entry renamed `b`: `Evidence { elements: 4 }`), `false-cnot-full-control.bisa` (t added: §12.1 mismatch at element 4) | 1.3.5, 1.5.5 (all of it), 1.6.3, 1.6.7; counter-witness until an R22 test lands |
| Council file `.tmp/r22-sol/domain-role-spoof.bisa` (`action @a (t:wire mut)`, body `x t`, domain only `borrowed: [t]`, table `[[1,0],[1,1]]`; no verdict recorded in the packet) | 1.5.5 with a table instead of Q (the row for t = 1 is never checked) |

No test exists yet for 1.2.5 (duplicate entries, width mismatch), 1.4.6
(the budget of an oracle claim with a `program` expectation) or 1.6.8. The
interpreter's `Object::domain` at `9851a9c` (`src/claims.rs`, lines 251 to
336) is the classifier N of 1.5.5: it puts the names of `bundles` and
`borrowed` entries into one set and tests the interface names against it.
It also sets `full = false` for every explicit cell list, so a list that
names every cell with full ranges gets `Evidence`. That is conservative,
and it agrees with (A), but under 1.3.1 such a list covers D.

## Council blockers as instances

- **R21-B01** (SOL-R21-B01, CODEX-R21-B01; a legal region[63,1]
  `cells: "all"` sampled claim with `count` 1 aborted the process with
  SIGABRT while the domain components were being expanded): violates
  1.7.6 (no normal termination and no `HostLimit` outcome). The council's fix
  rules out the two dishonest alternatives as well: capping A or relabelling
  the range as invalid violates 1.7.2, and labelling the claim violates
  1.7.3. Its root cause is 1.7.4: a `count` of 1 does not bound the size
  of an element. 0.8 gives the checker no outcome to report (1.7.5), so the
  determining text the council cited (§12.2 schema, §4.6 "2^A cells") fixes
  legality, not the outcome.
- **SOL-R22-B01** (borrowed entry spelled `t` discharged the interface
  bundle `t`, which was zero-filled; CNOT certified equal to identity):
  violates 1.3.4, and through it 1.5.2 and the conclusion of (A). The
  classifier was N of 1.5.5, which checks names where 1.3 requires resolved
  identities. The zero fill (1.2.4) is not itself the defect: it is
  harmless once ⟦d⟧ ≠ D is recognised, and the verdict then becomes
  `Evidence(4)` by 1.6.3. The renaming control is an instance of 1.3.5:
  renaming a borrowed entry must not change the verdict. The council said
  no spec edit is required. Under readings 1.2.2 and 1.2.3 that holds, but
  0.8 states neither reading.

## Spec gaps

1. (1.1.3, next to `ISA-5.3-P1` (`ISA-5.3-P1.S1`)) ASSUMED. Needed sentence:
   "**Domain D** of an action: every value of each `mut` and `in` bundle, of
   every cell of every `mut` and `in` region and of every borrowed bundle;
   workspace at 0, local regions at image." Also make the factor list read
   "mut ⊗ ins ⊗ mem ⊗ (borrowed)", or say why `in` regions are absent.
2. (1.2.2, next to `ISA-12.2-P1` (`ISA-12.2-P1.S1`)) ASSUMED. Needed
   sentence: "The `name` of a `bundles` or `regions` entry is the local name
   of an interface bundle or region in the subject's header, and the entry
   denotes that interface slot (role and position); a name that is not one
   is an error. Coverage is decided on the denoted slots and cells, never on
   names."
3. (1.2.3, next to `ISA-12.2-P1` (`ISA-12.2-P1.S1`)) ASSUMED. Needed
   sentence: "The k-th `borrowed` entry denotes the subject's k-th borrowed
   bundle in the order of its borrow requirement; its `name` is a label
   only, may coincide with any other name, and never denotes an interface
   slot." This answers whether a borrowed name may coincide with an
   interface name: in 0.8 nothing forbids it and nothing gives it meaning.
4. (1.2.4, next to `ISA-12.2-P1` (`ISA-12.2-P1.S2`)) ASSUMED. Needed
   sentence: "A component of D that the domain omits is held at 0 on every
   element; the domain then denotes the slice of D at 0, and its covered
   fraction is the slice's size over |D|." The alternative is to forbid
   omission ("every component of D appears in the domain") and to express
   partial domains only by ranges.
5. (1.2.5, next to `ISA-12.2-P1` (`ISA-12.2-P1.S1`)) ASSUMED. Needed
   sentence: "Each component appears at most once; `width` equals the
   component's width; 0 ≤ lo ≤ hi < 2^width; cell indices are below 2^A;
   otherwise the claim is ill-formed."
6. (1.4.2, next to `ISA-12.1-P1` (`ISA-12.1-P1.S1`)) ASSUMED. Needed
   sentence: "The full tuple of a domain element is the final value of every
   component of D, in the order: interface bundles by role and slot,
   interface region cells, borrowed bundles." Also fix the table row
   encoding (gap 8).
7. (1.4.3, next to `ISA-12.1-P1` (`ISA-12.1-P1.S1`)) ASSUMED. Needed
   sentence: "An expected program has the subject's interface slots and
   borrow requirement; its components correspond to the subject's by role and
   position, not by name."
8. (1.4.4, next to `ISA-12.1-P1` (`ISA-12.1-P1.S1`)) ASSUMED. Needed
   sentence: "`table` holds one full tuple per domain element, in
   enumeration order; each entry is a §9.1 integer; a table of any other
   length is an error."
9. (1.4.6, next to `ISA-12.3-P2` (`ISA-12.3-P2.S3`) and `ISA-12.1-P1`
   (`ISA-12.1-P1.S1`)) ASSUMED. ISA-12.3-P2.S3 binds an `exhaustive` claim
   "through [its] subject", but the exhaustive payload has no subject.
   Needed: a `subject` (or at least `schedule_hash` and `budget`) in the
   `exhaustive` and `sampled` payloads of oracle claims, and the sentence
   "an oracle claim is replayed at the budget of its subject".
10. (1.5.1, next to `ISA-12.2-P1` (`ISA-12.2-P1.S2`)) ASSUMED. Needed
    sentence: "The label (`proof` or `evidence`) is the checker's verdict; a
    certificate does not assert it, and a written `label` field is
    rejected (or: is checked and rejected if it claims more than the
    verdict)."
11. (1.6.5, next to `ISA-12.1-P2` (`ISA-12.1-P2.S1`) and `ISA-12.2-P1.S2`)
    ASSUMED. Needed sentence: "A sampled claim reports `count` replayed
    draws; its covered fraction is the number of distinct elements drawn over
    |D|."
12. (1.7.5, next to `ISA-12.2-P1` (`ISA-12.2-P1.S1`,
    `ISA-12.2-P1.S2`)) OPEN; reading 1.7.6 ASSUMED. Needed sentence: "A
    checker that cannot replay a legal claim on its host reports the claim
    as **unchecked (host limit)**. This is neither a label nor a rejection of
    the certificate, and an unchecked claim discharges no obligation of §5.6,
    T3 or §12.3." State also that 0.8 imposes no cap on domain widths, A or
    `count`, so that no checker may invent one.

1.5.5 and 1.6.8 need no spec text: 1.5.5 refutes a classifier, and 1.6.8
limits the theorem's wording.


# The document under review (round 7 snapshot)

# Bennett Virtual ISA — Specification, version 0.9

**Date:** 2026-10-31. **Status:** version 0.9, **accepted by all three council seats on 2026-10-31** (sol r3, codex r2/r4, muse r5; K64/K65 ratified). ISA 0.9 is the version new consumers (bennett-vm M5 onward) implement. ISA 0.8 remains published as `spec/Bennett-ISA-Spec.md` and remains the version the dialect 0.2.x gate and the reference interpreter target until the dialect 0.3 track moves.
Snapshot `59eee9ad0d96` was accepted by the sol and codex seats (council run
`isa-09-2026-10-31`: codex round 2, sol round 3, both core accept, 0 blocking; muse seat held).
K64 and K65 were ratified by the maintainer on 2026-10-31; muse accepted
in round 5 that day, satisfying the council-vote publication gate
(maintainer ruling 2026-10-31). It
revises draft 0.8, which was **accepted by the council in round 8**
(2026-10-28; reports and the editor's responses under
`docs/council/isa-2026-10-28/round-{1..8}/` in the `bennett` meta
repository).
§0 lists every change from 0.8.
Implementation is expected to expose frictions; revisions go back
through the council. Founding text of
`bennett-isa-spec` (`Bennett-NorthStar.md` §4.4, §6.1); the north star
governs where this document is silent. The reference interpreter targets
0.8; 0.9 admission is not claimed. MUST, MUST
NOT, SHOULD, MAY are normative; *(non-normative)* explains; *(deferred)*
names items left open; every deferred decision that an implementer must
take carries a **default** in §17, which implementers follow until the
item is revised.

**Versioning.** ISA 0.9, object 0.9, launch 0.9, sched 0.9, cert 0.9,
coverage 0.9, target 0.9. The **full version string** (`0.9`) is part of
every semantic envelope (§9.2): drafts are not compatible with each
other, so every hash of every 0.8 object differs under 0.9 (§0, §16.3).

---

## 0. Changes from 0.8

Every change from the accepted draft 0.8 has one entry below; nothing
changes without an entry. **Kind**: *E* = editorial (wording, or a
reading pinned that a conformant 0.8 implementation could already take,
with local semantics unchanged); *S* = semantic (some outcome or
well-formedness verdict differs from some reading of 0.8, or a
capability is added). **Hash**: every entry rides on the version bump V,
which changes envelope part (1) and every signature's `abi`, hence the
hash of **every** symbol (§9.2): the four 0.8 example hashes all change
and §16.3 republishes their objects (the 0.8 vectors remain valid 0.8
vectors); "+bytes" marks an entry that also changes the canonical bytes
of functions that use the affected form; "new" marks new symbols.
Sources: *EN* = an item of the evidence note
`docs/notes/2026-10-29-isa-09-evidence.md`; *bd* = a bead of this
repository; *SQ n* = entry n of `reference-interpreter/SPEC-QUESTIONS.md`
(its reading is adopted unless the entry says otherwise); *RC* = the
reference-interpreter council round 1
(`docs/council/isa-ref-2026-10-29/round-1/report.md` in `bennett`),
member and finding; *r8* = a council round-8 suggestion (bead
`b-isa-spec-zsw.N`); *DL* = the dialect 0.2 outline's §25 list.

**No narrowing.** No entry rejects, faults, declares inert or removes a
capability that 0.8 permits or the north star promises. The entries
that add or sharpen a well-formedness check (E11's static view rule,
E16.9, E17.2, E17.3, E17.5's unmatched uncalls, E17.8, E17.9, E17.10,
E17.12, E17.14, the block terminators of K5) concern spellings that
always have a legal equivalent or uses that 0.8 did not define soundly
(E17.14: a location value as a classical argument would be superposed);
the run-time checks (E11, K1's width checks, K3's token validity, K4's
inverse-pair check) concern operations that 0.8 did not define or
already required (0.8's `qinplace` already demanded its certificates;
K4 admits library certificates as well as exhaustive claims, as the
north star §3.1 requires).

### 0.1 Group 1: repairs and pinned readings

| # | § | Change | Closes | Kind | Hash |
|---|---|---|---|---|---|
| V | title, §1.3, §6.4, §8–§13, §9.1, §9.2, §10, §16.3 | Full version string `0.9` in every sub-version, envelope part (1), every signature `abi` and every device-model version | brief | S | all |
| E1 | §3.6, §4.2 | The index space indexes **rows** (one per instruction line); a label denotes its block's first row; `qjumpr`'s range is the containing function's row indices | EN I8; bd ti2; SQ 1 | E | – |
| E2 | §3.6 | Lprocs are placed by SCC: a one-member SCC keyed by its member's closure hash, a multi-member SCC by its `scc_hash`, members consecutively in SCC index order | bd was; SQ 7; EN "SCC ordering"; RC fable s6, muse s1 | E | – |
| E3 | §9.2 | Acyclic symbols hash their own envelope; the SCC wrapper applies to cyclic SCCs, including a self-referencing singleton (pins the published vectors; r8 zsw.11 rejected) | EN ISA-10; zsw.11 | E | – |
| E4 | §16.1 | A data line with empty `HEX` is `NAME SP LF`, the sole trailing-space exception | bd oim; SQ 9 | E | – |
| E5 | §7.4 | Logical history (checkpoint/replay storage permitted); active versus audit history; an `uncall` marker is always skipped and nothing is undone twice | EN I4, I7; bd ql5; zsw.3, zsw.10 | E | – |
| E6 | §4.1 | The `uncall` summary states every §7.4 legality condition and the cancellation-aware traversal | zsw.1, zsw.9 | E | – |
| E7 | §12.1 | Invocation contexts come from the realised invocation tree, including default-covered invocations; context keys and their order are concrete | zsw.2, zsw.7 | E | – |
| E8 | §12.1 | Margin rule for numerically obtained SDP witnesses; non-normative Tr_out convention note | zsw.6, zsw.12, zsw.13 | E | – |
| E9 | §14.3 | T4 states its hypotheses (reverse eligibility, no `measure`, no unverified release) and restores *active* state | zsw.3, zsw.8 | E | – |
| E10 | §16.3, §15 | Example 3 (`borrow_demo`, an action with loop bounds and a translation-lemma borrow frame); suite D gains two SDP witness vectors | zsw.15; zsw.4 (part) | E | new |
| E11 | §3.3 | `qreg` values pass unchanged through `call`, `ret` and `br`; state belongs to the register; aliases; the exact static rule for views and repeated operands (suite F), every other overlap or use of a viewed register a run-time trap | DL "qreg across CC calls"; EN BLK-1; review of this draft | S | – |
| E12 | §3.3 | `qreg.slice` `lo` is a literal or a run-time `i64`; view state on reversal of the region call | EN ISA-5; DL "qreg.slice" | S | +bytes |
| E13 | §5.4 | Code 10 is not "R only": a lifted oracle virtualising entropy may `fault 10` | DL ISA §5.4 item; EN ISA-7 | E | – |
| E14 | §3.6, §4.2, §5.4 | **Effective cause**: a `fault 0` or triggered `lift.faultif p 0` records `FAULT_UB_TRAP` (4); no fault is ever recorded as `FAULT_NONE` | bd 7qu; EN "explicit fault code zero" | S | – |
| E15 | §3.1 | Call-tier policy as a table (CC calls CC and R; R calls R; `uncall` of CC or R segments) | RC codex B20 | E | – |
| E16.1 | §16.1 | The text form has no comment syntax | SQ 2 | E | – |
| E16.2 | §3.6 | An idle step writes `old_pc = HALT`; its inverse clears it (as printed) | SQ 3 | E | – |
| E16.3 | §3.7 | Counter widths: the reference realisation uses the minimum widths; wider counters give the same F_B | SQ 4; RC muse C4 | E | – |
| E16.4 | §14.1 | On budget exhaustion the reference interpreter has executed exactly B rows | SQ 5 | E | – |
| E16.5 | §9.1 | `devices.models` lists every §7.3 model an `effect` uses; an unmodelled device contributes no device line | SQ 6 | E | – |
| E16.6 | §10 | A host reply whose length does not fit `ptr_width` bits is refused with `E_ARG` before any write | SQ 8 | E | – |
| E16.7 | §3.3 | Fault literals in an lproc are checked against every enclosing oracle's F, again at link | SQ 10; RC muse s5 | E | – |
| E16.8 | §9.1, §9.4, §12.3, §13 | JSON encodings: type strings, program-point arrays, frame descriptor, certificate `versions`, variant identifiers, coverage field presence | SQ 11; DL "ISA-3 editorial" | E | – |
| E16.9 | §3.3 | A `const.iN`/`lift.const.iN` literal lies in [−2^(N−1), 2^N) (departs from SQ 12's modulo reading; NS §0 "never a silent wrong answer"; every value keeps a spelling) | SQ 12; RC fable R1-B2 | S | – |
| E16.10 | §16.1 | Canonical `FLOAT` spelling (RFC 8785 number rendering, `.0` appended, `-0.0`) | SQ 13; RC fable R1-B2, codex B12 | E | – |
| E17.1 | §3.3, §14.1 | `wire[N]`, `reg[N]`, cells and `qreg[n]` have no upper width bound; values are bit-vectors of any width | RC fable R1-B1, codex B01, muse B1 | E | – |
| E17.2 | §16.1 | Every integer token is a canonical `INT` (`032`, `+3`, `09` are ill-formed) | RC fable R1-B2, codex B12, muse B2 | E | – |
| E17.3 | §5.1 | The region call graph, including lifted calls and both `qinplace` callees, is acyclic | RC codex B02 | E | – |
| E17.4 | §4.7 | A caller's local `qregion` may be a region operand of a structured call | RC codex B06 | E | – |
| E17.5 | §5.5 | Matched `lift.oracle_uncall` pairs match LIFO; an intervening store is not ill-formed | RC codex B08 | S | – |
| E17.6 | §4.7 | Classical argument types `iN ptr f64 token` and how each is read in a lifted body | RC codex B10 | E | – |
| E17.7 | §3.4 | Uses need not follow definitions in block text order; a use with no current instance traps | RC codex B11 | E | – |
| E17.8 | §4.1, §9.1 | `load`/`store` take `.iN` suffixes only (no `load.ptr`); JSON numbers ≥ 2^53 are errors | RC codex B12 | E | – |
| E17.9 | §4.1 | `call` writes its arguments as bare operands (`r = call @f a b`); the parenthesised spelling is ill-formed | RC fable s2 | E | – |
| E17.10 | §9.1 | An interface region's name differs from every symbol and import name (a rename always exists) | RC fable s9, C2 | S | – |
| E17.11 | §5.1 | `in` wires may also be `qstore` value operands, memory-address operands and `qif` selectors | RC fable s10, muse B4 | S | – |
| E17.12 | §5.1 | Param role suffixes: optional on wires and equal to the group's role; required on regions | RC muse s3 | E | – |
| E17.13 | §4.2, §7.1 | `lift.free` / `free` match only unpinned entries (0.8 also cleared the live bit of a pinned size-0 global at the freed base) | RC fable s1, C3 | S | – |
| E17.14 | §4.2 | The `args` of lifted calls are classical arguments, never locations; Q14 (§0.2) supplies them to lprocs through explicit parameters | review of this draft; Q14 | S | – |
| E17.15 | §3.3, §4.2 | A lifted row's `.iN`/`.iM` suffix names a location width and has no upper bound (except `lift.load`/`lift.store`), so wide locations can be initialised and cast | review of this draft (after E17.1) | S | – |
| E17.16 | §3.6, §4.2 | `qjumpr` to an in-range index that is not a block's first row enters that row (the kept 0.8 sentence read "any other index faults" under block indexing); re-indexing preserves every reachable row index | review of this draft (after E1) | E | – |
| E17.17 | §2, §3.3, §10, §17 item 14 | **Verifying** versus non-verifying executors defined; cleanliness tests (`qreg.free`, host prepare/free) stated for both | review of this draft | E | – |
| D1 | §17 item 15, §8.2–§8.3, §11 | Routing/movement cost deferred to 0.10; optional topology and placement decided by K14 | zsw.16; b-isa-spec-wr7 | S | – |
| D2 | – | r8 suggestions: zsw.4 (controlled-action fixture published, §17 item 7), zsw.5 (citation unverified), zsw.14 (`ref` catalog published, §17 item 7) | zsw.4, .5, .14 | – | – |

### 0.2 Group 2: capability contracts

| # | § | Change | Closes | Kind | Hash |
|---|---|---|---|---|---|
| K1 | §3.2, §3.3, §4.1, §4.8, §7.4, §9.1, §10, §16.2 | **Run-time-width registers and handle lookup**: type `qreg[*]`; `qreg.new` with an `i64` count; `qreg.width`, `qreg.id`, `qreg.from_id`; a register ledger (ids executor-chosen, never reassigned); width checks at every `qreg[*]` → fixed-width transfer; `measure.iN` (also on `qreg[n]` with N = n); run-time slice `len`; `QREG` binds `qreg[*]`; ownership acquired by `qreg.from_id` lasts until CLOSED; host calls on a register another open run owns are `E_INVALID_STATE` | EN BLK-1; DL BLK-1; bd dw7 | S | +bytes |
| K2 | §3.3, §4.1, §4.8, §7.4 | **Quantum allocation in R**: `qreg.*` execute in CC and R; ledger frames and their reversal (`qreg.new` ↔ release, clean by construction; `qreg.free` ↔ re-creation with the same id); `measure` stays CC-only | EN BLK-4; DL BLK-4 | S | +bytes |
| K3 | §3.2, §4.1, §4.8, §5.1, §5.4, §7.4, §10 | **Device-minted budgets**: `budget.mint @o s h st d` in CC and R with `bennett_budget`'s checks; token validity (run-scoped, revoked by reversal); a token may be supplied to any region call of the program; an invocation executes the object's schedule only when its bindings (tuple and `params_hash` included) match, else the §11 defaults; a token is encoded in `params_hash` as its tuple | EN BLK-2; DL BLK-2; bd 4qy; bd 8wn (binding, found while drafting) | S | +bytes |
| K4 | §4.5, §5.3, §5.4, §6.1, §12.1–§12.3 | **Parametrised in-place**: `qinplace @g @ginv tk x (ins..) (mem..) (args..)`; signature compatibility; inverse-pair obligation carried by an `inverse_pairs` entry with a minimum tuple, exact `arg_tokens` tuples and an `args` domain, by an exhaustive claim (`expected: "inverse_pair"`) or a library claim (`inverse_pair_library`), covering both orientations, checked before any effect of the CC/R region call (executors check inverse-pair claims, §1.2); monotonicity in the tuple; §6.1 transfer with `ins`, `mem` cells and `other` preserved; adjoint swaps the pair and keeps the lists | EN BLK-3; DL BLK-3; bd gv7; RC codex B07, muse s4 | S | +bytes |
| K5 | §3.4, §4.1, §4.9, §5.4, §7.4, §10, §14.1, §15, §17 item 16 | **Classical fault contract (ISA-7, ratified A5)**: CC trap = R fault record = one terminal record; a cause → code table; `fault C` in CC and R (literal < 2^64, effective cause); an `effect` memory operand out of range is 7; CC/R blocks end in `br`, `ret`, `trap` or `fault`; a `FAILED` run has exactly one record (0.8: "at least one"). Round-1 follow-up (2026-10-29): exact nonzero C through the launch API, no subsequent source effect, intact reversible prefix, and explicit classical charge versus Q step-machine semantics | EN ISA-7; DL ISA-7; bd 221; RC fable C5, s4; dialect draft 0.2.1 §25.1 BLK-5, council D02-21 re-derivation, b-dialect-spec-bz6 | S | +bytes |
| K6 | §7.4, §10, §14.3 | **Reversible failed runs**: R faults are terminal; `FAILED → REVERSED` under the shared eligibility (no `measure`, no unverified free, ownership); reversal undoes the record, then the rest including open activations (an `effect`'s undo also removes its tape entry); T4 covers `FAILED` runs, the ledger entries of the registers a run created or touched and token validity, and states the exactness hypothesis for quantum state (exact when every undo is the exact inverse of its realisation, else within the declared bounds) | EN ISA-8; DL ISA-8 (terminal reading, DL §17.6); bd 0b9 | S | – |
| K7 | §3.3, §17 item 14 | 0.8's §17 item 14 default (a `FAILED` record for a condition hardware cannot test) contradicted §7.4's unverified frees: non-verifying executors release unverified and exclude `uncall` and reversal; a verifying executor records `FAULT_UB_TRAP` (host calls: `E_QREG_NOT_CLEAN`) | found while drafting; bd exc | S | – |
| K8 | §16.3, §15 | Examples 4–9 (one per new family, hand-derived results) and the suite rows for every new instruction and fault | brief | E | new |
| K9 | §8.1 | **EPS-DECADE (ratified A5)**: exact zero-based decimal accuracy bucket, domain and exact-entry prohibition; boundary witness | bennett-vm-cxg; b-isa-spec-f31 | S | – |
| K10 | §7.3 | **BLOCK-IMAGE (ratified A5)**: contiguous complete 512-byte sectors, byte order, partial-image rejection at device initialisation; witness | bennett-vm-47i; b-isa-spec-0d0 | S | – |
| K11 | §11.1, §17 item 7 | **ISA-REF-LIB (ratified A1)**. Decided serialization, envelope hash, ordinals, scratch/removable rules and decomposition set; witness only, publication gated on accepted 0.9 | bennett-vm-47t; b-isa-spec-8r4 | S | new |
| K12 | §10, §10.1, §12.3 | **LAUNCH-ESTIMATE (ratified A2)**. Resolved parameters, class-preserving resource keys, upward decimal encoding and exact certificate binding; witness | bennett-vm-hsd; b-isa-spec-c15 (open) | S | – |
| K13 | §9.2, §12.1–§12.3 | **CLAIM-REPLAY (ratified A3)**. Mandatory sampled expected relation, standalone invocation binding, canonical parameter and full-table tuple encoding; witness; sampling stays evidence | bennett-vm-clw; b-isa-spec-9uy (open) | S | – |
| K14 | §8.2–§8.3, §11, §17 item 15 | **Topology (ratified A6)**: optional ordered class vertices and undirected edges; native adjacency, scheme/placement binding; absent all-to-all; routing deferral with explicit-gate construction | b-isa-spec-wr7; b-targets-dd3; circuits b4k | S | – |
| K15 | §5.3 | **Multi-block actions (ratified B1)**: text-order unitary fragments, descriptive labels, cross-block lifetimes | b-isa-spec-2c9; circuits 7bu | E | – |
| K16 | §9.1, §9.4, §12.3 | **Frame JSON (ratified B5)**: identified slots and typed scratch/history/borrow/ancilla records, c-only width expressions, disjoint shared lifetimes | b-isa-spec-2c9; circuits 4fa; SQ 11 | S | – |
| K17 | §4.1 | **Draw ordering (ratified A5)**: FIFO draws; wire-first lexicographic outcomes, strict cumulative threshold; reference CLI witness | b-isa-spec-bas; SQ 29 | S | – |
| K18 | §0, §3.7, §4.2, §4.9, §5.4, §7.3, §8.1 | **Confirmations (ratified A4/A5)**: Q14 explicit forwarding; EPS-DECADE, BLOCK-IMAGE, ISA-7 and Q1–Q13 confirmed as applied | b-isa-spec-7u6; b-isa-spec-f31; b-isa-spec-0d0; b-isa-spec-221; b-isa-spec-2c9 | E | – |
| K19 | §11.1 | **REF-BINDING**. Typed integer/wire/body/symbol/environment bindings, lexical substitution, invocation-local ordinals and validation witnesses | b-isa-spec-cbk | S | new |
| K20 | §11.1 | **REF-QUANTUM**. Binary64 angle bits, variadic wires and full-basis matrix witnesses | b-isa-spec-8sc | S | new |
| K21 | §11.1 | **REF-IMAGE**. Bound image bytes emit unconditional LSB-ordered X leaves with an exact adjoint | b-isa-spec-afi | S | new |
| K22 | §11.1 | **REF-TEMPLATES**. Indexed typed body templates bind explicit frame actuals while retaining lexical captures | b-isa-spec-lph | S | new |
| K23 | §11.1 | **REF-LITERAL-BITS**. Exact nonnegative integer bit extraction fixes literal X emission | b-isa-spec-8r4 | S | new |
| K24 | §11.1 | **REF-ARGUMENTS**. Closure-bound positional argument vectors and exact ISA classical/token values | b-isa-spec-1a4 | S | new |
| K25 | §11.1 | **REF-DESCRIPTORS**. Ordered typed records for byte layouts and heterogeneous activation locations | b-isa-spec-1oa; b-isa-spec-evi | S | new |
| K26 | §11.1 | **REF-REGIONS**. Shape, role, origin and cell bindings preserved in closure arguments | b-isa-spec-1a4 | S | new |
| K27 | §11.1 | **REF-LIFETIMES**. Exact class actuals and shared allocation declarations across invocations | b-isa-spec-3xe | S | new |
| K28 | §11.1 | **REF-INSTRUCTION-RELEASE**. Recipe scratch follows reverse allocation order; instruction-defined release sequences remain exact, with the qinplace ordinal witness. [deps: ISA-4.5-P5, ISA-11.1-P29.S5] | b-isa-spec-82x; maintainer ruling 2026-10-31 | S | new |
| K29 | §5.3 | **QIF-ADJOINT**. Complete-expansion inverse for cross-arm lifetimes; §5.1 matches lifetimes region-wide, not arm-wise; witness: `qif p { d = qalloc any 1 } { qfree d }` recreates d before freeing it in the inverse. | INV-1 gap 2; b-isa-spec-bdv; SQ 28 | S | +bytes |
| K30 | §4.6 | **LOOP-BINDINGS**. Visit-local linear binding carry-over; witness: a body frees c then reallocates c, and the next visit uses the new c. | INV-1 gap 3; r9_mixed_loop_threads_reallocated_bindings | E | – |
| K31 | §5.3 | **MATCHED-PAIRS**. Callees, classical/token values, operand versions and effective control sets identify adjoints; witness: opaque oracle pairs under stacks [p,q] and [q,p,p] match. | INV-1 gap 4; r10_equivalent_control_sets_preserve_opaque_inverse | E | – |
| K32 | §3.7 | **LOCATION-DECLARATIONS**. Locations only in oracles/lprocs; witness: an action `regs { ghost:wire }` cannot manufacture a live wire; empty regs with bounds remains legal. | INV-2 gap 1; r11_action_regs_do_not_produce_wires | E | – |
| K33 | §3.3 | **WIRE-DISTINCTNESS**. Distinct denoted wires, not spellings; witness: w and w[0] overlap, and two w[0] operands overlap. | INV-2 gap 2; tier_arity_aliasing_and_input_roles | E | – |
| K34 | §3.3 | **REGISTER-FRESHNESS**. Fresh allocation disjoint from live/viewed registers; launch ids pairwise disjoint; witness: duplicate launch id returns E_ARG before execution, while from_id aliases remain references to one register. | INV-2 gap 3; register_handles_enforce_views_consumption_and_cleanliness | E | – |
| K35 | §3.3 | **CALL-ALIASES**. Atomic CC/R fault for overlapping qreg call slots, including control/target overlap; witness: the same id in two slots faults without consuming a view or mutating wires. | INV-2 gap 4; r4_dynamic_interface_alias_is_an_atomic_reversible_cc_and_r_fault | E | – |
| K36 | §6.1 | **REGION-PROVENANCE**. Image-relative cell version zero, perm, empty dependencies; witness: a nonzero image is the initial version, not outstanding garbage. | INV-3 gap 1; local_regions_require_explicit_restoration_and_load_pins_cell_versions | E | – |
| K37 | §6.2 | **UNDONE-CHANGES**. Matched permutation pairs with intervening basis-value preservation; witness: X on a dependency followed by X reopens the original wire binding, but any cell write invalidates its old version. | INV-3 gap 2; cleanup_windows_and_linear_lifetimes | E | – |
| K38 | §6.2 | **CLEANUP-VERSIONS**. Computation-time S and produced g versions current; witness: qcopy s then quncopy s d is legal without requiring the old zero d version. | INV-3 gap 3; cleanup_pins_predicate_versions_and_distinguishes_qif_polarity | E | – |
| K39 | §6.2 | **CLEANUP-CONTROLS**. Computing and cleanup effective control sets/versions agree; witness: compute under p, cleanup under q cannot discharge the obligation. | INV-3 gap 4; cleanup_pins_predicate_versions_and_distinguishes_qif_polarity | E | – |
| K40 | §6.2 | **OTHER-READERS**. SQ 25 outstanding-reader condition; witness: H d0; CCX d0 p d1; CX d1 t; CCX d0 p d1; H d0 cannot release d0. | INV-3 gap 5; b-isa-spec-0jo; SQ 25 | S | – |
| K41 | §6.1 | **OUTSTANDING-DEPENDENCE**. Exact residual-operator factorisation defines dependency jointly on live/interface values and phases, retaining transitive effects through cleaned scratch; witness: t still depends on d0 after d1 is cleaned, and S on d0 leaves a phase until SDG cancels it. | INV-3 gap 6; SQ 25; cleanup_adjoint_cannot_skip_an_entangling_reader | S | – |
| K42 | §5.6 | **TRANSLATION-CONTROLS**. Effective context included in every gate control set; inverse V has the same set/versions; witness: inherited p lies in X, never in a W target or B. | INV-3 gap 7; translation_lemma_checks_all_four_required_negative_patterns | E | – |
| K43 | §5.6 | **STATIC-FRAMES**. Maximality within containing qloop/qif static sequence, per lifetime; witness: outer touches and inner frame at ordinals 4–7 remain separate. | INV-3 gap 8; SQ 30; muse_r5_translation_frame_maximality_is_within_its_static_sequence | E | – |
| K44 | §4.3 | **STATIC-FREE**. qalloc version or explicit legal cleanup output at release; witness: fresh qalloc/free and H/H/free pass, H/free fails. | INV-3 gap 9; other_scratch_requires_the_exact_adjoint_but_accepts_h_h | E | – |
| K45 | §9.2 | **STRUCTURAL-OWNERSHIP**. Exact JSON owner/global keys determine closure selection; witness: oracle a excludes a.b even if its region suffix coincides. | INV-4 gap 1; r11_oracle_layout_ownership_uses_exact_names | E | – |
| K46 | §9.2 | **LAYOUT-ORDER**. Emit every structured leaf once, sorted bytewise by its JCS path; witness: both a/c.db and a.c/db survive, independently of their base values. | INV-4 gap 2; b-isa-spec-4it; SQ 31 | S | +bytes |
| K47 | §9.2, §16.3 | **INJECTIVE-PATHS**. JCS key-component arrays preserve leaf identity; witness: ["interface_regions","a","c.db"] differs from ["interface_regions","a.c","db"]. Prefer arrays: dialect §16.3 emits dotted block names and §12 Naming emits dotted temporaries; although its reference layout uses ref, no general ban on dotted oracle/region NAMEs is established, and a dot ban would narrow legal ISA names. Also disposes of INV-4 gap 5: structural selection is encoded regardless of any CC/R harm analysis. | INV-4 gaps 3, 5; b-isa-spec-ccv; SQ 31 | S | +bytes |
| K48 | §9.2 | **ENVELOPE-BOUNDARIES**. Grammar distinguishes function/data payload and suffix classes without new length fields; witness: a lhs named layout gives `layout = …`, never a layout-array line, and a data symbol named data has one payload line selected by its signature kind. | INV-4 gap 4; §16.2 grammar lemma | E | – |
| K49 | §11 | **INVOCATION-CHAINS**. Only region calls open schedule invocations; each fixed lproc row instance expands once per step and retains its enclosing oracle chain; witness: two lift.call sites with the same key share that row instance, while keys [0]/[1] remain distinct. [deps: ISA-3.7-P5, ISA-3.7-P6, ISA-11.1-P9] | INV-5 gap 1 | S | – |
| K50 | §11 | **NESTED-BUDGETS**. Each nested oracle uses its token budget, independently of its parent; witness: root B=2 and nested B=3 include nested step 3; nested B=2 excludes it. | INV-5 gap 2 | E | – |
| K51 | §11 | **NONSTEP-SELECTORS**. Absent oracle coordinates match only wildcard step/phase; witness: an action-root X matches */* but neither step 1 nor phase rev, including adjoint X. | INV-5 gap 4 | E | – |
| K52 | §11 | **SELECTOR-LEVEL**. The last oracle-call element in the entry path selects the invocation whose step/phase it reads; witness: path [] step 1 reads the root even inside nested step 3; a path ending at the nested call edge (including its instance and call_index) reads nested step 3. [deps: ISA-11-P5.S5, ISA-11-P5.S6, ISA-11-P5.S7, ISA-11.1-P9] | INV-5 gap 5 | S | – |
| K53 | §11 | **MAXIMAL-TIES**. Equal maximal lexicographic tuples at distinct array positions tie; shadowed overlaps do not; witness: duplicate C rejects; tied A/B covered by higher C (or a union of higher entries) admit in every order. | INV-5 gap 6 | S | – |
| K54 | §11 | **KIND-DOMAINS**. Gate, allocation and start decisions match only their operation classes; witness: gate and alloc entries with identical selectors cannot tie with each other. | INV-5 gap 7 | E | – |
| K55 | §11 | **TIE-CHECK-STAGES**. Admission checks known invocation domains; unknown nested domains check the first ambiguous concrete operation before its realisation; witness: unknown nested B=3 rejects at nested step 3; B=2 never generates it; a derivable B=3 rejects at admission. | INV-5 gap 9–10; b-isa-spec-6hs | S | – |
| K56 | §11 | **ENTRY-DEFAULTS**. Omitted payload fields take their defaults without inheritance from less specific entries; witness: a more-specific realisation-only gate entry uses the default share despite a broad explicit share. | INV-5 gap 11 | E | – |
| K57 | §17 item 7 | **DEFAULT-REF-BINDING**. The omitted expansion binds the object ISA version and its published library envelope hash; witness: a 0.9 object binds ref@0.9 at the §11.1 full-library hash, not the qxor witness hash. | INV-5 gap 12–13 | E | – |
| K58 | §17 item 9 | **SHARE-POPULATION**. An eps-independent exact-native test fixes N over the root expansion including nested invocations; witness: an exact native gate is excluded; three gates lacking an exact native match give N=3 even with explicit shares. | INV-5 gap 14 | S | – |
| K59 | §17 item 9 | **RATIONAL-DEFAULT-SHARE**. Exact reduced-rational resolved shares preserve §8.1 evaluation without rounding or modifying schedule bytes; witness: epsilon 0.1 with N=3 resolves to (1,30); N=0 assigns zero without division. | INV-5 gap 15 | S | – |
| K60 | §11 | **SCHEDULE-DECIMALS**. Schedule decimal values are exact rationals, independent of spelling; witness: 0, "0", "0.0" and "0.000" all denote exact zero. | INV-5 gap 16 | E | – |
| K61 | §11 | **UNCOVERED-NESTED-DEFAULTS**. Uncovered operations take defaults directly; no synthetic entry or multi-level selector is required; witness: root step 1 keeps scheme X while an uncovered root-step-2/nested-step-1 gate takes its default. | INV-5 gap 17 | E | – |
| K62 | §5.3, §11.1 | **SCHEDULED-ACTION-ADJOINT**. Source instruction replacements precede recipe instantiation; witness: adj(qinplace G H) allocates t[1] at 0 and f[4] at 1, calls H then G and releases t then f. [deps: ISA-5.3-P4, ISA-4.5-P5, ISA-11-P2, ISA-11.1-P29] | SOL09-R1-B01 | S | library |
| K63 | §9.2, §11, §11.1, §12.1 | **INVOCATION-EDGE-IDENTITY**. Serialize fixed-binding instance and forward semantic-call occurrence independently of leaf ordinals; witness: qinplace G G has call_index 0/1; lproc keys [0]/[1] have distinct contexts. [deps: ISA-3.7-P5, ISA-3.7-P6, ISA-9.2-P1.S3, ISA-11.1-P9, ISA-12.1-P11] | COD-R1-B01; SOL S2 | S | – |
| K64 | §11 | **NON-ROW-ADDRESSES**. Reserved support points and their source/step/callee partition define every non-row ordinal; witness: B=0 has construction/commit/release and B=1 starts step support at allocation at, ordinal 0. [deps: ISA-3.6, ISA-5.2-P3, ISA-11.1-P22, ISA-11.1-P29] | INV-5 gap 3; 8ka; ratified by the maintainer 2026-10-31 | S | – |
| K65 | §11 | **WHOLE-CLEANUP-CARRIER**. One non-emitting ordinal-0 carrier selects the whole explicit cleanup before expansion, even if empty; witness: reverse/recompute for quncopy share one carrier. [deps: ISA-6.2-P1, ISA-6.4-P1, ISA-11-P6] | INV-5 gap 8; 23g; ratified by the maintainer 2026-10-31 | S | – |
| K66 | §9.2, §11, §11.1, §12.1 | **DEPENDENCY-ACCURACY**. Retarget release, matching, staging, construction and replay declarations to their semantic premises; witness: K28 cites ordinal/scratch P29 rather than activation P21. [deps: ISA-11.1-P29, ISA-11-P5, ISA-11-P6, ISA-11-P7, ISA-9.2-P4, ISA-12.1-P7] | SOL S1; COD S01/S02 (targeted) | E | – |
| K67 | §12.1 | **LEGAL-REPLAY-WITNESS**. F=4 and W=8 with legal unused mapping give a 25-bit domain; witness: four singleton draws cover 1/33554432 with unchanged XOR outcomes. [deps: ISA-5.4, ISA-7.1, ISA-7.2, ISA-12.1-P8, ISA-12.2] | COD S03 | E | – |
| K68 | §5.3 | **ACTION-DOMAIN**. Include both region roles in the unitary and D; witness: an unchanged two-cell one-bit `in` region still contributes four configurations. [deps: ISA-5.1-P1, ISA-5.2-P4, ISA-3.3-P19, ISA-5.6-P1, ISA-14.2] | INV-6 gap 1; afu | E | – |
| K69 | §12.2 | **COMPONENT-COVERAGE**. Resolve interface names to group/slot/cell identities and require every full range for exhaustive proof; witness: full explicit cell lists cover D, but borrowed `t` cannot cover omitted mut slot t. [deps: ISA-5.1-P1, ISA-9.4-P2, ISA-3.3-P19, ISA-5.2-P4, ISA-5.3-P1, ISA-12.1-P8, ISA-14.3-P3] | INV-6 gap 2; SOL-R22-B01; afu | S | – |
| K70 | §12.2 | **BORROWED-POSITIONS**. Borrow entries denote checked lifetimes by position with label-only names; witness: borrowed labels t and b give the same four-element CNOT slice. [deps: ISA-4.3-P2, ISA-5.6-P1, ISA-12.1-P8] | INV-6 gap 3; afu | E | – |
| K71 | §12.2 | **OMITTED-ZERO-SLICE**. Hold omitted components at zero and count the resulting slice; witness: omitting t from three independent bits yields 4/8 coverage. [deps: ISA-5.2-P4, ISA-5.3-P1, ISA-12.2-P1] | INV-6 gap 4; afu | S | – |
| K72 | §12.2 | **DOMAIN-VALIDITY**. Validate unique resolved components, widths, bounds and cell indices; witness: duplicate cell 1, width 2 for a one-bit slot and index 2 for region[1,1] reject. [deps: ISA-3.3-P2.S2, ISA-3.3-P19, ISA-12.2-P1] | INV-6 gap 5; afu | S | – |
| K73 | §12.1 | **EXPECTED-CORRESPONDENCE**. Compare programs by ordered roles, shapes and borrow positions; witness: crossed local names on two equal-width slots do not exchange those slots. [deps: ISA-5.1-P1, ISA-9.4-P2, ISA-12.1-P7, ISA-12.1-P8] | INV-6 gap 7; afu | E | – |
| K74 | §12.2 | **CHECKER-VERDICT**. The checker records per-claim labels and counts in its report, never trusting a requested label; witness: the four-element CNOT slice reports evidence with count 4 and fraction 1/2. [deps: ISA-1.2-P4, ISA-12.1-P1, ISA-12.1-P2, ISA-12.1-P8, ISA-12.3-P1] | INV-6 gap 10; afu | S | – |
| K75 | §12.2 | **UNCHECKED-HOST-LIMIT**. Report host exhaustion separately from labels and rejection without a domain cap; witness: region[63,1] at count 1 remains legal even when one element cannot be stored. [deps: ISA-3.3-P2.S2, ISA-3.3-P19, ISA-12.1-P2, ISA-12.2-P1, ISA-5.6-P2, ISA-14.3-P3, ISA-12.3] | INV-6 gap 12; afu | S | – |
| K76 | §5.6 | **FRAME-ENTRY-DOMAIN**. Normative constant and causal-adjoint analysis fixes D_F; interface/borrowed components stay independent and full; checker establishes reachable-entry support before restricted T3 factorisation. Witness: CX(0,b) passes, polynomial-only prefix zero does not. | consumer 73y; pass V; SQ 20 | E | – |
| K77 | §4.7, §11.1, §16.2 | **ORACLE-INVOCATION-CONTEXT**. Explicit typed source-call token context is captured outside the declared argument vector, forwarded through adapters and retained under inverse traversal; each linked oracle construction uses its own tuple. Witness: the same inc8 closure and arguments at B=2 and B=3 in one expansion. | consumer 5xm; pass VII | S | – |

**Decided Q14 (applied 2026-10-29, confirmed 2026-10-30; b-isa-spec-7u6).** Lprocs take explicit
token and classical parameters (§3.7, §4.2, §4.7, §16.2), forwarded by
`lift.call`; mapped-region parameters preserve the complete lifted-call
interface. Fixed binding instances (§3.6–§3.7) keep those arguments
classical under coherent calls, without an extra budget charge (§5.4).
The interface and its hash include the new groups (§9.1–§9.2); §15 and
§16.3 example 10 supply conformance obligations and a witness. Source:
the maintainer's acceptance recorded as "the Q14 edit (lproc
token/classical params)" in the "interpreter milestone 1" session,
`worklog/001_2026-10-28_bootstrap.md` line 26; the orchestrator's
2026-10-29 decision selects explicit parameters. The maintainer's
2026-10-30 ratification confirms this reading: lproc header groups are
`(params)(result)(tokens)(classical)(mem)` and `lift.call` forwards tokens,
classical arguments and mapped regions.

**Decided confirmations (2026-10-30).** The maintainer ratified EPS-DECADE
(K9), complete-sector BLOCK-IMAGE (K10), the reference CLI draw ordering
(K17), ISA-7 `fault C` and its fault-code table (K5), and Q1–Q13 as
already applied. These decisions are recorded in the maintainer memo,
Ratification section, 2026-10-30. Q12 keeps the §16.3 draft example
hashes computed by the 0.9 precheck; independently checked target/frame witness hashes
are published in §8.3 and §9.4.

### 0.3 Group 3: optional efficiency semantics (deferred)

| # | § | Change | Closes | Kind | Hash |
|---|---|---|---|---|---|
| P1 | §17 item 17, §3.6 | Identity-idle step (old index encoded as k ⊕ HALT, idle frames zero), deferred with the printed step as default and its normative hook | EN I5; bd roy | E | – |
| P2 | §17 item 18, §5.7, §9.4 | Checkpointed and pebbled oracle realisations, deferred with full history as default and the expansion-library hook | EN I1; bd 9c3 | E | – |

**Considered and deferred** (efficiency in the evidence note; no 0.9
text; the capability is kept by the stated construction, so no rung and
no north-star promise depends on the deferred primitive):

| Item | Construction that keeps the capability |
|---|---|
| ISA-2 (R-tier budget) | an R step counter threaded through the code; exhaustion is now `fault 1` (K5) |
| ISA-5 (two simultaneous slices) | one action on the parent register (e.g. `cx q[0] q[7]`); run-time indices by dispatch or by run-time slice `lo` (E12) |
| ISA-6 (non-consuming measurement) | CNOT copy of the wires into a fresh register, then `measure` of the copy; the original keeps its id |
| ISA-9 (borrowing driven from CC) | a clean allocation, or a Q region with its own borrow frame |
| ISA-11 (host memory at native addresses) | promotion of the pointer-sharing callers to CC (`alloc`, `hostcall` for genuine host effects) |
| G-12 (run-time snapshot at native addresses) | replay every allocation in bump order (dead and zero-size ones included) and copy the bytes |
| G-13 (interface base chosen at call time) | static arenas and explicit logical-to-physical address translation rows |
| G-14 (step machine inside actions) | bounded, padded structured expansion with immutable selectors |
| G-15 (payloads wider than 128 bits) | realised directly: `tgt`, `reg[N]` and `result_val` have no width bound (E17.1), and lifted suffixes name location widths (E17.15) |
| G-16 (fibers, interrupts) | explicit continuation records in memory and polling at defined points |
| I2 (bounded-loop recovery) | §5.7 structure recovery with immutable selectors or retained history |
| I3 (budget provenance) | host tuple or bounded wrapper; dialect documentation |
| I6 (step-granular oracle interface) | whole-oracle budget ladders of region calls |
| SQLite E1–E5 | logical stack and frames as specified; compare tree plus static `lift.call`; a copy lproc; classical-data specialisation under §5.7 |
| measuring registers wider than 128 bits (bd 04w) | copy 128-bit slices to fresh registers, measure the copies, reset the source wire by wire with run-time slices |

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
| Executor | VM, specialiser, hardware stacks | §3–§7, §14 exactly, and the checking of inverse-pair claims (§4.5, §12.1; a certificate applies when its `closure_hash` binding equals the region's); suites A–E, H |
| Producer | plugin, library compilers | well-formed objects (§9, §16) and regions (§5, §6); suite F |
| Scheduler | `bennett-sched` and competitors | §11; only schedules valid under §6; suite H |
| Checker | `bennett-conformance` | validates certificates (§12) without trusting producers |
| Target author | vendors | target descriptions (§8); suite E |

### 1.3 Deferred *(asserted non-semantic)*

Binary encodings (§16 text is the interchange form); mechanisation of
§14; device models beyond §7.3; the gate-name registry process; the
memory layout of the opaque C objects of §10–§11 (every constructor,
accessor and destructor is listed). **Minimality claims** (north star
§5) are not supported by cert 0.9 and MUST NOT appear in a certificate.
Decisions deferred to implementation, each with its default, are listed
in §17.

## 2. Terminology

- **Tier.** CC, R, Q. **Wire**, **bundle** `wire[N]` (little-endian).
- **Location** `reg[N]`: a named mutable cell of an oracle or lproc
  register file. **Pseudo-location**: an oracle interface input or
  classical argument, or an lproc classical parameter (§3.7), readable
  only in its declaring function, never written.
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
- **Verifying executor**: an executor that can decide exactly whether a
  set of wires is clean on every basis configuration (a state-vector or
  branch-enumeration simulator); every other executor (hardware) is
  **non-verifying**. Rules that depend on the difference say which
  applies (§3.3 `qreg.free`, §10, §17 item 14).
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

**Call-tier policy** (suite F). The diagram, completed with same-tier
calls; a call, uncall or region call outside this table is ill-formed:

| Caller | `call` (§4.1) | `uncall` of a completed segment (§7.4) | region calls (§4.7) | lifted calls (§4.2) |
|---|---|---|---|---|
| CC function | CC and R functions | of a CC or R callee | oracles, actions | – |
| R function | R functions | of an R callee | oracles, actions | – |
| oracle body, lproc | – | – | – | `lift.call` of lprocs; `lift.oracle_call`/`lift.oracle_uncall` of oracles; `lift.perm_call` of permutation actions |
| action | – | – | oracles, actions (§5.3, §5.5) | – |

An R function never calls a CC function: CC code may measure and make
host requests (§4.1), which an R history cannot reverse.

### 3.2 State

| Component | Tier | Contents |
|---|---|---|
| classical environment | CC, R | dynamic SSA instances (§7.4), block parameters, activation stack, **quantum-register handles** (`qreg[n]`, `qreg[*]`, §3.3), tokens (§5.4) |
| register and token ledgers | CC, R | every register's id, class, width and state (§3.3); every device-minted token's tuple and validity (§5.4) |
| classical memory | CC, R | byte-addressed, little-endian, sparse; allocation table (§7.1) |
| effect tape, entropy tape | R | §7.3 |
| run history | CC, R | one frame per executed instruction (§7.4) |
| wire store | Q (CC and R via `qreg`) | live wires with roles `input target fault borrowed mutable workspace location cell` |
| quantum memory | Q | regions of `wire[W]` cells: local (§4.6) or interface (§5.1) |
| register file | Q | locations of the active oracle and its lproc closure (§3.7) |
| predicate stack | Q | wires; the active predicate is their conjunction |
| oracle step state | Q | `pc, pc' : wire[P]`; `faulted : wire`; `code : wire[F]`; `result_val : wire[T]`; counters (§3.7); B frames |
| budget | Q | classical: B, heap_limit, stack_limit, depth_limit |

### 3.3 Types, ownership, operand schema

```
  iN (1 ≤ N ≤ 128)   ptr (width ptr_width)   f64   token   qreg[n]   qreg[*]   region[A,W]
  wire   wire[N]      linear values in structured code and interfaces
  reg[N]              a location (oracle bodies, lprocs); not linear
```

**Widths.** The bound 1 ≤ N ≤ 128 applies to the type `iN` only (a lifted
row's `.iN` suffix names a location width, §4.2). `wire[N]`,
`reg[N]` and `qreg[n]` have N, n ≥ 1 and `region[A,W]` has A ≥ 0, W ≥ 1,
with no upper bound (a `qreg[*]` register's width is a run-time value n
≥ 0, §3.3 below); a value of these types is a bit-vector of its
width in every semantics (§14.1), including interface bundles,
pseudo-locations, locations, cells, stack cells and frame slots.

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
Distinctness is judged on the wires denoted: a bundle and an indexed
operand of it, or two indexed operands denoting the same wire, overlap
and are not distinct. [deps: ISA-3.3-P3, ISA-4.4]

**Per-opcode operand schema** (§4.8): every opcode has a tier set, a
fixed arity, operand kinds and a result type; results are written first
(`w = op a b`), modes are never written, and **result types that are not
determined by the operands are written as a suffix** (`r = const.i32 5`,
`r = zext.i64 a`, `r = trunc.i8 a`, `r = ptrtoint.i64 p`, `p = inttoptr
a`). Width rules: `binop`/`icmp` operands equal width; `select` arms equal
width; `zext`/`sext` strictly widen, `trunc` strictly narrows; `load.iN`
and `lift.load.iN` require N ∈ {8, 16, …, 128}; `measure` of `qreg[n]`
with n ≤ 128 yields `in`, and `measure.iN` (1 ≤ N ≤ 128) of a `qreg[*]`
yields `iN`; signed division truncates toward zero. The
literal c of `const.iN c` and `lift.const.iN c` satisfies −2^(N−1) ≤ c <
2^N and denotes c mod 2^N (both the signed and the unsigned spelling of
every value are accepted); any other literal is ill-formed (suite F).

**Lifted width rules** (suite F; a mismatch is ill-formed, never a
truncation or an extension). Every address operand (`a` of `lift.load`/
`lift.store`, `p` of `lift.boundscheck`/`lift.free`) and every address
result (`w` of `lift.addr`/`lift.alloc`) is `reg[ptr_width]`; the length
`n` of `lift.alloc`/`lift.boundscheck` is a location of any width or a
literal in [0, 2^ptr_width); `inrange` and every prospective sum are
computed at width max(widths of the operands involved) + 1 with no wrap.
The destination of `lift.label` and the operand of `qjumpr` have any
width N with 2^N > n (the index-space size). `lift.call` location
arguments have exactly the callee's parameter widths and its destination the callee's
result width; its token, classical and region lists match the callee's
corresponding groups in count, order and type (§3.7); `lift.ret v` has
the containing lproc's result width;
`lift.oracle_call`/`lift.oracle_uncall`/`lift.perm_call` operands have
exactly the callee signature widths, and `mem` operands name caller
regions whose `[A,W]` equal the callee's and whose role is `in` for an
`in` slot (an `in` region is never passed to a `mut` slot); `fault C` and
`lift.faultif p C` require the literal C < 2^F, where F is the fault
width of the containing oracle or, in an lproc, of every oracle whose
lproc closure contains it (checked at load and again at link; an lproc
in no oracle's closure is checked when linked into one); the width rules above
for `binop`, `icmp`, `select`, `zext`, `sext`, `trunc` apply verbatim to
their `lift.*` counterparts; the destinations of one `lift.parmov` are
pairwise distinct.

**Quantum registers in CC and R.** A **register** is n device-resident
wires of one class with a nonzero 64-bit **id**, recorded in the
program's **register ledger** with its class, width and state:
**live**, **viewed** (one slice of it is live) or **consumed**.
`qreg[n]` is the type of a register whose width n is fixed statically;
`qreg[*]` the type of a register whose width is known only at run time
(an unsigned 64-bit n ≥ 0). A `qreg[n]` value may be used wherever a
`qreg[*]` is expected; a `qreg[*]` value bound to a `qreg[n]` parameter
or block parameter (`call`, `br`, `ret`, launch) or to a slot of width n
(region call, §4.7) is checked at that transfer: its width MUST equal
the required one. The `qreg.*` instructions execute in CC and R;
`measure` only in CC. An instruction whose precondition fails is a CC
trap / R fault (§4.9) with code `FAULT_UB_TRAP` unless the table says
otherwise, and has no effect. An id's value is chosen by the executor
(the suites compare ids only for equality); an id is never reassigned to
another register while the program is loaded. **Handle transitions:**

| Instruction | Precondition | Effect |
|---|---|---|
| `q = qreg.new cls n` | `n` a literal n ≥ 1 (q: `qreg[n]`) or an `i64` value read unsigned, 0 included (q: `qreg[*]`); the device can provide n wires of class `cls`, else code `FAULT_BUDGET_HEAP` | q live, clean, with a fresh id and wires disjoint from every live or viewed register. [deps: ISA-3.3-P7] |
| `qreg.free q` | q live, not a view, clean on every basis configuration (a verifying executor checks it; on failure q stays live and unchanged; a non-verifying one: §17 item 14) | q consumed |
| `q2 = qreg.slice q lo len` | q live, not a view; `lo` and `len` each a literal (`len` ≥ 1) or an `i64` value, both unsigned; lo + len ≤ n, computed without wrap (a trap even when literals make the failure evident) | q2 a view of wires [lo, lo+len) of q, of type `qreg[len]` for a literal len and `qreg[*]` otherwise; q viewed; q2 MUST be the operand of exactly one region call and of nothing else; after that call q2 is consumed and q is live again; a use of q while it is viewed traps (the static rule below covers the cases suite F rejects). Reversing that region call (§7.4) restores q viewed and q2 live; reversing the slice frame then restores q live |
| `q = qreg.concat q1 q2` | q1, q2 live, not views, distinct registers | q1, q2 consumed; q live, with a fresh id, over the wires of q1 then q2; `qreg[n1+n2]` if both operands are static, else `qreg[*]` |
| `w = qreg.width q` | q live, not a view | w: `i64`, the width; no state change |
| `id = qreg.id q` | q live, not a view | id: `i64`, the bits of q's id; no state change |
| `q = qreg.from_id id` | `id` is the id of a register of the program that is live, not a view, and not owned by another run that is not CLOSED (§10) | q: `qreg[*]`, an alias of that register; no ledger state change; the run now owns the register (§10), which reversal does not undo (ownership ends when the run is CLOSED) |
| region call (§4.7) with q as operand | q live (a view included); its width equals the slot's (§3.3 binding); the wire sets filling distinct wire/region slots are pairwise disjoint, and an explicit control is disjoint from targets and consumed/produced operands (read-only input overlap remains allowed), else CC trap / R fault FAULT_UB_TRAP before any effect, including any view consumption. [deps: ISA-3.3-P4, ISA-4.7, ISA-4.9] | q unchanged. [deps: ISA-4.7] |
| `r = measure q` / `r = measure.iN q` | q live, not a view; the form `measure.iN` (1 ≤ N ≤ 128) for a `qreg[*]`, whose width MUST be N (checked before measuring); for a `qreg[n]` either `measure` or `measure.iN` with N = n (checked statically) | q consumed, its wires released; r: `in` / `iN` |
| reversal of a `qreg.*` frame (§7.4, §10) | – | the ledger state before that frame (below). A `measure` frame is **never reversed**: a segment containing one cannot be uncalled (§7.4) and a run containing one is not reversible (§10) |

**Ledger frames and their reversal** (§7.4). A `qreg.new` frame records
the id, class and width; its reversal releases that register without a
test: every later frame touching it has been undone first (LIFO) and the
run owns it exclusively (§10), so under T4's exactness hypothesis it is
clean, and otherwise its residual, within the declared bounds of the
undone realisations (§12.3), is discarded with it.
A `qreg.free` frame records the id, class, width and whether its
cleanliness was verified; its reversal re-creates the register clean and
live with the same id, class and width (every alias sees it live
again). A `qreg.slice` frame records the parent id, lo and len, a
`qreg.concat` frame the two operand ids and the new id; their reversal
restores the exact prior states and wire order without moving, copying
or measuring a wire. `qreg.width`, `qreg.id` and `qreg.from_id` change
no ledger state and their frames are pure (§7.4); if an `uncall` later
removes the register an alias refers to, every use of the alias traps.

**Binding**: a register of width n (`qreg[n]`, or `qreg[*]` of run-time
width n) fills a `wire[n]` slot bit for bit (bit 0 ↔ wire 0); it fills a
`region[A,W]` slot iff n = 2^A·W with cell i = bits [iW, (i+1)W); for a
`qreg[*]` the width is checked at the call, before any effect.
Host-supplied register ids are `qreg` values of the parameter's type.

The register ids supplied as arguments of one `bennett_run` MUST
denote pairwise disjoint registers, else `bennett_run` returns `E_ARG`
before executing the entry function or acquiring any register ownership.
[deps: ISA-3.3-P7, ISA-10]

**Registers, handles and aliases.** A `qreg` value is a reference to a
register of the device; the state live / viewed / consumed belongs to
the register, not to a name. `qreg` values pass unchanged as `call`
arguments, `ret` values and `br` block arguments (each transfer binds
another name to the same register and changes no state; a `qreg[*]`
reaching a `qreg[n]` parameter is width-checked, above). Two names bound
to one register (by such transfers or by `qreg.from_id`) are
**aliases**: a transition
made through either is observed through both. The wire operands of one
region call, with its effective control context, MUST denote pairwise
disjoint wires (§3.3 disjointness); aliases violate it. **Static and
run-time verdicts.** Suite F rejects exactly: two `qreg` operands of one
region call or of one `qreg.concat` that are the same name; and, on some path from a
`qreg.slice`, a use of the view's name other than as the operand of one
region call (a `br`, `call` or `ret` transfer included), its reaching a
`ret` or the end of the function unconsumed, or a use of the slice's
parent operand name before that call. Every other overlap, and every
use of a viewed register through another name, is a CC trap / R fault
with code `FAULT_UB_TRAP` before any effect.

### 3.4 Execution in CC and R

Sequential small-step execution with an instruction pointer, block
parameters instead of phi nodes, dynamic control flow and allocation;
every executed instruction pushes a run-history frame (§7.4).

**Names and definitions.** Every name used in a CC or R function is a
parameter, a block parameter or the result of at least one defining
instruction of that function, and all its definitions give it one type
(suite F). The text order of blocks is irrelevant: a definition need not
precede its uses textually. Executing a use of a name that has no
current instance (none was created on the executed path, or an `uncall`
removed it, §7.4) is a CC trap / R fault `FAULT_UB_TRAP`. Every CC or R
block ends in `br`, `ret`, `trap` or `fault` (suite F); `trap` and `fault`
end the run (§4.9).

### 3.5 Predication

Every Q instruction with unitary semantics executes controlled on the
active predicate. `qpred w` pushes, `qunpred w` pops the same wire; the
stack is empty at region entry and exit. Allocation, borrowing, release,
region creation and image gates are **unconditional**; only gates
(including those inside copy/XOR/exchange/memory instructions) are
controlled.

### 3.6 The predicated step machine

**Index space.** `I[0..n)` = the **rows** (one index per instruction
line) of the oracle's blocks, blocks in text order and rows in text
order within each block; then the rows of every lproc in its **lproc
closure** (transitively reachable through `lift.call`, linked ones
included), placed as follows: partition the closure into its SCCs
(§9.2); a one-member SCC's **order key** is its member's closure hash, a
multi-member SCC's order key is its closure `scc_hash`; SCCs are placed
in increasing bytewise order of their keys (64-hex), the members of a
multi-member SCC consecutively in SCC index order; each lproc's binding
instances (§3.7) consecutively in binding-key order, each instance's rows
in block text order as for the oracle. The oracle and each lproc
instance therefore occupy a contiguous range of indices, and a **label
`^b` denotes the index of the first row of block b**. `HALT = n`; 2^P > n. Branch and call
targets are labels; `w = lift.label ^b` is the only way a location
obtains an index value; executors MAY re-index dispatch extensionally
**provided every label value observable through `lift.label` keeps its
canonical numeric value and a `qjumpr` to any in-range index reaches the
row that canonical index names**. **Terminators**: `qjump qbranch qjumpr lift.
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
flag`, `code ^= flag·C′` after their other effects, where C′ is the
row's **effective cause** (§5.4: C′ = C, except C′ = `FAULT_UB_TRAP`
when a `lift.faultif` literal C is 0).

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

On an **idle** step (pc = HALT at its start) no row executes, step 3
XORs `HALT` into `pc'`, and step 4 leaves pc = HALT and `frame_t.old_pc` =
HALT; the inverse step clears it. (A variant that leaves idle frames at
zero is deferred, §17 item 17.)

**Inverse machine step** (prefix reversal runs it for t = B..1), in
this order:

1. Recompute every `at_k` from `frame_t.old_pc`.
2. `qexch pc' frame_t.old_pc`; `qexch pc pc'` (restores the old `pc`;
   `pc'` again holds the successor value; `old_pc` is clean).
3. For each k < n under `at_k`: XOR the row's successor into `pc'` again,
   using `frame_t.flag` / `frame_t.succ`; under `at_HALT`: XOR `HALT` into
   `pc'` (`pc'` is now clean).
4. For each k < n in **reverse index order** under `at_k`: undo the fault
   writes (`faulted ^= flag`, `code ^= flag·C′`); then undo the row's
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
location of that lproc; nothing else. Token and region parameters are
usable only in their operand kinds below, not as bit-vector locations.
A written operand is a location of the containing function. Globals and
mapped interface regions are reached only by address: `w = lift.addr @g`. Lprocs receive everything
else as parameters.

An oracle declares `regs { … }`; an lproc declares five header groups:

```
  lproc @f (params..) (result) (tokens..) (classical..) (mem..)
```

The first group consists of `reg[N]` parameters, the second of exactly
one `reg[T]` result location; the third consists of `token` parameters,
the fourth of `iN`, `ptr` or `f64` parameters, the fifth of `region[A,W]`
parameters with role `in`. Token and classical parameters are immutable;
their optional role suffixes are `token` and `classical` respectively
and MUST agree with their group (§16.2). They are not locations, stack
cells or frame slots. Classical parameters can be read as
pseudo-locations (§4.7); tokens cannot be read as bits or constructed
from them. Region parameters name the passed mapped regions, not copies
of their cells. Names in all groups and `regs` are distinct.

**Argument binding.** The complete call form is
`w = lift.call @f (a_1..a_m) (tokens..) (classical..) (mem..)`.
The first list supplies the location parameters using the capture and
bind steps below. The token and classical lists supply parameters from
the calling oracle's `args`, or from the calling lproc's token and
classical parameters, with exactly matching types. A location (including
a `reg[N]` parameter), an input wire or a literal cannot supply either
list. The region list supplies mapped interface regions of the calling
oracle, or region parameters of the calling lproc, with matching `[A,W]`
and `in` role. Thus the enclosing oracle passes all three lists
explicitly; a recursive or other lproc call forwards them explicitly.
The original form `w = lift.call @f (a_1..a_m)` is canonical exactly
when all three additional groups are empty; otherwise all four lists
are required, including empty ones.

**Fixed binding instances.** For one oracle invocation, resolve those
three lists transitively to the oracle's entry arguments and mapped
regions. An instance is a pair (lproc, binding key); its key is the
concatenation of the zero-based oracle `args` positions supplying its
token parameters, then its classical parameters, then the zero-based
oracle `mem` positions supplying its region parameters. Compare keys
lexicographically as integer sequences. Starting from calls in the
oracle body, close this set under calls in every reached instance;
only finitely many keys exist, even with recursion, since no call
constructs new token, classical or region bindings. Distinct keys stay
distinct even when entry values are equal. An lproc with no such
parameters has the single empty key, preserving its previous indexing.

The index space (§3.6), locations and labels are instantiated per key.
A call targets the callee instance selected by its resolved key; labels
and `qjumpr` ranges are local to the containing instance. All instance
bindings are classical and fixed before oracle entry; reaching a call
under a wire predicate only predicates its existing row operations.
No classical binding changes as a result of quantum control. Different
coherent paths may call the same lproc with different bindings: they
reach distinct instances, each using its own fixed arguments. This is
the reference semantics; executors MAY share their storage or inline
instances only extensionally (§5.7).

Each instance declares its own `regs`. All locations are clean at entry.
The oracle's `result_val : wire[T]` (T = the `tgt` width) is step state,
initially 0.

**Counters and sizes.** Size exponents: `mem` 2^H byte cells, `alloctab`
2^A_tab entries, stack 2^S_cells cells. Counter widths: `heap_used :
wire[Hc]`, Hc ≥ H + 2; `atop : wire[Ac]`, Ac ≥ A_tab + 1; `sp, fp :
wire[Sc]`, Sc ≥ S_cells + 1; `depth : wire[Dc]`, Dc ≥ ⌈log₂(depth_limit +
2)⌉. Every prospective sum (`heap_used + max(n,1)`, `sp + R_f`, `depth +
1`) is computed at width max(operand widths) + 1 before comparison, with
no wrap. `bennett_budget` rejects limits that do not fit (§5.4). The
layout fixes no counter width: the reference realisation uses the
minimum widths Hc = H + 2, Ac = A_tab + 1, Sc = S_cells + 1 and Dc =
⌈log₂(depth_limit + 2)⌉ (Dc from the invocation's budget). Every reachable
counter value fits them (heap_used ≤ heap_limit ≤ heap_limit_max < 2^H,
atop ≤ 2^A_tab, fp ≤ sp ≤ stack_limit ≤ 2^S_cells, depth ≤ depth_limit ≤
2^Dc − 2, each counter advancing only when its flag is clear), so an
executor MAY use wider counters with the same F_B (§5.7); `W_cell` below
uses the reference Sc.

**Initial allocator state** (oracle entry): `heap_used = 0`, bump =
`heap_base`, `atop` = number of pre-entries, `sp = fp = 0`, `depth = 0`,
`alloctab[0..atop)` = one pinned live entry per global in `layout.
globals` order then per mapped interface region in `layout.interface_
regions` order, storage of `mem` all zero except global images.

**Locations and the result name.** Locations of a function are numbered
in declaration order: an oracle's `regs`; for an lproc instance its
`reg[N]` parameters, then its **result name** (`(r:reg[8])` declares a
location `r` of the lproc, written like any location and read by `lift.ret`), then its
`regs`. Every location of the oracle and its instantiated closure has
a global id (Did bits: index-space order of instances, then declaration
order). `L_f` = all locations of the selected instance of `@f`, m′ =
|L_f| (`reg[N]` params + 1 + regs for an lproc); token, classical and
region parameters contribute no locations or stack cells; **R_f = 3 + m′**
cells; cell width W_cell = max(P, Sc, Did, W_max) with W_max the widest location width in the closure. A location
of width N exchanged with a cell exchanges the cell's low N bits; the
cell's remaining bits stay clean.

**`w = lift.call @f (a_1..a_m) (tokens..) (classical..) (mem..)`.**
Resolve the fixed callee instance above; m counts only location
arguments. flag := (depth + 1 > depth_limit) ∨
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

Successor: the entry label of the selected instance of `@f`. **Inverse** (§3.6 step 4, after the
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
one step each. Forwarding or resolving the fixed token, classical and
region bindings adds no rows, capture slots or stack cells. A nested
`lift.oracle_call`/`lift.oracle_uncall` is one outer row and executes the
callee with its own token's tuple; its internal rows do not decrement
the outer B. `lift.perm_call` is likewise one outer row. Executors MAY
inline extensionally. Suite B runs one
forward `lift.call` step and one forward `lift.ret` step of a recursive
call, each followed by its inverse, and asserts that the complete
pre-step tuple is restored and every frame field is clean.

Only oracles and lprocs declare locations, and every `regs` entry in
them has type `reg[N]`; the `regs` list of an action, permutation
action, CC or R function MUST be empty (an action's empty list may
still carry `bounds`). [deps: ISA-3.3-P1, ISA-3.7-P1, ISA-16.2]

## 4. Instruction set

### 4.1 Classical control (CC, R)

| Instruction | Form | Semantics |
|---|---|---|
| `const` | `r = const.iN c` | |
| `add sub mul and or xor shl lshr ashr` | `r = op a b` | wrap; shift ≥ N → 0 |
| `udiv urem sdiv srem` | `r = op a b` | divisor 0 or signed MIN/−1: CC trap; R fault record (`FAULT_UB_DIV0` / `FAULT_UB_SDIV_OVERFLOW`, §4.9) |
| `icmp` | `r = icmp.{eq,ne,ult,ule,slt,sle} a b` | |
| `select` | `r = select p a b` | |
| `zext sext trunc` | `r = op.iM a` | |
| `ptrtoint` / `inttoptr` | `r = ptrtoint.iM p` / `p = inttoptr a` | zero-extend/truncate to M / to ptr_width |
| `load` / `store` | `r = load.iN addr` / `store.iN addr v` | N/8 bytes little-endian, unaligned; outside every live allocation: CC trap / R fault record. The suffix is always `.iN` with N ∈ {8, 16, …, 128}: there is no pointer-typed load or store (a pointer is stored as `ptrtoint.iM` with M = ptr_width and reloaded with `inttoptr`) |
| `alloc` / `free` | `p = alloc n` / `free p` | §7.1 |
| `br` | `br ^b(args)` / `br p ^b1(args) ^b2(args)` | parallel block-parameter assignment |
| `call` / `ret` | `results = call @f args` / `ret vals` | arguments and values are bare operands (`r = call @f a b`, `(r1, r2) = call @f a`, `call @f`, `ret v`, `ret`); results bind in order; a parenthesised argument list is ill-formed for `call`; callee tiers per §3.1 |
| `uncall` | `uncall @f (args) (results)` | **segment uncall**, legal exactly under §7.4: the most recent completed call segment of the history is a call of `@f` whose recorded boundary argument and result values equal the current operand values, every frame after it is pure, and it contains, at any nesting depth, no `measure` frame and no `qreg.free` frame whose cleanliness was not verified; otherwise CC trap / R fault `FAULT_UB_TRAP` with no state change beyond the fault record. The segment is reversed by the cancellation-aware history traversal of §7.4 (LIFO, nested segments included; frames already reversed and `uncall` markers skipped) and its frames are marked reversed; the `uncall` itself pushes a frame naming the segment |
| `trap` | `trap` | CC trap; R fault record (`FAULT_UB_TRAP`, §4.9) |
| `fault` | `fault C` | CC and R; literal 0 ≤ C < 2^64; one terminal record with code C for C ≠ 0, else 4 (§5.4); run ends `FAILED`, no successor executes, prefix history retained for reversal (§7.4, §10, §14.1). One classical instruction (§8.2); in an oracle body or lproc, the one-budget-step §4.2 row instead |
| `qreg.new qreg.free qreg.slice qreg.concat qreg.width qreg.id qreg.from_id` | §3.3 | CC and R (§3.3) |
| `measure` | `r = measure q` / `r = measure.iN q` | CC only; Born rule (§14.2); consumes q; `.iN` for a `qreg[*]` (§3.3) |
| `budget.mint` | `tk = budget.mint @o s h st d` | CC and R; a token for the tuple (s, h, st, d) validated for oracle `@o` (§5.4) |
| `effect` | `effect dev.op args` | R only (§7.3); results are written to memory operands |
| `hostcall` | `rlen = hostcall service ptr len` | CC only (§10) |

**Measurement draws.** Supplied draws are consumed FIFO, one per
executed measurement in dynamic execution order (including measurements
of deterministic states); a failing precondition consumes no draw.
Each draw is in [0,1). Enumerate outcomes lexicographically by their
printed bits string, wire 0 first, and select the first outcome whose
cumulative Born weight is **strictly greater** than the draw times the
total weight. Thus an exact CDF tie selects the next nonzero-weight
outcome. Returned integers remain little-endian (wire 0 is bit 0).
This fixes the reference CLI convention; unsupplied draws follow the
Born distribution (§14.2).

**DRAW-ORDER witness**

```json
{"draws":["0.25","0.75"],"integer_order_values":[1,3],"outcomes_bits":["01","11"],"outcomes_values":[2,3],"reversed_draw_values":[3,2]}
```

Prepare two fresh two-wire registers with H on both wires and measure
them in order. Each has weights 1/4 on `00`, `01`, `10`, `11` in that
order. The first draw selects `01` (integer 2) and the second `11`
(integer 3). Reversed draw consumption would give integers 3,2;
integer-ordered outcomes would give 1,3. Both draws test exact CDF ties.

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
| `lift.free` | `lift.free p` | D | p, alloctab | match_i = (i < atop) ∧ (base_i = p) ∧ ¬pinned_i into scratch (at most one i matches: unpinned entries are heap entries, whose bases strictly increase); under ¬flag: live_i ^= match_i for all i; scratch uncomputed from the unchanged atop, bases and pinned bits | flag = ¬∃ i: match_i ∧ live_i; C = `FAULT_UB_MEMFAULT` | ¬flag: k+1; flag: HALT |
| `lift.faultif` | `lift.faultif p code` | D | p | – | flag = p; C = code, written as its effective cause C′ (§5.4) | ¬flag: k+1; flag: HALT |
| `lift.call` | `w = lift.call @f (a_1..a_m) (tokens..) (classical..) (mem..)` (short form: §3.7) | A+D | §3.7 | §3.7 (slots: m capture slots `disp_1..disp_m`, then assignment slots for fp, sp, depth) | flag per §3.7; C = `FAULT_BUDGET_DEPTH` | ¬flag: entry of @f; flag: HALT |
| `lift.ret` | `lift.ret v` | A+D | §3.7 | §3.7 (slots: the delivery slot `disp_1`, then assignment slots for fp, depth) | flag = (depth = 0); C = `FAULT_UB_TRAP` | ¬flag: `succ`; flag: HALT |
| `lift.retval` | `lift.retval v` | D | v | result_val ^= v | – | HALT |
| `lift.oracle_call` | `lift.oracle_call @o tk (ins..) tgt fr (mem..) (args..)` | D | ins, tgt, fr, mem | tgt ^= payload; fr ^= code (callee contract) | – | k+1 |
| `lift.oracle_uncall` | same form | D | as above | the matched inverse (§5.5): the identical permutation | – | k+1 |
| `lift.perm_call` | `lift.perm_call @a (mut..) (ins..) (mem..) (args..)` | D | ins, mut, mem | mut ← P(mut, ins, mem); inverse = `adj` of @a | – | k+1 |
| `qjump` | `qjump ^b` | D | – | – | – | ^b |
| `qbranch` | `qbranch p ^b1 ^b2` | D | p | – | – | p: ^b1; ¬p: ^b2 |
| `qjumpr` | `qjumpr a` | D | a | succ ← a | flag = (a < first_f) ∨ (a ≥ first_f + n_f), where `[first_f, first_f + n_f)` are the row indices of the containing function instance (contiguous, §3.6); C = `FAULT_UB_TRAP` | ¬flag: `succ`; flag: HALT |
| `fault` | `fault C` | D | – | code ^= C′; faulted ^= 1 (C′ the effective cause of C, §5.4) | – | HALT |

**`inrange(p, n)`** = ∃ i < atop: live_i ∧ base_i ≤ p ∧ p + n ≤ base_i +
size_i, every comparison computed at width max(ptr_width, width(n)) + 1
(no wrap; §3.3); `lift.load`/`lift.store` carry this check
**inherently** on their own address and length, so the reference
function is total for every well-formed body; `lift.boundscheck` is an
explicit assertion row the dialect emits before each access (after it
the access's own flag is never set, so dialect-produced bodies' step
counts are unchanged). Rules: `lift.retval` is ill-formed in an lproc;
`lift.ret` is ill-formed outside lprocs; `tk` is a token-typed classical
argument of the calling oracle or a token parameter of the calling
lproc. `lift.oracle_call`/`uncall`/`perm_call` carry the
complete callee interface; `mem` operands name the calling oracle's
mapped interface regions or the calling lproc's region parameters.
`lift.addr @g` names a global anywhere; it names an
interface region **only in the body of the oracle that declares it**
(lprocs are shared between oracles and receive region bases as
parameters, as in §16.3 example 2). Label values obtained by `lift.
label` denote first rows of blocks of the containing function instance;
`qjumpr` to an index outside that instance's row range faults, so
control never leaves a function except through `lift.call`/`lift.ret`; an
in-range index that is not a block's first row enters that row. The
`args` operands of `lift.oracle_call`, `lift.oracle_uncall` and
`lift.perm_call` are classical arguments of the calling oracle or token
and classical parameters of the calling lproc, in callee signature
order and with exactly matching types, never locations. They are fixed
at entry (§3.1, §3.7). Every lifted call available in an oracle body is
also available in an lproc by passing the required token, classical
arguments and mapped regions explicitly through `lift.call`. In lifted rows
a width suffix `.iN`/`.iM` names a location width and has no upper bound
(§3.3), except that `lift.load.iN`/`lift.store.iN` keep N ∈ {8, 16, …,
128}.

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

In addition to §3.3's operand rules, `qfree d` is well-formed iff
every wire's current version is its `qalloc` version (including a
version restored by a matched inverse) or the clean output of an
explicit §6.4 cleanup of the value occupying that wire.
[deps: ISA-3.3-P3, ISA-4.3-P1, ISA-5.1, ISA-6.4]

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
| `qinplace` | `qinplace @g @ginv tk x (ins..) (mem..) (args..)`; written `qinplace @g @ginv tk x` when all three lists are empty (and only then) | **Well-formed** iff `@g` and `@ginv` are oracles whose `in` slots are x's width n followed by the widths of `ins` in order, whose `tgt` width is n, whose fault widths are equal (F), whose `mem` slots match the `mem` regions (role `in`, §3.3's matching rule) and whose `args` types are those of `args`; x, the `ins` wires and the effective control context are pairwise disjoint. **Sem**: `t = qalloc any n; f = qalloc any F; oracle_call @g tk (x, ins..) t f (mem..) (args..); qexch x t; oracle_call @ginv tk (x, ins..) t f (mem..) (args..); qfree t; qfree f`, so x ← g(x; ins, mem, args); these are its generated operations, in this order (§11). **Inverse-pair obligation**: under the tuple of `tk`, the call's `args` values and the tuples of the tokens among them, on every basis value of x, of the `ins` wires and of the `mem` cells, both oracles are fault-free and g(·; ins, mem, args) and ginv(·; ins, mem, args) are mutually inverse permutations of the n-bit encoding. It is carried by an `inverse_pairs` entry (§12.3) of the certificate record of the region whose body contains the `qinplace`; an entry `{g: G, ginv: H}` covers both `qinplace @G @H` and `qinplace @H @G` (its claim checks both compositions). An entry **covers** a `qinplace` when its `budget` is componentwise ≤ the tuple of `tk` (success at a tuple implies the same result at every larger one, §5.4), every token-typed argument's tuple equals the entry's `arg_tokens` tuple for that argument (equality: a nested oracle's outcome may change with its budget), and every other `args` value lies in its claim's `args` domain. Its claim is an `exhaustive` claim with `expected: "inverse_pair"`, which the executor verifies as a checker does (once per closure hash, before first use), or a `structural` `inverse_pair_library` claim, which covers when the named claim of the linked library's certificate is such a claim for the same closure hashes of g and ginv (no re-execution; a library claim without an `args` domain covers every value; its proof or evidence label is the library claim's); a `sampled` claim never covers. Before any effect of a CC/R region call, every `qinplace` the callee executes (transitively; its token and `args` are resolved from the call's classical arguments, which reach lifted calls only as classical arguments, §4.2) MUST have a covering entry, else CC trap / R fault `FAULT_UB_TRAP`. The private t and f are not values of the region for §6: the certified pair cleans them, the only cleanup that is not a §6.4 realisation. Under control the allocations are unconditional and every gate of both calls and of the exchange is controlled |

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

A `qloop` body is threaded like a block: each visit resolves linear
names against the bindings live at its entry, and its exit bindings
supply the next visit's entry bindings; the entry and exit live names
and their types MUST agree, with consumed body-local names absent from
both. [deps: ISA-3.3-P3, ISA-4.6-P8, ISA-4.6-P9]

### 4.7 Region calls (structured code, CC and R)

`oracle_call @o tk (ins..) tgt fr (mem..) (args..)`; `action_call @a
(mut..) (ins..) (mem..) (args..)`; `adj action_call …`; `adj oracle_call
…` ≡ `oracle_call …`; `ctl w <call>` ≡ the call under `qpred w`. In CC
and R, wire and region slots are filled by `qreg` operands per §3.3
(§3.1: R functions call Q regions exactly as CC does; the call is one
frame of the R history, §7.4). In an action, a region operand names an
interface region of the caller or a local `qregion` of the caller
(§4.6); a local region fills an `in` or a `mut` slot (an `in` slot
returns it unchanged; the caller restores it to its image before exit
either way, §5.1). The `mem` operands of lifted rows follow §4.2.
**Classical arguments** have the signature's types `iN`, `ptr` (a value
of width ptr_width), `f64` and `token`. In an oracle body or lproc an
`iN` or `ptr` argument is a pseudo-location of width N or ptr_width, an
`f64` argument a pseudo-location of width 64 holding its binary64 bits,
and a `token` argument is usable only as the `tk` operand of
`lift.oracle_call`/`lift.oracle_uncall`, in a region call's `args` list,
or in `lift.call`'s token list. Lproc classical parameters have these
same bit readings and may also be forwarded in `lift.call`'s classical
list; token parameters retain their token identity and validity (§5.4).
The invocation operand `tk` is separate from the callee's declared
`args`; its explicit catalog context channel is `oracle_invocation`
(§11.1, K77), including for the lifted calls of §4.2.

### 4.8 Opcode table (tier, operands, result)

| Opcode family | Tiers | Operands | Result |
|---|---|---|---|
| `const.iN` | CC R Q(lift) | literal | iN / reg[N] |
| `add..ashr`, `udiv..srem`, `icmp.*`, `select` | CC R Q(lift) | values of equal width (select: i1, a, b) | same width (icmp: i1) |
| `zext.iM sext.iM trunc.iM` | CC R Q(lift) | value | iM |
| `ptrtoint.iM`, `inttoptr` | CC R | ptr / integer | iM / ptr |
| `load.iN store.iN` | CC R | ptr [, value] | iN / – |
| `alloc free` | CC R | iN / ptr | ptr / – |
| `br call ret uncall trap fault` | CC R (`fault` also Q(lift)) | per §3.1, §4.1, §4.9 | – |
| `qreg.new qreg.free qreg.slice qreg.concat qreg.width qreg.id qreg.from_id` | CC R | per §3.3 | qreg / – / qreg / qreg / i64 / i64 / qreg[*] |
| `measure`, `measure.iN` | CC | qreg[n] / qreg[*] | in / iN |
| `budget.mint` | CC R | oracle reference, four i64 values | token |
| `effect` | R | device op, ptr/len operands | – |
| `hostcall` | CC | service literal, ptr, len | iN (rlen, width ptr_width) |
| `lift.*`, `qjump qbranch qjumpr fault` | Q (oracle bodies, lprocs) | locations, pseudo-locations, labels, literals; call token, classical and region arguments per §3.7, §4.2 | locations |
| gates, `qalloc qborrow qfree qreturn qcopy quncopy qxor qexch qinplace qregion qload qunload qstore qexchm qpred qunpred qif qloop` | Q (actions) | wires, bundles, regions, literals | wires / – |
| `oracle_call action_call adj ctl` | Q, CC, R | per §4.7 | – |

### 4.9 Classical faults (CC, R)

A **CC trap** and an **R fault record** are one event. The failing
instruction is validated before any mutation and has no effect except
appending one **terminal fault record** (its cause code and program
point, §7.4); the run ends `FAILED` (§10) with no further instruction
executed, so the CC caller of a faulting R call executes no successor
instruction and receives no results, and a `FAILED` run has exactly
one fault record. Implicit trap causes and explicit faults have the
following code mapping:

| Cause | Code |
|---|---|
| `udiv urem sdiv srem` with divisor 0 | 5 `FAULT_UB_DIV0` |
| `sdiv srem` of the signed minimum by −1 | 6 `FAULT_UB_SDIV_OVERFLOW` |
| `load`/`store` outside every live allocation; `free` with no live unpinned entry at its address (§7.1); a `hostcall` range not in one live allocation (§10) | 7 `FAULT_UB_MEMFAULT` |
| `alloc` with the heap or the allocation table exhausted (§7.1); a `qreg.new` the device cannot satisfy (§3.3) | 2 `FAULT_BUDGET_HEAP` |
| an `effect` memory operand range not in one live allocation (§7.3) | 7 `FAULT_UB_MEMFAULT` |
| `effect` on a device outside §7.3 (§17 item 3) | 8 `FAULT_EFFECT_UNMODELLED` |
| `entropy.read` past the end of the tape (§7.3) | 10 `FAULT_ENTROPY_EXHAUSTED` |
| `trap`; an illegal `uncall` (§7.4); a use without a current instance (§3.4); a failed `qreg` precondition, width check or overlap check (§3.3), including an unclean `qreg.free` a verifying executor detects; an invalid token or a failed `budget.mint` validation (§5.4); a `qinplace` without a covering inverse-pair entry (§4.5) | 4 `FAULT_UB_TRAP` |
| `fault C` | C′, the effective cause of C (§5.4) |
| exhaustion of the executor's own classical resources | §17 item 16 |

`fault C` takes a literal 0 ≤ C < 2^64 (a launch fault code is a
`uint64_t`, §10); codes above 10 are program-defined. Its frame is the
fault record. `bennett_result_fault` returns the record's code
unchanged, including every nonzero program-defined code up to 2^64 − 1;
it MUST NOT replace such a code with `FAULT_UB_TRAP` or `FAULT_CALLEE`.
`trap` reports only code 4; it cannot stand in for an arbitrary `fault C`.
No host service is needed to report C (`hostcall` remains CC-only).

**Charge and history.** A CC/R `fault C` executes as one classical
instruction, taking `classical_step_time` (§8.2); it does not consume a Q
oracle's B. An R budget supplied by source instrumentation is enforced
by that code, not by the Q step machine. The terminal record
is appended to the existing logical history without erasing, cancelling
or changing any earlier frame, displaced value, effect-tape entry or
open activation. No subsequent source effect occurs, in this activation
or any caller. Forward failure does not reverse the prefix; an eligible
`bennett_reverse` removes the fault record and reverses that intact
prefix under §7.4, §10 and T4.

A Q region never produces a fault record: an oracle's fault is an
outcome in its fault register (§5.2). Its `fault C` is the existing
§4.2 D row: one executed reference row charges one step of B, writes
`code ^= C′; faulted ^= 1`, and selects HALT. Remaining forward machine
steps are the idle steps of §3.6; commit and prefix reversal follow
§5.2, undoing the fault writes and all preceding rows while retaining
the committed fault-register XOR (§14.1, T2). The classical terminal
record and the Q step-machine outcome are distinct reporting paths.

## 5. Regions

### 5.1 Interfaces and common well-formedness

Signatures list roles: `oracle @o (in a: wire[8]) (tgt t: wire[8]) (fault
f: wire[4]) (mem db: region[10,8] in) (args n: i64)`. **Interface
regions** are caller-owned, passed by name, role `in` (returned to entry
contents on every basis configuration) or `mut` (actions only). In the
text form (§16.2) a wire param's role suffix is optional and, when
present, MUST equal its group's role (`in` in an oracle's or action's
`in` group, `mut` in an action's `mut` group); a region param always
carries its role (`in` or `mut`); other region-interface params carry
no suffix. Lproc parameter roles are specified in §3.7 and §16.2. A region
MUST NOT contain `measure effect br call uncall trap hostcall qreg.* budget.mint` or
classical memory instructions, nor lifted rows outside oracle bodies.
Predicate stack empty at entry and exit. Every `qalloc` matched by a
`qfree` of a clean bundle, every `qborrow` by a `qreturn` after its
frame, every local `qregion` restored, by **explicit cleanup
instructions**; the schedule chooses only realisations. **`in` wires in
actions** appear only as controls (including the address operands of
`qload qunload qstore qexchm`, the wires pushed by `qpred`, the selector
of `qif`, whose two `x` gates restore it, and the `cond` wires of `qloop …
while`), as targets of diagonal gates, as `qcopy`/`qxor` sources, as the
value operand of `qstore` (it is only read, as the control of the XOR
into the selected cell), or as `in` arguments of calls. The **region
call graph** — an edge from a function to the callee of each of its
`oracle_call`, `action_call`, `lift.oracle_call`, `lift.oracle_uncall`
and `lift.perm_call` instructions and to both callees of each
`qinplace`, an oracle counting the rows of its lproc closure as its own —
is acyclic (suite F); recursion exists only through `lift.call` among
lprocs.

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

**Semantics.** The body denotes a unitary U on mut ⊗ ins ⊗ mem ⊗
(borrowed), where mem includes both `mut` and `in` interface regions,
block-diagonal in the computational basis of `ins` and of `in`-region
cells, identity on borrowed and external reference systems (§5.6),
workspace returned clean, with domain D every value of each `mut`
and `in` bundle, every cell of every `mut` and `in` interface region and
every borrowed bundle, workspace initially at 0 and local regions at
image. [deps: ISA-5.1-P1, ISA-5.2-P4, ISA-3.3-P19, ISA-5.6-P1, ISA-14.2] No fault outcome. Coherent internal
control yields the padded unitary under declared bounds, part of the
action's identity. **Permutation action**: realised unitary a
permutation matrix (ε = 0, permutation gates only, transitively).

**Body**: gates; `qcopy quncopy qxor qexch qinplace`; `qload qunload
qstore qexchm`; `qpred qunpred qif qloop`; `oracle_call action_call`;
`qalloc qborrow qfree qreturn`; `qregion`.
An action body with several `block`s executes its blocks in text order,
each a unitary fragment; labels are descriptive and carry no control
semantics, and lifetimes may span blocks.

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
  qxor qexch qstore qexchm: self-adjoint   qinplace @g @ginv tk x (ins) (mem) (args) ↦ qinplace @ginv @g tk x (ins) (mem) (args)
  oracle_call ↦ oracle_call
  action_call @b ↦ adj action_call @b   qpred/qunpred pairs reversed as a whole
  qif w {A}{B} ↦ adjoint of the complete §4.6 expansion, including unconditional lifetimes, in reverse order. [deps: ISA-3.5, ISA-4.6-P7]
  qloop n {A} ↦ qloop n {adj A}
  qloop n while cond {A} ↦ flags computed forward as §4.6; adj A for i = n..1 under c_i; flags uncomputed
```

**Control.** `ctl w @a` is controlled-U: workspace, regions and flags
allocated unconditionally; every gate of the body and its cleanup runs
under `w` in addition to the active predicate.

The shorthand `qif w {adj A}{adj B}` denotes that adjoint when each
arm's allocations and releases are matched within that arm; no
arm-local lifetime restriction is imposed on the source `qif`.
[deps: ISA-3.5, ISA-4.6-P7, ISA-5.1]

Two operations form a **matched pair** iff the second is the §5.3
adjoint of the first, with the same callee(s) (the pair exchanged for
`qinplace`), identical classical argument values and token identities
and tuples, the same operand wires with the first's read-only input
versions and produced target versions current at the second, and equal
effective control sets including the versions of their wires; order and
repetition in predicate stacks are irrelevant. [deps: ISA-2-P10, ISA-3.3-P3, ISA-4.5-P5, ISA-4.7, ISA-5.3-P4, ISA-5.4]
A matched inverse restores preceding wire-version bindings for
subsequent matching only when the §6.2 cleanup conditions hold; matching
alone does not discharge an outstanding-reader or phase obligation, and
a cell write always advances its cell version even when its value is
restored. [deps: ISA-3.3-P3, ISA-6.1-P1, ISA-6.2]

Scheduled action adjoints use the source replacements above before
reference-recipe instantiation, with the ordinal contract and `adj`
adapter specified in §11.1 (K62). [deps: ISA-5.3-P4, ISA-11-P2, ISA-11.1-P29]

### 5.4 Budgets and fault codes

Lproc token parameters forward existing tokens; they neither mint a
token nor alter its validity or tuple. Binding and forwarding have no
separate budget charge (§3.7); a lifted region call inside an lproc has
the same charge and token semantics as in an oracle body. In
particular, the enclosing oracle's token is not implicitly substituted
for a nested call's explicit token.

Budget = (B, heap_limit, stack_limit, depth_limit), classical. `bennett_
budget` validates: `heap_limit ≤ layout.heap_limit_max`, `stack_limit ≤
2^S_cells`, `depth_limit < 2^Dc − 1`; for a memoryless object (§7.2)
`heap_limit = stack_limit = depth_limit = 0`. B is enforced by running
exactly B steps; heap, stack and depth are wire counters.
*(non-normative, used by §4.5)* If the reference interpreter succeeds
on x under a tuple β₀, it succeeds with the same result under every
tuple β ≥ β₀ componentwise: its only limit-dependent decisions are the
flags of `lift.alloc` and `lift.call`, false on that trajectory and
still false with larger limits, and the step bound, not reached. A
nested `lift.oracle_call` row uses the tuple of its own token, not β,
which is why §4.5 fixes those tuples exactly.

**Tokens.** A token denotes a validated tuple (B, heap_limit,
stack_limit, depth_limit) and the oracle it was validated for; a region
call uses the tuple of the token it is given, and a token MAY be
supplied to any region call of the program (the checks above depend
only on the object's layout). Tokens come from `bennett_budget` (§10;
valid until the program is unloaded) or from **`tk = budget.mint @o s h
st d`** (CC and R): `@o` names an oracle of the program (a symbol
reference, §9.2) whose object's layout the checks use, and is recorded
with the token for diagnostics only; s, h, st, d are `i64` values read
as unsigned 64-bit;
the instruction applies exactly `bennett_budget`'s checks to (s, h, st,
d) before any mutation; failure is a fault record `FAULT_UB_TRAP` (§4.9)
and no token; success produces a fresh token for that tuple, valid
until its frame is reversed or its run is CLOSED, and never
constructible from an integer. A region call given a token that is not
valid is a CC trap / R fault `FAULT_UB_TRAP` before any effect (a launch
argument: `E_ARG`). A minted tuple binds its invocation exactly as a
host-minted one does (§11, §12): an invocation whose closure hash,
variant, inherited controls, tuple and `params_hash` equal the
`bindings` of the object's schedule executes that schedule; any other
invocation executes under the §11 defaults; a consumer MUST NOT apply a
schedule bound to another tuple, nor substitute another tuple. In
`params_hash` a token argument is encoded as its tuple
`[B,heap,stack,depth]`. A budget is classical and fixed before region entry (§3.1), so
`budget.mint` is not a region instruction (§5.1).

```
  0 FAULT_NONE            4 FAULT_UB_TRAP            8 FAULT_EFFECT_UNMODELLED
  1 FAULT_BUDGET_STEPS    5 FAULT_UB_DIV0            9 FAULT_CALLEE
  2 FAULT_BUDGET_HEAP     6 FAULT_UB_SDIV_OVERFLOW  10 FAULT_ENTROPY_EXHAUSTED
  3 FAULT_BUDGET_DEPTH    7 FAULT_UB_MEMFAULT
```

F ≥ 4. Code 10 is recorded by the R `entropy` device (§7.3) and is also
the code a lifted oracle that virtualises entropy uses (`fault 10`) when
its entropy input is exhausted.

**Effective cause.** The literal C of `fault C` (in every tier, §4.2,
§4.9) and of `lift.faultif p C` records the cause C′ = C if C ≠ 0 and C′ =
`FAULT_UB_TRAP` (4) if C = 0;
every other row's code is a fixed nonzero constant. So no fault is ever
recorded as `FAULT_NONE`: a faulted outcome F_B(x) = (0, code) has code ≠
0, and the fault register distinguishes it from every success (F ≥ 4
makes 4 representable). Forward and inverse fault writes use C′.

### 5.5 Nesting and matched cleanup

A `lift.oracle_call` supplies a caller location `fr'`, clean when
computing a fresh outcome. No automatic propagation: the dialect emits `p
= lift.icmp.ne fr' zero; lift.faultif p FAULT_CALLEE` (with `zero` a
`lift.const` location) where the source requires it. To clear `fr'`, the
producer emits `lift.oracle_uncall @o` with the same token, callee, `ins`
and `args` and `mem` values (no intervening row writes those `ins` locations
(suite F); intervening writes to `mem` cells are permitted but mean the
uncall is not guaranteed to clear `fr'`) and the successor versions of
`tgt` and `fr'`; the pair shares a
dynamic invocation identity. Alternatively `fr'` is retained until the
prefix reversal. Matching is **LIFO**: on every path, a
`lift.oracle_uncall` matches the most recent preceding unmatched
`lift.oracle_call` with the same callee, token, `ins`, `args` and `mem`
operands (two calls followed by two uncalls form two nested pairs); an
uncall that matches no call on some path, or different calls on
different paths, is ill-formed. In an lproc the match includes the
fixed bindings of its instance (§3.7); parameter forwarding does not
weaken any matching or cleanup condition.
Suite F rejects a pair when a row on a path between them writes one of
its `ins` locations; an intervening `lift.store` is not ill-formed (its
address is data): `lift.oracle_uncall` is the same permutation as the
call (§4.2), so a pair whose cells changed in between still executes
and is undone by the prefix reversal, and clearing `fr'` is then the
producer's obligation.

### 5.6 Borrowed systems and borrow frames

**Requirement.** A region's completed operation equals its declared
operation ⊗ identity on every borrowed bundle and on any external system
entangled with it.

**Rule (suite F).** Borrowed wires (set B) are touched (as control or
target) only inside **borrow frames**: maximal contiguous permutation-
only subcircuits from the first to the last instruction touching B. The
frame's domain D_F contains every value of every borrowed and interface
wire, independently, and the values of its other wires admitted by the
entry-state analysis below, starting from the region's D (§5.2). The
frame's realised permutation P_F MUST satisfy
`P_F|span(D_F) = (P' ⊗ I_B)|span(D_F)` for some P' independent of B,
established by a T3 claim over all of D_F (exhaustive, or a library
certificate, §12 `borrow_frames`) or
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

For (i)–(iii), every gate's controls include its effective control
context, and V⁻¹ runs under the same effective control set and wire
versions as V. [deps: ISA-2-P10, ISA-3.5, ISA-5.3-P5]
Maximality of a frame inside a `qloop` or `qif` body is judged within
that body's static instruction sequence, separately for each borrowed
lifetime, not across unrolled visits or across distinct arm sequences.
[deps: ISA-4.3-P2, ISA-4.3-P4, ISA-4.6, ISA-5.6-P2]

**Entry-state analysis (K76, normative).** This analysis fixes D_F; a
stronger analysis cannot narrow it. Resolve classical arguments, tokens,
controls, operand identities, allocations and the acyclic local call
expansions from the object (§3.5, §4, §5.1, §5.3), for each permitted
invocation. A wire's abstract value is 0, 1 or unknown (both values).
Interface and freshly borrowed wires start unknown; `qalloc` starts 0;
image preparation uses the corresponding X gates on allocated wires.
The transfer rules are:

1. If any control literal is known false, counting the operation's own
   controls together with its effective control context, the operation is
   disabled: preserve all abstract values and record no causal event. Otherwise,
   an X-family flip or controlled swap evaluates its targets only when
   all its operands are known; any other target becomes unknown.
   Read-only controls keep their values. Diagonal gates keep basis
   values; other quantum gates make their targets unknown. An opaque
   oracle or `qinplace` makes its outputs unknown; an unresolved action
   makes its modified wires unknown. Local action bodies use these same
   rules, with inherited controls.
2. Each enabled reversible operation records its exact identity and the
   preceding abstract values on **every** operand's causal stack,
   including readers. Its exact §5.3 adjoint restores those values only
   when that same event is the top event on every operand stack; pop
   that event everywhere. Identity includes operands, effective controls,
   callees, classical arguments and token identities/tuples. Disjoint
   events may interleave; nested pairs may cancel. A lifetime boundary
   or unresolved action invalidates the entire connected stack history
   reached through its operands. Allocation and release add/remove the
   corresponding abstract components.
3. Structured bodies follow §4.6, including unconditional lifetimes and
   predicated gates; bounded loops apply the transfer at each visit.
   Equal complete abstract states permit exact cycle skipping. A proved
   inductive over-approximation may represent remaining visits, but may
   not establish a constant that these transfers do not establish.
   The normative D_F is the union obtained by the stated finite transfers;
   acceleration must preserve that domain. A coarser invariant may prove
   the obligation on a superset, but failure on that superset is not a
   counterexample on D_F.
   This is a decidable finite rule set; Boolean polynomial simplification
   and quantum identities beyond these exact adjoint pops supply no
   entry facts.

At a frame entry, retain only the known constants of its allocated local
wires; every other local component independently takes both values, and
every interface and borrowed component independently takes both values
even if the prefix related or fixed them. D_F is this Cartesian product;
for repeated visits it is the union of these products. Thus `CX c b`
is identity on arbitrary b and its external reference when this analysis
establishes c = 0, whereas an interleaved CNOT prefix that clears c only
by polynomial algebra supplies no such entry fact. Exact Boolean
reasoning remains available to prove the permutation **within** a frame.
The checker MUST use this D_F for both exhaustive and library frame
claims and establish that the reachable entry states lie in span(D_F).
By linearity the restricted equality then applies to every reachable
entry state, including superpositions entangled with an external system.

### 5.7 Executor transformations

Inlining, structure recovery, dispatch re-indexing and simplification
MUST produce on every x ∈ D the same final interface tuple as §5.2's
construction on the reference body (T6). Checkpointed and pebbled
realisations: §17 item 18.

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
| `qinplace @g @ginv tk x (ins) (mem) (args)` | x: perm with S_x ∪ ins ∪ cells(every region in `mem`) ∪ Π if x was perm, else other; the `ins` wires and `mem` cells are unchanged |
| lifted rows | each written location/cell: perm with the union of its read operands' sets ∪ Π; written cells' versions advance |
| `qregion` creation | every cell: version 0, perm, S = ∅, with the declared image as its initial value. [deps: ISA-4.6-P1] |

**Outstanding dependence** (for `other` cleanup) extends the dependency
test beyond workspace provenance sets to the joint state of all other
live values, including interface `mut` wires, region cells, borrowed
wires and outstanding diagonal phases. [deps: ISA-3.3-P3, ISA-5.1, ISA-5.3-P1, ISA-6.1-P1]
For a candidate inverse of the computing sequence C of g, let G be g's
wires and M the composed intervening operation after C and before that
inverse, retaining every intervening gate and its effective controls,
with internal clean and borrowed lifetimes interpreted as in §14.2.
[deps: ISA-2-P10, ISA-3.5, ISA-4, ISA-14.2]
The remaining values or phases **depend on g** iff there is no single
operator V on the remaining wires such that M = I_G ⊗ V for every state
of G and every input in the remaining wires' declared domain, including
arbitrary external entanglement and the exact global phase.
[deps: ISA-5.2-P4, ISA-5.3-P1, ISA-5.6-P1, ISA-14.2]
This is a joint, transitive test on the composed operation: cleaning or
releasing an intermediate value does not erase its already-transferred
dependence, and a diagonal use remains an outstanding phase unless its
inverse cancels it in M. [deps: ISA-4.4, ISA-6.3, ISA-14.2]
Dependency-set propagation through reads supplies such transitive paths,
but absence of a direct provenance edge to g alone does not establish
the required factorisation. [deps: ISA-6.1-P1, ISA-14.2]
A producer MAY establish non-dependence by the dependency-set test: if no
live value, interface wire, region cell or uncancelled diagonal phase has
a transitive read path from g in the intervening sequence, then M
factorises as I_G ⊗ V; failure of this test does not by itself prove
dependence.

### 6.2 Window and obligations

A perm value g with set S is **in its window** from its computation
until the first of: a non-diagonal gate on a wire in S or in g; a version
advance of a cell in S; a non-permutation action call touching a wire in
S; a permutation change to a wire in S not undone before g's cleanup.
A permutation change to a wire of S is **undone** when it and its
undoing form a matched pair (§5.3), and every intervening operation
leaves the computational-basis values of S and g unchanged; a cell
version advance still closes the window even if its value is restored.
[deps: ISA-5.3, ISA-6.1-P1, ISA-14.2]
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
unpinned entry with base p dead (unpinned entries are heap entries,
whose bases strictly increase; pinned entries cannot be freed and a
pinned entry with base p is left unchanged; no live unpinned entry with
base p: CC trap / R fault `FAULT_UB_MEMFAULT`); storage is never
reclaimed.
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

**BLOCK-IMAGE** (K10; source: bennett-vm-47i). `layout.block_image`
names a data symbol (§9.1, §16.1). Decode each successive pair of its
lowercase hex digits to one byte, in textual order. Its decoded length
L MUST be a multiple of 512, including L = 0. At block-device
initialisation, before executing any instruction or changing device
state, reject an image of any other length; never pad or truncate it.
For 0 ≤ s < L/512, sector number s is present and its byte at offset b
(0 ≤ b < 512) is image[512s + b]. There is no sector header, length
prefix, sector-number field or reversal of bytes within a sector. An
all-zero sector in the image is present. Every other sector is absent
and reads as 512 zero bytes; no image and an empty image give an empty
map. This specifies the initial map only; the §7.3 write/reversal
presence-bit rule remains in force. Motivation (0.8 §7.3): "sector map
from the `block_image` (else empty), 512-byte sectors; absent sectors
read as zero"; §9.1: "`data` lines are `NAME SP HEX`". The contiguous
encoding and partial-sector policy are additions, not a claimed 0.8
loader requirement.

**BLOCK-IMAGE witness**

```json
{"length":1024,"present_sectors":[0,1],"sector_first_bytes":[[0,0],[1,255]],"absent_sector":2,"partial_lengths_rejected":[1,511,513,1023]}
```

The image is 512 bytes 00 followed by 512 bytes ff (2048 hex digits).
Sector 0 is present although zero; sector 1 is ff throughout; sector 2
is absent and reads zero. Writing sector 2 then reversing removes it;
writing sector 0 then reversing restores a present zero sector.

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
| `effect` | tape index plus the device-specific record of §7.3; reversal also removes its effect-tape entry |
| `hostcall` | payload bytes and reply bytes |
| `qreg.*`, `measure` | the ledger record of §3.3 (ids, class, widths, prior states, whether a free's cleanliness was verified) and the measured bits |
| `budget.mint` | the token and its tuple; reversal revokes the token |
| `oracle_call` / `action_call` | (region hash, variant, inherited control count, classical args with every token's tuple, register ids): reversed by re-application / adjoint, exactly once, by this frame |
| fault record (a failing instruction, `trap`, `fault`) | cause code (§4.9) and program point; terminal. Reversal (§10) removes the record; the failing instruction had no other effect, so the state is then the state before it |

**Logical history.** Frames and dynamic instances specify the
*logical* history. An executor MAY store it by checkpoints, deltas or
deterministic replay, provided it reconstructs the same logical frames,
instances, reversal marks and traversal order; it never re-issues an
external event (effects are replayed from the effect tape and host
replies from their frames, never requested again), never re-executes a
region call to recover its record, and never copies quantum state. T4 is
stated over the logical history. **Active and audit history.** The
*active* history is the sequence of frames not marked reversed;
reversed frames and `uncall` markers remain as immutable *audit
records*. Undoing a defining frame removes its dynamic instance from the
active environment although its audit record is retained.

**Pure frames.** A frame is **pure** iff it belongs to `br` or to a
defining instruction among `const`, the binops, `udiv..srem`, `icmp`,
`select`, `zext sext trunc`, `ptrtoint inttoptr`, `load`, `qreg.width
qreg.id qreg.from_id`: it changes only the set of instances. Every other
frame (`store alloc free call ret uncall trap fault effect hostcall
qreg.new qreg.free qreg.slice qreg.concat measure budget.mint`, region
calls, fault records) is impure.

**History traversal** (the one reversal procedure, used by segment
`uncall` and by whole-run reversal). A range of frames is **reversed**
by visiting its frames in LIFO order; a frame already marked reversed
and an `uncall` frame are **skipped**; every other frame is undone by
its row of the table above and then marked reversed. Reversed frames
stay in the history, marked, and are never undone again. An `uncall`
marker is always skipped: when a later traversal (an enclosing
segment's `uncall`, or whole-run reversal) reaches it, the frames of the
segment it names are already marked and are skipped too, so neither the
marker nor its segment is undone, re-executed or redone a second time.

**Segment uncall** (`uncall @f (args) (results)`). Let S be the most
recent completed call segment of the history (a `call` frame, its
matching `ret` frame and every frame between them). The `uncall` is
legal iff S is a call of `@f`, S's recorded boundary argument and result
values equal the operand values, **every frame after S is pure**, and S
contains, at any nesting depth, **no `measure` frame** and no `qreg.
free` frame whose cleanliness was not verified (hardware, §17 item 14);
otherwise it is a CC trap / R fault `FAULT_UB_TRAP` and changes nothing
beyond the fault record (§4.9). Execution reverses S by the history traversal (nested segments are
undone; nested segments already cancelled by an inner `uncall`, and that
inner `uncall` frame, are skipped), and pushes an `uncall` frame naming
S. The instances defined inside S no longer exist; using such a name
before it is redefined is a CC trap / R fault `FAULT_UB_TRAP`.
**Whole-run reversal** (§10) is the history traversal over the whole
history: S's effects on memory, the allocation table, devices, the
register ledger and tokens were undone by the `uncall`, and the frames between S and the
`uncall` are pure, so at the `uncall` frame every component except the
retained instances already equals its value before S. T4 is stated over
these frames. *(non-normative)* S is never re-executed and never redone;
the compute–copy–`uncall` idiom derives what it keeps through pure
instructions before the `uncall`. Suite A contains: `f` calls `g`,
uncalls `g`, returns; `g` performs one `clock.read`; `call f; uncall f`
leaves the clock at its entry value; and `uncall` of a segment that
measured is a trap.

## 8. Target descriptions (target 0.9)

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

**EPS-DECADE** (K9; source: bennett-vm-cxg). A table expression with
`index: "eps_decade"` evaluates its zero-based array index as the exact
integer min{ j ≥ 0 : eps · 10^j ≥ 1 }. It requires a context binding
`eps` and 0 < eps ≤ 1; otherwise it is a load-time error. Thus it uses
the requested `epsilon_share`, not the entry's achieved `epsilon`.
Evaluation uses exact rational comparisons, never a floating-point
logarithm. The existing out-of-array rule applies to this integer. An
entry with `epsilon` 0 MUST NOT use `eps_decade`, including through a
table lookup. This extends the exact-entry prohibition above; it does
not assign an index to eps = 0. Motivation (0.8 §8.1): the grammar names
`"index": "k" | "eps_decade"`, and "Division by zero and a table index
outside the array are load-time errors"; 0.8 defines no decimal index.

**EPS-DECADE witness**

```json
[{"eps":"1","index":0},{"eps":"0.1","index":1},{"eps":"0.1001","index":1},{"eps":"0.0999","index":2},{"eps":"0.001","index":3},{"eps":"0.000999","index":4}]
```

For eps = 999/10000, eps·10 = 999/1000 < 1 and eps·100 = 999/100 ≥ 1,
so the index is 2. A two-entry table rejects this index, a three-entry
table selects element 2. eps = 0, eps > 1 and an unbound eps reject;
no clamping, padding or fallback entry is admitted.

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
`max_parallel` is declared. Connectivity is all-to-all when `topology`
is absent, and is constrained by §8.3 when present (§17 item 15).
Interface wires are charged to the caller for the call's duration;
borrowed wires to the borrower at `dirty_rate`, replacing the owner's
charge.

### 8.3 Classes, gates, schemes, capabilities

```
  "ptr_widths_supported": [32, 64],
  "classes": { "<cls>": { "qubit_second": n, "dirty_rate": n, "capacity": n | "unbounded" } },
  "topology"?: { "vertices": [ { "class": "<cls>" }, … ], "edges": [ [u, v], … ] },
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

**Topology.** `topology` is optional. Its `vertices` array orders the
physical vertices; a vertex's index is its address and its `class` MUST
name a declared addressable class. Each edge is an undirected pair of
integer indices `[u,v]`, with `0 ≤ u < v < vertices.length`; edges MUST
be sorted lexicographically, without duplicates or self-loops. Unknown
fields reject. Each live wire occupies one vertex of its resolved
class, distinct from every other simultaneously live wire. The number
of vertices of a class limits occupancy in addition to its capacity.
A native multi-wire gate is realisable only if every pair of its
operand vertices is joined by an edge (including all effective control
wires); single-wire gates need no edge. Target schemes MUST meet this
rule for each native template leaf, including their ancillae. §11
schedules bind these placements to the target hash. Absent `topology`
means all-to-all with the existing class capacities. Routing and
movement costs are deferred to 0.10 under §17 item 15; placement itself
is validated in 0.9.

**TOPOLOGY witness**

```json
{"capabilities":{"classical_step_time":1,"max_parallel":"unbounded","max_predicate_depth":"unbounded","mbu":false,"measurement":{"feedforward_latency":0,"mid_circuit":false}},"classes":{"fast":{"capacity":4,"dirty_rate":1,"qubit_second":1}},"gates":[{"classes":["fast"],"controls":{"max":1,"min":1},"cost":{"time":1},"epsilon":0,"op":"cx"}],"imports":{},"objective":{"weighted":{"time":1}},"ptr_widths_supported":[32],"qram":null,"resources":{"peak_qubits":{"kind":"peak","unit":"qubit"},"qubit_second":{"kind":"occupancy","unit":"qubit_second"},"time":{"kind":"time","unit":"second"}},"schemes":[],"tables":{},"topology":{"edges":[[0,1],[0,2],[1,3],[2,3]],"vertices":[{"class":"fast"},{"class":"fast"},{"class":"fast"},{"class":"fast"}]}}
```

The vertices are the row-major 2×2 grid; its four edges connect
horizontal and vertical neighbors. A CX on vertices 0 and 1 is
realisable; on 0 and 3 it is infeasible under §17 item 15. The canonical
UTF-8 bytes above exclude the code-fence LF.
Target SHA-256: `960cee71e88da141cc6c2b13cab3f28fce1d50c006e67446aadb592e2bfd0882`.

### 8.4 Space budget

The capacity constraint is peak live qubits per class.

## 9. Objects, identity, linking, reversible ABI (object 0.9)

### 9.1 Sections and schemas

Order fixed: `symbols imports functions data devices layout schedule
certificate coverage`; each at most once; unknown sections or fields are
errors. Metadata sections are one JCS line each, an object:

```
  symbols:  { "<local index>": { "name", "kind": "cc"|"r"|"oracle"|"action"|"perm_action"|"lproc"|"data", "signature": <sig>, "interface_hash" } }
  imports:  { "<name>": { "signature": <sig>, "pinned_closure_hash"?: hex } }
  devices:  { "models": { "<dev>": { "version": "0.9" } }, "services": { "<reverse-dns id>": { "version": "…" } } }
  layout:   { "ptr_width", "H", "A_tab", "S_cells", "null_size", "heap_base", "heap_limit_max",
              "globals": { "<name>": { "base", "size", "image": "<data name>" } },
              "interface_regions": { "<oracle>": { "<region>": { "base" } } }, "block_image"?: "<data name>" }
  schedule: §11      certificate: §12      coverage: { "entries": [ §13 ] }
  <sig>:    kind "oracle": { "tier":"q", "kind", "in":[w…], "tgt":w, "fault":F, "mem":[{"A","W","role"}], "args":[types], "abi":"0.9" }
            kind "action"/"perm_action": { "tier":"q", "kind", "mut":[w…], "in":[w…], "mem":[…], "args":[types], "bounds":[…], "abi" }
            kind "lproc": { "tier":"q", "kind", "params":[w…], "result":w, "tokens":["token"…], "args":[types], "mem":[{"A","W","role":"in"}], "abi" }
            kind "cc"/"r": { "tier", "kind", "params":[types], "results":[types], "abi" }
            kind "data": { "tier":"-", "kind", "size", "abi" }
```

Integers that may exceed 2^53 are decimal strings, and a JSON number ≥
2^53 anywhere in metadata is an error. `data` lines are `NAME SP HEX`.
**Encodings.** `types` in `args`, `params` and `results` are the §16.2
type spellings as JSON strings (`"i64"`, `"ptr"`, `"f64"`, `"token"`,
`"qreg[8]"`); `w` in `in`, `tgt`, `mut`, lproc `params` and `result` is
the integer bundle or location width (§16.3). An lproc's `tokens`,
`args` and `mem` arrays are mandatory (empty arrays when absent from the
header); `args` excludes tokens and `mem` has only `in` roles (§3.7).
Array order is header order within each group. A **program-point id**
(§9.2) is the JSON array `[interface_hash, block name, ordinal]`.
Certificate `frame` fields use exactly the typed-record schema of §9.4;
unknown fields are errors there as in every metadata record.
`devices.models` lists every §7.3 model that an `effect` of the object
uses (an `effect` on an unlisted §7.3 model is a load error; a device
outside §7.3 is never listed and faults at run time, §17 item 3; a key
that is not a §7.3 model is an unknown field); `devices.services` lists
every `hostcall` service (§10). An interface region's name (its param
name and its `layout.interface_regions.<oracle>` key) MUST differ from
every symbol and import name of the object, since `@name` in `lift.addr`
denotes either (§9.2).

### 9.2 Identity

An lproc's token, classical and region parameter groups are part of
its JCS signature (§9.1), including their order and types. The header
and every forwarded operand list are canonical function bytes; changing
them changes the envelope and, through references, the caller's closure
hash. Fixed binding instances are derived per oracle (§3.7), not new
symbols or separately hashed bodies; instance rows share the source
row's program-point id and expand once per fixed row instance per step,
while the instance and semantic-call occurrence components in §11
invocation paths and §12.1 context keys distinguish their uses. [deps: ISA-3.7-P5, ISA-3.7-P6, ISA-11.1-P9, ISA-12.1-P11] Entry argument values and token tuples bind invocations through
`params_hash`, not through the lproc's interface hash (this section).
Imports must match all five groups; validation and instance formation
are repeated after linking (§9.3).

**Canonical function bytes**: the text from the function's header line
through its last instruction line, lines joined by LF, no trailing LF.
**Semantic envelope** of a symbol (byte-exact; every part ends with LF):

```
  (1) "isa=" <full version string, e.g. 0.9>
  (2) "ptr_width=" INT
  (3) the JCS signature
  (4) the canonical function bytes (with reference tokens replaced, below); for a data symbol: its data line NAME SP HEX
  (5a) for every data entry in the closure set, sorted by name bytewise:        "data " NAME " " HEX
  (5b) for every layout leaf in the closure set, sorted by JCS path bytes: "layout " <JCS key-component array> " " <JCS value>. [deps: ISA-9.1, ISA-16.1]
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
closure hashes. **Acyclic and cyclic symbols.** The reference graph
has an edge from a symbol to every symbol it references (parts
(4)–(5)). An **acyclic** symbol — a one-member SCC that does not
reference itself — has hash = SHA-256 of its own envelope (example 1's
`inc8`, example 2's `zero` and `sum_db`); the SCC procedure below applies
to every **cyclic** SCC, including a one-member SCC whose function
references itself (example 2's `sum`). **SCCs**: members ordered by name bytewise; every intra-
SCC `@name` token (parts (4)–(5)) is replaced by `@$<decimal index>`;
intra-SCC references contribute no part-(6) line; `scc_hash` = SHA-256
over the concatenation of the members' envelopes in that order; member
hash = SHA-256 over the ASCII bytes of `<scc_hash hex>:<decimal index>`.
**object_hash** = SHA-256 of the canonical object text with the
`schedule`, `certificate` and `coverage` sections deleted together with
the blank line preceding each. `reference_program_hash` = the oracle's
interface hash. `params_hash` = SHA-256 of the JCS array of classical
parameter values (the typed encoding of §12.3, K13); `schedule_hash` =
SHA-256 of the schedule's JCS bytes.
**Program-point id** = `(symbol interface hash, block name, instruction
ordinal within the block counting nested lines in text order)`.
Executable certificates and caches bind to **closure hashes** (required,
§12).

A layout leaf's path is the JCS array of its original JSON key
components from the layout root to the deepest schema-listed leaf,
so a scalar has a one-component path and an interface-region leaf has
path `["interface_regions","<oracle>","<region>"]`.
[deps: ISA-9.1-P1, ISA-16.1]
Part (5b) emits exactly one line for each structured leaf in the closure
set, including distinct leaves whose dotted renderings coincide, ordered
by the unsigned UTF-8 bytes of that JCS path array, independently of the
leaf values; no dotted rendering is used as a key or an ordering key.
[deps: ISA-9.1-P1, ISA-16.1]
An oracle's own interface-region leaves and entries of other oracles
are selected by equality of the original JSON key under
`interface_regions` to the oracle's name, never by a prefix of a
rendered path; an lproc's global leaves are selected by equality of
the key under `globals` to the global name.
[deps: ISA-3.7-P1, ISA-9.1-P1]

**Envelope boundary lemma** (non-normative).
For a function symbol, §16.2 requires a header beginning `fn `,
`oracle `, `action `, `perm_action ` or `lproc `; following lines are
`regs`, block labels, instructions, or structured closing braces. [deps: ISA-16.2]
No §4 opcode is `data`, `layout` or `device`; a result with one of
those names has ` = ` after the name, which cannot begin any part-(5)
line (a data name, a JSON array, or a device name is required there). [deps: ISA-4.8, ISA-9.1, ISA-16.2]
No canonical function line is a bare 64-hex string, so the first
part-(5)/(6) line ends the function bytes unambiguously. [deps: ISA-4.8, ISA-16.2]
The fixed `data `, `layout `, `device ` prefixes distinguish (5a–c),
and a bare 64-hex line distinguishes (6); JSON strings escape LF. [deps: ISA-9.1, ISA-16.1]
For a data symbol, the signature kind selects exactly one data line
for (4), with (5)–(6) empty, even when the data name itself is `data`,
`layout` or `device`. [deps: ISA-9.1, ISA-16.2]
Together with the fixed first three lines and the injective JCS array
paths, these facts make the envelope parts recoverable without length
prefixes; this is an encoding argument, not a claim of SHA-256 injectivity. [deps: ISA-9.1, ISA-16.1, ISA-16.2, ISA-9.2-P4]

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
- **Frame descriptor** (certificate): interface slots retain their identities;
  scratch is recorded by class and cleanliness, with widths as expressions
  in inherited control count `c`; retained history is B × frame width for
  the full-history oracle expansion, otherwise the bound library's realised
  history (§17 item 18). Borrowed wires and scheme ancilla frames are
  separate records. Callees `qborrow` only from the caller's designated
  idle set. Shared frames require disjoint live ranges (suite F).

**Frame JSON schema (B5).** The descriptor is the following JCS object;
all five arrays are required, including empty arrays. Every record has
exactly the shown fields; `live_ranges` is optional. Unknown fields at
any depth are errors under §9.1.

```
  { "slots": [ { "id": "<slot identity>", "role": "in"|"tgt"|"fault"|"mut"|"mem_in"|"mem_mut", "class": "<cls>", "width": expr }, … ],
    "scratch": [ { "id": "<frame identity>", "class": "<cls>", "state": "clean"|"dirty", "width": expr }, … ],
    "history": [ { "id": "<frame identity>", "class": "<cls>", "width": expr }, … ],
    "borrow": [ { "id": "<frame identity>", "class": "<cls>", "width": expr }, … ],
    "ancillae": [ { "id": "<frame identity>", "scheme": "<scheme name>", "class": "<cls>", "state": "clean"|"dirty", "width": expr }, … ],
    "live_ranges"?: [ { "frame": "<frame identity>", "start": ordinal, "end": ordinal }, … ] }
```

`slots` lists the source interface in operand order: oracle `in`, `tgt`,
`fault`, then regions; action `mut`, `in`, then regions. Slot identities
are `<group>:<zero-based index within group>` (`in:0`, `tgt:0`,
`fault:0`, `mut:0`, `mem:0`, …); a region uses role `mem_in` or
`mem_mut`. A region slot's width counts all its cells, in address then
bit order; bundle bits are least-significant first. Slot widths MUST
match the signature. Inherited controls are caller-owned and precede
these slots in §11 topology placement; they are not renamed callee
slots. Every class is a resolved target class. Non-slot frame identities
are nonempty producer-chosen strings, distinct from every other record
identity in the descriptor; a dynamic identity additionally includes
the invocation context and the expansion scratch identity (§11.1).
Array order is source interface order for slots, and first allocation
order in the realised expansion for each other array. `scratch` records
per-class, per-cleanliness workspace; `history` records retained history;
`borrow` records dirty requirements; `ancillae` records each scheme's
ancilla frame and its declared state. These categories do not double
count the same wires. No requirements may be omitted because they vanish
for one chosen basis input.

Every `expr` uses §8.1's expression language with **only `c` bound**;
other variables and table lookups (whose indices require `k` or `eps`)
are invalid. At every covered inherited control count the widths MUST
be nonnegative integers; interface widths are positive and signature
fixed. Instantiation substitutes the resolved budget, parameters and
expansion choices into constants before forming these expressions.
Widths describe the actual realisation, including history and scheme
ancillae, and are checked against it. Each `live_ranges` entry names a
non-slot frame identity and a half-open interval `[start,end)` of its
invocation's generated leaf order (including step/phase/path expansion,
§11); `start < end`. A shared frame identity retains its recorded class, state and width
across uses; every use of shared storage MUST be listed and intervals
of the same frame MUST be pairwise disjoint. An omitted list gives no shared-storage permission.

**FRAME witness**

```json
{"ancillae":[{"class":"fast","id":"a","scheme":"controlled-x","state":"clean","width":{"var":"c"}}],"borrow":[{"class":"fast","id":"b","width":1}],"history":[{"class":"fast","id":"h","width":3}],"live_ranges":[{"end":2,"frame":"s","start":0},{"end":4,"frame":"s","start":2}],"scratch":[{"class":"fast","id":"s","state":"clean","width":{"args":[2,{"var":"c"}],"op":"+"}}],"slots":[{"class":"fast","id":"mut:0","role":"mut","width":2},{"class":"fast","id":"in:0","role":"in","width":1}]}
```

At `c = 2`, the slot widths total 3, scratch width is 4, retained
history width is 3, borrow width is 1 and scheme ancilla width is 2.
The two half-open uses of `s` meet at 2 and do not overlap. This is a
schema/arithmetic witness; a real certificate must also bind the
expansion and target defining `controlled-x`. Its canonical UTF-8
bytes exclude the code-fence LF.
Frame SHA-256: `f314eeef24a5a65a9c72f91e062aa3c83556358eaca166e689571700a72083ff`.

## 10. Launch ABI (launch 0.9)

**Model.** A run executes a device CC entry; the host passes classical
arguments, register ids and the entropy tape, receives classical
results, fault codes and declared measurements; host services are
reached by `hostcall`. **Positional binding**: argument i of `bennett_
run` binds to parameter i of the entry's signature: `INT(width, bytes)`
to `iN` with width = N (else `E_ARG`), `F64` to `f64`, `QREG` to `qreg[n]`
with the register's n or to `qreg[*]` with any width, `TOKEN` to `token`
(a valid token, §5.4). Arguments and the entropy tape
are **copied** at `bennett_run`; the caller may free its buffers
afterwards. Host-minted tokens are scoped to the program and destroyed
at unload; device-minted tokens to their run (§5.4).
Accessor-returned pointers are valid until the owning object is freed.
`bennett_unload` with a run not CLOSED: `E_INVALID_STATE`.

**Invocation tree.** A run record is a tree (CC segments, R calls, Q
calls); an R call's subtree is owned by its R history; `bennett_reverse`
reverses post-order: CC segments by their run history, R calls by LIFO
reversal of their history (§7.4, reversed segments and `uncall` frames
skipped), top-level Q calls by re-application / adjoint. A fault record
is terminal (§4.9): the run is `FAILED`, and every activation open at
the fault keeps its frames, which reversal undoes like those of a call
that returned.

**States.** `CREATED → RUNNING → (SUSPENDED ⇄ RUNNING) → (HOST_REQUEST ⇄
RUNNING) → COMPLETED | FAILED`; `COMPLETED → REVERSED`; `FAILED →
REVERSED`; any of
`COMPLETED/FAILED/REVERSED → CLOSED` (`bennett_run_close` releases the
record; register ids created by the run remain valid unless measured or
freed). A run owns the registers and memory it touches exclusively while
not CLOSED; a register reached by `qreg.from_id` is touched from then
on; `bennett_qreg_prepare`, `bennett_qreg_free` and a `bennett_run`
argument naming a register owned by another run that is not CLOSED are
`E_INVALID_STATE`. **Reverse eligibility**: `COMPLETED` or `FAILED`; no `measure`
frame; no `qreg.free` frame whose cleanliness was not verified (§17
item 14); no register it touched has been prepared, freed, sliced or
used by another run since; else `E_NOT_REVERSIBLE`. Reversing a `FAILED`
run first undoes its terminal fault record, then traverses the rest of
its history exactly as for a completed run, including the frames of
activations that never returned; the run is then `REVERSED` with every
component T4 names at its entry value. `bennett_qreg_prepare` and `bennett_
qreg_free` require a clean register (`E_QREG_NOT_CLEAN` otherwise on a
verifying executor; a non-verifying one: §17 item 14); there
is no reset and no trace-out: a register in unknown state is released by
a `measure` inside a run, which consumes its handle (§3.3).

**Results.** `bennett_result_get` writes value i and sets `*kind` and
`*width`: `INT` as ⌈N/8⌉ little-endian bytes, `*width` = N; `F64` as the
8 IEEE 754 binary64 little-endian bytes, `*width` = 64; `QREG` and
`TOKEN` as the 8-byte little-endian id, `*width` = 64. A `cap` smaller
than that byte count is `E_ARG` and nothing is written. Fault records
are read by `bennett_result_nfaults` / `bennett_result_fault` (codes of
§4.9; a `COMPLETED` run has none, a `FAILED` run has exactly one, its
terminal record, and exposes no values).
For an R `fault C`, `bennett_wait` returns `OK` with `*result_out` set
and `*request_out` NULL as for any `FAILED` run;
`bennett_result_nvalues` is 0, `bennett_result_nfaults` is 1 and
`bennett_result_fault(result, 0)` is exactly C when C ≠ 0 (4 when C = 0,
§5.4), with all 64 bits preserved. The fault code is result data, not a
`bennett_status` error or a host-service reply.

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
`rlen` = the full reply length (so truncation is detectable; a reply
whose length does not fit `ptr_width` bits is refused by `bennett_reply`
with `E_ARG` before any write, and the run stays in `HOST_REQUEST`); the frame
records the request bytes, the overwritten bytes and the reply bytes.
Every `service` is declared in `devices.services`; an undeclared one is
a load error.

**Tape.** `bennett_tape_next` yields each `effect` in tape order; `args`
holds the operation's operands in the order of §7.3, each an unsigned
64-bit little-endian field (pointers zero-extended from `ptr_width`), so
`*alen` = 8 × arity.

```c
/* launch 0.9. All objects opaque. A function that returns an object transfers ownership to the caller,
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
/* K12: resolved classical parameter values, not live register ids. */
bennett_status bennett_estimate_run(bennett_program_t*, const char* region, bennett_token,
                                    const char* variant, uint32_t inherited_controls,
                                    const uint8_t* params_jcs, size_t params_len, bennett_estimate_t** out);
size_t         bennett_estimate_nresources(const bennett_estimate_t*);
bennett_status bennett_estimate_get(const bennett_estimate_t*, size_t i, const char** name, const char** value_decimal);
const uint8_t* bennett_estimate_certificate(const bennett_estimate_t*, size_t* len);   void bennett_estimate_free(bennett_estimate_t*);
bennett_status bennett_coverage_get(bennett_program_t*, bennett_coverage_t** out);
const uint8_t* bennett_coverage_jcs(const bennett_coverage_t*, size_t* len);   void bennett_coverage_free(bennett_coverage_t*);
```

### 10.1 Launch-estimate contract (K12)

**LAUNCH-ESTIMATE** (K12; b-isa-spec-c15, from bennett-vm-hsd).
The 0.9 request carries the complete resolved parameter vector.

**Resolved request.** `bennett_estimate_run` MUST copy and
validate `params_jcs`, the JCS array of **all** classical arguments in
signature order, encoded as §12.3 specifies; `params_len` is its UTF-8
byte length, excluding any NUL terminator. The separately supplied
valid token of that program fixes `[B,heap,stack,depth]`; token-typed
arguments fix their own tuples, never the outer tuple by default.
Host- and live device-minted tokens are both admitted (§5.4); the
request copies the tuple while valid, so later revocation cannot
retarget an already returned estimate.
An empty array binds an empty signature only; no argument is implicitly
zero, inferred from a hash, or taken from an earlier run. A missing,
extra, mistyped or out-of-range argument is `E_ARG` before producing an
estimate. Every well-typed resolved argument vector is supported; the
interface bundles, arbitrary target/fault entries, dirty wires and
interface cells remain quantum inputs, not chosen basis values.

The caller supplies a nonempty `variant` and `inherited_controls` as
in §11; these are part of the request, not inferred from a different
invocation. The request denotes that region/variant/control count at
its declared accuracy and those resolved parameters and budget.
It uses the object's schedule exactly when every §5.4/§11 binding
matches, otherwise the §11 defaults. The estimator MUST resolve the
complete generated realisation and aggregate its scheduled leaf events
and wire live intervals by §8.2; running one basis input, counting only
executed oracle rows instead of all padded B steps, or silently changing
parameters, budget, target, expansion library or cleanup is not an
estimate of that request. A consumer lacking the selected expansion
library reports `E_SCHEDULE_INFEASIBLE` as §11 requires (b-isa-spec-8r4);
this postpones mechanics, not the estimate capability.

**Resource rows.** `estimate_nresources` counts scalar rows,
not target resource declarations. A `count` or `time` resource has one
row named by its escaped resource name. Each `occupancy` or `peak`
resource has one row **for every target class**, including unused classes with value
zero, named `escape(resource)[escape(class)]`; no sum across classes is
substituted. `escape` percent-encodes the UTF-8 bytes except ASCII
letters, digits, `-._~`, using uppercase hex (including `%`, `[` and
`]`). Scalar resource names use the same escape. Rows are enumerated
by increasing bytewise encoded name. Thus names are injective even when
target names contain delimiters; `name` and `value_decimal` remain
ordinary NUL-terminated strings with §10's ownership lifetime.

**Decimal values.** Aggregation is exact rational arithmetic;
rounding occurs only at the accessor boundary. `value_decimal` is the
least nonnegative decimal with at most **34 significant digits** that
is ≥ the exact resource value. For q > 0 let e be the unique integer
with 10^e ≤ q < 10^(e+1); return
`ceil(q / 10^(e−33)) × 10^(e−33)`. Zero is `0`. The canonical spelling
uses ASCII digits and an optional decimal point, no exponent, plus
sign, leading integer zeros (except `0`), trailing fractional zeros or
negative zero. Exact integers and terminating rationals that fit are
unchanged. This is an upper enclosure, not a fabricated exact value for
1/3; capacity, matching, objective comparison and certificate checking
MUST use the exact rationals, never the rounded display.

**Certificate binding.** The estimate's certificate MUST bind
object, interface, closure, target and effective schedule hashes, root
variant/controls, accuracy, expansion identity and the resolved
`bindings.invocation` (§12.3). Even a default-only realisation has an
explicit empty-entries schedule document with those bindings, hence a
schedule hash. Its root region has `estimate: { precision_digits: 34,
exact_resources: { "<encoded row name>": { numerator: "<integer>",
denominator: "<positive integer>" } } }`; fractions are reduced,
nonnegative and decimal-string encoded, zero is 0/1. `resources` uses
the identical encoded keys and canonical decimal strings returned by
`estimate_get`. A checker MUST rebuild the bound realisation, recompute
all exact rows and their upward decimal encodings, and reject any
binding, key, rational or display mismatch. A producer's resource map
alone is not verification.

**LAUNCH-ESTIMATE witness**

```json
{
  "variant":"forward","inherited_controls":0,
  "binding": {"args":["2"],"budget":["2","0","0","0"]},
  "precision_digits": 34,
  "classes": ["A","B]","idle"],
  "live": [
    {"class":"A","count":2,"start":"0","end":"1/3"},
    {"class":"B]","count":1,"start":"0","end":"1/3"}
  ],
  "rows": [
    ["peak_qubits[A]","2"],
    ["peak_qubits[B%5D]","1"],
    ["peak_qubits[idle]","0"],
    ["qubit_second[A]","0.6666666666666666666666666666666667"],
    ["qubit_second[B%5D]","0.3333333333333333333333333333333334"],
    ["qubit_second[idle]","0"],
    ["time","0.3333333333333333333333333333333334"]
  ],
  "decimal_checks": [
    {"rational":"0","decimal":"0"},
    {"rational":"2","decimal":"2"},
    {"rational":"1/8","decimal":"0.125"},
    {"rational":"1/3","decimal":"0.3333333333333333333333333333333334"},
    {"rational":"2/3","decimal":"0.6666666666666666666666666666666667"},
    {"rational":"1/30","decimal":"0.03333333333333333333333333333333334"},
    {"rational":"10/3","decimal":"3.333333333333333333333333333333334"}
  ]
}
```

This **aggregation witness** assumes the displayed scheduled intervals,
unit class rates and no other events; it does not assert an unbound
oracle gate count. A permitted cost expression `1 / 3` produces that
makespan. The exact class peaks are 2 and 1, not a replacement scalar 3;
occupancies are 2/3 and 1/3, and the idle class is present. Changing the
argument `2` to `1` denotes a different request, even at the same budget.
No 0.8 request can transmit that distinction through §10's signature.

## 11. Scheduling interface (sched 0.9)

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

**Schedule document** (JCS) has the following schema, including reserved
support points and optional instance/call-occurrence selectors. [deps: ISA-11-P2, ISA-3.7-P5, ISA-11.1-P9, ISA-11.1-P22, ISA-11.1-P29]

```
  { "bindings": { "closure_hash", "target_hash", "region", "variant", "inherited_controls", "budget": [B,heap,stack,depth],
                  "params_hash", "epsilon", "expansion": { "name", "version", "hash" }, "scheduler": { "name", "version" } },
    "interface_vertices"?: [ [v, …], … ],
    "entries": [ { "path": [ { "symbol": hex, "point": "<block>:<ordinal>" | "$construct" | "$step" | "$commit" | "$release", "iteration": [n, …] | "*",
                              "instance"?: [n, …] | "*", "call_index"?: n | "*" }, … ],
                   "step": n | "*",  "phase": "fwd" | "rev" | "*",  "generated": n | "*",
                   "kind": "cleanup" | "gate" | "alloc" | "start",
                   "cleanup": { "realisation": "reverse" | "recompute" },
                   "gate":    { "realisation": "native" | "<scheme name>", "epsilon_share": decimal },
                   "alloc":   { "class": "<cls>", "vertices"?: [v, …] },           /* a concrete class; "any" is not allowed in a schedule */
                   "start":   { "time": decimal } } ] }
```

**Topology placement.** With a §8.3 topology, `interface_vertices`
lists inherited control wires first as individual width-one arrays, then
one vertex array per source interface slot in §9.4 slot order; array
elements follow bit order (and region cell address then bit order). A callee inherits its actual
operand placements. `alloc.vertices`, when present, assigns every bit
of that allocation in bit order. These arrays MUST have the declared
width, resolve to the correct classes and have disjoint live uses;
without a topology they MUST be absent. Omitted placements use the
lowest-index free vertex of the resolved class, assigning bits in order;
interface slots are assigned first in slot order, then allocations in
generated order. Vertices are retained for a wire's lifetime and freed
on release; borrowed wires retain their owner's vertices. Every native
leaf, including scheme leaves, MUST satisfy §8.3 adjacency, else
`E_SCHEDULE_INFEASIBLE` naming §17 item 15. No routing is inserted.

**Matching.** Every generated operation has an **invocation chain**:
the program points of the region calls and `lift.oracle_call`s that led
to it, outermost first, ending in its own point. [deps: ISA-4.7, ISA-4.2, ISA-3.6]
`lift.call` adds no element: an lproc row in an oracle's closure generates
its expansion once per fixed row instance per step under its dispatch
predicate, independently of which `lift.call` reached that instance or
the recursion depth. [deps: ISA-3.6, ISA-3.7-P5, ISA-3.7-P6]
`path` matches
an operation iff it is a **prefix** of that chain, element by element:
`symbol` and `point` equal, and `iteration` either `*` or equal to the
vector of 0-based dynamic repetition counts of the `qloop`s enclosing
that point (outermost first; its length is the point's loop nesting
depth, `[]` outside every loop); `instance` and `call_index` match as
specified below. [deps: ISA-4.6, ISA-3.7-P5, ISA-11.1-P9]
An oracle invocation's forward step coordinate is t ∈ 1..B and its
inverse step t has `phase: rev`; the root B is `bindings.budget[0]`
and a nested oracle's B is the steps component of its own call token,
not the parent's B. [deps: ISA-5.2-P3, ISA-5.4, ISA-10]
An entry's `step` and `phase` read the oracle invocation entered by the
last oracle-call element of its `path`, or the root invocation if there
is no such element. [deps: ISA-4.2, ISA-4.7, ISA-5.2-P3]
A call element enters that invocation only when it is followed along
the operation's chain into the callee: when the element is the
operation's own final point, it remains in its containing invocation. [deps: ISA-4.2, ISA-4.7]
`lift.call` never changes this level; a path ending at a call element
that is a proper prefix of the operation's chain already selects the
entered callee level. [deps: ISA-3.6, ISA-3.7, ISA-4.7]
At a level with no oracle step, including an action root and oracle
construction/commit/release outside the steps, only `step: "*"` and
`phase: "*"` match; an action's adjoint does not itself supply a
`rev` phase. [deps: ISA-5.2-P3, ISA-5.3, ISA-4.7]
`generated` is the ordinal within the row's expansion in the bound
library, or within its reserved support pseudo-point (K64), or the
non-emitting cleanup carrier ordinal (K65). [deps: ISA-11-P2.S3, ISA-11.1-P5, ISA-11.1-P29, ISA-6.4]

**Specificity** is the lexicographic tuple (path length, number of
non-`*` iterations, step non-`*`, phase non-`*`, generated non-`*`);
an entry applies iff all its selectors match, and among matching entries
of the same kind the unique maximal one applies. [deps: ISA-11-P3, ISA-4.6]
Two distinct entries (distinct array positions, even if identical)
with equal maximal specificity for the same generated operation and
kind make a tie; this is the meaning of "incomparable", and document
order is never significant. [deps: ISA-11-P6.S1]
A tie makes the schedule invalid for that operation under the validation
stages below; overlapping equal-specificity entries do not make a tie
where a more-specific matching entry applies, including coverage by a
union of such entries. [deps: ISA-11-P6.S1, ISA-11-P6.S2, ISA-11-P7]
Operations outside an invocation's own budget or inside a zero-trip
loop are not generated and cannot witness a tie. [deps: ISA-5.2-P3, ISA-4.6]
Selectors are resolved independently per `kind`.
A `gate` entry matches only gate operations, an `alloc` entry only
allocations, and a `start` entry every generated operation. [deps: ISA-11-P2.S1, ISA-11-P3]
The applying entry supplies the decision: an omitted field with a
default takes that default, never a value from a less-specific matching
entry. [deps: ISA-11-P3, ISA-17]
Defaults
for uncovered operations: `reverse`; `native` if the gate matches a
`gates` entry, else the first matching scheme; class = the first class
declared in the target's `classes` object (JCS order) that has capacity
for it; sequential timing in generated order.
An operation uncovered for one kind, including in a nested invocation,
takes that kind's default directly, without inserting an entry or
altering any other operation's selected decision. [deps: ISA-8.3, ISA-17]
There is no requirement that these defaults be expressible by additional
entries in the single-`step`, single-`phase` selector language. [deps: ISA-11-P3, ISA-17]
**Timing**: a `start` time
MUST be ≥ the end of every operation the operation depends on (data,
wire lifetime, region cell version, effect order); an entry violating
this makes the schedule invalid. **Obligations**: satisfy §6; respect
capacity; report every resource; be reproducible from the request plus
scheduler version.

**Validation stages (K55).** A consumer validates every binding and
every path against the object, including the maximal-match condition
at the stages specified here, and executes verbatim or rejects with
`E_SCHEDULE_INFEASIBLE`. [deps: ISA-9.2, ISA-11-P5, ISA-11-P6.S1, ISA-11-P6.S2, ISA-11-P6.S3, ISA-11-P6.S4, ISA-11-P7.S2, ISA-11-P7.S3, ISA-11-P7.S7]
For admission, a nested invocation budget is **object-derivable** exactly
when substituting literal integer constants and signature-positional
classical/token forwarding into the four operands of `budget.mint`
yields one tuple for that call site; an unresolved root parameter,
conflicting tuples or any other unresolved operand makes it
non-derivable. [deps: ISA-4.1, ISA-3.7, ISA-5.4, ISA-10]
Literal propagation initialises every nonliteral value to unknown,
takes exact bit-vector values from `const.iN`, copies values through
positional call/return and branch/block-parameter bindings to a fixed
point, and joins all syntactic incoming values as unknown unless they
are all the same known value; arithmetic, predicate reasoning and
additional implementation-specific inference do not make a budget
object-derivable for this staging rule. [deps: ISA-4.1, ISA-3.4, ISA-3.7, ISA-5.4]
The root region's token parameters remain unresolved at object
admission even if a CC/R caller in the object mints a literal-budget
token, since that caller does not bind every invocation of the
region. [deps: ISA-4.1, ISA-4.7, ISA-5.4, ISA-10]
This derivation does not invert `params_hash`, assume a token id's
tuple, or substitute an enclosing invocation's budget. [deps: ISA-9.2, ISA-12.3, ISA-5.4]
A consumer MUST reject root-level ties and nested ties whose invocation
domains are object-derivable at admission, and MUST reject a tie in a
non-derivable nested domain at the first concrete operation in generated
order having multiple maximal matching entries, before applying any realisation to
that operation, with `E_SCHEDULE_INFEASIBLE` and the diagnostic
"§11: multiple maximal matching schedule entries". [deps: ISA-11-P5, ISA-11-P6.S1, ISA-11-P6.S2, ISA-11-P6.S3, ISA-11-P7.S2, ISA-11-P7.S3, ISA-11-P7.S7, ISA-5.4, ISA-10]
A nested domain is object-derivable only if every oracle budget on its
invocation chain is object-derivable (the root uses the bound budget);
admission quantifies over the generated operations of these domains,
and defers the remaining domains without rejecting merely because
some possible budget would contain a tie. [deps: ISA-5.2-P3, ISA-4.6, ISA-11-P5, ISA-11-P6.S1, ISA-11-P6.S2, ISA-11-P7.S2, ISA-11-P7.S3]
Admission success therefore leaves the prescribed concrete checks in
non-derivable domains outstanding, even when actual token values become
available earlier; learning them does not move rejection to a different
stage. [deps: ISA-5.4, ISA-10, ISA-11-P7.S2, ISA-11-P7.S6, ISA-11-P7.S7]
Schedule decimal numbers and decimal strings denote the exact rational
of their decimal text; equal values match and resolve identically
regardless of spelling. [deps: ISA-8.1-P1, ISA-5.2-P1]
Token parameters in `params_hash` use §12.3's canonical four-component
tuple encoding, for host- and device-minted tokens alike. [deps: ISA-12.3, ISA-5.4]

**Selection witnesses** *(non-normative)*. [deps: ISA-11-P3, ISA-5.2-P3] For root B=2 and nested B=3,
nested step 3 exists; with nested B=2 it does not, independently of root
B. [deps: ISA-5.2-P3, ISA-5.4] A path of `[]` with `step: 1` reads root step 1 even for an operation
at nested step 3; a path through the nested call reads nested step 3. [deps: ISA-4.2, ISA-4.7, ISA-5.2-P3]
Two `lift.call` sites p1/p2 into the same lproc row q give one row-q
expansion per fixed instance per enclosing step, with neither p1 nor p2
in its chain; different binding keys yield distinct instance components. [deps: ISA-3.6, ISA-3.7-P5, ISA-3.7-P6]
An action-root X has no step/phase, including under adjoint. [deps: ISA-5.3, ISA-4.7]
Equal maximal entries A/B reject; A/B fully covered by higher C or a
union C1/C2 admit in every order; duplicate C entries reject. [deps: ISA-11-P3]
An alloc entry cannot shadow a gate entry. [deps: ISA-11-P2.S1, ISA-11-P3]
A more-specific realisation-only entry takes the default share even if
a broad entry writes a share. [deps: ISA-11-P3, ISA-17]
For root-step-1 scheme X and an uncovered root-step-2/nested-step-1
gate, only the latter takes its default; no synthetic nested entry
overrides the former. [deps: ISA-11-P3, ISA-17]
An unknown nested budget permits admission, but if the first ambiguous
operation is at nested step 3, B=3 rejects there before its realisation,
whereas B=2 has no such operation; an object-derivable B=3 rejects at
admission. [deps: ISA-11-P3, ISA-5.2-P3, ISA-5.4, ISA-10]
Numeral 0 and strings `"0"`, `"0.0"`, `"0.000"` all denote zero. [deps: ISA-8.1-P1, ISA-5.2-P1]

**Invocation-edge identity (K63).** Every invocation edge identifies the
source call point, the containing fixed-binding instance (the §3.7 integer
binding key, or `[]` outside an lproc instance), and the zero-based
semantic-call occurrence within that source row expansion, serialized as
`instance` and `call_index` alongside `symbol`, `point`, `iteration`.
[deps: ISA-3.7-P5, ISA-3.7-P6, ISA-9.2-P1.S3, ISA-11.1-P9]
Number semantic calls in forward instantiated constructor traversal order
before descending into callees, counting `call` constructors rather than
`invoke`/`apply` recipe composition, independently of leaf ordinals;
inverse traversal retains forward occurrence numbers. [deps: ISA-11.1-P5, ISA-11.1-P9, ISA-11.1-P29.S3]
The operation's terminal point also carries its containing `instance`,
but has no `call_index` unless it is an invocation edge into a callee.
[deps: ISA-3.7-P5, ISA-11-P5, ISA-11.1-P9]
In schedule path elements each new selector may be `*`, and omission
means `*`; a concrete `instance` matches that exact integer array, and
a concrete `call_index` matches only an edge with that occurrence number.
[deps: ISA-11-P3, ISA-3.7-P5, ISA-11.1-P9]
Validate concrete instance keys against §3.7 source instance formation
and concrete call indices against the bound-library expansion at that
source point and instance, including static repetitions. [deps: ISA-3.7-P5, ISA-3.7-P6, ISA-11.1-P5, ISA-11.1-P9]
These selectors do not add specificity components: the existing
lexicographic tuple is unchanged, so equally specific overlapping
entries still tie unless covered by a more-specific match. [deps: ISA-11-P6.S1, ISA-11-P6.S2, ISA-11-P6.S3]
The edge's source point selects the entered invocation for K52 exactly
as before; adding instance and call occurrence does not introduce a
`lift.call` invocation or another step level. [deps: ISA-11-P5.S5, ISA-11-P5.S6, ISA-11-P5.S7, ISA-3.7-P6]

**Non-row addresses (K64).** Non-row support leaves have reserved
pseudo-points `$construct`, `$step`, `$commit`, `$release` in their
containing oracle; these are legal path points rather than user block
names. [deps: ISA-3.6, ISA-5.2-P3, ISA-11-P2, ISA-11.1-P22]
For the bound `oracle.construct` recipe, its initial `visit State`
subtree has point `$construct`, each forward or inverse `step` invocation
has point `$step`, the commit segment from allocation of `halt` through
release of `halt` has point `$commit`, and the final inverse `visit State`
subtree has point `$release`. [deps: ISA-5.2-P3, ISA-11.1-P22.S14, ISA-11.1-P29]
Within `step`, dispatch comparisons, HALT successor support, pc/next/frame
exchanges and dispatch cleanup stay at `$step`; `Rows[k]` and `Next[k]`
source-template subtrees instead retain source row k's point and shared
row ordinal space in traversal order, and semantic callees retain their
own invocation chains and spaces. [deps: ISA-3.6, ISA-11.1-P14, ISA-11.1-P22.S14, ISA-11.1-P29]
All nested helper `invoke`, loops and descriptor visits inherit their
containing point unless they enter one of those source-row or semantic
callee subtrees. [deps: ISA-11.1-P5, ISA-11.1-P9, ISA-11.1-P18, ISA-11.1-P22]
Number support leaves from zero in instantiated expansion order within
each pseudo-point, separately for each oracle step and phase at `$step`,
excluding all source-row and callee subtrees; inverse traversal retains
the corresponding forward step's ordinals and occurrence numbers. [deps: ISA-11.1-P29.S1, ISA-11.1-P29.S2, ISA-11.1-P29.S3, ISA-11.1-P9]
Reversing a complete already expanded construction retains each leaf's
forward pseudo-point and ordinal while adjointing its operation. [deps: ISA-11.1-P5, ISA-11.1-P29.S3]
`$step` carries the containing oracle's t and fwd/rev phase; the other
three points have no step or phase at that level and match only wildcard
step/phase there, including when B=0. [deps: ISA-5.2-P3, ISA-11-P5.S8]
A pseudo-point's own instance and source-qloop iteration vectors are
`[]`; outer call edges retain their actual coordinates, and bound-library
constructor loops do not create source-qloop iterations. [deps: ISA-3.7-P5, ISA-4.6, ISA-11-P5, ISA-11.1-P5]
Path validation accepts exactly these reserved spellings for oracle
support and validates their generated domains by the partition above;
B=0 has no `$step` leaves but still has construction, commit and release.
[deps: ISA-5.2-P3, ISA-11-P7, ISA-11.1-P22]
These addresses annotate the bound event stream without removing,
reordering or changing the charge of any emitted leaf. [deps: ISA-11-P2, ISA-8.2, ISA-11.1-P29]

**Whole-cleanup selection (K65).** Each explicit computing-sequence/cleanup
pair has one non-emitting cleanup carrier at its source cleanup point,
identified before realisation expansion, even when the cleanup emits no
leaves. [deps: ISA-6.2-P1, ISA-6.4-P1, ISA-11-P3]
The point is the explicit `quncopy`, `qunload`, `lift.oracle_uncall` or
adjoint-call point when that instruction is the cleanup; for an explicitly
written inverse sequence ending in `qfree` or `qreturn`, it is that
terminating release point (also for an empty inverse sequence). [deps: ISA-4.3, ISA-4.5, ISA-4.6, ISA-4.2, ISA-5.3, ISA-5.5, ISA-6.2-P1]
The carrier uses that point's containing invocation chain, fixed-binding
instance, source-qloop iteration vector and containing step/phase, with
carrier ordinal 0; it creates no callee edge or leaf ordinal. [deps: ISA-11-P5, ISA-3.7-P5, ISA-4.6, ISA-11.1-P29]
Only cleanup-kind entries match the carrier, with `generated: "*"` or
`generated: 0`; other generated integers do not match, and gate, alloc
and start entries do not match it. [deps: ISA-11-P3, ISA-11-P6.S5, ISA-11-P6.S6]
Resolve the unique maximal cleanup entry or the reverse default before
expanding that cleanup, and apply its reverse/recompute realisation to
the entire paired cleanup, subject to §6's validity conditions. [deps: ISA-11-P6.S1, ISA-11-P6.S7, ISA-11-P6.S8, ISA-6.2, ISA-6.4]
The carrier emits no gate, allocation, release, start event, resource
charge or timing dependency; ordinary gate/alloc/start selection then
applies to the chosen realisation's emitted leaves, and cleanup-kind
entries do not match those leaves. [deps: ISA-8.2, ISA-11-P2, ISA-11-P6.S6, ISA-6.4]
Internal constructor uncomputation, implicit qregion image restoration,
loop-flag cleanup and the certified private qinplace t/f cleanup keep
their instruction-defined expansions and do not add explicit-pair
carriers. [deps: ISA-4.5-P5, ISA-4.6, ISA-11.1-P5, ISA-6.4]
For `d = qcopy s; quncopy s d`, selecting recompute at the quncopy point
chooses fresh-copy/XOR/uncompute for the whole cleanup, while reverse
chooses inverse-copy/release at the same carrier; an empty inverse
sequence still has its ordinal-0 carrier at its release point. [deps: ISA-4.5, ISA-6.2-P1, ISA-6.4-P1, ISA-11-P6]

### 11.1 Reference-library contract (K11)

**ISA-REF-LIB** (K11; b-isa-spec-8r4, from bennett-vm-47t).
This is the decided 0.9 contract. The catalog bound as ref version 0.9
is the file `spec/ref-0.9.json` whose four-line envelope hashes to
`5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197`.
It publishes the complete 219-recipe catalog, byte-identical to the
accepted catalog snapshot. Consumers lacking the bound library report
`E_SCHEDULE_INFEASIBLE` as §11 requires. The witness below is not a
full-library hash.

**Serialization and identity.** The schema and family witnesses are
documented in `spec/ref-0.9-draft.README.md`. The JSON file is RFC 8785 canonical
UTF-8, with no trailing LF, containing exactly `isa`, `name`, `version`
and `recipes`. The first three are strings `0.9`, `ref`, `0.9`.
`recipes` is an array in bytewise `kind` order, then increasing parameter
tuple order. Each instantiated recipe has `kind`, its integer width or
other named integer parameters, `operations`, `scratch`, `removable`
and `source` (the motivating ISA sentence). A parameterised recipe
uses `parameters` (an ordered array of formals defined below) and `body` instead of the
instance's `operations`; its body uses the closed constructors below.
Recipes cover every §4 instruction/row, the §3.6 step, §3.7 activation
operations and §5.2 construction, with no implementation-private leaf.
Classical instructions/effects remain classical leaf events (§8.2),
not invented quantum gates. The README documents schema, parameters,
coverage and witnesses; it is not hashed and cannot alter operations.

The library hash is SHA-256 of this UTF-8 envelope (every line ends LF,
including the last); the fourth line is the **entire** canonical library
JSON, including all recipes, sources and versions, without an embedded
hash field:

```
isa=0.9
expansion=ref
version=0.9
<JCS library document>
```

`bindings.expansion` names `ref`, version `0.9`, and this 64-lowercase-hex
hash. This adopts §9.2's version-prefixed, LF-terminated **envelope
convention**, with explicit expansion-domain and library-version lines;
it is a new library rule, not §9.2's symbol signature/SCC envelope.
Motivation (0.8 §11): "a versioned document, identified in the schedule's
`bindings.expansion` as { name, version, hash }"; 0.8 §9.2: "Semantic
envelope ... every part ends with LF". A changed recipe, source, scratch
name or ordering changes the library hash; no schedule/certificate can
silently inherit that change (§12.1's realised-subject binding).

**Expansion and ordinals.** Recipe bodies are ordered arrays
of constructors: a gate (`gate`, ordered `wires`, optional `params`), an
allocation (`alloc`, `width`, `class`, `state`), release (`release`),
classical event (`classical`, `point`), counted loop (`for`, `from`,
`to`, `body`), named recipe expansion (`invoke`, ordered `args`), or
inverse (`inverse`, `body`). Constructor objects have exactly those
keys. Fully instantiated `operations` contain only emitted leaves, each
also carrying its computed `ordinal`; unexpanded `body` constructors
carry no ordinal. Scalars are integer literals, parameter names, or prefix arrays
`[op, operands…]` for `+ - * div mod bit`; div is floor division with a
positive divisor. `bit(x,i)` requires nonnegative integers x and i and
returns floor(x/2^i) mod 2, with no fixed machine-word truncation (K23).
For x=13, bit(x,0..4) is 1,0,1,1,0; literal construction emits X only
for the one bits, in increasing bit order. Wires are declaration names with integer-expression
subscripts. Loops enumerate [from,to) in increasing order; expansion is
depth first, array order, and recipe dependencies are acyclic. An
inverse reverses its fully expanded body and adjoints each leaf by
§5.3, interchanging allocation/release. The complete serialized catalog
must encode the algorithms below in these constructors before release;
this document does not claim that prose alone is an interchangeable file.

**Typed binding (K19).** A formal is `{ "name": name, "type": type }`,
with exactly these keys, except `wire`, which additionally requires
`width`, and `templates`, which additionally requires `length` (integer
expressions using earlier integer formals); `arguments` requires `symbol`,
and `value` requires `isa_type`, as specified in K24; K25–K27 add
`records`, `region`, `class`, and `allocation` with the keys specified there. Types are `integer`,
`wire`, `angle`, `body`, `symbol`, `environment`, `event`, `image`,
`templates`, `arguments`, `value`, `records`, `region`, `class`, and
`allocation`. A bare name abbreviates an
`integer` formal, retaining the printed witness bytes. Names are unique
within a parameter list. Width expressions use only earlier integer
formals. A wire formal of width n is the ordered list w[n], with
little-endian indexing, including the empty list when n = 0.

`invoke` binds `args` positionally, evaluating actuals in the caller's
lexical environment before binding any callee formal. Integer actuals use
the scalar grammar above. A wire actual is a wire name, a subscripted
wire, an array of wire actuals concatenated left to right, or exactly
`{ "range": name, "from": scalar, "to": scalar }`, selecting [from,to)
from a named bundle; bounds must satisfy 0 ≤ from ≤ to ≤ its width.
An actual's resulting length must equal its formal's evaluated width.
In a gate's `wires` array a whole formal emits all its wires in order;
this encodes `mcx(k)` as k controls followed by one target, including k=0.
`{ "each": name, "in": actual, "body": [...] }` additionally visits
wire-list elements in order, binding name as a one-wire formal for each
visit. Its binding shadows lexically and is restored after the loop.

A body actual is an ordered constructor array, captured with its caller's
lexical environment, or the name of an existing body formal. Exactly
`{ "splice": name }` expands it at that point. Substitution is
capture-free: caller references never resolve to callee locals, loop and
`each` bindings have lexical scope, and every fresh allocation identity
is derived from its expansion occurrence path (including loop iteration,
body-splice occurrence and invocation path). Allocations must not shadow a
live declaration in the same scope; a release names its matching live
allocation. An inverse traverses constructors in reverse, toggles the
adjoint on nested bodies and uses the same restored bindings at each
position; allocation declarations supply release/adjoint metadata even
when allocation and release occur in different nested constructor lists.

A symbol actual is a 64-lowercase-hex §9.2 closure hash, or a bound symbol
formal. The linked closure registry supplies that symbol's own typed
interface and constructor body; the hash must match the linked closure,
not an arbitrary supplied body. Exactly `{ "call": name, "args": [...] }`
expands that symbol under a new invocation-path element identified by the
call constructor's source point, containing fixed-binding instance and
forward semantic-call occurrence number as serialized in §11. [deps: ISA-3.7-P5, ISA-3.7-P6, ISA-11, ISA-11.1-P29]
It retains its own ordinal space starting at zero. [deps: ISA-11-P2, ISA-11.1-P29.S2]
`invoke` is recipe composition within a row; `call` is a semantic symbol
invocation and never flattens callee ordinals into the caller's space. [deps: ISA-11-P2, ISA-11.1-P29.S2]
Repeated calls have distinct paths through their `call_index`, even when
callee hash and arguments agree. [deps: ISA-11, ISA-11.1-P29.S2]

The inherited effective-control set is always passed to callees and body
splices. An `environment` actual uses the wire-actual grammar and adds
its wires to that set (set union, repeated controls counted once).
Exactly `{ "under": actual, "body": [...] }` adds controls for its lexical
body and restores the outer set afterwards. Controls apply to semantic
gates only, never allocation/release or classical events (§3.5/§4.3).
A control may coincide with a gate's explicit control, but never with a
target (including a diagonal-gate target), as §3.3 requires. Gate operands
must otherwise be distinct.

An `event` actual is exactly `{ "instruction": text, "point": text }`,
or an event formal name. `instruction` is one complete canonical §9.1
classical instruction with its operand bindings; `point` identifies its
§8.2 classical execution point. `{ "classical": opcode, "point":
event_name }` emits that bound event (its opcode must match, allowing a
concrete `.iN` width suffix) without executing or substituting its
instruction text; classical semantics and retained history are §4.1/§7.4.
Literal classical leaves retain their existing `classical`/`point` form.
A classical event is not a unitary; an `inverse` containing one requires
retained §7.4 history and is not a quantum-library matrix witness.

Consumers MUST reject the library document on arity/type/width mismatch,
unbound name or closure hash, invalid wire range, duplicate formal,
nonfinite angle, unknown constructor/key/gate, invalid gate arity,
coincident target/control, unmatched allocation/release, or cyclic
`invoke`/symbol expansion. Static integer bounds must yield finite
expansion; validation is repeated for every actual parameter tuple before
its expansion can be used. There are no implicit bindings or defaults.
Acyclicity concerns declared
recipe/symbol dependencies, not repetition of a higher-order recipe name
inside finite captured actual syntax: qloop(3, qloop(2, B)) expands to six
copies of B. Consumers expand finite actual bodies to a constructor fixpoint.

**Image binding (K21).** An `image` actual is a bound image formal or
an even-length string of lowercase hexadecimal byte pairs in data-image
byte order. The empty string denotes the absent/default-zero image,
including on a wire list whose width is not byte-aligned. Exactly
`{ "image": name, "wires": actual }` emits no leaf for the empty image;
a nonempty image requires exactly eight wires per byte; bit 8j+i of the flattened wire list is bit i of byte j (i=0..7).
It emits one X leaf for each one bit in increasing bit order, with an
empty effective-control set regardless of inherited controls. This
constructor denotes only the unconditional data-image preparation or
restoration required by §3.5/§4.6; ordinary X gates remain semantic.
The bytes are serialized in the actual, not resolved from an unbound
external image name. Image leaves have ordinary row ordinals and the
same allocation wire identities as semantic leaves. Inverse traverses
these X leaves in reverse order, still unconditional. Reject malformed
hex, unbound image or a byte/wire width mismatch. Witness: `"8102"` on
16 wires emits X at indices 0,7,9; inverse emits 9,7,0, even under a
false inherited predicate. This fixes the image binding bytes without
altering §9.2's source data-symbol identity.

**Indexed typed body templates (K22).** A `templates` actual is an ordered
array of exactly `length` objects, each with exactly `parameters` and
`body`, or the name of a bound templates formal. Each object's parameters
use the same typed formal grammar as recipes; its body uses the same
closed constructors. The array is captured in the caller's lexical
environment. Exactly `{ "apply": name, "index": scalar, "args": [...] }`
selects its zero-based element and binds positional actuals evaluated at
the apply site, with the same type/width/arity validation as invoke.
Formal bindings shadow captured names only inside that application;
all free references still resolve in the captured environment. Effective
controls are the union of captured controls, apply-site controls and
explicit environment actuals. Fresh allocations include the application
occurrence in their identity. Applications compose within the containing
row's ordinal space; they do not introduce a semantic symbol call.
Reject negative/out-of-range indices, length mismatch, unknown/duplicate
formals or invalid constructor syntax even in unused templates. Inverse
reverses the applications and adjoints each selected body using its
restored positional bindings. This permits row templates with a typed
frame formal, applied to frame_t, and a step template applied to each
successive frame without rebinding a captured free name.
Witness: two templates `(f:wire[2])` containing CX outer f[0] and CX outer
f[1], applied in index order to a, emit CX outer a[0], CX outer a[1];
the inverse emits them in reverse order. Applying to a one-wire actual
rejects. Applying the same template to distinct frame slices cannot
change its captured outer binding.

**Closure-bound argument vectors (K24).** An `arguments` formal's
`symbol` names an earlier symbol formal. Its actual is an array of actuals
in that linked symbol's own formal order, or a bound arguments name for
the identical closure hash. The vector captures the actuals' lexical
environment; validate every argument against that symbol's interface at
binding, even when no call executes. `call` additionally accepts the
bound arguments name as its `args` value; it forwards the whole vector
without reinterpreting names in the forwarding recipe's scope. Reject a
vector bound to another closure, even if the two interfaces have equal
widths. Each call still has its own invocation path and callee ordinals.

A `value` formal's `isa_type` is `iN` (N a canonical positive decimal),
`f64`, `token`, or exactly `{ "ptr": N }` with N the linked object's
positive `ptr_width`. Values use exactly §12.3 invocation encodings:
canonical unsigned decimal strings within the iN/ptr range, binary64
bit-pattern hex (including signed zero and NaN payloads for classical
f64), or four canonical nonnegative decimal strings for a token tuple.
A value may also be the name of a bound value of exactly the same
`isa_type`; widening or converting it implicitly is forbidden. Token
values carry tuples, never process-local ids. This adds no arithmetic
on classical f64 or tokens inside a recipe.

Witness: a linked interface `(wire[1], wire[3], i128, f64, token)` accepts
`[a,b,"18446744073709551617","0x7ff8000000000001",["2","0","0","0"]]`.
A forwarding recipe `(S:symbol,A:arguments(S))` with two calls using A
preserves all bindings and emits two distinct invocation paths starting
at ordinal zero. Swapping a and b rejects; 2^128 for i128, a three-part
token, or an arguments vector for a different closure rejects. This
binding rule does not replace §3.3's source interface region shape/role
validation or the §9.2 linker obligation that the registry interface and
body match the supplied closure hash.

**Oracle invocation context (K77).** An oracle's catalog argument vector
contains exactly its declared parameters, flattened in header-group order
`in`, `tgt`, `fault`, `mem`, `args` (§16.2); empty groups add no entries.
The invocation token is not an additional formal or vector entry.
Before concrete expansion, consumers MUST supply and validate the
explicit source-binding channel `oracle_invocation`, preserve it through
the captures below, and reject missing, ill-typed or source-inconsistent
context. The channel is a record with exactly one field, `token`, of
K24's `value` type with `isa_type:"token"`: four canonical nonnegative
decimal strings in §5.4 order `(B, heap_limit, stack_limit, depth_limit)`,
resolved from that source call's `tk` and
validated for the linked callee under §5.4. A root oracle instead binds
the explicit launch/schedule request budget. Unresolved source parameters
retain §11's admission/concrete-check staging.

This channel is explicit input to the linked source-body builder, outside
the catalog JSON and positional actuals, not an implicit name, default,
new constructor key or token arithmetic inside a recipe. The registry
binds the closure's source/interface; its builder instantiates the
source-derived constructor body separately for each invocation, using
this tuple and the linked source/layout to derive B, frames and every
token-dependent limit or width supplied to `oracle.construct`.
A registry keyed by closure hash alone cannot fix one invocation budget.
The context is associated with the full §11 invocation identity, not
with the closure hash or positional vector values alone.

Source binding captures the channel with the corresponding `arguments`
actual and with any body/template adapter containing that call. Forwarding
an arguments name through `invoke` or `call`, or splicing/applying a
captured body/template, preserves that captured channel; unrelated
caller/apply-site context cannot replace it. The qinplace adapters capture
the source `tk` for both calls. Each nested source oracle call resolves
its own `tk` in its own fixed bindings, then restores the outer context.
Source-adjoint adapters retain their captured tuples and perform §5.3
replacements before recipe instantiation (K62). Inverse traversal retains
each instantiated forward call's channel and forward occurrence identity
while reversing/adjointing its operations (§11). None of these captures
adds a leaf, ordinal, source parameter or closure-hash component.

**Two-token witness.** Use §16.3 example 1's `inc8` closure and two source
calls `oracle_call @inc8 tk2 (x) t f () ()` and
`oracle_call @inc8 tk3 (x) t f () ()` in one action expansion, with
`tk2=(2,0,0,0)` and `tk3=(3,0,0,0)`. Both positional vectors are `[x,t,f]`;
their captured contexts are respectively `{"token":["2","0","0","0"]}`
and `{"token":["3","0","0","0"]}`. The linked closure hash is identical.
The first construction has two frames and XORs `(0,FAULT_BUDGET_STEPS)`
into `(t,f)`; the second has three frames and XORs `(x+1 mod 256,0)`.
Starting from `(t,f)=(0,0)`, the final pair is `(x+1 mod 256,1)`.
Their §11 edges are distinct: separate source points each have
`call_index=0`; two calls within a single source-row forwarding expansion
instead have forward `call_index=0,1`. Inverse traversal retains those
identities and tuples and restores the complete input. Neither binding
adds a token to `inc8`'s empty signature `args` list or changes its hash.

**Ordered descriptors (K25).** A `records` formal has exactly `name`,
`type`, `fields`, `order`. `fields` is an ordered typed formal list;
its types are `integer`, `wire`, `region`, `class`, `allocation`, or
`image` (K21, for source data-image descriptors).
A field's width/shape expressions may use enclosing earlier integer
formals and earlier integer fields, never later fields. `order` is an
array of distinct integer field names. An actual is an array of objects
whose keys are exactly the field names, or a bound records name with the
identical field schema and order. Each field actual resolves in the
actual's captured lexical environment; earlier integer fields additionally
bind width/shape expressions. Forwarding preserves resolved identities,
revalidates widths against the receiving enclosing integers, and never
resolves a wire name again. With nonempty `order`, the tuples of those
fields must be strictly increasing lexicographically; with empty `order`,
array order is normative. Empty arrays are valid.
`{"visit": name, "body": [...]}` visits records in array order, binding
all their fields lexically for that body, shadowing outer names across
all types and restoring them afterwards. An inverse visits the same
records in reverse order and adjoints each body. No record iteration
emits a leaf by itself. Reject extra/missing fields, an invalid schema,
order mismatch, duplicate/out-of-order keys, or any invalid field actual,
even for an unvisited list. Record iteration and K22 template application
share the same capture, effective-control and occurrence-identity rules.

The following descriptor schemas bind source metadata, rather than
caller-supplied circuit bodies. Source formation MUST check every record
against the linked source declarations/layout before expansion:

* A byte-layout list has integer fields `base`, `extent`, then
  `cells:wire[8*extent]`, ordered by `base`. Bases/extents are nonnegative
  mathematical integers, extents positive. Form the list by partitioning
  `[0,2^H)` at every mapped interface region endpoint. Each mapped interval
  binds its region's cells, flattened by increasing cell index and then
  LSB-first bit index. Each remaining maximal interval binds the same
  address slice of ordinary `mem`. Adjacent mapped intervals remain
  separate records. Require exact coverage, no overlap and no gap; mapped
  cells have W=8 as §7.2 requires. Byte `base+j` is exactly wires
  `cells[8*j .. 8*j+8)`. Ordinary `mem` under a mapped interval is never
  selected by an access. Interface shape and origin use K26.
* An activation location list has `id`, `width`, `slot` integers followed
  by `location:wire[width]`, ordered by `id`. The ids and widths are
  exactly §3.7's global ids and declared widths. For a selected instance,
  `slot` is its zero-based declaration index in L_f, including parameters
  and the result name; for a closure delivery list it is the declaration
  index within the location's own instance. A capture list has `position`,
  `width` integers followed by `source:wire[width]`,
  `parameter:wire[width]`, `capture:wire[width]`, ordered by `position`.
  Positions are 0..m-1 in source argument order; parameter and capture
  are the corresponding callee location and frame displacement slot.
  The stack low-width slice for location slot j starts at
  `(old_sp+3+j)*W_cell` in C2 and `(restored_fp+3+j)*W_cell` in R3;
  higher cell bits are untouched. Delivery scans the complete closure
  list in global id order. Reject records inconsistent with those source
  mappings. These lists add no locations for token/classical/region
  arguments; those remain K24/K26 fixed bindings.

* A construction state list has `width`, `initial` integers, `I:image`,
  `storage:allocation`, with empty `order` (array order). Each storage
  identity is distinct, clean and exactly `width` bits; its class is
  `any` for the implicit §5.2 state. In allocation order the list is:
  pc, pc-prime, faulted, code, result_val; then heap_used, atop, sp, fp,
  depth, ordinary mem, stack when layout state exists; locations in global
  id order; local regions in declaration order; alloctab when layout state
  exists; frames 0..B-1. Omit only the layout state excluded by §7.2's
  memoryless-object rule. Counter widths/values are the reference widths
  and initial values of §3.7; all other non-image initial values are zero
  except alloctab pre-entries. [deps: ISA-3.7] A table cell packs base[ptr_width],
  size[ptr_width], live, pinned, in that LSB-first order; pre-entries are
  in §3.7's layout order and unused entries are zero. Image-bearing mem
  and local regions have initial=0. Ordinary mem's I is exactly 2^H
  bytes, initially zero, with each global's image overlaid at its layout
  base; bytes hidden by mapped interface regions remain zero. A local
  region's I is its exact bound data image, or empty for absent/default
  zero. Every other record has I empty and initial
  the nonnegative integer encoding of its initial bit vector, strictly
  below 2^width. Mapped interface regions are borrowed inputs, never
  acquired by this state list. A separate frame list has `index` integer
  and `frame:allocation`, ordered by index; it contains exactly B entries
  indexed 0..B-1, referring to the identical frame handles in the state
  list, each with §3.6's fixed frame width and field order. [deps: ISA-3.6] Reject any
  mismatch of source state, image, width, class, order or identity. The
  construction acquires/initializes this list, invokes the catalog `step`
  once per frame, commits, then reverses frames and initialization before
  releasing the list in reverse order; source row/successor templates
  supply rows, never a replacement dispatcher or construction body. [deps: ISA-5.2-P3, ISA-3.6, ISA-11.1-P5, ISA-11.1-P22]

Witness: byte records `(base=0,extent=1,cells=a[8])` and
`(base=1,extent=2,cells=b[16])` bind addresses 0,1,2 to a[0..8),
b[0..8),b[8..16), respectively. Visiting X on each first bit emits
X a[0], X b[0]; inverse emits X b[0], X a[0]. A two-bit location
id 0/slot 0 followed by a one-bit location id 1/slot 1 exchanges only
the low 2 and low 1 bits of stack cells old_sp+3 and old_sp+4;
return/inverse address them at restored_fp+3 and restored_fp+4.
Exchanging the two record positions rejects for id order.
A construction witness with rows `loc = lift.add x y; lift.retval loc`
commits fault 1 for B=0/1 and `(x+y) mod 2^W` into the arbitrary target
for B>=2, preserving inputs and cleaning every state/frame allocation.
A local image 81 emits unconditional X at cell bits 0,7 and restores them
before release, including under a false external predicate.

**Source region bindings (K26).** A `region` formal has exactly `name`,
`type`, `address`, `cell`, `role`; address/cell are integer expressions
using earlier integers, with A>=0, W>0, and role is `in` or `mut`.
Its actual is a bound region name or exactly
`{"address": A, "cell": W, "role": role, "origin": origin, "cells": actual}`.
A and W in the actual are nonnegative/positive integer literals, role
must equal the formal role, and the cell wire actual has exactly 2^A*W
wires, in cell-index/LSB-first order. Both shape components must equal
the formal components, even if a different shape has the same total
width. Origin is `interface:` followed by the canonical source operand
name for a caller-owned interface, or `local:` followed by the local
source declaration's NAME token. Each suffix is the exact canonical
§16.1 NAME token, without a sigil. Its binding together with the ordered
cell wire identities identifies the source occurrence (including repeated
invocations); forwarding preserves both. The suffix
is checked against the linked source binding; a local origin cannot be
substituted for an interface origin by changing its string. A region
formal can be used as its flattened cells in any wire actual, while
forwarding it as a region retains shape, role, origin and wire identities.
K24 argument vectors validate regions in the linked signature's slot
order just as wires/values; source role/overlap restrictions remain §3.3.
Lifted calls accept only their permitted mapped/parameter origins (§4.2);
action calls may accept local regions where §3.3 permits them. No rule
infers source shape or role from total bit width.
Witness: a region[1,3] in local:r over six wires forwards unchanged through
two K24 calls. Binding it to region[0,6] in or region[1,3] mut rejects,
despite equal total width. Invalid/missing origins also reject.

**Classes and allocation declarations (K27).** A `class` formal has
exactly `name`,`type`. A class actual is a bound class name or exactly
`{"class": text}`, where text is the exact source class spelling (`any`
included), never an empty string or a resolved substitute class.
`{"declare": name, "width": scalar, "class": actual, "state": state,
"body": [...]}` reserves a fresh allocation identity with nonnegative
width, that class, and state `clean` or `borrowed`. It emits no leaf;
it binds an initially inactive allocation declaration for its lexical
body, including captured actual bodies. It may not shadow any binding.
An `allocation` formal (exactly `name`,`type`) passes that declaration
by identity, including metadata and live/inactive status. Exactly
`{"acquire": name}` emits its unconditional allocation and changes it
from inactive to live; exactly `{"relinquish": name}` emits its matching
unconditional release and changes it from live to inactive. An acquire
requires inactive, a relinquish requires live, and the declaration must
be inactive when its lexical body exits. While live, its name is a wire
actual of its declared width, including for subsequent caller constructors
after `invoke` returns; while inactive any wire use rejects. Captures and
invocations share the same status, not a copy of the lifetime. Inverse
exchanges acquire/relinquish, using the same declaration metadata and
occurrence identity. Reacquisition denotes a new allocation occurrence,
with fresh identity even within one declaration. Clean release requires
zero; borrowed release requires restoration on the full domain (§5.6),
never zero. These are user/instruction allocation results; internal
library scratch still obeys the clean LIFO rule below. A declaration
or allocation formal listed in `scratch` when acquired marks that entire
allocation lifetime as library scratch; the mark follows its identity
through captures and invokes, requires clean state and cannot be removed
by releasing through a different formal name. Allocations are
unconditional even under a false inherited control.
Witness: declare out[2] of class ancilla; invoke an allocation recipe on
out; apply two X gates to out[1] in separate caller/callee bodies; invoke
its release recipe. All leaves refer to the one live allocation identity
and release it clean. Wire use before acquisition/after release, double
acquisition, unmatched release or leaving the declaration live rejects.
A borrowed declaration preserves the exact class and both initial values
of every borrowed bit; no conversion to class any is permitted.

**Angles and quantum witnesses (K20).** An `angle` actual is a bound angle
formal or a finite binary64 value. Reusing §12.3's bit-pattern encoding:
`f64` is `0x` followed by exactly 16 lowercase hex digits of its IEEE 754
binary64 bit pattern, most significant nibble first (so −0 and NaN payloads
are not lost). Angles additionally reject NaN and infinities (§3.1).
Only `rx`, `ry`, `rz` have `params`, an array containing exactly one angle;
other §4.4 gates have no angle parameters. No recipe arithmetic on angles
is permitted. `inverse` negates each rotation angle by toggling bit 63,
including signed zero, and exchanges s/sdg and t/tdg as §5.3 requires.

For h, phase gates s/sdg/t/tdg/cz, and rotations, correctness is equality
of the §14.2 unitary (using §4.4 matrices), column by column on the full
computational basis of all recipe interface wires, with scratch initially
clean and finally clean. Arbitrary targets, controls and borrowed inputs
are included. This full-basis unitary is the witness extending T3's
basis argument; non-permutation leaves MUST NOT be certified by a basis
permutation simulator. Exact algebraic amplitude checks apply to Clifford+T
leaves. For arbitrary binary64 angles a numerical checker must state its
round-trip criterion and error bounds; numerical agreement is evidence,
not a proof of ε=0 for arbitrary transcendental matrix entries.

**REF-BINDING / REF-QUANTUM witnesses.** With formals
`[{"name":"N","type":"integer"},{"name":"w","type":"wire","width":"N"},
{"name":"theta","type":"angle"},{"name":"B","type":"body"}]`, actuals
`[1,{"range":"a","from":0,"to":1},"0x8000000000000000",[]]` bind
w[0]=a[0], θ=−0 and an empty body. Replacing the range end by 0 rejects
for width mismatch. Splicing a body allocating/releasing `tmp` twice gives
two distinct scratch identities even if the callee also declares `tmp`.
An inverse rx at `0x3ff0000000000000` emits rx at
`0xbff0000000000000`. For `w=[a[0],a[1]]` and t=a[2],
`{"gate":"mcx","wires":["w","t"]}` emits exactly those three operands;
`each` over w visits a[0] then a[1]. Two calls to the same closure have
separate invocation paths, each starting ordinal zero. H's two columns
are (1,1)/√2 and (1,−1)/√2; S's second column is (0,i), distinguishing
these witnesses from a bit permutation and fixing global phase.

Number every emitted leaf (including allocation/release and classical
leaves) 0,1,… within the containing row/instruction, after instantiating
widths and static loop counts, before any §5.7 transformation or target
scheme expansion. Calls have their own invocation-path element and
callee ordinal space; `step` and `phase` select the invocation's oracle
step as in §11. The inverse of a row visits the forward ordinals in
reverse order, retaining each ordinal under `phase: rev`; it does not
renumber them. Scratch identity is `(invocation chain, step, recipe
expansion path, allocation ordinal, bit index)`; the chain includes
fixed-binding instance and semantic-call occurrence, and allocations in
repeated bodies have their expanded occurrence path. [deps: ISA-3.7-P5, ISA-11-P5, ISA-11.1-P9] All library scratch is
clean, allocated unconditionally and released in reverse allocation
order after uncomputation; borrowed user operands remain borrowed.
`removable` is an explicit array of leaf ordinals and MUST be empty
for every recipe in `ref` version 0.9. No transformation
may infer extra permission from a zero-valued basis input. Motivation
(0.8 §11): "MUST keep the ordinals of the operations they keep and MAY
remove only operations the library marks removable"; §17 item 7:
"clean scratch released in reverse order".

The reverse-allocation release rule governs recipe scratch; an instruction whose own semantics fix a release sequence (qinplace per §4.5: `qfree t; qfree f`) keeps that sequence, and its recipe MUST reproduce it exactly. [deps: ISA-4.5-P5, ISA-11.1-P29.S5]

**Instruction-release witness (K28).** This is a synthetic constructor-binding
witness whose two callee fixtures each contain one CX at callee ordinal 0;
it illustrates caller ordinals and release order, rather than the complete
`ref` expansion or cost of an ISA oracle. [deps: ISA-4.5-P5, ISA-11.1-P9, ISA-11.1-P22, ISA-11.1-P29.S1, ISA-11.1-P29.S2]
For n=1, F=4 the private instruction trace is alloc t[1] at row ordinal 0,
alloc f[4] at 1, call G, swap x/t at 2, call H, release t at 3,
release f at 4, with
each call's complete expansion in its own ordinal space. [deps: ISA-4.5-P5, ISA-5.4, ISA-11.1-P29.S1, ISA-11.1-P29.S2]
The certified pair leaves t/f clean for both x values and both effective
controls; allocations and releases are unconditional. [deps: ISA-4.5-P5, ISA-3.5, ISA-4.3]
Recipe-internal scratch within either call still releases in reverse
allocation order. [deps: ISA-11.1-P29.S5]
Raw inverse traversal retains forward ordinals, reverses their order and
adjoints the leaves; it describes reversal of an already expanded machine
row, rather than formation of a scheduled action adjoint. [deps: ISA-5.3, ISA-11.1-P29.S3]

**Scheduled action adjoint (K62).** Before recipe instantiation, form an
action adjoint using the §5.3 instruction replacements in reverse source
order, and bind the `adj` recipe's body B to that source-adjointed body;
`adj` splices B without applying a leaf inverse. [deps: ISA-5.3-P4, ISA-11-P2, ISA-11.1-P5, ISA-11.1-P29]
Each replacement instruction has its own forward ordinal space, so
`adj(qinplace G H)` instantiates `qinplace H G` with allocations t then f,
exchange, and releases t then f in caller ordinals 0,1,2,3,4 for n=1,
F=4; its calls are H then G, each with a separate callee space. [deps: ISA-5.3-P4, ISA-4.5-P5, ISA-11.1-P29.S1, ISA-11.1-P29.S2]
The `qif` replacement still reverses its complete §4.6 expansion,
including unconditional lifetimes. [deps: ISA-5.3-P4, ISA-4.6-P7]
Schedulers, executors and estimators use this same action-adjoint trace;
raw `inverse` constructors retain forward ordinals when reversing an
already expanded row, including inverse oracle steps. [deps: ISA-11-P2, ISA-11.1-P29.S3, ISA-5.2-P3, ISA-5.3-P4]
For an alloc entry at this instruction with `generated: 0` and class
`special`, with other allocations resolving to class `default`, the
private allocations are t[1]:special and f[4]:default. [deps: ISA-11-P5, ISA-11-P6, ISA-4.5-P5]

**Decomposition set.** The §17 item 7 defaults are made explicit below. Bit
loops below increase from the least-significant bit. To make Boolean
recipes deterministic, use no common-subexpression elimination: visit
every Boolean expression tree in left-to-right postorder, giving each
internal node a fresh clean scratch bit. NOT(a) uses X d; CX a d,
XOR(a,b) uses CX a d; CX b d, AND(a,b) uses CCX a b d. OR(a,b) is the
ordered tree XOR(XOR(a,b),AND(a,b)); repeated operands are separate tree
occurrences (coincident AND operands reduce to a single CX so the gate
has distinct operands). XOR the root into the destination, then reverse
all compute gates and release scratch in reverse allocation order.
Constants are zero or X of a clean bit. All formulas use old source
values captured before an assignment/exchange. External effective
controls apply to the resulting semantic gates, not allocations; scratch
computations may be unconditional provided their compute/uncompute pair
is balanced when the external control is false (§3.5, §4.3).

| Family | Ordered expansion | Motivating 0.8 sentence |
|---|---|---|
| Copy, XOR, exchange; native gates | `qxor`: CX s[i] t[i]; `qcopy`: allocate then the same; `quncopy`: the same then release; `qexch`: SWAP a[i] b[i]. Keep each §4.4 gate as a leaf; target schemes expand later. | §4.5: "`cx s[i] t[i]`" and "`swap a[i] b[i]`"; §8.3: "Every template gate MUST itself match a gates entry". |
| Ripple add/sub and comparisons | c[0]=0; p[i]=a[i] XOR b[i]; sum[i]=p[i] XOR c[i]; c[i+1]=(a[i] AND b[i]) XOR (p[i] AND c[i]); compute each bit in this order, XOR sums out, reverse scratch. Subtraction adds bitwise NOT b with c[0]=1. Unsigned a<b is NOT the final subtraction carry; equality is the AND of NOT(a[i] XOR b[i]) in increasing-bit left-associated order. `ule` is OR(ult,eq); signed comparison selects sign(a) if signs differ, else ult. | §17 item 7: "ripple-carry adders and comparators"; §4.1: "wrap"; §3.7: prospective sums use "no wrap" (retain the extra carry for those). |
| Other arithmetic, casts, select | AND/XOR/OR use the Boolean trees above; select emits ((NOT p) AND b[i]) XOR (p AND a[i]). Multiply folds shifted partial products in increasing multiplier-bit order through ripple add modulo 2^N. Shifts scan shift amounts j=0..N−1, equality-selecting the corresponding source bit; ≥N produces zero. Sign-extend replicates the high source bit, zero-extend supplies zero, truncate drops high bits. Division uses restoring unsigned long division, scanning dividend bits from N−1 to 0: append that bit to an N+1-bit remainder, compare with the zero-extended divisor, subtract iff ≥, and emit that predicate as quotient bit. Signed forms conditionally negate operands, divide magnitudes, negate quotient iff signs differ and remainder iff dividend negative; row fault predicates precede these outputs. | §4.2: "w (under ¬flag)" and the div fault predicates; §4.1 wrap/shift rules and signed MIN/−1 fault; §3.3 equal operand widths. |
| Linear inrange and flags | For table entries i=0..2^A_tab−1 compute `(i<atop) AND live_i AND (base_i≤p) AND (p+n≤base_i+size_i)` in that parenthesisation at §4.2's widened width; left-fold OR from false, then uncompute entry scratch. `free` and allocator/call fault trees use their explicit §4.2/§3.7 formula and slot order (including 0.9's E17.13 correction). | §4.2: "inrange(p,n) = ∃ i < atop ..." and "no wrap"; §17 item 7: "linear inrange scans". |
| Address dispatch and multiplexers | Scan every address i in increasing numeric order; compute equality to i, copy/exchange cell bits in increasing order under that bit, uncompute equality before the next i. Lifted memory chooses the §7.2 mapped region in address order and scans its cells in increasing address order; captures use old addresses before exchanged counters. | §4.6: "for each cell i: under a == i"; §17 item 7: "one-hot address dispatch"; §3.7 C1–C5/R1–R5. |
| Row, oracle and structure | Compose these recipes in the printed §3.6 step order, §4.2 slot order, §3.7 activation order, §5.2 allocate/forward/commit/reverse/release order. `qif`, loops, local-region image X gates and `qinplace` use the literal sequences of §4.5–§4.6, incorporating 0.9's explicit parameters. Cleanup `reverse` adjoints that sequence; `recompute` follows §6.4. | §11: "Above gate level the order is fixed by §3.6, §4.2, §4.5–§4.6 and §5.2"; §5.2: "run the inverse step for t = B..1, then release (1)". |

The permutation algorithms define exact permutation circuits, preserving
every input required by the row and cleaning scratch; circuit correctness must still be checked
against full-domain T3 witnesses and §5.7, not inferred from costs or
names. Complete catalog: **219 recipes**; envelope SHA-256
`5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197`. [deps: ISA-11.1-P2, ISA-11.1-P3, ISA-11.1-P28, ISA-11.1-P29]
Publication follows acceptance. [deps: ISA-11.1-P1, ISA-11.1-P2] In particular this is
not permission to publish a partial library that omits division, stack,
coherent control, memory or any instruction.

**ISA-REF-LIB witness**

```json
{"isa":"0.9","name":"ref","recipes":[{"kind":"qxor","operations":[{"gate":"cx","ordinal":0,"wires":["s[0]","t[0]"]},{"gate":"cx","ordinal":1,"wires":["s[1]","t[1]"]}],"removable":[],"scratch":[],"source":"0.8 §4.5","width":2}],"version":"0.9"}
```

This is a single instantiated recipe witness, **not** a complete
library document for binding a schedule. Its envelope is the four-line
envelope above with this entire JSON as line four. It has two ordinals,
0 and 1, no scratch and no removable operations. For every two-bit s,t
(16 tuples), the result is `(s, t XOR s)`; reversing visits ordinal 1
then 0 and restores the entry tuple. Its hash identifies only these
witness bytes, not `ref@0.9` as a whole.

Witness envelope SHA-256: `299510fd67cc626fdcbcc10adcd40730f9af294ba596d86fb25fd31be08a5c7f`.

## 12. Certificate (cert 0.9; JCS)

### 12.1 Claims

| kind | payload | checker obligation |
|---|---|---|
| `exhaustive` | `domain` (§12.2); `expected`: `"oracle"` \| `{ "table": [...] }` \| `{ "program": closure_hash }` \| `"inverse_pair"` | re-execute every domain element on the reference interpreter / expected program; compare full tuples. For `"inverse_pair"` (the claim of an `inverse_pairs` entry, §12.3): for every element (x, ins, mem cells, args) run g and ginv at the entry's tuple, token-typed arguments at their `arg_tokens` tuples, and require both fault-free, ginv(g(x)) = x and g(ginv(x)) = x; the bundles and regions components MUST be the full domain of g's `in` and `mem` slots (the `args` component lists the covered classical values) |
| `sampled` | `domain`; `expected`: `"oracle"` \| `{ "table": [...] }` \| `{ "program": closure_hash }`; `subject` and invocation binding as below (K13); `sampler`: `{ "algorithm": "xoshiro256**", "seed": [4 decimal strings, not all zero], "count": n }` | independently replay both sides of the declared relation on every sampled element; compare full tuples; always **evidence**, even if every element is drawn |
| `structural` | `{ "rule": "translation_lemma" \| "inverse_pair_library" \| "adjoint_table", "subclaims": [indices], "witness": … }`; for `translation_lemma`: `{ "V": [points], "W": [points], "X": [wires], "B": [wires], "frame": [first point, last point] }`; for `inverse_pair_library`: `{ "library_closure_hash", "claim_index" }`; for `adjoint_table`: `{}` | check the rule's side conditions syntactically against the object and the subclaims' results |
| `numerical` | `{ "subject": { "closure_hash", "variant", "inherited_controls", "schedule_hash" }, "metric": "operator_norm", "precision_bits": n, "bound": decimal }` | **checker-computed, for every invocation context of the subject** (below): build the realised unitary U of that invocation (the region's realisation under the root schedule at that path, with its resolved classical arguments, budget, epsilon shares and cleanup choices, and `inherited_controls` control wires prepended) and the reference unitary V (the region's §5.3 semantics with the same arguments, controlled on the same wires) at the subject's signature widths in interval arithmetic at `precision_bits` (basis order = allocation order, controls first), form interval enclosures of `V†U − I` entrywise, derive the operator-norm bound as the Frobenius-norm upper bound in interval arithmetic, and verify it is ≤ `bound`; the claim holds iff it holds for every context |
| `channel` | `{ "subject": as above, "metric": "diamond", "precision_bits", "bound", "dual": [ { "Y": interval Hermitian matrix, "mu": decimal } … ] }` | for every invocation context of the subject, in enumeration order, verify its dual witness for the **diamond-norm SDP** below in interval arithmetic and `mu` ≤ `bound` (one witness per context; too few witnesses: reject) |

**CLAIM-REPLAY** (K13; b-isa-spec-9uy, from bennett-vm-clw).
Sampled observations remain evidence under the following replay contract.

**Comparison relation.** `exhaustive` and `sampled` claims
MUST name their `subject: { closure_hash, variant, inherited_controls,
schedule_hash? }` and an explicit `expected`; there is no implicit
self-comparison or default expected relation. Without a schedule the
left side is the subject's reference semantics at the bound invocation;
with one it is that invocation's realised operation. `expected: "oracle"`
compares the realised operation to §5.2's reference oracle map and
requires `schedule_hash`. [deps: ISA-5.2, ISA-11, ISA-12.1-P11] `expected: {program: H}` independently runs
the reference semantics of linked closure H at the **same** arguments,
budget and interface tuple; its signature MUST be compatible.
`expected: {table: rows}` compares to the explicit full-tuple rows
below. The checker MUST compare every interface output, preserve inputs
and borrowed systems, and verify clean workspace and exact +1 basis
phase for a permutation assertion (T3); matching a target or fault
projection alone, or a producer's claimed verdict, is insufficient. [deps: ISA-14.3-P3, ISA-5.6]
For a non-permutation realisation, use the existing numerical/channel
claims rather than labeling basis observations a permutation proof. [deps: ISA-12.1-P4, ISA-12.1-P5, ISA-14.2]
K4's `expected: "inverse_pair"` retains its separate two-composition
relation and entry/domain bindings; it is not a sampled proof option.

**Table tuples.** Each table row is `{ before: tuple,
after: tuple }`. A tuple is `{ bundles: ["<unsigned integer>", …],
borrowed: ["<unsigned integer>", …], regions: [["<cell>", …], …] }`.
`bundles` lists inherited control wires first (each width 1), then all
signature bundles in operand order, **including arbitrary initial
oracle target and fault bundles**. `borrowed` lists dirty bundles in
allocation order, with widths fixed by the checked borrow lifetimes;
`regions` lists interface regions in signature order, every cell in
increasing address order, each as an unsigned W-bit integer. All
integers use canonical decimal strings, within the declared widths;
no cells, inputs or unchanged components may be omitted. Workspace is
not an interface component and MUST finish zero. Rows are in domain
enumeration order, one per distinct declared domain element (including
for `sampled`); duplicate/missing/out-of-range rows reject. This favors
an explicit table; `{program: H}` provides the compact relation when a
full table is large. Sampling draws with replacement using the existing
sampler; coverage counts distinct drawn elements, not draws. A mismatch
rejects; success is always `evidence` with that distinct covered fraction
of D, including when the draws happen to cover all of D.

**CLAIM-REPLAY witness**

```json
{
  "invocation":{"args":["2"],"budget":["2","0","0","0"]},
  "row":{
    "before":{"bundles":["1","2","3"],"borrowed":["1"],"regions":[["2","1"]]},
    "after":{"bundles":["1","1","3"],"borrowed":["1"],"regions":[["2","1"]]}
  },
  "wrong_row":{
    "before":{"bundles":["1","2","3"],"borrowed":["1"],"regions":[["2","1"]]},
    "after":{"bundles":["1","2","3"],"borrowed":["1"],"regions":[["2","1"]]}
  },
  "changed_arg_after":{"bundles":["1","0","3"],"borrowed":["1"],"regions":[["2","1"]]},
  "short_budget_after":{"bundles":["1","2","2"],"borrowed":["1"],"regions":[["2","1"]]},
  "sampler":{"algorithm":"xoshiro256**","seed":["1","0","0","0"],"count":4},
  "widths":{"bundles":[2,2,4],"borrowed":[1],"regions":[[8,8]]},
  "sample_count":4,"distinct_samples":1,"covered_fraction":"1/33554432","verdict":"evidence"
}
```

The subject is a two-row oracle body `r = lift.add x a;`
`lift.retval r`, widths x = target = a = 2 and fault = 4, with a preserved
one-bit dirty bundle and an unused two-cell, eight-bit `in` interface
region; no inherited controls. [deps: ISA-5.4, ISA-7.2, ISA-12.1-P8] A legal layout has ptr_width=2, H=2, A_tab=1, S_cells=0,
null_size=1, no globals, the interface mapped at base 1 with extent 2,
heap_base=3 and heap_limit_max=0; the token is (2,0,0,0), and the unused
mapping is retained even though the body has no load/store. [deps: ISA-7.1, ISA-7.2, ISA-5.4]
The **body** does not access memory;
the interface cells remain part of D. [deps: ISA-7.2, ISA-12.2] The reference payload is
(1 + 2) mod 4 = 3: target 2 XOR 3 = 1 and fault 3 XOR 0 = 3.
The singleton declared domain is precisely `row.before`, within the
full 25-bit D (2+2+4+1+16 bits). [deps: ISA-5.4, ISA-7.2, ISA-12.1-P8, ISA-12.2] Four samples of singleton components draw no generator
words and cover one of 33554432 full tuples. [deps: ISA-12.1-P8, ISA-12.1-P13, ISA-12.2] An identity implementation
would agree with itself but MUST fail against `row`; using `wrong_row`
also MUST fail. At argument 1 the target is 2 XOR 2 = 0; at B = 1 the
payload is zero and fault is 3 XOR 1 = 2. A certificate for argument 2,
B = 2 cannot be replayed as either of those invocations. The printed
rows illustrate the relation; bound closure/object hashes still have
to be supplied in an actual certificate, not invented for this witness.

**Invocation contexts.** A subject denotes the set of invocations of
the region `closure_hash`, with the given `variant` and `inherited_
controls`, in the root schedule `schedule_hash`: every invocation of
the region in the root realisation's complete invocation tree —
including invocations that no schedule entry names and defaults alone
cover (§11) — with the classical arguments, budget, `epsilon_share`s and
cleanup realisations resolved for it. An invocation's **context key** is
its concrete invocation chain (§11), outermost first, each element `{
"symbol", "point", "iteration", "instance", "call_index" }` with every
iteration index, fixed-binding key and forward semantic-call occurrence
resolved
and, for an element inside an oracle, `"step"` (1..B) and `"phase"`
(`"fwd"` or `"rev"`) added; contexts are enumerated in increasing
bytewise order of the JCS encodings of their keys (wildcard selectors
play no part). [deps: ISA-3.7-P5, ISA-3.7-P6, ISA-9.2-P1.S3, ISA-11, ISA-11.1-P9]
Every claim bound and every
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
half of it). *(non-normative)* With this input-first Choi convention
Tr_out traces the second factor, Tr[(ρ ⊗ I)Y] = Tr[ρ Tr_out(Y)]; a
primal formulation that labels the input factor ρᵀ ranges over the same
set of density matrices, so the bound is unchanged. Encoding: `Y` is a row-major array of entries `[re_lo, re_
hi, im_lo, im_hi]` (decimal strings). **Positivity test.** The checker
proves each of the three matrices **positive definite** by an interval
Cholesky (or Hermitian LDL†) factorisation in which the interval lower
bound of every pivot is strictly positive, and rejects otherwise; no
other test is admitted (nonnegative leading principal minors do not
imply positive semidefiniteness: diag(0, −1)). Producers make witnesses
strictly feasible by replacing Y with Y + δI and mu with mu′ = mu + δ·(d
+ 1) for a small rational δ > 0 (any mu′ > mu + δ·d suffices): then Y ±
J(Φ) ⪰ δI ≻ 0 and, since Tr_out(Y + δI) = Tr_out(Y) + δ·d·I, mu′·I −
Tr_out(Y + δI) ⪰ δI ≻ 0; ‖Φ‖◇ ≤ mu′, which MUST be ≤ `bound`. That
recipe assumes an exactly feasible witness. For a numerically obtained
witness the producer first certifies lower bounds −η₊, −η₋, −η_s on the
smallest eigenvalues of Y − J(Φ), Y + J(Φ) and mu·I − Tr_out(Y), chooses
δ > max(η₊, η₋, η_s) and publishes Y′ = Y + δI and mu′ = mu + (d + 1)·δ:
then Y′ ± J(Φ) ⪰ (δ − η±)I ≻ 0 and mu′·I − Tr_out(Y′) ⪰ (δ − η_s)I ≻ 0.
These margins make the matrices positive definite; they do not make the
interval test conclusive: every pivot enclosure the checker computes at
`precision_bits` MUST still have a strictly positive lower endpoint,
else the checker rejects (no fixed allowance such as 2^−`precision_bits`
bounds the interval error, which depends on d and conditioning). **Interval
arithmetic** at `precision_bits`
means every operation rounds outward to `precision_bits`-bit binary
rationals; transcendental entries (`rx ry rz`) are enclosed by a Taylor
series with the Lagrange remainder bound (§17 item 8 fixes the term
count). A `numerical` or `channel` subject's `schedule_hash` is required:
it names the realisation the claim is about. K13 also requires it for
`expected: "oracle"`; standalone reference relations use the explicit
invocation binding instead.

**Sampling.** For each domain component with range size R = hi − lo + 1,
assemble m = ⌈⌈log₂ R⌉/64⌉ consecutive generator words (least-significant
word first) into an integer, reduce modulo 2^⌈log₂ R⌉, reject and redraw
if ≥ R, add `lo`; components are consumed in enumeration order.

**Invocation identity witnesses (K63).** For `qinplace @G @G tk x`
at action A's `entry:0`, the two call edges below are distinct even with
identical arguments, and each prefix is also a round-trippable schedule
path selecting that invocation's descendants. [deps: ISA-4.5-P5, ISA-11-P5, ISA-11.1-P9, ISA-12.1-P11]
For two `lift.call` sites forwarding root token positions 0 and 1 into
lproc f, whose `entry:0` contains one `lift.oracle_call`, the next two
keys distinguish the row instances at outer step 1, even if token values
happen to agree. [deps: ISA-3.7-P5, ISA-3.7-P6, ISA-9.2-P1.S3, ISA-12.1-P11]
The `instance`/`call_index` fields are present in both schedule path
prefixes and context keys; context-only step/phase fields below are
supplied separately as §11 selectors in the schedule form. [deps: ISA-11-P3, ISA-11-P5, ISA-12.1-P11]

```json
{
  "qinplace_context_keys": [
    [
      {
        "symbol": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "point": "entry:0",
        "iteration": [],
        "instance": [],
        "call_index": 0
      }
    ],
    [
      {
        "symbol": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "point": "entry:0",
        "iteration": [],
        "instance": [],
        "call_index": 1
      }
    ]
  ],
  "lproc_context_keys": [
    [
      {
        "symbol": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
        "point": "entry:0",
        "iteration": [],
        "instance": [
          0
        ],
        "call_index": 0,
        "step": 1,
        "phase": "fwd"
      }
    ],
    [
      {
        "symbol": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
        "point": "entry:0",
        "iteration": [],
        "instance": [
          1
        ],
        "call_index": 0,
        "step": 1,
        "phase": "fwd"
      }
    ]
  ]
}
```

**Expected-program correspondence (K73).** Compatibility for
`expected: {program: H}` requires the same ordered interface roles,
bundle widths/classes, region shapes/classes/roles, classical parameter
types and ordered borrowed-bundle widths/classes as the subject; local
names may differ. [deps: ISA-5.1-P1, ISA-9.4-P2, ISA-12.1-P7.S4, ISA-12.1-P8]
The checker initialises and compares each interface bundle by (group,
slot), each region cell by (group, slot, index), each borrowed bundle by
its checked lifetime position and each prepended inherited control by
position, using the complete before/after tuples of K13, never matching
components between the two programs by name. [deps: ISA-5.1-P1, ISA-9.4-P2, ISA-12.1-P7.S4, ISA-12.1-P8]

*(non-normative)* For subject mut slots named t,u and expected mut slots
named u,t, both one bit, the first slot is compared with the first and
the second with the second; exchanging the expected local names cannot
exchange the values compared. [deps: ISA-9.4-P2, ISA-12.1-P7.S4, ISA-12.1-P8]

### 12.2 Domains

`"domain": { "bundles": [ { "name", "width", "lo", "hi" } ], "borrowed": [ same ], "regions": [ { "name", "cells": "all" | [ { "index", "lo", "hi" } ] } ], "args"?: [ same as bundles ] }`,
bounds inclusive, enumeration order as listed, last component fastest.
`args` (inverse-pair claims only) ranges over classical arguments other
than tokens (whose tuples the entry's `arg_tokens` fixes, §12.3), each
read as an unsigned integer of its width (`ptr`: ptr_width; `f64`: 64,
its bits).
A `proof` label requires the domain to equal D; otherwise the claim is
`evidence` with the covered fraction.
For a borrow-frame obligation, use D_F of §5.6; a region claim over D
does not by itself establish the frame claim. For example, with c
allocated at zero, the single frame `CX(c,b)` over {c=0} × {b=0,1}
is identity on b. The interleaved prefix `CX a c; CX x c; CX a c;
CX x c` clears c only by polynomial algebra; §5.6 instead admits both
c values at entry, so the same single-CX frame fails its obligation.

**Component resolution (K69/K70).** These component-domain rules apply
to table/program/oracle relations; K4 inverse-pair claims retain their
separate two-composition relation and quantified argument bindings.
[deps: ISA-12.1-P7.S8, ISA-12.1-P1.S2, ISA-12.3-P3]
For an oracle the interface bundle groups are `in`, `tgt`, `fault` and its interface regions have role `in`;
for an action the bundle and region roles are `mut`, `in`, with slots
numbered from zero within each declared group. [deps: ISA-5.1-P1, ISA-5.2-P4, ISA-5.3-P1, ISA-9.4-P2]
A `bundles` or `regions` entry's `name` MUST be the subject header's
local name of an interface bundle or region of that category, resolving
to (group, slot); unknown names reject. [deps: ISA-5.1-P1, ISA-9.4-P2, ISA-12.2-P1]
For a subject with c inherited controls, the first c `bundles` entries
instead denote those prepended one-bit controls by position, with
label-only names; all c entries are required, and a singleton range
expresses a fixed control value. [deps: ISA-12.1-P8.S3, ISA-12.1-P7.S1, ISA-12.2-P1]
A region's `cells: "all"` denotes every cell (group, slot, index) in
increasing index order with its full W-bit range, and an explicit cell
list denotes those same cell identities in listed order with the stated
ranges. [deps: ISA-3.3-P19, ISA-12.2-P1.S1]
Entry k of `borrowed` denotes checked borrow lifetime k (zero-based) in
K13's tuple allocation order, independently of any physical storage
reuse; its `name` is only a label, may coincide with any other name and
never denotes an interface component. [deps: ISA-4.3-P2, ISA-5.6-P1, ISA-12.1-P8.S4]
A borrowed position beyond the checked borrow requirement rejects as
ill-formed. [deps: ISA-4.3-P2, ISA-12.1-P8.S4]
A `borrowed` entry MUST NOT discharge an interface bundle or region-cell
coverage obligation, whatever its name. [deps: ISA-4.3-P2, ISA-5.6-P1, ISA-12.1-P8]

**Domain validity and omission (K71/K72).** After resolution, each
component MUST occur at most once, every supplied `width` MUST equal
that component's width, ranges MUST satisfy 0 ≤ lo ≤ hi < 2^width, and
cell indices MUST satisfy 0 ≤ index < 2^A; a violation rejects the
claim as ill-formed. [deps: ISA-3.3-P2.S2, ISA-3.3-P19, ISA-12.2-P1]
Every omitted component is held at zero on every replayed element,
including omitted borrowed positions after the listed entries; workspace
and local regions retain their separate zero/image initialisations.
[deps: ISA-5.2-P4, ISA-5.3-P1, ISA-12.2-P1]
The domain denotes the product of the resolved ranges with those
omitted components fixed at zero, not the full range of an omitted
component. [deps: ISA-5.2-P4, ISA-5.3-P1, ISA-12.2-P1]
For an exhaustive claim its element count n is the product of the range
sizes over individual resolved components, the empty product being 1,
and its covered fraction is exactly n/|D|, with |D| the product of the
full component range sizes (prepended inherited controls included).
[deps: ISA-5.2-P4, ISA-5.3-P1, ISA-12.1-P8, ISA-12.2-P1]

**Coverage and verdicts (K69/K74).** For exhaustive and sampled claims,
`proof` and `evidence` are checker-assigned outcomes recorded in the
checker report against the region closure hash and zero-based `claims`
array index, with the bound invocation or invocation context key where
applicable; they are not producer assertions in the certificate.
[deps: ISA-1.2-P4, ISA-12.1-P7, ISA-12.1-P11, ISA-12.3-P1, ISA-12.3-P3]
An exhaustive table/program/oracle claim receives `proof` iff every
obligation of §12.1 succeeds on every element and its domain equals D
component by
component: every interface bundle, every interface region cell, every
borrowed position and every prepended inherited control occurs exactly
once with its full range. [deps: ISA-12.1-P1, ISA-12.1-P7, ISA-12.1-P8, ISA-5.2-P4, ISA-5.3-P1, ISA-14.3-P3]
This equality is decided over resolved identities and ranges, never
sets of names; an explicit full-range list of every cell covers exactly
the same region domain as `cells: "all"`. [deps: ISA-3.3-P19, ISA-12.2-P1, ISA-12.1-P8]
Successful exhaustive checks on a strict slice receive `evidence` with
n replayed elements and n/|D|; successful sampled checks receive
`evidence` with exactly `count` replayed draws and K13's distinct-draw
fraction, even if it is 1. [deps: ISA-12.1-P1, ISA-12.1-P2, ISA-12.1-P8.S9, ISA-12.1-P8.S10, ISA-12.2-P1]
A supplied `label` of `proof` or `evidence` is only a request: the
checker MUST compute the outcome independently and reject a requested
`proof` when a completed check yields only `evidence`. [deps: ISA-1.2-P4, ISA-12.1-P7.S6, ISA-12.2-P1]
Neither an evidence label nor a requested label discharges an obligation
requiring proof over D. [deps: ISA-5.6-P2, ISA-14.3-P3, ISA-12.3]

**Host limits (K75).** Domain widths, region address width A, cell-list
lengths and sampler `count` have no ISA-imposed upper cap; a checker
MUST NOT treat its host's representability, allocation or replay limits
as domain illegality. [deps: ISA-3.3-P2.S2, ISA-3.3-P19, ISA-12.1-P2, ISA-12.2-P1]
If a checker cannot complete a legal claim on its host, including
materialising an element, enumerating the domain or retaining the
required replay/coverage data, it MUST terminate normally and record
**unchecked (host limit)** for that claim in the same report, citing
§12.2 and the quantity or operation that exceeded the host limit.
[deps: ISA-12.1-P1, ISA-12.1-P2, ISA-12.1-P8, ISA-12.2-P1]
That outcome is distinct from rejection and from either label, supplies
no evidence count or covered fraction for the claim, and discharges no
obligation of §5.6, T3 or §12.3, including when a producer requested a
label. [deps: ISA-1.2-P4, ISA-5.6-P2, ISA-14.3-P3, ISA-12.3]

**COMPONENT-COVERAGE witness**
The following full tuples and resolved identities instantiate the
component rules without a schedule or inherited controls.
[deps: ISA-4.4, ISA-12.1-P8, ISA-12.2-P1]

```json
{
  "mut_names":["t","u"],"widths":[1,1],"borrowed_widths":[1],
  "domain":{"bundles":[{"name":"u","width":1,"lo":0,"hi":1}],"borrowed":[{"name":"t","width":1,"lo":0,"hi":1}],"regions":[]},
  "resolved":[["mut",1],["borrowed",0]],
  "elements":4,"full_elements":8,"covered_fraction":"1/2","verdict":"evidence",
  "renamed_borrowed":"b",
  "counterexample":{
    "before":{"bundles":["1","0"],"borrowed":["0"],"regions":[]},
    "cnot_after":{"bundles":["1","1"],"borrowed":["0"],"regions":[]},
    "identity_after":{"bundles":["1","0"],"borrowed":["0"],"regions":[]}
  },
  "full_bundle_order":["t","u"],"first_mismatch_index":4,
  "region":{"A":1,"W":1,"cells":[{"index":1,"lo":0,"hi":1},{"index":0,"lo":0,"hi":1}],"elements":4,"covers_all":true}
}
```

*(non-normative)* For the one-bit mut t,u action that borrows b,
applies `cx t u` and returns b, compared with identity with the same
borrow requirement, the four elements above agree because omitted t
is zero, while (t,u,b)=(1,0,0) distinguishes the programs; renaming the
borrowed label cannot change the domain or its verdict. [deps: ISA-4.4, ISA-4.3-P2, ISA-12.1-P7, ISA-12.2-P1]
Adding the full t range in the printed full-bundle order exposes the
mismatch at zero-based element 4, rather than yielding proof.
[deps: ISA-4.4, ISA-12.1-P1, ISA-12.2-P1]
The two-cell region's explicit reversed cell list covers all four basis
configurations, while repeating index 1 or using index 2 is ill-formed;
an action region[63,1] with `cells: "all"` and `count: 1` remains legal but has
2^63 bits per element, so an unable host reports unchecked (host limit).
[deps: ISA-3.3-P19, ISA-12.1-P2, ISA-12.2-P1]

### 12.3 Schema and composition

```
  versions; bindings { object_hash, interface_hash, closure_hash (required), reference_program_hash, dialect_mapping_version, target_hash, schedule_hash?, invocation? (K13) }
  producer { name, version, materialisation { llvm_version, pipeline, normaliser_version } }
  regions { <closure_hash>: { kind, signature, bounds, estimate? (K12), frame (required typed-record descriptor, §9.4), resources { name: decimal }, gates_used { gate: { count, scheme?, epsilon? } },
            claims: [ <claim> … ], verification: { oracle: i, borrow_frames: [i], inverse_pairs: [ { g, ginv, claim: i, budget: [B,heap,stack,depth], arg_tokens?: { "<arg>": [B,heap,stack,depth] } } ], unitary: [i], channel: [i],
                                                   fault_rate: { domain, faults_by_code, undefined_excluded, layout_dependent_excluded } },
            cleanup: { "<variant>:<inherited_controls>": [ { path, realisation } ] },
            error:   { "<variant>:<inherited_controls>": { local: { "operator_norm"?: v, "diamond"?: v }, inclusive: { "operator_norm"?: v, "diamond"?: v } } },
            definedness_assumptions: [ids] } }
  composition { multiplicities: { "<hash>:<variant>:<inherited_controls>": n (from the realised schedule) }, epsilon_total: { "diamond": v }, method: "sum_over_multiplicities" }
```

**Invocation binding (K13).** An invocation is
`{ args: [value, …], budget: [B,heap,stack,depth] }`, with every value
resolved before replay and all four budget components explicit even
when zero. `args` is in signature order: `iN` and `ptr` values are
canonical **unsigned decimal strings** of exactly that bit-vector
value (ptr has `ptr_width` bits); `f64` is `0x` followed by exactly 16
lowercase hex digits of its IEEE 754 binary64 bit pattern, most
significant nibble first (so −0 and NaN payloads are not lost); a token
is its four-component tuple of canonical nonnegative decimal strings,
not a process-local token id. Budget components are also canonical
nonnegative decimal strings. Signature types disambiguate encodings;
widths/ranges and every tuple MUST pass §5.4 validation. `params_hash`
is SHA-256 of the UTF-8 JCS **args array**, no trailing LF (§9.2), not
of the whole invocation. Thus equal token tuples have equal parameter
hashes regardless of ids, while +0 and −0 `f64` parameters differ.

Each standalone table/program/structural claim MUST carry its own
`invocation`; it binds
**every** classical argument and budget. Missing values have no implicit
zero/default. Claims with no arguments still bind `args: []` and their
budget. K4 inverse-pair claims instead bind the entry's budget,
`arg_tokens` and quantified `args` domain as already specified; this
rule does not replace that quantification by one chosen argument.
A parameter-uniform structural claim MAY instead bind
`invocation: { args: "all", budget: "all" }`: its checker MUST discharge
the rule's side conditions for every well-typed argument vector and
valid budget, not by replaying a chosen instance. Thus generic library
and adjoint/translation proofs retain their universal scope.
A scheduled certificate MUST carry the root `bindings.invocation`;
its args hash and budget MUST equal the root schedule's bindings, and
all nested arguments and budgets MUST be resolved at each realised
invocation context (§12.1), including default-covered contexts.
Explicit nested bindings, if supplied, MUST equal those resolutions;
a root binding MUST NOT be silently reused for a different callee.
A checker MUST reject absent or conflicting bindings before replay,
and an executor may use a verified result only for the invocation(s)
it actually covers. Reference table/program/structural claims need no
schedule; they prove only their reference relation, not a target
realisation. Scheduled/numerical/channel claims retain the expansion
library gate and all existing context and composition obligations.

**CLAIM-BINDING witness**

```json
{"signature":["i128","f64","token"],"args":["18446744073709551617","0x8000000000000000",["2","0","0","0"]],"params_hash":"9f628a694fa7259bf899bfb677aabce1c084e268a738a40f7f643eb6d8c9c093"}
```

The first argument is > 2^64; the second is binary64 negative zero;
the third is a token tuple, not an id. Replacing negative zero with
`0x0000000000000000` changes `params_hash`; replacing the token by
another valid id of the same tuple does not.

`versions` is the object `{ "isa", "object", "launch", "sched", "cert",
"coverage", "target" }` of the seven header versions. A **variant** is a
nonempty string chosen by the producer (the ISA enumerates none); it is
compared bytewise.

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
(`numerical`, `channel`, and `exhaustive` or `sampled` with
`expected: "oracle"`, plus table/program comparisons of a realised
operation) bind to `schedule_hash` through their subject. Standalone
reference relations have only the invocation scope defined above (K13).

## 13. Coverage (coverage 0.9)

`{ "entries": [ { "point": <program-point id>, "source": "<dialect-spec stable id>", "classification": "lowered" | "trapped" | "shimmed", "reason", "fault_code"?, "shim_hash"?, "count" } ] }`.
`fault_code` is present iff `classification` is `trapped`, `shim_hash`
iff it is `shimmed`.

## 14. Formal model

### 14.1 Reference interpreter *(normative)*

Executes an oracle's reference body per basis configuration: locations
and cells are bit-vectors of their declared widths (no upper bound,
§3.3), pseudo-locations read-only, predication is
`if`, each §4.2 row is its classical function (including the inherent
`inrange` check of loads and stores, the activation records of §3.7, the
`alloctab` and stack arrays), `fault` and a triggered `lift.faultif`
record their effective cause (§5.4) and halt, `lift.
retval` halts with success and `f(x) = result_val`, the step counter
counts executed rows (on budget exhaustion exactly B rows have
executed), counters are unbounded integers. It **defines** F_B
and the budget unit and rejects any body that executes a non-permutation
gate.

For CC/R, `fault C` has the terminal-record semantics of §4.9 and the
logical history of §7.4: it preserves the complete executed prefix for
eligible reversal, including activations that have not returned. This
is T4's history traversal, not the Q machine's B inverse steps. In an
oracle body or lproc the same spelling remains the §4.2 fault row;
§3.6 and §5.2 supply its step-machine inverse and T2 prefix reversal.

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
- **T4 (round trip).** For every finite CC/R trace with retained run
  history and tapes that is eligible for reversal under §10 — a
  `COMPLETED` or `FAILED` run containing no `measure` frame and no
  `qreg.free` frame whose cleanliness was not verified — the history
  traversal of §7.4 restores the active environment, memory, allocation
  table, device-model state, the ledger entries of every register the
  run created or touched, token validity and active history (§7.4) to
  their entry values; audit records may remain; observed external
  events are not retracted. If, in addition, every region call is undone
  by the exact inverse of its realised forward operation (ε = 0
  realisations, or a realisation that is applied as its own adjoint),
  the quantum state of every register the run touched is restored
  exactly; otherwise to within the sum of the realisations' declared
  bounds (§12.3).
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
| A | Executor | classical ISA; run history and LIFO reversal with loops, recursion, effects, segment `uncall` (impure suffix traps; nested `uncall` inside an uncalled segment; `uncall` over a `measure` traps; a segment that begins at the run's first instruction, uncalled, then whole-run reversal), `hostcall`, `qreg.*`, fault records (T4); CC `uncall` of a CC segment (§3.1); a use reached before any definition traps 4 whatever the block text order; `qreg[*]` (examples 4, 5): run-time widths 0, 2, 3, an id stored and reloaded, `qreg.from_id` of a stale, consumed or viewed id or of a register owned by another open run traps 4, a width-3 register bound to `wire[2]` or `qreg[2]` traps 4 with no effect, aliases consumed together, ids restored and never reused by reversal, run-time slice `lo` and `len`; `qreg.*` in R with whole-run reversal and segment `uncall` (a hardware-unverified free makes the segment non-uncallable); `budget.mint` valid and invalid and its reversal (example 6); the §4.9 causes — `udiv` by 0 → 5, i8 −128 `sdiv` −1 → 6, `load` at address 0 → 7, `alloc` beyond the heap → 2, `trap` → 4, `fault 1` → 1, `fault 0` → 4 — each with the pre-fault state unchanged and exactly one record; terminal R faults and FAILED-run reversal (example 8), also with `fault 2`, `fault 3` and `fault 18446744073709551615`: exact record code, no caller continuation or subsequent source effect, earlier memory/device/tape history intact until reversal |
| B | Executor | oracle totality and prefix reversal: every fault code; B = 0; boundary halts; `lift.call`/`lift.ret` recursion with argument capture; one forward `lift.call` and one forward `lift.ret` step of a recursive call each followed by its inverse (§3.7); stack exhaustion (`sp + R_f > stack_limit`); matched `lift.oracle_uncall`, including two calls followed by two uncalls; interface regions restored; pre-entries; `lift.free` on pinned entries, and of a heap entry whose base equals a size-0 global's (the global stays live); inherent load/store checks; row indices of multi-row blocks and their `lift.label` values; `qjumpr` to an in-range interior row enters it and to an out-of-range index faults 4; `fault 0` and a triggered `lift.faultif p 0` commit `FAULT_UB_TRAP`; `fault C` as the B-th executed row reports C′, whereas a cut just before that row reports 1; subsequent HALT steps and inverse steps preserve the §5.2 outcome and clean every frame; counters at the §3.7 minimum widths and interface widths above 128 bits |
| C | Executor, Producer | T3 over full D at exhaustive widths for oracles, permutation actions, `qinplace` pairs, borrow frames; T6 agreement among VM, specialiser, transformed forms and the reference interpreter; the §16.3 examples as normative test vectors, including the stack-capacity boundary of example 2 and example 3 over its 8 basis and 16 controlled configurations with an entangled reference on the borrowed wire; `qinplace` with `ins` and `args` (example 7) over all x, y, a and both control values, scratch clean, and its adjoint (covered by the same entry); example 10's lproc token/classical/region forwarding over every x, a and byte d, arbitrary target/fault contents, and an external reference, with successful and insufficient nested budgets; coherent calls to two binding instances of one lproc, including recursive forwarding, and matched `lift.oracle_uncall` through parameters; a library (`inverse_pair_library`) claim covering every `args` value; a token argument whose tuple differs from `arg_tokens` traps 4 |
| D | Executor | channel and unitary comparison for ε > 0 realisations; controlled-interference tests; checker-computed bounds; the diamond-norm SDP witness check of §12.1, including d = 2, J(Φ) = 0, Y = I₄/8, mu = bound = 3/8 (accepted: every pivot 1/8) and Y = 0, mu = 0 (rejected: pivot 0) |
| E | Target author, Executor | JCS parsing; AST evaluation; matching; scheme expansion and correctness; aggregation from event lists; timing model; imports |
| F | Producer | versioning, disjointness incl. control context; operand schema; row classes and frame sizing; index-space flattening; terminators; name resolution; permutation-only oracles; §6 transfer and windows; adjoint table; translation lemma side conditions with the four negative tests; `in`-wire use; acyclic action graphs; grammar; schemas; the §3.1 call-tier table (R → CC rejected); envelope and hashes, acyclic (inc8, zero, sum_db) and cyclic (sum, and a mutual SCC); SCC placement in the index space (mutual f, g whose member hashes order opposite to their names); empty data lines (`NAME SP LF` accepted, two spaces rejected); canonical `INT`/`FLOAT` at every literal site; const literal ranges; the region call graph with lifted calls and `qinplace`; `call` operand spelling; param role suffixes; interface-region names; local regions as call operands; the widened `in`-wire uses of §5.1; LIFO matched uncalls and an unmatched uncall rejected; the static view rule of §3.3 (a view passed through `br`, used twice, or left unconsumed is rejected); lifted-call `args` that are locations rejected; lproc header groups and `token`/`classical` suffixes (a suffix in the wrong group rejected), exact argument counts/types/region roles, missing nonempty lists and location-as-token/classical rejected, forwarding `iN ptr f64 token` without bit conversion, empty-list short form, fixed-binding closure and instance ordering (§3.7), lproc signatures including empty arrays and changed interface/closure hashes; `qreg[*]` typing, the `measure.iN` form and width checks; `budget.mint` rejected in regions; CC/R block terminators; `qinplace` signature compatibility, its short form exactly when the three lists are empty, and its §6.1 transfer (cleaning a value that depends on x after changing an `ins` wire is rejected); CC/R `fault` literal range; linking; frame-descriptor live ranges |
| G | Launch | every §10 entry point, state transition, binding rule, ownership rule; HOST_REQUEST/reply (a reply whose length does not fit `ptr_width` bits is `E_ARG`); reverse eligibility and tree order; `QREG` bound to `qreg[*]`; `FAILED → REVERSED` (example 8) and `E_NOT_REVERSIBLE` after a `measure` or an unverified free; exactly one fault record per `FAILED` run; an R `fault C` returns `OK` from `bennett_wait` with a result and no request, zero values and the exact nonzero 64-bit C (including 2^64 − 1) from `bennett_result_fault(result, 0)`; a device-minted token used after its run is CLOSED is `E_ARG` |
| H | Scheduler | §6 validity; capacity; reproducibility; specificity resolution; verbatim execution; INFEASIBLE/UNSUPPORTED; invocation contexts covering default-only invocations (an action calling one region twice, one call scheduled explicitly: a claim with one witness rejects, two passing witnesses accept); a device-minted tuple binds the schedule (a schedule bound to B = 3 is not applied to an invocation minted with B = 2, which runs under the defaults) |

## 16. Canonical textual form (normative)

### 16.1 Lexical

UTF-8; LF line endings; one instruction per line; tokens separated by
exactly one space; no trailing spaces; exactly one blank line before
each `section` line and none elsewhere. `NAME := [A-Za-z_][A-Za-z0-9_.]*`;
`INT := -?(0|[1-9][0-9]*)`; `FLOAT :=` shortest round-trip decimal with
`.` or exponent, finite; `STRING := "…"` with escapes `\"`, `\\`, `\n`;
`HEX := ([0-9a-f]{2})*`. Metadata lines are RFC 8785 canonical JSON
objects. Every integer token is an `INT` (`ptr_width`, type widths,
`bounds`, literal operands, data and region sizes), so `032`, `+3` and
`09` are ill-formed; every gate angle is a `FLOAT` whose spelling is the
ECMAScript Number-to-String rendering that RFC 8785 uses for numbers,
with `.0` appended when that rendering contains neither `.` nor `e`, and
`-0.0` for negative zero (`0.7`, `1.0`, `1e+21`, `-0.0`; never `0.70`,
`1.0e0` or `00.7`). Where §16.2 prints `SP` twice around an empty list
(`regs {  }`) that spelling is canonical. A data line whose `HEX` is
empty is `NAME SP LF`: its mandatory separator space is the sole
exception to the no-trailing-space rule. The text has no comment
syntax; annotations travel outside the object.

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
               -- oracle: (in..) (tgt) (fault) (mem..) (args..) ; action: (mut..) (in..) (mem..) (args..) () ; lproc: (params..) (result) (tokens..) (classical..) (mem..) ; fn: (params..) (results..) () () ()
  plist     := (param ("," SP param)*)?
  param     := NAME ":" type (SP ("in"|"mut"|"token"|"classical"))?
  type      := "i" INT | "ptr" | "f64" | "token" | "wire" | "wire[" INT "]" | "reg[" INT "]" | "region[" INT "," INT "]" | "qreg[" (INT | "*") "]"
  regs      := "regs" SP "{" SP (NAME ":" type ("," SP NAME ":" type)*)? SP "}" (SP "bounds" SP "{" INT ("," SP INT)* "}")? NL
  block     := "^" NAME "(" plist "):" NL instr+
  instr     := (lhs SP "=" SP)? OPCODE (SP operand)* (SP "{" NL instr+ "}" (SP "{" NL instr+ "}")?)? NL
  lhs       := NAME | "(" NAME ("," SP NAME)* ")"
  operand   := NAME | NAME "[" INT "]" | "@" NAME | "^" NAME ("(" (NAME ("," SP NAME)*)? ")")? | INT | FLOAT | STRING | "(" (NAME ("," SP NAME)*)? ")"
  OPCODE    := a mnemonic of §4 with its dotted suffix (§4.8 fixes operand count, kinds and result placement)
  VER       := INT "." INT
```

The oracle header and signature declare no invocation-token slot. Its
catalog interface follows the five printed groups exactly; the separate
`tk` operand binds the typed `oracle_invocation` channel of §11.1, not a
reserved header name or an extra `args` element.

Lproc groups have the types and roles of §3.7. A `token` suffix is
permitted only in the third group and a `classical` suffix only in the
fourth, each agreeing with that group's role; either suffix may be
omitted. The first and second groups carry no suffix, and the fifth
requires `in`. The `token` and `classical` suffixes are not permitted on
other kinds of function or on block parameters or `regs` entries. The additional
`lift.call` lists use the existing list operand grammar (§3.7).

### 16.3 Example objects (normative test vectors, suites A, C, F and G)

**Hashes.** Every interface_hash in this section is the 64-hex value computed by §9.2 from the displayed envelope. Examples 1 and 2 are the 0.8
objects with the version string changed and, for example 2's lproc,
the three empty signature arrays required by Q14; their 0.8 hashes
remain the 0.8 vectors.

**Example 1** (`inc8`): one oracle, no lprocs, no memory. The function
has **six** canonical lines.

```
bennett-object isa=0.9 object=0.9 launch=0.9 sched=0.9 cert=0.9 coverage=0.9 target=0.9 ptr_width=32

section symbols
{"0":{"interface_hash":"ed9865300b85a519c2379de98e36e635e72b5b78d8bdfca03dccf9a09aa3df5e","kind":"oracle","name":"inc8","signature":{"abi":"0.9","args":[],"fault":4,"in":[8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}}}

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
isa=0.9
ptr_width=32
{"abi":"0.9","args":[],"fault":4,"in":[8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}
oracle @inc8 (x:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { one:reg[8], r:reg[8] }
^entry():
one = lift.const.i8 1
r = lift.add x one
lift.retval r
```

With B ≥ 3 every x yields `(x + 1 mod 256, 0)` (`result_val` = 0 ⊕ r);
with B = 2 every x yields `(0, FAULT_BUDGET_STEPS)`. The three rows have
indices 0, 1, 2, `HALT` = 3 and P = 2 (§3.6); `inc8` is acyclic, so its
hash is SHA-256 of these envelope bytes (§9.2).

**Example 2** (`sum_db`): an oracle reading an interface region through
lifted memory with a recursive lproc that receives the base as a
parameter, and a global accessed by address.

```
bennett-object isa=0.9 object=0.9 launch=0.9 sched=0.9 cert=0.9 coverage=0.9 target=0.9 ptr_width=32

section symbols
{"0":{"interface_hash":"3ad937b1cd867454989c5c5f58244681ef2c09dbabf7fce56515a68f63462ee6","kind":"oracle","name":"sum_db","signature":{"abi":"0.9","args":[],"fault":4,"in":[8],"kind":"oracle","mem":[{"A":4,"W":8,"role":"in"}],"tgt":8,"tier":"q"}},"1":{"interface_hash":"cb52102decd586b7585b5d73b90841dcec75edac5a5a2d0f43c5efb34d4cceb1","kind":"lproc","name":"sum","signature":{"abi":"0.9","args":[],"kind":"lproc","mem":[],"params":[8,8,32],"result":8,"tier":"q","tokens":[]}},"2":{"interface_hash":"43e032f98d7aff20f6864d6368b20ab4ef9d810938999acff8d71ed16e6b17d7","kind":"data","name":"zero","signature":{"abi":"0.9","kind":"data","size":1,"tier":"-"}}}

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
isa=0.9
ptr_width=32
{"abi":"0.9","args":[],"kind":"lproc","mem":[],"params":[8,8,32],"result":8,"tier":"q","tokens":[]}
lproc @sum (n:reg[8], acc:reg[8], base:reg[32]) (r:reg[8]) () () ()
regs { zp:reg[32], zv:reg[8], z:reg[1], one:reg[8], n2:reg[8], idx:reg[32], p:reg[32], v:reg[8], acc2:reg[8] }
^entry():
zp = lift.addr @43e032f98d7aff20f6864d6368b20ab4ef9d810938999acff8d71ed16e6b17d7
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
layout ["globals","zero"] {"base":16,"image":"zero","size":1}
43e032f98d7aff20f6864d6368b20ab4ef9d810938999acff8d71ed16e6b17d7
```

The displayed `sum` envelope renders its global leaf path as
`["globals","zero"]`, preserving the original leaf value.
[deps: ISA-9.1-P1, ISA-16.1]
`@sum_db`'s envelope includes every layout leaf, the `zero` image, `@` +
the `sum` hash in place of `@sum`, and the `sum` hash as its part-(6)
line (`@db` is an interface region, not a symbol):

```
inc8 = ed9865300b85a519c2379de98e36e635e72b5b78d8bdfca03dccf9a09aa3df5e
zero = 43e032f98d7aff20f6864d6368b20ab4ef9d810938999acff8d71ed16e6b17d7
sum = cb52102decd586b7585b5d73b90841dcec75edac5a5a2d0f43c5efb34d4cceb1
sum_db = 3ad937b1cd867454989c5c5f58244681ef2c09dbabf7fce56515a68f63462ee6
```

**Example 3** (`borrow_demo`): a permutation action with a loop bound
and a borrow frame established by the translation lemma (§5.6).

```
bennett-object isa=0.9 object=0.9 launch=0.9 sched=0.9 cert=0.9 coverage=0.9 target=0.9 ptr_width=32

section symbols
{"0":{"interface_hash":"6f4782e9bde4267acd1afddd650093722a056d9d50ee465b79cb86a4606b2a94","kind":"perm_action","name":"borrow_demo","signature":{"abi":"0.9","args":[],"bounds":[1],"in":[1],"kind":"perm_action","mem":[],"mut":[1],"tier":"q"}}}

section functions
perm_action @borrow_demo (t:wire) (x:wire in) () () ()
regs {  } bounds {1}
^entry():
b = qborrow any 1
qloop 1 {
cx x b[0]
cx b[0] t
cx x b[0]
cx b[0] t
}
qreturn b
```

The bounds list is `[1]` (one `qloop`, trip count 1). The borrow frame is
the four `cx`: V = `cx x b[0]` (target in B = {b[0]}, control in X = {x},
X ∩ B = ∅), W = `cx b[0] t` (target t outside X, B and W's controls; one
control in B), V⁻¹ = V reversed, W again; no `swap`. On each of the 8
basis values of (t, x, b[0]) the action maps (t, x, b) ↦ (t ⊕ x, x, b):
V gives b ⊕ x, W gives t ⊕ b ⊕ x, V⁻¹ restores b, W gives t ⊕ x. Under an
inherited control w (16 configurations) it maps to (t ⊕ w·x, x, b); on a
borrowed wire entangled with a reference system it acts as that
permutation ⊗ I. The map is an involution, so the adjoint (the reverse
sequence `cx b[0] t; cx x b[0]; cx b[0] t; cx x b[0]`) realises the same
permutation; the adjoint's frame is not of the lemma's shape and is
covered by the `adjoint_table` rule (§12.1).

**Example 4** (`ones`, BLK-1): a register of run-time width, its id
stored to memory and reloaded, wires addressed by run-time slices.

```
bennett-object isa=0.9 object=0.9 launch=0.9 sched=0.9 cert=0.9 coverage=0.9 target=0.9 ptr_width=32

section symbols
{"0":{"interface_hash":"ff8e49307d5ec9ab32eea2406339f878630bbb4501080829200433a18d6951cb","kind":"cc","name":"ones","signature":{"abi":"0.9","kind":"cc","params":["i64"],"results":["i3"],"tier":"cc"}},"1":{"interface_hash":"3860ea712b2d70fc495834586bb397656a467c85235aa069768318a06e9fa89b","kind":"perm_action","name":"flip","signature":{"abi":"0.9","args":[],"bounds":[],"in":[],"kind":"perm_action","mem":[],"mut":[1],"tier":"q"}}}

section functions
fn cc @ones (n:i64) (m:i3) () () ()
^entry():
q = qreg.new any n
w = qreg.width q
id = qreg.id q
k = const.i32 8
p = alloc k
store.i64 p id
id2 = load.i64 p
q2 = qreg.from_id id2
zero = const.i64 0
one = const.i64 1
br ^test(zero)
^test(i:i64):
c = icmp.ult i w
br c ^body(i) ^done()
^body(j:i64):
s = qreg.slice q2 j 1
action_call @flip (s) () () ()
j2 = add j one
br ^test(j2)
^done():
m = measure.i3 q2
ret m
perm_action @flip (a:wire) () () () ()
^entry():
x a

section layout
{"A_tab":4,"H":12,"S_cells":0,"globals":{},"heap_base":16,"heap_limit_max":4080,"interface_regions":{},"null_size":16,"ptr_width":32}
```

Ranges: null [0, 16), heap [16, 4096), both within [0, 2^12); no globals. For n = 3:
`q` is a fresh register R (width 3, |000⟩); `p` = 16 (the bump pointer
starts at `heap_base`); `q2` is an alias of R; iterations i = 0, 1, 2
each slice [i, 1) (a `qreg[1]` view) and flip that wire; at i = 3 the
loop exits; `measure.i3` finds width 3 and outcome 0b111 = 7 with
probability 1. The run is `COMPLETED` with one `INT` result of width 3
(the byte `07`) and one measurement record (R, bits 1, 1, 1); it is not
reversible (a `measure` frame). For n = 2 the loop flips two wires and
`measure.i3` traps before measuring (width 2 ≠ 3): `FAILED`, one record
`FAULT_UB_TRAP`, no measurement, R live in |11⟩; that run *is*
reverse-eligible and reversal returns R to |00⟩ and releases it. For n =
0 the loop does not run and `measure.i3` traps likewise.

**Example 5** (`scratch`, BLK-4): quantum allocation inside an R
function, used and released, then reversed.

```
bennett-object isa=0.9 object=0.9 launch=0.9 sched=0.9 cert=0.9 coverage=0.9 target=0.9 ptr_width=32

section symbols
{"0":{"interface_hash":"5cebd5a72ee7873edda0d2c35afed2a5ab79eba60f2b242b2a856d5fa4074634","kind":"cc","name":"main","signature":{"abi":"0.9","kind":"cc","params":["i64"],"results":[],"tier":"cc"}},"1":{"interface_hash":"05525834cbe5a518aa97444912254f3c12c75dd86314a98ba550f45187208a0b","kind":"r","name":"scratch","signature":{"abi":"0.9","kind":"r","params":["i64"],"results":[],"tier":"r"}},"2":{"interface_hash":"3860ea712b2d70fc495834586bb397656a467c85235aa069768318a06e9fa89b","kind":"perm_action","name":"flip","signature":{"abi":"0.9","args":[],"bounds":[],"in":[],"kind":"perm_action","mem":[],"mut":[1],"tier":"q"}}}

section functions
fn cc @main (n:i64) () () () ()
^entry():
call @scratch n
ret
fn r @scratch (n:i64) () () () ()
^entry():
q = qreg.new any n
zero = const.i64 0
one = const.i64 1
br ^test(zero)
^test(i:i64):
c = icmp.ult i n
br c ^body(i) ^done()
^body(j:i64):
s = qreg.slice q j 1
action_call @flip (s) () () ()
t = qreg.slice q j 1
action_call @flip (t) () () ()
j2 = add j one
br ^test(j2)
^done():
qreg.free q
ret
perm_action @flip (a:wire) () () () ()
^entry():
x a
```

The object is memoryless. Forward, for every n the device can provide (else `qreg.new` records `FAULT_BUDGET_HEAP`): R creates register Q
(width n, |0…0⟩); iteration j flips wire j to |1⟩ and back to |0⟩; the
`qreg.free` finds Q clean (a verifying executor verifies it); the run is
`COMPLETED` with no values. Whole-run reversal re-creates Q clean with
its id, undoes iteration n − 1 (the second flip's adjoint makes wire n −
1 |1⟩, its slice frame restores Q live, the first flip's adjoint makes
it |0⟩), then every earlier iteration, and finally the `qreg.new` (Q is
clean: released); the run is `REVERSED` with the register ledger as at
entry, Q's id not reused. On hardware the free is unverified (§17 item
14) and `bennett_reverse` returns `E_NOT_REVERSIBLE`. Under 0.8 `@scratch`
is ill-formed (`qreg.*` was CC only).

**Example 6** (`adaptive`, BLK-2): a budget minted on the device from a
run-time value.

```
bennett-object isa=0.9 object=0.9 launch=0.9 sched=0.9 cert=0.9 coverage=0.9 target=0.9 ptr_width=32

section symbols
{"0":{"interface_hash":"b80aed1639a9ac6a6856f02b0b3264d905e4eea3fa3f9081c01e56283ea398cf","kind":"cc","name":"adaptive","signature":{"abi":"0.9","kind":"cc","params":["i1","qreg[8]","qreg[8]","qreg[4]"],"results":[],"tier":"cc"}},"1":{"interface_hash":"c0d9835844fa882c1864044acc6fa26dba3935e0d6a9d33f9cdbf1e7c877d250","kind":"cc","name":"overdraw","signature":{"abi":"0.9","kind":"cc","params":[],"results":[],"tier":"cc"}},"2":{"interface_hash":"ed9865300b85a519c2379de98e36e635e72b5b78d8bdfca03dccf9a09aa3df5e","kind":"oracle","name":"inc8","signature":{"abi":"0.9","args":[],"fault":4,"in":[8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}}}

section functions
fn cc @adaptive (b:i1, x:qreg[8], t:qreg[8], f:qreg[4]) () () () ()
^entry():
two = const.i64 2
three = const.i64 3
zero = const.i64 0
s = select b three two
tk = budget.mint @inc8 s zero zero zero
oracle_call @inc8 tk (x) t f () ()
ret
fn cc @overdraw () () () () ()
^entry():
three = const.i64 3
one = const.i64 1
zero = const.i64 0
tk = budget.mint @inc8 three one zero zero
ret
oracle @inc8 (x:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { one:reg[8], r:reg[8] }
^entry():
one = lift.const.i8 1
r = lift.add x one
lift.retval r
```

`@inc8` is example 1's oracle. With b = 1 the token's tuple is (3, 0, 0,
0) and, on basis inputs, t ⊕= (x + 1) mod 256 with f unchanged; with b = 0
it is (2, 0, 0, 0): t unchanged, f ⊕= `FAULT_BUDGET_STEPS` (example 1's
results). Both runs are `COMPLETED` (each under the schedule bound to
its tuple if the object has one, else under the §11 defaults). Reversal
re-applies `@inc8` with the
recorded tuple (an involution), restoring t and f, then revokes the
token. `@overdraw` asks for heap_limit 1 in a memoryless object: the mint
fails `bennett_budget`'s check, the run is `FAILED` with one record
`FAULT_UB_TRAP`, and no token exists.

**Example 7** (`addya`, BLK-3): a parametrised in-place update x ← (x
+ y + a) mod 4 from a declared inverse pair.

```
bennett-object isa=0.9 object=0.9 launch=0.9 sched=0.9 cert=0.9 coverage=0.9 target=0.9 ptr_width=32

section symbols
{"0":{"interface_hash":"0d65d926275688cfebf2831c1de960b03a6b8ea6400866e6d9fef8f393ca2c2e","kind":"oracle","name":"g","signature":{"abi":"0.9","args":["i2"],"fault":4,"in":[2,2],"kind":"oracle","mem":[],"tgt":2,"tier":"q"}},"1":{"interface_hash":"786f1970ca3d78ef3d5de795411ee276286711c89b756872757c24f9bd569cc9","kind":"oracle","name":"ginv","signature":{"abi":"0.9","args":["i2"],"fault":4,"in":[2,2],"kind":"oracle","mem":[],"tgt":2,"tier":"q"}},"2":{"interface_hash":"5999b6d3d2362f8c1971ef6f37b404766aa5c18f6ba1880d767bfde351e47392","kind":"perm_action","name":"addya","signature":{"abi":"0.9","args":["token","i2"],"bounds":[],"in":[2],"kind":"perm_action","mem":[],"mut":[2],"tier":"q"}},"3":{"interface_hash":"562ab7270a0f508d6a2f4a757f3f90964da0b60541bac2c5efa421bad009056a","kind":"cc","name":"run","signature":{"abi":"0.9","kind":"cc","params":["qreg[2]","qreg[2]","token","i2"],"results":[],"tier":"cc"}}}

section functions
oracle @g (x:wire[2] in, y:wire[2] in) (t:wire[2]) (f:wire[4]) () (a:i2)
regs { s:reg[2], r:reg[2] }
^entry():
s = lift.add x y
r = lift.add s a
lift.retval r
oracle @ginv (x:wire[2] in, y:wire[2] in) (t:wire[2]) (f:wire[4]) () (a:i2)
regs { s:reg[2], r:reg[2] }
^entry():
s = lift.sub x y
r = lift.sub s a
lift.retval r
perm_action @addya (x:wire[2]) (y:wire[2] in) () (tk:token, a:i2) ()
^entry():
qinplace @g @ginv tk x (y) () (a)
fn cc @run (x:qreg[2], y:qreg[2], tk:token, a:i2) () () () ()
^entry():
action_call @addya (x) (y) () (tk, a)
ret
```

Each oracle has three rows, so F_B = ((x + y + a) mod 4, 0), resp. ((x − y
− a) mod 4, 0), for B ≥ 3 and (0, `FAULT_BUDGET_STEPS`) for B ≤ 2; for each
(y, a) the two maps are mutually inverse bijections of [0, 4). The object
is completed for execution by a certificate (generated with the 0.9
precheck, which first computes `object_hash`) whose `@addya` region
record carries `verification.inverse_pairs` = `[{"budget":[3,0,0,0],"claim":0,"g":"<closure hash of g>","ginv":"<closure hash of ginv>"}]`
and claim 0 = `{"domain":{"args":[{"hi":3,"lo":0,"name":"a","width":2}],"borrowed":[],"bundles":[{"hi":3,"lo":0,"name":"x","width":2},{"hi":3,"lo":0,"name":"y","width":2}],"regions":[]},"expected":"inverse_pair","kind":"exhaustive"}`
(64 elements). With it and a token whose tuple is ≥ (3, 0, 0, 0), `@run`
maps every basis (x, y) and a ∈ [0, 4) to x′ = (x + y + a) mod 4, y
unchanged, scratch clean: for x = 3, y = 2, a = 1, `@g` gives t = 2, the
exchange gives x = 2, t = 3, and `@ginv`(2; 2, 1) = 3 clears t. The adjoint
maps x to (x − y − a) mod 4; under a control 0 nothing changes. Without the
certificate, or with a token of tuple (2, 0, 0, 0), `@run` traps
`FAULT_UB_TRAP` before any effect.

**Example 8** (`fails`, ISA-7/ISA-8): an R fault after effects, and the
reversal of the failed run.

```
bennett-object isa=0.9 object=0.9 launch=0.9 sched=0.9 cert=0.9 coverage=0.9 target=0.9 ptr_width=32

section symbols
{"0":{"interface_hash":"dbf66e749a776cbb1ceccfc8b530caf664e24fb416fdf52ccf3942f4b89fdcf2","kind":"cc","name":"main","signature":{"abi":"0.9","kind":"cc","params":[],"results":[],"tier":"cc"}},"1":{"interface_hash":"d365ade0d8452d7d12b1a72c87e7106b06eef99e5958d0345133cf6eb0cbeb03","kind":"r","name":"work","signature":{"abi":"0.9","kind":"r","params":["ptr"],"results":[],"tier":"r"}}}

section functions
fn cc @main () () () () ()
^entry():
n = const.i32 8
p = alloc n
call @work p
ret
fn r @work (p:ptr) () () () ()
^entry():
v = const.i64 7
store.i64 p v
effect clock.read p
fault 21

section devices
{"models":{"clock":{"version":"0.9"}},"services":{}}

section layout
{"A_tab":4,"H":12,"S_cells":0,"globals":{},"heap_base":16,"heap_limit_max":4080,"interface_regions":{},"null_size":16,"ptr_width":32}
```

`p` = 16; the store writes `07 00 00 00 00 00 00 00` at [16, 24); the clock
read writes c = 0 there (`00` × 8) and sets c = 1; `fault 21` ends the run:
`FAILED`, `bennett_result_nfaults` = 1, `bennett_result_fault` = 21, no
values, `@main`'s `ret` not executed, [16, 24) = `00` × 8, c = 1, tape
length 1. `bennett_reverse` (0.8: `E_NOT_REVERSIBLE`) removes the fault
record, undoes the clock read ([16, 24) = `07` then `00` × 7, c = 0, tape empty),
the store ([16, 24) = `00` × 8), the open activation of `@work` and the
call, and the allocation: the run is `REVERSED` with memory, allocation
table, clock and tape at their entry values.

**Example 9** (`zero_cause`, effective cause): a literal fault code 0.

```
bennett-object isa=0.9 object=0.9 launch=0.9 sched=0.9 cert=0.9 coverage=0.9 target=0.9 ptr_width=32

section symbols
{"0":{"interface_hash":"badf7dd2a59afa879f092921946539dfb918cedd35f6fbbaa838c630577eaed4","kind":"oracle","name":"zero_cause","signature":{"abi":"0.9","args":[],"fault":4,"in":[1],"kind":"oracle","mem":[],"tgt":1,"tier":"q"}},"1":{"interface_hash":"0403d76ff065acab57cb9165cfe1d3d73bbf8dad60bbc1348fb0305ee4f37611","kind":"cc","name":"zero_cc","signature":{"abi":"0.9","kind":"cc","params":[],"results":[],"tier":"cc"}}}

section functions
oracle @zero_cause (x:wire in) (t:wire) (f:wire[4]) () ()
^entry():
lift.faultif x 0
lift.retval x
fn cc @zero_cc () () () () ()
^entry():
fault 0
```

Rows: `lift.faultif` (index 0), `lift.retval` (1); `HALT` = 2, P = 2. With
B = 0 every x yields (0, `FAULT_BUDGET_STEPS`). With B = 1, x = 0 yields (0,
`FAULT_BUDGET_STEPS`) (not halted) and x = 1 yields (0, `FAULT_UB_TRAP`).
With B ≥ 2, x = 0 yields (0, 0) (success, payload 0) and x = 1 yields (0,
`FAULT_UB_TRAP`); under 0.8, x = 1 yielded (0, 0) for every B ≥ 1,
indistinguishable from success. A run of `@zero_cc` is `FAILED` with one
record `FAULT_UB_TRAP`.

**Example 10** (`through`, lproc token/classical parameters): the
oracle forwards its entry token, an `i2` argument and a mapped byte
region to an lproc. The lproc makes both a parametrised oracle call and
a parametrised permutation-action call, passing its token as `tk` and
also as a token-typed `args` operand. All token uses preserve identity.

```
bennett-object isa=0.9 object=0.9 launch=0.9 sched=0.9 cert=0.9 coverage=0.9 target=0.9 ptr_width=32

section symbols
{"0":{"interface_hash":"4ee502a2d517d53d229f2ae21346505af06a228a2f0d2967938d48683e16d9e7","kind":"oracle","name":"through","signature":{"abi":"0.9","args":["token","i2"],"fault":4,"in":[2],"kind":"oracle","mem":[{"A":0,"W":8,"role":"in"}],"tgt":2,"tier":"q"}},"1":{"interface_hash":"9bd5e97be1f600494476527fb2d7d088bffab607bdadac8e01f9b23d15f9dfe1","kind":"lproc","name":"worker","signature":{"abi":"0.9","args":["i2"],"kind":"lproc","mem":[{"A":0,"W":8,"role":"in"}],"params":[2],"result":2,"tier":"q","tokens":["token"]}},"2":{"interface_hash":"c6e53733d87782414d05720d444734d9335244155518db4f60916e3d4b06dd1d","kind":"oracle","name":"plus_db","signature":{"abi":"0.9","args":["i2"],"fault":4,"in":[2],"kind":"oracle","mem":[{"A":0,"W":8,"role":"in"}],"tgt":2,"tier":"q"}},"3":{"interface_hash":"bfa13d9a564e3f8562098c4ea39330d947efa64521310afad6a329dc594bd671","kind":"perm_action","name":"flip_arg","signature":{"abi":"0.9","args":["token","i2"],"bounds":[],"in":[],"kind":"perm_action","mem":[],"mut":[2],"tier":"q"}}}

section functions
oracle @through (x:wire[2] in) (t:wire[2]) (f:wire[4]) (db:region[0,8] in) (tk:token, a:i2)
regs { r:reg[2] }
^entry():
r = lift.call @worker (x) (tk) (a) (db)
lift.retval r
lproc @worker (x:reg[2]) (r:reg[2]) (tk:token token) (a:i2 classical) (db:region[0,8] in)
regs { fr:reg[4], zero:reg[4], bad:reg[1] }
^entry():
lift.oracle_call @plus_db tk (x) r fr (db) (a)
zero = lift.const.i4 0
bad = lift.icmp.ne fr zero
lift.faultif bad 9
lift.perm_call @flip_arg (r) () () (tk, a)
lift.ret r
oracle @plus_db (x:wire[2] in) (t:wire[2]) (f:wire[4]) (db:region[0,8] in) (a:i2)
regs { base:reg[32], byte:reg[8], low:reg[2], r:reg[2] }
^entry():
base = lift.addr @db
byte = lift.load.i8 base
low = lift.trunc.i2 byte
r = lift.add x a
r = lift.add r low
lift.retval r
perm_action @flip_arg (x:wire[2]) () () (tk:token, a:i2) ()
^entry():
x x[0]

section layout
{"A_tab":2,"H":6,"S_cells":4,"globals":{},"heap_base":32,"heap_limit_max":32,"interface_regions":{"plus_db":{"db":{"base":17}},"through":{"db":{"base":16}}},"null_size":16,"ptr_width":32}
```

The outer invocation's B is independent of `tk`'s tuple. The sole
`@worker` binding key is `[0,1,0]` (oracle argument positions 0 and 1,
region position 0). It has five locations (`x r fr zero bad`), so
R_worker = 8 cells; forwarding the three additional parameters adds no
cells. The two outer rows precede its six rows: indices 0, 1 and 2..7,
HALT = 8, P = 4. `@plus_db` has six rows and no lproc calls. The byte
region maps at 16 in the outer oracle and 17 in the nested oracle;
both mappings refer to the same passed cells, with no byte copy.

For every x, a ∈ [0,4) and byte d ∈ [0,256), an outer tuple
(B ≥ 8, 0, stack_limit ≥ 8, depth_limit ≥ 1) and `tk` tuple (6,0,0,0)
give F_B(x,d) = (((x + a + (d mod 4)) mod 4) XOR 1, 0).
For arbitrary initial target t and fault f, the final values are
(t XOR payload, f); x and d are unchanged and all workspace is clean.
This permutation extends by linearity to superpositions and an
entangled reference. With outer B = 7 the success path has not executed
`lift.retval`, so the outcome is (0, `FAULT_BUDGET_STEPS`); with outer
stack_limit = 7 or depth_limit = 0 the first row gives
(0, `FAULT_BUDGET_DEPTH`). With `tk` tuple (5,0,0,0), the nested oracle
returns fault 1; the lproc's `lift.faultif` propagates code 9 at outer
step 5, so B ≥ 5 gives (0, `FAULT_CALLEE`). The nested fault, stack
history, parameters and locations are cleared by prefix reversal; no
additional charge arises from forwarding, commit or reversal.

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
   a schedule that names no `expansion` binds `ref` at the ISA version
   in the object's header, with the full-library envelope hash published
   for that version in §11.1. [deps: ISA-9.1, ISA-11.1-P3, ISA-11.1-P4]
   For a 0.9 object this is exactly
   `{"name":"ref","version":"0.9","hash":"5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197"}`,
   equally for omission and an explicit binding. [deps: ISA-11.1-P3, ISA-11.1-P4, ISA-11.1]
   §11.1 fixes its schema, ordinals, scratch identities, empty removable
   sets and deterministic decomposition algorithms. [deps: ISA-11.1]
   The bound catalog is published as `spec/ref-0.9.json`. The worked
   `ctl` action fixture (zsw.4) is in
   `conformance/fixtures/controlled-action-09/`: `controlled.bisa`,
   `target.json`, `leaves.json`, `schedule.json`, `frame.json` and
   `certificate.json`. It contains one exact controlled-X leaf, starts
   at time 0 and ends at time 1, with two live fast-class interface wires
   and no workspace. Its README records derivation and the pinned 0.8
   compatibility check separately from the 0.9 bindings.
8. **Enclosure procedure for transcendental entries** (§12.1). Default:
   Taylor series of sin and cos to the first term whose Lagrange
   remainder bound is below 2^−(`precision_bits` + 2), argument reduced
   modulo 2π with an outward-rounded enclosure of π.
9. **Default `epsilon_share`** (§8.1, §11) when a schedule assigns none.
   Default: the exact rational `bindings.epsilon / N`, where N is the
   number of gate operations in the bound-library expansion of one
   invocation of `bindings.region`, including every nested invocation,
   that have no exact native match as defined below. [deps: ISA-8.1, ISA-8.3, ISA-11-P2]
   For this count only, an exact native match is a `gates` entry whose
   opcode, classes, control range and parameters cover the operation
   and whose `epsilon` expression is independent of `eps` and evaluates
   to zero; compute this test before the requested-accuracy filter,
   without selecting an achieved-error entry using the default share. [deps: ISA-8.1, ISA-8.3]
   N counts the gate operations before target scheme expansion and
   includes operations with explicit shares as well as omitted shares;
   the root accuracy is `bindings.epsilon`, not a nested region's
   separately requested accuracy. [deps: ISA-11-P2, ISA-11-P3, ISA-8.2, ISA-8.3]
   Gates with an exact native match take a default share of zero; if
   N=0 all default shares are zero and no division is performed. [deps: ISA-8.1, ISA-8.3]
   The resolved share is represented exactly as a reduced pair (p,q)
   of nonnegative numerator and positive denominator, with zero
   represented by (0,1); it is passed as that rational value to every
   §8.1 comparison, expression and accuracy bucket, without rounding
   to a finite decimal. [deps: ISA-8.1]
   This is a resolved value, not an inserted `epsilon_share` field;
   existing decimal schedule fields and the hashed schedule bytes are
   unchanged by default resolution. [deps: ISA-11-P3, ISA-9.2]
   Explicit shares still supply `eps` by their exact value and the
   §8.1 requested-versus-achieved filter and achieved-error charge
   still apply to every resolved share. [deps: ISA-8.1, ISA-8.3]
   *(non-normative witness)* At `bindings.epsilon: "0.1"`, three gates
   lacking exact native matches give N=3 and default (1,30), even if
   one gate has an explicit share; a fourth, exact-native gate takes
   zero and is excluded from N. [deps: ISA-8.1, ISA-8.3, ISA-11-P2]
   With no such inexact gates N=0. [deps: ISA-8.1, ISA-8.3, ISA-11-P2]
   Omitting expansion on a 0.9 object selects the full-library hash in
   item 7, not the single-qxor witness hash. [deps: ISA-11.1-P3, ISA-11.1-P4]
10. **`any`-class resolution** (§11). Default: the first class in JCS
    order with capacity.
11. **Occupancy rate of a class absent from `rate`** (§8.2). Default: 1.
12. **Classical step timing of CC/R instructions and effects** (§8.2).
    Default: `classical_step_time` each, sequential.
13. **Suite sizes** (§15): the exhaustive widths of suite C and the
    sample counts of `sampled` claims. Default: exhaustive for ≤ 16
    interface bits; 2^16 samples above.
14. **Hardware handling of `qreg.free`** (§3.3). Cleanliness of an
    arbitrary state is not testable nondestructively. Default: on
    hardware the release proceeds without a test and its frame is
    marked unverified, so a segment containing it cannot be uncalled
    (§7.4) and a run containing it is not reverse-eligible (§10);
    releasing a register that was not clean is a program error the
    hardware does not detect *(non-normative: physically its wires are
    then discarded as by an unrecorded measurement; this is a program
    error, not a trace-out operation, §10)*. The same holds for
    `bennett_qreg_prepare` and `bennett_qreg_free` on a non-verifying
    executor. A verifying executor tests and records `FAULT_UB_TRAP` on
    failure (§4.9), or returns `E_QREG_NOT_CLEAN` from the host calls.
15. **Routing and movement cost under a topology** (§8.2–§8.3, §11),
    deferred to 0.10. Default: no routing cost is charged and no routing
    is inserted; a schedule that needs a non-adjacent pair is
    `E_SCHEDULE_INFEASIBLE` naming this item. Absent topology remains
    all-to-all. A producer can supply an explicitly routed gate sequence
    using §4.4 `swap` gates; those gates execute and are charged normally.
    The optional topology schema and adjacency validation are decided in
    0.9; only automatic routing and its movement-cost model are deferred.
16. **Exhaustion of an executor's own classical resources in CC/R**
    (activation stack, history storage; §4.9). CC and R carry no budget
    (§5.4 budgets are Q-tier), so where a finite executor runs out is
    its own limit. Default: a terminal fault record `FAULT_BUDGET_HEAP`
    at the instruction that cannot proceed, raised before any mutation
    by that instruction (§4.9; an executor that cannot guarantee this
    for an exhaustion inside a region call marks the run not
    reverse-eligible); the point is executor-defined and the suites do
    not test it.
17. **Identity-idle step** (§3.6). A variant of the step in which an
    idle step leaves its frame at zero: forward, a = (pc ≠ HALT) into
    clean scratch; dispatch k < n only; rows as printed; the successor
    XORs for k < n and both commit exchanges under a, with no HALT
    successor; then `old_pc ^= HALT` under a (an active frame holds old
    index ⊕ HALT, never 0, since the old index is < n = HALT);
    dispatch uncomputed from old_pc ⊕ HALT under a; a cleared from
    (old_pc ≠ 0). Inverse: a = (old_pc ≠ 0); dispatch from old_pc ⊕
    HALT under a; `old_pc ^= HALT` under a; the two inverse exchanges
    under a; successors and rows undone as printed; dispatch uncomputed
    from pc under a; a cleared from (pc ≠ HALT). Same frame width, same
    F_B and the same postcondition as T2; on pc = HALT with a fresh zero
    frame a forward step is the identity (candidate theorem T7).
    Default: the printed step, whose idle frames record HALT. Hook: an
    expansion library (§11) MAY name this variant as its realisation of
    §3.6, and a schedule binding that library executes and charges it;
    making it the reference changes §3.6 and adds T7.
18. **Checkpointed or pebbled oracle realisations** (§5.2, §5.7, §9.4,
    §11). Default: the full-history reference expansion (B frames, the
    library `ref`). Hook: an expansion library MAY realise §5.2 by
    checkpoints and replay or by pebbling; it MUST list every generated
    allocation, copy, forward evaluation, inverse evaluation and release,
    every repeated evaluation included, with distinct ordinals and
    scratch identities, and carry a full-domain argument that the final
    interface tuple of §5.2 is produced with private scratch clean and
    borrowed correlations restored; a schedule binds its name, version
    and hash; every replay is executed and charged (§8.2); the frame
    descriptor reports the realised history (§9.4); the reference body,
    F_B and the budget unit are unchanged, and T2 remains stated for the
    reference expansion. *(non-normative)* Binary pebbling P_{j+1}(a, b) =
    P_j(a, c); P_j(c, b); P_j(a, c) uses 3^⌈log₂ B⌉ base evaluations and at
    most ⌈log₂ B⌉ intermediate configurations; no polylogarithmic-time
    bound is claimed.
