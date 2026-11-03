# Council — derive3-brt-vbi-2026-11-02 round 1

Document snapshot sha256 d89e0f5c3376; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 4 | 4 | 4.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 4 | 4 | 4.0 |  |

Overall mean: 4.62

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Blocking issues

- none

## sol

The delivery gap and missing-body witness are real, the cited clauses are accurate, and the proposed fixed point repairs the gap without narrowing arithmetic or mixed-object scope. Hash consequences are correctly distinguished from unchanged ISA catalog identity. No blocking defect found.

**Path to accept:** Already acceptable through the recommended next-patch dialect publication route, mirrored in the 0.3 draft. To raise C5 from 4 to 5, resolve the manifest’s non-function export wording using the concrete v1 rule above.

- **C1 5**: Both tracks’ §§12.7–12.8 retain the existing integer representation, partial top limb and shadow-stack conventions. The proposal changes delivery, not machine state or stepping. *Change:* No repair required. Retain §12.8’s sentence: “The existing shadow-stack slot layout, partial top limb and push/store/call/load/pop order are unchanged.”
- **C2 5**: The operation list matches the cited runtime-producing rows; the W>128 and overflow W>64 thresholds match those rows. The i257 result 6, ctpop(result)=2 and ctpop(a)=3 are correct. LLVM permits ctpop on arbitrary integer types with a matching result type. [LLVM 18 LangRef](https://releases.llvm.org/18.1.8/docs/LangRef.html#llvm-ctpop-intrinsic) *Change:* Optional §12.8 clarification: “Requests select existing helper ABIs; they do not replace the distinct scalar, wide-slot and overflow-result conventions of the preceding rows.”
- **C3 5**: Discovery does not emit or reorder normalisation. Linking the same complete closure into both builds preserves the materialised reference semantics, including fault and cleanup obligations; generation failure cannot become a device fault. *Change:* No repair required. Retain §12.8’s rule: “This discovery is a non-emitting analysis using the published rules; it does not rerun or change §12.1’s normative rule order.”
- **C4 5**: Generated bodies remain charged ordinary code. The note correctly requires fresh materialisation, resource and certificate bindings. No ISA instruction or ref recipe changes; I reproduced the published ref@0.9 envelope hash 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. *Change:* Optional §12.8 sentence: “Generated bodies and their dependencies incur the existing step, heap, stack and recursion charges, including their shadow-stack operations.”
- **C5 4**: The missing public runtime delivery protocol is real; §13.1 supplies the analogous arith protocol. Requests, validation, reproducibility and closure completeness are substantially decided. One manifest detail needs tightening: an externally visible data definition has no function_type. *Change:* §12.8 OUTPUT_JSON: state “exports lists every externally visible function definition; generated non-function definitions MUST have internal or private linkage.” Alternatively add versioned kind/type records for data exports; prefer internal data for v1.
- **C6 4**: I reproduced successful LLVM 18/23 verification and absence of both required i257 definitions in both current distributions. The note accurately limits this evidence to delivery. The arithmetic and canonical request hash also reproduce; helper execution remains future conformance work. *Change:* Conformance vectors: add “DN MUST check the INDEX canonical request against SHA-256 74e7a75be203bc350a18a84980258fa09a3e9936837e8aa67fb01532064cdd81; integration tests MUST execute the generated i257 closure in both materialised builds and obtain product 6, ctpop(product) 2 and ctpop(a) 3.”
- **C7 5**: All admitted widths remain obligations. The mixed-object section limits collection and comparison to marked device closures, preserves separate root certificate associations and explicitly names the remaining mixed-launch work. The standing bennett-4ht check passes. *Change:* No repair required. Retain the mixed-object rule: “Multiple roots may share generated bodies; each device root retains its own certificate/context association.”
- **C8 4**: The offline interface and fixed-point procedure are implementable without producer-private knowledge. Treatment of instances already supplied by the base runtime could be stated directly to avoid unnecessary duplicate definitions. *Change:* §12.8 collection: add “An already linked conforming definition satisfies its instance; request only unsatisfied instances, and recompute that set after linking each response.”

Suggestions:
1. §12.8 OUTPUT_JSON: state “exports lists every externally visible function definition; generated non-function definitions MUST have internal or private linkage.” A versioned manifest supporting typed data exports is also viable; prefer internal data for v1.
2. §19.9 build record: add “Record each instance producer’s version, canonical request hash, bitcode hash and manifest hash; use an empty instance list when no generated module is linked.” This makes the note’s cache and repinning requirements directly auditable.
3. §12.8 collection: add “An already linked conforming definition satisfies its instance; request only unsatisfied instances, and recompute that set after linking each response.”
4. K entry and publication route: state “Publish in the next available full 0.2 patch version and carry the matching protocol into the 0.3 draft; update version checks and consumer pins.” The workspace advanced to 0.2.13 during review, so a separate subsequent publication would use the next patch. The proposed route already permits this; no ISA K entry is needed.

## codex

Accept. The delivery gap and missing i257 definitions are verified, the proposed fixed point preserves normalisation semantics, and mixed execution remains reachable. Hash consequences and the publication route are sound. Acceptance authorises the contract repair, not closure of brt-vbi/brt-zct implementation work.

**Path to accept:** No blocking changes are required. Apply through the recommended next 0.2 patch and corresponding 0.3 draft publication, preserving each track's ISA target; no ISA K entry is needed. To raise C6 from 4 to 5, promote the verified canonical request and arithmetic expectations into tagged normative fixtures.

- **C1 5**: Within this proposal's scope, the machine model is unchanged. Helpers remain ordinary materialised code under dialect §§12.1, 16 and 18; the delivery protocol adds no execution tier or primitive. *Change:* None required.
- **C2 5**: The operation list matches the runtime-backed rows of §§12.7–12.8 in both tracks. W>128 for ordinary arithmetic helpers and W>64 for multiplication-overflow helpers are correct. Arbitrary-width ctpop is also supported by the [LLVM 18 LangRef](https://releases.llvm.org/18.1.8/docs/LangRef.html#llvm-ctpop-intrinsic). *Change:* None required.
- **C3 5**: The diff preserves existing fault behavior, full-width count results, partial top limbs and slot ordering. Its non-emitting discovery explicitly preserves §12.1's rule order and repeated N22 applications. Requiring identical resolved bodies in both builds prevents comparison against a different implementation. *Change:* None required.
- **C4 5**: Major, triple and DataLayout are request-bound and checked. Ordinary helper rows retain §9.4's budget charges and §17.3's shadow-stack accounting. The note correctly acknowledges changed costs and dependent bindings without proposing an ISA ref@0.9 recipe change. *Change:* None required.
- **C5 4**: The delivery gap is real: §13.1 publishes an arith protocol, while §§12.7–12.8 and 19.1 provide no corresponding runtime-integer protocol. The proposed request canonicalisation, hashes and closure obligation repair it. JCS is an appropriate existing encoding ([RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html)). Generated-input provenance could be integrated more explicitly into the existing build record. *Change:* In the proposed §19.1 addition, state: "The §19.9 build record MUST identify each instance producer and version and record each canonical request hash and generated bitcode hash alongside the resolved base-runtime and arith hashes."
- **C6 4**: I reproduced successful LLVM 18/23 verification and both missing-definition assertions against the current runtime publications. Their hashes differ from INDEX's historical evidence pins, but the finding remains true. The arithmetic vector and INDEX's request digest also reproduce. The note correctly distinguishes these checks from execution of delivered helpers. *Change:* Under Conformance vectors, publish a tagged request fixture using INDEX's exact canonical bytes, with expected SHA-256 74e7a75be203bc350a18a84980258fa09a3e9936837e8aa67fb01532064cdd81, and a result fixture requiring product limbs [6,0,0,0,0], ctpop(product) limbs [2,0,0,0,0], and ctpop(a) limbs [3,0,0,0,0]. State: "Duplicate or reordered entries MUST reproduce this canonical request and digest."
- **C7 5**: The proposal preserves all admitted widths and treats missing generation as unfinished implementation, not a program fault. Its §19.1 addition and Mixed fat object section retain native host code, marked device closures, per-root certificates and closure-specific native comparison. The standing mixed-object check passes. *Change:* None required in the proposed diff.
- **C8 4**: The executable interface, completion semantics, dependency fixed point and restart rule are implementable. One small manifest ambiguity remains: 'every externally visible definition' includes LLVM data definitions, whereas function_type describes functions only. Function-only generated exports provide a straightforward conforming implementation. *Change:* In §12.8's OUTPUT_JSON paragraph, state: "For v1, exports inventories externally visible function definitions; generated implementation data has internal or private linkage, and shared runtime data is imported from the published base distribution." Alternatively add a tagged function/data export schema; I would use the function-only default.

Suggestions:
1. Proposed §19.1/build provenance: add "The §19.9 build record MUST identify each instance producer and version and record each canonical request hash and generated bitcode hash alongside the resolved base-runtime and arith hashes." This makes the note's repinning requirement directly actionable.
2. Proposed §12.8/OUTPUT_JSON: add "For v1, exports inventories externally visible function definitions; generated implementation data has internal or private linkage, and shared runtime data is imported from the published base distribution." A tagged function/data schema is also viable; prefer the simpler function-only default.
3. Conformance vectors: promote INDEX's canonical request into a tagged fixture with digest 74e7a75be203bc350a18a84980258fa09a3e9936837e8aa67fb01532064cdd81. Require reordered and duplicate entries to yield those same bytes. For a=2^256+3 and b=2, require product [6,0,0,0,0], ctpop(product) [2,0,0,0,0], and ctpop(a) [3,0,0,0,0].
4. Mixed fat object/shared background note: its certificate-table assertion that current text does not explicitly delimit native inventory is stale against current ISA §12.3 K85. Replace it with: "ISA §12.3 K85 already scopes fixed-image certificate inventory and native comparison to the selected marked closure; general container association and mixed-launch memory/lifetime bindings remain outstanding." This concerns the background note, not brt-vbi's delivery defect.
