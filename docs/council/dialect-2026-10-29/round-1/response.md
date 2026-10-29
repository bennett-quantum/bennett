# Round-1 response — dialect 0.2 → 0.2.1

The JSON reports are the issue source. Each entry records the pre-edit derivation, decision,
section and witness. No north-star capability is narrowed. ISA remains 0.8; spec/README.md
requires a semantic version bump, so the full dialect version is 0.2.1 (descriptor ABI stays 2).
Independent execution and checker limitations are reported separately below; text state/TDL
vectors are normative expected results, not claims of a completed executor run.

## D02-11 — resolved

Before edit: A mutable initializer is reachable before any store. The [1 x ptr] GEP has stride 8, so index 1 reaches the second element of the actual two-entry allocation.

Edited §5.2 PT2/PT6: Seed all global initializers and use sound allocation/index bounds, never syntactic array dimensions. Witness: `normalisation-boundaries`.

## D02-12 — resolved

Before edit: Eight i1 lanes occupy one byte; lane 7 is (0x80 >> 7)&1 = 1, not byte p+7.

Edited §12.6: Packed vector loads/stores preserve bit layout, including masked inactive bits. Witness: `normalisation-boundaries`.

## D02-13 — resolved

Before edit: i129 has widths [64,64,1]. A carry into the last limb is already i1, and its sign bit is 0.

Edited §12.7: Every operation uses w_k; sign extension widens the partial top limb and fills new limbs. Witness: `normalisation-boundaries`.

## BD2-5 — resolved

Before edit: Unordered is bit 3; equal is bit 0, making ueq 9 and une 14.

Edited §13.1/§13.6: Corrected LLVM predicate numbers; NaN une is true. Witness: `n-fcmp and fcmp-abi`.

## D02-14 — resolved

Before edit: Same derivation as BD2-5; uno(1,2) is false while ueq(1,1) is true.

Edited §13.1/§13.6: Use LLVM enum values 8 through 14 in the correct order. Witness: `n-fcmp and fcmp-abi`.

## D02-16 — resolved

Before edit: A noreturn call permits LLVM to erase its continuation; a flag-and-return replacement cannot retain it.

Edited §14.4, N28–N30 residual obligation: Remove noreturn/tail constraints on returning transfers and use dedicated Bennett runtime symbols. Witness: `normalisation-boundaries; existing n-eh caught result 7`.

## D02-17 — resolved

Before edit: Nonmoving p=b+8 remains p, but its base is b and offset is 8.

Edited §12.8 N27: Run LLVM base-pointer analysis before statepoint erasure, carrying explicit provenance where necessary. Witness: `normalisation-boundaries`.

## BD2-6 — resolved

Before edit: ceil(24/16)*16=32. Choosing the rounded-size rule preserves the ratified aligned frame layout.

Edited §14.3 n-varargs, §17.3: Corrected the example to push 32 bytes and stated frame alignment/end. Witness: `normalisation-boundaries; corrected normalise-out=n-varargs`.

## BD2-1 — resolved

Before edit: Popping f hides its writes; use must see 9 between masks 0 xor 9.

Edited §10 TDL-2, §18.3: Retain f recorder visibility through use and adjoint. Witness: `compute-view`.

## BD2-2 — resolved

Before edit: Clearing byte 1 while K remains Co makes a later load return 0.

Edited §10 TDL-2/TDL-11: Retain basis bytes in arena until full object observation. Choose fable’s per-object alternative; invalidate observation coverage on writes. Witness: `partial-observe`.

## D02-02 — resolved

Before edit: Same two-byte derivation as BD2-2.

Edited §10 TDL-2/TDL-11: Use its explicitly permitted alternative: authoritative arena remains intact for partial observe. Witness: `partial-observe`.

## BD2-4 — resolved

Before edit: Unpredicated stores to local would leave 2 for every w.

Edited §10 MC4, TDL-3/TDL-5: Mark instructions including stores/calls; keep Co workspace stores and dependent reads together through the join. Witness: `branch-views`.

## D02-03 — resolved

Before edit: Both masks need old=0, giving 5 under w and 7 under not-w.

Edited §10 TDL-3: Fork branch views and merge only at the join. Witness: `branch-views`.

## D02-04 — resolved

Before edit: Zero payload is not a no-op for exchange or negative predicates.

Edited §10 TDL-8/TDL-10, §18.8: Require producing slice codes zero on every dependent effect; failed conditions select neither arm. Witness: `fault-consumers`.

## D02-05 — resolved

Before edit: Visible images [0,0] are not injective; measuring a retained condition creates a channel.

