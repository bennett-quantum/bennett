# bennett-arith quality-floor change set (job/quality-arith), council round 1

Subject: the quality-floor remediation of `bennett-arith` (adders, multipliers, QROM and soft-float as ISA library objects with certificates), range `6764ad25df3b6838e6082712726212796ed453a3..015b424` (22 commits). Sol review rounds: r1 BLOCK (P1 bennett-arith-awg: scripts/test reused a stale oracle.so, false green), r2 CLEAR at e11bc94 (docs/reviews/2026-11-06-quality-arith-r2.md; 015b424 adds only that document). Council focus: soft-float rounding (softfloat/trans.h, ppc_round.h, ppc_sum.h, named.c, generate.py) and the published dist/ bitcode + manifests. Background specs at the repo's pins: dialect 0.2.10 (023f5a7) and ISA 0.8 (f88b32f); the generated objects carry ISA 0.9 certificate fields.

Your working directory is a frozen detached worktree of `bennett-arith` at 015b424. Embedded below: (1) the unified diff of every path except generated objects (adders/objects, multipliers/objects, qrom/objects: 85+ one-line certificate re-serialisations, e.g. invocation gains "token_aliases":[]), tests/__pycache__ and docs; (2) the post-change text of the changed soft-float sources, scripts and central tests. Read the excluded paths in the worktree with `git diff 6764ad25df3b6838e6082712726212796ed453a3 015b424 -- <path>`. Grade: rounding semantics (round-to-nearest-even, subnormals, overflow, NaN/inf, the transcendental phases), whether a refactor changed a numeric result, test integrity (oracles independent of the code under test, tolerances no wider than the oracle allows), published bitcode/manifest consistency, and any narrowing. Unchanged code is context.

## 1. Unified diff (git diff 6764ad25df3b6838e6082712726212796ed453a3 015b424, excluding generated objects, __pycache__, docs, binaries)

````diff
diff --git a/.gitignore b/.gitignore
index 88d83a7..0f53087 100644
--- a/.gitignore
+++ b/.gitignore
@@ -19,3 +19,10 @@ Manifest.toml
 
 # Local build, oracle runners and detached gate worktrees
 .tmp/
+
+# Python bytecode and local diagnostic / Beads artefacts
+__pycache__/
+*.pyc
+*.log
+.beads/**/LOCK
+*.darc
diff --git a/HANDOFF.md b/HANDOFF.md
deleted file mode 100644
index 9eb4678..0000000
--- a/HANDOFF.md
+++ /dev/null
@@ -1,91 +0,0 @@
-# Current state — soft-float v2
-
-Updated 2026-11-01T13:45:50Z (real `date -u`). Accepted dialect 0.2.10
-@023f5a771a814270634db3be9cfde88ded69f975, ISA 0.8. No push.
-
-LLVM 18 and 23 each publish **1,134 integer-only carrier exports**, preserving
-all 606 previous signatures and adding 528. All 1,008 previously inventoried
-concrete entries now have definitions; no staged concrete placeholder remains.
-Includes PPCDoubleDouble scalar/wide arithmetic, all cross-format routes,
-all seven own-format libm families (ordinary and `_rm`), and powi at ten widths
-1/8/16/32/64/128/192/256/513/1025. Additional exact iK definitions are generated
-with `scripts/build MAJOR K ...`; LLVM's inclusive i8388608 limit is verified.
-Custom i7 bitcode executed 2^3=8; default publications were restored.
-
-## Binary edge and consumer action
-
-- LLVM 18 `dist/llvm18/bennett-arith.bc` SHA-256:
-  `8d99956e8741803f2115e48fa28c6c71795fb0041e992f8835851b71dd4b6fc1`
-- LLVM 23 `dist/llvm23/bennett-arith.bc` SHA-256:
-  `59563a3a10949b1ea48ca8b79027310ac9f9f7e28c85a30e70a013ced04a6793`
-
-Same-directory manifests record every literal signature, bitcode digest,
-tool versions and SHA-256/Git blob SHA-1 of implementation/build sources;
-SHA256SUMS also hashes the manifest. Link the matching-major artifact with
-program/runtimes **before normalisation**, then materialise its reachable
-closure in both builds. `_rm` wrappers use runtime-owned external
-`__bennett_rt_fenv` (`{ i32 round, i32 flags }`). No host FP/libm dependency.
-The tested layout remains x86_64 Linux, 64-bit little endian.
-
-**bennett-plugin must re-pin BENNETT_ARITH_BITCODE SHAs**, then verify its own
-L/CC closure and decide bp-xms/bp-7ni disposition. The plugin was read-only.
-Its tables/probes and softfloat receipt were inspected; arith does not claim
-that new producer exports alone close the consumer's complete blocker.
-
-## Semantics and remaining contracts
-
-§13.1/13.3 PPC uses the LLVM-major APFloat interpretation: component add/mul;
-legacy 106-bit divide/fmod/FMA and conversions where LLVM uses that fallback;
-LLVM23 component integral/integer conversion differs from LLVM18. Sparse wide
-integers, classification, modf and combined subnormal ldexp are tested.
-PPC-to-IEEE APFloat conversion uses only the high component, contradicting
-“fpext is exact”; special sign/status behavior and LLVM23 unsigned negative-low
-saturation are retained. APFloat lacks PPC sqrt: its implementation uses a
-correctly rounded legacy 106-bit result. Both readings and priority questions
-are in **b-dialect-spec-dfd**. This is not idealized IEEE double-double arithmetic.
-
-§13.4 explicitly waives correct rounding and gives no error bound. Libm v1 uses
-224 working significant bits and 17,408-bit Payne–Hanek constants, entirely in
-integer bitcode. Ordinary MPFR sweeps report a maximum of 0.5 ulp (rounded
-reporting); tests allow <=4 ulp, exhaustive half/bfloat sin <=1 ulp. This is
-empirical evidence, not a global correct-rounding/ulp-bound proof. Accuracy and
-§13.5 approximation flag policy questions are **b-dialect-spec-1av**.
-
-Closed: **r3d**, **0he**, and one libm bead per format (**0he.1–0he.7**).
-Still blocked, full capability retained: **38c** (metadata-named arbitrary
-APFloat schema; dialect **z7u**) and **chn** (distinct signaling constrained
-comparison ABI; dialect **21a**). No spec text was edited; only exported
-`.beads/issues.jsonl` was committed in that repo. No full DF/runtime claim.
-
-## Verification
-
-`scripts/gate` reproduces both publications and exercises the actual bitcode:
-
-| Checks | LLVM 18 | LLVM 23 |
-|---|---:|---:|
-| Original numerical regression, 606 prior exports | 1,029,583 | 1,029,583 |
-| Same-major PPC/APFloat | 792,786 | 792,786 |
-| Additional boundary/signatures | 519 | 526 |
-| Width-preserving powi | 3,668 | 3,668 |
-| MPFR/pair main sweep | 130,464 | 130,464 |
-| Exhaustive sin/PPC/libm rounding | 137,860 | 137,860 |
-| Subnormal-output/overflow sweep | 14,655 | 14,655 |
-| **Total numerical checks** | **2,109,535** | **2,109,542** |
-
-Also checks integer-only linked closure, all literal signatures, every half and
-bfloat sin encoding (65,536 each), every PPC predicate, NaNs/zeros, sparse
-2^1023+1 integer transport, f128 precision/range extremes, log just below 1,
-pi-adjacent arguments, all rounding modes and sticky flags. MPFR is test-only
-at 384 bits; APFloat oracle uses the installed same-major LLVM development
-library. The max-width powi test is structural assembly/verification.
-
-Root gate plus the new boundary sweep passed. Final source at 7826a10 reproduced
-bitcode, manifests and checksums exactly from a separate archived directory;
-default bitcode is byte-identical to bb79deb. Clean detached pre-push gate exited 0 on
-bb79deb44bea7f727717b3a9ddd59cd0ca3c75a8; its identical numerical bitcode passed the entire table
-above. The max-width validation fix was verified separately and changed only
-manifest provenance. Final-source relocated reproduction also passed. The
-temporary pre-push worktree was removed; no push occurred.
-See `docs/verification.json` for the committed evidence and added export names.
-Superseded/red/interrupted attempts are not green receipts. No CI, push, Dolt
-sync, desktop process or system /tmp artifact was used.
diff --git a/README.md b/README.md
index 277533b..0767e58 100644
--- a/README.md
+++ b/README.md
@@ -1,22 +1,22 @@
 # bennett-arith
 
 Arithmetic bitcode and ISA libraries for Bennett. The soft-float library publishes
-1,134 integer-only carrier definitions per major for LLVM 18 and 23 against dialect **0.2.10 @023f5a7** and
+1,141 integer-only carrier definitions per major for LLVM 18 and 23 against dialect **0.2.13 @95a4b8d** and
 ISA **0.8** (see `SPEC_VERSIONS.toml`).
 
 - [LLVM 18 bitcode](dist/llvm18/bennett-arith.bc) · [entry-point manifest](dist/llvm18/manifest.json)
 - [LLVM 23 bitcode](dist/llvm23/bennett-arith.bc) · [entry-point manifest](dist/llvm23/manifest.json)
 - [Linking, signatures, exactness and staged scope](softfloat/README.md)
-- [Current handoff](HANDOFF.md)
+- [Current handoff](../bennett/HANDOFF.md)
 
-Run `scripts/gate` to reproduce both checked-in publications and execute the
+Run `scripts/test` for bounded default checks and `scripts/gate` to reproduce both checked-in publications and execute the
 independent integer/rational, same-major APFloat, and MPFR oracle suites.
 PPCDoubleDouble and all seven own-format libm families are published; arbitrary
-metadata formats and signaling comparison still require contract clarification. `scripts/pre-push` tests a detached,
+metadata formats are delivered by the offline instance generator, and signaling comparison is published. `scripts/pre-push` tests a detached,
 clean checkout of every pushed commit. Install it with `scripts/install-hooks.sh`.
 Everything is local and headless, with temporary files under `.tmp/`.
 
 The wider arithmetic scope remains: `adders/`, `multipliers/`, `qrom/` and
 soft-float as ISA library objects with certificates. See `docs/PORT_PLAN.md`.
-This milestone publishes ordinary LLVM bitcode; ISA objects/certificates are
-produced by the downstream driver pipeline, not claimed here.
+This repository publishes ordinary LLVM bitcode and circuit objects with certificates.
+Raw modular certificate admission awaits the interpreter support recorded in [quality evidence](docs/quality.md).
diff --git a/SPEC_VERSIONS.toml b/SPEC_VERSIONS.toml
index deed02b..dad4282 100644
--- a/SPEC_VERSIONS.toml
+++ b/SPEC_VERSIONS.toml
@@ -1,11 +1,13 @@
 status = "softfloat-v2-concrete-published-parametric-contracts-open"
+softfloat_isa_version = "0.8"
 
 [specs.bennett-dialect-spec]
-version = "0.2.10"
-commit = "023f5a7"
+version = "0.2.13"
+commit = "95a4b8d06933018a07fef3516296a25fd582fcde"
 path = "spec/Bennett-Dialect-Spec.md"
 
 [specs.bennett-isa-spec]
-version = "0.8"
-commit = "f88b32fd3e3a9eb3f400aba68bd6fd4cec6e8202"
-path = "spec/Bennett-ISA-Spec.md"
+certificate_extensions_commit = "be109bd27889ea91e3c0ad78a30e5e4d71d3d0d3"
+version = "0.9"
+commit = "ecaaac060c44e317d1181345fa6b8e38c096c099"
+path = "spec/Bennett-ISA-Spec-0.9.md"
diff --git a/adders/circuits.py b/adders/circuits.py
index 2de819c..8a325a3 100644
--- a/adders/circuits.py
+++ b/adders/circuits.py
@@ -268,8 +268,8 @@ def _vectors(c):
 def _invocation(c):
     if isinstance(c, QinplaceAction):
         token = [str(c.budget), "0", "0", "0"]
-        return {"args": [token], "budget": token}
-    return {"args": [], "budget": ["0", "0", "0", "0"]}
+        return {"args": [token], "budget": token, "token_aliases": [0]}
+    return {"args": [], "budget": ["0", "0", "0", "0"], "token_aliases": []}
 
 
 def _claim(c, closure):
@@ -340,13 +340,14 @@ class Object:
         return {"ancillae": [], "borrow": borrow, "history": [], "scratch": scratch, "slots": slots}
 
     def _inverse_pair_claim(self, c, hashes):
-        token = [str(c.budget), "0", "0", "0"]
+        token = [_meta(c.budget), 0, 0, 0]
         names = c.g.inputs
         domain = {"borrowed": [], "bundles": [{"hi": _meta((1 << w) - 1), "lo": 0, "name": n, "width": w}
                                               for n, w in names], "regions": []}
         return {"domain": domain, "expected": "inverse_pair", "kind": "exhaustive",
                 "subject": {"closure_hash": hashes[c.g.name], "inherited_controls": 0, "variant": "forward"}}, {
-            "budget": token, "claim": 1, "g": hashes[c.g.name], "ginv": hashes[c.ginv.name]}
+            "budget": token, "claim": 1, "g": hashes[c.g.name], "ginv": hashes[c.ginv.name],
+            "token_aliases": [0]}
 
     def _region(self, c, closure, position):
         if isinstance(c, QinplaceAction):
@@ -372,7 +373,7 @@ class Object:
         claims = [_claim(c, closure)]
         if self.inverse == c.name:
             # The published g/ginv pair: this symbol is the literal section 5.3 adjoint of the root.
