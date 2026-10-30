# Round-7 response — draft 0.2.8

Source: full blocking text in out-sol.json and out-codex.json. Surgical edits;
ISA grading target remains 0.8. No narrowing, rejection, ISA edit or push.

## SOL-R7-01 ≡ R7-CODEX-01 — resolved

Sections: §5.2 PT4/PT5/PT6; pointer-integer examples; Appendix B; §23 version.
Hand derivation before editing: -2^63 + -2^63 = 0 modulo 2^64, so p=@tab,
f=@body and dispatch succeeds. ptrtoint to i128, +2^64, inttoptr to a 64-bit
pointer also returns @tab by truncation. Computing other-tab and adding it
to tab instead reaches another allocation; its loaded function must remain
represented even when the address is numerically unknown to the analysis.

PT4 copies only bit-preserving conversions and otherwise applies the actual
width conversion. PT5 uses modular displacements and preserves the base
provenance with explicit EXT/top alternatives for out-of-object or unrepresentable
images. The wildcard fallback is retained for other operations and uncertain
integer widening. PT6 propagates the address top flag even with no matching slot.
The erased-range rule and all prior PT2 tests remain. Numerical uncertainty is
not host provenance. No LLVM optimisation is required for admission.

Witnesses pt5-int-wrap, pt4-wide-wrap and pt6-unknown-address all accept with
candidates={body}. dialect_round7.check_state executes their original O0 and
instcombine forms with LLVM 18/23 recognition, then native marker dispatch:
exactly one successful call, trap=0. Only the first is required to fold to body;
LLVM 18 retains a wide constant expression for the i128 case. Both native forms
execute independently. The explicit-layout pointer source verifies on both majors;
clang code generation uses its complete host layout with the same 64-bit pointer
semantics (no claim that lli-23 accepts the abbreviated layout).

Units test_round7_pointer_arithmetic and test_round7_pointer_execution check
modular identity, wide truncation, address-TOP-only loads and wrong-call-count
mutations; the arithmetic test first failed at offset 2^64. The paired group gate
passes 2667/2667 (baseline 2651). Existing ISA 0.8 integer/cast rows suffice.

## R7-CODEX-02 — resolved

Sections: §5.2 PT10, pt10-lane-zero, Appendix B. Hand derivation before editing:
N15 maps unsigned indices >=2 to zero, so extraction from <1,3> has the finite
set {0,1,3}, and add one gives widths {1,2,4}. At indices 0,1,2,-1 the widths
are 2,4,1,1. The original rule's union {1,3} omitted the two width-1 executions.

PT10 now includes zero iff the represented unsigned index set permits an
out-of-range value, including top when 2^K>L. Proven in-range sets do not add
zero; the i1/two-lane regression keeps {1,3}. Insertions retain every old lane
unless certainly replaced, adding the inserted value only where selectable;
the out-of-range alternative preserves all lanes. Zero adds no ROOT.

Witness pt10-lane-zero includes the full marker allocation/free module. Its
recognition and dialect_round7.check_lanes require lane={0,1,3}, width={1,2,4},
verdict=accept. LLVM 18/23 O0 source verification is followed by actual N15/N21
materialisation and native execution with dispatch constrained to that inferred
width set. All four host indices allocate the stated width and free cleanly,
live_after=0/trap=0. No input precondition, new rejection or BLK-1 was introduced.
Units test_round7_lane_domains/execution first observed the missing zero, then
passed; wrong-width mutation fails. The arithmetic refinement uses PT10 atoms
for acyclic lane expressions, preserving the existing conservative loop fallback.
No ISA 0.8 change is needed.

## R7-CODEX-03 — resolved

Sections: §12.2 N15, §12.6, PT10; Appendix B. Hand derivation before editing:
2 and unsigned i32 -1 both exceed the two-lane length. Extraction gives zero;
insertion leaves <5,9> unchanged, so extracting lane 0 afterwards gives 5.
The old lane-renaming rule had no applicable lane (the regression raised
IndexError at 2); its negative-index path was also not a constant policy.

N15 now applies to every integer index, interpreting negative spellings as
unsigned bit patterns. Constant in-range indices proceed to N21; constant
out-of-range extraction/insertion is replaced by zero/unchanged vector and
deleted. §12.6's lane renaming is restricted to the remaining in-range cases.
This chooses the same policy as dynamic N15, without rejecting valid input.

Witness n-constant-lane is a literal normalise-in/out pair with four functions:
f/negative return 0, g/gnegative return 5. Both LLVM majors verify original
modules through O0 and execute the materialised output natively. Original
poison/freeze results are not falsely claimed to equal the chosen materialised
values. test_round7_constant_lanes and test_round7_lane_execution cover the
pair, both index spellings, native results and a wrong-result mutation.
No ISA change is needed.

The paired lane group passes 2680/2680; all 72 checker units pass.

## Remaining group

R7-CODEX-04 is in progress; final receipt follows its paired commit.
