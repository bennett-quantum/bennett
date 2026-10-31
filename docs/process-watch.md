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
