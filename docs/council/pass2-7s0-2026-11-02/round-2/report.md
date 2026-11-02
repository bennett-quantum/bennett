# Council — pass2-7s0-2026-11-02 round 2

Document snapshot sha256 b04483b52ac0; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 4 | 5 | 4.5 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 5 | 5 | 5.0 |  |

Overall mean: 4.81

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Previous-round blockers, status

- [sol] sol:B1: **resolved** — Union-rank rejection sampling now fixes tuple selection and generator consumption; both published seeds select rank 2.
- [sol] sol:B2: **resolved** — The normative §12.3 attachment paragraph explicitly limits the inventory to the launched device closure.
- [sol] codex:B1: **resolved** — The revision defines union sampling, complete claimed B-fiber replays without random words, and primary-tuple coverage.
- [sol] codex:B2: **resolved** — Device objects, closure-relative occurrences and invocation contexts are bound explicitly; native host code requires no borrow-proof inventory.
- [codex] sol B1: **resolved** — Union-rank sampling fixes enumeration, rejection sampling, word consumption and distinct-primary coverage; the supplied seed selects rank 2 and rejects CX(c,b).
- [codex] sol B2: **resolved** — The normative §12.3 addition explicitly attaches borrow claims to device closures and excludes native host inventory.
- [codex] codex B1: **resolved** — The revision specifies complete claimed-domain B-fiber replays without additional random words; the second seed and its expected rejection reproduce.
- [codex] codex B2: **resolved** — Closure-relative occurrences, lifetimes, invocation contexts and default-covered calls are explicitly covered in mixed fat objects.

## Blocking issues

- none

## sol

All four round-1 blockers are resolved: sol B1/codex B1 by deterministic union sampling and fiber replay, and sol B2/codex B2 by the normative mixed-object attachment rule. The defect is real, the repair is sound, and no new S0 or regression was found. K69's inherited-control exception warrants a wording correction. Finite and catalog checks passed; no proposed-format checker implementation is claimed.

**Path to accept:** Already acceptable as the proposed authorized 0.9 K repair. To raise C6 from 4 to 5, give explicit expected outcomes for incomplete-domain vectors, distinguishing evidence from rejection of a requested proof.

- **C1 5**: The diff preserves §5.6 K76/K78: interface and borrowed values remain independent and full, allocated locals receive only normative entry facts, and repeated visits contribute a union. *Change:* No change required; retain K76/K78 unchanged.
- **C2 5**: No instruction semantics change. The CX examples agree with §4.4, and adjacent CX/MCX cancellation agrees with K78's primitive identity rule. *Change:* No change required.
- **C3 5**: Restoration of B, independence of complete non-B outputs, exact +1 phase, internal release checks and complete D_F coverage establish the restricted tensor relation. Linearity extends it to entangled reference systems. The frame-boundary exception correctly permits surviving nonzero locals. *Change:* No change required; preserve these hypotheses together.
- **C4 5**: Target and resource semantics remain unchanged. K75 supplies the existing unchecked outcome without imposing domain caps, and physical storage reuse does not merge logical lifetimes. *Change:* No change required.
- **C5 4**: The expressibility defect is real: §§12.1–12.3 provide neither exhaustive frame selection nor local entry components. The repair supplies those bindings, deterministic sampling and complete device-closure inventory obligations. Source-occurrence serialization remains schematic. *Change:* In Conformance vectors, add one fully serialized, hash-bound single-CX claim. For the entry sequence qalloc c; qborrow b; cx c b; qreturn b; qfree c, use lifetime 0, first=last=entry:2, workspace allocation entry:0 with offset 0, width 1 and lo=hi=0, full one-bit borrowed range, and root context_key []; the expected result is proof with coverage 1.
- **C6 4**: The factorisation statement has sufficient hypotheses. check_rev2.py passed all eight result lines; independent checks confirmed both seeded rank-2 results, the causal-prefix example and six-element overlap. The conformance list does not distinguish incomplete-domain evidence from requested-proof rejection. *Change:* In Conformance vectors, state: "An otherwise successful exhaustive strict-domain slice receives evidence; it rejects when label:'proof' is requested." For c=0 and B={0}, the expected exhaustive count is 1 and coverage is 1/2; adding the proof request rejects.
- **C7 5**: The proposed §12.3 paragraph passes the mixed-fat-object standing check: claims cover the launched device closure, including default-covered calls, while native main and host-only code remain outside its inventory. The shared statement names the remaining boundary contracts without making their absence a source restriction. *Change:* No change required.
- **C8 5**: Enumeration, union deduplication, random-word consumption, auxiliary B-fiber replay, primary coverage, invocation binding and host-limit behavior are implementable. Under the explicitly authorized in-version route, §9.2 excludes certificate metadata from object_hash; source envelopes and schedule bytes are untouched. The catalog check returned the published 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197 hash. *Change:* No semantic change required; retain the publication-route qualifications and old-reader upgrade requirement.

