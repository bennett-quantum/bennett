# Council — pass2-v2v-2026-11-02 round 1

Document snapshot sha256 31ffa07d499a; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 4 | 4 | 4.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 4 | 4 | 4.0 |  |
| C8 | 4 | 4 | 4.0 |  |

Overall mean: 4.5

Verdicts: **sol: revise**, **codex: revise**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: no**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 1 (blocking 1), codex: core 0 / contract 1 (blocking 1)

## Blocking issues

- **[sol] V2V-1** (Recommended exact spec diff, §12.3; Hashes, catalog and consumers; contract): The proposal changes certificate layout and frame inventory but never states how those records apply within the mixed fat object required by North Star §§2, 3.3 and 4.4. INDEX's general assertion that no capability is removed does not identify the device-root boundary, distinguish it from the native executable entry, or delimit the certificate inventory. This fails the council's explicit bennett-4ht standing check, which requires revise for silence on this boundary. The context mechanism itself otherwise preserves the required capability. *Fix:* Append to §12.3: 'In a mixed fat object containing native host code and marked device ISA modules, frame and frame_contexts coverage is scoped to the certificate's bound scheduled ISA root and its complete linked device-region invocation tree. The native host invokes device computation through §10's device CC entry and launch shim. The context key [] identifies the bound scheduled device-region root, not the native executable entry. Native host functions, process argv/envp and host libc are outside this frame inventory; marking a region does not require lowering the whole native executable. Native comparison uses the corresponding materialised region and its materialised callee closure under the recorded comparison configuration.' This permits the pair/flip device root to use [] while the enclosing native main has no frame-context entry.
- **[codex] V2V-1** (Recommended exact spec diff (§12.3); mixed-fat-object compatibility; contract): This changes certificate layout but supplies no mixed-fat-object integration statement. Neither the diff nor INDEX specifies that context inventories are scoped to device roots rather than the native host binary. This fails the explicit standing C7 check, which requires that statement for certificate-layout changes. Preserving nested region calls alone does not discharge it. *Fix:* Append to §12.3: 'For a mixed fat object, these frame records describe only the linked ISA regions in a bound device-root realisation. Each scheduled device root has its own certificate bindings and context set; [] is relative to that root. The native host component invokes device code through §10, using a device CC entry where required. Native host functions need no frame records, and this inventory does not require unmarked host code to be lowered to ISA. Certificates for different roots may reference the same linked closure, but their frame contexts remain scoped to their respective root bindings.' Alternatively place this rule in a shared normative mixed-object clause and explicitly incorporate it here; prefer the local paragraph.

## sol

The frame defect is real and the proposed context-indexed repair is technically sound. Basis results, resource arithmetic and catalog claims check out. One contract blocker remains: explicitly preserve the mixed native/device fat-object boundary.

**Path to accept:** Add V2V-1's mixed-fat-object applicability paragraph to the proposed §12.3 diff. No other blocking change is required; the context-selection mechanism, worked values and conditional hash claims are sound.

- **C1 5**: The diff changes certificate frame selection without changing §3 machine state or the step relation. *Change:* §12.3, optional clarification: 'Frame-context records introduce no additional machine state.'
- **C2 5**: The pair/flip source uses valid §4.7 action calls. Existing source points distinguish the calls; no instruction or semantic call edge changes. *Change:* §12.3, optional clarification: 'Selecting a frame descriptor introduces no instruction, semantic call or generated leaf.'
- **C3 5**: Selection uses resolved invocation data. Caller-owned controls remain separate, and distinct dynamic identities plus existing disjointness obligations prevent identical descriptors from implicitly authorizing storage sharing. *Change:* §12.3, optional clarification: 'Frame selection and validation do not depend on whether a quantum predicate is true on a particular basis input.'
- **C4 5**: §9.4 requires concrete classes and budget/parameter instantiation before forming c-only widths. The proposed selector handles both differences correctly. Independently checked pair costs are time=2, occupancy[A]=occupancy[B]=2 and peak[A]=peak[B]=1 under the stated sequential unit-duration schedule. *Change:* §12.3, optional clarification: 'A uniform frame must also have valid allocation ordering, scheme identities and live_ranges in every covered context.'
- **C5 4**: The defect exists: §12.3 has one closure-keyed record with one required B5 frame. Exact context coverage, canonical ordering and uniform shorthand repair it. The remaining blocker is the missing explicit mixed-fat-object boundary. *Change:* §12.3: add the mixed-fat-object applicability paragraph specified in V2V-1.
- **C6 4**: All four basis outputs and inverse restoration check out. The sibling test actually expects Unsupported, as disclosed. INDEX's arithmetic assertions do not exercise the proposed certificate schema; the note accurately limits its verification claim. *Change:* §15 suites F/H: 'The pair/flip fixture accepts entry:0 with class A and entry:1 with class B; omitted, duplicate, foreign, reordered or class-swapped frame-context records reject.' Publish the complete serialized fixture with those expected verdicts.
- **C7 4**: The repair preserves nested calls and target-dependent placement, supporting North Star §§4.2, 4.4 and 5.1. No false cited premise or misnumbered clause was found. Neither the note nor INDEX explicitly addresses the mandatory bennett-4ht mixed-fat-object check. *Change:* §12.3: state explicitly that frame coverage concerns marked device ISA regions and their linked closures within a mixed native/device fat object, as specified in V2V-1.
- **C8 4**: The encoding is compact and implementable using existing context identities. Under INDEX's authorized in-version route, §9.2 confirms that certificate changes leave source envelopes and object_hash unchanged. The 219-recipe catalog check reproduced envelope hash 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. *Change:* Hashes, catalog and consumers: 'Unchanged-hash claims assume the authorized in-version publication route described in INDEX; changing an object-header version changes object_hash, and changing the ISA envelope version requires recomputing affected symbol hashes and consumer pins.'

