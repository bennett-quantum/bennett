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
