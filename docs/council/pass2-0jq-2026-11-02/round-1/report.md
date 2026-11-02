# Council — pass2-0jq-2026-11-02 round 1

Document snapshot sha256 e4e812fd4123; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 4 | 4 | 4.0 |  |
| C6 | 4 | 5 | 4.5 |  |
| C7 | 4 | 4 | 4.0 |  |
| C8 | 4 | 4 | 4.0 |  |

Overall mean: 4.56

Verdicts: **sol: revise**, **codex: revise**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: no**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 1 (blocking 1), codex: core 0 / contract 1 (blocking 1)

## Blocking issues

- **[sol] 0JQ-1** (Recommended exact spec diff, §§9.2 and 12.3; North Star scope; contract): The proposal changes certificate layout and root identity without stating how a mixed fat object uses them. Neither the note nor INDEX's shared publication decisions identifies the embedded device object as the binding subject or explains certificate inventory alongside native host code. This fails the council's explicit standing mixed-fat-object check, independently of the otherwise sound applicability repair. *Fix:* Append to §12.3: 'A mixed fat object may contain native host code together with embedded ISA objects and certificates for their oracle or action roots. Each certificate's object_hash binds its embedded ISA object; interface_hash, closure_hash and reference_program_hash identify the selected device root under §9.2. The fat-object container associates each certificate with that embedded object and root closure, and a composed certificate retains linked device proof records under their owner closure hashes. Native host code outside the tainted call graph remains native and is not required to appear as ISA regions or carry oracle comparison claims or fault censuses.' This permits a container inventory or separate per-root packets; I would use separate per-root packets associated by object and root closure hashes.
- **[codex] B1** (Recommended exact spec diff — §§9.2 and 12.3; Defect and North Star scope; contract): The proposal changes certificate root identity and linked owner-record inventory but provides no mixed-fat-object application statement. INDEX's general no-narrowing assertion does not identify which embedded object/root these bindings name or explain that native-only code remains outside the region inventory. This fails the explicitly required bennett-4ht standing check against North Star §§2, 3.3 and 4.4. *Fix:* Append to §12.3, cross-referenced from §9.2: 'For a mixed fat object, these certificate bindings apply to each embedded or linked ISA object and its certified device-region root. object_hash identifies that ISA object; reference_program_hash identifies the interface of the oracle or action root selected by bindings.closure_hash. Neither field identifies the native host binary or its entry point. The fat-object certificate inventory may aggregate certificates for multiple device roots. Each composed regions map contains the relevant device-region owner records and checked linked-library proofs; native-only code requires no region record, oracle comparison, fault census or inverse-pair entry. These rules do not require lifting the native host or unmarked code.' Example: native main with marked device roots A and B carries certificates rooted at A and B, with their respective ISA-object bindings; main is not a required regions entry. No container encoding or launch implementation is required by this clarification.

## sol

The main defect statements, clause references, H algebra, inverse-pair ownership and conditional hash/catalog claims check out. The proposal needs one contract addition to satisfy the mandatory mixed-fat-object check.

**Path to accept:** Add the mixed-fat-object binding and inventory statement in 0JQ-1 to the exact §12.3 diff. The remaining changes are editorial suggestions; no core repair is required.

- **C1 5**: The diff changes certificate metadata and applicability; it leaves the accepted machine state, tiers and step relation unchanged. *Change:* None required in §§3–5.
- **C2 5**: The ownership and coverage descriptions agree with §4.5, including swapped G/H orientations, componentwise primary-budget coverage and exact token-argument tuples. *Change:* None required in §4.5; retain its existing inverse-pair obligation and generated instruction sequence.
- **C3 5**: §4.4 gives the stated Hadamard matrix, so H²=I and H is not a permutation. §5.3 gives actions no fault outcome. The proposal preserves these distinctions and does not promote structural claims into executable correctness proofs. *Change:* Editorially, replace the final proposed §12.3 sentence with: 'Before any effect of the enclosing CC/R region call, check every transitively executed qinplace using its owner record and resolved token and arguments, as required by §4.5.'
- **C4 5**: Target, resource and schedule semantics remain unchanged. An in-memory removal of the fixture's action fault reports preserved object hash 45bbb506541e3a8bb28a18e1bb0aef16ba01ee1e7cac74d5a190deb3ad36ef5a. The catalog check reproduced 219 recipes and envelope hash 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. *Change:* None required; retain the INDEX qualification that unchanged envelope hashes depend on an explicitly authorized in-version repair.
- **C5 4**: The defects are real: §12.3 requires oracle:i and fault_rate despite K13 admitting standalone structural claims, and §9.2 defines reference_program_hash only for oracles. Owner-local lookup correctly follows §§4.5 and 9.3. The certificate change still lacks the required mixed-fat-object application statement. *Change:* Add the §12.3 mixed-object binding and certificate-inventory rule written in 0JQ-1.
- **C6 4**: The exact H witness in INDEX passes. The proposed positive and negative ownership vectors follow the existing obligations, and the note accurately discloses that no packet checker was implemented. A concrete structural packet would make conformance expectations easier to reproduce. *Change:* Add a §15 vector stating: 'A standalone h t adjoint_table claim with a valid K13 invocation, verification.oracle:null and absent fault_rate is accepted as a structural claim only; placing its structural claim index in verification.oracle rejects, and the packet discharges neither executable-realisation verification nor a zero-fault acceptance gate.'
- **C7 4**: The applicability repair preserves general quantum actions and honest proof/evidence distinctions required by North Star §§4.2 and 5.1. However, neither 0jq nor INDEX's publication section states how the revised certificate contract serves the mixed fat object required by §§2, 3.3 and 4.4. *Change:* Add the explicit mixed-fat-object rule in 0JQ-1; no host-shim implementation is required for this review.
- **C8 4**: The proposed root-reference definition, owner-local indices, conflict rejection and absence semantics are understandable. The alternatives table loosely says 'outer packet', although a composed outer packet may legitimately contain inner's owner record. *Change:* In the alternatives table, replace 'Put all nested proofs in the outer packet' with 'Put nested inverse_pairs entries and their claims in the outer region record'; state that a composed root packet may contain the correctly keyed inner owner record.

