# Council — derive3-sqr-2026-11-02 round 1

Document snapshot sha256 6806a4e94fdc; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 5 | 5 | 5.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 5 | 5 | 5.0 |  |

Overall mean: 4.88

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Blocking issues

- none

## sol

The ambiguity and cited grammar limitation are genuine. The proposed resolution is sound, deterministic and compatible with existing identity, catalog and predicate rules. Witness results and hashes reproduced; no false technical premise or misnumbered cited clause was found.

**Path to accept:** No blocking edits. Accept the explicitly council-authorized 0.9 K ambiguity repair; without that authorization, use 0.10 as proposed. To raise C6 from 4 to 5, publish the concrete ordering, rejection and phase-sensitive fixtures with their expected results.

- **C1 5**: The proposed §4.4 rule resolves operands to existing wires without changing state, ownership or predication. Its distinctness check agrees with §3.3. *Change:* No change required; retain §3.3's rule: “Distinctness is judged on the wires denoted.”
- **C2 5**: The defect is real. §§3.3, 4.4 and 4.8 do not specify source-list bundle expansion; §16.2 admits bare NAME entries but excludes indexed list entries. The diff decides expansion, ordering, arity, scalar targets, duplicates and empty lists. *Change:* No change required; retain proposed §4.4: “The k in mcx(k) is the number of resulting control wires, not the number of list entries.”
- **C3 5**: Expansion yields the exact conjunction-controlled X of §4.4. The witness map and reverse-order adjoint agree with §5.3. K78 already identifies X-family primitives by resolved target and complete effective controls. *Change:* No change required; retain §4.4's exact-phase obligation: “A relative-phase Toffoli is never a conformant ccx.”
- **C4 5**: Flattened control order supplies §8.3's operand order, and flattened k supplies §8.1's own-control count. The existing gate.mcx recipe accepts a width-K control list and one target; its bytes need no amendment. *Change:* Optional clarification in §4.4: “The flattened control sequence supplies the own-control operand order of §8.3 and the variable k of §8.1.”
- **C5 5**: Independent hashing reproduced both stated object hashes and both interface/closure hashes. §9.2 hashes source bytes rather than resolved operands. The 219-recipe catalog envelope also matches its published hash. Consumer regeneration and rechecking are expressly required. *Change:* Optional publication sentence under “Hashes, catalog and consumers”: “Consumers adopting this repair must invalidate cached execution, expansion and validation results that used a different MCX operand-resolution rule, including results for affected callers.”
- **C6 4**: The existing replay returns proof for 16 elements; the job-built reference binary rejects the original bundle object as reported. The scalar equivalent passes check/hash and all 16 forward plus 16 adjoint cases. Mixed-list ordering and phase-sensitive bundle fixtures remain acceptance work, accurately disclosed. *Change:* In §15, publish the listed operand vectors with concrete expectations: for a:wire[2], s:wire and target t, mcx (s, a) t resolves to [s,a[0],a[1],t], k=3, and toggles t exactly when s=1 and a=3, with amplitude +1.
- **C7 5**: The repair preserves general controlled computation and exact permutation semantics. The mixed-fat-object section confines resolution and certificates to device closures and explicitly retains the shared mixed-launch boundary obligations. *Change:* No change required; retain the mixed-fat-object statement: “Shared device helpers may be linked under several roots without making native main or host-only libc certificate regions.”
- **C8 5**: The amendment is implementable without another semantic decision. It correctly distinguishes current scalar-only execution from the proposed expansion and does not claim indexed parenthesized lists already parse. *Change:* Optional clarification in §4.4: “A bare target name may denote wire or wire[1]; an indexed target must denote one live wire.”

Suggestions:
1. §15: publish a mixed-list ordering vector stating: “For a:wire[2], s:wire and an active predicate r disjoint from these operands, mcx (s, a) t has own controls [s,a[0],a[1]], k=3 and total control count c=4; its target toggles exactly when r=s=1 and a=3.” Check the expanded operand order as well as the truth table.
2. §15: add a phase-sensitive witness stating: “For p=q=0, the action maps (|0,0,0,0⟩+|0,0,3,1⟩)/√2 to (|0,0,0,0⟩+|1,0,3,1⟩)/√2, in tuple order (p,q,c,R), preserving both displayed amplitudes.” Check the complete basis columns with amplitude +1.
3. §4.4: make the single-wire target wording explicit: “A bare target name may denote wire or wire[1]; an indexed target must denote one live wire.” This avoids treating the parenthetical “scalar name” as a restriction on width-one bundle declarations.

## codex

The defect and cited clauses check out. Ordered bundle expansion is sound, preserves source and catalog hashes as claimed, and keeps mixed fat objects reachable. No false technical premise or misnumbered citation was found.

**Path to accept:** No blocking changes are needed. Accept through the explicitly council-authorized 0.9 K-repair route, retaining the stated consumer revalidation requirements. Publishing the mixed-list operand/arity vector would raise C6 from 4 to 5.

- **C1 5**: The proposed §4.4 rule resolves declared bundles into ordered wires without inspecting quantum values. It preserves §3.3 ownership, distinctness and predicate-context rules. *Change:* No change required within this proposal’s scope.
- **C2 5**: The ambiguity is real: §§3.3, 4.4 and 4.8 do not specify MCX list-entry widths, while §16.2 admits NAME entries but excludes indexed list entries. The diff decides expansion, scalar target, duplicate rejection, empty controls and k. *Change:* No change required.
- **C3 5**: The resulting operation is the exact conjunction-controlled X required by §4.4. The witness map (p,q,c) → (q XOR [c=3],p,c) and reverse-order adjoint agree with §5.3. Expansion also supplies the complete operands required by K78. *Change:* No change required.
- **C4 5**: Flattened control count and order supply §§8.1–8.3 cost and scheme operands. The actual catalog’s gate.mcx recipe takes a width-K controls formal followed by a width-one target; no recipe modification is needed. *Change:* No change required.
- **C5 5**: §9.2 hashes canonical source text, so retaining the written operand preserves identity under the authorized same-version route. Both reported object/closure hash pairs and the ref@0.9 envelope hash were independently reproduced. The note correctly requires schedule regeneration and certificate rechecking. *Change:* No change required; retain the explicit council-authorization condition and the 0.10 fallback.
- **C6 4**: Reproduced the original object’s scalar-width rejection, the replay’s 16-element relation proof, and all 16 forward plus 16 adjoint cases for the indexed ccx comparison. The note correctly limits those results; mixed-list ordering and arity remain a conformance checklist rather than concrete published vectors. *Change:* In “Conformance vectors and actual verification,” add: “For s:wire, b:wire[2], t:wire, mcx (s, b) t resolves to [s,b[0],b[1],t], with k=3 and four gate operands. It maps (s,b,t) to (s,b,t XOR (s AND [b=3])) with phase +1 on all 16 basis inputs.”
- **C7 5**: The change preserves controlled-anything and linear wire semantics without narrowing any North Star capability. The mixed-fat-object section keeps expansion and certificates within device closures and names the remaining shared boundary obligations. *Change:* No change required.
- **C8 5**: The amendment is localized and implementable. It distinguishes source syntax, resolved operands, primitive matching and catalog realization, and accurately separates the older first-bit checker result from current scalar-only rejection. *Change:* No change required.

Suggestions:
1. In §15’s conformance additions, publish the concrete mixed-list vector given under C6. Also state: “mcx (b, s) t resolves to [b[0],b[1],s,t]; it has the same unitary and K78 primitive identity as mcx (s, b) t, while retaining its distinct canonical source bytes.” This tests operand ordering independently of conjunction semantics.
