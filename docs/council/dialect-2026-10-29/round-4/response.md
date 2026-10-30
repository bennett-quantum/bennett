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
