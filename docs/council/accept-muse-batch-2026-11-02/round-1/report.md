# Council — accept-muse-batch-2026-11-02 round 1

Document snapshot sha256 9bb2f1901ff3; rubric docs/council/rubric-isa.md. Members: muse. Scores are advisory.

| | muse | mean | spread ≥ 2 |
|---|---|---|---|
| C1 | 3 | 3.0 |  |
| C2 | 4 | 4.0 |  |
| C3 | 4 | 4.0 |  |
| C4 | 4 | 4.0 |  |
| C5 | 3 | 3.0 |  |
| C6 | 4 | 4.0 |  |
| C7 | 4 | 4.0 |  |
| C8 | 3 | 3.0 |  |

Overall mean: 3.62

Verdicts: **muse: revise**

Core verdicts: **muse: revise**

**Consensus: no**   **Core consensus: no**

Blocking by scope: muse: core 1 / contract 0 (blocking 1)

## Blocking issues

- **[muse] adg-M1** (ISA §7.3, §10 (adg diff); core): *Fix:* Section ISA §7.3 (new paragraph after the device table) and §10. The diff should add to §7.3 the sentence: 'Device-model state belongs to the loaded program like classical memory (§7.1): the console byte sequence, the clock counter c and the block sector map are established at load from their initial values (the block map from layout.block_image, K10) and persist across runs, changed only by effect execution and by reversal (§7.4, T4); closing a run does not reinitialise them. The entropy position p is per-run state: it starts at 0 over the entropy tape copied at that bennett_run (§10). The effect tape is per-run.' And in the §10 addition, replace 'initialization is never repeated merely to start a run' with 'the §7.1/§7.3 program-lifetime state is never reinitialised merely to start a run'. Corrected expected values for the new vectors: run A clock.read writes 0 (c becomes 1), COMPLETED, CLOSED unreversed; run B clock.read MUST write 1; if A is REVERSED before CLOSED, B writes 0. Run A block.write sector 2 then CLOSED unreversed; run B block.read sector 2 returns A's bytes; with A reversed, sector 2 is absent again and reads 512 zero bytes. Two ways out exist: (a) program-lifetime device state as above (recommended: matches T4 entry-value restoration, the block-as-disk device model of north-star rungs 3/6, and the proposal's own persistence principle); (b) per-run reinitialisation of all device state stated explicitly in §7.3 — viable but then the §10 sentence must be scoped to §7.1 state and the dialect/VM must not assume a persistent block device across entries. I would take (a).
  adg1 Device models have observable state with stated initial values but no stated lifetime; the entropy tape (hence position p) is supplied per run, while clock c and the block sector map are readable by later runs.  — clause:ISA-7.3 device table (State (initial): console empty, clock c=0, entropy p=0, block map from block_image); clause:ISA-10 (entropy tape copied at bennett_run, per-run; bennett_tape_open by run id)
  adg2 The adg diff pins load-time establishment and cross-run persistence only for classical memory, allocation table, bump pointer (§7.1) and the register ledger (§3.3); its §10 sentence 'initialization is never repeated merely to start a run' does not name device state, and read maximally it would also freeze the per-run entropy position.  — witness:adg recommended diff (dossier part adg, 'Recommended exact spec diff')
  adg3 On this input a persistence-reading executor returns clock=1 and A's sector bytes; a reinitialisation-reading executor returns clock=0 and 512 zero bytes. Both readings conform to the amended text.  — witness:sequential R entries on one loaded program: run A executes clock.read (writes 0, c=1) and block.write to an absent sector, COMPLETED then CLOSED without reversal; run B executes clock.read and block.read of that sector
  adg4 Conclusion: the defect adg exists to repair (load-time vs per-run initialisation) remains observable for clock and block after the diff is applied, and the unqualified §10 sentence is inconsistent for entropy p; two conformant executors compute different results (S0).  — step:adg1; step:adg2; step:adg3

## muse

z4c: ACCEPT
adg: BLOCK (adg-M1)
checker-diagnostics: ACCEPT
5u3: ACCEPT
z4c's defect, witness numbering (entry:1/entry:2 per §9.2 nested-line counting), traversal rule and hash claims all verify against ISA 0.9 and ref-0.9.json; the editor may apply it as a K repair. checker-diagnostics' disposition is correct (one misnumbered K citation, checker-S1, non-blocking). 5u3's coset mathematics and its refusal of verdict-changing caps are sound and keep rung 4 in scope. adg's memory/ledger persistence is the right and well-evidenced reading, but its diff leaves §7.3 clock/block device-state lifetime — observable on the second sequential launch — unsettled, and its unqualified §10 sentence would wrongly freeze the per-run entropy position; one paragraph (adg-M1) closes it.

