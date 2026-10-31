# Process watch: what each ceremony costs against what it has bought (newest last)

## 2026-10-31 ~08:00Z (first run, skim-level, capped at 15 tool calls)

1. **Council fix loop: shrink to one reviewer (astra) per fix round; bring sol back only for the acceptance vote.** Every sol blocker in isa-ref R9–R12 and dialect R8 was also raised by astra, or was the same kind of problem in another place. Each member reads a ~2 MB prompt. In R12, astra's 3 points bought one finding sol missed (R12-B02, an over-strict ban on names). R11-B02 and R12-B01 are the same dotted-name layout bug, patched one spot at a time. A generated test over dotted NAMEs and layout keys should replace round 13.
2. **One commit per council round, not four.** The meta repo has 46 `council` commits since 10-29 (prepare, collect ×2, aggregate).
3. **Cut `reference-interpreter/PROGRESS.md` (1,874 lines) to its "Resume here" block, which starts at line 1806.** The round 2–4 sections repeat response.md and git log.
4. **Cut `bennett/HANDOFF.md` to the current state block.** Three stacked "Orchestrator session block" sections each say "read this one first". The worklog keeps history.
5. **Drop the S0/S1 severity field from the council schema.** All 34 blockers in the rounds I read are S0, so the field tells us nothing.
6. **Make suite/ the interpreter's only copy of the 16 fixtures, or cut it.** It has no user yet. bennett-conformance's pre-push runs only `cargo test` in checker/, and nothing runs `suite/run.py` or the Python tests.
7. **Shrink rule 12 (bennett-conformance) to the check the runner already does, and delete the `proofs/` and `defects/` READMEs until a first proof or defect exists.** The runner only checks that tags look like `ISA-4.5`; it never checks them against clauses/. Both directories hold only a README.

**Keep, it earned it**
- Council with the astra seat on new semantics: R9 found borrow facts being erased (R9-B01) and a loop reusing physical names (R9-B02). Dialect R8 found that bitcast is not a lane-by-lane copy and that alloca contents are never seeded. Both would have bitten silently. The orchestrator's split (R9 and D8 real, R11–12 mostly patch fixes) holds. R10 was mixed.
- Quota pacing with each child's cost logged: it caught the 3-point astra R12 review and paused launches (HANDOFF, 03:24Z).

**Trend:** first entry, so no baseline yet. Recording is growing faster than defects are found: 3,183 lines of PROGRESS files in bennett-isa-spec against 3 blockers in round 12.

## 2026-10-31 ~18:00Z (second run, skim-level, 15 tool calls)

1. **Statement layer: keep the IDs, stop maintaining the output files.** The IDs earn their place: proofs cite 230, isa-09 R1 steps 42 and `[deps:]` 264, and all resolve. The rest does not. `clauses/` holds 6.9 MB of committed output. The 2,840 dialect statements are cited nowhere. The `.dot` files have no reader because Graphviz is absent. "Strong coverage 150" feeds no gate. Classifier rules K12–K16 and a retag served only the tool. Generate on demand and pause classifier tuning.
2. **Cut `bennett-isa-spec/spec/isa-0.9.PROGRESS.md` (1,380 lines) to its resume block.** Today's six sections repeat the K29–K61 commits, the same problem as the 0.8 file.
3. **Cut the committed `isa-0.8-to-0.9.diff` and its byte-compare.** Its only reader is the test that keeps it current, and it broke the gate on paths and mtimes. Shrink the `propos(al|ed|es)` ban (`draft_witnesses.py:239`) to the actual placeholder; it fired on the ordinary phrase "proposed inverse".
4. **isa-09 round 2: one seat.** In R1, sol and astra returned the same two spec gaps (G01, G02).
5. **Rule 12 `[deps:]`: shrink to new requirement sentences.** 101 markers have caught nothing, and placing the rule took three commits. The tool infers the other edges. Cut it if the next pass still finds no catch.
6. **Council `steps`: shrink to step-1 citation, `kind`, witness and fix.** R13–R17 blockers already opened with a reproduction. The `<1>n` numbering, the 3–6 step count and `step:` chaining only change the layout.

