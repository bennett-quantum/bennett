# Council — isa-09-2026-10-31 round 6

Document snapshot sha256 7b77c96e08a1; rubric /home/tobias/Projects/bennett-workspace/bennett/docs/council/rubric.md. Members: codex. Scores are advisory.

| | codex | mean | spread ≥ 2 |
|---|---|---|---|
| C1 | 5 | 5.0 |  |
| C2 | 4 | 4.0 |  |
| C3 | 5 | 5.0 |  |
| C4 | 5 | 5.0 |  |
| C5 | 5 | 5.0 |  |
| C6 | 4 | 4.0 |  |
| C7 | 5 | 5.0 |  |
| C8 | 4 | 4.0 |  |

Overall mean: 4.62

Verdicts: **codex: revise**

Core verdicts: **codex: revise**

**Consensus: no**   **Core consensus: no**

Blocking by scope: codex: core 1 / contract 0 (blocking 1)

## Blocking issues

- **[codex] R6-CODEX-1** (§5.6 Entry-state analysis, rule 1; §2 effective control context; §8.3 own versus total controls; core): *Fix:* In §5.6 rule 1, replace “An effective control known false disables the operation.” with: “If any control literal is known false, counting the operation’s own controls together with its effective control context, the operation is disabled: preserve all abstract values and record no causal event.” Keep the existing all-operands-known rule after this shortcut. Add the body in step <1>2 as a suite F/frame_domain case with expected acceptance and c=0 at frame entry. The alternative is to restrict the reference shortcut to contextual controls and require this object to fail; I recommend the text repair because it preserves the implemented, sound known-false analysis and the maintainer’s chosen admission boundary.
  <1>1 §5.6 first disables an operation when an “effective control” is known false, then makes an X-family target unknown unless all operands are known. §2 defines the effective control context as active predicates plus inherited controls, and §8.3 distinguishes these from a gate’s own controls. §5.6 forbids a stronger analysis from narrowing D_F.  — clause:ISA-5.6 (entry-state rule 1 and opening paragraph); clause:ISA-2-P10; clause:ISA-8.3
  <1>2 Use a perm_action with interface t:wire mut and u:wire in, no arguments, bounds or memory, and this complete body after ^entry():
z = qalloc any 1
c = qalloc any 1
ccx z u c
b = qborrow any 1
cx c b
qreturn b
ccx z u c
qfree c
qfree z
The current reference check accepted this object through /dev/stdin, returning status ok. It used the 0.8 header and signature abi under the binding erratum; the probe interface hash was eb30a43722acc6c124c4c4bea0e3649915b964ea4e08806933e96cc4c37581f6 and object hash 64de1ae460626ce409f99b798e654b3c9bf05b3a9d53ded0fdb93a0a416f019c. No file or repository modification was needed.  — witness:/home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/target/debug/bennett-isa-ref check /dev/stdin; witness:reference-interpreter/src/borrow.rs EntryAnalysis::condition and EntryAnalysis::apply
  <1>3 On the literal contextual-control reading, ccx z u c has an empty effective control context. Since u is unknown, not all operands are known, so the rule makes c unknown. At the subsequent single-gate frame, D_F includes c=1,b=0; cx c b sends b to 1. No P′ acting independently of B can satisfy the required identity on B over that domain. The later cleanup does not repair a failed individual frame obligation.  — step:<1>1; step:<1>2; clause:ISA-5.6 (Cartesian-product domain and restricted factorisation)
  <1>4 The reference tests all controls, including the explicit z operand of ccx. It skips the operation because z=0, retaining c=0, and the frame is identity on its resulting domain {c=0} × {b=0,1}. This explains the observed admission and agrees with the intended known-false transfer, but is stronger than the contextual-control reading of rule 1.  — step:<1>2; witness:reference-interpreter/src/borrow.rs EntryAnalysis::condition and EntryAnalysis::apply; clause:ISA-4.4
  <1>5 Thus the published control terminology and the aligned reference lead to different D_F and different validity decisions for one finite object. This is an S0 normative admission ambiguity, rather than a choice of proof format or a missing optimisation; both candidate domains conservatively contain the reachable entry state.  — step:<1>1; step:<1>3; step:<1>4

## codex

I confirmed the pass-IV/V diff first, reviewed the complete specification and supplied background, and found one new core S0 issue; round 5 had no blockers to carry forward. D_F is finite and decidable from a resolved object for each permitted invocation, without a semantic reachability oracle, and the exact transfer/cancellation construction otherwise gives an implementation-independent domain. As written, however, the own-versus-effective-control shortcut admits two different domain computations: the reproduced known-false CCX witness is accepted by the aligned reference but rejected by a literal contextual-control reading. The restricted equality itself is sound: reachable entry support in span(D_F), independent full borrowed/interface factors, and linearity imply the equality tensored with identity on the rest of the region and any external reference; repaired INV-3 supplies precisely that missing support step. I found no conflict between K76’s intended frame-domain obligation and K1–K75 or INV-3, and no weakening of whole-region coverage or host-limit rules. Pass IV’s memory-write qualification and permissive dependency test are sound; the 25 example hashes, published catalog envelope and controlled-action fixture byte checks passed. Both verdicts are revise solely for the control-shortcut wording, not for entanglement, proof mechanisation, or the non-blocking catalog/loop-summary clarifications.

