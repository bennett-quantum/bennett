# K93 candidate packet: bennett-isa-spec job/isa-k93 62a0cf0..1cf5a7e (commits 6bd1abb, 1cf5a7e)

Implements ISA 0.9 K93 (§4.4 mcx control bundles) in the reference interpreter's SET A files (validation.rs, action.rs, source_constructor/action.rs, borrow.rs) and publishes K93 conformance vectors (bead b-isa-spec-3ry, closed by the implementer). Grade fidelity to §4.4/K93 and that nothing is narrowed.

## Implementer PROGRESS.md (verbatim)

# Resume

Updated: Sun Nov  8 12:08:50 UTC 2026

Done: implementation complete; b-isa-spec-3ry CLOSED through bd in the main checkout. No other job bead or text-defect bead opened. No SET-A-external source edit needed. No full gate run. Council and full landing gate remain the orchestrator's steps.

Worktree: /home/tobias/Projects/bennett-workspace/bennett-isa-spec-job-isa-k93, branch job/isa-k93, base62a0cf0ef9f1f1c1db12c84ed24846b6b9695cdc. Commits:
- 6bd1abbf22a9182af1f8920a6bc469ba6aae21c3 — ISA09 control expansion and initial289 CLI vectors.
- 1cf5a7ed6c3f909ef65d6eb8657c9a5f0a0520c3 — final291 vectors, causal identity, cache actual remapping and certificate rechecks.
Both backed up with git push --no-verify -q origin HEAD:refs/heads/wip/isa-k93 after committing. Each message ends Agent: gpt-6.1-sol. Tracked tree clean; only .tmp untracked. All322 changed paths verified within SET A. No rebase/merge, worklog, spec, catalog, gate.toml or .beads commit.

Inventory at62a0cf0 and quoted K93 coverage:

| Clause (ISA0.9 §4.4 unless noted) | Baseline gap / existing behaviour | Final test in isa09_mcx_bundles.rs | Published vector |
|---|---|---|---|
| “It contributes every wire of that bundle, in increasing bit index; concatenate entries in written list order.” | validation.rs:603-617, action.rs:439-443, borrow.rs:930-934 required scalar controls and rejected bundles. | every_published_basis_column_and_adjoint_has_exact_positive_unit_amplitude; source_adapter_columns_match_independent_formula_vectors_in_both_directions | width-1/2/3, mixed-sb/bs |
| “The k in mcx(k) is the number of resulting control wires”; “k counts explicit flattened controls only; effective controls add per §3.5.” | quantum.rs:636 already counts resolved wires; source_constructor/action.rs:384-390 passed full formals to catalog flattening. Added explicit increasing-index expansion at source adapter. | mixed_written_order_and_active_predicate_have_k3_four_operands_and_c4 | predicate (all32 inputs); mixed-sb/bs (all16 each) |
| “The target denotes exactly one wire”; “A bare target name may denote wire or wire[1]; an indexed target must denote one live wire.” | validation.rs:615/action.rs:443 already enforce scalar target; preserve rule while admitting bundle controls. | basis-column tests; repeated_controls_overlap_and_non_scalar_or_dead_targets_reject_as_operands | wire1-target, indexed-target, multiwire-target, dead-target, target-out-of-range |
| “overlapping or repeated entries reject as ill-formed, never deduplicate them to repair an operand list.” | validation.rs:617 disjoint resolved all names but scalar check preempted bundle overlap checks. Runtime quantum.rs:415 positions also rejects duplicate physical wires. | repeated_controls_overlap_and_non_scalar_or_dead_targets_reject_as_operands; resolved_aliases_reject_before_any_gate_executes | repeated-scalar/bundle, target-overlap, scalar-target-overlap |
| “The empty list has zero explicit controls and applies X under the active predicate.” | Existing empty-list machinery works; lock it alongside new expansion. | both basis-column tests | empty, empty-predicate (all4 inputs each) |
| “Flattening determines resolved primitive operands, gate cost and realisation arity, but does not rewrite source identity or source points.” | Existing source hashing retains written operands. Catalog handles resolved arrays. | original_witness_retains_published_byte_identities; mixed_written_order_and_active_predicate_have_k3_four_operands_and_c4; k78_matches_complete_control_sets_after_bundle_expansion | original witness, mixed order, causal-same/different-controls |
| §15 “complete map ... (q XOR [c=3],p,c)”; “its adjoint applies MCX before SWAP”; “complete basis columns with amplitude +1.” | Entire original witness rejected at scalar validation. | every_published_basis_column_and_adjoint_has_exact_positive_unit_amplitude; source_adapter_columns_match_independent_formula_vectors_in_both_directions | witness all16 forward/adjoint tuples and exact sole amplitude[1,0] |
| §15 “preserving both displayed amplitudes” for entangled external R | Previously rejected. Expected amplitude independently specified as std::f64::consts::FRAC_1_SQRT_2; no output-derived expected amplitude. | external_reference_coherence_preserves_both_exact_prepared_amplitudes (H(R), CX(R,c0), CX(R,c1), full state and exact inverse equality) | k93.json.reference_witness; coherent-fwd/adj CLI inputs |
| §15 “unchanged source hashes do not validate old execution caches”; “certificates rechecked”; “those recipe bytes and their catalog hash stay unchanged.” | No persistent source-resolution cache. CallCache is fresh per compiler (borrow.rs:1950); remaps per actual (call_transfer:500). Constructor compiled nodes are local to one Compiler. No pre-existing accepted bundle fixture/schedule/leaf-hash lock existed at this pin. | cached_callee_transfer_remaps_complete_bundle_for_each_actual_binding; rechecked_certificate_proves_all_controls_and_rejects_stale_first_bit_relation; pinned catalog check | witness-certified proves full16 rows; identical-source-hash witness-firstbit-certificate admits operands/schema but fails full tuple mismatch at c=1 |

