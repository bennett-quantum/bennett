# Round-5 response — draft 0.2.6

Source: full round-5 out-sol.json, out-codex.json and out-muse.json findings.
Surgical corrections; ISA grading target remains 0.8. SOL-R5-01 and
R5-CODEX-02 are one defect and share a fix. No capability is narrowed.

## SOL-R5-01 — resolved

Sections: §1.5, §16.2–§16.4, §17.4, §18.1; Appendix B.
Hand derivation: P(0)=64, P(270)=32. inttoptr of 2^32 truncates to zero;
ptrtoint to i64 zero-extends that zero. Input 2^32+1 similarly gives 1.
Two pw-bit moves gave 2^32 and 2^32+1 instead. The regression executed the
old map and observed payload 4294967296/code 0 before the fix.
The text now carries P(a) through constants, parameters, fields, results and
pointer memory storage. GEP uses I(a) inside P(a), while ISA memory operands
cross an explicit pw-bit address bridge. addrspacecast follows the incoming
target's representation conversion, with mov restricted to equal-width
bit-preserving casts. CC/R, constant expressions and the comparison build use
the same conversions. No mixed-width-layout rejection was introduced.
Witness pointer-as270 is a dynamic lift/map/object/hash/run pair with canonical
trunc.i32 then zext.i64 and native LLVM probes. Both inputs run through the
independent interpreter with code 0 (five steps). opt 18/23 verify and fold the
dynamic source to `and i64 %x, 4294967295`; both constant-call probes return
0. The folded dynamic function executes on clang 18/23 and yields 0 and 1.
The checker saves the observed LLVM outputs under native-pointer-as270/fold-*.ll
in its run directory. This preserves the declared layout before clang replaces
it with its host layout. Unit: test_round5_pointer_width; exact artefact and
mutation checks: test_round5_gep_rows and test_round5_execution.
Recorded probe output, identical on LLVM 18 and 23 (module headers omitted):

```llvm
define i64 @f(i64 %x) {
  %r = and i64 %x, 4294967295
  ret i64 %r
}
define i64 @probe() {
  ret i64 0
}
```

The original council stdin/stdout probes were also rerun headlessly using
`opt -S -passes=verify,inline,instcombine -o -` on both installed majors:

| LLVM | Dynamic body | source_constant | prescribed_move_equivalent |
|---|---|---|---|
| 18 | `%r = and i64 %x, 4294967295` | `ret i64 0` | `ret i64 4294967296` |
| 23 | `%r = and i64 %x, 4294967295` | `ret i64 0` | `ret i64 4294967296` |

Full outputs: scripts/.tmp/r5-original-probes-{18,23}.ll. The move equivalent
uses two identity integer additions, matching the old map's two 64-bit moves.
ISA 0.8 integer trunc/zext/and suffice; no ISA change for this case.

## R5-CODEX-02 — resolved

Same pointer-representation defect and same sections, derivation, dynamic
pointer-as270 witness and checker cases as SOL-R5-01 above. The source
findings agree; per-address-space carriers were selected rather than a common
carrier requiring masks at every boundary. The address bridge retains ISA
0.8's single address width without changing LLVM's pointer storage widths.

## R5-CODEX-01 — resolved

Sections: §5.2 PT6–PT8 and witness blocks; Appendix B.
Hand derivation: bytes 01 01 loaded as little-endian i16 are 1+256=257.
INT(1) from either component is not a possible whole loaded value. A mutable
i32 store of 66049 has bytes 01 02 01 00; its two-byte subrange concretely
loads 513, while copying the whole INT(66049) atom is unsound.
Memory atoms now retain storage intervals and representation widths. PT6
copies compatible whole-interval atoms, decodes exact immutable byte images,
and otherwise sets unrepresented partial/spanning/overlapping non-handle bits
to TOP. ROOT provenance remains explicit for §6.2 checks. Partial stores and
copies participate; copies preserve a whole atom only when fully covered.
Constant-byte fills have a complete interval and decode the repeated byte at
the load width, with other overlapping writes still included. This is required
for existing frontend-generated zero-filled budget records; no expectation was
weakened to retain them.
Witness pt6-byte-width recognises finite dispatch {257}; a generated native
allocation dispatch admits exactly that inferred set. The actual LLVM source
allocates 257 wires, applies X;X at 256 and frees cleanly on clang 18/23.
Witness pt6-subrange has reference TOP/blocked:BD-B-ISA4, executes the actual
513-wire concrete allocation/free under the fallback, and never claims a
finite singleton {66049}. Units: test_round5_memory_intervals (red {1} versus
{257}, then green, including a partial-store invalidation); state execution
and wrong-result mutations in test_round5_execution. Existing Grover frontend
cases still accept. The pre-existing BLK-1 dynamic-width ISA change applies
to TOP widths; this is not a dialect rejection.

