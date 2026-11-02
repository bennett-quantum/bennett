# Council — contract-adg-2026-11-02 round 1

Document snapshot sha256 95d0566084c2; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 5 | 5 | 5.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 4 | 4 | 4.0 |  |

Overall mean: 4.75

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Blocking issues

- none

## sol

The initialization ambiguity is real, and program-lifetime persistence repairs it consistently with existing ownership, reversal and cross-entry register semantics. The witness values are correct. The prose-only diff leaves canonical object/envelope inputs and catalog bytes unchanged. No S0 issue found; correct the §3.2/§3.3 citation and strengthen lifecycle verification.

**Path to accept:** Already acceptable. To raise C6 from 4 to 5, add and execute the specified multi-launch lifecycle vectors, comparing complete memory, allocation-table and bump state together with register ownership and token validity.

- **C1 5**: §7.1 specifies initial bytes, allocation entries and bump pointer without locating initialization in the load/run lifecycle. The proposed once-per-load rule resolves that ambiguity and determines both witness outcomes. *Change:* Optional precision in §7.1: state, “These persistence rules concern CC/R classical memory, allocation-table entries and the bump pointer.”
- **C2 5**: The witness follows §7.1: allocations at 16 and 17 fit the heap and use three of four table entries including g. Free does not reclaim storage. No opcode semantics change. *Change:* In the conformance vectors, add: “If A additionally frees address 16 before closing, B still allocates at 17.”
- **C3 5**: Retained failed prefixes agree with §4.9; explicit reversal agrees with §§7.4/10 and T4. Persistent register ownership remains distinct from ledger state, as §3.3 requires. *Change:* For clarity, replace §7.1’s proposed reversal sentence with: “If the preceding run was successfully REVERSED before being CLOSED, these classical components have their restored entry values; quantum-state restoration retains T4’s exactness hypotheses and error bounds.”
- **C4 5**: Persistence preserves existing heap and allocation-table limits. The diff changes no target descriptions, resource rules, catalog recipes or catalog binding. The 219-recipe catalog check passes with the published hash. *Change:* Add this boundary vector: “After allocations at 16, 17 and 18 across CLOSED runs, the fourth heap allocation faults with code 2 because the global plus three heap entries fill the table; bump remains 19.”
- **C5 5**: The diff fits §10’s ownership and CLOSED transitions and §3.3’s program-scoped register identities. §5.4 independently preserves the distinction between program-scoped host tokens and run-scoped device tokens. §9.2’s hashed inputs remain unchanged. *Change:* In the lifecycle vectors, state: “After A is CLOSED, its device-minted token is invalid and a launch using it returns E_ARG; a host-minted token remains valid until unload.”
- **C6 4**: The scalar outcomes independently reproduce as (7,17) and (0,16). The verification-index script passes, but its lifecycle check assigns those states directly rather than exercising consecutive launches. The note accurately discloses that limitation. *Change:* Append to §15 suite G: “Execute A and B in one loaded program instance; without reversal B returns (7,17), with successful A reversal B returns (0,16), and closing a FAILED A preserves its completed stores and allocations unless explicitly reversed.”
- **C7 5**: Persistence supports North Star §§3.1/5 and the dialect draft’s actual §§6.5–6.6 persistent-table and cross-entry identity requirements. The proposal introduces no capability refusal or demo-ladder restriction. *Change:* Optional normative clarification in §10: “This persistence rule does not prohibit disjoint concurrent runs permitted by the existing ownership rules.”
- **C8 4**: The diff is small and implementable. One citation is inaccurate: §3.2 lists the register ledger as a state component; §3.3 explicitly calls it the program’s register ledger. The substantive premise is supported by §3.3. *Change:* In “Defect and North Star scope,” replace the citation sentence with: “§3.3 places the register ledger at program scope; §3.2 lists it among machine-state components.”

Suggestions:
1. Correct the defect paragraph’s §3.2 citation: “§3.3 places the register ledger at program scope; §3.2 lists it among machine-state components.” This is a citation error, not a nonexistent defect.
2. In the proposed §7.1 addition, write: “If the preceding run was successfully REVERSED before being CLOSED, these classical components have their restored entry values; quantum-state restoration retains T4’s exactness hypotheses and error bounds.” This makes the intended reference to T4 explicit.
3. Add the lifecycle cases to §15 suite G and execute them through consecutive launches in one loaded instance. Expected post-B state without reversal: g=7, bump=18, live heap entries at 16 and 17. With A reversed: g=0, bump=17, only B’s live heap entry at 16. Distinguish a conflicting host launch argument, which returns E_INVALID_STATE, from an executed qreg.from_id ownership violation, which produces terminal code 4.

