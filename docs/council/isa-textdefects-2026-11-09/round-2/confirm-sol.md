# SOL-TEXT-C01 round-2 confirmation

Verdict: **CLOSED (merge)**.

Reviewed at 2026-11-09T10:20:48Z; candidate `89d30f593046baeb210013d0a2fa3788924fa31d`, against
`b08940d2b6fa04e7322befe2e8f98b91a1055caf`. The candidate's tracked working
files equal HEAD. No blocking reason remains, and no new P2 bead is requested.
This is the requested one-item confirmation, not a new council round.

1. **Claim:** The source remains legal, with matching `k=1,c=2`.
   **By:** clause: §3.3 Disjointness and §11.1 Typed binding permit an effective
   control to coincide with an own control, with neither coinciding with the
   target. Clause: §8.1 still defines `c=k+effective_control_count`.
   Clause: §8.3 lines 2225–2235 explicitly supports this overlap in both model
   forms, including positive advertised epsilon. The repair adds no source
   rejection and does not alter matching, costs or scheme-template operands.

2. **Claim:** Both encodings now have a complete physical binding.
   **By:** clause: §8.3 lines 2225–2299 defines the sorted identity union `D`,
   model-only `d=|D|`, controlled_U order `D` followed by its base targets,
   and explicit arity `d+target_count` with model-local `c[j]=D[j]`. For
   `[p,p,t]`, `D=[p]`, `d=1`, model order is `[p,t]` and the permutation is
   `[0,1]`. Explicit context selection remains at `c=2`. Both literal and
   generated maps, and literal and d-dependent dimensions, bind successfully.
   **Witness:** re-ran `probe.py`: both model forms produce the matrix
   `diag(I2,X)` and outputs `(0,0),(0,1),(1,1),(1,0)` for the four ordered
   inputs. The exact operator error is zero, so advertised epsilon `1/4`
   with requested share `1/2` is conformant in both forms. Omission of the
   required positive-epsilon model still cannot establish accuracy.

3. **Claim:** The physical semantics agree with the existing reference adapter.
   **By:** witness: `conformance/src/ref_language.rs:149` represents a resolved
   wire as `(String,usize)`; `permutation()` at lines 2118–2176 unions the
   effective controls with the X-family own controls, sorts and deduplicates,
   then appends the target. Thus this CX uses one physical p control and
   toggles t iff p is one. The independent Fraction probe exhausts the four
   inputs. It also checks several overlaps, numeric bit indices 2 and 10,
   distinct-control `[1,0,2]` compatibility, and generated/literal map equality.
   This confirms the reference function's semantics by source inspection and
   independent arithmetic; no reference-executable/native-decoder run is claimed.

4. **Claim:** Genuinely ill-formed maps remain rejected.
   **By:** clause: §8.3 lines 2251–2265 retains the MUST rejecting non-permutation
   maps and the MUST comparing supplied maps to resolved identities on both
   matrix axes. Length is explicitly `d+target_count`; repeated, missing,
   out-of-range and stale positions reject. Deduplication happens before map
   construction, so `[0,0,1]` remains malformed.
   **Witness:** both-form probes reject `[0,0,1]`, `[0,0]`, `[0]`, `[0,2]`,
   and stale permutation `[1,0]`; an explicit row selected using d instead
   of matching c also rejects. The independent phase witness gives
   `||diag(I2,-X)-diag(I2,X)||op=2`, so it cannot pass epsilon `1/4`.

5. **Claim:** The fix preserves the round-1 accepted core without narrowing.
   **By:** clause: d is expressly model-only; k/c retain §8.1 meanings,
   §11.1's identity union is preserved, and full physical phase/accuracy and
   representation obligations remain separate. Clause: §15 N4/N5 now requires
   the overlap, both forms/maps/dimensions, positive epsilon and malformed
   counterparts. Witness: the exact scope check passes: only native §8.3/§15
   blocks changed. K85 process/preparation/replay and K91 token/loader text,
   interpreter/conformance code and catalog bytes are unchanged. Prior
   occurrence, mem-slot-order and realised-prefix regression checks pass.
   No host-size cap, new source fault, or smaller algorithm domain is added.

## Commands and receipts

All commands used headless settings and this review's `tmp-sol2` as TMPDIR.
The supplied probe/driver writes JSON and receipt files. To obey the read-only
brief, commands ran from `tmp-sol2/view`, with source/scripts symlinked to the
subject and real writable c01/fix receipt directories inside that view.
`GIT_WORK_TREE` pointed to the subject, so git checks inspected the actual
candidate. Script bytes were unchanged. Only the report and allowed scratch
area were written.

| Exact command from the review view | Observed result |
|---|---|
| `python3 -I -B .tmp/isa-textdefects-c01/probe.py` | Exit 0: both forms, four outputs, positive epsilon, malformed/stale maps, matching c and ordering checks pass |
| `python3 -I -B .tmp/isa-textdefects-c01/probe.py --baseline` | Expected exit 1: controlled_U `[0,0,1]` non-permutation; explicit arity/basis disagreement |
| `python3 -I -B .tmp/isa-textdefects/check_contract.py --self-check` | Exit 0: 31 MUST rows, 20 detected corruptions, 14 groups |
| `python3 -I -B .tmp/isa-textdefects-c01/run_checks.py --committed` | Exit 0: all eight checks, including prior driver with all 13 checks |
| `python3 -I -B conformance/tools/ref_catalog.py --check` | Exit 0: 219 recipes; envelope SHA-256 `5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197` |

Exact argv, head, source hash, UTC, exits and wall/CPU measurements:
`tmp-sol2/review-verification.json`. Per-command outputs are beside it;
nested receipts are under `tmp-sol2/view/.tmp/isa-textdefects-c01/` and
`tmp-sol2/view/.tmp/isa-textdefects-fix/`.

These are publication, rule-projection, exact-arithmetic and scope checks.
They do not establish an implemented native-model reader or executable
checker coverage. Those staged follow-ups and the orchestrator's full-gate
responsibility remain as accepted in round 1. No full gate, production edits,
commits, pushes, new agents or PR operations were performed by this reviewer.
