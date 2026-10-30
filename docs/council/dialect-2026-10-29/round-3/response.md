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

## SOL-R3-02 — resolved (theme E)

Sections: §17.3, §16.4 memory rows, §8.5 replay (implements §17.1). Hand
derivation: the backing allocation survives pop, so ISA physical boundscheck
alone accepts the stale pointer. Add logical base/extent/live validation before
every program access, including non-coh stack pointers, and charge helper rows.
Push/pop/restore update logical ranges; explicit restricted internal accesses
serve bookkeeping and replay. Both builds share the checks; entry replay includes
logical metadata and invalidates its cache on mutations. Witness shadow-stack-liveness
executes native push/store/pop/return/load (0/code 7), live load (7/code 0),
spanning/padding/restore/wrap failures, mutation gating and live metadata replay.
State also executes an independently checked Rust run-oracle object calling an
ordinary lproc helper with run-time frame metadata before its physical access.
Red absent adapter, then green result-mutation test. No ISA gap, decline or partial.

## SOL-R3-03 — resolved (theme F)

Sections: §6.1/6.3/6.5, §18.3 T-DEAD. Hand derivation: N(s)=1 proves
nonoverlapping storage use, not that the first allocation's saved tag denotes the
second allocation. The static file now stores a current generation tag/live bit
per slot; fresh-tag allocation changes identity, stale copies retain the retired
identity, dispatch validates both generation and liveness before mutation, and
equality compares allocation identities. No reuse while stale copies remain
observable, including no wrap onto such a generation. This is ordinary CC state,
not a new quantum instruction. Witness handle-stale-generation remains accepted
and has recogniser-derived N(s)=1. State executes its original LLVM through native
generation-tag marker dispatch on clang 18/23: old!=new, first old gate traps 4,
second register stays 0, fault cleanup leaves no live slot. The second gate never
executes. Red absent adapter, then green result-mutation test. No decline or partial.


## R3-CODEX-03 — resolved (theme G)

Sections: §8.2, §8.6, §16.2. Hand derivation: no payload slices does not
mean no invocation. A clean hidden bit XORed with constant zero stays clean,
while one call XORs the fault code into the caller's non-null four-wire fault
register. A second call would erase that code. W_empty therefore executes
exactly once, with the ordinary prologue, body and unwind check, then charged
`p0 = lift.const.i1 0; lift.retval p0` on success. The call is controlled;
allocation/free are unconditional. Null CONSOLE registers contribute no output.
Discarding a non-void return introduces no dropped-bit check.

oracle-empty-marker verifies acceptance of the null-target, zero-binding descriptor
with its four-wire fault register. Witnesses oracle-empty-output, oracle-empty-fault
and oracle-discard-return map source LLVM independently to the checked ISA object and run through Rust
run-oracle. Empty success takes four rows; budget 3 returns code 1, budget 4
returns code 0; explicit fault returns code 4 and zero budget returns code 1.
All synthetic payloads are zero. The state witness also executes actual CC
allocation/call/clean-free, verifies a trace count of one oracle call and the
fault measurement, and tests controls 0/1. The inherited test failed red on
null-target parsing; the mapper and execution adapter now pass it, including
mutated fault, budget, cleanliness and call-count expectations. No new ISA
requirement, decline or partial resolution.


## Complete disposition

| ID | Theme | Status |
|---|---|---|
| SOL-R3-01 | A | resolved |
| R3-CODEX-01 | A | resolved |
| BD3-R3-1 | A | resolved |
| R3-CODEX-02 | B | resolved |
| BD3-R3-2 | B | resolved |
| BD3-R3-3 | C | resolved |
| BD3-R3-4 | D | resolved |
| SOL-R3-02 | E | resolved |
| SOL-R3-03 | F | resolved |
| R3-CODEX-03 | G | resolved |
| REG-SOL-R3-TDL7 (sol regressions[0]) | A | resolved |
| REG-CODEX-R3-COUNT (codex regressions[0]) | A | resolved |