## BD3-R5-1 — resolved

Sections: §6.5 parameter/result boundary rule, §7.5(b) by reference,
§25.1 BLK-1 trigger, Appendix B.
Hand derivation: ROOT(stash,0) can denote h1 on one host call and h2 on the
next. Both remain live in @slots at the entry exit; no bound on executions
inside one call limits host repetition. The same applies to a qalloc result
loaded from an alloca and returned to the host. The entry-boundary condition
now covers received parameter roots and returned QREG roots, persistent memory
and QREG results, with augmented call and unwind/resume edges and exact-root
qfree discharge. Such roots have no finite static-file bound and use BLK-1;
R/env receipt uses BLK-4. Direct within-entry use, direct QREG transport that
never reaches memory, and guaranteed frees preserve their existing realisation.
This retains handle-return=accept; it does not impose a static-file bound on
direct SSA QREG transport. Once persistent memory is involved, it must use the
boundary test rather than treating a per-entry result as a finite file.
Witness handle-param-cross-entry changes red accept to blocked:BD-B-ISA4 with
a named blocker report. Its state adapter compiles the actual stash/useall
LLVM under the 64-slot fallback: the host allocates two distinct registers,
stash(h1); stash(h2); useall() takes three entry calls, both X;X pairs and frees
succeed, live_after=0/trap=0. Units test_round5_parameter_liveness also cover
returned-via-alloca QREGs, guaranteed-free acceptance, direct parameter use and
R/env propagation; test_round5_execution rejects a mutated terminal state.
The ISA gap is existing BLK-1/ISA-4 (dynamic-width register creation and
qreg.width/id/from_id, call-width checks and handle-reference history), plus
BLK-4/ISA-12 for R new/free/slice/concat with reversible allocation history.
Exact ISA changes remain in §25.1; bead b-dialect-spec-cbe records this newly
exposed trigger. The blocker verdict resolves the dialect contract; it does
not claim ISA 0.8 acquired these capabilities.

## BD3-R5-2 — resolved

Sections: §13.1 wide integer sides and saturation semantics; §12.7/§12.1
repeated width legalisation; witness n-fpconv-wide; Appendix B.
Hand derivation: limbs [0,0,1] represent 2^128, not zero; binary64 has exponent
128+1023=1151 and zero fraction, bits 0x47f0000000000000. Truncating −2.5
toward zero gives −2: [0xfffffffffffffffe,all-ones,all-ones]. Saturating
positive 1e300 to signed i192 gives 2^191−1, with top limb
0x7fffffffffffffff. An i128 intermediate cannot represent these functions.
The i128 ABI is now explicitly M≤128. Wider conversions use full limb slots,
least significant limb first, with exact M-bit signed/unsigned rounding and
saturation, no intermediate truncation. The same rule covers .sat and all four
integer-return rounding intrinsic forms. Canonical slot push/store/call/load/pop
order and normal charges are stated; temporary slots do not escape.
Witness n-fpconv-wide is an exact normalisation pair plus native differential
execution. Defined −2.5 uses ordinary fptosi; the out-of-range vector uses
llvm.fptosi.sat so its source is defined. LLVM 18's direct x86 backend cannot
codegen the wide FP conversion (Unsupported library call operation); source
constant probes are therefore independently folded by opt 18/23 before clang
18/23 executes their scalar results. The materialised limb helpers execute
dynamically on both compilers. This is recorded in the witness, not a hidden
skip or a native execution of source poison. Unit test_round5_fp_wide failed
on unsupported sitofp/fptosi before implementation; exact pairs and native
wrong-result/code mutations execute through test_round5_execution. No new ISA
capability is required: linked integer arithmetic plus ordinary memory rows.

## BD3-R5-3 — resolved

