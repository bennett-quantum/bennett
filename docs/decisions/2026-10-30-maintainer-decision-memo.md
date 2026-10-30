# Maintainer decision memo — 2026-10-30

Prepared by the orchestrator from `../../bennett-isa-spec/spec/isa-0.9.PROGRESS.md`, draft 0.9 §11.1,
`../../bennett-circuits/docs/design/2026-10-30-m2-open-proofs.md`, the `isa-0.9` beads and
`docs/council/northstar-amendments/A1,A2`. Each item: background, why it is blocked on the maintainer, the
options, a recommendation, and what the choice unblocks. Nothing here narrows north-star scope; every option
listed is a non-narrowing one as recorded by the drafting agents.

## A. ISA 0.9 contract decisions (gate the single 0.9 council dossier)

### A1. ISA-REF-LIB (K11, draft §11.1; beads b-isa-spec-8r4, bennett-vm-47t, b-targets-7dv, bennett-circuits-yz8)

Background. ISA 0.8 §11 says the ISA repository "publishes the reference library `ref`" and that every schedule
binds `{name, version, hash}` of the expansion library it was generated against; §17 item 7 gives only descriptive
defaults (ripple-carry adders, clean scratch released in reverse order). No such document exists, so nothing
that depends on generated ordinals can run: VM scheduled execution and suites E/G, circuits explicit schedules and
§6.4 recompute matching, targets' native inc8 execution. All of them refuse with E_SCHEDULE_INFEASIBLE today.
The 0.9 draft proposes: a JCS JSON catalog (`ref/ref-0.9.json`), a four-line LF envelope whose hash is
SHA-256 over the entire canonical document, recipes in constructor form (gate/alloc/release/classical/for/invoke/
inverse), leaf ordinals numbered per row before any transformation, scratch identity as
(invocation chain, step, expansion path, allocation ordinal, bit), `removable` empty everywhere initially,
deterministic Boolean decomposition (left-to-right postorder, fresh scratch per node, no CSE, bit loops from LSB).

Decision points. (a) The hash rule and schema. (b) The decomposition set: which recipes and which algorithms.

Recommendation. Accept the schema and hash rule as drafted; they adopt §9.2's envelope convention and make any
recipe change a new hash. For the decomposition set, accept the simplest deterministic choice (the §17 defaults
made explicit, no CSE, removable empty). The library is versioned, so an optimised `ref 1.0` can coexist later
without disturbing any 0.9 certificate. The schema and hash rule are the hard-to-change part; the catalog is not.

Consequence. One sol job serialises the catalog in constructor form with witnesses; after 0.9 acceptance the
`ref/` directory is published. Unblocks VM 47t/v23/abx, circuits yz8 and M4 schedules, targets 7dv, conformance
E/G promotion. Cost: 0.9 resource numbers reflect naive decompositions until a later library.

### A2. LAUNCH-ESTIMATE (K12, §10.1/§12.3; beads b-isa-spec-c15, bennett-vm-hsd; bennett-estimate waits on it)

Background. The 0.8 estimate request takes four arguments and no classical parameters; §8/§10 leave the
per-class representation, the decimal precision and the rounding direction unstated. The VM therefore refuses
every estimate rather than guess a basis input or a rounding. Three independent choices:

1. API. Proposal: change the versioned 0.9 request to carry `params_jcs, params_len` (every classical argument
   resolved, `[]` only for none). Alternative: keep the four-argument entry and add a named bound-request entry.
2. Class representation. Proposal: flat injective percent-escaped keys per (resource, class) row, keeping the
   `estimate_get` pair-of-strings accessor. Alternative: a class-aware accessor returning resource and class
   separately.
3. Decimal policy. Proposal: exact reduced rationals in the certificate plus a displayed 34-significant-digit
   enclosure rounded upward. Alternative: request-selected precision with an explicitly bound rounding policy.

Recommendation. 1: the new explicit signature. 0.9 is already a breaking version and one entry point avoids a
forwarding path that must never invert a hash. 2: flat escaped keys; the accessor shape stays and the vector is
identical. 3: fixed 34-digit upward enclosure plus exact rationals. An estimate is an upper bound by purpose, the
bytes are reproducible, and selectable precision can be added later as a request field without changing meaning.

Consequence. bennett-estimate can be briefed; VM hsd/c15 close; G-estimate conformance cases become available.

### A3. CLAIM-REPLAY (K13, §9.2/§12.1–12.3; beads b-isa-spec-9uy, bennett-vm-clw; circuits 4pf shares it)

Background. §12.1 says a sampled claim is replayed against an `expected` relation and compared as full tuples,
but 0.8 gives no default relation, no encoding of a table row or of the invocation (args, budget, tokens) that a
standalone claim was replayed under. A checker that compares a claim with itself proves nothing; the draft's
witness (x=1, a=2, target 2, fault 3) shows a case identity self-replay would miss. Three choices:

1. Sampled default. Proposal: `expected` is mandatory. Alternative: omitted means `"oracle"` with a bound subject.
2. Invocation. Proposal: each standalone claim carries its resolved invocation, the scheduled root in
   `bindings.invocation`, hashing the canonical args array with typed encodings (unsigned decimal bit-vectors,
   binary64 hex, token tuples). Alternative: a shared invocation registry with ids.
3. Tables. Proposal: complete positional before/after tuples, one row per domain element, with the compact
   `program` relation for large domains. Alternatives: fully named tuples, or a keyed table limited to sampled draws.

Recommendation. 1: mandatory `expected` (rule 1, no silent defaults inside a certificate). 2: per-claim resolved
invocation as drafted; certificates stay self-contained and hash-bound without a registry indirection. 3:
positional complete tuples as drafted, which also settles circuits 4pf's row encoding; use `program` for large
domains. Consequence: VM clw/9uy close; circuits 4pf reduces to the closure resolver choice (B3 below).

### A4. Q14 reading (lproc headers; bead 7u6 closed by the edit)

Background. Lifted procedures could not pass budget tokens or classical arguments to nested lifted calls. The
maintainer accepted Q14; the worklog wording was ambiguous and a sol editor applied it as lproc header groups
`(params)(result)(tokens)(classical)(mem)` with `lift.call` passing tokens and classical args. Not a rung-4
blocker (SQLite runs under one budget) but a north-star generality item (sub-budgets, A1's one-budget claim
unaffected). Recommendation: confirm as applied. Overrule only if you intended a readable classical-argument
environment instead of explicit parameters.

### A5. Items drafted without an open choice (confirm or object)

- EPS-DECADE (K9, §8.1): zero-based `min{j ≥ 0 : eps·10^j ≥ 1}`, domain (0,1], exact rational comparison, exact
  entries forbidden. Boundary cases print 0,1,1,2,3,4. Recommend accept. Unblocks VM cxg, circuits v44, targets w8o.
- BLOCK-IMAGE (K10, §7.3): complete 512-byte sectors; partial final sector rejected at device initialisation.
  Recommend accept (reference and VM already agree). Closes VM 47i.
- Measurement draw ordering (bead bas): 0.9 states the draw-consumption order normatively; the VM and the reference
  already share the reference CLI's convention. Recommend adopting that convention as the text.
- ISA-7 `fault C` row in CC/R and the fault-code table; Q1–Q13 as you accepted them on 2026-10-29. No action.

### A6. Topology schema (bead b-isa-spec-wr7 ← b-targets-dd3; circuits b4k) — NOT yet drafted

Background. §8.2 says "a topology is declared" but §8.3 defines no field. A 2D-grid superconducting target cannot
be expressed; circuits placement defaults to all-to-all; targets M1 is blocked on it. Rung 4(c) promises a
resource estimate "under a named target"; all-to-all makes that estimate a fiction for any real device.

Options. (i) Draft a topology schema into 0.9 now: vertices/edges, addressable class assignment, routing
validation rules; one sol drafting job plus council scrutiny. (ii) Ship §8.3 with an optional `topology` field
whose semantics when present are defined, default all-to-all, routing cost rules in 0.10. (iii) Defer wholly.

Recommendation. (ii). It unblocks targets and circuits placement without holding the 0.9 dossier on routing
semantics, and it is not a narrowing because the capability is defined, only its cost model deferred.

## B. Circuits M2 proof-contract decisions (beads 7bu, z9r, 4pf, 4fa, yz8)

These are design choices inside bennett-circuits that the implementer refused to make unilaterally because they
fix an interchange or proof contract. The specialiser refuses the affected paths naming the bead until decided.

- B1 Multi-block actions (7bu, needs one ISA sentence). §5.3 lists structured bodies; §16.2 permits several
  `block`s but defines no action branch or join. Reading one: blocks are text-order unitary fragments, labels
  descriptive. Reading two: executable CFG nodes with coherent branch/join/padding/adjoint semantics.
  Recommend reading one, stated in 0.9 §5.3. Reading two is a new ISA feature nobody has asked for.
- B2 Proof IR for symbolic workspace across calls (7bu). Histories: versioned symbolic instruction histories with
  argument/token atoms and call keys, proving universally at `check`. Obligations: canonical transfer expressions
  plus undischarged obligations discharged at instantiation, with a universal coverage rule. Recommend
  histories. It proves §6.2's "exact computing sequence" universally at check time; the obligations route
  invites the exact "check one token" trap the note warns about. Cost: a new versioned IR shared with cleanup
  checking.
