# K85 round-2 packet: bennett-isa-spec job/isa-k85-land a0b49a0..58a1378

Round-1 (docs/council/isa-k85-2026-11-08/round-1/report.md) returned REVISE (sol, astra) / ACCEPT (Muse) with two S0s: (1) core: no checked borrow-lifetime inventory (extra/wider borrowed positions accepted; legal omitted position rejected); (2) contract: K75 host-limit outcomes not reported per claim. The fix commits (cherry-picked unchanged from the SET B writer's branch job/isa-k86 8cf1f86/aae0cff/31c3b80/04d5fc3, without that branch's separate K86 helper commits) are 43c1b76, 7e576ac, 64f708a, 58a1378. src/borrow.rs gains ONE read-only accessor (ruled SET A -> SET B transfer for that accessor only).

## Fix diff a0b49a0..58a1378
```diff
diff --git a/reference-interpreter/SPEC-QUESTIONS.md b/reference-interpreter/SPEC-QUESTIONS.md
index d99b4f8..59259a8 100644
--- a/reference-interpreter/SPEC-QUESTIONS.md
+++ b/reference-interpreter/SPEC-QUESTIONS.md
@@ -332,3 +332,33 @@ changed in response to the council's round-1 review
     cli_xam::r18_cli_literal_nested_budget_check_hash_defer_and_run_reject,
     metadata::r18_nested_specificity_family_matches_brute_force. The orchestrator
     owns bead b-isa-spec-6hs; the interpreter's full-ISA bead remains active.
+
+34. **Requested labels across claim kinds (§12.2 K85/K75)**
+    (bead `bennett-isa-spec-b7k`; council `isa-k85-2026-11-08`, round 1,
+    Muse spec gap **B-K85-2**). The coverage paragraph defines its exclusive
+    replay outcomes for exhaustive and sampled claims, but its label rejection
+    sentences do not explicitly limit the claim kinds they govern.
+
+    Reading **(A)**, retained without a behaviour change: labels are a common
+    claim field, and “Requested proof rejects unless the computed outcome is
+    proof” and the corresponding image-relative rejection are kind-independent.
+    An established structural theorem can satisfy `proof`; it cannot satisfy
+    `proof_relative_to_image`. A producer label never upgrades the checker's
+    independently computed result.
+
+    `Unverified` and K75 unchecked outcomes are exempt from label rejection and
+    never satisfy a requested label. K75 explicitly retains an unchecked
+    obligation “including when a producer requested a label”. Applying a proof
+    request cannot convert missing checking machinery or a host limit into
+    either proof or a producer error. This also preserves the closed common
+    claim-field grammar and the existing kind-independent rejection wording.
+    Reading (B), treating labels as replay-only or rejecting an uncheckable
+    claim solely for its label, would contradict that unchecked exemption.
+
+    Proposed clarification of §12.2: “A label may accompany any claim kind.
+    A requested successful label must match the independently computed
+    successful outcome. An unchecked (host limit) or otherwise unestablished
+    outcome is reported as such; requesting a label neither upgrades that
+    outcome nor causes rejection solely because checking is unavailable.”
+    This records the interpreter's reading; it does not amend the published
+    ISA text or claim completion of staged numerical/channel verification.
diff --git a/reference-interpreter/src/borrow.rs b/reference-interpreter/src/borrow.rs
index ada9da3..2cd1072 100644
--- a/reference-interpreter/src/borrow.rs
+++ b/reference-interpreter/src/borrow.rs
@@ -1980,6 +1980,94 @@ impl Object {
         }
         Ok(compiler)
     }
+    /// §12.2 K70: widths of distinct checked borrow lifetimes, in allocation
+    /// order, including every repeated visit and transitive action call.
+    /// `None` means an unlinked action prevents a complete inventory. This
+    /// reads the existing compiler's facts without changing its semantics.
+    pub fn checked_borrow_lifetimes(&self, root: &str) -> Result<Option<Vec<usize>>> {
+        // Prove absence before materialising compiler wire coordinates. In
+        // particular, a large legal interface with no borrows needs no storage
+        // proportional to that interface merely to establish an empty list.
+        fn inspect(seq: &[Instruction], borrows: &mut bool, calls: &mut Vec<String>) -> Result<()> {
+            for instruction in seq {
+                *borrows |= instruction.op == "qborrow";
+                if matches!(instruction.op.as_str(), "action_call" | "adj" | "ctl") {
+                    let call = normalize_call(instruction)?;
+                    if call.instruction.op == "action_call" {
+                        calls.push(call.instruction.operands[0].trim_start_matches('@').into());
+                    }
+                }
+                for body in &instruction.bodies {
+                    inspect(body, borrows, calls)?;
+                }
+            }
+            Ok(())
+        }
+        fn collect(nodes: &[Node], out: &mut Vec<usize>) -> Result<()> {
+            for node in nodes {
+                match node {
+                    Node::Borrow(wires) => {
+                        crate::reserve_more(out, 1, "§12.2 K70", "checked borrow lifetimes")?;
+                        out.push(wires.len());
+                    }
+                    Node::Call {
+                        body: Some(body), ..
+                    } => collect(body, out)?,
+                    Node::Repeat(copies, body) => {
+                        let mut period = Vec::new();
+                        collect(body, &mut period)?;
+                        if period.is_empty() {
+                            continue;
+                        }
+                        let count = usize::try_from(*copies)
+                            .ok()
+                            .and_then(|n| n.checked_mul(period.len()))
+                            .ok_or_else(|| {
+                                crate::resource_error(
+                                    "§12.2 K70",
+                                    "checked borrow lifetime count exceeds usize",
+                                )
+                            })?;
+                        crate::reserve_more(out, count, "§12.2 K70", "checked borrow lifetimes")?;
+                        for _ in 0..*copies {
+                            out.extend_from_slice(&period);
+                        }
+                    }
+                    _ => {}
+                }
+            }
+            Ok(())
+        }
+        let Some(function) = self.functions.get(root) else {
+            return Ok(None);
+        };
+        if !matches!(function.kind.as_str(), "action" | "perm_action") {
+            return Ok(Some(Vec::new()));
+        }
+        let mut pending = vec![root.to_string()];
+        let mut seen = BTreeSet::new();
+        let mut borrows = false;
+        while let Some(name) = pending.pop() {
+            if !seen.insert(name.clone()) {
+                continue;
+            }
+            let Some(callee) = self.functions.get(&name) else {
+                return Ok(None);
+            };
+            for block in &callee.blocks {
+                inspect(&block.instructions, &mut borrows, &mut pending)?;
+            }
+        }
+        if !borrows {
+            return Ok(Some(Vec::new()));
+        }
+        let mut compiler = self.borrow_compiler(function)?;
+        let mut nodes = Vec::new();
+        compiler.compile_function(function, &[], &mut nodes)?;
+        let mut widths = Vec::new();
+        collect(&nodes, &mut widths)?;
+        Ok(Some(widths))
+    }
     /// Check a named source frame against the complete compiled circuit,
     /// including inherited predicates, loop structure and physical wire names.
     pub(crate) fn check_translation_frame(
diff --git a/reference-interpreter/src/certificate.rs b/reference-interpreter/src/certificate.rs
index 9d0c64c..66a20f6 100644
--- a/reference-interpreter/src/certificate.rs
+++ b/reference-interpreter/src/certificate.rs
@@ -262,7 +262,7 @@ fn frame09(value: &Json, f: &Function, contexts: &[u128]) -> Result<()> {
     }
     Ok(())
 }
-fn table09(c: &Json, f: &Function) -> Result<()> {
+fn table09(c: &Json, f: &Function, borrowed: Option<&[usize]>) -> Result<()> {
     let expected = c.get("expected")?;
     let Some(table) = expected.object().ok().and_then(|m| m.get("table")) else {
         return Ok(());
@@ -280,13 +280,8 @@ fn table09(c: &Json, f: &Function) -> Result<()> {
             }
         })
         .collect::<Vec<_>>();
-    let borrowed = c
-        .get("domain")?
-        .get("borrowed")?
-        .array()?
-        .iter()
-        .map(|p| p.get("width")?.uint())
-        .collect::<Result<Vec<_>>>()?;
+    // Unlinked source retains an unchecked replay obligation; producer domain
+    // entries cannot establish the missing lifetime inventory.
     let regions = f
         .params
         .iter()
@@ -322,11 +317,13 @@ fn table09(c: &Json, f: &Function) -> Result<()> {
                 crate::object::unsigned_literal(b.string()?, w)?;
             }
             let values = tuple.get("borrowed")?.array()?;
-            if values.len() != borrowed.len() {
-                return err("§12.1 K13", "incomplete borrowed tuple");
-            }
-            for (v, w) in values.iter().zip(&borrowed) {
-                crate::object::unsigned_literal(v.string()?, *w)?;
+            if let Some(borrowed) = borrowed {
+                if values.len() != borrowed.len() {
+                    return err("§12.1 K13", "incomplete borrowed tuple");
+                }
+                for (v, w) in values.iter().zip(borrowed) {
+                    crate::object::unsigned_literal(v.string()?, *w as u128)?;
+                }
             }
             let cells = tuple.get("regions")?.array()?;
             if cells.len() != regions.len() {
@@ -367,13 +364,14 @@ pub(crate) fn invocation_budget(value: &Json) -> Result<crate::Budget> {
 
 #[cfg(test)]
 fn domain(value: &Json, f: &Function) -> Result<()> {
-    domain_for(value, f, crate::IsaVersion::V08, 0)
+    domain_for(value, f, crate::IsaVersion::V08, 0, None)
 }
 pub(crate) fn domain_for(
     value: &Json,
     f: &Function,
     version: crate::IsaVersion,
     controls: u128,
+    borrowed: Option<&[usize]>,
 ) -> Result<()> {
     let mut names = BTreeSet::new();
     for group in ["bundles", "borrowed"] {
@@ -390,6 +388,19 @@ pub(crate) fn domain_for(
                 return err("§12.2", "repeated domain component");
             }
             let width = b.get("width")?.uint()?;
+            if version == crate::IsaVersion::V09 && group == "borrowed" {
+                if let Some(widths) = borrowed {
+                    let actual = widths.get(position).ok_or_else(|| {
+                        Error::new(
+                            "§12.2 K70: borrowed position exceeds checked lifetime inventory"
+                                .into(),
+                        )
+                    })?;
+                    if width != *actual as u128 {
+                        return err("§12.2 K72", "borrowed width differs from checked lifetime");
+                    }
+                }
+            }
             if width == 0 || (inherited && width != 1) {
                 return err("§12.2", "zero-width domain component");
             }
@@ -683,7 +694,13 @@ impl Object {
                 }
                 let fault = v.get("fault_rate")?;
 
-                domain_for(fault.get("domain")?, f, self.isa_version, 0)?;
+                domain_for(
+                    fault.get("domain")?,
+                    f,
+                    self.isa_version,
+                    0,
+                    self.admission_borrow_lifetimes(f)?.as_deref(),
+                )?;
                 if self.isa_version == crate::IsaVersion::V09 {
                     self.validate_image_domains09(fault.get("domain")?, f)?;
                 }
@@ -716,6 +733,19 @@ impl Object {
             Ok(())
         })
     }
+    // §12.2 K75: inability to materialise an inventory is a deferred checking
+    // obligation, not malformed producer metadata. Replay resolves it again
+    // inside the per-claim host-limit boundary before any successful verdict.
+    fn admission_borrow_lifetimes(&self, f: &Function) -> Result<Option<Vec<usize>>> {
+        if self.isa_version != crate::IsaVersion::V09 {
+            return Ok(None);
+        }
+        match self.checked_borrow_lifetimes(&f.name) {
+            Err(error) if error.kind() == crate::ErrorKind::HostResource => Ok(None),
+            result => result,
+        }
+    }
+
     fn validate_claim(&self, c: &Json, f: &Function, position: usize) -> Result<()> {
         crate::metadata_schema::validate_for(self.isa_version, "claim", c)?;
         if self.isa_version == crate::IsaVersion::V09
@@ -758,7 +788,16 @@ impl Object {
                 );
             }
             if matches!(c.get("kind")?.string()?, "exhaustive" | "sampled") {
-                table09(c, f)?;
+                let borrowed = self.admission_borrow_lifetimes(f)?;
+                let controls = c.get("subject")?.get("inherited_controls")?.uint()?;
+                domain_for(
+                    c.get("domain")?,
+                    f,
+                    self.isa_version,
+                    controls,
+                    borrowed.as_deref(),
+                )?;
+                table09(c, f, borrowed.as_deref())?;
             }
             if let Some(v) = c.object()?.get("invocation") {
                 if v.get("args")? != &Json::String("all".into()) {
@@ -790,7 +829,15 @@ impl Object {
                 } else {
                     0
                 };
-                domain_for(c.get("domain")?, f, self.isa_version, controls)?;
+                if self.isa_version != crate::IsaVersion::V09 {
+                    domain_for(
+                        c.get("domain")?,
+                        f,
+                        self.isa_version,
+                        controls,
+                        self.admission_borrow_lifetimes(f)?.as_deref(),
+                    )?;
+                }
                 if c.get("expected")? == &Json::String("oracle".into()) {
                     subject(c.get("subject")?)?;
                 }
@@ -801,7 +848,15 @@ impl Object {
                 } else {
                     0
                 };
-                domain_for(c.get("domain")?, f, self.isa_version, controls)?;
+                if self.isa_version != crate::IsaVersion::V09 {
+                    domain_for(
+                        c.get("domain")?,
+                        f,
+                        self.isa_version,
+                        controls,
+                        self.admission_borrow_lifetimes(f)?.as_deref(),
+                    )?;
+                }
                 if !c
                     .get("sampler")?
                     .get("seed")?
diff --git a/reference-interpreter/src/claims.rs b/reference-interpreter/src/claims.rs
index 8be74f2..bb21f6d 100644
--- a/reference-interpreter/src/claims.rs
+++ b/reference-interpreter/src/claims.rs
@@ -112,6 +112,7 @@ enum Component {
     Cell(usize, usize, usize),
 }
 struct Domain {
+    borrowed_widths: Vec<usize>,
     components: Vec<(Component, usize, BitVector, BitVector)>,
     covers_d: bool,
 }
@@ -204,6 +205,7 @@ pub(crate) fn r21_resource_cases() {
     for width in [1, 2, 3, 62, 63, 64, 127, 128] {
         for count in [1, 2] {
             let d = Domain {
+                borrowed_widths: Vec::new(),
                 covers_d: true,
                 components: (0..count)
                     .map(|i| {
@@ -317,6 +319,16 @@ impl Object {
             .ok_or_else(|| Error::new(format!("§12: closure {closure} is not a function")))
     }
     fn domain(&self, f: &Function, d: &Json) -> Result<Domain> {
+        let borrowed_widths = if self.isa_version == crate::IsaVersion::V09 {
+            self.checked_borrow_lifetimes(&f.name)?.ok_or_else(|| {
+                Error::new(
+                    "§12.2 K70: checked borrow lifetime inventory requires linked actions".into(),
+                )
+            })?
+        } else {
+            // Frozen 0.8 tuples retain their explicitly supplied idle pool.
+            Vec::new()
+        };
         let mut components = Vec::new();
         let mut bundles = BTreeSet::new();
         let mut regions = BTreeSet::new();
@@ -326,6 +338,15 @@ impl Object {
                 let name = b.get("name")?.string()?.to_string();
                 let width = usize::try_from(b.get("width")?.uint()?)
                     .map_err(|_| Error::host_resource("§12.2: host limit: domain width".into()))?;
+                if self.isa_version == crate::IsaVersion::V09
+                    && borrowed
+                    && borrowed_widths.get(ordinal) != Some(&width)
+                {
+                    return err(
+                        "§12.2 K70/K72",
+                        "borrowed position or width differs from checked lifetime inventory",
+                    );
+                }
                 let lo = json_bits(b.get("lo")?, width)?;
                 let hi = json_bits(b.get("hi")?, width)?;
                 full &= lo.is_zero() && hi == ones(width)?;
@@ -390,6 +411,9 @@ impl Object {
                 }
             }
         }
+        if self.isa_version == crate::IsaVersion::V09 {
+            full &= d.get("borrowed")?.array()?.len() == borrowed_widths.len();
+        }
         // D: every interface bundle and every region in the region's input
         // domain (§5.2, §5.3; tgt/fault included for oracles).
         let groups = if f.kind == "oracle" { 4 } else { 3 };
@@ -404,6 +428,7 @@ impl Object {
                     })
                 });
         Ok(Domain {
+            borrowed_widths,
             components,
             covers_d,
         })
@@ -606,13 +631,62 @@ impl Object {
             );
         }
         let mut borrowed = Vec::new();
-        for (c, v) in element {
-            if let Component::Borrowed(ordinal, _) = c {
-                if *ordinal != borrowed.len() {
-                    return err("§12.2", "borrowed component position mismatch");
+        if self.isa_version == crate::IsaVersion::V08 {
+            // Preserve the frozen legacy flat-tuple/idle-pool encoding. K70/K71
+            // complete-lifetime replay below belongs to the 0.9 checker.
+            for (component, value) in element {
+                if let Component::Borrowed(ordinal, _) = component {
+                    if *ordinal != borrowed.len() {
+                        return err("§12.2", "borrowed component position mismatch");
+                    }
+                    let wires = q.allocate(value.width())?;
+                    set(&mut q, &wires, value)?;
+                    borrowed.push(wires.clone());
+                    b.borrowed.push(wires);
                 }
-                let wires = q.allocate(v.width())?;
-                set(&mut q, &wires, v)?;
+            }
+        } else {
+            let borrowed_widths = if let Some(context) = context {
+                context.borrowed_widths.clone().ok_or_else(|| {
+                    Error::new(
+                        "§12.2 K70: replay invocation has no checked borrow lifetime inventory"
+                            .into(),
+                    )
+                })?
+            } else {
+                self.checked_borrow_lifetimes(&f.name)?.ok_or_else(|| {
+                    Error::new(
+                        "§12.2 K70: checked borrow lifetime inventory requires linked actions"
+                            .into(),
+                    )
+                })?
+            };
+            crate::reserve_more(
+                &mut borrowed,
+                borrowed_widths.len(),
+                "§12.2 K70",
+                "borrowed replay systems",
+            )?;
+            for (ordinal, width) in borrowed_widths.iter().copied().enumerate() {
+                let value = element.iter().find_map(|(component, value)| {
+                    matches!(component, Component::Borrowed(position, _) if *position == ordinal).then_some(value)
+                });
+                let zero;
+                let value = match value {
+                    Some(value) if value.width() == width => value,
+                    Some(_) => {
+                        return err(
+                            "§12.2 K72",
+                            "borrowed replay width differs from checked lifetime",
+                        )
+                    }
+                    None => {
+                        zero = BitVector::zero(width)?;
+                        &zero
+                    }
+                };
+                let wires = q.allocate(width)?;
+                set(&mut q, &wires, value)?;
                 borrowed.push(wires.clone());
                 b.borrowed.push(wires);
             }
@@ -1100,7 +1174,11 @@ impl Object {
                 .filter(|(c, _)| matches!(c, Component::Borrowed(..)))
                 .map(|(_, v)| v.to_decimal())
                 .collect();
-            let k = borrowed_in.len();
+            let k = if self.isa_version == crate::IsaVersion::V09 {
+                domain.borrowed_widths.len()
+            } else {
+                borrowed_in.len()
+            };
             let split = out
                 .len()
                 .checked_sub(k)
@@ -1150,6 +1228,7 @@ mod r20_tests {
             u64::MAX as u128,
         ] {
             let d = Domain {
+                borrowed_widths: Vec::new(),
                 covers_d: false,
                 components: vec![(
                     Component::Bundle(0, 0),
diff --git a/reference-interpreter/src/claims/pairs09.rs b/reference-interpreter/src/claims/pairs09.rs
index f280d2a..ccf0ebf 100644
--- a/reference-interpreter/src/claims/pairs09.rs
+++ b/reference-interpreter/src/claims/pairs09.rs
@@ -157,7 +157,13 @@ pub(super) fn args_domain(
     Ok(args)
 }
 fn full_quantum_domain(object: &Object, g: &Function, domain: &Json) -> Result<()> {
-    crate::certificate::domain_for(domain, g, crate::IsaVersion::V09, 0)?;
+    crate::certificate::domain_for(
+        domain,
+        g,
+        crate::IsaVersion::V09,
+        0,
+        object.checked_borrow_lifetimes(&g.name)?.as_deref(),
+    )?;
     if !domain.get("borrowed")?.array()?.is_empty()
         || domain
             .object()?
diff --git a/reference-interpreter/src/claims/replay09.rs b/reference-interpreter/src/claims/replay09.rs
index f3e4323..4c5a134 100644
--- a/reference-interpreter/src/claims/replay09.rs
+++ b/reference-interpreter/src/claims/replay09.rs
@@ -9,6 +9,7 @@ pub(super) struct Invocation {
     pub controls: Vec<BitVector>,
     pub adjoint: bool,
     pub budget: Budget,
+    pub borrowed_widths: Option<Vec<usize>>,
 }
 
 #[cfg(test)]
@@ -88,12 +89,10 @@ fn coverage(
                 })?;
         }
     }
-    for (c, width, ..) in &domain.domain.components {
-        if matches!(c, Component::Borrowed(..)) {
-            bits = bits.checked_add(*width).ok_or_else(|| {
-                crate::resource_error("§12.2 K74", "borrowed width exceeds usize")
-            })?;
-        }
+    for width in &domain.domain.borrowed_widths {
+        bits = bits
+            .checked_add(*width)
+            .ok_or_else(|| crate::resource_error("§12.2 K74", "borrowed width exceeds usize"))?;
     }
     let power = |exponent: usize| -> Result<String> {
         let width = exponent
@@ -163,7 +162,14 @@ impl Object {
             }
             bindings.get("invocation")?
         };
-        self.decode_invocation09(invocation, f)
+        let mut invocation = self.decode_invocation09(invocation, f)?;
+        invocation.borrowed_widths =
+            Some(self.checked_borrow_lifetimes(&f.name)?.ok_or_else(|| {
+                Error::new(
+                    "§12.2 K70: checked borrow lifetime inventory requires linked actions".into(),
+                )
+            })?);
+        Ok(invocation)
     }
 
     pub(super) fn decode_invocation09(
@@ -211,6 +217,9 @@ impl Object {
             controls: Vec::new(),
             adjoint: false,
             budget,
+            // K92 uses this decoder without replay or a linked borrow closure.
+            // Only invocation09 attaches a checked replay inventory.
+            borrowed_widths: None,
         })
     }
 
@@ -273,7 +282,7 @@ impl Object {
         f: &Function,
         flat: &[BitVector],
         controls: usize,
-        borrowed: usize,
+        borrowed_widths: &[usize],
     ) -> Result<Json> {
         let bundle_count = controls
             + f.params
@@ -300,9 +309,19 @@ impl Object {
                 offset = end;
             }
         }
-        if flat.len() != offset + borrowed {
+        if flat.len() != offset + borrowed_widths.len() {
             return err("§12.1 K13", "executor tuple length differs from interface");
         }
+        if flat[offset..]
+            .iter()
+            .zip(borrowed_widths)
+            .any(|(value, width)| value.width() != *width)
+        {
+            return err(
+                "§12.1 K13",
+                "executor borrowed tuple width differs from checked lifetime",
+            );
+        }
         Ok(Json::Object(BTreeMap::from([
             (
                 "bundles".into(),
@@ -321,6 +340,7 @@ impl Object {
         f: &Function,
         element: &[(Component, BitVector)],
         controls: usize,
+        borrowed_widths: &[usize],
     ) -> Result<Vec<BitVector>> {
         let find = |component: Component, width| {
             element
@@ -329,6 +349,7 @@ impl Object {
                     (match (&component, c) {
                         (Component::Control(a), Component::Control(b)) => a == b,
                         (Component::Bundle(a, b), Component::Bundle(c, d)) => (a, b) == (c, d),
+                        (Component::Borrowed(a, _), Component::Borrowed(b, _)) => a == b,
                         (Component::Cell(a, b, c), Component::Cell(d, e, f)) => {
                             (a, b, c) == (d, e, f)
                         }
@@ -366,11 +387,9 @@ impl Object {
                 }
             }
         }
-        out.extend(
-            element
-                .iter()
-                .filter_map(|(c, v)| matches!(c, Component::Borrowed(..)).then_some(v.clone())),
-        );
+        for (ordinal, width) in borrowed_widths.iter().copied().enumerate() {
+            out.push(find(Component::Borrowed(ordinal, String::new()), width)?);
+        }
         Ok(out)
     }
 
@@ -381,6 +400,24 @@ impl Object {
         claim: &Json,
         f: &Function,
     ) -> Result<Outcome> {
+        let result = self.replay09(closure, index, claim, f);
+        match result {
+            Err(error)
+                if error.kind() == crate::ErrorKind::HostResource
+                    && claim.get("expected")? != &Json::String("inverse_pair".into()) =>
+            {
+                Ok(Outcome {
+                    verdict: ClaimVerdict::Unverified(format!(
+                        "§12.2 K75: unchecked (host limit): {error}"
+                    )),
+                    coverage: None,
+                })
+            }
+            result => result,
+        }
+    }
+
+    fn replay09(&self, closure: &str, index: usize, claim: &Json, f: &Function) -> Result<Outcome> {
         if claim.get("expected")? == &Json::String("inverse_pair".into()) {
             return Ok(Outcome {
                 verdict: self.verify_inverse_pair_claim09(f, index, claim)?,
@@ -399,6 +436,14 @@ impl Object {
                 coverage: None,
             });
         }
+        if self.checked_borrow_lifetimes(&f.name)?.is_none() {
+            return Ok(Outcome {
+                verdict: ClaimVerdict::Unverified(
+                    "§12.2 K70: checked borrow lifetime inventory requires linked actions".into(),
+                ),
+                coverage: None,
+            });
+        }
         let mut invocation = self.invocation09(claim, f, closure)?;
         let controls = usize::try_from(claim.get("subject")?.get("inherited_controls")?.uint()?)
             .map_err(|_| crate::resource_error("§12.1 K13", "control count exceeds usize"))?;
@@ -467,11 +512,7 @@ impl Object {
                 "expected program has an incompatible signature",
             );
         }
-        let borrowed = domain
-            .components
-            .iter()
-            .filter(|(c, ..)| matches!(c, Component::Borrowed(..)))
-            .count();
+        let borrowed_widths = &domain.borrowed_widths;
         for (row, values) in elements.iter().enumerate() {
             let mut element = domain
                 .components
@@ -488,7 +529,7 @@ impl Object {
                 "replay fixed cells",
             )?;
             element.extend(resolved.fixed_cells.iter().cloned());
-            let before = self.entry09(f, &element, controls)?;
+            let before = self.entry09(f, &element, controls, borrowed_widths)?;
             invocation.controls = before[..controls].to_vec();
             let after = self.execute_element_bound(
                 f,
@@ -499,8 +540,8 @@ impl Object {
             )?;
             if let Some(table) = table {
                 let entry = &table[row];
-                if entry.get("before")? != &self.tuple09(f, &before, controls, borrowed)?
-                    || entry.get("after")? != &self.tuple09(f, &after, controls, borrowed)?
+                if entry.get("before")? != &self.tuple09(f, &before, controls, borrowed_widths)?
+                    || entry.get("after")? != &self.tuple09(f, &after, controls, borrowed_widths)?
                 {
                     return err(
                         "§12.1 K13",
diff --git a/reference-interpreter/tests/isa09_borrow_inventory.rs b/reference-interpreter/tests/isa09_borrow_inventory.rs
new file mode 100644
index 0000000..2f9ddfd
--- /dev/null
+++ b/reference-interpreter/tests/isa09_borrow_inventory.rs
@@ -0,0 +1,43 @@
+mod support;
+use bennett_isa_ref::Object;
+
+#[test]
+fn checked_lifetimes_keep_repeated_transitive_and_adjoint_allocations_in_order() {
+    let signature = r#"{"abi":"0.8","args":[],"bounds":[3],"in":[],"kind":"perm_action","mem":[],"mut":[1],"tier":"q"}"#;
+    let child_signature = signature.replace("[3]", "[]");
+    let root = "perm_action @root (t:wire mut) () () () ()\nregs {  } bounds {3}\n^entry():\naction_call @child (t) () () ()\nqloop 3 {\naction_call @child (t) () () ()\n}\nadj action_call @child (t) () () ()";
+    let child = "perm_action @child (t:wire mut) () () () ()\n^entry():\nb = qborrow any 1\nqreturn b\nc = qborrow any 2\nqreturn c";
+    let source = support::object(
+        &[
+            ("root", signature, root),
+            ("child", &child_signature, child),
+        ],
+        "{}",
+        "",
+    )
+    .replace("0.8", "0.9");
+    let object = support::rehash(&source);
+    let before = object.text.clone();
+    // First child [1,2], three repeated children [1,2] each, adjoint [2,1].
+    assert_eq!(
+        object.checked_borrow_lifetimes("root").unwrap().unwrap(),
+        vec![1, 2, 1, 2, 1, 2, 1, 2, 2, 1]
+    );
+    assert_eq!(
+        object.checked_borrow_lifetimes("child").unwrap().unwrap(),
+        vec![1, 2]
+    );
+    assert_eq!(object.text, before);
+}
+
+#[test]
+fn zero_trip_has_no_lifetimes_and_qif_visits_both_unconditional_arms() {
+    let signature = r#"{"abi":"0.8","args":[],"bounds":[0],"in":[1],"kind":"perm_action","mem":[],"mut":[1],"tier":"q"}"#;
+    let body = "perm_action @a (t:wire mut) (p:wire in) () () ()\nregs {  } bounds {0}\n^entry():\nqloop 0 {\nb = qborrow any 7\nqreturn b\n}\nqif p {\nc = qborrow any 1\nqreturn c\n} {\nd = qborrow any 2\nqreturn d\n}";
+    let source = support::object(&[("a", signature, body)], "{}", "").replace("0.8", "0.9");
+    let object = support::rehash(&source);
+    assert_eq!(
+        object.checked_borrow_lifetimes("a").unwrap().unwrap(),
+        vec![1, 2]
+    );
+}
diff --git a/reference-interpreter/tests/isa09_claim_replay.rs b/reference-interpreter/tests/isa09_claim_replay.rs
index 767e4b4..06a67f2 100644
--- a/reference-interpreter/tests/isa09_claim_replay.rs
+++ b/reference-interpreter/tests/isa09_claim_replay.rs
@@ -102,15 +102,19 @@ fn typed_oracle(argument: &str, steps: u64) -> Object {
         "\nsection layout\n{\"A_tab\":1,\"H\":2,\"S_cells\":0,\"globals\":{},\"heap_base\":3,\"heap_limit_max\":0,\"interface_regions\":{\"sum\":{\"db\":{\"base\":1}}},\"null_size\":1,\"ptr_width\":2}\n")
         .replace("=0.8", "=0.9").replace("\"0.8\"", "\"0.9\"").replace("ptr_width=32", "ptr_width=2");
     let object = support::rehash(&source);
+    assert_eq!(
+        object.checked_borrow_lifetimes("sum").unwrap(),
+        Some(vec![])
+    );
     let mut claim = support::json(
         r#"{
         "kind":"exhaustive","subject":{"closure_hash":"","variant":"forward","inherited_controls":0},
         "invocation":{"args":["2"],"budget":["2","0","0","0"]},
         "domain":{"bundles":[{"name":"x","width":2,"lo":1,"hi":1},{"name":"t","width":2,"lo":2,"hi":2},{"name":"f","width":4,"lo":3,"hi":3}],
-          "borrowed":[{"name":"dirty","width":1,"lo":1,"hi":1}],
+          "borrowed":[],
           "regions":[{"name":"db","cells":[{"index":0,"lo":2,"hi":2},{"index":1,"lo":1,"hi":1}]}]},
-        "expected":{"table":[{"before":{"bundles":["1","2","3"],"borrowed":["1"],"regions":[["2","1"]]},
-                               "after":{"bundles":["1","1","3"],"borrowed":["1"],"regions":[["2","1"]]}}]}}
+        "expected":{"table":[{"before":{"bundles":["1","2","3"],"borrowed":[],"regions":[["2","1"]]},
+                               "after":{"bundles":["1","1","3"],"borrowed":[],"regions":[["2","1"]]}}]}}
     "#,
     );
     fields(fields(&mut claim).get_mut("invocation").unwrap()).insert(
@@ -146,7 +150,7 @@ fn standalone_oracle_binds_its_own_argument_budget_and_complete_interface() {
         let error = verify_root(&object).unwrap_err().to_string();
         assert!(error.contains("full tuple mismatch"), "{error}");
     }
-    for field in ["bundles", "borrowed", "regions"] {
+    for field in ["bundles", "regions"] {
         let object = changed(&typed_oracle("2", 2).text, |claim| {
             let table = fields(fields(claim).get_mut("expected").unwrap())
                 .get_mut("table")
@@ -369,10 +373,7 @@ fn fixed_image_oracle() -> Object {
             {"name":"f","width":4,"lo":0,"hi":15}]"#,
             ),
         );
-        fields(domain).insert(
-            "borrowed".into(),
-            support::json(r#"[{"name":"dirty","width":1,"lo":0,"hi":1}]"#),
-        );
+        fields(domain).insert("borrowed".into(), support::json("[]"));
         fields(domain).insert("regions".into(), support::json("[]"));
         fields(domain).insert(
             "fixed_regions".into(),
@@ -385,11 +386,12 @@ fn fixed_image_oracle() -> Object {
         for x in 0..4 {
             for t in 0..4 {
                 for f in 0..16 {
-                    for b in 0..2 {
-                        rows.push(support::json(&format!(r#"{{
-                "before":{{"bundles":["{x}","{t}","{f}"],"borrowed":["{b}"],"regions":[["2","1"]]}},
-                "after":{{"bundles":["{x}","{}","{f}"],"borrowed":["{b}"],"regions":[["2","1"]]}}}}"#, t^((x+2)&3))));
-                    }
+                    rows.push(support::json(&format!(
+                        r#"{{
+                "before":{{"bundles":["{x}","{t}","{f}"],"borrowed":[],"regions":[["2","1"]]}},
+                "after":{{"bundles":["{x}","{}","{f}"],"borrowed":[],"regions":[["2","1"]]}}}}"#,
+                        t ^ ((x + 2) & 3)
+                    )));
                 }
             }
         }
@@ -414,7 +416,7 @@ fn fixed_image_metadata_is_admitted_without_inspecting_quantum_state() {
             coverage.full_domain_elements.as_str(),
             coverage.covered_fraction.as_str()
         ),
-        (512, "33554432", "1/65536")
+        (256, "16777216", "1/65536")
     );
     assert_eq!(coverage.fixed_regions.len(), 1);
     assert_eq!(coverage.fixed_regions[0].sha256, sha256_hex(&[2, 1]));
@@ -475,5 +477,5 @@ fn sampled_singleton_report_has_exact_distinct_coverage() {
     let report = object.verify_certificate().unwrap().claims.remove(0);
     assert_eq!(report.verdict, ClaimVerdict::Evidence { elements: 1 });
     let coverage = report.coverage.unwrap();
-    assert_eq!(coverage.covered_fraction, "1/33554432");
+    assert_eq!(coverage.covered_fraction, "1/16777216");
 }
diff --git a/reference-interpreter/tests/isa09_fixed_image.rs b/reference-interpreter/tests/isa09_fixed_image.rs
index 4583238..c247c99 100644
--- a/reference-interpreter/tests/isa09_fixed_image.rs
+++ b/reference-interpreter/tests/isa09_fixed_image.rs
@@ -50,6 +50,184 @@ fn claim(record: &mut Json) -> &mut Json {
     &mut claims[0]
 }
 
+fn program_relation(c: &mut Json) {
+    let hash = c
+        .get("subject")
+        .unwrap()
+        .get("closure_hash")
+        .unwrap()
+        .clone();
+    fields(c).insert(
+        "expected".into(),
+        Json::Object(BTreeMap::from([("program".into(), hash)])),
+    );
+}
+
+#[test]
+fn council_ghost_borrowed_position_rejects_admission() {
+    let text = mutate(&fixture("image-0102"), |record| {
+        let c = claim(record);
+        program_relation(c);
+        fields(fields(c).get_mut("domain").unwrap()).insert(
+            "borrowed".into(),
+            support::json(r#"[{"name":"ghost","width":1,"lo":0,"hi":1}]"#),
+        );
+    });
+    let error =
+        Object::parse(&text).expect_err("a source without qborrow cannot acquire a ghost lifetime");
+    assert!(error.to_string().contains("§12.2"), "{error}");
+}
+
+#[test]
+fn council_borrowed_width_two_rejects_one_bit_lifetime() {
+    let text = mutate(&fixture("controlled-dirty"), |record| {
+        let c = claim(record);
+        program_relation(c);
+        fields(fields(c).get_mut("domain").unwrap()).insert(
+            "borrowed".into(),
+            support::json(r#"[{"name":"b","width":2,"lo":0,"hi":3}]"#),
+        );
+    });
+    let error = Object::parse(&text).expect_err("the checked lifetime has exactly one bit");
+    assert!(error.to_string().contains("§12.2"), "{error}");
+}
+
+fn omitted_borrowed_slice(program: bool, label: Option<&str>) -> String {
+    mutate(&fixture("controlled-dirty"), |record| {
+        let c = claim(record);
+        fields(fields(c).get_mut("domain").unwrap()).insert("borrowed".into(), support::json("[]"));
+        if program {
+            program_relation(c);
+        } else {
+            let Json::Array(rows) = fields(fields(c).get_mut("expected").unwrap())
+                .get_mut("table")
+                .unwrap()
+            else {
+                panic!("table");
+            };
+            // K71 holds the omitted lifetime at zero. The original complete
+            // tuples already include that unchanged borrowed system.
+            rows.retain(|row| {
+                row.get("before").unwrap().get("borrowed").unwrap() == &support::json(r#"["0"]"#)
+            });
+            assert_eq!(rows.len(), 128);
+        }
+        if let Some(label) = label {
+            fields(c).insert("label".into(), Json::String(label.into()));
+        }
+    })
+}
+
+fn check_omitted_borrowed_slice(program: bool) {
+    for label in [None, Some("evidence")] {
+        let object = Object::parse(&omitted_borrowed_slice(program, label)).unwrap();
+        object.check_hashes().unwrap();
+        let expected = ClaimVerdict::Evidence { elements: 128 };
+        assert_eq!(object.verify_claim(root(&object), 0).unwrap(), expected);
+        let report = object.verify_certificate().unwrap().claims.remove(0);
+        assert_eq!(report.verdict, expected);
+        let coverage = report.coverage.unwrap();
+        // 1 control + 1 target + 4 fault + 1 address + 16 image + 1 borrow
+        // = 24 unrestricted bits; 2*2*16*2 = 128 replayed zero-borrow tuples.
+        assert_eq!(coverage.elements, 128);
+        assert_eq!(coverage.full_domain_elements, "16777216");
+        assert_eq!(coverage.covered_fraction, "1/131072");
+        assert_eq!(coverage.fixed_regions.len(), 1);
+        assert_eq!(
+            coverage.fixed_regions[0].sha256,
+            bennett_isa_ref::sha256_hex(&[1, 2])
+        );
+    }
+    for label in ["proof", "proof_relative_to_image"] {
+        let object = Object::parse(&omitted_borrowed_slice(program, Some(label))).unwrap();
+        assert!(object.verify_claim(root(&object), 0).is_err(), "{label}");
+        assert!(object.verify_certificate().is_err(), "{label}");
+    }
+}
+
+#[test]
+fn council_omitted_borrowed_program_is_zero_slice_evidence() {
+    check_omitted_borrowed_slice(true);
+}
+
+#[test]
+fn council_omitted_borrowed_complete_table_is_zero_slice_evidence() {
+    check_omitted_borrowed_slice(false);
+}
+
+#[test]
+fn checked_borrowed_output_is_part_of_the_complete_relation() {
+    let text = mutate(&fixture("controlled-dirty"), |record| {
+        let c = claim(record);
+        let Json::Array(rows) = fields(fields(c).get_mut("expected").unwrap())
+            .get_mut("table")
+            .unwrap()
+        else {
+            panic!("table");
+        };
+        fields(fields(&mut rows[0]).get_mut("after").unwrap())
+            .insert("borrowed".into(), support::json(r#"["1"]"#));
+    });
+    let object = Object::parse(&text).unwrap();
+    for result in [
+        object.verify_claim(root(&object), 0).map(|_| ()),
+        object.verify_certificate().map(|_| ()),
+    ] {
+        let error = result.unwrap_err().to_string();
+        assert!(error.contains("full tuple mismatch"), "{error}");
+    }
+}
+
+#[test]
+fn council_host_limited_claim_retains_later_claim_and_no_coverage() {
+    for label in [None, Some("proof"), Some("proof_relative_to_image")] {
+        let text = mutate(&fixture("image-0102"), |record| {
+            let original = claim(record).clone();
+            let c = claim(record);
+            fields(c).insert("kind".into(), Json::String("sampled".into()));
+            program_relation(c);
+            fields(c).insert("sampler".into(),support::json(r#"{"algorithm":"xoshiro256**","seed":["1","0","0","0"],"count":"18446744073709551615"}"#));
+            if let Some(label) = label {
+                fields(c).insert("label".into(), Json::String(label.into()));
+            }
+            let Json::Array(claims) = fields(record).get_mut("claims").unwrap() else {
+                panic!("claims");
+            };
+            claims.push(original);
+        });
+        let object = Object::parse(&text).unwrap();
+        object.check_hashes().unwrap();
+        let direct = object
+            .verify_claim(root(&object), 0)
+            .expect("legal host-limited claims have a verdict");
+        let ClaimVerdict::Unverified(reason) = &direct else {
+            panic!("host limit discharged a claim: {direct:?}");
+        };
+        assert!(
+            reason.contains("§12.2")
+                && reason.contains("unchecked (host limit)")
+                && reason.contains("18446744073709551615"),
+            "{reason}"
+        );
+        let reports = object
+            .verify_certificate()
+            .expect("later independent claims survive")
+            .claims;
+        assert_eq!(reports.len(), 2);
+        assert_eq!(reports[0].verdict, direct);
+        assert_eq!(reports[0].closure_hash, root(&object));
+        assert_eq!(reports[0].index, 0);
+        assert_eq!(reports[0].context_key, support::json("[]"));
+        assert!(reports[0].coverage.is_none());
+        assert_eq!(reports[1].index, 1);
+        assert_eq!(reports[1].verdict, ClaimVerdict::ProofRelativeToImage);
+        let coverage = reports[1].coverage.as_ref().unwrap();
+        assert_eq!(coverage.elements, 64);
+        assert_eq!(coverage.full_domain_elements, "4194304");
+        assert_eq!(coverage.covered_fraction, "1/65536");
+    }
+}
+
 #[test]
 fn published_fixed_image_vectors_replay_with_exact_coverage_and_bindings() {
     let manifest = Json::parse(include_str!(
```