**Keep, it earned it**
- Proofs, which are used rather than admired. INV-5 1.4.3 withdrew the R18 remedy (R19 report) and drove spec commits f78a759, 91c60dd and 3981258. K29–K61 closed every refuted or ASSUMED step except two.
- ASSUMED step 1 → `kind: spec-gap`. In isa-09 R1 it routed 4 of 6 items to the editor instead of to an interpreter patch.
- One reviewer on fix rounds. R13–R19 reached an accept single-seat, saving seven sol reads of ~2.5 MB.

**Trend:** last entry's cuts held: HANDOFF is 38 lines and fix rounds run single-seat. Five proofs refuted 8 steps; council rounds find 1–2 blockers. The new growth is generated output without readers: dialect statements, `.dot` files, coverage counts and the committed diff.

## 2026-10-31 ~12:50Z (third run; the orchestrator had mis-stamped this as 2026-11-01 03:00Z, skim-level, 14 tool calls)

1. **Rule 12 `[deps:]`: cut, and close bead 82i.** The markers caught errors only in themselves. In isa-09 R1, SOL S1 found stale P21 targets, which produced K66 (marker retargeting only) and open bead 82i (audit the K1–K27 markers). In dialect R10, SOL-R10-S1 found four markers naming ISA 0.8 clauses that do not exist, and nothing followed. No marker changed a decision.
2. **`bennett/HANDOFF.md`: one Running/Next/Waiting block, rewritten only at session end.** It had 16 commits in 24h, yet it says K64/K65 both "await ratification" and are "ratified", says "collect round 22" after R24 accepted, and lists plugin M1 as both Running and Held. Its "03:00Z" stamp sits on a 12:53Z commit. The conformance HANDOFF still lists INV-1..4 and an import already done. Nobody reads these closely.
3. **Council `steps`: drop the requirement, keep `kind`.** R20–R24: 8 blockers, all `implementation`, every step 1 a section cite (`clause:ISA-3.3`), 0 spec gaps. isa-09 R2–R4 and dialect R10: 0 blockers. ASSUMED → spec-gap fired once (isa-09 R1) and relabelled INV-5 gaps 3/8, already open as 8ka/23g. I withdraw last pass's credit.
4. **`isa-0.9.PROGRESS.md`: carry out verdict 2.** It was taken but grew from 1,380 to 1,695 lines and has no resume block. 55 of 98 isa-spec commits in 24h touch worklog/PROGRESS, and the "record dispositions" commits repeat response.md.
5. **Acceptance tail: at the second host-resource blocker, build the sweep before voting again.** The R23 injector (64 scenarios/340 stages) closed the class. Built at R21, it would have saved the host-resource halves of R22–R23 (~4 seats).
6. **Proof → K rows: check existing text first, and let a consumer choose the next pass.** isa-09 R4 found 3 of 12 INV-6 gaps already closed by K13. No code cites K29–K75: the interpreter is 0.8, and the VM has been held since 10-30.

**Keep, it earned it**
- Proofs: INV-6 §1.3.4 decided the R22 role-sensitive coverage fix (`claims.rs`).
- Two-seat acceptance votes on semantics: codex missed SOL-R22-B01 (a false certificate); sol missed CODEX-R21-B02 and CODEX-R22-B01.
- Outline with numbered rulings: D01–D22 became 0.2.11 in one pass; R10 had 0 blockers from both seats.

**Trend:** pass-1 cuts held (interpreter PROGRESS 1,874→100 lines). Half of pass 2's cuts landed. The councils converge (0 blockers across five spec rounds) and the records do not: churn moved from PROGRESS into a HANDOFF that is now less accurate.

**Maintainer decision (2026-10-31):** all six verdicts adopted as recommended by the orchestrator (item 2 as "session-end only"); recorded in docs/council/README.md.
