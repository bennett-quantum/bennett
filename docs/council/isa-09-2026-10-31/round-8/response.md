# Editor's response after round 8 (accept) — passes XI and XII, and the two S1s

Round 8 accepted passes VIII-X (K78-K80) with no blocking items; beads 7js, 9eq, 5cd closed. Both S1s adopted: portable
K78-K80 conformance vectors published (conformance/fixtures/accepted-k78-k80-09/: 21 vectors, 272 complete tuples,
byte-locked by three tests; the §15 sentence on adapter-assigned coordinates added); §3.3 now states that the equal-width
and widening/narrowing constraints apply to lifted rows on their location bit-vectors per §4.2 and that CC/R operand-type
restrictions do not retype lifted locations.

Pass XI (consumer-named by the rung-3 slice, musl hello-world in the reversible tier): b-isa-spec-221 (typed R faults) is
already determined by accepted K5, §4.9, §10 (closed as resolved; the 0.8 producer/executor migration is tracked as
b-isa-spec-fuk, open); b-isa-spec-04d (saved-tape interface) was an implementation item: the reference interpreter gained
`--tape-out FILE` / `--replay-tape FILE` on run-cc, CC/R reverse and run-program (strict JSON tapes validated entry by entry
before commit, exact exhaustion required; byte-identical output and reset on valid replay; divergence exits 1 with no
stdout; journals keep effects later cancelled by uncall). Nine regressions. No normative text; K1-K80 unchanged.

Pass XII (bead 9hv, consumer-named by bennett-vm): overlapping cleanup-pair partitioning. Reading B adopted: carriers at
entry:2 and entry:3 are independently selectable; the reference restores the call's captured entry versions before
quncopy; K80's release-ended whole cleanup is intact. New K81 (the only new MUST): "An intrinsic quncopy, qunload or
lift.oracle_uncall pairs only with its matching qcopy, qload or lift.oracle_call, respectively." Three regressions
(partition/ties, exact restoration, all four reverse/recompute combinations with nonzero history); reference src unchanged.

Also since round 8, not spec text: the reference's rung-2 run went from a 600 s timeout to 2 s (n8j); the VM's equivalent
defect was fixed; rung 2 is complete on both executors and both majors (2026-11-01T13:06Z).

Nothing declined. Diff attached is round-8 snapshot (pass X) to HEAD e4eb657 (passes XI-XII + housekeeping). Material to
scrutinise: K81 and §11's pairing text; the §3.3 lifted-rows sentence; §15 vectors sentence.
