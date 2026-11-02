# Council — contract-xv4-2026-11-02 round 2

Document snapshot sha256 ca70501b1bac; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 4 | 5 | 4.5 |  |
| C6 | 5 | 5 | 5.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 5 | 4 | 4.5 |  |

Overall mean: 4.88

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Previous-round blockers, status

- [sol] XV4-B01: **resolved** — Both blanket rules are explicitly replaced by one exclusive classifier; nonempty fixed_regions prevents vacuous qualification, and incompatible proof requests reject.
- [codex] XV4-B01: **resolved** — Both conflicting classification rules are explicitly replaced; full-D proof takes precedence and image-relative proof requires nonempty fixed_regions.

## Blocking issues

- none

## sol

XV4-B01 is resolved. No false cited premise, new S0 issue or regression was found. The finite witness and hashes reproduce, and the mixed fat object remains reachable. Under the stated authorized in-version K repair, §9.2 supports unchanged executable identities; certificate bytes change. The untouched 219-recipe catalog envelope was independently verified.

**Path to accept:** No blocking changes remain. To raise the lowest criterion, C5, from 4 to 5, specify the report binding order and resolved slot identifiers as suggested.

- **C1 5**: ISA §5.2 includes every interface-region cell in D, as claimed. The proposal changes claim classification without changing that domain or the machine. *Change:* §12.2, optional consolidation: state, 'fixed_regions restricts a verification claim only; it does not specialize the executable region or alter its semantics on unrestricted D.'
- **C2 5**: No instruction changes. The image packing agrees with register-to-region binding in ISA §3.3, including non-byte-aligned cells. *Change:* §12.2: add, 'Executable image preparation obeys §10's existing clean-register and ownership requirements.'
- **C3 5**: The proposal retains exact +1 phase, complete tuples, arbitrary targets and fault words, dirty systems and inherited controls. VJ_I = PJ_I extends linearly to arbitrary states of the remaining components and external references. *Change:* Recommended exact spec changes: state, 'With multiple fixed regions, J_I inserts their joint declared basis image and acts identically on every remaining input component.'
- **C4 5**: Conditional correctness explicitly preserves target matching, resource accounting and error composition. Fixing verification inputs does not remove the image storage or preparation cost. *Change:* §12.2: add, 'A fixed_regions binding does not reduce frame widths or remove resource events from the realised schedule.'
- **C5 4**: The exclusive classifier resolves XV4-B01 and preserves existing full-D proofs, ordinary-slice evidence and sampled evidence. Identity resolution, preparation obligations and invocation bindings are clear. The report's stated binding order remains unspecified, a non-semantic serialization choice. *Change:* §12.2: state, 'The checker reports fixed-region bindings in subject interface-region signature order, identifying each by its resolved mem slot rather than its local spelling.'
- **C6 5**: The conditional theorem has sufficient hypotheses and preserves non-permutation process obligations. Independently executed the revised Python witness: both hashes, both 64-tuple relations, all 64 swapped-image failures and both coverage calculations passed. *Change:* Conformance vectors: add, 'A sampled claim whose distinct draws cover all 64 image-slice tuples receives evidence with coverage 64/2^22 = 1/65536; exhaustive replay receives proof_relative_to_image with the same coverage.'
- **C7 5**: North Star §5.1 and §8 rung 4 are cited accurately. The mixed-object section identifies the selected VM closure, host preparation, native entry comparison and untouched native code; bennett-4ht passes. No demo capability is removed. *Change:* Mixed fat object: add, 'The native comparison includes the marked entry's entire materialized callee closure and the prescribed runtime and arithmetic shims, as required by North Star §3.2.'
- **C8 5**: The revised instructions identify both conflicting rules for replacement, distinguish requests from outcomes, preserve K75 and clearly limit verification claims. Stale bindings and fresh image checks are distinguished. *Change:* Conformance vectors: state, 'Omitting a required varying range prevents qualified promotion but may still yield evidence; a malformed domain, stale digest or replay mismatch rejects.'

Suggestions:
1. §12.2: state, 'Resolved fixed-region bindings are reported in subject interface-region signature order using mem slot identities.' This makes reports deterministic without changing verdicts.
2. Mixed fat object: add, 'The native comparison includes the marked entry's entire materialized callee closure and the prescribed runtime and arithmetic shims.' This makes the existing North Star comparison obligation explicit beside the native-libc statement.

## codex

XV4-B01 is resolved. No new S0 issue or false cited premise was found. Witness and catalog checks pass. The hash-preservation claim holds under the expressly conditioned in-version extension, and the mixed fat object remains reachable.

**Path to accept:** Already acceptable. To raise C8 from 4 to 5, explicitly specify the restricted numerical matrix and the reduced-input/full-output Choi construction described above.

- **C1 5**: ISA §5.2 includes every interface-region cell in D. The proposal preserves that domain and changes only certificate classification and applicability. *Change:* No change required.
- **C2 5**: No instruction changes. The image packing agrees with §3.3's register-to-region binding; preparation introduces no unknown-state inspection. *Change:* No change required.
- **C3 5**: The conditional equality VJ_I = PJ_I is sound with the retained exact phase, full-tuple, workspace, borrowed-system and inherited-control obligations. Executable use requires checked preparation. *Change:* No change required.
- **C4 5**: Target matching, resources, schedules and error composition remain unchanged. The catalog check passed: 219 recipes, envelope hash 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. *Change:* No change required.
- **C5 5**: The exclusive §12.2 classifier resolves the previous overlap. Nonempty bindings, resolved identities, requested labels, exact coverage, invocation restrictions and K75 handling are specified. §9.2 supports the conditional unchanged-hash claim. *Change:* No change required.
- **C6 5**: The restricted permutation and process statements have adequate hypotheses. The supplied script passed: both hashes, 64 tuples per image, 64 swapped-image failures, exclusive predicates and exact coverage. *Change:* No change required.
- **C7 5**: The cited ISA and dialect clauses accurately describe current evidence classification. The SQLite ladder remains intact. The mixed-object section supplies selected-closure inventory, image preparation and marked-entry comparison, satisfying the standing reachability check. *Change:* No required change. For clarity in Mixed fat object, add: 'A marked entry's selected VM closure includes its required transitive callees; native host copies may coexist with materialised device variants.'
- **C8 4**: The proposal is implementable and distinguishes verification from execution and publication. The process-comparison paragraph could more explicitly explain how existing square-matrix procedures receive the restricted maps. *Change:* Recommended exact spec changes, process paragraph (§12.1): add, 'For conditional numerical claims, apply the interval Frobenius-bound procedure to (U−V)J_I. For conditional channel claims, form the Choi matrix of (E_real−E_ref) composed with Ad_J_I, using the reduced input dimension and complete output dimension; retain the existing rigorous interval and invocation-context checks.'

Suggestions:
1. Mixed fat object (§§9/10/12): clarify the native-libc wording with: 'VM objects contain the selected marked entries and their required transitive device closures. Code outside those closures remains native; shared callees may have both host and device variants. Native comparison uses the materialised entry and its entire materialised callee closure with the North Star §3.2 runtimes and arithmetic libraries.' Thus an unmarked helper reached by a marked predicate receives a device variant without moving unrelated host calls onto the device.
2. Recommended exact spec changes, process paragraph (§12.1): explicitly adapt the existing numerical procedures to the restricted maps as stated under C8. A useful vector is a fixed image qubit |0⟩, U=Z on that qubit and V=I: ||(U−V)J_0||=0 although ||U−V||=2. This tests that conditional comparison actually uses the preparation isometry.
