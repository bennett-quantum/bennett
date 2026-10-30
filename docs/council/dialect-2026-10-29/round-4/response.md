# Round-4 response — draft 0.2.5

Source: full round-4 JSON findings. Surgical corrections; ISA target remains 0.8.

## SOL-R4-01 — resolved

Section: §12.7, §12.9, Appendix B; full dialect/norm 0.2.5 (ISA 0.8).
Hand derivation: limb 0 of [0,1,1]−[1,1,0] borrows; limb 1 has t=0
and incoming z=1, so t<z propagates the borrow. Limb 2 is 1−0−1=0.
The old inherited m<t comparison clears that borrow and gives the wrong high limb.
The text now explicitly defines both subtractions modulo each limb width and
beta=(a<b) OR (t<z), with identity conversion for an i1 top limb and discarded
final borrow. LangRef sub/usub.with.overflow links document the wrapping semantics.
Witness n-wide-sub is an exact normalisation pair with native vectors for the
council counterexample and final-borrow wrap. Checker normalise executes the N22
expansion; native compiles both source/output on clang 18/23. The targeted unit
regression failed on unsupported wide sub before implementation, then passed.
No decline, partial or new ISA capability required (ISA 0.8 §§3.3/4.2).

## SOL-R4-02 — resolved

Sections: §16.4 GEP row, §17.4, §18.1, §12.7 witness, Appendix B.
Hand derivation: I=32 truncates index 2^32 to zero, keeping base 2^32.
For base 0x1ffffffff plus one, the low 32 bits wrap to zero while high bits
remain 1; result 0x100000000. The rule now distinguishes pointer-index and
pointer-carrier widths, computes scaled/constant offsets modulo 2^I and
recombines the low result with unchanged high bits. It covers constant expressions
and CC/R equally, citing LangRef GEP/data-layout. No layout rejection added.
Witness n-gep-index: unchanged materialised normalisation pair, native LLVM-fold
probes (clang 18/23), and state execution of independently source-mapped Rust
objects for index truncation, negative offset, low-bit wrap and a constant-expression
wrap. The regression first observed expected 4294967296 versus actual 8589934592;
corrected mapping and wrong-result mutation now execute under run-oracle/code 0.
Native source probes fold with opt before clang because clang replaces custom
layouts with its host layout. Wrap and negative cases execute through Rust;
LLVM 18 constant-folding itself mishandles the wrap case, so it cannot serve as
that case's oracle. No expectation changes to existing examples. ISA 0.8 integer
trunc/zext/and/or/add rows suffice; no decline, partial or ISA edit.

## R4-CODEX-01 — resolved

Sections: §12.6 vector-memory bullet, §12.9 boundaries, Appendix B.
Hand derivation: 24-bit lanes occupy offsets 0 and 3; scalar i24 stride is 4
under i24:32. Thus lane 1 is 04+05*256+06*65536=394500; offset 4 gives
the incorrect 460293. The corrected rule permits scalar GEP T only when its
allocation stride equals vector lane spacing, uses byte offsets otherwise,
limits accesses to the original vector storage and derives alignment from the
actual offset. Packed/masked inactive-bit requirements remain. LangRef vector
layout and load semantics are linked at the rule.
Witness n-vector-i24 has exact load/store normalisation pairs, align 1 at offsets
0 and 3, and native source/output execution on clang 18/23. The store writes
[1,2,3,4,5,6] contiguously and preserves both following 0xaa sentinels. The unit
regression first showed scalar GEP i24 versus required i8 and an unexpanded store;
then passed. No decline, partial, rejection or ISA capability change.

## R4-CODEX-02 — resolved

Sections: §12.2 N15, §12.6 select chains, Appendix B.
Hand derivation: an i1 index can only be 0 or 1; writing constant 2 in i1
makes it zero, so the old uge guard incorrectly fires on every input. With
W=max(K,ceil(log2(L+1)))=2, zero-extension keeps both indices below exact L=2.
The rule and normaliser now use that width for both out-of-range and lane
comparisons, and never truncate lane constants. Insertion fuses the unchanged
out-of-range vector into per-lane equality selects. LangRef extractelement and
insertelement links confirm unsigned indices of any integer width are legal.
Witness n-narrow-lane executes extraction (5/9), insertion ([7,9]/[5,7],
packed 2311/1797), and four-lane extraction with unreachable lane constants
2/3. Exact normalisation and native source/output comparisons pass on clang
18/23 after the regression showed the old i1 comparison. Added native execution
of existing n-dynamic-lane output: indices 2 and -1 still return zero, preserving
the dialect's totalisation of LLVM poison. No decline, partial or ISA gap.

## BD3-R4-1 — resolved

