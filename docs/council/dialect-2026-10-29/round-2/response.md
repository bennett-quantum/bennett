# Round-2 response — dialect 0.2.3

ISA grading target remains 0.8. No declines. Derivations below precede each edit; witnesses execute through independent LLVM/native/Rust executors. A passing blocker verdict does not assert the absent ISA capability executes.

## SOL-R2-03 — resolved

- Section: §12.6.
- Hand derivation: Packed bytes are 0x5566778811223344; destination lane 1 is bits 16..31 = 4386. Lane count/width changes cannot be elementwise.
- Text now: Pack and resegment in datalayout order, retain both loads; scalar↔vector supported.
- Witness: `n-bitcast-lanes, n-bitcast-scalar`. Checker: parse, normalise, native.

## SOL-R2-04 — resolved

- Section: §12.6.
- Hand derivation: False selector lane chooses 9; a product with start 3 and only active value 5 is 15, not zero.
- Text now: Selector rules precede inactive-zero; merge preserves false values beyond evl; reductions skip inactive lanes.
- Witness: `n-vp-merge, n-vp-select, n-vp-product`. Checker: parse, normalise, native.

## R2-CODEX-04 — resolved

- Section: §12.2, §12.4.
- Hand derivation: N12 flag totalisation is intermediate; N27 removes the intrinsic, so the old positive contradicts V4.
- Text now: Full output uses runtime helpers; false and true residual intrinsics reject. f(0)=16 and f(1)=7 are unchanged.
- Witness: `n-defined-zero (corrected plus native), validator-v4-clean (corrected), validator-v4-false-residue`. Checker: parse, normalise, recognise, native.

## REG-CODEX-N27 — resolved

- Section: §12.2, §12.4.
- Hand derivation: Same introduced boundary contradiction as R2-CODEX-04.
- Text now: Resolved with the full N12→N27 pipeline, rather than reverting totalisation.
- Witness: `n-defined-zero, validator-v4-false-residue`. Checker: normalise, recognise, native.

## SOL-R2-02 — resolved

- Section: §8.5, §16.2.
- Hand derivation: Bump after caller malloc(16) is 16; next address is 4096+16=4112. Another caller allocation advances it to 4128. Empty LLVM byte reads do not mean empty metadata reads.
- Text now: Replay allocation history/liveness independently of bytes before private allocations; relevant allocator/stack mutations invalidate cache.
- Witness: `entry-allocation-only`. Checker: state (native).

## R2-CODEX-02 — resolved

- Section: §8.5, §16.2.
- Hand derivation: With caller heap already consuming 16, limit 16 leaves no room: allocation faults 2, payload zero.
- Text now: Same complete-table default as SOL-R2-02; caller state remains unchanged.
- Witness: `entry-allocation-only`. Checker: state (native).

## R2-CODEX-01 — resolved

- Section: TDL-4, §16.4.
- Hand derivation: Physical coh contains 0102 (=513), but neither live one-byte object contains [0,2), so fault 7 must precede access.
- Text now: Logical base/size/live check is distinct from physical bounds; materialised helper is charged, store mutation is success-gated, metadata transfers/allocator updates are explicit. Static containment may discharge it.
- Witness: `arena-logical-bounds`. Checker: state (Rust run-oracle helper; native dead/padding/store probes).

## SOL-R2-01 — resolved

- Section: TDL-9, §18.4.
- Hand derivation: One step records qalloc; exhaustion before the gate never reaches qfree, so unconditional source leak checking was wrong.
- Text now: Cancel the unapplied composite and provisional allocations outside budget; preserve foreign handles and emit only controlled fault. Failed f skips use.
- Witness: `generation-cancel`. Checker: state/native.

## REG-SOL-TDL9 — resolved

- Section: TDL-9, §18.4.
- Hand derivation: Same newly introduced exhaustion/leak interaction.
- Text now: Successful source completion still enforces T-LEAK; exhaustion finalizes by cancellation.
- Witness: `generation-cancel`. Checker: state/native.

## R2-CODEX-03 — resolved

- Section: TDL-2.
- Hand derivation: Parent speculative store gives t=9 before child generation; delayed application does not mean the child sees entry shadow 0.
- Text now: Nested ctrl/adj/compute inherit visible classical recorder updates in order; outer control is added at composition; siblings remain isolated.
- Witness: `nested-cl-view` state and checked TDL event list. Checker: state/native + Rust run-action.

## BD3-1 — resolved

- Section: TDL-8, §18.4.
- Hand derivation: Faulting f is nonzero; freeing after combine traps cleanliness, while retaining without a release point leaks.
- Text now: Declare fault outputs, exempt invocation leaks, retain to program end and report combined statistics once; measure/correct/free there. Clean f reused by adjoint may then be released.
- Witness: `fault-output-lifetime`. Checker: state/Rust run-action and branch-conditioned release.

## BD3-2 — resolved

- Section: TDL-7, TDL-10, §18.2.
- Hand derivation: Flat reverse first uses uncomputed flags. For n=2 a forward flag preparation must precede two inverse increments.
- Text now: Structured loop adjoint computes flags before inverse bodies and cleans in reverse; compute reuses flags. Explicit retained controls are distinct from incidental workspace; preserve overwritten trajectory inputs.
- Witness: `co-loop-adjoint`. Checker: state/Rust run-action incl standalone inverse and compute checkpoints.

## BD3-3 — resolved

- Section: §7.5(a), §7.7, §18.2.
- Hand derivation: Copying |+> to a record then H gives a uniform q marginal; erasing the record gives interference and changes the channel.
- Text now: Deferred record qcopy never becomes quncopy; adj allocates a retained record before consumers, compute reuses/retains it to boundary.
- Witness: `deferred-channel-adj`. Checker: state/Rust run-action.

## REG-MUSE-7.7 — resolved

- Section: §7.7.
- Hand derivation: The old nonnormative release note contradicted retain-to-boundary.
- Text now: Note now states retention and boundary measurement on adj/compute too.
- Witness: `deferred-channel-adj`. Checker: state/Rust run-action.

## BD3-6 — resolved

- Section: TDL-2, TDL-11.
- Hand derivation: Co arena is authoritative: shadow-only store loses the write, and free/reuse carries garbage.
- Text now: All CC accesses guard Co; observed bytes may be written consistently; dirty Co release traps 4 before reuse unless restored then dematerialised.
- Witness: `co-store-release`. Checker: state/native lifecycle.

## BD3-4 — resolved

- Section: §1.6, §11.5, §17.5–§17.6, §25.1; seven R examples.
- Hand derivation: N34 inserts a typed budget fault point in every R entry. A successful run cannot prove the module free of this capability dependency.
- Text now: Every R entry is BLK-5 on ISA 0.8; direct reversible calls inside generation are excluded. R fallback uses generic trap without hostcall only when a typed-fault execution is reached, preserving successful paths. Required ISA 0.9 K5: literal 0≤C<2^64, exact nonzero C (zero→4), one terminal FAILED record, no successor effects, intact reversible prefix and cause table.
- Witness: Seven retagged R source examples and blocker lines; positive CC sjlj/fiber companions retain N29/N30 acceptance; existing success run/state/cc-run expectations unchanged. Checker: recognise, blocker, frontend, cc-run, run-program, state.

## BD3-5 — resolved

- Section: §6.5, §7.5(b).
- Hand derivation: The setjmp second return repeats the allocation while the first h remains live, despite no source CFG back edge to the site. N=1 is unsound.
- Text now: Chose the explicitly permitted simple reference default: if a setjmp continuation can reach s, not self-disjoint and E(s)=infinity. BLK-1 (R hoisting BLK-4), with bounded file fallback. This preserves the source capability and never aliases two live handles. It does not claim a finite N=2 analysis.
- Witness: handle-setjmp-reentry, including source, blocker and state; native setjmp confirms two distinct instances and balanced release. Checker: parse, recognise, blocker, state/native.

## E-MUSE-TERM — resolved

- Section: §2 Terminology.
- Hand derivation: BLK-3 is retired and BLK-5 is active; 1-to-4 is no longer the active set.
- Text now: Names BLK-1, BLK-2, BLK-4 and BLK-5, with BLK-3 explicitly retired.
- Witness: All active blocker witnesses retained, with expanded BLK-5 classification reports. Checker: blocker, xrefs.

## E-MUSE-7.7 — resolved

- Section: §7.7.
- Hand derivation: The obsolete release note conflicts with the retained measurement-channel rule.
- Text now: Retain and measure at the §7.5(a) boundary, including adj/compute; also indexed as REG-MUSE-7.7.
- Witness: deferred-channel-adj Checker: state/Rust run-action.

The BD3-5 finite-bound refinement is optional follow-up for the maintainer, b-dialect-spec-egm. The normative conservative default and its fallback are resolved in this pass. ISA-7 remains the external dependency b-dialect-spec-bz6; no ISA source was edited. No declines or partial resolutions.

## Regression/editorial identity mapping

`REG-SOL-TDL9` = sol regressions[0]; `REG-CODEX-N27` = codex regressions[0];
`REG-MUSE-7.7` = muse regressions[0]. `E-MUSE-7.7` records the same obsolete
note as an editorial item; `E-MUSE-TERM` = muse regressions[1]/suggestions[0].
This accounts for all 14 S0 ids, three regression reports and both editorial items.

Implementation commits: f868741 (normalisation/memory), 2fa3460 (action lifecycle),
a9e9563 (R-entry/instance-bound classification). Response commits ff50287, c7719d7,
446548d. Final consistency fixes preserve N27's canonical abs compare/sub/select
expansion, explicitly cross-reference BLK-5 from §1.6 and execute the nested event
list. Allocator microvectors rebuild private allocator state by replaying sizes.

