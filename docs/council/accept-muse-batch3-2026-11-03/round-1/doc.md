# Acceptance dossier (Muse seat, batch 3): 0jq, checker-fault-rate, brt-vbi, adg, pe1

Scope (advisor ruling R13, 2026-11-03; maintainer decision D2: 0jq is routed as an in-version 0.9 K once this seat accepts): each proposal below was ACCEPTED by both other council members (sol, astra) in its latest round (empty blocking lists, consensus agree) and satisfied the rubric's standing bennett-4ht check (mixed fat object stays reachable) in that round. This is the final acceptance seat: grade each proposal independently on its own merits. Each part names its run, accepted round and the spec it amends. Several parts cite the shared scoping statement `docs/notes/2026-11-02-rev2/fat-object-scope.md`; it is reproduced once in the appendix. Parts are separated by horizontal rules.

---

## Dossier part: 0jq (run pass2-0jq-2026-11-02; accepted by sol, codex in round 3; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-03-notefix/0jq.md)

# 0jq — structural-only certificates and the owner of an inverse-pair proof

Council proposal for `b-isa-spec-0jq` (P1); no normative text is changed.

## Round-1 blocking items and resolution

Read the [round-1 report](../../../../bennett/docs/council/pass2-0jq-2026-11-02/round-1/report.md)
and both `out-sol.json` and `out-codex.json` in that directory. The table
maps every blocking item to this revision; it claims a proposed resolution,
not a new council verdict.

| Item | Change and witness |
|---|---|
| sol 0JQ-1; codex B1 — device-object/root inventory missing | Append the §12.3 mixed-object rule below and cross-reference it from §9.2. Witness: native main calls device A and B; the two object/root certificates inventory device owners only, with no main region. |

## Defect and North Star scope

ISA 0.9 §12.1 admits structural `adjoint_table` and `translation_lemma`
claims; §12.3 K13 explicitly admits standalone structural claims without a
schedule. However, §12.3's region schema requires `verification.oracle: i`
and `fault_rate`, without an applicability rule or a no-claim encoding.
An action has no fault outcome (§5.3), and an adjoint-table proof does not
assert an oracle relation or a fault census. In addition, §9.2 defines
`reference_program_hash` as **the oracle's** interface hash although the
required §12.3 binding also occurs in action certificates. These are
contract gaps (rubric C5/C8). The published controlled-action fixture
already uses `oracle:null`; that practice needs normative wording.

The ownership part of the request is **already substantially decided**:
§4.5 `qinplace` puts `inverse_pairs` in the certificate record of the
region whose body contains the instruction, including when that region is
nested. §9.3 requires linked certificate composition. K63's two call
occurrences and K65's private-cleanup exclusion do not move that owner to
either oracle or to an outer caller. A packet transport convention is
needed only to identify the linked owner record, not a new proof owner.

North Star §§4.2/4.4/5.1 requires general quantum actions, composable
certificates, and honest proof/evidence labels. Forcing a non-permutation
action to fabricate an oracle/T3 claim narrows that scope. The proposed
null encoding preserves each capability and every remaining obligation.

## Alternatives and worked witness

Take an action with body `h t`. The adjoint table establishes that its
source adjoint is `h t`; H²=I follows exactly from §4.4. It does not
establish a permutation assertion: H|0>=(|0>+|1>)/sqrt(2). Putting that
structural claim's index into `verification.oracle` would change its
meaning. A fault count of zero on an invented domain also asserts a
census that was never performed.

For ownership, let `outer` call `inner`, and let only `inner` contain
`qinplace @G @H tk x`. The covering entry belongs to
`regions[closure(inner)].verification.inverse_pairs`. Its `claim:i`
indexes **inner's** claims array. A same-numbered claim in outer is not
that claim. Two visits to inner resolve their own token/argument coverage;
a proof at budget 2 does not cover an argument-token tuple 3 merely
because the outer root uses 3. The existing componentwise bound for the
instruction's primary token and exact `arg_tokens` rule still apply.

| Alternative | Result |
|---|---|
| Require a dummy oracle claim or zero fault report | Misrepresents the assertion; reject. |
| Make the two verification entries nullable/conditional | Preserves structural-only packets and existing applicable checks. Recommended. |
| Put nested entries/claims in the outer region record | Contradicts §4.5's owner and makes claim indices ambiguous. |
| Resolve linked owner records by closure hash | Uses the existing `regions` map and §9.3 composition. Recommended. |

## Recommended exact spec diff

Replace §9.2's definition and the indicated §12.3 schema fragments:

```diff
-`reference_program_hash` = the oracle's interface hash.
+`reference_program_hash` = the interface hash of the certificate's
+root reference subject, oracle or action. It is not the hash of a
+claim's separate expected program. `closure_hash` remains required.

-verification: { oracle: i, ... fault_rate: { ... } }
+verification: { oracle: i | null, ... fault_rate: null | { ... } }
```

Append to §12.3:

```text
verification.oracle is null when this record makes no oracle/table/
program comparison claim. A non-null index must name an applicable
exhaustive or sampled comparison claim in this record's claims array;
its explicit expected relation determines its meaning. A structural
adjoint-table or translation claim is not such a comparison claim.

<!-- muse-fault-rate-paragraph -->
verification.fault_rate is required and has type null | RATE. For action and perm_action records it MUST be null and fault_rate_contexts MUST be absent. For an oracle record it MUST be a RATE whenever a fault census is asserted or is required to discharge an executable or scheduled acceptance claim; it MAY be null only when the record asserts no fault census, and null discharges no fault-rate obligation.
<!-- /muse-fault-rate-paragraph -->

For kind=oracle, verification.fault_rate MUST be a RATE whenever a fault census is asserted or is required to discharge an executable or scheduled acceptance claim (including every oracle in the complete invocation tree of a bound schedule, via fault_rate_contexts); it MAY be null only when the record asserts no fault census, and null discharges no fault-rate obligation and satisfies no zero-fault gate.

An action
has no fault outcome of its own; a nested oracle's census belongs to
that oracle and its resolved invocation. Applicable oracle-correctness,
fault-rate, borrowed-system and realisation obligations remain required
before an executable or algorithm acceptance claim can use them.
A non-null fault_rate must be validated even when no acceptance claim requires it.

The owner of a qinplace inverse-pair entry is exactly the region whose
source body contains that instruction (§4.5). After linking, select that
region's record by its exact closure hash in the composed regions map;
claim indices are local to that record. Imported proofs must be present
in the linked certificate, or reached by the existing checked
inverse_pair_library reference to its linked library certificate.
Conflicting records for one closure must not be chosen arbitrarily:
resolve them by §9.3 composition or reject the composition. An outer
record, an oracle callee record, and the two private qinplace call edges
cannot substitute for the owner. Before any effect of the enclosing CC/R region call, check coverage for
every transitively executed qinplace using its owner entry and resolved
token and classical arguments (§4.5). Failure is a CC trap or R
FAULT_UB_TRAP; validation cannot wait until after earlier effects.
```

This wording does not make an adjoint-table claim a proof of the
instruction's inverse-pair obligation, or turn numerical agreement into
an exact structural proof. `unitary` and `channel` retain their own
applicable claim types. Fault-rate invocation encoding is handled by
[jw7](../2026-11-02-pass2/b-isa-spec-jw7.md), not invented again here.

## Fat-object applicability

