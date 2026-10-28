# North-star amendment A1 — control flow under a qubit: one budget, no per-construct bounds

**Status:** draft for council review, 2026-10-28. Amends `docs/Bennett-NorthStar.md`
iteration 7 (council consensus, round 6). Proposed as iteration 8; to be graded as
`northstar-2026-10-28` round 7 with this file's changes applied surgically and the diff
attached by the runner. Nothing is implemented; the amendment changes only §7 (landscape)
and adds one sentence to §4.2 and one clause to "What is new".

**Why now.** The ISA (draft 0.8, accepted) made concrete what §4.2 states abstractly: a
lifted oracle runs under **one** classical step budget B per region call (ISA §3.6, §5.4),
and nested data-dependent loops and recursion draw on it jointly, with no bound attached to
any loop or call site. The maintainer's experience with Bennett.jl v1, whose circuit lowering
unrolled every loop and therefore demanded a bound per loop, nested bounds multiplying, is
the problem this solves; it is also the reason the quantum programming literature has
treated unbounded nested loops under a qubit as out of scope. Codex's round-5 request
(handoff item 6) was that §7 carry a **sourced** comparison instead of categorical negatives.
This amendment supplies that for the one axis where the project's claim is sharpest.

## A1.1 The claim, stated narrowly

Under a qubit, a program with arbitrary nested data-dependent loops and recursion is run as
one circuit whose length is a single run-level budget B, chosen per call at launch from
classical data, with the three classical resource limits (heap bytes, stack cells, recursion
depth) chosen the same way; no construct in the program carries a bound of its own; overrun
of any of the four is a named fault outcome in the result on exactly the affected branches,
and every ancilla returns to zero on every branch. Each ingredient is old (sources below);
their combination as a toolchain that accepts unmodified LLVM programs is what is new.

## A1.2 Sourced comparison (new sub-table for §7)

Insert after the main table of §7, before "**What is new**":

> **Control flow under a qubit, specifically.** The one axis on which the systems above
> differ most from Bennett is how a data-dependent loop or a recursive call behaves when the
> data is a qubit. The table names, for each, where the bound lives and what happens when
> it is exceeded.
>
> | Source | Data-dependent loops / recursion under superposition | Where the bound lives | On overrun | Relation to Bennett |
> |---|---|---|---|---|
> | Bennett, *Logical reversibility of computation*, IBM J. Res. Dev. 17 (1973) 525–532 | A reversible machine simulates an arbitrary (irreversible) machine for a fixed number of steps T, keeping a history and erasing it by running backwards. | One T for the whole run. | Not addressed (classical; the simulation is simply run longer). | **Taken whole.** The lifted oracle (ISA §5.2) is this simulation made uniform over a superposed input, plus a fault outcome and a final uncompute. |
> | Bennett, *Time/space trade-offs for reversible computation*, SIAM J. Comput. 18 (1989) 766–776; Knill, *An analysis of Bennett's pebble game*, 1995 (quant-ph/9508006) | Same model; the T-step history replaced by O(log T) checkpoints at polylogarithmic time cost. | One T. | — | Taken as run-time policy (§4.3, §9 item 8); ISA open item I1 admits pebbled realisations under the schedule. |
> | Bernstein and Vazirani, *Quantum complexity theory*, SIAM J. Comput. 26 (1997) 1411–1473; Myers, *Can a universal quantum computer be fully quantum?*, Phys. Rev. Lett. 78 (1997) | A universal quantum Turing machine simulates another for a number of steps given as input; branches that would halt at different times are the known obstruction ("the halting problem for QTMs"). | One step count, supplied classically. | Simulation stops at the count; the answer of unfinished branches is undefined. | The same obstruction, met the same way: the count is classical and per run. Bennett adds the defined fault outcome and the clean workspace on unfinished branches. |
> | Knill, *Conventions for quantum pseudocode*, LANL LAUR-96-2724 (1996); Quil / QAM; OpenQASM 3 | Loops are classical: the controller iterates, the quantum data does not decide termination. | In the classical controller, per loop. | Classical. | Bennett's CC and R tiers are this discipline; the Q tier is what these machines do not have. |
> | Quipper, PLDI 2013; Q#; Qiskit classical-function compiler; REVS; tweedledum/RevKit; Bennett.jl v1 (`src/lowering/cfg.jl`) | Classical code becomes a circuit by generation time: every loop is unrolled, so every loop needs a trip-count bound and nested loops multiply them; data-dependent termination under a qubit is unsupported or padded by hand. | Per loop, at compile time, supplied or inferred per construct. | Compile error or a hand-written guard. | **The regime Bennett replaces.** The circuit is the right *output* of the specialiser (§4.4) and the wrong *programming model*. |
> | Yuan and Carbin, *Tower: data structures in quantum superposition*, OOPSLA 2022 (arXiv:2205.10255) | Recursion over superposed data structures is allowed, with every recursion bounded by a classical parameter in the type system, which the authors argue is necessary to run on a quantum computer. | Per recursive definition, in the type. | Type error. | The necessity argument is the same (one circuit); Bennett moves the bound from each definition to the run: one B and one `depth_limit` for the whole region (ISA §5.4). |
> | Yuan, Villanyi and Carbin, *Quantum control machine: the limits of control flow in quantum programming*, OOPSLA 2024 (arXiv:2304.15000) | A superposed program counter with a restricted conditional jump; necessary and sufficient conditions (injectivity of transitions, synchronisation at join and exit) for control flow to be realisable; a naive lift of the classical jump is shown unsound. | Programs must synchronise; iteration is padded to a bound. | — | **Taken as the correctness conditions** the step machine satisfies (§4.2: predecessor recorded per step, common halt counter at exit). Bennett's step machine is the general-case realisation for arbitrary post-O3 CFGs, under one budget, with fault register and uncompute. |
> | Silq, PLDI 2020; Unqomp, PLDI 2021; Reqomp | Automatic uncomputation under a `qfree`/`const` discipline; control flow under a qubit is structured and bounded. | Per construct. | Type error. | The uncomputation-validity invariant is adopted (§4.2); unbounded nested loops under a qubit are outside their scope and inside Bennett's. |
> | Janus (Lutz 1986; Yokoyama and Glück, PEPM 2007) and the reversible-language tradition | Unbounded `while` loops are reversible classically, with entry and exit assertions. | None (classical, per input). | Assertion failure. | The R tier (ISA §3.4, §7.4) is this, with a run history instead of assertions, as BennettVM.jl demonstrated end to end on Collatz (2026, milestone M13). |
> | Ambainis, *Quantum search with variable times*, Theory Comput. Syst. 47 (2010) 786–807 (quant-ph/0609168); Ambainis, Kokainis and Vihrovs, TQC 2023 (arXiv:2302.06749); Jeffery, *Quantum subroutine composition*, 2022 (arXiv:2209.14146); Belovs, Jeffery and Yolcu, *Taming quantum time complexity*, Quantum 8 (2024) 1444 (arXiv:2311.15873); Jeffery, Mamindlapally and Nguetsa Tankeu, *Loop composition in quantum algorithms*, 2026 (arXiv:2605.07518) | Algorithms whose subroutines take different times on different branches: a per-step "done" projector that commutes with the computational basis and that later steps leave invariant; search costs the ℓ2 average √(Σ T_i²) rather than √N·max T_i; the 2026 paper shows that composing with the subroutine as a straight line loses this and composing as a loop recovers it. | An outer algorithm chooses time thresholds classically. | Unfinished branches are flagged, not faulted. | The lifted oracle is their "straight-line" subroutine of length B; the fault register under a ladder of budget tokens is their "done" flag (ISA §4.2, §5.4; note `bennett-isa-spec/docs/notes/2026-10-28-budgets-loops-variable-time.md`). ISA open item I5 makes idle steps exact identities so the oracle is a variable-time subroutine in their sense; loop-aware composition is a future layer (I6). |

