# Editor's response after round 6 (codex seat) — passes VI and VII

R6-CODEX-1 (core S0, §5.6 rule 1 own controls vs effective control context): ADOPTED as recommended (pass VI,
commit 44ffea0). Rule 1 now reads: "If any control literal is known false, counting the operation's own controls
together with its effective control context, the operation is disabled: preserve all abstract values and record no
causal event." The reviewer's witness (ccx z u c with z = qalloc, then the cx c b frame) is a frame_domain regression
in the reference interpreter (accepted with c=0 at frame entry; its c=1 variant rejected). The reference already
behaved this way; the text was aligned to it.

S1 (rule 3 canonical D_F under acceleration): ADOPTED verbatim. S1 (§12.2 frame obligation uses D_F, with the
illustration): ADOPTED. S1 (regenerate the 0.9 statement layer): orchestrator's job in bennett-conformance, done after
this round. Pass VI gates: reference 467, conformance 113, witness and catalog check green. (74af3fe records.)

Pass VII (new material, consumer-named gap b-isa-spec-5xm from bennett-vm): oracle catalog calls did not say where the
oracle's invocation token tk binds (§16.2 header groups (in)(tgt)(fault)(mem)(args); K24 actuals in formal order; no
implicit bindings). Reading B adopted: tk is an explicit source-binding channel `oracle_invocation` outside A,
carrying the canonical four-string tuple; consumers MUST supply and validate it before concrete expansion, preserve it
through forwarding, template adapters, nested calls and inverse traversal, and reject missing, ill-typed or
source-inconsistent context. K77 is the only new row. Worked example: the same inc8 closure at B=2 and B=3 in one
expansion (two and three frames; final (x+1,1) from zero target/fault; regression over all 256 inputs with inverse
restoration). Catalog bytes and envelope unchanged; 0.8 untouched. Gates: reference 468, conformance 113. Commits
1d86f00, 4f7e18f, e0bd3a8. Exact normative text: spec/isa-0.9.PROGRESS.md pass VII block.

Nothing declined. Diff attached is round-6 snapshot (pass V) to HEAD e0bd3a8 (passes VI and VII). Material to
scrutinise: §5.6 rule 1 and rule 3, §12.2 addition, §11.1/§16.2 `oracle_invocation` channel and K77.
