# Council — contract-adg-2026-11-02 round 2

Document snapshot sha256 dd9ce43076f1; rubric docs/council/rubric-isa.md. Members: sol, codex. Scores are advisory.

| | sol | codex | mean | spread ≥ 2 |
|---|---|---|---|---|
| C1 | 4 | 4 | 4.0 |  |
| C2 | 5 | 5 | 5.0 |  |
| C3 | 3 | 4 | 3.5 |  |
| C4 | 5 | 5 | 5.0 |  |
| C5 | 4 | 4 | 4.0 |  |
| C6 | 4 | 4 | 4.0 |  |
| C7 | 5 | 5 | 5.0 |  |
| C8 | 4 | 4 | 4.0 |  |

Overall mean: 4.31

Verdicts: **sol: revise**, **codex: revise**

Core verdicts: **sol: revise**, **codex: revise**

**Consensus: no**   **Core consensus: no**

Blocking by scope: sol: core 1 / contract 0 (blocking 1), codex: core 1 / contract 0 (blocking 1)

## Regressions reported

- **[sol]** The new program-shared device-state rule introduces reversal interference between runs with disjoint classical buffers unless device-model ownership is added (adg-R2-B1).

## Previous-round blockers, status

- [sol] adg-M1: **resolved** — Muse's §7.3 paragraph is present verbatim, §10 is scoped to program-lifetime state, and the required sequential device/entropy vectors are specified.
- [sol] adg-4HT-1: **resolved** — The accepted paragraph is verbatim and correctly extended to device-instance state and per-run device effects.
- [codex] adg-M1: **resolved** — Muse's §7.3 paragraph is reproduced verbatim; §10 is scoped to program-lifetime state, and the independent entropy/tape vectors are correct.
- [codex] adg-4HT-1: **resolved** — The accepted paragraph matches verbatim and is correctly extended to device-model state and run-associated tapes.

## Blocking issues

- **[sol] adg-R2-B1** (Recommended exact spec diff: §§7.3 and 10; interaction with §14.3 T4; core): *Fix:* In §§7.3/10, extend isolation to the newly shared models. Recommended rule: "At bennett_run, the run atomically acquires exclusive ownership of every console, clock and block model referenced by its entry's transitive CC/R call closure. Ownership lasts until CLOSED, including while COMPLETED, FAILED or REVERSED. If any required model is owned by another non-CLOSED run, bennett_run returns E_INVALID_STATE before executing the entry or acquiring ownership. Entropy positions and effect tapes remain per-run. Disjoint concurrent runs require disjoint model ownership sets as well as the existing register/memory conditions." Clarify §14.3: "Restoration concerns the run-owned state; state belonging exclusively to disjoint runs is unaffected." Add a §15 vector: after A reads clock 0 and completes without closing, B's conflicting launch returns E_INVALID_STATE, c remains 1 and B has no effects; after A closes, a new B reads 1, or reads 0 if A first reversed. A viable alternative is dynamic per-model ownership acquired at the first effect, retained until CLOSED, with a conflicting effect producing atomic terminal code 4; that alternative also needs an explicit §4.9 mapping. I recommend launch-time acquisition because it uses the existing launch-conflict status and prevents partial execution before discovering a model conflict.
  <1>1 A clock read increments c, and its reversal decrements c. An eligible COMPLETED run must reverse to its entry device-model state. Section 10's ownership and reverse-eligibility conditions name registers and memory, without making the clock counter an owned resource.  — clause:ISA §7.3 clock row; clause:ISA §10 States; clause:ISA §14.3 T4
  <1>2 The amendment makes c shared by all runs of a loaded program, preserves the existing ownership conditions and expressly preserves disjoint concurrent runs.  — witness:docs/notes/2026-11-02-rev3/adg.md, Recommended exact spec diff, §§7.3/10 additions
  <1>3 Use two disjoint live eight-byte globals and no quantum registers. A reads the clock into its buffer and reaches COMPLETED but remains open. B reads the clock into its other buffer, completes and closes. A then reverses. No stated register/memory ownership or reverse-eligibility condition excludes this sequence.  — clause:ISA §§7.3/10; witness:ABI sequence bennett_run(A), bennett_wait(A), bennett_run(B), bennett_wait(B), bennett_run_close(B), bennett_reverse(A)
  <1>4 Starting at c=0, A leaves c=1, B leaves c=2, and A's prescribed reversal leaves c=1 rather than A's entry value 0. The analogous console sequence A writes a5, B writes 5a, close B, reverse A pops B's byte and leaves A's byte.  — witness:python3 -c 'c=0; c+=1; c+=1; c-=1; print(c)' outputs 1; clause:ISA §7.3 console and clock reversal rows
  <1>5 The amended text therefore permits an eligible reversal that contradicts its explicit entry-state restoration guarantee. Atomic effects and separate effect tapes do not isolate the shared model state.  — step:<1>1; step:<1>2; step:<1>3; step:<1>4
