# Editor's response after round 7 (accept) — passes VIII, IX, X (consumer-named gaps from bennett-vm)

Round 7 accepted passes VI and VII with no blocking items; beads 73y and 5xm closed; the S1 suite-H K77 adapter
vector was added (inc8 at B=2/B=3, all 256 inputs, inverse identity retention, record rejection). The statement-layer
regeneration S1 is done in bennett-conformance after this round.

Pass VIII (bead 9eq, K78): K76's event identity after X-family arity resolution. Reading B adopted (matches §4.4 and the
unchanged reference): x/cx/ccx/mcx resolve to one X-family flip kind identified by resolved target and effective control
set (own and contextual literals, polarity); qxor/qexch resolve to their per-bit cx/swap primitives before recording;
resolution is confined to the entry analysis (source opcodes, hashes, §11 occurrence identities unchanged; no
target-scheme decompositions or Boolean-equivalent replacement). Three regressions.

Pass IX (bead 7js, K79; plus the icmp clarification): zero-width coherent addressing. For qload/qunload/qstore/qexchm on
region[A,W], the address actual is exactly A live wires (wire[A], or an indexed single wire at A=1); at A=0 the token
`()` denotes the empty bundle and selects the sole cell under the control context; no wire[0], no zero-width qalloc or
qborrow; §11.1 binding is the ordered list of exactly A wires, `()` binds []. Eight regressions, four red-first A=0
witnesses. Also §3.3/§4.8 now say explicitly: binop operands iN; icmp operands iN or ptr of equal width (the accepted
reference's reading since round 2; a second implementer had read integer-only). No new MUST for that.

Pass X (bead 5cd, K80): multirow recompute source ownership for K65 paired-cleanup carriers. Reading A for recompute:
the entire replacement's caller-level leaves and call edges belong to the carrier's point and coordinates; reverse keeps
the written cleanup's source points and per-point spaces; fresh computation/XOR/uncomputation/releases in §6.4 order with
contiguous caller-leaf ordinals and independent semantic-call occurrence numbering; original rows unchanged, replaced
inverse rows emit nothing; K64 partition unchanged. Three regressions; reference src unchanged.

Also in this window (not spec text): the reference interpreter's per-step checkpoint became O(1) (bead n8j; the rung-2
hashtable n=0 went from a 600 s timeout to 2.0 s), which let the rung-2 end-to-end slice pass on the reference executor
on both LLVM majors (forward = native on ten cases, byte-exact reversal).

Nothing declined. Diff attached is round-7 snapshot (pass VII) to HEAD 99efbe4 (passes VIII-X). Reviewer brief:
../bennett-isa-spec/docs/briefs/2026-11-01-isa-09-passes-viii-x.md. Material to scrutinise: §5.6 resolved identity
(K78), §4.6 zero-width addressing (K79), §11 recompute ownership (K80), §3.3/§4.8 icmp wording.
