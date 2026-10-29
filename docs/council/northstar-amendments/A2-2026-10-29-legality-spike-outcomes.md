# North-star amendment A2 — what the legality spike changed

**Status:** draft for council review, 2026-10-29. Amends `docs/Bennett-NorthStar.md`
iteration 7. To be applied surgically together with A1 as iteration 8 and graded as
`northstar-2026-10-28` round 7. Changes only two rows of the §3.1 table and the §3.2
legality-spike bullet. Nothing is implemented.

**Why.** North star §3.2 and §9 item 1 gate the dialect spec on a legality spike. The
spike ran (2026-10-28/29; `../bennett-dialect-spec/docs/spikes/2026-10-28-legality-findings.md`):
170,163 cells over LLVM 18.1.3, 20.1.8 and 23.1.1 (the majors of clang, Julia 1.13 and
rustc 1.99), 56 adversarial cases, every stock pass singly, every default and LTO
pipeline, and 200 random pass sequences per case and major. The central claim held:
attribute-free external marker declarations keep the dynamic sequence of marker calls on
every executed path under every standard pipeline of all three majors, and no pass adds a
motion- or elimination-licensing attribute to a marker. Two sentences of §3.1 did not hold
as written, and the maintainer decided both on 2026-10-29.

## A2.1 Handles: provenance through bitwise copies (§3.1, "Qubit handles" row)

**Evidence.** `instcombine` lowers an 8-byte `memcpy` of a handle to `ptrtoint` + `store i64`
on all three majors; LLVM 18 `lto<O3>` completes a `ptrtoint → inttoptr` round trip into
`__bennett_qfree` (corpus cases `val-memcpy-handle-int`, `c-memcpy-handle-int`). The source
contains no integer conversion. The current text would reject valid C after optimisation.

Replace

> a handle that flows through memory at a superposed address, or through an
> `inttoptr`/`ptrtoint` round trip, is **rejected fail-loud** in v1 of the dialect;

with

> a handle that flows through memory at a superposed address is **rejected fail-loud** in
> v1 of the dialect; handle provenance is tracked through bitwise copies (`ptrtoint`,
> `inttoptr`, integer and vector loads and stores of the whole value), because the
> optimiser introduces them into programs that never cast a handle, and any other use of a
> handle-derived integer (arithmetic, comparison, partial use) is rejected fail-loud;

## A2.2 Regions: identity by content, operands as classical data (§3.1, "Control as structure" row)

**Evidence.** After O1 the function operand of a region marker is a `select` of functions,
a switch table with a `phi`, or a load from a table (SimplifyCFG, all majors); MergeFunctions
replaces a region with its identical twin under `unnamed_addr`, which rustc emits on every
function and merges at O2 and above; `strip`, `iroutliner` and `global-merge-func` rename
regions or make them thunks. No pass produced an indirect call *to a marker*.

After "The plugin generates controlled and adjoint bodies on demand from one source body."
insert

> A region's identity is its content: the function the marker receives at link time,
> identified by its body, with aliases and forwarding thunks resolved to their target, so
> that merged twins are one region and symbol names are not normative. The function
> operand is classical data: the device's classical-control tier dispatches on it at run
> time, and the plugin generates bodies for the bounded set of functions whose address can
> reach a region marker, failing loud only when that set cannot be bounded.

## A2.3 The spike's status (§3.2, "The legality spike" bullet)

Append

> It ran on 2026-10-28/29 over LLVM 18, 20 and 23 and passed for every default and LTO
> pipeline; its findings (A2.1, A2.2; attribute envelope; Julia emission through
> `ccall(…, llvmcall, …)`; normalisation confirmed necessary by folded marker operands) are
> recorded in `bennett-dialect-spec/docs/spikes/2026-10-28-legality-findings.md`.