- **[codex] adg-R2-1** (Recommended exact spec diff: §§7.3/10, interacting with §7.4 and §14.3 T4; core): *Fix:* In §§7.3/10, add an explicit ownership rule. Recommended conservative wording: “A run's device ownership footprint is the set of console, clock and block models referenced by the entry's transitive CC/R call closure. bennett_run acquires that footprint exclusively before execution and retains it until CLOSED, including while COMPLETED, FAILED or REVERSED. If another non-CLOSED run owns any model in the footprint, bennett_run returns E_INVALID_STATE before execution or any ownership acquisition. Entropy position and effect tapes are run-local and do not conflict. Runs with disjoint device footprints remain subject to the existing register and memory ownership rules.” In §14.3 T4, add: “For shared program state, restoration concerns the reversing run's owned components; disjoint components belonging to other runs remain unchanged.” Add the §15 overlap vector: B's initial launch is E_INVALID_STATE with no effects; after A is reversed and closed, retried B leaves console=5a; after A is closed unreversed, retried B leaves console=a55a. A second viable approach is a specified global device-dependency history with reverse-dependency ordering for both segment uncall and whole-run reversal, accompanied by revised eligibility rules. I recommend exclusive ownership because it preserves the existing local reversal machinery.
  <1>1 Console reversal pops the recorded number of bytes; clock reversal decrements c. Whole-run reversal traverses only that run's history. §10 grants exclusive ownership of registers and memory, and its reversal eligibility does not mention device interference. T4 promises device-state restoration.  — clause:ISA-7.3 device table; clause:ISA-7.4 history traversal; clause:ISA-10 States; clause:ISA-14.3 T4
  <1>2 The amendment makes console/clock/block state shared across runs of one loaded program, while retaining ownership wording limited to registers and memory and explicitly preserving disjoint concurrent runs.  — witness:docs/notes/2026-11-02-rev3/adg.md, Recommended exact spec diff, §7.3 and §10 additions
  <1>3 Use two disjoint live one-byte globals containing a5 and 5a. A's CC entry calls an R helper that writes a5 to the console, then completes but remains open. B writes 5a using its separate global, completes and closes. Neither run uses registers, measurement or unverified free. Reversing A is eligible under §10, but its one-byte pop leaves console=a5, whereas A entered with an empty console. The literal transition calculation is reproducible with the command cited here.  — witness:python3 -c 's=bytearray(); s.extend(bytes([0xa5])); s.extend(bytes([0x5a])); del s[-1:]; print(s.hex())' outputs a5
  <1>4 Thus the amended shared-state model admits a trace whose prescribed reversal contradicts T4 and removes another run's console byte. Atomic individual effects do not protect retained undo histories. The claim that no additional device synchronization rule is needed is unsound.  — step:<1>1; step:<1>2; step:<1>3

## sol

