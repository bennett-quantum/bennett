# Acceptance dossier (Muse seat): z4c, adg, checker-diagnostics, 5u3

Scope (advisor ruling R6(a), 2026-11-02): each of the four contract proposals below was ACCEPTED by the sol and astra council members in round 1 (bennett/docs/council/contract-<id>-2026-11-02/round-1, consensus agree, empty blocking lists) and then PASSED the bennett-4ht mixed-fat-object re-check (bennett/docs/council/accept-4ht-recheck-2026-11-02, rounds 1-2). For z4c and adg the re-check added one mixed-fat-object statement each, reproduced at the end of their parts and now part of the proposal. This is the final acceptance seat: grade each proposal independently on its own merits. z4c, adg and checker-diagnostics amend Bennett ISA 0.9 (spec/Bennett-ISA-Spec-0.9.md in bennett-isa-spec); 5u3 amends the Bennett dialect spec (../bennett-dialect-spec/spec/). Parts are separated by horizontal rules.

---

## Dossier part: z4c (run contract-z4c-2026-11-02 round 1 accepted; 4ht statement from accept-4ht-recheck-2026-11-02)

# z4c — addresses for action-local region support

Proposal for council review; not a spec edit or an implementation claim.
Bead: `b-isa-spec-z4c`; blocks reference slice `b-isa-spec-fuk.3`.

## Defect and scope

ISA 0.9 §4.6, `qregion`, requires unconditional function-entry allocation
and image preparation, function scope, and function-exit restoration and
release. §16.2 permits a declaration inside either qif arm and inside a
qloop, including a zero-trip loop. §11 Matching requires every generated
leaf to end at a point whose iteration vector has the point's lexical loop
depth. K64 supplies non-row addresses only in a containing **oracle**.
K65 explicitly excludes implicit region restoration from cleanup carriers.

Consequently the following admitted action has mandatory leaves without
legal terminal addresses:

```text
action @gap (t:wire mut) () () () ()
regs {  } bounds {0}
^entry():
qloop 0 {
qregion local 0 1
}
x t
```

The associated signature has `mut:[1]`, `bounds:[0]`. The declaration is
`entry:1`; there is no executed iteration. `iteration:[]` has the wrong
depth and `[0]` is outside a zero-trip loop. Wildcard selectors can match
existing coordinates but cannot create a coordinate. Omitting the leaves
violates §4.6 even for an entirely default schedule. Calling them oracle
support contradicts K64's validation domain.

This is an S0 contract defect under rubric C5/C8: implementers must invent
an address or reject valid source. North Star §4.2 requires structured
coherent regions with unconditional workspace support; §4.4 requires an
independently implementable scheduler contract. Forbidding nested region
declarations would narrow the existing ISA. The fix preserves every
program, including the full SQLite/demo scope; no placement restriction is
proposed.

## Alternatives and worked witness

| Rule | Result on the witness |
|---|---|
| Action-root support pseudo-points (recommended) | Allocate local once at `$construct/[]/0`; execute X once at `entry:2/[]/0`; release local once at `$release/[]/0`. |
| Give declarations a separate hoisted coordinate type | Sound if it explicitly separates declaration coordinates from body iterations; requires another selector encoding and validation rule. |
| Use the lexical point with an invented iteration | `[]` violates depth; `[0]` names a nonexistent iteration. Requires a different normative rule, not an implementation convention. |
| Omit support or reject this source | Violates §4.6; rejected. |

Hand execution: for t=0, forward produces t=1; for t=1, t=0. The local
wire is allocated at zero and released at zero in either case. The inverse
restores t exactly and also allocates/releases the local wire once. The
loop body executes zero times. Resource counts before native decomposition
are one allocation, one X, one release. This is a derivation from the
clauses, not a newly run interpreter test. The bead reports a reference
test and diagnostics; those runs were not repeated in this job.

## Recommended exact spec diff

Insert after §11 **Non-row addresses (K64)**, before Whole-cleanup selection:

```diff
+**Action-local region support (K-new).** For each action or perm_action
+invocation, collect all function-local qregion declarations, including
+declarations nested in zero-trip qloops and in either qif arm. Each
+declaration creates one region per invocation, not one per loop visit.
+Traverse declarations in canonical function text order, recursively
+visiting the then arm before the else arm and a loop body once, for
+function-entry allocation and image preparation. Their terminal point is
+$construct in that action. Function-exit image restoration and release
+traverse the declarations in reverse order and have terminal point
+$release. Within a declaration, use the bound library's region creation
+expansion; restoration/release is its exact inverse. These support leaves
+are unconditional as specified in §3.5 and §4.6.
+Number leaves contiguously from zero within each of these pseudo-points
+in forward instantiated support order, including allocation, image gates
+and release leaves, excluding the action body and semantic callee
+subtrees. Each leaf retains its allocation identity. Their own instance
+and source-qloop iteration vectors are []; outer invocation edges retain
+their actual coordinates. At that action level the support has no step
+or phase and matches only wildcard step and phase, under §11 Matching.
+A selector ending at an enclosing oracle level retains that level's
+existing step/phase interpretation.
+Raw inversion of an already expanded trace retains forward pseudo-points,
+ordinals, invocation edges and allocation identities while adjointing
+operations. Source-adjoint formation continues to follow K62.
+Path validation admits $construct and $release for action and perm_action
+support. $step and $commit remain oracle-only. A reserved point with no
+leaves has an empty generated domain. K64's oracle partition and K65's
+exclusion of implicit region cleanup are unchanged.
```

Add to §0.2, assigning the next free K number at application time:

```text
K-new | §4.6, §11, §15 | ACTION-REGION-SUPPORT: action-local qregion
construction/release have reserved root support addresses, including
zero-trip declarations; no leaf changes. | b-isa-spec-z4c | S | –
```

The traversal rule resolves several declarations and both arms without
mistaking source-loop visits for declarations. It adds addresses, not
cleanup realisations or source instructions.

## Hashes, catalog and consumers

No change to canonical object text, semantic envelopes, `ref-0.9.json`, its
hash or generated leaf order is intended. Unaffected object closure hashes
stay fixed; the bead's witness closure hash is reported evidence, not
recomputed here. Address-bearing schedules/certificates for affected
actions must use the new coordinates, so their own serialized hashes
change. Published 0.8 behavior is untouched. Reference, VM, scheduler and
checker must implement identical action support partitioning; clause
extraction/coverage must include the new paragraphs. A catalog change is
unnecessary if its existing region construction already meets §4.6.

## Conformance vectors and verification

After acceptance, add these vectors to suite F and schedule suite H:

1. The zero-trip witness above: both t basis values, forward/inverse;
   exactly the three leaves and coordinates given above; no loop-body leaf.
2. Two declarations, one inside each qif arm: both constructed once in
   then/else text order regardless of selector value, released in reverse
   order. Nested zero-trip loops add no iteration coordinate to support.
3. `qregion r 0 8 @image` with one-byte image `01`: construction emits its
   allocation then X on bit 0; release undoes image then allocation. Check
   contiguous per-point ordinals and raw inverse identity retention.
4. A caller loop invokes this action twice: callee support has `[]`, caller
   edge has `[0]` or `[1]`; no alias of allocation identities across calls.
5. Concrete action `$step`/`$commit` reject; action support with nonempty
   own iteration/instance does not match; duplicate maximal matching
   entries on an actual support leaf reject by K55. Empty support domains
   cannot witness a tie.

These are proposed vectors, not claims of a passing implementation.
The exact commands used for the derivation were `sed -n '954,1617p'
spec/Bennett-ISA-Spec-0.9.md` and `sed -n '2401,2842p'
spec/Bennett-ISA-Spec-0.9.md`, plus inspection of the supplied bead.

## Release and after acceptance

Recommend a **0.9 K-entry repair**, ahead of the blocked reference slice.
Waiting for 0.10 would leave an existing legal 0.9 source without an
address. Council assigns the K number, applies the text, publishes the
vectors, regenerates the 0.8-to-0.9 diff and clause indexes, and authorizes
the reference owner to finish slice .3. The bead stays open until that
contract/implementation acceptance work is complete.

### Addition to 'Hashes, catalog and consumers': mixed fat object (bennett-4ht; closes z4c-4HT-1)

In a mixed fat object, the new support coordinates belong to action or perm_action invocations within the linked device ISA object(s). Each affected device object's schedules and certificates use them under the existing object, closure and schedule bindings. Native host functions require neither these support coordinates nor ISA region entries in that device certificate. $construct and $release denote device action entry and exit, not native process entry and exit; this repair does not require the surrounding native binary to become an ISA object.

