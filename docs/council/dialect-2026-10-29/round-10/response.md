# Editor's response after round 10 (0.2.11 accepted by sol and codex) — draft 0.2.12, consumer-named gaps

Round 10 accepted draft 0.2.11 (0 blocking; gate 2834/2834); the 33 evidence closures remain tracked in b-dialect-spec-oxs.

Draft 0.2.12 (2026-11-01, HEAD cc04ecb) exists because implementers named eight gaps against accepted 0.2.10 @ 023f5a7
while building the ladder (rung 2 complete, rung 3 in progress): the plugin (mkb: §7.2/§12 N0 forwarding-thunk
resolution versus N0 materialisation order), the runtimes (jjr: malloc alignment versus exact ISA primitive allocation
history; lbq: musl console syscall framing and startup/model history ABI; 0na: native comparison primitive exception and
resolved heap configuration ABI, `__bennett_rt_native_layout`) and arith (dfd: PPCDoubleDouble fallback versus correct
rounding; 1av: accuracy and constrained flags for own-format carrier libm; z7u: arbitrary-format metadata naming and
static bitcode instantiation schema; 21a: signaling constrained comparison versus quiet carrier ABI). Each pass has a
dispositions row in spec/Bennett-Dialect-Spec-0.2.PROGRESS.md and a checker addition; the gate went 2834 -> 2893.
Readings adopted (brief: ../bennett-dialect-spec/docs/briefs/2026-11-01-dialect-0212-consumer-gaps.md): mkb N0 before
resolution, retain source addresses (clarified; closed); jjr aligned C wrapper with exact primitive history (clarified);
lbq ordered writes, static startup, tier-specific history (clarified); 0na comparison-only primitives and resolved layout
(new ABI); dfd exact sum / correct rounding outrank fallback quirks (new precision requirement); 1av full-domain one-ulp
bound and explicit constrained flags (new requirement); z7u named formats and static instantiation schema (new ABI); 21a
distinct signaling `cmps_B_rm` (new ABI). spec/errata-0.2.10.md binds the interpretation of the eight 0.2.10 sentences
without editing 0.2.10 (the plugin's pin stays valid). Seven beads stay open as implementation blockers (the
implementations do not yet meet the stated requirements; 12 follow-up beads filed in plugin, runtimes, arith, driver).
Grading target remains ISA 0.8; the 0.3 track (target ISA 0.9) follows.

Nothing declined. Diff attached is the round-10 snapshot (0.2.11) to HEAD cc04ecb. Material to scrutinise: the eight
new/clarified sentences (§§3.1, 7.2, 11.2-11.3, 12.2, 13.1, 13.3-13.5, 16.9, 17.1, 17.7, 19.2, 19.5) and whether each
requirement is implementable and testable by two independent implementers; S0 only blocks.
