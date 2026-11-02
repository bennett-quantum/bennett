# Council — pass2-v2v-2026-11-02 round 2

Document snapshot sha256 22c2f9c63a09; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 5 | 5 | 5.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 4 | 5 | 4.5 |  |

Overall mean: 4.81

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Previous-round blockers, status

- [sol] sol:V2V-1: **resolved** — The proposed §12.3 paragraph supplies device-root inventory scope, native-host exclusions, root-relative [] and materialised-closure comparison scope.
- [sol] codex:V2V-1: **resolved** — Separate bindings and context sets per device root are explicit; shared closures do not merge inventories, and unmarked native code requires no frames.
- [codex] sol V2V-1: **resolved** — The proposed §12.3 paragraph explicitly scopes frames to each scheduled device root and its linked invocation tree, with native comparison and host exclusions.
- [codex] codex V2V-1: **resolved** — Separate object/root bindings and root-relative context sets preserve mixed native/device packaging without requiring whole-binary lowering.

## Blocking issues

- none

## sol

Accept the proposed repair. The frame defect, context mechanism, witness arithmetic and conditional hash claims check out. Both sol V2V-1 and codex V2V-1 are resolved; no new S0 issue or regression was found. Acceptance covers the proposal, not completed consumer or mixed-launch implementation.

**Path to accept:** No blocking changes remain. To raise C6 from 4 to 5, publish the bound serialized frame-context fixture and explicit accept/reject expectations described above.

- **C1 5**: The diff selects certificate descriptors using §12.1’s existing invocation tree. It changes neither §3 machine state nor the step relation. *Change:* Optional §12.3 clarification: 'Frame selection introduces no machine state or reference-interpreter step.'
- **C2 5**: The pair/flip calls conform to §4.7. Existing §11/K63 source points and call_index values distinguish both invocations without new instructions or call edges. *Change:* Optional §12.3 clarification: 'Frame-context records identify existing invocations and introduce no source instruction, semantic call or generated ordinal.'
- **C3 5**: Selection uses classical invocation data and explicitly excludes quantum-predicate inspection. Caller-owned controls, dynamic identities and §9.4 disjointness obligations remain intact. *Change:* §15 F/H: 'Setting a realised call’s quantum predicate to zero does not permit omitting its frame-context record.'
- **C4 5**: The defect is real: §9.4 requires resolved classes and c-only widths, while §12.3 requires one closure-keyed frame. Sequential unit-duration pair costs are correctly time=2, occupancy[A]=occupancy[B]=2 and peaks 1 each. *Change:* Worked witness: 'The root reports time=2, qubit_second[A]=qubit_second[B]=2 and peak_qubits[A]=peak_qubits[B]=1.'
- **C5 5**: Exactly-one representation, complete context coverage, canonical ordering and per-invocation validation repair the ambiguity. INDEX and the coordinated resource/fault proposals use the same context vocabulary. The new paragraph scopes inventories to device roots. *Change:* Optional §12.3 clarification: 'Each frame_contexts key must resolve to an invocation of the containing region record’s closure in this certificate’s bound root tree.'
- **C6 4**: Checker obligations and negative verdicts are derivable. check_rev2.py passed all eight result lines. Independent reference-interpreter runs confirmed four pair outputs and four inverse restorations; these checks do not validate the proposed certificate format. *Change:* §15 F/H: publish a bound frame-context fixture stating 'entry:0 selects A and entry:1 selects B; exchanging these classes rejects even though the source execution still returns the correct values.'
- **C7 5**: Both round-1 mixed-fat-object blockers are resolved. The proposed §12.3 paragraph distinguishes scheduled device roots from native entry, preserves separate root-relative contexts and scopes native comparison correctly. The incorporated statement accurately identifies remaining launch and memory-boundary work. No false cited premise or misnumbered clause was found. *Change:* At publication, include the incorporated boundary obligations alongside §12.3: 'Remaining mixed-launch contract work does not require whole-binary ISA lowering or remove mixed execution from scope.'
- **C8 4**: The representation is implementable using existing B5 descriptors and invocation identities. Under the expressly conditional in-version route, §9.2 excludes certificate metadata from object_hash and symbol envelopes. No recipe changes are required; the catalog check reproduced the published 219-recipe envelope hash. Full-version migration is correctly distinguished. *Change:* Hashes, catalog and consumers: 'Consumers validate legacy frame descriptors against every covered context; nonuniform legacy certificates must be regenerated, and consumers must support frame_contexts before accepting its certificates.'