Edited §10 TDL-5(b)/TDL-7, A11: Check whole predicated updates for bijectivity and clean non-fault workspace, restoring E3. Witness: `clean-predicate`.

## D02-06 — resolved

Before edit: Measuring the copied record dephases q, whereas quncopy undoes that channel.

Edited §10 §7.5(a): Retain intentional measurement records to the permitted CC boundary, separate from workspace. Witness: `deferred-channel`.

## D02-07 — resolved

Before edit: Controlled append is invertible on declared virtual console state without external output.

Edited §10 TDL-12, §11.1, §18.8, A10: Inherit per-run device bindings and apply reversible transitions with explicit model undo state; code 8 only for unbound/unmodelled operations or genuine host calls. Witness: `updated tdl-effect`.

## D02-08 — resolved

Before edit: A classical self-loop contains no budgeted slice and could hang G.

Edited §10 TDL-9, §18.4: Bound G before each counted instruction; enforce heap/depth before mutation; exhaustion emits a controlled fault then stops. Witness: `generation-budget`.

## B1 — resolved

Before edit: 3 xor 5=6, so shadow xor 6=5 with arena zero; later controlled add gives 8.

Edited §10 TDL-2/TDL-5, §18.2: Specify Cl/M/Co routing for each arena event form, materialising controlled or Co-valued writes. Witness: `classical-event-application`.

## BD2-3 — resolved

Before edit: A G data symbol inside coh overlaps an interface range and would read a classical image. ISA also scopes @coh to the wrapper, so L1 needs its base threaded.

Edited §16.2–§16.4, §16.11: Exclude relocated globals from layout.globals/data, reserve coh at A_coh, thread its hidden base into lprocs, and address globals by arena offsets. Witness: `arena-o1: check/hash pass, inputs coh=0000/0500 produce 1/6 in 10 rows`.

## D02-01 — resolved

Before edit: Different offset/load rows let one projection succeed while another exhausts the same B.

Edited §8.6, §16.2 delivery: Every wide variant computes/validates every projection with identical rows; only final retval selection differs. Single-slice rows stay unchanged. Witness: `wide-delivery`.

## D02-09 — resolved

Before edit: Source alloca objects precede N24, so a heap-only source read-set misses their later backing bytes.

Edited §8.5: Translate source objects to normalized backing allocations and snapshot live stack storage and metadata; uncertain reachability copies all live backing allocations. Witness: `entry-backing and entry-stack`.

## D02-10 — resolved

Before edit: 17 bytes need 136 wires, exceeding the 128-wire ISA measure limit.

Edited §8.5 release, TDL-11, A2: Unprepare snapshots in 128-bit views with original xor128 args and clean-free the whole register; observe copies/measures chunks of at most 16 bytes. Witness: `entry-backing and partial-observe`.

## D02-15 — resolved

Before edit: Retained FP bits have no integer row without carriers; binary64 fneg toggles bit 63. Aggregate results require explicit packing.

Edited §16.1/§16.4, §16.11: Use §13.1 carriers for all FP forms and constants; specify bit operations, field packing and call-result unpacking. Witness: `fp-sign-carrier; checked fp-aggregate`.

## B2 — resolved

Before edit: {1,-1} packed low-field-first is 1|(0xffffffff<<8)=0xffffffff01, independent of memory padding.

Edited §8.1/§8.2, §16.1/§16.4, §16.11: Flatten scalar carrier fields, bind FP through IN/ARG, count flattened nparam, and pack/unpack aggregate results. Witness: `fp-aggregate: check/hash/run pass, payload 1099511627521; clang18/23 native match`.

## B3 — resolved

Before edit: Replaying the 16-byte stack block already advances bump from 4096 to 4112; allocating it again would move malloc to 4128.

Edited §8.5, §17.3, §16.11: ss_init adopts replayed base/size/sp and allocates nothing; snapshot includes stack block and state globals. Witness: `entry-stack: checked one-entry replay microvector, run payload 4112 in 42 rows; clang18/23 contract seed matches. General replay-loop canonical map is not claimed by this microvector.`.

## B4 — resolved

Before edit: E14 and §7.2 reject only a unique invalid candidate; two measuring candidates are distinct trap bodies.

Edited §22.1, §7.7: Corrected diagnostic parenthetical to unique-only, retaining the wider capability. Witness: `region-two-measure-candidates accept, dispatched trap code 4`.

## D02-18 — resolved

Before edit: A sampled maximum 10 can miss an identity input taking 1000 steps, so it is not a universal bound.

Edited §8.7: B_sample is a lower bound; sampled pairs assume universal inverse/totality and a sound B_bound across all input/parameter values. Witness: `inplace-bound`.