---

## Dossier part: adg (run contract-adg-2026-11-02 round 1 accepted; 4ht statement from accept-4ht-recheck-2026-11-02)

# adg — loaded-program memory lifetime across launches

Proposal for council review; `b-isa-spec-adg`.

## Defect and North Star scope

ISA 0.9 §7.1 defines initial memory, allocation table and bump pointer
without saying whether initialization occurs at load or every run.
§3.2 places the register ledger at program scope; §10 gives a run
exclusive ownership only until CLOSED; §7.4 and T4 restore a run's entry
state on eligible reversal. These strongly favor program-lifetime state
but do not explicitly settle classical memory initialization.

Dialect 0.3 draft §§6.5–6.6 uses a persistent qreg table in device memory
and requires parameter/result roots to survive entry calls. North Star
§3.1's register handles and §5's REPL/library device model require
cross-entry quantum state. A fresh-every-run interpretation loses the
table while live registers remain. This is a contract ambiguity with
observable results, S0 under C1/C5; persistence is the compatible reading.
It adds no restriction to the North Star, including repeated SQLite or
kernel invocations.

## Alternatives and hand-worked witness

Layout: ptr_width=16, H=16, A_tab=2, S_cells=0, null_size=1,
heap_base=16, heap_limit_max=16; a one-byte global g at base 1 with image
00. Run A allocates one byte (returns 16) and stores 7 into g, then
completes and is CLOSED without reversal. Run B loads g and allocates
one byte. Under persistence it returns `(7,17)`; under reinitialization
it returns `(0,16)`. These are distinct visible results from the same
loaded program. Freeing 16 does not reclaim storage under §7.1.

If A is instead successfully REVERSED before CLOSED, its allocation
and store are undone, and B returns `(0,16)`. Merely closing A does not
reverse it. An eligible failed run retains its executed prefix until it
is reversed; closing a failed run does not silently roll it back.

| Alternative | Assessment |
|---|---|
| Program-lifetime memory and ledger (recommended) | Matches §10 ownership and the dialect's persistent table. |
| Reinitialize on each run | Would need a different host-held table and an explicit reset/lifetime ABI; it changes existing consumer assumptions. |
| Implicit reset when no register is live | Still changes classical allocation/global results; no clause authorizes it. |

## Recommended exact spec diff

Insert after §7.1's Initial state sentence:

```diff
+That state is established once when the program is loaded. Classical
+memory, allocation-table entries and the bump pointer belong to the
+loaded program and persist across runs. For sequential launches, a new
+run starts from the state left by the preceding CLOSED run. Closing a run does not restore its
+entry state. If the preceding run was successfully REVERSED before
+being CLOSED, its reversible state is its restored entry state (§7.4,
+§10, T4). A FAILED run otherwise leaves its executed prefix in place.
+Register-ledger entries and live register identities likewise persist
+under §3.3; ownership ends at CLOSED, not the register lifetime. Unloading
+and loading a program creates a new program instance with initial state;
+register ids of the old instance are not imported into it.
```

Append to §10's ownership paragraph:

```diff
+Persistence does not relax exclusive ownership of touched registers or
+memory while a run is not CLOSED. Separate loaded program instances have
+separate state; initialization is never repeated merely to start a run.
```

All examples here use sequential CLOSED runs. This wording does not add a
blanket prohibition on disjoint concurrent runs or invent a memory merge
rule. The existing ownership restrictions still govern overlapping uses.

## Hashes, catalog and consumers

This pins an existing reading: no source, envelope, target or catalog byte
changes and no hash re-pin. A consumer that reset memory on each run must
change its load/run lifecycle; plugin qreg-table code should not change.
Launch bindings and certificates that replay a later entry must include
its actual entry-state/preparation assumptions rather than presume a
fresh load. Domain claims do not acquire coverage of all histories merely
by showing one initialized run. Header diagnostics already include
E_INVALID_STATE; no new numeric status is proposed.

## Conformance vectors and verification

