# Council — isa-09-k82-2026-11-01 round 1

Document snapshot sha256 941534df1d9e; rubric /home/tobias/Projects/bennett-workspace/bennett/docs/council/rubric.md. Members: sol, codex. Scores are advisory.

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

Accept K82. The catalog counts and unchanged envelope hash reproduce, and the proposed rule resolves the binding defect while preserving typed closure, captures, lifetime checks, quantum witness obligations, invocation context and occurrence numbering. Reported consumer implementation failures do not invalidate the proposed normative rule.

**Path to accept:** No blocking changes are required. To raise C8 from 4 to 5, explicitly distinguish preserved lexical captures from forbidden additional caller imports using the sentence supplied above.

- **C1 5**: K82 repairs the published catalog’s binding defect without changing instruction semantics or narrowing north-star capabilities. Its exception is confined to recipes with serialized bare-name formals. *Change:* Optional, §11.1 K82: add “Named-interface binding changes recipe admission and name resolution only; source-instruction semantics remain unchanged.”
- **C2 5**: Reproducing generate.py --check confirms 54 named-interface recipes, 20 invoke sites, 86 finite instances and the published envelope hash. The width rule correctly permits partial reads without inferring widths from accessed indices; no false technical premise was found. *Change:* Optional, §11.1 K82: add “Classification uses the serialized parameters list before any internal normalization of bare names into typed integer formals.”
- **C3 5**: Bindings resolve from lexical expansion environments, preserving the machine’s prohibition on scheduling decisions derived from quantum values. Wider interface lists contribute untouched wires rather than additional operations. *Change:* Optional, §11.1 K82: add “Interface discovery and binding do not inspect the quantum values carried by the resolved wires.”
- **C4 5**: Consumers receive a public binding rule instead of depending on either consumer’s undocumented capture behavior. K26/K27 preserve wire identity and lifetime obligations, while K77 remains a separate explicit context channel. *Change:* Optional, §11.1 K82: add “A consumer MUST NOT supplement this interface with other caller bindings.”
- **C5 5**: The repair operates entirely within the expansion-library contract and adds no LLVM, frontend or language dependency. Existing source capabilities retain their constructions. *Change:* Optional, §11.1 K82: add “Producers need no additional source operands for named-interface binding; the invoking lexical environment supplies the specified wire actuals.”
- **C6 4**: The vector covers closure rejection, capture, transitive interfaces, bounds, regions and live declarations. Its normalized edge digests omit controls and allocation metadata, so they do not independently demonstrate every identity-preservation assertion relevant to scheduling. *Change:* In §15’s K82 vector description, add “Supplemental vectors record inherited controls, leaf ordinals and allocation width, class, state and occurrence identity.” Include forward/inverse expectations retaining each forward ordinal and allocation identity.
- **C7 5**: K82 makes no unsupported novelty claim. Explicit free-wire interfaces and lexical captures are coherent binding conventions, and the change leaves K20’s phase-sensitive quantum obligations intact. *Change:* Optional, §11.1 K82: add “Named-interface recipes retain all K20 witness obligations, including identity on unread interface wires.”
- **C8 4**: The paragraph supplies actionable rules for eligibility, lookup, widths, direct instantiation and allocation scope. “Every K22 template … is closed” is consistent with K22 when saved captures count as bindings, but stating that explicitly would prevent misreading. *Change:* After the closed-template sentence in §11.1 K82, add “Names bound in a body’s or template’s saved lexical capture remain bound; closed forbids importing additional bindings from the splice or apply site.”

Suggestions:
1. §15: add “Supplemental K82 vectors preserve inherited controls, leaf ordinals and complete allocation metadata across forward and inverse traversal.” For an allocated scratch lifetime, the inverse must retain its forward occurrence identity and visit its forward ordinals in reverse order.
2. §11.1 K82: add “Names bound in a saved lexical capture remain bound; closed forbids importing additional splice-site or apply-site bindings.” The existing bare-template witness must continue emitting X on captured b[0], even when the application environment binds b to a different wire.

## codex