Sections: §12.1 ordering, §12.8 wide intrinsic expansions and slots; Appendix B.
Hand derivation: all-ones in limb 0 plus one wraps that limb and carries into
limb 1, yielding [0,1,0]/overflow 0; all-ones in all three limbs plus one
wraps all limbs, yielding [0,0,0]/overflow 1. Population count of
[all-ones,1,0] is 64+1=65, represented as the full result [65,0,0].
After N27 and N32, N22 re-legalises the instructions they introduce; only width
legalisation repeats. Fused expansion is permitted only when it emits identical
canonical limb rows. Wide arithmetic forms use carries/borrows, lexicographic
compares, per-limb selects and aggregate limb-tuple/flag transport. Unsigned
overflow retains the true outgoing top-limb carry/borrow; signed forms test
the actual top bit. Wide runtime-call forms use destination/source limb slots,
with scalar flags retained and full-width count results, rather than residual
wide call parameters/results. Existing runtime fault rules remain.
Witness n-wide-intrinsics is an exact normalisation pair for
uadd.with.overflow.i192 and ctpop.i192; both source and materialised output
execute on clang 18/23 for the three vectors above, code 0. Unit
test_round5_wide_intrinsics first failed on unsupported wide call; the
normalisation-pair suite and test_round5_execution execute the expansion and
reject mutations. ISA 0.8 linked integer/memory rows suffice; no ISA gap.

## BD3-R5-4 — resolved

Sections: §12.2 N9, paired n-atomic-wrap/n-atomic-usub witnesses; Appendix B.
Hand derivation at limit 10: uinc_wrap increments 9 to 10 and wraps old≥10
to zero; udec_wrap returns the limit for old=0 or old>limit, otherwise old−1.
usub_cond keeps old when old<10, while usub_sat gives zero; both subtract
normally when old≥10. Every form returns old, not the stored result.
N9 now states the unsigned comparisons, wrapping add/sub and selects for all
four forms, with deterministic names and no overflow flags. The existing
single-thread assumption still applies.
Witnesses pin exact output and old/stored vectors: increment (9,10), (10,10),
(11,10); decrement (0,10), (11,10), (9,10); both subtraction variants (9,10)
and (11,10). Wrap source verifies on 18/20/23 and executes on clang 18/23;
subtraction source is explicitly tagged majors=23 because those opcodes are
newer, executes on clang 23, and its materialised output verifies on all
three and executes on clang 18/23. The checker does not attempt an LLVM-18
source opcode that that version does not define. Unit test_round5_atomic_forms
failed on uinc_wrap before the N9 fix; exact pairs, source/output execution
and code mutations run in test_round5_execution. No ISA change or rejection.

## BD3-R5-5 — resolved

Section: §16.4 GEP canonical rows, pinned objects, Appendix B.
Hand derivation: I=32 turns dynamic index 2^32 into zero and −1 into
0xffffffff, while preserving the base's high 0x1. Results are 4294967296
and 8589934591. Constant index 2^32 gives Δ=0 modulo 2^32; the GEP still
emits trunc/zext/const/and/or, exactly five rows, rather than mov or add-zero.
The restored per-index algorithm explicitly omits identity casts and
multiply-by-one, folds all constant sequential/structure offsets into Δ,
adds Δ last only when nonzero, writes v in the last I=P accumulation row,
and always emits the ordered I<P recombination. No inference from an old
version or a pinned example is needed to choose charged rows.
Pinned lift/object/hash/run witnesses gep-index-obj and gep-index-const
include the full independent-interpreter-checked objects. Dynamic f takes
13 total steps for both vectors; constant-expression c takes 9 total steps
(including wrappers and other source casts/operands), code 0. Unit
test_round5_gep_rows checks exact map text, hashes, results/counts and a
wrong-stride mutation. Existing n-gep-index and all earlier pinned objects
remain executed. This also resolves the reported 0.2.5 wording regression;
no semantics or expectation was weakened and no ISA edit is needed.

## Round-5 final freeze — 2026-10-30

