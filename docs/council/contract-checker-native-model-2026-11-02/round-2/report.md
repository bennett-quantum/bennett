# Council — contract-checker-native-model-2026-11-02 round 2

Document snapshot sha256 bf6d0139ab96; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 4 | 4 | 4.0 |  |
| C5 | 5 | 5 | 5.0 |  |
| C6 | 5 | 4 | 4.5 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 4 | 4 | 4.0 |  |

Overall mean: 4.69

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Previous-round blockers, status

- [sol] sol:B1: **resolved** — Per-context evaluated epsilon consistently governs omission: 1−1 remains exact, while epsilon=c requires a model for independent verification only in positive contexts.
- [sol] codex:B1: **resolved** — The expression-syntax MUST has been removed; exact zero-valued expressions receive the exact-opcode convention without a missing-model diagnostic.
- [sol] codex:B2: **resolved** — Native models remain logical unitaries with operator-norm epsilon; Kraus/instrument representations require phase-bearing U and reduced-map equivalence, and cannot replace controlled numerical claims.
- [codex] sol:B1: **resolved** — Requirements now follow evaluated epsilon: 1−1 remains exact without a model, and epsilon=c distinguishes c=0 from positive contexts.
- [codex] codex:B1: **resolved** — The expression-syntax requirement and exact-entry exemption no longer conflict.
- [codex] codex:B2: **resolved** — Native models must bind a phase-bearing unitary; genuinely nonunitary Kraus maps are excluded, and controlled numerical claims retain §12.3’s obligation.

## Blocking issues

- none

## sol

All three previous blockers—sol B1, codex B1 and codex B2—are resolved. No new S0 issue or regression was found. The cited clauses, phase witnesses, numerical acceptance claims and hash migration are sound. The mixed fat object remains reachable. Clarify the nonblocking “squared operators” wording.

**Path to accept:** Already acceptable; no blocking changes remain. To raise the lowest-scoring criteria C4/C8 from 4 to 5, publish the format-1 encoding table, including the operand permutation and constant/variable node spellings.

- **C1 5**: The amendment supplies target realisation data without changing §§3–7's state, tiers or step relation. *Change:* No required change. Optional §8.3 clarification: “Native models describe target realisations; they do not replace the reference machine semantics.”
- **C2 5**: The unitary-only admission rule preserves §4.4's phase-fixed matrices, operator-norm epsilon and exact permutation requirements. Angle bindings correctly cite §3.1 and §11.1 K20. *Change:* No required change. Preserve the stated rule: “A supplied model MUST agree with the exact §4.4 operation in every zero-epsilon context.”
- **C3 5**: The controlled X/−X witness is correct. Kraus representations must reduce to an explicitly phase-bearing unitary in every control context, preventing the round-1 channel admission error. *Change:* In “Alternatives and concrete witnesses”, replace “Their squared operators sum to identity” with “K0†K0 + K1†K1 = I.” Literal operator squares instead sum to zero for this example.
- **C4 4**: Evaluated-epsilon requirements agree with §8.1 and §17 item 9. Matching, cost and error charging remain intact. The operand permutation obligation is clear, but its serialized representation remains publication work. *Change:* In §8.3's version-1 schema, publish the permutation encoding and state: “operand_map[j] is the allocation-basis position of model operand j.” Example: model order [own_control, inherited_control, target] mapped to [inherited_control, own_control, target] uses [1,0,2].
- **C5 5**: The defect is real: §8.3 does not identify approximate native operators, while §12.1 requires realised-operation reconstruction. Migration preserves exact contexts and prevents missing models from discharging affected obligations. Hash migration agrees with §§8.1, 9.2 and 11. *Change:* No required change. Retain: “Model bytes change target_hash and require regenerating every dependent schedule_hash and certificate binding.”
- **C6 5**: The exact witness script passes. Operator distance 2, Frobenius bound 2√2 and rejection of zero-bound channel witnesses agree with §12.1. The independent catalog check confirms 219 recipes and hash 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. *Change:* Optional §15 suite D addition: “Controlled X versus controlled −X rejects numerical bound 2 and can pass bound 3 at sufficient precision; controlled X versus itself can pass numerical bound 0.”
- **C7 5**: Approximate algorithms remain supported, and logical epsilon remains separate from stochastic hardware failure. The mixed-object paragraph passes bennett-4ht: native host execution, selected VM closure, launch bindings and closure-scoped certificates remain reachable. *Change:* Optional clarification in the mixed-object paragraph: “The selected VM closure includes the transitive callees required by each marked entry, including callees whose source contains no marker.”
- **C8 4**: The versioned format, concrete X matrix, reconstruction obligations and unchecked migration outcomes are implementable. Constant and variable node spellings need a compact encoding table; these are S1 publication details under the stated exact-expression default. *Change:* In §8.3's format-1 encoding table, state: “Variables use {var:name}; constants pi and i use {op:name,args:[]}; function applications use {op:name,args:[...]}; rational leaves use the published reduced decimal-string pair.”

