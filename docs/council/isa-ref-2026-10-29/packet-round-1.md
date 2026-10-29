# bennett-isa-ref: the Rust reference interpreter of ISA 0.8 (snapshot for council review)

Snapshot of `reference-interpreter/` at commit `3dea965`. 55 files; each embedded verbatim below. Line counts and sha256 per file:

- `README.md` 96 lines, sha256 68cf15a43793
- `PROGRESS.md` 312 lines, sha256 fbb92d0c1b40
- `SPEC-QUESTIONS.md` 44 lines, sha256 0cff2147b132
- `BRIEF.md` 60 lines, sha256 702994e9abe7
- `Cargo.toml` 7 lines, sha256 62f73d0d28a5
- `src/lib.rs` 43 lines, sha256 fa10fc2201bf
- `src/action.rs` 818 lines, sha256 7d075533a395
- `src/borrow.rs` 61 lines, sha256 52dfca0b903e
- `src/call_discipline.rs` 227 lines, sha256 4dac20a5d6b5
- `src/classical.rs` 1121 lines, sha256 f29bf45126c0
- `src/handle_validation.rs` 99 lines, sha256 6b1e868a7572
- `src/identity.rs` 393 lines, sha256 f0b5d52737b7
- `src/json.rs` 384 lines, sha256 061cc3840607
- `src/linking.rs` 254 lines, sha256 3e6fcd6c6dee
- `src/machine.rs` 911 lines, sha256 47d0e7525c6e
- `src/main.rs` 275 lines, sha256 8e9ccc0cf4ae
- `src/object.rs` 1509 lines, sha256 33dc7b83c648
- `src/oracle.rs` 733 lines, sha256 4fa706240613
- `src/quantum.rs` 587 lines, sha256 122271f82ba1
- `src/registers.rs` 245 lines, sha256 b2ff21f8b1ea
- `src/sha256.rs` 89 lines, sha256 b46088d112ae
- `src/validation.rs` 1258 lines, sha256 801672169c98
- `tests/borrow.rs` 51 lines, sha256 cd402bd6bdd6
- `tests/classical.rs` 84 lines, sha256 3d2192b944bc
- `tests/cli.rs` 73 lines, sha256 4b002a5f6925
- `tests/discipline.rs` 96 lines, sha256 8a31ac17af62
- `tests/fixtures/actions.bisa` 39 lines, sha256 1b4250b0ee08
- `tests/fixtures/actions.comments` 2 lines, sha256 8fa05ce7cd7d
- `tests/fixtures/arithmetic.bisa` 194 lines, sha256 d11afe460bf7
- `tests/fixtures/arithmetic.comments` 1 lines, sha256 c29824e62bdf
- `tests/fixtures/classical.bisa` 105 lines, sha256 b8d9aab471f0
- `tests/fixtures/classical.comments` 2 lines, sha256 0d7e708118ff
- `tests/fixtures/heap.bisa` 73 lines, sha256 253a11b5bbe9
- `tests/fixtures/heap.comments` 1 lines, sha256 cad175f056b5
- `tests/fixtures/inc8.bisa` 12 lines, sha256 8093da48bad0
- `tests/fixtures/inc8.comments` 1 lines, sha256 dcae0475f284
- `tests/fixtures/mutual.bisa` 29 lines, sha256 ba0df453b2ad
- `tests/fixtures/mutual.comments` 1 lines, sha256 a64d54b45432
- `tests/fixtures/nested.bisa` 31 lines, sha256 8e6e852c4717
- `tests/fixtures/nested.comments` 1 lines, sha256 4d816294e8c6
- `tests/fixtures/registers.bisa` 50 lines, sha256 e27e84523d69
- `tests/fixtures/registers.comments` 1 lines, sha256 37c01188225a
- `tests/fixtures/sum_db.bisa` 39 lines, sha256 ce1a10eb0077
- `tests/fixtures/sum_db.comments` 1 lines, sha256 d8463c5d07f5
- `tests/fixtures/tiny_memory.bisa` 20 lines, sha256 6482f75d5409
- `tests/fixtures/tiny_memory.comments` 1 lines, sha256 1d8bf1b1ce4f
- `tests/identity.rs` 185 lines, sha256 23a37d917967
- `tests/linking.rs` 117 lines, sha256 8edbb0d5733a
- `tests/oracle.rs` 237 lines, sha256 562dbc9afd6f
- `tests/parser.rs` 126 lines, sha256 6a4ab37e2ed3
- `tests/quantum.rs` 131 lines, sha256 e2f29a770c33
- `tests/registers.rs` 122 lines, sha256 7111bef01079
- `tests/step_machine.rs` 134 lines, sha256 3c6f20dd1dce
- `tests/structured.rs` 77 lines, sha256 b79a5f348022
- `tests/support/mod.rs` 55 lines, sha256 a4cadf6cfcf4

Total embedded: 11618 lines.

## `README.md` (96 lines)

````markdown
# Bennett ISA reference interpreter

Rust 2021, standard library only, ISA 0.8. The implementation is in progress;
[PROGRESS.md](PROGRESS.md) records verified work and remaining obligations.
It is not yet a complete conformance reference. In particular
certificate composition, borrow proofs and comprehensive static validation
are unfinished. The numerical simulator uses `f64`; it does
not implement the rigorous certificate checker of §12.

Build and test offline from the repository root:

```sh
cargo build --manifest-path reference-interpreter/Cargo.toml --offline
cargo test --manifest-path reference-interpreter/Cargo.toml --offline
cargo test --manifest-path reference-interpreter/Cargo.toml --offline -- --ignored
```

The executable is `reference-interpreter/target/debug/bennett-isa-ref`.
All successful commands write one JSON object to stdout. Diagnostics go to
stderr with exit status 1; success returns 0. ISA diagnostics cite their rule.
Integers above the exact JSON integer range are decimal strings (§9.1).

## Commands

`check <object>` parses and validates the object, computes identities, and
verifies every stored interface hash. Output contains `status`, `object_hash`
and `symbols`, indexed by symbol name with `interface_hash` and `closure_hash`.
An unresolved dependency has a null closure hash.

`hash <object>` produces the same identities without comparing stored hashes.
This helps construct fixtures; it does not edit files or certify their hashes.

`run-oracle <object> <oracle> --input <x[,y...]> [options]` executes the §14.1
sequential interpreter. Output is `{"code":0,"payload":9,"steps":3}` for
inc8(8) at B=3. `--input ""` supplies an empty input list. Values may be
unsigned decimal or `0x` hexadecimal. The oracle name may start with `@`.

Options:

- `--budget B` changes the step limit; `--budget B,heap,stack,depth` sets all
  four limits. Default B is 1,000,000. Layout limits supply heap and stack
  defaults; depth defaults to 64 with a layout. Memoryless limits are zero.
- `--mem name=hex` supplies an interface region's bytes, in cell order.
  Unspecified regions start at zero. Each supplied region must have the exact
  declared byte count. Repeat for multiple regions.
- `--arg value` supplies the next classical argument. Unsigned integers are
  decimal/hex; `f64:0.5` supplies an angle; `token:B,heap,stack,depth` supplies
  a nested-oracle budget. Repeat in signature order. Specify `--budget` before
  abbreviated tokens to use its limits as their defaults.

`step-check <object> <oracle> --exhaustive [options]` compares the independent
sequential and reversible interpreters, then reverses all B steps and compares
every internal register, memory cell, stack cell, allocator entry and frame
against the entry tuple. It enumerates input bundles and all unspecified
interface-memory bytes. Target/fault entry values do not affect computation:
delivery XORs a fixed payload/code into them. Output reports `cases`,
`input_and_memory_bits`, `fixed_regions`, `status` and that delivery property.
Fixed regions restrict the tested domain and are explicitly listed.

The same `--budget`, `--mem` and `--arg` options apply. Default B is 256.
`--max-bits N` changes the exhaustive enumeration cap from 16 to at most 24.
Larger domains fail explicitly; the command never silently samples. Classical
arguments are fixed parameters of the check.

Examples from the repository root:

```sh
reference-interpreter/target/debug/bennett-isa-ref check reference-interpreter/tests/fixtures/inc8.bisa
reference-interpreter/target/debug/bennett-isa-ref run-oracle reference-interpreter/tests/fixtures/inc8.bisa inc8 --input 8 --budget 3
reference-interpreter/target/debug/bennett-isa-ref step-check reference-interpreter/tests/fixtures/inc8.bisa inc8 --exhaustive --budget 4
reference-interpreter/target/debug/bennett-isa-ref run-oracle reference-interpreter/tests/fixtures/sum_db.bisa sum_db --input 3 --mem db=0102030405060708090a0b0c0d0e0f10 --budget 1000,4080,512,64
```

## Library and fixtures

`Object::parse`, `identity`, `check_hashes`, `run_oracle` and `OracleMachine`
provide the corresponding library operations. `ClassicalMachine` exposes
dynamic SSA execution and retained-history reversal. A hostcall suspends `run`
with a `HostRequest`; `reply` supplies bytes, and another `run` resumes it.
The request/reply transcript is retained for reversal. `QuantumState` supports
basis permutations, small state vectors, gates, clean release and enumerated
Born measurement branches. `execute_action` executes structured Q bodies and
their adjoints. State vectors are limited to 24 live wires; basis permutations
can use larger wire stores. Numerical cleanliness uses tolerance 1e-12.

`Object::link` resolves imported declarations and pinned closures, rejects
conflicting definitions/layout/device/data entries, deduplicates definitions,
and regenerates canonical linked identities. `QuantumRegisters` implements
live/viewed/consumed handles and clean preparation. Pass it to
`ClassicalMachine::with_quantum_registers` for qreg entry arguments. Measurement
uses a reproducible xoshiro256** stream; `push_measurement_draw` supplies a
specific uniform draw for differential tests. Measured traces cannot reverse.

Canonical `.bisa` fixtures have adjacent `.comments` files with hand-derived
expected outcomes; comments are not an extension to the §16 grammar.
[SPEC-QUESTIONS.md](SPEC-QUESTIONS.md) records specification readings.
````

## `PROGRESS.md` (312 lines)

````markdown
# Bennett ISA reference interpreter progress

Resume from this file. Scope remains the entire accepted ISA 0.8. No git commands;
write only under reference-interpreter/. The user limits take precedence over the
repository-wide worklog rule, so this file also serves as this job's worklog.

## Session 2026-10-29

### Continuation: imports and linking (current)

Tracking: Beads issue b-isa-spec-zq2, already in_progress. Read beads skill and
ran bd prime. Claim was rejected because the existing job issue is already in
progress; updated its notes with the status guard instead of changing ownership.
The new AGENTS instruction authorizes Beads tracking metadata; implementation
edits remain confined to reference-interpreter/. No git or remote sync ran.

Red: `cargo test --manifest-path reference-interpreter/Cargo.toml --offline
--test linking` failed because Object::link did not exist. Implemented imported
declaration schemas, import fingerprint validation, explicit unresolved-call
execution errors, resolution by signature, pins, equal-definition dedup,
data/layout/device conflicts and regenerated canonical linked symbol hashes.
Green: four linking tests pass; full cargo test passes 41 normal tests with no
warnings (two ignored sweeps unchanged). Hand count: call + const + add + ret +
retval = 5; input 255 produces zero through 8-bit wrap, now tested after linking.

Files: src/linking.rs; Function::from_signature and Object::declaration;
tests/linking.rs plus tests/support/mod.rs. Remaining linking limitation:
different schedule/certificate metadata is still treated as conflicting;
certificate composition and stronger metadata validation are unfinished.
Next active work remains deliverable 1: inherited-control and nested-uncall
validation, then Q handle integration and remaining formal verification.

### Continuation: CC quantum handles and region history

Red: `cargo test --manifest-path reference-interpreter/Cargo.toml --offline
--test registers` failed on missing QuantumRegisters and measurement APIs.
Implemented live/viewed/consumed handles, slices and concat, clean preparation
and free, quantum action/oracle history frames, Born branch selection, and
measurement reversal/uncall exclusions. Handle reversal stores affected handle
records and released-wire positions; region reversal applies the actual inverse
operation once, not a saved quantum state. Trial execution only makes a failing
region invocation atomic; trial states are not retained as inverse history.

Red view-lifetime test initially accepted use of a viewed parent. Added CFG
validation of view-only-one-region-call and parent restrictions. Green: all 5
register tests pass. Full cargo test passes 46 normal tests; strict Clippy with
--all-targets -- -D warnings passes. New registers.bisa fixture has expected
results in registers.comments and validated identities.

Hand checks: for inc8(7), existing target 31 becomes 31 XOR 8 = 23, existing
fault 3 stays 3; at B=2 target stays 31 and fault becomes 3 XOR 1 = 2. Both calls
reverse to their complete entry tuples. Bell draws below/above 1/2 select 00/11.
Numerical Q state comparisons use 1e-12; reversible basis tests remain exact.
Beads issue b-isa-spec-zq2 remains in_progress; no deliverable is claimed done.

Read CLAUDE.md, HANDOFF.md, spec/README.md, the complete 1,675-line specification,
the complete Python seed, the workspace handoff, and the budget design note.
Rust 1.99.1 / Cargo 1.99.1 are available. No dependencies are permitted.
The existing crate contains only a version function and a skeleton test.

| Deliverable | Status | Verification |
| --- | --- | --- |
| 1. Canonical parser and well-formedness | Partial: lexical/structural parser, types, lifted row schemas/scope, signatures, layout validation | 4 integration tests green |
| 2. SHA-256, envelopes, SCC identity | Core implemented, including mutual SCCs and CC/R closures; imports/linking still incomplete | 7 identity tests green |
| 3. Sequential reference interpreter, every lifted row | Every row has an implementation, including lift.perm_call; broader adversarial verification and unbounded bundle widths remain | 5 oracle tests plus Q lifted-call test green; full division sweep passed |
| 4. Literal reversible step machine and exhaustive comparisons | Slot/exchange machine, C1–C5/R1–R5 and inverses, all rows implemented; full obligations not yet met | 4 normal tests and ignored recursive sweep passed |
| 5. CC/R interpreter, tapes, history, uncall | Classical rows, dynamic SSA, memory, four device models, tapes, host request/reply, segment/whole reversal; qreg/Q integration pending | 4 classical tests green |
| 6. Q simulator and static cleanup discipline | Basis/vector simulation and instruction paths implemented; borrow proofs and complete §6 checker remain | 5 Q tests green |
| 7. CLI and documentation | Required commands plus hash implemented/documented; check depends on incomplete validator | 2 CLI tests green |

### Milestone: canonical core and identity

Red: `cargo test --manifest-path reference-interpreter/Cargo.toml --offline`
failed with unresolved `json`/`Object` APIs before implementation.
Red: the same command with `--test identity` failed with missing SHA-256 and
identity APIs before implementation. Green: the complete command now passes all
8 integration tests in approximately 0.2 seconds, no compiler warnings.

Hand checks: inc8's envelope consists of 3 prefix lines and the 6 canonical
function lines, each LF-terminated; its resulting hash matches the printed
8ce5e64f… value. sum's recursive self-reference is @$0, so the test independently
derives SHA256(SHA256(envelope)-hex + ':0'). R_sum = 3 + (3+1+9) = 16 cells.

Files: src/json.rs, object.rs, identity.rs, sha256.rs; tests/parser.rs,
identity.rs; tests/fixtures/{inc8,sum_db}.bisa with adjacent .comments files.

### Milestone: broader validation and sequential oracle engine

Red: `cargo test --manifest-path reference-interpreter/Cargo.toml --offline
--test structured` ran 4 tests and failed all 4 against accepted malformed
actions/metadata. Implemented action/classical operand validation, predicates,
loop bounds, input-role checks, initial cleanup-window tracking, region-call
schemas, acyclic region graphs and metadata field validation. All 4 now pass.
This is still partial suite-F coverage: borrow proofs, full provenance/window
analysis, handle lifetimes, linking and deep certificate/schedule schemas need
more work. The initial no-op validation hooks have been replaced.

Red: `cargo test --manifest-path reference-interpreter/Cargo.toml --offline
--test oracle` failed before the execution APIs existed. Implemented independent
dynamic activation environments, monotonic stack accounting, allocator and
little-endian memory, all binops/divisions/comparisons/casts, simultaneous
parmov, label/range control, faults and nested oracle call/uncall. These are in
src/oracle.rs. lift.perm_call explicitly errors pending the Q engine.

Green: full cargo test passed 16 tests before nested-call additions;
`--test oracle nested_oracles` also passes. Python seed's unchanged
`python3 reference-interpreter/isa_check.py` passes. New canonical arithmetic,
heap and nested fixtures have hand-derived adjacent comments and hashes
independently generated using the unchanged seed's envelope implementation.

Hand checks: recursive sum_db(3), db=1..16, yields 6 in 52 rows (4 oracle rows +
3*14 recursive rows + 6 base rows); stack demand 64 cells. Signed -7/2 truncates
to -3, encoded 253; remainder -1, encoded 255. Heap 0x1234 stores bytes 34 12.
Fixed a test input typo: jump's expected 9 requires y=9, not y=0.

Next: literal reversible step machine and its one-step call/ret inverse tests;
run the ignored 262,144-case u8 division sweep; broader suite F and identity
tests; CC/R and Q engines; CLI and docs. None of the deliverables is yet marked
complete. Known engine gap: closure order currently sorts individual member
hashes, so mutual-lproc SCC member ordering must be corrected before D3/D4 done.

### Milestone: reversible basis machine

Red: `cargo test --manifest-path reference-interpreter/Cargo.toml --offline
--test step_machine` failed because OracleMachine did not exist. Implemented
src/machine.rs with assignment, capture and delivery slots, flags, saved
successors, PC XOR/exchanges, monotonic stack records and literal ordered
call/ret inverses. Inverse execution does not restore saved state snapshots.
Snapshots exist only as an external assertion surface for tests.

Green: the same command passes 4 tests (one ignored), covering all inc8 inputs
and B=0..5, arithmetic/branch/parmov/fault prefixes, heap/table restoration,
and immediate forward/inverse checks on every row of recursive sum_db(2).
The complete mutable tuple, including all frames, is compared on every check.
All 11 literal fault codes are exercised; code 10 here is an explicit fault
row, not a claim that R entropy is implemented. Nested oracles are recursively
executed as reversible machines, independently of the sequential engine.

`cargo test --manifest-path reference-interpreter/Cargo.toml --offline --test
oracle -- --ignored` PASSED: 262,144 unsigned/signed division and remainder
cases, 2.07 seconds. Expected values use host i16 arithmetic rather than the
engine's sign extension implementation.

Hand check: inc8(8), B=4, has pc sequence 0,1,2,HALT,HALT; registers become
one=1,r=9 and result_val=9. The idle frame retains old_pc=HALT. Inverse PC
exchanges restore 2 before undoing retval, then restore r=0 and one=0; all
four old_pc fields and slots clear. The commit result 9 remains external.

Next: run ignored recursive-prefix sweep; correct mutual-SCC closure ordering;
add linking and matched-nested-call validation; implement Q/action engine and
lift.perm_call, CC/R engine, CLI/docs. Parser/schema/provenance checks still
need adversarial expansion before any deliverable can be called complete.

### Milestone: CC/R history and device models

Ignored recursive sweep PASSED: `cargo test --manifest-path
reference-interpreter/Cargo.toml --offline --test step_machine -- --ignored`,
all 8-bit n and every prefix through completion/first memory fault, 12.58 sec.

Red: `cargo test --manifest-path reference-interpreter/Cargo.toml --offline
--test classical` failed with missing execution APIs. Green: 3 tests now pass
for dynamic SSA loops, pure copies surviving uncall, nested cancelled segments,
memory/allocator reversal, all four device models including absent-block
presence restoration, terminal fault reversal and entropy atomicity.

src/classical.rs records per-instruction deltas and activation controls,
not complete memory snapshots. New classical.bisa fixture has hand-derived
comments. Its symbol hashes remain placeholders (the seed cannot hash CC/R
closures correctly); regenerate/check independently when the identity/link
milestone is finished. No test currently claims its placeholder hashes pass.

Hand check: nested f calls g (clock 0->1), uncalls g (clock 1->0), then returns;
uncall f skips g's reversed frames and marker, keeping clock 0. effects emits
five tape entries (entropy, console, clock, block write, block read), returns
the clock's initial zero, and reverses to an absent sector map and empty tape.

Next: Q basis/state-vector kernels and action execution, then CC hostcall and
qreg/measurement integration; complete suite F, SCC/linking, CLI/docs. All
seven statuses remain partial/pending until exhaustive obligations are met.

### Milestone: Q execution and CLI

Red: `cargo test --manifest-path reference-interpreter/Cargo.toml --offline
--test quantum` failed before QuantumState/execute_action existed. Implemented
src/quantum.rs and action.rs: complex amplitudes, allocation, controlled gates,
copy/XOR/exchange, quantum memory and local images, predicate stacks, qif,
bounded loops, coherent while flags, region calls/adjoints, qinplace expansion,
borrow-pool binding and measurement branches. Some paths lack required tests,
particularly borrow validity, qinplace certificates, nested controlled actions
and coherent while loops. Do not interpret implemented paths as verified.

Green: 5 Q tests pass for Bell/Born outcomes, every primitive gate/inverse,
controlled global phase, >64-wire permutation fast path, clean release,
action adjoints, copy/memory cleanup, loops, and lifted permutation calls.
The lifted-call test first failed on the explicit missing-engine error; both
sequential and reversible engines now execute it, with the adjoint on reversal.

Red: `cargo test --manifest-path reference-interpreter/Cargo.toml --offline
--test cli` failed before a binary existed. Green: check, hash, run-oracle and
step-check now have passing process tests and README documentation. Full
input/memory enumeration is capped (default 16 bits, configurable to 24) and
never silently sampled; fixed regions are reported. Target/fault entry values
are handled via their XOR-delivery law, not enumerated in this command.

Hand check: Bell from |00> has amplitudes 1/sqrt(2) at indices 0 and 3 and
Born probabilities 1/2 each. Controlled Rz(2*pi) contributes -1 on the enabled
branch; H-control interference therefore yields control=1, explicitly tested.

### Milestone: host requests, mutual SCCs, and fixture identities

Host request test first failed with missing request/reply APIs. It now passes:
request payload a5 00 00, reply 11 22 33 44 55, three-byte write 11 22 33,
rlen=5, and complete prefix reversal. Null request pointers fault before any
request. The transcript is retained. Reply-length overflow reading is question 8.

Mutual SCC test first returned label 2 instead of hand-derived 4. Fixed canonical
lproc order to keep SCC members in name/index order, with scc_hash group keys.
The test independently derives both member hashes from concatenated envelopes.
Both interpreters share Program's canonical layout; the hand-derived check is
therefore essential and independent of their agreement.

Unknown effects initially could execute fault 8 but could not hash. Regression
failed with missing model entry; fixed per §17 (question 6). Independently
assembled g's complete device/layout envelope in Python, checked SHA-256
e8a3dc5429049b16559aa6a4262779e3dcd37a758967def4e08c371a5b765fff against Rust.
Regenerated classical fixture hashes including new host procedures. A new test
checks hashes of all eight fixture objects; no placeholder hashes remain.

The empty-HEX regression first failed the global trailing-space rule. Resolved
the grammar contradiction as question 9, accepting NAME SP LF only inside data
for zero-byte images. Leading-zero type widths are now rejected.

## Resume here: outstanding work, in priority order

No user decision is required. Do not mark the job complete; no deliverable has
its full verification obligation met yet. The entire ISA remains the scope.

1. Finish suite F and identity/linking: imported callees currently fail operand
   validation; implement resolution by signature, pinned closures, dedup and
   conflicts. Deep schedule/certificate/coverage schemas and bindings, effective
   inherited control checks, exact matched oracle_uncall discipline, frame
   live ranges, handle lifetimes and borrow-frame proofs remain incomplete.
   The current simple symbolic cleanup checker can reject valid adjoint
   cleanup (e.g. H;H on allocated scratch) and is not the full §6 transfer.
   It tracks loops only once statically and does not fully model cell versions.
2. Type::parse currently limits wire/reg/region cell widths to 128 as well as
   iN; the spec only explicitly bounds iN. Generalize bundle handling and
   audit wider locations before declaring full-width support. JSON/JCS shortest
   number corner cases and all integer spellings need expanded vectors.
3. CC quantum integration: qreg.new/free/slice/concat, measurement and region
   calls currently explicitly error in classical.rs. Implement handle states,
   exclusive views, retained-history inverses, Born outcome selection, segment
   prohibition on measure, whole-run reverse eligibility, and tests. Q kernels
   and action/oracle execution already exist and should be reused, with inverse
   region operations exactly once per history frame.
4. Complete Q verification: borrowed systems plus an entangled reference,
   translation-lemma positives and four required negatives, qinplace pair
   certificates/full domain, qif, while loops, inherited controls, nested region
   calls, local-image restoration and full cell-version cleanup obligations.
   permutation_action_values currently does not supply a borrowed idle pool;
   handle that according to the ABI once borrow validity is established.
5. Strengthen machine verification at genuinely small interface widths over
   complete D, including varied interface memory, nonzero target/fault values,
   explicit commit gates, call/ret special cases and every first-fault boundary.
   BasisConfiguration includes every internal mutable field; inverse code uses
   no snapshot restoration. Machine logical counters use u128 containers;
   audit their derived bit widths and generalized frame-slot sizing.
6. Audit the rest of §8–§13 referenced schemas and interpreter-facing contracts;
   do not assume the current shallow field checks implement target evaluation,
   schedules, certificate checking or linking. Keep scope aligned with the job.
7. Expand fixtures so every instruction/path (not just every opcode) and fault
   has a hand-derived expected result, run all ignored sweeps after substantive
   changes, complete README and only then mark deliverables done.

Current source files: lib.rs, json.rs, object.rs, validation.rs, sha256.rs,
identity.rs, oracle.rs (independent dynamic activations), machine.rs (literal
slots and inverse steps), classical.rs (delta history), quantum.rs, action.rs,
main.rs. Tests are integration tests in tests/*.rs. No dependencies were added.
No git commands were run; spec/ and isa_check.py were not edited.

### Latest regression and verification

Added a failing narrow-label test: an independent jump oracle has ten rows and
legally uses a 4-bit label location, despite many unrelated functions in the
same object. It previously failed width validation. Fixed validation to count
each reachable oracle/lproc closure (the largest applicable closure for a
shared lproc), rather than all object functions. The test now passes and
independently returns 42 on the zero branch.

Before this last regression: complete `cargo test` passed 36 normal tests, no
warnings; both ignored tests passed again (u8 divisions 2.08 sec, recursive
prefixes 8.78 sec). `cargo clippy --manifest-path
reference-interpreter/Cargo.toml --offline --all-targets -- -D warnings` and
`cargo fmt --manifest-path reference-interpreter/Cargo.toml -- --check` passed.
The unchanged Python seed passed. Final rerun results follow below.

Final rerun after the label fix: `cargo test --manifest-path
reference-interpreter/Cargo.toml --offline` PASSED, 37 normal integration tests,
2 deliberately ignored sweeps, no warnings. `cargo test --manifest-path
reference-interpreter/Cargo.toml --offline -- --ignored` PASSED both sweeps:
262,144 u8 division cases in 1.45 sec; all recursive n/prefix cases in 6.76 sec.
Clippy with `--offline --all-targets -- -D warnings` PASSED; fmt `-- --check`
PASSED; unchanged Python seed PASSED. Direct documented CLI invocation of
sum_db(3), db=1..16, B=1000/heap=4080/stack=512/depth=64 printed exactly
`{"code":0,"payload":6,"steps":52}`, matching the hand derivation.

This session is a verified intermediate implementation, not JOB-COMPLETE and
not blocked on a user decision. Continue from the outstanding-work list above.

Open specification readings are recorded in SPEC-QUESTIONS.md. No decision from
the maintainer is currently required. In particular the printed 0.8 HALT idle
step is authoritative; the design note's proposed done-invariance is not 0.8.
````

## `SPEC-QUESTIONS.md` (44 lines)

````markdown
# Implementation readings of ISA 0.8

These questions do not narrow the supported ISA. The accepted specification is
unchanged. Each entry records the applicable rule and the chosen reading.

1. **Indices: blocks or rows? (§3.6, §4.2, §16.3).** The index-space paragraph
   calls its elements blocks, but every instruction is a budget step with k+1
   fallthrough, calls record k+1, and the published inc8 takes three steps in
   one block. Use one index per instruction, concatenating blocks in text
   order; a label denotes its block's first instruction. A function's range
   contains all its instruction indices. Preserve these indices in lift.label.
2. **Fixture comments versus canonical text (§16.1–§16.2).** The job requests
   expected-result comments in fixtures; the interchange grammar has no comment
   syntax. Store hand-derived comments in adjacent .comments files. The .bisa
   files remain canonical objects, with no undocumented comment extension.
3. **Idle steps (§3.6, budget design note I5).** Implement the printed HALT
   successor XOR and two exchanges, including old_pc = HALT in an idle frame.
   Prefix reversal clears it. Do not silently implement the proposed 0.9 change.
4. **Counter widths (§3.7, §9.1).** The layout schema supplies size exponents
   but no Hc/Ac/Sc/Dc fields. Derive the minimum legal widths from §3.7 and the
   invocation's depth limit. The sequential interpreter uses unbounded logical
   counters; concrete machine counters use these derived widths.
5. **Reported step count on budget exhaustion (§14.1, Python seed).** Count
   executed rows, at most B. The seed increments to B+1 before refusing the
   next row; expose the normative executed-row count, and test the seed's
   outcomes independently of that off-by-one diagnostic.
6. **Unknown device identity (§9.2, §17 item 3).** An unmodelled effect has
   the specified fault outcome 8 and its operation token is in the canonical
   body. It contributes no device-envelope entry because no such model exists.
   A known device model or host service used without a declaration is an error.
7. **Ordering multi-member lproc SCCs (§3.6, §9.2).** Member closure hashes
   are unrelated SHA-256 values and cannot order members by SCC index. Sort
   multi-member SCC groups by their scc_hash, then their members by name/SCC
   index; a singleton uses its symbol closure hash. The mutual.bisa fixture
   deliberately has hash(f) > hash(g) and checks that g's label is still 4.
8. **Host reply length wider than ptr_width (§10).** rlen must report the full
   reply length, in an integer of ptr_width. Reject an unrepresentable reply
   with E_ARG before any memory write, allowing the host to provide a valid
   reply. Truncating rlen would defeat the specified truncation detection.
9. **Empty data images (§16.1 versus §16.2).** HEX explicitly admits the
   empty string and a zero-sized data signature is legal, but NAME SP HEX
   then ends with a space. Honor the explicit data grammar: accept exactly
   `NAME SP LF` for a zero-sized data image, as the sole trailing-space
   exception. All nonempty data and all other lines keep §16.1's space rule.
````

## `BRIEF.md` (60 lines)

````markdown
# Job: the Bennett ISA 0.8 reference interpreter in Rust

Working directory: the git repository `bennett-isa-spec`. Build the complete reference implementation
of the ISA specification `spec/Bennett-ISA-Spec.md` (draft 0.8, accepted) as the Rust crate in
`reference-interpreter/` (crate `bennett-isa-ref`, currently an empty skeleton). Read first: `CLAUDE.md`
(fail fast and loud, red-green TDD, exhaustive verification, skepticism), `HANDOFF.md`, `spec/README.md`,
then the whole specification, then `reference-interpreter/isa_check.py` (a Python seed that parses
§16, hashes §9.2 envelopes, and executes the lifted rows used by the two §16.3 examples).

## Scope is the whole ISA. Nothing may be left out.

This interpreter is the executable model every other Bennett tool will be checked against. A previous
document limited itself to what a partial model could execute, and that was rejected: the project's
target programs (for example an unmodified SQLite query evaluated as a lifted oracle) need every lifted
row, including memory, heap allocation, calls and procedures. So implement every instruction and row of
the specification. If the text is ambiguous or seems contradictory, do not drop the feature: choose the
reading most consistent with the rest of the specification, implement it, and record the question, the
reading and the section in `reference-interpreter/SPEC-QUESTIONS.md`. Never edit `spec/`.

## Deliverables, in priority order (each with tests written and seen failing before the code)

1. **Parser and well-formedness** for the §16 canonical textual form: every construct of §16.2 and of
   the sections it references; rejection of ill-formed objects with the rule cited (suite F, §15).
2. **Identity** (§9.2): envelopes, SCC hashing, symbol-reference replacement; SHA-256 implemented in the
   crate (standard FIPS 180-4 test vectors). Reproduce the four published hashes of §16.3 exactly.
3. **§14.1 reference interpreter** for oracle reference bodies, every §4.2 row: const, binop, div,
   icmp, select, cast, mov, parmov, label, addr, boundscheck, load, store, alloc, free, faultif, call,
   ret, retval, oracle_call, oracle_uncall, qjump, qbranch, qjumpr, fault; lprocs and their closure
   (§3.7); activation records, stack accounting, `alloctab`, globals and interface regions (§7.2);
   budgets B / heap / stack / depth and every fault code (§5.4). It defines F_B and the budget unit.
4. **The predicated step machine as a reversible machine on basis configurations** (§3.6, §3.7): the
   forward step and the inverse step exactly as printed (dispatch, slots, flag, succ, commit, delivery,
   the printed inverse lists of the A+D rows), executed on concrete bit-vectors. Check, exhaustively at
   small widths, that (a) the machine's result equals the §14.1 interpreter's F_B on every input, and (b)
   running B forward steps then B inverse steps restores every register, frame and memory cell (the
   prefix-reversal property, T2 of §14.3), for success and for every fault path.
5. **Classical-control and reversible tiers** (§3.4, §4.1, §7.1, §7.3, §7.4): instructions, memory and
   allocation table, effect and entropy tapes, the run history, `call`/`ret`/`uncall` segment rules.
6. **Q-tier semantics** (§4.3–§4.7, §5, §6, §14.2): allocation, gates, copy/XOR/exchange/in-place,
   quantum memory and predication, region calls, borrowed systems; a state-vector simulator for small
   widths and a basis-configuration (permutation) fast path; the §6 uncomputation-validity checks.
7. **A command-line tool** `bennett-isa-ref` with at least: `check <object>` (parse + well-formedness +
   hashes), `run-oracle <object> <oracle> --input <x> [--budget ...]` printing F_B and the step count as
   JSON, `step-check <object> <oracle> --exhaustive` (deliverable 4), so other repositories' tools can call
   it. Document every subcommand in `reference-interpreter/README.md`.

Test fixtures: write new §16 text objects under `reference-interpreter/tests/fixtures/` that exercise
every row and every fault code, each with a hand-derived expected result written in the fixture's
comments before running it. Port every check `isa_check.py` performs. Keep `cargo test` green and fast
(long exhaustive sweeps behind `--ignored`, run them anyway and record the result).

## Constraints

- Rust standard library only, no external crates (the network is unreliable and the build must work
  offline). Edition 2021. `cargo test` must pass with no warnings you introduced.
- Write only inside `reference-interpreter/`. Leave `isa_check.py` as it is.
- Progress goes in `reference-interpreter/PROGRESS.md` (see the job protocol below): per deliverable,
  status, the verifying command and its result.
- Correctness over speed of delivery: do not mark a deliverable done without its tests and an
  independent spot check of at least one stated result by hand.
````

## `Cargo.toml` (7 lines)

````toml
[package]
name = "bennett-isa-ref"
version = "0.0.0"
edition = "2021"
license = "AGPL-3.0-only"

[dependencies]
````

## `src/lib.rs` (43 lines)

````rust
//! Executable reference semantics for the Bennett ISA, version 0.8.
mod action;
mod borrow;
mod call_discipline;
mod classical;
mod handle_validation;
mod identity;
pub mod json;
mod linking;
mod machine;
mod object;
mod oracle;
mod quantum;
mod registers;
mod sha256;
mod validation;
pub use classical::{ClassicalMachine, ClassicalOutcome, ClassicalSnapshot, ClassicalValue};
pub use classical::{HostExchange, HostRequest};
pub use identity::Identity;
pub use machine::{BasisConfiguration, OracleMachine};
pub use object::*;
pub use oracle::{Argument, Budget, OracleInput, OracleOutcome};
pub use quantum::{Complex, MeasurementBranch, QuantumBindings, QuantumRegion, QuantumState};
pub use registers::QuantumRegisters;
pub use borrow::validate_translation_lemma;
pub use sha256::{sha256, sha256_hex};

/// A diagnostic always names the normative rule that was violated.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Error(pub String);
impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.0)
    }
}
impl std::error::Error for Error {}
pub type Result<T> = std::result::Result<T, Error>;
pub(crate) fn err<T>(rule: &str, message: impl std::fmt::Display) -> Result<T> {
    Err(Error(format!("{rule}: {message}")))
}
pub fn version() -> &'static str {
    "0.8"
}
````

## `src/action.rs` (818 lines)

````rust
use crate::{
    err,
    object::list,
    quantum::Wire,
    validation::{gate, normalize_call},
    Argument, Error, Function, Instruction, Object, OracleInput, OracleMachine, QuantumBindings,
    QuantumRegion, QuantumState, Result, Type,
};
use std::collections::{BTreeMap, BTreeSet};

struct Environment {
    bindings: QuantumBindings,
    widths: BTreeMap<String, usize>,
    predicates: Vec<Wire>,
    borrowed: BTreeMap<String, Vec<usize>>,
    borrow_used: BTreeSet<usize>,
}
impl Environment {
    fn bundle(&self, n: &str) -> Result<Vec<Wire>> {
        if let Some((base, index)) = n.split_once('[') {
            let index = index
                .strip_suffix(']')
                .and_then(|s| s.parse::<usize>().ok())
                .ok_or_else(|| Error("§3.3: invalid wire index".into()))?;
            let ws = self
                .bindings
                .bundles
                .get(base)
                .ok_or_else(|| Error(format!("§3.3: unknown live bundle {base}")))?;
            return ws
                .get(index)
                .map(|w| vec![*w])
                .ok_or_else(|| Error("§3.3: wire index out of range".into()));
        }
        self.bindings
            .bundles
            .get(n)
            .cloned()
            .ok_or_else(|| Error(format!("§3.3: unknown live bundle {n}")))
    }
    fn scalar(&self, n: &str) -> Result<Wire> {
        let w = self.bundle(n)?;
        if w.len() != 1 {
            return err("§3.3", "scalar wire required");
        }
        Ok(w[0])
    }
    fn controls(&self, inherited: &[(Wire, bool)]) -> Vec<(Wire, bool)> {
        let mut c = inherited.to_vec();
        for w in &self.predicates {
            if !c.contains(&(*w, true)) {
                c.push((*w, true));
            }
        }
        c
    }
    fn produce(&mut self, n: &str, wires: Vec<Wire>) -> Result<()> {
        if self.bindings.bundles.contains_key(n) {
            return err("§3.3", "live bundle produced twice");
        }
        self.widths.insert(n.into(), wires.len());
        self.bindings.bundles.insert(n.into(), wires);
        Ok(())
    }
}
impl Object {
    pub(crate) fn permutation_action_values(
        &self,
        name: &str,
        mutables: &[u128],
        inputs: &[u128],
        regions: &BTreeMap<String, Vec<u8>>,
        args: &[Argument],
        adjoint: bool,
    ) -> Result<Vec<u128>> {
        let f = &self.functions[name];
        if f.kind != "perm_action"
            || mutables.len() != f.params[0].len()
            || inputs.len() != f.params[1].len()
            || args.len() != f.params[3].len()
        {
            return err("§4.2", "lift.perm_call interface mismatch");
        }
        let mut q = QuantumState::new();
        let mut b = QuantumBindings::default();
        for (values, ps) in [(mutables, &f.params[0]), (inputs, &f.params[1])] {
            for (v, p) in values.iter().zip(ps) {
                let wires = q.allocate(p.ty.width(self.ptr_width)? as usize)?;
                for (i, w) in wires.iter().enumerate() {
                    if i < 128 && v & (1u128 << i) != 0 {
                        q.gate("x", &[*w], None, &[])?;
                    }
                }
                b.bundles.insert(p.name.clone(), wires);
            }
        }
        for p in &f.params[2] {
            let Type::Region(a, w) = p.ty else {
                unreachable!("region")
            };
            let bytes = regions
                .get(&p.name)
                .ok_or_else(|| Error("§4.2: missing lifted action region".into()))?;
            let mut cells = Vec::new();
            for byte in bytes {
                let cell = q.allocate(w as usize)?;
                for (i, wire) in cell.iter().enumerate() {
                    if i < 8 && byte & (1u8 << i) != 0 {
                        q.gate("x", &[*wire], None, &[])?;
                    }
                }
                cells.push(cell);
            }
            b.regions.insert(
                p.name.clone(),
                QuantumRegion {
                    address_width: a,
                    cell_width: w,
                    cells,
                },
            );
        }
        for (p, v) in f.params[3].iter().zip(args) {
            b.args.insert(p.name.clone(), v.clone());
        }
        let capacity=self.borrow_capacity(name)?;
        let idle=q.allocate(capacity)?;if !idle.is_empty(){b.borrowed.push(idle.clone());}
        self.execute_action(name, &mut q, &b, adjoint, &[])?;
        q.release(&idle)?;
        f.params[0]
            .iter()
            .map(|p| q.read_basis(&b.bundles[&p.name]))
            .collect()
    }
    fn borrow_capacity(&self,root:&str)->Result<usize>{
        fn scan(seq:&[Instruction],count:&mut usize,children:&mut Vec<String>)->Result<()>{for i in seq{if i.op=="qborrow"{*count=count.checked_add(i.operands[1].parse::<usize>().map_err(|_|Error("§5.6: borrow count exceeds host storage".into()))?).ok_or_else(||Error("§5.6: borrow capacity overflow".into()))?;}if let Ok(call)=normalize_call(i){if call.instruction.op=="action_call"{children.push(call.instruction.operands[0].trim_start_matches('@').into());}}for body in &i.bodies{scan(body,count,children)?;}}Ok(())}
        let mut count=0;let mut pending=vec![root.to_string()];let mut visited=BTreeSet::new();while let Some(name)=pending.pop(){if !visited.insert(name.clone()){continue;}let function=self.functions.get(&name).ok_or_else(||Error(format!("§9.3: unresolved action @{name}")))?;for block in &function.blocks{scan(&block.instructions,&mut count,&mut pending)?;}}Ok(count)
    }
    pub fn execute_action(
        &self,
        name: &str,
        q: &mut QuantumState,
        bindings: &QuantumBindings,
        adjoint: bool,
        controls: &[Wire],
    ) -> Result<()> {
        self.ensure_linked()?;
        self.action_internal(
            name,
            q,
            bindings,
            adjoint,
            &controls.iter().map(|w| (*w, true)).collect::<Vec<_>>(),
        )
    }
    fn action_internal(
        &self,
        name: &str,
        q: &mut QuantumState,
        bindings: &QuantumBindings,
        adjoint: bool,
        controls: &[(Wire, bool)],
    ) -> Result<()> {
        let f = self
            .functions
            .get(name)
            .filter(|f| matches!(f.kind.as_str(), "action" | "perm_action"))
            .ok_or_else(|| Error(format!("§5.3: unknown action @{name}")))?;
        let mut used = BTreeSet::new();
        for p in f.params[0].iter().chain(&f.params[1]) {
            let w = bindings
                .bundles
                .get(&p.name)
                .ok_or_else(|| Error(format!("§5.1: missing bundle {}", p.name)))?;
            if w.len() != p.ty.width(self.ptr_width)? as usize {
                return err("§3.3", "action bundle width mismatch");
            }
            for wire in w {
                q.position(*wire)?;
                if !used.insert(wire) {
                    return err("§3.3", "action interface bundles overlap");
                }
            }
        }
        for p in &f.params[2] {
            let Type::Region(a, w) = p.ty else {
                unreachable!("validated region")
            };
            let r = bindings
                .regions
                .get(&p.name)
                .ok_or_else(|| Error("§5.1: missing interface region".into()))?;
            if r.address_width != a
                || r.cell_width != w
                || r.cells.len() as u128 != 1u128 << a
                || r.cells.iter().any(|c| c.len() != w as usize)
            {
                return err("§3.3", "action interface region dimensions mismatch");
            }
            for wire in r.cells.iter().flatten() {
                q.position(*wire)?;
                if !used.insert(wire) {
                    return err("§3.3", "action regions overlap interface");
                }
            }
        }
        for p in &f.params[3] {
            let arg = bindings
                .args
                .get(&p.name)
                .ok_or_else(|| Error("§5.1: missing action classical argument".into()))?;
            match (&p.ty, arg) {
                (Type::Token, Argument::Token(b)) => self.validate_budget(*b)?,
                (Type::Int(w), Argument::Bits(n)) if *w == 128 || *n < 1u128 << w => {}
                (Type::F64, Argument::Float(a)) if a.is_finite() => {}
                _ => return err("§3.3", "action argument type mismatch"),
            }
        }
        let mut env = Environment {
            bindings: bindings.clone(),
            widths: bindings
                .bundles
                .iter()
                .map(|(n, w)| (n.clone(), w.len()))
                .collect(),
            predicates: Vec::new(),
            borrowed: BTreeMap::new(),
            borrow_used: BTreeSet::new(),
        };
        let mut regions = Vec::new();
        for b in &f.blocks {
            gather_regions(&b.instructions, &mut regions);
        }
        let mut local = Vec::new();
        for i in regions {
            let a = i.operands[1].parse::<u16>().expect("address width");
            let w = i.operands[2].parse::<u16>().expect("cell width");
            let count = usize::try_from(1u128 << a)
                .map_err(|_| Error("§4.6: local region exceeds host address space".into()))?;
            let n = count
                .checked_mul(w as usize)
                .ok_or_else(|| Error("§4.6: region bit size overflow".into()))?;
            let wires = q.allocate(n)?;
            let image = if i.operands.len() == 4 {
                self.data[i.operands[3].trim_start_matches('@')].clone()
            } else {
                vec![0; n.div_ceil(8)]
            };
            for (bit, wire) in wires.iter().enumerate() {
                if image[bit / 8] & (1 << (bit % 8)) != 0 {
                    q.gate("x", &[*wire], None, &[])?;
                }
            }
            let cells = wires.chunks_exact(w as usize).map(|c| c.to_vec()).collect();
            env.bindings.regions.insert(
                i.operands[0].clone(),
                QuantumRegion {
                    address_width: a,
                    cell_width: w,
                    cells,
                },
            );
            local.push((wires, image));
        }
        for b in &f.blocks {
            infer_widths(&b.instructions, &mut env)?;
        }
        let instructions: Vec<_> = f
            .blocks
            .iter()
            .flat_map(|b| b.instructions.iter().cloned())
            .collect();
        self.action_sequence(&instructions, q, &mut env, adjoint, controls)?;
        if !env.predicates.is_empty() || !env.borrowed.is_empty() {
            return err("§5.1", "action exited with unclosed predicate/borrow frame");
        }
        let interface: BTreeSet<_> = bindings.bundles.keys().collect();
        if env.bindings.bundles.keys().any(|n| !interface.contains(n)) {
            return err("§5.1", "action exited with live workspace");
        }
        for (wires, image) in local.into_iter().rev() {
            for (bit, wire) in wires.iter().enumerate() {
                if image[bit / 8] & (1 << (bit % 8)) != 0 {
                    q.gate("x", &[*wire], None, &[])?;
                }
            }
            q.release(&wires)?;
        }
        Ok(())
    }
    fn action_sequence(
        &self,
        sequence: &[Instruction],
        q: &mut QuantumState,
        e: &mut Environment,
        adjoint: bool,
        inherited: &[(Wire, bool)],
    ) -> Result<()> {
        let indices: Vec<_> = if adjoint {
            (0..sequence.len()).rev().collect()
        } else {
            (0..sequence.len()).collect()
        };
        for index in indices {
            let i = &sequence[index];
            let a = &i.operands;
            let context = e.controls(inherited);
            let op = i.op.as_str();
            if gate(op) {
                let mut wires = Vec::new();
                let mut angle = None;
                if op == "mcx" {
                    for n in list(&a[0])? {
                        wires.push(e.scalar(&n)?);
                    }
                    wires.push(e.scalar(&a[1])?);
                } else if matches!(op, "rx" | "ry" | "rz") {
                    let theta = match a[0].parse::<f64>() {
                        Ok(n) => n,
                        Err(_) => match e.bindings.args.get(&a[0]) {
                            Some(Argument::Float(n)) => *n,
                            _ => return err("§4.4", "angle is not a finite classical f64"),
                        },
                    };
                    angle = Some(if adjoint { -theta } else { theta });
                    wires.push(e.scalar(&a[1])?);
                } else {
                    for n in a {
                        wires.push(e.scalar(n)?);
                    }
                }
                let inverse = if adjoint {
                    match op {
                        "s" => "sdg",
                        "sdg" => "s",
                        "t" => "tdg",
                        "tdg" => "t",
                        _ => op,
                    }
                } else {
                    op
                };
                q.controlled_gate(inverse, &wires, angle, &context)?;
                continue;
            }
            match op {
                "qregion" => {}
                "qpred" | "qunpred" => {
                    let push = (op == "qpred") ^ adjoint;
                    let wire = e.scalar(&a[0])?;
                    if push {
                        e.predicates.push(wire);
                    } else if e.predicates.pop() != Some(wire) {
                        return err("§3.5", "action predicate pop mismatch");
                    }
                }
                "qif" => {
                    let w = e.scalar(&a[0])?;
                    let mut yes = context.clone();
                    yes.push((w, true));
                    self.action_sequence(&i.bodies[0], q, e, adjoint, &yes)?;
                    let mut no = context.clone();
                    no.push((w, false));
                    self.action_sequence(&i.bodies[1], q, e, adjoint, &no)?;
                }
                "qloop" => {
                    let n = a[0]
                        .parse::<usize>()
                        .map_err(|_| Error("§4.6: loop bound exceeds host index space".into()))?;
                    if a.len() == 1 {
                        for _ in 0..n {
                            self.action_sequence(&i.bodies[0], q, e, adjoint, &context)?;
                        }
                    } else {
                        let condition = e.bundle(&a[2])?;
                        let flags = q.allocate(n)?;
                        if adjoint {
                            for j in 0..n {
                                let controls = if j == 0 {
                                    vec![condition[j], flags[j]]
                                } else {
                                    vec![flags[j - 1], condition[j], flags[j]]
                                };
                                q.controlled_gate(
                                    if j == 0 { "cx" } else { "ccx" },
                                    &controls,
                                    None,
                                    &context,
                                )?;
                            }
                            for j in (0..n).rev() {
                                let mut c = context.clone();
                                c.push((flags[j], true));
                                self.action_sequence(&i.bodies[0], q, e, true, &c)?;
                            }
                        } else {
                            for j in 0..n {
                                let controls = if j == 0 {
                                    vec![condition[j], flags[j]]
                                } else {
                                    vec![flags[j - 1], condition[j], flags[j]]
                                };
                                q.controlled_gate(
                                    if j == 0 { "cx" } else { "ccx" },
                                    &controls,
                                    None,
                                    &context,
                                )?;
                                let mut c = context.clone();
                                c.push((flags[j], true));
                                self.action_sequence(&i.bodies[0], q, e, false, &c)?;
                            }
                        }
                        for j in (0..n).rev() {
                            let controls = if j == 0 {
                                vec![condition[j], flags[j]]
                            } else {
                                vec![flags[j - 1], condition[j], flags[j]]
                            };
                            q.controlled_gate(
                                if j == 0 { "cx" } else { "ccx" },
                                &controls,
                                None,
                                &context,
                            )?;
                        }
                        q.release(&flags)?;
                    }
                }
                "qalloc" | "qfree" => {
                    let allocate = (op == "qalloc") ^ adjoint;
                    let name = if op == "qalloc" { &i.lhs[0] } else { &a[0] };
                    if allocate {
                        let n = e.widths[name];
                        let w = q.allocate(n)?;
                        e.produce(name, w)?;
                    } else {
                        let w = e.bundle(name)?;
                        q.release(&w)?;
                        e.bindings.bundles.remove(name);
                    }
                }
                "qborrow" | "qreturn" => {
                    let borrow = (op == "qborrow") ^ adjoint;
                    let name = if op == "qborrow" { &i.lhs[0] } else { &a[0] };
                    if borrow {
                        let n = e.widths[name];
                        let pool=e.bindings.borrowed.iter().flatten().copied().collect::<Vec<_>>();
                        let indices=(0..pool.len()).filter(|i|!e.borrow_used.contains(i)).take(n).collect::<Vec<_>>();
                        if indices.len()!=n{return err("§5.6","designated idle set lacks requested borrowed wires");}
                        let wires=indices.iter().map(|i|pool[*i]).collect();e.borrow_used.extend(&indices);e.borrowed.insert(name.into(),indices);e.produce(name,wires)?;
                    } else {
                        let indices = e
                            .borrowed
                            .remove(name)
                            .ok_or_else(|| Error("§5.6: unmatched return".into()))?;
                        for index in indices{e.borrow_used.remove(&index);}
                        e.bindings.bundles.remove(name);
                    }
                }
                "qcopy" | "quncopy" => {
                    let copy = (op == "qcopy") ^ adjoint;
                    let source = e.bundle(&a[0])?;
                    let name = if op == "qcopy" { &i.lhs[0] } else { &a[1] };
                    let destination = if copy {
                        let w = q.allocate(source.len())?;
                        e.produce(name, w.clone())?;
                        w
                    } else {
                        e.bundle(name)?
                    };
                    bundle_xor(q, &source, &destination, &context)?;
                    if !copy {
                        q.release(&destination)?;
                        e.bindings.bundles.remove(name);
                    }
                }
                "qxor" => bundle_xor(q, &e.bundle(&a[0])?, &e.bundle(&a[1])?, &context)?,
                "qexch" => bundle_exchange(q, &e.bundle(&a[0])?, &e.bundle(&a[1])?, &context)?,
                "qload" | "qunload" | "qstore" | "qexchm" => {
                    let region = e
                        .bindings
                        .regions
                        .get(&a[0])
                        .cloned()
                        .ok_or_else(|| Error("§4.6: quantum region not found".into()))?;
                    let address = e.bundle(&a[1])?;
                    let load = matches!(op, "qload" | "qunload");
                    let compute = (op == "qload") ^ adjoint;
                    let name = if op == "qload" { &i.lhs[0] } else { &a[2] };
                    let value = if load && compute {
                        let w = q.allocate(region.cell_width as usize)?;
                        e.produce(name, w.clone())?;
                        w
                    } else {
                        e.bundle(name)?
                    };
                    for (index, cell) in region.cells.iter().enumerate() {
                        let mut c = context.clone();
                        for (bit, w) in address.iter().enumerate() {
                            c.push((*w, index & (1usize << bit) != 0));
                        }
                        if op == "qexchm" {
                            bundle_exchange(q, cell, &value, &c)?;
                        } else if load {
                            bundle_xor(q, cell, &value, &c)?;
                        } else {
                            bundle_xor(q, &value, cell, &c)?;
                        }
                    }
                    if load && !compute {
                        q.release(&value)?;
                        e.bindings.bundles.remove(name);
                    }
                }
                "oracle_call" | "action_call" | "adj" | "ctl" => {
                    let call = normalize_call(i)?;
                    let mut c = context.clone();
                    if let Some(w) = call.control {
                        c.push((e.scalar(&w)?, true));
                    }
                    let ca = &call.instruction.operands;
                    let callee = &self.functions[ca[0].trim_start_matches('@')];
                    if call.instruction.op == "oracle_call" {
                        let token = e
                            .bindings
                            .args
                            .get(&ca[1])
                            .and_then(|v| {
                                if let Argument::Token(b) = v {
                                    Some(*b)
                                } else {
                                    None
                                }
                            })
                            .ok_or_else(|| Error("§4.7: missing oracle token".into()))?;
                        let ins = list(&ca[2])?
                            .iter()
                            .map(|n| e.bundle(n))
                            .collect::<Result<Vec<_>>>()?;
                        let target = e.bundle(&ca[3])?;
                        let fault = e.bundle(&ca[4])?;
                        let mut regions = BTreeMap::new();
                        for (p, n) in callee.params[3].iter().zip(list(&ca[5])?) {
                            regions.insert(
                                p.name.clone(),
                                e.bindings
                                    .regions
                                    .get(&n)
                                    .ok_or_else(|| Error("§4.7: missing memory region".into()))?
                                    .clone(),
                            );
                        }
                        let args =
                            list(&ca[6])?
                                .iter()
                                .map(|n| {
                                    e.bindings.args.get(n).cloned().ok_or_else(|| {
                                        Error("§4.7: missing classical argument".into())
                                    })
                                })
                                .collect::<Result<Vec<_>>>()?;
                        self.oracle_quantum(
                            callee, q, &ins, &target, &fault, &regions, &args, token, &c,
                        )?;
                    } else {
                        let mut binding = QuantumBindings {
                            borrowed: vec![e.bindings.borrowed.iter().flatten().enumerate().filter_map(|(i,w)|(!e.borrow_used.contains(&i)).then_some(*w)).collect()],
                            ..QuantumBindings::default()
                        };
                        for group in 0..2 {
                            for (p, n) in callee.params[group].iter().zip(list(&ca[group + 1])?) {
                                binding.bundles.insert(p.name.clone(), e.bundle(&n)?);
                            }
                        }
                        for (p, n) in callee.params[2].iter().zip(list(&ca[3])?) {
                            binding
                                .regions
                                .insert(p.name.clone(), e.bindings.regions[&n].clone());
                        }
                        for (p, n) in callee.params[3].iter().zip(list(&ca[4])?) {
                            binding
                                .args
                                .insert(p.name.clone(), e.bindings.args[&n].clone());
                        }
                        self.action_internal(
                            &callee.name,
                            q,
                            &binding,
                            adjoint ^ call.adjoint,
                            &c,
                        )?;
                    }
                }
                "qinplace" => {
                    let g = &a[if adjoint { 1 } else { 0 }];
                    let gi = &a[if adjoint { 0 } else { 1 }];
                    let x = e.bundle(&a[3])?;
                    let token = e
                        .bindings
                        .args
                        .get(&a[2])
                        .and_then(|v| {
                            if let Argument::Token(b) = v {
                                Some(*b)
                            } else {
                                None
                            }
                        })
                        .ok_or_else(|| Error("§4.5: qinplace token".into()))?;
                    let gf = &self.functions[g.trim_start_matches('@')];
                    let gif = &self.functions[gi.trim_start_matches('@')];
                    let fw = gf.params[2][0].ty.width(self.ptr_width)? as usize;
                    let t = q.allocate(x.len())?;
                    let fault = q.allocate(fw)?;
                    self.oracle_quantum(
                        gf,
                        q,
                        std::slice::from_ref(&x),
                        &t,
                        &fault,
                        &BTreeMap::new(),
                        &[],
                        token,
                        &context,
                    )?;
                    bundle_exchange(q, &x, &t, &context)?;
                    self.oracle_quantum(
                        gif,
                        q,
                        &[x],
                        &t,
                        &fault,
                        &BTreeMap::new(),
                        &[],
                        token,
                        &context,
                    )?;
                    q.release(&t)?;
                    q.release(&fault)?;
                }
                _ => return err("§4.8", format!("unimplemented Q instruction {op}")),
            }
        }
        Ok(())
    }
    #[allow(clippy::too_many_arguments)]
    pub(crate) fn oracle_quantum(
        &self,
        callee: &Function,
        q: &mut QuantumState,
        ins: &[Vec<Wire>],
        target: &[Wire],
        fault: &[Wire],
        regions: &BTreeMap<String, QuantumRegion>,
        args: &[Argument],
        budget: crate::Budget,
        controls: &[(Wire, bool)],
    ) -> Result<()> {
        let input_positions = ins
            .iter()
            .map(|w| w.iter().map(|w| q.position(*w)).collect::<Result<Vec<_>>>())
            .collect::<Result<Vec<_>>>()?;
        let target = target
            .iter()
            .map(|w| q.position(*w))
            .collect::<Result<Vec<_>>>()?;
        let fault = fault
            .iter()
            .map(|w| q.position(*w))
            .collect::<Result<Vec<_>>>()?;
        let controls = controls
            .iter()
            .map(|(w, v)| Ok((q.position(*w)?, *v)))
            .collect::<Result<Vec<_>>>()?;
        let regions: BTreeMap<_, _> = regions
            .iter()
            .map(|(n, r)| {
                Ok((
                    n.clone(),
                    r.cells
                        .iter()
                        .map(|c| c.iter().map(|w| q.position(*w)).collect::<Result<Vec<_>>>())
                        .collect::<Result<Vec<_>>>()?,
                ))
            })
            .collect::<Result<_>>()?;
        q.permute(|bits| {
            let mut result = bits.to_vec();
            if controls.iter().any(|(p, v)| bits[*p] != *v) {
                return Ok(result);
            }
            let mut input = OracleInput::bits(
                &input_positions
                    .iter()
                    .map(|p| read_bits(bits, p))
                    .collect::<Result<Vec<_>>>()?,
            );
            input.args = args.to_vec();
            for (n, cells) in &regions {
                input.regions.insert(
                    n.clone(),
                    cells
                        .iter()
                        .map(|p| read_bits(bits, p).map(|v| v as u8))
                        .collect::<Result<Vec<_>>>()?,
                );
            }
            let mut machine = OracleMachine::new(self, &callee.name, &input, budget)?;
            let before = machine.snapshot();
            for _ in 0..budget.steps {
                machine.forward_step()?;
            }
            let outcome = machine.outcome();
            for _ in 0..budget.steps {
                machine.inverse_step()?;
            }
            if machine.snapshot() != before {
                return err("§5.2", "oracle ancillae did not restore");
            }
            for (i, p) in target.iter().enumerate() {
                if i < 128 {
                    result[*p] ^= outcome.payload & (1u128 << i) != 0;
                }
            }
            for (i, p) in fault.iter().enumerate() {
                if i < 128 {
                    result[*p] ^= outcome.code & (1u128 << i) != 0;
                }
            }
            Ok(result)
        })
    }
}
fn gather_regions<'a>(seq: &'a [Instruction], out: &mut Vec<&'a Instruction>) {
    for i in seq {
        if i.op == "qregion" {
            out.push(i);
        }
        for b in &i.bodies {
            gather_regions(b, out);
        }
    }
}
fn infer_widths(seq: &[Instruction], e: &mut Environment) -> Result<()> {
    for i in seq {
        match i.op.as_str() {
            "qalloc" | "qborrow" => {
                e.widths.insert(
                    i.lhs[0].clone(),
                    i.operands[1]
                        .parse()
                        .map_err(|_| Error("§4.3: allocation width".into()))?,
                );
            }
            "qcopy" => {
                let n = if i.operands[0].contains('[') {
                    1
                } else {
                    *e.widths
                        .get(&i.operands[0])
                        .ok_or_else(|| Error("§3.3: copy source width".into()))?
                };
                e.widths.insert(i.lhs[0].clone(), n);
            }
            "qload" => {
                let r = e
                    .bindings
                    .regions
                    .get(&i.operands[0])
                    .ok_or_else(|| Error("§4.6: load region width".into()))?;
                e.widths.insert(i.lhs[0].clone(), r.cell_width as usize);
            }
            _ => {}
        }
        for b in &i.bodies {
            infer_widths(b, e)?;
        }
    }
    Ok(())
}
fn bundle_xor(
    q: &mut QuantumState,
    source: &[Wire],
    target: &[Wire],
    context: &[(Wire, bool)],
) -> Result<()> {
    if source.len() != target.len() {
        return err("§3.3", "XOR bundle widths differ");
    }
    for (s, t) in source.iter().zip(target) {
        q.controlled_gate("cx", &[*s, *t], None, context)?;
    }
    Ok(())
}
fn bundle_exchange(
    q: &mut QuantumState,
    a: &[Wire],
    b: &[Wire],
    context: &[(Wire, bool)],
) -> Result<()> {
    if a.len() != b.len() {
        return err("§3.3", "exchange bundle widths differ");
    }
    for (s, t) in a.iter().zip(b) {
        q.controlled_gate("swap", &[*s, *t], None, context)?;
    }
    Ok(())
}
fn read_bits(bits: &[bool], positions: &[usize]) -> Result<u128> {
    if positions.len() > 128 {
        return err("§3.3", "integer evaluation exceeds 128 bits");
    }
    Ok(positions
        .iter()
        .enumerate()
        .fold(0, |n, (i, p)| n | ((bits[*p] as u128) << i)))
}
````

## `src/borrow.rs` (61 lines)

````rust
//! §5.6 translation lemma and exact small-frame permutation verification.
use crate::{err,object::list,validation::{gate,gate_operands},Error,Function,Instruction,Object,Result,Type};
use std::collections::{BTreeMap,BTreeSet};

pub fn validate_translation_lemma(v:&[Instruction],w:&[Instruction],x:&BTreeSet<String>,borrowed:&BTreeSet<String>)->Result<()>{
    if !x.is_disjoint(borrowed){return err("§5.6","translation lemma requires X disjoint from B");}
    let flips=|sequence:&[Instruction]|->Result<Vec<(Vec<String>,String)>>{sequence.iter().map(|i|{if !["x","cx","ccx","mcx"].contains(&i.op.as_str()){return err("§5.6","translation lemma contains a non-X-family gate");}let(c,t,_,_)=gate_operands(i)?;Ok((c,t[0].clone()))}).collect()};
    let v=flips(v)?;let w=flips(w)?;let controls:BTreeSet<_>=w.iter().flat_map(|(c,_)|c.iter().cloned()).collect();
    for(c,t)in v{if !borrowed.contains(&t)||c.iter().any(|c|!x.contains(c)){return err("§5.6","V must target only B with controls only in X");}}
    for(c,t)in w{if x.contains(&t)||borrowed.contains(&t)||controls.contains(&t){return err("§5.6","W target overlaps X, B, or W's controls");}if c.iter().filter(|c|borrowed.contains(*c)).count()>1{return err("§5.6","W gate has more than one borrowed control");}}
    Ok(())
}
#[derive(Clone,Debug,PartialEq,Eq)]
struct Operation{op:String,controls:Vec<(String,bool)>,targets:Vec<String>,permutation:bool,opaque:bool}
impl Operation{
    fn wires(&self)->impl Iterator<Item=&String>{self.controls.iter().map(|(w,_)|w).chain(&self.targets)}
    fn instruction(&self)->Instruction{let controls=self.controls.iter().map(|(w,_)|w.clone()).collect::<Vec<_>>();let(op,operands)=match controls.len(){0=>("x".into(),self.targets.clone()),1=>("cx".into(),[controls,self.targets.clone()].concat()),2=>("ccx".into(),[controls,self.targets.clone()].concat()),_ =>("mcx".into(),vec![format!("({})",controls.join(", ")),self.targets[0].clone()])};Instruction{lhs:Vec::new(),op,operands,bodies:Vec::new(),line:0}}
}
struct Compiler{bundles:BTreeMap<String,Vec<String>>,borrowed:BTreeSet<String>,operations:Vec<Operation>,generation:usize}
impl Compiler{
    fn bundle(&self,name:&str)->Result<Vec<String>>{if let Some((base,index))=name.split_once('['){let index=index.trim_end_matches(']').parse::<usize>().map_err(|_|Error("§3.3: indexed borrow operand".into()))?;return self.bundles.get(base).and_then(|w|w.get(index)).map(|w|vec![w.clone()]).ok_or_else(||Error("§3.3: unknown indexed borrow operand".into()));}self.bundles.get(name).cloned().ok_or_else(||Error(format!("§3.3: unknown borrow operand {name}")))}
    fn produce(&mut self,name:&str,width:usize)->Vec<String>{let generation=self.generation;self.generation+=1;let wires=(0..width).map(|bit|format!("v{generation}_{bit}")).collect::<Vec<_>>();self.bundles.insert(name.into(),wires.clone());wires}
    fn flip(&mut self,source:String,target:String,context:&[(String,bool)]){let mut controls=context.to_vec();if !controls.contains(&(source.clone(),true)){controls.push((source,true));}self.operations.push(Operation{op:"x".into(),controls,targets:vec![target],permutation:true,opaque:false});}
    fn compile(&mut self,seq:&[Instruction],context:&[(String,bool)])->Result<()>{let mut predicate=context.to_vec();for i in seq{let a=&i.operands;let op=i.op.as_str();match op{
        "qalloc"|"qborrow"=>{let wires=self.produce(&i.lhs[0],a[1].parse().map_err(|_|Error("§4.3: allocation width".into()))?);if op=="qborrow"{self.borrowed.extend(wires);}},
        "qfree"|"qreturn"=>{self.bundles.remove(&a[0]);},
        "qpred"=>{predicate.push((self.bundle(&a[0])?[0].clone(),true));},"qunpred"=>{predicate.pop().ok_or_else(||Error("§3.5: borrow predicate underflow".into()))?;},
        "qcopy"|"quncopy"=>{let source=self.bundle(&a[0])?;let target=if op=="qcopy"{self.produce(&i.lhs[0],source.len())}else{self.bundle(&a[1])?};for(s,t)in source.into_iter().zip(target){self.flip(s,t,&predicate);}if op=="quncopy"{self.bundles.remove(&a[1]);}},
        "qxor"=>{for(s,t)in self.bundle(&a[0])?.into_iter().zip(self.bundle(&a[1])?){self.flip(s,t,&predicate);}},
        "qexch"=>{for(s,t)in self.bundle(&a[0])?.into_iter().zip(self.bundle(&a[1])?){self.operations.push(Operation{op:"swap".into(),controls:predicate.clone(),targets:vec![s,t],permutation:true,opaque:false});}},
        "qif"=>{let selector=self.bundle(&a[0])?[0].clone();let mut yes=predicate.clone();yes.push((selector.clone(),true));self.compile(&i.bodies[0],&yes)?;let mut no=predicate.clone();no.push((selector,false));self.compile(&i.bodies[1],&no)?;},
        "qloop"=>{let count=a[0].parse::<usize>().map_err(|_|Error("§4.6: loop size".into()))?;if count>1_000_000{return err("§5.6","borrow circuit expansion exceeds reference verifier storage; supply a structural/library claim");}for iteration in 0..count{let mut c=predicate.clone();if a.len()==3{let selectors=self.bundle(&a[2])?;for selector in &selectors[..=iteration]{c.push((selector.clone(),true));}}self.compile(&i.bodies[0],&c)?;}},
        _ if gate(op)=>{let(controls,targets,_,_)=gate_operands(i)?;let mut context=predicate.clone();for control in controls{let wire=self.bundle(&control)?[0].clone();if !context.contains(&(wire.clone(),true)){context.push((wire,true));}}let targets=targets.iter().map(|w|self.bundle(w).map(|w|w[0].clone())).collect::<Result<Vec<_>>>()?;self.operations.push(Operation{op:if op=="swap"{"swap".into()}else{op.into()},controls:context,targets,permutation:["x","cx","ccx","mcx","swap"].contains(&op),opaque:false});},
        _=>{let mut operands=Vec::new();for operand in a{if operand.starts_with('('){operands.extend(list(operand)?);}else{operands.push(operand.clone());}}let touched=operands.iter().filter_map(|n|self.bundles.get(n)).flatten().cloned().collect();self.operations.push(Operation{op:op.into(),controls:predicate.clone(),targets:touched,permutation:true,opaque:true});},
    }}Ok(())}
}
impl Object{
    pub(crate) fn validate_borrow_frames(&self,f:&Function)->Result<()>{
        fn has_borrow(seq:&[Instruction])->bool{seq.iter().any(|i|i.op=="qborrow"||i.bodies.iter().any(|b|has_borrow(b)))}
        if !f.blocks.iter().any(|b|has_borrow(&b.instructions)){return Ok(());}
        let mut compiler=Compiler{bundles:BTreeMap::new(),borrowed:BTreeSet::new(),operations:Vec::new(),generation:0};
        for p in f.params.iter().flatten(){if let Type::Wire(width)=p.ty{compiler.produce(&p.name,width as usize);}}
        for block in &f.blocks{compiler.compile(&block.instructions,&[])?;}
        let mut start=0;while start<compiler.operations.len(){let op=&compiler.operations[start];if !op.permutation{if op.wires().any(|w|compiler.borrowed.contains(w)){return err("§5.6","borrowed wire touched by a non-permutation instruction");}start+=1;continue;}
            let end=(start..compiler.operations.len()).find(|i|!compiler.operations[*i].permutation).unwrap_or(compiler.operations.len());
            let touches=|op:&Operation|op.wires().any(|w|compiler.borrowed.contains(w));let first=(start..end).find(|i|touches(&compiler.operations[*i]));let last=(start..end).rfind(|i|touches(&compiler.operations[*i]));
            if let(Some(first),Some(last))=(first,last){verify_frame(&compiler.operations[first..=last],&compiler.borrowed)?;}start=end;
        }Ok(())
    }
}
fn verify_frame(frame:&[Operation],borrowed:&BTreeSet<String>)->Result<()>{
    if frame.iter().any(|o|o.opaque){return err("§5.6","borrow frame requires a checked full-domain library claim for its opaque operation");}
    let only_flips=frame.iter().all(|op|op.op!="swap"&&op.controls.iter().all(|(_,v)|*v));
    if only_flips&&frame.len().is_multiple_of(2){let half=frame.len()/2;for vlen in 1..half{let wlen=half-vlen;let v=&frame[..vlen];let w=&frame[vlen..half];if frame[half..half+vlen].iter().eq(v.iter().rev())&&frame[half+vlen..]==*w{
        let x=v.iter().flat_map(|o|o.controls.iter().map(|(w,_)|w.clone())).collect();if validate_translation_lemma(&v.iter().map(Operation::instruction).collect::<Vec<_>>(),&w.iter().map(Operation::instruction).collect::<Vec<_>>(),&x,borrowed).is_ok(){return Ok(());}let _=wlen;
    }}}
    let wires:BTreeSet<_>=frame.iter().flat_map(Operation::wires).cloned().collect();if wires.len()>16{return err("§5.6","borrow frame exceeds 16 exhaustive wires and has no valid structural proof");}let positions:BTreeMap<_,_>=wires.into_iter().enumerate().map(|(i,w)|(w,i)).collect();let borrowed_indices:Vec<_>=positions.iter().filter_map(|(w,i)|borrowed.contains(w).then_some(*i)).collect();let mut outputs=BTreeMap::new();
    for input in 0..1usize<<positions.len(){let mut output=input;for operation in frame{if operation.controls.iter().all(|(w,value)|(output&(1usize<<positions[w])!=0)==*value){if operation.op=="swap"{let a=1usize<<positions[&operation.targets[0]];let b=1usize<<positions[&operation.targets[1]];if(output&a!=0)!=(output&b!=0){output^=a|b;}}else{output^=1usize<<positions[&operation.targets[0]];}}}
        let borrowed_mask=borrowed_indices.iter().fold(0,|m,i|m|(1usize<<i));if input&borrowed_mask!=output&borrowed_mask{return err("§5.6","borrow frame changes a borrowed wire");}let key=input&!borrowed_mask;let value=output&!borrowed_mask;if outputs.get(&key).is_some_and(|prior|*prior!=value){return err("§5.6","borrow frame output depends on borrowed entry values");}outputs.insert(key,value);
    }Ok(())
}
````

## `src/call_discipline.rs` (227 lines)

````rust
use crate::{
    err,
    object::list,
    validation::{gate, gate_operands, normalize_call},
    Error, Function, Instruction, Object, Result, Type,
};
use std::collections::{BTreeMap, BTreeSet};
impl Object {
    fn interface_targets(
        &self,
        name: &str,
        active: &mut BTreeSet<String>,
    ) -> Result<BTreeSet<(String, u16)>> {
        if !active.insert(name.into()) {
            return err("§5.1", "recursive region graph");
        }
        let f = self.declaration(name)?;
        let mut out = BTreeSet::new();
        let add = |out: &mut BTreeSet<(String, u16)>, operand: &str| -> Result<()> {
            let (base, index) = if let Some((base, index)) = operand.split_once('[') {
                (
                    base,
                    Some(
                        index
                            .trim_end_matches(']')
                            .parse::<u16>()
                            .map_err(|_| Error("§3.3: wire index".into()))?,
                    ),
                )
            } else {
                (operand, None)
            };
            if let Some(p) = f
                .params
                .iter()
                .flatten()
                .find(|p| p.name == base && matches!(p.ty, Type::Wire(_)))
            {
                if let Some(index) = index {
                    out.insert((base.into(), index));
                } else {
                    for bit in 0..p.ty.width(self.ptr_width)? {
                        out.insert((base.into(), bit));
                    }
                }
            }
            Ok(())
        };
        fn flattened<'a>(seq: &'a [Instruction], out: &mut Vec<&'a Instruction>) {
            for i in seq {
                out.push(i);
                for body in &i.bodies {
                    flattened(body, out);
                }
            }
        }
        let mut instructions = Vec::new();
        for b in &f.blocks {
            flattened(&b.instructions, &mut instructions);
        }
        for i in instructions {
            if gate(&i.op) {
                for target in gate_operands(i)?.1 {
                    add(&mut out, &target)?;
                }
            } else {
                match i.op.as_str() {
                    "qxor" => add(&mut out, &i.operands[1])?,
                    "qexch" => {
                        for target in &i.operands {
                            add(&mut out, target)?;
                        }
                    }
                    "qinplace" => add(&mut out, &i.operands[3])?,
                    "qexchm" => add(&mut out, &i.operands[2])?,
                    "oracle_call" | "action_call" | "adj" | "ctl" => {
                        let call = normalize_call(i)?;
                        let a = &call.instruction.operands;
                        if call.instruction.op == "oracle_call" {
                            add(&mut out, &a[3])?;
                            add(&mut out, &a[4])?;
                        } else {
                            let callee = a[0].trim_start_matches('@');
                            let declaration = self.declaration(callee)?;
                            let actuals = [list(&a[1])?, list(&a[2])?];
                            let targets = self.interface_targets(callee, active)?;
                            for (param, index) in targets {
                                for (group,actual) in actuals.iter().enumerate() {
                                    if let Some(position) = declaration.params[group]
                                        .iter()
                                        .position(|p| p.name == param)
                                    {
                                        add(
                                            &mut out,
                                            &format!("{}[{index}]", actual[position]),
                                        )?;
                                    }
                                }
                            }
                        }
                    }
                    _ => {}
                }
            }
        }
        active.remove(name);
        Ok(out)
    }
    pub(crate) fn validate_inherited_targets(
        &self,
        call: &Instruction,
        context: &[String],
        types: &BTreeMap<String, Type>,
    ) -> Result<()> {
        if context.is_empty() || call.op != "action_call" {
            return Ok(());
        }
        let a = &call.operands;
        let name = a[0].trim_start_matches('@');
        let f = self.declaration(name)?;
        let actuals = [list(&a[1])?, list(&a[2])?];
        let targets = self.interface_targets(name, &mut BTreeSet::new())?;
        for (param, index) in targets {
            for (group,actual) in actuals.iter().enumerate() {
                if let Some(position) = f.params[group].iter().position(|p| p.name == param) {
                    let actual = &actual[position];
                    if !matches!(types.get(actual), Some(Type::Wire(_))) {
                        return err("§3.3", "controlled region operand must be a wire bundle");
                    }
                    if context.contains(&format!("{actual}[{index}]")) {
                        return err(
                            "§3.3",
                            format!("inherited control targets callee wire {param}[{index}]"),
                        );
                    }
                }
            }
        }
        Ok(())
    }
    pub(crate) fn validate_matched_oracle_calls(&self, f: &Function) -> Result<()> {
        let mut rows = Vec::new();
        let mut labels = BTreeMap::new();
        for block in &f.blocks {
            labels.insert(block.name.clone(), rows.len());
            rows.extend(&block.instructions);
        }
        let mut predecessors = vec![Vec::new(); rows.len()];
        for (k, row) in rows.iter().enumerate() {
            let destinations: Vec<usize> = match row.op.as_str() {
                "qjump" => vec![labels[row.operands[0].trim_start_matches('^')]],
                "qbranch" => row.operands[1..]
                    .iter()
                    .map(|s| labels[s.trim_start_matches('^')])
                    .collect(),
                "qjumpr" => (0..rows.len()).collect(),
                "fault" | "lift.ret" | "lift.retval" => Vec::new(),
                _ => {
                    if k + 1 < rows.len() {
                        vec![k + 1]
                    } else {
                        Vec::new()
                    }
                }
            };
            for destination in destinations {
                predecessors[destination].push(k);
            }
        }
        for (k, uncall) in rows
            .iter()
            .enumerate()
            .filter(|(_, r)| r.op == "lift.oracle_uncall")
        {
            let ins = list(&uncall.operands[2])?;
            let memory = list(&uncall.operands[5])?;
            let mut work = predecessors[k].clone();
            let mut seen = BTreeSet::new();
            let mut found = false;
            while let Some(point) = work.pop() {
                if !seen.insert(point) {
                    continue;
                }
                let row = rows[point];
                if row.op == "lift.oracle_call" && row.operands == uncall.operands {
                    found = true;
                    continue;
                }
                if row.op == "lift.oracle_uncall" && row.operands == uncall.operands {
                    return err(
                        "§5.5",
                        "oracle_uncall has already consumed its matching invocation",
                    );
                }
                let mut writes = row.lhs.clone();
                if matches!(row.op.as_str(), "lift.oracle_call" | "lift.oracle_uncall") {
                    writes.extend([row.operands[3].clone(), row.operands[4].clone()]);
                }
                if row.op == "lift.perm_call" {
                    writes.extend(list(&row.operands[1])?);
                }
                if writes.iter().any(|w| ins.contains(w)) {
                    return err(
                        "§5.5",
                        "oracle_uncall input was written after the computing call",
                    );
                }
                if !memory.is_empty()
                    && (row.op.starts_with("lift.store.") || row.op == "lift.call")
                {
                    return err("§5.5", "oracle_uncall memory version may have advanced");
                }
                if point == 0 || predecessors[point].is_empty() {
                    return err(
                        "§5.5",
                        "oracle_uncall lacks a matching invocation on an incoming path",
                    );
                }
                work.extend(&predecessors[point]);
            }
            if !found {
                return err("§5.5", "oracle_uncall lacks a matching invocation");
            }
        }
        Ok(())
    }
}
````

## `src/classical.rs` (1121 lines)

````rust
//! CC/R dynamic SSA, retained history and reversible device models (§7).
use crate::{
    err,
    object::{is_binop, is_div, list, mask, parse_bits},
    oracle::{binop, compare, divide, signed, Memory},
    registers::RegisterUndo,
    validation::normalize_call,
    Argument, Budget, Error, Instruction, Object, OracleInput, QuantumBindings, QuantumRegion,
    QuantumRegisters, Result, Type,
};
use std::collections::{BTreeMap, VecDeque};

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ClassicalValue {
    Int(u16, u128),
    Ptr(u128),
    F64(u64),
    Token(Budget),
    Qreg(u64),
}
impl ClassicalValue {
    pub fn int(width: u16, value: u128) -> Result<Self> {
        if !(1..=128).contains(&width) || value & !mask(width) != 0 {
            return err("§3.3", "classical value does not fit integer width");
        }
        Ok(Self::Int(width, value))
    }
    fn bits(&self) -> Result<u128> {
        match self {
            Self::Int(_, v) | Self::Ptr(v) => Ok(*v),
            _ => err("§3.3", "expected classical bit-vector value"),
        }
    }
    fn width(&self, ptr: u16) -> Result<u16> {
        match self {
            Self::Int(w, _) => Ok(*w),
            Self::Ptr(_) => Ok(ptr),
            _ => err("§3.3", "value has no integer width"),
        }
    }
    fn matches(&self, t: &Type, ptr: u16) -> bool {
        match (self, t) {
            (Self::Int(w, v), Type::Int(n)) => w == n && *v & !mask(*w) == 0,
            (Self::Ptr(v), Type::Ptr) => *v & !mask(ptr) == 0,
            (Self::F64(v), Type::F64) => f64::from_bits(*v).is_finite(),
            (Self::Token(_), Type::Token) | (Self::Qreg(_), Type::Qreg(_)) => true,
            _ => false,
        }
    }
}
#[derive(Clone, Debug, PartialEq, Eq)]
struct Activation {
    id: u64,
    function: String,
    block: usize,
    ip: usize,
    bindings: Vec<String>,
    segment: Option<usize>,
}
type Key = (u64, String);
#[derive(Clone, Debug, PartialEq, Eq, Default)]
struct Devices {
    console: Vec<u8>,
    clock: u64,
    entropy_position: usize,
    blocks: BTreeMap<u128, Vec<u8>>,
    tape: Vec<(String, String, Vec<u128>)>,
}
#[derive(Clone, Debug, PartialEq)]
pub struct ClassicalSnapshot {
    instances: BTreeMap<Key, Vec<ClassicalValue>>,
    memory: Memory,
    devices: Devices,
    control: Vec<Activation>,
    next_id: u64,
    fault: Option<u128>,
    finished: Option<Vec<ClassicalValue>>,
    pending: Option<HostRequest>,
    quantum: QuantumRegisters,
}
#[derive(Clone, Debug)]
struct Undo {
    control: Vec<Activation>,
    next_id: u64,
    definitions: Vec<Key>,
    bytes: Vec<(u128, u8)>,
    allocation: Option<(u128, usize)>,
    free: Option<(usize, bool)>,
    device: Option<DeviceUndo>,
    tape: bool,
    fault: Option<u128>,
    finished: Option<Vec<ClassicalValue>>,
    pending: Option<HostRequest>,
    registers: Vec<RegisterUndo>,
    region: Option<RegionRecord>,
}
#[derive(Clone, Debug)]
struct RegionRecord {
    name: String,
    bindings: QuantumBindings,
    budget: Option<Budget>,
    adjoint: bool,
    controls: Vec<u64>,
    wire_next: u64,
}
#[derive(Clone, Debug)]
enum DeviceUndo {
    Console(usize),
    Clock(u64),
    Entropy(usize),
    Block(u128, Option<Vec<u8>>),
}
#[derive(Clone, Debug)]
struct HistoryFrame {
    undo: Undo,
    reversed: bool,
    marker: bool,
    pure: bool,
    irreversible: bool,
    host: Option<HostExchange>,
    measurement: Option<(u64, Vec<bool>)>,
}
#[derive(Clone, Debug)]
struct Segment {
    start: usize,
    end: Option<usize>,
    callee: String,
    args: Vec<ClassicalValue>,
    results: Vec<ClassicalValue>,
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ClassicalOutcome {
    pub values: Vec<ClassicalValue>,
    pub fault: Option<u128>,
    pub trapped: bool,
    pub steps: u64,
    pub request: Option<HostRequest>,
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct HostRequest {
    pub service: String,
    pub payload: Vec<u8>,
    pub address: u128,
    pub capacity: u128,
    result_name: String,
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct HostExchange {
    pub request: HostRequest,
    pub reply: Vec<u8>,
}
pub struct ClassicalMachine<'a> {
    object: &'a Object,
    state: ClassicalSnapshot,
    history: Vec<HistoryFrame>,
    segments: Vec<Segment>,
    entropy: Vec<u8>,
    initial: ClassicalSnapshot,
    measurement_draws: VecDeque<f64>,
    measurement_rng: [u64; 4],
    idle_registers: Vec<u64>,
}

impl<'a> ClassicalMachine<'a> {
    pub fn new(
        object: &'a Object,
        entry: &str,
        args: &[ClassicalValue],
        entropy: &[u8],
    ) -> Result<Self> {
        Self::construct(object, entry, args, entropy, QuantumRegisters::new())
    }
    fn construct(
        object: &'a Object,
        entry: &str,
        args: &[ClassicalValue],
        entropy: &[u8],
        registers: QuantumRegisters,
    ) -> Result<Self> {
        object.ensure_linked()?;
        let f = object
            .functions
            .get(entry)
            .filter(|f| matches!(f.kind.as_str(), "cc" | "r"))
            .ok_or_else(|| Error("§3.4: classical entry not found".into()))?;
        if args.len() != f.params[0].len()
            || args
                .iter()
                .zip(&f.params[0])
                .any(|(a, p)| !a.matches(&p.ty, object.ptr_width))
        {
            return err("§10", "classical entry argument type/count mismatch");
        }
        for (p, a) in f.params[0].iter().zip(args) {
            if let (Type::Qreg(n), ClassicalValue::Qreg(id)) = (&p.ty, a) {
                if registers.bundle(*id)?.len() as u64 != *n {
                    return err("§10", "E_ARG: qreg argument width differs");
                }
            }
        }
        let instances = f.params[0]
            .iter()
            .zip(args)
            .map(|(p, v)| ((0, p.name.clone()), vec![v.clone()]))
            .collect();
        let mut devices = Devices::default();
        if let Some(l) = object.section("layout") {
            if let Some(image) = l.object()?.get("block_image") {
                let data = &object.data[image.string()?];
                if !data.len().is_multiple_of(512) {
                    return err("§7.3", "block image must have complete 512-byte sectors");
                }
                for (i, sector) in data.as_chunks::<512>().0.iter().enumerate() {
                    devices.blocks.insert(i as u128, sector.to_vec());
                }
            }
        }
        let state = ClassicalSnapshot {
            instances,
            memory: Memory::initial(object, f, &OracleInput::default())?,
            devices,
            control: vec![Activation {
                id: 0,
                function: entry.into(),
                block: 0,
                ip: 0,
                bindings: Vec::new(),
                segment: None,
            }],
            next_id: 1,
            fault: None,
            finished: None,
            pending: None,
            quantum: registers,
        };
        Ok(Self {
            object,
            state: state.clone(),
            history: Vec::new(),
            segments: Vec::new(),
            entropy: entropy.into(),
            initial: state,
            measurement_draws: VecDeque::new(),
            measurement_rng: [1, 2, 3, 4],
            idle_registers: Vec::new(),
        })
    }
    pub fn with_quantum_registers(
        object: &'a Object,
        entry: &str,
        args: &[ClassicalValue],
        entropy: &[u8],
        registers: QuantumRegisters,
    ) -> Result<Self> {
        Self::construct(object, entry, args, entropy, registers)
    }
    pub fn quantum_registers(&self) -> &QuantumRegisters {
        &self.state.quantum
    }
    pub fn designate_idle_registers(&mut self,ids:&[u64])->Result<()>{if !self.history.is_empty(){return err("§9.4","idle set must be designated before execution");}let mut wires=std::collections::BTreeSet::new();for id in ids{for wire in self.state.quantum.idle_bundle(*id)?{if !wires.insert(*wire){return err("§9.4","designated idle registers overlap");}}}self.idle_registers=ids.to_vec();Ok(())}
    pub fn push_measurement_draw(&mut self, draw: f64) -> Result<()> {
        if !(0.0..1.0).contains(&draw) {
            return err("§14.2", "measurement draw must be finite in [0,1)");
        }
        self.measurement_draws.push_back(draw);
        Ok(())
    }
    pub fn measurements(&self) -> Vec<(u64, Vec<bool>)> {
        self.history
            .iter()
            .filter_map(|h| h.measurement.clone())
            .collect()
    }
    fn measurement_draw(&mut self) -> f64 {
        if let Some(draw) = self.measurement_draws.pop_front() {
            return draw;
        }
        let s = &mut self.measurement_rng;
        let result = s[1].wrapping_mul(5).rotate_left(7).wrapping_mul(9);
        let t = s[1] << 17;
        s[2] ^= s[0];
        s[3] ^= s[1];
        s[1] ^= s[2];
        s[0] ^= s[3];
        s[2] ^= t;
        s[3] = s[3].rotate_left(45);
        ((result >> 11) as f64) * (1.0 / 9_007_199_254_740_992.0)
    }
    pub fn snapshot(&self) -> ClassicalSnapshot {
        self.state.clone()
    }
    pub fn clock(&self) -> u64 {
        self.state.devices.clock
    }
    pub fn console(&self) -> &[u8] {
        &self.state.devices.console
    }
    pub fn effect_tape_len(&self) -> usize {
        self.state.devices.tape.len()
    }
    pub fn memory_bytes(&self, address: u128, len: usize) -> Result<Vec<u8>> {
        if !self.state.memory.valid(address, len as u128) {
            return err("§7.1", "memory query outside live allocation");
        }
        Ok((0..len)
            .map(|n| self.state.memory.byte(address + n as u128))
            .collect())
    }
    pub fn host_transcript(&self) -> Vec<HostExchange> {
        self.history.iter().filter_map(|h| h.host.clone()).collect()
    }
    pub fn reply(&mut self, payload: &[u8]) -> Result<()> {
        let request = self
            .state
            .pending
            .clone()
            .ok_or_else(|| Error("§10: E_INVALID_STATE: no host request".into()))?;
        if payload.len() as u128 & !mask(self.object.ptr_width) != 0 {
            return err("§10", "E_ARG: reply length exceeds ptr_width");
        }
        let count = (payload.len() as u128).min(request.capacity) as usize;
        let mut undo = self
            .history
            .last()
            .ok_or_else(|| Error("§10: missing host frame".into()))?
            .undo
            .clone();
        self.save_bytes(request.address, count, &mut undo);
        for (n, b) in payload[..count].iter().enumerate() {
            self.state.memory.set_byte(request.address + n as u128, *b);
        }
        self.define(
            &request.result_name,
            ClassicalValue::Int(self.object.ptr_width, payload.len() as u128),
            &mut undo,
        )?;
        let frame = self.history.last_mut().expect("retained host frame");
        frame.undo = undo;
        frame
            .host
            .as_mut()
            .ok_or_else(|| Error("§10: missing retained host request".into()))?
            .reply = payload.to_vec();
        self.state.pending = None;
        Ok(())
    }
    pub fn run(&mut self, max_steps: u64) -> Result<ClassicalOutcome> {
        let mut steps = 0;
        while self.state.fault.is_none()
            && self.state.finished.is_none()
            && self.state.pending.is_none()
        {
            if steps == max_steps {
                return err(
                    "§3.4",
                    "reference execution fuel exhausted; CC/R has no ISA step budget",
                );
            }
            self.step()?;
            steps += 1;
        }
        Ok(ClassicalOutcome {
            values: self.state.finished.clone().unwrap_or_default(),
            fault: self.state.fault,
            trapped: self.state.fault.is_some()
                && self
                    .state
                    .control
                    .last()
                    .is_some_and(|a| self.object.functions[&a.function].kind == "cc"),
            steps,
            request: self.state.pending.clone(),
        })
    }
    pub fn reverse(&mut self) -> Result<()> {
        if self.state.pending.is_some() {
            return err("§10", "E_INVALID_STATE: host request is pending");
        }
        if self.history.iter().any(|f| f.irreversible) {
            return err(
                "§10",
                "E_NOT_REVERSIBLE: measurement or unverified release in history",
            );
        }
        for n in (0..self.history.len()).rev() {
            self.undo_frame(n)?;
        }
        self.history.clear();
        self.segments.clear();
        if self.state != self.initial {
            return err("§7.4", "whole-run reversal failed to restore entry tuple");
        }
        Ok(())
    }
    fn read(&self, name: &str) -> Result<ClassicalValue> {
        let id = self
            .state
            .control
            .last()
            .ok_or_else(|| Error("§3.4: empty activation stack".into()))?
            .id;
        self.state
            .instances
            .get(&(id, name.into()))
            .and_then(|v| v.last())
            .cloned()
            .ok_or_else(|| Error(format!("§7.4: instance {name} no longer exists")))
    }
    fn bits(&self, name: &str) -> Result<u128> {
        self.read(name)?.bits()
    }
    fn qreg(&self, name: &str) -> Result<u64> {
        match self.read(name)? {
            ClassicalValue::Qreg(id) => {
                self.state.quantum.bundle(id)?;
                Ok(id)
            }
            _ => err("§3.3", "region operand is not a qreg"),
        }
    }
    fn region_record(&self, instruction: &Instruction) -> Result<(RegionRecord, Vec<u64>)> {
        let call = normalize_call(instruction)?;
        let a = &call.instruction.operands;
        let name = a[0].trim_start_matches('@');
        let callee = self
            .object
            .functions
            .get(name)
            .ok_or_else(|| Error(format!("§9.3: unresolved region @{name}")))?;
        let mut bindings = QuantumBindings::default();
        let mut ids = Vec::new();
        let mut controls = Vec::new();
        if let Some(control) = call.control {
            let id = self.qreg(&control)?;
            let wires = self.state.quantum.bundle(id)?;
            if wires.len() != 1 {
                return err("§3.3", "ctl requires qreg[1]");
            }
            controls.push(wires[0]);
            ids.push(id);
        }
        let oracle = call.instruction.op == "oracle_call";
        let (groups, memory, args, budget) = if oracle {
            let token = match self.read(&a[1])? {
                ClassicalValue::Token(b) => b,
                _ => return err("§3.3", "oracle_call needs a budget token"),
            };
            (
                vec![
                    (0, list(&a[2])?),
                    (1, vec![a[3].clone()]),
                    (2, vec![a[4].clone()]),
                ],
                (3, list(&a[5])?),
                (4, list(&a[6])?),
                Some(token),
            )
        } else {
            (
                vec![(0, list(&a[1])?), (1, list(&a[2])?)],
                (2, list(&a[3])?),
                (3, list(&a[4])?),
                None,
            )
        };
        for (group, names) in groups {
            for (p, n) in callee.params[group].iter().zip(names) {
                let id = self.qreg(&n)?;
                let wires = self.state.quantum.bundle(id)?.to_vec();
                bindings.bundles.insert(p.name.clone(), wires);
                if !ids.contains(&id) {
                    ids.push(id);
                }
            }
        }
        for (p, n) in callee.params[memory.0].iter().zip(memory.1) {
            let id = self.qreg(&n)?;
            let wires = self.state.quantum.bundle(id)?;
            let Type::Region(a, w) = p.ty else {
                unreachable!("validated region")
            };
            if wires.len() as u128 != (1u128 << a) * (w as u128) {
                return err("§3.3", "qreg does not fill region dimensions");
            }
            bindings.regions.insert(
                p.name.clone(),
                QuantumRegion {
                    address_width: a,
                    cell_width: w,
                    cells: wires.chunks_exact(w as usize).map(|c| c.to_vec()).collect(),
                },
            );
            if !ids.contains(&id) {
                ids.push(id);
            }
        }
        for (p, n) in callee.params[args.0].iter().zip(args.1) {
            let arg = match self.read(&n)? {
                ClassicalValue::Int(_, v) | ClassicalValue::Ptr(v) => Argument::Bits(v),
                ClassicalValue::F64(bits) => Argument::Float(f64::from_bits(bits)),
                ClassicalValue::Token(b) => Argument::Token(b),
                _ => return err("§3.3", "qreg is not a classical region argument"),
            };
            bindings.args.insert(p.name.clone(), arg);
        }
        let used=ids.iter().map(|id|self.state.quantum.bundle(*id)).collect::<Result<Vec<_>>>()?.into_iter().flatten().copied().collect::<std::collections::BTreeSet<_>>();
        for id in &self.idle_registers{let wires=self.state.quantum.idle_bundle(*id)?.to_vec();if wires.iter().any(|w|used.contains(w)){return err("§9.4","designated idle wires overlap the region interface or control");}bindings.borrowed.push(wires);}
        Ok((
            RegionRecord {
                name: name.into(),
                bindings,
                budget,
                adjoint: call.adjoint,
                controls,
                wire_next: self.state.quantum.state.next_wire_id(),
            },
            ids,
        ))
    }
    fn execute_region(&mut self, record: &RegionRecord, inverse: bool) -> Result<()> {
        let callee = &self.object.functions[&record.name];
        let mut state = self.state.quantum.state.clone();
        if let Some(budget) = record.budget {
            let ins = callee.params[0]
                .iter()
                .map(|p| record.bindings.bundles[&p.name].clone())
                .collect::<Vec<_>>();
            let target = &record.bindings.bundles[&callee.params[1][0].name];
            let fault = &record.bindings.bundles[&callee.params[2][0].name];
            let args = callee.params[4]
                .iter()
                .map(|p| record.bindings.args[&p.name].clone())
                .collect::<Vec<_>>();
            self.object.oracle_quantum(
                callee,
                &mut state,
                &ins,
                target,
                fault,
                &record.bindings.regions,
                &args,
                budget,
                &record
                    .controls
                    .iter()
                    .map(|w| (*w, true))
                    .collect::<Vec<_>>(),
            )?;
        } else {
            self.object.execute_action(
                &record.name,
                &mut state,
                &record.bindings,
                record.adjoint ^ inverse,
                &record.controls,
            )?;
        }
        self.state.quantum.state = state;
        Ok(())
    }
    fn define(&mut self, name: &str, value: ClassicalValue, undo: &mut Undo) -> Result<()> {
        let id = self
            .state
            .control
            .last()
            .ok_or_else(|| Error("§3.4: define without activation".into()))?
            .id;
        self.define_at(id, name, value, undo);
        Ok(())
    }
    fn define_at(&mut self, id: u64, name: &str, value: ClassicalValue, undo: &mut Undo) {
        let key = (id, name.into());
        self.state
            .instances
            .entry(key.clone())
            .or_default()
            .push(value);
        undo.definitions.push(key);
    }
    fn save_bytes(&self, p: u128, len: usize, undo: &mut Undo) {
        for n in 0..len {
            undo.bytes
                .push((p + n as u128, self.state.memory.byte(p + n as u128)));
        }
    }
    fn undo_record(&mut self, undo: Undo) -> Result<()> {
        for record in undo.registers.into_iter().rev() {
            self.state.quantum.undo(record)?;
        }
        if let Some(record) = undo.region {
            self.execute_region(&record, true)?;
            self.state
                .quantum
                .state
                .restore_next_wire_id(record.wire_next)?;
        }
        for key in undo.definitions.into_iter().rev() {
            let stack = self
                .state
                .instances
                .get_mut(&key)
                .ok_or_else(|| Error("§7.4: missing retained dynamic instance".into()))?;
            stack
                .pop()
                .ok_or_else(|| Error("§7.4: empty retained dynamic instance".into()))?;
            if stack.is_empty() {
                self.state.instances.remove(&key);
            }
        }
        for (p, b) in undo.bytes.into_iter().rev() {
            self.state.memory.set_byte(p, b);
        }
        if let Some((used, len)) = undo.allocation {
            self.state.memory.heap_used = used;
            self.state.memory.allocations.truncate(len);
        }
        if let Some((n, live)) = undo.free {
            self.state.memory.allocations[n].live = live;
        }
        if undo.tape {
            self.state
                .devices
                .tape
                .pop()
                .ok_or_else(|| Error("§7.3: empty effect tape on reversal".into()))?;
        }
        if let Some(d) = undo.device {
            match d {
                DeviceUndo::Console(n) => self.state.devices.console.truncate(n),
                DeviceUndo::Clock(c) => self.state.devices.clock = c,
                DeviceUndo::Entropy(p) => self.state.devices.entropy_position = p,
                DeviceUndo::Block(n, Some(v)) => {
                    self.state.devices.blocks.insert(n, v);
                }
                DeviceUndo::Block(n, None) => {
                    self.state.devices.blocks.remove(&n);
                }
            }
        }
        self.state.control = undo.control;
        self.state.next_id = undo.next_id;
        self.state.fault = undo.fault;
        self.state.finished = undo.finished;
        self.state.pending = undo.pending;
        Ok(())
    }
    fn undo_frame(&mut self, n: usize) -> Result<()> {
        if self.history[n].reversed || self.history[n].marker {
            return Ok(());
        }
        let undo = self.history[n].undo.clone();
        self.undo_record(undo)?;
        self.history[n].reversed = true;
        Ok(())
    }
    fn effect(&mut self, op: &str, args: &[String], undo: &mut Undo) -> Result<Option<u128>> {
        let Some((dev, operation)) = op.split_once('.') else {
            return Ok(Some(8));
        };
        let values = args
            .iter()
            .map(|s| self.bits(s))
            .collect::<Result<Vec<_>>>()?;
        let arity = match (dev, operation) {
            ("console", "write") | ("entropy", "read") | ("block", "read" | "write") => 2,
            ("clock", "read") => 1,
            _ => return Ok(Some(8)),
        };
        if values.len() != arity {
            return err("§7.3", "device operation arity mismatch");
        }
        let (p, len) = match dev {
            "clock" => (values[0], 8),
            "block" => (values[1], 512),
            _ => (values[0], values[1]),
        };
        if !self.state.memory.valid(p, len) {
            return Ok(Some(7));
        }
        let len = usize::try_from(len)
            .map_err(|_| Error("§7.3: device length exceeds host address space".into()))?;
        if dev == "entropy"
            && self
                .state
                .devices
                .entropy_position
                .checked_add(len)
                .is_none_or(|end| end > self.entropy.len())
        {
            return Ok(Some(10));
        }
        match (dev, operation) {
            ("console", "write") => {
                undo.device = Some(DeviceUndo::Console(self.state.devices.console.len()));
                let bytes: Vec<_> = (0..len)
                    .map(|i| self.state.memory.byte(p + i as u128))
                    .collect();
                self.state.devices.console.extend(bytes);
            }
            ("clock", "read") => {
                self.save_bytes(p, 8, undo);
                let c = self.state.devices.clock;
                undo.device = Some(DeviceUndo::Clock(c));
                self.state.memory.store(p, 64, c as u128);
                self.state.devices.clock = c.wrapping_add(1);
            }
            ("entropy", "read") => {
                self.save_bytes(p, len, undo);
                let start = self.state.devices.entropy_position;
                undo.device = Some(DeviceUndo::Entropy(start));
                for n in 0..len {
                    self.state
                        .memory
                        .set_byte(p + n as u128, self.entropy[start + n]);
                }
                self.state.devices.entropy_position += len;
            }
            ("block", "read") => {
                self.save_bytes(p, 512, undo);
                let bytes = self
                    .state
                    .devices
                    .blocks
                    .get(&values[0])
                    .cloned()
                    .unwrap_or_else(|| vec![0; 512]);
                for (n, b) in bytes.into_iter().enumerate() {
                    self.state.memory.set_byte(p + n as u128, b);
                }
            }
            ("block", "write") => {
                let sector = values[0];
                let old = self.state.devices.blocks.get(&sector).cloned();
                undo.device = Some(DeviceUndo::Block(sector, old));
                let bytes = (0..512).map(|n| self.state.memory.byte(p + n)).collect();
                self.state.devices.blocks.insert(sector, bytes);
            }
            _ => unreachable!("device operation validated"),
        }
        self.state
            .devices
            .tape
            .push((dev.into(), operation.into(), values));
        undo.tape = true;
        Ok(None)
    }
    fn step(&mut self) -> Result<()> {
        let object = self.object;
        let current = self
            .state
            .control
            .last()
            .ok_or_else(|| Error("§3.4: no active function".into()))?
            .clone();
        let f = &object.functions[&current.function];
        let i = f.blocks[current.block]
            .instructions
            .get(current.ip)
            .ok_or_else(|| Error("§3.4: fell off classical block".into()))?
            .clone();
        let op = i.op.as_str();
        let a = &i.operands;
        let mut undo = Undo {
            control: self.state.control.clone(),
            next_id: self.state.next_id,
            definitions: Vec::new(),
            bytes: Vec::new(),
            allocation: None,
            free: None,
            device: None,
            tape: false,
            fault: self.state.fault,
            finished: self.state.finished.clone(),
            pending: self.state.pending.clone(),
            registers: Vec::new(),
            region: None,
        };
        self.state.control.last_mut().expect("activation").ip += 1;
        let mut fault = None;
        let mut output = None;
        let mut marker = false;
        let mut measurement = None;
        let pure = op.starts_with("const.")
            || is_binop(op)
            || is_div(op)
            || op.starts_with("icmp.")
            || op == "select"
            || ["zext.", "sext.", "trunc.", "ptrtoint.", "load."]
                .iter()
                .any(|p| op.starts_with(p))
            || op == "inttoptr"
            || op == "br";
        let execute = (|| -> Result<()> {
            if let Some(t) = op.strip_prefix("const.") {
                let Type::Int(w) = Type::parse(t)? else {
                    return err("§4.8", "const type");
                };
                output = Some(ClassicalValue::Int(w, parse_bits(&a[0], w)?));
            } else if is_binop(op) || is_div(op) {
                let av = self.read(&a[0])?;
                let w = av.width(object.ptr_width)?;
                let left = av.bits()?;
                let right = self.bits(&a[1])?;
                let value = if is_binop(op) {
                    Some(binop(op, left, right, w))
                } else {
                    match divide(op, left, right, w) {
                        Ok(v) => Some(v),
                        Err(c) => {
                            fault = Some(c);
                            None
                        }
                    }
                };
                output = value.map(|v| ClassicalValue::Int(w, v));
            } else if let Some(pred) = op.strip_prefix("icmp.") {
                let av = self.read(&a[0])?;
                output = Some(ClassicalValue::Int(
                    1,
                    compare(
                        pred,
                        av.bits()?,
                        self.bits(&a[1])?,
                        av.width(object.ptr_width)?,
                    ) as u128,
                ));
            } else if let Some((cast, t)) = op
                .split_once('.')
                .filter(|(c, _)| ["zext", "sext", "trunc", "ptrtoint"].contains(c))
            {
                let Type::Int(w) = Type::parse(t)? else {
                    return err("§4.8", "cast target type");
                };
                let from = self.read(&a[0])?;
                let value = if cast == "sext" {
                    signed(from.bits()?, from.width(object.ptr_width)?) as u128
                } else {
                    from.bits()?
                };
                output = Some(ClassicalValue::Int(w, value & mask(w)));
            } else if let Some(t) = op.strip_prefix("load.") {
                let w = Type::parse(t)?.width(object.ptr_width)?;
                let p = self.bits(&a[0])?;
                if !self.state.memory.valid(p, (w / 8) as u128) {
                    fault = Some(7);
                } else {
                    output = Some(ClassicalValue::Int(w, self.state.memory.load(p, w)));
                }
            } else if let Some(t) = op.strip_prefix("store.") {
                let w = Type::parse(t)?.width(object.ptr_width)?;
                let p = self.bits(&a[0])?;
                let v = self.bits(&a[1])?;
                if !self.state.memory.valid(p, (w / 8) as u128) {
                    fault = Some(7);
                } else {
                    self.save_bytes(p, (w / 8) as usize, &mut undo);
                    self.state.memory.store(p, w, v);
                }
            } else {
                match op {
                    "select" => {
                        output =
                            Some(self.read(if self.bits(&a[0])? != 0 { &a[1] } else { &a[2] })?)
                    }
                    "inttoptr" => {
                        output = Some(ClassicalValue::Ptr(
                            self.bits(&a[0])? & mask(object.ptr_width),
                        ))
                    }
                    "alloc" => {
                        let n = self.bits(&a[0])?;
                        let b = object.default_budget(0)?;
                        if self.state.memory.allocation_fails(n, b) {
                            fault = Some(2);
                        } else {
                            undo.allocation = Some((
                                self.state.memory.heap_used,
                                self.state.memory.allocations.len(),
                            ));
                            output = Some(ClassicalValue::Ptr(self.state.memory.allocate(n)));
                        }
                    }
                    "free" => {
                        let p = self.bits(&a[0])?;
                        if let Some(n) = self
                            .state
                            .memory
                            .allocations
                            .iter()
                            .position(|e| e.base == p && e.live && !e.pinned)
                        {
                            undo.free = Some((n, true));
                            self.state.memory.allocations[n].live = false;
                        } else {
                            fault = Some(7);
                        }
                    }
                    "br" => {
                        let target = if a.len() == 1 {
                            &a[0]
                        } else if self.bits(&a[0])? != 0 {
                            &a[1]
                        } else {
                            &a[2]
                        };
                        let (n, args) = target
                            .trim_start_matches('^')
                            .split_once('(')
                            .ok_or_else(|| Error("§4.1: malformed branch".into()))?;
                        let values = list(&format!("({args}"))?
                            .iter()
                            .map(|n| self.read(n))
                            .collect::<Result<Vec<_>>>()?;
                        let block = f
                            .blocks
                            .iter()
                            .position(|b| b.name == n)
                            .expect("validated branch target");
                        for (p, v) in f.blocks[block].params.iter().zip(values) {
                            self.define(&p.name, v, &mut undo)?;
                        }
                        let active = self.state.control.last_mut().expect("activation");
                        active.block = block;
                        active.ip = 0;
                    }
                    "call" => {
                        let n = a[0].trim_start_matches('@');
                        let callee = &object.functions[n];
                        let args = if a.len() == 2 && a[1].starts_with('(') {
                            list(&a[1])?
                        } else {
                            a[1..].to_vec()
                        };
                        let values = args
                            .iter()
                            .map(|n| self.read(n))
                            .collect::<Result<Vec<_>>>()?;
                        let segment = self.segments.len();
                        self.segments.push(Segment {
                            start: self.history.len(),
                            end: None,
                            callee: n.into(),
                            args: values.clone(),
                            results: Vec::new(),
                        });
                        let id = self.state.next_id;
                        self.state.next_id += 1;
                        self.state.control.push(Activation {
                            id,
                            function: n.into(),
                            block: 0,
                            ip: 0,
                            bindings: i.lhs.clone(),
                            segment: Some(segment),
                        });
                        for (p, v) in callee.params[0].iter().zip(values) {
                            self.define(&p.name, v, &mut undo)?;
                        }
                    }
                    "ret" => {
                        let values = a.iter().map(|n| self.read(n)).collect::<Result<Vec<_>>>()?;
                        let active = self.state.control.pop().expect("return activation");
                        if let Some(segment) = active.segment {
                            self.segments[segment].end = Some(self.history.len());
                            self.segments[segment].results = values.clone();
                        }
                        if self.state.control.is_empty() {
                            self.state.finished = Some(values);
                        } else {
                            for (n, v) in active.bindings.iter().zip(values) {
                                self.define(n, v, &mut undo)?;
                            }
                        }
                    }
                    "uncall" => {
                        let name = a[0].trim_start_matches('@');
                        let args = list(&a[1])?
                            .iter()
                            .map(|n| self.read(n))
                            .collect::<Result<Vec<_>>>()?;
                        let results = list(&a[2])?
                            .iter()
                            .map(|n| self.read(n))
                            .collect::<Result<Vec<_>>>()?;
                        let segment = self
                            .segments
                            .iter()
                            .filter(|s| s.end.is_some() && !self.history[s.start].reversed)
                            .max_by_key(|s| s.end)
                            .cloned();
                        if let Some(s) = segment {
                            let end = s.end.expect("completed segment");
                            if s.callee != name
                                || s.args != args
                                || s.results != results
                                || self.history[end + 1..].iter().any(|f| !f.pure)
                                || self.history[s.start..=end].iter().any(|f| f.irreversible)
                            {
                                fault = Some(4);
                            } else {
                                let control = self.state.control.clone();
                                let next_id = self.state.next_id;
                                for n in (s.start..=end).rev() {
                                    self.undo_frame(n)?;
                                }
                                self.state.control = control;
                                self.state.next_id = next_id;
                                marker = true;
                            }
                        } else {
                            fault = Some(4);
                        }
                    }
                    "effect" => fault = self.effect(&a[0], &a[1..], &mut undo)?,
                    "trap" => fault = Some(4),
                    "hostcall" => {
                        let address = self.bits(&a[1])?;
                        let capacity = self.bits(&a[2])?;
                        if !self.state.memory.valid(address, capacity) {
                            fault = Some(7);
                        } else {
                            let count = usize::try_from(capacity).map_err(|_| {
                                Error("§10: request exceeds host address space".into())
                            })?;
                            let payload = self.memory_bytes(address, count)?;
                            self.state.pending = Some(HostRequest {
                                service: a[0].clone(),
                                payload,
                                address,
                                capacity,
                                result_name: i.lhs[0].clone(),
                            });
                        }
                    }
                    "qreg.new" => {
                        let n = a[1]
                            .parse::<usize>()
                            .map_err(|_| Error("§3.3: qreg size exceeds host storage".into()))?;
                        let (id, record) = self.state.quantum.allocate_recorded(n)?;
                        undo.registers.push(record);
                        output = Some(ClassicalValue::Qreg(id));
                    }
                    "qreg.free" => {
                        let id = self.qreg(&a[0])?;
                        undo.registers.push(self.state.quantum.free_recorded(id)?);
                    }
                    "qreg.slice" => {
                        let id = self.qreg(&a[0])?;
                        let lo = a[1]
                            .parse::<usize>()
                            .map_err(|_| Error("§3.3: slice offset exceeds host storage".into()))?;
                        let len = a[2]
                            .parse::<usize>()
                            .map_err(|_| Error("§3.3: slice length exceeds host storage".into()))?;
                        let (id, record) = self.state.quantum.slice_recorded(id, lo, len)?;
                        undo.registers.push(record);
                        output = Some(ClassicalValue::Qreg(id));
                    }
                    "qreg.concat" => {
                        let a = self.qreg(&a[0])?;
                        let b = self.qreg(&i.operands[1])?;
                        let (id, record) = self.state.quantum.concat_recorded(a, b)?;
                        undo.registers.push(record);
                        output = Some(ClassicalValue::Qreg(id));
                    }
                    "measure" => {
                        let id = self.qreg(&a[0])?;
                        let draw = self.measurement_draw();
                        let bits = self.state.quantum.measure(id, draw)?;
                        let value = bits
                            .iter()
                            .enumerate()
                            .fold(0, |v, (i, b)| v | ((*b as u128) << i));
                        output = Some(ClassicalValue::Int(bits.len() as u16, value));
                        measurement = Some((id, bits));
                    }
                    "oracle_call" | "action_call" | "adj" | "ctl" => {
                        let (record, ids) = self.region_record(&i)?;
                        let mut trial = self.state.quantum.clone();
                        trial.complete_call(&ids)?;
                        self.execute_region(&record, false)?;
                        undo.registers
                            .push(self.state.quantum.complete_call_recorded(&ids)?);
                        undo.region = Some(record);
                    }
                    _ => return err("§4.8", format!("unimplemented classical opcode {op}")),
                }
            }
            Ok(())
        })();
        if let Err(e) = execute {
            if e.0.starts_with("§7.4: instance")
                || e.0.starts_with("§3.3:")
                || e.0.contains("E_QREG_NOT_CLEAN")
            {
                fault = Some(4);
            } else {
                self.undo_record(undo)?;
                return Err(e);
            }
        }
        if let Some(code) = fault {
            self.state.fault = Some(code);
        } else if let Some(v) = output {
            self.define(&i.lhs[0], v, &mut undo)?;
        }
        self.history.push(HistoryFrame {
            undo,
            reversed: false,
            marker,
            pure: pure && fault.is_none(),
            irreversible: measurement.is_some(),
            measurement,
            host: self.state.pending.clone().map(|request| HostExchange {
                request,
                reply: Vec::new(),
            }),
        });
        Ok(())
    }
}
````

## `src/handle_validation.rs` (99 lines)

````rust
use crate::{err, object::list, validation::normalize_call, Error, Function, Object, Result, Type};
use std::collections::{BTreeMap, BTreeSet};
#[derive(Clone, Default, PartialEq, Eq, PartialOrd, Ord)]
struct Views {
    live: BTreeMap<String, String>,
    dead: BTreeSet<String>,
}
impl Object {
    pub(crate) fn validate_handle_views(
        &self,
        f: &Function,
        types: &BTreeMap<String, Type>,
    ) -> Result<()> {
        let mut work = vec![(0usize, Views::default())];
        let mut seen = BTreeSet::new();
        while let Some((block, mut views)) = work.pop() {
            if !seen.insert((block, views.clone())) {
                continue;
            }
            for instruction in &f.blocks[block].instructions {
                let op = instruction.op.as_str();
                let a = &instruction.operands;
                let region = matches!(op, "oracle_call" | "action_call" | "ctl" | "adj");
                let operands: Vec<String> = match op {
                    "qreg.new" => Vec::new(),
                    "qreg.slice" | "qreg.free" | "measure" => vec![a[0].clone()],
                    "qreg.concat" => a.clone(),
                    _ => {
                        let mut values = Vec::new();
                        for operand in a {
                            if operand.starts_with('(') {
                                values.extend(list(operand)?);
                            } else if operand.starts_with('^') {
                                if let Some((_, suffix)) = operand.split_once('(') {
                                    values.extend(list(&format!("({suffix}"))?);
                                }
                            } else {
                                values.push(operand.clone());
                            }
                        }
                        values
                    }
                };
                let handles: Vec<_> = operands
                    .into_iter()
                    .filter(|n| matches!(types.get(n), Some(Type::Qreg(_))))
                    .collect();
                for handle in &handles {
                    if views.live.values().any(|parent| parent == handle) {
                        return err("§3.3", format!("use of viewed parent {handle}"));
                    }
                    if views.dead.contains(handle) {
                        return err("§3.3", format!("view {handle} used after its region call"));
                    }
                    if views.live.contains_key(handle) && !region {
                        return err(
                            "§3.3",
                            format!("view {handle} may only be an operand of one region call"),
                        );
                    }
                }
                if op == "qreg.slice" {
                    let view = instruction.lhs[0].clone();
                    views.dead.remove(&view);
                    views.live.insert(view, a[0].clone());
                }
                if region {
                    normalize_call(instruction)?;
                    for handle in handles {
                        if views.live.remove(&handle).is_some() {
                            views.dead.insert(handle);
                        }
                    }
                }
                if op == "br" {
                    for branch in if a.len() == 1 { &a[..] } else { &a[1..] } {
                        let (label, _) = branch
                            .trim_start_matches('^')
                            .split_once('(')
                            .ok_or_else(|| Error("§3.4: malformed branch".into()))?;
                        let target = f
                            .blocks
                            .iter()
                            .position(|b| b.name == label)
                            .expect("validated block");
                        work.push((target, views.clone()));
                    }
                }
                if matches!(op, "ret" | "trap") && !views.live.is_empty() {
                    return err(
                        "§3.3",
                        "view is not consumed by exactly one region call on every exit path",
                    );
                }
            }
        }
        Ok(())
    }
}
````

## `src/identity.rs` (393 lines)

````rust
use crate::{err, json::Json, sha256_hex, Error, Object, Result};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Clone, Debug)]
pub struct Identity {
    pub interface_hashes: BTreeMap<String, String>,
    /// None denotes a symbol whose dependency closure still has an unresolved import.
    pub closure_hashes: BTreeMap<String, Option<String>>,
    pub envelopes: BTreeMap<String, String>,
    pub object_hash: String,
    pub scc_members: BTreeMap<String, Vec<String>>,
    pub scc_hashes: BTreeMap<String, String>,
}

/// Symbol reference tokens only: @ inside a quoted string is ordinary text.
fn references(line: &str) -> Vec<(usize, usize, &str)> {
    let bytes = line.as_bytes();
    let mut out = Vec::new();
    let mut i = 0;
    let mut quoted = false;
    while i < bytes.len() {
        if quoted {
            if bytes[i] == b'\\' {
                i += 2;
                continue;
            }
            if bytes[i] == b'"' {
                quoted = false;
            }
            i += 1;
            continue;
        }
        if bytes[i] == b'"' {
            quoted = true;
            i += 1;
            continue;
        }
        if bytes[i] == b'@'
            && i + 1 < bytes.len()
            && (bytes[i + 1].is_ascii_alphabetic() || bytes[i + 1] == b'_')
        {
            let start = i;
            i += 2;
            while i < bytes.len()
                && (bytes[i].is_ascii_alphanumeric() || matches!(bytes[i], b'_' | b'.'))
            {
                i += 1;
            }
            out.push((start, i, &line[start + 1..i]));
        } else {
            i += 1;
        }
    }
    out
}

impl Object {
    pub fn identity(&self) -> Result<Identity> {
        let symbols: BTreeMap<_, _> = self
            .symbols()?
            .values()
            .map(|s| Ok((s.get("name")?.string()?.to_string(), s)))
            .collect::<Result<_>>()?;
        let imports = self
            .section("imports")
            .map(Json::object)
            .transpose()?
            .cloned()
            .unwrap_or_default();
        let mut graph: BTreeMap<String, Vec<String>> = BTreeMap::new();
        for n in symbols.keys() {
            let mut deps = Vec::new();
            if let Some(f) = self.functions.get(n) {
                for line in f.lines.iter().skip(1) {
                    for (_, _, r) in references(line) {
                        if symbols.contains_key(r) || imports.contains_key(r) {
                            if !deps.iter().any(|s| s == r) {
                                deps.push(r.to_string());
                            }
                        } else if !(f.kind == "oracle" && f.params[3].iter().any(|p| p.name == r)) {
                            return err("§9.3", format!("unresolved undeclared reference @{r}"));
                        }
                    }
                }
            }
            graph.insert(n.clone(), deps);
        }
        // Tarjan emits dependency SCCs before their users.
        let components = components(&graph);
        let mut hashes = BTreeMap::new();
        let mut closure = BTreeMap::new();
        let mut envelopes = BTreeMap::new();
        let mut scc_members = BTreeMap::new();
        let mut scc_hashes = BTreeMap::new();
        for (n, im) in &imports {
            let mut seed = n.as_bytes().to_vec();
            seed.push(0);
            seed.extend_from_slice(im.get("signature")?.canonical().as_bytes());
            hashes.insert(n.clone(), sha256_hex(&seed));
            closure.insert(n.clone(), None);
        }
        for comp in components {
            let mut envs = Vec::new();
            let closed = comp.iter().all(|n| {
                graph[n]
                    .iter()
                    .all(|r| comp.contains(r) || closure.get(r).is_some_and(Option::is_some))
            });
            for n in &comp {
                let env = self.envelope(n, symbols[n], &comp, &hashes)?;
                envelopes.insert(n.clone(), env.clone());
                envs.push(env);
            }
            let recursive = comp.len() > 1 || graph[&comp[0]].contains(&comp[0]);
            let scc = sha256_hex(envs.concat().as_bytes());
            for (i, n) in comp.iter().enumerate() {
                scc_members.insert(n.clone(), comp.clone());
                scc_hashes.insert(n.clone(), scc.clone());
                let hash = if recursive {
                    sha256_hex(format!("{scc}:{i}").as_bytes())
                } else {
                    sha256_hex(envs[i].as_bytes())
                };
                closure.insert(n.clone(), if closed { Some(hash.clone()) } else { None });
                hashes.insert(n.clone(), hash);
            }
        }
        for n in imports.keys() {
            hashes.remove(n);
            closure.remove(n);
        }
        let mut canonical = String::new();
        let mut skip = false;
        let mut pending_blank = false;
        for line in self.text.lines() {
            if line.is_empty() {
                pending_blank = true;
                continue;
            }
            if let Some(s) = line.strip_prefix("section ") {
                skip = matches!(s, "schedule" | "certificate" | "coverage");
            }
            if !skip {
                if pending_blank {
                    canonical.push('\n');
                }
                canonical.push_str(line);
                canonical.push('\n');
            }
            pending_blank = false;
        }
        Ok(Identity {
            interface_hashes: hashes,
            closure_hashes: closure,
            envelopes,
            object_hash: sha256_hex(canonical.as_bytes()),
            scc_members,
            scc_hashes,
        })
    }
    pub fn check_hashes(&self) -> Result<()> {
        let identity = self.identity()?;
        for s in self.symbols()?.values() {
            let n = s.get("name")?.string()?;
            if s.get("interface_hash")?.string()? != identity.interface_hashes[n] {
                return err(
                    "§9.2",
                    format!(
                        "interface_hash mismatch for @{n}: expected {}",
                        identity.interface_hashes[n]
                    ),
                );
            }
        }
        Ok(())
    }
    fn envelope(
        &self,
        n: &str,
        symbol: &Json,
        comp: &[String],
        hashes: &BTreeMap<String, String>,
    ) -> Result<String> {
        let kind = symbol.get("kind")?.string()?;
        let mut body = if let Some(f) = self.functions.get(n) {
            f.lines.clone()
        } else {
            vec![format!("{n} {}", hex(&self.data[n]))]
        };
        let mut leaves = BTreeMap::new();
        let mut images = BTreeSet::new();
        if let Some(layout) = self.section("layout") {
            let all = layout_leaves(layout)?;
            match kind {
                "oracle" => {
                    for (k, v) in all {
                        if !k.starts_with("interface_regions.")
                            || k.starts_with(&format!("interface_regions.{n}."))
                        {
                            leaves.insert(k, v);
                        }
                    }
                }
                "cc" | "r" => leaves = all,
                "lproc" => {
                    for line in &body {
                        if let Some(g) = line.split_once("lift.addr @").map(|(_, g)| g) {
                            let k = format!("globals.{g}");
                            if let Some(v) = all.get(&k) {
                                leaves.insert(k, v.clone());
                            }
                        }
                    }
                }
                _ => {}
            }
            for v in leaves.values() {
                if let Json::Object(o) = v {
                    if let Some(img) = o.get("image") {
                        images.insert(img.string()?.to_string());
                    }
                }
            }
            if matches!(kind, "oracle" | "cc" | "r") {
                if let Some(img) = leaves.get("block_image") {
                    images.insert(img.string()?.to_string());
                }
            }
        }
        let mut refs = Vec::new();
        let replace = |line: &str, refs: &mut Vec<String>| -> String {
            let mut out = String::new();
            let mut previous = 0;
            for (start, end, r) in references(line) {
                out.push_str(&line[previous..start]);
                if let Some(index) = comp.iter().position(|n| n == r) {
                    out.push_str(&format!("@${index}"));
                } else if let Some(hash) = hashes.get(r) {
                    out.push('@');
                    out.push_str(hash);
                    if !refs.contains(hash) {
                        refs.push(hash.clone());
                    }
                } else {
                    out.push_str(&line[start..end]);
                }
                previous = end;
            }
            out.push_str(&line[previous..]);
            out
        };
        if self.functions.contains_key(n) {
            for line in body.iter_mut().skip(1) {
                *line = replace(line, &mut refs);
            }
        }
        let mut lines = vec![
            "isa=0.8".into(),
            format!("ptr_width={}", self.ptr_width),
            symbol.get("signature")?.canonical(),
        ];
        lines.extend(body);
        for img in images {
            let bytes = self
                .data
                .get(&img)
                .ok_or_else(|| Error(format!("§9.2: missing closure data {img}")))?;
            lines.push(replace(&format!("data {img} {}", hex(bytes)), &mut refs));
        }
        for (path, v) in leaves {
            lines.push(replace(
                &format!("layout {path} {}", v.canonical()),
                &mut refs,
            ));
        }
        if matches!(kind, "cc" | "r") {
            let mut used = BTreeSet::new();
            for i in self.functions[n].instructions() {
                if i.op == "effect" {
                    if let Some((dev, _)) = i.operands.first().and_then(|s| s.split_once('.')) {
                        used.insert(("models", dev.to_string()));
                    }
                }
                if i.op == "hostcall" {
                    if let Some(service) = i.operands.first() {
                        used.insert(("services", service.clone()));
                    }
                }
            }
            let devices = self.section("devices");
            let mut entries = BTreeMap::new();
            for (group, key) in used {
                let entry = devices
                    .map(|d| d.get(group).and_then(Json::object))
                    .transpose()?
                    .and_then(|entries| entries.get(&key));
                if let Some(value) = entry {
                    entries.insert(key, value);
                } else if group == "services"
                    || ["console", "clock", "entropy", "block"].contains(&key.as_str())
                {
                    return err("§9.1", format!("missing declared {group} entry {key}"));
                }
            }
            for (key, v) in entries {
                lines.push(format!("device {key} {}", v.canonical()));
            }
        }
        lines.extend(refs);
        Ok(lines.join("\n") + "\n")
    }
}
pub(crate) fn hex(bytes: &[u8]) -> String {
    bytes.iter().map(|b| format!("{b:02x}")).collect()
}
pub(crate) fn layout_leaves(layout: &Json) -> Result<BTreeMap<String, Json>> {
    let mut leaves = BTreeMap::new();
    for (k, v) in layout.object()? {
        match k.as_str() {
            "globals" => {
                for (n, e) in v.object()? {
                    leaves.insert(format!("globals.{n}"), e.clone());
                }
            }
            "interface_regions" => {
                for (n, rs) in v.object()? {
                    for (r, e) in rs.object()? {
                        leaves.insert(format!("interface_regions.{n}.{r}"), e.clone());
                    }
                }
            }
            _ => {
                leaves.insert(k.clone(), v.clone());
            }
        }
    }
    Ok(leaves)
}
fn components(graph: &BTreeMap<String, Vec<String>>) -> Vec<Vec<String>> {
    struct Tarjan<'a> {
        graph: &'a BTreeMap<String, Vec<String>>,
        index: BTreeMap<String, usize>,
        low: BTreeMap<String, usize>,
        stack: Vec<String>,
        on: BTreeSet<String>,
        result: Vec<Vec<String>>,
    }
    fn visit(t: &mut Tarjan<'_>, v: &str) {
        let index = t.index.len();
        t.index.insert(v.into(), index);
        t.low.insert(v.into(), index);
        t.stack.push(v.into());
        t.on.insert(v.into());
        for w in &t.graph[v] {
            if !t.graph.contains_key(w) {
                continue;
            }
            if !t.index.contains_key(w) {
                visit(t, w);
                t.low.insert(v.into(), t.low[v].min(t.low[w]));
            } else if t.on.contains(w) {
                t.low.insert(v.into(), t.low[v].min(t.index[w]));
            }
        }
        if t.low[v] == t.index[v] {
            let mut comp = Vec::new();
            loop {
                let w = t.stack.pop().expect("Tarjan stack");
                t.on.remove(&w);
                comp.push(w.clone());
                if w == v {
                    break;
                }
            }
            comp.sort();
            t.result.push(comp);
        }
    }
    let mut t = Tarjan {
        graph,
        index: BTreeMap::new(),
        low: BTreeMap::new(),
        stack: Vec::new(),
        on: BTreeSet::new(),
        result: Vec::new(),
    };
    for v in graph.keys() {
        if !t.index.contains_key(v) {
            visit(&mut t, v);
        }
    }
    t.result
}
````

## `src/json.rs` (384 lines)

````rust
//! Strict JSON and RFC 8785 canonical serialization, without dependencies.
use crate::{err, Result};
use std::collections::BTreeMap;

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Json {
    Null,
    Bool(bool),
    Number(String),
    String(String),
    Array(Vec<Json>),
    Object(BTreeMap<String, Json>),
}

impl Json {
    pub fn parse(text: &str) -> Result<Self> {
        let mut p = Parser {
            text,
            pos: 0,
            depth: 0,
        };
        let value = p.value()?;
        p.ws();
        if p.pos != text.len() {
            return err("§16.1", "trailing JSON input");
        }
        Ok(value)
    }
    pub fn canonical(&self) -> String {
        match self {
            Self::Null => "null".into(),
            Self::Bool(b) => b.to_string(),
            Self::Number(n) => n.clone(),
            Self::String(s) => quote(s),
            Self::Array(a) => format!(
                "[{}]",
                a.iter().map(Self::canonical).collect::<Vec<_>>().join(",")
            ),
            Self::Object(o) => {
                let mut entries: Vec<_> = o.iter().collect();
                entries.sort_by(|(a, _), (b, _)| a.encode_utf16().cmp(b.encode_utf16()));
                format!(
                    "{{{}}}",
                    entries
                        .into_iter()
                        .map(|(k, v)| format!("{}:{}", quote(k), v.canonical()))
                        .collect::<Vec<_>>()
                        .join(",")
                )
            }
        }
    }
    pub fn object(&self) -> Result<&BTreeMap<String, Json>> {
        if let Self::Object(o) = self {
            Ok(o)
        } else {
            err("§9.1", "expected JSON object")
        }
    }
    pub fn array(&self) -> Result<&[Json]> {
        if let Self::Array(a) = self {
            Ok(a)
        } else {
            err("§9.1", "expected JSON array")
        }
    }
    pub fn string(&self) -> Result<&str> {
        if let Self::String(s) = self {
            Ok(s)
        } else {
            err("§9.1", "expected JSON string")
        }
    }
    pub fn get(&self, key: &str) -> Result<&Json> {
        self.object()?
            .get(key)
            .ok_or_else(|| crate::Error(format!("§9.1: missing field {key}")))
    }
    /// Metadata integers may be JSON numbers or decimal strings (§9.1).
    pub fn uint(&self) -> Result<u128> {
        let s = match self {
            Self::Number(s) | Self::String(s) => s,
            _ => return err("§9.1", "expected unsigned integer"),
        };
        s.parse()
            .map_err(|_| crate::Error(format!("§9.1: invalid unsigned integer {s}")))
    }
    pub fn fields(&self, required: &[&str], optional: &[&str]) -> Result<()> {
        let obj = self.object()?;
        for key in required {
            self.get(key)?;
        }
        for key in obj.keys() {
            if !required.contains(&key.as_str()) && !optional.contains(&key.as_str()) {
                return err("§9.1", format!("unknown field {key}"));
            }
        }
        Ok(())
    }
}

pub fn quote(s: &str) -> String {
    let mut out = String::from("\"");
    for c in s.chars() {
        match c {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\u{8}' => out.push_str("\\b"),
            '\t' => out.push_str("\\t"),
            '\n' => out.push_str("\\n"),
            '\u{c}' => out.push_str("\\f"),
            '\r' => out.push_str("\\r"),
            c if c < ' ' => out.push_str(&format!("\\u{:04x}", c as u32)),
            c => out.push(c),
        }
    }
    out.push('"');
    out
}

fn canonical_number(raw: &str) -> Result<String> {
    let n: f64 = raw
        .parse()
        .map_err(|_| crate::Error("§16.1: invalid JSON number".into()))?;
    if !n.is_finite() {
        return err("§16.1", "non-finite JSON number");
    }
    if n == 0.0 {
        return Ok("0".into());
    }
    let negative = n < 0.0;
    let display = n.abs().to_string();
    let (mantissa, exponent) = match display.split_once('e') {
        Some((m, e)) => (m, e.parse::<i32>().expect("Rust float exponent")),
        None => (display.as_str(), 0),
    };
    let dot = mantissa.find('.').unwrap_or(mantissa.len()) as i32;
    let digits: String = mantissa.chars().filter(|c| *c != '.').collect();
    let leading = digits.bytes().take_while(|b| *b == b'0').count();
    let position = dot + exponent - leading as i32;
    let digits = digits[leading..].trim_end_matches('0');
    let mut out = if negative {
        "-".to_string()
    } else {
        String::new()
    };
    if position > 0 && position <= 21 {
        if position as usize >= digits.len() {
            out.push_str(digits);
            out.push_str(&"0".repeat(position as usize - digits.len()));
        } else {
            let (a, b) = digits.split_at(position as usize);
            out.push_str(a);
            out.push('.');
            out.push_str(b);
        }
    } else if position > -6 && position <= 0 {
        out.push_str("0.");
        out.push_str(&"0".repeat((-position) as usize));
        out.push_str(digits);
    } else {
        out.push_str(&digits[..1]);
        if digits.len() > 1 {
            out.push('.');
            out.push_str(&digits[1..]);
        }
        out.push('e');
        let e = position - 1;
        if e >= 0 {
            out.push('+');
        }
        out.push_str(&e.to_string());
    }
    Ok(out)
}

struct Parser<'a> {
    text: &'a str,
    pos: usize,
    depth: usize,
}
impl Parser<'_> {
    fn peek(&self) -> Option<u8> {
        self.text.as_bytes().get(self.pos).copied()
    }
    fn ws(&mut self) {
        while matches!(self.peek(), Some(b' ' | b'\n' | b'\r' | b'\t')) {
            self.pos += 1;
        }
    }
    fn take(&mut self, b: u8) -> bool {
        if self.peek() == Some(b) {
            self.pos += 1;
            true
        } else {
            false
        }
    }
    fn expect(&mut self, b: u8) -> Result<()> {
        if self.take(b) {
            Ok(())
        } else {
            err(
                "§16.1",
                format!("expected JSON '{}' at byte {}", b as char, self.pos),
            )
        }
    }
    fn value(&mut self) -> Result<Json> {
        self.ws();
        self.depth += 1;
        if self.depth > 256 {
            return err("§16.1", "JSON nesting exceeds 256");
        }
        let value = match self.peek() {
            Some(b'"') => Json::String(self.string()?),
            Some(b'{') => {
                self.pos += 1;
                self.ws();
                let mut o = BTreeMap::new();
                if !self.take(b'}') {
                    loop {
                        self.ws();
                        let key = self.string()?;
                        self.ws();
                        self.expect(b':')?;
                        let v = self.value()?;
                        if o.insert(key.clone(), v).is_some() {
                            return err("§16.1", format!("duplicate JSON key {key}"));
                        }
                        self.ws();
                        if self.take(b'}') {
                            break;
                        }
                        self.expect(b',')?;
                    }
                }
                Json::Object(o)
            }
            Some(b'[') => {
                self.pos += 1;
                self.ws();
                let mut a = Vec::new();
                if !self.take(b']') {
                    loop {
                        a.push(self.value()?);
                        self.ws();
                        if self.take(b']') {
                            break;
                        }
                        self.expect(b',')?;
                    }
                }
                Json::Array(a)
            }
            Some(b'-' | b'0'..=b'9') => {
                let start = self.pos;
                self.take(b'-');
                if !self.take(b'0') {
                    if !matches!(self.peek(), Some(b'1'..=b'9')) {
                        return err("§16.1", "invalid JSON integer");
                    }
                    while matches!(self.peek(), Some(b'0'..=b'9')) {
                        self.pos += 1;
                    }
                }
                if self.take(b'.') {
                    let p = self.pos;
                    while matches!(self.peek(), Some(b'0'..=b'9')) {
                        self.pos += 1;
                    }
                    if p == self.pos {
                        return err("§16.1", "empty fraction");
                    }
                }
                if self.take(b'e') || self.take(b'E') {
                    if !self.take(b'+') {
                        self.take(b'-');
                    }
                    let p = self.pos;
                    while matches!(self.peek(), Some(b'0'..=b'9')) {
                        self.pos += 1;
                    }
                    if p == self.pos {
                        return err("§16.1", "empty exponent");
                    }
                }
                Json::Number(canonical_number(&self.text[start..self.pos])?)
            }
            _ => {
                let mut found = None;
                for (s, v) in [
                    ("null", Json::Null),
                    ("true", Json::Bool(true)),
                    ("false", Json::Bool(false)),
                ] {
                    if self.text[self.pos..].starts_with(s) {
                        self.pos += s.len();
                        found = Some(v);
                        break;
                    }
                }
                found.ok_or_else(|| {
                    crate::Error(format!("§16.1: invalid JSON at byte {}", self.pos))
                })?
            }
        };
        self.depth -= 1;
        Ok(value)
    }
    fn hex4(&mut self) -> Result<u16> {
        let end = self.pos + 4;
        let s = self
            .text
            .as_bytes()
            .get(self.pos..end)
            .ok_or_else(|| crate::Error("§16.1: short Unicode escape".into()))?;
        let mut n = 0;
        for b in s {
            n = n * 16
                + match b {
                    b'0'..=b'9' => (b - b'0') as u16,
                    b'a'..=b'f' => (b - b'a' + 10) as u16,
                    b'A'..=b'F' => (b - b'A' + 10) as u16,
                    _ => return err("§16.1", "invalid Unicode escape"),
                };
        }
        self.pos = end;
        Ok(n)
    }
    fn string(&mut self) -> Result<String> {
        self.expect(b'"')?;
        let mut out = String::new();
        loop {
            match self.peek() {
                None => return err("§16.1", "unterminated JSON string"),
                Some(b'"') => {
                    self.pos += 1;
                    return Ok(out);
                }
                Some(b'\\') => {
                    self.pos += 1;
                    let b = self
                        .peek()
                        .ok_or_else(|| crate::Error("§16.1: short escape".into()))?;
                    self.pos += 1;
                    out.push(match b {
                        b'"' => '"',
                        b'\\' => '\\',
                        b'/' => '/',
                        b'b' => '\u{8}',
                        b'f' => '\u{c}',
                        b'n' => '\n',
                        b'r' => '\r',
                        b't' => '\t',
                        b'u' => {
                            let hi = self.hex4()?;
                            let n = if (0xd800..=0xdbff).contains(&hi) {
                                self.expect(b'\\')?;
                                self.expect(b'u')?;
                                let lo = self.hex4()?;
                                if !(0xdc00..=0xdfff).contains(&lo) {
                                    return err("§16.1", "invalid low surrogate");
                                }
                                0x10000 + (((hi as u32 - 0xd800) << 10) | (lo as u32 - 0xdc00))
                            } else {
                                hi as u32
                            };
                            char::from_u32(n)
                                .ok_or_else(|| crate::Error("§16.1: lone surrogate".into()))?
                        }
                        _ => return err("§16.1", "invalid JSON escape"),
                    });
                }
                Some(0..=31) => return err("§16.1", "unescaped JSON control character"),
                _ => {
                    let c = self.text[self.pos..].chars().next().expect("UTF-8 char");
                    self.pos += c.len_utf8();
                    out.push(c);
                }
            }
        }
    }
}
````

## `src/linking.rs` (254 lines)

````rust
//! Symbol resolution and canonical linked objects (§9.3).
use crate::{err, identity::hex, json::Json, Error, Object, Result, SECTIONS};
use std::collections::BTreeMap;

impl Object {
    pub fn link(objects: &[Object]) -> Result<Self> {
        let first = objects
            .first()
            .ok_or_else(|| Error("§9.3: no objects to link".into()))?;
        let mut result = Self {
            text: String::new(),
            ptr_width: first.ptr_width,
            metadata: BTreeMap::new(),
            functions: BTreeMap::new(),
            function_order: Vec::new(),
            data: BTreeMap::new(),
        };
        let mut definitions: BTreeMap<String, Json> = BTreeMap::new();
        let mut imports: Vec<(String, Json)> = Vec::new();
        let mut known_closures: BTreeMap<String, String> = BTreeMap::new();
        let mut old_identities = Vec::new();
        for object in objects {
            object.check_hashes()?;
            if object.ptr_width != result.ptr_width {
                return err("§9.3", "pointer widths differ");
            }
            let identity = object.identity()?;
            for (name, hash) in &identity.closure_hashes {
                if let Some(hash) = hash {
                    if known_closures.get(name).is_some_and(|prior| prior != hash) {
                        return err("§9.3", format!("unequal closure definitions for @{name}"));
                    }
                    known_closures.insert(name.clone(), hash.clone());
                }
            }
            old_identities.push(identity);
            for symbol in object.symbols()?.values() {
                let name = symbol.get("name")?.string()?;
                if let Some(prior) = definitions.get(name) {
                    if prior.get("signature")? != symbol.get("signature")?
                        || prior.get("kind")? != symbol.get("kind")?
                    {
                        return err("§9.3", format!("incompatible duplicate @{name}"));
                    }
                } else {
                    definitions.insert(name.into(), symbol.clone());
                }
            }
            for (name, function) in &object.functions {
                if result
                    .functions
                    .get(name)
                    .is_some_and(|prior| prior.lines != function.lines)
                {
                    return err("§9.3", format!("conflicting function bodies for @{name}"));
                }
                result.functions.insert(name.clone(), function.clone());
            }
            for (name, bytes) in &object.data {
                if result.data.get(name).is_some_and(|prior| prior != bytes) {
                    return err("§9.3", format!("conflicting data @{name}"));
                }
                result.data.insert(name.clone(), bytes.clone());
            }
            if let Some(entries) = object.section("imports") {
                for (name, value) in entries.object()? {
                    imports.push((name.clone(), value.clone()));
                }
            }
            for (section, value) in &object.metadata {
                if matches!(section.as_str(), "symbols" | "imports") {
                    continue;
                }
                match result.metadata.get_mut(section) {
                    None => {
                        result.metadata.insert(section.clone(), value.clone());
                    }
                    Some(prior) => merge_metadata(prior, value, section)?,
                }
            }
        }
        for (name, import) in &imports {
            let definition = definitions
                .get(name)
                .ok_or_else(|| Error(format!("§9.3: unresolved import @{name}")))?;
            if import.get("signature")? != definition.get("signature")? {
                return err("§9.3", format!("import signature mismatch for @{name}"));
            }
        }
        result.function_order = result.functions.keys().cloned().collect();
        result.metadata.insert(
            "symbols".into(),
            Json::Object(
                definitions
                    .values()
                    .cloned()
                    .enumerate()
                    .map(|(i, s)| (i.to_string(), s))
                    .collect(),
            ),
        );
        // Resolution changes envelopes which used unresolved-name fingerprints.
        // Recompute the graph before rebinding any external metadata.
        let identity = result.identity()?;
        for (name, import) in &imports {
            if let Some(pin) = import.object()?.get("pinned_closure_hash") {
                if identity.closure_hashes[name].as_deref() != Some(pin.string()?) {
                    return err("§9.3", format!("pinned closure mismatch for @{name}"));
                }
            }
        }
        if let Some(Json::Object(symbols)) = result.metadata.get_mut("symbols") {
            for symbol in symbols.values_mut() {
                let n = symbol.get("name")?.string()?.to_string();
                let Json::Object(fields) = symbol else {
                    unreachable!("validated symbol")
                };
                fields.insert(
                    "interface_hash".into(),
                    Json::String(identity.interface_hashes[&n].clone()),
                );
            }
        }
        let mut replacements = BTreeMap::new();
        for old in old_identities {
            for (name, hash) in old.interface_hashes {
                replacements.insert(hash, identity.interface_hashes[&name].clone());
            }
            for (name, hash) in old.closure_hashes {
                if let Some(hash) = hash {
                    replacements.insert(
                        hash,
                        identity.closure_hashes[&name]
                            .clone()
                            .expect("fully resolved closure"),
                    );
                }
            }
        }
        for section in ["schedule", "certificate", "coverage"] {
            if let Some(value) = result.metadata.get_mut(section) {
                replace_hashes(value, &replacements);
            }
        }
        result.text = result.render()?;
        let object_hash = result.identity()?.object_hash;
        if let Some(Json::Object(cert)) = result.metadata.get_mut("certificate") {
            if let Some(Json::Object(bindings)) = cert.get_mut("bindings") {
                bindings.insert("object_hash".into(), Json::String(object_hash));
            }
        }
        result.text = result.render()?;
        let linked = Self::parse(&result.text)?;
        linked.check_hashes()?;
        Ok(linked)
    }
    pub(crate) fn render(&self) -> Result<String> {
        let mut text=format!("bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width={}\n",self.ptr_width);
        for section in SECTIONS {
            let body = match section {
                "functions" => {
                    if self.functions.is_empty() {
                        continue;
                    }
                    self.function_order
                        .iter()
                        .map(|n| self.functions[n].lines.join("\n"))
                        .collect::<Vec<_>>()
                        .join("\n")
                }
                "data" => {
                    if self.data.is_empty() {
                        continue;
                    }
                    self.data
                        .iter()
                        .map(|(n, b)| format!("{n} {}", hex(b)))
                        .collect::<Vec<_>>()
                        .join("\n")
                }
                _ => match self.section(section) {
                    Some(value) => value.canonical(),
                    None => continue,
                },
            };
            text.push_str(&format!("\nsection {section}\n{body}\n"));
        }
        Ok(text)
    }
}
fn merge_metadata(destination: &mut Json, source: &Json, path: &str) -> Result<()> {
    if destination == source {
        return Ok(());
    }
    if path == "coverage.entries" {
        let (Json::Array(a), Json::Array(b)) = (destination, source) else {
            return err("§9.3", "coverage entries must be arrays");
        };
        for e in b {
            if !a.contains(e) {
                a.push(e.clone());
            }
        }
        return Ok(());
    }
    let recursive = matches!(
        path,
        "layout"
            | "layout.globals"
            | "layout.interface_regions"
            | "devices"
            | "devices.models"
            | "devices.services"
            | "coverage"
    ) || path.starts_with("layout.interface_regions.")
        && path.split('.').count() == 3;
    if !recursive {
        return err("§9.3", format!("conflicting metadata at {path}"));
    }
    let Json::Object(target) = destination else {
        return err("§9.3", format!("metadata object required at {path}"));
    };
    for (key, value) in source.object()? {
        if let Some(prior) = target.get_mut(key) {
            merge_metadata(prior, value, &format!("{path}.{key}"))?;
        } else {
            target.insert(key.clone(), value.clone());
        }
    }
    Ok(())
}
fn replace_hashes(value: &mut Json, replacements: &BTreeMap<String, String>) {
    match value {
        Json::String(s) => {
            if let Some(next) = replacements.get(s) {
                *s = next.clone();
            }
        }
        Json::Array(values) => {
            for v in values {
                replace_hashes(v, replacements);
            }
        }
        Json::Object(fields) => {
            let previous = std::mem::take(fields);
            for (key, mut value) in previous {
                replace_hashes(&mut value, replacements);
                let key = replacements.get(&key).cloned().unwrap_or(key);
                fields.insert(key, value);
            }
        }
        _ => {}
    }
}
````

## `src/machine.rs` (911 lines)

````rust
//! Literal §3.6/§3.7 basis machine. Frames contain displaced/captured values;
//! reversal uses inverse operations, never a saved pre-step state.
use crate::{
    err,
    object::{integer, is_binop, is_div, list, mask, parse_bits},
    oracle::{binop, compare, divide, signed, Allocation, Memory, Program},
    Argument, Budget, Error, Function, Instruction, Object, OracleInput, OracleOutcome, Result,
    Type,
};
use std::collections::BTreeMap;

#[derive(Clone, Debug, PartialEq, Eq, Default)]
struct Slot {
    word: u128,
    size: u128,
    live: bool,
    pinned: bool,
}
impl Slot {
    fn word(word: u128) -> Self {
        Self {
            word,
            ..Self::default()
        }
    }
    fn entry(e: Allocation) -> Self {
        Self {
            word: e.base,
            size: e.size,
            live: e.live,
            pinned: e.pinned,
        }
    }
    fn allocation(&self) -> Allocation {
        Allocation {
            base: self.word,
            size: self.size,
            live: self.live,
            pinned: self.pinned,
        }
    }
    fn xor(&mut self, other: &Self) {
        self.word ^= other.word;
        self.size ^= other.size;
        self.live ^= other.live;
        self.pinned ^= other.pinned;
    }
}
#[derive(Clone, Debug, PartialEq, Eq, Default)]
struct Frame {
    old_pc: usize,
    slots: Vec<Slot>,
    flag: bool,
    succ: usize,
}

/// The complete mutable basis tuple, including every retained frame and cell.
/// Immutable program text, input bindings and budget are held by OracleMachine.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct BasisConfiguration {
    pub locations: BTreeMap<(String, String), u128>,
    pub stack: BTreeMap<u128, u128>,
    pub pc: usize,
    pub pc_prime: usize,
    pub faulted: bool,
    pub code: u128,
    pub result_val: u128,
    pub sp: u128,
    pub fp: u128,
    pub depth: u128,
    pub atop: u128,
    memory: Memory,
    frames: Vec<Frame>,
}
pub struct OracleMachine<'a> {
    object: &'a Object,
    root: String,
    input: OracleInput,
    budget: Budget,
    program: Program<'a>,
    state: BasisConfiguration,
    used: usize,
    ids: Vec<(String, String)>,
}
#[derive(Clone)]
enum Destination {
    Location(String),
    Memory(String, u16),
    EntryAtop,
    Heap,
    Atop,
}

impl<'a> OracleMachine<'a> {
    pub fn new(
        object: &'a Object,
        name: &str,
        input: &OracleInput,
        budget: Budget,
    ) -> Result<Self> {
        object.validate_budget(budget)?;
        let program = Program::new(object, name)?;
        let root = &object.functions[name];
        if root.params[0].len() != input.ins.len()
            || root.params[4].len() != input.args.len()
            || root.params[3].len() != input.regions.len()
        {
            return err("§5.1", "machine interface argument count mismatch");
        }
        let mut locations = BTreeMap::new();
        let mut ids = Vec::new();
        for (f, _) in &program.rows {
            for p in f.locations() {
                let key = (f.name.clone(), p.name.clone());
                if let std::collections::btree_map::Entry::Vacant(entry) = locations.entry(key) {
                    ids.push(entry.key().clone());
                    entry.insert(0);
                }
            }
        }
        for (p, v) in root.params[0].iter().zip(&input.ins) {
            if *v & !mask(p.ty.width(object.ptr_width)?) != 0 {
                return err("§3.3", "machine input exceeds width");
            }
            locations.insert((name.into(), p.name.clone()), *v);
        }
        for (p, v) in root.params[4].iter().zip(&input.args) {
            match (&p.ty, v) {
                (Type::Int(w), Argument::Bits(v)) if *v & !mask(*w) == 0 => {
                    locations.insert((name.into(), p.name.clone()), *v);
                }
                (Type::Ptr, Argument::Bits(v)) if *v & !mask(object.ptr_width) == 0 => {
                    locations.insert((name.into(), p.name.clone()), *v);
                }
                (Type::Token, Argument::Token(b)) => object.validate_budget(*b)?,
                (Type::F64, Argument::Float(x)) if x.is_finite() => {}
                _ => return err("§3.3", "machine classical argument type mismatch"),
            }
        }
        let memory = Memory::initial(object, root, input)?;
        let atop = memory.allocations.len() as u128;
        let slots = program
            .rows
            .iter()
            .map(|(_, i)| match i.op.as_str() {
                "lift.call" => list(&i.operands[1]).map(|a| a.len() + 3).unwrap_or(0),
                "lift.ret" => 3,
                "lift.alloc" => 4,
                "lift.parmov" => i.lhs.len(),
                _ => usize::from(!i.lhs.is_empty() || i.op.starts_with("lift.store.")),
            })
            .max()
            .unwrap_or(0);
        let count = usize::try_from(budget.steps)
            .map_err(|_| Error("§3.6: frame count exceeds host address space".into()))?;
        let frame = Frame {
            slots: vec![Slot::default(); slots],
            ..Frame::default()
        };
        let mut frames = Vec::new();
        frames
            .try_reserve_exact(count)
            .map_err(|e| Error(format!("§3.6: cannot allocate step frames: {e}")))?;
        frames.resize(count, frame);
        Ok(Self {
            object,
            root: name.into(),
            input: input.clone(),
            budget,
            program,
            state: BasisConfiguration {
                locations,
                stack: BTreeMap::new(),
                pc: 0,
                pc_prime: 0,
                faulted: false,
                code: 0,
                result_val: 0,
                sp: 0,
                fp: 0,
                depth: 0,
                atop,
                memory,
                frames,
            },
            used: 0,
            ids,
        })
    }
    pub fn snapshot(&self) -> BasisConfiguration {
        self.state.clone()
    }
    pub fn frames_clean(&self) -> bool {
        self.state.frames.iter().all(|f| {
            f.old_pc == 0 && !f.flag && f.succ == 0 && f.slots.iter().all(|s| s == &Slot::default())
        })
    }
    /// §5.2 commit, with caller-owned target/fault entry values. These writes
    /// persist while all internal state is subsequently prefix-reversed.
    pub fn commit(&self,mut target:u128,mut fault:u128)->Result<(u128,u128)>{
        let root=&self.object.functions[&self.root];let tw=root.params[1][0].ty.width(self.object.ptr_width)?;let fw=root.params[2][0].ty.width(self.object.ptr_width)?;
        if target&!mask(tw)!=0||fault&!mask(fw)!=0{return err("§3.3","commit interface value exceeds declared width");}
        let at_halt=self.state.pc==self.program.halt;
        if at_halt&&!self.state.faulted{target^=self.state.result_val;}
        if self.state.faulted{fault^=self.state.code;}
        if !at_halt{fault^=1;}
        Ok((target,fault))
    }
    pub fn outcome(&self) -> OracleOutcome {
        let code = if self.state.faulted {
            self.state.code
        } else if self.state.pc != self.program.halt {
            1
        } else {
            0
        };
        OracleOutcome {
            payload: if self.state.pc == self.program.halt && !self.state.faulted {
                self.state.result_val
            } else {
                0
            },
            code,
            steps: self.state.frames[..self.used]
                .iter()
                .filter(|f| f.old_pc != self.program.halt)
                .count() as u64,
        }
    }
    pub fn forward_step(&mut self) -> Result<()> {
        if self.used == self.state.frames.len() {
            return err("§3.6", "forward step exceeds budget");
        }
        let mut frame = self.state.frames[self.used].clone();
        if frame
            != (Frame {
                slots: vec![Slot::default(); frame.slots.len()],
                ..Frame::default()
            })
        {
            return err("§3.6", "forward frame is not clean");
        }
        // Dispatch is read once before any row effects. On a basis tuple exactly
        // one comparator is true, so inactive controlled rows are identities.
        let old = self.state.pc;
        let successor = if old == self.program.halt {
            self.program.halt
        } else {
            let (f, i) = self.program.rows[old];
            let (flag, code) = self.flag(f, i)?;
            frame.flag ^= flag;
            if i.op == "lift.ret" {
                self.forward_ret(f, i, &mut frame)?;
            } else if i.op == "lift.call" {
                self.forward_call(f, i, old, &mut frame)?;
            } else {
                if matches!(i.op.as_str(), "qbranch" | "qjumpr") {
                    frame.succ ^= self.dynamic_successor(f, i)?;
                }
                if !flag {
                    let destinations = self.destinations(i)?;
                    let values = self.values(f, i)?;
                    for (j, v) in values.iter().enumerate() {
                        frame.slots[j].xor(v);
                    }
                    for (j, d) in destinations.iter().enumerate() {
                        self.exchange(f, d, &mut frame.slots[j])?;
                    }
                    self.direct(f, i, false)?;
                }
            }
            if flag {
                self.state.faulted ^= true;
                self.state.code ^= code;
            }
            self.successor(f, i, old, &frame)?
        };
        self.state.pc_prime ^= successor;
        std::mem::swap(&mut self.state.pc, &mut self.state.pc_prime);
        std::mem::swap(&mut self.state.pc_prime, &mut frame.old_pc);
        // Uncomputing dispatch from old_pc leaves no retained comparator bits.
        if self.state.pc_prime != 0 {
            return err("§3.6", "forward pc scratch did not clear");
        }
        self.state.frames[self.used] = frame;
        self.used += 1;
        Ok(())
    }
    pub fn inverse_step(&mut self) -> Result<()> {
        if self.used == 0 {
            return err("§3.6", "no forward step to invert");
        }
        let index = self.used - 1;
        let mut frame = self.state.frames[index].clone();
        let old = frame.old_pc;
        std::mem::swap(&mut self.state.pc_prime, &mut frame.old_pc);
        std::mem::swap(&mut self.state.pc, &mut self.state.pc_prime);
        let successor = if old == self.program.halt {
            self.program.halt
        } else {
            let (f, i) = self.program.rows[old];
            self.successor(f, i, old, &frame)?
        };
        self.state.pc_prime ^= successor;
        if self.state.pc_prime != 0 {
            return err("§3.6", "inverse successor scratch did not clear");
        }
        if old != self.program.halt {
            let (f, i) = self.program.rows[old];
            let code = self.fault_code(f, i)?;
            if frame.flag {
                self.state.faulted ^= true;
                self.state.code ^= code;
            }
            if i.op == "lift.call" {
                self.inverse_call(f, i, old, &mut frame)?;
            } else if i.op == "lift.ret" {
                self.inverse_ret(f, i, &mut frame)?;
            } else {
                if !frame.flag {
                    self.direct(f, i, true)?;
                    let destinations = self.destinations(i)?;
                    for (j, d) in destinations.iter().enumerate().rev() {
                        self.exchange(f, d, &mut frame.slots[j])?;
                    }
                    let values = self.values(f, i)?;
                    for (j, v) in values.iter().enumerate() {
                        frame.slots[j].xor(v);
                    }
                }
                if matches!(i.op.as_str(), "qbranch" | "qjumpr") {
                    frame.succ ^= self.dynamic_successor(f, i)?;
                }
            }
            frame.flag ^= self.flag(f, i)?.0;
        }
        if frame.old_pc != 0
            || frame.flag
            || frame.succ != 0
            || frame.slots.iter().any(|s| s != &Slot::default())
        {
            return err(
                "§3.6",
                format!("inverse frame is not clean at row {old}: {frame:?}"),
            );
        }
        self.state.frames[index] = frame;
        self.used -= 1;
        Ok(())
    }
    fn read(&self, f: &Function, n: &str) -> Result<u128> {
        self.state
            .locations
            .get(&(f.name.clone(), n.into()))
            .copied()
            .ok_or_else(|| Error(format!("§3.7: missing machine location {n} in @{}", f.name)))
    }
    fn width(&self, f: &Function, n: &str) -> Result<u16> {
        f.locations()
            .into_iter()
            .chain(f.params[0].iter())
            .chain(f.params[4].iter())
            .find(|p| p.name == n)
            .ok_or_else(|| Error("§3.7: unknown machine operand width".into()))?
            .ty
            .width(self.object.ptr_width)
    }
    fn length(&self, f: &Function, n: &str) -> Result<u128> {
        if integer(n) {
            n.parse()
                .map_err(|_| Error("§3.3: invalid machine length".into()))
        } else {
            self.read(f, n)
        }
    }
    fn stack_read(&self, p: u128) -> u128 {
        self.state.stack.get(&p).copied().unwrap_or(0)
    }
    fn stack_set(&mut self, p: u128, v: u128) {
        if v == 0 {
            self.state.stack.remove(&p);
        } else {
            self.state.stack.insert(p, v);
        }
    }
    fn stack_xor(&mut self, p: u128, v: u128) {
        let value = self.stack_read(p) ^ v;
        self.stack_set(p, value);
    }
    fn exchange_location(&mut self, f: &Function, n: &str, value: &mut u128) -> Result<()> {
        let w = self.width(f, n)?;
        let mask = mask(w);
        let loc = self
            .state
            .locations
            .get_mut(&(f.name.clone(), n.into()))
            .ok_or_else(|| Error("§3.7: missing exchange location".into()))?;
        let low = *value & mask;
        *value = (*value & !mask) | *loc;
        *loc = low;
        Ok(())
    }
    fn fault_code(&self, f: &Function, i: &Instruction) -> Result<u128> {
        Ok(match i.op.as_str() {
            "lift.call" => 3,
            "lift.ret" | "qjumpr" => 4,
            "lift.alloc" => 2,
            "lift.free" | "lift.boundscheck" => 7,
            "lift.faultif" => i.operands[1].parse().expect("validated fault code"),
            op if op.starts_with("lift.load.") || op.starts_with("lift.store.") => 7,
            op if op.strip_prefix("lift.").is_some_and(is_div) => {
                let a = self.read(f, &i.operands[0])?;
                let b = self.read(f, &i.operands[1])?;
                if b == 0 {
                    5
                } else if op.starts_with("lift.s")
                    && a == 1u128 << (self.width(f, &i.operands[0])? - 1)
                    && b == mask(self.width(f, &i.operands[0])?)
                {
                    6
                } else {
                    5
                }
            }
            _ => 0,
        })
    }
    fn flag(&self, f: &Function, i: &Instruction) -> Result<(bool, u128)> {
        let a = &i.operands;
        let flag =
            match i.op.as_str() {
                "lift.call" => {
                    let c = &self.object.functions[a[0].trim_start_matches('@')];
                    self.state.depth + 1 > self.budget.depth
                        || self
                            .state
                            .sp
                            .checked_add(c.frame_cells() as u128)
                            .is_none_or(|s| s > self.budget.stack)
                }
                "lift.ret" => self.state.depth == 0,
                "lift.alloc" => self
                    .state
                    .memory
                    .allocation_fails(self.length(f, &a[0])?, self.budget),
                "lift.free" => !self.state.memory.allocations.iter().any(|e| {
                    e.base == self.read(f, &a[0]).unwrap_or(u128::MAX) && e.live && !e.pinned
                }),
                "lift.boundscheck" => !self
                    .state
                    .memory
                    .valid(self.read(f, &a[0])?, self.length(f, &a[1])?),
                "lift.faultif" => self.read(f, &a[0])? != 0,
                "qjumpr" => {
                    let v = self.read(f, &a[0])?;
                    let (start, end) = self.program.ranges[&f.name];
                    v < start as u128 || v >= end as u128
                }
                op if op.starts_with("lift.load.i") || op.starts_with("lift.store.i") => {
                    !self.state.memory.valid(
                        self.read(f, &a[0])?,
                        op.rsplit_once(".i")
                            .expect("memory suffix")
                            .1
                            .parse::<u128>()
                            .expect("validated width")
                            / 8,
                    )
                }
                op if op.strip_prefix("lift.").is_some_and(is_div) => divide(
                    op.trim_start_matches("lift."),
                    self.read(f, &a[0])?,
                    self.read(f, &a[1])?,
                    self.width(f, &a[0])?,
                )
                .is_err(),
                _ => false,
            };
        Ok((flag, self.fault_code(f, i)?))
    }
    fn dynamic_successor(&self, f: &Function, i: &Instruction) -> Result<usize> {
        if i.op == "qbranch" {
            self.program.label(
                &f.name,
                if self.read(f, &i.operands[0])? != 0 {
                    &i.operands[1]
                } else {
                    &i.operands[2]
                },
            )
        } else {
            let w = (usize::BITS - self.program.halt.leading_zeros()).max(1);
            Ok((self.read(f, &i.operands[0])? & mask(w as u16)) as usize)
        }
    }
    fn successor(&self, f: &Function, i: &Instruction, k: usize, frame: &Frame) -> Result<usize> {
        if frame.flag {
            return Ok(self.program.halt);
        }
        Ok(match i.op.as_str() {
            "lift.retval" | "fault" => self.program.halt,
            "qjump" => self.program.label(&f.name, &i.operands[0])?,
            "qbranch" | "qjumpr" | "lift.ret" => frame.succ,
            "lift.call" => self.program.ranges[i.operands[0].trim_start_matches('@')].0,
            _ => k + 1,
        })
    }
    fn destinations(&self, i: &Instruction) -> Result<Vec<Destination>> {
        Ok(match i.op.as_str() {
            "lift.alloc" => vec![
                Destination::Location(i.lhs[0].clone()),
                Destination::EntryAtop,
                Destination::Heap,
                Destination::Atop,
            ],
            op if op.starts_with("lift.store.i") => vec![Destination::Memory(
                i.operands[0].clone(),
                op.rsplit_once(".i")
                    .expect("suffix")
                    .1
                    .parse()
                    .expect("width"),
            )],
            _ => i
                .lhs
                .iter()
                .filter(|_| !matches!(i.op.as_str(), "lift.call" | "lift.ret"))
                .map(|n| Destination::Location(n.clone()))
                .collect(),
        })
    }
    fn values(&self, f: &Function, i: &Instruction) -> Result<Vec<Slot>> {
        let op = i.op.as_str();
        let a = &i.operands;
        let rd = |n: &str| self.read(f, n);
        let width = |n: &str| self.width(f, n);
        let values = if let Some(w) = op.strip_prefix("lift.const.i") {
            vec![parse_bits(&a[0], w.parse().expect("width"))?]
        } else if let Some(bin) = op.strip_prefix("lift.").filter(|s| is_binop(s)) {
            vec![binop(bin, rd(&a[0])?, rd(&a[1])?, width(&a[0])?)]
        } else if let Some(div) = op.strip_prefix("lift.").filter(|s| is_div(s)) {
            vec![divide(div, rd(&a[0])?, rd(&a[1])?, width(&a[0])?)
                .map_err(|c| Error(format!("§3.6: unguarded division fault {c}")))?]
        } else if let Some(pred) = op.strip_prefix("lift.icmp.") {
            vec![compare(pred, rd(&a[0])?, rd(&a[1])?, width(&a[0])?) as u128]
        } else if let Some((cast, _)) = op
            .strip_prefix("lift.")
            .and_then(|s| s.split_once(".i"))
            .filter(|(c, _)| ["zext", "sext", "trunc"].contains(c))
        {
            vec![if cast == "sext" {
                signed(rd(&a[0])?, width(&a[0])?) as u128
            } else {
                rd(&a[0])?
            }]
        } else if let Some(w) = op.strip_prefix("lift.load.i") {
            vec![self
                .state
                .memory
                .load(rd(&a[0])?, w.parse().expect("width"))]
        } else if op.starts_with("lift.store.i") {
            vec![rd(&a[1])?]
        } else {
            match op {
                "lift.mov" => vec![rd(&a[0])?],
                "lift.select" => vec![rd(if rd(&a[0])? != 0 { &a[1] } else { &a[2] })?],
                "lift.parmov" => list(&a[0])?.iter().map(|s| rd(s)).collect::<Result<_>>()?,
                "lift.label" => vec![self.program.label(&f.name, &a[0])? as u128],
                "lift.addr" => vec![self.state.memory.addresses[a[0].trim_start_matches('@')]],
                "lift.alloc" => {
                    let n = self.length(f, &a[0])?;
                    let base = self.state.memory.heap_base + self.state.memory.heap_used;
                    return Ok(vec![
                        Slot::word(base),
                        Slot::entry(Allocation {
                            base,
                            size: n,
                            live: true,
                            pinned: false,
                        }),
                        Slot::word(self.state.memory.heap_used + n.max(1)),
                        Slot::word(self.state.atop + 1),
                    ]);
                }
                _ => Vec::new(),
            }
        };
        Ok(values
            .into_iter()
            .enumerate()
            .map(|(j, v)| {
                Slot::word(if j < i.lhs.len() {
                    v & mask(width(&i.lhs[j]).expect("validated assignment width"))
                } else {
                    v
                })
            })
            .collect())
    }
    fn exchange(&mut self, f: &Function, d: &Destination, s: &mut Slot) -> Result<()> {
        match d {
            Destination::Location(n) => self.exchange_location(f, n, &mut s.word)?,
            Destination::Memory(n, w) => {
                let p = self.read(f, n)?;
                let old = self.state.memory.load(p, *w);
                self.state.memory.store(p, *w, s.word);
                s.word = old;
            }
            Destination::Heap => std::mem::swap(&mut self.state.memory.heap_used, &mut s.word),
            Destination::Atop => std::mem::swap(&mut self.state.atop, &mut s.word),
            Destination::EntryAtop => {
                let index = usize::try_from(self.state.atop).map_err(|_| {
                    Error("§3.6: allocation index exceeds host address space".into())
                })?;
                let zero = Allocation {
                    base: 0,
                    size: 0,
                    live: false,
                    pinned: false,
                };
                let old = self
                    .state
                    .memory
                    .allocations
                    .get(index)
                    .cloned()
                    .unwrap_or_else(|| zero.clone());
                let new = s.allocation();
                if index == self.state.memory.allocations.len() {
                    self.state.memory.allocations.push(new);
                } else {
                    self.state.memory.allocations[index] = new;
                }
                while self.state.memory.allocations.last() == Some(&zero) {
                    self.state.memory.allocations.pop();
                }
                *s = Slot::entry(old);
            }
        }
        Ok(())
    }
    fn direct(&mut self, f: &Function, i: &Instruction, inverse: bool) -> Result<()> {
        match i.op.as_str() {
            "lift.free" => {
                let p = self.read(f, &i.operands[0])?;
                for e in &mut self.state.memory.allocations {
                    if e.base == p {
                        e.live ^= true;
                    }
                }
            }
            "lift.retval" => self.state.result_val ^= self.read(f, &i.operands[0])?,
            "fault" => {
                self.state.code ^= i.operands[0].parse::<u128>().expect("fault code");
                self.state.faulted ^= true;
            }
            "lift.oracle_call" | "lift.oracle_uncall" => self.nested_oracle(f, i)?,
            "lift.perm_call" => self.permutation_call(f, i, inverse)?,
            _ => {}
        }
        Ok(())
    }
    fn push_pop_locations(&mut self, f: &Function, base: u128) -> Result<()> {
        for (j, p) in f.locations().iter().enumerate() {
            let addr = base + 3 + j as u128;
            let mut cell = self.stack_read(addr);
            self.exchange_location(f, &p.name, &mut cell)?;
            self.stack_set(addr, cell);
        }
        Ok(())
    }
    fn forward_call(
        &mut self,
        f: &Function,
        i: &Instruction,
        k: usize,
        frame: &mut Frame,
    ) -> Result<()> {
        if frame.flag {
            return Ok(());
        }
        let callee = &self.object.functions[i.operands[0].trim_start_matches('@')];
        let args = list(&i.operands[1])?;
        let m = args.len();
        // C1 capture before moving ANY callee locations (including recursive args).
        for (j, a) in args.iter().enumerate() {
            frame.slots[j].word ^= self.read(f, a)?;
        }
        self.push_pop_locations(callee, self.state.sp)?; // C2
        self.stack_xor(self.state.sp, (k + 1) as u128);
        self.stack_xor(self.state.sp + 1, self.state.fp);
        let dest = (f.name.clone(), i.lhs[0].clone());
        let id = self
            .ids
            .iter()
            .position(|n| *n == dest)
            .ok_or_else(|| Error("§3.7: missing destination id".into()))?;
        self.stack_xor(self.state.sp + 2, id as u128); // C3
        for (j, p) in callee.params[0].iter().enumerate() {
            *self
                .state
                .locations
                .get_mut(&(callee.name.clone(), p.name.clone()))
                .expect("callee param") ^= frame.slots[j].word;
        } // C4
        frame.slots[m].word ^= self.state.sp;
        frame.slots[m + 1].word ^= self.state.sp + callee.frame_cells() as u128;
        frame.slots[m + 2].word ^= self.state.depth + 1;
        std::mem::swap(&mut frame.slots[m].word, &mut self.state.fp);
        std::mem::swap(&mut frame.slots[m + 1].word, &mut self.state.sp);
        std::mem::swap(&mut frame.slots[m + 2].word, &mut self.state.depth);
        Ok(())
    }
    fn inverse_call(
        &mut self,
        f: &Function,
        i: &Instruction,
        k: usize,
        frame: &mut Frame,
    ) -> Result<()> {
        if frame.flag {
            return Ok(());
        }
        let callee = &self.object.functions[i.operands[0].trim_start_matches('@')];
        let args = list(&i.operands[1])?;
        let m = args.len();
        std::mem::swap(&mut frame.slots[m + 2].word, &mut self.state.depth);
        std::mem::swap(&mut frame.slots[m + 1].word, &mut self.state.sp);
        std::mem::swap(&mut frame.slots[m].word, &mut self.state.fp);
        frame.slots[m + 2].word ^= self.state.depth + 1;
        frame.slots[m + 1].word ^= self.state.sp + callee.frame_cells() as u128;
        frame.slots[m].word ^= self.state.sp;
        for (j, p) in callee.params[0].iter().enumerate() {
            *self
                .state
                .locations
                .get_mut(&(callee.name.clone(), p.name.clone()))
                .expect("callee param") ^= frame.slots[j].word;
        }
        let id = self
            .ids
            .iter()
            .position(|n| *n == (f.name.clone(), i.lhs[0].clone()))
            .expect("destination id");
        self.stack_xor(self.state.sp + 2, id as u128);
        self.stack_xor(self.state.sp + 1, self.state.fp);
        self.stack_xor(self.state.sp, (k + 1) as u128);
        self.push_pop_locations(callee, self.state.sp)?;
        for (j, a) in args.iter().enumerate() {
            frame.slots[j].word ^= self.read(f, a)?;
        }
        Ok(())
    }
    fn deliver(&mut self, slot: &mut Slot) -> Result<()> {
        let id = self.stack_read(self.state.fp + 2);
        let (f, n) = self
            .ids
            .get(usize::try_from(id).map_err(|_| Error("§3.7: invalid delivery id".into()))?)
            .ok_or_else(|| Error("§3.7: invalid delivery location".into()))?
            .clone();
        self.exchange_location(&self.object.functions[&f], &n, &mut slot.word)
    }
    fn forward_ret(&mut self, f: &Function, i: &Instruction, frame: &mut Frame) -> Result<()> {
        if frame.flag {
            return Ok(());
        }
        frame.succ ^= self.stack_read(self.state.fp) as usize;
        frame.slots[0].word ^= self.read(f, &i.operands[0])?;
        self.push_pop_locations(f, self.state.fp)?;
        self.deliver(&mut frame.slots[0])?;
        frame.slots[1].word ^= self.stack_read(self.state.fp + 1);
        frame.slots[2].word ^= self.state.depth - 1;
        std::mem::swap(&mut frame.slots[1].word, &mut self.state.fp);
        std::mem::swap(&mut frame.slots[2].word, &mut self.state.depth);
        Ok(())
    }
    fn inverse_ret(&mut self, f: &Function, i: &Instruction, frame: &mut Frame) -> Result<()> {
        if frame.flag {
            return Ok(());
        }
        std::mem::swap(&mut frame.slots[2].word, &mut self.state.depth);
        std::mem::swap(&mut frame.slots[1].word, &mut self.state.fp);
        frame.slots[2].word ^= self.state.depth - 1;
        frame.slots[1].word ^= self.stack_read(self.state.fp + 1);
        self.deliver(&mut frame.slots[0])?;
        self.push_pop_locations(f, self.state.fp)?;
        frame.slots[0].word ^= self.read(f, &i.operands[0])?;
        frame.succ ^= self.stack_read(self.state.fp) as usize;
        Ok(())
    }
    fn nested_oracle(&mut self, f: &Function, i: &Instruction) -> Result<()> {
        let a = &i.operands;
        let callee = &self.object.functions[a[0].trim_start_matches('@')];
        let root = &self.object.functions[&self.root];
        let arguments: BTreeMap<_, _> = root.params[4]
            .iter()
            .zip(&self.input.args)
            .map(|(p, a)| (p.name.clone(), a))
            .collect();
        let Some(Argument::Token(budget)) = arguments.get(&a[1]).copied() else {
            return err("§4.2", "nested machine oracle needs token");
        };
        let mut input = OracleInput::bits(
            &list(&a[2])?
                .iter()
                .map(|n| self.read(f, n))
                .collect::<Result<Vec<_>>>()?,
        );
        for (p, n) in callee.params[3].iter().zip(list(&a[5])?) {
            let base = self.state.memory.addresses[&n];
            let Type::Region(aw, _) = p.ty else {
                unreachable!("region")
            };
            let len = usize::try_from(1u128 << aw)
                .map_err(|_| Error("§7.2: nested region too large".into()))?;
            input.regions.insert(
                p.name.clone(),
                (0..len)
                    .map(|j| self.state.memory.byte(base + j as u128))
                    .collect(),
            );
        }
        for n in list(&a[6])? {
            input.args.push(match arguments.get(&n) {
                Some(v) => (*v).clone(),
                None => Argument::Bits(self.read(f, &n)?),
            });
        }
        // A nested invocation is itself a complete compute/commit/reverse
        // permutation. Use the reversible executor recursively as well.
        let mut child = Self::new(self.object, &callee.name, &input, *budget)?;
        for _ in 0..budget.steps {
            child.forward_step()?;
        }
        let outcome = child.outcome();
        for _ in 0..budget.steps {
            child.inverse_step()?;
        }
        if !child.frames_clean() {
            return err("§5.2", "nested oracle left dirty frames");
        }
        *self
            .state
            .locations
            .get_mut(&(f.name.clone(), a[3].clone()))
            .expect("target location") ^= outcome.payload;
        *self
            .state
            .locations
            .get_mut(&(f.name.clone(), a[4].clone()))
            .expect("fault location") ^= outcome.code;
        Ok(())
    }
    fn permutation_call(&mut self, f: &Function, i: &Instruction, inverse: bool) -> Result<()> {
        let a = &i.operands;
        let callee = &self.object.functions[a[0].trim_start_matches('@')];
        let names = list(&a[1])?;
        let mutable = names
            .iter()
            .map(|n| self.read(f, n))
            .collect::<Result<Vec<_>>>()?;
        let inputs = list(&a[2])?
            .iter()
            .map(|n| self.read(f, n))
            .collect::<Result<Vec<_>>>()?;
        let mut regions = BTreeMap::new();
        for (p, n) in callee.params[2].iter().zip(list(&a[3])?) {
            let base = self.state.memory.addresses[&n];
            let Type::Region(aw, _) = p.ty else {
                unreachable!("region")
            };
            let count = usize::try_from(1u128 << aw)
                .map_err(|_| Error("§7.2: action region too large".into()))?;
            regions.insert(
                p.name.clone(),
                (0..count)
                    .map(|j| self.state.memory.byte(base + j as u128))
                    .collect(),
            );
        }
        let root = &self.object.functions[&self.root];
        let arguments: BTreeMap<_, _> = root.params[4]
            .iter()
            .zip(&self.input.args)
            .map(|(p, a)| (p.name.clone(), a))
            .collect();
        let args = list(&a[4])?
            .iter()
            .map(|n| match arguments.get(n) {
                Some(v) => Ok((*v).clone()),
                None => Ok(Argument::Bits(self.read(f, n)?)),
            })
            .collect::<Result<Vec<_>>>()?;
        let values = self.object.permutation_action_values(
            &callee.name,
            &mutable,
            &inputs,
            &regions,
            &args,
            inverse,
        )?;
        for (n, v) in names.iter().zip(values) {
            *self
                .state
                .locations
                .get_mut(&(f.name.clone(), n.clone()))
                .expect("action output") = v;
        }
        Ok(())
    }
}
````

## `src/main.rs` (275 lines)

````rust
use bennett_isa_ref::{
    json::Json, Argument, Budget, Error, Object, OracleInput, OracleMachine, Result, Type,
};

const USAGE:&str="bennett-isa-ref check <object>\nbennett-isa-ref hash <object>\nbennett-isa-ref run-oracle <object> <oracle> --input <x[,y...]> [--budget B[,heap,stack,depth]] [--mem name=hex] [--arg value]\nbennett-isa-ref step-check <object> <oracle> --exhaustive [--budget B[,heap,stack,depth]] [--arg value] [--max-bits N]";
fn fail(message: impl std::fmt::Display) -> Error {
    Error(message.to_string())
}
fn uint(s: &str) -> Result<u128> {
    if let Some(hex) = s.strip_prefix("0x") {
        u128::from_str_radix(hex, 16).map_err(fail)
    } else {
        s.parse().map_err(fail)
    }
}
fn number(n: u128) -> Json {
    if n > 9_007_199_254_740_991 {
        Json::String(n.to_string())
    } else {
        Json::Number(n.to_string())
    }
}
fn string(s: impl Into<String>) -> Json {
    Json::String(s.into())
}
fn object(pairs: impl IntoIterator<Item = (String, Json)>) -> Json {
    Json::Object(pairs.into_iter().collect())
}
fn budget(raw: &str, default: Budget) -> Result<Budget> {
    let v = raw.split(',').map(uint).collect::<Result<Vec<_>>>()?;
    if v.len() != 1 && v.len() != 4 {
        return Err(fail("budget requires B or B,heap,stack,depth (§5.4)"));
    }
    let steps = u64::try_from(v[0]).map_err(fail)?;
    Ok(if v.len() == 1 {
        Budget { steps, ..default }
    } else {
        Budget {
            steps,
            heap: v[1],
            stack: v[2],
            depth: v[3],
        }
    })
}
fn main() {
    if let Err(e) = run() {
        eprintln!("{e}");
        std::process::exit(1);
    }
}
fn run() -> Result<()> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    if args.is_empty() {
        return Err(fail(USAGE));
    }
    if matches!(args[0].as_str(), "--help" | "help") {
        println!("{USAGE}");
        return Ok(());
    }
    let command = args[0].as_str();
    if !["check", "hash", "run-oracle", "step-check"].contains(&command) {
        return Err(fail(format!("unknown subcommand {}\n{USAGE}", args[0])));
    }
    let path = args.get(1).ok_or_else(|| fail(USAGE))?;
    let text = std::fs::read_to_string(path).map_err(|e| fail(format!("{path}: {e}")))?;
    let program = Object::parse(&text)?;
    if matches!(command, "check" | "hash") {
        if args.len() != 2 {
            return Err(fail(USAGE));
        }
        if command == "check" {
            program.check_hashes()?;
        }
        let identity = program.identity()?;
        let symbols = object(identity.interface_hashes.into_iter().map(|(name, hash)| {
            let closure = identity.closure_hashes[&name]
                .clone()
                .map(string)
                .unwrap_or(Json::Null);
            (
                name,
                object([
                    ("closure_hash".into(), closure),
                    ("interface_hash".into(), string(hash)),
                ]),
            )
        }));
        println!(
            "{}",
            object([
                ("object_hash".into(), string(identity.object_hash)),
                ("status".into(), string("ok")),
                ("symbols".into(), symbols)
            ])
            .canonical()
        );
        return Ok(());
    }
    let name = args
        .get(2)
        .ok_or_else(|| fail(USAGE))?
        .trim_start_matches('@');
    let oracle = program
        .functions
        .get(name)
        .filter(|f| f.kind == "oracle")
        .ok_or_else(|| fail(format!("§5.2: unknown oracle @{name}")))?;
    program.check_hashes()?;
    let mut input = OracleInput::default();
    let mut limits = program.default_budget(if command == "step-check" {
        256
    } else {
        1_000_000
    })?;
    let mut exhaustive = false;
    let mut max_bits = 16u16;
    let mut fixed_regions = Vec::new();
    let mut pos = 3;
    while pos < args.len() {
        let option = &args[pos];
        pos += 1;
        if option == "--exhaustive" {
            exhaustive = true;
            continue;
        }
        let value = args
            .get(pos)
            .ok_or_else(|| fail(format!("missing value for {option}")))?;
        pos += 1;
        match option.as_str() {
            "--input" => {
                input.ins = if value.is_empty() {
                    Vec::new()
                } else {
                    value.split(',').map(uint).collect::<Result<_>>()?
                };
            }
            "--budget" => limits = budget(value, limits)?,
            "--max-bits" => max_bits = value.parse().map_err(fail)?,
            "--mem" => {
                let (name, hex) = value
                    .split_once('=')
                    .ok_or_else(|| fail("--mem requires name=hex"))?;
                if hex.len() % 2 != 0 || !hex.bytes().all(|c| c.is_ascii_hexdigit()) {
                    return Err(fail("invalid memory HEX"));
                }
                let bytes = (0..hex.len())
                    .step_by(2)
                    .map(|i| u8::from_str_radix(&hex[i..i + 2], 16).map_err(fail))
                    .collect::<Result<Vec<_>>>()?;
                if input.regions.insert(name.into(), bytes).is_some() {
                    return Err(fail("duplicate --mem region"));
                }
                fixed_regions.push(name.to_string());
            }
            "--arg" => {
                let arg = if let Some(s) = value.strip_prefix("token:") {
                    Argument::Token(budget(s, limits)?)
                } else if let Some(s) = value.strip_prefix("f64:") {
                    Argument::Float(s.parse().map_err(fail)?)
                } else {
                    Argument::Bits(uint(value)?)
                };
                input.args.push(arg);
            }
            _ => return Err(fail(format!("unknown option {option}"))),
        }
    }
    for p in &oracle.params[3] {
        if !input.regions.contains_key(&p.name) {
            let Type::Region(a, _) = p.ty else {
                unreachable!("region type")
            };
            let n = usize::try_from(1u128 << a).map_err(fail)?;
            let mut zero = Vec::new();
            zero.try_reserve_exact(n).map_err(fail)?;
            zero.resize(n, 0);
            input.regions.insert(p.name.clone(), zero);
        }
    }
    if command == "run-oracle" {
        if exhaustive {
            return Err(fail("--exhaustive is a step-check option"));
        }
        let r = program.run_oracle(name, &input, limits)?;
        println!(
            "{}",
            object([
                ("payload".into(), number(r.payload)),
                ("code".into(), number(r.code)),
                ("steps".into(), number(r.steps as u128))
            ])
            .canonical()
        );
        return Ok(());
    }
    if !exhaustive {
        return Err(fail("step-check requires --exhaustive"));
    }
    if max_bits > 24 {
        return Err(fail("--max-bits exceeds the CLI enumeration limit of 24"));
    }
    let input_widths = oracle.params[0]
        .iter()
        .map(|p| p.ty.width(program.ptr_width))
        .collect::<Result<Vec<_>>>()?;
    let mut bits = input_widths.iter().map(|w| *w as u128).sum::<u128>();
    for p in &oracle.params[3] {
        if !fixed_regions.contains(&p.name) {
            let Type::Region(a, w) = p.ty else {
                unreachable!("region type")
            };
            bits = bits
                .checked_add((1u128 << a) * w as u128)
                .ok_or_else(|| fail("domain bit count overflow"))?;
        }
    }
    if bits > max_bits as u128 {
        return Err(fail(format!("§17.13: exhaustive domain has {bits} input/memory bits, above --max-bits {max_bits}; no sampling performed")));
    }
    let cases = 1u128 << (bits as u32);
    for value in 0..cases {
        let mut cursor = 0;
        input.ins.clear();
        for w in &input_widths {
            let mask = if *w == 128 {
                u128::MAX
            } else {
                (1u128 << w) - 1
            };
            input.ins.push((value >> cursor) & mask);
            cursor += *w as u32;
        }
        for p in &oracle.params[3] {
            if !fixed_regions.contains(&p.name) {
                for byte in input.regions.get_mut(&p.name).expect("region initialised") {
                    *byte = ((value >> cursor) & 255) as u8;
                    cursor += 8;
                }
            }
        }
        let expected = program.run_oracle(name, &input, limits)?;
        let mut machine = OracleMachine::new(&program, name, &input, limits)?;
        let before = machine.snapshot();
        for _ in 0..limits.steps {
            machine.forward_step()?;
        }
        if machine.outcome() != expected {
            return Err(fail(format!("§14.3 T6: disagreement at input {value}")));
        }
        for _ in 0..limits.steps {
            machine.inverse_step()?;
        }
        if machine.snapshot() != before || !machine.frames_clean() {
            return Err(fail(format!("§14.3 T2: dirty prefix at input {value}")));
        }
    }
    let fixed = Json::Array(fixed_regions.into_iter().map(string).collect());
    println!(
        "{}",
        object([
            ("cases".into(), number(cases)),
            ("input_and_memory_bits".into(), number(bits)),
            ("fixed_regions".into(), fixed),
            ("status".into(), string("ok")),
            (
                "target_fault".into(),
                string("XOR delivery is independent of their entry values")
            )
        ])
        .canonical()
    );
    Ok(())
}
````

## `src/object.rs` (1509 lines)

````rust
use crate::{err, json::Json, Error, Result};
use std::collections::{BTreeMap, BTreeSet};

pub const SECTIONS: [&str; 9] = [
    "symbols",
    "imports",
    "functions",
    "data",
    "devices",
    "layout",
    "schedule",
    "certificate",
    "coverage",
];

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Type {
    Int(u16),
    Ptr,
    F64,
    Token,
    Qreg(u64),
    Wire(u16),
    Reg(u16),
    Region(u16, u16),
}
impl Type {
    pub fn parse(s: &str) -> Result<Self> {
        let width = |s: &str| -> Result<u16> {
            if !integer(s) || s.starts_with('-') {
                return err("§3.3", "width must use canonical unsigned INT");
            }
            let n = s
                .parse::<u16>()
                .map_err(|_| Error(format!("§3.3: invalid width {s}")))?;
            if !(1..=128).contains(&n) {
                return err("§3.3", "width outside 1..128");
            }
            Ok(n)
        };
        let bundle_width=|s:&str|->Result<u16>{if !integer(s)||s.starts_with('-'){return err("§3.3","bundle width requires canonical positive INT");}let n=s.parse::<u16>().map_err(|_|Error("§3.3: bundle width exceeds host descriptor range".into()))?;if n==0{return err("§3.3","bundle width must be positive");}Ok(n)};
        Ok(match s {
            "ptr" => Self::Ptr,
            "f64" => Self::F64,
            "token" => Self::Token,
            "wire" => Self::Wire(1),
            _ if s.starts_with("i") => Self::Int(width(&s[1..])?),
            _ if s.starts_with("wire[") && s.ends_with(']') => {
                Self::Wire(bundle_width(&s[5..s.len() - 1])?)
            }
            _ if s.starts_with("reg[") && s.ends_with(']') => Self::Reg(width(&s[4..s.len() - 1])?),
            _ if s.starts_with("qreg[") && s.ends_with(']') => Self::Qreg(
                s[5..s.len() - 1]
                    .parse()
                    .map_err(|_| Error("§3.3: invalid qreg size".into()))?,
            ),
            _ if s.starts_with("region[") && s.ends_with(']') => {
                let (a, w) = s[7..s.len() - 1]
                    .split_once(',')
                    .ok_or_else(|| Error("§3.3: malformed region type".into()))?;
                let a = a
                    .parse()
                    .map_err(|_| Error("§3.3: invalid address width".into()))?;
                if a > 127 {
                    return err("§3.3", "region address width exceeds 127");
                }
                Self::Region(a, bundle_width(w)?)
            }
            _ => return err("§3.3", format!("unknown type {s}")),
        })
    }
    pub fn width(&self, ptr: u16) -> Result<u16> {
        match self {
            Self::Int(n) | Self::Wire(n) | Self::Reg(n) => Ok(*n),
            Self::Ptr => Ok(ptr),
            _ => err("§3.3", "expected bit-vector type"),
        }
    }
    pub fn text(&self) -> String {
        match self {
            Self::Int(n) => format!("i{n}"),
            Self::Wire(n) => format!("wire[{n}]"),
            Self::Reg(n) => format!("reg[{n}]"),
            Self::Region(a, w) => format!("region[{a},{w}]"),
            Self::Qreg(n) => format!("qreg[{n}]"),
            Self::Ptr => "ptr".into(),
            Self::F64 => "f64".into(),
            Self::Token => "token".into(),
        }
    }
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Param {
    pub name: String,
    pub ty: Type,
    pub role: Option<String>,
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Instruction {
    pub lhs: Vec<String>,
    pub op: String,
    pub operands: Vec<String>,
    pub bodies: Vec<Vec<Instruction>>,
    pub line: usize,
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Block {
    pub name: String,
    pub params: Vec<Param>,
    pub instructions: Vec<Instruction>,
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Function {
    pub kind: String,
    pub name: String,
    pub params: [Vec<Param>; 5],
    pub regs: Vec<Param>,
    pub bounds: Vec<u64>,
    pub blocks: Vec<Block>,
    pub lines: Vec<String>,
}
impl Function {
    /// An imported declaration has the same operand schema as a definition.
    /// Its synthetic parameter names are local to validation, never executable.
    pub(crate) fn from_signature(name: &str, signature: &Json) -> Result<Self> {
        let kind = signature.get("kind")?.string()?;
        let fields: &[&str] = match kind {
            "oracle" => &["abi", "tier", "kind", "in", "tgt", "fault", "mem", "args"],
            "action" | "perm_action" => {
                &["abi", "tier", "kind", "mut", "in", "mem", "args", "bounds"]
            }
            "lproc" => &["abi", "tier", "kind", "params", "result"],
            "cc" | "r" => &["abi", "tier", "kind", "params", "results"],
            _ => return err("§9.1", "unknown function signature kind"),
        };
        signature.fields(fields, &[])?;
        let mut f = Self {
            kind: kind.into(),
            name: name.into(),
            params: Default::default(),
            regs: Vec::new(),
            bounds: Vec::new(),
            blocks: Vec::new(),
            lines: Vec::new(),
        };
        let widths = |key: &str, reg: bool, role: Option<&str>| -> Result<Vec<Param>> {
            signature
                .get(key)?
                .array()?
                .iter()
                .enumerate()
                .map(|(i, v)| {
                    let w = v.uint()?;
                    let ty = Type::parse(&format!("{}[{w}]", if reg { "reg" } else { "wire" }))?;
                    Ok(Param {
                        name: format!("{key}_{i}"),
                        ty,
                        role: role.map(str::to_string),
                    })
                })
                .collect()
        };
        let scalar = |key: &str, reg: bool| -> Result<Vec<Param>> {
            let w = signature.get(key)?.uint()?;
            Ok(vec![Param {
                name: key.into(),
                ty: Type::parse(&format!("{}[{w}]", if reg { "reg" } else { "wire" }))?,
                role: None,
            }])
        };
        let types = |key: &str| -> Result<Vec<Param>> {
            signature
                .get(key)?
                .array()?
                .iter()
                .enumerate()
                .map(|(i, v)| {
                    Ok(Param {
                        name: format!("{key}_{i}"),
                        ty: Type::parse(v.string()?)?,
                        role: None,
                    })
                })
                .collect()
        };
        let memory = || -> Result<Vec<Param>> {
            signature
                .get("mem")?
                .array()?
                .iter()
                .enumerate()
                .map(|(i, v)| {
                    v.fields(&["A", "W", "role"], &[])?;
                    let a = v.get("A")?.uint()?;
                    let w = v.get("W")?.uint()?;
                    let role = v.get("role")?.string()?;
                    if !["in", "mut"].contains(&role) {
                        return err("§5.1", "invalid interface region role");
                    }
                    Ok(Param {
                        name: format!("mem_{i}"),
                        ty: Type::parse(&format!("region[{a},{w}]"))?,
                        role: Some(role.into()),
                    })
                })
                .collect()
        };
        match kind {
            "oracle" => {
                f.params[0] = widths("in", false, Some("in"))?;
                f.params[1] = scalar("tgt", false)?;
                f.params[2] = scalar("fault", false)?;
                f.params[3] = memory()?;
                f.params[4] = types("args")?;
            }
            "action" | "perm_action" => {
                f.params[0] = widths("mut", false, Some("mut"))?;
                f.params[1] = widths("in", false, Some("in"))?;
                f.params[2] = memory()?;
                f.params[3] = types("args")?;
                f.bounds = signature
                    .get("bounds")?
                    .array()?
                    .iter()
                    .map(|n| {
                        u64::try_from(n.uint()?).map_err(|_| {
                            Error("§5.3: loop bound exceeds implementation counter".into())
                        })
                    })
                    .collect::<Result<_>>()?;
            }
            "lproc" => {
                f.params[0] = widths("params", true, None)?;
                f.params[1] = scalar("result", true)?;
            }
            _ => {
                f.params[0] = types("params")?;
                f.params[1] = types("results")?;
            }
        }
        validate_header(&f)?;
        if &f.signature() != signature {
            return err(
                "§9.1",
                "invalid signature version, tier, or field representation",
            );
        }
        Ok(f)
    }
    pub fn locations(&self) -> Vec<&Param> {
        let mut out = Vec::new();
        if self.kind == "lproc" {
            out.extend(&self.params[0]);
            out.extend(&self.params[1]);
        }
        out.extend(&self.regs);
        out
    }
    pub fn frame_cells(&self) -> usize {
        3 + self.locations().len()
    }
    pub fn instructions(&self) -> impl Iterator<Item = &Instruction> {
        self.blocks.iter().flat_map(|b| &b.instructions)
    }
    pub fn signature(&self) -> Json {
        let widths = |p: &[Param]| {
            Json::Array(
                p.iter()
                    .map(|p| {
                        Json::Number(match &p.ty {
                            Type::Wire(n) | Type::Reg(n) => n.to_string(),
                            _ => "0".into(),
                        })
                    })
                    .collect(),
            )
        };
        let types =
            |p: &[Param]| Json::Array(p.iter().map(|p| Json::String(p.ty.text())).collect());
        let mem = |p: &[Param]| {
            Json::Array(
                p.iter()
                    .map(|p| {
                        let (a, w) = match p.ty {
                            Type::Region(a, w) => (a, w),
                            _ => (0, 0),
                        };
                        Json::Object(
                            [
                                ("A".into(), Json::Number(a.to_string())),
                                ("W".into(), Json::Number(w.to_string())),
                                (
                                    "role".into(),
                                    Json::String(p.role.clone().unwrap_or_default()),
                                ),
                            ]
                            .into(),
                        )
                    })
                    .collect(),
            )
        };
        let mut m = BTreeMap::from([
            ("abi".into(), Json::String("0.8".into())),
            ("kind".into(), Json::String(self.kind.clone())),
            (
                "tier".into(),
                Json::String(if matches!(self.kind.as_str(), "cc" | "r") {
                    self.kind.clone()
                } else {
                    "q".into()
                }),
            ),
        ]);
        match self.kind.as_str() {
            "oracle" => {
                m.insert("in".into(), widths(&self.params[0]));
                m.insert(
                    "tgt".into(),
                    widths(&self.params[1]).array().expect("array")[0].clone(),
                );
                m.insert(
                    "fault".into(),
                    widths(&self.params[2]).array().expect("array")[0].clone(),
                );
                m.insert("mem".into(), mem(&self.params[3]));
                m.insert("args".into(), types(&self.params[4]));
            }
            "lproc" => {
                m.insert("params".into(), widths(&self.params[0]));
                m.insert(
                    "result".into(),
                    widths(&self.params[1]).array().expect("array")[0].clone(),
                );
            }
            "action" | "perm_action" => {
                m.insert("mut".into(), widths(&self.params[0]));
                m.insert("in".into(), widths(&self.params[1]));
                m.insert("mem".into(), mem(&self.params[2]));
                m.insert("args".into(), types(&self.params[3]));
                m.insert(
                    "bounds".into(),
                    Json::Array(
                        self.bounds
                            .iter()
                            .map(|n| Json::Number(n.to_string()))
                            .collect(),
                    ),
                );
            }
            _ => {
                m.insert("params".into(), types(&self.params[0]));
                m.insert("results".into(), types(&self.params[1]));
            }
        }
        Json::Object(m)
    }
}

#[derive(Clone, Debug)]
pub struct Object {
    pub text: String,
    pub ptr_width: u16,
    pub metadata: BTreeMap<String, Json>,
    pub functions: BTreeMap<String, Function>,
    pub function_order: Vec<String>,
    pub data: BTreeMap<String, Vec<u8>>,
}

pub(crate) fn name(s: &str) -> bool {
    let mut b = s.bytes();
    matches!(b.next(), Some(b'A'..=b'Z' | b'a'..=b'z' | b'_'))
        && b.all(|b| b.is_ascii_alphanumeric() || b == b'_' || b == b'.')
}
pub(crate) fn integer(s: &str) -> bool {
    let s = s.strip_prefix('-').unwrap_or(s);
    s == "0" || (!s.starts_with('0') && !s.is_empty() && s.bytes().all(|b| b.is_ascii_digit()))
}
pub(crate) fn list(s: &str) -> Result<Vec<String>> {
    let s = s
        .strip_prefix('(')
        .and_then(|s| s.strip_suffix(')'))
        .ok_or_else(|| Error(format!("§16.2: expected operand list {s}")))?;
    if s.is_empty() {
        return Ok(Vec::new());
    }
    let v: Vec<_> = s.split(", ").map(str::to_string).collect();
    if v.iter().any(|s| !name(s)) {
        return err(
            "§16.2",
            "operand lists require names separated by comma and space",
        );
    }
    Ok(v)
}
fn params(s: &str) -> Result<Vec<Param>> {
    if s.is_empty() {
        return Ok(Vec::new());
    }
    let mut seen = BTreeSet::new();
    let mut out = Vec::new();
    for p in s.split(", ") {
        let (n, rest) = p
            .split_once(':')
            .ok_or_else(|| Error(format!("§16.2: invalid parameter {p}")))?;
        if !name(n) || !seen.insert(n) {
            return err("§16.2", "invalid or duplicate parameter name");
        }
        let (t, role) = match rest.split_once(' ') {
            Some((t, r)) if matches!(r, "in" | "mut") => (t, Some(r.to_string())),
            Some(_) => return err("§16.2", "invalid parameter role"),
            None => (rest, None),
        };
        out.push(Param {
            name: n.into(),
            ty: Type::parse(t)?,
            role,
        });
    }
    Ok(out)
}

/// Split instruction operands without splitting tuple or string operands.
pub(crate) fn tokens(s: &str) -> Result<Vec<String>> {
    let mut out = Vec::new();
    let mut start = 0;
    let mut nesting = 0;
    let mut quoted = false;
    let mut escaped = false;
    for (i, c) in s.char_indices() {
        if quoted {
            if escaped {
                escaped = false;
            } else if c == '\\' {
                escaped = true;
            } else if c == '"' {
                quoted = false;
            }
            continue;
        }
        match c {
            '"' => quoted = true,
            '(' => nesting += 1,
            ')' => {
                nesting -= 1;
                if nesting < 0 {
                    return err("§16.2", "unmatched close parenthesis");
                }
            }
            ' ' if nesting == 0 => {
                if start == i {
                    return err("§16.1", "multiple spaces between tokens");
                }
                out.push(s[start..i].into());
                start = i + 1;
            }
            _ => {}
        }
    }
    if quoted || nesting != 0 {
        return err("§16.2", "unterminated operand");
    }
    if start < s.len() {
        out.push(s[start..].into());
    } else if !s.is_empty() {
        return err("§16.1", "trailing space");
    }
    Ok(out)
}
fn instruction(lines: &[(usize, &str)], pos: &mut usize) -> Result<Instruction> {
    let (line, raw) = lines[*pos];
    *pos += 1;
    let (lhs, rhs) = if let Some((a, b)) = raw.split_once(" = ") {
        let lhs = if a.starts_with('(') {
            list(a)?
        } else if name(a) {
            vec![a.into()]
        } else {
            return err("§16.2", "invalid result list");
        };
        (lhs, b)
    } else {
        (Vec::new(), raw)
    };
    let ts = tokens(rhs)?;
    if ts.is_empty() {
        return err("§16.2", "empty instruction");
    }
    let mut ins = Instruction {
        lhs,
        op: ts[0].clone(),
        operands: ts[1..].to_vec(),
        bodies: Vec::new(),
        line,
    };
    if ins.operands.last().is_some_and(|s| s == "{") {
        ins.operands.pop();
        loop {
            let mut body = Vec::new();
            while *pos < lines.len() && !lines[*pos].1.starts_with('}') {
                body.push(instruction(lines, pos)?);
            }
            if body.is_empty() || *pos == lines.len() {
                return err("§16.2", "empty or unterminated structured body");
            }
            let close = lines[*pos].1;
            *pos += 1;
            ins.bodies.push(body);
            match close {
                "}" => break,
                "} {" if ins.bodies.len() == 1 => {}
                _ => return err("§16.2", "invalid structured body close"),
            }
        }
    }
    Ok(ins)
}

impl Object {
    pub(crate) fn declaration(&self, name: &str) -> Result<Function> {
        if let Some(f) = self.functions.get(name) {
            return Ok(f.clone());
        }
        let import = self
            .section("imports")
            .and_then(|s| s.object().ok())
            .and_then(|s| s.get(name))
            .ok_or_else(|| Error(format!("§9.3: undefined symbol @{name}")))?;
        Function::from_signature(name, import.get("signature")?)
    }
    pub(crate) fn data_size(&self,name:&str)->Result<u128>{
        if let Some(bytes)=self.data.get(name){return Ok(bytes.len()as u128);}
        let import=self.section("imports").and_then(|v|v.object().ok()).and_then(|v|v.get(name)).ok_or_else(||Error(format!("§9.3: unknown data symbol @{name}")))?;
        let sig=import.get("signature")?;if sig.get("kind")?.string()?!="data"{return err("§4.6","qregion image reference must have data kind");}sig.get("size")?.uint()
    }
    pub(crate) fn ensure_linked(&self)->Result<()>{if self.section("imports").map(|s|s.object().map(|s|!s.is_empty())).transpose()?.unwrap_or(false){return err("§9.3","object has unresolved imports; link before execution");}Ok(())}
    pub fn parse(text: &str) -> Result<Self> {
        if !text.ends_with('\n') || text.contains('\r') || text.contains('\t') {
            return err(
                "§16.1",
                "object requires LF lines, no tabs or trailing spaces, and final LF",
            );
        }
        let mut data_section = false;
        for line in text.lines() {
            if let Some(section) = line.strip_prefix("section ") {
                data_section = section == "data";
            }
            if line.ends_with(' ') && !(data_section && line.strip_suffix(' ').is_some_and(name)) {
                return err("§16.1", "trailing space outside an empty HEX data line");
            }
        }
        let lines: Vec<_> = text.lines().collect();
        let header = tokens(lines.first().copied().unwrap_or(""))?;
        if header.len() != 9 || header[0] != "bennett-object" {
            return err("§16.2", "malformed object header");
        }
        for (i, k) in [
            "isa", "object", "launch", "sched", "cert", "coverage", "target",
        ]
        .iter()
        .enumerate()
        {
            if header[i + 1] != format!("{k}=0.8") {
                return err("§1", format!("expected {k}=0.8"));
            }
        }
        let ptr_width = header[8]
            .strip_prefix("ptr_width=")
            .and_then(|s| s.parse::<u16>().ok())
            .ok_or_else(|| Error("§16.2: invalid ptr_width".into()))?;
        if !(1..=128).contains(&ptr_width) {
            return err("§3.3", "pointer width outside 1..128");
        }
        let mut obj = Object {
            text: text.into(),
            ptr_width,
            metadata: BTreeMap::new(),
            functions: BTreeMap::new(),
            function_order: Vec::new(),
            data: BTreeMap::new(),
        };
        let mut pos = 1;
        let mut previous = None;
        while pos < lines.len() {
            if !lines[pos].is_empty()
                || pos + 1 >= lines.len()
                || !lines[pos + 1].starts_with("section ")
            {
                return err(
                    "§16.1",
                    format!(
                        "exactly one blank required before section at line {}",
                        pos + 1
                    ),
                );
            }
            pos += 1;
            let section = &lines[pos][8..];
            pos += 1;
            let order = SECTIONS
                .iter()
                .position(|s| *s == section)
                .ok_or_else(|| Error(format!("§9.1: unknown section {section}")))?;
            if previous.is_some_and(|n| n >= order) {
                return err("§9.1", "duplicate or out-of-order section");
            }
            previous = Some(order);
            let start = pos;
            while pos < lines.len() && !lines[pos].is_empty() {
                if lines[pos].starts_with("section ") {
                    return err("§16.1", "missing blank line before section");
                }
                pos += 1;
            }
            if pos < lines.len()
                && (pos + 1 == lines.len() || !lines[pos + 1].starts_with("section "))
            {
                return err("§16.1", "blank line outside section boundary");
            }
            match section {
                "functions" => obj.parse_functions(&lines[start..pos], start + 1)?,
                "data" => {
                    for line in &lines[start..pos] {
                        let t = if let Some(n) = line.strip_suffix(' ').filter(|n| name(n)) {
                            vec![n.to_string(), String::new()]
                        } else {
                            tokens(line)?
                        };
                        // Empty data images have an empty HEX token, represented by NAME SP.
                        if t.len() != 2
                            || !name(&t[0])
                            || t[1].len() % 2 != 0
                            || !t[1]
                                .bytes()
                                .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
                        {
                            return err("§16.2", "invalid data line");
                        }
                        let bytes = (0..t[1].len())
                            .step_by(2)
                            .map(|i| u8::from_str_radix(&t[1][i..i + 2], 16).expect("hex checked"))
                            .collect();
                        if obj.data.insert(t[0].clone(), bytes).is_some() {
                            return err("§9.1", "duplicate data name");
                        }
                    }
                }
                _ => {
                    if pos - start != 1 {
                        return err(
                            "§9.1",
                            format!("section {section} requires one JSON object line"),
                        );
                    }
                    let v = Json::parse(lines[start])?;
                    v.object()?;
                    if v.canonical() != lines[start] {
                        return err(
                            "§16.1",
                            format!("section {section} is not RFC 8785 canonical"),
                        );
                    }
                    obj.metadata.insert(section.into(), v);
                }
            }
        }
        obj.validate()?;
        Ok(obj)
    }
    fn parse_functions(&mut self, lines: &[&str], base: usize) -> Result<()> {
        let mut pos = 0;
        while pos < lines.len() {
            let start = pos;
            let ts = tokens(lines[pos])?;
            pos += 1;
            let (kind, offset) = if ts.first().is_some_and(|s| s == "fn") {
                (ts.get(1).map(String::as_str).unwrap_or(""), 2)
            } else {
                (ts.first().map(String::as_str).unwrap_or(""), 1)
            };
            if !matches!(
                kind,
                "cc" | "r" | "oracle" | "action" | "perm_action" | "lproc"
            ) || ts.len() != offset + 6
            {
                return err(
                    "§16.2",
                    "invalid function header or number of parameter lists",
                );
            }
            let n = ts[offset]
                .strip_prefix('@')
                .filter(|s| name(s))
                .ok_or_else(|| Error("§16.2: invalid function name".into()))?;
            let mut ps: [Vec<Param>; 5] = Default::default();
            for (i, s) in ts[offset + 1..].iter().enumerate() {
                let inner = s
                    .strip_prefix('(')
                    .and_then(|s| s.strip_suffix(')'))
                    .ok_or_else(|| Error("§16.2: invalid parameter list".into()))?;
                ps[i] = params(inner)?;
            }
            let mut f = Function {
                kind: kind.into(),
                name: n.into(),
                params: ps,
                regs: Vec::new(),
                bounds: Vec::new(),
                blocks: Vec::new(),
                lines: Vec::new(),
            };
            if pos < lines.len() && lines[pos].starts_with("regs ") {
                let body = lines[pos]
                    .strip_prefix("regs { ")
                    .ok_or_else(|| Error("§16.2: malformed regs".into()))?;
                let (rs, rest) = body
                    .split_once(" }")
                    .ok_or_else(|| Error("§16.2: malformed regs close".into()))?;
                f.regs = params(rs)?;
                if !rest.is_empty() {
                    let bs = rest
                        .strip_prefix(" bounds {")
                        .and_then(|s| s.strip_suffix('}'))
                        .ok_or_else(|| Error("§16.2: malformed bounds".into()))?;
                    if !bs.is_empty() {
                        f.bounds = bs
                            .split(", ")
                            .map(|s| {
                                s.parse::<u64>()
                                    .map_err(|_| Error("§16.2: invalid loop bound".into()))
                            })
                            .collect::<Result<_>>()?;
                    }
                }
                pos += 1;
            }
            while pos < lines.len() && lines[pos].starts_with('^') {
                let b = lines[pos];
                pos += 1;
                let (bn, ps) = b[1..]
                    .split_once('(')
                    .ok_or_else(|| Error("§16.2: malformed block".into()))?;
                if !name(bn) {
                    return err("§16.2", "invalid block name");
                }
                let ps = ps
                    .strip_suffix("):")
                    .ok_or_else(|| Error("§16.2: malformed block parameter list".into()))?;
                let mut block = Block {
                    name: bn.into(),
                    params: params(ps)?,
                    instructions: Vec::new(),
                };
                let end = (pos..lines.len())
                    .find(|i| lines[*i].starts_with('^') || is_head(lines[*i]))
                    .unwrap_or(lines.len());
                let numbered: Vec<_> = lines[pos..end]
                    .iter()
                    .enumerate()
                    .map(|(i, s)| (base + pos + i, *s))
                    .collect();
                let mut ip = 0;
                while ip < numbered.len() {
                    block.instructions.push(instruction(&numbered, &mut ip)?);
                }
                if block.instructions.is_empty() {
                    return err("§16.2", "empty block");
                }
                f.blocks.push(block);
                pos = end;
            }
            if f.blocks.is_empty() {
                return err("§16.2", "function requires blocks");
            }
            f.lines = lines[start..pos].iter().map(|s| s.to_string()).collect();
            self.function_order.push(n.into());
            if self.functions.insert(n.into(), f).is_some() {
                return err("§9.1", "duplicate function name");
            }
        }
        Ok(())
    }
    pub fn section(&self, key: &str) -> Option<&Json> {
        self.metadata.get(key)
    }
    pub fn symbols(&self) -> Result<&BTreeMap<String, Json>> {
        self.metadata
            .get("symbols")
            .ok_or_else(|| Error("§9.1: missing symbols section".into()))?
            .object()
    }
    fn validate(&self) -> Result<()> {
        self.validate_symbols()?;
        for f in self.functions.values() {
            self.validate_function(f)?;
        }
        self.validate_layout()?;
        self.validate_metadata()?;
        self.validate_call_graph()?;
        Ok(())
    }
    fn validate_symbols(&self) -> Result<()> {
        let mut names = BTreeSet::new();
        for (index, s) in self.symbols()? {
            if !integer(index) || index.starts_with('-') {
                return err("§9.1", "invalid local symbol index");
            }
            s.fields(&["name", "kind", "signature", "interface_hash"], &[])?;
            let n = s.get("name")?.string()?;
            let k = s.get("kind")?.string()?;
            if !name(n) || !names.insert(n) {
                return err("§9.1", "invalid or duplicate symbol name");
            }
            let h = s.get("interface_hash")?.string()?;
            if h.len() != 64
                || !h
                    .bytes()
                    .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
            {
                return err("§9.2", "interface_hash must be 64 lowercase hex digits");
            }
            let sig = s.get("signature")?;
            if k == "data" {
                sig.fields(&["abi", "kind", "size", "tier"], &[])?;
                if sig.get("kind")?.string()? != "data"
                    || sig.get("tier")?.string()? != "-"
                    || sig.get("abi")?.string()? != "0.8"
                {
                    return err("§9.1", "invalid data signature");
                }
                let bytes = self
                    .data
                    .get(n)
                    .ok_or_else(|| Error(format!("§9.1: missing data definition {n}")))?;
                if sig.get("size")?.uint()? != bytes.len() as u128 {
                    return err("§7.2", "data size differs from signature");
                }
            } else {
                let f = self
                    .functions
                    .get(n)
                    .ok_or_else(|| Error(format!("§9.1: missing function definition {n}")))?;
                validate_header(f)?;
                if k != f.kind || sig != &f.signature() {
                    return err("§9.1", format!("signature mismatch for {n}"));
                }
            }
        }
        if self
            .functions
            .keys()
            .chain(self.data.keys())
            .any(|n| !names.contains(n.as_str()))
        {
            return err("§9.1", "definition without symbol");
        }
        if let Some(imports) = self.section("imports") {
            for (n, im) in imports.object()? {
                if !name(n) || names.contains(n.as_str()) {
                    return err(
                        "§9.3",
                        "invalid import name or import conflicts with definition",
                    );
                }
                im.fields(&["signature"], &["pinned_closure_hash"])?;
                let signature = im.get("signature")?;
                if signature.get("kind")?.string()? == "data" {
                    signature.fields(&["abi", "tier", "kind", "size"], &[])?;
                    if signature.get("abi")?.string()? != "0.8"
                        || signature.get("tier")?.string()? != "-"
                    {
                        return err("§9.1", "invalid imported data signature");
                    }
                    signature.get("size")?.uint()?;
                } else {
                    Function::from_signature(n, signature)?;
                }
                if let Some(p) = im.object()?.get("pinned_closure_hash") {
                    let h = p.string()?;
                    if h.len() != 64
                        || !h
                            .bytes()
                            .all(|b| b.is_ascii_hexdigit() && !b.is_ascii_uppercase())
                    {
                        return err("§9.3", "invalid pinned hash");
                    }
                }
            }
        }
        Ok(())
    }
    fn validate_function(&self, f: &Function) -> Result<()> {
        let lifted = matches!(f.kind.as_str(), "oracle" | "lproc");
        let mut types = BTreeMap::new();
        for p in f
            .params
            .iter()
            .enumerate()
            .filter(|(i, _)| !matches!(f.kind.as_str(), "cc" | "r") || *i == 0)
            .flat_map(|(_, ps)| ps)
            .chain(&f.regs)
        {
            if types.insert(p.name.clone(), p.ty.clone()).is_some() {
                return err("§3.7", "duplicate function location or parameter");
            }
        }
        let mut labels = BTreeSet::new();
        for b in &f.blocks {
            if !labels.insert(&b.name) {
                return err("§3.6", "duplicate block label");
            }
            if lifted && !b.params.is_empty() {
                return err("§3.7", "lifted blocks have no parameters");
            }
        }
        if lifted {
            for b in &f.blocks {
                for (i, ins) in b.instructions.iter().enumerate() {
                    let term = matches!(
                        ins.op.as_str(),
                        "qjump" | "qbranch" | "qjumpr" | "lift.ret" | "lift.retval" | "fault"
                    );
                    if term != (i + 1 == b.instructions.len()) {
                        return err(
                            "§3.6",
                            format!("block {} must end in exactly one terminator", b.name),
                        );
                    }
                    self.validate_row(f, ins, &types, &labels)?;
                }
            }
            self.validate_matched_oracle_calls(f)?;
        } else {
            self.validate_structured(f, &mut types, &labels)?;
        }
        Ok(())
    }
    fn index_space_size(&self, containing: &Function) -> Result<u128> {
        let mut maximum = containing.instructions().count() as u128;
        for oracle in self.functions.values().filter(|f| f.kind == "oracle") {
            let mut pending = vec![oracle.name.clone()];
            let mut seen = BTreeSet::new();
            let mut count = 0u128;
            while let Some(name) = pending.pop() {
                if !seen.insert(name.clone()) {
                    continue;
                }
                let function = self.declaration(&name)?;
                count += function.instructions().count() as u128;
                for call in function.instructions().filter(|i| i.op == "lift.call") {
                    let target = call
                        .operands
                        .first()
                        .and_then(|n| n.strip_prefix('@'))
                        .ok_or_else(|| Error("§4.8: malformed lift.call".into()))?;
                    pending.push(target.to_string());
                }
            }
            if seen.contains(&containing.name) {
                maximum = maximum.max(count);
            }
        }
        Ok(maximum)
    }
    fn fault_width(&self,containing:&Function)->Result<u16>{
        if containing.kind=="oracle"{return containing.params[2][0].ty.width(self.ptr_width);}
        let mut width=128;
        for oracle in self.functions.values().filter(|f|f.kind=="oracle"){
            let mut pending=vec![oracle.name.clone()];let mut seen=BTreeSet::new();
            while let Some(name)=pending.pop(){if !seen.insert(name.clone()){continue;}let f=self.declaration(&name)?;for call in f.instructions().filter(|i|i.op=="lift.call"){let target=call.operands.first().and_then(|s|s.strip_prefix('@')).ok_or_else(||Error("§4.8: malformed lift.call".into()))?;pending.push(target.into());}}
            if seen.contains(&containing.name){width=width.min(oracle.params[2][0].ty.width(self.ptr_width)?);}
        }Ok(width)
    }
    fn validate_row(
        &self,
        f: &Function,
        i: &Instruction,
        types: &BTreeMap<String, Type>,
        labels: &BTreeSet<&String>,
    ) -> Result<()> {
        let op = i.op.as_str();
        let args = &i.operands;
        if !i.bodies.is_empty() {
            return err("§4.8", "structured instructions are not lifted rows");
        }
        let rd = |n: &str| -> Result<u16> {
            let p = if f.kind == "oracle" {
                f.regs
                    .iter()
                    .chain(&f.params[0])
                    .chain(&f.params[4])
                    .find(|p| p.name == n)
            } else {
                f.params[0]
                    .iter()
                    .chain(&f.params[1])
                    .chain(&f.regs)
                    .find(|p| p.name == n)
            };
            p.ok_or_else(|| Error(format!("§3.7: unreadable location {n}")))?
                .ty
                .width(self.ptr_width)
        };
        let dest = |n: &str| -> Result<u16> {
            if !f.locations().iter().any(|p| p.name == n) {
                return err("§3.7", format!("not a writable location: {n}"));
            }
            types[n].width(self.ptr_width)
        };
        let arity = |n: usize, lhs: usize| -> Result<()> {
            if args.len() != n || i.lhs.len() != lhs {
                err(
                    "§4.8",
                    format!(
                        "{} expects {lhs} results and {n} operands at line {}",
                        op, i.line
                    ),
                )
            } else {
                Ok(())
            }
        };
        let eq = |a: u16, b: u16| -> Result<()> {
            if a != b {
                err("§3.3", format!("width mismatch in {op}: {a} != {b}"))
            } else {
                Ok(())
            }
        };
        let label = |s: &str| -> Result<()> {
            if s.strip_prefix('^')
                .is_none_or(|s| !labels.iter().any(|x| x.as_str() == s))
            {
                err("§3.6", format!("unknown label {s}"))
            } else {
                Ok(())
            }
        };
        let addr = |s: &str| -> Result<()> { eq(rd(s)?, self.ptr_width) };
        let length = |s: &str| -> Result<()> {
            if integer(s) {
                let n = s
                    .parse::<u128>()
                    .map_err(|_| Error("§3.3: invalid length".into()))?;
                if self.ptr_width < 128 && n >= 1u128 << self.ptr_width {
                    return err("§3.3", "length does not fit pointer");
                }
                Ok(())
            } else {
                rd(s).map(|_| ())
            }
        };
        let code = |s: &str| -> Result<()> {
            let n = s
                .parse::<u128>()
                .map_err(|_| Error("§3.3: fault code requires nonnegative literal".into()))?;
            let fw = self.fault_width(f)?;
            if fw < 128 && n >= 1u128 << fw {
                return err("§3.3", "fault code does not fit fault register");
            }
            Ok(())
        };
        if let Some(n) = op.strip_prefix("lift.const.i") {
            arity(1, 1)?;
            let w = Type::parse(&format!("i{n}"))?.width(self.ptr_width)?;
            eq(dest(&i.lhs[0])?, w)?;
            if !integer(&args[0]) || parse_bits(&args[0], w).is_err() {
                return err("§16.1", "invalid integer literal");
            }
        } else if let Some(base) = op
            .strip_prefix("lift.")
            .filter(|s| is_binop(s) || is_div(s))
        {
            let _ = base;
            arity(2, 1)?;
            eq(rd(&args[0])?, rd(&args[1])?)?;
            eq(dest(&i.lhs[0])?, rd(&args[0])?)?;
        } else if let Some(pred) = op.strip_prefix("lift.icmp.") {
            arity(2, 1)?;
            if !["eq", "ne", "ult", "ule", "slt", "sle"].contains(&pred) {
                return err("§4.8", "unknown comparison predicate");
            }
            eq(rd(&args[0])?, rd(&args[1])?)?;
            eq(dest(&i.lhs[0])?, 1)?;
        } else if op == "lift.select" {
            arity(3, 1)?;
            eq(rd(&args[0])?, 1)?;
            eq(rd(&args[1])?, rd(&args[2])?)?;
            eq(dest(&i.lhs[0])?, rd(&args[1])?)?;
        } else if let Some((cast, n)) = op
            .strip_prefix("lift.")
            .and_then(|s| s.split_once(".i"))
            .filter(|(c, _)| ["zext", "sext", "trunc"].contains(c))
        {
            arity(1, 1)?;
            let out = Type::parse(&format!("i{n}"))?.width(self.ptr_width)?;
            eq(dest(&i.lhs[0])?, out)?;
            let input = rd(&args[0])?;
            if if cast == "trunc" {
                out >= input
            } else {
                out <= input
            } {
                return err("§3.3", "cast has wrong width direction");
            }
        } else {
            match op {
                "lift.mov" => {
                    arity(1, 1)?;
                    eq(dest(&i.lhs[0])?, rd(&args[0])?)?;
                }
                "lift.parmov" => {
                    if args.len() != 1 {
                        return err("§4.8", "parmov needs one source tuple");
                    }
                    let src = list(&args[0])?;
                    if src.len() != i.lhs.len() || src.is_empty() {
                        return err("§4.8", "parmov source/destination arity");
                    }
                    let mut seen = BTreeSet::new();
                    for (d, s) in i.lhs.iter().zip(src) {
                        if !seen.insert(d) {
                            return err("§3.3", "parmov destinations alias");
                        }
                        eq(dest(d)?, rd(&s)?)?;
                    }
                }
                "lift.label" => {
                    arity(1, 1)?;
                    label(&args[0])?;
                    let w = dest(&i.lhs[0])?;
                    if w < 128 && (1u128 << w) <= self.index_space_size(f)? {
                        return err("§3.3", "label location cannot represent index space");
                    }
                }
                "lift.addr" => {
                    arity(1, 1)?;
                    eq(dest(&i.lhs[0])?, self.ptr_width)?;
                    let n = args[0]
                        .strip_prefix('@')
                        .ok_or_else(|| Error("§4.8: addr requires @name".into()))?;
                    let global = self
                        .section("layout")
                        .and_then(|l| l.get("globals").ok())
                        .and_then(|g| g.object().ok())
                        .is_some_and(|g| g.contains_key(n));
                    if !global && !(f.kind == "oracle" && f.params[3].iter().any(|p| p.name == n)) {
                        return err("§4.2", format!("addr cannot name {n} in {}", f.name));
                    }
                }
                "lift.boundscheck" => {
                    arity(2, 0)?;
                    addr(&args[0])?;
                    length(&args[1])?;
                }
                "lift.alloc" => {
                    arity(1, 1)?;
                    length(&args[0])?;
                    eq(dest(&i.lhs[0])?, self.ptr_width)?;
                }
                "lift.free" => {
                    arity(1, 0)?;
                    addr(&args[0])?;
                }
                "lift.faultif" => {
                    arity(2, 0)?;
                    eq(rd(&args[0])?, 1)?;
                    code(&args[1])?;
                }
                "lift.call" => {
                    arity(2, 1)?;
                    let callee = self.declaration(
                        args[0]
                            .strip_prefix('@')
                            .ok_or_else(|| Error("§4.8: lift.call requires @symbol".into()))?,
                    )?;
                    if callee.kind != "lproc" {
                        return err("§3.7", "lift.call requires lproc");
                    }
                    let src = list(&args[1])?;
                    if src.len() != callee.params[0].len() {
                        return err("§3.3", "lproc argument count");
                    }
                    for (s, p) in src.iter().zip(&callee.params[0]) {
                        eq(rd(s)?, p.ty.width(self.ptr_width)?)?;
                    }
                    eq(
                        dest(&i.lhs[0])?,
                        callee.params[1][0].ty.width(self.ptr_width)?,
                    )?;
                }
                "lift.ret" | "lift.retval" => {
                    arity(1, 0)?;
                    if (op == "lift.ret") != (f.kind == "lproc") {
                        return err("§4.2", "ret/retval in wrong function kind");
                    }
                    eq(rd(&args[0])?, f.params[1][0].ty.width(self.ptr_width)?)?;
                }
                "qjump" => {
                    arity(1, 0)?;
                    label(&args[0])?;
                }
                "qbranch" => {
                    arity(3, 0)?;
                    eq(rd(&args[0])?, 1)?;
                    label(&args[1])?;
                    label(&args[2])?;
                }
                "qjumpr" => {
                    arity(1, 0)?;
                    let w = rd(&args[0])?;
                    if w < 128 && (1u128 << w) <= self.index_space_size(f)? {
                        return err("§3.3", "qjumpr width cannot represent index space");
                    }
                }
                "fault" => {
                    arity(1, 0)?;
                    code(&args[0])?;
                }
                "lift.oracle_call" | "lift.oracle_uncall" | "lift.perm_call" => {
                    self.validate_region_call(f, i, types)?
                }
                _ if op.starts_with("lift.load.i") || op.starts_with("lift.store.i") => {
                    let load = op.starts_with("lift.load");
                    arity(if load { 1 } else { 2 }, if load { 1 } else { 0 })?;
                    let n = op
                        .rsplit_once(".i")
                        .expect("suffix")
                        .1
                        .parse::<u16>()
                        .map_err(|_| Error("§4.8: malformed memory width".into()))?;
                    if n == 0 || n > 128 || n % 8 != 0 {
                        return err("§3.3", "load/store width must be a byte multiple up to 128");
                    }
                    addr(&args[0])?;
                    eq(
                        if load {
                            dest(&i.lhs[0])?
                        } else {
                            rd(&args[1])?
                        },
                        n,
                    )?;
                }
                _ => return err("§4.8", format!("unknown or invalid lifted opcode {op}")),
            }
        }
        Ok(())
    }
    fn validate_layout(&self) -> Result<()> {
        let Some(l) = self.section("layout") else {
            for f in self.functions.values() {
                if f.kind == "lproc"
                    || f.params
                        .iter()
                        .flatten()
                        .any(|p| matches!(p.ty, Type::Region(..)))
                    || f.instructions().any(|i| {
                        matches!(
                            i.op.as_str(),
                            "lift.addr"
                                | "lift.boundscheck"
                                | "lift.alloc"
                                | "lift.free"
                                | "lift.call"
                                | "lift.ret"
                                | "alloc"
                                | "free"
                        ) || i.op.starts_with("lift.load.")
                            || i.op.starts_with("lift.store.")
                            || i.op.starts_with("load.")
                            || i.op.starts_with("store.")
                    })
                {
                    return err("§7.2", "memory or lprocs require layout");
                }
            }
            return Ok(());
        };
        l.fields(
            &[
                "ptr_width",
                "H",
                "A_tab",
                "S_cells",
                "null_size",
                "heap_base",
                "heap_limit_max",
                "globals",
                "interface_regions",
            ],
            &["block_image"],
        )?;
        if l.get("ptr_width")?.uint()? != self.ptr_width as u128 {
            return err("§7.2", "layout pointer width mismatch");
        }
        let h = l.get("H")?.uint()?;
        let a = l.get("A_tab")?.uint()?;
        let s = l.get("S_cells")?.uint()?;
        if h > self.ptr_width as u128 || h > 127 || a > 127 || s > 127 {
            return err("§7.2", "invalid layout size exponent");
        }
        let capacity = 1u128 << (h as u32);
        let entries = 1u128 << (a as u32);
        let globals = l.get("globals")?.object()?;
        let null = l.get("null_size")?.uint()?;
        if null == 0 {
            return err("§7.1", "null region must be nonempty");
        }
        let mut shared = vec![
            (0, null, "null".to_string()),
            (
                l.get("heap_base")?.uint()?,
                l.get("heap_limit_max")?.uint()?,
                "heap".into(),
            ),
        ];
        for (n, g) in globals {
            g.fields(&["base", "size", "image"], &[])?;
            let image = g.get("image")?.string()?;
            if image != n
                || self.data.get(n).is_none_or(|b| {
                    b.len() as u128 != g.get("size").and_then(Json::uint).unwrap_or(u128::MAX)
                })
            {
                return err(
                    "§7.2",
                    "global image must be same-name data of declared size",
                );
            }
            shared.push((g.get("base")?.uint()?, g.get("size")?.uint()?, n.clone()));
        }
        let interfaces = l.get("interface_regions")?.object()?;
        for (n, regions) in interfaces {
            let f = self
                .functions
                .get(n)
                .filter(|f| f.kind == "oracle")
                .ok_or_else(|| Error("§7.2: interface layout must name an oracle".into()))?;
            let regions = regions.object()?;
            if regions.len() != f.params[3].len() {
                return err("§7.2", "interface mapping count mismatch");
            }
            let mut ranges = shared.clone();
            for p in &f.params[3] {
                let (a, w) = match p.ty {
                    Type::Region(a, w) => (a, w),
                    _ => return err("§5.1", "mem slot requires region"),
                };
                if w != 8 {
                    return err("§7.2", "lifted interface regions require W=8");
                }
                let r = regions
                    .get(&p.name)
                    .ok_or_else(|| Error("§7.2: missing interface mapping".into()))?;
                r.fields(&["base"], &[])?;
                ranges.push((r.get("base")?.uint()?, 1u128 << a, p.name.clone()));
            }
            if globals.len() as u128 + regions.len() as u128 > entries {
                return err("§7.2", "too many allocation pre-entries");
            }
            validate_ranges(&ranges, capacity)?;
        }
        for f in self
            .functions
            .values()
            .filter(|f| f.kind == "oracle" && !f.params[3].is_empty())
        {
            if !interfaces.contains_key(&f.name) {
                return err("§7.2", "missing oracle interface layout");
            }
        }
        if globals.len() as u128 > entries {
            return err("§7.2", "too many globals");
        }
        validate_ranges(&shared, capacity)
    }
}

fn is_head(s: &str) -> bool {
    [
        "fn cc @",
        "fn r @",
        "oracle @",
        "lproc @",
        "action @",
        "perm_action @",
    ]
    .iter()
    .any(|p| s.starts_with(p))
}
pub(crate) fn is_binop(op: &str) -> bool {
    [
        "add", "sub", "mul", "and", "or", "xor", "shl", "lshr", "ashr",
    ]
    .contains(&op)
}
pub(crate) fn is_div(op: &str) -> bool {
    ["udiv", "urem", "sdiv", "srem"].contains(&op)
}
pub(crate) fn parse_bits(s: &str, width: u16) -> Result<u128> {
    let negative = s.starts_with('-');
    let magnitude = s
        .trim_start_matches('-')
        .parse::<u128>()
        .map_err(|_| Error("§16.1: integer exceeds 128 bits".into()))?;
    let n = if negative {
        0u128.wrapping_sub(magnitude)
    } else {
        magnitude
    };
    Ok(n & mask(width))
}
pub(crate) fn mask(width: u16) -> u128 {
    if width == 128 {
        u128::MAX
    } else {
        (1u128 << width) - 1
    }
}
fn validate_header(f: &Function) -> Result<()> {
    let empty = |indices: &[usize]| -> Result<()> {
        if indices.iter().any(|i| !f.params[*i].is_empty()) {
            err("§16.2", "nonempty reserved parameter list")
        } else {
            Ok(())
        }
    };
    let all = |ps: &[Param], kind: fn(&Type) -> bool| -> Result<()> {
        if ps.iter().any(|p| !kind(&p.ty)) {
            err("§3.3", "invalid interface operand type")
        } else {
            Ok(())
        }
    };
    let classical=|t:&Type|matches!(t,Type::Int(_)|Type::Ptr|Type::F64|Type::Token);
    match f.kind.as_str() {
        "oracle" => {
            all(&f.params[4],classical)?;
            if f.params[1].len() != 1 || f.params[2].len() != 1 {
                return err("§5.1", "oracle needs one target and one fault slot");
            }
            for j in 0..3 {
                all(&f.params[j], |t| matches!(t, Type::Wire(_)))?;
            }
            if f.params[2][0].ty.width(1)? < 4 {
                return err("§5.4", "fault width must be at least 4");
            }
            all(&f.params[3], |t| matches!(t, Type::Region(..)))?;
            if f.params[0]
                .iter()
                .chain(&f.params[3])
                .any(|p| p.role.as_deref() != Some("in"))
            {
                return err("§5.1", "oracle inputs and regions require in role");
            }
        }
        "lproc" => {
            empty(&[2, 3, 4])?;
            if f.params[1].len() != 1 {
                return err("§3.7", "lproc needs one result location");
            }
            all(&f.params[0], |t| matches!(t, Type::Reg(_)))?;
            all(&f.params[1], |t| matches!(t, Type::Reg(_)))?;
        }
        "action" | "perm_action" => {
            all(&f.params[3],classical)?;
            empty(&[4])?;
            for j in 0..2 {
                all(&f.params[j], |t| matches!(t, Type::Wire(_)))?;
            }
            all(&f.params[2], |t| matches!(t, Type::Region(..)))?;
            if f.params[2].iter().any(|p|!matches!(p.role.as_deref(),Some("in"|"mut"))){return err("§5.1","action regions need in or mut roles");}
        }
        _ => {empty(&[2,3,4])?;for group in 0..2{all(&f.params[group],|t|matches!(t,Type::Int(_)|Type::Ptr|Type::F64|Type::Token|Type::Qreg(_)))?;}if !f.regs.is_empty()||!f.bounds.is_empty(){return err("§3.3","classical functions use SSA definitions, not a mutable regs file");}}
    }
    if matches!(f.kind.as_str(), "oracle" | "lproc") {
        all(&f.regs, |t| matches!(t, Type::Reg(_)))?;
        if !f.bounds.is_empty() {
            return err("§5.3", "bounds only on actions");
        }
    }
    Ok(())
}
fn validate_ranges(ranges: &[(u128, u128, String)], capacity: u128) -> Result<()> {
    let mut sorted = Vec::new();
    for (base, size, n) in ranges {
        let end = base
            .checked_add(*size)
            .ok_or_else(|| Error("§7.2: range overflow".into()))?;
        if end > capacity {
            return err("§7.2", format!("{n} exceeds address space"));
        }
        if *size != 0 {
            sorted.push((*base, end, n));
        }
    }
    sorted.sort();
    for p in sorted.windows(2) {
        if p[0].1 > p[1].0 {
            return err(
                "§7.2",
                format!("overlapping layout ranges {} and {}", p[0].2, p[1].2),
            );
        }
    }
    Ok(())
}
````

## `src/oracle.rs` (733 lines)

````rust
//! §14.1 sequential interpreter. It uses independent dynamic activations rather
//! than the reversible machine's global location file and frame-slot exchanges.
use crate::{
    err,
    object::{integer, is_binop, is_div, list, mask, parse_bits},
    Error, Function, Instruction, Object, Result, Type,
};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Budget {
    pub steps: u64,
    pub heap: u128,
    pub stack: u128,
    pub depth: u128,
}
impl Budget {
    pub fn steps(steps: u64) -> Self {
        Self {
            steps,
            heap: 0,
            stack: 0,
            depth: 0,
        }
    }
}
#[derive(Clone, Debug, PartialEq)]
pub enum Argument {
    Bits(u128),
    Float(f64),
    Token(Budget),
}
#[derive(Clone, Debug, Default, PartialEq)]
pub struct OracleInput {
    pub ins: Vec<u128>,
    pub args: Vec<Argument>,
    pub regions: BTreeMap<String, Vec<u8>>,
}
impl OracleInput {
    pub fn bits(ins: &[u128]) -> Self {
        Self {
            ins: ins.into(),
            ..Self::default()
        }
    }
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct OracleOutcome {
    pub payload: u128,
    pub code: u128,
    pub steps: u64,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct Allocation {
    pub base: u128,
    pub size: u128,
    pub live: bool,
    pub pinned: bool,
}
#[derive(Clone, Debug, PartialEq, Eq, Default)]
pub(crate) struct Memory {
    pub bytes: BTreeMap<u128, u8>,
    pub allocations: Vec<Allocation>,
    pub heap_base: u128,
    pub heap_used: u128,
    pub table_capacity: u128,
    pub addresses: BTreeMap<String, u128>,
}
impl Memory {
    pub fn initial(object: &Object, oracle: &Function, input: &OracleInput) -> Result<Self> {
        let Some(layout) = object.section("layout") else {
            return Ok(Self::default());
        };
        let mut m = Self {
            heap_base: layout.get("heap_base")?.uint()?,
            table_capacity: 1u128 << (layout.get("A_tab")?.uint()? as u32),
            ..Self::default()
        };
        for (n, g) in layout.get("globals")?.object()? {
            let base = g.get("base")?.uint()?;
            let size = g.get("size")?.uint()?;
            m.addresses.insert(n.clone(), base);
            m.allocations.push(Allocation {
                base,
                size,
                live: true,
                pinned: true,
            });
            for (i, b) in object.data[n].iter().enumerate() {
                m.set_byte(base + i as u128, *b);
            }
        }
        if !oracle.params[3].is_empty() {
            let regions = layout.get("interface_regions")?.get(&oracle.name)?;
            // Allocation pre-entries follow layout order (§3.7), not signature order.
            for (n, r) in regions.object()? {
                let p = oracle.params[3]
                    .iter()
                    .find(|p| p.name == *n)
                    .expect("validated region mapping");
                let Type::Region(a, _) = p.ty else {
                    unreachable!("validated region type")
                };
                let base = r.get("base")?.uint()?;
                let size = 1u128 << a;
                let bytes = input
                    .regions
                    .get(n)
                    .ok_or_else(|| Error(format!("§5.1: missing interface region {n}")))?;
                if bytes.len() as u128 != size {
                    return err("§5.1", format!("interface region {n} has wrong byte count"));
                }
                m.addresses.insert(n.clone(), base);
                m.allocations.push(Allocation {
                    base,
                    size,
                    live: true,
                    pinned: true,
                });
                for (i, b) in bytes.iter().enumerate() {
                    m.set_byte(base + i as u128, *b);
                }
            }
        }
        Ok(m)
    }
    pub fn valid(&self, p: u128, n: u128) -> bool {
        p.checked_add(n).is_some_and(|end| {
            self.allocations.iter().any(|e| {
                e.live
                    && e.base <= p
                    && e.base.checked_add(e.size).is_some_and(|limit| end <= limit)
            })
        })
    }
    pub fn byte(&self, p: u128) -> u8 {
        self.bytes.get(&p).copied().unwrap_or(0)
    }
    pub fn set_byte(&mut self, p: u128, b: u8) {
        if b == 0 {
            self.bytes.remove(&p);
        } else {
            self.bytes.insert(p, b);
        }
    }
    pub fn load(&self, p: u128, width: u16) -> u128 {
        (0..width / 8)
            .map(|i| (self.byte(p + i as u128) as u128) << (8 * i))
            .fold(0, |a, b| a | b)
    }
    pub fn store(&mut self, p: u128, width: u16, v: u128) {
        for i in 0..width / 8 {
            self.set_byte(p + i as u128, (v >> (8 * i)) as u8);
        }
    }
    pub fn allocation_fails(&self, n: u128, budget: Budget) -> bool {
        self.heap_used
            .checked_add(n.max(1))
            .is_none_or(|total| total > budget.heap)
            || self.allocations.len() as u128 >= self.table_capacity
    }
    pub fn allocate(&mut self, n: u128) -> u128 {
        let base = self.heap_base + self.heap_used;
        self.allocations.push(Allocation {
            base,
            size: n,
            live: true,
            pinned: false,
        });
        self.heap_used += n.max(1);
        base
    }
    pub fn free(&mut self, p: u128) -> bool {
        if let Some(e) = self
            .allocations
            .iter_mut()
            .find(|e| e.base == p && e.live && !e.pinned)
        {
            e.live = false;
            true
        } else {
            false
        }
    }
}

pub(crate) struct Program<'a> {
    pub rows: Vec<(&'a Function, &'a Instruction)>,
    pub labels: BTreeMap<(String, String), usize>,
    pub ranges: BTreeMap<String, (usize, usize)>,
    pub halt: usize,
}
impl<'a> Program<'a> {
    pub fn new(object: &'a Object, root: &str) -> Result<Self> {
        object.ensure_linked()?;
        let oracle = object
            .functions
            .get(root)
            .filter(|f| f.kind == "oracle")
            .ok_or_else(|| Error(format!("§5.2: unknown oracle @{root}")))?;
        let mut reachable = BTreeSet::new();
        let mut pending = vec![root.to_string()];
        while let Some(n) = pending.pop() {
            let function = object.functions.get(&n).ok_or_else(|| {
                Error(format!(
                    "§9.3: oracle closure has unresolved lproc @{n}; link before execution"
                ))
            })?;
            for i in function.instructions().filter(|i| i.op == "lift.call") {
                let n = i.operands[0].trim_start_matches('@').to_string();
                if reachable.insert(n.clone()) {
                    pending.push(n);
                }
            }
        }
        let mut closure: Vec<_> = reachable.into_iter().collect();
        if !closure.is_empty() {
            let identity = object.identity()?;
            closure.sort_by(|a, b| {
                let key = |n: &String| {
                    if identity.scc_members[n].len() > 1 {
                        identity.scc_hashes[n].as_str()
                    } else {
                        identity.closure_hashes[n]
                            .as_deref()
                            .expect("defined lproc closure")
                    }
                };
                key(a).cmp(key(b)).then(a.cmp(b))
            });
        }
        let order = std::iter::once(&oracle.name).chain(closure.iter());
        let mut rows = Vec::new();
        let mut labels = BTreeMap::new();
        let mut ranges = BTreeMap::new();
        for n in order {
            let f = &object.functions[n];
            let start = rows.len();
            for b in &f.blocks {
                labels.insert((n.clone(), b.name.clone()), rows.len());
                for i in &b.instructions {
                    rows.push((f, i));
                }
            }
            ranges.insert(n.clone(), (start, rows.len()));
        }
        let halt = rows.len();
        Ok(Self {
            rows,
            labels,
            ranges,
            halt,
        })
    }
    pub fn label(&self, f: &str, label: &str) -> Result<usize> {
        self.labels
            .get(&(f.into(), label.trim_start_matches('^').into()))
            .copied()
            .ok_or_else(|| Error(format!("§3.6: unknown label {label} in @{f}")))
    }
}

#[derive(Clone)]
struct Activation {
    function: String,
    values: BTreeMap<String, u128>,
    ret_pc: usize,
    destination: String,
}
impl Activation {
    fn new(f: &Function) -> Self {
        Self {
            function: f.name.clone(),
            values: f.locations().iter().map(|p| (p.name.clone(), 0)).collect(),
            ret_pc: 0,
            destination: String::new(),
        }
    }
    fn read(&self, n: &str) -> Result<u128> {
        self.values.get(n).copied().ok_or_else(|| {
            Error(format!(
                "§3.7: unreadable operand {n} in @{}",
                self.function
            ))
        })
    }
    fn write(&mut self, f: &Function, n: &str, v: u128, ptr: u16) -> Result<()> {
        let p = f
            .locations()
            .into_iter()
            .find(|p| p.name == n)
            .ok_or_else(|| Error(format!("§3.7: unwritable location {n}")))?;
        self.values.insert(n.into(), v & mask(p.ty.width(ptr)?));
        Ok(())
    }
}

impl Object {
    pub fn validate_budget(&self, b: Budget) -> Result<()> {
        if let Some(l) = self.section("layout") {
            if b.heap > l.get("heap_limit_max")?.uint()?
                || b.stack > 1u128 << (l.get("S_cells")?.uint()? as u32)
                || b.depth == u128::MAX
            {
                return err("§5.4", "budget limit does not fit layout/counter");
            }
        } else if b.heap != 0 || b.stack != 0 || b.depth != 0 {
            return err(
                "§5.4",
                "memoryless budgets require zero heap, stack and depth",
            );
        }
        Ok(())
    }
    pub fn default_budget(&self, steps: u64) -> Result<Budget> {
        if let Some(l) = self.section("layout") {
            Ok(Budget {
                steps,
                heap: l.get("heap_limit_max")?.uint()?,
                stack: 1u128 << (l.get("S_cells")?.uint()? as u32),
                depth: 64,
            })
        } else {
            Ok(Budget::steps(steps))
        }
    }
    pub fn run_oracle(
        &self,
        name: &str,
        input: &OracleInput,
        budget: Budget,
    ) -> Result<OracleOutcome> {
        self.validate_budget(budget)?;
        let program = Program::new(self, name)?;
        let root = &self.functions[name];
        if input.ins.len() != root.params[0].len()
            || input.args.len() != root.params[4].len()
            || input.regions.len() != root.params[3].len()
        {
            return err("§5.1", "oracle interface argument count mismatch");
        }
        let mut activation = Activation::new(root);
        let mut arguments = BTreeMap::new();
        for (p, v) in root.params[0].iter().zip(&input.ins) {
            if *v & !mask(p.ty.width(self.ptr_width)?) != 0 {
                return err("§3.3", "input value exceeds declared width");
            }
            activation.values.insert(p.name.clone(), *v);
        }
        for (p, v) in root.params[4].iter().zip(&input.args) {
            match (&p.ty, v) {
                (Type::Int(w), Argument::Bits(v)) if *v & !mask(*w) == 0 => {
                    activation.values.insert(p.name.clone(), *v);
                }
                (Type::Ptr, Argument::Bits(v)) if *v & !mask(self.ptr_width) == 0 => {
                    activation.values.insert(p.name.clone(), *v);
                }
                (Type::F64, Argument::Float(v)) if v.is_finite() => {}
                (Type::Token, Argument::Token(b)) => {
                    self.validate_budget(*b)?;
                }
                _ => return err("§3.3", "classical argument type/width mismatch"),
            }
            arguments.insert(p.name.clone(), v.clone());
        }
        let mut memory = Memory::initial(self, root, input)?;
        let mut stack: Vec<Activation> = Vec::new();
        let mut sp = 0u128;
        let mut pc = 0;
        let mut steps = 0;
        let mut result = 0;
        macro_rules! fault {
            ($code:expr) => {
                return Ok(OracleOutcome {
                    payload: 0,
                    code: $code,
                    steps,
                })
            };
        }
        while steps < budget.steps {
            if pc == program.halt {
                return Ok(OracleOutcome {
                    payload: result,
                    code: 0,
                    steps,
                });
            }
            let (f, i) = program.rows[pc];
            if activation.function != f.name {
                return err("§3.7", "control escaped its active function");
            }
            steps += 1;
            let mut next = pc + 1;
            let op = i.op.as_str();
            let a = &i.operands;
            let rd = |n: &str| activation.read(n);
            let width = |n: &str| -> Result<u16> {
                f.locations()
                    .into_iter()
                    .chain(if f.kind == "oracle" {
                        f.params[0].iter().chain(&f.params[4]).collect::<Vec<_>>()
                    } else {
                        Vec::new()
                    })
                    .find(|p| p.name == n)
                    .ok_or_else(|| Error(format!("§3.7: unknown width for {n}")))?
                    .ty
                    .width(self.ptr_width)
            };
            let mut output = None;
            if let Some(n) = op.strip_prefix("lift.const.i") {
                output = Some(parse_bits(
                    &a[0],
                    n.parse().expect("validated constant width"),
                )?);
            } else if let Some(bin) = op.strip_prefix("lift.").filter(|s| is_binop(s)) {
                output = Some(binop(bin, rd(&a[0])?, rd(&a[1])?, width(&a[0])?));
            } else if let Some(div) = op.strip_prefix("lift.").filter(|s| is_div(s)) {
                match divide(div, rd(&a[0])?, rd(&a[1])?, width(&a[0])?) {
                    Ok(v) => output = Some(v),
                    Err(c) => fault!(c),
                }
            } else if let Some(pred) = op.strip_prefix("lift.icmp.") {
                output = Some(compare(pred, rd(&a[0])?, rd(&a[1])?, width(&a[0])?) as u128);
            } else if let Some((cast, _)) = op
                .strip_prefix("lift.")
                .and_then(|s| s.split_once(".i"))
                .filter(|(c, _)| ["zext", "sext", "trunc"].contains(c))
            {
                let v = rd(&a[0])?;
                output = Some(if cast == "sext" {
                    signed(v, width(&a[0])?) as u128
                } else {
                    v
                });
            } else if let Some(n) = op.strip_prefix("lift.load.i") {
                let w = n.parse::<u16>().expect("validated load width");
                let p = rd(&a[0])?;
                if !memory.valid(p, (w / 8) as u128) {
                    fault!(7);
                }
                output = Some(memory.load(p, w));
            } else if let Some(n) = op.strip_prefix("lift.store.i") {
                let w = n.parse::<u16>().expect("validated store width");
                let p = rd(&a[0])?;
                let v = rd(&a[1])?;
                if !memory.valid(p, (w / 8) as u128) {
                    fault!(7);
                }
                memory.store(p, w, v);
            } else {
                match op {
                    "lift.mov" => output = Some(rd(&a[0])?),
                    "lift.select" => {
                        output = Some(rd(if rd(&a[0])? != 0 { &a[1] } else { &a[2] })?)
                    }
                    "lift.parmov" => {
                        let values = list(&a[0])?
                            .iter()
                            .map(|s| rd(s))
                            .collect::<Result<Vec<_>>>()?;
                        for (d, v) in i.lhs.iter().zip(values) {
                            activation.write(f, d, v, self.ptr_width)?;
                        }
                    }
                    "lift.label" => output = Some(program.label(&f.name, &a[0])? as u128),
                    "lift.addr" => {
                        output = Some(
                            *memory
                                .addresses
                                .get(a[0].trim_start_matches('@'))
                                .ok_or_else(|| Error("§4.2: address not mapped".into()))?,
                        )
                    }
                    "lift.boundscheck" => {
                        let p = rd(&a[0])?;
                        let n = if integer(&a[1]) {
                            a[1].parse::<u128>().expect("validated length")
                        } else {
                            rd(&a[1])?
                        };
                        if !memory.valid(p, n) {
                            fault!(7);
                        }
                    }
                    "lift.alloc" => {
                        let n = if integer(&a[0]) {
                            a[0].parse::<u128>().expect("validated length")
                        } else {
                            rd(&a[0])?
                        };
                        if memory.allocation_fails(n, budget) {
                            fault!(2);
                        }
                        output = Some(memory.allocate(n));
                    }
                    "lift.free" => {
                        let p = rd(&a[0])?;
                        if !memory.free(p) {
                            fault!(7);
                        }
                    }
                    "lift.faultif" => {
                        if rd(&a[0])? != 0 {
                            fault!(a[1].parse::<u128>().expect("validated fault code"));
                        }
                    }
                    "fault" => fault!(a[0].parse::<u128>().expect("validated fault code")),
                    "qjump" => next = program.label(&f.name, &a[0])?,
                    "qbranch" => {
                        next =
                            program.label(&f.name, if rd(&a[0])? != 0 { &a[1] } else { &a[2] })?
                    }
                    "qjumpr" => {
                        let address = rd(&a[0])?;
                        let (start, end) = program.ranges[&f.name];
                        if address < (start as u128) || address >= end as u128 {
                            fault!(4);
                        }
                        next = address as usize;
                    }
                    "lift.call" => {
                        let callee = &self.functions[a[0].trim_start_matches('@')];
                        let cells = callee.frame_cells() as u128;
                        if stack.len() as u128 + 1 > budget.depth
                            || sp.checked_add(cells).is_none_or(|p| p > budget.stack)
                        {
                            fault!(3);
                        }
                        let values = list(&a[1])?
                            .iter()
                            .map(|s| rd(s))
                            .collect::<Result<Vec<_>>>()?;
                        let mut called = Activation::new(callee);
                        called.ret_pc = pc + 1;
                        called.destination = i.lhs[0].clone();
                        for (p, v) in callee.params[0].iter().zip(values) {
                            called.values.insert(p.name.clone(), v);
                        }
                        sp += cells;
                        stack.push(activation);
                        activation = called;
                        next = program.ranges[&callee.name].0;
                    }
                    "lift.ret" => {
                        if stack.is_empty() {
                            fault!(4);
                        }
                        let v = rd(&a[0])?;
                        let ret = activation.ret_pc;
                        let dest = activation.destination.clone();
                        activation = stack.pop().expect("nonempty activation stack");
                        let caller = &self.functions[&activation.function];
                        activation.write(caller, &dest, v, self.ptr_width)?;
                        next = ret;
                    }
                    "lift.retval" => {
                        result ^= rd(&a[0])?;
                        return Ok(OracleOutcome {
                            payload: result,
                            code: 0,
                            steps,
                        });
                    }
                    "lift.oracle_call" | "lift.oracle_uncall" => {
                        let callee = &self.functions[a[0].trim_start_matches('@')];
                        let token = arguments
                            .get(&a[1])
                            .and_then(|a| {
                                if let Argument::Token(b) = a {
                                    Some(*b)
                                } else {
                                    None
                                }
                            })
                            .ok_or_else(|| {
                                Error("§4.2: nested oracle call needs a budget token".into())
                            })?;
                        let mut child = OracleInput::bits(
                            &list(&a[2])?
                                .iter()
                                .map(|s| rd(s))
                                .collect::<Result<Vec<_>>>()?,
                        );
                        let region_args = list(&a[5])?;
                        for (p, n) in callee.params[3].iter().zip(region_args) {
                            let base = memory.addresses[&n];
                            let Type::Region(aw, _) = p.ty else {
                                unreachable!("validated region")
                            };
                            let len = usize::try_from(1u128 << aw).map_err(|_| {
                                Error("§7.2: region exceeds host addressable storage".into())
                            })?;
                            child.regions.insert(
                                p.name.clone(),
                                (0..len).map(|i| memory.byte(base + i as u128)).collect(),
                            );
                        }
                        for arg in list(&a[6])? {
                            child.args.push(match arguments.get(&arg) {
                                Some(v) => v.clone(),
                                None => Argument::Bits(rd(&arg)?),
                            });
                        }
                        let r = self.run_oracle(&callee.name, &child, token)?;
                        let tgt = rd(&a[3])? ^ r.payload;
                        let code = rd(&a[4])? ^ r.code;
                        activation.write(f, &a[3], tgt, self.ptr_width)?;
                        activation.write(f, &a[4], code, self.ptr_width)?;
                    }
                    "lift.perm_call" => {
                        let callee = &self.functions[a[0].trim_start_matches('@')];
                        let destinations = list(&a[1])?;
                        let mutable = destinations
                            .iter()
                            .map(|n| rd(n))
                            .collect::<Result<Vec<_>>>()?;
                        let inputs = list(&a[2])?
                            .iter()
                            .map(|n| rd(n))
                            .collect::<Result<Vec<_>>>()?;
                        let mut regions = BTreeMap::new();
                        for (p, n) in callee.params[2].iter().zip(list(&a[3])?) {
                            let base = memory.addresses[&n];
                            let Type::Region(aw, _) = p.ty else {
                                unreachable!("region")
                            };
                            let len = usize::try_from(1u128 << aw)
                                .map_err(|_| Error("§7.2: action region too large".into()))?;
                            regions.insert(
                                p.name.clone(),
                                (0..len).map(|i| memory.byte(base + i as u128)).collect(),
                            );
                        }
                        let args = list(&a[4])?
                            .iter()
                            .map(|n| match arguments.get(n) {
                                Some(v) => Ok(v.clone()),
                                None => Ok(Argument::Bits(rd(n)?)),
                            })
                            .collect::<Result<Vec<_>>>()?;
                        let values = self.permutation_action_values(
                            &callee.name,
                            &mutable,
                            &inputs,
                            &regions,
                            &args,
                            false,
                        )?;
                        for (n, v) in destinations.iter().zip(values) {
                            activation.write(f, n, v, self.ptr_width)?;
                        }
                    }
                    _ => return err("§4.8", format!("unimplemented sequential row {op}")),
                }
            }
            if let Some(v) = output {
                activation.write(f, &i.lhs[0], v, self.ptr_width)?;
            }
            pc = next;
        }
        Ok(OracleOutcome {
            payload: 0,
            code: 1,
            steps,
        })
    }
}
pub(crate) fn signed(v: u128, width: u16) -> i128 {
    let shift = 128 - width;
    (v << shift) as i128 >> shift
}
pub(crate) fn binop(op: &str, a: u128, b: u128, w: u16) -> u128 {
    let v = match op {
        "add" => a.wrapping_add(b),
        "sub" => a.wrapping_sub(b),
        "mul" => a.wrapping_mul(b),
        "and" => a & b,
        "or" => a | b,
        "xor" => a ^ b,
        "shl" => {
            if b >= w as u128 {
                0
            } else {
                a << (b as u32)
            }
        }
        "lshr" => {
            if b >= w as u128 {
                0
            } else {
                a >> (b as u32)
            }
        }
        "ashr" => {
            if b >= w as u128 {
                0
            } else {
                (signed(a, w) >> (b as u32)) as u128
            }
        }
        _ => unreachable!("validated binop"),
    };
    v & mask(w)
}
pub(crate) fn divide(op: &str, a: u128, b: u128, w: u16) -> std::result::Result<u128, u128> {
    if b == 0 {
        return Err(5);
    }
    if op.starts_with('s') && a == 1u128 << (w - 1) && b == mask(w) {
        return Err(6);
    }
    Ok(match op {
        "udiv" => a / b,
        "urem" => a % b,
        "sdiv" => (signed(a, w) / signed(b, w)) as u128,
        "srem" => (signed(a, w) % signed(b, w)) as u128,
        _ => unreachable!("validated division"),
    } & mask(w))
}
pub(crate) fn compare(pred: &str, a: u128, b: u128, w: u16) -> bool {
    match pred {
        "eq" => a == b,
        "ne" => a != b,
        "ult" => a < b,
        "ule" => a <= b,
        "slt" => signed(a, w) < signed(b, w),
        "sle" => signed(a, w) <= signed(b, w),
        _ => unreachable!("validated comparison"),
    }
}
````

## `src/quantum.rs` (587 lines)

````rust
//! Small state-vector semantics and a sparse basis-permutation fast path.
use crate::{err, Argument, Error, Result};
use std::collections::{BTreeMap, BTreeSet};
pub type Wire = u64;

#[derive(Clone, Copy, Debug, PartialEq, Default)]
pub struct Complex {
    pub re: f64,
    pub im: f64,
}
impl Complex {
    pub const ZERO: Self = Self { re: 0.0, im: 0.0 };
    pub const ONE: Self = Self { re: 1.0, im: 0.0 };
    pub fn new(re: f64, im: f64) -> Self {
        Self { re, im }
    }
    fn phase(a: f64) -> Self {
        Self::new(a.cos(), a.sin())
    }
    fn norm2(self) -> f64 {
        self.re * self.re + self.im * self.im
    }
    fn scale(self, s: f64) -> Self {
        Self::new(self.re * s, self.im * s)
    }
}
impl std::ops::Add for Complex {
    type Output = Self;
    fn add(self, b: Self) -> Self {
        Self::new(self.re + b.re, self.im + b.im)
    }
}
impl std::ops::Mul for Complex {
    type Output = Self;
    fn mul(self, b: Self) -> Self {
        Self::new(
            self.re * b.re - self.im * b.im,
            self.re * b.im + self.im * b.re,
        )
    }
}
#[derive(Clone, Debug, PartialEq)]
enum State {
    Basis { bits: Vec<bool>, phase: Complex },
    Vector(Vec<Complex>),
}
#[derive(Clone, Debug)]
pub struct QuantumState {
    ids: Vec<Wire>,
    next: Wire,
    state: State,
}
impl PartialEq for QuantumState {
    fn eq(&self, other: &Self) -> bool {
        if self.ids != other.ids || self.next != other.next {
            return false;
        }
        let close =
            |a: Complex, b: Complex| (a.re - b.re).abs() <= 1e-12 && (a.im - b.im).abs() <= 1e-12;
        match (&self.state, &other.state) {
            (State::Basis { bits: a, phase: p }, State::Basis { bits: b, phase: q }) => {
                a == b && close(*p, *q)
            }
            _ => match (self.amplitudes(), other.amplitudes()) {
                (Ok(a), Ok(b)) => {
                    a.len() == b.len() && a.into_iter().zip(b).all(|(a, b)| close(a, b))
                }
                _ => false,
            },
        }
    }
}
impl Default for QuantumState {
    fn default() -> Self {
        Self::new()
    }
}
#[derive(Clone, Debug)]
pub struct MeasurementBranch {
    pub probability: f64,
    pub bits: Vec<bool>,
    pub state: QuantumState,
}
#[derive(Clone, Debug, Default)]
pub struct QuantumBindings {
    pub bundles: BTreeMap<String, Vec<Wire>>,
    pub regions: BTreeMap<String, QuantumRegion>,
    pub args: BTreeMap<String, Argument>,
    pub borrowed: Vec<Vec<Wire>>,
}
#[derive(Clone, Debug)]
pub struct QuantumRegion {
    pub address_width: u16,
    pub cell_width: u16,
    pub cells: Vec<Vec<Wire>>,
}

impl QuantumState {
    pub(crate) fn next_wire_id(&self) -> u64 {
        self.next
    }
    pub(crate) fn restore_next_wire_id(&mut self, next: u64) -> Result<()> {
        if self.ids.iter().any(|id| *id >= next) {
            return err("§7.4", "cannot restore wire counter over live wires");
        }
        self.next = next;
        Ok(())
    }
    pub(crate) fn restore_clean(&mut self, positions: &[(usize, Wire)]) -> Result<()> {
        let n = self
            .ids
            .len()
            .checked_add(positions.len())
            .ok_or_else(|| Error("§7.4: wire count overflow".into()))?;
        let mut removed = BTreeMap::new();
        for (pos, wire) in positions {
            if *pos >= n || removed.insert(*pos, *wire).is_some() || self.ids.contains(wire) {
                return err("§7.4", "invalid released-wire history");
            }
        }
        let mut ids = Vec::with_capacity(n);
        let mut source = self.ids.iter();
        for i in 0..n {
            ids.push(if let Some(w) = removed.get(&i) {
                *w
            } else {
                *source.next().expect("restored wire count")
            });
        }
        match &mut self.state {
            State::Basis { bits, .. } => {
                let mut old = bits.iter();
                let next = (0..n)
                    .map(|i| {
                        if removed.contains_key(&i) {
                            false
                        } else {
                            *old.next().expect("basis width")
                        }
                    })
                    .collect();
                *bits = next;
            }
            State::Vector(vector) => {
                if n > 24 {
                    return err("§14.2", "restored state exceeds vector limit");
                }
                let mut next = vec![Complex::ZERO; 1usize << n];
                for (i, a) in vector.iter().enumerate() {
                    let mut bit = 0;
                    let mut destination = 0;
                    for pos in 0..n {
                        if !removed.contains_key(&pos) {
                            destination |= ((i >> bit) & 1) << pos;
                            bit += 1;
                        }
                    }
                    next[destination] = *a;
                }
                *vector = next;
            }
        }
        self.ids = ids;
        Ok(())
    }
    pub fn new() -> Self {
        Self {
            ids: Vec::new(),
            next: 0,
            state: State::Basis {
                bits: Vec::new(),
                phase: Complex::ONE,
            },
        }
    }
    pub fn wire_count(&self) -> usize {
        self.ids.len()
    }
    pub fn is_basis(&self) -> bool {
        matches!(self.state, State::Basis { .. })
    }
    pub fn allocate(&mut self, n: usize) -> Result<Vec<Wire>> {
        let end = self
            .next
            .checked_add(n as u64)
            .ok_or_else(|| Error("§4.3: wire identity overflow".into()))?;
        if let State::Vector(v) = &mut self.state {
            let bits = self
                .ids
                .len()
                .checked_add(n)
                .ok_or_else(|| Error("§14.2: vector size overflow".into()))?;
            if bits > 24 {
                return err("§14.2", "state-vector simulation limit is 24 live wires");
            }
            v.resize(1usize << bits, Complex::ZERO);
        } else if let State::Basis { bits, .. } = &mut self.state {
            bits.try_reserve(n)
                .map_err(|e| Error(format!("§4.3: wire allocation failed: {e}")))?;
            bits.resize(bits.len() + n, false);
        }
        let wires: Vec<_> = (self.next..end).collect();
        self.next = end;
        self.ids.extend(&wires);
        Ok(wires)
    }
    fn positions(&self, wires: &[Wire]) -> Result<Vec<usize>> {
        let mut seen = BTreeSet::new();
        wires
            .iter()
            .map(|w| {
                if !seen.insert(w) {
                    return err("§3.3", "duplicate wire operand");
                }
                self.ids
                    .iter()
                    .position(|n| n == w)
                    .ok_or_else(|| Error(format!("§3.3: dead or unknown wire {w}")))
            })
            .collect()
    }
    pub fn amplitudes(&self) -> Result<Vec<Complex>> {
        match &self.state {
            State::Vector(v) => Ok(v.clone()),
            State::Basis { bits, phase } => {
                if bits.len() > 24 {
                    return err(
                        "§14.2",
                        "basis tuple exceeds vector materialisation limit of 24 wires",
                    );
                }
                let mut out = vec![Complex::ZERO; 1usize << bits.len()];
                out[bits
                    .iter()
                    .enumerate()
                    .fold(0, |n, (i, b)| n | ((*b as usize) << i))] = *phase;
                Ok(out)
            }
        }
    }
    pub fn read_basis(&self, wires: &[Wire]) -> Result<u128> {
        if wires.len() > 128 {
            return err("§3.3", "integer bundle read exceeds 128 bits");
        }
        let positions = self.positions(wires)?;
        match &self.state {
            State::Basis { bits, .. } => Ok(positions
                .iter()
                .enumerate()
                .fold(0, |n, (i, p)| n | ((bits[*p] as u128) << i))),
            State::Vector(_) => err("§14.2", "basis read requested on a state vector"),
        }
    }
    pub fn release(&mut self, wires: &[Wire]) -> Result<()> {
        let positions = self.positions(wires)?;
        let mut remove = vec![false; self.ids.len()];
        for p in &positions {
            remove[*p] = true;
        }
        match &mut self.state {
            State::Basis { bits, .. } => {
                if positions.iter().any(|p| bits[*p]) {
                    return err("§4.3", "E_QREG_NOT_CLEAN: released wire is one");
                }
                let mut index = 0;
                bits.retain(|_| {
                    let keep = !remove[index];
                    index += 1;
                    keep
                });
            }
            State::Vector(v) => {
                if v.iter()
                    .enumerate()
                    .any(|(i, a)| positions.iter().any(|p| i & (1 << p) != 0) && a.norm2() > 1e-24)
                {
                    return err("§4.3", "E_QREG_NOT_CLEAN: released factor is not zero");
                }
                let mut next = vec![Complex::ZERO; 1usize << (self.ids.len() - positions.len())];
                for (i, a) in v.iter().enumerate() {
                    if positions.iter().all(|p| i & (1 << p) == 0) {
                        next[compress(i, &remove)] = *a;
                    }
                }
                *v = next;
            }
        }
        let mut index = 0;
        self.ids.retain(|_| {
            let keep = !remove[index];
            index += 1;
            keep
        });
        Ok(())
    }
    pub fn gate(
        &mut self,
        op: &str,
        wires: &[Wire],
        angle: Option<f64>,
        predicate: &[Wire],
    ) -> Result<()> {
        self.controlled_gate(
            op,
            wires,
            angle,
            &predicate.iter().map(|w| (*w, true)).collect::<Vec<_>>(),
        )
    }
    pub(crate) fn controlled_gate(
        &mut self,
        op: &str,
        wires: &[Wire],
        angle: Option<f64>,
        predicate: &[(Wire, bool)],
    ) -> Result<()> {
        let positions = self.positions(wires)?;
        let own = match op {
            "cx" => 1,
            "ccx" => 2,
            "mcx" => wires.len().saturating_sub(1),
            _ => 0,
        };
        let expected = match op {
            "x" | "h" | "s" | "sdg" | "t" | "tdg" | "rx" | "ry" | "rz" => 1,
            "cx" | "swap" | "cz" => 2,
            "ccx" => 3,
            "mcx" if !wires.is_empty() => wires.len(),
            _ => return err("§4.4", format!("unknown gate {op}")),
        };
        if wires.len() != expected {
            return err("§4.8", "wrong gate arity");
        }
        if matches!(op, "rx" | "ry" | "rz") && angle.is_none_or(|a| !a.is_finite()) {
            return err("§4.4", "rotation needs a finite angle");
        }
        let mut controls: Vec<_> = positions[..own].iter().map(|p| (*p, true)).collect();
        let targets = &positions[own..];
        for (w, value) in predicate {
            let p = self.positions(&[*w])?[0];
            if targets.contains(&p) {
                return err("§3.3", "effective control aliases target");
            }
            if !controls.contains(&(p, *value)) {
                controls.push((p, *value));
            }
        }
        let active = |bits: &[bool]| controls.iter().all(|(p, v)| bits[*p] == *v);
        let permutation = matches!(op, "x" | "cx" | "ccx" | "mcx" | "swap");
        if let State::Basis { bits, phase } = &mut self.state {
            if !active(bits) {
                return Ok(());
            }
            if permutation {
                if op == "swap" {
                    bits.swap(targets[0], targets[1]);
                } else {
                    bits[targets[0]] ^= true;
                }
                return Ok(());
            }
            if !matches!(op, "h" | "rx" | "ry") {
                let theta = match op {
                    "s" => std::f64::consts::FRAC_PI_2,
                    "sdg" => -std::f64::consts::FRAC_PI_2,
                    "t" => std::f64::consts::FRAC_PI_4,
                    "tdg" => -std::f64::consts::FRAC_PI_4,
                    "cz" => {
                        if bits[targets[0]] && bits[targets[1]] {
                            std::f64::consts::PI
                        } else {
                            0.0
                        }
                    }
                    "rz" => angle.expect("angle") * if bits[targets[0]] { 0.5 } else { -0.5 },
                    _ => 0.0,
                };
                if op == "rz" || op == "cz" || bits[targets[0]] {
                    *phase = *phase * Complex::phase(theta);
                }
                return Ok(());
            }
        }
        if matches!(self.state, State::Basis { .. }) {
            self.state = State::Vector(self.amplitudes()?);
        }
        let State::Vector(vector) = &mut self.state else {
            unreachable!("materialised vector")
        };
        let enabled = |index: usize| {
            controls
                .iter()
                .all(|(p, v)| (index & (1usize << p) != 0) == *v)
        };
        if op == "swap" {
            let (a, b) = (1usize << targets[0], 1usize << targets[1]);
            for i in 0..vector.len() {
                if enabled(i) && i & a == 0 && i & b != 0 {
                    vector.swap(i, i ^ a ^ b);
                }
            }
            return Ok(());
        }
        if op == "cz" {
            for (i, a) in vector.iter_mut().enumerate() {
                if enabled(i) && targets.iter().all(|p| i & (1usize << p) != 0) {
                    *a = a.scale(-1.0);
                }
            }
            return Ok(());
        }
        let zero = Complex::ZERO;
        let one = Complex::ONE;
        let h = std::f64::consts::FRAC_1_SQRT_2;
        let matrix = match op {
            "x" | "cx" | "ccx" | "mcx" => [zero, one, one, zero],
            "h" => [one.scale(h), one.scale(h), one.scale(h), one.scale(-h)],
            "s" => [one, zero, zero, Complex::new(0.0, 1.0)],
            "sdg" => [one, zero, zero, Complex::new(0.0, -1.0)],
            "t" => [one, zero, zero, Complex::phase(std::f64::consts::FRAC_PI_4)],
            "tdg" => [
                one,
                zero,
                zero,
                Complex::phase(-std::f64::consts::FRAC_PI_4),
            ],
            "rx" => {
                let a = angle.expect("angle") / 2.0;
                [
                    one.scale(a.cos()),
                    Complex::new(0.0, -a.sin()),
                    Complex::new(0.0, -a.sin()),
                    one.scale(a.cos()),
                ]
            }
            "ry" => {
                let a = angle.expect("angle") / 2.0;
                [
                    one.scale(a.cos()),
                    one.scale(-a.sin()),
                    one.scale(a.sin()),
                    one.scale(a.cos()),
                ]
            }
            "rz" => {
                let a = angle.expect("angle") / 2.0;
                [Complex::phase(-a), zero, zero, Complex::phase(a)]
            }
            _ => unreachable!("gate validated"),
        };
        let bit = 1usize << targets[0];
        for i in 0..vector.len() {
            if i & bit == 0 && enabled(i) {
                let a = vector[i];
                let b = vector[i | bit];
                vector[i] = matrix[0] * a + matrix[1] * b;
                vector[i | bit] = matrix[2] * a + matrix[3] * b;
            }
        }
        Ok(())
    }
    pub fn measurement_branches(&self, wires: &[Wire]) -> Result<Vec<MeasurementBranch>> {
        let positions = self.positions(wires)?;
        let mut remove = vec![false; self.ids.len()];
        for p in &positions {
            remove[*p] = true;
        }
        if let State::Basis { bits, phase } = &self.state {
            let mut state = self.clone();
            let result = positions.iter().map(|p| bits[*p]).collect();
            let kept: Vec<_> = bits
                .iter()
                .enumerate()
                .filter_map(|(p, b)| (!remove[p]).then_some(*b))
                .collect();
            state.ids = self
                .ids
                .iter()
                .enumerate()
                .filter_map(|(p, w)| (!remove[p]).then_some(*w))
                .collect();
            state.state = State::Basis {
                bits: kept,
                phase: *phase,
            };
            return Ok(vec![MeasurementBranch {
                probability: 1.0,
                bits: result,
                state,
            }]);
        }
        if wires.len() > 24 {
            return err("§14.2", "measurement outcome enumeration exceeds 24 wires");
        }
        let vector = self.amplitudes()?;
        let mut probabilities = vec![0.0; 1usize << positions.len()];
        let outcome = |i: usize| {
            positions
                .iter()
                .enumerate()
                .fold(0, |n, (j, p)| n | (((i >> p) & 1) << j))
        };
        for (i, a) in vector.iter().enumerate() {
            probabilities[outcome(i)] += a.norm2();
        }
        let mut branches = Vec::new();
        for (k, probability) in probabilities.into_iter().enumerate() {
            if probability == 0.0 {
                continue;
            }
            let mut amplitudes = vec![Complex::ZERO; 1usize << (self.ids.len() - positions.len())];
            for (i, a) in vector.iter().enumerate() {
                if outcome(i) == k {
                    amplitudes[compress(i, &remove)] = a.scale(1.0 / probability.sqrt());
                }
            }
            let mut state = self.clone();
            state.ids = self
                .ids
                .iter()
                .enumerate()
                .filter_map(|(p, w)| (!remove[p]).then_some(*w))
                .collect();
            state.state = State::Vector(amplitudes);
            branches.push(MeasurementBranch {
                probability,
                bits: (0..positions.len())
                    .map(|i| k & (1usize << i) != 0)
                    .collect(),
                state,
            });
        }
        Ok(branches)
    }
    pub(crate) fn permute(
        &mut self,
        mut permutation: impl FnMut(&[bool]) -> Result<Vec<bool>>,
    ) -> Result<()> {
        match &mut self.state {
            State::Basis { bits, .. } => {
                let next = permutation(bits)?;
                if next.len() != bits.len() {
                    return err("§14.2", "permutation changes wire count");
                }
                *bits = next;
            }
            State::Vector(v) => {
                let mut out = vec![Complex::ZERO; v.len()];
                let mut seen = vec![false; v.len()];
                for (i, a) in v.iter().enumerate() {
                    let bits: Vec<_> = (0..self.ids.len())
                        .map(|p| i & (1usize << p) != 0)
                        .collect();
                    let mapped = permutation(&bits)?;
                    if mapped.len() != self.ids.len() {
                        return err("§14.2", "permutation changes wire count");
                    }
                    let j = mapped
                        .iter()
                        .enumerate()
                        .fold(0, |n, (p, b)| n | ((*b as usize) << p));
                    if seen[j] {
                        return err("§5.3", "action mapping is not a permutation");
                    }
                    seen[j] = true;
                    out[j] = *a;
                }
                *v = out;
            }
        }
        Ok(())
    }
    pub(crate) fn position(&self, w: Wire) -> Result<usize> {
        Ok(self.positions(&[w])?[0])
    }
}
fn compress(index: usize, remove: &[bool]) -> usize {
    let mut out = 0;
    let mut next = 0;
    for (p, removed) in remove.iter().enumerate() {
        if !removed {
            out |= ((index >> p) & 1) << next;
            next += 1;
        }
    }
    out
}
````

## `src/registers.rs` (245 lines)

````rust
//! CC quantum-register ownership and the reversible handle transitions of §3.3.
use crate::{err, quantum::Wire, Error, QuantumState, Result};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Clone, Debug, PartialEq, Eq)]
enum Status {
    Live,
    Viewed,
    Consumed,
}
#[derive(Clone, Debug, PartialEq, Eq)]
struct Handle {
    wires: Vec<Wire>,
    status: Status,
    parent: Option<u64>,
}
#[derive(Clone, Debug, PartialEq)]
pub struct QuantumRegisters {
    pub(crate) state: QuantumState,
    handles: BTreeMap<u64, Handle>,
    next: u64,
}
impl Default for QuantumRegisters {
    fn default() -> Self {
        Self::new()
    }
}
#[derive(Clone, Debug)]
enum KernelUndo {
    None,
    Allocation(Vec<Wire>),
    Release(Vec<(usize, Wire)>),
}
#[derive(Clone, Debug)]
pub(crate) struct RegisterUndo {
    handles: Vec<(u64, Option<Handle>)>,
    next: u64,
    wire_next: u64,
    kernel: KernelUndo,
}

impl QuantumRegisters {
    pub fn new() -> Self {
        Self {
            state: QuantumState::new(),
            handles: BTreeMap::new(),
            next: 1,
        }
    }
    pub fn quantum_state(&self) -> &QuantumState {
        &self.state
    }
    pub fn prepare(&mut self, id: u64, bits: &[bool]) -> Result<()> {
        let wires = self.ordinary(id)?.wires.clone();
        if wires.len() != bits.len() {
            return err("§10", "E_ARG: preparation width mismatch");
        }
        let mut check = self.state.clone();
        check.release(&wires)?;
        for (wire, bit) in wires.iter().zip(bits) {
            if *bit {
                self.state.gate("x", &[*wire], None, &[])?;
            }
        }
        Ok(())
    }
    pub fn bundle(&self, id: u64) -> Result<&[Wire]> {
        let h = self
            .handles
            .get(&id)
            .filter(|h| h.status == Status::Live)
            .ok_or_else(|| Error(format!("§3.3: qreg {id} is not live")))?;
        Ok(&h.wires)
    }
    fn ordinary(&self, id: u64) -> Result<&Handle> {
        self.bundle(id)?;
        let h = &self.handles[&id];
        if h.parent.is_some() {
            return err(
                "§3.3",
                "a qreg view may only be used by its one region call",
            );
        }
        Ok(h)
    }
    pub(crate) fn idle_bundle(&self,id:u64)->Result<&[Wire]>{Ok(&self.ordinary(id)?.wires)}
    fn record(&self, ids: &[u64]) -> RegisterUndo {
        RegisterUndo {
            handles: ids
                .iter()
                .map(|id| (*id, self.handles.get(id).cloned()))
                .collect(),
            next: self.next,
            wire_next: self.state.next_wire_id(),
            kernel: KernelUndo::None,
        }
    }
    fn create(&mut self, wires: Vec<Wire>, parent: Option<u64>) -> Result<u64> {
        let id = self.next;
        let next = id
            .checked_add(1)
            .ok_or_else(|| Error("§3.3: qreg identity overflow".into()))?;
        self.handles.insert(
            id,
            Handle {
                wires,
                status: Status::Live,
                parent,
            },
        );
        self.next = next;
        Ok(id)
    }
    pub fn allocate(&mut self, n: usize) -> Result<u64> {
        Ok(self.allocate_recorded(n)?.0)
    }
    pub(crate) fn allocate_recorded(&mut self, n: usize) -> Result<(u64, RegisterUndo)> {
        let mut undo = self.record(&[self.next]);
        let wires = self.state.allocate(n)?;
        undo.kernel = KernelUndo::Allocation(wires.clone());
        let id = self.create(wires, None)?;
        Ok((id, undo))
    }
    pub fn free(&mut self, id: u64) -> Result<()> {
        self.free_recorded(id).map(|_| ())
    }
    pub(crate) fn free_recorded(&mut self, id: u64) -> Result<RegisterUndo> {
        let wires = self.ordinary(id)?.wires.clone();
        let mut undo = self.record(&[id]);
        let positions = wires
            .iter()
            .map(|w| Ok((self.state.position(*w)?, *w)))
            .collect::<Result<Vec<_>>>()?;
        self.state.release(&wires)?;
        self.handles.get_mut(&id).expect("live handle").status = Status::Consumed;
        undo.kernel = KernelUndo::Release(positions);
        Ok(undo)
    }
    pub fn slice(&mut self, id: u64, lo: usize, len: usize) -> Result<u64> {
        Ok(self.slice_recorded(id, lo, len)?.0)
    }
    pub(crate) fn slice_recorded(
        &mut self,
        id: u64,
        lo: usize,
        len: usize,
    ) -> Result<(u64, RegisterUndo)> {
        let h = self.ordinary(id)?;
        let end = lo
            .checked_add(len)
            .filter(|end| *end <= h.wires.len())
            .ok_or_else(|| Error("§3.3: qreg slice out of bounds".into()))?;
        let wires = h.wires[lo..end].to_vec();
        let undo = self.record(&[id, self.next]);
        self.handles.get_mut(&id).expect("live parent").status = Status::Viewed;
        let view = self.create(wires, Some(id))?;
        Ok((view, undo))
    }
    pub fn concat(&mut self, a: u64, b: u64) -> Result<u64> {
        Ok(self.concat_recorded(a, b)?.0)
    }
    pub(crate) fn concat_recorded(&mut self, a: u64, b: u64) -> Result<(u64, RegisterUndo)> {
        if a == b {
            return err("§3.3", "qreg concat operands alias");
        }
        let mut wires = self.ordinary(a)?.wires.clone();
        wires.extend(&self.ordinary(b)?.wires);
        if wires.iter().collect::<BTreeSet<_>>().len() != wires.len() {
            return err("§3.3", "qreg concat wires overlap");
        }
        let undo = self.record(&[a, b, self.next]);
        self.handles.get_mut(&a).expect("handle").status = Status::Consumed;
        self.handles.get_mut(&b).expect("handle").status = Status::Consumed;
        let id = self.create(wires, None)?;
        Ok((id, undo))
    }
    pub fn complete_call(&mut self, ids: &[u64]) -> Result<()> {
        self.complete_call_recorded(ids).map(|_| ())
    }
    pub(crate) fn complete_call_recorded(&mut self, ids: &[u64]) -> Result<RegisterUndo> {
        let mut affected = Vec::new();
        let mut wires = BTreeSet::new();
        for id in ids {
            for wire in self.bundle(*id)? {
                if !wires.insert(*wire) {
                    return err("§3.3", "region interface qregs overlap");
                }
            }
            affected.push(*id);
            if let Some(parent) = self.handles[id].parent {
                affected.push(parent);
            }
        }
        let undo = self.record(&affected);
        for id in ids {
            if let Some(parent) = self.handles[id].parent {
                self.handles.get_mut(id).expect("view").status = Status::Consumed;
                self.handles.get_mut(&parent).expect("parent").status = Status::Live;
            }
        }
        Ok(undo)
    }
    pub(crate) fn measure(&mut self, id: u64, draw: f64) -> Result<Vec<bool>> {
        if !(0.0..1.0).contains(&draw) {
            return err("§14.2", "measurement draw outside [0,1)");
        }
        let wires = self.ordinary(id)?.wires.clone();
        let branches = self.state.measurement_branches(&wires)?;
        let mut cursor = draw;
        let mut selected = None;
        for branch in branches {
            cursor -= branch.probability;
            let last = branch.probability > 0.0;
            if cursor < 0.0 {
                selected = Some(branch);
                break;
            }
            if last {
                selected = Some(branch);
            }
        }
        let branch =
            selected.ok_or_else(|| Error("§14.2: measurement has no nonzero outcome".into()))?;
        self.state = branch.state;
        self.handles.get_mut(&id).expect("handle").status = Status::Consumed;
        Ok(branch.bits)
    }
    pub(crate) fn undo(&mut self, undo: RegisterUndo) -> Result<()> {
        match undo.kernel {
            KernelUndo::None => {}
            KernelUndo::Allocation(wires) => self.state.release(&wires)?,
            KernelUndo::Release(positions) => self.state.restore_clean(&positions)?,
        };
        for (id, prior) in undo.handles {
            if let Some(prior) = prior {
                self.handles.insert(id, prior);
            } else {
                self.handles.remove(&id);
            }
        }
        self.next = undo.next;
        self.state.restore_next_wire_id(undo.wire_next)?;
        Ok(())
    }
}
````

## `src/sha256.rs` (89 lines)

````rust
//! FIPS 180-4, sections 4.2.2, 5 and 6.2. All arithmetic is modulo 2^32.
const K: [u32; 64] = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
];

pub fn sha256(input: &[u8]) -> [u8; 32] {
    let mut h = [
        0x6a09e667u32,
        0xbb67ae85,
        0x3c6ef372,
        0xa54ff53a,
        0x510e527f,
        0x9b05688c,
        0x1f83d9ab,
        0x5be0cd19,
    ];
    let length = u64::try_from(input.len())
        .expect("SHA-256 input length fits u64")
        .checked_mul(8)
        .expect("SHA-256 input shorter than 2^64 bits");
    let blocks = (input.len() + 9).div_ceil(64);
    for block in 0..blocks {
        let mut bytes = [0u8; 64];
        for (j, b) in bytes.iter_mut().enumerate() {
            let i = block * 64 + j;
            *b = if i < input.len() {
                input[i]
            } else if i == input.len() {
                0x80
            } else {
                0
            };
        }
        if block + 1 == blocks {
            bytes[56..].copy_from_slice(&length.to_be_bytes());
        }
        let mut w = [0u32; 64];
        for (i, chunk) in bytes.as_chunks::<4>().0.iter().enumerate() {
            w[i] = u32::from_be_bytes(*chunk);
        }
        for t in 16..64 {
            let s0 = w[t - 15].rotate_right(7) ^ w[t - 15].rotate_right(18) ^ (w[t - 15] >> 3);
            let s1 = w[t - 2].rotate_right(17) ^ w[t - 2].rotate_right(19) ^ (w[t - 2] >> 10);
            w[t] = w[t - 16]
                .wrapping_add(s0)
                .wrapping_add(w[t - 7])
                .wrapping_add(s1);
        }
        let [mut a, mut b, mut c, mut d, mut e, mut f, mut g, mut hh] = h;
        for t in 0..64 {
            let sum1 = e.rotate_right(6) ^ e.rotate_right(11) ^ e.rotate_right(25);
            let ch = (e & f) ^ (!e & g);
            let t1 = hh
                .wrapping_add(sum1)
                .wrapping_add(ch)
                .wrapping_add(K[t])
                .wrapping_add(w[t]);
            let sum0 = a.rotate_right(2) ^ a.rotate_right(13) ^ a.rotate_right(22);
            let maj = (a & b) ^ (a & c) ^ (b & c);
            let t2 = sum0.wrapping_add(maj);
            hh = g;
            g = f;
            f = e;
            e = d.wrapping_add(t1);
            d = c;
            c = b;
            b = a;
            a = t1.wrapping_add(t2);
        }
        for (v, x) in h.iter_mut().zip([a, b, c, d, e, f, g, hh]) {
            *v = v.wrapping_add(x);
        }
    }
    let mut out = [0; 32];
    for (bytes, n) in out.as_chunks_mut::<4>().0.iter_mut().zip(h) {
        bytes.copy_from_slice(&n.to_be_bytes());
    }
    out
}
pub fn sha256_hex(input: &[u8]) -> String {
    sha256(input).iter().map(|b| format!("{b:02x}")).collect()
}
````

## `src/validation.rs` (1258 lines)

````rust
//! Operand schemas and static discipline. Dynamic cleanliness is also checked
//! by executors; accepting a text object does not waive those obligations.
use crate::{
    err,
    object::{integer, is_binop, is_div, list, name},
    Error, Function, Instruction, Object, Result, Type,
};
use std::collections::{BTreeMap, BTreeSet};

impl Object {
    pub(crate) fn validate_structured(
        &self,
        f: &Function,
        types: &mut BTreeMap<String, Type>,
        labels: &BTreeSet<&String>,
    ) -> Result<()> {
        if matches!(f.kind.as_str(), "cc" | "r") {
            return self.validate_classical(f, types, labels);
        }
        let mut state = Discipline::new(f, types.clone());
        for b in &f.blocks {
            if !b.params.is_empty() {
                return err("§5.1", "action blocks cannot have classical parameters");
            }
            self.validate_action_sequence(f, &b.instructions, &mut state)?;
        }
        if !state.predicates.is_empty() {
            return err("§3.5", "unclosed predicate stack");
        }
        if !state.created.is_empty() {
            return err(
                "§5.1",
                format!(
                    "unreleased workspace {:?}",
                    state.created.keys().collect::<Vec<_>>()
                ),
            );
        }
        if state.bounds != f.bounds {
            return err("§5.3", "declared bounds do not equal loops in text order");
        }
        self.validate_borrow_frames(f)?;
        Ok(())
    }
    fn validate_action_sequence(
        &self,
        f: &Function,
        seq: &[Instruction],
        s: &mut Discipline,
    ) -> Result<()> {
        for i in seq {
            let op = i.op.as_str();
            let a = &i.operands;
            let arity = |n: usize, lhs: usize| -> Result<()> {
                if a.len() != n || i.lhs.len() != lhs {
                    err("§4.8", format!("{op}: wrong arity at line {}", i.line))
                } else {
                    Ok(())
                }
            };
            let scalar = |s: &Discipline, n: &str| -> Result<()> {
                if s.wires(n)?.len() != 1 {
                    err("§3.3", format!("{n} must name one wire"))
                } else {
                    Ok(())
                }
            };
            if !matches!(op, "qif" | "qloop") && !i.bodies.is_empty() {
                return err("§4.8", "opcode does not take a structured body");
            }
            match op {
                "qif" => {
                    arity(1, 0)?;
                    scalar(s, &a[0])?;
                    if i.bodies.len() != 2 {
                        return err("§4.8", "qif needs two arms");
                    }
                    s.predicates.push(a[0].clone());
                    for body in &i.bodies {
                        self.validate_action_sequence(f, body, s)?;
                    }
                    if s.predicates.pop().as_deref() != Some(&a[0]) {
                        return err("§3.5", "qif body altered predicate stack");
                    }
                }
                "qloop" => {
                    if !i.lhs.is_empty() || !matches!(a.len(), 1 | 3) || i.bodies.len() != 1 {
                        return err("§4.8", "qloop arity/body mismatch");
                    }
                    let n = a[0].parse::<u64>().map_err(|_| {
                        Error("§4.8: loop count must be nonnegative literal".into())
                    })?;
                    s.bounds.push(n);
                    if a.len() == 3 {
                        if a[1] != "while" || s.wires(&a[2])?.len() as u64 != n {
                            return err("§4.6", "qloop selector width mismatch");
                        }
                        s.predicates.push(a[2].clone());
                    }
                    self.validate_action_sequence(f, &i.bodies[0], s)?;
                    if a.len() == 3 && s.predicates.pop().as_deref() != Some(&a[2]) {
                        return err("§3.5", "loop predicate stack mismatch");
                    }
                }
                "qpred" => {
                    arity(1, 0)?;
                    scalar(s, &a[0])?;
                    s.predicates.push(a[0].clone());
                }
                "qunpred" => {
                    arity(1, 0)?;
                    if s.predicates.pop().as_deref() != Some(&a[0]) {
                        return err("§3.5", "unmatched predicate pop");
                    }
                }
                "qalloc" | "qborrow" => {
                    arity(2, 1)?;
                    if !name(&a[0]) {
                        return err("§4.8", "invalid wire class");
                    }
                    let n = a[1]
                        .parse::<u16>()
                        .map_err(|_| Error("§3.3: invalid allocation width".into()))?;
                    if n == 0 {
                        return err("§3.3", "allocation width must be positive");
                    }
                    s.produce(
                        &i.lhs[0],
                        Type::Wire(n),
                        Creation {
                            kind: op.into(),
                            sources: Vec::new(),
                            versions: Vec::new(),
                            controls: Vec::new(),
                        },
                    )?;
                }
                "qfree" | "qreturn" => {
                    arity(1, 0)?;
                    s.check_target(&a[0], false)?;
                    let c = s
                        .created
                        .get(&a[0])
                        .ok_or_else(|| Error("§3.3: release of non-workspace value".into()))?;
                    if c.kind != if op == "qreturn" { "qborrow" } else { "qalloc" } {
                        return err("§5.1", "allocation/release kind mismatch");
                    }
                    if s.wires(&a[0])?
                        .iter()
                        .any(|w| !s.versions.get(w).is_none_or(Vec::is_empty))
                    {
                        return err("§6.2", "released value has not been uncomputed");
                    }
                    s.consume(&a[0])?;
                }
                "qcopy" => {
                    arity(1, 1)?;
                    let wires = s.wires(&a[0])?;
                    s.disjoint(&[a[0].as_str()])?;
                    let c = Creation {
                        kind: op.into(),
                        sources: vec![a[0].clone()],
                        versions: s.snapshot(&wires),
                        controls: s.predicates.clone(),
                    };
                    s.produce(&i.lhs[0], Type::Wire(wires.len() as u16), c)?;
                }
                "quncopy" => {
                    arity(2, 0)?;
                    s.check_target(&a[1], false)?;
                    s.disjoint(&[&a[0], &a[1]])?;
                    let c = s
                        .created
                        .get(&a[1])
                        .ok_or_else(|| Error("§6.2: unmatched quncopy".into()))?;
                    if c.kind != "qcopy"
                        || c.sources != vec![a[0].clone()]
                        || c.versions != s.snapshot(&s.wires(&a[0])?)
                        || c.controls != s.predicates
                        || s.wires(&a[1])?
                            .iter()
                            .any(|w| !s.versions.get(w).is_none_or(Vec::is_empty))
                        || s.wires(&a[0])?.iter().any(|w| s.closed.contains(w))
                    {
                        return err("§6.2", "quncopy outside its computing window");
                    }
                    s.consume(&a[1])?;
                }
                "qregion" => {
                    if !i.lhs.is_empty() || !matches!(a.len(), 3 | 4) || !name(&a[0]) {
                        return err("§4.8", "qregion operand schema");
                    }
                    let aw = a[1]
                        .parse::<u16>()
                        .map_err(|_| Error("§4.8: qregion address width".into()))?;
                    let w = a[2]
                        .parse::<u16>()
                        .map_err(|_| Error("§4.8: qregion cell width".into()))?;
                    if aw > 127 || w == 0 {
                        return err("§3.3", "invalid region dimensions");
                    }
                    if a.len() == 4 {
                        let img = a[3]
                            .strip_prefix('@')
                            .ok_or_else(|| Error("§4.6: unknown qregion image".into()))?;
                        let size=self.data_size(img)?;
                        let bits = (1u128 << aw)
                            .checked_mul(w as u128)
                            .ok_or_else(|| Error("§4.6: image size overflow".into()))?;
                        if bits % 8 != 0 || bits / 8 != size {
                            return err("§4.6", "image size mismatch");
                        }
                    }
                    if s.types.insert(a[0].clone(), Type::Region(aw, w)).is_some() {
                        return err("§3.3", "region name already defined");
                    }
                }
                "qload" | "qunload" | "qstore" | "qexchm" => {
                    let load = op == "qload";
                    arity(if load { 2 } else { 3 }, if load { 1 } else { 0 })?;
                    let (aw, w) = match s.types.get(&a[0]) {
                        Some(Type::Region(aw, w)) => (*aw, *w),
                        _ => return err("§3.3", "unknown region"),
                    };
                    if s.wires(&a[1])?.len() != aw as usize {
                        return err("§3.3", "memory address width mismatch");
                    }
                    if load {
                        let mut deps = s.wires(&a[1])?;
                        deps.push(format!("{}[*]", a[0]));
                        s.produce(
                            &i.lhs[0],
                            Type::Wire(w),
                            Creation {
                                kind: op.into(),
                                sources: a.clone(),
                                versions: s.snapshot(&deps),
                                controls: s.predicates.clone(),
                            },
                        )?;
                    } else {
                        if s.wires(&a[2])?.len() != w as usize {
                            return err("§3.3", "memory value width mismatch");
                        }
                        s.disjoint(&[&a[1], &a[2]])?;
                        if op == "qunload" {
                            s.check_target(&a[2], false)?;
                            let c = s
                                .created
                                .get(&a[2])
                                .ok_or_else(|| Error("§6.2: unmatched qunload".into()))?;
                            let mut deps = s.wires(&a[1])?;
                            deps.push(format!("{}[*]", a[0]));
                            if c.kind != "qload"
                                || c.sources != a[..2]
                                || c.controls != s.predicates
                                || c.versions != s.snapshot(&deps)
                            {
                                return err("§6.2", "qunload outside computing window");
                            }
                            s.consume(&a[2])?;
                        } else {
                            if s.inputs.contains(&a[0]) {
                                return err("§5.1", "in region cannot be modified by action");
                            }
                            s.versions
                                .entry(format!("{}[*]", a[0]))
                                .or_default()
                                .push(format!("{}:{}", op, i.line));
                            if op == "qexchm" {
                                s.change(&a[2], format!("{op}:{}", a.join(" ")), false)?;
                            }
                        }
                    }
                }
                "qinplace" => {
                    arity(4, 0)?;
                    for callee in &a[..2] {
                        let callee = callee
                            .strip_prefix('@')
                            .and_then(|n| self.functions.get(n))
                            .filter(|f| f.kind == "oracle")
                            .ok_or_else(|| Error("§4.5: qinplace requires oracle pair".into()))?;
                        if callee.params[0].len() != 1
                            || callee.params[0][0].ty != callee.params[1][0].ty
                        {
                            return err(
                                "§4.5",
                                "qinplace requires equal-width single-input oracles",
                            );
                        }
                    }
                    if s.types.get(&a[2]) != Some(&Type::Token) {
                        return err("§3.3", "qinplace token operand");
                    }
                    s.change(&a[3], format!("qinplace:{}", a.join(" ")), false)?;
                }
                "oracle_call" | "action_call" | "adj" | "ctl" => {
                    let call = normalize_call(i)?;
                    if let Some(control) = call.control.as_ref() {
                        scalar(s, control)?;
                        s.predicates.push(control.clone());
                    }
                    self.validate_region_call(f, &call.instruction, &s.types)?;
                    let context = s
                        .predicates
                        .iter()
                        .map(|p| s.wires(p))
                        .collect::<Result<Vec<_>>>()?
                        .concat();
                    self.validate_inherited_targets(&call.instruction, &context, &s.types)?;
                    let callee =
                        self.declaration(call.instruction.operands[0].trim_start_matches('@'))?;
                    if f.kind == "perm_action" && callee.kind == "action" {
                        return err("§5.3", "permutation action calls non-permutation action");
                    }
                    let ca = &call.instruction.operands;
                    let targets = if call.instruction.op == "oracle_call" {
                        vec![ca[3].clone(), ca[4].clone()]
                    } else {
                        list(&ca[1])?
                    };
                    for target in targets {
                        let other = callee.kind == "action";
                        s.change(
                            &target,
                            format!(
                                "call_{}_{}:{}:{:?}",
                                if other { "other" } else { "perm" },
                                if call.adjoint { "adj" } else { "fwd" },
                                ca.join(" "),
                                s.predicates
                            ),
                            other,
                        )?;
                    }
                    if call.control.is_some() {
                        s.predicates.pop();
                    }
                }
                _ if gate(op) => {
                    if matches!(op,"rx"|"ry"|"rz")&&a.first().is_some_and(|angle|angle.parse::<f64>().is_err())&&s.types.get(&a[0])!=Some(&Type::F64){return err("§3.3","gate angle must be a classical f64 argument");}
                    let (controls, targets, diagonal, other) = gate_operands(i)?;
                    if f.kind == "perm_action" && (diagonal || other) {
                        return err("§5.3", "permutation action contains non-permutation gate");
                    }
                    let all: Vec<_> = controls
                        .iter()
                        .chain(&targets)
                        .map(String::as_str)
                        .collect();
                    for w in &all {
                        scalar(s, w)?;
                    }
                    s.disjoint(&all)?;
                    let mut normalized = a.clone();
                    if matches!(op, "rx" | "ry" | "rz") {
                        if let Ok(angle) = a[0].parse::<f64>() {
                            normalized[0] = format!("#{:016x}", angle.to_bits());
                        }
                    }
                    let version = format!(
                        "{op}:{}:{:?}:{:?}",
                        normalized.join(" "),
                        s.snapshot(
                            &controls
                                .iter()
                                .flat_map(|w| s.wires(w).unwrap_or_default())
                                .collect::<Vec<_>>()
                        ),
                        s.predicates
                    );
                    for t in targets {
                        s.check_target(&t, diagonal)?;
                        if !diagonal {
                            s.change(&t, version.clone(), other)?;
                        } else if s.is_other(&t)? {
                            s.record_change(&t, version.clone())?;
                        }
                    }
                }
                "qxor" | "qexch" => {
                    arity(2, 0)?;
                    s.disjoint(&[&a[0], &a[1]])?;
                    if s.wires(&a[0])?.len() != s.wires(&a[1])?.len() {
                        return err("§3.3", "bundle widths differ");
                    }
                    s.check_target(&a[1], false)?;
                    let version = format!(
                        "{op}:{}:{:?}:{:?}",
                        a.join(" "),
                        s.snapshot(&s.wires(&a[0])?),
                        s.predicates
                    );
                    s.change(&a[1], version.clone(), false)?;
                    if op == "qexch" {
                        s.check_target(&a[0], false)?;
                        s.change(&a[0], version, false)?;
                    }
                }
                "measure" | "effect" | "br" | "call" | "uncall" | "ret" | "trap" | "hostcall" => {
                    return err("§5.1", "classical instruction inside Q region")
                }
                _ => return err("§4.8", format!("unknown or disallowed action opcode {op}")),
            }
        }
        Ok(())
    }
    pub(crate) fn validate_region_call(
        &self,
        f: &Function,
        i: &Instruction,
        types: &BTreeMap<String, Type>,
    ) -> Result<()> {
        let a = &i.operands;
        let oracle = matches!(
            i.op.as_str(),
            "oracle_call" | "lift.oracle_call" | "lift.oracle_uncall"
        );
        if !i.lhs.is_empty() || a.len() != if oracle { 7 } else { 5 } {
            return err("§4.8", "region call arity mismatch");
        }
        let n = a[0]
            .strip_prefix('@')
            .ok_or_else(|| Error("§4.8: call requires @symbol".into()))?;
        let callee = self.declaration(n)?;
        if oracle && callee.kind != "oracle"
            || !oracle && !matches!(callee.kind.as_str(), "action" | "perm_action")
        {
            return err("§4.8", "region call kind mismatch");
        }
        if i.op == "lift.perm_call" && callee.kind != "perm_action" {
            return err("§5.2", "lifted bodies require exact permutation callees");
        }
        let mut values = Vec::new();
        if oracle {
            if types.get(&a[1]) != Some(&Type::Token) {
                return err("§3.3", "oracle call token must be classical token");
            }
            values.push((list(&a[2])?, &callee.params[0]));
            values.push((vec![a[3].clone()], &callee.params[1]));
            values.push((vec![a[4].clone()], &callee.params[2]));
            values.push((list(&a[5])?, &callee.params[3]));
            values.push((list(&a[6])?, &callee.params[4]));
        } else {
            for (index, ps) in callee.params[..4].iter().enumerate() {
                values.push((list(&a[index + 1])?, ps));
            }
        }
        let lifted = matches!(f.kind.as_str(), "oracle" | "lproc");
        let mut wires = BTreeSet::new();
        for (vs, ps) in values {
            if vs.len() != ps.len() {
                return err("§3.3", "region call operand count differs from signature");
            }
            for (v, p) in vs.iter().zip(ps) {
                let ty = types
                    .get(v)
                    .ok_or_else(|| Error(format!("§3.3: unknown call operand {v}")))?;
                let compatible = match (&p.ty, ty) {
                    (Type::Wire(n), Type::Wire(m)) | (Type::Wire(n), Type::Reg(m)) => n == m,
                    (Type::Wire(n), Type::Qreg(m)) => *n as u64 == *m,
                    (Type::Region(a, w), Type::Region(b, z)) => a == b && w == z,
                    (Type::Region(a, w), Type::Qreg(n)) => {
                        *a < 64 && (1u128 << *a) * (*w as u128) == *n as u128
                    }
                    _ => &p.ty == ty,
                };
                if !compatible {
                    return err("§3.3", "region call operand type/width mismatch");
                }
                if matches!(
                    ty,
                    Type::Wire(_) | Type::Reg(_) | Type::Qreg(_) | Type::Region(..)
                ) && !wires.insert(v.clone())
                {
                    return err("§3.3", "region interface operands alias");
                }
                if let Type::Region(..) = ty {
                    let caller = f
                        .params
                        .iter()
                        .flatten()
                        .find(|p| &p.name == v)
                        .ok_or_else(|| {
                            Error("§3.3: memory call operand is not caller interface".into())
                        })?;
                    if p.role.as_deref() == Some("mut") && caller.role.as_deref() == Some("in") {
                        return err("§3.3", "in region passed to mut slot");
                    }
                }
                if lifted
                    && matches!(p.ty, Type::Wire(_))
                    && !f.locations().iter().any(|l| &l.name == v)
                    && p.role.as_deref() != Some("in")
                {
                    return err("§3.7", "callee outputs require writable caller locations");
                }
            }
        }
        Ok(())
    }
    fn validate_classical(
        &self,
        f: &Function,
        types: &mut BTreeMap<String, Type>,
        labels: &BTreeSet<&String>,
    ) -> Result<()> {
        for b in &f.blocks {
            for p in &b.params {
                if types.insert(p.name.clone(), p.ty.clone()).is_some() {
                    return err("§3.3", "duplicate SSA definition");
                }
            }
        }
        for b in &f.blocks {
            for (ordinal, i) in b.instructions.iter().enumerate() {
                let op = i.op.as_str();
                let a = &i.operands;
                let arity = |n: usize, lhs: usize| -> Result<()> {
                    if a.len() != n || i.lhs.len() != lhs {
                        err("§4.8", format!("{op}: wrong arity"))
                    } else {
                        Ok(())
                    }
                };
                let rd = |n: &str| -> Result<Type> {
                    types
                        .get(n)
                        .cloned()
                        .ok_or_else(|| Error(format!("§3.3: undefined classical operand {n}")))
                };
                let same = |x: &str, y: &str| -> Result<Type> {
                    let t = rd(x)?;
                    if t != rd(y)? {
                        return err("§3.3", "classical operand types differ");
                    }
                    Ok(t)
                };
                if !i.bodies.is_empty() {
                    return err(
                        "§4.8",
                        "classical instruction cannot have Q structured body",
                    );
                }
                let term = matches!(op, "br" | "ret" | "trap");
                if term != (ordinal + 1 == b.instructions.len()) {
                    return err("§3.4", "classical block requires final br/ret/trap");
                }
                let mut result = None;
                if let Some(t) = op.strip_prefix("const.") {
                    arity(1, 1)?;
                    let t = Type::parse(t)?;
                    if !matches!(t, Type::Int(_)) || !integer(&a[0]) {
                        return err("§4.8", "invalid classical const");
                    }
                    result = Some(t);
                } else if is_binop(op) || is_div(op) {
                    arity(2, 1)?;
                    let t = same(&a[0], &a[1])?;
                    if !matches!(t, Type::Int(_)) {
                        return err("§3.3", "binop requires integers");
                    }
                    result = Some(t);
                } else if let Some(pred) = op.strip_prefix("icmp.") {
                    arity(2, 1)?;
                    if !["eq", "ne", "ult", "ule", "slt", "sle"].contains(&pred) {
                        return err("§4.8", "unknown comparison");
                    }
                    same(&a[0], &a[1])?;
                    result = Some(Type::Int(1));
                } else if let Some((cast, suffix)) = op
                    .split_once('.')
                    .filter(|(c, _)| ["zext", "sext", "trunc", "ptrtoint", "load"].contains(c))
                {
                    arity(1, 1)?;
                    let t = Type::parse(suffix)?;
                    let to = t.width(self.ptr_width)?;
                    let from = rd(&a[0])?;
                    if cast == "load" || cast == "ptrtoint" {
                        if from != Type::Ptr {
                            return err("§3.3", "pointer operand required");
                        }
                        if cast == "load" && to % 8 != 0 {
                            return err("§3.3", "load width must be byte multiple");
                        }
                    } else {
                        let w = from.width(self.ptr_width)?;
                        if if cast == "trunc" { to >= w } else { to <= w } {
                            return err("§3.3", "cast direction mismatch");
                        }
                    }
                    result = Some(t);
                } else {
                    match op {
                        "select" => {
                            arity(3, 1)?;
                            if rd(&a[0])? != Type::Int(1) {
                                return err("§3.3", "select requires i1 condition");
                            }
                            result = Some(same(&a[1], &a[2])?);
                        }
                        "inttoptr" => {
                            arity(1, 1)?;
                            if !matches!(rd(&a[0])?, Type::Int(_)) {
                                return err("§3.3", "inttoptr requires integer");
                            }
                            result = Some(Type::Ptr);
                        }
                        "alloc" => {
                            arity(1, 1)?;
                            if !matches!(rd(&a[0])?, Type::Int(_)) {
                                return err("§3.3", "alloc requires integer length");
                            }
                            result = Some(Type::Ptr);
                        }
                        "free" => {
                            arity(1, 0)?;
                            if rd(&a[0])? != Type::Ptr {
                                return err("§3.3", "free requires pointer");
                            }
                        }
                        _ if op.starts_with("store.") => {
                            arity(2, 0)?;
                            let t = Type::parse(&op[6..])?;
                            if t.width(self.ptr_width)? % 8 != 0
                                || rd(&a[0])? != Type::Ptr
                                || rd(&a[1])? != t
                            {
                                return err("§3.3", "store operand type mismatch");
                            }
                        }
                        "br" => {
                            if !i.lhs.is_empty() || !matches!(a.len(), 1 | 3) {
                                return err("§4.8", "br operand count");
                            }
                            if a.len() == 3 && rd(&a[0])? != Type::Int(1) {
                                return err("§3.3", "br predicate must be i1");
                            }
                            for branch in if a.len() == 1 { &a[..] } else { &a[1..] } {
                                let label = branch
                                    .strip_prefix('^')
                                    .ok_or_else(|| Error("§4.8: br target must be label".into()))?;
                                let (label, args) = label.split_once('(').ok_or_else(|| {
                                    Error("§4.8: br target needs argument list".into())
                                })?;
                                if !labels.iter().any(|l| l.as_str() == label) {
                                    return err("§3.4", "unknown branch label");
                                }
                                let vs = list(&format!("({args}"))?;
                                let block = f
                                    .blocks
                                    .iter()
                                    .find(|b| b.name == label)
                                    .expect("label checked");
                                if vs.len() != block.params.len() {
                                    return err("§3.3", "branch argument count mismatch");
                                }
                                for (v, p) in vs.iter().zip(&block.params) {
                                    if rd(v)? != p.ty {
                                        return err("§3.3", "branch parameter type mismatch");
                                    }
                                }
                            }
                        }
                        "ret" => {
                            if !i.lhs.is_empty() || a.len() != f.params[1].len() {
                                return err("§4.8", "return arity mismatch");
                            }
                            for (v, p) in a.iter().zip(&f.params[1]) {
                                if rd(v)? != p.ty {
                                    return err("§3.3", "return type mismatch");
                                }
                            }
                        }
                        "trap" => arity(0, 0)?,
                        "call" | "uncall" => {
                            if a.is_empty() {
                                return err("§4.8", "missing callee");
                            }
                            let callee = self
                                .declaration(a[0].strip_prefix('@').ok_or_else(|| {
                                    Error("§4.8: call requires @symbol".into())
                                })?)?;
                            if !matches!(callee.kind.as_str(), "cc" | "r")
                                || op == "uncall" && callee.kind != "r"
                            {
                                return err("§4.8", "classical call tier mismatch");
                            }
                            let vs = if op == "uncall" {
                                arity(3, 0)?;
                                list(&a[1])?
                            } else if a.len() == 2 && a[1].starts_with('(') {
                                list(&a[1])?
                            } else {
                                a[1..].to_vec()
                            };
                            if vs.len() != callee.params[0].len() {
                                return err("§3.3", "call argument count");
                            }
                            for (v, p) in vs.iter().zip(&callee.params[0]) {
                                if rd(v)? != p.ty {
                                    return err("§3.3", "call argument type");
                                }
                            }
                            if op == "call" {
                                if i.lhs.len() != callee.params[1].len() {
                                    return err("§3.3", "call result count");
                                }
                                for (n, p) in i.lhs.iter().zip(&callee.params[1]) {
                                    if types.insert(n.clone(), p.ty.clone()).is_some() {
                                        return err("§3.3", "SSA name defined twice");
                                    }
                                }
                            } else {
                                let rs = list(&a[2])?;
                                if rs.len() != callee.params[1].len() {
                                    return err("§3.3", "uncall result count");
                                }
                                for (v, p) in rs.iter().zip(&callee.params[1]) {
                                    if rd(v)? != p.ty {
                                        return err("§3.3", "uncall result type");
                                    }
                                }
                            }
                        }
                        "effect" => {
                            if f.kind != "r" {
                                return err("§4.8", "effect is R only");
                            }
                            if !i.lhs.is_empty() || a.is_empty() {
                                return err("§4.8", "effect schema");
                            }
                            for n in &a[1..] {
                                rd(n)?;
                            }
                        }
                        "hostcall" => {
                            arity(3, 1)?;
                            if f.kind != "cc"
                                || rd(&a[1])? != Type::Ptr
                                || !matches!(rd(&a[2])?, Type::Int(_))
                            {
                                return err("§4.8", "hostcall tier/type mismatch");
                            }
                            let service = self
                                .section("devices")
                                .and_then(|d| d.get("services").ok())
                                .and_then(|s| s.object().ok());
                            if service.is_none_or(|s| !s.contains_key(&a[0])) {
                                return err("§10", "hostcall service undeclared");
                            }
                            result = Some(Type::Int(self.ptr_width));
                        }
                        "qreg.new" => {
                            arity(2, 1)?;
                            if f.kind != "cc" {
                                return err("§4.8", "qreg instructions are CC only");
                            }
                            let n = a[1]
                                .parse::<u64>()
                                .map_err(|_| Error("§3.3: qreg literal width".into()))?;
                            result = Some(Type::Qreg(n));
                        }
                        "qreg.free" => {
                            arity(1, 0)?;
                            if f.kind != "cc" || !matches!(rd(&a[0])?, Type::Qreg(_)) {
                                return err("§3.3", "qreg.free operand/tier");
                            }
                        }
                        "qreg.slice" => {
                            arity(3, 1)?;
                            let Type::Qreg(n) = rd(&a[0])? else {
                                return err("§3.3", "slice needs qreg");
                            };
                            let lo = a[1]
                                .parse::<u64>()
                                .map_err(|_| Error("§3.3: slice offset".into()))?;
                            let len = a[2]
                                .parse::<u64>()
                                .map_err(|_| Error("§3.3: slice length".into()))?;
                            if f.kind != "cc" || lo.checked_add(len).is_none_or(|end| end > n) {
                                return err("§3.3", "invalid slice");
                            }
                            result = Some(Type::Qreg(len));
                        }
                        "qreg.concat" => {
                            arity(2, 1)?;
                            let (Type::Qreg(n), Type::Qreg(m)) = (rd(&a[0])?, rd(&a[1])?) else {
                                return err("§3.3", "concat needs qregs");
                            };
                            if f.kind != "cc" || a[0] == a[1] {
                                return err("§3.3", "concat tier/alias");
                            }
                            result = Some(Type::Qreg(
                                n.checked_add(m)
                                    .ok_or_else(|| Error("§3.3: qreg size overflow".into()))?,
                            ));
                        }
                        "measure" => {
                            arity(1, 1)?;
                            let Type::Qreg(n) = rd(&a[0])? else {
                                return err("§3.3", "measure needs qreg");
                            };
                            if f.kind != "cc" || n == 0 || n > 128 {
                                return err("§3.3", "measure tier/width");
                            }
                            result = Some(Type::Int(n as u16));
                        }
                        "oracle_call" | "action_call" | "adj" | "ctl" => {
                            let call = normalize_call(i)?;
                            self.validate_region_call(f, &call.instruction, types)?;
                        }
                        _ => return err("§4.8", format!("unknown classical opcode {op}")),
                    }
                }
                if let Some(ty) = result {
                    if types.insert(i.lhs[0].clone(), ty).is_some() {
                        return err("§3.3", "SSA definition reused");
                    }
                }
            }
        }
        self.validate_handle_views(f, types)
    }
    pub(crate) fn validate_call_graph(&self) -> Result<()> {
        fn calls<'a>(i: &'a Instruction, output: &mut Vec<&'a str>) {
            if let Ok(c) = normalize_call(i) {
                if matches!(c.instruction.op.as_str(), "action_call" | "oracle_call") {
                    if let Some(n) = i.operands.iter().find_map(|s| s.strip_prefix('@')) {
                        output.push(n);
                    }
                }
            }
            for body in &i.bodies {
                for child in body {
                    calls(child, output);
                }
            }
        }
        fn visit(
            obj: &Object,
            n: &str,
            active: &mut BTreeSet<String>,
            done: &mut BTreeSet<String>,
        ) -> Result<()> {
            if done.contains(n) {
                return Ok(());
            }
            if !active.insert(n.into()) {
                return err("§5.1", "recursive region call graph");
            }
            let f = &obj.functions[n];
            let mut children = Vec::new();
            for i in f.instructions() {
                calls(i, &mut children);
            }
            for child in children {
                if obj.functions.contains_key(child) {
                    visit(obj, child, active, done)?;
                }
            }
            active.remove(n);
            done.insert(n.into());
            Ok(())
        }
        let mut done = BTreeSet::new();
        for f in self
            .functions
            .values()
            .filter(|f| matches!(f.kind.as_str(), "action" | "perm_action" | "oracle"))
        {
            visit(self, &f.name, &mut BTreeSet::new(), &mut done)?;
        }
        Ok(())
    }
    pub(crate) fn validate_metadata(&self) -> Result<()> {
        if let Some(d) = self.section("devices") {
            d.fields(&["models", "services"], &[])?;
            for group in ["models", "services"] {
                for (n, v) in d.get(group)?.object()? {
                    v.fields(&["version"], &[])?;
                    if group == "models"
                        && (!["console", "clock", "entropy", "block"].contains(&n.as_str())
                            || v.get("version")?.string()? != "0.8")
                    {
                        return err("§7.3", "unsupported device model/version");
                    }
                }
            }
        }
        if let Some(c) = self.section("coverage") {
            c.fields(&["entries"], &[])?;
            for e in c.get("entries")?.array()? {
                e.fields(
                    &["point", "source", "classification", "reason", "count"],
                    &["fault_code", "shim_hash"],
                )?;
                if !["lowered", "trapped", "shimmed"].contains(&e.get("classification")?.string()?)
                {
                    return err("§13", "unknown coverage classification");
                }
                e.get("count")?.uint()?;
            }
        }
        if let Some(s) = self.section("schedule") {
            s.fields(&["bindings", "entries"], &[])?;
            let b = s.get("bindings")?;
            b.fields(
                &[
                    "closure_hash",
                    "target_hash",
                    "region",
                    "variant",
                    "inherited_controls",
                    "budget",
                    "params_hash",
                    "epsilon",
                    "scheduler",
                ],
                &["expansion"],
            )?;
            b.get("scheduler")?.fields(&["name", "version"], &[])?;
            if let Some(e) = b.object()?.get("expansion") {
                e.fields(&["name", "version", "hash"], &[])?;
            }
            if b.get("budget")?.array()?.len() != 4 {
                return err("§11", "schedule budget needs four values");
            }
            for e in s.get("entries")?.array()? {
                e.fields(
                    &["path", "step", "phase", "generated", "kind"],
                    &["cleanup", "gate", "alloc", "start"],
                )?;
                let k = e.get("kind")?.string()?;
                match k {
                    "cleanup" => {
                        let c = e.get(k)?;
                        c.fields(&["realisation"], &[])?;
                        if !["reverse", "recompute"].contains(&c.get("realisation")?.string()?) {
                            return err("§6.4", "unsupported cleanup realisation");
                        }
                    }
                    "gate" => e.get(k)?.fields(&["realisation", "epsilon_share"], &[])?,
                    "alloc" => {
                        e.get(k)?.fields(&["class"], &[])?;
                        if e.get(k)?.get("class")?.string()? == "any" {
                            return err("§11", "schedule requires concrete class");
                        }
                    }
                    "start" => e.get(k)?.fields(&["time"], &[])?,
                    _ => return err("§11", "unknown schedule entry kind"),
                };
                for p in e.get("path")?.array()? {
                    p.fields(&["symbol", "point", "iteration"], &[])?;
                }
            }
        }
        if let Some(c) = self.section("certificate") {
            c.fields(
                &["versions", "bindings", "producer", "regions", "composition"],
                &[],
            )?;
            c.get("bindings")?.fields(
                &[
                    "object_hash",
                    "interface_hash",
                    "closure_hash",
                    "reference_program_hash",
                    "dialect_mapping_version",
                    "target_hash",
                ],
                &["schedule_hash"],
            )?;
            c.get("producer")?
                .fields(&["name", "version", "materialisation"], &[])?;
            c.get("producer")?
                .get("materialisation")?
                .fields(&["llvm_version", "pipeline", "normaliser_version"], &[])?;
            c.get("composition")?
                .fields(&["multiplicities", "epsilon_total", "method"], &[])?;
            for r in c.get("regions")?.object()?.values() {
                r.fields(
                    &[
                        "kind",
                        "signature",
                        "bounds",
                        "frame",
                        "resources",
                        "gates_used",
                        "claims",
                        "verification",
                        "cleanup",
                        "error",
                        "definedness_assumptions",
                    ],
                    &[],
                )?;
                r.get("verification")?.fields(
                    &[
                        "oracle",
                        "borrow_frames",
                        "inverse_pairs",
                        "unitary",
                        "channel",
                        "fault_rate",
                    ],
                    &[],
                )?;
            }
        }
        Ok(())
    }
}

#[derive(Clone)]
struct Creation {
    kind: String,
    sources: Vec<String>,
    versions: Vec<(String, Vec<String>)>,
    controls: Vec<String>,
}
struct Discipline {
    types: BTreeMap<String, Type>,
    inputs: BTreeSet<String>,
    predicates: Vec<String>,
    created: BTreeMap<String, Creation>,
    versions: BTreeMap<String, Vec<String>>,
    closed: BTreeSet<String>,
    bounds: Vec<u64>,
}
impl Discipline {
    fn new(f: &Function, types: BTreeMap<String, Type>) -> Self {
        Self {
            types,
            inputs: f.params[1]
                .iter()
                .chain(
                    f.params[2]
                        .iter()
                        .filter(|p| p.role.as_deref() == Some("in")),
                )
                .map(|p| p.name.clone())
                .collect(),
            predicates: Vec::new(),
            created: BTreeMap::new(),
            versions: BTreeMap::new(),
            closed: BTreeSet::new(),
            bounds: Vec::new(),
        }
    }
    fn wires(&self, n: &str) -> Result<Vec<String>> {
        let (base, index) = if let Some((base, index)) = n.split_once('[') {
            let index = index
                .strip_suffix(']')
                .and_then(|s| s.parse::<u16>().ok())
                .ok_or_else(|| Error("§3.3: invalid indexed wire".into()))?;
            (base, Some(index))
        } else {
            (n, None)
        };
        let w = match self.types.get(base) {
            Some(Type::Wire(n)) => *n,
            _ => return err("§3.3", format!("unknown/live wire {n}")),
        };
        if let Some(i) = index {
            if i >= w {
                return err("§3.3", "wire index out of range");
            }
            Ok(vec![format!("{base}[{i}]")])
        } else {
            Ok((0..w).map(|i| format!("{base}[{i}]")).collect())
        }
    }
    fn disjoint(&self, operands: &[&str]) -> Result<()> {
        let mut seen = BTreeSet::new();
        for o in operands {
            for w in self.wires(o)? {
                if !seen.insert(w) {
                    return err("§3.3", "overlapping wire operands");
                }
            }
        }
        Ok(())
    }
    fn snapshot(&self, wires: &[String]) -> Vec<(String, Vec<String>)> {
        wires
            .iter()
            .map(|w| (w.clone(), self.versions.get(w).cloned().unwrap_or_default()))
            .collect()
    }
    fn produce(&mut self, n: &str, ty: Type, c: Creation) -> Result<()> {
        if self.types.contains_key(n) {
            return err("§3.3", "linear name produced twice");
        }
        self.types.insert(n.into(), ty);
        self.created.insert(n.into(), c);
        Ok(())
    }
    fn consume(&mut self, n: &str) -> Result<()> {
        self.wires(n)?;
        self.types.remove(n);
        self.created.remove(n);
        Ok(())
    }
    fn check_target(&self, n: &str, diagonal: bool) -> Result<()> {
        let wires = self.wires(n)?;
        for p in &self.predicates {
            if self.wires(p)?.iter().any(|w| wires.contains(w)) {
                return err("§3.3", "effective control aliases target");
            }
        }
        let base = n.split('[').next().expect("name");
        if !diagonal && self.inputs.contains(base) {
            return err("§5.1", "instruction changes an in wire");
        }
        Ok(())
    }
    fn change(&mut self, n: &str, version: String, other: bool) -> Result<()> {
        self.check_target(n, false)?;
        for w in self.wires(n)? {
            if other {
                self.closed.insert(w.clone());
            }
            let log = self.versions.entry(w).or_default();
            if log
                .last()
                .is_some_and(|prior| operation_inverse(prior).as_deref() == Some(version.as_str()))
            {
                log.pop();
            } else {
                log.push(version.clone());
            }
        }
        Ok(())
    }
    fn is_other(&self, n: &str) -> Result<bool> {
        Ok(self.wires(n)?.iter().any(|w| {
            self.versions.get(w).is_some_and(|log| {
                log.iter().any(|v| {
                    ["h:", "rx:", "ry:", "call_other_"]
                        .iter()
                        .any(|p| v.starts_with(p))
                })
            })
        }))
    }
    fn record_change(&mut self, n: &str, version: String) -> Result<()> {
        for wire in self.wires(n)? {
            let log = self.versions.entry(wire).or_default();
            if log
                .last()
                .is_some_and(|p| operation_inverse(p).as_deref() == Some(&version))
            {
                log.pop();
            } else {
                log.push(version.clone());
            }
        }
        Ok(())
    }
}
fn operation_inverse(version: &str) -> Option<String> {
    let (op, rest) = version.split_once(':')?;
    let inverse = match op {
        "s" => "sdg",
        "sdg" => "s",
        "t" => "tdg",
        "tdg" => "t",
        "call_other_fwd" => "call_other_adj",
        "call_other_adj" => "call_other_fwd",
        "call_perm_fwd" => "call_perm_adj",
        "call_perm_adj" => "call_perm_fwd",
        "x" | "cx" | "ccx" | "mcx" | "swap" | "h" | "qxor" | "qexch" | "qexchm" => op,
        "rx" | "ry" | "rz" => {
            let (angle, tail) = rest.split_once(' ')?;
            let bits = u64::from_str_radix(angle.strip_prefix('#')?, 16).ok()?;
            return Some(format!("{op}:#{:016x} {tail}", bits ^ (1u64 << 63)));
        }
        _ => return None,
    };
    Some(format!("{inverse}:{rest}"))
}
pub(crate) fn gate(op: &str) -> bool {
    [
        "x", "h", "s", "sdg", "t", "tdg", "cx", "ccx", "mcx", "swap", "cz", "rx", "ry", "rz",
    ]
    .contains(&op)
}
pub(crate) fn gate_operands(i: &Instruction) -> Result<(Vec<String>, Vec<String>, bool, bool)> {
    let a = &i.operands;
    let op = i.op.as_str();
    let n = match op {
        "x" | "h" | "s" | "sdg" | "t" | "tdg" => 1,
        "ccx" => 3,
        _ => 2,
    };
    if !i.lhs.is_empty() || a.len() != n {
        return err("§4.8", "gate arity mismatch");
    }
    let diagonal = matches!(op, "s" | "sdg" | "t" | "tdg" | "cz" | "rz");
    let other = matches!(op, "h" | "rx" | "ry");
    let (controls, targets) = match op {
        "cx" => (vec![a[0].clone()], vec![a[1].clone()]),
        "ccx" => (a[..2].to_vec(), vec![a[2].clone()]),
        "mcx" => (list(&a[0])?, vec![a[1].clone()]),
        "swap" | "cz" => (Vec::new(), a.clone()),
        "rx" | "ry" | "rz" => {
            if let Ok(x) = a[0].parse::<f64>() {
                if !x.is_finite() || !a[0].contains(['.', 'e', 'E']) {
                    return err("§16.1", "angle must be finite FLOAT");
                }
            } else if !name(&a[0]) {
                return err("§4.4", "angle must be literal or classical argument");
            }
            (Vec::new(), vec![a[1].clone()])
        }
        _ => (Vec::new(), vec![a[0].clone()]),
    };
    Ok((controls, targets, diagonal, other))
}
pub(crate) struct NormalCall {
    pub instruction: Instruction,
    pub control: Option<String>,
    pub adjoint: bool,
}
pub(crate) fn normalize_call(i: &Instruction) -> Result<NormalCall> {
    let mut out = i.clone();
    let mut control = None;
    let mut adjoint = false;
    loop {
        match out.op.as_str() {
            "adj" => {
                adjoint = !adjoint;
                if out.operands.is_empty() {
                    return err("§4.7", "missing adjoint call");
                }
                out.op = out.operands.remove(0);
            }
            "ctl" => {
                if control.is_some() || out.operands.len() < 2 {
                    return err("§4.7", "invalid controlled call");
                }
                control = Some(out.operands.remove(0));
                out.op = out.operands.remove(0);
            }
            _ => break,
        }
    }
    if !matches!(out.op.as_str(), "oracle_call" | "action_call") {
        return err("§4.7", "adj/ctl requires a region call");
    }
    Ok(NormalCall {
        instruction: out,
        control,
        adjoint,
    })
}
````

## `tests/borrow.rs` (51 lines)

````rust
mod support;
use bennett_isa_ref::{validate_translation_lemma,Instruction,Object,QuantumBindings,QuantumState};
use std::collections::BTreeSet;
use support::object;
fn gate(op:&str,operands:&[&str])->Instruction{Instruction{lhs:Vec::new(),op:op.into(),operands:operands.iter().map(|s|(*s).into()).collect(),bodies:Vec::new(),line:1}}
#[test]
fn translation_lemma_checks_all_four_required_negative_patterns(){
    let b=BTreeSet::from(["b".into(),"b2".into()]);let x=BTreeSet::from(["x".into()]);let v=[gate("cx",&["x","b"])];let w=[gate("cx",&["b","t"])];validate_translation_lemma(&v,&w,&x,&b).unwrap();
    // A V;W;V^-1 prefix lacks the required final W and is checked as a full frame below.
    assert!(validate_translation_lemma(&[gate("cx",&["b2","b"])],&w,&BTreeSet::from(["b2".into()]),&b).is_err());
    assert!(validate_translation_lemma(&[gate("cx",&["b","x"])],&w,&BTreeSet::from(["b".into()]),&b).is_err());
    assert!(validate_translation_lemma(&v,&[gate("swap",&["y","z"]),gate("cx",&["b","y"])],&x,&b).is_err());
    assert!(validate_translation_lemma(&v,&[gate("cx",&["b","y"]),gate("cx",&["y","z"])],&x,&b).is_err());
}
fn borrowed(body:&str)->String {
    let signature=r#"{"abi":"0.8","args":[],"bounds":[],"in":[1],"kind":"perm_action","mem":[],"mut":[1,1,1],"tier":"q"}"#;
    object(&[("a",signature,&format!("perm_action @a (t:wire mut, y:wire mut, z:wire mut) (x:wire in) () () ()\n^entry():\nb = qborrow any 1\n{body}\nqreturn b"))],"{}","")
}
#[test]
fn borrow_frame_exhaustion_rejects_hidden_dependence_on_borrowed_bits(){
    let raw=borrowed("cx b y\ncx y z\ncx b y");let error=Object::parse(&raw).expect_err("borrowed-dependent output accepted");assert!(error.to_string().contains("§5.6"));
}
#[test]
fn translation_pattern_returns_an_entangled_borrowed_system(){
    let o=Object::parse(&borrowed("cx x b\ncx b t\ncx x b\ncx b t")).unwrap();
    let mut q=QuantumState::new();let t=q.allocate(1).unwrap();let y=q.allocate(1).unwrap();let z=q.allocate(1).unwrap();let x=q.allocate(1).unwrap();let b=q.allocate(1).unwrap();let reference=q.allocate(1).unwrap();
    q.gate("h",&[b[0]],None,&[]).unwrap();q.gate("cx",&[b[0],reference[0]],None,&[]).unwrap();q.gate("x",&x,None,&[]).unwrap();
    let mut bindings=QuantumBindings::default();for(n,w)in[("t",t.clone()),("y",y),("z",z),("x",x)]{bindings.bundles.insert(n.into(),w);}bindings.borrowed.push(b.clone());
    o.execute_action("a",&mut q,&bindings,false,&[]).unwrap();
    // The output is t=1 tensor the original Bell pair on borrowed b/reference.
    q.gate("x",&t,None,&[]).unwrap();q.gate("cx",&[b[0],reference[0]],None,&[]).unwrap();q.gate("h",&b,None,&[]).unwrap();q.release(&b).unwrap();q.release(&reference).unwrap();
}

#[test]
fn classical_region_calls_supply_only_designated_idle_registers(){
    use bennett_isa_ref::{ClassicalMachine,ClassicalValue,QuantumRegisters};
    let action=support::rehash(&borrowed("cx x b\ncx b t\ncx x b\ncx b t"));let sig=r#"{"abi":"0.8","kind":"cc","params":["qreg[1]","qreg[1]","qreg[1]","qreg[1]"],"results":[],"tier":"cc"}"#;
    let imports=format!("{{\"a\":{{\"signature\":{}}}}}",action.symbols().unwrap()["0"].get("signature").unwrap().canonical());
    let caller=support::rehash(&object(&[("invoke",sig,"fn cc @invoke (t:qreg[1], y:qreg[1], z:qreg[1], x:qreg[1]) () () () ()\n^entry():\naction_call @a (t, y, z) (x) () ()\nret")],&imports,""));let program=Object::link(&[caller,action]).unwrap();
    let mut registers=QuantumRegisters::new();let mut ids=Vec::new();for _ in 0..5{ids.push(registers.allocate(1).unwrap());}registers.prepare(ids[3],&[true]).unwrap();registers.prepare(ids[4],&[true]).unwrap();let args=ids[..4].iter().map(|id|ClassicalValue::Qreg(*id)).collect::<Vec<_>>();
    let mut m=ClassicalMachine::with_quantum_registers(&program,"invoke",&args,&[],registers).unwrap();m.designate_idle_registers(&[ids[4]]).unwrap();let before=m.snapshot();assert_eq!(m.run(100).unwrap().fault,None);let r=m.quantum_registers();for id in [ids[0],ids[4]]{assert_eq!(r.quantum_state().read_basis(r.bundle(id).unwrap()).unwrap(),1);}m.reverse().unwrap();assert_eq!(m.snapshot(),before);
}

#[test]
fn lifted_permutation_actions_can_borrow_workspace_and_reverse(){
    use bennett_isa_ref::{Budget,OracleInput,OracleMachine};
    let action=support::rehash(&borrowed("cx x b\ncx b t\ncx x b\ncx b t"));let signature=r#"{"abi":"0.8","args":[],"fault":4,"in":[1],"kind":"oracle","mem":[],"tgt":1,"tier":"q"}"#;
    let imports=format!("{{\"a\":{{\"signature\":{}}}}}",action.symbols().unwrap()["0"].get("signature").unwrap().canonical());
    let caller=support::rehash(&object(&[("lifted",signature,"oracle @lifted (input:wire in) (target:wire) (fault:wire[4]) () ()\nregs { t:reg[1], y:reg[1], z:reg[1], x:reg[1] }\n^entry():\nx = lift.mov input\nt = lift.const.i1 0\ny = lift.const.i1 0\nz = lift.const.i1 0\nlift.perm_call @a (t, y, z) (x) () ()\nlift.retval t")],&imports,""));let o=Object::link(&[caller,action]).unwrap();
    for x in 0..2{for steps in 0..8{let input=OracleInput::bits(&[x]);let budget=Budget::steps(steps);let result=o.run_oracle("lifted",&input,budget).unwrap();assert_eq!((result.payload,result.code),if steps>=6{(x,0)}else{(0,1)});let mut m=OracleMachine::new(&o,"lifted",&input,budget).unwrap();let before=m.snapshot();for _ in 0..steps{m.forward_step().unwrap();}assert_eq!(m.outcome(),result);for _ in 0..steps{m.inverse_step().unwrap();}assert_eq!(m.snapshot(),before);}}
}
````

## `tests/classical.rs` (84 lines)

````rust
use bennett_isa_ref::{ClassicalMachine, ClassicalValue, Object};

#[test]
fn dynamic_instances_loop_and_whole_run_reversal() {
    let o = Object::parse(include_str!("fixtures/classical.bisa")).unwrap();
    for n in 0..=8 {
        let mut m =
            ClassicalMachine::new(&o, "sum", &[ClassicalValue::int(8, n).unwrap()], &[]).unwrap();
        let before = m.snapshot();
        let r = m.run(1000).unwrap();
        assert_eq!(r.fault, None);
        assert_eq!(
            r.values,
            vec![ClassicalValue::int(8, n * (n + 1) / 2).unwrap()]
        );
        m.reverse().unwrap();
        assert_eq!(m.snapshot(), before);
    }
}
#[test]
fn nested_uncall_and_effects_are_reversed_exactly_once() {
    let o = Object::parse(include_str!("fixtures/classical.bisa")).unwrap();
    for name in ["nested", "effects"] {
        let mut m = ClassicalMachine::new(&o, name, &[], &[11, 22, 33]).unwrap();
        let before = m.snapshot();
        let result = m.run(1000).unwrap();
        assert_eq!(result.fault, None);
        assert_eq!(result.values, vec![ClassicalValue::int(64, 0).unwrap()]);
        if name == "nested" {
            assert_eq!(m.clock(), 0);
            assert_eq!(m.effect_tape_len(), 0);
        } else {
            assert_eq!(m.clock(), 1);
            assert_eq!(m.console(), &[11, 22, 33]);
            assert_eq!(m.effect_tape_len(), 5);
        }
        m.reverse().unwrap();
        assert_eq!(m.snapshot(), before);
    }
}
#[test]
fn faults_are_atomic_terminal_and_reversible() {
    let o = Object::parse(include_str!("fixtures/classical.bisa")).unwrap();
    for (name, code) in [
        ("impure", 4),
        ("entropy_short", 10),
        ("unknown_effect", 8),
        ("memfault", 7),
        ("divzero", 5),
    ] {
        let mut m = ClassicalMachine::new(&o, name, &[], &[]).unwrap();
        let before = m.snapshot();
        let result = m.run(1000).unwrap();
        assert_eq!(result.fault, Some(code), "{name}");
        assert!(result.values.is_empty());
        if name == "entropy_short" {
            assert_eq!(m.effect_tape_len(), 0);
        }
        m.reverse().unwrap();
        assert_eq!(m.snapshot(), before, "{name}");
    }
}

#[test]
fn host_request_reply_records_full_length_and_reverses_bytes() {
    let o = Object::parse(include_str!("fixtures/classical.bisa")).unwrap();
    let mut m = ClassicalMachine::new(&o, "host", &[], &[]).unwrap();
    let before = m.snapshot();
    let waiting = m.run(100).unwrap();
    let request = waiting.request.unwrap();
    assert_eq!(request.service, "org.bennett.test");
    assert_eq!(request.payload, [165, 0, 0]);
    m.reply(&[17, 34, 51, 68, 85]).unwrap();
    assert_eq!(m.memory_bytes(request.address, 3).unwrap(), [17, 34, 51]);
    let result = m.run(100).unwrap();
    assert_eq!(result.values, vec![ClassicalValue::int(16, 5).unwrap()]);
    m.reverse().unwrap();
    assert_eq!(m.snapshot(), before);
    assert!(m.reply(&[]).is_err());
    let mut invalid = ClassicalMachine::new(&o, "host_invalid", &[], &[]).unwrap();
    let result = invalid.run(100).unwrap();
    assert_eq!(result.fault, Some(7));
    assert!(result.request.is_none());
}
````

## `tests/cli.rs` (73 lines)

````rust
use std::process::Command;
fn fixture(name: &str) -> String {
    format!("{}/tests/fixtures/{name}.bisa", env!("CARGO_MANIFEST_DIR"))
}
fn cli(args: &[&str]) -> std::process::Output {
    Command::new(env!("CARGO_BIN_EXE_bennett-isa-ref"))
        .args(args)
        .output()
        .unwrap()
}
#[test]
fn check_and_run_print_machine_readable_json() {
    let output = cli(&["check", &fixture("inc8")]);
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    let value =
        bennett_isa_ref::json::Json::parse(std::str::from_utf8(&output.stdout).unwrap()).unwrap();
    assert_eq!(value.get("status").unwrap().string().unwrap(), "ok");
    for (budget, payload, code, steps) in [("3", 0, 0, 3), ("2", 0, 1, 2), ("0", 0, 1, 0)] {
        let output = cli(&[
            "run-oracle",
            &fixture("inc8"),
            "inc8",
            "--input",
            "255",
            "--budget",
            budget,
        ]);
        assert!(
            output.status.success(),
            "{}",
            String::from_utf8_lossy(&output.stderr)
        );
        let value =
            bennett_isa_ref::json::Json::parse(std::str::from_utf8(&output.stdout).unwrap())
                .unwrap();
        for (k, v) in [("payload", payload), ("code", code), ("steps", steps)] {
            assert_eq!(value.get(k).unwrap().uint().unwrap(), v);
        }
    }
}
#[test]
fn exhaustive_step_check_and_diagnostics() {
    let output = cli(&[
        "step-check",
        &fixture("inc8"),
        "inc8",
        "--exhaustive",
        "--budget",
        "4",
    ]);
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    let value =
        bennett_isa_ref::json::Json::parse(std::str::from_utf8(&output.stdout).unwrap()).unwrap();
    assert_eq!(value.get("cases").unwrap().uint().unwrap(), 256);
    for args in [
        vec!["nonsense"],
        vec!["check", "/no/such/object"],
        vec!["run-oracle"],
        vec!["run-oracle", &fixture("inc8"), "inc8", "--input", "256"],
    ] {
        let output = cli(&args);
        assert!(!output.status.success());
        assert!(!output.stderr.is_empty());
    }
}
````

## `tests/discipline.rs` (96 lines)

````rust
mod support;
use bennett_isa_ref::Object;
use support::object;
const ACTION: &str =
    r#"{"abi":"0.8","args":[],"bounds":[],"in":[1],"kind":"action","mem":[],"mut":[1],"tier":"q"}"#;
const ORACLE: &str = r#"{"abi":"0.8","args":["token"],"fault":4,"in":[8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}"#;
const INC: &str =
    r#"{"abi":"0.8","args":[],"fault":4,"in":[8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}"#;
fn action(body: &str) -> String {
    object(
        &[(
            "a",
            ACTION,
            &format!("action @a (t:wire mut) (p:wire in) () () ()\n^entry():\n{body}"),
        )],
        "{}",
        "",
    )
}
fn reject(text: &str, rule: &str) {
    let error = match Object::parse(text){Err(error)=>error,Ok(_)=>panic!("ill-formed cleanup accepted")};
    assert!(error.to_string().contains(rule), "{error}");
}
#[test]
fn other_scratch_requires_the_exact_adjoint_but_accepts_h_h() {
    Object::parse(&action("d = qalloc any 1\nh d\nh d\nqfree d")).unwrap();
    reject(&action("d = qalloc any 1\nh d\ns d\nh d\nqfree d"), "§6.2");
    Object::parse(&action("d = qalloc any 1\nh d\ns d\nsdg d\nh d\nqfree d")).unwrap();
    Object::parse(&action("d = qalloc any 1\nrx 0.7 d\nrx -0.7 d\nqfree d")).unwrap();
}
#[test]
fn inherited_control_cannot_be_a_callee_diagonal_target() {
    let parent="action @parent (t:wire mut) (p:wire in) () () ()\n^entry():\nqpred p\naction_call @child (t) (p) () ()\nqunpred p";
    let child = "action @child (t:wire mut) (p:wire in) () () ()\n^entry():\ns p\nx t";
    reject(
        &object(
            &[("parent", ACTION, parent), ("child", ACTION, child)],
            "{}",
            "",
        ),
        "§3.3",
    );
    let legal = child.replace("s p\nx t", "cx p t");
    Object::parse(&object(
        &[("parent", ACTION, parent), ("child", ACTION, &legal)],
        "{}",
        "",
    ))
    .unwrap();
}
#[test]
fn matched_oracle_cleanup_rejects_input_writes_and_unmatched_invocations() {
    let inc="oracle @inc (x:wire[8] in) (t:wire[8]) (f:wire[4]) () ()\nregs { r:reg[8] }\n^entry():\nr = lift.mov x\nlift.retval r";
    let build = |middle: &str| {
        object(&[("inc",INC,inc),("outer",ORACLE,&format!("oracle @outer (x:wire[8] in) (t:wire[8]) (f:wire[4]) () (tk:token)\nregs {{ input:reg[8], r:reg[8], fr:reg[4] }}\n^entry():\ninput = lift.mov x\nlift.oracle_call @inc tk (input) r fr () ()\n{middle}lift.oracle_uncall @inc tk (input) r fr () ()\nlift.retval r"))],"{}","")
    };
    Object::parse(&build("")).unwrap();
    reject(&build("input = lift.mov x\n"), "§5.5");
    reject(
        &build("").replace("lift.oracle_call @inc tk (input) r fr () ()\n", ""),
        "§5.5",
    );
    reject(
        &build("lift.oracle_uncall @inc tk (input) r fr () ()\n"),
        "§5.5",
    );
}

#[test]
fn release_cannot_consume_its_effective_control() {
    reject(
        &action("d = qalloc any 1\nqpred d\nqfree d\nqunpred d"),
        "§3.3",
    );
    reject(
        &action("d = qcopy p\nqpred d\nquncopy p d\nqunpred d"),
        "§3.3",
    );
}

#[test]
fn angles_and_function_interfaces_require_classical_argument_types(){
    reject(&action("rx p t"),"§3.3");
    let signature=r#"{"abi":"0.8","kind":"cc","params":["wire[8]"],"results":[],"tier":"cc"}"#;
    reject(&object(&[("bad",signature,"fn cc @bad (x:wire[8]) () () () ()\n^entry():\nret")],"{}",""),"§3.3");
}
#[test]
fn lproc_fault_literals_use_the_enclosing_oracles_fault_width(){
    use bennett_isa_ref::{Budget,OracleInput};
    let oracle=r#"{"abi":"0.8","args":[],"fault":5,"in":[],"kind":"oracle","mem":[],"tgt":1,"tier":"q"}"#;
    let proc=r#"{"abi":"0.8","kind":"lproc","params":[],"result":1,"tier":"q"}"#;
    let layout="\nsection layout\n{\"A_tab\":0,\"H\":8,\"S_cells\":4,\"globals\":{},\"heap_base\":16,\"heap_limit_max\":0,\"interface_regions\":{},\"null_size\":1,\"ptr_width\":32}\n";
    let text=object(&[("main",oracle,"oracle @main () (t:wire) (f:wire[5]) () ()\nregs { r:reg[1] }\n^entry():\nr = lift.call @p ()\nlift.retval r"),("p",proc,"lproc @p () (r:reg[1]) () () ()\n^entry():\nfault 31")],"{}",layout);
    let o=Object::parse(&text).unwrap();let r=o.run_oracle("main",&OracleInput::bits(&[]),Budget{steps:2,heap:0,stack:16,depth:8}).unwrap();assert_eq!((r.payload,r.code),(0,31));
    reject(&text.replace("fault 31","fault 32"),"§3.3");
}
````

## `tests/fixtures/actions.bisa` (39 lines)

````
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=32

section symbols
{"0":{"interface_hash":"7b3212f6647103050fa24c34e767afd19fbe3009134d6f5c7280a400ff9ef398","kind":"perm_action","name":"flip","signature":{"abi":"0.8","args":[],"bounds":[],"in":[2],"kind":"perm_action","mem":[],"mut":[2],"tier":"q"}},"1":{"interface_hash":"62c70737b8fcae09329da78eed2ed48aad61dfe0137e2d8d02c1e1ffb9dc5f76","kind":"perm_action","name":"memory","signature":{"abi":"0.8","args":[],"bounds":[],"in":[2],"kind":"perm_action","mem":[],"mut":[2],"tier":"q"}},"2":{"interface_hash":"56ab73b8a0938e882c2a3293d4fb401a07bbbb931485b88948973ba1c3dc1597","kind":"perm_action","name":"loop","signature":{"abi":"0.8","args":[],"bounds":[3],"in":[2],"kind":"perm_action","mem":[],"mut":[2],"tier":"q"}},"3":{"interface_hash":"3b0881575762fa4e1fd5b2a160cd6abfcbfe60f011df3b1968df7e44de11e1d3","kind":"action","name":"bell","signature":{"abi":"0.8","args":[],"bounds":[],"in":[2],"kind":"action","mem":[],"mut":[2],"tier":"q"}},"4":{"interface_hash":"90dbeda2a04d9f5ac10570fa079aaf22540fb1bf8da780415dcd238334996aa4","kind":"data","name":"image","signature":{"abi":"0.8","kind":"data","size":1,"tier":"-"}},"5":{"interface_hash":"2acd73fbb764d1a278bcba54e7a13c99ddd1d159e8f63ea59f3af7338e313f67","kind":"oracle","name":"lifted","signature":{"abi":"0.8","args":[],"fault":4,"in":[2],"kind":"oracle","mem":[],"tgt":2,"tier":"q"}}}

section functions
perm_action @flip (t:wire[2] mut) (p:wire[2] in) () () ()
^entry():
d = qcopy p
qxor d t
quncopy p d
perm_action @memory (t:wire[2] mut) (p:wire[2] in) () () ()
^entry():
qregion r 2 2 @image
d = qload r p
qunload r p d
qstore r p t
qstore r p t
qexchm r p t
qexchm r p t
perm_action @loop (t:wire[2] mut) (p:wire[2] in) () () ()
regs {  } bounds {3}
^entry():
qloop 3 {
x t[0]
}
action @bell (t:wire[2] mut) (p:wire[2] in) () () ()
^entry():
h t[0]
cx t[0] t[1]
oracle @lifted (x:wire[2] in) (t:wire[2]) (f:wire[4]) () ()
regs { r:reg[2] }
^entry():
r = lift.const.i2 1
lift.perm_call @flip (r) (x) () ()
lift.retval r

section data
image 00
````

## `tests/fixtures/actions.comments` (2 lines)

````
Hand derivations: flip computes d=p, XORs d into t and uncomputes d, so t XOR p with no garbage. memory has an all-zero 4x2-bit local image; load/unload cancels, two stores cancel and two memory exchanges cancel, so it is identity. loop flips t[0] three times, hence once. bell maps |00> to (|00>+|11>)/sqrt(2). Each adjoint composed after its action is identity including phase.
lifted starts r=1, then flip(r,x) computes r XOR x, so the oracle payload is x XOR 1 in three rows.
````

## `tests/fixtures/arithmetic.bisa` (194 lines)

````
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=32

section symbols
{"0":{"interface_hash":"7c80a06412db38f658cf0441a0f64529cbfb8b903814f239cad3ba770f99308a","kind":"oracle","name":"add","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"1":{"interface_hash":"080d1d22642a043ef267f4f6814af1591511d8f746ecb494b087878ce8397e7c","kind":"oracle","name":"sub","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"10":{"interface_hash":"47ca0d92dc35e402faca3b1bce44bc6b9d2f047bdf5921cd40093eeca9aa3f45","kind":"oracle","name":"urem","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"11":{"interface_hash":"115fb415f346d9066d5edd800ec3710fea7d6e5da3baf10491341d097f900fae","kind":"oracle","name":"sdiv","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"12":{"interface_hash":"02a4afa08d8a425d1d7a3737c8da3a2c27b5d9fcaf528ba17f46e4bcaa4b87e2","kind":"oracle","name":"srem","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"13":{"interface_hash":"2f2605b2208e04ed6f91cf3f8375b9c70839038c0c8209cac79bee33280d152c","kind":"oracle","name":"eq","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"14":{"interface_hash":"8ec6f6ce7f64dc1bfb699e6166c919b59de152d8b7227783c89eb1f87b87886c","kind":"oracle","name":"ne","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"15":{"interface_hash":"84f277fc86190b7d3986429b5f8958057c574dccbb5a652ca9a6de7e827702b4","kind":"oracle","name":"ult","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"16":{"interface_hash":"89739797986f1edc445035af8de35eedfe4495fe9d1e7e91ae626ae9004c2f11","kind":"oracle","name":"ule","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"17":{"interface_hash":"c77dfe5f449851d9c44b4f06070166c6f1161f5ff42e6ebe9824776dca18ee31","kind":"oracle","name":"slt","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"18":{"interface_hash":"fad9f7b527b8a6142f938078be56cedf05333583633636031027cd0286352e42","kind":"oracle","name":"sle","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"19":{"interface_hash":"8666f45532a3e411d9b74245fbac9d868d9bb74b58c35cf48dc507f38c0fb8df","kind":"oracle","name":"select","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"2":{"interface_hash":"3201940a9efdc65fe248f48883412904740b49486dba3bce20b2c75230ce80f7","kind":"oracle","name":"mul","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"20":{"interface_hash":"df2e1f2c1b24610d7e868f6f8a4cb1865e7c05f9637ae1e0438f93636eed4f11","kind":"oracle","name":"casts","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"21":{"interface_hash":"dfa3e93a694fd26506ab85fdb5c91cc2f7240e5c67ac2f96489aff4415ae43cd","kind":"oracle","name":"parmov","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"22":{"interface_hash":"0dc6f86ee00be08f2a9a93b13c3bb15f10fd6c5fb7724afc50d818525b2ca908","kind":"oracle","name":"jump","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"23":{"interface_hash":"0b0f368147c4bf9c5fcffc84abb37ee1775504d13204ed6fcd6b19b735c00abf","kind":"oracle","name":"badjump","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"24":{"interface_hash":"1f5780fc3ed3345fb966ec20479590f11403222b2889dc8a76ad6e2cb9026f25","kind":"oracle","name":"fault0","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"25":{"interface_hash":"569088300ff8a05a82e69a1fa7af2569c976892b46f33cf4256debbe49f28c88","kind":"oracle","name":"fault1","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"26":{"interface_hash":"8012e4889e407a4fd174d943b4ca9cd3281a008c50ceaccb24a8566529fd2a18","kind":"oracle","name":"fault2","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"27":{"interface_hash":"64962111607ff89d5875a2044ee582d558ff1e51570a1703d8541eb15b0aef67","kind":"oracle","name":"fault3","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"28":{"interface_hash":"1025848f6bd2dcf9697b2bf1933aa9b4ce8293ec7c252538c92d5d04a295d2e8","kind":"oracle","name":"fault4","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"29":{"interface_hash":"7e21c6f8f21d6746da6357344ca5aaf21e84d50f6352970744eb052a21158c16","kind":"oracle","name":"fault5","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"3":{"interface_hash":"bf8e3bb2f7c71c884f5632c3ae27be18ba6854bac45ec83d3d7b5ab42d9160ac","kind":"oracle","name":"and","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"30":{"interface_hash":"e3174365e07ee50aea728a15c1529eb69d3dd71ee0189e86135ce59336b99654","kind":"oracle","name":"fault6","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"31":{"interface_hash":"feee076120be5fb4b5c60870794a5951fc02bd764996b00b5a98fcf4df7c21b7","kind":"oracle","name":"fault7","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"32":{"interface_hash":"3f9151ece9237c1ffc912095056f4e03331d1b4e05d77b0f64985f95d07248ee","kind":"oracle","name":"fault8","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"33":{"interface_hash":"a953e00368a00f72dd71de2f704258d4c4ede6e46a11c43400f117277befbd3d","kind":"oracle","name":"fault9","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"34":{"interface_hash":"9331bcea7de7b1492be6918c6e29e5635a5f9faf6d54cce3a498cae23b7e83e3","kind":"oracle","name":"fault10","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"4":{"interface_hash":"fbfd5ca4f0d388fd3e9c51f7be47eac64bbd208760ee23b77778c2d793c28391","kind":"oracle","name":"or","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"5":{"interface_hash":"c2d37f0c1c6740bb8ca00e7a0cd766101a34953e97353e9bc883b27a654e8adf","kind":"oracle","name":"xor","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"6":{"interface_hash":"f58b391c05e70784bbb6da613f5a690282026fca38f7a3409bb07e1bb527bc5a","kind":"oracle","name":"shl","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"7":{"interface_hash":"c5e57c21e06831cfcfb142078cb72ef2366f1c5bc591808001eb7ea3601594c4","kind":"oracle","name":"lshr","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"8":{"interface_hash":"2dc127ee704b144c5ff8110fbce24ebfc8ae148670deb64dbb7c458de84ff5ca","kind":"oracle","name":"ashr","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"9":{"interface_hash":"394b35c6548da71eb06f4ebbdf620c7fe900eff4359464c51216f3dc07a9cc62","kind":"oracle","name":"udiv","signature":{"abi":"0.8","args":[],"fault":4,"in":[8,8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}}}

section functions
oracle @add (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
r = lift.add x y
lift.retval r
oracle @sub (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
r = lift.sub x y
lift.retval r
oracle @mul (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
r = lift.mul x y
lift.retval r
oracle @and (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
r = lift.and x y
lift.retval r
oracle @or (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
r = lift.or x y
lift.retval r
oracle @xor (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
r = lift.xor x y
lift.retval r
oracle @shl (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
r = lift.shl x y
lift.retval r
oracle @lshr (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
r = lift.lshr x y
lift.retval r
oracle @ashr (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
r = lift.ashr x y
lift.retval r
oracle @udiv (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
r = lift.udiv x y
lift.retval r
oracle @urem (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
r = lift.urem x y
lift.retval r
oracle @sdiv (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
r = lift.sdiv x y
lift.retval r
oracle @srem (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
r = lift.srem x y
lift.retval r
oracle @eq (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { p:reg[1], r:reg[8] }
^entry():
p = lift.icmp.eq x y
r = lift.zext.i8 p
lift.retval r
oracle @ne (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { p:reg[1], r:reg[8] }
^entry():
p = lift.icmp.ne x y
r = lift.zext.i8 p
lift.retval r
oracle @ult (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { p:reg[1], r:reg[8] }
^entry():
p = lift.icmp.ult x y
r = lift.zext.i8 p
lift.retval r
oracle @ule (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { p:reg[1], r:reg[8] }
^entry():
p = lift.icmp.ule x y
r = lift.zext.i8 p
lift.retval r
oracle @slt (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { p:reg[1], r:reg[8] }
^entry():
p = lift.icmp.slt x y
r = lift.zext.i8 p
lift.retval r
oracle @sle (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { p:reg[1], r:reg[8] }
^entry():
p = lift.icmp.sle x y
r = lift.zext.i8 p
lift.retval r
oracle @select (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { p:reg[1], r:reg[8] }
^entry():
p = lift.const.i1 1
r = lift.select p x y
lift.retval r
oracle @casts (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { wide:reg[16], eight:reg[16], r:reg[8] }
^entry():
wide = lift.sext.i16 x
eight = lift.const.i16 8
wide = lift.lshr wide eight
r = lift.trunc.i8 wide
lift.retval r
oracle @parmov (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8], s:reg[8] }
^entry():
r = lift.mov x
s = lift.mov y
(r, s) = lift.parmov (s, r)
lift.retval r
oracle @jump (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { z:reg[8], p:reg[1], idx:reg[32], r:reg[8] }
^entry():
z = lift.const.i8 0
p = lift.icmp.ne x z
qbranch p ^yes ^no
^yes():
r = lift.mov y
qjump ^done
^no():
idx = lift.label ^fortytwo
qjumpr idx
^fortytwo():
r = lift.const.i8 42
qjump ^done
^done():
lift.retval r
oracle @badjump (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { idx:reg[32] }
^entry():
idx = lift.const.i32 4294967295
qjumpr idx
oracle @fault0 (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
fault 0
oracle @fault1 (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
fault 1
oracle @fault2 (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
fault 2
oracle @fault3 (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
fault 3
oracle @fault4 (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
fault 4
oracle @fault5 (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
fault 5
oracle @fault6 (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
fault 6
oracle @fault7 (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
fault 7
oracle @fault8 (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
fault 8
oracle @fault9 (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
fault 9
oracle @fault10 (x:wire[8] in, y:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { r:reg[8] }
^entry():
fault 10
````

## `tests/fixtures/arithmetic.comments` (1 lines)

````
Hand-derived vectors: arithmetic is modulo 256. 255+2=1, 0-1=255, 128*3=128; 0xaa & 0xf0=0xa0, OR=0xfa, XOR=0x5a. Shifts >=8 give zero including signed right shift. Signed -7/2 truncates to -3 (253), remainder -1 (255). Signed -128/-1 faults 6, division by zero faults 5. sext(0x80) to 16 bits gives 0xff80; logical shift by 8 and trunc gives 255. parmov swaps 3 and 9, returns 9. jump(0,0) returns 42, jump(1,9) returns 9. badjump faults 4. fault0..fault10 XOR the named literal fault code and return no payload.
````

## `tests/fixtures/classical.bisa` (105 lines)

````
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=16

section symbols
{"0":{"interface_hash":"0fe8c7991be189017d08024a7b880f04646a46bd0831a4de093cd99a063918ab","kind":"r","name":"sum","signature":{"abi":"0.8","kind":"r","params":["i8"],"results":["i8"],"tier":"r"}},"1":{"interface_hash":"e8a3dc5429049b16559aa6a4262779e3dcd37a758967def4e08c371a5b765fff","kind":"r","name":"g","signature":{"abi":"0.8","kind":"r","params":["ptr"],"results":[],"tier":"r"}},"10":{"interface_hash":"6ef7b54c8ab5641636211b2d43f0df86cfbc129916db3b25b805e7ad33b97774","kind":"cc","name":"host","signature":{"abi":"0.8","kind":"cc","params":[],"results":["i16"],"tier":"cc"}},"11":{"interface_hash":"cd54f756eb0a65f3c2881453c9c7e03d44e1ae9c651ca01efdeede661b3fb573","kind":"cc","name":"host_invalid","signature":{"abi":"0.8","kind":"cc","params":[],"results":["i16"],"tier":"cc"}},"2":{"interface_hash":"564cbe6a49414643ca03211d12c78f3cf431ba3d2ecf0c8b06ea1aafc0392389","kind":"r","name":"f","signature":{"abi":"0.8","kind":"r","params":["ptr"],"results":[],"tier":"r"}},"3":{"interface_hash":"e0db43691a75656b7a37a8156ca44cfa17523a63c0e2a36e20433869c7b1112b","kind":"r","name":"nested","signature":{"abi":"0.8","kind":"r","params":[],"results":["i64"],"tier":"r"}},"4":{"interface_hash":"f1344e767c6ce40993c3c6164eba4d58ac6bb8bbbfdba33de7400aa795d4c0b9","kind":"r","name":"effects","signature":{"abi":"0.8","kind":"r","params":[],"results":["i64"],"tier":"r"}},"5":{"interface_hash":"c8b90ca42cbf14f0ac90c4395b94100ddbe1319688931014e900acb2a4694840","kind":"r","name":"impure","signature":{"abi":"0.8","kind":"r","params":[],"results":[],"tier":"r"}},"6":{"interface_hash":"260aa61d5d96b991e946e2fd4986fe9e319e2c43ef374e8f90d85c112b3d5b88","kind":"r","name":"entropy_short","signature":{"abi":"0.8","kind":"r","params":[],"results":[],"tier":"r"}},"7":{"interface_hash":"9ccebed66dd2a159125d50818ef06c82b8512612940a695605826fd3452d3524","kind":"r","name":"unknown_effect","signature":{"abi":"0.8","kind":"r","params":[],"results":[],"tier":"r"}},"8":{"interface_hash":"818b6f38c57d9afe5fbad77a00457a7f9f3484af7f3d25e3b6238b6ea301ba7e","kind":"r","name":"memfault","signature":{"abi":"0.8","kind":"r","params":[],"results":["i8"],"tier":"r"}},"9":{"interface_hash":"30fd03864fe91c61b0c8aa2ce72a158e1647c02a9dc655fa1018c5196b4efbfd","kind":"r","name":"divzero","signature":{"abi":"0.8","kind":"r","params":[],"results":["i8"],"tier":"r"}}}

section functions
fn r @sum (n:i8) (answer:i8) () () ()
^entry():
zero = const.i8 0
one = const.i8 1
br ^loop(n, zero)
^loop(i:i8, acc:i8):
p = icmp.eq i zero
br p ^done(acc) ^more(i, acc)
^more(ii:i8, aa:i8):
next = sub ii one
s = add aa ii
br ^loop(next, s)
^done(answer:i8):
ret answer
fn r @g (p:ptr) () () () ()
^entry():
effect clock.read p
ret
fn r @f (p:ptr) () () () ()
^entry():
call @g p
uncall @g (p) ()
ret
fn r @nested () (r:i64) () () ()
^entry():
n = const.i16 1024
p = alloc n
call @f p
r = load.i64 p
uncall @f (p) ()
ret r
fn r @effects () (r:i64) () () ()
^entry():
n = const.i16 1024
p = alloc n
len = const.i16 3
effect entropy.read p len
effect console.write p len
effect clock.read p
sector = const.i64 7
effect block.write sector p
effect block.read sector p
r = load.i64 p
ret r
fn r @impure () () () () ()
^entry():
n = const.i16 1024
p = alloc n
call @g p
v = const.i64 0
store.i64 p v
uncall @g (p) ()
ret
fn r @entropy_short () () () () ()
^entry():
n = const.i16 1024
p = alloc n
len = const.i16 3
effect entropy.read p len
ret
fn r @unknown_effect () () () () ()
^entry():
n = const.i16 1024
p = alloc n
effect missing.op p
ret
fn r @memfault () (r:i8) () () ()
^entry():
z = const.i16 0
p = inttoptr z
r = load.i8 p
ret r
fn r @divzero () (r:i8) () () ()
^entry():
a = const.i8 3
b = const.i8 0
r = udiv a b
ret r
fn cc @host () (len:i16) () () ()
^entry():
n = const.i16 3
p = alloc n
v = const.i8 165
store.i8 p v
len = hostcall org.bennett.test p n
ret len
fn cc @host_invalid () (len:i16) () () ()
^entry():
n = const.i16 3
z = const.i16 0
p = inttoptr z
len = hostcall org.bennett.test p n
ret len

section devices
{"models":{"block":{"version":"0.8"},"clock":{"version":"0.8"},"console":{"version":"0.8"},"entropy":{"version":"0.8"}},"services":{"org.bennett.test":{"version":"1"}}}

section layout
{"A_tab":4,"H":12,"S_cells":0,"globals":{},"heap_base":16,"heap_limit_max":1024,"interface_regions":{},"null_size":1,"ptr_width":16}
````

## `tests/fixtures/classical.comments` (2 lines)

````
Hand derivations: sum(n) accumulates n+(n-1)+...+1, hence n(n+1)/2 for n<=8. nested calls f, whose clock.read in g is cancelled by an inner uncall; uncalling f must skip those frames, leaving clock=0. effects copies entropy [11,22,33] to console, clock.read writes initial 0, then block.write/read sector 7; five tape entries, clock=1, return 0. Whole reversal removes the formerly absent sector. impure performs store after g, so uncall faults 4. entropy_short has live destination but empty tape and faults 10 atomically. Unknown device faults 8. Null load faults 7; 3/0 faults 5.
Host: request is a5 00 00 in a three-byte allocation. Reply 11 22 33 44 55 writes 11 22 33 and returns full length 5; reversal restores the original bytes and then allocation. Null host pointer faults 7 before making a request.
````

## `tests/fixtures/heap.bisa` (73 lines)

````
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=16

section symbols
{"0":{"interface_hash":"30660357457354b768b86e153f366ead95aeac5d125e860d8e6cb8743f8d35a8","kind":"oracle","name":"heap","signature":{"abi":"0.8","args":[],"fault":4,"in":[],"kind":"oracle","mem":[],"tgt":16,"tier":"q"}},"1":{"interface_hash":"415e0ce86806f048d197ed864b321091a00cc27575e56b7661a85958ad17b20d","kind":"oracle","name":"zeroalloc","signature":{"abi":"0.8","args":[],"fault":4,"in":[],"kind":"oracle","mem":[],"tgt":16,"tier":"q"}},"2":{"interface_hash":"b4e19ac0b85b4c81d01de0e0e8f15b5a631fdaec8dca6680c17175e81ea945d7","kind":"oracle","name":"afterfree","signature":{"abi":"0.8","args":[],"fault":4,"in":[],"kind":"oracle","mem":[],"tgt":16,"tier":"q"}},"3":{"interface_hash":"7fbc54ee4a45cf4ebaeb84b5d9344b3fa04906b125784404342055b075509197","kind":"oracle","name":"pinned","signature":{"abi":"0.8","args":[],"fault":4,"in":[],"kind":"oracle","mem":[],"tgt":16,"tier":"q"}},"4":{"interface_hash":"86f87b18056089dd5ab1648a9843bb8f69d3cb6ac70755866be63ef068c425d4","kind":"oracle","name":"doublefree","signature":{"abi":"0.8","args":[],"fault":4,"in":[],"kind":"oracle","mem":[],"tgt":16,"tier":"q"}},"5":{"interface_hash":"b4147fd646bdfdc270596c04cb445561fe401774e1fdd178fcde3e77a5699725","kind":"oracle","name":"badstore","signature":{"abi":"0.8","args":[],"fault":4,"in":[],"kind":"oracle","mem":[],"tgt":16,"tier":"q"}},"6":{"interface_hash":"a06203de444a4a9a9a34a6781efee8e6290b27d79ed102165e5e2edd571fd56f","kind":"oracle","name":"outoftable","signature":{"abi":"0.8","args":[],"fault":4,"in":[],"kind":"oracle","mem":[],"tgt":16,"tier":"q"}},"7":{"interface_hash":"3ef6c026118750eebb4c309eadf18c20eab4daab5aa5ef05b25dd7861238cd50","kind":"oracle","name":"faultif","signature":{"abi":"0.8","args":[],"fault":4,"in":[],"kind":"oracle","mem":[],"tgt":16,"tier":"q"}},"8":{"interface_hash":"f5c5556f79f032f7a0607387d69cab7bbb21988ca15461645340abb11e562813","kind":"data","name":"g","signature":{"abi":"0.8","kind":"data","size":1,"tier":"-"}}}

section functions
oracle @heap () (t:wire[16]) (f:wire[4]) () ()
regs { p:reg[16], q:reg[16], n:reg[16], v:reg[16], r:reg[16], c:reg[1] }
^entry():
n = lift.const.i16 2
p = lift.alloc n
v = lift.const.i16 4660
lift.store.i16 p v
r = lift.load.i16 p
lift.free p
lift.retval r
oracle @zeroalloc () (t:wire[16]) (f:wire[4]) () ()
regs { p:reg[16], q:reg[16], n:reg[16], v:reg[16], r:reg[16], c:reg[1] }
^entry():
p = lift.alloc 0
q = lift.alloc 0
r = lift.sub q p
lift.retval r
oracle @afterfree () (t:wire[16]) (f:wire[4]) () ()
regs { p:reg[16], q:reg[16], n:reg[16], v:reg[16], r:reg[16], c:reg[1] }
^entry():
n = lift.const.i16 2
p = lift.alloc n
v = lift.const.i16 4660
lift.free p
r = lift.load.i16 p
lift.retval r
oracle @pinned () (t:wire[16]) (f:wire[4]) () ()
regs { p:reg[16], q:reg[16], n:reg[16], v:reg[16], r:reg[16], c:reg[1] }
^entry():
p = lift.addr @g
lift.free p
lift.retval r
oracle @doublefree () (t:wire[16]) (f:wire[4]) () ()
regs { p:reg[16], q:reg[16], n:reg[16], v:reg[16], r:reg[16], c:reg[1] }
^entry():
n = lift.const.i16 2
p = lift.alloc n
v = lift.const.i16 4660
lift.free p
lift.free p
lift.retval r
oracle @badstore () (t:wire[16]) (f:wire[4]) () ()
regs { p:reg[16], q:reg[16], n:reg[16], v:reg[16], r:reg[16], c:reg[1] }
^entry():
p = lift.const.i16 0
lift.store.i16 p v
lift.retval r
oracle @outoftable () (t:wire[16]) (f:wire[4]) () ()
regs { p:reg[16], q:reg[16], n:reg[16], v:reg[16], r:reg[16], c:reg[1] }
^entry():
p = lift.alloc 0
p = lift.alloc 0
p = lift.alloc 0
p = lift.alloc 0
lift.retval r
oracle @faultif () (t:wire[16]) (f:wire[4]) () ()
regs { p:reg[16], q:reg[16], n:reg[16], v:reg[16], r:reg[16], c:reg[1] }
^entry():
c = lift.const.i1 1
lift.faultif c 9
lift.retval r

section data
g 00

section layout
{"A_tab":2,"H":8,"S_cells":0,"globals":{"g":{"base":16,"image":"g","size":1}},"heap_base":32,"heap_limit_max":32,"interface_regions":{},"null_size":1,"ptr_width":16}
````

## `tests/fixtures/heap.comments` (1 lines)

````
Hand-derived vectors: heap_base=32, heap_limit=32, initial pinned g=(16,1); table capacity=4. heap allocates two bytes at 32, stores 0x1234 little endian (34 12), loads 4660. heap_limit=1 faults 2. Two zero-sized allocations still consume one byte each, so returned pointers differ by 1. Freed, pinned, double-freed, null store accesses fault 7. Three new allocations fill the table; the fourth faults 2. faultif(true,9) gives (0,9).
````

## `tests/fixtures/inc8.bisa` (12 lines)

````
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=32

section symbols
{"0":{"interface_hash":"8ce5e64f15830d8e596ba9b4861def6565dd567b5804300f427d8b9566d5be93","kind":"oracle","name":"inc8","signature":{"abi":"0.8","args":[],"fault":4,"in":[8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}}}

section functions
oracle @inc8 (x:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { one:reg[8], r:reg[8] }
^entry():
one = lift.const.i8 1
r = lift.add x one
lift.retval r
````

## `tests/fixtures/inc8.comments` (1 lines)

````
Hand derivation (§16.3): x=255, one=1, r=(255+1) mod 256=0. Three rows; B=2 gives (0,1). B=0 executes zero rows and gives (0,1).
````

## `tests/fixtures/mutual.bisa` (29 lines)

````
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=16

section symbols
{"0":{"interface_hash":"598fdf171d0a201d52e8fbe2339c70d1a26b36a72dcd60503c87c51dff88039b","kind":"oracle","name":"main","signature":{"abi":"0.8","args":[],"fault":4,"in":[],"kind":"oracle","mem":[],"tgt":16,"tier":"q"}},"1":{"interface_hash":"e4028cf7347c2779e19c8193ef1039837944acebd4784e9c3a42fbe236e737ec","kind":"lproc","name":"f","signature":{"abi":"0.8","kind":"lproc","params":[],"result":16,"tier":"q"}},"2":{"interface_hash":"7dc9c25aff5230a46ae697edf187d34ba72a03f7a3c1a520c6fc6bf5462c6374","kind":"lproc","name":"g","signature":{"abi":"0.8","kind":"lproc","params":[],"result":16,"tier":"q"}}}

section functions
oracle @main () (t:wire[16]) (fault:wire[4]) () ()
regs { r:reg[16] }
^entry():
r = lift.call @g ()
lift.retval r
lproc @f () (r:reg[16]) () () ()
^entry():
r = lift.call @g ()
lift.ret r
lproc @g () (r:reg[16]) () () ()
regs { p:reg[1] }
^entry():
p = lift.const.i1 1
qbranch p ^done ^recurse
^done():
r = lift.label ^entry
lift.ret r
^recurse():
r = lift.call @f ()
lift.ret r

section layout
{"A_tab":0,"H":8,"S_cells":5,"globals":{},"heap_base":16,"heap_limit_max":0,"interface_regions":{},"null_size":1,"ptr_width":16}
````

## `tests/fixtures/mutual.comments` (1 lines)

````
Hand derivation: main has indices 0..2. The f,g SCC is ordered by names, hence f has indices 2..4 and g starts at 4. g always takes done and returns lift.label ^entry = 4, in six total executed rows. The fixture deliberately has hash(f)>hash(g), so sorting individual closure hashes gives the wrong label value 2.
````

## `tests/fixtures/nested.bisa` (31 lines)

````
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=32

section symbols
{"0":{"interface_hash":"8ce5e64f15830d8e596ba9b4861def6565dd567b5804300f427d8b9566d5be93","kind":"oracle","name":"inc8","signature":{"abi":"0.8","args":[],"fault":4,"in":[8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"1":{"interface_hash":"562ad89a1befd9629409f21362684d92dc9d57b93968b1d6d5a868e6e2bc6afd","kind":"oracle","name":"nested","signature":{"abi":"0.8","args":["token"],"fault":4,"in":[8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"2":{"interface_hash":"c98f82615ce05c7f82ee89d9106ae0655f3396332ad2a6616f63266c03043c34","kind":"oracle","name":"cancel","signature":{"abi":"0.8","args":["token"],"fault":4,"in":[8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}},"3":{"interface_hash":"9687f21af62158ff87ab8a974e056774ee75b531e158cc4538a11d4631f89012","kind":"oracle","name":"ignore","signature":{"abi":"0.8","args":["token"],"fault":4,"in":[8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}}}

section functions
oracle @inc8 (x:wire[8] in) (t:wire[8]) (f:wire[4]) () ()
regs { one:reg[8], r:reg[8] }
^entry():
one = lift.const.i8 1
r = lift.add x one
lift.retval r
oracle @nested (x:wire[8] in) (t:wire[8]) (f:wire[4]) () (tk:token)
regs { r:reg[8], fr:reg[4], zero:reg[4], p:reg[1] }
^entry():
lift.oracle_call @inc8 tk (x) r fr () ()
zero = lift.const.i4 0
p = lift.icmp.ne fr zero
lift.faultif p 9
lift.retval r
oracle @cancel (x:wire[8] in) (t:wire[8]) (f:wire[4]) () (tk:token)
regs { r:reg[8], fr:reg[4], zero:reg[4], p:reg[1] }
^entry():
lift.oracle_call @inc8 tk (x) r fr () ()
lift.oracle_uncall @inc8 tk (x) r fr () ()
lift.retval r
oracle @ignore (x:wire[8] in) (t:wire[8]) (f:wire[4]) () (tk:token)
regs { r:reg[8], fr:reg[4], zero:reg[4], p:reg[1] }
^entry():
lift.oracle_call @inc8 tk (x) r fr () ()
lift.retval r
````

## `tests/fixtures/nested.comments` (1 lines)

````
Hand derivation: inc8(8)=9 in three rows. nested calls it, compares fr to zero, and raises FAULT_CALLEE=9 on an unsuccessful inner budget. cancel calls then uncalls with identical ins/mem/token, so target and fr return to zero even for a callee fault. ignore returns a zero payload when the callee faults without automatic propagation. inc8(255)=0 by 8-bit wrap.
````

## `tests/fixtures/registers.bisa` (50 lines)

````
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=32

section symbols
{"0":{"interface_hash":"de3621c3dee0d970a86479e38ff4088730604a5b4d16429b71af2ec85ab0f42f","kind":"perm_action","name":"toggle","signature":{"abi":"0.8","args":[],"bounds":[],"in":[],"kind":"perm_action","mem":[],"mut":[1],"tier":"q"}},"1":{"interface_hash":"0f633b7a5f72475dc249883c0b8c6a3c91bfe62d40de642013afb5bd2015f149","kind":"action","name":"bell","signature":{"abi":"0.8","args":[],"bounds":[],"in":[],"kind":"action","mem":[],"mut":[2],"tier":"q"}},"2":{"interface_hash":"20449c3d1c45ec590a7f7b356ed59719e2daaec9bbaa18f8da2eaa43dfab0008","kind":"cc","name":"allocation","signature":{"abi":"0.8","kind":"cc","params":[],"results":[],"tier":"cc"}},"3":{"interface_hash":"6ea78656c92cd787bea86133572e2c9766d3f70208676cad0c043731c0fd6102","kind":"cc","name":"views","signature":{"abi":"0.8","kind":"cc","params":[],"results":[],"tier":"cc"}},"4":{"interface_hash":"fe0d76be58a95d67e2619cd08f33cd9e25ba530a09d6fa848d6bf955e162f56b","kind":"cc","name":"unclean","signature":{"abi":"0.8","kind":"cc","params":[],"results":[],"tier":"cc"}},"5":{"interface_hash":"dfc970cdea49da3834707362043d64ff084bcb641da635034e4cce0271b2943f","kind":"cc","name":"measurement","signature":{"abi":"0.8","kind":"cc","params":[],"results":["i2"],"tier":"cc"}},"6":{"interface_hash":"16b81231139518e906b5bebd7fb10a0b0054b427404bdfdf7eb45487aa844d8c","kind":"r","name":"measuring","signature":{"abi":"0.8","kind":"r","params":[],"results":["i2"],"tier":"r"}},"7":{"interface_hash":"c21d3737583af9c15d6011a94e2b885a8b179bb697e3a3d9ed29dfcc64a65ed4","kind":"cc","name":"bad_uncall","signature":{"abi":"0.8","kind":"cc","params":[],"results":["i2"],"tier":"cc"}}}

section functions
perm_action @toggle (t:wire mut) () () () ()
^entry():
x t
action @bell (t:wire[2] mut) () () () ()
^entry():
h t[0]
cx t[0] t[1]
fn cc @allocation () () () () ()
^entry():
a = qreg.new any 1
b = qreg.new any 1
q = qreg.concat a b
qreg.free q
ret
fn cc @views () () () () ()
^entry():
q = qreg.new any 2
s = qreg.slice q 0 1
action_call @toggle (s) () () ()
s2 = qreg.slice q 0 1
action_call @toggle (s2) () () ()
qreg.free q
ret
fn cc @unclean () () () () ()
^entry():
q = qreg.new any 1
action_call @toggle (q) () () ()
qreg.free q
ret
fn cc @measurement () (r:i2) () () ()
^entry():
q = qreg.new any 2
action_call @bell (q) () () ()
r = measure q
ret r
fn r @measuring () (r:i2) () () ()
^entry():
r = call @measurement
ret r
fn cc @bad_uncall () (r:i2) () () ()
^entry():
r = call @measuring
uncall @measuring () (r)
ret r
````

## `tests/fixtures/registers.comments` (1 lines)

````
Hand-derived vectors: allocation concatenates two clean one-wire qregs and frees the resulting clean two-wire qreg. views flips bit 0 through a view twice; each region call consumes that view and restores its parent to live, so free succeeds. unclean flips a one-wire qreg once, so free traps with code 4 before consuming it. measurement produces Bell amplitudes at 00 and 11, probabilities 1/2; draws 0.1 and 0.9 select 0 and 3 respectively. measuring wraps that call; bad_uncall must trap 4 because the segment contains measurement. Reversal restores handle states and wire identities for reversible traces; measurement traces are ineligible.
````

## `tests/fixtures/sum_db.bisa` (39 lines)

````
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=32

section symbols
{"0":{"interface_hash":"68225d213c44812fe844cd295d8821127c3cf31682be4eb19303cb53f9b147f7","kind":"oracle","name":"sum_db","signature":{"abi":"0.8","args":[],"fault":4,"in":[8],"kind":"oracle","mem":[{"A":4,"W":8,"role":"in"}],"tgt":8,"tier":"q"}},"1":{"interface_hash":"74f110bbafde68a4785025e7e571ef871ddd83a09465ab9c1604f653a0cfcd92","kind":"lproc","name":"sum","signature":{"abi":"0.8","kind":"lproc","params":[8,8,32],"result":8,"tier":"q"}},"2":{"interface_hash":"7002ed5ea010907a0ae99065663f22fb7d18ca1d6cb171fed57e2594bd9367e6","kind":"data","name":"zero","signature":{"abi":"0.8","kind":"data","size":1,"tier":"-"}}}

section functions
oracle @sum_db (n:wire[8] in) (t:wire[8]) (f:wire[4]) (db:region[4,8] in) ()
regs { base:reg[32], acc:reg[8], r:reg[8] }
^entry():
base = lift.addr @db
acc = lift.const.i8 0
r = lift.call @sum (n, acc, base)
lift.retval r
lproc @sum (n:reg[8], acc:reg[8], base:reg[32]) (r:reg[8]) () () ()
regs { zp:reg[32], zv:reg[8], z:reg[1], one:reg[8], n2:reg[8], idx:reg[32], p:reg[32], v:reg[8], acc2:reg[8] }
^entry():
zp = lift.addr @zero
lift.boundscheck zp 1
zv = lift.load.i8 zp
z = lift.icmp.eq n zv
qbranch z ^done ^more
^more():
one = lift.const.i8 1
n2 = lift.sub n one
idx = lift.zext.i32 n2
p = lift.add base idx
lift.boundscheck p 1
v = lift.load.i8 p
acc2 = lift.add acc v
r = lift.call @sum (n2, acc2, base)
lift.ret r
^done():
lift.ret acc

section data
zero 00

section layout
{"A_tab":4,"H":13,"S_cells":9,"globals":{"zero":{"base":16,"image":"zero","size":1}},"heap_base":4112,"heap_limit_max":4080,"interface_regions":{"sum_db":{"db":{"base":4096}}},"null_size":16,"ptr_width":32}
````

## `tests/fixtures/sum_db.comments` (1 lines)

````
Hand derivation (§16.3): db=[1,2,...,16], n=3 sums 3+2+1=6. Each sum activation has 3+3+1+9=16 cells; n=16 needs 17*16=272. 271 faults code 3. n=17 first checks db[16], fault code 7.
````

## `tests/fixtures/tiny_memory.bisa` (20 lines)

````
bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=8

section symbols
{"0":{"interface_hash":"be21636357102b2a324f99db1bd058ad82f1c2eb3337d99f22a2533a32436142","kind":"oracle","name":"tiny","signature":{"abi":"0.8","args":[],"fault":4,"in":[1],"kind":"oracle","mem":[{"A":0,"W":8,"role":"in"}],"tgt":1,"tier":"q"}}}

section functions
oracle @tiny (x:wire in) (t:wire) (f:wire[4]) (db:region[0,8] in) ()
regs { p:reg[8], b:reg[8], v:reg[8], q:reg[8], one:reg[8], zero:reg[8], bit:reg[1] }
^entry():
p = lift.addr @db
b = lift.zext.i8 x
v = lift.load.i8 p
q = lift.udiv v b
one = lift.const.i8 1
q = lift.and q one
bit = lift.icmp.ne q zero
lift.retval bit

section layout
{"A_tab":0,"H":5,"S_cells":0,"globals":{},"heap_base":24,"heap_limit_max":0,"interface_regions":{"tiny":{"db":{"base":16}}},"null_size":1,"ptr_width":8}
````

## `tests/fixtures/tiny_memory.comments` (1 lines)

````
Hand derivation over full D (14 bits): input x is one bit, db is one caller-owned byte, target one bit, fault four bits. Rows: addr, zext x, load db, udiv(db,x), const one, and, icmp, retval. x=0 faults DIV0=5 at row 4. x=1 returns db&1 at row 8. Earlier prefixes give step-budget fault 1. B=9 has one idle HALT frame. Every target/fault entry value is checked by explicit commit and every internal location/frame/byte/pre-entry must restore.
````

## `tests/identity.rs` (185 lines)

````rust
use bennett_isa_ref::{sha256_hex, Object};

#[test]
fn fips_180_4_sha256_vectors() {
    for (input, expected) in [
        ("", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
        ("abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
        ("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"),
        ("abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu", "cf5b16a778af8380036ce59e7b0492370b249b11e8f07a51afac45037afee9d1"),
    ] { assert_eq!(sha256_hex(input.as_bytes()), expected); }
    assert_eq!(
        sha256_hex(&vec![b'a'; 1_000_000]),
        "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0"
    );
}

#[test]
fn all_four_published_hashes_and_printed_envelopes() {
    let spec = include_str!("../../spec/Bennett-ISA-Spec.md");
    let mut hashes = std::collections::BTreeMap::new();
    let mut envelopes = Vec::new();
    for fixture in [
        include_str!("fixtures/inc8.bisa"),
        include_str!("fixtures/sum_db.bisa"),
    ] {
        let object = Object::parse(fixture).unwrap();
        let identity = object.identity().unwrap();
        object.check_hashes().unwrap();
        for (name, hash) in identity.interface_hashes {
            assert_eq!(
                identity.closure_hashes[&name].as_deref(),
                Some(hash.as_str())
            );
            hashes.insert(name, hash);
        }
        envelopes.extend(identity.envelopes.into_values());
    }
    for (name, expected) in [
        (
            "inc8",
            "8ce5e64f15830d8e596ba9b4861def6565dd567b5804300f427d8b9566d5be93",
        ),
        (
            "zero",
            "7002ed5ea010907a0ae99065663f22fb7d18ca1d6cb171fed57e2594bd9367e6",
        ),
        (
            "sum",
            "74f110bbafde68a4785025e7e571ef871ddd83a09465ab9c1604f653a0cfcd92",
        ),
        (
            "sum_db",
            "68225d213c44812fe844cd295d8821127c3cf31682be4eb19303cb53f9b147f7",
        ),
    ] {
        assert_eq!(hashes[name], expected);
    }
    let mut count = 0;
    for block in spec.split("```\n").skip(1) {
        if block.starts_with("isa=0.8\n") {
            let envelope = block.split("```").next().unwrap();
            assert!(
                envelopes.iter().any(|e| e == envelope),
                "printed envelope differs byte-for-byte"
            );
            count += 1;
        }
    }
    assert_eq!(count, 2);
}

#[test]
fn object_hash_excludes_only_the_three_nonsemantic_sections() {
    let raw = include_str!("fixtures/inc8.bisa");
    let base = Object::parse(raw).unwrap().identity().unwrap();
    let annotated = format!("{raw}\nsection coverage\n{{\"entries\":[]}}\n");
    let after = Object::parse(&annotated).unwrap().identity().unwrap();
    assert_eq!(base.object_hash, sha256_hex(raw.as_bytes()));
    assert_eq!(base.object_hash, after.object_hash);
    assert!(
        Object::parse(&raw.replace("lift.const.i8 1", "lift.const.i8 2"))
            .unwrap()
            .check_hashes()
            .is_err()
    );
}

#[test]
fn reference_order_and_self_scc_are_observable() {
    let raw = include_str!("fixtures/sum_db.bisa");
    let base = Object::parse(raw).unwrap().identity().unwrap();
    let env = &base.envelopes["sum"];
    assert!(env.contains("lift.call @$0"));
    assert_eq!(
        base.interface_hashes["sum"],
        sha256_hex(format!("{}:0", sha256_hex(env.as_bytes())).as_bytes())
    );
    let shifted = Object::parse(&raw.replace("\"base\":16,\"image\"", "\"base\":17,\"image\""))
        .unwrap()
        .identity()
        .unwrap();
    assert_ne!(
        base.interface_hashes["sum"],
        shifted.interface_hashes["sum"]
    );
    assert_ne!(
        base.interface_hashes["sum_db"],
        shifted.interface_hashes["sum_db"]
    );
    assert_eq!(
        base.interface_hashes["zero"],
        shifted.interface_hashes["zero"]
    );
}

#[test]
fn unmodelled_effect_is_hashable_and_keeps_its_fault_semantics() {
    let o = Object::parse(include_str!("fixtures/classical.bisa")).unwrap();
    let identity = o.identity().unwrap();
    assert!(identity.envelopes["g"].contains("device clock {\"version\":\"0.8\"}\n"));
    assert!(!identity.envelopes["unknown_effect"].contains("device missing"));
}

#[test]
fn mutual_scc_hashing_and_canonical_lproc_member_order() {
    use bennett_isa_ref::{Budget, OracleInput};
    let o = Object::parse(include_str!("fixtures/mutual.bisa")).unwrap();
    let id = o.identity().unwrap();
    assert!(
        id.interface_hashes["f"] > id.interface_hashes["g"],
        "fixture must expose sorting by member hashes"
    );
    let digest = sha256_hex(format!("{}{}", id.envelopes["f"], id.envelopes["g"]).as_bytes());
    assert_eq!(
        id.interface_hashes["f"],
        sha256_hex(format!("{digest}:0").as_bytes())
    );
    assert_eq!(
        id.interface_hashes["g"],
        sha256_hex(format!("{digest}:1").as_bytes())
    );
    assert!(id.envelopes["f"].contains("lift.call @$1"));
    assert!(id.envelopes["g"].contains("lift.call @$0"));
    let r = o
        .run_oracle(
            "main",
            &OracleInput::bits(&[]),
            Budget {
                steps: 20,
                heap: 0,
                stack: 32,
                depth: 8,
            },
        )
        .unwrap();
    assert_eq!((r.payload, r.code), (4, 0));
}

#[test]
fn every_committed_fixture_has_valid_identity() {
    for name in [
        "inc8",
        "sum_db",
        "arithmetic",
        "heap",
        "nested",
        "classical",
        "actions",
        "mutual",
        "registers",
    ] {
        let path = format!("{}/tests/fixtures/{name}.bisa", env!("CARGO_MANIFEST_DIR"));
        let text = std::fs::read_to_string(path).unwrap();
        Object::parse(&text)
            .unwrap()
            .check_hashes()
            .unwrap_or_else(|e| panic!("{name}: {e}"));
    }
    // Independently hand-assembled device/layout envelope, checked by Python hashlib.
    let o = Object::parse(include_str!("fixtures/classical.bisa")).unwrap();
    assert_eq!(
        o.identity().unwrap().interface_hashes["g"],
        "e8a3dc5429049b16559aa6a4262779e3dcd37a758967def4e08c371a5b765fff"
    );
}
````

## `tests/linking.rs` (117 lines)

````rust
mod support;
use bennett_isa_ref::{sha256_hex, Budget, Object, OracleInput};
use support::{object, rehash};
const SIG: &str =
    r#"{"abi":"0.8","args":[],"fault":4,"in":[8],"kind":"oracle","mem":[],"tgt":8,"tier":"q"}"#;
const PROC: &str = r#"{"abi":"0.8","kind":"lproc","params":[8],"result":8,"tier":"q"}"#;
const CC: &str = r#"{"abi":"0.8","kind":"r","params":["i8"],"results":["i8"],"tier":"r"}"#;
const LAYOUT:&str="\nsection layout\n{\"A_tab\":0,\"H\":8,\"S_cells\":4,\"globals\":{},\"heap_base\":16,\"heap_limit_max\":0,\"interface_regions\":{},\"null_size\":1,\"ptr_width\":32}\n";
fn library() -> Object {
    rehash(&object(&[("inc",PROC,"lproc @inc (x:reg[8]) (r:reg[8]) () () ()\nregs { one:reg[8] }\n^entry():\none = lift.const.i8 1\nr = lift.add x one\nlift.ret r")],"{}",LAYOUT))
}
fn client(pin: Option<&str>) -> String {
    let pin = pin
        .map(|h| format!(",\"pinned_closure_hash\":\"{h}\""))
        .unwrap_or_default();
    let imports = format!("{{\"inc\":{{\"signature\":{PROC}{pin}}}}}");
    object(&[("main",SIG,"oracle @main (x:wire[8] in) (t:wire[8]) (f:wire[4]) () ()\nregs { r:reg[8] }\n^entry():\nr = lift.call @inc (x)\nlift.retval r")],&imports,LAYOUT)
}
#[test]
fn unresolved_lproc_has_fingerprint_and_no_executable_closure() {
    let o = rehash(&client(None));
    let identity = o.identity().unwrap();
    let mut bytes = b"inc\0".to_vec();
    bytes.extend(PROC.as_bytes());
    let fingerprint = sha256_hex(&bytes);
    assert!(identity.envelopes["main"].contains(&format!("lift.call @{fingerprint} (x)")));
    assert_eq!(identity.closure_hashes["main"], None);
    assert!(o
        .run_oracle(
            "main",
            &OracleInput::bits(&[2]),
            Budget {
                steps: 20,
                heap: 0,
                stack: 16,
                depth: 8
            }
        )
        .is_err());
}
#[test]
fn link_resolves_calls_and_pins_and_deduplicates() {
    let lib = library();
    let pin = lib.identity().unwrap().closure_hashes["inc"]
        .clone()
        .unwrap();
    let c = rehash(&client(Some(&pin)));
    let linked = Object::link(&[c, lib.clone(), lib]).unwrap();
    linked.check_hashes().unwrap();
    assert!(linked.section("imports").is_none());
    assert_eq!(linked.functions.len(), 2);
    let result = linked
        .run_oracle(
            "main",
            &OracleInput::bits(&[255]),
            Budget {
                steps: 6,
                heap: 0,
                stack: 16,
                depth: 8,
            },
        )
        .unwrap();
    assert_eq!((result.payload, result.code, result.steps), (0, 0, 5));
}
#[test]
fn link_rejects_unresolved_signature_pin_definition_and_layout_conflicts() {
    let lib = library();
    for c in [
        client(Some(&"0".repeat(64))),
        client(None).replace("\"params\":[8]", "\"params\":[16]"),
    ] {
        let error = match Object::parse(&c) {
            Ok(c) => Object::link(&[rehash(&c.text), lib.clone()]).unwrap_err(),
            Err(e) => e,
        };
        assert!(
            error.to_string().contains("§9.3") || error.to_string().contains("§3.3"),
            "{error}"
        );
    }
    assert!(Object::link(&[rehash(&client(None))]).is_err());
    let changed = rehash(&lib.text.replace("lift.const.i8 1", "lift.const.i8 2"));
    assert!(Object::link(&[lib.clone(), changed]).is_err());
    let changed = rehash(&lib.text.replace("\"null_size\":1", "\"null_size\":2"));
    assert!(Object::link(&[lib, changed]).is_err());
}
#[test]
fn classical_and_region_import_signatures_are_validated() {
    let imports = format!("{{\"f\":{{\"signature\":{CC}}}}}");
    let raw = object(
        &[(
            "caller",
            CC,
            "fn r @caller (x:i8) (r:i8) () () ()\n^entry():\nr = call @f x\nret r",
        )],
        &imports,
        "",
    );
    assert!(Object::parse(&raw).is_ok());
    let action_sig = r#"{"abi":"0.8","args":[],"bounds":[],"in":[],"kind":"perm_action","mem":[],"mut":[8],"tier":"q"}"#;
    let imports = format!("{{\"f\":{{\"signature\":{action_sig}}}}}");
    let raw=object(&[("caller",action_sig,"perm_action @caller (x:wire[8] mut) () () () ()\n^entry():\naction_call @f (x) () () ()")],&imports,"");
    assert!(Object::parse(&raw).is_ok());
    let malformed = raw.replace("\"mut\":[8]", "\"mut\":[0]");
    assert!(Object::parse(&malformed).is_err());
}

#[test]
fn imported_quantum_region_image_resolves_by_data_signature(){
    let signature=r#"{"abi":"0.8","args":[],"bounds":[],"in":[],"kind":"perm_action","mem":[],"mut":[1],"tier":"q"}"#;
    let imports=r#"{"image":{"signature":{"abi":"0.8","kind":"data","size":1,"tier":"-"}}}"#;
    let caller=rehash(&object(&[("a",signature,"perm_action @a (t:wire mut) () () () ()\n^entry():\nqregion r 0 8 @image")],imports,""));
    let text=format!("bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=32\n\nsection symbols\n{{\"0\":{{\"interface_hash\":\"{}\",\"kind\":\"data\",\"name\":\"image\",\"signature\":{{\"abi\":\"0.8\",\"kind\":\"data\",\"size\":1,\"tier\":\"-\"}}}}}}\n\nsection data\nimage ff\n","0".repeat(64));
    let linked=Object::link(&[caller,rehash(&text)]).unwrap();linked.check_hashes().unwrap();
    let mut q=bennett_isa_ref::QuantumState::new();let t=q.allocate(1).unwrap();let mut binding=bennett_isa_ref::QuantumBindings::default();binding.bundles.insert("t".into(),t.clone());linked.execute_action("a",&mut q,&binding,false,&[]).unwrap();assert_eq!(q.read_basis(&t).unwrap(),0);
}
````

## `tests/oracle.rs` (237 lines)

````rust
use bennett_isa_ref::{Argument, Budget, Object, OracleInput};

#[test]
fn seed_inc8_full_input_domain_and_budget_boundaries() {
    let o = Object::parse(include_str!("fixtures/inc8.bisa")).unwrap();
    for x in 0..256 {
        for b in 0..=4 {
            let r = o
                .run_oracle("inc8", &OracleInput::bits(&[x]), Budget::steps(b))
                .unwrap();
            assert_eq!(
                (r.payload, r.code),
                if b >= 3 { ((x + 1) & 255, 0) } else { (0, 1) },
                "x={x},B={b}"
            );
            assert_eq!(r.steps, b.min(3));
        }
    }
}

#[test]
fn seed_recursive_memory_interface_and_stack_boundaries() {
    let o = Object::parse(include_str!("fixtures/sum_db.bisa")).unwrap();
    // Hand derivation: db[i]=i+1, so n bytes sum to n(n+1)/2.
    for n in 0..24 {
        let mut input = OracleInput::bits(&[n]);
        input.regions.insert("db".into(), (1..=16).collect());
        let budget = Budget {
            steps: 1000,
            heap: 4080,
            stack: 512,
            depth: 64,
        };
        let r = o.run_oracle("sum_db", &input, budget).unwrap();
        assert_eq!(
            (r.payload, r.code),
            if n <= 16 {
                (n * (n + 1) / 2, 0)
            } else {
                (0, 7)
            },
            "n={n}"
        );
        if n <= 16 {
            assert_eq!(r.steps, 14 * n as u64 + 10);
            for stack in [16 * (n + 1), 16 * (n + 1) - 1] {
                let r = o
                    .run_oracle("sum_db", &input, Budget { stack, ..budget })
                    .unwrap();
                assert_eq!(r.code, if stack % 16 == 0 { 0 } else { 3 });
            }
            let r = o
                .run_oracle("sum_db", &input, Budget { depth: n, ..budget })
                .unwrap();
            assert_eq!(r.code, 3);
            let r = o
                .run_oracle(
                    "sum_db",
                    &input,
                    Budget {
                        depth: n + 1,
                        ..budget
                    },
                )
                .unwrap();
            assert_eq!(r.code, 0);
            let r = o
                .run_oracle(
                    "sum_db",
                    &input,
                    Budget {
                        steps: r.steps - 1,
                        ..budget
                    },
                )
                .unwrap();
            assert_eq!(r.code, 1);
        } else {
            assert_eq!(r.steps, 13);
        }
    }
}

#[test]
fn all_arithmetic_rows_and_faults() {
    let o = Object::parse(include_str!("fixtures/arithmetic.bisa")).unwrap();
    for (name, input, expected) in [
        ("add", vec![255, 2], (1, 0)),
        ("sub", vec![0, 1], (255, 0)),
        ("mul", vec![128, 3], (128, 0)),
        ("and", vec![170, 240], (160, 0)),
        ("or", vec![170, 240], (250, 0)),
        ("xor", vec![170, 240], (90, 0)),
        ("shl", vec![1, 7], (128, 0)),
        ("shl", vec![1, 8], (0, 0)),
        ("lshr", vec![128, 7], (1, 0)),
        ("ashr", vec![128, 7], (255, 0)),
        ("ashr", vec![128, 8], (0, 0)),
        ("udiv", vec![255, 2], (127, 0)),
        ("urem", vec![255, 2], (1, 0)),
        ("sdiv", vec![249, 2], (253, 0)),
        ("srem", vec![249, 2], (255, 0)),
        ("udiv", vec![3, 0], (0, 5)),
        ("sdiv", vec![128, 255], (0, 6)),
        ("srem", vec![128, 255], (0, 6)),
        ("eq", vec![2, 2], (1, 0)),
        ("ne", vec![2, 2], (0, 0)),
        ("ult", vec![255, 0], (0, 0)),
        ("ule", vec![2, 2], (1, 0)),
        ("slt", vec![255, 0], (1, 0)),
        ("sle", vec![128, 128], (1, 0)),
        ("select", vec![2, 9], (2, 0)),
        ("casts", vec![128, 0], (255, 0)),
        ("parmov", vec![3, 9], (9, 0)),
        ("jump", vec![0, 0], (42, 0)),
        ("jump", vec![1, 9], (9, 0)),
        ("badjump", vec![0, 0], (0, 4)),
    ] {
        let r = o
            .run_oracle(name, &OracleInput::bits(&input), Budget::steps(100))
            .unwrap();
        assert_eq!((r.payload, r.code), expected, "{name} {input:?}");
    }
    for code in 0..=10 {
        let r = o
            .run_oracle(
                &format!("fault{code}"),
                &OracleInput::bits(&[0, 0]),
                Budget::steps(1),
            )
            .unwrap();
        assert_eq!((r.payload, r.code), (0, code));
    }
}

#[test]
fn heap_allocation_free_and_inherent_checks_are_total() {
    let o = Object::parse(include_str!("fixtures/heap.bisa")).unwrap();
    for (name, expected) in [
        ("heap", (0x1234, 0)),
        ("zeroalloc", (1, 0)),
        ("afterfree", (0, 7)),
        ("pinned", (0, 7)),
        ("doublefree", (0, 7)),
        ("badstore", (0, 7)),
        ("outoftable", (0, 2)),
        ("faultif", (0, 9)),
    ] {
        let r = o
            .run_oracle(
                name,
                &OracleInput::bits(&[]),
                Budget {
                    steps: 100,
                    heap: 32,
                    stack: 0,
                    depth: 0,
                },
            )
            .unwrap();
        assert_eq!((r.payload, r.code), expected, "{name}");
    }
    let r = o
        .run_oracle(
            "heap",
            &OracleInput::bits(&[]),
            Budget {
                steps: 100,
                heap: 1,
                stack: 0,
                depth: 0,
            },
        )
        .unwrap();
    assert_eq!(r.code, 2);
    assert!(o
        .run_oracle(
            "heap",
            &OracleInput::bits(&[]),
            Budget {
                steps: 100,
                heap: 33,
                stack: 0,
                depth: 0
            }
        )
        .is_err());
}

#[test]
fn nested_oracles_xor_targets_and_faults_with_explicit_propagation() {
    let o = Object::parse(include_str!("fixtures/nested.bisa")).unwrap();
    for b in [0, 2, 3, 4] {
        let mut input = OracleInput::bits(&[255]);
        input.args.push(Argument::Token(Budget::steps(b)));
        for (name, expected) in [
            ("nested", if b >= 3 { (0, 0) } else { (0, 9) }),
            ("cancel", (0, 0)),
            ("ignore", (0, 0)),
        ] {
            let r = o.run_oracle(name, &input, Budget::steps(20)).unwrap();
            assert_eq!((r.payload, r.code), expected, "{name},B={b}");
        }
        input.ins[0] = 8;
        let r = o.run_oracle("nested", &input, Budget::steps(20)).unwrap();
        assert_eq!((r.payload, r.code), if b >= 3 { (9, 0) } else { (0, 9) });
    }
}

#[test]
#[ignore = "full 8-bit arithmetic sweep"]
fn exhaustive_unsigned_and_signed_division_u8() {
    let o = Object::parse(include_str!("fixtures/arithmetic.bisa")).unwrap();
    for a in 0..=255u128 {
        for b in 0..=255u128 {
            for name in ["udiv", "urem", "sdiv", "srem"] {
                let r = o
                    .run_oracle(name, &OracleInput::bits(&[a, b]), Budget::steps(2))
                    .unwrap();
                let overflow = name.starts_with('s') && a == 128 && b == 255;
                if b == 0 || overflow {
                    assert_eq!((r.payload, r.code), (0, if b == 0 { 5 } else { 6 }));
                } else {
                    let sa = a as u8 as i8 as i16;
                    let sb = b as u8 as i8 as i16;
                    let expected = match name {
                        "udiv" => a / b,
                        "urem" => a % b,
                        "sdiv" => (sa / sb) as u8 as u128,
                        _ => (sa % sb) as u8 as u128,
                    };
                    assert_eq!((r.payload, r.code), (expected, 0), "{name}({a},{b})");
                }
            }
        }
    }
}
````

## `tests/parser.rs` (126 lines)

````rust
use bennett_isa_ref::{json::Json, Object};

const INC: &str = include_str!("fixtures/inc8.bisa");
const SUM: &str = include_str!("fixtures/sum_db.bisa");

fn rejects(text: &str, rule: &str) {
    let error = Object::parse(text).expect_err("ill-formed object accepted");
    assert!(error.to_string().contains(rule), "{error} must cite {rule}");
}

#[test]
fn published_objects_parse() {
    let inc = Object::parse(INC).unwrap();
    assert_eq!(inc.ptr_width, 32);
    assert_eq!(inc.functions["inc8"].blocks[0].instructions.len(), 3);
    let sum = Object::parse(SUM).unwrap();
    assert_eq!(sum.functions["sum"].locations().len(), 13);
    assert_eq!(sum.functions["sum"].frame_cells(), 16);
}

#[test]
fn lexical_and_section_errors_cite_rules() {
    for text in [
        INC.replace('\n', "\r\n"),
        INC.replace("lift.add x", "lift.add  x"),
        INC.replace("lift.add x one", "lift.add x one "),
        INC.replace("\n\nsection", "\nsection"),
        INC.replace("^entry():", "\n^entry():"),
    ] {
        rejects(&text, "§16.1");
    }
    rejects(&INC.replace("isa=0.8", "isa=0.9"), "§1");
    rejects(&INC.replace("section symbols", "section unknown"), "§9.1");
    rejects(&format!("{INC}\nsection symbols\n{{}}\n"), "§9.1");
    rejects(&INC.replace("{\"0\":", "{ \"0\":"), "§16.1");
}

#[test]
fn names_widths_opcodes_and_terminators_are_checked() {
    rejects(
        &INC.replace("lift.add x one", "lift.add missing one"),
        "§3.7",
    );
    rejects(&INC.replace("r = lift.add", "x = lift.add"), "§3.7");
    rejects(&INC.replace("r:reg[8]", "r:reg[7]"), "§3.3");
    rejects(
        &INC.replace("one = lift.const.i8 1", "one = lift.magic x"),
        "§4.8",
    );
    rejects(&INC.replace("lift.retval r", "r = lift.mov one"), "§3.6");
    rejects(&INC.replace("lift.retval r", "lift.ret r"), "§4.2");
    rejects(&INC.replace("lift.retval r", "qjump ^missing"), "§3.6");
    rejects(&INC.replace("lift.retval r", "fault 16"), "§3.3");
    rejects(
        &SUM.replace("idx = lift.zext.i32 n2", "idx = lift.trunc.i32 n2"),
        "§3.3",
    );
    rejects(
        &SUM.replace(
            "lift.call @sum (n, acc, base)",
            "lift.call @sum (base, acc, n)",
        ),
        "§3.3",
    );
    rejects(
        &SUM.replace("zp = lift.addr @zero", "zp = lift.addr @db"),
        "§4.2",
    );
    rejects(&SUM.replace("\"base\":4096", "\"base\":16"), "§7.2");
    rejects(&SUM.replace("\"size\":1", "\"size\":2"), "§7.2");
}

#[test]
fn json_is_strict_and_canonical() {
    let raw = r#"{"a":[null,true,false,"\n",-1,1e+30],"z":"é"}"#;
    assert_eq!(Json::parse(raw).unwrap().canonical(), raw);
    for bad in [
        "{\"a\":1,\"a\":2}",
        "[01]",
        "[1.]",
        "[NaN]",
        "[1e999]",
        "\"\u{0001}\"",
        "\"\\ud800\"",
    ] {
        assert!(Json::parse(bad).is_err(), "accepted {bad}");
    }
    assert_eq!(
        Json::parse("[-0,1e-7,1e-6,1e20,1e21]").unwrap().canonical(),
        "[0,1e-7,0.000001,100000000000000000000,1e+21]"
    );
    // RFC 8785 sorts object keys by UTF-16 units: a supplementary character
    // sorts before U+E000, despite its larger Unicode scalar value.
    assert_eq!(
        Json::parse("{\"\u{e000}\":0,\"😀\":1}")
            .unwrap()
            .canonical(),
        "{\"😀\":1,\"\u{e000}\":0}"
    );
}

#[test]
fn empty_hex_data_and_canonical_type_widths() {
    let data=format!("bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=32\n\nsection symbols\n{{\"0\":{{\"interface_hash\":\"{}\",\"kind\":\"data\",\"name\":\"empty\",\"signature\":{{\"abi\":\"0.8\",\"kind\":\"data\",\"size\":0,\"tier\":\"-\"}}}}}}\n\nsection data\nempty \n","0".repeat(64));
    assert!(Object::parse(&data).unwrap().data["empty"].is_empty());
    rejects(&INC.replace("reg[8]", "reg[08]"), "§3.3");
}

#[test]
fn label_width_uses_reachable_closure_not_unrelated_functions() {
    let raw = include_str!("fixtures/arithmetic.bisa");
    let narrow = raw.replace(
        "z:reg[8], p:reg[1], idx:reg[32], r:reg[8]",
        "z:reg[8], p:reg[1], idx:reg[4], r:reg[8]",
    );
    // jump has ten rows, so 2^4 > 10, regardless of other independent oracles.
    let object = Object::parse(&narrow).unwrap();
    let result = object
        .run_oracle(
            "jump",
            &bennett_isa_ref::OracleInput::bits(&[0, 0]),
            bennett_isa_ref::Budget::steps(10),
        )
        .unwrap();
    assert_eq!((result.payload, result.code), (42, 0));
}
````

## `tests/quantum.rs` (131 lines)

````rust
use bennett_isa_ref::{Complex, Object, QuantumBindings, QuantumState};

fn close(a: Complex, b: Complex) {
    assert!(
        (a.re - b.re).abs() < 1e-12 && (a.im - b.im).abs() < 1e-12,
        "{a:?} != {b:?}"
    );
}
#[test]
fn bell_state_born_branches_and_adjoint() {
    let mut q = QuantumState::new();
    let wires = q.allocate(2).unwrap();
    q.gate("h", &[wires[0]], None, &[]).unwrap();
    q.gate("cx", &wires, None, &[]).unwrap();
    let a = q.amplitudes().unwrap();
    let h = std::f64::consts::FRAC_1_SQRT_2;
    close(a[0], Complex::new(h, 0.0));
    close(a[3], Complex::new(h, 0.0));
    close(a[1], Complex::ZERO);
    close(a[2], Complex::ZERO);
    let branches = q.measurement_branches(&wires).unwrap();
    assert_eq!(branches.len(), 2);
    for b in branches {
        assert!((b.probability - 0.5).abs() < 1e-12);
        assert_eq!(b.bits[0], b.bits[1]);
        assert_eq!(b.state.wire_count(), 0);
    }
    q.gate("cx", &wires, None, &[]).unwrap();
    q.gate("h", &[wires[0]], None, &[]).unwrap();
    q.release(&wires).unwrap();
    assert_eq!(q.wire_count(), 0);
}
#[test]
fn every_gate_and_controlled_global_phase() {
    for (op, n, angle, inverse) in [
        ("x", 1, None, "x"),
        ("h", 1, None, "h"),
        ("s", 1, None, "sdg"),
        ("t", 1, None, "tdg"),
        ("rx", 1, Some(0.7), "rx"),
        ("ry", 1, Some(-0.2), "ry"),
        ("rz", 1, Some(1.1), "rz"),
        ("cx", 2, None, "cx"),
        ("ccx", 3, None, "ccx"),
        ("swap", 2, None, "swap"),
        ("cz", 2, None, "cz"),
    ] {
        let mut q = QuantumState::new();
        let w = q.allocate(n + 1).unwrap();
        for wire in &w {
            q.gate("h", &[*wire], None, &[]).unwrap();
        }
        let before = q.amplitudes().unwrap();
        q.gate(op, &w[..n], angle, &[w[n]]).unwrap();
        q.gate(inverse, &w[..n], angle.map(|x| -x), &[w[n]])
            .unwrap();
        for (a, b) in q.amplitudes().unwrap().into_iter().zip(before) {
            close(a, b);
        }
    }
    // Controlled Rz(2*pi) is -I on its enabled subspace; global phase matters.
    let mut q = QuantumState::new();
    let w = q.allocate(2).unwrap();
    q.gate("h", &[w[0]], None, &[]).unwrap();
    q.gate("rz", &[w[1]], Some(std::f64::consts::TAU), &[w[0]])
        .unwrap();
    q.gate("h", &[w[0]], None, &[]).unwrap();
    close(q.amplitudes().unwrap()[1], Complex::new(1.0, 0.0));
}
#[test]
fn permutation_fast_path_and_clean_release() {
    let mut q = QuantumState::new();
    let w = q.allocate(100).unwrap();
    q.gate("x", &[w[99]], None, &[]).unwrap();
    q.gate("mcx", &[w[99], w[3]], None, &[]).unwrap();
    assert!(q.is_basis());
    assert_eq!(q.read_basis(&[w[3]]).unwrap(), 1);
    assert!(q.release(&w).is_err());
    q.gate("mcx", &[w[99], w[3]], None, &[]).unwrap();
    q.gate("x", &[w[99]], None, &[]).unwrap();
    q.release(&w).unwrap();
}
#[test]
fn actions_copy_cleanup_quantum_memory_loops_and_adjoint() {
    let o = Object::parse(include_str!("fixtures/actions.bisa")).unwrap();
    for name in ["flip", "memory", "loop", "bell"] {
        let mut q = QuantumState::new();
        let t = q.allocate(2).unwrap();
        let p = q.allocate(2).unwrap();
        q.gate("x", &[p[0]], None, &[]).unwrap();
        let mut b = QuantumBindings::default();
        b.bundles.insert("t".into(), t.clone());
        b.bundles.insert("p".into(), p.clone());
        let before = q.amplitudes().unwrap();
        o.execute_action(name, &mut q, &b, false, &[]).unwrap();
        o.execute_action(name, &mut q, &b, true, &[]).unwrap();
        for (a, b) in q.amplitudes().unwrap().into_iter().zip(before) {
            close(a, b);
        }
    }
}

#[test]
fn lifted_permutation_calls_use_the_action_and_its_adjoint() {
    use bennett_isa_ref::{Budget, OracleInput, OracleMachine};
    let o = Object::parse(include_str!("fixtures/actions.bisa")).unwrap();
    for x in 0..4 {
        let input = OracleInput::bits(&[x]);
        let budget = Budget::steps(5);
        let result = o.run_oracle("lifted", &input, budget).unwrap();
        assert_eq!((result.payload, result.code), (x ^ 1, 0));
        let mut m = OracleMachine::new(&o, "lifted", &input, budget).unwrap();
        let before = m.snapshot();
        for _ in 0..5 {
            m.forward_step().unwrap();
        }
        assert_eq!(m.outcome(), result);
        for _ in 0..5 {
            m.inverse_step().unwrap();
        }
        assert_eq!(m.snapshot(), before);
    }
}

#[test]
fn wide_structured_bundles_are_not_limited_to_integer_widths(){
    let signature=r#"{"abi":"0.8","args":[],"bounds":[],"in":[256],"kind":"perm_action","mem":[],"mut":[256],"tier":"q"}"#;
    let text=format!("bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=32\n\nsection symbols\n{{\"0\":{{\"interface_hash\":\"{}\",\"kind\":\"perm_action\",\"name\":\"wide\",\"signature\":{signature}}}}}\n\nsection functions\nperm_action @wide (t:wire[256] mut) (p:wire[256] in) () () ()\n^entry():\nd = qcopy p\nqxor d t\nquncopy p d\n","0".repeat(64));
    let object=Object::parse(&text).unwrap();let mut q=QuantumState::new();let t=q.allocate(256).unwrap();let p=q.allocate(256).unwrap();q.gate("x",&[p[255]],None,&[]).unwrap();let mut b=QuantumBindings::default();b.bundles.insert("t".into(),t.clone());b.bundles.insert("p".into(),p);
    object.execute_action("wide",&mut q,&b,false,&[]).unwrap();assert_eq!(q.read_basis(&[t[0],t[128],t[255]]).unwrap(),4);assert_eq!(q.wire_count(),512);object.execute_action("wide",&mut q,&b,true,&[]).unwrap();assert_eq!(q.read_basis(&[t[255]]).unwrap(),0);
}
````

## `tests/registers.rs` (122 lines)

````rust
mod support;
use bennett_isa_ref::{ClassicalMachine, ClassicalValue, Object, QuantumRegisters};
use support::{object, rehash};
fn program() -> Object {
    Object::parse(include_str!("fixtures/registers.bisa")).unwrap()
}

#[test]
fn register_handles_enforce_views_consumption_and_cleanliness() {
    let mut r = QuantumRegisters::new();
    let q = r.allocate(2).unwrap();
    let s = r.slice(q, 0, 1).unwrap();
    assert!(r.bundle(q).is_err());
    assert!(r.free(s).is_err());
    assert!(r.slice(s, 0, 1).is_err());
    r.complete_call(&[s]).unwrap();
    assert!(r.bundle(s).is_err());
    assert_eq!(r.bundle(q).unwrap().len(), 2);
    let b = r.allocate(1).unwrap();
    let joined = r.concat(q, b).unwrap();
    assert!(r.bundle(q).is_err());
    assert!(r.bundle(b).is_err());
    assert_eq!(r.bundle(joined).unwrap().len(), 3);
    r.free(joined).unwrap();
    assert!(r.bundle(joined).is_err());
}
#[test]
fn allocation_views_and_region_calls_reverse_with_their_frames() {
    let p = program();
    for name in ["allocation", "views"] {
        let mut m = ClassicalMachine::new(&p, name, &[], &[]).unwrap();
        let before = m.snapshot();
        assert_eq!(m.run(100).unwrap().fault, None);
        m.reverse().unwrap();
        assert_eq!(m.snapshot(), before, "{name}");
    }
    let mut m = ClassicalMachine::new(&p, "unclean", &[], &[]).unwrap();
    let before = m.snapshot();
    assert_eq!(m.run(100).unwrap().fault, Some(4));
    m.reverse().unwrap();
    assert_eq!(m.snapshot(), before);
}
#[test]
fn measurement_uses_born_branches_and_prevents_uncall_and_reversal() {
    let p = program();
    for (draw, expected) in [(0.1, 0), (0.9, 3)] {
        let mut m = ClassicalMachine::new(&p, "measurement", &[], &[]).unwrap();
        m.push_measurement_draw(draw).unwrap();
        let r = m.run(100).unwrap();
        assert_eq!(r.values, vec![ClassicalValue::int(2, expected).unwrap()]);
        assert!(m.reverse().is_err());
    }
    let mut m = ClassicalMachine::new(&p, "bad_uncall", &[], &[]).unwrap();
    m.push_measurement_draw(0.1).unwrap();
    assert_eq!(m.run(100).unwrap().fault, Some(4));
    assert!(m.reverse().is_err());
}

#[test]
fn viewed_parent_and_view_only_one_call_are_static_errors() {
    let p = program();
    for replacement in [
        "qreg.free q\naction_call @toggle (s) () () ()",
        "qreg.free s\naction_call @toggle (s) () () ()",
        "action_call @toggle (s) () () ()\naction_call @toggle (s) () () ()",
    ] {
        let bad = p
            .text
            .replacen("action_call @toggle (s) () () ()", replacement, 1);
        let error = Object::parse(&bad).expect_err("invalid qreg view lifetime accepted");
        assert!(error.to_string().contains("§3.3"), "{error}");
    }
}

#[test]
fn external_register_binding_oracle_xor_and_history_inverse() {
    use bennett_isa_ref::Budget;
    let inc = Object::parse(include_str!("fixtures/inc8.bisa")).unwrap();
    let sig = r#"{"abi":"0.8","kind":"cc","params":["qreg[8]","qreg[8]","qreg[4]","token"],"results":[],"tier":"cc"}"#;
    let imports = format!(
        "{{\"inc8\":{{\"signature\":{}}}}}",
        inc.symbols().unwrap()["0"]
            .get("signature")
            .unwrap()
            .canonical()
    );
    let caller=rehash(&object(&[("invoke",sig,"fn cc @invoke (x:qreg[8], t:qreg[8], f:qreg[4], tk:token) () () () ()\n^entry():\noracle_call @inc8 tk (x) t f () ()\nret")],&imports,""));
    let p = Object::link(&[caller, inc]).unwrap();
    for steps in [2, 3] {
        let mut regs = QuantumRegisters::new();
        let x = regs.allocate(8).unwrap();
        let t = regs.allocate(8).unwrap();
        let f = regs.allocate(4).unwrap();
        regs.prepare(x, &[true, true, true, false, false, false, false, false])
            .unwrap();
        regs.prepare(t, &[true, true, true, true, true, false, false, false])
            .unwrap();
        regs.prepare(f, &[true, true, false, false]).unwrap();
        assert!(regs.prepare(x, &[false; 8]).is_err());
        let args = [
            ClassicalValue::Qreg(x),
            ClassicalValue::Qreg(t),
            ClassicalValue::Qreg(f),
            ClassicalValue::Token(Budget::steps(steps)),
        ];
        let mut m =
            ClassicalMachine::with_quantum_registers(&p, "invoke", &args, &[], regs).unwrap();
        let before = m.snapshot();
        m.run(100).unwrap();
        let r = m.quantum_registers();
        assert_eq!(
            r.quantum_state().read_basis(r.bundle(t).unwrap()).unwrap(),
            if steps == 3 { 31 ^ 8 } else { 31 }
        );
        assert_eq!(
            r.quantum_state().read_basis(r.bundle(f).unwrap()).unwrap(),
            if steps == 3 { 3 } else { 2 }
        );
        m.reverse().unwrap();
        assert_eq!(m.snapshot(), before);
    }
}
````

## `tests/step_machine.rs` (134 lines)

````rust
use bennett_isa_ref::{Budget, Object, OracleInput, OracleMachine};

fn compare(o: &Object, name: &str, input: &OracleInput, budget: Budget) {
    let expected = o.run_oracle(name, input, budget).unwrap();
    let mut m = OracleMachine::new(o, name, input, budget).unwrap();
    let initial = m.snapshot();
    for _ in 0..budget.steps {
        m.forward_step().unwrap();
    }
    assert_eq!(m.outcome(), expected, "{name}:B={}", budget.steps);
    for _ in 0..budget.steps {
        m.inverse_step().unwrap();
    }
    assert_eq!(m.snapshot(), initial, "{name}: prefix reversal");
    assert!(m.frames_clean());
}

#[test]
fn inc8_every_input_and_budget_cutoff_including_idle_halt() {
    let o = Object::parse(include_str!("fixtures/inc8.bisa")).unwrap();
    for x in 0..256 {
        for b in 0..=5 {
            compare(&o, "inc8", &OracleInput::bits(&[x]), Budget::steps(b));
        }
    }
}
#[test]
fn arithmetic_parallel_assignment_control_and_every_fault() {
    let o = Object::parse(include_str!("fixtures/arithmetic.bisa")).unwrap();
    for name in o.functions.keys() {
        for a in [0, 1, 2, 127, 128, 255] {
            for b in [0, 1, 2, 8, 128, 255] {
                for steps in 0..=4 {
                    compare(&o, name, &OracleInput::bits(&[a, b]), Budget::steps(steps));
                }
            }
        }
    }
}
#[test]
fn heap_cells_and_allocation_table_restore_on_success_and_faults() {
    let o = Object::parse(include_str!("fixtures/heap.bisa")).unwrap();
    for name in o.functions.keys() {
        for heap in [0, 1, 2, 32] {
            for steps in 0..=10 {
                compare(
                    &o,
                    name,
                    &OracleInput::bits(&[]),
                    Budget {
                        steps,
                        heap,
                        stack: 0,
                        depth: 0,
                    },
                );
            }
        }
    }
}
#[test]
fn recursive_call_and_ret_each_invert_the_complete_pre_step_tuple() {
    let o = Object::parse(include_str!("fixtures/sum_db.bisa")).unwrap();
    let mut input = OracleInput::bits(&[2]);
    input.regions.insert("db".into(), (1..=16).collect());
    let budget = Budget {
        steps: 40,
        heap: 4080,
        stack: 512,
        depth: 64,
    };
    let mut m = OracleMachine::new(&o, "sum_db", &input, budget).unwrap();
    for _ in 0..budget.steps {
        let before = m.snapshot();
        m.forward_step().unwrap();
        let after = m.snapshot();
        m.inverse_step().unwrap();
        assert_eq!(m.snapshot(), before);
        m.forward_step().unwrap();
        assert_eq!(m.snapshot(), after);
    }
    for stack in [0, 15, 16, 47, 48, 512] {
        for depth in [0, 1, 2, 3] {
            compare(
                &o,
                "sum_db",
                &input,
                Budget {
                    stack,
                    depth,
                    ..budget
                },
            );
        }
    }
}
#[test]
#[ignore = "all prefixes of recursive sum for each 8-bit n"]
fn exhaustive_recursive_prefixes() {
    let o = Object::parse(include_str!("fixtures/sum_db.bisa")).unwrap();
    for n in 0..=255 {
        let mut input = OracleInput::bits(&[n]);
        input.regions.insert("db".into(), (1..=16).collect());
        let stop = if n <= 16 { 14 * n as u64 + 11 } else { 14 };
        for steps in 0..=stop {
            compare(
                &o,
                "sum_db",
                &input,
                Budget {
                    steps,
                    heap: 4080,
                    stack: 512,
                    depth: 64,
                },
            );
        }
    }
}

#[test]
fn full_small_domain_includes_memory_and_nonzero_target_and_fault(){
    let o=Object::parse(include_str!("fixtures/tiny_memory.bisa")).unwrap();let mut covered=0;
    for x in 0..=1{for byte in 0..=255u128{for steps in 0..=9{
        let mut input=OracleInput::bits(&[x]);input.regions.insert("db".into(),vec![byte as u8]);let budget=Budget::steps(steps);
        let expected=if x==0&&steps>=4{(0,5)}else if x==1&&steps>=8{(byte&1,0)}else{(0,1)};
        let result=o.run_oracle("tiny",&input,budget).unwrap();assert_eq!((result.payload,result.code),expected);
        let mut machine=OracleMachine::new(&o,"tiny",&input,budget).unwrap();let initial=machine.snapshot();for _ in 0..steps{machine.forward_step().unwrap();}
        assert_eq!(machine.outcome(),result);
        for target in 0..=1{for fault in 0..16{assert_eq!(machine.commit(target,fault).unwrap(),(target^expected.0,fault^expected.1));covered+=1;}}
        for _ in 0..steps{machine.inverse_step().unwrap();}assert_eq!(machine.snapshot(),initial);assert!(machine.frames_clean());
    }}}
    assert_eq!(covered,10*(1<<14));
}
````

## `tests/structured.rs` (77 lines)

````rust
use bennett_isa_ref::Object;

fn action(kind: &str, body: &str, bounds: &str) -> String {
    let signature = format!(
        r#"{{"abi":"0.8","args":[],"bounds":[{bounds}],"in":[1],"kind":"{kind}","mem":[],"mut":[1],"tier":"q"}}"#
    );
    let regs = if bounds.is_empty() {
        String::new()
    } else {
        format!("regs {{  }} bounds {{{bounds}}}\n")
    };
    format!("bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=32\n\nsection symbols\n{{\"0\":{{\"interface_hash\":\"{}\",\"kind\":\"{kind}\",\"name\":\"a\",\"signature\":{signature}}}}}\n\nsection functions\n{kind} @a (t:wire mut) (p:wire in) () () ()\n{regs}^entry():\n{body}\n","0".repeat(64))
}
fn bad(text: &str, rule: &str) {
    let e = Object::parse(text).expect_err("invalid action accepted");
    assert!(e.to_string().contains(rule), "{e} must cite {rule}");
}

#[test]
fn nested_structured_code_and_bounds_parse() {
    let s = action("action", "qloop 3 {\nqif p {\nx t\n} {\nh t\n}\n}", "3");
    let o = Object::parse(&s).unwrap();
    let i = &o.functions["a"].blocks[0].instructions[0];
    assert_eq!(i.bodies[0][0].bodies.len(), 2);
    bad(&s.replace("qloop 3", "qloop 4"), "§5.3");
    bad(&action("action", "qloop 3 {\nx t\n}", ""), "§5.3");
}
#[test]
fn tier_arity_aliasing_and_input_roles() {
    bad(&action("action", "mystery t", ""), "§4.8");
    bad(&action("action", "x t p", ""), "§4.8");
    bad(&action("action", "x absent", ""), "§3.3");
    bad(&action("action", "cx t t", ""), "§3.3");
    bad(&action("action", "qpred p\nx p\nqunpred p", ""), "§3.3");
    bad(&action("action", "qpred t\ncx p t\nqunpred t", ""), "§3.3");
    bad(&action("action", "x p", ""), "§5.1");
    bad(&action("perm_action", "h t", ""), "§5.3");
    bad(&action("action", "qpred p\nx t", ""), "§3.5");
    bad(&action("action", "qpred p\nx t\nqunpred t", ""), "§3.5");
    bad(&action("action", "r = measure t", ""), "§5.1");
}
#[test]
fn cleanup_windows_and_linear_lifetimes() {
    Object::parse(&action("action", "d = qcopy p\nz d\nquncopy p d", "").replace("z d", "s d"))
        .unwrap();
    bad(
        &action("action", "d = qcopy t\nh t\nquncopy t d", ""),
        "§6.2",
    );
    bad(
        &action("action", "d = qcopy t\nx t\nquncopy t d", ""),
        "§6.2",
    );
    Object::parse(&action("action", "d = qcopy t\nx t\nx t\nquncopy t d", "")).unwrap();
    bad(&action("action", "d = qcopy t", ""), "§5.1");
    bad(&action("action", "d = qcopy t\nquncopy p d", ""), "§6.2");
    bad(
        &action("action", "d = qalloc any 1\nqfree d\nx d", ""),
        "§3.3",
    );
}
#[test]
fn metadata_unknown_fields_are_errors() {
    let inc = include_str!("fixtures/inc8.bisa");
    bad(
        &format!("{inc}\nsection coverage\n{{\"entries\":[],\"extra\":0}}\n"),
        "§9.1",
    );
    bad(
        &format!("{inc}\nsection devices\n{{\"models\":{{}},\"services\":{{}},\"unknown\":0}}\n"),
        "§9.1",
    );
    bad(
        &format!("{inc}\nsection schedule\n{{\"unknown\":0}}\n"),
        "§9.1",
    );
}
````

## `tests/support/mod.rs` (55 lines)

````rust
#![allow(dead_code)]
use bennett_isa_ref::{json::Json, Object};
use std::collections::BTreeMap;

pub fn json(s: &str) -> Json {
    Json::parse(s).unwrap()
}
pub fn object(functions: &[(&str, &str, &str)], imports: &str, extra: &str) -> String {
    let symbols = functions
        .iter()
        .enumerate()
        .map(|(i, (name, signature, _))| {
            let sig = json(signature);
            let value = Json::Object(BTreeMap::from([
                ("name".into(), Json::String((*name).into())),
                ("kind".into(), sig.get("kind").unwrap().clone()),
                ("signature".into(), sig),
                ("interface_hash".into(), Json::String("0".repeat(64))),
            ]));
            (i.to_string(), value)
        })
        .collect();
    let mut text=format!("bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width=32\n\nsection symbols\n{}\n",Json::Object(symbols).canonical());
    if imports != "{}" {
        text.push_str(&format!(
            "\nsection imports\n{}\n",
            json(imports).canonical()
        ));
    }
    text.push_str("\nsection functions\n");
    for (_, _, body) in functions {
        text.push_str(body.trim_end_matches('\n'));
        text.push('\n');
    }
    text.push_str(extra);
    text
}
pub fn rehash(text: &str) -> Object {
    let parsed = Object::parse(text).unwrap();
    let hashes = parsed.identity().unwrap().interface_hashes;
    let mut lines: Vec<_> = text.lines().map(str::to_string).collect();
    let i = lines.iter().position(|s| s == "section symbols").unwrap() + 1;
    let Json::Object(mut symbols) = json(&lines[i]) else {
        unreachable!()
    };
    for symbol in symbols.values_mut() {
        let name = symbol.get("name").unwrap().string().unwrap().to_string();
        let Json::Object(value) = symbol else {
            unreachable!()
        };
        value.insert("interface_hash".into(), Json::String(hashes[&name].clone()));
    }
    lines[i] = Json::Object(symbols).canonical();
    Object::parse(&(lines.join("\n") + "\n")).unwrap()
}
````
