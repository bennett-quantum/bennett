# Council — contract-z4c-2026-11-02 round 1

Document snapshot sha256 6fcabf8da311; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

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

Accept the 0.9 K repair. The missing action-support addresses are demonstrated by the actual clauses and reproduced witness. The diff closes the defect without narrowing source capability or requiring catalog or source-envelope byte changes.

**Path to accept:** No blocking changes are required. To raise C6 from 4 to 5, publish the proposed support vectors with complete forward/raw-inverse address records, including the image-81 and nested-oracle selector expectations above.

- **C1 5**: The repair agrees with §3.5 and §4.6: local regions exist once per invocation, independently of predicates and source-loop visits. It changes addressing without changing the action's state transition. *Change:* Optional, §11 K-new: add “Collect declarations from the linked source function before expanding source-loop iterations or forming the action-body adjoint.”
- **C2 5**: §16.2 admits the witness, and §9.2 confirms its declaration is entry:1 and its X is entry:2. The catalog's qregion recipe already implements allocation, unconditional image preparation, body application, inverse image preparation and release. *Change:* Optional, §11 K-new: add “A hoisted qregion declaration emits no additional operation at its lexical declaration point.” For the witness, entry:1 generates no body leaf.
- **C3 5**: Unconditional support preserves §3.5 and K21 under coherent control. Exact inverse image preparation preserves cleanliness. The distinction between raw trace inversion and K62 source-adjoint formation is correct. *Change:* Optional, §11 K-new: add “Image restoration here means reversing image preparation after the body has restored the region to its image; it does not implicitly undo body writes.”
- **C4 5**: The zero-trip witness requires exactly one allocation, one X and one release before target decomposition. Partitioning support separately leaves target matching, allocation widths and resource charges intact. *Change:* Optional, §11 K-new: add “Support addresses neither remove emitted leaves nor change their widths, controls, resource charges or timing dependencies.”
- **C5 5**: The cited defect is real: §11 Matching requires lexical loop-depth coordinates, K64 supplies reserved points only for oracle support, and K65 explicitly excludes implicit qregion restoration. The proposed action points close that hole and specify traversal, ordinals, invocation coordinates and validation. The catalog reproduces as 219 recipes with envelope hash 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197; its bytes need not change. *Change:* Optional, “Hashes, catalog and consumers”: add “Regenerate affected schedules and realised-subject certificate bindings together; unchanged source closure hashes do not establish compatibility of the old support coordinates.”
- **C6 4**: The finite witness is correct. Its closure hash independently reproduces as 439ba7ad235b7ad1663322bc1b7cdf4cffb15d9e798dff7e85d402a9921a20fc. Running the existing prebuilt source_addressing test passed and reproduced all four published selector diagnostics. That corroborates the existing defect, but does not execute the proposed address rules. The proposed vectors are useful; explicit multi-bit image and inverse address records would strengthen them. *Change:* §15, support conformance vectors: add “For qregion r 0 8 @image with image 81, construction is allocation/0, X bit 0/1, X bit 7/2 at $construct; release is X bit 7/0, X bit 0/1, release/2 at $release. Raw inversion retains these points and ordinals while reversing and adjointing the operations.”
- **C7 5**: The repair preserves all admitted placements and imposes no capability restriction on the North Star's coherent programs or demo ladder. §4.6 is the direct normative authority for the hoisted lifetime. No false clause quotation or numbering was found. *Change:* Optional, “Defect and scope”: state “ISA §4.6 requires unconditional function-entry region support; North Star §4.2 and §4.4 require preserving coherent capability and scheduler interoperability.”
- **C8 5**: A consumer can implement the repair using existing reserved-point syntax and the existing qregion recipe. Declaration order, reverse release order, empty vectors, raw inverse identity retention and empty generated domains are specified. The alternative separate coordinate type is viable, but the recommended reuse is smaller. *Change:* Optional, §15: add “For action support inside an oracle step, a selector stopping at the enclosing oracle uses that oracle's step/phase; a selector reaching the action support point requires wildcard step/phase.”

Suggestions:
1. §15: publish complete address records for image 81. Expected $construct ordinals are allocation 0, X bit 0 at 1, X bit 7 at 2; expected $release ordinals are X bit 7 at 0, X bit 0 at 1, release 2. Raw inversion begins with allocation at $release/2, then X bit 0 at $release/1 and X bit 7 at $release/0, retaining allocation identity.
2. §15: add the rule “A selector stopping at the enclosing oracle retains its oracle step/phase; a selector reaching the nested action's support point requires wildcard step/phase.” Include one matching concrete enclosing-oracle selector and one nonmatching concrete action-support selector.
3. “Hashes, catalog and consumers”: add “Affected schedules and their realised-subject certificate bindings must be regenerated together.” Source envelopes and the pinned catalog hash remain unchanged by this diff.

