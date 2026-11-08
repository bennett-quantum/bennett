# Function pointers in lifted oracles — round-1 review

Reviewer: gpt-6.1-sol

Date (UTC): 2026-11-08T10:24:45Z

Reviewed note: [Function pointers inside lifted oracles](../design/2026-11-08-function-pointers-in-lifted-oracles.md), commit `8c0a188432fb619d7063558a9da4e9ce5776ee3d` (includes `5265ccb0059de4173cc4a3484be61a94eb0e9a51`), branch `job/s2-0vi-design`.

Author verification rerun: `python3 -B .tmp/s2-0vi-design/verify_note.py` — **PASS, exit 0**: 99 quotations after whitespace normalization; 15 footnote source scopes; 32 file/heading links; 10 fully qualified code citation ranges; 15 source hashes; inventory total 2,229; canonical cost enumeration for k=1..129. The unchanged script ran under `bwrap --ro-bind / /`, with the author scratch directory privately overlaid by its byte-identical copy at `.tmp/s2-0vi-review/verification/`. This preserves the original command and inputs while directing its two generated receipts into review-owned storage. Original and rerun source-snapshot records match exactly. Receipt: `.tmp/s2-0vi-review/verify-note.txt`.

## Findings

None. **P0/P1 on North Star §8 rung 4: 0; P2: 0; nits: 0.** No review beads are proposed. Existing implementation and acceptance dependencies are not new defects in this design-only note.

## Evidence and judgment

**The no-ISA-change verdict is supported as an expressibility conclusion.** I opened the cited sources rather than relying on the verifier matching strings:

- ISA 0.9 §3.7, `spec/Bennett-ISA-Spec-0.9.md:834–854`, says “Resolve the fixed callee instance above”; §4.2, `:953–1008`, supplies integer constants, equality/unsigned comparisons, branches, static calls, returns and faults, and says “control never leaves a function except through `lift.call`/`lift.ret`”. Its `qjumpr` range is the containing function instance. Comparing a pointer bit pattern and choosing a static call therefore uses existing rows and normal call history; it does not require an indirect jump across functions.
- ISA 0.9 §7.2, `:1693–1704`, fixes “each global's base and image”; §9.1, `:2137–2159`, specifies “`data` lines are `NAME SP HEX`.” These encode stored address bits without an executable-address allocation. Dialect §4.4, `spec/Bennett-Dialect-Spec.md:921–939`, explicitly requires “A(F) is the value of `ptr @F` in every tier” and includes code constants and “in every data image: global initialisers, vtables, function tables”. The note correctly separates A(F), row indices and callee symbols.
- Dialect §§4.1/5.2/14.2, `:862–887`, `:1009–1039`, `:7436–7459`, require initializer seeding, joint closure/value/memory convergence, explicit FN candidates, and the type-compatible fallback over addresses used anywhere in the linked program. The determining closure sentence is “The device closure includes every candidate”. Data tables, heap registration and callbacks are analysis obligations, not an assumption that direct edges alone suffice. Whole-program coverage itself is stated in North Star §3.3, `docs/Bennett-NorthStar.md:276–304`; missing bitcode must be reported. The note does not claim that the actual runtime/SQLite closure has already satisfied those obligations.
- Dialect §16.4, `:8331–8347`, explicitly gives a static call leaf, continuation jump and default fault. REPORT §5.2(ii), `docs/spikes/sqlite/REPORT.md:303–310`, contains the quoted construction and “No ISA change (confirms R2).” ISA §0.3, `:291–310`, expressly defers SQLite E1–E5 while retaining “compare tree plus static `lift.call`”. E3 is correctly classified as a future contract change, not a published row.

No additional normative sentence is needed to establish that construction. Proving complete candidate coverage for a particular materialised module remains necessary implementation/acceptance evidence; the note explicitly leaves it open. It also correctly distinguishes published dialect 0.2.14 targeting ISA 0.8 from the classical-only accepted `0.3-r1` profile in draft §1.7, `:183–229`. A reviewed coherent ISA-0.9 profile/pin decision is still required. Acceptance of this note does not publish that profile.