Suggestions:
1. Conformance vectors/§15 F,H: publish the serialized pair/flip frame-context fixture with H_pair=b98f9111e8533f00a8e5ac195e1b335678d14efcabb653d754d9999e21297c16, entry:0 selecting mut:0/class A/width 1 and entry:1 selecting class B/width 1. State: 'The correct ordered array accepts; swapped classes, reversed array order, duplicate keys and omission of either default-covered call reject.' Include all five B5 arrays.
2. Hashes, catalog and consumers: add 'Truthful legacy uniform frames retain their encoding and undergo all-context validation. Producers regenerate nonuniform certificates; consumers must not discard frame_contexts or substitute its first descriptor for the complete array.' Retain the explicit publication-authorization caveat.

## codex

Both round-1 V2V-1 findings are resolved. The defect, clause references, context keys, witness arithmetic and conditional hash claims check out. No false premise, misnumbered citation, regression or new S0 issue was found. Accept the proposed repair; consumer implementation and publication authorization remain separate.

**Path to accept:** No blocking changes remain. To raise C6 from 4 to 5, publish the fully bound serialized pair/flip fixture and its explicit accept/reject mutations, including canonical ordering, class swapping and separate-root coverage.

- **C1 5**: The diff selects certificate metadata through the existing §12.1 invocation tree without changing §3 machine state or execution. *Change:* Optional §12.3 clarification: 'Frame-context selection introduces no additional machine state.'
- **C2 5**: The witness uses valid §4.7 action calls. §11/K63 already distinguishes entry:0 and entry:1, each with instance:[] and call_index:0. *Change:* Retain in 'Hashes, catalog and consumers': 'Existing schedules already distinguish the two source call points; no new call edge is invented.'
- **C3 5**: Selection never inspects quantum predicates. Predicated-off calls retain coverage, inherited controls remain caller-owned, and §9.4 allocation identity, lifetime and disjointness obligations remain intact. *Change:* Retain the proposed §12.3 rule: 'Identical descriptor bytes do not authorize shared physical storage; §9.4’s live-range and disjointness rules remain required.'
- **C4 5**: The defect is genuine: §9.4 requires concrete classes and c-only width expressions, whereas §12.3 supplies one frame per closure. The two-class witness requires distinct descriptors. Its sequential time, occupancy and peaks are correct under §8.2. *Change:* In 'Alternatives and worked witness', use the normative resource names: 'time=2, qubit_second[A]=qubit_second[B]=2, and peak_qubits[A]=peak_qubits[B]=1.'
- **C5 5**: The proposal specifies exclusive representations, complete context coverage, canonical ordering, per-context validation and truthful uniform shorthand. INDEX aligns the frame, resource and fault context vocabulary without conflating their meanings. *Change:* Retain the proposed §12.3 sentence: 'Each scheduled region record contains exactly one of frame and frame_contexts.'
- **C6 4**: check_rev2.py reproduced all eight PASS lines. Independently running the prebuilt reference interpreter reproduced all four pair outputs and four adjoint restorations. These checks validate the witness, not the proposed certificate schema, as the note correctly discloses. *Change:* In 'Conformance vectors and verification'/§15 F,H, publish a fully bound serialized fixture stating: 'entry:0 selects A and entry:1 selects B, both width 1; swapping their classes or reversing canonical record order rejects.' Expected outputs for inputs (0,0),(0,1),(1,0),(1,1) are (1,1),(1,0),(0,1),(0,0), respectively.
- **C7 5**: The new §12.3 paragraph resolves the standing mixed-fat-object check: inventories are device-root-relative, native main/argv/envp/host-only libc are excluded, shared closures retain separate contexts, and native comparison uses the materialised device closure. The incorporated statement accurately identifies the remaining launch and host-memory contract work without claiming §10 already supplies it. *Change:* Retain the proposed §12.3 sentence: 'Shared linked closures retain separate root-relative contexts.'
- **C8 5**: The encoding is implementable using existing context identities and B5 descriptors. §9.2 excludes certificate metadata from object_hash and symbol envelopes; no recipe or catalog change follows from this diff. The catalog pin reproduced, and the publication caveat correctly distinguishes an authorized in-version repair from version-changing publication and reader upgrades. *Change:* Optional addition to 'Hashes, catalog and consumers': 'Upgraded consumers retain truthful legacy uniform frames; producers regenerate certificates requiring nonuniform frames, and consumers must never substitute the first context descriptor for the complete array.'

Suggestions:
1. Conformance vectors/§15 F,H: add a two-root fixture stating, 'Each root has its own [] context; a descriptor from another root is validated against the receiving root’s bindings and placements.' Use a shared flip closure placed in A under root A and B under root B; copying the A descriptor into B’s certificate rejects.
2. Conformance vectors/§15 F,H: add, 'A homogeneous two-call realization accepts one uniform frame; a single-context frame_contexts array is also fully validated.' The homogeneous case uses class A at both call points; the heterogeneous case requires A at entry:0 and B at entry:1.
