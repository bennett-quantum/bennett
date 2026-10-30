# Round-6 response — draft 0.2.7

Source: the full blocking text in round-6/out-sol.json and out-codex.json,
with round-5 fixes retained. Surgical corrections; ISA grading target remains
0.8. All four findings are resolved together with their checker cases. No
capability is narrowed; no decline, partial, ISA edit or push.

## SOL-R6-01 — resolved

Sections: §9.2, §7.3, §16.2–§16.3, §19.9; Appendix B.
Hand derivation before editing: the source alloca reserves 24 bytes. The fixed
linked fixture saves the old sp in an 8-byte header and aligns to 8: start=8,
end=32. A baseline size 16 therefore faults; 32 admits the frame. Since the
wrapper's size constant participates in the interface hash, selecting 32 by
H16 and rematching against the resulting H32 would select 16 again. No fixed
point exists for that table. Both LLVM 18 and 23 verify and retain the original
alloca/store/load at default<O0> (probes in scripts/.tmp/round6-probes/budget-o0-*.ll).

§9.2 now resolves region-key/symbol/default baselines without identity entries,
freezes capacities from effective defaults, all raw entries (matched or not),
and static non-sentinel record fields, hashes a provisional object, and overlays
identity-selected components once. It never rematches the final object. Explicit
marker records and sentinels retain precedence. Each shape records selection_identity,
final semantic identity, resolved components and frozen capacities. Launch tokens
bind the final identity and resolved tuple. §7.3 preserves final semantic identity;
§16.2 states which sstack to emit, §16.3 fixes capacities before lookup, and §19.9
requires both identities in the resolved table/build record.

Witnesses: n-budget-stage is the source/normalise-out pair; budget-stage-runtime
appends an explicit, fixed linked helper fixture (one valid frame on this path,
no hidden shadow frames). This is a canonical map of that stated materialised
function and linked input, not the earlier entry-stack microvector substituted
for the source. budget-stage gives the actual canonical JSON table and pinned
state results, using adequate fixed steps/heap/stack/depth = 10000/64/512/16.
The independent Rust interpreter computes:

- H16 = `5abf922254697a7876cb137143c5142a7a5dd29ef77cb0183704044a09b9ab5d`.
- H32 = `d32a6a29f9dc1a2fc8baa1f2e07f782e4b5ceed981ca5f82fc780ef4c1b36c82`.
- H16, input 7: code 2, payload 0, 43 steps.
- H16-keyed sstack=32 overlay: final H32, wrapper constant 32, code 0,
  payload 7, 316 steps; the build record retains selection_identity=H16.
- A steps-only overlay selecting zero steps preserves H16, changes the token
  tuple, and executes with code 1/payload 0/steps 0.

Checker: dialect_meta.stage_budget performs the two builds under identical frozen
capacities; dialect_map emits the actual wrapper/helper calls; dialect_round6.
check_budget_stage checks the canonical source pair, reproduces both hashes,
checks each ISA object, examines the final wrapper, compares all resolved fields,
and executes the final-object budget tuple through run-oracle. The driver and
state families both execute this witness. Its resolved record is saved as
budget-stage-resolved.json in the run directory. test_round6_budget_staging
covers unmatched-entry maxima, region-key priority, once-only selection and
steps-only identity; it failed without the staging implementation. The execution
mutation test changes final_sstack and must fail. No ISA 0.8 change is needed.

## R6-CODEX-01 — resolved

Sections: §5.2 PT2/PT6, the pt2-wrap witness; Appendix B. §16.4's canonical
concrete GEP rows are retained.
Hand derivation before editing: P=64, I=32, and index 4294967296 truncates to
zero; stride is one, so accumulated Delta=0 modulo 2^32. The pointer is exactly
@tab, its load is FN(body), candidates={body}, and invocation succeeds.
The old checker instead gave (tab,4294967296) and no loaded function; the new
unit regression observed that failure before implementation.

PT2 now explicitly shares §16.4's finite-width computation, including constant
expressions, signed index extension/truncation, modular scaling/accumulation and
preserved bits above I. It takes the union over unknown base bits consistent
with layout, allocation extent and alignment, copies AV for zero Delta, and
propagates unknown-address alternatives through PT6 instead of dropping them.
Dimensions set stride, never index bounds. The implementation retains original
base provenance for §6.4: an unknown-address alternative introduced by analysis
is not itself proof of host escape. This preserves the existing handle-table,
cross-entry and descriptor corpus; actual host-origin stores still reject under
the existing maintainer restriction. No new rejection was added.

Witness pt2-wrap recognises AV(%p)={(tab,0)}, AV(%f)={FN(body)} and candidates={body}.
The state adapter runs default<O0> then instcombine on both LLVM 18 and 23,
checks both candidate sets, requires the folded operand to be @body, and executes
native dispatch with calls=1/trap=0. The observed fold is
`call void @__bennett_adj(ptr nonnull @body, ptr null, ptr null)` on both majors.
The fold occurs while the custom DataLayout is still attached, before clang
installs the host layout (the same convention as the existing pointer vectors).
An additional direct probe ran the O0 dispatch through lli-18 successfully;
lli-23 refuses the target-incompatible custom DataLayout, so the checker uses
the independent fold plus native execution on both majors rather than claiming
that JIT path ran. Units: test_round6_wrapped_gep (including modular scaling and
negative indices), test_round6_gep_constant_expression (including retained host
escape restriction), test_round6_execution (wrong call count fails).
No ISA 0.8 gap: the existing modular integer/GEP map suffices.

## R6-CODEX-02 — resolved