## codex

The cited address defect exists, and the proposed diff repairs it without narrowing scope or changing catalog bytes. The clause references and minimal witness check out. Only stronger test vectors and more precise hash wording are suggested.

**Path to accept:** Already acceptable. To raise C6 from 4 to 5, add the multi-bit image vector with explicit forward and raw-inverse coordinates. To raise C8 from 4 to 5, narrow the canonical-text claim as specified.

- **C1 5**: §4.6 makes qregion function-scoped and creates it at entry; §16.2 permits nested declarations. The proposal preserves that machine model, including declarations inside zero-trip loops. *Change:* No required change. Retain §11's proposed rule: 'Each declaration creates one region per invocation, not one per loop visit.'
- **C2 5**: The diff introduces schedule addresses, not instructions. The witness's source ordinals are correct: qloop is entry:0, qregion is entry:1, and X is entry:2. *Change:* No required change. Retain the proposed §11 rule: '$step and $commit remain oracle-only.'
- **C3 5**: Unconditional allocation and image preparation agree with §3.5 and §11.1 K21. Exact inverse restoration agrees with the catalog. The distinction between raw trace inversion and K62 source-adjoint formation is preserved. *Change:* §15: strengthen the image vector to state: 'For image 81, construction emits allocation, X[0], X[7]; restoration emits X[7], X[0], release, including under a false inherited control.'
- **C4 5**: The zero-trip witness requires exactly allocation, X, and release before target decomposition. The catalog's qregion recipe already supplies these leaves; assigning pseudo-points preserves resource accounting and existing allocation defaults. *Change:* §11: optionally add 'These addresses annotate the existing event stream without adding, removing, reordering, or changing the charge of any emitted leaf.'
- **C5 5**: The defect is real: §11 Matching requires lexical loop-depth coordinates, K64 admits reserved points only for oracle support, and K65 excludes implicit qregion image restoration. The diff supplies deterministic action support coordinates, ordering, and numbering. The 219-recipe catalog envelope independently hashes to 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197, matching §11.1; no catalog edit is needed. *Change:* No required change. Retain §11's proposed rule: 'Their own instance and source-qloop iteration vectors are []; outer invocation edges retain their actual coordinates.'
- **C6 4**: The proposed vectors cover the principal address and validation cases. I also ran the existing prebuilt source_addressing regression: one test passed, reproducing both basis-state round trips, the reported closure hash, and all four address diagnostics. That corroborates the existing defect, not implementation of the proposed coordinates. A multi-bit image would better distinguish inverse ordering. *Change:* §15: add 'With image 81, construction ordinals 0,1,2 denote allocation,X[0],X[7], and release ordinals 0,1,2 denote X[7],X[0],release. Raw inversion visits $release ordinals 2,1,0 first and $construct ordinals 2,1,0 last, adjointing operations without relabelling.'
- **C7 5**: The repair preserves all currently admitted declaration placements and the North Star's coherent-program and substitutable-scheduler scope. It neither suppresses required workspace nor rejects programs to avoid addressing them. *Change:* No required change. Retain §11's explicit inclusion of declarations 'nested in zero-trip qloops and in either qif arm.'
- **C8 4**: The insertion is actionable and the consumer migration is stated. One wording issue remains: 'No change to canonical object text' is too broad when rewritten schedules or certificates are embedded in that text. §9.2 excludes those sections from object_hash, so this does not invalidate the substantive hash claim. *Change:* In 'Hashes, catalog and consumers', replace the opening sentence with: 'Canonical function bytes, symbol envelopes, schedule-independent object_hash values, and ref-0.9.json bytes and hash remain unchanged. Rewriting embedded schedules or certificates changes their serialized bytes and hashes, and the enclosing object's full text.'

Suggestions:
1. §15, image vector: use image 81 as an additional case. State: 'Construction at $construct has allocation at ordinal 0, X[0] at 1, and X[7] at 2; $release has X[7] at 0, X[0] at 1, and release at 2. These support operations remain unconditional for both external control values. Raw inversion retains these addresses while reversing and adjointing the operations.'
2. Hashes, catalog and consumers: distinguish canonical function bytes and object_hash from the entire serialized object. State: 'Updating embedded schedule/certificate sections changes the full object text but not object_hash, because §9.2 excludes those sections; changed schedule bytes require a new schedule_hash and updated certificate bindings.'
