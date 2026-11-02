# Council — contract-checker-fault-rate-2026-11-02 round 2

Document snapshot sha256 7a4c4e39e5c6; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 4 | 4 | 4.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 4 | 4 | 4.0 |  |

Overall mean: 4.62

Verdicts: **sol: revise**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: no**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 1 (blocking 1), codex: core 0 / contract 0 (blocking 0)

## Previous-round blockers, status

- [sol] FR-1: **resolved** — Oracle-only applicability and mandatory action nulls remove the undefined action recount; both controlled-action-09 records receive null.
- [sol] CFR-1: **resolved** — Actions have no context arrays or invented F_B, while contained oracle invocations retain their own recount obligations.
- [sol] CFR-2: **resolved** — The revision acknowledges the missing prior exclusion contract, introduces bound replay evidence, and retains every declared tuple in the F_B recount.
- [codex] FR-1: **resolved** — Actions and permutation actions now require null and omit contexts; nested oracle obligations remain separate.
- [codex] CFR-1: **resolved** — The oracle-only applicability rule removes the undefined action F_B calculation, including both controlled-action-09 records.
- [codex] CFR-2: **resolved** — The unsupported inherited-validation premise is withdrawn; new replay obligations retain all 256 reference tuples while counting 64 exclusions separately.

## Blocking issues

- **[sol] CFR-3** (Recommended exact spec changes (§12.3), Exclusion evidence and default validation, final artifact-delivery paragraph; contract): The claim that artifact delivery can use 'existing certificate attachments' is false. ISA 0.9 §9.1 enumerates a closed object/metadata schema and makes unknown sections or fields errors; §12.3 defines no attachments field or transport. The proposal introduces a replay obligation but attributes its delivery mechanism to an existing contract that does not supply it. This is a false existing-coverage premise under convergence rule 1, rather than a request for field-level encoding completeness. *Fix:* Replace that paragraph with: 'ISA 0.9 defines no certificate-attachment transport. This repair introduces a separate checker input bundle containing the certificate and the required content-addressed artifacts. By default, classifier and input-map blobs are supplied outside the ISA object and certificate schemas; artifact_hash and input_map_hash are SHA-256 of their exact raw bytes. The checker verifies those digests before replay. Missing required blobs make the exclusion report unchecked; mismatched digests reject it. Other transports MAY supply the identical addressed bytes.' Existing materialisation, program, native-build and domain binding obligations still apply. Alternatively, explicitly introduce a new certificate attachments member and its default interpretation in §§9.1/12.3; I recommend the external bundle because it avoids another metadata extension. For the synthetic fixture, valid supplied artifacts reproduce undefined_excluded="64"; absent artifacts leave that exclusion report unchecked while the independent F_B recount may still verify faults_by_code={"1":"256"}.

## sol

FR-1, CFR-1 and CFR-2 are resolved. The counting witnesses pass, the mixed fat object stays reachable, and the conditional identity claims hold: §9.2 excludes certificate bytes from object identity, and no target, schedule or catalog bytes change. One new false premise remains: ISA 0.9 has no existing certificate-attachment facility.

**Path to accept:** Replace the unsupported existing-attachments claim with the explicit external-artifact default in CFR-3, or introduce a new attachment contract explicitly. No other blocking change is required.

- **C1 5**: The repair preserves §§5.2 and 14.1 and explicitly makes recounts intrinsic to F_B, independent of inherited control values or root reachability. *Change:* None required; retain: 'The report is not the probability that a root execution reaches a call.'
- **C2 5**: No instruction semantics change. §4.2 assigns one step to each lifted row, so the two-row add/retval witness correctly faults at B=0 and B=1 and succeeds at B=2. *Change:* None required; retain §14.1's rule that the step counter counts executed rows.
- **C3 5**: Oracle-only recounts respect §5.3's absence of action-owned faults. Counting code(F_B), rather than the accumulated fault word, correctly handles arbitrary incoming fault values and preserves the XOR interface. *Change:* None required; retain: 'The final XOR-accumulated fault word is never the predicate for this count.'
- **C4 5**: The repair changes no resource, target-matching or scheduling function. The host-limit rule follows §12.2 and preserves legal domains without substituting partial counts. *Change:* None required; retain: 'If limits prevent a legal recount, report unchecked (host limit), discharging no verified fault-rate obligation.'
- **C5 4**: Invocation binding, complete-context coverage and deterministic projection agree with K13 and §12.1. The new exclusion contract is explicit, but its supporting claim that certificate attachments already exist is false: §§9.1 and 12.3 define no such facility. *Change:* In §12.3's artifact-delivery paragraph, state: 'This repair introduces separate checker inputs containing the required content-addressed artifacts; ISA 0.9 provides no pre-existing certificate-attachment transport.' Supply the external-bundle default described in CFR-3.
- **C6 4**: The finite counting script passes: each short budget produces 256 faults, and the synthetic classifier flags 64 tuples without reducing the recount. Its stated limitation is accurate: it exercises neither the reference interpreter nor a certificate checker. The proposed conformance obligations are otherwise derivable. *Change:* In Conformance vectors and verification, add: 'Publish a serialized two-context fixture with concrete §12.1 context keys: B=1 reports {"1":"256"}, B=2 reports {}, the legacy record equals the first canonical context, and altering that projection rejects the report.'
- **C7 5**: The mixed-fat-object paragraph passes the standing check: only the marked VM closure receives oracle records; native comparison may use a marked-entry thunk with captured state. Full-domain reference validation and separately reported native exclusions preserve North Star §§3.2 and 5.1. *Change:* None required; retain: 'Unmarked host main, argv/envp and libc are not invented oracle records and need no F_B recount.'
- **C8 4**: The recount function, context ordering, projection, exclusion unions and unchecked outcomes are sufficiently precise to implement. Artifact delivery needs the correction in CFR-3; an explicit oracle/non-null typing sentence would also improve the schema. *Change:* In §12.3, add: 'For kind=oracle, verification.fault_rate MUST be a RATE; null is reserved for action and perm_action records.'