## Implementer receipts (job/isa-k86 PROGRESS.md, verbatim)
# Resume

STOPPED as maintainer directed (2026-11-08T12:35Z, restated): finish K85 fixes to green, preserve the K86 committed/backed-up checkpoint, start no further K86 clause or follow-on work. Final verification recorded by date -u: Sun Nov  8 13:19:36 UTC 2026.

Head: 04d5fc381cf906a007c17657e4f320129527906c, branch job/isa-k86, backed up to origin refs/heads/wip/isa-k86 (remote equality checked). Tracked working tree clean; only private .tmp evidence untracked. No rebase/merge, main push, .beads commit, full repo gate, sub-agent or sibling source edit. Orchestrator merges K93 first, rebases later and reviews shared borrow.rs lines; K85 council round2/full gate remain orchestrator-owned. No K93 blocker was delivered.

K85-fix commits (separate from K86):
- 8cf1f86: ONE read-only Object::checked_borrow_lifetimes accessor plus tests. borrow.rs diff is +88/-0; existing compiler semantics unchanged. It reads Borrow/Repeat/transitive Call facts; repeated and adjoint allocations remain ordered, zero-trip contributes none, both qif arms retain unconditional lifetimes. Unknown linked source is None, not a proven empty inventory.
- aae0cff: shared checked inventory for domain admission, tuple widths/counts, missing-zero replay systems, full-D denominator and proof classification; exact council regressions and K75 per-claim host-limit outcomes, retaining later reports. Admission host limits defer the inventory obligation to the replay boundary; known semantic errors remain rejection.
- 31c3b80: SPEC-QUESTIONS.md §34 records labels reading A, reasons, bennett-isa-spec-b7k and council round1 B-K85-2; no label-policy behavior change.
- 04d5fc3: preserve frozen0.8 flat tuple/idle-pool behavior; generic K92 invocation decoding leaves checked replay inventory unset, and only the replay invocation binder attaches it. This preserves unresolved-import applicability reports.
All messages end Agent: gpt-6.1-sol and each commit was backed up.

