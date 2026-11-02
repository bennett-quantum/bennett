# Council — pass2-2cg-2026-11-02 round 1

Document snapshot sha256 a2c8ce8418ac; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 4 | 4 | 4.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 4 | 4 | 4.0 |  |
| C8 | 4 | 5 | 4.5 |  |

Overall mean: 4.56

Verdicts: **sol: revise**, **codex: revise**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: no**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 1 (blocking 1), codex: core 0 / contract 1 (blocking 1)

## Blocking issues

- **[sol] B1** (Recommended exact spec diff, §17.1 in both maintained texts; contract): The standing bennett-4ht check requires a change governing host memory by reference to state its mixed-fat-object use. This diff permits ordinary allocator metadata in §17.1's shared classical memory, but states obligations only for device and native materialisation. Under §17.7, native materialisation here is the comparison binary; it does not itself explain the production native host image. The proposal never states how unrelated host code remains native or how shared allocator metadata follows the existing boundary rules. Existing §§4.2–4.4, 8.5 and 19.4–19.5 provide a route, so this needs an applicability statement rather than a new ABI. *Fix:* Append to §17.1 in both maps: 'In a mixed fat object, this bookkeeping allowance applies to runtime code in the selected materialised device closures and their native comparison build; unrelated host code remains native under §§4.2–4.4. Allocations and bookkeeping shared across the host–device boundary follow the shared-memory, promotion and layout rules of §§17.1 and 19.4–19.5, and oracle entry-state transfer under §8.5 preserves the ordinary metadata bytes as well as primitive allocation history. This clarification does not require the native host entry, argv/envp or host-only libc closure to be included in an ISA object.' Use this existing-contract route.
- **[codex] B1** (Recommended exact spec diff — §17.1; Defect and North Star scope; contract): The proposal specifies identical materialised allocator operations, actual budgets and body identities, but does not state how those obligations apply within a mixed fat object containing a native host binary and selected device closures. References to §§17.7/19.1 describe the comparison and linking paths without supplying the explicit applicability statement required by the council's standing mixed-fat-object check. This is that check's required scope omission, not a demonstrated defect in the allocation arithmetic or the accepted host/device split. *Fix:* Append to proposed §17.1 in both maps: "In a mixed fat object, this rule governs the allocator closure selected for a marked device entry and that closure's native comparison build; the surrounding native host binary and host-only libc remain outside the device object. Allocation traces, budgets and runtime-body identities are bound to that selected closure, with shared caller allocation state transferred and charged under §8.5 and boundary addresses governed by §19.5. This clarification does not require whole-program device entry or add host promotion beyond §§4.2–4.3 and 19.4." An illustrative mixed case should retain native main and host-only work while the marked allocator-using closure produces its ISA object and comparison closure.

## sol

The allocation mechanism, trace arithmetic and catalog claims check out. Core accepted. One required mixed-fat-object applicability statement prevents whole-proposal acceptance.

**Path to accept:** Add B1's applicability statement to the proposed §17.1 addition for both maintained texts. No primitive or catalog change is needed; retain the stated publication and consumer re-pin requirements.

