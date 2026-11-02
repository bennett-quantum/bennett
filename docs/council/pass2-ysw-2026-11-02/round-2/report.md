# Council — pass2-ysw-2026-11-02 round 2

Document snapshot sha256 8596c7bf9d22; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 4 | 4 | 4.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 4 | 5 | 4.5 |  |

Overall mean: 4.69

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Previous-round blockers, status

- [sol] sol:B1: **resolved** — The normative fat-object paragraph and incorporated shared statement supply device scope, certificate inventory and launch-feature negotiation obligations.
- [sol] codex:B1: **resolved** — Oracle-only primary-token ordering and corrected action/CC/R defaults agree with §§4.7/16.2.
- [sol] codex:B2: **resolved** — Bindings are scoped to loaded device objects and roots; native main, argv/envp and host-only libc remain outside the device inventory.
- [codex] sol B1: **resolved** — The proposed §§10/12.3 paragraph and shared scope statement supply device-module boundaries, alias negotiation responsibility and certificate inventory.
- [codex] codex B1: **resolved** — Only oracle invocations prepend a token; action/perm_action/CC/R ordering and both legacy defaults now agree with §4.7.
- [codex] codex B2: **resolved** — Mixed execution explicitly retains native host code and scopes alias bindings to selected device roots and invocations.

## Blocking issues

- none

## sol

All previous blockers are resolved: codex B1 by the corrected token ordering/defaults, and sol B1 plus codex B2 by the mixed-object scope additions. No false cited premise, misnumbered clause or new S0 issue was found. Hash/catalog claims hold under the stated publication conditions. The finite checker passes; actual history and K81 execution are not claimed as reproduced tests.

**Path to accept:** No blocking changes are required. To raise C5 from 4 to 5, render the universal-claim token_aliases shorthand explicitly in §12.3 while retaining its stated quantification over all consistent partitions.

- **C1 5**: The partition records equality without replacing live token identities or changing §5.4 validity and lifetime rules. Nested partitions retain their resolved identity mapping. *Change:* Optional §3.2 cross-reference: “Invocation bindings export token equality through token_aliases (§12.3); these labels are not runtime token handles.”
- **C2 5**: The revised ordering agrees with §§4.7/16.2: only oracle_call supplies a separate invocation token. The token-free action and oracle defaults are correct. *Change:* Optional §4.1 budget.mint annotation: “Serialization of token_aliases neither creates a token nor changes token validity.”
- **C3 5**: The defect is real: §5.3 compares identities and tuples; §§4.1/7.4 compare recorded boundary values. Preserving identities through forwarding, captures and inverse traversal repairs serialization without changing quantum semantics. *Change:* Clarify the §7.4 region-call frame row: “Retain the resolved token identity mapping alongside token tuples, and reuse that mapping during reversal.”
- **C4 5**: Partition-aware schedule selection preserves §10.1 exact aggregation. The revised inverse-pair example correctly rejects raising the primary budget while retaining an equal-label argument at the old tuple. *Change:* Optional §10.1 sentence: “Resolve cleanup pairs and the scheduled event stream using args, budget and token_aliases before exact resource aggregation.”
- **C5 4**: Invocation, schedule, cache, claim and inverse-pair bindings are covered. The additive ABI supports every consistent partition, with an explicit legacy E_ARG default. The remaining universal-claim encoding detail is mechanical; its quantification is decided. *Change:* In §12.3, give the uniform shorthand explicitly: “A parameter-uniform structural claim uses invocation:{args:"all",budget:"all",token_aliases:"all"}; token_aliases:"all" quantifies over every partition consistent with each quantified argument vector and budget.”
- **C6 4**: check_rev2.py completed successfully with all eight PASS lines. Independent hashing confirmed the originating fixture pin and args digest bf8eae8d885943f1948223391b24a677ec8eaefc4d39544bd6ed106277a211ed. History execution and K81 carrier formation remain disclosed, hand-derived witnesses. *Change:* In Conformance vectors/§15, make the Q witness executable: “For oracle_call @identity a (x) t f () () followed by oracle_call @identity b (x) t f () (), action partition [0,0] produces one K65 carrier at the second call; [0,1] produces none. Both compose to identity at equal tuples.”
- **C7 5**: Every consistent partition remains admitted. Fat-object applicability and the incorporated shared statement delimit device roots, native inventory and the exact remaining launch/memory obligations, satisfying bennett-4ht without claiming an existing mixed-launch shim. *Change:* Optional §9.2 cross-reference: “For mixed native/device containers, token-alias bindings and certificates are scoped to the selected device object/root under §§10/12.3.”
- **C8 4**: Canonical labels, arity, tuple consistency, forwarding, fresh mints and legacy behavior are implementable. Publication conditions correctly distinguish unchanged source/catalog envelopes from changed schedule/certificate bytes and full-version migration. *Change:* Update §5.4's existing schedule-selection sentence directly: “An invocation uses the bound schedule only when closure hash, variant, inherited controls, budget tuple, params_hash and token_aliases all match; otherwise it uses the §11 defaults.”

