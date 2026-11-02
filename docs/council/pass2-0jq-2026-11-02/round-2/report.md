# Council — pass2-0jq-2026-11-02 round 2

Document snapshot sha256 19ffcda5e44a; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

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

- [sol] 0JQ-1: **resolved** — The proposed §12.3 mixed-object paragraph identifies device object/root bindings, certificate association, linked owner records and the native-only inventory exclusion.
- [sol] B1: **resolved** — The new paragraph and shared scoping statement cover multiple device roots without requiring native main, argv/envp or host-only libc to become ISA regions.
- [codex] 0JQ-1: **resolved** — The proposed §12.3 mixed-object paragraph identifies device-object/root bindings and owner-record inventory while preserving native host code.
- [codex] B1: **resolved** — The §9.2 cross-reference, §12.3 paragraph and shared scope statement provide the requested multiple-root certificate association and native-only exclusions.

## Blocking issues

- none

## sol

Both round-1 blockers, sol 0JQ-1 and codex B1, are resolved. The cited defects, clause references, ownership premises, H algebra and conditional hash claims check out. No false technical premise, misnumbered citation or new S0 issue was found. Accept as a 0.9 K repair subject to the stated publication authorization.

**Path to accept:** No blocking changes remain. To raise the lowest score, C6, from 4 to 5, publish the complete structural H packet and explicit negative outcomes described above.

- **C1 5**: The diff preserves the accepted machine state and step relation. Its oracle/action distinction agrees with §§5.2–5.3. *Change:* No change required; retain §5.3's rule that an action has no fault outcome.
- **C2 5**: The ownership, swapped-pair coverage, componentwise primary-budget bound and exact arg_tokens premises accurately reflect §4.5. *Change:* No change required; retain §4.5's instruction expansion and inverse-pair coverage rules.
- **C3 5**: The H witness follows exactly from §4.4. Structural claims remain distinct from permutation, numerical and channel comparisons. The revised preflight sentence preserves §4.5's before-any-effect requirement. *Change:* No change required; retain the proposed §12.3 rule that absent fault_rate asserts neither zero faults nor a checked census.
- **C4 5**: No resource, target or schedule semantics change. An in-memory fixture migration preserved object hash 45bbb506541e3a8bb28a18e1bb0aef16ba01ee1e7cac74d5a190deb3ad36ef5a and its function, target and schedule identities while changing certificate bytes. The catalog check reproduced all 219 recipes and the published envelope hash. *Change:* No change required; retain the publication qualification that unchanged hashes assume an authorized in-version repair with unchanged source and catalog envelopes.
- **C5 5**: The defects exist in §§9.2 and 12.3: the reference hash is oracle-specific, and the schema requires comparison/census fields despite K13 permitting standalone structural claims. The repair defines absence, owner-local indices, checked library references and device-root inventory without weakening applicable obligations. *Change:* No change required; retain the proposed §12.3 requirements for owner-local claim indices and checked linked-library references.
- **C6 4**: The eight revision checks pass, including exact H algebra. The proposed positive and negative vectors are sound, and the note accurately discloses that they do not implement a packet checker. A complete structural packet would make the repaired schema easier to conformance-test. *Change:* In 'Conformance vectors and verification', publish a complete standalone H packet with a valid K13 invocation, verification.oracle:null and absent fault_rate. State: 'Accept its structural claim only; reject the structural claim's index as verification.oracle; absence of fault_rate does not satisfy a zero-fault acceptance gate.'
- **C7 5**: The new §12.3 paragraph satisfies the mixed-fat-object standing check: object/root bindings identify device subjects, multiple roots retain separate certificates, and native-only code requires no region inventory. The shared statement names the exact remaining boundary-contract work without requiring whole-binary lowering. *Change:* No change required; retain the proposed mixed-object paragraph and its §9.2 cross-reference.
- **C8 5**: The revision distinguishes packet containment from region ownership, states preflight timing explicitly, and gives the correct controlled-action migration: root index 0, numerical-only child null, both action censuses omitted. Publication authority and consumer migration are expressly qualified. *Change:* No change required; retain the fixture migration sentence and the explicit council/maintainer authorization requirement for the 0.9 K route.

