# Council — td-fd0-2026-11-02 round 3

Document snapshot sha256 6aaf7a6220be; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 4 | 4 | 4.0 |  |
| C5 | 4 | 4 | 4.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 4 | 4 | 4.0 |  |

Overall mean: 4.5

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Previous-round blockers, status

- [sol] R2-1: **resolved** — Launch 0.10 now transports and copies ModelInputs, binds default schedules, defines embedded applicability and missing-input behavior, and supplies passing N=1/N=3 witnesses.
- [codex] R2-1: **resolved** — Launch 0.10 now transports ModelInputs, binds them into default schedules, checks embedded applicability and explicitly defines completeness and missing-input behavior; the requested finite witnesses pass.

## Blocking issues

- none

## sol

Accept. R2-1 is resolved; no new S0 issue, regression, false cited premise or misnumbered ISA clause was established. Both finite checkers pass. Source/model and catalog hashes reproduce, including the acknowledged ref@0.10 identity change with all 219 recipes preserved. The 0.10 route preserves required 0.9 estimates, and the mixed-fat-object standing check passes. Acceptance covers the proposed text, not completion of adapters or production consumers.

**Path to accept:** No blocking changes are required. To raise C6 from 4 to 5, publish the complete bound target/schedule/Report fixture and independently check its expected outputs, embedded/default selection and wrong-context rejection.

