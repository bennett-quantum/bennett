# Council — contract-xv4-2026-11-02 round 1

Document snapshot sha256 55d0eb6494b0; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

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

Verdicts: **sol: revise**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: no**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 1 (blocking 1), codex: core 0 / contract 0 (blocking 0)

## Blocking issues

- **[sol] XV4-B01** (Recommended exact spec diff; ISA §12.2 K74 coverage and verdicts; contract): *Fix:* §12.2, preferred repair: replace K74's classification sentences with: 'After every §12.1 obligation succeeds, an exhaustive table/program/oracle claim receives exactly one verdict: proof if its domain equals unrestricted D component by component; otherwise proof_relative_to_image iff fixed_regions is nonempty, every image binding is valid, and every non-fixed component occurs exactly once with its full range; otherwise evidence. An absent fixed_regions field means an empty list. Successful sampled claims always receive evidence. Coverage remains the exact n/|D| against unrestricted D. A requested proof MUST be rejected unless the computed verdict is proof; a requested proof_relative_to_image MUST satisfy the qualified-verdict conditions.' Preserve mismatch rejection and K75 host-limit handling. Expected outcomes: the full-domain one-bit X claim receives proof with fraction 1; the exhaustive 0102 image claim receives proof_relative_to_image with 64 elements and fraction 1/65536; sampling remains evidence. Alternatively, retain K74's full-D sentence, add the explicit nonempty guard, and replace its strict-slice sentence with 'Successful exhaustive strict slices receive evidence unless they satisfy the proof_relative_to_image rule.' I prefer the single exclusive classifier.
  <1>1 K74 assigns proof to successful componentwise full-D exhaustive claims and evidence to successful exhaustive strict slices.  — clause:ISA-12.2, Coverage and verdicts (K69/K74), spec/Bennett-ISA-Spec-0.9.md:3784–3796
  <1>2 The proposed addition assigns proof_relative_to_image when all non-fixed components are full-range and all remaining components are fixed_regions bindings. It neither requires any fixed binding nor explicitly replaces K74's blanket strict-slice classification.  — witness:docs/notes/2026-11-02-contract-xv4.md:53–74
  <1>3 Consider a successful exhaustive comparison of a one-bit X action over t=0,1, with no regions or borrowed systems and fixed_regions absent or empty. Every non-fixed component is full-range and there are no remaining components, so the added condition holds vacuously: K74 assigns proof while the addition assigns proof_relative_to_image. For the proposed 64-case image slice, retained K74 instead assigns evidence while the addition assigns proof_relative_to_image.  — witness:full domain bundles=[{name:t,width:1,lo:0,hi:1}], borrowed=[], regions=[], expected table 0→1 and 1→0; witness:proposal's 64-case image slice; step:<1>1; step:<1>2
  <1>4 The amended text gives overlapping outcomes without a precedence rule. In particular, the claimed preservation of old full-D K74 labels is not secured.  — step:<1>1; step:<1>2; step:<1>3

## sol

The conditional-proof design is sound, its cited premises and arithmetic check out, and it preserves North Star scope. One contract blocker remains: the exact added verdict rule overlaps existing K74 outcomes and also matches legacy full-domain claims vacuously.

**Path to accept:** Replace the overlapping K74 verdict rules with one exclusive classification that preserves full-D proof, requires nonempty image bindings for the qualified verdict, and assigns evidence to other successful slices. Explicitly reject requested unqualified proof for a qualified result. No machine, instruction, target or catalog change is needed.

- **C1 5**: The proposal changes certificate scope without changing §5.2's machine domain D, reference result F_B, or execution semantics. *Change:* No change required.
- **C2 5**: No instruction changes are proposed. The image-to-cell mapping agrees with §3.3's register-to-region binding. *Change:* No change required.
- **C3 5**: The conditional permutation argument is sound with the retained exact-phase, full-tuple, dirty-system and inherited-control obligations. Preparation is established from operations rather than inspection of unknown quantum data. *Change:* No change required.
- **C4 5**: Targets, costs and resource semantics are unchanged. The catalog check reproduces 219 recipes and envelope hash 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. *Change:* No change required.
- **C5 4**: Resolved image identities, invocation binding and protection of unrestricted obligations are appropriate. However, the added verdict rule overlaps both existing K74 classifications; see XV4-B01. *Change:* §12.2: replace the verdict classification with the mutually exclusive rule written in XV4-B01, including a nonempty fixed_regions requirement.
- **C6 4**: The mathematical hypotheses are sufficient. Independently reproduced: 64 cases, coverage 1/65536, 524288 fixed bits at A=16,W=8, and the stated raw-byte SHA-256. The tiny example lacks a specific oracle relation for a complete conformance vector. *Change:* Conformance vectors: state, 'For the tiny oracle, payload(x,db)=db[x]&1 and code=0 at a sufficient budget. The expected tuple is (x,t XOR (db[x]&1),f,db), with workspace clean.' For image 0102, x=0 flips t and x=1 preserves t; all 64 tuples must agree.
- **C7 5**: The cited ISA clauses, Dialect 0.3 draft §§19.9/25.2 and North Star §5.1/§8 rung 4 are accurately represented. The proposal preserves the complete SQLite rung and correctly distinguishes a certificate terminology repair from missing execution capability. *Change:* No change required.
- **C8 4**: The proposal clearly separates conditional proof, evidence and executable applicability, and accurately limits its verification claims. The exact verdict integration needs correction, and the image-mutation vectors should specify which bindings remain unchanged. *Change:* Conformance vectors: state, 'Changing image bytes while retaining the old digest or preparation binding rejects reuse of the old claim; a consistently rebound image requires a fresh successful check and may receive its own qualified verdict.'