Test load→A→CLOSED→B and load→A→REVERSED→CLOSED→B with the results
above; check every byte, table live bit, bump pointer, register identity
and token lifetime. Add a failed A whose prefix stored 7: B sees 7 unless
that prefix was reversed. If B passes a register still owned by A before
A is CLOSED, it must return E_INVALID_STATE before effects. Fresh loading
restores g=0 and bump=16. A stored id can be recovered by qreg.from_id in
the next run after ownership is released. These are hand derivations;
the scalar state transitions are checked by
[contract-verification](2026-11-02-contract-verification.md), not by a
new reference execution.

## Release and after acceptance

Recommend a **0.9 K wording repair** to §§7.1/10 with lifecycle vectors.
Council should explicitly accept program scope under existing ownership, then
VM/reference owners validate their lifecycle and the dialect updates its
cross-reference. Keep adg open until the contract decision lands.

### Addition to 'Hashes, catalog and consumers': mixed fat object (bennett-4ht; closes adg-4HT-1)

In a mixed fat object, 'loaded program' means a loaded device program instance, not the native host process or entire fat binary. The native host may retain that instance and repeatedly invoke its device CC entries; the specified memory, allocation-table, bump-pointer and register-ledger persistence applies to that instance, with separate state for separate loaded instances. Loading a device program or closing or reversing a device run does not initialize or roll back unrelated native host state. This rule does not require moving native main, argv/envp handling or host-only libc into the device object. Later-entry certificate replay records the actual device entry-state preparation assumptions, without presuming a fresh native process.

---

## Dossier part: checker-diagnostics (run contract-checker-diagnostics-2026-11-02 round 1 accepted; passed accept-4ht-recheck-2026-11-02 round 1 unchanged)

# Checker question 2 — diagnostic-code ownership

Disposition proposal for council review; source request 2 in
`../bennett-conformance/checker/.tmp/CROSS_REPO_BEADS.md`.

## Defect classification and North Star scope

ISA §12 requires rejection of invalid certificates but defines no global
checker error-code registry. §11 separately mandates
`E_SCHEDULE_INFEASIBLE` and K55's multiple-maximal-entry diagnostic.
Launch §10 enumerates executor statuses; §5.4 enumerates program fault
outcomes. These are different interfaces, and the latter two lists do
not imply an unlisted E_CERT registry.

Two checkers rejecting the same invalid certificate under different
documented local codes compute the same specified verdict. The lack of
a registry is therefore **not an established contract defect**. It is a
possible diagnostics portability improvement (rubric C8/S1). North Star
§§4.4/5.1 requires independent checkability and honest labels, not a
particular spelling for every checker-local code. No capability is lost
by leaving those codes local. Inventing required codes would make
otherwise conformant checkers fail an unstated condition.

## Alternatives and concrete witness

Certificate A omits a table claim's required `expected`. Certificate B
has a complete table and invocation but repeats a component in its domain.
K13 requires A to reject; §12.2 K71 requires B to reject. Checker 1 may
use `E_CERT_RELATION` and `E_CERT_DOMAIN`; checker 2 may use
`missing_expected` and `duplicate_component`. All four diagnostic
spellings are illustrative local choices, not normative codes.

| Alternative | Assessment |
|---|---|
| Keep codes implementation-defined (recommended) | Preserve existing contracts; test local documented codes and normative verdicts separately. |
| Add a small report-location convention | Useful optional interoperability, without reserving every local code. |
| Publish a full ISA-wide E_CERT registry | New interface/versioning work; no evidence it is required for correctness. |
| Reuse launch statuses or quantum fault codes | Conflates checker rejection with run failure or quantum oracle outcome. |

## Recommended exact spec diff

No semantic change or mandatory rejection registry is required. If the
council wants explicit wording, append to §12.3:

```diff
+Checker diagnostic codes other than codes explicitly mandated elsewhere
+in this specification are implementation-defined. A checker SHOULD
+document its stable code meanings and report the failed normative
+obligation and certificate location with a rejection. Such codes are
+scoped by checker name and version; their spelling does not alter the
+verdict or any executor status/fault code. This convention does not
+replace mandated E_SCHEDULE_INFEASIBLE behavior or K55 diagnostics.
```

The original request's mandatory report schema would be a new API; it
should not be inferred from present text. An application needing that
API can version its checker-report format independently.

## Hashes, catalog and consumers

