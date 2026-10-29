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