**2598/2598 passed; 0 failed; 0 blocked/unavailable. Baseline 2514 → 2598.**
Draft/full version `0.2.6` (`dialect-0.2.6;isa-0.8`); ISA grading target 0.8.
59 checker unit tests and 4 legacy runtime tests pass headless.
Code/spec/checker snapshot: `5b01a51ac216fa36a2c7d1cbb5f92aa73b491798`.
Spec SHA-256: `4bbf697dd39e43c5c815864bcb27b502b47a047b18092a67ade466c858a05adc`.
Checker/source file-set SHA-256: `19192e6ba7b92cd3f023091dc103a634739dc692f68315711375645407944fec`.
Independent interpreter: `0b913dace5d69082dda28c85ce5dbb1aefb52cd2`; immutable source fingerprint:
`c65b7590fd21e8de29ea81851ffdbef919a3bc91ba200de5b2ede348ae993c4e`. Dependency HEAD matched when the green gate ended.
Machine receipt: `scripts/dialect_check.LAST-RUN.json`; full executed rows:
`scripts/.tmp/round5-fixes-freeze.json`.

| Family | Passed | Failed | Blocked |
|---|---:|---:|---:|
| asm | 1 | 0 | 0 |
| blocker | 19 | 0 | 0 |
| cc-run | 8 | 0 | 0 |
| check | 21 | 0 | 0 |
| coverage | 125 | 0 | 0 |
| driver | 1 | 0 | 0 |
| events | 3 | 0 | 0 |
| frontend | 21 | 0 | 0 |
| hash | 8 | 0 | 0 |
| header | 1 | 0 | 0 |
| map | 20 | 0 | 0 |
| native | 29 | 0 | 0 |
| normalise | 37 | 0 | 0 |
| parse | 691 | 0 | 0 |
| recognise | 134 | 0 | 0 |
| run-oracle | 21 | 0 | 0 |
| run-program | 5 | 0 | 0 |
| seeds | 1 | 0 | 0 |
| state | 57 | 0 | 0 |
| step-check | 6 | 0 | 0 |
| tdl | 10 | 0 | 0 |
| trace | 3 | 0 | 0 |
| xrefs | 1376 | 0 | 0 |
| **Total** | **2598** | **0** | **0** |

All eight S0 findings and the GEP wording regression are resolved. No declines,
partials, weakened expectations, removed examples, ISA edits or push. The checked
ISA-4/ISA-12 dependency verdicts do not claim those capabilities landed in 0.8;
newly exposed parameter/result accumulation is tracked by **b-dialect-spec-cbe**.

The prior `scripts/.tmp/round5-isa-head-race.json` preserves the 2597/2598 run
whose sole failure was an ISA HEAD-moved snapshot guard. Earlier development
receipts retain the red witness/adapter failures; the green receipt above supersedes
them. The guard was retained. The aborted intervening freeze used superseded
text; final SHA above includes PT2 restored and the canonical GEP algorithm
placed in §16.4. No normative source or checker file changed during the final
successful freeze (source file hashes are in the machine receipt).

Exact final command (scripts/.tmp existed):

```sh
env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER TMPDIR=/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/.tmp python3 /home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py --json /home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/.tmp/round5-fixes-freeze.json
```

Offline build passed:

```sh
env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER TMPDIR=/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/.tmp CARGO_TARGET_DIR=/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/.tmp/isa-build cargo build --manifest-path /home/tobias/Projects/bennett-workspace/bennett-isa-spec/reference-interpreter/Cargo.toml --offline
```

Version bumps follow spec/README.md. Changed full/handles/regions/norm/map
versions are 0.2.6; unchanged component subversions retain their earlier values.
All fixes were held as one coupled implementation group until the whole freeze
was green, then committed with the spec/checker together to avoid a red handoff.
Bead b-dialect-spec-p7u is closed; b-dialect-spec-cbe remains open for the exact
ISA dependency changes described above. No push.

| Blocker | Status | Dialect implementation commit |
|---|---|---|
| SOL-R5-01 | resolved | 5b01a51 |
| R5-CODEX-01 | resolved | 5b01a51 |
| R5-CODEX-02 | resolved | 5b01a51 |
| BD3-R5-1 | resolved | 5b01a51 |
| BD3-R5-2 | resolved | 5b01a51 |
| BD3-R5-3 | resolved | 5b01a51 |
| BD3-R5-4 | resolved | 5b01a51 |
| BD3-R5-5 | resolved | 5b01a51 |

Dialect freeze/Beads receipt commit: ff249d5. Implementation: 5b01a51.
