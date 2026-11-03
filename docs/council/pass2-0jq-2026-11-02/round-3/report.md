# Council — pass2-0jq-2026-11-02 round 3

Document snapshot sha256 19aa96db4ba6; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

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

- [sol] 0jq-M1: **resolved** — Both proposals now require null | RATE, require action null with contexts absent, and permit structural-only oracle null without discharging census obligations; paragraph bytes and the conditional oracle sentence match Muse exactly.
- [codex] 0jq-M1: **resolved** — Both proposals use the required nullable field, identical applicability wording and matching fixture migration; omitted keys reject and null proves no census.
- [codex] checker-fault-rate-M1: **resolved** — The sibling's unconditional oracle RATE requirement is replaced by the agreed conditional rule, preserving structural-only packets and all scheduled census obligations.

## Blocking issues

- none

## sol

0jq-M1 is resolved. The joint diffs are satisfiable with one encoding, the claimed paragraph hash is correct, and the accepted bennett-4ht statement is unchanged. No new S0 issue, regression, false technical premise or misnumbered citation was found. Accept this repair; D2's remaining joint-review and Muse conditions still govern publication.

**Path to accept:** No blocking changes remain. To raise the lowest criterion, C6, from 4 to 5, publish the complete structural-H positive and negative certificate fixtures specified above.

- **C1 5**: The diff preserves machine state and execution. Its oracle/action distinction matches ISA §§5.2–5.3. *Change:* No change required. Retain §5.3's rule: 'No fault outcome.'
- **C2 5**: Owner-local inverse-pair entries, swapped orientations, primary-budget inequality, exact arg_tokens and pre-effect validation agree with §4.5. K63 and K65 do not transfer ownership; K91's additional identity constraints remain applicable. *Change:* No change required. Retain the proposed §12.3 sentence: 'Before any effect of the enclosing CC/R region call, check coverage for every transitively executed qinplace using its owner entry and resolved token and classical arguments (§4.5).'
- **C3 5**: The H witness follows exactly from §4.4: H²=I, while H is not a permutation. Structural claims remain distinct from comparison, numerical and channel claims. Null discharges no fault-rate obligation. *Change:* No change required. Retain §12.3's proposed rule: 'A structural adjoint-table or translation claim is not such a comparison claim.'
- **C4 5**: The diff changes no resource, target, schedule or catalog semantics. An independent in-memory fixture migration preserved object_hash 45bbb506541e3a8bb28a18e1bb0aef16ba01ee1e7cac74d5a190deb3ad36ef5a and function, target and schedule identities while changing certificate bytes. The catalog check reproduced all 219 recipes and its published envelope hash. *Change:* No change required. Retain 'Publication and validation boundary': 'All unchanged-hash claims assume unchanged header/source and catalog envelopes.'
- **C5 5**: The cited defects exist: §9.2 defines reference_program_hash specifically for an oracle, and §12.3 requires comparison/census fields despite K13 admitting standalone structural claims. Both revised notes contain Muse's byte-identical paragraph with SHA-256 b34376b04d0d2e295018245c1f7f3ce36b4f55ad5ed18e8f127119e36b9685b0 and the identical conditional oracle sentence. Their combined rules admit one consistent encoding. *Change:* No change required. Retain §12.3's proposed rule: 'verification.fault_rate is required and has type null | RATE.'
- **C6 4**: check_rev2.py passed all eight result lines; the joint check passed. The existing interpreter witness reproduced 256 faults at B=0 and B=1, zero at B=2, arbitrary-target/fault XOR delivery and complete machine reversal. The new verification fragment correctly distinguishes structural acceptance from census-dependent acceptance, but is explicitly not a complete certificate fixture. *Change:* In 'Conformance vectors and verification', publish a complete invocation-bound structural-H certificate and state: 'Accept the adjoint_table claim with verification.oracle:null and verification.fault_rate:null; reject oracle:0, reject omission of fault_rate, and reject using null to discharge a required census or zero-fault gate.'
- **C7 5**: The accepted bennett-4ht normative paragraph is byte-identical to round 2; only its shared-statement link was relocated. Device-root identity, separate certificates and native-only inventory exclusions remain explicit. Remaining launch and host-memory obligations are named without excluding mixed execution. *Change:* No change required. Retain the proposed §12.3 sentence: 'The container associates each object/root pair with its certificate; several device roots may have separate certificates.'
- **C8 5**: The fixture migration correctly selects the root's table claim at index 0, leaves the numerical-only child's oracle selector null and changes both action census placeholders to null. Required-key handling, linked proof resolution, coordinated reader upgrades and conditional D2 publication authority are explicit. *Change:* No change required. Retain 'Paragraph byte identity and verification': 'Every producer and closed-schema reader using these amended 0.9 certificate bytes must upgrade together for the required nullable field and context/evidence fields; older readers cannot silently accept them.'

