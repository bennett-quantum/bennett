# Dossier (round 2): bennett-4ht re-check of z4c and adg with the round-1 fat-object statements appended

Scope (advisor ruling R6(b), 2026-11-02): round 1 of this run (astra only) re-checked four accepted contract proposals against the rubric's standing check "the mixed fat object stays reachable" (bennett-4ht) only. checker-diagnostics and 5u3 passed and are not in this round. z4c and adg failed only for a missing mixed-fat-object statement (blocking items z4c-4HT-1, adg-4HT-1), with no objection to their accepted contract content. Each proposal below is its round-1 doc.md verbatim, followed by a section appending the exact statement the round-1 fix asked for, verbatim, as the addition to its 'Hashes, catalog and consumers' section. Nothing else changed. Grade only whether the appended statements close z4c-4HT-1 and adg-4HT-1 and whether either proposal still fails the standing check.

---

## Dossier part: z4c (run contract-z4c-2026-11-02, round 1 accepted)

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

## Dossier part: adg (run contract-adg-2026-11-02, round 1 accepted)

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