No source, object, target, catalog, schedule or certificate bytes need
change. Optional checker report fields affect only that report's format
and identity. Consumers must not compare an implementation's code against
an invented normative registry. A normative schedule failure still needs
its mandated code and validation stage.

## Conformance vectors and verification

Use A/B above as negative schema/domain tests; assert rejection and the
normative clause, and separately assert the implementation's documented
local code. For an otherwise valid schedule containing duplicate maximal
matching entries, retain K55's named diagnostic and staged rejection.
Do not turn a checker-local mismatch into a program fault or invalid
source verdict. This is a clause derivation; no checker test was run here.
The common document verification checks this disposition's required
sections and source links.

## Release and after acceptance

**No new K requirement and no 0.10 blocker.** Optional 0.9 editorial
clarification is sufficient. The orchestrator can disposition request 2
as documentation/API guidance; it should not file an ISA semantic bug
solely for missing E_CERT spellings. Existing checker tests may continue
to pin their own stable documented codes.

---

## Dossier part: 5u3 (run contract-5u3-2026-11-02 round 1 accepted; passed accept-4ht-recheck-2026-11-02 round 1 unchanged)

# 5u3 — exact pointer fixpoints without verdict-changing caps

Proposal for the dialect council; `b-dialect-spec-5u3`, linked to
`bennett-plugin` bp-fj1. This job writes no dialect or plugin source.

## Defect classification and North Star scope

Both dialect `Bennett-Dialect-Spec.md` (draft 0.2.12) and the 0.3 draft
§5 require every verdict/candidate/dispatch domain to come from the
specified reference analysis. §5.1 caps INT atoms at K=4096, but does not
cap explicit object offsets or PT6–PT8 memory intervals. PT2/PT5 use
finite-width modular pointer arithmetic. Hence an explicit enumeration
is finite but can have 2^61 members. §5.1 already admits residue classes
and `*`; it does not require enumerative storage.

The bead establishes a severe implementation/performance problem, **not
by itself an inconsistent or undefined reference semantics**. A sound
over-approximation may still change a compile-time verdict, which §5
forbids. The proposed thresholds (4096 offsets, 4 outside extent, 32 for
unknown extent; max(64,extent/4) slots) are not justified as exact. They
must not become normative merely because one plugin uses them.

North Star §§0/3.3/6.1 require arbitrary defined bounded programs,
whole-program analysis and substitutable compilers; §8 rung 4 requires
unmodified SQLite. Widening that introduces a false handle-use/escape
rejection narrows those capabilities. Removing SQLite features, changing
its source, suppressing vectorisation or declaring valid pointer patterns
unsupported does not resolve the issue. Keep bp-fj1 open for practical
convergence; do not declare the rung delivered from a coarse fixpoint.

## Plugin evidence actually inspected

`../bennett-plugin-rung4/.tmp/rung4/PROGRESS.md` reports 177381 slots
plateauing by round 7 on the N=16, LLVM-18 closure, with additional atoms
still growing. The tail of `.tmp/rung4/prof/trace-k.log` shows round 39,
177381 slots, growth in SQLite integer/value sets, then
`§5.2 PT8/PT9/PT12 budget exhausted` at a memcpy in
`@sqlite3CreateForeignKey`, exit 1 after 3401.31 seconds. It does **not**
demonstrate a converged exact reference fixpoint or prove that remaining
growth is only a pointer chain. The supplied earlier 800k-slot report is
historical bead evidence, not reproduced here. No full sibling gate was
run, and no plugin implementation was copied.

## Alternatives and worked recurrence

Take width W=64 and an unfiltered inclusion cycle with one provenance X:

```text
S initially contains offset 0
S includes { (o+8) mod 2^64 : o in S }
```

Its exact least solution is `{o: o=0 mod 8, 0<=o<2^64}`. There are
`2^64/gcd(8,2^64)=2^61` offsets, representable by one residue class.
For W=8 the set is exactly 0,8,...,248 (32 offsets), followed by 0.
Starting at 3 instead gives 3,11,...,251; adding a seed at 4 gives two
cosets, not `*`. Extent=16 does not permit dropping offsets ≥16:
PT2 retains original provenance and adds EXT/top for possibly invalid
addresses; it does not turn numerical out-of-range into host escape.