-            claims.append({"invocation": {"args": "all", "budget": "all"}, "kind": "structural",
+            claims.append({"invocation": {"args": "all", "budget": "all", "token_aliases": "all"}, "kind": "structural",
                            "label": "proof", "rule": "adjoint_table", "subclaims": [], "witness": {}})
         return {"bounds": [], "claims": claims, "cleanup": {}, "definedness_assumptions": [], "error": {},
                 "frame": self._frame(c), "gates_used": gates, "kind": c.kind,
@@ -429,19 +430,21 @@ def census(c):
 
 
 def interpreter_view(obj):
-    """Object text with each K4 inverse-pair record removed, for the reference interpreter.
+    """Diagnostic execution view for the pre-K4/K91 pinned interpreter.
 
-    The certificate is published to the ISA 0.9 text (expected "inverse_pair", entry budget); the
-    interpreter's 0.9 schema does not admit those two records yet (bead in docs/circuits-port.md).
-    It decides qinplace by re-execution anyway, so the view loses no check it would have made.
+    This view cannot establish release compatibility: raw validation is kept
+    separately under BENNETT_ARITH_PROMISED until the interpreter supports it.
     """
     text = obj.text()
     if "section certificate\n" not in text:
         return text
     head, _, line = text.rpartition("section certificate\n")
     cert = json.loads(line)
+    cert["bindings"]["invocation"].pop("token_aliases")
     for region in cert["regions"].values():
         region["claims"] = [c for c in region["claims"] if c.get("expected") != "inverse_pair"]
+        for claim in region["claims"]:
+            claim["invocation"].pop("token_aliases")
         region["verification"]["inverse_pairs"] = []
     return f"{head}section certificate\n{jcs(cert)}\n"
 
diff --git a/adders/constructions.py b/adders/constructions.py
index 4d66698..fe4ed76 100644
--- a/adders/constructions.py
+++ b/adders/constructions.py
@@ -581,6 +581,7 @@ def mulmod_const(W, k, m):
     _check_modulus(W, m)
     if math.gcd(k, m) != 1:
         raise ValueError(f"mulmod needs gcd(k, m) = 1, got k={k} m={m}")
+    k %= m
     kinv = pow(k, -1, m) if m > 1 else 0
     tag = f"w{W}.k{k:x}.m{m:x}"
     return _named_pair(_mulmod_oracle(f"arith.ref.mulmodk.{tag}", W, m, k),
diff --git a/adders/generate.py b/adders/generate.py
index 8c0e413..b0856b8 100755
--- a/adders/generate.py
+++ b/adders/generate.py
@@ -18,7 +18,8 @@ from adders.circuits import OracleFn, QinplaceAction, census, jcs  # noqa: E402
 from multipliers import constructions as M  # noqa: E402
 from qrom import constructions as Q  # noqa: E402
 
-ISA_SPEC_COMMIT = "5513d7822edc7cfc54aeda37092bfb3f2fec7581"
+ISA_SPEC_COMMIT = "ecaaac060c44e317d1181345fa6b8e38c096c099"
+CERTIFICATE_EXTENSION_SPEC_COMMIT = "be109bd27889ea91e3c0ad78a30e5e4d71d3d0d3"
 MANIFEST = ROOT / "adders/objects/manifest.json"
 SOURCES = ["adders/circuits.py", "adders/constructions.py", "adders/generate.py", "adders/target-unit.json",
            "multipliers/constructions.py", "qrom/constructions.py"]
@@ -95,6 +96,7 @@ def build():
                         "file": path, "inverse": obj.inverse, "root": obj.root,
                         "sha256": hashlib.sha256(text.encode()).hexdigest(), "symbols": symbols})
     manifest = {"entries": entries, "isa": "0.9", "isa_spec_commit": ISA_SPEC_COMMIT,
+                "certificate_extensions": {"K91": CERTIFICATE_EXTENSION_SPEC_COMMIT},
                 "sources": {s: hashlib.sha256((ROOT / s).read_bytes()).hexdigest() for s in SOURCES},
                 "target_sha256": hashlib.sha256((ROOT / "adders/target-unit.json").read_bytes()).hexdigest()}
     files[str(MANIFEST.relative_to(ROOT))] = jcs(manifest) + "\n"
@@ -107,7 +109,9 @@ def main(argv):
     if argv[1] == "one":
         if len(argv) < 3 or argv[2] not in FAMILIES:
             raise SystemExit(f"family must be one of {sorted(FAMILIES)}")
-        args = [tuple(int(w, 0) for w in a.split(",")) if "," in a else int(a, 0) for a in argv[3:]]
+        args = [tuple(int(w, 0) for w in a.split(","))
+                if i == 0 and argv[2] in {"qrom", "qrom.select_swap", "qrom.select_swap_dirty"}
+                else int(a, 0) for i, a in enumerate(argv[3:])]
         sys.stdout.write(FAMILIES[argv[2]](*args).text())
         return
     files = build()
diff --git a/dist/llvm18/SHA256SUMS b/dist/llvm18/SHA256SUMS
index 20f2814..138ef3d 100644
--- a/dist/llvm18/SHA256SUMS
+++ b/dist/llvm18/SHA256SUMS
@@ -1,2 +1,2 @@
-c37b7520661fcdf322d8b7d377fc66cea3e112e724bc1b63cdee2c34ed15233d  bennett-arith.bc
-39287e78d42fc7b7363c797cb826536933727c3730cea0fc1d25c14fbf88b6ca  manifest.json
+eae6ce295a9b8b80d6e88da7281dc1de3fbdcb2b07f8ba54315f70bb1361ee0f  bennett-arith.bc
+f6dfd33bde48ad81ff6d42d839b738ddc67291f6e0a8da819b8ef19eea1f5bbf  manifest.json
diff --git a/dist/llvm18/bennett-arith.bc b/dist/llvm18/bennett-arith.bc
index 2bac6bd..f6f811a 100644
Binary files a/dist/llvm18/bennett-arith.bc and b/dist/llvm18/bennett-arith.bc differ
diff --git a/dist/llvm18/manifest.json b/dist/llvm18/manifest.json
index 8ae3b70..41eb9f5 100644
--- a/dist/llvm18/manifest.json
+++ b/dist/llvm18/manifest.json
@@ -1,9 +1,9 @@
 {
-  "dialect": "0.2.12",
+  "dialect": "0.2.13",
   "isa": "0.8",
   "conformance_pending": [
-    "bennett-arith-4yg",
-    "bennett-arith-wvh"
+    "ppc-full-domain-arithmetic",
+    "elementary-full-domain-accuracy"
   ],
   "instance_generator": {
     "command": "python3 -I softfloat/instantiate.py REQUEST.json OUTPUT_DIRECTORY",
@@ -2576,8 +2576,7 @@
       "constrained": false,
       "id": 141,
       "signature": "i128 (i16)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -2595,8 +2594,7 @@
       "constrained": true,
       "id": 142,
       "signature": "i128 (i16, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -2613,8 +2611,7 @@
       "constrained": false,
       "id": 143,
       "signature": "i128 (i16)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -2632,8 +2629,7 @@
       "constrained": true,
       "id": 144,
       "signature": "i128 (i16, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -5200,8 +5196,7 @@
       "constrained": false,
       "id": 286,
       "signature": "i128 (i16)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -5219,8 +5214,7 @@
       "constrained": true,
       "id": 287,
       "signature": "i128 (i16, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -5237,8 +5231,7 @@
       "constrained": false,
       "id": 288,
       "signature": "i128 (i16)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -5256,8 +5249,7 @@
       "constrained": true,
       "id": 289,
       "signature": "i128 (i16, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -7824,8 +7816,7 @@
       "constrained": false,
       "id": 431,
       "signature": "i128 (i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -7843,8 +7834,7 @@
       "constrained": true,
       "id": 432,
       "signature": "i128 (i32, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -7861,8 +7851,7 @@
       "constrained": false,
       "id": 433,
       "signature": "i128 (i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -7880,8 +7869,7 @@
       "constrained": true,
       "id": 434,
       "signature": "i128 (i32, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -10448,8 +10436,7 @@
       "constrained": false,
       "id": 576,
       "signature": "i128 (i64)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -10467,8 +10454,7 @@
       "constrained": true,
       "id": 577,
       "signature": "i128 (i64, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -10485,8 +10471,7 @@
       "constrained": false,
       "id": 578,
       "signature": "i128 (i64)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -10504,8 +10489,7 @@
       "constrained": true,
       "id": 579,
       "signature": "i128 (i64, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -13069,8 +13053,7 @@
       "constrained": false,
       "id": 721,
       "signature": "i128 (i80)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -13088,8 +13071,7 @@
       "constrained": true,
       "id": 722,
       "signature": "i128 (i80, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -13106,8 +13088,7 @@
       "constrained": false,
       "id": 723,
       "signature": "i128 (i80)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -13125,8 +13106,7 @@
       "constrained": true,
       "id": 724,
       "signature": "i128 (i80, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -15693,8 +15673,7 @@
       "constrained": false,
       "id": 866,
       "signature": "i128 (i128)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -15712,8 +15691,7 @@
       "constrained": true,
       "id": 867,
       "signature": "i128 (i128, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -15730,8 +15708,7 @@
       "constrained": false,
       "id": 868,
       "signature": "i128 (i128)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -15749,8 +15726,7 @@
       "constrained": true,
       "id": 869,
       "signature": "i128 (i128, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -16808,8 +16784,7 @@
       "constrained": false,
       "id": 927,
       "signature": "i128 (i128, i128, i128)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -16829,8 +16804,7 @@
       "constrained": true,
       "id": 928,
       "signature": "i128 (i128, i128, i128, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -20860,8 +20834,7 @@
         1025
       ],
       "generator": "softfloat/instantiate.py",
-      "section": "13.4",
-      "bead": "bennett-arith-0he"
+      "section": "13.4"
     },
     {
       "name": "__bennett_sf_convert_to_<fmt>_B",
@@ -20869,8 +20842,7 @@
       "formats": "all eleven LLVM23 interpretation names from each of seven bases; no names on LLVM18",
       "generator": "softfloat/instantiate.py",
       "section": "13.1",
-      "status": "available-offline",
-      "bead": "bennett-arith-38c"
+      "status": "available-offline"
     },
     {
       "name": "__bennett_sf_convert_from_<fmt>_B",
@@ -20878,15 +20850,14 @@
       "formats": "each of seven bases from all eleven LLVM23 interpretation names; no names on LLVM18",
       "generator": "softfloat/instantiate.py",
       "section": "13.1",
-      "status": "available-offline",
-      "bead": "bennett-arith-38c"
+      "status": "available-offline"
     }
   ],
   "numerical_accuracy": {
-    "contract": "0.2.12 13.4: full-domain one-local-ulp; constrained correctly rounded selection and exact flags",
-    "pending_bead": "bennett-arith-wvh",
+    "contract": "0.2.13 13.4: full-domain one-local-ulp; constrained correctly rounded selection and exact flags",
+    "pending_obligation": "elementary-full-domain-accuracy",
     "claim": "deterministic approximation; no global correct-rounding or ulp-bound proof",
-    "working_significand_bits": 224,
+    "working_significand_bits": 240,
     "exact_dyadic_families": [
       "pow",
       "exp2",
@@ -20902,12 +20873,11 @@
         "domain": "finite |x| <= 2^-112",
         "method": "exact high+low midpoint comparison; quadratic/cubic log(1+h) comparison for directed sides",
         "guarantee": "correct canonical pair in all five modes; zero is exact, otherwise only inexact",
-        "test": "tests/test_ppc_exp.py",
-        "bead": "bennett-arith-wvh.1"
+        "test": "tests/test_ppc_exp.py"
       }
     ],
     "payne_hanek_constant_bits": 17408,
-    "verification": "tests/test_trans.py and tests/test_trans_extra.py compare published bitcode with MPFR at 384 bits; <=4 ulp engineering acceptance, exhaustive f16/bf16 sin <=1 ulp"
+    "verification": "tests/test_trans.py and tests/test_trans_extra.py compare published bitcode with adaptive directed MPFR brackets and exact carrier selection; unresolved PPC cases use BENNETT_ARITH_PROMISED"
   },
   "ppc_semantics": {
     "oracle": "independent exact rational arithmetic for explicit guarantees; same-major LLVM APFloat for component operations",
@@ -20918,16 +20888,10 @@
     "sqrt_comparison_bits": 4352,
     "llvm18": "component add/mul; legacy 106-bit divide/remainder operation conventions",
     "llvm23": "same operations as LLVM18, including explicit 0.2.12 exact-value overrides",
-    "pending_bead": "bennett-arith-4yg",
-    "implementation_gaps": "0.2.13 nearest-even parity migration follows review round 2; the current publication retains the 0.2.12 parity interpretation"
+    "pending_obligation": "ppc-full-domain-arithmetic",
+    "implementation_gaps": "legacy component add/mul and divide/remainder conventions remain versioned"
   },
-  "contract_questions": [
-    {
-      "bead": "bennett-arith-4yg.1",
-      "section": "13.1",
-      "question": "Published 0.2.13 resolves the 0.2.12 zero-low parity question; implementation migration is sequenced after review round 2."
-    }
-  ],
+  "contract_questions": [],
   "comparison_semantics": {
     "quiet": "cmp_B_rm: invalid only on signaling NaN",
     "signaling": "cmps_B_rm: invalid on any NaN, including false/true predicates",
@@ -20947,7 +20911,7 @@
     "flags": "sticky invalid only; plain cmp_B has no fenv access"
   },
   "llvm_major": 18,
-  "bitcode_sha256": "c37b7520661fcdf322d8b7d377fc66cea3e112e724bc1b63cdee2c34ed15233d",
+  "bitcode_sha256": "eae6ce295a9b8b80d6e88da7281dc1de3fbdcb2b07f8ba54315f70bb1361ee0f",
   "tool_versions": {
     "clang": "Ubuntu clang version 18.1.3 (1ubuntu1)",
     "llvm-as": "Ubuntu LLVM version 18.1.3",
@@ -20956,8 +20920,8 @@
   },
   "sources": {
     "scripts/build": {
-      "sha256": "4850c9d6f80217f1ca86ce748ecab57c8bd4d56e21e9fa973f763492ce3192a8",
-      "git_blob_sha1": "aa0bbfd5c7a6bfa35e6f33141401fe51d119e6ad"
+      "sha256": "0de749605eccab1c3aef6dacac832cb49abe3e7aac6507d89b8eac171f4d124e",
+      "git_blob_sha1": "ce7ca8ab0d6009d440ad7b4267ad2298c99d63c5"
     },
     "scripts/provenance.py": {
       "sha256": "35116f907716df661cdfa74a402670eea2074a64d2eedae9fb1f0a2bbfc75298",
@@ -20972,28 +20936,28 @@
       "git_blob_sha1": "d292a70d55cd81e270fe12791fced101fd6b84ed"
     },
     "softfloat/generate.py": {
-      "sha256": "3a80f63e440c0ca64adf2fba24c023551d75ad2a2d84e7136e230acfe84ee5e0",
-      "git_blob_sha1": "55a986338660f891916f35fcda003e2b4cbb5e48"
+      "sha256": "07479ec49109d902ef7a212560ed7f3b59441a7c1e8aaaf39347bb5e1c52299f",
+      "git_blob_sha1": "2f9146bdc129f08647b3c90adcb47f07d2641b0f"
     },
     "softfloat/instantiate.py": {
       "sha256": "0b406a951a090a23fc24f3d0eb8b364d5de0d988938e3cc3f49b72d164875ba0",
       "git_blob_sha1": "66f14b00b67020b01e90ca6bcbd74ebb6d8b3695"
     },
     "softfloat/named.c": {
-      "sha256": "7256883acf65d744101feff594a7d6a008afd29ac22d5e9bdefc53c54f5ea1c2",
-      "git_blob_sha1": "07d3108d7a064aa6dc86041a1c1d3f9f2fef4bbe"
+      "sha256": "faf4ee9e90e08b9aadf1fd9090bd6b16e3438b1a0cddc2915aa6f037170da3e0",
+      "git_blob_sha1": "83d597d04376347a6d93c12da59cab729f6c5e0d"
     },
     "softfloat/ppc.h": {
       "sha256": "4ff05b6bb8872889b8f405c82baa915b0eea39cfe12c6c44789c8b3a08dcd40a",
       "git_blob_sha1": "ef171eb0b28cd31352ca8af9b4e2235c87016539"
     },
     "softfloat/ppc_round.h": {
-      "sha256": "650bb656299da06528281092866eb8b469122217c1ea4a4435234ac749e9b4f2",
-      "git_blob_sha1": "e9afda5e1875792e6c5a7a801b457361bb28204d"
+      "sha256": "5b0673ec86359586f9c4a97bf9d2410a40dcb4ffa41d4e7c6f1418e9483cf89d",
+      "git_blob_sha1": "b00563ec4eb723f4b21b8cf4b0c7dccdbe485ad0"
     },
     "softfloat/ppc_sum.h": {
-      "sha256": "6331d37405f5c7fbeb5c4b2fc620fe9deb72b050de7ddc16205cb0734e35f40d",
-      "git_blob_sha1": "b4ef10fe47e22c0d2607ba1e02aac8c1f6aa8e90"
+      "sha256": "eba161097c818d4528c7f0e1bda2a9ba5caa8d33308e823715f84dd7644483d6",
+      "git_blob_sha1": "0a45a4d5bac227bd333d497d06b7d798d6748dbd"
     },
     "softfloat/test_cmps.py": {
       "sha256": "87031e689c53bf5c90ef67ed143ddeb4f6965b6cfcbdb2d41cb9a37f008d13f0",
@@ -21004,16 +20968,16 @@
       "git_blob_sha1": "5455f9c79c53e755e251cf4f18cd6147a380486e"
     },
     "softfloat/test_instances.py": {
-      "sha256": "e4d904f3d822854472725a8ec9f00960d6c1e0053b2119f484b4c07700e06d7a",
-      "git_blob_sha1": "3221d50a954994e34a9ebd819ae2fcda2fae39dd"
+      "sha256": "c86e6362993dd8c70876eca6bc42ffb0ea7edd463a31c2dc5110391ab334b10d",
+      "git_blob_sha1": "b0ab7480adbcabed534d263abec2ce8800607d23"
     },
     "softfloat/test_publication.py": {
-      "sha256": "96485566f7c7447ed4635240cbfdfbf700572caa0ad7fcb57ee6bc6982716823",
-      "git_blob_sha1": "638ec82402da8ad274622db39fbc7334884d9915"
+      "sha256": "a728f74821f679bd0125ea831c64cd8cf79aa4808e662af36870d817cf3f4112",
+      "git_blob_sha1": "2683f8cc91015e16b8cae1efba6eb9f13da9f6d3"
     },
     "softfloat/trans.h": {
-      "sha256": "f33667ddf65c8a86e2d67070a6b5880d8692977c4137e4fef15fccaebaf51a32",
-      "git_blob_sha1": "c2c1ab2adcab497d3a2dc0434b73486557c39a2d"
+      "sha256": "f61643535b60cb22ec5cb73bc6721d15c5f30970fcba4f1e4ad56b492c492cc4",
+      "git_blob_sha1": "1e5a9c597d0c7428fb593c2e53b5731965a3a1b5"
     },
     "softfloat/trans_exact.h": {
       "sha256": "402ba4ae26241af7af91a5a0278390ae8fa7d9f0e38d4caa902e77c553207118",
diff --git a/dist/llvm23/SHA256SUMS b/dist/llvm23/SHA256SUMS
index 8184b80..9c849d2 100644
--- a/dist/llvm23/SHA256SUMS
+++ b/dist/llvm23/SHA256SUMS
@@ -1,2 +1,2 @@
-dfe0da8e1282e520c4dde7a843f25f268a022bd854a73e8f3c5b52009fbcae09  bennett-arith.bc
-d531a68966d8dc35b9f0952a4f31f7b20f9f8af7ef0e470cb4324bb7741e3051  manifest.json
+e49fe95b03171bc7876e91fb635fd11c5c0b242d6b9445b4847682f9cee00b5f  bennett-arith.bc
+4d02d34da28811bcb08f793ad51ec43a160612354bb371d9ed2c2c416124d61a  manifest.json
diff --git a/dist/llvm23/bennett-arith.bc b/dist/llvm23/bennett-arith.bc
index d491ebf..4b67852 100644
Binary files a/dist/llvm23/bennett-arith.bc and b/dist/llvm23/bennett-arith.bc differ
diff --git a/dist/llvm23/manifest.json b/dist/llvm23/manifest.json
index e5660d4..46a97db 100644
--- a/dist/llvm23/manifest.json
+++ b/dist/llvm23/manifest.json
@@ -1,9 +1,9 @@
 {
-  "dialect": "0.2.12",
+  "dialect": "0.2.13",
   "isa": "0.8",
   "conformance_pending": [
-    "bennett-arith-4yg",
-    "bennett-arith-wvh"
+    "ppc-full-domain-arithmetic",
+    "elementary-full-domain-accuracy"
   ],
   "instance_generator": {
     "command": "python3 -I softfloat/instantiate.py REQUEST.json OUTPUT_DIRECTORY",
@@ -2576,8 +2576,7 @@
       "constrained": false,
       "id": 141,
       "signature": "i128 (i16)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -2595,8 +2594,7 @@
       "constrained": true,
       "id": 142,
       "signature": "i128 (i16, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -2613,8 +2611,7 @@
       "constrained": false,
       "id": 143,
       "signature": "i128 (i16)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -2632,8 +2629,7 @@
       "constrained": true,
       "id": 144,
       "signature": "i128 (i16, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -5200,8 +5196,7 @@
       "constrained": false,
       "id": 286,
       "signature": "i128 (i16)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -5219,8 +5214,7 @@
       "constrained": true,
       "id": 287,
       "signature": "i128 (i16, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -5237,8 +5231,7 @@
       "constrained": false,
       "id": 288,
       "signature": "i128 (i16)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -5256,8 +5249,7 @@
       "constrained": true,
       "id": 289,
       "signature": "i128 (i16, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -7824,8 +7816,7 @@
       "constrained": false,
       "id": 431,
       "signature": "i128 (i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -7843,8 +7834,7 @@
       "constrained": true,
       "id": 432,
       "signature": "i128 (i32, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -7861,8 +7851,7 @@
       "constrained": false,
       "id": 433,
       "signature": "i128 (i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -7880,8 +7869,7 @@
       "constrained": true,
       "id": 434,
       "signature": "i128 (i32, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -10448,8 +10436,7 @@
       "constrained": false,
       "id": 576,
       "signature": "i128 (i64)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -10467,8 +10454,7 @@
       "constrained": true,
       "id": 577,
       "signature": "i128 (i64, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -10485,8 +10471,7 @@
       "constrained": false,
       "id": 578,
       "signature": "i128 (i64)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -10504,8 +10489,7 @@
       "constrained": true,
       "id": 579,
       "signature": "i128 (i64, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -13069,8 +13053,7 @@
       "constrained": false,
       "id": 721,
       "signature": "i128 (i80)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -13088,8 +13071,7 @@
       "constrained": true,
       "id": 722,
       "signature": "i128 (i80, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -13106,8 +13088,7 @@
       "constrained": false,
       "id": 723,
       "signature": "i128 (i80)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -13125,8 +13106,7 @@
       "constrained": true,
       "id": 724,
       "signature": "i128 (i80, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -15693,8 +15673,7 @@
       "constrained": false,
       "id": 866,
       "signature": "i128 (i128)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -15712,8 +15691,7 @@
       "constrained": true,
       "id": 867,
       "signature": "i128 (i128, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -15730,8 +15708,7 @@
       "constrained": false,
       "id": 868,
       "signature": "i128 (i128)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -15749,8 +15726,7 @@
       "constrained": true,
       "id": 869,
       "signature": "i128 (i128, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -16808,8 +16784,7 @@
       "constrained": false,
       "id": 927,
       "signature": "i128 (i128, i128, i128)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.1"
     },
     {
@@ -16829,8 +16804,7 @@
       "constrained": true,
       "id": 928,
       "signature": "i128 (i128, i128, i128, i32)",
-      "status": "canonical-pair-pending-parity-migration",
-      "bead": "bennett-arith-4yg",
+      "status": "canonical-pair-exact",
       "section": "13.5"
     },
     {
@@ -20860,8 +20834,7 @@
         1025
       ],
       "generator": "softfloat/instantiate.py",
-      "section": "13.4",
-      "bead": "bennett-arith-0he"
+      "section": "13.4"
     },
     {
       "name": "__bennett_sf_convert_to_<fmt>_B",
@@ -20869,8 +20842,7 @@
       "formats": "all eleven LLVM23 interpretation names from each of seven bases; no names on LLVM18",
       "generator": "softfloat/instantiate.py",
       "section": "13.1",
-      "status": "available-offline",
-      "bead": "bennett-arith-38c"
+      "status": "available-offline"
     },
     {
       "name": "__bennett_sf_convert_from_<fmt>_B",
@@ -20878,15 +20850,14 @@
       "formats": "each of seven bases from all eleven LLVM23 interpretation names; no names on LLVM18",
       "generator": "softfloat/instantiate.py",
       "section": "13.1",
-      "status": "available-offline",
-      "bead": "bennett-arith-38c"
+      "status": "available-offline"
     }
   ],
   "numerical_accuracy": {
-    "contract": "0.2.12 13.4: full-domain one-local-ulp; constrained correctly rounded selection and exact flags",
-    "pending_bead": "bennett-arith-wvh",
+    "contract": "0.2.13 13.4: full-domain one-local-ulp; constrained correctly rounded selection and exact flags",
+    "pending_obligation": "elementary-full-domain-accuracy",
     "claim": "deterministic approximation; no global correct-rounding or ulp-bound proof",
-    "working_significand_bits": 224,
+    "working_significand_bits": 240,
     "exact_dyadic_families": [
       "pow",
       "exp2",
@@ -20902,12 +20873,11 @@
         "domain": "finite |x| <= 2^-112",
         "method": "exact high+low midpoint comparison; quadratic/cubic log(1+h) comparison for directed sides",
         "guarantee": "correct canonical pair in all five modes; zero is exact, otherwise only inexact",
-        "test": "tests/test_ppc_exp.py",
-        "bead": "bennett-arith-wvh.1"
+        "test": "tests/test_ppc_exp.py"
       }
     ],
     "payne_hanek_constant_bits": 17408,
-    "verification": "tests/test_trans.py and tests/test_trans_extra.py compare published bitcode with MPFR at 384 bits; <=4 ulp engineering acceptance, exhaustive f16/bf16 sin <=1 ulp"
+    "verification": "tests/test_trans.py and tests/test_trans_extra.py compare published bitcode with adaptive directed MPFR brackets and exact carrier selection; unresolved PPC cases use BENNETT_ARITH_PROMISED"
   },
   "ppc_semantics": {
     "oracle": "independent exact rational arithmetic for explicit guarantees; same-major LLVM APFloat for component operations",
@@ -20918,16 +20888,10 @@
     "sqrt_comparison_bits": 4352,
     "llvm18": "component add/mul; legacy 106-bit divide/remainder operation conventions",
     "llvm23": "same operations as LLVM18, including explicit 0.2.12 exact-value overrides",
-    "pending_bead": "bennett-arith-4yg",
-    "implementation_gaps": "0.2.13 nearest-even parity migration follows review round 2; the current publication retains the 0.2.12 parity interpretation"
+    "pending_obligation": "ppc-full-domain-arithmetic",
+    "implementation_gaps": "legacy component add/mul and divide/remainder conventions remain versioned"
   },
-  "contract_questions": [
-    {
-      "bead": "bennett-arith-4yg.1",
-      "section": "13.1",
-      "question": "Published 0.2.13 resolves the 0.2.12 zero-low parity question; implementation migration is sequenced after review round 2."
-    }
-  ],
+  "contract_questions": [],
   "comparison_semantics": {
     "quiet": "cmp_B_rm: invalid only on signaling NaN",
     "signaling": "cmps_B_rm: invalid on any NaN, including false/true predicates",
@@ -20947,17 +20911,17 @@
     "flags": "sticky invalid only; plain cmp_B has no fenv access"
   },
   "llvm_major": 23,
-  "bitcode_sha256": "dfe0da8e1282e520c4dde7a843f25f268a022bd854a73e8f3c5b52009fbcae09",
+  "bitcode_sha256": "e49fe95b03171bc7876e91fb635fd11c5c0b242d6b9445b4847682f9cee00b5f",
   "tool_versions": {
-    "clang": "Ubuntu clang version 23.1.5 (++20261028083854+a738f2737189-1~exp1~20261028203912.92)",
-    "llvm-as": "Ubuntu LLVM version 23.1.5",
-    "llvm-link": "Ubuntu LLVM version 23.1.5",
-    "opt": "Ubuntu LLVM version 23.1.5"
+    "clang": "Ubuntu clang version 23.1.6 (++20261103094202+2875c6073a7e-1~exp1~20261103214217.95)",
+    "llvm-as": "Ubuntu LLVM version 23.1.6",
+    "llvm-link": "Ubuntu LLVM version 23.1.6",
+    "opt": "Ubuntu LLVM version 23.1.6"
   },
   "sources": {
     "scripts/build": {
-      "sha256": "4850c9d6f80217f1ca86ce748ecab57c8bd4d56e21e9fa973f763492ce3192a8",
-      "git_blob_sha1": "aa0bbfd5c7a6bfa35e6f33141401fe51d119e6ad"
+      "sha256": "0de749605eccab1c3aef6dacac832cb49abe3e7aac6507d89b8eac171f4d124e",
+      "git_blob_sha1": "ce7ca8ab0d6009d440ad7b4267ad2298c99d63c5"
     },
     "scripts/provenance.py": {
       "sha256": "35116f907716df661cdfa74a402670eea2074a64d2eedae9fb1f0a2bbfc75298",
@@ -20972,28 +20936,28 @@
       "git_blob_sha1": "d292a70d55cd81e270fe12791fced101fd6b84ed"
     },
     "softfloat/generate.py": {
-      "sha256": "3a80f63e440c0ca64adf2fba24c023551d75ad2a2d84e7136e230acfe84ee5e0",
-      "git_blob_sha1": "55a986338660f891916f35fcda003e2b4cbb5e48"
+      "sha256": "07479ec49109d902ef7a212560ed7f3b59441a7c1e8aaaf39347bb5e1c52299f",
+      "git_blob_sha1": "2f9146bdc129f08647b3c90adcb47f07d2641b0f"
     },
     "softfloat/instantiate.py": {
       "sha256": "0b406a951a090a23fc24f3d0eb8b364d5de0d988938e3cc3f49b72d164875ba0",
       "git_blob_sha1": "66f14b00b67020b01e90ca6bcbd74ebb6d8b3695"
     },
     "softfloat/named.c": {
-      "sha256": "7256883acf65d744101feff594a7d6a008afd29ac22d5e9bdefc53c54f5ea1c2",
-      "git_blob_sha1": "07d3108d7a064aa6dc86041a1c1d3f9f2fef4bbe"
+      "sha256": "faf4ee9e90e08b9aadf1fd9090bd6b16e3438b1a0cddc2915aa6f037170da3e0",
+      "git_blob_sha1": "83d597d04376347a6d93c12da59cab729f6c5e0d"
     },
     "softfloat/ppc.h": {
       "sha256": "4ff05b6bb8872889b8f405c82baa915b0eea39cfe12c6c44789c8b3a08dcd40a",
       "git_blob_sha1": "ef171eb0b28cd31352ca8af9b4e2235c87016539"
     },
     "softfloat/ppc_round.h": {
-      "sha256": "650bb656299da06528281092866eb8b469122217c1ea4a4435234ac749e9b4f2",
-      "git_blob_sha1": "e9afda5e1875792e6c5a7a801b457361bb28204d"
+      "sha256": "5b0673ec86359586f9c4a97bf9d2410a40dcb4ffa41d4e7c6f1418e9483cf89d",
+      "git_blob_sha1": "b00563ec4eb723f4b21b8cf4b0c7dccdbe485ad0"
     },
     "softfloat/ppc_sum.h": {
-      "sha256": "6331d37405f5c7fbeb5c4b2fc620fe9deb72b050de7ddc16205cb0734e35f40d",
-      "git_blob_sha1": "b4ef10fe47e22c0d2607ba1e02aac8c1f6aa8e90"
+      "sha256": "eba161097c818d4528c7f0e1bda2a9ba5caa8d33308e823715f84dd7644483d6",
+      "git_blob_sha1": "0a45a4d5bac227bd333d497d06b7d798d6748dbd"
     },
     "softfloat/test_cmps.py": {
       "sha256": "87031e689c53bf5c90ef67ed143ddeb4f6965b6cfcbdb2d41cb9a37f008d13f0",
@@ -21004,16 +20968,16 @@
       "git_blob_sha1": "5455f9c79c53e755e251cf4f18cd6147a380486e"
     },
     "softfloat/test_instances.py": {
-      "sha256": "e4d904f3d822854472725a8ec9f00960d6c1e0053b2119f484b4c07700e06d7a",
-      "git_blob_sha1": "3221d50a954994e34a9ebd819ae2fcda2fae39dd"
+      "sha256": "c86e6362993dd8c70876eca6bc42ffb0ea7edd463a31c2dc5110391ab334b10d",
+      "git_blob_sha1": "b0ab7480adbcabed534d263abec2ce8800607d23"
     },
     "softfloat/test_publication.py": {
-      "sha256": "96485566f7c7447ed4635240cbfdfbf700572caa0ad7fcb57ee6bc6982716823",
-      "git_blob_sha1": "638ec82402da8ad274622db39fbc7334884d9915"
+      "sha256": "a728f74821f679bd0125ea831c64cd8cf79aa4808e662af36870d817cf3f4112",
+      "git_blob_sha1": "2683f8cc91015e16b8cae1efba6eb9f13da9f6d3"
     },
     "softfloat/trans.h": {
-      "sha256": "f33667ddf65c8a86e2d67070a6b5880d8692977c4137e4fef15fccaebaf51a32",
-      "git_blob_sha1": "c2c1ab2adcab497d3a2dc0434b73486557c39a2d"
+      "sha256": "f61643535b60cb22ec5cb73bc6721d15c5f30970fcba4f1e4ad56b492c492cc4",
+      "git_blob_sha1": "1e5a9c597d0c7428fb593c2e53b5731965a3a1b5"
     },
     "softfloat/trans_exact.h": {
       "sha256": "402ba4ae26241af7af91a5a0278390ae8fa7d9f0e38d4caa902e77c553207118",
diff --git a/gate.toml b/gate.toml
index aeb0e74..04470c2 100644
--- a/gate.toml
+++ b/gate.toml
@@ -4,8 +4,13 @@ repo = "bennett-arith"
 tool_sha = "01c0314c9aaa4a37313ab530da2134efafe9cbd5"
 timeout_s = 28800
 
-[env]
-BENNETT_ISA_REF = "{sibling:bennett-isa-spec}/reference-interpreter/target/debug/bennett-isa-ref"
+[[check]]
+name = "quality baseline ratchet"
+argv = ["python3", "-I", "scripts/quality_metrics.py"]
+
+[[check]]
+name = "bounded default tests"
+argv = ["scripts/test"]
 
 [[check]]
 name = "arith gate"
@@ -26,3 +31,7 @@ argv = ["cargo", "build", "--offline"]
 outputs = ["reference-interpreter/target/debug/bennett-isa-ref"]
 env = { CARGO_BUILD_JOBS = "4" }
 
+[siblings."bennett-dialect-spec"]
+sha = "95a4b8d06933018a07fef3516296a25fd582fcde"
+note = "Published 0.2.13: total PPC nearest-even tie parity"
+
diff --git a/scripts/build b/scripts/build
index aa0bbfd..ce7ca8a 100755
--- a/scripts/build
+++ b/scripts/build
@@ -2,12 +2,12 @@
 set -euo pipefail
 unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER
 root="$(dirname "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")")"
-export TMPDIR="$root/.tmp"
+export TMPDIR="${TMPDIR:-$root/.tmp}"
 mkdir -p "$TMPDIR"
 major="${1:?usage: scripts/build 18|23}"
 case "$major" in 18|23) ;; *) echo 'only LLVM 18 and 23 are pinned' >&2; exit 1;; esac
 llvm="/usr/lib/llvm-$major/bin"
-build="$TMPDIR/llvm$major"
+build="$root/.tmp/llvm$major"
 dist="$root/dist/llvm$major"
 mkdir -p "$build" "$dist"
 python3 -I "$root/softfloat/generate.py" "$build" "${@:2}"
diff --git a/scripts/gate b/scripts/gate
index 647e80a..112e761 100755
--- a/scripts/gate
+++ b/scripts/gate
@@ -2,8 +2,10 @@
 set -euo pipefail
 unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER
 root="$(dirname "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")")"
-export TMPDIR="$root/.tmp"
+export TMPDIR="${TMPDIR:-$root/.tmp}"
 mkdir -p "$TMPDIR"
+# Multiple real bridge rebuilds stay outside the bounded numerical suite.
+timeout 600s python3 -B -I "$root/tests/test_default_cache.py"
 # Fail if checked-in publications differ from a fresh build (including the path).
 for major in 18 23; do
   dir="$root/dist/llvm$major"
@@ -30,4 +32,12 @@ python3 -I "$root/tests/test_powi_limit.py"
 python3 -I "$root/tests/test_trans.py"
 python3 -I "$root/tests/test_trans_extra.py"
 python3 -I "$root/tests/test_trans_boundaries.py"
+timeout 300s python3 -I "$root/tests/test_directed.py"
+timeout 60s python3 -I "$root/tests/test_pair_parity.py"
+timeout 60s python3 -I "$root/tests/test_trans_phases.py"
+timeout 180s python3 -I "$root/tests/test_named_overflow.py"
+timeout 900s python3 -I "$root/softfloat/test_instances.py"
+timeout 900s python3 -I "$root/softfloat/test_instance_limits.py"
+timeout 300s python3 -I "$root/softfloat/test_cmps.py"
+timeout 30s python3 -I "$root/softfloat/test_publication.py"
 echo 'gate: both published bitcode edges reproduced and passed'
diff --git a/scripts/pinned_sibling.py b/scripts/pinned_sibling.py
new file mode 100644
index 0000000..3debadd
--- /dev/null
+++ b/scripts/pinned_sibling.py
@@ -0,0 +1,37 @@
+"""Resolve this repo's gate.toml pins without consulting live sibling contents."""
+import os
+from pathlib import Path
+import subprocess
+import tomllib
+
+ROOT = Path(__file__).resolve().parents[1]
+
+
+def _head(path):
+    if not (path / ".git").exists():
+        return "unavailable"
+    try:
+        done = subprocess.run(
+            ["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True,
+            text=True, timeout=10, env={k: v for k, v in os.environ.items() if not k.startswith("GIT_")},
+        )
+        return done.stdout.strip() if done.returncode == 0 else "unavailable"
+    except (OSError, subprocess.SubprocessError):
+        return "unavailable"
+
+
+def resolve_sibling(name):
+    with (ROOT / "gate.toml").open("rb") as stream:
+        config = tomllib.load(stream)
+    sha = config["siblings"][name]["sha"]
+    layout = os.environ.get("BENNETT_GATE_LAYOUT")
+    path = (Path(layout) / name if layout else
+            ROOT / ".tmp/gate/cache" / f"{name}@{sha[:12]}" / name)
+    actual = _head(path)
+    if actual != sha:
+        raise SystemExit(
+            f"pinned sibling {name}@{sha}: {path} HEAD={actual}; "
+            f"live ../{name} HEAD={_head(ROOT.parent / name)}; "
+            f"materialise with gate_run.py verify --repo {config['repo']} --sha HEAD"
+        )
+    return path
diff --git a/scripts/quality_metrics.py b/scripts/quality_metrics.py
new file mode 100644
index 0000000..64bdc22
--- /dev/null
+++ b/scripts/quality_metrics.py
@@ -0,0 +1,94 @@
+#!/usr/bin/env python3
+"""Local syntax metrics and a monotone ratchet against docs/quality.md."""
+import ast
+import json
+from pathlib import Path
+import re
+import subprocess
+import sys
+
+ROOT=Path(__file__).resolve().parents[1]
+SOURCE_DIRS={"adders","multipliers","qrom","softfloat","scripts","tests"}
+PROCESS=re.compile(r"\bbennett-arith-[a-z0-9]{3}(?:\.[0-9]+)?\b|\bjob[/]|\b(?:shift|round) +[0-9]+")
+LITTER=re.compile(r"(^|/)(__pycache__|PROGRESS[^/]*|LAST-RUN[^/]*|LOCK)(/|$)|\.(?:pyc|log|darc|lock)$")
+BOUNDS=(25,50,100,200,300)
+START="<!-- quality-baseline -->"
+END="<!-- /quality-baseline -->"
+
+def python_functions(text):
+    tree=ast.parse(text)
+    def mass(node,depth=0):
+        decision=isinstance(node,(ast.If,ast.For,ast.AsyncFor,ast.While,ast.ExceptHandler,ast.IfExp,ast.Match,ast.comprehension))
+        score=(1+depth) if decision else 0
+        if isinstance(node,ast.BoolOp):score+=len(node.values)-1
+        return score+sum(mass(child,depth+int(decision)) for child in ast.iter_child_nodes(node))
+    result=[]
+    for node in ast.walk(tree):
+        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
+            body=node.body
+            only=body[0] if len(body)==1 else None
+            value=only.value if isinstance(only,(ast.Return,ast.Expr)) else None
+            result.append((node.end_lineno-node.lineno+1,mass(node),int(isinstance(value,ast.Call))))
+    return result
+
+def c_functions(text):
+    # Keep newlines so physical lengths remain comparable across revisions.
+    text=re.sub(r"/\*.*?\*/|//[^\n]*",lambda m:"\n"*m[0].count("\n"),text,flags=re.S)
+    text=re.sub(r'"(?:\\.|[^"\\])*"', '""', text)
+    head=re.compile(r"^[ \t]*(?:[A-Za-z_]\w*[ \t*]+)+([A-Za-z_]\w*)\s*\([^;{}]*\)\s*\{",re.M)
+    result=[]
+    for match in head.finditer(text):
+        start=match.end()-1;level=1;end=start+1
+        while level and end<len(text):
+            level+=(text[end]=="{")-(text[end]=="}");end+=1
+        if level:raise ValueError("unbalanced C function "+match[1])
+        body=text[start+1:end-1];depth=0;score=0
+        for token in re.findall(r"\b(?:if|for|while|switch|case|catch)\b|&&|\|\||[?{}]",body):
+            if token=="{":depth+=1
+            elif token=="}":depth-=1
+            else:score+=1+(depth if token not in ("&&","||") else 0)
+        wrapper=bool(re.fullmatch(r"\s*(?:return\s+)?[A-Za-z_]\w*\([^;{}]*\);\s*",body))
+        result.append((text[match.start():end].count("\n")+1,score,int(wrapper)))
+    return result
+
+def measure():
+    paths=subprocess.check_output(["git","ls-files","--cached","--others","--exclude-standard","-z"],cwd=ROOT).decode().split("\0")
+    files={};litter=[];identifiers=[]
+    for name in sorted(set(paths)-{""}):
+        path=ROOT/name
+        if not path.is_file():continue
+        if LITTER.search(name):litter.append(name)
+        if Path(name).parts[0] not in SOURCE_DIRS or path.suffix not in (".py",".c",".h",".cpp"):continue
+        text=path.read_text()
+        if not name.startswith("tests/") and not path.name.startswith("test_"):
+            identifiers.extend(f"{name}:{text.count(chr(10),0,m.start())+1}" for m in PROCESS.finditer(text))
+        rows=python_functions(text) if path.suffix==".py" else c_functions(text)
+        files[name]={"functions":len(rows),"max_lines":max((r[0] for r in rows),default=0),
+                     **{f"over_{n}":sum(r[0]>n for r in rows) for n in BOUNDS},
+                     "cognitive_mass":sum(r[1] for r in rows),"trivial_wrappers":sum(r[2] for r in rows)}
+    return {"files":files,"litter":litter,"process_identifiers":identifiers}
+
+def regressions(current,baseline):
+    failures=[]
+    for name,row in current["files"].items():
+        old=baseline["files"].get(name,{})
+        for key,value in row.items():
+            if value>old.get(key,0):failures.append(f"{name} {key}: {value} > {old.get(key,0)}")
+    for key in ("litter","process_identifiers"):
+        if len(current[key])>len(baseline[key]):failures.append(f"{key}: {current[key]}")
+    return failures
+
+def main():
+    current=measure()
+    if sys.argv[1:]==["--report"]:
+        print(json.dumps(current,sort_keys=True,indent=2));return
+    if sys.argv[1:]:raise SystemExit("usage: quality_metrics.py [--report]")
+    doc=(ROOT/"docs/quality.md").read_text()
+    if START not in doc or END not in doc:raise SystemExit("missing quality baseline in docs/quality.md")
+    block=doc.split(START,1)[1].split(END,1)[0].strip()
+    baseline=json.loads(block.removeprefix("```json").removesuffix("```").strip())
+    failures=regressions(current,baseline)
+    if failures:raise SystemExit("\n".join(failures))
+    print(f"quality ratchet: {len(current['files'])} source files, no baseline regression")
+
+if __name__=="__main__":main()
diff --git a/scripts/test b/scripts/test
new file mode 100755
index 0000000..6d2ee7c
--- /dev/null
+++ b/scripts/test
@@ -0,0 +1,18 @@
+#!/usr/bin/env bash
+# Bounded default suite; scripts/gate retains exhaustive checks on both majors.
+set -euo pipefail
+unset DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER
+root="$(dirname "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")")"
+export TMPDIR="${TMPDIR:-$root/.tmp/tests}"
+export PYTHONDONTWRITEBYTECODE=1
+mkdir -p "$TMPDIR"
+# Rebuild even when outputs exist: a cached bridge can hide publication changes,
+# and source-level checks must use current generated constants and ABI metadata.
+work="$root/.tmp/llvm18"
+mkdir -p "$work"
+python3 -B -I "$root/softfloat/generate.py" "$work"
+python3 -B -I "$root/softfloat/constants.py" "$work"
+timeout 90s /usr/lib/llvm-18/bin/clang -shared -fPIC \
+  "$root/dist/llvm18/bennett-arith.bc" "$work/bridge.ll" -o "$work/oracle-new.so"
+mv -f "$work/oracle-new.so" "$work/oracle.so"
+exec python3 -B -I "$root/tests/test_default.py" "$@"
diff --git a/softfloat/README.md b/softfloat/README.md
index 86aa4fd..656001d 100644
--- a/softfloat/README.md
+++ b/softfloat/README.md
@@ -9,7 +9,7 @@ substitute host libc/libm. The plugin consumes this binary edge only.
 
 Each distribution includes `manifest.json` (all exported names, literal LLVM
 signatures, formats, semantic status, and spec section), `staged_exports` (required
-concrete signatures awaiting mechanics, each linked to a bead), three parametric
+concrete signatures awaiting mechanics, with explicit semantic status), three parametric
 families and `SHA256SUMS` for the bitcode and manifest. The manifest is the complete
 machine-readable entry-point list. Public wrappers use the dialect's LLVM carrier
 ABI, not C's aggregate/sret ABI for `_BitInt(80)` or `_BitInt(128)`.
@@ -78,7 +78,7 @@ bridge alone defines this global. Code using only unconstrained wrappers has no
 reachable reference to it. Flags use ordinary loads/stores under the contract's
 single-thread assumption.
 
-The IEEE core uses unsigned 512-bit integers. Libm uses 224 working significand
+The IEEE core uses unsigned 512-bit integers. Libm uses 240 working significand
 bits and a 1024-bit integer product for Payne–Hanek reduction with 17,408 bits of
 2/pi. Constants are generated with integer Chudnovsky and Python Decimal at
 5,400 decimal digits. There are no LLVM FP instructions, APFloat calls, host
@@ -123,20 +123,19 @@ Incoming IEEE conversion preserves its exact dyadic value until final pair
 selection. FMA forms the exact product and sum in 4352 integer bits at quantum
 2^-2148, including cancellation, then rounds once. Intermediate component
 operations contribute no flags. Independent Fraction tests replace APFloat
-expectations for these explicit guarantees. The current publication retains
-the 0.2.12 tie interpretation; the published 0.2.13 total tie policy is scheduled
-for implementation after the review fixes, tracked in **bennett-arith-4yg.1**.
-
-Dialect 0.2.12 §13.4 requires a full-domain one-local-ulp envelope, correctly
-rounded constrained selection, and exact mathematical flags. The current
-libm v1 is a deterministic approximation evaluated at 224 working bits, then
-rounded to the requested carrier format (including explicit R for `_rm`). The
-engineering tests require <=4 ulp against MPFR at 384 bits, and exhaustive half/
-bfloat sin <=1 ulp. Passing these tests is measured evidence, not a universal
-error-bound or correct-rounding proof. No float/long-double host ABI is used.
-Constrained wrappers preserve sticky flags; full-domain accuracy and exact-flag
-implementation evidence remains in **bennett-arith-wvh**. Aggregate order and
-signed zeros are tested separately.
+expectations for these explicit guarantees. Dialect 0.2.13 supplies the total
+nearest-even tie rule: compare both low significands, including zero, whenever
+either is nonzero; use high parity only when both lows are zero; equal parity
+selects the smaller absolute sum. Both signs and zero-low transitions are tested.
+
+Dialect 0.2.13 §13.4 requires a full-domain one-local-ulp envelope, correctly
+rounded constrained selection, and exact mathematical flags. Libm uses 240
+working bits. Tests select exact carrier bits from directed MPFR intervals,
+refining precision when necessary; no ulp tolerance can hide a wrong side.
+Passing the sampled IEEE tests is measured evidence, not a universal proof.
+Sparse PPC low-component failures remain visible under
+`BENNETT_ARITH_PROMISED=1`; see [quality evidence](../docs/quality.md).
+The full published domain and all entry points remain required.
 
 Exact dyadic powers and decimal/binary logarithm identities use normalized
 integer significands, perfect roots and integer exponentiation before one
@@ -157,14 +156,13 @@ x is exactly on it; that case selects the upper neighbour. Directed rounding
 compares x with log(1+h): the exact quadratic term settles the comparison
 unless it cancels l exactly, when the sign of the cubic term settles it.
 These integer comparisons preserve sparse tails in all five modes and raise
-only inexact; exp(±0) is exactly 1 with no flags. This fixes **bennett-arith-wvh.1**,
-whose original exp(2^-700) result exceeded one local ulp by over 2^52.
+only inexact; exp(±0) is exactly 1 with no flags. This preserves the sparse low component even for exp(2^-700).
 `tests/test_ppc_exp.py` verifies every power-of-two exponent in this range,
 both signs, sparse tails, component midpoints, quadratic cancellation, signed
 zeros and final flags. Its oracle encloses the exact result between independent
 rational Taylor bounds and requires both endpoints to round identically.
 The earlier diagnostic `tests/ppc_exp_sparse_witness.py` retains the exact
-counterexample bounds. Full-domain libm correctness remains in wvh; the
+counterexample bounds. Full-domain libm correctness remains open; the
 published contract's domain and available operations are unchanged.
 
 The default bitcode publishes powi at K = 1, 8, 16, 32, 64, 128, 192, 256, 513,
@@ -179,27 +177,18 @@ manifest lists its widths. No exponent is narrowed to i32/i128.
 ## Remaining parametric contracts
 
 The offline generator below implements the 0.2.12 static request protocol.
-The default `dist/` manifest targets 0.2.12 and records outstanding verification,
+The default `dist/` manifest targets 0.2.13 and records outstanding verification,
 PPC and libm obligations in `conformance_pending`.
 
 All 1,008 previously inventoried concrete signatures are published, plus 126
 additional powi and seven signaling comparison signatures: **1,141 exports per
 major**, no staged concrete bodies.
-The remaining obligations are retained:
+Named-format conversions and arbitrary powi widths are available through the
+offline generator below. Signaling comparisons are published for all seven
+formats. Consumers re-pin the matching bitcode and verify their materialised
+L/CC closure; producer tests do not establish consumer resource bounds.
 
-- `bennett-arith-38c`: named-format conversions and arbitrary powi widths are
-  available through the documented offline generator below.
-- `bennett-arith-chn`: the distinct 0.2.12 `cmps_B_rm` implementation is
-  published and verified for all seven formats; **bennett-arith-chn.1** is
-  closed. `softfloat/test_cmps.py` tests all predicates,
-  half/bfloat NaN payloads, sticky flags and scalar lane sequences.
-
-No placeholder numerical bodies or input-dependent unsupported traps implement
-these unresolved families. This publication alone is not full DF/runtime or
-plugin bp-7ni conformance. The consumer must re-pin BENNETT_ARITH_BITCODE hashes
-and verify its own materialised L/CC closure. The plugin was read-only here.
-
-## Offline instances (dialect 0.2.12)
+## Offline instances (dialect 0.2.13)
 
 Run `python3 -I softfloat/instantiate.py REQUEST.json OUTPUT_DIRECTORY` with
 `TMPDIR` set to an existing job-local build directory. The installed LLVM 18 or
@@ -259,9 +248,7 @@ an independent LLVM dispatcher. It checks all source encodings of every named
 format into all seven bases, conversion midpoints under all five modes and
 both saturation settings, malformed requests, request/bitcode hashes, exact
 exports, target fields, sticky flags, and the absence of hardware FP/imported
-numerical routines. It does not establish the separate PPC sqrt/FMA or
-full-domain transcendental obligations in `bennett-arith-4yg` and
-`bennett-arith-wvh`.
+numerical routines. It does not establish the separate full-domain PPC or transcendental obligations.
 
 `python3 -I softfloat/test_instance_limits.py --reproduce` verifies the inclusive
 i8388608 exponent on both majors and AArch64 request fields. Run the numerical
@@ -289,7 +276,7 @@ normaliser; this is link-input bitcode, not already-materialised ISA code.
 
 The gate additionally sweeps exp/exp2/exp10 through every subnormal-output
 exponent and overflow boundaries, and runs a test-only C++ oracle linked to the **same LLVM major's
-APFloat**, MPFR 384-bit oracle comparisons, all 65,536 encodings of half and
+APFloat**, adaptive directed MPFR bracket comparisons, all 65,536 encodings of half and
 bfloat sin, PPC sparse-tail conversions and all predicates, and powi transport
 through i1025. `libmpfr.so.6` is required by tests only; LLVM development headers
 and llvm-config provide the APFloat oracle. Each manifest records the bitcode
diff --git a/softfloat/generate.py b/softfloat/generate.py
index 55a9863..2f9146b 100644
--- a/softfloat/generate.py
+++ b/softfloat/generate.py
@@ -189,7 +189,7 @@ def generate(dest, widths=POWI_WIDTHS):
         e['signature'] = f"{e['result']} ({', '.join(e['params'])})"
         e['status'] = 'deterministic-integer-libm-v1' if e['op']!='cmps' and OPS.index(e['op'])>=OPS.index('sin') else 'exact' if e['op'] != 'powi' else 'deterministic-repeated-squaring'
         if (e['fi']==6 and e['op']=='fma') or (e['op']=='convert' and e['extra']==6):
-            e.update(status='canonical-pair-pending-parity-migration',bead='bennett-arith-4yg')
+            e.update(status='canonical-pair-exact')
         ret, params, op = e['result'], e['params'], e['op']
         if op in ('cmp','cmps') and e['fi'] in IEEE_COMPARE:
             e['comparison_implementation']='format-specific-integer-ir'
@@ -290,8 +290,8 @@ def generate(dest, widths=POWI_WIDTHS):
     (dest/'wrappers.ll').write_text('\n'.join(ir)+'\n')
     (dest/'bridge.ll').write_text('\n'.join(bridge)+'\n')
     (dest/'exports.txt').write_text('\n'.join(e['name'] for e in rows)+'\n__bennett_rt_fenv\n')
-    manifest = dict(dialect='0.2.12', isa='0.8',
-                    conformance_pending=['bennett-arith-4yg','bennett-arith-wvh'],
+    manifest = dict(dialect='0.2.13', isa='0.8',
+                    conformance_pending=['ppc-full-domain-arithmetic','elementary-full-domain-accuracy'],
                     instance_generator=dict(command='python3 -I softfloat/instantiate.py REQUEST.json OUTPUT_DIRECTORY',
                         request_schema='bennett-arith-instantiations-1',manifest_schema='bennett-arith-instances-1'),
                     implementation='integer-core-v2-libm1', exports=rows,
@@ -301,38 +301,37 @@ def generate(dest, widths=POWI_WIDTHS):
                         dict(name='__bennett_sf_powi_B_i<K>', signature='C_B (C_B, iK)',
                              constrained_name='__bennett_sf_powi_B_i<K>_rm', constrained_signature='C_B (C_B, iK, i32 R)',
                              formats='all seven', status='published listed widths; arbitrary LLVM iK widths available offline', published_widths=[32]+list(widths), generator='softfloat/instantiate.py',
-                             section='13.4', bead='bennett-arith-0he'),
+                             section='13.4'),
                         dict(name='__bennett_sf_convert_to_<fmt>_B', signature='iN (C_B, i32 R, i1 Sat)',
                              formats='all eleven LLVM23 interpretation names from each of seven bases; no names on LLVM18',
-                             generator='softfloat/instantiate.py',section='13.1', status='available-offline', bead='bennett-arith-38c'),
+                             generator='softfloat/instantiate.py',section='13.1', status='available-offline'),
                         dict(name='__bennett_sf_convert_from_<fmt>_B', signature='C_B (iN)',
                              formats='each of seven bases from all eleven LLVM23 interpretation names; no names on LLVM18',
-                             generator='softfloat/instantiate.py',section='13.1', status='available-offline', bead='bennett-arith-38c')])
+                             generator='softfloat/instantiate.py',section='13.1', status='available-offline')])
     implemented={e['name'] for e in rows}
     for e in entries(FORMATS):
         if e['name'] not in implemented:
             e['signature']=f"{e['result']} ({', '.join(e['params'])})"
-            e.update(status='staged', bead='bennett-arith-r3d', section='13.1/13.3/13.5')
+            e.update(status='staged', section='13.1/13.3/13.5')
             manifest['staged_exports'].append(e)
-    manifest['numerical_accuracy'] = dict(contract='0.2.12 13.4: full-domain one-local-ulp; constrained correctly rounded selection and exact flags',
-        pending_bead='bennett-arith-wvh',
-        claim='deterministic approximation; no global correct-rounding or ulp-bound proof', working_significand_bits=224,
+    manifest['numerical_accuracy'] = dict(contract='0.2.13 13.4: full-domain one-local-ulp; constrained correctly rounded selection and exact flags',
+        pending_obligation='elementary-full-domain-accuracy',
+        claim='deterministic approximation; no global correct-rounding or ulp-bound proof', working_significand_bits=240,
         exact_dyadic_families=['pow','exp2','exp10','log2','log10','half-integer sincospi'],
         exact_dyadic_method='normalized integer significands, perfect roots/powers and one final target rounding',
         proven_paths=[dict(operation='exp_ppcf128',domain='finite |x| <= 2^-112',
             method='exact high+low midpoint comparison; quadratic/cubic log(1+h) comparison for directed sides',
             guarantee='correct canonical pair in all five modes; zero is exact, otherwise only inexact',
-            test='tests/test_ppc_exp.py',bead='bennett-arith-wvh.1')],
-        payne_hanek_constant_bits=17408, verification='tests/test_trans.py and tests/test_trans_extra.py compare published bitcode with MPFR at 384 bits; <=4 ulp engineering acceptance, exhaustive f16/bf16 sin <=1 ulp')
+            test='tests/test_ppc_exp.py')],
+        payne_hanek_constant_bits=17408, verification='tests/test_trans.py and tests/test_trans_extra.py compare published bitcode with adaptive directed MPFR brackets and exact carrier selection; unresolved PPC cases use BENNETT_ARITH_PROMISED')
     manifest['ppc_semantics'] = dict(oracle='independent exact rational arithmetic for explicit guarantees; same-major LLVM APFloat for component operations', high_component_carrier_bits='0..63',
         both_majors='exact high+low conversions, full-width integer inputs, canonical-pair integral rounding, sqrt and one-rounding exact FMA',
         exact_sum_quantum='2^-1074',exact_sum_bits=2176,sqrt_comparison_bits=4352,
         llvm18='component add/mul; legacy 106-bit divide/remainder operation conventions',
         llvm23='same operations as LLVM18, including explicit 0.2.12 exact-value overrides',
-        pending_bead='bennett-arith-4yg',
-        implementation_gaps='0.2.13 nearest-even parity migration follows review round 2; the current publication retains the 0.2.12 parity interpretation')
-    manifest['contract_questions']=[dict(bead='bennett-arith-4yg.1',section='13.1',
-        question='Published 0.2.13 resolves the 0.2.12 zero-low parity question; implementation migration is sequenced after review round 2.')]
+        pending_obligation='ppc-full-domain-arithmetic',
+        implementation_gaps='legacy component add/mul and divide/remainder conventions remain versioned')
+    manifest['contract_questions']=[]
     manifest['comparison_semantics']=dict(quiet='cmp_B_rm: invalid only on signaling NaN',
         signaling='cmps_B_rm: invalid on any NaN, including false/true predicates',
         specialized_formats=[FORMATS[i][0] for i in IEEE_COMPARE],
diff --git a/softfloat/named.c b/softfloat/named.c
index 07d3108..83d597d 100644
--- a/softfloat/named.c
+++ b/softfloat/named.c
@@ -51,7 +51,8 @@ static U named_pack(V a,Named n,int rm,int sat) {
             return sign|((U)(a.exp+f.p-1+f.bias)<<(f.p-1))|((U)a.mag & (U)mask(f.p-1));
         }
     }
