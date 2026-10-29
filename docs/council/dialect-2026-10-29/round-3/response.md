# Round-3 response — draft 0.2.4

Source findings: full round-3 JSON, with the two regressions tracked separately below.
ISA grading target remains 0.8. Semantic changes bump full dialect/norm to 0.2.4;
unchanged sub-artifact versions and existing map objects keep their identities.

## Theme A — single reading: clean control workspace, adjoint = U†

Hand derivation: retaining n-dependent flags distinguishes count branches even when
the body is identity. Undoing count preparation cannot erase those flags: H(c) then
gives P(1)=1/2. Exact inverse flag computation makes P(1)=0. The rule applies at
forward return, standalone adj return, and compute's matching inverse. Fault outputs
and intentional source measurements retain their separate lifetimes.

For preserved guards, construct flags forward, use them, and reverse their computing
slices. For overwritten guards, a standalone in-place interface must have the already
required bounded inverse: reconstruct the entry on copies, reconstruct the trajectory,
and clean all copies against the restored entry/output within valid windows. In compute,
reuse the actual forward history and clean it on reversal. No implicit count channel.
This implements NS §4.2 and agrees with ISA 0.8 §§4.6/5.3/6.2; no new ISA operation.

| ID | Status | Sections | Witness / executing family |
|---|---|---|---|
| SOL-R3-01 | resolved | TDL-7/10, §18.2/18.4, A11 | co-loop-identity count 0/2; state / Rust run-action |
| R3-CODEX-01 | resolved | same | co-loop-identity count 0/1 with X;X; state / Rust run-action |
| BD3-R3-1 | resolved | TDL-10, §18.2 | co-loop-adj-overwritten; state / native exhaustive collision check and Rust run-action |
| REG-SOL-R3-TDL7 | resolved | TDL-7/10, A11 | co-loop-identity; state / Rust run-action |
| REG-CODEX-R3-COUNT | resolved | same | co-loop-identity; state / Rust run-action |

The regression IDs map to sol regressions[0] and codex regressions[0]. Both
identity examples return z=0 with clean flags and P(c=1)=0, no T-CLEAN/T-LEAK.
The prior co-loop-adjoint preserved-count standalone/compute witness remains executed.

BD3-R3-1 correctly identifies an impossible reconstruction. Its proposed entry-guard
meaning is not adopted: B2 maps (0,0), (1,1), (2,2) to (2,2), so no data-only U† exists.
Deciding pre-existing TDL-5(b) sentence: “The complete predicated update MUST be a total
bijection on the declared mutable interface, with bounded inverse and clean non-fault
workspace.” TDL-7 already directs non-bijective overwrites to TDL-5(d) while keeping
out-of-place or compute/use/uncompute. The new witness executes compute(B2,empty)
for all three entries: each returns its original state, including (2,2), no trap,
clean flags. This resolves the ambiguity without changing adj into an instrument,
rejecting Co loops as a class, or assuming a nonexistent earlier invocation.

Validation: red missing adapter, then green mutation-sensitive loop regression.
