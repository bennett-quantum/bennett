# Council — contract-checker-fault-rate-2026-11-02 round 3

Document snapshot sha256 71a74c494872; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 5 | 5 | 5.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 5 | 5 | 5.0 |  |

Overall mean: 4.88

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Previous-round blockers, status

- [sol] CFR-3: **resolved** — The nonexistent existing-attachments premise is withdrawn. The new external bundle defines raw-byte SHA-256 checks, missing-blob unchecked outcomes and digest-mismatch rejection; the finite witness passes.
- [codex] CFR-3: **resolved** — The unsupported existing-attachments premise is replaced by an explicit external checker bundle with raw-byte SHA-256 validation; supplied, missing and altered blob cases reproduce the specified outcomes.

## Blocking issues

- none

## sol

CFR-3 is resolved. The defect statement, clause references, recount arithmetic and conditional hash-preservation claims check out. The mixed fat object remains reachable. No new S0 issue or regression found.

**Path to accept:** No blocking changes remain. To raise C6 from 4 to 5, publish the serialized two-context certificate and its acceptance/rejection vectors described above.

- **C1 5**: The repair leaves the accepted machine model unchanged. Intrinsic recounts follow §§5.2/14.1 and do not depend on inherited predicates or root reachability. *Change:* No change required; retain in §12.3: "The report is not the probability that a root execution reaches a call."
- **C2 5**: §4.2 charges one step per lifted row. The interpreter witness confirms faults at B=0/1 and payload (x+1) mod 4 at B=2. *Change:* No change required; retain the two-row example with faults_by_code={"1":"256"} at B=0/1 and {} at B=2.
- **C3 5**: Counting code(F_B), rather than the accumulated fault word, respects §5.2's XOR interface. Mandatory action nulls correctly implement §5.3's absence of action-owned faults. *Change:* No change required; retain in §12.3: "The final XOR-accumulated fault word is never the predicate for this count."
- **C4 5**: Actual args and validated four-component token tuples remain authoritative. The host-limit outcome follows §12.2 without changing resource, target or scheduling semantics. *Change:* No change required; retain in §12.3: "If limits prevent a legal recount, report unchecked (host limit), discharging no verified fault-rate obligation."
- **C5 5**: The binding defect exists in published §12.3. Independent RATE bindings, complete §12.1 contexts and the deterministic projection repair it. The external bundle explicitly supplies the new artifact contract without violating §9.1's closed schema. *Change:* No change required; retain in §12.3: "This bundle is a new checker input contract; it adds no attachments field to either closed schema."
- **C6 4**: Read-only runs of the inline script and check_rev4.py pass, including actual commit/reversal, 64 exclusions and artifact rejection paths. The absence of a complete serialized multi-context certificate is accurately disclosed. *Change:* In Conformance vectors and verification, publish: "A serialized two-call certificate with concrete §12.1 keys reports {\"1\":\"256\"} for B=1 and {} for B=2; its legacy RATE equals the first canonical context with context_key removed. Deleting either context or altering that projection rejects the report."
- **C7 5**: All declared tuples remain in reference validation, while native exclusions remain separately reported. The mixed-fat-object statement preserves marked device closures, native host execution and comparison thunks, and names the remaining launch and host-memory obligations. *Change:* No change required; retain in Mixed fat object: "Unmarked host main, argv/envp and libc are not invented oracle records and need no F_B recount."
- **C8 5**: Applicability, encodings, context ordering, exclusion unions and unchecked/rejection outcomes are implementable. §9.2 confirms the conditional identity claims; an independent in-memory action-null conversion preserves object_hash and schedule bytes, and the ref catalog pin reproduces. *Change:* No change required; retain in Hashes, publication and consumers: "A full-version publication instead requires regenerating version-envelope identities and dependent pins."

Suggestions:
1. In Conformance vectors and verification, add the complete serialized two-context fixture specified under C6. State its expected verdicts explicitly: B=1 reports {"1":"256"}, B=2 reports {}, the legacy projection matches the first canonical context, and omitted contexts or a corrupted projection reject.