Suggestions:
1. In §12.3, repeat the existing preflight timing explicitly: 'Before any effect of the enclosing CC/R region call, validate coverage for every transitively executed qinplace using its resolved token and arguments.' The existing §4.5 rule remains binding; the new phrase 'at every reached instruction' should not suggest delaying validation until after earlier gates have executed.
2. In the alternatives table, replace 'Put all nested proofs in the outer packet' with 'Put nested inverse_pairs entries and their claims in the outer region record'. A single composed outer packet containing regions[closure(inner)] is valid and is precisely the transport arrangement the recommended diff permits.

## codex

The cited defects, ownership premises, H witness and conditional unchanged-hash claims check out. No false technical premise or misnumbered citation was found. One mandatory mixed-fat-object contract statement is missing; the core is acceptable.

**Path to accept:** 1. Add B1's mixed-fat-object binding and inventory paragraph to the exact diff. This is the only blocking change; the fixture migration and wording suggestions are discretionary.

- **C1 5**: The diff changes certificate applicability and bindings, leaving machine state and the step relation unchanged. Its distinction between oracle outcomes and fault-free action interfaces agrees with §§5.2–5.3. *Change:* No machine-model change required; retain §5.3: 'An action has no fault outcome of its own.'
- **C2 5**: The H witness agrees exactly with §4.4. The ownership, swapped-pair coverage, componentwise primary-budget bound and exact arg_tokens rules accurately quote §4.5. *Change:* No instruction change required; retain §4.5's rule: 'Coverage requires the entry budget to be componentwise no greater than the instruction token tuple, and token-argument tuples to equal arg_tokens exactly.'
- **C3 5**: H²=I does not establish a permutation assertion. The diff correctly separates structural claims from executable comparison claims and preserves numerical/channel, borrowed-system and inverse-pair obligations. *Change:* Optional §12.3 clarification: 'A structural adjoint-table claim establishes the source adjoint relation; it does not certify a target realisation or discharge a required numerical/channel claim.'
- **C4 5**: No target, resource or schedule rule changes. Under INDEX's authorized in-version route, §9.2 excludes the changed certificate bytes from object identity. The 219-recipe catalog check reproduced the published envelope hash. *Change:* Retain the publication qualification: 'Unchanged non-certificate hashes assume an authorized in-version repair with unchanged source envelopes; a full-version bump requires recomputing affected version-prefixed identities.'
- **C5 4**: Both reported gaps exist in §§9.2 and 12.3. K13 permits standalone structural relations, while the schema requires an oracle index and fault_rate. Owner-local indexing agrees with §4.5; K63 and K65 do not transfer ownership. The required mixed-fat-object binding statement is missing. *Change:* Add to §§9.2/12.3: 'In a mixed fat object, certificate object and root bindings identify an embedded or linked ISA object and its device-region root; native-only code is not part of the regions inventory.'
- **C6 5**: The exact H-square/non-permutation check passes. The proposed positive and negative cases distinguish structural applicability, wrong owners, dangling references and invocation coverage without claiming an implemented packet checker. *Change:* Optional §15 vector: 'Accept an invocation-bound structural H certificate with verification.oracle=null and no fault_rate; reject that structural claim's index as verification.oracle, and never treat the absent census as zero faults.'
- **C7 4**: The repair preserves general quantum actions and honest proof/evidence labels. However, neither 0jq nor INDEX states how the changed certificate roots and inventory serve native host code plus marked device modules, as the standing bennett-4ht check requires. *Change:* Add the mixed-fat-object paragraph specified in B1, explicitly permitting separate certificates for multiple device roots without requiring the native host entry point to become an ISA region.
- **C8 4**: The repair is small and actionable, and its clause citations are accurate. Migration should explicitly cover the published fixture's root table claim as well as its numerical-only callee: both currently use oracle:null. *Change:* In 'Hashes, catalog and consumers', state: 'For the controlled-action fixture, set the root verification.oracle to 0, retain null for the numerical-only flip record, and omit both action fault_rate placeholders.'

Suggestions:
1. In 'Hashes, catalog and consumers' and the controlled-action conformance vector, state: 'The root record's exhaustive table claim is index 0, so verification.oracle is 0; the numerical-only flip record retains null; both action fault_rate placeholders are omitted.' An in-memory migration preserved object_hash 45bbb506541e3a8bb28a18e1bb0aef16ba01ee1e7cac74d5a190deb3ad36ef5a while changing certificate bytes.
2. In the final §12.3 ownership sentence, preserve §4.5's explicit timing: 'Before any effect of the enclosing CC/R region call, check covering owner entries for every transitively executed qinplace using its resolved token and classical arguments; failure is a CC trap or R FAULT_UB_TRAP.' This avoids suggesting that checking may wait until earlier instructions have already taken effect.
3. In §12.3, make the action-field default explicit: 'For action and perm_action records, fault_rate is absent; nested oracle censuses belong to their oracle records.' Alternatively define a legacy empty action placeholder that asserts no census and discharges no obligation. Prefer absence, matching the proposed schema and avoiding an undefined action-owned recount.
