# Council — derive3-pe1-2026-11-02 round 1

Document snapshot sha256 e91c1415fe69; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 5 | 5 | 5.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 5 | 4 | 4.5 |  |

Overall mean: 4.81

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Blocking issues

- none

## sol

The defect is real and the proposed repair is correct. No false technical premise or misnumbered cited clause was found. The repaired domain is 2^24, coverage is 1/16777216, and genuine dirty borrowing remains supported. Source/object identities and ref@0.9 stay unchanged; affected certificate bytes change as disclosed.

**Path to accept:** Accept as written through the recommended council-authorized 0.9 K13 witness erratum. Publishing and executing the fully bound four-draw fixture described above would raise C6 from 4 to 5.

- **C1 5**: §§5.2, 12.1 and 12.2 support an empty borrowed component for this subject. With the classical argument fixed, D contains 2+2+4+16=24 bits. *Change:* None required. Retain the proposed §12.1 statement: “The empty borrowed array is required here: the two-row oracle has no checked borrow lifetime.”
- **C2 5**: §4.2 contains no qborrow row; §4.3 supplies qborrow for action bodies (§5.3). The displayed add/retval body introduces no borrowed lifetime. *Change:* None required. Keep the repair confined to §12.1; retain §4.3's rule: “qborrow introduces unknown-state wires usable only inside a borrow frame (§5.6).”
- **C3 5**: §§5.2 and 5.4 give the stated XOR results. Reference executions using the printed ptr_width=2 layout returned (payload,code)=(3,0), (2,0) and (0,1) for the three stated invocations. §5.6 retains preservation of borrowed systems and external correlations. *Change:* None required. Retain §12.1's corrected results: target/fault=(1,3) normally, (0,3) at a=1, and (2,2) at B=1, always with borrowed:[] and regions:[["2","1"]].
- **C4 5**: The unchanged layout satisfies §§7.1–7.2 and §5.4; the reference interpreter accepted it. The unused interface cells remain in D despite the absence of memory accesses. *Change:* None required. Retain the §12.1 rule: “The body does not access memory; the interface cells remain part of D.”
- **C5 5**: K70 expressly rejects positions beyond the checked borrow requirement and treats borrowed names as labels. The repair changes neither that resolver nor the ABI. Under §9.2, source identities remain unchanged; affected certificate tuple/domain bytes change, as the note acknowledges. *Change:* None required. Retain “Hashes, catalog and consumers”: “Any concrete certificate/table fixture based on the invalid example must change its tuple/domain bytes and coverage report; a certificate digest consequently changes.”
- **C6 4**: All 12 cited focused tests passed. Independent checks confirmed all six replacements, the 24-bit denominator, and rejection of invented borrowed positions even labelled x or t. Sampling's R=1 rule consumes zero words. The fully bound four-draw packet remains a publication deliverable, accurately distinguished from the existing exhaustive singleton tests. *Change:* In “Conformance vectors and actual verification” and §15, publish and register the bound ptr_width=2 sampled fixture. State: “Seed [1,0,0,0], count 4, on the singleton before tuple produces four draws, one distinct tuple, zero generator words consumed, and evidence with covered_fraction 1/16777216.”
- **C7 5**: The repair preserves North Star dirty borrowing and external-reference obligations through §§4.3, 5.6 and the genuine borrowing example in §16.3. “Mixed fat object” applies the shared scope statement to the selected device subject and names the remaining mixed-launch work without requiring whole-binary lowering. *Change:* None required. Retain the mixed-object statement: “A native host or another marked module does not contribute a borrowed coordinate, interface cell or certificate record to this subject.”
- **C8 5**: The six tuple occurrences and all prose replacement phrases match the published text, allowing for wrapping. Applying the proposed edits in memory leaves every published object block and the reference-library contract byte-identical. The recommended council-authorized 0.9 example-erratum route repairs an inconsistency with existing K70 rather than introducing different machine semantics. *Change:* None required. Retain the publication decision: “K13 erratum | §12.1 | remove nonexistent borrowed coordinate; D=2^24, coverage=1/16777216 | pe1 | example repair.”