- **C1 5**: The proposal preserves §3's state and step relation. Model validation, incomplete estimates and schedule infeasibility remain separate from executed-program faults. *Change:* No change required. Retain §12.3: “No model output changes the object's instruction semantics.”
- **C2 5**: No instructions or operand semantics change. The operational-destination whitelist excludes quantum operations, interface widths and source budgets. *Change:* No change required. Retain §8.5's explicit destination whitelist and prohibition on substitutions into instruction semantics or correctness fields.
- **C3 5**: Model inputs remain classical. Physical risk, logical approximation error and oracle faults remain distinct. Checked accounting establishes no unsupported physical or quantum-correctness theorem. *Change:* No change required. Retain §8.5: “Results do not become permutation proofs, channel bounds, operator-norm bounds or oracle fault guarantees by appearing in a checked model report.”
- **C4 4**: Typed units, exact arithmetic, operational freezing, interval composition and shared reservations are coherent. The source-unit clarification correctly applies the conversion factor once. The d=3/d=5 arithmetic and hierarchy results reproduce. *Change:* In Conformance vectors add a serialized algebraic-rounding case: “For sqrt(2) seconds, upper binding at places="3" requires value="283/200"; the corresponding tight Report interval has lo="707/500", hi="283/200", places="3".”
- **C5 4**: The launch insertion resolves R2-1 through explicit copied ModelInputs, default-schedule binding, canonical embedded matching and a complete-request definition. Schedule/report identities and the ref@0.10 migration are explicit. Complete production interchange fixtures remain publication work. *Change:* In Worked serialized import add a complete target, effective schedule and containing certificate. State: “These bytes are an interchange conformance fixture; changing the report's actual invocation or context while retaining its outputs MUST reject.”
- **C6 4**: check_rev4.py and check_rev2.py pass read-only using existing interpreter artifacts. They reproduce the source/model hashes, both catalog hashes, launch-input outcomes and reservation accounting. Their limited coverage is accurately disclosed; no generic consumer implementation or proof is claimed. *Change:* In publication conformance fixtures require independently produced and checked N=3 outputs: duration 9/100000000 seconds, risk_charge 3/10000000, physical peak 50 and occupancy 9/2000000 physical-qubit seconds, plus rejection under a different invocation/context.
- **C7 5**: The cited §8.1–§8.3 defect is real. The 0.9 bridge retains complete padded §10.1 estimates, including the demo ladder; symbolic import remains an explicit implementation obligation. Device-root report attachment passes the mixed-fat-object check. External premises agree with [Microsoft's parameterized architecture example](https://quantum.microsoft.com/en-us/insights/blogs/modeling-quantum-architecture-with-azure-quantum-resource-estimator), [Qualtran's symbolic call-graph protocol](https://qualtran.readthedocs.io/en/latest/resource_counting/call_graph.html) and [its release notes](https://github.com/quantumlib/Qualtran/releases). *Change:* No change required. Retain Consumer impact's rule that every fully bound 0.9 invocation keeps its complete padded estimate, and the §12.3 statement that device reports assert no whole-native-program resource total.
- **C8 4**: Independent consumers can implement the stated arithmetic, accounting and launch-binding obligations. Remaining adapter, generic evaluation and fixture work is clearly distinguished from accepted semantics. Publication requirements are complete but scattered. *Change:* In Publication edits add: “The coordinated 0.10 publication changes target §§8.2–8.5, launch §§10–10.1, sched §11, cert §12.3, and the ref catalog/default bindings in §§11.1 and 17 item 7, with dependent identities recomputed.”

Suggestions:
1. Worked serialized import / publication fixtures: add a complete target, schedule and certificate using actual recomputed identities. State: “For d=5/N=3, duration is 9/100000000 seconds, risk_charge is 3/10000000, physical peak is 50 and occupancy is 9/2000000 physical-qubit seconds; an otherwise numerically correct report attached to a different invocation/context MUST reject.”
2. Conformance vectors: serialize the existing algebraic enclosure obligation using canonical Q strings. State: “sqrt(2) seconds rounded upward at three decimal places binds value="283/200"; its tight interval is {lo:"707/500",hi:"283/200",places:"3"}.”

## codex

Accept the proposed 0.10 text. R2-1 is resolved; no new S0 issue or regression was established. The defect citations, arithmetic and identity claims check out. The route preserves current 0.9 demo estimates, and the mixed-fat-object standing check passes. Acceptance does not claim production adapter or consumer implementation.

**Path to accept:** No blocking changes are required. To raise C6 from 4 to 5, publish and independently validate the complete target/schedule/Report fixture, including wrong-context rejection and the serialized cross-model invocation.

- **C1 5**: The proposal preserves ISA §3 state and stepping. Model validation errors remain distinct from executed-program faults. *Change:* No change required. Retain §12.3: “No model output changes the object's instruction semantics.”
- **C2 5**: No instruction or operand semantics change. The operational-binding whitelist excludes quantum operations, interface widths and source budgets. *Change:* No change required. Retain §8.5's prohibition on binding quantum operations, interface widths, source budgets or certificate proof fields.
- **C3 5**: Model inputs are classical; physical risk remains separate from logical epsilon, channel bounds and oracle faults. Checked accounting does not claim physical-model correctness. *Change:* No change required. Retain: “Results do not become permutation proofs, channel bounds, operator-norm bounds or oracle fault guarantees by appearing in a checked model report.”
- **C4 4**: The cited §8.1–§8.3 limitations are real. Typed units, operational freezing, rounding and interval accounting are specified. The source-unit clarification is correct, and d=3/d=5 arithmetic reproduces. Cross-model invocation still lacks a complete serialized fixture. *Change:* In Conformance vectors add a serialized two-model invoke fixture stating: “Passing 10 ns binds the callee's microsecond parameter to 1/100; its leaf duration is 1/100000000 seconds, while its report-level default quantity remains 1 microsecond.”
- **C5 4**: The §§10–10.1 insertion resolves R2-1 through explicit transport, copied inputs, canonical embedded matching and default-schedule binding. Schedule and report identities are consistent with §9.2. Both catalog hashes reproduce with all 219 recipes unchanged. *Change:* In Worked serialized import add: “These complete target, schedule and certificate bytes form an interchange fixture.” Supply actual object/context bindings, an N=3 Report and a wrong-context rejection variant.
- **C6 4**: check_rev4.py and check_rev2.py both exit 0 read-only, using existing interpreter artifacts. Source/model hashes, catalog identities and supplied/missing/free/conflicting launch-input cases reproduce. The note accurately distinguishes finite witnesses from production implementations. *Change:* In Conformance vectors state: “For d=5/N=3, the complete Report has duration 9/100000000 seconds, risk_charge 3/10000000, physical peak 50 and occupancy 9/2000000 physical-qubit seconds; attaching it to a different invocation context rejects.” Validate the fixture with independently implemented producer and checker paths.
- **C7 5**: The 0.9 bridge preserves complete padded estimates, including SQLite at N=2^20. The mixed-fat-object insertion explicitly scopes reports to device objects and roots. External premises agree with [Microsoft's parameterized architecture example](https://quantum.microsoft.com/en-us/insights/blogs/modeling-quantum-architecture-with-azure-quantum-resource-estimator), [Qualtran's symbolic call graphs](https://qualtran.readthedocs.io/en/latest/resource_counting/call_graph.html) and [its release notes](https://github.com/quantumlib/Qualtran/releases). *Change:* No change required. Retain the consumer rule preserving every fully bound 0.9 estimate and the §12.3 statement that model reports assert no whole-native-program resource total.
- **C8 4**: The normative obligations are implementable without choosing vendor-specific semantics. The repaired launch path is clear, but its finite witness does not exercise the newly specified pointer/length omission cases. *Change:* In Conformance vectors add: “Null/zero-length and nonnull/zero-length inputs denote omission: scalar targets retain their ordinary estimate path, while model-objective targets return E_ARG with incomplete-model-objective. Null/nonzero-length is E_ARG; JSON null is a malformed map.”

Suggestions:
1. Worked serialized import / publication fixtures: add complete target, schedule and certificate bytes with actual identities. State: “For d=5/N=3, duration is 9/100000000 seconds, risk_charge is 3/10000000, physical peak is 50 and physical occupancy is 9/2000000 physical-qubit seconds.” The same numerical outputs attached to another invocation context must reject.
2. Conformance vectors / cross-model invocation: serialize both caller and callee and state: “The 10 ns argument binds t=1/100 in microseconds and contributes 1/100000000 seconds; the report-level quantity display retains its default of 1 microsecond.” Exercise namespace resolution and local rebinding, beyond the existing standalone arithmetic check.
3. Conformance vectors / launch omission: add the pointer/length cases specified in §10.1. State: “Both zero-length forms denote omission; null with nonzero length returns E_ARG; supplied JSON null is malformed.” Check omission against both scalar and model-objective targets.
