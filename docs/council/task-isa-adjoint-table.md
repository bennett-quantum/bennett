You are a member of a three-model council (sol, astra, Muse) grading the document below, SUBJECT. The document is an in-version
ISA 0.9 contract repair: it carries its own exact diff (spec text, reference-interpreter implementation, tests, conformance
cases). Grade the repair (its spec text and the implementation's fidelity to that text) against the rubric on the absolute scale.
The rest of ISA 0.9 is accepted text and is not under review, except where the diff interacts with it. Be exacting and skeptical:
verify every technical premise against the actual spec text; name any premise that is false, including a misquoted or misnumbered
clause. Return `accept` only if the blocking list is empty.

You run read-only in a frozen snapshot of `bennett-isa-spec` at the candidate commit. The normative text is
`spec/Bennett-ISA-Spec-0.9.md` (too large to attach; the packet below carries every changed file in full). Read §5.3 (the adjoint
table), §12.1 (claims, the `structural` row and the new adjoint_table text), §12.2-§12.3 where the text refers to them, and §16.3
example 3. The reference interpreter is in `reference-interpreter/` (binary built at `reference-interpreter/target/debug/bennett-isa-ref`);
the new checks are `reference-interpreter/src/claims/adjoint09.rs` (plus the shared body-shape guards in `reference-interpreter/src/object.rs`), its tests `reference-interpreter/tests/isa09_adjoint_table.rs`,
the conformance cases `conformance/cases/F/F-adjoint-table-*`. The north star is `../bennett/docs/Bennett-NorthStar.md`.

Why this repair exists: §12.1 told checkers to "check the rule's side conditions syntactically against the object and the subclaims'
results" for `rule: adjoint_table`, but never said what those side conditions are, so the reference interpreter returned Unverified
for every adjoint_table claim (37 published universal claims in bennett-arith; first witness `arith.bij.add.w1` claim 1, copied as
`reference-interpreter/tests/support/adjoint-table/arith.bij.add.w1.bisa`). The reference interpreter is the project's ORACLE:
certificates (north-star rung 4(a)) consume these claims.

Be constructive, always: for every blocking issue the `fix` field gives the section and the sentence or rule the text should state
(write it), and where an example is involved the corrected example or expected value; the `steps` carry the witness (step 1 the
spec clause, a later step a reproducible witness: a quoted line, a path, or a command you ran in the snapshot with its output).
Where two viable ways out exist, name both and say which you would take. In `path_to_accept` state the minimal ordered set of
changes that would make you return `accept`; if you accept, say what would raise the lowest criterion by one point.

Answer only with JSON matching the schema.

Convergence rules for this council (read before grading):
1. Blocking means S0 only: two conformant checkers built from the text would return different verdicts for the same claim; the rule
   is unsound (a claim whose premises were not actually established can come out as proof, i.e. the oracle certifies too much);
   the text is self-contradictory or contradicts §5.3/§12.1-§12.3; a normative decision needed to build a checker is missing; the
   reference implementation diverges from the text so that it returns proof where the text does not; or the repair narrows
   north-star scope (rejects a well-formed, true adjoint_table claim that the previous text admitted as checkable in principle, or
   removes a capability). Tag every blocking issue with `scope` (`core` = claim semantics and soundness; `contract` = encodings,
   diagnostics, conformance-case layout) and `severity` S0. S1 items (an implementer would have to choose but any choice is
   conformant; diagnostic wording; extra test ideas) go to `suggestions`.
2. Give `verdict_core` for the claim semantics alone and `verdict` for the whole repair.
3. This is the ONLY council round for this candidate (policy rule 5 as amended 2026-11-07): your blocking items become beads and the
   editor fixes them once; there is no second round unless the maintainer orders one. Be precise rather than numerous.
