# Council — td-0h4-2026-11-02 round 1

Document snapshot sha256 9af5f6d7a540; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 5 | 5 | 5.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 4 | 4 | 4.0 |  |

Overall mean: 4.75

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Blocking issues

- none

## sol

Accept both the disposition and optional strengthening. Current ISA 0.9 §4.1/K17 already fixes the claimed outcome mapping and consumption rules; 0.8 §4.1 does not. The optional formula is equivalent, its expected values are correct, and it changes no executable semantics or ISA-defined hashes. Agreement assumes a common quantum state and supplied draw stream; unsupplied PRNG identity is correctly excluded. No false normative premise or misquoted or misnumbered clause was found.

**Path to accept:** No blocking changes are required. To raise C6 from 4 to 5, publish the already-reproduced single-H boundary cases as durable conformance data with explicit binary64 encodings, exact-reference hypotheses and the existing 0.8 carrier limitation.

- **C1 5**: ISA 0.9 §4.1 explicitly fixes FIFO consumption, deterministic measurements, failed preconditions, wire-first ordering and the strict threshold. Combined with §14.2, it determines the note's sequential conditional measurements. *Change:* Optional, §4.1: add “Multiplying every outcome weight by the same positive factor leaves the selected outcome unchanged.”
- **C2 5**: One joint measure consumes one draw because §4.1 assigns one draw per executed measurement instruction. The note preserves §3.3's width, ownership and view preconditions. *Change:* Optional, §15: add “Measuring a fresh deterministic zero register and then H|0> with draws 0.75,0.25 returns integers 0,0.”
- **C3 5**: The proposed interval C_(j-1) <= uT < C_j is exactly equivalent to selecting the first cumulative weight strictly greater than uT. Zero-weight intervals are empty; u=0 selects the first supported outcome. The conditional residual-state formula agrees with projective measurement in §14.2. *Change:* Optional, §4.1: add “At draw zero, select the first outcome with positive weight.”
- **C4 5**: The optional strengthening changes no resource, capability, target or approximation contract. The displayed H boundaries are correct for the exact reference H defined in §4.4. *Change:* Optional, §15: add “The stated endpoint outcomes use exact reference gate realizations, with epsilon zero.”
- **C5 5**: The three patch hunks affect only prose in §0.2, §4.1 and §15. Existing fenced examples and hash literals remain unchanged. The §11.1 catalog envelope independently reproduces 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197; §9.2 hashes no Markdown publication prose. *Change:* Optional, note's “Exact proposed 0.9 diff”: add “The Markdown publication digest changes; canonical executable object bytes, catalog bytes and their ISA-defined hashes do not.”
- **C6 4**: Independently replayed all 28 stored draw vectors, the published K17 carrier and seven CLI rejection vectors successfully. The embedded probe matches its scratch script. The note accurately disclaims 0.9 interpreter admission and unexecuted retry, loop and width coverage; the additional vectors remain outside durable conformance fixtures. *Change:* Publish a durable boundary fixture and state in §15: “For exact H|0>, binary64 draw tokens 0.49999999999999994, 0.5 and 0.5000000000000001 produce bits 0,1,1 and integers 0,1,1.” Keep its 0.8 execution-carrier status explicit.
- **C7 5**: No north-star capability is narrowed. The change preserves device measurement and classical feedback without changing object, launch or host-memory contracts; native host code plus marked device modules remains reachable. The 0.8 comparison, K17 numbering and ratification quotations are accurate. *Change:* Optional, note's north-star paragraph: add “In a mixed fat object, this rule governs device measurements, whose classical results remain available through the existing launch result interface.”
- **C8 4**: The disposition clearly separates normative K17 semantics from binary64 parsing, generator defaults and historical consumer reports. The remaining presentation weakness is §15's “immediately below/above” wording without an explicit draw representation in that paragraph. *Change:* In the optional §15 addition, replace “draws immediately below, exactly at and immediately above 0.5” with “binary64 draws spelled 0.49999999999999994, 0.5 and 0.5000000000000001”; state that this encoding describes the vector rather than restricting all ISA draws to binary64.

