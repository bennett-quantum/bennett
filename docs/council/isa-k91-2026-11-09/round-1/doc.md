# Graded document: ISA 0.9 K91 token-alias ABI feature clause (bennett-isa-spec job/b3ui-k91 ec81d8b, base f7cb01b)

Maintainer ruling (2026-11-08 19:21Z, item 1): b3ui = alternative A, published as a normative clause inside ISA 0.9 K91: two per-role feature-query exports; manifest schema bennett.abi-features/1; one shared identifier token_aliases/1 with role-specific obligations; the driver owns the shim path and the runtimes the native layout under the existing 4ht obligations; the VM advertises nothing until its alias-aware estimate works (advertising is a conformance condition; the capability stays promised).

Prior review round (not council): astra ACCEPT; sol P1 (cross-provider hash invariance vs §9.2/§11) fixed in ec81d8b.

## Diff of spec/ (f7cb01b..ec81d8b)
```diff
diff --git a/spec/Bennett-ISA-Spec-0.9.md b/spec/Bennett-ISA-Spec-0.9.md
index c2cf36f..bda5b1a 100644
--- a/spec/Bennett-ISA-Spec-0.9.md
+++ b/spec/Bennett-ISA-Spec-0.9.md
@@ -251,7 +251,7 @@ north star §3.1 requires).
 | K88 | §3.2–§3.3, §7.4, §9.4, §10, §12.3 | **4TA**. Ordered per-wire register class vectors, reversible heterogeneous concat/slice and canonical B5 slot fragments preserve one source slot. S1: all ledger references, atomic class/placement preflight, failed-view reversal, upgraded readers and zero-width runtime vectors binding no slot. Certificate bytes change; unchanged source/signature/closure/object, target, schedule, ref recipes/ordinals/catalog identities. | 4ta; council pass2-4ta-2026-11-02 round 2; Muse accept-muse-batch2-2026-11-02 round 1; in-version 0.9 K, maintainer D2 2026-11-03 | S | – |
 | K89 | §12.1–§12.3 | **7S0**. Selected maximal borrow_frame relations, workspace entry components and entry_products express existing K76/K78 D_F without changing it; union-rank sampling and B-fiber checks fix coverage. S1: K69 positional inherited controls, evidence versus requested-proof rejection, causal-stack/seed witnesses and Cartesian sampler cross-reference. Certificate bytes change; source/closure/object, target/schedule leaves, K78 and ref catalog identities stay unchanged. | 7s0; council pass2-7s0-2026-11-02 round 2; Muse accept-muse-batch2-2026-11-02 round 1; in-version 0.9 K, maintainer D2 2026-11-03 | S | – |
 | K90 | §12.3 | **V2V**. Exclusive uniform frame or complete canonical frame_contexts, validated against each resolved invocation and its allocation/lifetime metadata. S1: pair/two-root/singleton fixtures, truthful legacy migration and checked scope uniformity. Certificate bytes change; no callee clone, source/interface/closure/object, target/schedule, call edge or ref catalog identity change. Narrow reading: future fault-context arrays are not presumed; existing published context obligations stand. | v2v; council pass2-v2v-2026-11-02 round 2; Muse accept-muse-batch2-2026-11-02 round 1; in-version 0.9 K, maintainer D2 2026-11-03 | S | – |
-| K91 | §5.4, §7.4, §10.1, §11, §12.3 | **YSW**. Canonical token_aliases equality partitions preserve actual identities through calls, source builders and reversal; only oracle invocations prepend a primary token. S1: universal partition encoding, schedule matching/history, identity-call carrier and self-adjoint wording. Additive launch/sched token_aliases/1 feature with explicit loader negotiation, preserving legacy symbols; legacy token-argument requests need an alias binding. Alias-bearing schedule/certificate hashes change; args/params_hash, source/interface/closure/object and ref catalog identities stay fixed under unchanged envelopes. Narrow choice: versioned ABI feature rather than a header-version bump. Editor's note (advisor R21, 2026-11-03): the loader capability negotiation this row invokes (feature-query entry point, defined absent-feature behaviour, version field) is not yet defined in 0.9 text; it is pending b-isa-spec-b3ui (note, sol+astra round, editorial completion of K91). Do not implement against an undefined negotiation. | ysw; council pass2-ysw-2026-11-02 round 2; Muse accept-muse-batch2-2026-11-02 round 1; in-version 0.9 K, maintainer D2 2026-11-03 | S | +schedule/certificate bytes |
+| K91 | §5.4, §7.4, §10.1, §11, §12.3 | **YSW**. Canonical token_aliases equality partitions preserve actual identities through calls, source builders and reversal; only oracle invocations prepend a primary token. S1: universal partition encoding, schedule matching/history, identity-call carrier and self-adjoint wording. Additive launch/sched token_aliases/1 feature negotiated independently per role through bennett_launch_features / bennett_sched_features and bennett.abi-features/1 manifests (§10.1), preserving legacy symbols; legacy token-argument requests need an alias binding. Missing or inconsistent support gives a pre-request BENNETT_E_VERSION loader diagnostic. Alias-bearing schedule/certificate hashes change; negotiation adds no artifact fields or hashes, and args/params_hash, source/interface/closure/object and ref catalog identities stay fixed under unchanged envelopes. Narrow choice: versioned ABI feature rather than a header-version bump. | ysw; council pass2-ysw-2026-11-02 round 2; Muse accept-muse-batch2-2026-11-02 round 1; in-version 0.9 K, maintainer D2 2026-11-03 | S | +schedule/certificate bytes |
 | K92 | §4.5, §12.3 | **2QC**. QINPLACE-CHECKER-COVERAGE: owner-local exact pair presence and all reached bound transitive contexts, explicit unestablished applicability outcome, executor pre-effect coverage retained. S1: correct insertion before CLAIM-BINDING, literal reference-Q traversal including disabled predicates/zero-trip distinction and nested fixture. Compatibility: incorrect executable packets now reject or remain incomplete; correcting missing entries changes certificate bytes/digests. No executor/source/interface/closure/object, target/schedule, expansion or ref catalog identity changes. Narrow reading: owner-local requirements follow existing §4.5 and this K only; held 0jq is not presumed. | 2qc; council derive3-2qc-2026-11-02 round 1; Muse accept-muse-batch2-2026-11-02 round 1; in-version 0.9 K, maintainer D2 2026-11-03 | S | – |
 | K93 | §3.3, §4.4, §11.1, §15 | **SQR**. MCX-BUNDLE-CONTROLS: ordered bundle expansion, wire distinctness, flattened k and scalar target. S1: mixed-list order/arity, phase-sensitive external-reference witness, wire[1] target and active-predicate count. Route taken: in-version 0.9 K by maintainer D2 explicitly naming sqr (Muse sqr-S1); witness object/interface/closure hashes unchanged. Existing ref recipes/catalog bytes stay unchanged; wrong-arity adapter leaf hashes, schedules and cached execution/validation require regeneration and certificates rechecking. | sqr; council derive3-sqr-2026-11-02 round 1; Muse accept-muse-batch2-2026-11-02 round 1; in-version 0.9 K, maintainer D2 2026-11-03 | S | – |
 | K94 | §12.1, §16.3 example 3 | **ADJOINT-TABLE-PREMISES**. Defines the reference-action adjoint theorem, full-D/control scope, optional conjunctive subclaims and decidable syntactic premises; distinguishes established proof, named unchecked premises and malformed/refuted rejection. Compatibility: formerly Unverified adjoint_table claims become established or rejected when checkable; unavailable premises remain Unverified. No grammar or envelope changes: unchanged source/interface/closure/object, target/schedule/certificate and ref recipe/catalog bytes and hashes stay fixed; checker verdicts and validation caches require rechecking. Narrow reading: generated adjoint, no self-adjointness or variant-name inference, no mandatory replay subclaim. | in-version 0.9 K, advisor R34 2026-11-07; council pending | S | – |
@@ -2592,21 +2592,140 @@ The 0.9 request carries the complete resolved parameter vector.
 
 **Token-alias ABI feature (K91).**
 
-Both `bennett_estimate_run_with_token_aliases` and `bennett_sched_request_set_token_aliases` copy and validate the JCS array. Keep the old ABI callable; with no
-token args infer [0] for an oracle and [] for an action/perm_action.
-A legacy request with token arguments and no alias binding returns E_ARG;
-the additive alias-aware function admits every consistent partition and
-provides exact estimates of each resolved request. A bound over partitions
-is not a K12 exact result. This request diagnostic does not make any valid
-program or alias pattern illegal, and does not replace implementing the
-full alias-aware capability. Publish
-the extension under an explicit launch/sched ABI revision or feature
-contract, including loader capability negotiation; do not change the
-published C argument layout/symbol meaning silently.
+Launch and sched providers MUST copy and validate the JCS partition array
+at `bennett_estimate_run_with_token_aliases` and
+`bennett_sched_request_set_token_aliases`, respectively, according to
+§12.3. Both providers admit every consistent partition. The launch provider's
+alias-aware estimate is exact for the resolved request under K12; a bound
+over partitions is not an exact result. Invalid bindings return
+`BENNETT_E_ARG` before an estimate or effect. These request diagnostics
+do not make a valid program or partition illegal or replace implementing
+the full capability.
 
-The additive symbols and binding rules above define the launch/sched 0.9 feature `token_aliases/1`. Loader capability negotiation establishes support for both additive symbols and the token_aliases metadata contract before issuing an alias-aware request; symbol availability alone does not authorize silently dropping the partition. This feature retains the existing C argument layouts and symbol meanings.
+The shared feature identifier is `token_aliases/1`, with the role-specific
+obligations below. The following additive exports define its negotiation
+for launch/sched 0.9; neither takes a program or request handle:
 
-*Editor's note (advisor R21, 2026-11-03).* The loader capability negotiation named above (its query entry point, absent-feature behaviour and version field) is not yet defined by this draft; the text is pending b-isa-spec-b3ui and completes K91 editorially. Implementations MUST NOT invent a negotiation in the meantime.
+```c
+bennett_status bennett_launch_features(const uint8_t** jcs_out, size_t* len_out);
+bennett_status bennett_sched_features(const uint8_t** jcs_out, size_t* len_out);
+```
+
+**Query results.** On success, each provider MUST return `BENNETT_OK` with
+`*jcs_out` pointing to its immutable, provider-owned UTF-8/JCS manifest and
+`*len_out` equal to its byte length, excluding any NUL terminator. The bytes remain
+valid and unchanged until that provider is unloaded; the caller neither
+modifies nor frees them. Each provider MUST make repeated and concurrent
+queries return identical manifest bytes without changing program, request,
+run or device state; querying requires no program, target or run creation.
+Each provider MUST return `BENNETT_E_ARG` if either output pointer is NULL,
+without writing either output; otherwise any query failure with a non-OK
+status sets `*jcs_out=NULL` and `*len_out=0`. Callers MUST keep the selected
+provider loaded while querying, reading its manifest or using its resolved
+entry points, and discard cached pointers and advertisements at unload.
+
+**Manifest validation.** Each provider MUST encode its successful manifest
+with exactly three fields: `schema`, the string `"bennett.abi-features/1"`;
+`abi`, the string `"launch/0.9"` for the launch query or `"sched/0.9"` for
+the sched query; and `features`, a bytewise-sorted unique array of nonempty
+ASCII feature identifiers. An empty array advertises no extensions.
+The `abi` field identifies the C ABI family, independently of an object's
+header versions. The examples for providers supporting this feature are:
+
+```json
+{"abi":"launch/0.9","features":["token_aliases/1"],"schema":"bennett.abi-features/1"}
+```
+
+```json
+{"abi":"sched/0.9","features":["token_aliases/1"],"schema":"bennett.abi-features/1"}
+```
+
+The loader MUST compare `schema`, the selected role's `abi` and each
+required feature identifier by exact string equality. A feature version
+is part of its identifier: `token_aliases/2` alone does not establish
+`token_aliases/1`. Unknown feature identifiers may be ignored and confer
+no support for known identifiers; duplicate or unsorted entries, empty or
+non-ASCII identifiers, duplicate/unknown/missing fields, wrong field types,
+invalid UTF-8 or non-JCS bytes are malformed manifests, not empty lists.
+
+**Role obligations.** A provider advertising `token_aliases/1` MUST
+implement its declared base C ABI and the following applicable obligations:
+
+| Advertised role | Required entry point and behavior |
+|---|---|
+| `launch/0.9` | `bennett_estimate_run_with_token_aliases`; exact resolved estimates (§10.1), live-handle identity and reversal (§5.4, §7.4), and partition-sensitive schedule, certificate and source-binding metadata (§11, §12.3) on its launch/estimate paths |
+| `sched/0.9` | `bennett_sched_request_set_token_aliases` and `bennett_sched_schedule`; partition validation and preservation in requests, schedule selection/production and certificate bindings (§11, §12.3) |
+
+Neither role requires the other role's exports in the same library.
+An unavailable-estimate stub does not meet the launch pledge: a VM or
+other launch provider MUST omit `token_aliases/1` until its alias-aware
+estimate and the other launch obligations work. For a VM, this condition
+applies to each role manifest it exposes: its feature lists remain empty
+until its alias-aware estimate works. A sched provider MUST
+omit it while its required scheduling/metadata mechanics remain
+unimplemented. Ordinary specified argument and feasibility errors remain
+distinct from missing mechanics; withholding an advertisement does not
+discharge the promised capability or permit rejecting a valid source
+program or consistent partition.
+
+**Loader behavior.** Before any alias-aware request, the loader MUST
+resolve the applicable query on the selected provider, validate its
+manifest, find `token_aliases/1` and resolve the role's required entry
+points in that same provider. The loader MUST negotiate each participating
+launch/sched provider independently; one role's advertisement is no evidence
+for another provider or for an independent checker or metadata reader.
+Independent checkers and schedule/certificate readers MUST implement and
+validate the applicable K91 bindings before using alias-bearing artifacts;
+the launch/sched manifests do not attest to those independent consumers.
+
+The loader MUST report a compatibility diagnostic corresponding to
+`BENNETT_E_VERSION` before any alias-aware request or effect for a missing
+query, missing feature, unsupported schema or base ABI, malformed manifest,
+or advertisement whose required entry point is missing. A missing symbol
+cannot return a C status: the loader synthesizes this diagnostic; a static
+link requiring an absent symbol fails explicitly at link time. On a query
+failure the loader MUST propagate its non-OK status and stop negotiation
+without retrying the request. On either failure path the loader MUST retain
+the unresolved request and its partition, require a conforming provider,
+and issue no alias-aware work, partition-erasing legacy retry or successful
+estimate. Deployment incompatibility is not an illegal program/partition;
+a cross-partition bound is never substituted as an exact estimate.
+
+**Legacy compatibility.** Providers MUST retain the published C layouts
+and symbol meanings of their declared ABI family and keep its legacy
+entry points callable. For tuple-only requests with no token arguments,
+launch/sched providers MUST retain inference of `[0]` for an oracle and
+`[]` for an action/perm_action; a legacy request with token arguments and
+no alias binding returns `BENNETT_E_ARG`. Live-handle execution still
+derives actual identities under §12.3. A loader using a token-free legacy
+path MUST independently establish its base C ABI before dispatch; symbol
+names or object header `0.9` alone do not establish it. In particular a
+0.8 estimate signature is never called as 0.9, and old callers retain
+their actual ABI family. Neither a query nor feature absence changes this.
+
+**Mixed launch.** The driver owns negotiation in the actual startup/shim
+path for each selected marked device object/root; the runtimes own the
+native layout and its preservation at that boundary. The driver and
+runtimes MUST preserve that root's object/closure association, valid
+handle lifetimes and token equality mapping through the shim, under the
+existing §12.3 mixed-launch boundary obligations. Native entry points,
+argv/envp and host-only libc require no device alias records or whole-binary
+lowering. This query contract leaves the mixed-container/host-memory ABI,
+budget/handle and tape/run association work named in §12.3 required; it
+does not equate a native layout version with a launch/sched feature.
+
+**Artifact identity.** Negotiation is provider-local deployment metadata;
+it adds no field to objects, schedules or certificates and records no
+negotiated feature list there. Producers and readers MUST retain the K91
+partition in schedule/certificate bindings, proof scope and cache matching
+(§11, §12.3); no process-local handle or manifest pointer is serialized.
+Changing alias-bearing artifact bytes changes their hashes as before.
+Querying adds no artifact fields or hashes, and selecting a provider to
+consume unchanged artifacts does not rewrite them. Regenerating schedules
+or certificates with a different scheduler identity or scheduling decisions
+follows the existing binding and hash rules of §§9.2, 10.1 and 11.
+With unchanged envelopes, args/params_hash, source/interface/closure/object
+and ref catalog identities remain unchanged.
 
 **Resolved request.** `bennett_estimate_run` MUST copy and
 validate `params_jcs`, the JCS array of **all** classical arguments in
@@ -5026,6 +5145,82 @@ The vectors record source admission, complete output tuples and expanded source
 | G | Launch | every §10 entry point, state transition, binding rule, ownership rule; HOST_REQUEST/reply (a reply whose length does not fit `ptr_width` bits is `E_ARG`); reverse eligibility and tree order; `QREG` bound to `qreg[*]`; `FAILED → REVERSED` (example 8) and `E_NOT_REVERSIBLE` after a `measure` or an unverified free; exactly one fault record per `FAILED` run; an R `fault C` returns `OK` from `bennett_wait` with a result and no request, zero values and the exact nonzero 64-bit C (including 2^64 − 1) from `bennett_result_fault(result, 0)`; a device-minted token used after its run is CLOSED is `E_ARG` |
 | H | Scheduler | §6 validity; capacity; reproducibility; specificity resolution; verbatim execution; INFEASIBLE/UNSUPPORTED; invocation contexts covering default-only invocations (an action calling one region twice, one call scheduled explicitly: a claim with one witness rejects, two passing witnesses accept); a device-minted tuple binds the schedule (a schedule bound to B = 3 is not applied to an invocation minted with B = 2, which runs under the defaults) |
 
+**Loader-capability conformance (K91; suites G/H).**
+
+1. **Query ownership and state.** For each role, compare the exact manifest
+   bytes and byte length on repeated and concurrent successful queries,
+   including queries before any program/request creation. Read them after
+   unrelated program/request frees while the provider remains loaded; the
+   caller never frees the buffer. Observe unchanged program, request, run
+   and device state. With either output pointer NULL observe
+   `BENNETT_E_ARG` and no output writes; inject a query failure with valid
+   outputs and observe NULL/0. Unload/reload invalidates the loader cache;
+   no old buffer or function pointer is reused.
+2. **Manifest grammar and versions.** Accept both exact §10.1 example
+   manifests and a role-correct empty `features` array as valid manifests;
+   an empty array still lacks the required feature. Reject invalid UTF-8,
+   non-JCS JSON, duplicate/unknown/missing fields, wrong types, empty or
+   non-ASCII identifiers and duplicate/unsorted features with loader
+   `BENNETT_E_VERSION`. Exercise unsupported schema/base ABI, the wrong
+   role's ABI and `token_aliases/2` without `/1`: none authorizes the
+   request. An unknown feature alongside `/1` leaves `/1` support intact.
+3. **Failure before dispatch.** Exercise a missing query with an additive
+   export present, a query advertising `/1` with its required export
+   absent, and a manifest without `/1`. Observe loader
+   `BENNETT_E_VERSION`, no request/effect and no legacy retry. For a query
+   failure, observe its original non-OK status and the same absence of
+   dispatch. Verify explicit static-link failure when a required symbol
+   is absent, and preservation of the unresolved request and partition
+   on all loader failures.
+4. **Independent roles and readers.** Use distinct launch/sched providers
+   with support present on only one, then support on both. Only the
+   independently validated roles permit their requests. A scheduler-only
+   provider needs no launch export, and conversely. A checker or artifact
+   reader without K91 binding support cannot consume alias-bearing output
+   by relying on either manifest; wrong-partition proof reuse rejects.
+5. **Truthful support and full partitions.** An unavailable alias-aware
+   estimator or unimplemented required scheduler/metadata path cannot
+   advertise `/1`; a VM's role manifests have empty feature lists until its
+   alias-aware estimate works. With support advertised, exercise all five partitions
+   `[0,0,0]`, `[0,0,1]`, `[0,1,0]`, `[0,1,1]`, `[0,1,2]` on three
+   equal-tuple token positions, for action arguments and oracle
+   primary/arguments. Compare exact estimates to independent aggregation
+   of each resolved realisation, not a bound over partitions. Exercise
+   forwarding/capture, repeated fresh mints of the same tuple and reversal:
+   live identities, history and revocation follow §5.4/§7.4/§12.3,
+   irrespective of the query result. Ordinary argument/feasibility errors
+   retain their specified statuses after successful negotiation.
+6. **Partition validation and copying.** `[1,1]`, `[0,2]`, negative labels,
+   wrong arity and equal labels with unequal tuples return
+   `BENNETT_E_ARG` before an estimate/effect. Mutate/free the caller's
+   partition buffer after a successful setter or estimate call; the
+   stored request or returned estimate retains the original binding.
+7. **Legacy ABI safety.** Old callers/new providers retain callable
+   signatures in their actual ABI family. Observe token-free oracle `[0]`
+   and action/perm_action `[]`, and `BENNETT_E_ARG` for tuple-only token
+   arguments without aliases. A new loader detects an unknown/mismatched
+   base ABI before any legacy call, even with matching symbol names or
+   an object header saying 0.9; a 0.8 estimate address is never dispatched
+   through the 0.9 signature.
+8. **Bindings and hashes.** Hold args and `params_hash` fixed and change
+   only the consistent partition: a mismatched bound schedule is not
+   applied (§11 defaults), a wrong-partition certificate rejects, and
+   cache keys distinguish the requests. Changed alias-bearing schedule
+   and certificate bytes change their hashes. Compare fixed input artifacts
+   before and after queries and consumption by another conforming provider:
+   no artifact bytes/hashes change and no manifest/feature-list fields are
+   inserted. Regenerated artifacts retain their actual scheduler identity
+   and scheduling decisions and are hashed under the existing rules;
+   provider substitution does not imply byte-identical production.
+   Unchanged source/header/catalog envelopes preserve their identities.
+9. **Mixed-object boundary.** Select two embedded device roots with
+   separate bindings; observe driver/shim negotiation against their
+   actual providers, object/closure associations and valid token-handle
+   equality/lifetimes across the runtime native layout boundary. No root
+   inherits another's alias binding. Native entry, argv/envp and host-only
+   libc need no fabricated device alias entries. A native layout version
+   alone cannot authorize an alias-aware launch/sched request.
+
 **Suite H / §11.1 K77 adapter vector.** Captured `oracle_invocation`
 follows the source call's arguments and body/template capture, irrespective
 of unrelated apply-site context; nested calls restore the enclosing context
diff --git a/spec/isa-0.9.PROGRESS.md b/spec/isa-0.9.PROGRESS.md
index 583ca3e..cad77d2 100644
--- a/spec/isa-0.9.PROGRESS.md
+++ b/spec/isa-0.9.PROGRESS.md
@@ -1,3 +1,30 @@
+## Resume — K91 loader-capability contract
+
+**Done.** §10.1's **Token-alias ABI feature (K91)** now specifies separate
+`bennett_launch_features` / `bennett_sched_features` queries, the
+`bennett.abi-features/1` manifest, exact role/version matching, ownership
+and concurrent-query behavior, and explicit pre-request failure.
+`token_aliases/1` has role-specific identity/metadata obligations; an
+incomplete VM advertises no features until its alias-aware estimate works.
+The K91 ledger matches the clause. §15 adds nine observable conformance
+groups. Driver/shim and runtime native-layout responsibilities retain the
+existing mixed-launch obligations. Negotiation adds no artifact fields.
+
+**Verified.** The job-local text-contract checker failed on the original
+placeholder and passes on the replacement, including seven corrupted-text
+checks, the role/observable audit of all 21 MUST statements and unchanged
+spec bytes outside the owned K91 portions. `python3 -I -B
+conformance/tools/ref_catalog.py --check` passes: 219 recipes and unchanged
+envelope `5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197`.
+`git diff --check` passes. These are publication checks, not executable
+provider conformance or a full gate.
+
+**Next.** Contract review/council and the single full gate remain with the
+orchestrator. Regenerate `spec/isa-0.8-to-0.9.diff` from the final text
+before that gate (bennett-isa-spec-zs2); it is outside this edit's owned
+paths. b-isa-spec-b3ui stays open for that review/publication disposition;
+b-isa-spec-8ui / b-isa-spec-8ui.1 retain interpreter/vector/header work.
+
 ## 2026-11-01 Pass XIII — round 9 acceptance and S1 tool/fixture follow-up
 
 **round 9: accepted**, codex seat, zero blocking. Passes XI–XII and
```