## D02-19 — resolved

Before edit: After g and swap, x=g(old,y) and t=old; XOR ginv(x,y) clears t for every y, hence by linearity for superposed y.

Edited §8.7/§8.8, §22.2, §25.1/§25.3: CC-level call/swap/inverse with preserved bindings implements ISA 0.8; retire BLK-3 and move parameterised qinplace to efficiency. Witness: `inplace-param-quantum accept; state for basis and superposed y`.

## D02-20 — resolved

Before edit: With zero steps, a console effect before the next entry/latch mark could execute without a charge.

Edited §12.2 N34, §17.6: Charge before each counted materialised instruction, including final suffix/return; batching must preserve the exact effect prefix and fault boundary. Witness: `r-budget-prefix`.

## D02-21 — resolved

Before edit: R cannot hostcall and generic trap does not encode arbitrary C; code 2 cannot be guaranteed by the old construction.

Edited §11.5, §17.5–§17.6, §22.2, §25.1–§25.2: Promote ISA-7 to BLK-5 with exact R fault C semantics. Affected points are blocked:BD-B-ISA7; no typed-fault implementation is claimed until the dependency lands. Witness: `r-fault-code blocked and required code=2 state`.

## D02-22 — resolved

Before edit: Sv39 supervisor alias V of physical P must refer to the same byte; raw high-address loads would instead miss the RAM allocation.

Edited §20.6: Translate every guest access in enabled effective privilege contexts, including kernel accesses, while runtime helpers use physical backing. Record virtual code mappings for dispatch/trap resumption. Witness: `sv39-kernel-alias`.

## Final accounting and validation

“Resolved” above means the disputed normative rule has been changed with its stated
witness; it does not claim a green P-1/P-2 freeze gate or successful independent TDL
execution. No blocker is declined and no normative-text blocker remains partial.
The full checker requirement remains incomplete in the separately owned checker job.

| Blocker | Status |
|---|---|
| BD2-1 | resolved |
| BD2-2 | resolved |
| BD2-3 | resolved |
| BD2-4 | resolved |
| BD2-5 | resolved |
| BD2-6 | resolved |
| D02-01 | resolved |
| D02-02 | resolved |
| D02-03 | resolved |
| D02-04 | resolved |
| D02-05 | resolved |
| D02-06 | resolved |
| D02-07 | resolved |
| D02-08 | resolved |
| D02-09 | resolved |
| D02-10 | resolved |
| D02-11 | resolved |
| D02-12 | resolved |
| D02-13 | resolved |
| D02-14 | resolved |
| D02-15 | resolved |
| D02-16 | resolved |
| D02-17 | resolved |
| D02-18 | resolved |
| D02-19 | resolved |
| D02-20 | resolved |
| D02-21 | resolved |
| D02-22 | resolved |
| B1 | resolved |
| B2 | resolved |
| B3 | resolved |
| B4 | resolved |

Validation (headless; local TMPDIR, offline Rust build; no push):

- `cargo build --manifest-path ../bennett-isa-spec/reference-interpreter/Cargo.toml --offline`
  succeeded. All nine ISA objects pass `check` and their `run-oracle` lines; all five
  hash blocks reproduce. The three new objects were independently checked before insertion.
- Final selected executable gate, `python3 scripts/dialect_check.py --family
  parse,header,check,hash,run-oracle,xrefs`: **1702/1702 passed**. This includes 393 LLVM
  verification cells across majors 18/20/23, header agreement, 9 object checks, 5 hash
  blocks, 9 run blocks and 1285 reference checks. Existing six map and six prefix-reversal
  families passed in the full run.
- Full `python3 scripts/dialect_check.py --json .tmp/council-final.json`: exit 1,
  **1939/2029 passed; 90 failed/blocked** (baseline **1922/1982; 60 failed/blocked**).
  Outstanding: 35 coverage obligations; 29 state and 9 TDL executor obligations; 8 CC/R
  executor/adapter failures; 2 recognition expectations, 1 new ISA-7 blocker expectation;
  2 normaliser failures (old 24-byte frame, missing n-fcmp); 3 missing native adapters;
  1 FP-aggregate map adapter. New examples remain obligations; none were removed or weakened.
- Direct `python3 scripts/dialect_check_v02.py`: exit 0, no output; this module has no
  main entry and is exercised by the frontend command above. Its empty run is not evidence
  of a green check.