Sections: §6.5 precondition/rule 2, §7.5(b), Appendix B.
Hand derivation: @put runs its site once per invocation, but @slots retains the
first live ROOT at return; another host call allocates a second distinct live
instance. No finite per-call TC/E bound limits repetitions. Before self-disjoint
or loop/call counting, the text now checks may-live ROOT in persistent memory
and paths to an entry return lacking an exact-provenance free. Such sites have
E=∞ and BLK-1; §7.5(b) substitutes reversible-invocation return and BLK-4.
Internal callee return alone is insufficient; guaranteed caller frees can discharge
it. The recogniser follows interprocedural call/return continuations and checks
persistent memory reachable from globals, heap, results/env.
Witness handle-cross-entry changed from observed accept/N=1 to
blocked:BD-B-ISA4 with the named BLK-1 report. Its state family compiles the actual
@put/@use LLVM with a native 64-slot fallback on clang 18/23: two host calls,
two distinct allocations, both X;X and free, live_after=0/trap=0. Mutation of
distinct fails. Unit checks also preserve accept after guaranteed free, the
round-3 caller-free finite case, and verify BLK-4 for an R-entry variant.
ISA 0.8 §§3.2–3.3/4.1 still lacks qreg memory conversion/dynamic register naming
and R allocation; BLK-1=ISA-4 and BLK-4=ISA-12 retain their existing exact
ISA changes in §25.1. A passing named-blocker verdict does not claim those
operations landed. No decline, partial or scope narrowing.

Final review supplements R4-CODEX-01 with native source/materialised packed-i1 store execution and a following-byte sentinel (red, then green). Full/changed subversions are 0.2.5; unchanged oracle-abi/tdl/effects stay 0.2.4.

## Round-4 final freeze — 2026-10-30

**2514/2514 passed; 0 failed; 0 blocked/unavailable.**
Full version `0.2.5` (`dialect-0.2.5;isa-0.8`); ISA grading target 0.8.
50 checker unit tests and 4 legacy runtime tests pass headless.
Code/spec snapshot: `3e4c27e7fcdd21b59f32bde83b3d5f1e9441568f`.
Spec SHA-256: `c19dc84c476fe9a3c6ebb9cb621efd540a04aad05dd675a8ca78f3fd7f452d9a`.
Independent interpreter: `9e4984fc47587aa2dd501038b011dfc137449aae`; immutable source fingerprint:
`320982f83c264f805f06d2dc9730d87ba19e247d3485a40e11e8c4efc8b544cc`. Dependency HEAD matched at final verification.
Machine receipt: `scripts/dialect_check.LAST-RUN.json`; full executed rows:
`scripts/.tmp/round4-fixes-freeze.json`.

| Family | Passed | Failed | Blocked |
|---|---:|---:|---:|
| asm | 1 | 0 | 0 |
| blocker | 17 | 0 | 0 |
| cc-run | 8 | 0 | 0 |
| check | 18 | 0 | 0 |
| coverage | 125 | 0 | 0 |
| driver | 1 | 0 | 0 |
| events | 3 | 0 | 0 |
| frontend | 21 | 0 | 0 |
| hash | 5 | 0 | 0 |
| header | 1 | 0 | 0 |
| map | 17 | 0 | 0 |
| native | 24 | 0 | 0 |
| normalise | 33 | 0 | 0 |
| parse | 651 | 0 | 0 |
| recognise | 131 | 0 | 0 |
| run-oracle | 18 | 0 | 0 |
| run-program | 5 | 0 | 0 |
| seeds | 1 | 0 | 0 |
| state | 54 | 0 | 0 |
| step-check | 6 | 0 | 0 |
| tdl | 10 | 0 | 0 |
| trace | 3 | 0 | 0 |
| xrefs | 1361 | 0 | 0 |
| **Total** | **2514** | **0** | **0** |


| Blocker | Status | Dialect commit | Response commit |
|---|---|---|---|
| SOL-R4-01 | resolved | bec39eb | fc97aa7 |
| SOL-R4-02 | resolved | 68d8f5b | a285b98 |
| R4-CODEX-01 | resolved | 22d23e9 | 29c3944 |
| R4-CODEX-02 | resolved | 6663d8a | ac2c64e |
| BD3-R4-1 | resolved | bdfa241 | ba395b6 |

Supplemental packed-store regression/subversion receipt: 3e4c27e / 399962b.
No declines, partials, removed expectations, ISA edits or pushes. Named ISA
blocker examples pass their specified dependency verdicts; zero unavailable
checks does not claim ISA 0.8 gained dynamic register naming or R allocation.
New witnesses execute: n-wide-sub (normalise/native), n-gep-index
(normalise/native/state with Rust mapping), n-vector-i24 (normalise/native),
n-narrow-lane (normalise/native), handle-cross-entry (recognise/blocker/state).
Existing n-dynamic-lane output also executes natively at 0,1,2,-1.
The intermediate freeze failed one check because dependency HEAD moved during
its build; `scripts/.tmp/round4-freeze-head-race.json` preserves that result.
The full final rerun above supersedes it, with the guard retained unchanged.
External LLVM18 low-bit-wrap folding discrepancy is filed as
**b-dialect-spec-co5** for maintainer/upstream follow-up. The Rust-mapped wrap
and constant-expression witnesses execute the required high-bit-preserving
semantics; native LLVM-fold/clang18/23 probes execute the council truncation
case. This is not an unexecuted dialect witness or partial council resolution.

Exact final command:

```sh
env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER TMPDIR=/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/.tmp python3 /home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py --json /home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/.tmp/round4-fixes-freeze.json
```