Suggestions:
1. In “Alternatives and concrete witnesses”, write “K0†K0 + K1†K1 = I” instead of “Their squared operators sum to identity.” For the displayed operators, K0² + K1² = 0; the script correctly checks the adjoint products.
2. In §8.3, publish the format-1 expression-node and operand-map encodings while retaining the exact reconstruction default. State: “operand_map[j] gives model operand j's allocation-basis position”; the own-control/inherited-control swap example should encode [1,0,2].
3. In the mixed-object paragraph, add: “The selected VM closure includes transitive callees of marked entries, whether or not those callees contain markers; native comparison materializes that same callee closure with the prescribed runtime and arithmetic libraries.” This makes the existing closure obligation explicit.

## codex

sol B1, codex B1 and codex B2 are resolved. The defect is genuine, the cited operative clauses are correctly identified, and no new S0 issue or mixed-fat-object narrowing remains. Exact witnesses and hash checks passed; the catalog check confirmed the unchanged 219-recipe envelope. Native-model checker execution remains unclaimed.

**Path to accept:** No blocking changes are required. To raise C6 from 4 to 5, replace the misleading Kraus “squared operators” sentence with the explicit adjoint-product normalization above.

- **C1 5**: The extension describes target realisations without changing §3’s state, tiers or step relation. *Change:* Optional clarification in §8.3: “Realisation models describe target implementations; §§3–7 continue to define reference execution.”
- **C2 5**: The revised unitary-only admission rule preserves §4.4’s phase-fixed matrices and operator-norm accuracy contract. The angle references to §3.1 and §11.1 K20 are correct. *Change:* Optional clarification in §8.3: “The existing requirements for epsilon-zero gates in oracles and permutation actions, and the prohibition of relative-phase ccx, remain unchanged.”
- **C3 5**: The X/−X interference witness is correct. Requiring a phase-bearing U and its actual controlled implementation prevents channel equivalence from erasing observable controlled phase. *Change:* Optional clarification in §8.3: “Unitary comparison uses the supplied phase and MUST NOT minimise the distance over an overall phase.”
- **C4 4**: Evaluated epsilon, shared k/c/eps bindings, exact angles and control-context reconstruction are decided. Detailed encodings beyond the concrete controlled_U example remain implementation work, with a matrix/expression default provided. *Change:* In §8.3 add this encoding example: “For cx with own control a and inherited control q, k=1 and c=2; controlled_U uses base basis [t], adds both controls, and maps entry order [a,q,t] to checker order [q,a,t].”
- **C5 5**: The missing-operator defect is real under §§8.3 and 12.1. Migration preserves execution compatibility without permitting unsupported independent claims. In-memory checks confirmed model-dependent target and schedule hashes; §9.2 supports unchanged source identities under the stated unchanged-envelope condition. *Change:* Optional clarification in Migration: “Changing realisation_model bytes invalidates cached verification results bound to the former target_hash or any dependent schedule_hash.”
- **C6 4**: The supplied exact script passed. The operator distance 2, Frobenius bound 2√2, diamond distance 2 and strict-positive-pivot observations agree with §12.1. However, “Their squared operators sum to identity” is literally false: the ordinary squares sum to zero; the script correctly checks adjoint-products. *Change:* In Alternatives and concrete witnesses replace that sentence with: “K0†K0 + K1†K1 = I, so the Kraus map is trace preserving.” For these operators, K0² + K1² = 0.
- **C7 5**: Approximate algorithms remain available, and unchecked legacy handling does not replace the model mechanism. The bennett-4ht paragraph explicitly scopes models and certificates to selected VM closures while retaining native main, argv/envp and ordinary host code. *Change:* Optional clarification in Mixed fat object: “Selected VM modules include their required device callee closures; untainted host code remains native.”
- **C8 4**: The proposal is implementable at this review stage: it supplies a model version, concrete X representation, reconstruction obligations and default evaluation behavior. Complete interchange fixtures would make the remaining encoding work easier to implement consistently. *Change:* In Conformance vectors add: “Publish a complete canonical target containing the displayed X model and a bound schedule; at c=1 its reconstructed matrix is diag(I2,X), and adding the model changes target_hash and the dependent schedule_hash.”

Suggestions:
1. Alternatives and concrete witnesses: replace “Their squared operators sum to identity” with “K0†K0 + K1†K1 = I.” Ordinary squares instead give K0² + K1² = 0. This is a wording correction because the normative admission rule and executable witness already use the correct normalization.
2. §8.3 representation examples: state, “For cx with own control a and inherited control q, controlled_U uses base basis [t] and c=2; entry order [a,q,t] maps to checker order [q,a,t].” This illustrates the already-required permutation without adding a new semantic obligation.
3. Conformance vectors: add a complete canonical X-model target and bound schedule. State, “At c=1 the model reconstructs diag(I2,X); adding model bytes changes target_hash and the dependent schedule_hash, while unchanged source-object bytes retain their §9.2 identities.” Keep this fixture distinct from a claim that a native-model checker has already been implemented.