- **C1 5**: Both maintained §17.1 texts are identical. ISA 0.8 and 0.9 §7.1 support the stated bump and requested-size rules. The 32-byte/three-record and 64-byte/five-record traces are correct. *Change:* §17.1, optional clarification: 'An alloc(0) address probe consumes one heap byte and one allocation-table entry, records requested size zero, and provides no accessible payload bytes.'
- **C2 5**: The proposed construction uses the three existing §3.1 primitives and ordinary memory operations. Requested-size bookkeeping does not require a new ISA query. *Change:* §17.1, optional sentence: 'This allowance adds no primitive; bookkeeping uses ordinary materialised operations and the published allocation, free and fault primitives.'
- **C3 5**: Preserving a successfully executed prefix at a failing primitive is consistent with primitive failure atomicity and subsequent reversal. Reusing still-live metadata slots changes ordinary data without reclaiming primitive storage or history. *Change:* §17.1, optional sentence: 'Prefix retention describes the state at the failing primitive; oracle workspace cleanup and R-run reversal remain governed by the existing region and fault contracts.'
- **C4 5**: The diff charges probes, padding, metadata and stores rather than importing the thin fixture's costs. The production metadata allocation correctly fails at heap capacity 32 after four successful records and bump 4128. *Change:* §17.1, optional sentence: 'List traversal, metadata stores and reused metadata slots retain their actual step, heap and history charges under the resolved materialised body.'
- **C5 4**: The identity and migration account agrees with §§7.3, 19.9 and 23. In-memory application preserves all existing example blocks; the published ref-0.9 catalog hash checks. The exact diff lacks the mixed-object applicability statement required by the standing check. *Change:* §17.1: add the mixed-fat-object applicability and shared-metadata rule written in B1.
- **C6 4**: The INDEX allocation assertions reproduce. Existing LLVM 18/23 thin-fixture executables match every published output, and existing alignment executables pass six cases each. The proposal appropriately distinguishes these checks from full runtime and rung acceptance, but supplies no tagged production-body execution vector yet. *Change:* §17.1 acceptance vector: state 'For the pinned production body, heap capacity 64 gives requests [3,0,12,16,32], five records and bump 4160; capacity 32 faults with code 2, four records and bump 4128, without returning from malloc. Reverse all metadata stores and primitive history, then reproduce the same execution.'
- **C7 4**: Ordinary metadata preserves the allocator capability needed by SQLite and Julia. The min-size preservation rule agrees with [WG14 N1570 §7.22.3.5](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf#page=367). The required mixed-fat-object statement is missing from the proposal. *Change:* §17.1: explicitly retain native host code outside the selected device closures and route shared allocation metadata through the existing layout, promotion and entry-state contracts, as written in B1.
- **C8 4**: The fixture/production distinction is actionable and supported by bump.c. Defining C requested size separately from the rounded primitive request would make the realloc rule easier to implement correctly. *Change:* §17.1: add 'Old requested size means the original C byte count, including the checked calloc product, rather than the ABI-rounded primitive extent or padding; for malloc(1), that count is 1 even when the primitive payload request is 16.'

Suggestions:
1. §17.1: define requested size explicitly: 'For realloc, old requested size is the original C byte count, not the rounded primitive allocation extent.' Example: malloc(1) records C size 1 alongside a primitive payload request of 16.
2. Alternatives and worked witness: add 'The 64-byte figure assumes empty live/spare metadata lists, alignment 16, sufficient step and table capacity, and no additional prologue allocations; entry replay or shadow-stack allocations are charged separately when present.' Keep the stated allocation-only expected trace unchanged.
3. Release and route: replace the dependency sentence with 'This bookkeeping clarification introduces no new ISA dependency; the 0.2 text retains its existing typed-R-fault and failed-run-reversal blockers, while the 0.3 text uses its existing ISA 0.9 K5/K6 contracts.'
4. Conformance vectors: add 'On metadata-allocation failure, 4112 denotes an allocation in the retained prefix, not a returned malloc result.' Expected state at heap capacity 32 is fault 2, bump 4128 and four primitive records.

## codex

The core clarification is sound, its numerical witnesses reproduce, and its technical citations are accurate. Existing canonical examples remain unchanged. The sole blocker is the explicit mixed-fat-object applicability statement required by the standing council check.

**Path to accept:** Add B1's mixed-fat-object applicability paragraph to the proposed §17.1 append in both maps. No allocation-semantic repair, new ISA primitive or replacement of the existing fixture is needed. Publication should retain the note's stated versioning and separate production-vector obligations.

- **C1 5**: Both maintained §17.1 texts have identical allocation rules. The proposal preserves ISA §7.1's requested-size records, max(n,1) bump, liveness and nonreclamation, while representing allocator bookkeeping as ordinary memory. *Change:* No change required.
- **C2 5**: Dialect §3.1 publishes exactly fault/alloc/free primitives; §16.4 lowers allocation directly. The inspected bump.c implements size retention and cursor refresh using these existing primitives and ordinary stores. No allocation-query instruction is necessary. *Change:* No change required.
- **C3 5**: Per-primitive failure atomicity and retained successful prefixes agree with ISA §§7.1/7.4 and dialect §§17.5–17.6. Metadata stores participate in ordinary reversal; the proposal grants no memory-check exemption. Existing oracle cleanup obligations remain applicable. *Change:* No change required.
- **C4 5**: The INDEX allocation witness reproduced both traces: minimal requests 3,13,16 end at 4128; production requests 3,0,12,16,32 end at 4160. With 32 heap bytes, production faults with code 2 at bump 4128 after four successful records. Additional metadata and probe costs are explicitly charged. *Change:* No change required.
- **C5 4**: Body-specific identity and consumer re-pinning agree with §§7.3/19.9/23. Applying the proposed append in memory leaves existing ISA, hash and run blocks byte-identical in both texts; no ISA catalog change is required. The proposal does not explicitly connect its accounting and identity obligations to a marked closure within a mixed fat object. *Change:* In §17.1 add: "In a mixed fat object, these allocation-trace, budget and runtime-body identity obligations apply to the selected device closure and its native comparison closure, with shared entry state handled under §8.5."
- **C6 4**: The arithmetic witness passes, and its limitation is honestly stated: it does not simulate production metadata stores. The proposed separate production-body vector is appropriate, but its executable, identity-bound specification remains publication work. *Change:* For the new §17.1 tagged vector, state: "Record the materialised-body identity, empty metadata lists, sufficient step/depth capacity and at least five available allocation records." Expected results are heap=64: return 4112, bump=4160, records=5, code=0; heap=32: no malloc return, bump=4128, records=4, code=2. Reversal must restore metadata bytes as well as primitive state.
- **C7 4**: Ordinary dynamic bookkeeping preserves the libc, SQLite and Julia requirements without a fixed metadata cap. However, the note contains no explicit mixed-fat-object applicability statement despite revising allocator budgeting, materialisation and identity obligations; the council's standing check requires one. *Change:* In §17.1 add: "This clarification does not require whole-program device entry: the surrounding native host binary and host-only libc remain outside the device object, subject to the existing placement rules of §§4.2–4.3 and 19.4."
- **C8 5**: The proposed append clearly distinguishes fixture conformance from production-body conformance. Its cited clauses and description of the current allocator are accurate. The claimed ambiguity is supported by the originating request, without falsely claiming that existing text forbids bookkeeping or that realloc remains unimplemented. *Change:* No change required.

Suggestions:
1. In §17.1 clarify the two meanings of requested size: "On successful realloc(p,n) of a non-null live C allocation, old requested size means the original C request, excluding ABI rounding, padding and metadata; preserve its first min(old_requested,n) bytes." For malloc(1) followed by realloc(p,48), the preserved length is 1, although the original primitive payload request was 16.
2. In the new §17.1 production vector, explicitly distinguish the internal payload allocation from a returned malloc value. At heap=32, payload storage at 4112 exists in the retained prefix, but malloc never returns because its metadata allocation faults. Record bump=4128, four successful primitive records and code=2, then verify reversal of the actual allocator stores.
3. After §17.1's failure-prefix sentence, add: "Prefix retention describes forward execution before reversal; it does not waive coherent-oracle cleanup under §18.5 or alter the version-specific R-fault and reversal provisions of §§17.5–17.6."
