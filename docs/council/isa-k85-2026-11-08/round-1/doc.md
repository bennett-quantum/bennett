# K85 candidate packet: bennett-isa-spec job/isa-k85 62a0cf0..a0b49a0 (commits 4a6d20c, 6e0a3ce, a0b49a0)

Implements ISA 0.9 K85 (§12.2 fixed-image claims) in the reference interpreter and publishes K85 conformance vectors (bead b-isa-spec-qrc). The implementer ended JOB-BLOCKED: conditional numerical/channel checking (J_I-restricted maps) and executable preparation/native bindings are NOT implemented (text-defect bead bennett-isa-spec-rqn: payloads have no conditional domain; §12.3 has no preparation-witness encoding). Grade what exists for fidelity; grade whether every unimplemented part fails loud (unverified/unestablished, never a silent pass) and is truthfully declared.

## Implementer PROGRESS.md (verbatim)

# Resume

Done: read brief, COMMON.md, T3CHILD.md, CLAUDE.md, AGENTS.md, HANDOFF.md and Beads skill in full. Branch job/isa-k85 is at 62a0cf0; only owned paths will change. Old origin/wip/sol-isa-k85 is the published-text change 57151aa, not a prior implementation. Its .tmp notes are absent here.

Ownership update (orchestrator 2026-11-08T11:37Z): SET B only; another writer owns validation.rs, action.rs, source_constructor/action.rs, borrow.rs, isa09_mcx_bundles.rs and all K93 vector paths. main.rs, cli_mem_file.rs and other K vector paths remain excluded. Do not change those paths. Current 4a6d20c changes comply. .tmp/isa-k85 remains the private progress/receipt area.

Baseline inventory (ISA 0.9 K85, quoted normative clauses):

| Clause | Existing behaviour at 62a0cf0 | Gap |
| --- | --- | --- |
| 4355–4361: “name resolves ... to an in-role interface region”; “Each resolved fixed region occurs exactly once” | claims/images09.rs:47–80 resolves shapes, roles, duplicates and ranged overlap | Dedicated portable shape/role/duplicate vectors and tests |
| 4363–4370: “Cell i consists of bits [iW,(i+1)W)”; “hashes independently” | claims/images09.rs:81–149 checks byte length, lowercase, padding, raw SHA256; unpacks cells | Non-byte packing, swapped/stale/hex-text vectors |
| 4372–4383: “exactly one outcome, in this order”; “Successful sampled claims always receive evidence” | claims/replay09.rs:475–503 classifies replay and enforces two requested labels | Full outcome/request matrix, omitted varying components, complete-sampling vectors; label enforcement bypasses structural/inverse-pair results |
| 4385–4393: “Coverage remains exact n/\|D\|”; “ordered resolved ... bindings” | claims/replay09.rs:24–81 computes exact coverage; images09.rs uses signature-order BTreeMap | mem slot identities not explicit; scheduled contexts remain staged |
| 4397–4405: “requires checked preparation/binding”; “Without that preparation evidence ... does not discharge the invocation” | claims.rs:43–44 documents conditional theorem only | No preparation encoding/checker/applicability report |
| 4407–4413: “cannot discharge an unrestricted borrow-frame, inverse-pair”; “exact +1 ... full-tuple ... external-reference” | claims.rs:957–975 requires Proof for borrow frames; pairs09.rs:164 rejects fixed images; replay09.rs executes complete tuples with exact phase/clean workspace | Controlled/dirty/phase/reference portable vectors |
| 4416–4417: “signature order using mem slot identities”; “Fixed regions do not add an enumeration component” | images09.rs orders resolved group/slot; replay09.rs:197–217 appends singleton fixed cells to enumerated components | Separate fixed-cell population from enumeration and expose mem slot id |
| 4080–4089: “apply ... to (U−V)J_I”; “reduced input dimension and complete output dimension” | claims.rs:869–872 returns staged Unverified for every numerical/channel claim | Entire rigorous interval and target/schedule executor absent; closed schema has no conditional domain |
| 4505–4521: “selected ... transitive device closures”; “corresponding materialized marked entry” | No native manifest/comparison executor | Outside interpreter source execution; record contract/API prerequisites, do not claim implementation |

Done: 30 portable object vectors (including both independent 64-row 0102/0201 relations), 28 suite-D admission cases, a separate exact restricted-map vector, an independent conformance reader and seven reference integration tests. Centralised successful-label checking, removed fixed cells from enumeration and added explicit mem:N binding identities. Public source/interface/closure/object identities stay unchanged between image certificates. Existing closed 0.9 grammar already supported images; added explicit 0.8/0.9 closed-schema tests instead of widening it.

Verified (private run.py adds headless env, private TMPDIR/target, four build jobs and hang guard; receipts carry exact argv/wall/CPU):
- baseline-build: cargo build --offline --manifest-path reference-interpreter/Cargo.toml, exit 0.
- red-baseline: cargo test --offline --manifest-path .tmp/isa-k85/tmp/baseline/reference-interpreter/Cargo.toml --test isa09_fixed_image -- --test-threads=4, exit 101: five pass, one intended structural requested-label failure. Archive is exact 62a0cf0 plus new tests/vectors.
- red-enumeration: same baseline crate with --lib fixed_cells_never_become_enumeration_components, exit 101: expected 3 enumeration components, found 5.
- green-reference: cargo test --offline --manifest-path reference-interpreter/Cargo.toml --test isa09_fixed_image --test isa09_claim_replay --test isa09_certificate --lib -- --test-threads=4, exit 0 (all passing).
- green-final-fixed: final generated-vector manifest, seven tests pass, exit 0.
- green-conformance: cargo test --offline --manifest-path conformance/Cargo.toml --test ref_k85 --test case_data -- --test-threads=4, six pass, exit 0.
- Both cargo fmt invocations and git diff --check pass. No scripts/quality.py exists or is invoked by gate.toml.

Open: b-isa-spec-qrc remains IN_PROGRESS and now depends on text-defect bennett-isa-spec-rqn. The published numerical/channel payloads (spec lines 3839–3840) have no conditional domain and §12.3 has no checked preparation witness encoding, despite lines 4080–4089 and 4397–4405 requiring them. Existing staged rigorous interval/realised-schedule checks remain Unverified. Native selected transitive-closure manifest/comparison and executable image preparation are not implemented. The independent Z/I map vector is not an executable certificate. No main.rs change is required for the public Rust checker APIs used here; CLI check remains admission-only and no CLI report/replay is claimed. No full gate will run (orchestrator owns it).

