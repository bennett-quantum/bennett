# Round-8 response — draft 0.2.10

Source: both members' full round-8 JSON blockers and report. Surgical edits;
ISA grading target remains 0.8. No narrowing, rejection, ISA edit or push.

## SOL-R8-01 ≡ R8-CODEX-02 — resolved

Sections: §5.2 introduction and PT3, DB/DN/DS witnesses, Appendix B.
Hand derivation before editing: under the witnesses' little-endian DataLayout,
<1,1> packs to 1 | (1 << 8) = 257; <0,1> packs to 256. Zext to i64
preserves each value. Conversely 769 = 1 + (3 << 8) splits into <1,3>;
extracting lane 1 gives width 3. LLVM 18 and 23 independently verify the
original O0 modules and instcombine folds the allocation widths accordingly.

PT3 now copies corresponding lanes only for equal lane counts and equal
per-lane representation widths (scalar = one lane). Other geometries use the
virtual N21 bit-string expansion during S2, before verdicts, candidates, shapes
and dispatch domains freeze. PT4/PT5 evaluate its transfers; finite lane INT
sets denote their Cartesian product, capped per resulting lane. The text keeps
sol's explicit prohibition on copying a source-lane INT as a packed scalar,
and codex's constant-expression/fixed-vscale, unknown-bit and provenance rules.
No finite packing witness is rejected or assigned BLK-1.

Checker dialect_flow.Flow.bitcast directly evaluates that finite expansion,
projecting source bits to each output lane before taking products so the K cap
cannot destroy precision because of irrelevant bits. Unknown bits use non-handle
top; explicit object/ROOT provenance is retained subject to unchanged §6.2.
Witnesses pt3-pack257, pt3-pack256 and pt3-unpack have exact scalar AV domains
{257}, {256}, {3} and the matching finite width domains. dialect_round8.check_state
verifies source O0/instcombine/materialised IR and executes all three forms with
clang 18/23 at O0/O3. Its marker harness guards every received width against S2,
checks gate operation/index/bounds, free count and clean workspace, and requires
exit 0. The 257 case executes two X gates at 256, final bit=0; every case frees
once with live_after=0/code=0.

Units test_round8_bitcast_domains failed in all six witness/major subtests
before the repair: source lane maps remained on the scalars, and unpack falsely
blocked on ISA4. They now pass. Transfer units cover Cartesian products, inverse
geometry, constant expressions, per-output K, DataLayout order and unknown
bits with explicit provenance. Native units also require wrong-width mutations
to fail. No ISA change is needed.

## R8-CODEX-01 — resolved

Sections: §5.2 initial seeding, PT1/PT6/PT8; §8.4 explanatory sentence;
DB/DN/DS witnesses; Appendix B. Existing N24 and §§17.1/17.3 semantics remain.
Hand derivation before editing: the eight zero-filled allocation bytes contribute
INT(0) on the path without a store; the conditional i64 store contributes INT(1).
Freeze preserves both; extraction from <1,3> gives widths {1,3}. The same
reasoning applies to zero-filled heap storage. A copy of those source bytes into
a global initially holding 1 must carry the zero possibility too.

The initial-seeding paragraph now adopts codex's zero-byte initial-image rule
for each zero-filled alloca/allocation-site extent, with symbolic nonconstant
extents. Stores union and never erase the initial possibilities. PT6 includes
the all-zero representation for a possibly valid load wholly within the extent,
unioned with every overlapping store/copy under the existing interval rules;
PT8 propagates initial bytes. Zero adds no ROOT. Region inputs, replayed caller
bytes and other nonzero-initialised contents keep their specified sources.
This is neither an input precondition nor an ISA blocker.

Checker dialect_flow keeps zero_images as byte intervals separately from typed
memory atoms, so i8/i16/i64 and subrange reads decode zero without pretending
an overlapping typed integer is a whole load. Unknown allocation extents remain
symbolic. copy_memory propagates the initial image alongside the unchanged
interval/representation rules for written atoms. Recognition covers the §5.1
allocation names and allockind/allocsize declarations; copied allocator sources
remain additional possibilities. No globals or EXT/region inputs are zeroed by
this rule.

Witness pt6-zero-stack is the member's complete conditional alloca module;
pt6-zero-heap is its zero-filled calloc companion (including free of the heap
object); pt8-zero-copy copies the stack bytes into a mutable global initially 1.
Each accepts with AV(raw)=AV(idx)={INT(0),INT(1)} and VS(width)={1,3}.
dialect_round8.check_state verifies original source through LLVM 18/23 O0,
materialises N24/N8/N15/N21, independently verifies the result and runs it with
clang 18/23 at O0/O3. False/true allocate widths 1/3, with width-membership
guards tied to S2, one clean free per invocation, live_after=0/code=0 and exit 0.
For stack/copy, execution uses the repository zero-filled shadow-stack seed;
calloc supplies the heap companion's zero-filled storage. No execution of an
uninitialised source LLVM load is claimed as the dialect's oracle.