adg-M1 is resolved, and adg-4HT-1 remains resolved. The corrected citations, sequential results and conditional unchanged-hash claim check out. One new core S0 remains: shared device models lack isolation between open runs, allowing eligible reversal to contradict T4.

**Path to accept:** 1. Add explicit ownership acquisition, retention and conflict behavior for shared console/clock/block models. 2. Align the concurrency sentence and T4 restoration scope with that ownership. 3. Add the overlapping-open-run clock vector to §15. The existing sequential vectors and accepted fat-object statement can remain.

- **C1 4**: The proposed §§7.1/7.3 additions correctly distinguish program-lifetime memory and devices from per-run entropy position and tapes. However, shared device state is outside §10's stated register/memory ownership rule. *Change:* In §7.3, add: "The console sequence, clock counter and block sector map are exclusive program-state resources subject to the run ownership rules of §10." Specify acquisition and conflict handling as in adg-R2-B1.
- **C2 5**: The memory examples follow §7.1 exactly, including pinned globals, monotonic allocation, dead entries and table exhaustion. The device vectors follow §7.3's byte, cursor and sector-presence rules. *Change:* Optional §15 addition: "If A frees address 16 before closing, B still allocates at 17; the dead entry at 16 remains in the allocation table."
- **C3 3**: Sequential reversal and T4's quantum qualifications are handled correctly. With multiple open runs, the newly shared clock/console state can be changed by another run before eligible reversal, contradicting §§7.3/10 and T4. *Change:* In §10, state: "Ownership of a program-lifetime device model lasts until CLOSED, including while the owning run is COMPLETED, FAILED or REVERSED." Add the acquisition/conflict rule in adg-R2-B1.
- **C4 5**: The diff changes no target capability, resource formula, expansion recipe or budget tuple. Persistent allocation consumption preserves existing limits. *Change:* Optional §15 addition: "After allocations at 16, 17 and 18 across CLOSED runs, the next allocation faults with code 2; bump remains 19 and memory and table entries are unchanged."
- **C5 4**: Register and token lifetimes agree with §§3.3/5.4/10. Under the explicitly conditional in-version repair, §9.2's canonical bytes and envelope inputs remain unchanged. Launch isolation is incomplete for the new program-shared devices. *Change:* In §10, add: "A launch conflicting with another non-CLOSED run's device-model ownership returns E_INVALID_STATE before execution or ownership acquisition." Define the model set as in adg-R2-B1.
- **C6 4**: The sequential lifecycle vectors are precise and derivable. I reran the existing witness binary and reproduced all five expected lines; its source matches the note. This was not a fresh rebuild or repeated-launch ABI test. No overlapping-run vector checks the new sharing rule. *Change:* Add to §15: "With A COMPLETED but not CLOSED and owning the clock, a conflicting B launch returns E_INVALID_STATE without effects. After A closes, B reads 1; if A reverses before closing, B reads 0."
- **C7 5**: The accepted bennett-4ht paragraph is carried verbatim. Its extension correctly scopes console/clock/block state to the retained device instance and excludes unrelated native host I/O. The shared scope names the remaining container, launch and memory-mapping obligations. No North Star capability is removed. *Change:* No change required. Retain the accepted paragraph verbatim and the sentence: "The new console/clock/block rule has the same device-instance scope; its per-run tapes cover device R effects, not unrelated native host I/O."
- **C8 4**: The additions have valid anchors and clearly separate load, run, close and reversal. The §3.2/§3.3 citation is now correct. The assertion that unchanged ownership rules suffice is false for shared device models. *Change:* Replace §10's final concurrency sentence with: "Concurrent runs require disjoint register, memory and program-lifetime device-model ownership sets; entropy positions and effect tapes remain per-run."

Suggestions:
1. In §15 suite G, promote the note's allocator boundary examples into explicit vectors: freeing 16 does not prevent B allocating 17; after heap allocations at 16, 17 and 18, the next allocation faults with code 2 and leaves bump=19, bytes and table unchanged.

## codex

