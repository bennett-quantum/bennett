# Council — td-fd0-2026-11-02 round 2

Document snapshot sha256 5f41427c26a4; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

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

Verdicts: **sol: revise**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: no**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 1 (blocking 1), codex: core 0 / contract 0 (blocking 0)

## Regressions reported

- **[sol]** The new schedule-wide ModelInput requirement is not integrated with the inherited §10.1 default-only launch-estimate path; see R2-1.

## Previous-round blockers, status

- [sol] FD0-1: **resolved** — The syntactic transitive dependency set freezes operational parameters regardless of role across reports, ModelInputs and invokes.
- [sol] FD0-2: **resolved** — Standalone subjects now explicitly identify variant, inherited controls and the complete invocation.
- [sol] FD0-3: **resolved** — The normative rule and vectors consistently classify a missing selector as malformed input.
- [sol] FD0-4: **resolved** — Normal ref@0.10 publication, envelope changes, default binding and dependent re-pinning are explicit; both stated catalog hashes reproduce.
- [sol] FD0-5: **resolved** — The §12.3 insertion and shared scope statement identify device-only certificates and preserve native host code and remaining mixed-launch obligations.
- [sol] B1: **resolved** — Scheduling requests now bind root, parameters and reservations through schedule_hash; R2-1 concerns the newly required input's separate launch/default integration.
- [sol] B2: **resolved** — Missing selectors, missing ModelInputs and free dependent parameters now have distinct, consistent outcomes.
- [sol] B3: **resolved** — Reports bind identified embedded device objects and root closures, with independent contexts and no whole-native-program total.
- [codex] FD0-1: **resolved** — The syntactic transitive operational dependency set freezes values across reports, ModelInputs and invokes regardless of parameter role.
- [codex] FD0-2: **resolved** — Standalone subjects explicitly include variant and inherited_controls; scheduled subjects must match the actual context.
- [codex] FD0-3: **resolved** — Missing selectors consistently produce validation errors; free dependencies with valid selectors remain symbolic.
- [codex] FD0-4: **resolved** — Normal ref@0.10 publication, envelope changes and dependent rebinding are explicit; the stated 83cc9c17… catalog hash reproduces.
- [codex] FD0-5: **resolved** — The §12.3 insertion and shared statement delimit device objects, roots, inventories and native comparison while preserving native host code.
- [codex] B1: **resolved** — Objective ModelInputs include parameters and reservations, participate in schedule_hash, and must be reproduced by certifying reports.
- [codex] B2: **resolved** — The selector conformance vectors now distinguish malformed selectors, missing inputs and valid symbolic inputs.
- [codex] B3: **resolved** — Mixed-fat-object report attachment is explicit and does not require whole-binary lowering or a host-shim implementation.

## Blocking issues

- **[sol] R2-1** (§8.5 Objective input binding; inherited §§10–10.1 default launch-estimate contract; contract): *Fix:* In §10.1 add: “A launch 0.10 estimate request additionally carries model_inputs JCS bytes governed by §8.5. The implementation MUST copy and validate them. A default-only effective schedule MUST serialize exactly those inputs in bindings.model_inputs. An embedded schedule is applicable only when its ModelInputs also match the request after JCS. Every complete, well-typed resolved request, including its required ModelInputs, MUST be supported. Missing required ModelInputs produce incomplete-model-objective before an estimate is returned; no parameter or reservation is inferred.” Expose these bytes through a versioned launch-estimate request or bennett_estimate_run_with_model_inputs, and update §10.1's completeness statement accordingly. Add vectors: supplied N=3 → model objective 9/100000000 seconds and a schedule hash covering that input; supplied N=1 → 3/100000000 and a distinct hash; missing required input → incomplete-model-objective; conflicting embedded input → use a correctly bound default schedule. Alternatively, explicitly exempt non-optimizing §10.1 scheduled-leaf estimates from the ModelInput requirement, retaining their complete §8.2 rows and checked certificate while leaving model objectives unresolved. I recommend explicit launch input transport. The ordinary scalar 0.9 API and its required demo estimates remain unchanged.
  <1>1 Launch estimates support every well-typed resolved argument vector, use §11 defaults when no embedded schedule matches, and return an explicit effective schedule even for a default-only realisation.  — clause:ISA 0.9 §10.1 Resolved request and Certificate binding, inherited by the proposed full-version publication
  <1>2 The new rule requires ModelInputs in schedule.bindings whenever the target objective has model-resource terms. Missing required inputs permit no completed concrete schedule. The only new input transport is a setter on bennett_sched_request_t; bennett_estimate_run has no such input, and no default-estimate exception is stated.  — witness:docs/notes/2026-11-02-rev2/fd0.md:156; witness:docs/notes/2026-11-02-rev2/fd0.md:193; clause:ISA 0.9 §10, bennett_estimate_run signature
  <1>3 Use the worked resolved surface target with objective weighted model_cycle:1 and selector {model:"surface",node:"algorithm",metric:"duration"}. Request an otherwise supported launch estimate with no matching embedded schedule. Its operational fields are concrete, but the launch request cannot supply the required ModelInput. Legal explicit N=1 and N=3 inputs would select respectively 3/100000000 and 9/100000000 seconds.  — witness:docs/notes/2026-11-02-rev2/fd0.md, Worked serialized import; witness:spec/Bennett-ISA-Spec-0.9.md:2283
  <1>4 The inherited obligation requires a default-schedule estimate, while the new binding rule prohibits completing that schedule without an input this request cannot carry. Returning incomplete-model-objective and returning the required default estimate are conflicting obligations. This needs a semantic request/default decision, beyond C-header enumeration.  — step:<1>1; step:<1>2; step:<1>3

