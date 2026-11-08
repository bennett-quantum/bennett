# Editor response — estimate-e9a council round 1

Commit `0038d37b15e1d8ab9f5ae5dd953cbc243733c1f4`, branch `job/est-e9a-def`, continuing `ea01cf1`. Line references below name `docs/design/2026-11-08-recompute-cleanup-admissibility.md` at this commit. Edits are surgical: accepted sections remain in place; all five quotation blocks, obligations 1–2, the six historical verdict rows and their numeric resource totals are unchanged. The interpreter and production code are unchanged.

## Core blockers

- **Sol SOL-1:** lines 178–187 compare the composition of retained operations in candidate order and the literal K80 replacement with the original full-domain joint effect, including relative/global phase under control, external references and clean/restored releases. Occurrence, ownership, window, replay and version requirements remain independently mandatory.
- **Astra CODEX-S0-1:** the same edit removes the extra intermediate-effect restriction. Line 189 treats per-row commutation/effect checks as sufficient proof methods where applicable, rather than necessary admission conditions. The yak single-read refusal remains; line 279 now states that its read does not cancel elsewhere in the composition.
- **Muse B1:** obligation 3 cites §6.1 composed-M dependence and the realised-unitary requirement against §5.3's reference unitary at introduction. The seventh witness is **ADMIT** (line 258, explained at lines 312–327). Sol SOL-1 and Muse B1 are identical including row order, so one fixture pair covers both. The same independent oracle exhausts all eight bases in both directions with clean releases; its interpreter is unchanged. Fixture notes hand-derive identity, cleanup, inverse traversal, resource totals 9/5/41 and ownership entry:3,6,7. A fifth explicitly ignored future test requires actual recompute admission, resources and emitted semantics.

## Suggestions and nits

Every listed S1/nit was accepted as a one-line edit or within the blocker fix; none was declined.

- **Sol phase S1:** lines 183–184 explicitly include relative and global phase under control. §5 retains the phase-free X/CX evidence limitation.
- **Astra target/occupancy S1; Muse C4:** line 248 names the gate-pinned ideal-all-to-all assumptions; unchanged totals now have sums at lines 270, 293, 310: 3*4+5*5=37, 4*3+5*4=32, 5*4+5*5=45.
- **Muse S1-1 derivation:** lines 178–180 cite composed-M dependence and realised/reference unitary equality.
- **Muse S1-2 read/window cross-reference:** line 205 preserves all obligation-2 closing events, explicitly including §6.2 clause 3's non-permutation action call touching S even when read-only and basis-preserving.
- **Muse S1-3 terminal scope; C5:** line 133 distinguishes non-terminal adjoint/oracle carriers and independent-call-pair pre-call-history replay/target restoration.
- **Muse S1-4 rstrip:** line 360 accurately describes stripping trailing whitespace with rstrip(); mechanics remain unchanged.
- **Muse excerpt nit; C2:** line 62 marks §1.3 as a partial paragraph without changing the quote.
- **Muse endpoint nit:** line 211 identifies the designated endpoint writes as excluded from intervening operations.
- **Muse C1:** line 141 explicitly identifies CX controls as unchanged reads and cites §6.1's target/controls distinction.
- **Muse C8:** line 189 names the composed equality and §6.1's incomplete dependency-set non-dependence proof method; failure of that sufficient test is not an admission refusal rule.

## Muse B2 — upstream spec gap

Line 200 explicitly identifies the overlap between §6.2 clauses 1 and 4. Pending owner clarification, this note reads clause 1 as non-diagonal, non-permutation, following §6.1's separate provenance rows; clause 4 governs permutation changes to S. The upstream contract and quotations are unchanged.

Proposed **b-isa-spec** bead text (also in `.tmp/est-e9a-fix1/PROGRESS.md` for the orchestrator to file):

> Clarify ISA 0.9 §6.2 window clause 1 versus clause 4. Clause 1's non-diagonal-gate wording literally includes permutation X and closes tdf/w2b windows before their matched undo, conflicting with clause 4's undone-permutation allowance. Align clause 1 with §6.1's separate provenance rows: non-diagonal, non-permutation gate on S or g; permutation changes to S remain governed by clause 4. Add adjacent X/undo and CX-read-between-X/undo conformance witnesses. Evidence: council round-1 Muse B2 and the admitted restored-input/restored-input-read fixtures.

No bead was created or closed by this child; bennett-estimate-e9a remains open for the orchestrator.

## Verification

Headless, assigned worktree, job-local TMPDIR/CARGO_TARGET_DIR. CARGO_BUILD_JOBS=19 was derived from current host resources with reserved headroom. The inherited measured short-command guard records wall/CPU and reports trips as UNKNOWN/124.

- `python3 -I -B .tmp/est-e9a-fix1/verify-note.py`: **"Pinned digest and five verbatim excerpts: PASS"**.
- `python3 -B .tmp/est-e9a-fix1/run-focused.py cargo test --offline --locked --test recompute_witness -- --test-threads=1`: **"7 passed; 0 failed; 5 ignored; 0 measured; 0 filtered out"**; wall 3.144 s, CPU 3.293 s. Across seven fixtures, 192 exact literal executions cover 48 bases in both directions; 96 emitted reverse traces are checked against fresh sources.
- Red-first: the new named live test initially failed compilation because its two literal fixture files were absent, then passed after adding them without modifying the interpreter.
- Separate focused command with `-- --ignored --test-threads=1`: **0 passed; 5 failed; 7 filtered out**, expected on existing generic pending mechanics; wall 2.135 s, CPU 2.095 s. The future tests do not accept pending implementation as conformance.
- `python3 -B .tmp/est-e9a-fix1/run-focused.py cargo clippy --offline --locked --test recompute_witness -- -D warnings`: PASS; wall 0.315 s, CPU 0.262 s.
- `cargo fmt --check`, `git diff --check`: PASS. Mechanical comparison against ea01cf1 confirms byte-identical obligations 1–2 and historical six verdict rows.

No full repository or sibling gate was run.