Clause disposition:
| Clause | Result |
| --- | --- |
| §12.2 K69/K70/K72 checked positions/widths | Extra ghost and width2/hi3 on a checked one-bit lifetime reject admission |
| §12.1 K13 / §12.2 K71/K85 omission/full tuples/coverage | Both table and program forms preserve omitted b=0; Evidence{elements:128}, fullD=16777216, fraction1/131072; proof/image-relative requests reject |
| §12.2 K75 | count=18446744073709551615 claim0 yields Unverified("§12.2 K75: unchecked (host limit): ..."), coverage=None; original claim1 still reports conditional theorem with64/4194304=1/65536; requested proof labels remain unchecked |
| §12.2 labels (b7k) | Reading A documented; common field, kind-independent rejection, unchecked/Unverified exempt and never satisfy a label |
| K86 | Exact arithmetic/interval/process helpers only; model/target/schedule reconstruction and vectors remain incomplete |

Exact red-first council witnesses are committed tests in isa09_fixed_image.rs. Command:
python3 .tmp/isa-k86/run.py k85-council-red short cargo test --offline --manifest-path reference-interpreter/Cargo.toml --test isa09_fixed_image council_ -- --nocapture
Before fixes: exit101,0 passed,5 intended failures (four witnesses, omitted table/program separate). Quotes:
- ghost: “a source without qborrow cannot acquire a ghost lifetime: Object ...” (admission wrongly succeeds).
- width2/hi3: “the checked lifetime has exactly one bit: Object ...” (admission wrongly succeeds).
- omitted table: “§12: §12.1 K13: incomplete borrowed tuple”.
- omitted program: “§5.6: designated idle set lacks requested borrowed wires”.
- huge sampled claim: “legal host-limited claims have a verdict: Error(... sampled domain elements allocation of 18446744073709551615 elements failed ... HostResource)”.
Green quotes in k85-focused-committable.log and the final full reference log: council_ghost_borrowed_position_rejects_admission ... ok; council_borrowed_width_two_rejects_one_bit_lifetime ... ok; council_omitted_borrowed_program_is_zero_slice_evidence ... ok; council_omitted_borrowed_complete_table_is_zero_slice_evidence ... ok; council_host_limited_claim_retains_later_claim_and_no_coverage ... ok. Both public APIs and requested-label variants are asserted. Expected values are independently derived from the council's source relation, never copied from interpreter output.