Suggestions:
1. §15: identify exact-reference hypotheses and concrete vector encodings: “For exact H|0> with epsilon zero, binary64 draw tokens 0.49999999999999994, 0.5 and 0.5000000000000001 return 0,1,1. This binary64 encoding is a fixture convention.” Publish those cases as durable data while retaining the disclosed 0.8 carrier limitation. This avoids treating identical supplied draws as a guarantee of identical outcomes after different permitted approximate gate realizations.
2. Note, “Conformance vectors and consumer impact”: replace “All draws in this table have exact binary64 representations except the explicit parsing vector” with “Except for the deliberate parsing witness, the tokens are round-trip decimal spellings of the intended binary64 draws; comparisons use their exact dyadic values.” For example, 0.49999999999999994 denotes 1/2 − 2^-54 after parsing; the decimal numeral itself is not that exact dyadic rational.
3. Note, paragraph beginning “The interval length”: state the sampling hypothesis explicitly: “With u uniformly distributed over the real interval [0,1), each selection interval has probability w_s/T, and changing only endpoint assignments preserves the Born distribution.” Endpoint conventions can change finite-grid PRNG frequencies, so the probability statement should not be read as an exact claim about every binary64 generator.

## codex

Accept the disposition and optional strengthening. Current 0.9 K17 already decides the stated mapping and consumption cases; 0.8 does not. The added intervals and conditional-state wording preserve existing semantics and artifact hashes. No misquoted or misnumbered normative clause was found.

**Path to accept:** Already acceptable. Making the proposed §15 boundary values and expected outputs explicit would raise C6 from 4 to 5; correcting the decimal-spelling sentence would similarly improve C8.

- **C1 5**: 0.9 §4.1 explicitly requires FIFO consumption, one draw per executed measurement including deterministic states, and no consumption on failed preconditions. With identical pre-measurement weights and supplied draws, its strict cumulative comparison uniquely determines the outcome. *Change:* None required.
- **C2 5**: The proposed interval C_(j-1) <= u*T < C_j is equivalent to §4.1's first cumulative weight strictly exceeding u*T. Zero-weight intervals are empty; u=0 selects the first supported outcome; u=1 is excluded. Wire-first ordering gives integer values 0,2,1,3 for 00,01,10,11. *Change:* None required.
- **C3 5**: §14.2 specifies projective computational-basis measurement, so subsequent measurements use the conditional state. Scaling an unnormalized state cancels through u*T. The independent-register and Bell-pair examples are correct. The additions preserve measurement restrictions and reversal eligibility. *Change:* None required.
- **C4 5**: The optional diff changes only §§0.2, 4.1 and 15. It introduces no resource, target, scheduling or gate-realization decision. *Change:* None required.
- **C5 5**: The three diff hunks apply exactly in memory. They change no canonical object text, signature, version, catalog or hash-definition input under §§8.1, 9.2 and 11.1. The catalog envelope independently recomputes to the published 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. The Markdown document checksum changes, as expected. *Change:* None required.
- **C6 4**: §§4.1 and 14.2 support the derivation and all listed expected outcomes. Read-only replay using the existing reference binary passed the 28 stored vectors, published K17 carrier and seven CLI rejection cases; both cached measurement tests passed. The proposed §15 phrase 'immediately below' needs a representation or explicit values. *Change:* In the proposed §15 addition, replace the first sentence with: "Suite A shall include exact-state H|0> vectors at draws 1/2 - 2^-54, 1/2, and 1/2 + 2^-53, returning bits 0, 1, and 1 respectively."
- **C7 5**: No North Star capability is narrowed. The change preserves classical feedback and the native-host/device split; it imposes no whole-binary object, launch or certificate requirement. The mixed fat object remains reachable. *Change:* None required.
- **C8 4**: The quotations and numbering are correct: 0.8 §4.1 lacks the mapping, while 0.9 §4.1, K17 and Decided confirmations contain it. CLI parsing, PRNG and seed conventions are appropriately distinguished from universal ISA requirements. The table introduction loosely calls rounded decimal spellings exactly representable. *Change:* In 'Conformance vectors and consumer impact', replace the two introductory sentences with: "Except for the explicit parsing witness, decimal tokens are round-trip spellings of the intended binary64 draws; comparison uses the exact dyadic value obtained after parsing."

Suggestions:
1. Proposed §15: replace 'immediately below, exactly at and immediately above 0.5' with the explicit exact-state vectors u = 1/2 - 2^-54, 1/2, 1/2 + 2^-53 and expected bits 0,1,1. Phrase this as a suite requirement so it does not imply that new fixtures have already been published.
2. Note, 'Conformance vectors and consumer impact': state that the decimal tokens are round-trip spellings of binary64 draws, rather than themselves exactly representable decimals. For example, 0.49999999999999994 parses to exactly 1/2 - 2^-54 and returns 0; 0.49999999999999999 parses to exactly 1/2 and returns 1.