All clauses above GREEN. No interpreter execution parallelism or restructuring. ISA0.8 scalar admission is retained and tested separately. K78 matching uses complete resolved control sets; source version histories remain written identities, as §5.6 requires. New resolutions are regenerated per invocation; no persisted cache schema or bound schedule needed changing. Correct and stale certificates are regenerated from the §15 conjunction/first-bit equations, never executor results. The original witness file is byte-identical to the published witness and pins object db3d3f92a79077074901449d83532f1a0d82ef1621bd833adb7ad14d1aedd467 / closure e38d5da64f9a0ae89a66243bcbe5a321cb807a5bbabf83952b63d3465dfab346.

Read: brief/COMMON/T3CHILD, repo CLAUDE/AGENTS/HANDOFF, bead, §4.4/K93/§15 and derive3 council doc/report. No K94 fixtures exist at this pin; K84/K91 publication layouts inspected. All expected semantic values are hand-derived integer conjunction/XOR formulas in generate.py and vector notes; optional --ref uses CLI only for identity metadata.

Verified, exact commands (all headless, offline and job-local):
Environment prefix for every shell command: env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER TMPDIR=/home/tobias/Projects/bennett-workspace/bennett-isa-spec-job-isa-k93/.tmp/isa-k93/tmp CARGO_TARGET_DIR=/home/tobias/Projects/bennett-workspace/bennett-isa-spec-job-isa-k93/.tmp/isa-k93/target. Conformance additionally BENNETT_CONFORMANCE_BIN=/home/tobias/Projects/bennett-workspace/bennett-isa-spec-job-isa-k93/.tmp/isa-k93/target/debug/bennett-isa-ref.
- RED: python3 .tmp/isa-k93/run.py red-reference-behavior cargo test --offline -j4 --manifest-path reference-interpreter/Cargo.toml --test isa09_mcx_bundles -- --test-threads=4 =>exit101, 7 scalar-width failures/2 passed. red-reference was an initial test compile mismatch, corrected before the behavioral red.
- RED: python3 .tmp/isa-k93/run.py red-conformance cargo test --offline -j4 --manifest-path conformance/Cargo.toml --test k93_vectors -- --test-threads=4 =>exit101, coherent-adj rejected by the scalar-width §3.3 diagnostic.
- GREEN focused final: python3 .tmp/isa-k93/run.py green-reference-final-expected cargo test --offline -j4 --manifest-path reference-interpreter/Cargo.toml --test isa09_mcx_bundles -- --test-threads=4 =>11 passed/0 failed, exit0, 19.02s wall/20.07s CPU.
- GREEN final complete reference: python3 .tmp/isa-k93/run.py full-reference-final cargo test --offline -j4 --manifest-path reference-interpreter/Cargo.toml -- --test-threads=4 =>730 passed/0 failed/6 existing ignored, exit0, 320.260691s wall/370.516022s CPU. Includes all final11 K93 tests. Earlier initial full-reference also passed728/0/6 before the two additional tests.
- GREEN complete conformance: python3 .tmp/isa-k93/run.py full-conformance cargo test --offline -j4 --manifest-path .tmp/isa-k93/test-layout/repo/conformance/Cargo.toml -- --test-threads=4 =>131 passed/0 failed/0 ignored, exit0, 472.958848s wall/807.571781s CPU. All291 K93 CLI cases executed; none unavailable. Existing staged-suite status remains distinct from this crate-test result.
- python3 -I conformance/fixtures/accepted-k93-09/generate.py --ref /home/tobias/Projects/bennett-workspace/bennett-isa-spec-job-isa-k93/.tmp/isa-k93/target/debug/bennett-isa-ref --check =>11 relations/291 CLI vectors match.
- python3 -I conformance/tools/ref_catalog.py --check =>219 recipes, unchanged envelope5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197, exit0 (catalog.json/log receipt).
- cargo fmt --manifest-path reference-interpreter/Cargo.toml --check; cargo fmt --manifest-path conformance/Cargo.toml --check; git diff --check =>all exit0.

