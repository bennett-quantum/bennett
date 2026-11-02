# Council — contract-b5b-2026-11-02 round 1

Document snapshot sha256 8db876e28ce8; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

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

Accept the no-change disposition. Accepted §11.1 K82 and K27 already decide both b5b divergences, the examples match the fixtures, and both independent checks passed. No false technical premise or incorrect clause reference was found. Implementation completion remains the owner's responsibility.

**Path to accept:** Already acceptable. To raise C6 from 4 to 5, identify the passing implementation checkpoint and its limits using the suggested replacement sentence; retain the empty spec diff.

- **C1 5**: The proposed diff is empty and changes no machine state, tier or step relation. *Change:* No machine-model change required.
- **C2 5**: No instruction changes are proposed. Both worked examples match the published four-leaf alloc/X/X/release expectations. *Change:* No instruction-set change required.
- **C3 5**: §11.1 K82 gives callee allocations their own scope. K27 makes acquired declarations usable as wire actuals and rejects inactive wire uses. Two X applications restore the clean allocation before release. *Change:* No coherent-semantics change required.
- **C4 5**: The no-op diff changes neither resource accounting nor target matching. It preserves catalog expansion and allocation leaves. *Change:* No resources or targets change required.
- **C5 5**: §11.1 K82 explicitly imports only interface names, evaluates them using K26/K27 wire-actual rules, and hides unrelated caller names. These rules directly settle both failures described by b-isa-spec-b5b. §15 publishes the cited accepted fixture. *Change:* No contract amendment required; retain the implementation-follow-up disposition.
- **C6 4**: I ran generate.py --check successfully: 54 interfaces, 20 edges, 86 instances and 16 cases. ref_catalog.py --check also passed with envelope hash 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. The generator reproduces fixture cases; it does not execute them against Rust. The note correctly distinguishes these checks from the owner's reported implementation evidence, but identifies that checkpoint imprecisely. *Change:* In 'Conformance vectors and verification', state: 'The checkpoint recorded in .tmp/sol-ref09/k82-green.log passed all 16 binding cases and all 86 edge digests; it predates the declaration-release ownership refinement and does not establish a current-tree full gate.'
- **C7 5**: Keeping accepted K82 preserves the independent-consumer contract required by North Star §§4.4 and 6.1 and removes no promised capability. The earlier K82 council verdict confirms acceptance; the bead's pending-round wording is historical. *Change:* No North Star or release-scope change required.
- **C8 5**: The disposition identifies the exact existing rule, both reproducible fixture cases, rejected alternatives and the responsible implementation stream. The empty diff supports the unchanged-byte and unchanged-hash claims without requiring consumer migration. *Change:* No additional specification text required.

Suggestions:
1. In 'Conformance vectors and verification', replace the mutable 'now pass' attribution with: 'The checkpoint recorded in .tmp/sol-ref09/k82-green.log passed all 16 binding cases and all 86 edge digests; it predates the declaration-release ownership refinement and does not establish a current-tree full gate.' Keep b5b open until its owner completes the relevant gate, as the note already requires.

## codex

Accept the empty spec diff. Accepted K82 already resolves both b5b binding failures, and the examples, counts and catalog hash check out. No false load-bearing premise or misnumbered citation was found. Consumer completion remains an implementation obligation.

**Path to accept:** No changes are required for acceptance. To raise C6 from 4 to 5, document the fixture's sorted-set representation and the normative body-order example specified above.

- **C1 5**: The proposed empty diff leaves the accepted machine model unchanged. Both reported failures concern recipe binding, not machine-state semantics. *Change:* None required; retain the empty spec diff.
- **C2 5**: No instruction or constructor changes. The independent generator confirmed 54 named-interface recipes, 20 invoke edges and 86 finite edge instances. *Change:* None required; retain the existing instructions and catalog.
- **C3 5**: Both worked examples match the accepted fixture: alloc #0; x #0[0]; x #0[0]; release #0. The local allocation returns clean, and the unrelated caller wire is untouched. K27 expressly rejects inactive declaration wire uses. *Change:* None required; retain both examples and their expected leaves.
- **C4 5**: The disposition introduces no target, resource or scheduling-policy change. Existing expansion leaves and their accounting remain authoritative. *Change:* None required; retain existing resource and target rules.
- **C5 5**: §11.1 K82 expressly imports exactly the named interface through ordinary wire-actual evaluation, applies K26/K27, and hides unrelated caller names. These rules directly cover both failures recorded in b-isa-spec-b5b. §15 publishes the cited fixture. The spec's round-10 acceptance and the K82 council verdict confirm acceptance. *Change:* None required; keep b5b as an implementation follow-up under accepted K82.
- **C6 4**: I reran generate.py --check successfully: 54 interfaces, 20 edges, 86 instances, 16 cases. The owner's red/green logs substantiate the reported two failures and subsequent focused passes; these remain reported implementation evidence, not a fresh current-tree gate. One inherited fixture discrepancy remains: 31 interface arrays are sorted rather than in K82 body order. *Change:* In 'Conformance vectors and verification', add: 'Fixture interface arrays represent name sets in sorted order; derive traversal order from §11.1 K82. For value.select, body order is [p,b,a,t], while the fixture stores [a,b,p,t].' This preserves fixture bytes and leaf digests.
- **C7 5**: The disposition preserves the independent-consumer contract promised by North Star §§4.4 and 6.1. It neither removes a capability nor substitutes implementation behavior for normative semantics. *Change:* None required; retain the requirement that each consumer independently implement K82.
- **C8 5**: The note correctly separates accepted contract text, outstanding implementation work and historical evidence. Its empty diff requires no migration. I also reran ref_catalog.py --check: 219 recipes and envelope SHA-256 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. *Change:* None required; retain the no-change disposition and owner-controlled completion gate.

Suggestions:
1. In 'Conformance vectors and verification', state: 'Fixture interface arrays represent name sets in sorted order; §11.1 K82 supplies body order. For value.select these are [a,b,p,t] and [p,b,a,t], respectively.' This documents the existing S1 discrepancy without changing catalog bytes or expected-leaf hashes; binding remains by name.
2. In 'Defect classification and North Star scope', clarify: 'K22 templates retain their saved lexical captures; closure forbids importing unrelated apply-site bindings.' The accepted bare-template-formals-import-nothing case must continue emitting x b[0], even when the applying recipe binds its own b to a.