- Independent clang 18 and 23 runs: packed i1 lane 7 and i129 add/sext vectors pass;
  n-fcmp input and output modules give NaN-une=1/equal-une=0, and corrected ABI
  ueq(1,1)=1/uno(1,2)=0 passes against a dedicated correct-enum contract seed.
  Existing checker-owned softfloat seed still has the old wrong enum and was not edited.
  Native aggregate packing yields 1099511627521; replay/adopting allocator contract
  yields pointer 4112 with stack pointer 4097. `entry-stack` is explicitly a one-entry
  runtime contract microvector, not an executed canonical general replay loop.
- `git diff --check` passes. No scripts code, ISA source, worklog or handoff file edited.
  The generated `.beads/issues.jsonl` and unrelated concurrent changes remain outside commits.

Checker requests are appended as Q4–Q8 in `scripts/CHECKER-QUESTIONS.md` and tracked as
`b-dialect-spec-ofu`. The two pre-existing spec/checker reading findings Q1 and Q2 were
also corrected (candidate text order and NS-reference punctuation) during the final read.

New ISA 0.8 dependency: **BLK-5/ISA-7**, Bead `b-dialect-spec-bz6`: add R `fault C`
that terminates with record code C, executes no subsequent source effect and preserves
reversible prefix history, plus the implicit trap-cause/code table. This resolves the
council's classification defect without pretending the ISA change is implemented. BLK-3
is retired because the parameterised in-place CC expansion exists on ISA 0.8. Existing
BLK-1, BLK-2 and BLK-4 remain as specified; no ISA repository edit was made.

Dialect commits by group: `25b52ea` (normalisation), `5186b42` (TDL), `bf9a5f3`
(interfaces/objects), `40a4962` (R/platform), followed by the final consistency/validation
commit containing this report's companion progress update. Response commits:
`a75a35d`, `202b65b`, `6dbbad9`, `aa73a5a`, followed by this final report commit.

## Post-round editor notes

### V10 / b-dialect-spec-7u1 — resolved (2026-10-29)

Both readings were re-derived before editing. Literal V10 accepts the old half
load/bitcast witness but rejects fneg half; it also excludes retained fabs/
copysign and extended-format call/return/aggregate transport. That narrows the
capability promised by NS §3.2 and already specified by §13.1, §13.3 and §16.
The other reading preserves those forms for all seven formats while still
requiring N32/N33 to rewrite arithmetic, comparison and conversion. Rule 10
selects it; no maintainer choice between two non-narrowing alternatives remains.

Deciding sentence: **V10 must permit every bit-exact operation retained by §13.1
and every carrier transport admitted by §16, for all seven floating-point formats.**

Hand derivation: fneg half transforms carrier b to b xor 0x8000; NaN payload and
quiet/signaling bits survive. This agrees with the
[LLVM 18 fneg semantics](https://releases.llvm.org/18.1.8/docs/LangRef.html#fneg-instruction)
and [LLVM 20 bit-operation semantics](https://releases.llvm.org/20.1.0/docs/LangRef.html#behavior-of-floating-point-nan-values).
Residual fadd half, by contrast, must become __bennett_sf_add_f16 on i16 carriers.

Surgical change: V10 now exempts all eight §13.1 retained forms and §16 carrier
transport (parameters, call arguments/results, ret, insertvalue, extractvalue),
with calls still subject to V4/V9/V12. validator-v10-clean now contains fneg half;
validator-v10-residue contains fadd half instead, retaining its rejection verdict.
New indexed validator-v10-carriers covers retained fabs/copysign and defined-call/
return/aggregate transport. §13.1 and the lifting map themselves are unchanged.
Appendix B records resolution; no example or expected result was weakened to
match the checker. Full dialect and norm advance to 0.2.2 under spec/README.md
and §23; map stays 0.2.1, ISA stays 0.8, and objects/hashes are unchanged.

Validation: all 190 tagged LLVM blocks verify on 18/20/23 (570/570); three V10
verdicts agree with the checker; supplemental seven-format retained/transport
versus fadd probes pass and verify on all three majors (42/42); LLVM folds ten
half sign-bit vectors per major including NaNs (30/30); current 0.2 xrefs pass
1310/1310. The legacy 0.1 xref helper's seven errors reproduce on e74d70c.

Only the three assigned documents were edited. The full preflight writes under
checker-owned scripts/.tmp and may build scripts/.isa-ref, so this editor used
read-only imports and LLVM stdin/stdout checks instead. **b-dialect-spec-bvy**
records the owner follow-up to synchronize SPEC_VERSIONS.toml and checker version
handling to 0.2.2, then run the full gate. No full-green claim or push; the council
should review this capability-preserving correction next round.

Spec/progress commit: `976e4bb83feafe3d6fcb2b9ef25118a2aeb350de`.