Suggestions:
1. Recommended exact spec diff, §12.3: explicitly encode the already-required universal partition quantification as invocation:{args:"all",budget:"all",token_aliases:"all"}, restricted to consistent partitions. This is schema completion, not an unresolved semantic choice.
2. Recommended exact spec diff, §§5.4/7.4: replace the old schedule-matching checklist with one including token_aliases, and state that region-call history retains the identity mapping for reversal. The proposal's general obligations already require both behaviors.
3. Conformance vectors/check_rev2.py: add an integration test for the two identity-oracle calls. Expected action partitions are [0,0] and [0,1], with respectively one carrier at the second call and no carrier. Replay of a certificate bound to the other partition must reject despite identical params_hash.

## codex

sol B1, codex B1 and codex B2 are resolved. No new S0 issue, false technical premise or material clause miscitation was found. The identity defect is real, the repair preserves source semantics and mixed-object scope, and hash preservation is correctly conditional on the publication route.

**Path to accept:** No blocking changes remain. To raise C6 from 4 to 5, publish the complete Q witness with pinned source coordinates and expected carrier records, alongside the existing partition/hash checks.

- **C1 5**: The partition preserves §§3.2/5.4 token identity, validity and freshness. Context-local labels do not become globally interchangeable identities. *Change:* No required change. Retain the Recommended exact spec diff rule: “Equal local label numbers in two contexts do not by themselves denote one global token.”
- **C2 5**: The revised ordering agrees with §§4.7/16.2: only oracle_call has a separate invocation token. Token-free actions correctly use [], and source instruction signatures remain unchanged. *Change:* In Recommended exact spec diff, add: “This amendment changes invocation metadata, not the operand lists of oracle_call, action_call, call or uncall.”
- **C3 5**: The defect is real: §5.3 explicitly compares token identities and tuples, §5.4 creates fresh tokens, and §7.4 compares recorded boundary values. Identity preservation through forwarding, captures and inverse traversal repairs the distinction without inspecting quantum data. *Change:* For clarity, amend the §7.4 region-call history row: “The frame retains resolved token identities as well as tuples; reversal reuses those identities.”
- **C4 5**: Alias-sensitive schedule matching identifies the correct K81 partition before K65 selection. Target accounting and K12 exact rational aggregation remain unchanged; a bound across partitions is correctly excluded from exact-request results. *Change:* In §10.1, add: “Requests with equal arguments and budgets but unequal token_aliases are distinct requests, even when their resource totals happen to agree.”
- **C5 4**: The additive ABI, explicit legacy E_ARG default, nested identity mapping and inverse-pair coverage obligations are sufficient. K24/K77 correctly remain tuple-encoded channels with additional source-binding metadata. Publication and consumer migration are explicitly conditional on the authorized version route. *Change:* In §12.3, make the universal encoding explicit: “A parameter-uniform structural invocation uses token_aliases: "all"; its checker quantifies over every canonical partition consistent with each quantified argument vector and budget.”
- **C6 4**: check_rev2.py returned all eight PASS lines. The 0.9 debug CLI admitted the originating fixture and reproduced object_hash cda0f55ff3f299b165453ff9162b051ddf96856a799d22e09499c226bf35c011. The CC step counts and Q carrier consequences agree with §§7.4/11, but remain derivations rather than token-sensitive executor tests. *Change:* In Conformance vectors/§15, publish a complete action fixture containing “oracle_call @identity a (x) t f () (); oracle_call @identity b (x) t f () ()”, with both tokens at (1,0,0,0). State: “Both partitions preserve the complete input tuple; [0,0] produces a K65 carrier at entry:1, generated 0, while [0,1] produces no matched-call carrier.”
- **C7 5**: Fat-object applicability and the incorporated shared statement identify device roots, linked closures, native exclusions and exact remaining mixed-launch obligations. Every consistent alias partition remains supported through the new interface; no North Star capability is removed. *Change:* No required change. Retain in §§10/12.3: “Alias-bearing schedules and certificates bind that device object/root and invocation.”
- **C8 5**: Canonical ordering, validation, defaults and propagation are explicit. The inverse-pair example correctly distinguishes tuple inconsistency from a changed partition. Hash claims agree with §9.2 and INDEX's publication caveat; the published ref catalog envelope was independently reproduced. *Change:* In Hashes, catalog and consumers, add: “If only schedule/certificate sections change and header/source bytes remain fixed, object_hash remains unchanged because §9.2 excludes those sections; changing header versions requires recomputing object_hash and downstream bindings.”

Suggestions:
1. In §12.3, specify the encoding already implied by universal proof semantics: “A parameter-uniform structural invocation uses token_aliases: "all" and quantifies over every tuple-consistent canonical partition.” Concrete invocations continue to use arrays.
2. In Conformance vectors/§15, publish the complete memoryless identity-oracle/action fixture with a,b at (1,0,0,0). Require unchanged x,t,f for both partitions, a sole matched-call carrier at entry:1/generated:0 for [0,0], and none for [0,1]. This makes the existing prose witness directly consumable by independent implementations.
3. In Hashes, catalog and consumers, state: “Schedule/certificate-only changes preserve object_hash under unchanged header/source bytes; changing any header version requires recomputing object_hash and downstream bindings.”