Suggestions:
1. In 'Conformance vectors and verification', publish the complete structural-H packet described under C6, including ordinary bindings and its K13 invocation. Expected results: structural claim accepted with oracle:null and fault_rate:null; structural index oracle:0 rejected; missing fault_rate rejected; null insufficient for census-dependent or zero-fault acceptance.

## codex

0jq-M1 and the corresponding checker-fault-rate-M1 are resolved. The shared paragraph hash, conditional oracle sentence, retained recount/context rules, fixture migration and unchanged bennett-4ht statement check out. The cited defect premises are real; no false technical premise, misnumbered citation, regression or new S0 issue was found. Accept the joint repair.

**Path to accept:** No blocking changes remain. To raise the lowest criterion, C6, from 4 to 5, publish the complete structural-H certificate and its explicit negative variants. Publication remains subject to D2's joint-review and Muse-acceptance conditions.

- **C1 5**: The repair preserves the machine state and step relation. Its oracle/action distinction agrees with ISA §§5.2–5.3. *Change:* No change required; retain §5.3's rule: 'No fault outcome.'
- **C2 5**: Owner-local inverse-pair entries, swapped-pair coverage, primary-budget inequality, exact arg_tokens matching and pre-effect validation accurately reflect §4.5. K63/K65 do not transfer ownership; the amendment also preserves §12.3 K91/K92's additional requirements. *Change:* No change required; retain the proposed §12.3 sentence: 'The owner of a qinplace inverse-pair entry is exactly the region whose source body contains that instruction (§4.5).'
- **C3 5**: The Hadamard witness follows exactly from §4.4. Structural claims remain distinct from permutation, numerical and channel comparisons. Null supplies no fault-rate evidence and does not weaken executable obligations. *Change:* No change required; retain the proposed §12.3 rule: 'Applicable oracle-correctness, fault-rate, borrowed-system and realisation obligations remain required before an executable or algorithm acceptance claim can use them.'
- **C4 5**: No resource, target or schedule semantics change. In-memory fixture migration changed certificate bytes while preserving object_hash 45bbb506541e3a8bb28a18e1bb0aef16ba01ee1e7cac74d5a190deb3ad36ef5a and target/schedule bytes. ref_catalog.py --check reproduced 219 recipes and envelope hash 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. *Change:* No change required; retain the publication qualification: 'All unchanged-hash claims assume unchanged header/source and catalog envelopes.'
- **C5 5**: The applicability defects remain present in published §§9.2 and 12.3 despite K13 admitting standalone structural claims. Both revised proposals now require fault_rate:null|RATE, agree on conditional oracle censuses and retain invocation/context validation. Their shared paragraph is byte-identical to Muse's requested text, with SHA-256 b34376b04d0d2e295018245c1f7f3ce36b4f55ad5ed18e8f127119e36b9685b0. *Change:* No change required; retain the shared §12.3 rule: 'For action and perm_action records it MUST be null and fault_rate_contexts MUST be absent.'
- **C6 4**: check_notes.py joint and all eight check_rev2.py result lines pass. The existing interpreter witness reproduced 768 tuples: 256 code-1 faults at each of B=0 and B=1, zero at B=2, with commit and reversal checks. The new structural-oracle vector is explicitly a fragment, not a complete certificate or production-checker test. *Change:* In 'Conformance vectors and verification', publish a complete invocation-bound structural-H certificate and state: 'With verification.oracle:null and fault_rate:null, accept only the checked structural claim; changing oracle to its structural claim index rejects, omitting fault_rate rejects schema validation, and null cannot discharge a zero-fault gate.' Include the required current §12.3 bindings.
- **C7 5**: The accepted bennett-4ht normative paragraph is unchanged; the surrounding section changes only its relative link. Separate device roots retain their certificates and contexts, native-only code remains outside their inventory, and the shared statement names the remaining launch and host-memory obligations. No north-star capability is narrowed. *Change:* No change required; retain the proposed §12.3 sentence: 'The container associates each object/root pair with its certificate; several device roots may have separate certificates.'
- **C8 5**: The combined diffs admit one consistent encoding: actions use null; structural-only oracles may use null without satisfying census obligations; required censuses use invocation-bound RATE records. Fixture migration correctly selects root comparison index 0, retains the numerical-only child's oracle:null and replaces both action census placeholders with null. Consumer upgrades and D2's conditional publication route are explicit. *Change:* No change required; retain the consumer rule: 'Every producer and closed-schema reader using these amended 0.9 certificate bytes must upgrade together for the required nullable field and context/evidence fields; older readers cannot silently accept them.'

Suggestions:
1. In 'Conformance vectors and verification', add the complete structural-H certificate described under C6. Expected results: structural validation succeeds with both fields null; a structural index used as verification.oracle rejects; an omitted fault_rate key rejects; requesting a zero-fault acceptance result from null fails. This is conformance packaging, not an acceptance prerequisite.
