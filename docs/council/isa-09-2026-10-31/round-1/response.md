# Editor's response to ISA 0.9 round 1

Both seats: **accept core**, **revise overall**. Both new S0 contract
findings are addressed. The two carried owner gaps are drafted for
maintainer ratification in round 2; bead closure records that drafting,
not ratification. No accepted 0.8 bytes change and no north-star
capability is removed.

## Dispositions

Clause locations below use the final scratch statement view. Dependency
IDs use the supplied catalog authority; the new §11 concepts follow the
existing paragraphs, preserving the matching/specificity/staging IDs.

| Finding | Disposition | K row | Clauses | Declared dependencies | Bead status |
|---|---|---|---|---|---|
| SOL09-R1-B01 | addressed; canonical source adjoint | K62 (K28 retained) | ISA-5.3-P8; ISA-11.1-P30/P31/P32/P40 | [deps: ISA-11-P2, ISA-11-P5, ISA-11-P6, ISA-11.1-P29, ISA-11.1-P29.S1, ISA-11.1-P29.S2, ISA-11.1-P29.S3, ISA-11.1-P5, ISA-4.5-P5, ISA-4.6-P7, ISA-5.2-P3, ISA-5.3-P4] | — |
| COD-R1-B01 | addressed; explicit instance/call_index | K63 (K49/K52 reconciled) | ISA-9.2-P1.S3; ISA-11-P3/P5/P9; ISA-11.1-P9/P29.S4; ISA-12.1-P11/P14 | [deps: ISA-11-P3, ISA-11-P5, ISA-11-P5.S5, ISA-11-P5.S6, ISA-11-P5.S7, ISA-11-P6.S1, ISA-11-P6.S2, ISA-11-P6.S3, ISA-11.1-P29.S3, ISA-11.1-P5, ISA-11.1-P9, ISA-3.7-P5, ISA-3.7-P6, ISA-9.2-P1.S3] | — |
| SOL09-R1-G01; COD-R1-G01 | drafted for ratification; council round 2 | K64 | ISA-11-P3/P5.S9/P10 | [deps: ISA-11-P2, ISA-11-P5, ISA-11-P5.S8, ISA-11-P7, ISA-11.1-P14, ISA-11.1-P18, ISA-11.1-P22, ISA-11.1-P22.S14, ISA-11.1-P29, ISA-11.1-P29.S1, ISA-11.1-P29.S2, ISA-11.1-P29.S3, ISA-11.1-P5, ISA-11.1-P9, ISA-3.6, ISA-3.7-P5, ISA-4.6, ISA-5.2-P3, ISA-8.2] | 8ka CLOSED; maintainer ratification pending |
| SOL09-R1-G02; COD-R1-G02 | drafted for ratification; council round 2 | K65 | ISA-11-P5.S9/P11 | [deps: ISA-11-P2, ISA-11-P3, ISA-11-P5, ISA-11-P6, ISA-11-P6.S1, ISA-11-P6.S5, ISA-11-P6.S6, ISA-11-P6.S7, ISA-11-P6.S8, ISA-11.1-P29, ISA-11.1-P5, ISA-3.7-P5, ISA-4.2, ISA-4.3, ISA-4.5, ISA-4.5-P5, ISA-4.6, ISA-5.3, ISA-5.5, ISA-6.2, ISA-6.2-P1, ISA-6.4, ISA-6.4-P1, ISA-8.2] | 23g CLOSED; maintainer ratification pending |
| SOL S1; COD-R1-S01 | addressed; semantic dependency targets | K66 | ISA-9.2-P5.S6; ISA-11-P6.S2/S3, P7.S1/S6/S7/S8; ISA-11.1-P30/P31 | [deps: ISA-9.2-P4, ISA-11-P5, ISA-11-P6.S1, ISA-11-P6.S2, ISA-11-P6.S3, ISA-11-P6.S4, ISA-11-P7.S2, ISA-11-P7.S3, ISA-11-P7.S7, ISA-11.1-P29.S3, ISA-11.1-P29.S5] | — |
| SOL S2 | addressed with COD-R1-B01 | K63 | same K63 clauses | [deps: ISA-3.7-P5, ISA-3.7-P6, ISA-11-P5, ISA-11.1-P9, ISA-12.1-P11] | — |
| SOL S3; COD-R1-S04 | addressed; synthetic fixture scope | K62 / K28 | ISA-11.1-P31 | [deps: ISA-4.5-P5, ISA-11.1-P9, ISA-11.1-P22, ISA-11.1-P29.S1, ISA-11.1-P29.S2] | — |
| COD-R1-S02 | named omissions addressed; broad historical audit recorded | K66 | ISA-11.1-P9.S3/S4/S5/S6, P22.S5/S12/S14; ISA-12.1-P7.S3/S6/S7 | [deps: ISA-3.7, ISA-3.6, ISA-5.2-P3, ISA-11-P5, ISA-11.1-P29, ISA-5.2, ISA-14.3-P3, ISA-5.6, ISA-12.1-P4, ISA-12.1-P5, ISA-14.2] | 82i OPEN for remaining K1–K27 audit |
| COD-R1-S03 | addressed; legal F/W/layout and coverage | K67 | ISA-12.1-P9/P10 | [deps: ISA-5.4, ISA-7.1, ISA-7.2, ISA-12.1-P8, ISA-12.1-P13, ISA-12.2] | — |