K82 closes the helper-binding defect without introducing an S0 semantic conflict. The catalog counts and hash are verified, and the recorded finite expansion results reproduce. The two disclosed consumer failures concern implementing the proposed rule, not defects in that rule. Remaining improvements concern fixture ordering and clearer wording about syntactic eligibility and template captures.

**Path to accept:** Already accept. To raise C6 from 4 to 5, align the fixture’s interface arrays with K82’s stated first-use ordering and add the explicit §15 ordering sentence; the catalog and its hash remain unchanged.

- **C1 5**: K82 repairs the published helpers’ missing bindings without changing source instruction semantics or narrowing a north-star capability. Its exception is confined to syntactically identified recipes. *Change:* Optional, §0 K82 row: append, “This changes helper binding only; source instruction interfaces retain their existing validation rules.”
- **C2 5**: The catalog hash, 54 named-interface recipes and 20 incoming invoke sites check out. Bounds checking without inferred exact widths is sound: truncation, extension and division helpers do not necessarily access every supplied wire. *Change:* Optional, §11.1 K82: add, “For example, value.trunc(4,2) may receive a four-wire a while accessing only a[0] and a[1]; accesses never infer an exact interface width.”
- **C3 5**: The rule binds existing wire identities and introduces no quantum operation, measurement or state-dependent scheduling. K77’s explicit token channel and K78–K81’s analysis and cleanup identities remain intact. *Change:* Optional, §11.1 K82: add, “Named-interface binding preserves wire identities and inherited controls and emits no leaf or semantic-call occurrence.”
- **C4 5**: Importing exactly the interface replaces incompatible consumer conventions with a public rule. Typed recipes remain closed, while K26 region flattening and K27 live-allocation wire access supply the existing conversion rules. *Change:* Optional, §11.1 K82: add, “Consumers MUST resolve only the named interface, rather than initialize the callee with the caller’s entire environment.”
- **C5 5**: Within the requested scope, K82 adds no frontend restriction or LLVM extension premise. It operates entirely inside the ISA expansion contract. *Change:* Optional, §0 K82 row: add, “No source-language marker, frontend convention or LLVM mechanism changes.”
- **C6 4**: The generator check passes, and the existing probe reproduces 86 matching edge digests and the two disclosed implementation failures among 16 binding cases. However, the vector alphabetically sorts interface arrays while K82 specifies body order; this does not change name-keyed binding results. *Change:* §15 and the K82 fixture: state, “Interface arrays list names once in first-use body order,” and preserve the collected order in generate.py instead of returning sorted(used). For value.select, the expected array is ["p","b","a","t"].
- **C7 5**: The proposal makes no unsupported novelty claim for lexical or by-name binding. It addresses a concrete interoperability defect in an existing published representation. *Change:* Optional, §11.1 K82: add, “This is a compatibility rule for the published helper representation, not a source-language calling convention.”
- **C8 4**: The operative admission and binding rules are buildable. Two terminology details merit clarification: K19’s bare-name abbreviation is now spelling-sensitive, and a K22 template described as closed still retains its lexical capture. *Change:* §11.1 K82: add, “Eligibility is determined from the serialized parameter spelling before expanding K19 abbreviations. A K22 template is closed over its positional formals and captured lexical environment; K82 never imports additional names from its apply site.”

Suggestions:
1. S1 — Align §15’s vector with K82’s body-order rule. State, “Interface arrays list names once in first-use body order,” and change generate.py’s interface result from sorted(used) to used; value.select must list ["p","b","a","t"]. Alternatively, explicitly document the fixture arrays as sorted set representations rather than normative interface order. Prefer preserving body order. Neither option requires changing catalog bytes or expanded-leaf digests.
2. S1 — Clarify §11.1 K82’s interaction with K19: “Determine named-interface eligibility from the serialized parameter list before desugaring bare integer formals.” Example: ["N"] can import an otherwise free wire q; [{"name":"N","type":"integer"}] cannot, and the same free-q body rejects.
3. S1 — Clarify §11.1 K82’s interaction with K22: “Closed templates retain their K22 lexical captures; no uncaptured name is supplied by the apply-site environment.” A template captured with q=x and applied where q=y still uses x; without a captured or formal q, it rejects.
