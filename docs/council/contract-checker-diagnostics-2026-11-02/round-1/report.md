# Council — contract-checker-diagnostics-2026-11-02 round 1

Document snapshot sha256 c6c590967a57; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 5 | 5 | 5.0 |  |
| C6 | 4 | 5 | 4.5 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 4 | 4 | 4.0 |  |

Overall mean: 4.81

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Blocking issues

- none

## sol

Accept the optional editorial clarification. No false technical premise or misnumbered cited clause was found. Mandatory verdicts, K55 diagnostics and validation stages remain intact; canonical-byte rules and catalog identity remain unchanged.

**Path to accept:** Already acceptable. To raise C6 from 4 to 5, publish the valid baseline certificate and the two isolated A/B mutations with the stated rejection expectations.

- **C1 5**: The §12.3 addition concerns checker diagnostics only; it changes no machine state or transition rule. *Change:* None required; retain §3 unchanged.
- **C2 5**: No instruction, operand, well-formedness condition or cost hook changes. *Change:* None required; retain §4 unchanged.
- **C3 5**: The proposal correctly distinguishes checker rejection from §5.4 fault outcomes and §10 API statuses. Its diagnostic convention cannot change the oracle map. *Change:* None required; retain the proposed §12.3 rule that diagnostic spelling does not alter verdicts or executor status/fault codes.
- **C4 5**: The explicit exception preserves §11's E_SCHEDULE_INFEASIBLE obligations and K55's diagnostic and validation stages. Target matching and accounting remain unchanged. *Change:* None required; retain §11 K55 unchanged.
- **C5 5**: §12 contains no E_CERT registry. The addition preserves existing certificate schemas and mandatory rejection rules. §9.2 identity inputs and §11.1 catalog bytes are untouched; independently recomputing the 219-recipe catalog envelope reproduced the published hash. *Change:* None required; apply the addition without changing certificate fields, versions or canonical encodings.
- **C6 4**: A's rejection follows directly from §12.1 K13's mandatory explicit expected relation; B's follows from §12.2 K71's uniqueness requirement. These are sound clause derivations, but A/B are descriptions rather than replayable fixtures. The note accurately discloses that no checker test was run. *Change:* In 'Conformance vectors and verification', state: 'Starting from an otherwise valid standalone exhaustive table certificate, A deletes expected; B duplicates a domain.bundles entry resolving to the same interface slot, retaining the invocation and table. A rejects under §12.1 K13; B rejects under §12.2 K71; neither has a mandated local diagnostic spelling.' Publish the baseline and both mutations.
- **C7 5**: North Star §§4.4/5.1 requires independently checkable certificates and honest verification labels, not universally spelled checker diagnostics. No promised capability or demo rung is narrowed. *Change:* None required; retain the distinction between independent verification and optional diagnostic interoperability.
- **C8 4**: The proposed exception for mandated diagnostics is clear and implementable. The note could more explicitly distinguish its SHOULD reporting guidance from existing mandatory §12.2 report obligations and portable conformance assertions. *Change:* Append to §12.3: 'This diagnostic convention does not relax §12.2's mandatory claim-report bindings, proof/evidence outcomes, or unchecked (host limit) reporting.'

Suggestions:
1. Note, 'Conformance vectors and verification': replace 'assert rejection and the normative clause' with 'Portable tests assert the required rejection verdict; if clause/location reporting is supplied, validate it. Checker-specific tests may additionally assert documented local codes.' This avoids turning the proposed SHOULD into an unstated portable MUST.
2. §12.3: add 'This diagnostic convention does not relax §12.2's mandatory claim-report bindings, proof/evidence outcomes, or unchecked (host limit) reporting.' Expected boundary: a legal claim that exceeds host capacity remains unchecked (host limit), rather than becoming a domain rejection.
3. Note, 'Alternatives and concrete witness': publish an otherwise valid baseline table certificate and two independent mutations: A removes expected; B duplicates one resolved interface component in its domain. Expected results are rejection under §12.1 K13 and §12.2 K71 respectively; local code spelling remains unconstrained.

## codex

Accept. The proposal correctly leaves unmandated diagnostic spellings local while preserving rejection verdicts and mandated schedule diagnostics. Canonical bytes and hashes need no migration. The K71 citation is an editorial error, not a semantic blocker.

**Path to accept:** Already acceptable as an editorial clarification. Correcting the K71 attribution to K72 would raise C8 from 4 to 5.

- **C1 5**: The §12.3 addition changes no machine state or transition. Its separation of checker diagnostics, §10 statuses and §5.4 fault outcomes matches the published interfaces. *Change:* None required.
- **C2 5**: No instruction, operand rule, cost hook or program fault code changes. *Change:* None required.
- **C3 5**: Diagnostic spelling cannot alter the specified verdict or executor outcome. The proposal introduces no coherent-control, reversibility or phase-semantic change. *Change:* None required.
- **C4 5**: The explicit exception preserves §11's E_SCHEDULE_INFEASIBLE requirement and K55's diagnostic and validation stages. Resource accounting and target matching remain unchanged. *Change:* None required.
- **C5 5**: §12 contains no global E_CERT registry. Local code ownership is compatible with existing certificate obligations. The addition changes no serialized artifact or hashing rule; the 219-recipe catalog's envelope hash was independently recomputed and matches §11.1. *Change:* None required.
- **C6 5**: K13 requires an explicit expected relation, and §12.2's domain-validity rule rejects repeated resolved components. Both negative verdicts follow directly from the text. The note correctly disclaims having run checker tests. *Change:* None required.
- **C7 5**: North Star §§4.4 and 5.1 require independent certificate checking and honest proof/evidence distinctions, without prescribing universal rejection-code spellings. No promised capability is narrowed. *Change:* None required.
- **C8 4**: The clarification is implementable, but the witness misattributes duplicate-component rejection to K71. The §0.2 catalog assigns that rule to K72 DOMAIN-VALIDITY; K71 concerns omitted-zero slices. *Change:* In 'Alternatives and concrete witness', replace the attribution with: 'K13 requires A to reject; §12.2 K72 requires B to reject.'

Suggestions:
1. In 'Alternatives and concrete witness', state: 'K13 requires A to reject; §12.2 K72 requires B to reject.' K71 is the wrong identifier, although the cited §12.2 contains the required rule. For B, specify a repeated resolved interface component or region-cell index; repeated borrowed labels alone are permitted by K70.
2. Optionally append to the proposed §12.3 paragraph: 'This convention does not modify §12.2’s required checker-report outcomes, claim identification and coverage information, or its distinct unchecked (host limit) outcome.' K74/K75 already impose these obligations; only the additional rejection-diagnostic convention is discretionary.
3. In 'Conformance vectors and verification', state: 'Portable tests assert the specified rejection and any explicitly mandated diagnostic; clause/location output and local-code assertions otherwise follow the checker’s documented reporting contract.' This keeps the proposed SHOULD-level reporting guidance from becoming an unintended mandatory conformance requirement.
