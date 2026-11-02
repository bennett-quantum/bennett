# Council — derive3-2qc-2026-11-02 round 1

Document snapshot sha256 cdef451a4f49; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 5 | 5 | 5.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 4 | 4 | 4.0 |  |

Overall mean: 4.75

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Blocking issues

- none

## sol

Accept. The proposal correctly distinguishes existing executor enforcement from an insufficiently explicit checker coverage duty. Its owner, token and context premises match ISA 0.9; no substantive false technical premise was found. The insertion-location paragraph ending is misstated but its anchor is unambiguous. The authorized K repair preserves execution semantics and source/catalog identities while tightening checker conclusions.

**Path to accept:** Already acceptable through the explicitly authorized 0.9 K repair route. To raise C6 from 4 to 5, publish the complete nested object/certificate fixture and expected context results described above.

- **C1 5**: The repair uses classical invocation bindings and existing context identities; it introduces no machine-state or execution-tier change. *Change:* None required.
- **C2 5**: §4.5 already specifies the owner, symmetric pair coverage, componentwise primary-token minimum, exact argument-token tuples and argument domain. The proposal preserves these rules. *Change:* None required.
- **C3 5**: Disabled predicates do not excuse entered instructions, consistent with §§3.5–3.6. The proposal retains §4.5 preflight and §§4.9/7.4 fault-prefix preservation without inspecting superposed data. *Change:* None required.
- **C4 5**: Primary-token monotonicity follows the stated hypotheses in §5.4; separately forwarded token tuples remain fixed. Example 7's minimum [3,0,0,0] and the proposal's applicability results are correct. *Change:* None required.
- **C5 5**: The checker-duty ambiguity is real: §§12.1–12.3 specify claim verification and binding resolution without expressly requiring complete site coverage. The insertion supplies owner-local inventory, transitive applicability, linked-proof resolution and limited standalone conclusions. *Change:* None required.
- **C6 4**: The 12 reported replay tests independently pass. Both inverse compositions in example 7 hold on all 64 tuples. The note accurately distinguishes those checks from its unimplemented nested traversal vectors. *Change:* Conformance vectors: publish a complete outer→inner→qinplace object/certificate fixture with inner token actuals [3,0,0,0] and [2,0,0,0], entry minimum [3,0,0,0], and expected applicability results covered/uncovered with overall rejection. Changing the second token to [3,0,0,0] must establish coverage for both contexts.
- **C7 5**: The repair preserves checked in-place bijections and proof/evidence distinctions. Its mixed-fat-object section explicitly scopes coverage to each selected device root, excludes native-only inventory and names the outstanding boundary contracts. *Change:* None required.
- **C8 4**: The owner/site/context distinction is implementable. An in-memory insertion leaves all 10 example object blocks and the identity/reference-library clauses unchanged; the catalog check confirms 219 recipes and envelope hash 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. The unscheduled-tree shorthand could be more explicit. *Change:* §12.3: add 'Without a schedule, derive the reference invocation tree from the literal constructions of §§3.6, 4.5–4.7 and 5.2–5.3, retaining predicated calls regardless of predicate value and omitting dynamic visits inside zero-trip qloops.'

Suggestions:
1. Recommended exact spec diff, insertion instruction: the claimed paragraph ending is inaccurate. The current paragraph ends with 'Scheduled/numerical/channel claims retain the expansion library gate and all existing context and composition obligations.' Replace the location instruction with: 'Insert immediately before **CLAIM-BINDING witness**, after the complete Invocation binding (K13) paragraph.' The existing witness anchor already makes the intended location recoverable.
2. §12.3: add 'Without a schedule, derive the reference invocation tree from the literal constructions of §§3.6, 4.5–4.7 and 5.2–5.3, retaining predicated calls regardless of predicate value and omitting dynamic visits inside zero-trip qloops.' This makes the intended traversal explicit.
3. Conformance vectors: publish the complete two-inner-context fixture with minimum token [3,0,0,0]. Actual tokens 3 then 2 must yield covered/uncovered and rejection; 3 then 3 must establish both contexts' coverage. An outer root budget of 9 must not change either result.

