# Pebble: a design for the optimising, pebbling circuit compiler (pointer)

Date: 2026-11-10. Status: research input, **not reviewed by council, not on
the manifest, not gated**. Relates to bead `bennett-p2i` ("optimising
specialiser and scheduler", `docs/plan/2026-10-29-path-to-north-star.md`) and to
`bennett-circuits/docs/design/2026-11-09-exporter-redesign.md`, which defers
pebbling.

The work lives in its own repository, outside the workspace process:
**`bennett-quantum/bennett-pebble`** (private), checked out beside the other
repositories as `bennett-pebble/`. Read its `HANDOFF.md` first.

## What it contains

- `docs/DESIGN.md`, `docs/CORE.md`: the compiler design and its formal core.
  Target is the oracle function F_B of ISA 0.9 §5.2/§14.1; per-step history is
  reduced to a small *residue*; history is a pebble game over residues and
  checkpoints under a peak-qubit cap; the circuit is a shared hierarchical
  description that is priced and emitted without being materialised.
- `docs/THEORY.md`: analytic proofs, including twelve corrections to the first
  draft of the core.
- `formal/`: Lean 4 mechanisation, 65 theorems, no `sorry`, no added axioms.
- `model/`: a std-only Rust model (parser, reference interpreter, compiler,
  chain-game solver, exhaustive verification) for the memory-free subset.

## Headline evidence

- Collatz per-step history: 206 bits → 4 bits.
- Collatz at B = 2048, where the current exporter runs out of memory:
  4.9M Toffoli-equivalents at 387k qubits, or 88M at 8.8k qubits.
- Compile time ~0.3 s and ~30 MiB from B = 9 to B = 10⁹.

## What it asks of this workspace

1. Consider the design as the starting point for `bennett-p2i`.
2. ISA feedback for `bennett-isa-spec`: §17 item 18 has to carry in-place
   erasures, which are sound but are not a §6 `reverse`; measurement-based
   cleanup is a plan goal that 0.9 does not admit.
3. The model can serve `bennett-conformance` as a differential oracle for the
   real exporter on small fixtures.

Known gaps (binary-only scheduler in the model, no lifted memory, model source
not line-reviewed) are listed in the handoff's sections 4 and 5.
