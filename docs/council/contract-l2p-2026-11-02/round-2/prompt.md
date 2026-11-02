# Council

You are a member of a two-model council (sol, astra) grading the document below, ISA contract proposal l2p, round 2: K85 private measurement cleanup with checked relocation, 0.10 amendment (sol-bwm, b-isa-spec-bwm). This is ROUND 2: the document is a full, self-contained revised proposal that supersedes the round-1 note (the round-1 snapshot is `../bennett/docs/council/contract-l2p-2026-11-02/round-1/doc.md`; the members' outputs are beside it). Its section "Round-1 blocking items and resolution" is the editor's response, and its section on the mixed fat object (bennett-4ht) answers the rubric's standing check. The document is a contract-repair proposal note for the published Bennett ISA 0.9. It carries a defect statement, alternatives and a "Recommended exact spec diff". Grade the proposal, meaning its proposed spec diff and the claims supporting it, against the rubric on the absolute scale. The rest of ISA 0.9 is accepted text and is not under review, except where the diff interacts with it. Be exacting and skeptical. Verify every technical premise against your own knowledge and against the actual spec text. Name any premise that is false, including a misquoted or misnumbered clause.

Document map for this proposal: it is a 0.10 amendment (proposed K85), not a 0.9 K repair; its "Recommended exact spec diff" is the set of BEFORE/AFTER blocks in sections B-E (core, K85) and G (optional, separate efficiency entry); section A states release and scope; section J is its "Round-1 blocking items and resolution"; sections A, D1 and D3 answer the bennett-4ht standing check (with `docs/notes/2026-11-02-rev2/fat-object-scope.md`). Wherever the instructions below say "as a 0.9 K repair", read "as the proposed 0.10 amendment (K85, plus the optional G entry if you accept it separately)". The author's verifier is `docs/notes/2026-11-02-rev3/verify_l2p.py` (read-only; it writes nothing).

You run read-only in `bennett-isa-spec`. The normative text the diff amends is `spec/Bennett-ISA-Spec-0.9.md`. It is NOT attached because of its size. Read the clauses the note cites, and every clause the diff touches, before grading. Other files you can read:
- `docs/notes/` holds the sibling proposal notes of 2026-11-02 and `docs/notes/2026-11-02-contract-verification.md`, the author's verification index with its reproduction scripts.
- `reference-interpreter/` is the reference interpreter.
- `.beads/issues.jsonl` holds the beads the notes cite.
- `../bennett/docs/Bennett-NorthStar.md` is the north star, also attached below.
- `../bennett/docs/council/` holds earlier council rounds, including `isa-09-k82-2026-11-01` (K82).

A blocking issue is one that would make the project build the wrong thing if the diff were applied as written, or if it were left unapplied while the note's defect is real. Everything else is a suggestion. Return `accept` only if the blocking list is empty. `accept` means that the editor may apply this diff (with your suggestions at their discretion) as a 0.9 K repair.

Be constructive, always. The editor must be able to act on your output without asking you anything. For every blocking issue, the `fix` field must give:
- the section;
- the sentence or rule the diff should state (write it out);
- where an example is involved, the corrected example or expected value.

Each blocking item carries either `steps` (step 1 the spec clause, a later step a reproducible witness) or a precise `problem`, and a `kind`: `implementation` when the note's diff is wrong, `spec-gap` when the spec is silent in a way the note does not repair. Where two viable ways out exist, name both and say which you would take. Every `suggestions` entry and every criterion's `change` field follows the same rule. In `path_to_accept`, state the minimal ordered set of changes that would make you return `accept`. If you already accept, say what would raise the lowest-scoring criterion by one point.

Grading instructions for this proposal (advisor ruling R7, 2026-11-02, binding; quoted verbatim):
"(i) the clean-isometry perm-provenance rule is an efficiency extension, graded on soundness only, not required for acceptance; (ii) the §9.6 claim is overstated: under control unitary cleanup remains the sanctioned fallback; (iii) apply the bennett-4ht rubric (channel claim §12.1 and certificate layout)."
The advisor has already ruled that l2p is a real north-star gap and ISA blocker (b-isa-spec-bwm, P1); do not re-litigate whether the gap exists. Grade the note's "Recommended exact spec diff" as the mechanism that closes it. Under (i): a defect in the perm-provenance rule blocks only if it is unsound (it admits a program whose semantics differs from its claim); its absence or narrowness is never blocking. Under (ii): treat the note's §9.6 claim as overstated, and block only if the diff as written would forbid or remove unitary cleanup under control. Under (iii): apply the rubric's standing check "the mixed fat object stays reachable" to the channel claim in §12.1 and to the certificate layout the diff adds.

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
3. This is round 2. Fill `previous_status` for every blocking issue of round 1 (listed under "Previous round" below, from both members, by id) with resolved | partially | unresolved | regressed and a one-line note. List in `regressions` anything that was correct in the round-1 snapshot and is wrong now. Re-raise a round-1 item in `blocking` only if it is not resolved; then re-read the whole document for new S0 issues, including the bennett-4ht standing check.
4. Give `verdict_core` (accept/revise/reject) for the core scope alone, and `verdict` for the whole proposal.
5. Check hash and catalog claims: if the note says no canonical bytes or hashes change, verify that the diff really leaves them unchanged. If they do change, the note must say so and say how consumers move.
6. Formal correctness is pursued after practical revisions: correct *statements* with explicit hypotheses are required, proofs are not. Demands for proof formats, mechanisation or checker algorithms are S1 as long as the obligation and a default procedure are stated.


Blocking items: `steps` are optional; use them (3 to 6 objects {"n": "<1>1", "claim": "...", "by": "..."}) for implementation findings with a reproducible witness, else give a free-text `problem`; leave the other empty.
Steps: <1>1 what the spec requires (`by`: `clause:<ID>` or `ASSUMED: <why the spec is silent>`); <1>2 what the implementation does (`witness:<path or command>`); <1>3 an input where they differ; last step cites earlier ones (`step:<1>1`).
`OPEN: <what is missing>` marks an unjustified step; several `by` parts are separated by `; `.
If the spec is silent (step 1 or `problem` begins `ASSUMED:`) set `kind` to `spec-gap` (otherwise `implementation`); a spec gap goes to the spec owner,
is not an editor blocker and does not count against `accept`.


# Previous round (1)

Verdicts: sol: revise, codex: revise

Blocking issues raised last round:
- [sol] B1 (Recommended exact spec diff: §§6.2, 6.4 and 11/K65–K81): The closed-window exception does not reconcile the remaining source rules with its proposed realisation. §6.2 still requires each cleanup’s external input versions to be current. §11/K81 forms source pairs using §§5.3 and 6.2 before selecting realisations, and §11 retains source dependency ordering. The new text permits closed windows but neither identifies a legal earlier source cleanup as the reference nor expressly permits its relocation across those dependencies. This problem exists even without the optional clean-isometry extension: d=qcopy a; h a; quncopy a d cannot form the required source pair after H changes a. Its literal late inverse also supplies the wrong reference: on initial a=d=0 it produces (|00>+|11>)/sqrt(2), so d is one with probability 1/2. The desired measurement-assisted realisation instead produces |+>_a|0>_d. The exact helpers in docs/notes/2026-11-02-contract-verification.md reproduce these states as flip(hadamard(flip({0:ONE},1,(0,)),0),1,(0,)) and hadamard(flip(flip({0:ONE},1,(0,)),1,(0,)),0), respectively. The mechanism needs to decide which source operation is being implemented and how its delayed cleanup remains selectable. Fix proposed: In §§6.2 and 11 add: “A measure_fixup witness binds a well-formed source computing/cleanup pair at its original K65 carrier and an explicit later realised cleanup location. Source pairing uses the original legal source versions. The witness MAY delay that cleanup across identified intervening operations, extending workspace lifetimes and replacing the corresponding scheduling dependency edges. The checker verifies the complete realised region channel against the unchanged well-formed source region, including all interface wires, inherited controls, borrowed systems and clean workspace restoration. The current-version and window restrictions remain mandatory for reverse/recompute; the checked relocation rule governs measure_fixup.” Give this corrected example: reference source d=qcopy a; quncopy a d; h a; realised sequence d=qcopy a; h a; X-measure d; apply H_a Z_a^m H_a=X_a^m; reset/release d. Each branch operator on a is H/sqrt(2), and input zero finishes as |+>_a with d clean. For the AND example, use reference C; cx g y; C†; release g; h a, whose interface operation is H_a CCX(a,b;y); the delayed realisation uses H_a CZ(a,b)^m H_a. Alternatively, introduce an explicit transported logical-cleanup source operation with a defined unitary reference and amend source pairing and grammar accordingly. I would take the legal-source/checked-relocation approach because it preserves existing source bytes and hashes.
- [sol] B2 (Recommended exact spec diff: §§12.1 and 12.3; bennett-4ht standing check): The diff adds channel claims and certificate cleanup witnesses but never states their use in a mixed fat object containing native host code and only marked device modules. Hiding private outcomes from the launch measurement list does not establish certificate inventory or subject scope. The binding standing check explicitly requires this statement for certificate-layout changes; its absence requires revise. Fix proposed: In §§12.1–12.3 add: “A mixed fat object may contain native host code and multiple embedded ISA modules. Each channel subject identifies a region closure within its embedded device object and covers that region’s declared device interface and device callee closure. Native host entry points, argv/envp and unlifted native library code are outside that quantum channel subject. The default certificate layout is one certificate per embedded ISA object, with a fat-object inventory mapping each device module to its object_hash and certificate. Native comparison, where claimed, concerns the materialised outlined region and its materialised callee closure. Private cleanup outcomes remain internal to the device invocation and do not enter the host-visible measurement inventory.” A unified certificate with explicit per-module bindings is also viable; I would take the per-module default because it preserves the existing single-object bindings.
- [codex] L2P-1 (Recommended exact spec diff: §§6.2, 6.4 and 11; closed-window witness): <1>1 Source regions require explicit cleanup. Cleanup matching requires current computing-input versions, and K81 forms source pairs before realization selection. The source reference therefore cannot silently mean a differently ordered cleanup. (clause:§5.1; clause:§5.3 matched pairs; clause:§6.2; clause:§11 K65/K81) <1>2 The diff permits closed-window witnesses but retains those source-pair requirements and compares the realization against 'the source's unitary-cleanup semantics'. It does not define how a legal source cleanup is moved past the operation closing its window. (witness:docs/notes/2026-11-02-contract-l2p.md:131-187) <1>3 A literal C; CX(g,y); H(a); C† is not the intended clean reference. Starting from (a,b,g,y)=(0,1,0,0), it produces (|0,1,0,0> + i|1,1,1,0>)/sqrt(2), so g=1 with probability 1/2. This reproduces by loading the verification script's definitions and evaluating sequence(hadamard(flip(sequence({2:ONE},C),3,(2,)),0),CDAG). (witness:docs/notes/2026-11-02-contract-verification.md exact Python block; clause:§4.4) <1>4 The correctly transported measurement cleanup instead produces (|0,1,0,0> + |1,1,0,0>)/sqrt(2). Its reference is C; CX(g,y); C†; release(g); H(a), whose logical operation is H(a)CCX(a,b;y). (witness:docs/notes/2026-11-02-contract-verification.md branches and expected functions) <1>5 Thus admitting the direct post-H source contradicts source cleanliness/reference semantics, while enforcing the retained source rules without a delayed-cleanup rule leaves the advertised closed-window realization unsupported. This is a missing semantic bridge, not merely an unenumerated witness field. (step:<1>1; step:<1>2; step:<1>3; step:<1>4) Fix proposed: In §§6.2/6.4 and §11 add: "A measure_fixup realization replaces a cleanup that is valid at its original source point. K81 pairing and source-version checks are performed at that point. The realization MAY delay its measurement, correction, reset and release past subsequent source operations; for this replacement, the original cleanup ordering/version dependencies are replaced by the explicitly bound realized dependencies. All operands must be live at their realized versions, the extended workspace lifetime must be accounted for, and the complete realized channel must satisfy §12.1 against the original unitary source, before the delay. Other operations may not access a source-released lifetime." Publish the positive vector with source C; CX(g,y); C†; release(g); H(a), realization C; CX(g,y); H(a); X-measure(g); conditional H(a)CZ(a,b)H(a); reset/release(g), and expected operation H(a)CCX(a,b;y). On input (0,1,0,0), the expected state is (|0,1,0,0>+|1,1,0,0>)/sqrt(2). Alternatively introduce an explicit logical-cleanup source construct with independently defined transported semantics and corresponding source-hash migration. I recommend the schedule-transformation rule because it preserves existing source semantics and bytes.
- [codex] L2P-2 (Recommended exact spec diff: §12.1 channel claims and §12.3 cleanup certificate layout): The proposal adds channel and cleanup-certificate obligations without stating how they attach to a mixed fat object. The binding bennett-4ht check expressly requires that statement for these changes. Nothing identifies the native-host/device boundary of the new channel subject and certificate inventory; mentioning the launch measurement list does not supply it. Fix proposed: Add to §§12.1/12.3: "A mixed fat object may contain a native host binary and ISA objects for only its marked device modules. Native main, argv/envp handling, unmarked libc and ordinary host effects remain native. Its launch manifest associates selected exported VM entries with their device closures, schedules and certificates. A cleanup channel subject and its invocation-context inventory cover that selected device closure, including its interface systems and external correlations, not the entire host binary. Private cleanup outcomes are absent from host results and launch measurement records. Native comparison, where applicable, uses the corresponding materialized marked entry and its callee closure with captured launch inputs; unrelated native host code need not have an ISA or channel certificate." Example: native main may call ordinary libc, launch a marked AND module, and continue natively; only the selected device invocation receives the cleanup-channel certificate. A container-level certificate referencing these per-closure records is also viable; I recommend per-closure records without requiring a new whole-binary quantum certificate.

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


# The document under review (round 2 snapshot)

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
