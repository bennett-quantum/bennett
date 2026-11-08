# Loader capability negotiation — round-1 review

Reviewer: gpt-6.1-sol

Date (UTC): 2026-11-08T11:38:11Z

Reviewed commit: `c08116ba3a572fb41b3be860c66d810bfc3b2d0a`, branch `job/b3ui-note`.

Reviewed note: [Loader capability negotiation](../design/2026-11-08-loader-capability-negotiation.md).

Verify result: `python3 -I -B .tmp/b3ui-note/verify_note.py --self-check` — **PASS, exit 0**: 37 byte-exact quotations, 14 source files, six immutable repository pins, exact diff deletions, 224 note lines, six corruption controls rejected.

Started from the author's `.tmp/b3ui-note/PROGRESS.md`, brief and verifier. The author claims documentary verification only; no red-first implementation test, ABI execution or full-gate receipt is claimed or supplied. I read the verifier, reran its positive/negative checks, read the proposed text and independently inspected the cited contracts and current consumer code. No full repository/sibling gate was run, as T3CHILD requires.

P0/P1: **0**. P2: **0**. Nits: **0**. No new review beads are proposed.

## Numbered findings

1. **The stated defect is correct.** ISA 0.9 §10.1, `bennett-isa-spec/spec/Bennett-ISA-Spec-0.9.md:2594–2608`, requires every consistent partition, exact resolved estimates, preserved legacy layouts and explicit negotiation, but expressly leaves the query, absence behavior and version field undefined. The K91 row at `:254` repeats that warning. The §10/§11 declarations (`:2527–2585`, `:2723–2744`) contain no negotiation operation; the status enumerator alone provides none. The accepted ysw text, `bennett/docs/council/pass2-ysw-2026-11-02/round-2/doc.md:128–131,185–186`, requires publication and explicit old/new compatibility without choosing a mechanism. Note lines 3–8, 80 and 94–104 accurately distinguish this defect from symbol discovery and object-header validation. No contract quotation is misrepresented.

2. **All three alternatives retain K91's domain and compatibility obligations.** The shared rules at note lines 96–104 apply to A, B and C. Here old/new means before/after the proposed negotiation within launch/sched 0.9; 0.8 is a separate C ABI family. The four combinations have the following consequences:

   | Caller / library | Required behavior in A, B and C |
   |---|---|
   | Old / old | Existing actual-ABI behavior remains the baseline; lack of negotiation proves no new support. K91 legacy tuple-only requests with token arguments need an explicit binding or return `E_ARG`; token-free oracle/action inference is `[0]`/`[]`. |
   | Old / new | Existing constructors and actual C layouts remain callable with those same legacy rules; live-handle execution still derives actual identities. New negotiation is not imposed retroactively on old callers. |
   | New / old | Missing query/constructor yields a pre-request loader incompatibility diagnostic, or explicit static-link failure. Keep the unresolved partition; never retry after removing it or present a bound as exact. |
   | New / new | A requires a validated role manifest and the additive symbol from the same provider; B requires successful revision-1/bit-0 construction; C requires the feature as a required sidecar entry. Successful support includes the role's full identity/metadata semantics and every consistent partition. |

   A's role-scoped pledge and independent provider/reader checks (note `:124–140`) prevent a launch export from blessing an unsupported scheduler. B binds requirements per handle and preserves existing constructors (`:144–159`); refusing a new handle's unrequested feature does not outlaw any partition, because the caller can request bit 0. C makes `token_aliases/1` mandatory when depended upon and infers that requirement for existing alias-bearing artifacts without the table (`:163–177`); optional or missing metadata cannot license erasure. The old/old and old/new legacy `E_ARG` cells are the request diagnostic explicitly required by ISA `:2594–2600`, not a claim that alias-unaware callers implement the complete capability.

   These rules agree with §5.4's forwarding, fresh-mint lifetime and exact schedule matching (`:1353–1358,1373–1397`), §7.4's reversal identity record (`:1780–1781`), and §12.3's universal partitions, context propagation and proof/cache binding (`:4707–4752`). No alternative interns equal tuples, substitutes an outer token/bound, discards a partition or treats deployment absence as source illegality. The five three-slot partitions in note `:196` are complete.

3. **The proposed diffs are appropriately additive and do not conflict with existing status meanings.** The common replacement (`note:108–120`) is expressly unapplied and conditional on acceptance/publication (`:106`); it does not remove today's warning by itself. A adds two query declarations and their manifest contract; B adds one shared descriptor and two constructors; C adds two sidecar constructors and an explicit optional metadata field. Existing published signatures are preserved. C's larger closed-schema migration is disclosed rather than presented as an ignorable extension: ISA §9.1 (`:2139–2141,2168–2169`), the schedule schema (`:2769–2779`) and §12.3 (`:4751–4752`) require upgraded readers and changed artifact hashes. It is a cost of that alternative, not work concealed by the recommendation.

   The new `BENNETT_E_VERSION` uses concern negotiation/ABI support before an alias-aware request. The loader synthesizes that diagnostic when no callable symbol exists; the note does not claim an absent function returns a status. A propagates actual query errors; B/C distinguish invalid input from unsupported revision/required features. The existing malformed-partition `E_ARG` and post-negotiation expansion/schedule `E_SCHEDULE_INFEASIBLE` obligations remain intact (ISA `:2596,2620–2638,2758–2759,2869–2872,4724–4728`). No request feasibility error is converted into negotiation success or permission to downgrade. A is the smallest proposed contract because it avoids B's handle state and C's additional artifact schema.