All ten S0 items and both regressions are resolved. Theme A chooses exactly one
reading: restored control workspace and adjoint = U† on the declared bijective
interface; compute retains its actual trajectory only until matching uncomputation.
The impossible data-only inverse of B2 is not silently redefined as an instrument.
The existing out-of-place and compute capabilities remain. No item is declined
or partially resolved; the named external ISA dependencies retain their explicit
passing blocker verdicts and are not claimed implemented by dialect fixes.


## Round-3 final freeze — 2026-10-30

**2466/2466 passed; 0 failed; 0 blocked/unavailable.** Full version
`0.2.4` (`dialect-0.2.4;isa-0.8`); ISA grading target remains 0.8.
Theme G and resumption fixes: 8d1517a6586a506488c4af7a9c35800c7053b508; A–F commits remain 8e56d56,
5e13596, 3303a5b, 1a511c5, 90fa101 and 111e889.
Spec SHA-256: `2ba040956ac8e22d11ff2bd4655d908b08de9d44564913a8b4f12c8a522fa156`.
Independent Rust interpreter: `92c26af045b816f5ef1e283a7b734aa244d8f320`;
immutable source fingerprint: `2dd454deeb8352a0b0e64ac1e61ddcc346ae5e2bdea59bd60440d35654946050`.
ISA HEAD remained at this revision throughout the successful freeze.
Machine-readable receipt: `scripts/dialect_check.LAST-RUN.json`.

| Family | Passed | Failed | Blocked |
|---|---:|---:|---:|
| asm | 1 | 0 | 0 |
| blocker | 16 | 0 | 0 |
| cc-run | 8 | 0 | 0 |
| check | 18 | 0 | 0 |
| coverage | 125 | 0 | 0 |
| driver | 1 | 0 | 0 |
| events | 3 | 0 | 0 |
| frontend | 21 | 0 | 0 |
| hash | 5 | 0 | 0 |
| header | 1 | 0 | 0 |
| map | 17 | 0 | 0 |
| native | 19 | 0 | 0 |
| normalise | 29 | 0 | 0 |
| parse | 624 | 0 | 0 |
| recognise | 130 | 0 | 0 |
| run-oracle | 18 | 0 | 0 |
| run-program | 5 | 0 | 0 |
| seeds | 1 | 0 | 0 |
| state | 52 | 0 | 0 |
| step-check | 6 | 0 | 0 |
| tdl | 10 | 0 | 0 |
| trace | 3 | 0 | 0 |
| xrefs | 1353 | 0 | 0 |
| **Total** | **2466** | **0** | **0** |


| Theme | Executed state witness | Status |
|---|---|---|
| A | co-loop-identity | passed |
| A | co-loop-adj-overwritten | passed |
| B | deferred-channel-adj-place | passed |
| C | co-observe-write-observe | passed |
| D | handle-setjmp-interproc | passed |
| E | shadow-stack-liveness | passed |
| F | handle-stale-generation | passed |
| G | oracle-empty-output | passed |


The G map/check/run families also execute oracle-empty-fault and
oracle-discard-return; oracle-empty-marker passes parse and recognition.
A–F witnesses are actual passing state rows in this receipt, not index-only
claims. The original co-loop-adjoint, deferred-channel-adj and other round-2
vectors remain executed. Named ISA dependency examples pass their specified
blocker verdicts; zero gate blockers does not claim those capabilities have
been added to ISA 0.8. No expectation was weakened and no ISA source was edited.

Exact freeze command:

```sh
env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER TMPDIR=/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/.tmp python3 /home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/dialect_check_v02.py --json /home/tobias/Projects/bennett-workspace/bennett-dialect-spec/scripts/.tmp/round3-fixes-freeze.json
```

44 checker unit tests and 4 legacy runtime unit tests pass headless. Full
version, SPEC_VERSIONS.toml and current/stale module-flag parsing agree on 0.2.4.
The deliberate-fault probe disables core dumps only; expected -4/132 exits
remain checked. The earlier stale-version test, ambiguous cross-reference,
concurrent ISA snapshot race and core-dump timeout were reproduced and fixed
or rerun; none is hidden in this receipt. All ten S0 findings and both regressions
are resolved, with theme A's single clean-workspace/U† reading stated above.
No decline, partial resolution, scope narrowing or push.