A full-width same-object memory copy from offset o to o+8 can similarly
propagate one stored atom along that relation. An exact periodic memory
summary must retain storage width, intervals and value/root provenance;
merging all fields into one slot may turn a nearby integer field into a
handle-derived value. That would be a different verdict even though it
is conservative for aliasing.

| Alternative | Assessment |
|---|---|
| Unbounded explicit enumeration | Same reference semantics, often impractical. Not required by the existing text. |
| Normative widening with the bead's thresholds | Deterministic only with further rules for ordering/stickiness/joins; can reject previously admitted programs. Not acceptable without a capability-preserving lowering for every newly coarse case. |
| Exact symbolic sets and translation-cycle closure (recommended) | Preserves verdicts and handles this witness compactly. Does not claim every SQLite recurrence has this form. |
| Resource/time cap with an explicit unfinished build | Honest operational outcome, not a completed analysis or a source rejection. Remains implementation work. |

## Recommended exact spec diff

Add a dialect K/clarification adjacent to §5.1's K and §5.2's least
fixpoint, in both maintained maps:

```text
The reference bounds INT atoms as above; it imposes no additional
cardinality bound on pointer-offset sets or memory intervals. Implementers
MAY use exact symbolic sets, shared interval relations and SCC
acceleration instead of enumerating represented offsets or slots.
All reference sets and byte/representation-width distinctions must be
preserved for verdicts, candidate sets and dispatch domains. A coarser
summary is not the reference result merely because it is sound for
aliasing. An unfinished analysis reports an unfinished build with the
rule and exhausted implementation resource, not a source rejection,
completed verdict or run-time fault for a valid input.

In a pure modular-translation inclusion SCC, if every cycle transfer is
an unfiltered fixed displacement at one bit width W and preserves one
base/provenance coordinate, close the generated displacements as a
subgroup of Z/(2^W). For a single self-cycle of stride s, each seed a
denotes the coset a modulo gcd(s,2^W). Union distinct seed cosets. For
multiple vertices, retain vertex-specific path displacements; do not
merge their seed coordinates. Apply the same rule to a memory relation
only when every transfer preserves the complete storage interval and
representation width and all PT6–PT8 read/overlap results are identical
to the represented individual slots. Retain every ROOT and FN alternative
explicitly. Otherwise use the original rules or another exact method.
PT2's pointer-index width and preserved high pointer bits still apply;
this rule does not replace them by unrestricted full-pointer addition.
```

Add to §24:

```text
Analysis representation/acceleration is implementation policy; the
default result is the exact §5 least fixpoint, including existing K=4096
INT abstraction. Time or memory caps do not alter that result. A report
of unfinished analysis keeps the remaining implementation obligation open.
```

This recommends an exact acceleration and explicitly **declines new
verdict-affecting bounds**. If council instead wants a new abstract
domain, it must supply canonical joins, evaluation order independence,
ROOT/partial-access rules and a lowering that preserves all programs
previously in scope; the current bead does not establish those properties.

## Hashes, catalog and consumers

An exact representation clarification changes no materialised program,
ISA object/certificate or catalog bytes. A dialect publication still
gets its required revision/mapping identity. A threshold widening could
change descriptors, dispatch domains, diagnostics and emitted object
hashes, so cannot masquerade as a local plugin optimization. Plugin and
independent dialect checker should compare normalized exact results on
small-width cases, not implementation data-structure counts.

## Conformance vectors and verification

Enumerate all W=8, stride-8 cases above and compare their symbolic cosets;
W=64 is a symbolic cardinality test, never a 2^61-element allocation.
Test stride 0, stride 1, multiple seeds, a cycle with a filter (must not
use the pure-cycle rule), and GEP with I(a)<P(a). Memory vectors include
same-width full copies, overlapping partial copies and adjacent handle/
integer fields; retain PT6's non-handle top and ROOT distinctions. Check
identical verdicts independent of worklist order. Mathematical cosets are
checked by [contract-verification](2026-11-02-contract-verification.md).
The SQLite exact fixpoint and production gate remain unverified here.

## Release and after acceptance

Recommend a **dialect K clarification on the current 0.2/0.3 tracks**,
not an ISA-0.10 dependency. As stated, 5u3 is primarily an implementation
scalability request. After acceptance, add the finite vectors and let the
plugin owner establish exact convergence on both LLVM majors and the
full rung-4 closure. No new source restriction is authorized by this note.