adg-M1 is resolved, the corrected citations and sequential results are valid, and the mixed-fat-object check passes. No canonical source, envelope or catalog bytes change under the authorized in-version repair. One new S0 remains: program-shared device state can be modified by another open run without violating the stated ownership rules, making run-local reversal contradict T4.

**Path to accept:** 1. Define exclusive ownership and conflict behavior for shared device models. 2. Scope T4 restoration to the reversing run's owned program-state components. 3. Add the overlapping-open-run console vector with the specified conflict and retry outcomes. The existing sequential vectors and hash policy can remain unchanged.

- **C1 4**: The additions correctly distinguish program-lifetime memory and console/clock/block state from per-run entropy position, tapes and environments. Shared devices, however, remain outside §10's explicit ownership rule. *Change:* In §§7.3/10, state: “Program-lifetime device models require exclusive run ownership through CLOSED; runs accessing the same model are not disjoint.” Specify acquisition and conflict handling as detailed in adg-R2-1.
- **C2 5**: The proposal preserves instruction semantics. The allocation addresses, four-entry table boundary, non-reclaiming free, device byte patterns and entropy results follow §§7.1/7.3. *Change:* No instruction change required; retain the existing allocation, effect-atomicity and reversal rules.
- **C3 4**: Sequential reversal and FAILED-prefix retention agree with §§4.9/7.4/10. Quantum restoration correctly retains T4's hypotheses. Overlapping open runs can nevertheless interleave shared device effects and invalidate T4. *Change:* After adding device ownership, qualify §14.3 T4: “For shared program state, restoration concerns the reversing run's owned components; disjoint components belonging to other runs remain unchanged.”
- **C4 5**: Heap/table limits, budgets, target capabilities, resource formulas and expansion recipes are unchanged. Persistent allocation consumption respects the existing allocator. *Change:* No resource or target amendment required.
- **C5 4**: Register and token lifetimes match §§3.3/5.4/10. Under an authorized in-version repair, none of §9.2's hashed inputs or catalog bytes changes. Launch conflict behavior for the newly shared device state remains undecided. *Change:* In §10, define a device-ownership footprint and state: “A bennett_run conflicting with another non-CLOSED run's device ownership returns E_INVALID_STATE before execution or acquisition of ownership.”
- **C6 4**: The sequential vectors are correct and sufficiently explicit. I confirmed the stored witness source matches the note and reran its existing executable: all five reported lines reproduced with exit 0. This was not a rebuild or a multi-launch test. The suite omits overlapping-open-run device reversal. *Change:* Add to §15 suite G: “After A writes console byte a5 and completes without closing, a conflicting B launch returns E_INVALID_STATE without effects. After reversing and closing A, retrying B writes 5a to an empty console; after merely closing A, retrying B leaves a55a.”
- **C7 5**: The accepted bennett-4ht paragraph is carried verbatim, verified against the accepted dossier. Its extension correctly scopes console/clock/block state and tapes to device instances/runs. Native host state, marked device closures and the remaining mixed-launch boundary obligations remain distinct. No north-star capability is removed. *Change:* No scope change required; preserve the accepted paragraph and its device-state extension.
- **C8 4**: The revised §3.2/§3.3 citation is correct, the insertion anchors exist, and the note accurately separates primitive execution evidence from lifecycle obligations. The accepted 4ht text is required at publication but lacks an explicit insertion anchor in the exact-diff section. *Change:* In “Recommended exact spec diff,” explicitly insert the accepted 4ht paragraph after §10's Model paragraph, followed by: “The console, clock and block state of §7.3 has the same device-instance scope; per-run tapes cover device effects, not unrelated native host I/O.”

Suggestions:
1. Recommended exact spec diff: give the accepted bennett-4ht paragraph an explicit publication anchor after §10's Model paragraph, followed by: “The console, clock and block state of §7.3 has the same device-instance scope; per-run tapes cover device effects, not unrelated native host I/O.”
