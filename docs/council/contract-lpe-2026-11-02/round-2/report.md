# Council — contract-lpe-2026-11-02 round 2

Document snapshot sha256 abaaca1013ac; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 4 | 5 | 4.5 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 4 | 4 | 4.0 |  |
| C5 | 4 | 4 | 4.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 4 | 4 | 4.0 |  |

Overall mean: 4.44

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Previous-round blockers, status

- [sol] LPE-1: **resolved** — Explicit CC/R and launch width_args supply A/W independently of ledger width; coherent calls additionally check axis equality.
- [sol] LPE-2: **resolved** — Concrete family records, frames, subjects and composition references distinguish instances; the mixed-width root contains both required child records.
- [sol] B1: **resolved** — No unavailable caller descriptor is presumed. Explicit shape values and pre-effect validation distinguish equal-size memory shapes.
- [sol] B2: **resolved** — Instance-specific certificates and preserved nested shape captures prevent one width's verification from discharging another.
- [codex] LPE-1: **resolved** — Explicit call and launch width_args supply A/W; mathematical width checks precede effects, and coherent calls preserve both axes.
- [codex] LPE-2: **resolved** — Concrete family records are instance-keyed, with resolved signatures, frames, claims and composition references.
- [codex] B1: **resolved** — The unavailable caller descriptor is no longer presumed; equal-total-width memory shapes remain explicitly distinct.
- [codex] B2: **resolved** — Separate instance records and preserved argument/body/template shape contexts support both widths within one composed certificate.

## Blocking issues

- none

## sol

LPE-1, LPE-2, B1 and B2 are resolved. No new S0 issue or scope narrowing found. The cited technical premises, packing values, 4,352-tuple script and catalog hash check out. Acceptance covers the stated 0.10 extension; it does not authorize incompatible changes to frozen 0.9 bytes.

**Path to accept:** Already acceptable as the proposed 0.10 extension. To raise C6 from 4 to 5, publish the complete serialized mixed-width certificate vector, including rejection of cross-instance claim reuse.

- **C1 5**: Explicit classical width_args resolve the missing CC/R shape input. Mathematical-integer width checks preserve §3.3 binding, while coherent callers must match both resolved memory axes. *Change:* No required change. Retain §5.1's rule: "The resolved denotation is exactly the literal substitution."
- **C2 4**: The revision enumerates permitted substitution positions and preserves ordinary opcode checks. The remaining work is a canonical grammar incorporating those positions and bracketed calls. *Change:* §16.2: add the canonical production "shape_actuals := '[' shape_value (', ' shape_value)* ']'", where shape_value is a literal or permitted classical shape name. Include the example "oracle_call @xor_width[3] tk (x) t f () ()".
- **C3 5**: Literal substitution preserves control, adjoint, prefix reversal, borrowed-system identity and restoration obligations. §4.2 and §5.2 confirm the stated B=0 and B≥1 outcomes. The supplied script passes all 4,352 tuples. *Change:* No required change. Retain the rule that full-domain, control, adjoint, prefix-reversal, borrow-frame and restoration obligations apply independently to every resolved instance.
- **C4 4**: Scheduling and estimation receive complete shape vectors without live register ids. Instance-sensitive bindings prevent cross-width schedule reuse. The stated 219-recipe ref@0.9 envelope hash reproduces exactly. *Change:* §17 item 7: state, "For every ISA 0.10 object, including non-family regions, omitted expansion selects ref version 0.9 with hash 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197, unless another library is explicitly bound."
- **C5 4**: Instance-keyed records now supply distinct signatures, frames, claim subjects, expected-program references and inverse-pair references. Nested captures preserve callee shape identity. Launch transport is decided, although its complete declaration remains a publication deliverable. *Change:* §10: publish the launch 0.10 declaration implementing this rule: "The request explicitly selects the exported family, carries copied width_args_jcs and its byte length, and supplies the existing typed argument, register and token bindings; invalid bindings return E_ARG before ownership acquisition."
- **C6 4**: Family validity and width-uniform claim obligations are stated without claiming an implementation or general proof. Both instance-hash vectors and memory-packing results reproduce. The Python record dictionary is appropriately identified as mathematical verification. *Change:* §15: add a complete serialized two-width certificate vector with the rule, "The mixed root validates with separate H1 and H3 records of widths [1,1,4] and [3,3,4]; substituting an H1 claim for the H3 claim rejects."
- **C7 5**: The cited ISA clauses, dialect §8.4, D34 and G-17 support the efficiency-extension classification. Literal specialization remains available. The mixed-fat-object section explicitly preserves native host code, selected VM closures, dependency linking and corresponding native comparison. *Change:* No required change. Retain §§9/10's statement that certificate inventory covers the selected VM closure and reached instances, rather than every host function.
- **C8 4**: The revision is substantially implementable and states an honest 0.10 release boundary. A small wording improvement would reconcile the broad dialect lowering instruction with the expressly retained literal fallback for layouts beyond direct substitution. *Change:* Dialect §8.4 append: state, "Use a width family where the required shape variation is expressible by this direct-substitution contract; otherwise the existing complete literal-specialization construction remains valid. A finite emitted prefix remains unfinished."