## Author rationale and MUST audit (.tmp/b3ui-k91/RATIONALE.md)
# K91 loader-capability rationale and self-check

Alternative A completes §10.1 inside ISA 0.9 as directed. One exact feature identifier has separate launch/sched pledges so a standalone scheduler need not ship a launch implementation. The schema version, role ABI and feature version are separate exact-match strings; an object header or additive symbol alone attests to none of them. New query declarations live in the shared K91 clause, keeping edits inside the owned clause rather than changing headers or unrelated ABI declarations.

The caller can query before creating any object. Immutable provider-owned bytes, lifetime through provider unload and identical concurrent replies avoid hidden handle state. Invalid output arguments have a defined no-write result; other failed queries clear valid outputs. Loader compatibility failures synthesize BENNETT_E_VERSION because a missing export cannot itself return a status. Query errors retain their original status. In neither case is a partition-erasing retry allowed. Known token-free legacy calls retain their actual ABI family.

An advertisement pledges implemented role semantics, including exact alias-aware estimates. Withholding an incomplete VM advertisement is an honesty condition, not a withdrawal of the promised capability. The driver owns the actual per-root shim negotiation; runtimes own native layout preservation under the existing mixed-launch obligations. No container or host-memory ABI is invented and no whole-binary lowering is required.

