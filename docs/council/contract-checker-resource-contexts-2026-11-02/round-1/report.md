# Council — contract-checker-resource-contexts-2026-11-02 round 1

Document snapshot sha256 deb2675e092b; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 4 | 4 | 4.0 |  |
| C5 | 4 | 4 | 4.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 4 | 4 | 4.0 |  |

Overall mean: 4.5

Verdicts: **sol: accept**, **codex: revise**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: no**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 1 (blocking 1)

## Blocking issues

- **[codex] RC-1** (Recommended exact spec diff — §12.3 resource values and optional estimate; contract): *Fix:* In §12.3 add: 'For every resources map, including single-context maps, resource_contexts records and unkeyed projections, accounting is performed in exact rational arithmetic. Whether or not estimate is present, each reported value uses §10.1’s canonical 34-significant-digit upward decimal encoding. The checker compares that encoding with the encoding of its recomputed exact value, not the displayed decimal with the exact rational. When estimate is present, its reduced exact_resources fractions MUST also equal the recomputed values; K12’s existing mandatory-estimate obligations remain unchanged.' Thus time 1/3 displays as '0.3333333333333333333333333333333334'; an included exact_resources entry is {"numerator":"1","denominator":"3"}. A viable alternative is to require estimate whenever any total lacks an exact finite decimal representation, retaining exact decimal equality otherwise. I recommend the unconditional encoding rule.
  <1>1 Target cost expressions admit division, and §8.2 aggregates their exact rational values. The resource schema stores decimal values; §10.1 supplies upward decimal encoding and exact-resource binding for estimates.  — clause:§8.1; clause:§8.2; clause:§10.1; clause:§12.3
  <1>2 The proposed rule requires exact resource accounting for every context, leaves estimate optional, and invokes §10.1 encodings only for an estimate in the record. It supplies no numeric encoding or comparison default for a non-estimate report with a non-terminating resource value.  — witness:docs/notes/2026-11-02-contract-checker-resource-contexts.md, Recommended exact spec diff
  <1>3 Change the witness target’s native duration to {"op":"/","args":[1,3]} and omit estimate. Each child’s exact time is 1/3; the root time is 2/3. Neither has a finite exact decimal representation. Reproduction: python3 -I -B -c 'from fractions import Fraction as F; print(F(1,3), 2*F(1,3))'.  — witness:python3 fractions arithmetic; clause:§8.1
  <1>4 A checker comparing the reported decimal to the exact rational rejects every possible time value, while one extending K12’s rounding convention accepts its upward encoding. The amended text must select that verdict; this is not merely an unspecified serialization layout.  — step:<1>1; step:<1>2; step:<1>3

## sol

Accept. The cited defect exists, and the proposed context records repair it without changing execution semantics or double-counting root costs. Hash and catalog claims hold for the proposed in-version repair. Remaining suggestions concern explanatory wording and executable fixtures.

**Path to accept:** Already acceptable. To raise C6 from 4 to 5, publish and execute the complete repeated-context certificate fixture with the stated positive totals and negative mutations.

- **C1 5**: The diff changes certificate metadata only. Invocation identity comes from §12.1; the machine state and §3.1 control invariant remain unchanged. *Change:* No required change. Optional §12.3 clarification: 'Resource-context records introduce no machine state or execution-time scheduling decision.'
- **C2 5**: No instruction changes. The worked action_call and ctl forms agree with §4.7, and native-leaf counting agrees with §§8.2–8.3. *Change:* No required change. Optional §12.3 clarification: 'gates_used counts native gate leaves after target-scheme expansion, each leaf exactly once.'
- **C3 5**: Counting controlled operations independently of the control's basis value preserves the classical scheduling invariant. Oracle construction, cleanup and existing error composition are unchanged. *Change:* No required change. Optional §12.3 sentence: 'Resource charges do not depend on whether a quantum predicate is true on a particular basis input.'
- **C4 4**: The proposal correctly distinguishes count, makespan, occupancy and peak. Its child values (1,1,1) and (1,2,2), and root time/occupancy/peak (2,4,2), follow under the stated intervals and rates. The published controlled-action fixture also includes the inherited control in the child's footprint. *Change:* §12.3, make the intended subtree view explicit: 'A child view restricts wire lifetimes to its invocation interval, includes its interface and inherited-control wires during that interval, and applies §8.2 dirty-borrow replacement without charging the same physical wire twice within that view.'
- **C5 4**: The defect is real: §12.1 identifies all scheduled contexts, while §12.3 supplies flat resource maps without selecting a context or aggregation. Full keys, canonical ordering, exact coverage and deterministic projection repair that contract without changing error-bound multiplicities. *Change:* §12.3, clarify the standalone boundary: 'Schedule-free reference claims retain K13's reference-only meaning; a verified standalone resource report binds an effective §11 schedule, including an explicit empty-entries schedule when defaults supply every decision.'
- **C6 4**: The checker obligation is stated and uses existing expansion and scheduling defaults. The proposed negative vectors are derivable. The verification-index script passed, but its resource checks are arithmetic assertions, not execution of the proposed certificate schema; the note accurately discloses this. *Change:* §15 suites E/H, add: 'The two-flip fixture accepts child time/occupancy/peak values (1,1,1) and (1,2,2), root values (2,4,2), and gate counts 1,1,2; omitted, duplicated, reordered, foreign-key or numerically mismatched context records reject.'
- **C7 5**: The repair supports North Star §§4.3–4.4 and §5.1 by making resource reports independently checkable across repeated invocations. It introduces no restriction on controlled calls, budgets or demo-ladder capabilities. No false cited premise or misnumbered clause was found. *Change:* No required change. Preserve the proposed §12.3 rule: 'Error-bound multiplicities remain governed by their existing separate composition rule.'
- **C8 4**: The representation reuses existing context keys rather than inventing another identity system. Migration requires recomputation rather than guessed aggregation. Under the proposed authorized in-version repair, §9.2 excludes certificate bytes from object_hash, and no function, target, schedule or catalog bytes need change. The published 219-recipe catalog envelope hash was independently reproduced. *Change:* §0, add a repair entry stating: 'RESOURCE-CONTEXTS (§12.3; b-isa-spec-cwq): bind resource reports to complete invocation contexts; migrate legacy multi-context certificates by recomputation; object, closure, target, schedule and ref-catalog identities remain unchanged.'