Suggestions:
1. Defect and North Star scope: replace the K69/K70 sentence with: "K69/K70 resolves bundles and regions to interface components, with positional prepended inherited controls, and borrowed entries to lifetime positions; none selects allocated local frame-entry wires." The current word 'only' overlooks K69's inherited-control exception; this does not invalidate the expressibility defect.
2. Conformance vectors: state: "Missing B values or narrowed interface ranges prevent proof, but an otherwise successful exhaustive slice receives evidence unless proof was requested." For the c=0 frame with B={0}, expect count 1, coverage 1/2 and evidence; label:"proof" changes that result to rejection.
3. Conformance vectors: publish the complete single-CX certificate described under C5, with actual object/closure hashes and concrete occurrence records. Its two entries must be (c,b)=(0,0),(0,1), both unchanged with phase +1, yielding proof and coverage 1.

## codex

Accept. sol B1, sol B2, codex B1 and codex B2 are resolved. The defect and cited clauses are accurate; no new S0 issue or regression was found. The supplied checks passed, and independent finite checks confirmed the central witnesses. Hash stability is correct under the explicitly qualified in-version publication route.

**Path to accept:** No blocking changes remain. To raise C6 from 4 to 5, add the direct K76/K78 causal-stack conformance vector and its expected frame verdicts.

- **C1 5**: The diff preserves §5.6 K76/K78: interface and borrowed values remain independent, local constants come from the normative analysis, and repeated visits contribute a union. *Change:* No change required; retain the stated K76/K78 domain and lifetime rules.
- **C2 5**: No instruction semantics change. The CX examples and CX/MCX cancellation agree with §§4.4–4.6 and K78. *Change:* No change required; retain the existing primitive-operation identities.
- **C3 5**: Complete non-B output independence, B restoration, exact +1 phase and internal release checks establish the restricted tensor relation. Linearity preserves external correlations. The explicit allowance for surviving nonzero locals correctly distinguishes frame boundaries from region exit. *Change:* No change required; retain all complete-output, phase and release obligations.
- **C4 5**: Target and resource semantics remain unchanged. Logical lifetimes remain distinct despite storage reuse, and K75 handles checker exhaustion without imposing a domain cap. *Change:* No change required; retain the explicit K75 outcome and logical-lifetime distinction.
- **C5 5**: The expressibility defect is real under §§12.1–12.3. The repair supplies frame/workspace selection, standalone invocation binding, scheduled context selection, deterministic union sampling and complete proof inventory. Primary-draw coverage is distinguished from auxiliary B replays. *Change:* No change required; retain the union-rank sampler and explicit invocation bindings.
- **C6 4**: The factorisation statement has sufficient hypotheses. check_rev2.py passed all eight result lines; independent checks also confirmed the causal-analysis examples, tensor relation and overlap order. The supplied script checks Boolean cancellation but does not itself exercise K76's causal stacks. *Change:* In Conformance vectors and check_rev2.py, add a direct causal-stack vector stating: 'Starting with c=0 and a,x unknown, cx a c; mcx (a) c establishes c=0, whereas cx a c; cx x c; cx a c; cx x c leaves c unknown.' Require the subsequent CX(c,b) frame to receive proof in the first case and reject in the second.
- **C7 5**: The proposed §12.3 paragraph attaches claims to the launched device closure, includes default-covered calls, and excludes native main and host-only code. The shared statement names the remaining mixed-launch boundary obligations without removing capabilities. *Change:* No change required; retain the normative attachment paragraph and shared boundary statement.
- **C8 5**: Replay, maximality, context scope, overlap handling and checker outcomes are implementable. The hash claim agrees with §9.2's exclusion of certificates from object_hash and unchanged source envelopes. INDEX and the publication section correctly qualify the K route and require consumer upgrades. *Change:* No change required; preserve the publication-route qualification alongside the unchanged-hash claim.

Suggestions:
1. Conformance vectors/check_rev2.py: add a direct K76 causal-stack test with the rule and expected outcomes stated under C6. The existing algebraic assertion confirms that the interleaved prefix computes zero, but does not test why the normative entry analysis must nevertheless retain both c values.
2. Seeded sampling witness: add the successful counterpart: 'For CX(c,b); CX(d,b), either listed seed with count=1 yields evidence, primary count 1, distinct primary count 1 and coverage 1/4; replaying the second B value does not increase coverage.' This complements the existing seeded rejection vector.