Accessor red: k85-accessor-red receipt, missing checked_borrow_lifetimes, exit101. Valid accessor green: k85-accessor-green-valid,2 passed. Two intermediate accessor fixture drafts had malformed bounds/regs syntax; those are not semantic red evidence.

SOLE INVENTORY receipt: .tmp/isa-k86/borrowed-inventory-grep-final.txt, generated after all fixes with:
rg -n 'borrowed_widths|checked_borrow_lifetimes|admission_borrow_lifetimes|domain_for\(|get\("borrowed"\)' reference-interpreter/src/certificate.rs reference-interpreter/src/claims.rs reference-interpreter/src/claims/replay09.rs
Quoted consumers: claims.rs “self.checked_borrow_lifetimes(&f.name)?”; width validation “borrowed_widths.get(ordinal) != Some(&width)”; completeness compares listed length with resolver length; 0.9 replay iterates “borrowed_widths.iter().copied().enumerate()”; replay09 coverage sums “&domain.domain.borrowed_widths”; tuple/entry conversion receives “&domain.borrowed_widths”; certificate.rs passes “self.admission_borrow_lifetimes(f)?” to domain_for/table09. In ISA0.9, domain.borrowed is no longer an inventory anywhere: it supplies only labels/ranges validated against the resolver, plus a completeness check. Complete tuple shape, omitted zero systems and unrestricted D derive solely from checked widths. Frozen ISA0.8 retains its prior explicit flat tuple encoding, with a visible version branch; it does not supply a 0.9 checked inventory. Object::borrow_capacity is unused by the resolver.