- B3 Opaque imports (z9r). Extensional proofs from signatures via uninterpreted function identities, or pending
  obligations discharged after §9.3 linking. Recommend pending obligations: §9.3 places certificate composition
  at link time, and an unlinked `hash` must report obligations pending rather than a completed proof.
- B4 Certificate replay encoding and resolver (4pf). Row encoding: settled by A3 (positional complete tuples).
  Resolver for `expected.program` and `inverse_pair_library`: a linked-object closure registry (certificate DAG,
  rebinding, cycle checks) or an explicit replay-input bundle. Recommend the closure registry; linking needs the
  DAG anyway under §9.3/§12.3.
- B5 Frame schema JSON (4fa, §9.4/§12.3). Typed records (`slots`, scratch/history/borrow/ancillae) or per-class
  expression maps with role annotations. Recommend typed records, published in 0.9 §9.4; explicit slot
  identities are easier to validate and the recursive schema is a one-time cost.
- B6 Inherited context and recompute (yz8). Resolved by publishing the library (A1); no second identity contract.

Consequence of B as a whole: circuits M4 (new certificates) and M5 (QIR/Quil) can be briefed immediately; M4's
numerical and channel claims still wait on A1's published library.

## C. North star iteration 8 (amendments A1, A2) and process

- A1 (one run-level budget, sourced landscape table) and A2 (handles through bitwise copies; region identity by
  content, operand as classical data) are ready for council round 7 of `northstar-2026-10-28`. A2 codifies
  decisions you took on 2026-10-29 that the dialect already implements; A1 is precision and attribution.
  Recommend running round 7 tomorrow when muse is back, in parallel with the dialect's next round. One round
  expected; not on the critical path.
- Council seats: sol in the opus/fable seat, astra, muse for specs and acceptance votes. Recommend keeping it;
  it converged the interpreter from 3.33 to 4.38 in six rounds.
- Plugin and driver start: held on dialect acceptance by process rule only. Recommend releasing plugin M1 now
  against 0.2.5/0.2.6 (taint inference and marker emission are insensitive to the open blockers); driver M1 after
  the dialect's §17 lowering text stops moving.

## D. Suggested order of answering

A1 (schema/hash, decomposition set) → A2 → A3 → A6 (needs a drafting job if (i) or (ii)) → A4/A5 confirmations
→ B1 (one ISA sentence) → B2–B5 → C. With A and B1 answered, one sol editor finishes the 0.9 draft, the
precheck is extended, and the 0.9 council dossier runs after the interpreter is accepted.

## Ratification — 2026-10-30

The maintainer ratified every recommendation above ("I am happy with all of your recs, please ratify").
Record of decisions, by item:

- A1: ISA-REF-LIB schema, envelope hash rule, ordinals, scratch identity, `removable` empty, deterministic
  Boolean decomposition (postorder, fresh scratch per node, no CSE, bit loops from LSB) as drafted in 0.9 §11.1;
  decomposition set = the §17 defaults made explicit, simplest deterministic choice; later libraries are new versions.
- A2: new explicit 0.9 estimate signature with resolved parameter vector; flat injective percent-escaped
  (resource, class) keys; exact reduced rationals in certificates plus a 34-significant-digit upward enclosure.
- A3: `expected` mandatory on sampled claims; per-claim resolved invocation and `bindings.invocation` at the
  scheduled root with typed canonical encodings; complete positional before/after tuples, `program` for large domains.
- A4: Q14 as applied (lproc header groups `(params)(result)(tokens)(classical)(mem)`; `lift.call` passes tokens and
  classical args). Confirmed.
- A5: EPS-DECADE, BLOCK-IMAGE (complete 512-byte sectors), draw ordering = the reference CLI convention stated
  normatively, ISA-7 `fault C`, Q1–Q13. Confirmed.
- A6: 0.9 §8.3 gains an optional `topology` field (vertices, edges, addressable class assignment) with defined
  semantics when present; absent = all-to-all; routing cost rules deferred to 0.10 as a §17 item.
- B1: multi-block actions are text-order unitary fragments, labels descriptive; one sentence in 0.9 §5.3.
- B2: proof IR = versioned symbolic instruction histories (universal proof at `check`).
- B3: opaque imports = pending obligations discharged after §9.3 linking; unlinked `hash` reports pending obligations.
- B4: replay resolver = linked-object closure registry (certificate DAG); row encoding per A3.
- B5: frame schema = typed records (`slots`, scratch/history/borrow/ancillae), published in 0.9 §9.4.
- B6: resolved by A1.
- C: north-star round 7 (A1 + A2 as iteration 8) when muse is available; council seats unchanged; plugin M1 may
  start against dialect 0.2.x now; driver M1 after the lowering text stops moving.