Sections: §3.4, §5.2 PT5, §12.2 N3/N4, with execution still defined on the
materialised module under §12.1/§18.1/§18.7; Appendix B.
Hand derivation before editing: after annotation removal, n ranges over all
i64 inputs; n&3 gives {0,1,2,3}; or 1 gives {1,3}. At n=2, width=3; two X
operations on wire 2 restore zero and qfree succeeds. The old parameter-range
rule gave only {1}; the regression observed that failure before the fix.

Removed range attributes/metadata now cannot restrict a verdict, candidate set,
descriptor shape or dispatch domain. Only bounds established independently by
materialised instructions may narrow the set; masks and remainder rules remain.
N3 explicitly ignores ranges removed by N3/N4 when computing reference domains,
and §3.4 no longer advertises erased annotations as finite-width evidence.
The alternative of a new checked runtime precondition was declined as a repair
choice because it would narrow the annotation-free reference executions; this
finding itself is fully resolved, not declined.

Witnesses: pt5-range is the LLVM-23 parameter-attribute example; pt5-range-load
is the equivalent LLVM-18/23 load-!range example. Both infer {1,3} and accept.
Their state adapters execute the actual N3/N4-stripped module on clang 18/23
with dispatch constrained to the inferred set: input 2, width 3, both gates
successful, live_after=0, trap=0. The original annotation-bearing function is
not executed outside its source precondition. Both original forms verify through
O0 on their applicable majors; independent annotation-free arithmetic probes
fold n=2 to `ret i64 3` on LLVM 18/23. Units: test_round6_removed_range and
state/result mutations in test_round6_execution. No new ISA capability needed.

## R6-CODEX-03 — resolved

Sections: §12.2 N9, normalisation/native/map witnesses; Appendix B.
Hand derivation before editing: old=0xf0=240, v=0xcc=204; and gives 0xc0;
xor 0xff gives 0x3f=63. The atomic result is the old byte, independently of
the stored new byte. The old normaliser raised `N9 atomicrmw nand`; the new
unit reproduced that error before implementation.

N9 now emits `%nz.a.r = and iW %nz.l.r, v` then
`%nz.v.r = xor iW %nz.a.r, -1`, with no flags, followed by the common store
and old-result substitution. The ordinary-op template is limited to
add/sub/and/or/xor. Sweeping the LLVM 18/23 AtomicRMWInst enumerations found
no additional uncovered normative exception after explicitly spelling the FP
mapping: fadd/fsub, fmax/fmin -> maxnum/minnum, fmaximum/fminimum ->
maximum/minimum, fmaximumnum/fminimumnum -> maximumnum/minimumnum, then N32.
The checker now handles all enumerated integer and floating exceptions rather
than relying on the nonexistent ordinary opcode spelling.

Witness n-atomic-nand includes the council's @cell/@f module and an old-result
probe. Its exact normalise-out has load/and/xor/store/load/ret for @f. Native
source/output on clang 18/23 give f()=63 and old(240)=[240,63], code 0.
Independent lli probes on LLVM 18/23 also succeed. atomic-nand pins the map,
ISA object, hashes and interpreter result: code 0, payload 63, **16 rows**,
including wrapper, address/constant/bounds rows and the two logical operations.
Units: test_round6_nand, test_round6_atomic_sweep (all 23 operation names
normalise and verify with LLVM 23), test_round6_execution (wrong expected new
value fails). No ISA 0.8 gap; ordinary and/xor suffice.

## Validation and retained dependencies

Final freeze: **2651/2651 passed, 0 failed, 0 blocked/unavailable**, from the
2598/2598 baseline. **67 checker unit tests and 4 legacy runtime tests pass.**
All four fixes and their paired checker cases are commit `8c7fb5264384c53e8659b101aa30c4416ef4d4ee`.
Spec SHA-256: `d183190bd4d8f924e617b2de570beda317175cb388b2bead635bcd847275e09c`.
Checker/source snapshot: `90c2c9374896f2ef8ed3abd796348ad6b2afedaf21179ad29b01d3ab5857e875`.
Independent interpreter: `0bc842653c2cbf860fec90a79ac2115d3d5e11fa`; source fingerprint
`1d4920cd86333b6902202e1472245b917dd1340a62c7166aaadc35a03784743d`. Final dependency HEAD matched
at validation end; the normative/checker source manifest stayed unchanged during
the final freeze. Both PROGRESS files and dialect_check.LAST-RUN.json contain
the complete family receipt and source hashes (receipt commit `95c3cd3`).

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
| native | 30 | 0 | 0 |
| normalise | 39 | 0 | 0 |
| parse | 716 | 0 | 0 |
| recognise | 138 | 0 | 0 |
| run-oracle | 22 | 0 | 0 |
| run-program | 5 | 0 | 0 |
| seeds | 1 | 0 | 0 |
| state | 61 | 0 | 0 |
| step-check | 6 | 0 | 0 |
| tdl | 10 | 0 | 0 |
| trace | 3 | 0 | 0 |
| xrefs | 1388 | 0 | 0 |
| **Total** | **2651** | **0** | **0** |

The exact inherited gate command is retained, including its round5-fixes-freeze.json
output path; this run's receipt is the round-6 receipt in both PROGRESS files.
The baseline is the recorded 2598/2598 round-5 freeze. Development runs are not
freeze receipts. No example or expectation was removed or weakened.

These four repairs need no ISA change. Existing named ISA-0.8 dependencies in
§25.1 remain explicit, including ISA-4 (dynamic register-file/index selection),
ISA-1 (device-value budget-token construction), ISA-12 (QREG transport in R),
and ISA-7 (typed R faults preserving the executed reversible prefix). Their
passing blocked-verdict checks do not claim those capabilities landed in 0.8.