## codex

The defect is accurately scoped and the diff repairs it without changing executor semantics, source identities or catalog bytes. The reported focused tests reproduce. No S0 issue found; the inaccurate insertion anchor is editorial.

**Path to accept:** Accepted as the explicitly council-authorized 0.9 K checker-obligation repair proposed by the note. To raise C6 from 4 to 5, publish the concrete nested-context fixture with the stated expected results; the current finite predicate demonstrates the distinction but does not exercise traversal.

- **C1 5**: The diff adds certificate obligations without changing state, tiers or execution. Its context-local token resolution agrees with §§4.7 and 5.4. *Change:* No change required within this proposal's scope.
- **C2 5**: §4.5 confirms the stated owner, unordered closure pair, componentwise primary-budget comparison, exact argument-token tuples and classical argument domain. Example 7's minimum budget is correctly stated. *Change:* No change required; retain the explicit reference to §4.5's complete covering test.
- **C3 5**: The proposal preserves pre-effect FAULT_UB_TRAP, both inverse compositions, full quantum-input quantification and source-adjoint pair exchange. Disabled coherent predicates cannot bypass coverage. No quantum-state inspection is introduced. *Change:* No change required within this proposal's scope.
- **C4 5**: Per-context checking includes default-covered invocations without changing target resources, schedules or generated operations. Primary-token monotonicity and exact nested-token equality match §5.4. *Change:* No change required within this proposal's scope.
- **C5 5**: The checker-duty ambiguity is real: §§12.1 and 12.3 specify claim verification and binding resolution but do not explicitly require site coverage. The diff supplies owner-local inventory, transitive applicability, incomplete outcomes and safe reuse. §9.2 excludes certificates from object_hash; no source envelope or catalog change is required. *Change:* No change required; retain the explicit compatibility notice and council-authorized publication route.
- **C6 4**: The 12 reported replay tests pass. The INDEX coverage predicate, all 64 example-7 inverse compositions and the published ref@0.9 catalog hash also reproduce. These checks do not implement nested traversal, as the note correctly acknowledges. *Change:* In Conformance vectors, add a serialized outer/inner fixture with two context keys and state: 'The first inner invocation, tk=[3,0,0,0], is covered; the second, tk=[2,0,0,0], is uncovered; the bound root is rejected even when its own budget is [9,0,0,0].'
- **C7 5**: Checked in-place bijections and honest proof/evidence scope preserve North Star §§3.1, 4.2 and 5.1. The mixed-object section scopes checking to selected device roots and linked closures, excludes native-only inventory, and names the remaining mixed-launch and memory-boundary obligations. *Change:* No change required; preserve the mixed-fat-object statement when publishing the repair.
- **C8 4**: The obligations and incomplete-result default are implementable. The insertion anchor inaccurately describes a paragraph ending at 'not a target realisation'; that paragraph actually has another sentence. The unscheduled traversal could also be made easier to implement by explicitly referencing the padded Q construction. *Change:* In the §12.3 insertion, add: 'Without a schedule, derive entered contexts from the bound reference Q construction (§§3.6, 4.6 and 5.2), retaining coherently disabled calls; do not derive coverage solely from a basis-input interpreter trace.'

Suggestions:
1. Conformance vectors: publish the concrete two-inner-context fixture and expected per-context results described under C6. Include its default-covered and source-adjoint forms; each must reject because the second invocation is uncovered.
2. Recommended exact spec diff: replace the placement instruction with 'Insert immediately before **CLAIM-BINDING witness**, after the sentence “Scheduled/numerical/channel claims retain the expansion library gate and all existing context and composition obligations.”' The current paragraph-ending description is inaccurate, although the intended location is identifiable.
3. §12.3 Qinplace coverage checking: add the reference-Q-construction sentence given under C8. As an illustrative vector, a qloop 0 body requires static pair inventory but has no applicability visits; a reached qinplace under a zero coherent control still requires applicability.
