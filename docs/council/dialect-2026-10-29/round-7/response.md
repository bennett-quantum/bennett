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

## R7-CODEX-04 — resolved

Sections: §13.4, §13.6 portable libm pairs, Appendix B. Hand derivation before
editing: x86_fp80 has 64 significand bits; binary128 has 113. Thus converting
fp128 to x86_fp80 is narrowing, never an exact fpext. ppc_fp128 and fp128 each
have a 128-bit representation but different numeric formats, so their direct
fpext is invalid too. LLVM 18 and 23 both accept the original sin intrinsic
sources on x86-64, AArch64 and RISC-V64 and reject the old cast recipe with
exit 1 and `invalid cast opcode` (the state adapter records the full diagnostic).

I selected the direct own-format soft-float-library alternative explicitly
allowed by the finding/brief. float/double/native-long-double scalar libm calls
remain; all other source formats call their own §13.1 carrier function
`__bennett_sf_<name>_<suffix>` with input/output bitcasts only to that format's
own carrier. No numeric conversion through long double occurs. This also
covers half/bfloat and x86_fp80 on fp128-long-double targets. The ABI fixes
operand order, non-FP operand types, result naming, NaN canonicalisation, signed
zero policy and the linked versioned implementation in both builds. It promises
bit-exact determinism, retaining the draft's explicit absence of a universal
correct-rounding claim. These are linked arith/runtimes bitcode functions, not
new ISA instructions or unresolved host calls.

Powi retains repeated squaring and its integer exponent (the carrier symbol
includes the exponent width to prevent signature collisions). Sincos, sincospi
and modf retain their named operations and pair order through carrier aggregate
results reconstructed field by field. Their scalar/pair carrier route is
specified for every format, avoiding an invented C pointer-output ABI.

Six normalisation pairs cover x86 fp128/ppc_fp128, AArch64 ppc_fp128/x86_fp80,
and RISC-V64 ppc_fp128/x86_fp80. Each source/output verifies with exit 0 on both
LLVM majors. Four state cases execute the fp128/ppc_fp128 materialised carrier
bodies: +0 -> +0 and 1+2^-100, whose low bits would be lost through x87 long
double. Independent libquadmath numerical execution gives:

| Source format | Input carrier (hex) | Result carrier (hex) |
|---|---|---|
| fp128 | 3fff0000000000000000000000001000 | 3ffeaed548f090cee0418dd3d2139b69 |
| ppc_fp128 | 39b00000000000003ff0000000000000 | 3c406374f484e6da3feaed548f090cee |

The ppc carrier is APFloat's high-double in the low 64 bits, low-double in
the high 64 bits. LLVM 23 independently prints the corresponding numeric
constant as f0x39B00000000000003FF0000000000000. Native execution links the
integer-carrier body to scripts/round7_libm.c, an explicitly test-only numerical
fixture using sinq and numerical double-double split/reassembly. It is not a
production soft-float library implementation and no cross-native ARM/RISC-V
execution is claimed; those modules are independently verified at their target
triples before host execution of the same carrier body.

Checker: dialect_normalise.Normaliser.fp emits the new ABI; dialect_round7.
check_libm compares each exact pair, verifies each triple, executes the stated
vectors and requires the old casts to fail with the exact diagnostic. Units
test_round7_fp_formats/execution first failed for the missing own-format ABI,
then passed across 7 formats x 3 triples x 2 LLVM majors, including powi/pair
verification and wrong-result mutations. No ISA 0.8 change is required.

## Additional no-narrowing regression

During the final review I derived a wrapped pointer back to a global handle
slot. Synthetic EXT/top from its intermediate arithmetic was incorrectly
being treated as actual host provenance by the escape check. The deciding
existing PT2 sentence says numerical uncertainty does not itself establish host
escape. The checker now follows the arithmetic/cast base origins for that
check. test_round7_pointer_origin first observed an erroneous rejection, then
passed with accept for the global-origin case and the unchanged rejection for
a real host-pointer escape. This completes R7-CODEX-01's provenance obligation;
no spec capability was shrunk to fit conservative numerical analysis.

## Validation and retained dependencies

Final freeze **2731/2731 passed, 0 failed, 0 blocked/unavailable**;
baseline **2651 → 2731**. **75 checker units and 4 legacy runtime tests pass**.
Pointer group: `8f83291`; lane group: `8694e5f`; final FP/provenance group: `d627fd10b3feae73e25f04b189ddc90d549a6fa5`.
Spec SHA-256: `8f493e36ab5dee9a934d55312767589b81e7961ab22877bc1d0db5cf4ed95cdc`.
Checker/source snapshot: `b61294a4199b057417f5f23b9c0feeab49bb86aec84a8845f631a4e72390680e`.
Both PROGRESS files and dialect_check.LAST-RUN.json carry the family table,
source-file hashes and interpreter fingerprints. The spec/checker manifest did
not change during the final freeze. The exact inherited command, including its
historical round5-fixes-freeze.json filename, was retained.

The concurrently edited ISA checkout advanced during validation. Independent
execution used immutable initial snapshot `c37b9698c6208303cb63498626649ec183179171`
(fingerprint `bfc88c5be2029d66bc77e59c15f21cbf9dd6313eaf8069ff2cdd028d1db41290`) and final snapshot
`0b70157c65ddf91184e9ef9e753dd61ab94a7c0b` (fingerprint
`cebb8019f4e657361ce395b89bab04efb590fdd157bda73281c2ea18b48d8097`). The final dependency HEAD **and source files** matched
at validation end (checked immediately after the green gate); the working
interpreter sources changed again while the receipts were written. The immutable
snapshots above identify the executed code regardless of that later work. The development run rejected by the HEAD-during-build guard
was discarded and restarted; no guard or expectation was relaxed.

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
| parse | 770 | 0 | 0 |
| recognise | 142 | 0 | 0 |
| run-oracle | 22 | 0 | 0 |
| run-program | 5 | 0 | 0 |
| seeds | 1 | 0 | 0 |
| state | 70 | 0 | 0 |
| step-check | 6 | 0 | 0 |
| tdl | 10 | 0 | 0 |
| trace | 3 | 0 | 0 |
| xrefs | 1393 | 0 | 0 |
| **Total** | **2731** | **0** | **0** |

There are **no declines or partials**, and no new ISA-0.8 gap. Existing named
§25.1 dependencies remain: ISA-4 dynamic register-file/index selection; ISA-1
construction of budget tokens from device values; ISA-12 QREG transport in R;
ISA-7 typed R faults preserving the executed reversible prefix. Those dependency
verdict checks passing do not claim these capabilities execute on ISA 0.8.
No new ISA change is requested by this round; the five reviewed witnesses stay
admissible. No ISA, worklog, HANDOFF or brief file was edited, and nothing was pushed.
