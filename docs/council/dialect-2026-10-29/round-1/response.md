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

