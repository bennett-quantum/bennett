# Bennett ISA 0.9 reference interpreter: quality-floor change set (job/quality-isaref), council round 1

Subject: the quality-floor remediation of `bennett-isa-spec` (reference-interpreter/ and conformance/), range `be109bd27889ea91e3c0ad78a30e5e4d71d3d0d3..e9ab12a` (16 commits; code head 8056ecf, e9ab12a adds only the r3 review document). Sol review rounds: r1 BLOCK, r2 BLOCK (P0 b-isa-spec-lfbd), r3 CLEAR at 8056ecf (docs/reviews/2026-11-07-quality-isaref-r3.md). The specification is spec/Bennett-ISA-Spec-0.9.md (0.9), attached as context.

Your working directory is a frozen detached worktree of `bennett-isa-spec` at e9ab12a: the whole crate is there to read; this document embeds (1) the full unified diff of the range and (2) the post-change text of every changed file. Grade the change set: semantics changes in claims/qinplace/pairs/replay/certificate/source_constructor, test integrity of the new and changed tests, and any narrowing. Unchanged code is context, not the subject.

## 1. Unified diff (git diff be109bd27889ea91e3c0ad78a30e5e4d71d3d0d3...e9ab12a)

````diff
diff --git a/conformance/Cargo.toml b/conformance/Cargo.toml
index f2d47f7..c39ff37 100644
--- a/conformance/Cargo.toml
+++ b/conformance/Cargo.toml
@@ -5,3 +5,8 @@ edition = "2021"
 license = "AGPL-3.0-only"
 
 [dependencies]
+
+# Keep exhaustive semantic checks practical without dropping debug/overflow checks.
+[profile.test]
+opt-level = 1
+debug = "line-tables-only"
diff --git a/docs/quality.md b/docs/quality.md
new file mode 100644
index 0000000..5133508
--- /dev/null
+++ b/docs/quality.md
@@ -0,0 +1,226 @@
+# Reference interpreter quality floor
+
+Batch 1 (2026-11-06) fixes the round-2 certificate findings and the two
+previously failing crate tests. It leaves the broader coverage, integration
+binary consolidation, and source decomposition work for batch 2.
+
+## Semantic checks
+
+- A K13 subject with a schedule denotes the realised operation for table,
+  program, and oracle relations alike. Until that operation is executed,
+  verification returns `Unverified`, with no reference-only proof or coverage.
+  Absent or mismatching subject schedules are admission errors.
+- K4 inverse-pair claims use their owner-local entry, entry budget and argument
+  domain. Both public verification APIs prove the published parameterised pair;
+  noninverse pairs and absent entries reject. The entry-bound route was already
+  present in the inherited WIP; batch 1 adds certificate-level regression coverage.
+- Example 7 is loaded directly from the published spec. Its qinplace source
+  adapters now use a collision-free lexical alias when constructing an internal
+  ISA operand list; private constructor identities remain private. The source
+  test checks both orientations, instruction allocation/release order, arithmetic
+  results, preserved inputs, and complete reversal.
+- The qreg handle/class-vector capacity check cites §3.3 (the register/type
+  rules); dense quantum-state allocation checks retain §4.3.
+- K91 schedule/certificate readers are checked for canonical partitions,
+  required token-argument bindings, tuple-inconsistent equality, cross-partition
+  certificate reuse, uniform claims, and rejection by the unchanged 0.8 grammar.
+  The inherited K91 support passed these checks; no schema widening was needed.
+
+The regression tests are in `isa09_certificate`, `isa09_qinplace`,
+`r21_resources`, `isa09_token_aliases`, and the published `k91_vectors`.
+
+## Bounded forwarding
+
+The full-width materialisation-capacity witness is ignored in default tests
+with the named reason `slow-source-forwarding`. The default run retains both
+the complete published Example 10 literal domain (4096 inputs, two engines,
+full reversal) and a compact source semantic witness. A separate 1024-leaf
+capacity fixture exercises the host-resource diagnostic in the default run.
+
+Run the wide capacity witness explicitly with:
+
+```sh
+sh reference-interpreter/tools/test-slow-source-forwarding.sh
+```
+
+The script enforces `ulimit -v 8388608`, disables core dumps, bounds wall time
+to 600 seconds, uses one test thread, and reports elapsed time and peak RSS
+with `/usr/bin/time`. The gate invokes this script separately from default
+tests. Both default crate checks in the gate also enforce the 8 GiB address-space
+cap. No unbounded full-width source materialisation is run.
+
+Test profiles use optimisation level 1 and line-table debug information;
+debug assertions and overflow checks retain their enabled test defaults.
+
+## Measurements
+
+The wide slow witness passed with **1,030,472 KiB peak RSS**: 34.38 s test
+execution, 86.91 s wall time including a 52.49 s rebuild. The first bounded
+forwarding run passed 11 tests with one named slow ignore in 40.02 s
+(179.69 s including the initial profile build; 930,700 KiB peak RSS).
+
+The commands below run from the repository root. They use a private target
+directory, a project-local temporary directory, at most three compiler jobs
+and four test threads. GNU time reports wall time including compilation and
+the largest resident-set high-water mark among the command's children,
+not a sum of simultaneous processes.
+
+```sh
+unset DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER
+export TMPDIR="$PWD/.tmp/quality-isaref/tmp"
+export CARGO_TARGET_DIR="$PWD/.tmp/quality-isaref/target"
+mkdir -p "$TMPDIR"
+ulimit -v 8388608
+ulimit -c 0
+/usr/bin/time -v timeout 1800 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml --no-fail-fast -- --test-threads=4
+python3 -I reference-interpreter/tools/publish-cli.py "$CARGO_TARGET_DIR/debug/bennett-isa-ref"
+/usr/bin/time -v timeout 1800 cargo test --offline -j3 --manifest-path conformance/Cargo.toml --no-fail-fast -- --test-threads=4
+```
+
+Verified at 2026-11-06 07:33:36 UTC. Both complete default
+commands above exited 0 under the 8 GiB address-space cap.
+
+| Crate | Passed | Ignored | Wall (min:sec) | Peak RSS (KiB) | Exit |
+|---|---:|---:|---:|---:|---:|
+| reference-interpreter | 653 | 6 | 19:08.93 | 1,591,284 | 0 |
+| conformance | 129 | 0 | 25:39.00 | 723,100 | 0 |
+
+The reference final run reused compiled artifacts; the conformance measurement
+includes its initial test build. These runs overlapped on a shared Linux host,
+so the numbers describe the observed commands rather than isolated benchmarks.
+The reference's six ignores comprise five existing exhaustive sweeps and the
+new named slow forwarding witness. Conformance has no ignored tests.
+
+The original qinplace and register-capacity failures were reproduced before
+their fixes. The first whole reference run also exposed an older controlled-table
+test that expected the false realised `Proof`; its final test now checks
+`Unverified` for the unchanged scheduled fixture and proves the full table
+through an explicit reference-only invocation. The final complete rerun passed.
+
+Both crates also pass `cargo fmt --check` with their manifest paths. Interpreter
+library/binary linting passed:
+`cargo clippy --offline -j3 --manifest-path reference-interpreter/Cargo.toml --lib --bins -- -D warnings`.
+
+The 180-second programme target is **not met** by this batch: conformance's
+1,048,320-tuple call-interface test alone took 337.93 s. Runtime reduction is
+tracked in `b-isa-spec-e923` for batch 2; the remaining `b-isa-spec-x6to`
+nits are also outside the batch-1 correctness fixes. Coverage is not remeasured
+in this batch. The complete repository gate is reserved for the orchestrator.
+
+
+## Certificate review remediation
+
+The follow-up keeps the standalone inverse-pair theorem distinct from executable
+applicability. `ClaimReport.qinplace_applicability` records either `Established`
+or `Unestablished(reason)` for a supplied qinplace owner. Static inventory includes
+nested sites and zero-trip loop bodies. Concrete root and standalone claim
+invocations check the transitive reference construction with each callee's actual
+tokens and arguments; coherent predicates retain their obligations. Missing
+owner-local pairs and uncovered bound sites reject through both public checking
+routes. Zero-trip loops have no dynamic applicability visits.
+
+Linked inverse-pair claims must resolve to an exhaustive pair theorem through an
+acyclic library chain. Every link preserves the exact resolved closure pair,
+minimum tuple, argument-token tuples, token partition and proved argument domain.
+The runtime accepts this library route in both orientations. The published
+Example 7 arithmetic and complete reversal are checked over every x, y and a at
+primary budgets 3 and 9, using an exhaustive donor with no domain on the library
+claim itself. A missing library body retains an unverified theorem and explicit
+unestablished applicability; execution rejects it before effects. Scheduled
+realisation trees and unsupported bound root kinds also remain explicitly
+unestablished rather than inheriting a reference-only acceptance.
+
+Five review regressions were run against an archived `b572e17` source tree before
+the implementation: missing owner inventory, uncovered bound minimum, omitted
+unestablished outcome, proof transfer to g/g, and valid library execution each
+failed for its intended semantic reason. The final suite also covers nested
+sites, zero-trip inventory, disabled controls, transitive owners, donor budget and
+argument-domain preservation, and missing library bodies. No published spec or
+fixture bytes changed.
+
+
+The remediation focused check passed **58 tests with one existing ignore**:
+
+```sh
+timeout 600 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml --test isa09_qinplace --test isa09_claim_replay --test isa09_certificate --test r1_certificates --test r1_qinplace -- --test-threads=4
+```
+
+Both crates passed `cargo fmt --manifest-path <crate>/Cargo.toml -- --check`
+and strict library/binary linting with
+`timeout 600 cargo clippy --offline -j3 --manifest-path <crate>/Cargo.toml --lib --bins -- -D warnings`.
+The reference default command documented above was run once after the source
+changes, with the same environment and caps: **664 passed, six existing ignores,
+exit 0, 21:58.05 wall, 1,592,024 KiB peak RSS**. The freshly built CLI was then
+published to the stable path inside this worktree for the conformance run.
+The conformance default command also passed once after publication, with no
+source changes between either complete run. Runtime and wider quality work remain
+outside this remediation.
+
+
+Final remediation validation recorded at 2026-11-07 06:23:46 UTC.
+Both exact default commands are listed above; each used `ulimit -v 8388608`,
+`timeout 1800`, three compiler jobs and four test threads.
+
+| Crate | Passed | Ignored | Wall (min:sec) | Peak RSS (KiB) | Exit |
+|---|---:|---:|---:|---:|---:|
+| reference-interpreter | 664 | 6 | 21:58.05 | 1,592,024 | 0 |
+| conformance | 129 | 0 | 16:52.64 | 723,256 | 0 |
+
+The reference run includes rebuilding affected binaries; conformance reused its
+compiled artifacts. They ran sequentially on a shared host. The 180-second
+programme target remains open for batch 2; these measurements do not claim it
+is met. No full repository or sibling gate was run for this remediation.
+
+## Bound-root obligation reporting
+
+Certificate checking now returns `CertificateReport`: its `claims` field retains
+standalone claim verdicts, while `qinplace_applicability` records obligations by
+owner or bound root closure independently of the claim collection. Callers that
+previously consumed the returned claim vector select `.claims`. A retained
+standalone `Proof` does not establish executable acceptance when the report
+contains an unestablished applicability obligation.
+
+Unsupported bound root kinds retain their obligation even when no supplied
+record directly owns qinplace, all claims and inverse-pair entries are removed,
+or the region map is empty. The same rule applies to unchecked scheduled trees,
+parameter-uniform invocations and host-resource-limited traversal. Unresolved
+contexts take precedence over checked contexts of the same closure. Concrete
+reference traversal still rejects missing owner-local entries and uncovered
+sites; unbound direct owners retain their separate unestablished outcome.
+
+The attachment audit covered inventory owners, concrete roots, standalone claim
+invocations, uniform invocations, scheduled traversal and work-limit exits, and
+the final claim-report construction. Obligations no longer require a discovered
+owner, claim, record or inverse-pair entry to reach the certificate report.
+Three empty-collection variants and an unchecked uniform transitive claim were
+reproduced as semantic failures before the fix. Additional regressions cover an
+unchecked scheduled root with no reached owners or claims and a concrete check
+that cannot discharge a separate uniform obligation. No published spec or
+fixture bytes changed.
+
+
+Bound-root focused validation passed **64 tests with one existing ignore**, using
+the focused command above. Both crates passed the same formatting and strict
+library/binary Clippy commands, and all reference test binaries compiled with
+`timeout 600 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml --no-run`.
+
+The full default reference command above ran once after the source was frozen:
+**670 passed, six existing ignores, exit 0, 7:00.81 wall, 1,591,540 KiB peak RSS**.
+This run reused the compiled test artifacts and retained the 8 GiB address-space
+cap. Reference results recorded at 2026-11-07 06:52:55 UTC. The completed CLI was atomically
+published inside this worktree before starting the conformance command.
+
+
+Complete bound-root validation recorded at 2026-11-07 07:04:00 UTC. Both default commands
+listed above ran once, sequentially, with `ulimit -v 8388608`, `timeout 1800`,
+three compiler jobs and four test threads. Source stayed unchanged between runs.
+
+| Crate | Passed | Ignored | Wall (min:sec) | Peak RSS (KiB) | Exit |
+|---|---:|---:|---:|---:|---:|
+| reference-interpreter | 670 | 6 | 7:00.81 | 1,591,540 | 0 |
+| conformance | 129 | 0 | 11:27.10 | 727,476 | 0 |
+
+Both runs reused compiled test artifacts on the shared host. The reference's
+six ignores are unchanged; conformance has none. The 180-second target, coverage
+measurement and remaining structural quality work are still deferred to batch 2.
+No full repository or sibling gate ran.
diff --git a/docs/reviews/2026-11-06-quality-isaref-r1.md b/docs/reviews/2026-11-06-quality-isaref-r1.md
new file mode 100644
index 0000000..6d69d97
--- /dev/null
+++ b/docs/reviews/2026-11-06-quality-isaref-r1.md
@@ -0,0 +1,113 @@
+# ISA reference interpreter: quality batch 1, review 1
+
+**Verdict: BLOCK — two P0, one P1.** No implementation files changed.
+
+Reviewed head: `f0c97a864bf7afe23c23371b4f94bcf2ed7c0661` (`job/quality-isaref`).
+Batch range: `main..job/quality-isaref`, seven commits, `7518447..f0c97a8`.
+At review start `main` was `e0424a99197e95057529eae25c176fa34491757a`;
+its source equals the brief's `be109bd` (only the Beads export differs).
+Also reviewed the inherited reference-interpreter changes in
+`9825c42ad5c95cce9cd1419dcbcae0bfffab6e16..e0424a99197e95057529eae25c176fa34491757a`
+(`origin/main..main`) affecting claims, replay, certificates, metadata and token aliases.
+Findings below concern these inherited semantics as well as the batch's intended K4/K92 coverage.
+
+## Blocking findings
+
+**P0-1 — K92 certificate obligations are omitted. Bead `b-isa-spec-jple`.**
+`reference-interpreter/src/claims.rs:874` returns claim reports without checking
+the qinplace pair inventory, bound invocation applicability, or an unresolved
+applicability outcome. Starting from `isa09_qinplace.rs::inverse_certificate()`,
+remove the `addya` record's claims and `verification.inverse_pairs`: parsing
+succeeds and `verify_certificate()` returns `Ok([])` despite its qinplace site.
+Alternatively retain the correct pair and bind root invocation
+`{"args":[["2","0","0","0"],"1"],"budget":["0","0","0","0"],"token_aliases":[0]}`.
+The entry minimum is 3, but verification reports only `[Proof]`; execution
+of that same root rejects `no covering inverse-pair entry`.
+ISA 0.9 §12.3 K92 requires missing owner-local entries and uncovered bound
+sites to reject, and unresolved applicability to be reported explicitly.
+Execution-only checks do not discharge the checker obligation.
+Ran `timeout 60 .tmp/rev-quality-isaref-r1/tmp/review-probe`: exit 0,
+asserting both observations and the execution rejection.
+
+**P0-2 — A library proof transfers to a different, noninverse pair. Bead `b-isa-spec-b6ds`.**
+`reference-interpreter/src/claims.rs:807`–812 returns the referenced claim's
+verdict without checking K4's same-pair side condition. Copy the fixture's
+correct exhaustive `g/ginv` claim and entry into a linked `g` region record
+(with its oracle signature and frame). Replace `addya` claim 0 with a
+concrete `inverse_pair_library` claim referencing that record's claim 0,
+but change the owner entry to `g/g`. Both public verification APIs report
+`Proof`. For the published `g(x;y,a) = x+y+a mod 4`, at `x=y=0,a=1`,
+`g(g(x))=2`, not 0. The exhaustive route correctly rejects this same pair.
+ISA 0.9 §4.5 permits library reuse only for the same resolved g/ginv closures.
+Ran `timeout 60 .tmp/rev-quality-isaref-r1/tmp/review-library-probe`: exit 0,
+asserting the wrong `Proof` and observing exhaustive-route rejection.
+
+**P1-3 — Valid linked-library pair coverage cannot execute. Bead `b-isa-spec-0dq0`.**
+`reference-interpreter/src/claims/qinplace09.rs:131`–134 admits only
+`exhaustive` / `expected:"inverse_pair"`. Keep the correct `g/ginv` entry
+and linked exhaustive donor from P0-2; its owner-local
+`inverse_pair_library` claim verifies as `Proof`. At the covered `tk=3,a=1`,
+`execute_action_with_token_aliases("addya", …, &[0])` nevertheless rejects
+`unestablished linked inverse-pair proof`. The original exhaustive fixture
+executes successfully. This excludes the library route explicitly promised
+by ISA 0.9 §4.5 and suite C, rather than merely leaving applicability unknown.
+Ran `timeout 60 .tmp/rev-quality-isaref-r1/tmp/review-probe`: exit 0,
+asserting that rejection.
+
+The two probes were compiled from stdin with `timeout 120 rustc`, linked
+against the freshly built review rlib, and included the existing
+`tests/isa09_qinplace.rs` helpers. Their mutations affect certificate JSON
+only; the independent arithmetic counterexample is given above.
+
+## Verification and scope
+
+All commands were headless, with private `.tmp/rev-quality-isaref-r1/{tmp,target}`
+directories; Cargo runs had an 8 GiB address-space cap and core dumps disabled.
+
+```sh
+timeout 600 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml \
+  --test isa09_certificate --test isa09_claim_replay --test isa09_token_aliases \
+  --test isa09_qinplace --test r21_resources --test k91_vectors -- --test-threads=4
+timeout 300 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml \
+  --test isa09_forwarding -- --test-threads=4
+git diff --check main...job/quality-isaref
+```
+
+Results: exit 0 for each; respectively 53 passed, then 11 passed / one
+`slow-source-forwarding` ignore. No full crate suite, gate or sibling gate ran.
+The wide slow witness was inspected, not rerun; its script supplies the memory
+and wall-time caps and the gate invokes it explicitly.
+
+The scheduled table/program/oracle regressions now return `Unverified` without
+coverage; dangling/missing schedules reject. Reading `git show main:<path>`
+confirms those scheduled-table regressions and the existing source-qinplace
+expansion test catch the old paths. The r21 correction matches §3.3's qreg
+storage rule. The exhaustive inverse-pair route already existed on main;
+the added certificate assertions exercise it, not a newly failing baseline.
+K91's concrete partitions, uniform admission, cross-partition rejection and
+unchanged 0.8 grammar pass the focused tests. Correcting the old scheduled
+`Proof` expectation preserves its full reference-table checks.
+
+P2+ nits, **one bead `b-isa-spec-nivd`**: redundant/dead inverse-pair dispatch;
+tracked pycache/log/progress litter; deferred long functions and production
+test hooks; missing gate ratchet, stale `HANDOFF.md`, coverage and runtime target.
+Programme items 9–10 were checked: the batch-1 implementer brief expressly
+assigns them to batch 2. The reported default runtimes exceed 180 seconds.
+
+Anti-slop: checked each COMMON rule. No new inconsistent state flags, silent
+failure default, repeated compound predicate, semantic magic number, process
+identifier, oracle-derived test expectation, test weakening or owned-path
+violation found in the batch fix. The library dispatch and missing K92
+validation above are the confirmed semantic failures; structural debt is in
+the combined nit bead.
+
+Coverage: read closely the complete batch source/test diff, `claims/replay09.rs`,
+`pairs09.rs`, `qinplace09.rs`, `images09.rs`, claim execution/verdict routes,
+certificate admission, token partition resolution, and K91 schedule binding
+paths against §§4.5, 12.1–12.3; skimmed other source-path/tie-selection code,
+fixture generators, CLI plumbing and broad inherited changes outside those paths.
+Full conformance, target realisation, numerical/channel and unrelated interpreter
+subsystems were not exhaustively reviewed.
+
+Provenance: implementer **gpt-6.1-sol**; reviewer **gpt-6.1-sol, fresh session, D9**.
+This BLOCK review does not claim council clearance.
diff --git a/docs/reviews/2026-11-07-quality-isaref-r2.md b/docs/reviews/2026-11-07-quality-isaref-r2.md
new file mode 100644
index 0000000..e0fa3da
--- /dev/null
+++ b/docs/reviews/2026-11-07-quality-isaref-r2.md
@@ -0,0 +1,88 @@
+# ISA reference interpreter: quality batch 1, review 2
+
+**Verdict: BLOCK — one residual P0; no P1.** No implementation files changed.
+
+Reviewed head: `cdef3eb184e2aab9dcf97bde5fd3be1fcf6e1982` (`job/quality-isaref`).
+Batch inventory: `git log --reverse main..job/quality-isaref` and
+`git diff main...job/quality-isaref`; round-2 review focuses on
+`b572e17..cdef3eb` (`92fbe5c`, `75cec86`, `cdef3eb`) and reproduces the
+three findings in `2026-11-06-quality-isaref-r1.md`.
+
+## Blocking finding
+
+**P0-1 — Unresolved bound-root applicability disappears when the owner map is empty.
+Bead `b-isa-spec-lfbd` (residual of `b-isa-spec-jple`).**
+`reference-interpreter/src/claims/qinplace09.rs:142`–144 records an unsupported
+CC/R root as unresolved, but lines 179–182 attach that outcome only to already
+inventoried direct qinplace owners. If none of the supplied records directly
+contains qinplace, the map is empty and the obligation silently disappears.
+`reference-interpreter/src/claims.rs:923` consequently reports applicability
+`None`, rather than `Unestablished`.
+
+Repro from `tests/isa09_qinplace.rs::transitive_certificate(false)`:
+the linked path is `run` (CC) → `addya` → `inner` → qinplace. The certificate
+contains only the outer `addya` record and its valid inverse-pair theorem;
+the required `inner` owner entry is absent. Change `bindings.closure_hash`,
+`reference_program_hash` and `interface_hash` to the identities of `run`, and
+set `bindings.invocation = root_invocation(2, 1)`. Parsing succeeds.
+`verify_certificate()` returns one `Proof` with `qinplace_applicability: None`;
+`verify_claim(addya, 0)` also returns `Proof`. Removing the outer record’s
+claims and inverse-pair entries instead returns `Ok([])`, still without an
+unestablished outcome. Executing the corresponding `addya` invocation at
+`tk=3,a=1` rejects `no covering inverse-pair entry in @inner` before effects.
+
+ISA 0.9 §12.3 K92 requires bound transitive coverage, and explicitly requires
+an unestablished obligation when an invocation/context cannot be checked.
+Keeping the standalone theorem is permitted; omitting the unresolved
+applicability obligation is not. An unsupported root needs an observable
+obligation even when the actual owner record or all claim reports are absent.
+
+Ran `timeout 60 .tmp/rev-quality-isaref-r2/tmp/review-probe` and
+`timeout 60 .tmp/rev-quality-isaref-r2/tmp/review-applicability-probe`: both
+exit 0, asserting these observations. Probes were compiled from stdin with
+`timeout 120 rustc`, included the existing qinplace fixture helpers, and
+linked against the freshly built review rlib. Only certificate JSON was mutated.
+
+## Verification and scope
+
+The original round-1 probes now pass: missing direct owner inventory rejects;
+a bound primary tuple below the entry minimum rejects through both public
+checking APIs; an unbound direct owner reports explicit unestablished
+applicability; the library g/g substitution rejects; a valid linked g/ginv
+pair executes with the hand-derived arithmetic result and reverses exactly.
+Thus `b-isa-spec-b6ds` and `b-isa-spec-0dq0` are fixed in the reviewed paths;
+`b-isa-spec-jple` retains the sibling-route gap above.
+
+All test/probe commands were headless, used private
+`.tmp/rev-quality-isaref-r2/{tmp,target}` directories, and ran under
+`ulimit -v 8388608; ulimit -c 0`.
+
+```sh
+timeout 600 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml \
+  --test isa09_qinplace --test isa09_claim_replay --test isa09_certificate -- --test-threads=4
+timeout 600 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml \
+  --test r1_certificates --test r1_qinplace -- --test-threads=4
+git diff --check b572e17..cdef3eb
+```
+
+Results: **58 passed, one existing ignore**, all commands exit 0. No full
+reference suite, repository gate or sibling gate ran. Reading the main-side
+and pre-fix claim/coverage code confirms the new inventory, library-pair
+identity and executable-library regressions distinguish the old behavior;
+expected arithmetic is independent of the implementation.
+
+P2+ nits: **one bead `b-isa-spec-fg4u`** consolidates continuing dead dispatch,
+tracked litter, stale `HANDOFF.md`, missing gate ratchet, production no-op
+hooks, and deferred function/coverage/runtime work (also `b-isa-spec-nivd`).
+No new nonblocking pattern found in the fix. Checked every COMMON anti-slop
+rule; the silent obligation loss is the confirmed blocking violation. Batch-2
+items remain assigned to batch 2 by the implementer brief.
+
+Coverage: read closely the complete round-2 source/test diff, pair theorem
+resolution, inventory/applicability traversal, both public checking APIs,
+replay invocation decoding and certificate admission against §§4.5, 12.3
+K4/K92; skimmed unchanged action/oracle call plumbing and prior structural
+debt. Other interpreter subsystems and full conformance were not re-reviewed.
+
+Provenance: implementer **gpt-6.1-sol**; reviewer **gpt-6.1-sol, fresh session, D9**.
+This BLOCK review does not claim council clearance.
diff --git a/docs/reviews/2026-11-07-quality-isaref-r3.md b/docs/reviews/2026-11-07-quality-isaref-r3.md
new file mode 100644
index 0000000..2fdd823
--- /dev/null
+++ b/docs/reviews/2026-11-07-quality-isaref-r3.md
@@ -0,0 +1,83 @@
+# ISA reference interpreter: quality batch 1, review 3
+
+**Verdict: CLEAR — no P0/P1.** No implementation files changed.
+
+Reviewed head: `8056ecf3834955ec8a46f091b7d90b026dc207dd` (`job/quality-isaref`).
+Batch inventory: `git log --reverse main..job/quality-isaref` and
+`git diff main...job/quality-isaref`; this final review focuses on
+`d3a338e..8056ecf` (`15c8c3a`, `fa8f276`, `8056ecf`) and rechecks the
+P0/P1 scenarios from both earlier review documents against ISA 0.9 §§4.5,
+12.3 K92.
+
+The residual **P0-1 `b-isa-spec-lfbd` is fixed**. An independent stdin Rust
+probe rebuilt the round-2 `run → addya → inner → qinplace` certificate,
+retargeting the root bindings to `run` with `root_invocation(2, 1)`.
+With the outer pair claim retained, its standalone verdict remains `Proof`
+and the report independently contains `run: Unestablished`. Removing the
+outer claims and entries preserves that root obligation with zero claim
+reports; removing every region record also preserves it. In all three
+variants, executing `addya` at tk=3,a=1 rejects the missing inner-owner
+entry before effects and leaves the quantum state unchanged.
+
+The original round-1 findings remain fixed: missing direct inventory and
+below-minimum bound tuples reject; wrong g/g library reuse rejects through
+both public verification APIs; valid g/ginv library coverage executes the
+hand-derived result and reverses exactly. Focused tests also cover transitive
+arguments, zero-trip inventory, disabled predicates and unavailable libraries.
+
+`CertificateReport.qinplace_applicability` retains obligations independently
+of records and claims. Unsupported roots, unchecked uniform arguments,
+scheduled trees and host-resource failures insert their own closure keys;
+unresolved outcomes merge last so a checked concrete context cannot discharge
+a uniform obligation. Static owner outcomes and checked transitive owners
+are retained too. Explicit borrow-frame references remain index-validated
+and checked separately; their enforcement does not rely on a nonempty report.
+The standalone `verify_claim` contract explicitly disclaims executable
+applicability.
+
+The report-shape change retains all claim fields and their closure-map /
+claim-index order inside `.claims`; the probe checks both linked-library
+records are present and ordered. The Rust API intentionally requires callers
+to select `.claims`. No production CLI command serializes or consumes
+`verify_certificate`; CLI/JSON formatting code is unchanged. Existing public
+CLI partition and resource-output tests pass.
+
+Verification used headless commands, private
+`.tmp/rev-quality-isaref-r3/{tmp,target}`, `ulimit -v 8388608` and `ulimit -c 0`:
+
+```sh
+timeout 600 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml \
+  --test isa09_qinplace --test isa09_claim_replay --test isa09_certificate \
+  --test isa09_token_aliases -- --test-threads=4
+timeout 600 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml \
+  --test r1_certificates --test r1_qinplace --test r21_resources \
+  --test r22_coverage -- --test-threads=4
+timeout 60 .tmp/rev-quality-isaref-r3/tmp/review-probe
+git diff --check main...job/quality-isaref
+```
+
+All exit 0: **95 tests passed, one unchanged ignore**; independent probe passed.
+The probe was compiled with `timeout 120 rustc --edition=2021 -C opt-level=1`,
+including the existing fixture helpers and linking freshly built review rlibs.
+Reading `git show main:reference-interpreter/src/claims.rs` and the pre-fix
+`qinplace09.rs` confirms the empty-report and uniform/scheduled regressions
+would fail there: main has no independent applicability report, while the
+round-2 code loses unresolved outcomes on an empty owner map and skips uniform
+obligations. No branch switching, full crate suite, repository gate or sibling
+gate was used. No tests or expectations were weakened.
+
+P2+ nits: **one bead `b-isa-spec-bkqj`** consolidates existing dead dispatch,
+tracked litter, stale `HANDOFF.md`, missing gate ratchet, production no-op
+hooks and deferred function/coverage/runtime work; no new nit in this fix.
+Checked every COMMON anti-slop rule; no new semantic violation or narrowing.
+Batch-2 items remain assigned to batch 2 by the implementer brief.
+
+Coverage: read closely the complete round-3 source/test diff, both verification
+APIs, K92 inventory/traversal and outcome merges, certificate invocation/index
+admission, prior P0/P1 scenarios and public report consumers; skimmed unchanged
+pair-theorem and CLI plumbing and continuing structural debt. Other interpreter
+subsystems and full conformance were not re-reviewed.
+
+Provenance: implementer **gpt-6.1-sol**; reviewer **gpt-6.1-sol, fresh session, D9**.
+CLEAR applies to this review scope; the required critical-batch council round
+remains the orchestrator's next step.
diff --git a/gate.toml b/gate.toml
index adf6e0c..12491aa 100644
--- a/gate.toml
+++ b/gate.toml
@@ -13,11 +13,15 @@ argv = ["sh", "-c", "for c in reference-interpreter conformance; do rm -rf \"$c/
 
 [[check]]
 name = "cargo test reference-interpreter"
-argv = ["cargo", "test", "--offline", "--manifest-path", "reference-interpreter/Cargo.toml"]
+argv = ["sh", "-ec", "ulimit -v 8388608; ulimit -c 0; exec timeout 1800 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml -- --test-threads=4"]
 
 [[check]]
 name = "cargo test conformance"
-argv = ["cargo", "test", "--offline", "--manifest-path", "conformance/Cargo.toml"]
+argv = ["sh", "-ec", "ulimit -v 8388608; ulimit -c 0; exec timeout 1800 cargo test --offline -j3 --manifest-path conformance/Cargo.toml -- --test-threads=4"]
+
+[[check]]
+name = "slow-source-forwarding (8 GiB cap)"
+argv = ["sh", "reference-interpreter/tools/test-slow-source-forwarding.sh"]
 
 [[check]]
 name = "diff witness"
diff --git a/reference-interpreter/Cargo.toml b/reference-interpreter/Cargo.toml
index 932ef42..0012983 100644
--- a/reference-interpreter/Cargo.toml
+++ b/reference-interpreter/Cargo.toml
@@ -6,3 +6,8 @@ license = "AGPL-3.0-only"
 
 [dependencies]
 bennett-isa-conformance = { path = "../conformance" }
+
+# Keep exhaustive semantic checks practical without dropping debug/overflow checks.
+[profile.test]
+opt-level = 1
+debug = "line-tables-only"
diff --git a/reference-interpreter/src/certificate.rs b/reference-interpreter/src/certificate.rs
index c0d4d1e..2dfc3b3 100644
--- a/reference-interpreter/src/certificate.rs
+++ b/reference-interpreter/src/certificate.rs
@@ -734,6 +734,14 @@ impl Object {
                 .get("subject")
                 .and_then(|s| s.object().ok())
                 .and_then(|s| s.get("schedule_hash"));
+            if let Some(bound_hash) = subject_schedule {
+                let schedule = self
+                    .section("schedule")
+                    .ok_or_else(|| Error::new("§12.1 K13: claim schedule is absent".into()))?;
+                if bound_hash.string()? != sha256_hex(schedule.canonical().as_bytes()) {
+                    return err("§12.1 K13", "claim schedule hash mismatch");
+                }
+            }
             if c.object()?.get("expected") == Some(&Json::String("oracle".into()))
                 && subject_schedule.is_none()
             {
diff --git a/reference-interpreter/src/claims.rs b/reference-interpreter/src/claims.rs
index 1be449f..95d6717 100644
--- a/reference-interpreter/src/claims.rs
+++ b/reference-interpreter/src/claims.rs
@@ -46,6 +46,14 @@ pub enum ClaimVerdict {
     Unverified(String),
 }
 #[derive(Clone, Debug, PartialEq, Eq)]
+pub struct CertificateReport {
+    pub claims: Vec<ClaimReport>,
+    /// K92 obligations keyed by the owning or bound root closure. These survive
+    /// absent owner records and empty claim lists; a claim proof does not
+    /// discharge an unestablished invocation obligation.
+    pub qinplace_applicability: BTreeMap<String, QinplaceApplicability>,
+}
+#[derive(Clone, Debug, PartialEq, Eq)]
 pub struct ClaimReport {
     pub closure_hash: String,
     pub region: String,
@@ -54,6 +62,13 @@ pub struct ClaimReport {
     pub verdict: ClaimVerdict,
     pub context_key: Json,
     pub coverage: Option<ClaimCoverage>,
+    /// K92 applicability is separate from the standalone theorem's verdict.
+    pub qinplace_applicability: Option<QinplaceApplicability>,
+}
+#[derive(Clone, Debug, PartialEq, Eq)]
+pub enum QinplaceApplicability {
+    Established,
+    Unestablished(String),
 }
 #[derive(Clone, Debug, PartialEq, Eq)]
 pub struct ClaimCoverage {
@@ -647,9 +662,14 @@ impl Object {
         }))
     }
     /// Checks one claim of region `closure`. A false claim is an error; an
-    /// uncheckable one is `Unverified` with its reason.
+    /// uncheckable one is `Unverified` with its reason. This standalone verdict
+    /// does not establish executable applicability; see `verify_certificate`.
     pub fn verify_claim(&self, closure: &str, index: usize) -> Result<ClaimVerdict> {
-        self.verify_claim_guarded(closure, index, &mut BTreeSet::new())
+        let verdict = self.verify_claim_guarded(closure, index, &mut BTreeSet::new())?;
+        if self.isa_version == crate::IsaVersion::V09 {
+            self.check_qinplace_bindings09()?;
+        }
+        Ok(verdict)
     }
     fn verify_claim_guarded(
         &self,
@@ -805,6 +825,9 @@ impl Object {
                         ClaimVerdict::Proof
                     }
                     "inverse_pair_library" => {
+                        if self.isa_version == crate::IsaVersion::V09 {
+                            self.inverse_pair_theorem09(closure, index, &mut BTreeSet::new())?;
+                        }
                         let library = witness.get("library_closure_hash")?.string()?;
                         let i = usize::try_from(witness.get("claim_index")?.uint()?)
                             .map_err(|_| Error::new("§12: claim index".into()))?;
@@ -870,11 +893,16 @@ impl Object {
         )
     }
     /// Checks every claim of the certificate: false claims are errors, and
-    /// the report lists each claim's verdict.
-    pub fn verify_certificate(&self) -> Result<Vec<ClaimReport>> {
+    /// the report lists each claim's verdict and independent K92 obligations.
+    pub fn verify_certificate(&self) -> Result<CertificateReport> {
         let certificate = self
             .section("certificate")
             .ok_or_else(|| Error::new("§12: object has no certificate".into()))?;
+        let applicability = if self.isa_version == crate::IsaVersion::V09 {
+            self.check_qinplace_bindings09()?
+        } else {
+            BTreeMap::new()
+        };
         let mut reports = Vec::new();
         for (closure, region) in certificate.get("regions")?.object()? {
             let name = self.region_function(closure)?.name.clone();
@@ -888,7 +916,10 @@ impl Object {
                     let outcome = self.verify_replay09(closure, index, claim, f)?;
                     (outcome.verdict, outcome.coverage)
                 } else {
-                    (self.verify_claim(closure, index)?, None)
+                    (
+                        self.verify_claim_guarded(closure, index, &mut BTreeSet::new())?,
+                        None,
+                    )
                 };
                 reports.push(ClaimReport {
                     closure_hash: closure.clone(),
@@ -898,6 +929,7 @@ impl Object {
                     verdict,
                     context_key: Json::Array(Vec::new()),
                     coverage,
+                    qinplace_applicability: applicability.get(closure).cloned(),
                 });
             }
             // A borrow_frames claim must be a proof over D with the §5.6 property.
@@ -916,7 +948,10 @@ impl Object {
                 self.check_borrow_independence(f, closure, i)?;
             }
         }
-        Ok(reports)
+        Ok(CertificateReport {
+            claims: reports,
+            qinplace_applicability: applicability,
+        })
     }
     /// §5.6 library route: a region whose frames the symbolic decision cannot
     /// settle is admitted iff each of its certificate `borrow_frames` claims
diff --git a/reference-interpreter/src/claims/pairs09.rs b/reference-interpreter/src/claims/pairs09.rs
index 7569ca4..7c6baf6 100644
--- a/reference-interpreter/src/claims/pairs09.rs
+++ b/reference-interpreter/src/claims/pairs09.rs
@@ -188,6 +188,91 @@ fn full_quantum_domain(object: &Object, g: &Function, domain: &Json) -> Result<(
     Ok(())
 }
 impl Object {
+    /// Resolve the pair theorem, retaining its domain through library reuse.
+    /// Every link must bind the same closures and a covered token context.
+    pub(super) fn inverse_pair_theorem09(
+        &self,
+        closure: &str,
+        index: usize,
+        active: &mut BTreeSet<(String, usize)>,
+    ) -> Result<Option<(&Json, &Function)>> {
+        let key = (closure.to_string(), index);
+        if !active.insert(key.clone()) {
+            return err("§12.1 K4", "cyclic inverse-pair library reference");
+        }
+        let regions = self
+            .section("certificate")
+            .unwrap()
+            .get("regions")?
+            .object()?;
+        let Some(record) = regions.get(closure) else {
+            return Ok(None);
+        };
+        let claim = record
+            .get("claims")?
+            .array()?
+            .get(index)
+            .ok_or_else(|| Error::new("§12.1 K4: library claim index out of range".into()))?;
+        let owner = self.region_function(closure)?;
+        let entries = self.pair_claim_entries(owner, index)?;
+        let result = match claim.get("kind")?.string()? {
+            "exhaustive" if claim.get("expected")? == &Json::String("inverse_pair".into()) => {
+                self.validate_inverse_pair_claim09(owner, index, claim)?;
+                Some((claim, pair(self, entries[0])?.g))
+            }
+            "structural" if claim.get("rule")?.string()? == "inverse_pair_library" => {
+                let witness = claim.get("witness")?;
+                let library = witness.get("library_closure_hash")?.string()?;
+                let donor_index = usize::try_from(witness.get("claim_index")?.uint()?)
+                    .map_err(|_| crate::resource_error("§12.1 K4", "claim index exceeds host"))?;
+                let Some(theorem) = self.inverse_pair_theorem09(library, donor_index, active)?
+                else {
+                    return Ok(None);
+                };
+                let donor = self.region_function(library)?;
+                let donor_entries = self.pair_claim_entries(donor, donor_index)?;
+                for entry in entries {
+                    let current = pair(self, entry)?;
+                    let mut covered = false;
+                    for donor_entry in &donor_entries {
+                        let source = pair(self, donor_entry)?;
+                        let (g, gi) = (entry.get("g")?, entry.get("ginv")?);
+                        let (sg, si) = (donor_entry.get("g")?, donor_entry.get("ginv")?);
+                        let same_pair = (g == sg && gi == si) || (g == si && gi == sg);
+                        covered |= same_pair
+                            && current.budget.steps >= source.budget.steps
+                            && current.budget.heap >= source.budget.heap
+                            && current.budget.stack >= source.budget.stack
+                            && current.budget.depth >= source.budget.depth
+                            && current.aliases == source.aliases
+                            && current.g.params[4]
+                                .iter()
+                                .filter(|p| p.ty == Type::Token)
+                                .map(|p| current.tokens[&p.name])
+                                .eq(source.g.params[4]
+                                    .iter()
+                                    .filter(|p| p.ty == Type::Token)
+                                    .map(|p| source.tokens[&p.name]));
+                    }
+                    if !covered {
+                        return err(
+                            "§12.1 K4",
+                            "library theorem must cover the same resolved pair and token context",
+                        );
+                    }
+                }
+                Some(theorem)
+            }
+            _ => {
+                return err(
+                    "§12.1 K4",
+                    "entry claim is not an exhaustive or linked-library inverse-pair theorem",
+                )
+            }
+        };
+        active.remove(&key);
+        Ok(result)
+    }
     fn pair_claim_entries(&self, owner: &Function, index: usize) -> Result<Vec<&Json>> {
         let closure = self.identity()?.closure_hashes[&owner.name]
             .clone()
@@ -273,7 +358,10 @@ impl Object {
             }
             for row in enumerate(&domain)? {
                 let mut input = OracleVectorInput {
-                    ins: p.g.params[0].iter().map(|p| BitVector::zero(p.ty.bits(self.ptr_width)?)).collect::<Result<_>>()?,
+                    ins: p.g.params[0]
+                        .iter()
+                        .map(|p| BitVector::zero(p.ty.bits(self.ptr_width)?))
+                        .collect::<Result<_>>()?,
                     ..Default::default()
                 };
                 for param in &p.g.params[3] {
diff --git a/reference-interpreter/src/claims/qinplace09.rs b/reference-interpreter/src/claims/qinplace09.rs
index 54f3521..012ef6e 100644
--- a/reference-interpreter/src/claims/qinplace09.rs
+++ b/reference-interpreter/src/claims/qinplace09.rs
@@ -10,6 +10,17 @@ struct Invocation {
     budget: Option<Budget>,
     primary: Option<BudgetToken>,
 }
+fn qinplace_sites(f: &Function) -> Vec<&Instruction> {
+    let mut work = f.instructions().collect::<Vec<_>>();
+    let mut sites = Vec::new();
+    while let Some(i) = work.pop() {
+        if i.op == "qinplace" {
+            sites.push(i);
+        }
+        work.extend(i.bodies.iter().flatten());
+    }
+    sites
+}
 fn values(f: &Function, args: &BTreeMap<String, Argument>) -> Result<Vec<Argument>> {
     f.params[if f.kind == "oracle" { 4 } else { 3 }]
         .iter()
@@ -54,12 +65,150 @@ fn push(
     Ok(())
 }
 impl Object {
+    /// Inventory is static (including zero-trip bodies); applicability belongs
+    /// to the resolved invocation tree, never to the standalone proof label.
+    pub(super) fn check_qinplace_bindings09(
+        &self,
+    ) -> Result<BTreeMap<String, QinplaceApplicability>> {
+        let certificate = self.section("certificate").unwrap();
+        let identity = self.identity()?;
+        let mut outcomes = BTreeMap::new();
+        if !self
+            .functions
+            .values()
+            .any(|f| !qinplace_sites(f).is_empty())
+        {
+            return Ok(outcomes);
+        }
+        for (closure, record) in certificate.get("regions")?.object()? {
+            let f = self.region_function(closure)?;
+            for site in qinplace_sites(f) {
+                let hash = |name: &str| -> Result<&str> {
+                    identity.closure_hashes[name.trim_start_matches('@')]
+                        .as_deref()
+                        .ok_or_else(|| Error::new("§12.3 K92: unresolved qinplace closure".into()))
+                };
+                let g = hash(&site.operands[0])?;
+                let gi = hash(&site.operands[1])?;
+                let mut found = false;
+                for entry in record.get("verification")?.get("inverse_pairs")?.array()? {
+                    let eg = entry.get("g")?.string()?;
+                    let ei = entry.get("ginv")?.string()?;
+                    if !((eg == g && ei == gi) || (eg == gi && ei == g)) {
+                        continue;
+                    }
+                    found = true;
+                    let index = usize::try_from(entry.get("claim")?.uint()?).map_err(|_| {
+                        crate::resource_error("§12.3 K92", "claim index exceeds host")
+                    })?;
+                    self.inverse_pair_theorem09(closure, index, &mut BTreeSet::new())?;
+                    self.verify_claim_guarded(closure, index, &mut BTreeSet::new())?;
+                }
+                if !found {
+                    return err(
+                        "§12.3 K92",
+                        format!("missing owner-local inverse-pair entry in @{}", f.name),
+                    );
+                }
+                outcomes.insert(
+                    closure.clone(),
+                    QinplaceApplicability::Unestablished(
+                        "no resolved invocation establishes qinplace applicability".into(),
+                    ),
+                );
+            }
+        }
+        let bindings = certificate.get("bindings")?;
+        let root = bindings.get("closure_hash")?.string()?;
+        let mut invocations = Vec::new();
+        let mut unresolved = BTreeMap::new();
+        if let Some(invocation) = bindings.object()?.get("invocation") {
+            invocations.push((root, invocation));
+        }
+        for (closure, record) in certificate.get("regions")?.object()? {
+            for claim in record.get("claims")?.array()? {
+                if let Some(invocation) = claim.object()?.get("invocation") {
+                    // Parameter-uniform claims keep their universal theorem;
+                    // proving applicability requires a separate uniform check.
+                    if invocation.get("args")?.array().is_ok() {
+                        invocations.push((closure.as_str(), invocation));
+                    } else {
+                        unresolved.insert(
+                            closure.clone(),
+                            QinplaceApplicability::Unestablished(
+                                "parameter-uniform invocation tree is not checked".into(),
+                            ),
+                        );
+                    }
+                }
+            }
+        }
+        let mut checked = BTreeMap::new();
+        for (closure, binding) in invocations {
+            let f = self.region_function(closure)?;
+            if !matches!(f.kind.as_str(), "oracle" | "action" | "perm_action") {
+                unresolved.insert(
+                    closure.to_string(),
+                    QinplaceApplicability::Unestablished(format!(
+                        "bound @{} invocation tree is not checked",
+                        f.name
+                    )),
+                );
+                continue;
+            }
+            let invocation = self.decode_invocation09(binding, f)?;
+            let group = if f.kind == "oracle" { 4 } else { 3 };
+            let args = f.params[group]
+                .iter()
+                .zip(invocation.args)
+                .map(|(p, value)| (p.name.clone(), value))
+                .collect();
+            match self.qinplace_coverage09(
+                f,
+                &args,
+                Some(invocation.budget),
+                invocation.primary.as_ref(),
+            ) {
+                Ok(owners) if self.section("schedule").is_none() => {
+                    for (owner, outcome) in owners {
+                        if !matches!(
+                            checked.get(&owner),
+                            Some(QinplaceApplicability::Unestablished(_))
+                        ) {
+                            checked.insert(owner, outcome);
+                        }
+                    }
+                }
+                Ok(_) => {
+                    unresolved.insert(
+                        closure.to_string(),
+                        QinplaceApplicability::Unestablished(
+                            "complete realised invocation tree is not checked".into(),
+                        ),
+                    );
+                }
+                Err(error) if error.kind() == crate::ErrorKind::HostResource => {
+                    unresolved.insert(
+                        closure.to_string(),
+                        QinplaceApplicability::Unestablished(error.to_string()),
+                    );
+                }
+                Err(error) => return Err(error),
+            }
+        }
+        outcomes.extend(checked);
+        // Root obligations cannot depend on discovering an owner or a claim.
+        // An unchecked context also takes precedence over a checked context of
+        // the same closure: one invocation cannot discharge another's coverage.
+        outcomes.extend(unresolved);
+        Ok(outcomes)
+    }
     fn check_qinplace_site09(
         &self,
         owner: &Function,
         i: &Instruction,
         args: &BTreeMap<String, Argument>,
-    ) -> Result<()> {
+    ) -> Result<QinplaceApplicability> {
         let a = &i.operands;
         let primary = token(args, &a[2])?;
         let actuals = if a.len() == 7 {
@@ -95,6 +244,7 @@ impl Object {
         let gi = identity.closure_hashes[a[1].trim_start_matches('@')]
             .as_deref()
             .ok_or_else(missing)?;
+        let mut unresolved = None;
         for entry in record.get("verification")?.get("inverse_pairs")?.array()? {
             let eg = entry.get("g")?.string()?;
             let ei = entry.get("ginv")?.string()?;
@@ -123,17 +273,13 @@ impl Object {
             }
             let index = usize::try_from(entry.get("claim")?.uint()?)
                 .map_err(|_| crate::resource_error("§12.3 K4", "claim index exceeds host"))?;
-            let claim = record
-                .get("claims")?
-                .array()?
-                .get(index)
-                .ok_or_else(|| Error::new("§12.3 K4: pair claim index out of range".into()))?;
-            if claim.get("kind")?.string()? != "exhaustive"
-                || claim.object()?.get("expected") != Some(&Json::String("inverse_pair".into()))
-            {
-                return err("§4.5 K4", "unestablished linked inverse-pair proof");
-            }
-            let ranges = args_domain(self, p.g, claim.get("domain")?)?;
+            let Some((claim, domain_function)) =
+                self.inverse_pair_theorem09(owner_hash, index, &mut BTreeSet::new())?
+            else {
+                unresolved = Some("linked inverse-pair theorem is unavailable".into());
+                continue;
+            };
+            let ranges = args_domain(self, domain_function, claim.get("domain")?)?;
             let mut covers = true;
             for (slot, (param, value)) in p.g.params[4].iter().zip(&actuals).enumerate() {
                 if param.ty == Type::Token {
@@ -151,11 +297,17 @@ impl Object {
             if !covers {
                 continue;
             }
-            if self.verify_claim(owner_hash, index)? == ClaimVerdict::Proof {
-                return Ok(());
+            if self.verify_claim_guarded(owner_hash, index, &mut BTreeSet::new())?
+                == ClaimVerdict::Proof
+            {
+                return Ok(QinplaceApplicability::Established);
             }
+            unresolved = Some("entry claim is not an established inverse-pair proof".into());
+        }
+        match unresolved {
+            Some(reason) => Ok(QinplaceApplicability::Unestablished(reason)),
+            None => Err(missing()),
         }
-        Err(missing())
     }
     pub(crate) fn precheck_qinplace09(
         &self,
@@ -164,13 +316,30 @@ impl Object {
         budget: Option<Budget>,
         primary: Option<&BudgetToken>,
     ) -> Result<()> {
+        for outcome in self.qinplace_coverage09(f, args, budget, primary)?.values() {
+            if let QinplaceApplicability::Unestablished(reason) = outcome {
+                return err(
+                    "§4.5 K4/K92",
+                    format!("unestablished qinplace applicability: {reason}"),
+                );
+            }
+        }
+        Ok(())
+    }
+    fn qinplace_coverage09(
+        &self,
+        f: &Function,
+        args: &BTreeMap<String, Argument>,
+        budget: Option<Budget>,
+        primary: Option<&BudgetToken>,
+    ) -> Result<BTreeMap<String, QinplaceApplicability>> {
         if self.isa_version != crate::IsaVersion::V09
             || !self
                 .functions
                 .values()
-                .any(|f| f.instructions().any(|i| i.op == "qinplace"))
+                .any(|f| !qinplace_sites(f).is_empty())
         {
-            return Ok(());
+            return Ok(BTreeMap::new());
         }
         let mut work = vec![Invocation {
             name: f.name.clone(),
@@ -179,6 +348,7 @@ impl Object {
             primary: primary.cloned(),
         }];
         let mut visited = BTreeSet::new();
+        let mut owners = BTreeMap::new();
         while let Some(invocation) = work.pop() {
             let f = &self.functions[&invocation.name];
             let ids = invocation
@@ -203,6 +373,14 @@ impl Object {
             if !visited.insert(key) {
                 continue;
             }
+            if !qinplace_sites(f).is_empty() {
+                let closure = self.identity()?.closure_hashes[&f.name]
+                    .clone()
+                    .ok_or_else(|| Error::new("§12.3 K92: unresolved owner".into()))?;
+                owners
+                    .entry(closure)
+                    .or_insert(QinplaceApplicability::Established);
+            }
             let args = f.params[if f.kind == "oracle" { 4 } else { 3 }]
                 .iter()
                 .zip(&invocation.args)
@@ -255,7 +433,15 @@ impl Object {
                         }
                         let a = &i.operands;
                         if i.op == "qinplace" {
-                            self.check_qinplace_site09(f, i, &args)?;
+                            let outcome = self.check_qinplace_site09(f, i, &args)?;
+                            if let QinplaceApplicability::Unestablished(_) = outcome {
+                                let closure = self.identity()?.closure_hashes[&f.name]
+                                    .clone()
+                                    .ok_or_else(|| {
+                                        Error::new("§12.3 K92: unresolved owner".into())
+                                    })?;
+                                owners.insert(closure, outcome);
+                            }
                             let names = if a.len() == 7 {
                                 crate::object::list(&a[6])?
                             } else {
@@ -293,6 +479,6 @@ impl Object {
                 }
             }
         }
-        Ok(())
+        Ok(owners)
     }
 }
diff --git a/reference-interpreter/src/claims/replay09.rs b/reference-interpreter/src/claims/replay09.rs
index 4dc78d9..b031aab 100644
--- a/reference-interpreter/src/claims/replay09.rs
+++ b/reference-interpreter/src/claims/replay09.rs
@@ -8,7 +8,7 @@ pub(super) struct Invocation {
     pub primary: Option<crate::BudgetToken>,
     pub controls: Vec<BitVector>,
     pub adjoint: bool,
-    budget: Budget,
+    pub budget: Budget,
 }
 
 struct ResolvedDomain {
@@ -112,7 +112,6 @@ impl Object {
         }
         // Variant is an open identifier selecting a realisation. It does not
         // change the region's reference semantics or imply an adjoint.
-        let adjoint = false;
         let invocation = if let Some(invocation) = claim.object()?.get("invocation") {
             invocation
         } else {
@@ -125,6 +124,14 @@ impl Object {
             }
             bindings.get("invocation")?
         };
+        self.decode_invocation09(invocation, f)
+    }
+
+    pub(super) fn decode_invocation09(
+        &self,
+        invocation: &Json,
+        f: &Function,
+    ) -> Result<Invocation> {
         let group = if f.kind == "oracle" { 4 } else { 3 };
         let args = invocation
             .get("args")?
@@ -163,7 +170,7 @@ impl Object {
             args: resolved.arguments,
             primary: resolved.primary,
             controls: Vec::new(),
-            adjoint,
+            adjoint: false,
             budget,
         })
     }
@@ -335,16 +342,19 @@ impl Object {
         f: &Function,
     ) -> Result<Outcome> {
         if claim.get("expected")? == &Json::String("inverse_pair".into()) {
-            return err(
-                "§12.1 K4",
-                "inverse-pair claims require their entry binding",
-            );
+            return Ok(Outcome {
+                verdict: self.verify_inverse_pair_claim09(f, index, claim)?,
+                coverage: None,
+            });
         }
-        if claim.get("expected")? == &Json::String("oracle".into()) {
+        if claim
+            .get("subject")?
+            .object()?
+            .contains_key("schedule_hash")
+        {
             return Ok(Outcome {
                 verdict: ClaimVerdict::Unverified(
-                    "expected oracle needs realised target/schedule execution (deliverables 9–11)"
-                        .into(),
+                    "scheduled subject needs realised target/schedule execution".into(),
                 ),
                 coverage: None,
             });
diff --git a/reference-interpreter/src/lib.rs b/reference-interpreter/src/lib.rs
index 3d2e443..962c413 100644
--- a/reference-interpreter/src/lib.rs
+++ b/reference-interpreter/src/lib.rs
@@ -31,7 +31,10 @@ mod sha256;
 mod validation;
 pub use bits::BitVector;
 pub use borrow::validate_translation_lemma;
-pub use claims::{ClaimCoverage, ClaimReport, ClaimVerdict, FixedRegionBinding, Xoshiro256};
+pub use claims::{
+    CertificateReport, ClaimCoverage, ClaimReport, ClaimVerdict, FixedRegionBinding,
+    QinplaceApplicability, Xoshiro256,
+};
 pub use classical::{
     ClassicalMachine, ClassicalOutcome, ClassicalSnapshot, ClassicalValue, RegisterDelta,
     SnapshotDelta, StepPoint, TapeEntry,
diff --git a/reference-interpreter/src/source_constructor/action.rs b/reference-interpreter/src/source_constructor/action.rs
index 57cdd23..919c44a 100644
--- a/reference-interpreter/src/source_constructor/action.rs
+++ b/reference-interpreter/src/source_constructor/action.rs
@@ -362,7 +362,7 @@ impl Compiler<'_> {
                         env.wires.remove(&a[2]);
                     }
                 }
-                "qinplace" => out.extend(self.qinplace(i,env)?),
+                "qinplace" => out.extend(self.qinplace(i, env)?),
                 "oracle_call" | "action_call" | "ctl" | "adj" => out.extend(self.call(i, env)?),
                 _ => {
                     let mut node = if matches!(op, "rx" | "ry" | "rz") {
@@ -518,8 +518,10 @@ fn source_adjoint(body: Vec<Value>, symbols: &mut [SourceSymbol]) -> Result<Vec<
                 let Some(Value::Arr(args)) = m.get_mut("args") else {
                     return Err(Error::new("§11 K62: qinplace actuals".into()));
                 };
-                if args.len()!=6 {return Err(Error::new("§11 K62: qinplace adapter arity".into()));}
-                args.swap(3,4);
+                if args.len() != 6 {
+                    return Err(Error::new("§11 K62: qinplace adapter arity".into()));
+                }
+                args.swap(3, 4);
             } else if kind == "qloop" {
                 let Some(Value::Arr(args)) = m.get_mut("args") else {
                     return Err(Error::new("§11.1: loop body".into()));
diff --git a/reference-interpreter/src/source_constructor/action/qinplace.rs b/reference-interpreter/src/source_constructor/action/qinplace.rs
index ab214a5..60de1f3 100644
--- a/reference-interpreter/src/source_constructor/action/qinplace.rs
+++ b/reference-interpreter/src/source_constructor/action/qinplace.rs
@@ -2,22 +2,66 @@
 //! recipe owns instruction allocation/release order in both orientations.
 use super::*;
 impl Compiler<'_> {
-    pub(super) fn qinplace(&mut self,i: &crate::Instruction,env: &Env) -> Result<Vec<Value>> {
-        let a=&i.operands;
-        let n=env.width(&a[3])?;
-        let f=self.object.functions[a[0].trim_start_matches('@')].params[2][0].ty.bits(self.object.ptr_width)?;
-        let names=[format!("$qinplace/x/{}",self.counter),format!("$qinplace/t/{}",self.counter),format!("$qinplace/f/{}",self.counter)];
-        let mut bound=env.clone();bound.predicates.clear();
-        for (name,width) in names.iter().zip([n,n,f]) {bound.wires.insert(name.clone(),(name.clone(),width));}
-        let mut inputs=vec![names[0].clone()];
-        if a.len()==7 {inputs.extend(crate::object::list(&a[4])?);}
-        let mut call=i.clone();call.op="oracle_call".into();call.lhs.clear();
-        call.operands=vec![a[0].clone(),a[2].clone(),format!("({})",inputs.join(", ")),names[1].clone(),names[2].clone(),
-            a.get(5).cloned().unwrap_or_else(|| "()".into()),a.get(6).cloned().unwrap_or_else(|| "()".into())];
-        let formals=names.iter().zip([n,n,f]).map(|(name,width)| formal(name,width)).collect::<Result<Vec<_>>>()?;
-        let g=template(formals.clone(),self.call(&call,&bound)?);
-        call.operands[0]=a[1].clone();
-        let h=template(formals,self.call(&call,&bound)?);
-        Ok(vec![invoke("qinplace",[number(n)?,number(f)?,env.wire(&a[3])?,array([g]),array([h]),array(env.predicates.clone())])])
+    pub(super) fn qinplace(&mut self, i: &crate::Instruction, env: &Env) -> Result<Vec<Value>> {
+        let a = &i.operands;
+        let n = env.width(&a[3])?;
+        let f = self.object.functions[a[0].trim_start_matches('@')].params[2][0]
+            .ty
+            .bits(self.object.ptr_width)?;
+        let names = [
+            format!("$qinplace/x/{}", self.counter),
+            format!("$qinplace/t/{}", self.counter),
+            format!("$qinplace/f/{}", self.counter),
+        ];
+        let mut bound = env.clone();
+        bound.predicates.clear();
+        for (name, width) in names.iter().zip([n, n, f]) {
+            bound.wires.insert(name.clone(), (name.clone(), width));
+        }
+        // The temporary Instruction passes through the public operand-list
+        // parser. Give its private x formal a collision-free lexical alias;
+        // keep the actual constructor identity in the environment.
+        let mut input_name = format!("qinplace_x_{}", self.counter);
+        while bound.wires.contains_key(&input_name) {
+            input_name.push('_');
+        }
+        bound
+            .wires
+            .insert(input_name.clone(), (names[0].clone(), n));
+        let mut inputs = vec![input_name];
+        if a.len() == 7 {
+            inputs.extend(crate::object::list(&a[4])?);
+        }
+        let mut call = i.clone();
+        call.op = "oracle_call".into();
+        call.lhs.clear();
+        call.operands = vec![
+            a[0].clone(),
+            a[2].clone(),
+            format!("({})", inputs.join(", ")),
+            names[1].clone(),
+            names[2].clone(),
+            a.get(5).cloned().unwrap_or_else(|| "()".into()),
+            a.get(6).cloned().unwrap_or_else(|| "()".into()),
+        ];
+        let formals = names
+            .iter()
+            .zip([n, n, f])
+            .map(|(name, width)| formal(name, width))
+            .collect::<Result<Vec<_>>>()?;
+        let g = template(formals.clone(), self.call(&call, &bound)?);
+        call.operands[0] = a[1].clone();
+        let h = template(formals, self.call(&call, &bound)?);
+        Ok(vec![invoke(
+            "qinplace",
+            [
+                number(n)?,
+                number(f)?,
+                env.wire(&a[3])?,
+                array([g]),
+                array([h]),
+                array(env.predicates.clone()),
+            ],
+        )])
     }
 }
diff --git a/reference-interpreter/tests/isa09_certificate.rs b/reference-interpreter/tests/isa09_certificate.rs
index 8c7f437..fbad194 100644
--- a/reference-interpreter/tests/isa09_certificate.rs
+++ b/reference-interpreter/tests/isa09_certificate.rs
@@ -120,3 +120,77 @@ fn a_data_root_certificate_is_a_diagnostic_and_never_a_panic() {
     assert!(result.is_ok(), "untrusted certificate data root panicked");
     assert!(result.unwrap().is_err());
 }
+
+// K13: a schedule subject denotes the realised operation for every relation.
+#[test]
+fn scheduled_table_and_program_claims_never_prove_reference_only_replay() {
+    use bennett_isa_ref::ClaimVerdict;
+    let source = include_str!("../../conformance/fixtures/accepted-k91-09/pair-distinct.bisa");
+    let object = Object::parse(source).unwrap();
+    let root = object.identity().unwrap().closure_hashes["pair"]
+        .clone()
+        .unwrap();
+    for relation in ["table", "program", "oracle"] {
+        let mut c = object.section("certificate").unwrap().clone();
+        let schedule = c
+            .get("bindings")
+            .unwrap()
+            .get("schedule_hash")
+            .unwrap()
+            .clone();
+        let cl = claim(&mut c);
+        fields(fields(cl).get_mut("subject").unwrap()).insert("schedule_hash".into(), schedule);
+        match relation {
+            "program" => {
+                fields(cl).insert(
+                    "expected".into(),
+                    support::json(&format!(r#"{{"program":"{root}"}}"#)),
+                );
+            }
+            "oracle" => {
+                fields(cl).insert("expected".into(), Json::String("oracle".into()));
+            }
+            _ => {}
+        }
+        let o = Object::parse(&replace(source, "certificate", Some(&c))).unwrap();
+        assert!(
+            matches!(
+                o.verify_claim(&root, 0).unwrap(),
+                ClaimVerdict::Unverified(_)
+            ),
+            "{relation}"
+        );
+        let reports = o.verify_certificate().unwrap().claims;
+        assert!(
+            matches!(reports[0].verdict, ClaimVerdict::Unverified(_)),
+            "{relation}"
+        );
+        assert!(reports[0].coverage.is_none());
+
+        // A syntactically valid hash must resolve to this object's schedule.
+        fields(fields(claim(&mut c)).get_mut("subject").unwrap())
+            .insert("schedule_hash".into(), Json::String("ab".repeat(32)));
+        let error = Object::parse(&replace(source, "certificate", Some(&c))).unwrap_err();
+        assert!(error.to_string().contains("schedule"), "{error}");
+    }
+}
+
+#[test]
+fn claim_schedule_hash_requires_a_present_matching_schedule() {
+    let source = include_str!("../../conformance/fixtures/accepted-k91-09/pair-distinct.bisa");
+    let object = Object::parse(source).unwrap();
+    let mut c = object.section("certificate").unwrap().clone();
+    let hash = c
+        .get("bindings")
+        .unwrap()
+        .get("schedule_hash")
+        .unwrap()
+        .clone();
+    fields(fields(claim(&mut c)).get_mut("subject").unwrap()).insert("schedule_hash".into(), hash);
+    let missing = replace(&replace(source, "schedule", None), "certificate", Some(&c));
+    let error = Object::parse(&missing).unwrap_err();
+    assert!(
+        error.to_string().contains("claim schedule is absent"),
+        "{error}"
+    );
+}
diff --git a/reference-interpreter/tests/isa09_claim_replay.rs b/reference-interpreter/tests/isa09_claim_replay.rs
index f4f0e6e..767e4b4 100644
--- a/reference-interpreter/tests/isa09_claim_replay.rs
+++ b/reference-interpreter/tests/isa09_claim_replay.rs
@@ -171,12 +171,70 @@ fn standalone_oracle_binds_its_own_argument_budget_and_complete_interface() {
     }
 }
 #[test]
-fn published_full_tuple_tables_verify_as_proof() {
+fn published_full_tuple_tables_prove_only_the_bound_reference_relation() {
     for source in [BASE, CONTROLLED] {
-        assert_eq!(
-            verify_root(&Object::parse(source).unwrap()).unwrap(),
-            ClaimVerdict::Proof
-        );
+        let object = Object::parse(source).unwrap();
+        let certificate = object.section("certificate").unwrap();
+        let root = certificate
+            .get("bindings")
+            .unwrap()
+            .get("closure_hash")
+            .unwrap()
+            .string()
+            .unwrap();
+        let claim = &certificate
+            .get("regions")
+            .unwrap()
+            .get(root)
+            .unwrap()
+            .get("claims")
+            .unwrap()
+            .array()
+            .unwrap()[0];
+        if claim
+            .get("subject")
+            .unwrap()
+            .object()
+            .unwrap()
+            .contains_key("schedule_hash")
+        {
+            assert!(matches!(
+                verify_root(&object).unwrap(),
+                ClaimVerdict::Unverified(_)
+            ));
+            let root_report = |o: &Object| {
+                o.verify_certificate()
+                    .unwrap()
+                    .claims
+                    .into_iter()
+                    .find(|r| r.closure_hash == root && r.index == 0)
+                    .unwrap()
+            };
+            assert!(matches!(
+                root_report(&object).verdict,
+                ClaimVerdict::Unverified(_)
+            ));
+            // Keep the published table as a full reference-semantic oracle,
+            // without misrepresenting it as execution of its realisation.
+            let invocation = certificate
+                .get("bindings")
+                .unwrap()
+                .get("invocation")
+                .unwrap()
+                .clone();
+            let reference = changed(source, |claim| {
+                fields(fields(claim).get_mut("subject").unwrap()).remove("schedule_hash");
+                fields(claim).insert("invocation".into(), invocation);
+            });
+            assert_eq!(verify_root(&reference).unwrap(), ClaimVerdict::Proof);
+            assert_eq!(root_report(&reference).verdict, ClaimVerdict::Proof);
+            assert_eq!(
+                reference.identity().unwrap().object_hash,
+                object.identity().unwrap().object_hash
+            );
+        } else {
+            assert_eq!(verify_root(&object).unwrap(), ClaimVerdict::Proof);
+        }
     }
 }
 #[test]
@@ -348,7 +406,7 @@ fn fixed_image_metadata_is_admitted_without_inspecting_quantum_state() {
         verify_root(&object).unwrap(),
         ClaimVerdict::ProofRelativeToImage
     );
-    let report = object.verify_certificate().unwrap().remove(0);
+    let report = object.verify_certificate().unwrap().claims.remove(0);
     let coverage = report.coverage.unwrap();
     assert_eq!(
         (
@@ -414,7 +472,7 @@ fn sampled_singleton_report_has_exact_distinct_coverage() {
             support::json(r#"{"algorithm":"xoshiro256**","seed":["1","0","0","0"],"count":4}"#),
         );
     });
-    let report = object.verify_certificate().unwrap().remove(0);
+    let report = object.verify_certificate().unwrap().claims.remove(0);
     assert_eq!(report.verdict, ClaimVerdict::Evidence { elements: 1 });
     let coverage = report.coverage.unwrap();
     assert_eq!(coverage.covered_fraction, "1/33554432");
diff --git a/reference-interpreter/tests/isa09_forwarding.rs b/reference-interpreter/tests/isa09_forwarding.rs
index aed269d..a648f3e 100644
--- a/reference-interpreter/tests/isa09_forwarding.rs
+++ b/reference-interpreter/tests/isa09_forwarding.rs
@@ -196,10 +196,20 @@ fn source_object(ptr: usize) -> Object {
 }
 
 #[test]
+fn source_forwarding_bounded_materialisation_reports_host_capacity() {
+    source_forwarding_materialisation_limit(3, Some(1_024));
+}
+
+#[test]
+#[ignore = "slow-source-forwarding: million-leaf capacity witness; run only under an 8 GiB memory cap"]
 fn source_forwarding_large_materialisation_reports_host_capacity_before_exhausting_memory() {
+    source_forwarding_materialisation_limit(32, None);
+}
+
+fn source_forwarding_materialisation_limit(ptr: usize, leaf_limit: Option<usize>) {
     use bennett_isa_conformance::json;
     use bennett_isa_ref::ref_library::OracleInvocation;
-    let o = source_object(32);
+    let o = source_object(ptr);
     let args=json::parse(r#"["x","t","f",{"address":0,"cell":8,"role":"in","origin":"interface:db","cells":"db"},["6","0","0","0"],"2"]"#).unwrap();
     let context = json::parse(r#"{"token":["8","0","8","1"]}"#).unwrap();
     let call = OracleInvocation::capture_with_token_aliases(
@@ -211,12 +221,13 @@ fn source_forwarding_large_materialisation_reports_host_capacity_before_exhausti
         &[0, 1],
     )
     .unwrap();
-    let error = call
-        .expand_source(
-            &o.bound_ref_library().unwrap(),
-            &[("x", 2), ("t", 2), ("f", 4), ("db", 8)],
-        )
-        .unwrap_err();
+    let library = o.bound_ref_library().unwrap();
+    let bundles = &[("x", 2), ("t", 2), ("f", 4), ("db", 8)];
+    let error = match leaf_limit {
+        Some(limit) => call.expand_source_with_leaf_limit(&library, bundles, limit),
+        None => call.expand_source(&library, bundles),
+    }
+    .unwrap_err();
     assert_eq!(error.kind(), bennett_isa_ref::ErrorKind::HostResource);
     assert!(error.to_string().contains("materialised leaf budget"));
 }
diff --git a/reference-interpreter/tests/isa09_qinplace.rs b/reference-interpreter/tests/isa09_qinplace.rs
index 5daba4f..d44e8aa 100644
--- a/reference-interpreter/tests/isa09_qinplace.rs
+++ b/reference-interpreter/tests/isa09_qinplace.rs
@@ -106,6 +106,16 @@ fn inverse_certificate_for(object: &Object) -> String {
         "signature".into(),
         object.functions["addya"].signature_for(object.isa_version),
     );
+    fields(&mut record).insert(
+        "bounds".into(),
+        Json::Array(
+            object.functions["addya"]
+                .bounds
+                .iter()
+                .map(|n| Json::Number(n.to_string()))
+                .collect(),
+        ),
+    );
     fields(&mut record).insert("frame".into(),support::json(r#"{"slots":[{"id":"mut:0","role":"mut","class":"any","width":2},{"id":"in:0","role":"in","class":"any","width":2}],"scratch":[],"history":[],"borrow":[],"ancillae":[]}"#));
     fields(&mut record).insert("resources".into(), support::json("{}"));
     fields(&mut record).insert("gates_used".into(), support::json("{}"));
@@ -141,6 +151,38 @@ fn k4_inverse_pair_claim_binds_its_entry_and_quantified_arguments() {
         object.verify_claim(&closure, 0).unwrap(),
         bennett_isa_ref::ClaimVerdict::Proof
     );
+
+    let reports = object.verify_certificate().unwrap().claims;
+    assert_eq!(reports.len(), 1);
+    assert_eq!(reports[0].verdict, bennett_isa_ref::ClaimVerdict::Proof);
+    assert!(reports[0].coverage.is_none());
+}
+
+#[test]
+fn inverse_pair_certificate_rejects_a_noninverse_and_an_unbound_claim() {
+    let object = Object::parse(&inverse_certificate()).unwrap();
+    let identity = object.identity().unwrap();
+    let gi = identity.closure_hashes["ginv"].as_ref().unwrap();
+    let g = identity.closure_hashes["g"].as_ref().unwrap();
+    let original = inverse_certificate();
+    let wrong = original.replace(&format!(r#""ginv":"{gi}""#), &format!(r#""ginv":"{g}""#));
+    assert_ne!(wrong, original);
+    let wrong = Object::parse(&wrong).unwrap();
+    let owner = identity.closure_hashes["addya"].as_ref().unwrap();
+    let error = wrong.verify_claim(owner, 0).unwrap_err();
+    assert!(error.to_string().contains("differs from x"), "{error}");
+    let error = wrong.verify_certificate().unwrap_err();
+    assert!(error.to_string().contains("missing owner-local"), "{error}");
+    let no_entry = original.replace(
+        &format!(r#"[{{"budget":[3,0,0,0],"claim":0,"g":"{g}","ginv":"{gi}"}}]"#),
+        "[]",
+    );
+    assert_ne!(no_entry, original);
+    let error = Object::parse(&no_entry).unwrap_err();
+    assert!(
+        error.to_string().contains("owner-local entry binding"),
+        "{error}"
+    );
 }
 
 #[test]
@@ -275,27 +317,647 @@ fn uncovered_pair_rejects_before_the_earliest_effect_of_the_region() {
     }
 }
 
-
 #[test]
 fn source_qinplace_adjoints_preserve_instruction_allocation_and_release_order() {
-    use bennett_isa_conformance::{json,ref_catalog::Machine,ref_language::permutation};
-    let object=Object::parse(&inverse_certificate()).unwrap();
-    let root=object.identity().unwrap().closure_hashes["addya"].clone().unwrap();
-    let args=json::parse(r#"["x","y",["3","0","0","0"],"1"]"#).unwrap();
-    for adjoint in [false,true] {
-        let leaves=object.expand_action_source_with_token_aliases("addya",args.as_arr().unwrap(),&[("x",2),("y",2)],adjoint,&[0]).unwrap();
-        let own=leaves.iter().filter(|l| l.source.as_ref().is_some_and(|s| s.terminal.symbol==root)).collect::<Vec<_>>();
-        let allocation=own.iter().filter(|l| l.gate=="alloc").map(|l| l.allocation.as_ref().unwrap().1).collect::<Vec<_>>();
-        let release=own.iter().filter(|l| l.gate=="release").map(|l| l.allocation.as_ref().unwrap().1).collect::<Vec<_>>();
-        assert_eq!(allocation,[2,4],"adjoint={adjoint}");
-        assert_eq!(release,[2,4],"adjoint={adjoint}");
-        let machine=Machine::compile(&permutation(&leaves).unwrap(),&[("x",2),("y",2)]).unwrap();
-        for x in 0..4 {for y in 0..4 {
-            let mut state=machine.state();machine.set(&mut state,"x",x);machine.set(&mut state,"y",y);let before=state.clone();
-            machine.run(&mut state,true,false).unwrap();
-            assert_eq!(machine.get(&state,"x"),if adjoint {(x+8-y-1)&3}else{(x+y+1)&3});
-            assert_eq!(machine.get(&state,"y"),y);
-            machine.run(&mut state,true,true).unwrap();assert_eq!(state,before);
-        }}
+    use bennett_isa_conformance::{json, ref_catalog::Machine, ref_language::permutation};
+    let object = Object::parse(&inverse_certificate()).unwrap();
+    let root = object.identity().unwrap().closure_hashes["addya"]
+        .clone()
+        .unwrap();
+    let args = json::parse(r#"["x","y",["3","0","0","0"],"1"]"#).unwrap();
+    for adjoint in [false, true] {
+        let leaves = object
+            .expand_action_source_with_token_aliases(
+                "addya",
+                args.as_arr().unwrap(),
+                &[("x", 2), ("y", 2)],
+                adjoint,
+                &[0],
+            )
+            .unwrap();
+        let own = leaves
+            .iter()
+            .filter(|l| l.source.as_ref().is_some_and(|s| s.terminal.symbol == root))
+            .collect::<Vec<_>>();
+        let allocation = own
+            .iter()
+            .filter(|l| l.gate == "alloc")
+            .map(|l| l.allocation.as_ref().unwrap().1)
+            .collect::<Vec<_>>();
+        let release = own
+            .iter()
+            .filter(|l| l.gate == "release")
+            .map(|l| l.allocation.as_ref().unwrap().1)
+            .collect::<Vec<_>>();
+        assert_eq!(allocation, [2, 4], "adjoint={adjoint}");
+        assert_eq!(release, [2, 4], "adjoint={adjoint}");
+        let machine =
+            Machine::compile(&permutation(&leaves).unwrap(), &[("x", 2), ("y", 2)]).unwrap();
+        for x in 0..4 {
+            for y in 0..4 {
+                let mut state = machine.state();
+                machine.set(&mut state, "x", x);
+                machine.set(&mut state, "y", y);
+                let before = state.clone();
+                machine.run(&mut state, true, false).unwrap();
+                assert_eq!(
+                    machine.get(&state, "x"),
+                    if adjoint {
+                        (x + 8 - y - 1) & 3
+                    } else {
+                        (x + y + 1) & 3
+                    }
+                );
+                assert_eq!(machine.get(&state, "y"), y);
+                machine.run(&mut state, true, true).unwrap();
+                assert_eq!(state, before);
+            }
+        }
     }
 }
+
+fn change_certificate(text: &str, change: impl FnOnce(&mut bennett_isa_ref::json::Json)) -> String {
+    let (source, packet) = text.split_once("section certificate\n").unwrap();
+    let mut certificate = bennett_isa_ref::json::Json::parse(packet.trim()).unwrap();
+    change(&mut certificate);
+    format!("{source}section certificate\n{}\n", certificate.canonical())
+}
+fn root_invocation(steps: u64, a: u64) -> bennett_isa_ref::json::Json {
+    support::json(&format!(
+        r#"{{"args":[["{steps}","0","0","0"],"{a}"],"budget":["0","0","0","0"],"token_aliases":[0]}}"#
+    ))
+}
+fn linked_inverse_certificate(wrong_pair: bool) -> String {
+    let text = inverse_certificate();
+    let object = Object::parse(&text).unwrap();
+    let identity = object.identity().unwrap();
+    let owner = identity.closure_hashes["addya"].as_ref().unwrap();
+    let g = identity.closure_hashes["g"].as_ref().unwrap();
+    change_certificate(&text, |certificate| {
+        let regions = fields(fields(certificate).get_mut("regions").unwrap());
+        let mut donor = regions[owner].clone();
+        fields(&mut donor).insert("kind".into(), support::json("\"oracle\""));
+        fields(&mut donor).insert("bounds".into(), support::json("[]"));
+        fields(&mut donor).insert(
+            "signature".into(),
+            object.functions["g"].signature_for(object.isa_version),
+        );
+        fields(&mut donor).insert("frame".into(), support::json(r#"{"slots":[{"id":"in:0","role":"in","class":"any","width":2},{"id":"in:1","role":"in","class":"any","width":2},{"id":"tgt:0","role":"tgt","class":"any","width":2},{"id":"fault:0","role":"fault","class":"any","width":4}],"scratch":[],"history":[],"borrow":[],"ancillae":[]}"#));
+        let record = fields(regions.get_mut(owner).unwrap());
+        record.insert("claims".into(), support::json(&format!(r#"[{{"kind":"structural","rule":"inverse_pair_library","subclaims":[],"witness":{{"library_closure_hash":"{g}","claim_index":0}},"invocation":{}}}]"#, root_invocation(3,1).canonical())));
+        if wrong_pair {
+            let entries = fields(record.get_mut("verification").unwrap())
+                .get_mut("inverse_pairs")
+                .unwrap();
+            let bennett_isa_ref::json::Json::Array(entries) = entries else {
+                panic!("entries")
+            };
+            fields(&mut entries[0]).insert(
+                "ginv".into(),
+                bennett_isa_ref::json::Json::String(g.clone()),
+            );
+        }
+        regions.insert(g.clone(), donor);
+    })
+}
+#[test]
+fn checker_rejects_missing_owner_local_qinplace_inventory() {
+    let text = change_certificate(&inverse_certificate(), |c| {
+        let record = fields(fields(c).get_mut("regions").unwrap())
+            .values_mut()
+            .next()
+            .unwrap();
+        fields(record).insert("claims".into(), support::json("[]"));
+        fields(fields(record).get_mut("verification").unwrap())
+            .insert("inverse_pairs".into(), support::json("[]"));
+    });
+    let error = Object::parse(&text)
+        .unwrap()
+        .verify_certificate()
+        .unwrap_err();
+    assert!(error.to_string().contains("K92"), "{error}");
+}
+#[test]
+fn checker_rejects_bound_invocation_below_the_pair_minimum() {
+    let text = change_certificate(&inverse_certificate(), |c| {
+        fields(fields(c).get_mut("bindings").unwrap())
+            .insert("invocation".into(), root_invocation(2, 1));
+    });
+    let error = Object::parse(&text)
+        .unwrap()
+        .verify_certificate()
+        .unwrap_err();
+    assert!(
+        error.to_string().contains("no covering inverse-pair entry"),
+        "{error}"
+    );
+}
+#[test]
+fn standalone_pair_proof_reports_unestablished_applicability() {
+    let reports = Object::parse(&inverse_certificate())
+        .unwrap()
+        .verify_certificate()
+        .unwrap()
+        .claims;
+    assert_eq!(reports[0].verdict, bennett_isa_ref::ClaimVerdict::Proof);
+    assert!(
+        matches!(
+            reports[0].qinplace_applicability,
+            Some(bennett_isa_ref::QinplaceApplicability::Unestablished(_))
+        ),
+        "{reports:?}"
+    );
+}
+#[test]
+fn library_proof_cannot_transfer_to_a_different_pair() {
+    let object = Object::parse(&linked_inverse_certificate(true)).unwrap();
+    let owner = object.identity().unwrap().closure_hashes["addya"]
+        .clone()
+        .unwrap();
+    // g(x;y,a)=x+y+a mod 4: g(g(0;0,1);0,1)=2, so g/g is not inverse.
+    let error = object.verify_claim(&owner, 0).unwrap_err();
+    assert!(error.to_string().contains("same resolved pair"), "{error}");
+    let error = object.verify_certificate().unwrap_err();
+    assert!(error.to_string().contains("K92"), "{error}");
+}
+#[test]
+fn linked_library_pair_executes_every_argument_and_adjoint() {
+    use bennett_isa_ref::{Argument, Budget, ClaimVerdict};
+    let object = Object::parse(&linked_inverse_certificate(false)).unwrap();
+    let owner = object.identity().unwrap().closure_hashes["addya"]
+        .clone()
+        .unwrap();
+    assert_eq!(object.verify_claim(&owner, 0).unwrap(), ClaimVerdict::Proof);
+    for steps in [3, 9] {
+        for x in 0..4 {
+            for y in 0..4 {
+                for a in 0..4 {
+                    let (mut q, mut b, wires) = quantum_input(x, y);
+                    b.args
+                        .insert("tk".into(), Argument::Token(Budget::steps(steps)));
+                    b.args.insert("a".into(), Argument::Bits(a));
+                    let before = q.clone();
+                    object
+                        .execute_action_with_token_aliases("addya", &mut q, &b, false, &[], &[0])
+                        .unwrap();
+                    assert_eq!(q.read_basis(&wires).unwrap(), ((x + y + a) & 3) | (y << 2));
+                    object
+                        .execute_action_with_token_aliases("addya", &mut q, &b, true, &[], &[0])
+                        .unwrap();
+                    assert_eq!(q, before);
+                }
+            }
+        }
+    }
+}
+
+fn loop_certificate(iterations: usize) -> String {
+    let text = published_source()
+        .replace("\"bounds\":[]", &format!("\"bounds\":[{iterations}]"))
+        .replace(
+            "(tk:token, a:i2) ()\n^entry():",
+            &format!("(tk:token, a:i2) ()\nregs {{  }} bounds {{{iterations}}}\n^entry():"),
+        )
+        .replace(
+            "qinplace @g @ginv tk x (y) () (a)",
+            &format!("qloop {iterations} {{\nqinplace @g @ginv tk x (y) () (a)\n}}"),
+        )
+        + "\n";
+    inverse_certificate_for(&support::rehash(&text))
+}
+#[test]
+fn zero_trip_qinplace_requires_inventory_but_has_no_applicability_visit() {
+    let text = loop_certificate(0);
+    let bound = change_certificate(&text, |c| {
+        fields(fields(c).get_mut("bindings").unwrap())
+            .insert("invocation".into(), root_invocation(2, 1));
+    });
+    let reports = Object::parse(&bound)
+        .unwrap()
+        .verify_certificate()
+        .unwrap()
+        .claims;
+    assert_eq!(
+        reports[0].qinplace_applicability,
+        Some(bennett_isa_ref::QinplaceApplicability::Established)
+    );
+    let missing = change_certificate(&bound, |c| {
+        let record = fields(fields(c).get_mut("regions").unwrap())
+            .values_mut()
+            .next()
+            .unwrap();
+        fields(record).insert("claims".into(), support::json("[]"));
+        fields(fields(record).get_mut("verification").unwrap())
+            .insert("inverse_pairs".into(), support::json("[]"));
+    });
+    let error = Object::parse(&missing)
+        .unwrap()
+        .verify_certificate()
+        .unwrap_err();
+    assert!(error.to_string().contains("K92"), "{error}");
+}
+#[test]
+fn nested_qinplace_below_minimum_rejects_in_checker_and_before_execution() {
+    use bennett_isa_ref::{Argument, Budget};
+    let text = change_certificate(&loop_certificate(1), |c| {
+        fields(fields(c).get_mut("bindings").unwrap())
+            .insert("invocation".into(), root_invocation(2, 1));
+    });
+    let object = Object::parse(&text).unwrap();
+    let error = object.verify_certificate().unwrap_err();
+    assert!(
+        error.to_string().contains("no covering inverse-pair entry"),
+        "{error}"
+    );
+    let (mut q, mut b, _) = quantum_input(0, 0);
+    b.args
+        .insert("tk".into(), Argument::Token(Budget::steps(2)));
+    b.args.insert("a".into(), Argument::Bits(1));
+    let before = q.clone();
+    let error = object
+        .execute_action_with_token_aliases("addya", &mut q, &b, false, &[], &[0])
+        .unwrap_err();
+    assert!(
+        error.to_string().contains("no covering inverse-pair entry"),
+        "{error}"
+    );
+    assert_eq!(q, before);
+}
+#[test]
+fn library_reuse_preserves_the_proved_minimum_and_argument_domain() {
+    let text = linked_inverse_certificate(false);
+    let object = Object::parse(&text).unwrap();
+    let owner = object.identity().unwrap().closure_hashes["addya"]
+        .clone()
+        .unwrap();
+    let too_small = change_certificate(&text, |c| {
+        let record = fields(fields(c).get_mut("regions").unwrap())
+            .get_mut(&owner)
+            .unwrap();
+        let entries = fields(fields(record).get_mut("verification").unwrap())
+            .get_mut("inverse_pairs")
+            .unwrap();
+        let bennett_isa_ref::json::Json::Array(entries) = entries else {
+            panic!("entries")
+        };
+        fields(&mut entries[0]).insert("budget".into(), support::json("[2,0,0,0]"));
+    });
+    let error = Object::parse(&too_small)
+        .unwrap()
+        .verify_claim(&owner, 0)
+        .unwrap_err();
+    assert!(error.to_string().contains("token context"), "{error}");
+    let scoped = text.replace(
+        "\"hi\":3,\"lo\":0,\"name\":\"a\"",
+        "\"hi\":2,\"lo\":0,\"name\":\"a\"",
+    );
+    assert_ne!(scoped, text);
+    let uncovered = change_certificate(&scoped, |c| {
+        fields(fields(c).get_mut("bindings").unwrap())
+            .insert("invocation".into(), root_invocation(3, 3));
+    });
+    let error = Object::parse(&uncovered)
+        .unwrap()
+        .verify_certificate()
+        .unwrap_err();
+    assert!(
+        error.to_string().contains("no covering inverse-pair entry"),
+        "{error}"
+    );
+}
+
+fn transitive_certificate(include_inner: bool) -> String {
+    use bennett_isa_ref::json::Json;
+    let original = Object::parse(&(published_source().to_string() + "\n")).unwrap();
+    let mut symbols = original.section("symbols").unwrap().clone();
+    let mut inner = fields(&mut symbols)["2"].clone();
+    fields(&mut inner).insert("name".into(), Json::String("inner".into()));
+    fields(&mut symbols).insert("4".into(), inner);
+    let mut lines = original
+        .text
+        .lines()
+        .map(str::to_string)
+        .collect::<Vec<_>>();
+    let i = lines.iter().position(|s| s == "section symbols").unwrap() + 1;
+    lines[i] = symbols.canonical();
+    let source = (lines.join("\n")+"\n").replace("qinplace @g @ginv tk x (y) () (a)", "action_call @inner (x) (y) () (tk, a)")
+        + "perm_action @inner (x:wire[2]) (y:wire[2] in) () (tk:token, a:i2) ()\n^entry():\nqinplace @g @ginv tk x (y) () (a)\n";
+    let object = support::rehash(&source);
+    let text = inverse_certificate_for(&object);
+    change_certificate(&text, |c| {
+        if include_inner {
+            let hash = object.identity().unwrap().closure_hashes["inner"]
+                .clone()
+                .unwrap();
+            let regions = fields(fields(c).get_mut("regions").unwrap());
+            let record = regions.values().next().unwrap().clone();
+            regions.insert(hash, record);
+        }
+    })
+}
+#[test]
+fn bound_reference_tree_checks_transitive_owner_and_actual_arguments() {
+    for (include_inner, steps) in [(false, 3), (true, 2), (true, 3), (true, 9)] {
+        let text = change_certificate(&transitive_certificate(include_inner), |c| {
+            fields(fields(c).get_mut("bindings").unwrap())
+                .insert("invocation".into(), root_invocation(steps, 1));
+        });
+        let result = Object::parse(&text).unwrap().verify_certificate();
+        if include_inner && steps >= 3 {
+            let reports = result.unwrap().claims;
+            let inner = reports.iter().find(|r| r.region == "inner").unwrap();
+            assert_eq!(
+                inner.qinplace_applicability,
+                Some(bennett_isa_ref::QinplaceApplicability::Established)
+            );
+        } else {
+            let error = result.unwrap_err();
+            assert!(
+                error
+                    .to_string()
+                    .contains("no covering inverse-pair entry in @inner"),
+                "{error}"
+            );
+        }
+    }
+}
+#[test]
+fn disabled_coherent_predicate_keeps_the_qinplace_obligation() {
+    let source = published_source().replace("qinplace @g @ginv tk x (y) () (a)", "c = qalloc any 1\nqif c {\nqinplace @g @ginv tk x (y) () (a)\n} {\nx x[0]\nx x[0]\n}\nqfree c") + "\n";
+    let text = change_certificate(&inverse_certificate_for(&support::rehash(&source)), |c| {
+        fields(fields(c).get_mut("bindings").unwrap())
+            .insert("invocation".into(), root_invocation(2, 1));
+    });
+    let error = Object::parse(&text)
+        .unwrap()
+        .verify_certificate()
+        .unwrap_err();
+    assert!(
+        error.to_string().contains("no covering inverse-pair entry"),
+        "{error}"
+    );
+}
+
+#[test]
+fn missing_library_body_reports_unestablished_and_cannot_execute() {
+    use bennett_isa_ref::{Argument, Budget, ClaimVerdict, QinplaceApplicability};
+    let text = linked_inverse_certificate(false);
+    let object = Object::parse(&text).unwrap();
+    let g = object.identity().unwrap().closure_hashes["g"]
+        .clone()
+        .unwrap();
+    let text = change_certificate(&text, |c| {
+        fields(fields(c).get_mut("regions").unwrap()).remove(&g);
+    });
+    let object = Object::parse(&text).unwrap();
+    let report = object.verify_certificate().unwrap().claims.remove(0);
+    assert!(
+        matches!(report.verdict, ClaimVerdict::Unverified(_)),
+        "{report:?}"
+    );
+    assert!(
+        matches!(
+            report.qinplace_applicability,
+            Some(QinplaceApplicability::Unestablished(_))
+        ),
+        "{report:?}"
+    );
+    let (mut q, mut b, _) = quantum_input(0, 0);
+    b.args
+        .insert("tk".into(), Argument::Token(Budget::steps(3)));
+    b.args.insert("a".into(), Argument::Bits(1));
+    let before = q.clone();
+    let error = object
+        .execute_action_with_token_aliases("addya", &mut q, &b, false, &[], &[0])
+        .unwrap_err();
+    assert!(
+        error
+            .to_string()
+            .contains("unestablished qinplace applicability"),
+        "{error}"
+    );
+    assert_eq!(q, before);
+}
+
+enum CertificateContents {
+    PairClaim,
+    EmptyClaims,
+    EmptyRecords,
+}
+
+fn unsupported_bound_root_certificate(contents: CertificateContents) -> String {
+    use bennett_isa_ref::json::Json;
+    let text = transitive_certificate(false);
+    let identity = Object::parse(&text).unwrap().identity().unwrap();
+    change_certificate(&text, |c| {
+        let bindings = fields(fields(c).get_mut("bindings").unwrap());
+        for (key, value) in [
+            (
+                "closure_hash",
+                identity.closure_hashes["run"].as_ref().unwrap(),
+            ),
+            (
+                "reference_program_hash",
+                identity.closure_hashes["run"].as_ref().unwrap(),
+            ),
+            ("interface_hash", &identity.interface_hashes["run"]),
+        ] {
+            bindings.insert(key.into(), Json::String(value.clone()));
+        }
+        bindings.insert("invocation".into(), root_invocation(2, 1));
+        let regions = fields(fields(c).get_mut("regions").unwrap());
+        match contents {
+            CertificateContents::PairClaim => {}
+            CertificateContents::EmptyRecords => regions.clear(),
+            CertificateContents::EmptyClaims => {
+                for record in regions.values_mut() {
+                    fields(record).insert("claims".into(), support::json("[]"));
+                    fields(fields(record).get_mut("verification").unwrap())
+                        .insert("inverse_pairs".into(), support::json("[]"));
+                }
+            }
+        }
+    })
+}
+
+#[test]
+fn unsupported_bound_root_keeps_applicability_without_direct_owner() {
+    use bennett_isa_ref::{ClaimVerdict, QinplaceApplicability};
+    let object = Object::parse(&unsupported_bound_root_certificate(
+        CertificateContents::PairClaim,
+    ))
+    .unwrap();
+    let identity = object.identity().unwrap();
+    let owner = identity.closure_hashes["addya"].as_ref().unwrap();
+    let root = identity.closure_hashes["run"].as_ref().unwrap();
+    let report = object.verify_certificate().unwrap();
+    assert_eq!(report.claims.len(), 1);
+    assert_eq!(report.claims[0].verdict, ClaimVerdict::Proof);
+    assert_eq!(object.verify_claim(owner, 0).unwrap(), ClaimVerdict::Proof);
+    assert_eq!(report.qinplace_applicability.len(), 1);
+    assert!(
+        matches!(report.qinplace_applicability.get(root), Some(QinplaceApplicability::Unestablished(reason)) if reason.contains("bound @run")),
+        "{report:?}"
+    );
+}
+
+#[test]
+fn unsupported_bound_root_keeps_applicability_without_claims() {
+    let object = Object::parse(&unsupported_bound_root_certificate(
+        CertificateContents::EmptyClaims,
+    ))
+    .unwrap();
+    let root = object.identity().unwrap().closure_hashes["run"]
+        .clone()
+        .unwrap();
+    let report = object.verify_certificate().unwrap();
+    assert!(report.claims.is_empty(), "{report:?}");
+    assert!(
+        matches!(report.qinplace_applicability.get(&root), Some(bennett_isa_ref::QinplaceApplicability::Unestablished(reason)) if reason.contains("bound @run")),
+        "{report:?}"
+    );
+}
+
+#[test]
+fn unsupported_bound_root_keeps_applicability_without_records() {
+    let object = Object::parse(&unsupported_bound_root_certificate(
+        CertificateContents::EmptyRecords,
+    ))
+    .unwrap();
+    let root = object.identity().unwrap().closure_hashes["run"]
+        .clone()
+        .unwrap();
+    let report = object.verify_certificate().unwrap();
+    assert!(report.claims.is_empty(), "{report:?}");
+    assert!(
+        matches!(report.qinplace_applicability.get(&root), Some(bennett_isa_ref::QinplaceApplicability::Unestablished(reason)) if reason.contains("bound @run")),
+        "{report:?}"
+    );
+}
+
+#[test]
+fn uncheckable_uniform_transitive_claim_keeps_applicability() {
+    // The outer caller has no local site; universal transitive coverage is
+    // separate from the structural theorem.
+    let source = transitive_certificate(false);
+    let owner = Object::parse(&source)
+        .unwrap()
+        .identity()
+        .unwrap()
+        .closure_hashes["addya"]
+        .clone()
+        .unwrap();
+    let text = change_certificate(&source, |c| {
+        let record = fields(fields(c).get_mut("regions").unwrap())
+            .get_mut(&owner)
+            .unwrap();
+        fields(record).insert("claims".into(), support::json(r#"[{"kind":"structural","rule":"adjoint_table","subclaims":[],"witness":{},"invocation":{"args":"all","budget":"all","token_aliases":"all"}}]"#));
+        fields(fields(record).get_mut("verification").unwrap())
+            .insert("inverse_pairs".into(), support::json("[]"));
+    });
+    let report = Object::parse(&text).unwrap().verify_certificate().unwrap();
+    assert_eq!(report.claims.len(), 1);
+    assert!(
+        matches!(report.qinplace_applicability.get(&owner), Some(bennett_isa_ref::QinplaceApplicability::Unestablished(reason)) if reason.contains("parameter-uniform")),
+        "{report:?}"
+    );
+}
+
+#[test]
+fn scheduled_root_keeps_unchecked_tree_obligation_without_owners_or_claims() {
+    use bennett_isa_ref::{json::Json, sha256_hex, QinplaceApplicability};
+    let text = transitive_certificate(false);
+    let original = Object::parse(&text).unwrap();
+    let mut symbols = original.section("symbols").unwrap().clone();
+    fields(
+        fields(fields(&mut symbols).get_mut("2").unwrap())
+            .get_mut("signature")
+            .unwrap(),
+    )
+    .insert("bounds".into(), support::json("[0]"));
+    let mut lines = text.lines().map(str::to_string).collect::<Vec<_>>();
+    let index = lines
+        .iter()
+        .position(|line| line == "section symbols")
+        .unwrap()
+        + 1;
+    lines[index] = symbols.canonical();
+    let text = lines.join("\n");
+    let source = text.split_once("section certificate\n").unwrap().0.replace(
+        "action_call @inner (x) (y) () (tk, a)",
+        "qloop 0 {\naction_call @inner (x) (y) () (tk, a)\n}",
+    ).replace(
+        "perm_action @addya (x:wire[2]) (y:wire[2] in) () (tk:token, a:i2) ()\n^entry():",
+        "perm_action @addya (x:wire[2]) (y:wire[2] in) () (tk:token, a:i2) ()\nregs {  } bounds {0}\n^entry():",
+    );
+    let object = support::rehash(&(source.trim_end().to_string() + "\n"));
+    let owner = object.identity().unwrap().closure_hashes["addya"]
+        .clone()
+        .unwrap();
+    let invocation = root_invocation(3, 1);
+    let params = sha256_hex(invocation.get("args").unwrap().canonical().as_bytes());
+    let schedule = support::json(&format!(
+        r#"{{"bindings":{{"budget":[0,0,0,0],"closure_hash":"{owner}","epsilon":0,"inherited_controls":0,"params_hash":"{params}","region":"addya","scheduler":{{"name":"test","version":"1"}},"target_hash":"{}","token_aliases":[0],"variant":"forward"}},"entries":[]}}"#,
+        "0".repeat(64)
+    ));
+    let text = change_certificate(&inverse_certificate_for(&object), |c| {
+        fields(fields(c).get_mut("regions").unwrap()).clear();
+        let bindings = fields(fields(c).get_mut("bindings").unwrap());
+        bindings.insert("invocation".into(), invocation);
+        bindings.insert("target_hash".into(), Json::String("0".repeat(64)));
+        bindings.insert(
+            "schedule_hash".into(),
+            Json::String(sha256_hex(schedule.canonical().as_bytes())),
+        );
+    });
+    let (source, certificate) = text.split_once("section certificate\n").unwrap();
+    let text = format!(
+        "{}\n\nsection schedule\n{}\n\nsection certificate\n{certificate}",
+        source.trim_end(),
+        schedule.canonical()
+    );
+    let report = Object::parse(&text).unwrap().verify_certificate().unwrap();
+    assert!(report.claims.is_empty());
+    assert!(
+        matches!(report.qinplace_applicability.get(&owner), Some(QinplaceApplicability::Unestablished(reason)) if reason.contains("realised invocation tree")),
+        "{report:?}"
+    );
+}
+
+#[test]
+fn checked_concrete_context_does_not_discharge_uniform_applicability() {
+    let text = linked_inverse_certificate(false);
+    let object = Object::parse(&text).unwrap();
+    let owner = object.identity().unwrap().closure_hashes["addya"]
+        .clone()
+        .unwrap();
+    let text = change_certificate(&text, |c| {
+        fields(fields(c).get_mut("bindings").unwrap())
+            .insert("invocation".into(), root_invocation(3, 1));
+        let record = fields(fields(c).get_mut("regions").unwrap())
+            .get_mut(&owner)
+            .unwrap();
+        let bennett_isa_ref::json::Json::Array(claims) = fields(record).get_mut("claims").unwrap()
+        else {
+            panic!("claims")
+        };
+        fields(&mut claims[0]).insert(
+            "invocation".into(),
+            support::json(r#"{"args":"all","budget":"all","token_aliases":"all"}"#),
+        );
+    });
+    let report = Object::parse(&text).unwrap().verify_certificate().unwrap();
+    assert_eq!(
+        report
+            .claims
+            .iter()
+            .find(|c| c.closure_hash == owner)
+            .unwrap()
+            .verdict,
+        bennett_isa_ref::ClaimVerdict::Proof
+    );
+    assert!(
+        matches!(report.qinplace_applicability.get(&owner), Some(bennett_isa_ref::QinplaceApplicability::Unestablished(reason)) if reason.contains("parameter-uniform")),
+        "{report:?}"
+    );
+}
diff --git a/reference-interpreter/tests/isa09_token_aliases.rs b/reference-interpreter/tests/isa09_token_aliases.rs
index 404045c..e2de811 100644
--- a/reference-interpreter/tests/isa09_token_aliases.rs
+++ b/reference-interpreter/tests/isa09_token_aliases.rs
@@ -86,6 +86,10 @@ fn certificate_invocations_admit_both_equal_tuple_identity_partitions() {
             object.verify_claim(closure, 0).unwrap(),
             ClaimVerdict::Proof
         );
+        assert_eq!(
+            object.verify_certificate().unwrap().claims[0].verdict,
+            ClaimVerdict::Proof
+        );
     }
     assert_eq!(
         hashes[0], hashes[1],
@@ -806,3 +810,53 @@ fn controlled_native_oracles_match_the_actual_inherited_control_count() {
         assert_eq!(state, entry);
     }
 }
+
+#[test]
+fn schedule_reader_checks_canonical_aliases_and_keeps_the_closed_schema() {
+    let object = oracle_source(true);
+    let original = scheduled(&object, Some("[0,1]"));
+    let parsed = Object::parse(&original).unwrap();
+    assert_eq!(
+        parsed
+            .section("schedule")
+            .unwrap()
+            .get("bindings")
+            .unwrap()
+            .get("token_aliases")
+            .unwrap(),
+        &support::json("[0,1]")
+    );
+    for labels in ["[1,1]", "[0,2]", "[0]", "[]", "[-1,0]", "[0,0.5]"] {
+        let text = scheduled(&object, Some(labels));
+        let error = Object::parse(&text).unwrap_err();
+        assert!(error.to_string().contains("K91"), "{labels}: {error}");
+    }
+    let mut schedule = parsed.section("schedule").unwrap().clone();
+    fields(fields(&mut schedule).get_mut("bindings").unwrap())
+        .insert("token_alias".into(), support::json("[0,1]"));
+    let error = Object::parse(&format!(
+        "{}\nsection schedule\n{}\n",
+        object.text,
+        schedule.canonical()
+    ))
+    .unwrap_err();
+    assert!(error.to_string().contains("unknown"), "{error}");
+}
+
+#[test]
+fn alias_metadata_is_versioned_and_does_not_widen_08_readers() {
+    let original = certificate_object(Some("[0,1]"), 1);
+    let source = original.split_once("section certificate\n").unwrap().0;
+    let legacy = support::rehash(
+        &(source.trim_end().to_string() + "\n")
+            .replace("=0.9", "=0.8")
+            .replace("\"0.9\"", "\"0.8\""),
+    );
+    let with_aliases = scheduled(&legacy, Some("[0,1]"));
+    let error = Object::parse(&with_aliases).unwrap_err();
+    assert!(error.to_string().contains("token_aliases"), "{error}");
+    Object::parse(&scheduled(&legacy, None))
+        .unwrap()
+        .check_hashes()
+        .unwrap();
+}
diff --git a/reference-interpreter/tests/r1_certificates.rs b/reference-interpreter/tests/r1_certificates.rs
index ebed2a2..2f7b467 100644
--- a/reference-interpreter/tests/r1_certificates.rs
+++ b/reference-interpreter/tests/r1_certificates.rs
@@ -63,7 +63,7 @@ fn b14_checked_borrow_claim_and_altered_or_incomplete_claims() {
     let text = swap_frame(n);
     let good = certificate(&text, n, &claim(n, "15", 1, r#"{"program":"ID"}"#), "0");
     let o = Object::parse(&good).unwrap();
-    let reports = o.verify_certificate().unwrap();
+    let reports = o.verify_certificate().unwrap().claims;
     assert_eq!(reports.len(), 1);
     assert_eq!(reports[0].verdict, ClaimVerdict::Proof);
     // Altered: the expected program is the frame itself... replaced by a
@@ -79,7 +79,12 @@ fn b14_checked_borrow_claim_and_altered_or_incomplete_claims() {
     let table = format!(r#"{{"table":[{}]}}"#, rows.join(","));
     let exact = certificate(&text, n, &claim(n, "15", 1, &table), "0");
     assert_eq!(
-        Object::parse(&exact).unwrap().verify_certificate().unwrap()[0].verdict,
+        Object::parse(&exact)
+            .unwrap()
+            .verify_certificate()
+            .unwrap()
+            .claims[0]
+            .verdict,
         ClaimVerdict::Proof
     );
     let wrong = table.replacen("[0,0,0]", "[1,0,0]", 1);
@@ -115,7 +120,11 @@ fn b14_seventeen_wire_frame_with_checked_claim() {
     let n = 16;
     let text = swap_frame(n);
     let good = certificate(&text, n, &claim(n, "65535", 1, r#"{"program":"ID"}"#), "0");
-    let reports = Object::parse(&good).unwrap().verify_certificate().unwrap();
+    let reports = Object::parse(&good)
+        .unwrap()
+        .verify_certificate()
+        .unwrap()
+        .claims;
     assert_eq!(reports[0].verdict, ClaimVerdict::Proof);
 }
 
@@ -279,7 +288,7 @@ fn sol_assert_translation(text: &str, claim: &str, valid: bool) {
     let h = o.identity().unwrap().closure_hashes["a"].clone().unwrap();
     for verdict in [
         o.verify_claim(&h, 0),
-        o.verify_certificate().map(|r| r[0].verdict.clone()),
+        o.verify_certificate().map(|r| r.claims[0].verdict.clone()),
     ] {
         if valid {
             assert_eq!(verdict.unwrap(), ClaimVerdict::Proof);
@@ -395,7 +404,7 @@ fn sol_positional_verdict(text: &str, claim: &str) -> Result<ClaimVerdict, benne
     let o = Object::parse(&certificate(text, 1, claim, "")).unwrap();
     let h = o.identity().unwrap().closure_hashes["a"].clone().unwrap();
     let v = o.verify_claim(&h, 0)?;
-    assert_eq!(o.verify_certificate().unwrap()[0].verdict, v);
+    assert_eq!(o.verify_certificate().unwrap().claims[0].verdict, v);
     Ok(v)
 }
 #[test]
@@ -610,7 +619,7 @@ fn sol_r5_b01_library_replay_checks_boundaries_even_when_region_map_is_identity(
     ] {
         let o = Object::parse(&support::certified_borrow_identity(body, &[2])).unwrap();
         assert_eq!(
-            o.verify_certificate().unwrap()[0].verdict,
+            o.verify_certificate().unwrap().claims[0].verdict,
             ClaimVerdict::Proof
         );
         support::borrow_identity(&o);
@@ -633,7 +642,7 @@ fn sol_r5_b01_certificate_return_checks_keep_quantum_surrounding_state() {
         ))
         .unwrap();
         assert_eq!(
-            o.verify_certificate().unwrap()[0].verdict,
+            o.verify_certificate().unwrap().claims[0].verdict,
             ClaimVerdict::Proof
         );
         support::borrow_identity(&o);
@@ -825,7 +834,7 @@ fn codex_r5_b02_exact_cz_certificate_cannot_admit_a_nonpermutation_frame() {
         ))
         .unwrap();
         assert_eq!(
-            o.verify_certificate().unwrap()[0].verdict,
+            o.verify_certificate().unwrap().claims[0].verdict,
             ClaimVerdict::Proof
         );
         support::borrow_identity(&o);
diff --git a/reference-interpreter/tests/r21_resources.rs b/reference-interpreter/tests/r21_resources.rs
index 792506a..99adc94 100644
--- a/reference-interpreter/tests/r21_resources.rs
+++ b/reference-interpreter/tests/r21_resources.rs
@@ -48,7 +48,7 @@ fn claim(text: &str, small: bool) {
     let r = catch_unwind(|| o.verify_certificate()).expect("no certificate panic");
     if small {
         assert_eq!(
-            r.unwrap()[0].verdict,
+            r.unwrap().claims[0].verdict,
             ClaimVerdict::Evidence { elements: 1 }
         );
     } else {
@@ -160,7 +160,7 @@ fn r21_resource_child() {
                 .unwrap();
             o.check_hashes().unwrap();
             assert_eq!(
-                o.verify_certificate().unwrap()[0].verdict,
+                o.verify_certificate().unwrap().claims[0].verdict,
                 ClaimVerdict::Proof
             );
         }
@@ -201,7 +201,9 @@ fn r21_resource_child() {
                 if n <= 8 {
                     assert_eq!(q.bundle(r.unwrap()).unwrap().len(), n);
                 } else {
-                    resource(r, "§4.3");
+                    // Qreg handle/class-vector storage is §3.3; dense
+                    // quantum-state materialisation below remains §4.3.
+                    resource(r, "§3.3");
                 }
                 let mut q = QuantumRegisters::new();
                 let id = q.allocate(8).unwrap();
diff --git a/reference-interpreter/tests/r22_coverage.rs b/reference-interpreter/tests/r22_coverage.rs
index 4e6fd5c..ce7bbec 100644
--- a/reference-interpreter/tests/r22_coverage.rs
+++ b/reference-interpreter/tests/r22_coverage.rs
@@ -25,7 +25,7 @@ fn sol_r22_b01_false_proof_and_controls() {
                 ClaimVerdict::Evidence { elements: 4 }
             );
             assert_eq!(
-                o.verify_certificate().unwrap()[0].verdict,
+                o.verify_certificate().unwrap().claims[0].verdict,
                 ClaimVerdict::Evidence { elements: 4 }
             );
         }
@@ -205,7 +205,7 @@ fn r23_public_oracle_roles_and_explicit_region_cells() {
         .unwrap();
         p.check_hashes().unwrap();
         let verdict = p.verify_claim(&hash, 0).unwrap();
-        assert_eq!(p.verify_certificate().unwrap()[0].verdict, verdict);
+        assert_eq!(p.verify_certificate().unwrap().claims[0].verdict, verdict);
         verdict
     }
     let sig =
diff --git a/reference-interpreter/tools/test-slow-source-forwarding.sh b/reference-interpreter/tools/test-slow-source-forwarding.sh
new file mode 100755
index 0000000..5cf4f1a
--- /dev/null
+++ b/reference-interpreter/tools/test-slow-source-forwarding.sh
@@ -0,0 +1,12 @@
+#!/bin/sh
+# Explicit opt-in: never materialise the wide source witness without a host cap.
+set -eu
+ulimit -v 8388608
+ulimit -c 0
+root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
+exec /usr/bin/time -f 'slow-source-forwarding wall_s=%e peak_rss_kib=%M' \
+    timeout 600 cargo test --offline -j3 \
+    --manifest-path "$root/reference-interpreter/Cargo.toml" \
+    --test isa09_forwarding \
+    source_forwarding_large_materialisation_reports_host_capacity_before_exhausting_memory \
+    -- --ignored --exact --test-threads=1 --nocapture
````

## 2. Changed files at e9ab12a

# Changed files of job/quality-isaref at e9ab12a

Snapshot of `isaref-stage/` at commit `e9ab12a302650b41a83ac651608494174484af22`. 24 files; each embedded verbatim below. Line counts and sha256 per file:

- `conformance/Cargo.toml` 12 lines, sha256 a517143e9e06
- `docs/quality.md` 226 lines, sha256 163ed1ddc7bd
- `docs/reviews/2026-11-06-quality-isaref-r1.md` 113 lines, sha256 993f00f198b8
- `docs/reviews/2026-11-07-quality-isaref-r2.md` 88 lines, sha256 448f24346dc2
- `docs/reviews/2026-11-07-quality-isaref-r3.md` 83 lines, sha256 02841f81101e
- `gate.toml` 45 lines, sha256 51be957c891d
- `reference-interpreter/Cargo.toml` 13 lines, sha256 3250d894e2c7
- `reference-interpreter/src/certificate.rs` 941 lines, sha256 e4849e2296e8
- `reference-interpreter/src/claims/pairs09.rs` 479 lines, sha256 64d7d7287eb4
- `reference-interpreter/src/claims/qinplace09.rs` 484 lines, sha256 906918bf8184
- `reference-interpreter/src/claims/replay09.rs` 505 lines, sha256 854df1cbd55b
- `reference-interpreter/src/claims.rs` 1175 lines, sha256 87e43cb48a1b
- `reference-interpreter/src/lib.rs` 204 lines, sha256 8c4022e9c3a3
- `reference-interpreter/src/source_constructor/action/qinplace.rs` 67 lines, sha256 6697bf1d3c45
- `reference-interpreter/src/source_constructor/action.rs` 715 lines, sha256 d1acd5e2d7e0
- `reference-interpreter/tests/isa09_certificate.rs` 196 lines, sha256 fa65b8d840f0
- `reference-interpreter/tests/isa09_claim_replay.rs` 479 lines, sha256 7bd221412b57
- `reference-interpreter/tests/isa09_forwarding.rs` 456 lines, sha256 3601716ccc97
- `reference-interpreter/tests/isa09_qinplace.rs` 963 lines, sha256 f74d8b1fda49
- `reference-interpreter/tests/isa09_token_aliases.rs` 862 lines, sha256 43f698a67dd6
- `reference-interpreter/tests/r1_certificates.rs` 895 lines, sha256 2abfb2b2e783
- `reference-interpreter/tests/r21_resources.rs` 410 lines, sha256 24d248dc9c0d
- `reference-interpreter/tests/r22_coverage.rs` 274 lines, sha256 95d7e61f38f2
- `reference-interpreter/tools/test-slow-source-forwarding.sh` 12 lines, sha256 49e282bf9225

Total embedded: 9697 lines.

## `conformance/Cargo.toml` (12 lines)

````toml
[package]
name = "bennett-isa-conformance"
version = "0.0.0"
edition = "2021"
license = "AGPL-3.0-only"

[dependencies]

# Keep exhaustive semantic checks practical without dropping debug/overflow checks.
[profile.test]
opt-level = 1
debug = "line-tables-only"
````

## `docs/quality.md` (226 lines)

````markdown
# Reference interpreter quality floor

Batch 1 (2026-11-06) fixes the round-2 certificate findings and the two
previously failing crate tests. It leaves the broader coverage, integration
binary consolidation, and source decomposition work for batch 2.

## Semantic checks

- A K13 subject with a schedule denotes the realised operation for table,
  program, and oracle relations alike. Until that operation is executed,
  verification returns `Unverified`, with no reference-only proof or coverage.
  Absent or mismatching subject schedules are admission errors.
- K4 inverse-pair claims use their owner-local entry, entry budget and argument
  domain. Both public verification APIs prove the published parameterised pair;
  noninverse pairs and absent entries reject. The entry-bound route was already
  present in the inherited WIP; batch 1 adds certificate-level regression coverage.
- Example 7 is loaded directly from the published spec. Its qinplace source
  adapters now use a collision-free lexical alias when constructing an internal
  ISA operand list; private constructor identities remain private. The source
  test checks both orientations, instruction allocation/release order, arithmetic
  results, preserved inputs, and complete reversal.
- The qreg handle/class-vector capacity check cites §3.3 (the register/type
  rules); dense quantum-state allocation checks retain §4.3.
- K91 schedule/certificate readers are checked for canonical partitions,
  required token-argument bindings, tuple-inconsistent equality, cross-partition
  certificate reuse, uniform claims, and rejection by the unchanged 0.8 grammar.
  The inherited K91 support passed these checks; no schema widening was needed.

The regression tests are in `isa09_certificate`, `isa09_qinplace`,
`r21_resources`, `isa09_token_aliases`, and the published `k91_vectors`.

## Bounded forwarding

The full-width materialisation-capacity witness is ignored in default tests
with the named reason `slow-source-forwarding`. The default run retains both
the complete published Example 10 literal domain (4096 inputs, two engines,
full reversal) and a compact source semantic witness. A separate 1024-leaf
capacity fixture exercises the host-resource diagnostic in the default run.

Run the wide capacity witness explicitly with:

```sh
sh reference-interpreter/tools/test-slow-source-forwarding.sh
```

The script enforces `ulimit -v 8388608`, disables core dumps, bounds wall time
to 600 seconds, uses one test thread, and reports elapsed time and peak RSS
with `/usr/bin/time`. The gate invokes this script separately from default
tests. Both default crate checks in the gate also enforce the 8 GiB address-space
cap. No unbounded full-width source materialisation is run.

Test profiles use optimisation level 1 and line-table debug information;
debug assertions and overflow checks retain their enabled test defaults.

## Measurements

The wide slow witness passed with **1,030,472 KiB peak RSS**: 34.38 s test
execution, 86.91 s wall time including a 52.49 s rebuild. The first bounded
forwarding run passed 11 tests with one named slow ignore in 40.02 s
(179.69 s including the initial profile build; 930,700 KiB peak RSS).

The commands below run from the repository root. They use a private target
directory, a project-local temporary directory, at most three compiler jobs
and four test threads. GNU time reports wall time including compilation and
the largest resident-set high-water mark among the command's children,
not a sum of simultaneous processes.

```sh
unset DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER
export TMPDIR="$PWD/.tmp/quality-isaref/tmp"
export CARGO_TARGET_DIR="$PWD/.tmp/quality-isaref/target"
mkdir -p "$TMPDIR"
ulimit -v 8388608
ulimit -c 0
/usr/bin/time -v timeout 1800 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml --no-fail-fast -- --test-threads=4
python3 -I reference-interpreter/tools/publish-cli.py "$CARGO_TARGET_DIR/debug/bennett-isa-ref"
/usr/bin/time -v timeout 1800 cargo test --offline -j3 --manifest-path conformance/Cargo.toml --no-fail-fast -- --test-threads=4
```

Verified at 2026-11-06 07:33:36 UTC. Both complete default
commands above exited 0 under the 8 GiB address-space cap.

| Crate | Passed | Ignored | Wall (min:sec) | Peak RSS (KiB) | Exit |
|---|---:|---:|---:|---:|---:|
| reference-interpreter | 653 | 6 | 19:08.93 | 1,591,284 | 0 |
| conformance | 129 | 0 | 25:39.00 | 723,100 | 0 |

The reference final run reused compiled artifacts; the conformance measurement
includes its initial test build. These runs overlapped on a shared Linux host,
so the numbers describe the observed commands rather than isolated benchmarks.
The reference's six ignores comprise five existing exhaustive sweeps and the
new named slow forwarding witness. Conformance has no ignored tests.

The original qinplace and register-capacity failures were reproduced before
their fixes. The first whole reference run also exposed an older controlled-table
test that expected the false realised `Proof`; its final test now checks
`Unverified` for the unchanged scheduled fixture and proves the full table
through an explicit reference-only invocation. The final complete rerun passed.

Both crates also pass `cargo fmt --check` with their manifest paths. Interpreter
library/binary linting passed:
`cargo clippy --offline -j3 --manifest-path reference-interpreter/Cargo.toml --lib --bins -- -D warnings`.

The 180-second programme target is **not met** by this batch: conformance's
1,048,320-tuple call-interface test alone took 337.93 s. Runtime reduction is
tracked in `b-isa-spec-e923` for batch 2; the remaining `b-isa-spec-x6to`
nits are also outside the batch-1 correctness fixes. Coverage is not remeasured
in this batch. The complete repository gate is reserved for the orchestrator.


## Certificate review remediation

The follow-up keeps the standalone inverse-pair theorem distinct from executable
applicability. `ClaimReport.qinplace_applicability` records either `Established`
or `Unestablished(reason)` for a supplied qinplace owner. Static inventory includes
nested sites and zero-trip loop bodies. Concrete root and standalone claim
invocations check the transitive reference construction with each callee's actual
tokens and arguments; coherent predicates retain their obligations. Missing
owner-local pairs and uncovered bound sites reject through both public checking
routes. Zero-trip loops have no dynamic applicability visits.

Linked inverse-pair claims must resolve to an exhaustive pair theorem through an
acyclic library chain. Every link preserves the exact resolved closure pair,
minimum tuple, argument-token tuples, token partition and proved argument domain.
The runtime accepts this library route in both orientations. The published
Example 7 arithmetic and complete reversal are checked over every x, y and a at
primary budgets 3 and 9, using an exhaustive donor with no domain on the library
claim itself. A missing library body retains an unverified theorem and explicit
unestablished applicability; execution rejects it before effects. Scheduled
realisation trees and unsupported bound root kinds also remain explicitly
unestablished rather than inheriting a reference-only acceptance.

Five review regressions were run against an archived `b572e17` source tree before
the implementation: missing owner inventory, uncovered bound minimum, omitted
unestablished outcome, proof transfer to g/g, and valid library execution each
failed for its intended semantic reason. The final suite also covers nested
sites, zero-trip inventory, disabled controls, transitive owners, donor budget and
argument-domain preservation, and missing library bodies. No published spec or
fixture bytes changed.


The remediation focused check passed **58 tests with one existing ignore**:

```sh
timeout 600 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml --test isa09_qinplace --test isa09_claim_replay --test isa09_certificate --test r1_certificates --test r1_qinplace -- --test-threads=4
```

Both crates passed `cargo fmt --manifest-path <crate>/Cargo.toml -- --check`
and strict library/binary linting with
`timeout 600 cargo clippy --offline -j3 --manifest-path <crate>/Cargo.toml --lib --bins -- -D warnings`.
The reference default command documented above was run once after the source
changes, with the same environment and caps: **664 passed, six existing ignores,
exit 0, 21:58.05 wall, 1,592,024 KiB peak RSS**. The freshly built CLI was then
published to the stable path inside this worktree for the conformance run.
The conformance default command also passed once after publication, with no
source changes between either complete run. Runtime and wider quality work remain
outside this remediation.


Final remediation validation recorded at 2026-11-07 06:23:46 UTC.
Both exact default commands are listed above; each used `ulimit -v 8388608`,
`timeout 1800`, three compiler jobs and four test threads.

| Crate | Passed | Ignored | Wall (min:sec) | Peak RSS (KiB) | Exit |
|---|---:|---:|---:|---:|---:|
| reference-interpreter | 664 | 6 | 21:58.05 | 1,592,024 | 0 |
| conformance | 129 | 0 | 16:52.64 | 723,256 | 0 |

The reference run includes rebuilding affected binaries; conformance reused its
compiled artifacts. They ran sequentially on a shared host. The 180-second
programme target remains open for batch 2; these measurements do not claim it
is met. No full repository or sibling gate was run for this remediation.

## Bound-root obligation reporting

Certificate checking now returns `CertificateReport`: its `claims` field retains
standalone claim verdicts, while `qinplace_applicability` records obligations by
owner or bound root closure independently of the claim collection. Callers that
previously consumed the returned claim vector select `.claims`. A retained
standalone `Proof` does not establish executable acceptance when the report
contains an unestablished applicability obligation.

Unsupported bound root kinds retain their obligation even when no supplied
record directly owns qinplace, all claims and inverse-pair entries are removed,
or the region map is empty. The same rule applies to unchecked scheduled trees,
parameter-uniform invocations and host-resource-limited traversal. Unresolved
contexts take precedence over checked contexts of the same closure. Concrete
reference traversal still rejects missing owner-local entries and uncovered
sites; unbound direct owners retain their separate unestablished outcome.

The attachment audit covered inventory owners, concrete roots, standalone claim
invocations, uniform invocations, scheduled traversal and work-limit exits, and
the final claim-report construction. Obligations no longer require a discovered
owner, claim, record or inverse-pair entry to reach the certificate report.
Three empty-collection variants and an unchecked uniform transitive claim were
reproduced as semantic failures before the fix. Additional regressions cover an
unchecked scheduled root with no reached owners or claims and a concrete check
that cannot discharge a separate uniform obligation. No published spec or
fixture bytes changed.


Bound-root focused validation passed **64 tests with one existing ignore**, using
the focused command above. Both crates passed the same formatting and strict
library/binary Clippy commands, and all reference test binaries compiled with
`timeout 600 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml --no-run`.

The full default reference command above ran once after the source was frozen:
**670 passed, six existing ignores, exit 0, 7:00.81 wall, 1,591,540 KiB peak RSS**.
This run reused the compiled test artifacts and retained the 8 GiB address-space
cap. Reference results recorded at 2026-11-07 06:52:55 UTC. The completed CLI was atomically
published inside this worktree before starting the conformance command.


Complete bound-root validation recorded at 2026-11-07 07:04:00 UTC. Both default commands
listed above ran once, sequentially, with `ulimit -v 8388608`, `timeout 1800`,
three compiler jobs and four test threads. Source stayed unchanged between runs.

| Crate | Passed | Ignored | Wall (min:sec) | Peak RSS (KiB) | Exit |
|---|---:|---:|---:|---:|---:|
| reference-interpreter | 670 | 6 | 7:00.81 | 1,591,540 | 0 |
| conformance | 129 | 0 | 11:27.10 | 727,476 | 0 |

Both runs reused compiled test artifacts on the shared host. The reference's
six ignores are unchanged; conformance has none. The 180-second target, coverage
measurement and remaining structural quality work are still deferred to batch 2.
No full repository or sibling gate ran.
````

## `docs/reviews/2026-11-06-quality-isaref-r1.md` (113 lines)

````markdown
# ISA reference interpreter: quality batch 1, review 1

**Verdict: BLOCK — two P0, one P1.** No implementation files changed.

Reviewed head: `f0c97a864bf7afe23c23371b4f94bcf2ed7c0661` (`job/quality-isaref`).
Batch range: `main..job/quality-isaref`, seven commits, `7518447..f0c97a8`.
At review start `main` was `e0424a99197e95057529eae25c176fa34491757a`;
its source equals the brief's `be109bd` (only the Beads export differs).
Also reviewed the inherited reference-interpreter changes in
`9825c42ad5c95cce9cd1419dcbcae0bfffab6e16..e0424a99197e95057529eae25c176fa34491757a`
(`origin/main..main`) affecting claims, replay, certificates, metadata and token aliases.
Findings below concern these inherited semantics as well as the batch's intended K4/K92 coverage.

## Blocking findings

**P0-1 — K92 certificate obligations are omitted. Bead `b-isa-spec-jple`.**
`reference-interpreter/src/claims.rs:874` returns claim reports without checking
the qinplace pair inventory, bound invocation applicability, or an unresolved
applicability outcome. Starting from `isa09_qinplace.rs::inverse_certificate()`,
remove the `addya` record's claims and `verification.inverse_pairs`: parsing
succeeds and `verify_certificate()` returns `Ok([])` despite its qinplace site.
Alternatively retain the correct pair and bind root invocation
`{"args":[["2","0","0","0"],"1"],"budget":["0","0","0","0"],"token_aliases":[0]}`.
The entry minimum is 3, but verification reports only `[Proof]`; execution
of that same root rejects `no covering inverse-pair entry`.
ISA 0.9 §12.3 K92 requires missing owner-local entries and uncovered bound
sites to reject, and unresolved applicability to be reported explicitly.
Execution-only checks do not discharge the checker obligation.
Ran `timeout 60 .tmp/rev-quality-isaref-r1/tmp/review-probe`: exit 0,
asserting both observations and the execution rejection.

**P0-2 — A library proof transfers to a different, noninverse pair. Bead `b-isa-spec-b6ds`.**
`reference-interpreter/src/claims.rs:807`–812 returns the referenced claim's
verdict without checking K4's same-pair side condition. Copy the fixture's
correct exhaustive `g/ginv` claim and entry into a linked `g` region record
(with its oracle signature and frame). Replace `addya` claim 0 with a
concrete `inverse_pair_library` claim referencing that record's claim 0,
but change the owner entry to `g/g`. Both public verification APIs report
`Proof`. For the published `g(x;y,a) = x+y+a mod 4`, at `x=y=0,a=1`,
`g(g(x))=2`, not 0. The exhaustive route correctly rejects this same pair.
ISA 0.9 §4.5 permits library reuse only for the same resolved g/ginv closures.
Ran `timeout 60 .tmp/rev-quality-isaref-r1/tmp/review-library-probe`: exit 0,
asserting the wrong `Proof` and observing exhaustive-route rejection.

**P1-3 — Valid linked-library pair coverage cannot execute. Bead `b-isa-spec-0dq0`.**
`reference-interpreter/src/claims/qinplace09.rs:131`–134 admits only
`exhaustive` / `expected:"inverse_pair"`. Keep the correct `g/ginv` entry
and linked exhaustive donor from P0-2; its owner-local
`inverse_pair_library` claim verifies as `Proof`. At the covered `tk=3,a=1`,
`execute_action_with_token_aliases("addya", …, &[0])` nevertheless rejects
`unestablished linked inverse-pair proof`. The original exhaustive fixture
executes successfully. This excludes the library route explicitly promised
by ISA 0.9 §4.5 and suite C, rather than merely leaving applicability unknown.
Ran `timeout 60 .tmp/rev-quality-isaref-r1/tmp/review-probe`: exit 0,
asserting that rejection.

The two probes were compiled from stdin with `timeout 120 rustc`, linked
against the freshly built review rlib, and included the existing
`tests/isa09_qinplace.rs` helpers. Their mutations affect certificate JSON
only; the independent arithmetic counterexample is given above.

## Verification and scope

All commands were headless, with private `.tmp/rev-quality-isaref-r1/{tmp,target}`
directories; Cargo runs had an 8 GiB address-space cap and core dumps disabled.

```sh
timeout 600 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml \
  --test isa09_certificate --test isa09_claim_replay --test isa09_token_aliases \
  --test isa09_qinplace --test r21_resources --test k91_vectors -- --test-threads=4
timeout 300 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml \
  --test isa09_forwarding -- --test-threads=4
git diff --check main...job/quality-isaref
```

Results: exit 0 for each; respectively 53 passed, then 11 passed / one
`slow-source-forwarding` ignore. No full crate suite, gate or sibling gate ran.
The wide slow witness was inspected, not rerun; its script supplies the memory
and wall-time caps and the gate invokes it explicitly.

The scheduled table/program/oracle regressions now return `Unverified` without
coverage; dangling/missing schedules reject. Reading `git show main:<path>`
confirms those scheduled-table regressions and the existing source-qinplace
expansion test catch the old paths. The r21 correction matches §3.3's qreg
storage rule. The exhaustive inverse-pair route already existed on main;
the added certificate assertions exercise it, not a newly failing baseline.
K91's concrete partitions, uniform admission, cross-partition rejection and
unchanged 0.8 grammar pass the focused tests. Correcting the old scheduled
`Proof` expectation preserves its full reference-table checks.

P2+ nits, **one bead `b-isa-spec-nivd`**: redundant/dead inverse-pair dispatch;
tracked pycache/log/progress litter; deferred long functions and production
test hooks; missing gate ratchet, stale `HANDOFF.md`, coverage and runtime target.
Programme items 9–10 were checked: the batch-1 implementer brief expressly
assigns them to batch 2. The reported default runtimes exceed 180 seconds.

Anti-slop: checked each COMMON rule. No new inconsistent state flags, silent
failure default, repeated compound predicate, semantic magic number, process
identifier, oracle-derived test expectation, test weakening or owned-path
violation found in the batch fix. The library dispatch and missing K92
validation above are the confirmed semantic failures; structural debt is in
the combined nit bead.

Coverage: read closely the complete batch source/test diff, `claims/replay09.rs`,
`pairs09.rs`, `qinplace09.rs`, `images09.rs`, claim execution/verdict routes,
certificate admission, token partition resolution, and K91 schedule binding
paths against §§4.5, 12.1–12.3; skimmed other source-path/tie-selection code,
fixture generators, CLI plumbing and broad inherited changes outside those paths.
Full conformance, target realisation, numerical/channel and unrelated interpreter
subsystems were not exhaustively reviewed.

Provenance: implementer **gpt-6.1-sol**; reviewer **gpt-6.1-sol, fresh session, D9**.
This BLOCK review does not claim council clearance.
````

## `docs/reviews/2026-11-07-quality-isaref-r2.md` (88 lines)

````markdown
# ISA reference interpreter: quality batch 1, review 2

**Verdict: BLOCK — one residual P0; no P1.** No implementation files changed.

Reviewed head: `cdef3eb184e2aab9dcf97bde5fd3be1fcf6e1982` (`job/quality-isaref`).
Batch inventory: `git log --reverse main..job/quality-isaref` and
`git diff main...job/quality-isaref`; round-2 review focuses on
`b572e17..cdef3eb` (`92fbe5c`, `75cec86`, `cdef3eb`) and reproduces the
three findings in `2026-11-06-quality-isaref-r1.md`.

## Blocking finding

**P0-1 — Unresolved bound-root applicability disappears when the owner map is empty.
Bead `b-isa-spec-lfbd` (residual of `b-isa-spec-jple`).**
`reference-interpreter/src/claims/qinplace09.rs:142`–144 records an unsupported
CC/R root as unresolved, but lines 179–182 attach that outcome only to already
inventoried direct qinplace owners. If none of the supplied records directly
contains qinplace, the map is empty and the obligation silently disappears.
`reference-interpreter/src/claims.rs:923` consequently reports applicability
`None`, rather than `Unestablished`.

Repro from `tests/isa09_qinplace.rs::transitive_certificate(false)`:
the linked path is `run` (CC) → `addya` → `inner` → qinplace. The certificate
contains only the outer `addya` record and its valid inverse-pair theorem;
the required `inner` owner entry is absent. Change `bindings.closure_hash`,
`reference_program_hash` and `interface_hash` to the identities of `run`, and
set `bindings.invocation = root_invocation(2, 1)`. Parsing succeeds.
`verify_certificate()` returns one `Proof` with `qinplace_applicability: None`;
`verify_claim(addya, 0)` also returns `Proof`. Removing the outer record’s
claims and inverse-pair entries instead returns `Ok([])`, still without an
unestablished outcome. Executing the corresponding `addya` invocation at
`tk=3,a=1` rejects `no covering inverse-pair entry in @inner` before effects.

ISA 0.9 §12.3 K92 requires bound transitive coverage, and explicitly requires
an unestablished obligation when an invocation/context cannot be checked.
Keeping the standalone theorem is permitted; omitting the unresolved
applicability obligation is not. An unsupported root needs an observable
obligation even when the actual owner record or all claim reports are absent.

Ran `timeout 60 .tmp/rev-quality-isaref-r2/tmp/review-probe` and
`timeout 60 .tmp/rev-quality-isaref-r2/tmp/review-applicability-probe`: both
exit 0, asserting these observations. Probes were compiled from stdin with
`timeout 120 rustc`, included the existing qinplace fixture helpers, and
linked against the freshly built review rlib. Only certificate JSON was mutated.

## Verification and scope

The original round-1 probes now pass: missing direct owner inventory rejects;
a bound primary tuple below the entry minimum rejects through both public
checking APIs; an unbound direct owner reports explicit unestablished
applicability; the library g/g substitution rejects; a valid linked g/ginv
pair executes with the hand-derived arithmetic result and reverses exactly.
Thus `b-isa-spec-b6ds` and `b-isa-spec-0dq0` are fixed in the reviewed paths;
`b-isa-spec-jple` retains the sibling-route gap above.

All test/probe commands were headless, used private
`.tmp/rev-quality-isaref-r2/{tmp,target}` directories, and ran under
`ulimit -v 8388608; ulimit -c 0`.

```sh
timeout 600 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml \
  --test isa09_qinplace --test isa09_claim_replay --test isa09_certificate -- --test-threads=4
timeout 600 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml \
  --test r1_certificates --test r1_qinplace -- --test-threads=4
git diff --check b572e17..cdef3eb
```

Results: **58 passed, one existing ignore**, all commands exit 0. No full
reference suite, repository gate or sibling gate ran. Reading the main-side
and pre-fix claim/coverage code confirms the new inventory, library-pair
identity and executable-library regressions distinguish the old behavior;
expected arithmetic is independent of the implementation.

P2+ nits: **one bead `b-isa-spec-fg4u`** consolidates continuing dead dispatch,
tracked litter, stale `HANDOFF.md`, missing gate ratchet, production no-op
hooks, and deferred function/coverage/runtime work (also `b-isa-spec-nivd`).
No new nonblocking pattern found in the fix. Checked every COMMON anti-slop
rule; the silent obligation loss is the confirmed blocking violation. Batch-2
items remain assigned to batch 2 by the implementer brief.

Coverage: read closely the complete round-2 source/test diff, pair theorem
resolution, inventory/applicability traversal, both public checking APIs,
replay invocation decoding and certificate admission against §§4.5, 12.3
K4/K92; skimmed unchanged action/oracle call plumbing and prior structural
debt. Other interpreter subsystems and full conformance were not re-reviewed.

Provenance: implementer **gpt-6.1-sol**; reviewer **gpt-6.1-sol, fresh session, D9**.
This BLOCK review does not claim council clearance.
````

## `docs/reviews/2026-11-07-quality-isaref-r3.md` (83 lines)

````markdown
# ISA reference interpreter: quality batch 1, review 3

**Verdict: CLEAR — no P0/P1.** No implementation files changed.

Reviewed head: `8056ecf3834955ec8a46f091b7d90b026dc207dd` (`job/quality-isaref`).
Batch inventory: `git log --reverse main..job/quality-isaref` and
`git diff main...job/quality-isaref`; this final review focuses on
`d3a338e..8056ecf` (`15c8c3a`, `fa8f276`, `8056ecf`) and rechecks the
P0/P1 scenarios from both earlier review documents against ISA 0.9 §§4.5,
12.3 K92.

The residual **P0-1 `b-isa-spec-lfbd` is fixed**. An independent stdin Rust
probe rebuilt the round-2 `run → addya → inner → qinplace` certificate,
retargeting the root bindings to `run` with `root_invocation(2, 1)`.
With the outer pair claim retained, its standalone verdict remains `Proof`
and the report independently contains `run: Unestablished`. Removing the
outer claims and entries preserves that root obligation with zero claim
reports; removing every region record also preserves it. In all three
variants, executing `addya` at tk=3,a=1 rejects the missing inner-owner
entry before effects and leaves the quantum state unchanged.

The original round-1 findings remain fixed: missing direct inventory and
below-minimum bound tuples reject; wrong g/g library reuse rejects through
both public verification APIs; valid g/ginv library coverage executes the
hand-derived result and reverses exactly. Focused tests also cover transitive
arguments, zero-trip inventory, disabled predicates and unavailable libraries.

`CertificateReport.qinplace_applicability` retains obligations independently
of records and claims. Unsupported roots, unchecked uniform arguments,
scheduled trees and host-resource failures insert their own closure keys;
unresolved outcomes merge last so a checked concrete context cannot discharge
a uniform obligation. Static owner outcomes and checked transitive owners
are retained too. Explicit borrow-frame references remain index-validated
and checked separately; their enforcement does not rely on a nonempty report.
The standalone `verify_claim` contract explicitly disclaims executable
applicability.

The report-shape change retains all claim fields and their closure-map /
claim-index order inside `.claims`; the probe checks both linked-library
records are present and ordered. The Rust API intentionally requires callers
to select `.claims`. No production CLI command serializes or consumes
`verify_certificate`; CLI/JSON formatting code is unchanged. Existing public
CLI partition and resource-output tests pass.

Verification used headless commands, private
`.tmp/rev-quality-isaref-r3/{tmp,target}`, `ulimit -v 8388608` and `ulimit -c 0`:

```sh
timeout 600 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml \
  --test isa09_qinplace --test isa09_claim_replay --test isa09_certificate \
  --test isa09_token_aliases -- --test-threads=4
timeout 600 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml \
  --test r1_certificates --test r1_qinplace --test r21_resources \
  --test r22_coverage -- --test-threads=4
timeout 60 .tmp/rev-quality-isaref-r3/tmp/review-probe
git diff --check main...job/quality-isaref
```

All exit 0: **95 tests passed, one unchanged ignore**; independent probe passed.
The probe was compiled with `timeout 120 rustc --edition=2021 -C opt-level=1`,
including the existing fixture helpers and linking freshly built review rlibs.
Reading `git show main:reference-interpreter/src/claims.rs` and the pre-fix
`qinplace09.rs` confirms the empty-report and uniform/scheduled regressions
would fail there: main has no independent applicability report, while the
round-2 code loses unresolved outcomes on an empty owner map and skips uniform
obligations. No branch switching, full crate suite, repository gate or sibling
gate was used. No tests or expectations were weakened.

P2+ nits: **one bead `b-isa-spec-bkqj`** consolidates existing dead dispatch,
tracked litter, stale `HANDOFF.md`, missing gate ratchet, production no-op
hooks and deferred function/coverage/runtime work; no new nit in this fix.
Checked every COMMON anti-slop rule; no new semantic violation or narrowing.
Batch-2 items remain assigned to batch 2 by the implementer brief.

Coverage: read closely the complete round-3 source/test diff, both verification
APIs, K92 inventory/traversal and outcome merges, certificate invocation/index
admission, prior P0/P1 scenarios and public report consumers; skimmed unchanged
pair-theorem and CLI plumbing and continuing structural debt. Other interpreter
subsystems and full conformance were not re-reviewed.

Provenance: implementer **gpt-6.1-sol**; reviewer **gpt-6.1-sol, fresh session, D9**.
CLEAR applies to this review scope; the required critical-batch council round
remains the orchestrator's next step.
````

## `gate.toml` (45 lines)

````toml
# Push-gate pins (bennett/tools/gate_README.md). Siblings resolve only to these commits.
schema = 1
repo = "bennett-isa-spec"
tool_sha = "01c0314c9aaa4a37313ab530da2134efafe9cbd5"
timeout_s = 14400

[env]
CARGO_TARGET_DIR = "{root}/.tmp/gate-target"

[[check]]
name = "crate target links (witness and tests address <crate>/target)"
argv = ["sh", "-c", "for c in reference-interpreter conformance; do rm -rf \"$c/target\"; ln -s \"$CARGO_TARGET_DIR\" \"$c/target\"; done; mkdir -p \"$CARGO_TARGET_DIR\""]

[[check]]
name = "cargo test reference-interpreter"
argv = ["sh", "-ec", "ulimit -v 8388608; ulimit -c 0; exec timeout 1800 cargo test --offline -j3 --manifest-path reference-interpreter/Cargo.toml -- --test-threads=4"]

[[check]]
name = "cargo test conformance"
argv = ["sh", "-ec", "ulimit -v 8388608; ulimit -c 0; exec timeout 1800 cargo test --offline -j3 --manifest-path conformance/Cargo.toml -- --test-threads=4"]

[[check]]
name = "slow-source-forwarding (8 GiB cap)"
argv = ["sh", "reference-interpreter/tools/test-slow-source-forwarding.sh"]

[[check]]
name = "diff witness"
argv = ["python3", "-I", "conformance/tests/draft_witnesses.py"]

[[check]]
name = "bound catalog"
argv = ["python3", "-I", "conformance/tools/ref_catalog.py", "--check"]

[siblings."bennett-isa-spec-review"]
sha = "8d9a5c60aff9aa35b44eb3ac1c541c020f24d737"
repo = "bennett-isa-spec"
note = "the pinned review binary draft_witnesses.py reaches by relative path"

[[siblings."bennett-isa-spec-review".build]]
name = "reference interpreter (debug)"
cwd = "reference-interpreter"
argv = ["cargo", "build", "--offline"]
outputs = ["reference-interpreter/target/debug/bennett-isa-ref"]
env = { CARGO_BUILD_JOBS = "4" }
````

## `reference-interpreter/Cargo.toml` (13 lines)

````toml
[package]
name = "bennett-isa-ref"
version = "0.0.0"
edition = "2021"
license = "AGPL-3.0-only"

[dependencies]
bennett-isa-conformance = { path = "../conformance" }

# Keep exhaustive semantic checks practical without dropping debug/overflow checks.
[profile.test]
opt-level = 1
debug = "line-tables-only"
````

## `reference-interpreter/src/certificate.rs` (941 lines)

````rust
//! Certificate schemas, bindings and references (§9.4, §12).
use crate::{
    err,
    json::Json,
    metadata::{hash, text, variant},
    sha256_hex, Error, Function, Object, Result, Type,
};
use std::collections::{BTreeMap, BTreeSet};

fn contextual<T>(rule: &str, f: impl FnOnce() -> Result<T>) -> Result<T> {
    f().map_err(|e| e.context(rule))
}
fn context_key(key: &str) -> Result<(&str, u128)> {
    let (name, controls) = key
        .split_once(':')
        .ok_or_else(|| Error::new("§12: variant:inherited_controls key required".into()))?;
    variant(&Json::String(name.into()))?;
    let n = crate::object::host_count(controls, "inherited control count")?;
    Ok((name, n as u128))
}
/// The closed §8.1 AST; frame expressions bind only c.
pub(crate) fn expression(value: &Json, variables: &BTreeSet<&str>) -> Result<()> {
    crate::metadata_schema::validate("expression", value)?;
    match value {
        Json::Number(_) => {}
        Json::Object(fields) => {
            if fields.contains_key("var") {
                if !variables.contains(value.get("var")?.string()?) {
                    return err("§8.1", "expression references an unbound variable");
                }
            } else if fields.contains_key("op") {
                let arity = match value.get("op")?.string()? {
                    "+" | "-" | "*" | "/" | "max" | "min" => 2,
                    "ceil" => 1,
                    "log2inv_eps" => 0,
                    _ => return err("§8.1", "unknown expression operator"),
                };
                let args = value.get("args")?.array()?;
                if args.len() != arity {
                    return err("§8.1", "expression arity mismatch");
                }
                if value.get("op")?.string()? == "log2inv_eps" && !variables.contains("eps") {
                    return err("§8.1", "epsilon is unbound");
                }
                for a in args {
                    expression(a, variables)?;
                }
            } else {
                text(value.get("table")?)?;
                let index = value.get("index")?.string()?;
                if (index == "k" && !variables.contains("k"))
                    || (index == "eps_decade" && !variables.contains("eps"))
                    || !["k", "eps_decade"].contains(&index)
                {
                    return err("§8.1", "unbound table index");
                }
            }
        }
        _ => return err("§8.1", "expression must be a number or closed AST"),
    }
    Ok(())
}
fn frame(value: &Json) -> Result<()> {
    contextual("§9.4", || {
        for slot in value.get("interface")?.array()? {
            if slot.get("width")?.uint()? == 0 {
                return err("§9.4", "zero-width frame slot");
            }
        }
        let variables = BTreeSet::from(["c"]);
        expression(value.get("retained_history")?, &variables)?;
        for key in ["scratch", "borrow", "scheme_ancillae"] {
            for count in value.get(key)?.object()?.values() {
                if key == "scratch"
                    && count
                        .object()
                        .is_ok_and(|m| m.contains_key("clean") || m.contains_key("dirty"))
                {
                    expression(count.get("clean")?, &variables)?;
                    expression(count.get("dirty")?, &variables)?;
                } else {
                    expression(count, &variables)?;
                }
            }
        }
        if let Some(ranges) = value.object()?.get("live_ranges") {
            let mut grouped: BTreeMap<String, Vec<(u128, u128)>> = BTreeMap::new();
            for r in ranges.array()? {
                let id = text(r.get("frame")?)?.to_string();
                let lo = r.get("start")?.uint()?;
                let hi = r.get("end")?.uint()?;
                if lo >= hi {
                    return err("§9.4", "empty or inverted shared-frame live range");
                }
                let prior = grouped.entry(id).or_default();
                if prior.iter().any(|(a, b)| lo < *b && *a < hi) {
                    return err("§9.4", "shared frame has overlapping live ranges");
                }
                prior.push((lo, hi));
            }
        }
        Ok(())
    })
}
fn frame_width(v: &Json, c: u128) -> Result<u128> {
    // Evaluate with exact rational arithmetic; large intermediates report host
    // capacity rather than changing the declared width.
    fn eval(v: &Json, c: u128) -> Result<(i128, i128)> {
        let capacity =
            || crate::resource_error("§9.4", "frame expression exceeds rational host capacity");
        if matches!(v, Json::Number(_)) {
            let t = v.canonical();
            let (mantissa, exp) = t.split_once('e').map_or(Ok((t.as_str(), 0i32)), |(m, e)| {
                e.parse::<i32>().map(|e| (m, e)).map_err(|_| capacity())
            })?;
            let (whole, fractional) = mantissa.split_once('.').unwrap_or((mantissa, ""));
            let scale = (fractional.len() as i32)
                .checked_sub(exp)
                .ok_or_else(capacity)?;
            let mut num = format!("{whole}{fractional}")
                .parse::<i128>()
                .map_err(|_| capacity())?;
            let den = if scale >= 0 {
                10i128.checked_pow(scale as u32).ok_or_else(capacity)?
            } else {
                num = num
                    .checked_mul(
                        10i128
                            .checked_pow(scale.unsigned_abs())
                            .ok_or_else(capacity)?,
                    )
                    .ok_or_else(capacity)?;
                1
            };
            return Ok((num, den));
        }
        if v.object()?.contains_key("var") {
            return Ok((i128::try_from(c).map_err(|_| capacity())?, 1));
        }
        let args = v
            .get("args")?
            .array()?
            .iter()
            .map(|a| eval(a, c))
            .collect::<Result<Vec<_>>>()?;
        let op = v.get("op")?.string()?;
        let (a, b) = args[0];
        if op == "ceil" {
            return Ok((a.div_euclid(b) + i128::from(a.rem_euclid(b) != 0), 1));
        }
        let (d, e) = args[1];
        let mul = |x: i128, y: i128| x.checked_mul(y).ok_or_else(capacity);
        let (mut n, mut q) = match op {
            "+" => (
                mul(a, e)?.checked_add(mul(d, b)?).ok_or_else(capacity)?,
                mul(b, e)?,
            ),
            "-" => (
                mul(a, e)?.checked_sub(mul(d, b)?).ok_or_else(capacity)?,
                mul(b, e)?,
            ),
            "*" => (mul(a, d)?, mul(b, e)?),
            "/" if d != 0 => (mul(a, e)?, mul(b, d)?),
            "min" | "max" => {
                let less = mul(a, e)? < mul(d, b)?;
                if less == (op == "min") {
                    (a, b)
                } else {
                    (d, e)
                }
            }
            _ => return err("§9.4", "undefined frame expression"),
        };
        if q < 0 {
            n = n.checked_neg().ok_or_else(capacity)?;
            q = q.checked_neg().ok_or_else(capacity)?;
        }
        let (mut x, mut y) = (n.unsigned_abs(), q as u128);
        while y != 0 {
            (x, y) = (y, x % y);
        }
        Ok((n / (x as i128), q / (x as i128)))
    }
    expression(v, &BTreeSet::from(["c"]))?;
    let (n, d) = eval(v, c)?;
    if n < 0 || n % d != 0 {
        return err("§9.4", "frame width must be a nonnegative integer");
    }
    Ok((n / d) as u128)
}
fn frame09(value: &Json, f: &Function, contexts: &[u128]) -> Result<()> {
    let mut ids = BTreeSet::new();
    let mut frames = BTreeSet::new();
    for group in ["slots", "scratch", "history", "borrow", "ancillae"] {
        for record in value.get(group)?.array()? {
            let id = record.get("id")?.string()?;
            if !ids.insert(id) {
                return err("§9.4", "duplicate frame identity");
            }
            if group != "slots" {
                frames.insert(id);
            }
            for c in contexts {
                frame_width(record.get("width")?, *c)?;
            }
        }
    }
    let mut expected = Vec::new();
    let groups: &[(&str, usize)] = match f.kind.as_str() {
        "oracle" => &[("in", 0), ("tgt", 1), ("fault", 2), ("mem", 3)],
        "action" | "perm_action" => &[("mut", 0), ("in", 1), ("mem", 2)],
        _ => &[],
    };
    for (group, index) in groups {
        for (i, p) in f.params[*index].iter().enumerate() {
            let (role, width) = match p.ty {
                Type::Wire(w) => ((*group).to_string(), w as u128),
                Type::Region(a, w) => (
                    format!("mem_{}", p.role.as_deref().unwrap_or("in")),
                    crate::oracle::power_of_two(a as u128)
                        .and_then(|n| n.checked_mul(w as u128))
                        .ok_or_else(|| {
                            crate::resource_error("§9.4", "interface region width exceeds u128")
                        })?,
                ),
                _ => return err("§9.4", "invalid frame interface type"),
            };
            expected.push((format!("{group}:{i}"), role, width));
        }
    }
    let slots = value.get("slots")?.array()?;
    if slots.len() != expected.len() {
        return err("§9.4", "frame interface slot count mismatch");
    }
    for (slot, (id, role, width)) in slots.iter().zip(expected) {
        if slot.get("id")?.string()? != id || slot.get("role")?.string()? != role || width == 0 {
            return err("§9.4", "frame interface identity or role mismatch");
        }
        for c in contexts {
            if frame_width(slot.get("width")?, *c)? != width {
                return err("§9.4", "frame interface width mismatch");
            }
        }
    }
    if let Some(ranges) = value.object()?.get("live_ranges") {
        let mut prior = BTreeMap::<&str, Vec<(u128, u128)>>::new();
        for r in ranges.array()? {
            let id = r.get("frame")?.string()?;
            let (lo, hi) = (r.get("start")?.uint()?, r.get("end")?.uint()?);
            if !frames.contains(id)
                || lo >= hi
                || prior
                    .entry(id)
                    .or_default()
                    .iter()
                    .any(|(a, b)| lo < *b && *a < hi)
            {
                return err("§9.4", "invalid or overlapping non-slot frame live range");
            }
            prior.entry(id).or_default().push((lo, hi));
        }
    }
    Ok(())
}
fn table09(c: &Json, f: &Function) -> Result<()> {
    let expected = c.get("expected")?;
    let Some(table) = expected.object().ok().and_then(|m| m.get("table")) else {
        return Ok(());
    };
    let controls = c.get("subject")?.get("inherited_controls")?.uint()?;
    let widths = f
        .params
        .iter()
        .flatten()
        .filter_map(|p| {
            if let Type::Wire(w) = p.ty {
                Some(w as u128)
            } else {
                None
            }
        })
        .collect::<Vec<_>>();
    let borrowed = c
        .get("domain")?
        .get("borrowed")?
        .array()?
        .iter()
        .map(|p| p.get("width")?.uint())
        .collect::<Result<Vec<_>>>()?;
    let regions = f
        .params
        .iter()
        .flatten()
        .filter_map(|p| {
            if let Type::Region(a, w) = p.ty {
                Some((a, w))
            } else {
                None
            }
        })
        .collect::<Vec<_>>();
    let mut before = BTreeSet::new();
    for row in table.array()? {
        if !before.insert(row.get("before")?.canonical()) {
            return err("§12.1 K13", "duplicate table input tuple");
        }
        for key in ["before", "after"] {
            let tuple = row.get(key)?;
            let bundles = tuple.get("bundles")?.array()?;
            if controls
                .checked_add(widths.len() as u128)
                .is_none_or(|n| n != bundles.len() as u128)
            {
                return err("§12.1 K13", "incomplete table bundle tuple");
            }
            for (i, b) in bundles.iter().enumerate() {
                let w = if (i as u128) < controls {
                    1
                } else {
                    widths[i - controls as usize]
                };
                crate::object::unsigned_literal(b.string()?, w)?;
            }
            let values = tuple.get("borrowed")?.array()?;
            if values.len() != borrowed.len() {
                return err("§12.1 K13", "incomplete borrowed tuple");
            }
            for (v, w) in values.iter().zip(&borrowed) {
                crate::object::unsigned_literal(v.string()?, *w)?;
            }
            let cells = tuple.get("regions")?.array()?;
            if cells.len() != regions.len() {
                return err("§12.1 K13", "incomplete region tuple");
            }
            for (r, (a, w)) in cells.iter().zip(&regions) {
                let values = r.array()?;
                if crate::oracle::power_of_two(*a as u128) != Some(values.len() as u128) {
                    return err("§12.1 K13", "incomplete region cells");
                }
                for v in values {
                    crate::object::unsigned_literal(v.string()?, *w as u128)?;
                }
            }
        }
    }
    Ok(())
}

pub(crate) fn invocation_budget(value: &Json) -> Result<crate::Budget> {
    let v = value.array()?;
    let n = v
        .iter()
        .map(|v| {
            v.string()?.parse::<u128>().map_err(|_| {
                crate::resource_error("§12.3 K13", "invocation component exceeds u128")
            })
        })
        .collect::<Result<Vec<_>>>()?;
    Ok(crate::Budget {
        steps: u64::try_from(n[0])
            .map_err(|_| crate::resource_error("§12.3 K13", "invocation steps exceed u64"))?,
        heap: n[1],
        stack: n[2],
        depth: n[3],
    })
}

#[cfg(test)]
fn domain(value: &Json, f: &Function) -> Result<()> {
    domain_for(value, f, crate::IsaVersion::V08, 0)
}
pub(crate) fn domain_for(
    value: &Json,
    f: &Function,
    version: crate::IsaVersion,
    controls: u128,
) -> Result<()> {
    let mut names = BTreeSet::new();
    for group in ["bundles", "borrowed"] {
        let entries = value.get(group)?.array()?;
        if group == "bundles" && (entries.len() as u128) < controls {
            return err("§12.2 K72", "domain omits inherited control positions");
        }
        for (position, b) in entries.iter().enumerate() {
            let inherited = group == "bundles" && (position as u128) < controls;
            let name = text(b.get("name")?)?;
            let label_only =
                inherited || (version == crate::IsaVersion::V09 && group == "borrowed");
            if !label_only && !names.insert((group, name.to_string())) {
                return err("§12.2", "repeated domain component");
            }
            let width = b.get("width")?.uint()?;
            if width == 0 || (inherited && width != 1) {
                return err("§12.2", "zero-width domain component");
            }
            // Admission compares the spelling's magnitude, never allocates width
            // bits for an endpoint. Resource errors retain their own diagnostic.
            let lo = b.get("lo")?.uint_text()?;
            let hi = b.get("hi")?.uint_text()?;
            crate::object::unsigned_literal(lo, width)?;
            crate::object::unsigned_literal(hi, width)?;
            if (lo.len(), lo) > (hi.len(), hi) {
                return err("§12.2", "domain interval with lo > hi");
            }
            if group == "bundles" && !inherited {
                let p = f
                    .params
                    .iter()
                    .flatten()
                    .find(|p| p.name == name && matches!(p.ty, Type::Wire(_)))
                    .ok_or_else(|| Error::new("§12.2: unknown domain interface bundle".into()))?;
                if p.ty.width(32)? as u128 != width {
                    return err("§12.2", "domain bundle width mismatch");
                }
            }
        }
    }
    for region in value.get("regions")?.array()? {
        let name = text(region.get("name")?)?;
        if !names.insert(("regions", name.to_string())) {
            return err("§12.2", "repeated domain region");
        }
        let (a, w) = f
            .params
            .iter()
            .flatten()
            .find_map(|p| {
                if p.name == name {
                    if let Type::Region(a, w) = p.ty {
                        Some((a, w))
                    } else {
                        None
                    }
                } else {
                    None
                }
            })
            .ok_or_else(|| Error::new("§12.2: unknown domain interface region".into()))?;
        if w == 0 {
            return err("§12.2", "zero-width domain cell");
        }
        let cells = region.get("cells")?;
        if cells == &Json::String("all".into()) {
            continue;
        }
        let mut indices = BTreeSet::new();
        for cell in cells.array()? {
            let index = cell.get("index")?.uint()?;
            let lo = cell.get("lo")?.uint_text()?;
            let hi = cell.get("hi")?.uint_text()?;
            crate::object::unsigned_literal(lo, w as u128)?;
            crate::object::unsigned_literal(hi, w as u128)?;
            if crate::oracle::power_of_two(a as u128).is_some_and(|cells| index >= cells)
                || !indices.insert(index)
                || (lo.len(), lo) > (hi.len(), hi)
            {
                return err("§12.2", "invalid domain cell interval");
            }
        }
    }
    Ok(())
}
fn index(value: &Json, count: usize) -> Result<usize> {
    let n = usize::try_from(value.uint()?)
        .map_err(|_| Error::new("§12: claim index exceeds host range".into()))?;
    if n >= count {
        return err("§12", "claim index out of range or cyclic subclaim");
    }
    Ok(n)
}
fn subject(value: &Json) -> Result<()> {
    hash(value.get("closure_hash")?)?;
    if let Some(h) = value.object()?.get("schedule_hash") {
        hash(h)?;
    }
    variant(value.get("variant")?)?;
    value.get("inherited_controls")?.uint()?;
    Ok(())
}
impl Object {
    pub(crate) fn validate_invocation09(&self, v: &Json, f: &Function) -> Result<Vec<u64>> {
        crate::metadata_schema::validate_for(self.isa_version, "invocation09", v)?;
        self.validate_budget(invocation_budget(v.get("budget")?)?)?;
        let args = v.get("args")?.array()?;
        let groups: &[usize] = match f.kind.as_str() {
            "oracle" => &[4],
            "action" | "perm_action" => &[3],
            "lproc" => &[2, 3],
            "cc" | "r" => &[0],
            _ => return err("§12.3 K13", "invocation must bind a function"),
        };
        let params = groups
            .iter()
            .flat_map(|g| &f.params[*g])
            .filter(|p| matches!(p.ty, Type::Int(_) | Type::Ptr | Type::F64 | Type::Token))
            .collect::<Vec<_>>();
        if args.len() != params.len() {
            return err("§12.3 K13", "invocation argument count mismatch");
        }
        for (a, p) in args.iter().zip(&params) {
            match p.ty {
                Type::Int(w) => {
                    crate::metadata_schema::validate_for(
                        self.isa_version,
                        "canonical_decimal09",
                        a,
                    )?;
                    crate::object::unsigned_literal(a.string()?, w as u128)?;
                }
                Type::Ptr => {
                    crate::metadata_schema::validate_for(
                        self.isa_version,
                        "canonical_decimal09",
                        a,
                    )?;
                    crate::object::unsigned_literal(a.string()?, self.ptr_width as u128)?;
                }
                Type::Token => self.validate_budget(invocation_budget(a)?)?,
                Type::F64 => {
                    let t = a.string()?;
                    if t.len() != 18
                        || !t.starts_with("0x")
                        || !t[2..]
                            .bytes()
                            .all(|c| c.is_ascii_digit() || (b'a'..=b'f').contains(&c))
                    {
                        return err("§12.3 K13", "invalid f64 bit pattern");
                    }
                }
                _ => unreachable!(),
            }
        }
        let mut tokens = Vec::new();
        if f.kind == "oracle" {
            tokens.push(Some(invocation_budget(v.get("budget")?)?));
        }
        let mut argument_tokens = 0;
        for (a, p) in args.iter().zip(&params) {
            if p.ty == Type::Token {
                tokens.push(Some(invocation_budget(a)?));
                argument_tokens += 1;
            }
        }
        crate::tokens::alias_binding(
            v.object()?.get("token_aliases"),
            &tokens,
            argument_tokens == 0,
        )
    }
    pub(crate) fn validate_certificate_details(&self, c: &Json) -> Result<()> {
        crate::metadata_schema::validate_for(self.isa_version, "certificate", c)?;
        contextual("§12", || {
            let b = c.get("bindings")?;
            let identity = self.identity()?;
            if b.get("object_hash")?.string()? != identity.object_hash {
                return err("§12", "certificate object hash mismatch");
            }
            let interface = hash(b.get("interface_hash")?)?;
            if !identity.interface_hashes.values().any(|h| h == interface) {
                return err("§12", "certificate interface hash binding mismatch");
            }
            if !identity.closure_hashes.values().any(|h| {
                h.as_deref() == Some(b.get("closure_hash").and_then(Json::string).unwrap_or(""))
            }) {
                return err("§12", "certificate closure hash binding mismatch");
            }
            if let Some(schedule_hash) = b.object()?.get("schedule_hash") {
                hash(schedule_hash)?;
                if let Some(s) = self.section("schedule") {
                    if schedule_hash.string()? != sha256_hex(s.canonical().as_bytes()) {
                        return err("§12", "certificate schedule hash mismatch");
                    }
                }
            }
            if self.isa_version == crate::IsaVersion::V09 {
                let root = identity
                    .closure_hashes
                    .iter()
                    .find_map(|(n, h)| {
                        (h.as_deref()
                            == Some(b.get("closure_hash").and_then(Json::string).unwrap_or("")))
                        .then_some(n)
                    })
                    .ok_or_else(|| {
                        Error::new("§12.3: certificate root closure is not defined".into())
                    })?;
                let root_function = self.functions.get(root).ok_or_else(|| {
                    Error::new("§12.3: certificate root must name a function, not data".into())
                })?;
                let invocation = b.object()?.get("invocation");
                if self.section("schedule").is_some() && invocation.is_none() {
                    return err("§12.3 K13", "scheduled certificate requires invocation");
                }
                if let Some(v) = invocation {
                    let invocation_aliases = self.validate_invocation09(v, root_function)?;
                    if let Some(schedule) = self.section("schedule") {
                        let sb = schedule.get("bindings")?;
                        let values = v.get("budget")?.array()?;
                        for (actual, wanted) in values.iter().zip(sb.get("budget")?.array()?) {
                            if actual.string()? != wanted.uint_text()? {
                                return err("§12.3 K13", "invocation and schedule budget differ");
                            }
                        }
                        if sha256_hex(v.get("args")?.canonical().as_bytes())
                            != sb.get("params_hash")?.string()?
                        {
                            return err("§12.3 K13", "invocation params hash mismatch");
                        }
                        let implicit = if root_function.kind == "oracle" {
                            invocation_aliases.len() == 1
                        } else {
                            invocation_aliases.is_empty()
                        };
                        let tuples = vec![None; invocation_aliases.len()];
                        let schedule_aliases = crate::tokens::alias_binding(
                            sb.object()?.get("token_aliases"),
                            &tuples,
                            implicit,
                        )?;
                        if invocation_aliases != schedule_aliases {
                            return err(
                                "§12.3 K91",
                                "invocation and schedule token_aliases differ",
                            );
                        }
                    }
                }
            }
            for (closure, r) in c.get("regions")?.object()? {
                hash(&Json::String(closure.clone()))?;
                let name = identity
                    .closure_hashes
                    .iter()
                    .find_map(|(n, h)| (h.as_deref() == Some(closure.as_str())).then_some(n))
                    .ok_or_else(|| Error::new("§12: region closure is not defined".into()))?;
                let f = self
                    .functions
                    .get(name)
                    .ok_or_else(|| Error::new("§12: certificate region is data".into()))?;
                if r.get("kind")?.string()? != f.kind
                    || r.get("signature")? != &f.signature_for(self.isa_version)
                {
                    return err("§12", "region signature mismatch");
                }
                let bounds = r
                    .get("bounds")?
                    .array()?
                    .iter()
                    .map(Json::uint)
                    .collect::<Result<Vec<_>>>()?;
                if bounds != f.bounds.iter().map(|n| *n as u128).collect::<Vec<_>>() {
                    return err("§12", "certificate bounds mismatch");
                }
                if self.isa_version == crate::IsaVersion::V09 {
                    let mut counts = r
                        .get("error")?
                        .object()?
                        .keys()
                        .map(|key| context_key(key).map(|(_, n)| n))
                        .collect::<Result<Vec<_>>>()?;
                    if counts.is_empty() {
                        counts.push(0);
                    }
                    frame09(r.get("frame")?, f, &counts)?;
                } else {
                    frame(r.get("frame")?)?;
                }
                let claims = r.get("claims")?.array()?;
                for (position, claim) in claims.iter().enumerate() {
                    self.validate_claim(claim, f, position)?;
                }
                let v = r.get("verification")?;
                if v.get("oracle")? != &Json::Null {
                    index(v.get("oracle")?, claims.len())?;
                }
                for group in ["borrow_frames", "unitary", "channel"] {
                    for claim in v.get(group)?.array()? {
                        index(claim, claims.len())?;
                    }
                }
                for pair in v.get("inverse_pairs")?.array()? {
                    index(pair.get("claim")?, claims.len())?;
                }
                let fault = v.get("fault_rate")?;

                domain_for(fault.get("domain")?, f, self.isa_version, 0)?;
                if self.isa_version == crate::IsaVersion::V09 {
                    self.validate_image_domains09(fault.get("domain")?, f)?;
                }
                for (code, count) in fault.get("faults_by_code")?.object()? {
                    code.parse::<u128>()
                        .map_err(|_| Error::new("§12: invalid fault code key".into()))?;
                    count.uint()?;
                }
                fault.get("undefined_excluded")?.uint()?;
                fault.get("layout_dependent_excluded")?.uint()?;
                for (key, cleanups) in r.get("cleanup")?.object()? {
                    context_key(key)?;
                    for cleanup in cleanups.array()? {
                        self.validate_path(cleanup.get("path")?, Some(name))?;
                    }
                }
                for key in r.get("error")?.object()?.keys() {
                    context_key(key)?;
                }
            }
            let composition = c.get("composition")?;
            for (key, n) in composition.get("multiplicities")?.object()? {
                let (closure, context) = key
                    .split_once(':')
                    .ok_or_else(|| Error::new("§12.3: malformed multiplicity key".into()))?;
                hash(&Json::String(closure.into()))?;
                context_key(context)?;
                n.uint()?;
            }
            Ok(())
        })
    }
    fn validate_claim(&self, c: &Json, f: &Function, position: usize) -> Result<()> {
        crate::metadata_schema::validate_for(self.isa_version, "claim", c)?;
        if self.isa_version == crate::IsaVersion::V09
            && c.object()?.get("expected") == Some(&Json::String("inverse_pair".into()))
        {
            return self.validate_inverse_pair_claim09(f, position, c);
        }
        if self.isa_version == crate::IsaVersion::V09 {
            if let Some(d) = c.object()?.get("domain") {
                self.validate_image_domains09(d, f)?;
            }
            let inverse_pair =
                c.object()?.get("expected") == Some(&Json::String("inverse_pair".into()));
            let subject_schedule = c
                .object()?
                .get("subject")
                .and_then(|s| s.object().ok())
                .and_then(|s| s.get("schedule_hash"));
            if let Some(bound_hash) = subject_schedule {
                let schedule = self
                    .section("schedule")
                    .ok_or_else(|| Error::new("§12.1 K13: claim schedule is absent".into()))?;
                if bound_hash.string()? != sha256_hex(schedule.canonical().as_bytes()) {
                    return err("§12.1 K13", "claim schedule hash mismatch");
                }
            }
            if c.object()?.get("expected") == Some(&Json::String("oracle".into()))
                && subject_schedule.is_none()
            {
                return err(
                    "§12.1 K13",
                    "expected:oracle requires subject.schedule_hash",
                );
            }
            if matches!(c.get("kind")?.string()?, "exhaustive" | "sampled") {
                table09(c, f)?;
            }
            if let Some(v) = c.object()?.get("invocation") {
                if v.get("args")? != &Json::String("all".into()) {
                    self.validate_invocation09(v, f)?;
                } else if f.params.iter().flatten().any(|p| p.ty == Type::Token)
                    && v.object()?.get("token_aliases") != Some(&Json::String("all".into()))
                {
                    return err(
                        "§12.3 K91",
                        "uniform token arguments require token_aliases:all",
                    );
                }
            } else if subject_schedule.is_none()
                && !inverse_pair
                && matches!(
                    c.get("kind")?.string()?,
                    "exhaustive" | "sampled" | "structural"
                )
            {
                return err("§12.3 K13", "standalone claim requires invocation");
            }
        }
        // §12.1–12.2: domain/name bindings, executable subjects and acyclic
        // indices need the enclosing function/claim list, beyond the grammar.
        match c.get("kind")?.string()? {
            "exhaustive" => {
                let controls = if self.isa_version == crate::IsaVersion::V09 {
                    c.get("subject")?.get("inherited_controls")?.uint()?
                } else {
                    0
                };
                domain_for(c.get("domain")?, f, self.isa_version, controls)?;
                if c.get("expected")? == &Json::String("oracle".into()) {
                    subject(c.get("subject")?)?;
                }
            }
            "sampled" => {
                let controls = if self.isa_version == crate::IsaVersion::V09 {
                    c.get("subject")?.get("inherited_controls")?.uint()?
                } else {
                    0
                };
                domain_for(c.get("domain")?, f, self.isa_version, controls)?;
                if !c
                    .get("sampler")?
                    .get("seed")?
                    .array()?
                    .iter()
                    .any(|w| w.string().is_ok_and(|s| s.bytes().any(|b| b != b'0')))
                {
                    return err("§12.1", "all-zero sampler seed");
                }
            }
            "structural" => {
                for claim in c.get("subclaims")?.array()? {
                    index(claim, position)?;
                }
            }
            "numerical" | "channel" => {
                subject(c.get("subject")?)?;
                if c.get("precision_bits")?.uint()? == 0 {
                    return err("§12.1", "precision must be positive");
                }
            }
            _ => return err("§12.1", "unknown certificate claim kind"),
        }
        Ok(())
    }
}

#[cfg(test)]
mod r20_tests {
    use super::*;
    #[test]
    fn r20_region_domain_extremes() {
        let values = [0u64, 1, (1 << 63) - 1, 1 << 63, u64::MAX - 1, u64::MAX];
        let mut cases = 0;
        for n in values {
            for path in ["A", "W", "index", "lo", "hi"] {
                let (a, w, index, lo, hi) = match path {
                    "A" => (n, 1, 0, 0, 1),
                    "W" => (0, n, 0, 0, 1),
                    "index" => (1, 1, n, 0, 1),
                    "lo" => (0, 1, 0, n, n),
                    _ => (0, 1, 0, 0, n),
                };
                let mut f = Function::from_signature("o", &Json::parse(r#"{"abi":"0.8","args":[],"fault":4,"in":[],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}"#).unwrap()).unwrap();
                f.params[3].push(crate::Param {
                    name: "r".into(),
                    ty: Type::Region(a, w),
                    role: Some("in".into()),
                });
                let meta = |n: u64| {
                    if n <= 9_007_199_254_740_991 {
                        n.to_string()
                    } else {
                        format!("\"{n}\"")
                    }
                };
                let d = Json::parse(&format!(r#"{{"bundles":[],"borrowed":[],"regions":[{{"name":"r","cells":[{{"index":{},"lo":{},"hi":{}}}]}}]}}"#,meta(index),meta(lo),meta(hi))).unwrap();
                let admit = match path {
                    "A" => true,
                    "W" => n > 0,
                    "index" => n < 2,
                    _ => n < 2,
                };
                let result = std::panic::catch_unwind(|| domain(&d, &f)).expect("no domain panic");
                if admit {
                    result.unwrap();
                } else {
                    let e = result.unwrap_err().to_string();
                    assert!(
                        e.contains('§') && !e.contains("host limit"),
                        "{path}={n}: {e}"
                    );
                }
                cases += 1;
            }
        }
        assert_eq!(cases, 30);
        eprintln!("R20 region domains: 5 paths, {cases} cases");
    }
}

#[cfg(test)]
mod frame09_tests {
    use super::*;
    #[test]
    fn invocation_binds_classical_parameters_and_excludes_results_and_handles() {
        let mut o = Object::parse(include_str!("../tests/fixtures/inc8.bisa")).unwrap();
        o.isa_version = crate::IsaVersion::V09;
        let f=Function::from_signature("entry",&Json::parse(r#"{"abi":"0.9","kind":"cc","tier":"cc","params":["qreg[2]","i8"],"results":["i8"]}"#).unwrap()).unwrap();
        let invocation = Json::parse(r#"{"args":["7"],"budget":["0","0","0","0"]}"#).unwrap();
        o.validate_invocation09(&invocation, &f).unwrap();
        let extra = Json::parse(r#"{"args":["7","8"],"budget":["0","0","0","0"]}"#).unwrap();
        assert!(o.validate_invocation09(&extra, &f).is_err());
    }

    #[test]
    fn published_frame_witness_uses_exact_control_widths_and_disjoint_ranges() {
        let value=Json::parse(r#"{"ancillae":[{"class":"fast","id":"a","scheme":"controlled-x","state":"clean","width":{"var":"c"}}],"borrow":[{"class":"fast","id":"b","width":1}],"history":[{"class":"fast","id":"h","width":3}],"live_ranges":[{"end":2,"frame":"s","start":0},{"end":4,"frame":"s","start":2}],"scratch":[{"class":"fast","id":"s","state":"clean","width":{"args":[2,{"var":"c"}],"op":"+"}}],"slots":[{"class":"fast","id":"mut:0","role":"mut","width":2},{"class":"fast","id":"in:0","role":"in","width":1}]}"#).unwrap();
        let f=Function::from_signature("a", &Json::parse(r#"{"abi":"0.9","tier":"q","kind":"action","args":[],"bounds":[],"mut":[2],"in":[1],"mem":[]}"#).unwrap()).unwrap();
        crate::metadata_schema::validate_for(crate::IsaVersion::V09, "frame", &value).unwrap();
        frame09(&value, &f, &[0, 2, 9]).unwrap();
        assert_eq!(
            frame_width(
                value.get("scratch").unwrap().array().unwrap()[0]
                    .get("width")
                    .unwrap(),
                2
            )
            .unwrap(),
            4
        );
        assert_eq!(
            frame_width(
                value.get("ancillae").unwrap().array().unwrap()[0]
                    .get("width")
                    .unwrap(),
                2
            )
            .unwrap(),
            2
        );
        for (text, want) in [
            ("1e+3", 1000),
            (r#"{"op":"ceil","args":[{"op":"/","args":[5,2]}]}"#, 3),
            (r#"{"op":"max","args":[{"var":"c"},2]}"#, 2),
            (r#"{"op":"min","args":[{"var":"c"},2]}"#, 2),
            (r#"{"op":"*","args":[1.5,2]}"#, 3),
        ] {
            assert_eq!(frame_width(&Json::parse(text).unwrap(), 2).unwrap(), want);
        }
        for text in [
            r#"{"var":"k"}"#,
            r#"{"table":"t","index":"k"}"#,
            r#"{"op":"/","args":[1,0]}"#,
            r#"{"op":"/","args":[1,2]}"#,
            r#"{"op":"-","args":[0,1]}"#,
        ] {
            assert!(
                frame_width(&Json::parse(text).unwrap(), 2).is_err(),
                "{text}"
            );
        }
    }
}
````

## `reference-interpreter/src/claims/pairs09.rs` (479 lines)

````rust
//! K4's entry-bound relation is separate from ordinary K13 tuple replay.
use super::*;
use crate::{Argument, OracleVectorInput, OracleVectorMachine};
pub(super) struct Pair<'a> {
    pub(super) g: &'a Function,
    pub(super) gi: &'a Function,
    pub(super) budget: Budget,
    pub(super) tokens: BTreeMap<String, Budget>,
    pub(super) aliases: Vec<u64>,
}
fn entry_budget(value: &Json) -> Result<Budget> {
    let v = value.array()?;
    if v.len() != 4 {
        return err("§12.3 K4", "inverse-pair budget requires four components");
    }
    Ok(Budget {
        steps: u64::try_from(v[0].uint()?)
            .map_err(|_| crate::resource_error("§12.3 K4", "entry steps exceed host u64"))?,
        heap: v[1].uint()?,
        stack: v[2].uint()?,
        depth: v[3].uint()?,
    })
}
pub(super) fn pair<'a>(object: &'a Object, entry: &Json) -> Result<Pair<'a>> {
    let g = object.region_function(entry.get("g")?.string()?)?;
    let gi = object.region_function(entry.get("ginv")?.string()?)?;
    if g.kind != "oracle"
        || gi.kind != "oracle"
        || g.params[0].is_empty()
        || g.params
            .iter()
            .take(5)
            .map(|ps| ps.iter().map(|p| p.ty.clone()).collect::<Vec<_>>())
            .collect::<Vec<_>>()
            != gi
                .params
                .iter()
                .take(5)
                .map(|ps| ps.iter().map(|p| p.ty.clone()).collect::<Vec<_>>())
                .collect::<Vec<_>>()
        || g.params[0][0].ty != g.params[1][0].ty
    {
        return err(
            "§12.3 K4",
            "inverse-pair oracle signatures are incompatible",
        );
    }
    let budget = entry_budget(entry.get("budget")?)?;
    object.validate_budget(budget)?;
    let tokens = entry
        .object()?
        .get("arg_tokens")
        .map(|v| {
            v.object()?
                .iter()
                .map(|(n, b)| Ok((n.clone(), entry_budget(b)?)))
                .collect::<Result<BTreeMap<_, _>>>()
        })
        .transpose()?
        .unwrap_or_default();
    let expected = g.params[4]
        .iter()
        .filter(|p| p.ty == Type::Token)
        .map(|p| p.name.as_str())
        .collect::<BTreeSet<_>>();
    if tokens.keys().map(String::as_str).collect::<BTreeSet<_>>() != expected {
        return err(
            "§12.3 K4",
            "arg_tokens must bind exactly the token-typed oracle arguments",
        );
    }
    for b in tokens.values() {
        object.validate_budget(*b)?;
    }
    let mut tuples = vec![Some(budget)];
    tuples.extend(
        g.params[4]
            .iter()
            .filter(|p| p.ty == Type::Token)
            .map(|p| Some(tokens[&p.name])),
    );
    let aliases = crate::tokens::alias_binding(
        entry.object()?.get("token_aliases"),
        &tuples,
        expected.is_empty(),
    )?;
    Ok(Pair {
        g,
        gi,
        budget,
        tokens,
        aliases,
    })
}
pub(super) fn args_domain(
    object: &Object,
    f: &Function,
    domain: &Json,
) -> Result<Vec<(usize, BitVector, BitVector)>> {
    let mut args = Vec::new();
    let mut seen = BTreeSet::new();
    if let Some(ranges) = domain.object()?.get("args") {
        for range in ranges.array()? {
            let name = range.get("name")?.string()?;
            let index = f.params[4]
                .iter()
                .position(|p| p.name == name)
                .ok_or_else(|| Error::new(format!("§12.2 K4: unknown argument {name}")))?;
            let p = &f.params[4][index];
            if p.ty == Type::Token || !seen.insert(index) {
                return err("§12.2 K4", "token/repeated argument in args domain");
            }
            let width = p.ty.bits(object.ptr_width)?;
            if range.get("width")?.uint()? != width as u128 {
                return err("§12.2 K4", "argument domain width differs");
            }
            let lo = json_bits(range.get("lo")?, width)?;
            let hi = json_bits(range.get("hi")?, width)?;
            if lo.unsigned_cmp(&hi)? == std::cmp::Ordering::Greater {
                return err("§12.2 K4", "argument domain has lo > hi");
            }
            args.push((index, lo, hi));
        }
    }
    Ok(args)
}
fn full_quantum_domain(object: &Object, g: &Function, domain: &Json) -> Result<()> {
    crate::certificate::domain_for(domain, g, crate::IsaVersion::V09, 0)?;
    if !domain.get("borrowed")?.array()?.is_empty()
        || domain
            .object()?
            .get("fixed_regions")
            .is_some_and(|v| v.array().is_ok_and(|v| !v.is_empty()))
    {
        return err(
            "§12.2 K4/K85",
            "inverse-pair relation requires unrestricted inputs and memory",
        );
    }
    let mut inputs = BTreeSet::new();
    for b in domain.get("bundles")?.array()? {
        let n = b.get("name")?.string()?;
        let p = g.params[0].iter().find(|p| p.name == n).ok_or_else(|| {
            Error::new("§12.2 K4: inverse-pair bundles are oracle inputs only".into())
        })?;
        let w = p.ty.bits(object.ptr_width)?;
        if !inputs.insert(n)
            || !json_bits(b.get("lo")?, w)?.is_zero()
            || json_bits(b.get("hi")?, w)? != ones(w)?
        {
            return err("§12.2 K4", "inverse-pair input domain must be full");
        }
    }
    if inputs.len() != g.params[0].len() {
        return err("§12.2 K4", "inverse-pair domain omits input slots");
    }
    let mut memory = BTreeSet::new();
    for r in domain.get("regions")?.array()? {
        let name = r.get("name")?.string()?;
        let p = g.params[3]
            .iter()
            .find(|p| p.name == name)
            .ok_or_else(|| Error::new("§12.2 K4: unknown inverse-pair region".into()))?;
        if !memory.insert(name) {
            return err("§12.2 K4", "repeated inverse-pair region");
        }
        let Type::Region(a, w) = p.ty else {
            return err("§12.2 K4", "expected region type");
        };
        if r.get("cells")? != &Json::String("all".into()) {
            let cells = r.get("cells")?.array()?;
            if crate::oracle::power_of_two(a as u128) != Some(cells.len() as u128) {
                return err("§12.2 K4", "inverse-pair domain omits cells");
            }
            for c in cells {
                if !json_bits(c.get("lo")?, w as usize)?.is_zero()
                    || json_bits(c.get("hi")?, w as usize)? != ones(w as usize)?
                {
                    return err("§12.2 K4", "inverse-pair cell domain must be full");
                }
            }
        }
    }
    if memory.len() != g.params[3].len() {
        return err("§12.2 K4", "inverse-pair domain omits regions");
    }
    args_domain(object, g, domain)?;
    Ok(())
}
impl Object {
    /// Resolve the pair theorem, retaining its domain through library reuse.
    /// Every link must bind the same closures and a covered token context.
    pub(super) fn inverse_pair_theorem09(
        &self,
        closure: &str,
        index: usize,
        active: &mut BTreeSet<(String, usize)>,
    ) -> Result<Option<(&Json, &Function)>> {
        let key = (closure.to_string(), index);
        if !active.insert(key.clone()) {
            return err("§12.1 K4", "cyclic inverse-pair library reference");
        }
        let regions = self
            .section("certificate")
            .unwrap()
            .get("regions")?
            .object()?;
        let Some(record) = regions.get(closure) else {
            return Ok(None);
        };
        let claim = record
            .get("claims")?
            .array()?
            .get(index)
            .ok_or_else(|| Error::new("§12.1 K4: library claim index out of range".into()))?;
        let owner = self.region_function(closure)?;
        let entries = self.pair_claim_entries(owner, index)?;
        let result = match claim.get("kind")?.string()? {
            "exhaustive" if claim.get("expected")? == &Json::String("inverse_pair".into()) => {
                self.validate_inverse_pair_claim09(owner, index, claim)?;
                Some((claim, pair(self, entries[0])?.g))
            }
            "structural" if claim.get("rule")?.string()? == "inverse_pair_library" => {
                let witness = claim.get("witness")?;
                let library = witness.get("library_closure_hash")?.string()?;
                let donor_index = usize::try_from(witness.get("claim_index")?.uint()?)
                    .map_err(|_| crate::resource_error("§12.1 K4", "claim index exceeds host"))?;
                let Some(theorem) = self.inverse_pair_theorem09(library, donor_index, active)?
                else {
                    return Ok(None);
                };
                let donor = self.region_function(library)?;
                let donor_entries = self.pair_claim_entries(donor, donor_index)?;
                for entry in entries {
                    let current = pair(self, entry)?;
                    let mut covered = false;
                    for donor_entry in &donor_entries {
                        let source = pair(self, donor_entry)?;
                        let (g, gi) = (entry.get("g")?, entry.get("ginv")?);
                        let (sg, si) = (donor_entry.get("g")?, donor_entry.get("ginv")?);
                        let same_pair = (g == sg && gi == si) || (g == si && gi == sg);
                        covered |= same_pair
                            && current.budget.steps >= source.budget.steps
                            && current.budget.heap >= source.budget.heap
                            && current.budget.stack >= source.budget.stack
                            && current.budget.depth >= source.budget.depth
                            && current.aliases == source.aliases
                            && current.g.params[4]
                                .iter()
                                .filter(|p| p.ty == Type::Token)
                                .map(|p| current.tokens[&p.name])
                                .eq(source.g.params[4]
                                    .iter()
                                    .filter(|p| p.ty == Type::Token)
                                    .map(|p| source.tokens[&p.name]));
                    }
                    if !covered {
                        return err(
                            "§12.1 K4",
                            "library theorem must cover the same resolved pair and token context",
                        );
                    }
                }
                Some(theorem)
            }
            _ => {
                return err(
                    "§12.1 K4",
                    "entry claim is not an exhaustive or linked-library inverse-pair theorem",
                )
            }
        };
        active.remove(&key);
        Ok(result)
    }
    fn pair_claim_entries(&self, owner: &Function, index: usize) -> Result<Vec<&Json>> {
        let closure = self.identity()?.closure_hashes[&owner.name]
            .clone()
            .ok_or_else(|| Error::new("§12.3 K4: unlinked pair owner".into()))?;
        let record = self
            .section("certificate")
            .ok_or_else(|| Error::new("§12.3 K4: absent certificate".into()))?
            .get("regions")?
            .get(&closure)?;
        let entries = record
            .get("verification")?
            .get("inverse_pairs")?
            .array()?
            .iter()
            .filter(|entry| entry.get("claim").and_then(Json::uint) == Ok(index as u128))
            .collect::<Vec<_>>();
        if entries.is_empty() {
            return err(
                "§12.3 K4",
                "inverse-pair claim has no owner-local entry binding",
            );
        }
        Ok(entries)
    }
    pub(crate) fn validate_inverse_pair_claim09(
        &self,
        owner: &Function,
        index: usize,
        claim: &Json,
    ) -> Result<()> {
        if claim.get("kind")?.string()? != "exhaustive" {
            return err("§12.1 K4", "inverse-pair relation is exhaustive");
        }
        if let Some(subject) = claim.object()?.get("subject") {
            if self.identity()?.closure_hashes[&owner.name].as_deref()
                != Some(subject.get("closure_hash")?.string()?)
            {
                return err("§12.1 K4", "inverse-pair subject differs from its owner");
            }
        }
        for entry in self.pair_claim_entries(owner, index)? {
            let p = pair(self, entry)?;
            full_quantum_domain(self, p.g, claim.get("domain")?)?;
        }
        Ok(())
    }
    pub(super) fn verify_inverse_pair_claim09(
        &self,
        owner: &Function,
        index: usize,
        claim: &Json,
    ) -> Result<ClaimVerdict> {
        self.validate_inverse_pair_claim09(owner, index, claim)?;
        let key = format!(
            "{}:{}:{}:{}",
            self.identity()?.object_hash,
            self.identity()?.closure_hashes[&owner.name]
                .as_deref()
                .unwrap_or(""),
            index,
            crate::sha256_hex(self.section("certificate").unwrap().canonical().as_bytes())
        );
        if self
            .pair_proofs
            .lock()
            .map_err(|_| Error::new("§12.1 K4: proof cache poisoned".into()))?
            .contains(&key)
        {
            return Ok(ClaimVerdict::Proof);
        }
        for entry in self.pair_claim_entries(owner, index)? {
            let p = pair(self, entry)?;
            let mut domain = self.domain(p.g, claim.get("domain")?)?;
            let quantum = domain.components.len();
            let ranges = args_domain(self, p.g, claim.get("domain")?)?;
            for (index, lo, hi) in &ranges {
                domain.components.push((
                    Component::Bundle(4, *index),
                    lo.width(),
                    lo.clone(),
                    hi.clone(),
                ));
            }
            for row in enumerate(&domain)? {
                let mut input = OracleVectorInput {
                    ins: p.g.params[0]
                        .iter()
                        .map(|p| BitVector::zero(p.ty.bits(self.ptr_width)?))
                        .collect::<Result<_>>()?,
                    ..Default::default()
                };
                for param in &p.g.params[3] {
                    let Type::Region(a, _) = param.ty else {
                        return err("§12.2 K4", "expected region");
                    };
                    let count = crate::oracle::power_of_two(a as u128)
                        .and_then(|n| usize::try_from(n).ok())
                        .ok_or_else(|| {
                            crate::resource_error("§12.2 K4", "region capacity exceeds host")
                        })?;
                    let mut bytes = crate::reserved(count, "§12.2 K4", "pair region bytes")?;
                    bytes.resize(count, 0);
                    input.regions.insert(param.name.clone(), bytes);
                }
                for ((component, ..), value) in
                    domain.components[..quantum].iter().zip(&row[..quantum])
                {
                    match component {
                        Component::Bundle(0, slot) => input.ins[*slot] = value.clone(),
                        Component::Cell(3, slot, cell) => {
                            input.regions.get_mut(&p.g.params[3][*slot].name).unwrap()[*cell] =
                                u8::try_from(value.to_u128()?).map_err(|_| {
                                    Error::new("§12.2 K4: oracle region cell exceeds byte".into())
                                })?
                        }
                        _ => return err("§12.2 K4", "unexpected inverse-pair component"),
                    }
                }
                let mut values = p.g.params[4]
                    .iter()
                    .map(|param| {
                        if param.ty == Type::Token {
                            Ok(Argument::Token(p.tokens[&param.name]))
                        } else if param.ty == Type::F64 {
                            Ok(Argument::Float(0.0))
                        } else {
                            Ok(Argument::Bits(0))
                        }
                    })
                    .collect::<Result<Vec<_>>>()?;
                for ((slot, ..), value) in ranges.iter().zip(&row[quantum..]) {
                    values[*slot] = if p.g.params[4][*slot].ty == Type::F64 {
                        Argument::Float(f64::from_bits(value.to_u128()? as u64))
                    } else {
                        Argument::Bits(value.to_u128()?)
                    };
                }
                let resolved = self.resolve_invocation_tokens(
                    p.g,
                    &values,
                    Some(p.budget),
                    None,
                    Some(&p.aliases),
                )?;
                input.args = resolved.arguments;
                let primary = resolved.primary.as_ref();
                let run = |f: &Function, ins: &[BitVector]| -> Result<BitVector> {
                    let mut call = OracleVectorInput {
                        ins: ins.to_vec(),
                        args: input.args.clone(),
                        regions: BTreeMap::new(),
                    };
                    for (a, b) in f.params[3].iter().zip(&p.g.params[3]) {
                        call.regions
                            .insert(a.name.clone(), input.regions[&b.name].clone());
                    }
                    let result =
                        self.run_oracle_vectors_bound(&f.name, &call, p.budget, primary, None, 0)?;
                    let mut machine = OracleVectorMachine::new_bound(
                        self, &f.name, &call, p.budget, primary, None, 0,
                    )?;
                    let before = machine.snapshot();
                    for _ in 0..p.budget.steps {
                        machine.forward_step()?;
                    }
                    let other = machine.outcome()?;
                    if (other.payload, other.code) != (result.payload.clone(), result.code.clone())
                    {
                        return err("§12.1 K4/T3", "inverse-pair independent engines disagree");
                    }
                    for _ in 0..p.budget.steps {
                        machine.inverse_step()?;
                    }
                    if machine.snapshot() != before || !machine.frames_clean() {
                        return err(
                            "§12.1 K4/T3",
                            "inverse-pair oracle workspace is not restored",
                        );
                    }
                    if !result.code.is_zero() {
                        return err("§12.1 K4", "inverse-pair oracle faults at entry budget");
                    }
                    Ok(result.payload)
                };
                let g = run(p.g, &input.ins)?;
                let gi = run(p.gi, &input.ins)?;
                let mut changed = input.ins.clone();
                changed[0] = g;
                if run(p.gi, &changed)? != input.ins[0] {
                    return err("§12.1 K4", "ginv(g(x)) differs from x");
                }
                changed[0] = gi;
                if run(p.g, &changed)? != input.ins[0] {
                    return err("§12.1 K4", "g(ginv(x)) differs from x");
                }
            }
        }
        self.pair_proofs
            .lock()
            .map_err(|_| Error::new("§12.1 K4: proof cache poisoned".into()))?
            .insert(key);
        Ok(ClaimVerdict::Proof)
    }
}
````

## `reference-interpreter/src/claims/qinplace09.rs` (484 lines)

````rust
//! Pre-effect K4/K91 coverage over the bound reference invocation tree. Q
//! predicates cannot remove a visit; zero-trip loops have no dynamic visits.
use super::*;
use crate::{Argument, BudgetToken, Instruction};
use pairs09::{args_domain, pair};

struct Invocation {
    name: String,
    args: Vec<Argument>,
    budget: Option<Budget>,
    primary: Option<BudgetToken>,
}
fn qinplace_sites(f: &Function) -> Vec<&Instruction> {
    let mut work = f.instructions().collect::<Vec<_>>();
    let mut sites = Vec::new();
    while let Some(i) = work.pop() {
        if i.op == "qinplace" {
            sites.push(i);
        }
        work.extend(i.bodies.iter().flatten());
    }
    sites
}
fn values(f: &Function, args: &BTreeMap<String, Argument>) -> Result<Vec<Argument>> {
    f.params[if f.kind == "oracle" { 4 } else { 3 }]
        .iter()
        .map(|p| {
            args.get(&p.name)
                .cloned()
                .ok_or_else(|| Error::new(format!("§4.5 K92: unresolved argument {}", p.name)))
        })
        .collect()
}
fn token(args: &BTreeMap<String, Argument>, name: &str) -> Result<BudgetToken> {
    match args.get(name) {
        Some(Argument::DeviceToken(t)) => Ok(t.clone()),
        _ => err(
            "§4.5 K91",
            "qinplace coverage needs an actual token identity",
        ),
    }
}
fn push(
    work: &mut Vec<Invocation>,
    f: &Function,
    names: &[String],
    args: &BTreeMap<String, Argument>,
    primary: Option<BudgetToken>,
) -> Result<()> {
    let actuals = names
        .iter()
        .map(|n| {
            args.get(n)
                .cloned()
                .ok_or_else(|| Error::new(format!("§4.5 K92: unresolved call argument {n}")))
        })
        .collect::<Result<_>>()?;
    crate::reserve_more(work, 1, "§4.5 K92", "reference invocation contexts")?;
    work.push(Invocation {
        name: f.name.clone(),
        args: actuals,
        budget: primary.as_ref().map(BudgetToken::tuple),
        primary,
    });
    Ok(())
}
impl Object {
    /// Inventory is static (including zero-trip bodies); applicability belongs
    /// to the resolved invocation tree, never to the standalone proof label.
    pub(super) fn check_qinplace_bindings09(
        &self,
    ) -> Result<BTreeMap<String, QinplaceApplicability>> {
        let certificate = self.section("certificate").unwrap();
        let identity = self.identity()?;
        let mut outcomes = BTreeMap::new();
        if !self
            .functions
            .values()
            .any(|f| !qinplace_sites(f).is_empty())
        {
            return Ok(outcomes);
        }
        for (closure, record) in certificate.get("regions")?.object()? {
            let f = self.region_function(closure)?;
            for site in qinplace_sites(f) {
                let hash = |name: &str| -> Result<&str> {
                    identity.closure_hashes[name.trim_start_matches('@')]
                        .as_deref()
                        .ok_or_else(|| Error::new("§12.3 K92: unresolved qinplace closure".into()))
                };
                let g = hash(&site.operands[0])?;
                let gi = hash(&site.operands[1])?;
                let mut found = false;
                for entry in record.get("verification")?.get("inverse_pairs")?.array()? {
                    let eg = entry.get("g")?.string()?;
                    let ei = entry.get("ginv")?.string()?;
                    if !((eg == g && ei == gi) || (eg == gi && ei == g)) {
                        continue;
                    }
                    found = true;
                    let index = usize::try_from(entry.get("claim")?.uint()?).map_err(|_| {
                        crate::resource_error("§12.3 K92", "claim index exceeds host")
                    })?;
                    self.inverse_pair_theorem09(closure, index, &mut BTreeSet::new())?;
                    self.verify_claim_guarded(closure, index, &mut BTreeSet::new())?;
                }
                if !found {
                    return err(
                        "§12.3 K92",
                        format!("missing owner-local inverse-pair entry in @{}", f.name),
                    );
                }
                outcomes.insert(
                    closure.clone(),
                    QinplaceApplicability::Unestablished(
                        "no resolved invocation establishes qinplace applicability".into(),
                    ),
                );
            }
        }
        let bindings = certificate.get("bindings")?;
        let root = bindings.get("closure_hash")?.string()?;
        let mut invocations = Vec::new();
        let mut unresolved = BTreeMap::new();
        if let Some(invocation) = bindings.object()?.get("invocation") {
            invocations.push((root, invocation));
        }
        for (closure, record) in certificate.get("regions")?.object()? {
            for claim in record.get("claims")?.array()? {
                if let Some(invocation) = claim.object()?.get("invocation") {
                    // Parameter-uniform claims keep their universal theorem;
                    // proving applicability requires a separate uniform check.
                    if invocation.get("args")?.array().is_ok() {
                        invocations.push((closure.as_str(), invocation));
                    } else {
                        unresolved.insert(
                            closure.clone(),
                            QinplaceApplicability::Unestablished(
                                "parameter-uniform invocation tree is not checked".into(),
                            ),
                        );
                    }
                }
            }
        }
        let mut checked = BTreeMap::new();
        for (closure, binding) in invocations {
            let f = self.region_function(closure)?;
            if !matches!(f.kind.as_str(), "oracle" | "action" | "perm_action") {
                unresolved.insert(
                    closure.to_string(),
                    QinplaceApplicability::Unestablished(format!(
                        "bound @{} invocation tree is not checked",
                        f.name
                    )),
                );
                continue;
            }
            let invocation = self.decode_invocation09(binding, f)?;
            let group = if f.kind == "oracle" { 4 } else { 3 };
            let args = f.params[group]
                .iter()
                .zip(invocation.args)
                .map(|(p, value)| (p.name.clone(), value))
                .collect();
            match self.qinplace_coverage09(
                f,
                &args,
                Some(invocation.budget),
                invocation.primary.as_ref(),
            ) {
                Ok(owners) if self.section("schedule").is_none() => {
                    for (owner, outcome) in owners {
                        if !matches!(
                            checked.get(&owner),
                            Some(QinplaceApplicability::Unestablished(_))
                        ) {
                            checked.insert(owner, outcome);
                        }
                    }
                }
                Ok(_) => {
                    unresolved.insert(
                        closure.to_string(),
                        QinplaceApplicability::Unestablished(
                            "complete realised invocation tree is not checked".into(),
                        ),
                    );
                }
                Err(error) if error.kind() == crate::ErrorKind::HostResource => {
                    unresolved.insert(
                        closure.to_string(),
                        QinplaceApplicability::Unestablished(error.to_string()),
                    );
                }
                Err(error) => return Err(error),
            }
        }
        outcomes.extend(checked);
        // Root obligations cannot depend on discovering an owner or a claim.
        // An unchecked context also takes precedence over a checked context of
        // the same closure: one invocation cannot discharge another's coverage.
        outcomes.extend(unresolved);
        Ok(outcomes)
    }
    fn check_qinplace_site09(
        &self,
        owner: &Function,
        i: &Instruction,
        args: &BTreeMap<String, Argument>,
    ) -> Result<QinplaceApplicability> {
        let a = &i.operands;
        let primary = token(args, &a[2])?;
        let actuals = if a.len() == 7 {
            crate::object::list(&a[6])?
                .iter()
                .map(|n| {
                    args.get(n)
                        .cloned()
                        .ok_or_else(|| Error::new(format!("§4.5 K4: unresolved pair argument {n}")))
                })
                .collect::<Result<Vec<_>>>()?
        } else {
            Vec::new()
        };
        let identity = self.identity()?;
        let owner_hash = identity.closure_hashes[&owner.name]
            .as_deref()
            .ok_or_else(|| Error::new("§4.5 K92: unresolved owner".into()))?;
        let missing = || {
            Error::new(format!(
                "§4.5 K4/K92: no covering inverse-pair entry in @{}",
                owner.name
            ))
        };
        let record = self
            .section("certificate")
            .and_then(|c| c.get("regions").ok())
            .and_then(|r| r.get(owner_hash).ok())
            .ok_or_else(missing)?;
        let g = identity.closure_hashes[a[0].trim_start_matches('@')]
            .as_deref()
            .ok_or_else(missing)?;
        let gi = identity.closure_hashes[a[1].trim_start_matches('@')]
            .as_deref()
            .ok_or_else(missing)?;
        let mut unresolved = None;
        for entry in record.get("verification")?.get("inverse_pairs")?.array()? {
            let eg = entry.get("g")?.string()?;
            let ei = entry.get("ginv")?.string()?;
            if !((eg == g && ei == gi) || (eg == gi && ei == g)) {
                continue;
            }
            let p = pair(self, entry)?;
            let b = primary.tuple();
            if p.budget.steps > b.steps
                || p.budget.heap > b.heap
                || p.budget.stack > b.stack
                || p.budget.depth > b.depth
            {
                continue;
            }
            let resolved =
                self.resolve_invocation_tokens(p.g, &actuals, Some(b), Some(&primary), None)?;
            if resolved.aliases != p.aliases {
                continue;
            }
            if p.g.params[4].iter().zip(&actuals).any(|(param, value)| {
                param.ty == Type::Token
                    && value.token_budget() != p.tokens.get(&param.name).copied()
            }) {
                continue;
            }
            let index = usize::try_from(entry.get("claim")?.uint()?)
                .map_err(|_| crate::resource_error("§12.3 K4", "claim index exceeds host"))?;
            let Some((claim, domain_function)) =
                self.inverse_pair_theorem09(owner_hash, index, &mut BTreeSet::new())?
            else {
                unresolved = Some("linked inverse-pair theorem is unavailable".into());
                continue;
            };
            let ranges = args_domain(self, domain_function, claim.get("domain")?)?;
            let mut covers = true;
            for (slot, (param, value)) in p.g.params[4].iter().zip(&actuals).enumerate() {
                if param.ty == Type::Token {
                    continue;
                }
                let bits =
                    crate::oracle::argument_bits(self, &param.ty, value)?.ok_or_else(missing)?;
                covers &= if let Some((_, lo, hi)) = ranges.iter().find(|(i, ..)| *i == slot) {
                    bits.unsigned_cmp(lo)? != std::cmp::Ordering::Less
                        && bits.unsigned_cmp(hi)? != std::cmp::Ordering::Greater
                } else {
                    bits.is_zero()
                };
            }
            if !covers {
                continue;
            }
            if self.verify_claim_guarded(owner_hash, index, &mut BTreeSet::new())?
                == ClaimVerdict::Proof
            {
                return Ok(QinplaceApplicability::Established);
            }
            unresolved = Some("entry claim is not an established inverse-pair proof".into());
        }
        match unresolved {
            Some(reason) => Ok(QinplaceApplicability::Unestablished(reason)),
            None => Err(missing()),
        }
    }
    pub(crate) fn precheck_qinplace09(
        &self,
        f: &Function,
        args: &BTreeMap<String, Argument>,
        budget: Option<Budget>,
        primary: Option<&BudgetToken>,
    ) -> Result<()> {
        for outcome in self.qinplace_coverage09(f, args, budget, primary)?.values() {
            if let QinplaceApplicability::Unestablished(reason) = outcome {
                return err(
                    "§4.5 K4/K92",
                    format!("unestablished qinplace applicability: {reason}"),
                );
            }
        }
        Ok(())
    }
    fn qinplace_coverage09(
        &self,
        f: &Function,
        args: &BTreeMap<String, Argument>,
        budget: Option<Budget>,
        primary: Option<&BudgetToken>,
    ) -> Result<BTreeMap<String, QinplaceApplicability>> {
        if self.isa_version != crate::IsaVersion::V09
            || !self
                .functions
                .values()
                .any(|f| !qinplace_sites(f).is_empty())
        {
            return Ok(BTreeMap::new());
        }
        let mut work = vec![Invocation {
            name: f.name.clone(),
            args: values(f, args)?,
            budget,
            primary: primary.cloned(),
        }];
        let mut visited = BTreeSet::new();
        let mut owners = BTreeMap::new();
        while let Some(invocation) = work.pop() {
            let f = &self.functions[&invocation.name];
            let ids = invocation
                .args
                .iter()
                .map(|a| {
                    if let Argument::DeviceToken(t) = a {
                        t.id()
                    } else {
                        0
                    }
                })
                .collect::<Vec<_>>();
            let key = format!(
                "{}:{:?}:{:?}:{:?}:{}",
                f.name,
                invocation.budget,
                invocation.primary.as_ref().map(BudgetToken::id),
                ids,
                crate::tokens::typed_arguments(&invocation.args).canonical()
            );
            if !visited.insert(key) {
                continue;
            }
            if !qinplace_sites(f).is_empty() {
                let closure = self.identity()?.closure_hashes[&f.name]
                    .clone()
                    .ok_or_else(|| Error::new("§12.3 K92: unresolved owner".into()))?;
                owners
                    .entry(closure)
                    .or_insert(QinplaceApplicability::Established);
            }
            let args = f.params[if f.kind == "oracle" { 4 } else { 3 }]
                .iter()
                .zip(&invocation.args)
                .map(|(p, a)| (p.name.clone(), a.clone()))
                .collect::<BTreeMap<_, _>>();
            if f.kind == "oracle" {
                if invocation.budget.is_none_or(|b| b.steps == 0) {
                    continue;
                }
                let program = crate::oracle::Program::new(self, &f.name)?;
                for (activation, i) in &program.rows {
                    if !matches!(
                        i.op.as_str(),
                        "lift.oracle_call" | "lift.oracle_uncall" | "lift.perm_call"
                    ) {
                        continue;
                    }
                    let fixed = program.arguments(activation, &args)?;
                    let a = &i.operands;
                    let oracle = i.op != "lift.perm_call";
                    let callee = &self.functions[a[0].trim_start_matches('@')];
                    push(
                        &mut work,
                        callee,
                        &crate::object::list(&a[if oracle { 6 } else { 4 }])?,
                        &fixed,
                        if oracle {
                            Some(token(&fixed, &a[1])?)
                        } else {
                            None
                        },
                    )?;
                }
            } else {
                let mut sequences = f
                    .blocks
                    .iter()
                    .map(|b| b.instructions.as_slice())
                    .collect::<Vec<_>>();
                while let Some(sequence) = sequences.pop() {
                    for i in sequence {
                        if i.op == "qloop"
                            && crate::object::host_count(&i.operands[0], "qinplace loop count")?
                                == 0
                        {
                            continue;
                        }
                        for body in &i.bodies {
                            sequences.push(body);
                        }
                        let a = &i.operands;
                        if i.op == "qinplace" {
                            let outcome = self.check_qinplace_site09(f, i, &args)?;
                            if let QinplaceApplicability::Unestablished(_) = outcome {
                                let closure = self.identity()?.closure_hashes[&f.name]
                                    .clone()
                                    .ok_or_else(|| {
                                        Error::new("§12.3 K92: unresolved owner".into())
                                    })?;
                                owners.insert(closure, outcome);
                            }
                            let names = if a.len() == 7 {
                                crate::object::list(&a[6])?
                            } else {
                                Vec::new()
                            };
                            for name in &a[..2] {
                                push(
                                    &mut work,
                                    &self.functions[name.trim_start_matches('@')],
                                    &names,
                                    &args,
                                    Some(token(&args, &a[2])?),
                                )?;
                            }
                        } else if matches!(
                            i.op.as_str(),
                            "action_call" | "oracle_call" | "adj" | "ctl"
                        ) {
                            let call = crate::validation::normalize_call(i)?;
                            let a = &call.instruction.operands;
                            let oracle = call.instruction.op == "oracle_call";
                            push(
                                &mut work,
                                &self.functions[a[0].trim_start_matches('@')],
                                &crate::object::list(&a[if oracle { 6 } else { 4 }])?,
                                &args,
                                if oracle {
                                    Some(token(&args, &a[1])?)
                                } else {
                                    None
                                },
                            )?;
                        }
                    }
                }
            }
        }
        Ok(owners)
    }
}
````

## `reference-interpreter/src/claims/replay09.rs` (505 lines)

````rust
//! ISA 0.9 full-tuple replay. The legacy 0.8 table encoding stays in claims.rs.
use super::*;
use crate::Argument;

#[derive(Clone)]
pub(super) struct Invocation {
    pub args: Vec<Argument>,
    pub primary: Option<crate::BudgetToken>,
    pub controls: Vec<BitVector>,
    pub adjoint: bool,
    pub budget: Budget,
}

struct ResolvedDomain {
    domain: Domain,
    relative_to_image: bool,
    images: Vec<FixedRegionBinding>,
}
pub(super) struct Outcome {
    pub verdict: ClaimVerdict,
    pub coverage: Option<ClaimCoverage>,
}

fn coverage(
    f: &Function,
    controls: usize,
    domain: &ResolvedDomain,
    elements: usize,
) -> Result<ClaimCoverage> {
    let mut bits = controls;
    for p in f.params.iter().flatten() {
        let width = match p.ty {
            Type::Wire(w) => Some(w as u128),
            Type::Region(a, w) => Some(
                crate::oracle::power_of_two(a as u128)
                    .and_then(|n| n.checked_mul(w as u128))
                    .ok_or_else(|| {
                        crate::resource_error("§12.2 K74", "full region width exceeds u128")
                    })?,
            ),
            _ => None,
        };
        if let Some(width) = width {
            bits = usize::try_from(width)
                .ok()
                .and_then(|w| bits.checked_add(w))
                .ok_or_else(|| {
                    crate::resource_error("§12.2 K74", "full interface width exceeds usize")
                })?;
        }
    }
    for (c, width, ..) in &domain.domain.components {
        if matches!(c, Component::Borrowed(..)) {
            bits = bits.checked_add(*width).ok_or_else(|| {
                crate::resource_error("§12.2 K74", "borrowed width exceeds usize")
            })?;
        }
    }
    let power = |exponent: usize| -> Result<String> {
        let width = exponent
            .checked_add(1)
            .ok_or_else(|| crate::resource_error("§12.2 K74", "coverage storage exceeds usize"))?;
        let mut n = BitVector::zero(width)?;
        n.set(exponent, true)?;
        Ok(n.to_decimal())
    };
    let full_domain_elements = power(bits)?;
    let mut numerator = elements as u128;
    let covered_fraction = if numerator == 0 {
        "0/1".into()
    } else {
        let reduce = (numerator.trailing_zeros() as usize).min(bits);
        numerator >>= reduce;
        format!("{numerator}/{}", power(bits - reduce)?)
    };
    Ok(ClaimCoverage {
        elements: elements as u128,
        full_domain_elements,
        covered_fraction,
        fixed_regions: domain.images.clone(),
    })
}

fn budget(value: &Json) -> Result<Budget> {
    let values = value
        .array()?
        .iter()
        .map(|v| {
            v.string()?
                .parse::<u128>()
                .map_err(|_| crate::resource_error("§12.1 K13", "invocation tuple exceeds u128"))
        })
        .collect::<Result<Vec<_>>>()?;
    Ok(Budget {
        steps: u64::try_from(values[0])
            .map_err(|_| crate::resource_error("§12.1 K13", "invocation steps exceed u64"))?,
        heap: values[1],
        stack: values[2],
        depth: values[3],
    })
}

fn decimal(value: &BitVector) -> Json {
    Json::String(value.to_decimal())
}

impl Object {
    fn invocation09(&self, claim: &Json, f: &Function, closure: &str) -> Result<Invocation> {
        let subject = claim.get("subject")?;
        if subject.get("closure_hash")?.string()? != closure {
            return err("§12.1 K13", "claim subject differs from its region closure");
        }
        // Variant is an open identifier selecting a realisation. It does not
        // change the region's reference semantics or imply an adjoint.
        let invocation = if let Some(invocation) = claim.object()?.get("invocation") {
            invocation
        } else {
            let bindings = self.section("certificate").unwrap().get("bindings")?;
            if bindings.get("closure_hash")?.string()? != closure {
                return err(
                    "§12.1 K13",
                    "nested scheduled invocation needs concrete context resolution",
                );
            }
            bindings.get("invocation")?
        };
        self.decode_invocation09(invocation, f)
    }

    pub(super) fn decode_invocation09(
        &self,
        invocation: &Json,
        f: &Function,
    ) -> Result<Invocation> {
        let group = if f.kind == "oracle" { 4 } else { 3 };
        let args = invocation
            .get("args")?
            .array()?
            .iter()
            .zip(&f.params[group])
            .map(|(value, p)| {
                Ok(match p.ty {
                    Type::Int(_) | Type::Ptr => {
                        Argument::Bits(value.string()?.parse::<u128>().map_err(|_| {
                            crate::resource_error("§12.1 K13", "classical value exceeds u128")
                        })?)
                    }
                    Type::F64 => Argument::Float(f64::from_bits(
                        u64::from_str_radix(&value.string()?[2..], 16)
                            .map_err(|_| Error::new("§12.1 K13: f64 bits".into()))?,
                    )),
                    Type::Token => Argument::Token(budget(value)?),
                    _ => return err("§12.1 K13", "invalid classical invocation type"),
                })
            })
            .collect::<Result<Vec<_>>>()?;
        if args.len() != f.params[group].len() {
            return err("§12.1 K13", "invocation argument count mismatch");
        }
        let budget = budget(invocation.get("budget")?)?;
        let aliases = self.validate_invocation09(invocation, f)?;
        let resolved = self.resolve_invocation_tokens(
            f,
            &args,
            (f.kind == "oracle").then_some(budget),
            None,
            Some(&aliases),
        )?;
        Ok(Invocation {
            args: resolved.arguments,
            primary: resolved.primary,
            controls: Vec::new(),
            adjoint: false,
            budget,
        })
    }

    fn domain09(&self, claim: &Json, f: &Function) -> Result<ResolvedDomain> {
        let controls = usize::try_from(claim.get("subject")?.get("inherited_controls")?.uint()?)
            .map_err(|_| {
                crate::resource_error("§12.2 K72", "inherited control count exceeds usize")
            })?;
        let mut source = claim.get("domain")?.clone();
        let Json::Object(fields) = &mut source else {
            unreachable!()
        };
        let Json::Array(bundles) = fields.get_mut("bundles").unwrap() else {
            unreachable!()
        };
        if bundles.len() < controls {
            return err("§12.2 K72", "domain omits inherited controls");
        }
        let inherited = bundles.drain(..controls).collect::<Vec<_>>();
        let images = self.image_domains09(claim.get("domain")?, f)?;
        let mut unrestricted = source.clone();
        for (value, full) in [(&mut source, false), (&mut unrestricted, true)] {
            let Json::Object(fields) = value else {
                unreachable!()
            };
            let Json::Array(regions) = fields.get_mut("regions").unwrap() else {
                unreachable!()
            };
            for image in &images {
                regions.push(image.entry(full)?);
            }
        }
        let mut domain = self.domain(f, &source)?;
        let mut relative_to_image = !images.is_empty() && self.domain(f, &unrestricted)?.covers_d;
        let mut components = Vec::new();
        for (i, entry) in inherited.iter().enumerate() {
            if entry.get("width")?.uint()? != 1 {
                return err("§12.2 K72", "inherited control width differs from one");
            }
            let lo = json_bits(entry.get("lo")?, 1)?;
            let hi = json_bits(entry.get("hi")?, 1)?;
            domain.covers_d &= lo.is_zero() && hi == ones(1)?;
            relative_to_image &= lo.is_zero() && hi == ones(1)?;
            components.push((Component::Control(i), 1, lo, hi));
        }
        components.append(&mut domain.components);
        domain.components = components;
        Ok(ResolvedDomain {
            domain,
            relative_to_image,
            images: images.into_iter().map(|i| i.binding).collect(),
        })
    }

    /// Convert the flat executor output to K13's complete typed tuple; the
    /// region/cell boundaries come from the subject signature, never the table.
    fn tuple09(
        &self,
        f: &Function,
        flat: &[BitVector],
        controls: usize,
        borrowed: usize,
    ) -> Result<Json> {
        let bundle_count = controls
            + f.params
                .iter()
                .flatten()
                .filter(|p| matches!(p.ty, Type::Wire(_)))
                .count();
        let mut offset = bundle_count;
        let mut regions = Vec::new();
        for p in f.params.iter().flatten() {
            if let Type::Region(a, _) = p.ty {
                let cells = crate::oracle::power_of_two(a as u128)
                    .and_then(|n| usize::try_from(n).ok())
                    .ok_or_else(|| {
                        crate::resource_error("§12.1 K13", "region tuple exceeds usize")
                    })?;
                let end = offset.checked_add(cells).ok_or_else(|| {
                    crate::resource_error("§12.1 K13", "region tuple size overflow")
                })?;
                let values = flat.get(offset..end).ok_or_else(|| {
                    Error::new("§12.1 K13: incomplete executor region tuple".into())
                })?;
                regions.push(Json::Array(values.iter().map(decimal).collect()));
                offset = end;
            }
        }
        if flat.len() != offset + borrowed {
            return err("§12.1 K13", "executor tuple length differs from interface");
        }
        Ok(Json::Object(BTreeMap::from([
            (
                "bundles".into(),
                Json::Array(flat[..bundle_count].iter().map(decimal).collect()),
            ),
            ("regions".into(), Json::Array(regions)),
            (
                "borrowed".into(),
                Json::Array(flat[offset..].iter().map(decimal).collect()),
            ),
        ])))
    }

    fn entry09(
        &self,
        f: &Function,
        element: &[(Component, BitVector)],
        controls: usize,
    ) -> Result<Vec<BitVector>> {
        let find = |component: Component, width| {
            element
                .iter()
                .find_map(|(c, v)| {
                    (match (&component, c) {
                        (Component::Control(a), Component::Control(b)) => a == b,
                        (Component::Bundle(a, b), Component::Bundle(c, d)) => (a, b) == (c, d),
                        (Component::Cell(a, b, c), Component::Cell(d, e, f)) => {
                            (a, b, c) == (d, e, f)
                        }
                        _ => false,
                    })
                    .then_some(v.clone())
                })
                .map_or_else(|| BitVector::zero(width), Ok)
        };
        let mut out = (0..controls)
            .map(|i| find(Component::Control(i), 1))
            .collect::<Result<Vec<_>>>()?;
        for (group, params) in f.params.iter().enumerate() {
            for (slot, p) in params.iter().enumerate() {
                if matches!(p.ty, Type::Wire(_)) {
                    out.push(find(
                        Component::Bundle(group, slot),
                        p.ty.bits(self.ptr_width)?,
                    )?);
                }
            }
        }
        for (group, params) in f.params.iter().enumerate() {
            for (slot, p) in params.iter().enumerate() {
                if let Type::Region(a, w) = p.ty {
                    let count = crate::oracle::power_of_two(a as u128)
                        .and_then(|n| usize::try_from(n).ok())
                        .ok_or_else(|| {
                            crate::resource_error("§12.1 K13", "region tuple exceeds usize")
                        })?;
                    crate::reserve_more(&mut out, count, "§12.1 K13", "entry region cells")?;
                    for index in 0..count {
                        out.push(find(Component::Cell(group, slot, index), w as usize)?);
                    }
                }
            }
        }
        out.extend(
            element
                .iter()
                .filter_map(|(c, v)| matches!(c, Component::Borrowed(..)).then_some(v.clone())),
        );
        Ok(out)
    }

    pub(super) fn verify_replay09(
        &self,
        closure: &str,
        index: usize,
        claim: &Json,
        f: &Function,
    ) -> Result<Outcome> {
        if claim.get("expected")? == &Json::String("inverse_pair".into()) {
            return Ok(Outcome {
                verdict: self.verify_inverse_pair_claim09(f, index, claim)?,
                coverage: None,
            });
        }
        if claim
            .get("subject")?
            .object()?
            .contains_key("schedule_hash")
        {
            return Ok(Outcome {
                verdict: ClaimVerdict::Unverified(
                    "scheduled subject needs realised target/schedule execution".into(),
                ),
                coverage: None,
            });
        }
        let mut invocation = self.invocation09(claim, f, closure)?;
        let controls = usize::try_from(claim.get("subject")?.get("inherited_controls")?.uint()?)
            .map_err(|_| crate::resource_error("§12.1 K13", "control count exceeds usize"))?;
        let resolved = self.domain09(claim, f)?;
        let domain = &resolved.domain;
        let sampled = claim.get("kind")?.string()? == "sampled";
        let elements = if sampled {
            let sampler = claim.get("sampler")?;
            let seed = sampler
                .get("seed")?
                .array()?
                .iter()
                .map(|v| {
                    v.string()?
                        .parse::<u64>()
                        .map_err(|_| Error::new("§12.1: sampler seed".into()))
                })
                .collect::<Result<Vec<_>>>()?;
            let mut rng = Xoshiro256([seed[0], seed[1], seed[2], seed[3]]);
            let count = sample_count(sampler)?;
            // Retain the existing fallible host-capacity check before a
            // metadata-controlled sampling loop or allocation can run away.
            let _capacity = sample_elements(count)?;
            let mut distinct = BTreeMap::new();
            for _ in 0..count {
                let row = domain
                    .components
                    .iter()
                    .map(|(_, w, lo, hi)| rng.draw(*w, lo, hi))
                    .collect::<Result<Vec<_>>>()?;
                // Fixed-width unsigned decimal magnitude order equals domain
                // enumeration order, independent of draw order and duplicates.
                let key = row
                    .iter()
                    .map(|v| {
                        let s = v.to_decimal();
                        (s.len(), s)
                    })
                    .collect::<Vec<_>>();
                distinct.insert(key, row);
            }
            distinct.into_values().collect::<Vec<_>>()
        } else {
            enumerate(domain)?
        };
        let expected = claim.get("expected")?;
        let table = expected
            .object()?
            .get("table")
            .map(Json::array)
            .transpose()?;
        let program = expected
            .object()?
            .get("program")
            .map(|p| self.region_function(p.string()?))
            .transpose()?;
        if table.is_some_and(|table| table.len() != elements.len()) {
            return err(
                "§12.1 K13",
                "table must contain one row per distinct domain element",
            );
        }
        if program.is_some_and(|p| p.signature() != f.signature()) {
            return err(
                "§12.1 K13",
                "expected program has an incompatible signature",
            );
        }
        let borrowed = domain
            .components
            .iter()
            .filter(|(c, ..)| matches!(c, Component::Borrowed(..)))
            .count();
        for (row, values) in elements.iter().enumerate() {
            let element = domain
                .components
                .iter()
                .map(|c| c.0.clone())
                .zip(values.iter().cloned())
                .collect::<Vec<_>>();
            let before = self.entry09(f, &element, controls)?;
            invocation.controls = before[..controls].to_vec();
            let after = self.execute_element_bound(
                f,
                &element,
                Some(invocation.budget),
                None,
                Some(&invocation),
            )?;
            if let Some(table) = table {
                let entry = &table[row];
                if entry.get("before")? != &self.tuple09(f, &before, controls, borrowed)?
                    || entry.get("after")? != &self.tuple09(f, &after, controls, borrowed)?
                {
                    return err(
                        "§12.1 K13",
                        format!("claim {index} of {closure}: full tuple mismatch at element {row}"),
                    );
                }
            }
            if let Some(program) = program {
                let other = self.execute_element_bound(
                    program,
                    &element,
                    Some(invocation.budget),
                    None,
                    Some(&invocation),
                )?;
                if other != after {
                    return err("§12.1 K13", "expected program full tuple mismatch");
                }
            }
        }
        let verdict = if !sampled && domain.covers_d {
            ClaimVerdict::Proof
        } else if !sampled && resolved.relative_to_image {
            ClaimVerdict::ProofRelativeToImage
        } else {
            ClaimVerdict::Evidence {
                elements: elements.len() as u128,
            }
        };
        if claim.object()?.get("label") == Some(&Json::String("proof".into()))
            && verdict != ClaimVerdict::Proof
        {
            return err(
                "§12.2 K74",
                "requested proof but replay covers only a slice of D",
            );
        }
        if claim.object()?.get("label") == Some(&Json::String("proof_relative_to_image".into()))
            && verdict != ClaimVerdict::ProofRelativeToImage
        {
            return err(
                "§12.2 K85",
                "requested proof_relative_to_image without complete remaining domain",
            );
        }
        Ok(Outcome {
            verdict,
            coverage: Some(coverage(f, controls, &resolved, elements.len())?),
        })
    }
}
````

## `reference-interpreter/src/claims.rs` (1175 lines)

````rust
//! §12 claim checking: re-execution of exhaustive and sampled claims on the
//! reference semantics, and the syntactic side conditions of structural claims.
//!
//! Legacy ISA 0.8 encodings fixed in SPEC-QUESTIONS 21:
//! a domain element's output tuple is the region's final interface in
//! signature order (oracle: ins, tgt, fault, in-region cells; action: mut
//! bundles, in bundles, region cells in signature order), then the borrowed
//! components; `expected.table` lists one tuple per domain element in
//! enumeration order, each component a canonical decimal (JSON number when
//! at most 2^53 - 1, else string). Interval-arithmetic claims (`numerical`,
//! `channel`) and `expected: "oracle"` (which compares a realisation under a
//! schedule) need the target/schedule executor and are reported as
//! `Unverified` with that reason, never as verified.
//! ISA 0.9's explicit invocation/full-tuple contract is in replay09.rs.
use crate::{
    err, json::Json, BitVector, Budget, Error, Function, Object, QuantumBindings, QuantumState,
    Result, Type,
};
use std::collections::{BTreeMap, BTreeSet};
mod images09;
mod pairs09;
mod qinplace09;
mod replay09;
pub use images09::FixedRegionBinding;

/// §17 item 13: an explicitly sampled claim defaults to 2^16 samples.
/// This is a consumer default, never a mutation of certificate JCS.
pub(crate) fn sample_count(sampler: &Json) -> Result<u128> {
    crate::metadata_schema::validate("sampler", sampler)?;
    sampler
        .object()?
        .get("count")
        .map_or(Ok(1 << 16), Json::uint)
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ClaimVerdict {
    /// Re-executed over D (or the structural rule holds with verified subclaims).
    Proof,
    /// K85 theorem conditional on the report's exact in-region images. This
    /// does not discharge an executable invocation without preparation evidence.
    ProofRelativeToImage,
    /// Re-executed over a domain that is not all of D (or sampled).
    Evidence { elements: u128 },
    /// Not checkable by this crate yet; the reason names the missing machinery.
    Unverified(String),
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct CertificateReport {
    pub claims: Vec<ClaimReport>,
    /// K92 obligations keyed by the owning or bound root closure. These survive
    /// absent owner records and empty claim lists; a claim proof does not
    /// discharge an unestablished invocation obligation.
    pub qinplace_applicability: BTreeMap<String, QinplaceApplicability>,
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ClaimReport {
    pub closure_hash: String,
    pub region: String,
    pub index: usize,
    pub kind: String,
    pub verdict: ClaimVerdict,
    pub context_key: Json,
    pub coverage: Option<ClaimCoverage>,
    /// K92 applicability is separate from the standalone theorem's verdict.
    pub qinplace_applicability: Option<QinplaceApplicability>,
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum QinplaceApplicability {
    Established,
    Unestablished(String),
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ClaimCoverage {
    pub elements: u128,
    pub full_domain_elements: String,
    pub covered_fraction: String,
    pub fixed_regions: Vec<FixedRegionBinding>,
}
#[derive(Clone, Debug)]
enum Component {
    Control(usize),
    Bundle(usize, usize),
    Borrowed(usize, String),
    Cell(usize, usize, usize),
}
struct Domain {
    components: Vec<(Component, usize, BitVector, BitVector)>,
    covers_d: bool,
}
/// ABI slot identity, independent of a function's local spelling. The domain
/// is resolved once against its subject; the same positions bind the reference.
fn interface_slot(f: &Function, name: &str) -> Result<(usize, usize)> {
    f.params
        .iter()
        .enumerate()
        .find_map(|(group, params)| {
            params
                .iter()
                .position(|p| p.name == name)
                .map(|index| (group, index))
        })
        .ok_or_else(|| Error::new(format!("§12.2: unknown interface component {name}")))
}
fn json_bits(value: &Json, width: usize) -> Result<BitVector> {
    BitVector::parse_unsigned_exact(width, value.uint_text()?)
}
/// Every element of the domain, last component fastest (§12.2).
fn enumerate(domain: &Domain) -> Result<Vec<Vec<BitVector>>> {
    let mut count = 1u128;
    for (_, _, lo, hi) in &domain.components {
        let span = hi.binary("sub", lo)?.to_u128().map_err(|_| {
            Error::host_resource(
                "§12.2: host limit: exhaustive interval cardinality exceeds u128".into(),
            )
        })?;
        count = span
            .checked_add(1)
            .and_then(|span| count.checked_mul(span))
            .ok_or_else(|| {
                Error::host_resource(
                    "§12.2: host limit: exhaustive domain cardinality exceeds u128".into(),
                )
            })?;
    }
    let count = usize::try_from(count).map_err(|_| {
        Error::host_resource(
            "§12.2: host limit: exhaustive domain cardinality exceeds usize".into(),
        )
    })?;
    let mut out = crate::reserved(count, "§12.2", "exhaustive domain elements")?;
    let mut current = crate::reserved(domain.components.len(), "§12.2", "domain tuple components")?;
    current.extend(domain.components.iter().map(|c| c.2.clone()));
    loop {
        let mut row = crate::reserved(current.len(), "§12.2", "exhaustive tuple components")?;
        row.extend(current.iter().cloned());
        out.push(row);
        let mut i = domain.components.len();
        let mut wrapped = true;
        while i > 0 {
            i -= 1;
            if current[i] == domain.components[i].3 {
                current[i] = domain.components[i].2.clone();
            } else {
                current[i] = increment(&current[i])?;
                wrapped = false;
                break;
            }
        }
        if wrapped {
            return Ok(out);
        }
    }
}
fn ones(width: usize) -> Result<BitVector> {
    BitVector::zero(width)?.binary("sub", &BitVector::from_u128(width, 1)?)
}
fn increment(v: &BitVector) -> Result<BitVector> {
    v.binary("add", &BitVector::from_u128(v.width(), 1)?)
}
fn decimal_json(v: &BitVector) -> Json {
    match v.to_u128() {
        Ok(n) if n <= 9_007_199_254_740_991 => Json::Number(n.to_string()),
        _ => Json::String(v.to_decimal()),
    }
}

fn sample_elements(count: u128) -> Result<Vec<Vec<BitVector>>> {
    let count = usize::try_from(count).map_err(|_| {
        Error::host_resource("§12.1: host limit: sample count exceeds usize".into())
    })?;
    crate::reserved(count, "§12.1", "sampled domain elements")
}

#[cfg(test)]
pub(crate) fn r21_resource_cases() {
    for width in [1, 2, 3, 62, 63, 64, 127, 128] {
        for count in [1, 2] {
            let d = Domain {
                covers_d: true,
                components: (0..count)
                    .map(|i| {
                        (
                            Component::Bundle(0, i),
                            width,
                            BitVector::zero(width).unwrap(),
                            ones(width).unwrap(),
                        )
                    })
                    .collect(),
            };
            let r = enumerate(&d);
            if width < 4 {
                assert_eq!(r.unwrap().len(), 1 << (width * count));
            } else {
                let e = r.unwrap_err().to_string();
                assert!(e.contains("§12.2") && e.contains("host limit"), "{e}");
            }
        }
    }
    for count in [0, 1, 8, (1u128 << 63) - 1, 1 << 63, u64::MAX as u128] {
        let r = sample_elements(count);
        if count <= 8 {
            assert!(r.unwrap().capacity() >= count as usize);
        } else {
            let e = r.unwrap_err().to_string();
            assert!(e.contains("§12.1") && e.contains("host limit"), "{e}");
        }
    }
    // Direct replay consumer: domain admission is covered separately through
    // parse/check_hashes/verify_claim, including both region schema branches.
    let mut o = Object::parse(include_str!("../tests/fixtures/tiny_memory.bisa")).unwrap();
    let mut f = o.functions["tiny"].clone();
    for a in [0, 1, 3, 62, 63, 64, 127, 128] {
        f.params[3][0].ty = Type::Region(a, 8);
        o.functions.insert("tiny".into(), f.clone());
        let r = o.execute_element(&f, &[], Some(Budget::steps(0)));
        if a < 4 {
            r.unwrap();
        } else {
            let e = r.unwrap_err().to_string();
            assert!(e.contains("§12.2") && e.contains("host limit"), "{e}");
        }
    }
    eprintln!("R21 exhaustive power/product / samples / oracle replay region: 4 paths / 30 cases");
}

/// xoshiro256** (Blackman and Vigna), the §12.1 sampler.
pub struct Xoshiro256(pub [u64; 4]);
impl Xoshiro256 {
    pub fn next_word(&mut self) -> u64 {
        let s = &mut self.0;
        let result = s[1].wrapping_mul(5).rotate_left(7).wrapping_mul(9);
        let t = s[1] << 17;
        s[2] ^= s[0];
        s[3] ^= s[1];
        s[1] ^= s[2];
        s[0] ^= s[3];
        s[2] ^= t;
        s[3] = s[3].rotate_left(45);
        result
    }
    /// A uniform value of `width` bits (R = 2^width: no redraws, §12.1).
    pub fn bits(&mut self, width: usize) -> Result<BitVector> {
        let lo = BitVector::zero(width)?;
        let hi = ones(width)?;
        self.draw(width, &lo, &hi)
    }
    /// §12.1: m = ceil(ceil(log2 R)/64) words, least significant first,
    /// reduced modulo 2^ceil(log2 R), redrawn while >= R, plus lo.
    fn draw(&mut self, width: usize, lo: &BitVector, hi: &BitVector) -> Result<BitVector> {
        let range = increment(&hi.binary("sub", lo)?.resize(width + 1, false)?)?;
        let bits = {
            let r_minus_1 = range.binary("sub", &BitVector::from_u128(width + 1, 1)?)?;
            (0..=width)
                .rev()
                .find(|i| r_minus_1.bit(*i).unwrap_or(false))
                .map_or(0, |i| i + 1)
        };
        loop {
            let mut v = BitVector::zero(width + 1)?;
            for word in 0..bits.div_ceil(64) {
                let w = self.next_word();
                for b in 0..64 {
                    let i = word * 64 + b;
                    if i < bits && w >> b & 1 == 1 {
                        v.set(i, true)?;
                    }
                }
            }
            if v.unsigned_cmp(&range)? == std::cmp::Ordering::Less {
                return v
                    .binary("add", &lo.resize(width + 1, false)?)?
                    .resize(width, false);
            }
        }
    }
}

impl Object {
    fn region_function(&self, closure: &str) -> Result<&Function> {
        let identity = self.identity()?;
        let name = identity
            .closure_hashes
            .iter()
            .find_map(|(n, h)| (h.as_deref() == Some(closure)).then_some(n.clone()))
            .ok_or_else(|| Error::new(format!("§12: no region has closure hash {closure}")))?;
        self.functions
            .get(&name)
            .ok_or_else(|| Error::new(format!("§12: closure {closure} is not a function")))
    }
    fn domain(&self, f: &Function, d: &Json) -> Result<Domain> {
        let mut components = Vec::new();
        let mut bundles = BTreeSet::new();
        let mut regions = BTreeSet::new();
        let mut full = true;
        for (group, borrowed) in [("bundles", false), ("borrowed", true)] {
            for (ordinal, b) in d.get(group)?.array()?.iter().enumerate() {
                let name = b.get("name")?.string()?.to_string();
                let width = usize::try_from(b.get("width")?.uint()?)
                    .map_err(|_| Error::host_resource("§12.2: host limit: domain width".into()))?;
                let lo = json_bits(b.get("lo")?, width)?;
                let hi = json_bits(b.get("hi")?, width)?;
                full &= lo.is_zero() && hi == ones(width)?;
                components.push((
                    if borrowed {
                        Component::Borrowed(ordinal, name)
                    } else {
                        let (group, index) = interface_slot(f, &name)?;
                        bundles.insert((group, index));
                        Component::Bundle(group, index)
                    },
                    width,
                    lo,
                    hi,
                ));
            }
        }
        for r in d.get("regions")?.array()? {
            let name = r.get("name")?.string()?.to_string();
            let (group, slot) = interface_slot(f, &name)?;
            let (a, w) = f
                .params
                .iter()
                .flatten()
                .find_map(|p| match p.ty {
                    Type::Region(a, w) if p.name == name => Some((a, w as usize)),
                    _ => None,
                })
                .ok_or_else(|| Error::new(format!("§12.2: unknown domain region {name}")))?;
            let cells = crate::oracle::power_of_two(a as u128)
                .and_then(|n| usize::try_from(n).ok())
                .ok_or_else(|| Error::host_resource("§12.2: host limit: region cells".into()))?;
            match r.get("cells")? {
                Json::String(s) if s == "all" => {
                    regions.insert((group, slot));
                    crate::reserve_more(&mut components, cells, "§12.2", "domain components")?;
                    for i in 0..cells {
                        components.push((
                            Component::Cell(group, slot, i),
                            w,
                            BitVector::zero(w)?,
                            ones(w)?,
                        ));
                    }
                }
                cs => {
                    let mut covered = BTreeSet::new();
                    for c in cs.array()? {
                        let i = usize::try_from(c.get("index")?.uint()?)
                            .map_err(|_| Error::new("§12.2: cell index".into()))?;
                        let lo = json_bits(c.get("lo")?, w)?;
                        let hi = json_bits(c.get("hi")?, w)?;
                        full &= lo.is_zero() && hi == ones(w)?;
                        if i < cells {
                            covered.insert(i);
                        }
                        components.push((Component::Cell(group, slot, i), w, lo, hi));
                    }
                    if covered.len() == cells {
                        regions.insert((group, slot));
                    }
                }
            }
        }
        // D: every interface bundle and every region in the region's input
        // domain (§5.2, §5.3; tgt/fault included for oracles).
        let groups = if f.kind == "oracle" { 4 } else { 3 };
        let covers_d = full
            && f.params[..groups]
                .iter()
                .enumerate()
                .all(|(group, params)| {
                    params.iter().enumerate().all(|(slot, p)| match p.ty {
                        Type::Region(..) => regions.contains(&(group, slot)),
                        _ => bundles.contains(&(group, slot)),
                    })
                });
        Ok(Domain {
            components,
            covers_d,
        })
    }
    /// Executes region `f` on one domain element; returns the output tuple.
    fn execute_element(
        &self,
        f: &Function,
        element: &[(Component, BitVector)],
        budget: Option<Budget>,
    ) -> Result<Vec<BitVector>> {
        self.execute_element_audited(f, element, budget, None)
    }
    fn execute_element_audited(
        &self,
        f: &Function,
        element: &[(Component, BitVector)],
        budget: Option<Budget>,
        audit: Option<&mut Vec<crate::quantum::BorrowObservation>>,
    ) -> Result<Vec<BitVector>> {
        self.execute_element_bound(f, element, budget, audit, None)
    }
    fn execute_element_bound(
        &self,
        f: &Function,
        element: &[(Component, BitVector)],
        budget: Option<Budget>,
        mut audit: Option<&mut Vec<crate::quantum::BorrowObservation>>,
        context: Option<&replay09::Invocation>,
    ) -> Result<Vec<BitVector>> {
        let value = |name: &str, width: usize| -> Result<BitVector> {
            let (group, index) = interface_slot(f, name)?;
            Ok(element
                .iter()
                .find_map(|(c, v)| match c {
                    Component::Bundle(g, j) if (*g, *j) == (group, index) => Some(v.clone()),
                    _ => None,
                })
                .unwrap_or(BitVector::zero(width)?))
        };
        let cell = |region: &str, i: usize, width: usize| -> Result<BitVector> {
            let (group, slot) = interface_slot(f, region)?;
            Ok(element
                .iter()
                .find_map(|(c, v)| match c {
                    Component::Cell(g, s, j) if (*g, *s, *j) == (group, slot, i) => Some(v.clone()),
                    _ => None,
                })
                .unwrap_or(BitVector::zero(width)?))
        };
        let region_dims = |p: &crate::Param| -> Result<(usize, usize)> {
            let Type::Region(a, w) = p.ty else {
                return err("§5.1", "mem slot requires region type");
            };
            let cells = crate::oracle::power_of_two(a as u128)
                .and_then(|n| usize::try_from(n).ok())
                .ok_or_else(|| Error::host_resource("§12.2: host limit: region cells".into()))?;
            Ok((cells, w as usize))
        };
        if f.kind == "oracle" {
            let budget =
                budget.ok_or_else(|| Error::new("§12: oracle claim needs a budget".into()))?;
            let mut input = crate::OracleVectorInput::default();
            for p in &f.params[0] {
                input.ins.push(value(&p.name, p.ty.bits(self.ptr_width)?)?);
            }
            for p in &f.params[3] {
                let (cells, w) = region_dims(p)?;
                let mut bytes = crate::reserved(cells, "§12.2", "oracle replay region bytes")?;
                for i in 0..cells {
                    bytes.push(cell(&p.name, i, w)?.to_u128()? as u8);
                }
                input.regions.insert(p.name.clone(), bytes);
            }
            if let Some(context) = context {
                input.args.clone_from(&context.args);
            } else if !f.params[4].is_empty() {
                return err(
                    "§12",
                    "claim domains carry no classical arguments for this oracle",
                );
            }
            let primary = context.and_then(|c| c.primary.as_ref());
            let r = self.run_oracle_vectors_bound(
                &f.name,
                &input,
                budget,
                primary,
                None,
                context.map_or(0, |c| c.controls.len()),
            )?;
            if context.is_some() {
                // The sequential result alone does not witness clean workspace.
                // Check the independent reversible machine and the entire
                // successful/failed padded prefix, including uncomputation.
                let mut machine = crate::OracleVectorMachine::new_bound(
                    self,
                    &f.name,
                    &input,
                    budget,
                    primary,
                    None,
                    context.map_or(0, |c| c.controls.len()),
                )?;
                let entry = machine.snapshot();
                for _ in 0..budget.steps {
                    machine.forward_step()?;
                }
                let other = machine.outcome()?;
                if (other.payload, other.code) != (r.payload.clone(), r.code.clone()) {
                    return err("§12.1 K13/T3", "independent oracle replay differs");
                }
                for _ in 0..budget.steps {
                    machine.inverse_step()?;
                }
                if machine.snapshot() != entry || !machine.frames_clean() {
                    return err(
                        "§12.1 K13/T3",
                        "oracle replay does not restore clean workspace",
                    );
                }
            }
            let mut out = context.map_or_else(Vec::new, |c| c.controls.clone());
            let enabled = context.is_none_or(|c| c.controls.iter().all(|v| !v.is_zero()));
            out.extend(input.ins.iter().cloned());
            let target = value(&f.params[1][0].name, r.payload.width())?;
            let fault = value(&f.params[2][0].name, r.code.width())?;
            out.push(if enabled {
                target.binary("xor", &r.payload)?
            } else {
                target
            });
            out.push(if enabled {
                fault.binary("xor", &r.code)?
            } else {
                fault
            });
            for p in &f.params[3] {
                let (cells, w) = region_dims(p)?;
                crate::reserve_more(&mut out, cells, "§12.2", "oracle replay output cells")?;
                for i in 0..cells {
                    out.push(cell(&p.name, i, w)?);
                }
            }
            if context.is_some() {
                out.extend(element.iter().filter_map(|(c, v)| {
                    matches!(c, Component::Borrowed(..)).then_some(v.clone())
                }));
            }
            return Ok(out);
        }
        if context.is_none() && !f.params[3].is_empty() {
            return err(
                "§12",
                "claim domains carry no classical arguments for this action",
            );
        }
        let mut q = QuantumState::new();
        let mut b = QuantumBindings::default();
        if let Some(context) = context {
            b.args.extend(
                f.params[3]
                    .iter()
                    .zip(&context.args)
                    .map(|(p, a)| (p.name.clone(), a.clone())),
            );
        }
        let set = |q: &mut QuantumState, wires: &[u64], v: &BitVector| -> Result<()> {
            for (i, w) in wires.iter().enumerate() {
                if v.bit(i)? {
                    q.gate("x", &[*w], None, &[])?;
                }
            }
            Ok(())
        };
        for p in f.params[0].iter().chain(&f.params[1]) {
            let width = p.ty.bits(self.ptr_width)?;
            let wires = q.allocate(width)?;
            set(&mut q, &wires, &value(&p.name, width)?)?;
            b.bundles.insert(p.name.clone(), wires);
        }
        for p in &f.params[2] {
            let (cells, w) = region_dims(p)?;
            let mut all = crate::reserved(cells, "§12.2", "action replay region cells")?;
            for i in 0..cells {
                let wires = q.allocate(w)?;
                set(&mut q, &wires, &cell(&p.name, i, w)?)?;
                all.push(wires);
            }
            let Type::Region(a, w) = p.ty else {
                return err("§5.1", "mem slot requires region type");
            };
            b.regions.insert(
                p.name.clone(),
                crate::QuantumRegion {
                    address_width: a,
                    cell_width: w,
                    cells: all,
                },
            );
        }
        let mut borrowed = Vec::new();
        for (c, v) in element {
            if let Component::Borrowed(ordinal, _) = c {
                if *ordinal != borrowed.len() {
                    return err("§12.2", "borrowed component position mismatch");
                }
                let wires = q.allocate(v.width())?;
                set(&mut q, &wires, v)?;
                borrowed.push(wires.clone());
                b.borrowed.push(wires);
            }
        }
        if audit.is_some() {
            q.start_borrow_audit()?;
        }
        let mut control_wires = Vec::new();
        if let Some(context) = context {
            for value in &context.controls {
                let wires = q.allocate(1)?;
                set(&mut q, &wires, value)?;
                control_wires.extend(wires);
            }
        }
        self.execute_action(
            &f.name,
            &mut q,
            &b,
            context.is_some_and(|c| c.adjoint),
            &control_wires,
        )?;
        if context.is_some() {
            q.require_positive_basis()?;
        }
        if let Some(audit) = &mut audit {
            audit.extend(q.take_borrow_audit());
        }
        let read = |q: &QuantumState, wires: &[u64]| -> Result<BitVector> {
            let mut v = BitVector::zero(wires.len())?;
            for (i, w) in wires.iter().enumerate() {
                v.set(i, q.read_basis(&[*w])? == 1)?;
            }
            Ok(v)
        };
        let mut out = Vec::new();
        for wire in &control_wires {
            out.push(read(&q, &[*wire])?);
        }
        for p in f.params[0].iter().chain(&f.params[1]) {
            out.push(read(&q, &b.bundles[&p.name])?);
        }
        for p in &f.params[2] {
            for c in &b.regions[&p.name].cells {
                out.push(read(&q, c)?);
            }
        }
        for wires in &borrowed {
            out.push(read(&q, wires)?);
        }
        Ok(out)
    }
    fn claim_budget(&self, claim: &Json, f: &Function) -> Result<Option<Budget>> {
        if f.kind != "oracle" {
            return Ok(None);
        }
        let Some(subject) = claim.object()?.get("subject") else {
            return Ok(None);
        };
        let Some(schedule) = self.section("schedule") else {
            return Ok(None);
        };
        if subject.get("schedule_hash")?.string()?
            != crate::sha256_hex(schedule.canonical().as_bytes())
        {
            return Ok(None);
        }
        let b = schedule.get("bindings")?.get("budget")?.array()?;
        Ok(Some(Budget {
            steps: u64::try_from(b[0].uint()?).map_err(|_| Error::new("§11: steps".into()))?,
            heap: b[1].uint()?,
            stack: b[2].uint()?,
            depth: b[3].uint()?,
        }))
    }
    /// Checks one claim of region `closure`. A false claim is an error; an
    /// uncheckable one is `Unverified` with its reason. This standalone verdict
    /// does not establish executable applicability; see `verify_certificate`.
    pub fn verify_claim(&self, closure: &str, index: usize) -> Result<ClaimVerdict> {
        let verdict = self.verify_claim_guarded(closure, index, &mut BTreeSet::new())?;
        if self.isa_version == crate::IsaVersion::V09 {
            self.check_qinplace_bindings09()?;
        }
        Ok(verdict)
    }
    fn verify_claim_guarded(
        &self,
        closure: &str,
        index: usize,
        active: &mut BTreeSet<(String, usize)>,
    ) -> Result<ClaimVerdict> {
        if !active.insert((closure.to_string(), index)) {
            return err("§12", "cyclic claim reference");
        }
        let certificate = self
            .section("certificate")
            .ok_or_else(|| Error::new("§12: object has no certificate".into()))?;
        let region = certificate.get("regions")?.get(closure)?;
        let claims = region.get("claims")?.array()?;
        let claim = claims
            .get(index)
            .ok_or_else(|| Error::new(format!("§12: claim index {index} out of range")))?;
        let f = self.region_function(closure)?;
        let kind = claim.get("kind")?.string()?;
        let verdict = match kind {
            "exhaustive"
                if self.isa_version == crate::IsaVersion::V09
                    && claim.get("expected")? == &Json::String("inverse_pair".into()) =>
            {
                self.verify_inverse_pair_claim09(f, index, claim)?
            }
            "exhaustive" | "sampled" if self.isa_version == crate::IsaVersion::V09 => {
                self.verify_replay09(closure, index, claim, f)?.verdict
            }
            "exhaustive" | "sampled" => {
                let domain = self.domain(f, claim.get("domain")?)?;
                let budget = self.claim_budget(claim, f)?;
                if f.kind == "oracle" && budget.is_none() {
                    return Ok(ClaimVerdict::Unverified(
                        "an oracle claim needs a budget: bind its subject to this object's schedule".into(),
                    ));
                }
                let expected = claim.object()?.get("expected");
                if expected == Some(&Json::String("oracle".into())) {
                    return Ok(ClaimVerdict::Unverified(
                        "expected \"oracle\" compares a realisation under a schedule (target/schedule executor staged)".into(),
                    ));
                }
                let mut elements;
                if kind == "exhaustive" {
                    for lo in &domain.components {
                        if lo.2.unsigned_cmp(&lo.3)? == std::cmp::Ordering::Greater {
                            return err("§12.2", "domain interval with lo > hi");
                        }
                    }
                    elements = enumerate(&domain)?;
                } else {
                    let sampler = claim.get("sampler")?;
                    let seed = sampler
                        .get("seed")?
                        .array()?
                        .iter()
                        .map(|w| {
                            w.string()?
                                .parse::<u64>()
                                .map_err(|_| Error::new("§12.1: seed".into()))
                        })
                        .collect::<Result<Vec<_>>>()?;
                    let mut rng = Xoshiro256([seed[0], seed[1], seed[2], seed[3]]);
                    let count = sample_count(sampler)?;
                    elements = sample_elements(count)?;
                    for _ in 0..count {
                        let mut row = crate::reserved(
                            domain.components.len(),
                            "§12.1",
                            "sample tuple components",
                        )?;
                        for (_, w, lo, hi) in &domain.components {
                            row.push(rng.draw(*w, lo, hi)?);
                        }
                        elements.push(row);
                    }
                }
                let table = match expected {
                    Some(e) if e.object().is_ok_and(|o| o.contains_key("table")) => {
                        Some(e.get("table")?.array()?.to_vec())
                    }
                    _ => None,
                };
                let program = match expected {
                    Some(e) if e.object().is_ok_and(|o| o.contains_key("program")) => {
                        Some(self.region_function(e.get("program")?.string()?)?)
                    }
                    _ => None,
                };
                if let Some(t) = &table {
                    if kind == "exhaustive" && t.len() != elements.len() {
                        return err(
                            "§12.1",
                            format!(
                                "expected table has {} rows for {} domain elements",
                                t.len(),
                                elements.len()
                            ),
                        );
                    }
                }
                for (row, values) in elements.iter().enumerate() {
                    let element: Vec<(Component, BitVector)> = domain
                        .components
                        .iter()
                        .map(|c| c.0.clone())
                        .zip(values.iter().cloned())
                        .collect();
                    let out = self.execute_element(f, &element, budget)?;
                    if let Some(t) = &table {
                        let entry = t.get(row).ok_or_else(|| {
                            Error::new("§12.1: expected table is too short".into())
                        })?;
                        let got: Vec<Json> = out.iter().map(decimal_json).collect();
                        if entry.array()? != got.as_slice() {
                            return err("§12.1", format!("claim {index} of {closure}: element {row} yields {got:?}, the table says {entry:?}"));
                        }
                    }
                    if let Some(p) = program {
                        if p.signature() != f.signature() {
                            return err("§12.1", "expected program has a different signature");
                        }
                        let other = self.execute_element(p, &element, budget)?;
                        if other != out {
                            return err("§12.1", format!("claim {index} of {closure}: element {row} differs from the expected program"));
                        }
                    }
                }
                if kind == "exhaustive" && domain.covers_d {
                    ClaimVerdict::Proof
                } else {
                    ClaimVerdict::Evidence {
                        elements: elements.len() as u128,
                    }
                }
            }
            "structural" => {
                for sub in claim.get("subclaims")?.array()? {
                    let s = usize::try_from(sub.uint()?)
                        .map_err(|_| Error::new("§12: subclaim".into()))?;
                    if self.verify_claim_guarded(closure, s, active)? != ClaimVerdict::Proof {
                        return Ok(ClaimVerdict::Unverified(format!(
                            "subclaim {s} is not a verified proof"
                        )));
                    }
                }
                let witness = claim.get("witness")?;
                match claim.get("rule")?.string()? {
                    "translation_lemma" => {
                        self.check_translation_witness(f, witness)?;
                        ClaimVerdict::Proof
                    }
                    "inverse_pair_library" => {
                        if self.isa_version == crate::IsaVersion::V09 {
                            self.inverse_pair_theorem09(closure, index, &mut BTreeSet::new())?;
                        }
                        let library = witness.get("library_closure_hash")?.string()?;
                        let i = usize::try_from(witness.get("claim_index")?.uint()?)
                            .map_err(|_| Error::new("§12: claim index".into()))?;
                        if certificate.get("regions")?.object()?.contains_key(library) {
                            self.verify_claim_guarded(library, i, active)?
                        } else {
                            ClaimVerdict::Unverified(format!(
                                "library {library} is not linked into this certificate"
                            ))
                        }
                    }
                    _ => ClaimVerdict::Unverified(
                        "the adjoint_table rule's side conditions are not specified beyond its subclaims".into(),
                    ),
                }
            }
            _ => ClaimVerdict::Unverified(format!(
                "{kind} claims need the rigorous interval checker (§12.1), staged as deliverable 11"
            )),
        };
        active.remove(&(closure.to_string(), index));
        Ok(verdict)
    }
    fn check_translation_witness(&self, f: &Function, w: &Json) -> Result<()> {
        let hash = &self.identity()?.interface_hashes[&f.name];
        let points = |key: &str| -> Result<Vec<&crate::Instruction>> {
            w.get(key)?
                .array()?
                .iter()
                .map(|p| {
                    let p = p.array()?;
                    if p.len() != 3 || p[0].string()? != hash {
                        return err("§5.6/§12.1", "translation-lemma point outside the region");
                    }
                    let point = self
                        .point(hash, p[1].string()?, p[2].uint()?)
                        .map_err(|e| e.context("§5.6/§12.1"))?;
                    if !std::ptr::eq(point.function, f) {
                        return err("§5.6/§12.1", "point outside subject");
                    }
                    Ok(point.instruction)
                })
                .collect()
        };
        let names = |key: &str| -> Result<BTreeSet<String>> {
            w.get(key)?
                .array()?
                .iter()
                .map(|s| Ok(s.string()?.to_string()))
                .collect()
        };
        let frame = points("frame")?;
        if frame.len() != 2 {
            return err("§5.6/§12.1", "frame needs two endpoints");
        }
        self.check_translation_frame(
            f,
            [frame[0], frame[1]],
            &points("V")?,
            &points("W")?,
            &names("X")?,
            &names("B")?,
        )
    }
    /// Checks every claim of the certificate: false claims are errors, and
    /// the report lists each claim's verdict and independent K92 obligations.
    pub fn verify_certificate(&self) -> Result<CertificateReport> {
        let certificate = self
            .section("certificate")
            .ok_or_else(|| Error::new("§12: object has no certificate".into()))?;
        let applicability = if self.isa_version == crate::IsaVersion::V09 {
            self.check_qinplace_bindings09()?
        } else {
            BTreeMap::new()
        };
        let mut reports = Vec::new();
        for (closure, region) in certificate.get("regions")?.object()? {
            let name = self.region_function(closure)?.name.clone();
            let f = self.region_function(closure)?;
            for (index, claim) in region.get("claims")?.array()?.iter().enumerate() {
                let kind = claim.get("kind")?.string()?;
                let (verdict, coverage) = if self.isa_version == crate::IsaVersion::V09
                    && matches!(kind, "exhaustive" | "sampled")
                    && claim.object()?.get("expected") != Some(&Json::String("inverse_pair".into()))
                {
                    let outcome = self.verify_replay09(closure, index, claim, f)?;
                    (outcome.verdict, outcome.coverage)
                } else {
                    (
                        self.verify_claim_guarded(closure, index, &mut BTreeSet::new())?,
                        None,
                    )
                };
                reports.push(ClaimReport {
                    closure_hash: closure.clone(),
                    region: name.clone(),
                    index,
                    kind: kind.into(),
                    verdict,
                    context_key: Json::Array(Vec::new()),
                    coverage,
                    qinplace_applicability: applicability.get(closure).cloned(),
                });
            }
            // A borrow_frames claim must be a proof over D with the §5.6 property.
            for i in region.get("verification")?.get("borrow_frames")?.array()? {
                let i = usize::try_from(i.uint()?)
                    .map_err(|_| Error::new("§12: claim index".into()))?;
                if reports
                    .iter()
                    .any(|r| r.region == name && r.index == i && r.verdict != ClaimVerdict::Proof)
                {
                    return err(
                        "§5.6",
                        format!("borrow_frames claim {i} of @{name} is not a proof over D"),
                    );
                }
                self.check_borrow_independence(f, closure, i)?;
            }
        }
        Ok(CertificateReport {
            claims: reports,
            qinplace_applicability: applicability,
        })
    }
    /// §5.6 library route: a region whose frames the symbolic decision cannot
    /// settle is admitted iff each of its certificate `borrow_frames` claims
    /// is a verified proof over D that restores every borrowed component and
    /// whose other outputs do not depend on the borrowed entry values.
    pub(crate) fn borrow_frames_certified(&self, f: &Function) -> Result<bool> {
        let Some(certificate) = self.section("certificate") else {
            return Ok(false);
        };
        let identity = self.identity()?;
        let Some(Some(closure)) = identity.closure_hashes.get(&f.name) else {
            return Ok(false);
        };
        let Ok(region) = certificate.get("regions").and_then(|r| r.get(closure)) else {
            return Ok(false);
        };
        let indices = region.get("verification")?.get("borrow_frames")?.array()?;
        if indices.is_empty() {
            return Ok(false);
        }
        for i in indices {
            let i =
                usize::try_from(i.uint()?).map_err(|_| Error::new("§12: claim index".into()))?;
            if self.verify_claim(closure, i)? != ClaimVerdict::Proof {
                return err(
                    "§5.6",
                    format!("borrow_frames claim {i} is not a verified proof over D"),
                );
            }
            self.check_borrow_independence(f, closure, i)?;
        }
        Ok(true)
    }
    fn check_borrow_independence(&self, f: &Function, closure: &str, index: usize) -> Result<()> {
        // §12.1 tuple replay does not prove the §14.3 T3 permutation premise.
        // Require permutation-only borrowed touches even when phases happen to
        // cancel, or are invisible on a known-clean auxiliary wire.
        self.check_borrow_frame_structure(f)?;
        let certificate = self
            .section("certificate")
            .ok_or_else(|| Error::new("§12: object has no certificate".into()))?;
        let claims = certificate
            .get("regions")?
            .get(closure)?
            .get("claims")?
            .array()?;
        let claim = claims
            .get(index)
            .ok_or_else(|| Error::new("§12: claim index out of range".into()))?;
        let domain = self.domain(f, claim.get("domain")?)?;
        if !domain
            .components
            .iter()
            .any(|c| matches!(c.0, Component::Borrowed(..)))
        {
            return err(
                "§5.6",
                "a borrow_frames claim must range over the borrowed bundles",
            );
        }
        // Group elements by their non-borrowed part: outputs must agree and
        // borrowed outputs must equal borrowed inputs.
        let mut by_rest: BTreeMap<Vec<String>, Vec<String>> = BTreeMap::new();
        let mut at_return = BTreeMap::new();
        for values in enumerate(&domain)? {
            let element: Vec<(Component, BitVector)> = domain
                .components
                .iter()
                .map(|c| c.0.clone())
                .zip(values)
                .collect();
            let mut audit = Vec::new();
            let out = self.execute_element_audited(f, &element, None, Some(&mut audit))?;
            // Each completed lifetime is checked before any future borrowing.
            // Prior checked frames are independent of their returned entries,
            // so reusing a physical pool bit cannot cancel an invalid lifetime.
            for (ordinal, (wires, rest, output)) in audit.into_iter().enumerate() {
                let key = (ordinal, wires, rest);
                if at_return.get(&key).is_some_and(|prior| *prior != output) {
                    return err("§5.6", "qreturn outputs depend on its borrowed entry");
                }
                at_return.insert(key, output);
            }
            let borrowed_in: Vec<String> = element
                .iter()
                .filter(|(c, _)| matches!(c, Component::Borrowed(..)))
                .map(|(_, v)| v.to_decimal())
                .collect();
            let k = borrowed_in.len();
            let split = out
                .len()
                .checked_sub(k)
                .ok_or_else(|| Error::new("§12: output tuple".into()))?;
            let borrowed_out: Vec<String> =
                out[split..].iter().map(BitVector::to_decimal).collect();
            if borrowed_in != borrowed_out {
                let names: Vec<&str> = element
                    .iter()
                    .filter_map(|(c, _)| match c {
                        Component::Borrowed(_, n) => Some(n.as_str()),
                        _ => None,
                    })
                    .collect();
                return err(
                    "§5.6",
                    format!("borrowed components {names:?} are not restored"),
                );
            }
            let rest: Vec<String> = element
                .iter()
                .filter(|(c, _)| !matches!(c, Component::Borrowed(..)))
                .map(|(_, v)| v.to_decimal())
                .collect();
            let outputs: Vec<String> = out[..split].iter().map(BitVector::to_decimal).collect();
            if by_rest.get(&rest).is_some_and(|prior| *prior != outputs) {
                return err("§5.6", "outputs depend on borrowed entry values");
            }
            by_rest.insert(rest, outputs);
        }
        Ok(())
    }
}

#[cfg(test)]
mod r20_tests {
    use super::*;
    #[test]
    fn r20_exhaustive_domain_cardinality_extremes() {
        let mut cases = 0;
        for hi in [
            0u128,
            1,
            (1 << 63) - 1,
            1 << 63,
            u64::MAX as u128 - 1,
            u64::MAX as u128,
        ] {
            let d = Domain {
                covers_d: false,
                components: vec![(
                    Component::Bundle(0, 0),
                    64,
                    BitVector::zero(64).unwrap(),
                    BitVector::from_u128(64, hi).unwrap(),
                )],
            };
            let result = std::panic::catch_unwind(|| enumerate(&d)).expect("no cardinality panic");
            if hi <= 1 {
                assert_eq!(result.unwrap().len(), hi as usize + 1);
            } else {
                let e = result.unwrap_err().to_string();
                assert!(e.contains("§12.2") && e.contains("host limit"), "{e}");
            }
            let sampled =
                std::panic::catch_unwind(|| sample_elements(hi)).expect("no sample count panic");
            if hi <= 1 {
                sampled.unwrap();
            } else {
                let e = sampled.unwrap_err().to_string();
                assert!(e.contains("§12.1") && e.contains("host limit"), "{e}");
            }
            cases += 2;
        }
        assert_eq!(cases, 12);
        eprintln!("R20 exhaustive/sample storage: 2 paths, {cases} cases");
    }
}

#[cfg(test)]
mod r22_coverage_tests {
    use super::*;
    #[test]
    fn sol_r22_b01_resolved_role_collision_family() {
        let o = Object::parse(include_str!("../tests/fixtures/r22/false-cnot-proof.bisa")).unwrap();
        let mut f = o.functions["a"].clone();
        let mut region = f.params[0][0].clone();
        region.name = "r".into();
        region.ty = Type::Region(0, 1);
        f.params[2].push(region);
        let mut cases = 0;
        for borrowed in ["t", "u", "r", "b"] {
            for subset in 0..8 {
                for (cell_mode, cell_full) in [
                    ("\"all\"", true),
                    ("[{\"index\":0,\"lo\":0,\"hi\":1}]", true),
                    ("[]", false),
                    ("[{\"index\":0,\"lo\":0,\"hi\":0}]", false),
                ] {
                    for full_range in [false, true] {
                        let bundles = ["t", "u"]
                            .iter()
                            .enumerate()
                            .filter(|(i, _)| subset & (1 << i) != 0)
                            .map(|(_, n)| {
                                format!(
                                    r#"{{"name":"{n}","width":1,"lo":0,"hi":{}}}"#,
                                    u8::from(full_range)
                                )
                            })
                            .collect::<Vec<_>>()
                            .join(",");
                        let regions = if subset & 4 != 0 {
                            format!(r#"{{"name":"r","cells":{cell_mode}}}"#)
                        } else {
                            String::new()
                        };
                        let d = Json::parse(&format!(r#"{{"bundles":[{bundles}],"regions":[{regions}],"borrowed":[{{"name":"{borrowed}","width":1,"lo":0,"hi":1}}]}}"#)).unwrap();
                        let domain = o.domain(&f, &d).unwrap();
                        assert_eq!(
                            domain.covers_d,
                            subset == 7 && full_range && cell_full,
                            "borrowed={borrowed}, subset={subset}, full={full_range}"
                        );
                        cases += 1;
                    }
                }
            }
        }
        assert_eq!(cases, 256);
    }
}
````

## `reference-interpreter/src/lib.rs` (204 lines)

````rust
//! Executable reference semantics for the Bennett ISA, version 0.8.
mod action;
mod bits;
mod borrow;
mod call_discipline;
mod certificate;
mod claims;
mod classical;
mod controls;
mod exact;
mod handle_validation;
mod identity;
mod instances;
pub mod json;
mod linking;
mod machine;
mod metadata;
mod metadata_schema;
mod metadata_types;
mod object;
mod oracle;
mod quantum;
pub mod ref_library;
mod registers;
mod retained;
mod tokens;
pub use retained::Retained;
pub use tokens::BudgetToken;
mod schema;
mod sha256;
mod validation;
pub use bits::BitVector;
pub use borrow::validate_translation_lemma;
pub use claims::{
    CertificateReport, ClaimCoverage, ClaimReport, ClaimVerdict, FixedRegionBinding,
    QinplaceApplicability, Xoshiro256,
};
pub use classical::{
    ClassicalMachine, ClassicalOutcome, ClassicalSnapshot, ClassicalValue, RegisterDelta,
    SnapshotDelta, StepPoint, TapeEntry,
};
pub use classical::{HostExchange, HostRequest, HostRequestData};
pub use identity::Identity;
pub use machine::{
    BasisConfiguration, BasisVectorConfiguration, DerivedWidths, OracleMachine, OracleVectorMachine,
};
pub use metadata::{ScheduleEpsilonShare, ScheduleExpansion};
pub use object::*;
pub use oracle::{
    Argument, Budget, OracleInput, OracleOutcome, OracleVectorInput, OracleVectorOutcome,
};
pub use quantum::{Complex, MeasurementBranch, QuantumBindings, QuantumRegion, QuantumState};
pub use registers::QuantumRegisters;
pub use sha256::{sha256, sha256_hex};

/// A diagnostic always names the normative rule that was violated.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Error(pub String, pub ErrorKind);
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ErrorKind {
    Diagnostic,
    HostResource,
}
impl Error {
    pub fn new(message: String) -> Self {
        Self(message, ErrorKind::Diagnostic)
    }
    pub fn host_resource(message: String) -> Self {
        Self(message, ErrorKind::HostResource)
    }
    pub fn kind(&self) -> ErrorKind {
        self.1
    }
    pub fn context(self, rule: &str) -> Self {
        Self(format!("{rule}: {}", self.0), self.1)
    }
}
pub(crate) fn resource_error(rule: &str, message: impl std::fmt::Display) -> Error {
    Error(
        format!("{rule}: host limit: {message}"),
        ErrorKind::HostResource,
    )
}
impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.0)
    }
}
impl std::error::Error for Error {}
pub type Result<T> = std::result::Result<T, Error>;
pub(crate) fn err<T>(rule: &str, message: impl std::fmt::Display) -> Result<T> {
    Err(Error::new(format!("{rule}: {message}")))
}
pub fn version() -> &'static str {
    "0.8"
}

/// Reserve text-derived storage fallibly before iteration or initialization.
pub(crate) fn reserved<T>(count: usize, rule: &str, what: &str) -> Result<Vec<T>> {
    let mut out = Vec::new();
    reserve_more(&mut out, count, rule, what)?;
    Ok(out)
}

/// Check cumulative storage before a count-driven loop or any visible mutation.
pub(crate) fn reserve_more<T>(
    out: &mut Vec<T>,
    count: usize,
    rule: &str,
    what: &str,
) -> Result<()> {
    preparation(rule, what)?;
    out.len()
        .checked_add(count)
        .ok_or_else(|| resource_error(rule, format!("{what} cumulative count exceeds usize")))?;
    out.try_reserve_exact(count).map_err(|e| {
        resource_error(
            rule,
            format!("{what} allocation of {count} elements failed: {e}"),
        )
    })?;
    Ok(())
}

#[cfg(test)]
mod r21_tests {
    use super::*;
    #[test]
    fn r21_derived_consumers_memory_limited() {
        if std::env::var_os("R21_UNIT_CHILD").is_none() {
            let out = std::process::Command::new("python3").args(["-c",
                "import os,resource,sys; resource.setrlimit(resource.RLIMIT_AS,(256*1024*1024,)*2); resource.setrlimit(resource.RLIMIT_CORE,(0,0)); os.execv(sys.argv[1],sys.argv[1:])"])
                .arg(std::env::current_exe().unwrap())
                .args(["--exact", "r21_tests::r21_derived_consumers_memory_limited", "--nocapture"])
                .env("R21_UNIT_CHILD", "1").output().unwrap();
            assert!(out.status.success(), "{out:?}");
            eprintln!("{}", String::from_utf8_lossy(&out.stderr));
            return;
        }
        std::panic::catch_unwind(|| {
            crate::oracle::r21_resource_cases();
            crate::claims::r21_resource_cases();
            crate::classical::r21_resource_cases();
            for count in [0, 1, 8, (1usize << 63) - 1, 1 << 63, usize::MAX] {
                let mut console = vec![0u8; 8];
                let result = reserve_more(&mut console, count, "§7.3", "console bytes");
                if count <= 8 {
                    result.unwrap();
                } else {
                    let e = result.unwrap_err().to_string();
                    assert!(e.contains("§7.3") && e.contains("host limit"), "{e}");
                }
                assert_eq!(console, vec![0; 8]);
            }
            eprintln!("R21 cumulative console storage: 1 path / 6 cases");
        })
        .expect("no derived-cardinality or transfer panic");
    }
}

// Test-only, thread-local stage injection: no global allocator replacement and
// no interference with concurrent tests. Production preparation is a no-op.
#[inline]
pub(crate) fn preparation(rule: &str, stage: &str) -> Result<()> {
    #[cfg(test)]
    allocation_test::hit(rule, stage)?;
    #[cfg(not(test))]
    let _ = (rule, stage);
    Ok(())
}
#[cfg(test)]
pub(crate) mod allocation_test {
    use std::cell::RefCell;
    thread_local! {
        static PLAN: RefCell<Option<(usize, usize, Vec<String>)>> = const { RefCell::new(None) };
    }
    pub fn start(fail_at: usize) {
        PLAN.with(|p| *p.borrow_mut() = Some((fail_at, 0, Vec::new())));
    }
    pub fn finish() -> Vec<String> {
        PLAN.with(|p| p.borrow_mut().take().expect("injection armed").2)
    }
    pub fn hit(rule: &str, stage: &str) -> crate::Result<()> {
        PLAN.with(|p| {
            if let Some((fail_at, count, stages)) = &mut *p.borrow_mut() {
                stages.push(stage.to_owned());
                let index = *count;
                *count += 1;
                if index == *fail_at {
                    return Err(crate::resource_error(
                        rule,
                        format!("injected preparation {index}: {stage}"),
                    ));
                }
            }
            Ok(())
        })
    }
}

#[cfg(test)]
mod r23_transaction;

mod source_constructor;
````

## `reference-interpreter/src/source_constructor/action/qinplace.rs` (67 lines)

````rust
//! K22 adapters capture the ins/mem/args/token context; the pinned qinplace
//! recipe owns instruction allocation/release order in both orientations.
use super::*;
impl Compiler<'_> {
    pub(super) fn qinplace(&mut self, i: &crate::Instruction, env: &Env) -> Result<Vec<Value>> {
        let a = &i.operands;
        let n = env.width(&a[3])?;
        let f = self.object.functions[a[0].trim_start_matches('@')].params[2][0]
            .ty
            .bits(self.object.ptr_width)?;
        let names = [
            format!("$qinplace/x/{}", self.counter),
            format!("$qinplace/t/{}", self.counter),
            format!("$qinplace/f/{}", self.counter),
        ];
        let mut bound = env.clone();
        bound.predicates.clear();
        for (name, width) in names.iter().zip([n, n, f]) {
            bound.wires.insert(name.clone(), (name.clone(), width));
        }
        // The temporary Instruction passes through the public operand-list
        // parser. Give its private x formal a collision-free lexical alias;
        // keep the actual constructor identity in the environment.
        let mut input_name = format!("qinplace_x_{}", self.counter);
        while bound.wires.contains_key(&input_name) {
            input_name.push('_');
        }
        bound
            .wires
            .insert(input_name.clone(), (names[0].clone(), n));
        let mut inputs = vec![input_name];
        if a.len() == 7 {
            inputs.extend(crate::object::list(&a[4])?);
        }
        let mut call = i.clone();
        call.op = "oracle_call".into();
        call.lhs.clear();
        call.operands = vec![
            a[0].clone(),
            a[2].clone(),
            format!("({})", inputs.join(", ")),
            names[1].clone(),
            names[2].clone(),
            a.get(5).cloned().unwrap_or_else(|| "()".into()),
            a.get(6).cloned().unwrap_or_else(|| "()".into()),
        ];
        let formals = names
            .iter()
            .zip([n, n, f])
            .map(|(name, width)| formal(name, width))
            .collect::<Result<Vec<_>>>()?;
        let g = template(formals.clone(), self.call(&call, &bound)?);
        call.operands[0] = a[1].clone();
        let h = template(formals, self.call(&call, &bound)?);
        Ok(vec![invoke(
            "qinplace",
            [
                number(n)?,
                number(f)?,
                env.wire(&a[3])?,
                array([g]),
                array([h]),
                array(env.predicates.clone()),
            ],
        )])
    }
}
````

## `reference-interpreter/src/source_constructor/action.rs` (715 lines)

````rust
//! Structured source formation, before catalog recipe instantiation.
use super::*;
use bennett_isa_conformance::ref_language::{SourceBody, SourcePoint, SourceSymbol};
#[derive(Clone)]
struct Region {
    cells: String,
    address: usize,
    cell: usize,
    origin: Value,
}
#[derive(Clone, Default)]
struct Env {
    wires: BTreeMap<String, (String, usize)>,
    regions: BTreeMap<String, Region>,
    predicates: Vec<Value>,
    iteration: Vec<usize>,
}
struct Compiler<'a> {
    object: &'a crate::Object,
    values: &'a BTreeMap<String, Value>,
    tokens: &'a bennett_isa_conformance::ref_language::SourceTokenContext,
    declarations: Vec<(String, usize, String, String)>,
    symbols: Vec<SourceSymbol>,
    counter: usize,
    hashes: BTreeMap<String, Option<String>>,
    symbol: String,
    points: BTreeMap<String, SourcePoint>,
    locations: BTreeMap<usize, (String, usize)>,
    compiled: BTreeMap<crate::validation::cleanup::Key, Compiled>,
}
#[derive(Clone)]
struct Compiled {
    nodes: Vec<Value>,
    before: Env,
    after: Env,
    tag: String,
}
impl Env {
    fn wire(&self, name: &str) -> Result<Value> {
        if name == "()" {
            return Ok(array([]));
        }
        if let Some((base, index)) = name.split_once('[') {
            let index = index
                .strip_suffix(']')
                .ok_or_else(|| Error::new("§11.1: malformed wire index".into()))?;
            let (alias, _) = self
                .wires
                .get(base)
                .ok_or_else(|| Error::new(format!("§11.1: unbound source wire {base}")))?;
            return Ok(text(format!("{alias}[{index}]")));
        }
        Ok(text(
            &self
                .wires
                .get(name)
                .ok_or_else(|| Error::new(format!("§11.1: unbound source wire {name}")))?
                .0,
        ))
    }
    fn width(&self, name: &str) -> Result<usize> {
        if name.contains('[') {
            return Ok(1);
        }
        self.wires
            .get(name)
            .map(|v| v.1)
            .ok_or_else(|| Error::new(format!("§11.1: missing source width {name}")))
    }
    fn indexed(&self, name: &str, i: usize) -> Result<Value> {
        if name.contains('[') {
            if i != 0 {
                return Err(Error::new("§11.1: scalar index out of range".into()));
            }
            self.wire(name)
        } else {
            let (alias, w) = self
                .wires
                .get(name)
                .ok_or_else(|| Error::new("§11.1: unknown source wire".into()))?;
            if i >= *w {
                return Err(Error::new("§11.1: source bit out of range".into()));
            }
            Ok(bit(alias, i))
        }
    }
    fn region(&self, name: &str, role: &str) -> Result<Value> {
        let r = self
            .regions
            .get(name)
            .ok_or_else(|| Error::new(format!("§11.1: unknown source region {name}")))?;
        Ok(obj([
            ("address", number(r.address)?),
            ("cell", number(r.cell)?),
            ("role", text(role)),
            ("origin", r.origin.clone()),
            ("cells", text(&r.cells)),
        ]))
    }
}
fn controlled(env: &Env, body: Vec<Value>) -> Vec<Value> {
    if body.is_empty() || env.predicates.is_empty() {
        body
    } else {
        vec![under(array(env.predicates.clone()), body)]
    }
}
impl Compiler<'_> {
    fn declare(&mut self, width: usize, class: &str, state: &str) -> String {
        let name = format!("$source-allocation/{}", self.counter);
        self.counter += 1;
        self.declarations
            .push((name.clone(), width, class.into(), state.into()));
        name
    }
    fn value(&self, name: &str) -> Result<Value> {
        self.values
            .get(name)
            .cloned()
            .ok_or_else(|| Error::new(format!("§11.1: missing fixed argument {name}")))
    }
    fn call(&mut self, i: &crate::Instruction, env: &Env) -> Result<Vec<Value>> {
        let normal = crate::validation::normalize_call(i)?;
        let a = &normal.instruction.operands;
        let oracle = normal.instruction.op == "oracle_call";
        let f = &self.object.functions[a[0].trim_start_matches('@')];
        let alias = format!("$source-call/{}", self.counter);
        self.counter += 1;
        let hash = self.hashes[&f.name]
            .clone()
            .ok_or_else(|| Error::new("§11.1: unlinked call".into()))?;
        let context = if oracle {
            Some(obj([("token", self.value(&a[1])?)]))
        } else {
            None
        };
        let tokens = crate::ref_library::tokens::forward(
            f,
            oracle.then_some(a[1].as_str()),
            &crate::object::list(&a[if oracle { 6 } else { 4 }])?,
            &self.tokens.arguments,
        )?;
        self.symbols.push(SourceSymbol {
            name: alias.clone(),
            hash,
            oracle_invocation: context,
            tokens: Some(tokens),
            adjoint: normal.adjoint && !oracle,
        });
        let mut args = Vec::new();
        if oracle {
            for n in crate::object::list(&a[2])? {
                args.push(env.wire(&n)?);
            }
            args.extend([env.wire(&a[3])?, env.wire(&a[4])?]);
        } else {
            for group in [1usize, 2] {
                for n in crate::object::list(&a[group])? {
                    args.push(env.wire(&n)?);
                }
            }
        }
        let mem = if oracle { 5 } else { 3 };
        let parameters = if oracle { 3 } else { 2 };
        for (p, n) in f.params[parameters]
            .iter()
            .zip(crate::object::list(&a[mem])?)
        {
            args.push(env.region(&n, p.role.as_deref().unwrap_or("in"))?);
        }
        for n in crate::object::list(&a[mem + 1])? {
            args.push(self.value(&n)?);
        }
        let mut body = vec![invoke(
            if oracle { "oracle_call" } else { "action_call" },
            [text(alias), array(args)],
        )];
        if let Some(control) = normal.control {
            body = vec![under(env.wire(&control)?, body)];
        }
        Ok(controlled(env, body))
    }
    fn sequence(&mut self, seq: &[crate::Instruction], env: &mut Env) -> Result<Vec<Value>> {
        let mut out = Vec::new();
        for i in seq {
            let start = out.len();
            let before = env.clone();
            let a = &i.operands;
            let op = i.op.as_str();
            match op {
                "qregion" => {}
                "qpred" => env.predicates.push(env.wire(&a[0])?),
                "qunpred" => {
                    env.predicates
                        .pop()
                        .ok_or_else(|| Error::new("§11.1: predicate stack underflow".into()))?;
                }
                "qalloc" | "qborrow" => {
                    let width =
                        usize::try_from(crate::object::host_count(&a[1], "allocation width")?)
                            .map_err(|_| {
                                crate::resource_error("§11.1", "allocation width exceeds host")
                            })?;
                    let name = self.declare(
                        width,
                        &a[0],
                        if op == "qborrow" { "borrowed" } else { "clean" },
                    );
                    env.wires.insert(i.lhs[0].clone(), (name.clone(), width));
                    out.push(obj([("acquire", text(name))]));
                }
                "qfree" | "qreturn" => {
                    let (name, _) = env
                        .wires
                        .remove(&a[0])
                        .ok_or_else(|| Error::new("§11.1: unknown released value".into()))?;
                    out.push(obj([("relinquish", text(name))]));
                }
                "qcopy" => {
                    let width = env.width(&a[0])?;
                    let name = self.declare(width, "any", "clean");
                    out.push(obj([("acquire", text(&name))]));
                    let body = (0..width)
                        .map(|b| Ok(gate("cx", [env.indexed(&a[0], b)?, bit(&name, b)])))
                        .collect::<Result<Vec<_>>>()?;
                    out.extend(controlled(env, body));
                    env.wires.insert(i.lhs[0].clone(), (name, width));
                }
                "quncopy" => {
                    let (name, width) = env
                        .wires
                        .get(&a[1])
                        .cloned()
                        .ok_or_else(|| Error::new("§11.1: unknown copied value".into()))?;
                    let body = (0..width)
                        .map(|b| Ok(gate("cx", [env.indexed(&a[0], b)?, bit(&name, b)])))
                        .collect::<Result<Vec<_>>>()?;
                    out.extend(controlled(env, body));
                    out.push(obj([("relinquish", text(name))]));
                    env.wires.remove(&a[1]);
                }
                "qxor" | "qexch" => {
                    let width = env.width(&a[0])?;
                    let body = (0..width)
                        .map(|b| {
                            Ok(gate(
                                if op == "qxor" { "cx" } else { "swap" },
                                [env.indexed(&a[0], b)?, env.indexed(&a[1], b)?],
                            ))
                        })
                        .collect::<Result<Vec<_>>>()?;
                    out.extend(controlled(env, body));
                }
                "qif" => {
                    let predicate = env.wire(&a[0])?;
                    let outer = env.predicates.clone();
                    env.predicates.push(predicate.clone());
                    out.extend(self.sequence(&i.bodies[0], env)?);
                    env.predicates = outer.clone();
                    out.extend(controlled(env, vec![gate("x", [predicate.clone()])]));
                    env.predicates.push(predicate.clone());
                    out.extend(self.sequence(&i.bodies[1], env)?);
                    env.predicates = outer;
                    out.extend(controlled(env, vec![gate("x", [predicate])]));
                }
                "qloop" => {
                    let count = usize::try_from(crate::object::host_count(&a[0], "loop count")?)
                        .map_err(|_| crate::resource_error("§11.1", "loop count exceeds host"))?;
                    let _capacity = crate::reserved::<u8>(count, "§11.1", "source loop instances")?;
                    let outer = env.predicates.clone();
                    let mut flags = None;
                    let mut computes = Vec::new();
                    if a.len() == 3 && count > 0 {
                        let name = self.declare(count, "any", "clean");
                        out.push(obj([("acquire", text(&name))]));
                        let first = gate("cx", [env.indexed(&a[2], 0)?, bit(&name, 0)]);
                        out.extend(controlled(env, vec![first.clone()]));
                        computes.push(first);
                        flags = Some(name);
                    }
                    let outer_iteration = env.iteration.clone();
                    for iteration in 0..count {
                        env.iteration.push(iteration);
                        if let Some(name) = &flags {
                            env.predicates.push(bit(name, iteration));
                        }
                        // A unit-count body adapter captures this source instance,
                        // including its immutable oracle contexts, before splicing.
                        let body = self.sequence(&i.bodies[0], env)?;
                        out.push(invoke("qloop", [number(1)?, array(body)]));
                        env.predicates = outer.clone();
                        env.iteration = outer_iteration.clone();
                        if let Some(name) = &flags {
                            if iteration + 1 < count {
                                let next = gate(
                                    "ccx",
                                    [
                                        bit(name, iteration),
                                        env.indexed(&a[2], iteration + 1)?,
                                        bit(name, iteration + 1),
                                    ],
                                );
                                out.extend(controlled(env, vec![next.clone()]));
                                computes.push(next);
                            }
                        }
                    }
                    if let Some(name) = flags {
                        computes.reverse();
                        out.extend(controlled(env, computes));
                        out.push(obj([("relinquish", text(name))]));
                    }
                }
                "qload" | "qunload" | "qstore" | "qexchm" => {
                    let region = env
                        .regions
                        .get(&a[0])
                        .cloned()
                        .ok_or_else(|| Error::new("§11.1: missing source region".into()))?;
                    let count = 1usize
                        .checked_shl(region.address.try_into().map_err(|_| {
                            crate::resource_error("§11.1", "region address width exceeds host")
                        })?)
                        .ok_or_else(|| {
                            crate::resource_error("§11.1", "region extent exceeds host")
                        })?;
                    let address = env.wire(&a[1])?;
                    let name = if op == "qload" {
                        let name = self.declare(region.cell, "any", "clean");
                        out.push(obj([("acquire", text(&name))]));
                        env.wires
                            .insert(i.lhs[0].clone(), (name.clone(), region.cell));
                        name
                    } else {
                        env.wires
                            .get(&a[2])
                            .ok_or_else(|| Error::new("§11.1: missing memory value".into()))?
                            .0
                            .clone()
                    };
                    let operation = match op {
                        "qstore" => "dispatch.store",
                        "qexchm" => "dispatch.exchange",
                        _ => "dispatch.copy",
                    };
                    out.extend(controlled(
                        env,
                        vec![invoke(
                            operation,
                            [
                                number(region.address)?,
                                number(count)?,
                                number(region.cell)?,
                                address,
                                text(&region.cells),
                                text(&name),
                            ],
                        )],
                    ));
                    if op == "qunload" {
                        out.push(obj([("relinquish", text(name))]));
                        env.wires.remove(&a[2]);
                    }
                }
                "qinplace" => out.extend(self.qinplace(i, env)?),
                "oracle_call" | "action_call" | "ctl" | "adj" => out.extend(self.call(i, env)?),
                _ => {
                    let mut node = if matches!(op, "rx" | "ry" | "rz") {
                        let angle = if let Some(value) = self.values.get(&a[0]) {
                            value.clone()
                        } else {
                            text(format!(
                                "0x{:016x}",
                                a[0].parse::<f64>()
                                    .map_err(|_| Error::new("§11.1: malformed angle".into()))?
                                    .to_bits()
                            ))
                        };
                        obj([
                            ("gate", text(op)),
                            ("wires", array([env.wire(&a[1])?])),
                            ("params", array([angle])),
                        ])
                    } else if op == "mcx" {
                        let mut wires = crate::object::list(&a[0])?
                            .iter()
                            .map(|n| env.wire(n))
                            .collect::<Result<Vec<_>>>()?;
                        wires.push(env.wire(&a[1])?);
                        gate(op, wires)
                    } else if matches!(
                        op,
                        "x" | "h" | "s" | "sdg" | "t" | "tdg" | "cx" | "cz" | "swap" | "ccx"
                    ) {
                        gate(
                            op,
                            a.iter().map(|n| env.wire(n)).collect::<Result<Vec<_>>>()?,
                        )
                    } else {
                        return Err(Error::new(format!(
                            "§11.1: unknown source action operation {op}"
                        )));
                    };
                    // Keep the JSON node's typed angle rather than host float text.
                    out.extend(controlled(
                        env,
                        vec![std::mem::replace(&mut node, Value::Null)],
                    ));
                }
            }
            let (point, _) = self.locations.get(&i.line).cloned().ok_or_else(|| {
                Error::new("§11.1: structured operation has no source point".into())
            })?;
            let tag = format!("$source-point/{}", self.counter);
            self.counter += 1;
            self.points.insert(
                tag.clone(),
                SourcePoint {
                    symbol: self.symbol.clone(),
                    point,
                    iteration: env.iteration.clone(),
                    instance: Vec::new(),
                },
            );
            let nodes = out.split_off(start);
            if !matches!(op, "qif" | "qloop") {
                self.compiled.insert(
                    (i.line, env.iteration.clone()),
                    Compiled {
                        nodes: nodes.clone(),
                        before,
                        after: env.clone(),
                        tag: tag.clone(),
                    },
                );
            }
            out.push(obj([
                ("for", text(tag)),
                ("from", Value::Num(0.0)),
                ("to", Value::Num(1.0)),
                ("body", array(nodes)),
            ]));
        }
        Ok(out)
    }
}
fn source_adjoint(body: Vec<Value>, symbols: &mut [SourceSymbol]) -> Result<Vec<Value>> {
    let mut out = Vec::new();
    for mut node in body.into_iter().rev() {
        let Value::Obj(m) = &mut node else {
            return Err(Error::new(
                "§11.1: source operation is not a constructor".into(),
            ));
        };
        if let Some(Value::Str(g)) = m.get_mut("gate") {
            *g = match g.as_str() {
                "s" => "sdg",
                "sdg" => "s",
                "t" => "tdg",
                "tdg" => "t",
                g => g,
            }
            .to_string();
            if let Some(Value::Arr(angles)) = m.get_mut("params") {
                for angle in angles {
                    let Value::Str(t) = angle else {
                        return Err(Error::new("§11.1: angle encoding".into()));
                    };
                    let bits = u64::from_str_radix(
                        t.strip_prefix("0x")
                            .ok_or_else(|| Error::new("§11.1: angle encoding".into()))?,
                        16,
                    )
                    .map_err(|_| Error::new("§11.1: angle encoding".into()))?;
                    *t = format!("0x{:016x}", bits ^ (1 << 63));
                }
            }
        } else if m.contains_key("acquire") {
            let value = m.remove("acquire").expect("key checked");
            m.insert("relinquish".into(), value);
        } else if m.contains_key("relinquish") {
            let value = m.remove("relinquish").expect("key checked");
            m.insert("acquire".into(), value);
        } else if m.contains_key("under") {
            let value = m.remove("body").expect("body constructor");
            let Value::Arr(body) = value else {
                return Err(Error::new("§11.1: constructor body".into()));
            };
            m.insert("body".into(), array(source_adjoint(body, symbols)?));
        } else if m.contains_key("for") {
            let Value::Arr(body) = m.remove("body").expect("source point body") else {
                return Err(Error::new("§11.1: source point body".into()));
            };
            m.insert("body".into(), array(source_adjoint(body, symbols)?));
        } else if m.contains_key("source_cleanup") {
            for key in ["reverse", "recompute"] {
                let Value::Arr(body) = m.remove(key).expect("cleanup realisation body") else {
                    return Err(Error::new("§11 K81: cleanup body".into()));
                };
                m.insert(key.into(), array(source_adjoint(body, symbols)?));
            }
        } else if let Some(Value::Str(kind)) = m.get("invoke") {
            if matches!(kind.as_str(), "oracle_call" | "action_call") {
                if kind == "action_call" {
                    let alias = m
                        .get("args")
                        .and_then(Value::as_arr)
                        .and_then(|a| a.first())
                        .and_then(Value::as_str)
                        .ok_or_else(|| Error::new("§11.1: source call actual".into()))?;
                    let symbol = symbols
                        .iter_mut()
                        .find(|s| s.name == alias)
                        .ok_or_else(|| Error::new("§11.1: source call binding".into()))?;
                    symbol.adjoint = !symbol.adjoint;
                }
            } else if kind == "qinplace" {
                let Some(Value::Arr(args)) = m.get_mut("args") else {
                    return Err(Error::new("§11 K62: qinplace actuals".into()));
                };
                if args.len() != 6 {
                    return Err(Error::new("§11 K62: qinplace adapter arity".into()));
                }
                args.swap(3, 4);
            } else if kind == "qloop" {
                let Some(Value::Arr(args)) = m.get_mut("args") else {
                    return Err(Error::new("§11.1: loop body".into()));
                };
                let Value::Arr(body) = args.remove(1) else {
                    return Err(Error::new("§11.1: loop body".into()));
                };
                args.push(array(source_adjoint(body, symbols)?));
            } else {
                node = inverse(vec![node]);
            }
        } else if m.contains_key("inverse") {
            let Value::Arr(body) = m.remove("body").expect("inverse body") else {
                return Err(Error::new("§11.1: inverse body".into()));
            };
            out.extend(body);
            continue;
        } else {
            return Err(Error::new(
                "§11.1: unknown source operation in adjoint".into(),
            ));
        }
        out.push(node);
    }
    Ok(out)
}
pub(super) fn construct(
    object: &crate::Object,
    f: &crate::Function,
    values: &BTreeMap<String, Value>,
    actual_regions: &BTreeMap<String, Value>,
    tokens: &bennett_isa_conformance::ref_language::SourceTokenContext,
    adjoint: bool,
) -> Result<SourceBody> {
    let plan = object.source_cleanup_plan_with_tokens(f, &tokens.arguments)?;
    let hashes = object.identity()?.closure_hashes;
    let symbol = hashes[&f.name]
        .clone()
        .ok_or_else(|| Error::new("§11.1: source action is unlinked".into()))?;
    let mut locations = BTreeMap::new();
    fn visit(
        seq: &[crate::Instruction],
        block: &str,
        cursor: &mut usize,
        depth: usize,
        out: &mut BTreeMap<usize, (String, usize)>,
    ) {
        for i in seq {
            out.insert(i.line, (format!("{block}:{}", *cursor), depth));
            *cursor += 1;
            for body in &i.bodies {
                visit(
                    body,
                    block,
                    cursor,
                    depth + usize::from(i.op == "qloop"),
                    out,
                );
            }
        }
    }
    for block in &f.blocks {
        visit(&block.instructions, &block.name, &mut 0, 0, &mut locations);
    }
    let mut compiler = Compiler {
        object,
        values,
        tokens,
        declarations: Vec::new(),
        symbols: Vec::new(),
        counter: 0,
        hashes,
        symbol: symbol.clone(),
        points: BTreeMap::new(),
        locations,
        compiled: BTreeMap::new(),
    };
    let mut env = Env::default();
    for p in f.params.iter().flatten() {
        match p.ty {
            crate::Type::Wire(w) | crate::Type::Reg(w) => {
                env.wires
                    .insert(p.name.clone(), (p.name.clone(), w as usize));
            }
            crate::Type::Region(a, w) => {
                let origin = actual_regions
                    .get(&p.name)
                    .and_then(|r| r.get("origin"))
                    .cloned()
                    .ok_or_else(|| {
                        Error::new("§11.1: missing bound interface region origin".into())
                    })?;
                env.regions.insert(
                    p.name.clone(),
                    Region {
                        cells: p.name.clone(),
                        address: a as usize,
                        cell: w as usize,
                        origin,
                    },
                );
            }
            _ => {}
        }
    }
    let locals = crate::validation::region_declarations(f);
    for i in &locals {
        let a = &i.operands;
        env.regions.insert(
            a[0].clone(),
            Region {
                cells: a[0].clone(),
                address: crate::object::host_count(&a[1], "address width")? as usize,
                cell: crate::object::host_count(&a[2], "cell width")? as usize,
                origin: text(format!("local:{}", a[0])),
            },
        );
    }
    let mut body = Vec::new();
    for block in &f.blocks {
        body.extend(compiler.sequence(&block.instructions, &mut env)?);
    }
    if !env.predicates.is_empty() {
        return Err(Error::new("§11.1: unclosed source predicates".into()));
    }
    body = cleanup::apply(&mut compiler, &plan, body)?;
    if adjoint {
        body = source_adjoint(body, &mut compiler.symbols)?;
    }
    let local_count = locals.len();
    for i in locals.into_iter().rev() {
        let a = &i.operands;
        let r = &env.regions[&a[0]];
        let count = 1usize
            .checked_shl(
                r.address
                    .try_into()
                    .map_err(|_| crate::resource_error("§11.1", "region width exceeds host"))?,
            )
            .ok_or_else(|| crate::resource_error("§11.1", "region count exceeds host"))?;
        let width = count
            .checked_mul(r.cell)
            .ok_or_else(|| crate::resource_error("§11.1", "region extent overflow"))?;
        let image = if a.len() == 4 {
            object.data[a[3].trim_start_matches('@')]
                .iter()
                .map(|b| format!("{b:02x}"))
                .collect::<String>()
        } else {
            String::new()
        };
        body = vec![invoke(
            "qregion",
            [
                number(count)?,
                number(r.cell)?,
                text(image),
                array([template(vec![formal(&a[0], width)?], body)]),
                array([]),
            ],
        )];
    }
    if compiler.declarations.len().saturating_add(local_count)
        >= bennett_isa_conformance::ref_language::SOURCE_SCOPE_LIMIT
    {
        return Err(crate::resource_error(
            "§11.1",
            "source declaration scopes exceed the host expansion stack budget",
        ));
    }
    for (name, width, class, state) in compiler.declarations.into_iter().rev() {
        body = vec![obj([
            ("declare", text(name)),
            ("width", number(width)?),
            ("class", obj([("class", text(class))])),
            ("state", text(state)),
            ("body", array(body)),
        ])];
    }
    Ok(SourceBody {
        binding: None, // The linked factory supplies the complete invocation.
        body: array(body),
        symbols: compiler.symbols,
        symbol,
        oracle: false,
        points: compiler.points,
        rows: Vec::new(),
    })
}
mod cleanup;
mod qinplace;
````

## `reference-interpreter/tests/isa09_certificate.rs` (196 lines)

````rust
mod support;
use bennett_isa_ref::{json::Json, Object};
use std::collections::BTreeMap;
const SOURCE: &str =
    include_str!("../../conformance/fixtures/controlled-action-09/controlled.bisa");
fn fields(j: &mut Json) -> &mut BTreeMap<String, Json> {
    let Json::Object(m) = j else { panic!("object") };
    m
}
fn replace(text: &str, name: &str, value: Option<&Json>) -> String {
    let mut lines = text.lines();
    let mut out = Vec::new();
    while let Some(line) = lines.next() {
        if line == format!("section {name}") {
            lines.next().unwrap();
            if let Some(value) = value {
                out.push(line.to_string());
                out.push(value.canonical());
            }
        } else {
            out.push(line.to_string());
        }
    }
    {
        let mut text = out.join("\n");
        while text.contains("\n\n\n") {
            text = text.replace("\n\n\n", "\n\n");
        }
        text.trim_end_matches('\n').to_string() + "\n"
    }
}
fn certificate() -> Json {
    Object::parse(SOURCE)
        .unwrap()
        .section("certificate")
        .unwrap()
        .clone()
}
fn claim(c: &mut Json) -> &mut Json {
    let root = c
        .get("bindings")
        .unwrap()
        .get("closure_hash")
        .unwrap()
        .string()
        .unwrap()
        .to_string();
    let r = fields(c).get_mut("regions").unwrap();
    let region = fields(r).get_mut(&root).unwrap();
    let Json::Array(claims) = fields(region).get_mut("claims").unwrap() else {
        panic!("claims")
    };
    &mut claims[0]
}
#[test]
fn standalone_claims_require_invocation_even_in_scheduled_objects() {
    for structural in [false, true] {
        let mut c = certificate();
        let cl = claim(&mut c);
        if structural {
            *cl = support::json(
                r#"{"kind":"structural","rule":"adjoint_table","subclaims":[],"witness":{}}"#,
            );
        } else {
            fields(fields(cl).get_mut("subject").unwrap()).remove("schedule_hash");
            fields(cl).remove("invocation");
        }
        let result = Object::parse(&replace(SOURCE, "certificate", Some(&c)));
        assert!(
            result.is_err(),
            "standalone structural={structural} admitted without invocation"
        );
        assert!(result.unwrap_err().to_string().contains("K13"));
    }
}
#[test]
fn expected_oracle_requires_its_own_realised_schedule_binding() {
    let mut c = certificate();
    let cl = claim(&mut c);
    fields(cl).insert("expected".into(), Json::String("oracle".into()));
    fields(fields(cl).get_mut("subject").unwrap()).remove("schedule_hash");
    fields(cl).insert(
        "invocation".into(),
        support::json(r#"{"args":[],"budget":["0","0","0","0"]}"#),
    );
    let source = SOURCE.to_string();
    let result = Object::parse(&replace(&source, "certificate", Some(&c)));
    assert!(
        result.is_err(),
        "expected:oracle admitted without subject.schedule_hash"
    );
    assert!(result.unwrap_err().to_string().contains("schedule"));
}
#[test]
fn a_data_root_certificate_is_a_diagnostic_and_never_a_panic() {
    let mut c = certificate();
    let mut base = replace(SOURCE, "certificate", None);
    let mut symbols = Object::parse(&base)
        .unwrap()
        .section("symbols")
        .unwrap()
        .clone();
    let data_index = fields(&mut symbols).len().to_string();
    fields(&mut symbols).insert(data_index,support::json(r#"{"name":"img","kind":"data","signature":{"abi":"0.9","kind":"data","tier":"-","size":1},"interface_hash":"0000000000000000000000000000000000000000000000000000000000000000"}"#));
    base = replace(&base, "symbols", Some(&symbols));
    base = base.replace(
        "\nsection schedule\n",
        "\nsection data\nimg 00\n\nsection schedule\n",
    );
    let base = support::rehash(&base);
    let id = base.identity().unwrap();
    let b = fields(fields(&mut c).get_mut("bindings").unwrap());
    b.insert("object_hash".into(), Json::String(id.object_hash));
    b.insert(
        "closure_hash".into(),
        Json::String(id.closure_hashes["img"].clone().unwrap()),
    );
    let source = format!("{}\nsection certificate\n{}\n", base.text, c.canonical());
    let result = std::panic::catch_unwind(|| Object::parse(&source));
    assert!(result.is_ok(), "untrusted certificate data root panicked");
    assert!(result.unwrap().is_err());
}

// K13: a schedule subject denotes the realised operation for every relation.
#[test]
fn scheduled_table_and_program_claims_never_prove_reference_only_replay() {
    use bennett_isa_ref::ClaimVerdict;
    let source = include_str!("../../conformance/fixtures/accepted-k91-09/pair-distinct.bisa");
    let object = Object::parse(source).unwrap();
    let root = object.identity().unwrap().closure_hashes["pair"]
        .clone()
        .unwrap();
    for relation in ["table", "program", "oracle"] {
        let mut c = object.section("certificate").unwrap().clone();
        let schedule = c
            .get("bindings")
            .unwrap()
            .get("schedule_hash")
            .unwrap()
            .clone();
        let cl = claim(&mut c);
        fields(fields(cl).get_mut("subject").unwrap()).insert("schedule_hash".into(), schedule);
        match relation {
            "program" => {
                fields(cl).insert(
                    "expected".into(),
                    support::json(&format!(r#"{{"program":"{root}"}}"#)),
                );
            }
            "oracle" => {
                fields(cl).insert("expected".into(), Json::String("oracle".into()));
            }
            _ => {}
        }
        let o = Object::parse(&replace(source, "certificate", Some(&c))).unwrap();
        assert!(
            matches!(
                o.verify_claim(&root, 0).unwrap(),
                ClaimVerdict::Unverified(_)
            ),
            "{relation}"
        );
        let reports = o.verify_certificate().unwrap().claims;
        assert!(
            matches!(reports[0].verdict, ClaimVerdict::Unverified(_)),
            "{relation}"
        );
        assert!(reports[0].coverage.is_none());

        // A syntactically valid hash must resolve to this object's schedule.
        fields(fields(claim(&mut c)).get_mut("subject").unwrap())
            .insert("schedule_hash".into(), Json::String("ab".repeat(32)));
        let error = Object::parse(&replace(source, "certificate", Some(&c))).unwrap_err();
        assert!(error.to_string().contains("schedule"), "{error}");
    }
}

#[test]
fn claim_schedule_hash_requires_a_present_matching_schedule() {
    let source = include_str!("../../conformance/fixtures/accepted-k91-09/pair-distinct.bisa");
    let object = Object::parse(source).unwrap();
    let mut c = object.section("certificate").unwrap().clone();
    let hash = c
        .get("bindings")
        .unwrap()
        .get("schedule_hash")
        .unwrap()
        .clone();
    fields(fields(claim(&mut c)).get_mut("subject").unwrap()).insert("schedule_hash".into(), hash);
    let missing = replace(&replace(source, "schedule", None), "certificate", Some(&c));
    let error = Object::parse(&missing).unwrap_err();
    assert!(
        error.to_string().contains("claim schedule is absent"),
        "{error}"
    );
}
````

## `reference-interpreter/tests/isa09_claim_replay.rs` (479 lines)

````rust
mod support;
use bennett_isa_ref::{json::Json, sha256_hex, ClaimVerdict, Object};
use std::collections::BTreeMap;

const BASE: &str = include_str!("../../conformance/fixtures/accepted-k84-09/baseline.bisa");
const CONTROLLED: &str =
    include_str!("../../conformance/fixtures/controlled-action-09/controlled.bisa");

fn fields(value: &mut Json) -> &mut BTreeMap<String, Json> {
    let Json::Object(fields) = value else {
        panic!("object")
    };
    fields
}
fn changed(source: &str, mutate: impl FnOnce(&mut Json)) -> Object {
    Object::parse(&changed_text(source, mutate)).unwrap()
}
fn changed_text(source: &str, mutate: impl FnOnce(&mut Json)) -> String {
    let (base, certificate) = source.split_once("section certificate\n").unwrap();
    let mut certificate = Json::parse(certificate.trim()).unwrap();
    let root = certificate
        .get("bindings")
        .unwrap()
        .get("closure_hash")
        .unwrap()
        .string()
        .unwrap()
        .to_string();
    let region = fields(fields(&mut certificate).get_mut("regions").unwrap())
        .get_mut(&root)
        .unwrap();
    let Json::Array(claims) = fields(region).get_mut("claims").unwrap() else {
        panic!("claims")
    };
    mutate(&mut claims[0]);
    format!("{base}section certificate\n{}\n", certificate.canonical())
}
fn verify_root(object: &Object) -> bennett_isa_ref::Result<ClaimVerdict> {
    let closure = object
        .section("certificate")
        .unwrap()
        .get("bindings")
        .unwrap()
        .get("closure_hash")
        .unwrap()
        .string()
        .unwrap();
    object.verify_claim(closure, 0)
}

fn with_certificate(object: &Object, name: &str, mut claim: Json, slots: Json) -> Object {
    let mut certificate = Object::parse(BASE)
        .unwrap()
        .section("certificate")
        .unwrap()
        .clone();
    let identity = object.identity().unwrap();
    let closure = identity.closure_hashes[name].as_ref().unwrap();
    fields(fields(&mut claim).get_mut("subject").unwrap())
        .insert("closure_hash".into(), Json::String(closure.clone()));
    let bindings = fields(fields(&mut certificate).get_mut("bindings").unwrap());
    for (key, value) in [
        ("object_hash", &identity.object_hash),
        ("interface_hash", &identity.interface_hashes[name]),
        ("closure_hash", closure),
        ("reference_program_hash", closure),
    ] {
        bindings.insert(key.into(), Json::String(value.clone()));
    }
    bindings.insert(
        "invocation".into(),
        claim.get("invocation").unwrap().clone(),
    );
    let regions = fields(fields(&mut certificate).get_mut("regions").unwrap());
    let mut region = regions.values().next().unwrap().clone();
    fields(&mut region).insert(
        "signature".into(),
        object.functions[name].signature_for(object.isa_version),
    );
    fields(&mut region).insert(
        "kind".into(),
        Json::String(object.functions[name].kind.clone()),
    );
    fields(&mut region).insert("claims".into(), Json::Array(vec![claim]));
    fields(fields(&mut region).get_mut("frame").unwrap()).insert("slots".into(), slots);
    regions.clear();
    regions.insert(closure.clone(), region);
    fields(fields(&mut certificate).get_mut("composition").unwrap())
        .insert("multiplicities".into(), support::json("{}"));
    Object::parse(&format!(
        "{}\nsection certificate\n{}\n",
        object.text,
        certificate.canonical()
    ))
    .unwrap()
}

fn typed_oracle(argument: &str, steps: u64) -> Object {
    let source = support::object(&[("sum",
        r#"{"abi":"0.8","args":["i2"],"fault":4,"in":[2],"kind":"oracle","mem":[{"A":1,"W":8,"role":"in"}],"tgt":2,"tier":"q"}"#,
        "oracle @sum (x:wire[2] in) (t:wire[2]) (f:wire[4]) (db:region[1,8] in) (a:i2)\nregs { r:reg[2] }\n^entry():\nr = lift.add x a\nlift.retval r")], "{}",
        "\nsection layout\n{\"A_tab\":1,\"H\":2,\"S_cells\":0,\"globals\":{},\"heap_base\":3,\"heap_limit_max\":0,\"interface_regions\":{\"sum\":{\"db\":{\"base\":1}}},\"null_size\":1,\"ptr_width\":2}\n")
        .replace("=0.8", "=0.9").replace("\"0.8\"", "\"0.9\"").replace("ptr_width=32", "ptr_width=2");
    let object = support::rehash(&source);
    let mut claim = support::json(
        r#"{
        "kind":"exhaustive","subject":{"closure_hash":"","variant":"forward","inherited_controls":0},
        "invocation":{"args":["2"],"budget":["2","0","0","0"]},
        "domain":{"bundles":[{"name":"x","width":2,"lo":1,"hi":1},{"name":"t","width":2,"lo":2,"hi":2},{"name":"f","width":4,"lo":3,"hi":3}],
          "borrowed":[{"name":"dirty","width":1,"lo":1,"hi":1}],
          "regions":[{"name":"db","cells":[{"index":0,"lo":2,"hi":2},{"index":1,"lo":1,"hi":1}]}]},
        "expected":{"table":[{"before":{"bundles":["1","2","3"],"borrowed":["1"],"regions":[["2","1"]]},
                               "after":{"bundles":["1","1","3"],"borrowed":["1"],"regions":[["2","1"]]}}]}}
    "#,
    );
    fields(fields(&mut claim).get_mut("invocation").unwrap()).insert(
        "args".into(),
        Json::Array(vec![Json::String(argument.into())]),
    );
    fields(fields(&mut claim).get_mut("invocation").unwrap()).insert(
        "budget".into(),
        support::json(&format!("[\"{steps}\",\"0\",\"0\",\"0\"]")),
    );
    with_certificate(
        &object,
        "sum",
        claim,
        support::json(
            r#"[
        {"id":"in:0","role":"in","width":2,"class":"fast"},
        {"id":"tgt:0","role":"tgt","width":2,"class":"fast"},
        {"id":"fault:0","role":"fault","width":4,"class":"fast"},
        {"id":"mem:0","role":"mem_in","width":16,"class":"fast"}]"#,
        ),
    )
}

#[test]
fn standalone_oracle_binds_its_own_argument_budget_and_complete_interface() {
    let object = typed_oracle("2", 2);
    assert_eq!(
        verify_root(&object).unwrap(),
        ClaimVerdict::Evidence { elements: 1 }
    );
    for object in [typed_oracle("1", 2), typed_oracle("2", 1)] {
        let error = verify_root(&object).unwrap_err().to_string();
        assert!(error.contains("full tuple mismatch"), "{error}");
    }
    for field in ["bundles", "borrowed", "regions"] {
        let object = changed(&typed_oracle("2", 2).text, |claim| {
            let table = fields(fields(claim).get_mut("expected").unwrap())
                .get_mut("table")
                .unwrap();
            let Json::Array(rows) = table else {
                panic!("rows")
            };
            let after = fields(&mut rows[0]).get_mut("after").unwrap();
            let Json::Array(values) = fields(after).get_mut(field).unwrap() else {
                panic!("values")
            };
            if field == "regions" {
                let Json::Array(cells) = &mut values[0] else {
                    panic!("cells")
                };
                cells[0] = Json::String("3".into());
            } else {
                values[0] = Json::String("0".into());
            }
        });
        assert!(verify_root(&object).is_err(), "ignored changed {field}");
    }
}
#[test]
fn published_full_tuple_tables_prove_only_the_bound_reference_relation() {
    for source in [BASE, CONTROLLED] {
        let object = Object::parse(source).unwrap();
        let certificate = object.section("certificate").unwrap();
        let root = certificate
            .get("bindings")
            .unwrap()
            .get("closure_hash")
            .unwrap()
            .string()
            .unwrap();
        let claim = &certificate
            .get("regions")
            .unwrap()
            .get(root)
            .unwrap()
            .get("claims")
            .unwrap()
            .array()
            .unwrap()[0];
        if claim
            .get("subject")
            .unwrap()
            .object()
            .unwrap()
            .contains_key("schedule_hash")
        {
            assert!(matches!(
                verify_root(&object).unwrap(),
                ClaimVerdict::Unverified(_)
            ));
            let root_report = |o: &Object| {
                o.verify_certificate()
                    .unwrap()
                    .claims
                    .into_iter()
                    .find(|r| r.closure_hash == root && r.index == 0)
                    .unwrap()
            };
            assert!(matches!(
                root_report(&object).verdict,
                ClaimVerdict::Unverified(_)
            ));
            // Keep the published table as a full reference-semantic oracle,
            // without misrepresenting it as execution of its realisation.
            let invocation = certificate
                .get("bindings")
                .unwrap()
                .get("invocation")
                .unwrap()
                .clone();
            let reference = changed(source, |claim| {
                fields(fields(claim).get_mut("subject").unwrap()).remove("schedule_hash");
                fields(claim).insert("invocation".into(), invocation);
            });
            assert_eq!(verify_root(&reference).unwrap(), ClaimVerdict::Proof);
            assert_eq!(root_report(&reference).verdict, ClaimVerdict::Proof);
            assert_eq!(
                reference.identity().unwrap().object_hash,
                object.identity().unwrap().object_hash
            );
        } else {
            assert_eq!(verify_root(&object).unwrap(), ClaimVerdict::Proof);
        }
    }
}
#[test]
fn a_wrong_before_or_after_tuple_rejects() {
    for side in ["before", "after"] {
        let object = changed(BASE, |claim| {
            let table = fields(fields(claim).get_mut("expected").unwrap())
                .get_mut("table")
                .unwrap();
            let Json::Array(rows) = table else {
                panic!("rows")
            };
            let tuple = fields(&mut rows[0]).get_mut(side).unwrap();
            fields(tuple).insert("bundles".into(), support::json("[\"1\"]"));
            if side == "after" {
                fields(tuple).insert("bundles".into(), support::json("[\"0\"]"));
            } else {
                let tuple = fields(&mut rows[1]).get_mut(side).unwrap();
                fields(tuple).insert("bundles".into(), support::json("[\"0\"]"));
            }
        });
        let error = verify_root(&object).unwrap_err().to_string();
        assert!(error.contains("K13"), "{error}");
    }
}
#[test]
fn singleton_sampling_counts_distinct_elements_and_uses_one_table_row() {
    let object = changed(BASE, |claim| {
        fields(claim).insert("kind".into(), Json::String("sampled".into()));
        fields(claim).insert(
            "sampler".into(),
            support::json(r#"{"algorithm":"xoshiro256**","seed":["1","0","0","0"],"count":4}"#),
        );
        let domain = fields(claim).get_mut("domain").unwrap();
        fields(domain).insert(
            "bundles".into(),
            support::json(r#"[{"name":"t","width":1,"lo":0,"hi":0}]"#),
        );
        let table = fields(fields(claim).get_mut("expected").unwrap())
            .get_mut("table")
            .unwrap();
        let Json::Array(rows) = table else {
            panic!("rows")
        };
        rows.truncate(1);
    });
    assert_eq!(
        verify_root(&object).unwrap(),
        ClaimVerdict::Evidence { elements: 1 }
    );
}

#[test]
fn inherited_control_positions_have_label_only_names_and_complete_tuples() {
    let bare = Object::parse(
        &(BASE
            .split_once("section certificate\n")
            .unwrap()
            .0
            .trim_end()
            .to_string()
            + "\n"),
    )
    .unwrap();
    let mut claim = Object::parse(BASE)
        .unwrap()
        .section("certificate")
        .unwrap()
        .get("regions")
        .unwrap()
        .object()
        .unwrap()
        .values()
        .next()
        .unwrap()
        .get("claims")
        .unwrap()
        .array()
        .unwrap()[0]
        .clone();
    fields(fields(&mut claim).get_mut("subject").unwrap())
        .insert("inherited_controls".into(), Json::Number("1".into()));
    fields(fields(&mut claim).get_mut("domain").unwrap()).insert(
        "bundles".into(),
        support::json(
            r#"[{"name":"t","width":1,"lo":0,"hi":1},{"name":"t","width":1,"lo":0,"hi":1}]"#,
        ),
    );
    let rows = (0..2).flat_map(|c| (0..2).map(move |t| {
        support::json(&format!(r#"{{"before":{{"bundles":["{c}","{t}"],"borrowed":[],"regions":[]}},"after":{{"bundles":["{c}","{}"],"borrowed":[],"regions":[]}}}}"#,t^c))
    })).collect();
    fields(fields(&mut claim).get_mut("expected").unwrap())
        .insert("table".into(), Json::Array(rows));
    let object = with_certificate(
        &bare,
        "flip",
        claim,
        support::json(r#"[{"id":"mut:0","role":"mut","width":1,"class":"fast"}]"#),
    );
    assert_eq!(verify_root(&object).unwrap(), ClaimVerdict::Proof);
}

#[test]
fn exact_global_phase_is_part_of_a_permutation_table_assertion() {
    let source = support::object(&[("phase",
        r#"{"abi":"0.8","args":[],"bounds":[],"in":[],"kind":"action","mem":[],"mut":[1],"tier":"q"}"#,
        "action @phase (t:wire mut) () () () ()\n^entry():\ns t\ns t")],"{}","")
        .replace("=0.8","=0.9").replace("\"0.8\"","\"0.9\"");
    let bare = support::rehash(&source);
    let claim = support::json(
        r#"{"kind":"exhaustive","subject":{"closure_hash":"","variant":"forward","inherited_controls":0},"invocation":{"args":[],"budget":["0","0","0","0"]},"domain":{"bundles":[{"name":"t","width":1,"lo":0,"hi":1}],"borrowed":[],"regions":[]},"expected":{"table":[{"before":{"bundles":["0"],"borrowed":[],"regions":[]},"after":{"bundles":["0"],"borrowed":[],"regions":[]}},{"before":{"bundles":["1"],"borrowed":[],"regions":[]},"after":{"bundles":["1"],"borrowed":[],"regions":[]}}]}}"#,
    );
    let object = with_certificate(
        &bare,
        "phase",
        claim,
        support::json(r#"[{"id":"mut:0","role":"mut","width":1,"class":"fast"}]"#),
    );
    let error = verify_root(&object).unwrap_err().to_string();
    assert!(error.contains("exact +1 basis phase"), "{error}");
}

fn fixed_image_oracle() -> Object {
    changed(&typed_oracle("2", 2).text, |claim| {
        let domain = fields(claim).get_mut("domain").unwrap();
        fields(domain).insert(
            "bundles".into(),
            support::json(
                r#"[
            {"name":"x","width":2,"lo":0,"hi":3},
            {"name":"t","width":2,"lo":0,"hi":3},
            {"name":"f","width":4,"lo":0,"hi":15}]"#,
            ),
        );
        fields(domain).insert(
            "borrowed".into(),
            support::json(r#"[{"name":"dirty","width":1,"lo":0,"hi":1}]"#),
        );
        fields(domain).insert("regions".into(), support::json("[]"));
        fields(domain).insert(
            "fixed_regions".into(),
            support::json(&format!(
                r#"[{{"name":"db","A":1,"W":8,"image":"0201","sha256":"{}"}}]"#,
                sha256_hex(&[2, 1])
            )),
        );
        let mut rows = Vec::new();
        for x in 0..4 {
            for t in 0..4 {
                for f in 0..16 {
                    for b in 0..2 {
                        rows.push(support::json(&format!(r#"{{
                "before":{{"bundles":["{x}","{t}","{f}"],"borrowed":["{b}"],"regions":[["2","1"]]}},
                "after":{{"bundles":["{x}","{}","{f}"],"borrowed":["{b}"],"regions":[["2","1"]]}}}}"#, t^((x+2)&3))));
                    }
                }
            }
        }
        fields(fields(claim).get_mut("expected").unwrap())
            .insert("table".into(), Json::Array(rows));
    })
}

#[test]
fn fixed_image_metadata_is_admitted_without_inspecting_quantum_state() {
    let object = fixed_image_oracle();
    object.check_hashes().unwrap();
    assert_eq!(
        verify_root(&object).unwrap(),
        ClaimVerdict::ProofRelativeToImage
    );
    let report = object.verify_certificate().unwrap().claims.remove(0);
    let coverage = report.coverage.unwrap();
    assert_eq!(
        (
            coverage.elements,
            coverage.full_domain_elements.as_str(),
            coverage.covered_fraction.as_str()
        ),
        (512, "33554432", "1/65536")
    );
    assert_eq!(coverage.fixed_regions.len(), 1);
    assert_eq!(coverage.fixed_regions[0].sha256, sha256_hex(&[2, 1]));
    assert_eq!(report.context_key, support::json("[]"));
    let request = changed(&object.text, |claim| {
        fields(claim).insert("label".into(), Json::String("proof".into()));
    });
    assert!(verify_root(&request)
        .unwrap_err()
        .to_string()
        .contains("requested proof"));
}

#[test]
fn fixed_image_stale_hash_wrong_dimensions_and_duplicate_regions_reject() {
    let object = fixed_image_oracle();
    for mutation in ["hash", "width", "duplicate", "also-ranged", "uppercase"] {
        let text = changed_text(&object.text, |claim| {
            let domain = fields(claim).get_mut("domain").unwrap();
            if mutation == "also-ranged" {
                fields(domain).insert(
                    "regions".into(),
                    support::json(r#"[{"name":"db","cells":"all"}]"#),
                );
                return;
            }
            let Json::Array(images) = fields(domain).get_mut("fixed_regions").unwrap() else {
                panic!("images")
            };
            match mutation {
                "hash" => {
                    fields(&mut images[0]).insert("sha256".into(), Json::String("0".repeat(64)));
                }
                "width" => {
                    fields(&mut images[0]).insert("W".into(), Json::Number("7".into()));
                }
                "uppercase" => {
                    fields(&mut images[0]).insert("image".into(), Json::String("AB01".into()));
                }
                "duplicate" => images.push(images[0].clone()),
                _ => unreachable!(),
            }
        });
        let error = Object::parse(&text).unwrap_err().to_string();
        assert!(error.contains("K85"), "{mutation}: {error}");
    }
}

#[test]
fn sampled_singleton_report_has_exact_distinct_coverage() {
    let object = changed(&typed_oracle("2", 2).text, |claim| {
        fields(claim).insert("kind".into(), Json::String("sampled".into()));
        fields(claim).insert(
            "sampler".into(),
            support::json(r#"{"algorithm":"xoshiro256**","seed":["1","0","0","0"],"count":4}"#),
        );
    });
    let report = object.verify_certificate().unwrap().claims.remove(0);
    assert_eq!(report.verdict, ClaimVerdict::Evidence { elements: 1 });
    let coverage = report.coverage.unwrap();
    assert_eq!(coverage.covered_fraction, "1/33554432");
}
````

## `reference-interpreter/tests/isa09_forwarding.rs` (456 lines)

````rust
mod support;
use bennett_isa_ref::{Argument, Budget, Object, OracleInput, OracleMachine};
use std::collections::BTreeMap;
fn object() -> Object {
    let spec = include_str!("../../spec/Bennett-ISA-Spec-0.9.md");
    let body = spec
        .split_once("**Example 10**")
        .unwrap()
        .1
        .split_once("```\n")
        .unwrap()
        .1
        .split_once("\n```")
        .unwrap()
        .0;
    let o = Object::parse(&format!("{body}\n")).unwrap();
    o.check_hashes().unwrap();
    o
}
fn budget(steps: u64, stack: u128, depth: u128) -> Budget {
    Budget {
        steps,
        heap: 0,
        stack,
        depth,
    }
}
fn input(x: u128, a: u128, byte: u8, nested: u64) -> OracleInput {
    OracleInput {
        ins: vec![x],
        args: vec![Argument::Token(Budget::steps(nested)), Argument::Bits(a)],
        regions: BTreeMap::from([("db".into(), vec![byte])]),
    }
}
#[test]
fn published_example10_forwards_every_input_argument_and_cell_without_extra_charge() {
    let o = object();
    for x in 0..4 {
        for a in 0..4 {
            for d in 0..=255 {
                let input = input(x, a, d, 6);
                let want = ((x + a + u128::from(d & 3)) & 3) ^ 1;
                let out = o
                    .run_oracle_with_token_aliases("through", &input, budget(8, 8, 1), &[0, 1])
                    .unwrap();
                assert_eq!((out.payload, out.code), (want, 0), "x={x} a={a} d={d}");
                let mut machine = OracleMachine::new_with_token_aliases(
                    &o,
                    "through",
                    &input,
                    budget(8, 8, 1),
                    &[0, 1],
                )
                .unwrap();
                let entry = machine.snapshot();
                for _ in 0..8 {
                    machine.forward_step().unwrap();
                }
                assert_eq!(machine.commit(2, 13).unwrap(), (want ^ 2, 13));
                for _ in 0..8 {
                    machine.inverse_step().unwrap();
                }
                assert_eq!(machine.snapshot(), entry);
            }
        }
    }
}
#[test]
fn forwarded_nested_faults_and_outer_boundaries_reverse_the_complete_prefix() {
    let o = object();
    for (outer, nested, code) in [
        (budget(7, 8, 1), 6, 1),
        (budget(8, 7, 1), 6, 3),
        (budget(8, 8, 0), 6, 3),
        (budget(5, 8, 1), 5, 9),
    ] {
        let input = input(3, 2, 255, nested);
        let out = o
            .run_oracle_with_token_aliases("through", &input, outer, &[0, 1])
            .unwrap();
        assert_eq!((out.payload, out.code), (0, code));
        let mut machine =
            OracleMachine::new_with_token_aliases(&o, "through", &input, outer, &[0, 1]).unwrap();
        let entry = machine.snapshot();
        for _ in 0..outer.steps {
            machine.forward_step().unwrap();
        }
        assert_eq!(machine.commit(3, 10).unwrap(), (3, 10 ^ code));
        for _ in 0..outer.steps {
            machine.inverse_step().unwrap();
        }
        assert_eq!(machine.snapshot(), entry);
    }
}

#[test]
fn source_constructor_binds_lproc_tokens_values_and_region_cells_per_instance() {
    use bennett_isa_conformance::{json, ref_catalog::Machine, ref_language::permutation};
    use bennett_isa_ref::ref_library::OracleInvocation;
    // Keep the published 32-bit example exhaustive in the literal tests.
    // A compact source circuit separately checks each fixed-binding channel.
    let o = compact_source_object();
    let args=json::parse(r#"["x","t","f",{"address":0,"cell":8,"role":"in","origin":"interface:db","cells":"db"},["2","0","0","0"],"1"]"#).unwrap();
    let context = json::parse(r#"{"token":["6","0","7","1"]}"#).unwrap();
    let call = OracleInvocation::capture_with_token_aliases(
        &o,
        "through",
        Some(&context),
        budget(6, 7, 1),
        args.as_arr().unwrap(),
        &[0, 1],
    )
    .unwrap();
    let leaves = call
        .expand_source_with_leaf_limit(
            &o.bound_ref_library().unwrap(),
            &[("x", 1), ("t", 1), ("f", 4), ("db", 8)],
            2_000_000,
        )
        .unwrap();
    eprintln!(
        "compact forwarded source expansion: {} leaves",
        leaves.len()
    );
    let hash = o.identity().unwrap().closure_hashes["worker"]
        .clone()
        .unwrap();
    assert!(leaves.iter().any(|l| l
        .source
        .as_ref()
        .is_some_and(|s| s.terminal.symbol == hash && s.terminal.instance == [0, 1, 0])));
    assert!(leaves.iter().any(
        |l| l.source.as_ref().is_some_and(|s| s
            .path
            .iter()
            .any(|e| e.point.symbol == hash && e.point.instance == [0, 1, 0]))
    ));
    for leaf in &leaves {
        let source = leaf.source.as_ref().unwrap();
        let root = source.invocations[0].tokens.as_ref().unwrap();
        if let Some(child) = source.invocations.get(1) {
            assert_eq!(
                child.tokens.as_ref().unwrap().primary,
                root.arguments.values().next().copied(),
                "lifted fixed binding retains the root token identity"
            );
            assert_eq!(child.binding.as_ref().unwrap().token_aliases, [0]);
        }
    }
    let m = Machine::compile(
        &permutation(&leaves).unwrap(),
        &[("x", 1), ("t", 1), ("f", 4), ("db", 8)],
    )
    .unwrap();
    for x in 0..2 {
        for d in [0u8, 1, 127, 128, 255] {
            let mut state = m.state();
            m.set(&mut state, "x", x);
            m.set(&mut state, "t", 1);
            m.set(&mut state, "f", 13);
            m.set(&mut state, "db", d as u64);
            let entry = state.clone();
            m.run(&mut state, true, false).unwrap();
            assert_eq!(m.get(&state, "x"), x);
            assert_eq!(m.get(&state, "db"), d as u64);
            assert_eq!(m.get(&state, "t"), x);
            assert_eq!(m.get(&state, "f"), 13);
            m.run(&mut state, true, true).unwrap();
            assert_eq!(state, entry);
        }
    }
}

fn compact_source_object() -> Object {
    let root = r#"{"abi":"0.9","args":["token","i1"],"fault":4,"in":[1],"kind":"oracle","mem":[{"A":0,"W":8,"role":"in"}],"tgt":1,"tier":"q"}"#;
    let worker = r#"{"abi":"0.9","args":["i1"],"kind":"lproc","mem":[{"A":0,"W":8,"role":"in"}],"params":[1],"result":1,"tier":"q","tokens":["token"]}"#;
    let leaf = r#"{"abi":"0.9","args":["i1"],"fault":4,"in":[1],"kind":"oracle","mem":[{"A":0,"W":8,"role":"in"}],"tgt":1,"tier":"q"}"#;
    support::rehash(&support::object(&[("through",root,"oracle @through (x:wire in) (t:wire) (f:wire[4]) (db:region[0,8] in) (tk:token, a:i1)\nregs { r:reg[1] }\n^entry():\nr = lift.call @worker (x) (tk) (a) (db)\nlift.retval r"),("worker",worker,"lproc @worker (x:reg[1]) (r:reg[1]) (tk:token) (a:i1) (cell:region[0,8] in)\nregs { fr:reg[4], bit:reg[1] }\n^entry():\nlift.oracle_call @leaf tk (x) r fr (cell) (a)\nbit = lift.trunc.i1 fr\nr = lift.xor r bit\nlift.ret r"),("leaf",leaf,"oracle @leaf (x:wire in) (t:wire) (f:wire[4]) (db:region[0,8] in) (a:i1)\nregs { r:reg[1] }\n^entry():\nr = lift.xor x a\nlift.retval r")],"{}","\nsection layout\n{\"A_tab\":1,\"H\":2,\"S_cells\":3,\"globals\":{},\"heap_base\":3,\"heap_limit_max\":0,\"interface_regions\":{\"leaf\":{\"db\":{\"base\":2}},\"through\":{\"db\":{\"base\":1}}},\"null_size\":1,\"ptr_width\":3}\n").replace("=0.8","=0.9").replace("ptr_width=32","ptr_width=3"))
}

fn source_object(ptr: usize) -> Object {
    let published = object();
    let layout = support::json(&format!(
        r#"{{"A_tab":1,"H":2,"S_cells":3,"globals":{{}},"heap_base":3,"heap_limit_max":1,"interface_regions":{{"plus_db":{{"db":{{"base":2}}}},"through":{{"db":{{"base":1}}}}}},"null_size":1,"ptr_width":{ptr}}}"#
    ));
    support::rehash(
        &published
            .text
            .replace(
                &published.section("layout").unwrap().canonical(),
                &layout.canonical(),
            )
            .replace("ptr_width=32", &format!("ptr_width={ptr}"))
            .replace("base:reg[32]", &format!("base:reg[{ptr}]")),
    )
}

#[test]
fn source_forwarding_bounded_materialisation_reports_host_capacity() {
    source_forwarding_materialisation_limit(3, Some(1_024));
}

#[test]
#[ignore = "slow-source-forwarding: million-leaf capacity witness; run only under an 8 GiB memory cap"]
fn source_forwarding_large_materialisation_reports_host_capacity_before_exhausting_memory() {
    source_forwarding_materialisation_limit(32, None);
}

fn source_forwarding_materialisation_limit(ptr: usize, leaf_limit: Option<usize>) {
    use bennett_isa_conformance::json;
    use bennett_isa_ref::ref_library::OracleInvocation;
    let o = source_object(ptr);
    let args=json::parse(r#"["x","t","f",{"address":0,"cell":8,"role":"in","origin":"interface:db","cells":"db"},["6","0","0","0"],"2"]"#).unwrap();
    let context = json::parse(r#"{"token":["8","0","8","1"]}"#).unwrap();
    let call = OracleInvocation::capture_with_token_aliases(
        &o,
        "through",
        Some(&context),
        budget(8, 8, 1),
        args.as_arr().unwrap(),
        &[0, 1],
    )
    .unwrap();
    let library = o.bound_ref_library().unwrap();
    let bundles = &[("x", 2), ("t", 2), ("f", 4), ("db", 8)];
    let error = match leaf_limit {
        Some(limit) => call.expand_source_with_leaf_limit(&library, bundles, limit),
        None => call.expand_source(&library, bundles),
    }
    .unwrap_err();
    assert_eq!(error.kind(), bennett_isa_ref::ErrorKind::HostResource);
    assert!(error.to_string().contains("materialised leaf budget"));
}

fn dual_instance_object() -> Object {
    let root = r#"{"abi":"0.9","args":["token","token"],"fault":4,"in":[1],"kind":"oracle","mem":[],"tgt":1,"tier":"q"}"#;
    let worker = r#"{"abi":"0.9","args":[],"kind":"lproc","mem":[],"params":[1],"result":1,"tier":"q","tokens":["token"]}"#;
    let id =
        r#"{"abi":"0.9","args":[],"fault":4,"in":[1],"kind":"oracle","mem":[],"tgt":1,"tier":"q"}"#;
    support::rehash(&support::object(&[("o",root,"oracle @o (x:wire in) (t:wire) (f:wire[4]) () (left:token, right:token)\nregs { r:reg[1] }\n^entry():\nqbranch x ^left ^right\n^left():\nr = lift.call @w (x) (left) () ()\nqjump ^done\n^right():\nr = lift.call @w (x) (right) () ()\nqjump ^done\n^done():\nlift.retval r"),("w",worker,"lproc @w (x:reg[1]) (r:reg[1]) (tk:token) () ()\nregs { fr:reg[4], bit:reg[1], zero:reg[4], bad:reg[1] }\n^entry():\nlift.oracle_call @id tk (x) r fr () ()\nbit = lift.trunc.i1 fr\nlift.oracle_uncall @id tk (x) r fr () ()\nzero = lift.const.i4 0\nbad = lift.icmp.ne fr zero\nlift.faultif bad 9\nlift.ret bit"),("id",id,"oracle @id (x:wire in) (t:wire) (f:wire[4]) () ()\n^entry():\nlift.retval x")],"{}","\nsection layout\n{\"A_tab\":1,\"H\":4,\"S_cells\":4,\"globals\":{},\"heap_base\":1,\"heap_limit_max\":0,\"interface_regions\":{},\"null_size\":1,\"ptr_width\":32}\n").replace("=0.8","=0.9"))
}
#[test]
fn coherent_paths_keep_two_lproc_instances_even_when_entry_token_values_are_equal() {
    let o = dual_instance_object();
    let b = budget(11, 9, 1);
    let widths = bennett_isa_ref::DerivedWidths::derive(&o, "o", b).unwrap();
    assert_eq!((widths.p, widths.did), (5, 4));
    for (left, right) in [(0, 1), (1, 1)] {
        for x in 0..2 {
            let input = OracleInput {
                ins: vec![x],
                args: vec![
                    Argument::Token(Budget::steps(left)),
                    Argument::Token(Budget::steps(right)),
                ],
                ..Default::default()
            };
            let expected = if x == 1 {
                u128::from(left == 0)
            } else {
                u128::from(right == 0)
            };
            let out = o
                .run_oracle_with_token_aliases("o", &input, b, &[0, 1, 2])
                .unwrap();
            assert_eq!((out.payload, out.code), (expected, 0));
            let mut machine =
                OracleMachine::new_with_token_aliases(&o, "o", &input, b, &[0, 1, 2]).unwrap();
            let entry = machine.snapshot();
            for _ in 0..b.steps {
                machine.forward_step().unwrap();
            }
            assert_eq!(machine.commit(1, 13).unwrap(), (1 ^ expected, 13));
            for _ in 0..b.steps {
                machine.inverse_step().unwrap();
            }
            assert_eq!(machine.snapshot(), entry);
        }
    }
}
#[test]
fn recursive_forwarding_closes_over_two_permuted_binding_keys() {
    let root = r#"{"abi":"0.9","args":["token","token"],"fault":4,"in":[1],"kind":"oracle","mem":[],"tgt":1,"tier":"q"}"#;
    let worker = r#"{"abi":"0.9","args":[],"kind":"lproc","mem":[],"params":[1],"result":1,"tier":"q","tokens":["token","token"]}"#;
    let id =
        r#"{"abi":"0.9","args":[],"fault":4,"in":[1],"kind":"oracle","mem":[],"tgt":1,"tier":"q"}"#;
    let source=support::object(&[("o",root,"oracle @o (x:wire in) (t:wire) (f:wire[4]) () (left:token, right:token)\nregs { r:reg[1] }\n^entry():\nr = lift.call @w (x) (left, right) () ()\nlift.retval r"),("w",worker,"lproc @w (x:reg[1]) (r:reg[1]) (tk:token, other:token) () ()\nregs { zero:reg[1], z:reg[1], n:reg[1], fr:reg[4], bit:reg[1] }\n^entry():\nzero = lift.const.i1 0\nz = lift.icmp.eq x zero\nqbranch z ^base ^recurse\n^recurse():\nn = lift.const.i1 0\nr = lift.call @w (n) (other, tk) () ()\nlift.ret r\n^base():\nlift.oracle_call @id tk (x) r fr () ()\nbit = lift.trunc.i1 fr\nlift.oracle_uncall @id tk (x) r fr () ()\nlift.ret bit"),("id",id,"oracle @id (x:wire in) (t:wire) (f:wire[4]) () ()\n^entry():\nlift.retval x")],"{}","\nsection layout\n{\"A_tab\":1,\"H\":4,\"S_cells\":5,\"globals\":{},\"heap_base\":1,\"heap_limit_max\":0,\"interface_regions\":{},\"null_size\":1,\"ptr_width\":32}\n").replace("=0.8","=0.9");
    let o = support::rehash(&source);
    let b = budget(15, 20, 2);
    let widths = bennett_isa_ref::DerivedWidths::derive(&o, "o", b).unwrap();
    assert_eq!((widths.p, widths.did), (5, 4));
    for x in 0..2 {
        let input = OracleInput {
            ins: vec![x],
            args: vec![
                Argument::Token(Budget::steps(0)),
                Argument::Token(Budget::steps(1)),
            ],
            ..Default::default()
        };
        let expected = x ^ 1;
        let out = o
            .run_oracle_with_token_aliases("o", &input, b, &[0, 1, 2])
            .unwrap();
        assert_eq!((out.payload, out.code), (expected, 0));
        let mut machine =
            OracleMachine::new_with_token_aliases(&o, "o", &input, b, &[0, 1, 2]).unwrap();
        let entry = machine.snapshot();
        for _ in 0..b.steps {
            machine.forward_step().unwrap();
        }
        assert_eq!(machine.commit(1, 7).unwrap(), (1 ^ expected, 7));
        for _ in 0..b.steps {
            machine.inverse_step().unwrap();
        }
        assert_eq!(machine.snapshot(), entry);
    }
}

#[test]
fn source_expansion_host_stack_limit_is_explicit_and_not_an_isa_fault() {
    use bennett_isa_conformance::json;
    use bennett_isa_ref::ref_library::OracleInvocation;
    let o = object();
    let args=json::parse(r#"["x","t","f",{"address":0,"cell":8,"role":"in","origin":"interface:db","cells":"db"},["6","0","0","0"],"2"]"#).unwrap();
    let context = json::parse(r#"{"token":["600","0","8","1"]}"#).unwrap();
    let call = OracleInvocation::capture_with_token_aliases(
        &o,
        "through",
        Some(&context),
        budget(600, 8, 1),
        args.as_arr().unwrap(),
        &[0, 1],
    )
    .unwrap();
    let error = call
        .expand_source(
            &o.bound_ref_library().unwrap(),
            &[("x", 2), ("t", 2), ("f", 4), ("db", 8)],
        )
        .unwrap_err();
    assert_eq!(error.kind(), bennett_isa_ref::ErrorKind::HostResource);
    assert!(error.to_string().contains("stack budget"));
}

#[test]
fn lproc_address_rows_resolve_the_forwarded_region_and_do_not_hash_it_as_a_symbol() {
    let root = r#"{"abi":"0.9","args":[],"fault":4,"in":[],"kind":"oracle","mem":[{"A":0,"W":8,"role":"in"}],"tgt":1,"tier":"q"}"#;
    let proc = r#"{"abi":"0.9","args":[],"kind":"lproc","mem":[{"A":0,"W":8,"role":"in"}],"params":[],"result":1,"tier":"q","tokens":[]}"#;
    let source=support::object(&[("o",root,"oracle @o () (t:wire) (f:wire[4]) (db:region[0,8] in) ()\nregs { r:reg[1] }\n^entry():\nr = lift.call @w () () () (db)\nlift.retval r"),("w",proc,"lproc @w () (r:reg[1]) () () (cell:region[0,8] in)\nregs { base:reg[32], byte:reg[8] }\n^entry():\nbase = lift.addr @cell\nbyte = lift.load.i8 base\nr = lift.trunc.i1 byte\nlift.ret r")],"{}","\nsection layout\n{\"A_tab\":1,\"H\":2,\"S_cells\":3,\"globals\":{},\"heap_base\":2,\"heap_limit_max\":0,\"interface_regions\":{\"o\":{\"db\":{\"base\":1}}},\"null_size\":1,\"ptr_width\":32}\n").replace("=0.8","=0.9");
    let o = support::rehash(&source);
    o.check_hashes().unwrap();
    for d in 0..=255u8 {
        let input = OracleInput {
            regions: BTreeMap::from([("db".into(), vec![d])]),
            ..Default::default()
        };
        let b = budget(6, 6, 1);
        let result = o.run_oracle("o", &input, b).unwrap();
        assert_eq!((result.payload, result.code), (u128::from(d & 1), 0));
        let mut m = OracleMachine::new(&o, "o", &input, b).unwrap();
        let entry = m.snapshot();
        for _ in 0..b.steps {
            m.forward_step().unwrap();
        }
        assert_eq!(m.commit(1, 13).unwrap(), (1 ^ u128::from(d & 1), 13));
        for _ in 0..b.steps {
            m.inverse_step().unwrap();
        }
        assert_eq!(m.snapshot(), entry);
    }
}

#[test]
fn label_width_covers_all_fixed_binding_instances_in_the_entry_index_space() {
    let o = dual_instance_object();
    let narrow = o
        .text
        .replace("regs { fr:reg[4]", "regs { ip:reg[4], fr:reg[4]")
        .replace(
            "^entry():\nlift.oracle_call @id",
            "^entry():\nip = lift.label ^entry\nlift.oracle_call @id",
        );
    let error = Object::parse(&narrow)
        .expect_err("two distinct worker instances exceed a four-bit index space");
    assert!(error.to_string().contains("index space"));
    let wide = support::rehash(&narrow.replace("ip:reg[4]", "ip:reg[5]"));
    assert_eq!(
        bennett_isa_ref::DerivedWidths::derive(&wide, "o", budget(12, 10, 1))
            .unwrap()
            .p,
        5
    );
}

#[test]
fn forwarding_rejects_missing_lists_locations_literals_and_wrong_fixed_types() {
    let o = object();
    let original = "r = lift.call @worker (x) (tk) (a) (db)";
    for invalid in [
        "r = lift.call @worker (x)",
        "r = lift.call @worker (x) () (a) (db)",
        "r = lift.call @worker (x) (x) (a) (db)",
        "r = lift.call @worker (x) (a) (a) (db)",
        "r = lift.call @worker (x) (tk) (r) (db)",
        "r = lift.call @worker (x) (tk) (0) (db)",
        "r = lift.call @worker (x) (tk) (tk) (db)",
        "r = lift.call @worker (x) (tk) (a) (a)",
    ] {
        assert!(
            Object::parse(&o.text.replace(original, invalid)).is_err(),
            "admitted invalid forwarding: {invalid}"
        );
    }
}

#[test]
fn forwarded_i128_ptr_and_f64_keep_all_bits_including_nan_payloads() {
    let root = r#"{"abi":"0.9","args":["i128","ptr","f64"],"fault":4,"in":[],"kind":"oracle","mem":[],"tgt":128,"tier":"q"}"#;
    let worker = r#"{"abi":"0.9","args":["i128","ptr","f64"],"kind":"lproc","mem":[],"params":[],"result":128,"tier":"q","tokens":[]}"#;
    let o=support::rehash(&support::object(&[("o",root,"oracle @o () (t:wire[128]) (f:wire[4]) () (wide:i128, p:ptr, raw:f64)\nregs { r:reg[128] }\n^entry():\nr = lift.call @w () () (wide, p, raw) ()\nlift.retval r"),("w",worker,"lproc @w () (r:reg[128]) () (wide:i128, p:ptr, raw:f64) ()\nregs { v:reg[128], lo:reg[128], hi:reg[128] }\n^entry():\nv = lift.zext.i128 raw\nlo = lift.zext.i128 p\nhi = lift.xor v wide\nhi = lift.xor hi lo\nlift.ret hi")],"{}","\nsection layout\n{\"A_tab\":1,\"H\":2,\"S_cells\":3,\"globals\":{},\"heap_base\":1,\"heap_limit_max\":0,\"interface_regions\":{},\"null_size\":1,\"ptr_width\":32}\n").replace("=0.8","=0.9"));
    let wide = (1u128 << 127) | 0x0123456789abcdef;
    let pointer = 0xfedcba98u128;
    let b = budget(7, 7, 1);
    for raw in [
        0u64,
        0x8000000000000000,
        0x3ff8000000000000,
        0x7ff0000000000000,
        0xfff0000000000000,
        0x7ff8000000000001,
        0x7ff0000000000042,
    ] {
        let input = OracleInput {
            args: vec![
                Argument::Bits(wide),
                Argument::Bits(pointer),
                Argument::Float(f64::from_bits(raw)),
            ],
            ..Default::default()
        };
        let expected = wide ^ pointer ^ u128::from(raw);
        let out = o.run_oracle("o", &input, b).unwrap();
        assert_eq!((out.payload, out.code), (expected, 0), "raw={raw:016x}");
        let mut m = OracleMachine::new(&o, "o", &input, b).unwrap();
        let entry = m.snapshot();
        for _ in 0..b.steps {
            m.forward_step().unwrap();
        }
        assert_eq!(m.commit(0x55, 13).unwrap(), (expected ^ 0x55, 13));
        for _ in 0..b.steps {
            m.inverse_step().unwrap();
        }
        assert_eq!(m.snapshot(), entry);
    }
}
````

## `reference-interpreter/tests/isa09_qinplace.rs` (963 lines)

````rust
mod support;
use bennett_isa_ref::Object;
fn published_source() -> &'static str {
    include_str!("../../spec/Bennett-ISA-Spec-0.9.md")
        .split_once("**Example 7**")
        .unwrap()
        .1
        .split_once("```\n")
        .unwrap()
        .1
        .split_once("\n```")
        .unwrap()
        .0
}
#[test]
fn published_parameterised_qinplace_source_is_admitted_without_edits() {
    let object = Object::parse(&(published_source().to_string() + "\n")).unwrap();
    object.check_hashes().unwrap();
    assert_eq!(
        object.functions["addya"]
            .instructions()
            .next()
            .unwrap()
            .operands
            .len(),
        7
    );
}
#[test]
fn parameterised_qinplace_checks_both_signatures_and_full_operand_lists() {
    for (from, to) in [
        ("tk x (y) () (a)", "tk x (x) () (a)"),
        ("tk x (y) () (a)", "tk x () () (a)"),
        ("tk x (y) () (a)", "tk x (y) () ()"),
        ("tk x (y) () (a)", "a x (y) () (a)"),
        ("tk x (y) () (a)", "tk x"),
        (
            "oracle @ginv (x:wire[2] in, y:wire[2] in)",
            "oracle @ginv (x:wire[2] in, y:wire in)",
        ),
    ] {
        let bad = published_source().replace(from, to) + "\n";
        assert!(
            Object::parse(&bad).is_err(),
            "admitted mutation {from} -> {to}"
        );
    }
}

fn fields(
    j: &mut bennett_isa_ref::json::Json,
) -> &mut std::collections::BTreeMap<String, bennett_isa_ref::json::Json> {
    let bennett_isa_ref::json::Json::Object(m) = j else {
        panic!("object")
    };
    m
}
fn copy_history(change_input: bool) -> String {
    let object = Object::parse(&(published_source().to_string() + "\n")).unwrap();
    let mut symbols = object.section("symbols").unwrap().clone();
    let signature = fields(fields(&mut symbols).get_mut("2").unwrap())
        .get_mut("signature")
        .unwrap();
    fields(signature).insert("mut".into(), support::json("[2,2]"));
    fields(signature).insert("in".into(), support::json("[]"));
    let mut lines = object.text.lines().map(str::to_string).collect::<Vec<_>>();
    let index = lines.iter().position(|s| s == "section symbols").unwrap() + 1;
    lines[index] = symbols.canonical();
    (lines.join("\n")+"\n")
        .replace("(x:wire[2]) (y:wire[2] in)","(x:wire[2] mut, y:wire[2] mut) ()")
        .replace("action_call @addya (x) (y)","action_call @addya (x, y) ()")
        .replace("qinplace @g @ginv tk x (y) () (a)",&format!("d = qcopy x\nqinplace @g @ginv tk d (y) () (a)\n{}qinplace @ginv @g tk d (y) () (a)\nquncopy x d",if change_input {"x y[0]\n"}else{""}))
}
#[test]
fn qinplace_transfer_keeps_the_read_input_versions_in_its_inverse_key() {
    Object::parse(&copy_history(false)).unwrap();
    let error = Object::parse(&copy_history(true)).unwrap_err();
    assert!(error.to_string().contains("§6.2"), "{error}");
}
fn inverse_certificate() -> String {
    let object = Object::parse(&(published_source().to_string() + "\n")).unwrap();
    inverse_certificate_for(&object)
}
fn inverse_certificate_for(object: &Object) -> String {
    use bennett_isa_ref::json::Json;
    let identity = object.identity().unwrap();
    let owner = identity.closure_hashes["addya"].as_ref().unwrap();
    let g = identity.closure_hashes["g"].as_ref().unwrap();
    let gi = identity.closure_hashes["ginv"].as_ref().unwrap();
    let base = include_str!("../../conformance/fixtures/accepted-k84-09/baseline.bisa");
    let mut certificate =
        Json::parse(base.split_once("section certificate\n").unwrap().1.trim()).unwrap();
    let bindings = fields(fields(&mut certificate).get_mut("bindings").unwrap());
    for (key, value) in [
        ("object_hash", &identity.object_hash),
        ("interface_hash", &identity.interface_hashes["addya"]),
        ("closure_hash", owner),
        ("reference_program_hash", owner),
    ] {
        bindings.insert(key.into(), Json::String(value.clone()));
    }
    bindings.remove("invocation");
    let regions = fields(fields(&mut certificate).get_mut("regions").unwrap());
    let mut record = regions.values().next().unwrap().clone();
    fields(&mut record).insert(
        "signature".into(),
        object.functions["addya"].signature_for(object.isa_version),
    );
    fields(&mut record).insert(
        "bounds".into(),
        Json::Array(
            object.functions["addya"]
                .bounds
                .iter()
                .map(|n| Json::Number(n.to_string()))
                .collect(),
        ),
    );
    fields(&mut record).insert("frame".into(),support::json(r#"{"slots":[{"id":"mut:0","role":"mut","class":"any","width":2},{"id":"in:0","role":"in","class":"any","width":2}],"scratch":[],"history":[],"borrow":[],"ancillae":[]}"#));
    fields(&mut record).insert("resources".into(), support::json("{}"));
    fields(&mut record).insert("gates_used".into(), support::json("{}"));
    let claim = support::json(
        r#"{"kind":"exhaustive","expected":"inverse_pair","domain":{"args":[{"name":"a","width":2,"lo":0,"hi":3}],"borrowed":[],"bundles":[{"name":"x","width":2,"lo":0,"hi":3},{"name":"y","width":2,"lo":0,"hi":3}],"regions":[]}}"#,
    );
    fields(&mut record).insert("claims".into(), Json::Array(vec![claim]));
    let verification = fields(fields(&mut record).get_mut("verification").unwrap());
    verification.insert("unitary".into(), support::json("[]"));
    verification.insert(
        "inverse_pairs".into(),
        support::json(&format!(
            r#"[{{"g":"{g}","ginv":"{gi}","claim":0,"budget":[3,0,0,0]}}]"#
        )),
    );
    regions.clear();
    regions.insert(owner.clone(), record);
    fields(fields(&mut certificate).get_mut("composition").unwrap())
        .insert("multiplicities".into(), support::json("{}"));
    format!(
        "{}\nsection certificate\n{}\n",
        object.text,
        certificate.canonical()
    )
}
#[test]
fn k4_inverse_pair_claim_binds_its_entry_and_quantified_arguments() {
    let object = Object::parse(&inverse_certificate()).unwrap();
    let closure = object.identity().unwrap().closure_hashes["addya"]
        .clone()
        .unwrap();
    assert_eq!(
        object.verify_claim(&closure, 0).unwrap(),
        bennett_isa_ref::ClaimVerdict::Proof
    );

    let reports = object.verify_certificate().unwrap().claims;
    assert_eq!(reports.len(), 1);
    assert_eq!(reports[0].verdict, bennett_isa_ref::ClaimVerdict::Proof);
    assert!(reports[0].coverage.is_none());
}

#[test]
fn inverse_pair_certificate_rejects_a_noninverse_and_an_unbound_claim() {
    let object = Object::parse(&inverse_certificate()).unwrap();
    let identity = object.identity().unwrap();
    let gi = identity.closure_hashes["ginv"].as_ref().unwrap();
    let g = identity.closure_hashes["g"].as_ref().unwrap();
    let original = inverse_certificate();
    let wrong = original.replace(&format!(r#""ginv":"{gi}""#), &format!(r#""ginv":"{g}""#));
    assert_ne!(wrong, original);
    let wrong = Object::parse(&wrong).unwrap();
    let owner = identity.closure_hashes["addya"].as_ref().unwrap();
    let error = wrong.verify_claim(owner, 0).unwrap_err();
    assert!(error.to_string().contains("differs from x"), "{error}");
    let error = wrong.verify_certificate().unwrap_err();
    assert!(error.to_string().contains("missing owner-local"), "{error}");
    let no_entry = original.replace(
        &format!(r#"[{{"budget":[3,0,0,0],"claim":0,"g":"{g}","ginv":"{gi}"}}]"#),
        "[]",
    );
    assert_ne!(no_entry, original);
    let error = Object::parse(&no_entry).unwrap_err();
    assert!(
        error.to_string().contains("owner-local entry binding"),
        "{error}"
    );
}

#[test]
fn inverse_pair_proof_checks_padded_success_and_rejects_a_faulting_minimum() {
    for steps in [2, 3, 9] {
        let text = inverse_certificate().replace(
            "\"budget\":[3,0,0,0]",
            &format!("\"budget\":[{steps},0,0,0]"),
        );
        let object = Object::parse(&text).unwrap();
        let owner = object.identity().unwrap().closure_hashes["addya"]
            .clone()
            .unwrap();
        let result = object.verify_claim(&owner, 0);
        if steps == 2 {
            assert!(result
                .unwrap_err()
                .to_string()
                .contains("inverse-pair oracle faults"));
        } else {
            assert_eq!(
                result.unwrap(),
                bennett_isa_ref::ClaimVerdict::Proof,
                "B={steps}"
            );
        }
    }
}
#[test]
fn inverse_pair_quantum_domains_must_be_full_but_argument_ranges_are_scoped() {
    for (from, to) in [
        (
            "\"hi\":3,\"lo\":0,\"name\":\"x\"",
            "\"hi\":2,\"lo\":0,\"name\":\"x\"",
        ),
        (
            "\"hi\":3,\"lo\":0,\"name\":\"a\",\"width\":2",
            "\"hi\":3,\"lo\":0,\"name\":\"a\",\"width\":3",
        ),
    ] {
        let original = inverse_certificate();
        assert!(original.contains(from));
        let result = Object::parse(&original.replace(from, to));
        assert!(result.is_err());
        assert!(result.unwrap_err().to_string().contains("K4"));
    }
    let text = inverse_certificate().replace(
        "\"hi\":3,\"lo\":0,\"name\":\"a\"",
        "\"hi\":2,\"lo\":0,\"name\":\"a\"",
    );
    let object = Object::parse(&text).unwrap();
    let owner = object.identity().unwrap().closure_hashes["addya"]
        .clone()
        .unwrap();
    assert_eq!(
        object.verify_claim(&owner, 0).unwrap(),
        bennett_isa_ref::ClaimVerdict::Proof
    );
}

fn quantum_input(
    x: u128,
    y: u128,
) -> (
    bennett_isa_ref::QuantumState,
    bennett_isa_ref::QuantumBindings,
    Vec<u64>,
) {
    use bennett_isa_ref::{QuantumBindings, QuantumState};
    let mut q = QuantumState::new();
    let wires = q.allocate(4).unwrap();
    for (i, w) in wires.iter().enumerate() {
        if (x | (y << 2)) >> i & 1 != 0 {
            q.gate("x", &[*w], None, &[]).unwrap();
        }
    }
    let mut b = QuantumBindings::default();
    b.bundles.insert("x".into(), wires[..2].to_vec());
    b.bundles.insert("y".into(), wires[2..].to_vec());
    (q, b, wires)
}
#[test]
fn declared_parameterised_pair_executes_every_x_y_a_and_its_adjoint() {
    use bennett_isa_ref::{Argument, Budget};
    let object = Object::parse(&inverse_certificate()).unwrap();
    for steps in [3, 9] {
        for x in 0..4 {
            for y in 0..4 {
                for a in 0..4 {
                    let (mut q, mut b, wires) = quantum_input(x, y);
                    b.args
                        .insert("tk".into(), Argument::Token(Budget::steps(steps)));
                    b.args.insert("a".into(), Argument::Bits(a));
                    let before = q.clone();
                    object
                        .execute_action_with_token_aliases("addya", &mut q, &b, false, &[], &[0])
                        .unwrap();
                    assert_eq!(q.read_basis(&wires).unwrap(), ((x + y + a) & 3) | (y << 2));
                    object
                        .execute_action_with_token_aliases("addya", &mut q, &b, true, &[], &[0])
                        .unwrap();
                    assert_eq!(q, before);
                }
            }
        }
    }
}
#[test]
fn uncovered_pair_rejects_before_the_earliest_effect_of_the_region() {
    use bennett_isa_ref::{Argument, Budget};
    let text = published_source().replace(
        "qinplace @g @ginv tk x (y) () (a)",
        "x x[0]\nqinplace @g @ginv tk x (y) () (a)",
    ) + "\n";
    let source = support::rehash(&text);
    let packet = inverse_certificate_for(&source).replace(
        "\"hi\":3,\"lo\":0,\"name\":\"a\"",
        "\"hi\":2,\"lo\":0,\"name\":\"a\"",
    );
    for object in [source, Object::parse(&packet).unwrap()] {
        for (steps, a) in [(2, 1), (3, 3)] {
            let (mut q, mut b, _) = quantum_input(2, 1);
            b.args
                .insert("tk".into(), Argument::Token(Budget::steps(steps)));
            b.args.insert("a".into(), Argument::Bits(a));
            let before = q.clone();
            let result =
                object.execute_action_with_token_aliases("addya", &mut q, &b, false, &[], &[0]);
            assert!(result.is_err());
            assert_eq!(q, before, "uncovered tk={steps}/a={a} changed a prefix");
        }
    }
}

#[test]
fn source_qinplace_adjoints_preserve_instruction_allocation_and_release_order() {
    use bennett_isa_conformance::{json, ref_catalog::Machine, ref_language::permutation};
    let object = Object::parse(&inverse_certificate()).unwrap();
    let root = object.identity().unwrap().closure_hashes["addya"]
        .clone()
        .unwrap();
    let args = json::parse(r#"["x","y",["3","0","0","0"],"1"]"#).unwrap();
    for adjoint in [false, true] {
        let leaves = object
            .expand_action_source_with_token_aliases(
                "addya",
                args.as_arr().unwrap(),
                &[("x", 2), ("y", 2)],
                adjoint,
                &[0],
            )
            .unwrap();
        let own = leaves
            .iter()
            .filter(|l| l.source.as_ref().is_some_and(|s| s.terminal.symbol == root))
            .collect::<Vec<_>>();
        let allocation = own
            .iter()
            .filter(|l| l.gate == "alloc")
            .map(|l| l.allocation.as_ref().unwrap().1)
            .collect::<Vec<_>>();
        let release = own
            .iter()
            .filter(|l| l.gate == "release")
            .map(|l| l.allocation.as_ref().unwrap().1)
            .collect::<Vec<_>>();
        assert_eq!(allocation, [2, 4], "adjoint={adjoint}");
        assert_eq!(release, [2, 4], "adjoint={adjoint}");
        let machine =
            Machine::compile(&permutation(&leaves).unwrap(), &[("x", 2), ("y", 2)]).unwrap();
        for x in 0..4 {
            for y in 0..4 {
                let mut state = machine.state();
                machine.set(&mut state, "x", x);
                machine.set(&mut state, "y", y);
                let before = state.clone();
                machine.run(&mut state, true, false).unwrap();
                assert_eq!(
                    machine.get(&state, "x"),
                    if adjoint {
                        (x + 8 - y - 1) & 3
                    } else {
                        (x + y + 1) & 3
                    }
                );
                assert_eq!(machine.get(&state, "y"), y);
                machine.run(&mut state, true, true).unwrap();
                assert_eq!(state, before);
            }
        }
    }
}

fn change_certificate(text: &str, change: impl FnOnce(&mut bennett_isa_ref::json::Json)) -> String {
    let (source, packet) = text.split_once("section certificate\n").unwrap();
    let mut certificate = bennett_isa_ref::json::Json::parse(packet.trim()).unwrap();
    change(&mut certificate);
    format!("{source}section certificate\n{}\n", certificate.canonical())
}
fn root_invocation(steps: u64, a: u64) -> bennett_isa_ref::json::Json {
    support::json(&format!(
        r#"{{"args":[["{steps}","0","0","0"],"{a}"],"budget":["0","0","0","0"],"token_aliases":[0]}}"#
    ))
}
fn linked_inverse_certificate(wrong_pair: bool) -> String {
    let text = inverse_certificate();
    let object = Object::parse(&text).unwrap();
    let identity = object.identity().unwrap();
    let owner = identity.closure_hashes["addya"].as_ref().unwrap();
    let g = identity.closure_hashes["g"].as_ref().unwrap();
    change_certificate(&text, |certificate| {
        let regions = fields(fields(certificate).get_mut("regions").unwrap());
        let mut donor = regions[owner].clone();
        fields(&mut donor).insert("kind".into(), support::json("\"oracle\""));
        fields(&mut donor).insert("bounds".into(), support::json("[]"));
        fields(&mut donor).insert(
            "signature".into(),
            object.functions["g"].signature_for(object.isa_version),
        );
        fields(&mut donor).insert("frame".into(), support::json(r#"{"slots":[{"id":"in:0","role":"in","class":"any","width":2},{"id":"in:1","role":"in","class":"any","width":2},{"id":"tgt:0","role":"tgt","class":"any","width":2},{"id":"fault:0","role":"fault","class":"any","width":4}],"scratch":[],"history":[],"borrow":[],"ancillae":[]}"#));
        let record = fields(regions.get_mut(owner).unwrap());
        record.insert("claims".into(), support::json(&format!(r#"[{{"kind":"structural","rule":"inverse_pair_library","subclaims":[],"witness":{{"library_closure_hash":"{g}","claim_index":0}},"invocation":{}}}]"#, root_invocation(3,1).canonical())));
        if wrong_pair {
            let entries = fields(record.get_mut("verification").unwrap())
                .get_mut("inverse_pairs")
                .unwrap();
            let bennett_isa_ref::json::Json::Array(entries) = entries else {
                panic!("entries")
            };
            fields(&mut entries[0]).insert(
                "ginv".into(),
                bennett_isa_ref::json::Json::String(g.clone()),
            );
        }
        regions.insert(g.clone(), donor);
    })
}
#[test]
fn checker_rejects_missing_owner_local_qinplace_inventory() {
    let text = change_certificate(&inverse_certificate(), |c| {
        let record = fields(fields(c).get_mut("regions").unwrap())
            .values_mut()
            .next()
            .unwrap();
        fields(record).insert("claims".into(), support::json("[]"));
        fields(fields(record).get_mut("verification").unwrap())
            .insert("inverse_pairs".into(), support::json("[]"));
    });
    let error = Object::parse(&text)
        .unwrap()
        .verify_certificate()
        .unwrap_err();
    assert!(error.to_string().contains("K92"), "{error}");
}
#[test]
fn checker_rejects_bound_invocation_below_the_pair_minimum() {
    let text = change_certificate(&inverse_certificate(), |c| {
        fields(fields(c).get_mut("bindings").unwrap())
            .insert("invocation".into(), root_invocation(2, 1));
    });
    let error = Object::parse(&text)
        .unwrap()
        .verify_certificate()
        .unwrap_err();
    assert!(
        error.to_string().contains("no covering inverse-pair entry"),
        "{error}"
    );
}
#[test]
fn standalone_pair_proof_reports_unestablished_applicability() {
    let reports = Object::parse(&inverse_certificate())
        .unwrap()
        .verify_certificate()
        .unwrap()
        .claims;
    assert_eq!(reports[0].verdict, bennett_isa_ref::ClaimVerdict::Proof);
    assert!(
        matches!(
            reports[0].qinplace_applicability,
            Some(bennett_isa_ref::QinplaceApplicability::Unestablished(_))
        ),
        "{reports:?}"
    );
}
#[test]
fn library_proof_cannot_transfer_to_a_different_pair() {
    let object = Object::parse(&linked_inverse_certificate(true)).unwrap();
    let owner = object.identity().unwrap().closure_hashes["addya"]
        .clone()
        .unwrap();
    // g(x;y,a)=x+y+a mod 4: g(g(0;0,1);0,1)=2, so g/g is not inverse.
    let error = object.verify_claim(&owner, 0).unwrap_err();
    assert!(error.to_string().contains("same resolved pair"), "{error}");
    let error = object.verify_certificate().unwrap_err();
    assert!(error.to_string().contains("K92"), "{error}");
}
#[test]
fn linked_library_pair_executes_every_argument_and_adjoint() {
    use bennett_isa_ref::{Argument, Budget, ClaimVerdict};
    let object = Object::parse(&linked_inverse_certificate(false)).unwrap();
    let owner = object.identity().unwrap().closure_hashes["addya"]
        .clone()
        .unwrap();
    assert_eq!(object.verify_claim(&owner, 0).unwrap(), ClaimVerdict::Proof);
    for steps in [3, 9] {
        for x in 0..4 {
            for y in 0..4 {
                for a in 0..4 {
                    let (mut q, mut b, wires) = quantum_input(x, y);
                    b.args
                        .insert("tk".into(), Argument::Token(Budget::steps(steps)));
                    b.args.insert("a".into(), Argument::Bits(a));
                    let before = q.clone();
                    object
                        .execute_action_with_token_aliases("addya", &mut q, &b, false, &[], &[0])
                        .unwrap();
                    assert_eq!(q.read_basis(&wires).unwrap(), ((x + y + a) & 3) | (y << 2));
                    object
                        .execute_action_with_token_aliases("addya", &mut q, &b, true, &[], &[0])
                        .unwrap();
                    assert_eq!(q, before);
                }
            }
        }
    }
}

fn loop_certificate(iterations: usize) -> String {
    let text = published_source()
        .replace("\"bounds\":[]", &format!("\"bounds\":[{iterations}]"))
        .replace(
            "(tk:token, a:i2) ()\n^entry():",
            &format!("(tk:token, a:i2) ()\nregs {{  }} bounds {{{iterations}}}\n^entry():"),
        )
        .replace(
            "qinplace @g @ginv tk x (y) () (a)",
            &format!("qloop {iterations} {{\nqinplace @g @ginv tk x (y) () (a)\n}}"),
        )
        + "\n";
    inverse_certificate_for(&support::rehash(&text))
}
#[test]
fn zero_trip_qinplace_requires_inventory_but_has_no_applicability_visit() {
    let text = loop_certificate(0);
    let bound = change_certificate(&text, |c| {
        fields(fields(c).get_mut("bindings").unwrap())
            .insert("invocation".into(), root_invocation(2, 1));
    });
    let reports = Object::parse(&bound)
        .unwrap()
        .verify_certificate()
        .unwrap()
        .claims;
    assert_eq!(
        reports[0].qinplace_applicability,
        Some(bennett_isa_ref::QinplaceApplicability::Established)
    );
    let missing = change_certificate(&bound, |c| {
        let record = fields(fields(c).get_mut("regions").unwrap())
            .values_mut()
            .next()
            .unwrap();
        fields(record).insert("claims".into(), support::json("[]"));
        fields(fields(record).get_mut("verification").unwrap())
            .insert("inverse_pairs".into(), support::json("[]"));
    });
    let error = Object::parse(&missing)
        .unwrap()
        .verify_certificate()
        .unwrap_err();
    assert!(error.to_string().contains("K92"), "{error}");
}
#[test]
fn nested_qinplace_below_minimum_rejects_in_checker_and_before_execution() {
    use bennett_isa_ref::{Argument, Budget};
    let text = change_certificate(&loop_certificate(1), |c| {
        fields(fields(c).get_mut("bindings").unwrap())
            .insert("invocation".into(), root_invocation(2, 1));
    });
    let object = Object::parse(&text).unwrap();
    let error = object.verify_certificate().unwrap_err();
    assert!(
        error.to_string().contains("no covering inverse-pair entry"),
        "{error}"
    );
    let (mut q, mut b, _) = quantum_input(0, 0);
    b.args
        .insert("tk".into(), Argument::Token(Budget::steps(2)));
    b.args.insert("a".into(), Argument::Bits(1));
    let before = q.clone();
    let error = object
        .execute_action_with_token_aliases("addya", &mut q, &b, false, &[], &[0])
        .unwrap_err();
    assert!(
        error.to_string().contains("no covering inverse-pair entry"),
        "{error}"
    );
    assert_eq!(q, before);
}
#[test]
fn library_reuse_preserves_the_proved_minimum_and_argument_domain() {
    let text = linked_inverse_certificate(false);
    let object = Object::parse(&text).unwrap();
    let owner = object.identity().unwrap().closure_hashes["addya"]
        .clone()
        .unwrap();
    let too_small = change_certificate(&text, |c| {
        let record = fields(fields(c).get_mut("regions").unwrap())
            .get_mut(&owner)
            .unwrap();
        let entries = fields(fields(record).get_mut("verification").unwrap())
            .get_mut("inverse_pairs")
            .unwrap();
        let bennett_isa_ref::json::Json::Array(entries) = entries else {
            panic!("entries")
        };
        fields(&mut entries[0]).insert("budget".into(), support::json("[2,0,0,0]"));
    });
    let error = Object::parse(&too_small)
        .unwrap()
        .verify_claim(&owner, 0)
        .unwrap_err();
    assert!(error.to_string().contains("token context"), "{error}");
    let scoped = text.replace(
        "\"hi\":3,\"lo\":0,\"name\":\"a\"",
        "\"hi\":2,\"lo\":0,\"name\":\"a\"",
    );
    assert_ne!(scoped, text);
    let uncovered = change_certificate(&scoped, |c| {
        fields(fields(c).get_mut("bindings").unwrap())
            .insert("invocation".into(), root_invocation(3, 3));
    });
    let error = Object::parse(&uncovered)
        .unwrap()
        .verify_certificate()
        .unwrap_err();
    assert!(
        error.to_string().contains("no covering inverse-pair entry"),
        "{error}"
    );
}

fn transitive_certificate(include_inner: bool) -> String {
    use bennett_isa_ref::json::Json;
    let original = Object::parse(&(published_source().to_string() + "\n")).unwrap();
    let mut symbols = original.section("symbols").unwrap().clone();
    let mut inner = fields(&mut symbols)["2"].clone();
    fields(&mut inner).insert("name".into(), Json::String("inner".into()));
    fields(&mut symbols).insert("4".into(), inner);
    let mut lines = original
        .text
        .lines()
        .map(str::to_string)
        .collect::<Vec<_>>();
    let i = lines.iter().position(|s| s == "section symbols").unwrap() + 1;
    lines[i] = symbols.canonical();
    let source = (lines.join("\n")+"\n").replace("qinplace @g @ginv tk x (y) () (a)", "action_call @inner (x) (y) () (tk, a)")
        + "perm_action @inner (x:wire[2]) (y:wire[2] in) () (tk:token, a:i2) ()\n^entry():\nqinplace @g @ginv tk x (y) () (a)\n";
    let object = support::rehash(&source);
    let text = inverse_certificate_for(&object);
    change_certificate(&text, |c| {
        if include_inner {
            let hash = object.identity().unwrap().closure_hashes["inner"]
                .clone()
                .unwrap();
            let regions = fields(fields(c).get_mut("regions").unwrap());
            let record = regions.values().next().unwrap().clone();
            regions.insert(hash, record);
        }
    })
}
#[test]
fn bound_reference_tree_checks_transitive_owner_and_actual_arguments() {
    for (include_inner, steps) in [(false, 3), (true, 2), (true, 3), (true, 9)] {
        let text = change_certificate(&transitive_certificate(include_inner), |c| {
            fields(fields(c).get_mut("bindings").unwrap())
                .insert("invocation".into(), root_invocation(steps, 1));
        });
        let result = Object::parse(&text).unwrap().verify_certificate();
        if include_inner && steps >= 3 {
            let reports = result.unwrap().claims;
            let inner = reports.iter().find(|r| r.region == "inner").unwrap();
            assert_eq!(
                inner.qinplace_applicability,
                Some(bennett_isa_ref::QinplaceApplicability::Established)
            );
        } else {
            let error = result.unwrap_err();
            assert!(
                error
                    .to_string()
                    .contains("no covering inverse-pair entry in @inner"),
                "{error}"
            );
        }
    }
}
#[test]
fn disabled_coherent_predicate_keeps_the_qinplace_obligation() {
    let source = published_source().replace("qinplace @g @ginv tk x (y) () (a)", "c = qalloc any 1\nqif c {\nqinplace @g @ginv tk x (y) () (a)\n} {\nx x[0]\nx x[0]\n}\nqfree c") + "\n";
    let text = change_certificate(&inverse_certificate_for(&support::rehash(&source)), |c| {
        fields(fields(c).get_mut("bindings").unwrap())
            .insert("invocation".into(), root_invocation(2, 1));
    });
    let error = Object::parse(&text)
        .unwrap()
        .verify_certificate()
        .unwrap_err();
    assert!(
        error.to_string().contains("no covering inverse-pair entry"),
        "{error}"
    );
}

#[test]
fn missing_library_body_reports_unestablished_and_cannot_execute() {
    use bennett_isa_ref::{Argument, Budget, ClaimVerdict, QinplaceApplicability};
    let text = linked_inverse_certificate(false);
    let object = Object::parse(&text).unwrap();
    let g = object.identity().unwrap().closure_hashes["g"]
        .clone()
        .unwrap();
    let text = change_certificate(&text, |c| {
        fields(fields(c).get_mut("regions").unwrap()).remove(&g);
    });
    let object = Object::parse(&text).unwrap();
    let report = object.verify_certificate().unwrap().claims.remove(0);
    assert!(
        matches!(report.verdict, ClaimVerdict::Unverified(_)),
        "{report:?}"
    );
    assert!(
        matches!(
            report.qinplace_applicability,
            Some(QinplaceApplicability::Unestablished(_))
        ),
        "{report:?}"
    );
    let (mut q, mut b, _) = quantum_input(0, 0);
    b.args
        .insert("tk".into(), Argument::Token(Budget::steps(3)));
    b.args.insert("a".into(), Argument::Bits(1));
    let before = q.clone();
    let error = object
        .execute_action_with_token_aliases("addya", &mut q, &b, false, &[], &[0])
        .unwrap_err();
    assert!(
        error
            .to_string()
            .contains("unestablished qinplace applicability"),
        "{error}"
    );
    assert_eq!(q, before);
}

enum CertificateContents {
    PairClaim,
    EmptyClaims,
    EmptyRecords,
}

fn unsupported_bound_root_certificate(contents: CertificateContents) -> String {
    use bennett_isa_ref::json::Json;
    let text = transitive_certificate(false);
    let identity = Object::parse(&text).unwrap().identity().unwrap();
    change_certificate(&text, |c| {
        let bindings = fields(fields(c).get_mut("bindings").unwrap());
        for (key, value) in [
            (
                "closure_hash",
                identity.closure_hashes["run"].as_ref().unwrap(),
            ),
            (
                "reference_program_hash",
                identity.closure_hashes["run"].as_ref().unwrap(),
            ),
            ("interface_hash", &identity.interface_hashes["run"]),
        ] {
            bindings.insert(key.into(), Json::String(value.clone()));
        }
        bindings.insert("invocation".into(), root_invocation(2, 1));
        let regions = fields(fields(c).get_mut("regions").unwrap());
        match contents {
            CertificateContents::PairClaim => {}
            CertificateContents::EmptyRecords => regions.clear(),
            CertificateContents::EmptyClaims => {
                for record in regions.values_mut() {
                    fields(record).insert("claims".into(), support::json("[]"));
                    fields(fields(record).get_mut("verification").unwrap())
                        .insert("inverse_pairs".into(), support::json("[]"));
                }
            }
        }
    })
}

#[test]
fn unsupported_bound_root_keeps_applicability_without_direct_owner() {
    use bennett_isa_ref::{ClaimVerdict, QinplaceApplicability};
    let object = Object::parse(&unsupported_bound_root_certificate(
        CertificateContents::PairClaim,
    ))
    .unwrap();
    let identity = object.identity().unwrap();
    let owner = identity.closure_hashes["addya"].as_ref().unwrap();
    let root = identity.closure_hashes["run"].as_ref().unwrap();
    let report = object.verify_certificate().unwrap();
    assert_eq!(report.claims.len(), 1);
    assert_eq!(report.claims[0].verdict, ClaimVerdict::Proof);
    assert_eq!(object.verify_claim(owner, 0).unwrap(), ClaimVerdict::Proof);
    assert_eq!(report.qinplace_applicability.len(), 1);
    assert!(
        matches!(report.qinplace_applicability.get(root), Some(QinplaceApplicability::Unestablished(reason)) if reason.contains("bound @run")),
        "{report:?}"
    );
}

#[test]
fn unsupported_bound_root_keeps_applicability_without_claims() {
    let object = Object::parse(&unsupported_bound_root_certificate(
        CertificateContents::EmptyClaims,
    ))
    .unwrap();
    let root = object.identity().unwrap().closure_hashes["run"]
        .clone()
        .unwrap();
    let report = object.verify_certificate().unwrap();
    assert!(report.claims.is_empty(), "{report:?}");
    assert!(
        matches!(report.qinplace_applicability.get(&root), Some(bennett_isa_ref::QinplaceApplicability::Unestablished(reason)) if reason.contains("bound @run")),
        "{report:?}"
    );
}

#[test]
fn unsupported_bound_root_keeps_applicability_without_records() {
    let object = Object::parse(&unsupported_bound_root_certificate(
        CertificateContents::EmptyRecords,
    ))
    .unwrap();
    let root = object.identity().unwrap().closure_hashes["run"]
        .clone()
        .unwrap();
    let report = object.verify_certificate().unwrap();
    assert!(report.claims.is_empty(), "{report:?}");
    assert!(
        matches!(report.qinplace_applicability.get(&root), Some(bennett_isa_ref::QinplaceApplicability::Unestablished(reason)) if reason.contains("bound @run")),
        "{report:?}"
    );
}

#[test]
fn uncheckable_uniform_transitive_claim_keeps_applicability() {
    // The outer caller has no local site; universal transitive coverage is
    // separate from the structural theorem.
    let source = transitive_certificate(false);
    let owner = Object::parse(&source)
        .unwrap()
        .identity()
        .unwrap()
        .closure_hashes["addya"]
        .clone()
        .unwrap();
    let text = change_certificate(&source, |c| {
        let record = fields(fields(c).get_mut("regions").unwrap())
            .get_mut(&owner)
            .unwrap();
        fields(record).insert("claims".into(), support::json(r#"[{"kind":"structural","rule":"adjoint_table","subclaims":[],"witness":{},"invocation":{"args":"all","budget":"all","token_aliases":"all"}}]"#));
        fields(fields(record).get_mut("verification").unwrap())
            .insert("inverse_pairs".into(), support::json("[]"));
    });
    let report = Object::parse(&text).unwrap().verify_certificate().unwrap();
    assert_eq!(report.claims.len(), 1);
    assert!(
        matches!(report.qinplace_applicability.get(&owner), Some(bennett_isa_ref::QinplaceApplicability::Unestablished(reason)) if reason.contains("parameter-uniform")),
        "{report:?}"
    );
}

#[test]
fn scheduled_root_keeps_unchecked_tree_obligation_without_owners_or_claims() {
    use bennett_isa_ref::{json::Json, sha256_hex, QinplaceApplicability};
    let text = transitive_certificate(false);
    let original = Object::parse(&text).unwrap();
    let mut symbols = original.section("symbols").unwrap().clone();
    fields(
        fields(fields(&mut symbols).get_mut("2").unwrap())
            .get_mut("signature")
            .unwrap(),
    )
    .insert("bounds".into(), support::json("[0]"));
    let mut lines = text.lines().map(str::to_string).collect::<Vec<_>>();
    let index = lines
        .iter()
        .position(|line| line == "section symbols")
        .unwrap()
        + 1;
    lines[index] = symbols.canonical();
    let text = lines.join("\n");
    let source = text.split_once("section certificate\n").unwrap().0.replace(
        "action_call @inner (x) (y) () (tk, a)",
        "qloop 0 {\naction_call @inner (x) (y) () (tk, a)\n}",
    ).replace(
        "perm_action @addya (x:wire[2]) (y:wire[2] in) () (tk:token, a:i2) ()\n^entry():",
        "perm_action @addya (x:wire[2]) (y:wire[2] in) () (tk:token, a:i2) ()\nregs {  } bounds {0}\n^entry():",
    );
    let object = support::rehash(&(source.trim_end().to_string() + "\n"));
    let owner = object.identity().unwrap().closure_hashes["addya"]
        .clone()
        .unwrap();
    let invocation = root_invocation(3, 1);
    let params = sha256_hex(invocation.get("args").unwrap().canonical().as_bytes());
    let schedule = support::json(&format!(
        r#"{{"bindings":{{"budget":[0,0,0,0],"closure_hash":"{owner}","epsilon":0,"inherited_controls":0,"params_hash":"{params}","region":"addya","scheduler":{{"name":"test","version":"1"}},"target_hash":"{}","token_aliases":[0],"variant":"forward"}},"entries":[]}}"#,
        "0".repeat(64)
    ));
    let text = change_certificate(&inverse_certificate_for(&object), |c| {
        fields(fields(c).get_mut("regions").unwrap()).clear();
        let bindings = fields(fields(c).get_mut("bindings").unwrap());
        bindings.insert("invocation".into(), invocation);
        bindings.insert("target_hash".into(), Json::String("0".repeat(64)));
        bindings.insert(
            "schedule_hash".into(),
            Json::String(sha256_hex(schedule.canonical().as_bytes())),
        );
    });
    let (source, certificate) = text.split_once("section certificate\n").unwrap();
    let text = format!(
        "{}\n\nsection schedule\n{}\n\nsection certificate\n{certificate}",
        source.trim_end(),
        schedule.canonical()
    );
    let report = Object::parse(&text).unwrap().verify_certificate().unwrap();
    assert!(report.claims.is_empty());
    assert!(
        matches!(report.qinplace_applicability.get(&owner), Some(QinplaceApplicability::Unestablished(reason)) if reason.contains("realised invocation tree")),
        "{report:?}"
    );
}

#[test]
fn checked_concrete_context_does_not_discharge_uniform_applicability() {
    let text = linked_inverse_certificate(false);
    let object = Object::parse(&text).unwrap();
    let owner = object.identity().unwrap().closure_hashes["addya"]
        .clone()
        .unwrap();
    let text = change_certificate(&text, |c| {
        fields(fields(c).get_mut("bindings").unwrap())
            .insert("invocation".into(), root_invocation(3, 1));
        let record = fields(fields(c).get_mut("regions").unwrap())
            .get_mut(&owner)
            .unwrap();
        let bennett_isa_ref::json::Json::Array(claims) = fields(record).get_mut("claims").unwrap()
        else {
            panic!("claims")
        };
        fields(&mut claims[0]).insert(
            "invocation".into(),
            support::json(r#"{"args":"all","budget":"all","token_aliases":"all"}"#),
        );
    });
    let report = Object::parse(&text).unwrap().verify_certificate().unwrap();
    assert_eq!(
        report
            .claims
            .iter()
            .find(|c| c.closure_hash == owner)
            .unwrap()
            .verdict,
        bennett_isa_ref::ClaimVerdict::Proof
    );
    assert!(
        matches!(report.qinplace_applicability.get(&owner), Some(bennett_isa_ref::QinplaceApplicability::Unestablished(reason)) if reason.contains("parameter-uniform")),
        "{report:?}"
    );
}
````

## `reference-interpreter/tests/isa09_token_aliases.rs` (862 lines)

````rust
mod support;
use bennett_isa_ref::{json::Json, ClaimVerdict, Object};
use std::collections::BTreeMap;
const BASE: &str = include_str!("../../conformance/fixtures/accepted-k84-09/baseline.bisa");
fn fields(value: &mut Json) -> &mut BTreeMap<String, Json> {
    let Json::Object(fields) = value else {
        panic!("object")
    };
    fields
}
fn certificate_object(aliases: Option<&str>, second: u64) -> String {
    let (source, certificate) = BASE.split_once("section certificate\n").unwrap();
    let source = source.trim_end().to_string() + "\n";
    let mut symbols = Object::parse(&source)
        .unwrap()
        .section("symbols")
        .unwrap()
        .clone();
    let symbol = fields(&mut symbols).get_mut("0").unwrap();
    fields(fields(symbol).get_mut("signature").unwrap())
        .insert("args".into(), support::json(r#"["token","token"]"#));
    let mut lines = source.lines().map(str::to_string).collect::<Vec<_>>();
    let section = lines.iter().position(|s| s == "section symbols").unwrap();
    lines[section + 1] = symbols.canonical();
    let source = (lines.join("\n") + "\n").replace(
        "(t:wire mut) () () () ()",
        "(t:wire mut) () () (a:token, b:token) ()",
    );
    let object = support::rehash(&source);
    let identity = object.identity().unwrap();
    let closure = identity.closure_hashes["flip"].as_ref().unwrap();
    let mut c = Json::parse(certificate.trim()).unwrap();
    let bindings = fields(fields(&mut c).get_mut("bindings").unwrap());
    for (key, value) in [
        ("object_hash", &identity.object_hash),
        ("interface_hash", &identity.interface_hashes["flip"]),
        ("closure_hash", closure),
        ("reference_program_hash", closure),
    ] {
        bindings.insert(key.into(), Json::String(value.clone()));
    }
    let mut invocation = support::json(&format!(
        r#"{{"args":[["1","0","0","0"],["{second}","0","0","0"]],"budget":["0","0","0","0"]}}"#
    ));
    if let Some(aliases) = aliases {
        fields(&mut invocation).insert("token_aliases".into(), support::json(aliases));
    }
    bindings.insert("invocation".into(), invocation.clone());
    let regions = fields(fields(&mut c).get_mut("regions").unwrap());
    let mut region = regions.values().next().unwrap().clone();
    fields(&mut region).insert(
        "signature".into(),
        object.functions["flip"].signature_for(object.isa_version),
    );
    let Json::Array(claims) = fields(&mut region).get_mut("claims").unwrap() else {
        panic!("claims")
    };
    fields(&mut claims[0]).insert("invocation".into(), invocation);
    fields(fields(&mut claims[0]).get_mut("subject").unwrap())
        .insert("closure_hash".into(), Json::String(closure.clone()));
    regions.clear();
    regions.insert(closure.clone(), region);
    fields(fields(&mut c).get_mut("composition").unwrap()).insert(
        "multiplicities".into(),
        support::json(&format!(r#"{{"{closure}:forward:0":1}}"#)),
    );
    format!("{}\nsection certificate\n{}\n", object.text, c.canonical())
}

#[test]
fn certificate_invocations_admit_both_equal_tuple_identity_partitions() {
    let mut hashes = Vec::new();
    for labels in ["[0,0]", "[0,1]"] {
        let object = Object::parse(&certificate_object(Some(labels), 1)).unwrap();
        object.check_hashes().unwrap();
        hashes.push(object.identity().unwrap().object_hash);
        let certificate = object.section("certificate").unwrap();
        let closure = certificate
            .get("bindings")
            .unwrap()
            .get("closure_hash")
            .unwrap()
            .string()
            .unwrap();
        assert_eq!(
            object.verify_claim(closure, 0).unwrap(),
            ClaimVerdict::Proof
        );
        assert_eq!(
            object.verify_certificate().unwrap().claims[0].verdict,
            ClaimVerdict::Proof
        );
    }
    assert_eq!(
        hashes[0], hashes[1],
        "partition metadata does not change object identity"
    );
}

#[test]
fn missing_malformed_and_tuple_inconsistent_certificate_partitions_reject() {
    for (labels, second) in [
        (None, 1),
        (Some("[1,1]"), 1),
        (Some("[0,2]"), 1),
        (Some("[0]"), 1),
        (Some("[0,0]"), 2),
        (Some("[-1,0]"), 1),
    ] {
        let result = Object::parse(&certificate_object(labels, second));
        assert!(result.is_err(), "admitted {labels:?}/{second}");
        assert!(result.unwrap_err().to_string().contains("K91"));
    }
}

#[test]
fn uniform_token_claims_quantify_over_every_consistent_partition() {
    let original = certificate_object(Some("[0,1]"), 1);
    let (source, c) = original.split_once("section certificate\n").unwrap();
    for aliases in [false, true] {
        let mut certificate = Json::parse(c.trim()).unwrap();
        let regions = fields(fields(&mut certificate).get_mut("regions").unwrap());
        let region = regions.values_mut().next().unwrap();
        let mut claim = support::json(
            r#"{"kind":"structural","rule":"adjoint_table","subclaims":[],"witness":{},"invocation":{"args":"all","budget":"all"}}"#,
        );
        if aliases {
            fields(fields(&mut claim).get_mut("invocation").unwrap())
                .insert("token_aliases".into(), Json::String("all".into()));
        }
        fields(region).insert("claims".into(), Json::Array(vec![claim]));
        let result = Object::parse(&format!(
            "{source}section certificate\n{}\n",
            certificate.canonical()
        ));
        assert_eq!(result.is_ok(), aliases);
        if !aliases {
            assert!(result.unwrap_err().to_string().contains("K91"));
        }
    }
}

fn oracle_source(token: bool) -> Object {
    let signature = format!(
        r#"{{"abi":"0.8","args":{},"fault":4,"in":[1],"kind":"oracle","mem":[],"tgt":1,"tier":"q"}}"#,
        if token { r#"["token"]"# } else { "[]" }
    );
    let body = format!(
        "oracle @id (x:wire in) (t:wire) (f:wire[4]) () {}\n^entry():\nlift.retval x",
        if token { "(a:token)" } else { "()" }
    );
    support::rehash(
        &support::object(&[("id", &signature, &body)], "{}", "")
            .replace("=0.8", "=0.9")
            .replace("\"0.8\"", "\"0.9\""),
    )
}
fn scheduled(source: &Object, aliases: Option<&str>) -> String {
    let name = &source.function_order[0];
    let closure = source.identity().unwrap().closure_hashes[name]
        .clone()
        .unwrap();
    let mut schedule = support::json(&format!(
        r#"{{"bindings":{{"budget":[1,0,0,0],"closure_hash":"{closure}","epsilon":0,"inherited_controls":0,"params_hash":"{}","region":"{name}","scheduler":{{"name":"k91","version":"1"}},"target_hash":"{}","variant":"forward"}},"entries":[]}}"#,
        bennett_isa_ref::sha256_hex(b"[]"),
        "0".repeat(64)
    ));
    if let Some(aliases) = aliases {
        fields(fields(&mut schedule).get_mut("bindings").unwrap())
            .insert("token_aliases".into(), support::json(aliases));
    }
    format!(
        "{}\nsection schedule\n{}\n",
        source.text,
        schedule.canonical()
    )
}

#[test]
fn schedule_alias_slots_prepend_primary_only_for_oracles() {
    let action = Object::parse(
        &(BASE
            .split_once("section certificate\n")
            .unwrap()
            .0
            .trim_end()
            .to_string()
            + "\n"),
    )
    .unwrap();
    for (source, valid, invalid) in [(&action, "[]", "[0]"), (&oracle_source(false), "[0]", "[]")] {
        Object::parse(&scheduled(source, Some(valid)))
            .unwrap()
            .check_hashes()
            .unwrap();
        Object::parse(&scheduled(source, None)).unwrap(); // legacy token-free binding
        assert!(Object::parse(&scheduled(source, Some(invalid)))
            .unwrap_err()
            .to_string()
            .contains("K91"));
    }
    let source = oracle_source(true);
    for aliases in ["[0,0]", "[0,1]"] {
        Object::parse(&scheduled(&source, Some(aliases))).unwrap();
    }
    let error = Object::parse(&scheduled(&source, None)).unwrap_err();
    assert!(error.to_string().contains("K91"));
}

#[test]
fn a_schedule_certificate_cannot_reuse_equal_params_under_another_partition() {
    let original = certificate_object(Some("[0,0]"), 1);
    let object = Object::parse(&original).unwrap();
    let (source, raw) = original.split_once("section certificate\n").unwrap();
    let mut certificate = Json::parse(raw.trim()).unwrap();
    let binding = certificate.get("bindings").unwrap();
    let hash = binding.get("closure_hash").unwrap().string().unwrap();
    let params = bennett_isa_ref::sha256_hex(
        binding
            .get("invocation")
            .unwrap()
            .get("args")
            .unwrap()
            .canonical()
            .as_bytes(),
    );
    let schedule = support::json(&format!(
        r#"{{"bindings":{{"budget":[0,0,0,0],"closure_hash":"{hash}","epsilon":0,"inherited_controls":0,"params_hash":"{params}","region":"flip","scheduler":{{"name":"k91","version":"1"}},"target_hash":"{}","token_aliases":[0,0],"variant":"forward"}},"entries":[]}}"#,
        "0".repeat(64)
    ));
    fields(fields(&mut certificate).get_mut("bindings").unwrap()).insert(
        "schedule_hash".into(),
        Json::String(bennett_isa_ref::sha256_hex(schedule.canonical().as_bytes())),
    );
    let render = |c: &Json| {
        format!(
            "{}\n\nsection schedule\n{}\n\nsection certificate\n{}\n",
            source.trim_end(),
            schedule.canonical(),
            c.canonical()
        )
    };
    let scheduled = Object::parse(&render(&certificate)).unwrap();
    assert_eq!(
        scheduled.identity().unwrap().object_hash,
        object.identity().unwrap().object_hash
    );
    let invocation = fields(fields(&mut certificate).get_mut("bindings").unwrap())
        .get_mut("invocation")
        .unwrap();
    fields(invocation).insert("token_aliases".into(), support::json("[0,1]"));
    let error = Object::parse(&render(&certificate)).unwrap_err();
    assert!(
        error
            .to_string()
            .contains("invocation and schedule token_aliases differ"),
        "{error}"
    );
}

fn identity_pair_source() -> Object {
    let action = r#"{"abi":"0.9","args":["token","token"],"bounds":[],"in":[1],"kind":"perm_action","mem":[],"mut":[1,4],"tier":"q"}"#;
    let oracle =
        r#"{"abi":"0.9","args":[],"fault":4,"in":[1],"kind":"oracle","mem":[],"tgt":1,"tier":"q"}"#;
    support::rehash(&support::object(&[
        ("pair",action,"perm_action @pair (t:wire mut, f:wire[4] mut) (x:wire in) () (a:token, b:token) ()\n^entry():\noracle_call @id a (x) t f () ()\noracle_call @id b (x) t f () ()"),
        ("id",oracle,"oracle @id (x:wire in) (t:wire) (f:wire[4]) () ()\n^entry():\nlift.retval x")
    ],"{}", "").replace("=0.8","=0.9").replace("ptr_width=32","ptr_width=2"))
}
fn pair_schedule(source: &Object, aliases: &str, entries: &[Json]) -> String {
    let closure = source.identity().unwrap().closure_hashes["pair"]
        .clone()
        .unwrap();
    let params = bennett_isa_ref::sha256_hex(br#"[["1","0","0","0"],["1","0","0","0"]]"#);
    let schedule = support::json(&format!(
        r#"{{"bindings":{{"budget":[0,0,0,0],"closure_hash":"{closure}","epsilon":0,"inherited_controls":0,"params_hash":"{params}","region":"pair","scheduler":{{"name":"k91","version":"1"}},"target_hash":"{}","token_aliases":{aliases},"variant":"forward"}},"entries":{}}}"#,
        "0".repeat(64),
        Json::Array(entries.to_vec()).canonical()
    ));
    format!(
        "{}\nsection schedule\n{}\n",
        source.text,
        schedule.canonical()
    )
}
fn pair_cleanup(source: &Object) -> Json {
    let symbol = &source.identity().unwrap().interface_hashes["pair"];
    support::json(&format!(
        r#"{{"cleanup":{{"realisation":"recompute"}},"generated":0,"kind":"cleanup","path":[{{"instance":[],"iteration":[],"point":"entry:1","symbol":"{symbol}"}}],"phase":"*","step":"*"}}"#
    ))
}
#[test]
fn equal_identity_has_the_published_carrier_but_equal_tuples_alone_do_not() {
    let source = identity_pair_source();
    let entry = pair_cleanup(&source);
    let entries = [entry.clone(), entry];
    // A tie exists exactly on a real K65 carrier. Neither call's unitary
    // truth table nor equality of the two tuples determines this partition.
    for (aliases, carrier) in [("[0,0]", true), ("[0,1]", false)] {
        let result = Object::parse(&pair_schedule(&source, aliases, &entries));
        assert_eq!(result.is_err(), carrier, "{aliases}: {result:?}");
        if carrier {
            assert!(result.unwrap_err().to_string().contains("multiple maximal"));
        }
    }
}

#[test]
fn tuple_only_source_token_arguments_require_an_identity_binding() {
    let source = identity_pair_source();
    let args = bennett_isa_conformance::json::parse(
        r#"["t","f","x",["1","0","0","0"],["1","0","0","0"]]"#,
    )
    .unwrap();
    let result = source.expand_action_source(
        "pair",
        args.as_arr().unwrap(),
        &[("t", 1), ("f", 4), ("x", 1)],
        false,
    );
    assert!(
        result.is_err(),
        "source adapter admitted an unspecified partition"
    );
    assert!(result.unwrap_err().to_string().contains("K91"));
}

fn expand_pair(
    source: &Object,
    aliases: &[u64],
    adjoint: bool,
) -> Vec<bennett_isa_conformance::ref_language::Leaf> {
    let args = bennett_isa_conformance::json::parse(
        r#"["t","f","x",["1","0","0","0"],["1","0","0","0"]]"#,
    )
    .unwrap();
    source
        .expand_action_source_with_token_aliases(
            "pair",
            args.as_arr().unwrap(),
            &[("t", 1), ("f", 4), ("x", 1)],
            adjoint,
            aliases,
        )
        .unwrap()
}
#[test]
fn source_cleanup_decisions_require_the_actual_root_partition() {
    let source = identity_pair_source();
    let entry = pair_cleanup(&source);
    let default = expand_pair(&source, &[0, 0], false);
    let wrong = Object::parse(&pair_schedule(&source, "[0,1]", &[entry.clone()])).unwrap();
    let leaves = expand_pair(&wrong, &[0, 0], false);
    assert_eq!(
        leaves.len(),
        default.len(),
        "a different partition uses defaults"
    );
    let matched = Object::parse(&pair_schedule(&source, "[0,0]", &[entry])).unwrap();
    let leaves = expand_pair(&matched, &[0, 0], false);
    assert!(
        leaves.len() > default.len(),
        "same identity selects real recomputation"
    );
}

#[test]
fn source_captures_keep_identity_and_restore_all_sixty_four_basis_tuples() {
    use bennett_isa_conformance::{
        ref_catalog::Machine,
        ref_language::{invert_trace, permutation},
    };
    let source = identity_pair_source();
    for (labels, partition) in [("[0,0]", vec![0, 0]), ("[0,1]", vec![0, 1])] {
        let scheduled =
            Object::parse(&pair_schedule(&source, labels, &[pair_cleanup(&source)])).unwrap();
        for adjoint in [false, true] {
            let leaves = expand_pair(&scheduled, &partition, adjoint);
            for leaf in &leaves {
                let location = leaf.source.as_ref().unwrap();
                let root = &location.invocations[0];
                let tokens = root.tokens.as_ref().unwrap();
                assert!(
                    tokens.primary.is_none(),
                    "an action has no primary identity"
                );
                assert_eq!(
                    tokens.arguments["a"] == tokens.arguments["b"],
                    partition[0] == partition[1]
                );
                assert_eq!(root.binding.as_ref().unwrap().token_aliases, partition);
                if let Some(child) = location.invocations.get(1) {
                    assert_eq!(child.binding.as_ref().unwrap().token_aliases, [0]);
                    let token = child.tokens.as_ref().unwrap().primary.unwrap();
                    assert!(tokens.arguments.values().any(|id| *id == token));
                }
            }
            let mut inverse = leaves.clone();
            invert_trace(&mut inverse).unwrap();
            for (a, b) in inverse.iter().zip(leaves.iter().rev()) {
                assert_eq!(a.source, b.source);
            }
            let bundles = [("x", 1), ("t", 1), ("f", 4)];
            let machine = Machine::compile(&permutation(&leaves).unwrap(), &bundles).unwrap();
            let inv = Machine::compile(&permutation(&inverse).unwrap(), &bundles).unwrap();
            for m in [&machine, &inv] {
                let mut state = m.packed_state();
                for lane in 0..64 {
                    m.set_lane(&mut state, "x", (lane & 1) as u64, lane);
                    m.set_lane(&mut state, "t", ((lane >> 1) & 1) as u64, lane);
                    m.set_lane(&mut state, "f", (lane >> 2) as u64, lane);
                }
                let entry = state.clone();
                m.run_packed(&mut state, u64::MAX, false).unwrap();
                assert_eq!(
                    state, entry,
                    "{labels}, adjoint={adjoint}: complete identity"
                );
                m.run_packed(&mut state, u64::MAX, true).unwrap();
                assert_eq!(state, entry);
            }
        }
    }
}

#[test]
fn source_tuple_adapters_reject_malformed_bindings_before_construction() {
    let source = identity_pair_source();
    for token in [
        r#"[]"#,
        r#"["1","0","0"]"#,
        r#"[1,"0","0","0"]"#,
        r#"["01","0","0","0"]"#,
    ] {
        let args = bennett_isa_conformance::json::parse(&format!(
            r#"["t","f","x",{token},["1","0","0","0"]]"#
        ))
        .unwrap();
        assert!(source
            .expand_action_source_with_token_aliases(
                "pair",
                args.as_arr().unwrap(),
                &[("t", 1), ("f", 4), ("x", 1)],
                false,
                &[0, 0]
            )
            .is_err());
    }
    let args = bennett_isa_conformance::json::parse(
        r#"["t","f","x",["1","0","0","0"],["1","0","0","0"]]"#,
    )
    .unwrap();
    for labels in [vec![1, 1], vec![0, 2], vec![0], vec![]] {
        assert!(source
            .expand_action_source_with_token_aliases(
                "pair",
                args.as_arr().unwrap(),
                &[("t", 1), ("f", 4), ("x", 1)],
                false,
                &labels
            )
            .is_err());
    }
}

#[test]
fn a_token_free_oracle_uses_defaults_for_a_different_primary_budget() {
    use bennett_isa_ref::{Budget, OracleInput, OracleMachine};
    let source = oracle_source(false);
    let raw = scheduled(&source, Some("[0]"));
    let (body, raw) = raw.split_once("section schedule\n").unwrap();
    let mut schedule = Json::parse(raw.trim()).unwrap();
    fields(fields(&mut schedule).get_mut("bindings").unwrap())
        .insert("budget".into(), support::json("[2,0,0,0]"));
    let symbol = &source.identity().unwrap().interface_hashes["id"];
    let entry = support::json(&format!(
        r#"{{"gate":{{"epsilon_share":0,"realisation":"native"}},"generated":"*","kind":"gate","path":[{{"instance":[],"iteration":[],"point":"entry:0","symbol":"{symbol}"}}],"phase":"*","step":3}}"#
    ));
    fields(&mut schedule).insert("entries".into(), Json::Array(vec![entry.clone(), entry]));
    let object = Object::parse(&format!(
        "{body}section schedule\n{}\n",
        schedule.canonical()
    ))
    .unwrap();
    for x in 0..2 {
        let input = OracleInput::bits(&[x]);
        assert_eq!(
            object
                .run_oracle("id", &input, Budget::steps(3))
                .unwrap()
                .payload,
            x
        );
        let mut machine = OracleMachine::new(&object, "id", &input, Budget::steps(3)).unwrap();
        let before = machine.snapshot();
        for _ in 0..3 {
            machine.forward_step().unwrap();
        }
        assert_eq!(machine.outcome().unwrap().payload, x);
        for _ in 0..3 {
            machine.inverse_step().unwrap();
        }
        assert_eq!(machine.snapshot(), before);
    }
}

#[test]
fn tuple_only_native_oracle_arguments_require_an_identity_binding() {
    use bennett_isa_ref::{Argument, Budget, OracleInput, OracleMachine};
    let object = oracle_source(true);
    let mut input = OracleInput::bits(&[1]);
    input.args.push(Argument::Token(Budget::steps(1)));
    let result = object.run_oracle("id", &input, Budget::steps(1));
    assert!(
        result.is_err(),
        "native tuple adapter admitted unspecified primary/argument equality"
    );
    assert!(result.unwrap_err().to_string().contains("K91"));
    assert!(OracleMachine::new(&object, "id", &input, Budget::steps(1)).is_err());
}

#[test]
fn native_oracle_partitions_bind_the_primary_and_preserve_actual_handles() {
    use bennett_isa_ref::{Argument, Budget, OracleInput, OracleMachine};
    let object = oracle_source(true);
    for aliases in [&[0, 0][..], &[0, 1][..]] {
        for x in 0..2 {
            let mut input = OracleInput::bits(&[x]);
            input.args.push(Argument::Token(Budget::steps(1)));
            assert_eq!(
                object
                    .run_oracle_with_token_aliases("id", &input, Budget::steps(1), aliases)
                    .unwrap()
                    .payload,
                x
            );
            let mut machine = OracleMachine::new_with_token_aliases(
                &object,
                "id",
                &input,
                Budget::steps(1),
                aliases,
            )
            .unwrap();
            let before = machine.snapshot();
            machine.forward_step().unwrap();
            assert_eq!(machine.outcome().unwrap().payload, x);
            machine.inverse_step().unwrap();
            assert_eq!(machine.snapshot(), before);
        }
    }
    let primary = object.budget_token("id", Budget::steps(1)).unwrap();
    let distinct = object.budget_token("id", Budget::steps(1)).unwrap();
    for token in [&primary, &distinct] {
        let mut input = OracleInput::bits(&[1]);
        input.args.push(Argument::DeviceToken(token.clone()));
        assert_eq!(
            object
                .run_oracle_with_token("id", &input, &primary)
                .unwrap()
                .payload,
            1
        );
        assert!(
            object
                .run_oracle_with_token_aliases("id", &input, Budget::steps(1), &[0, 0])
                .is_ok(),
            "an unspecified primary can bind to the supplied handle"
        );
    }
    for labels in [vec![1, 1], vec![0, 2], vec![], vec![0]] {
        let mut input = OracleInput::bits(&[1]);
        input.args.push(Argument::Token(Budget::steps(1)));
        assert!(object
            .run_oracle_with_token_aliases("id", &input, Budget::steps(1), &labels)
            .is_err());
    }
    let mut unequal = OracleInput::bits(&[1]);
    unequal.args.push(Argument::Token(Budget::steps(2)));
    assert!(object
        .run_oracle_with_token_aliases("id", &unequal, Budget::steps(1), &[0, 0])
        .is_err());
}

fn scheduled_nested_oracle() -> Object {
    let outer = r#"{"abi":"0.9","args":["token"],"fault":4,"in":[1],"kind":"oracle","mem":[],"tgt":1,"tier":"q"}"#;
    let inner =
        r#"{"abi":"0.9","args":[],"fault":4,"in":[1],"kind":"oracle","mem":[],"tgt":1,"tier":"q"}"#;
    let source=support::rehash(&support::object(&[
        ("outer",outer,"oracle @outer (x:wire in) (t:wire) (f:wire[4]) () (a:token)\nregs { r:reg[1], fr:reg[4] }\n^entry():\nlift.oracle_call @inner a (x) r fr () ()\nlift.retval r"),
        ("inner",inner,"oracle @inner (x:wire in) (t:wire) (f:wire[4]) () ()\n^entry():\nlift.retval x")
    ],"{}", "").replace("=0.8","=0.9"));
    let id = source.identity().unwrap();
    let root = id.closure_hashes["outer"].as_ref().unwrap();
    let child = &id.interface_hashes["inner"];
    let params = bennett_isa_ref::sha256_hex(br#"[["3","0","0","0"]]"#);
    let entry = support::json(&format!(
        r#"{{"gate":{{"epsilon_share":0,"realisation":"native"}},"generated":"*","kind":"gate","path":[{{"call_index":0,"instance":[],"iteration":[],"point":"entry:0","symbol":"{root}"}},{{"instance":[],"iteration":[],"point":"entry:0","symbol":"{child}"}}],"phase":"*","step":3}}"#
    ));
    let schedule = support::json(&format!(
        r#"{{"bindings":{{"budget":[3,0,0,0],"closure_hash":"{root}","epsilon":0,"inherited_controls":0,"params_hash":"{params}","region":"outer","scheduler":{{"name":"k91","version":"1"}},"target_hash":"{}","token_aliases":[0,0],"variant":"forward"}},"entries":{}}}"#,
        "0".repeat(64),
        Json::Array(vec![entry.clone(), entry]).canonical()
    ));
    Object::parse(&format!(
        "{}\nsection schedule\n{}\n",
        source.text,
        schedule.canonical()
    ))
    .unwrap()
}
#[test]
fn native_schedule_dispatch_compares_the_actual_primary_argument_partition() {
    use bennett_isa_ref::{Argument, Budget, OracleInput, OracleMachine};
    let object = scheduled_nested_oracle();
    for x in 0..2 {
        let mut input = OracleInput::bits(&[x]);
        input.args.push(Argument::Token(Budget::steps(3)));
        let error = object
            .run_oracle_with_token_aliases("outer", &input, Budget::steps(3), &[0, 0])
            .unwrap_err();
        assert!(error.to_string().contains("multiple maximal"));
        assert!(OracleMachine::new_with_token_aliases(
            &object,
            "outer",
            &input,
            Budget::steps(3),
            &[0, 0]
        )
        .is_err());
        assert_eq!(
            object
                .run_oracle_with_token_aliases("outer", &input, Budget::steps(3), &[0, 1])
                .unwrap()
                .payload,
            x
        );
        let mut machine = OracleMachine::new_with_token_aliases(
            &object,
            "outer",
            &input,
            Budget::steps(3),
            &[0, 1],
        )
        .unwrap();
        let before = machine.snapshot();
        for _ in 0..3 {
            machine.forward_step().unwrap();
        }
        assert_eq!(machine.outcome().unwrap().payload, x);
        for _ in 0..3 {
            machine.inverse_step().unwrap();
        }
        assert_eq!(machine.snapshot(), before);
    }
    let primary = object.budget_token("outer", Budget::steps(3)).unwrap();
    let distinct = object.budget_token("inner", Budget::steps(3)).unwrap();
    let mut input = OracleInput::bits(&[1]);
    input.args.push(Argument::DeviceToken(primary.clone()));
    assert!(object
        .run_oracle_with_token("outer", &input, &primary)
        .is_err());
    input.args[0] = Argument::DeviceToken(distinct);
    assert_eq!(
        object
            .run_oracle_with_token("outer", &input, &primary)
            .unwrap()
            .payload,
        1
    );
}

#[test]
fn public_cli_q_invocations_bind_aliases_for_run_reverse_and_step_check() {
    use std::{path::PathBuf, process::Command};
    let dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join(".tmp");
    std::fs::create_dir_all(&dir).unwrap();
    let path = dir.join("k91-native-cli.bisa");
    std::fs::write(&path, oracle_source(true).text).unwrap();
    for aliases in ["[0,0]", "[0,1]"] {
        for command in ["run-oracle", "reverse", "step-check"] {
            let mut cmd = Command::new(env!("CARGO_BIN_EXE_bennett-isa-ref"));
            cmd.arg(command).arg(&path).arg("id").args([
                "--budget",
                "1,0,0,0",
                "--arg",
                "token:1,0,0,0",
                "--token-aliases",
                aliases,
            ]);
            if command == "step-check" {
                cmd.args(["--exhaustive", "--max-bits", "1"]);
            } else {
                cmd.args(["--input", "1"]);
            }
            let output = cmd.output().unwrap();
            assert!(
                output.status.success(),
                "{command}/{aliases}: {}",
                String::from_utf8_lossy(&output.stderr)
            );
            let json = Json::parse(std::str::from_utf8(&output.stdout).unwrap().trim()).unwrap();
            if command == "run-oracle" {
                assert_eq!(json.get("payload").unwrap().uint().unwrap(), 1);
            }
            if command == "reverse" {
                assert_eq!(json.get("equals_entry").unwrap(), &Json::Bool(true));
            }
        }
    }
    for aliases in [
        None,
        Some("[1,1]"),
        Some("[0,2]"),
        Some("[0]"),
        Some("[-1,0]"),
    ] {
        let mut cmd = Command::new(env!("CARGO_BIN_EXE_bennett-isa-ref"));
        cmd.arg("run-oracle").arg(&path).arg("id").args([
            "--input",
            "1",
            "--budget",
            "1,0,0,0",
            "--arg",
            "token:1,0,0,0",
        ]);
        if let Some(labels) = aliases {
            cmd.args(["--token-aliases", labels]);
        }
        let output = cmd.output().unwrap();
        assert_eq!(output.status.code(), Some(1));
        assert!(output.stdout.is_empty());
        assert!(String::from_utf8_lossy(&output.stderr).contains("E_ARG"));
    }
    std::fs::write(&path, identity_pair_source().text).unwrap();
    for aliases in ["[0,0]", "[0,1]"] {
        for command in ["run-action", "reverse"] {
            let output = Command::new(env!("CARGO_BIN_EXE_bennett-isa-ref"))
                .arg(command)
                .arg(&path)
                .arg("pair")
                .args([
                    "--mut",
                    "1,7",
                    "--in",
                    "1",
                    "--arg",
                    "token:1,0,0,0",
                    "--arg",
                    "token:1,0,0,0",
                    "--token-aliases",
                    aliases,
                ])
                .output()
                .unwrap();
            assert!(
                output.status.success(),
                "{command}/{aliases}: {}",
                String::from_utf8_lossy(&output.stderr)
            );
            let json = Json::parse(std::str::from_utf8(&output.stdout).unwrap().trim()).unwrap();
            if command == "reverse" {
                assert_eq!(json.get("equals_entry").unwrap(), &Json::Bool(true));
            }
        }
    }
}

#[test]
fn controlled_native_oracles_match_the_actual_inherited_control_count() {
    use bennett_isa_ref::{Argument, Budget, QuantumBindings, QuantumState};
    let source = scheduled_nested_oracle();
    let (body, schedule) = source.text.split_once("section schedule\n").unwrap();
    let mut symbols = source.section("symbols").unwrap().clone();
    fields(&mut symbols).insert("2".into(),support::json(r#"{"interface_hash":"0000000000000000000000000000000000000000000000000000000000000000","kind":"perm_action","name":"wrap","signature":{"abi":"0.9","args":["token","token"],"bounds":[],"in":[1,1],"kind":"perm_action","mem":[],"mut":[1,4],"tier":"q"}}"#));
    let mut lines = body.lines().map(str::to_string).collect::<Vec<_>>();
    let index = lines.iter().position(|s| s == "section symbols").unwrap() + 1;
    lines[index] = symbols.canonical();
    let text=format!("{}\nperm_action @wrap (t:wire mut, f:wire[4] mut) (x:wire in, c:wire in) () (p:token, a:token) ()\n^entry():\nctl c oracle_call @outer p (x) t f () (a)\n\nsection schedule\n{schedule}",lines.join("\n").trim_end());
    let object = support::rehash(&text);
    for bits in 0..128u128 {
        let mut state = QuantumState::new();
        let wires = state.allocate(7).unwrap();
        for (i, w) in wires.iter().enumerate() {
            if bits >> i & 1 != 0 {
                state.gate("x", &[*w], None, &[]).unwrap();
            }
        }
        let mut binding = QuantumBindings::default();
        binding.bundles.insert("t".into(), vec![wires[0]]);
        binding.bundles.insert("f".into(), wires[1..5].to_vec());
        binding.bundles.insert("x".into(), vec![wires[5]]);
        binding.bundles.insert("c".into(), vec![wires[6]]);
        for n in ["p", "a"] {
            binding
                .args
                .insert(n.into(), Argument::Token(Budget::steps(3)));
        }
        let entry = state.clone();
        object
            .execute_action_with_token_aliases("wrap", &mut state, &binding, false, &[], &[0, 0])
            .unwrap();
        assert_eq!(
            state.read_basis(&wires).unwrap(),
            bits ^ ((bits >> 5 & 1) & (bits >> 6 & 1))
        );
        object
            .execute_action_with_token_aliases("wrap", &mut state, &binding, true, &[], &[0, 0])
            .unwrap();
        assert_eq!(state, entry);
    }
}

#[test]
fn schedule_reader_checks_canonical_aliases_and_keeps_the_closed_schema() {
    let object = oracle_source(true);
    let original = scheduled(&object, Some("[0,1]"));
    let parsed = Object::parse(&original).unwrap();
    assert_eq!(
        parsed
            .section("schedule")
            .unwrap()
            .get("bindings")
            .unwrap()
            .get("token_aliases")
            .unwrap(),
        &support::json("[0,1]")
    );
    for labels in ["[1,1]", "[0,2]", "[0]", "[]", "[-1,0]", "[0,0.5]"] {
        let text = scheduled(&object, Some(labels));
        let error = Object::parse(&text).unwrap_err();
        assert!(error.to_string().contains("K91"), "{labels}: {error}");
    }
    let mut schedule = parsed.section("schedule").unwrap().clone();
    fields(fields(&mut schedule).get_mut("bindings").unwrap())
        .insert("token_alias".into(), support::json("[0,1]"));
    let error = Object::parse(&format!(
        "{}\nsection schedule\n{}\n",
        object.text,
        schedule.canonical()
    ))
    .unwrap_err();
    assert!(error.to_string().contains("unknown"), "{error}");
}

#[test]
fn alias_metadata_is_versioned_and_does_not_widen_08_readers() {
    let original = certificate_object(Some("[0,1]"), 1);
    let source = original.split_once("section certificate\n").unwrap().0;
    let legacy = support::rehash(
        &(source.trim_end().to_string() + "\n")
            .replace("=0.9", "=0.8")
            .replace("\"0.9\"", "\"0.8\""),
    );
    let with_aliases = scheduled(&legacy, Some("[0,1]"));
    let error = Object::parse(&with_aliases).unwrap_err();
    assert!(error.to_string().contains("token_aliases"), "{error}");
    Object::parse(&scheduled(&legacy, None))
        .unwrap()
        .check_hashes()
        .unwrap();
}
````

## `reference-interpreter/tests/r1_certificates.rs` (895 lines)

````rust
//! Council round 1: codex B14 (claim route), B16, muse B7 (typed metadata and
//! checked claims).
mod support;
use bennett_isa_ref::{json::Json, ClaimVerdict, Object};
use support::json;

const INC: &str = include_str!("fixtures/inc8.bisa");

fn rejects(text: &str, rule: &str) {
    match Object::parse(text) {
        Err(e) => assert!(e.to_string().contains(rule), "{e} must cite {rule}"),
        Ok(_) => panic!("malformed metadata accepted"),
    }
}
/// A perm_action `a` borrowing one wire around a swap frame over t[0..n),
/// and an identity reference `id` of the same signature.
fn swap_frame(n: u64) -> String {
    let sig = format!(
        r#"{{"abi":"0.8","args":[],"bounds":[],"in":[1],"kind":"perm_action","mem":[],"mut":[{n}],"tier":"q"}}"#
    );
    let forward: Vec<String> = (0..n).map(|i| format!("swap b t[{i}]")).collect();
    let back: Vec<String> = (0..n).rev().map(|i| format!("swap b t[{i}]")).collect();
    let a = format!(
        "perm_action @a (t:wire[{n}] mut) (x:wire in) () () ()\n^entry():\nb = qborrow any 1\n{}\nqreturn b",
        [forward, back].concat().join("\n")
    );
    let id = format!(
        "perm_action @id (t:wire[{n}] mut) (x:wire in) () () ()\n^entry():\nx t[0]\nx t[0]"
    );
    support::rehash(&support::object(
        &[("a", &sig, &a), ("id", &sig, &id)],
        "{}",
        "",
    ))
    .text
}
fn certificate(text: &str, n: u64, claims: &str, borrow_frames: &str) -> String {
    let o = Object::parse(text).unwrap();
    let identity = o.identity().unwrap();
    let a = identity.closure_hashes["a"].clone().unwrap();
    let id = identity.closure_hashes["id"].clone().unwrap();
    let signature = o.functions["a"].signature().canonical();
    let claims = claims.replace("ID", &id);
    let bounds = format!("{:?}", o.functions["a"].bounds);
    let cert = json(&format!(
        r#"{{"versions":{{"isa":"0.8","object":"0.8","launch":"0.8","sched":"0.8","cert":"0.8","coverage":"0.8","target":"0.8"}},"bindings":{{"object_hash":"{}","interface_hash":"{}","closure_hash":"{a}","reference_program_hash":"{}","dialect_mapping_version":"test.1","target_hash":"{}"}},"producer":{{"name":"tests","version":"1","materialisation":{{"llvm_version":"none","pipeline":"none","normaliser_version":"1"}}}},"regions":{{"{a}":{{"kind":"perm_action","signature":{signature},"bounds":{bounds},"frame":{{"interface":[{{"role":"mut","width":{n},"class":"any"}},{{"role":"in","width":1,"class":"any"}}],"scratch":{{}},"retained_history":0,"borrow":{{"any":1}},"scheme_ancillae":{{}}}},"resources":{{}},"gates_used":{{}},"claims":[{claims}],"verification":{{"oracle":null,"borrow_frames":[{borrow_frames}],"inverse_pairs":[],"unitary":[],"channel":[],"fault_rate":{{"domain":{{"bundles":[],"borrowed":[],"regions":[]}},"faults_by_code":{{}},"undefined_excluded":0,"layout_dependent_excluded":0}}}},"cleanup":{{}},"error":{{}},"definedness_assumptions":[]}}}},"composition":{{"multiplicities":{{}},"epsilon_total":{{"diamond":0}},"method":"sum_over_multiplicities"}}}}"#,
        identity.object_hash,
        identity.interface_hashes["a"],
        identity.interface_hashes["a"],
        "3".repeat(64)
    ));
    format!("{text}\nsection certificate\n{}\n", cert.canonical())
}
fn claim(n: u64, t_hi: &str, b_hi: u32, expected: &str) -> String {
    format!(
        r#"{{"kind":"exhaustive","label":"proof","domain":{{"bundles":[{{"name":"t","width":{n},"lo":0,"hi":{t_hi}}},{{"name":"x","width":1,"lo":0,"hi":1}}],"borrowed":[{{"name":"b","width":1,"lo":0,"hi":{b_hi}}}],"regions":[]}},"expected":{expected}}}"#
    )
}

#[test]
fn b14_checked_borrow_claim_and_altered_or_incomplete_claims() {
    let n = 4;
    let text = swap_frame(n);
    let good = certificate(&text, n, &claim(n, "15", 1, r#"{"program":"ID"}"#), "0");
    let o = Object::parse(&good).unwrap();
    let reports = o.verify_certificate().unwrap().claims;
    assert_eq!(reports.len(), 1);
    assert_eq!(reports[0].verdict, ClaimVerdict::Proof);
    // Altered: the expected program is the frame itself... replaced by a
    // table with one wrong row (2^6 rows: t fastest-last order).
    let mut rows = Vec::new();
    for t in 0..16u32 {
        for x in 0..2u32 {
            for b in 0..2u32 {
                rows.push(format!("[{t},{x},{b}]"));
            }
        }
    }
    let table = format!(r#"{{"table":[{}]}}"#, rows.join(","));
    let exact = certificate(&text, n, &claim(n, "15", 1, &table), "0");
    assert_eq!(
        Object::parse(&exact)
            .unwrap()
            .verify_certificate()
            .unwrap()
            .claims[0]
            .verdict,
        ClaimVerdict::Proof
    );
    let wrong = table.replacen("[0,0,0]", "[1,0,0]", 1);
    let altered = certificate(&text, n, &claim(n, "15", 1, &wrong), "0");
    let e = Object::parse(&altered)
        .unwrap()
        .verify_certificate()
        .unwrap_err()
        .to_string();
    assert!(e.contains("§12.1"), "{e}");
    // Incomplete: t only up to 7, so the domain is not D: evidence, not proof,
    // and therefore not a borrow_frames proof (§5.6, §12.2).
    let incomplete = certificate(&text, n, &claim(n, "7", 1, r#"{"program":"ID"}"#), "0");
    let e = Object::parse(&incomplete)
        .unwrap()
        .verify_certificate()
        .unwrap_err()
        .to_string();
    assert!(e.contains("§5.6"), "{e}");
    // A borrow claim must range over the borrowed bundle.
    let no_borrowed = claim(n, "15", 1, r#"{"program":"ID"}"#)
        .replace(r#"[{"name":"b","width":1,"lo":0,"hi":1}]"#, "[]");
    let e = Object::parse(&certificate(&text, n, &no_borrowed, "0"))
        .unwrap()
        .verify_certificate()
        .unwrap_err()
        .to_string();
    assert!(e.contains("§5.6"), "{e}");
}
#[test]
#[ignore = "the codex B14 17-wire frame with its 2^18-element claim; run with --ignored"]
fn b14_seventeen_wire_frame_with_checked_claim() {
    let n = 16;
    let text = swap_frame(n);
    let good = certificate(&text, n, &claim(n, "65535", 1, r#"{"program":"ID"}"#), "0");
    let reports = Object::parse(&good)
        .unwrap()
        .verify_certificate()
        .unwrap()
        .claims;
    assert_eq!(reports[0].verdict, ClaimVerdict::Proof);
}

fn schedule(field: &str, value: &str) -> Json {
    let base = format!(
        r#"{{"bindings":{{"budget":[3,0,0,0],"closure_hash":"8ce5e64f15830d8e596ba9b4861def6565dd567b5804300f427d8b9566d5be93","epsilon":0,"expansion":{{"hash":"{}","name":"ref","version":"0.8"}},"inherited_controls":0,"params_hash":"{}","region":"inc8","scheduler":{{"name":"test","version":"1"}},"target_hash":"{}","variant":"forward"}},"entries":[{{"generated":"*","kind":"start","path":[{{"iteration":[],"point":"entry:0","symbol":"8ce5e64f15830d8e596ba9b4861def6565dd567b5804300f427d8b9566d5be93"}}],"phase":"fwd","start":{{"time":0}},"step":1}}]}}"#,
        "1".repeat(64),
        "2".repeat(64),
        "3".repeat(64)
    );
    let mut s = json(&base);
    let Json::Object(top) = &mut s else { panic!() };
    match field {
        "" => {}
        "budget" | "variant" => {
            let Json::Object(b) = top.get_mut("bindings").unwrap() else {
                panic!()
            };
            b.insert(field.into(), json(value));
        }
        _ => {
            let Json::Array(entries) = top.get_mut("entries").unwrap() else {
                panic!()
            };
            let Json::Object(e) = &mut entries[0] else {
                panic!()
            };
            if field == "time" {
                e.insert("start".into(), json(&format!(r#"{{"time":{value}}}"#)));
            } else if field == "path" {
                e.insert("path".into(), json(value));
            } else {
                e.insert(field.into(), json(value));
            }
        }
    }
    s
}
#[test]
fn b16_schedule_values_are_typed() {
    let with = |s: &Json| format!("{INC}\nsection schedule\n{}\n", s.canonical());
    Object::parse(&with(&schedule("", ""))).unwrap();
    for (field, value) in [
        ("budget", "[3,true,0,0]"),
        ("budget", "[3,null,0,0]"),
        ("budget", "[3,-1,0,0]"),
        ("phase", "\"garbage\""),
        (
            "path",
            r#"[{"iteration":[],"point":7,"symbol":"8ce5e64f15830d8e596ba9b4861def6565dd567b5804300f427d8b9566d5be93"}]"#,
        ),
        (
            "path",
            r#"[{"iteration":"all","point":"entry:0","symbol":"8ce5e64f15830d8e596ba9b4861def6565dd567b5804300f427d8b9566d5be93"}]"#,
        ),
        ("time", "-1"),
        ("variant", "\"a:b\""),
    ] {
        rejects(&with(&schedule(field, value)), "§");
    }
}
#[test]
fn b16_muse_b7_certificate_values_and_claims_are_typed() {
    let text = swap_frame(2);
    let good = certificate(&text, 2, &claim(2, "3", 1, r#"{"program":"ID"}"#), "0");
    Object::parse(&good).unwrap();
    for (from, to) in [
        (
            r#""versions":{"cert":"0.8""#,
            r#""versions":false,"x":{"cert":"0.8""#,
        ),
        (
            r#""dialect_mapping_version":"test.1""#,
            r#""dialect_mapping_version":false"#,
        ),
        (r#""multiplicities":{}"#, r#""multiplicities":false"#),
        (
            r#""method":"sum_over_multiplicities""#,
            r#""method":"nonsense""#,
        ),
        (
            r#""epsilon_total":{"diamond":0}"#,
            r#""epsilon_total":false"#,
        ),
        (r#""claims":[{"#, r#""claims":[{"bogus":1},{"#),
        (r#""scratch":{}"#, r#""scratch":{},"unknown":1"#),
        (r#""gates_used":{}"#, r#""gates_used":{"x":{"count":-1}}"#),
    ] {
        let bad = good.replacen(from, to, 1);
        assert_ne!(bad, good, "{from}");
        // Re-canonicalise so the test reaches the schema, not the JCS check.
        let line = bad.lines().last().unwrap();
        let fixed = match Json::parse(line) {
            Ok(j) => bad.replace(line, &j.canonical()),
            Err(_) => bad,
        };
        rejects(&fixed, "§");
    }
}

#[test]
fn r2_interval_claim_diagnostics_name_deliverable_eleven() {
    let text = swap_frame(1);
    let o = Object::parse(&text).unwrap();
    let closure = o.identity().unwrap().closure_hashes["a"].clone().unwrap();
    for kind in ["numerical", "channel"] {
        let metric = if kind == "channel" {
            "diamond"
        } else {
            "operator_norm"
        };
        let dual = if kind == "channel" {
            ",\"dual\":[]"
        } else {
            ""
        };
        let claim = format!(
            r#"{{"kind":"{kind}","subject":{{"closure_hash":"{closure}","variant":"fwd","inherited_controls":0,"schedule_hash":"{}"}},"metric":"{metric}","precision_bits":128,"bound":0{dual}}}"#,
            "4".repeat(64)
        );
        let o = Object::parse(&certificate(&text, 1, &claim, "")).unwrap();
        match o.verify_claim(&closure, 0).unwrap() {
            ClaimVerdict::Unverified(why) => assert!(why.contains("deliverable 11"), "{why}"),
            other => panic!("staged interval checker cannot prove a claim: {other:?}"),
        }
    }
}

fn sol_translation_object(gates: &str, nested: bool) -> String {
    let sig = r#"{"abi":"0.8","args":[],"bounds":[],"in":[1],"kind":"perm_action","mem":[],"mut":[1],"tier":"q"}"#;
    let asig = if nested {
        sig.replace("\"bounds\":[]", "\"bounds\":[2]")
    } else {
        sig.into()
    };
    let regs = if nested { "regs {  } bounds {2}\n" } else { "" };
    let body = format!("perm_action @a (t:wire mut) (p:wire in) () () ()\n{regs}^entry():\nb = qborrow any 1\n{}\nqreturn b", if nested { format!("qloop 2 {{\n{gates}\n}}") } else { gates.into() });
    support::rehash(&support::object(
        &[
            ("a", &asig, &body),
            (
                "id",
                sig,
                "perm_action @id (u:wire mut) (v:wire in) () () ()\n^entry():\nx u\nx u",
            ),
        ],
        "{}",
        "",
    ))
    .text
}
fn sol_translation_claim(text: &str, start: u32, end: u32, v: u32, w: u32, b: &str) -> String {
    let o = Object::parse(text).unwrap();
    let h = &o.identity().unwrap().interface_hashes["a"];
    format!(
        r#"{{"kind":"structural","rule":"translation_lemma","subclaims":[],"witness":{{"V":[["{h}","entry",{v}]],"W":[["{h}","entry",{w}]],"X":["p"],"B":["{b}"],"frame":[["{h}","entry",{start}],["{h}","entry",{end}]]}}}}"#
    )
}
fn sol_assert_translation(text: &str, claim: &str, valid: bool) {
    let o = Object::parse(&certificate(text, 1, claim, "")).unwrap();
    let h = o.identity().unwrap().closure_hashes["a"].clone().unwrap();
    for verdict in [
        o.verify_claim(&h, 0),
        o.verify_certificate().map(|r| r.claims[0].verdict.clone()),
    ] {
        if valid {
            assert_eq!(verdict.unwrap(), ClaimVerdict::Proof);
        } else {
            let e = verdict
                .expect_err("false structural frame proved")
                .to_string();
            assert!(e.contains("§5.6") || e.contains("§12.1"), "{e}");
        }
    }
}
#[test]
fn sol_r4_b02_translation_claim_must_prove_its_complete_named_frame() {
    // Full frame: b ^= p; t ^= b; b ^= p; t ^= b => (t ^= p, b unchanged).
    // Truncated frame: b ^= p; t ^= b => b dirty and t dependent on entry b.
    let text = sol_translation_object("cx p b\ncx b t\ncx p b\ncx b t", false);
    for (start, end, v, w, valid) in [
        (1, 2, 1, 2, false),
        (1, 4, 1, 2, true),
        (99, 100, 1, 2, false),
        (4, 1, 1, 2, false),
        (1, 4, 99, 2, false),
        (1, 4, 1, 3, false),
    ] {
        sol_assert_translation(
            &text,
            &sol_translation_claim(&text, start, end, v, w, "b"),
            valid,
        );
    }
    sol_assert_translation(&text, &sol_translation_claim(&text, 1, 4, 1, 2, "p"), false);
    // The object itself is still valid, but its first four gates have a
    // changed second W; later gates complete the actual independent circuit.
    let changed = sol_translation_object("cx p b\ncx b t\ncx p b\nx t\ncx b t\nx t", false);
    sol_assert_translation(
        &changed,
        &sol_translation_claim(&changed, 1, 4, 1, 2, "b"),
        false,
    );
}
#[test]
fn sol_r4_b02_translation_claim_uses_nested_line_ordinals() {
    // qborrow=0, qloop=1, nested gates=2..5, qreturn=6. Prove the
    // complete body frame, uniformly for both loop iterations.
    let text = sol_translation_object("cx p b\ncx b t\ncx p b\ncx b t", true);
    sol_assert_translation(&text, &sol_translation_claim(&text, 2, 5, 2, 3, "b"), true);
    sol_assert_translation(&text, &sol_translation_claim(&text, 2, 3, 2, 3, "b"), false);
}

#[test]
fn sol_r4_b02_translation_frame_rejects_omissions_and_checks_reverse_order() {
    let gates = "x b\ncx p b\ncx b t\ncx p b\nx b\ncx b t";
    let text = sol_translation_object(gates, false);
    let mut claim = json(&sol_translation_claim(&text, 1, 6, 1, 3, "b"));
    let h = Object::parse(&text)
        .unwrap()
        .identity()
        .unwrap()
        .interface_hashes["a"]
        .clone();
    let Json::Object(c) = &mut claim else {
        panic!()
    };
    let Json::Object(w) = c.get_mut("witness").unwrap() else {
        panic!()
    };
    w.insert(
        "V".into(),
        json(&format!(r#"[["{h}","entry",1],["{h}","entry",2]]"#)),
    );
    sol_assert_translation(&text, &claim.canonical(), true);
    // Skip x b between the named V and W; the remaining four gates happen
    // to form a valid independent circuit, but the named frame contains six.
    sol_assert_translation(&text, &sol_translation_claim(&text, 1, 6, 2, 3, "b"), false);
    let twice = sol_translation_object(
        "cx p b\ncx b t\ncx p b\ncx b t\ncx p b\ncx b t\ncx p b\ncx b t",
        false,
    );
    sol_assert_translation(
        &twice,
        &sol_translation_claim(&twice, 1, 4, 1, 2, "b"),
        false,
    );
}

fn sol_positional_object(region: bool, reference: &str) -> String {
    let mem = if region {
        r#"[{"A":1,"W":1,"role":"mut"}]"#
    } else {
        "[]"
    };
    let sig = format!(
        r#"{{"abi":"0.8","args":[],"bounds":[],"in":[1],"kind":"perm_action","mem":{mem},"mut":[1],"tier":"q"}}"#
    );
    let a = format!(
        "perm_action @a (t:wire mut) (p:wire in) ({}) () ()\n^entry():\nx t\nx t",
        if region { "m:region[1,1] mut" } else { "" }
    );
    let id = format!(
        "perm_action @id (u:wire mut) (v:wire in) ({}) () ()\n^entry():\n{reference}",
        if region { "n:region[1,1] mut" } else { "" }
    );
    support::rehash(&support::object(&[("a",&sig,&a),("id",&sig,&id)],"{}",if region { "\nsection layout\n{\"A_tab\":0,\"H\":0,\"S_cells\":0,\"globals\":{},\"heap_base\":1,\"heap_limit_max\":0,\"interface_regions\":{},\"null_size\":1,\"ptr_width\":32}\n" } else {""})).text
}
fn sol_positional_claim(regions: &str, borrowed: &str, bundles: &str) -> String {
    format!(
        r#"{{"kind":"exhaustive","label":"proof","domain":{{"bundles":[{bundles}],"borrowed":[{borrowed}],"regions":[{regions}]}},"expected":{{"program":"ID"}}}}"#
    )
}
const SOL_BUNDLES: &str =
    r#"{"name":"t","width":1,"lo":0,"hi":1},{"name":"p","width":1,"lo":0,"hi":1}"#;
fn sol_positional_verdict(text: &str, claim: &str) -> Result<ClaimVerdict, bennett_isa_ref::Error> {
    let o = Object::parse(&certificate(text, 1, claim, "")).unwrap();
    let h = o.identity().unwrap().closure_hashes["a"].clone().unwrap();
    let v = o.verify_claim(&h, 0)?;
    assert_eq!(o.verify_certificate().unwrap().claims[0].verdict, v);
    Ok(v)
}
#[test]
fn sol_r4_b03_expected_program_uses_signature_positions_for_renamed_bundles() {
    // Independently: both bodies are identity on 00,01,10,11. Local names
    // t,p versus u,v have no ABI significance (§9.4).
    let text = sol_positional_object(false, "x u\nx u");
    let claim = sol_positional_claim("", "", SOL_BUNDLES);
    assert_eq!(
        sol_positional_verdict(&text, &claim).unwrap(),
        ClaimVerdict::Proof
    );
    // Permuting domain enumeration order must not permute interface slots.
    let reverse = sol_positional_claim(
        "",
        "",
        r#"{"name":"p","width":1,"lo":0,"hi":1},{"name":"t","width":1,"lo":0,"hi":1}"#,
    );
    assert_eq!(
        sol_positional_verdict(&text, &reverse).unwrap(),
        ClaimVerdict::Proof
    );
    // Borrowed pool entries follow their domain order, independently of the
    // expected program's local names. A truly omitted input stays zero.
    let borrowed = r#"{"name":"z","width":1,"lo":0,"hi":1},{"name":"b","width":2,"lo":0,"hi":3}"#;
    assert_eq!(
        sol_positional_verdict(&text, &sol_positional_claim("", borrowed, SOL_BUNDLES)).unwrap(),
        ClaimVerdict::Proof
    );
    let partial = sol_positional_claim("", "", r#"{"name":"t","width":1,"lo":0,"hi":1}"#);
    assert_eq!(
        sol_positional_verdict(&text, &partial).unwrap(),
        ClaimVerdict::Evidence { elements: 2 }
    );
    let wrong = sol_positional_object(false, "x u");
    let e = sol_positional_verdict(&wrong, &claim)
        .unwrap_err()
        .to_string();
    assert!(
        e.contains("§12.1") && e.contains("differs from the expected program"),
        "{e}"
    );
}
#[test]
fn sol_r4_b03_expected_program_maps_renamed_region_cells_positionally() {
    // 2 interface bits and 2 independent region cells => 16 identical final
    // tuples. Changing only reference memory must still be detected.
    let text = sol_positional_object(true, "x u\nx u");
    let claim = sol_positional_claim(r#"{"name":"m","cells":"all"}"#, "", SOL_BUNDLES);
    assert_eq!(
        sol_positional_verdict(&text, &claim).unwrap(),
        ClaimVerdict::Proof
    );
    let partial = sol_positional_claim(
        r#"{"name":"m","cells":[{"index":1,"lo":0,"hi":1}]}"#,
        "",
        SOL_BUNDLES,
    );
    assert_eq!(
        sol_positional_verdict(&text, &partial).unwrap(),
        ClaimVerdict::Evidence { elements: 8 }
    );
    let wrong = sol_positional_object(true, "qstore n v u");
    assert!(sol_positional_verdict(&wrong, &claim)
        .unwrap_err()
        .to_string()
        .contains("§12.1"));
}

#[test]
fn sol_r4_b03_positions_distinguish_same_width_slots_and_crossed_names() {
    let sig = r#"{"abi":"0.8","args":[],"bounds":[],"in":[1],"kind":"perm_action","mem":[],"mut":[1,1],"tier":"q"}"#;
    // Rename by crossing existing local names. Both maps are (t,u,p) ->
    // (t XOR p,u,p); a name-based correspondence would exchange mut and in.
    let a = "perm_action @a (t:wire mut, u:wire mut) (p:wire in) () () ()\n^entry():\ncx p t";
    let id = "perm_action @id (p:wire mut, t:wire mut) (u:wire in) () () ()\n^entry():\ncx u p";
    let text = support::rehash(&support::object(
        &[("a", sig, a), ("id", sig, id)],
        "{}",
        "",
    ))
    .text;
    let claim = sol_positional_claim(
        "",
        "",
        r#"{"name":"u","width":1,"lo":0,"hi":1},{"name":"p","width":1,"lo":0,"hi":1},{"name":"t","width":1,"lo":0,"hi":1}"#,
    );
    assert_eq!(
        sol_positional_verdict(&text, &claim).unwrap(),
        ClaimVerdict::Proof
    );
    // Writing the second mutable slot instead must fail the full-tuple check.
    let wrong = support::rehash(&support::object(
        &[("a", sig, a), ("id", sig, &id.replace("cx u p", "cx u t"))],
        "{}",
        "",
    ))
    .text;
    assert!(sol_positional_verdict(&wrong, &claim)
        .unwrap_err()
        .to_string()
        .contains("§12.1"));
}

/// The hashes are derived without parsing the invalid uncertified subject.
fn r5_certified_lifetime(gate: &str) -> String {
    let (h, object_hash) = match gate {
        "x b" => (
            "3bc76b4398502416eed66400092c8ec2e5e273d97283b5199065a88a3ed9f1d7",
            "9b10654c083129047b847830d3582ff3dbf15cf7c8759f4586f836c02e5b6266",
        ),
        "cx b t" => (
            "1e0d1484447af491bd512ef5cc3cbe4f1b9532863aa56ae2149f61247973f343",
            "4aaf72716633ad6037e3b542f000eb31372accd743ddb97aa97d2960447ac43b",
        ),
        "cx t b" => (
            "020372af2df49bc56df0f37f08dfc7b58af2e258df9fb58da7010a7a8d3eb24a",
            "cb7ef9243fc8e1144a6863142a46e2969941940894e993bd2abddb685725f7cd",
        ),
        _ => panic!("test gate"),
    };
    let body = format!("qloop 2 {{\nb = qborrow any 1\n{gate}\nqreturn b\n}}");
    let text = support::borrow_lifetime_object(&body, &[2]).replace(&"0".repeat(64), h);
    let certified = support::certified_borrow_identity(&body, &[2]);
    assert_eq!(
        certified.split("\nsection certificate").next().unwrap(),
        text
    );
    let cert = json(certified.lines().last().unwrap());
    assert_eq!(
        cert.get("bindings")
            .unwrap()
            .get("object_hash")
            .unwrap()
            .string()
            .unwrap(),
        object_hash
    );
    certified
}

#[test]
fn sol_r5_b01_certificates_cannot_waive_completed_lifetimes() {
    for (i, gate) in ["x b", "cx b t"].iter().enumerate() {
        // Each beta_i is independent: X fails restoration, CX fails output
        // independence. Whole-loop parity is irrelevant to either obligation.
        let certified = r5_certified_lifetime(gate);
        for (j, text) in [
            certified.split("\nsection certificate").next().unwrap(),
            &certified,
        ]
        .iter()
        .enumerate()
        {
            support::reject_cli(text, "§5.6", &format!("r5-certified-{i}-{j}"));
        }
    }
}

#[test]
fn sol_r5_b01_library_replay_checks_boundaries_even_when_region_map_is_identity() {
    for gate in ["x b", "cx b t"] {
        let invalid = r5_certified_lifetime(gate);
        // Object's fields are public. Isolate verify_certificate from parse's
        // definite-failure guard by constructing the same compiled subject from
        // a valid paired-gate object, then installing the independently bound
        // invalid source/metadata. This tests the second admission defense.
        let valid = support::borrow_lifetime_object(
            &format!("qloop 2 {{\nb = qborrow any 1\n{gate}\n{gate}\nqreturn b\n}}"),
            &[2],
        );
        let mut o = Object::parse(&valid).unwrap();
        let f = o.functions.get_mut("a").unwrap();
        f.blocks[0].instructions[0].bodies[0].remove(2);
        f.lines = invalid
            .split("section functions\n")
            .nth(1)
            .unwrap()
            .split("\n\nsection certificate")
            .next()
            .unwrap()
            .lines()
            .map(str::to_string)
            .collect();
        o.metadata.insert(
            "symbols".into(),
            json(
                invalid
                    .split("section symbols\n")
                    .nth(1)
                    .unwrap()
                    .lines()
                    .next()
                    .unwrap(),
            ),
        );
        o.metadata
            .insert("certificate".into(), json(invalid.lines().last().unwrap()));
        o.text = invalid;
        let closure = o.identity().unwrap().closure_hashes["a"].clone().unwrap();
        assert_eq!(o.verify_claim(&closure, 0).unwrap(), ClaimVerdict::Proof);
        let error = o.verify_certificate().unwrap_err().to_string();
        assert!(
            error.contains("§5.6") && error.contains("qreturn"),
            "{error}"
        );
    }
    for body in [
        "qloop 2 {\nb = qborrow any 1\nx b\nx b\nqreturn b\n}",
        "qloop 2 {\nb = qborrow any 1\ncx b t\ncx b t\nqreturn b\n}",
        "b = qborrow any 1\nqloop 2 {\ncx b t\n}\nqreturn b",
    ] {
        let o = Object::parse(&support::certified_borrow_identity(body, &[2])).unwrap();
        assert_eq!(
            o.verify_certificate().unwrap().claims[0].verdict,
            ClaimVerdict::Proof
        );
        support::borrow_identity(&o);
    }
}

#[test]
fn sol_r5_b01_certificate_return_checks_keep_quantum_surrounding_state() {
    // Each borrowed frame is identity even though t is a superposition at
    // qreturn. Auditing the classical values of all other wires would narrow
    // this valid action; compare their exact quantum state instead.
    for body in [
        "h t\nb = qborrow any 1\nx b\nx b\nqreturn b\nh t",
        "b = qborrow any 1\nx b\nx b\nh t\nh t\nx b\nx b\nqreturn b",
    ] {
        let o = Object::parse(&support::certified_borrow_identity_kind(
            body,
            &[],
            "action",
        ))
        .unwrap();
        assert_eq!(
            o.verify_certificate().unwrap().claims[0].verdict,
            ClaimVerdict::Proof
        );
        support::borrow_identity(&o);
    }
}

#[test]
fn sol_r5_b01_library_replay_checks_frames_before_nonpermutation_boundaries() {
    for gate in ["x b", "cx b t"] {
        let body = format!("b = qborrow any 1\n{gate}\nh t\nh t\n{gate}\nqreturn b");
        let invalid = support::certified_borrow_identity_kind(&body, &[], "action");
        let valid = support::borrow_lifetime_object(
            &format!("b = qborrow any 1\n{gate}\n{gate}\nh t\nh t\n{gate}\n{gate}\nqreturn b"),
            &[],
        )
        .replace("perm_action", "action");
        let mut o = Object::parse(&valid).unwrap();
        let f = o.functions.get_mut("a").unwrap();
        f.blocks[0].instructions.remove(6);
        f.blocks[0].instructions.remove(2);
        f.lines = invalid
            .split("section functions\n")
            .nth(1)
            .unwrap()
            .split("\n\nsection certificate")
            .next()
            .unwrap()
            .lines()
            .map(str::to_string)
            .collect();
        o.metadata.insert(
            "symbols".into(),
            json(
                invalid
                    .split("section symbols\n")
                    .nth(1)
                    .unwrap()
                    .lines()
                    .next()
                    .unwrap(),
            ),
        );
        o.metadata
            .insert("certificate".into(), json(invalid.lines().last().unwrap()));
        o.text = invalid;
        let closure = o.identity().unwrap().closure_hashes["a"].clone().unwrap();
        assert_eq!(o.verify_claim(&closure, 0).unwrap(), ClaimVerdict::Proof);
        assert!(o
            .verify_certificate()
            .unwrap_err()
            .to_string()
            .contains("§5.6"));
    }
}

#[test]
fn codex_r5_b01_exact_three_certified_lifetime_witnesses() {
    for (i, gate) in ["x b", "cx b t", "cx t b"].iter().enumerate() {
        let exact = r5_certified_lifetime(gate);
        for (j, text) in [exact.split("\nsection certificate").next().unwrap(), &exact]
            .iter()
            .enumerate()
        {
            support::reject_cli(text, "§5.6", &format!("codex-r5-b01-{i}-{j}"));
        }
        // No lifetime may borrow a future lifetime's parity cancellation.
        for (j, (body, bounds)) in [
            (format!("b = qborrow any 1\n{gate}\nqreturn b"), vec![]),
            (
                format!("qloop 2 {{\nqloop 2 {{\nb = qborrow any 1\n{gate}\nqreturn b\n}}\n}}"),
                vec![2, 2],
            ),
        ]
        .iter()
        .enumerate()
        {
            support::reject_cli(
                &support::certified_borrow_identity(body, bounds),
                "§5.6",
                &format!("codex-r5-b01-more-{i}-{j}"),
            );
        }
    }
}

fn codex_r5_install_subject(invalid: &str, body: &str) -> Object {
    // Parse a legal shape, then reconstruct public fields to isolate the
    // certificate API's checks from load-time admission.
    let valid = support::borrow_lifetime_object(body, &[]).replace("perm_action", "action");
    let mut o = Object::parse(&valid.replace("cz b ", "x ")).unwrap();
    for i in &mut o.functions.get_mut("a").unwrap().blocks[0].instructions {
        if i.op == "x" {
            i.op = "cz".into();
            i.operands.insert(0, "b".into());
        }
    }
    o.functions.get_mut("a").unwrap().lines = invalid
        .split("section functions\n")
        .nth(1)
        .unwrap()
        .split("\n\nsection certificate")
        .next()
        .unwrap()
        .lines()
        .map(str::to_string)
        .collect();
    o.metadata.insert(
        "symbols".into(),
        json(
            invalid
                .split("section symbols\n")
                .nth(1)
                .unwrap()
                .lines()
                .next()
                .unwrap(),
        ),
    );
    o.metadata
        .insert("certificate".into(), json(invalid.lines().last().unwrap()));
    o.text = invalid.into();
    o
}

#[test]
fn codex_r5_b02_exact_cz_certificate_cannot_admit_a_nonpermutation_frame() {
    let body = "b = qborrow any 1\ncz b t\nqreturn b";
    let exact = support::certified_borrow_identity_kind(body, &[], "action");
    let cert = json(exact.lines().last().unwrap());
    let bindings = cert.get("bindings").unwrap();
    assert_eq!(
        bindings.get("interface_hash").unwrap().string().unwrap(),
        "26374c7b2da2747a9a755d48da06130bfa53e8ba67102e4749fa1cb8adc2f1a0"
    );
    assert_eq!(
        bindings.get("object_hash").unwrap().string().unwrap(),
        "2340cad379662fdcec0e7664aa161a667d77294eee1da295bced60916553158d"
    );
    for (i, text) in [
        exact.split("\nsection certificate").next().unwrap(),
        &exact,
        &exact.replace("\"borrow_frames\":[0]", "\"borrow_frames\":[]"),
    ]
    .iter()
    .enumerate()
    {
        support::reject_cli(text, "§5.6", &format!("codex-r5-b02-{i}"));
    }
    // Public API: a full tuple claim alone is not a T3 proof. Even a pair of
    // illegal phase touches which cancels in the final unitary must fail the
    // mandatory permutation-only gate-boundary premise, independently of replay.
    for body in [
        body,
        "b = qborrow any 1\ncz b t\ncz b t\nqreturn b",
        "c = qalloc any 1\nb = qborrow any 1\ncz b c\ncz b c\nqfree c\nqreturn b",
    ] {
        let invalid = support::certified_borrow_identity_kind(body, &[], "action");
        let o = codex_r5_install_subject(&invalid, body);
        let error = o
            .verify_certificate()
            .expect_err("nonpermutation borrow frame certified");
        assert!(error.to_string().contains("§5.6"), "{error}");
    }
    // Quantum phase witness, not integer basis labels: CZ|++> has -1/2 at 11.
    let o = codex_r5_install_subject(&exact, body);
    let mut q = bennett_isa_ref::QuantumState::new();
    let w = q.allocate(2).unwrap();
    for wire in &w {
        q.gate("h", &[*wire], None, &[]).unwrap();
    }
    let mut b = bennett_isa_ref::QuantumBindings::default();
    b.bundles.insert("t".into(), vec![w[0]]);
    b.borrowed.push(vec![w[1]]);
    o.execute_action("a", &mut q, &b, false, &[]).unwrap();
    for (bits, (re, im)) in q.exact_support() {
        assert_eq!(re, if bits == [true, true] { -0.5 } else { 0.5 });
        assert_eq!(im, 0.0);
    }
    // Non-permutation gates on unrelated wires remain legal, including when
    // t is superposed at the frame's entry or return.
    for body in [
        "h t\nb = qborrow any 1\nx b\nx b\nqreturn b\nh t",
        "b = qborrow any 1\nh t\nx b\nx b\nh t\nqreturn b",
    ] {
        let o = Object::parse(&support::certified_borrow_identity_kind(
            body,
            &[],
            "action",
        ))
        .unwrap();
        assert_eq!(
            o.verify_certificate().unwrap().claims[0].verdict,
            ClaimVerdict::Proof
        );
        support::borrow_identity(&o);
    }
}

#[test]
fn muse_r5_translation_frame_maximality_is_within_its_static_sequence() {
    // Two pre-loop borrowed touches form an identity frame. Each iteration's
    // complete translation frame is maximal within its own static body.
    let text = sol_translation_object("cx p b\ncx b t\ncx p b\ncx b t", true).replace(
        "b = qborrow any 1\nqloop",
        "b = qborrow any 1\ncx p b\ncx p b\nqloop",
    );
    let text = support::rehash(&text).text;
    sol_assert_translation(&text, &sol_translation_claim(&text, 4, 7, 4, 5, "b"), true);
}

#[test]
fn r17_sample_count_default_replays_and_present_values_validate() {
    let base = swap_frame(1);
    let domain = r#"{"bundles":[{"name":"t","width":1,"lo":0,"hi":1},{"name":"x","width":1,"lo":0,"hi":1}],"borrowed":[{"name":"b","width":1,"lo":0,"hi":1}],"regions":[]}"#;
    let mut sampler = json(r#"{"algorithm":"xoshiro256**","seed":["1","2","3","4"]}"#);
    for count in [None, Some(0), Some(3)] {
        if let Some(count) = count {
            let Json::Object(fields) = &mut sampler else {
                unreachable!()
            };
            fields.insert("count".into(), json(&count.to_string()));
        }
        let claim = format!(
            r#"{{"kind":"sampled","domain":{domain},"sampler":{}}}"#,
            sampler.canonical()
        );
        let text = certificate(&base, 1, &claim, "");
        let o = Object::parse(&text).unwrap();
        let closure = o.identity().unwrap().closure_hashes["a"].clone().unwrap();
        assert_eq!(
            o.verify_claim(&closure, 0).unwrap(),
            ClaimVerdict::Evidence {
                elements: count.unwrap_or(65536)
            }
        );
        assert_eq!(o.text, text);
    }
    for bad in ["null", "{}", "-1", r#""invalid""#] {
        let Json::Object(fields) = &mut sampler else {
            unreachable!()
        };
        fields.insert("count".into(), json(bad));
        let claim = format!(
            r#"{{"kind":"sampled","domain":{domain},"sampler":{}}}"#,
            sampler.canonical()
        );
        let error = Object::parse(&certificate(&base, 1, &claim, "")).unwrap_err();
        assert!(error.to_string().contains("§12.1"), "{error}");
    }
}
````

## `reference-interpreter/tests/r21_resources.rs` (410 lines)

````rust
//! Resource guards run in a fresh process: catch_unwind cannot catch allocator aborts.
mod support;
use bennett_isa_ref::{ClaimVerdict, ClassicalMachine, Object, QuantumRegisters, QuantumState};
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::process::{Command, Output};

const CLAIM: &str = include_str!("fixtures/r21/domain-all.bisa");
const CC: &str = include_str!("fixtures/r21/cc-length.bisa");
const R: &str = include_str!("fixtures/r21/r-length.bisa");

fn guarded(command: &mut Command) -> Output {
    // exec, rather than fork a Rust multithreaded test runner. No unsafe/libc dependency.
    let mut child = Command::new("python3");
    child.args(["-c", "import os,resource,sys; resource.setrlimit(resource.RLIMIT_AS,(256*1024*1024,)*2); resource.setrlimit(resource.RLIMIT_CORE,(0,0)); os.execv(sys.argv[1],sys.argv[1:])"]);
    child.arg(command.get_program()).args(command.get_args());
    for (k, v) in command.get_envs() {
        if let Some(v) = v {
            child.env(k, v);
        }
    }
    child.output().unwrap()
}
fn family(name: &str) {
    let out = guarded(
        Command::new(std::env::current_exe().unwrap())
            .args(["--exact", "r21_resource_child", "--nocapture"])
            .env("R21_FAMILY", name),
    );
    assert!(out.status.success(), "{name}: {out:?}");
    eprintln!("{}", String::from_utf8_lossy(&out.stderr));
}
fn resource<T: std::fmt::Debug>(r: bennett_isa_ref::Result<T>, section: &str) {
    let error = r.expect_err("host-resource error required");
    assert_eq!(error.kind(), bennett_isa_ref::ErrorKind::HostResource);
    let e = error.to_string();
    assert!(e.contains(section) && e.contains("host limit"), "{e}");
}
fn claim(text: &str, small: bool) {
    let o = Object::parse(text).unwrap();
    o.check_hashes().unwrap();
    let h = o.identity().unwrap().closure_hashes["a"].clone().unwrap();
    let r = catch_unwind(|| o.verify_claim(&h, 0)).expect("no claim panic");
    if small {
        assert_eq!(r.unwrap(), ClaimVerdict::Evidence { elements: 1 });
    } else {
        resource(r, "§12.2");
    }
    let r = catch_unwind(|| o.verify_certificate()).expect("no certificate panic");
    if small {
        assert_eq!(
            r.unwrap().claims[0].verdict,
            ClaimVerdict::Evidence { elements: 1 }
        );
    } else {
        resource(r, "§12.2");
    }
}
fn region_claim(a: u64, explicit: bool) -> String {
    let old = Object::parse(CLAIM).unwrap().identity().unwrap();
    let (base, cert) = CLAIM.split_once("\nsection certificate\n").unwrap();
    let base = base
        .replace("\"A\":63", &format!("\"A\":{a}"))
        .replace("region[63,1]", &format!("region[{a},1]"));
    let o = support::rehash(&base);
    let id = o.identity().unwrap();
    let mut cert = cert
        .replace("\"A\":63", &format!("\"A\":{a}"))
        .replace(&old.interface_hashes["a"], &id.interface_hashes["a"])
        .replace(&old.object_hash, &id.object_hash);
    if explicit {
        cert = cert.replace(
            "\"cells\":\"all\"",
            "\"cells\":[{\"hi\":1,\"index\":0,\"lo\":0}]",
        );
    }
    format!("{}\nsection certificate\n{cert}", o.text)
}
fn transfer(text: &str, len: u64, host: bool) {
    let heap = len.max(1);
    let meta = if heap <= 9_007_199_254_740_991 {
        heap.to_string()
    } else {
        format!("\"{heap}\"")
    };
    let text = text
        .replace("\"9223372036854775808\"", &meta)
        .replace("const.i64 9223372036854775808", &format!("const.i64 {len}"));
    let o = if len == 1 << 63 {
        Object::parse(&text).unwrap()
    } else {
        support::rehash(&text)
    };
    o.check_hashes().unwrap();
    let mut m = ClassicalMachine::new(&o, "f", &[], &[]).unwrap();
    let entry = m.snapshot();
    m.step_once().unwrap();
    m.step_once().unwrap(); // alloc stays sparse and legal at every tested length.
    let prefix = m.snapshot();
    let digest = m.memory_digest().unwrap();
    assert_eq!(digest.len(), 64); // digest iterates resident bytes, never allocation size.
    let result = catch_unwind(AssertUnwindSafe(|| m.step_once())).expect("no transfer panic");
    if len > 8 {
        resource(result, if host { "§10" } else { "§7.3" });
        assert_eq!(
            m.snapshot(),
            prefix,
            "failed transfer must restore the entire prefix"
        );
        assert!(m.host_transcript().unwrap().is_empty());
        assert!(m.console().is_empty());
        assert_eq!(m.effect_tape_len(), 0);
        resource(m.memory_bytes(1, len as usize), "§7.1");
    } else {
        result.unwrap();
        assert_eq!(
            m.memory_bytes(1, len as usize).unwrap(),
            vec![0; len as usize]
        );
        if host {
            assert_eq!(m.outcome().request.unwrap().payload, vec![0; len as usize]);
            m.reply(&[]).unwrap();
        } else {
            assert_eq!(m.console(), vec![0; len as usize]);
            assert_eq!(m.effect_tape_len(), 1);
        }
    }
    m.reverse().unwrap();
    assert_eq!(m.snapshot(), entry);
}
#[test]
fn r21_resource_child() {
    let Ok(name) = std::env::var("R21_FAMILY") else {
        return;
    };
    match name.as_str() {
        "claims" => {
            for (text, small) in [
                (CLAIM, false),
                (include_str!("fixtures/r21/domain-all-A0.bisa"), true),
                (include_str!("fixtures/r21/domain-all-A1.bisa"), true),
                (include_str!("fixtures/r21/domain-all-A64.bisa"), false),
                (
                    include_str!("fixtures/r21/sol-claim-region-all-sampled.bisa"),
                    false,
                ),
                (
                    include_str!("fixtures/r21/sol-claim-region-all-sampled-small.bisa"),
                    true,
                ),
            ] {
                claim(text, small);
            }
            for a in [0, 1, 3, 62, 63, 64, 127, 128] {
                for explicit in [false, true] {
                    claim(&region_claim(a, explicit), a < 4);
                }
            }
            eprintln!("R21 executable region domains: 2 paths x 8 exponents x 2 public consumers = 32 cases; 13 pinned controls");
            let o = Object::parse(include_str!("fixtures/r21/sol-claim-region-all-small.bisa"))
                .unwrap();
            o.check_hashes().unwrap();
            assert_eq!(
                o.verify_certificate().unwrap().claims[0].verdict,
                ClaimVerdict::Proof
            );
        }
        "hostcall" | "console" => {
            let host = name == "hostcall";
            for len in [0, 1, 8, (1 << 63) - 1, 1 << 63, u64::MAX] {
                transfer(if host { CC } else { R }, len, host);
            }
            eprintln!("R21 {name}: 6 transfer, 6 memory-query, 6 sparse digest/trace, 6 reversal controls");
        }
        "entropy" => {
            for len in [0, 1, 8, (1u64 << 63) - 1, 1 << 63, u64::MAX] {
                let text = R
                    .replace("console", "entropy")
                    .replace("entropy.write", "entropy.read")
                    .replace("const.i64 9223372036854775808", &format!("const.i64 {len}"))
                    .replace(
                        "\"heap_limit_max\":\"9223372036854775808\"",
                        "\"heap_limit_max\":\"18446744073709551615\"",
                    );
                let o = support::rehash(&text);
                o.check_hashes().unwrap();
                let mut m = ClassicalMachine::new(&o, "f", &[], &[1; 8]).unwrap();
                let entry = m.snapshot();
                let out = catch_unwind(AssertUnwindSafe(|| m.run(10)))
                    .expect("no entropy length panic")
                    .unwrap();
                assert_eq!(out.fault, if len <= 8 { None } else { Some(10) });
                assert_eq!(m.effect_tape_len(), if len <= 8 { 1 } else { 0 });
                m.reverse().unwrap();
                assert_eq!(m.snapshot(), entry);
            }
        }
        "quantum" => {
            for n in [0, 1, 8, (1usize << 63) - 1, 1 << 63, usize::MAX] {
                let mut q = QuantumRegisters::new();
                let r = catch_unwind(AssertUnwindSafe(|| q.allocate(n))).expect("no qreg panic");
                if n <= 8 {
                    assert_eq!(q.bundle(r.unwrap()).unwrap().len(), n);
                } else {
                    // Qreg handle/class-vector storage is §3.3; dense
                    // quantum-state materialisation below remains §4.3.
                    resource(r, "§3.3");
                }
                let mut q = QuantumRegisters::new();
                let id = q.allocate(8).unwrap();
                let slice =
                    catch_unwind(AssertUnwindSafe(|| q.slice(id, 0, n))).expect("no slice panic");
                if n <= 8 {
                    assert_eq!(q.bundle(slice.unwrap()).unwrap().len(), n);
                } else {
                    let e = slice.unwrap_err().to_string();
                    assert!(e.contains("§3.3") && !e.contains("host limit"), "{e}");
                }
            }
            let mut q = QuantumRegisters::new();
            let a = q.allocate(3).unwrap();
            let b = q.allocate(5).unwrap();
            let c = q.concat(a, b).unwrap();
            assert_eq!(q.bundle(c).unwrap().len(), 8);
            eprintln!(
                "R21 qreg allocation/slice/dense amplitudes: 3 paths / 17 cases; concat control"
            );
            for exponent in [1, 3, 62, 63, 64] {
                let mut q = QuantumState::new();
                q.allocate(exponent).unwrap();
                let r = catch_unwind(|| q.amplitudes()).expect("no dense panic");
                if exponent < 4 {
                    assert_eq!(r.unwrap().len(), 1 << exponent);
                } else {
                    resource(r, "§4.3");
                }
            }
        }
        _ => panic!("unknown family {name}"),
    }
}

#[test]
fn r21_cli_cardinality_and_sparse_output() {
    let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join(".tmp");
    std::fs::create_dir_all(&dir).unwrap();
    for a in [0, 1, 3, 62, 63, 64, 127, 128] {
        let text = region_claim(a, false);
        let path = dir.join(format!("r21-cli-region-{a}.bisa"));
        std::fs::write(&path, text).unwrap();
        let out = guarded(
            Command::new(env!("CARGO_BIN_EXE_bennett-isa-ref"))
                .arg("run-action")
                .arg(&path)
                .args(["a", "--mut", "0"]),
        );
        if a < 4 {
            assert!(out.status.success(), "{out:?}");
        } else {
            assert_eq!(out.status.code(), Some(1), "{out:?}");
            assert!(out.stdout.is_empty());
            assert!(
                String::from_utf8_lossy(&out.stderr).contains("host limit"),
                "{out:?}"
            );
        }
    }
    for len in [0, 1, 8, (1u64 << 63) - 1, 1 << 63, u64::MAX] {
        let text = CC
            .replace("r = hostcall org.bennett.test p n\nret r", "ret n")
            .replace("const.i64 9223372036854775808", &format!("const.i64 {len}"))
            // Full pointer range remains available independent of the chosen n.
            .replace(
                "\"heap_limit_max\":\"9223372036854775808\"",
                "\"heap_limit_max\":\"18446744073709551615\"",
            );
        let o = support::rehash(&text);
        let path = dir.join(format!("r21-cli-sparse-{len}.bisa"));
        std::fs::write(&path, o.text).unwrap();
        let out = guarded(
            Command::new(env!("CARGO_BIN_EXE_bennett-isa-ref"))
                .arg("run-cc")
                .arg(&path)
                .arg("f"),
        );
        assert!(out.status.success(), "{out:?}");
        assert!(
            out.stdout.len() < 8192,
            "sparse memory trace must stay sparse"
        );
    }
    eprintln!("R21 CLI region cells / sparse digest+trace+output: 2 paths / 14 cases");
    let inc = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/inc8.bisa");
    for count in [0, 1, 8, (1u64 << 63) - 1, 1 << 63, u64::MAX] {
        // The replay odometer stays lazy. A downstream frame reservation stops
        // the first element; this does not claim completion of a huge replay.
        let out = guarded(
            Command::new(env!("CARGO_BIN_EXE_bennett-isa-ref"))
                .arg("step-check")
                .arg(&inc)
                .args([
                    "inc8",
                    "--samples",
                    &count.to_string(),
                    "--budget",
                    "18446744073709551615",
                ]),
        );
        assert_eq!(out.status.code(), Some(1), "{out:?}");
        assert!(out.stdout.is_empty());
        let e = String::from_utf8_lossy(&out.stderr);
        assert!(e.contains('§'), "{e}");
        assert_eq!(e.contains("host limit"), count != 0, "{e}");
    }
    for count in [1, 8] {
        let out = guarded(
            Command::new(env!("CARGO_BIN_EXE_bennett-isa-ref"))
                .arg("step-check")
                .arg(&inc)
                .args(["inc8", "--samples", &count.to_string(), "--budget", "3"]),
        );
        assert!(out.status.success(), "{out:?}");
    }
    eprintln!("R21 CLI lazy sample count: 1 path / 6 cases; 2 completed small controls");
}

#[test]
fn r21_independent_witness_pins() {
    for (text, hash, envelope) in [
        (
            CC,
            "23802c541101025a57a13ffb5f00ca72a7ad5ff95f78e9a4fd565c59f566752d",
            include_str!("fixtures/r21/cc-length.envelope"),
        ),
        (
            R,
            "2751a25e6e906ea512bc075da07cda7463161576c56cebf06455ba2d9dfab704",
            include_str!("fixtures/r21/r-length.envelope"),
        ),
    ] {
        let o = Object::parse(text).unwrap();
        o.check_hashes().unwrap();
        let id = o.identity().unwrap();
        assert_eq!(bennett_isa_ref::sha256_hex(envelope.as_bytes()), hash);
        assert_eq!(id.envelopes["f"], envelope);
        assert_eq!(id.interface_hashes["f"], hash);
        assert_eq!(id.closure_hashes["f"].as_deref(), Some(hash));
    }
    let id = Object::parse(CLAIM).unwrap().identity().unwrap();
    assert_eq!(
        id.interface_hashes["a"],
        "f30725fa31cc35b68090b82cfd046681c4342821591cd2d6dd5300ea522499af"
    );
    assert_eq!(
        id.object_hash,
        "5fa6df63e007ad2bca8ab69c5a0c82e7671c585982048cf99919e59cc48a1e43"
    );
    assert_eq!(
        bennett_isa_ref::sha256_hex(include_bytes!(
            "fixtures/r21/sol-claim-region-all-sampled.bisa"
        )),
        "dfca89aa2073705841586a1c4a76e27be92618417476e9cb3b9016c0e09ab3c4"
    );
}
#[test]
fn r21_b01_claims_public_consumers() {
    family("claims");
}
#[test]
fn r21_b02_hostcall_public_consumer() {
    family("hostcall");
}
#[test]
fn r21_b02_console_public_consumer() {
    family("console");
}
#[test]
fn r21_entropy_transfer_length_fault_separation() {
    family("entropy");
}
#[test]
fn r21_quantum_cardinality_and_lengths() {
    family("quantum");
}

#[test]
fn r21_b02_cli_pinned_transfers() {
    for file in ["cc-length.bisa", "r-length.bisa"] {
        let path = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("tests/fixtures/r21")
            .join(file);
        let out = guarded(
            Command::new(env!("CARGO_BIN_EXE_bennett-isa-ref"))
                .arg("run-cc")
                .arg(path)
                .arg("f"),
        );
        assert_eq!(out.status.code(), Some(1), "{out:?}");
        assert!(out.stdout.is_empty());
        let e = String::from_utf8_lossy(&out.stderr);
        assert!(
            e.contains("host limit")
                && e.contains(if file.starts_with("cc") {
                    "§10"
                } else {
                    "§7.3"
                }),
            "{e}"
        );
    }
}
````

## `reference-interpreter/tests/r22_coverage.rs` (274 lines)

````rust
mod support;
use bennett_isa_ref::{ClaimVerdict, Object};
#[test]
fn sol_r22_b01_false_proof_and_controls() {
    for (text, full) in [
        (include_str!("fixtures/r22/false-cnot-proof.bisa"), false),
        (
            include_str!("fixtures/r22/false-cnot-renamed-control.bisa"),
            false,
        ),
        (
            include_str!("fixtures/r22/false-cnot-full-control.bisa"),
            true,
        ),
    ] {
        let o = Object::parse(text).unwrap();
        o.check_hashes().unwrap();
        let hash = o.identity().unwrap().closure_hashes["a"].clone().unwrap();
        if full {
            let e = o.verify_claim(&hash, 0).unwrap_err().to_string();
            assert!(e.contains("§12.1") && e.contains("element 4"), "{e}");
        } else {
            assert_eq!(
                o.verify_claim(&hash, 0).unwrap(),
                ClaimVerdict::Evidence { elements: 4 }
            );
            assert_eq!(
                o.verify_certificate().unwrap().claims[0].verdict,
                ClaimVerdict::Evidence { elements: 4 }
            );
        }
    }
}

#[test]
fn sol_r22_b01_public_role_collision_family() {
    use bennett_isa_ref::json::Json;
    let text = include_str!("fixtures/r22/false-cnot-proof.bisa");
    let (base, cert) = text.split_once("\nsection certificate\n").unwrap();
    let o = Object::parse(text).unwrap();
    let hash = o.identity().unwrap().closure_hashes["a"].clone().unwrap();
    let original_expected = o.identity().unwrap().closure_hashes["identity"]
        .clone()
        .unwrap();
    let mut labels = std::collections::BTreeMap::new();
    let mut cases = 0;
    for borrowed in ["t", "u", "b", "r"] {
        for subset in 0..4 {
            for full in [false, true] {
                let bundles = ["t", "u"]
                    .iter()
                    .enumerate()
                    .filter(|(i, _)| subset & (1 << i) != 0)
                    .map(|(_, name)| {
                        format!(
                            r#"{{"name":"{name}","width":1,"lo":0,"hi":{}}}"#,
                            u8::from(full)
                        )
                    })
                    .collect::<Vec<_>>()
                    .join(",");
                let new_domain = Json::parse(&format!(r#"{{"bundles":[{bundles}],"regions":[],"borrowed":[{{"name":"{borrowed}","width":1,"lo":0,"hi":1}}]}}"#)).unwrap();
                let mut cert = Json::parse(cert).unwrap();
                fn replace_domain(j: &mut Json, domain: &Json) {
                    match j {
                        Json::Object(o) => {
                            for (k, v) in o {
                                if k == "domain" && matches!(v, Json::Object(_)) {
                                    *v = domain.clone();
                                } else {
                                    replace_domain(v, domain);
                                }
                            }
                        }
                        Json::Array(a) => {
                            for j in a {
                                replace_domain(j, domain);
                            }
                        }
                        _ => (),
                    }
                }
                replace_domain(&mut cert, &new_domain);
                // Compare each replay with itself, so verdict tests coverage,
                // independently of the witness's expected-program mismatch.
                let cert = cert.canonical().replace(
                    &format!("\"program\":\"{original_expected}\""),
                    &format!("\"program\":\"{hash}\""),
                );
                let o = Object::parse(&format!("{base}\nsection certificate\n{cert}\n")).unwrap();
                o.check_hashes().unwrap();
                let verdict = o.verify_claim(&hash, 0).unwrap();
                if let Some(previous) = labels.insert((subset, full), verdict.clone()) {
                    assert_eq!(
                        verdict, previous,
                        "borrowed renaming must preserve the exact label/count"
                    );
                }
                assert_eq!(
                    verdict == ClaimVerdict::Proof,
                    subset == 3 && full,
                    "borrowed={borrowed} subset={subset} full={full}: {verdict:?}"
                );
                cases += 1;
            }
        }
    }
    assert_eq!(cases, 32);
}

#[test]
fn sol_r22_b01_table_spoof_and_borrowed_renaming() {
    let text = include_str!("fixtures/r22/domain-role-spoof.bisa");
    let o = Object::parse(text).unwrap();
    o.check_hashes().unwrap();
    let hash = o.identity().unwrap().closure_hashes["a"].clone().unwrap();
    for name in ["t", "b", "unrelated"] {
        let renamed = text.replace(
            "\"name\":\"t\",\"width\":1",
            &format!("\"name\":\"{name}\",\"width\":1"),
        );
        let o = Object::parse(&renamed).unwrap();
        o.check_hashes().unwrap();
        assert_eq!(
            o.verify_claim(&hash, 0).unwrap(),
            ClaimVerdict::Evidence { elements: 2 }
        );
    }
}

#[test]
fn r23_public_oracle_roles_and_explicit_region_cells() {
    use bennett_isa_ref::json::Json;
    use std::collections::BTreeMap;
    fn set(value: &mut Json, key: &str, next: Json) {
        let Json::Object(fields) = value else {
            panic!("object expected")
        };
        fields.insert(key.into(), next);
    }
    fn replay(o: &Object, domain: Json, interface: Json) -> ClaimVerdict {
        let (_, template) = include_str!("fixtures/r22/false-cnot-proof.bisa")
            .split_once("\nsection certificate\n")
            .unwrap();
        let mut cert = Json::parse(template).unwrap();
        let id = o.identity().unwrap();
        let hash = id.closure_hashes["a"].clone().unwrap();
        let mut bindings = cert.get("bindings").unwrap().clone();
        for (key, value) in [
            ("object_hash", id.object_hash),
            ("interface_hash", id.interface_hashes["a"].clone()),
            ("closure_hash", hash.clone()),
            ("reference_program_hash", hash.clone()),
        ] {
            set(&mut bindings, key, Json::String(value));
        }
        set(&mut cert, "bindings", bindings);
        let mut region = cert
            .get("regions")
            .unwrap()
            .object()
            .unwrap()
            .values()
            .next()
            .unwrap()
            .clone();
        set(
            &mut region,
            "kind",
            Json::String(o.functions["a"].kind.clone()),
        );
        set(&mut region, "signature", o.functions["a"].signature());
        let mut frame = region.get("frame").unwrap().clone();
        set(&mut frame, "interface", interface);
        set(&mut region, "frame", frame);
        let mut claim = Json::Object(BTreeMap::from([
            ("kind".into(), Json::String("exhaustive".into())),
            ("domain".into(), domain),
            (
                "expected".into(),
                Json::Object(BTreeMap::from([(
                    "program".into(),
                    Json::String(hash.clone()),
                )])),
            ),
        ]));
        let schedule = (o.functions["a"].kind == "oracle").then(|| Json::parse(&format!(r#"{{"bindings":{{"budget":[1,0,0,0],"closure_hash":"{hash}","epsilon":0,"inherited_controls":0,"params_hash":"{}","region":"a","scheduler":{{"name":"test","version":"1"}},"target_hash":"{}","variant":"forward"}},"entries":[]}}"#, "2".repeat(64), "3".repeat(64))).unwrap());
        if let Some(schedule) = &schedule {
            set(&mut claim,"subject",Json::parse(&format!(r#"{{"closure_hash":"{hash}","variant":"forward","inherited_controls":0,"schedule_hash":"{}"}}"#, bennett_isa_ref::sha256_hex(schedule.canonical().as_bytes()))).unwrap());
        }
        set(&mut region, "claims", Json::Array(vec![claim]));
        set(
            &mut cert,
            "regions",
            Json::Object(BTreeMap::from([(hash.clone(), region)])),
        );
        let schedule = schedule
            .map(|s| format!("\nsection schedule\n{}\n", s.canonical()))
            .unwrap_or_default();
        let p = Object::parse(&format!(
            "{}{schedule}\nsection certificate\n{}\n",
            o.text,
            cert.canonical()
        ))
        .unwrap();
        p.check_hashes().unwrap();
        let verdict = p.verify_claim(&hash, 0).unwrap();
        assert_eq!(p.verify_certificate().unwrap().claims[0].verdict, verdict);
        verdict
    }
    let sig =
        r#"{"abi":"0.8","args":[],"fault":4,"in":[1],"kind":"oracle","mem":[],"tgt":1,"tier":"q"}"#;
    let body = "oracle @a (x:wire in) (t:wire) (f:wire[4]) () ()\n^entry():\nlift.retval x";
    let oracle = support::rehash(&support::object(&[("a", sig, body)], "{}", ""));
    let mut count = 0;
    let mut previous = BTreeMap::new();
    for borrowed in ["x", "t", "f", "other"] {
        for subset in 0..8 {
            let bundles = [("x", 1, 1), ("t", 1, 1), ("f", 4, 15)]
                .iter()
                .enumerate()
                .filter(|(i, _)| subset & (1 << i) != 0)
                .map(|(_, (name, width, hi))| {
                    format!(r#"{{"name":"{name}","width":{width},"lo":0,"hi":{hi}}}"#)
                })
                .collect::<Vec<_>>()
                .join(",");
            let domain=Json::parse(&format!(r#"{{"bundles":[{bundles}],"regions":[],"borrowed":[{{"name":"{borrowed}","width":1,"lo":0,"hi":1}}]}}"#)).unwrap();
            let verdict=replay(&oracle,domain,Json::parse(r#"[{"role":"in","width":1,"class":"any"},{"role":"tgt","width":1,"class":"any"},{"role":"fault","width":4,"class":"any"}]"#).unwrap());
            assert_eq!(
                verdict == ClaimVerdict::Proof,
                subset == 7,
                "{borrowed}/{subset}: {verdict:?}"
            );
            if let Some(old) = previous.insert(subset, verdict.clone()) {
                assert_eq!(old, verdict);
            }
            count += 1;
        }
    }
    let region = Object::parse(
        include_str!("fixtures/r21/sol-claim-region-all-small.bisa")
            .split_once("\nsection certificate\n")
            .unwrap()
            .0,
    )
    .unwrap();
    // This region has A=1, hence two cells: exercise explicit lists publicly.
    let mut previous = BTreeMap::new();
    for borrowed in ["t", "r", "other"] {
        for subset in 0..4 {
            for bundle in [false, true] {
                let cells = (0..2)
                    .filter(|i| subset & (1 << i) != 0)
                    .map(|i| format!(r#"{{"index":{i},"lo":0,"hi":1}}"#))
                    .collect::<Vec<_>>()
                    .join(",");
                let bundles = if bundle {
                    r#"{"name":"t","width":1,"lo":0,"hi":1}"#
                } else {
                    ""
                };
                let domain=Json::parse(&format!(r#"{{"bundles":[{bundles}],"regions":[{{"name":"r","cells":[{cells}]}}],"borrowed":[{{"name":"{borrowed}","width":1,"lo":0,"hi":1}}]}}"#)).unwrap();
                let verdict=replay(&region,domain,Json::parse(r#"[{"role":"mut","width":1,"class":"any"},{"role":"in","width":2,"class":"any"}]"#).unwrap());
                assert_eq!(verdict == ClaimVerdict::Proof, subset == 3 && bundle);
                if let Some(old) = previous.insert((subset, bundle), verdict.clone()) {
                    assert_eq!(old, verdict);
                }
                count += 1;
            }
        }
    }
    assert_eq!(count, 56);
}
````

## `reference-interpreter/tools/test-slow-source-forwarding.sh` (12 lines)

````bash
#!/bin/sh
# Explicit opt-in: never materialise the wide source witness without a host cap.
set -eu
ulimit -v 8388608
ulimit -c 0
root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
exec /usr/bin/time -f 'slow-source-forwarding wall_s=%e peak_rss_kib=%M' \
    timeout 600 cargo test --offline -j3 \
    --manifest-path "$root/reference-interpreter/Cargo.toml" \
    --test isa09_forwarding \
    source_forwarding_large_materialisation_reports_host_capacity_before_exhausting_memory \
    -- --ignored --exact --test-threads=1 --nocapture
````