Necessary test-fixture correction: the older typed_oracle helper invented a dirty borrowed entry although its oracle source has no checked lifetime. Its legal domain now has borrowed=[],24 bits (2 input+2 target+4 fault+16 region), singleton1/16777216 and fixed-image256/16777216=1/65536. All real input/fault/address/image ranges and arithmetic assertions remain. The borrowed-output mismatch assertion now uses the checked lifetime in controlled-dirty (checked_borrowed_output_is_part_of_the_complete_relation); both checker APIs must reject a changed borrowed output. Existing entangled dirty/reference tests remain. No published vector/source/object/catalog bytes changed, and no test was skipped/ignored or weakened to accept a wrong result.

Verification on the frozen final implementation (run.py supplies headless env/private TMPDIR/CARGO_TARGET_DIR,4 compiler jobs,4 test threads; full crates also use8GiB AS cap/core dumps off):
- Focused: cargo test --offline --manifest-path reference-interpreter/Cargo.toml --test isa09_fixed_image --test isa09_borrow_inventory --test isa09_claim_replay --test isa09_certificate --lib -- --test-threads=4 =>64 pass,exit0 (k85-focused-committable).
- Initial full reference k85-full-reference =>exit101,8 compatibility failures in4 targets. Corrected only the0.8/version routing and shared K92 decoder in04d5fc3. All failures and receipts retained.
- Affected targets plus focused/lib: k85-compatibility-green =>152 passed,0 failed,2 existing ignores,exit0.
- Full reference: python3 .tmp/isa-k86/run.py k85-full-reference-final moderate cargo test --offline --manifest-path reference-interpreter/Cargo.toml --no-fail-fast -- --test-threads=4 =>743 passed,0 failed,6 existing ignores,exit0;309.06s wall,416.42s CPU,1591040KiB peak RSS.
- Private CLI: cargo build --offline --manifest-path reference-interpreter/Cargo.toml =>exit0 (k85-final-cli). SHA256=12a429a4b8536be7916a797c3391c028f8c7dc09109cb7dd6fbddb72ba2c5d4f.
- Focused conformance with BENNETT_CONFORMANCE_BIN selecting that CLI: cargo test --offline --manifest-path conformance/Cargo.toml --test ref_k85 --test case_data -- --test-threads=4 =>6 pass,exit0.
- Full conformance with the same selected CLI: python3 .tmp/isa-k86/run.py k85-full-conformance moderate cargo test --offline --manifest-path conformance/Cargo.toml --no-fail-fast -- --test-threads=4 =>132 passed,0 failed/ignored,exit0;478.81s wall,809.30s CPU,722716KiB peak RSS.
- Both cargo fmt --manifest-path <crate>/Cargo.toml -- --check commands pass; git diff --check passes.
- Both crates pass cargo clippy --offline --manifest-path <crate>/Cargo.toml --lib --bins -- -D warnings (k85-clippy-reference-final and k85-clippy-conformance receipts). Conformance source remained unchanged throughout. No source changes after04d5fc3 or after either full run.

