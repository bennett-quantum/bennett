# Bennett ISA 0.9 reference interpreter: quality-floor change set (job/quality-isaref), council round 3 (FIX ROUND, last round)

Subject: as rounds 1-2, now at head `185e9ba` (range `be109bd27889ea91e3c0ad78a30e5e4d71d3d0d3..185e9ba`). Round 2 (graded at
5b71208): sol ACCEPT, muse ACCEPT, codex REVISE / core accept with one blocker CODEX-R2-B1 (an imported qinplace pair whose
body is unavailable skipped the K92 missing-owner-pair rejection: ISA 0.9 §12.3, §9.3). Since round 2 the editor landed
704d21d (isa-spec main review r2 document: CLEAR), be2ce19 (mandatory pair bindings checked before unavailable proof outcomes),
09f183d (static pair context validated before linked proof replay is deferred; touches claims/pairs09.rs), b618b16 (saved
imported regression fixture audited), 185e9ba (evidence). The editor reports CODEX-R2-B1 resolved together with a sweep of the
same early-return ordering class (docs/quality.md); bead b-isa-spec-dqkt closed. Reported: isa09_qinplace 42 pass.

Fix-round policy: the members re-grading here are those whose round-2 verdict was not accept (codex) plus sol because the fix
reaches beyond qinplace09.rs (pairs09.rs). Fill previous_status for CODEX-R2-B1. Grade the fix diff 704d21d..185e9ba closely
(`git diff 704d21d 185e9ba` in the working directory), check the early-return sweep for the same class elsewhere, and confirm
no earlier-round fix regressed. Round 3 is the LAST council round: a blocker must be a real S0 with a reproducible witness.

Your working directory is a frozen detached worktree of `bennett-isa-spec` at 185e9ba (reference-interpreter/target/debug/
bennett-isa-ref prebuilt). Embedded: (1) the full unified diff of the range and (2) the post-change text of every changed file.
