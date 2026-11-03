# Council — contract-checker-fault-rate-2026-11-02 round 4

Document snapshot sha256 fc8bc890d6b4; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 5 | 4 | 4.5 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 5 | 5 | 5.0 |  |

Overall mean: 4.81

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Previous-round blockers, status

- [sol] checker-fault-rate-M1: **resolved** — Both proposals now require action nulls and permit structural-only oracle nulls without census credit; the shared paragraph, conditional sentence and applicability vectors agree.
- [codex] checker-fault-rate-M1: **resolved** — Both notes reproduce Muse's paragraph and conditional oracle sentence exactly: actions require null, structural-only oracles may use null, and required censuses still require RATE/context coverage.

## Blocking issues

- none

## sol

checker-fault-rate-M1 is resolved. The joint diffs admit one consistent encoding, preserve the accepted recount contract and carry bennett-4ht unchanged. Witnesses and conditional identity claims check out; no new S0 issue or regression was found.

**Path to accept:** No blocking changes are required. Publishing the complete serialized two-context certificate and its acceptance/rejection mutations would raise C6 from 4 to 5.

- **C1 5**: The diff preserves §§5.2/14.1's machine semantics. Intrinsic oracle recounts are explicitly distinguished from invocation reachability. *Change:* No change required. Retain in §12.3: 'The report is not the probability that a root execution reaches a call.'
- **C2 5**: §4.2 charges one step per lifted row. The two-row add/retval witness correctly faults at B=0/1 and succeeds at B=2. *Change:* No change required. Retain the example's expected fault maps: {"1":"256"} at B=0/1 and {} at B=2.
- **C3 5**: Counting code(F_B), rather than the accumulated fault word, respects §5.2's XOR interface. Action nulls respect §5.3 without discharging nested oracle obligations. *Change:* No change required. Retain in §12.3: 'The final XOR-accumulated fault word is never the predicate for this count.'
- **C4 5**: Exact budgets, complete scheduled contexts and host-limit outcomes follow §§5.4/12.1/12.2. Target, resource and expansion semantics remain unchanged. *Change:* No change required. Retain in §12.3: 'If limits prevent a legal recount, report unchecked (host limit), discharging no verified fault-rate obligation.'
- **C5 5**: Published §12.3 genuinely lacks per-rate invocation bindings and exclusion replay rules. The repair supplies both. Both notes reproduce Muse's paragraph hash b34376b04d0d2e295018245c1f7f3ce36b4f55ad5ed18e8f127119e36b9685b0 and its conditional oracle sentence; their encodings are jointly satisfiable. *Change:* No change required. Retain the shared §12.3 paragraph: fault_rate is required, actions use null, and oracle null discharges no census obligation.
- **C6 4**: Read-only execution using available compiled interpreter artifacts passed all 768 interface tuples, commit/reversal checks and classifier-bundle cases. The complete serialized multi-context certificate remains accurately disclosed as unpublished. *Change:* In 'Conformance vectors and verification', publish: 'A complete two-call certificate reports {"1":"256"} for B=1 and {} for B=2 using concrete §12.1 keys; its legacy RATE equals the first canonical context without context_key. Missing contexts or a corrupted projection reject.'
- **C7 5**: Reference recounts retain excluded tuples, preserving North Star §§3.2/5.1. The entire bennett-4ht section is byte-identical to round 3 and preserves native host execution, device-root certificates and the explicit remaining boundary obligations. *Change:* No change required. Retain in 'Mixed fat object': 'Unmarked host main, argv/envp and libc are not invented oracle records and need no F_B recount.'
- **C8 5**: Checked, unchecked and rejected outcomes are actionable. In-memory fixture migration changes certificate bytes while preserving object_hash and target/schedule bindings. The unchanged 219-recipe catalog envelope pin reproduces; full-version regeneration and reader upgrades are disclosed. *Change:* No change required. Retain in 'Hashes, publication and consumers': 'A full-version publication instead requires regenerating version-envelope identities and dependent pins.'

Suggestions:
1. In 'Conformance vectors and verification', publish the complete serialized two-context certificate and rejection mutations: B=1 gives {"1":"256"}, B=2 gives {}, the legacy projection matches the first canonical context, and deletion, duplication, reordering or projection corruption rejects.
2. In §12.3's RATE schema notation, make the existing K13 cross-reference explicit for the current K91 text: 'invocation denotes the complete K13 invocation record, including token_aliases where required; process-local ids are never serialized, and the applicable equality partition remains checked.' Update the token-free oracle fixture invocation to include token_aliases:[0]. This clarifies the shorthand without changing recount arithmetic.