Negotiation is deployment metadata and adds no artifact fields. K91 partition/proof/cache bindings still carry semantic identity; only changes in those existing bytes change the corresponding hashes. Queries and consumption leave fixed input artifacts unchanged; regenerated schedules/certificates carry the actual scheduler identity and decisions and are hashed by §§9.2/10.1/11. Distinct conforming producers need not generate identical bytes. This preserves source, object and catalog envelopes and avoids an additional closed-schema migration.

## Every MUST: responsible role and observable

The following is an exhaustive, ordered inventory of the clause's 21 MUST occurrences. The scratch checker ties each occurrence to this inventory; the role/observable pairing was checked against the actual prose. Group numbers refer to the nine §15 K91 conformance items.

| # | Responsible role | Observable | §15 group |
|---|---|---|---|
| 1 | Launch/sched providers at their respective additive calls | Copied, validated partition; malformed or tuple-inconsistent bindings return E_ARG before work | 5, 6 |
| 2 | Query provider on success | OK, immutable owned UTF-8/JCS buffer, exact length without NUL, validity through provider unload | 1 |
| 3 | Query provider | Identical repeated/concurrent reply bytes; unchanged program/request/run/device state, no created program/target/run | 1 |
| 4 | Query provider on invalid outputs | E_ARG and neither output written if either is NULL; other failures clear valid outputs to NULL/0 | 1, 3 |
| 5 | Caller using the query/buffer/exports | Provider remains loaded; loader caches/pointers discarded at unload | 1 |
| 6 | Query provider on success | Exactly schema, abi and features with the defined types, role and canonical ordering | 2 |
| 7 | Loader | Exact schema/role-ABI/feature match; /2 never substitutes for /1 | 2 |
| 8 | Advertising provider in the specified role | Declared base ABI and complete tabled entry point/identity/metadata behavior | 4, 5, 7, 8 |
| 9 | VM/other launch provider with incomplete estimate/launch mechanics | No token_aliases/1 advertisement while required launch behavior is unimplemented; every exposed VM role has an empty feature list until its alias-aware estimate works | 5 |
| 10 | Sched provider with incomplete required mechanics | No token_aliases/1 advertisement while required scheduling/metadata behavior is unimplemented | 5 |
| 11 | Loader before an alias-aware request | Query, valid manifest, required feature and required exports resolved on the same selected provider | 2, 3 |
| 12 | Loader using multiple roles/providers | Each participating role checked independently; other providers/readers gain no inferred support | 4 |
| 13 | Independent checker and schedule/certificate reader | K91 binding validation before artifact use; wrong-partition proof reuse rejects | 4, 8 |
| 14 | Loader facing missing/inconsistent protocol support | E_VERSION diagnostic before alias-aware request/effect; missing-symbol diagnostic synthesized | 2, 3 |
| 15 | Loader facing a failed query | Original non-OK status propagated and no request retry | 1, 3 |
| 16 | Loader on either failure path | Unresolved request/partition retained; no alias-aware work, partition erasure or successful estimate | 3 |
| 17 | Provider for its declared base ABI | Existing C layouts/symbol meanings/legacy entry points remain callable | 7 |
| 18 | Launch/sched provider for a tuple-only legacy request | Token-free oracle [0], action/perm_action []; token arguments without aliases return E_ARG | 7 |
| 19 | Loader using a token-free legacy path | Independently established matching base ABI before dispatch; no 0.8-as-0.9 call | 7 |
| 20 | Driver and runtimes at the real per-root shim/layout boundary | Preserved object/closure association, valid handle lifetimes and token equality mapping | 9 |
| 21 | Artifact producers and readers | Partition retained in schedule/certificate bindings, proof scope and cache matching; no process-local handle serialization. Query/consumption invariance covers fixed input artifacts only; regenerated outputs keep actual scheduler identity/decisions and their hashes | 8, 9 |