## A1.3 Change to "What is new" (§7, last paragraph)

Replace "(d) correctness defined by the permutation theorem …" through "Everything else is
adopted from the systems above with attribution." with:

> (d) correctness defined by the permutation theorem plus channel-comparison oracles,
> attached to linkable objects as certificates that separate proof from evidence; (e) **one
> run-level budget for arbitrary nested data-dependent loops and recursion under a qubit**:
> the programmer and the host supply one step budget and the three classical resource
> limits per region call, never a bound per loop or per recursive definition, and the
> optimiser alone may reintroduce per-construct bounds where it can prove them (§4.2, §4.4);
> overrun is a fault outcome in the result. Every ingredient of (e) is in the sources above
> (Bennett 1973's fixed-T simulation, the QTM halting obstruction, the quantum control
> machine's conditions, Tower's necessity argument); the combination, delivered for
> unmodified programs, is not. Everything else is adopted from the systems above with
> attribution.

## A1.4 One sentence for §4.2

After "**Nothing about the VM makes superposed trip counts observable or cheap; what it
makes possible is choosing the budget at run time from classical data instead of at
compile time.**" insert:

> The budget is one number per region call, counting rows executed on a branch; nested
> loops and recursive calls draw on it jointly, no construct carries a bound of its own, and
> the three classical resource limits (heap, stack, depth) are chosen with it, exactly as a
> classical process runs under one stopwatch and its `ulimit`s. Per-loop bounds, the regime
> of circuit generators (§7), reappear only inside the optimiser where it can prove them.

## A1.5 What the council should check

1. Every source above is real and says what the row says (the editor verified Tower,
   QCM, Ambainis 2010, AKV23, Jef22, BJY24 and the 2026 loop-composition paper against
   their arXiv pages or text on 2026-10-28; Bennett 1973/1989, Bernstein–Vazirani 1997,
   Myers 1997, Knill 1995/1996, Janus and the PLDI papers from the editor's knowledge).
2. The claim in A1.1 does not exceed what the ISA 0.8 provides (§3.6 single step counter,
   §3.7 call/return under `depth_limit` and `stack_limit`, §4.2 `lift.alloc` under
   `heap_limit`, §5.2 fault commit, T2 clean workspace on every branch).
3. The claim is not weakened by the known costs: per-step dispatch over the program (the
   price of not unrolling; specialiser structure recovery recovers it where bounds are
   provable, ISA I2) and B retained frames (pebbling, ISA I1). Both are efficiency
   items; neither changes the programming model.
4. Consistency with §10 (process): this amendment is landscape and precision, not new
   design; the ISA's semantics were accepted first and the vision now cites them.