Conformance test environment: draft_witnesses.py:178/228 hard-code reference-interpreter/target, :272 hard-codes sibling review. An exact1077-file source snapshot under owned .tmp supplies those paths without editing SET B. conformance-snapshot.json records every SHA256; all source digests still match HEAD. Snapshot spec/include are read-only links; current binary is the job target; review binary is linked from gate.toml's cache at8d9a5c60aff9aa35b44eb3ac1c541c020f24d737 (cache HEAD confirmed), not an unpinned sibling checkout. No tests altered or skipped.

Resources: nproc64 and MemAvailable about52GiB, reserve16 threads/16GiB and split remainder across four lanes, 2GiB per worker =>4 build/test workers. Repo has no hang-guard class table/profile at this pin; runner inherits existing gate.toml cargo-test1800s guard, recording wall/CPU and UNKNOWN=124 on timeout. No trip. Receipts and logs are .tmp/isa-k93/<label>.json/.log.

Next: orchestrator fresh sol/astra/Muse council review of head1cf5a7e, then one full landing gate on that head, bead export and merge. Do not run a full gate in this child. No remaining implementation work, external-path need, text defect or open job bead.

## Source diff
```diff
diff --git a/reference-interpreter/src/action.rs b/reference-interpreter/src/action.rs
index eb0dfad..3cc3b7c 100644
--- a/reference-interpreter/src/action.rs
+++ b/reference-interpreter/src/action.rs
@@ -438,7 +438,11 @@ impl Object {
                 let mut angle = None;
                 if op == "mcx" {
                     for n in list(&a[0])? {
-                        wires.push(e.scalar(&n)?);
+                        if self.isa_version == crate::IsaVersion::V09 {
+                            wires.extend(e.bundle(&n)?);
+                        } else {
+                            wires.push(e.scalar(&n)?);
+                        }
                     }
                     wires.push(e.scalar(&a[1])?);
                 } else if matches!(op, "rx" | "ry" | "rz") {
diff --git a/reference-interpreter/src/borrow.rs b/reference-interpreter/src/borrow.rs
index ada9da3..4acf06b 100644
--- a/reference-interpreter/src/borrow.rs
+++ b/reference-interpreter/src/borrow.rs
@@ -930,7 +930,15 @@ impl Compiler<'_> {
                     let (controls, targets, diagonal, other) = gate_operands(i)?;
                     let mut c = effective.clone();
                     for control in &controls {
-                        c = with(&[(self.scalar(control)?, true)], &c);
+                        let wires =
+                            if op == "mcx" && self.object.isa_version == crate::IsaVersion::V09 {
+                                self.bundle(control)?
+                            } else {
+                                vec![self.scalar(control)?]
+                            };
+                        for wire in wires {
+                            c = with(&[(wire, true)], &c);
+                        }
                     }
                     let targets = targets
                         .iter()
diff --git a/reference-interpreter/src/source_constructor/action.rs b/reference-interpreter/src/source_constructor/action.rs
index 919c44a..836b799 100644
--- a/reference-interpreter/src/source_constructor/action.rs
+++ b/reference-interpreter/src/source_constructor/action.rs
@@ -382,10 +382,12 @@ impl Compiler<'_> {
                             ("params", array([angle])),
                         ])
                     } else if op == "mcx" {
-                        let mut wires = crate::object::list(&a[0])?
-                            .iter()
-                            .map(|n| env.wire(n))
-                            .collect::<Result<Vec<_>>>()?;
+                        let mut wires = Vec::new();
+                        for name in crate::object::list(&a[0])? {
+                            for index in 0..env.width(&name)? {
+                                wires.push(env.indexed(&name, index)?);
+                            }
+                        }
                         wires.push(env.wire(&a[1])?);
                         gate(op, wires)
                     } else if matches!(
diff --git a/reference-interpreter/src/validation.rs b/reference-interpreter/src/validation.rs
index 9db9101..e46737c 100644
--- a/reference-interpreter/src/validation.rs
+++ b/reference-interpreter/src/validation.rs
@@ -600,7 +600,16 @@ impl Object {
                     {
                         return err("§3.3", "gate angle must be a classical f64 argument");
                     }
-                    let (controls, targets, diagonal, other) = gate_operands(i)?;
+                    let (mut controls, targets, diagonal, other) = gate_operands(i)?;
+                    if op == "mcx" && self.isa_version == crate::IsaVersion::V09 {
+                        // §4.4: expand each entry before checking distinctness;
+                        // neither source operands nor their order are rewritten.
+                        controls = controls
+                            .iter()
+                            .map(|name| s.wires(name))
+                            .collect::<Result<Vec<_>>>()?
+                            .concat();
+                    }
                     if f.kind == "perm_action" && (diagonal || other) {
                         return err("§5.3", "permutation action contains non-permutation gate");
                     }
```

