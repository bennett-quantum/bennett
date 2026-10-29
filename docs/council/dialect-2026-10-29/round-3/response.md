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

## Theme B — deterministic standalone adjoint channel placement

| ID | Status | Section | Witness / checker |
|---|---|---|---|
| R3-CODEX-02 | resolved | §18.2, §7.5(a) contract preserved | deferred-channel-adj-place; state / Rust run-action |
| BD3-R3-2 | resolved | same | same, zero-input/final-H probe |

Hand derivation: H on the source does not commute with its record copy. Choose
latest-before-consumer as both members recommend: H(a), qcopy(a,w), CX(w,t).
Plus input gives joint a=t=w=0 with probability 1. Zero input then final H gives
P(a=0)=P(a=1)=1/2. The text also pins unused records at reversed source position,
source-order ties, producer dependencies, unconditional inverse-allocation hoisting,
and source lifetime extension. Compute still reuses its actual records. Optimisation
must preserve the complete instrument. Red missing scheduler; green executable and
mutated-probability tests. No decline, partial, or new ISA dependency.

## BD3-R3-3 — resolved (theme C)

Sections: TDL-2/11, §18.2. Hand derivation: observed byte 0 remains basis-known
after the CC store writes 9 to both copies, so it needs no second measurement.
Choose the existing TDL-11 retain reading and state its exception in TDL-2 and
observe completion; event-application writes still invalidate coverage. Witness
co-observe-write-observe executes via state/native coherence seed on clang 18/23:
final K=Cl, load=9/code 0, arena=0. It also checks pre-observe store traps 4
and applied writes invalidate coverage. Red absent adapter, then green mutation test.
No decline, partial, or ISA gap.

## BD3-R3-4 — resolved (theme D)

Sections: §6.5 preamble/rule 2; §7.5(b) inherits it. Hand derivation: P's
setjmp continuation calls G twice without returning through the first G, so a
function-local test misses two simultaneous live instances. Augmented N29 edges
and may-ancestor continuation reachability now force E(s)=∞; E(c) is explicitly
defined on the same augmented CFG/call recurrence. The recogniser changed from
accept (observed red test) to blocked:BD-B-ISA4, with the exact ISA 0.9 K1
run-time-width qreg and width/id/from_id change; R hoisting uses BLK-4/K2.
Witness handle-setjmp-interproc: parse/recognise/blocker plus state/native clang
18/23 executes the 64-slot fallback with instances=2, distinct=true, max-live=2,
live-after=0, trap=0. Removing setjmp keeps the ordinary finite-bound accept case.
This is a passing named-blocker verdict, not a claim that ISA 0.8 gained dynamic
lookup. No decline or partial; existing dependency remains external.