Suggestions:
1. §12.3, document the worked witness's time origin: 'Child timing is measured relative to that invocation's entry while preserving internal delays from the bound schedule.' In the sequential flip example, the second child occupies root time [1,2) but reports time 1.
2. Conformance vectors, publish complete certificate JSON using §10.1 keys. For the single class fast, the uncontrolled child should report peak_qubits[fast]=1, qubit_second[fast]=1, time=1; the controlled child 2,2,1; and the root 2,4,2. Also include a duration-1/3 context with estimate.exact_resources.time=1/3 and resources.time="0.3333333333333333333333333333333334" to exercise exact accounting versus decimal display.

## codex

The repeated-context defect is real, the worked integer costs are correct, and the identity/hash claims hold. One contract blocker remains: reports without estimate need a defined encoding and acceptance rule for exact non-terminating rational costs.

**Path to accept:** Add RC-1’s numeric encoding and comparison rule, then include the duration-1/3 expected values in the conformance vectors. No core, object-identity, schedule or catalog change is needed.

- **C1 5**: The diff changes certificate reporting, leaving §3 state and execution semantics unchanged. *Change:* No change required to §3.
- **C2 5**: The flip example uses valid §4.7 calls. §8.3 permits a native x entry covering total control counts 0 through 1. *Change:* No change required to §4.
- **C3 5**: Charging controlled operations independently of control-wire basis values is correct. Resource views do not modify the existing error-bound composition. *Change:* Retain the proposed §12.3 sentence: 'Error-bound multiplicities remain governed by their existing separate composition rule.'
- **C4 4**: Per-context accounting and independent root aggregation address the real ambiguity. The integer witness is correct, but exact accounting without estimate lacks a rule for non-terminating rational values. *Change:* In §12.3 state: 'Whether or not estimate is present, resources values use §10.1’s canonical 34-significant-digit upward decimal encoding of the independently recomputed exact rational totals.'
- **C5 4**: §12.1 supplies concrete keys and canonical ordering, including default-covered invocations; K77 confirms that budgets can differ within one variant/control-count pair. The remaining encoding problem changes checker verdicts. *Change:* Apply RC-1’s unconditional numeric-encoding rule to both resource_contexts records and their unkeyed projection.
- **C6 4**: The verification script passes and accurately limits its claims to arithmetic and document checks. The proposed negative cases are useful; the missing rational-value case exposes an undecided acceptance condition. *Change:* Add a §15 resource-context vector with native duration 1/3: each child time is exactly 1/3 and displays as '0.3333333333333333333333333333333334', including when estimate is absent.
- **C7 5**: The approach preserves repeated, controlled, default-covered and differently budgeted invocations. No cited clause is misnumbered or misquoted. Under the proposed in-version repair, §9.2 confirms that certificate changes leave object and closure hashes unchanged; the catalog envelope hash also checks. *Change:* Retain complete §12.1 context coverage and the requirement to recompute legacy multi-context reports.
- **C8 4**: The proposal is compact and actionable. Caller ownership versus child footprint reporting would benefit from an explicit sentence; the published controlled-action fixture supports the note’s footprint interpretation. *Change:* Append to §12.3: 'Displaying caller-owned interface and inherited-control wires in a child invocation’s footprint neither transfers ownership nor creates an additional charge.'

Suggestions:
1. §12.3: add 'Child reports include caller-owned interface and inherited-control wires as footprint views during that invocation; they do not create additional charges. Borrower charges replace the owner’s charge during borrowed intervals.' The original flip footprints remain 1 and 2, and root occupancy remains 4. For one wire live over [0,2), borrowed over [0,1), with owner rate 1 and dirty rate 1/4, the combined occupancy is 5/4, not 9/4.
2. §12.3: add 'For a single invocation, resource_contexts may be omitted; if present, it MUST contain exactly one matching record and its projection MUST equal the unkeyed fields. The root invocation’s context_key is [].' This makes optional singleton records subject to the same validation as repeated-context records.
3. Conformance vectors: publish a serialized two-call fixture with derived concrete context keys. Require child (time, occupancy, peak) values (1,1,1) and (1,2,2), root values (2,4,2), and root x count 2; swapping, omitting or duplicating context records must reject.