Suggestions:
1. §12.3: add 'Every supplied frame_contexts array is validated even when the region has only one invocation; it then contains exactly one matching record.' For a root-only fixture that record has context_key:[]. The existing exactly-one-of rule still prohibits simultaneously supplying frame.
2. §15 suites F/H: add 'Complete invocation-tree coverage includes predicated-off calls and calls covered entirely by schedule defaults.' In a fixture containing two statically realised flip calls, disabling one quantum predicate still requires both context descriptors; predicate values do not remove frame requirements.
3. Release and route: add 'Publish the certificate encoding decision before migrating consumers; consumers supporting this repair accept truthful legacy uniform frames and the new context-indexed form. Legacy consumers require an update before verifying certificates that need context-indexed frames.' Retain INDEX's explicit publication-route caveat.

## codex

The defect, cited premises, witness arithmetic and conditional hash claims check out. The context-indexed repair is sound. One contract blocker remains: explicitly preserve mixed-fat-object packaging and scope frame inventories to device roots.

**Path to accept:** Add V2V-1's normative device-root/mixed-fat-object scoping paragraph. No other blocking change is required; retain the proposed frame selection, complete context coverage and uniform shorthand.

- **C1 5**: The diff selects certificate metadata using the existing §12.1 invocation tree. It changes neither machine state nor the step relation. *Change:* Optional §12.3 clarification: 'Frame-context selection changes certificate interpretation only; the machine state and step relation remain unchanged.'
- **C2 5**: No instruction or call edge changes. §11/K63 already distinguishes the pair witness's two source call points, including their instance and call_index components. *Change:* Retain the consumer rule: 'Context keys identify existing invocation edges; this repair introduces no new instruction or call edge.'
- **C3 5**: The proposed descriptor selection preserves §9.4 ownership, dynamic allocation identity and live-range obligations. It neither shares storage implicitly nor changes coherent execution or cleanup. *Change:* Retain §12.3's proposed sentence: 'Inherited controls remain caller-owned and separate from callee slots.'
- **C4 5**: The defect is real: §9.4 requires resolved classes and c-only width expressions, while §12.3 provides one frame per closure. The A/B witness is legal under §§8.3 and 11. Its sequential time, occupancy and peak values are correct. *Change:* Conformance vectors: state the exact resource keys: 'time=2, qubit_second[A]=qubit_second[B]=2, and peak_qubits[A]=peak_qubits[B]=1.'
- **C5 4**: Exactly-one representation, complete context coverage, canonical ordering and per-context validation repair the frame ambiguity. INDEX correctly aligns context identities across reports. The required mixed-fat-object certificate scope is unstated. *Change:* §12.3: 'In a mixed fat object, frame contexts belong to each bound device-root certificate; native host functions are outside this frame inventory.'
- **C6 4**: The checker obligation and negative vectors are derivable. Using the prebuilt reference interpreter, I verified all four pair outputs and four adjoint restorations. The INDEX frame/resource arithmetic passes; neither exercise implements the proposed certificate schema. *Change:* Conformance vectors/§15 F,H: 'The pair call at entry:0 selects class A and entry:1 selects class B, both width 1; swapping their classes rejects even though the program outputs remain correct.'
- **C7 4**: Repeated mixed-class calls remain admissible, consistent with North Star §§4.2 and 4.4. No cited clause is misquoted or misnumbered. However, neither v2v nor INDEX explicitly explains how the certificate change supports the required mixed native-host/device object. *Change:* §12.3: 'A native host binary may package these certificates with only its marked modules lowered to ISA, using the existing §10 device CC launch path.'
- **C8 4**: The representation is implementable using existing invocation identities and B5 descriptors. Under the authorized in-version route, §9.2 excludes certificate metadata from object_hash and symbol envelopes. No catalog bytes change; the published 219-recipe envelope hash independently reproduces. *Change:* Release and route: 'Legacy uniform frames remain valid after validation against every covered context; nonuniform legacy certificates must be regenerated, and consumers must support frame_contexts before claiming this repair.'

Suggestions:
1. Conformance vectors: publish a serialized pair/flip frame_contexts example. With H_pair denoting the pair closure hash, use keys [{symbol:H_pair,point:"entry:0",iteration:[],instance:[],call_index:0}] and [{symbol:H_pair,point:"entry:1",iteration:[],instance:[],call_index:0}], selecting mut:0/class A/width 1 and mut:0/class B/width 1 respectively. Include all five required B5 arrays. State: 'A default-covered call requires its record even when entries is empty; replacing the second class by A rejects.'
2. Release and route: record the requested compatibility decision explicitly: 'This is a council-authorized 0.9 K certificate repair with unchanged source/version envelopes. Existing uniform frame records retain their encoding and undergo all-context validation. Producers regenerate nonuniform certificates; consumers must not discard frame_contexts or substitute its first descriptor for the complete array.' This makes migration concrete without changing the ref@0.9 catalog.
