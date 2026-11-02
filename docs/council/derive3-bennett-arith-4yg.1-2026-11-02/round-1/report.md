# Council — derive3-bennett-arith-4yg.1-2026-11-02 round 1

Document snapshot sha256 1faab512ffcf; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

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

## Blocking issues

- none

## sol

The cited defect is real, both exact witnesses and flag claims check out, and the proposed parity rule repairs it deterministically. No S0 issue remains. Publication must use the recommended versioned route; metadata and example-format corrections are discretionary improvements.

**Path to accept:** Already acceptable through the recommended next full 0.2 version and corresponding 0.3-draft publication. Correcting the mapping-version sentence would raise C5 from 4 to 5.

- **C1 5**: Both tracks’ §13.1 define the quoted canonical pairs. The repair preserves that value set and supplies a deterministic decision between equidistant candidates. *Change:* Optional clarification in §13.1: “This tie rule does not change the set of canonical finite values.”
- **C2 5**: The proposed integer-significand definition handles normal, subnormal, zero and negative components. The high fallback covers two zero lows; the same-parity fallback completes the selection policy. *Change:* Optional cross-reference in §13.4’s nearest-side selection paragraph: “For PPC nearest-even ties, use §13.1’s candidate-pair parity rule.”
- **C3 5**: The selected results are deterministic classical functions implemented by linked integer bodies. Existing §13.1 final-rounding rules require exactly inexact=16 for both witnesses; neither rounded total is tiny. *Change:* Optional sentence after the normative witnesses: “Observed constrained invocations OR 16 into existing sticky flags; unconstrained invocations leave the floating-point environment unchanged.”
- **C4 5**: No target, resource-vector or scheduling interface changes. Revised helper bodies may change execution costs, consistently with the note’s requirement to replace affected object and certificate bindings. *Change:* Optional sentence in “Hashes, catalog and consumers”: “Recompute schedules and resource evidence affected by replaced helper bodies against their new object identities.”
- **C5 4**: The next-full-version publication route and consumer re-pinning are appropriate. I independently verified the published 219-recipe ref@0.9 envelope hash. However, “A dialect version change also changes mapping-version bindings” is false as a general requirement: §§16 and 23 version the lifting map separately; dialect 0.2.12 retains map 0.2.9. *Change:* In “Hashes, catalog and consumers”, replace that sentence with: “Bump the full dialect version and update affected consumer and build-record pins. Change dialect_mapping_version only if the §16 lifting map is separately revised; this numerical helper repair alone does not require that change.”
- **C6 4**: The bounded witness reproduced the reported LLVM 18/23 values and flags. Independent Fraction arithmetic confirmed both midpoints, the binary128 encoding, adjacency and inexactness. The note correctly distinguishes this evidence from arithmetic conformance, but the publication diff supplies prose witnesses without executable example tags. *Change:* In §13.6, register both witnesses as tagged DF examples with R=0, observed exceptions and initial flags zero: expected results are (0x3ff0000000000001,+0) and (0x0030000000000001,+0), respectively, with flags=16.
- **C7 5**: The repair preserves all formats and operation domains, restores deterministic numerical selection, and retains the demo ladder. The mixed-fat-object section explicitly limits revised helpers and certificates to device closures and binds native comparison to the same materialised bodies. *Change:* No change required; retain the mixed-fat-object statement and its explicit remaining boundary obligations.
- **C8 4**: The numerical rule is implementable without an additional normative decision. Editorial integration needs care: the replacement introduces several sentences inside an existing sentence, and §13.5’s flags are specified in prose, not a “flags table”. *Change:* In the final §13.1 paragraph, end “directed and nearest-away modes retain their specified rules” with a period, then state: “NaNs and infinities are represented in the high component with low +0.” In the note, replace “§13.5’s flags table” with “§13.5’s flags paragraph”.

Suggestions:
1. “Hashes, catalog and consumers”: correct the automatic mapping-version-change claim using the C5 replacement. Full dialect compatibility, lifting-map version and linked-body identities are separate bindings.
2. Recommended normative witness: begin “Both following vectors use nearest-even mode (R=0).” This makes the conversion’s mode explicit. For either positive midpoint, downward/toward-zero select the zero-low endpoint; upward/nearest-away select the +u endpoint. Every observed constrained case raises exactly 16.
3. Conformance vectors: add the tagged DF examples described under C6. For negative counterparts, nearest-even/upward/toward-zero return (-h,+0) or (-H,+0); downward/nearest-away return (-h,-u) or (-H,-u), with flags=16 throughout.
4. Conformance vectors: replace “Include a direct test of the equal-parity fallback” with “Directly exercise the selector’s equal-parity branch and require the smaller-absolute-value candidate; an end-to-end rounding vector must establish that its candidates are adjacent canonical values.” This tests the stated policy without presuming a reachable equal-parity boundary.

## codex

Accept. The numerical defect is real, both witnesses and incorrect native flags reproduce, and the proposed tie rule repairs the ambiguity without narrowing capability. The publication route and unchanged ISA catalog are appropriate. Correct the nonblocking claim that a dialect-version bump automatically changes the lifting-map binding.

