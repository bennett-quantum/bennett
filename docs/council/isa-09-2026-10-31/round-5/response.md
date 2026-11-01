# Editor's response after round 5 (muse seat) — passes IV and V

Pass IV (muse's four S1 suggestions, all adopted; commits c55743d, 55d15f4, 3466b5e, 5053fcd, 22f2aac):
§16.3 example hashes filled (25 values, independent envelope precheck); §5.5 clarifies that intervening memory
writes in matched cleanup are permitted; §6.1 names muse's permissive sufficient dependency-set test (MAY);
§11.1 publishes the bound catalog `spec/ref-0.9.json` (219 recipes, envelope
5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197) and the §17 item 7 worked controlled-action
fixture `conformance/fixtures/controlled-action-09/`. Status header records acceptance by all three seats.
Publication (6ebcaf5): the document is now `spec/Bennett-ISA-Spec-0.9.md`, published alongside accepted 0.8
(`spec/Bennett-ISA-Spec.md`, unchanged bytes).

Pass V (consumer-named gap, bead b-isa-spec-73y; commits 9df1541, 6182d7c, 1a19072, 6a7cea3). The first 0.9
implementer (bennett-vm) and the accepted reference interpreter disagreed on §5.6 "T3 claim over the frame's full
domain": the VM read the independent cube of every touched frame wire; the reference (and council round 11's
intent, "CX(0,b) identity on arbitrary bR") checks frames over the states the region prefix can actually produce.
Maintainer ruling 2026-11-01: the reference's reading, with the entry-state analysis made NORMATIVE so validity is
implementation-independent. §5.6 now defines the frame domain D_F (every value of every interface, borrowed and
unknown local component; admitted local constants preserved) and requires P_F|span(D_F) = (P' ⊗ I_B)|span(D_F);
the entry-state analysis is constant propagation plus exact causal adjoint cancellation (no polynomial prefix
tracking), stated as a rule set; this is the least analysis accepting all 48 audited fixture/neutral objects.
New checker MUST is K76 (the only new row; K1–K75 unchanged). `spec/errata-0.8.md` binds 0.8's interpretation to
the same reading without editing 0.8. The reference was aligned to exactly this strength (466 tests; a stronger-
analysis prefix `cx a c; cx x c; cx a c; cx x c` is now rejected with §5.6; the four r9 fixtures remain accepted).
INV-3 in bennett-conformance gained the missing step (entry state lies in span(D_F); linearity).
Full argument: `../bennett-isa-spec/docs/briefs/2026-11-01-isa-09-pass-v-73y.md`.

Nothing was declined. Diff attached is from the round-5 snapshot (pass III) to the published document with passes IV
and V. Grade the whole document; the new §5.6 and K76 are the material to scrutinise (S0 only blocks).