Commits 4a6d20c (interpreter and portable vectors), 6e0a3ce (phase-sensitive independent map case), and a0b49a0 (private-target/pinned witness helper) are backed up to origin wip/isa-k85. The later commits change only conformance tests/map data/generator/docs; reference source and its included object vectors stayed unchanged after the full reference run began. Full reference crate run passed: 728 passed, six existing ignores, exit 0; 338.49s wall, 523.92s CPU, 1590976KiB peak RSS (full-reference.log/.receipt). Verified at 6e0a3ce: both crates pass cargo fmt -- --check and cargo clippy --offline --manifest-path <crate>/Cargo.toml --lib --bins -- -D warnings (clippy-reference/conformance receipts). Final CLI rebuilt, its SHA256 is conformance-binary.sha256. Generator --check passes (final-vectors-check receipt). Updated phase-sensitive map test passes (two tests, phase-vector-check receipt). First full conformance run (full-conformance.log/.receipt) exited 101 after finding draft_witnesses.py ignored BENNETT_CONFORMANCE_BIN and used an unpinned sibling path. This was a fixture/harness setup failure, not a completed green run. Fixed in a0b49a0 (owned generic conformance/tests helper only): current binary follows BENNETT_CONFORMANCE_BIN; review binary resolves exact gate.toml SHA through the gate symlink/cache, verifies HEAD and tracked cleanliness, and retains all existing semantic assertions. Focused cargo test --offline --manifest-path conformance/Cargo.toml --test draft_contracts -- --test-threads=4 passed (one test, green-witness receipt). Finding bennett-isa-spec-6qk was filed and closed with that evidence. Third commit backed up to wip/isa-k85. Full conformance rerun passed at a0b49a0: 132 passed, zero failed/ignored, exit 0; 476.35s wall, 788.12s CPU, 726584KiB peak RSS (full-conformance-final.log/.receipt). Final tracked working tree is clean; only private .tmp evidence is untracked. Remote wip/isa-k85 was verified to equal a0b49a0646c56955b0e89e126b865965c5a82599. Final evidence verified at 2026-11-08T11:56:51Z. Next: orchestrator full gate and council on the final head; resolve rqn then implement the remaining rigorous conditional checker, preparation/applicability and selected native closure comparison before closing qrc. No rebase, merge, main push, .beads commit, excluded SET A edit or CLI/main.rs edit was performed. Orchestrator retains full gate/council review and the remaining contract-dependent implementation. Parent qrc must not be closed.

Execution policy: no repo hang-guard class table or machine profile exists at this baseline. Derive private classes from docs/quality.md measured runs (reference 279s, conformance 482s, cold compile 180s), at >=10x (short 1800s, moderate 6000s, long 12000s); guard exit 124 is UNKNOWN. Host has 64 threads and ~47GiB MemAvailable; cap this job to four build jobs/four test threads, leaving >=16 threads/16GiB. Commands unset display/browser variables, use private TMPDIR and CARGO_TARGET_DIR; guard records wall and child CPU.

Red evidence note: red-fixed.log was an early invalid fixture draft (extra blank line), not a claimed semantic red. The authoritative before-fix failures are red-baseline.log and red-enumeration.log against the exact archived baseline.

## Source diff (reference-interpreter/src)
```diff
diff --git a/reference-interpreter/src/claims.rs b/reference-interpreter/src/claims.rs
index 819b7ba..8be74f2 100644
--- a/reference-interpreter/src/claims.rs
+++ b/reference-interpreter/src/claims.rs
@@ -47,6 +47,31 @@ pub enum ClaimVerdict {
     /// Not checkable by this crate yet; the reason names the missing machinery.
     Unverified(String),
 }
+
+/// §12.2 K85: requests constrain the independently computed successful
+/// category. An unchecked claim has no successful category to advertise.
+fn check_requested_label(claim: &Json, verdict: &ClaimVerdict) -> Result<()> {
+    if matches!(verdict, ClaimVerdict::Unverified(_)) {
+        return Ok(());
+    }
+    let requested = claim.object()?.get("label").map(Json::string).transpose()?;
+    let matches = match requested {
+        None | Some("evidence") => true,
+        Some("proof") => *verdict == ClaimVerdict::Proof,
+        Some("proof_relative_to_image") => *verdict == ClaimVerdict::ProofRelativeToImage,
+        Some(other) => return err("§12.2 K85", format!("unknown requested label {other}")),
+    };
+    if !matches {
+        return err(
+            "§12.2 K85",
+            format!(
+                "requested {} differs from computed outcome",
+                requested.unwrap()
+            ),
+        );
+    }
+    Ok(())
+}
 #[derive(Clone, Debug, PartialEq, Eq)]
 pub struct CertificateReport {
     pub claims: Vec<ClaimReport>,
@@ -682,7 +707,21 @@ impl Object {
         if !active.insert((closure.to_string(), index)) {
             return err("§12", "cyclic claim reference");
         }
-        let result = self.verify_claim_inner(closure, index, active);
+        let result = self
+            .verify_claim_inner(closure, index, active)
+            .and_then(|verdict| {
+                let claim = &self
+                    .section("certificate")
+                    .unwrap()
+                    .get("regions")?
+                    .get(closure)?
+                    .get("claims")?
+                    .array()?[index];
+                if self.isa_version == crate::IsaVersion::V09 {
+                    check_requested_label(claim, &verdict)?;
+                }
+                Ok(verdict)
+            });
         active.remove(&(closure.to_string(), index));
         result
     }
diff --git a/reference-interpreter/src/claims/images09.rs b/reference-interpreter/src/claims/images09.rs
index c02f4d7..949a635 100644
--- a/reference-interpreter/src/claims/images09.rs
+++ b/reference-interpreter/src/claims/images09.rs
@@ -4,6 +4,8 @@ use super::*;
 
 #[derive(Clone, Debug, PartialEq, Eq)]
 pub struct FixedRegionBinding {
+    /// §12.2 K85: signature mem slot, independent of local region spelling.
+    pub id: String,
     pub group: usize,
     pub slot: usize,
     pub address_width: u64,
@@ -18,14 +20,10 @@ pub(super) struct ImageDomain {
 }
 
 impl ImageDomain {
-    pub fn entry(&self, unrestricted: bool) -> Result<Json> {
+    pub fn unrestricted_entry(&self) -> Result<Json> {
         let mut cells = crate::reserved(self.values.len(), "§12.2 K85", "fixed region cells")?;
         for (index, value) in self.values.iter().enumerate() {
-            let (lo, hi) = if unrestricted {
-                (BitVector::zero(value.width())?, ones(value.width())?)
-            } else {
-                (value.clone(), value.clone())
-            };
+            let (lo, hi) = (BitVector::zero(value.width())?, ones(value.width())?);
             cells.push(Json::Object(BTreeMap::from([
                 ("index".into(), Json::Number(index.to_string())),
                 ("lo".into(), decimal_json(&lo)),
@@ -37,6 +35,17 @@ impl ImageDomain {
             ("cells".into(), Json::Array(cells)),
         ])))
     }
+
+    pub fn append_cells(&self, cells: &mut Vec<(Component, BitVector)>) -> Result<()> {
+        crate::reserve_more(cells, self.values.len(), "§12.2 K85", "fixed cells")?;
+        cells.extend(self.values.iter().enumerate().map(|(index, value)| {
+            (
+                Component::Cell(self.binding.group, self.binding.slot, index),
+                value.clone(),
+            )
+        }));
+        Ok(())
+    }
 }
 
 impl Object {
@@ -132,6 +141,7 @@ impl Object {
                 (group, slot),
                 ImageDomain {
                     binding: FixedRegionBinding {
+                        id: format!("mem:{slot}"),
                         group,
                         slot,
                         address_width: a,
diff --git a/reference-interpreter/src/claims/replay09.rs b/reference-interpreter/src/claims/replay09.rs
index b031aab..f3e4323 100644
--- a/reference-interpreter/src/claims/replay09.rs
+++ b/reference-interpreter/src/claims/replay09.rs
@@ -11,10 +11,49 @@ pub(super) struct Invocation {
     pub budget: Budget,
 }
 
+#[cfg(test)]
+mod tests {
+    use super::*;
+
+    #[test]
+    fn fixed_cells_never_become_enumeration_components() {
+        let object = Object::parse(include_str!(
+            "../../../conformance/fixtures/accepted-k85-09/image-0102.bisa"
+        ))
+        .unwrap();
+        let certificate = object.section("certificate").unwrap();
+        let closure = certificate
+            .get("bindings")
+            .unwrap()
+            .get("closure_hash")
+            .unwrap()
+            .string()
+            .unwrap();
+        let claim = &certificate
+            .get("regions")
+            .unwrap()
+            .get(closure)
+            .unwrap()
+            .get("claims")
+            .unwrap()
+            .array()
+            .unwrap()[0];
+        let domain = object.domain09(claim, &object.functions["lookup"]).unwrap();
+        // Only t,f,a enumerate. db[0],db[1] fill the tuple independently.
+        assert_eq!(domain.domain.components.len(), 3);
+        assert!(domain
+            .domain
+            .components
+            .iter()
+            .all(|(c, ..)| !matches!(c, Component::Cell(..))));
+    }
+}
+
 struct ResolvedDomain {
     domain: Domain,
     relative_to_image: bool,
     images: Vec<FixedRegionBinding>,
+    fixed_cells: Vec<(Component, BitVector)>,
 }
 pub(super) struct Outcome {
     pub verdict: ClaimVerdict,
@@ -193,16 +232,16 @@ impl Object {
         let inherited = bundles.drain(..controls).collect::<Vec<_>>();
         let images = self.image_domains09(claim.get("domain")?, f)?;
         let mut unrestricted = source.clone();
-        for (value, full) in [(&mut source, false), (&mut unrestricted, true)] {
-            let Json::Object(fields) = value else {
-                unreachable!()
-            };
-            let Json::Array(regions) = fields.get_mut("regions").unwrap() else {
-                unreachable!()
-            };
-            for image in &images {
-                regions.push(image.entry(full)?);
-            }
+        let Json::Object(fields) = &mut unrestricted else {
+            unreachable!()
+        };
+        let Json::Array(regions) = fields.get_mut("regions").unwrap() else {
+            unreachable!()
+        };
+        let mut fixed_cells = Vec::new();
+        for image in &images {
+            regions.push(image.unrestricted_entry()?);
+            image.append_cells(&mut fixed_cells)?;
         }
         let mut domain = self.domain(f, &source)?;
         let mut relative_to_image = !images.is_empty() && self.domain(f, &unrestricted)?.covers_d;
@@ -223,6 +262,7 @@ impl Object {
             domain,
             relative_to_image,
             images: images.into_iter().map(|i| i.binding).collect(),
+            fixed_cells,
         })
     }
 
@@ -433,12 +473,21 @@ impl Object {
             .filter(|(c, ..)| matches!(c, Component::Borrowed(..)))
             .count();
         for (row, values) in elements.iter().enumerate() {
-            let element = domain
+            let mut element = domain
                 .components
                 .iter()
                 .map(|c| c.0.clone())
                 .zip(values.iter().cloned())
                 .collect::<Vec<_>>();
+            // K85: fixed cells fill complete tuples but never add an
+            // enumeration component or consume sampler generator words.
+            crate::reserve_more(
+                &mut element,
+                resolved.fixed_cells.len(),
+                "§12.2 K85",
+                "replay fixed cells",
+            )?;
+            element.extend(resolved.fixed_cells.iter().cloned());
             let before = self.entry09(f, &element, controls)?;
             invocation.controls = before[..controls].to_vec();
             let after = self.execute_element_bound(
@@ -481,22 +530,7 @@ impl Object {
                 elements: elements.len() as u128,
             }
         };
-        if claim.object()?.get("label") == Some(&Json::String("proof".into()))
-            && verdict != ClaimVerdict::Proof
-        {
-            return err(
-                "§12.2 K74",
-                "requested proof but replay covers only a slice of D",
-            );
-        }
-        if claim.object()?.get("label") == Some(&Json::String("proof_relative_to_image".into()))
-            && verdict != ClaimVerdict::ProofRelativeToImage
-        {
-            return err(
-                "§12.2 K85",
-                "requested proof_relative_to_image without complete remaining domain",
-            );
-        }
+        check_requested_label(claim, &verdict)?;
         Ok(Outcome {
             verdict,
             coverage: Some(coverage(f, controls, &resolved, elements.len())?),
diff --git a/reference-interpreter/src/metadata_schema/tests.rs b/reference-interpreter/src/metadata_schema/tests.rs
index 03ec5dc..dc641c4 100644
--- a/reference-interpreter/src/metadata_schema/tests.rs
+++ b/reference-interpreter/src/metadata_schema/tests.rs
@@ -5,6 +5,25 @@ use std::collections::{BTreeMap, BTreeSet};
 fn j(s: &str) -> Json {
     Json::parse(s).unwrap()
 }
+
+#[test]
+fn fixed_images_and_relative_label_are_explicitly_versioned_closed_fields() {
+    let domain = j(
+        r#"{"bundles":[],"borrowed":[],"regions":[],"fixed_regions":[{"name":"db","A":0,"W":1,"image":"00","sha256":"6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d"}]}"#,
+    );
+    validate_for(crate::IsaVersion::V09, "domain", &domain).unwrap();
+    assert!(validate_for(crate::IsaVersion::V08, "domain", &domain).is_err());
+    let label = j(r#""proof_relative_to_image""#);
+    validate_for(crate::IsaVersion::V09, "label", &label).unwrap();
+    assert!(validate_for(crate::IsaVersion::V08, "label", &label).is_err());
+    let mut malformed = domain;
+    let Json::Object(fields) = &mut malformed else {
+        panic!("domain")
+    };
+    fields.insert("image_prepared".into(), Json::Bool(true));
+    // K85 never grants a producer boolean authority to discharge preparation.
+    assert!(validate_for(crate::IsaVersion::V09, "domain", &malformed).is_err());
+}
 #[test]
 fn r15_translation_frame_is_first_and_last_point_tuple() {
     // Literal §12.1 cardinality oracle, independent of TABLE/samples/baseline.
```

## Test diff (reference-interpreter/tests, conformance/tests, conformance/src)
```diff
diff --git a/conformance/tests/draft_witnesses.py b/conformance/tests/draft_witnesses.py
index f5c7049..33b79c4 100644
--- a/conformance/tests/draft_witnesses.py
+++ b/conformance/tests/draft_witnesses.py
@@ -3,8 +3,13 @@ from pathlib import Path
 from fractions import Fraction
 import hashlib
 import json
+import os
+import tomllib
 
 root = Path(__file__).resolve().parents[2]
+reference = Path(os.environ.get("BENNETT_CONFORMANCE_BIN", str(
+    root / "reference-interpreter/target/debug/bennett-isa-ref")))
+assert reference.is_file(), f"reference binary missing: {reference}; build it or set BENNETT_CONFORMANCE_BIN"
 draft = (root / "spec/Bennett-ISA-Spec-0.9.md").read_text()
 accepted = root / "spec/Bennett-ISA-Spec.md"
 assert hashlib.sha256(accepted.read_bytes()).hexdigest() == "90e61d9c377c939fe9652758f61cd5ead068ef06e4e40d812d3f3c5197ab605e"
@@ -175,7 +180,7 @@ for t in range(4):
         first = t ^ 1
         expected = first ^ ((first & 1) << 1) ^ p
         for value, adjoint, output in [(t, False, expected), (expected, True, t)]:
-            command = [str(root / "reference-interpreter/target/debug/bennett-isa-ref"), "run-action", str(multi_dir / "two-blocks.bisa"), "flip", "--mut", str(value), "--in", str(p)]
+            command = [str(reference), "run-action", str(multi_dir / "two-blocks.bisa"), "flip", "--mut", str(value), "--in", str(p)]
             if adjoint:
                 command.append("--adjoint")
             result = subprocess.run(command, capture_output=True, text=True)
@@ -225,7 +230,7 @@ assert bits == draws["outcomes_bits"] and values == draws["outcomes_values"]
 assert values[::-1] == draws["reversed_draw_values"]
 assert [bit_order.index(b) for b in bits] == draws["integer_order_values"]
 draw_dir = root / "conformance/cases/A/A-measure-draw-order-09"
-result = subprocess.run([str(root / "reference-interpreter/target/debug/bennett-isa-ref"), "run-program", str(draw_dir / "two-measures.bisa"), "twice", "--draws", ",".join(draws["draws"])], capture_output=True, text=True)
+result = subprocess.run([str(reference), "run-program", str(draw_dir / "two-measures.bisa"), "twice", "--draws", ",".join(draws["draws"])], capture_output=True, text=True)
 assert result.returncode == 0, result.stderr
 measurements = json.loads(result.stdout)["measurements"]
 assert [m["bits"] for m in measurements] == bits
@@ -269,7 +274,22 @@ runpy.run_path(str(root / "conformance/tools/draft_examples.py"))["check"](draft
 fixture = runpy.run_path(str(root / "conformance/tools/controlled_action_fixture.py"))
 for name, raw in fixture["artifacts"]().items():
     assert (fixture["DIR"] / name).read_bytes() == raw, name
-pinned = root.parent / "bennett-isa-spec-review/reference-interpreter/target/debug/bennett-isa-ref"
+name = "bennett-isa-spec-review"
+pin = tomllib.loads((root / "gate.toml").read_text())["siblings"][name]["sha"]
+# The gate exposes a symlink beside its detached checkout. Direct crate runs
+# use that same pin's materialised cache, never an unpinned sibling worktree.
+pinned_checkout = root.parent / name
+if not pinned_checkout.is_symlink():
+    pinned_checkout = root / ".tmp/gate/cache" / f"{name}@{pin[:12]}" / name
+assert pinned_checkout.is_dir(), f"materialise gate.toml sibling {name}@{pin} before checking witnesses"
+head = subprocess.run(["git", "-C", str(pinned_checkout), "rev-parse", "HEAD"],
+                      check=True, capture_output=True, text=True).stdout.strip()
+assert head == pin, f"pinned witness checkout {head} differs from gate.toml {pin}"
+dirty = subprocess.run(["git", "-C", str(pinned_checkout), "status", "--porcelain", "-uno"],
+                       check=True, capture_output=True, text=True).stdout
+assert not dirty, f"pinned witness checkout has tracked changes: {dirty}"
+pinned = pinned_checkout / "reference-interpreter/target/debug/bennett-isa-ref"
+assert pinned.is_file(), f"build gate.toml sibling {name}@{pin} before checking witnesses"
 compat = fixture["DIR"] / "compat-0.8.bisa"
 for command in ("check", "hash"):
     result = subprocess.run([str(pinned), command, str(compat)], capture_output=True, text=True)
diff --git a/conformance/tests/ref_k85.rs b/conformance/tests/ref_k85.rs
new file mode 100644
index 0000000..7a6dd83
--- /dev/null
+++ b/conformance/tests/ref_k85.rs
@@ -0,0 +1,249 @@
+//! Portable K85 readers deliberately admit fixed_regions and the third
+//! successful category; old closed readers must upgrade explicitly.
+use bennett_isa_conformance::{
+    json::{self, Json},
+    ref_hash::sha256,
+};
+use std::{collections::BTreeSet, path::PathBuf};
+
+const VECTORS: &str = include_str!("../fixtures/accepted-k85-09/k85.json");
+const RESTRICTED: &str = include_str!("../fixtures/accepted-k85-09/restricted-map.json");
+
+fn text(value: &Json) -> &str {
+    value.as_str().unwrap()
+}
+
+fn keys(value: &Json) -> BTreeSet<&str> {
+    let Json::Obj(fields) = value else {
+        panic!("object")
+    };
+    fields.keys().map(String::as_str).collect()
+}
+
+#[test]
+fn portable_fixed_image_reader_preserves_closed_schema_and_independent_hashes() {
+    let vectors = json::parse(VECTORS).unwrap();
+    assert_eq!(
+        text(vectors.get("format").unwrap()),
+        "bennett.fixed-images.v1"
+    );
+    let mut names = BTreeSet::new();
+    let mut image_relations = 0;
+    for vector in vectors.get("cases").unwrap().as_arr().unwrap() {
+        let name = text(vector.get("name").unwrap());
+        assert!(names.insert(name), "duplicate vector {name}");
+        let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
+            .join("fixtures/accepted-k85-09")
+            .join(text(vector.get("object").unwrap()));
+        let source = std::fs::read_to_string(path).unwrap();
+        assert_eq!(
+            sha256(source.as_bytes()),
+            text(vector.get("sha256").unwrap()),
+            "{name}"
+        );
+        let certificate =
+            json::parse(source.split_once("section certificate\n").unwrap().1.trim()).unwrap();
+        let Json::Obj(regions) = certificate.get("regions").unwrap() else {
+            panic!("regions")
+        };
+        let claim = &regions
+            .values()
+            .next()
+            .unwrap()
+            .get("claims")
+            .unwrap()
+            .as_arr()
+            .unwrap()[0];
+        let domain = claim.get("domain").unwrap();
+        let allowed = BTreeSet::from(["bundles", "borrowed", "regions", "args", "fixed_regions"]);
+        assert!(
+            keys(domain).is_subset(&allowed),
+            "unknown domain field in {name}"
+        );
+        if let Some(label) = claim.get("label") {
+            assert!(["proof", "proof_relative_to_image", "evidence"].contains(&text(label)));
+        }
+        if name == "image-0102" || name == "image-0201" {
+            image_relations += 1;
+            let image = &domain.get("fixed_regions").unwrap().as_arr().unwrap()[0];
+            assert_eq!(
+                keys(image),
+                BTreeSet::from(["name", "A", "W", "image", "sha256"])
+            );
+            let bytes = match text(image.get("image").unwrap()) {
+                "0102" => [1, 2],
+                "0201" => [2, 1],
+                other => panic!("unexpected image {other}"),
+            };
+            assert_eq!(sha256(&bytes), text(image.get("sha256").unwrap()));
+            let rows = claim
+                .get("expected")
+                .unwrap()
+                .get("table")
+                .unwrap()
+                .as_arr()
+                .unwrap();
+            assert_eq!(rows.len(), 64);
+            for (ordinal, row) in rows.iter().enumerate() {
+                // t outermost, f next, a fastest: ordinal=32*t+2*f+a.
+                let t = ordinal / 32;
+                let f = (ordinal / 2) % 16;
+                let a = ordinal % 2;
+                for (side, value) in [("before", t), ("after", t ^ (bytes[a] as usize & 1))] {
+                    let tuple = row.get(side).unwrap();
+                    let bundles = tuple.get("bundles").unwrap().as_arr().unwrap();
+                    assert_eq!(
+                        bundles.iter().map(text).collect::<Vec<_>>(),
+                        [value.to_string(), f.to_string(), a.to_string()]
+                    );
+                    let cells = &tuple.get("regions").unwrap().as_arr().unwrap()[0];
+                    assert_eq!(
+                        cells.as_arr().unwrap().iter().map(text).collect::<Vec<_>>(),
+                        bytes.map(|n| n.to_string())
+                    );
+                    assert!(tuple.get("borrowed").unwrap().as_arr().unwrap().is_empty());
+                }
+            }
+            assert_eq!(text(vector.get("covered_fraction").unwrap()), "1/65536");
+            assert_eq!(text(vector.get("full_domain_elements").unwrap()), "4194304");
+        }
+    }
+    assert_eq!(image_relations, 2);
+    for required in [
+        "swapped-hash",
+        "stale-hash",
+        "hex-text-hash",
+        "omit-a",
+        "omit-f",
+        "omit-t",
+        "sampled-full-d",
+        "mut-region",
+        "nonzero-padding",
+        "duplicate-image",
+        "controlled-dirty",
+        "external-reference",
+    ] {
+        assert!(names.contains(required), "missing vector {required}");
+    }
+}
+
+fn matrix(value: &Json) -> Vec<Vec<i64>> {
+    value
+        .as_arr()
+        .unwrap()
+        .iter()
+        .map(|row| {
+            row.as_arr()
+                .unwrap()
+                .iter()
+                .map(|n| {
+                    let Json::Num(n) = n else { panic!("integer") };
+                    assert_eq!(n.fract(), 0.0);
+                    *n as i64
+                })
+                .collect()
+        })
+        .collect()
+}
+
+#[test]
+fn restricted_z_identity_map_has_reduced_input_and_complete_output() {
+    let vector = json::parse(RESTRICTED).unwrap();
+    let u = matrix(vector.get("U").unwrap());
+    let v = matrix(vector.get("V").unwrap());
+    let j = matrix(vector.get("J").unwrap());
+    assert_eq!(u, vec![vec![1, 0], vec![0, -1]]);
+    assert_eq!(v, vec![vec![1, 0], vec![0, 1]]);
+    assert_eq!(j, vec![vec![1], vec![0]]);
+    assert_eq!(vector.get("input_dimension"), Some(&Json::Num(1.0)));
+    assert_eq!(vector.get("output_dimension"), Some(&Json::Num(2.0)));
+    // Exact integer algebra: no interpreter state or numerical output is read.
+    let difference = (0..2)
+        .map(|r| (0..2).map(|c| u[r][c] - v[r][c]).collect::<Vec<_>>())
+        .collect::<Vec<_>>();
+    let restricted = difference
+        .iter()
+        .map(|row| {
+            row.iter()
+                .enumerate()
+                .map(|(c, x)| x * j[c][0])
+                .sum::<i64>()
+        })
+        .collect::<Vec<_>>();
+    assert_eq!(restricted, vec![0, 0]);
+    assert_eq!(
+        vector.get("restricted_frobenius_squared"),
+        Some(&Json::Num(0.0))
+    );
+    assert_eq!(difference.iter().flatten().map(|x| x * x).sum::<i64>(), 4);
+    assert_eq!(
+        vector.get("unrestricted_frobenius_squared"),
+        Some(&Json::Num(4.0))
+    );
+    // Reduced input dimension one times complete output dimension two gives
+    // a 2x2 Choi difference, not 1x1 and not unrestricted 4x4.
+    assert_eq!(
+        matrix(vector.get("restricted_choi_difference").unwrap()),
+        vec![vec![0, 0], vec![0, 0]]
+    );
+    let dual = vector.get("strict_dual").unwrap();
+    let y = dual.get("Y").unwrap().as_arr().unwrap();
+    assert_eq!(y.len(), 2);
+    assert_eq!(
+        y[0].as_arr().unwrap().iter().map(text).collect::<Vec<_>>(),
+        vec!["0.125", "0"]
+    );
+    assert_eq!(
+        y[1].as_arr().unwrap().iter().map(text).collect::<Vec<_>>(),
+        vec!["0", "0.125"]
+    );
+    assert_eq!(text(dual.get("mu").unwrap()), "0.375");
+    assert_eq!(text(dual.get("bound").unwrap()), "0.375");
+    // Exact dyadic arithmetic in units of 1/8 for this diagonal witness.
+    let eighths = |s: &str| match s {
+        "0" => 0,
+        "0.125" => 1,
+        "0.375" => 3,
+        _ => panic!("unexpected witness endpoint {s}"),
+    };
+    let a = eighths(text(&y[0].as_arr().unwrap()[0]));
+    let b = eighths(text(&y[1].as_arr().unwrap()[1]));
+    let mu = eighths(text(dual.get("mu").unwrap()));
+    assert!(a > 0 && b > 0);
+    assert_eq!(mu - (a + b), 1);
+
+    let phase = vector.get("phase_sensitive").unwrap();
+    let phase_u = matrix(phase.get("U").unwrap());
+    let phase_v = matrix(phase.get("V").unwrap());
+    assert_eq!(phase_u, vec![vec![-1, 0], vec![0, -1]]);
+    assert_eq!(phase_v, v);
+    let column = |m: &[Vec<i64>]| {
+        (0..2)
+            .map(|r| (0..2).map(|c| m[r][c] * j[c][0]).sum::<i64>())
+            .collect::<Vec<_>>()
+    };
+    let prepared_u = column(&phase_u);
+    let prepared_v = column(&phase_v);
+    let phase_norm_squared = prepared_u
+        .iter()
+        .zip(&prepared_v)
+        .map(|(u, v)| (u - v) * (u - v))
+        .sum::<i64>();
+    assert_eq!(phase_norm_squared, 4);
+    assert_eq!(
+        phase.get("restricted_frobenius_squared"),
+        Some(&Json::Num(phase_norm_squared as f64))
+    );
+    let choi = (0..2)
+        .map(|r| {
+            (0..2)
+                .map(|c| prepared_u[r] * prepared_u[c] - prepared_v[r] * prepared_v[c])
+                .collect::<Vec<_>>()
+        })
+        .collect::<Vec<_>>();
+    assert_eq!(
+        choi,
+        matrix(phase.get("uncontrolled_choi_difference").unwrap())
+    );
+    assert_eq!(choi, vec![vec![0, 0], vec![0, 0]]);
+}
diff --git a/reference-interpreter/tests/isa09_fixed_image.rs b/reference-interpreter/tests/isa09_fixed_image.rs
new file mode 100644
index 0000000..4583238
--- /dev/null
+++ b/reference-interpreter/tests/isa09_fixed_image.rs
@@ -0,0 +1,319 @@
+//! Every expected tuple/verdict is derived in the portable vector generator,
+//! independently of the interpreter. K85 preserves exact phase and full tuples.
+mod support;
+use bennett_isa_ref::{
+    json::Json, ClaimVerdict, Object, QuantumBindings, QuantumRegion, QuantumState,
+};
+use std::{collections::BTreeMap, path::PathBuf};
+
+fn fields(value: &mut Json) -> &mut BTreeMap<String, Json> {
+    let Json::Object(fields) = value else {
+        panic!("object")
+    };
+    fields
+}
+
+fn root(object: &Object) -> &str {
+    object
+        .section("certificate")
+        .unwrap()
+        .get("bindings")
+        .unwrap()
+        .get("closure_hash")
+        .unwrap()
+        .string()
+        .unwrap()
+}
+
+fn fixture(name: &str) -> String {
+    std::fs::read_to_string(PathBuf::from(env!("CARGO_MANIFEST_DIR")).join(format!(
+        "../conformance/fixtures/accepted-k85-09/{name}.bisa"
+    )))
+    .unwrap()
+}
+
+fn mutate(source: &str, change: impl FnOnce(&mut Json)) -> String {
+    let (base, cert) = source.split_once("section certificate\n").unwrap();
+    let mut cert = Json::parse(cert.trim()).unwrap();
+    let record = fields(fields(&mut cert).get_mut("regions").unwrap())
+        .values_mut()
+        .next()
+        .unwrap();
+    change(record);
+    format!("{base}section certificate\n{}\n", cert.canonical())
+}
+
+fn claim(record: &mut Json) -> &mut Json {
+    let Json::Array(claims) = fields(record).get_mut("claims").unwrap() else {
+        panic!("claims")
+    };
+    &mut claims[0]
+}
+
+#[test]
+fn published_fixed_image_vectors_replay_with_exact_coverage_and_bindings() {
+    let manifest = Json::parse(include_str!(
+        "../../conformance/fixtures/accepted-k85-09/k85.json"
+    ))
+    .unwrap();
+    for vector in manifest.get("cases").unwrap().array().unwrap() {
+        let name = vector.get("name").unwrap().string().unwrap();
+        let text = fixture(name);
+        assert_eq!(
+            bennett_isa_ref::sha256_hex(text.as_bytes()),
+            vector.get("sha256").unwrap().string().unwrap(),
+            "{name}"
+        );
+        let outcome = vector.get("outcome").unwrap().string().unwrap();
+        let parsed = Object::parse(&text);
+        if outcome == "reject_admission" {
+            let error = parsed.unwrap_err().to_string();
+            assert!(error.contains("§12.2"), "{name}: {error}");
+            continue;
+        }
+        let object = parsed.unwrap_or_else(|e| panic!("{name}: {e}"));
+        object.check_hashes().unwrap();
+        if outcome == "reject_replay" {
+            assert!(
+                object.verify_claim(root(&object), 0).is_err(),
+                "{name}: direct checker"
+            );
+            assert!(
+                object.verify_certificate().is_err(),
+                "{name}: certificate checker"
+            );
+            continue;
+        }
+        let n = vector.get("elements").unwrap().uint().unwrap();
+        let expected = match outcome {
+            "proof" => ClaimVerdict::Proof,
+            "proof_relative_to_image" => ClaimVerdict::ProofRelativeToImage,
+            "evidence" => ClaimVerdict::Evidence { elements: n },
+            _ => panic!("unexpected outcome {outcome}"),
+        };
+        assert_eq!(
+            object.verify_claim(root(&object), 0).unwrap(),
+            expected,
+            "{name}"
+        );
+        let report = object.verify_certificate().unwrap().claims.remove(0);
+        assert_eq!(report.verdict, expected, "{name}");
+        assert_eq!(report.closure_hash, root(&object));
+        assert_eq!(report.index, 0);
+        assert_eq!(report.context_key, support::json("[]"));
+        let coverage = report.coverage.unwrap();
+        assert_eq!(coverage.elements, n, "{name}");
+        assert_eq!(
+            coverage.full_domain_elements,
+            vector
+                .get("full_domain_elements")
+                .unwrap()
+                .string()
+                .unwrap(),
+            "{name}"
+        );
+        assert_eq!(
+            coverage.covered_fraction,
+            vector.get("covered_fraction").unwrap().string().unwrap(),
+            "{name}"
+        );
+        if name == "report-order" {
+            // Producer order is aux,db. Signature mem slots are db,aux.
+            assert_eq!(
+                coverage
+                    .fixed_regions
+                    .iter()
+                    .map(|b| (b.group, b.slot))
+                    .collect::<Vec<_>>(),
+                vec![(2, 0), (2, 1)]
+            );
+            assert_eq!(
+                coverage.fixed_regions[0].sha256,
+                bennett_isa_ref::sha256_hex(&[1, 2])
+            );
+            assert_eq!(
+                coverage.fixed_regions[1].sha256,
+                bennett_isa_ref::sha256_hex(&[1])
+            );
+            assert_eq!(
+                coverage
+                    .fixed_regions
+                    .iter()
+                    .map(|b| b.id.as_str())
+                    .collect::<Vec<_>>(),
+                vec!["mem:0", "mem:1"]
+            );
+        }
+    }
+}
+
+#[test]
+fn requested_labels_are_exclusive_for_full_and_image_relative_proofs() {
+    for (fixture_name, computed) in [
+        ("full-d-x", "proof"),
+        ("image-0102", "proof_relative_to_image"),
+        ("omit-a", "evidence"),
+        ("sampled-full-d", "evidence"),
+    ] {
+        for label in ["proof", "proof_relative_to_image", "evidence"] {
+            let text = mutate(&fixture(fixture_name), |record| {
+                fields(claim(record)).insert("label".into(), Json::String(label.into()));
+            });
+            let object = Object::parse(&text).unwrap();
+            let accepts = label == "evidence" || label == computed;
+            assert_eq!(
+                object.verify_claim(root(&object), 0).is_ok(),
+                accepts,
+                "{fixture_name}: {label}"
+            );
+            assert_eq!(
+                object.verify_certificate().is_ok(),
+                accepts,
+                "{fixture_name}: {label}"
+            );
+        }
+    }
+}
+
+#[test]
+fn structural_full_d_theorem_cannot_satisfy_an_image_relative_request() {
+    let text = mutate(&fixture("full-d-x"), |record| {
+        *claim(record) = support::json(
+            r#"{"kind":"structural","rule":"adjoint_table","subclaims":[],"witness":{},"invocation":{"args":[],"budget":["0","0","0","0"]},"label":"proof_relative_to_image"}"#,
+        );
+    });
+    let object = Object::parse(&text).unwrap();
+    // K94 establishes a full-D adjoint theorem. K85's relative request is
+    // exclusive; stronger/different theorem categories cannot stand in for it.
+    assert!(object.verify_claim(root(&object), 0).is_err());
+    assert!(object.verify_certificate().is_err());
+}
+
+#[test]
+fn fixed_image_proof_does_not_discharge_an_unrestricted_borrow_frame() {
+    let text = mutate(&fixture("controlled-dirty"), |record| {
+        fields(fields(record).get_mut("verification").unwrap())
+            .insert("borrow_frames".into(), support::json("[0]"));
+    });
+    let object = Object::parse(&text).unwrap();
+    assert_eq!(
+        object.verify_claim(root(&object), 0).unwrap(),
+        ClaimVerdict::ProofRelativeToImage
+    );
+    let error = object.verify_certificate().unwrap_err().to_string();
+    assert!(error.contains("proof over D"), "{error}");
+}
+
+#[test]
+fn full_tuples_include_every_fixed_cell_and_preserved_bundle() {
+    for field in ["bundles", "regions"] {
+        let text = mutate(&fixture("image-0102"), |record| {
+            let Json::Array(rows) = fields(fields(claim(record)).get_mut("expected").unwrap())
+                .get_mut("table")
+                .unwrap()
+            else {
+                panic!("rows")
+            };
+            let after = fields(fields(&mut rows[0]).get_mut("after").unwrap());
+            let Json::Array(values) = after.get_mut(field).unwrap() else {
+                panic!("values")
+            };
+            if field == "regions" {
+                let Json::Array(cells) = &mut values[0] else {
+                    panic!("cells")
+                };
+                cells[0] = Json::String("0".into());
+            } else {
+                values[1] = Json::String("1".into());
+            }
+        });
+        let object = Object::parse(&text).unwrap();
+        let error = object
+            .verify_claim(root(&object), 0)
+            .unwrap_err()
+            .to_string();
+        assert!(error.contains("full tuple mismatch"), "{field}: {error}");
+    }
+}
+
+#[test]
+fn certificate_image_metadata_never_changes_executable_identities() {
+    let a = Object::parse(&fixture("image-0102")).unwrap();
+    let b = Object::parse(&fixture("image-0201")).unwrap();
+    let a_id = a.identity().unwrap();
+    let b_id = b.identity().unwrap();
+    assert_eq!(a_id.object_hash, b_id.object_hash);
+    assert_eq!(a_id.interface_hashes, b_id.interface_hashes);
+    assert_eq!(a_id.closure_hashes, b_id.closure_hashes);
+    // Old closed 0.8 readers must reject the 0.9 fields/label explicitly.
+    let legacy = fixture("image-0102")
+        .replace("=0.9", "=0.8")
+        .replace("\"0.9\"", "\"0.8\"");
+    assert!(Object::parse(&legacy).is_err());
+}
+
+#[test]
+fn controlled_fixed_map_restores_dirty_and_arbitrary_entangled_references() {
+    let object = Object::parse(&fixture("external-reference")).unwrap();
+    assert_eq!(
+        object.verify_claim(root(&object), 0).unwrap(),
+        ClaimVerdict::ProofRelativeToImage
+    );
+    let mut q = QuantumState::new();
+    let t = q.allocate(1).unwrap();
+    let f = q.allocate(4).unwrap();
+    let a = q.allocate(1).unwrap();
+    let cells = vec![q.allocate(1).unwrap(), q.allocate(1).unwrap()];
+    let dirty = q.allocate(1).unwrap();
+    let control = q.allocate(1).unwrap();
+    let references = [
+        q.allocate(1).unwrap(),
+        q.allocate(1).unwrap(),
+        q.allocate(1).unwrap(),
+    ];
+    q.gate("x", &cells[0], None, &[]).unwrap();
+    for bit in [f[0], f[2]] {
+        q.gate("x", &[bit], None, &[]).unwrap();
+    }
+    for (wire, reference) in [&a, &dirty, &control].into_iter().zip(&references) {
+        q.gate("h", wire, None, &[]).unwrap();
+        q.gate("cx", &[wire[0], reference[0]], None, &[]).unwrap();
+    }
+    let mut bindings = QuantumBindings::default();
+    for (name, wires) in [("t", &t), ("f", &f), ("a", &a)] {
+        bindings.bundles.insert(name.into(), wires.clone());
+    }
+    bindings.regions.insert(
+        "db".into(),
+        QuantumRegion {
+            address_width: 1,
+            cell_width: 1,
+            cells: cells.clone(),
+        },
+    );
+    bindings.borrowed.push(dirty.clone());
+    object
+        .execute_action("lookup", &mut q, &bindings, false, &control)
+        .unwrap();
+    // Independently derived inverse of t ^= control & !a. The other
+    // systems, including the three untouched references, must factor back.
+    q.gate("x", &a, None, &[]).unwrap();
+    q.gate("ccx", &[control[0], a[0], t[0]], None, &[]).unwrap();
+    q.gate("x", &a, None, &[]).unwrap();
+    for (wire, reference) in [&a, &dirty, &control].into_iter().zip(&references).rev() {
+        q.gate("cx", &[wire[0], reference[0]], None, &[]).unwrap();
+        q.gate("h", wire, None, &[]).unwrap();
+    }
+    q.gate("x", &cells[0], None, &[]).unwrap();
+    for bit in [f[0], f[2]] {
+        q.gate("x", &[bit], None, &[]).unwrap();
+    }
+    for wires in [&t, &f, &a, &cells[0], &cells[1], &dirty, &control]
+        .into_iter()
+        .chain(references.iter())
+    {
+        // release checks exact-zero amplitudes, not a binary64 tolerance.
+        q.release(wires).unwrap();
+    }
+    assert_eq!(q.wire_count(), 0);
+}
```

## Vector files added/changed (contents in the repository you run in)
     conformance/cases/D/D-k85-also-ranged/case.json                           |  18 ++++++++
     conformance/cases/D/D-k85-controlled-dirty/case.json                      |  17 ++++++++
     conformance/cases/D/D-k85-duplicate-bundle/case.json                      |  18 ++++++++
     conformance/cases/D/D-k85-duplicate-cell/case.json                        |  18 ++++++++
     conformance/cases/D/D-k85-duplicate-image/case.json                       |  18 ++++++++
     conformance/cases/D/D-k85-duplicate-region/case.json                      |  18 ++++++++
     conformance/cases/D/D-k85-external-reference/case.json                    |  17 ++++++++
     conformance/cases/D/D-k85-full-d-x/case.json                              |  17 ++++++++
     conformance/cases/D/D-k85-hex-text-hash/case.json                         |  18 ++++++++
     conformance/cases/D/D-k85-image-0102/case.json                            |  17 ++++++++
     conformance/cases/D/D-k85-image-0201/case.json                            |  17 ++++++++
     conformance/cases/D/D-k85-long-image/case.json                            |  18 ++++++++
     conformance/cases/D/D-k85-mut-region/case.json                            |  18 ++++++++
     conformance/cases/D/D-k85-nonzero-padding/case.json                       |  18 ++++++++
     conformance/cases/D/D-k85-omit-a/case.json                                |  17 ++++++++
     conformance/cases/D/D-k85-omit-f/case.json                                |  17 ++++++++
     conformance/cases/D/D-k85-omit-t/case.json                                |  17 ++++++++
     conformance/cases/D/D-k85-packing/case.json                               |  17 ++++++++
     conformance/cases/D/D-k85-report-order/case.json                          |  17 ++++++++
     conformance/cases/D/D-k85-request-evidence/case.json                      |  17 ++++++++
     conformance/cases/D/D-k85-request-proof_relative_to_image/case.json       |  17 ++++++++
     conformance/cases/D/D-k85-sampled-full-d/case.json                        |  17 ++++++++
     conformance/cases/D/D-k85-short-image/case.json                           |  18 ++++++++
     conformance/cases/D/D-k85-stale-hash/case.json                            |  18 ++++++++
     conformance/cases/D/D-k85-swapped-hash/case.json                          |  18 ++++++++
     conformance/cases/D/D-k85-uppercase/case.json                             |  18 ++++++++
     conformance/cases/D/D-k85-wrong-a/case.json                               |  18 ++++++++
     conformance/cases/D/D-k85-wrong-w/case.json                               |  18 ++++++++
     conformance/fixtures/accepted-k85-09/README.md                            |  64 ++++++++++++++++++++++++++++
     conformance/fixtures/accepted-k85-09/also-ranged.bisa                     |  17 ++++++++
     conformance/fixtures/accepted-k85-09/controlled-dirty.bisa                |  21 +++++++++
     conformance/fixtures/accepted-k85-09/duplicate-bundle.bisa                |  17 ++++++++
     conformance/fixtures/accepted-k85-09/duplicate-cell.bisa                  |  17 ++++++++
     conformance/fixtures/accepted-k85-09/duplicate-image.bisa                 |  17 ++++++++
     conformance/fixtures/accepted-k85-09/duplicate-region.bisa                |  17 ++++++++
     conformance/fixtures/accepted-k85-09/external-reference.bisa              |  21 +++++++++
     conformance/fixtures/accepted-k85-09/full-d-x.bisa                        |  12 ++++++
     conformance/fixtures/accepted-k85-09/generate.py                          | 276 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
     conformance/fixtures/accepted-k85-09/hex-text-hash.bisa                   |  17 ++++++++
     conformance/fixtures/accepted-k85-09/image-0102.bisa                      |  17 ++++++++
     conformance/fixtures/accepted-k85-09/image-0201.bisa                      |  17 ++++++++
     conformance/fixtures/accepted-k85-09/k85.json                             |   1 +
     conformance/fixtures/accepted-k85-09/long-image.bisa                      |  17 ++++++++
     conformance/fixtures/accepted-k85-09/mut-region.bisa                      |  17 ++++++++
     conformance/fixtures/accepted-k85-09/nonzero-padding.bisa                 |  17 ++++++++
     conformance/fixtures/accepted-k85-09/omit-a.bisa                          |  17 ++++++++
     conformance/fixtures/accepted-k85-09/omit-f.bisa                          |  17 ++++++++
     conformance/fixtures/accepted-k85-09/omit-t.bisa                          |  17 ++++++++
     conformance/fixtures/accepted-k85-09/packing.bisa                         |  17 ++++++++
     conformance/fixtures/accepted-k85-09/phase.bisa                           |  19 +++++++++
     conformance/fixtures/accepted-k85-09/report-order.bisa                    |  17 ++++++++
     conformance/fixtures/accepted-k85-09/request-evidence.bisa                |  17 ++++++++
     conformance/fixtures/accepted-k85-09/request-proof.bisa                   |  17 ++++++++
     conformance/fixtures/accepted-k85-09/request-proof_relative_to_image.bisa |  17 ++++++++
     conformance/fixtures/accepted-k85-09/restricted-map.json                  |   1 +
     conformance/fixtures/accepted-k85-09/sampled-full-d.bisa                  |  12 ++++++
     conformance/fixtures/accepted-k85-09/short-image.bisa                     |  17 ++++++++
     conformance/fixtures/accepted-k85-09/stale-hash.bisa                      |  17 ++++++++
     conformance/fixtures/accepted-k85-09/swapped-hash.bisa                    |  17 ++++++++
     conformance/fixtures/accepted-k85-09/uppercase.bisa                       |  17 ++++++++
     conformance/fixtures/accepted-k85-09/wrong-a.bisa                         |  17 ++++++++
     conformance/fixtures/accepted-k85-09/wrong-w.bisa                         |  17 ++++++++
     62 files changed, 1343 insertions(+)