K86 committed checkpoint, retained without starting further clauses:34c9f0c exact arbitrary-precision Rational/binary64 bindings; ed1e4c7 directed binary interval operations, complex matrices, V†U-I Frobenius bounds, strict Hermitian LDL channel dual and rectangular K85 process helpers. Their7 independent helper tests pass in the full reference run. No connected target/model reader, native normalization/control/accuracy verifier, exact transcendental model evaluator, target/schedule invocation executor, certificate process dispatch or portable K86 vectors is implemented. Low-level process helpers are not executable certificate acceptance. No SET A need remains for the completed K85 slice; action.rs/validation.rs/source_constructor/action.rs/main.rs stayed unchanged.

Open: b-isa-spec-0ib remains IN_PROGRESS (not closed; depends on bennett-isa-spec-u94). K85 parent b-isa-spec-qrc remains open/in progress with bennett-isa-spec-rqn for conditional process/preparation/native attachment. b7k remains a published-text clarification; its requested reference reading is recorded. u94 records missing closed Kraus/instrument/explicit-control/enclosure-certificate encodings in §8.3; no producer encoding was invented. Existing scheduled/numerical/channel claims remain explicitly staged/Unverified.

Execution policy retained: always /home/tobias paths, owned SET B only with the narrow read-only borrow.rs grant. No repo hang-guard table/profile exists at this baseline; private classes derive from docs/quality.md measurements at>=10x: short1800s,moderate18000s,long30000s; exit124 UNKNOWN. TMPDIR=.tmp/isa-k86/tmp; CARGO_TARGET_DIR=.tmp/isa-k86/target; DISPLAY/WAYLAND_DISPLAY/DBUS_SESSION_BUS_ADDRESS/BROWSER unset. Final action: hand off this green checkpoint and STOP; only the orchestrator proceeds with K93-first integration, shared-line review, K85 council round2 and full gate. No further K86 clause or follow-on work is authorized in this run.