Incorporate [the shared scoping statement](../2026-11-02-rev2/fat-object-scope.md#citable-scoping-statement).
Append the following proposed normative paragraph to §12.3, cross-referenced from §9.2:

```text
For a mixed fat object, object_hash identifies the embedded or linked ISA
object, and bindings.closure_hash selects its certified device root.
reference_program_hash identifies that oracle or action root's interface,
not native main or a separate expected program. The container associates
each object/root pair with its certificate; several device roots may have
separate certificates. Each composed regions map contains the required
device-region owner records and checked linked-library proofs. Native-only
host code, argv/envp and host-only libc require no region record, oracle
comparison, fault census or inverse-pair entry.
```

The shared statement lists today's assumptions and the exact remaining
container, launch, budget, handle, tape and host-memory contract changes.
This note does not assume that the device object is the entire binary.

## Hashes, catalog and consumers

No source, interface, closure, target, schedule or `ref@0.9` catalog bytes
need change under an authorized in-version repair. Replacing an inapplicable
fault report with null changes certificate bytes. Linkers,
specialisers and checkers must preserve owner-local claim indices and
resolve linked library proofs before use. Old ambiguous standalone action
bindings need explicit validation, not silent reinterpretation.

## Conformance vectors and verification

Require structural H and translation-only packets with `oracle:null` and
no fault census; reject a structural index masquerading as an oracle
comparison. An absent census must not satisfy a rung's zero-fault gate.
For outer→inner→qinplace, accept the covering entry in inner; reject an
outer-only entry, dangling library reference, changed G/H closure,
uncovered token argument and claim index into another record. Test two
inner contexts, swapped G/H, inherited control, and default-covered calls.

The H² and non-permutation facts are exact algebra checked by
[check_rev2.py](../2026-11-02-rev2/check_rev2.py). The originating note cites:
`../bennett-circuits/docs/design/2026-11-01-m5-contract-requests.md`,
“Structural-only packets”. No new packet checker is implemented here. A composed root packet may
contain inner's correctly keyed owner record; packet containment does not
move the entry into the outer region record. For the published controlled-action
fixture migration, the root table claim at index 0 gives verification.oracle:0;
the numerical-only flip record retains null, and both action fault-rate
placeholders become null. These are proposed certificate changes only.

## Release and route

Recommend a **0.9 K applicability/hash-definition repair**. The owner rule
needs clarification and link/consumer tests, not a new proof mechanism.
Keep 0jq open for council acceptance and producer/checker implementation.
Maintainer D2 (2026-11-03) authorizes this in-version 0.9 K route only
after the joint 0jq/checker-fault-rate revision passes sol+astra and a
Muse seat accepts. Until both conditions hold, 0jq remains HELD and is
not ACCEPTED FOR SPEC. The publication rules below apply.

## Publication and validation boundary

This is a revision proposal, not council acceptance or a consumer implementation.
The default publication rule in spec/README.md requires a full version bump
for semantic changes. The recommended 0.9 K route has conditional maintainer
authorization under D2; it still requires the joint sol+astra round and
Muse acceptance stated above. This note grants no council acceptance. All unchanged-hash claims assume unchanged header/source
and catalog envelopes. A full version publication recomputes affected symbol,
object, target, schedule, certificate and versioned ref-library identities and
consumer pins even when recipe bodies stay fixed. Published 0.9 bytes remain
available; older closed-schema readers require an upgrade for new fields.

The reproducible finite and document checks are in [check_rev2.py](../2026-11-02-rev2/check_rev2.py):
`timeout 120 python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/docs/notes/2026-11-02-rev2/check_rev2.py`.
Executed for this revision: exit 0, all eight PASS result lines.
These finite checks verify witnesses and revision structure; they implement
no proposed-format checker or host shim. No full repository gate or sibling gate is claimed: scripts/pre-push
uses git/worktree writes, forbidden by this runner, and its setup changes paths
outside this job. Underlying beads remain open for publication and consumers.

## Muse blocking items and resolution

This joint revision starts from the latest graded notes: 0jq round 2
(`19ffcda5e44a87d0878c89e357fa4ccea163d50883e031aff781fb3e43bd923e`)
and checker-fault-rate round 3
(`71a74c494872f94fa40271dd0d81ef140fa01d6095006ad859400a5b5037a189`).
It proposes resolutions, not council verdicts. Both notes carry the same
Muse paragraph above and the same conditional oracle sentence, copied
verbatim from [out-muse.json](../../../../bennett/docs/council/accept-muse-batch2-2026-11-02/round-1/out-muse.json).
RATE abbreviates `{invocation:{args,budget},domain,faults_by_code,
undefined_excluded,layout_dependent_excluded,exclusion_evidence?}`.
A non-null RATE binds its own exact invocation and full oracle domain;
it never inherits a convenient claim's budget. For a bound schedule,
every complete-tree oracle context, including defaults and predicated-off
calls, needs its recount; the legacy field is the first canonical
context's projection. Exclusions do not shrink the reference census.
The complete context and evidence contract is retained in
[checker-fault-rate.md](checker-fault-rate.md); these requirements neither
invent a census for a structural-only packet nor relax acceptance gates.

| Blocking item | Resolution and concrete witness |
|---|---|
| 0jq-M1 | The closed schema requires `fault_rate: null | RATE`; actions use null and omit `fault_rate_contexts`. Both action fault-rate placeholders become null. A missing key is malformed, and null proves no zero-fault result. The reference_program_hash definition and owner-local inverse-pair rules are unchanged. |
| checker-fault-rate-M1 | Oracle RATE is conditional on an asserted/required census, including every oracle context in a bound schedule. A structural-only oracle may use null; it discharges no census or zero-fault gate. All accepted recount, deterministic context projection and classifier-bundle rules remain. |

There are no other Muse blocking items for these two proposals. The
accepted mixed-fat-object scope, hash conditions and prior-round fixes
remain. Relative witness links now point to their original directories;
historical verification reports above remain historical.

### Structural-only oracle conformance vector

Take a standalone oracle with body `r = lift.add x a; lift.retval r` and
a checked structural `adjoint_table`/translation claim only, no comparison
claim, no asserted census and no bound schedule. Supply all ordinary
identity, signature, frame and claim fields as required. The following
JSON is the verification fragment under test, not a complete certificate
or a newly introduced certificate field:

<!-- structural-only-oracle -->
```json
{"kind":"oracle","verification":{"oracle":null,"fault_rate":null}}
```

| Request for the same structurally valid packet | Expected result |
|---|---|
| Standalone structural validation, no census asserted | Accept as a structural packet. |
| Executable acceptance requiring a fault census | Reject that acceptance claim: null discharges no census obligation. |
| Scheduled acceptance requiring all oracle contexts, or a zero-fault gate | Reject that acceptance claim: no RATE/context coverage is supplied. |
| Remove fault_rate instead of using null | Reject schema validation: required key missing. |
| Assert a census while retaining null | Reject the asserted census. |

With the same body, args=["1"] and B=1, a verified RATE counts
256 code-1 faults over the full 4×4×16 domain; with B=2 it counts zero.
Those are actual census results and cannot be inferred from the null
packet. The focused script checks these applicability outcomes, action
null versus omitted keys, the fixture migration, unchanged owner rules
and the retained recount/bundle text. It is a finite contract test,
not an implementation of the proposed production certificate checker.

### Paragraph byte identity and verification

Extract exactly the UTF-8 bytes between the two `muse-fault-rate-paragraph`
markers, excluding the marker lines and the paragraph's terminating LF.
There is no line reflow or Unicode normalization. These are the paragraph
bytes quoted by Muse in 0jq-M1; the extra conditional oracle sentence
is copied verbatim from checker-fault-rate-M1 in both notes.

| Note | Shared paragraph SHA-256 |
|---|---|
| 0jq.md | `b34376b04d0d2e295018245c1f7f3ce36b4f55ad5ed18e8f127119e36b9685b0` |
| checker-fault-rate.md | `b34376b04d0d2e295018245c1f7f3ce36b4f55ad5ed18e8f127119e36b9685b0` |

Verification: `timeout 30s python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/check_notes.py joint`
exited 0. Both extracted hashes equal the values above and Muse's exact
paragraph. No source, fixture, spec or catalog was edited.

Every producer and closed-schema reader using these amended 0.9
certificate bytes must upgrade together for the required nullable field
and context/evidence fields; older readers cannot silently accept them.
Remaining council work: joint sol+astra review, then a Muse acceptance
seat. D2 keeps 0jq HELD until those conditions pass. Publication and
producer/checker implementation follow acceptance; this revision performs
none of those steps and reserves no K number.

---

## Dossier part: checker-fault-rate (run contract-checker-fault-rate-2026-11-02; accepted by sol, codex in round 4; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-03-notefix/checker-fault-rate.md)

# Checker fault rates — oracle-only, invocation-bound recounts

Full round-4 revision for council review, 2026-11-02; checker request 3
in the existing cross-repo filing queue. Supersedes
`2026-11-02-rev/checker-fault-rate.md`; proposal only. This document
retains the complete accepted recount contract and replaces its unsupported
artifact-transport premise.

## Defect classification and North Star scope

ISA 0.9 §12.3 names fault_rate.domain, faults_by_code and two exclusion
counters but provides no invocation binding for them. K13 binds claims
individually and scheduled certificates at the root; several claims or
callee contexts can use different args/budgets. §§5.2/14.1 makes F_B
depend on those values. A flat recount is therefore ambiguous. This is
an S0 contract gap, not a change to oracle execution.

A separate gap is explicit here: §§12.1–12.3/14.1 name exclusion counters
but do not define independently replayable exclusion evidence. The first
note's assertion that this validation was already specified was wrong.
The repair below supplies that obligation and a concrete default.
North Star §§3.2/5.1 separates native-comparison exclusions from reference
validation and records source-definedness assumptions; post-optimization
classifiers do not detect source UB already erased by optimization.

North Star §5.1 requires fault-rate reporting and §8 requires zero on
its acceptance domains. Dropping rates, choosing a convenient budget,
removing excluded inputs from reference validation or treating unchecked
counts as verified would not meet that requirement. Actions remain
supported: §5.3 gives them no fault outcome of their own, so this repair
uses an explicit non-applicable value for their records.

## Alternatives and concrete witnesses

| Choice | Consequence |
|---|---|
| Take the first claim's invocation | Ambiguous and dependent on claim ordering. |
| Restrict a region to one invocation | Removes existing composition capability. |
| Bind every oracle recount explicitly | Recommended; exact standalone invocation or full scheduled context. |

The oracle has x:wire[2], target:wire[2], fault:wire[4], a:i2, and body
`r = lift.add x a; lift.retval r`. At args=["1"], budget
["1","0","0","0"] cannot reach retval: all 4×4×16=256 tuples contribute
code 1. Budget ["2","0","0","0"] succeeds on all 256 with payload
(x+1) mod 4 and code 0. Every tuple includes its arbitrary target and
fault words. Incoming f=1 becomes zero on a code-1 failure; success
leaves it one. The final accumulated fault word is not the fault event.

For a classification-count fixture flagging precisely x=0, 64 of those
256 tuples are excluded from native comparison. Even then B=1 reports
faults_by_code={"1":"256"}, with undefined_excluded="64" separately.
This fixture demonstrates counting and evidence replay; it does not
assert that the two-row reference add itself has source UB. A real UB
classifier must be identified with its materialized program/configuration.

The published controlled-action-09 certificate has `controlled` and
`flip` records of kind perm_action. Neither has an F_B. The corrected
representation puts fault_rate:null on both, without evaluating an
invented action oracle. An action containing the two oracle calls above
also uses null, while its callee records retain both bound recounts.

## Recommended exact spec changes (§12.3)

Replace verification.fault_rate's schema and add the sibling context
field inside verification. The notation RATE abbreviates this record:

```text
RATE = {invocation:{args,budget},domain,faults_by_code,
        undefined_excluded,layout_dependent_excluded,exclusion_evidence?}
verification.fault_rate: null | RATE
verification.fault_rate_contexts?:[{context_key, ...RATE}]
```

Add the following normative rules:

```text
F_B recounts and fault_rate_contexts apply only to kind=oracle records.
<!-- muse-fault-rate-paragraph -->
verification.fault_rate is required and has type null | RATE. For action and perm_action records it MUST be null and fault_rate_contexts MUST be absent. For an oracle record it MUST be a RATE whenever a fault census is asserted or is required to discharge an executable or scheduled acceptance claim; it MAY be null only when the record asserts no fault census, and null discharges no fault-rate obligation.
<!-- /muse-fault-rate-paragraph -->

For kind=oracle, verification.fault_rate MUST be a RATE whenever a fault census is asserted or is required to discharge an executable or scheduled acceptance claim (including every oracle in the complete invocation tree of a bound schedule, via fault_rate_contexts); it MAY be null only when the record asserts no fault census, and null discharges no fault-rate obligation and satisfies no zero-fault gate.
For action and perm_action, verification.fault_rate MUST be null and
fault_rate_contexts MUST be absent. Null denotes no action-owned fault
outcome, not a verified zero-fault oracle. Each contained oracle
invocation remains subject to the recount obligations in its own oracle
record; no action placeholder discharges those obligations.

Every oracle RATE binds its own invocation using K13's exact typed args,
four-component budget, token-tuple encodings and validation. It inherits
no claim's invocation. Missing or conflicting bindings reject a requested
verified recount before replay; old unbound data cannot discharge it.

The rate is intrinsic to the underlying oracle's §5.2 F_B. Its domain
uses §12.2 resolution, validity, omission-at-zero and enumeration for
that oracle with zero inherited controls. Targets, fault words, inputs,
region cells and declared borrowed components each contribute as the
domain specifies; inherited control wires add no components to this
intrinsic recount. A predicate's basis value does not suppress counts.
The report is not the probability that a root execution reaches a call.

Each enumerated tuple contributes exactly once to faults_by_code[c]
when code(F_B)=c and c is nonzero. The final XOR-accumulated fault word
is never the predicate for this count. All tuples in the declared domain
are recounted, including native-comparison exclusions. Counts use
canonical nonnegative decimal integer strings; omit zero fault-code
entries. Code keys denote nonzero valid fault codes. Each count and the
sum of fault counts are at most n, the exact enumerated domain size.
Exclusion counts are separate, not subtractions from n or faults_by_code.
If limits prevent a legal recount, report unchecked (host limit),
discharging no verified fault-rate obligation; do not shrink the domain,
substitute partial counts, or declare the input domain invalid.
```

### Complete contexts and deterministic compatibility projection

```text
For an oracle present in the complete §12.1 invocation tree of a bound
schedule, including default-covered and predicated-off invocations,
report exactly one fault_rate_contexts record per context when there is
more than one. Use increasing bytewise JCS context-key order. Every
explicit invocation MUST equal that context's resolved args and budget,
including nested token tuples. Equal tuples with different process-local
token ids denote the same recount; the ids are not certificate values.

The required legacy fault_rate is the first canonical context record
with context_key removed. It MUST equal that projection and discharges
only that context. For one context the legacy RATE suffices and MUST bind
that context; an optional singleton context array, if supplied, must
match it. Missing, duplicate, reordered, foreign or conflicting context
records reject the requested report. A standalone oracle RATE binds its
own invocation and domain, with no invented root-context inheritance.
```

This keeps the required old field meaningful; a later arrays-only
interchange version could remove the projection. Claim reordering has
no effect. Full context identity, not merely (variant, control count),
distinguishes different nested token budgets and call occurrences.

### Exclusion evidence and default validation

Add this schema for RATE.exclusion_evidence:

```text
{ materialisation_hash, reference_program_hash, native_build_hash, native_entry,
  invocation:{args,budget}, domain_hash,
  classifiers:[{category,artifact_hash,version,configuration,input_map_hash}] }
```

```text
Exclusion counters MUST be independently reproduced from classification
evidence bound to the same materialized program, native build,
invocation and complete declared domain. materialisation_hash hashes
UTF-8 JCS of the recorded materialisation configuration;
reference_program_hash uses §9.2's oracle interface hash; the containing
region's closure hash and certificate object binding additionally identify
the linked reference program whose classifications are replayed;
native_build_hash identifies the corresponding comparison build, and
native_entry explicitly selects its exported comparison entry/thunk.
domain_hash hashes UTF-8 JCS of the exact domain record, without LF.
Invocation equality uses K13's resolved encodings.

Each category is undefined or layout_dependent. artifact_hash identifies
replayable classifier bytes, version and configuration identify its
semantics/options, and input_map_hash identifies the replayable mapping
from a full interface tuple to native/classifier inputs. All hashed
artifacts must be available by content for a checked result. Multiple
classifiers in one category combine their flagged sets by union; a tuple
counts once per category. Categories may overlap, so their counts must
not be added without computing their union for a native exclusion set.

Default validation replays the identified classifiers and input mapping
on every domain tuple and recomputes both counters independently. When
initial target/fault values do not feed the native program, mapping may
ignore them, but their distinct tuples still each count. A classification
flag reports an exclusion under that declared classifier; it does not
prove complete detection of source-level UB or erase the recorded
definedness assumption. This does not change F_B semantics.

Missing replayable evidence or unsupported classifier semantics makes
the exclusion report unchecked and discharges no exclusion-dependent
acceptance obligation; it MUST NOT mean zero exclusions. This includes
an asserted zero count. A complete F_B recount may still be verified
separately. Evidence that replays to different counts or has conflicting
bindings rejects the requested exclusion report. This is a new validation
contract, not a premise supplied by the pre-repair counter names.
```

ISA 0.9 defines no certificate-attachment transport. This repair introduces
a separate checker input bundle containing the certificate and the required
content-addressed artifacts. By default, classifier and input-map blobs
are supplied outside the ISA object and certificate schemas; artifact_hash
and input_map_hash are SHA-256 of their exact raw bytes. The checker verifies
those digests before replay. Missing required blobs make the exclusion
report unchecked; mismatched digests reject it. Other transports MAY supply
the identical addressed bytes. This bundle is a new checker input contract;
it adds no attachments field to either closed schema. A producer's flag list
alone is not replay evidence. All materialisation, reference-program/closure,
native-build/entry, invocation and complete-domain bindings above still apply.
Native comparison still excludes flagged inputs as the North Star
requires, while reference validation keeps every domain element.

## Mixed fat object (bennett-4ht)

Incorporate [the shared mixed-fat-object scoping statement](../2026-11-02-rev2/fat-object-scope.md#citable-scoping-statement),
including its explicit remaining launch and host-memory obligations.
Add to §§9/10/12: "A fat native binary may embed VM objects only for
marked modules. The launch manifest selects the marked VM entry, with
its actual args, budget, token tuples and image; the certificate covers
that VM closure's oracle contexts. Unmarked host main, argv/envp and
libc are not invented oracle records and need no F_B recount. Classifier
and native-comparison artifacts may be thunks calling the corresponding
materialized marked native entry with captured host state and input
mapping; native_build_hash identifies that build/entry. They need not
translate or replay the entire native binary as a VM object. Required
marked dependencies and runtime shims are recorded; host device handles
remain process-local, with only resolved shapes/tuples entering bindings."

Separate host launches of the same marked arithmetic module under B=1 and
B=2 use separate root schedule/certificate bindings and rates. The native
host binary stays native. fault_rate_contexts enumerates calls within one
bound root schedule: a device action wrapper containing both calls instead
supplies two contexts in that schedule, with distinct call-occurrence keys.
A native comparison of successful inputs uses the corresponding arithmetic
thunk, not main's exit code. Root-relative contexts never identify native
process entry. Each embedded device object/root has its own certificate
association; the external checker bundle associates artifacts with that
certificate's device closure. It introduces no whole-host certificate.

## Round-1 blocking items and resolution

| Item | Change and concrete witness |
|---|---|
| sol FR-1 / codex CFR-1: F_B applied to actions | Oracle-only recount/context rules; null for both published perm_action records. Nested oracle counts remain required. |
| codex CFR-2: unsupported exclusion premise and ambiguous recount domain | Explicit new hash-bound classifier replay default; reference recount retains all 256 tuples even with 64 separately excluded. Unavailable validation is unchecked, never assumed zero. |

## Round-2 blocking items and resolution

The [round-2 report](../../../../bennett/docs/council/contract-checker-fault-rate-2026-11-02/round-2/report.md)
and out-sol.json/out-codex.json agree that FR-1, CFR-1 and CFR-2 are resolved.
Both accept core scope; sol blocks only CFR-3. The convenor table calls the
second seat astra, while the stored report/output identifies it as codex;
this revision follows the actual outputs and claims no new council acceptance.

| Item | Exact resolution and concrete witness |
|---|---|
| sol CFR-3 — nonexistent existing attachment transport | The replacement §12.3 paragraph explicitly introduces the external checker input bundle and raw-byte SHA-256 validation. check_rev4.py supplies both blobs and reproduces 64 exclusions; removing either leaves exclusions unchecked while the independent B=1 recount remains {"1":"256"}; replacing either addressed blob with changed bytes rejects before replay. |

No prior recount or evidence-binding rule is removed. Oracle RATE typing,
reference interface versus closure binding, and separate-launch context
wording also incorporate the round's nonblocking clarifications.

## Hashes, publication and consumers

Recommend an authorized 0.9 K certificate repair. New invocation,
context, null and exclusion-evidence bytes change certificate identity.
Under an unchanged 0.9 semantic envelope, §9.2 leaves source/interface/
closure/object, target, schedule and ref catalog identities unchanged.
A full-version publication instead requires regenerating version-envelope
identities and dependent pins. No publication is performed here.

Producer, classifier harness and checker must implement the same binding
and context rules. Zero-fault rung gates select the actual oracle domain
and invocation; no budget result covers another by guessing. Monotonic
success would require its own proved statement. The existing cross-repo
request remains open for acceptance/implementation; this notes-only job
does not close it or mutate tracker/council files.

## Conformance vectors and verification

Require both 256-tuple budgets, all incoming fault values, B=0, reordered
claims, a mismatched args vector, missing budget, equal token tuples with
different ids, default/predicated-off contexts and two call occurrences.
Duplicate/omit/swap a context, conflict with its invocation or alter the
legacy projection: reject. Test overlapping classifier categories,
missing evidence (including zero counters), stale artifact/domain/native
bindings and evidence that flags 64 tuples without shrinking F_B counts.
An action without oracle callees has null; one with oracle callees still
has null and separately checked callee recounts.

This script checks exact finite reference arithmetic and the counting
witness by hand-model replay; it does not run a certificate or exclusion
checker and does not establish a real source-UB classification.

```python
from collections import Counter
import itertools
import json
import hashlib

rows = list(itertools.product(range(4), range(4), range(16)))
assert len(rows) == 256

def outcome(x, a, b):
    # Two reference rows: add, then retval. No memory or earlier fault.
    return (((x+a) % 4, 0) if b >= 2 else (0, 1))

for b, expected in [(0, {1: 256}), (1, {1: 256}), (2, {})]:
    counts = Counter()
    for x, t, f in rows:
        payload, code = outcome(x, 1, b)
        if code:
            counts[code] += 1
        after = (x, t ^ payload, f ^ code)
        assert (after[0], after[1] ^ payload, after[2] ^ code) == (x, t, f)
    assert dict(counts) == expected
assert (1 ^ outcome(0, 1, 1)[1]) == 0
assert (1 ^ outcome(0, 1, 2)[1]) == 1
# Synthetic replayable classifier fixture; not an assertion about add UB.
flagged = [row for row in rows if row[0] == 0]
assert len(flagged) == 64
assert sum(outcome(x, 1, 1)[1] != 0 for x, t, f in rows) == 256
# The exclusion predicate duplicates across 4*16 initial target/fault values.
assert len({x for x, t, f in flagged}) == 1
counters = {'faults_by_code': {'1': '256'}, 'undefined_excluded': '64',
            'layout_dependent_excluded': '0'}
assert int(counters['faults_by_code']['1']) == 256
# Null is distinct from an oracle's verified zero-fault record.
action_record = {'kind': 'perm_action', 'verification': {'fault_rate': None}}
assert json.loads(json.dumps(action_record))['verification']['fault_rate'] is None
assert 'fault_rate_contexts' not in action_record['verification']
zero_oracle = {'invocation': {'args': ['1'], 'budget': ['2','0','0','0']},
               'faults_by_code': {}}
assert zero_oracle is not None
# Binding changes cannot accidentally reuse a domain digest.
a, b = {'bundles': [0, 1]}, {'bundles': [0]}
def digest(d):
    return hashlib.sha256(json.dumps(d, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
assert digest(a) != digest(b)
print('PASS fault-rate: 768 oracle tuples; 256 faults with 64 separate exclusions; action null distinction')
```


## Round-4 executable witness and evidence boundary

The files [checker-fault-rate.bisa](../2026-11-02-rev4/checker-fault-rate.bisa) and
[oracle_witness.rs](../2026-11-02-rev4/oracle_witness.rs) exercise this exact two-row oracle
through the read-only reference interpreter library. For B=0,1,2 and each
x=0..3, the witness compares the independent reference outcome with the
literal reversible machine, calls its actual commit method for all 4 target
words and 16 incoming fault words, and then inverses every executed step.
It checks the entire initial machine snapshot and clean frames. This covers
768 full interface tuples: 256 faults at each short budget, zero at B=2.

[check_rev4.py](../2026-11-02-rev4/check_rev4.py) supplies two fixed, serialized raw blobs in
an external in-memory bundle: a version-1 synthetic classifier selecting
mapped x=0, and a version-1 input map selecting tuple component 0. Their
literal bytes and raw-byte digests are present in the checker. Replaying
all 256 tuples yields undefined_excluded="64" and
layout_dependent_excluded="0". Missing classifier, missing map and an
asserted-zero count with missing evidence are unchecked. A digest mismatch
in either blob rejects before classifier interpretation; even JSON whitespace
changes fail under the old digest. A replayed count of 63 or conflicting
invocation/domain/program binding rejects. Unsupported classifier semantics
is unchecked. All these cases preserve the independent F_B recount.

This is a finite contract witness, not a production certificate checker,
a native build, a proof of source UB detection, or a complete serialized
multi-context certificate. The latter remains the conformance publication
obligation described above: concrete §12.1 keys, B=1 map {"1":"256"}, B=2
map {}, exact first-context legacy projection, and rejection on missing
contexts or a corrupted projection. It is not claimed implemented here.
The synthetic evidence bindings identify only this fixture's recorded
configuration; no real native-comparison certification is asserted.

Run the focused build and witnesses from any working directory:

```sh
timeout 300s python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/run_witnesses.py
```

The script unsets GUI/browser variables, sets TMPDIR and CARGO_TARGET_DIR
under .tmp/sol-notefix-s4, bounds processes at 6 GiB, uses -j4 and applies
timeouts. It runs no full gate or git command and changes no interpreter
source. It runs the retained finite CFR-3 checker in memory against this
revision, redirecting only the job artifact paths. The current run exited
0: all 768 oracle tuples and classifier-bundle positive/negative cases
passed. Historical outcomes remain in
[the shared verification results](../2026-11-02-rev4/verification.md). The earlier inline
hand model remains an independently understandable counting example; the
actual interpreter/machine witness above supplies execution evidence.

## Muse blocking items and resolution

This joint revision starts from the latest graded notes: 0jq round 2
(`19ffcda5e44a87d0878c89e357fa4ccea163d50883e031aff781fb3e43bd923e`)
and checker-fault-rate round 3
(`71a74c494872f94fa40271dd0d81ef140fa01d6095006ad859400a5b5037a189`).
It proposes resolutions, not council verdicts. Both notes carry the same
Muse paragraph above and the same conditional oracle sentence, copied
verbatim from [out-muse.json](../../../../bennett/docs/council/accept-muse-batch2-2026-11-02/round-1/out-muse.json).
RATE abbreviates `{invocation:{args,budget},domain,faults_by_code,
undefined_excluded,layout_dependent_excluded,exclusion_evidence?}`.
A non-null RATE binds its own exact invocation and full oracle domain;
it never inherits a convenient claim's budget. For a bound schedule,
every complete-tree oracle context, including defaults and predicated-off
calls, needs its recount; the legacy field is the first canonical
context's projection. Exclusions do not shrink the reference census.
The complete context and evidence contract is retained in
[checker-fault-rate.md](checker-fault-rate.md); these requirements neither
invent a census for a structural-only packet nor relax acceptance gates.

| Blocking item | Resolution and concrete witness |
|---|---|
| 0jq-M1 | The closed schema requires `fault_rate: null | RATE`; actions use null and omit `fault_rate_contexts`. Both action fault-rate placeholders become null. A missing key is malformed, and null proves no zero-fault result. The reference_program_hash definition and owner-local inverse-pair rules are unchanged. |
| checker-fault-rate-M1 | Oracle RATE is conditional on an asserted/required census, including every oracle context in a bound schedule. A structural-only oracle may use null; it discharges no census or zero-fault gate. All accepted recount, deterministic context projection and classifier-bundle rules remain. |

There are no other Muse blocking items for these two proposals. The
accepted mixed-fat-object scope, hash conditions and prior-round fixes
remain. Relative witness links now point to their original directories;
historical verification reports above remain historical.

### Structural-only oracle conformance vector

Take a standalone oracle with body `r = lift.add x a; lift.retval r` and
a checked structural `adjoint_table`/translation claim only, no comparison
claim, no asserted census and no bound schedule. Supply all ordinary
identity, signature, frame and claim fields as required. The following
JSON is the verification fragment under test, not a complete certificate
or a newly introduced certificate field:

<!-- structural-only-oracle -->
```json
{"kind":"oracle","verification":{"oracle":null,"fault_rate":null}}
```

| Request for the same structurally valid packet | Expected result |
|---|---|
| Standalone structural validation, no census asserted | Accept as a structural packet. |
| Executable acceptance requiring a fault census | Reject that acceptance claim: null discharges no census obligation. |
| Scheduled acceptance requiring all oracle contexts, or a zero-fault gate | Reject that acceptance claim: no RATE/context coverage is supplied. |
| Remove fault_rate instead of using null | Reject schema validation: required key missing. |
| Assert a census while retaining null | Reject the asserted census. |

With the same body, args=["1"] and B=1, a verified RATE counts
256 code-1 faults over the full 4×4×16 domain; with B=2 it counts zero.
Those are actual census results and cannot be inferred from the null
packet. The focused script checks these applicability outcomes, action
null versus omitted keys, the fixture migration, unchanged owner rules
and the retained recount/bundle text. It is a finite contract test,
not an implementation of the proposed production certificate checker.

### Paragraph byte identity and verification

Extract exactly the UTF-8 bytes between the two `muse-fault-rate-paragraph`
markers, excluding the marker lines and the paragraph's terminating LF.
There is no line reflow or Unicode normalization. These are the paragraph
bytes quoted by Muse in 0jq-M1; the extra conditional oracle sentence
is copied verbatim from checker-fault-rate-M1 in both notes.

| Note | Shared paragraph SHA-256 |
|---|---|
| 0jq.md | `b34376b04d0d2e295018245c1f7f3ce36b4f55ad5ed18e8f127119e36b9685b0` |
| checker-fault-rate.md | `b34376b04d0d2e295018245c1f7f3ce36b4f55ad5ed18e8f127119e36b9685b0` |

Verification: `timeout 30s python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/check_notes.py joint`
exited 0. Both extracted hashes equal the values above and Muse's exact
paragraph. No source, fixture, spec or catalog was edited.

Every producer and closed-schema reader using these amended 0.9
certificate bytes must upgrade together for the required nullable field
and context/evidence fields; older readers cannot silently accept them.
Remaining council work: joint sol+astra review, then a Muse acceptance
seat. D2 keeps 0jq HELD until those conditions pass. Publication and
producer/checker implementation follow acceptance; this revision performs
none of those steps and reserves no K number.

---

## Dossier part: brt-vbi (run derive3-brt-vbi-2026-11-02; accepted by sol, codex in round 1; amends the Bennett dialect spec (../bennett-dialect-spec/spec/); source note bennett-isa-spec/docs/notes/2026-11-02-derive3/brt-vbi.md)

# brt-vbi — delivery of arbitrary-width runtime helper bodies

Council proposal, not a specification or runtime implementation. Origin:
`brt-vbi` (blocked decision), blocking `brt-zct` in bennett-runtimes.
References: [dialect 0.2.12](../../../../bennett-dialect-spec/spec/Bennett-Dialect-Spec.md)
§§12.1, 12.7–12.8, 13.1, 19.1, and the corresponding
[0.3 draft](../../../../bennett-dialect-spec/spec/Bennett-Dialect-Spec-0.3-draft.md).

## Exact defect and North Star scope

§12.7 names width-specific ordinary runtime bodies for wide multiply,
divide, remainder and shifts. §12.8 similarly names integer intrinsic
helpers, including slot-based wide forms. §19.1 requires matching-major
runtime bitcode before materialisation. §13.1 publishes an offline
instance-request protocol for arith, but none of these clauses publishes
a runtime-integer request/response contract or a collection procedure for
helpers introduced during normalisation. A consumer cannot depend on
the runtime producer's private generator interface.

This is a **dialect delivery/interoperability gap**, alongside an actual
missing-implementation obligation. It is not a new ISA arithmetic
instruction or launch ABI gap. Naming an ordinary helper already makes
its body required; a finite default library failing to contain i257
does not make that LLVM width unsupported. The gap matters to North Star
§§3.2–3.3, 5.1's whole materialised LLVM and reproducible comparison.
It does not justify narrowing widths, trapping valid arithmetic, omitting
libc/Julia/SQLite closure, or declaring the broader brt-zct work complete.

## Alternatives and concrete witness

Read-only source witness:
`../bennett-runtimes/.tmp/sol-runtimes-queue/tmp/runtime-width-request.ll`.
It loads two i257 values, multiplies, calls `llvm.ctpop.i257`, stores i257.
Both LLVM 18 and 23 `opt -passes=verify -disable-output` accept it.
Both live `dist/llvm<M>/bennett-runtimes.bc` lack definitions for
`__bennett_rt_i257_mul` and `__bennett_rt_i257_ctpop`, confirmed with
matching-major `llvm-nm --defined-only`. These are current observations,
not an inference from the producer's progress report.

For a concrete numerical vector, a=2^256+3, b=2. Modulo 2^257 the product
is 6 and its population count is 2. A five-limb input slot has widths
[64,64,64,64,1]; ctpop writes [2,0,0,0,0]. Dropping the top input limb
can be caught separately by ctpop(a)=3. This requires actual ordinary
bodies, not a declaration that merely passes LLVM verification.

| Alternative | Assessment |
|---|---|
| Publish an offline request/manifest protocol in the dialect | Producer-independent, analogous to arith; recommended. |
| Prebuild every admitted width and operation | A possible complete distribution, but costly; a common-width subset is only a cache. |
| Publish a separate runtime ABI note | Viable only if versioned and normatively incorporated by the dialect; a producer README alone cannot bind competitors. |
| Add ISA primitives or a private driver-generator API | Unnecessary machine extension or unpublished coupling. |

## Recommended exact dialect/ABI text

Insert the following titled subsection at the end of §12.8 before the
examples, and cross-reference it from §19.1. Mirror it in both tracks.
The executable name below is a proposed public interface, not a claim
that today's runtimes supplies it.

```text
Runtime integer instance delivery v1.

The runtimes distribution MUST supply an offline executable interface:
  bennett-runtimes-instantiate --request REQUEST --bitcode OUTPUT_BC
                             --manifest OUTPUT_JSON
The driver may configure the executable path. Exit zero means both
outputs are complete; nonzero means no output is usable. Generation
must not require network access, a host runtime service or private
consumer knowledge. The distribution MUST identify its version.

REQUEST is UTF-8 JSON with exactly schema, llvm_major, target_triple,
data_layout and entries. schema is "bennett-runtimes-instantiations-1";
llvm_major is the link's integer LLVM major; target_triple and
data_layout are the link's effective LLVM strings. Each entries element
has exactly op (string) and width (integer, not boolean).

The op set is mul, udiv, sdiv, urem, srem, shl, lshr, ashr from §12.7;
and bswap, bitreverse, ctpop, ctlz, cttz, fshl, fshr, sshl_sat,
ushl_sat, smul_fix, umul_fix, smul_fix_sat, umul_fix_sat, sdiv_fix,
udiv_fix, sdiv_fix_sat, udiv_fix_sat, pdep, pext, clmul,
smul_with_overflow and umul_with_overflow from §12.8. Dots in an
intrinsic name become underscores. width is the original integer
operand width W, not a limb width or result aggregate size. The
operation and width must be admitted by the link's LLVM major and the
corresponding published row; §12.7 requests require W>128, and the
overflow-helper requests require W>64. Unknown fields/operations,
nonintegral/out-of-range widths and target/major/layout mismatches are
errors. Every valid request remains an implementation obligation.

Duplicates denote one instance. Canonical request bytes are UTF-8 JCS,
without a trailing LF, with unique entries sorted by op's unsigned
UTF-8 bytes then ascending numeric width. request_sha256 is the
lowercase hexadecimal SHA-256 of those bytes. A supplied width list
or prebuilt cache MUST NOT become a capability limit.

OUTPUT_BC is ordinary matching-major bitcode whose triple and
DataLayout equal the request. For each requested (op,W), provide the
exact public definition, type, scalar flags, result convention and
fault behavior of §§12.7–12.8. In particular, wide mul is
void @__bennett_rt_i<W>_mul(ptr dst,ptr a,ptr b), and wide ctpop is
void @__bennett_rt_i<W>_ctpop(ptr dst,ptr a). The existing shadow-stack
slot layout, partial top limb and push/store/call/load/pop order are
unchanged. All reachable implementation bodies must be supplied or
resolved through the published matching-major base runtime/arith
distributions and their published instance protocols. No unresolved
instance placeholder, trap stub or hidden host implementation counts
as delivery.

OUTPUT_JSON is JCS with exactly schema, request_sha256,
bitcode_sha256 and exports. schema is "bennett-runtimes-instances-1";
bitcode_sha256 hashes the exact OUTPUT_BC bytes. exports lists every
externally visible definition in that module, sorted by unsigned UTF-8
symbol bytes, each with exactly symbol and function_type; function_type
is LLVM's printed function type for the requested major, without the
function name or attributes. Every requested public symbol must occur
exactly once and have its published type. Generation with identical
canonical request and producer version must reproduce both output
byte strings regardless of output paths. The driver verifies hashes,
triple, layout, definitions and types before using the output.

Collection is a link-preparation fixed point. Starting from the selected
device entries and their conservatively reachable bitcode closure,
include calls already naming these helpers and all helpers that the
published normalisation rules will introduce, including vector
scalarisation, N27 and the N22 applications after N27/N32. Collect
arith instances by §13.1 as well. Resolve runtime/arith requests and
their dependencies until no new (provider,instance) is required and
every required body is linked. Include all possible device call
targets; do not select just one runtime input path. Declarations alone
do not satisfy the fixed point. A provider cycle must resolve to actual
linked definitions; repeated unresolved requests are a loud failure.

This discovery is a non-emitting analysis using the published rules;
it does not rerun or change §12.1's normative rule order. Link the
complete collected bodies before final materialisation, identically
in the lifted and native comparison inputs. If later optimisation or
materialisation reveals a new required helper, restart preparation
with the enlarged request and rebuild both outputs; never patch only
one build or silently leave it unresolved. Failure to generate a
valid instance is an implementation blocker, not an unsupported-width
verdict, narrower substitute or permitted fault of the device program.
```

Add to §19.1 after the bitcode-source paragraph:

```text
Before final materialisation the driver MUST complete the runtime
integer instance-delivery fixed point of §12.8 and the arith requests
of §13.1, using the same resolved closure in both builds. Whole-program
device mode uses its entire device closure; selective-module mode
collects the union required by its marked device roots. Neither mode
requires host-only code to become a device region.
```

## Hashes, catalog and consumers

Request and output hashes are different identities; neither is an ISA
`object_hash` or the arith/ref catalog hash. Provider-version changes
invalidate the generation cache even when the request is identical.
Generated bitcode changes materialised closures, costs, stack use and
the resulting object/schedule/certificate bindings. Drivers, plugins,+runtimes, numerical providers and conformance owners must coordinate
publication and repin. No ISA `ref@0.9` recipe change is necessary.

## Conformance vectors and actual verification

The bounded command in [INDEX](INDEX.md) ran both major-specific LLVM
verifiers and symbol audits: exit 0, both missing-definition assertions
passed. This establishes the delivery witness, not helper implementation
or whole-program execution. No sibling gate was run.

After publication require: i129/i192/i257 partial-top-limb values;
mul and ctpop together; large admitted widths with a resource-bounded
generation test; narrow intrinsic helpers; scalar flags and overflow
aggregate types; all helper families with published fault behavior.
Check reordered/duplicate requests canonicalise identically, unknown
op/invalid width/major/layout reject loudly, manifests cannot omit or
mis-type a requested definition, and changed request/bitcode hashes fail.
Test a helper introduced only by scalarisation, one after N32/repeated
N22, a transitive dependency and a discovery restart. Verify byte
reproduction in relocated directories and link/execute both materialised
builds. Merely passing opt verification is insufficient.

## K entry and publication route

**No ISA 0.9/0.10 K entry:** this is a dialect/tool-distribution contract.
Proposed dialect decision row: `RUNTIME-INSTANCES-1 | §§12.8,19.1 |
offline request/manifest and complete device-closure fixed point |
brt-vbi | additive versioned delivery protocol`. Recommend the next
published 0.2 patch and the corresponding 0.3 draft text. A separate
ABI note is acceptable only with a normative versioned dialect reference.
Leave brt-vbi/brt-zct open for ratification and implementation; publication
of a proposal does not unblock a consumer's unpublished interface.

## Mixed fat object

[fat-object-scope.md](../2026-11-02-rev2/fat-object-scope.md) binds this
proposal (North Star §§2, 3.3, 4.4). Collect helpers for marked modules and
their linked device closures. Multiple roots may share generated bodies;
each device root retains its own certificate/context association. The
ordinary native host binary, host entry/argv/envp and host-only libc stay
outside that inventory. Native comparison binds the matching materialised
device closure. Request manifests are build inputs, not a new launch,
budget, handle or effect-tape protocol. Container/root association and
host-memory mapping still need the exact mixed-launch additions named in
the shared scope note; this delivery decision keeps them reachable.

---

## Dossier part: adg (run contract-adg-2026-11-02; accepted by sol, codex in round 3; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-03-notefix/adg.md)

# adg — loaded-device-program state across launches

Full revised proposal for council review; `b-isa-spec-adg`. This replaces
the [first-pass note](../2026-11-02-contract-adg.md) as a review document;
it does not edit the published spec or interpreter. Clause numbers refer
to [ISA 0.9](../../../spec/Bennett-ISA-Spec-0.9.md).

Round 1 accepted the memory/ledger rule (sol and astra); the round-2
bennett-4ht re-check accepted the added device-instance scoping statement.
Muse subsequently blocked the proposal on **adg-M1**, a core §7.3/§10
lifetime omission. This revision retains those accepted decisions and
chooses Muse's recommended program-lifetime device state, with per-run
entropy position and effect tape. It still requires renewed sol/astra
review and a later Muse seat; it is not yet ACCEPTED FOR SPEC.
Round 2 then raised adg-R2-1/adg-R2-B1: persistent device models also
need exclusive ownership. This revision adopts launch-time acquisition
and adds overlapping-run witnesses; no other contract fix is made.

## Defect and North Star scope

ISA §7.1 defines initial memory, allocation table and bump pointer without
saying whether initialization occurs at load or every run. **§3.3 places
the register ledger at program scope; §3.2 lists it among machine-state
components.** §10 gives a run exclusive ownership only until CLOSED;
§7.4 and T4 restore a run's entry state on eligible reversal. These support
program-lifetime state but do not explicitly settle classical-memory
initialization.

The same omission affects §7.3's initially empty console, clock `c=0`
and block sector map. The original §10 addition's unqualified
“initialization is never repeated merely to start a run” could also
incorrectly carry entropy position `p` into the next run, although §10
copies a new entropy tape at each `bennett_run`. A persistence-reading
executor and a reset-reading executor would still return different clock
and block results on the second entry. This is adg-M1's observable S0
contract defect, not an instruction or allocator change.

Dialect 0.3 draft §§6.5–6.6 requires a persistent qreg table in device
memory and parameter/result identities across entries. North Star §3.1's
register handles and §5's REPL/library device model require this lifetime;
its block-device uses require a disk that survives repeated entries. A
reset on every entry loses the table while registers remain live.
Persistence preserves repeated SQLite/kernel invocations and every demo
rung. No capability is rejected or made inert by this repair. Oracle-local
workspace initialization and cleanup remain governed by §5.2.

## Chosen lifetime rule and alternatives

| State | Established | Later run / reversal |
|---|---|---|
| CC/R memory bytes, allocation table, bump pointer (§7.1) | Once per loaded device program | Inherit preceding CLOSED run's state; eligible reversal restores entry values. |
| Register ledger and live identities (§3.3) | Program instance; entries created by the existing operations | Survive CLOSED unless consumed/freed; ownership is released at CLOSED. Ids remain subject to §3.3's non-reuse rule, including reversal. |
| Console bytes, clock `c`, block sector map (§7.3) | At device-program load; block map from `layout.block_image` under K10, else empty | Persist; effects and their reversal change them; CLOSED does not reset them. |
| Copied entropy tape and position `p` (§§7.3/10) | Each `bennett_run`, with `p=0` | Bound to that run; undo restores that run's position, never a previous run's cursor. |
| Active effect tape, dynamic environments and run history (§§7.3–7.4/10) | Each run | Record that run's effects/history; no inheritance into the next run. Saved journals remain a separately versioned tool interface. |
| Host-minted / device-minted budget tokens (§5.4) | Program / minting run respectively | Host token valid until unload; device token invalid after its run is CLOSED (or revoked by reversal). |

Program-lifetime memory and devices are the recommendation: they match the
ledger, T4's entry-state restoration and the existing persistent-table
consumer. Explicitly resetting *all* devices on each run is Muse's other
possible contract decision, but would require different cross-entry disk
assumptions and would not preserve the selected persistence rule. An
implicit reset when no register is live still changes classical/device
results and has no supporting clause. The recommendation changes none of
§7.1's heap/table limits or `free` semantics.

## Concrete lifecycle witnesses

### Classical memory retained from round 1

Use `ptr_width=16, H=16, A_tab=2, S_cells=0, null_size=1,
heap_base=16, heap_limit_max=16` and one global `g` at base 1, size 1,
image `00`. Run A allocates one byte (address 16), stores 7 in `g`,
completes and is CLOSED. Run B loads `g`, allocates one byte and completes.
The results and full allocation state after B are:

| A disposition before B | B result `(g, allocation)` | Bump | Table `(base,size,live,pinned)` |
|---|---|---|---|
| COMPLETED → CLOSED | `(7,17)` | 18 | `[(1,1,1,1),(16,1,1,0),(17,1,1,0)]` |
| COMPLETED → REVERSED → CLOSED | `(0,16)` | 17 | `[(1,1,1,1),(16,1,1,0)]` |

All heap bytes are zero in this witness; `g` is respectively `07` or
`00`, and every other logical byte is zero. A reset-reading executor would
return `(0,16)` even without reversal, distinguishing the interpretations.
If A also frees 16, B still allocates 17: the dead entry remains and
storage is not reclaimed. After allocations at 16, 17 and 18 across CLOSED
runs, a fourth heap allocation faults with code 2, with bump still 19 and
no table/byte mutation: the global plus three heap entries fill the table.
A FAILED R call whose completed prefix allocated 16 and stored 7 leaves
those mutations in place on close; explicit eligible reversal removes
them. Closing is never implicit rollback.

### Device witness resolving adg-M1

Use one loaded instance, sequential device CC launches whose bodies call
R helpers. The layout has disjoint live globals: `src` at 16, size 512,
all bytes `a5`; `dst` at 528, size 512, zero; `clk` at 1040, size 8,
zero; `ent` at 1048, size 1, zero. Set `ptr_width=16, H=12, A_tab=3,
S_cells=0, null_size=1, heap_base=2048, heap_limit_max=64`.
`block_image` contains sector 0 = 512 zero bytes and sector 1 = 512
`ff` bytes, so sector 2 is initially **absent**.

Run A's R helper executes, in order: `clock.read(clk)`,
`block.write(2,src)`, `console.write(src,1)`, `entropy.read(ent,1)`.
Its copied entropy tape is `[11]` (hex bytes). It writes clock value 0,
leaves `c=1`, creates sector 2 with 512 `a5` bytes, appends console byte
`a5`, consumes its entropy byte and has four effect-tape entries.

Run B's R helper executes `clock.read(clk)`, `block.read(2,dst)` and
`entropy.read(ent,1)`, with its own copied tape `[33]`. It returns
`(load.i64 clk, load.i8 dst, load.i8 ent)`:

| A disposition before B | B result (decimal) | Device state after B | Tape belonging to B |
|---|---|---|---|
| COMPLETED → CLOSED | `(1,165,51)` | `c=2`, console=`a5`, sector 2 present with 512 `a5` bytes | Three entries, beginning with B's clock read of 1; entropy entry is byte `33`. |
| COMPLETED → REVERSED → CLOSED | `(0,0,51)` | `c=1`, console empty, sector 2 absent; B reads all 512 zero bytes | Three entries, beginning with B's clock read of 0; entropy entry is byte `33`. |

In either case B starts with `p=0`, ends with `p=1`, and its tape never
contains A's four entries. Closing A releases its record; reversal first
removes its active effects. Saved journals do not become B's tape. Inspect
all 512 bytes of `dst`, not only the returned first byte. Sectors 0 and 1 remain present
with their initial bytes; reversal must preserve the distinction between
present-zero sector 0 and absent sector 2. A FAILED after the four effects
has the same retained device prefix until reversed. Reversal restores the
modeled console sequence; T4 does **not** retract externally observed output.
Fresh loading restores the initial clock/console/block map and memory.

### Overlapping open runs: adg-R2-1 / adg-R2-B1

Use disjoint live buffers, no quantum registers and one loaded device
instance initially at clock 0 and empty console. A's entry calls an R
helper that reads the clock and appends `a5`; B's entry calls a different
R helper that reads the clock and appends `5a`. Both transitive call
closures reference the same clock and console despite disjoint buffers.

Without device ownership, A completes open at `c=1`, console=`a5`;
B completes and closes at `c=2`, console=`a55a`. Reversing A decrements
the clock and pops one byte, leaving `c=1`, console=`a5`, rather than
A's entry `c=0`, empty console. B's byte is popped. This is the reported
T4 counterexample, including A reversing after B touched both models.

Under the proposed fix, A acquires both models before execution and
retains them after COMPLETED. B's attempted launch returns
`E_INVALID_STATE`, with no run effects, entropy consumption, memory
mutation or ownership acquisition; `c=1`, console=`a5` remain. Now A
can reverse while still owning both: `c=0`, console empty and A's own
buffers/entropy cursor/effect tape restore their entry state. T4 holds.
Ownership remains A's while REVERSED, so another B attempt still
conflicts until A is CLOSED.

| A disposition, then retry B | B reads | State after B |
|---|---|---|
| A CLOSED without reversal | 1 | `c=2`, console=`a55a` |
| A REVERSED then CLOSED | 0 | `c=1`, console=`5a` |

B has its own new entropy position and tape. Reversing B, if eligible,
restores B's entry values (respectively `c=1`, console=`a5`, or `c=0`,
empty console). A cannot reverse after it is CLOSED. The same launch
conflict applies while A is FAILED, including its retained effect prefix.
For block, A writes previously absent sector 2; a B closure that reads
that block model conflicts until A closes. After unreversed A, retry B
reads all 512 `a5` bytes; after reversed A, it reads 512 zero bytes and
sector 2 remains absent. Present-zero sectors retain their presence.

A run using only the clock and a run using only the console can remain
concurrent if their existing register/memory ownership is also disjoint.
Reversing the clock run restores its clock and own buffers and leaves the
other run's console bytes unchanged. A launch needing clock plus block
while another run owns block acquires neither model: acquisition is atomic.
An effect hidden in an R helper is in the transitive footprint even when
its branch is not taken in this execution. This schedules conflicting
device use across CLOSED boundaries and preserves disjoint concurrency,
all existing sequential programs and the mixed-fat-object path.

The finite contract witness in
[ownership_witness.py](../../../.tmp/sol-notefix-s4/ownership_witness.py)
checks these outcomes and every pair of the eight model subsets. It is
a small model of the proposed ownership rule, not a repeated-launch ABI
implementation. The separate read-only interpreter witness below checks
the actual clock, console, block, entropy and inverse operations.

## Recommended exact spec diff

These are the complete additions to the published 0.9 text, superseding
the first-pass diff. They are not a patch to that unpublished proposal.

Insert after §7.1's Initial state sentence:

```diff
 Initial state: bump = `heap_base`, table = the pre-entries in layout
 order, memory zero except images.
+That state is established once when the program is loaded. These
+persistence rules concern CC/R classical memory, allocation-table entries
+and the bump pointer. These components belong to the loaded program and
+persist across runs. For sequential launches, a new run inherits these
+components from the preceding CLOSED run. Closing a run does not restore
+its entry state. If the preceding run was successfully REVERSED before
+being CLOSED, these classical components have their restored entry values
+(§7.4, §10, T4); quantum-state restoration retains T4's exactness
+hypotheses and error bounds. A FAILED run otherwise leaves its completed
+prefix mutations in place. Register-ledger entries and live register
+identities likewise persist under §3.3; ownership ends at CLOSED, not the
+register lifetime. Unloading and loading a program creates a new program
+instance with initial state; register ids of the old instance are not
+imported into it.
```

Insert immediately after §7.3's device table, before **BLOCK-IMAGE**.
The following paragraph is Muse's requested wording verbatim:

```diff
+Device-model state belongs to the loaded program like classical memory (§7.1): the console byte sequence, the clock counter c and the block sector map are established at load from their initial values (the block map from layout.block_image, K10) and persist across runs, changed only by effect execution and by reversal (§7.4, T4); closing a run does not reinitialise them. The entropy position p is per-run state: it starts at 0 over the entropy tape copied at that bennett_run (§10). The effect tape is per-run.
+The console sequence, clock counter and block sector map are exclusive
+program-state resources subject to the run ownership rules of §10.
```

Append to §10's **States** paragraph, after its final §3.3 reference:

```diff
+Persistence does not relax exclusive ownership of touched registers or
+memory while a run is not CLOSED. Separate loaded program instances have
+separate state; the §7.1/§7.3 program-lifetime state is never reinitialised
+merely to start a run. This persistence rule does not prohibit disjoint
+concurrent runs with disjoint model ownership sets as well as the
+existing register/memory conditions.
+At bennett_run, the run atomically acquires exclusive ownership of every console, clock and block model referenced by its entry's transitive CC/R call closure. Ownership lasts until CLOSED, including while COMPLETED, FAILED or REVERSED. If any required model is owned by another non-CLOSED run, bennett_run returns E_INVALID_STATE before executing the entry or acquiring ownership. Entropy positions and effect tapes remain per-run. Disjoint concurrent runs require disjoint model ownership sets as well as the existing register/memory conditions.
```

The §10 sentence deliberately names only program-lifetime state. §7.3
positively defines the separate per-run entropy and effect-tape lifetimes;
the amendment does not inherit dynamic environments, history or oracle
workspace into later runs. The original witnesses use sequential CLOSED runs. The overlap vectors
now add explicit device ownership; no concurrent memory merge is assumed.

Append to §14.3 T4, retaining its existing reversal eligibility,
quantum exactness/error bounds, audit and observed-event qualifications:

```text
Restoration concerns the run-owned state; state belonging exclusively to disjoint runs is unaffected.
```

Here run-owned state includes the §7.3 models acquired by the transitive
closure at launch; it never includes unrelated native host state.
The §10 restoration wording is read with this same run-owned scope.

Add after the §15 suite table (a suite G requirement):

```diff
+**Suite G — loaded-program lifetime (K-new).** Execute successive CC
+launches A and B in one loaded device program, each CLOSED before the
+next launch. With ptr_width=16, H=16, A_tab=2, S_cells=0, null_size=1,
+heap_base=16, heap_limit_max=16 and global g at base 1, size 1, image 00,
+let A allocate one byte and store 7 in g; let B return g and a new
+one-byte allocation. Without A reversal B returns (7,17), bump=18 and
+table=[(1,1,1,1),(16,1,1,0),(17,1,1,0)]; with successful A reversal
+before close B returns (0,16), bump=17 and
+table=[(1,1,1,1),(16,1,1,0)], in (base,size,live,pinned) order.
+Check every logical byte and table entry. Closing a FAILED A preserves
+its completed stores and allocations unless explicitly reversed.
+Bytes in the following device vector are hexadecimal. Use live, disjoint
+buffers and an initial block image with sector 0 all zero and sector 1
+all ff (512 bytes each), so
+sector 2 is absent. A reads clock 0, writes 512 a5 bytes to sector 2,
+appends a5 to the console and consumes byte 11 from its copied entropy
+tape. B reads the clock and sector 2 and consumes byte 33 from a new
+one-byte entropy tape. After unreversed A, B reads clock 1 and 512 a5
+bytes; after reversed A, B reads clock 0 and 512 zero bytes, with sector
+2 absent. Check sector presence, console persistence/restoration and
+unchanged sectors 0 and 1. In both cases B starts p=0, reads entropy
+byte 33 and has its own three-entry effect tape without A's entries.
+Repeat with A FAILED after its effects, with and without eligible
+reversal. Fresh load restores the initial program state. Check that
+CLOSED releases register ownership without destroying live identities,
+that host-minted tokens remain valid until unload, and that a device-
+minted token passed after its run is CLOSED returns E_ARG.
+**Suite G — overlapping device ownership.** With disjoint live buffers,
+let A read clock 0 and append a5, complete and remain open. A B entry
+whose transitive CC/R closure reads that clock and appends 5a returns
+E_INVALID_STATE at launch; c stays 1, console stays a5, and B has no
+effects or ownership. After A closes unreversed, retry B reads 1 and
+leaves c=2, console=a55a. After eligible A reversal then close, retry B
+reads 0 and leaves c=1, console=5a. While A is REVERSED but not CLOSED,
+B still conflicts; repeat while A is FAILED. Include transitive helper
+effects, a conflicting block read after A creates sector 2, and a launch
+requesting one free and one owned model: no partial acquisition.
+Disjoint clock-only and console-only runs may execute concurrently under
+the existing register/memory rules; reversing either restores its owned
+state and leaves the other's state intact. Check separate entropy
+positions/tapes, all bytes and block presence, not only scalar results.
```

Add to §0.2, assigning the next available K number when applied:

```text
K-new | §7.1, §7.3, §10, §14.3, §15 | LOADED-PROGRAM-LIFETIME: CC/R memory,
allocation table, bump pointer and console/clock/block state persist
across runs in one loaded device instance; entropy position and effect
tape are per-run; referenced console/clock/block models exclusively
owned from launch through CLOSED; CLOSED does not reverse. | b-isa-spec-adg | S | –
```

## Hashes, catalog and consumers

Under the **council-authorized in-version 0.9 K repair**, canonical source,
semantic envelope, target and catalog bytes remain unchanged; no hash
re-pin is needed. A full ISA-version bump would change §9.2 envelopes and
require new pins. This note changes neither `ref-0.9.json` nor expansion
recipes, charges, resources or target capabilities; no catalog check is
claimed here. Published 0.8 text is untouched.

A consumer resetting §7.1 memory or console/clock/block on each run must
separate its load and run lifecycles. The plugin's persistent qreg table
needs no redesign. Bindings/certificates replaying a later entry must
record its actual device entry-state/preparation assumptions; one fresh
load does not establish coverage of all histories. Entropy buffers remain
copied at launch; tape access remains associated with the particular run.
Existing `E_ARG` and `E_INVALID_STATE` suffice; no status number is added.

### Accepted bennett-4ht statement (verbatim)

In a mixed fat object, 'loaded program' means a loaded device program instance, not the native host process or entire fat binary. The native host may retain that instance and repeatedly invoke its device CC entries; the specified memory, allocation-table, bump-pointer and register-ledger persistence applies to that instance, with separate state for separate loaded instances. Loading a device program or closing or reversing a device run does not initialize or roll back unrelated native host state. This rule does not require moving native main, argv/envp handling or host-only libc into the device object. Later-entry certificate replay records the actual device entry-state preparation assumptions, without presuming a fresh native process.

That is the adg paragraph accepted in
[the round-2 4ht dossier](../../../../bennett/docs/council/accept-4ht-recheck-2026-11-02/round-2/doc.md).
The new console/clock/block rule has the same device-instance scope;
its per-run tapes cover device R effects, not unrelated native host I/O.
The ordinary native host binary and only marked device modules plus their
linked device closures remain reachable (North Star §§2, 3.3, 4.4).

The [shared fat-object scope](../2026-11-02-rev2/fat-object-scope.md) supplies
the remaining bennett-4ht publication obligations: a versioned
container-to-device-object/root/certificate inventory, native-call to device
entry bindings, budget and opaque-handle lifetime negotiation, and
device-run/tape association with effect-proxy ordering and replay. A general
host-memory-by-reference ABI must also specify address/layout mapping,
range/liveness, aliasing, ownership/synchronization, writeback and reversal.
The current copied-argument/hostcall ABI does not supply those mechanics.
They remain explicit boundary work, never grounds to require whole-binary
lowering or omit mixed execution. Certificates and native comparison retain
the selected materialised device closure as their subject.

## Read-only interpreter witness and reproduction

The public reference `ClassicalMachine` creates initial memory/devices in
its constructor; the CLI's `run_program` is explicitly one-shot. There is
no public API for transferring all program-owned state to a second run.
Thus the following **executed instruction/reversal witness** checks the
device primitives and their observable values, not a multi-launch ABI.
The cross-launch CLOSED transitions, separate tapes while retaining
devices, ownership and token vectors remain explicit suite G obligations.

The harness builds an ISA 0.9 object, computes and checks every interface
hash, and invokes the unmodified library through a job-local Cargo package.
`keep` calls A then executes B's operations in the same run. `undo` first
uncalls A, then executes B. Their one copied entropy tape is `[11,22]`:
B reads `22` without uncall and `11` with uncall, as it must **within one
run**. A fresh B-only machine supplied `[33]` reads `33` at position 0.
This intentionally differs from the two-launch vector's B entropy `33`
and separate three-entry tape. No reset or fake close is inserted into
the reference machine.

Both completed and FAILED A are also executed and whole-run reversed.
Complete snapshot equality checks memory, device state (including sector
presence), ledger, control, dynamic instances and fault/result state; the
initialized block map includes the present-zero sector. It does not inspect
retained audit-history layout or establish cross-run ledger/token lifetimes.
`keep` and `undo` check all 512 read bytes and tape counts, then verify
whole-run restoration too.

```rust
use bennett_isa_ref::{json::Json, ClassicalMachine, ClassicalValue, Object};
use std::collections::BTreeMap;

fn json(s: &str) -> Json { Json::parse(s).unwrap() }

fn object() -> Object {
    let a = "fn r @a () () () () ()\n^entry():\n\
        s = const.i16 16\np = inttoptr s\n\
        k = const.i16 1040\nc = inttoptr k\n\
        e = const.i16 1048\nep = inttoptr e\n\
        sector = const.i64 2\none = const.i16 1\n\
        effect clock.read c\neffect block.write sector p\n\
        effect console.write p one\neffect entropy.read ep one\nret";
    let b = "k = const.i16 1040\nc = inttoptr k\n\
        d = const.i16 528\ndp = inttoptr d\n\
        e = const.i16 1048\nep = inttoptr e\n\
        sector = const.i64 2\none = const.i16 1\n\
        effect clock.read c\neffect block.read sector dp\n\
        effect entropy.read ep one\n\
        cv = load.i64 c\nbv = load.i8 dp\nev = load.i8 ep\nret cv bv ev";
    let mut functions = vec![
        ("a", a.to_string()),
        ("failed", a.replace("@a ", "@failed ").replace("\nret", "\nfault 2")),
        ("b", format!("fn r @b () (cv:i64, bv:i8, ev:i8) () () ()\n^entry():\n{b}")),
    ];
    for (name, prefix) in [
        ("keep", "call @a\n"),
        ("undo", "call @a\nuncall @a () ()\n"),
        ("read", ""),
    ] {
        functions.push((name, format!(
            "fn cc @{name} () (cv:i64, bv:i8, ev:i8) () () ()\n^entry():\n{prefix}(cv, bv, ev) = call @b\nret cv bv ev"
        )));
    }
    let data = [
        ("src", "a5".repeat(512)), ("dst", "00".repeat(512)),
        ("clk", "00".repeat(8)), ("ent", "00".to_string()),
        ("disk", format!("{}{}", "00".repeat(512), "ff".repeat(512))),
    ];
    let mut symbols = BTreeMap::new();
    for (name, body) in &functions {
        let kind = if body.starts_with("fn r ") { "r" } else { "cc" };
        let results = if matches!(*name, "a" | "failed") { "[]" } else { "[\"i64\",\"i8\",\"i8\"]" };
        let sig = json(&format!(
            r#"{{"abi":"0.9","kind":"{kind}","params":[],"results":{results},"tier":"{kind}"}}"#
        ));
        symbols.insert(symbols.len().to_string(), json(&format!(
            r#"{{"name":"{name}","kind":"{kind}","signature":{},"interface_hash":"{}"}}"#,
            sig.canonical(), "0".repeat(64)
        )));
    }
    for (name, hex) in &data {
        symbols.insert(symbols.len().to_string(), json(&format!(
            r#"{{"name":"{name}","kind":"data","signature":{{"abi":"0.9","kind":"data","size":{},"tier":"-"}},"interface_hash":"{}"}}"#,
            hex.len()/2, "0".repeat(64)
        )));
    }
    let tail = r#"
section devices
{"models":{"block":{"version":"0.9"},"clock":{"version":"0.9"},"console":{"version":"0.9"},"entropy":{"version":"0.9"}},"services":{}}

section layout
{"A_tab":3,"H":12,"S_cells":0,"block_image":"disk","globals":{"src":{"base":16,"size":512,"image":"src"},"dst":{"base":528,"size":512,"image":"dst"},"clk":{"base":1040,"size":8,"image":"clk"},"ent":{"base":1048,"size":1,"image":"ent"}},"heap_base":2048,"heap_limit_max":64,"interface_regions":{},"null_size":1,"ptr_width":16}
"#;
    let render = |symbols: BTreeMap<String, Json>| {
        let mut text = format!(
            "bennett-object isa=0.9 object=0.9 launch=0.9 sched=0.9 cert=0.9 coverage=0.9 target=0.9 ptr_width=16\n\nsection symbols\n{}\n\nsection functions\n",
            Json::Object(symbols).canonical()
        );
        for (_, body) in &functions { text.push_str(&format!("{body}\n")); }
        text.push_str("\nsection data\n");
        for (name, hex) in &data { text.push_str(&format!("{name} {hex}\n")); }
        for line in tail.lines() {
            let line = if line.starts_with('{') { json(line).canonical() } else { line.into() };
            text.push_str(&format!("{line}\n"));
        }
        text
    };
    let parsed = Object::parse(&render(symbols.clone())).unwrap();
    let hashes = parsed.identity().unwrap().interface_hashes;
    for symbol in symbols.values_mut() {
        let name = symbol.get("name").unwrap().string().unwrap().to_string();
        let Json::Object(fields) = symbol else { panic!("symbol is not an object") };
        fields.insert("interface_hash".into(), Json::String(hashes[&name].clone()));
    }
    let object = Object::parse(&render(symbols)).unwrap();
    object.check_hashes().unwrap();
    object
}

fn main() {
    let o = object();
    for (name, fault) in [("a", None), ("failed", Some(2))] {
        let mut m = ClassicalMachine::new(&o, name, &[], &[0x11]).unwrap();
        let entry = m.snapshot();
        let outcome = m.run(100).unwrap();
        assert_eq!(outcome.fault, fault);
        assert!(!m.is_running());
        assert_eq!(m.clock(), 1);
        assert_eq!(m.console(), &[0xa5]);
        assert_eq!(m.effect_tape_len(), 4);
        assert_eq!(&*m.effect_tape()[0].bytes, &[0; 8]);
        assert_eq!(&*m.effect_tape()[1].bytes, &[0xa5; 512]);
        assert_eq!(&*m.effect_tape()[3].bytes, &[0x11]);
        m.reverse().unwrap();
        assert_eq!(m.snapshot(), entry, "complete restoration of {name}");
        println!("{name}: clock=1 console=a5 tape=4; reverse=entry");
    }
    for (name, entropy, clock, byte, ent, tape, console) in [
        ("keep", vec![0x11,0x22], 1, 0xa5, 0x22, 7, vec![0xa5]),
        ("undo", vec![0x11,0x22], 0, 0, 0x11, 3, vec![]),
        ("read", vec![0x33], 0, 0, 0x33, 3, vec![]),
    ] {
        let mut m = ClassicalMachine::new(&o, name, &[], &entropy).unwrap();
        let entry = m.snapshot();
        let out = m.run(100).unwrap();
        assert_eq!(out.fault, None);
        assert!(!m.is_running());
        assert_eq!(&*out.values, &[
            ClassicalValue::Int(64,clock), ClassicalValue::Int(8,byte),
            ClassicalValue::Int(8,ent),
        ]);
        assert_eq!(m.memory_bytes(528,512).unwrap(), vec![byte as u8;512]);
        assert_eq!(m.clock() as u128, clock+1);
        assert_eq!(m.console(), console.as_slice());
        assert_eq!(m.effect_tape_len(), tape);
        assert_eq!(&*m.effect_tape()[tape-1].bytes, &[ent as u8]);
        m.reverse().unwrap();
        assert_eq!(m.snapshot(), entry, "complete restoration of {name}");
        println!("{name}: ({clock},{byte},{ent}) block=512 checked bytes tape={tape}; reverse=entry");
    }
}
```

Run this exact command from any directory. All generated files and Cargo
outputs stay under `.tmp/sol-notefix-s4/`; the dependency source is read-only.
There are four Cargo jobs, a 4 GiB per-process address-space bound (in
addition to the runner's 14 GiB scope), no core dumps and a 240-second
timeout. This is one small witness executable, not a repository gate.

```sh
env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER \
  TMPDIR=/home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/tmp \
  CARGO_TARGET_DIR=/home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/target \
  python3 - <<'PY'
import os, pathlib, resource, subprocess
repo = pathlib.Path('/home/tobias/Projects/bennett-workspace/bennett-isa-spec')
job = repo / '.tmp/sol-notefix-s4'
(job / 'tmp').mkdir(parents=True, exist_ok=True)
crate = job / 'witness'
(crate / 'src').mkdir(parents=True, exist_ok=True)
note = (repo / 'docs/notes/2026-11-03-notefix/adg.md').read_text()
(crate / 'src/main.rs').write_text(note.split('```rust\n', 1)[1].split('\n```', 1)[0] + '\n')
(crate / 'Cargo.toml').write_text('''[package]
name = "adg-device-witness"
version = "0.0.0"
edition = "2021"
[workspace]
[dependencies]
bennett-isa-ref = { path = "../../../reference-interpreter" }
[profile.dev]
debug = 0
incremental = false
codegen-units = 4
''')
resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3,) * 2)
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
subprocess.run(['timeout', '240s', 'cargo', 'run', '--offline',
                '--manifest-path', str(crate / 'Cargo.toml'), '--bin', 'adg-device-witness', '-j4', '--quiet'], check=True)
PY
```

Expected stdout (the verification result below records whether reproduced):

```text
a: clock=1 console=a5 tape=4; reverse=entry
failed: clock=1 console=a5 tape=4; reverse=entry
keep: (1,165,34) block=512 checked bytes tape=7; reverse=entry
undo: (0,0,17) block=512 checked bytes tape=3; reverse=entry
read: (0,0,51) block=512 checked bytes tape=3; reverse=entry
```

Verification result: the exact bounded command above exited **0** and
reproduced all five stdout lines. Every assertion passed, including full
512-byte comparisons and complete entry-snapshot restoration for all five
cases. The reference interpreter and conformance sources were not edited.
No full gate or actual repeated-launch ABI test was run.

The bounded document self-check also passed: Muse's §7.3 paragraph and the
accepted 4ht statement match verbatim, §10 has the scoped lifetime phrase,
the citation is corrected, all four spec insertions apply at their stated
anchors in an in-memory dry run, fences balance and all six links resolve.

## Additional conformance obligations

At publication, suite G must exercise the **actual** two-launch sequences
above, comparing complete memory/table/bump, ledger and device state,
token validity and run-associated tapes. An executed `qreg.from_id` of
another open run's register produces terminal fault code 4; supplying that
register as a conflicting host launch argument returns `E_INVALID_STATE`
before effects. After A is CLOSED, its stored live id can be recovered by
`qreg.from_id` in B. A device-minted token passed after A is CLOSED returns
`E_ARG`; a host-minted token remains valid until unload. Separate loaded
instances have separate state. A native host invoking a retained device
instance must also check that device reversal leaves unrelated host state
unchanged. These vectors are requirements, not tests claimed to have run
through the current one-shot interpreter.

## Round-2 blocking items and resolution

The [round-2 report](../../../../bennett/docs/council/contract-adg-2026-11-02/round-2/report.md)
and both reviewer outputs agree on the device-ownership defect. This
revision adopts the complete launch-time rule verbatim from sol's
adg-R2-B1 fix, which also resolves codex's adg-R2-1. These are proposed
resolutions pending round 3 and a Muse seat.

| Item | Resolution and witness |
|---|---|
| adg-R2-1 / adg-R2-B1 | §§7.3/10 exclusively acquire every referenced console/clock/block model atomically at launch through CLOSED, including COMPLETED, FAILED and REVERSED. Conflict returns E_INVALID_STATE before effects or any acquisition. The clock/console overlap now blocks B before A reverses, preserving A's entry state. |
| T4 interaction | §14.3 restores run-owned state; disjoint runs' state is unaffected. The clock-only/console-only concurrent witness exercises this distinction. |
| Required §15 vectors | Both clock and console retry outcomes, block presence, FAILED/REVERSED retention, transitive helper footprint, no partial acquisition and independent entropy/tapes are specified. |

All other round-2 content is retained, including the exact Muse adg-M1
paragraph, accepted bennett-4ht paragraph, memory/allocator/token rules,
sequential device vectors and interpreter witness source. Only the
ownership/T4/vector additions, their necessary explanatory wording and
job-local reproduction paths change. No unrelated suggestion is applied.

## Muse blocking items and resolution

| Review item | Resolution in this proposal | Evidence / remaining validation |
|---|---|---|
| **adg-M1 (core), §7.3 lifetime missing** | Add Muse's paragraph verbatim after the device table: console/clock/block established at load and persistent; `p=0` and effect tape per run. | Concrete two-launch vector: B clock 1 / sector a5 without A reversal; clock 0 / absent sector 2 and 512 zero bytes with reversal. Real interpreter effects and complete reversal are checked by the bounded witness; actual multi-launch API conformance remains to implement. |
| **adg-M1 (core), §10 initialization too broad** | Replace the original unqualified phrase with “the §7.1/§7.3 program-lifetime state is never reinitialised merely to start a run”. | B's new one-byte tape `[33]` always yields `33` at `p=0`, and B owns exactly three effects. The within-run harness explicitly retains its cursor, distinguishing run boundaries from calls. |
| **adg-M1 required conformance vectors** | Add the clock/block vectors to §15 suite G, including reversal, FAILED-prefix retention, present-zero versus absent sectors, console and independent entropy/tapes. | Exact full byte patterns and state transitions are specified above; no lifecycle implementation pass is inferred from a scalar assignment or one-shot execution. |
| **adg-4HT-1, previously resolved** | Preserve the accepted paragraph verbatim in “Hashes, catalog and consumers”; extend the same instance scope to the new devices. | Native host binary, marked device modules, later-entry replay and unrelated host state remain separated as in the accepted re-check and shared scope. |
| **Round-1 citation correction** | Attribute program scope to §3.3; §3.2 only lists machine state. | Corrected in the defect paragraph and the complete spec diff. |

Muse's `suggestions` array is empty; its report's S1/S2 items address
z4c, 5u3 or checker-diagnostics, not adg. There is no unaddressed adg S1.
The source is
[out-muse.json](../../../../bennett/docs/council/accept-muse-batch-2026-11-02/round-1/out-muse.json)
and its [report](../../../../bennett/docs/council/accept-muse-batch-2026-11-02/round-1/report.md).
Round-1 optional refinements are also retained here: explicit T4 quantum
qualifications, full scalar table states, free/table-capacity boundary,
token/ownership distinctions and the in-version hash condition.

## Release and after acceptance

Recommend a **0.9 K wording repair to §§7.1, 7.3 and 10**, with the §15
lifecycle vectors. The core change must return to sol and astra and then a
later Muse seat, as the convenor requires. Once accepted and authorized,
the spec editor assigns the K number, applies the complete additions plus
the accepted 4ht statement, and regenerates the relevant indexes/diffs.
Reference/VM owners then implement and test repeated-launch lifetimes;
the dialect updates its cross-reference. Keep `b-isa-spec-adg` open until
the contract decision and its required follow-through land. `bennett-4ht`
continues to track the mixed-launch boundary. No full gates, spec edits,
interpreter changes, commits or remote operations are part of this job.

## Ownership revision verification and council follow-through

`timeout 30s python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/check_notes.py adg`
checks the exact reviewer wording, preserved adg-M1/4ht bytes, T4 and
§15 insertions, complete original Rust witness and links. The finite
ownership model command is
`timeout 30s python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/ownership_witness.py`.
Both exited 0. The job-local interpreter build reproduced the five
recorded stdout lines with complete machine-snapshot restoration; see
`timeout 300s python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/run_witnesses.py`.
The interpreter has no multi-launch ownership API, so the overlap rule
has finite-model evidence and required suite G vectors, not an actual
multi-launch implementation pass. No full repository gate was run.

Open council work is acceptance of the launch-time ownership rule in
adg round 3, then a Muse seat; publication and actual ABI conformance
follow. The existing adg and bennett-4ht obligations remain open. This
revision makes no new contract choice beyond the reviewers' requested
ownership repair and reserves no K number.

---

## Dossier part: pe1 (RE-SEAT. run derive3-pe1-2026-11-02; accepted by sol, codex (astra) in round 1; your batch-2 seat (accept-muse-batch2-2026-11-02 round 1) blocked it on pe1-M1 (the §0.2 K67 ledger row still says 25-bit / 1/33554432); this revision adds exactly your pe1-M1 replacement text and nothing else; convenor ruling: no further sol+astra round because the change is your verbatim text; amends the Bennett ISA (spec/Bennett-ISA-Spec-0.9.md); source note bennett-isa-spec/docs/notes/2026-11-03-notefix/pe1.md)

# b-isa-spec-pe1 — K13's extra borrowed bit

Council proposal; published text and fixtures are unchanged. References:
[ISA 0.9](../../../spec/Bennett-ISA-Spec-0.9.md) §§4.2–4.3, 5.6,
12.1 “CLAIM-REPLAY witness”, 12.2 “Component resolution (K69/K70)”.

## Exact defect and North Star scope

The §12.1 subject is exactly the two-row oracle `r = lift.add x a;
lift.retval r`, with no inherited controls and an unused interface
region. The printed tuples nevertheless contain `borrowed:["1"]`,
the widths include `borrowed:[1]`, and the prose counts a 25-bit D and
coverage `1/33554432`. The lifted opcode set in §4.2 supplies no qborrow
instruction. This subject has no checked dirty-bundle lifetime.
§12.2 K70 expressly rejects a borrowed position beyond the checked
borrow requirement. The example cannot pass the rule it illustrates.

This is an inconsistent normative example, **not a missing borrow
capability** or a reason to relax K70. §4.3/§5.6 already supplies dirty
allocation and borrowed-system preservation where applicable. North
Star §§3.1, 4.2, 5.1 remains reachable, including dirty ancillae and
entanglement with an external reference. Correct the example rather
than adding a fictitious oracle input component.

## Alternatives and concrete witnesses

For x=1, a=2, target=2, fault=3, cells=[2,1], B=2, the two rows return
payload 3 and fault code 0. The resulting complete tuple is
`bundles:["1","1","3"], borrowed:[], regions:[["2","1"]]`.
The full basis domain has 2+2+4+16 = 24 bits. A singleton declared
domain, sampled four times with replacement, covers one of 2^24 full
tuples and remains evidence. Singleton ranges consume no random words.

Changing a to 1 changes target to 0. Reducing B to 1 changes the payload
to 0 and the final fault word to 3 XOR 1 = 2. An identity expected row
fails. Dropping the borrowed coordinate changes none of these results.
An invented one-bit coordinate must still reject under K70, even if
the table preserves it perfectly or calls it the same name as a real
interface bundle.

| Alternative | Assessment |
|---|---|
| Remove the extra borrowed coordinate and adjust D/fraction | Repairs the example without changing any machine/domain rule. Recommended. |
| Replace the subject by a checked borrowing action wrapper | Possible new example, but needs its actual body, frame, lifetimes and new domains; the printed two-row oracle cannot stand in for it. |
| Invent oracle borrowed inputs or infer them from unused labels | Changes the oracle ABI and breaks K70 positional resolution; unjustified. |
| Count a lift.perm_call callee's internal scratch as this oracle's borrowed interface | Needs a separate lifetime/tuple contract; no such call exists in this witness. |

## Recommended exact spec diff

Within the single §12.1 CLAIM-REPLAY witness JSON block, replace **all
six** tuple occurrences of `"borrowed":["1"]` by `"borrowed":[]`,
and make these additional replacements:

```diff
-  "widths":{"bundles":[2,2,4],"borrowed":[1],"regions":[[8,8]]},
+  "widths":{"bundles":[2,2,4],"borrowed":[],"regions":[[8,8]]},
-  "sample_count":4,"distinct_samples":1,"covered_fraction":"1/33554432","verdict":"evidence"
+  "sample_count":4,"distinct_samples":1,"covered_fraction":"1/16777216","verdict":"evidence"
```

Replace the indicated prose immediately below that block:

```diff
-with a preserved one-bit dirty bundle and an unused two-cell,
-eight-bit `in` interface region; no inherited controls.
+with an unused two-cell, eight-bit `in` interface region; no borrowed
+lifetimes and no inherited controls.
-full 25-bit D (2+2+4+1+16 bits).
+full 24-bit D (2+2+4+16 bits).
-words and cover one of 33554432 full tuples.
+words and cover one of 16777216 full tuples.
```

Append to that witness paragraph:

```text
The empty borrowed array is required here: the two-row oracle has no
checked borrow lifetime. Adding a borrowed coordinate to this witness
rejects under K70; unchanged borrowed contents alone do not establish
that a lifetime exists.
```

The replacements operate on the exact phrases across line wrapping;
do not change the separate general tuple encoding, sampler, layout,
arguments, target/fault widths or K70 rule.

## Hashes, catalog and consumers

The witness deliberately supplies no bound object/closure hashes, so
there are no printed subject digests to recompute. No source instruction,
interface or ref catalog changes. Any concrete certificate/table fixture
based on the invalid example must change its tuple/domain bytes and
coverage report; a certificate digest consequently changes. Consumers
following K70 already reject the old example. Do not change their
component resolver or call the repair a proof over dirty inputs.

## Conformance vectors and actual verification

The read-only replay suite's `tests.test_replay.K13Witness` has four
focused tests using the repaired empty-borrowed relation, including the
changed argument, short budget, wrong row and missing-cell cases.
Ran it together with `QinplaceCoverage` using the bounded command in
[INDEX](INDEX.md): all 12 tests passed, exit 0. The replay fixture uses
ptr_width=32 rather than the printed legal 2-bit layout, so this run
checks the relation/domain behavior, not literal byte reproduction of
that layout. It is also an exhaustive singleton-slice test, not the
printed four-draw sampled packet. The finite INDEX checks independently
check the bit count, all six tuple repairs and sampling calculation.

For acceptance publish a complete bound certificate for the repaired
2-bit-layout oracle, with the exact four-draw sampler and all region
cells. Expect evidence `1/16777216`; reject the extra borrowed position,
unchanged-argument/budget rebinding, identity row and omitted cell.
Retain a separate genuine qborrow action with an entangled external
reference to test dirty preservation; it must not be folded into this
oracle's D. A small example fix does not discharge suite C's full-D T3.

## K entry and publication route

Recommend a **0.9 K13 witness erratum**, not a new oracle ABI or 0.10
deferral. Proposed decision row: `K13 erratum | §12.1 | remove nonexistent
borrowed coordinate; D=2^24, coverage=1/16777216 | pe1 | example repair`.
Council assigns any new ledger number; this proposal reserves none.
The semantic rule already belongs to accepted K70. Keep pe1 open until
the editor and conformance owners publish the repair.

## Mixed fat object

Apply [fat-object-scope.md](../2026-11-02-rev2/fat-object-scope.md) and
North Star §§2, 3.3, 4.4. This tuple belongs to one embedded device
subject and its selected root. A native host or another marked module
does not contribute a borrowed coordinate, interface cell or certificate
record to this subject. No container, launch, budget, handle or tape
change is needed; the shared note's explicit mixed-launch association
work remains. The native binary need not become an oracle to repair K13.

## Muse blocking items and resolution

**pe1-M1 — §0.2 K67 ledger row.** This revision adds exactly one
spec edit to the original proposal: replace K67's witness sentence in
the same erratum as the existing §12.1 repair. Nothing else changes;
every byte of the original note above is retained. This is a proposed
resolution, pending the Muse re-seat or the convenor's ruling that the
verbatim replacement suffices; it is not a new acceptance verdict.

The replacement text copied verbatim from
[Muse pe1-M1](../../../../bennett/docs/council/accept-muse-batch2-2026-11-02/round-1/out-muse.json)
is:

```text
LEGAL-REPLAY-WITNESS. F=4 and W=8 with legal unused mapping give a 24-bit domain; witness: four singleton draws cover 1/16777216 with unchanged XOR outcomes.
```

Checked against the current published §0.2 K67 row at **line 203**, the
line cited by Muse. These are the complete before/after UTF-8 row bytes,
excluding the terminating LF; retain all other columns and dependency
markers. The old bold label becomes the exact plain label Muse supplied.

```diff
-| K67 | §12.1 | **LEGAL-REPLAY-WITNESS**. F=4 and W=8 with legal unused mapping give a 25-bit domain; witness: four singleton draws cover 1/33554432 with unchanged XOR outcomes. [deps: ISA-5.4, ISA-7.1, ISA-7.2, ISA-12.1-P8, ISA-12.2] | COD S03 | E | – |
+| K67 | §12.1 | LEGAL-REPLAY-WITNESS. F=4 and W=8 with legal unused mapping give a 24-bit domain; witness: four singleton draws cover 1/16777216 with unchanged XOR outcomes. [deps: ISA-5.4, ISA-7.1, ISA-7.2, ISA-12.1-P8, ISA-12.2] | COD S03 | E | – |
```

Before row SHA-256: `ad71cdb6cdfbf9b2b56b0aeaa9f65dea6173df80d92cd208f9fac94152a552c3`.
After row SHA-256: `c020b85859bb1ade45b2d47ad24c956a791b85d9372ed08d50b5338267fb8a5b`.
The numeric substitutions are ASCII `25-bit` → `24-bit` and
`1/33554432` → `1/16777216`; the XOR outcomes are unchanged.

The focused check applies the original §12.1 edits and this new row edit
to an in-memory copy of the published text. It checks all six tuple
repairs, empty borrowed widths, the 24-bit count and singleton fraction,
and requires no remaining `25-bit` or `33554432` occurrence in that copy.
The on-disk spec is unchanged. The four draws of the singleton consume
no random words and have one distinct tuple. This does not publish the
complete bound 2-bit-layout certificate requested by the original note;
that remains a conformance publication obligation.

Verification: `timeout 30s python3 -I -B /home/tobias/Projects/bennett-workspace/bennett-isa-spec/.tmp/sol-notefix-s4/check_notes.py pe1`
exited 0 with the pe1 PASS line. The inherited `INDEX.md` references
above refer to [the originating INDEX](../2026-11-02-derive3/INDEX.md);
the original note's historical test report is retained, not reclassified
as a fresh interpreter or full-repository test.

---

## Appendix: shared scoping statement fat-object-scope.md (verbatim)

# Mixed fat object — shared contract scope

Proposal for every revision in this directory; not a published ISA amendment.
Clause references are to [ISA 0.9](../../../spec/Bennett-ISA-Spec-0.9.md),
[the North Star](../../../../bennett/docs/Bennett-NorthStar.md), and, where
qualified, the maintained dialect 0.2/0.3 texts. This is the shared statement
required by bennett-4ht and the council rubric's standing mixed-fat-object check.

## Citable scoping statement

> A mixed fat object retains an ordinary native host binary and embeds ISA
> objects for marked device modules and their linked device closures (North
> Star §§2, 3.3, 4.4). ISA §§9.1–9.3 identify each device object and selected
> root; §12.3 certificates, owner records and reports cover that closure,
> with a separate binding/context set per device root and [] relative to
> that root (§12.1). Native entry, argv/envp and host-only libc need no ISA
> region, frame or certificate record; native comparison binds the selected
> materialised closure, not the whole host. Today §10 launches a device CC
> entry with copied arguments/entropy; §5.4 budgets bind device invocations,
> §3.3/§10 handles belong to a loaded program/run, and §7.3/§10 tapes cover
> device R effects. These require explicit container-to-object/root/certificate
> association, host-entry-to-device-entry bindings, budget/handle lifetime
> negotiation and tape/run association in a versioned mixed-launch contract.
> ISA §7.1 defines device memory but §10 defines no general host-memory-by-reference
> launch ABI: that contract must add address/layout mapping, range/liveness,
> aliasing, ownership/synchronisation, writeback and reversal rules, preserving
> dialect §§6.6, 8.5, 19.4–19.5. Until published, these are explicit
> bennett-4ht boundary obligations, not grounds to require whole-binary
> lowering or omit mixed execution.

## Present assumptions and exact publication changes

| Contract object | Assumption today | Exact change needed for mixed use |
|---|---|---|
| Object and linking (§§9.1–9.3) | One ISA object's closed sections and linked symbols; no native-container schema. | Publish a versioned inventory associating embedded/linked ISA object bytes and object_hash with selected device roots and certificates. A native-container hash, if used, is a separate identity. |
| Certificates/inventory (§§12.1–12.3) | Closure-keyed device-region records; current text does not explicitly delimit native inventory. | Insert the shared scoping rule in §12.3, cross-reference from §9.2, and require complete device-owner/link-proof coverage per root. Multiple device roots can share static closures without merging root-relative contexts. |
| Launch/entry (§10) | bennett_run(program, cc_entry, args, entropy) starts device CC; it is not native main. | Publish a host call/return shim and container/root selection/feature negotiation. Define native argument/result marshalling, including ptr (whose host binding §10 does not specify), status/fault propagation, suspend/reverse/close and ownership. Do not invent a current general launch shim. |
| Budgets (§5.4; §§10–11) | Validated token tuples and identity scoped to a program/run; action_call has no primary token (§4.7). | Bind selected device invocation budgets and token equality to the launch request; charge actual device/replay work. State host/shim accounting separately; a native process has no invented global B. |
| Handles (§3.3; §10; dialect §6.6) | Register ids refer to the loaded program's ledger; run ownership and token validity are explicit. | Map host-visible opaque handles to that program/ledger with validity and cross-launch ownership checks; preserve class vectors and token identities. Do not serialize native pointers as device ids or token tuples as identities. |
| Effect tape (§7.3; §10) | Run-associated R effects and explicit copied hostcall requests; no implicit log of native host I/O. | Associate each device run and tape with the launched root and define host effect/proxy ordering and replay at the boundary, preserving §7.4 reversal. Saved-journal interchange needs its own versioned replay profile. |
| Host memory by reference (§§7.1–7.2; dialect §§8.5, 17.1, 19.4–19.5) | Device layout plus dialect snapshot/replay and boundary-address/promotion rules; copied hostcall bytes do not provide general shared pointers. | Publish the mapping and lifetime protocol named in the statement, including allocator metadata/history and pointer-rich layouts, so ordinary host memory can be supplied safely without universal host promotion. Retain existing snapshot/replay as a construction, not the sole eventual capability. |

For example native main can call marked roots A and B in distinct ISA objects.
Each has its own object/root certificate and root context []; neither
certificate inventories main or host-only libc. A shared linked device
callee is checked in each root's actual invocation tree. A native comparison
executes the corresponding materialised region/callee closure under its
recorded layout, input and tool configuration (dialect §§17.7, 19.5, 19.9).

These notes specify boundary scope and exact remaining contract work; they
implement no container, host shim or memory registration. The existing
bennett-4ht issue tracks that publication/implementation obligation. Current
device contracts and their complete estimate/proof requirements remain in
force; an unimplemented boundary is not evidence that mixed execution works.