**Path to accept:** No blocking changes are required. Apply through the recommended new full dialect version and matching draft amendment. Correcting the separately versioned mapping-binding claim would raise C5 from 4 to 5.

- **C1 5**: Both tracks have byte-identical §§13.1–13.5. The quoted parity rule and canonical-pair definition are accurate. Comparing both lows resolves the demonstrated odd/odd case. The smaller-magnitude fallback is deterministic: distinct adjacent numerical values cannot straddle zero because zero is representable. *Change:* Optional §13.1 clarification: “L and U denote distinct numerical sums with L < U; signed-zero encodings remain governed by the existing zero-sign rules.”
- **C2 5**: The repair preserves carriers, helper signatures and operation coverage. Incoming conversion and FMA are correctly identified as affected paths; §13.1 already gives explicit numerical guarantees priority over APFloat fallbacks. *Change:* Add to §13.1: “The nearest-even PPC tie rule also governs nearest-even selection for the constrained carrier transcendentals of §13.4.”
- **C3 5**: Both exact results are unrepresentable midpoints with normal rounded totals. Existing §§13.1 and 13.5 therefore require exactly inexact=16 for observed exceptions, independently of which nearest candidate wins. The repair changes a deterministic numerical function without changing its reversible embedding or cleanup obligations. *Change:* Extend the normative witness: “Negating each exact input value gives nearest-even results (-h,+0) and (-H,+0), respectively, again raising exactly inexact (16).”
- **C4 5**: No target, budget or resource-accounting rule changes. The ISA §11.1 catalog expands integer operations rather than selecting PPC results. Its 219-recipe envelope independently hashes to the published 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. *Change:* Add under “Hashes, catalog and consumers”: “Regenerate affected schedules and resource certificates against the new linked closures; the target schema and ref@0.9 catalog remain unchanged.”
- **C5 4**: The versioned 0.2 publication route, consumer re-pinning and changed-body proof invalidation are appropriate. One supporting premise is false: a full dialect-version change does not automatically change dialect_mapping_version. Maintained §§16, 19.9 and 23 explicitly separate dialect 0.2.12 from map 0.2.9; the draft separately specifies map 0.3. This does not invalidate the numerical diff. *Change:* Replace the mapping-version sentence in “Hashes, catalog and consumers” with: “The full dialect compatibility version and consumer pins change. dialect_mapping_version remains the separately declared lifting-map version—0.2.9 on the maintained track and 0.3 in the current draft—unless §§16 and 19.9 explicitly revise that map version.”
- **C6 4**: The supplied witness exits 0 and reproduces both LLVM majors’ FMA flags 0 and conversion flags 24. Independent rational decoding confirms the FMA midpoint and the stated binary128 encoding. These establish the defect, not producer conformance. Broader acceptance vectors are specified but not supplied as executed conformance tests. *Change:* Add an executable two-zero-low witness under “Conformance vectors”: “For u=2^-1074, fma((u,+0),(1/2,+0),(+0,+0)) returns (+0,+0) in nearest-even mode and raises underflow|inexact (24) when exceptions are observed.”
- **C7 5**: The proposal preserves all format and input-domain obligations and restores deterministic numerical selection required by North Star §§3.2 and 5.1. Its mixed-fat-object statement and incorporated scope note preserve native host execution, closure-specific certificates and explicit remaining mixed-launch obligations. The standing check passes. *Change:* Optional addition to “Mixed fat object”: “Native entry points and host-only argv/envp preparation remain outside the device certificate inventory.”
- **C8 5**: The proposed rule defines integer significands, zero parity, sign handling, a deterministic fallback and preservation of other rounding modes. An implementer can implement the selection without another numerical decision. The replacement leaves awkward punctuation before the inherited NaN/inf clause, but no competing semantics. *Change:* End the replacement with: “Directed and nearest-away modes retain their specified rules. NaN and infinity are represented in the high component with low +0.” Remove the inherited “and NaN/inf represented…” fragment and retain the following overflow sentence.

Suggestions:
1. In “Hashes, catalog and consumers”, replace the automatic mapping-version claim with: “The full dialect compatibility version and consumer pins change; dialect_mapping_version changes only when the separately declared lifting-map version changes.” Retain map 0.2.9 and map 0.3 unless the publication explicitly amends their declarations and certificate bindings.
2. In “Conformance vectors”, supply executable mode expectations for both witnesses. With positive adjacent candidates L and U, the results for nearest-even/down/up/toward-zero/nearest-away are L/L/U/L/U; for the negated inputs they are -L/-U/-L/-L/-U. Each observed-exception case raises exactly 16; an initial unrelated sticky bit 32 therefore yields flags 48.
3. Replace “Include a direct test of the equal-parity fallback” with: “Test the equal-parity selector branch independently. Count such a test as an arithmetic conformance vector only when its candidates are shown to be adjacent canonical values.” This preserves the defensive policy without assuming that a reachable binary64 example exists.
4. In the exact diff, separate the inherited nonfinite clause into: “NaN and infinity are represented in the high component with low +0.” Keep the existing overflow and underflow sentences unchanged.