## codex

CFR-3 is resolved. The cited defect, counting rules, external-artifact contract and conditional identity claims check out. Certificate bytes change; with unchanged version envelopes, object, symbol, target, schedule and catalog identities remain unchanged. The mixed fat object stays reachable. No new S0 issue, false technical premise or regression found.

**Path to accept:** No blocking changes required. Publishing the complete serialized multi-context fixture and its rejection mutations would raise C6 from 4 to 5.

- **C1 5**: The repair preserves §§5.2/14.1's machine and F_B semantics. Recounts explicitly measure intrinsic oracle outcomes rather than call reachability. *Change:* No change required. In §12.3, retain: 'The report is not the probability that a root execution reaches a call.'
- **C2 5**: §4.2 charges one step per lifted row. The add/retval example correctly faults at B=0 and B=1 and succeeds at B=2; the executable witness confirms this. *Change:* No change required. Retain the two-row example: 256 code-1 faults at each short budget, and zero faults with payload (x+1) mod 4 at B=2.
- **C3 5**: Counting code(F_B) respects §5.2's XOR interface for arbitrary incoming fault words. Mandatory action nulls respect §5.3, while contained oracle obligations remain intact. Recounting excludes inherited controls without conditioning on their basis values. *Change:* No change required. In §12.3, retain: 'The final XOR-accumulated fault word is never the predicate for this count.'
- **C4 5**: Exact four-component budgets and nested token tuples follow K13 and §5.4. Host-limit handling agrees with §12.2. Resource, target and expansion semantics are unchanged; the published 219-recipe catalog hash reproduces. *Change:* No change required. Retain the unchanged-version-envelope qualification in 'Hashes, publication and consumers'.
- **C5 5**: The original invocation-binding defect is real. Complete §12.1 contexts, canonical legacy projection and independent exclusion replay repair it. The external bundle now explicitly introduces transport outside §9.1's closed schemas. Reference interface and closure bindings correctly follow §9.2. *Change:* No change required. In §12.3, retain: 'Missing required blobs make the exclusion report unchecked; mismatched digests reject it.'
- **C6 4**: check_rev4.py passed using the available compiled interpreter and machine witness: 768 interface tuples, fault counts 256/256/0, commit checks and complete machine reversal. Exclusion replay reproduced 64 flags and the stated negative outcomes. Complete serialized multi-context conformance remains unimplemented and accurately disclosed; no fresh build was performed. *Change:* In 'Conformance vectors and verification', add and fulfill: 'Publish a complete serialized two-call certificate with concrete §12.1 context keys: B=1 reports {"1":"256"}, B=2 reports {}, and the legacy RATE equals the first canonical context with context_key removed; deleting either context or corrupting the projection rejects.'
- **C7 5**: Full-domain reference recounts and separate native exclusions preserve North Star §§3.2/5.1. The bennett-4ht standing check passes: certificates cover marked device closures, comparison thunks select the corresponding native entry, and the incorporated statement names remaining launch and host-memory obligations. *Change:* No change required. Retain: 'Unmarked host main, argv/envp and libc are not invented oracle records and need no F_B recount.'
- **C8 5**: Applicability, invocation encoding, context ordering, projection, category unions and checked/unchecked/rejected outcomes are actionable. Migration rejects unbound recounts. An in-memory conversion of both controlled-action certificate records to null changed certificate bytes while preserving object identity and schedule/target pins. *Change:* No change required. In §12.3, retain: 'For kind=oracle, verification.fault_rate MUST be a RATE; null is reserved for action and perm_action records.'

Suggestions:
1. In 'Conformance vectors and verification', add and fulfill: 'Publish a complete serialized two-call certificate with concrete §12.1 context keys, full domains and the canonical legacy projection.' Expected fault maps are {"1":"256"} at B=1 and {} at B=2; deleting, duplicating or reordering contexts, or altering the projection, rejects. This is publication evidence, not a missing semantic decision.