Units test_round8_zero_domains first failed all six witness/major subtests with
{1} instead of {0,1}, then passed. test_round8_zero_images checks typed/subrange
zero decoding, boundary exclusion, symbolic stack/heap/allocsize extents, PT8
subranges, overlapping-store TOP, no ROOT and preservation of nonzero global/EXT
sources. Native units require wrong-width mutations to fail.

The first full gate exposed a checker bookkeeping bug: kind0 from initial zero
was counted as a valid descriptor shape, changing five existing counts to
2/4/6/4/2. §8.4 already defines only five valid kinds and T-IFACE outside the
table. A new five-subtest regression failed, then passed after valid-shape
counting intersected the unchanged table {1,2,3,4,5}. The underlying AV still
contains zero; no initial possibility or runtime fault path was removed and no
existing expected shape count changed. §8.4's non-normative singleton remark
now refers to valid field values, rather than falsely claiming that every
constant store erases the initial image. No ISA change is needed.

## Additional wording and scope

Applied sol's S1 wording correction at §12.1 and Appendix A A23: N33 precedes
N32 so introduced floating-point instructions receive N32; own-format carriers
and bit-exact reconstruction remain §13.4. No normalisation algorithm changed.
Full compatibility is 0.2.10 in the header, §19.9, §23, module-flag recogniser,
version unit and SPEC_VERSIONS.toml. Following spec/README.md, unchanged map and
normalisation subversions stay 0.2.9 and 0.2.8; ISA-owned interface signatures
and their hashes are unchanged and rechecked.

The additional finite arithmetic regression first returned TOP for packed256
plus1; the checker now uses the finite PT3/PT4 domain through PT5, giving257.
This completes the virtual-expansion transfer rather than relying on LLVM
optimisation to preserve admission.

## Validation and retained dependencies

Final freeze **2767/2767 passed, 0 failed, 0 blocked/unavailable**; baseline
**2732 → 2767**. All **84 checker units and 7 legacy runtime tests pass**.
PT3 green group `4fecd06`; zero-image/version/arithmetic group `023f5a771a814270634db3be9cfde88ded69f975`.
The intermediate five-shape-failure development gate is archived separately
and is not a receipt. No S0 blocker is declined
or partial. Both repairs need no new ISA capability or exact ISA change. Existing
§25.1 ISA-0.8 dependencies remain unchanged: dynamic-width/register-id operations
(ISA4), device budget minting (ISA1), QREG transport/allocation in R (ISA12),
and typed R faults preserving the reversible prefix (ISA7). Passing their
blocked-verdict checks does not claim those capabilities execute on ISA0.8.

Codex's separate nonblocking PT12 atomic-update suggestion is recorded for
follow-up as **b-dialect-spec-0y2**. It was outside this brief's two S0 groups
and is not claimed resolved. Sol's additional controlled-witness/budget/naming
conformance suggestions were not part of the two blocker repairs. No S0
blocker is declined or partially resolved.

Spec SHA-256: `d4f3c1a88391cc147f8c8fa4f80f82852e3ebe6f880610fc16cd5151f33d7206`.
Checker/source manifest SHA-256: `74372f9f2a7077e5eba1063ed687115e4ed0854b9732abb061b236b69efe16ff`.
Interpreter commit: `697c9a8d64690f0f467a8677a445f4db283a73fc`; fingerprint
`ddc1a303cd52bd828744e7aa4f85b17127a2869d6ad59da39934f7a6e5bf6c3e`. Interpreter HEAD/source files matched
at receipt writing; all 105 normative/checker/harness/corpus source files matched
before/after the final gate and the committed code snapshot. Both PROGRESS files
and scripts/dialect_check.LAST-RUN.json carry the receipt and family table
(receipt commit `d0a160d`).
The exact inherited command and historical round5-fixes-freeze.json filename
were retained. All 22 published ISA objects check; all 9 published hash checks
pass, without changing ISA-owned signatures or editing the ISA repository.
No pushes or edits outside owned paths.

| Family | Passed | Failed | Blocked |
|---|---:|---:|---:|
| asm | 1 | 0 | 0 |
| blocker | 19 | 0 | 0 |
| cc-run | 8 | 0 | 0 |
| check | 22 | 0 | 0 |
| coverage | 125 | 0 | 0 |
| driver | 2 | 0 | 0 |
| events | 3 | 0 | 0 |
| frontend | 21 | 0 | 0 |
| hash | 9 | 0 | 0 |
| header | 1 | 0 | 0 |
| map | 21 | 0 | 0 |
| native | 31 | 0 | 0 |
| normalise | 46 | 0 | 0 |
| parse | 788 | 0 | 0 |
| recognise | 148 | 0 | 0 |
| run-oracle | 22 | 0 | 0 |
| run-program | 5 | 0 | 0 |
| seeds | 1 | 0 | 0 |
| state | 76 | 0 | 0 |
| step-check | 6 | 0 | 0 |
| tdl | 10 | 0 | 0 |
| trace | 3 | 0 | 0 |
| xrefs | 1399 | 0 | 0 |
| **Total** | **2767** | **0** | **0** |
