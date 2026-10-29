# Implementation rubric — grading a reference implementation against its specification

The rubric the council (`docs/council/README.md`) uses to grade an
**implementation** of a published Bennett contract: first use, the Rust
reference interpreter `bennett-isa-ref` in `bennett-isa-spec/reference-interpreter/`
against `Bennett-ISA-Spec.md` (draft 0.8, accepted). Eight criteria, each scored
1–5 on an absolute scale, plus blocking issues, a path to accept, and verdicts.
Scores are advisory; the maintainer decides.

## What is being graded, and the goal

The specification is settled. The thing under review is code that claims to
**be** the specification's executable meaning: ISA §14.1 says the reference
interpreter *defines* F_B and the budget unit. Every VM, specialiser, checker and
pre-flight tool in the ecosystem will be tested against this crate, so an error
here is invisible to differential testing downstream. The maintainer's goal is
**a crate whose every behaviour can be traced to a sentence of the spec, with
nothing of the spec left out**. The stakes are higher than for the spec text
itself: a spec error is caught by the next reader; an interpreter error becomes
the definition.

The reviewer's job is therefore **adversarial reproduction**, not reading for
plausibility. Derive expected results by hand from the spec text and compare them
with what the code and its fixtures assert. Pick rows, fault paths and corner
cases the tests do not cover and work them through the code. Treat every test's
expected value as a claim to be checked, not as evidence.

## Blocking, S0 and S1, scope

A **blocking** issue is **S0**:

- **Divergence.** On some well-formed object, input and budget, the code's
  result (payload, fault code, step count, final memory, hash, reversal
  outcome, diagnostic class) differs from what the spec text determines.
  One concrete witness is enough; give it (object fragment, input, budget,
  expected, actual or the code path that produces the wrong value).
- **Omission or narrowing.** A row, instruction, fault code, tier, frame
  rule, well-formedness rule, schema field, suite obligation or CLI
  capability the spec defines is missing, stubbed, declared out of scope,
  silently accepted, or implemented for a subset (fixed widths, scalar only,
  "not supported" paths). The job's brief says scope is the whole ISA;
  CLAUDE.md rule 10 forbids narrowing. Disclosed omissions in PROGRESS.md
  are still S0 unless the brief's deliverable list explicitly stages them
  and the staging is recorded there; then they are S1 with the staging as
  the "default".
- **Silent fallback.** Any path that returns a value, guesses, truncates,
  wraps, clamps or continues where the spec says trap, fault or reject
  (CLAUDE.md rule 1: fail fast, fail loud). Any `unwrap`/`expect`/`panic`
  on a path the spec defines as a *reported* outcome.
- **A test that does not test its claim.** A fixture whose hand-derived
  comment is wrong; a test that asserts the implementation's own output;
  an exhaustive sweep that is not exhaustive over the stated domain; an
  "ignored" sweep whose result is not recorded as run.
- **An unjustified reading.** A SPEC-QUESTIONS entry whose chosen reading
  contradicts other spec text, or an ambiguity resolved in the code without
  an entry. (A reading that is defensible and recorded is not S0; say in
  `suggestions` whether the spec should be amended.)
- **Identity.** Any deviation in the §9.2 envelope, SCC ordering, hashing
  input bytes or the published §16.3 hashes.
- **Reversal.** Any state the forward machine touches that the inverse step
  or the §7.4 LIFO reversal does not restore, or restores only in the
  common case.

**S1** issues: structure, naming, performance, duplicated logic, missing
documentation, test organisation, diagnostics wording, CLI ergonomics,
unidiomatic Rust, and spec ambiguities recorded in SPEC-QUESTIONS with a
defensible reading. S1 items are `suggestions`, not blockers.

Every blocking issue is tagged with a **scope**: `core` (parser and
well-formedness, the §14.1 interpreter and every §4.2 row, the §3.6 step
machine and its inverse, CC/R tiers with history, tapes and uncall, Q
semantics and the §6 checks, budgets and faults) or `contract` (identity and
linking, the CLI, JSON output, documentation, test infrastructure).
**Acceptance is staged**: core consensus (every member's `verdict_core` =
accept with no core blocking issue) is the first milestone.

## The standard

