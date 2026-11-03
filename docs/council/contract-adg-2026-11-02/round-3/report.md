# Council — contract-adg-2026-11-02 round 3

Document snapshot sha256 79bb33bdd3b0; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 5 | 5 | 5.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 5 | 5 | 5.0 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 5 | 5 | 5.0 |  |
| C6 | 4 | 5 | 4.5 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 4 | 4 | 4.0 |  |

Overall mean: 4.81

Verdicts: **sol: accept**, **codex: accept**

Core verdicts: **sol: accept**, **codex: accept**

**Consensus: YES**   **Core consensus: YES**

Blocking by scope: sol: core 0 / contract 0 (blocking 0), codex: core 0 / contract 0 (blocking 0)

## Regressions reported

- **[codex]** Editorial only: the release synopsis's section list was complete in round 2 but now omits the new §14.3 amendment.

## Previous-round blockers, status

- [sol] adg-R2-B1: **resolved** — Launch-time atomic ownership, retention through CLOSED, conflict behavior, T4 scoping and overlap vectors implement the requested fix.
- [sol] adg-R2-1: **resolved** — B cannot modify A's owned console/clock/block state before A closes; the former console-pop counterexample is excluded.
- [sol] adg-M1: **resolved** — Muse's paragraph remains verbatim; devices persist, while entropy position starts at zero and effect tapes remain per-run.
- [sol] adg-4HT-1: **resolved** — The accepted statement is carried verbatim and correctly extended to persistent device models and run-associated device tapes.
- [codex] adg-R2-1: **resolved** — Launch-time exclusive model ownership through CLOSED excludes the interfering console trace; T4 and retry vectors are corrected.
- [codex] adg-R2-B1: **resolved** — The requested atomic transitive-footprint rule and run-owned restoration scope are present verbatim, with clock, console, block and disjoint-run vectors.
- [codex] adg-M1: **resolved** — Muse's paragraph is preserved verbatim; program-lifetime devices and per-run p=0/tapes remain correctly separated.
- [codex] adg-4HT-1: **resolved** — The accepted paragraph is verbatim and correctly extended to device state without including unrelated native host state.

## Blocking issues

- none

## sol

adg-R2-B1 and adg-R2-1 are resolved; adg-M1 and adg-4HT-1 remain resolved. The cited technical premises, witness values and conditional unchanged-hash claim verify against ISA 0.9. No new S0 issue or regression was found. Accept as the proposed in-version K repair; actual multi-launch conformance remains implementation follow-through.

**Path to accept:** Already acceptable. To raise C8 from 4 to 5, provide the explicit §10 publication anchor for the accepted 4ht paragraph and update the release/verification wording to include the T4 amendment.

- **C1 5**: The §§7.1/7.3/10 additions distinguish program-lifetime memory, ledger and devices from per-run entropy position, tapes and history. The corrected §3.3 attribution is supported by the loaded-program id rules. *Change:* None required; retain the explicit load/run lifetime distinction and ownership through CLOSED.
- **C2 5**: Instruction semantics remain unchanged. Allocation addresses, table capacity, non-reclaiming free, device bytes and entropy values agree with §§4.9/7.1/7.3. *Change:* None required; retain §7.3 effect atomicity and the existing instruction fault mappings.
- **C3 5**: Exclusive acquisition of the complete transitive device footprint prevents cross-run interference with retained undo histories. Ownership survives COMPLETED, FAILED and REVERSED; the T4 addition correctly scopes restoration without weakening its quantum hypotheses. *Change:* None required; retain the launch-conflict rule and T4 sentence exactly as proposed.
- **C4 5**: The repair changes no target capability, resource component, expansion recipe, budget unit or charge. Device ownership is a launch constraint over existing models. *Change:* None required in §§8/11; preserve the existing target and resource contracts.
- **C5 5**: The linked CC/R closure determines the device footprint without a new object field. Existing E_INVALID_STATE expresses conflicts. Section 9.2 envelope inputs and catalog bytes remain unchanged under the expressly conditional in-version repair; consumer migration is described. *Change:* None required; retain the in-version authorization condition and the instruction that resetting consumers separate load from run lifecycles.
- **C6 4**: T4 retains explicit eligibility, exactness, audit and observed-event qualifications. Suite G specifies reproducible lifecycle and overlap outcomes. The document check and 64-footprint-pair model passed; the matching prebuilt interpreter witness reproduced all five lines. Actual multi-launch ABI execution remains unverified, as disclosed. *Change:* For §15 suite G implementation, require: “Lifecycle and overlap vectors use distinct bennett_run invocations on one retained loaded instance.” Publish complete state comparisons, including B's initial E_INVALID_STATE, unchanged c=1/console=a5, and the two specified retry outcomes.
- **C7 5**: The accepted bennett-4ht paragraph matches verbatim. Its extension correctly gives persistent devices the same device-instance scope and excludes unrelated native I/O. Marked device closures, persistent handles and all demo rungs remain reachable. *Change:* None required; preserve the accepted paragraph and its explicit device-state extension.
- **C8 4**: The normative repair is implementable, and all six amendment blocks apply at their cited anchors in memory. Publication instructions still lack an explicit location for the accepted 4ht paragraph, and inherited verification/release bookkeeping omits the new T4 insertion. *Change:* In Recommended exact spec diff, state: “Insert the accepted bennett-4ht paragraph after §10's Model paragraph, followed by the device-instance scoping sentence.” Update Release and after acceptance to name §14.3 explicitly.

