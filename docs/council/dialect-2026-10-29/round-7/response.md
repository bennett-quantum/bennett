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

## Remaining groups

R7-CODEX-02/03 and R7-CODEX-04 are being implemented by the same editor; the
final receipt and their derivations follow in subsequent commits.
