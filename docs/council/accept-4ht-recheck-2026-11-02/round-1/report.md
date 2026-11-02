# Council — accept-4ht-recheck-2026-11-02 round 1

Document snapshot sha256 832603a2f1ba; rubric docs/council/rubric-isa.md. Members: codex. Scores are advisory.

| | codex | mean | spread ≥ 2 |
|---|---|---|---|
| C1 | 5 | 5.0 |  |
| C2 | 5 | 5.0 |  |
| C3 | 5 | 5.0 |  |
| C4 | 5 | 5.0 |  |
| C5 | 4 | 4.0 |  |
| C6 | 4 | 4.0 |  |
| C7 | 3 | 3.0 |  |
| C8 | 4 | 4.0 |  |

Overall mean: 4.38

Verdicts: **codex: revise**

Core verdicts: **codex: accept**

**Consensus: no**   **Core consensus: YES**

Blocking by scope: codex: core 0 / contract 2 (blocking 2)

## Blocking issues

- **[codex] z4c-4HT-1** (z4c — Hashes, catalog and consumers; proposed ISA §11 action-support addresses; contract): The C7/bennett-4ht standing check explicitly requires a mixed-fat-object compatibility statement when certificate layout is touched. z4c expressly requires address-bearing schedules/certificates to adopt new coordinates. ISA §9.1 embeds those sections, while §§9.2 and 12 bind certificates to device objects, closures and schedules. The proposal explains coordinate migration but does not state how those records belong to the device portion of a mixed binary. This is the required compatibility statement missing from the proposal, not a reopened objection to the accepted addressing rules. *Fix:* Append to z4c's 'Hashes, catalog and consumers': "In a mixed fat object, the new support coordinates belong to action or perm_action invocations within the linked device ISA object(s). Each affected device object's schedules and certificates use them under the existing object, closure and schedule bindings. Native host functions require neither these support coordinates nor ISA region entries in that device certificate. $construct and $release denote device action entry and exit, not native process entry and exit; this repair does not require the surrounding native binary to become an ISA object."
- **[codex] adg-4HT-1** (adg — Hashes, catalog and consumers; proposed ISA §§7.1 and 10 lifetime rules; contract): The C7/bennett-4ht standing check explicitly covers launch API decisions. adg fixes initialization, persistence, register identity and replay assumptions across launches, but never identifies how its 'loaded program' relates to the native host and device components of a mixed fat object. ISA §10 supplies a device CC entry and program handle, so the accepted mechanism can support that composition; the proposal still needs the required explicit application statement. The omission concerns launch-boundary scope, not the accepted core persistence semantics. *Fix:* Append to adg's 'Hashes, catalog and consumers': "In a mixed fat object, 'loaded program' means a loaded device program instance, not the native host process or entire fat binary. The native host may retain that instance and repeatedly invoke its device CC entries; the specified memory, allocation-table, bump-pointer and register-ledger persistence applies to that instance, with separate state for separate loaded instances. Loading a device program or closing or reversing a device run does not initialize or roll back unrelated native host state. This rule does not require moving native main, argv/envp handling or host-only libc into the device object. Later-entry certificate replay records the actual device entry-state preparation assumptions, without presuming a fresh native process."

## codex

z4c: FAIL (z4c-4HT-1)
adg: FAIL (adg-4HT-1)
checker-diagnostics: PASS
5u3: PASS

z4c needs explicit device scope for its address-bearing schedules/certificates; adg needs explicit device-instance scope for persistence across host launches. checker-diagnostics does not change certificate layout. 5u3 preserves exact analysis results and changes neither runtime handles nor host-memory transport; whole-program analysis does not require whole-program device execution. The accepted contract content remains accepted. Both blockers are missing bennett-4ht compatibility statements.

**Path to accept:** Add the following statements to each failing proposal's 'Hashes, catalog and consumers' section.

z4c: "In a mixed fat object, the new support coordinates belong to action or perm_action invocations within the linked device ISA object(s). Each affected device object's schedules and certificates use them under the existing object, closure and schedule bindings. Native host functions require neither these support coordinates nor ISA region entries in that device certificate. $construct and $release denote device action entry and exit, not native process entry and exit; this repair does not require the surrounding native binary to become an ISA object."

adg: "In a mixed fat object, 'loaded program' means a loaded device program instance, not the native host process or entire fat binary. The native host may retain that instance and repeatedly invoke its device CC entries; the specified memory, allocation-table, bump-pointer and register-ledger persistence applies to that instance, with separate state for separate loaded instances. Loading a device program or closing or reversing a device run does not initialize or roll back unrelated native host state. This rule does not require moving native main, argv/envp handling or host-only libc into the device object. Later-entry certificate replay records the actual device entry-state preparation assumptions, without presuming a fresh native process."

No launch ABI implementation, host shim or mixed-binary execution test is required for this acceptance.

- **C1 5**: Round-1 assessment retained: z4c preserves invocation-local region lifetime; adg specifies persistent device state under ISA §§3.3, 7.1 and 10. *Change:* No core change required by this re-check.
- **C2 5**: The accepted proposals add no instruction or change opcode semantics. *Change:* None required.
- **C3 5**: The accepted rules preserve unconditional region support, explicit reversal and existing ownership conditions. *Change:* None required.
- **C4 5**: z4c retains emitted leaves and their charges. 5u3 concerns analysis resources, not execution budgets or target limits. *Change:* None required.
- **C5 4**: Round-1 contract acceptance is retained. The affected interfaces are z4c's address-bearing schedules/certificates and adg's loaded-program launch lifecycle. *Change:* Add the device-object scoping statements specified in z4c-4HT-1 and adg-4HT-1.
- **C6 4**: The proposals distinguish derived witnesses and proposed conformance vectors from executed implementation checks. This re-check is a read-only clause review. *Change:* No additional execution or proof obligation is required for bennett-4ht.
- **C7 3**: z4c and adg touch listed boundary contracts without stating their mixed-fat-object use. checker-diagnostics changes only checker-report codes. 5u3 changes exact compile-time analysis representation, preserving runtime handle representation and the §5 analysis scope that already includes host functions exchanging data with device variants. *Change:* Add the two compatibility statements below; no addition is required for checker-diagnostics or 5u3.
- **C8 4**: The accepted diffs have precise insertion points and defaults. The remaining standing-check omissions can be repaired locally in the affected proposals' consumer notes. *Change:* Place each required statement in its proposal's 'Hashes, catalog and consumers' section.

Suggestions:
