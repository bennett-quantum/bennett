# Council — isa-09-2026-10-31 round 5

Document snapshot sha256 150da8afe0c8; rubric docs/council/rubric-isa.md. Members: muse. Scores are advisory.

| | muse | mean | spread ≥ 2 |
|---|---|---|---|
| C1 | 4 | 4.0 |  |
| C2 | 4 | 4.0 |  |
| C3 | 4 | 4.0 |  |
| C4 | 4 | 4.0 |  |
| C5 | 4 | 4.0 |  |
| C6 | 4 | 4.0 |  |
| C7 | 5 | 5.0 |  |
| C8 | 4 | 4.0 |  |

Overall mean: 4.12

Verdicts: **muse: accept**

Core verdicts: **muse: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: muse: core 0 / contract 0 (blocking 0)

## Blocking issues

- none

## muse

Accept. The round-5 diff from round 4 changes only the status header and records maintainer ratification of K64 and K65; it introduces no semantic change and no regression. Previous round had no blocking issues, so there are no previous blockers to close. Re-reading the full snapshot against the north star and the 0.8 ISA found no S0 core or contract issue: the step machine and its inverse, F_B and commit, lproc binding instances, coherent control, borrow frames, cleanup discipline, identity envelopes, schedule selection, claim replay and host-limit handling are each given one normative reading, and deferred items keep their capabilities through stated defaults or explicit constructions.

**Path to accept:** Already accept. To raise the lowest criteria from 4 to 5: (1) in §16.3 replace every '<to be computed by the 0.9 precheck: example k, name>' placeholder with the computed 64-hex interface hash and verify each displayed envelope against §9.2; (2) in §11.1 publish ref/ref-0.9.json with the stated 219 recipes and envelope hash 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197; (3) add the pending worked controlled-action target, schedule and certificate fixture referenced by §17 item 7.

- **C1 4**: §3.1 fixes tiers and the no-wire-dependent-control invariant; §3.2 lists all state components; §3.3 fixes linear SSA, wire distinctness, register ledger states and width checks; §3.6-§3.7 give a complete forward and inverse step relation. *Change:* In §3.3, add one consolidated register-state diagram generated from the handle-transition table, including viewed, consumed, alias and reversal transitions.
- **C2 4**: §4.1-§4.9 cover classical, lifted, allocation, gate, memory, structured and fault instructions; §4.2 gives class, reads, writes, flags and successors; §4.8 closes tiers, arities and result placement. *Change:* In §4.8, add the result type and width rule for every dotted lift suffix in the opcode table itself, rather than requiring the reader to combine §3.3, §4.2 and §4.8.
- **C3 4**: §3.6 gives dispatch, execute, successor, commit and inverse steps; §5.2 defines F_B, commit and prefix reversal; §3.7 gives C1-C5 and R1-R5 with inverses; §5.6, §6.1, §6.2 and §6.4 define borrow frames, provenance, cleanup windows, matched pairs and unitary cleanup realisations. *Change:* In §6.1, add a conservative syntactic sufficient condition for the outstanding-dependence factorisation test, while retaining the exact operator factorisation as the semantic definition.
- **C4 4**: §8.1 fixes exact-rational expressions, EPS-DECADE and variable contexts; §8.2 fixes aggregation; §8.3 fixes first-match gates, schemes, capabilities, topology and placement; §17 items 9-12 and 15 give defaults. *Change:* In §8.3, publish one additional worked target containing a scheme, a table-indexed epsilon expression and a topology together, with its matched leaves and aggregate resource vector.
- **C5 4**: §9 fixes object sections, signatures, structural layout-leaf identity, hashing, linking and frame records; §10 and §10.1 fix launch and resolved estimates; §11 fixes schedule matching and validation stages; §12-§13 fix claims, domains, composition and coverage. *Change:* In §12.3, replace the abbreviated certificate outline with one complete minimal certificate JSON instance containing bindings.invocation, one region record, one claim and composition.
- **C6 4**: §14.1 defines F_B operationally; §14.2 defines allocation order, borrowed systems and measurement; §14.3 states T1-T6 with hypotheses; §15 derives suites A-H and names boundary witnesses for faults, stack exhaustion, SDP pivots and nested budgets. *Change:* In §14.3, add to T2 and T5 the same explicit domain and realisation hypotheses now stated in §5.2 and §6.2, so each theorem can be quoted without reconstructing its premises from earlier sections.
- **C7 5**: The draft preserves three tiers, total lifted oracles with fault registers, quantum actions, virtual allocation classes, target descriptions, linking, launch, scheduling and proof/evidence certificates; deferred routing and pebbling retain explicit-swap and full-history constructions. *Change:* In §0, add a north-star traceability index mapping each §8 demo rung to the ISA sections and conformance suites that carry it.
- **C8 4**: A VM author can implement §3-§7 and a specialiser author can implement §5, §8 and §11 from the text; §17 gives a default for every deferred implementation decision. Remaining friction is the unpublished ref serialization, placeholder example hashes and the size of the §11.1 binding language. *Change:* Before publication, replace every §16.3 hash placeholder with its computed 64-hex value and publish the §11.1 ref catalog plus the pending controlled-action target, schedule and certificate fixture named in §17 item 7.

Suggestions:
1. §16.3 (S1, contract): the normative examples still contain distinct hash placeholders. Fix: in §16.3, state 'Every interface_hash in this section is the 64-hex value computed by §9.2 from the displayed envelope' and replace, for example, example 1's placeholder for inc8 with SHA-256 of the six-line envelope printed immediately below it. This does not change semantics because §9.2 already determines every value.
2. §5.5 (S1, core): the sentence 'no intervening row writes those locations, suite F, nor those cells, below' can be read as making an intervening lift.store ill-formed, while the later paragraph says it is not ill-formed. Fix: in §5.5 replace that parenthetical with 'no intervening row writes those ins locations (suite F); intervening writes to mem cells are permitted but mean the uncall is not guaranteed to clear fr', retaining the corrected example that lift.oracle_uncall remains the identical permutation and prefix reversal still restores the caller state.
3. §6.1 (S1, core): outstanding dependence is defined exactly by nonexistence of V with M = I_G tensor V, but no decidable sufficient check is named. Fix: in §6.1 add 'A producer MAY establish non-dependence by the dependency-set test: if no live value, interface wire, region cell or uncancelled diagonal phase has a transitive read path from g in the intervening sequence, then M factorises as I_G tensor V; failure of this test does not by itself prove dependence.' The H d0; CCX d0 p d1; CX d1 t; CCX d0 p d1; H d0 witness remains rejected because t has such a path.
4. §11.1 and §17 item 7 (S1, contract): the complete ref catalog and controlled-action fixture are named but not reproduced in the specification. Fix: in §11.1 state 'The catalog bound as ref version 0.9 is the file ref/ref-0.9.json whose four-line envelope hashes to 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197' and publish that file and one ctl action fixture with its target leaf events, schedule entries, frame descriptor and certificate. Until then §11 correctly requires E_SCHEDULE_INFEASIBLE from consumers lacking the bound library, so no executor computes a different function.