Suggestions:
1. Recommended exact spec diff, §10: explicitly instruct publication of the accepted 4ht paragraph after Model, followed by: “The console, clock and block state of §7.3 has the same device-instance scope; per-run tapes cover device effects, not unrelated native host I/O.”
2. Verification result: replace the stale four-insertion/six-link claim with: “All proposed insertions apply at their stated anchors, fences balance and local links resolve.” Release and after acceptance should say: “Recommend a 0.9 K repair to §§7.1, 7.3, 10 and 14.3, with §15 lifecycle vectors and a §0.2 entry.”

## codex

adg-R2-1 and adg-R2-B1 are resolved; adg-M1 and adg-4HT-1 remain resolved. The cited premises, lifecycle values and conditional unchanged-hash claim check out. No S0 remains. Actual multi-launch ABI conformance remains implementation work, explicitly acknowledged by the proposal.

**Path to accept:** Already acceptable. Align the release instructions as specified under C8 to raise the lowest score from 4 to 5.

- **C1 5**: The §§7.1/7.3 additions distinguish program-owned memory and devices from per-run entropy position, tapes and history. The §3.3 ledger citation is correct; §3.2 lists state components. *Change:* None required within this proposal's scope.
- **C2 5**: The repair preserves §7.3 effect operations and inverses, §7.1 allocation/free semantics and §4.9 fault mapping. Launch conflicts correctly use the existing E_INVALID_STATE status. *Change:* None required; retain the existing instruction semantics.
- **C3 5**: Exclusive model ownership through CLOSED prevents interference with both segment uncall and whole-run reversal under §7.4. The T4 addition scopes restoration without removing its quantum exactness, error-bound or observed-event qualifications. *Change:* None required within this proposal's scope.
- **C4 5**: The diff changes no resource formulas, target capabilities, expansion recipes or catalog entries. Device ownership is a launch-admission condition and preserves execution of sequential programs. *Change:* None required; no target or catalog amendment is needed.
- **C5 5**: The §10 addition specifies the transitive footprint, atomic acquisition, conflict status and retention in COMPLETED, FAILED and REVERSED states. Register/token lifetimes agree with §§3.3/5.4/10. Inspection of §9.2 confirms unchanged hash inputs under the explicitly conditional in-version repair. *Change:* None required within this proposal's scope.
- **C6 5**: The sequential memory/device values and overlapping-run outcomes follow from the cited clauses. The document check and all 64 footprint-pair checks passed. The existing witness executable reproduced all five expected lines; its source matches the note. No rebuild or actual multi-launch ABI validation was performed, consistent with the note's limits. *Change:* None required for specification acceptance; retain the stated actual-ABI suite G obligations.
- **C7 5**: The bennett-4ht paragraph matches the accepted dossier verbatim and correctly extends device-instance scope to console/clock/block state and run-associated tapes. Native host state remains outside reversal. Persistent handles agree with dialect §§6.5–6.6; no north-star capability is removed. *Change:* None required; preserve the accepted mixed-object paragraph and its device-state extension.
- **C8 4**: The complete diff is implementable and separates evidence from future conformance work. The release synopsis omits the newly added §14.3 amendment and does not give an insertion anchor for the accepted mixed-object paragraph. *Change:* In 'Release and after acceptance', replace the opening sentence with: 'Apply the in-version 0.9 K repair to §§7.1, 7.3, 10, 14.3 and 15, record it in §0.2, and append the accepted bennett-4ht paragraph verbatim after §10’s Model paragraph.'

Suggestions:
1. In 'Release and after acceptance', state: 'Apply the in-version 0.9 K repair to §§7.1, 7.3, 10, 14.3 and 15, record it in §0.2, and append the accepted bennett-4ht paragraph verbatim after §10’s Model paragraph.' This aligns publication instructions with the complete diff.