## Decisions and rejected alternatives

- **Adjoint:** form the §5.3 source replacements before recipe instantiation.
  `adj` now splices the already source-adjointed body. For n=1/F=4,
  `adj(qinplace G H)` has alloc t[1]=0, alloc f[4]=1, call H, swap=2,
  call G, release t=3, release f=4. With ordinal-0 allocation class
  special and default otherwise, t is special and f is default. The
  qif replacement still reverses its complete expansion, including
  lifetimes. Raw inverse constructors retain forward ordinals when
  reversing expanded machine rows. Reject the alternative that treats
  the table as only extensional and changes K28's scheduled order.
- **Invocation identity:** explicit instance and call_index fields keep
  source points independently checkable. Semantic calls are counted in
  forward instantiated traversal before callee descent; inverses retain
  the numbers. Fixed keys [0]/[1] remain distinct even for equal values.
  Omission means wildcard, and specificity remains unchanged. Reject
  dynamic lift.call histories, leaf ordinals as caller identity, argument
  value hashes as instance identity, and opaque synthetic-point encodings.
- **Non-row points:** choose $construct/$step/$commit/$release over
  $alloc:0 etc., because construction includes initialisation gates and
  these are support phases rather than invented block/row numbers. The
  exact oracle.construct/step partition, nested helper inheritance,
  Rows/Next/callee exclusions and B=0 behavior are printed in §11.
  These are addressing annotations over the same recipe stream.
- **Cleanup:** one non-emitting carrier at the source cleanup point,
  generated wildcard or 0, precedes realisation expansion and exists for
  empty cleanup. Only cleanup entries match it; the selected unitary
  realisation applies to the whole pair. Reject a first-realised-leaf
  carrier, per-leaf realisation selection and an artificially charged
  event. Both reverse and recompute remain available.

## Suggestions not fully applied

COD-R1-S02's named omissions are repaired, as are all the other six
suggestions. A complete premise audit of every remaining historical
K1–K27 addition is recorded as b-isa-spec-82i. This advisory task needs
sentence-content review; mechanically inserting broad existing-ID edges
would repeat the problem. The focused changed-sentence audit does not
claim to complete that historical audit. Rejected alternatives and all
seven suggestion dispositions are also in spec/isa-0.9.PROGRESS.md.

## Library binding and mechanical checks

The adj recipe body and source bytes changed; the recipe count remains
**219**. Old envelope SHA-256:
`fcb2f1e6d61aced0bf9689eab5f6d82c4ae42e9fea8d1b21ae9c7ffccda6f5ce`.
New envelope SHA-256, independently computed in Python -I and Rust:
`5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197`.
The §11.1 complete-library marker is updated; the qxor witness hash is
unchanged. `conformance/tools/ref_catalog.py --check` passes and Rust's
independent_canonical_bytes_and_envelope_hashes agrees byte for byte.

The trace regression first failed on the old adj adapter (first private
allocation width 4 instead of 1). The final vector instantiates the actual
bound adj and qinplace recipes with synthetic identity-map fixtures,
checks H then G, caller ordinals, separate callee spaces, widths,
allocation/release identity and the nondefault allocation-class selector.
It does not claim full ISA oracle executor conformance from synthetic
callees. The existing qinplace symbolic tests exercise both orientations.
Four distinct invocation keys and their schedule prefixes round-trip in
JSON, including both fixed instances.

The replay witness now has x/target/a width 2, fault width 4, one dirty
bit and two W=8 cells. Its printed legal layout maps the unused interface;
its full domain is 25 bits, with unchanged XOR outcomes. Four singleton
draws consume no generator words and cover 1/33554432.

- Exact requested diff -u command regenerated spec/isa-0.8-to-0.9.diff.
- `python3 -I conformance/tests/draft_witnesses.py`: PASS, including exact
  diff-byte comparison and unchanged accepted-0.8 digest.
- `cargo test --offline --manifest-path conformance/Cargo.toml --test draft_contracts`:
  PASS (1 test).
- Targeted ref_catalog, ref_structure and ref_qinplace_contract checks: PASS.
- Changed normative prose audit: all 53 changed sentences have markers;
  every declared ID exists in the supplied authority. Scratch graphs and
  statements are in project-local .tmp only. The schema block has a
  declared prose introduction. No forbidden draft wording remains.
- Full offline conformance suite: PASS, 112 passed, 0 failed, 0 ignored
  across 35 result groups (including empty unit/doc groups).
- `bd export -o .beads/issues.jsonl` performed; no push or Dolt sync.

Implementation commits in bennett-isa-spec: `afd4bb6` (item 1), `b818b40`
(item 2), `317d919` (item 3), `efaad51` (item 4). Final validation commit `32c585a`
records the completed checks in spec/isa-0.9.PROGRESS.md. This
response is committed separately in bennett. No push is performed.

Accepted 0.8 SHA-256 remains
`90e61d9c377c939fe9652758f61cd5ead068ef06e4e40d812d3f3c5197ab605e`.
Final draft SHA-256:
`59eee9ad0d96d34b6c6fd8be0acb041a56c652e8be821393c153f83cde5df96b`.
Final diff SHA-256:
`2f244ed04ab07a4674c68ee46286934c22a7e007f01a242ff3ae580e164df91d`.