Suggestions:
1. In §12.3, make the tagged union explicit: 'For kind=oracle, verification.fault_rate MUST be a RATE; null is reserved for action and perm_action.' A missing oracle recount cannot discharge a verified fault-rate obligation.
2. In Conformance vectors and verification, publish the concrete serialized two-context fixture described under C6. Expected counts are {"1":"256"} at B=1 and {} at B=2; both controlled-action-09 action records use null, and a corrupted legacy projection rejects the requested report.

## codex

FR-1, CFR-1 and CFR-2 are resolved. The binding defect, arithmetic witnesses, context rules and conditional hash-preservation claims check out. The mixed fat object remains reachable. No new S0 issue or regression found.

**Path to accept:** No blocking changes required. To raise C6 from 4 to 5, publish the complete serialized two-context certificate fixture described above, with explicit expected acceptance and mutation-rejection results.

- **C1 5**: The repair changes certificate reporting, leaving the accepted state and step relation unchanged. *Change:* No change required; retain §14.1's executed-row budget semantics.
- **C2 5**: §4.2 charges one step each for add and retval. Independent execution with the available 0.9 interpreter confirms code 1 at B=0 and B=1, and payload (x+1) mod 4 with code 0 at B=2. *Change:* No instruction change required; retain the stated two-row witness and its expected values.
- **C3 5**: Counting code(F_B) follows §5.2, including arbitrary incoming fault words. Oracle-only applicability and action null records correctly respect §5.3. Intrinsic recounts do not inspect or condition reporting on superposed controls. *Change:* No change required; retain: 'The final XOR-accumulated fault word is never the predicate for this count.'
- **C4 5**: K13 invocation encodings preserve §5.4's actual token tuples. No target, resource or expansion semantics change. The catalog envelope independently reproduces 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. *Change:* No change required; retain the unchanged-envelope condition on the hash-preservation claim.
- **C5 4**: The original binding defect is real. Explicit invocations, complete §12.1 contexts, canonical projection and independently replayed exclusion counts repair it. The evidence record's reference_program_hash wording could distinguish the existing interface hash from closure binding more explicitly. *Change:* In Exclusion evidence and default validation, state: 'reference_program_hash uses §9.2's oracle interface hash; the containing region's closure hash and certificate object binding additionally identify the linked reference program whose classifications are replayed.'
- **C6 4**: The supplied script passes. Independent 0.9 run-oracle and exhaustive step-check runs confirm all four x values at B=0,1,2. Certificate rejection vectors are specified, but complete serialized multi-context and classifier fixtures remain future conformance work, accurately disclosed. *Change:* In Conformance vectors, add a complete two-call certificate fixture with canonical context keys, domains and legacy projection: the B=1 record reports {"1":"256"}, the B=2 record reports {}, and deleting either context or altering the projection rejects.
- **C7 5**: The repair preserves North Star §§3.2/5.1 reference validation for excluded inputs, action support and zero-fault acceptance checks. The bennett-4ht paragraph explicitly preserves native host code, marked VM closures, comparison thunks and process-local handles. *Change:* No scope change required; retain the explicit statement that unmarked host main, argv/envp and libc need no invented oracle recounts.
- **C8 4**: Applicability, count encodings, context ordering, host-limit outcomes and migration are actionable. §9.2 confirms certificate changes do not affect object-hash inputs; an in-memory null conversion of the controlled-action fixture verifies this. Artifact transport has a default, but its description should avoid implying an already standardized attachment container. *Change:* In Exclusion evidence and default validation, replace 'existing certificate attachments' with: 'The default transport is SHA-256-addressed sidecar artifacts accompanying the certificate, outside §9.1 object metadata; unavailable artifacts leave the exclusion report unchecked.'

Suggestions:
1. In Mixed fat object, clarify the two-launch example: 'Separate host launches under B=1 and B=2 use separate root schedule/certificate bindings. fault_rate_contexts enumerates calls within one bound root schedule; a device action wrapper containing both calls instead supplies two contexts in that schedule.' The respective full-domain fault maps remain {"1":"256"} and {}.
2. In Exclusion evidence and default validation, identify the attachment transport as the new sidecar default stated under C8. §§9.1/12.3 do not currently define a certificate attachment container; this is transport clarification, not a missing recount obligation.
3. In Round-1 blocking items and resolution, change 'astra CFR-1' and 'astra CFR-2' to 'codex CFR-1' and 'codex CFR-2', matching the supplied previous-round outputs.