## codex

Accept as a 0.9 K repair. The initialization ambiguity is real, persistence resolves it consistently, and the proposed results are correct. No S0 defect, scope narrowing or canonical-byte change was found. Correct the §3.2 attribution to §3.3.

**Path to accept:** Already acceptable. To raise C6 from 4 to 5, extend the lifecycle vectors with the complete allocation states specified above and explicit token-validity outcomes, then exercise them through a multi-launch implementation when available.

- **C1 5**: §7.1 specifies initial contents but not their initialization event. The diff supplies that event and preserves memory, allocation entries and bump position across sequential launches. The witness respects both heap and table limits. *Change:* No semantic change required.
- **C2 5**: The proposal preserves alloc/free semantics: allocations return 16 then 17; free neither reclaims storage nor removes a table entry. No instruction changes are needed. *Change:* No change required to §4.
- **C3 5**: Closing and reversing remain distinct. FAILED-prefix retention agrees with §§4.9, 7.4 and 10. Restoration invokes T4, including its quantum-exactness qualifications. Oracle-local initialization and cleanup remain governed by §5.2. *Change:* No semantic change required.
- **C4 5**: No target capabilities, accounting formulas, budgets or expansion recipes change. Persistent allocation consumption follows the existing §7.1 allocator. *Change:* No change required to §8 or the reference catalog.
- **C5 5**: The diff retains §10 exclusive ownership and §3.3 program-scoped identities. E_INVALID_STATE already exists. Under the proposed in-version repair, §9.2 canonical inputs remain unchanged. The catalog check passes with 219 recipes and envelope hash 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197. *Change:* In 'Hashes, catalog and consumers', make the publication condition explicit: 'Under the council-authorized in-version 0.9 K repair, canonical source, envelope, target and catalog bytes remain unchanged.'
- **C6 4**: The scalar witnesses agree with §§7.1/7.4 and T4, and the supplied verification script passes. Its adg checks assign the expected scalar states directly; they do not exercise allocation-table, ledger, token or multi-launch executor behavior. The note accurately discloses this limitation. *Change:* In 'Conformance vectors and verification', add complete expected states: after unreversed A and completed B, bump=18 and table=[(1,1,1,1),(16,1,1,0),(17,1,1,0)]; after reversed A and completed B, bump=17 and table=[(1,1,1,1),(16,1,1,0)], using (base,size,live,pinned). The respective results remain (7,17) and (0,16).
- **C7 5**: Dialect draft §§6.5–6.6 explicitly require persistent table lookup and parameter/result identities across entries. The repair supports the North Star REPL and register lifetimes without restricting repeated oracle or kernel invocations. *Change:* No scope change required.
- **C8 4**: The exact diff is small and implementable. One supporting citation is misnumbered: §3.2 lists the ledger, whereas §3.3 establishes the program's ledger and loaded-program id lifetime. The substantive premise is supported. *Change:* In 'Defect and North Star scope', replace the attribution with: '§3.2 lists the register ledger as machine state; §3.3 places it at program scope and prohibits id reassignment while the program is loaded.'

Suggestions:
1. Defect and North Star scope: replace '§3.2 places the register ledger at program scope' with '§3.3 defines the program’s register ledger and its loaded-program id lifetime.' This is a citation correction; the claimed lifetime does exist.
2. Recommended exact spec diff, §§7.1/10: make the antecedent explicit by writing 'For sequential launches, the new run inherits these classical-memory components from the preceding CLOSED run' and 'These program-owned components are not reinitialized merely to start a run.' This avoids suggesting that dynamic environments, histories or oracle-local workspace persist.
3. Conformance vectors and verification: state the token expectations explicitly: 'A host-minted token remains valid across CLOSED runs until unload; a device-minted token becomes invalid at its run’s CLOSED transition, and passing it to a later bennett_run returns E_ARG.' For register lookup, distinguish 'an owned QREG launch argument returns E_INVALID_STATE' from 'an executed qreg.from_id encountering another open run’s ownership produces terminal fault code 4'.
4. Hashes, catalog and consumers: state 'No hash re-pin is needed under the authorized in-version 0.9 K repair; a full ISA-version bump changes the §9.2 envelopes and requires new pins.' The verification index already supplies this qualification; repeating it makes this note self-contained.