## Test diff
```diff
diff --git a/conformance/tests/k93_vectors.rs b/conformance/tests/k93_vectors.rs
new file mode 100644
index 0000000..add8733
--- /dev/null
+++ b/conformance/tests/k93_vectors.rs
@@ -0,0 +1,30 @@
+use bennett_isa_conformance::{cases_dir, default_bin, json, load_cases, run_case, Outcome};
+use std::collections::BTreeSet;
+
+#[test]
+fn all_k93_portable_vectors_run_against_the_published_cli() {
+    let manifest = json::parse(include_str!("../fixtures/accepted-k93-09/k93.json")).unwrap();
+    let ids = manifest
+        .get("conformance_cases")
+        .unwrap()
+        .as_arr()
+        .unwrap()
+        .iter()
+        .map(|v| v.as_str().unwrap().to_string())
+        .collect::<BTreeSet<_>>();
+    assert_eq!(ids.len(), 291);
+    let temporary = std::path::PathBuf::from(std::env::var("TMPDIR").unwrap()).join("k93-harness");
+    std::fs::create_dir_all(&temporary).unwrap();
+    let mut seen = BTreeSet::new();
+    for case in load_cases(&cases_dir())
+        .unwrap()
+        .iter()
+        .filter(|c| ids.contains(&c.id))
+    {
+        let outcome = run_case(&default_bin(), case, &temporary);
+        assert!(matches!(outcome, Outcome::Pass), "{}: {outcome:?}", case.id);
+        assert!(case.unavailable.is_none());
+        seen.insert(case.id.clone());
+    }
+    assert_eq!(seen, ids);
+}
diff --git a/reference-interpreter/tests/isa09_mcx_bundles.rs b/reference-interpreter/tests/isa09_mcx_bundles.rs
new file mode 100644
index 0000000..3140864
--- /dev/null
+++ b/reference-interpreter/tests/isa09_mcx_bundles.rs
@@ -0,0 +1,365 @@
+mod support;
+use bennett_isa_conformance::{
+    ref_amplitudes::{column, Complex as ExactComplex},
+    ref_language::Leaf,
+};
+use bennett_isa_ref::{json::Json, ref_library::Value, Object, QuantumBindings, QuantumState};
+use std::path::PathBuf;
+
+const MANIFEST: &str = include_str!("../../conformance/fixtures/accepted-k93-09/k93.json");
+fn fixture(name: &str) -> String {
+    std::fs::read_to_string(
+        PathBuf::from(env!("CARGO_MANIFEST_DIR"))
+            .join("../conformance/fixtures/accepted-k93-09")
+            .join(name),
+    )
+    .unwrap()
+}
+fn strings(value: &Json) -> Vec<String> {
+    value
+        .array()
+        .unwrap()
+        .iter()
+        .map(|v| v.string().unwrap().into())
+        .collect()
+}
+fn integers(value: &Json) -> Vec<usize> {
+    value
+        .array()
+        .unwrap()
+        .iter()
+        .map(|v| v.uint().unwrap() as usize)
+        .collect()
+}
+fn coordinates(values: &[usize], widths: &[usize]) -> Vec<bool> {
+    values
+        .iter()
+        .zip(widths)
+        .flat_map(|(v, w)| (0..*w).map(move |i| v >> i & 1 == 1))
+        .collect()
+}
+fn basis(values: &[usize], widths: &[usize]) -> usize {
+    coordinates(values, widths)
+        .iter()
+        .enumerate()
+        .fold(0, |v, (i, b)| v | (usize::from(*b) << i))
+}
+fn prepared(
+    names: &[String],
+    widths: &[usize],
+    values: &[usize],
+) -> (QuantumState, QuantumBindings) {
+    let mut q = QuantumState::new();
+    let mut bindings = QuantumBindings::default();
+    for ((name, width), value) in names.iter().zip(widths).zip(values) {
+        let wires = q.allocate(*width).unwrap();
+        for (i, wire) in wires.iter().enumerate() {
+            if value >> i & 1 == 1 {
+                q.gate("x", &[*wire], None, &[]).unwrap();
+            }
+        }
+        bindings.bundles.insert(name.clone(), wires);
+    }
+    (q, bindings)
+}
+fn leaves(object: &Object, names: &[String], widths: &[usize], adjoint: bool) -> Vec<Leaf> {
+    let args = names
+        .iter()
+        .map(|n| Value::Str(n.clone()))
+        .collect::<Vec<_>>();
+    let bundles = names
+        .iter()
+        .zip(widths)
+        .map(|(n, w)| (n.as_str(), *w))
+        .collect::<Vec<_>>();
+    object
+        .expand_action_source("a", &args, &bundles, adjoint)
+        .unwrap()
+}
+
+#[test]
+fn every_published_basis_column_and_adjoint_has_exact_positive_unit_amplitude() {
+    let manifest = Json::parse(MANIFEST).unwrap();
+    for vector in manifest.get("vectors").unwrap().array().unwrap() {
+        let object = support::rehash(&fixture(vector.get("object").unwrap().string().unwrap()));
+        let names = strings(vector.get("names").unwrap());
+        let widths = integers(vector.get("widths").unwrap());
+        for row in vector.get("rows").unwrap().array().unwrap() {
+            let before = integers(row.get("before").unwrap());
+            let after = integers(row.get("after").unwrap());
+            for adjoint in [false, true] {
+                let (input, output) = if adjoint {
+                    (&after, &before)
+                } else {
+                    (&before, &after)
+                };
+                let (mut q, bindings) = prepared(&names, &widths, input);
+                object
+                    .execute_action("a", &mut q, &bindings, adjoint, &[])
+                    .unwrap();
+                assert_eq!(
+                    q.exact_support(),
+                    vec![(coordinates(output, &widths), (1.0, 0.0))],
+                    "{} adj={adjoint}",
+                    vector.canonical()
+                );
+            }
+        }
+    }
+}
+
+#[test]
+fn source_adapter_columns_match_independent_formula_vectors_in_both_directions() {
+    let manifest = Json::parse(MANIFEST).unwrap();
+    for vector in manifest.get("vectors").unwrap().array().unwrap() {
+        let object = support::rehash(&fixture(vector.get("object").unwrap().string().unwrap()));
+        let names = strings(vector.get("names").unwrap());
+        let widths = integers(vector.get("widths").unwrap());
+        let wires = names
+            .iter()
+            .zip(&widths)
+            .flat_map(|(n, w)| (0..*w).map(move |i| (n.clone(), i)))
+            .collect::<Vec<_>>();
+        for adjoint in [false, true] {
+            let expanded = leaves(&object, &names, &widths, adjoint);
+            for row in vector.get("rows").unwrap().array().unwrap() {
+                let before = integers(row.get("before").unwrap());
+                let after = integers(row.get("after").unwrap());
+                let (input, output) = if adjoint {
+                    (&after, &before)
+                } else {
+                    (&before, &after)
+                };
+                let mut expected = vec![ExactComplex::default(); 1 << wires.len()];
+                expected[basis(output, &widths)] = ExactComplex::one();
+                assert_eq!(
+                    column(&expanded, &wires, basis(input, &widths)).unwrap(),
+                    expected,
+                    "{} adj={adjoint}",
+                    vector.canonical()
+                );
+            }
+        }
+    }
+}
+
+#[test]
+fn mixed_written_order_and_active_predicate_have_k3_four_operands_and_c4() {
+    let names = ["t", "r", "s", "b"].map(String::from);
+    let object = support::rehash(&fixture("predicate.bisa"));
+    let expanded = leaves(&object, &names, &[1, 1, 1, 2], false);
+    assert_eq!(expanded.len(), 1);
+    assert_eq!(expanded[0].gate, "mcx");
+    assert_eq!(
+        expanded[0].wires,
+        vec![
+            ("s".into(), 0),
+            ("b".into(), 0),
+            ("b".into(), 1),
+            ("t".into(), 0)
+        ]
+    );
+    assert_eq!(expanded[0].controls, vec![("r".into(), 0)]);
+    assert_eq!(expanded[0].wires.len() - 1, 3);
+    assert_eq!(expanded[0].wires.len() - 1 + expanded[0].controls.len(), 4);
+    assert_eq!(
+        expanded[0].source.as_ref().unwrap().terminal.point,
+        "entry:1"
+    );
+    let names = ["t", "s", "b"].map(String::from);
+    let first = support::rehash(&fixture("mixed-sb.bisa"));
+    let second = support::rehash(&fixture("mixed-bs.bisa"));
+    let a = leaves(&first, &names, &[1, 1, 2], false);
+    let b = leaves(&second, &names, &[1, 1, 2], false);
+    assert_eq!(
+        a[0].wires,
+        vec![
+            ("s".into(), 0),
+            ("b".into(), 0),
+            ("b".into(), 1),
+            ("t".into(), 0)
+        ]
+    );
+    assert_eq!(
+        b[0].wires,
+        vec![
+            ("b".into(), 0),
+            ("b".into(), 1),
+            ("s".into(), 0),
+            ("t".into(), 0)
+        ]
+    );
+    assert_ne!(
+        first.identity().unwrap().object_hash,
+        second.identity().unwrap().object_hash
+    );
+    assert_ne!(
+        first.identity().unwrap().closure_hashes,
+        second.identity().unwrap().closure_hashes
+    );
+    assert_eq!(
+        a[0].source.as_ref().unwrap().terminal.point,
+        b[0].source.as_ref().unwrap().terminal.point
+    );
+}
+
+#[test]
+fn original_witness_retains_published_byte_identities() {
+    let object = Object::parse(&fixture("witness.bisa")).unwrap();
+    object.check_hashes().unwrap();
+    let id = object.identity().unwrap();
+    assert_eq!(
+        id.object_hash,
+        "db3d3f92a79077074901449d83532f1a0d82ef1621bd833adb7ad14d1aedd467"
+    );
+    assert_eq!(
+        id.closure_hashes["a"].as_deref(),
+        Some("e38d5da64f9a0ae89a66243bcbe5a321cb807a5bbabf83952b63d3465dfab346")
+    );
+    let library = object.bound_ref_library().unwrap();
+    assert_eq!(
+        library.hash(),
+        "5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197"
+    );
+}
+
+#[test]
+fn external_reference_coherence_preserves_both_exact_prepared_amplitudes() {
+    let object = Object::parse(&fixture("witness.bisa")).unwrap();
+    let mut q = QuantumState::new();
+    let wires = q.allocate(5).unwrap(); // p,q,c0,c1,R
+    q.gate("h", &[wires[4]], None, &[]).unwrap();
+    q.gate("cx", &[wires[4], wires[2]], None, &[]).unwrap();
+    q.gate("cx", &[wires[4], wires[3]], None, &[]).unwrap();
+    let before = q.clone();
+    // §4.4 H and the §15 witness give 1/sqrt(2) independently of execution.
+    let amplitude = (std::f64::consts::FRAC_1_SQRT_2, 0.0);
+    assert_eq!(
+        q.exact_support(),
+        vec![
+            (vec![false; 5], amplitude),
+            (vec![false, false, true, true, true], amplitude)
+        ]
+    );
+    let mut bindings = QuantumBindings::default();
+    bindings.bundles.insert("p".into(), vec![wires[0]]);
+    bindings.bundles.insert("q".into(), vec![wires[1]]);
+    bindings.bundles.insert("c".into(), wires[2..4].to_vec());
+    object
+        .execute_action("a", &mut q, &bindings, false, &[])
+        .unwrap();
+    assert_eq!(
+        q.exact_support(),
+        vec![
+            (vec![false; 5], amplitude),
+            (vec![true, false, true, true, true], amplitude)
+        ]
+    );
+    object
+        .execute_action("a", &mut q, &bindings, true, &[])
+        .unwrap();
+    assert_eq!(q, before);
+}
+
+#[test]
+fn repeated_controls_overlap_and_non_scalar_or_dead_targets_reject_as_operands() {
+    for name in [
+        "repeated-bundle",
+        "repeated-scalar",
+        "target-overlap",
+        "scalar-target-overlap",
+        "multiwire-target",
+        "dead-target",
+        "target-out-of-range",
+    ] {
+        let error = Object::parse(&fixture(&format!("{name}.bisa"))).expect_err(name);
+        assert!(error.to_string().contains("§3.3"), "{name}: {error}");
+    }
+}
+
+#[test]
+fn resolved_aliases_reject_before_any_gate_executes() {
+    let object = support::rehash(&fixture("mixed-sb.bisa"));
+    let names = ["t", "s", "b"].map(String::from);
+    let (mut q, mut bindings) = prepared(&names, &[1, 1, 2], &[0, 1, 3]);
+    bindings
+        .bundles
+        .insert("s".into(), vec![bindings.bundles["b"][0]]);
+    let before = q.clone();
+    let error = object
+        .execute_action("a", &mut q, &bindings, false, &[])
+        .unwrap_err();
+    assert!(error.to_string().contains("§3.3"));
+    assert_eq!(q, before);
+}
+
+#[test]
+fn k78_matches_complete_control_sets_after_bundle_expansion() {
+    let object = Object::parse(&fixture("causal-same-controls.bisa")).unwrap();
+    object.check_hashes().unwrap();
+    // c=0 follows from two matching resolved flips. The subsequent frame
+    // may touch arbitrary d only if K78 supplied that exact entry fact.
+    let error = Object::parse(&fixture("causal-different-controls.bisa"))
+        .expect_err("different effective controls cannot match");
+    assert!(error.to_string().contains("§5.6"), "{error}");
+}
+
+#[test]
+fn rechecked_certificate_proves_all_controls_and_rejects_stale_first_bit_relation() {
+    let closure = "e38d5da64f9a0ae89a66243bcbe5a321cb807a5bbabf83952b63d3465dfab346";
+    let corrected = Object::parse(&fixture("witness-certified.bisa")).unwrap();
+    corrected.check_hashes().unwrap();
+    assert_eq!(
+        corrected.verify_claim(closure, 0).unwrap(),
+        bennett_isa_ref::ClaimVerdict::Proof
+    );
+    let stale = Object::parse(&fixture("witness-firstbit-certificate.bisa")).unwrap();
+    stale.check_hashes().unwrap(); // identical source hashes do not prove the table
+    let error = stale.verify_claim(closure, 0).unwrap_err();
+    assert!(error.to_string().contains("full tuple mismatch"), "{error}");
+    assert_eq!(
+        corrected.identity().unwrap().object_hash,
+        stale.identity().unwrap().object_hash
+    );
+}
+
+#[test]
+fn cached_callee_transfer_remaps_complete_bundle_for_each_actual_binding() {
+    let root = r#"{"abi":"0.9","args":[],"bounds":[],"in":[2,2],"kind":"action","mem":[],"mut":[1],"tier":"q"}"#;
+    let child = r#"{"abi":"0.9","args":[],"bounds":[],"in":[2],"kind":"perm_action","mem":[],"mut":[1],"tier":"q"}"#;
+    let body = "action @a (t:wire mut) (b:wire[2] in, c:wire[2] in) () () ()\n^entry():\nd = qborrow any 1\naction_call @g (d) (b) () ()\naction_call @g (d) (b) () ()\nqreturn d";
+    let source = support::object(
+        &[
+            ("a", root, body),
+            (
+                "g",
+                child,
+                "perm_action @g (t:wire mut) (b:wire[2] in) () () ()\n^entry():\nmcx (b) t",
+            ),
+        ],
+        "{}",
+        "",
+    )
+    .replace("=0.8", "=0.9");
+    support::rehash(&source).check_hashes().unwrap();
+    // The callee is cached on its first use. A different second actual must
+    // retain both c bits, rather than reusing the first call's b mapping.
+    let wrong = source.replacen(
+        "action_call @g (d) (b) () ()\nqreturn d",
+        "action_call @g (d) (c) () ()\nqreturn d",
+        1,
+    );
+    let error = Object::parse(&wrong).expect_err("independent conjunctions cannot restore d");
+    assert!(error.to_string().contains("§5.6"), "{error}");
+}
+
+#[test]
+fn isa08_scalar_admission_stays_unchanged() {
+    let source = fixture("width-2.bisa")
+        .replace("=0.9", "=0.8")
+        .replace("\"0.9\"", "\"0.8\"");
+    assert!(Object::parse(&source)
+        .unwrap_err()
+        .to_string()
+        .contains("§3.3"));
+}
```

## Vector files added/changed
     conformance/cases/C/C-k93-witness-11-fwd/case.json                     |  37 +++++++++++++++++++++
     conformance/cases/C/C-k93-witness-12-adj/case.json                     |  38 ++++++++++++++++++++++
     conformance/cases/C/C-k93-witness-12-fwd/case.json                     |  37 +++++++++++++++++++++
     conformance/cases/C/C-k93-witness-13-adj/case.json                     |  38 ++++++++++++++++++++++
     conformance/cases/C/C-k93-witness-13-fwd/case.json                     |  37 +++++++++++++++++++++
     conformance/cases/C/C-k93-witness-14-adj/case.json                     |  38 ++++++++++++++++++++++
     conformance/cases/C/C-k93-witness-14-fwd/case.json                     |  37 +++++++++++++++++++++
     conformance/cases/C/C-k93-witness-15-adj/case.json                     |  38 ++++++++++++++++++++++
     conformance/cases/C/C-k93-witness-15-fwd/case.json                     |  37 +++++++++++++++++++++
     conformance/cases/C/C-k93-witness-2-adj/case.json                      |  38 ++++++++++++++++++++++
     conformance/cases/C/C-k93-witness-2-fwd/case.json                      |  37 +++++++++++++++++++++
     conformance/cases/C/C-k93-witness-3-adj/case.json                      |  38 ++++++++++++++++++++++
     conformance/cases/C/C-k93-witness-3-fwd/case.json                      |  37 +++++++++++++++++++++
     conformance/cases/C/C-k93-witness-4-adj/case.json                      |  38 ++++++++++++++++++++++
     conformance/cases/C/C-k93-witness-4-fwd/case.json                      |  37 +++++++++++++++++++++
     conformance/cases/C/C-k93-witness-5-adj/case.json                      |  38 ++++++++++++++++++++++
     conformance/cases/C/C-k93-witness-5-fwd/case.json                      |  37 +++++++++++++++++++++
     conformance/cases/C/C-k93-witness-6-adj/case.json                      |  38 ++++++++++++++++++++++
     conformance/cases/C/C-k93-witness-6-fwd/case.json                      |  37 +++++++++++++++++++++
     conformance/cases/C/C-k93-witness-7-adj/case.json                      |  38 ++++++++++++++++++++++
     conformance/cases/C/C-k93-witness-7-fwd/case.json                      |  37 +++++++++++++++++++++
     conformance/cases/C/C-k93-witness-8-adj/case.json                      |  38 ++++++++++++++++++++++
     conformance/cases/C/C-k93-witness-8-fwd/case.json                      |  37 +++++++++++++++++++++
     conformance/cases/C/C-k93-witness-9-adj/case.json                      |  38 ++++++++++++++++++++++
     conformance/cases/C/C-k93-witness-9-fwd/case.json                      |  37 +++++++++++++++++++++
     conformance/cases/F/F-k93-causal-different-controls/case.json          |  18 +++++++++++
     conformance/cases/F/F-k93-causal-same-controls/case.json               |  17 ++++++++++
     conformance/cases/F/F-k93-dead-target/case.json                        |  18 +++++++++++
     conformance/cases/F/F-k93-multiwire-target/case.json                   |  18 +++++++++++
     conformance/cases/F/F-k93-repeated-bundle/case.json                    |  18 +++++++++++
     conformance/cases/F/F-k93-repeated-scalar/case.json                    |  18 +++++++++++
     conformance/cases/F/F-k93-scalar-target-overlap/case.json              |  18 +++++++++++
     conformance/cases/F/F-k93-target-out-of-range/case.json                |  18 +++++++++++
     conformance/cases/F/F-k93-target-overlap/case.json                     |  18 +++++++++++
     conformance/fixtures/accepted-k93-09/README.md                         |  54 +++++++++++++++++++++++++++++++
     conformance/fixtures/accepted-k93-09/causal-different-controls.bisa    |  17 ++++++++++
     conformance/fixtures/accepted-k93-09/causal-same-controls.bisa         |  17 ++++++++++
     conformance/fixtures/accepted-k93-09/dead-target.bisa                  |   9 ++++++
     conformance/fixtures/accepted-k93-09/empty-predicate.bisa              |  11 +++++++
     conformance/fixtures/accepted-k93-09/empty.bisa                        |   9 ++++++
     conformance/fixtures/accepted-k93-09/generate.py                       | 212 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
     conformance/fixtures/accepted-k93-09/indexed-target.bisa               |   9 ++++++
     conformance/fixtures/accepted-k93-09/k93.json                          |   1 +
     conformance/fixtures/accepted-k93-09/mixed-bs.bisa                     |   9 ++++++
     conformance/fixtures/accepted-k93-09/mixed-sb.bisa                     |   9 ++++++
     conformance/fixtures/accepted-k93-09/multiwire-target.bisa             |   9 ++++++
     conformance/fixtures/accepted-k93-09/predicate.bisa                    |  11 +++++++
     conformance/fixtures/accepted-k93-09/repeated-bundle.bisa              |   9 ++++++
     conformance/fixtures/accepted-k93-09/repeated-scalar.bisa              |   9 ++++++
     conformance/fixtures/accepted-k93-09/scalar-target-overlap.bisa        |   9 ++++++
     conformance/fixtures/accepted-k93-09/target-out-of-range.bisa          |   9 ++++++
     conformance/fixtures/accepted-k93-09/target-overlap.bisa               |   9 ++++++
     conformance/fixtures/accepted-k93-09/width-1.bisa                      |   9 ++++++
     conformance/fixtures/accepted-k93-09/width-2.bisa                      |   9 ++++++
     conformance/fixtures/accepted-k93-09/width-3.bisa                      |   9 ++++++
     conformance/fixtures/accepted-k93-09/wire1-target.bisa                 |   9 ++++++
     conformance/fixtures/accepted-k93-09/witness-certified.bisa            |  13 ++++++++
     conformance/fixtures/accepted-k93-09/witness-firstbit-certificate.bisa |  13 ++++++++
     conformance/fixtures/accepted-k93-09/witness.bisa                      |  10 ++++++
     316 files changed, 11164 insertions(+)