Suggestions:
1. Identity/expansion and §17 item 7: make the existing intended default explicitly cover all 0.10 objects: "Omitted expansion selects the unchanged ref@0.9 library for family and non-family regions alike." This avoids readers applying the inherited object-version default to an ordinary re-emitted 0.10 region.
2. §16.2 and conformance publication: provide canonical family header/call grammar and one complete object/schedule/certificate fixture. State, "The fixture's H1 and H3 records are independently validated; a false instance_hash or cross-instance claim rejects before replay." Expected child widths remain [1,1,4] and [3,3,4].
3. Dialect §8.4 append: state, "Direct-substitution families and complete literal specialization are alternative valid constructions where applicable; missing specializations never become runtime T-IFACE." This makes the formula-layout fallback explicit.
4. Round-1 blocking-items table: replace "astra B1" and "astra B2" with "codex B1" and "codex B2", matching the supplied prior-round outputs.

## codex

LPE-1, LPE-2, B1 and B2 are resolved. No new S0 issue or false technical premise was found. The mathematical witnesses and catalog hash pass verification, and the mixed-fat-object standing check is satisfied. Accept the proposed 0.10 extension.

**Path to accept:** Already acceptable as the proposed 0.10 extension. To raise C8 from 4 to 5, publish the canonical grammar productions and one complete family/two-instance certificate fixture. Retain the explicit version boundary; this acceptance does not endorse silently changing published 0.9 identities.

- **C1 5**: Explicit classical width_args, pre-effect validation and literal substitution preserve ISA §§3.1–3.3. Memory shapes are supplied rather than inferred from register width. *Change:* Optional clarification in §3.2: “An invocation retains its resolved width_args throughout execution, suspension and reversal.”
- **C2 5**: The revision enumerates permitted symbolic positions and preserves ordinary opcode checks after substitution. ISA §§4.2, 4.6 and 16.2 support the stated width and empty-address distinctions. *Change:* Optional clarification in §5.1: “Shape substitution introduces no reference-interpreter instruction and consumes no oracle budget step.”
- **C3 5**: The resolved denotation explicitly retains full-domain, control, adjoint, prefix-reversal and restoration obligations. The xor_width success and B=0 outcomes agree with §5.2; both memory-packing results are correct. *Change:* Conformance vectors: add the explicit boundary result “At n=1, B=0 and true control, (x,t,f)=(1,1,1) becomes (1,1,0); false control leaves (1,1,1) unchanged.” This illustrates XOR fault accumulation.
- **C4 4**: Scheduling and estimation receive complete shapes without register ids; cache bindings distinguish instances. The stated 219-recipe ref@0.9 hash was reproduced. The new expansion default should also appear at the existing default’s authoritative location. *Change:* Amend §17 item 7: “For an ISA 0.10 object, omission of expansion binds ref version 0.9 with hash 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197, for family and non-family regions alike.”
- **C5 4**: Instance-keyed records now resolve the §9.4/§12.3 conflict. Subjects, expected programs, inverse pairs, composition and captured contexts distinguish instances. Version-envelope changes and consumer migration are disclosed; canonical interchange fixtures remain publication work. *Change:* In §9.1 state the compatibility default explicitly: “A signature without width_params has no shape parameters; its launch width_args is [], and its certificate region record remains keyed by closure_hash.”
- **C6 4**: The executable script passes all 4,352 tuples and both instance-hash vectors. Its stated limitation is accurate: it checks mathematical witnesses, not parsing, expansion or certificate checking. Universal obligations have explicit hypotheses and a concrete-claim default. *Change:* Add to §15: “A composed fixture invokes the same family at widths 1 and 3, requires separate records with slot widths [1,1,4] and [3,3,4], and rejects an attempt to discharge the width-3 obligation using only the width-1 claim.”
- **C7 5**: ISA §3.3 and dialect §8.4, D34 and G-17 support the efficiency/interface classification. Existing literal widths remain available. The mixed-fat-object paragraph explicitly preserves native main, argv/envp, unmarked libc, selected VM closures and corresponding native comparison. *Change:* Optional standing-check fixture in §15: “Launching a marked family from a native executable requires certificates for its selected VM closure and reached instances, without requiring certificates for unrelated native functions.”
- **C8 4**: The revised rules decide the previously missing semantics and provide actionable consumer obligations. The remaining work is consolidating those rules into canonical grammar and interchange examples before adoption. *Change:* In §16.2 state: “A family header appends [p0, p1, …] immediately after its symbol; every family call appends [s0, s1, …] in the same parameter order.” Publish a canonical xor_width[n] object with width_params=[{name:"n",bind:{group:"in",slot:0}}] and its two-instance certificate fixture.

Suggestions:
1. Identity, expansion and schedules / §17 item 7: repeat the explicit override at the existing default rule: “ISA 0.10 uses the published ref@0.9 catalog by default, including for non-family regions.” The expected catalog hash remains 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. This is consolidation of the proposed default, not a request for a new catalog.
2. Conformance vectors / §§15–16.2: publish a canonical family object and a bound mixed-width certificate alongside the mathematical script. State: “The checker recomputes each instance hash, substitutes its signature, and validates that record’s frame and claims independently.” Expected child slot widths are [1,1,4] and [3,3,4]; replacing either instance hash with the other must reject before replay.
3. Release / §9.1: state the non-family default explicitly: “Absent width_params means an empty parameter list; non-family launch requests carry width_args=[], and existing non-family certificate keys remain closure hashes.” This makes migration straightforward without altering the proposal’s semantics.
