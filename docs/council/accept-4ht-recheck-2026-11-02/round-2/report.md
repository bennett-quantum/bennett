# Council — accept-4ht-recheck-2026-11-02 round 2

Document snapshot sha256 16c9f1a28cfa; rubric docs/council/rubric-isa.md. Members: codex. Scores are advisory.

| | codex | mean | spread ≥ 2 |
|---|---|---|---|
| C1 | 5 | 5.0 |  |
| C2 | 5 | 5.0 |  |
| C3 | 5 | 5.0 |  |
| C4 | 5 | 5.0 |  |
| C5 | 5 | 5.0 |  |
| C6 | 4 | 4.0 |  |
| C7 | 5 | 5.0 |  |
| C8 | 4 | 4.0 |  |

Overall mean: 4.75

Verdicts: **codex: accept**

Core verdicts: **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: codex: core 0 / contract 0 (blocking 0)

## Previous-round blockers, status

- [codex] z4c-4HT-1: **resolved** — The requested statement is present verbatim and explicitly scopes support coordinates, certificate inventory and action entry/exit to the device portion.
- [codex] adg-4HT-1: **resolved** — The requested statement is present verbatim and explicitly scopes persistence and replay assumptions to device instances while preserving native host state and responsibilities.

## Blocking issues

- none

## codex

z4c: PASS
adg: PASS
z4c-4HT-1 and adg-4HT-1 are resolved. The mixed fat object remains reachable under both proposals, and the additions introduce no regression. Acceptance is limited to the bennett-4ht re-check; previously accepted contract content is not reopened, and no launch implementation or host shim is required now.

**Path to accept:** No statements remain to be added. Both appended statements satisfy the standing check; preserve them when integrating the accepted proposals.

- **C1 5**: Accepted machine semantics remain intact. adg explicitly scopes memory, allocation-table, bump-pointer and register-ledger persistence to a loaded device instance, consistent with ISA §§3.3, 7.1 and 10. *Change:* None required for this re-check.
- **C2 5**: Neither addition changes instructions. z4c explicitly identifies $construct and $release as device action boundaries, preserving §4.6. *Change:* None required for this re-check.
- **C3 5**: The additions preserve the accepted construction and reversal rules. adg's exclusion of unrelated native host state from device rollback agrees with §7.4, §10 and T4. *Change:* None required for this re-check.
- **C4 5**: Accepted resource semantics remain unchanged. Neither addition introduces process-wide budgets or makes native host execution part of device resource accounting. *Change:* None required for this re-check.
- **C5 5**: z4c retains the device object, closure and schedule bindings of §§9.1–9.3, 11 and 12. adg applies §10's device CC entries and program-instance lifetime without requiring the native binary to become an ISA object. *Change:* None required for this re-check.
- **C6 4**: Round-1 assessment retained: both proposals distinguish proposed conformance vectors and hand derivations from executed implementation tests. The additions introduce no conflicting conformance claim. *Change:* Optional future conformance enhancement: exercise repeated device entries from one native host while checking that unrelated host state remains unchanged by device reversal.
- **C7 5**: Both pass bennett-4ht. z4c explicitly limits support coordinates and ISA certificate region entries to device objects. adg explicitly preserves native main, argv/envp handling and host-only libc, permits repeated device entry, separates loaded instances and binds later-entry replay to actual preparation assumptions. Neither equates the device object with the whole binary or changes native-comparison scope. *Change:* None; retain both appended mixed-fat-object statements.
- **C8 4**: Round-1 clarity assessment retained without reopening accepted contract content. Both appended statements identify their destination, device scope and host implications clearly. *Change:* Optional editorial integration: place each appended paragraph directly in its proposal's 'Hashes, catalog and consumers' section.

Suggestions:
