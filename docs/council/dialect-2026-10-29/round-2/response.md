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