4. **Consumer claims reproduce at today's inspected heads.** Every non-meta head still equals the note's pin; tracked source files are unchanged. The accepted ysw file is also unchanged between the note's meta pin and inspected meta main `26dc3b9922f2bf3c7231d9d39c148c4cea113986`. Source inspection, rather than ABI execution, establishes the following:

   | Repository / inspected HEAD | Independently checked evidence |
   |---|---|
   | `bennett-vm` / `4f49792bc6416da6a006adccfd61f99cde2ae76c` | `src/launch.rs:888–893` exports four parameters, matching ISA 0.8 `spec/Bennett-ISA-Spec.md:1201`; ISA 0.9 `:2571–2573` requires eight. The additive export at `src/launch.rs:942–965` validates/copies the invocation representation, calls `invocation::resolve` at `:964`, then unconditionally calls `estimate_unavailable` at `:965` after successful validation. That helper (`:922–938`) returns status 5 without a target, 10 for an oracle with a target, and 5 otherwise; `status` (`:31–43`) returns the error code, not a successful estimate. `src/sched_abi.rs:248–254` builds outcome 2, the unsupported scheduler result. The note's central VM claim is true. |
   | `bennett-sched` / `3fc4d7bdc399a5c6e3df4cd51ce01c4a040eb2fc` | `src/lib.rs:84–88` calls the version probe nonnormative and returns 9; `src/object.rs:160–173` checks header versions. Alias storage/validation is present at `src/request.rs:84–86`, `src/token_aliases.rs:87–106`; `src/schedule.rs:329–349` requires the alias field in closed bindings. None supplies the missing normative negotiation. |
   | `bennett-driver` / `286040cd005b86e9731d0e7a085e88591bce582e` | `src/main.rs:21–22` selects dialect 0.2.13 / ISA 0.8. For a nonempty startup binding, `src/native.rs:501–514` requires a real supplied component retaining the live program; it does not implement launch/sched feature negotiation. Searching all tracked `src` finds no direct launch/sched C-ABI call or dynamic-library feature probe. |
   | `bennett-runtimes` / `d6a4f801d6be3ee9f3743031c2cbc30293de1e79` | The tracked-source search locates `abi_version` only at `src/native/layout.h:9` and `src/native/heap.c:93`. The header's `:1–4` defines the unrelated native comparison ABI; `heap.c:90–96` validates revision 1/layout. No token-alias or launch/sched negotiation path was found. |
   | `bennett-isa-spec` / `62a0cf0ef9f1f1c1db12c84ed24846b6b9695cdc` | `reference-interpreter/src/object.rs:443–447,785–808` accepts coherent 0.8/0.9 object headers. `reference-interpreter/src/main.rs:1871–1881` rejects the named staged target/schedule paths. There is no C launch/sched feature query to infer as a normative default. |

   Reproduction searches used `git -C <repository> grep -n -i -E 'abi_version|features|capabilit|libloading|dlopen|dlsym|bennett_(launch_features|sched_features|load_with_(abi|features)|sched_version|estimate_run|sched_request_set_token_aliases)' HEAD -- src include data`, followed by targeted `nl -ba` reads. Additional broad launch/loader/scheduler/token-alias searches covered driver/runtime sources and the reference loader. The VM's incompatible base signature and incomplete mechanics are existing blockers correctly exposed by the note, not new safe capabilities conferred by a manifest. Consumer matrix lines 185–189 describe future work honestly.

5. **Maintainer decisions remain open and the proposed follow-ups are appropriate.** Note lines 207–212 reserve mechanism/symbol/schema selection, per-role obligations, publication version, loader/shim ownership and the VM ABI boundary for maintainer/council action. Recommendation A is advice, not contract publication. The ysw publication caveat (`doc.md:202–217`), ISA full-envelope versioning (`spec/Bennett-ISA-Spec-0.9.md:68–71`) and mixed-launch boundary (`:4483–4503,4755–4764`) support these questions and the stated hash consequences. Existing b-isa-spec-b3ui and b-isa-spec-8ui remain open; the proposed VM and consumer adoption tasks at note lines 214–220 cover the discovered implementation gaps. No maintainer-only choice is represented as already authorized, and no bead write or closure occurred in this review.

**Disposition: ACCEPT**

This accepts the research note and its evidence. Contract publication, consumer implementation, complete ABI conformance and a full-gate PASS remain unclaimed.