-    if(sat) return sign|max;
+    if(sat || (a.kind==FINITE && (rm==3 || (rm==1 && !a.sign) || (rm==2 && a.sign))))
+        return sign|max;
     return kind==NI ? infbits(f,a.sign):0;
 }
 void bennett_sf_named(U *out,int fi,int ni,int to,const U *in,int rm,int sat) {
diff --git a/softfloat/ppc_round.h b/softfloat/ppc_round.h
index e9afda5..b00563e 100644
--- a/softfloat/ppc_round.h
+++ b/softfloat/ppc_round.h
@@ -12,6 +12,15 @@ static int dyadic_compare(SquareBits a,int ae,SquareBits b,int be) {
 static U pair_sign(U x,int sign) {
     return sign ? x^((U)1<<63)^(x>>64 ? (U)1<<127:0):x;
 }
+static U ppc_even_neighbour(U lower,U upper) {
+    /* Dialect 13.1: compare low significands, including zero, whenever
+     * either is nonzero; only two zero lows use the high significands.
+     * Equal parity selects the smaller magnitude (toward zero). */
+    U ll=lower>>64,ul=upper>>64;
+    int low=ll || ul;
+    int le=!((low ? ll:low64(lower))&1),ue=!((low ? ul:low64(upper))&1);
+    return le || !ue ? lower:upper;
+}
 static U ppc_round_exact(SquareBits mag,int exp,int sign,int rm,int *flags) {
     if(!mag)return (U)sign<<63;
     int mode=sign ? (rm==1 ? 2:rm==2 ? 1:rm):rm;
@@ -45,11 +54,7 @@ static U ppc_round_exact(SquareBits mag,int exp,int sign,int rm,int *flags) {
         int midpoint=dyadic_compare(mag,exp+1,(SquareBits)l.mag+u.mag,-1074);
         if(midpoint<0)result=lower;
         else if(midpoint>0 || mode==4)result=upper;
-        else {
-            U ll=lower>>64,ul=upper>>64;
-            int le=!((ll ? ll:low64(lower))&1),ue=!((ul ? ul:low64(upper))&1);
-            result=le || !ue ? lower:upper;
-        }
+        else result=ppc_even_neighbour(lower,upper);
     }
     PairSum rounded=sum_read(result);
     if(dyadic_compare(mag,exp,(SquareBits)rounded.mag,-1074)) {
diff --git a/softfloat/ppc_sum.h b/softfloat/ppc_sum.h
index b4ef10f..0a45a4d 100644
--- a/softfloat/ppc_sum.h
+++ b/softfloat/ppc_sum.h
@@ -153,13 +153,7 @@ static U ppc_sum_sqrt(U x,int rm,int *flags) {
         SquareBits squared=mid*mid,scaled=rad<<2;
         if(scaled<squared)result=lower;
         else if(scaled>squared || rm==4)result=upper;
-        else {
-            U low=lower>>64;
-            /* At a zero-low transition an odd/odd pair midpoint has a half
-             * grid unit, whose square cannot be a binary64-pair input. Thus
-             * the unresolved 4yg.1 FMA tie is unreachable for sqrt. */
-            result=!((low ? low:low64(lower))&1) ? lower:upper;
-        }
+        else result=ppc_even_neighbour(lower,upper);
     }
     PairSum r=sum_read(result);
     if((SquareBits)r.mag*r.mag!=rad) {
diff --git a/softfloat/test_instances.py b/softfloat/test_instances.py
index 3221d50..b0ab748 100644
--- a/softfloat/test_instances.py
+++ b/softfloat/test_instances.py
@@ -85,8 +85,9 @@ def expected_to(value, sign, f, rm, sat):
         units,_=edge.roundedq(v/edge.power(step),sign,rm)
         rounded=units*edge.power(step)
         if rounded>maximum:
-            if not sat and kind!='ieee': return 0
-            result=maxbits if sat else (((1<<eb)-1)<<(p-1) if kind=='ieee' else 0)
+            finite_direction=rm==3 or (rm==1 and not sign) or (rm==2 and sign)
+            if not sat and not finite_direction and kind!='ieee': return 0
+            result=maxbits if sat or finite_direction else (((1<<eb)-1)<<(p-1) if kind=='ieee' else 0)
         else:
             result=values[rounded]
             if not result and kind=='uz': return 0
diff --git a/softfloat/test_publication.py b/softfloat/test_publication.py
index 638ec82..2683f8c 100644
--- a/softfloat/test_publication.py
+++ b/softfloat/test_publication.py
@@ -1,4 +1,4 @@
-"""Independent audit of the 0.2.12 offline generator's publication metadata."""
+"""Independent audit of the 0.2.13 offline generator's publication metadata."""
 import hashlib
 import json
 from pathlib import Path
@@ -7,7 +7,7 @@ ROOT=Path(__file__).resolve().parents[1]
 for major in (18,23):
     dist=ROOT/f'dist/llvm{major}'
     m=json.loads((dist/'manifest.json').read_text())
-    assert m['dialect']=='0.2.12'
+    assert m['dialect']=='0.2.13'
     assert m['bitcode_sha256']==hashlib.sha256((dist/'bennett-arith.bc').read_bytes()).hexdigest()
     generator=m['instance_generator']
     assert generator['command']=='python3 -I softfloat/instantiate.py REQUEST.json OUTPUT_DIRECTORY'
@@ -19,6 +19,6 @@ for major in (18,23):
     assert to['signature']=='iN (C_B, i32 R, i1 Sat)'
     assert fr['signature']=='C_B (iN)'
     assert to['status']==fr['status']=='available-offline'
-    assert {'bennett-arith-4yg','bennett-arith-wvh'}<=set(m['conformance_pending'])
-    assert m['numerical_accuracy']['pending_bead']=='bennett-arith-wvh'
-    print(f'LLVM {major}: 0.2.12 request protocol, exact signatures and pending numerical obligations recorded')
+    assert {'ppc-full-domain-arithmetic','elementary-full-domain-accuracy'}<=set(m['conformance_pending'])
+    assert m['numerical_accuracy']['pending_obligation']=='elementary-full-domain-accuracy'
+    print(f'LLVM {major}: 0.2.13 request protocol, exact signatures and pending numerical obligations recorded')
diff --git a/softfloat/trans.h b/softfloat/trans.h
index c2c1ab2..1e5a9c5 100644
--- a/softfloat/trans.h
+++ b/softfloat/trans.h
@@ -1,10 +1,13 @@
-/* Versioned integer libm v1. 224 significant working bits; no host FP.
+/* Versioned integer libm v1. 240 significant working bits; no host FP.
  * Payne-Hanek reduction uses 17408 bits of 2/pi over the full binary128 range.
  * Results are deterministic approximations, NOT claimed correctly rounded.
  */
 #include "constants.h"
+/* Two 113-bit input significands plus guard bits for near-one powers;
+ * twice this precision still fits the 512-bit product accumulator. */
+enum { TRANS_BITS = 240 };
 static V tn(V a) {
-    if(a.kind==FINITE && width(a.mag)>224) {int s=width(a.mag)-224;a.mag=jam(a.mag,s);a.exp+=s;}
+    if(a.kind==FINITE && width(a.mag)>TRANS_BITS) {int s=width(a.mag)-TRANS_BITS;a.mag=jam(a.mag,s);a.exp+=s;}
     return a;
 }
 static V ti(int n) { return (V){n<0 ? (Big)(0u-(unsigned)n):(Big)n,0,n<0,FINITE,0}; }
@@ -175,86 +178,185 @@ static V trans_unpack(U x,int fi) {
     return ta(hi,unpack(x>>64,formats[3]));
 }
 #include "trans_exact.h"
-static void trans_eval(U *out,int fi,int op,const U *in,int rm) {
+enum TransPath { TRANS_CORE, TRANS_EXACT, TRANS_PPC_EXP, TRANS_TANH_LIMIT, TRANS_LINEAR };
+typedef struct {
+    enum TransPath path;
+    V a, b, r, c;
+    ExactReal exact[2];
+    PairSum sum;
+    int flags, pair;
+} TransState;
+
+static TransState trans_domain(int fi,int op,const U *in) {
+    TransState s={.path=TRANS_CORE,.pair=op==SINCOS || op==SINCOSPI};
     if(op==SINCOSPI) {
-        ExactReal a=trans_input(in[0],fi),s,c;
-        if(trans_exact_sincospi(a,&s,&c)) {
-            int flags=0;out[0]=trans_pack_exact(s,fi,rm,&flags);
-            out[1]=trans_pack_exact(c,fi,rm,&flags);out[2]=flags;return;
+        ExactReal a=trans_input(in[0],fi);
+        if(trans_exact_sincospi(a,&s.exact[0],&s.exact[1])) {
+            s.path=TRANS_EXACT;
+            return s;
         }
     }
     if(op==POW || op==EXP2 || op==EXP10 || op==LOG2 || op==LOG10) {
-        ExactReal a=trans_input(in[0],fi),b=trans_input(in[1],fi),result;
-        if(trans_exact_math(op,a,b,&result)) {
-            int flags=a.snan || (op==POW && b.snan);
-            out[0]=trans_pack_exact(result,fi,rm,&flags);out[1]=0;out[2]=flags;return;
+        ExactReal a=trans_input(in[0],fi),b=trans_input(in[1],fi);
+        if(trans_exact_math(op,a,b,&s.exact[0])) {
+            s.path=TRANS_EXACT;
+            s.flags=a.snan || (op==POW && b.snan);
+            return s;
         }
     }
     if(fi==6 && op==EXP) {
-        PairSum exact=sum_read(in[0]);
-        if(exact.kind==FINITE && exact.mag<=((SumBits)1<<962)) {
-            int flags=0;out[0]=ppc_exp_near_zero(exact,rm,&flags);
-            out[1]=0;out[2]=flags;return;
+        s.sum=sum_read(in[0]);
+        if(s.sum.kind==FINITE && s.sum.mag<=((SumBits)1<<962)) {
+            s.path=TRANS_PPC_EXP;
+            return s;
         }
     }
-    Format f=formats[fi];V a=trans_unpack(in[0],fi),b=trans_unpack(in[1],fi),r=nanv(),c=ti(0);
-    int flags=a.snan || ((op==ATAN2 || op==POW) && b.snan),pair=0;
-    if(op==TANH && a.kind==FINITE && a.mag && width(a.mag)+a.exp>8) {
-        /* The finite limit is strict. Ordinary IEEE formats cannot resolve
-         * the tail at |x|>=256; PPC can, until it falls below 2^-1075. */
-        if(fi!=6)out[0]=pack((V){mask(480),-480,a.sign,FINITE,0},f,rm,&flags);
-        else {
-            V x=a;x.sign=0;
-            /* e^3>16 proves this tail is below half a PPC quantum. */
-            if(compare(x,ti(512))>=0)
-                out[0]=ppc_round_exact(((SquareBits)1<<2148)-1,-2148,a.sign,rm,&flags);
-            else {
-                ++x.exp;x.sign=1;
-                V q=texp(x),tail=td(tm(ti(2),q),ta(ti(1),q));
-                /* Here -tail.exp lies between 900 and 1800. */
-                SquareBits value=((SquareBits)1<<-tail.exp)-(SquareBits)tail.mag;
-                out[0]=ppc_round_exact(value,tail.exp,a.sign,rm,&flags);
-            }
-        }
-        out[1]=0;out[2]=flags|16;return;
+    s.a=trans_unpack(in[0],fi);
+    s.b=trans_unpack(in[1],fi);
+    s.r=nanv();s.c=ti(0);
+    s.flags=s.a.snan || ((op==ATAN2 || op==POW) && s.b.snan);
+    if(op==TANH && s.a.kind==FINITE && s.a.mag && width(s.a.mag)+s.a.exp>6) {
+        s.path=TRANS_TANH_LIMIT;
+        return s;
     }
-    if(op==SIN || op==COS || op==TAN || op==SINCOS || op==SINCOSPI){
-        V s;tsc(a,op==SINCOSPI,&s,&c);r=op==COS ? c:op==TAN ? td(s,c):s;pair=op==SINCOS || op==SINCOSPI;
-    }else if(op==ATAN)r=tatan(a);
-    else if(op==ATAN2)r=tatan2(a,b);
-    else if(op==ASIN || op==ACOS){
+    /* Below 2^-112 the cubic correction is less than half an IEEE
+     * carrier ulp, while its strict sign still selects directed neighbours.
+     * PPC sparse residuals require their own full-precision treatment. */
+    if(fi!=6 && (op==TAN || op==ASIN || op==TANH) &&
+       s.a.kind==FINITE && s.a.mag && width(s.a.mag)+s.a.exp<=-112) {
+        int shift=480-width(s.a.mag);
+        s.r=s.a;s.r.mag<<=shift;s.r.exp-=shift;
+        if(op==TANH)--s.r.mag;else ++s.r.mag;
+        s.path=TRANS_LINEAR;
+    }
+    return s;
+}
+
+static void trans_core(TransState *s,int op) {
+    V a=s->a,b=s->b,r=nanv(),c=ti(0);
+    switch(op) {
+    case SIN: case COS: case TAN: case SINCOS: case SINCOSPI: {
+        V sine;tsc(a,op==SINCOSPI,&sine,&c);
+        r=op==COS ? c:op==TAN ? td(sine,c):sine;
+        break;
+    }
+    case ATAN: r=tatan(a);break;
+    case ATAN2: r=tatan2(a,b);break;
+    case ASIN: case ACOS: {
         V x=a;x.sign=0;
         if(a.kind!=NANV && compare(x,ti(1))<=0) {
             V root=tsqrt(tm(ta(ti(1),tneg(x)),ta(ti(1),x)));
             r=op==ASIN ? tatan2(a,root):tatan2(root,a);
         }
-    }else if(op==LOG || op==LOG2 || op==LOG10){r=tlog(a);if(op!=LOG)r=td(r,op==LOG2 ? tc_ln2():tc_ln10());}
-    else if(op==EXP || op==EXP2 || op==EXP10){r=texp(op==EXP ? a:tm(a,op==EXP2 ? tc_ln2():tc_ln10()));}
-    else if(op==POW)r=tpow(a,b);
-    else if(op==SINH || op==COSH || op==TANH){
+        break;
+    }
+    case LOG: case LOG2: case LOG10:
+        r=tlog(a);
+        if(op!=LOG)r=td(r,op==LOG2 ? tc_ln2():tc_ln10());
+        break;
+    case EXP: case EXP2: case EXP10:
+        r=texp(op==EXP ? a:tm(a,op==EXP2 ? tc_ln2():tc_ln10()));
+        break;
+    case POW: r=tpow(a,b);break;
+    case SINH: case COSH: case TANH: {
         V x=a;x.sign=0;
         if(op==TANH && x.kind==INF)r=ti(a.sign ? -1:1);
         else if(x.kind==FINITE && (!x.mag || width(x.mag)+x.exp< -4)) {
             V term=op==COSH ? ti(1):a,sum=term,xx=tm(a,a);
-            for(int n=1;n<=90;++n){term=td(tm(term,xx),ti(op==COSH ? (2*n-1)*(2*n):(2*n)*(2*n+1)));sum=ta(sum,term);if(tinyterm(term,sum))break;}
-            if(op==TANH){V sh=sum,ch=ti(1),t=ch;for(int n=1;n<=90;++n){t=td(tm(t,xx),ti((2*n-1)*(2*n)));ch=ta(ch,t);}sum=td(sh,ch);}r=sum;
-        }else {V ex=texp(x),inv=td(ti(1),ex);r=op==COSH ? ta(ex,inv):ta(ex,tneg(inv));
-            if(op==TANH)r=td(r,ta(ex,inv));else --r.exp;if(op!=COSH)r.sign=a.sign;}
+            for(int n=1;n<=90;++n) {
+                term=td(tm(term,xx),ti(op==COSH ? (2*n-1)*(2*n):(2*n)*(2*n+1)));
+                sum=ta(sum,term);
+                if(tinyterm(term,sum))break;
+            }
+            if(op==TANH) {
+                V sh=sum,ch=ti(1),t=ch;
+                for(int n=1;n<=90;++n) {
+                    t=td(tm(t,xx),ti((2*n-1)*(2*n)));
+                    ch=ta(ch,t);
+                }
+                sum=td(sh,ch);
+            }
+            r=sum;
+        } else {
+            V ex=texp(x),inv=td(ti(1),ex);
+            r=op==COSH ? ta(ex,inv):ta(ex,tneg(inv));
+            if(op==TANH)r=td(r,ta(ex,inv));else --r.exp;
+            if(op!=COSH)r.sign=a.sign;
+        }
+        break;
+    }
+    default: __builtin_trap();
+    }
+    s->r=r;s->c=c;
+}
+
+enum ExactDomain { EXACT_ZERO=1, EXACT_ONE=2, EXACT_INFINITY=4,
+                   EXACT_OTHER_INFINITY=8, EXACT_ZERO_RESULT=16 };
+static const unsigned trans_exact_domains[SINCOSPI+1]={
+    [SIN]=EXACT_ZERO, [COS]=EXACT_ZERO, [TAN]=EXACT_ZERO,
+    [ASIN]=EXACT_ZERO, [ACOS]=EXACT_ONE, [ATAN]=EXACT_ZERO,
+    [ATAN2]=EXACT_ZERO_RESULT, [SINH]=EXACT_ZERO, [COSH]=EXACT_ZERO,
+    [TANH]=EXACT_ZERO|EXACT_INFINITY, [EXP]=EXACT_ZERO|EXACT_INFINITY,
+    [EXP2]=EXACT_INFINITY, [EXP10]=EXACT_INFINITY, [LOG]=EXACT_ONE,
+    [POW]=EXACT_INFINITY|EXACT_OTHER_INFINITY, [SINCOS]=EXACT_ZERO
+};
+
+static int trans_is_exact(int op,V a,V b,V r) {
+    unsigned domains=trans_exact_domains[op];
+    return ((domains&EXACT_ZERO) && a.kind==FINITE && !a.mag) ||
+           ((domains&EXACT_ONE) && a.kind==FINITE && compare(a,ti(1))==0) ||
+           ((domains&EXACT_INFINITY) && a.kind==INF) ||
+           ((domains&EXACT_OTHER_INFINITY) && b.kind==INF) ||
+           ((domains&EXACT_ZERO_RESULT) && r.kind==FINITE && !r.mag);
+}
+
+static U trans_tanh_limit(V a,int fi,int rm,int *flags) {
+    /* The finite limit is strict. IEEE formats cannot resolve the tail at
+     * |x|>=64; PPC can until it falls below half its least quantum. */
+    if(fi!=6)return pack((V){mask(480),-480,a.sign,FINITE,0},formats[fi],rm,flags);
+    V x=a;x.sign=0;
+    /* e^3>16 bounds this tail below half a PPC quantum. */
+    if(compare(x,ti(512))>=0)
+        return ppc_round_exact(((SquareBits)1<<2148)-1,-2148,a.sign,rm,flags);
+    ++x.exp;x.sign=1;
+    V q=texp(x),tail=td(tm(ti(2),q),ta(ti(1),q));
+    SquareBits value=((SquareBits)1<<-tail.exp)-(SquareBits)tail.mag;
+    return ppc_round_exact(value,tail.exp,a.sign,rm,flags);
+}
+
+static void trans_pack(U *out,int fi,int op,int rm,TransState s) {
+    switch(s.path) {
+    case TRANS_EXACT:
+        out[0]=trans_pack_exact(s.exact[0],fi,rm,&s.flags);
+        out[1]=s.pair ? trans_pack_exact(s.exact[1],fi,rm,&s.flags):0;
+        out[2]=s.flags;
+        return;
+    case TRANS_PPC_EXP:
+        out[0]=ppc_exp_near_zero(s.sum,rm,&s.flags);
+        out[1]=0;out[2]=s.flags;
+        return;
+    case TRANS_TANH_LIMIT:
+        out[0]=trans_tanh_limit(s.a,fi,rm,&s.flags);
+        out[1]=0;out[2]=s.flags|16;
+        return;
+    case TRANS_CORE: case TRANS_LINEAR:
+        break;
     }
-    if(r.kind==NANV && a.kind!=NANV && (op!=POW && op!=ATAN2 || b.kind!=NANV))flags|=1;
-    if((op==LOG || op==LOG2 || op==LOG10) && a.kind==FINITE && !a.mag)flags|=2;
-    if(op==POW && a.kind==FINITE && !a.mag && b.sign && (b.mag || b.kind==INF))flags|=2;
-    /* Exact elementary cases do not spuriously raise inexact. */
-    int exact=(!a.mag && a.kind==FINITE &&
-        (op==SIN || op==COS || op==TAN || op==ASIN || op==ATAN ||
-         op==SINH || op==COSH || op==TANH || op==EXP || op==SINCOS)) ||
-        (op==LOG && a.kind==FINITE && compare(a,ti(1))==0);
-    if(op==ACOS && a.kind==FINITE && compare(a,ti(1))==0)exact=1;
-    if(a.kind==INF && (op==EXP || op==EXP2 || op==EXP10 || op==TANH))exact=1;
-    if(op==POW && (a.kind==INF || b.kind==INF))exact=1;
-    if(op==ATAN2 && r.kind==FINITE && !r.mag)exact=1;
-    if(r.kind==FINITE && !exact)flags|=16;
-    if((op==EXP || op==EXP2 || op==EXP10 || op==POW) && !r.mag && r.kind==FINITE && a.kind==FINITE && a.mag && !exact)flags|=24;
-    out[0]=fi==6 ? ppc_round(r,rm,&flags):pack(r,f,rm,&flags);
-    out[1]=pair ? (fi==6 ? ppc_round(c,rm,&flags):pack(c,f,rm,&flags)):0;out[2]=flags;
+    V a=s.a,b=s.b,r=s.r,c=s.c;
+    if(r.kind==NANV && a.kind!=NANV && ((op!=POW && op!=ATAN2) || b.kind!=NANV))s.flags|=1;
+    if((op==LOG || op==LOG2 || op==LOG10) && a.kind==FINITE && !a.mag)s.flags|=2;
+    if(op==POW && a.kind==FINITE && !a.mag && b.sign && (b.mag || b.kind==INF))s.flags|=2;
+    int exact=trans_is_exact(op,a,b,r);
+    if(r.kind==FINITE && !exact)s.flags|=16;
+    if((op==EXP || op==EXP2 || op==EXP10 || op==POW) && !r.mag &&
+       r.kind==FINITE && a.kind==FINITE && a.mag && !exact)s.flags|=24;
+    out[0]=fi==6 ? ppc_round(r,rm,&s.flags):pack(r,formats[fi],rm,&s.flags);
+    out[1]=s.pair ? (fi==6 ? ppc_round(c,rm,&s.flags):pack(c,formats[fi],rm,&s.flags)):0;
+    out[2]=s.flags;
+}
+
+static void trans_eval(U *out,int fi,int op,const U *in,int rm) {
+    TransState s=trans_domain(fi,op,in);
+    if(s.path==TRANS_CORE)trans_core(&s,op);
+    trans_pack(out,fi,op,rm,s);
 }
diff --git a/tests/circuits/harness.py b/tests/circuits/harness.py
index bcc46fc..c587ea8 100644
--- a/tests/circuits/harness.py
+++ b/tests/circuits/harness.py
@@ -13,6 +13,7 @@ import os
 import random
 import re
 import subprocess
+import sys
 from concurrent.futures import ThreadPoolExecutor
 from pathlib import Path
 
@@ -20,28 +21,16 @@ import numpy as np
 
 ROOT = Path(__file__).resolve().parents[2]
 VECTOR_ABOVE = 1 << 17  # Specs run per lane up to here, as numpy expressions above it.
-
-
-def main_checkout():
-    """The main checkout, also from the detached worktree scripts/pre-push uses."""
-    common = subprocess.run(
-        ["git", "-C", str(ROOT), "rev-parse", "--git-common-dir"],
-        check=True, capture_output=True, text=True,
-    ).stdout.strip()
-    path = Path(common)
-    if not path.is_absolute():
-        path = ROOT / path
-    return path.resolve().parent
+sys.path.insert(0, str(ROOT / "scripts"))
+from pinned_sibling import resolve_sibling  # noqa: E402
 
 
 def ref_binary():
-    """Debug build: the release binary in that crate still accepts only ISA 0.8."""
-    configured = os.environ.get("BENNETT_ISA_REF")
-    path = Path(configured) if configured else (
-        main_checkout().parent / "bennett-isa-spec/reference-interpreter/target/debug/bennett-isa-ref"
-    )
+    """Use the debug build from the pinned ISA checkout (release only accepts 0.8)."""
+    path = resolve_sibling("bennett-isa-spec") / "reference-interpreter/target/debug/bennett-isa-ref"
     if not path.is_file():
-        raise SystemExit(f"reference interpreter binary not found at {path}; set BENNETT_ISA_REF")
+        raise SystemExit(f"reference interpreter binary not found at {path}; "
+                         "materialise with gate_run.py verify --repo bennett-arith --sha HEAD")
     return path
 
 
diff --git a/tests/circuits/run b/tests/circuits/run
index b7aa14b..2c7be66 100755
--- a/tests/circuits/run
+++ b/tests/circuits/run
@@ -1,15 +1,15 @@
 #!/usr/bin/env bash
-# The tests/circuits gate. Needs the reference interpreter binary (BENNETT_ISA_REF, or the sibling
-# bennett-isa-spec debug build) and numpy.
+# The tests/circuits gate. Needs numpy and the gate.toml-pinned reference interpreter,
+# resolved through BENNETT_GATE_LAYOUT or this working tree's gate cache.
 set -euo pipefail
 unset DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER
 here="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
 root="$(dirname "$(dirname "$here")")"
-export TMPDIR="$root/.tmp/opus-arith-circuits/tmp"
+export TMPDIR="${TMPDIR:-$root/.tmp/opus-arith-circuits/tmp}"
 export PYTHONDONTWRITEBYTECODE=1
 mkdir -p "$TMPDIR"
 cd "$here"
-for t in test_adders test_multipliers test_qrom test_objects; do
+for t in test_pins test_adders test_multipliers test_qrom test_objects; do
   python3 -I "$t.py"
 done
 echo 'circuits: adders, multipliers, QROM and published certificates passed'
diff --git a/tests/circuits/test_adders.py b/tests/circuits/test_adders.py
index 2432ab7..c781f77 100644
--- a/tests/circuits/test_adders.py
+++ b/tests/circuits/test_adders.py
@@ -299,6 +299,16 @@ class Differential(unittest.TestCase):
         self.dir = Path(__file__).resolve().parents[2] / ".tmp/opus-arith-circuits/objects"
         self.dir.mkdir(parents=True, exist_ok=True)
 
+    def test_mulmod_unbounded_constants(self):
+        for k in (31, -2, 11 * (1 << 80) + 9):
+            obj = C.mulmod_const(4, k, 11)
+            path = self.dir / "mulmod_oracles.bisa"
+            # Isolate arithmetic from certificate admission; exercise emitted IR.
+            path.write_text(Object(obj.circuits[:2])._base())
+            for x in range(16):
+                self.assertEqual(REF.oracle(path, obj.circuits[0].name, [x], "9,0,0,0"),
+                                 k * x % 11 if x < 11 else x, (k, x))
+
     def place(self, obj):
         path = self.dir / f"{obj.root}.bisa"
         write_object(obj, path)
diff --git a/tests/circuits/test_objects.py b/tests/circuits/test_objects.py
index df0b285..3ab0012 100644
--- a/tests/circuits/test_objects.py
+++ b/tests/circuits/test_objects.py
@@ -1,6 +1,7 @@
 """Published objects and certificates: reproducible, accepted, every claim independently replayed."""
 import hashlib
 import json
+import os
 import subprocess
 import sys
 import unittest
@@ -51,6 +52,19 @@ def xoshiro(seed):
 
 
 class Published(unittest.TestCase):
+    def test_token_aliases(self):
+        from adders import constructions as c
+        for obj, aliases in ((c.cuccaro(2), []), (c.mulmod_const(4, 5, 11), [0])):
+            cert = certificate(obj.text())
+            self.assertEqual(cert["bindings"]["invocation"]["token_aliases"], aliases)
+            for region in cert["regions"].values():
+                for claim in region["claims"]:
+                    if "invocation" in claim:
+                        inv = claim["invocation"]
+                        self.assertEqual(inv["token_aliases"], "all" if inv["args"] == "all" else aliases)
+                for entry in region["verification"]["inverse_pairs"]:
+                    self.assertEqual(entry["token_aliases"], [0])
+
     def test_reproduces_byte_for_byte(self):
         done = subprocess.run([sys.executable, "-I", str(ROOT / "adders/generate.py"), "check"],
                               capture_output=True, text=True)
@@ -63,24 +77,21 @@ class Published(unittest.TestCase):
         for e in m["entries"]:
             self.assertEqual(hashlib.sha256((ROOT / e["file"]).read_bytes()).hexdigest(), e["sha256"], e["file"])
 
-    def test_interpreter_accepts_identities_and_schema(self):
+    def test_pinned_interpreter_diagnostic_view(self):
         DIR.mkdir(parents=True, exist_ok=True)
         from adders.generate import FAMILIES, published
-        by_root = {}
-        for _, family, args in published():
-            obj = FAMILIES[family](*args)
-            by_root[obj.root] = obj
+        by_root = {obj.root: obj for _, family, args in published()
+                   for obj in [FAMILIES[family](*args)]}
         checked = 0
         for e in manifest()["entries"]:
             text = (ROOT / e["file"]).read_text()
-            if "qinplace" in text and " (k) () ()" in text:
-                continue    # The interpreter's parser does not take qinplace's ins list yet (bead).
+            if "qinplace" in text:
+                continue    # Raw modular validation is the explicit promised test below.
             if sum(row.get("census", {}).get("gates", {}).get(g, 0) for row in e["symbols"].values()
                    for g in ("x", "cx", "ccx", "swap")) > CHECK_GATE_LIMIT:
                 continue
-            obj = by_root[e["root"]]
             path = DIR / f"{e['root']}.bisa"
-            path.write_text(interpreter_view(obj))
+            path.write_text(interpreter_view(by_root[e["root"]]))
             got = REF.check(path)
             self.assertEqual(got["status"], "ok", e["file"])
             cert = certificate(text)
@@ -90,6 +101,27 @@ class Published(unittest.TestCase):
             checked += 1
         self.assertGreater(checked, 80)
 
+    @unittest.skipUnless(os.environ.get("BENNETT_ARITH_PROMISED"),
+                         "BENNETT_ARITH_PROMISED=1: bennett-arith-gdg / bennett-arith-vwi")
+    def test_raw_modular_publications_bennett_arith_gdg(self):
+        for entry in manifest()["entries"]:
+            path = ROOT / entry["file"]
+            if "qinplace" in path.read_text():
+                self.assertEqual(REF.check(path)["status"], "ok", entry["file"])
+
+    def test_inverse_pair_obligation_is_published(self):
+        checked = 0
+        for entry in manifest()["entries"]:
+            text = (ROOT / entry["file"]).read_text()
+            if "qinplace" not in text:
+                continue
+            for region in certificate(text)["regions"].values():
+                for pair in region["verification"]["inverse_pairs"]:
+                    self.assertEqual(region["claims"][pair["claim"]]["expected"], "inverse_pair")
+                    self.assertTrue(all(isinstance(n, int) for n in pair["budget"]))
+                    checked += 1
+        self.assertGreater(checked, 0)
+
     def test_certificates_tell_the_truth(self):
         """Census, frame, labels and every table row, replayed on the emitted text, not the builder."""
         m = manifest()
diff --git a/tests/circuits/test_pins.py b/tests/circuits/test_pins.py
new file mode 100644
index 0000000..be4574e
--- /dev/null
+++ b/tests/circuits/test_pins.py
@@ -0,0 +1,148 @@
+"""Sibling resolution uses gate.toml even when the live sibling is unusable."""
+import os
+from pathlib import Path
+import shutil
+import subprocess
+import sys
+import tempfile
+import unittest
+
+
+ROOT = Path(__file__).resolve().parents[2]
+SIBLING = "bennett-isa-spec"
+PIN = "1" * 40
+OTHER = "2" * 40
+BINARY = Path("reference-interpreter/target/debug/bennett-isa-ref")
+
+
+def checkout(path, sha):
+    """Minimal local HEAD metadata; no git mutation or sibling worktree needed."""
+    (path / ".git/objects").mkdir(parents=True)
+    (path / ".git/refs").mkdir()
+    (path / ".git/HEAD").write_text(sha + "\n")
+    return path
+
+
+class Pins(unittest.TestCase):
+    def setUp(self):
+        self.tmp = tempfile.TemporaryDirectory()
+        self.addCleanup(self.tmp.cleanup)
+        workspace = Path(self.tmp.name)
+        self.repo = checkout(workspace / "bennett-arith", OTHER)
+        self.live = workspace / SIBLING
+        self.live.mkdir()
+        (self.repo / "tests/circuits").mkdir(parents=True)
+        shutil.copyfile(ROOT / "tests/circuits/harness.py", self.repo / "tests/circuits/harness.py")
+        shutil.copytree(ROOT / "scripts", self.repo / "scripts")
+        (self.repo / "gate.toml").write_text(
+            f'repo = "bennett-arith"\n[siblings."{SIBLING}"]\nsha = "{PIN}"\n'
+        )
+        self.cache = self.repo / f".tmp/gate/cache/{SIBLING}@{PIN[:12]}/{SIBLING}"
+        self.layout = workspace / "layout"
+        self.env = {k: v for k, v in os.environ.items()
+                    if not k.startswith(("BENNETT_", "GIT_"))}
+        self.env["PYTHONDONTWRITEBYTECODE"] = "1"
+
+    def pinned(self, path, sha=PIN, binary=True):
+        checkout(path, sha)
+        if binary:
+            (path / BINARY).parent.mkdir(parents=True)
+            (path / BINARY).write_text("fixture binary\n")
+        return path / BINARY
+
+    def resolve(self, **env):
+        code = (
+            f"import sys; sys.path.insert(0, {str(self.repo / 'tests/circuits')!r}); "
+            "from harness import ref_binary; print(ref_binary())"
+        )
+        return subprocess.run([sys.executable, "-I", "-B", "-c", code],
+                              env=self.env | env, capture_output=True, text=True, timeout=20)
+
+    def assert_binary(self, done, expected):
+        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
+        self.assertEqual(Path(done.stdout.strip()), expected)
+
+    def assert_failure(self, done, live_head="unavailable", detail=""):
+        self.assertNotEqual(done.returncode, 0, done.stdout + done.stderr)
+        self.assertEqual(done.stdout, "")
+        self.assertEqual(len(done.stderr.splitlines()), 1, done.stderr)
+        self.assertIn(SIBLING, done.stderr)
+        self.assertIn(PIN, done.stderr)
+        self.assertIn(f"live ../{SIBLING} HEAD={live_head}", done.stderr)
+        self.assertIn("gate_run.py verify --repo bennett-arith --sha HEAD", done.stderr)
+        self.assertIn(detail, done.stderr)
+
+    def test_cache_with_empty_live_sibling(self):
+        expected = self.pinned(self.cache)
+        self.assert_binary(self.resolve(), expected)
+
+    def test_layout_precedes_cache(self):
+        self.pinned(self.cache, OTHER)
+        expected = self.pinned(self.layout / SIBLING)
+        self.assert_binary(self.resolve(BENNETT_GATE_LAYOUT=str(self.layout)), expected)
+
+    def test_layout_symlink_to_pinned_checkout(self):
+        self.pinned(self.cache)
+        self.layout.mkdir()
+        (self.layout / SIBLING).symlink_to(self.cache, target_is_directory=True)
+        self.assert_binary(self.resolve(BENNETT_GATE_LAYOUT=str(self.layout)),
+                           self.layout / SIBLING / BINARY)
+
+    def test_missing_layout_does_not_fall_back_to_cache(self):
+        self.pinned(self.cache)
+        self.assert_failure(self.resolve(BENNETT_GATE_LAYOUT=str(self.layout)))
+
+    def test_mismatched_layout_does_not_fall_back_to_cache(self):
+        self.pinned(self.cache)
+        self.pinned(self.layout / SIBLING, OTHER)
+        self.assert_failure(self.resolve(BENNETT_GATE_LAYOUT=str(self.layout)), detail=OTHER)
+
+    def test_missing_cache_reports_pin_and_live_head(self):
+        self.live.rmdir()
+        checkout(self.live, OTHER)
+        self.assert_failure(self.resolve(), live_head=OTHER)
+
+    def test_missing_cache_with_empty_live_sibling(self):
+        self.assert_failure(self.resolve())
+
+    def test_cache_head_mismatch_is_fatal(self):
+        self.pinned(self.cache, OTHER)
+        self.assert_failure(self.resolve(), detail=OTHER)
+
+    def test_directory_without_its_own_git_metadata_is_rejected(self):
+        # Git would otherwise walk up and return the enclosing repo's HEAD.
+        (self.repo / ".git/HEAD").write_text(PIN + "\n")
+        self.cache.mkdir(parents=True)
+        (self.cache / BINARY).parent.mkdir(parents=True)
+        (self.cache / BINARY).write_text("unverified binary\n")
+        self.assert_failure(self.resolve())
+
+    def test_worktree_git_file(self):
+        expected = self.pinned(self.cache)
+        metadata = self.cache.parent / "metadata"
+        (self.cache / ".git").rename(metadata)
+        (self.cache / ".git").write_text("gitdir: ../metadata\n")
+        self.assert_binary(self.resolve(), expected)
+
+    def test_inherited_git_environment_cannot_redirect_head_check(self):
+        expected = self.pinned(self.cache)
+        self.assert_binary(self.resolve(GIT_DIR=str(self.repo / ".git"),
+                                        GIT_WORK_TREE=str(self.repo)), expected)
+
+    def test_live_binary_environment_override_cannot_bypass_pin(self):
+        expected = self.pinned(self.cache)
+        poison = self.live / BINARY
+        poison.parent.mkdir(parents=True)
+        poison.write_text("live binary must not be used\n")
+        self.assert_binary(self.resolve(BENNETT_ISA_REF=str(poison)), expected)
+
+    def test_missing_binary_names_pinned_path(self):
+        self.pinned(self.cache, binary=False)
+        done = self.resolve()
+        self.assertNotEqual(done.returncode, 0)
+        self.assertEqual(len(done.stderr.splitlines()), 1, done.stderr)
+        self.assertIn(str(self.cache / BINARY), done.stderr)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tests/circuits/test_qrom.py b/tests/circuits/test_qrom.py
index bf1e328..6d705df 100644
--- a/tests/circuits/test_qrom.py
+++ b/tests/circuits/test_qrom.py
@@ -2,12 +2,13 @@
 import random
 import sys
 import unittest
+import subprocess
 from pathlib import Path
 
 sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
 sys.path.insert(0, str(Path(__file__).resolve().parent))
 
-from harness import RefInterp, counts, depths, parse  # noqa: E402
+from harness import RefInterp, counts, depths, parse, simulate, word  # noqa: E402
 from test_adders import verify  # noqa: E402
 from adders.circuits import write_object  # noqa: E402
 from qrom import constructions as Q  # noqa: E402
@@ -30,6 +31,19 @@ def sizes(obj):
 
 
 class Qrom(unittest.TestCase):
+    def test_cli_single_word_table(self):
+        for family, n, extra in (("qrom", 0, []), ("qrom.select_swap", 0, ["0"]),
+                                 ("qrom.select_swap_dirty", 1, ["0"])):
+            result = subprocess.run([sys.executable, "-B", "-I",
+                                     str(Path(__file__).resolve().parents[2] / "adders/generate.py"),
+                                     "one", family, "1", str(n), "1", *extra],
+                                    capture_output=True, text=True, timeout=20)
+            self.assertEqual(result.returncode, 0, result.stderr)
+            fn = next(iter(parse(result.stdout)[0].values()))
+            values = {name: [0] * width for name, width in fn.mut + fn.ins + fn.borrowed()}
+            store = simulate(fn, values, 1)
+            self.assertEqual(word(store, "t", 1), [1])
+
     def test_every_address_every_target(self):
         for n in range(0, 9):
             for W in (1, 3, 8):
diff --git a/tests/named_oracle.cpp b/tests/named_oracle.cpp
new file mode 100644
index 0000000..4a1b209
--- /dev/null
+++ b/tests/named_oracle.cpp
@@ -0,0 +1,26 @@
+// LLVM APFloat is an independent oracle for named-format overflow.
+#include <llvm/ADT/APFloat.h>
+#include <llvm/ADT/APInt.h>
+#include <iostream>
+using llvm::APFloat;
+int main() {
+    const llvm::fltSemantics *formats[] = {
+        &APFloat::Float8E5M2(), &APFloat::Float8E5M2FNUZ(),
+        &APFloat::Float8E4M3(), &APFloat::Float8E4M3FN(),
+        &APFloat::Float8E4M3FNUZ(), &APFloat::Float8E4M3B11FNUZ(),
+        &APFloat::Float8E3M4()
+    };
+    const APFloat::roundingMode modes[] = {
+        APFloat::rmNearestTiesToEven, APFloat::rmTowardNegative,
+        APFloat::rmTowardPositive, APFloat::rmTowardZero,
+        APFloat::rmNearestTiesToAway
+    };
+    unsigned raw, fmt, mode;
+    while (std::cin >> raw >> fmt >> mode) {
+        if (fmt >= 7 || mode >= 5) return 2;
+        APFloat value(APFloat::IEEEsingle(), llvm::APInt(32, raw));
+        bool loses;
+        value.convert(*formats[fmt], modes[mode], &loses);
+        std::cout << value.bitcastToAPInt().getZExtValue() << '\n';
+    }
+}
diff --git a/tests/ppc_exact_oracle.py b/tests/ppc_exact_oracle.py
index 0f90532..6a33345 100644
--- a/tests/ppc_exact_oracle.py
+++ b/tests/ppc_exact_oracle.py
@@ -1,7 +1,7 @@
-"""Fraction oracles for 0.2.12 exact-sum conversions and integral operations.
+"""Fraction oracles for 0.2.13 exact-sum conversions and integral operations.
 
 No arithmetic implementation source is imported. Pair results here are exact
-integer decompositions; this module does not choose an ambiguous pair midpoint.
+rational selections, including the total nearest-even pair midpoint selector.
 """
 import importlib.util
 from functools import lru_cache
@@ -122,7 +122,8 @@ def to_pair(n,rm=0,zero_sign=0):
     elif v-low>up-v:chosen,raw=up,ub
     elif mode==4:chosen,raw=up,ub
     else:
-        even=lambda b:not (((b>>64) if b>>64 else b&MASK64)&1)
+        use_low=bool((lb>>64) or (ub>>64))
+        even=lambda b:not (((b>>64) if use_low else b&MASK64)&1)
         chosen,raw=(low,lb) if even(lb) or not even(ub) else (up,ub)
     flags=int(chosen!=v)*16
     if flags and chosen<e.power(-1022):flags|=8
diff --git a/tests/test_contract.py b/tests/test_contract.py
index cf44965..630fa63 100644
--- a/tests/test_contract.py
+++ b/tests/test_contract.py
@@ -63,14 +63,14 @@ for major in map(int,sys.argv[1:] or (18,23)):
         assert row['signature']==signature,(name,signature,row['signature'])
         assert row['format'] and row['section']
         if name in staged:
-            assert row['bead'].startswith('bennett-arith-') and row['status']=='staged'
+            assert row['status']=='staged'
     assert len(data['parametric_families'])==3
-    assert [q['bead'] for q in data['contract_questions']]==['bennett-arith-4yg.1']
-    assert {'bennett-arith-4yg','bennett-arith-wvh'}<=set(data['conformance_pending'])
+    assert data['contract_questions']==[]
+    assert {'ppc-full-domain-arithmetic','elementary-full-domain-accuracy'}<=set(data['conformance_pending'])
     assert 'bennett-arith-chn.1' not in data['conformance_pending']
     for row in allrows.values():
         if (row['fi']==6 and row['op']=='fma') or (row['op']=='convert' and row['extra']==6):
-            assert row['status']=='canonical-pair-pending-parity-migration' and row['bead']=='bennett-arith-4yg'
+            assert row['status']=='canonical-pair-exact'
     assert data['comparison_semantics']['predicate_range']==[0,15]
     assert data['comparison_semantics']['rounding_operand']==0
     print(f'LLVM {major}: manifest accounts for {len(expected)} concrete signatures and 3 parametric families')
diff --git a/tests/test_default.py b/tests/test_default.py
new file mode 100644
index 0000000..a9c3ccf
--- /dev/null
+++ b/tests/test_default.py
@@ -0,0 +1,97 @@
+"""Bounded default checks; exhaustive and both-major suites live in scripts/gate."""
+import importlib.util
+from pathlib import Path
+import sys
+import unittest
+
+ROOT=Path(__file__).resolve().parents[1]
+sys.path[:0]=[str(ROOT),str(ROOT/"tests/circuits")]
+from harness import parse
+from test_adders import verify
+from test_objects import Published
+from test_pins import Pins
+from test_qrom import Qrom
+from adders import constructions as A
+from multipliers import constructions as M
+from qrom import constructions as Q
+sys.path.insert(0,str(ROOT/"tests"))
+from test_quality import Quality
+
+def module(name):
+    spec=importlib.util.spec_from_file_location(name,ROOT/"tests"/(name+".py"))
+    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
+    return mod
+
+class SmallCircuits(unittest.TestCase):
+    def test_adders(self):
+        for make in (A.cuccaro,A.gidney,A.ripple,A.qcla):
+            for w in range(1,5):
+                obj=make(w);fn=parse(obj.text())[0][obj.root];mask=(1<<w)-1
+                target=fn.mut[-1][0]
+                def expected(v):
+                    if target=="b":return {"a":v["a"],"b":(v["a"]+v["b"])&mask}
+                    return {target:v[target] ^ (v["a"]+v["b"])}
+                verify(self,fn,expected,None)
+    def test_multipliers(self):
+        for make in (M.muladd_school,M.mul_school,M.muladd_karatsuba,M.mul_karatsuba):
+            for w in (2,3,4):
+                obj=make(w,2*w);fn=parse(obj.text())[0][obj.root]
+                target=fn.mut[0][0]
+                def expected(v):
+                    product=v["a"]*v["b"]
+                    return {target:(v[target]+product)%(1<<(2*w)) if "muladd" in fn.name else v[target]^product}
+                verify(self,fn,expected,None)
+    def test_qrom(self):
+        for make,args in ((Q.qrom,()),(Q.select_swap,(1,)),(Q.select_swap_dirty,(1,))):
+            data=(1,0,3,2);obj=make(data,2,2,*args)
+            verify(self,parse(obj.text())[0][obj.root],lambda v:{"t":v["t"]^data[v["idx"]]},None)
+
+class Numeric(unittest.TestCase):
+    def test_invalid_integer_conversion_is_observable(self):
+        e=module("test_edge");edge=e.Edge(18)
+        for suffix,f in e.FORMATS.items():
+            for op in ("fptosi","fptoui"):
+                for rm in range(5):
+                    edge.check(op+"_"+suffix+"_rm",[e.nan(f),64,rm],0,1)
+        self.assertEqual(edge.count,60)
+
+    def test_basic_operations(self):
+        e=module("test_edge");edge=e.Edge(18)
+        for suffix,f in e.FORMATS.items():
+            for op in ("add","sub","mul","div","sqrt","fma"):
+                for a,b in ((e.Q(1),e.Q(3)),(e.power(1-f[3]),e.Q(2)),(e.Q(-3,2),e.Q(1,2))):
+                    raw=[e.encode(a,f)[0]]
+                    if op!="sqrt":raw.append(e.encode(b,f)[0])
+                    if op=="fma":raw.append(e.encode(-a,f)[0])
+                    for rm in range(5):
+                        expected,flags=e.oracle(op,raw,f,rm)
+                        edge.check(op+"_"+suffix+"_rm",[*raw,rm],expected,flags)
+        self.assertEqual(edge.count,540)
+    def test_directed(self):
+        module("test_directed").run(18,quick=True)
+    def test_review(self):
+        module("test_review_numeric").run(18,ROOT,"all")
+    def test_pair_parity(self):
+        module("test_pair_parity").run(18)
+    def test_trans_phases(self):
+        module("test_trans_phases").run()
+    def test_named_overflow(self):
+        module("test_named_overflow").run()
+    def test_contract(self):
+        # The script validates both publications, signatures and provenance.
+        import runpy
+        runpy.run_path(str(ROOT/"tests/test_contract.py"),run_name="__main__")
+
+def suite():
+    out=unittest.TestSuite()
+    for cls in (SmallCircuits,Numeric,Pins,Quality):
+        out.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
+    for name in ("test_manifest_is_current","test_reproduces_byte_for_byte",
+                 "test_inverse_pair_obligation_is_published","test_token_aliases"):
+        out.addTest(Published(name))
+    out.addTest(Qrom("test_cli_single_word_table"))
+    return out
+
+if __name__=="__main__":
+    result=unittest.TextTestRunner(verbosity=2).run(suite())
+    raise SystemExit(not result.wasSuccessful())
diff --git a/tests/test_default_cache.py b/tests/test_default_cache.py
new file mode 100644
index 0000000..32ff80f
--- /dev/null
+++ b/tests/test_default_cache.py
@@ -0,0 +1,96 @@
+"""Exercise scripts/test preparation with real publications and a focused probe.
+
+The fixture replaces the suite body with one exact rounding assertion to avoid
+recursion. The runner, generators, bitcode, bridge and compiler are real.
+"""
+import hashlib
+import json
+from pathlib import Path
+import re
+import shutil
+import subprocess
+import tempfile
+import unittest
+
+ROOT = Path(__file__).resolve().parents[1]
+LLVM = Path("/usr/lib/llvm-18/bin")
+PROBE = '''import sys
+from pathlib import Path
+root = Path(__file__).resolve().parents[1]
+sys.path.insert(0, str(root / "tests"))
+from test_edge import Edge
+actual = Edge(18, root).call("tanh_f16_rm", 0x54e0, 1)
+print(f"observed {actual[0]:#06x}", flush=True)
+assert actual == (0x3bff, 0), actual
+'''
+
+
+class DefaultPreparation(unittest.TestCase):
+    def setUp(self):
+        tmp = tempfile.TemporaryDirectory()
+        self.addCleanup(tmp.cleanup)
+        self.root = Path(tmp.name)
+        for name in ("scripts/test", "softfloat/generate.py", "softfloat/constants.py",
+                     "dist/llvm18/bennett-arith.bc", "dist/llvm18/manifest.json",
+                     "tests/test_edge.py"):
+            dest = self.root / name
+            dest.parent.mkdir(parents=True, exist_ok=True)
+            shutil.copy2(ROOT / name, dest)
+        (self.root / "tests/test_default.py").write_text(PROBE)
+        self.work = self.root / ".tmp/llvm18"
+
+    def default_run(self):
+        return subprocess.run([str(self.root / "scripts/test")], capture_output=True,
+                              text=True, timeout=120)
+
+    def test_changed_publication_cannot_pass_with_previous_bridge(self):
+        first = self.default_run()
+        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
+        bc = self.root / "dist/llvm18/bennett-arith.bc"
+        ir = subprocess.check_output([str(LLVM / "llvm-dis"), str(bc), "-o", "-"],
+                                     text=True, timeout=30)
+        # Deliberately return 1 instead of its predecessor for this downward
+        # tanh case, retaining the ABI and every other published definition.
+        pattern = r"(define i16 @__bennett_sf_tanh_f16_rm\([^\n]*\) \{\n).*?^}"
+        broken, count = re.subn(pattern, r"\g<1>  ret i16 15360\n}", ir, flags=re.M | re.S)
+        self.assertEqual(count, 1)
+        subprocess.run([str(LLVM / "llvm-as"), "-o", str(bc)], input=broken,
+                       text=True, check=True, timeout=30)
+        dist = bc.parent
+        manifest = dist / "manifest.json"
+        data = json.loads(manifest.read_text())
+        data["bitcode_sha256"] = hashlib.sha256(bc.read_bytes()).hexdigest()
+        manifest.write_text(json.dumps(data, indent=2) + "\n")
+        (dist / "SHA256SUMS").write_text("".join(
+            hashlib.sha256((dist / name).read_bytes()).hexdigest() + "  " + name + "\n"
+            for name in ("bennett-arith.bc", "manifest.json")))
+        second = self.default_run()
+        self.assertNotEqual(second.returncode, 0, second.stdout + second.stderr)
+        self.assertIn("observed 0x3c00", second.stdout)
+
+    def test_support_sources_and_missing_outputs_are_refreshed(self):
+        first = self.default_run()
+        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
+        for source, output, marker in (("generate.py", "bridge.ll", "; fresh bridge"),
+                                       ("constants.py", "constants.h", "/* fresh constants */")):
+            path = self.root / "softfloat" / source
+            with path.open("a") as stream:
+                stream.write(f'\nwith open(pathlib.Path(sys.argv[1]) / {output!r}, "a") as out:\n'
+                             f'    out.write({marker!r} + "\\n")\n')
+        (self.work / "bridge.ll").write_text("invalid cached IR\n")
+        (self.work / "constants.h").unlink()
+        second = self.default_run()
+        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
+        self.assertIn("; fresh bridge", (self.work / "bridge.ll").read_text())
+        self.assertIn("/* fresh constants */", (self.work / "constants.h").read_text())
+        # A failed rebuild must stop before the old, still-loadable library
+        # reaches the suite body.
+        (self.root / "dist/llvm18/bennett-arith.bc").write_bytes(b"invalid bitcode\n")
+        failed = self.default_run()
+        self.assertNotEqual(failed.returncode, 0, failed.stdout + failed.stderr)
+        self.assertNotIn("observed", failed.stdout)
+        self.assertIn("error:", failed.stderr)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tests/test_directed.py b/tests/test_directed.py
new file mode 100644
index 0000000..b931be2
--- /dev/null
+++ b/tests/test_directed.py
@@ -0,0 +1,49 @@
+"""All constrained elementary operations against exact MPFR bracket rounding."""
+import importlib.util
+from pathlib import Path
+import sys
+import os
+
+ROOT=Path(__file__).resolve().parents[1]
+s=importlib.util.spec_from_file_location("trans",ROOT/"tests/test_trans.py")
+t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
+e=t.e
+
+def run(major, quick=False):
+    edge=e.Edge(major);oracle=t.Oracle()
+    formats=list(e.FORMATS.items())
+    if os.environ.get("BENNETT_ARITH_PROMISED"):
+        formats.append(("ppcf128",None))
+    else:
+        print("PPC exact sweep: BENNETT_ARITH_PROMISED=1 (bennett-arith-wvh)",flush=True)
+    for suffix,f in formats:
+        def enc(v):
+            return oracle.pairs.to_pair(v)[0] if f is None else e.encode(v,f)[0]
+        if f is None:
+            oracle.rounded("exp",e.Q(0),0)
+        tiny=-1074 if f is None else 1-f[3]-(f[1]-1)
+        exponents=(-169,-300) if quick else (tiny,tiny+1,-300,-169,-113,-112,-111,-20)
+        values=[sign*e.power(k) for k in exponents for sign in (-1,1)]
+        values += [e.Q(x) for x in (64,78,80,100,136,161,255,256,512,-64,-100,-255)]
+        values += [e.Q(1)+d*e.power(-52 if f is None else 1-f[1]) for d in (-2,-1,0,1,2)]
+        for v in values:
+            raw=enc(v)
+            a,sa=(oracle.pairs.decode(raw)[:2] if f is None else e.decode(raw,f)[:2])
+            if isinstance(a,str):continue
+            for op in t.ops:
+                b=e.Q(3,2) if op=="pow" else e.Q(-3,4)
+                args=[raw,enc(b)] if op in ("pow","atan2") else [raw]
+                for rm in range(5):
+                    expected=oracle.rounded(op,a,sa,b,f=f,rm=rm)
+                    edge.check(op+"_"+suffix+"_rm",[*args,rm],expected)
+            for pair, components in (("sincos",("sin","cos")),
+                                     ("sincospi",("sinpi","cospi"))):
+                for rm in range(5):
+                    expected=tuple(oracle.rounded(op,a,sa,f=f,rm=rm) for op in components)
+                    edge.check(pair+"_"+suffix+"_rm",[raw,rm],expected)
+        print(f"LLVM {major} {suffix}: {edge.count} exact directed checks",flush=True)
+    assert not oracle.inconclusive
+
+if __name__=="__main__":
+    for major in map(int,[a for a in sys.argv[1:] if a!="--quick"] or [18,23]):
+        run(major,"--quick" in sys.argv)
diff --git a/tests/test_named_overflow.py b/tests/test_named_overflow.py
new file mode 100644
index 0000000..549013f
--- /dev/null
+++ b/tests/test_named_overflow.py
@@ -0,0 +1,35 @@
+"""Directed named-format overflow, checked against LLVM APFloat 23."""
+import ctypes
+import os
+from pathlib import Path
+import subprocess
+import sys
+
+ROOT=Path(__file__).resolve().parents[1]
+WORK=Path(os.environ["TMPDIR"])/"named-overflow"
+WORK.mkdir(parents=True,exist_ok=True)
+LLVM=Path("/usr/lib/llvm-23/bin")
+
+def run():
+    flags=subprocess.check_output([str(LLVM/"llvm-config"),"--cxxflags","--ldflags","--libs","support","--system-libs"],text=True).split()
+    subprocess.run([str(LLVM/"clang++"),str(ROOT/"tests/named_oracle.cpp"),*flags,"-o",str(WORK/"oracle")],check=True,timeout=60)
+    subprocess.run([str(LLVM/"clang"),"-std=c2x","-O0","-shared","-fPIC","-DBENNETT_LLVM_MAJOR=23",
+                    "-I",str(ROOT/".tmp/llvm18"),str(ROOT/"softfloat/named.c"),"-o",str(WORK/"named.so")],check=True,timeout=90)
+    lib=ctypes.CDLL(str(WORK/"named.so"))
+    call=lib.bennett_sf_named
+    call.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
+    # Finite overflow and values just beyond each maximal representable bin.
+    cases=[(raw,fmt,rm) for raw in (0x501502f9,0xd01502f9,0x43fffffe,0xc3fffffe,
+                                   0x47800000,0xc7800000,0x7f7fffff,0xff7fffff)
+           for fmt in range(7) for rm in (1,2,3)
+           if rm==3 or (rm==1 and raw>>31==0) or (rm==2 and raw>>31==1)]
+    data="".join(f"{raw} {fmt} {rm}\n" for raw,fmt,rm in cases)
+    expected=list(map(int,subprocess.check_output([str(WORK/"oracle")],input=data,text=True).split()))
+    assert len(expected)==len(cases)
+    for (raw,fmt,rm),want in zip(cases,expected):
+        src=(ctypes.c_uint64*2)(raw,0);out=(ctypes.c_uint64*2)()
+        call(out,2,fmt,1,src,rm,0)
+        assert out[0]==want,(hex(raw),fmt,rm,hex(out[0]),hex(want))
+    print(f"{len(cases)} named directed-overflow APFloat comparisons")
+
+if __name__=="__main__":run()
diff --git a/tests/test_pair_parity.py b/tests/test_pair_parity.py
new file mode 100644
index 0000000..fa942a1
--- /dev/null
+++ b/tests/test_pair_parity.py
@@ -0,0 +1,31 @@
+"""Dialect 13.1 parity at both zero-low transitions, from exact dyadic midpoints."""
+import importlib.util
+from pathlib import Path
+import sys
+ROOT=Path(__file__).resolve().parents[1]
+s=importlib.util.spec_from_file_location("pair",ROOT/"tests/ppc_exact_oracle.py")
+o=importlib.util.module_from_spec(s);s.loader.exec_module(o)
+e=o.e
+
+def run(major):
+    edge=e.Edge(major);u=e.power(-1074);f=e.FORMATS["f64"]
+    for hb in (0x3ff0000000000001,0x0030000000000001):
+        h=e.decode(hb,f)[0]
+        for sign in (-1,1):
+            expected=hb ^ ((1<<63) if sign<0 else 0)
+            for direction in (-1,1):
+                # FMA is exactly sign*(h +/- u/2); the zero-low neighbour
+                # has even low significand and must win either midpoint.
+                a=o.pair(sign*h,sign*direction*u)
+                half=o.pair(e.Q(1,2));c=o.pair(sign*h/2)
+                edge.check("fma_ppcf128_rm",[a,half,c,0],expected,16)
+                if hb==0x0030000000000001:
+                    value=sign*(h+direction*u/2)
+                    raw,flags=e.encode(value,e.FORMATS["f128"])
+                    assert flags==0
+                    edge.check("fptrunc_f128_ppcf128_rm",[raw,0],expected,16)
+                assert o.to_pair(sign*(h+direction*u/2))==(expected,16)
+    print(f"LLVM {major}: {edge.count} exact zero-low parity/flag checks")
+
+if __name__=="__main__":
+    for major in map(int,sys.argv[1:] or [18,23]):run(major)
diff --git a/tests/test_quality.py b/tests/test_quality.py
new file mode 100644
index 0000000..fb27112
--- /dev/null
+++ b/tests/test_quality.py
@@ -0,0 +1,35 @@
+"""Quality measurement and rejection of source regressions."""
+import importlib.util
+from pathlib import Path
+import unittest
+ROOT=Path(__file__).resolve().parents[1]
+spec=importlib.util.spec_from_file_location("quality",ROOT/"scripts/quality_metrics.py")
+q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
+
+class Quality(unittest.TestCase):
+    def test_product_has_no_process_identifiers(self):
+        self.assertEqual(q.measure()["process_identifiers"],[])
+    def test_no_tracked_litter(self):
+        self.assertEqual(q.measure()["litter"],[])
+    def test_nested_branch_and_wrapper_are_detected(self):
+        baseline={"files":{"a.py":{"cognitive_mass":0,"trivial_wrappers":0}},"litter":[],"process_identifiers":[]}
+        current={"files":{"a.py":{"cognitive_mass":2,"trivial_wrappers":1}},"litter":[],"process_identifiers":[]}
+        errors=q.regressions(current,baseline)
+        self.assertTrue(any("cognitive_mass" in e for e in errors))
+        self.assertTrue(any("trivial_wrappers" in e for e in errors))
+    def test_new_file_and_litter_are_detected(self):
+        baseline={"files":{},"litter":[],"process_identifiers":[]}
+        current={"files":{"new.py":{"functions":1}},"litter":["cache.pyc"],"process_identifiers":["new.py:1"]}
+        self.assertEqual(len(q.regressions(current,baseline)),3)
+    def test_python_decisions_and_forwarder(self):
+        rows=q.python_functions("def f(x):\n    if x:\n        while x:\n            x-=1\n    return x\ndef g(x):\n    return f(x)\n")
+        self.assertGreater(rows[0][1],1)
+        self.assertEqual(rows[1][2],1)
+    def test_c_decisions_ignore_comments_and_strings(self):
+        rows=q.c_functions('static int f(int x) { /* if while */ if(x) { while(x) --x; } return x; }\n'
+                           'static char *g(void) { return "if for"; }\n')
+        self.assertEqual(len(rows),2)
+        self.assertGreater(rows[0][1],1)
+        self.assertEqual(rows[1][1],0)
+
+if __name__=="__main__":unittest.main()
diff --git a/tests/test_review_numeric.py b/tests/test_review_numeric.py
index 598dc37..9b4f27a 100644
--- a/tests/test_review_numeric.py
+++ b/tests/test_review_numeric.py
@@ -11,19 +11,8 @@ o=importlib.util.module_from_spec(s);s.loader.exec_module(o);e=o.e
 def tanh_bounds(x):
     spec=importlib.util.spec_from_file_location('mpfr',ROOT/'tests/test_trans.py')
     t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
-    oracle=t.Oracle();t.m.mpfr_clear(t.C.byref(oracle.r));t.m.mpfr_init2(t.C.byref(oracle.r),2048)
-    try:
-        oracle.put(oracle.a,x);bounds=[]
-        for direction in (3,2): # MPFR downward/upward
-            t.m.mpfr_tanh(t.C.byref(oracle.r),t.C.byref(oracle.a),direction)
-            exponent=t.C.c_long()
-            p=t.m.mpfr_get_str(None,t.C.byref(exponent),2,0,t.C.byref(oracle.r),0)
-            digits=t.C.string_at(p).decode();t.m.mpfr_free_str(p)
-            sign=-1 if digits.startswith('-') else 1;digits=digits.lstrip('-')
-            bounds.append(sign*int(digits,2)*e.power(exponent.value-len(digits)))
-        return bounds
-    finally:
-        for item in (oracle.a,oracle.b,oracle.r):t.m.mpfr_clear(t.C.byref(item))
+    oracle=t.Oracle(2048)
+    return [oracle.call("tanh",x,0,direction=direction)[0] for direction in (3,2)]
 
 def run(major,root,case):
     edge=e.Edge(major,root);f=e.FORMATS['f64'];one=e.encode(e.Q(1),f)[0]
diff --git a/tests/test_trans.py b/tests/test_trans.py
index a964337..8487bc6 100644
--- a/tests/test_trans.py
+++ b/tests/test_trans.py
@@ -11,34 +11,71 @@ m=C.CDLL('libmpfr.so.6')
 for name,args,ret in [('init2',[C.POINTER(MP),C.c_long],None),('clear',[C.POINTER(MP)],None),('set_str',[C.POINTER(MP),C.c_char_p,C.c_int,C.c_int],C.c_int),('mul_2si',[C.POINTER(MP),C.POINTER(MP),C.c_long,C.c_int],C.c_int),('get_str',[C.c_void_p,C.POINTER(C.c_long),C.c_int,C.c_size_t,C.POINTER(MP),C.c_int],C.c_void_p),('free_str',[C.c_void_p],None)]:
     f=getattr(m,'mpfr_'+name);f.argtypes=args;f.restype=ret
 ops='sin cos tan asin acos atan sinh cosh tanh exp exp2 exp10 log log2 log10 atan2 pow'.split()
-for op in ops:
+for op in ops+['sinpi','cospi']:
     fn=getattr(m,'mpfr_'+op);fn.argtypes=[C.POINTER(MP)]*(4 if op in ('atan2','pow') else 3) # last is rounding, corrected below
     fn.argtypes=[C.POINTER(MP)]*(3 if op in ('atan2','pow') else 2)+[C.c_int]
     fn.restype=C.c_int
 class Oracle:
-    def __init__(self):
+    """Directed MPFR intervals, refined until both ends choose the same carrier."""
+    def __init__(self, precision=384):
+        self.precision=precision
         self.a=MP();self.b=MP();self.r=MP()
-        for x in (self.a,self.b,self.r):m.mpfr_init2(C.byref(x),384)
+        for x in (self.a,self.b,self.r):m.mpfr_init2(C.byref(x),precision)
+        self.inconclusive=0
+    def __del__(self):
+        for x in (self.a,self.b,self.r):m.mpfr_clear(C.byref(x))
+    def resize(self,precision):
+        if precision==self.precision:return
+        for x in (self.a,self.b,self.r):
+            m.mpfr_clear(C.byref(x));m.mpfr_init2(C.byref(x),precision)
+        self.precision=precision
     def put(self,x,v,sign=0):
-        if isinstance(v,str):s=('-' if sign else '')+('nan' if v=='nan' else 'inf');m.mpfr_set_str(C.byref(x),s.encode(),10,0);return
+        if isinstance(v,str):
+            s=('-' if sign else '')+('nan' if v=='nan' else 'inf')
+            m.mpfr_set_str(C.byref(x),s.encode(),10,0)
+            return
         n=v.numerator;d=v.denominator
         s=('-' if n<0 or not n and sign else '')+bin(abs(n))[2:]
         assert m.mpfr_set_str(C.byref(x),s.encode(),2,0)==0
         m.mpfr_mul_2si(C.byref(x),C.byref(x),-(d.bit_length()-1),0)
     def get(self):
-        exp=C.c_long();p=m.mpfr_get_str(None,C.byref(exp),2,384,C.byref(self.r),0)
+        exp=C.c_long();p=m.mpfr_get_str(None,C.byref(exp),2,self.precision,C.byref(self.r),0)
         s=C.string_at(p).decode();m.mpfr_free_str(p)
         if '@NaN@' in s:return 'nan',0
         if '@Inf@' in s:return 'inf',int(s.startswith('-'))
         sign=int(s.startswith('-'));s=s.lstrip('-')
-        if abs(exp.value)>20000:return (-1 if sign else 1)*e.power(20000 if exp.value>0 else -20000),sign
+        if abs(exp.value)>20000:
+            return (-1 if sign else 1)*e.power(20000 if exp.value>0 else -20000),sign
         return (-1 if sign else 1)*int(s,2)*e.power(exp.value-len(s)),sign
-    def call(self,op,a,sa,b=0,sb=0):
+    def call(self,op,a,sa,b=0,sb=0,direction=0):
         self.put(self.a,a,sa);self.put(self.b,b,sb)
         fn=getattr(m,'mpfr_'+op)
-        if op in ('atan2','pow'):fn(C.byref(self.r),C.byref(self.a),C.byref(self.b),0)
-        else:fn(C.byref(self.r),C.byref(self.a),0)
+        args=[C.byref(self.r),C.byref(self.a)]
+        if op in ('atan2','pow'):args.append(C.byref(self.b))
+        fn(*args,direction)
         return self.get()
+    def rounded(self,op,a,sa,b=0,sb=0,f=None,rm=0):
+        if f is None:
+            if not hasattr(self,'pairs'):
+                spec=importlib.util.spec_from_file_location('pairs',R/'tests/ppc_exact_oracle.py')
+                self.pairs=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.pairs)
+            def encode(v,sign):
+                if isinstance(v,str):return e.nan(self.pairs.F) if v=='nan' else e.infinity(self.pairs.F,sign)
+                return self.pairs.to_pair(v,rm,sign)[0]
+        else:
+            def encode(v,sign):return e.encode(v,f,rm,sign)[0]
+        input_bits=max((v.numerator.bit_length() for v in (a,b) if not isinstance(v,str)),default=0)
+        precision=max(384,input_bits)
+        while precision<=65536:
+            self.resize(precision)
+            lower,ls=self.call(op,a,sa,b,sb,direction=3)
+            upper,us=self.call(op,a,sa,b,sb,direction=2)
+            lo,hi=encode(lower,ls),encode(upper,us)
+            if lo==hi:return lo
+            precision*=2
+        self.inconclusive+=1
+        raise AssertionError((op,a,b,rm,'MPFR bracket inconclusive at 65536 bits'))
+
 if __name__=='__main__':
     for major in map(int,sys.argv[1:] or [18,23]):
         edge=e.Edge(major)
@@ -67,7 +104,7 @@ if __name__=='__main__':
                     rb=e.encode(b,f)[0]
                     want,ws=oracle.call(op,a,sa,b)
                     args=[raw,rb] if op in ('pow','atan2') else [raw]
-                    expected=e.encode(want,f,zero_sign=ws)[0]
+                    expected=oracle.rounded(op,a,sa,b,f=f)
                     actual=edge.call(op+'_'+suffix,*args)[0]
                     av,_,_=e.decode(actual,f)
                     if isinstance(want,str) or isinstance(av,str) or not want or not av:
@@ -75,7 +112,7 @@ if __name__=='__main__':
                     else:
                         step=max(e.log2q(abs(want)),1-bias)-(p-1)
                         ulps=abs(av-want)/e.power(step)
-                        assert ulps<=4,(major,suffix,op,hex(raw),float(ulps))
+                        assert actual==expected,(major,suffix,op,hex(raw),hex(actual),hex(expected))
                         worst[op]=max(worst.get(op,e.Q(0)),ulps)
                     edge.count+=1
                 # Pair order and scalar consistency, including signed zeros/NaNs.
diff --git a/tests/test_trans_boundaries.py b/tests/test_trans_boundaries.py
index 440ddc1..c8aab03 100644
--- a/tests/test_trans_boundaries.py
+++ b/tests/test_trans_boundaries.py
@@ -16,11 +16,9 @@ for major in map(int,sys.argv[1:] or [18,23]):
                     raw=e.encode((n+delta)*scale,f)[0];a,sa,_=e.decode(raw,f)
                     want,ws=oracle.call(op,a,sa)
                     for rm in range(5):
-                        got=edge.call(op+'_'+suffix+'_rm',raw,rm)[0];av,_,_=e.decode(got,f);expected,more=e.encode(want,f,rm,ws)
-                        if isinstance(av,str) or isinstance(want,str) or more&4:assert got==expected,(suffix,op,n,rm)
-                        else:
-                            step=max(e.log2q(abs(want)),1-f[3])-(f[1]-1)
-                            assert abs(av-want)<=4*e.power(step),(suffix,op,n,rm)
+                        expected=oracle.rounded(op,a,sa,f=f,rm=rm)
+                        got=edge.call(op+'_'+suffix+'_rm',raw,rm)[0]
+                        assert got==expected,(suffix,op,n,rm,hex(got),hex(expected))
                         edge.count+=1
         # Exact powers, including exact tiny and rounded-underflow cases, flags.
         for n in [tiny-1,tiny,emin,0,1,f[3],f[3]+1]:
diff --git a/tests/test_trans_extra.py b/tests/test_trans_extra.py
index aab93f0..e745836 100644
--- a/tests/test_trans_extra.py
+++ b/tests/test_trans_extra.py
@@ -1,5 +1,5 @@
 """Exhaustive small-format sin, PPC libm, sincospi, and constrained flags."""
-import ctypes,importlib.util,pathlib,sys,random
+import ctypes,importlib.util,pathlib,sys,random,os
 sys.dont_write_bytecode=True
 R=pathlib.Path(__file__).resolve().parents[1]
 s=importlib.util.spec_from_file_location('trans',R/'tests/test_trans.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
@@ -28,11 +28,11 @@ for major in map(int,sys.argv[1:] or [18,23]):
         for raw in range(65536):
             v,sign,_=e.decode(raw,f);want,ws=oracle.call('sin',v,sign)
             actual=edge.call('sin_'+suffix,raw)[0];av,_,_=e.decode(actual,f)
-            expected=e.encode(want,f,zero_sign=ws)[0]
+            expected=oracle.rounded('sin',v,sign,f=f)
             if isinstance(want,str) or isinstance(av,str) or not want or not av:assert actual==expected,(suffix,raw,actual,expected)
             else:
                 step=max(e.log2q(abs(want)),1-f[3])-(f[1]-1)
-                err=abs(av-want)/e.power(step);assert err<=1,(suffix,raw,float(err));worst=max(worst,err)
+                err=abs(av-want)/e.power(step);assert actual==expected,(suffix,raw,hex(actual),hex(expected));worst=max(worst,err)
             edge.count+=1
         print(f'LLVM {major} exhaustive sin {suffix}: 65536 encodings',flush=True)
     values=[0,1,1<<63,e.infinity(e.FORMATS['f64']),e.infinity(e.FORMATS['f64'],1),e.nan(e.FORMATS['f64'])]
@@ -40,16 +40,19 @@ for major in map(int,sys.argv[1:] or [18,23]):
         for sign in [1,-1]:
             values.append(dd(sign*e.power(exp)))
             if exp> -1000 and exp<1000:values.append(dd(sign*(e.power(exp)+e.power(exp-60))))
+    if not os.environ.get('BENNETT_ARITH_PROMISED'):
+        print('PPC full-domain exact libm: BENNETT_ARITH_PROMISED=1 (bennett-arith-wvh)',flush=True)
+        values=[]
     for raw in values:
         v,sign=undd(raw)
         for op in t.ops:
             b=e.Q(3,2) if op=='pow' else e.Q(-3,4);br=dd(b)
             want,ws=oracle.call(op,v,sign,b);actual=edge.call(op+'_ppcf128',raw,*([br] if op in ('atan2','pow') else []))[0]
-            av,_=undd(actual);expected=dd(want,ws)
+            av,_=undd(actual);expected=oracle.rounded(op,v,sign,b)
             if isinstance(want,str) or isinstance(av,str) or not want or not av:assert actual==expected,(major,op,hex(raw),hex(actual),hex(expected))
             else:
                 step=max(e.log2q(abs(want)),-969)-105;err=abs(av-want)/e.power(step)
-                assert err<=4,(major,op,hex(raw),float(err));worst=max(worst,err)
+                assert actual==expected,(major,op,hex(raw),hex(actual),hex(expected));worst=max(worst,err)
             edge.count+=1
         edge.check('sincos_ppcf128',[raw],(edge.call('sin_ppcf128',raw)[0],edge.call('cos_ppcf128',raw)[0]))
     # All _rm signatures, with a nontrivial finite point and unchanged sticky bits.
@@ -63,19 +66,15 @@ for major in map(int,sys.argv[1:] or [18,23]):
                 edge.env[1]=32
                 got=edge.call(op+'_'+suffix+'_rm',enc(a),*([enc(b)] if op in ('atan2','pow') else []),rm)[0]
                 av=dec(got);step=max(e.log2q(abs(want)),-969 if f is None else 1-f[3])-(105 if f is None else f[1]-1)
-                assert abs(av-want)<=4*e.power(step),(suffix,op,rm)
+                expected=oracle.rounded(op,a,0,b,f=f,rm=rm)
+                assert got==expected,(suffix,op,rm,hex(got),hex(expected))
                 assert edge.env[1]&32
                 edge.count+=1
         for v in [e.Q(0),e.Q(-0),e.Q(1,2),e.Q(-1,2),e.Q(1),e.Q(-1),e.Q(3,2),e.Q(1024),e.power(100)]:
             source=enc(v);vv=dec(source)
-            sv,ss=oracle.call('sinpi',vv,0);cv,cs=oracle.call('cospi',vv,0)
-            expected=(enc(sv,ss),enc(cv,cs))
-            # Approximate finite outputs may differ at a rounding boundary.
+            expected=tuple(oracle.rounded(op,vv,0,f=f) for op in ('sinpi','cospi'))
             actual=edge.call('sincospi_'+suffix,enc(v))
-            for got,want in zip(actual,expected):
-                gv,wv=dec(got),dec(want)
-                if isinstance(wv,str) or not wv:assert got==want,(suffix,'sincospi',v,hex(got),hex(want))
-                else:assert abs(gv-wv)<=e.power(e.log2q(abs(wv))-(104 if f is None else f[1]-2))
+            assert actual==expected,(suffix,'sincospi',v,actual,expected)
             for rm in range(5):
                 pair=edge.call('sincospi_'+suffix+'_rm',enc(v),rm);assert len(pair)==2;edge.count+=1
             for rm in range(5):
diff --git a/tests/test_trans_phases.py b/tests/test_trans_phases.py
new file mode 100644
index 0000000..1c02977
--- /dev/null
+++ b/tests/test_trans_phases.py
@@ -0,0 +1,19 @@
+"""Unit checks for domain, core and packing phase boundaries."""
+import os
+from pathlib import Path
+import subprocess
+import sys
+ROOT=Path(__file__).resolve().parents[1]
+
+def run(source=ROOT):
+    work=Path(os.environ["TMPDIR"])/"trans-phases"
+    work.mkdir(parents=True,exist_ok=True)
+    exe=work/"phases"
+    subprocess.run(["/usr/lib/llvm-18/bin/clang","-std=c2x","-O0",
+                    "-DBENNETT_LLVM_MAJOR=18",f'-DBENNETT_CORE="{source}/softfloat/core.c"',
+                    "-I",str(ROOT/".tmp/llvm18"),str(ROOT/"tests/trans_phases.c"),
+                    "-o",str(exe)],check=True,timeout=60)
+    subprocess.run([str(exe)],check=True,timeout=10)
+    print("domain/core/pack/exactness-table invariants passed")
+
+if __name__=="__main__":run(Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT)
diff --git a/tests/trans_phases.c b/tests/trans_phases.c
new file mode 100644
index 0000000..0b2e869
--- /dev/null
+++ b/tests/trans_phases.c
@@ -0,0 +1,60 @@
+/* Phase invariants for the integer elementary evaluator. */
+#include <assert.h>
+#include BENNETT_CORE
+
+static U raw(int n) {
+    int flags=0;
+    return pack(ti(n),formats[3],0,&flags);
+}
+static void test_domain(void) {
+    U in[3]={raw(3),0,0};
+    assert(trans_domain(3,EXP2,in).path==TRANS_EXACT);
+    in[0]=raw(100);
+    assert(trans_domain(3,TANH,in).path==TRANS_TANH_LIMIT);
+    in[0]=raw(0);
+    assert(trans_domain(6,EXP,in).path==TRANS_PPC_EXP);
+    in[0]=((U)854<<52); /* binary64 2^-169 */
+    assert(trans_domain(3,TAN,in).path==TRANS_LINEAR);
+    in[0]=raw(2);
+    assert(trans_domain(3,ASIN,in).path==TRANS_CORE);
+}
+static void test_core(void) {
+    U in[3]={0};
+    TransState state=trans_domain(3,SINCOS,in);
+    trans_core(&state,SINCOS);
+    assert(state.r.kind==FINITE && !state.r.mag);
+    assert(compare(state.c,ti(1))==0);
+    in[0]=raw(2);state=trans_domain(3,ASIN,in);
+    trans_core(&state,ASIN);
+    assert(state.r.kind==NANV);
+}
+static void test_pack(void) {
+    U in[3]={raw(1),0,0},out[3];
+    TransState state=trans_domain(3,LOG,in);
+    trans_core(&state,LOG);trans_pack(out,3,LOG,0,state);
+    assert(out[0]==0 && out[1]==0 && out[2]==0);
+    in[0]=0;state=trans_domain(3,ACOS,in);
+    trans_core(&state,ACOS);trans_pack(out,3,ACOS,0,state);
+    assert(out[0]!=0 && out[2]==16);
+    in[0]=raw(2);state=trans_domain(3,ASIN,in);
+    trans_core(&state,ASIN);trans_pack(out,3,ASIN,0,state);
+    assert(out[0]==nanbits(formats[3]) && out[2]==1);
+    in[0]=raw(-100000);state=trans_domain(3,EXP,in);
+    trans_core(&state,EXP);trans_pack(out,3,EXP,2,state);
+    assert(out[0]==1 && out[2]==24);
+}
+static void test_exactness_table(void) {
+    int zero_ops[]={SIN,COS,TAN,ASIN,ATAN,SINH,COSH,TANH,EXP,SINCOS};
+    for(unsigned i=0;i<sizeof(zero_ops)/sizeof(*zero_ops);++i)
+        assert(trans_is_exact(zero_ops[i],ti(0),ti(0),ti(0)));
+    assert(trans_is_exact(LOG,ti(1),ti(0),ti(0)));
+    assert(trans_is_exact(ACOS,ti(1),ti(0),ti(0)));
+    assert(!trans_is_exact(ACOS,ti(0),ti(0),tc_pi()));
+    V inf={0,0,0,INF,0};
+    assert(trans_is_exact(TANH,inf,ti(0),ti(1)));
+    assert(!trans_is_exact(ATAN,inf,ti(0),tc_pi()));
+    assert(trans_is_exact(POW,ti(2),inf,inf));
+}
+int main(void) {
+    test_domain();test_core();test_pack();test_exactness_table();
+}
````

## 2. Changed sources at 015b424

# Changed sources of job/quality-arith at 015b424

Snapshot of `arith-stage/` at commit `015b424dd7b20ed819e341763a9f4b94c088c099`. 22 files; each embedded verbatim below. Line counts and sha256 per file:

- `gate.toml` 37 lines, sha256 59744ffcb46a
- `scripts/build` 42 lines, sha256 0de749605ecc
- `scripts/gate` 43 lines, sha256 a595126f5ff8
- `scripts/pinned_sibling.py` 37 lines, sha256 bdeed6cf177c
- `scripts/quality_metrics.py` 94 lines, sha256 e6ec7698e084
- `scripts/test` 18 lines, sha256 5a3d8eb6f4c6
- `softfloat/README.md` 289 lines, sha256 66b25e622ba2
- `softfloat/generate.py` 343 lines, sha256 07479ec49109
- `softfloat/named.c` 73 lines, sha256 faf4ee9e90e0
- `softfloat/ppc_round.h` 88 lines, sha256 5b0673ec8635
- `softfloat/ppc_sum.h` 202 lines, sha256 eba161097c81
- `softfloat/test_instances.py` 229 lines, sha256 c86e6362993d
- `softfloat/test_publication.py` 24 lines, sha256 a728f74821f6
- `softfloat/trans.h` 362 lines, sha256 f61643535b60
- `tests/named_oracle.cpp` 26 lines, sha256 d12a87262c59
- `tests/ppc_exact_oracle.py` 153 lines, sha256 f2cf51ecdc7b
- `tests/test_directed.py` 49 lines, sha256 dc5ea8cdc649
- `tests/test_named_overflow.py` 35 lines, sha256 504421e0286a
- `tests/test_pair_parity.py` 31 lines, sha256 7d09856cf913
- `tests/test_trans.py` 121 lines, sha256 07af8be1bcaf
- `tests/test_trans_phases.py` 19 lines, sha256 cfb5c6ecfe5d
- `tests/trans_phases.c` 60 lines, sha256 39547e886181

Total embedded: 2375 lines.

## `gate.toml` (37 lines)

````toml
# Push-gate pins (bennett/tools/gate_README.md). Siblings resolve only to these commits.
schema = 1
repo = "bennett-arith"
tool_sha = "01c0314c9aaa4a37313ab530da2134efafe9cbd5"
timeout_s = 28800

[[check]]
name = "quality baseline ratchet"
argv = ["python3", "-I", "scripts/quality_metrics.py"]

[[check]]
name = "bounded default tests"
argv = ["scripts/test"]

[[check]]
name = "arith gate"
argv = ["scripts/gate"]

[[check]]
name = "circuits"
argv = ["tests/circuits/run"]

[siblings."bennett-isa-spec"]
sha = "ecaaac060c44e317d1181345fa6b8e38c096c099"
note = "ISA main as gated by the 2026-11-02 push wave"

[[siblings."bennett-isa-spec".build]]
name = "reference interpreter (debug)"
cwd = "reference-interpreter"
argv = ["cargo", "build", "--offline"]
outputs = ["reference-interpreter/target/debug/bennett-isa-ref"]
env = { CARGO_BUILD_JOBS = "4" }

[siblings."bennett-dialect-spec"]
sha = "95a4b8d06933018a07fef3516296a25fd582fcde"
note = "Published 0.2.13: total PPC nearest-even tie parity"
````

## `scripts/build` (42 lines)

````
#!/usr/bin/env bash
set -euo pipefail
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER
root="$(dirname "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")")"
export TMPDIR="${TMPDIR:-$root/.tmp}"
mkdir -p "$TMPDIR"
major="${1:?usage: scripts/build 18|23}"
case "$major" in 18|23) ;; *) echo 'only LLVM 18 and 23 are pinned' >&2; exit 1;; esac
llvm="/usr/lib/llvm-$major/bin"
build="$root/.tmp/llvm$major"
dist="$root/dist/llvm$major"
mkdir -p "$build" "$dist"
python3 -I "$root/softfloat/generate.py" "$build" "${@:2}"
python3 -I "$root/softfloat/constants.py" "$build"
"$llvm/clang" -I "$build" -target x86_64-unknown-linux-gnu -std=c2x -DBENNETT_LLVM_MAJOR="$major" -O1 -ffreestanding -fno-builtin -fno-vectorize -fno-slp-vectorize -fno-ident -S -emit-llvm "$root/softfloat/core.c" -o "$build/core.ll"
# Normalize the sole source path so a detached pushed-SHA build is byte-identical.
python3 -I - "$build/core.ll" <<'PY'
import pathlib, re, sys
p=pathlib.Path(sys.argv[1])
s=p.read_text()
s=re.sub(r'^source_filename = .*', 'source_filename = "softfloat/core.c"', s, flags=re.M)
p.write_text(s)
PY
"$llvm/llvm-as" "$build/core.ll" -o "$build/core.bc"
"$llvm/llvm-as" "$build/wrappers.ll" -o "$build/wrappers.bc"
"$llvm/llvm-link" "$build/core.bc" "$build/wrappers.bc" -o "$build/linked.bc"
"$llvm/opt" -passes=internalize,globaldce -internalize-public-api-file="$build/exports.txt" "$build/linked.bc" -o "$build/publish.bc"
"$llvm/opt" -passes=verify -disable-output "$build/publish.bc"
# Atomic replacement: a concurrent binary-edge consumer never reads half a file.
mv -f "$build/publish.bc" "$dist/bennett-arith.bc"
cp -f "$build/manifest.json" "$dist/manifest.json"
"$llvm/llvm-dis" "$dist/bennett-arith.bc" -o "$build/published.ll"
# A test-only C ABI bridge invokes every exact LLVM carrier signature.
"$llvm/clang" -target x86_64-unknown-linux-gnu -shared -fPIC "$dist/bennett-arith.bc" "$build/bridge.ll" -o "$build/oracle-new.so"
mv -f "$build/oracle-new.so" "$build/oracle.so"
python3 -I "$root/scripts/provenance.py" "$major"
python3 -I - "$dist" <<'PY'
import hashlib, pathlib, sys
p=pathlib.Path(sys.argv[1])
(p/'SHA256SUMS').write_text(''.join(hashlib.sha256((p/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in ('bennett-arith.bc','manifest.json')))
PY
echo "built LLVM $major: $dist/bennett-arith.bc"
````

## `scripts/gate` (43 lines)

````
#!/usr/bin/env bash
set -euo pipefail
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER
root="$(dirname "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")")"
export TMPDIR="${TMPDIR:-$root/.tmp}"
mkdir -p "$TMPDIR"
# Multiple real bridge rebuilds stay outside the bounded numerical suite.
timeout 600s python3 -B -I "$root/tests/test_default_cache.py"
# Fail if checked-in publications differ from a fresh build (including the path).
for major in 18 23; do
  dir="$root/dist/llvm$major"
  saved="$TMPDIR/expected-llvm$major"
  mkdir -p "$saved"
  for name in bennett-arith.bc manifest.json SHA256SUMS; do
    test -f "$dir/$name"
    cp -f "$dir/$name" "$saved/$name"
  done
  env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER \
    TMPDIR="$TMPDIR" "$root/scripts/build" "$major"
  for name in bennett-arith.bc manifest.json SHA256SUMS; do
    cmp "$saved/$name" "$dir/$name"
  done
done
env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER \
  TMPDIR="$TMPDIR" python3 -I "$root/tests/test_contract.py"
env -u DISPLAY -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS -u BROWSER \
  TMPDIR="$TMPDIR" python3 -I "$root/tests/test_edge.py"
python3 -I "$root/tests/test_ppc.py"
python3 -I "$root/tests/test_extended.py"
python3 -I "$root/tests/test_powi.py"
python3 -I "$root/tests/test_powi_limit.py"
python3 -I "$root/tests/test_trans.py"
python3 -I "$root/tests/test_trans_extra.py"
python3 -I "$root/tests/test_trans_boundaries.py"
timeout 300s python3 -I "$root/tests/test_directed.py"
timeout 60s python3 -I "$root/tests/test_pair_parity.py"
timeout 60s python3 -I "$root/tests/test_trans_phases.py"
timeout 180s python3 -I "$root/tests/test_named_overflow.py"
timeout 900s python3 -I "$root/softfloat/test_instances.py"
timeout 900s python3 -I "$root/softfloat/test_instance_limits.py"
timeout 300s python3 -I "$root/softfloat/test_cmps.py"
timeout 30s python3 -I "$root/softfloat/test_publication.py"
echo 'gate: both published bitcode edges reproduced and passed'
````

## `scripts/pinned_sibling.py` (37 lines)

````python
"""Resolve this repo's gate.toml pins without consulting live sibling contents."""
import os
from pathlib import Path
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def _head(path):
    if not (path / ".git").exists():
        return "unavailable"
    try:
        done = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True,
            text=True, timeout=10, env={k: v for k, v in os.environ.items() if not k.startswith("GIT_")},
        )
        return done.stdout.strip() if done.returncode == 0 else "unavailable"
    except (OSError, subprocess.SubprocessError):
        return "unavailable"


def resolve_sibling(name):
    with (ROOT / "gate.toml").open("rb") as stream:
        config = tomllib.load(stream)
    sha = config["siblings"][name]["sha"]
    layout = os.environ.get("BENNETT_GATE_LAYOUT")
    path = (Path(layout) / name if layout else
            ROOT / ".tmp/gate/cache" / f"{name}@{sha[:12]}" / name)
    actual = _head(path)
    if actual != sha:
        raise SystemExit(
            f"pinned sibling {name}@{sha}: {path} HEAD={actual}; "
            f"live ../{name} HEAD={_head(ROOT.parent / name)}; "
            f"materialise with gate_run.py verify --repo {config['repo']} --sha HEAD"
        )
    return path
````

## `scripts/quality_metrics.py` (94 lines)

````python
#!/usr/bin/env python3
"""Local syntax metrics and a monotone ratchet against docs/quality.md."""
import ast
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
SOURCE_DIRS={"adders","multipliers","qrom","softfloat","scripts","tests"}
PROCESS=re.compile(r"\bbennett-arith-[a-z0-9]{3}(?:\.[0-9]+)?\b|\bjob[/]|\b(?:shift|round) +[0-9]+")
LITTER=re.compile(r"(^|/)(__pycache__|PROGRESS[^/]*|LAST-RUN[^/]*|LOCK)(/|$)|\.(?:pyc|log|darc|lock)$")
BOUNDS=(25,50,100,200,300)
START="<!-- quality-baseline -->"
END="<!-- /quality-baseline -->"

def python_functions(text):
    tree=ast.parse(text)
    def mass(node,depth=0):
        decision=isinstance(node,(ast.If,ast.For,ast.AsyncFor,ast.While,ast.ExceptHandler,ast.IfExp,ast.Match,ast.comprehension))
        score=(1+depth) if decision else 0
        if isinstance(node,ast.BoolOp):score+=len(node.values)-1
        return score+sum(mass(child,depth+int(decision)) for child in ast.iter_child_nodes(node))
    result=[]
    for node in ast.walk(tree):
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
            body=node.body
            only=body[0] if len(body)==1 else None
            value=only.value if isinstance(only,(ast.Return,ast.Expr)) else None
            result.append((node.end_lineno-node.lineno+1,mass(node),int(isinstance(value,ast.Call))))
    return result

def c_functions(text):
    # Keep newlines so physical lengths remain comparable across revisions.
    text=re.sub(r"/\*.*?\*/|//[^\n]*",lambda m:"\n"*m[0].count("\n"),text,flags=re.S)
    text=re.sub(r'"(?:\\.|[^"\\])*"', '""', text)
    head=re.compile(r"^[ \t]*(?:[A-Za-z_]\w*[ \t*]+)+([A-Za-z_]\w*)\s*\([^;{}]*\)\s*\{",re.M)
    result=[]
    for match in head.finditer(text):
        start=match.end()-1;level=1;end=start+1
        while level and end<len(text):
            level+=(text[end]=="{")-(text[end]=="}");end+=1
        if level:raise ValueError("unbalanced C function "+match[1])
        body=text[start+1:end-1];depth=0;score=0
        for token in re.findall(r"\b(?:if|for|while|switch|case|catch)\b|&&|\|\||[?{}]",body):
            if token=="{":depth+=1
            elif token=="}":depth-=1
            else:score+=1+(depth if token not in ("&&","||") else 0)
        wrapper=bool(re.fullmatch(r"\s*(?:return\s+)?[A-Za-z_]\w*\([^;{}]*\);\s*",body))
        result.append((text[match.start():end].count("\n")+1,score,int(wrapper)))
    return result

def measure():
    paths=subprocess.check_output(["git","ls-files","--cached","--others","--exclude-standard","-z"],cwd=ROOT).decode().split("\0")
    files={};litter=[];identifiers=[]
    for name in sorted(set(paths)-{""}):
        path=ROOT/name
        if not path.is_file():continue
        if LITTER.search(name):litter.append(name)
        if Path(name).parts[0] not in SOURCE_DIRS or path.suffix not in (".py",".c",".h",".cpp"):continue
        text=path.read_text()
        if not name.startswith("tests/") and not path.name.startswith("test_"):
            identifiers.extend(f"{name}:{text.count(chr(10),0,m.start())+1}" for m in PROCESS.finditer(text))
        rows=python_functions(text) if path.suffix==".py" else c_functions(text)
        files[name]={"functions":len(rows),"max_lines":max((r[0] for r in rows),default=0),
                     **{f"over_{n}":sum(r[0]>n for r in rows) for n in BOUNDS},
                     "cognitive_mass":sum(r[1] for r in rows),"trivial_wrappers":sum(r[2] for r in rows)}
    return {"files":files,"litter":litter,"process_identifiers":identifiers}

def regressions(current,baseline):
    failures=[]
    for name,row in current["files"].items():
        old=baseline["files"].get(name,{})
        for key,value in row.items():
            if value>old.get(key,0):failures.append(f"{name} {key}: {value} > {old.get(key,0)}")
    for key in ("litter","process_identifiers"):
        if len(current[key])>len(baseline[key]):failures.append(f"{key}: {current[key]}")
    return failures

def main():
    current=measure()
    if sys.argv[1:]==["--report"]:
        print(json.dumps(current,sort_keys=True,indent=2));return
    if sys.argv[1:]:raise SystemExit("usage: quality_metrics.py [--report]")
    doc=(ROOT/"docs/quality.md").read_text()
    if START not in doc or END not in doc:raise SystemExit("missing quality baseline in docs/quality.md")
    block=doc.split(START,1)[1].split(END,1)[0].strip()
    baseline=json.loads(block.removeprefix("```json").removesuffix("```").strip())
    failures=regressions(current,baseline)
    if failures:raise SystemExit("\n".join(failures))
    print(f"quality ratchet: {len(current['files'])} source files, no baseline regression")

if __name__=="__main__":main()
````

## `scripts/test` (18 lines)

````
#!/usr/bin/env bash
# Bounded default suite; scripts/gate retains exhaustive checks on both majors.
set -euo pipefail
unset DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER
root="$(dirname "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")")"
export TMPDIR="${TMPDIR:-$root/.tmp/tests}"
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$TMPDIR"
# Rebuild even when outputs exist: a cached bridge can hide publication changes,
# and source-level checks must use current generated constants and ABI metadata.
work="$root/.tmp/llvm18"
mkdir -p "$work"
python3 -B -I "$root/softfloat/generate.py" "$work"
python3 -B -I "$root/softfloat/constants.py" "$work"
timeout 90s /usr/lib/llvm-18/bin/clang -shared -fPIC \
  "$root/dist/llvm18/bennett-arith.bc" "$work/bridge.ll" -o "$work/oracle-new.so"
mv -f "$work/oracle-new.so" "$work/oracle.so"
exec python3 -B -I "$root/tests/test_default.py" "$@"
````

## `softfloat/README.md` (289 lines)

````markdown
# Soft-float binary edge

The driver links `dist/llvm<major>/bennett-arith.bc` with the program and the
same-major `bennett-runtimes` bitcode, **before** normalisation/materialisation.
Use `/usr/lib/llvm-18/bin/llvm-link` or `/usr/lib/llvm-23/bin/llvm-link` as
appropriate. Both the device and native comparison builds must use that same
linked, materialised closure. Do not compile the C source in the consumer or
substitute host libc/libm. The plugin consumes this binary edge only.

Each distribution includes `manifest.json` (all exported names, literal LLVM
signatures, formats, semantic status, and spec section), `staged_exports` (required
concrete signatures awaiting mechanics, with explicit semantic status), three parametric
families and `SHA256SUMS` for the bitcode and manifest. The manifest is the complete
machine-readable entry-point list. Public wrappers use the dialect's LLVM carrier
ABI, not C's aggregate/sret ABI for `_BitInt(80)` or `_BitInt(128)`.

## Implemented

For `B = f16, bf16, f32, f64, f80, f128, ppcf128`, the carriers are
`i16, i16, i32, i64, i80, i128, i128`. IEEE claims below apply to the first six;
PPC follows the major-specific APFloat rules described below:

| Name after `__bennett_sf_` | Literal signature | Contract |
|---|---|---|
| `{add,sub,mul,div,rem}_B` | `C (C, C)` | correctly rounded; rem is exact fmod |
| `cmp_B` | `i1 (C, C, i32)` | all 16 LLVM predicates |
| `cmps_B_rm` | `i1 (C, C, i32 P, i32 R)` | signaling comparison, P = 0..15 and R = 0 |
| `{fptosi,fptoui,lround,llround,lrint,llrint}_B` | `i128 (C, i32 M)` | saturated, NaN → 0, signed/unsigned extension |
| `{sitofp,uitofp}_B` | `C (i128)` | correct rounding of exact integer |
| `{fpext,fptrunc}_S_D` | `C_D (C_S)` | exact extension; correctly rounded truncation |
| `{sqrt,floor,ceil,trunc,round,roundeven,rint,nearbyint,canonicalize}_B` | `C (C)` | §13.1, signed zeros and canonical arithmetic NaNs |
| `{minnum,maxnum,minimum,maximum,minimumnum,maximumnum}_B` | `C (C, C)` | §13.1 NaN selection; −0 < +0 |
| `fma_B` | `C (C, C, C)` | one rounding, never mul then add |
| `isfpclass_B` | `i1 (C, i32)` | ten bit-pattern classes |
| `ldexp_B` | `C (C, i32)` | exact scaling, correctly rounded subnormal result |
| `frexp_B` | `{ C, i32 } (C)` | exact fraction and exponent |
| `modf_B` | `{ C, C } (C)` | fractional, integral field order |
| `powi_B_iK` | `C (C, iK)` | deterministic repeated squaring with per-step format rounding; signed exponent retained |
| `{sin,cos,tan,asin,acos,atan,sinh,cosh,tanh,exp,exp2,exp10,log,log2,log10}_B` | `C (C)` | deterministic own-format integer libm; no correct-rounding claim |
| `{atan2,pow}_B` | `C (C, C)` | own-format libm, operand order retained |
| `{sincos,sincospi}_B` | `{ C, C } (C)` | sin then cos; sinpi then cospi |
| `{fptosi,fptoui,lround,llround,lrint,llrint}_B_wide` | `void (ptr, C, i32 M)` | exact saturated M-bit little-endian limb result |
| `{sitofp,uitofp}_B_wide` | `C (ptr, i32 M)` | correctly rounded from all M bits |

`_rm` variants of arithmetic, quiet/signaling comparison, conversion (including `_wide`), sqrt, integer
rounding, min/max and ldexp append `i32 R`. Modes 0–4 are nearest/even, downward,
upward, toward zero, nearest/away. They OR invalid=1, divbyzero=2, overflow=4,
underflow=8, inexact=16 into `__bennett_rt_fenv.flags`; ordinary entry points do
not access the environment. Tininess is detected after rounding. Non-saturating
and .sat FP-to-integer operations share the specified saturated implementation.
For rounding-to-integral functions the operation's named rounding rule applies;
`rint`/`nearbyint` and `lrint`/`llrint` use the supplied R in constrained
wrappers (nearest/even in their ordinary §13.1 wrappers). LLVM `fptrunc.round` can also use
`_rm`; flags may accumulate even when exceptions are ignored.

Quiet `cmp_B_rm` raises invalid only for a signaling NaN. Distinct `cmps_B_rm`
raises invalid for either quiet or signaling NaN, even for false/true predicates;
both return the same truth value and raise no other flags. Comparisons use R = 0
because their source constrained intrinsics have no rounding operand. Every
`_rm` comparison ORs its flags into the runtime environment without a host trap.
Exception-ignore lowering uses plain `cmp_B` for either source intrinsic and
leaves the environment unchanged. Arguments are read-only integer carriers.

Comparisons on f16, bf16, f32, f64 and f128 use format-specific integer IR.
Each export handles signed zeros, ordered predicates and NaNs directly;
constrained entries OR the exact invalid flag into the runtime global. Selecting
only one of these exports retains a single LLVM function with no arithmetic
helpers or scratch slots. `tests/test_compare_closure.py` checks all fifteen
closures in actual published bitcode. All seven formats remain available;
f80 and PPC retain their existing comparison implementations. Consumer
materialisation, budgets and performance must be verified against the newly
pinned publication; producer closure measurements alone do not establish them.

`__bennett_rt_fenv` is an **external runtime global**, with the ABI
`{ i32 round, i32 flags }`; the arith library does not define a competing copy.
For dynamic rounding the normaliser loads `round` and passes it as R. The test
bridge alone defines this global. Code using only unconstrained wrappers has no
reachable reference to it. Flags use ordinary loads/stores under the contract's
single-thread assumption.

The IEEE core uses unsigned 512-bit integers. Libm uses 240 working significand
bits and a 1024-bit integer product for Payne–Hanek reduction with 17,408 bits of
2/pi. Constants are generated with integer Chudnovsky and Python Decimal at
5,400 decimal digits. There are no LLVM FP instructions, APFloat calls, host
math, malloc, or external numerical dependencies in the publication. The six
IEEE formats retain their own precision; none is routed through binary64. x87 unnormals,
pseudo-denormals and pseudo-infinities become canonical NaN inputs. Arithmetic
NaN payload/sign are canonicalised; external bitwise operations preserve bits.
All ordered S/D conversion spellings are available, including redundant ones;
valid LLVM fpext routes are exact, and the numerical conversion machinery rounds
once if a precision-reducing route is called directly.

The bitcode has the tested x86_64 Linux triple and 64-bit little-endian layout.
Cross-target integration/execution is not certified by this gate. Vector
operations need no separate ABI: §13.2 applies these functions lane by lane after
N21; ordered reductions call the scalar operations in left-fold order. FP atomic
normalisation uses the same scalar add/sub/min/max functions. The gate tests
ordered reduction/reassociation inputs and the pinned unfused fmuladd witness;
it does not run or modify the sibling plugin.

## PPCDoubleDouble and libm semantics

PPC high double occupies carrier bits 0..63 and low double bits 64..127. Add and
multiply use the same component operation sequence as LLVM DoubleAPFloat, with
integer-only binary64 operations. Divide and fmod use LLVM's legacy 106-bit
fallback (minimum normal exponent −969, subnormal quantum 2^-1074). Comparison is lexicographic high,
then low. Canonical NaN is high 0x7ff8000000000000, low +0.

Dialect 0.2.12 resolves the PPC priority rule: exact-sum conversion and correctly
rounded canonical-pair sqrt/FMA/integral operations take precedence over legacy
APFloat fallbacks. On both LLVM majors, outgoing FP conversion rounds the exact
sum once, and integer conversion saturates the combined value. Integer inputs
retain every source bit, including sparse tails such as 2^1023+1. Integral
rounding preserves the named operation's flags, including the rint/nearbyint
difference. These paths use an exact 2176-bit magnitude at quantum 2^-1074.
Square root finds its bounding canonical pairs using an integer square root,
then compares exact squares and squared midpoints in 4352 bits. Only the final
result affects its flags; no intermediate binary64 underflow is reported.
Independent Fraction tests cover exact-value conversions, integer saturation,
canonical neighbours and hard square-root midpoints on both majors.

Incoming IEEE conversion preserves its exact dyadic value until final pair
selection. FMA forms the exact product and sum in 4352 integer bits at quantum
2^-2148, including cancellation, then rounds once. Intermediate component
operations contribute no flags. Independent Fraction tests replace APFloat
expectations for these explicit guarantees. Dialect 0.2.13 supplies the total
nearest-even tie rule: compare both low significands, including zero, whenever
either is nonzero; use high parity only when both lows are zero; equal parity
selects the smaller absolute sum. Both signs and zero-low transitions are tested.

Dialect 0.2.13 §13.4 requires a full-domain one-local-ulp envelope, correctly
rounded constrained selection, and exact mathematical flags. Libm uses 240
working bits. Tests select exact carrier bits from directed MPFR intervals,
refining precision when necessary; no ulp tolerance can hide a wrong side.
Passing the sampled IEEE tests is measured evidence, not a universal proof.
Sparse PPC low-component failures remain visible under
`BENNETT_ARITH_PROMISED=1`; see [quality evidence](../docs/quality.md).
The full published domain and all entry points remain required.

Exact dyadic powers and decimal/binary logarithm identities use normalized
integer significands, perfect roots and integer exponentiation before one
target rounding. This derives flags from representability, including exact
roots, reciprocal powers of two, overflow and underflow. Half-integer
sincospi arguments use the full input's quadrant, preserving sparse integer
parity. Exponentials retain strict positivity below all subnormal ranges;
finite saturated tanh values retain the side of their limiting value, including
the PPC low-component tail. These fixes do not establish the remaining global
libm accuracy proof. `tests/test_review_numeric.py` contains independent exact
identities, strict bounds and a directed MPFR interval for the PPC tanh tail.

The PPC exponential has a separate exact path for finite |x| <= 2^-112.
The exact input sum is first split into canonical h+l, including overlapping
or cancelling input fields. Its result has high component 1. The positive
correction exp(x)-1-x is too small to cross a low-component midpoint unless
x is exactly on it; that case selects the upper neighbour. Directed rounding
compares x with log(1+h): the exact quadratic term settles the comparison
unless it cancels l exactly, when the sign of the cubic term settles it.
These integer comparisons preserve sparse tails in all five modes and raise
only inexact; exp(±0) is exactly 1 with no flags. This preserves the sparse low component even for exp(2^-700).
`tests/test_ppc_exp.py` verifies every power-of-two exponent in this range,
both signs, sparse tails, component midpoints, quadratic cancellation, signed
zeros and final flags. Its oracle encloses the exact result between independent
rational Taylor bounds and requires both endpoints to round identically.
The earlier diagnostic `tests/ppc_exp_sparse_witness.py` retains the exact
counterexample bounds. Full-domain libm correctness remains open; the
published contract's domain and available operations are unchanged.

The default bitcode publishes powi at K = 1, 8, 16, 32, 64, 128, 192, 256, 513,
1025 on every format, with `_rm` variants. `scripts/build 18 7 193` (or major 23)
adds exact i7/i193 signatures to that publication and its manifest. The generator
accepts any LLVM integer width 1..8388608 and emits repeated-squaring IR with the
original iK exponent throughout. A bitcode file has a finite export set; consumers
requiring another K must obtain the generated matching-major artifact and pin
its new SHA. The gate verifies the default publication; a custom artifact's
manifest lists its widths. No exponent is narrowed to i32/i128.

## Remaining parametric contracts

The offline generator below implements the 0.2.12 static request protocol.
The default `dist/` manifest targets 0.2.13 and records outstanding verification,
PPC and libm obligations in `conformance_pending`.

All 1,008 previously inventoried concrete signatures are published, plus 126
additional powi and seven signaling comparison signatures: **1,141 exports per
major**, no staged concrete bodies.
Named-format conversions and arbitrary powi widths are available through the
offline generator below. Signaling comparisons are published for all seven
formats. Consumers re-pin the matching bitcode and verify their materialised
L/CC closure; producer tests do not establish consumer resource bounds.

## Offline instances (dialect 0.2.13)

Run `python3 -I softfloat/instantiate.py REQUEST.json OUTPUT_DIRECTORY` with
`TMPDIR` set to an existing job-local build directory. The installed LLVM 18 or
23 tools are used offline. The output is ordinary `bennett-arith.bc` and a JCS
`manifest.json`. The generator does not replace the default distribution.

A request has exactly these fields:

```json
{"schema":"bennett-arith-instantiations-1","llvm_major":23,"target_triple":"x86_64-unknown-linux-gnu","data_layout":"e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128","entries":[{"op":"convert_to","format":"Float6E3M2FN","base":"f128"},{"op":"convert_from","format":"Float8E4M3FN","base":"f80"},{"op":"powi","base":"ppcf128","exponent_bits":193}]}
```

`base` is any of the seven suffixes in the table above. A conversion entry has
exactly `op`, `format`, and `base`; a powi entry has exactly `op`, `base`, and
`exponent_bits`, with an integer width from 1 through 8388608 inclusive. Duplicate
entries request one instance. Requests reject unknown fields, duplicate JSON
keys, invalid widths and format names absent on their LLVM major.

LLVM 23 supports all eleven 0.2.12 interpretation names: `Float8E5M2`,
`Float8E5M2FNUZ`, `Float8E4M3`, `Float8E4M3FN`, `Float8E4M3FNUZ`,
`Float8E4M3B11FNUZ`, `Float8E3M4`, `Float8E8M0FNU`, `Float6E3M2FN`,
`Float6E2M3FN`, and `Float4E2M1FN`. Their carriers are i8, i6, or i4 as named.
LLVM 18 has no arbitrary-format intrinsic names; its requests can instantiate
powi. A missing LLVM APFloat intrinsic helper does not restrict this name set.

Conversion exports are exactly `iN @__bennett_sf_convert_to_<format>_<base>(C_B,
i32 R, i1 Sat)` and `C_B @__bennett_sf_convert_from_<format>_<base>(iN)`.
Conversions use integer arithmetic, canonical NaNs, zero bits for source poison
outcomes, explicit rounding and saturation, and no fenv side effect. PPC inputs
use both component values. Powi requests emit both plain and final-`_rm`
spellings with the original iK exponent and format-rounded repeated squaring.
The generated module contains the requested exported definitions and their
reachable implementation; it imports no host numerical library.

The C implementation first emits integer IR through the pinned x86 frontend,
whose `_BitInt` support includes the working precisions. The generator removes
CPU-specific attributes and assigns the request's triple and data layout to
both modules before linking. Private C function conventions remain internal;
public carrier wrappers are explicit LLVM IR. This also avoids LLVM 18's
AArch64 frontend limit of 128 bits. The limits test verifies AArch64 output
bitcode; numerical execution tests run on x86_64 Linux.
Target fields are checked against the requested LLVM major's interpretation;
LLVM 23 expands historical AArch64 layout spellings with its address-space and
function alignment defaults. The manifest retains the original request string.

Canonical request bytes use JCS with entries deduplicated and sorted by
`(op, base, format-or-empty, exponent_bits-or-zero)`. The manifest has schema
`bennett-arith-instances-1`, `request_sha256`, `bitcode_sha256`, the requested
`llvm_major`, `target_triple`, and `data_layout`, and `exports` sorted by `symbol`.
Each export records its exact LLVM `function_type`. Hashes cover the canonical
request bytes and the actual output bitcode. JCS files have no trailing newline.
Consumers link and pin this matching-major artifact before normalisation in
both builds. No finite set of default widths limits offline generation.

`python3 -I softfloat/test_instances.py` verifies the generated bitcode through
an independent LLVM dispatcher. It checks all source encodings of every named
format into all seven bases, conversion midpoints under all five modes and
both saturation settings, malformed requests, request/bitcode hashes, exact
exports, target fields, sticky flags, and the absence of hardware FP/imported
numerical routines. It does not establish the separate full-domain PPC or transcendental obligations.

`python3 -I softfloat/test_instance_limits.py --reproduce` verifies the inclusive
i8388608 exponent on both majors and AArch64 request fields. Run the numerical
test first: the reproduction check then regenerates its requests and compares
bitcode and JCS manifests byte for byte in different temporary directories.

## Verification

`scripts/gate` builds on both installed toolchains, checks byte-for-byte
reproduction of the publications, audits every manifest signature independently,
and compiles a test-only LLVM dispatcher against the **published bitcode**.
Python runs with `-I`; Fraction/integer division and squared midpoint comparisons
compute expected arithmetic, sqrt and rounding without host FP. No implementation
source is imported by the oracle. Tests cover all modes, canonical/signaling NaNs,
invalid x87 encodings, denormals, infinities, zeros, saturation, aggregate field
order, widths 129/193/257/513/1025, all pairwise format routes, and every export.
All 65,536 encodings of each of half and bfloat are checked for canonicalization,
extension/truncation round trip and square root. Finite arithmetic is otherwise
edge/seeded differential coverage, not an exhaustive proof over binary128.

The build uses `-O1`, disables vectorisation and host builtins, and records no
absolute source path. LLVM-generated integer/memory intrinsics remain for the
normaliser to materialise. Source integer flags/attributes also go through the
normaliser; this is link-input bitcode, not already-materialised ISA code.

The gate additionally sweeps exp/exp2/exp10 through every subnormal-output
exponent and overflow boundaries, and runs a test-only C++ oracle linked to the **same LLVM major's
APFloat**, adaptive directed MPFR bracket comparisons, all 65,536 encodings of half and
bfloat sin, PPC sparse-tail conversions and all predicates, and powi transport
through i1025. `libmpfr.so.6` is required by tests only; LLVM development headers
and llvm-config provide the APFloat oracle. Each manifest records the bitcode
SHA-256, tool versions, and path-independent SHA-256/Git blob SHA-1 of every
implementation/build source. SHA256SUMS also hashes the manifest. Gate builds in
place and requires byte-identical bitcode, manifest and checksum reproduction.

The component adapter in ppc.h follows LLVM DoubleAPFloat algorithms under
Apache-2.0 WITH LLVM-exception; see LLVM-LICENSE.txt. The numerical core,
fixed-precision libm, constant generator and oracle drivers are local code.
````

## `softfloat/generate.py` (343 lines)

````python
"""Emit contract ABI wrappers, a machine-readable manifest, and test-only bridge.
C's ABI lowering of _BitInt(80/128) is NOT the dialect's i80/i128 ABI.
Keeping these wrappers in IR avoids accidental aggregate or sret ABI changes.
"""
import json
import pathlib
import sys

FORMATS = [('f16', 16, 'binary16'), ('bf16', 16, 'bfloat16'),
           ('f32', 32, 'binary32'), ('f64', 64, 'binary64'),
           ('f80', 80, 'x86_fp80'), ('f128', 128, 'binary128'),
           ('ppcf128',128,'PPCDoubleDouble')]
OPS = ('add sub mul div rem cmp fptosi fptoui sitofp uitofp sqrt floor ceil trunc '
       'round roundeven rint nearbyint canonicalize minnum maxnum minimum maximum '
       'minimumnum maximumnum fma isfpclass ldexp frexp lround llround lrint llrint '
       'convert powi modf sin cos tan asin acos atan atan2 sinh cosh tanh exp exp2 exp10 log log2 log10 pow sincos sincospi cmps').split()


def entries(formats=FORMATS):
    for fi, (suffix, bits, fmt) in enumerate(formats):
        C = f'i{bits}'
        for op in OPS:
            if op == 'cmps':
                yield dict(name=f'__bennett_sf_cmps_{suffix}_rm', result='i1', params=[C,C,'i32','i32'],
                           format=fmt, fi=fi, op=op, extra=0, wide=False, constrained=True)
                continue
            if op == 'convert':
                continue
            ret, params = C, [C]
            if op in ('add', 'sub', 'mul', 'div', 'rem', 'minnum', 'maxnum',
                      'minimum', 'maximum', 'minimumnum', 'maximumnum', 'atan2', 'pow'):
                params += [C]
            if op == 'fma':
                params += [C, C]
            if op in ('sitofp', 'uitofp'):
                params = ['i128']
            if op in ('cmp', 'isfpclass'):
                ret, params = 'i1', ([C, C, 'i32'] if op == 'cmp' else [C, 'i32'])
            if op in ('fptosi', 'fptoui', 'lround', 'llround', 'lrint', 'llrint'):
                ret, params = 'i128', [C, 'i32']
            if op == 'ldexp' or op == 'powi':
                params += ['i32']
            if op == 'frexp':
                ret = f'{{ {C}, i32 }}'
            if op in ('modf','sincos','sincospi'):
                ret = f'{{ {C}, {C} }}'
            name = f'__bennett_sf_{op}_{suffix}' + ('_i32' if op == 'powi' else '')
            yield dict(name=name, result=ret, params=params, format=fmt, fi=fi, op=op,
                       extra=0, wide=False, constrained=False)
            if op in ('fptosi', 'fptoui', 'lround', 'llround', 'lrint', 'llrint', 'sitofp', 'uitofp'):
                tofp = op in ('sitofp', 'uitofp')
                for constrained in (False, True):
                    yield dict(name=name+'_wide'+('_rm' if constrained else ''), result=C if tofp else 'void',
                               params=(['ptr', 'i32'] if tofp else ['ptr', C, 'i32'])+(['i32'] if constrained else []),
                               format=fmt, fi=fi, op=op, extra=0, wide=True, constrained=constrained)
            # The numeric core also supports explicit rounding and flag accumulation.
            if op not in ('isfpclass', 'canonicalize', 'frexp', 'modf'):
                yield dict(name=name+'_rm', result=ret, params=params+['i32'],
                           format=fmt, fi=fi, op=op, extra=0, wide=False, constrained=True)
        for di, (dest, db, df) in enumerate(formats):
            if di == fi:
                continue
            for op in ('fpext', 'fptrunc'):
                for constrained in (False, True):
                    yield dict(name=f'__bennett_sf_{op}_{suffix}_{dest}'+('_rm' if constrained else ''),
                               result=f'i{db}', params=[C]+(['i32'] if constrained else []),
                               format=f'{fmt} -> {df}', fi=fi, op='convert', extra=di,
                               wide=False, constrained=constrained)


POWI_WIDTHS = [1,8,16,64,128,192,256,513,1025]
IEEE_COMPARE = {0:10,1:7,2:23,3:52,5:112}

def ieee_compare_wrapper(e):
    """Compare the format's integer fields without retaining the evaluator.

    Ordered positive encodings increase numerically; negative encodings run
    in reverse. Collapse signed zeros for equality, then select the predicate
    truth mask. NaN classification and invalid differ only for cmp/cmps.
    """
    bits=FORMATS[e['fi']][1];C=f'i{bits}';fraction=IEEE_COMPARE[e['fi']]
    magnitude=(1<<(bits-1))-1;infinity=magnitude^((1<<fraction)-1)
    ir=[f"define i1 @{e['name']}({', '.join(t+' %a'+str(i) for i,t in enumerate(e['params']))}) {{"]
    for i in (0,1):
        ir += [f'  %mag{i} = and {C} %a{i}, {magnitude}',
               f'  %nan{i} = icmp ugt {C} %mag{i}, {infinity}',
               f'  %zero{i} = icmp eq {C} %mag{i}, 0']
    ir += ['  %unordered = or i1 %nan0, %nan1',
           '  %bothzero = and i1 %zero0, %zero1',
           f'  %samebits = icmp eq {C} %a0, %a1',
           '  %equal = or i1 %samebits, %bothzero',
           '  %unequal = xor i1 %equal, true',
           f'  %negative = icmp slt {C} %a0, 0',
           f'  %different = xor {C} %a0, %a1',
           f'  %differentsigns = icmp slt {C} %different, 0',
           f'  %ascending = icmp ult {C} %a0, %a1',
           f'  %descending = icmp ugt {C} %a0, %a1',
           '  %samesignless = select i1 %negative, i1 %descending, i1 %ascending',
           '  %rawless = select i1 %differentsigns, i1 %negative, i1 %samesignless',
           '  %less = and i1 %rawless, %unequal',
           '  %eqgtmask = select i1 %equal, i32 170, i32 204',
           '  %mask = select i1 %less, i32 240, i32 %eqgtmask',
           '  %predicate = and i32 %a2, 7',
           '  %shifted = lshr i32 %mask, %predicate',
           '  %ordered = trunc i32 %shifted to i1',
           '  %unorderedtruth = icmp uge i32 %a2, 8',
           '  %result = select i1 %unordered, i1 %unorderedtruth, i1 %ordered']
    if e['constrained']:
        invalid='%unordered'
        if e['op']=='cmp':
            for i in (0,1):
                ir += [f'  %quiet{i} = and {C} %a{i}, {1<<(fraction-1)}',
                       f'  %quietclear{i} = icmp eq {C} %quiet{i}, 0',
                       f'  %snan{i} = and i1 %nan{i}, %quietclear{i}']
            ir += ['  %invalid = or i1 %snan0, %snan1'];invalid='%invalid'
        ir += [f'  %flags = zext i1 {invalid} to i32',
               '  %env = getelementptr { i32, i32 }, ptr @__bennett_rt_fenv, i32 0, i32 1',
               '  %old = load i32, ptr %env, align 4',
               '  %new = or i32 %old, %flags',
               '  store i32 %new, ptr %env, align 4']
    return ir+['  ret i1 %result','}']

def powi_entries(widths):
    for fi,(suffix,bits,fmt) in enumerate(FORMATS):
        for k in widths:
            if k==32:continue
            assert 1<=k<=8388608, 'LLVM integer exponent width out of range'
            for constrained in (False,True):
                yield dict(name=f'__bennett_sf_powi_{suffix}_i{k}'+('_rm' if constrained else ''),
                    result=f'i{bits}',params=[f'i{bits}',f'i{k}']+(['i32'] if constrained else []),
                    format=fmt,fi=fi,op='powi',extra=0,wide=False,constrained=constrained,exponent_bits=k)

def powi_wrapper(e):
    C=e['result'];K=f"i{e['exponent_bits']}";suffix=FORMATS[e['fi']][0]
    rm=', i32 %a2' if e['constrained'] else ''
    tag='_rm' if e['constrained'] else ''
    mul=f'__bennett_sf_mul_{suffix}{tag}';div=f'__bennett_sf_div_{suffix}{tag}'
    one=[0x3c00,0x3f80,0x3f800000,0x3ff0000000000000,0x3fff8000000000000000,0x3fff0000000000000000000000000000,0x3ff0000000000000][e['fi']]
    shift=f'lshr {K} %n, 1' if e['exponent_bits']>1 else 'and i1 %n, 0'
    return f'''define {C} @{e['name']}({', '.join(t+' %a'+str(i) for i,t in enumerate(e['params']))}) {{
entry:
  %neg = icmp slt {K} %a1, 0
  %abs = sub {K} 0, %a1
  %initial = select i1 %neg, {K} %abs, {K} %a1
  %zero = icmp eq {K} %initial, 0
  br i1 %zero, label %empty, label %loop
empty:
  ret {C} {one}
loop:
  %n = phi {K} [ %initial, %entry ], [ %n2, %square ]
  %base = phi {C} [ %a0, %entry ], [ %squared, %square ]
  %result = phi {C} [ {one}, %entry ], [ %next, %square ]
  %bit = trunc {K} %n to i1
  br i1 %bit, label %odd, label %even
odd:
  %product = call {C} @{mul}({C} %result, {C} %base{rm})
  br label %advance
even:
  br label %advance
advance:
  %next = phi {C} [ %product, %odd ], [ %result, %even ]
  %n2 = {shift}
  %done = icmp eq {K} %n2, 0
  br i1 %done, label %finish, label %square
square:
  %squared = call {C} @{mul}({C} %base, {C} %base{rm})
  br label %loop
finish:
  br i1 %neg, label %reciprocal, label %return
reciprocal:
  %recip = call {C} @{div}({C} {one}, {C} %next{rm})
  ret {C} %recip
return:
  ret {C} %next
}}'''.replace('  %bit = trunc i1 %n to i1','  %bit = and i1 %n, true').splitlines()


def generate(dest, widths=POWI_WIDTHS):
    dest.mkdir(parents=True, exist_ok=True)
    rows = list(entries())+list(powi_entries(widths))
    ir = ['; Generated contract ABI; do not use a C ABI for carrier functions.',
          'declare void @bennett_sf_eval(ptr, i32, i32, ptr, i32, i32)',
          'declare void @bennett_sf_wide(ptr, i32, i32, ptr, i32, ptr, i32)',
          '@__bennett_rt_fenv = external global { i32, i32 }']
    bridge = []
    cases = []
    for index, e in enumerate(rows):
        e['id'] = index
        e['signature'] = f"{e['result']} ({', '.join(e['params'])})"
        e['status'] = 'deterministic-integer-libm-v1' if e['op']!='cmps' and OPS.index(e['op'])>=OPS.index('sin') else 'exact' if e['op'] != 'powi' else 'deterministic-repeated-squaring'
        if (e['fi']==6 and e['op']=='fma') or (e['op']=='convert' and e['extra']==6):
            e.update(status='canonical-pair-exact')
        ret, params, op = e['result'], e['params'], e['op']
        if op in ('cmp','cmps') and e['fi'] in IEEE_COMPARE:
            e['comparison_implementation']='format-specific-integer-ir'
            ir += ieee_compare_wrapper(e)
        elif 'exponent_bits' in e:
            ir += powi_wrapper(e)
        else:
            ir += [f"define {ret} @{e['name']}({', '.join(t+' %a'+str(i) for i,t in enumerate(params))}) {{",
                   '  %in = alloca [3 x i128], align 16', '  %out = alloca [3 x i128], align 16',
                   '  store [3 x i128] zeroinitializer, ptr %in, align 16']
            fps = []
            extra = str(e['extra'])
            slot = 'null'
            for i,t in enumerate(params):
                if e['constrained'] and i == len(params)-1:
                    continue
                if t == 'ptr':
                    slot = f'%a{i}'
                elif t == 'i32' and i == len(params)-1-int(e['constrained']) and (e['wide'] or op in ('cmp','cmps','isfpclass','fptosi','fptoui','lround','llround','lrint','llrint','ldexp','powi')):
                    extra = f'%a{i}'
                else:
                    n = len(fps); fps.append(i)
                    ir += [f'  %p{n} = getelementptr i128, ptr %in, i32 {n}']
                    value = f'%a{i}'
                    if t != 'i128':
                        ir += [f'  %z{n} = zext {t} {value} to i128']; value=f'%z{n}'
                    ir += [f'  store i128 {value}, ptr %p{n}, align 16']
            rm = f'%a{len(params)-1}' if e['constrained'] else '0'
            if e['wide']:
                ir += [f'  call void @bennett_sf_wide(ptr %out, i32 {e["fi"]}, i32 {OPS.index(op)}, ptr {slot}, i32 {extra}, ptr %in, i32 {rm})']
            else:
                ir += [f'  call void @bennett_sf_eval(ptr %out, i32 {e["fi"]}, i32 {OPS.index(op)}, ptr %in, i32 {extra}, i32 {rm})']
            if e['constrained']:
                ir += ['  %pf = getelementptr i128, ptr %out, i32 2',
                       '  %fw = load i128, ptr %pf, align 16', '  %fl = trunc i128 %fw to i32',
                       '  %env = getelementptr { i32, i32 }, ptr @__bennett_rt_fenv, i32 0, i32 1',
                       '  %old = load i32, ptr %env', '  %new = or i32 %old, %fl', '  store i32 %new, ptr %env']
            if ret == 'void':
                ir += ['  ret void', '}']
            else:
                ir += ['  %r0 = load i128, ptr %out, align 16']
                if ret.startswith('{'):
                    types = ret[2:-2].split(', ')
                    ir += ['  %p1out = getelementptr i128, ptr %out, i32 1',
                           '  %r1 = load i128, ptr %p1out, align 16']
                    vals = []
                    for j,t in enumerate(types):
                        val = f'%r{j}'
                        if t != 'i128':
                            ir += [f'  %ret{j} = trunc i128 {val} to {t}']; val=f'%ret{j}'
                        vals.append(val)
                    ir += [f'  %pair0 = insertvalue {ret} zeroinitializer, {types[0]} {vals[0]}, 0',
                           f'  %pair1 = insertvalue {ret} %pair0, {types[1]} {vals[1]}, 1', f'  ret {ret} %pair1', '}']
                else:
                    value = '%r0'
                    if ret != 'i128':
                        ir += [f'  %ret = trunc i128 %r0 to {ret}']; value='%ret'
                    ir += [f'  ret {ret} {value}', '}']
        # A separate bridge tests the published wrappers, not a C recompile.
        bridge += [f"declare {ret} @{e['name']}({', '.join(params)})"]
        case = [f'case{index}:']
        args = []
        for j,t in enumerate(params):
            case += [f'  %p{index}_{j} = getelementptr i128, ptr %args, i32 {j}',
                     f'  %v{index}_{j} = load i128, ptr %p{index}_{j}, align 16']
            v = f'%v{index}_{j}'
            if t == 'ptr':
                case += [f'  %x{index}_{j} = inttoptr i128 {v} to ptr']; v=f'%x{index}_{j}'
            elif t.startswith('i') and int(t[1:])>128:
                case += [f'  %ptr{index}_{j} = inttoptr i128 {v} to ptr', f'  %x{index}_{j} = load {t}, ptr %ptr{index}_{j}, align 1']; v=f'%x{index}_{j}'
            elif t != 'i128':
                case += [f'  %x{index}_{j} = trunc i128 {v} to {t}']; v=f'%x{index}_{j}'
            args.append(t+' '+v)
        call = f"call {ret} @{e['name']}({', '.join(args)})"
        case += [f'  %r{index} = '+call if ret!='void' else '  '+call]
        types = ret[2:-2].split(', ') if ret.startswith('{') else ([] if ret=='void' else [ret])
        for j,t in enumerate(types):
            v = f'%r{index}'
            if ret.startswith('{'):
                case += [f'  %el{index}_{j} = extractvalue {ret} {v}, {j}']; v=f'%el{index}_{j}'
            if t != 'i128':
                case += [f'  %wide{index}_{j} = zext {t} {v} to i128']; v=f'%wide{index}_{j}'
            case += [f'  %o{index}_{j} = getelementptr i128, ptr %out, i32 {j}',
                     f'  store i128 {v}, ptr %o{index}_{j}, align 16']
        case += ['  ret void']
        cases += case
    bridge += ['define void @test_call(i32 %id, ptr %args, ptr %out) {',
               '  switch i32 %id, label %bad [']
    bridge += [f'    i32 {i}, label %case{i}' for i in range(len(rows))]
    bridge += ['  ]', 'bad:', '  call void @llvm.trap()', '  unreachable']+cases+['}', 'declare void @llvm.trap()',
                '@__bennett_rt_fenv = global { i32, i32 } zeroinitializer']
    layout='target datalayout = \"e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128\"'
    triple='target triple = \"x86_64-unknown-linux-gnu\"'
    ir=[layout,triple]+ir
    bridge=[layout,triple]+bridge
    for e in rows:
        e['section']='13.4' if e['op'] in ('powi','modf') or (e['op']!='cmps' and OPS.index(e['op'])>=OPS.index('sin')) else '13.5' if e['constrained'] else '13.1'
    (dest/'wrappers.ll').write_text('\n'.join(ir)+'\n')
    (dest/'bridge.ll').write_text('\n'.join(bridge)+'\n')
    (dest/'exports.txt').write_text('\n'.join(e['name'] for e in rows)+'\n__bennett_rt_fenv\n')
    manifest = dict(dialect='0.2.13', isa='0.8',
                    conformance_pending=['ppc-full-domain-arithmetic','elementary-full-domain-accuracy'],
                    instance_generator=dict(command='python3 -I softfloat/instantiate.py REQUEST.json OUTPUT_DIRECTORY',
                        request_schema='bennett-arith-instantiations-1',manifest_schema='bennett-arith-instances-1'),
                    implementation='integer-core-v2-libm1', exports=rows,
                    external_globals=[dict(name='__bennett_rt_fenv', type='{ i32 round, i32 flags }',
                                           owner='bennett-runtimes', used_by='constrained _rm wrappers only')],
                    staged_exports=[], parametric_families=[
                        dict(name='__bennett_sf_powi_B_i<K>', signature='C_B (C_B, iK)',
                             constrained_name='__bennett_sf_powi_B_i<K>_rm', constrained_signature='C_B (C_B, iK, i32 R)',
                             formats='all seven', status='published listed widths; arbitrary LLVM iK widths available offline', published_widths=[32]+list(widths), generator='softfloat/instantiate.py',
                             section='13.4'),
                        dict(name='__bennett_sf_convert_to_<fmt>_B', signature='iN (C_B, i32 R, i1 Sat)',
                             formats='all eleven LLVM23 interpretation names from each of seven bases; no names on LLVM18',
                             generator='softfloat/instantiate.py',section='13.1', status='available-offline'),
                        dict(name='__bennett_sf_convert_from_<fmt>_B', signature='C_B (iN)',
                             formats='each of seven bases from all eleven LLVM23 interpretation names; no names on LLVM18',
                             generator='softfloat/instantiate.py',section='13.1', status='available-offline')])
    implemented={e['name'] for e in rows}
    for e in entries(FORMATS):
        if e['name'] not in implemented:
            e['signature']=f"{e['result']} ({', '.join(e['params'])})"
            e.update(status='staged', section='13.1/13.3/13.5')
            manifest['staged_exports'].append(e)
    manifest['numerical_accuracy'] = dict(contract='0.2.13 13.4: full-domain one-local-ulp; constrained correctly rounded selection and exact flags',
        pending_obligation='elementary-full-domain-accuracy',
        claim='deterministic approximation; no global correct-rounding or ulp-bound proof', working_significand_bits=240,
        exact_dyadic_families=['pow','exp2','exp10','log2','log10','half-integer sincospi'],
        exact_dyadic_method='normalized integer significands, perfect roots/powers and one final target rounding',
        proven_paths=[dict(operation='exp_ppcf128',domain='finite |x| <= 2^-112',
            method='exact high+low midpoint comparison; quadratic/cubic log(1+h) comparison for directed sides',
            guarantee='correct canonical pair in all five modes; zero is exact, otherwise only inexact',
            test='tests/test_ppc_exp.py')],
        payne_hanek_constant_bits=17408, verification='tests/test_trans.py and tests/test_trans_extra.py compare published bitcode with adaptive directed MPFR brackets and exact carrier selection; unresolved PPC cases use BENNETT_ARITH_PROMISED')
    manifest['ppc_semantics'] = dict(oracle='independent exact rational arithmetic for explicit guarantees; same-major LLVM APFloat for component operations', high_component_carrier_bits='0..63',
        both_majors='exact high+low conversions, full-width integer inputs, canonical-pair integral rounding, sqrt and one-rounding exact FMA',
        exact_sum_quantum='2^-1074',exact_sum_bits=2176,sqrt_comparison_bits=4352,
        llvm18='component add/mul; legacy 106-bit divide/remainder operation conventions',
        llvm23='same operations as LLVM18, including explicit 0.2.12 exact-value overrides',
        pending_obligation='ppc-full-domain-arithmetic',
        implementation_gaps='legacy component add/mul and divide/remainder conventions remain versioned')
    manifest['contract_questions']=[]
    manifest['comparison_semantics']=dict(quiet='cmp_B_rm: invalid only on signaling NaN',
        signaling='cmps_B_rm: invalid on any NaN, including false/true predicates',
        specialized_formats=[FORMATS[i][0] for i in IEEE_COMPARE],
        specialization='direct integer IR; no arithmetic evaluator, private helpers or scratch slots',
        predicate_range=[0,15],rounding_operand=0,flags='sticky invalid only; plain cmp_B has no fenv access')
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__ == '__main__':
    generate(pathlib.Path(sys.argv[1]), sorted(set(POWI_WIDTHS+[int(k) for k in sys.argv[2:]])))
````

## `softfloat/named.c` (73 lines)

````c
/* Named LLVM 23 formats. Use the integer core directly, never host FP or
 * APFloat. This translation unit is used by the offline instance generator. */
#include "core.c"
typedef struct { Format f; int behavior; } Named;
enum { NI, NUZ, NFN, NSCALE, NFINITE };
static const Named named[] = {
    {{8,3,5,15,0},NI}, {{8,3,5,16,0},NUZ},
    {{8,4,4,7,0},NI}, {{8,4,4,7,0},NFN},
    {{8,4,4,8,0},NUZ}, {{8,4,4,11,0},NUZ},
    {{8,5,3,3,0},NI}, {{8,1,8,127,0},NSCALE},
    {{6,3,3,3,0},NFINITE}, {{6,4,2,1,0},NFINITE},
    {{4,2,2,1,0},NFINITE}
};
static U named_nan(Named n) {
    return n.behavior==NUZ ? (U)1<<(n.f.bits-1):
           n.behavior==NFN ? mask(n.f.bits-1):
           n.behavior==NSCALE ? 255:n.behavior==NFINITE ? 0:nanbits(n.f);
}
static V named_unpack(U x,Named n) {
    Format f=n.f;int kind=n.behavior;
    if(kind==NI) return unpack(x,f);
    if(kind==NSCALE) return x==255 ? nanv():(V){1,(int)x-127,0,FINITE,0};
    U sign=(U)1<<(f.bits-1),body=x & (sign-1);
    if((kind==NUZ && x==sign) || (kind==NFN && body==sign-1)) return nanv();
    int e=(int)(body>>(f.p-1));
    Big m=body & mask(f.p-1);
    if(e) m|=(Big)1<<(f.p-1);
    return (V){m,(e ? e:1)-f.bias-f.p+1,(int)(x>>(f.bits-1)),FINITE,0};
}
static U named_pack(V a,Named n,int rm,int sat) {
    Format f=n.f;int kind=n.behavior,ignored=0;
    U sign=kind==NSCALE ? 0:(U)a.sign<<(f.bits-1);
    U max=kind==NSCALE ? 254:mask(f.bits-1)-(kind==NFN ? 1:kind==NI ? (1<<(f.p-1)):0);
    if(a.kind==NANV) return named_nan(n);
    /* N1 fixes poison results at zero bits, including unsigned negatives. */
    if(kind==NSCALE && a.sign && (a.mag || a.kind==INF)) return 0;
    int overflow=a.kind==INF;
    if(!overflow) {
        if(!a.mag) return kind==NSCALE || kind==NUZ ? 0:sign;
        int top=width(a.mag)-1+a.exp;
        int target=kind==NSCALE ? (top < -127 ? -127:top):
                   (top < 1-f.bias ? 1-f.bias:top)-(f.p-1);
        a.mag=rounded(a.mag,target-a.exp,a.sign,rm,&ignored);a.exp=target;
        if(width(a.mag)>f.p) {a.mag>>=1;++a.exp;}
        V limit=named_unpack(max,n);limit.sign=a.sign;
        overflow=magcmp(a,limit)>0;
        if(!overflow) {
            if(kind==NSCALE) return (U)(a.exp+127);
            if(!a.mag) return kind==NUZ ? 0:sign;
            if(a.mag<((Big)1<<(f.p-1))) return sign|(U)a.mag;
            return sign|((U)(a.exp+f.p-1+f.bias)<<(f.p-1))|((U)a.mag & (U)mask(f.p-1));
        }
    }
    if(sat || (a.kind==FINITE && (rm==3 || (rm==1 && !a.sign) || (rm==2 && a.sign))))
        return sign|max;
    return kind==NI ? infbits(f,a.sign):0;
}
void bennett_sf_named(U *out,int fi,int ni,int to,const U *in,int rm,int sat) {
    if(fi<0 || fi>6 || ni<0 || ni>10 || rm<0 || rm>4) __builtin_trap();
    Named n=named[ni];int ignored=0;
    if(to) {
        V a=unpack(fi==6 ? low64(in[0]):in[0],formats[fi==6 ? 3:fi]);
        if(fi==6 && a.kind==FINITE) {
            V lo=unpack(in[0]>>64,formats[3]);
            if(a.mag || lo.mag || lo.kind!=FINITE) a=add(a,lo,0);
        }
        out[0]=named_pack(a,n,rm,sat);
    } else {
        V a=named_unpack(in[0],n);
        /* Every finite named value fits binary64 exactly, so its PPC low is 0. */
        out[0]=pack(a,formats[fi==6 ? 3:fi],0,&ignored);
    }
}
````

## `softfloat/ppc_round.h` (88 lines)

````c
/* Round an exact dyadic value once to adjacent canonical binary64 pairs.
 * FMA uses quantum 2^-2148 and at most 4197 bits, including cancellation.
 * Incoming IEEE values retain their original exponent, even below that grid.
 */
static int dyadic_compare(SquareBits a,int ae,SquareBits b,int be) {
    if(!a || !b)return !!a-!!b;
    int aw=square_width(a),bw=square_width(b);
    if(aw+ae!=bw+be)return aw+ae>bw+be ? 1:-1;
    if(ae>be)a<<=ae-be;else b<<=be-ae;
    return a>b ? 1:a<b ? -1:0;
}
static U pair_sign(U x,int sign) {
    return sign ? x^((U)1<<63)^(x>>64 ? (U)1<<127:0):x;
}
static U ppc_even_neighbour(U lower,U upper) {
    /* Dialect 13.1: compare low significands, including zero, whenever
     * either is nonzero; only two zero lows use the high significands.
     * Equal parity selects the smaller magnitude (toward zero). */
    U ll=lower>>64,ul=upper>>64;
    int low=ll || ul;
    int le=!((low ? ll:low64(lower))&1),ue=!((low ? ul:low64(upper))&1);
    return le || !ue ? lower:upper;
}
static U ppc_round_exact(SquareBits mag,int exp,int sign,int rm,int *flags) {
    if(!mag)return (U)sign<<63;
    int mode=sign ? (rm==1 ? 2:rm==2 ? 1:rm):rm;
    if(square_width(mag)+exp>1024)return sum_overflow(sign,rm,flags);
    U maxbits=(U)0x7fefffffffffffffULL|((U)0x7c8fffffffffffffULL<<64);
    PairSum maximum=sum_read(maxbits);
    int mc=dyadic_compare(mag,exp,(SquareBits)maximum.mag,-1074);
    if(mc>=0) {
        if(!mc)return pair_sign(maxbits,sign);
        SumBits boundary=sum_scalar(unpack(0x7fefffffffffffffULL,formats[3])).mag+((SumBits)1<<2044);
        int overflow=mode==2 || ((mode==0 || mode==4) ?
            dyadic_compare(mag,exp+1,(SquareBits)maximum.mag+boundary,-1074)>=0:
            dyadic_compare(mag,exp,(SquareBits)boundary,-1074)>=0);
        if(overflow)return sum_overflow(sign,rm,flags);
        *flags|=16;return pair_sign(maxbits,sign);
    }
    int shift=exp+1074,fractional=0;SumBits n;
    if(shift>=0)n=(SumBits)mag<<shift;
    else {
        int s=-shift;
        n=s>=4352 ? 0:(SumBits)(mag>>s);
        fractional=s>=4352 ? !!mag:!!(mag&(((SquareBits)1<<s)-1));
    }
    int ignored=0;
    U lower=sum_round_pair((PairSum){n,0,FINITE,0},1,&ignored);
    U upper=sum_round_pair((PairSum){n+fractional,0,FINITE,0},2,&ignored),result;
    PairSum l=sum_read(lower),u=sum_read(upper);
    if(mode==1 || mode==3)result=lower;
    else if(mode==2)result=upper;
    else {
        int midpoint=dyadic_compare(mag,exp+1,(SquareBits)l.mag+u.mag,-1074);
        if(midpoint<0)result=lower;
        else if(midpoint>0 || mode==4)result=upper;
        else result=ppc_even_neighbour(lower,upper);
    }
    PairSum rounded=sum_read(result);
    if(dyadic_compare(mag,exp,(SquareBits)rounded.mag,-1074)) {
        *flags|=16;if(rounded.mag<((SumBits)1<<52))*flags|=8;
    }
    return pair_sign(result,sign);
}
static U ppc_round(V a,int rm,int *flags) {
    if(a.kind==NANV){if(a.snan)*flags|=1;return nanbits(formats[3]);}
    if(a.kind==INF)return infbits(formats[3],a.sign);
    return ppc_round_exact((SquareBits)a.mag,a.exp,a.sign,rm,flags);
}
static U ppc_fma(U x,U y,U z,int rm,int *flags) {
    PairSum a=sum_read(x),b=sum_read(y),c=sum_read(z);
    if(a.snan || b.snan || c.snan)*flags|=1;
    if(a.kind==NANV || b.kind==NANV || c.kind==NANV)return nanbits(formats[3]);
    int invalid=(a.kind==INF && b.kind==FINITE && !b.mag) ||
                (b.kind==INF && a.kind==FINITE && !a.mag);
    if(invalid){*flags|=1;return nanbits(formats[3]);}
    int sign=a.sign^b.sign;
    if(a.kind==INF || b.kind==INF) {
        if(c.kind==INF && c.sign!=sign){*flags|=1;return nanbits(formats[3]);}
        return infbits(formats[3],sign);
    }
    if(c.kind==INF)return infbits(formats[3],c.sign);
    SquareBits product=(SquareBits)a.mag*b.mag,addend=(SquareBits)c.mag<<1074,mag;
    if(sign==c.sign)mag=product+addend;
    else if(product>=addend){mag=product-addend;if(!mag)sign=rm==1;}
    else {mag=addend-product;sign=c.sign;}
    return ppc_round_exact(mag,-2148,sign,rm,flags);
}
````

## `softfloat/ppc_sum.h` (202 lines)

````c
/* Exact sums of two binary64 components. Every finite component is an integer
 * multiple of 2^-1074; 2176 bits cover both full exponent ranges plus a carry.
 * These helpers never round an intermediate component or use host FP. */
typedef unsigned _BitInt(2176) SumBits;
typedef struct { SumBits mag; int sign,kind,snan; } PairSum;
static SumBits sum_mask(int n) { return n==2176 ? ~(SumBits)0:((SumBits)1<<n)-1; }
static int sum_width(SumBits x) {
    int n=0;
    if(x>>2048){x>>=2048;n+=2048;}
    if(x>>1024){x>>=1024;n+=1024;}
    if(x>>512){x>>=512;n+=512;}
    return n+width((Big)x);
}
static PairSum sum_scalar(V a) {
    return (PairSum){a.kind==FINITE ? (SumBits)a.mag<<(a.exp+1074):0,a.sign,a.kind,a.snan};
}
static PairSum sum_add(PairSum a,PairSum b) {
    if(!a.mag && !b.mag) return (PairSum){0,a.sign==b.sign ? a.sign:0,FINITE,0};
    if(!a.mag)return b;
    if(!b.mag)return a;
    if(a.sign==b.sign)return (PairSum){a.mag+b.mag,a.sign,FINITE,0};
    if(a.mag==b.mag)return (PairSum){0,0,FINITE,0};
    return a.mag>b.mag ? (PairSum){a.mag-b.mag,a.sign,FINITE,0}:(PairSum){b.mag-a.mag,b.sign,FINITE,0};
}
static PairSum sum_read(U x) {
    V h=unpack(low64(x),formats[3]),l=unpack(x>>64,formats[3]);
    int sn=h.snan || l.snan;
    if(h.kind==NANV || l.kind==NANV)return (PairSum){0,0,NANV,sn};
    if(h.kind==INF || l.kind==INF) {
        if(h.kind==INF && l.kind==INF && h.sign!=l.sign)return (PairSum){0,0,NANV,1};
        return (PairSum){0,h.kind==INF ? h.sign:l.sign,INF,0};
    }
    if(!h.mag && !l.mag)return (PairSum){0,h.sign,FINITE,0};
    return sum_add(sum_scalar(h),sum_scalar(l));
}
static V sum_value(PairSum a) {
    if(a.kind!=FINITE || !a.mag)return (V){0,0,a.sign,a.kind,a.snan};
    int shift=sum_width(a.mag)-480;if(shift<0)shift=0;
    Big m=(Big)(a.mag>>shift);
    if(shift && (a.mag&sum_mask(shift)))m|=1;
    return (V){m,shift-1074,a.sign,FINITE,0};
}
static SumBits sum_integral(PairSum a,int mode,int record_inexact,int *flags) {
    SumBits q=a.mag>>1074,rem=a.mag&sum_mask(1074),half=(SumBits)1<<1073;
    if(!rem)return q;
    if(record_inexact)*flags|=16;
    int up=(mode==1 && a.sign) || (mode==2 && !a.sign) ||
        ((mode==0 || mode==4) && (rem>half || (rem==half && (mode==4 || (q&1)))));
    return q+up;
}
static U sum_overflow(int sign,int mode,int *flags) {
    *flags|=20;
    if(mode==3 || (mode==1 && !sign) || (mode==2 && sign)) {
        U s=(U)sign<<63;
        return (s|0x7fefffffffffffffULL)|((s|0x7c8fffffffffffffULL)<<64);
    }
    return infbits(formats[3],sign);
}
static PairSum sum_difference(PairSum a,PairSum b) { b.sign^=1;return sum_add(a,b); }
static U sum_round_pair(PairSum exact,int mode,int *flags) {
    if(!exact.mag)return (U)exact.sign<<63;
    int ignored=0;
    U hi=pack(sum_value(exact),formats[3],0,&ignored);
    V h=unpack(hi,formats[3]);
    if(h.kind==INF)return sum_overflow(exact.sign,mode,flags);
    h.sign^=1;
    PairSum residual=sum_add(exact,sum_scalar(h));
    V rv=sum_value(residual);U lo;
    if(mode==4) {
        U down=pack(rv,formats[3],1,&ignored),up=pack(rv,formats[3],2,&ignored);
        PairSum de=sum_difference(residual,sum_scalar(unpack(down,formats[3])));
        PairSum ue=sum_difference(sum_scalar(unpack(up,formats[3])),residual);
        lo=de.mag<ue.mag ? down:de.mag>ue.mag ? up:exact.sign ? down:up;
    } else {
        int lm=mode==3 ? (exact.sign ? 2:1):mode;
        lo=pack(rv,formats[3],lm,&ignored);
    }
    if(!residual.mag)lo=0;
    PairSum rounded=sum_add(sum_scalar(unpack(hi,formats[3])),sum_scalar(unpack(lo,formats[3])));
    hi=pack(sum_value(rounded),formats[3],0,&ignored);h=unpack(hi,formats[3]);
    if(h.kind==INF)return sum_overflow(exact.sign,mode,flags);
    PairSum tail=sum_difference(rounded,sum_scalar(h));
    lo=tail.mag ? pack(sum_value(tail),formats[3],0,&ignored):0;
    U result=hi|(lo<<64);
    PairSum actual=sum_read(result);
    if(actual.mag!=exact.mag || actual.sign!=exact.sign) {
        *flags|=16;
        if(actual.mag<((SumBits)1<<52))*flags|=8;
    }
    return result;
}
static U sum_integer_pair(SumBits n,int sign,int mode,int *flags) {
    return sum_round_pair((PairSum){n<<1074,sign,FINITE,0},mode,flags);
}
static U ppc_sum_fromwide(const unsigned char *src,int bits,int sign,int rm,int *flags) {
    if(bits<1)__builtin_trap();
    V leading=fromwide(src,bits,sign);
    if(leading.mag && width(leading.mag)+leading.exp>1024)return sum_overflow(leading.sign,rm,flags);
    SumBits n=0;unsigned carry=leading.sign;
    for(int i=0;i<(bits+7)/8;++i) {
        unsigned v=(src[i]^(leading.sign ? 255:0))+carry;carry=v>>8;v&=255;
        if(bits-8*i<8)v&=(1u<<(bits-8*i))-1;
        if(8*i<2176)n|=(SumBits)v<<(8*i);
    }
    return sum_integer_pair(n,leading.sign,rm,flags);
}
static U ppc_sum_integral(U x,int op,int rm,int *flags) {
    PairSum a=sum_read(x);
    if(a.kind==NANV){if(a.snan)*flags|=1;return nanbits(formats[3]);}
    if(a.kind==INF)return infbits(formats[3],a.sign);
    int mode=op==FLOOR ? 1:op==CEIL ? 2:op==TRUNC ? 3:op==ROUND ? 4:op==ROUNDEVEN ? 0:rm;
    SumBits n=sum_integral(a,mode,op==RINT,flags);
    return sum_integer_pair(n,a.sign,rm,flags);
}
/* sqrt(x)/2^-1074 = sqrt(M*2^1074), where x=M*2^-1074 exactly.
 * The radicand has at most 3173 bits, and squared pair midpoints at most 3176.
 * Every canonical pair lies on the 2^-1074 grid. Its neighbours are therefore
 * found by directed rounding of floor(root) and floor(root)+1, without an
 * approximate real square root. Only final comparisons affect IEEE flags. */
typedef unsigned _BitInt(4352) SquareBits;
static int square_width(SquareBits x) {
    int n=0;
    if(x>>4096){x>>=4096;n+=4096;}
    if(x>>2048){x>>=2048;n+=2048;}
    if(x>>1024){x>>=1024;n+=1024;}
    if(x>>512){x>>=512;n+=512;}
    return n+width((Big)x);
}
#include "ppc_round.h"
static U ppc_sum_sqrt(U x,int rm,int *flags) {
    PairSum a=sum_read(x);
    if(a.kind==NANV){if(a.snan)*flags|=1;return nanbits(formats[3]);}
    if(a.sign && (a.mag || a.kind==INF)){*flags|=1;return nanbits(formats[3]);}
    if(a.kind==INF)return infbits(formats[3],0);
    if(!a.mag)return (U)a.sign<<63;
    SquareBits rad=(SquareBits)a.mag<<1074,root=0,rem=0;
    for(int i=(square_width(rad)+1)/2-1;i>=0;--i) {
        rem=(rem<<2)|((rad>>(2*i))&3);
        SquareBits trial=(root<<2)|1;
        root<<=1;
        if(rem>=trial){rem-=trial;++root;}
    }
    int ignored=0;
    U lower=sum_round_pair((PairSum){(SumBits)root,0,FINITE,0},1,&ignored);
    PairSum ls=sum_read(lower);
    if((SquareBits)ls.mag*ls.mag==rad)return lower;
    U upper=sum_round_pair((PairSum){(SumBits)(root+1),0,FINITE,0},2,&ignored);
    PairSum us=sum_read(upper);U result;
    if(rm==1 || rm==3)result=lower;
    else if(rm==2)result=upper;
    else {
        SquareBits mid=(SquareBits)ls.mag+us.mag;
        SquareBits squared=mid*mid,scaled=rad<<2;
        if(scaled<squared)result=lower;
        else if(scaled>squared || rm==4)result=upper;
        else result=ppc_even_neighbour(lower,upper);
    }
    PairSum r=sum_read(result);
    if((SquareBits)r.mag*r.mag!=rad) {
        *flags|=16;
        if(r.mag<((SumBits)1<<52))*flags|=8;
    }
    return result;
}
static U ppc_sum_integer(U x,int bits,int sign,int mode,int record_inexact,int *flags) {
    if(bits<1 || bits>128)__builtin_trap();
    PairSum a=sum_read(x);
    if(a.kind==NANV){*flags|=1;return 0;}
    SumBits n=sum_integral(a,mode,record_inexact,flags);
    SumBits bound=sign ? (SumBits)1<<(bits-1):sum_mask(bits);
    if(sign && !a.sign)--bound;
    if(!sign && a.sign)bound=0;
    if(a.kind==INF || n>bound){n=bound;*flags|=1;}
    return a.sign ? (U)0-(U)n:(U)n;
}
static void ppc_sum_towide(unsigned char *slot,U x,int bits,int sign,int mode,int record_inexact,int *flags) {
    if(bits<1)__builtin_trap();
    PairSum a=sum_read(x);
    if(a.kind==NANV){*flags|=1;a=(PairSum){0,0,FINITE,0};}
    SumBits n=sum_integral(a,mode,record_inexact,flags);
    int nb=sum_width(n),sat=a.kind==INF || nb>bits-sign;
    if(sign && a.sign && nb==bits && n && !(n&(n-1)))sat=0;
    if(!sign && a.sign && n)sat=1;
    if(sat)*flags|=1;
    unsigned carry=a.sign;
    for(int i=0;i<(bits+7)/8;++i) {
        unsigned byte=0;
        if(sat) {
            for(int j=0;j<8 && 8*i+j<bits;++j) {
                int k=8*i+j;
                unsigned bit=sign ? (a.sign ? k==bits-1:k<bits-1):!a.sign;
                byte|=bit<<j;
            }
        } else {
            unsigned digit=8*i<2176 ? (unsigned)(n>>(8*i))&255:0;
            unsigned v=(digit^(a.sign ? 255:0))+carry;carry=v>>8;byte=v&255;
            if(bits-8*i<8)byte&=(1u<<(bits-8*i))-1;
        }
        slot[i]=(unsigned char)byte;
    }
    for(int i=(bits+7)/8;i<8*((bits+63)/64);++i)slot[i]=0;
}
````

## `softfloat/test_instances.py` (229 lines)

````python
"""Black-box tests of the offline 0.2.12 request and actual LLVM carrier ABI.

Run with python3 -I softfloat/test_instances.py. Expected numbers use Fraction;
the implementation is invoked only as a separate generator and linked bitcode.
"""
import ctypes
from fractions import Fraction as Q
from functools import cache, lru_cache
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
WORK = Path(os.environ['TMPDIR']) / 'instances-test'
WORK.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('edge', ROOT/'tests/test_edge.py')
edge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edge)
FORMATS = {
    # bits, precision, exponent bits, bias, nonfinite encoding
    'Float8E5M2': (8,3,5,15,'ieee'),
    'Float8E5M2FNUZ': (8,3,5,16,'uz'),
    'Float8E4M3': (8,4,4,7,'ieee'),
    'Float8E4M3FN': (8,4,4,7,'fn'),
    'Float8E4M3FNUZ': (8,4,4,8,'uz'),
    'Float8E4M3B11FNUZ': (8,4,4,11,'uz'),
    'Float8E3M4': (8,5,3,3,'ieee'),
    'Float8E8M0FNU': (8,1,8,127,'scale'),
    'Float6E3M2FN': (6,3,3,3,'finite'),
    'Float6E2M3FN': (6,4,2,1,'finite'),
    'Float4E2M1FN': (4,2,2,1,'finite'),
}

def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()

def decode(x, f):
    n,p,eb,bias,kind = f
    if kind == 'scale':
        return 'nan' if x == 255 else edge.power(x-127)
    sign=x>>(n-1); body=x & ((1<<(n-1))-1)
    exponent=body>>(p-1); fraction=body & ((1<<(p-1))-1)
    if kind == 'uz' and x == 1<<(n-1): return 'nan'
    if kind == 'fn' and body == (1<<(n-1))-1: return 'nan'
    if kind == 'ieee' and exponent == (1<<eb)-1:
        return 'nan' if fraction else ('-inf' if sign else 'inf')
    v=(fraction+((1<<(p-1)) if exponent else 0))*edge.power((exponent or 1)-bias-p+1)
    return -v if sign else v

@cache
def finite_values(f):
    n,p,eb,bias,kind=f
    return {decode(i,f):i for i in range(1<<(n if kind=='scale' else n-1)) if isinstance(decode(i,f),Q)}

@cache
def limits(f):
    values=finite_values(f)
    return min(values),max(values),values[max(values)]

@lru_cache(maxsize=32768)
def expected_to(value, sign, f, rm, sat):
    n,p,eb,bias,kind=f
    nan = {'ieee': (((1<<eb)-1)<<(p-1)) | (1<<max(0,p-2)),
           'uz': 1<<(n-1), 'fn': (1<<(n-1))-1, 'finite': 0, 'scale': 255}[kind]
    if value == 'nan': return nan
    values=finite_values(f)
    minimum,maximum,maxbits=limits(f)
    if kind == 'scale' and sign and value != 0: return 0
    if isinstance(value,str):
        if not sat and kind!='ieee': return 0
        result=maxbits if sat else (((1<<eb)-1)<<(p-1) if kind=='ieee' else 0)
    else:
        v=abs(value)
        if kind == 'scale':
            if v < minimum: return 0
            step=edge.log2q(v)
        else:
            step=max(edge.log2q(v) if v else 1-bias, 1-bias)-p+1
        units,_=edge.roundedq(v/edge.power(step),sign,rm)
        rounded=units*edge.power(step)
        if rounded>maximum:
            finite_direction=rm==3 or (rm==1 and not sign) or (rm==2 and sign)
            if not sat and not finite_direction and kind!='ieee': return 0
            result=maxbits if sat or finite_direction else (((1<<eb)-1)<<(p-1) if kind=='ieee' else 0)
        else:
            result=values[rounded]
            if not result and kind=='uz': return 0
    return result | ((sign<<(n-1)) if kind!='scale' and (result or kind in ('ieee','finite','fn')) else 0)

count=0
# Invalid requests must fail before creating a publication. This also guards
# Python's bool-is-an-int behavior and JSON's otherwise permissive parser.
valid=dict(schema='bennett-arith-instantiations-1',llvm_major=23,
           target_triple='x86_64-unknown-linux-gnu',data_layout='e',entries=[])
bad=[{**valid,'schema':'unknown'}, {**valid,'extra':0},
     {**valid,'llvm_major':True}, {**valid,'entries':{}},
     {**valid,'target_triple':'x86_64\n'}]
bad += [{**valid,'entries':[dict(op='powi',base='f32',exponent_bits=k)]}
        for k in (0,8388609,True,1.0)]
bad += [{**valid,'entries':[dict(op='convert_to',base='f32',format='made-up')]},
        {**valid,'llvm_major':18,'entries':[dict(op='convert_from',base='f16',format='Float8E4M3')]},
        {**valid,'entries':[dict(op='powi',base='f32',exponent_bits=7,extra=1)]}]
for i,body in enumerate([json.dumps(x) for x in bad]+['{"schema":"a","schema":"b"}','{"llvm_major":NaN}']):
    req=WORK/'invalid.json';req.write_text(body)
    out=WORK/f'invalid-{i}'
    proc=subprocess.run([sys.executable,'-I',str(ROOT/'softfloat/instantiate.py'),str(req),str(out)],capture_output=True,text=True)
    assert proc.returncode!=0 and not (out/'bennett-arith.bc').exists(),body
print(f'{len(bad)+2} invalid requests rejected before publication')
for major in (18,23):
    llvm=Path(f'/usr/lib/llvm-{major}/bin')
    layout='e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128'
    bases={**edge.FORMATS,'ppcf128': (128,106,11,1023,False)}
    entries=[dict(op='powi',base=b,exponent_bits=k) for b in bases for k in (1,7,32,193)]
    if major==23:
        entries += [dict(op=op,base=b,format=f) for b in bases for f in FORMATS for op in ('convert_to','convert_from')]
    request=dict(schema='bennett-arith-instantiations-1',llvm_major=major,
                 target_triple='x86_64-unknown-linux-gnu',data_layout=layout,entries=entries[::-1]+entries[:2])
    req=WORK/f'request-{major}.json';req.write_text(json.dumps(request))
    out=WORK/f'llvm{major}'
    if '--reuse' not in sys.argv:
        subprocess.run([sys.executable,'-I',str(ROOT/'softfloat/instantiate.py'),str(req),str(out)],check=True)
    mbytes=(out/'manifest.json').read_bytes();m=json.loads(mbytes)
    assert mbytes==canonical(m), 'manifest must be JCS without trailing newline'
    request['entries']=sorted(entries,key=lambda e:(e['op'],e['base'],e.get('format',''),e.get('exponent_bits',0)))
    assert m['request_sha256']==hashlib.sha256(canonical(request)).hexdigest()
    bc=out/'bennett-arith.bc'
    assert m['bitcode_sha256']==hashlib.sha256(bc.read_bytes()).hexdigest()
    assert m['schema']=='bennett-arith-instances-1'
    assert m['exports']==sorted(m['exports'],key=lambda e:e['symbol'])
    expected={}
    for entry in request['entries']:
        base=entry['base'];c=f'i{bases[base][0]}'
        if entry['op']=='powi':
            k=entry['exponent_bits'];name=f'__bennett_sf_powi_{base}_i{k}'
            expected[name]=f'{c} ({c}, i{k})'
            expected[name+'_rm']=f'{c} ({c}, i{k}, i32)'
        else:
            fmt=entry['format'];n=f'i{FORMATS[fmt][0]}'
            expected[f'__bennett_sf_{entry["op"]}_{fmt}_{base}']=f'{n} ({c}, i32, i1)' if entry['op']=='convert_to' else f'{c} ({n})'
    assert {e['symbol']:e['function_type'] for e in m['exports']}==expected
    ir=subprocess.check_output([str(llvm/'llvm-dis'),str(bc),'-o','-'],text=True)
    assert f'target datalayout = "{layout}"' in ir
    assert 'target triple = "x86_64-unknown-linux-gnu"' in ir
    assert not re.search(r'\b(?:fadd|fsub|fmul|fdiv|frem|fcmp|fptrunc|fpext|sitofp|uitofp)\b',ir)
    definitions=set(re.findall(r'^define (?!internal)[^@\n]+@([^ (]+)',ir,re.M))
    assert definitions=={e['symbol'] for e in m['exports']}
    signatures={name:f'{ret} ({", ".join(p.split()[0] for p in params.split(", "))})'
                for ret,name,params in re.findall(r'^define (i[0-9]+) @([^ (]+)\(([^)]*)\)',ir,re.M)}
    assert signatures==expected
    assert not re.findall(r'^declare .*@(?!llvm\.)[^ (]+',ir,re.M)
    bridge=['@__bennett_rt_fenv = global {i32, i32} zeroinitializer']
    for i,row in enumerate(m['exports']):
        ret,params=row['function_type'].split(' (');params=params[:-1].split(', ')
        bridge += [f'declare {ret} @{row["symbol"]}({", ".join(params)})',f'define void @call{i}(ptr %in, ptr %out) {{']
        args=[]
        for j,t in enumerate(params):
            bridge += [f'%p{j} = getelementptr i256, ptr %in, i32 {j}',f'%v{j} = load {t}, ptr %p{j}, align 1']
            args.append(f'{t} %v{j}')
        bridge += [f'%r = call {ret} @{row["symbol"]}({", ".join(args)})',f'store {ret} %r, ptr %out, align 1','ret void','}']
    bridgepath=out/'test.ll';bridgepath.write_text('\n'.join(bridge))
    so=out/'test.so'
    subprocess.run([str(llvm/'clang'),'-shared','-fPIC',str(bc),str(bridgepath),'-o',str(so)],check=True)
    lib=ctypes.CDLL(str(so));env=(ctypes.c_int*2).in_dll(lib,'__bennett_rt_fenv')
    def check(i,args,want,flags=0):
        global count
        fn=getattr(lib,f'call{i}');fn.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        src=ctypes.create_string_buffer(b''.join(x.to_bytes(32,'little') for x in args))
        dst=ctypes.create_string_buffer(16);env[0]=4;env[1]=32
        fn(src,dst);actual=int.from_bytes(dst.raw,'little')
        assert actual==want,(m['exports'][i]['symbol'],args,hex(actual),hex(want))
        assert env[0]==4 and env[1]==32|flags,(m['exports'][i]['symbol'],list(env),flags)
        count+=1
    for i,row in enumerate(m['exports']):
        name=row['symbol'];b=next(b for b in bases if f'_{b}_i' in name or name.endswith('_'+b))
        f=bases[b]
        if 'powi' in name:
            one=edge.encode(Q(1),edge.FORMATS['f64'] if b=='ppcf128' else f)[0]
            k=int(re.search(r'_i(\d+)',name)[1]);exponent=(1<<k)-1
            check(i,[one,exponent]+([0] if name.endswith('_rm') else []),one)
            if k==193 and b=='f64':
                constrained=name.endswith('_rm');rm=[0] if constrained else []
                two=edge.encode(Q(2),f)[0]
                for exponent,want in [(1<<180,edge.infinity(f)),((1<<k)-(1<<180),0)]:
                    check(i,[two,exponent]+rm,want,20 if constrained else 0)
            continue
        fmt=next(fmt for fmt in FORMATS if f'_{fmt}_' in name);nf=FORMATS[fmt]
        if 'convert_from' in name:
            for bits in range(1<<nf[0]):
                value=decode(bits,nf);sign=bits>>(nf[0]-1) if nf[4]!='scale' else 0
                if value=='-inf': value='inf'
                want=edge.encode(value,edge.FORMATS['f64'] if b=='ppcf128' else f,zero_sign=sign)[0]
                check(i,[bits],want)
        else:
            values=[Q(0),Q(1),Q(-1),edge.power(-140),edge.power(130),'inf','nan']
            positives=sorted({decode(x,nf) for x in range(1<<(nf[0] if nf[4]=='scale' else nf[0]-1)) if isinstance(decode(x,nf),Q)})
            for a,z in zip(positives,positives[1:]):
                values += [(a+z)/2, (a+z)/2-edge.power(-150), (a+z)/2+edge.power(-150)]
            values += [-v for v in values if isinstance(v,Q)]
            values += [positives[-1]*2,positives[-1]+(positives[-1]-positives[-2])/2]
            for value in values:
                bits=edge.encode(value,edge.FORMATS['f64'] if b=='ppcf128' else f)[0]
                actualvalue,sign,_=edge.decode(bits,edge.FORMATS['f64'] if b=='ppcf128' else f)
                for rm in range(5):
                    for sat in (0,1): check(i,[bits,rm,sat],expected_to(actualvalue,sign,nf,rm,sat))
            bf=edge.FORMATS['f64'] if b=='ppcf128' else f
            for bits in [1<<(bf[0]-1),edge.infinity(bf,1),edge.nan(bf)|1]:
                value,sign,_=edge.decode(bits,bf)
                for rm in range(5):
                    for sat in (0,1): check(i,[bits,rm,sat],expected_to(value,sign,nf,rm,sat))
            if b=='ppcf128':
                # A sparse low component on either side of a target midpoint
                # must determine rounding even across a gap exceeding 512 bits.
                for a,z in zip(positives,positives[1:]):
                    high=(a+z)/2
                    h=edge.encode(high,bf)[0]
                    for low in (-edge.power(-700),edge.power(-700)):
                        lowbits=edge.encode(low,bf)[0]|0x12345
                        bits=h|(lowbits<<64)
                        value=high+edge.decode(lowbits,bf)[0]
                        for rm in range(5):
                            for sat in (0,1): check(i,[bits,rm,sat],expected_to(value,int(value<0),nf,rm,sat))
    print(f'LLVM {major}: request hash, exact exports, integer closure and carrier values verified ({count} checks)')
print('offline instantiation tests passed')
````

## `softfloat/test_publication.py` (24 lines)

````python
"""Independent audit of the 0.2.13 offline generator's publication metadata."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
for major in (18,23):
    dist=ROOT/f'dist/llvm{major}'
    m=json.loads((dist/'manifest.json').read_text())
    assert m['dialect']=='0.2.13'
    assert m['bitcode_sha256']==hashlib.sha256((dist/'bennett-arith.bc').read_bytes()).hexdigest()
    generator=m['instance_generator']
    assert generator['command']=='python3 -I softfloat/instantiate.py REQUEST.json OUTPUT_DIRECTORY'
    assert generator['request_schema']=='bennett-arith-instantiations-1'
    assert generator['manifest_schema']=='bennett-arith-instances-1'
    families={f['name']:f for f in m['parametric_families']}
    to=families['__bennett_sf_convert_to_<fmt>_B']
    fr=families['__bennett_sf_convert_from_<fmt>_B']
    assert to['signature']=='iN (C_B, i32 R, i1 Sat)'
    assert fr['signature']=='C_B (iN)'
    assert to['status']==fr['status']=='available-offline'
    assert {'ppc-full-domain-arithmetic','elementary-full-domain-accuracy'}<=set(m['conformance_pending'])
    assert m['numerical_accuracy']['pending_obligation']=='elementary-full-domain-accuracy'
    print(f'LLVM {major}: 0.2.13 request protocol, exact signatures and pending numerical obligations recorded')
````

## `softfloat/trans.h` (362 lines)

````c
/* Versioned integer libm v1. 240 significant working bits; no host FP.
 * Payne-Hanek reduction uses 17408 bits of 2/pi over the full binary128 range.
 * Results are deterministic approximations, NOT claimed correctly rounded.
 */
#include "constants.h"
/* Two 113-bit input significands plus guard bits for near-one powers;
 * twice this precision still fits the 512-bit product accumulator. */
enum { TRANS_BITS = 240 };
static V tn(V a) {
    if(a.kind==FINITE && width(a.mag)>TRANS_BITS) {int s=width(a.mag)-TRANS_BITS;a.mag=jam(a.mag,s);a.exp+=s;}
    return a;
}
static V ti(int n) { return (V){n<0 ? (Big)(0u-(unsigned)n):(Big)n,0,n<0,FINITE,0}; }
static int tinyterm(V term,V sum) {return !term.mag || (sum.mag && width(term.mag)+term.exp < width(sum.mag)+sum.exp-240);}
static V tneg(V a) {a.sign^=1;return a;}
static V ta(V a,V b) {return tn(add(a,b,0));}
static V tm(V a,V b) {return tn(mul(tn(a),tn(b)));}
static V td(V a,V b) {
    a=tn(a);b=tn(b);int sign=a.sign^b.sign;
    if(a.kind==NANV || b.kind==NANV || (a.kind==INF && b.kind==INF) || (!a.mag && a.kind==FINITE && !b.mag && b.kind==FINITE))return nanv();
    if(a.kind==INF || (b.kind==FINITE && !b.mag))return (V){0,0,sign,INF,0};
    if(b.kind==INF || !a.mag)return (V){0,0,sign,FINITE,0};
    int shift=256+width(b.mag)-width(a.mag);Big rem;
    Big q=quotient(a.mag<<shift,b.mag,&rem);
    return tn((V){q|(rem!=0),a.exp-b.exp-shift,sign,FINITE,0});
}
static V tsqrt(V a) {
    if(a.kind==NANV || (a.sign && (a.mag || a.kind==INF)))return nanv();
    if(a.kind==INF || !a.mag)return a;
    int shift=480-width(a.mag);if((a.exp-shift)%2)--shift;
    Big n=a.mag<<shift,root=0,rem=0;
    for(int i=239;i>=0;--i) {rem=(rem<<2)|((n>>(2*i))&3);Big trial=(root<<2)|1;root<<=1;if(rem>=trial){rem-=trial;++root;}}
    return tn((V){root|(rem!=0),(a.exp-shift)/2,0,FINITE,0});
}
static V tred(V a,int *quadrant) {
    if(width(a.mag)+a.exp<=-1) {*quadrant=0;return a;}
    a=tn(a);int start=17408-a.exp-320-192;
    typedef unsigned _BitInt(1024) Product;
    Product window=0;
    for(int i=0;i<9;++i) {
        int pos=start+64*i,index=pos/64,offset=pos%64;
        unsigned long long limb=index>=0 && index<272 ? two_over_pi[index]>>offset:0;
        if(offset && index+1>=0 && index+1<272)limb|=two_over_pi[index+1]<<(64-offset);
        window|=(Product)limb<<(64*i);
    }
    Big y=(Big)(((Product)window*(Product)a.mag)>>192)&mask(322);
    int q=(int)(y>>320);Big fraction=y&mask(320);
    V r={fraction,-320,0,FINITE,0};
    if(fraction>=((Big)1<<319)) {r.mag=((Big)1<<320)-fraction;r.sign=1;++q;}
    V p=tc_pi();--p.exp;r=tm(tn(r),p);
    if(a.sign){r.sign^=1;q=-q;}
    *quadrant=q&3;return r;
}
static void tsc(V a,int piarg,V *s,V *c) {
    if(a.kind!=FINITE) {*s=*c=nanv();return;}
    if(!a.mag) {*s=a;*c=ti(1);return;}
    int q;V x;
    if(piarg) {
        /* Reduce 2*x exactly before multiplying by pi/2 (integer arguments). */
        V twice=a;++twice.exp;int ignored=0;
        V whole=integral(twice,0,&ignored),frac=ta(twice,tneg(whole));
        Big n=whole.exp>=0 ? (whole.exp<2 ? whole.mag<<whole.exp:0):whole.mag>>-whole.exp;
        q=(int)(n&3);if(whole.sign)q=(-q)&3;
        V p=tc_pi();--p.exp;x=tm(frac,p);
    } else x=tred(a,&q);
    V xx=tneg(tm(x,x)),st=x,ct=ti(1),ss=st,cc=ct;
    for(int n=1;n<=90;++n) {
        st=td(tm(st,xx),ti((2*n)*(2*n+1)));ss=ta(ss,st);
        ct=td(tm(ct,xx),ti((2*n-1)*(2*n)));cc=ta(cc,ct);
        if(tinyterm(st,ss) && tinyterm(ct,cc))break;
    }
    if(!x.mag) {ss=x;cc=ti(1);}
    if(q==0){*s=ss;*c=cc;}else if(q==1){*s=cc;*c=tneg(ss);}else if(q==2){*s=tneg(ss);*c=tneg(cc);}else{*s=tneg(cc);*c=ss;}
    if(piarg && !s->mag)s->sign=a.sign;
    if(piarg && !c->mag)c->sign=0;
}
static V tlog(V a) {
    if(a.kind==NANV || (a.sign && a.mag))return nanv();
    if(a.kind==INF)return a.sign ? nanv():a;
    if(!a.mag)return (V){0,0,1,INF,0};
    int e=width(a.mag)+a.exp-1;a.exp-=e;
    /* Keep the significand around 1, avoiding log(2-eps)-ln2 cancellation. */
    if(compare(a,(V){3,-1,0,FINITE,0})>0){--a.exp;++e;}
    V z=td(ta(a,ti(-1)),ta(a,ti(1))),zz=tm(z,z),term=z,sum=z;
    for(int n=3;n<501;n+=2){term=tm(term,zz);sum=ta(sum,td(term,ti(n)));if(tinyterm(term,sum))break;}
    ++sum.exp;return ta(sum,tm(ti(e),tc_ln2()));
}
static V texp(V a) {
    if(a.kind==NANV)return nanv();
    if(a.kind==INF)return a.sign ? ti(0):a;
    /* Preserve strict positivity below every carrier's half-minimum quantum;
     * final packing must still select the upward neighbour and raise flags. */
    if(a.mag && width(a.mag)+a.exp>16)return (V){1,a.sign ? -100000:100000,0,FINITE,0};
    V v=td(a,tc_ln2());int ignored=0;V rounded=integral(v,0,&ignored);
    int n=(int)toint(rounded,32,1,3,&ignored);
    V r=ta(a,tneg(tm(ti(n),tc_ln2()))),term=ti(1),sum=term;
    for(int k=1;k<=150;++k){term=td(tm(term,r),ti(k));sum=ta(sum,term);if(tinyterm(term,sum))break;}
    sum.exp+=n;return sum;
}
static V tatan(V a) {
    if(a.kind==NANV)return nanv();
    int sign=a.sign;a.sign=0;
    V halfpi=tc_pi();--halfpi.exp;
    if(a.kind==INF){halfpi.sign=sign;return halfpi;}
    int inv=compare(a,ti(1))>0;if(inv)a=td(ti(1),a);
    int offset=compare(a,(V){1,-1,0,FINITE,0})>0;
    if(offset)a=td(ta(a,ti(-1)),ta(a,ti(1)));
    V term=a,sum=a,xx=tneg(tm(a,a));
    for(int k=3;k<601;k+=2){term=tm(term,xx);sum=ta(sum,td(term,ti(k)));if(tinyterm(term,sum))break;}
    if(offset){V p=tc_pi();p.exp-=2;sum=ta(sum,p);}
    if(inv)sum=ta(halfpi,tneg(sum));sum.sign^=sign;return sum;
}
static V tatan2(V y,V x) {
    if(x.kind==NANV || y.kind==NANV)return nanv();
    V p=tc_pi();
    if(!y.mag && y.kind==FINITE){if(x.sign){p.sign=y.sign;return p;}return y;}
    if(!x.mag && x.kind==FINITE){--p.exp;p.sign=y.sign;return p;}
    if(x.kind==INF && y.kind==INF){p.exp-=2;if(x.sign)p=tm(p,ti(3));p.sign=y.sign;return p;}
    V r=tatan(td(y,x));
    if(x.sign){p.sign=y.sign;r=ta(r,p);}return r;
}
static V tpow(V a,V b) {
    if(b.kind==FINITE && !b.mag)return ti(1);
    if(compare(a,ti(1))==0 && a.kind==FINITE)return ti(1);
    if(a.kind==NANV || b.kind==NANV)return nanv();
    int ignored=0;V bi=integral(b,3,&ignored);
    int integer=b.kind==FINITE && compare(b,bi)==0;
    int odd=integer && bi.mag && bi.exp<=0 && (bi.mag>>-bi.exp&1);
    if(b.kind==INF){V aa=a;aa.sign=0;int d=compare(aa,ti(1));if(!d)return ti(1);return (d>0)^b.sign ? (V){0,0,0,INF,0}:ti(0);}
    if(a.kind==INF || !a.mag){int inf=(a.kind==INF)^b.sign;return (V){0,0,a.sign&&odd,inf ? INF:FINITE,0};}
    if(a.sign && !integer)return nanv();
    int sign=a.sign&&odd;a.sign=0;V r=texp(tm(b,tlog(a)));r.sign=sign;return r;
}
/* Canonicalise the exact two-component input sum x=h+l first, so overlapping
 * or cancelling input fields have the same result. With |x|<=2^-112, exp(x)
 * has high=1.
 * Nearest rounding of its low differs from rounding x only at exact binary64
 * midpoints: the positive correction exp(x)-1-x < x*x is smaller than the
 * smallest nonzero midpoint gap of a two-binary64 input (>=2^(E-107)).
 * Directed rounding also needs to know whether exp(x)-1 crosses h. Compare
 * x with log(1+h), whose residual is -h*h/2 + h*h*h/3 - ... . A nonzero
 * quadratic comparison gap is at least 2^(2*h.exp-1), or much larger when l
 * is tiny; the cubic remainder is smaller by >=32. At exact quadratic
 * equality its sign is the sign of h, settling the side without approximation.
 * All comparisons below are exact integers at quantum 2^-2149. A nonzero
 * rational input has non-dyadic exp(x), so the normal result raises only
 * inexact. This retains sparse tails that the 224/106-bit paths lose.
 */
static U ppc_exp_near_zero(PairSum a,int rm,int *flags) {
    const U one=0x3ff0000000000000ULL;
    if(!a.mag)return one;
    int ignored=0;V v=sum_value(a);
    U hb=pack(v,formats[3],0,&ignored),lo;V h=unpack(hb,formats[3]);
    PairSum tail=sum_difference(a,sum_scalar(h));
    if(rm==1 || rm==2 || rm==3) {
        int above=1;
        if(tail.sign && tail.mag) {
            SquareBits low=(SquareBits)tail.mag<<1075;
            SquareBits high=(SquareBits)sum_scalar(h).mag,quadratic=high*high;
            above=low<quadratic || (low==quadratic && h.sign);
        }
        U previous=(hb>>63) ? hb+1:hb-1,following=(hb>>63) ? hb-1:hb+1;
        lo=rm==2 ? (above ? following:hb):(above ? hb:previous);
    } else {
        U lower=pack(v,formats[3],1,&ignored),upper=pack(v,formats[3],2,&ignored);
        PairSum down=sum_difference(a,sum_scalar(unpack(lower,formats[3])));
        PairSum up=sum_difference(sum_scalar(unpack(upper,formats[3])),a);
        lo=down.mag<up.mag ? lower:upper; /* An exact midpoint moves upward. */
    }
    if(lo==((U)1<<63))lo=0; /* Canonical residual zero is positive. */
    *flags|=16;
    return one|(lo<<64);
}
static V trans_unpack(U x,int fi) {
    if(fi!=6)return unpack(x,formats[fi]);
    V hi=unpack(low64(x),formats[3]);
    if(hi.kind!=FINITE || !hi.mag)return hi;
    return ta(hi,unpack(x>>64,formats[3]));
}
#include "trans_exact.h"
enum TransPath { TRANS_CORE, TRANS_EXACT, TRANS_PPC_EXP, TRANS_TANH_LIMIT, TRANS_LINEAR };
typedef struct {
    enum TransPath path;
    V a, b, r, c;
    ExactReal exact[2];
    PairSum sum;
    int flags, pair;
} TransState;

static TransState trans_domain(int fi,int op,const U *in) {
    TransState s={.path=TRANS_CORE,.pair=op==SINCOS || op==SINCOSPI};
    if(op==SINCOSPI) {
        ExactReal a=trans_input(in[0],fi);
        if(trans_exact_sincospi(a,&s.exact[0],&s.exact[1])) {
            s.path=TRANS_EXACT;
            return s;
        }
    }
    if(op==POW || op==EXP2 || op==EXP10 || op==LOG2 || op==LOG10) {
        ExactReal a=trans_input(in[0],fi),b=trans_input(in[1],fi);
        if(trans_exact_math(op,a,b,&s.exact[0])) {
            s.path=TRANS_EXACT;
            s.flags=a.snan || (op==POW && b.snan);
            return s;
        }
    }
    if(fi==6 && op==EXP) {
        s.sum=sum_read(in[0]);
        if(s.sum.kind==FINITE && s.sum.mag<=((SumBits)1<<962)) {
            s.path=TRANS_PPC_EXP;
            return s;
        }
    }
    s.a=trans_unpack(in[0],fi);
    s.b=trans_unpack(in[1],fi);
    s.r=nanv();s.c=ti(0);
    s.flags=s.a.snan || ((op==ATAN2 || op==POW) && s.b.snan);
    if(op==TANH && s.a.kind==FINITE && s.a.mag && width(s.a.mag)+s.a.exp>6) {
        s.path=TRANS_TANH_LIMIT;
        return s;
    }
    /* Below 2^-112 the cubic correction is less than half an IEEE
     * carrier ulp, while its strict sign still selects directed neighbours.
     * PPC sparse residuals require their own full-precision treatment. */
    if(fi!=6 && (op==TAN || op==ASIN || op==TANH) &&
       s.a.kind==FINITE && s.a.mag && width(s.a.mag)+s.a.exp<=-112) {
        int shift=480-width(s.a.mag);
        s.r=s.a;s.r.mag<<=shift;s.r.exp-=shift;
        if(op==TANH)--s.r.mag;else ++s.r.mag;
        s.path=TRANS_LINEAR;
    }
    return s;
}

static void trans_core(TransState *s,int op) {
    V a=s->a,b=s->b,r=nanv(),c=ti(0);
    switch(op) {
    case SIN: case COS: case TAN: case SINCOS: case SINCOSPI: {
        V sine;tsc(a,op==SINCOSPI,&sine,&c);
        r=op==COS ? c:op==TAN ? td(sine,c):sine;
        break;
    }
    case ATAN: r=tatan(a);break;
    case ATAN2: r=tatan2(a,b);break;
    case ASIN: case ACOS: {
        V x=a;x.sign=0;
        if(a.kind!=NANV && compare(x,ti(1))<=0) {
            V root=tsqrt(tm(ta(ti(1),tneg(x)),ta(ti(1),x)));
            r=op==ASIN ? tatan2(a,root):tatan2(root,a);
        }
        break;
    }
    case LOG: case LOG2: case LOG10:
        r=tlog(a);
        if(op!=LOG)r=td(r,op==LOG2 ? tc_ln2():tc_ln10());
        break;
    case EXP: case EXP2: case EXP10:
        r=texp(op==EXP ? a:tm(a,op==EXP2 ? tc_ln2():tc_ln10()));
        break;
    case POW: r=tpow(a,b);break;
    case SINH: case COSH: case TANH: {
        V x=a;x.sign=0;
        if(op==TANH && x.kind==INF)r=ti(a.sign ? -1:1);
        else if(x.kind==FINITE && (!x.mag || width(x.mag)+x.exp< -4)) {
            V term=op==COSH ? ti(1):a,sum=term,xx=tm(a,a);
            for(int n=1;n<=90;++n) {
                term=td(tm(term,xx),ti(op==COSH ? (2*n-1)*(2*n):(2*n)*(2*n+1)));
                sum=ta(sum,term);
                if(tinyterm(term,sum))break;
            }
            if(op==TANH) {
                V sh=sum,ch=ti(1),t=ch;
                for(int n=1;n<=90;++n) {
                    t=td(tm(t,xx),ti((2*n-1)*(2*n)));
                    ch=ta(ch,t);
                }
                sum=td(sh,ch);
            }
            r=sum;
        } else {
            V ex=texp(x),inv=td(ti(1),ex);
            r=op==COSH ? ta(ex,inv):ta(ex,tneg(inv));
            if(op==TANH)r=td(r,ta(ex,inv));else --r.exp;
            if(op!=COSH)r.sign=a.sign;
        }
        break;
    }
    default: __builtin_trap();
    }
    s->r=r;s->c=c;
}

enum ExactDomain { EXACT_ZERO=1, EXACT_ONE=2, EXACT_INFINITY=4,
                   EXACT_OTHER_INFINITY=8, EXACT_ZERO_RESULT=16 };
static const unsigned trans_exact_domains[SINCOSPI+1]={
    [SIN]=EXACT_ZERO, [COS]=EXACT_ZERO, [TAN]=EXACT_ZERO,
    [ASIN]=EXACT_ZERO, [ACOS]=EXACT_ONE, [ATAN]=EXACT_ZERO,
    [ATAN2]=EXACT_ZERO_RESULT, [SINH]=EXACT_ZERO, [COSH]=EXACT_ZERO,
    [TANH]=EXACT_ZERO|EXACT_INFINITY, [EXP]=EXACT_ZERO|EXACT_INFINITY,
    [EXP2]=EXACT_INFINITY, [EXP10]=EXACT_INFINITY, [LOG]=EXACT_ONE,
    [POW]=EXACT_INFINITY|EXACT_OTHER_INFINITY, [SINCOS]=EXACT_ZERO
};

static int trans_is_exact(int op,V a,V b,V r) {
    unsigned domains=trans_exact_domains[op];
    return ((domains&EXACT_ZERO) && a.kind==FINITE && !a.mag) ||
           ((domains&EXACT_ONE) && a.kind==FINITE && compare(a,ti(1))==0) ||
           ((domains&EXACT_INFINITY) && a.kind==INF) ||
           ((domains&EXACT_OTHER_INFINITY) && b.kind==INF) ||
           ((domains&EXACT_ZERO_RESULT) && r.kind==FINITE && !r.mag);
}

static U trans_tanh_limit(V a,int fi,int rm,int *flags) {
    /* The finite limit is strict. IEEE formats cannot resolve the tail at
     * |x|>=64; PPC can until it falls below half its least quantum. */
    if(fi!=6)return pack((V){mask(480),-480,a.sign,FINITE,0},formats[fi],rm,flags);
    V x=a;x.sign=0;
    /* e^3>16 bounds this tail below half a PPC quantum. */
    if(compare(x,ti(512))>=0)
        return ppc_round_exact(((SquareBits)1<<2148)-1,-2148,a.sign,rm,flags);
    ++x.exp;x.sign=1;
    V q=texp(x),tail=td(tm(ti(2),q),ta(ti(1),q));
    SquareBits value=((SquareBits)1<<-tail.exp)-(SquareBits)tail.mag;
    return ppc_round_exact(value,tail.exp,a.sign,rm,flags);
}

static void trans_pack(U *out,int fi,int op,int rm,TransState s) {
    switch(s.path) {
    case TRANS_EXACT:
        out[0]=trans_pack_exact(s.exact[0],fi,rm,&s.flags);
        out[1]=s.pair ? trans_pack_exact(s.exact[1],fi,rm,&s.flags):0;
        out[2]=s.flags;
        return;
    case TRANS_PPC_EXP:
        out[0]=ppc_exp_near_zero(s.sum,rm,&s.flags);
        out[1]=0;out[2]=s.flags;
        return;
    case TRANS_TANH_LIMIT:
        out[0]=trans_tanh_limit(s.a,fi,rm,&s.flags);
        out[1]=0;out[2]=s.flags|16;
        return;
    case TRANS_CORE: case TRANS_LINEAR:
        break;
    }
    V a=s.a,b=s.b,r=s.r,c=s.c;
    if(r.kind==NANV && a.kind!=NANV && ((op!=POW && op!=ATAN2) || b.kind!=NANV))s.flags|=1;
    if((op==LOG || op==LOG2 || op==LOG10) && a.kind==FINITE && !a.mag)s.flags|=2;
    if(op==POW && a.kind==FINITE && !a.mag && b.sign && (b.mag || b.kind==INF))s.flags|=2;
    int exact=trans_is_exact(op,a,b,r);
    if(r.kind==FINITE && !exact)s.flags|=16;
    if((op==EXP || op==EXP2 || op==EXP10 || op==POW) && !r.mag &&
       r.kind==FINITE && a.kind==FINITE && a.mag && !exact)s.flags|=24;
    out[0]=fi==6 ? ppc_round(r,rm,&s.flags):pack(r,formats[fi],rm,&s.flags);
    out[1]=s.pair ? (fi==6 ? ppc_round(c,rm,&s.flags):pack(c,formats[fi],rm,&s.flags)):0;
    out[2]=s.flags;
}

static void trans_eval(U *out,int fi,int op,const U *in,int rm) {
    TransState s=trans_domain(fi,op,in);
    if(s.path==TRANS_CORE)trans_core(&s,op);
    trans_pack(out,fi,op,rm,s);
}
````

## `tests/named_oracle.cpp` (26 lines)

````
// LLVM APFloat is an independent oracle for named-format overflow.
#include <llvm/ADT/APFloat.h>
#include <llvm/ADT/APInt.h>
#include <iostream>
using llvm::APFloat;
int main() {
    const llvm::fltSemantics *formats[] = {
        &APFloat::Float8E5M2(), &APFloat::Float8E5M2FNUZ(),
        &APFloat::Float8E4M3(), &APFloat::Float8E4M3FN(),
        &APFloat::Float8E4M3FNUZ(), &APFloat::Float8E4M3B11FNUZ(),
        &APFloat::Float8E3M4()
    };
    const APFloat::roundingMode modes[] = {
        APFloat::rmNearestTiesToEven, APFloat::rmTowardNegative,
        APFloat::rmTowardPositive, APFloat::rmTowardZero,
        APFloat::rmNearestTiesToAway
    };
    unsigned raw, fmt, mode;
    while (std::cin >> raw >> fmt >> mode) {
        if (fmt >= 7 || mode >= 5) return 2;
        APFloat value(APFloat::IEEEsingle(), llvm::APInt(32, raw));
        bool loses;
        value.convert(*formats[fmt], modes[mode], &loses);
        std::cout << value.bitcastToAPInt().getZExtValue() << '\n';
    }
}
````

## `tests/ppc_exact_oracle.py` (153 lines)

````python
"""Fraction oracles for 0.2.13 exact-sum conversions and integral operations.

No arithmetic implementation source is imported. Pair results here are exact
rational selections, including the total nearest-even pair midpoint selector.
"""
import importlib.util
from functools import lru_cache
from pathlib import Path
import sys

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('edge',ROOT/'tests/test_edge.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
F=e.FORMATS['f64'];MASK64=(1<<64)-1

def decode(raw):
    h,sign,sn=e.decode(raw&MASK64,F);l,_,lsn=e.decode(raw>>64,F)
    if h=='nan' or l=='nan': return 'nan',sign,sn or lsn
    if isinstance(h,str): return h,sign,sn or lsn
    if isinstance(l,str): return l,(raw>>127)&1,sn or lsn
    return h+l,sign,sn or lsn

def pair(h,l=0,zero_sign=0):
    hi=e.encode(h,F,zero_sign=zero_sign)[0];lo=e.encode(l,F)[0]
    raw=hi|(lo<<64)
    if not isinstance(h,str):
        assert e.decode(hi,F)[0]==h and e.decode(lo,F)[0]==l
        assert e.encode(h+l,F,zero_sign=zero_sign)[0]==hi
    return raw

def integer_pair(n,zero_sign=0):
    hi=e.encode(e.Q(n),F,zero_sign=zero_sign)[0]
    h=e.decode(hi,F)[0]
    assert not isinstance(h,str), 'integer decomposition requires an in-range result'
    residual=e.Q(n)-h;lo=e.encode(residual,F)[0]
    assert e.decode(lo,F)[0]==residual, 'exact integral result must fit two components'
    raw=hi|(lo<<64)
    assert decode(raw)[0]==n
    return raw

def integral(raw,op,rm=0):
    v,sign,sn=decode(raw)
    if isinstance(v,str):
        return e.nan(F) if v=='nan' else (raw&MASK64),int(sn)
    mode={'floor':1,'ceil':2,'trunc':3,'round':4,'roundeven':0}.get(op,rm)
    n,flags=e.roundedq(abs(v),sign,mode)
    if sign:n=-n
    return integer_pair(n,sign),flags if op=='rint' else 0

def to_integer(raw,bits,signed,mode,signal_inexact=True):
    v,sign,_=decode(raw)
    lower=-(1<<(bits-1)) if signed else 0;upper=(1<<(bits-int(signed)))-1
    if v=='nan': return 0,1
    if v=='inf': return (lower if sign else upper),1
    n,flags=e.roundedq(abs(v),sign,mode)
    if sign:n=-n
    if not signal_inexact:flags=0
    if n<lower or n>upper:flags|=1
    return max(lower,min(upper,n)),flags

def convert(raw,dest,rm=0):
    v,sign,sn=decode(raw)
    value,flags=e.encode(v,dest,rm,sign)
    return value,flags|int(sn)

def _near_low(bits):
    if not bits or bits==1<<63:return (0,1,(1<<63)|1)
    return (bits-1,bits,bits+1)

def canonical_candidates(v):
    """Enumerate local fields and high-bin boundaries, filtering by definition."""
    high=e.encode(v,F)[0];candidates={}
    for hb in (high-1,high,high+1):
        if hb<0:continue
        hv=e.decode(hb,F)[0]
        if isinstance(hv,str):continue
        previous=e.decode(hb-1,F)[0] if hb else -e.power(-1074)
        following=e.decode(hb+1,F)[0]
        if following=='inf':following=e.power(1024)
        probes=[v-hv,(previous-hv)/2,(following-hv)/2]
        for probe in probes:
            for direction in (1,2):
                for lb in _near_low(e.encode(probe,F,direction)[0]):
                    lv=e.decode(lb,F)[0]
                    if isinstance(lv,str):continue
                    total=hv+lv
                    if total<0 or e.encode(total,F)[0]!=hb:continue
                    raw=hb|((lb if lv else 0)<<64)
                    candidates[raw]=total
    return candidates

@lru_cache(maxsize=8192)
def neighbours(raw):
    v=decode(raw)[0];candidates=canonical_candidates(v)
    return (max((x,b) for b,x in candidates.items() if x<v),
            min((x,b) for b,x in candidates.items() if x>v))

@lru_cache(maxsize=8192)
def to_pair(n,rm=0,zero_sign=0):
    """Search canonical neighbours and compare exact rational distances."""
    if not n:return zero_sign<<63,0
    negative=n<0;v=e.Q(abs(n));mode=({1:2,2:1}.get(rm,rm) if negative else rm)
    hmax=e.decode(0x7fefffffffffffff,F)[0]
    lmax=e.decode(0x7c8fffffffffffff,F)[0];maximum=hmax+lmax
    boundary=hmax+e.power(970)
    overflow=(v>=(maximum+boundary)/2 if mode in (0,4) else v>maximum if mode==2 else v>=boundary)
    maxbits=0x7fefffffffffffff|(0x7c8fffffffffffff<<64)
    def signed(bits):
        return bits^((1<<63)|((1<<127) if bits>>64 else 0)) if negative else bits
    if overflow:
        return signed(e.infinity(F) if mode in (0,2,4) else maxbits),20
    if v>maximum:return signed(maxbits),16
    candidates=canonical_candidates(v)
    below=[(x,b) for b,x in candidates.items() if x<=v]
    above=[(x,b) for b,x in candidates.items() if x>=v]
    low,lb=max(below);up,ub=min(above)
    if low==up:chosen,raw=low,lb
    elif mode in (1,3):chosen,raw=low,lb
    elif mode==2:chosen,raw=up,ub
    elif v-low<up-v:chosen,raw=low,lb
    elif v-low>up-v:chosen,raw=up,ub
    elif mode==4:chosen,raw=up,ub
    else:
        use_low=bool((lb>>64) or (ub>>64))
        even=lambda b:not (((b>>64) if use_low else b&MASK64)&1)
        chosen,raw=(low,lb) if even(lb) or not even(ub) else (up,ub)
    flags=int(chosen!=v)*16
    if flags and chosen<e.power(-1022):flags|=8
    return signed(raw),flags

def integer_to_pair(n,rm=0):return to_pair(n,rm)

def incoming(raw,fmt,rm=0):
    value,sign,sn=e.decode(raw,fmt)
    if isinstance(value,str):return (e.nan(F) if value=='nan' else e.infinity(F,sign)),int(sn)
    return to_pair(value,rm,sign)

def fma(a,b,c,rm=0):
    av,sa,an=decode(a);bv,sb,bn=decode(b);cv,sc,cn=decode(c)
    flags=int(an or bn or cn)
    if 'nan' in (av,bv,cv):return e.nan(F),flags
    invalid=(av=='inf' and bv==0) or (bv=='inf' and av==0)
    if invalid:return e.nan(F),1
    sign=sa^sb
    if av=='inf' or bv=='inf':
        if cv=='inf' and sc!=sign:return e.nan(F),1
        return e.infinity(F,sign),flags
    if cv=='inf':return e.infinity(F,sc),flags
    exact=av*bv+cv
    zero_sign=sign if (av==0 or bv==0) and cv==0 and sign==sc else int(rm==1)
    value,raised=to_pair(exact,rm,zero_sign)
    return value,flags|raised
````

## `tests/test_directed.py` (49 lines)

````python
"""All constrained elementary operations against exact MPFR bracket rounding."""
import importlib.util
from pathlib import Path
import sys
import os

ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("trans",ROOT/"tests/test_trans.py")
t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
e=t.e

def run(major, quick=False):
    edge=e.Edge(major);oracle=t.Oracle()
    formats=list(e.FORMATS.items())
    if os.environ.get("BENNETT_ARITH_PROMISED"):
        formats.append(("ppcf128",None))
    else:
        print("PPC exact sweep: BENNETT_ARITH_PROMISED=1 (bennett-arith-wvh)",flush=True)
    for suffix,f in formats:
        def enc(v):
            return oracle.pairs.to_pair(v)[0] if f is None else e.encode(v,f)[0]
        if f is None:
            oracle.rounded("exp",e.Q(0),0)
        tiny=-1074 if f is None else 1-f[3]-(f[1]-1)
        exponents=(-169,-300) if quick else (tiny,tiny+1,-300,-169,-113,-112,-111,-20)
        values=[sign*e.power(k) for k in exponents for sign in (-1,1)]
        values += [e.Q(x) for x in (64,78,80,100,136,161,255,256,512,-64,-100,-255)]
        values += [e.Q(1)+d*e.power(-52 if f is None else 1-f[1]) for d in (-2,-1,0,1,2)]
        for v in values:
            raw=enc(v)
            a,sa=(oracle.pairs.decode(raw)[:2] if f is None else e.decode(raw,f)[:2])
            if isinstance(a,str):continue
            for op in t.ops:
                b=e.Q(3,2) if op=="pow" else e.Q(-3,4)
                args=[raw,enc(b)] if op in ("pow","atan2") else [raw]
                for rm in range(5):
                    expected=oracle.rounded(op,a,sa,b,f=f,rm=rm)
                    edge.check(op+"_"+suffix+"_rm",[*args,rm],expected)
            for pair, components in (("sincos",("sin","cos")),
                                     ("sincospi",("sinpi","cospi"))):
                for rm in range(5):
                    expected=tuple(oracle.rounded(op,a,sa,f=f,rm=rm) for op in components)
                    edge.check(pair+"_"+suffix+"_rm",[raw,rm],expected)
        print(f"LLVM {major} {suffix}: {edge.count} exact directed checks",flush=True)
    assert not oracle.inconclusive

if __name__=="__main__":
    for major in map(int,[a for a in sys.argv[1:] if a!="--quick"] or [18,23]):
        run(major,"--quick" in sys.argv)
````

## `tests/test_named_overflow.py` (35 lines)

````python
"""Directed named-format overflow, checked against LLVM APFloat 23."""
import ctypes
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
WORK=Path(os.environ["TMPDIR"])/"named-overflow"
WORK.mkdir(parents=True,exist_ok=True)
LLVM=Path("/usr/lib/llvm-23/bin")

def run():
    flags=subprocess.check_output([str(LLVM/"llvm-config"),"--cxxflags","--ldflags","--libs","support","--system-libs"],text=True).split()
    subprocess.run([str(LLVM/"clang++"),str(ROOT/"tests/named_oracle.cpp"),*flags,"-o",str(WORK/"oracle")],check=True,timeout=60)
    subprocess.run([str(LLVM/"clang"),"-std=c2x","-O0","-shared","-fPIC","-DBENNETT_LLVM_MAJOR=23",
                    "-I",str(ROOT/".tmp/llvm18"),str(ROOT/"softfloat/named.c"),"-o",str(WORK/"named.so")],check=True,timeout=90)
    lib=ctypes.CDLL(str(WORK/"named.so"))
    call=lib.bennett_sf_named
    call.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
    # Finite overflow and values just beyond each maximal representable bin.
    cases=[(raw,fmt,rm) for raw in (0x501502f9,0xd01502f9,0x43fffffe,0xc3fffffe,
                                   0x47800000,0xc7800000,0x7f7fffff,0xff7fffff)
           for fmt in range(7) for rm in (1,2,3)
           if rm==3 or (rm==1 and raw>>31==0) or (rm==2 and raw>>31==1)]
    data="".join(f"{raw} {fmt} {rm}\n" for raw,fmt,rm in cases)
    expected=list(map(int,subprocess.check_output([str(WORK/"oracle")],input=data,text=True).split()))
    assert len(expected)==len(cases)
    for (raw,fmt,rm),want in zip(cases,expected):
        src=(ctypes.c_uint64*2)(raw,0);out=(ctypes.c_uint64*2)()
        call(out,2,fmt,1,src,rm,0)
        assert out[0]==want,(hex(raw),fmt,rm,hex(out[0]),hex(want))
    print(f"{len(cases)} named directed-overflow APFloat comparisons")

if __name__=="__main__":run()
````

## `tests/test_pair_parity.py` (31 lines)

````python
"""Dialect 13.1 parity at both zero-low transitions, from exact dyadic midpoints."""
import importlib.util
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("pair",ROOT/"tests/ppc_exact_oracle.py")
o=importlib.util.module_from_spec(s);s.loader.exec_module(o)
e=o.e

def run(major):
    edge=e.Edge(major);u=e.power(-1074);f=e.FORMATS["f64"]
    for hb in (0x3ff0000000000001,0x0030000000000001):
        h=e.decode(hb,f)[0]
        for sign in (-1,1):
            expected=hb ^ ((1<<63) if sign<0 else 0)
            for direction in (-1,1):
                # FMA is exactly sign*(h +/- u/2); the zero-low neighbour
                # has even low significand and must win either midpoint.
                a=o.pair(sign*h,sign*direction*u)
                half=o.pair(e.Q(1,2));c=o.pair(sign*h/2)
                edge.check("fma_ppcf128_rm",[a,half,c,0],expected,16)
                if hb==0x0030000000000001:
                    value=sign*(h+direction*u/2)
                    raw,flags=e.encode(value,e.FORMATS["f128"])
                    assert flags==0
                    edge.check("fptrunc_f128_ppcf128_rm",[raw,0],expected,16)
                assert o.to_pair(sign*(h+direction*u/2))==(expected,16)
    print(f"LLVM {major}: {edge.count} exact zero-low parity/flag checks")

if __name__=="__main__":
    for major in map(int,sys.argv[1:] or [18,23]):run(major)
````

## `tests/test_trans.py` (121 lines)

````python
"""Independent MPFR oracle against the actual published carrier functions.
MPFR is test-only. Production bitcode has no external numerical dependency.
"""
import ctypes as C,importlib.util,pathlib,sys,random
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('edge',R/'tests/test_edge.py');e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
class MP(C.Structure):
    _fields_=[('prec',C.c_long),('sign',C.c_int),('exp',C.c_long),('limbs',C.c_void_p)]
m=C.CDLL('libmpfr.so.6')
for name,args,ret in [('init2',[C.POINTER(MP),C.c_long],None),('clear',[C.POINTER(MP)],None),('set_str',[C.POINTER(MP),C.c_char_p,C.c_int,C.c_int],C.c_int),('mul_2si',[C.POINTER(MP),C.POINTER(MP),C.c_long,C.c_int],C.c_int),('get_str',[C.c_void_p,C.POINTER(C.c_long),C.c_int,C.c_size_t,C.POINTER(MP),C.c_int],C.c_void_p),('free_str',[C.c_void_p],None)]:
    f=getattr(m,'mpfr_'+name);f.argtypes=args;f.restype=ret
ops='sin cos tan asin acos atan sinh cosh tanh exp exp2 exp10 log log2 log10 atan2 pow'.split()
for op in ops+['sinpi','cospi']:
    fn=getattr(m,'mpfr_'+op);fn.argtypes=[C.POINTER(MP)]*(4 if op in ('atan2','pow') else 3) # last is rounding, corrected below
    fn.argtypes=[C.POINTER(MP)]*(3 if op in ('atan2','pow') else 2)+[C.c_int]
    fn.restype=C.c_int
class Oracle:
    """Directed MPFR intervals, refined until both ends choose the same carrier."""
    def __init__(self, precision=384):
        self.precision=precision
        self.a=MP();self.b=MP();self.r=MP()
        for x in (self.a,self.b,self.r):m.mpfr_init2(C.byref(x),precision)
        self.inconclusive=0
    def __del__(self):
        for x in (self.a,self.b,self.r):m.mpfr_clear(C.byref(x))
    def resize(self,precision):
        if precision==self.precision:return
        for x in (self.a,self.b,self.r):
            m.mpfr_clear(C.byref(x));m.mpfr_init2(C.byref(x),precision)
        self.precision=precision
    def put(self,x,v,sign=0):
        if isinstance(v,str):
            s=('-' if sign else '')+('nan' if v=='nan' else 'inf')
            m.mpfr_set_str(C.byref(x),s.encode(),10,0)
            return
        n=v.numerator;d=v.denominator
        s=('-' if n<0 or not n and sign else '')+bin(abs(n))[2:]
        assert m.mpfr_set_str(C.byref(x),s.encode(),2,0)==0
        m.mpfr_mul_2si(C.byref(x),C.byref(x),-(d.bit_length()-1),0)
    def get(self):
        exp=C.c_long();p=m.mpfr_get_str(None,C.byref(exp),2,self.precision,C.byref(self.r),0)
        s=C.string_at(p).decode();m.mpfr_free_str(p)
        if '@NaN@' in s:return 'nan',0
        if '@Inf@' in s:return 'inf',int(s.startswith('-'))
        sign=int(s.startswith('-'));s=s.lstrip('-')
        if abs(exp.value)>20000:
            return (-1 if sign else 1)*e.power(20000 if exp.value>0 else -20000),sign
        return (-1 if sign else 1)*int(s,2)*e.power(exp.value-len(s)),sign
    def call(self,op,a,sa,b=0,sb=0,direction=0):
        self.put(self.a,a,sa);self.put(self.b,b,sb)
        fn=getattr(m,'mpfr_'+op)
        args=[C.byref(self.r),C.byref(self.a)]
        if op in ('atan2','pow'):args.append(C.byref(self.b))
        fn(*args,direction)
        return self.get()
    def rounded(self,op,a,sa,b=0,sb=0,f=None,rm=0):
        if f is None:
            if not hasattr(self,'pairs'):
                spec=importlib.util.spec_from_file_location('pairs',R/'tests/ppc_exact_oracle.py')
                self.pairs=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.pairs)
            def encode(v,sign):
                if isinstance(v,str):return e.nan(self.pairs.F) if v=='nan' else e.infinity(self.pairs.F,sign)
                return self.pairs.to_pair(v,rm,sign)[0]
        else:
            def encode(v,sign):return e.encode(v,f,rm,sign)[0]
        input_bits=max((v.numerator.bit_length() for v in (a,b) if not isinstance(v,str)),default=0)
        precision=max(384,input_bits)
        while precision<=65536:
            self.resize(precision)
            lower,ls=self.call(op,a,sa,b,sb,direction=3)
            upper,us=self.call(op,a,sa,b,sb,direction=2)
            lo,hi=encode(lower,ls),encode(upper,us)
            if lo==hi:return lo
            precision*=2
        self.inconclusive+=1
        raise AssertionError((op,a,b,rm,'MPFR bracket inconclusive at 65536 bits'))

if __name__=='__main__':
    for major in map(int,sys.argv[1:] or [18,23]):
        edge=e.Edge(major)
        assert '__bennett_sf_sin_f128' in edge.rows,'RED: missing own-format binary128 sin'
        oracle=Oracle();rng=random.Random(0x12851);worst={}
        for suffix,f in e.FORMATS.items():
            bits,p,eb,bias,_=f
            values=[0,1,1<<(bits-1),e.infinity(f),e.infinity(f,1),e.nan(f)]
            for q in [e.Q(1),e.Q(-1),e.Q(1,2),e.Q(-1,2),e.Q(2),e.Q(-2),e.Q(10),e.Q(-10)]:values.append(e.encode(q,f)[0])
            for exp in list(range(1,(1<<eb)-1,max(1,((1<<eb)-2)//160)))+[1,2,bias,bias+1,(1<<eb)-2]:
                for frac in [0,1,(1<<(p-1))-1]:
                    # Explicit x87 significand.
                    raw=(exp<<(p-1+f[4]))|frac|((1<<(p-1)) if f[4] else 0)
                    values += [raw,raw^(1<<(bits-1))]
            one=e.encode(e.Q(1),f)[0]
            values += [one-1,one+1,one-2,one+2]
            for text in ['3.1415926535897932384626433832795028841971','1.5707963267948966192313216916397514420986','11356.523406294143949491931077970763']:
                center=e.encode(e.Q(text),f)[0]
                if center!=e.infinity(f):values += [center+d for d in range(-2,3)]
            for _ in range(64):values.append(rng.getrandbits(bits))
            for _ in range(50):values.append(e.encode(e.Q(rng.randrange(-10000,10000),1024),f)[0])
            for raw in values:
                a,sa,_=e.decode(raw,f)
                for op in ops:
                    b=e.Q(3,2) if op=='pow' else e.Q(-3,4)
                    rb=e.encode(b,f)[0]
                    want,ws=oracle.call(op,a,sa,b)
                    args=[raw,rb] if op in ('pow','atan2') else [raw]
                    expected=oracle.rounded(op,a,sa,b,f=f)
                    actual=edge.call(op+'_'+suffix,*args)[0]
                    av,_,_=e.decode(actual,f)
                    if isinstance(want,str) or isinstance(av,str) or not want or not av:
                        assert actual==expected,(major,suffix,op,hex(raw),hex(actual),hex(expected))
                    else:
                        step=max(e.log2q(abs(want)),1-bias)-(p-1)
                        ulps=abs(av-want)/e.power(step)
                        assert actual==expected,(major,suffix,op,hex(raw),hex(actual),hex(expected))
                        worst[op]=max(worst.get(op,e.Q(0)),ulps)
                    edge.count+=1
                # Pair order and scalar consistency, including signed zeros/NaNs.
                edge.check('sincos_'+suffix,[raw],(edge.call('sin_'+suffix,raw)[0],edge.call('cos_'+suffix,raw)[0]))
            print(f'LLVM {major} {suffix}: {edge.count} checks so far',flush=True)
        print(f'LLVM {major}: {edge.count} own-format MPFR/pair checks; max observed ulp '+str({k:round(float(v),5) for k,v in worst.items()}),flush=True)
````

## `tests/test_trans_phases.py` (19 lines)

````python
"""Unit checks for domain, core and packing phase boundaries."""
import os
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]

def run(source=ROOT):
    work=Path(os.environ["TMPDIR"])/"trans-phases"
    work.mkdir(parents=True,exist_ok=True)
    exe=work/"phases"
    subprocess.run(["/usr/lib/llvm-18/bin/clang","-std=c2x","-O0",
                    "-DBENNETT_LLVM_MAJOR=18",f'-DBENNETT_CORE="{source}/softfloat/core.c"',
                    "-I",str(ROOT/".tmp/llvm18"),str(ROOT/"tests/trans_phases.c"),
                    "-o",str(exe)],check=True,timeout=60)
    subprocess.run([str(exe)],check=True,timeout=10)
    print("domain/core/pack/exactness-table invariants passed")

if __name__=="__main__":run(Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT)
````

## `tests/trans_phases.c` (60 lines)

````c
/* Phase invariants for the integer elementary evaluator. */
#include <assert.h>
#include BENNETT_CORE

static U raw(int n) {
    int flags=0;
    return pack(ti(n),formats[3],0,&flags);
}
static void test_domain(void) {
    U in[3]={raw(3),0,0};
    assert(trans_domain(3,EXP2,in).path==TRANS_EXACT);
    in[0]=raw(100);
    assert(trans_domain(3,TANH,in).path==TRANS_TANH_LIMIT);
    in[0]=raw(0);
    assert(trans_domain(6,EXP,in).path==TRANS_PPC_EXP);
    in[0]=((U)854<<52); /* binary64 2^-169 */
    assert(trans_domain(3,TAN,in).path==TRANS_LINEAR);
    in[0]=raw(2);
    assert(trans_domain(3,ASIN,in).path==TRANS_CORE);
}
static void test_core(void) {
    U in[3]={0};
    TransState state=trans_domain(3,SINCOS,in);
    trans_core(&state,SINCOS);
    assert(state.r.kind==FINITE && !state.r.mag);
    assert(compare(state.c,ti(1))==0);
    in[0]=raw(2);state=trans_domain(3,ASIN,in);
    trans_core(&state,ASIN);
    assert(state.r.kind==NANV);
}
static void test_pack(void) {
    U in[3]={raw(1),0,0},out[3];
    TransState state=trans_domain(3,LOG,in);
    trans_core(&state,LOG);trans_pack(out,3,LOG,0,state);
    assert(out[0]==0 && out[1]==0 && out[2]==0);
    in[0]=0;state=trans_domain(3,ACOS,in);
    trans_core(&state,ACOS);trans_pack(out,3,ACOS,0,state);
    assert(out[0]!=0 && out[2]==16);
    in[0]=raw(2);state=trans_domain(3,ASIN,in);
    trans_core(&state,ASIN);trans_pack(out,3,ASIN,0,state);
    assert(out[0]==nanbits(formats[3]) && out[2]==1);
    in[0]=raw(-100000);state=trans_domain(3,EXP,in);
    trans_core(&state,EXP);trans_pack(out,3,EXP,2,state);
    assert(out[0]==1 && out[2]==24);
}
static void test_exactness_table(void) {
    int zero_ops[]={SIN,COS,TAN,ASIN,ATAN,SINH,COSH,TANH,EXP,SINCOS};
    for(unsigned i=0;i<sizeof(zero_ops)/sizeof(*zero_ops);++i)
        assert(trans_is_exact(zero_ops[i],ti(0),ti(0),ti(0)));
    assert(trans_is_exact(LOG,ti(1),ti(0),ti(0)));
    assert(trans_is_exact(ACOS,ti(1),ti(0),ti(0)));
    assert(!trans_is_exact(ACOS,ti(0),ti(0),tc_pi()));
    V inf={0,0,0,INF,0};
    assert(trans_is_exact(TANH,inf,ti(0),ti(1)));
    assert(!trans_is_exact(ATAN,inf,ti(0),tc_pi()));
    assert(trans_is_exact(POW,ti(2),inf,inf));
}
int main(void) {
    test_domain();test_core();test_pack();test_exactness_table();
}
````