**No narrowing of rung 4 is introduced.** The entire rung-4 quotation matches North Star §8, `docs/Bennett-NorthStar.md:802`, byte for byte. Note §4, line 73, says “Never discard defined native successes to obtain a smaller domain.” Its §6 question 3 requires evidence for empty/default paths on the full rung domain and expressly prohibits compiler-induced traps on supported executions. Thus the 73 empty sites are historical inventory, not an unreachability proof or permission to drop valid runs. A real defined SQLite call reaching an omitted target would block rung 4; this note neither asserts such a run is correct nor closes its acceptance dependencies. No candidate ceiling, scalar-only pipeline, source rewriting, domain reduction or resource-exhaustion-as-fault alternative is allowed.

The fault explanation agrees with ISA §§4.2/5.2/5.4: a reached `fault 4` has HALT successor and bounded result `(0,4)`; commit XORs the fault and leaves the target unchanged; prefix reversal restores work/image state. The note preserves earlier budget exhaustion. Certificate quotations match §12.1, `:3834–3838`, and image identity matches §9.2, `:2208–2227`; the text does not infer SQL correctness from reversibility alone.

**All code citations were checked, including shorthand ranges.** Paths below are in the inspected `bennett-plugin` snapshot `2319890511cdd2fa46b8c4cc748b52877408be6f`:

| Source and ranges | What the source establishes |
|---|---|
| `src/Analysis.cpp:434–487`, `1842–1844`, `708–723` | Symbolic FN values, recursive aggregate seeding for every initialized global, explicit candidates and address-taken/type fallback. |
| `src/Analysis.cpp:791–820`, `1607–1611`, `1893–1909` | Candidate argument/return binding, call edges and iteration to convergence, with explicit resource-exhaustion handling. |
| `src/Analysis.cpp:1284`, `1340–1352`, `1168` | Composite handling precedes scalar GEP and retains the cited unimplemented diagnostic. These are accurately described as inspection points, not a new vectorised SQLite execution. |
| `src/Production.cpp:2280–2289`, `2761–2767` | Candidate-dependent state discovery and indirect CC closure growth. |
| `src/Production.cpp:585–604`, `309–311`, `1772–1790`, `945–953` | Comparison-map addresses, supplied-map failure, separately labelled standalone convention, pointer constants, recursive relocation discovery and the oracle path into `lowerScalar`. |
| `src/Production.cpp:610–624`, `1386–1410` | A separate equality-first CC/R emitter; it is not used as evidence for lifted dispatch cost. |
| `src/Scalar.cpp:146–151`, `685–708`, `305–348`, `784–802`, `997–1015` | Comparison-address constants/images, canonical hybrid dispatch with declaration/default faults, indirect closure collection, and fresh analysis after preparation. |

The required-work table is consistent with these existing mechanisms: analysis/production work extends and validates them rather than claiming indirect-call support is absent. Its implementation/fixture/report rows are within existing contracts, while coherent-profile publication and E3 are explicitly contract changes. Proposed driver/test paths exist; the note correctly labels the driver row as follow-up work rather than a driver-code audit. Historical bp-fj1 measurements and bp-1bb branch progress remain qualified, matching the supplied bead snapshots and binding 5u3 interpretation.

**Cost was independently checked.** `python3 -B .tmp/s2-0vi-review/audit_evidence.py` passed. It locates all 99 quotations with source headings, checks unchanged source snapshots and the full rung quotation, and constructs/walks the printed §16.4 row graph for k=0..129 without calling the author recurrence or plugin. At k=99, worst defined-target dispatch is 29 rows and worst miss is 28, with the note's exclusions; at k=0 the jump/default fault costs two rows. REPORT's older approximation is correctly qualified and queued for correction. These checks are documentary arithmetic, not executable oracle acceptance.

**Disposition: ACCEPT**

## Suggestions

1. Attach this review to bennett-0vi and retain the note's existing publication, exact-analysis/vector-GEP, address-map and complete rung-4 acceptance follow-ups. File the author's queued REPORT-cost correction separately; no review repair round is needed.

No compilation, simulator, sibling test suite or full gate was run. This disposition covers the committed design note and its evidence, not implementation completion or a rung-4 PASS.