A reference interpreter in the sense of the CompCert interpreter, the
WebAssembly reference interpreter, or Sail models of ISAs: code that a
spec reader can hold next to the text and match sentence to function. The
reviewer should be able to name, for any row of §4.2 and any fault code of
§5.4, the function and the test that establish it. Scope is fixed by the
spec and the brief and is not the crate's to trade.

Method required of every member (state in `summary` which you did):

1. Reproduce at least three stated results by hand from the spec text
   before looking at the code's answer: one lifted-oracle result with its
   step count at a tight budget, one fault path (budget, bounds, stack or
   depth), and one identity hash input (the envelope bytes, not necessarily
   the digest).
2. Trace one complete inverse step of the §3.6 machine against the printed
   inverse lists, and one §7.4 segment reversal with a `call`/`ret` pair.
3. Audit every SPEC-QUESTIONS entry against the spec text.
4. Grep the crate for `todo!`, `unimplemented!`, `unwrap(`, `expect(`,
   `panic!`, `unreachable!`, "not supported", "unsupported", "TODO",
   "simplif", "assume", "for now", "approximat", and classify every hit.
5. Compare the list of rows, opcodes, fault codes, frame kinds, schema
   fields and CLI commands in the spec with the ones the code dispatches on.

### Scale

- **5:** every spec sentence has its function and its test; nothing omitted;
  no silent path; hashes reproduced; reversal total; a stranger could use it
  as the oracle for a VM tomorrow.
- **4:** complete in scope with one localised defect a reviewer names at once.
- **3:** the shape is right and most rows are correct, but several
  behaviours diverge or are missing and must be fixed before anything is
  tested against it.
- **2:** a partial interpreter: whole tiers, rows or the reversal are absent.
- **1:** wrong at the core (step relation, budgets or identity).

## Criteria

### C1 Parser and well-formedness
Every §16.2 production and every referenced schema; ill-formed objects
rejected with the rule cited; suite F obligations (§15); no accepted
construct the grammar forbids, no rejected construct it allows.

### C2 Identity and linking
§9.2 envelopes, SCC hashing and ordering, symbol-reference replacement,
SHA-256 against FIPS vectors, the four §16.3 hashes reproduced, §9.3
linking rules, conflicts and dedup.

### C3 The §14.1 interpreter
Every §4.2 row as its classical function, inherent checks, activation
records, `alloctab`, stack accounting, interface regions, globals, nested
oracle calls, every §5.4 fault code and the four budget components;
F_B total (T1) and the step counter as the spec counts it.

### C4 The reversible step machine
§3.6 forward and inverse steps exactly as printed: dispatch, slots, flag,
succ, commit, delivery; the A+D inverse lists; counters at derived widths;
exhaustive equality with C3 and prefix reversal (T2) on every input and
every fault path at the tested widths; the sweeps actually run.

### C5 Classical-control and reversible tiers
§3.4, §4.1, §7.1, §7.3, §7.4: instructions, memory and allocation table,
device models, effect and entropy tapes, run history, dynamic SSA,
`call`/`ret`/`uncall` segment rules and their traps, hostcall, qreg
handles in CC; T4 round trip.

### C6 Q-tier semantics and uncomputation validity
§4.3–§4.7, §5, §6, §14.2: allocation, gates under predication, copy/XOR/
exchange/in-place, quantum memory, region calls, borrowed systems, the
state-vector and permutation paths agreeing, the §6 static checks.

### C7 Tests, fixtures and evidence
Red-green discipline visible; fixtures with hand-derived expectations
that are correct; exhaustive sweeps over the stated domains; every
`isa_check.py` check ported; PROGRESS.md truthful about what is verified
and what is not.

### C8 Fidelity of readings and reporting
SPEC-QUESTIONS entries defensible and complete; no silent choices;
diagnostics cite rules; CLI and README match the code; fail-fast
throughout.

## What the council returns

Per criterion: a score 1–5, evidence pointing at files, functions and
spec sections, the single change that would most raise it. Then
`blocking` (id, section = the spec section and the file/function, scope,
severity S0, problem with its witness, and the concrete fix),
`previous_status`, `regressions`, `suggestions`, `path_to_accept`,
`verdict_core`, `verdict`, `summary` (including which hand reproductions
you did and their results). Consensus is reached when every member
returns `accept` with an empty blocking list.
