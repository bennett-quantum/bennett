# Council — pass2-2cg-2026-11-02 round 2

Document snapshot sha256 69ad4cacfaae; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

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

## Previous-round blockers, status

- [sol] sol:B1: **resolved** — The proposed §17.1 paragraph explicitly scopes bookkeeping to selected device/comparison closures, retains native host code subject to existing promotion rules, and covers shared metadata/history transfer.
- [sol] codex:B1: **resolved** — The added paragraph binds traces, budgets and identities to the selected closure; the mixed example and incorporated boundary obligations preserve the native-host/device-object split.
- [codex] sol:B1: **resolved** — The new §17.1 paragraph explicitly covers mixed-object placement, selected comparison closures, shared metadata and existing layout/promotion rules.
- [codex] codex:B1: **resolved** — Allocation traces, budgets and runtime-body identities now bind the selected device closure without requiring whole-binary lowering.

## Blocking issues

- none

## sol

Accept. Both sol B1 and codex B1 are resolved. Allocation arithmetic, source claims, boundary references and catalog claims check out; no new S0 issue or regression was found.

**Path to accept:** Already acceptable. To raise C6 from 4 to 5, supply the tagged, identity-bound production vector with executed metadata-state, failure-prefix, reversal and replay checks under the publication rules.

- **C1 5**: Both maintained §17.1 texts preserve the same primitive allocation model. ISA 0.8 and 0.9 §7.1 confirm max(n,1) bumps, requested-size records and nonreclamation. The proposed bookkeeping remains ordinary memory state. *Change:* §17.1, optional: “A zero-size probe consumes one heap byte and one allocation-table entry, records requested size zero, and supplies no accessible payload bytes.”
- **C2 5**: The inspected bump.c implements cursor refresh, size retention and liveness using existing allocation primitives and ordinary loads/stores. No allocation-query instruction is necessary. *Change:* §17.1, optional: “This allowance introduces no primitive; allocator bookkeeping executes through the existing materialised operations.”
- **C3 5**: Retaining successful operations before a failing primitive agrees with per-primitive failure atomicity and ISA §7.4 history. Metadata-slot reuse changes ordinary bytes without reclaiming primitive storage. Existing oracle cleanup and version-specific R-fault obligations remain applicable. *Change:* §17.1, optional: “Prefix retention describes forward execution before cleanup or reversal; it does not waive oracle workspace restoration or alter §§17.5–17.6.”
- **C4 5**: Both traces reproduce: [3,13,16] ends at 4128 with three records; [3,0,12,16,32] ends at 4160 with five. At heap capacity 32, production metadata allocation faults with code 2 after four successful records at bump 4128. Actual bookkeeping and replay costs remain charged. *Change:* Alternatives and worked witness, optional: “These figures assume empty metadata lists, alignment 16, sufficient step/table capacity and no additional prologue allocations; any entry replay or shadow-stack allocation is charged separately.”
- **C5 5**: The new applicability paragraph binds traces, budgets and identities to the selected device closure and its comparison build. §§7.3, 17.7, 19.9 and 23 support the identity/publication account. Applying both additions in memory preserves every existing fenced artefact in both texts. The ref@0.9 envelope remains 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. *Change:* Publication boundary, optional: “Unchanged catalog bytes do not imply unchanged identities for generated closures, runtime bodies or layouts.”
- **C6 4**: check_rev2.py exits 0 with all eight PASS lines. Its allocation checks establish arithmetic and retained primitive prefixes, not execution or reversal of production metadata stores. The note accurately discloses that limitation and requires a separate tagged production vector. *Change:* Conformance vectors: specify “For the pinned body with empty metadata lists and sufficient non-heap capacity, heap=64 returns 4112 with bump=4160, records=5 and code=0; heap=32 never returns from malloc and stops with bump=4128, records=4 and code=2. Verify metadata bytes and primitive state through reversal and identical replay.”
- **C7 5**: Dynamic bookkeeping preserves libc, SQLite and Julia allocation capability. Both round-1 mixed-object omissions are repaired. The incorporated scope statement explicitly names the remaining mixed-launch and host-memory contract work without requiring whole-binary lowering. Successful realloc preservation agrees with [WG14 N1570 §7.22.3.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf#page=367). *Change:* Fat-object applicability, optional: “The §8.5 snapshot/replay construction does not itself constitute the general host-memory-by-reference launch ABI identified in the shared scope statement.”
- **C8 4**: The fixture/production distinction is actionable and matches the actual fixture and allocator source. The defect is accurately presented as an ambiguity rather than a missing primitive. The remaining clarity issue is distinguishing original C requested size from the ABI-rounded primitive requested size. *Change:* §17.1: “For successful realloc of a non-null live C allocation, old requested size means the original C byte count, including the checked calloc product, excluding rounding, padding and metadata.” Example: malloc(1) followed by realloc(p,48) preserves one byte although the original primitive payload request was 16.

Suggestions:
1. §17.1: add “Old requested size means the original C request, excluding ABI rounding, padding and metadata.” For malloc(1) followed by realloc(p,48), preserve one byte, not 16.
2. Conformance vectors: add the identity-bound production case with heap=64 yielding return 4112, bump 4160, five records and code 0; heap=32 yielding no malloc return, bump 4128, four successful records and code 2. Execute reversal of metadata/list stores as well as primitive history.
3. §17.1: add “Prefix retention describes forward execution before cleanup or reversal and does not waive coherent-oracle workspace restoration or the version-specific R-fault provisions of §§17.5–17.6.”

## codex

Both round-1 B1 items are resolved. Allocation arithmetic, primitive-history claims and catalog preservation check out; no new S0 issue or regression was found. Acceptance does not claim implementation of the separately identified mixed-launch contract.

**Path to accept:** Accepted as a proposal under the stated publication rules. To raise C6 from 4 to 5, supply the identity-bound production execution/reversal vector specified above; to raise C8, define C requested size explicitly.

- **C1 5**: Both maintained §17.1 texts preserve the same allocation model. The proposed addition retains ISA §7.1's exact bump, requested-size records, liveness and nonreclamation; allocator metadata remains ordinary memory. *Change:* Optional §17.1 clarification: 'An alloc(0) probe consumes one heap byte and one allocation-table entry, records requested size zero, and supplies no accessible payload bytes.'
- **C2 5**: Dialect §3.1 supplies alloc/free/fault primitives. The inspected bump.c implements bookkeeping and cursor refresh with those primitives and ordinary operations; no allocation-query instruction is necessary. *Change:* No change required.
- **C3 5**: Per-primitive failure atomicity and retained successful prefixes agree with ISA §§7.1/7.4 and dialect §§17.5–17.6. Metadata reuse changes ordinary bytes without reclaiming primitive allocations. Existing oracle cleanup obligations remain applicable. *Change:* Optional §17.1 sentence: 'Prefix retention describes the forward state at failure; oracle workspace restoration and eligible run reversal remain governed by their existing contracts.'
- **C4 5**: The traces reproduce: [3,13,16] uses 32 bytes and three records; [3,0,12,16,32] uses 64 bytes and five. At capacity 32, production faults with code 2 at bump 4128 after four successful records. Additional bookkeeping and replay costs are explicitly charged. *Change:* In 'Alternatives and worked witness', add: 'These allocation-only totals assume empty metadata lists, sufficient other resources and no additional prologue allocations; entry replay and shadow-stack backing are charged separately when present.'
- **C5 5**: The mixed-object paragraph scopes traces, budgets and body identities to the selected closure. Publication and re-pinning requirements agree with §§19.9/23. In-memory application of both additions preserves every existing fenced example/hash block in both texts; no ISA catalog amendment is introduced. *Change:* No change required.
- **C6 4**: check_rev2.py exited 0 with all eight PASS lines. Its allocation assertions establish the arithmetic and failure prefix, but do not execute production metadata stores or mixed launch. The note accurately limits its verification claims and requests a separate production vector. *Change:* For the §17.1 production vector, state: 'Bind the materialised-body identity, base 4096, alignment 16, empty metadata lists and sufficient other resources. Heap=64 returns 4112 with bump=4160 and five records; heap=32 faults with code 2, no malloc return, bump=4128 and four records. Independently execute metadata-store reversal and identical replay.'
- **C7 5**: Both previous applicability omissions are repaired. The paragraph preserves native host code subject to existing promotion rules; the incorporated shared statement explicitly identifies remaining mixed-launch and host-memory contract work. Dynamic bookkeeping preserves SQLite/Julia allocator scope without a fixed metadata cap. *Change:* No change required.
- **C8 4**: The fixture/production distinction is actionable, and the cited allocation, comparison and publication clauses support it. 'Requested size' would be clearer if it explicitly distinguished the C request from the rounded primitive request. *Change:* In §17.1, add: 'For realloc, old requested size is the original C byte count, including the checked calloc product, not the ABI-rounded primitive extent or padding; malloc(1) has C requested size 1 even when its primitive payload request is 16.'

Suggestions:
1. In 'Fat-object applicability', optionally add: 'The §8.5 reference governs oracle entry-state snapshot/replay; it does not itself define general host-memory-by-reference launch. The remaining mapping, lifetime, aliasing, synchronisation, writeback and reversal obligations are those explicitly listed in fat-object-scope.md.'
2. In 'Alternatives and worked witness', make the information-loss example explicit: 'For primitive-only histories alloc(16); alloc(32) and alloc(32); alloc(16), the first pointer is p and the final bump is p+48, while the first requested sizes differ.' This avoids confusing that example with the production wrapper's additional allocations.
3. In 'Release and route', replace 'no ISA 0.9 K or ISA 0.10 dependency' with: 'This clarification introduces no new ISA dependency; the 0.2 map retains its existing fault/reversal blockers, and the 0.3 map retains its existing ISA 0.9 dependencies.'