Suggestions:
1. In 'Conformance vectors and verification', add a complete JCS standalone H certificate and two mutations. Expected results: accept the invocation-bound structural packet with oracle:null and no fault_rate as structural verification only; reject its structural claim index as verification.oracle; reject use of the absent census to discharge a zero-fault acceptance gate.

## codex

Both round-1 blockers, 0JQ-1 and B1, are resolved. No new S0 issue, regression, false technical premise or misnumbered citation was found. The applicability repair, ownership rules, fixture migration and conditional hash/catalog claims check out. Accept the proposed repair; publication still requires the stated maintainer authorization.

**Path to accept:** No blocking changes remain. To raise C6 from 4 to 5, publish complete serialized structural-H acceptance/rejection fixtures with the invocation, bindings and expected verdicts specified above.

- **C1 5**: The diff leaves machine state and execution unchanged. Its distinction between oracle outcomes and action interfaces agrees with §§5.2–5.3. *Change:* No change required; retain §5.3's rule: 'No fault outcome.'
- **C2 5**: The ownership, swapped-pair coverage, componentwise primary-budget bound, exact arg_tokens matching and pre-effect validation agree with §4.5. K63 and K65 do not transfer proof ownership. *Change:* No change required; retain the proposed §12.3 rule requiring coverage for every transitively executed qinplace before any effect of the enclosing CC/R region call.
- **C3 5**: The Hadamard witness follows exactly from §4.4: H²=I, while H is not a permutation. The diff preserves numerical/channel, borrowed-system and inverse-pair obligations rather than treating structural claims as executable correctness proofs. *Change:* No change required; retain the §12.3 statement that applicable correctness, borrowed-system and realisation obligations remain required before executable or algorithm acceptance.
- **C4 5**: Resource, target and schedule semantics remain unchanged. An independent in-memory fixture migration preserved object_hash 45bbb506541e3a8bb28a18e1bb0aef16ba01ee1e7cac74d5a190deb3ad36ef5a while changing certificate bytes. The catalog check reproduced 219 recipes and envelope hash 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. *Change:* No change required; retain the publication rule that unchanged hashes assume an authorized in-version repair with unchanged source and catalog envelopes.
- **C5 5**: Both stated applicability defects exist in §§9.2 and 12.3. The proposed null/absence semantics, root-reference definition, owner-local indices and checked library references repair them consistently. The referenced jw7 and first-pass census text supply explicit invocation/context binding. *Change:* No change required; retain the §12.3 rules that an absent census asserts neither zero faults nor verification, and every supplied census must be validated.
- **C6 4**: All eight check_rev2.py result lines pass. The exact algebra and proposed rejection cases are sound, and the note accurately distinguishes finite checks from an implemented packet checker. Complete serialized structural and ownership fixtures would strengthen reproducibility. *Change:* Add a complete §15 structural-H fixture stating: 'With a valid K13 invocation, the sole adjoint_table claim, verification.oracle:null and absent fault_rate validate only the structural relation; changing oracle to 0 rejects, and the absent census cannot satisfy a zero-fault acceptance gate.' Publish both packet variants with their expected verdicts.
- **C7 5**: The new §12.3 paragraph and incorporated shared statement satisfy the standing mixed-fat-object check: bindings select device objects and roots, native-only code needs no region inventory, and separate roots retain separate contexts. Remaining launch and memory boundary obligations are explicitly identified without requiring whole-binary lowering. *Change:* No change required; retain the proposed rule associating each embedded ISA object/root pair with its certificate and excluding native-only host code from the device-region inventory.
- **C8 5**: The revision resolves the packet-versus-record wording, states preflight timing explicitly and gives the correct controlled-action fixture migration: root oracle index 0, numerical-only flip null, both action census placeholders omitted. Publication and consumer limitations are explicit. *Change:* No change required; retain the migration instruction that ambiguous old action bindings require explicit validation rather than silent reinterpretation.

Suggestions:
1. In §15, publish the complete structural-H positive and negative packets described under C6. Expected results: structural relation accepted with oracle:null and no census; structural claim index 0 rejected as verification.oracle; absent census insufficient for a zero-fault gate. This is conformance packaging, not a prerequisite for acceptance.