Suggestions:
1. Conformance vectors: distinguish stale-binding mutations from valid new claims. State, 'Swapping 0102 to 0201 while retaining the original digest rejects. Rebinding to SHA-256 25dfd29c09617dcc9852281c030e5b3037a338a4712a42a21c907f259c6412a0 and establishing the new preparation permits a fresh conditional check; it does not reuse the old result.'
2. Hashes, catalog and consumers: distinguish certificate requests from checker outcomes. State, 'fixed_regions and any supplied label request change certificate bytes; the independently assigned qualified verdict is recorded in the checker report. Under the proposed in-version K repair, source/interface/closure and object hashes remain unchanged because §9.2 excludes certificate sections from object_hash; target and catalog bytes are unchanged.'

## codex

The fixed-image qualification is sound and the cited defect is real. No false cited premise or S0 issue was found. Counts and the raw-byte hash were reproduced. Under the proposed authorized 0.9 K extension, §9.2 confirms that certificate changes leave source, interface and object hashes unchanged; target and catalog bytes are untouched.

**Path to accept:** Already acceptable. To raise C6 from 4 to 5, specify the tiny oracle and complete expected tuple relation, then publish the 64-case fixture with its expected qualified verdict, coverage and stale-binding rejection results.

- **C1 5**: The proposal restricts a certificate claim's domain without changing the machine. ISA §5.2 does include every interface-region cell in D, as claimed. *Change:* §12.2: add, 'A fixed_regions binding restricts the verification domain only; it does not alter the region's signature or its semantics on unrestricted D.'
- **C2 5**: No instruction semantics change. The image packing agrees with §3.3's register-to-region binding. *Change:* §12.2: add, 'fixed_regions is certificate metadata and introduces no new ISA instruction or operation for inspecting coherent data.'
- **C3 5**: Exact permutation phase, complete tuples, arbitrary target/fault values, dirty systems and inherited controls remain required. Equality on this basis slice extends linearly to its span, including external references. *Change:* §12.2: add, 'For image I, the exact assertion is VJ_I = PJ_I, where J_I inserts the fixed image and prescribed clean workspace; the equality also holds after tensoring with identity on an arbitrary external reference.'
- **C4 5**: The diff changes neither targets nor resource accounting. Invocation and schedule bindings remain applicable; conditional correctness does not authorize a different realization or cost calculation. *Change:* §12.2: add, 'This qualification does not relax target matching, schedule binding, resource accounting or error-composition obligations.'
- **C5 4**: Resolved region identities, shapes, raw-byte hashes, invocation scope and executable preparation obligations are specified. K69–K74 and dialect draft §§19.9/25.2 are cited accurately. An explicit verdict decision table would make the extension easier to integrate with existing K74 prose. *Change:* §12.2: state, 'After successful replay, an exhaustive claim receives proof for full D; otherwise it receives proof_relative_to_image when fixed_regions is nonempty and every other component has its full range; every other exhaustive slice receives evidence. Sampled claims always receive evidence.'
- **C6 4**: The restricted permutation statement is sound, and unrestricted borrow-frame/inverse-pair obligations remain protected. The reproduction script passed; the 64-case count, 1/65536 coverage and raw-byte SHA-256 are correct. The tiny example does not specify an oracle function or complete expected relation. *Change:* Conformance vectors: define a fault-free fixture with payload db[x] & 1 at a sufficient bound. For image 0102, state the complete relation (x,t,f,db) → (x,t XOR (1 XOR x),f,db), covering all 64 tuples.
- **C7 5**: The proposal preserves the fixed-database interpretation of North Star rung 4 while retaining all varying components. It neither substitutes sampling nor narrows SQLite, Grover or resource-estimation requirements. The claimed terminology mismatch exists. *Change:* Release and after acceptance: add, 'This verdict establishes only the stated fixed-image relation; all other North Star rung-4 acceptance requirements remain independently required.'
- **C8 4**: The proposal is implementable at this specification stage. Preparation is checked through declared bytes and logical operations, with no unknown-state inspection. The certificate-versus-checker-report distinction could be stated more precisely in the hash discussion. *Change:* Hashes, catalog and consumers: replace the certificate-verdict sentence with, 'The fixed image and any requested label change certificate bytes; the checker-assigned verdict and resolved bindings appear in the checker report. Neither change alters the §9.2 object or symbol hashes.'

Suggestions:
1. §12.2: make the new rule an explicit exception to the existing strict-slice evidence sentences. State: 'Full-D exhaustive claims retain proof. A strict slice receives proof_relative_to_image only with at least one fixed_regions binding and full ranges for every remaining component; otherwise it receives evidence.' This also makes absent or empty fixed_regions unambiguously preserve existing K74 outcomes.
2. Conformance vectors: specify the tiny oracle as payload db[x] & 1, with no fault at the chosen bound. Image 0102 yields target t XOR (1 XOR x); image 0201 yields t XOR x. An implementation that ignores the supplied image and uses 0102 passes the first 64 tuples and fails all 64 swapped-image tuples. For mutation tests, state that the original hash, expected relation or executable preparation binding is retained: changing an image is not inherently invalid when a fresh, correct claim and preparation binding are supplied.
3. §12.1, conditional process comparisons: state, 'With image-preparation isometry J_I, compare the channels E_real ∘ Ad_J_I and E_ref ∘ Ad_J_I while retaining the complete output interface. Controlled-unitary claims retain a phase-sensitive bound on ||U J_I − V J_I||; equality of uncontrolled channels alone does not discharge that obligation.' This makes explicit the phase requirement the proposal already preserves.