## codex

checker-fault-rate-M1 is resolved. The joint §12.3 encoding is satisfiable, the paragraph hash verifies, and the accepted mixed-fat-object statement is unchanged. The defect and counting premises check out; conditional hash-preservation claims hold. No new S0 issue or regression found.

**Path to accept:** No blocking changes required. The K91 clarification would raise C5 from 4 to 5; publishing the complete serialized multi-context fixture and rejection vectors would raise C6 from 4 to 5.

- **C1 5**: The repair preserves §§5.2/14.1 semantics. Recounts describe intrinsic F_B outcomes, independently of inherited predicates and root-call reachability. *Change:* No change required. Retain: "The report is not the probability that a root execution reaches a call."
- **C2 5**: §4.2 charges one step per lifted row. The add/retval witness correctly produces 256 code-1 faults at each of B=0 and B=1, and zero at B=2. *Change:* No change required. Retain the example's fault maps {"1":"256"} at B=0/1 and {} at B=2.
- **C3 5**: Counting code(F_B), rather than the accumulated fault register, respects §5.2's XOR interface. Action nulls respect §5.3, without discharging contained-oracle obligations. *Change:* No change required. Retain: "The final XOR-accumulated fault word is never the predicate for this count."
- **C4 5**: Budget validation follows §5.4; nested calls retain their own tuples. Host-limit handling follows §12.2 and does not shrink domains or alter target/resource semantics. *Change:* No change required. Retain: "If limits prevent a legal recount, report unchecked (host limit), discharging no verified fault-rate obligation."
- **C5 4**: The binding defect exists in published §12.3. The joint diffs now admit one consistent encoding, complete context coverage and independently replayable exclusions. Their shared paragraph reproduces SHA-256 b34376b04d0d2e295018245c1f7f3ce36b4f55ad5ed18e8f127119e36b9685b0. Current K91 warrants an explicit distinction between census tuple equality and full invocation identity. *Change:* In §12.3's recount-binding paragraph, add: "Equality of intrinsic F_B census inputs does not waive K91 token_aliases validation of any full invocation, schedule or identity-dependent claim; equal token tuples do not establish equal token identities."
- **C6 4**: Read-only runs using existing binaries reproduced all 768 interface tuples, commit/reversal checks, 64 exclusions and bundle rejection/unchecked cases. The joint applicability script passed. No fresh build or production certificate checker was exercised; the note accurately discloses its missing serialized multi-context fixture. *Change:* In Conformance vectors and verification, publish: "A complete two-call certificate reports {\"1\":\"256\"} at B=1 and {} at B=2 under concrete §12.1 keys; its legacy RATE equals the first canonical context with context_key removed. Missing, duplicated or reordered contexts and a corrupted projection reject."
- **C7 5**: Full-domain reference recounts remain separate from native-comparison exclusions. The bennett-4ht section is byte-identical to round 3 and preserves native host execution, marked device closures, comparison thunks and explicit remaining launch/memory obligations. *Change:* No change required. Retain: "Unmarked host main, argv/envp and libc are not invented oracle records and need no F_B recount."
- **C8 5**: Applicability, context ordering, projection, replay defaults and failure outcomes are actionable. An in-memory fixture migration changed certificate bytes while preserving object identity and source/schedule bytes. The 219-recipe ref@0.9 envelope hash reproduced; unchanged-envelope qualifications and reader upgrades are explicit. *Change:* No change required. Retain: "Every producer and closed-schema reader using these amended 0.9 certificate bytes must upgrade together."

Suggestions:
1. In §12.3's recount-binding paragraph, add: "Equality of intrinsic F_B census inputs does not waive K91 token_aliases validation of any full invocation, schedule or identity-dependent claim; equal token tuples do not establish equal token identities." Existing K91 obligations remain applicable; this clarifies their relationship to the tuple-only census.
2. In Conformance vectors and verification, publish a complete serialized two-call certificate with concrete §12.1 keys, full domains and the canonical legacy projection. Expected maps are {"1":"256"} at B=1 and {} at B=2; missing, duplicated or reordered contexts and an altered projection must reject.