Suggestions:
1. Conformance publication (§15 and the note's verification section): publish the complete bound object/certificate fixture and register its check in reference-interpreter/isa_check.py. Its single table row should map {bundles:["1","2","3"],borrowed:[],regions:[["2","1"]]} to {bundles:["1","1","3"],borrowed:[],regions:[["2","1"]]} at args:["2"], budget:["2","0","0","0"]. State: “Four sampled draws yield evidence, sample_count=4, distinct_samples=1, covered_fraction=1/16777216.” Include rejection cases for an extra borrowed position, stale expected rows after argument/budget rebinding, identity, and an omitted nonzero cell. This completes the disclosed verification deliverable; it is not a semantic blocker.

## codex

The defect is real and the proposed repair is correct. No false operative premise or misnumbered cited clause was found. The repair preserves machine semantics, borrowing capability, source identities and the ref catalog; only affected certificate/table bytes and coverage reports change.

**Path to accept:** Already acceptable through the proposed council-authorized 0.9 K erratum route. Publishing the exact bound sampled fixture would raise C6 to 5; correcting or annotating K67’s historical summary would raise C8 to 5.

- **C1 5**: The repair preserves §5.2’s oracle interface and state transition. The classical argument is fixed by invocation; the domain comprises 2 input, 2 target, 4 fault and 16 interface-memory bits. *Change:* No change required within this repair.
- **C2 5**: §4.2 contains no qborrow row. The stated subject contains only lift.add and lift.retval, with no callee introducing a borrowed lifetime. No opcode changes are proposed. *Change:* No change required within this repair.
- **C3 5**: §§5.2 and 5.4 give the stated results: target 1 at a=2, target 0 at a=1, and target 2/fault 2 at B=1. §§4.3 and 5.6 retain genuine borrowing and preservation of external entanglement. *Change:* No change required within this repair.
- **C4 5**: The retained ptr_width=2 layout satisfies §§7.1–7.2: null [0,1), interface [1,3), empty heap at 3, and one pre-entry within the two-entry table. No target, allocation or resource rule changes. *Change:* No change required within this repair.
- **C5 5**: §12.2 K70 explicitly rejects the invented borrowed position. All six tuple replacements and the widths replacement are correct. Under §9.2, certificate changes do not change object_hash or symbol envelopes; no ref catalog bytes change. The note correctly requires affected certificate bytes/digests to change. *Change:* No change required within this repair.
- **C6 4**: The cited 12 tests reran successfully. An additional in-memory ptr_width=2 singleton replay produced evidence 1/16777216 and rejected extra borrowed positions, argument/budget rebinding, identity output and an omitted output cell. The sampler arithmetic is correct, but the existing replay harness reports sampled claims unchecked; a complete bound four-draw fixture remains unpublished. *Change:* In 'Conformance vectors and actual verification', publish the promised bound ptr_width=2 sampled fixture with seed ["1","0","0","0"], count 4, both region cells and empty borrowed arrays. Its report must show four draws, one distinct tuple, evidence 1/16777216, and after={bundles:["1","1","3"],borrowed:[],regions:[["2","1"]]}.
- **C7 5**: Removing a nonexistent coordinate does not remove dirty-ancilla capability. The mixed-fat-object section explicitly scopes the tuple to its device subject/root and preserves the shared note’s outstanding boundary obligations, without requiring native-host lowering. *Change:* No change required within this repair.
- **C8 4**: The exact edit anchors exist, including across line wrapping, and the proposed same-version erratum resolves an example conflict with accepted K70. However, §0’s K67 historical summary would still advertise 25 bits and 1/33554432. *Change:* In §0’s K67 row, state: 'F=4 and W=8 with a legal unused mapping and no checked borrowed lifetime give a 24-bit domain; four singleton draws cover 1/16777216 with unchanged XOR outcomes.' Cross-reference the newly assigned erratum entry.

Suggestions:
1. §0, K67: update its numerical summary to '24-bit domain' and '1/16777216', and cross-reference the pe1 erratum. Alternatively retain the historical numbers with an explicit supersession annotation; updating the summary is clearer. This is an editorial consistency issue, not a competing execution rule.
2. Conformance publication: publish the promised fully bound 2-bit-layout sampled fixture and negative mutations. Require evidence with four draws, one distinct tuple and coverage 1/16777216; reject the extra borrowed position even when its label matches an interface name. Keep genuine dirty-borrow restoration testing separate.