**Path to accept:** adg (only blocked proposal), minimal ordered set: (1) add the §7.3 device-state lifetime paragraph quoted in adg-M1's fix (console/clock/block program-lifetime; entropy position and effect tape per-run); (2) scope the §10 sentence to 'the §7.1/§7.3 program-lifetime state'; (3) add the two conformance vectors with the expected values in adg-M1's fix (clock B=1 unreversed / 0 reversed; block sector persists unreversed / absent after reversal). With those three changes I accept adg and C1/C5/C8 each rise by one point. z4c, checker-diagnostics and 5u3 need no change to be applied; their suggestions are at the editor's discretion.

- **C1 3**: adg correctly pins §7.1 memory/table/bump and §3.3 ledger to loaded-program lifetime (§7.1 'Initial state' is indeed timing-silent; §10 l.2175-2176 and §3.3 'while the program is loaded' support persistence), but §7.3 clock/block state lifetime is left ambiguous (adg-M1). z4c does not disturb the state model. *Change:* Add the §7.3 device-state lifetime sentence of adg-M1 so every §3.2 state component has a stated load/run lifetime.
- **C2 4**: z4c's defect is real: §4.6 mandates unconditional function-entry/exit qregion support, §16.2/§9.2 numbering (nested lines counted in text order, so the witness declaration is entry:1 and X is entry:2, as the note says) admits nested declarations, K64 addresses exist only 'in their containing oracle' (§11), and K65 excludes implicit qregion restoration; the bound ref-0.9 qregion recipe already wraps the whole function body, confirming function scope. The diff addresses exactly the missing leaves. *Change:* State the $construct/$release ordinal correspondence under K62 source-adjoint formation (z4c-S1).
- **C3 4**: z4c keeps support unconditional (§3.5, §5.3 Control), numbering excludes body/callee subtrees as K64 does, raw inversion retains forward points/ordinals as K64/§11.1 require; no phase-unsafe or superposition-inspecting rule is introduced. 5u3's exactness requirement preserves all reference sets. *Change:* In z4c's text, name §5.3 Control (regions allocated unconditionally under ctl) alongside §3.5/§4.6.
- **C4 4**: No proposal changes resources, classes, target format or cost rules; z4c only labels pre-existing leaves (verified against ref-0.9.json: the qregion recipe and its leaf order are untouched, so the 'no ref-0.9.json/hash change' claim holds; only address-bearing schedule/certificate bytes for actions with local qregions change, as disclosed). *Change:* None required; retain z4c's statement that leaf set, order and charges are unchanged when the K entry is published.
- **C5 3**: z4c closes a genuine scheduler-contract hole with a deterministic traversal (text order, then-before-else, loop body once, reverse at release); checker-diagnostics correctly finds no E_CERT registry in §12 (§11 E_SCHEDULE_INFEASIBLE/K55 and §10 statuses/§5.4 fault codes are distinct interfaces, as claimed). adg's launch-lifetime contract remains incomplete for device state (adg-M1). *Change:* Apply adg-M1's §7.3 sentence; it is the only missing normative decision in the launch contract.
- **C6 4**: 5u3's worked mathematics is correct (subgroup generated by stride s in Z/2^W is gcd(s,2^W)Z; 2^64/8=2^61; W=8 stride 8 gives 32 offsets 0..248; seeds 0 and 4 give two mod-8 cosets, not *) and its hypotheses are explicit (unfiltered, one width, one provenance, PT2 index width preserved); the overriding 'exact least fixpoint' obligation makes the acceleration checkable. z4c/adg vectors are derivable and concrete. *Change:* Define the multi-vertex subgroup in 5u3 as generated by cycle-sum displacements (5u3-S1).
- **C7 4**: No proposal narrows north-star scope: z4c forbids no placement, adg's persistence is the reading dialect 0.3 §6.5/§6.6 require (qtab is a device-memory global with never-reused tags; handles 'MUST retain identity across entries'), 5u3 declines verdict-changing caps and keeps rung-4 SQLite in scope with bp-fj1 honestly open. Standing bennett-4ht check: z4c and adg carry adequate mixed-fat statements (device-object scope, not native process/argv/libc); checker-diagnostics and 5u3 decide none of the listed topics. *Change:* Add one-line mixed-fat-object non-interaction statements to checker-diagnostics and 5u3 when published (checker-S2).
- **C8 3**: z4c, checker-diagnostics and 5u3 are implementable as written (deterministic rules, honest non-claims about unrun tests). adg as written forces the VM and reference implementers to guess clock/block lifetime on the first repeated R entry — the exact failure the bead was filed to prevent. *Change:* Apply adg-M1; then a VM author and the reference owner can implement the lifecycle identically.

Suggestions:
