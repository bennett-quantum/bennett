# Council — pass2-4ta-2026-11-02 round 2

Document snapshot sha256 2fdc2c25635f; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

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

- [sol] 4ta-B1: **resolved** — Sol: the §3.3 replacement now specifies heterogeneous vectors, concat/slice, reversal and atomic frame-binding checks.
- [sol] 4ta-B2: **resolved** — Sol: the proposed §9.4 paragraph explicitly scopes descriptors to device invocations in mixed fat objects.
- [sol] B1: **resolved** — Codex: the homogeneous-register contradiction is repaired, with the A/B construction and reversal witness.
- [sol] B2: **resolved** — Codex: the native-host/device-wrapper example and shared boundary obligations make the fragmented slot reachable without whole-binary lowering.
- [codex] 4ta-B1: **resolved** — Sol: the §3.3 replacement explicitly defines heterogeneous vectors, construction, binding and reversal, with the requested A/B witness.
- [codex] 4ta-B2: **resolved** — Sol: the proposed §9.4 paragraph and shared scope statement delimit device certificate inventory and preserve the native-host boundary.
- [codex] B1: **resolved** — Codex: the singular-class register contradiction is removed; concatenation, slicing, free and reversal preserve complete vectors.
- [codex] B2: **resolved** — Codex: the mixed-object statement supplies the device CC wrapper route and excludes native entry, argv/envp and host-only libc from B5 inventory.

## Blocking issues

- none

## sol

All four previous blockers—sol 4ta-B1/4ta-B2 and codex B1/B2—are resolved. No new S0 issue or regression was found. The witnesses, cited ISA premises and conditional hash claims check out. Acceptance supports the proposed repair; publication still follows its stated authorization boundary.

**Path to accept:** Already acceptable. Raise C6 from 4 to 5 by adding the complete fragmented-frame fixture and explicit admission verdicts given under C6.

- **C1 5**: The proposed §3.3 replacement consistently defines ordered wire/class vectors, homogeneous allocation, heterogeneous concatenation, slicing and ledger restoration. Existing alias and ownership rules remain applicable. *Change:* No correction required; retain §3.3's rule that class vectors grant no permission to relabel, move or share wires.
- **C2 5**: The revised qreg transitions reconcile heterogeneous registers with §4.7's CC/R operands. Width, disjointness and view-consumption checks remain intact. *Change:* Optionally add to §3.3: 'For qreg.new any n, resolve any under §17 item 10 before constructing the homogeneous class vector.'
- **C3 5**: The exact X sequence implements t XOR 3, with outputs 3,2,1,0 and an exact inverse. Fragmentation introduces no quantum operation or state inspection. Reversal retains the existing §3.3, §10 and T4 hypotheses. *Change:* No correction required; retain the explicit preservation of new-frame reversal's cleanliness and exclusivity hypotheses.
- **C4 5**: §§8.2–8.4 and 11 support the per-bit placement premise and the stated sequential time 2, occupancy 2 per class and peak 1 per class. Region flattening and the enlarged controlled target are correct. *Change:* Optionally add under Conformance vectors: 'The enlarged controlled target uses unit occupancy rates for A, B and C.'
- **C5 5**: The B5 defect is real. The proposed alternatives define complete, canonical class partitions while preserving slot identity and legacy homogeneous records. §9.2 excludes certificate bytes from object identity; the conditional unchanged-source and catalog claims are sound. *Change:* No correction required; retain the publication boundary distinguishing an authorized in-version repair from a full-version publication.
- **C6 4**: check_rev2.py reproduced all eight PASS lines. The FRAME hash and 219-recipe catalog envelope also match. The conformance obligations are derivable, but the note supplies no complete serialized fragmented frame with explicit positive and negative admission verdicts. *Change:* Under Conformance vectors add this accepted frame: {"slots":[{"id":"mut:0","role":"mut","width":2,"fragments":[{"offset":0,"width":1,"class":"A"},{"offset":1,"width":1,"class":"B"}]}],"scratch":[],"history":[],"borrow":[],"ancillae":[]}. State: 'Accept for the A/B witness; changing the second offset to 2 rejects for incomplete and out-of-range coverage.'
- **C7 5**: The §9.4 mixed-object paragraph and incorporated scope statement satisfy bennett-4ht: native host code remains native, device invocations receive frames, and missing boundary contracts are named explicitly. No North Star capability is removed. *Change:* No correction required; retain the distinction between device-frame inventory and native main, argv/envp and host-only libc.
- **C8 4**: The fragment rules and consumer obligations are implementable. The instruction to update every ledger reference is semantically sufficient, but an explicit edit list would make application less error-prone. *Change:* In Recommended exact spec diff, explicitly include §3.2's ledger-state row and §7.4's qreg history row: replace stored register 'class' with 'ordered class vector', using the plural where multiple registers are recorded.

Suggestions:
1. Recommended exact spec diff: explicitly change §3.2's ledger-state row and §7.4's qreg history row to record ordered class vectors, as specified under C8.
2. Recommended §3.3 binding rule: optionally state, 'At a CC/R call, failure of register-to-selected-frame class-vector or inherited-placement equality produces FAULT_UB_TRAP before any effect or view consumption.' For actual [A,B] and selected [A,A], the expected outcome is code 4 with the register and view states unchanged.

## codex

All four round-1 blockers are resolved. The defect, revised class-vector semantics, resource examples and conditional identity claims withstand the cited-clause checks. No new S0 issue or regression was found. Acceptance is for the proposed repair, subject to its stated publication authorization rules.

**Path to accept:** No blocking changes remain. To raise C6 from 4 to 5, add the explicit failed-binding ledger-state vector and its reversal expectations.

- **C1 5**: The proposed §3.3 class vector reconciles heterogeneous registers with the existing ownership model. Concatenation, slicing, zero-width registers and ledger reversal preserve wire identity and ordering. *Change:* None required; retain the explicit prohibition on relabelling, movement and new storage-sharing permissions.
- **C2 5**: The revised qreg.new/concat/slice/free rules compose with §§3.3 and 4.7 without changing gate semantics. Class-vector validation uses the existing preflight before effects or view consumption. *Change:* None required; retain homogeneous allocation requests and heterogeneous concatenation.
- **C3 5**: Fragments introduce no quantum operation. The exact X sequence implements t XOR 3; its adjoint restores every input. Ledger restoration retains the existing cleanliness, exclusivity and reverse-eligibility hypotheses. *Change:* None required; retain §10 and T4's eligibility and exactness qualifications.
- **C4 5**: §§8.3 and 11 support per-bit placement, while current B5 supplies one class per slot. The repair correctly enforces complete canonical partitions, inherited classes, topology equality and per-class accounting. The sequential time, occupancy and peak values are correct. *Change:* None required; retain the distinction between descriptive fragments and allocations or lifetimes.
- **C5 5**: The B5 alternatives preserve slot identity and homogeneous records. Under the explicitly conditional in-version route, §9.2 excludes certificate bytes from object identity. The ref catalog's qreg recipes remain classical events, so no recipe or ordinal change is required. Full-version migration is acknowledged. *Change:* None required; retain the publication authorization caveat and full-version identity regeneration rule.
- **C6 4**: check_rev2.py reproduced all eight PASS lines. Independent checks confirmed the published FRAME, topology-target and 219-recipe catalog hashes. The finite script checks the stated arithmetic and modelled vectors, but does not exercise failed-binding view-state preservation. *Change:* In Conformance vectors add: “After v = qreg.slice t 1 1 on t with classes [A,B], binding v to a selected width-one A slot faults with FAULT_UB_TRAP (4) before effects or view consumption; t remains viewed and v remains live. Reversing the fault and slice restores the pre-slice ledger state.”
- **C7 5**: The new §9.4 paragraph and incorporated shared scope statement satisfy bennett-4ht: native host code remains native, device roots retain separate certificate scopes, and the CC wrapper makes the heterogeneous slot reachable. Remaining mixed-launch and host-memory obligations are explicitly identified without removing capabilities. *Change:* None required; retain the distinction between the existing device CC launch and the remaining general mixed-launch contract.
- **C8 5**: The revised rules determine fragment normalization, bit order, binding and reversal. INDEX supplies the common context vocabulary and publication caveat. The note accurately limits its validation claims and preserves existing schemas outside interface slots. *Change:* Optional clarification in Release and route: “Updated consumers accept both B5 alternatives; producers require support for this repair before emitting fragments and must never substitute a false homogeneous record for an unsupported heterogeneous vector.”

Suggestions:
1. Conformance vectors: add the failed sliced-view binding case specified under C6, with expected fault code 4 and unchanged viewed/live states before reversal. This strengthens coverage of the new atomic preflight obligation.
2. Release and route: add “Updated consumers accept both B5 alternatives; producers require support for this repair before emitting fragments and must never substitute a false homogeneous record for an unsupported heterogeneous vector.”