**Path to accept:** Resolve R6-CODEX-1 by explicitly including own and contextual controls in §5.6’s known-false shortcut, then confirm the supplied witness is admitted with c=0 at frame entry while the existing polynomial-prefix and interface-correlation negatives still fail. No other semantic change is required for acceptance. Regenerating the statement layer and clarifying loop summaries would improve C6/C8 but are not additional acceptance gates.

- **C1 5**: §1.1, §§3–7 and §§8–13 describe one classical/reversible/coherent machine with independent execution, scheduling and verification contracts. Passes IV and V preserve the north-star capabilities and make borrowed-wire admission more explicit. *Change:* Optional signpost in §1.1: “The VM and circuit specialiser implement the same region semantics; their execution strategy does not change the region’s declared operation or its certificate obligations.”
- **C2 4**: The restricted frame-factorisation statement is mathematically sound with the stated support hypothesis, and the causal adjoint rule includes all readers. However, §5.6 rule 1 uses “effective control” where the implementation tests both own and contextual controls; the distinction already made in §§2 and 8.3 changes which constants survive and therefore changes admission (R6-CODEX-1). *Change:* In §5.6 rule 1 replace the first sentence with: “If any control literal is known false, counting the operation’s own controls together with its effective control context, the operation is disabled: preserve all abstract values and record no causal event.” Retain the subsequent all-operands-known rule for operations not disabled this way.
- **C3 5**: §§3–5 retain virtual allocation, arbitrary borrowed states, bounded coherent control and padded execution; §§8–11 account for the resulting resources. The new support premise permits tensoring the restricted equality with identity on every untouched wire, so entanglement with the rest of the region introduces no new borrowed-wire loophole. *Change:* Optional explanatory sentence after §5.6’s final paragraph: “Writing an entering state as Σ_d |d⟩|r_d⟩ with d ∈ D_F proves the same equality after tensoring with identity on all untouched region wires and any external reference; mixed states follow by purification.”
- **C4 5**: §1.2 assigns separable conformance obligations, while object identities, targets, schedules and certificates bind the replacement boundaries explicitly. Publishing the full ref catalog and the controlled-action fixture strengthens those boundaries without making the reference interpreter the only permitted implementation. *Change:* Optional note in §1.2: “A replacement scheduler or checker is assessed against the versions and bindings carried by the object and its associated artefacts, independently of which producer or executor supplied them.”
- **C5 5**: §1.1 deliberately keeps the ISA independent of LLVM, and the CC/R/Q call and host boundaries provide a concrete target for the north-star producer architecture. Nothing in the reviewed changes introduces a compiler fork requirement or removes a promised source-language or execution capability. *Change:* Optional clarification in §1.1: “A producer may use LLVM or another implementation; conformance is determined by the emitted object and its ISA semantics.”
- **C6 4**: I recomputed all 25 displayed symbol hashes, checked the 219-recipe catalog envelope, and ran the read-only controlled-action fixture byte check successfully. The attached statement layer still describes the pre-pass-V §5.6 and lacks the new statements cited by repaired INV-3, while the false-control boundary needs a normative conformance case. *Change:* Regenerate the attached 0.9 statement layer from the final specification, record that revision’s SHA-256, and resolve every repaired INV-3 §5.6 citation against it. Add the explicit-control witness in R6-CODEX-1 to suite F with expected admission, alongside the existing polynomial-prefix rejection.
- **C7 5**: The background distinguishes the VM contract from circuit languages and compiler frameworks, and the ISA makes its inherited constructions concrete rather than claiming new gate mathematics. §17 item 18 correctly charges pebbling replay and explicitly avoids a polylogarithmic-time claim. *Change:* Optional provenance sentence in §17 item 18: “The checkpointing construction is an implementation choice for the declared oracle semantics; its repeated forward and inverse evaluations are part of the realised resource cost, not a reduction in the declared budget unit.”
- **C8 4**: The normative transfer rules, independent interface/borrowed factors, repeated-visit union and support obligation make the intended domain substantially clearer. The own-versus-effective-control wording is the remaining admission-sensitive defect; the loop-summary wording and stale statement catalog are useful non-blocking clarification work. *Change:* Add to §12.2: “For a borrow-frame obligation, the required domain is D_F defined in §5.6; the region-claim domain D and its coverage accounting remain unchanged. A whole-region claim does not discharge a frame obligation unless it proves that obligation over all of D_F.”

Suggestions:
1. S1 — §5.6 rule 3: make explicit that the finite repeated transfer defines the canonical D_F, while loop summaries are proof representations. Suggested sentence: “The normative D_F is the union obtained by the stated finite transfers; acceleration must preserve that domain. A coarser invariant may prove the obligation on a superset, but failure on that superset is not a counterexample on D_F.” The existing per-visit rule supplies the baseline, so this is clarification rather than a second blocker.
2. S1 — Attached 0.9 statement layer and INV-3 references: regenerate the catalog from the final spec revision. Its §5.6 currently retains the old full-operator sentence and omits the new entry-analysis paragraphs. The regenerated record must contain the restricted equality, K76, and the support/linearity statements cited as ISA-5.6-P13.S5 and ISA-5.6-P13.S6; update citations if regeneration changes their identifiers. This is evidence-maintenance work, not a defect in the repaired mathematical argument.
3. S1 — §12.2: add “For a borrow-frame obligation, use D_F of §5.6; a region claim over D does not by itself establish the frame claim.” Illustrate with c allocated at zero: the single frame CX(c,b) has domain {c=0} × {b=0,1}; the interleaved polynomial-only prefix in reference-interpreter/tests/frame_domain.rs instead gives both c values under the normative analysis and must fail that frame obligation.