## sol

All eight round-1 blockers are resolved: FD0-1 through FD0-5 and B1 through B3. The arithmetic, fixture identities and catalog migration reproduce; no cited-clause defect premise was found false. One new contract conflict remains between mandatory ModelInputs and §10.1 default launch estimates. Core scope accepts. The 0.10 route preserves current 0.9 padded demo estimates through concrete scalar targets, and the mixed-fat-object standing check passes.

**Path to accept:** 1. Resolve R2-1 by explicitly transporting ModelInputs through launch 0.10 estimates, or by specifying the scheduled-leaf-only default-estimate exception. 2. Add conformance cases for supplied, missing and conflicting inputs on that path. No core change, 0.9 schema amendment, completed vendor adapter or host shim is required for acceptance of this text.

- **C1 5**: The insertion leaves ISA §3 state and stepping unchanged. Model validation failures are explicitly separated from executed-program faults. *Change:* Retain §8.5's rule: “Model validation errors do not change F_B or introduce ISA fault codes.”
- **C2 5**: No instructions or operands change. Operational substitutions have explicit destinations and cannot alter instruction semantics, interface widths or source budgets. *Change:* Retain the sentence prohibiting bindings to quantum operations, interface widths, source budgets and certificate proof fields.
- **C3 5**: Physical risk, approximation epsilon and oracle faults remain distinct. Model parameters cannot inspect coherent state. Checked accounting is explicitly conditional on external physical assumptions. *Change:* Retain: “Results do not become permutation proofs, channel bounds, operator-norm bounds or oracle fault guarantees by appearing in a checked model report.”
- **C4 4**: Typed dimensions, exact evaluation, operational freezing, interval composition and shared reservations are substantially specified. The d=3/d=5 arithmetic and sequential/parallel results reproduce. *Change:* In Operational bindings state: “Let q be the evaluated base value divided by the quantity's declared unit scale; the destination coefficient is x=q*factor.” The worked conversion remains 30*(1/1000000000)=3/100000000 seconds.
- **C5 4**: All round-1 identity defects are repaired. However, the mandatory ModelInput binding is not integrated with inherited §10.1 default-only launch estimates. The catalog migration correctly changes the versioned identity to 83cc9c177bad054bd7af35dc1892645d869b9e4c0b9c968f35b8783ce2b54c42. *Change:* Extend §10.1 with: “A launch 0.10 estimate request carries explicit model_inputs, which are copied into its effective schedule and checked under §8.5.” Define the default-schedule and missing-input outcomes as specified in R2-1.
- **C6 4**: check_rev2.py exits 0 with eight PASS lines. Source/model hashes, exact arithmetic, reservation identities and both catalog hashes reproduce. The note accurately disclaims generic consumer validation and a complete serialized Report fixture. *Change:* Publish a complete target/schedule/Report fixture with real production bindings. For d=5/N=3 require model duration 9/100000000 seconds, risk charge 3/10000000, physical peak 50 and occupancy 9/2000000 physical-qubit seconds.
- **C7 5**: The 0.9 defect citations are accurate. The scalar compatibility path preserves current demo estimates, and the mixed-fat-object insertion explicitly separates device certificates from native main, argv/envp and host libc. The external premises agree with [Microsoft's architecture example](https://quantum.microsoft.com/en-us/insights/blogs/modeling-quantum-architecture-with-azure-quantum-resource-estimator), [Qualtran's symbolic call-graph protocol](https://qualtran.readthedocs.io/en/latest/resource_counting/call_graph.html) and [its release notes](https://github.com/quantumlib/Qualtran/releases). *Change:* Retain the consumer rule: “Every fully bound 0.9 invocation retains its §10.1 estimate of the complete padded realisation, including the SQLite N=2^20 instance; symbolic interchange remains open fd0/gyp work.”
- **C8 4**: The proposal supplies implementable arithmetic and accounting obligations without demanding a particular algebraic-number library. The remaining launch/default integration conflict prevents independent consumers from implementing one consistent request path. *Change:* Add §10.1 to Publication edits and state exactly how launch estimates obtain ModelInputs when no embedded schedule matches; do not leave this to an inferred parameter or reservation default.

Suggestions:
1. Worked examples/publication fixtures: add one complete serialized target, schedule and Report using production object/closure hashes. State: “These bytes are an interchange conformance fixture.” Require duration 9/100000000, risk_charge 3/10000000, physical peak 50 and occupancy 9/2000000 for d=5/N=3, and reject the same correct numbers attached to a different invocation/context.
2. §8.5 Operational bindings: make the coefficient conversion explicit: “Evaluate the quantity in base units, divide by its declared source-unit scale, then multiply by factor exactly once.” For cycle=30 ns, the seconds binding is 3/100000000, not 3/100000000000000000.

## codex

Accept. All round-1 blockers are resolved: sol FD0-1 through FD0-5 and codex B1 through B3. No new S0 issue or regression was established. The cited import defect is real; arithmetic and identity witnesses reproduce. The 0.10 route preserves current 0.9 estimates, and the mixed-fat-object standing check passes. No false technical premise or misnumbered cited ISA clause was found.

**Path to accept:** No blocking changes are required. To raise C6 from 4 to 5, publish the complete bound target/schedule/Report fixture and independently check its outputs, wrong-context rejection and cross-model rebinding case.

- **C1 5**: The insertion preserves the machine state and step relation. Its validation and infeasibility outcomes explicitly remain separate from ISA faults. *Change:* No change required. Retain §12.3: “No model output changes the object's instruction semantics.”
- **C2 5**: No instruction or operand semantics change. Operational destinations exclude quantum operations, interface widths and source budgets. *Change:* No change required. Retain §8.5's explicit operational-destination whitelist and prohibition on binding instruction semantics.
- **C3 5**: Model evaluation uses classical inputs. Physical risk remains separate from epsilon, channel bounds and oracle faults; positive model risk does not contradict an exact logical gate. *Change:* No change required. Retain §8.5: “Results do not become permutation proofs, channel bounds, operator-norm bounds or oracle fault guarantees by appearing in a checked model report.”
- **C4 4**: The §8.1–§8.3 defect citations are correct. Units, operational freezing, exact arithmetic, composition and shared reservations are specified coherently. The worked d=3/d=5 arithmetic reproduces. Cross-model conversion and local rebinding still lack a concrete acceptance example. *Change:* In Conformance vectors add: “An invoke passing 10 ns to a non-operational algorithm parameter declared in microseconds binds the coefficient 1/100.” A callee leaf lasting that parameter must contribute 1/100000000 seconds.
- **C5 4**: ModelInput now binds objective parameters and reservations through schedule_hash. Reports identify variant, controls and invocation context. Full-version catalog migration matches §§11.1 and 17 item 7. A complete serialized Report remains an acknowledged publication fixture obligation. *Change:* In Worked serialized import add a complete target, schedule and containing certificate with recomputed identities, including one Report for N=3 and a rejection case attaching its unchanged outputs to the wrong invocation.
- **C6 4**: check_rev2.py exited 0 with all eight PASS lines. Source/model hashes, rational arithmetic, reservation accounting and both catalog hashes reproduce. The script's limited coverage is accurately disclosed. Selector validation now agrees with the normative rule. *Change:* Extend the publication fixture with complete Report outputs: duration 9/100000000 seconds, risk_charge 3/10000000, physical peak 50 and occupancy 9/2000000 physical-qubit seconds; validate these through independently implemented producer and checker paths.
- **C7 5**: The 0.9 bridge preserves §10.1 padded estimates, including the demo ladder. The mixed-fat-object insertion explicitly preserves native host code and device-root report scope. The external premises are supported by Microsoft's parameterized QEC example and Qualtran's symbolic call graph: [Microsoft](https://quantum.microsoft.com/en-us/insights/blogs/modeling-quantum-architecture-with-azure-quantum-resource-estimator), [Qualtran](https://qualtran.readthedocs.io/en/latest/resource_counting/call_graph.html). *Change:* No change required. Retain the consumer rule preserving complete 0.9 estimates and the §12.3 statement that model reports assert no whole-native-program resource total.
- **C8 4**: Consumers can implement the specified arithmetic and accounting independently. Unsupported interpretation has an explicit obligation path rather than an invented value. The distinction between base-valued expression evaluation and source-unit binding coefficients could be stated more directly. *Change:* In §8.5 Operational bindings replace “Let x be the exact quantity value times factor” with “Let x be the quantity's numeric coefficient in its declared Quantity.unit, multiplied by factor.” The worked conversion remains 30 × 1/1000000000 = 3/100000000 seconds.

Suggestions:
1. Worked serialized import / publication fixtures: add a complete target, schedule and containing certificate with actual recomputed hashes. State: “For d=5 and N=3, duration is 9/100000000 seconds, risk_charge is 3/10000000, physical peak is 50 and physical occupancy is 9/2000000 physical-qubit seconds.” An otherwise numerically correct report attached to a different invocation/context must reject.
2. Conformance vectors / cross-model invokes: add a caller passing 10 ns to a callee's non-operational algorithm parameter t declared in microseconds, whose report-level default is 1. State: “The invocation binds t=1/100 and contributes 1/100000000 seconds; the callee's report-level quantity display retains its default value of 1 microsecond.” This exercises the existing conversion and local-environment rules without changing them.
3. §8.5 Operational bindings: state “Let x be the quantity's numeric coefficient in its declared Quantity.unit, multiplied by factor.” This makes the existing conversion rule immediately apparent: the example uses 30 × 1/1000000000 = 3/100000000 seconds.