## Evidence and handoff

`python3 -I -B .tmp/b3ui-k91/check_contract.py` failed on baseline f7cb01b with missing signatures/manifests/contract/conformance items (`contract-red.log`). The edited text passes with `--self-check`; nine deliberately broken texts are rejected, including regressions to provider-independent production invariance, and the checker asserts byte-identical non-owned spec text. The strengthened artifact-identity check failed on reviewed head 8541ad3 with five scope errors (revision-red.log) and passes after the two reviewed passages are clarified (revision-green.log). A schema/hash witness reproduces both review counterexample hashes from the published controlled-action fixture, differing only in scheduler name. These checks concern publication text and hashing only, not executable ABI conformance.

`python3 -I -B conformance/tools/ref_catalog.py --check` passes: 219 recipes, envelope 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. `git diff --check` passes.

The stable-label generated diff matched the baseline but needs refreshing after this edit. Its exact replacement is `.tmp/b3ui-k91/isa-0.8-to-0.9.diff`; published `spec/isa-0.8-to-0.9.diff` is outside ownership and unchanged. Follow-up bennett-isa-spec-zs2 asks the orchestrator to regenerate on final merged text before the single full gate. No full gate or full draft_witnesses.py run is claimed (the latter requires that generated artifact and interpreter binaries absent here). b-isa-spec-b3ui stays open for sol/astra review, council and gate; b-isa-spec-8ui and b-isa-spec-8ui.1 retain implementation/header ownership.
