# bennett-plugin quality-floor change set (job/quality-plugin), council round 1

Subject: the quality-floor remediation of `bennett-plugin` (LLVM pass plugin: lowering of dialect-marked LLVM IR to the Bennett ISA), range `5a092cded3ba3351ba8cc2977a7eaf3b40f46526..2ecdd90` (27 commits; carries pin-plugin, reviewed CLEAR in docs/reviews/2026-11-06-pin-plugin-r2.md). Sol review rounds: r1 BLOCK (P0 bp-kya shared-global guard depends on function order: silent wrong value; P0 bp-9t7 weakened normalisation coverage), r2 CLEAR at cd6943d (docs/reviews/2026-11-06-quality-plugin-r2.md; 2ecdd90 adds only that document). Default test command `scripts/test` (23 commands) exit 0 in a solo orchestrator rerun. Background specs: dialect 0.2.13 (pinned 95a4b8d) and ISA 0.8.

Your working directory is a frozen detached worktree of `bennett-plugin` at 2ecdd90. This document embeds (1) the unified diff of every non-test path (src/, scripts/, gate.toml, CMakeLists.txt, SPEC_VERSIONS.toml, docs excluded) and (2) the post-change text of the changed source files and the three new/central regression tests. The test-suite diff (about 800 KB over 55 files under tests/) is NOT embedded: read it with `git diff 5a092cded3ba3351ba8cc2977a7eaf3b40f46526 2ecdd90 -- tests/` in the worktree. Grade: lowering semantics changed in src/Production.cpp, src/Scalar.cpp, src/Reversible.inc, src/BennettPlugin.cpp (a behaviour change hidden in a refactor is the main risk), test integrity of the rewritten suites (weakened, deleted or self-referential expectations), gate/ratchet changes, and any narrowing. Unchanged code is context.

## Files changed under tests/ (read in the worktree)

     tests/address_spaces.py          |   88 ++++++
     tests/aggregate_rows.py          |  235 +++++++++++++---
     tests/allocator_closure.py       |  222 ++++++++++++----
     tests/analysis_clock.py          |   34 ++-
     tests/analysis_edges.py          |  269 ++++++++++++++-----
     tests/analysis_performance.py    |   90 +++++--
     tests/budget_stage.py            |  271 ++++++++++++++-----
     tests/build_defaults.py          |   74 ++++++
     tests/build_fallback.py          |  138 +++++++---
     tests/cc_calls.py                |  149 ++++++++---
     tests/cc_switch.py               |  180 +++++++++----
     tests/contract_policy.py         |  121 +++++----
     tests/contracts.py               |  158 +++++++++--
     tests/corpus_gate.py             |  628 ++++++++++++++++++++++++++++++++-----------
     tests/descriptors.py             |  115 ++++++--
     tests/dialect_version.py         |  137 +++++++---
     tests/entry_runtime.py           |   65 +++++
     tests/entry_snapshot.py          |  397 +++++++++++++++++++++-------
     tests/gate_policy.py             |   72 ++++-
     tests/general_dispatch.py        |  388 +++++++++++++++++++++------
     tests/integer_intrinsics.py      |  559 +++++++++++++++++++++++++++++----------
     tests/key_audit.py               |   98 +++++--
     tests/materialisation.py         |  181 +++++++++++--
     tests/memory_runtime.py          |  345 ++++++++++++++++++++----
     tests/native_checked.py          |  264 ++++++++++++------
     tests/native_comparison.py       |  219 +++++++++------
     tests/native_fixtures.py         |  192 +++++++++-----
     tests/native_hello.py            |  154 +++++++----
     tests/native_layout.py           |  209 ++++++++++-----
     tests/native_link.py             |  335 ++++++++++++++++-------
     tests/normalisation_check.cpp    |   66 +++++
     tests/normalisation_scope.py     |   91 +++++++
     tests/pin_policy.py              |  479 +++++++++++++++++++++++++++++++++
     tests/pinned_siblings.py         |   45 ++++
     tests/prior_objects.py           |   33 ++-
     tests/probes/allocator-bounds.ll |    5 +-
     tests/production.py              |  304 +++++++++++++++++----
     tests/production_budgets.py      |  159 +++++++++--
     tests/production_cross_major.py  |   52 +++-
     tests/production_dispatch.py     |  189 +++++++++++--
     tests/production_environments.py |  383 ++++++++++++++++++++++-----
     tests/production_lifts.py        |  223 +++++++++++++---
     tests/production_records.py      |   87 ++++--
     tests/production_shapes.py       |  338 ++++++++++++++++++++----
     tests/quality_ratchet.py         |   72 +++++
     tests/recognition.py             |  175 +++++++++---
     tests/reference_images.py        |  299 ++++++++++++++-------
     tests/region_keys.py             |  306 ++++++++++++++++-----
     tests/register_classes.py        |  162 ++++++++++++
     tests/reversible.py              |  386 ++++++++++++++++++++++-----
     tests/review_regressions.py      | 1131 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------
     tests/scalars.py                 |  316 +++++++++++++++++-----
     tests/shadow_stack.py            |  167 +++++++++---
     tests/smoke.py                   |  213 +++++++++++----
     tests/softfloat.py               | 1013 ++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------
     tests/validation.py              |  212 ++++++++++++---
     tests/wide.py                    |  357 ++++++++++++++++++-------
     57 files changed, 10741 insertions(+), 2909 deletions(-)

## 1. Unified diff, non-test paths (git diff 5a092cded3ba3351ba8cc2977a7eaf3b40f46526 2ecdd90 -- . ':!tests' ':!docs' ':!README.md' ':!HANDOFF.md')

````diff
diff --git a/.gitignore b/.gitignore
index d51f152..44c702e 100644
--- a/.gitignore
+++ b/.gitignore
@@ -24,3 +24,9 @@ compile_commands.json
 
 .tmp/
 __pycache__/
+*.pyc
+*.log
+.beads/**/LOCK
+*.darc
+PROGRESS*
+LAST-RUN*
diff --git a/CMakeLists.txt b/CMakeLists.txt
index 7d98fe8..a7d7e44 100644
--- a/CMakeLists.txt
+++ b/CMakeLists.txt
@@ -2,6 +2,10 @@ cmake_minimum_required(VERSION 3.20)
 project(bennett-plugin LANGUAGES C CXX)
 set(CMAKE_CXX_STANDARD 17)
 set(CMAKE_CXX_STANDARD_REQUIRED ON)
+option(BENNETT_COVERAGE "Instrument a single LLVM-major GCC build with gcov" OFF)
+if(BENNETT_COVERAGE AND NOT LLVM_DIR)
+  message(FATAL_ERROR "Set LLVM_DIR to select one major for coverage")
+endif()
 if(NOT LLVM_DIR)
   include(ExternalProject)
   foreach(major 18 23)
@@ -18,18 +22,37 @@ else()
     message(FATAL_ERROR "Tested LLVM majors are 18 and 23")
   endif()
   add_library(BennettPlugin MODULE src/BennettPlugin.cpp src/NativeComparison.cpp src/Analysis.cpp src/Scalar.cpp src/Normalise.cpp src/SoftFloat.cpp src/Wide.cpp src/Integer.cpp src/Memory.cpp src/Residual.cpp src/Production.cpp src/Snapshot.cpp)
+  if(BENNETT_COVERAGE)
+    if(NOT CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
+      message(FATAL_ERROR "BENNETT_COVERAGE requires GCC and matching gcov")
+    endif()
+    target_compile_options(BennettPlugin PRIVATE --coverage -O0 -g1)
+    target_link_options(BennettPlugin PRIVATE --coverage)
+  endif()
   target_include_directories(BennettPlugin SYSTEM PRIVATE ${LLVM_INCLUDE_DIRS})
   target_compile_definitions(BennettPlugin PRIVATE ${LLVM_DEFINITIONS})
   set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS
-    "${CMAKE_CURRENT_SOURCE_DIR}/SPEC_VERSIONS.toml")
+    "${CMAKE_CURRENT_SOURCE_DIR}/SPEC_VERSIONS.toml"
+    "${CMAKE_CURRENT_SOURCE_DIR}/gate.toml"
+    "${CMAKE_CURRENT_SOURCE_DIR}/tests/contracts.py"
+    "${CMAKE_CURRENT_SOURCE_DIR}/tests/pinned_siblings.py")
+  find_package(Python3 REQUIRED COMPONENTS Interpreter)
+  execute_process(
+    COMMAND "${Python3_EXECUTABLE}" -c
+      "import sys; sys.path.insert(0, sys.argv[1] + '/tests'); from contracts import arith_path; print(arith_path(int(sys.argv[2])).absolute())"
+      "${CMAKE_CURRENT_SOURCE_DIR}" "${LLVM_VERSION_MAJOR}"
+    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
+    RESULT_VARIABLE arith_status OUTPUT_VARIABLE arith_path ERROR_VARIABLE arith_error
+    OUTPUT_STRIP_TRAILING_WHITESPACE)
+  if(NOT arith_status STREQUAL "0")
+    message(FATAL_ERROR "Pinned arithmetic LLVM ${LLVM_VERSION_MAJOR} unavailable:\n${arith_error}")
+  endif()
   file(READ "${CMAKE_CURRENT_SOURCE_DIR}/SPEC_VERSIONS.toml" spec_pins)
-  foreach(field path sha256)
-    string(REGEX MATCH "llvm${LLVM_VERSION_MAJOR}_${field} = \"([^\"]+)\"" arith_pin "${spec_pins}")
-    if(NOT arith_pin)
-      message(FATAL_ERROR "Missing arith LLVM ${LLVM_VERSION_MAJOR} ${field} pin")
-    endif()
-    set(arith_${field} "${CMAKE_MATCH_1}")
-  endforeach()
+  string(REGEX MATCH "llvm${LLVM_VERSION_MAJOR}_sha256 = \"([^\"]+)\"" arith_pin "${spec_pins}")
+  if(NOT arith_pin)
+    message(FATAL_ERROR "Missing arith LLVM ${LLVM_VERSION_MAJOR} sha256 pin")
+  endif()
+  set(arith_sha256 "${CMAKE_MATCH_1}")
   target_compile_definitions(BennettPlugin PRIVATE
     BENNETT_ARITH_DEFAULT_PATH="${arith_path}"
     BENNETT_ARITH_DEFAULT_SHA256="${arith_sha256}")
diff --git a/SPEC_VERSIONS.toml b/SPEC_VERSIONS.toml
index 3c42b0d..631eb1b 100644
--- a/SPEC_VERSIONS.toml
+++ b/SPEC_VERSIONS.toml
@@ -1,17 +1,18 @@
 status = "milestone-1-in-progress"
 dialect = "0.2.13"
 isa = "0.8"
+dialect_sha256 = "803c2e5589fb26ddba322206a08e8759a38c23bd7eded5c31ed0ad99ba4bda15"
 [specs]
 "bennett-dialect-spec" = "0.2.13"
 "bennett-isa-spec" = "0.8"
 [commits]
-"bennett-dialect-spec" = "95a4b8d06933018a07fef3516296a25fd582fcde"
+"bennett-dialect-spec" = "1c29c8d731228b67902c3fa72e410e1bb71d16b4"
 [arith]
-commit = "0dea42d001ffe832493fa0711da4a59b8cc1dd10"
-llvm18_path = "/home/tobias/Projects/bennett-workspace/bennett-arith/dist/llvm18/bennett-arith.bc"
-llvm18_sha256 = "8d99956e8741803f2115e48fa28c6c71795fb0041e992f8835851b71dd4b6fc1"
-llvm23_path = "/home/tobias/Projects/bennett-workspace/bennett-arith/dist/llvm23/bennett-arith.bc"
-llvm23_sha256 = "59563a3a10949b1ea48ca8b79027310ac9f9f7e28c85a30e70a013ced04a6793"
+commit = "5e9b4509f3ee3f95ac9f7d22b43359e72cf9fdab"
+llvm18_path = ".tmp/gate/cache/bennett-arith@5e9b4509f3ee/bennett-arith/dist/llvm18/bennett-arith.bc"
+llvm18_sha256 = "a027f16991c06f39eb1305f28da0b1504651791bdd3533888171aa54e704f7ff"
+llvm23_path = ".tmp/gate/cache/bennett-arith@5e9b4509f3ee/bennett-arith/dist/llvm23/bennett-arith.bc"
+llvm23_sha256 = "8216b27231c36d750c326bbaef384011a1bdf7f7dbb717b8b8f5167551163f79"
 
 # Native-only transports/tools; production runtime remains the separate allocator pin.
 [native_comparison]
diff --git a/gate.toml b/gate.toml
index 818d60a..657d359 100644
--- a/gate.toml
+++ b/gate.toml
@@ -9,6 +9,10 @@ BENNETT_SIBLINGS = "{layout}"
 BENNETT_ARITH_PINNED_ROOT = "{sibling:bennett-arith}/dist"
 BENNETT_ALLOCATOR_PINNED_ROOT = "{sibling:bennett-runtimes}/dist"
 
+[[check]]
+name = "quality baseline"
+argv = ["python3", "-B", "scripts/quality.py", "--check"]
+
 [[check]]
 name = "plugin gate"
 argv = ["scripts/gate"]
@@ -22,29 +26,61 @@ name = "reference interpreter (debug)"
 cwd = "reference-interpreter"
 argv = ["cargo", "build", "--offline"]
 outputs = ["reference-interpreter/target/debug/bennett-isa-ref"]
-env = { CARGO_BUILD_JOBS = "4" }
+env = { CARGO_BUILD_JOBS = "3" }
 
 [[siblings."bennett-isa-spec".build]]
 name = "reference interpreter (release)"
 cwd = "reference-interpreter"
 argv = ["cargo", "build", "--offline", "--release"]
 outputs = ["reference-interpreter/target/release/bennett-isa-ref"]
-env = { CARGO_BUILD_JOBS = "4" }
+env = { CARGO_BUILD_JOBS = "3" }
 
 [siblings."bennett-dialect-spec"]
-sha = "023f5a771a814270634db3be9cfde88ded69f975"
-note = "the accepted 0.2.10 contract commit named in SPEC_VERSIONS.toml"
+sha = "1c29c8d731228b67902c3fa72e410e1bb71d16b4"
+note = "0.2.13 registry correction required by contract_policy.py; accepted spec text and corpus unchanged from 95a4b8d"
 
 [siblings."bennett-arith"]
-sha = "0dea42d001ffe832493fa0711da4a59b8cc1dd10"
+sha = "5e9b4509f3ee3f95ac9f7d22b43359e72cf9fdab"
 note = "commit named in SPEC_VERSIONS.toml [arith]"
 [siblings."bennett-arith".files]
-"dist/llvm18/bennett-arith.bc" = "8d99956e8741803f2115e48fa28c6c71795fb0041e992f8835851b71dd4b6fc1"
-"dist/llvm23/bennett-arith.bc" = "59563a3a10949b1ea48ca8b79027310ac9f9f7e28c85a30e70a013ced04a6793"
+"dist/llvm18/bennett-arith.bc" = "a027f16991c06f39eb1305f28da0b1504651791bdd3533888171aa54e704f7ff"
+"dist/llvm23/bennett-arith.bc" = "8216b27231c36d750c326bbaef384011a1bdf7f7dbb717b8b8f5167551163f79"
 
 [siblings."bennett-runtimes"]
-sha = "2076014f81164ca75cc8f26cfe0081c2478cfdaf"
+sha = "248e468ca505c684bbf254e52eb8148f1e530c83"
 note = "publication hashed by tests/allocator_closure.py and tests/reversible.py"
 [siblings."bennett-runtimes".files]
-"dist/llvm18/bennett-runtimes.bc" = "4ca7fb401658e145c611aa4b3817d1b5fe1623c4d973c04be8b80a0b5893633f"
-"dist/llvm23/bennett-runtimes.bc" = "bbdef17b6cbb05636ab97276a651705b115f6c5ec9622fb5ff391ba197f0179e"
+"dist/llvm18/bennett-runtimes.bc" = "bbc402fd9b97ce0c5cdf06eff864f77ea4bce22f619a0ad561b081f445f3c67a"
+"dist/llvm23/bennett-runtimes.bc" = "78bfc3f4c4ac2d269dc53e03a476fb67283b9d7e63592a6139ad2a7cd7ece884"
+
+[siblings."bennett-native-runtimes"]
+sha = "248e468ca505c684bbf254e52eb8148f1e530c83"
+repo = "bennett-runtimes"
+note = "native-only support and checker publication in SPEC_VERSIONS.toml; allocator stays at its own pin"
+[siblings."bennett-native-runtimes".files]
+"dist/llvm18/musl-sysroot/lib/native-support.bc" = "c7a1306784e7f487c040b724e2074294ff687f149bf6403a9e403973a833e596"
+"dist/llvm23/musl-sysroot/lib/native-support.bc" = "f7fee923e2b06d1c4106439e46ed03936a9ee7721d3498d008e298cb5265cade"
+"scripts/native-check" = "bb11d8498a8403a415a77910193302b00bb1978d6ee24c0079bab5aa69ab5c2e"
+"scripts/native-check.cpp" = "a5c383379ce3dcf5a53eca274aa446e968d533c13516a64a9d80dd6e3298828d"
+
+[siblings."bennett-vm"]
+sha = "805f0ec3481365132d517fefd5b5c12cbd39a845"
+note = "freeze the previously live native comparison launch API dependency at its observed HEAD"
+[[siblings."bennett-vm".build]]
+name = "launch API library (debug)"
+argv = ["cargo", "build", "--offline", "--lib", "-j3"]
+outputs = ["target/debug/libbennett_vm.so"]
+needs = ["bennett-isa-spec"]
+[[siblings."bennett-vm".build]]
+name = "launch API library (release)"
+argv = ["cargo", "build", "--offline", "--release", "--lib", "-j3"]
+outputs = ["target/release/libbennett_vm.so"]
+needs = ["bennett-isa-spec"]
+
+[siblings."bennett-targets"]
+sha = "dd036711936c496f53f6f1a9bebeb686335bf7cc"
+note = "pushed publication of ideal-all-to-all.json used by native_comparison.py and native_link.py; identical at 3ef86a56"
+
+[siblings."bennett-conformance"]
+sha = "6e6a6f1ebd69f6e81f4f7ea2dd15ea775733e616"
+note = "pushed rung-2 fixtures and sha256.json used by native_fixtures.py; identical at e39501e3"
diff --git a/scripts/build b/scripts/build
index 287c1ce..f053d3c 100755
--- a/scripts/build
+++ b/scripts/build
@@ -1,20 +1,23 @@
 #!/usr/bin/env python3
 """Offline dual-major build. Uses CMake when present, llvm-config otherwise."""
-import concurrent.futures, hashlib, os, shutil, subprocess, tomllib
+import concurrent.futures, hashlib, os, shutil, subprocess, sys, tomllib
 from pathlib import Path
 R=Path(__file__).resolve().parents[1]
 for key in ['DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','BROWSER']: os.environ.pop(key,None)
-(R/'.tmp').mkdir(exist_ok=True);os.environ['TMPDIR']=str(R/'.tmp')
+(R/'.tmp').mkdir(exist_ok=True);os.environ.setdefault('TMPDIR',str(R/'.tmp'))
+sys.path.insert(0, str(R/'tests'))
+from contracts import arith_path
+arith_paths={major:arith_path(major) for major in (18,23)}
 if shutil.which('cmake'):
  subprocess.run(['cmake','-S',str(R),'-B',str(R/'build')],check=True)
- subprocess.run(['cmake','--build',str(R/'build'),'-j','4'],check=True)
+ subprocess.run(['cmake','--build',str(R/'build'),'-j','3'],check=True)
 else:
  print('cmake unavailable: offline llvm-config build (CMake configuration unverified)',flush=True)
  pins=tomllib.loads((R/'SPEC_VERSIONS.toml').read_text())['arith']
  def build(major):
   tool=Path(f'/usr/lib/llvm-{major}/bin')
   flags=subprocess.check_output([str(tool/'llvm-config'),'--cxxflags'],text=True).split()
-  definitions=[f'-DBENNETT_ARITH_DEFAULT_PATH="{pins[f"llvm{major}_path"]}"',
+  definitions=[f'-DBENNETT_ARITH_DEFAULT_PATH="{arith_paths[major]}"',
                f'-DBENNETT_ARITH_DEFAULT_SHA256="{pins[f"llvm{major}_sha256"]}"']
   compile_flags=[*flags,'-std=c++17','-fPIC','-g','-O2',*definitions]
   dest=R/f'build/llvm{major}';dest.mkdir(parents=True,exist_ok=True)
diff --git a/scripts/coverage b/scripts/coverage
new file mode 100755
index 0000000..a41ac12
--- /dev/null
+++ b/scripts/coverage
@@ -0,0 +1,67 @@
+#!/usr/bin/env python3
+"""Summarise GCC executable-line coverage for plugin sources, without a threshold."""
+
+import argparse
+import gzip
+import json
+from pathlib import Path
+import subprocess
+
+ROOT = Path(__file__).resolve().parents[1]
+
+
+def main():
+    parser = argparse.ArgumentParser(description=__doc__)
+    parser.add_argument("--build-dir", type=Path, default=ROOT / "build/coverage18")
+    args = parser.parse_args()
+    notes = sorted(args.build_dir.rglob("*.gcno"))
+    if not notes:
+        raise SystemExit(f"no instrumented objects under {args.build_dir}")
+    destination = ROOT / ".tmp/coverage-report"
+    destination.mkdir(parents=True, exist_ok=True)
+    files = {}
+    for note in notes:
+        result = subprocess.run(
+            ["gcov", "--json-format", str(note.resolve())],
+            cwd=destination,
+            capture_output=True,
+            text=True,
+            timeout=30,
+        )
+        if result.returncode:
+            raise SystemExit(result.stderr)
+        report = destination / (note.stem + ".gcov.json.gz")
+        with gzip.open(report, "rt") as stream:
+            data = json.load(stream)
+        for source in data["files"]:
+            path = Path(source["file"]).resolve()
+            if not path.is_relative_to(ROOT / "src"):
+                continue
+            name = str(path.relative_to(ROOT))
+            lines = files.setdefault(name, {})
+            for line in source["lines"]:
+                number = line["line_number"]
+                lines[number] = lines.get(number, 0) + line["count"]
+    rows = {
+        name: {
+            "covered": sum(count > 0 for count in lines.values()),
+            "lines": len(lines),
+        }
+        for name, lines in sorted(files.items())
+    }
+    covered = sum(row["covered"] for row in rows.values())
+    total = sum(row["lines"] for row in rows.values())
+    if not total:
+        raise SystemExit("gcov reports contain no executable plugin source lines")
+    result = {
+        "covered": covered,
+        "lines": total,
+        "percent": round(100 * covered / total, 2),
+        "files": rows,
+    }
+    (destination / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
+    print(json.dumps(result, indent=2))
+
+
+if __name__ == "__main__":
+    main()
diff --git a/scripts/gate b/scripts/gate
index ab2c532..01a77a7 100755
--- a/scripts/gate
+++ b/scripts/gate
@@ -8,22 +8,21 @@ script_dir="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
 root="$(cd "$script_dir/.." && pwd)"
 unset DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER
 export TMPDIR="${TMPDIR:-$root/.tmp}"
-export BENNETT_SIBLINGS="${BENNETT_SIBLINGS:-$(dirname "$root")}"
 mkdir -p "$TMPDIR"
-# A relocated immutable publication is allowed; its digest remains the contract pin.
-python3 - "$root" <<'PYTHON'
+# Resolve arithmetic before any plugin subprocess inherits its implicit input.
+BENNETT_ARITH_PINNED_ROOT="$(python3 - "$root" <<'PYTHON'
 import sys
 sys.path.insert(0, sys.argv[1]+'/tests')
 from contracts import arith_path
-for major in (18,23): print(f'arith LLVM {major}: {arith_path(major)}', flush=True)
+for major in (18,23): print(f'arith LLVM {major}: {arith_path(major)}', file=sys.stderr, flush=True)
+print(arith_path(18).parent.parent)
 PYTHON
+)"
+export BENNETT_ARITH_PINNED_ROOT
 "$root/scripts/build"
-python3 "$root/tests/smoke.py"
-python3 "$root/tests/gate_policy.py"
-python3 "$root/tests/contract_policy.py"
+python3 "$root/tests/build_defaults.py"
+"$root/scripts/test"
 for major in 18 23; do
-  python3 "$root/tests/recognition.py" --major "$major"
-  python3 "$root/tests/analysis_edges.py" --major "$major"
   python3 "$root/tests/analysis_performance.py" --major "$major"
   python3 "$root/tests/reference_images.py" --major "$major"
   python3 "$root/tests/materialisation.py" --major "$major"
@@ -43,8 +42,6 @@ for major in 18 23; do
   python3 "$root/tests/memory_runtime.py" --major "$major"
   python3 "$root/tests/region_keys.py" --major "$major"
   python3 "$root/tests/key_audit.py" --major "$major"
-  python3 "$root/tests/validation.py" --major "$major"
-  python3 "$root/tests/scalars.py" --major "$major"
   python3 "$root/tests/descriptors.py" --major "$major"
   python3 "$root/tests/production.py" --major "$major"
   python3 "$root/tests/production_environments.py" --major "$major" --case memory-handle --case retired-handle --case combined-devices --case multiple-outputs --case heterogeneous-layouts --case pointer-layouts --case return-console --case inplace-inout --case inplace-not-inverse --case inplace-small-budget --case inplace-second-small-budget --case memory-layouts --case wide-output --case unnamed-layouts
@@ -55,6 +52,7 @@ for major in 18 23; do
   python3 "$root/tests/production_records.py" --major "$major"
   python3 "$root/tests/shadow_stack.py" --major "$major"
   python3 "$root/tests/production_lifts.py" --major "$major" --case entry-replay-byte --case rung4-mini --case rung8-mini --case listsum --case shadow-n24
+  python3 "$root/tests/review_regressions.py" --major "$major" --case mixed-native
 done
 # Independent snapshot executions are CPU-heavy; their artifacts are major-local.
 python3 "$root/tests/entry_snapshot.py" --major 18 &
diff --git a/scripts/quality.py b/scripts/quality.py
new file mode 100644
index 0000000..37f69f7
--- /dev/null
+++ b/scripts/quality.py
@@ -0,0 +1,210 @@
+#!/usr/bin/env python3
+"""Repository-local quality proxies and a ratchet against docs/quality.md."""
+
+import argparse
+import ast
+import json
+import math
+from pathlib import Path
+import re
+import subprocess
+
+ROOT = Path(__file__).resolve().parents[1]
+BASELINE = re.compile(r"<!-- quality-baseline -->\s*```json\n(.*?)\n```", re.S)
+IDENTIFIER = re.compile(
+    r"\b(?:bp|bd|b-dialect-spec)-[a-z0-9]+\b|\b(?:sol|quality)-plugin\b"
+)
+LITTER = re.compile(
+    r"(^|/)(__pycache__|PROGRESS[^/]*|LAST-RUN[^/]*)(/|$)|\.(pyc|log|lock|darc)$|(^|/)LOCK$"
+)
+CONTROL = {"if", "for", "while", "switch", "catch", "sizeof", "alignas"}
+TOKENS = re.compile(
+    r'//[^\n]*|/\*.*?\*/|R"([^ ()\\\t\r\n]*)\(.*?\)\1"|"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27',
+    re.S,
+)
+
+
+def cpp_functions(source):
+    masked = TOKENS.sub(lambda match: re.sub(r"[^\n]", " ", match.group()), source)
+    stack, functions = [], []
+    for match in re.finditer(r"[{}]", masked):
+        position = match.start()
+        if match.group() == "{":
+            boundary = max(masked.rfind(char, 0, position) for char in ";{}") + 1
+            header = masked[boundary:position]
+            signature = re.search(
+                r"([A-Za-z_~]\w*)\s*\([^{};]*\)\s*(?:const|override|noexcept)?\s*$",
+                header,
+            )
+            name = signature.group(1) if signature else None
+            stack.append((position, name if name not in CONTROL else None, boundary))
+        else:
+            if not stack:
+                raise ValueError("unbalanced closing brace in C++ source")
+            start, name, boundary = stack.pop()
+            if name:
+                first = (
+                    boundary
+                    + len(masked[boundary:start])
+                    - len(masked[boundary:start].lstrip())
+                )
+                line = masked.count("\n", 0, first) + 1
+                length = masked.count("\n", first, position) + 1
+                body = masked[start + 1 : position].strip()
+                trivial = bool(re.fullmatch(r"(?:return\s+)?[\w:.]+\([^;{}]*\);", body))
+                functions.append(
+                    {"name": name, "line": line, "length": length, "trivial": trivial}
+                )
+    if stack:
+        raise ValueError("unbalanced opening brace in C++ source")
+    depth, complexity = 0, 0
+    for match in re.finditer(
+        r"\b(?:if|for|while|switch|catch|else)\b|&&|\|\||\?|[{}]", masked
+    ):
+        token = match.group()
+        if token == "{":
+            depth += 1
+        elif token == "}":
+            depth -= 1
+        else:
+            complexity += 1 + depth
+    return functions, complexity
+
+
+def python_functions(source):
+    tree = ast.parse(source)
+    functions = []
+    for node in ast.walk(tree):
+        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
+            body = node.body
+            if (
+                body
+                and isinstance(body[0], ast.Expr)
+                and isinstance(body[0].value, ast.Constant)
+                and isinstance(body[0].value.value, str)
+            ):
+                body = body[1:]
+            trivial = (
+                len(body) == 1
+                and isinstance(body[0], (ast.Return, ast.Expr))
+                and isinstance(body[0].value, ast.Call)
+            )
+            functions.append(
+                {
+                    "name": node.name,
+                    "line": node.lineno,
+                    "length": node.end_lineno - node.lineno + 1,
+                    "trivial": trivial,
+                }
+            )
+    branches = (
+        ast.If,
+        ast.For,
+        ast.AsyncFor,
+        ast.While,
+        ast.ExceptHandler,
+        ast.IfExp,
+        ast.Match,
+    )
+
+    def mass(node, depth=0):
+        branch = isinstance(node, branches)
+        own = 1 + depth if branch else 0
+        if isinstance(node, ast.BoolOp):
+            own += len(node.values) - 1
+        return own + sum(
+            mass(child, depth + branch) for child in ast.iter_child_nodes(node)
+        )
+
+    return functions, mass(tree)
+
+
+def measure(root, paths):
+    files, long_functions = {}, []
+    process_identifiers = 0
+    for name in sorted(paths):
+        path = root / name
+        if not path.is_file():
+            continue
+        is_python = path.suffix == ".py" or (
+            name.startswith("scripts/")
+            and not path.suffix
+            and "python" in path.read_text().partition("\n")[0]
+        )
+        if not is_python and path.suffix not in (".cpp", ".c", ".h", ".inc"):
+            continue
+        source = path.read_text()
+        if name.startswith(("src/", "include/")):
+            process_identifiers += len(IDENTIFIER.findall(source))
+        if is_python:
+            functions, complexity = python_functions(source)
+        else:
+            functions, complexity = cpp_functions(source)
+        lengths = sorted(function["length"] for function in functions)
+        percentile = lambda fraction: (
+            lengths[math.ceil(fraction * len(lengths)) - 1] if lengths else 0
+        )
+        files[name] = {
+            "functions": len(lengths),
+            "length_p50": percentile(0.5),
+            "length_p90": percentile(0.9),
+            "length_max": max(lengths, default=0),
+            "over_300": sum(length > 300 for length in lengths),
+            "complexity": complexity,
+            "trivial_wrappers": sum(function["trivial"] for function in functions),
+        }
+        long_functions.extend(
+            {"file": name, **function}
+            for function in functions
+            if function["length"] > 300
+        )
+    return {
+        "files": files,
+        "process_identifiers": process_identifiers,
+        "litter": sorted(name for name in paths if LITTER.search(name)),
+        "long_functions": long_functions,
+    }
+
+
+def regressions(current, baseline):
+    failures = []
+    for key in ("process_identifiers", "litter"):
+        count = lambda value: len(value) if isinstance(value, list) else value
+        if count(current[key]) > count(baseline[key]):
+            failures.append(f"{key}: {count(baseline[key])} -> {count(current[key])}")
+    for name, values in current["files"].items():
+        previous = baseline["files"].get(name, {})
+        for key, value in values.items():
+            if key != "functions" and value > previous.get(key, 0):
+                failures.append(f"{name} {key}: {previous.get(key, 0)} -> {value}")
+    return failures
+
+
+def main():
+    parser = argparse.ArgumentParser(description=__doc__)
+    parser.add_argument("--check", action="store_true")
+    args = parser.parse_args()
+    result = subprocess.run(
+        ["git", "ls-files", "-z"],
+        cwd=ROOT,
+        capture_output=True,
+        text=True,
+        timeout=10,
+        check=True,
+    )
+    paths = result.stdout.rstrip("\0").split("\0")
+    current = measure(ROOT, paths)
+    if args.check:
+        match = BASELINE.search((ROOT / "docs/quality.md").read_text())
+        if not match:
+            raise SystemExit("docs/quality.md has no quality-baseline JSON block")
+        failures = regressions(current, json.loads(match.group(1)))
+        if failures:
+            raise SystemExit("quality baseline worsened:\n" + "\n".join(failures))
+        print("quality baseline: no regressions")
+    else:
+        print(json.dumps(current, indent=2, sort_keys=True))
+
+
+if __name__ == "__main__":
+    main()
diff --git a/scripts/record-verification.py b/scripts/record-verification.py
index b78643d..bf22d9d 100644
--- a/scripts/record-verification.py
+++ b/scripts/record-verification.py
@@ -13,10 +13,10 @@ import argparse, datetime, hashlib, json, os, re, subprocess, sys
 from pathlib import Path
 R = Path(__file__).resolve().parents[1]
 sys.path.insert(0, str(R / 'tests'))
-from contracts import PIN, SIBLINGS, dialect_text, drift
+from contracts import PIN, sibling, dialect_text, drift
 
 MAJORS = (18, 23)
-ISA_REF = SIBLINGS / 'bennett-isa-spec/reference-interpreter/target/debug/bennett-isa-ref'
+ISA_REF = sibling('bennett-isa-spec') / 'reference-interpreter/target/debug/bennett-isa-ref'
 SUMMARY_KEYS = ('cases_run', 'cases_agree', 'cases_deferred', 'cases_blocked', 'cases_diverge')
 
 
@@ -177,7 +177,7 @@ def main():
         'dialect': '0.2.13', 'dialect_commit': PIN, 'isa': '0.8',
         'arith': __import__('tomllib').loads((R/'SPEC_VERSIONS.toml').read_text())['arith'],
         'arith_gate_paths': {str(m):str(__import__('contracts').arith_path(m)) for m in MAJORS},
-        'allocator_gate_root': os.environ.get('BENNETT_ALLOCATOR_PINNED_ROOT'),
+        'allocator_gate_root': str(sibling('bennett-runtimes') / 'dist'),
         'plugin_sha256': gate['plugin_sha256'],
         'gate': {'command': 'scripts/gate', 'exit': a.gate_exit, 'accepted_contract_drift': False,
                  'contract_head_drift': gate['contract_head_drift'], 'contract_worktree_drift': gate['contract_worktree_drift'],
diff --git a/scripts/test b/scripts/test
new file mode 100755
index 0000000..f56cf88
--- /dev/null
+++ b/scripts/test
@@ -0,0 +1,91 @@
+#!/usr/bin/env python3
+"""Default, bounded checks; scripts/gate also runs the slow integration drivers."""
+
+import argparse
+import json
+import os
+from pathlib import Path
+import subprocess
+import sys
+import time
+
+ROOT = Path(__file__).resolve().parents[1]
+POLICIES = ("smoke", "gate_policy", "contract_policy", "pin_policy", "quality_ratchet")
+DRIVERS = (
+    "recognition",
+    "analysis_edges",
+    "validation",
+    "scalars",
+    "address_spaces",
+    "register_classes",
+    "entry_runtime",
+    "normalisation_scope",
+)
+REGRESSIONS = (
+    "shuffle",
+    "byval",
+    "global-diagnostic",
+    "byte-order",
+    "native-abi",
+    "block-order",
+    "control",
+    "dynamic-gate",
+    "unresolved-call",
+)
+
+
+def main():
+    parser = argparse.ArgumentParser(description=__doc__)
+    parser.add_argument("--major", action="append", type=int, choices=(18, 23))
+    args = parser.parse_args()
+    environment = dict(os.environ)
+    for key in ("DISPLAY", "WAYLAND_DISPLAY", "DBUS_SESSION_BUS_ADDRESS", "BROWSER"):
+        environment.pop(key, None)
+    temporary = ROOT / ".tmp/tests"
+    temporary.mkdir(parents=True, exist_ok=True)
+    environment.setdefault("TMPDIR", str(temporary))
+    environment["PYTHONDONTWRITEBYTECODE"] = "1"
+    commands = [[sys.executable, "-B", f"tests/{name}.py"] for name in POLICIES]
+    for major in args.major or (18, 23):
+        commands.extend(
+            [sys.executable, "-B", f"tests/{name}.py", "--major", str(major)]
+            for name in DRIVERS
+        )
+        commands.append(
+            [
+                sys.executable,
+                "-B",
+                "tests/review_regressions.py",
+                "--major",
+                str(major),
+                *(argument for name in REGRESSIONS for argument in ("--case", name)),
+            ]
+        )
+    started = time.monotonic()
+    for command in commands:
+        remaining = 180 - (time.monotonic() - started)
+        if remaining <= 0:
+            raise SystemExit("default tests exceeded the 180-second allowance")
+        result = subprocess.run(
+            command,
+            cwd=ROOT,
+            env=environment,
+            text=True,
+            capture_output=True,
+            timeout=min(120, remaining),
+        )
+        label = " ".join(command[2:])
+        print(f"{label}: exit {result.returncode}", flush=True)
+        if result.returncode:
+            print(result.stdout)
+            print(result.stderr, file=sys.stderr)
+            return result.returncode
+    elapsed = time.monotonic() - started
+    receipt = {"commands": len(commands), "elapsed_s": round(elapsed, 3)}
+    (temporary / "default.json").write_text(json.dumps(receipt, indent=2) + "\n")
+    print(json.dumps(receipt))
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
diff --git a/src/BennettPlugin.cpp b/src/BennettPlugin.cpp
index ddd8223..bcd637c 100644
--- a/src/BennettPlugin.cpp
+++ b/src/BennettPlugin.cpp
@@ -422,12 +422,12 @@ struct BennettPass : PassInfoMixin<BennettPass> {
     }
     if(rEntry) {
       lowerReversible(m,a,*rEntry,Output,StackCells,BudgetDefault,BudgetTableFile,Disk);
-      errs()<<"bennett: blocked:BD-B-ISA7 §11.5/§17.6 R entry; objects emitted; typed pre-instruction fault requires ISA-7 (bp-is0)\n";
+      errs()<<"bennett: blocked:BD-B-ISA7 §11.5/§17.6 R entry; objects emitted; typed pre-instruction fault requires ISA-7\n";
       std::exit(3);
     }
     for (Function &f : m)
       if (a.tiers[&f].count("R"))
-        fail("unimplemented", "§25.1 BLK-5 (blocked: bp-is0)", &f);
+        fail("unimplemented", "§25.1 BLK-5", &f);
     for (Function &f : m)
       for (Instruction &i : instructions(f))
         if (auto *c = dyn_cast<CallBase>(&i))
@@ -436,7 +436,7 @@ struct BennettPass : PassInfoMixin<BennettPass> {
                     g->getName() == "__bennett_qborrow")) {
             auto width = a.get(c->getArgOperand(1));
             if (width.top)
-              fail("unimplemented", "§25.1 BLK-1 (blocked: bp-2tw)", c);
+              fail("unimplemented", "§25.1 BLK-1", c);
           }
     lowerProduction(m, a, Output, StackCells, BudgetDefault, BudgetTableFile);
     return PreservedAnalyses::none();
diff --git a/src/Production.cpp b/src/Production.cpp
index af5b9d5..461a9f3 100644
--- a/src/Production.cpp
+++ b/src/Production.cpp
@@ -581,8 +581,12 @@ struct Entry {
   unsigned dispatchBlock = 0;
   Function *selectedCallee = nullptr;
   bool generalDescriptor = false;
+  std::set<uint64_t> functionAddresses;
   uint64_t functionAddress(Function *fn) {
-    if (auto address = comparisonFunctionAddress(*fn)) return *address;
+    if (auto address = comparisonFunctionAddress(*fn)) {
+      functionAddresses.insert(*address);
+      return *address;
+    }
     if (hasComparisonLayout())
       fail("BD-E-COMPARISON-LAYOUT", "missing function address", fn);
     // Standalone comparison link, matching the module-order convention used
@@ -590,7 +594,13 @@ struct Entry {
     uint64_t address=4096;
     for(auto &g:m.globals())address=alignTo(address,m.getDataLayout().getPreferredAlign(&g))+m.getDataLayout().getTypeAllocSize(g.getValueType()).getFixedValue();
     address=alignTo(address,uint64_t(4096));
-    for(auto &g:m) { if(&g==fn)return address; address+=16; }
+    for(auto &g:m) {
+      if(&g==fn) {
+        functionAddresses.insert(address);
+        return address;
+      }
+      address+=16;
+    }
     llvm_unreachable("function missing from comparison link");
   }
   AV intValue(uint64_t n, unsigned w=64) { Atom x; x.kind=Atom::Int;x.integer=APInt(w,n); AV v;v.atoms.insert(x);return v; }
@@ -1214,7 +1224,42 @@ struct Entry {
     }
   }
 #include "runtime/CallerSnapshot.inc"
-  void lower() {
+  void allocateRegister(CallBase &call, const std::string &q, uint64_t width) {
+    std::vector<std::string> classes = {"any"};
+    if (auto *metadata = m.getModuleFlag("bennett.classes")) {
+      auto *table = dyn_cast<MDNode>(metadata);
+      if (!table) fail("BD-E-OPERAND", "malformed register class table", &call);
+      for (auto &item : table->operands()) {
+        auto *name = dyn_cast<MDString>(item.get());
+        if (!name) fail("BD-E-OPERAND", "malformed register class name", &call);
+        classes.push_back(name->getString().str());
+      }
+    }
+    auto domain = a.get(call.getArgOperand(0));
+    auto allocate = [&](uint64_t index, const std::string &destination) {
+      rows.push_back(destination + " = qreg.new " + classes.at(index) + " " + std::to_string(width));
+    };
+    if (singletonInt(domain)) {
+      auto index = integer(domain, &call);
+      if (index >= classes.size()) fail("BD-E-OPERAND", "register class index outside the link table", &call);
+      allocate(index, q);
+      return;
+    }
+    std::vector<uint64_t> keys;
+    for (uint64_t index = 0; index < classes.size(); ++index)
+      if (domain.top || domain.atoms.count(*intValue(index).atoms.begin())) keys.push_back(index);
+    auto value = operand(call.getArgOperand(0));
+    auto id = std::to_string(dispatchBlock++), done = "class" + id + "done", bad = "class" + id + "bad";
+    compareTree(value, 64, keys, [&](uint64_t index) {
+      auto instance = fresh("qreg[" + std::to_string(width) + "]");
+      allocate(index, instance);
+      rows.push_back("br ^" + done + "(" + instance + ")");
+    }, bad);
+    rows.push_back("^" + bad + "():");
+    rows.push_back("trap");
+    rows.push_back("^" + done + "(" + q + ":qreg[" + std::to_string(width) + "]):");
+  }
+  void prepareLowering() {
     setupSnapshot();
     // Descriptor memory has no device representation: its fields are virtual
     // operands. Elide only local storage whose complete use closure is records.
@@ -1336,6 +1381,121 @@ struct Entry {
       blocks[&bb] = "b" + std::to_string(bn++);
     for (BasicBlock &bb : f)
       for (PHINode &p : bb.phis()) destinations(&p);
+  }
+  enum class CallFlow { Continue, EndBlock };
+  CallFlow lowerCall(CallBase *c) {
+    auto *g = resolve(c->getCalledOperand());
+    if(!g && ccNames && !c->isInlineAsm()) {
+      auto pointer=operand(c->getCalledOperand());auto pw=m.getDataLayout().getPointerSizeInBits();
+      auto value=emit("i"+std::to_string(pw),"ptrtoint.i"+std::to_string(pw)+" "+pointer);
+      std::map<uint64_t,Function *> candidates;std::vector<uint64_t> keys;
+      for(auto *candidate:a.candidates(c->getCalledOperand(),c->getFunctionType()))
+        if(ccNames->count(candidate) || (candidate->isDeclaration() && !candidate->isIntrinsic() && !markers().count(candidate->getName().str())))
+          candidates[functionAddress(candidate)]=candidate;
+      for(auto &candidate:candidates)keys.push_back(candidate.first);
+      auto args=callArguments(*c);
+      auto result=c->getType()->isVoidTy()?std::vector<std::string>{}:destinations(c);
+      auto id=std::to_string(dispatchBlock++),done="call"+id+"done",bad="call"+id+"bad";
+      compareTree(value,pw,keys,[&](uint64_t key) {
+        if(candidates.at(key)->isDeclaration()) {unresolvedCall(candidates.at(key)->getName());return;}
+        auto call="call @"+ccNames->at(candidates.at(key))+(args.values.empty()?"":" "+join(args.values," "));
+        std::vector<std::string> values;
+        if(!c->getType()->isVoidTy())for(auto &field:fields(c->getType()))values.push_back(fresh(fieldType(field.type)));
+        rows.push_back((values.empty()?"":(values.size()==1?values[0]:"("+join(values)+")")+" = ")+call);
+        rows.push_back("br ^"+done+"("+join(values)+")");
+      },bad);
+      rows.push_back("^"+bad+"():");rows.push_back("trap");
+      std::vector<std::string> bindings;
+      if(!result.empty()) {auto fs=fields(c->getType());for(unsigned k=0;k<result.size();++k)bindings.push_back(result[k]+":"+fieldType(fs[k].type));}
+      rows.push_back("^"+done+"("+join(bindings)+"):");releaseCallArguments(args);propagateExit();usesCCCalls=true;return CallFlow::Continue;
+    }
+    if (!g)
+      unimplemented("§17.4 indirect CC call", 1, c);
+    auto n = g->getName();
+    if (n.starts_with("llvm.lifetime.") ||
+        (!memoryDescriptors && n.starts_with("llvm.memset.") &&
+         descriptorObjects.count(
+             getUnderlyingObject(c->getArgOperand(0)))))
+      return CallFlow::Continue;
+    if(rTier && n.starts_with("__bennett_effect_")) {
+      auto suffix=n.drop_front(StringRef("__bennett_effect_").size());auto parts=suffix.split('_');
+      effectModels.insert(parts.first.str());std::vector<std::string> args;
+      for(auto &v:c->args())args.push_back(operand(v));
+      rows.push_back("effect "+parts.first.str()+"."+parts.second.str()+" "+join(args," "));return CallFlow::Continue;
+    }
+    if (n == "__bennett_nz_fault") {
+      if(auto *asmMD=c->getMetadata("bennett.asm")) {
+        std::string block;unsigned ordinal=0;
+        for(auto &row:rows)if(StringRef(row).starts_with("^")) {block=StringRef(row).drop_front().split('(').first.str();ordinal=0;}else ++ordinal;
+        asmPoints.push_back(json::Object{{"symbol",ccNames->at(&f)},{"block",block},{"ordinal",ordinal},
+          {"reason",cast<MDString>(asmMD->getOperand(0))->getString()}});
+      }
+      // Newly materialised allocator closures report the explicit code
+      // through §11.5 before trapping. The payload is private storage,
+      // not an extra logical heap allocation on a failing path.
+      if (!rTier && f.hasFnAttribute("bennett.cc.allocator")) {
+        reportedFault(c->getArgOperand(0));return CallFlow::EndBlock;
+      }
+      rows.push_back("trap"); return CallFlow::EndBlock;
+    }
+    if (n == "llvm.trap") { rows.push_back("trap"); return CallFlow::EndBlock; }
+    if (n == "__bennett_qalloc" || n == "__bennett_qborrow") {
+      auto w = integer(a.get(c->getArgOperand(1)), c);
+      auto q = files.count(c) ? files.at(c).q : fresh("qreg[" + std::to_string(w) + "]");
+      if (files.count(c)) {
+        // No site is executed twice in this acyclic entry-local file.
+        // Distinct nonzero identities are stable across stores and loads;
+        // free retires the live tag before any later use can match it.
+        auto tag = fresh("i" + std::to_string(m.getDataLayout().getPointerSizeInBits()));
+        rows.push_back(tag + " = const.i" + std::to_string(m.getDataLayout().getPointerSizeInBits()) + " " + std::to_string(files.at(c).identity));
+        names[c] = tag;
+        rows.push_back("store.i" + std::to_string(m.getDataLayout().getPointerSizeInBits()) + " " + files.at(c).tag + " " + tag);
+      } else names[c] = q;
+      allocateRegister(*c, q, w);
+    } else if (n == "__bennett_qfree")
+      withHandle(c->getArgOperand(0), [&](std::string q) { rows.push_back("qreg.free " + q); }, true);
+    else if (n == "__bennett_oracle")
+      descriptor(*c);
+    else if (n == "__bennett_inplace")
+      inplace(*c);
+    else if(n=="__bennett_ctrl" && controlledIdentity(*c)) {}
+    else if (n == "__bennett_gate" || n == "__bennett_measure")
+      gate(*c);
+    else if(n=="__bennett_nz_alloc") {
+      auto size=operand(c->getArgOperand(0));auto p=fresh("ptr");rows.push_back(p+" = alloc "+size);names[c]=p;recordAllocation(p,size);ccHeapBytes=table.capacities[1];
+    } else if(n=="__bennett_nz_free") {
+      auto p=operand(c->getArgOperand(0));auto bits=emit("i64","ptrtoint.i64 "+p);auto zero=number(0);auto isNull=emit("i1","icmp.eq "+bits+" "+zero);
+      auto id=std::to_string(dispatchBlock++),live="free"+id,done=live+"done";rows.push_back("br "+isNull+" ^"+done+"() ^"+live+"()");rows.push_back("^"+live+"():");rows.push_back("free "+p);recordFree(p);rows.push_back("br ^"+done+"()");rows.push_back("^"+done+"():");
+    } else if (ccNames && ccNames->count(g)) {
+      usesCCCalls=true;
+      // §14.1: LLVM fastcc/tail are source ABI/optimisation details.
+      // ISA calls bind typed operands, keep a callee environment and
+      // retain nested frames for LIFO reversal (§9.3 leaves CC dynamic).
+      auto args=callArguments(*c);
+      auto call="call @"+ccNames->at(g)+(args.values.empty()?"":" "+join(args.values," "));
+      if(c->getType()->isVoidTy())rows.push_back(call);
+      else {auto ns=destinations(c);rows.push_back((ns.size()==1?ns[0]:"("+join(ns)+")")+" = "+call);}
+      releaseCallArguments(args);propagateExit();
+    } else if(g->isDeclaration() && !g->isIntrinsic() && !markers().count(n.str()) &&
+              !n.starts_with("__bennett_sf_") && !n.starts_with("__bennett_rt_")) {
+      // A reached missing import is F(8). Continue naming the source
+      // tail in an unreachable block so successor uses remain valid.
+      if(!c->getType()->isVoidTy()) {
+        auto ns=destinations(c);auto fs=fields(c->getType());
+        for(unsigned k=0;k<ns.size();++k) {
+          if(fs[k].type->isPointerTy())rows.push_back(ns[k]+" = inttoptr "+number(0));
+          else rows.push_back(ns[k]+" = const.i"+std::to_string(width(fs[k].type))+" 0");
+        }
+      }
+      unresolvedCall(n);
+      rows.push_back("^missing" + std::to_string(dispatchBlock++) + "tail():");
+      return CallFlow::Continue;
+    } else
+      unimplemented("§17.4 CC marker/call lowering", 1, c);
+    return CallFlow::Continue;
+  }
+  void lower() {
+    prepareLowering();
     auto edge = [&](BasicBlock *to, BasicBlock *from) {
       std::vector<std::string> values;
       for (PHINode &p : to->phis()) {auto vs=operands(p.getIncomingValueForBlock(from));values.insert(values.end(),vs.begin(),vs.end());}
@@ -1385,115 +1545,7 @@ struct Entry {
           if(!target || (!target->getName().starts_with("llvm.dbg.") && !target->getName().starts_with("llvm.lifetime.") && !target->getName().starts_with("__bennett_nz_rstep")))countRStep();
         }
         if (auto *c = dyn_cast<CallBase>(&i)) {
-          auto *g = resolve(c->getCalledOperand());
-          if(!g && ccNames && !c->isInlineAsm()) {
-            auto pointer=operand(c->getCalledOperand());auto pw=m.getDataLayout().getPointerSizeInBits();
-            auto value=emit("i"+std::to_string(pw),"ptrtoint.i"+std::to_string(pw)+" "+pointer);
-            std::map<uint64_t,Function *> candidates;std::vector<uint64_t> keys;
-            for(auto *candidate:a.candidates(c->getCalledOperand(),c->getFunctionType()))
-              if(ccNames->count(candidate) || (candidate->isDeclaration() && !candidate->isIntrinsic() && !markers().count(candidate->getName().str())))
-                candidates[functionAddress(candidate)]=candidate;
-            for(auto &candidate:candidates)keys.push_back(candidate.first);
-            auto args=callArguments(*c);
-            auto result=c->getType()->isVoidTy()?std::vector<std::string>{}:destinations(c);
-            auto id=std::to_string(dispatchBlock++),done="call"+id+"done",bad="call"+id+"bad";
-            compareTree(value,pw,keys,[&](uint64_t key) {
-              if(candidates.at(key)->isDeclaration()) {unresolvedCall(candidates.at(key)->getName());return;}
-              auto call="call @"+ccNames->at(candidates.at(key))+(args.values.empty()?"":" "+join(args.values," "));
-              std::vector<std::string> values;
-              if(!c->getType()->isVoidTy())for(auto &field:fields(c->getType()))values.push_back(fresh(fieldType(field.type)));
-              rows.push_back((values.empty()?"":(values.size()==1?values[0]:"("+join(values)+")")+" = ")+call);
-              rows.push_back("br ^"+done+"("+join(values)+")");
-            },bad);
-            rows.push_back("^"+bad+"():");rows.push_back("trap");
-            std::vector<std::string> bindings;
-            if(!result.empty()) {auto fs=fields(c->getType());for(unsigned k=0;k<result.size();++k)bindings.push_back(result[k]+":"+fieldType(fs[k].type));}
-            rows.push_back("^"+done+"("+join(bindings)+"):");releaseCallArguments(args);propagateExit();usesCCCalls=true;continue;
-          }
-          if (!g)
-            unimplemented("§17.4 indirect CC call", 1, c);
-          auto n = g->getName();
-          if (n.starts_with("llvm.lifetime.") ||
-              (!memoryDescriptors && n.starts_with("llvm.memset.") &&
-               descriptorObjects.count(
-                   getUnderlyingObject(c->getArgOperand(0)))))
-            continue;
-          if(rTier && n.starts_with("__bennett_effect_")) {
-            auto suffix=n.drop_front(StringRef("__bennett_effect_").size());auto parts=suffix.split('_');
-            effectModels.insert(parts.first.str());std::vector<std::string> args;
-            for(auto &v:c->args())args.push_back(operand(v));
-            rows.push_back("effect "+parts.first.str()+"."+parts.second.str()+" "+join(args," "));continue;
-          }
-          if (n == "__bennett_nz_fault") {
-            if(auto *asmMD=c->getMetadata("bennett.asm")) {
-              std::string block;unsigned ordinal=0;
-              for(auto &row:rows)if(StringRef(row).starts_with("^")) {block=StringRef(row).drop_front().split('(').first.str();ordinal=0;}else ++ordinal;
-              asmPoints.push_back(json::Object{{"symbol",ccNames->at(&f)},{"block",block},{"ordinal",ordinal},
-                {"reason",cast<MDString>(asmMD->getOperand(0))->getString()}});
-            }
-            // Newly materialised allocator closures report the explicit code
-            // through §11.5 before trapping. The payload is private storage,
-            // not an extra logical heap allocation on a failing path.
-            if (!rTier && f.hasFnAttribute("bennett.cc.allocator")) {
-              reportedFault(c->getArgOperand(0));break;
-            }
-            rows.push_back("trap"); break;
-          }
-          if (n == "llvm.trap") { rows.push_back("trap"); break; }
-          if (n == "__bennett_qalloc" || n == "__bennett_qborrow") {
-            auto cls = integer(a.get(c->getArgOperand(0)), c),
-                 w = integer(a.get(c->getArgOperand(1)), c);
-            if (cls)
-              unimplemented("§3.4 configured register class", 1, c);
-            auto q = files.count(c) ? files.at(c).q : fresh("qreg[" + std::to_string(w) + "]");
-            if (files.count(c)) {
-              // No site is executed twice in this acyclic entry-local file.
-              // Distinct nonzero identities are stable across stores and loads;
-              // free retires the live tag before any later use can match it.
-              auto tag = fresh("i" + std::to_string(m.getDataLayout().getPointerSizeInBits()));
-              rows.push_back(tag + " = const.i" + std::to_string(m.getDataLayout().getPointerSizeInBits()) + " " + std::to_string(files.at(c).identity));
-              names[c] = tag;
-              rows.push_back("store.i" + std::to_string(m.getDataLayout().getPointerSizeInBits()) + " " + files.at(c).tag + " " + tag);
-            } else names[c] = q;
-            rows.push_back(q + " = qreg.new any " + std::to_string(w));
-          } else if (n == "__bennett_qfree")
-            withHandle(c->getArgOperand(0), [&](std::string q) { rows.push_back("qreg.free " + q); }, true);
-          else if (n == "__bennett_oracle")
-            descriptor(*c);
-          else if (n == "__bennett_inplace")
-            inplace(*c);
-          else if(n=="__bennett_ctrl" && controlledIdentity(*c)) {}
-          else if (n == "__bennett_gate" || n == "__bennett_measure")
-            gate(*c);
-          else if(n=="__bennett_nz_alloc") {
-            auto size=operand(c->getArgOperand(0));auto p=fresh("ptr");rows.push_back(p+" = alloc "+size);names[c]=p;recordAllocation(p,size);ccHeapBytes=table.capacities[1];
-          } else if(n=="__bennett_nz_free") {
-            auto p=operand(c->getArgOperand(0));auto bits=emit("i64","ptrtoint.i64 "+p);auto zero=number(0);auto isNull=emit("i1","icmp.eq "+bits+" "+zero);
-            auto id=std::to_string(dispatchBlock++),live="free"+id,done=live+"done";rows.push_back("br "+isNull+" ^"+done+"() ^"+live+"()");rows.push_back("^"+live+"():");rows.push_back("free "+p);recordFree(p);rows.push_back("br ^"+done+"()");rows.push_back("^"+done+"():");
-          } else if (ccNames && ccNames->count(g)) {
-            usesCCCalls=true;
-            // §14.1: LLVM fastcc/tail are source ABI/optimisation details.
-            // ISA calls bind typed operands, keep a callee environment and
-            // retain nested frames for LIFO reversal (§9.3 leaves CC dynamic).
-            auto args=callArguments(*c);
-            auto call="call @"+ccNames->at(g)+(args.values.empty()?"":" "+join(args.values," "));
-            if(c->getType()->isVoidTy())rows.push_back(call);
-            else {auto ns=destinations(c);rows.push_back((ns.size()==1?ns[0]:"("+join(ns)+")")+" = "+call);}
-            releaseCallArguments(args);propagateExit();
-          } else if(g->isDeclaration() && !g->isIntrinsic() && !markers().count(n.str()) &&
-                    !n.starts_with("__bennett_sf_") && !n.starts_with("__bennett_rt_")) {
-            // A reached missing import is F(8). Give unreachable successor
-            // blocks names for the unused result without executing source work.
-            if(!c->getType()->isVoidTy()) {
-              auto ns=destinations(c);auto fs=fields(c->getType());
-              for(unsigned k=0;k<ns.size();++k) {
-                if(fs[k].type->isPointerTy())rows.push_back(ns[k]+" = inttoptr "+number(0));
-                else rows.push_back(ns[k]+" = const.i"+std::to_string(width(fs[k].type))+" 0");
-              }
-            }
-            unresolvedCall(n);break;
-          } else
-            unimplemented("§17.4 CC marker/call lowering", 1, c);
+          if (lowerCall(c) == CallFlow::EndBlock) break;
         } else if(auto *insert=dyn_cast<InsertValueInst>(&i)) {
           auto vs=operands(insert->getAggregateOperand()),part=operands(insert->getInsertedValueOperand());
           auto fs=fields(insert->getType());unsigned k=0;
@@ -1769,6 +1821,10 @@ std::string linkReferences(Entry &e) {
   std::map<const GlobalVariable *,uint64_t> sourceBases;
   for(auto &g:e.m.globals()) if(globalSymbols.count(scalarGlobalKey(g)))sourceBases[&g]=bases.at(globalSymbols.at(scalarGlobalKey(g)));
   json::Object globals,interfaces;
+  // Function identities occupy their own address range before the standalone
+  // heap. Include even unreferenced source data used to place those identities.
+  if (!hasComparisonLayout() && !e.functionAddresses.empty())
+    base = std::max(base, *e.functionAddresses.rbegin() + 1);
   uint64_t heap=comparisonHeapBase().value_or(alignTo(base,uint64_t(4096))),heapLimit=0,stack=0;
   std::vector<std::map<std::string,std::string>> parsed;
   for(auto &ref:e.references) {
@@ -1777,6 +1833,10 @@ std::string linkReferences(Entry &e) {
     stack=std::max(stack,uint64_t(*layout.getAsObject()->getInteger("S_cells")));
   }
   heapLimit=std::max(heapLimit,e.ccHeapBytes);
+  if (parsed.empty()) heapLimit = std::max(heapLimit, e.table.capacities[1]);
+  for (auto address : e.functionAddresses)
+    if (address >= heap && address - heap < heapLimit)
+      fail("BD-E-COMPARISON-LAYOUT", "function address overlaps the heap", &e.f);
   if(parsed.empty())while((uint64_t(1)<<stack)<std::max(uint64_t(e.stack),e.table.capacities[2]))++stack;
   uint64_t endAddress=heap+heapLimit,memCount=0;
   for(auto &g:e.m.globals())if(e.ccGlobals.count(scalarGlobalKey(g))) {
@@ -1910,8 +1970,8 @@ std::string launchObject(Entry &e, json::Object &record,
       if(sec["layout"]!=first["layout"] || !e.referenceGlobals.front().empty() || mapped) unified=true;
     }
   }
-  unified |= (e.ccHeapBytes>0 || !e.ccGlobals.empty()) && !e.references.empty();
-  if(unified || (e.references.empty() && !e.ccGlobals.empty())) {
+  unified |= (e.ccHeapBytes>0 || !e.ccGlobals.empty() || !e.functionAddresses.empty()) && !e.references.empty();
+  if(unified || (e.references.empty() && (!e.ccGlobals.empty() || !e.functionAddresses.empty()))) {
     ref=linkReferences(e);
     if(e.references.empty()) ref="bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width="+
         std::to_string(e.m.getDataLayout().getPointerSizeInBits())+ref;
@@ -2216,9 +2276,31 @@ json::Object completeCoverage(StringRef object,
   }
   return json::Object{{"entries", std::move(entries)}};
 }
+// Discover source state while every reachable entry still has its original body.
+bool sharesGlobalState(Function &f) {
+  std::set<const Value *> visited;
+  bool sharedState = false;
+  std::function<void(const Value *)> findState = [&](const Value *value) {
+    if (!visited.insert(value).second) return;
+    if (auto *function = dyn_cast<Function>(value)) {
+      if (!function->isDeclaration())
+        for (const auto &instruction : instructions(function)) findState(&instruction);
+      return;
+    }
+    if (auto *global = dyn_cast<GlobalVariable>(value)) {
+      sharedState |= !global->isConstant();
+      if (global->hasInitializer()) findState(global->getInitializer());
+      return;
+    }
+    if (auto *user = dyn_cast<User>(value))
+      for (const auto &operand : user->operands()) findState(operand);
+  };
+  findState(&f);
+  return sharedState;
+}
 // The host uses only the published launch 0.8 C ABI. BENNETT_TARGET supplies
 // the target JSON at runtime; it is copied by bennett_load before launch.
-void hostStub(Function &f, StringRef object, const json::Object &record) {
+void hostStub(Function &f, StringRef object, const json::Object &record, bool sharedState) {
   Module &m = *f.getParent();
   auto &ctx = m.getContext();
   auto *ptr = PointerType::get(ctx, 0);
@@ -2239,6 +2321,19 @@ void hostStub(Function &f, StringRef object, const json::Object &record) {
        *bad = BasicBlock::Create(ctx, "launch.failed", &f);
   IRBuilder<> b(entry);
   IRBuilder<> err(bad);
+  if (sharedState) {
+    // Maintainer-approved interim until the native-sharing contract publishes.
+    auto message = "bennett: shared global state is promised and pending the native-sharing contract "
+                   "(bp-acm; b-dialect-spec-6u6) for " + f.getName().str() + "\n";
+    auto *text = b.CreateGlobalString(message);
+    auto write = m.getOrInsertFunction("write", size, i32, ptr, size);
+    b.CreateCall(write, {b.getInt32(2), text, ConstantInt::get(size, message.size())});
+    auto exit = m.getOrInsertFunction("_Exit", b.getVoidTy(), i32);
+    b.CreateCall(exit, {b.getInt32(125)});
+    b.CreateUnreachable();
+    err.CreateUnreachable();
+    return;
+  }
   auto intrinsic = [&](Intrinsic::ID id,
                        ArrayRef<Type *> types = ArrayRef<Type *>()) {
 #if LLVM_VERSION_MAJOR >= 23
@@ -2367,7 +2462,7 @@ void hostStub(Function &f, StringRef object, const json::Object &record) {
                       {p, id, result, request}));
   if(record.getString("mode")=="reversible") {
     // §19.2's one launch request. Entries needing argv/envp byte storage
-    // remain an explicit bp-ivy mechanic, rather than passing host pointers.
+    // require explicit byte marshalling, rather than passing host pointers.
     auto *req=b.CreateLoad(ptr,request);require(b.CreateIsNotNull(req));
     auto *service=b.CreateCall(api("bennett_request_service",ptr,{ptr}),{req});
     auto *same=b.CreateCall(api("strcmp",i32,{ptr,ptr}),{service,string("bennett.argv")});require(b.CreateICmpEQ(same,b.getInt32(0)));
@@ -2424,9 +2519,17 @@ void hostStub(Function &f, StringRef object, const json::Object &record) {
 }
 
 } // namespace
+// Freeze all dependencies before the first host body is replaced.
+void replaceHostEntries(ArrayRef<Function *> entries, StringRef out) {
+  std::map<Function *, bool> sharedState;
+  for (auto *entry : entries) sharedState.emplace(entry, sharesGlobalState(*entry));
+  for(auto *entry:entries) {
+    auto dir=out.str()+"/"+entry->getName().str();auto build=parse(read(dir+"/build.json"));
+    hostStub(*entry,read(dir+"/launch.bennett"),*build.getAsObject(),sharedState.at(entry));
+  }
+}
 #include "Reversible.inc"
-void lowerProduction(Module &m, Analysis &a, StringRef out, unsigned stack,
-                     StringRef budgetDefault, StringRef budgetFile) {
+bool specialiseRegisterWidths(Module &m, Analysis &a) {
   // Finite source widths become distinct static roots before register-file
   // construction. Unbounded widths retain the explicit BLK-1 obligation.
   std::vector<std::pair<CallInst *,std::vector<uint64_t>>> allocations;
@@ -2434,7 +2537,7 @@ void lowerProduction(Module &m, Analysis &a, StringRef out, unsigned stack,
     if(auto *c=dyn_cast<CallInst>(&i);c && c->getCalledFunction() &&
        (c->getCalledFunction()->getName()=="__bennett_qalloc" || c->getCalledFunction()->getName()=="__bennett_qborrow") && !isa<ConstantInt>(c->getArgOperand(1))) {
       auto v=a.get(c->getArgOperand(1));std::vector<uint64_t> widths;
-      if(v.top)unimplemented("§25.1 BLK-1 dynamic widths (blocked: bp-2tw)",3,c);
+      if(v.top)unimplemented("§25.1 BLK-1 dynamic widths",3,c);
       for(auto &x:v.atoms)if(x.kind==Atom::Int)widths.push_back(x.integer.getLimitedValue());
       std::sort(widths.begin(),widths.end());widths.erase(std::unique(widths.begin(),widths.end()),widths.end());allocations.push_back({c,widths});
     }
@@ -2461,9 +2564,12 @@ void lowerProduction(Module &m, Analysis &a, StringRef out, unsigned stack,
         rb.CreateCondBr(rb.CreateICmpULT(c->getArgOperand(1),key),left,right);tree(left,lo,mid);tree(right,mid+1,hi);
       };tree(head,0,site.second.size());c->replaceAllUsesWith(phi);c->eraseFromParent();
     }
-    Analysis specialised(m);specialised.run();lowerProduction(m,specialised,out,stack,budgetDefault,budgetFile);return;
+    return true;
   }
 
+  return false;
+}
+BudgetTable productionBudget(Module &m, Analysis &a, StringRef budgetDefault, StringRef budgetFile) {
   SmallVector<StringRef> components;
   budgetDefault.split(components, ',');
   std::vector<uint64_t> defaults;
@@ -2489,6 +2595,15 @@ void lowerProduction(Module &m, Analysis &a, StringRef out, unsigned stack,
               table.capacities[j] = std::max(table.capacities[j], atom.integer.getLimitedValue());
         }
   }
+  return table;
+}
+void lowerProduction(Module &m, Analysis &a, StringRef out, unsigned stack,
+                     StringRef budgetDefault, StringRef budgetFile) {
+  if (specialiseRegisterWidths(m, a)) {
+    Analysis specialised(m);specialised.run();
+    lowerProduction(m,specialised,out,stack,budgetDefault,budgetFile);return;
+  }
+  auto table = productionBudget(m, a, budgetDefault, budgetFile);
   // CC arithmetic uses the same linked definitions as L and native comparison.
   // Keep recursive numerical closures as §14.1 CC calls; acyclic closures
   // retain their established inlining and object identities.
@@ -2663,6 +2778,7 @@ void lowerProduction(Module &m, Analysis &a, StringRef out, unsigned stack,
       e.referenceGlobals=std::move(callee.referenceGlobals);e.snapshotFunctions=std::move(callee.snapshotFunctions);
       e.budgets=std::move(callee.budgets);
       e.ccGlobals.insert(callee.ccGlobals.begin(),callee.ccGlobals.end());
+      e.functionAddresses.insert(callee.functionAddresses.begin(),callee.functionAddresses.end());
       e.trappedCalls.insert(callee.trappedCalls.begin(),callee.trappedCalls.end());
       for(auto &proof:callee.controlledIdentities)e.controlledIdentities.push_back(std::move(proof));
       e.usesSourceMemory|=callee.usesSourceMemory;
@@ -2727,10 +2843,7 @@ void lowerProduction(Module &m, Analysis &a, StringRef out, unsigned stack,
   // Snapshot analysis of every entry sees the linked source memory, before
   // native stubs add embedded objects and launch-API string globals.
   a.releaseTransferGraphs();
-  for(auto *entry:entries) {
-    auto dir=out.str()+"/"+entry->getName().str();auto build=parse(read(dir+"/build.json"));
-    hostStub(*entry,read(dir+"/launch.bennett"),*build.getAsObject());
-  }
+  replaceHostEntries(entries, out);
   normaliseWideABI(*device);
   for (Function &f : *device)
     if (!f.isDeclaration() && a.tiers[m.getFunction(f.getName())].count("L"))
diff --git a/src/Reversible.inc b/src/Reversible.inc
index 130af13..1fd372b 100644
--- a/src/Reversible.inc
+++ b/src/Reversible.inc
@@ -26,7 +26,7 @@ void lowerReversible(Module &source, Analysis &sourceAnalysis, Function &sourceE
   auto device=CloneModule(source);auto &m=*device;
   auto entryName=sourceEntry.getName().str();auto *root=m.getFunction(entryName);
   for(auto &arg:root->args())if(arg.getArgNo()>0 && !arg.use_empty())
-    unimplemented("§19.2 argv/envp byte storage in R launch (bp-ivy)",4,&arg);
+    unimplemented("§19.2 argv/envp byte storage in R launch",4,&arg);
   SmallVector<StringRef> components;budgetDefault.split(components,',');
   std::vector<uint64_t> defaults;
   for(auto c:components) {uint64_t n;if(c.getAsInteger(10,n))fail("input","§9.2 budget default");defaults.push_back(n);}
@@ -143,7 +143,7 @@ void lowerReversible(Module &source, Analysis &sourceAnalysis, Function &sourceE
   launch->eraseFromParent();root->setName(entryName);
   checkComparisonMaterialisation(m);
   raw_fd_ostream bc(out.str()+"/device.bc",ec);if(ec)fail("output",ec.message());WriteBitcodeToFile(m,bc);bc.close();
-  auto buildRecord=parse(build);hostStub(sourceEntry,object,*buildRecord.getAsObject());
+  auto buildRecord=parse(build);hostStub(sourceEntry,object,*buildRecord.getAsObject(),sharesGlobalState(sourceEntry));
   raw_fd_ostream host(out.str()+"/host.bc",ec);if(ec)fail("output",ec.message());WriteBitcodeToFile(source,host);host.close();
   write(out.str()+"/launches.json",jcs(json::Value(json::Array{json::Object{{"entry",entryName},{"object",entryName+"/launch.bennett"},{"build_sha256",hash(build)},{"verdict","blocked:BD-B-ISA7"}}}))+"\n");
   json::Object artifacts;
diff --git a/src/Scalar.cpp b/src/Scalar.cpp
index 5ca16b8..03b799c 100644
--- a/src/Scalar.cpp
+++ b/src/Scalar.cpp
@@ -239,7 +239,128 @@ struct Scalar {
     }
     return acc;
   }
-  std::string body() {
+  bool lowerAggregate(Instruction &i) {
+    if(auto *insert=dyn_cast<InsertValueInst>(&i)) {
+      auto original=locations(insert->getAggregateOperand());
+      auto added=locations(insert->getInsertedValueOperand());
+      std::vector<std::string> aliases;unsigned j=0,n=0;
+      for(auto &field:fields(i.getType())) {
+        if(prefix(field.path,insert->getIndices())) {
+          auto output=names[&i]+"_"+std::to_string(n);dest(output,width(field.type));
+          lines.push_back(output+" = lift.mov "+added[j++].first);aliases.push_back(output);
+        } else aliases.push_back(original[n].first);
+        ++n;
+      }
+      fieldAliases[&i]=std::move(aliases);return true;
+    }
+    if(auto *extract=dyn_cast<ExtractValueInst>(&i)) {
+      auto input=locations(extract->getAggregateOperand());unsigned j=0,n=0;
+      for(auto &field:fields(extract->getAggregateOperand()->getType())) {
+        if(prefix(field.path,extract->getIndices())) {
+          auto output=names[&i]+(i.getType()->isAggregateType()?"_"+std::to_string(j):"");
+          dest(output,width(field.type));lines.push_back(output+" = lift.mov "+input[n].first);++j;
+        }
+        ++n;
+      }
+      return true;
+    }
+    if(i.getType()->isAggregateType() && (isa<SelectInst>(i)||isa<FreezeInst>(i))) {
+      auto *select=dyn_cast<SelectInst>(&i);auto condition=select?value(select->getCondition()):"";
+      auto left=locations(select?select->getTrueValue():i.getOperand(0));
+      auto right=select?locations(select->getFalseValue()):left;
+      for(unsigned n=0;n<left.size();++n) {auto output=fieldName(&i,n);dest(output,left[n].second);
+        lines.push_back(output+(select?" = lift.select "+condition+" "+left[n].first+" "+right[n].first:" = lift.mov "+left[n].first));}
+      return true;
+    }
+    return false;
+  }
+  bool lowerCall(CallBase *call, BasicBlock &bb, const std::function<std::string(BasicBlock *)> &blockName) {
+    if (auto *g = call->getCalledFunction();
+        g && g->getName() == "__bennett_nz_fault") {
+      auto *c = dyn_cast<ConstantInt>(call->getArgOperand(0));
+      if (!c)
+        unimplemented("§12.3 nonliteral fault", 2, call);
+      lines.push_back("fault " + number(c->getValue()));
+      return false;
+    }
+    auto *g = call->getCalledFunction();
+    if(!g)g=resolve(call->getCalledOperand());
+    std::vector<std::string> args;
+    for (Value *v : call->args())for(auto &part:locations(v))args.push_back(part.first);
+    auto name = g ? g->getName() : StringRef();
+    if (name == "__bennett_nz_alloc") {
+      dest(names[call],width(call->getType()));
+      lines.push_back(names[call]+" = lift.alloc "+args[0]); return true;
+    }
+    if (name == "__bennett_nz_free") {lines.push_back("lift.free "+args[0]);return true;}
+    auto result = names[call];
+    if (call->getType()->isVoidTy()) {result="t"+std::to_string(temps++);dest(result,1);}
+    else if(call->getType()->isAggregateType()) {result="t"+std::to_string(temps++);dest(result,width(call->getType()));}
+    else dest(result,width(call->getType()));
+    if (g && functions.count(g)) {
+      lines.push_back(result+" = lift.call @"+functions[g]+" ("+join(args)+")");if(call->getType()->isAggregateType())unpack(call,result);return true;
+    }
+    if (!g && analysis) {
+      auto candidates=analysis->candidates(call->getCalledOperand(),call->getFunctionType());
+      std::vector<Function *> sorted(candidates.begin(),candidates.end());
+      auto address=[](Function *f) -> uint64_t {
+        if(auto n=comparisonFunctionAddress(*f))return *n;
+        if(hasComparisonLayout())fail("BD-E-COMPARISON-LAYOUT","missing function address",f);
+        auto *md=f->getMetadata("bennett.address");
+        if (!md) unimplemented("§19.5 comparison function addresses",4,f);
+        return cast<ConstantInt>(cast<ConstantAsMetadata>(md->getOperand(0))->getValue())->getZExtValue();
+      };
+      std::sort(sorted.begin(),sorted.end(),[&](auto *a,auto *b){return address(a)<address(b);});
+      auto callee=value(call->getCalledOperand());
+      unsigned ordinal=1;for (Instruction &prev:bb) {if (&prev==call) break;if(auto *c=dyn_cast<CallBase>(&prev)) if(!resolve(c->getCalledOperand())) ++ordinal;}
+      auto prefix=blockName(&bb)+".q"+std::to_string(ordinal);
+      unsigned serial=0;
+      std::function<void(int,int)> tree=[&](int lo,int hi) {
+        if(hi<lo) {lines.push_back("qjump "+prefix+"d");return;}
+        if(hi-lo+1<=3) {
+          for(int k=lo;k<=hi;++k) {
+            auto c=constant(APInt(width(call->getCalledOperand()->getType()),address(sorted[k])));
+            auto t=temp(1,"lift.icmp.eq "+callee+" "+c);
+            auto next=k<hi?blockName(&bb)+".s"+std::to_string(++serial):prefix+"d";
+            lines.push_back("qbranch "+t+" "+prefix+"c"+std::to_string(k)+" "+next);
+            if(k<hi) lines.push_back(next+"():");
+          }
+        } else {
+          int mid=(lo+hi)/2;
+          auto c=constant(APInt(width(call->getCalledOperand()->getType()),address(sorted[mid])));
+          auto t=temp(1,"lift.icmp.ult "+callee+" "+c);
+          auto l=blockName(&bb)+".s"+std::to_string(++serial),r=blockName(&bb)+".s"+std::to_string(++serial);
+          lines.push_back("qbranch "+t+" "+l+" "+r);lines.push_back(l+"():");tree(lo,mid-1);lines.push_back(r+"():");tree(mid,hi);
+        }
+      };
+      tree(0,int(sorted.size())-1);
+      for(unsigned k=0;k<sorted.size();++k) {
+        lines.push_back(prefix+"c"+std::to_string(k)+"():");
+        lines.push_back(result+" = lift.call @"+functions.at(sorted[k])+" ("+join(args)+")");
+        lines.push_back("qjump "+prefix+"r");
+      }
+      lines.push_back(prefix+"d():");lines.push_back("fault 4");lines.push_back(prefix+"r():");if(call->getType()->isAggregateType())unpack(call,result);return true;
+    }
+    unimplemented("§14 calls (missing linked definition)", 2, call);
+    return true;
+  }
+  void lowerReturn(ReturnInst &returned) {
+    Value *rv = returned.getReturnValue();
+    std::string v = "r";
+    if (rv && rv->getType()->isAggregateType()) {
+      // §16.4: evaluate all flattened fields first, then pack without padding.
+      auto parts=locations(rv); unsigned packed = width(rv->getType()), offset = 0;
+      for (auto &part : parts) {
+        auto n = part.first;
+        if (part.second != packed) n = temp(packed,"lift.zext.i"+std::to_string(packed)+" "+n);
+        if (offset) { auto c = constant(APInt(packed,offset)); n = temp(packed,"lift.shl "+n+" "+c); }
+        v = offset ? temp(packed,"lift.or "+v+" "+n) : n;
+        offset += part.second;
+      }
+    } else if (rv) v = value(rv);
+    lines.push_back("lift.ret " + v);
+  }
+  void prepareValueNames() {
     unsigned k = 0;
     for (Argument &a : f.args())
       names[&a] = "a" + std::to_string(k++);
@@ -247,8 +368,11 @@ struct Scalar {
     for (Instruction &i : instructions(f))
       if (!i.getType()->isVoidTy())
         names[&i] = runtimeNames() && i.hasName() ? i.getName().str() : "v" + std::to_string(k++);
+  }
+  std::string body() {
+    prepareValueNames();
     std::map<BasicBlock *, unsigned> blockIndex;
-    k = 0;
+    unsigned k = 0;
     for (BasicBlock &b : f)
       blockIndex[&b] = k++;
     auto blockName = [&](BasicBlock *b) {
@@ -384,57 +508,13 @@ struct Scalar {
           }
           continue;
         }
-        if(auto *insert=dyn_cast<InsertValueInst>(&i)) {
-          auto original=locations(insert->getAggregateOperand());
-          auto added=locations(insert->getInsertedValueOperand());
-          std::vector<std::string> aliases;unsigned j=0,n=0;
-          for(auto &field:fields(i.getType())) {
-            if(prefix(field.path,insert->getIndices())) {
-              auto output=names[&i]+"_"+std::to_string(n);dest(output,width(field.type));
-              lines.push_back(output+" = lift.mov "+added[j++].first);aliases.push_back(output);
-            } else aliases.push_back(original[n].first);
-            ++n;
-          }
-          fieldAliases[&i]=std::move(aliases);continue;
-        }
-        if(auto *extract=dyn_cast<ExtractValueInst>(&i)) {
-          auto input=locations(extract->getAggregateOperand());unsigned j=0,n=0;
-          for(auto &field:fields(extract->getAggregateOperand()->getType())) {
-            if(prefix(field.path,extract->getIndices())) {
-              auto output=names[&i]+(i.getType()->isAggregateType()?"_"+std::to_string(j):"");
-              dest(output,width(field.type));lines.push_back(output+" = lift.mov "+input[n].first);++j;
-            }
-            ++n;
-          }
-          continue;
-        }
-        if(i.getType()->isAggregateType() && (isa<SelectInst>(i)||isa<FreezeInst>(i))) {
-          auto *select=dyn_cast<SelectInst>(&i);auto condition=select?value(select->getCondition()):"";
-          auto left=locations(select?select->getTrueValue():i.getOperand(0));
-          auto right=select?locations(select->getFalseValue()):left;
-          for(unsigned n=0;n<left.size();++n) {auto output=fieldName(&i,n);dest(output,left[n].second);
-            lines.push_back(output+(select?" = lift.select "+condition+" "+left[n].first+" "+right[n].first:" = lift.mov "+left[n].first));}
-          continue;
-        }
+        if (lowerAggregate(i)) continue;
         if (auto *g = dyn_cast<GetElementPtrInst>(&i)) {
           gep(cast<GEPOperator>(g), names[&i]);
           continue;
         }
         if (auto *r = dyn_cast<ReturnInst>(&i)) {
-          Value *rv = r->getReturnValue();
-          std::string v = "r";
-          if (rv && rv->getType()->isAggregateType()) {
-            // §16.4: evaluate all flattened fields first, then pack without padding.
-            auto parts=locations(rv); unsigned packed = width(rv->getType()), offset = 0;
-            for (auto &part : parts) {
-              auto n = part.first;
-              if (part.second != packed) n = temp(packed,"lift.zext.i"+std::to_string(packed)+" "+n);
-              if (offset) { auto c = constant(APInt(packed,offset)); n = temp(packed,"lift.shl "+n+" "+c); }
-              v = offset ? temp(packed,"lift.or "+v+" "+n) : n;
-              offset += part.second;
-            }
-          } else if (rv) v = value(rv);
-          lines.push_back("lift.ret " + v);
+          lowerReturn(*r);
           continue;
         }
         if (isa<UnreachableInst>(i)) {
@@ -442,73 +522,8 @@ struct Scalar {
           continue;
         }
         if (auto *call = dyn_cast<CallBase>(&i)) {
-          if (auto *g = call->getCalledFunction();
-              g && g->getName() == "__bennett_nz_fault") {
-            auto *c = dyn_cast<ConstantInt>(call->getArgOperand(0));
-            if (!c)
-              unimplemented("§12.3 nonliteral fault", 2, call);
-            lines.push_back("fault " + number(c->getValue()));
-            break;
-          }
-          auto *g = call->getCalledFunction();
-          if(!g)g=resolve(call->getCalledOperand());
-          std::vector<std::string> args;
-          for (Value *v : call->args())for(auto &part:locations(v))args.push_back(part.first);
-          auto name = g ? g->getName() : StringRef();
-          if (name == "__bennett_nz_alloc") {
-            dest(names[call],width(call->getType()));
-            lines.push_back(names[call]+" = lift.alloc "+args[0]); continue;
-          }
-          if (name == "__bennett_nz_free") {lines.push_back("lift.free "+args[0]);continue;}
-          auto result = names[call];
-          if (call->getType()->isVoidTy()) {result="t"+std::to_string(temps++);dest(result,1);}
-          else if(call->getType()->isAggregateType()) {result="t"+std::to_string(temps++);dest(result,width(call->getType()));}
-          else dest(result,width(call->getType()));
-          if (g && functions.count(g)) {
-            lines.push_back(result+" = lift.call @"+functions[g]+" ("+join(args)+")");if(call->getType()->isAggregateType())unpack(call,result);continue;
-          }
-          if (!g && analysis) {
-            auto candidates=analysis->candidates(call->getCalledOperand(),call->getFunctionType());
-            std::vector<Function *> sorted(candidates.begin(),candidates.end());
-            auto address=[](Function *f) -> uint64_t {
-              if(auto n=comparisonFunctionAddress(*f))return *n;
-              if(hasComparisonLayout())fail("BD-E-COMPARISON-LAYOUT","missing function address",f);
-              auto *md=f->getMetadata("bennett.address");
-              if (!md) unimplemented("§19.5 comparison function addresses",4,f);
-              return cast<ConstantInt>(cast<ConstantAsMetadata>(md->getOperand(0))->getValue())->getZExtValue();
-            };
-            std::sort(sorted.begin(),sorted.end(),[&](auto *a,auto *b){return address(a)<address(b);});
-            auto callee=value(call->getCalledOperand());
-            unsigned ordinal=1;for (Instruction &prev:bb) {if (&prev==call) break;if(auto *c=dyn_cast<CallBase>(&prev)) if(!resolve(c->getCalledOperand())) ++ordinal;}
-            auto prefix=blockName(&bb)+".q"+std::to_string(ordinal);
-            unsigned serial=0;
-            std::function<void(int,int)> tree=[&](int lo,int hi) {
-              if(hi<lo) {lines.push_back("qjump "+prefix+"d");return;}
-              if(hi-lo+1<=3) {
-                for(int k=lo;k<=hi;++k) {
-                  auto c=constant(APInt(width(call->getCalledOperand()->getType()),address(sorted[k])));
-                  auto t=temp(1,"lift.icmp.eq "+callee+" "+c);
-                  auto next=k<hi?blockName(&bb)+".s"+std::to_string(++serial):prefix+"d";
-                  lines.push_back("qbranch "+t+" "+prefix+"c"+std::to_string(k)+" "+next);
-                  if(k<hi) lines.push_back(next+"():");
-                }
-              } else {
-                int mid=(lo+hi)/2;
-                auto c=constant(APInt(width(call->getCalledOperand()->getType()),address(sorted[mid])));
-                auto t=temp(1,"lift.icmp.ult "+callee+" "+c);
-                auto l=blockName(&bb)+".s"+std::to_string(++serial),r=blockName(&bb)+".s"+std::to_string(++serial);
-                lines.push_back("qbranch "+t+" "+l+" "+r);lines.push_back(l+"():");tree(lo,mid-1);lines.push_back(r+"():");tree(mid,hi);
-              }
-            };
-            tree(0,int(sorted.size())-1);
-            for(unsigned k=0;k<sorted.size();++k) {
-              lines.push_back(prefix+"c"+std::to_string(k)+"():");
-              lines.push_back(result+" = lift.call @"+functions.at(sorted[k])+" ("+join(args)+")");
-              lines.push_back("qjump "+prefix+"r");
-            }
-            lines.push_back(prefix+"d():");lines.push_back("fault 4");lines.push_back(prefix+"r():");if(call->getType()->isAggregateType())unpack(call,result);continue;
-          }
-          unimplemented("§14 calls (missing linked definition)", 2, call);
+          if (!lowerCall(call, bb, blockName)) break;
+          continue;
         }
         if (auto *l = dyn_cast<LoadInst>(&i)) {
           unsigned w = width(l->getType());
@@ -684,15 +699,40 @@ std::string scalarGlobalImage(GlobalVariable &g, const std::map<const GlobalVari
   if(!g.hasInitializer())unimplemented("§19.5 undefined data image",2,&g);
   image(g.getInitializer(),0);return toHex(ArrayRef<uint8_t>(bytes),true);
 }
-void lowerScalar(Module &m, Function &f, StringRef desc, StringRef out,
-                 unsigned stackCells, uint64_t heapCapacity, int projection, std::map<std::string,std::string> *globalNames, uint64_t sstack, unsigned autoSnapshot) {
+uint64_t scalarModuleFlag(Module &m, StringRef name, uint64_t fallback) {
+  auto *metadata = m.getModuleFlag(name);
+  if (!metadata) return fallback;
+  auto *constant = dyn_cast<ConstantAsMetadata>(metadata);
+  auto *integer = constant ? dyn_cast<ConstantInt>(constant->getValue()) : nullptr;
+  if (!integer) fail("BD-E-ENTRY-RUNTIME", ("integer module flag required: " + name).str());
+  return integer->getZExtValue();
+}
+bool prepareScalarModule(Module &m, Function &f, uint64_t &sstack, unsigned autoSnapshot) {
   // This module is the private device clone. Retain symbols/addresses for
   // native-only definitions but do not send their bodies through N0.
   {
     Analysis selection(m,&f);selection.run();
     selection.releaseTransferGraphs();
-    for(auto &g:m)if(!g.isDeclaration() && selection.tiers[&g].empty())g.deleteBody();
-    for(auto &g:m)if(!g.isDeclaration() && selection.tiers[&g]==std::set<std::string>{"H"})g.deleteBody();
+    std::set<const Function *> deviceClosure;
+    std::function<void(Function *)> retain = [&](Function *function) {
+      if (!deviceClosure.insert(function).second || function->isDeclaration()) return;
+      for (auto &instruction : instructions(function))
+        if (auto *call = dyn_cast<CallBase>(&instruction)) {
+          if (auto *callee = call->getCalledFunction()) retain(callee);
+          else for (auto *callee : selection.candidates(call->getCalledOperand(), call->getFunctionType())) retain(callee);
+        }
+    };
+    retain(&f);
+    for (auto entry : {std::make_pair("bennett.entry.snapshot", "__bennett_rt_entry_replay"),
+                       std::make_pair("bennett.ss.init", "__bennett_rt_ss_init")}) {
+      if (!scalarModuleFlag(m, entry.first, 0)) continue;
+      auto *function = m.getFunction(entry.second);
+      if (!function || function->isDeclaration())
+        fail("BD-E-ENTRY-RUNTIME", std::string("missing linked definition for ") + entry.second, &f);
+      retain(function);
+    }
+    for(auto &g:m)if(!g.isDeclaration() && !deviceClosure.count(&g) && selection.tiers[&g].empty())g.deleteBody();
+    for(auto &g:m)if(!g.isDeclaration() && !deviceClosure.count(&g) && selection.tiers[&g]==std::set<std::string>{"H"})g.deleteBody();
   }
   if(auto *md=m.getModuleFlag("bennett.sstack"))sstack=cast<ConstantInt>(cast<ConstantAsMetadata>(md)->getValue())->getZExtValue();
   if(autoSnapshot && m.getGlobalVariable("__bennett_ss_base",true))m.addModuleFlag(Module::Error,"bennett.entry.stack",uint32_t(1));
@@ -711,20 +751,17 @@ void lowerScalar(Module &m, Function &f, StringRef desc, StringRef out,
   normaliseWideABI(m);
   // Materialise every linked member before computing candidates and read dependencies.
   for (Function &g:m) if(!g.isDeclaration()) {normaliseScalar(g);materialiseFPBits(g);}
-  // The command/descriptor-selected internal oracle is an invocation entry,
-  // even when the input module has no host marker referring to it. PT11 must
-  // seed its parameters before the same fixpoint computes indirect domains.
-  Analysis analysis(m, &f); analysis.run();
-  std::vector<Function *> closure;
-  std::map<Function *,std::string> functions;
-  std::function<void(Function *)> collect=[&](Function *g) {
-    if(!g) return;
+  return singleFrame;
+}
+void collectScalarFunction(Function *g, Analysis &analysis,
+                           std::vector<Function *> &closure, std::map<Function *,std::string> &functions) {
+    if(!g) fail("BD-E-ENTRY-RUNTIME", "required scalar runtime helper is missing");
     requireSoftFloat(*g);
     if(g->isDeclaration() || functions.count(g)) return;
     functions[g]="L"+std::to_string(functions.size()+1);closure.push_back(g);
     for(Instruction &i:instructions(g)) if(auto *c=dyn_cast<CallBase>(&i)) {
-      if(auto *target=c->getCalledFunction()) collect(target);
-      else if(auto *target=resolve(c->getCalledOperand())) collect(target);
+      if(auto *target=c->getCalledFunction()) collectScalarFunction(target, analysis, closure, functions);
+      else if(auto *target=resolve(c->getCalledOperand())) collectScalarFunction(target, analysis, closure, functions);
       else {
         auto targets=analysis.candidates(c->getCalledOperand(),c->getFunctionType());
         std::vector<Function *> sorted(targets.begin(),targets.end());
@@ -733,21 +770,166 @@ void lowerScalar(Module &m, Function &f, StringRef desc, StringRef out,
             if(auto n=comparisonFunctionAddress(*f))return *n;
             if(hasComparisonLayout())fail("BD-E-COMPARISON-LAYOUT","missing function address",f);
             auto *md=f->getMetadata("bennett.address");if(!md) unimplemented("§19.5 comparison function addresses",4,f);return cast<ConstantInt>(cast<ConstantAsMetadata>(md->getOperand(0))->getValue())->getZExtValue();};return address(a)<address(b);
-        });for(auto *target:sorted) collect(target);
+        });for(auto *target:sorted) collectScalarFunction(target, analysis, closure, functions);
+      }
+    }
+}
+struct ScalarPublication {
+  std::vector<std::string> ins, mems, args, wrapperRegs, wrapperRows, argTypes, insWidths, memSigs;
+  unsigned tgt, stackCells;
+  uint64_t heapLimit;
+  std::vector<std::pair<std::string,uint64_t>> devices;
+  std::map<std::string,std::string> bodies, signatures;
+  std::string lproc;
+  std::vector<Function *> closure;
+};
+void publishScalarObject(Scalar &s, ScalarPublication publication, StringRef out) {
+  auto &[ins, mems, args, wrapperRegs, wrapperRows, argTypes, insWidths, memSigs,
+         tgt, stackCells, heapLimit, devices, bodies, signatures, lproc, closure] = publication;
+  auto &m = s.m;
+  auto &f = s.f;
+  std::string wrapper = "oracle @ref (" + join(ins) + ") (tgt:wire[" +
+                        std::to_string(tgt) + "]) (fault:wire[4]) (" + join(mems) + ") (" +
+                        join(args) + ")\nregs { " + join(wrapperRegs) +
+                        " }\n^entry():\n" + join(wrapperRows, "\n");
+  std::string osig =
+      "{\"abi\":\"0.8\",\"args\":[" + join(argTypes, ",") +
+      "],\"fault\":4,\"in\":[" + join(insWidths, ",") +
+      "],\"kind\":\"oracle\",\"mem\":[" + join(memSigs, ",") + "],\"tgt\":" + std::to_string(tgt) +
+      ",\"tier\":\"q\"}";
+  unsigned sc = 0;
+  while ((uint64_t(1) << sc) < stackCells)
+    ++sc;
+  unsigned pw = m.getDataLayout().getPointerSizeInBits();
+  std::string prefix = "isa=0.8\nptr_width=" + std::to_string(pw) + "\n";
+  // M1 standalone comparison layout: globals in link/module order, data at
+  // 4096, heap at the next page, no heap allocations. Driver-supplied layouts M4.
+  std::map<std::string,std::string> data, globalLeaves, dataSigs, dataHashes;
+  uint64_t nullSize=scalarModuleFlag(m, "bennett.null_size",4096);
+  uint64_t base=nullSize;std::map<const GlobalVariable *,uint64_t> globalBases;
+  for(GlobalVariable &g:m.globals())if(s.globals.count(&g)) {base=alignTo(base,m.getDataLayout().getPreferredAlign(&g));globalBases[&g]=comparisonGlobalAddress(g).value_or(base);base=std::max(base,globalBases[&g]+m.getDataLayout().getTypeAllocSize(g.getValueType()).getFixedValue());}
+  for(GlobalVariable &g:m.globals())if(s.globals.count(&g)) {
+    auto size=m.getDataLayout().getTypeAllocSize(g.getValueType()).getFixedValue();
+    auto hex=scalarGlobalImage(g,globalBases),name=s.globals[&g];
+    data[name]=hex;
+    dataSigs[name]="{\"abi\":\"0.8\",\"kind\":\"data\",\"size\":"+std::to_string(size)+",\"tier\":\"-\"}";
+    dataHashes[name]=sha(prefix+dataSigs[name]+"\n"+name+" "+hex+"\n");
+    globalLeaves[name]="{\"base\":"+std::to_string(globalBases[&g])+",\"image\":\""+name+"\",\"size\":"+std::to_string(size)+"}";
+  }
+  uint64_t heap=comparisonHeapBase().value_or(scalarModuleFlag(m, "bennett.heap_base",alignTo(base,uint64_t(4096))));unsigned h=0,at=0;
+  uint64_t endAddress = scalarModuleFlag(m, "bennett.region_base",heap + heapLimit);
+  std::string regionLayout, regionHashLeaves;
+  for (auto &d : devices) if (d.first == "BLOCK") {
+    uint64_t size = uint64_t(1) << (d.second + 9);
+    uint64_t regionBase = alignTo(endAddress, size);
+    auto leaf = "{\"base\":" + std::to_string(regionBase) + "}";
+    regionLayout = "\"k0\":" + leaf;
+    regionHashLeaves = "layout interface_regions.ref.k0 " + leaf + "\n";
+    endAddress = regionBase + size;
+  }
+  for (auto &mem : mems) {
+    std::smatch parts;
+    if (!std::regex_search(mem, parts, std::regex(R"(([mes][0-9]+):region\[([0-9]+),8\])"))) continue;
+    uint64_t size = uint64_t(1) << std::stoul(parts[2]);
+    auto leaf = "{\"base\":" + std::to_string(alignTo(endAddress, size)) + "}";
+    if (!regionLayout.empty()) regionLayout += ",";
+    regionLayout += "\"" + parts[1].str() + "\":" + leaf;
+    regionHashLeaves += "layout interface_regions.ref." + parts[1].str() + " " + leaf + "\n";
+    endAddress = alignTo(endAddress, size) + size;
+  }
+  while((uint64_t(1)<<h)<endAddress)++h;
+  while((uint64_t(1)<<at)<data.size()+mems.size()+heapLimit)++at;
+  std::string images,globalLayout,globalHashLeaves,dataSection,refs;
+  for(auto &e:data) {
+    images+="data "+e.first+" "+e.second+"\n";
+    if(!globalLayout.empty())globalLayout+=",";
+    globalLayout+="\""+e.first+"\":"+globalLeaves[e.first];
+    globalHashLeaves+="layout globals."+e.first+" "+globalLeaves[e.first]+"\n";
+    dataSection+=e.first+" "+e.second+"\n";
+  }
+  // Hash the complete call graph in SCC dependency order (ISA §9.2).
+  std::map<std::string,std::string> hashes=dataHashes;
+  std::map<std::string,std::set<std::string>> edges;
+  std::regex symbolToken(R"(@([LG][0-9]+)\b)");
+  for(auto &b:bodies) {
+    auto rest=b.second.substr(b.second.find('\n')+1);
+    for(std::sregex_iterator it(rest.begin(),rest.end(),symbolToken),end;it!=end;++it)
+      if(bodies.count((*it)[1]))edges[b.first].insert((*it)[1]);
+  }
+  auto reaches=[&](std::string from,std::string to) {
+    std::set<std::string> seen;std::function<bool(std::string)> walk=[&](std::string n) {if(n==to)return true;if(!seen.insert(n).second)return false;for(auto &v:edges[n])if(walk(v))return true;return false;};return walk(from);
+  };
+  std::function<void(std::string)> hashMember=[&](std::string n) {
+    if(hashes.count(n))return;
+    std::vector<std::string> group;
+    for(auto &b:bodies)if(reaches(n,b.first)&&reaches(b.first,n))group.push_back(b.first);
+    bool cyclic=group.size()>1 || edges[n].count(n);
+    std::set<std::string> members(group.begin(),group.end());
+    for(auto &g:group)for(auto &e:edges[g])if(!members.count(e))hashMember(e);
+    std::string envelopes;
+    for(auto &g:group) {
+      auto newline=bodies[g].find('\n');auto rest=bodies[g].substr(newline+1);
+      std::string canonical=bodies[g].substr(0,newline+1),refs;size_t last=0;std::set<std::string> referenced;
+      for(std::sregex_iterator it(rest.begin(),rest.end(),symbolToken),end;it!=end;++it) {
+        auto v=(*it)[1].str();std::string replacement;
+        if(cyclic && members.count(v)) replacement="$"+std::to_string(std::find(group.begin(),group.end(),v)-group.begin());
+        else {replacement=hashes.at(v);if(referenced.insert(v).second)refs+=replacement+"\n";}
+        canonical+=rest.substr(last,it->position()-last)+"@"+replacement;last=it->position()+it->length();
       }
+      canonical+=rest.substr(last);std::string images,leaves;
+      for(auto &v:data)if(referenced.count(v.first)) {images+="data "+v.first+" "+v.second+"\n";leaves+="layout globals."+v.first+" "+globalLeaves[v.first]+"\n";}
+      envelopes+=prefix+signatures[g]+"\n"+canonical+"\n"+images+leaves+refs;
     }
+    auto h=sha(envelopes);
+    for(unsigned i=0;i<group.size();++i)hashes[group[i]]=cyclic?sha(h+":"+std::to_string(i)):h;
   };
-  auto flag=[&](StringRef name,uint64_t fallback) {auto *md=m.getModuleFlag(name);return md?cast<ConstantInt>(cast<ConstantAsMetadata>(md)->getValue())->getZExtValue():fallback;};
-  sstack=flag("bennett.sstack",sstack);
-  unsigned snapshot=flag("bennett.entry.snapshot",0);
-  bool initialise=flag("bennett.ss.init",0) || flag("bennett.entry.stack",0);
-  if(snapshot) collect(m.getFunction("__bennett_rt_entry_replay"));
-  for(auto &g:m)for(auto &i:instructions(g))if(auto *c=dyn_cast<CallBase>(&i))if(c->getCalledFunction() && c->getCalledFunction()->getName()=="__bennett_rt_ss_push")initialise=true;
-  if(initialise)collect(m.getFunction("__bennett_rt_ss_init"));
-  collect(&f);
-  Scalar s{m, f}; s.functions=functions;s.analysis=&analysis;
-  std::string d = desc.str(), device;
-  uint64_t deviceSize = 0, heapLimit = heapCapacity;
+  for(auto &b:bodies)hashMember(b.first);
+  std::string canonical, wrapperRefs; size_t last = 0; std::set<std::string> referenced;
+  std::regex wrapperToken(R"(@(L[0-9]+|G[0-9]+)\b)");
+  for (std::sregex_iterator it(wrapper.begin(),wrapper.end(),wrapperToken),end;it!=end;++it) {
+    auto n = it->str().substr(1), hash = hashes.at(n);
+    if (referenced.insert(n).second) wrapperRefs += hash + "\n";
+    canonical += wrapper.substr(last,it->position()-last) + "@" + hash;
+    last = it->position()+it->length();
+  }
+  canonical += wrapper.substr(last);
+  std::string leaves="layout A_tab "+std::to_string(at)+"\nlayout H "+std::to_string(h)+"\nlayout S_cells "+std::to_string(sc)+"\n"+globalHashLeaves+
+    "layout heap_base "+std::to_string(heap)+"\nlayout heap_limit_max "+std::to_string(heapLimit)+"\n"+regionHashLeaves+"layout null_size "+std::to_string(nullSize)+"\nlayout ptr_width "+std::to_string(pw)+"\n";
+  std::string oh=sha(prefix+osig+"\n"+canonical+"\n"+images+leaves+wrapperRefs);
+  std::string symbols="{\"0\":{\"interface_hash\":\""+oh+"\",\"kind\":\"oracle\",\"name\":\"ref\",\"signature\":"+osig+"}";
+  unsigned si=1;
+  for(auto *g:closure) {auto n=s.functions.at(g);symbols+=",\""+std::to_string(si++)+"\":{\"interface_hash\":\""+hashes[n]+"\",\"kind\":\"lproc\",\"name\":\""+n+"\",\"signature\":"+signatures[n]+"}";}
+  for(auto &e:data)symbols+=",\""+std::to_string(si++)+"\":{\"interface_hash\":\""+dataHashes[e.first]+"\",\"kind\":\"data\",\"name\":\""+e.first+"\",\"signature\":"+dataSigs[e.first]+"}";
+  symbols+="}";
+  auto parsedSymbols=json::parse(symbols);if(!parsedSymbols)fail("output",toString(parsedSymbols.takeError()));
+  symbols=canonicalJSON(*parsedSymbols);
+  std::string layout="{\"A_tab\":"+std::to_string(at)+",\"H\":"+std::to_string(h)+",\"S_cells\":"+std::to_string(sc)+",\"globals\":{"+globalLayout+"},\"heap_base\":"+std::to_string(heap)+",\"heap_limit_max\":"+std::to_string(heapLimit)+",\"interface_regions\":{\"ref\":{"+regionLayout+"}},\"null_size\":"+std::to_string(nullSize)+",\"ptr_width\":"+std::to_string(pw)+"}";
+  // Every successfully materialised L closure is independently read before
+  // publishing an object. This is after all producers and object construction,
+  // so unimplemented source transforms retain their own capability diagnostic.
+  // H functions in the private whole-program module are not L variants.
+  std::set<Function *> variants(closure.begin(),closure.end());
+  validateResidual(m,false,&variants);
+  errs()<<"bennett: residual validator accepted L closure ("<<variants.size()<<" functions)\n";
+  if (auto ec = sys::fs::create_directories(out))
+    fail("output", ec.message());
+  SmallString<256> path(out);
+  sys::path::append(path, "ref.bennett");
+  std::error_code ec;
+  raw_fd_ostream o(path, ec);
+  if (ec)
+    fail("output", ec.message());
+  o << "bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 "
+       "coverage=0.8 target=0.8 ptr_width="
+    << pw << "\n\nsection symbols\n"
+    << symbols << "\n\nsection functions\n"
+    << wrapper << "\n"
+    << lproc << (dataSection.empty() ? "" : "\n\nsection data\n" + StringRef(dataSection).rtrim().str()) << "\n\nsection layout\n"
+    << layout << "\n";
+  errs() << "bennett: scalar reference object " << path << "\n";
+}
+std::vector<std::pair<std::string,uint64_t>> scalarDevices(std::string &d, Function &f) {
+  std::string device;
   if (StringRef(d).starts_with("dev=")) d=";"+d;
   auto deviceStart = d.find(";dev=");
   if (deviceStart != std::string::npos) {
@@ -765,6 +947,47 @@ void lowerScalar(Module &m, Function &f, StringRef desc, StringRef out,
       devices.push_back({dev[1],std::stoull(dev[2])});
     }
   }
+  return devices;
+}
+struct ScalarMembers {
+  std::map<std::string,std::string> bodies, signatures;
+  std::string text;
+};
+ScalarMembers scalarMembers(Scalar &s, const std::vector<Function *> &closure,
+                            Analysis &analysis, const std::map<Function *,std::string> &functions) {
+  auto &m = s.m;
+  ScalarMembers members;
+  for(auto *g:closure) {
+    Scalar member{m,*g};member.globals=s.globals;member.functions=functions;member.analysis=&analysis;
+    auto name=functions.at(g);members.bodies[name]=member.body();
+    std::vector<std::string> widths;for(auto &a:g->args())for(auto &field:member.fields(a.getType()))widths.push_back(std::to_string(member.width(field.type)));
+    members.signatures[name]="{\"abi\":\"0.8\",\"kind\":\"lproc\",\"params\":["+join(widths,",")+"],\"result\":"+std::to_string(member.width(g->getReturnType()))+",\"tier\":\"q\"}";
+    if(!members.text.empty())members.text+="\n";members.text+=members.bodies[name];
+  }
+  return members;
+}
+void lowerScalar(Module &m, Function &f, StringRef desc, StringRef out,
+                 unsigned stackCells, uint64_t heapCapacity, int projection, std::map<std::string,std::string> *globalNames, uint64_t sstack, unsigned autoSnapshot) {
+  bool singleFrame = prepareScalarModule(m, f, sstack, autoSnapshot);
+  // The command/descriptor-selected internal oracle is an invocation entry,
+  // even when the input module has no host marker referring to it. PT11 must
+  // seed its parameters before the same fixpoint computes indirect domains.
+  Analysis analysis(m, &f); analysis.run();
+  std::vector<Function *> closure;
+  std::map<Function *,std::string> functions;
+
+
+  sstack=scalarModuleFlag(m, "bennett.sstack",sstack);
+  unsigned snapshot=scalarModuleFlag(m, "bennett.entry.snapshot",0);
+  bool initialise=scalarModuleFlag(m, "bennett.ss.init",0) || scalarModuleFlag(m, "bennett.entry.stack",0);
+  if(snapshot) collectScalarFunction(m.getFunction("__bennett_rt_entry_replay"), analysis, closure, functions);
+  for(auto &g:m)for(auto &i:instructions(g))if(auto *c=dyn_cast<CallBase>(&i))if(c->getCalledFunction() && c->getCalledFunction()->getName()=="__bennett_rt_ss_push")initialise=true;
+  if(initialise)collectScalarFunction(m.getFunction("__bennett_rt_ss_init"), analysis, closure, functions);
+  collectScalarFunction(&f, analysis, closure, functions);
+  Scalar s{m, f}; s.functions=functions;s.analysis=&analysis;
+  std::string d = desc.str();
+  uint64_t heapLimit = heapCapacity;
+  auto devices = scalarDevices(d, f);
   auto hasDevice = [&](StringRef name) { for (auto &d : devices) if (d.first == name) return true; return false; };
   std::set<const GlobalVariable *> used;
   std::set<const Value *> seen;
@@ -973,15 +1196,7 @@ void lowerScalar(Module &m, Function &f, StringRef desc, StringRef out,
   bool returnDiscard = discard;
   if (discard)
     tgt = 1;
-  std::map<std::string,std::string> bodies, signatures;
-  std::string lproc;
-  for(auto *g:closure) {
-    Scalar member{m,*g};member.globals=s.globals;member.functions=functions;member.analysis=&analysis;
-    auto name=functions[g];bodies[name]=member.body();
-    std::vector<std::string> widths;for(auto &a:g->args())for(auto &field:member.fields(a.getType()))widths.push_back(std::to_string(member.width(field.type)));
-    signatures[name]="{\"abi\":\"0.8\",\"kind\":\"lproc\",\"params\":["+join(widths,",")+"],\"result\":"+std::to_string(member.width(g->getReturnType()))+",\"tier\":\"q\"}";
-    if(!lproc.empty())lproc+="\n";lproc+=bodies[name];
-  }
+  auto members = scalarMembers(s, closure, analysis, functions);
   wrapperRegs.push_back("r:reg[" + std::to_string(ret) + "]");
   wrapperRows.push_back("r = lift.call @" + functions.at(&f) + " (" + join(invoke) + ")");
   if (projection >= 0) {
@@ -1040,147 +1255,11 @@ void lowerScalar(Module &m, Function &f, StringRef desc, StringRef out,
   }
   else
     wrapperRows.push_back("lift.retval r");
-  std::string wrapper = "oracle @ref (" + join(ins) + ") (tgt:wire[" +
-                        std::to_string(tgt) + "]) (fault:wire[4]) (" + join(mems) + ") (" +
-                        join(args) + ")\nregs { " + join(wrapperRegs) +
-                        " }\n^entry():\n" + join(wrapperRows, "\n");
-  std::string lsig = "{\"abi\":\"0.8\",\"kind\":\"lproc\",\"params\":[" +
-                     join(paramWidths, ",") +
-                     "],\"result\":" + std::to_string(ret) + ",\"tier\":\"q\"}";
-  std::string osig =
-      "{\"abi\":\"0.8\",\"args\":[" + join(argTypes, ",") +
-      "],\"fault\":4,\"in\":[" + join(insWidths, ",") +
-      "],\"kind\":\"oracle\",\"mem\":[" + join(memSigs, ",") + "],\"tgt\":" + std::to_string(tgt) +
-      ",\"tier\":\"q\"}";
-  unsigned sc = 0;
-  while ((uint64_t(1) << sc) < stackCells)
-    ++sc;
-  unsigned pw = m.getDataLayout().getPointerSizeInBits();
-  std::string prefix = "isa=0.8\nptr_width=" + std::to_string(pw) + "\n";
-  // M1 standalone comparison layout: globals in link/module order, data at
-  // 4096, heap at the next page, no heap allocations. Driver-supplied layouts M4.
-  std::map<std::string,std::string> data, globalLeaves, dataSigs, dataHashes;
-  uint64_t nullSize=flag("bennett.null_size",4096);
-  uint64_t base=nullSize;std::map<const GlobalVariable *,uint64_t> globalBases;
-  for(GlobalVariable &g:m.globals())if(s.globals.count(&g)) {base=alignTo(base,m.getDataLayout().getPreferredAlign(&g));globalBases[&g]=comparisonGlobalAddress(g).value_or(base);base=std::max(base,globalBases[&g]+m.getDataLayout().getTypeAllocSize(g.getValueType()).getFixedValue());}
-  for(GlobalVariable &g:m.globals())if(s.globals.count(&g)) {
-    auto size=m.getDataLayout().getTypeAllocSize(g.getValueType()).getFixedValue();
-    auto hex=scalarGlobalImage(g,globalBases),name=s.globals[&g];
-    data[name]=hex;
-    dataSigs[name]="{\"abi\":\"0.8\",\"kind\":\"data\",\"size\":"+std::to_string(size)+",\"tier\":\"-\"}";
-    dataHashes[name]=sha(prefix+dataSigs[name]+"\n"+name+" "+hex+"\n");
-    globalLeaves[name]="{\"base\":"+std::to_string(globalBases[&g])+",\"image\":\""+name+"\",\"size\":"+std::to_string(size)+"}";
-  }
-  uint64_t heap=comparisonHeapBase().value_or(flag("bennett.heap_base",alignTo(base,uint64_t(4096))));unsigned h=0,at=0;
-  uint64_t endAddress = flag("bennett.region_base",heap + heapLimit);
-  std::string regionLayout, regionHashLeaves;
-  for (auto &d : devices) if (d.first == "BLOCK") {
-    uint64_t size = uint64_t(1) << (d.second + 9);
-    uint64_t regionBase = alignTo(endAddress, size);
-    auto leaf = "{\"base\":" + std::to_string(regionBase) + "}";
-    regionLayout = "\"k0\":" + leaf;
-    regionHashLeaves = "layout interface_regions.ref.k0 " + leaf + "\n";
-    endAddress = regionBase + size;
-  }
-  for (auto &mem : mems) {
-    std::smatch parts;
-    if (!std::regex_search(mem, parts, std::regex(R"(([mes][0-9]+):region\[([0-9]+),8\])"))) continue;
-    uint64_t size = uint64_t(1) << std::stoul(parts[2]);
-    auto leaf = "{\"base\":" + std::to_string(alignTo(endAddress, size)) + "}";
-    if (!regionLayout.empty()) regionLayout += ",";
-    regionLayout += "\"" + parts[1].str() + "\":" + leaf;
-    regionHashLeaves += "layout interface_regions.ref." + parts[1].str() + " " + leaf + "\n";
-    endAddress = alignTo(endAddress, size) + size;
-  }
-  while((uint64_t(1)<<h)<endAddress)++h;
-  while((uint64_t(1)<<at)<data.size()+mems.size()+heapLimit)++at;
-  std::string images,globalLayout,globalHashLeaves,dataSection,refs;
-  for(auto &e:data) {
-    images+="data "+e.first+" "+e.second+"\n";
-    if(!globalLayout.empty())globalLayout+=",";
-    globalLayout+="\""+e.first+"\":"+globalLeaves[e.first];
-    globalHashLeaves+="layout globals."+e.first+" "+globalLeaves[e.first]+"\n";
-    dataSection+=e.first+" "+e.second+"\n";
-  }
-  // Hash the complete call graph in SCC dependency order (ISA §9.2).
-  std::map<std::string,std::string> hashes=dataHashes;
-  std::map<std::string,std::set<std::string>> edges;
-  std::regex symbolToken(R"(@([LG][0-9]+)\b)");
-  for(auto &b:bodies) {
-    auto rest=b.second.substr(b.second.find('\n')+1);
-    for(std::sregex_iterator it(rest.begin(),rest.end(),symbolToken),end;it!=end;++it)
-      if(bodies.count((*it)[1]))edges[b.first].insert((*it)[1]);
-  }
-  auto reaches=[&](std::string from,std::string to) {
-    std::set<std::string> seen;std::function<bool(std::string)> walk=[&](std::string n) {if(n==to)return true;if(!seen.insert(n).second)return false;for(auto &v:edges[n])if(walk(v))return true;return false;};return walk(from);
-  };
-  std::function<void(std::string)> hashMember=[&](std::string n) {
-    if(hashes.count(n))return;
-    std::vector<std::string> group;
-    for(auto &b:bodies)if(reaches(n,b.first)&&reaches(b.first,n))group.push_back(b.first);
-    bool cyclic=group.size()>1 || edges[n].count(n);
-    std::set<std::string> members(group.begin(),group.end());
-    for(auto &g:group)for(auto &e:edges[g])if(!members.count(e))hashMember(e);
-    std::string envelopes;
-    for(auto &g:group) {
-      auto newline=bodies[g].find('\n');auto rest=bodies[g].substr(newline+1);
-      std::string canonical=bodies[g].substr(0,newline+1),refs;size_t last=0;std::set<std::string> referenced;
-      for(std::sregex_iterator it(rest.begin(),rest.end(),symbolToken),end;it!=end;++it) {
-        auto v=(*it)[1].str();std::string replacement;
-        if(cyclic && members.count(v)) replacement="$"+std::to_string(std::find(group.begin(),group.end(),v)-group.begin());
-        else {replacement=hashes.at(v);if(referenced.insert(v).second)refs+=replacement+"\n";}
-        canonical+=rest.substr(last,it->position()-last)+"@"+replacement;last=it->position()+it->length();
-      }
-      canonical+=rest.substr(last);std::string images,leaves;
-      for(auto &v:data)if(referenced.count(v.first)) {images+="data "+v.first+" "+v.second+"\n";leaves+="layout globals."+v.first+" "+globalLeaves[v.first]+"\n";}
-      envelopes+=prefix+signatures[g]+"\n"+canonical+"\n"+images+leaves+refs;
-    }
-    auto h=sha(envelopes);
-    for(unsigned i=0;i<group.size();++i)hashes[group[i]]=cyclic?sha(h+":"+std::to_string(i)):h;
-  };
-  for(auto &b:bodies)hashMember(b.first);
-  std::string canonical, wrapperRefs; size_t last = 0; std::set<std::string> referenced;
-  std::regex wrapperToken(R"(@(L[0-9]+|G[0-9]+)\b)");
-  for (std::sregex_iterator it(wrapper.begin(),wrapper.end(),wrapperToken),end;it!=end;++it) {
-    auto n = it->str().substr(1), hash = hashes.at(n);
-    if (referenced.insert(n).second) wrapperRefs += hash + "\n";
-    canonical += wrapper.substr(last,it->position()-last) + "@" + hash;
-    last = it->position()+it->length();
-  }
-  canonical += wrapper.substr(last);
-  std::string leaves="layout A_tab "+std::to_string(at)+"\nlayout H "+std::to_string(h)+"\nlayout S_cells "+std::to_string(sc)+"\n"+globalHashLeaves+
-    "layout heap_base "+std::to_string(heap)+"\nlayout heap_limit_max "+std::to_string(heapLimit)+"\n"+regionHashLeaves+"layout null_size "+std::to_string(nullSize)+"\nlayout ptr_width "+std::to_string(pw)+"\n";
-  std::string oh=sha(prefix+osig+"\n"+canonical+"\n"+images+leaves+wrapperRefs);
-  std::string symbols="{\"0\":{\"interface_hash\":\""+oh+"\",\"kind\":\"oracle\",\"name\":\"ref\",\"signature\":"+osig+"}";
-  unsigned si=1;
-  for(auto *g:closure) {auto n=functions[g];symbols+=",\""+std::to_string(si++)+"\":{\"interface_hash\":\""+hashes[n]+"\",\"kind\":\"lproc\",\"name\":\""+n+"\",\"signature\":"+signatures[n]+"}";}
-  for(auto &e:data)symbols+=",\""+std::to_string(si++)+"\":{\"interface_hash\":\""+dataHashes[e.first]+"\",\"kind\":\"data\",\"name\":\""+e.first+"\",\"signature\":"+dataSigs[e.first]+"}";
-  symbols+="}";
-  auto parsedSymbols=json::parse(symbols);if(!parsedSymbols)fail("output",toString(parsedSymbols.takeError()));
-  symbols=canonicalJSON(*parsedSymbols);
-  std::string layout="{\"A_tab\":"+std::to_string(at)+",\"H\":"+std::to_string(h)+",\"S_cells\":"+std::to_string(sc)+",\"globals\":{"+globalLayout+"},\"heap_base\":"+std::to_string(heap)+",\"heap_limit_max\":"+std::to_string(heapLimit)+",\"interface_regions\":{\"ref\":{"+regionLayout+"}},\"null_size\":"+std::to_string(nullSize)+",\"ptr_width\":"+std::to_string(pw)+"}";
-  // Every successfully materialised L closure is independently read before
-  // publishing an object. This is after all producers and object construction,
-  // so unimplemented source transforms retain their own capability diagnostic.
-  // H functions in the private whole-program module are not L variants.
-  std::set<Function *> variants(closure.begin(),closure.end());
-  validateResidual(m,false,&variants);
-  errs()<<"bennett: residual validator accepted L closure ("<<variants.size()<<" functions)\n";
-  if (auto ec = sys::fs::create_directories(out))
-    fail("output", ec.message());
-  SmallString<256> path(out);
-  sys::path::append(path, "ref.bennett");
-  std::error_code ec;
-  raw_fd_ostream o(path, ec);
-  if (ec)
-    fail("output", ec.message());
-  o << "bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 "
-       "coverage=0.8 target=0.8 ptr_width="
-    << pw << "\n\nsection symbols\n"
-    << symbols << "\n\nsection functions\n"
-    << wrapper << "\n"
-    << lproc << (dataSection.empty() ? "" : "\n\nsection data\n" + StringRef(dataSection).rtrim().str()) << "\n\nsection layout\n"
-    << layout << "\n";
-  errs() << "bennett: scalar reference object " << path << "\n";
+  publishScalarObject(s, {
+      std::move(ins), std::move(mems), std::move(args), std::move(wrapperRegs),
+      std::move(wrapperRows), std::move(argTypes), std::move(insWidths), std::move(memSigs),
+      tgt, stackCells, heapLimit, std::move(devices), std::move(members.bodies),
+      std::move(members.signatures), std::move(members.text), std::move(closure)}, out);
+
 }
 } // namespace bennett
````

## 2. Changed source files at 2ecdd90

# Changed source of job/quality-plugin at 2ecdd90

Snapshot of `plugin-stage/` at commit `2ecdd90da9b174186a1305fdb8587d2f19884ddc`. 16 files; each embedded verbatim below. Line counts and sha256 per file:

- `CMakeLists.txt` 63 lines, sha256 828544a192ea
- `SPEC_VERSIONS.toml` 23 lines, sha256 16b912379ff9
- `gate.toml` 86 lines, sha256 883f939b07c5
- `scripts/build` 36 lines, sha256 386b21cd9d09
- `scripts/coverage` 67 lines, sha256 6362f782b2ee
- `scripts/gate` 66 lines, sha256 9d57173f66f8
- `scripts/quality.py` 210 lines, sha256 ec251a633643
- `scripts/record-verification.py` 219 lines, sha256 8135114ac4fd
- `scripts/test` 91 lines, sha256 a16abbdf15f0
- `src/BennettPlugin.cpp` 471 lines, sha256 e8d516e9faf2
- `src/Production.cpp` 2895 lines, sha256 49c80960cf08
- `src/Reversible.inc` 153 lines, sha256 821e4c949c00
- `src/Scalar.cpp` 1265 lines, sha256 467795639673
- `tests/normalisation_check.cpp` 66 lines, sha256 7493e5d62a43
- `tests/normalisation_scope.py` 91 lines, sha256 93943c0a1164
- `tests/review_regressions.py` 1001 lines, sha256 e3630e545d54

Total embedded: 6803 lines.

## `CMakeLists.txt` (63 lines)

````
cmake_minimum_required(VERSION 3.20)
project(bennett-plugin LANGUAGES C CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
option(BENNETT_COVERAGE "Instrument a single LLVM-major GCC build with gcov" OFF)
if(BENNETT_COVERAGE AND NOT LLVM_DIR)
  message(FATAL_ERROR "Set LLVM_DIR to select one major for coverage")
endif()
if(NOT LLVM_DIR)
  include(ExternalProject)
  foreach(major 18 23)
    ExternalProject_Add(llvm${major}
      SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}"
      BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}/llvm${major}"
      CMAKE_ARGS -DLLVM_DIR=/usr/lib/llvm-${major}/lib/cmake/llvm
        -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBENNETT_OUTPUT_DIR=${CMAKE_CURRENT_BINARY_DIR}
      INSTALL_COMMAND "" BUILD_ALWAYS TRUE)
  endforeach()
else()
  find_package(LLVM REQUIRED CONFIG)
  if(NOT LLVM_VERSION_MAJOR MATCHES "^(18|23)$")
    message(FATAL_ERROR "Tested LLVM majors are 18 and 23")
  endif()
  add_library(BennettPlugin MODULE src/BennettPlugin.cpp src/NativeComparison.cpp src/Analysis.cpp src/Scalar.cpp src/Normalise.cpp src/SoftFloat.cpp src/Wide.cpp src/Integer.cpp src/Memory.cpp src/Residual.cpp src/Production.cpp src/Snapshot.cpp)
  if(BENNETT_COVERAGE)
    if(NOT CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
      message(FATAL_ERROR "BENNETT_COVERAGE requires GCC and matching gcov")
    endif()
    target_compile_options(BennettPlugin PRIVATE --coverage -O0 -g1)
    target_link_options(BennettPlugin PRIVATE --coverage)
  endif()
  target_include_directories(BennettPlugin SYSTEM PRIVATE ${LLVM_INCLUDE_DIRS})
  target_compile_definitions(BennettPlugin PRIVATE ${LLVM_DEFINITIONS})
  set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS
    "${CMAKE_CURRENT_SOURCE_DIR}/SPEC_VERSIONS.toml"
    "${CMAKE_CURRENT_SOURCE_DIR}/gate.toml"
    "${CMAKE_CURRENT_SOURCE_DIR}/tests/contracts.py"
    "${CMAKE_CURRENT_SOURCE_DIR}/tests/pinned_siblings.py")
  find_package(Python3 REQUIRED COMPONENTS Interpreter)
  execute_process(
    COMMAND "${Python3_EXECUTABLE}" -c
      "import sys; sys.path.insert(0, sys.argv[1] + '/tests'); from contracts import arith_path; print(arith_path(int(sys.argv[2])).absolute())"
      "${CMAKE_CURRENT_SOURCE_DIR}" "${LLVM_VERSION_MAJOR}"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    RESULT_VARIABLE arith_status OUTPUT_VARIABLE arith_path ERROR_VARIABLE arith_error
    OUTPUT_STRIP_TRAILING_WHITESPACE)
  if(NOT arith_status STREQUAL "0")
    message(FATAL_ERROR "Pinned arithmetic LLVM ${LLVM_VERSION_MAJOR} unavailable:\n${arith_error}")
  endif()
  file(READ "${CMAKE_CURRENT_SOURCE_DIR}/SPEC_VERSIONS.toml" spec_pins)
  string(REGEX MATCH "llvm${LLVM_VERSION_MAJOR}_sha256 = \"([^\"]+)\"" arith_pin "${spec_pins}")
  if(NOT arith_pin)
    message(FATAL_ERROR "Missing arith LLVM ${LLVM_VERSION_MAJOR} sha256 pin")
  endif()
  set(arith_sha256 "${CMAKE_MATCH_1}")
  target_compile_definitions(BennettPlugin PRIVATE
    BENNETT_ARITH_DEFAULT_PATH="${arith_path}"
    BENNETT_ARITH_DEFAULT_SHA256="${arith_sha256}")
  set_target_properties(BennettPlugin PROPERTIES OUTPUT_NAME bennett-plugin-${LLVM_VERSION_MAJOR})
  if(BENNETT_OUTPUT_DIR)
    set_target_properties(BennettPlugin PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${BENNETT_OUTPUT_DIR}")
  endif()
endif()
````

## `SPEC_VERSIONS.toml` (23 lines)

````toml
status = "milestone-1-in-progress"
dialect = "0.2.13"
isa = "0.8"
dialect_sha256 = "803c2e5589fb26ddba322206a08e8759a38c23bd7eded5c31ed0ad99ba4bda15"
[specs]
"bennett-dialect-spec" = "0.2.13"
"bennett-isa-spec" = "0.8"
[commits]
"bennett-dialect-spec" = "1c29c8d731228b67902c3fa72e410e1bb71d16b4"
[arith]
commit = "5e9b4509f3ee3f95ac9f7d22b43359e72cf9fdab"
llvm18_path = ".tmp/gate/cache/bennett-arith@5e9b4509f3ee/bennett-arith/dist/llvm18/bennett-arith.bc"
llvm18_sha256 = "a027f16991c06f39eb1305f28da0b1504651791bdd3533888171aa54e704f7ff"
llvm23_path = ".tmp/gate/cache/bennett-arith@5e9b4509f3ee/bennett-arith/dist/llvm23/bennett-arith.bc"
llvm23_sha256 = "8216b27231c36d750c326bbaef384011a1bdf7f7dbb717b8b8f5167551163f79"

# Native-only transports/tools; production runtime remains the separate allocator pin.
[native_comparison]
runtime_commit = "248e468ca505c684bbf254e52eb8148f1e530c83"
llvm18_support_sha256 = "c7a1306784e7f487c040b724e2074294ff687f149bf6403a9e403973a833e596"
llvm23_support_sha256 = "f7fee923e2b06d1c4106439e46ed03936a9ee7721d3498d008e298cb5265cade"
checker_script_sha256 = "bb11d8498a8403a415a77910193302b00bb1978d6ee24c0079bab5aa69ab5c2e"
checker_source_sha256 = "a5c383379ce3dcf5a53eca274aa446e968d533c13516a64a9d80dd6e3298828d"
````

## `gate.toml` (86 lines)

````toml
# Push-gate pins (bennett/tools/gate_README.md). Siblings resolve only to these commits.
schema = 1
repo = "bennett-plugin"
tool_sha = "01c0314c9aaa4a37313ab530da2134efafe9cbd5"
timeout_s = 28800

[env]
BENNETT_SIBLINGS = "{layout}"
BENNETT_ARITH_PINNED_ROOT = "{sibling:bennett-arith}/dist"
BENNETT_ALLOCATOR_PINNED_ROOT = "{sibling:bennett-runtimes}/dist"

[[check]]
name = "quality baseline"
argv = ["python3", "-B", "scripts/quality.py", "--check"]

[[check]]
name = "plugin gate"
argv = ["scripts/gate"]

[siblings."bennett-isa-spec"]
sha = "ecaaac060c44e317d1181345fa6b8e38c096c099"
note = "ISA main as gated by the 2026-11-02 push wave"

[[siblings."bennett-isa-spec".build]]
name = "reference interpreter (debug)"
cwd = "reference-interpreter"
argv = ["cargo", "build", "--offline"]
outputs = ["reference-interpreter/target/debug/bennett-isa-ref"]
env = { CARGO_BUILD_JOBS = "3" }

[[siblings."bennett-isa-spec".build]]
name = "reference interpreter (release)"
cwd = "reference-interpreter"
argv = ["cargo", "build", "--offline", "--release"]
outputs = ["reference-interpreter/target/release/bennett-isa-ref"]
env = { CARGO_BUILD_JOBS = "3" }

[siblings."bennett-dialect-spec"]
sha = "1c29c8d731228b67902c3fa72e410e1bb71d16b4"
note = "0.2.13 registry correction required by contract_policy.py; accepted spec text and corpus unchanged from 95a4b8d"

[siblings."bennett-arith"]
sha = "5e9b4509f3ee3f95ac9f7d22b43359e72cf9fdab"
note = "commit named in SPEC_VERSIONS.toml [arith]"
[siblings."bennett-arith".files]
"dist/llvm18/bennett-arith.bc" = "a027f16991c06f39eb1305f28da0b1504651791bdd3533888171aa54e704f7ff"
"dist/llvm23/bennett-arith.bc" = "8216b27231c36d750c326bbaef384011a1bdf7f7dbb717b8b8f5167551163f79"

[siblings."bennett-runtimes"]
sha = "248e468ca505c684bbf254e52eb8148f1e530c83"
note = "publication hashed by tests/allocator_closure.py and tests/reversible.py"
[siblings."bennett-runtimes".files]
"dist/llvm18/bennett-runtimes.bc" = "bbc402fd9b97ce0c5cdf06eff864f77ea4bce22f619a0ad561b081f445f3c67a"
"dist/llvm23/bennett-runtimes.bc" = "78bfc3f4c4ac2d269dc53e03a476fb67283b9d7e63592a6139ad2a7cd7ece884"

[siblings."bennett-native-runtimes"]
sha = "248e468ca505c684bbf254e52eb8148f1e530c83"
repo = "bennett-runtimes"
note = "native-only support and checker publication in SPEC_VERSIONS.toml; allocator stays at its own pin"
[siblings."bennett-native-runtimes".files]
"dist/llvm18/musl-sysroot/lib/native-support.bc" = "c7a1306784e7f487c040b724e2074294ff687f149bf6403a9e403973a833e596"
"dist/llvm23/musl-sysroot/lib/native-support.bc" = "f7fee923e2b06d1c4106439e46ed03936a9ee7721d3498d008e298cb5265cade"
"scripts/native-check" = "bb11d8498a8403a415a77910193302b00bb1978d6ee24c0079bab5aa69ab5c2e"
"scripts/native-check.cpp" = "a5c383379ce3dcf5a53eca274aa446e968d533c13516a64a9d80dd6e3298828d"

[siblings."bennett-vm"]
sha = "805f0ec3481365132d517fefd5b5c12cbd39a845"
note = "freeze the previously live native comparison launch API dependency at its observed HEAD"
[[siblings."bennett-vm".build]]
name = "launch API library (debug)"
argv = ["cargo", "build", "--offline", "--lib", "-j3"]
outputs = ["target/debug/libbennett_vm.so"]
needs = ["bennett-isa-spec"]
[[siblings."bennett-vm".build]]
name = "launch API library (release)"
argv = ["cargo", "build", "--offline", "--release", "--lib", "-j3"]
outputs = ["target/release/libbennett_vm.so"]
needs = ["bennett-isa-spec"]

[siblings."bennett-targets"]
sha = "dd036711936c496f53f6f1a9bebeb686335bf7cc"
note = "pushed publication of ideal-all-to-all.json used by native_comparison.py and native_link.py; identical at 3ef86a56"

[siblings."bennett-conformance"]
sha = "6e6a6f1ebd69f6e81f4f7ea2dd15ea775733e616"
note = "pushed rung-2 fixtures and sha256.json used by native_fixtures.py; identical at e39501e3"
````

## `scripts/build` (36 lines)

````
#!/usr/bin/env python3
"""Offline dual-major build. Uses CMake when present, llvm-config otherwise."""
import concurrent.futures, hashlib, os, shutil, subprocess, sys, tomllib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for key in ['DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','BROWSER']: os.environ.pop(key,None)
(R/'.tmp').mkdir(exist_ok=True);os.environ.setdefault('TMPDIR',str(R/'.tmp'))
sys.path.insert(0, str(R/'tests'))
from contracts import arith_path
arith_paths={major:arith_path(major) for major in (18,23)}
if shutil.which('cmake'):
 subprocess.run(['cmake','-S',str(R),'-B',str(R/'build')],check=True)
 subprocess.run(['cmake','--build',str(R/'build'),'-j','3'],check=True)
else:
 print('cmake unavailable: offline llvm-config build (CMake configuration unverified)',flush=True)
 pins=tomllib.loads((R/'SPEC_VERSIONS.toml').read_text())['arith']
 def build(major):
  tool=Path(f'/usr/lib/llvm-{major}/bin')
  flags=subprocess.check_output([str(tool/'llvm-config'),'--cxxflags'],text=True).split()
  definitions=[f'-DBENNETT_ARITH_DEFAULT_PATH="{arith_paths[major]}"',
               f'-DBENNETT_ARITH_DEFAULT_SHA256="{pins[f"llvm{major}_sha256"]}"']
  compile_flags=[*flags,'-std=c++17','-fPIC','-g','-O2',*definitions]
  dest=R/f'build/llvm{major}';dest.mkdir(parents=True,exist_ok=True)
  objs=[]
  for src in sorted((R/'src').glob('*.cpp')):
   obj=dest/(src.stem+'.o');objs.append(str(obj))
   digest=hashlib.sha256(src.read_bytes()+(R/'src/Bennett.h').read_bytes()+'\0'.join(compile_flags).encode()).hexdigest()
   stamp=obj.with_suffix('.sha256')
   if not obj.exists() or not stamp.exists() or stamp.read_text()!=digest:
    subprocess.run(['g++',*compile_flags,'-c',str(src),'-o',str(obj)],check=True)
    stamp.write_text(digest)
  output=R/f'build/libbennett-plugin-{major}.so'
  temporary=output.with_suffix('.so.new')
  subprocess.run(['g++','-shared',*objs,'-o',str(temporary)],check=True)
  temporary.replace(output)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(build,[18,23]))
````

## `scripts/coverage` (67 lines)

````
#!/usr/bin/env python3
"""Summarise GCC executable-line coverage for plugin sources, without a threshold."""

import argparse
import gzip
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", type=Path, default=ROOT / "build/coverage18")
    args = parser.parse_args()
    notes = sorted(args.build_dir.rglob("*.gcno"))
    if not notes:
        raise SystemExit(f"no instrumented objects under {args.build_dir}")
    destination = ROOT / ".tmp/coverage-report"
    destination.mkdir(parents=True, exist_ok=True)
    files = {}
    for note in notes:
        result = subprocess.run(
            ["gcov", "--json-format", str(note.resolve())],
            cwd=destination,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode:
            raise SystemExit(result.stderr)
        report = destination / (note.stem + ".gcov.json.gz")
        with gzip.open(report, "rt") as stream:
            data = json.load(stream)
        for source in data["files"]:
            path = Path(source["file"]).resolve()
            if not path.is_relative_to(ROOT / "src"):
                continue
            name = str(path.relative_to(ROOT))
            lines = files.setdefault(name, {})
            for line in source["lines"]:
                number = line["line_number"]
                lines[number] = lines.get(number, 0) + line["count"]
    rows = {
        name: {
            "covered": sum(count > 0 for count in lines.values()),
            "lines": len(lines),
        }
        for name, lines in sorted(files.items())
    }
    covered = sum(row["covered"] for row in rows.values())
    total = sum(row["lines"] for row in rows.values())
    if not total:
        raise SystemExit("gcov reports contain no executable plugin source lines")
    result = {
        "covered": covered,
        "lines": total,
        "percent": round(100 * covered / total, 2),
        "files": rows,
    }
    (destination / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
````

## `scripts/gate` (66 lines)

````
#!/usr/bin/env bash
# The full gate, run in the tree this script lives in. Prefer scripts/pre-push, which
# gates a clean checkout of the commit being pushed (or HEAD). Use this directly only
# to iterate on a dirty tree; its results are not a push gate.
set -euo pipefail
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
script_dir="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
root="$(cd "$script_dir/.." && pwd)"
unset DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER
export TMPDIR="${TMPDIR:-$root/.tmp}"
mkdir -p "$TMPDIR"
# Resolve arithmetic before any plugin subprocess inherits its implicit input.
BENNETT_ARITH_PINNED_ROOT="$(python3 - "$root" <<'PYTHON'
import sys
sys.path.insert(0, sys.argv[1]+'/tests')
from contracts import arith_path
for major in (18,23): print(f'arith LLVM {major}: {arith_path(major)}', file=sys.stderr, flush=True)
print(arith_path(18).parent.parent)
PYTHON
)"
export BENNETT_ARITH_PINNED_ROOT
"$root/scripts/build"
python3 "$root/tests/build_defaults.py"
"$root/scripts/test"
for major in 18 23; do
  python3 "$root/tests/analysis_performance.py" --major "$major"
  python3 "$root/tests/reference_images.py" --major "$major"
  python3 "$root/tests/materialisation.py" --major "$major"
  python3 "$root/tests/aggregate_rows.py" --major "$major"
  python3 "$root/tests/allocator_closure.py" --major "$major"
  python3 "$root/tests/native_comparison.py" --major "$major"
  python3 "$root/tests/native_layout.py" --major "$major"
  python3 "$root/tests/native_fixtures.py" --major "$major"
  python3 "$root/tests/native_hello.py" --major "$major"
  python3 "$root/tests/native_checked.py" --major "$major"
  python3 "$root/tests/cc_calls.py" --major "$major"
  python3 "$root/tests/cc_switch.py" --major "$major"
  python3 "$root/tests/reversible.py" --major "$major"
  python3 "$root/tests/softfloat.py" --major "$major"
  python3 "$root/tests/wide.py" --major "$major"
  python3 "$root/tests/integer_intrinsics.py" --major "$major"
  python3 "$root/tests/memory_runtime.py" --major "$major"
  python3 "$root/tests/region_keys.py" --major "$major"
  python3 "$root/tests/key_audit.py" --major "$major"
  python3 "$root/tests/descriptors.py" --major "$major"
  python3 "$root/tests/production.py" --major "$major"
  python3 "$root/tests/production_environments.py" --major "$major" --case memory-handle --case retired-handle --case combined-devices --case multiple-outputs --case heterogeneous-layouts --case pointer-layouts --case return-console --case inplace-inout --case inplace-not-inverse --case inplace-small-budget --case inplace-second-small-budget --case memory-layouts --case wide-output --case unnamed-layouts
  python3 "$root/tests/production_dispatch.py" --major "$major"
  python3 "$root/tests/production_shapes.py" --major "$major"
  python3 "$root/tests/production_budgets.py" --major "$major"
  python3 "$root/tests/budget_stage.py" --major "$major"
  python3 "$root/tests/production_records.py" --major "$major"
  python3 "$root/tests/shadow_stack.py" --major "$major"
  python3 "$root/tests/production_lifts.py" --major "$major" --case entry-replay-byte --case rung4-mini --case rung8-mini --case listsum --case shadow-n24
  python3 "$root/tests/review_regressions.py" --major "$major" --case mixed-native
done
# Independent snapshot executions are CPU-heavy; their artifacts are major-local.
python3 "$root/tests/entry_snapshot.py" --major 18 &
snapshot18=$!
python3 "$root/tests/entry_snapshot.py" --major 23 &
snapshot23=$!
wait "$snapshot18"
wait "$snapshot23"
python3 "$root/tests/production_cross_major.py"
python3 "$root/tests/prior_objects.py"
python3 "$root/tests/corpus_gate.py"
````

## `scripts/quality.py` (210 lines)

````python
#!/usr/bin/env python3
"""Repository-local quality proxies and a ratchet against docs/quality.md."""

import argparse
import ast
import json
import math
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASELINE = re.compile(r"<!-- quality-baseline -->\s*```json\n(.*?)\n```", re.S)
IDENTIFIER = re.compile(
    r"\b(?:bp|bd|b-dialect-spec)-[a-z0-9]+\b|\b(?:sol|quality)-plugin\b"
)
LITTER = re.compile(
    r"(^|/)(__pycache__|PROGRESS[^/]*|LAST-RUN[^/]*)(/|$)|\.(pyc|log|lock|darc)$|(^|/)LOCK$"
)
CONTROL = {"if", "for", "while", "switch", "catch", "sizeof", "alignas"}
TOKENS = re.compile(
    r'//[^\n]*|/\*.*?\*/|R"([^ ()\\\t\r\n]*)\(.*?\)\1"|"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27',
    re.S,
)


def cpp_functions(source):
    masked = TOKENS.sub(lambda match: re.sub(r"[^\n]", " ", match.group()), source)
    stack, functions = [], []
    for match in re.finditer(r"[{}]", masked):
        position = match.start()
        if match.group() == "{":
            boundary = max(masked.rfind(char, 0, position) for char in ";{}") + 1
            header = masked[boundary:position]
            signature = re.search(
                r"([A-Za-z_~]\w*)\s*\([^{};]*\)\s*(?:const|override|noexcept)?\s*$",
                header,
            )
            name = signature.group(1) if signature else None
            stack.append((position, name if name not in CONTROL else None, boundary))
        else:
            if not stack:
                raise ValueError("unbalanced closing brace in C++ source")
            start, name, boundary = stack.pop()
            if name:
                first = (
                    boundary
                    + len(masked[boundary:start])
                    - len(masked[boundary:start].lstrip())
                )
                line = masked.count("\n", 0, first) + 1
                length = masked.count("\n", first, position) + 1
                body = masked[start + 1 : position].strip()
                trivial = bool(re.fullmatch(r"(?:return\s+)?[\w:.]+\([^;{}]*\);", body))
                functions.append(
                    {"name": name, "line": line, "length": length, "trivial": trivial}
                )
    if stack:
        raise ValueError("unbalanced opening brace in C++ source")
    depth, complexity = 0, 0
    for match in re.finditer(
        r"\b(?:if|for|while|switch|catch|else)\b|&&|\|\||\?|[{}]", masked
    ):
        token = match.group()
        if token == "{":
            depth += 1
        elif token == "}":
            depth -= 1
        else:
            complexity += 1 + depth
    return functions, complexity


def python_functions(source):
    tree = ast.parse(source)
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                body = body[1:]
            trivial = (
                len(body) == 1
                and isinstance(body[0], (ast.Return, ast.Expr))
                and isinstance(body[0].value, ast.Call)
            )
            functions.append(
                {
                    "name": node.name,
                    "line": node.lineno,
                    "length": node.end_lineno - node.lineno + 1,
                    "trivial": trivial,
                }
            )
    branches = (
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.ExceptHandler,
        ast.IfExp,
        ast.Match,
    )

    def mass(node, depth=0):
        branch = isinstance(node, branches)
        own = 1 + depth if branch else 0
        if isinstance(node, ast.BoolOp):
            own += len(node.values) - 1
        return own + sum(
            mass(child, depth + branch) for child in ast.iter_child_nodes(node)
        )

    return functions, mass(tree)


def measure(root, paths):
    files, long_functions = {}, []
    process_identifiers = 0
    for name in sorted(paths):
        path = root / name
        if not path.is_file():
            continue
        is_python = path.suffix == ".py" or (
            name.startswith("scripts/")
            and not path.suffix
            and "python" in path.read_text().partition("\n")[0]
        )
        if not is_python and path.suffix not in (".cpp", ".c", ".h", ".inc"):
            continue
        source = path.read_text()
        if name.startswith(("src/", "include/")):
            process_identifiers += len(IDENTIFIER.findall(source))
        if is_python:
            functions, complexity = python_functions(source)
        else:
            functions, complexity = cpp_functions(source)
        lengths = sorted(function["length"] for function in functions)
        percentile = lambda fraction: (
            lengths[math.ceil(fraction * len(lengths)) - 1] if lengths else 0
        )
        files[name] = {
            "functions": len(lengths),
            "length_p50": percentile(0.5),
            "length_p90": percentile(0.9),
            "length_max": max(lengths, default=0),
            "over_300": sum(length > 300 for length in lengths),
            "complexity": complexity,
            "trivial_wrappers": sum(function["trivial"] for function in functions),
        }
        long_functions.extend(
            {"file": name, **function}
            for function in functions
            if function["length"] > 300
        )
    return {
        "files": files,
        "process_identifiers": process_identifiers,
        "litter": sorted(name for name in paths if LITTER.search(name)),
        "long_functions": long_functions,
    }


def regressions(current, baseline):
    failures = []
    for key in ("process_identifiers", "litter"):
        count = lambda value: len(value) if isinstance(value, list) else value
        if count(current[key]) > count(baseline[key]):
            failures.append(f"{key}: {count(baseline[key])} -> {count(current[key])}")
    for name, values in current["files"].items():
        previous = baseline["files"].get(name, {})
        for key, value in values.items():
            if key != "functions" and value > previous.get(key, 0):
                failures.append(f"{name} {key}: {previous.get(key, 0)} -> {value}")
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )
    paths = result.stdout.rstrip("\0").split("\0")
    current = measure(ROOT, paths)
    if args.check:
        match = BASELINE.search((ROOT / "docs/quality.md").read_text())
        if not match:
            raise SystemExit("docs/quality.md has no quality-baseline JSON block")
        failures = regressions(current, json.loads(match.group(1)))
        if failures:
            raise SystemExit("quality baseline worsened:\n" + "\n".join(failures))
        print("quality baseline: no regressions")
    else:
        print(json.dumps(current, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
````

## `scripts/record-verification.py` (219 lines)

````python
#!/usr/bin/env python3
"""Record the latest gate pass into docs/verification.json.

The file keeps only the latest pass.
Full history: `git log -p docs/verification.json`.

Evidence comes from a completed gate run: <root>/.tmp/*.json written by tests/*.py and
<root>/build/*.so. Run the gate first (scripts/gate in the tree), then for example:

  scripts/record-verification.py --pass ninth --date 2026-11-01 --commits abc1234,def5678 --gate-exit 0
"""
import argparse, datetime, hashlib, json, os, re, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'tests'))
from contracts import PIN, sibling, dialect_text, drift

MAJORS = (18, 23)
ISA_REF = sibling('bennett-isa-spec') / 'reference-interpreter/target/debug/bennett-isa-ref'
SUMMARY_KEYS = ('cases_run', 'cases_agree', 'cases_deferred', 'cases_blocked', 'cases_diverge')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gate_counts(summary):
    """run/agree/deferred/blocked/diverge plus cells, per major."""
    return {str(m): '/'.join(str(summary[str(m)][k]) for k in SUMMARY_KEYS) +
            f" cells {summary[str(m)]['cells_agree']}/{summary[str(m)]['cells_run']}" for m in MAJORS}


def check_rows(rows):
    """Count rows whose own recorded verdicts all hold (checks, runs, rejections)."""
    ok = 0
    for r in rows:
        good = r.get('ok', True) and r.get('check', True) and r.get('run', True)
        good = good and all(x.get('ok', True) for x in r.get('runs', []))
        good = good and r.get('common_failure', True)
        ok += bool(good)
    return {'cases': len(rows), 'ok': ok, 'expected_rejections': sum(bool(r.get('expected_rejection')) for r in rows)}


def object_paths(tmp, major, scalars):
    """(name, path) of every emitted object whose cross-major equality is recorded."""
    out = []
    for o in scalars['objects']:
        if o.get('lowered'):
            out.append((f"scalar/{o['name']}", tmp / f"scalars/{major}/{o['name']}/ref.bennett"))
    out.append(('scalar/c-O3-inc8', tmp / f'scalars/{major}/c-inc8/ref.bennett'))
    out.append(('descriptor-reference/inc8', tmp / f'descriptors/{major}/oracle-0/ref.bennett'))
    for rel in ('top/launch.bennett', 'top/oracle-0/ref.bennett'):
        out.append((f'descriptor-production/{rel}', tmp / f'descriptors/{major}/production/{rel}'))
    for case in ('0', '7', '255', 'published'):
        for rel in ('launch.bennett', 'oracle-0/ref.bennett'):
            out.append((f'production/{case}/{rel}', tmp / f'production/{major}/{case}/out/top/{rel}'))
    out.append(('production/abi/launch.bennett', tmp / f'production/{major}/abi/out/abi/launch.bennett'))
    for family in ('production-shapes', 'production-budgets', 'production-dispatch', 'production-environments', 'production-lifts', 'shadow-stack', 'budget-stage', 'entry-snapshot', 'softfloat', 'wide', 'integer-intrinsics', 'memory-runtime', 'aggregate-rows', 'cc-calls', 'cc-switch', 'reversible'):
        base = tmp / f'{family}/{major}'
        for p in sorted(base.rglob('*.bennett')):
            if family=='reversible' and 'r-hello' in p.relative_to(base).parts: continue
            out.append((f'{family}/{p.relative_to(base)}', p))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pass', dest='name', required=True, help='pass name, e.g. ninth')
    ap.add_argument('--date', required=True)
    ap.add_argument('--commits', required=True, help='comma-separated landed commits')
    ap.add_argument('--gate-exit', type=int, required=True)
    ap.add_argument('--root', type=Path, default=R, help='tree whose .tmp/ and build/ the gate used')
    ap.add_argument('--rung3-report', type=Path, help='consumer report, including failed prerequisite rows')
    a = ap.parse_args()
    assert a.gate_exit == 0, 'refusing to record a failed gate'
    tmp, build = a.root / '.tmp', a.root / 'build'
    read = lambda name: json.loads((tmp / name).read_text())
    assert not drift(), 'accepted contract drift'
    gate = read('corpus-gate.json')
    assert gate['dialect_commit'] == PIN and not gate['accepted_contract_drift']
    for major, h in gate['plugin_sha256'].items():
        assert digest(build / f'libbennett-plugin-{major}.so') == h, f'plugin {major} changed after the gate'
    for m in MAJORS:
        s = gate['summary'][str(m)]
        assert [s[k] for k in SUMMARY_KEYS]==[66,66,0,0,0], (m,s)

    checks, scalars = {}, {}
    for m in MAJORS:
        c = {}
        for name in ('recognition', 'analysis-edges', 'analysis-performance', 'reference-images', 'materialisation', 'aggregate-rows', 'allocator-closure', 'cc-calls', 'cc-switch', 'reversible', 'softfloat', 'wide', 'integer-intrinsics', 'memory-runtime', 'region-keys', 'validation'):
            j = read(f'{name}-{m}.json')
            assert j['passed'] == j['cases'], (name, m)
            c[name] = {'cases': j['cases'], 'passed': j['passed']}
            if name in ('aggregate-rows','allocator-closure','cc-calls', 'cc-switch', 'reversible'):c[name]['evidence']=j['results']
            if name=='analysis-performance':
                c[name].update(seconds=j['seconds'],rounds=j['rounds'],budget_diagnostic=j['budget_diagnostic'])
            if name=='softfloat':
                c[name]['known_remainders']=[r for r in j['results'] if r.get('expected_unimplemented')]
                c[name]['native_wide']=[r for r in j['results'] if r['name'].startswith('published-native-wide-')]
                c[name]['recursive_closure']=[r for r in j['results'] if r['name'].startswith('CC-recursive-')]
                c[name]['closure_contract'] = {
                    'rewrite': '§13.1: The entry points are defined by bennett-arith and are part of its bitcode the driver links.',
                    'recursion': '§14.1: Direct calls lower to CC/R call; Recursion is unrestricted.',
                    'transport': '§17.4: LLVM integer and memory instructions map to ISA instructions; phis to block parameters; multi-result calls carry aggregates.',
                    'original_stop': '§13.1 recursive CC soft-float closure: active-set inlining guard at bennett_sf_eval',
                    'llvm23_recursive_instruction': 'call void @bennett_sf_eval(ptr %19, i32 %1, i32 3, ptr %18, i32 0, i32 %5)',
                    'cc_steps_note': 'run-program reports CC steps separately from the nested oracle; successful unchanged 64-wire launch uses two 1000000-step oracle tokens. L numerical rows record nested materialised steps.'}

                c[name]['published_production']=[r for r in j['results'] if r['name'].startswith('published-production')]
        audit = read(f'key-audit-{m}.json')
        assert not audit['unaccounted'] and audit['accounted'] == audit['unmatched']
        c['full-key-audit'] = {k: audit[k] for k in ('cases', 'matched', 'unmatched', 'accounted', 'unaccounted')}
        d = read(f'descriptors-{m}.json')
        assert d['descriptor_inc8_equal'] and d['production_complete'] and d['production_exit'] == 0
        c['descriptors'] = {'descriptor_inc8_equal': True, 'production_complete': True}
        p = read(f'production-{m}.json')
        assert p['passed'] == 3 and p['published_oracle_inc8']['ok'] and p['native_abi']['ok']
        c['production'] = check_rows(p['cases'])
        for fam in ('dispatch', 'environments', 'shapes', 'budgets', 'records', 'lifts'):
            c[f'production-{fam}'] = check_rows(read(f'production-{fam}-{m}.json')['cases'])
            assert c[f'production-{fam}']['cases'] == c[f'production-{fam}']['ok'], (fam, m)
        snapshot = read(f'entry-snapshot-{m}.json')
        assert snapshot['cases'] and all(r.get('ok') and r.get('check') for r in snapshot['cases'])
        c['entry-snapshot'] = check_rows(snapshot['cases'])
        c['entry-snapshot']['isa_ref'] = snapshot['isa_ref']
        c['entry-snapshot']['isa_ref_sha256'] = snapshot['isa_ref_sha256']
        ss = read(f'shadow-stack-{m}.json')
        assert all(r.get('check') and r.get('ok') for r in ss['cases'])
        c['shadow-stack'] = check_rows(ss['cases'])
        stage = read(f'budget-stage-{m}.json')
        assert all(r.get('ok') and r.get('check') for r in stage['cases'])
        assert all(r['ok'] for r in stage['proof_cases'])
        final = next(r for r in stage['cases'] if r['name'] == 'identity-once')
        assert final['reference_exact'] and final['prefix_vectors'] == 316 and final['prefixes_ok'] and final['tokens_final']
        shape = final['build']['budget_table']['shapes'][0]
        c['budget-stage'] = dict(check_rows(stage['cases']), proof_cases=len(stage['proof_cases']),
                                prefix_vectors=316, reference_exact=True, tokens_final=True,
                                selection_identity=shape['selection_identity'], identity=shape['identity'])
        checks[str(m)] = c
        sc = read(f'scalars-{m}.json')
        assert sc['c_inc8_equal'] and sc['passed'] == 21
        lowered = [o for o in sc['objects'] if o.get('lowered')]
        assert all(o['check'] and o['fixture_equal'] and o['hash_fixture_equal'] and all(r['ok'] for r in o['runs']) for o in lowered)
        scalars[str(m)] = {'objects_byte_exact': len(lowered), 'run_vectors': sum(len(o['runs']) for o in lowered),
                           'deferred': sc['deferred'], 'c_inc8_equal': True}
    assert scalars['18'] == scalars['23']

    fixtures = {n: b.encode() for n, b in re.findall(r'```isa object=([^\n ]+)\n(.*?)```', dialect_text(), re.S)}
    for size in (16, 32):
        fixtures[f'budget-stage-{size}'] = (R / f'tests/fixtures/budget-stage-{size}.bennett').read_bytes()
    sc18 = read('scalars-18.json')
    by_major = {m: dict(object_paths(tmp, m, sc18)) for m in MAJORS}
    assert by_major[18].keys() == by_major[23].keys()
    rows = []
    for name, p18 in by_major[18].items():
        data = p18.read_bytes()
        assert data == by_major[23][name].read_bytes(), f'{name}: LLVM 18/23 bytes differ'
        golden = next((g for g, b in fixtures.items() if b == data), None)
        rows.append({'object': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'published_golden': golden})
    cross = read('production-cross-major.json')
    assert cross['byte_identical']
    # Independent check of every launch object (CC lowering is plugin-defined, 17.4: no published golden).
    for name, p18 in by_major[18].items():
        if name.endswith('launch.bennett'):
            r = subprocess.run([str(ISA_REF), 'check', str(p18)], capture_output=True, text=True, timeout=60)
            assert r.returncode == 0, (name, r.stderr)

    path = R / 'docs/verification.json'
    baseline = json.loads(path.read_text()).get('latest_pass', {}).get('object_pairs', {}).get('rows', []) if path.exists() else []
    current = {r['object']: r for r in rows}
    for old in baseline:
        assert old['object'] in current and old['sha256'] == current[old['object']]['sha256'], f"previously recorded object changed: {old['object']}"
    head = subprocess.check_output(['git', '-C', str(a.root), 'rev-parse', 'HEAD'], text=True).strip()
    latest = {
        'name': a.name, 'date': a.date, 'commits': a.commits.split(','), 'code_head': head,
        'recorded_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
        'dialect': '0.2.13', 'dialect_commit': PIN, 'isa': '0.8',
        'arith': __import__('tomllib').loads((R/'SPEC_VERSIONS.toml').read_text())['arith'],
        'arith_gate_paths': {str(m):str(__import__('contracts').arith_path(m)) for m in MAJORS},
        'allocator_gate_root': str(sibling('bennett-runtimes') / 'dist'),
        'plugin_sha256': gate['plugin_sha256'],
        'gate': {'command': 'scripts/gate', 'exit': a.gate_exit, 'accepted_contract_drift': False,
                 'contract_head_drift': gate['contract_head_drift'], 'contract_worktree_drift': gate['contract_worktree_drift'],
                 'corpus': gate_counts(gate['summary']),
                 'non_agreeing': [{k: r[k] for k in ('case', 'major', 'pipeline', 'classification')}
                                  for r in gate['cells'] if r['classification'] != 'agree']},
        'checks': checks, 'scalars': scalars,
        'rung2_analysis': json.loads((R/'docs/rung2-analysis.json').read_text()),
        'object_pairs': {'count': len(rows), 'byte_identical': True,
                         'published_matches': sum(bool(r['published_golden']) for r in rows),
                         'production_cross_major_pairs': cross['pairs'], 'preserved_previous_objects': len(baseline), 'rows': rows},
    }
    if a.rung3_report:
        report = json.loads(a.rung3_report.read_text())
        latest['rung3'] = {'source_report': str(a.rung3_report.resolve()),
                          'source_report_sha256': digest(a.rung3_report),
                          'exit': int(any(row['status'] != 'PASS' for stages in report['stages'].values() for row in stages.values())),
                          'report': report}
    if a.name == 'bp-ivy' and (tmp/'r-hello23-execution.json').is_file():
        obj = tmp/'reversible/23/r-hello/out/main/launch.bennett'
        checked = read('r-hello23-check.log')
        assert checked['object_hash'] == digest(obj), 'exploratory object changed after execution'
        latest['whole_program_r_exploratory'] = {
            'major': 23, 'classification': 'measured failure, not corpus agreement',
            'object_sha256': digest(obj), 'admission': checked['status'],
            'command': ['bennett-isa-spec/reference-interpreter/target/release/bennett-isa-ref',
                        'run-program', str(obj), 'main', '--budget', '10000000,1048576,65536,256',
                        '--replies', str(tmp/'reversible/23/r-console/argv.json')],
            'result': read('r-hello23-execution.json'),
            'execution_log_sha256': digest(tmp/'r-hello23-execution.json')}
    failed_logs = sorted(tmp.glob('bp-ivy-gate-*-red.log'))
    latest['prior_failed_attempts'] = [{'log': str(p.relative_to(a.root)), 'sha256': digest(p)} for p in failed_logs]
    path.write_text(json.dumps({'schema': 2, 'latest_pass': latest}, indent=2) + '\n')
    print(f"recorded pass {a.name}: {len(rows)} object pairs, {latest['object_pairs']['published_matches']} published matches, "
          "latest pass only")


if __name__ == '__main__':
    main()
````

## `scripts/test` (91 lines)

````
#!/usr/bin/env python3
"""Default, bounded checks; scripts/gate also runs the slow integration drivers."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
POLICIES = ("smoke", "gate_policy", "contract_policy", "pin_policy", "quality_ratchet")
DRIVERS = (
    "recognition",
    "analysis_edges",
    "validation",
    "scalars",
    "address_spaces",
    "register_classes",
    "entry_runtime",
    "normalisation_scope",
)
REGRESSIONS = (
    "shuffle",
    "byval",
    "global-diagnostic",
    "byte-order",
    "native-abi",
    "block-order",
    "control",
    "dynamic-gate",
    "unresolved-call",
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--major", action="append", type=int, choices=(18, 23))
    args = parser.parse_args()
    environment = dict(os.environ)
    for key in ("DISPLAY", "WAYLAND_DISPLAY", "DBUS_SESSION_BUS_ADDRESS", "BROWSER"):
        environment.pop(key, None)
    temporary = ROOT / ".tmp/tests"
    temporary.mkdir(parents=True, exist_ok=True)
    environment.setdefault("TMPDIR", str(temporary))
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    commands = [[sys.executable, "-B", f"tests/{name}.py"] for name in POLICIES]
    for major in args.major or (18, 23):
        commands.extend(
            [sys.executable, "-B", f"tests/{name}.py", "--major", str(major)]
            for name in DRIVERS
        )
        commands.append(
            [
                sys.executable,
                "-B",
                "tests/review_regressions.py",
                "--major",
                str(major),
                *(argument for name in REGRESSIONS for argument in ("--case", name)),
            ]
        )
    started = time.monotonic()
    for command in commands:
        remaining = 180 - (time.monotonic() - started)
        if remaining <= 0:
            raise SystemExit("default tests exceeded the 180-second allowance")
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            timeout=min(120, remaining),
        )
        label = " ".join(command[2:])
        print(f"{label}: exit {result.returncode}", flush=True)
        if result.returncode:
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
            return result.returncode
    elapsed = time.monotonic() - started
    receipt = {"commands": len(commands), "elapsed_s": round(elapsed, 3)}
    (temporary / "default.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
````

## `src/BennettPlugin.cpp` (471 lines)

````
#include "Bennett.h"
#include "NativeComparison.h"
#include "ComparisonLayout.h"
#include "llvm/Config/llvm-config.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/InstIterator.h"
#include "llvm/Passes/PassBuilder.h"
#if LLVM_VERSION_MAJOR >= 23
#include "llvm/Plugins/PassPlugin.h"
#else
#include "llvm/Passes/PassPlugin.h"
#endif
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Transforms/Utils/Local.h"
#include "llvm/Bitcode/BitcodeWriter.h"
#include "llvm/Transforms/Utils/Cloning.h"
#include <cstdlib>
using namespace llvm;
namespace {
cl::opt<std::string> Dialect("bennett-dialect",
                             cl::desc("Required exact dialect version"));
cl::opt<std::string> ISA("bennett-isa", cl::init("0.8"));
cl::opt<std::string> Output("bennett-out");
cl::opt<std::string> Tier("bennett-tier");
cl::opt<std::string> ProgramEntry("bennett-entry");
cl::opt<std::string> Disk("bennett-disk");
cl::opt<std::string> BudgetTableFile("bennett-budgets",cl::init(""));
cl::opt<std::string> BudgetDefault("bennett-budget-default",cl::init("1048576,1048576,65536,256,65536"));
cl::opt<std::string> Report("bennett-report");
cl::opt<bool> DescriptorReference("bennett-descriptor-reference", cl::desc("Non-production reference objects from statically resolved marker descriptors"));
cl::opt<bool> ValidateOnly("bennett-validate-only", cl::desc("Validate materialised L/R IR independently of normalisation"));
cl::opt<bool> ValidateClassical("bennett-validate-classical", cl::desc("Use CC V12 host-call rules in independent validation"));
cl::opt<bool> Comparison("bennett-comparison", cl::desc("§13.1 native comparison: normalise and require linked soft-float closure"));
cl::opt<bool> NormaliseOnly("bennett-normalise-only", cl::desc("Test-only M1 scalar N-rule materialisation; no conformance verdict"));
cl::opt<bool> AnalysisOnly(
    "bennett-analysis-only",
    cl::desc("Non-production S1-S5 report; emits no device object"));
cl::opt<bool> LegalityAudit(
    "bennett-legality-audit",
    cl::desc("Test-only §21.1 legacy spike ABI; requires analysis-only"));
cl::opt<bool> Prelink("bennett-pre-link",
                      cl::desc("Explicit pre-link phase: do nothing"));
cl::opt<bool> Closed("bennett-closed-unit");
cl::opt<std::string> Oracle("bennett-oracle");
cl::opt<std::string>
    Shape("bennett-scalar-shape",
          cl::desc("Scalar test shape, e.g. IN(8,zext),IN(8,zext);tgt=9"));
cl::opt<uint64_t> HeapBytes("bennett-scalar-heap", cl::init(0));
cl::opt<unsigned> StackCells("bennett-scalar-stack", cl::init(32));
} // namespace
namespace bennett {
[[noreturn]] void fail(StringRef code, StringRef section, const Value *v) {
  errs() << "bennett: " << code << ": " << section;
  if (v) {
    errs() << " at ";
    v->print(errs());
  }
  errs() << "\n";
  std::exit(1);
}
[[noreturn]] void unimplemented(StringRef sec, unsigned n, const Value *v) {
  fail("unimplemented", (sec + " (milestone " + Twine(n) + ")").str(), v);
}
bool auditLegality() { return LegalityAudit; }
const std::map<std::string, std::string> &markers() {
  // Compact types: v=void, p=ptr AS0, b=i1, w=i32, n=i64, d=double.
  static std::map<std::string, std::string> names = {
      {"__bennett_qalloc", "pnn"},
      {"__bennett_qborrow", "pnn"},
      {"__bennett_qfree", "vp"},
      {"__bennett_gate", "vwpn"},
      {"__bennett_gate2", "vwpnpn"},
      {"__bennett_gate3", "vwpnpnpn"},
      {"__bennett_rot", "vwpnd"},
      {"__bennett_measure", "bpn"},
      {"__bennett_qload", "vppp"},
      {"__bennett_qstore", "vppp"},
      {"__bennett_qprep", "vppn"},
      {"__bennett_observe", "vpn"},
      {"__bennett_ctrl", "vpnppp"},
      {"__bennett_adj", "vppp"},
      {"__bennett_compute", "vpppp"},
      {"__bennett_reversible", "vppp"},
      {"__bennett_oracle", "vppp"},
      {"__bennett_inplace", "vpppp"},
      {"__bennett_effect_console_write", "vpn"},
      {"__bennett_effect_clock_read", "vp"},
      {"__bennett_effect_entropy_read", "vpn"},
      {"__bennett_effect_block_read", "vnp"},
      {"__bennett_effect_block_write", "vnp"}};
  if (LegalityAudit)
    names["__bennett_ctrl_v"] = "vnpnn";
  return names;
}
std::vector<unsigned> regionOperands(StringRef n) {
  if (n == "__bennett_ctrl" || n == "__bennett_ctrl_v")
    return {2};
  if (n == "__bennett_compute" || n == "__bennett_inplace")
    return {0, 1};
  if (n == "__bennett_adj" || n == "__bennett_reversible" ||
      n == "__bennett_oracle")
    return {0};
  return {};
}
std::vector<unsigned> handleOperands(StringRef n) {
  if (n == "__bennett_qfree" || n == "__bennett_measure" ||
      n == "__bennett_qprep" || n == "__bennett_ctrl" ||
      n == "__bennett_ctrl_v")
    return {0};
  if (n == "__bennett_gate" || n == "__bennett_rot")
    return {1};
  if (n == "__bennett_gate2")
    return {1, 3};
  if (n == "__bennett_gate3")
    return {1, 3, 5};
  if (n == "__bennett_qload" || n == "__bennett_qstore")
    return {0, 1, 2};
  return {};
}
static Type *type(LLVMContext &c, char t) {
  switch (t) {
  case 'v':
    return Type::getVoidTy(c);
  case 'p':
    return PointerType::get(c, 0);
  case 'b':
    return Type::getInt1Ty(c);
  case 'w':
    return Type::getInt32Ty(c);
  case 'n':
    return Type::getInt64Ty(c);
  case 'd':
    return Type::getDoubleTy(c);
  }
  llvm_unreachable("invalid marker table");
}
static FunctionType *signature(LLVMContext &c, const std::string &s,
                               bool var = false) {
  SmallVector<Type *> args;
  for (unsigned i = 1; i < s.size(); ++i)
    args.push_back(type(c, s[i]));
  return FunctionType::get(type(c, s[0]), args, var);
}
static void attributes(AttributeList attrs, const Value *v) {
  for (unsigned idx : attrs.indexes())
    for (Attribute a : attrs.getAttributes(idx)) {
      if (a.isStringAttribute())
        continue;
      StringRef n = Attribute::getNameFromAttrKind(a.getKindAsEnum());
      bool fn = idx == AttributeList::FunctionIndex;
      static const std::set<std::string> functionAttrs = {
          "nounwind",  "nonlazybind", "uwtable",  "strictfp",   "cold",
          "hot",       "nomerge",     "noinline", "convergent", "builtin",
          "nobuiltin", "optsize",     "minsize",  "optnone"};
      static const std::set<std::string> valueAttrs = {
          "noundef", "nonnull", "range", "zeroext", "signext"};
      bool good = (fn ? functionAttrs : valueAttrs).count(n.str());
      if (!good)
        fail("BD-E-MARKER-ATTRIBUTE", "§3.6 " + n.str(), v);
    }
}
static bool runtimeName(StringRef n) {
  return n.starts_with("__bennett_nz_") || n.starts_with("__bennett_sf_") ||
         n.starts_with("__bennett_rt_") || n.starts_with("__bennett_dev_");
}
static void recognise(Module &m) {
  // §4.1 S1: reserved-name rules precede recognition, in module order.
  for (Function &f : m)
    if (markers().count(f.getName().str()) || runtimeName(f.getName()))
      if (!f.isDeclaration() && (Closed || !runtimeName(f.getName())))
        fail("BD-E-MARKER-DEFINED", "§3.1", &f);
  for (GlobalValue &v : m.global_values())
    if (v.getName().starts_with("__bennett_") &&
        !markers().count(v.getName().str()) &&
        (!runtimeName(v.getName()) || Closed))
      fail("BD-E-MARKER-UNKNOWN", "§3.1", &v);
  for (Function &f : m)
    if (markers().count(f.getName().str()))
      for (User *u : f.users()) {
        auto *cb = dyn_cast<CallBase>(u);
        if (!cb || cb->getCalledOperand() != &f)
          fail("BD-E-MARKER-ADDRESS", "§3.1", u);
        // Callee use is permitted, but the same instruction may also pass its
        // address.
        for (Value *a : cb->args())
          if (a == &f)
            fail("BD-E-MARKER-ADDRESS", "§3.1", cb);
      }
  for (Function &f : m)
    if (auto it = markers().find(f.getName().str()); it != markers().end()) {
      auto *expected = signature(m.getContext(), it->second);
      bool variadicProbe = LegalityAudit && f.getName() == "__bennett_ctrl_v";
      if (LegalityAudit) {
        static const std::map<std::string, std::string> legacy = {
            {"__bennett_ctrl", "vnpnn"},   {"__bennett_adj", "vpp"},
            {"__bennett_compute", "vppp"}, {"__bennett_reversible", "vpnp"},
            {"__bennett_inplace", "vppp"}, {"__bennett_ctrl_v", "vnpnn"}};
        auto it = legacy.find(f.getName().str());
        if (it != legacy.end()) {
          // The spike control begins with ptr, i64, ptr, i64.
          auto sig = it->second;
          if (f.getName() == "__bennett_ctrl")
            sig = "vpnpnp";
          if (variadicProbe)
            sig = "vpnpn";
          auto *old = signature(m.getContext(), sig, variadicProbe);
          if (f.getFunctionType() == old)
            expected = old;
        }
      }
      bool kr = f.isVarArg() && f.arg_empty() &&
                f.getReturnType() == expected->getReturnType();
      for (User *u : f.users())
        if (auto *cb = dyn_cast<CallBase>(u)) {
          if ((f.getFunctionType() != expected && !kr) ||
              (cb->getFunctionType() != expected &&
               !(kr && cb->getFunctionType() ==
                           signature(m.getContext(), it->second, true))) ||
              (!variadicProbe && cb->arg_size() != expected->getNumParams()) ||
              (variadicProbe && cb->arg_size() < expected->getNumParams()) ||
              cb->getCallingConv() != CallingConv::C ||
              f.getCallingConv() != CallingConv::C || cb->hasOperandBundles())
            fail("BD-E-MARKER-SIGNATURE", "§3.5", cb);
          for (unsigned i = 0; i < expected->getNumParams(); ++i)
            if (cb->getArgOperand(i)->getType() != expected->getParamType(i))
              fail("BD-E-MARKER-SIGNATURE", "§3.5 argument type", cb);
        }
    }
  for (Function &f : m)
    if (markers().count(f.getName().str())) {
      if (f.hasExternalWeakLinkage())
        fail("BD-E-MARKER-ATTRIBUTE", "§3.6 extern_weak", &f);
      attributes(f.getAttributes(), &f);
      for (User *u : f.users())
        if (auto *cb = dyn_cast<CallBase>(u)) {
          attributes(cb->getAttributes(), cb);
          if (auto *ci = dyn_cast<CallInst>(cb); ci && ci->isMustTailCall())
            fail("BD-E-MARKER-ATTRIBUTE", "§3.6 musttail", ci);
        }
    }
  for (GlobalVariable &g : m.globals()) {
    auto n = g.getName();
    if ((n.starts_with("jlplt___bennett_") && n.ends_with("_got")) ||
        (g.getAttributes().hasAttribute("julia.fname") &&
         g.getAttributes()
             .getAttribute("julia.fname")
             .getValueAsString()
             .starts_with("__bennett_")))
      fail("BD-E-JULIA-CCALL", "§3.8", &g);
  }
  SmallVector<InvokeInst *> invokes;
  for (Function &f : m)
    for (Instruction &i : instructions(f))
      if (auto *iv = dyn_cast<InvokeInst>(&i))
        if (auto *callee = iv->getCalledFunction();
            callee && markers().count(callee->getName().str()))
          invokes.push_back(iv);
  for (InvokeInst *iv : invokes)
    changeToCall(iv);
  for (Function &f : m)
    if (!f.isDeclaration())
      removeUnreachableBlocks(f);
  // Effect lies use the full S2 call graph later, including region edges.
}
static void checkVersion(Module &m) {
  if (Dialect != "0.2.13" || ISA != "0.8")
    fail("BD-E-VERSION", "§19.9 expected dialect 0.2.13 / ISA 0.8");
  if (auto *md = m.getModuleFlag("bennett.dialect")) {
    auto *s = dyn_cast<MDString>(md);
    if (!s || s->getString() != "0.2.13")
      fail("BD-E-VERSION", "§19.9 module flag");
  }
}
static void checkOperands(Module &m) {
  unsigned classes = 0;
  if (auto *md = dyn_cast_or_null<MDNode>(m.getModuleFlag("bennett.classes")))
    classes = md->getNumOperands();
  for (Function &f : m)
    for (Instruction &i : instructions(f))
      if (auto *c = dyn_cast<CallBase>(&i))
        if (auto *g = c->getCalledFunction()) {
          auto n = g->getName();
          unsigned max = 0;
          if (n == "__bennett_gate")
            max = 8;
          else if (n == "__bennett_gate2" || n == "__bennett_rot")
            max = 3;
          else if (n == "__bennett_gate3")
            max = 1;
          if (max)
            if (auto *op = dyn_cast<ConstantInt>(c->getArgOperand(0));
                op && (op->isZero() || op->getValue().ugt(max)))
              fail("BD-E-OPERAND", "§3.4 operation code", c);
          if (n == "__bennett_qalloc" || n == "__bennett_qborrow") {
            if (auto *cls = dyn_cast<ConstantInt>(c->getArgOperand(0));
                cls && cls->getValue().ugt(classes))
              fail("BD-E-OPERAND", "§3.4 class", c);
            if (auto *width = dyn_cast<ConstantInt>(c->getArgOperand(1));
                width && width->isZero())
              fail("BD-E-OPERAND", "§3.4 width zero", c);
          }
        }
}
struct BennettPass : PassInfoMixin<BennettPass> {
  PreservedAnalyses run(Module &m, ModuleAnalysisManager &) {
    if (Prelink)
      return PreservedAnalyses::all();
    if (LegalityAudit && !AnalysisOnly)
      fail("test mode",
           "legality-audit requires analysis-only; never production");
    recognise(m);
    checkVersion(m);
    initialiseComparisonLayout(m);
    if (ValidateOnly) {
      validateResidual(m,ValidateClassical);
      return PreservedAnalyses::all();
    }
    if (NormaliseOnly || Comparison) {
      if(Comparison || std::getenv("BENNETT_ARITH_BITCODE"))linkArith(m,nullptr,false,true);
      if(!Comparison)normaliseWideABI(m);
      for (Function &f : m) if (!f.isDeclaration() && !f.hasFnAttribute("bennett.native.comparison.runtime")) normaliseScalar(f,!Comparison);
      for(auto &f:m)if(!f.use_empty())materialiseIntegerRuntime(f);
      if(Comparison)prepareNativeComparison(m);
      if(Comparison) for(auto &f:m)for(auto &i:instructions(f))if(auto *c=dyn_cast<CallBase>(&i))if(auto *g=c->getCalledFunction())requireSoftFloat(*g);
      errs() << "bennett: scalar normalisation test mode; full N0-N35/V1-V16 pending M2\n";
      return PreservedAnalyses::none();
    }
    if(!AnalysisOnly || std::getenv("BENNETT_ARITH_BITCODE"))
      linkArith(m,Tier.empty()?m.getFunction(Oracle):m.getFunction(ProgramEntry),!Tier.empty());
    if(!Tier.empty() && Tier!="reversible")fail("input","§19.2 expected tier reversible");
    if(Tier.empty() && (!ProgramEntry.empty() || !Disk.empty()))fail("input","§19.2 entry/disk require reversible tier");
    auto *rEntry=Tier.empty()?nullptr:m.getFunction(ProgramEntry);
    if(!Tier.empty() && (!rEntry || rEntry->isDeclaration()))fail("input","§19.2 whole-program entry missing");
    Analysis a(m,rEntry,!Tier.empty());
    a.run();
    a.checkHandles();
    a.checkRegions();
    if (!Report.empty()) {
      std::error_code ec;
      raw_fd_ostream o(Report, ec);
      if (ec)
        fail("output", ec.message());
      o << formatv("{0:2}\n", json::Value(a.report()));
    }
    if (AnalysisOnly) {
      errs()
          << "bennett: analysis-only: S1-S5 complete; no production artefact\n";
      return PreservedAnalyses::none();
    }
    checkOperands(m);
    if (Output.empty())
      fail("output", "§19.9 -bennett-out is required");
    if (!Oracle.empty()) {
      auto *f = m.getFunction(Oracle);
      if (!f || f->isDeclaration())
        fail("input", "oracle function missing");
      ValueToValueMapTy map;
      auto materialised = CloneModule(m, map);
      auto *mf = cast<Function>(map[f]);
      mf=normaliseWideABI(*materialised,mf);
      normaliseScalar(*mf);
      lowerScalar(*materialised, *mf, Shape, Output, StackCells, HeapBytes);
      std::error_code ec;
      raw_fd_ostream bc(Output + "/materialised.bc", ec);
      if (ec) fail("output", ec.message());
      WriteBitcodeToFile(*materialised, bc);
      return PreservedAnalyses::none();
    }
    if (DescriptorReference) {
      unsigned objects=0;
      for(Function &caller:m)for(Instruction &i:instructions(caller))
        if(auto *c=dyn_cast<CallBase>(&i))
          if(auto *marker=c->getCalledFunction();marker && marker->getName()=="__bennett_oracle") {
            Value *desc=c->getArgOperand(2);
            auto integer=[&](AV v)->uint64_t {
              if(v.top || v.atoms.size()!=1 || v.atoms.begin()->kind!=Atom::Int)
                unimplemented("§8.4 non-singleton descriptor shape",2,c);
              return v.atoms.begin()->integer.getLimitedValue();
            };
            auto u32=Type::getInt32Ty(m.getContext());auto ptr=PointerType::get(m.getContext(),0);
            auto *h=StructType::get(m.getContext(),{u32,u32,u32,u32,ptr,ptr});
            auto *b=StructType::get(m.getContext(),{u32,u32,ptr,Type::getInt64Ty(m.getContext()),Type::getInt64Ty(m.getContext())});
            auto *hl=m.getDataLayout().getStructLayout(h),*bl=m.getDataLayout().getStructLayout(b);
            auto field=[&](uint64_t off,Type *t) {return a.readAt(*c,desc,off,t);};
            if(integer(field(0,u32))!=2 || integer(field(12,u32))!=0 || integer(field(8,u32))!=0)
              unimplemented("§8.1/§8.3 descriptor header/device dispatch",2,c);
            unsigned params=integer(field(4,u32));
            auto qwidth=[&](AV q)->unsigned {
              if(q.top || q.atoms.size()!=1 || q.atoms.begin()->kind!=Atom::Root)
                unimplemented("§6.5 descriptor register dispatch",3,c);
              auto *alloc=dyn_cast<CallBase>(q.atoms.begin()->object);
              if(!alloc)unimplemented("§6.6 boundary descriptor register",3,c);
              return integer(a.get(alloc->getArgOperand(1)));
            };
            auto target=field(hl->getElementOffset(4),ptr), fault=field(hl->getElementOffset(5),ptr);
            if(qwidth(fault)!=4)unimplemented("§8.2 T-SIZE fault dispatch",3,c);
            bool discard=!target.top && target.atoms.size()==1 && target.atoms.begin()->kind==Atom::Int && target.atoms.begin()->integer.isZero();
            unsigned tgt=discard?0:qwidth(target);
            auto candidates=a.candidates(c->getArgOperand(0));
            for(Function *f:candidates) {
              if(params!=f->arg_size())unimplemented("§8.2 flattened descriptor arity",2,c);
              std::string shape;unsigned j=0;
              for(Argument &param:f->args()) {
                uint64_t off=hl->getSizeInBytes()+j*bl->getSizeInBytes();
                unsigned kind=integer(field(off,u32)),mode=integer(field(off+bl->getElementOffset(1),u32));
                if(j++)shape+=",";
                if(kind==1 && mode<=1)shape+="IN("+std::to_string(qwidth(field(off+bl->getElementOffset(2),ptr)))+","+(mode?"sext":"zext")+")";
                else if(kind==2) {
                  unsigned w=param.getType()->isPointerTy()?m.getDataLayout().getPointerTypeSizeInBits(param.getType()):param.getType()->getPrimitiveSizeInBits().getFixedValue();
                  shape+="ARG("+std::to_string(w)+")";
                } else unimplemented("§8.4 MEM_IN/OUT/INOUT descriptor dispatch",2,c);
              }
              shape+=";tgt="+(discard?std::string("null"):std::to_string(tgt));
              ValueToValueMapTy map;auto clone=CloneModule(m,map);auto *mf=cast<Function>(map[f]);mf=normaliseWideABI(*clone,mf);normaliseScalar(*mf);
              lowerScalar(*clone,*mf,shape,Output+"/oracle-"+std::to_string(objects++),StackCells);
            }
          }
      if(!objects)fail("input","descriptor-reference found no oracle shape");
      errs()<<"bennett: descriptor reference objects only; CC launches remain unimplemented: §17.4 (milestone 3)\n";
      return PreservedAnalyses::none();
    }
    if(rEntry) {
      lowerReversible(m,a,*rEntry,Output,StackCells,BudgetDefault,BudgetTableFile,Disk);
      errs()<<"bennett: blocked:BD-B-ISA7 §11.5/§17.6 R entry; objects emitted; typed pre-instruction fault requires ISA-7\n";
      std::exit(3);
    }
    for (Function &f : m)
      if (a.tiers[&f].count("R"))
        fail("unimplemented", "§25.1 BLK-5", &f);
    for (Function &f : m)
      for (Instruction &i : instructions(f))
        if (auto *c = dyn_cast<CallBase>(&i))
          if (auto *g = c->getCalledFunction();
              g && (g->getName() == "__bennett_qalloc" ||
                    g->getName() == "__bennett_qborrow")) {
            auto width = a.get(c->getArgOperand(1));
            if (width.top)
              fail("unimplemented", "§25.1 BLK-1", c);
          }
    lowerProduction(m, a, Output, StackCells, BudgetDefault, BudgetTableFile);
    return PreservedAnalyses::none();
  }
  static bool isRequired() { return true; }
};
} // namespace bennett
extern "C" LLVM_ATTRIBUTE_WEAK PassPluginLibraryInfo llvmGetPassPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "bennett", "dialect-0.2.13;isa-0.8",
          [](PassBuilder &pb) {
            pb.registerPipelineParsingCallback(
                [](StringRef n, ModulePassManager &pm,
                   ArrayRef<PassBuilder::PipelineElement>) {
                  if (n == "bennett-native-comparison") {
                    bennett::addNativeComparisonPass(pm);
                    return true;
                  }
                  if (n == "bennett-native-host-imports") {
                    bennett::addNativeHostImportsPass(pm);
                    return true;
                  }
                  if (n == "bennett-native-comparison-finalise") {
                    bennett::addNativeFinalisePass(pm);
                    return true;
                  }
                  if (n != "bennett")
                    return false;
                  pm.addPass(bennett::BennettPass());
                  return true;
                });
          }};
}
````

## `src/Production.cpp` (2895 lines)

````
#include "Bennett.h"
#include "ByteOrder.h"
#include "ComparisonLayout.h"
#include "llvm/ADT/StringExtras.h"
#include "llvm/ADT/MapVector.h"
#include "llvm/ADT/PostOrderIterator.h"
#include "llvm/Analysis/ValueTracking.h"
#include "llvm/Analysis/InstructionSimplify.h"
#include "llvm/Bitcode/BitcodeWriter.h"
#include "llvm/Config/llvm-config.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/InlineAsm.h"
#include "llvm/IR/CFG.h"
#include "llvm/IR/InstIterator.h"
#include "llvm/IR/Intrinsics.h"
#include "llvm/IR/IntrinsicInst.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/Support/SHA256.h"
#include "llvm/Support/Program.h"
#include <cstdlib>
#include "llvm/Transforms/Utils/Cloning.h"
#include <regex>
using namespace llvm;
namespace bennett {
namespace {
std::string hash(StringRef s) {
  return toHex(SHA256::hash(arrayRefFromStringRef(s)), true);
}
std::string jcs(const json::Value &v) {
  if (auto *o = v.getAsObject()) {
    std::map<std::string, const json::Value *> sorted;
    for (auto &e : *o)
      sorted[e.first.str()] = &e.second;
    std::string s = "{";
    for (auto &e : sorted) {
      if (s.size() > 1)
        s += ",";
      s += jcs(json::Value(e.first)) + ":" + jcs(*e.second);
    }
    return s + "}";
  }
  if (auto *a = v.getAsArray()) {
    std::string s = "[";
    for (auto &e : *a) {
      if (s.size() > 1)
        s += ",";
      s += jcs(e);
    }
    return s + "]";
  }
  return formatv("{0}", v).str();
}
json::Value parse(StringRef text) {
  auto v = json::parse(text);
  if (!v)
    fail("output", toString(v.takeError()));
  return std::move(*v);
}
std::string read(StringRef path) {
  auto b = MemoryBuffer::getFile(path);
  if (!b)
    fail("output", b.getError().message());
  return (*b)->getBuffer().str();
}
void write(StringRef path, StringRef text) {
  std::error_code ec;
  raw_fd_ostream o(path, ec);
  if (ec)
    fail("output", ec.message());
  o << text;
}
std::string join(const std::vector<std::string> &v, StringRef sep = ", ") {
  std::string s;
  for (auto &x : v) {
    if (!s.empty())
      s += sep;
    s += x;
  }
  return s;
}
std::string decimal(const APInt &v) {
  SmallString<48> s;
  v.toString(s, 10, false);
  return s.str().str();
}
uint64_t integer(AV v, const Value *at) {
  if (v.top || v.atoms.size() != 1 || v.atoms.begin()->kind != Atom::Int)
    unimplemented("§8.4 scalar descriptor finite dispatch", 1, at);
  return v.atoms.begin()->integer.getLimitedValue();
}
const char *budgetNames[] = {"steps", "heap", "stack", "depth", "sstack"};
json::Object tuple(const std::vector<uint64_t> &v) {
  json::Object o;
  for (unsigned i = 0; i < 5; ++i) o[budgetNames[i]] = std::to_string(v[i]);
  return o;
}
struct BudgetTable {
  std::vector<uint64_t> defaults, capacities;
  json::Value document = json::Object{};
  bool enabled;
  uint64_t number(const json::Value &v) {
    auto s = v.getAsString(); uint64_t n;
    if (!s || s->empty() || (s->size() > 1 && (*s)[0] == '0') || s->getAsInteger(10,n))
      fail("input", "§9.2 budget components require unsigned decimal strings");
    return n;
  }
  BudgetTable(std::vector<uint64_t> d, StringRef path) : defaults(d), capacities(d), enabled(!path.empty()) {
    if (!enabled) return;
    auto bytes = read(path); document = parse(bytes);
    auto *o = document.getAsObject();
    if (!o || o->getString("version") != "0.2" || !o->getArray("entries") ||
        jcs(document) != StringRef(bytes).rtrim())
      fail("input", "§9.2 budget table must be version 0.2 JCS");
    for (auto &v : *o) if (v.first != "version" && v.first != "defaults" && v.first != "entries")
      fail("input", "§9.2 unknown budget-table field");
    if (auto *defs = o->getObject("defaults")) {
      for (auto &v : *defs) {
        unsigned i = 0; for (; i < 5; ++i) if (v.first == budgetNames[i]) break;
        if (i == 5) fail("input", "§9.2 unknown default component");
        defaults[i] = number(v.second);
      }
    } else if (o->get("defaults")) fail("input", "§9.2 defaults must be an object");
    capacities = defaults;
    for (auto &v : *o->getArray("entries")) {
      auto *entry = v.getAsObject(); unsigned selectors = 0;
      if (!entry) fail("input", "§9.2 entry must be an object");
      for (auto &field : *entry) {
        if (field.first == "symbol" || field.first == "region_key" || field.first == "identity") {
          ++selectors; auto str = field.second.getAsString();
          if (!str || (field.first != "symbol" && !std::regex_match(str->str(), std::regex("[0-9a-f]{64}"))))
            fail("input", "§9.2 invalid selector");
        } else {
          unsigned i = 0; for (; i < 5; ++i) if (field.first == budgetNames[i]) break;
          if (i == 5) fail("input", "§9.2 unknown entry component");
          capacities[i] = std::max(capacities[i], number(field.second));
        }
      }
      if (selectors != 1) fail("input", "§9.2 entry requires exactly one selector");
    }
  }
  bool glob(StringRef pattern, StringRef name) {
    std::string re = "^";
    for (char c : pattern) {
      if (c == '*') re += ".*";
      else if (c == '?') re += ".";
      else { if (StringRef(".[]{}()^$|+\\").contains(c)) re += '\\'; re += c; }
    }
    return std::regex_match(name.str(), std::regex(re + "$"));
  }
  std::vector<uint64_t> baseline(Function &f) {
    auto result = defaults;
    if (!enabled) return result;
    auto key = regionKey(&f);
    for (unsigned i = 0; i < 5; ++i) {
      bool found = false;
      for (auto selector : {"region_key", "symbol"}) {
        for (auto &v : *document.getAsObject()->getArray("entries")) {
          auto *e = v.getAsObject(); auto sel = e->getString(selector);
          if (!sel || !e->get(budgetNames[i])) continue;
          if ((StringRef(selector) == "region_key" && *sel == key) ||
              (StringRef(selector) == "symbol" && glob(*sel, f.getName()))) {
            result[i] = number(*e->get(budgetNames[i])); found = true; break;
          }
        }
        if (found) break;
      }
    }
    return result;
  }
  void overlay(std::vector<uint64_t> &budget, StringRef selection) {
    if (!enabled) return;
    for (unsigned i = 0; i < 5; ++i)
      for (auto &v : *document.getAsObject()->getArray("entries")) {
        auto *e = v.getAsObject();
        if (e->getString("identity") == selection && e->get(budgetNames[i])) {
          budget[i] = number(*e->get(budgetNames[i])); break;
        }
      }
  }
};
std::string oracleIdentity(StringRef object) {
  auto text = object.split("section symbols\n").second.split('\n').first;
  auto syms = parse(text);
  for (auto &v : *syms.getAsObject())
    if (v.second.getAsObject()->getString("name") == "ref")
      return v.second.getAsObject()->getString("interface_hash")->str();
  fail("output", "missing reference identity");
}
struct Entry {
  Module &m;
  Analysis &a;
  Function &f;
  std::string out;
  unsigned stack;
  BudgetTable &table;
  json::Array resolvedShapes;
  std::map<const Value *, std::string> names;
  std::map<const BasicBlock *, std::string> blocks;
  std::set<const Value *> descriptorObjects;
  bool memoryDescriptors = false;
  bool rTier = false;
  bool argvService = false;
  std::set<std::string> effectModels;
  std::string diskImage, diskDataKey;
  json::Array asmPoints;
  GlobalVariable *rSteps = nullptr, *rEH = nullptr;
  void rReturn() {
    for(auto &p:localMemory)rows.push_back("free "+p);
    std::vector<std::string> values;
    for(auto &t:resultTypes) {
      auto z=number(0);if(t=="ptr")z=emit("ptr","inttoptr "+z);
      else if(t!="i64")z=emit(t,"trunc."+t+" "+z);
      values.push_back(z);
    }
    rows.push_back("ret"+(values.empty()?"":" "+join(values," ")));
  }
  void propagateExit() {
    if(!rTier || !rEH)return;
    auto p=operand(rEH),active=emit("i32","load.i32 "+p);
    auto four=operand(ConstantInt::get(Type::getInt32Ty(m.getContext()),4));
    auto exiting=emit("i1","icmp.eq "+active+" "+four);
    auto id=std::to_string(dispatchBlock++);
    rows.push_back("br "+exiting+" ^exit"+id+"() ^continue"+id+"()");
    rows.push_back("^exit"+id+"():");rReturn();rows.push_back("^continue"+id+"():");
  }
  void countRStep() {
    auto p=operand(rSteps),left=emit("i64","load.i64 "+p),zero=number(0);
    auto exhausted=emit("i1","icmp.eq "+left+" "+zero);
    auto id=std::to_string(dispatchBlock++);
    rows.push_back("br "+exhausted+" ^budget"+id+"() ^step"+id+"()");
    rows.push_back("^budget"+id+"():");rows.push_back("trap");
    rows.push_back("^step"+id+"():");auto one=number(1),remaining=emit("i64","sub "+left+" "+one);
    rows.push_back("store.i64 "+p+" "+remaining);
  }
  std::set<std::string> ccGlobals;
  uint64_t ccHeapBytes = 0, allocatedBytes = 0;
  const Value *activeRoot = nullptr;
  bool generalUsed = false;
  bool allocatorFaultService = false;
  bool usesCCCalls = false;
  bool usesSourceMemory = false;
  std::map<Function *, std::string> *ccNames = nullptr;
  std::map<std::string, std::pair<std::string,std::string>> ccFunctions;
  std::vector<std::string> regs, rows, params, results, paramTypes, resultTypes;
  std::vector<json::Object> budgets;
  std::string reference, shape, refPath;
  std::vector<std::string> references;
  std::vector<std::map<std::string,std::string>> referenceGlobals;
  json::Array coverage;
  json::Array controlledIdentities;
  std::map<std::pair<std::string,std::string>,std::string> trappedCalls;
  std::map<std::string, std::pair<std::string, std::string>> actions;
  unsigned next = 0, ordinal = 0;
  struct PhysicalSlot { std::string q, tag; unsigned identity; };
  std::vector<const Value *> fileOrder;
  std::map<const Value *, PhysicalSlot> files;
  std::vector<std::string> localMemory;
  bool tagged(AV v) {
    for (auto &x : v.atoms) if (x.kind == Atom::Root && files.count(x.object)) return true;
    return false;
  }
  void withHandle(Value *v, const std::function<void(std::string)> &body, bool retire = false, std::string result = "", const Value *returned = nullptr) {
    auto provenance = a.get(v);
    if (!tagged(provenance)) { body(operand(v)); return; }
    auto id = std::to_string(dispatchBlock++), done = "handle" + id + "done";
    auto value = operand(v);
    for (auto *site : fileOrder) {
      bool candidate=false;
      for(auto &x:provenance.atoms) if(x.kind==Atom::Root && x.object==site)candidate=true;
      if(!candidate)continue;
      auto &slot = files.at(site);
      auto eq = fresh("i1"), live = fresh("i1"), ok = fresh("i1"), liveTag = fresh("i" + std::to_string(m.getDataLayout().getPointerSizeInBits()));
      rows.push_back(liveTag + " = load.i" + std::to_string(m.getDataLayout().getPointerSizeInBits()) + " " + slot.tag);
      auto zero = operand(ConstantInt::get(m.getDataLayout().getIntPtrType(m.getContext()),0));
      auto leaf = "handle" + std::to_string(dispatchBlock++), next = leaf + "next";
      rows.push_back(eq + " = icmp.eq " + value + " " + liveTag);
      rows.push_back(live + " = icmp.ne " + liveTag + " " + zero);
      rows.push_back(ok + " = and " + eq + " " + live);
      rows.push_back("br " + ok + " ^" + leaf + "() ^" + next + "()");
      rows.push_back("^" + leaf + "():"); activeRoot=site; body(slot.q); activeRoot=nullptr;
      if (retire) rows.push_back("store.i" + std::to_string(m.getDataLayout().getPointerSizeInBits()) + " " + slot.tag + " " + zero);
      rows.push_back("br ^" + done + "(" + (result.empty() ? "" : names.at(returned)) + ")"); rows.push_back("^" + next + "():");
    }
    rows.push_back("trap"); rows.push_back("^" + done + "(" + (result.empty() ? "" : result+":i1") + "):");
  }
  unsigned width(Type *t) {
    if(t->isPointerTy())return m.getDataLayout().getPointerTypeSizeInBits(t);
    if(t->isFloatingPointTy())return t->getPrimitiveSizeInBits();
    if (t->isIntegerTy() && t->getIntegerBitWidth() <= 128)
      return t->getIntegerBitWidth();
    unimplemented("§17.4 CC scalar carrier", 1, &f);
  }
  std::string fresh(std::string type) {
    auto n = "v" + std::to_string(next++);
    regs.push_back(n + ":" + type);
    return n;
  }
  std::string operand(Value *v) {
    if (names.count(v))
      return names[v];
    if(auto *c=dyn_cast<ConstantFP>(v))return operand(ConstantInt::get(c->getContext(),c->getValueAPF().bitcastToAPInt()));
    if (auto *c = dyn_cast<ConstantInt>(v)) {
      auto n = fresh("i" + std::to_string(c->getBitWidth()));
      rows.push_back(n + " = const.i" + std::to_string(c->getBitWidth()) + " " +
                     decimal(c->getValue()));
      return n;
    }
    if (auto *fn = resolve(v); fn && v->getType()->isPointerTy()) {
      auto n=fresh("ptr");auto address=operand(ConstantInt::get(m.getDataLayout().getIntPtrType(m.getContext()),functionAddress(fn)));
      rows.push_back(n+" = inttoptr "+address);return n;
    }
    if (auto *g=dyn_cast<ConstantExpr>(v);g && g->getOpcode()==Instruction::GetElementPtr)return gep(cast<GEPOperator>(g));
    if(auto *g=dyn_cast<GlobalVariable>(v)) {
      ccGlobals.insert(scalarGlobalKey(*g));auto n=fresh("ptr");
      // Resolved by the unified object linker, in the same namespace as L.
      auto pw=m.getDataLayout().getPointerSizeInBits();auto bits=fresh("i"+std::to_string(pw));
      rows.push_back(bits+" = const.i"+std::to_string(pw)+" CCADDRESS"+std::to_string(std::distance(m.global_begin(),g->getIterator())));
      rows.push_back(n+" = inttoptr "+bits);return n;
    }
    if (isa<ConstantPointerNull>(v)) {
      auto n = fresh("ptr"); auto z = operand(ConstantInt::get(m.getDataLayout().getIntPtrType(m.getContext()),0));
      rows.push_back(n + " = inttoptr " + z); return n;
    }
    unimplemented("§17.4 CC operand / §6.5 handle environment", 1, v);
  }
  // §17.4: aggregates travel as depth-first scalar tuples, including
  // recursive call arguments/results and parallel phi bindings.
  struct Field { std::vector<unsigned> path; Type *type; uint64_t offset; };
  std::vector<Field> fields(Type *t) {
    std::vector<Field> out;
    std::function<void(Type *,std::vector<unsigned>,uint64_t)> visit =
      [&](Type *t,std::vector<unsigned> path,uint64_t offset) {
        if(t->isAggregateType()) {
          unsigned n=t->isStructTy()?cast<StructType>(t)->getNumElements():t->getArrayNumElements();
          for(unsigned k=0;k<n;++k) {
            auto p=path;p.push_back(k);
            auto *e=t->isStructTy()?t->getStructElementType(k):t->getArrayElementType();
            auto off=t->isStructTy()?m.getDataLayout().getStructLayout(cast<StructType>(t))->getElementOffset(k):k*m.getDataLayout().getTypeAllocSize(e).getFixedValue();
            visit(e,p,offset+off);
          }
        } else out.push_back({path,t,offset});
      };
    visit(t,{},0);return out;
  }
  std::map<const Value *,std::vector<std::string>> tuples;
  std::string fieldType(Type *t) {
    return t->isPointerTy()?"ptr":"i"+std::to_string(width(t));
  }
  std::vector<std::string> operands(Value *v) {
    if(!v->getType()->isAggregateType())return {operand(v)};
    if(auto it=tuples.find(v);it!=tuples.end())return it->second;
    if(auto *c=dyn_cast<Constant>(v)) {
      std::vector<std::string> out;
      for(auto &field:fields(v->getType())) {
        auto *e=c;for(auto k:field.path)e=e->getAggregateElement(k);
        out.push_back(operand(e));
      }
      return out;
    }
    unimplemented("§17.4 aggregate CC operand",2,v);
  }
  std::vector<std::string> destinations(Value *v) {
    if(!v->getType()->isAggregateType()) {auto n=fresh(type(v));names[v]=n;return {n};}
    std::vector<std::string> out;
    for(auto &field:fields(v->getType()))out.push_back(fresh(fieldType(field.type)));
    tuples[v]=out;return out;
  }
  struct CallArguments {
    std::vector<std::string> values, copies;
  };
  CallArguments callArguments(CallBase &call) {
    CallArguments result;
    for(unsigned k=0;k<call.arg_size();++k) {
      auto *arg=call.getArgOperand(k);
      auto *copyType=call.getParamByValType(k);
      if(!copyType) {
        auto values=operands(arg);
        result.values.insert(result.values.end(),values.begin(),values.end());
        continue;
      }
      // N25: each byval argument gets independent caller-owned storage.
      // Copy bytes, including padding, without changing source endianness.
      auto bytes=m.getDataLayout().getTypeAllocSize(copyType).getFixedValue();
      auto length=number(bytes),copy=emit("ptr","alloc "+length);
      result.values.push_back(copy);result.copies.push_back(copy);
      allocatedBytes+=std::max(uint64_t(1),bytes);recordAllocation(copy,length);
      if(!bytes)continue;
      auto pointerType="i"+std::to_string(m.getDataLayout().getPointerSizeInBits());
      auto source=emit(pointerType,"ptrtoint."+pointerType+" "+operand(arg));
      auto target=emit(pointerType,"ptrtoint."+pointerType+" "+copy);
      auto zero=operand(ConstantInt::get(m.getDataLayout().getIntPtrType(m.getContext()),0));
      auto one=operand(ConstantInt::get(m.getDataLayout().getIntPtrType(m.getContext()),1));
      auto limit=operand(ConstantInt::get(m.getDataLayout().getIntPtrType(m.getContext()),bytes));
      auto index=fresh(pointerType),id=std::to_string(dispatchBlock++);
      auto loop="byval"+id,done=loop+"done";
      rows.push_back("br ^"+loop+"("+zero+")");
      rows.push_back("^"+loop+"("+index+":"+pointerType+"):");
      auto from=emit("ptr","inttoptr "+emit(pointerType,"add "+source+" "+index));
      auto to=emit("ptr","inttoptr "+emit(pointerType,"add "+target+" "+index));
      auto value=emit("i8","load.i8 "+from);rows.push_back("store.i8 "+to+" "+value);
      auto next=emit(pointerType,"add "+index+" "+one);
      auto more=emit("i1","icmp.ult "+next+" "+limit);
      rows.push_back("br "+more+" ^"+loop+"("+next+") ^"+done+"()");
      rows.push_back("^"+done+"():");
    }
    return result;
  }
  void releaseCallArguments(const CallArguments &args) {
    for(auto it=args.copies.rbegin();it!=args.copies.rend();++it) {
      rows.push_back("free "+*it);recordFree(*it);
    }
  }
  std::string sourceByteOrder(std::string value,unsigned bits) {
    return reverseBytes(value,bits,[&](APInt n){return operand(ConstantInt::get(m.getContext(),n));},
      [&](unsigned w,std::string op){return emit("i"+std::to_string(w),op);});
  }
  std::string sourceLoad(std::string pointer,unsigned bits) {
    usesSourceMemory=true;
    auto carrier=(!m.getDataLayout().isLittleEndian() && bits>8)?alignTo(bits,8u):bits;
    auto value=emit("i"+std::to_string(carrier),"load.i"+std::to_string(carrier)+" "+pointer);
    if(!m.getDataLayout().isLittleEndian() && bits>8)value=sourceByteOrder(value,carrier);
    if(bits!=carrier)value=emit("i"+std::to_string(bits),"trunc.i"+std::to_string(bits)+" "+value);
    return value;
  }
  void sourceStore(std::string pointer,std::string value,unsigned bits) {
    usesSourceMemory=true;
    if(!m.getDataLayout().isLittleEndian() && bits>8) {
      auto carrier=alignTo(bits,8u);
      if(bits!=carrier)value=emit("i"+std::to_string(carrier),"zext.i"+std::to_string(carrier)+" "+value);
      bits=carrier;value=sourceByteOrder(value,bits);
    }
    rows.push_back("store.i"+std::to_string(bits)+" "+pointer+" "+value);
  }
  void reportedFault(Value *code) {
    if(!rTier) {
      allocatorFaultService=true;
      auto *payload=m.getGlobalVariable("__bennett_cc_fault_payload",true);
      if(!payload)payload=new GlobalVariable(m,Type::getInt64Ty(m.getContext()),false,
        GlobalValue::InternalLinkage,ConstantInt::get(Type::getInt64Ty(m.getContext()),0),"__bennett_cc_fault_payload");
      auto pointer=operand(payload),value=operand(code);
      rows.push_back("store.i64 "+pointer+" "+value);
      emit("i"+std::to_string(m.getDataLayout().getPointerSizeInBits()),"hostcall bennett.fault "+pointer+" "+number(8));
    }
    rows.push_back("trap");
  }
  void unresolvedCall(StringRef callee) {
    std::string block;
    for(auto it=rows.rbegin();it!=rows.rend();++it)if(StringRef(*it).starts_with("^")) {
      block=StringRef(*it).drop_front().split('(').first.str();break;
    }
    auto symbol=ccNames?ccNames->at(&f):f.getName().str();
    trappedCalls[{symbol,block}]="§4.5 no bitcode or bound host service for "+callee.str();
    reportedFault(ConstantInt::get(Type::getInt64Ty(m.getContext()),8));
  }
  std::string fieldPointer(const std::string &p,uint64_t offset) {
    if(!offset)return p;
    auto t="i"+std::to_string(m.getDataLayout().getPointerSizeInBits());
    auto bits=emit(t,"ptrtoint."+t+" "+p);
    auto off=operand(ConstantInt::get(m.getDataLayout().getIntPtrType(m.getContext()),offset));
    bits=emit(t,"add "+bits+" "+off);return emit("ptr","inttoptr "+bits);
  }
  const Value *root(AV v, const Value *at) {
    if (v.top || v.atoms.size() != 1 || v.atoms.begin()->kind != Atom::Root)
      unimplemented("§6.5 descriptor handle dispatch", 1, at);
    return v.atoms.begin()->object;
  }
  unsigned qwidth(AV v, const Value *at) {
    unsigned width = 0;
    if (v.top || v.atoms.empty()) unimplemented("§6.5 handle width dispatch", 1, at);
    for (auto &atom : v.atoms) {
      if(activeRoot && atom.kind==Atom::Root && atom.object!=activeRoot)continue;
      auto *c = atom.kind == Atom::Root ? dyn_cast<CallBase>(atom.object) : nullptr;
      if (!c && atom.kind == Atom::Int && atom.integer.isZero()) continue;
      if (!c) unimplemented("§6.6 scalar boundary handles", 1, at);
      auto w = integer(a.get(c->getArgOperand(1)), at);
      if (width && width != w) unimplemented("§6.5 mixed-width handle dispatch", 1, at);
      width = w;
    }
    return width;
  }
  std::string type(Value *v) {
    if (tagged(a.get(v))) return "i" + std::to_string(m.getDataLayout().getPointerSizeInBits());
    if (v->getType()->isPointerTy() && !a.get(v).roots()) return "ptr";
    if (v->getType()->isPointerTy() && a.get(v).roots())
      return "qreg[" + std::to_string(qwidth(a.get(v), v)) + "]";
    return "i" + std::to_string(width(v->getType()));
  }
  std::string handle(AV v, const Value *at) {
    if (generalDescriptor) { auto *r=root(v,at); return files.count(r) ? files.at(r).q : names.at(r); }
    auto *r = root(v, at);
    if (!names.count(r))
      unimplemented("§6.5 handle not in live register environment", 1, at);
    if (files.count(r)) {
      std::string q;
      withHandle(const_cast<Value *>(r), [&](std::string n) { q = n; });
      return q;
    }
    return names[r];
  }
  // Call-local reaching definitions are a virtual descriptor load. Never use
  // a flow-insensitive union as the runtime field value.
  Value *fieldValue(CallBase &c, uint64_t off, Type *t) {
    auto base = a.get(c.getArgOperand(2));
    if (base.top || base.atoms.size() != 1) return nullptr;
    auto p = *base.atoms.begin();
    for (auto it = c.getIterator(); it != c.getParent()->begin();) {
      auto &i = *--it;
      if (auto *st = dyn_cast<StoreInst>(&i)) {
        auto dst = a.get(st->getPointerOperand());
        if (dst.top) break;
        for (auto &d : dst.atoms) if (d.object == p.object) {
          auto bytes = m.getDataLayout().getTypeStoreSize(st->getValueOperand()->getType()).getFixedValue();
          if (d.stride || (d.offset < int64_t(p.offset + off + m.getDataLayout().getTypeStoreSize(t).getFixedValue()) &&
                          d.offset + int64_t(bytes) > int64_t(p.offset + off))) {
            if (!d.stride && dst.atoms.size() == 1 && d.offset == int64_t(p.offset + off) && st->getValueOperand()->getType() == t)
              return st->getValueOperand();
            return nullptr;
          }
        }
      } else if (auto *call = dyn_cast<CallBase>(&i)) {
        auto *g = call->getCalledFunction();
        if (!g || (!g->getName().starts_with("__bennett_") && !g->getName().starts_with("llvm.lifetime."))) break;
      }
    }
    return nullptr;
  }
  AV descriptorField(CallBase &c,uint64_t off,Type *t) {
    if(automaticSnapshot && !memoryDescriptors)if(auto *v=fieldValue(c,off,t))return a.get(v);
    return a.readAt(c,c.getArgOperand(2),off,t);
  }
  // The fast path above is an optimisation only. All other reads use the
  // actual caller memory at the marker, including predecessor stores/phis.
  std::string fieldOperand(CallBase &c, uint64_t off, Type *t) {
    if (!memoryDescriptors)
      if (auto *v = fieldValue(c, off, t)) return operand(v);
    auto p = operand(c.getArgOperand(2));
    auto pw = m.getDataLayout().getPointerSizeInBits();
    auto bits = fresh("i"+std::to_string(pw));
    rows.push_back(bits+" = ptrtoint.i"+std::to_string(pw)+" "+p);
    auto k = operand(ConstantInt::get(IntegerType::get(m.getContext(),pw),off));
    auto sum = fresh("i"+std::to_string(pw)), address = fresh("ptr");
    rows.push_back(sum+" = add "+bits+" "+k);
    rows.push_back(address+" = inttoptr "+sum);
    auto w = t->isPointerTy() ? pw : width(t);
    return sourceLoad(address,w);
  }
  std::string gep(GEPOperator *g) {
    auto &dl = m.getDataLayout();
    unsigned p = dl.getPointerTypeSizeInBits(g->getType()), i = dl.getIndexTypeSizeInBits(g->getType());
    auto base = fresh("i"+std::to_string(p));
    rows.push_back(base+" = ptrtoint.i"+std::to_string(p)+" "+operand(g->getPointerOperand()));
    auto op = [&](unsigned w, std::string text) { auto n=fresh("i"+std::to_string(w)); rows.push_back(n+" = "+text); return n; };
    auto acc = i<p ? op(i,"trunc.i"+std::to_string(i)+" "+base) : base;
#if LLVM_VERSION_MAJOR >= 23
    SmallMapVector<Value *, APInt, 4> vars;
#else
    MapVector<Value *, APInt> vars;
#endif
    APInt offset(i,0);
    if (!g->collectOffset(dl,i,vars,offset)) unimplemented("§16.4 CC GEP",2,&f);
    for (auto &v : vars) {
      auto idx=operand(v.first);auto w=width(v.first->getType());
      if(w!=i)idx=op(i,std::string(w<i ? "sext.i" : "trunc.i")+std::to_string(i)+" "+idx);
      if(v.second!=1)idx=op(i,"mul "+idx+" "+operand(ConstantInt::get(m.getContext(),v.second)));
      acc=op(i,"add "+acc+" "+idx);
    }
    if(!offset.isZero())acc=op(i,"add "+acc+" "+operand(ConstantInt::get(m.getContext(),offset)));
    if(i<p) {
      auto lo=op(p,"zext.i"+std::to_string(p)+" "+acc);
      auto hi=op(p,"and "+base+" "+operand(ConstantInt::get(m.getContext(),APInt::getHighBitsSet(p,p-i))));
      acc=op(p,"or "+hi+" "+lo);
    }
    auto result=fresh("ptr");rows.push_back(result+" = inttoptr "+acc);return result;
  }
  bool compilingInplace = false;
  std::string inplaceTarget, inplaceFault;
  json::Array inplaceEvidence;
  std::map<std::string,std::pair<uint64_t,uint64_t>> verifiedPairs;
  std::map<uint64_t, AV> selectedFields;
  unsigned dispatchBlock = 0;
  Function *selectedCallee = nullptr;
  bool generalDescriptor = false;
  std::set<uint64_t> functionAddresses;
  uint64_t functionAddress(Function *fn) {
    if (auto address = comparisonFunctionAddress(*fn)) {
      functionAddresses.insert(*address);
      return *address;
    }
    if (hasComparisonLayout())
      fail("BD-E-COMPARISON-LAYOUT", "missing function address", fn);
    // Standalone comparison link, matching the module-order convention used
    // for data by the scalar linker. The production driver owns §19.5 layout.
    uint64_t address=4096;
    for(auto &g:m.globals())address=alignTo(address,m.getDataLayout().getPreferredAlign(&g))+m.getDataLayout().getTypeAllocSize(g.getValueType()).getFixedValue();
    address=alignTo(address,uint64_t(4096));
    for(auto &g:m) {
      if(&g==fn) {
        functionAddresses.insert(address);
        return address;
      }
      address+=16;
    }
    llvm_unreachable("function missing from comparison link");
  }
  AV intValue(uint64_t n, unsigned w=64) { Atom x; x.kind=Atom::Int;x.integer=APInt(w,n); AV v;v.atoms.insert(x);return v; }
  bool singletonInt(AV v) { return !v.top && v.atoms.size()==1 && v.atoms.begin()->kind==Atom::Int; }
  // The same unsigned, balanced compare tree serves candidate addresses,
  // fields, register identities and finite allocation widths (§14.2).
  void compareTree(std::string value, unsigned w, const std::vector<uint64_t> &keys,
                   const std::function<void(uint64_t)> &body, const std::string &bad) {
    std::function<void(unsigned,unsigned)> tree=[&](unsigned lo,unsigned hi) {
      if(lo==hi){rows.push_back("br ^"+bad+"()");return;}
      unsigned mid=(lo+hi)/2;auto key=keys[mid];
      auto k=operand(ConstantInt::get(IntegerType::get(m.getContext(),w),key)),eq=fresh("i1");
      auto leaf="dispatch"+std::to_string(dispatchBlock++),rest=leaf+"rest";
      rows.push_back(eq+" = icmp.eq "+value+" "+k);
      rows.push_back("br "+eq+" ^"+leaf+"() ^"+rest+"()");rows.push_back("^"+leaf+"():");body(key);
      rows.push_back("^"+rest+"():");
      if(hi-lo==1){rows.push_back("br ^"+bad+"()");return;}
      auto lt=fresh("i1"),left=rest+"left",right=rest+"right";
      rows.push_back(lt+" = icmp.ult "+value+" "+k);rows.push_back("br "+lt+" ^"+left+"() ^"+right+"()");
      rows.push_back("^"+left+"():");tree(lo,mid);rows.push_back("^"+right+"():");tree(mid+1,hi);
    };tree(0,keys.size());
  }
  void descriptor(CallBase &c) {
    auto &ctx=m.getContext();auto *u32=Type::getInt32Ty(ctx),*u64=Type::getInt64Ty(ctx);auto *ptr=PointerType::get(ctx,0);
    auto candidates=a.candidates(c.getArgOperand(0));
    auto *hl=m.getDataLayout().getStructLayout(StructType::get(ctx,{u32,u32,u32,u32,ptr,ptr}));
    auto *bl=m.getDataLayout().getStructLayout(StructType::get(ctx,{u32,u32,ptr,u64,u64}));
    bool general=memoryDescriptors || candidates.size()!=1 || !resolve(c.getArgOperand(0));
    // Keep the established straight-line encoding exactly when no new shape
    // field requires dispatch. ARG value bits remain runtime arguments.
    for(auto *fn:candidates) {
      for(unsigned off:{8u,unsigned(hl->getElementOffset(4)),unsigned(hl->getElementOffset(5))}) {
        auto v=descriptorField(c,off,off==8?static_cast<Type *>(u32):ptr);
        general |= v.top || v.atoms.size()!=1;
      }
      for(unsigned i=0;i<fn->arg_size();++i) {
        auto off=hl->getSizeInBytes()+i*bl->getSizeInBytes();auto k=descriptorField(c,off,u32);
        auto q=descriptorField(c,off+bl->getElementOffset(2),ptr);
        general |= q.top || q.atoms.size()!=1;
        if(!singletonInt(k) || integer(k,&c)!=2) {
          auto size=descriptorField(c,off+bl->getElementOffset(4),u64);general |= size.top || size.atoms.size()!=1;
        }
      }
      auto nd=descriptorField(c,8,u32);
      if(singletonInt(nd))for(unsigned j=0;j<integer(nd,&c);++j) {
        auto off=hl->getSizeInBytes()+fn->arg_size()*bl->getSizeInBytes()+j*24;
        for(unsigned d:{0u,8u,16u}){auto v=descriptorField(c,off+d,d==0?static_cast<Type *>(u32):d==8?static_cast<Type *>(ptr):u64);general |= v.top || v.atoms.size()!=1;}
      }
    }
    if(!general){descriptorLegacy(c);return;}
    generalDescriptor=true; generalUsed=true;
    auto id=std::to_string(dispatchBlock++),done="dispatch"+id+"done",bad="dispatch"+id+"bad";
    auto field=[&](uint64_t off,Type *t){return descriptorField(c,off,t);};
    auto pw=m.getDataLayout().getPointerSizeInBits();
    auto choose=[&](uint64_t off,Type *t,std::vector<AV> choices,const std::function<void(AV)> &body) {
      auto actual=field(off,t);std::map<uint64_t,AV> keyed;
      for(auto v:choices)for(auto x:v.atoms) {
        if(!actual.top && !actual.atoms.count(x))continue;
        uint64_t key=x.kind==Atom::Root ? (files.count(x.object)?files.at(x.object).identity:0) : x.integer.getLimitedValue();keyed[key]=v;
      }
      if(keyed.empty()){rows.push_back("br ^"+bad+"()");return;}
      auto leaf=[&](uint64_t key){selectedFields[off]=keyed.at(key);body(keyed.at(key));selectedFields.erase(off);};
      if(!actual.top && actual.atoms.size()==1 && keyed.size()==1){leaf(keyed.begin()->first);return;}
      std::vector<uint64_t> keys;for(auto &x:keyed)keys.push_back(x.first);
      auto value=fieldOperand(c,off,t);
      if(t->isPointerTy() && !memoryDescriptors) {
        if(auto *v=fieldValue(c,off,t); v && !tagged(a.get(v))) {auto n=fresh("i"+std::to_string(pw));rows.push_back(n+" = ptrtoint.i"+std::to_string(pw)+" "+value);value=n;}
      }
      compareTree(value,t->isPointerTy()?pw:width(t),keys,leaf,bad);
    };
    auto ints=[&](std::vector<uint64_t> ns,unsigned w){std::vector<AV> vs;for(auto n:ns)vs.push_back(intValue(n,w));return vs;};
    auto handles=[&](uint64_t off,bool null,const std::function<bool(unsigned)> &valid) {
      auto v=field(off,ptr);std::vector<AV> vs;
      if(null)vs.push_back(intValue(0,pw));
      for(auto &x:v.atoms)if(x.kind==Atom::Root && valid(qwidth(AV{{x},false},&c)))vs.push_back(AV{{x},false});
      return vs;
    };
    auto compile=[&](Function *fn) {
      selectedCallee=fn;
      choose(0,u32,ints({2},32),[&](AV){choose(4,u32,ints({fn->arg_size()},32),[&](AV){choose(12,u32,ints({0},32),[&](AV){
      choose(8,u32,ints({0,1,2,3,4},32),[&](AV nd){
      choose(hl->getElementOffset(4),ptr,handles(hl->getElementOffset(4),true,[](unsigned){return true;}),[&](AV){
      choose(hl->getElementOffset(5),ptr,handles(hl->getElementOffset(5),false,[](unsigned w){return w==4;}),[&](AV){
        std::function<void(unsigned)> devices;
        devices=[&](unsigned j) {
          if(j==integer(nd,&c)){
            std::set<const Value *> used;
            for(auto &v:selectedFields)for(auto &x:v.second.atoms)if(x.kind==Atom::Root) {
              if(!used.insert(x.object).second){rows.push_back("br ^"+bad+"()");return;}
              if(files.count(x.object)) {
                auto &slot=files.at(x.object);auto live=fresh("i"+std::to_string(pw)),ok=fresh("i1"),next="dispatch"+std::to_string(dispatchBlock++);
                rows.push_back(live+" = load.i"+std::to_string(pw)+" "+slot.tag);
                rows.push_back(ok+" = icmp.eq "+live+" "+operand(ConstantInt::get(IntegerType::get(ctx,pw),slot.identity)));
                rows.push_back("br "+ok+" ^"+next+"() ^"+bad+"()");rows.push_back("^"+next+"():");
              }
            }
            descriptorLeaf(c);rows.push_back("br ^"+done+"()");return;
          }
          auto off=hl->getSizeInBytes()+fn->arg_size()*bl->getSizeInBytes()+j*24;
          choose(off,u32,ints({1,2,3,4},32),[&](AV model){
            auto code=integer(model,&c);bool duplicate=false;
            for(unsigned k=0;k<j;++k)duplicate |= integer(selectedFields.at(off-(j-k)*24),&c)==code;
            if(duplicate){rows.push_back("br ^"+bad+"()");return;}
            choose(off+4,u32,ints({0},32),[&](AV){
              if(code==3){devices(j+1);return;}
              choose(off+8,ptr,handles(off+8,code==4,[&](unsigned w){auto unit=code==2?4096u:8u;return w%unit==0 && (code==4 || isPowerOf2_64(w/unit));}),[&](AV){
                // value is reserved outside CLOCK and does not affect a shape.
                selectedFields[off+16]=intValue(0);devices(j+1);selectedFields.erase(off+16);
              });
            });
          });
        };
        std::function<void(unsigned)> params;
        params=[&](unsigned i) {
          if(i==fn->arg_size()){devices(0);return;}
          auto *t=fn->getArg(i)->getType();auto off=hl->getSizeInBytes()+i*bl->getSizeInBytes();
          choose(off,u32,ints(t->isPointerTy()?std::vector<uint64_t>{1,2,3,4}:std::vector<uint64_t>{1,2},32),[&](AV kind){
            auto code=integer(kind,&c);
            choose(off+4,u32,ints(code==1?std::vector<uint64_t>{0,1}:std::vector<uint64_t>{0},32),[&](AV){
              if(code==2){params(i+1);return;}
              choose(off+bl->getElementOffset(2),ptr,handles(off+bl->getElementOffset(2),false,[&](unsigned w){return code==1?w<=(t->isPointerTy()?pw:width(t)):w%8==0 && w>0 && (code!=3 || isPowerOf2_64(w/8));}),[&](AV q){
                if(code==1){params(i+1);return;}
                auto n=qwidth(q,&c)/8;
                choose(off+bl->getElementOffset(4),u64,ints({n},64),[&](AV){params(i+1);});
              });
            });
          });
        };params(0);
      });});});});});});
      selectedCallee=nullptr;
    };
    if(candidates.size()==1 && resolve(c.getArgOperand(0)))compile(*candidates.begin());
    else {
      std::map<uint64_t,Function *> ordered;for(auto *fn:candidates)if(!fn->isDeclaration())ordered[functionAddress(fn)]=fn;
      auto address=fresh("i"+std::to_string(pw));rows.push_back(address+" = ptrtoint.i"+std::to_string(pw)+" "+operand(c.getArgOperand(0)));
      std::vector<uint64_t> keys;for(auto &v:ordered)keys.push_back(v.first);compareTree(address,pw,keys,[&](uint64_t k){compile(ordered.at(k));},bad);
    }
    rows.push_back("^"+bad+"():");rows.push_back("trap");rows.push_back("^"+done+"():");generalDescriptor=false;
  }
  void descriptorLegacy(CallBase &c) {
    auto &ctx = m.getContext();
    auto *u32 = Type::getInt32Ty(ctx), *u64 = Type::getInt64Ty(ctx);
    auto *ptr = PointerType::get(ctx, 0);
    auto *h = StructType::get(ctx, {u32,u32,u32,u32,ptr,ptr});
    auto *b = StructType::get(ctx, {u32,u32,ptr,u64,u64});
    auto *hl = m.getDataLayout().getStructLayout(h), *bl = m.getDataLayout().getStructLayout(b);
    std::vector<std::pair<uint64_t,std::vector<uint64_t>>> fields;
    auto domain = [&](uint64_t off, Type *t, std::vector<uint64_t> valid) {
      auto v = descriptorField(c,off,t);
      if (!v.top && v.atoms.size() == 1) return;
      if (!v.top) {
        std::vector<uint64_t> finite;
        for (auto &x : v.atoms) if (x.kind == Atom::Int &&
            std::find(valid.begin(),valid.end(),x.integer.getLimitedValue()) != valid.end()) finite.push_back(x.integer.getLimitedValue());
        valid = finite;
      }
      fields.push_back({off, valid});
    };
    auto candidates = a.candidates(c.getArgOperand(0));
    if (candidates.size() != 1) unimplemented("§7.2 production region dispatch",1,&c);
    auto *callee = *candidates.begin();
    domain(0,u32,{2}); domain(4,u32,{callee->arg_size()}); domain(12,u32,{0});
    unsigned idx = 0;
    for (auto &p : callee->args()) {
      auto off = hl->getSizeInBytes() + idx++ * bl->getSizeInBytes();
      domain(off,u32,p.getType()->isPointerTy() ? std::vector<uint64_t>{1,2,3,4} : std::vector<uint64_t>{1,2});
      domain(off+4,u32,{0,1});
    }
    if (fields.empty()) { descriptorLeaf(c); return; }
    auto id = std::to_string(dispatchBlock++), done = "dispatch" + id + "done", bad = "dispatch" + id + "bad";
    std::function<void(unsigned)> select = [&](unsigned index) {
      if (index == fields.size()) { descriptorLeaf(c); rows.push_back("br ^" + done + "()"); return; }
      auto off = fields[index].first;
      auto value = fieldOperand(c,off,u32);
      auto &keys = fields[index].second;
      std::function<void(unsigned,unsigned)> tree = [&](unsigned lo,unsigned hi) {
        if (lo == hi) { rows.push_back("br ^" + bad + "()"); return; }
        auto mid = (lo+hi)/2; auto key = keys[mid];
        auto k = operand(ConstantInt::get(u32,key)), eq = fresh("i1");
        auto leaf = "dispatch" + std::to_string(dispatchBlock++), rest = leaf + "rest";
        rows.push_back(eq + " = icmp.eq " + value + " " + k);
        rows.push_back("br " + eq + " ^" + leaf + "() ^" + rest + "()");
        rows.push_back("^" + leaf + "():");
        Atom atom; atom.kind = Atom::Int; atom.integer = APInt(32,key); AV v; v.atoms.insert(atom); selectedFields[off] = v;
        select(index+1); selectedFields.erase(off);
        rows.push_back("^" + rest + "():");
        if (hi-lo == 1) { rows.push_back("br ^" + bad + "()"); return; }
        auto lt = fresh("i1"), left = rest + "left", right = rest + "right";
        rows.push_back(lt + " = icmp.ult " + value + " " + k);
        rows.push_back("br " + lt + " ^" + left + "() ^" + right + "()");
        rows.push_back("^" + left + "():"); tree(lo,mid);
        rows.push_back("^" + right + "():"); tree(mid+1,hi);
      };
      tree(0,keys.size());
    };
    select(0); rows.push_back("^" + bad + "():"); rows.push_back("trap"); rows.push_back("^" + done + "():");
  }
  void descriptorLeaf(CallBase &c) {
    auto *desc = c.getArgOperand(2);
    auto &ctx = m.getContext();
    auto *u32 = Type::getInt32Ty(ctx), *u64 = Type::getInt64Ty(ctx);
    auto *ptr = PointerType::get(ctx, 0);
    auto *h = StructType::get(ctx, {u32, u32, u32, u32, ptr, ptr});
    auto *b = StructType::get(ctx, {u32, u32, ptr, u64, u64});
    auto &dl = m.getDataLayout();
    auto *hl = dl.getStructLayout(h), *bl = dl.getStructLayout(b);
    auto field = [&](uint64_t off, Type *t) {
      return selectedFields.count(off) ? selectedFields.at(off) : descriptorField(c, off, t);
    };
    if (integer(field(0, u32), &c) != 2 || integer(field(12, u32), &c) != 0)
      fail("T-IFACE", "§8.1 descriptor header", &c);
    auto ndev = integer(field(8, u32), &c);
    auto candidates = a.candidates(c.getArgOperand(0));
    auto *callee = selectedCallee ? selectedCallee : *candidates.begin();
    if (integer(field(4, u32), &c) != callee->arg_size())
      fail("T-IFACE", "§8.2 descriptor arity", &c);
    auto target = field(hl->getElementOffset(4), ptr),
         fault = field(hl->getElementOffset(5), ptr);
    if (!compilingInplace && qwidth(fault, &c) != 4)
      fail("T-SIZE", "§8.2 fault width", &c);
    bool discard = !target.top && target.atoms.size() == 1 &&
                   target.atoms.begin()->kind == Atom::Int &&
                   target.atoms.begin()->integer.isZero();
    std::vector<std::string> ins, args, mems;
    AV output = target;
    std::vector<AV> outputs;
    if (!discard) outputs.push_back(target);
    bool bufferOutput = false;
    std::string current;
    unsigned index = 0;
    for (Argument &p : callee->args()) {
      auto off = hl->getSizeInBytes() + index++ * bl->getSizeInBytes();
      auto kind = integer(field(off, u32), &c),
           mode = integer(field(off + bl->getElementOffset(1), u32), &c);
      if (!current.empty())
        current += ",";
      if (kind == 1 && mode <= 1) {
        auto q = field(off + bl->getElementOffset(2), ptr);
        current += "IN(" + std::to_string(qwidth(q, &c)) + "," +
                   (mode ? "sext" : "zext") + ")";
        ins.push_back(handle(q, &c));
      } else if (kind == 2) {
        auto w = width(p.getType());
        auto low = field(off + bl->getElementOffset(3), u64), high = field(off + bl->getElementOffset(4), u64);
        auto singleton = [](AV v) { return !v.top && v.atoms.size()==1 && v.atoms.begin()->kind==Atom::Int; };
        std::string n;
        if (singleton(low) && singleton(high)) {
          APInt val = APInt(128,integer(low,&c)) | (APInt(128,integer(high,&c)) << 64);
          n = fresh("i" + std::to_string(w));
          rows.push_back(n + " = const.i" + std::to_string(w) + " " + decimal(val.zextOrTrunc(w)));
        } else {
          auto cast = [&](std::string x, unsigned from) {
            if (w == from) return x;
            auto d = fresh("i" + std::to_string(w));
            rows.push_back(d + (w < from ? " = trunc.i" : " = zext.i") + std::to_string(w) + " " + x); return d;
          };
          auto part = [&](AV v, uint64_t offset) { return singleton(v) ? operand(ConstantInt::get(u64,integer(v,&c))) : fieldOperand(c,offset,u64); };
          n = cast(part(low,off+bl->getElementOffset(3)),64);
          if (w > 64) {
            auto hi = cast(part(high,off+bl->getElementOffset(4)),64);
            auto shift = operand(ConstantInt::get(IntegerType::get(ctx,w),64)), bits = fresh("i"+std::to_string(w)), combined = fresh("i"+std::to_string(w));
            rows.push_back(bits + " = shl " + hi + " " + shift); rows.push_back(combined + " = or " + n + " " + bits); n = combined;
          }
        }
        args.push_back(n);
        current += "ARG(" + std::to_string(w) + ")";
      } else if (kind == 3 || kind == 4) {
        if (!p.getType()->isPointerTy() || mode)
          fail("T-IFACE", "§8.2 memory binding carrier/mode", &c);
        auto q = field(off + bl->getElementOffset(2), ptr);
        auto size = integer(field(off + bl->getElementOffset(4), u64), &c);
        if (!size || size > UINT64_MAX / 8 || qwidth(q, &c) != size * 8)
          fail("T-SIZE", "§8.2 memory binding width", &c);
        if (kind == 3) {
          if (!isPowerOf2_64(size)) fail("T-SIZE", "§8.2 MEM_IN power of two", &c);
          current += "MEM_IN(" + std::to_string(size) + ")";
          mems.push_back(handle(q, &c));
        } else {
          current += "OUT(" + std::to_string(size) + ")";
          outputs.push_back(q);
          output = q; bufferOutput = true;
        }
      } else
        fail("T-IFACE", "§8.2 oracle binding kind", &c);
    }
    std::vector<std::string> deviceMems;
    std::set<uint64_t> models;
    for (unsigned j = 0; j < ndev; ++j) {
      auto off = hl->getSizeInBytes() + index * bl->getSizeInBytes() + j * 24;
      auto model = integer(field(off, u32), &c);
      if (!models.insert(model).second || integer(field(off + 4, u32), &c))
        fail("T-IFACE", "§8.3 duplicate model or device mode", &c);
      auto q = field(off + 8, ptr);
      auto clock=field(off+16,u64);
      auto value = model==3 && singletonInt(clock) ? integer(clock,&c) : 0;
      auto separator = j ? std::string("+") : std::string(";dev=");
      if (model == 3) {
        if(singletonInt(clock))current += separator + "CLOCK(" + std::to_string(value) + ")";
        else { current += separator + "CLOCK_ARG(0)"; args.insert(args.begin(),fieldOperand(c,off+16,u64)); }
      }
      else if (model == 2 || model == 1) {
        auto w = qwidth(q, &c), bytes = w / 8;
        auto unit = model == 2 ? 512 : 1;
        if (w % 8 || bytes < unit || !isPowerOf2_64(bytes / unit))
          fail("T-SIZE", "§8.3 device input extent", &c);
        current += separator + (model == 2 ? "BLOCK(" : "ENTROPY(") +
                   std::to_string(Log2_64(bytes / unit)) + ")";
        deviceMems.push_back(handle(q, &c));
      } else if (model == 4) {
        bool null = !q.top && q.atoms.size()==1 && q.atoms.begin()->kind==Atom::Int && q.atoms.begin()->integer.isZero();
        auto w = null ? 0 : qwidth(q, &c);
        if (w % 8) fail("T-SIZE", "§8.3 console width", &c);
        current += separator + "CONSOLE(" + std::to_string(w / 8) + ")";
        if (!null) { outputs.push_back(q); output = q; bufferOutput = true; }
      } else fail("T-IFACE", "§8.3 unknown device model", &c);
    }
    mems.insert(mems.begin(),deviceMems.begin(),deviceMems.end());
    struct Slice { AV output; unsigned lo, width; };
    std::vector<Slice> slices;
    for (auto &o : outputs) { auto w=qwidth(o,&c); for (unsigned lo=0;lo<w;lo+=128) slices.push_back({o,lo,std::min(128u,w-lo)}); }
    bool multi = slices.size()>1;
    current += ";tgt=" + ((multi ? discard : discard && !bufferOutput) ? std::string("null")
                                  : std::to_string(qwidth(multi ? target : output, &c)));
    discard = discard && !bufferOutput;
    // Null selects the resolved default. Explicit records use the published
    // four i64 fields + fault handle; all-ones means table/default lookup.
    auto baseline = table.baseline(*callee);
    std::vector<uint64_t> budget = baseline, explicitFields(5, UINT64_MAX);
    if (!isa<ConstantPointerNull>(c.getArgOperand(1))) {
      auto *bp = c.getArgOperand(1);
      for (unsigned i = 0; i < 4; ++i) {
        auto n = integer(a.readAt(c, bp, 8 * i, u64), &c);
        explicitFields[i] = n;
        if (n != UINT64_MAX) budget[i] = n;
      }
    }
    for (int projection = multi ? int(slices.size())-1 : -1; projection >= (multi ? 0 : -1); --projection) {
    budget = baseline;
    for (unsigned i=0;i<5;++i) if (explicitFields[i]!=UINT64_MAX) budget[i]=explicitFields[i];
    std::string refName = "ref";
    ValueToValueMapTy vm;
    auto clone = CloneModule(m, vm);
    auto *cf = cast<Function>(vm[callee]);
    cf=normaliseWideABI(*clone,cf);
    normaliseScalar(*cf);
    auto path = out + "/oracle-" + std::to_string(references.size());
    auto capacities = table.capacities;
    std::map<std::string,std::string> globalNames;
    lowerScalar(*clone, *cf, current, path, capacities[2], capacities[1], projection, &globalNames, baseline[4], automaticSnapshot?snapshotExponent:0);
    auto candidate = read(path + "/ref.bennett");
    auto selection = oracleIdentity(candidate);
    table.overlay(budget, selection);
    for (unsigned i = 0; i < 5; ++i)
      if (explicitFields[i] != UINT64_MAX) budget[i] = explicitFields[i];
    // §9.2: one overlay, then a fresh generation under the SAME capacities.
    // Never reuse the provisional module: N24/runtime materialisation mutates it.
    if (budget[4] != baseline[4]) {
      ValueToValueMapTy finalMap;
      auto finalModule = CloneModule(m, finalMap);
      auto *finalFunction = cast<Function>(finalMap[callee]);
      finalFunction=normaliseWideABI(*finalModule,finalFunction);
      normaliseScalar(*finalFunction);
      globalNames.clear();
      lowerScalar(*finalModule, *finalFunction, current, path, capacities[2],
                  capacities[1], projection, &globalNames, budget[4], automaticSnapshot?snapshotExponent:0);
      candidate = read(path + "/ref.bennett");
    }
    if (table.enabled) resolvedShapes.push_back(json::Object{
      {"region_key", regionKey(callee)}, {"symbol", callee->getName()}, {"shape", current},
      {"selection_identity", selection}, {"identity", oracleIdentity(candidate)},
      {"baseline", tuple(baseline)}, {"resolved", tuple(budget)}});
    unsigned ri = 0;
    while (ri < references.size() && (references[ri] != candidate || referenceGlobals[ri] != globalNames)) ++ri;
    if (ri == references.size()) { references.push_back(candidate); referenceGlobals.push_back(globalNames); }
    else sys::fs::remove_directories(path);
    if (ri) refName += std::to_string(ri);
    if (reference.empty()) { reference = candidate; shape = current; refPath = path; }
    // Tokens are minted by the host, positional launch parameters per ISA §10.
    std::string tk = "tk" + std::to_string(budgets.size());
    params.push_back(tk + ":token");
    paramTypes.push_back("token");
    budgets.push_back(json::Object{{"token", tk},
                                   {"selection_identity", selection},
                                   {"steps", std::to_string(budget[0])},
                                   {"heap", std::to_string(budget[1])},
                                   {"stack", std::to_string(budget[2])},
                                   {"depth", std::to_string(budget[3])},
                                   {"sstack", std::to_string(budget[4])}});
    if (refName != "ref") budgets.back()["region"] = refName;
    std::string tgt, faultRegister = compilingInplace ? inplaceFault : handle(fault,&c);
    if (multi) {
      auto &slice = slices[projection];
      if (projection) {
        tgt = fresh("qreg["+std::to_string(slice.width)+"]");
        rows.push_back(tgt+" = qreg.new any "+std::to_string(slice.width));
        faultRegister=fresh("qreg[4]");rows.push_back(faultRegister+" = qreg.new any 4");
      } else { tgt=fresh("qreg["+std::to_string(slice.width)+"]"); rows.push_back(tgt+" = qreg.slice "+handle(slice.output,&c)+" "+std::to_string(slice.lo)+" "+std::to_string(slice.width)); }
    } else if (discard) {
      tgt = fresh("qreg[1]"); rows.push_back(tgt + " = qreg.new any 1");
    } else tgt = compilingInplace ? inplaceTarget : handle(output, &c);
    std::string snapshotData,snapshotQ;
    auto callMems=mems;
    if(automaticSnapshot){snapshotData=buildSnapshot();snapshotQ=prepareSnapshot(snapshotData);callMems.insert(callMems.begin(),snapshotQ);}
    auto call = "oracle_call @" + refName + " " + tk + " (" + join(ins) + ") " + tgt + " " + faultRegister + " (" + join(callMems) + ") (" + join(args) + ")";
    rows.push_back(call);
    if (multi && projection) {
      auto &slice=slices[projection];auto view=fresh("qreg["+std::to_string(slice.width)+"]");
      rows.push_back(view+" = qreg.slice "+handle(slice.output,&c)+" "+std::to_string(slice.lo)+" "+std::to_string(slice.width));
      auto w=std::to_string(slice.width);
      auto xorAction=action("d:wire["+w+"] mut","s:wire["+w+"] in",w,w,"qxor s d");
      rows.push_back("action_call @"+xorAction+" ("+view+") ("+tgt+") () ()");rows.push_back(call);
      rows.push_back("qreg.free "+faultRegister);rows.push_back("qreg.free "+tgt);
    } else if (discard) rows.push_back("qreg.free " + tgt);
    if(automaticSnapshot)releaseSnapshot(snapshotQ,snapshotData);
    }
  }
  void verifyInverse(unsigned forward, unsigned inverse, unsigned bits, CallBase &at) {
    auto key=hash(references.at(forward)+references.at(inverse));
    auto checkBudget=[&](uint64_t stepsMinimum,uint64_t stackMinimum) {
      for(unsigned i=budgets.size()-2;i<budgets.size();++i) {
        auto &b=budgets[i];uint64_t steps,cells,depth;
        b.getString("steps")->getAsInteger(10,steps);b.getString("stack")->getAsInteger(10,cells);b.getString("depth")->getAsInteger(10,depth);
        if(steps<stepsMinimum || cells<stackMinimum || depth<1)fail("BD-E-INPLACE-NOT-INVERSE","§8.7 budget below exhaustive B_min",&at);
      }
    };
    if(verifiedPairs.count(key)) { auto minima=verifiedPairs.at(key);checkBudget(minima.first,minima.second);return; }
    if(bits>24)unimplemented("§8.7 sampled inverse evidence and sound universal budget bound",1,&at);
    for(auto i:{forward,inverse}) {
      auto object=StringRef(references.at(i));auto body=object.split("lproc @L1").second;
      if(object.contains("lift.alloc") || object.contains("lift.load") || object.contains("lift.store") || body.contains("lift.call"))
        unimplemented("§8.7 general inverse reference budget verification",1,&at);
    }
    const char *configured=std::getenv("BENNETT_ISA_REF");
    auto tool=sys::findProgramByName(configured ? configured : "bennett-isa-ref");
    if(!tool)fail("input","§8.7 requires bennett-isa-ref (or BENNETT_ISA_REF)",&at);
    auto output=out+"/inplace-reference.json";
    uint64_t maxSteps=0,minStack=0;
    auto evaluate=[&](unsigned ref,uint64_t x,uint64_t cells) {
      auto path=out+"/oracle-"+std::to_string(ref)+"/ref.bennett";
      auto text=std::to_string(x),budget="18446744073709551615,0,"+std::to_string(cells)+",1";
      SmallVector<StringRef> args{*tool,"run-oracle",path,"ref","--input",text,"--budget",budget};
      std::optional<StringRef> redirects[]={StringRef(),StringRef(output),StringRef()};
      sys::fs::remove(output);
      std::string error;auto status=sys::ExecuteAndWait(*tool,args,std::nullopt,redirects,0,0,&error);
      if(status)fail("output","§8.7 reference interpreter failed: "+error,&at);
      return parse(read(output));
    };
    for(auto ref:{forward,inverse}) {
      auto layout=parse(objectSectionsForInverse(references.at(ref)));
      uint64_t capacity=uint64_t(1)<<*layout.getAsObject()->getInteger("S_cells");
      // One direct lproc has one fixed frame shape on every input (§3.7).
      // With no memory or nested calls, heap minimum is zero and depth one.
      uint64_t lo=0,hi=capacity;
      while(lo<hi) {auto mid=(lo+hi)/2;auto v=evaluate(ref,0,mid);if(v.getAsObject()->getInteger("code")==0)hi=mid;else lo=mid+1;}
      minStack=std::max(minStack,lo);
    }
    uint64_t count=uint64_t(1)<<bits;
    for(uint64_t x=0;x<count;++x) {
      auto y=evaluate(forward,x,minStack);auto *yo=y.getAsObject();auto payload=yo->getInteger("payload");
      if(yo->getInteger("code")!=0 || !payload)fail("BD-E-INPLACE-NOT-INVERSE","§8.7 forward fault",&at);
      auto z=evaluate(inverse,*payload,minStack);auto *zo=z.getAsObject();
      if(zo->getInteger("code")!=0 || zo->getInteger("payload")!=int64_t(x))fail("BD-E-INPLACE-NOT-INVERSE","§8.7 inverse mismatch",&at);
      maxSteps=std::max({maxSteps,uint64_t(*yo->getInteger("steps")),uint64_t(*zo->getInteger("steps"))});
    }
    checkBudget(maxSteps,minStack);
    inplaceEvidence.push_back(json::Object{{"kind","exhaustive"},{"bits",bits},{"inputs",int64_t(count)},
      {"forward",hash(references.at(forward))},{"inverse",hash(references.at(inverse))},
      {"B_min",json::Object{{"steps",int64_t(maxSteps)},{"heap",0},{"stack",int64_t(minStack)},{"depth",1}}},
      {"interpreter_sha256",hash(read(*tool))},{"checked_executable_claim",false}});
    verifiedPairs[key]={maxSteps,minStack};write(out+"/inplace-evidence.json",jcs(json::Value(parse(jcs(json::Value(std::move(inplaceEvidence))))))+"\n");
    // Keep the evidence array available for another pair in this entry.
    auto evidence=parse(read(out+"/inplace-evidence.json"));inplaceEvidence=std::move(*evidence.getAsArray());
    sys::fs::remove(output);
  }
  std::string objectSectionsForInverse(StringRef object) {
    return object.split("section layout\n").second.split('\n').first.str();
  }
  void inplace(CallBase &c) {
    auto &ctx=m.getContext();auto *u32=Type::getInt32Ty(ctx);auto *ptr=PointerType::get(ctx,0);
    auto *desc=c.getArgOperand(3);
    auto header=a.readAt(c,desc,0,u32),flags=a.readAt(c,desc,12,u32),np=a.readAt(c,desc,4,u32);
    if(integer(header,&c)!=2 || integer(flags,&c)!=0)fail("T-IFACE","§8.7 descriptor header",&c);
    auto target=a.readAt(c,desc,16,ptr);
    if(target.top || target.atoms.size()!=1 || target.atoms.begin()->kind!=Atom::Int || !target.atoms.begin()->integer.isZero())fail("T-IFACE","§8.7 target must be null",&c);
    if(integer(np,&c)!=1 || integer(a.readAt(c,desc,8,u32),&c)!=0 || integer(a.readAt(c,desc,32,u32),&c)!=5)
      unimplemented("§8.7 general INOUT parameter and device bindings",1,&c);
    auto q=a.readAt(c,desc,40,ptr);auto w=qwidth(q,&c);auto x=handle(q,&c);
    auto t=fresh("qreg["+std::to_string(w)+"]"),fr=fresh("qreg[4]");
    rows.push_back(t+" = qreg.new any "+std::to_string(w));rows.push_back(fr+" = qreg.new any 4");
    auto oracle=m.getOrInsertFunction("__bennett_oracle",FunctionType::get(Type::getVoidTy(ctx),{ptr,ptr,ptr},false));
    Atom kind;kind.kind=Atom::Int;kind.integer=APInt(32,1);AV in;in.atoms.insert(kind);
    selectedFields[32]=in;selectedFields[16]=q;
    compilingInplace=true;inplaceTarget=t;inplaceFault=fr;
    unsigned refs[2];
    for(unsigned i=0;i<2;++i) {
      auto *call=CallInst::Create(oracle,{c.getArgOperand(i),c.getArgOperand(2),desc},"",&c);
      auto before=budgets.size();descriptorLeaf(*call);
      auto region=budgets.at(before).getString("region").value_or("ref");
      refs[i]=region=="ref"?0:std::stoul(region.drop_front(3).str());call->eraseFromParent();
      if(!i) {
        auto width=std::to_string(w);auto swap=action("x:wire["+width+"] mut, t:wire["+width+"] mut","",width+","+width,"","qexch x t");
        rows.push_back("action_call @"+swap+" ("+x+", "+t+") () () ()");
      }
    }
    compilingInplace=false;selectedFields.clear();
    verifyInverse(refs[0],refs[1],w,c);
    rows.push_back("qreg.free "+fr);rows.push_back("qreg.free "+t);
  }
  std::string action(std::string mut, std::string in, std::string widths,
                     std::string inWidths, std::string ops) {
    auto n = "M" + std::to_string(actions.size());
    std::string sig = "{\"abi\":\"0.8\",\"args\":[],\"bounds\":[],\"in\":[" +
                      inWidths + "],\"kind\":\"action\",\"mem\":[],\"mut\":[" +
                      widths + "],\"tier\":\"q\"}";
    actions[n] = {sig, "action @" + n + " (" + mut + ") (" + in +
                           ") () () ()\n^entry():\n" + ops};
    return n;
  }
  bool controlledIdentity(CallBase &call) {
    auto *body=resolve(call.getArgOperand(2));
    if(!body || body->isDeclaration() || body->size()!=1)return false;
    unsigned instructions=0;
    for(auto &i:body->getEntryBlock())if(!isa<DbgInfoIntrinsic>(i)) {
      if(!isa<ReturnInst>(i) || cast<ReturnInst>(i).getReturnValue())return false;
      ++instructions;
    }
    // This is an identity proof, not evaluation of a general generation.
    // One return consumes one G step; a positive resolved default proves no
    // generation fault can occur. Other generations use the general path.
    if(instructions!=1 || !isa<ConstantPointerNull>(call.getArgOperand(3)))return false;
    auto budget=table.baseline(*body);
    if(!budget[0])return false;
    auto index=integer(a.get(call.getArgOperand(1)),&call);
    auto width=qwidth(a.get(call.getArgOperand(0)),&call);
    withHandle(call.getArgOperand(0),[&](std::string control) {
      if(index>=width) {
        rows.push_back("trap");rows.push_back("^control"+std::to_string(dispatchBlock++)+"unreachable():");return;
      }
      auto wire="c["+std::to_string(index)+"]";
      auto name=action("","c:wire["+std::to_string(width)+"] in","",std::to_string(width),
        "qpred "+wire+"\nqunpred "+wire);
      rows.push_back("action_call @"+name+" () ("+control+") () ()");
    });
    controlledIdentities.push_back(json::Object{{"source",body->getName()},
      {"region_key",regionKey(body)},{"generation_steps",1},{"resolved_budget",tuple(budget)}});
    return true;
  }
  void gate(CallBase &c) {
    auto measurement = c.getCalledFunction()->getName() == "__bennett_measure";
    auto *v = c.getArgOperand(measurement ? 0 : 1);
    auto result = measurement && tagged(a.get(v)) ? fresh("i1") : "";
    withHandle(v, [&](std::string q) { gateOn(c,q); }, false, result, &c);
    if(!result.empty())names[&c]=result;
  }
  void gateOn(CallBase &c, std::string src) {
    bool measurement=c.getCalledFunction()->getName()=="__bennett_measure";
    auto *index=c.getArgOperand(measurement?1:2);
    auto width=qwidth(a.get(c.getArgOperand(measurement?0:1)),&c);
    auto indices=a.get(index),ops=measurement?intValue(0,32):a.get(c.getArgOperand(0));
    if(singletonInt(indices) && singletonInt(ops) && integer(indices,&c)<width) {
      gateLeaf(c,src,integer(indices,&c),integer(ops,&c));return;
    }
    auto id=std::to_string(dispatchBlock++),done="gate"+id+"done",bad="gate"+id+"bad";
    auto result=measurement?fresh("i1"):"";
    auto choose=[&](Value *value,AV domain,std::vector<uint64_t> keys,const std::function<void(uint64_t)> &body) {
      if(!domain.top) {
        std::vector<uint64_t> finite;
        for(auto key:keys)if(domain.atoms.count(*intValue(key,cast<IntegerType>(value->getType())->getBitWidth()).atoms.begin()))finite.push_back(key);
        keys=std::move(finite);
      }
      if(keys.empty()){rows.push_back("br ^"+bad+"()");return;}
      if(singletonInt(domain) && keys.size()==1){body(keys[0]);return;}
      compareTree(operand(value),widthOf(value),keys,body,bad);
    };
    std::vector<uint64_t> keys;for(uint64_t i=0;i<width;++i)keys.push_back(i);
    choose(index,indices,keys,[&](uint64_t i) {
      auto leaf=[&](uint64_t op) {
        gateLeaf(c,src,i,op);
        rows.push_back("br ^"+done+"("+(measurement?names.at(&c):"")+")");
      };
      if(measurement)leaf(0);
      else choose(c.getArgOperand(0),ops,{1,2,3,4,5,6,7,8},leaf);
    });
    rows.push_back("^"+bad+"():");rows.push_back("trap");
    rows.push_back("^"+done+"("+(measurement?result+":i1":"")+"):");
    if(measurement)names[&c]=result;
  }
  unsigned widthOf(Value *value) {return width(value->getType());}
  void gateLeaf(CallBase &c, std::string src,uint64_t i,uint64_t op) {
    auto n = c.getCalledFunction()->getName();
    bool measurement = n == "__bennett_measure";
    auto q = a.get(c.getArgOperand(measurement ? 0 : 1));
    auto w = qwidth(q, &c);
    if (i >= w)
      fail("T-INDEX", "§18.3 gate/measurement index", &c);
    if (measurement) {
      auto name =
          action("d:wire[1] mut", "s:wire[" + std::to_string(w) + "] in", "1",
                 std::to_string(w), "cx s[" + std::to_string(i) + "] d[0]");
      auto copy = fresh("qreg[1]");
      rows.push_back(copy + " = qreg.new any 1");
      rows.push_back("action_call @" + name + " (" + copy + ") (" + src +
                     ") () ()");
      auto value = fresh("i1");
      names[&c] = value;
      rows.push_back(value + " = measure " + copy);
    } else {
      static const char *ops[] = {"", "x", "h", "s", "sdg", "t", "tdg"};
      std::string wire = "s[" + std::to_string(i) + "]", row;
      if (op >= 1 && op <= 6)
        row = std::string(ops[op]) + " " + wire;
      else if (op == 7)
        row = "s " + wire + "\ns " + wire;
      else if (op == 8)
        row = "sdg " + wire + "\nx " + wire + "\ns " + wire;
      else
        fail("T-OP", "§3.4 gate opcode", &c);
      auto name = action("s:wire[" + std::to_string(w) + "] mut", "",
                         std::to_string(w), "", row);
      rows.push_back("action_call @" + name + " (" + src + ") () () ()");
    }
  }
#include "runtime/CallerSnapshot.inc"
  void allocateRegister(CallBase &call, const std::string &q, uint64_t width) {
    std::vector<std::string> classes = {"any"};
    if (auto *metadata = m.getModuleFlag("bennett.classes")) {
      auto *table = dyn_cast<MDNode>(metadata);
      if (!table) fail("BD-E-OPERAND", "malformed register class table", &call);
      for (auto &item : table->operands()) {
        auto *name = dyn_cast<MDString>(item.get());
        if (!name) fail("BD-E-OPERAND", "malformed register class name", &call);
        classes.push_back(name->getString().str());
      }
    }
    auto domain = a.get(call.getArgOperand(0));
    auto allocate = [&](uint64_t index, const std::string &destination) {
      rows.push_back(destination + " = qreg.new " + classes.at(index) + " " + std::to_string(width));
    };
    if (singletonInt(domain)) {
      auto index = integer(domain, &call);
      if (index >= classes.size()) fail("BD-E-OPERAND", "register class index outside the link table", &call);
      allocate(index, q);
      return;
    }
    std::vector<uint64_t> keys;
    for (uint64_t index = 0; index < classes.size(); ++index)
      if (domain.top || domain.atoms.count(*intValue(index).atoms.begin())) keys.push_back(index);
    auto value = operand(call.getArgOperand(0));
    auto id = std::to_string(dispatchBlock++), done = "class" + id + "done", bad = "class" + id + "bad";
    compareTree(value, 64, keys, [&](uint64_t index) {
      auto instance = fresh("qreg[" + std::to_string(width) + "]");
      allocate(index, instance);
      rows.push_back("br ^" + done + "(" + instance + ")");
    }, bad);
    rows.push_back("^" + bad + "():");
    rows.push_back("trap");
    rows.push_back("^" + done + "(" + q + ":qreg[" + std::to_string(width) + "]):");
  }
  void prepareLowering() {
    setupSnapshot();
    // Descriptor memory has no device representation: its fields are virtual
    // operands. Elide only local storage whose complete use closure is records.
    for (Instruction &i : instructions(f))
      if (auto *c = dyn_cast<CallBase>(&i))
        if (c->getCalledFunction() &&
            (c->getCalledFunction()->getName() == "__bennett_oracle" || c->getCalledFunction()->getName() == "__bennett_inplace")) {
          bool ip=c->getCalledFunction()->getName()=="__bennett_inplace";
          descriptorObjects.insert(getUnderlyingObject(c->getArgOperand(ip?3:2)));
          for(auto &base:a.get(c->getArgOperand(ip?3:2)).atoms)if(base.kind==Atom::Ptr && base.object)descriptorObjects.insert(base.object);
          if (!isa<ConstantPointerNull>(c->getArgOperand(ip?2:1)))
            descriptorObjects.insert(getUnderlyingObject(c->getArgOperand(ip?2:1)));
        }
    // Preserve elision for straight-line record-only descriptors. Once an
    // address escapes that proof, lower the storage and all its ordinary uses.
    for (Instruction &i : instructions(f)) {
      if (auto *c = dyn_cast<CallBase>(&i); c && c->getCalledFunction() && c->getCalledFunction()->getName()=="__bennett_oracle") {
        auto base=a.get(c->getArgOperand(2));
        if(base.top || base.atoms.size()!=1 || !isa<AllocaInst>(getUnderlyingObject(c->getArgOperand(2))))memoryDescriptors=true;
        for(auto &x:base.atoms) for(auto &j:instructions(f))
          if(auto *st=dyn_cast<StoreInst>(&j); st && st->getParent()!=c->getParent())
            for(auto &d:a.get(st->getPointerOperand()).atoms)if(d.object==x.object)memoryDescriptors=true;
      }
      if (auto *ld=dyn_cast<LoadInst>(&i); ld && descriptorObjects.count(getUnderlyingObject(ld->getPointerOperand())))memoryDescriptors=true;
    }
    std::set<const Value *> visited;
    std::function<void(const Value *)> validate = [&](const Value *v) {
      if (!visited.insert(v).second)
        return;
      for (const User *u : v->users()) {
        if (isa<GetElementPtrInst>(u) || isa<BitCastInst>(u)) {
          validate(u);
          continue;
        }
        if (auto *s = dyn_cast<StoreInst>(u); s && s->getPointerOperand() == v)
          continue;
        if (auto *c = dyn_cast<CallBase>(u))
          if (auto *g = c->getCalledFunction();
              g && (g->getName() == "__bennett_oracle" || g->getName() == "__bennett_inplace" ||
                    g->getName().starts_with("llvm.lifetime.") ||
                    g->getName().starts_with("llvm.memset.")))
            continue;
        unimplemented("§8.1 escaping descriptor storage", 1, u);
      }
    };
    if (!memoryDescriptors) for (auto *v : descriptorObjects) validate(v);
    // Acyclic entry-local files have one physical instance per allocation
    // site. General N(s), recursive environments and surviving-entry files
    // require the interprocedural bound/table implementation, never slot reuse.
    std::set<const Value *> memoryRoots;
    for (Instruction &i : instructions(f)) if (auto *st = dyn_cast<StoreInst>(&i))
      if (memoryDescriptors || !descriptorObjects.count(getUnderlyingObject(st->getPointerOperand())))
        for (auto &x : a.get(st->getValueOperand()).atoms) if (x.kind == Atom::Root) memoryRoots.insert(x.object);
    for(Instruction &i:instructions(f)) if(isa<SelectInst>(i) || isa<PHINode>(i)) {
      bool descriptorUse=i.getName().starts_with("width.handle");
      for(auto *u:i.users())if(auto *st=dyn_cast<StoreInst>(u))descriptorUse |= descriptorObjects.count(getUnderlyingObject(st->getPointerOperand()));
      auto v=a.get(&i); if(descriptorUse && v.roots())for(auto &x:v.atoms)if(x.kind==Atom::Root)memoryRoots.insert(x.object);
    }
    bool enlarged=true;
    while(enlarged) {
      enlarged=false;
      for(Instruction &i:instructions(f)) {
        auto v=a.get(&i);bool shares=false;
        for(auto &x:v.atoms) if(x.kind==Atom::Root && memoryRoots.count(x.object)) shares=true;
        if(shares) for(auto &x:v.atoms) if(x.kind==Atom::Root) enlarged |= memoryRoots.insert(x.object).second;
      }
    }
    if (!memoryRoots.empty()) {
      for (Instruction &i : instructions(f)) {
        if (auto *st = dyn_cast<StoreInst>(&i); st && a.get(st->getValueOperand()).roots() &&
            !isa<AllocaInst>(getUnderlyingObject(st->getPointerOperand())) &&
            !descriptorObjects.count(getUnderlyingObject(st->getPointerOperand())))
          unimplemented("§6.5 persistent static-file tag allocator",1,st);
        if (auto *r = dyn_cast<ReturnInst>(&i); r && r->getReturnValue() && a.get(r->getReturnValue()).roots())
          unimplemented("§6.5 static-file result environment",1,r);
      }
      std::set<const BasicBlock *> visiting, visited;
      for(auto *root:memoryRoots)if(auto *site=dyn_cast<Instruction>(root)) {
        visiting.clear();visited.clear();
        std::function<bool(const BasicBlock *)> returns=[&](const BasicBlock *block){
          if(!visited.insert(block).second)return false;
          for(auto *to:successors(block))if(to==site->getParent() || returns(to))return true;
          return false;
        };
        if(returns(site->getParent()))unimplemented("§6.5 cyclic static-file instance bound",3,site);
      }
      for (Instruction &i : instructions(f)) if (memoryRoots.count(&i)) {
        auto *r = &i;
        auto *call = dyn_cast<CallBase>(r);
        if (!call || call->getFunction() != &f) unimplemented("§6.5 interprocedural static-file environment",1,r);
        auto w = qwidth(a.get(r),r);
        files[r] = {fresh("qreg[" + std::to_string(w) + "]"), fresh("ptr"), unsigned(fileOrder.size()+1)};
        fileOrder.push_back(r);
      }
    }
    for (Argument &p : f.args()) {
      if(p.getType()->isAggregateType()) {
        std::vector<std::string> ns;unsigned k=0;
        for(auto &field:fields(p.getType())) {
          auto n="a"+std::to_string(p.getArgNo())+"_"+std::to_string(k++),t=fieldType(field.type);
          ns.push_back(n);params.push_back(n+":"+t);paramTypes.push_back(t);
        }
        tuples[&p]=ns;
      } else {
        auto n="a"+std::to_string(p.getArgNo()),t=type(&p);
        names[&p]=n;params.push_back(n+":"+t);paramTypes.push_back(t);
      }
    }
    if (!f.getReturnType()->isVoidTy()) {
      unsigned k=0;
      for(auto &field:fields(f.getReturnType())) {
        auto t=fieldType(field.type);
        results.push_back("result"+(f.getReturnType()->isAggregateType()?std::to_string(k++):"")+":"+t);
        resultTypes.push_back(t);
      }
    }
    unsigned bn = 0;
    for (BasicBlock &bb : f)
      blocks[&bb] = "b" + std::to_string(bn++);
    for (BasicBlock &bb : f)
      for (PHINode &p : bb.phis()) destinations(&p);
  }
  enum class CallFlow { Continue, EndBlock };
  CallFlow lowerCall(CallBase *c) {
    auto *g = resolve(c->getCalledOperand());
    if(!g && ccNames && !c->isInlineAsm()) {
      auto pointer=operand(c->getCalledOperand());auto pw=m.getDataLayout().getPointerSizeInBits();
      auto value=emit("i"+std::to_string(pw),"ptrtoint.i"+std::to_string(pw)+" "+pointer);
      std::map<uint64_t,Function *> candidates;std::vector<uint64_t> keys;
      for(auto *candidate:a.candidates(c->getCalledOperand(),c->getFunctionType()))
        if(ccNames->count(candidate) || (candidate->isDeclaration() && !candidate->isIntrinsic() && !markers().count(candidate->getName().str())))
          candidates[functionAddress(candidate)]=candidate;
      for(auto &candidate:candidates)keys.push_back(candidate.first);
      auto args=callArguments(*c);
      auto result=c->getType()->isVoidTy()?std::vector<std::string>{}:destinations(c);
      auto id=std::to_string(dispatchBlock++),done="call"+id+"done",bad="call"+id+"bad";
      compareTree(value,pw,keys,[&](uint64_t key) {
        if(candidates.at(key)->isDeclaration()) {unresolvedCall(candidates.at(key)->getName());return;}
        auto call="call @"+ccNames->at(candidates.at(key))+(args.values.empty()?"":" "+join(args.values," "));
        std::vector<std::string> values;
        if(!c->getType()->isVoidTy())for(auto &field:fields(c->getType()))values.push_back(fresh(fieldType(field.type)));
        rows.push_back((values.empty()?"":(values.size()==1?values[0]:"("+join(values)+")")+" = ")+call);
        rows.push_back("br ^"+done+"("+join(values)+")");
      },bad);
      rows.push_back("^"+bad+"():");rows.push_back("trap");
      std::vector<std::string> bindings;
      if(!result.empty()) {auto fs=fields(c->getType());for(unsigned k=0;k<result.size();++k)bindings.push_back(result[k]+":"+fieldType(fs[k].type));}
      rows.push_back("^"+done+"("+join(bindings)+"):");releaseCallArguments(args);propagateExit();usesCCCalls=true;return CallFlow::Continue;
    }
    if (!g)
      unimplemented("§17.4 indirect CC call", 1, c);
    auto n = g->getName();
    if (n.starts_with("llvm.lifetime.") ||
        (!memoryDescriptors && n.starts_with("llvm.memset.") &&
         descriptorObjects.count(
             getUnderlyingObject(c->getArgOperand(0)))))
      return CallFlow::Continue;
    if(rTier && n.starts_with("__bennett_effect_")) {
      auto suffix=n.drop_front(StringRef("__bennett_effect_").size());auto parts=suffix.split('_');
      effectModels.insert(parts.first.str());std::vector<std::string> args;
      for(auto &v:c->args())args.push_back(operand(v));
      rows.push_back("effect "+parts.first.str()+"."+parts.second.str()+" "+join(args," "));return CallFlow::Continue;
    }
    if (n == "__bennett_nz_fault") {
      if(auto *asmMD=c->getMetadata("bennett.asm")) {
        std::string block;unsigned ordinal=0;
        for(auto &row:rows)if(StringRef(row).starts_with("^")) {block=StringRef(row).drop_front().split('(').first.str();ordinal=0;}else ++ordinal;
        asmPoints.push_back(json::Object{{"symbol",ccNames->at(&f)},{"block",block},{"ordinal",ordinal},
          {"reason",cast<MDString>(asmMD->getOperand(0))->getString()}});
      }
      // Newly materialised allocator closures report the explicit code
      // through §11.5 before trapping. The payload is private storage,
      // not an extra logical heap allocation on a failing path.
      if (!rTier && f.hasFnAttribute("bennett.cc.allocator")) {
        reportedFault(c->getArgOperand(0));return CallFlow::EndBlock;
      }
      rows.push_back("trap"); return CallFlow::EndBlock;
    }
    if (n == "llvm.trap") { rows.push_back("trap"); return CallFlow::EndBlock; }
    if (n == "__bennett_qalloc" || n == "__bennett_qborrow") {
      auto w = integer(a.get(c->getArgOperand(1)), c);
      auto q = files.count(c) ? files.at(c).q : fresh("qreg[" + std::to_string(w) + "]");
      if (files.count(c)) {
        // No site is executed twice in this acyclic entry-local file.
        // Distinct nonzero identities are stable across stores and loads;
        // free retires the live tag before any later use can match it.
        auto tag = fresh("i" + std::to_string(m.getDataLayout().getPointerSizeInBits()));
        rows.push_back(tag + " = const.i" + std::to_string(m.getDataLayout().getPointerSizeInBits()) + " " + std::to_string(files.at(c).identity));
        names[c] = tag;
        rows.push_back("store.i" + std::to_string(m.getDataLayout().getPointerSizeInBits()) + " " + files.at(c).tag + " " + tag);
      } else names[c] = q;
      allocateRegister(*c, q, w);
    } else if (n == "__bennett_qfree")
      withHandle(c->getArgOperand(0), [&](std::string q) { rows.push_back("qreg.free " + q); }, true);
    else if (n == "__bennett_oracle")
      descriptor(*c);
    else if (n == "__bennett_inplace")
      inplace(*c);
    else if(n=="__bennett_ctrl" && controlledIdentity(*c)) {}
    else if (n == "__bennett_gate" || n == "__bennett_measure")
      gate(*c);
    else if(n=="__bennett_nz_alloc") {
      auto size=operand(c->getArgOperand(0));auto p=fresh("ptr");rows.push_back(p+" = alloc "+size);names[c]=p;recordAllocation(p,size);ccHeapBytes=table.capacities[1];
    } else if(n=="__bennett_nz_free") {
      auto p=operand(c->getArgOperand(0));auto bits=emit("i64","ptrtoint.i64 "+p);auto zero=number(0);auto isNull=emit("i1","icmp.eq "+bits+" "+zero);
      auto id=std::to_string(dispatchBlock++),live="free"+id,done=live+"done";rows.push_back("br "+isNull+" ^"+done+"() ^"+live+"()");rows.push_back("^"+live+"():");rows.push_back("free "+p);recordFree(p);rows.push_back("br ^"+done+"()");rows.push_back("^"+done+"():");
    } else if (ccNames && ccNames->count(g)) {
      usesCCCalls=true;
      // §14.1: LLVM fastcc/tail are source ABI/optimisation details.
      // ISA calls bind typed operands, keep a callee environment and
      // retain nested frames for LIFO reversal (§9.3 leaves CC dynamic).
      auto args=callArguments(*c);
      auto call="call @"+ccNames->at(g)+(args.values.empty()?"":" "+join(args.values," "));
      if(c->getType()->isVoidTy())rows.push_back(call);
      else {auto ns=destinations(c);rows.push_back((ns.size()==1?ns[0]:"("+join(ns)+")")+" = "+call);}
      releaseCallArguments(args);propagateExit();
    } else if(g->isDeclaration() && !g->isIntrinsic() && !markers().count(n.str()) &&
              !n.starts_with("__bennett_sf_") && !n.starts_with("__bennett_rt_")) {
      // A reached missing import is F(8). Continue naming the source
      // tail in an unreachable block so successor uses remain valid.
      if(!c->getType()->isVoidTy()) {
        auto ns=destinations(c);auto fs=fields(c->getType());
        for(unsigned k=0;k<ns.size();++k) {
          if(fs[k].type->isPointerTy())rows.push_back(ns[k]+" = inttoptr "+number(0));
          else rows.push_back(ns[k]+" = const.i"+std::to_string(width(fs[k].type))+" 0");
        }
      }
      unresolvedCall(n);
      rows.push_back("^missing" + std::to_string(dispatchBlock++) + "tail():");
      return CallFlow::Continue;
    } else
      unimplemented("§17.4 CC marker/call lowering", 1, c);
    return CallFlow::Continue;
  }
  void lower() {
    prepareLowering();
    auto edge = [&](BasicBlock *to, BasicBlock *from) {
      std::vector<std::string> values;
      for (PHINode &p : to->phis()) {auto vs=operands(p.getIncomingValueForBlock(from));values.insert(values.end(),vs.begin(),vs.end());}
      return "^" + blocks[to] + ("(" + join(values) + ")");
    };
    // LLVM block layout need not put a dominating definition before its use.
    // Keep existing emission order when it already meets that dependency.
    std::map<const BasicBlock *,unsigned> position;
    unsigned index=0;for(auto &bb:f)position[&bb]=index++;
    bool laterDefinition=false;
    for(auto &bb:f)for(auto &i:bb)if(!isa<PHINode>(i))for(auto &use:i.operands())
      if(auto *definition=dyn_cast<Instruction>(use.get()))
        laterDefinition|=position.at(definition->getParent())>position.at(&bb);
    std::vector<BasicBlock *> order;
    if(laterDefinition || f.hasFnAttribute("bennett.cc.allocator") || (ccNames && ccNames->size()>1)) {
      for(auto *bb:ReversePostOrderTraversal<Function *>(&f))order.push_back(bb);
      for(auto &bb:f)if(!is_contained(order,&bb))order.push_back(&bb);
    } else for(auto &bb:f)order.push_back(&bb);
    for (auto *block : order) {
      auto &bb=*block;
      std::vector<std::string> bindings;
      for (PHINode &p : bb.phis()) {
        auto ns=operands(&p);auto fs=fields(p.getType());
        for(unsigned k=0;k<ns.size();++k)bindings.push_back(ns[k]+":"+(p.getType()->isAggregateType()?fieldType(fs[k].type):type(&p)));
      }
      rows.push_back("^" + blocks[&bb] + "(" + join(bindings) + "):");
      ordinal = 0;
      if (&bb == &f.getEntryBlock()) for (auto *site : fileOrder) {
        auto zero = operand(ConstantInt::get(m.getDataLayout().getIntPtrType(m.getContext()),0));
        auto size = operand(ConstantInt::get(Type::getInt64Ty(m.getContext()),m.getDataLayout().getPointerSize()));
        auto p = files.at(site).tag; rows.push_back(p + " = alloc " + size); localMemory.push_back(p); allocatedBytes+=m.getDataLayout().getPointerSize();recordAllocation(p,size);
        rows.push_back("store.i" + std::to_string(m.getDataLayout().getPointerSizeInBits()) + " " + p + " " + zero);
      }
      for (Instruction &i : bb) {
        bool record = false;
        if (auto *g = dyn_cast<GetElementPtrInst>(&i))
          record = descriptorObjects.count(getUnderlyingObject(g));
        if (auto *s = dyn_cast<StoreInst>(&i))
          record = descriptorObjects.count(
              getUnderlyingObject(s->getPointerOperand()));
        if (auto *al = dyn_cast<AllocaInst>(&i))
          record = descriptorObjects.count(al);
        if ((!memoryDescriptors && record) || isa<PHINode>(i))
          continue;
        if(rTier && !isa<DbgInfoIntrinsic>(i)) {
          auto *call=dyn_cast<CallBase>(&i);auto *target=call?call->getCalledFunction():nullptr;
          if(!target || (!target->getName().starts_with("llvm.dbg.") && !target->getName().starts_with("llvm.lifetime.") && !target->getName().starts_with("__bennett_nz_rstep")))countRStep();
        }
        if (auto *c = dyn_cast<CallBase>(&i)) {
          if (lowerCall(c) == CallFlow::EndBlock) break;
        } else if(auto *insert=dyn_cast<InsertValueInst>(&i)) {
          auto vs=operands(insert->getAggregateOperand()),part=operands(insert->getInsertedValueOperand());
          auto fs=fields(insert->getType());unsigned k=0;
          for(unsigned j=0;j<fs.size();++j)if(ArrayRef<unsigned>(fs[j].path).take_front(insert->getNumIndices())==insert->getIndices())vs[j]=part.at(k++);
          tuples[insert]=vs;
        } else if(auto *extract=dyn_cast<ExtractValueInst>(&i)) {
          auto vs=operands(extract->getAggregateOperand());auto fs=fields(extract->getAggregateOperand()->getType());
          std::vector<std::string> out;
          for(unsigned j=0;j<fs.size();++j)if(ArrayRef<unsigned>(fs[j].path).take_front(extract->getNumIndices())==extract->getIndices())out.push_back(vs[j]);
          if(extract->getType()->isAggregateType())tuples[extract]=out;else names[extract]=out.at(0);
        } else if (auto *g = dyn_cast<GetElementPtrInst>(&i)) {
          names[g] = gep(cast<GEPOperator>(g));
        } else if (auto *al = dyn_cast<AllocaInst>(&i)) {
          auto n = m.getDataLayout().getTypeAllocSize(al->getAllocatedType()).getFixedValue();
          auto *count = dyn_cast<ConstantInt>(al->getArraySize());
          if (!count) unimplemented("§17.3 dynamic CC stack extent",1,al);
          auto bytes = operand(ConstantInt::get(Type::getInt64Ty(m.getContext()),n*count->getZExtValue()));
          auto p = fresh("ptr"); rows.push_back(p + " = alloc " + bytes); names[al] = p; localMemory.push_back(p); allocatedBytes+=std::max(uint64_t(1),n*count->getZExtValue());recordAllocation(p,bytes);
        } else if (auto *st = dyn_cast<StoreInst>(&i)) {
          if(st->getValueOperand()->getType()->isAggregateType()) {
            auto vs=operands(st->getValueOperand());auto p=operand(st->getPointerOperand());auto fs=fields(st->getValueOperand()->getType());
            for(unsigned k=0;k<fs.size();++k) {
              auto value=vs[k],address=fieldPointer(p,fs[k].offset),t="i"+std::to_string(width(fs[k].type));
              if(fs[k].type->isPointerTy())value=emit(t,"ptrtoint."+t+" "+value);
              sourceStore(address,value,width(fs[k].type));
            }
            continue;
          }
          auto value = operand(st->getValueOperand()), p = operand(st->getPointerOperand());
          auto w = st->getValueOperand()->getType()->isPointerTy() ? m.getDataLayout().getPointerSizeInBits() : width(st->getValueOperand()->getType());
          if (st->getValueOperand()->getType()->isPointerTy() && !tagged(a.get(st->getValueOperand()))) {
            auto d = fresh("i" + std::to_string(w)); rows.push_back(d + " = ptrtoint.i" + std::to_string(w) + " " + value); value = d;
          }
          sourceStore(p,value,w);
        } else if (auto *ld = dyn_cast<LoadInst>(&i)) {
          if(ld->getType()->isAggregateType()) {
            auto p=operand(ld->getPointerOperand());std::vector<std::string> ns;
            for(auto &field:fields(ld->getType())) {
              auto address=fieldPointer(p,field.offset),t="i"+std::to_string(width(field.type));
              auto n=sourceLoad(address,width(field.type));
              if(field.type->isPointerTy())n=emit("ptr","inttoptr "+n);
              ns.push_back(n);
            }
            tuples[ld]=ns;continue;
          }
          auto p = operand(ld->getPointerOperand());
          auto w = ld->getType()->isPointerTy() ? m.getDataLayout().getPointerSizeInBits() : width(ld->getType());
          auto value = sourceLoad(p,w);
          if (ld->getType()->isPointerTy() && !tagged(a.get(ld))) { auto d = fresh("ptr"); rows.push_back(d + " = inttoptr " + value); value=d; }
          names[ld] = value;
        } else if (auto *r = dyn_cast<ReturnInst>(&i)) {
          auto v = r->getReturnValue() ? join(operands(r->getReturnValue())," ") : "";
          for (auto &p : localMemory) rows.push_back("free " + p);
          rows.push_back("ret" + (v.empty() ? "" : " " + v));
        } else if (auto *br = dyn_cast<BranchInst>(&i)) {
          if (br->isUnconditional())
            rows.push_back("br " + edge(br->getSuccessor(0), &bb));
          else {
            auto p = operand(br->getCondition());
            auto yes = edge(br->getSuccessor(0), &bb), no = edge(br->getSuccessor(1), &bb);
            rows.push_back("br " + p + " " + yes + " " + no);
          }
        } else if (auto *sw = dyn_cast<SwitchInst>(&i)) {
          // §§14.8/16.4: unsigned sorted compare tree, not a jump table.
          // Capture original-predecessor phi arguments before creating any
          // synthetic block. ISA §3.4 transfers each tuple in parallel; this
          // also preserves duplicate destinations and loop-carried swaps.
          auto cond = operand(sw->getCondition());
          auto fallback = edge(sw->getDefaultDest(), &bb);
          std::vector<std::pair<APInt, std::string>> keys;
          for (auto c : sw->cases())
            keys.emplace_back(c.getCaseValue()->getValue(), edge(c.getCaseSuccessor(), &bb));
          llvm::sort(keys, [](auto &a, auto &b) { return a.first.ult(b.first); });
          std::vector<std::string> ids = {"^" + blocks[&bb] + "()"};
          std::vector<std::vector<std::string>> chunks(1);
          auto newBlock = [&]() {
            unsigned n = ids.size();
            ids.push_back("^" + blocks[&bb] + ".s" + std::to_string(n) + "()");
            chunks.emplace_back();
            return n;
          };
          std::function<void(int, int, unsigned)> tree = [&](int lo, int hi, unsigned cur) {
            auto begin = rows.size();
            auto save = [&]() {
              chunks[cur].insert(chunks[cur].end(), rows.begin() + begin, rows.end());
              rows.resize(begin);
            };
            if (hi < lo) {
              rows.push_back("br " + fallback);
            } else if (hi - lo + 1 <= 3) {
              for (int j = lo; j <= hi; ++j) {
                auto c = operand(ConstantInt::get(m.getContext(), keys[j].first));
                auto t = fresh("i1");
                rows.push_back(t + " = icmp.eq " + cond + " " + c);
                unsigned next = j < hi ? newBlock() : 0;
                rows.push_back("br " + t + " " + keys[j].second + " " + (j < hi ? ids[next] : fallback));
                save(); cur = next;
              }
              return;
            } else {
              int mid = (lo + hi) / 2;
              auto c = operand(ConstantInt::get(m.getContext(), keys[mid].first));
              auto t = fresh("i1");
              rows.push_back(t + " = icmp.ult " + cond + " " + c);
              unsigned l = newBlock(), r = newBlock();
              rows.push_back("br " + t + " " + ids[l] + " " + ids[r]);
              save();
              tree(lo, mid - 1, l); tree(mid, hi, r);
              return;
            }
            save();
          };
          tree(0, int(keys.size()) - 1, 0);
          // Text order follows creation order (L then R, then descendants).
          for (unsigned n = 0; n < chunks.size(); ++n) {
            if (n) rows.push_back(ids[n] + ":");
            rows.insert(rows.end(), chunks[n].begin(), chunks[n].end());
          }
        } else if (auto *b = dyn_cast<BinaryOperator>(&i)) {
          auto x = operand(b->getOperand(0)), y = operand(b->getOperand(1)),
               d = fresh("i" + std::to_string(width(b->getType())));
          names[b] = d;
          rows.push_back(d + " = " + b->getOpcodeName() + " " + x + " " + y);
        } else if (auto *sel = dyn_cast<SelectInst>(&i)) {
          if(sel->getType()->isAggregateType()) {
            auto p=operand(sel->getCondition());
            auto xs=operands(sel->getTrueValue()),ys=operands(sel->getFalseValue()),ns=destinations(sel);
            for(unsigned k=0;k<ns.size();++k)rows.push_back(ns[k]+" = select "+p+" "+xs[k]+" "+ys[k]);
            continue;
          }
          auto p = operand(sel->getCondition()),
               x = operand(sel->getTrueValue()),
               y = operand(sel->getFalseValue()),
               d = fresh(type(sel));
          if(sel->getType()->isPointerTy() && !tagged(a.get(sel))) {
            auto pw=m.getDataLayout().getPointerSizeInBits();
            auto xb=fresh("i"+std::to_string(pw)),yb=fresh("i"+std::to_string(pw)),bits=fresh("i"+std::to_string(pw));
            rows.push_back(xb+" = ptrtoint.i"+std::to_string(pw)+" "+x);rows.push_back(yb+" = ptrtoint.i"+std::to_string(pw)+" "+y);
            rows.push_back(bits+" = select "+p+" "+xb+" "+yb);rows.push_back(d+" = inttoptr "+bits);
          } else rows.push_back(d + " = select " + p + " " + x + " " + y);
          names[sel] = d;
        } else if (auto *cmp = dyn_cast<ICmpInst>(&i)) {
          auto pred = cmp->getPredicate();
          auto *xv = cmp->getOperand(0), *yv = cmp->getOperand(1);
          // §6.3: every allocation identity is nonzero, including stale copies.
          // A qreg is not an ISA pointer/integer operand of icmp. For an exact
          // non-null provenance this observation is independent of its value;
          // nullable unions still require their scalar generation tags.
          auto nonnullHandle = [&](Value *v) {
            auto av = a.get(v);
            return !av.top && !av.atoms.empty() &&
              llvm::all_of(av.atoms, [](const Atom &x) { return x.kind == Atom::Root; });
          };
          if ((pred == CmpInst::ICMP_EQ || pred == CmpInst::ICMP_NE) &&
              ((isa<ConstantPointerNull>(xv) && nonnullHandle(yv)) ||
               (isa<ConstantPointerNull>(yv) && nonnullHandle(xv)))) {
            names[cmp] = operand(ConstantInt::get(cmp->getType(), pred == CmpInst::ICMP_NE));
            continue;
          }
          if (pred == CmpInst::ICMP_UGT || pred == CmpInst::ICMP_UGE ||
              pred == CmpInst::ICMP_SGT || pred == CmpInst::ICMP_SGE) {
            pred = CmpInst::getSwappedPredicate(pred);
            std::swap(xv, yv);
          }
          auto x = operand(xv), y = operand(yv), d = fresh("i1");
          // Keep this pass local to the newly materialised numerical closure;
          // unrelated CC objects retain their recorded §17.4 lowering.
          if((rTier || f.hasFnAttribute("bennett.cc.softfloat") || f.hasFnAttribute("bennett.cc.softfloat.callee")) &&
             xv->getType()->isPointerTy() && !tagged(a.get(xv)) && !tagged(a.get(yv))) {
            auto t="i"+std::to_string(width(xv->getType()));
            x=emit(t,"ptrtoint."+t+" "+x);y=emit(t,"ptrtoint."+t+" "+y);
          }
          names[cmp] = d;
          rows.push_back(d + " = icmp." +
                         CmpInst::getPredicateName(pred).str() + " " + x + " " +
                         y);
        } else if (auto *cast = dyn_cast<CastInst>(&i); cast && (isa<PtrToIntInst>(cast) || isa<IntToPtrInst>(cast))) {
          auto x=operand(cast->getOperand(0));auto w=m.getDataLayout().getPointerSizeInBits();
          auto source=isa<PtrToIntInst>(cast)?w:width(cast->getOperand(0)->getType());
          auto target=isa<IntToPtrInst>(cast)?w:width(cast->getType());
          if(isa<PtrToIntInst>(cast)){auto n=fresh("i"+std::to_string(w));rows.push_back(n+" = ptrtoint.i"+std::to_string(w)+" "+x);x=n;}
          if(source!=target){auto n=fresh("i"+std::to_string(target));rows.push_back(n+std::string(source<target?" = zext.i":" = trunc.i")+std::to_string(target)+" "+x);x=n;}
          if(isa<IntToPtrInst>(cast)){auto n=fresh("ptr");rows.push_back(n+" = inttoptr "+x);x=n;}names[cast]=x;
        } else if(auto *c=dyn_cast<BitCastInst>(&i)) {
          names[c]=operand(c->getOperand(0));
        } else if (auto *c = dyn_cast<CastInst>(&i);
                   c && (isa<ZExtInst>(c) || isa<SExtInst>(c) ||
                         isa<TruncInst>(c))) {
          auto x = operand(c->getOperand(0)),
               d = fresh("i" + std::to_string(width(c->getType())));
          names[c] = d;
          rows.push_back(d + " = " + c->getOpcodeName() + ".i" +
                         std::to_string(width(c->getType())) + " " + x);
        } else if (isa<UnreachableInst>(i)) {
          rows.push_back("trap");
        } else
          unimplemented("§17.4 production CC instruction", 1, &i);
      }
    }
  }
};
// ISA envelopes are derived from generated functions and reference metadata.
// Keep the standalone reference object untouched for byte-exact comparison.
std::map<std::string,std::string> objectSections(StringRef object) {
  std::map<std::string,std::string> sections;
  auto pos=object.find("\n\nsection ");
  while(pos!=StringRef::npos) {
    auto start=pos+10,end=object.find('\n',start),next=object.find("\n\nsection ",end);
    sections[object.slice(start,end).str()]=object.slice(end+1,next).rtrim().str();pos=next;
  }
  return sections;
}
// Unified production layout. Standalone reference files retain their original
// images/layout/hash for independent published-object comparisons.
std::string linkReferences(Entry &e) {
  auto &dl=e.m.getDataLayout(); auto pw=dl.getPointerSizeInBits();
  std::string prefix="isa=0.8\nptr_width="+std::to_string(pw)+"\n";
  struct Symbol { std::string name,kind,body; json::Value sig; };
  std::vector<Symbol> functions;
  std::map<std::string,std::string> globalSymbols, data, dataSignatures;
  std::map<std::string,uint64_t> bases,sizes;
  std::set<std::string> used=e.ccGlobals;
  for (auto &names:e.referenceGlobals) for (auto &n:names) used.insert(n.second);
  // Include pointer relocation targets for every tier. A data image can name
  // another source global or a function even when no instruction loads it.
  std::set<const Value *> relocationVisited;
  std::function<void(const Value *)> relocation=[&](const Value *v) {
    if (!relocationVisited.insert(v).second) return;
    if (auto *g=dyn_cast<GlobalVariable>(v)) {
      used.insert(scalarGlobalKey(*g));e.ccGlobals.insert(scalarGlobalKey(*g));
      if (g->hasInitializer()) relocation(g->getInitializer());
      return;
    }
    if (auto *fn=dyn_cast<Function>(v)) {
      auto address=e.functionAddress(const_cast<Function *>(fn));
      const_cast<Function *>(fn)->setMetadata("bennett.address",MDNode::get(e.m.getContext(),
          ConstantAsMetadata::get(ConstantInt::get(dl.getIntPtrType(e.m.getContext()),address))));
      return;
    }
    if(auto *constant=dyn_cast<Constant>(v))for(auto &operand:constant->operands())relocation(operand);
  };
  for (auto &g:e.m.globals())if(used.count(scalarGlobalKey(g)))relocation(&g);
  if(e.argvService) {
    std::set<const Value *> visited;
    std::function<void(const Value *)> include=[&](const Value *v) {
      if(!visited.insert(v).second)return;
      if(auto *g=dyn_cast<GlobalVariable>(v)) {used.insert(scalarGlobalKey(*g));e.ccGlobals.insert(scalarGlobalKey(*g));if(g->hasInitializer())include(g->getInitializer());return;}
      if(isa<Function>(v))return;
      if(auto *constant=dyn_cast<Constant>(v))for(auto &operand:constant->operands())include(operand);
    };
    for(auto &g:e.m.globals())if(used.count(scalarGlobalKey(g)))include(&g);
    // The shared image and the indirect compare trees use the same addresses.
    for(auto &f:e.m) {
      if (hasComparisonLayout() && !comparisonFunctionAddress(f)) continue;
      auto address=e.functionAddress(&f);
      f.setMetadata("bennett.address",MDNode::get(e.m.getContext(),ConstantAsMetadata::get(ConstantInt::get(e.m.getDataLayout().getIntPtrType(e.m.getContext()),address))));
    }
  }
  uint64_t base=4096;
  for (auto &g:e.m.globals()) if (used.count(scalarGlobalKey(g))) {
    auto key=scalarGlobalKey(g),name="G"+std::to_string(globalSymbols.size()+1);
    globalSymbols[key]=name;base=alignTo(base,dl.getPreferredAlign(&g));bases[name]=comparisonGlobalAddress(g).value_or(base);
    sizes[name]=dl.getTypeAllocSize(g.getValueType()).getFixedValue();base=std::max(base,bases[name]+sizes[name]);
  }
  for(auto &key:used) if(!globalSymbols.count(key)) {
    // Model state materialised only in a scalar clone has the published i64
    // default image; its source name still identifies it across wrappers.
    if(!StringRef(key).starts_with("name:__bennett_dev_")) unimplemented("§19.5 unnamed unified global",1,&e.f);
    auto name="G"+std::to_string(globalSymbols.size()+1);globalSymbols[key]=name;
    if (hasComparisonLayout())fail("BD-E-COMPARISON-LAYOUT", "materialised model global missing from source module");
    base=alignTo(base,uint64_t(8));bases[name]=base;sizes[name]=8;base+=8;
  }
  std::map<const GlobalVariable *,uint64_t> sourceBases;
  for(auto &g:e.m.globals()) if(globalSymbols.count(scalarGlobalKey(g)))sourceBases[&g]=bases.at(globalSymbols.at(scalarGlobalKey(g)));
  json::Object globals,interfaces;
  // Function identities occupy their own address range before the standalone
  // heap. Include even unreferenced source data used to place those identities.
  if (!hasComparisonLayout() && !e.functionAddresses.empty())
    base = std::max(base, *e.functionAddresses.rbegin() + 1);
  uint64_t heap=comparisonHeapBase().value_or(alignTo(base,uint64_t(4096))),heapLimit=0,stack=0;
  std::vector<std::map<std::string,std::string>> parsed;
  for(auto &ref:e.references) {
    parsed.push_back(objectSections(ref));auto layout=parse(parsed.back().at("layout"));
    heapLimit=std::max(heapLimit,uint64_t(*layout.getAsObject()->getInteger("heap_limit_max")));
    stack=std::max(stack,uint64_t(*layout.getAsObject()->getInteger("S_cells")));
  }
  heapLimit=std::max(heapLimit,e.ccHeapBytes);
  if (parsed.empty()) heapLimit = std::max(heapLimit, e.table.capacities[1]);
  for (auto address : e.functionAddresses)
    if (address >= heap && address - heap < heapLimit)
      fail("BD-E-COMPARISON-LAYOUT", "function address overlaps the heap", &e.f);
  if(parsed.empty())while((uint64_t(1)<<stack)<std::max(uint64_t(e.stack),e.table.capacities[2]))++stack;
  uint64_t endAddress=heap+heapLimit,memCount=0;
  for(auto &g:e.m.globals())if(e.ccGlobals.count(scalarGlobalKey(g))) {
    auto name=globalSymbols.at(scalarGlobalKey(g)),image=scalarGlobalImage(g,sourceBases);
    data[name]=image;dataSignatures[name]="{\"abi\":\"0.8\",\"kind\":\"data\",\"size\":"+std::to_string(sizes.at(name))+",\"tier\":\"-\"}";
    globals[name]=json::Object{{"base",int64_t(bases.at(name))},{"size",int64_t(sizes.at(name))},{"image",name}};
    auto marker="CCADDRESS"+std::to_string(std::distance(e.m.global_begin(),g.getIterator()));
    for(auto &row:e.rows)row=std::regex_replace(row,std::regex(marker+"\\b"),std::to_string(bases.at(name)));
    for(auto &fn:e.ccFunctions)fn.second.second=std::regex_replace(fn.second.second,std::regex(marker+"\\b"),std::to_string(bases.at(name)));
  }
  for(unsigned i=0;i<parsed.size();++i) {
    auto &sec=parsed[i];auto syms=parse(sec.at("symbols"));auto suffix=i?std::to_string(i):"";
    std::map<std::string,std::string> rename;
    rename["ref"]="ref"+suffix;rename["L1"]=i?"L1_"+suffix:"L1";
    for(auto &v:*syms.getAsObject()) {auto *sym=v.second.getAsObject();auto n=sym->getString("name")->str();if(sym->getString("kind")=="lproc")rename[n]=i?n+"_"+suffix:n;}
    for(auto &g:e.referenceGlobals[i]) rename[g.first]=globalSymbols.at(g.second);
    auto replace=[&](std::string text) {
      std::string result;size_t last=0;std::regex refs(R"(@([A-Za-z_][A-Za-z_0-9]*))");
      for(std::sregex_iterator it(text.begin(),text.end(),refs),end;it!=end;++it) {
        auto name=(*it)[1].str();result+=text.substr(last,it->position()-last)+"@"+(rename.count(name)?rename.at(name):name);last=it->position()+it->length();
      }
      return result+text.substr(last);
    };
    auto body=sec.at("functions");
    for(auto &v:*syms.getAsObject()) {
      auto *sym=v.second.getAsObject();auto name=sym->getString("name")->str(),kind=sym->getString("kind")->str();
      if(kind=="data") {
        auto renamed=rename.at(name);auto bytes=StringRef(sec.at("data")).split(name+" ").second.split('\n').first.str();
        auto source=e.referenceGlobals[i].at(name);
        for(auto &g:e.m.globals()) if(scalarGlobalKey(g)==source) bytes=scalarGlobalImage(g,sourceBases);
        if(data.count(renamed) && data.at(renamed)!=bytes) fail("output","inconsistent shared global image",&e.f);
        data[renamed]=bytes;dataSignatures[renamed]=jcs(*sym->get("signature"));
        globals[renamed]=json::Object{{"base",int64_t(bases.at(renamed))},{"size",int64_t(sizes.at(renamed))},{"image",renamed}};
      } else {
        std::string marker=(kind=="oracle"?"oracle @":"lproc @")+name+" ";auto begin=body.find(marker);
        auto finish=body.find("\nlproc @",begin+1);
        auto text=StringRef(body).slice(begin,finish).rtrim().str();
        functions.push_back({rename.at(name),kind,replace(text),parse(jcs(*sym->get("signature")))});
        if(kind=="oracle") {
          json::Object regions;std::regex mem(R"(([A-Za-z_][A-Za-z_0-9]*):region\[([0-9]+),([0-9]+)\])");
          auto header=StringRef(text).split('\n').first.str();
          for(std::sregex_iterator it(header.begin(),header.end(),mem),end;it!=end;++it) {
            uint64_t size=(uint64_t(1)<<std::stoul((*it)[2]))*std::stoul((*it)[3])/8;
            endAddress=alignTo(endAddress,size);regions[(*it)[1].str()]=json::Object{{"base",int64_t(endAddress)}};endAddress+=size;++memCount;
          }
          interfaces[rename.at(name)]=std::move(regions);
        }
      }
    }
  }
  unsigned h=0,tab=0;
  while((uint64_t(1)<<h)<endAddress)++h;
  while((uint64_t(1)<<tab)<data.size()+memCount+heapLimit)++tab;
  if(e.automaticSnapshot) {
    // A_tab bounds one oracle's pre-entries, not the union of all oracle
    // interface maps. Keep the same static table capacity used to size S.
    uint64_t largest=0;for(auto &owner:interfaces)largest=std::max(largest,uint64_t(owner.second.getAsObject()->size()));
    if(data.size()+largest+heapLimit>(uint64_t(1)<<e.snapshotTableExponent))fail("output","snapshot allocation-table capacity underestimated",&e.f);
    tab=e.snapshotTableExponent;
  }
  json::Object layout{{"A_tab",tab},{"H",h},{"S_cells",int64_t(stack)},{"globals",std::move(globals)},
    {"heap_base",int64_t(heap)},{"heap_limit_max",int64_t(heapLimit)},{"interface_regions",std::move(interfaces)},{"null_size",4096},{"ptr_width",pw}};
  if(!e.diskDataKey.empty())layout["block_image"]=globalSymbols.at(e.diskDataKey);
  std::map<std::string,std::string> allLeaves;
  for(auto &v:layout) {
    if(v.first=="globals") for(auto &g:*v.second.getAsObject()) allLeaves["globals."+g.first.str()]=jcs(g.second);
    else if(v.first=="interface_regions") for(auto &o:*v.second.getAsObject()) for(auto &r:*o.second.getAsObject()) allLeaves["interface_regions."+o.first.str()+"."+r.first.str()]=jcs(r.second);
    else allLeaves[v.first.str()]=jcs(v.second);
  }
  // JSON Object iteration differs between LLVM majors. Definition order is
  // part of the full object bytes even when all interface hashes agree.
  std::sort(functions.begin(),functions.end(),[](const Symbol &a,const Symbol &b) { return a.name < b.name; });
  std::map<std::string,std::string> hashes;json::Object symbols;
  auto addSymbol=[&](std::string name,std::string kind,json::Value sig,std::string ih) {
    symbols[std::to_string(symbols.size())]=json::Object{{"name",name},{"kind",kind},{"signature",std::move(sig)},{"interface_hash",ih}};
  };
  for(auto &v:data) { hashes[v.first]=hash(prefix+dataSignatures.at(v.first)+"\n"+v.first+" "+v.second+"\n"); addSymbol(v.first,"data",parse(dataSignatures.at(v.first)),hashes.at(v.first)); }
  // Hash arbitrary linked closures, including recursive SCCs, after relocation.
  std::map<std::string,Symbol *> members;
  for(auto &f:functions)members[f.name]=&f;
  std::regex token(R"(@([A-Za-z_][A-Za-z_0-9]*))");
  std::map<std::string,std::set<std::string>> edges;
  for(auto &f:functions) {auto rest=f.body.substr(f.body.find('\n')+1);for(std::sregex_iterator it(rest.begin(),rest.end(),token),end;it!=end;++it)if(members.count((*it)[1]))edges[f.name].insert((*it)[1]);}
  auto reaches=[&](std::string from,std::string to) {std::set<std::string> seen;std::function<bool(std::string)> walk=[&](std::string n){if(n==to)return true;if(!seen.insert(n).second)return false;for(auto &v:edges[n])if(walk(v))return true;return false;};return walk(from);};
  std::function<void(std::string)> hashFunction=[&](std::string name) {
    if(hashes.count(name))return;
    std::vector<std::string> group;for(auto &v:members)if(reaches(name,v.first)&&reaches(v.first,name))group.push_back(v.first);
    std::set<std::string> inside(group.begin(),group.end());bool cyclic=group.size()>1 || edges[name].count(name);
    for(auto &n:group)for(auto &edge:edges[n])if(!inside.count(edge))hashFunction(edge);
    std::string envelopes;
    for(auto &n:group) {
      auto &f=*members.at(n);auto newline=f.body.find('\n');std::string canonical=f.body.substr(0,newline+1),refs;auto rest=f.body.substr(newline+1);
      std::set<std::string> referenced;size_t last=0;
      for(std::sregex_iterator it(rest.begin(),rest.end(),token),end;it!=end;++it) {
        auto v=(*it)[1].str();std::string replacement;
        if(cyclic && inside.count(v))replacement="$"+std::to_string(std::find(group.begin(),group.end(),v)-group.begin());
        else if(hashes.count(v)) {replacement=hashes.at(v);if(referenced.insert(v).second)refs+=replacement+"\n";}
        else {auto *owner=layout.getObject("interface_regions")->getObject(f.name);if(f.kind!="oracle" || !owner || !owner->get(v))fail("output","unresolved production symbol "+v,&e.f);replacement=v;}
        canonical+=rest.substr(last,it->position()-last)+"@"+replacement;last=it->position()+it->length();
      }
      canonical+=rest.substr(last);std::string images,leaves;
      for(auto &v:data)if(f.kind=="oracle" || referenced.count(v.first))images+="data "+v.first+" "+v.second+"\n";
      for(auto &v:allLeaves) {
        bool include=f.kind=="oracle" ? !StringRef(v.first).starts_with("interface_regions.") || StringRef(v.first).starts_with("interface_regions."+f.name+".") : false;
        if(f.kind=="lproc" && StringRef(v.first).starts_with("globals."))include=referenced.count(StringRef(v.first).drop_front(8).str());
        if(include)leaves+="layout "+v.first+" "+v.second+"\n";
      }
      envelopes+=prefix+jcs(f.sig)+"\n"+canonical+"\n"+images+leaves+refs;
    }
    auto digest=hash(envelopes);for(unsigned i=0;i<group.size();++i)hashes[group[i]]=cyclic?hash(digest+":"+std::to_string(i)):digest;
  };
  for(auto kind:{"lproc","oracle"})for(auto &f:functions)if(f.kind==kind)hashFunction(f.name);
  for(auto kind:{"lproc","oracle"})for(auto &f:functions)if(f.kind==kind)addSymbol(f.name,f.kind,parse(jcs(f.sig)),hashes.at(f.name));
  std::string object=e.reference.substr(0,e.reference.find("\n\nsection "))+"\n\nsection symbols\n"+jcs(json::Value(std::move(symbols)))+"\n\nsection functions\n";
  for(auto &f:functions)object+=f.body+"\n";
  if(!data.empty()) { object+="\nsection data\n";for(auto &v:data)object+=v.first+" "+v.second+"\n"; }
  object+="\nsection layout\n"+jcs(json::Value(std::move(layout)))+"\n";return object;
}
// Hash CC call SCCs only after the entire shared memory layout is fixed.
#include "CCCalls.inc"
std::string launchObject(Entry &e, json::Object &record,
                         json::Object &certificate) {
  std::map<std::string, std::string> sections;
  std::string ref = e.reference;
  bool unified = false;
  if (e.references.size()>1) {
    auto first=objectSections(ref);
    for (auto &r:e.references) {
      auto sec=objectSections(r); auto layout=parse(sec.at("layout")); bool mapped=false;
      for(auto &owner:*layout.getAsObject()->getObject("interface_regions")) if(!owner.second.getAsObject()->empty()) mapped=true;
      if(sec["layout"]!=first["layout"] || !e.referenceGlobals.front().empty() || mapped) unified=true;
    }
  }
  unified |= (e.ccHeapBytes>0 || !e.ccGlobals.empty() || !e.functionAddresses.empty()) && !e.references.empty();
  if(unified || (e.references.empty() && (!e.ccGlobals.empty() || !e.functionAddresses.empty()))) {
    ref=linkReferences(e);
    if(e.references.empty()) ref="bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 coverage=0.8 target=0.8 ptr_width="+
        std::to_string(e.m.getDataLayout().getPointerSizeInBits())+ref;
  }
  size_t pos = ref.find("\n\nsection ");
  std::string header =
      pos == std::string::npos
          ? "bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 "
            "coverage=0.8 target=0.8 ptr_width=" +
                std::to_string(e.m.getDataLayout().getPointerSizeInBits())
          : ref.substr(0, pos);
  while (pos != std::string::npos) {
    auto start = pos + 10, end = ref.find('\n', start),
         next = ref.find("\n\nsection ", end-1);
    sections[ref.substr(start, end - start)] =
        StringRef(ref.substr(end + 1,
                             next == std::string::npos ? next : (next > end ? next - end - 1 : 0)))
            .rtrim()
            .str();
    pos = next;
  }
  if(sections.count("functions") && sections["functions"].empty())sections.erase("functions");
  if (!sections.count("layout") && (!e.localMemory.empty() || e.ccHeapBytes || e.usesCCCalls || e.usesSourceMemory)) {
    uint64_t heap = std::max(e.table.capacities[1],e.ccHeapBytes); unsigned h = 0, tab = 0, sc = 0;
    while ((uint64_t(1)<<h) < 4096 + heap) ++h;
    while ((uint64_t(1)<<tab) < ((e.f.hasFnAttribute("bennett.cc.allocator") || e.usesCCCalls) ? heap : e.localMemory.size())) ++tab;
    while ((uint64_t(1)<<sc) < ((e.f.hasFnAttribute("bennett.cc.allocator") || e.usesCCCalls) ? std::max(uint64_t(e.stack),e.table.capacities[2]) : e.stack)) ++sc;
    sections["layout"] = jcs(json::Value(json::Object{{"A_tab",tab},{"H",h},{"S_cells",sc},
      {"globals",json::Object{}},{"heap_base",4096},{"heap_limit_max",int64_t(heap)},
      {"interface_regions",json::Object{}},{"null_size",4096},{"ptr_width",e.m.getDataLayout().getPointerSizeInBits()}}));
  }
  if(e.allocatorFaultService || e.argvService) {
    auto devices=sections.count("devices")?parse(sections["devices"]):json::Value(json::Object{{"models",json::Object{}},{"services",json::Object{}}});
    auto *services=devices.getAsObject()->getObject("services");
    if(!services) {(*devices.getAsObject())["services"]=json::Object{};services=devices.getAsObject()->getObject("services");}
    if(e.allocatorFaultService)(*services)["bennett.fault"]=json::Object{{"version","0.2.10"}};
    if(e.argvService)(*services)["bennett.argv"]=json::Object{{"version","0.2.10"}};
    if(e.argvService) {
      auto *models=devices.getAsObject()->getObject("models");
      for(auto &model:e.effectModels)(*models)[model]=json::Object{{"version","0.8"}};
      if(!e.diskDataKey.empty())(*models)["block"]=json::Object{{"version","0.8"}};
    }
    sections["devices"]=jcs(devices);
  }
  auto symbols = sections.count("symbols") ? parse(sections["symbols"])
                                           : json::Value(json::Object{});
  auto *so = symbols.getAsObject();
  std::string oracleHash;
  for (auto &s : *so)
    if (s.second.getAsObject()->getString("name") == "ref")
      oracleHash = s.second.getAsObject()->getString("interface_hash")->str();
  std::map<std::string, std::string> referenceHashes;
  referenceHashes["ref"] = oracleHash;
  if(unified) for(auto &s:*so) if(s.second.getAsObject()->getString("kind")=="oracle")
    referenceHashes[s.second.getAsObject()->getString("name")->str()]=s.second.getAsObject()->getString("interface_hash")->str();
  for (unsigned i = 1; !unified && i < e.references.size(); ++i) {
    std::map<std::string, std::string> extra;
    auto text = e.references[i];
    size_t p = text.find("\n\nsection ");
    while (p != std::string::npos) {
      auto start = p + 10, end = text.find('\n', start), next = text.find("\n\nsection ", end);
      extra[text.substr(start, end - start)] = StringRef(text.substr(end + 1, next == std::string::npos ? next : (next > end ? next - end - 1 : 0))).rtrim().str();
      p = next;
    }
    if (extra["layout"] != sections["layout"] || (extra.count("data") ? extra.at("data") : "") != (sections.count("data") ? sections.at("data") : ""))
      unimplemented("§16.3 multi-region unified layout", 1, &e.f);
    auto suffix = std::to_string(i);
    auto syms = parse(extra["symbols"]);
    for (auto &v : *syms.getAsObject()) {
      auto *sym = v.second.getAsObject();
      auto name = sym->getString("name")->str();
      if (name == "ref" || name == "L1") {
        auto renamed = name == "ref" ? "ref" + suffix : "L1_" + suffix;
        extra["functions"] = std::regex_replace(extra["functions"], std::regex("@" + name + "\\b"), "@" + renamed);
        // Definition names participate in the envelope; recompute both hashes.
        (*sym)["name"] = renamed;
      } else continue; // shared data was checked byte-identical above
    }
    // Rehash in dependency order, retaining the reference envelope's layout.
    std::map<std::string, std::string> changed;
    for (auto name : {"L1_" + suffix, "ref" + suffix}) {
      json::Object *sym = nullptr;
      for (auto &v : *syms.getAsObject())
        if (v.second.getAsObject()->getString("name") == name) sym = v.second.getAsObject();
      auto begin = extra["functions"].find(name[0] == 'L' ? "lproc @" + name : "oracle @" + name);
      auto end = extra["functions"].find("\nlproc @", begin + 1);
      auto body = extra["functions"].substr(begin, end == std::string::npos ? end : end - begin);
      // For memory-free lprocs only signatures/body/references enter; oracle
      // envelopes include all scalar layout leaves, as in lowerScalar.
      std::string env = "isa=0.8\nptr_width=" + std::to_string(e.m.getDataLayout().getPointerSizeInBits()) + "\n" + jcs(*sym->get("signature")) + "\n";
      std::string refs;
      for (auto &x : changed) {
        if (body.find("@" + x.first) != std::string::npos) refs += x.second + "\n";
        body = std::regex_replace(body, std::regex("@" + x.first + "\\b"), "@" + x.second);
      }
      env += body + "\n";
      if (name[0] != 'L') {
        auto layout = parse(extra["layout"]);
        std::map<std::string, std::string> leaves;
        for (auto &v : *layout.getAsObject()) {
          if (v.first == "globals" || v.first == "interface_regions") {
            if (v.first == "globals" && !v.second.getAsObject()->empty()) unimplemented("§16.3 multi-region data layout", 1, &e.f);
            if (v.first == "interface_regions") for (auto &r : *v.second.getAsObject())
              if (!r.second.getAsObject()->empty()) unimplemented("§16.3 multi-region interface layout", 1, &e.f);
          } else leaves[v.first.str()] = jcs(v.second);
        }
        for (auto &v : leaves) env += "layout " + v.first + " " + v.second + "\n";
      }
      changed[name] = hash(env + refs);
      (*sym)["interface_hash"] = changed[name];
      (*so)[std::to_string(so->size())] = parse(jcs(json::Value(std::move(*sym))));
    }
    referenceHashes["ref" + suffix] = changed["ref" + suffix];
    sections["functions"] += "\n" + extra["functions"];
  }
  json::Array pt, rt;
  for (auto &x : e.paramTypes)
    pt.push_back(x);
  for (auto &x : e.resultTypes)
    rt.push_back(x);
  json::Object sig{{"abi", "0.8"},
                   {"kind", "cc"},
                   {"params", std::move(pt)},
                   {"results", std::move(rt)},
                   {"tier", "cc"}};
  std::string body = "fn cc @" + e.f.getName().str() + " (" + join(e.params) +
                     ") (" + join(e.results) + ") () () ()\n";
  body += join(e.rows, "\n");
  std::map<std::string, std::string> hashes;
  hashes = referenceHashes;
  std::string actionBodies;
  for (auto &x : e.actions) {
    auto ah = hash("isa=0.8\nptr_width=" +
                   std::to_string(e.m.getDataLayout().getPointerSizeInBits()) +
                   "\n" + x.second.first + "\n" + x.second.second + "\n");
    hashes[x.first] = ah;
    (*so)[std::to_string(so->size())] =
        json::Object{{"interface_hash", ah},
                     {"kind", "action"},
                     {"name", x.first},
                     {"signature", parse(x.second.first)}};
    actionBodies += "\n" + x.second.second;
  }
  if(e.usesCCCalls)linkCCCalls(e,sections,sig,body,hashes,*so,actionBodies);
  std::function<void(std::string)> helper=[&](std::string name) {
    if(hashes.count(name))return;
    auto &item=e.snapshotFunctions.at(name);auto text=item.second;auto nl=text.find('\n');auto rest=text.substr(nl+1);std::string canonical=text.substr(0,nl+1),refs;size_t last=0;std::set<std::string> seen;
    std::regex token(R"(@([A-Za-z_][A-Za-z_0-9]*))");
    for(std::sregex_iterator it(rest.begin(),rest.end(),token),end;it!=end;++it) {auto n=(*it)[1].str();helper(n);canonical+=rest.substr(last,it->position()-last)+"@"+hashes.at(n);last=it->position()+it->length();if(seen.insert(n).second)refs+=hashes.at(n)+"\n";}
    canonical+=rest.substr(last);
    std::string memoryEnvelope;
    if(sections.count("layout")) {
      if(sections.count("data")){SmallVector<StringRef> lines;StringRef(sections["data"]).split(lines,'\n');for(auto line:lines)memoryEnvelope+="data "+line.str()+"\n";}
      auto layout=parse(sections["layout"]);std::map<std::string,std::string> leaves;
      for(auto &v:*layout.getAsObject()) {
        if(v.first=="globals")for(auto &g:*v.second.getAsObject())leaves["globals."+g.first.str()]=jcs(g.second);
        else if(v.first=="interface_regions" && name!="xor128") {for(auto &owner:*v.second.getAsObject())for(auto &region:*owner.second.getAsObject())leaves["interface_regions."+owner.first.str()+"."+region.first.str()]=jcs(region.second);}
        else if(v.first!="interface_regions")leaves[v.first.str()]=jcs(v.second);
      }
      for(auto &leaf:leaves)memoryEnvelope+="layout "+leaf.first+" "+leaf.second+"\n";
    }
    hashes[name]=hash("isa=0.8\nptr_width="+std::to_string(e.m.getDataLayout().getPointerSizeInBits())+"\n"+item.first+"\n"+canonical+"\n"+memoryEnvelope+refs);
    (*so)[std::to_string(so->size())]=json::Object{{"name",name},{"kind",name=="xor128"?"oracle":"cc"},{"signature",parse(item.first)},{"interface_hash",hashes.at(name)}};
    actionBodies+="\n"+text;
  };
  for(auto &item:e.snapshotFunctions)helper(item.first);
  std::string canonical, refs;
  std::set<std::string> referenced;
  std::regex token(R"(@(ref[0-9]*|M[0-9]+|B[0-9]+|U[0-9]+|xor128)\b)");
  size_t last = 0;
  for (std::sregex_iterator it(body.begin(), body.end(), token), end; it != end;
       ++it) {
    auto name = (*it)[1].str();
    canonical +=
        body.substr(last, it->position() - last) + "@" + hashes.at(name);
    last = it->position() + it->length();
    if (referenced.insert(name).second)
      refs += hashes.at(name) + "\n";
  }
  canonical += body.substr(last);
  std::map<std::string, std::string> leaves;
  if (sections.count("layout")) {
    auto layout = parse(sections["layout"]);
    for (auto &x : *layout.getAsObject()) {
      auto n = x.first.str();
      if (n == "globals" || n == "interface_regions") {
        for (auto &y : *x.second.getAsObject())
          if (n == "globals")
            leaves[n + "." + y.first.str()] = jcs(y.second);
          else
            for (auto &z : *y.second.getAsObject())
              leaves[n + "." + y.first.str() + "." + z.first.str()] =
                  jcs(z.second);
      } else
        leaves[n] = jcs(x.second);
    }
  }
  std::string envelope =
      "isa=0.8\nptr_width=" +
      std::to_string(e.m.getDataLayout().getPointerSizeInBits()) + "\n" +
      jcs(json::Value(std::move(sig))) + "\n" + canonical + "\n";
  auto signature = parse(StringRef(envelope)
                             .split('\n')
                             .second.split('\n')
                             .second.split('\n')
                             .first);
  if (sections.count("data")) {
    SmallVector<StringRef> lines;
    StringRef(sections["data"]).split(lines, '\n');
    for (auto l : lines)
      envelope += "data " + l.str() + "\n";
  }
  for (auto &x : leaves)
    envelope += "layout " + x.first + " " + x.second + "\n";
  if(e.allocatorFaultService) envelope += "device bennett.fault {\"version\":\"0.2.10\"}\n";
  envelope += refs;
  auto ih = e.usesCCCalls ? hashes.at(e.f.getName().str()) : hash(envelope);
  std::string block;
  unsigned ordinal = 0;
  for (auto &line : e.rows) {
    if (line[0] == '^') {
      block = line.substr(1, line.find('(') - 1);
      ordinal = 0;
      continue;
    }
    auto trapped=e.trappedCalls.find({e.f.getName().str(),block});
    bool missing=line=="trap" && trapped!=e.trappedCalls.end();
    e.coverage.push_back(
        json::Object{{"point", json::Array{ih, block, ordinal++}},
                     {"source", missing?"dialect-0.2.13:4.5":"dialect-0.2.13:17.4"},
                     {"classification", missing?"trapped":"lowered"},
                     {"reason", missing?trapped->second:"CC scalar/marker lowering"}});
  }
  (*so)[std::to_string(so->size())] =
      json::Object{{"interface_hash", ih},
                   {"kind", "cc"},
                   {"name", e.f.getName()},
                   {"signature", std::move(signature)}};
  std::string object =
      header + "\n\nsection symbols\n" + jcs(symbols) +
      "\n\nsection functions\n" + body +
      (sections.count("functions") ? "\n" + sections["functions"] : "") +
      actionBodies + "\n";
  for (auto name : {"data", "devices", "layout"})
    if (sections.count(name))
      object += "\nsection " + std::string(name) + "\n" + sections[name] + "\n";
  json::Array budgets;
  for (auto &b : e.budgets) {
    auto name = b.getString("region").value_or("ref").str();
    if (!b.get("selection_identity")) b["selection_identity"] = hashes.at(name);
    b["identity"] = hashes.at(name);
    budgets.push_back(std::move(b));
  }
  record["budgets"] = std::move(budgets);
  record["budget_table_sha256"] = record.get("budget_table") ? hash(jcs(*record.get("budget_table"))) : hash(jcs(*record.get("budgets")));
  record["layout"] = sections.count("layout") ? parse(sections["layout"])
                                              : json::Value(json::Object{});
  record["build_flags"] =
      json::Object{{"scalar_stack", e.stack},
                   {"launch_target", "environment:BENNETT_TARGET"}};
  record["runtimes_sha256"] = nullptr;
  record["arith_sha256"] = nullptr;
  record["asm_table_sha256"] = nullptr;
  record["snapshot_sha256"] = nullptr;
  record["cpuid"] = json::Object{};
  record["entry"] = e.f.getName();
  record["interface_hash"] = ih;
  record["object_hash"] = hash(object);
  certificate["bindings"] = json::Object{{"object_hash", hash(object)},
                                         {"interface_hash", ih},
                                         {"closure_hash", ih},
                                         {"reference_program_hash", oracleHash},
                                         {"dialect_mapping_version", "0.2.9"}};
  return object;
}
// Supplementary coverage preserves the existing CC coverage sidecar's bytes.
json::Object completeCoverage(StringRef object,
    const std::map<std::pair<std::string,std::string>,std::string> &trapped = {}) {
  auto symbols = parse(object.split("section symbols\n").second.split('\n').first);
  std::map<std::string, std::string> hashes;
  for (auto &v : *symbols.getAsObject()) {
    auto *sym = v.second.getAsObject();
    hashes[sym->getString("name")->str()] = sym->getString("interface_hash")->str();
  }
  json::Array entries;
  auto body = object.split("section functions\n").second.split("\n\nsection ").first;
  SmallVector<StringRef> lines; body.split(lines, '\n');
  std::string symbol, block, rule; unsigned ordinal = 0;
  for (auto line : lines) {
    if (line.starts_with("fn cc @") || line.starts_with("fn r @") || line.starts_with("oracle @") ||
        line.starts_with("lproc @") || line.starts_with("action @")) {
      symbol = line.split('@').second.split(' ').first.str();
      rule = line.starts_with("fn cc") ? "17.4" : line.starts_with("action") ? "18.3" : "16.4";
    } else if (line.starts_with("^")) {
      block = line.drop_front().split('(').first.str(); ordinal = 0;
    } else if (!line.empty() && !line.starts_with("regs ")) {
      auto missing=trapped.find({symbol,block});bool fault=line=="trap" && missing!=trapped.end();
      entries.push_back(json::Object{{"point", json::Array{hashes.at(symbol), block, ordinal++}},
        {"source", "dialect-0.2.13:" + (fault?std::string("4.5"):rule)}, {"classification", fault?"trapped":"lowered"},
        {"reason", fault?missing->second:"materialised scalar production instruction"}});
    }
  }
  return json::Object{{"entries", std::move(entries)}};
}
// Discover source state while every reachable entry still has its original body.
bool sharesGlobalState(Function &f) {
  std::set<const Value *> visited;
  bool sharedState = false;
  std::function<void(const Value *)> findState = [&](const Value *value) {
    if (!visited.insert(value).second) return;
    if (auto *function = dyn_cast<Function>(value)) {
      if (!function->isDeclaration())
        for (const auto &instruction : instructions(function)) findState(&instruction);
      return;
    }
    if (auto *global = dyn_cast<GlobalVariable>(value)) {
      sharedState |= !global->isConstant();
      if (global->hasInitializer()) findState(global->getInitializer());
      return;
    }
    if (auto *user = dyn_cast<User>(value))
      for (const auto &operand : user->operands()) findState(operand);
  };
  findState(&f);
  return sharedState;
}
// The host uses only the published launch 0.8 C ABI. BENNETT_TARGET supplies
// the target JSON at runtime; it is copied by bennett_load before launch.
void hostStub(Function &f, StringRef object, const json::Object &record, bool sharedState) {
  Module &m = *f.getParent();
  auto &ctx = m.getContext();
  auto *ptr = PointerType::get(ctx, 0);
  auto *i32 = Type::getInt32Ty(ctx), *i64 = Type::getInt64Ty(ctx);
  auto *size = m.getDataLayout().getIntPtrType(ctx);
  auto linkage = f.getLinkage();
  auto attrs = f.getAttributes();
  SmallVector<AttributeSet> paramAttrs;
  for (unsigned i = 0; i < f.arg_size(); ++i)
    paramAttrs.push_back(attrs.getParamAttrs(i));
  f.deleteBody();
  f.setLinkage(linkage);
  // The body now performs I/O through the launch library, but native parameter
  // and result attributes (signext/zeroext) still describe the caller's ABI.
  f.setAttributes(
      AttributeList::get(ctx, AttributeSet(), attrs.getRetAttrs(), paramAttrs));
  auto *entry = BasicBlock::Create(ctx, "launch", &f),
       *bad = BasicBlock::Create(ctx, "launch.failed", &f);
  IRBuilder<> b(entry);
  IRBuilder<> err(bad);
  if (sharedState) {
    // Maintainer-approved interim until the native-sharing contract publishes.
    auto message = "bennett: shared global state is promised and pending the native-sharing contract "
                   "(bp-acm; b-dialect-spec-6u6) for " + f.getName().str() + "\n";
    auto *text = b.CreateGlobalString(message);
    auto write = m.getOrInsertFunction("write", size, i32, ptr, size);
    b.CreateCall(write, {b.getInt32(2), text, ConstantInt::get(size, message.size())});
    auto exit = m.getOrInsertFunction("_Exit", b.getVoidTy(), i32);
    b.CreateCall(exit, {b.getInt32(125)});
    b.CreateUnreachable();
    err.CreateUnreachable();
    return;
  }
  auto intrinsic = [&](Intrinsic::ID id,
                       ArrayRef<Type *> types = ArrayRef<Type *>()) {
#if LLVM_VERSION_MAJOR >= 23
    return Intrinsic::getOrInsertDeclaration(&m, id, types);
#else
    return Intrinsic::getDeclaration(&m, id, types);
#endif
  };
  auto string = [&](StringRef s, StringRef name = "") {
    return b.CreateGlobalString(s, name);
  };
  err.CreateCall(intrinsic(Intrinsic::trap));
  err.CreateUnreachable();
  auto api = [&](StringRef n, Type *ret, ArrayRef<Type *> types) {
    return m.getOrInsertFunction(n, FunctionType::get(ret, types, false));
  };
  auto status = [&](Value *v) {
    auto *ok = BasicBlock::Create(ctx, "launch.ok", &f);
    b.CreateCondBr(b.CreateICmpEQ(v, b.getInt32(0)), ok, bad);
    b.SetInsertPoint(ok);
  };
  auto require = [&](Value *v) {
    auto *ok = BasicBlock::Create(ctx, "launch.valid", &f);
    b.CreateCondBr(v, ok, bad);
    b.SetInsertPoint(ok);
  };
  auto slot = [&](Type *t) { return b.CreateAlloca(t); };
  auto launchByteOrder = [&](Value *value) -> Value * {
    auto bits=cast<IntegerType>(value->getType())->getBitWidth();
    if(m.getDataLayout().isLittleEndian() || bits<=8)return value;
    // llvm.bswap requires an even number of bytes; launch carriers such as
    // i24 still have a well-defined byte encoding.
    Value *result=ConstantInt::get(value->getType(),0);
    for(unsigned k=0;k<bits/8;++k) {
      auto *byte=b.CreateAnd(b.CreateLShr(value,k*8),ConstantInt::get(value->getType(),255));
      result=b.CreateOr(result,b.CreateShl(byte,bits-8-k*8));
    }
    return result;
  };
  struct NativeField { Type *type; SmallVector<unsigned> path; };
  auto fields = [&](Type *type) {
    std::vector<NativeField> result;
    std::function<void(Type *,SmallVector<unsigned>)> visit=[&](Type *t,SmallVector<unsigned> path) {
      if(t->isAggregateType()) {
        auto count=t->isStructTy()?t->getStructNumElements():t->getArrayNumElements();
        for(unsigned k=0;k<count;++k) {
          auto nested=path;nested.push_back(k);
          visit(t->isStructTy()?t->getStructElementType(k):t->getArrayElementType(),nested);
        }
      } else result.push_back({t,path});
    };
    visit(type,{});return result;
  };
  auto symbols=parse(object.split("section symbols\n").second.split('\n').first);
  const json::Object *signature=nullptr;
  for(auto &symbol:*symbols.getAsObject())if(symbol.second.getAsObject()->getString("name")==f.getName())
    signature=symbol.second.getAsObject()->getObject("signature");
  if(!signature)fail("output","missing native launch signature",&f);
  std::vector<Value *> arguments;
  if(record.getString("mode")!="reversible")for(auto &arg:f.args())
    for(auto &field:fields(arg.getType()))arguments.push_back(field.path.empty()?&arg:b.CreateExtractValue(&arg,field.path));
  auto *program = slot(ptr), *args = slot(ptr), *run = slot(i64),
       *result = slot(ptr), *request = slot(ptr);
  auto *target =
      b.CreateCall(api("getenv", ptr, {ptr}), {string("BENNETT_TARGET")});
  require(b.CreateIsNotNull(target));
  auto *targetSize = b.CreateCall(api("strlen", size, {ptr}), {target});
  status(b.CreateCall(api("bennett_load", i32, {ptr, size, ptr, size, ptr}),
                      {string(object, "bennett.object"),
                       ConstantInt::get(size, object.size()), target,
                       targetSize, program}));
  auto *p = b.CreateLoad(ptr, program);
  auto *bs = record.getArray("budgets");
  status(
      b.CreateCall(api("bennett_args_new", i32, {size, ptr}),
                   {ConstantInt::get(size, arguments.size() + bs->size()), args}));
  auto *av = b.CreateLoad(ptr, args);
  unsigned index = 0;
  for (auto *arg : arguments) {
    auto isaType=(*signature->getArray("params"))[index].getAsString().value();
    auto *type=arg->getType();
    if(isaType.starts_with("qreg[")) {
      Value *id=type->isPointerTy()?b.CreatePtrToInt(arg,i64):b.CreateZExtOrTrunc(arg,i64);
      status(b.CreateCall(api("bennett_args_set_qreg",i32,{ptr,size,i64}),
        {av,ConstantInt::get(size,index++),id}));continue;
    }
    auto w = type->isPointerTy()?m.getDataLayout().getPointerTypeSizeInBits(type):
      type->isIntegerTy()?type->getIntegerBitWidth():unsigned(type->getPrimitiveSizeInBits());
    auto bytes = (w + 7) / 8;
    auto *bits=IntegerType::get(ctx,w);
    Value *value=type->isPointerTy()?b.CreatePtrToInt(arg,bits):
      type->isIntegerTy()?arg:b.CreateBitCast(arg,bits);
    auto *storage = slot(IntegerType::get(ctx, bytes * 8));
    value = b.CreateZExtOrTrunc(value, IntegerType::get(ctx, bytes * 8));
    // Launch integers are little endian even on a big endian host.
    value=launchByteOrder(value);
    b.CreateStore(value, storage);
    status(b.CreateCall(
        api("bennett_args_set_int", i32, {ptr, size, i32, ptr}),
        {av, ConstantInt::get(size, index++), b.getInt32(w), storage}));
  }
  for (auto &bv : *bs) {
    auto *budget = bv.getAsObject();
    auto *tk = slot(i64);
    auto number = [&](StringRef name) {
      uint64_t n;
      if (budget->getString(name)->getAsInteger(10, n))
        fail("output", "invalid resolved budget");
      return b.getInt64(n);
    };
    status(b.CreateCall(
        api("bennett_budget", i32, {ptr, ptr, i64, i64, i64, i64, ptr}),
        {p, string(budget->getString("region").value_or("ref")), number("steps"), number("heap"), number("stack"),
         number("depth"), tk}));
    status(b.CreateCall(
        api("bennett_args_set_token", i32, {ptr, size, i64}),
        {av, ConstantInt::get(size, index++), b.CreateLoad(i64, tk)}));
  }
  status(
      b.CreateCall(api("bennett_run", i32, {ptr, ptr, ptr, ptr, size, ptr}),
                   {p, string(f.getName()), av, ConstantPointerNull::get(ptr),
                    ConstantInt::get(size, 0), run}));
  b.CreateCall(api("bennett_args_free", b.getVoidTy(), {ptr}), {av});
  auto *id = b.CreateLoad(i64, run);
  status(b.CreateCall(api("bennett_wait", i32, {ptr, i64, ptr, ptr}),
                      {p, id, result, request}));
  if(record.getString("mode")=="reversible") {
    // §19.2's one launch request. Entries needing argv/envp byte storage
    // require explicit byte marshalling, rather than passing host pointers.
    auto *req=b.CreateLoad(ptr,request);require(b.CreateIsNotNull(req));
    auto *service=b.CreateCall(api("bennett_request_service",ptr,{ptr}),{req});
    auto *same=b.CreateCall(api("strcmp",i32,{ptr,ptr}),{service,string("bennett.argv")});require(b.CreateICmpEQ(same,b.getInt32(0)));
    auto *replyType=ArrayType::get(b.getInt8Ty(),4+2*m.getDataLayout().getPointerSize());auto *reply=slot(replyType);
    b.CreateStore(ConstantAggregateZero::get(replyType),reply);
    Value *argc=f.arg_empty()?(Value *)b.getInt32(0):f.getArg(0);
    if(!m.getDataLayout().isLittleEndian())argc=b.CreateCall(intrinsic(Intrinsic::bswap,{i32}),{argc});
    b.CreateStore(argc,reply);
    status(b.CreateCall(api("bennett_reply",i32,{ptr,i64,ptr,size}),{p,id,reply,ConstantInt::get(size,replyType->getNumElements())}));
    b.CreateCall(api("bennett_request_free",b.getVoidTy(),{ptr}),{req});
    status(b.CreateCall(api("bennett_wait",i32,{ptr,i64,ptr,ptr}),{p,id,result,request}));
  }
  require(b.CreateIsNull(b.CreateLoad(ptr, request)));
  auto *res = b.CreateLoad(ptr, result);
  require(b.CreateIsNotNull(res));
  require(b.CreateICmpEQ(
      b.CreateCall(api("bennett_result_nfaults", size, {ptr}), {res}),
      ConstantInt::get(size, 0)));
  Value *ret = nullptr;
  if (!f.getReturnType()->isVoidTy()) {
    if(f.getReturnType()->isAggregateType())ret=Constant::getNullValue(f.getReturnType());
    unsigned index=0;
    for(auto &field:fields(f.getReturnType())) {
    auto *kind = slot(i32), *width = slot(i32);
    auto isaType=(*signature->getArray("results"))[index].getAsString().value();
    auto *type=field.type;
    auto w=isaType.starts_with("qreg[")?64u:type->isPointerTy()?m.getDataLayout().getPointerTypeSizeInBits(type):
      type->isIntegerTy()?type->getIntegerBitWidth():unsigned(type->getPrimitiveSizeInBits());
    auto bytes=(w+7)/8;
    auto *carrier = IntegerType::get(ctx, bytes * 8);
    auto *storage = slot(carrier);
    status(b.CreateCall(
        api("bennett_result_get", i32, {ptr, size, ptr, ptr, ptr, size}),
        {res, ConstantInt::get(size, index++), kind, width, storage,
         ConstantInt::get(size, bytes)}));
    require(b.CreateICmpEQ(b.CreateLoad(i32, kind), b.getInt32(isaType.starts_with("qreg[")?2:0)));
    require(b.CreateICmpEQ(b.CreateLoad(i32, width), b.getInt32(w)));
    Value *value = b.CreateLoad(carrier, storage);
    value=launchByteOrder(value);
    auto bits=type->isPointerTy()?m.getDataLayout().getPointerTypeSizeInBits(type):
      type->isIntegerTy()?type->getIntegerBitWidth():unsigned(type->getPrimitiveSizeInBits());
    value=b.CreateZExtOrTrunc(value,IntegerType::get(ctx,bits));
    value=type->isPointerTy()?b.CreateIntToPtr(value,type):type->isIntegerTy()?value:b.CreateBitCast(value,type);
    ret=field.path.empty()?value:b.CreateInsertValue(ret,value,field.path);
    }
  }
  status(b.CreateCall(api("bennett_run_close", i32, {ptr, i64}), {p, id}));
  b.CreateCall(api("bennett_result_free", b.getVoidTy(), {ptr}), {res});
  status(b.CreateCall(api("bennett_unload", i32, {ptr}), {p}));
  if (ret)
    b.CreateRet(ret);
  else
    b.CreateRetVoid();
}

} // namespace
// Freeze all dependencies before the first host body is replaced.
void replaceHostEntries(ArrayRef<Function *> entries, StringRef out) {
  std::map<Function *, bool> sharedState;
  for (auto *entry : entries) sharedState.emplace(entry, sharesGlobalState(*entry));
  for(auto *entry:entries) {
    auto dir=out.str()+"/"+entry->getName().str();auto build=parse(read(dir+"/build.json"));
    hostStub(*entry,read(dir+"/launch.bennett"),*build.getAsObject(),sharedState.at(entry));
  }
}
#include "Reversible.inc"
bool specialiseRegisterWidths(Module &m, Analysis &a) {
  // Finite source widths become distinct static roots before register-file
  // construction. Unbounded widths retain the explicit BLK-1 obligation.
  std::vector<std::pair<CallInst *,std::vector<uint64_t>>> allocations;
  for(auto &f:m)if(a.tiers[&f].count("CC"))for(auto &i:instructions(f))
    if(auto *c=dyn_cast<CallInst>(&i);c && c->getCalledFunction() &&
       (c->getCalledFunction()->getName()=="__bennett_qalloc" || c->getCalledFunction()->getName()=="__bennett_qborrow") && !isa<ConstantInt>(c->getArgOperand(1))) {
      auto v=a.get(c->getArgOperand(1));std::vector<uint64_t> widths;
      if(v.top)unimplemented("§25.1 BLK-1 dynamic widths",3,c);
      for(auto &x:v.atoms)if(x.kind==Atom::Int)widths.push_back(x.integer.getLimitedValue());
      std::sort(widths.begin(),widths.end());widths.erase(std::unique(widths.begin(),widths.end()),widths.end());allocations.push_back({c,widths});
    }
  if(!allocations.empty()) {
    for(auto &site:allocations) {
      auto *c=site.first;auto *head=c->getParent();auto *fn=head->getParent();
      auto *done=head->splitBasicBlock(c->getIterator(),"width.done");head->getTerminator()->eraseFromParent();
      auto *phi=PHINode::Create(c->getType(),site.second.size(),"width.handle",&done->front());
      auto *bad=BasicBlock::Create(m.getContext(),"width.bad",fn,done);IRBuilder<> failBuilder(bad);
      failBuilder.CreateCall(
#if LLVM_VERSION_MAJOR >= 23
        Intrinsic::getOrInsertDeclaration(&m,Intrinsic::trap)
#else
        Intrinsic::getDeclaration(&m,Intrinsic::trap)
#endif
      );failBuilder.CreateUnreachable();
      std::function<void(BasicBlock *,unsigned,unsigned)> tree=[&](BasicBlock *block,unsigned lo,unsigned hi) {
        IRBuilder<> b(block);if(lo==hi){b.CreateBr(bad);return;}
        auto mid=(lo+hi)/2;auto *key=ConstantInt::get(c->getArgOperand(1)->getType(),site.second[mid]);
        auto *leaf=BasicBlock::Create(m.getContext(),"width.leaf",fn,done),*rest=BasicBlock::Create(m.getContext(),"width.rest",fn,done);
        b.CreateCondBr(b.CreateICmpEQ(c->getArgOperand(1),key),leaf,rest);
        IRBuilder<> lb(leaf);auto *allocation=cast<CallInst>(c->clone());allocation->setName("width.static");allocation->setArgOperand(1,key);lb.Insert(allocation);lb.CreateBr(done);phi->addIncoming(allocation,leaf);
        IRBuilder<> rb(rest);auto *left=BasicBlock::Create(m.getContext(),"width.left",fn,done),*right=BasicBlock::Create(m.getContext(),"width.right",fn,done);
        rb.CreateCondBr(rb.CreateICmpULT(c->getArgOperand(1),key),left,right);tree(left,lo,mid);tree(right,mid+1,hi);
      };tree(head,0,site.second.size());c->replaceAllUsesWith(phi);c->eraseFromParent();
    }
    return true;
  }

  return false;
}
BudgetTable productionBudget(Module &m, Analysis &a, StringRef budgetDefault, StringRef budgetFile) {
  SmallVector<StringRef> components;
  budgetDefault.split(components, ',');
  std::vector<uint64_t> defaults;
  for (auto c : components) {
    uint64_t n;
    if (c.getAsInteger(10, n))
      fail("input", "§9.2 invalid budget default");
    defaults.push_back(n);
  }
  if (defaults.size() != 5)
    fail("input", "§9.2 budget default needs five components");
  BudgetTable table(defaults, budgetFile);
  {
    auto *u64 = Type::getInt64Ty(m.getContext());
    for (Function &f : m) for (Instruction &i : instructions(f))
      if (auto *c = dyn_cast<CallBase>(&i); c && c->getCalledFunction() &&
          (c->getCalledFunction()->getName() == "__bennett_oracle" || c->getCalledFunction()->getName() == "__bennett_inplace") &&
          !isa<ConstantPointerNull>(c->getArgOperand(c->getCalledFunction()->getName()=="__bennett_inplace"?2:1)))
        for (unsigned j = 0; j < 4; ++j) {
          auto v = a.readAt(*c, c->getArgOperand(c->getCalledFunction()->getName()=="__bennett_inplace"?2:1), 8*j, u64);
          if (!v.top) for (auto &atom : v.atoms)
            if (atom.kind == Atom::Int && !atom.integer.isAllOnes())
              table.capacities[j] = std::max(table.capacities[j], atom.integer.getLimitedValue());
        }
  }
  return table;
}
void lowerProduction(Module &m, Analysis &a, StringRef out, unsigned stack,
                     StringRef budgetDefault, StringRef budgetFile) {
  if (specialiseRegisterWidths(m, a)) {
    Analysis specialised(m);specialised.run();
    lowerProduction(m,specialised,out,stack,budgetDefault,budgetFile);return;
  }
  auto table = productionBudget(m, a, budgetDefault, budgetFile);
  // CC arithmetic uses the same linked definitions as L and native comparison.
  // Keep recursive numerical closures as §14.1 CC calls; acyclic closures
  // retain their established inlining and object identities.
  bool preparedFP=false;
  for(auto &fn:m)if(!fn.isDeclaration() && a.tiers[&fn].count("CC") && !fn.hasFnAttribute("bennett.cc.softfloat")) {
    bool needed=false;
    for(auto &i:instructions(fn)) {
      needed|=isa<FCmpInst>(i) || (isa<BinaryOperator>(i) && i.getType()->isFloatingPointTy());
      if(auto *c=dyn_cast<CastInst>(&i))needed|=c->getOpcode()==Instruction::SIToFP||c->getOpcode()==Instruction::UIToFP||c->getOpcode()==Instruction::FPToSI||c->getOpcode()==Instruction::FPToUI||c->getOpcode()==Instruction::FPExt||c->getOpcode()==Instruction::FPTrunc;
      if(auto *c=dyn_cast<CallBase>(&i))if(auto *g=c->getCalledFunction())needed|=g->getName().starts_with("__bennett_sf_") || (g->isIntrinsic() && c->getType()->isFloatingPointTy());
    }
    if(!needed)continue;
    a.releaseTransferGraphs();
    fn.addFnAttr("bennett.cc.softfloat");preparedFP=true;normaliseScalar(fn);materialiseFPBits(fn);
    // A back edge is a real call frame, never an inlining refusal.
    bool recursive=false;
    std::set<Function *> active,done;
    std::function<void(Function *)> check=[&](Function *f) {
      requireSoftFloat(*f);if(f->isDeclaration() || done.count(f))return;
      if(!active.insert(f).second) {recursive=true;return;}
      normaliseScalar(*f);materialiseFPBits(*f);
      for(auto &i:instructions(f))if(auto *c=dyn_cast<CallBase>(&i))if(auto *g=c->getCalledFunction();g && !markers().count(g->getName().str()))check(g);
      active.erase(f);done.insert(f);
    };
    for(auto &i:instructions(fn))if(auto *c=dyn_cast<CallBase>(&i))if(auto *g=c->getCalledFunction();g && g->getName().starts_with("__bennett_sf_"))check(g);
    if(recursive) {
      for(auto *g:done)g->addFnAttr("bennett.cc.softfloat.callee");
      auto *entry=normaliseWideABI(m,&fn);
      for(auto &g:m)if(!g.isDeclaration()) {normaliseScalar(g);materialiseFPBits(g);}
      for(auto &g:m)if(!g.use_empty())materialiseIntegerRuntime(g);
      prepareStack(m,*entry,table.capacities[4]);
      if(auto *init=m.getFunction("__bennett_rt_ss_init");init && !init->isDeclaration()) {
        IRBuilder<> b(&*entry->getEntryBlock().getFirstInsertionPt());b.CreateCall(init,{b.getInt64(table.capacities[4])});
      }
      for(auto &g:m)if(!g.isDeclaration()) {normaliseScalar(g);materialiseFPBits(g);}
      // N22/N27 and N24 introduce additional linked runtime definitions.
      // All reachable helpers execute in this entry, including externally
      // named slot helpers; their H bodies must not become launch stubs.
      std::set<Function *> closure;
      std::function<void(Function *)> retain=[&](Function *g) {
        if(g->isDeclaration() || !closure.insert(g).second)return;
        if(g!=entry)g->addFnAttr("bennett.cc.softfloat.callee");
        for(auto &i:instructions(g))if(auto *c=dyn_cast<CallBase>(&i))
          if(auto *target=resolve(c->getCalledOperand()))retain(target);
      };retain(entry);
      Analysis prepared(m);prepared.run();lowerProduction(m,prepared,out,stack,budgetDefault,budgetFile);return;
    }
    while(true) {
      CallBase *site=nullptr;
      for(auto &i:instructions(fn))if(auto *c=dyn_cast<CallBase>(&i);c && c->getCalledFunction() && done.count(c->getCalledFunction())) {site=c;break;}
      if(!site)break;InlineFunctionInfo info;
      if(!InlineFunction(*site,info).isSuccess())fail("output","§13.1 CC helper inlining failed",site);
    }
  }
  if(preparedFP) {Analysis prepared(m);prepared.run();lowerProduction(m,prepared,out,stack,budgetDefault,budgetFile);return;}
  bool preparedCaller=false;
  std::vector<Function *> callers;
  for(auto &fn:m)if(!fn.isDeclaration() && a.tiers[&fn].count("CC"))callers.push_back(&fn);
  for(auto *fn:callers) {
    Entry probe{m,a,*fn,"",stack,table};if(!probe.wantsSnapshot() || fn->hasFnAttribute("bennett.cc.snapshot"))continue;
    fn->addFnAttr("bennett.cc.snapshot");preparedCaller=true;
    for(auto &i:instructions(fn))if(auto *c=dyn_cast<CallBase>(&i);c && c->getCalledFunction() && c->getCalledFunction()->getName()=="__bennett_oracle")
      if(auto *al=dyn_cast<AllocaInst>(getUnderlyingObject(c->getArgOperand(2))))al->setMetadata("bennett.cc.descriptor",MDNode::get(m.getContext(),{}));
    prepareStack(m,*fn,table.capacities[4]);
    if(auto *init=m.getFunction("__bennett_rt_ss_init");init && !init->isDeclaration()) {IRBuilder<> b(&*fn->getEntryBlock().getFirstInsertionPt());b.CreateCall(init,{b.getInt64(table.capacities[4])});}
    // Materialised classical helpers use this same CC allocator and memory.
    // Inline acyclic calls before the ordinary SSA/CFG lowering, including
    // logical-stack bookkeeping. Marker calls stay as launch operations.
    while(true) {
      CallBase *site=nullptr;
      for(auto &i:instructions(fn))if(auto *c=dyn_cast<CallBase>(&i);c && c->getCalledFunction() && !c->getCalledFunction()->isDeclaration() && !markers().count(c->getCalledFunction()->getName().str())) {site=c;break;}
      if(!site)break;
      if(site->getCalledFunction()==fn)break;
      InlineFunctionInfo info;if(!InlineFunction(*site,info).isSuccess())fail("output","caller snapshot helper inlining failed",site);
    }
    normaliseScalar(*fn);
  }
  if(preparedCaller) {Analysis prepared(m);prepared.run();lowerProduction(m,prepared,out,stack,budgetDefault,budgetFile);return;}
  // §19.1/§17.4: follow linked allocator bodies, never substitute libc
  // summaries. Normalise before inlining (notably calloc's N27 overflow
  // arithmetic and N26 memset), then retain every primitive and byte access.
  bool preparedAllocator=false;
  for(auto *fn:callers) {
    auto allocator=[](StringRef n) {return n=="malloc" || n=="calloc" || n=="free" || n=="memset";};
    bool needed=false;
    for(auto &i:instructions(*fn))if(auto *c=dyn_cast<CallBase>(&i))if(auto *g=resolve(c->getCalledOperand()))needed|=allocator(g->getName());
    if(!needed || fn->hasFnAttribute("bennett.cc.allocator"))continue;
    fn->addFnAttr("bennett.cc.allocator");preparedAllocator=true;
    normaliseScalar(*fn);
    std::set<Function *> active,done;
    std::function<void(Function *)> visit=[&](Function *g) {
      materialiseIntegerRuntime(*g);
      if(g->isDeclaration() || markers().count(g->getName().str()) || done.count(g))return;
      if(!active.insert(g).second)unimplemented("§17.4 recursive CC allocator closure",2,g);
      normaliseScalar(*g);
      for(auto &i:instructions(*g))if(auto *c=dyn_cast<CallBase>(&i))if(auto *target=resolve(c->getCalledOperand()))visit(target);
      active.erase(g);done.insert(g);
    };
    // Only calls in the allocator closure are expanded in this pass.
    for(auto &i:instructions(*fn))if(auto *c=dyn_cast<CallBase>(&i))if(auto *g=resolve(c->getCalledOperand());g && (allocator(g->getName()) || g->getName()=="__bennett_rt_memset"))visit(g);
    while(true) {
      CallBase *site=nullptr;
      for(auto &i:instructions(*fn))if(auto *c=dyn_cast<CallBase>(&i))if(auto *g=resolve(c->getCalledOperand());g && done.count(g)) {site=c;break;}
      if(!site)break;
      InlineFunctionInfo info;if(!InlineFunction(*site,info).isSuccess())fail("output","§17.4 allocator closure inlining failed",site);
    }
    // N27 produces field shells for the overflow result. Project those SSA
    // fields without running an optimiser that could erase heap history.
    SmallVector<Instruction *> fields;
    for(auto &i:instructions(*fn))if(isa<ExtractValueInst>(i))fields.push_back(&i);
    for(auto *i:fields)if(auto *v=simplifyInstruction(i,SimplifyQuery(m.getDataLayout()))) {i->replaceAllUsesWith(v);i->eraseFromParent();}
    bool dead=true;while(dead) {
      dead=false;SmallVector<Instruction *> shells;
      for(auto &i:instructions(*fn))if(isa<InsertValueInst>(i) && i.use_empty())shells.push_back(&i);
      for(auto *i:shells) {i->eraseFromParent();dead=true;}
    }
  }
  if(preparedAllocator) {Analysis prepared(m);prepared.run();lowerProduction(m,prepared,out,stack,budgetDefault,budgetFile);return;}
  if (auto ec = sys::fs::create_directories(out)) fail("output", ec.message());
  ValueToValueMapTy vm;
  auto device = CloneModule(m, vm);
  std::vector<Function *> entries;
  for (Function &f : m)
    if (!f.isDeclaration() && a.tiers[&f].count("CC")) {
      // Internal direct-only callees execute in their caller's launch and
      // memory. Keep their H body; no host launch ABI is crossed here.
      if(f.hasFnAttribute("bennett.cc.softfloat.callee") || f.hasFnAttribute("bennett.stack.internal"))continue;
      bool internal=f.hasLocalLinkage();
      for(auto *u:f.users()) {
        auto *c=dyn_cast<CallBase>(u);
        internal &= c && c->getCalledOperand()==&f && a.tiers[c->getFunction()].count("CC");
      }
      for(auto &i:instructions(f))if(auto *c=dyn_cast<CallBase>(&i))
        if(auto *g=resolve(c->getCalledOperand());g && markers().count(g->getName().str()))internal=false;
      if(!internal)entries.push_back(&f);
    }
  json::Array launches;
  for (Function *f : entries) {
    std::string dir = out.str() + "/" + f->getName().str();
    if (auto ec = sys::fs::create_directories(dir))
      fail("output", ec.message());
    Entry e{m, a, *f, dir, stack, table};
    std::map<Function *,std::string> ccNames;
    ccNames[f]=f->getName().str();
    std::vector<Function *> closure{f};
    auto include = [&](Function *g) {
      if (g && !g->isDeclaration() && !markers().count(g->getName().str()) && !ccNames.count(g)) {
        auto name="C"+std::to_string(closure.size()-1);
        if(name==f->getName())name+="callee";
        ccNames[g]=name;closure.push_back(g);
      }
    };
    for(unsigned k=0;k<closure.size();++k)for(auto &i:instructions(*closure[k]))
      if(auto *c=dyn_cast<CallBase>(&i)) {
        if(auto *g=resolve(c->getCalledOperand())) include(g);
        else {
          auto candidates=a.candidates(c->getCalledOperand(),c->getFunctionType());
          for(auto &g:m)if(candidates.count(&g))include(&g);
        }
      }
    e.ccNames=&ccNames;
    e.lower();
    for(unsigned k=1;k<closure.size();++k) {
      Entry callee{m,a,*closure[k],dir,stack,table};callee.ccNames=&ccNames;
      // One object owns the memory, references and action namespace, while
      // each CC body has its own SSA registers and block parameters.
      callee.actions=e.actions;callee.references=e.references;callee.reference=e.reference;
      callee.referenceGlobals=e.referenceGlobals;callee.snapshotFunctions=e.snapshotFunctions;
      callee.budgets=std::move(e.budgets);
      callee.lower();
      e.actions=std::move(callee.actions);e.references=std::move(callee.references);e.reference=std::move(callee.reference);
      e.referenceGlobals=std::move(callee.referenceGlobals);e.snapshotFunctions=std::move(callee.snapshotFunctions);
      e.budgets=std::move(callee.budgets);
      e.ccGlobals.insert(callee.ccGlobals.begin(),callee.ccGlobals.end());
      e.functionAddresses.insert(callee.functionAddresses.begin(),callee.functionAddresses.end());
      e.trappedCalls.insert(callee.trappedCalls.begin(),callee.trappedCalls.end());
      for(auto &proof:callee.controlledIdentities)e.controlledIdentities.push_back(std::move(proof));
      e.usesSourceMemory|=callee.usesSourceMemory;
      e.ccHeapBytes=std::max(e.ccHeapBytes,callee.ccHeapBytes);e.allocatedBytes+=callee.allocatedBytes;
      e.allocatorFaultService|=callee.allocatorFaultService;
      json::Array pt,rt;for(auto &t:callee.paramTypes)pt.push_back(t);for(auto &t:callee.resultTypes)rt.push_back(t);
      auto sig=jcs(json::Value(json::Object{{"abi","0.8"},{"kind","cc"},{"params",std::move(pt)},{"results",std::move(rt)},{"tier","cc"}}));
      auto name=ccNames.at(closure[k]);
      e.ccFunctions[name]={sig,"fn cc @"+name+" ("+join(callee.params)+") ("+join(callee.results)+") () () ()\n"+join(callee.rows,"\n")};
    }
    if(e.automaticSnapshot)e.ccHeapBytes=e.table.capacities[1];
    else if(e.memoryDescriptors || e.generalUsed)e.ccHeapBytes=e.allocatedBytes;
    json::Object record{{"dialect", "0.2.13"},
                        {"isa", "0.8"},
                        {"llvm_version", LLVM_VERSION_STRING},
                        {"pipeline", "bennett"},
                        {"shape", e.shape}};
    if(auto *id=dyn_cast_or_null<MDString>(m.getModuleFlag("bennett.arith.bitcode.sha256")))record["arith_bitcode_sha256"]=id->getString();
    if (table.enabled) {
      json::Object resolved{{"version", "0.2"}, {"defaults", tuple(table.defaults)},
        {"capacities", tuple(table.capacities)}, {"shapes", std::move(e.resolvedShapes)},
        {"input", parse(jcs(table.document))}};
      auto resolvedText = jcs(json::Value(std::move(resolved)));
      record["resolved_table_sha256"] = hash(resolvedText);
      record["budget_table"] = parse(resolvedText);
    }
    json::Object cert{
        {"versions", json::Object{{"isa", "0.8"}, {"cert", "0.8"}}},
        {"regions", json::Object{}},
        {"composition",
         json::Object{{"multiplicities", json::Object{}},
                      {"epsilon_total", json::Object{{"diamond", 0}}},
                      {"method", "sum_over_multiplicities"}}}};
    auto obj = launchObject(e, record, cert);
    if(!e.controlledIdentities.empty())record["controlled_identity_proofs"]=std::move(e.controlledIdentities);
    write(dir + "/launch.bennett", obj);
    auto allCoverage=completeCoverage(obj,e.trappedCalls);
    std::set<std::string> covered;
    for(auto &row:e.coverage)covered.insert(jcs(*row.getAsObject()->get("point")));
    for(auto &row:*allCoverage.getArray("entries"))if(row.getAsObject()->getString("classification")=="trapped")
      if(covered.insert(jcs(*row.getAsObject()->get("point"))).second)e.coverage.push_back(parse(jcs(row)));
    write(dir + "/all-coverage.json", jcs(json::Value(std::move(allCoverage))) + "\n");
    auto build = jcs(json::Value(std::move(record)));

    write(dir + "/build.json", build + "\n");
    cert["producer"] = json::Object{
        {"name", "bennett-plugin"},
        {"version", "0.2.13+build." + hash(build)},
        {"materialisation", json::Object{{"llvm_version", LLVM_VERSION_STRING},
                                         {"pipeline", "bennett"},
                                         {"normaliser_version", "0.2.8"}}}};
    write(dir + "/certificate.json", jcs(json::Value(std::move(cert))) + "\n");
    write(dir + "/coverage.json",
          jcs(json::Value(json::Object{{"entries", std::move(e.coverage)}})) +
              "\n");
    write(dir + "/blockers.json", "[]\n");
    launches.push_back(
        json::Object{{"entry", f->getName()},
                     {"object", f->getName().str() + "/launch.bennett"},
                     {"build_sha256", hash(build)}});
  }
  // Snapshot analysis of every entry sees the linked source memory, before
  // native stubs add embedded objects and launch-API string globals.
  a.releaseTransferGraphs();
  replaceHostEntries(entries, out);
  normaliseWideABI(*device);
  for (Function &f : *device)
    if (!f.isDeclaration() && a.tiers[m.getFunction(f.getName())].count("L"))
      normaliseScalar(f);
  std::error_code ec;
  raw_fd_ostream bc(out.str() + "/device.bc", ec);
  if (ec)
    fail("output", ec.message());
  checkComparisonMaterialisation(*device);
  WriteBitcodeToFile(*device, bc);
  for(auto &f:m)if(!f.isDeclaration() && (a.tiers[&f].count("CC") || a.tiers[&f].count("R") || a.tiers[&f].count("L")))normaliseFP(f);
  for(auto &f:m)for(auto &i:instructions(f))if(auto *c=dyn_cast<CallBase>(&i))if(auto *g=c->getCalledFunction())requireSoftFloat(*g);
  raw_fd_ostream host(out.str() + "/host.bc", ec);
  if (ec)
    fail("output", ec.message());
  WriteBitcodeToFile(m, host);
  write(out.str() + "/launches.json",
        jcs(json::Value(std::move(launches))) + "\n");
  bc.close(); host.close();
  // Hash only closed, final artifacts. The record is not included in its own
  // inventory, and never upgrades metadata to a checked executable claim.
  for (Function *f : entries) {
    std::string dir = f->getName().str();
    json::Object artifacts;
    auto add = [&](const std::string &path) {
      auto bytes = read(out.str() + "/" + path);
      artifacts[path] = json::Object{{"bytes", int64_t(bytes.size())}, {"sha256", hash(bytes)}};
    };
    for (auto file : {"host.bc", "device.bc", "launches.json"}) add(file);
    for (auto file : {"launch.bennett", "build.json", "certificate.json", "coverage.json", "all-coverage.json", "blockers.json"}) add(dir + "/" + file);
    if(sys::fs::exists(out.str()+"/"+dir+"/inplace-evidence.json")) add(dir+"/inplace-evidence.json");
    for (unsigned i = 0;; ++i) {
      auto path = dir + "/oracle-" + std::to_string(i) + "/ref.bennett";
      if (!sys::fs::exists(out.str() + "/" + path)) break;
      add(path);
    }
    auto build = parse(read(out.str() + "/" + dir + "/build.json"));
    json::Object record{{"schema", "bennett-plugin-launch-record-1"},
      {"entry", dir}, {"object_hash", *build.getAsObject()->getString("object_hash")},
      {"artifacts", std::move(artifacts)}, {"certificate_acceptance", "metadata_only"},
      {"target_source", "runtime:BENNETT_TARGET"},
      {"checked_executable_claims", false}, {"linked_runtime_acceptance", false},
      {"required_acceptance", json::Array{"target/schedule-bound checked executable claims", "real linked launch-library execution"}}};
    if (hasComparisonLayout()) record["comparison_layout_sha256"] = comparisonLayoutDigest();
    write(out.str() + "/" + dir + "/launch-record.json", jcs(json::Value(std::move(record))) + "\n");
  }

}
} // namespace bennett
````

## `src/Reversible.inc` (153 lines)

````
// §15.2 rows without an IR replacement trap only when reached.
static void normaliseRAsm(Function &f, json::Array &coverage) {
  SmallVector<CallInst *> sites;
  for(auto &i:instructions(f))if(auto *c=dyn_cast<CallInst>(&i);c && c->isInlineAsm())sites.push_back(c);
  for(auto *c:sites) {
    auto *assembly=cast<InlineAsm>(c->getCalledOperand());
    auto text=std::regex_replace(StringRef(assembly->getAsmString()).str(),std::regex("[;\\s]+")," ");text=StringRef(text).trim().str();
    bool erased=c->getType()->isVoidTy() && (text.empty() || text=="pause" || text=="nop");
    coverage.push_back(json::Object{{"function",f.getName()},{"asm",text},{"constraints",assembly->getConstraintString()},
      {"source","dialect-0.2.13:N31"},{"classification",erased?"lowered":"trapped"},{"reason",erased?"§15.2 barrier/no-op":"§15.2 unlisted asm row: F(8)"}});
    if(!erased) {
      IRBuilder<> b(c);auto fault=f.getParent()->getOrInsertFunction("__bennett_nz_fault",b.getVoidTy(),b.getInt64Ty());
      auto *trap=b.CreateCall(fault,{b.getInt64(8)});
      trap->setMetadata("bennett.asm",MDNode::get(f.getContext(),MDString::get(f.getContext(),"§15.2 asm "+text+" constraints "+StringRef(assembly->getConstraintString()).str())));
      if(!c->getType()->isVoidTy())c->replaceAllUsesWith(Constant::getNullValue(c->getType()));
    }
    c->eraseFromParent();
  }
}
// §19.2 whole-program mode uses the same scalar ABI and memory linker as CC.
// R bodies differ in effects, history, mandatory counters and exit propagation.
void lowerReversible(Module &source, Analysis &sourceAnalysis, Function &sourceEntry,
                     StringRef out, unsigned stack, StringRef budgetDefault,
                     StringRef budgetFile, StringRef disk) {
  sourceAnalysis.releaseTransferGraphs();
  auto device=CloneModule(source);auto &m=*device;
  auto entryName=sourceEntry.getName().str();auto *root=m.getFunction(entryName);
  for(auto &arg:root->args())if(arg.getArgNo()>0 && !arg.use_empty())
    unimplemented("§19.2 argv/envp byte storage in R launch",4,&arg);
  SmallVector<StringRef> components;budgetDefault.split(components,',');
  std::vector<uint64_t> defaults;
  for(auto c:components) {uint64_t n;if(c.getAsInteger(10,n))fail("input","§9.2 budget default");defaults.push_back(n);}
  if(defaults.size()!=5)fail("input","§9.2 budget default needs five components");
  BudgetTable table(defaults,budgetFile);auto limits=table.baseline(*root);
  // Each R instruction reads and consumes the shared source-step counter.
  auto *steps=new GlobalVariable(m,Type::getInt64Ty(m.getContext()),false,
      GlobalValue::InternalLinkage,ConstantInt::get(Type::getInt64Ty(m.getContext()),0),"__bennett_rt_rsteps");
  root->setName(entryName+".R");
  auto *launch=Function::Create(FunctionType::get(Type::getInt32Ty(m.getContext()),false),
      GlobalValue::ExternalLinkage,entryName,m);
  IRBuilder<> builder(BasicBlock::Create(m.getContext(),"launch",launch));builder.CreateRet(builder.getInt32(0));
  // The published runtime supplies logical frames; no native allocator is used.
  prepareStack(m,*root,table.capacities[4]);
  materialiseStackRuntime(m,table.capacities[4]);
  auto *init=m.getFunction("__bennett_rt_ss_init");
  json::Array asmCoverage;
  std::vector<Function *> closure{root,init};std::set<Function *> seen;
  std::set<Value *> addresses;
  std::function<void(Value *)> address=[&](Value *v) {
    if(!addresses.insert(v).second)return;
    if(auto *f=resolve(v);f && !f->isDeclaration()) {if(!seen.count(f))closure.push_back(f);return;}
    if(auto *g=dyn_cast<GlobalVariable>(v)) {if(g->hasInitializer())address(g->getInitializer());return;}
    if(auto *constant=dyn_cast<Constant>(v))for(auto &operand:constant->operands())address(operand);
  };
  for(unsigned k=0;k<closure.size();++k) {
    auto *f=closure[k];if(!f || !seen.insert(f).second)continue;
    normaliseScalar(*f);materialiseFPBits(*f);normaliseRAsm(*f,asmCoverage);
    for(auto &i:instructions(*f))if(auto *call=dyn_cast<IntrinsicInst>(&i);call && call->getType()->isVectorTy())
      unimplemented("§12 N21/N27 vector intrinsic lane materialisation",2,call);
    for(auto &i:instructions(*f))for(auto &v:i.operands())address(v);
    for(auto &i:instructions(*f))if(auto *c=dyn_cast<CallBase>(&i)) {
      auto *g=resolve(c->getCalledOperand());
      if(g) {materialiseIntegerRuntime(*g);materialiseMemoryRuntime(*g);if(!g->isDeclaration() && !markers().count(g->getName().str()) && !seen.count(g))closure.push_back(g);}
    }
  }
  closure.assign(seen.begin(),seen.end());
  // Stable source order, independent of heap addresses and LLVM major.
  closure.clear();for(auto &f:m)if(seen.count(&f))closure.push_back(&f);
  Analysis a(m,root,true);a.run();a.checkHandles();a.checkRegions();
  std::error_code ec;if((ec=sys::fs::create_directories(out)))fail("output",ec.message());
  std::string dir=out.str()+"/"+entryName;if((ec=sys::fs::create_directories(dir)))fail("output",ec.message());
  Entry e{m,a,*launch,dir,stack,table};e.argvService=true;e.usesCCCalls=true;e.ccHeapBytes=table.capacities[1];
  if(!disk.empty()) {
    e.diskImage=read(disk);auto *image=ConstantDataArray::getString(m.getContext(),e.diskImage,false);
    auto *global=new GlobalVariable(m,image->getType(),true,GlobalValue::InternalLinkage,image,"__bennett_rt_disk_image");
    e.diskDataKey=scalarGlobalKey(*global);e.ccGlobals.insert(e.diskDataKey);
  }
  std::map<Function *,std::string> names;unsigned ordinal=0;
  for(auto *f:closure)names[f]="R"+std::to_string(ordinal++);
  e.ccNames=&names;
  auto *argv=new GlobalVariable(m,ArrayType::get(builder.getInt8Ty(),4+2*m.getDataLayout().getPointerSize()),false,
      GlobalValue::InternalLinkage,ConstantAggregateZero::get(ArrayType::get(builder.getInt8Ty(),4+2*m.getDataLayout().getPointerSize())),"__bennett_rt_argv");
  auto *eh=m.getGlobalVariable("__bennett_rt_eh",true);
  for(auto *f:closure) {
    Entry callee{m,a,*f,dir,stack,table};callee.ccNames=&names;callee.rTier=f!=init;
    callee.rSteps=steps;callee.rEH=eh;callee.lower();
    e.ccGlobals.insert(callee.ccGlobals.begin(),callee.ccGlobals.end());
    for(auto &point:callee.asmPoints)e.asmPoints.push_back(std::move(point));
    e.effectModels.insert(callee.effectModels.begin(),callee.effectModels.end());
    e.ccHeapBytes=std::max(e.ccHeapBytes,callee.ccHeapBytes);
    json::Array pt,rt;for(auto &t:callee.paramTypes)pt.push_back(t);for(auto &t:callee.resultTypes)rt.push_back(t);
    auto tier=callee.rTier?"r":"cc";
    auto sig=jcs(json::Value(json::Object{{"abi","0.8"},{"kind",tier},{"tier",tier},{"params",std::move(pt)},{"results",std::move(rt)}}));
    e.ccFunctions[names.at(f)]={sig,"fn "+std::string(tier)+" @"+names.at(f)+" ("+join(callee.params)+") ("+join(callee.results)+") () () ()\n"+join(callee.rows,"\n")};
  }
  e.rows={"^entry():"};
  // argv service reply: little-endian (argc:i32, argv:P, envp:P), packed.
  // The host populates the pointed-to argument storage in device memory.
  auto argp=e.operand(argv),length=e.number(4+2*m.getDataLayout().getPointerSize());
  e.emit("i64","hostcall bennett.argv "+argp+" "+length);
  e.rows.push_back("call @"+names.at(init)+" "+e.number(table.capacities[4]));
  auto stepP=e.operand(steps),limit=e.number(limits[0]);e.rows.push_back("store.i64 "+stepP+" "+limit);
  std::vector<std::string> args;
  if(root->arg_size()) {
    if(root->arg_size()!=2 && root->arg_size()!=3)fail("input","§19.2 entry needs main ABI",root);
    args.push_back(e.emit("i32","load.i32 "+argp));
    auto pw=std::to_string(m.getDataLayout().getPointerSizeInBits());
    for(unsigned k=1;k<root->arg_size();++k)args.push_back(e.emit("ptr","inttoptr "+e.emit("i"+pw,"load.i"+pw+" "+e.fieldPointer(argp,4+(k-1)*m.getDataLayout().getPointerSize()))));
  }
  if(!root->getReturnType()->isIntegerTy(32))fail("input","§19.2 entry status must be i32",root);
  auto status=e.emit("i32","call @"+names.at(root)+(args.empty()?"":" "+join(args," ")));
  if(eh) {
    auto p=e.operand(eh),active=e.emit("i32","load.i32 "+p),four=e.operand(builder.getInt32(4));
    auto exiting=e.emit("i1","icmp.eq "+active+" "+four);
    auto selector=e.emit("i32","load.i32 "+e.fieldPointer(p,4));status=e.emit("i32","select "+exiting+" "+selector+" "+status);
  }
  e.rows.push_back("ret "+status);e.resultTypes={"i32"};e.results={"status:i32"};
  json::Object record{{"dialect","0.2.13"},{"isa","0.8"},{"llvm_version",LLVM_VERSION_STRING},{"pipeline","bennett"},
    {"mode","reversible"},{"verdict","blocked:BD-B-ISA7"},{"source_step_limit",std::to_string(limits[0])},{"asm_rows",std::move(asmCoverage)}};
  record["entry_initialisation"] = json::Object{{"shadow_stack_bytes",std::to_string(table.capacities[4])}};
  json::Object cert{{"versions",json::Object{{"isa","0.8"},{"cert","0.8"}}},{"regions",json::Object{}},
    {"composition",json::Object{{"multiplicities",json::Object{}},{"epsilon_total",json::Object{{"diamond",0}}},{"method","sum_over_multiplicities"}}}};
  auto object=launchObject(e,record,cert);write(dir+"/launch.bennett",object);
  auto build=jcs(json::Value(std::move(record)));write(dir+"/build.json",build+"\n");
  cert["producer"]=json::Object{{"name","bennett-plugin"},{"version","0.2.13+build."+hash(build)},
    {"materialisation",json::Object{{"llvm_version",LLVM_VERSION_STRING},{"pipeline","bennett"},{"normaliser_version","0.2.8"}}}};
  write(dir+"/certificate.json",jcs(json::Value(std::move(cert)))+"\n");
  auto report=completeCoverage(object);auto sections=objectSections(object);auto symbols=parse(sections.at("symbols"));
  for(auto &point:e.asmPoints) {
    auto *p=point.getAsObject();StringRef identity;
    for(auto &symbol:*symbols.getAsObject())if(symbol.second.getAsObject()->getString("name")==p->getString("symbol"))identity=*symbol.second.getAsObject()->getString("interface_hash");
    for(auto &entry:*report.getArray("entries")) {
      auto *entryObject=entry.getAsObject();auto *at=entryObject->getArray("point");
      if((*at)[0].getAsString()==identity && (*at)[1].getAsString()==p->getString("block") && (*at)[2].getAsInteger()==p->getInteger("ordinal")) {
        (*entryObject)["source"]="dialect-0.2.13:N31";(*entryObject)["classification"]="trapped";(*entryObject)["reason"]=*p->getString("reason");
      }
    }
  }
  auto coverage=jcs(json::Value(std::move(report)))+"\n";write(dir+"/coverage.json",coverage);write(dir+"/all-coverage.json",coverage);
  write(dir+"/blockers.json",jcs(json::Value(json::Array{json::Object{{"code","BD-B-ISA7"},{"entry",entryName},
    {"section","11.5/17.6/25.1"},{"reason","R entry: mandatory pre-instruction typed fault 1 requires ISA-7; generic trap only on exhausted counter; no later source effect; prefix history retained"}}}))+"\n");
  // Device bitcode retains materialised bodies; host main gets the launch ABI.
  launch->eraseFromParent();root->setName(entryName);
  checkComparisonMaterialisation(m);
  raw_fd_ostream bc(out.str()+"/device.bc",ec);if(ec)fail("output",ec.message());WriteBitcodeToFile(m,bc);bc.close();
  auto buildRecord=parse(build);hostStub(sourceEntry,object,*buildRecord.getAsObject(),sharesGlobalState(sourceEntry));
  raw_fd_ostream host(out.str()+"/host.bc",ec);if(ec)fail("output",ec.message());WriteBitcodeToFile(source,host);host.close();
  write(out.str()+"/launches.json",jcs(json::Value(json::Array{json::Object{{"entry",entryName},{"object",entryName+"/launch.bennett"},{"build_sha256",hash(build)},{"verdict","blocked:BD-B-ISA7"}}}))+"\n");
  json::Object artifacts;
  for(auto file:{"host.bc","device.bc","launches.json"}) {auto bytes=read(out.str()+"/"+file);artifacts[file]=json::Object{{"bytes",int64_t(bytes.size())},{"sha256",hash(bytes)}};}
  for(auto file:{"launch.bennett","build.json","certificate.json","coverage.json","all-coverage.json","blockers.json"}) {auto path=entryName+"/"+file;auto bytes=read(out.str()+"/"+path);artifacts[path]=json::Object{{"bytes",int64_t(bytes.size())},{"sha256",hash(bytes)}};}
  write(dir+"/launch-record.json",jcs(json::Value(json::Object{{"schema","bennett-plugin-launch-record-1"},{"entry",entryName},{"artifacts",std::move(artifacts)}}))+"\n");
}
````

## `src/Scalar.cpp` (1265 lines)

````
#include "Bennett.h"
#include "ByteOrder.h"
#include "ComparisonLayout.h"
#include "llvm/ADT/StringExtras.h"
#include "llvm/Config/llvm-config.h"
#include "llvm/IR/InstIterator.h"
#include "llvm/IR/Operator.h"
#include "llvm/Analysis/ValueTracking.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/Path.h"
#include "llvm/Support/SHA256.h"
#include <regex>
using namespace llvm;
namespace bennett {
static std::string sha(StringRef s) {
  return toHex(SHA256::hash(arrayRefFromStringRef(s)), true);
}
static std::string number(const APInt &n) {
  SmallString<48> s;
  n.toString(s, 10, false);
  return s.str().str();
}
static std::string join(const std::vector<std::string> &v,
                        StringRef sep = ", ") {
  std::string s;
  for (auto &x : v) {
    if (!s.empty())
      s += sep;
    s += x;
  }
  return s;
}
static std::string canonicalJSON(const json::Value &v) {
  if(auto *o=v.getAsObject()) {
    std::map<std::string,const json::Value *> sorted;for(auto &e:*o)sorted[e.first.str()]=&e.second;
    std::string out="{";for(auto &e:sorted){if(out.size()>1)out+=",";out+=canonicalJSON(json::Value(e.first))+":"+canonicalJSON(*e.second);}return out+"}";
  }
  if(auto *a=v.getAsArray()) {std::string out="[";for(auto &e:*a){if(out.size()>1)out+=",";out+=canonicalJSON(e);}return out+"]";}
  return formatv("{0}",v).str();
}
struct Scalar {
  Module &m;
  Function &f;
  std::map<const Value *, std::string> names;
  std::vector<std::string> regs, lines;
  unsigned constants = 0, temps = 0, expressions = 0;
  // Linked runtime microvectors may retain their explicitly supplied register
  // spelling. Source functions always use the canonical §16.3 numbering.
  bool runtimeNames() {return f.hasFnAttribute("bennett.runtime.locations");}
  std::map<std::string,std::string> runtimeConstants;

  std::map<const GlobalVariable *, std::string> globals;
  std::map<Function *, std::string> functions;
  Analysis *analysis = nullptr;
  unsigned width(Type *t) {
    if (t->isIntegerTy() && t->getIntegerBitWidth() <= 128)
      return t->getIntegerBitWidth();
    if (t->isPointerTy())
      return m.getDataLayout().getPointerTypeSizeInBits(t);
    if (t->isVoidTy())
      return 1;
    if (t->isFloatingPointTy())
      return t->getPrimitiveSizeInBits();
    if(t->isAggregateType()) {
      unsigned n=0;for(auto &field:fields(t))n+=width(field.type);
      if(n && n<=128)return n;
    }
    unimplemented("§12.6/§12.7 vector/aggregate/wide scalar", 2, &f);
  }
  struct Field {std::vector<unsigned> path;Type *type;};
  std::vector<Field> fields(Type *type) {
    std::vector<Field> result;
    std::function<void(Type *,std::vector<unsigned>)> visit=[&](Type *t,std::vector<unsigned> path) {
      if(t->isAggregateType()) {
        unsigned n=t->isStructTy()?cast<StructType>(t)->getNumElements():cast<ArrayType>(t)->getNumElements();
        for(unsigned k=0;k<n;++k) {auto next=path;next.push_back(k);visit(t->isStructTy()?cast<StructType>(t)->getElementType(k):t->getArrayElementType(),next);}
      } else result.push_back({path,t});
    };visit(type,{});return result;
  }
  std::map<const Value *,std::vector<std::string>> fieldAliases;
  static bool prefix(ArrayRef<unsigned> path,ArrayRef<unsigned> start) {
    return path.size()>=start.size() && std::equal(start.begin(),start.end(),path.begin());
  }
  std::string fieldName(Value *v,unsigned n) {
    if(auto *c=dyn_cast<Constant>(v)) {
      auto layout=fields(v->getType());
      for(unsigned index:layout[n].path)c=c->getAggregateElement(index);
      return value(c);
    }
    if(auto it=fieldAliases.find(v);it!=fieldAliases.end())return it->second[n];
    if(auto *insert=dyn_cast<InsertValueInst>(v))
      if(!prefix(fields(v->getType())[n].path,insert->getIndices()))return fieldName(insert->getAggregateOperand(),n);
    return names.at(v)+(v->getType()->isAggregateType()?"_"+std::to_string(n):"");
  }
  std::vector<std::pair<std::string,unsigned>> locations(Value *v) {
    std::vector<std::pair<std::string,unsigned>> result;unsigned n=0;
    for(auto &field:fields(v->getType()))result.push_back({fieldName(v,n++),width(field.type)});
    return result;
  }
  void unpack(Value *v,const std::string &packed) {
    unsigned offset=0,total=width(v->getType()),n=0;
    for(auto &field:fields(v->getType())) {
      auto part=packed;unsigned w=width(field.type);
      if(offset) {auto c=constant(APInt(total,offset));part=temp(total,"lift.lshr "+part+" "+c);}
      auto output=names.at(v)+"_"+std::to_string(n++);
      if(w!=total) {dest(output,w);lines.push_back(output+" = lift.trunc.i"+std::to_string(w)+" "+part);}
      else {fieldAliases[v]={part};}
      offset+=w;
    }
  }
  void dest(std::string n, unsigned w) {
    regs.push_back(n + ":reg[" + std::to_string(w) + "]");
  }
  std::string constant(APInt n) {
    auto key=std::to_string(n.getBitWidth())+":"+number(n);
    if(runtimeNames() && runtimeConstants.count(key))return runtimeConstants[key];
    std::string s = "c" + std::to_string(constants++);
    if(runtimeNames()) {
      auto attr=f.getFnAttribute("bennett.runtime.constants").getValueAsString();
      SmallVector<StringRef> list;attr.split(list,',');
      if(constants<=list.size() && !list[constants-1].empty())s=list[constants-1].str();
      runtimeConstants[key]=s;
    }
    dest(s, n.getBitWidth());
    lines.push_back(s + " = lift.const.i" + std::to_string(n.getBitWidth()) +
                    " " + number(n));
    return s;
  }
  std::string temp(unsigned w, std::string row) {
    std::string s = "t" + std::to_string(temps++);
    dest(s, w);
    lines.push_back(s + " = " + row);
    return s;
  }
  std::string value(Value *v) {
    if (isa<UndefValue>(v) || isa<PoisonValue>(v) ||
        isa<ConstantPointerNull>(v))
      return constant(APInt(width(v->getType()), 0));
    if (auto *g = dyn_cast<GlobalVariable>(v)) {
      if (!globals.count(g)) unimplemented("§19.5 comparison global layout",2,g);
      if(runtimeNames() && names.count(g))return names[g];
      std::string n = "c" + std::to_string(constants++);
      if(runtimeNames()) {n="g";--constants;names[g]=n;}
      dest(n,width(g->getType())); lines.push_back(n+" = lift.addr @"+globals[g]); return n;
    }
    if (auto *fn = dyn_cast<Function>(v)) {
      if (auto address=comparisonFunctionAddress(*fn))
        return constant(APInt(width(fn->getType()),*address));
      if (!hasComparisonLayout())if(auto *md=fn->getMetadata("bennett.address"))
        return constant(cast<ConstantInt>(cast<ConstantAsMetadata>(md->getOperand(0))->getValue())->getValue());
      unimplemented("§19.5 comparison function address",4,fn);
    }
    if (auto *c = dyn_cast<ConstantFP>(v))
      return constant(c->getValueAPF().bitcastToAPInt());
    if (auto *c = dyn_cast<ConstantInt>(v))
      return constant(c->getValue());
    if (auto *c = dyn_cast<ConstantExpr>(v)) {
      if (c->getOpcode() == Instruction::GetElementPtr)
        return gep(cast<GEPOperator>(c),
                   "expr" + std::to_string(expressions++));
      if (c->isCast()) {
        auto a = value(c->getOperand(0));
        unsigned from = width(c->getOperand(0)->getType()),
                 to = width(c->getType());
        if (from == to)
          return a;
        return temp(to,
                    std::string(from < to ? "lift.zext.i" : "lift.trunc.i") +
                        std::to_string(to) + " " + a);
      }
      unimplemented("§16.4 constant expression", 2, v);
    }
    if (names.count(v))
      return names[v];
    unimplemented("§16.4 non-scalar operand", 2, v);
  }
  std::string gep(GEPOperator *g, std::string output) {
    unsigned p = width(g->getType()),
             i = m.getDataLayout().getIndexTypeSizeInBits(g->getType());
    if (i > 128 || p > 128)
      unimplemented("§12.7 wide pointer limbs", 2, &f);
    std::string base = value(g->getPointerOperand()), acc = base;
    if (i < p)
      acc = temp(i, "lift.trunc.i" + std::to_string(i) + " " + base);
// collectOffset preserves insertion order of dynamic indices.
#if LLVM_VERSION_MAJOR >= 23
    SmallMapVector<Value *, APInt, 4> vars;
#else
    MapVector<Value *, APInt> vars;
#endif
    APInt off(i, 0);
    if (!g->collectOffset(m.getDataLayout(), i, vars, off))
      unimplemented("§16.4 GEP", 2, &f);
    std::vector<std::pair<Value *, APInt>> dynamic;
    for (auto &e : vars)
      dynamic.push_back(e);
    for (unsigned k = 0; k < dynamic.size(); ++k) {
      auto &e = dynamic[k];
      std::string idx = value(e.first);
      unsigned w = width(e.first->getType());
      if (w != i)
        idx = temp(i, std::string(w < i ? "lift.sext.i" : "lift.trunc.i") +
                          std::to_string(i) + " " + idx);
      if (e.second != 1) {
        auto c = constant(e.second);
        idx = temp(i, "lift.mul " + idx + " " + c);
      }
      bool last = k + 1 == dynamic.size() && off.isZero() && i == p;
      if (last && !output.empty()) {
        dest(output, p);
        lines.push_back(output + " = lift.add " + acc + " " + idx);
        acc = output;
      } else
        acc = temp(i, "lift.add " + acc + " " + idx);
    }
    if (!off.isZero()) {
      auto c = constant(off);
      if (i == p && !output.empty()) {
        dest(output, p);
        lines.push_back(output + " = lift.add " + acc + " " + c);
        acc = output;
      } else
        acc = temp(i, "lift.add " + acc + " " + c);
    }
    if (i < p) {
      auto lo = temp(p, "lift.zext.i" + std::to_string(p) + " " + acc);
      auto c = constant(APInt::getHighBitsSet(p, p - i));
      auto hi = temp(p, "lift.and " + base + " " + c);
      if (output.empty())
        return temp(p, "lift.or " + hi + " " + lo);
      dest(output, p);
      lines.push_back(output + " = lift.or " + hi + " " + lo);
      return output;
    }
    if (acc == base && !output.empty()) {
      dest(output, p);
      lines.push_back(output + " = lift.mov " + base);
      return output;
    }
    return acc;
  }
  bool lowerAggregate(Instruction &i) {
    if(auto *insert=dyn_cast<InsertValueInst>(&i)) {
      auto original=locations(insert->getAggregateOperand());
      auto added=locations(insert->getInsertedValueOperand());
      std::vector<std::string> aliases;unsigned j=0,n=0;
      for(auto &field:fields(i.getType())) {
        if(prefix(field.path,insert->getIndices())) {
          auto output=names[&i]+"_"+std::to_string(n);dest(output,width(field.type));
          lines.push_back(output+" = lift.mov "+added[j++].first);aliases.push_back(output);
        } else aliases.push_back(original[n].first);
        ++n;
      }
      fieldAliases[&i]=std::move(aliases);return true;
    }
    if(auto *extract=dyn_cast<ExtractValueInst>(&i)) {
      auto input=locations(extract->getAggregateOperand());unsigned j=0,n=0;
      for(auto &field:fields(extract->getAggregateOperand()->getType())) {
        if(prefix(field.path,extract->getIndices())) {
          auto output=names[&i]+(i.getType()->isAggregateType()?"_"+std::to_string(j):"");
          dest(output,width(field.type));lines.push_back(output+" = lift.mov "+input[n].first);++j;
        }
        ++n;
      }
      return true;
    }
    if(i.getType()->isAggregateType() && (isa<SelectInst>(i)||isa<FreezeInst>(i))) {
      auto *select=dyn_cast<SelectInst>(&i);auto condition=select?value(select->getCondition()):"";
      auto left=locations(select?select->getTrueValue():i.getOperand(0));
      auto right=select?locations(select->getFalseValue()):left;
      for(unsigned n=0;n<left.size();++n) {auto output=fieldName(&i,n);dest(output,left[n].second);
        lines.push_back(output+(select?" = lift.select "+condition+" "+left[n].first+" "+right[n].first:" = lift.mov "+left[n].first));}
      return true;
    }
    return false;
  }
  bool lowerCall(CallBase *call, BasicBlock &bb, const std::function<std::string(BasicBlock *)> &blockName) {
    if (auto *g = call->getCalledFunction();
        g && g->getName() == "__bennett_nz_fault") {
      auto *c = dyn_cast<ConstantInt>(call->getArgOperand(0));
      if (!c)
        unimplemented("§12.3 nonliteral fault", 2, call);
      lines.push_back("fault " + number(c->getValue()));
      return false;
    }
    auto *g = call->getCalledFunction();
    if(!g)g=resolve(call->getCalledOperand());
    std::vector<std::string> args;
    for (Value *v : call->args())for(auto &part:locations(v))args.push_back(part.first);
    auto name = g ? g->getName() : StringRef();
    if (name == "__bennett_nz_alloc") {
      dest(names[call],width(call->getType()));
      lines.push_back(names[call]+" = lift.alloc "+args[0]); return true;
    }
    if (name == "__bennett_nz_free") {lines.push_back("lift.free "+args[0]);return true;}
    auto result = names[call];
    if (call->getType()->isVoidTy()) {result="t"+std::to_string(temps++);dest(result,1);}
    else if(call->getType()->isAggregateType()) {result="t"+std::to_string(temps++);dest(result,width(call->getType()));}
    else dest(result,width(call->getType()));
    if (g && functions.count(g)) {
      lines.push_back(result+" = lift.call @"+functions[g]+" ("+join(args)+")");if(call->getType()->isAggregateType())unpack(call,result);return true;
    }
    if (!g && analysis) {
      auto candidates=analysis->candidates(call->getCalledOperand(),call->getFunctionType());
      std::vector<Function *> sorted(candidates.begin(),candidates.end());
      auto address=[](Function *f) -> uint64_t {
        if(auto n=comparisonFunctionAddress(*f))return *n;
        if(hasComparisonLayout())fail("BD-E-COMPARISON-LAYOUT","missing function address",f);
        auto *md=f->getMetadata("bennett.address");
        if (!md) unimplemented("§19.5 comparison function addresses",4,f);
        return cast<ConstantInt>(cast<ConstantAsMetadata>(md->getOperand(0))->getValue())->getZExtValue();
      };
      std::sort(sorted.begin(),sorted.end(),[&](auto *a,auto *b){return address(a)<address(b);});
      auto callee=value(call->getCalledOperand());
      unsigned ordinal=1;for (Instruction &prev:bb) {if (&prev==call) break;if(auto *c=dyn_cast<CallBase>(&prev)) if(!resolve(c->getCalledOperand())) ++ordinal;}
      auto prefix=blockName(&bb)+".q"+std::to_string(ordinal);
      unsigned serial=0;
      std::function<void(int,int)> tree=[&](int lo,int hi) {
        if(hi<lo) {lines.push_back("qjump "+prefix+"d");return;}
        if(hi-lo+1<=3) {
          for(int k=lo;k<=hi;++k) {
            auto c=constant(APInt(width(call->getCalledOperand()->getType()),address(sorted[k])));
            auto t=temp(1,"lift.icmp.eq "+callee+" "+c);
            auto next=k<hi?blockName(&bb)+".s"+std::to_string(++serial):prefix+"d";
            lines.push_back("qbranch "+t+" "+prefix+"c"+std::to_string(k)+" "+next);
            if(k<hi) lines.push_back(next+"():");
          }
        } else {
          int mid=(lo+hi)/2;
          auto c=constant(APInt(width(call->getCalledOperand()->getType()),address(sorted[mid])));
          auto t=temp(1,"lift.icmp.ult "+callee+" "+c);
          auto l=blockName(&bb)+".s"+std::to_string(++serial),r=blockName(&bb)+".s"+std::to_string(++serial);
          lines.push_back("qbranch "+t+" "+l+" "+r);lines.push_back(l+"():");tree(lo,mid-1);lines.push_back(r+"():");tree(mid,hi);
        }
      };
      tree(0,int(sorted.size())-1);
      for(unsigned k=0;k<sorted.size();++k) {
        lines.push_back(prefix+"c"+std::to_string(k)+"():");
        lines.push_back(result+" = lift.call @"+functions.at(sorted[k])+" ("+join(args)+")");
        lines.push_back("qjump "+prefix+"r");
      }
      lines.push_back(prefix+"d():");lines.push_back("fault 4");lines.push_back(prefix+"r():");if(call->getType()->isAggregateType())unpack(call,result);return true;
    }
    unimplemented("§14 calls (missing linked definition)", 2, call);
    return true;
  }
  void lowerReturn(ReturnInst &returned) {
    Value *rv = returned.getReturnValue();
    std::string v = "r";
    if (rv && rv->getType()->isAggregateType()) {
      // §16.4: evaluate all flattened fields first, then pack without padding.
      auto parts=locations(rv); unsigned packed = width(rv->getType()), offset = 0;
      for (auto &part : parts) {
        auto n = part.first;
        if (part.second != packed) n = temp(packed,"lift.zext.i"+std::to_string(packed)+" "+n);
        if (offset) { auto c = constant(APInt(packed,offset)); n = temp(packed,"lift.shl "+n+" "+c); }
        v = offset ? temp(packed,"lift.or "+v+" "+n) : n;
        offset += part.second;
      }
    } else if (rv) v = value(rv);
    lines.push_back("lift.ret " + v);
  }
  void prepareValueNames() {
    unsigned k = 0;
    for (Argument &a : f.args())
      names[&a] = "a" + std::to_string(k++);
    k = 0;
    for (Instruction &i : instructions(f))
      if (!i.getType()->isVoidTy())
        names[&i] = runtimeNames() && i.hasName() ? i.getName().str() : "v" + std::to_string(k++);
  }
  std::string body() {
    prepareValueNames();
    std::map<BasicBlock *, unsigned> blockIndex;
    unsigned k = 0;
    for (BasicBlock &b : f)
      blockIndex[&b] = k++;
    auto blockName = [&](BasicBlock *b) {
      return std::string("^b") + std::to_string(blockIndex[b]);
    };
    auto moves = [&](BasicBlock *from, BasicBlock *to) {
      std::vector<std::string> dst, src;
      for (PHINode &phi : to->phis()) {
        auto incoming=locations(phi.getIncomingValueForBlock(from));unsigned n=0;
        for(auto &part:incoming) {auto name=fieldName(&phi,n++);dst.push_back(name);src.push_back(part.first);dest(name,part.second);}
      }
      if (!dst.empty())
        lines.push_back("(" + join(dst) + ") = lift.parmov (" + join(src) +
                        ")");
    };
    for (BasicBlock &bb : f) {
      lines.push_back(blockName(&bb) + "():");
      std::set<BasicBlock *> edgeBlocks;
      auto target = [&](BasicBlock *b) {
        if (b->phis().empty())
          return blockName(b);
        edgeBlocks.insert(b);
        return blockName(&bb) + ".e" + std::to_string(blockIndex[b]);
      };
      for (Instruction &i : bb) {
        if (isa<PHINode>(i))
          continue;
        auto branch=[&](Value *condition,BasicBlock *yes,BasicBlock *no) {
          if(!condition || yes==no) {moves(&bb,yes);lines.push_back("qjump "+blockName(yes));}
          else {auto cond=value(condition);auto y=target(yes),n=target(no);lines.push_back("qbranch "+cond+" "+y+" "+n);}
        };
#if LLVM_VERSION_MAJOR >= 23
        if(auto *br=dyn_cast<UncondBrInst>(&i)) {branch(nullptr,br->getSuccessor(0),nullptr);continue;}
        if(auto *br=dyn_cast<CondBrInst>(&i)) {branch(br->getCondition(),br->getSuccessor(0),br->getSuccessor(1));continue;}
#else
        if(auto *br=dyn_cast<BranchInst>(&i)) {branch(br->isUnconditional()?nullptr:br->getCondition(),br->getSuccessor(0),br->isUnconditional()?nullptr:br->getSuccessor(1));continue;}
#endif
        if(auto *br=dyn_cast<IndirectBrInst>(&i)) {
          auto address=value(br->getAddress());
          // §14.9: B(F)+k, with k counting non-entry address-taken blocks in
          // layout order. Comparison layout must provide the backing object.
          auto *object=m.getGlobalVariable("__bennett_rt_blk."+f.getName().str(),true);
          if(!object || !globals.count(object)) unimplemented("§14.9 blockaddress comparison layout",2,br);
          uint64_t base=4096;
          for(GlobalVariable &g:m.globals()) if(globals.count(&g)) {
            base=alignTo(base,m.getDataLayout().getPreferredAlign(&g));
            if(&g==object) break;
            base+=m.getDataLayout().getTypeAllocSize(g.getValueType()).getFixedValue();
          }
          std::vector<std::pair<uint64_t,BasicBlock *>> candidates;
          uint64_t ordinal=0;
          for(BasicBlock &b:f) if(&b!=&f.getEntryBlock() && b.hasAddressTaken()) {
            bool listed=false;
            for(unsigned k=0;k<br->getNumDestinations();++k) listed|=br->getDestination(k)==&b;
            if(listed) candidates.push_back({base+ordinal,&b});
            ++ordinal;
          }
          // Addresses are sorted by layout; the short-domain linear tree is
          // the <=3 leaf case of §14.2. Larger domains need its balanced tree.
          if(candidates.size()>3) unimplemented("§14.9 balanced indirectbr tree",2,br);
          for(unsigned k=0;k<candidates.size();++k) {
            if(k) lines.push_back(blockName(&bb)+".s"+std::to_string(k)+"():");
            auto c=constant(APInt(width(br->getAddress()->getType()),candidates[k].first));
            auto t=temp(1,"lift.icmp.eq "+address+" "+c);
            auto next=k+1<candidates.size()?blockName(&bb)+".s"+std::to_string(k+1):blockName(&bb)+".d";
            lines.push_back("qbranch "+t+" "+target(candidates[k].second)+" "+next);
          }
          lines.push_back(blockName(&bb)+".d():");lines.push_back("fault 4");
          continue;
        }
        if (auto *sw = dyn_cast<SwitchInst>(&i)) {
          std::string cond = value(sw->getCondition()),
                      fallback = target(sw->getDefaultDest());
          std::vector<std::pair<APInt, std::string>> keys;
          for (auto c : sw->cases())
            keys.emplace_back(c.getCaseValue()->getValue(),
                              target(c.getCaseSuccessor()));
          std::sort(keys.begin(), keys.end(),
                    [](auto &a, auto &b) { return a.first.ult(b.first); });
          // Allocate compare blocks in creation order; emit rows in that same
          // order.
          std::vector<std::string> ids = {blockName(&bb)};
          std::vector<std::vector<std::string>> chunks(1);
          auto newBlock = [&]() {
            unsigned n = ids.size();
            ids.push_back(blockName(&bb) + ".s" + std::to_string(n));
            chunks.emplace_back();
            return n;
          };
          std::function<void(int, int, unsigned)> tree = [&](int lo, int hi,
                                                             unsigned cur) {
            size_t begin = lines.size();
            if (hi < lo)
              lines.push_back("qjump " + fallback);
            else if (hi - lo + 1 <= 3) {
              for (int j = lo; j <= hi; ++j) {
                auto c = constant(keys[j].first);
                auto t = temp(1, "lift.icmp.eq " + cond + " " + c);
                unsigned next = j < hi ? newBlock() : 0;
                lines.push_back("qbranch " + t + " " + keys[j].second + " " +
                                (j < hi ? ids[next] : fallback));
                chunks[cur].insert(chunks[cur].end(), lines.begin() + begin,
                                   lines.end());
                lines.resize(begin);
                cur = next;
              }
              return;
            } else {
              int mid = (lo + hi) / 2;
              auto c = constant(keys[mid].first);
              auto t = temp(1, "lift.icmp.ult " + cond + " " + c);
              unsigned l = newBlock(), r = newBlock();
              lines.push_back("qbranch " + t + " " + ids[l] + " " + ids[r]);
              chunks[cur].insert(chunks[cur].end(), lines.begin() + begin,
                                 lines.end());
              lines.resize(begin);
              tree(lo, mid - 1, l);
              tree(mid, hi, r);
              return;
            }
            chunks[cur].insert(chunks[cur].end(), lines.begin() + begin,
                               lines.end());
            lines.resize(begin);
          };
          // Destinations must be numbered by output text order, not DFS
          // recursion order. Build shape above, then remap constants/temps by
          // first appearance below.
          tree(0, (int)keys.size() - 1, 0);
          for (unsigned n = 0; n < chunks.size(); ++n) {
            if (n)
              lines.push_back(ids[n] + "():");
            lines.insert(lines.end(), chunks[n].begin(), chunks[n].end());
          }
          continue;
        }
        if (lowerAggregate(i)) continue;
        if (auto *g = dyn_cast<GetElementPtrInst>(&i)) {
          gep(cast<GEPOperator>(g), names[&i]);
          continue;
        }
        if (auto *r = dyn_cast<ReturnInst>(&i)) {
          lowerReturn(*r);
          continue;
        }
        if (isa<UnreachableInst>(i)) {
          lines.push_back("fault 4");
          continue;
        }
        if (auto *call = dyn_cast<CallBase>(&i)) {
          if (!lowerCall(call, bb, blockName)) break;
          continue;
        }
        if (auto *l = dyn_cast<LoadInst>(&i)) {
          unsigned w = width(l->getType());
          if (w % 8) unimplemented("§12 N22 nonbyte load",2,l);
          auto p = value(l->getPointerOperand());lines.push_back("lift.boundscheck "+p+" "+std::to_string(w/8));
          dest(names[l],w);
          if(m.getDataLayout().isLittleEndian() || w==8)
            lines.push_back(names[l]+" = lift.load.i"+std::to_string(w)+" "+p);
          else {
            auto raw=temp(w,"lift.load.i"+std::to_string(w)+" "+p);
            auto value=reverseBytes(raw,w,[&](APInt n){return constant(n);},
              [&](unsigned bits,std::string op){return temp(bits,"lift."+op);});
            lines.push_back(names[l]+" = lift.mov "+value);
          }
          continue;
        }
        if (auto *st = dyn_cast<StoreInst>(&i)) {
          auto v=value(st->getValueOperand()),p=value(st->getPointerOperand());
          unsigned w=width(st->getValueOperand()->getType());
          if(w%8)unimplemented("§12 N22 nonbyte store",2,st);
          lines.push_back("lift.boundscheck "+p+" "+std::to_string(w/8));
          if(!m.getDataLayout().isLittleEndian() && w>8)
            v=reverseBytes(v,w,[&](APInt n){return constant(n);},
              [&](unsigned bits,std::string op){return temp(bits,"lift."+op);});
          lines.push_back("lift.store.i"+std::to_string(w)+" "+p+" "+v);continue;
        }
        if (isa<AllocaInst>(i)) unimplemented("§17.3 shadow stack",2,&i);
        if (i.getType()->isFPOrFPVectorTy() && !isa<BitCastInst>(i) && !isa<SelectInst>(i))
          unimplemented("§13 soft-float", 2, &i);
        std::string row;
        if (auto *c = dyn_cast<ICmpInst>(&i)) {
          auto a = value(c->getOperand(0)), b = value(c->getOperand(1));
          auto pred = c->getPredicate();
          if (pred == CmpInst::ICMP_UGT || pred == CmpInst::ICMP_UGE ||
              pred == CmpInst::ICMP_SGT || pred == CmpInst::ICMP_SGE) {
            pred = CmpInst::getSwappedPredicate(pred);
            std::swap(a, b);
          }
          row = "lift.icmp." + CmpInst::getPredicateName(pred).str() + " " + a +
                " " + b;
        } else if (auto *b = dyn_cast<BinaryOperator>(&i)) {
          auto a = value(b->getOperand(0)), c = value(b->getOperand(1));
          // ISA shifts define >=W as zero; the materialised scalar semantics
          // agrees.
          row = "lift." + std::string(b->getOpcodeName()) + " " + a + " " + c;
        } else if (auto *s = dyn_cast<SelectInst>(&i)) {
          auto c = value(s->getCondition()), a = value(s->getTrueValue()),
               b = value(s->getFalseValue());
          row = "lift.select " + c + " " + a + " " + b;
        } else if (auto *c = dyn_cast<CastInst>(&i)) {
          auto a = value(c->getOperand(0));
          unsigned from = width(c->getOperand(0)->getType()),
                   to = width(c->getType());
          std::string op = c->getOpcodeName();
          if (op == "ptrtoint" || op == "inttoptr" || op == "addrspacecast" ||
              op == "bitcast")
            op = from == to ? "mov" : from < to ? "zext" : "trunc";
          row = "lift." + op + (op == "mov" ? "" : ".i" + std::to_string(to)) +
                " " + a;
        } else if (isa<FreezeInst>(i))
          row = "lift.mov " + value(i.getOperand(0));
        else
          unimplemented("§16.4 scalar row", 2, &i);
        dest(names[&i], width(i.getType()));
        lines.push_back(names[&i] + " = " + row);
      }
      std::vector<BasicBlock *> sortedEdges(edgeBlocks.begin(),
                                            edgeBlocks.end());
      std::sort(sortedEdges.begin(), sortedEdges.end(), [&](auto *a, auto *b) {
        return blockIndex[a] < blockIndex[b];
      });
      for (auto *b : sortedEdges) {
        lines.push_back(blockName(&bb) + ".e" + std::to_string(blockIndex[b]) +
                        "():");
        moves(&bb, b);
        lines.push_back("qjump " + blockName(b));
      }
    }
    // Canonical first-destination order also renumbers compare-tree rows
    // emitted in creation order. Phi destinations are listed only once.
    std::map<std::string, unsigned> widths;
    for (auto &r : regs) {
      auto at = r.find(":reg[");
      widths[r.substr(0, at)] = std::stoul(r.substr(at + 5));
    }
    std::map<std::string, std::string> renames;
    unsigned cn = 0, tn = 0;
    for (auto &line : lines) {
      if(runtimeNames())break;
      auto eq = line.find(" = ");
      if (eq == std::string::npos)
        continue;
      auto dst = line.substr(0, eq);
      if (dst.size() > 1 && (dst[0] == 'c' || dst[0] == 't') &&
          std::isdigit(dst[1]) && !renames.count(dst))
        renames[dst] = std::string(1, dst[0]) +
                       std::to_string(dst[0] == 'c' ? cn++ : tn++);
    }
    std::vector<std::string> finalRegs;
    std::set<std::string> declared;
    for (auto &line : lines) {
      std::string replaced;
      std::regex token(R"(\b[ct][0-9]+\b)");
      size_t last = 0;
      for (std::sregex_iterator it(line.begin(), line.end(), token), end;
           it != end; ++it) {
        replaced += line.substr(last, it->position() - last);
        replaced += renames.count(it->str()) ? renames[it->str()] : it->str();
        last = it->position() + it->length();
      }
      replaced += line.substr(last);
      line = replaced;
      auto eq = line.find(" = ");
      if (eq != std::string::npos) {
        std::string dst = line.substr(0, eq);
        std::regex loc(R"([A-Za-z_][A-Za-z_0-9]*)");
        for (std::sregex_iterator it(dst.begin(), dst.end(), loc), end;
             it != end; ++it) {
          auto n = it->str();
          if (!declared.insert(n).second)
            continue;
          unsigned w = widths[n];
          for (auto &r : renames)
            if (r.second == n) {
              w = widths[r.first];
              break;
            }
          finalRegs.push_back(n + ":reg[" + std::to_string(w) + "]");
        }
      }
    }
    regs = finalRegs;
    std::vector<std::string> params;
    for(Argument &a:f.args())for(auto &part:locations(&a))params.push_back(part.first+":reg["+std::to_string(part.second)+"]");
    std::string b = "lproc @" + functions.at(&f) + " (" + join(params) + ") (r:reg[" +
                    std::to_string(width(f.getReturnType())) + "]) () () ()\n";
    if (!regs.empty())
      b += "regs { " + join(regs) + " }\n";
    b += join(lines, "\n");
    return b;
  }
};
std::string scalarGlobalKey(const GlobalVariable &g) {
  if(g.hasName())return "name:"+g.getName().str();
  unsigned ordinal=0;for(auto &v:g.getParent()->globals()) {if(&v==&g)break;++ordinal;}
  return "index:"+std::to_string(ordinal);
}
std::string scalarGlobalImage(GlobalVariable &g, const std::map<const GlobalVariable *,uint64_t> &bases) {
  auto &dl=g.getParent()->getDataLayout();
  uint64_t size=dl.getTypeAllocSize(g.getValueType()).getFixedValue();std::vector<uint8_t> bytes(size,0);
  std::function<void(Constant *,uint64_t)> image=[&](Constant *c,uint64_t off) {
    auto *t=c->getType();if(c->isNullValue() || isa<UndefValue>(c) || isa<PoisonValue>(c))return;
    if(auto *st=dyn_cast<StructType>(t)) {auto *sl=dl.getStructLayout(st);for(unsigned k=0;k<st->getNumElements();++k)image(c->getAggregateElement(k),off+sl->getElementOffset(k));return;}
    if(auto *at=dyn_cast<ArrayType>(t)) {for(unsigned k=0;k<at->getNumElements();++k)image(c->getAggregateElement(k),off+k*dl.getTypeAllocSize(at->getElementType()).getFixedValue());return;}
    APInt bits(1,0);
    if(auto *n=dyn_cast<ConstantInt>(c))bits=n->getValue();
    else if(auto *n=dyn_cast<ConstantFP>(c))bits=n->getValueAPF().bitcastToAPInt();
    else if(t->isPointerTy()) {
      auto pw=dl.getPointerSizeInBits(t->getPointerAddressSpace());APInt offset(pw,0);
      auto *root=c->stripAndAccumulateConstantOffsets(dl,offset,true);
      if(auto *target=dyn_cast<GlobalVariable>(root);target && bases.count(target))bits=APInt(pw,bases.at(target))+offset;
      else if(auto *f=dyn_cast<Function>(root)) {
        if(auto address=comparisonFunctionAddress(*f))bits=APInt(pw,*address)+offset;
        else if(!hasComparisonLayout() && f->getMetadata("bennett.address"))bits=cast<ConstantInt>(cast<ConstantAsMetadata>(f->getMetadata("bennett.address")->getOperand(0))->getValue())->getValue().zextOrTrunc(pw)+offset;
        else unimplemented("§19.5 comparison function relocation",4,f);
      }
      else if(auto *ce=dyn_cast<ConstantExpr>(c);ce && ce->getOpcode()==Instruction::IntToPtr && isa<ConstantInt>(ce->getOperand(0)))bits=cast<ConstantInt>(ce->getOperand(0))->getValue().zextOrTrunc(pw);
      else unimplemented("§19.5 global pointer relocation target",1,c);
    } else unimplemented("§19.5 vector data image",2,c);
    auto n=dl.getTypeStoreSize(t).getFixedValue();bits=bits.zextOrTrunc(n*8);
    for(unsigned k=0;k<n;++k)bytes[off+k]=bits.lshr((dl.isLittleEndian()?k:n-1-k)*8).getLimitedValue()&255;
  };
  if(!g.hasInitializer())unimplemented("§19.5 undefined data image",2,&g);
  image(g.getInitializer(),0);return toHex(ArrayRef<uint8_t>(bytes),true);
}
uint64_t scalarModuleFlag(Module &m, StringRef name, uint64_t fallback) {
  auto *metadata = m.getModuleFlag(name);
  if (!metadata) return fallback;
  auto *constant = dyn_cast<ConstantAsMetadata>(metadata);
  auto *integer = constant ? dyn_cast<ConstantInt>(constant->getValue()) : nullptr;
  if (!integer) fail("BD-E-ENTRY-RUNTIME", ("integer module flag required: " + name).str());
  return integer->getZExtValue();
}
bool prepareScalarModule(Module &m, Function &f, uint64_t &sstack, unsigned autoSnapshot) {
  // This module is the private device clone. Retain symbols/addresses for
  // native-only definitions but do not send their bodies through N0.
  {
    Analysis selection(m,&f);selection.run();
    selection.releaseTransferGraphs();
    std::set<const Function *> deviceClosure;
    std::function<void(Function *)> retain = [&](Function *function) {
      if (!deviceClosure.insert(function).second || function->isDeclaration()) return;
      for (auto &instruction : instructions(function))
        if (auto *call = dyn_cast<CallBase>(&instruction)) {
          if (auto *callee = call->getCalledFunction()) retain(callee);
          else for (auto *callee : selection.candidates(call->getCalledOperand(), call->getFunctionType())) retain(callee);
        }
    };
    retain(&f);
    for (auto entry : {std::make_pair("bennett.entry.snapshot", "__bennett_rt_entry_replay"),
                       std::make_pair("bennett.ss.init", "__bennett_rt_ss_init")}) {
      if (!scalarModuleFlag(m, entry.first, 0)) continue;
      auto *function = m.getFunction(entry.second);
      if (!function || function->isDeclaration())
        fail("BD-E-ENTRY-RUNTIME", std::string("missing linked definition for ") + entry.second, &f);
      retain(function);
    }
    for(auto &g:m)if(!g.isDeclaration() && !deviceClosure.count(&g) && selection.tiers[&g].empty())g.deleteBody();
    for(auto &g:m)if(!g.isDeclaration() && !deviceClosure.count(&g) && selection.tiers[&g]==std::set<std::string>{"H"})g.deleteBody();
  }
  if(auto *md=m.getModuleFlag("bennett.sstack"))sstack=cast<ConstantInt>(cast<ConstantAsMetadata>(md)->getValue())->getZExtValue();
  if(autoSnapshot && m.getGlobalVariable("__bennett_ss_base",true))m.addModuleFlag(Module::Error,"bennett.entry.stack",uint32_t(1));
  for(auto &g:m)if(!g.isDeclaration())normaliseFP(g);
  normaliseWideABI(m);
  // N27 closure must precede N24 stack preparation (slot helpers introduce pushes).
  for(auto &g:m)if(!g.isDeclaration())normaliseScalar(g);
  for(auto &g:m)if(!g.use_empty())materialiseIntegerRuntime(g);
  bool singleFrame=prepareStack(m,f,sstack);
  if(autoSnapshot) {
    // CC assembly storage has no L users and is not part of caller memory.
    SmallVector<GlobalVariable *> scratch;for(auto &g:m.globals())if(g.getMetadata("bennett.snapshot.scratch"))scratch.push_back(&g);
    for(auto *g:scratch) {if(!g->use_empty())fail("output","CC snapshot scratch escaped into L",g);g->eraseFromParent();}
    prepareEntryReplay(m,autoSnapshot);
  }
  normaliseWideABI(m);
  // Materialise every linked member before computing candidates and read dependencies.
  for (Function &g:m) if(!g.isDeclaration()) {normaliseScalar(g);materialiseFPBits(g);}
  return singleFrame;
}
void collectScalarFunction(Function *g, Analysis &analysis,
                           std::vector<Function *> &closure, std::map<Function *,std::string> &functions) {
    if(!g) fail("BD-E-ENTRY-RUNTIME", "required scalar runtime helper is missing");
    requireSoftFloat(*g);
    if(g->isDeclaration() || functions.count(g)) return;
    functions[g]="L"+std::to_string(functions.size()+1);closure.push_back(g);
    for(Instruction &i:instructions(g)) if(auto *c=dyn_cast<CallBase>(&i)) {
      if(auto *target=c->getCalledFunction()) collectScalarFunction(target, analysis, closure, functions);
      else if(auto *target=resolve(c->getCalledOperand())) collectScalarFunction(target, analysis, closure, functions);
      else {
        auto targets=analysis.candidates(c->getCalledOperand(),c->getFunctionType());
        std::vector<Function *> sorted(targets.begin(),targets.end());
        std::sort(sorted.begin(),sorted.end(),[](auto *a,auto *b) {
          auto address=[](Function *f) {
            if(auto n=comparisonFunctionAddress(*f))return *n;
            if(hasComparisonLayout())fail("BD-E-COMPARISON-LAYOUT","missing function address",f);
            auto *md=f->getMetadata("bennett.address");if(!md) unimplemented("§19.5 comparison function addresses",4,f);return cast<ConstantInt>(cast<ConstantAsMetadata>(md->getOperand(0))->getValue())->getZExtValue();};return address(a)<address(b);
        });for(auto *target:sorted) collectScalarFunction(target, analysis, closure, functions);
      }
    }
}
struct ScalarPublication {
  std::vector<std::string> ins, mems, args, wrapperRegs, wrapperRows, argTypes, insWidths, memSigs;
  unsigned tgt, stackCells;
  uint64_t heapLimit;
  std::vector<std::pair<std::string,uint64_t>> devices;
  std::map<std::string,std::string> bodies, signatures;
  std::string lproc;
  std::vector<Function *> closure;
};
void publishScalarObject(Scalar &s, ScalarPublication publication, StringRef out) {
  auto &[ins, mems, args, wrapperRegs, wrapperRows, argTypes, insWidths, memSigs,
         tgt, stackCells, heapLimit, devices, bodies, signatures, lproc, closure] = publication;
  auto &m = s.m;
  auto &f = s.f;
  std::string wrapper = "oracle @ref (" + join(ins) + ") (tgt:wire[" +
                        std::to_string(tgt) + "]) (fault:wire[4]) (" + join(mems) + ") (" +
                        join(args) + ")\nregs { " + join(wrapperRegs) +
                        " }\n^entry():\n" + join(wrapperRows, "\n");
  std::string osig =
      "{\"abi\":\"0.8\",\"args\":[" + join(argTypes, ",") +
      "],\"fault\":4,\"in\":[" + join(insWidths, ",") +
      "],\"kind\":\"oracle\",\"mem\":[" + join(memSigs, ",") + "],\"tgt\":" + std::to_string(tgt) +
      ",\"tier\":\"q\"}";
  unsigned sc = 0;
  while ((uint64_t(1) << sc) < stackCells)
    ++sc;
  unsigned pw = m.getDataLayout().getPointerSizeInBits();
  std::string prefix = "isa=0.8\nptr_width=" + std::to_string(pw) + "\n";
  // M1 standalone comparison layout: globals in link/module order, data at
  // 4096, heap at the next page, no heap allocations. Driver-supplied layouts M4.
  std::map<std::string,std::string> data, globalLeaves, dataSigs, dataHashes;
  uint64_t nullSize=scalarModuleFlag(m, "bennett.null_size",4096);
  uint64_t base=nullSize;std::map<const GlobalVariable *,uint64_t> globalBases;
  for(GlobalVariable &g:m.globals())if(s.globals.count(&g)) {base=alignTo(base,m.getDataLayout().getPreferredAlign(&g));globalBases[&g]=comparisonGlobalAddress(g).value_or(base);base=std::max(base,globalBases[&g]+m.getDataLayout().getTypeAllocSize(g.getValueType()).getFixedValue());}
  for(GlobalVariable &g:m.globals())if(s.globals.count(&g)) {
    auto size=m.getDataLayout().getTypeAllocSize(g.getValueType()).getFixedValue();
    auto hex=scalarGlobalImage(g,globalBases),name=s.globals[&g];
    data[name]=hex;
    dataSigs[name]="{\"abi\":\"0.8\",\"kind\":\"data\",\"size\":"+std::to_string(size)+",\"tier\":\"-\"}";
    dataHashes[name]=sha(prefix+dataSigs[name]+"\n"+name+" "+hex+"\n");
    globalLeaves[name]="{\"base\":"+std::to_string(globalBases[&g])+",\"image\":\""+name+"\",\"size\":"+std::to_string(size)+"}";
  }
  uint64_t heap=comparisonHeapBase().value_or(scalarModuleFlag(m, "bennett.heap_base",alignTo(base,uint64_t(4096))));unsigned h=0,at=0;
  uint64_t endAddress = scalarModuleFlag(m, "bennett.region_base",heap + heapLimit);
  std::string regionLayout, regionHashLeaves;
  for (auto &d : devices) if (d.first == "BLOCK") {
    uint64_t size = uint64_t(1) << (d.second + 9);
    uint64_t regionBase = alignTo(endAddress, size);
    auto leaf = "{\"base\":" + std::to_string(regionBase) + "}";
    regionLayout = "\"k0\":" + leaf;
    regionHashLeaves = "layout interface_regions.ref.k0 " + leaf + "\n";
    endAddress = regionBase + size;
  }
  for (auto &mem : mems) {
    std::smatch parts;
    if (!std::regex_search(mem, parts, std::regex(R"(([mes][0-9]+):region\[([0-9]+),8\])"))) continue;
    uint64_t size = uint64_t(1) << std::stoul(parts[2]);
    auto leaf = "{\"base\":" + std::to_string(alignTo(endAddress, size)) + "}";
    if (!regionLayout.empty()) regionLayout += ",";
    regionLayout += "\"" + parts[1].str() + "\":" + leaf;
    regionHashLeaves += "layout interface_regions.ref." + parts[1].str() + " " + leaf + "\n";
    endAddress = alignTo(endAddress, size) + size;
  }
  while((uint64_t(1)<<h)<endAddress)++h;
  while((uint64_t(1)<<at)<data.size()+mems.size()+heapLimit)++at;
  std::string images,globalLayout,globalHashLeaves,dataSection,refs;
  for(auto &e:data) {
    images+="data "+e.first+" "+e.second+"\n";
    if(!globalLayout.empty())globalLayout+=",";
    globalLayout+="\""+e.first+"\":"+globalLeaves[e.first];
    globalHashLeaves+="layout globals."+e.first+" "+globalLeaves[e.first]+"\n";
    dataSection+=e.first+" "+e.second+"\n";
  }
  // Hash the complete call graph in SCC dependency order (ISA §9.2).
  std::map<std::string,std::string> hashes=dataHashes;
  std::map<std::string,std::set<std::string>> edges;
  std::regex symbolToken(R"(@([LG][0-9]+)\b)");
  for(auto &b:bodies) {
    auto rest=b.second.substr(b.second.find('\n')+1);
    for(std::sregex_iterator it(rest.begin(),rest.end(),symbolToken),end;it!=end;++it)
      if(bodies.count((*it)[1]))edges[b.first].insert((*it)[1]);
  }
  auto reaches=[&](std::string from,std::string to) {
    std::set<std::string> seen;std::function<bool(std::string)> walk=[&](std::string n) {if(n==to)return true;if(!seen.insert(n).second)return false;for(auto &v:edges[n])if(walk(v))return true;return false;};return walk(from);
  };
  std::function<void(std::string)> hashMember=[&](std::string n) {
    if(hashes.count(n))return;
    std::vector<std::string> group;
    for(auto &b:bodies)if(reaches(n,b.first)&&reaches(b.first,n))group.push_back(b.first);
    bool cyclic=group.size()>1 || edges[n].count(n);
    std::set<std::string> members(group.begin(),group.end());
    for(auto &g:group)for(auto &e:edges[g])if(!members.count(e))hashMember(e);
    std::string envelopes;
    for(auto &g:group) {
      auto newline=bodies[g].find('\n');auto rest=bodies[g].substr(newline+1);
      std::string canonical=bodies[g].substr(0,newline+1),refs;size_t last=0;std::set<std::string> referenced;
      for(std::sregex_iterator it(rest.begin(),rest.end(),symbolToken),end;it!=end;++it) {
        auto v=(*it)[1].str();std::string replacement;
        if(cyclic && members.count(v)) replacement="$"+std::to_string(std::find(group.begin(),group.end(),v)-group.begin());
        else {replacement=hashes.at(v);if(referenced.insert(v).second)refs+=replacement+"\n";}
        canonical+=rest.substr(last,it->position()-last)+"@"+replacement;last=it->position()+it->length();
      }
      canonical+=rest.substr(last);std::string images,leaves;
      for(auto &v:data)if(referenced.count(v.first)) {images+="data "+v.first+" "+v.second+"\n";leaves+="layout globals."+v.first+" "+globalLeaves[v.first]+"\n";}
      envelopes+=prefix+signatures[g]+"\n"+canonical+"\n"+images+leaves+refs;
    }
    auto h=sha(envelopes);
    for(unsigned i=0;i<group.size();++i)hashes[group[i]]=cyclic?sha(h+":"+std::to_string(i)):h;
  };
  for(auto &b:bodies)hashMember(b.first);
  std::string canonical, wrapperRefs; size_t last = 0; std::set<std::string> referenced;
  std::regex wrapperToken(R"(@(L[0-9]+|G[0-9]+)\b)");
  for (std::sregex_iterator it(wrapper.begin(),wrapper.end(),wrapperToken),end;it!=end;++it) {
    auto n = it->str().substr(1), hash = hashes.at(n);
    if (referenced.insert(n).second) wrapperRefs += hash + "\n";
    canonical += wrapper.substr(last,it->position()-last) + "@" + hash;
    last = it->position()+it->length();
  }
  canonical += wrapper.substr(last);
  std::string leaves="layout A_tab "+std::to_string(at)+"\nlayout H "+std::to_string(h)+"\nlayout S_cells "+std::to_string(sc)+"\n"+globalHashLeaves+
    "layout heap_base "+std::to_string(heap)+"\nlayout heap_limit_max "+std::to_string(heapLimit)+"\n"+regionHashLeaves+"layout null_size "+std::to_string(nullSize)+"\nlayout ptr_width "+std::to_string(pw)+"\n";
  std::string oh=sha(prefix+osig+"\n"+canonical+"\n"+images+leaves+wrapperRefs);
  std::string symbols="{\"0\":{\"interface_hash\":\""+oh+"\",\"kind\":\"oracle\",\"name\":\"ref\",\"signature\":"+osig+"}";
  unsigned si=1;
  for(auto *g:closure) {auto n=s.functions.at(g);symbols+=",\""+std::to_string(si++)+"\":{\"interface_hash\":\""+hashes[n]+"\",\"kind\":\"lproc\",\"name\":\""+n+"\",\"signature\":"+signatures[n]+"}";}
  for(auto &e:data)symbols+=",\""+std::to_string(si++)+"\":{\"interface_hash\":\""+dataHashes[e.first]+"\",\"kind\":\"data\",\"name\":\""+e.first+"\",\"signature\":"+dataSigs[e.first]+"}";
  symbols+="}";
  auto parsedSymbols=json::parse(symbols);if(!parsedSymbols)fail("output",toString(parsedSymbols.takeError()));
  symbols=canonicalJSON(*parsedSymbols);
  std::string layout="{\"A_tab\":"+std::to_string(at)+",\"H\":"+std::to_string(h)+",\"S_cells\":"+std::to_string(sc)+",\"globals\":{"+globalLayout+"},\"heap_base\":"+std::to_string(heap)+",\"heap_limit_max\":"+std::to_string(heapLimit)+",\"interface_regions\":{\"ref\":{"+regionLayout+"}},\"null_size\":"+std::to_string(nullSize)+",\"ptr_width\":"+std::to_string(pw)+"}";
  // Every successfully materialised L closure is independently read before
  // publishing an object. This is after all producers and object construction,
  // so unimplemented source transforms retain their own capability diagnostic.
  // H functions in the private whole-program module are not L variants.
  std::set<Function *> variants(closure.begin(),closure.end());
  validateResidual(m,false,&variants);
  errs()<<"bennett: residual validator accepted L closure ("<<variants.size()<<" functions)\n";
  if (auto ec = sys::fs::create_directories(out))
    fail("output", ec.message());
  SmallString<256> path(out);
  sys::path::append(path, "ref.bennett");
  std::error_code ec;
  raw_fd_ostream o(path, ec);
  if (ec)
    fail("output", ec.message());
  o << "bennett-object isa=0.8 object=0.8 launch=0.8 sched=0.8 cert=0.8 "
       "coverage=0.8 target=0.8 ptr_width="
    << pw << "\n\nsection symbols\n"
    << symbols << "\n\nsection functions\n"
    << wrapper << "\n"
    << lproc << (dataSection.empty() ? "" : "\n\nsection data\n" + StringRef(dataSection).rtrim().str()) << "\n\nsection layout\n"
    << layout << "\n";
  errs() << "bennett: scalar reference object " << path << "\n";
}
std::vector<std::pair<std::string,uint64_t>> scalarDevices(std::string &d, Function &f) {
  std::string device;
  if (StringRef(d).starts_with("dev=")) d=";"+d;
  auto deviceStart = d.find(";dev=");
  if (deviceStart != std::string::npos) {
    auto deviceEnd = d.find(';', deviceStart + 1);
    device = d.substr(deviceStart + 5, deviceEnd - deviceStart - 5);
    d.erase(deviceStart, deviceEnd == std::string::npos ? std::string::npos : deviceEnd - deviceStart);
  }
  std::vector<std::pair<std::string,uint64_t>> devices;
  if (!device.empty()) {
    SmallVector<StringRef> parts; StringRef(device).split(parts,'+');
    for (auto part : parts) {
      std::smatch dev; auto value = part.str();
      if (!std::regex_match(value, dev, std::regex(R"((CLOCK|CLOCK_ARG|BLOCK|CONSOLE|ENTROPY)\(([0-9]+)\))")))
        fail("shape","invalid device binding",&f);
      devices.push_back({dev[1],std::stoull(dev[2])});
    }
  }
  return devices;
}
struct ScalarMembers {
  std::map<std::string,std::string> bodies, signatures;
  std::string text;
};
ScalarMembers scalarMembers(Scalar &s, const std::vector<Function *> &closure,
                            Analysis &analysis, const std::map<Function *,std::string> &functions) {
  auto &m = s.m;
  ScalarMembers members;
  for(auto *g:closure) {
    Scalar member{m,*g};member.globals=s.globals;member.functions=functions;member.analysis=&analysis;
    auto name=functions.at(g);members.bodies[name]=member.body();
    std::vector<std::string> widths;for(auto &a:g->args())for(auto &field:member.fields(a.getType()))widths.push_back(std::to_string(member.width(field.type)));
    members.signatures[name]="{\"abi\":\"0.8\",\"kind\":\"lproc\",\"params\":["+join(widths,",")+"],\"result\":"+std::to_string(member.width(g->getReturnType()))+",\"tier\":\"q\"}";
    if(!members.text.empty())members.text+="\n";members.text+=members.bodies[name];
  }
  return members;
}
void lowerScalar(Module &m, Function &f, StringRef desc, StringRef out,
                 unsigned stackCells, uint64_t heapCapacity, int projection, std::map<std::string,std::string> *globalNames, uint64_t sstack, unsigned autoSnapshot) {
  bool singleFrame = prepareScalarModule(m, f, sstack, autoSnapshot);
  // The command/descriptor-selected internal oracle is an invocation entry,
  // even when the input module has no host marker referring to it. PT11 must
  // seed its parameters before the same fixpoint computes indirect domains.
  Analysis analysis(m, &f); analysis.run();
  std::vector<Function *> closure;
  std::map<Function *,std::string> functions;


  sstack=scalarModuleFlag(m, "bennett.sstack",sstack);
  unsigned snapshot=scalarModuleFlag(m, "bennett.entry.snapshot",0);
  bool initialise=scalarModuleFlag(m, "bennett.ss.init",0) || scalarModuleFlag(m, "bennett.entry.stack",0);
  if(snapshot) collectScalarFunction(m.getFunction("__bennett_rt_entry_replay"), analysis, closure, functions);
  for(auto &g:m)for(auto &i:instructions(g))if(auto *c=dyn_cast<CallBase>(&i))if(c->getCalledFunction() && c->getCalledFunction()->getName()=="__bennett_rt_ss_push")initialise=true;
  if(initialise)collectScalarFunction(m.getFunction("__bennett_rt_ss_init"), analysis, closure, functions);
  collectScalarFunction(&f, analysis, closure, functions);
  Scalar s{m, f}; s.functions=functions;s.analysis=&analysis;
  std::string d = desc.str();
  uint64_t heapLimit = heapCapacity;
  auto devices = scalarDevices(d, f);
  auto hasDevice = [&](StringRef name) { for (auto &d : devices) if (d.first == name) return true; return false; };
  std::set<const GlobalVariable *> used;
  std::set<const Value *> seen;
  std::function<void(const Value *)> visit = [&](const Value *v) {
    if (!seen.insert(v).second) return;
    if (auto *g=dyn_cast<GlobalVariable>(v)) {
      used.insert(g); if(g->hasInitializer())visit(g->getInitializer());return;
    }
    if (isa<Function>(v)) return;
    if(auto *u=dyn_cast<User>(v))for(Value *a:u->operands())visit(a);
  };
  for(auto *g:closure) for(Instruction &i:instructions(g))for(Value *v:i.operands())visit(v);
  bool entropyPositionUsed=used.count(m.getGlobalVariable("__bennett_dev_entropy_pos",true));
  auto deviceGlobal = [&](StringRef suffix) -> GlobalVariable * {
    auto *g = m.getGlobalVariable("__bennett_dev_" + suffix.str(), true);
    if (!g) g = new GlobalVariable(m, Type::getInt64Ty(m.getContext()),false,GlobalValue::InternalLinkage,
      ConstantInt::get(Type::getInt64Ty(m.getContext()),0),"__bennett_dev_"+suffix.str());
    used.insert(g);
    return g;
  };
  for (auto &d : devices) {
    auto &device = d.first; auto deviceSize = d.second;
    if (device == "CLOCK" || device == "CLOCK_ARG") deviceGlobal("clock_c");
    if (device == "ENTROPY") { deviceGlobal("entropy_base"); deviceGlobal("entropy_size"); deviceGlobal("entropy_pos"); }
    if (device == "BLOCK") { deviceGlobal("block_base"); deviceGlobal("block_nsect"); }
    if (device == "CONSOLE") {
      deviceGlobal("console_buf"); deviceGlobal("console_L"); deviceGlobal("console_n");
      heapLimit = std::max(heapLimit, deviceSize);
    }
  }
  // The entry dependency decision precedes private allocation (§16.2). A
  // pointer supplied by OUT or read from this invocation's model buffer does
  // not name caller memory. An arbitrary ARG/loaded pointer still needs replay.
  std::set<const Argument *> privateArguments;
  std::regex bindingPattern(R"((IN|ARG|OUT|MEM_IN)\([^)]*\))");
  unsigned bindingIndex = 0;
  for (std::sregex_iterator it(d.begin(),d.end(),bindingPattern),end;it!=end;++it,++bindingIndex)
    if (((*it)[1] == "OUT" || (*it)[1] == "MEM_IN") && bindingIndex < f.arg_size()) privateArguments.insert(f.getArg(bindingIndex));
  // Track caller pointer parameters through uses and defined calls. Conversion
  // alone needs no bytes; a memory access requires an actual entry snapshot.
  std::set<Value *> pointerUses;
  std::function<bool(Value *)> memoryUse=[&](Value *v) {
    if(!pointerUses.insert(v).second)return false;
    for(User *u:v->users()) {
      if(auto *l=dyn_cast<LoadInst>(u);l && l->getPointerOperand()==v)return true;
      if(auto *st=dyn_cast<StoreInst>(u);st && st->getPointerOperand()==v)return true;
      if(auto *c=dyn_cast<CallBase>(u)) {
        auto *g=c->getCalledFunction();
        if(!g || g->isDeclaration())return true;
        for(unsigned j=0;j<c->arg_size();++j)if(c->getArgOperand(j)==v && memoryUse(g->getArg(j)))return true;
      } else if(isa<Instruction>(u) && !isa<ReturnInst>(u) && memoryUse(u))return true;
    }
    return false;
  };
  if(!snapshot) for(auto &a:f.args())if(a.getType()->isPointerTy() && !privateArguments.count(&a) && memoryUse(&a))
    unimplemented("§8.5 caller pointer snapshot transfer",2,&a);
  // The closure, rather than just its root, owns writes to private globals.
  for(Function &g:m) if(!snapshot && !functions.count(&g) && !g.hasFnAttribute("bennett.stack.internal"))
    for(Instruction &i:instructions(g)) if(auto *st=dyn_cast<StoreInst>(&i))
      if(auto *v=dyn_cast<GlobalVariable>(getUnderlyingObject(st->getPointerOperand()));v && used.count(v))
        unimplemented("§8.5 caller snapshot transfer",2,&i);
  unsigned gn=1;for(GlobalVariable &g:m.globals())if(used.count(&g))s.globals[&g]="G"+std::to_string(gn++);
  if (globalNames) for (auto &g : s.globals) (*globalNames)[g.second] = scalarGlobalKey(*g.first);
  unsigned ret = s.width(f.getReturnType());
  auto semi = d.find(';');
  std::string bindings = d.substr(0, semi);
  std::string target = semi == std::string::npos ? "" : d.substr(semi + 1);
  if (!target.empty() && !std::regex_match(target,std::regex(R"(tgt=(null|[0-9]+))")))
    unimplemented("§8.3 device descriptor bindings",2,&f);
  bool discard = d == "tgt=null" || target == "tgt=null";
  unsigned tgt = ret;
  if (StringRef(target).starts_with("tgt=")) {
    auto v = StringRef(target).drop_front(4);
    if (!discard && v.getAsInteger(10, tgt))
      fail("shape", "invalid target width");
  }
  if (projection < 0 && (tgt == 0 || tgt > 128))
    unimplemented("§8.6 wide outputs", 2, &f);
  std::regex pat(R"((IN|ARG|OUT|MEM_IN)\((\d+)(?:,(zext|sext))?\))");
  std::sregex_iterator it(bindings.begin(), bindings.end(), pat), end;
  std::vector<std::string> ins, args, invoke, insWidths, paramWidths, argTypes,
      wrapperRegs, wrapperRows, mems, memSigs;
  unsigned dn = 0;
  auto prologue = [&](std::string row) {
    auto n = "d" + std::to_string(dn++);
    wrapperRegs.push_back(n + ":reg[64]");
    wrapperRows.push_back(n + " = " + row);
    return n;
  };
  auto devStore = [&](StringRef suffix, std::string value) {
    auto p = prologue("lift.addr @" + s.globals[deviceGlobal(suffix)]);
    wrapperRows.push_back("lift.boundscheck " + p + " 8");
    wrapperRows.push_back("lift.store.i64 " + p + " " + value);
  };
  if(snapshot) {
    mems.push_back("s0:region["+std::to_string(snapshot)+",8] in");
    memSigs.push_back("{\"A\":"+std::to_string(snapshot)+",\"W\":8,\"role\":\"in\"}");
    wrapperRegs.push_back("s:reg[64]");wrapperRows.push_back("s = lift.addr @s0");
    wrapperRegs.push_back("d0:reg[1]");wrapperRows.push_back("d0 = lift.call @"+functions.at(m.getFunction("__bennett_rt_entry_replay"))+" (s)");
  }
  if(initialise) {
    wrapperRegs.push_back("c0:reg[64]");wrapperRows.push_back("c0 = lift.const.i64 "+std::to_string(sstack));
    // The fixed §9.2 linked-input wrapper spells its init result d0.
    // Keep existing object bytes for all other wrappers.
    auto loc=snapshot?"d1":singleFrame?"d0":"t0";wrapperRegs.push_back(std::string(loc)+":reg[1]");
    wrapperRows.push_back(std::string(loc)+" = lift.call @"+functions.at(m.getFunction("__bennett_rt_ss_init"))+" (c0)");
  }
  std::string buffer;
  uint64_t bufferSize = 0;
  std::vector<std::pair<std::string,uint64_t>> outputBuffers;
  std::pair<std::string,uint64_t> consoleBuffer;
  for (auto &d : devices) {
  auto &device = d.first; auto deviceSize = d.second;
  if (device == "CLOCK" || device == "CLOCK_ARG") {
    auto c = device=="CLOCK" ? prologue("lift.const.i64 " + std::to_string(deviceSize)) : prologue("lift.mov clock_initial");
    if(device=="CLOCK_ARG"){args.push_back("clock_initial:i64");argTypes.push_back("\"i64\"");}
    devStore("clock_c", c);
  } else if (device == "ENTROPY") {
    if (deviceSize > 54) fail("shape", "ENTROPY extent exceeds address space");
    mems.push_back("e0:region[" + std::to_string(deviceSize) + ",8] in");
    memSigs.push_back("{\"A\":" + std::to_string(deviceSize) + ",\"W\":8,\"role\":\"in\"}");
    auto p = prologue("lift.addr @e0"); devStore("entropy_base", p);
    auto n = prologue("lift.const.i64 " + std::to_string(uint64_t(1) << deviceSize)); devStore("entropy_size", n);
    // Preserve the already published plugin bytes of an unused model binding.
    // A consuming closure (the §16.8 linked model) starts pos at its data image.
    if(!entropyPositionUsed) {auto z=prologue("lift.const.i64 0");devStore("entropy_pos",z);}

  } else if (device == "BLOCK") {
    if (deviceSize > 54) fail("shape", "BLOCK extent exceeds address space");
    mems.push_back("k0:region[" + std::to_string(deviceSize + 9) + ",8] in");
    memSigs.push_back("{\"A\":" + std::to_string(deviceSize + 9) + ",\"W\":8,\"role\":\"in\"}");
    auto p = prologue("lift.addr @k0"); devStore("block_base", p);
    auto n = prologue("lift.const.i64 " + std::to_string(uint64_t(1) << deviceSize));
    devStore("block_nsect", n);
  } else if (device == "CONSOLE") {
    auto n = prologue("lift.const.i64 " + std::to_string(deviceSize));
    devStore("console_L", n);
    buffer = prologue("lift.alloc " + n); devStore("console_buf", buffer);
    bufferSize = deviceSize; consoleBuffer = {buffer,bufferSize};
    auto z = prologue("lift.const.i64 0"); devStore("console_n", z);
    if (!deviceSize) buffer.clear();
  }
  }
  uint64_t outputBytes = consoleBuffer.second;
  unsigned idx = 0, inCount = 0, argCount = 0;
  std::string reconstructed;
  for (; it != end; ++it) {
    if (!reconstructed.empty())
      reconstructed += ",";
    reconstructed += it->str();
    if (idx >= f.arg_size())
      fail("shape", "too many scalar bindings");
    unsigned w = std::stoul((*it)[2]),
             param = s.width(f.getArg(idx)->getType());
    paramWidths.push_back(std::to_string(param));
    if ((*it)[1] == "IN") {
      if (w > param || !w)
        fail("shape", "invalid IN width");
      std::string n = "x" + std::to_string(inCount++);
      ins.push_back(n + ":wire[" + std::to_string(w) + "] in");
      insWidths.push_back(std::to_string(w));
      if (w < param) {
        auto loc = "w" + std::to_string(idx);
        wrapperRegs.push_back(loc + ":reg[" + std::to_string(param) + "]");
        wrapperRows.push_back(loc + " = lift." +
                              ((*it)[3] == "sext" ? "sext" : "zext") + ".i" +
                              std::to_string(param) + " " + n);
        n = loc;
      }
      invoke.push_back(n);
    } else if ((*it)[1] == "MEM_IN") {
      if (!f.getArg(idx)->getType()->isPointerTy() || !isPowerOf2_64(w))
        fail("shape", "MEM_IN requires a pointer and power-of-two size");
      auto n = "m" + std::to_string(idx), loc = "w" + std::to_string(idx);
      auto a = Log2_64(w);
      mems.push_back(n + ":region[" + std::to_string(a) + ",8] in");
      memSigs.push_back("{\"A\":" + std::to_string(a) + ",\"W\":8,\"role\":\"in\"}");
      wrapperRegs.push_back(loc + ":reg[64]");
      wrapperRows.push_back(loc + " = lift.addr @" + n);
      invoke.push_back(loc);
    } else if ((*it)[1] == "OUT") {
      if (!f.getArg(idx)->getType()->isPointerTy()) fail("shape", "OUT requires a pointer parameter");
      if (!buffer.empty() && projection < 0) unimplemented("§8.6 common multi-output delivery", 2, &f);
      auto c = "c" + std::to_string(idx), loc = "w" + std::to_string(idx);
      wrapperRegs.push_back(c + ":reg[64]");
      wrapperRows.push_back(c + " = lift.const.i64 " + std::to_string(w));
      wrapperRegs.push_back(loc + ":reg[64]");
      wrapperRows.push_back(loc + " = lift.alloc " + c);
      invoke.push_back(loc); buffer = loc; bufferSize = w; outputBuffers.push_back({loc,w});
      if (projection < 0) heapLimit = std::max(heapLimit, uint64_t(w));
      else { outputBytes += w; heapLimit = std::max(heapLimit,outputBytes); }
    } else {
      if (w != param)
        fail("shape", "ARG carrier width mismatch");
      std::string n = "a" + std::to_string(argCount++);
      args.push_back(n + ":i" + std::to_string(w));
      argTypes.push_back("\"i" + std::to_string(w) + "\"");
      invoke.push_back(n);
    }
    ++idx;
  }
  if (idx != f.arg_size() || (!bindings.empty() && reconstructed != bindings &&
                              bindings != "tgt=null"))
    unimplemented("§8 descriptor shape", 2, &f);
  unsigned returnTarget = tgt;
  bool returnDiscard = discard;
  if (discard)
    tgt = 1;
  auto members = scalarMembers(s, closure, analysis, functions);
  wrapperRegs.push_back("r:reg[" + std::to_string(ret) + "]");
  wrapperRows.push_back("r = lift.call @" + functions.at(&f) + " (" + join(invoke) + ")");
  if (projection >= 0) {
    if (!consoleBuffer.first.empty() && consoleBuffer.second) outputBuffers.push_back(consoleBuffer);
    std::vector<std::pair<std::string,unsigned>> projections;
    if (!returnDiscard) {
      // Return payloads use zero extension; narrowed nonzero dropped bits fault.
      auto n = std::min(returnTarget,128u);
      std::string value = "r";
      if (n != ret) {
        value = "return0"; wrapperRegs.push_back(value + ":reg[" + std::to_string(n) + "]");
        if (n < ret) {
          auto shift = "returnShift", dropped = "returnDropped", zero = "returnZero", bad = "returnBad";
          wrapperRegs.push_back(std::string(shift)+":reg["+std::to_string(ret)+"]"); wrapperRows.push_back(std::string(shift)+" = lift.const.i"+std::to_string(ret)+" "+std::to_string(n));
          wrapperRegs.push_back(std::string(dropped)+":reg["+std::to_string(ret)+"]"); wrapperRows.push_back(std::string(dropped)+" = lift.lshr r "+shift);
          wrapperRegs.push_back(std::string(zero)+":reg["+std::to_string(ret)+"]"); wrapperRows.push_back(std::string(zero)+" = lift.const.i"+std::to_string(ret)+" 0");
          wrapperRegs.push_back(std::string(bad)+":reg[1]"); wrapperRows.push_back(std::string(bad)+" = lift.icmp.ne "+dropped+" "+zero); wrapperRows.push_back(std::string("lift.faultif ")+bad+" 4");
        }
        wrapperRows.push_back(value + (n < ret ? " = lift.trunc.i" : " = lift.zext.i") + std::to_string(n) + " r");
      }
      projections.push_back({value,n});
      for (unsigned lo=128;lo<returnTarget;lo+=128) {
        auto w=std::min(128u,returnTarget-lo); auto p="return"+std::to_string(lo);
        wrapperRegs.push_back(p+":reg["+std::to_string(w)+"]");wrapperRows.push_back(p+" = lift.const.i"+std::to_string(w)+" 0");projections.push_back({p,w});
      }
    }
    for (auto &out : outputBuffers) for (uint64_t lo=0;lo<out.second;lo+=16) {
      auto bytes=std::min(uint64_t(16),out.second-lo), w=bytes*8; auto p="payload"+std::to_string(projections.size()); auto address=out.first;
      if (lo) { auto offset=prologue("lift.const.i64 "+std::to_string(lo)); address=prologue("lift.add "+out.first+" "+offset); }
      wrapperRegs.push_back(p+":reg["+std::to_string(w)+"]");wrapperRows.push_back("lift.boundscheck "+address+" "+std::to_string(bytes));
      wrapperRows.push_back(p+" = lift.load.i"+std::to_string(w)+" "+address);projections.push_back({p,unsigned(w)});
    }
    if (unsigned(projection)>=projections.size()) fail("shape","output projection index",&f);
    tgt=projections[projection].second;wrapperRows.push_back("lift.retval "+projections[projection].first);
  } else if (discard) {
    wrapperRegs.push_back("p0:reg[1]");
    wrapperRows.push_back("p0 = lift.const.i1 0");
    wrapperRows.push_back("lift.retval p0");
  } else if (!buffer.empty()) {
    if (!f.getReturnType()->isVoidTy() || bufferSize * 8 != tgt)
      unimplemented("§8.6 common multi-slice delivery", 2, &f);
    if (tgt % 8) fail("shape", "non-byte buffer delivery");
    wrapperRegs.push_back("t0:reg[" + std::to_string(tgt) + "]");
    wrapperRows.push_back("lift.boundscheck " + buffer + " " + std::to_string(tgt / 8));
    wrapperRows.push_back("t0 = lift.load.i" + std::to_string(tgt) + " " + buffer);
    wrapperRows.push_back("lift.retval t0");
  } else if (tgt != ret) {
    if(tgt<ret) {
      wrapperRegs.push_back("c0:reg["+std::to_string(ret)+"]");wrapperRows.push_back("c0 = lift.const.i"+std::to_string(ret)+" "+std::to_string(tgt));
      wrapperRegs.push_back("t0:reg["+std::to_string(ret)+"]");wrapperRows.push_back("t0 = lift.lshr r c0");
      wrapperRegs.push_back("c1:reg["+std::to_string(ret)+"]");wrapperRows.push_back("c1 = lift.const.i"+std::to_string(ret)+" 0");
      wrapperRegs.push_back("t1:reg[1]");wrapperRows.push_back("t1 = lift.icmp.ne t0 c1");wrapperRows.push_back("lift.faultif t1 4");
    }
    auto n=tgt<ret?"t2":"t0";wrapperRegs.push_back(std::string(n)+":reg["+std::to_string(tgt)+"]");
    wrapperRows.push_back(std::string(n)+" = lift."+(tgt<ret?"trunc":"zext")+".i"+std::to_string(tgt)+" r");wrapperRows.push_back(std::string("lift.retval ")+n);
  }
  else
    wrapperRows.push_back("lift.retval r");
  publishScalarObject(s, {
      std::move(ins), std::move(mems), std::move(args), std::move(wrapperRegs),
      std::move(wrapperRows), std::move(argTypes), std::move(insWidths), std::move(memSigs),
      tgt, stackCells, heapLimit, std::move(devices), std::move(members.bodies),
      std::move(members.signatures), std::move(members.text), std::move(closure)}, out);

}
} // namespace bennett
````

## `tests/normalisation_check.cpp` (66 lines)

````
// Inspect the exact module compiled by the numerical drivers, including helpers.
#include "llvm/ADT/STLExtras.h"
#include "llvm/ADT/StringSwitch.h"
#include "llvm/IR/InstIterator.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/Module.h"
#include "llvm/IRReader/IRReader.h"
#include "llvm/Support/SourceMgr.h"
#include "llvm/Support/raw_ostream.h"
#include <optional>
using namespace llvm;

// Dialect §12.4 V14 caps scalar values; N25 makes memory accesses byte-sized.
constexpr unsigned MaxScalarBits = 128;
constexpr unsigned ByteBits = 8;

bool residueType(Type *type, bool memory) {
  if (type->isVectorTy()) return true;
  if (auto *integer = dyn_cast<IntegerType>(type))
    return integer->getBitWidth() > MaxScalarBits || (memory && integer->getBitWidth() % ByteBits);
  if (auto *structure = dyn_cast<StructType>(type))
    return any_of(structure->elements(), [&](Type *element) { return residueType(element, memory); });
  if (auto *array = dyn_cast<ArrayType>(type)) return residueType(array->getElementType(), memory);
  return false;
}

bool checkFunction(Function &function, bool byteMemory) {
  if (residueType(function.getReturnType(), false)) return false;
  for (auto &argument : function.args())
    if (residueType(argument.getType(), false)) return false;
  for (auto &instruction : instructions(function)) {
    if (auto *call = dyn_cast<CallBase>(&instruction))
      if (auto *callee = call->getCalledFunction(); callee && callee->isIntrinsic()) return false;
    if (residueType(instruction.getType(), byteMemory && isa<LoadInst>(instruction))) return false;
    for (auto &operand : instruction.operands())
      if (residueType(operand->getType(), byteMemory && isa<StoreInst>(instruction))) return false;
  }
  return true;
}

int main(int argc, char **argv) {
  if (argc != 3) {
    errs() << "usage: normalisation_check <module.ll> <values|byte-memory>\n";
    return 2;
  }
  auto byteMemory = StringSwitch<std::optional<bool>>(argv[2])
      .Case("values", false).Case("byte-memory", true).Default(std::nullopt);
  if (!byteMemory) {
    errs() << "unknown memory representation: " << argv[2] << "\n";
    return 2;
  }
  LLVMContext context;
  SMDiagnostic diagnostic;
  auto module = parseIRFile(argv[1], diagnostic, context);
  if (!module) {
    diagnostic.print(argv[0], errs());
    return 2;
  }
  for (auto &function : *module)
    if (!function.isDeclaration() && !checkFunction(function, *byteMemory)) {
      errs() << "normalisation residue: " << function.getName()
             << " in " << argv[1] << " (intrinsic, vector, wide value or non-byte memory)\n";
      return 1;
    }
  return 0;
}
````

## `tests/normalisation_scope.py` (91 lines)

````python
#!/usr/bin/env python3
"""Mutate the real numerical suites to prove their structural checks see residue."""

import argparse
from contextlib import redirect_stdout
import io
from pathlib import Path
import re
import runpy
import sys

import contracts


CASES = {
    "integer-call": ("integer_intrinsics", "integer-intrinsics", "f8_cttz"),
    "integer-vector": ("integer_intrinsics", "integer-intrinsics", "vf16_ctpop"),
    "integer-helper": ("integer_intrinsics", "integer-intrinsics", None),
    "wide-memory": ("wide", "wide", "nonbyte"),
    "memory-call": ("memory_runtime", "memory-runtime", "memmove"),
}


def mutation(source, output, name):
    # Regexes select mutations only; the verifier parses the complete LLVM module.
    if name is None:
        changed, count = re.subn(
            r"(define i1 @__bennett_rt_ctpop_i1[^\n]*\{\nentry:\n)",
            r"\1  %residual.mutation = call i8 @llvm.cttz.i8(i8 1, i1 false)\n",
            output,
            count=1,
        )
    else:
        pattern = rf"define [^\n]*@{name}\([^}}]*}}"
        raw = re.search(pattern, source)
        assert raw is not None, name
        changed, count = re.subn(pattern, lambda match: raw.group(), output)
    assert count == 1 and changed != output, (name, count)
    return changed


def check_case(major, label):
    driver, directory, name = CASES[label]
    target = contracts.ROOT / f".tmp/{directory}/{major}/out.ll"
    original_run, original_args = contracts.run_checked, sys.argv
    snapshots = []

    def intercept(command, **kwargs):
        result = original_run(command, **kwargs)
        arguments = list(map(str, command))
        if "-bennett-normalise-only" in arguments and "-o" in arguments:
            output = Path(arguments[arguments.index("-o") + 1])
            if output == target:
                memory = "byte-memory" if driver == "wide" else "values"
                contracts.validate_normalisation(major, output, memory)
                text = output.read_text()
                snapshots.append(text)
                output.write_text(mutation((output.parent / "in.ll").read_text(), text, name))
        return result

    contracts.run_checked = intercept
    sys.argv = [driver, "--major", str(major)]
    try:
        with redirect_stdout(io.StringIO()):
            try:
                runpy.run_path(str(contracts.ROOT / f"tests/{driver}.py"), run_name="__main__")
            except AssertionError as error:
                expected = name or "__bennett_rt_ctpop_i1"
                assert len(snapshots) == 1 and f"normalisation residue: {expected} " in str(error), str(error)
            else:
                assert snapshots, f"{label}: no output was mutated"
                raise AssertionError(f"{label}: suite accepted residue in its real output")
    finally:
        contracts.run_checked, sys.argv = original_run, original_args
        if snapshots:
            target.write_text(snapshots[0])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--major", type=int, required=True, choices=(18, 23))
    parser.add_argument("--case", choices=CASES)
    args = parser.parse_args()
    cases = [args.case] if args.case else CASES
    for label in cases:
        check_case(args.major, label)
    print(f"LLVM {args.major}: rejected {len(cases)}/{len(cases)} real-module mutations")


if __name__ == "__main__":
    main()
````

## `tests/review_regressions.py` (1001 lines)

````python
#!/usr/bin/env python3
"""Correct-result regressions for the plugin batch review."""

import argparse
import json
import os
from pathlib import Path
import subprocess

from contracts import ROOT, sibling

REF = sibling("bennett-isa-spec") / "reference-interpreter/target/debug/bennett-isa-ref"


from contracts import run_checked as run


def global_cases(case, command, tool, work):
    rows, failures = [], []
    original = (ROOT / "tests/probes/review-global-counter.ll").read_text()
    extra_entry = original + original[
        original.index("define i32 @top()") :
    ].replace("@top()", "@other()")
    helper = original.replace("@top()", "@helper()")
    prefix, helper_body = helper.split("define i32 @helper()", 1)
    top = """define i32 @top() {
 %q = call ptr @__bennett_qalloc(i64 0, i64 1)
 call void @__bennett_qfree(ptr %q)
 %v = call i32 @helper()
 ret i32 %v
}
"""
    for name, body, actions, expected in [
        (
            "repeat",
            original,
            "unsigned a=top(), b=top();",
            "1 2 host_global=2\n",
        ),
        (
            "host-write",
            original,
            "unsigned a=top(); g=40; unsigned b=top();",
            "1 41 host_global=41\n",
        ),
        (
            "two-entries",
            extra_entry,
            "unsigned a=top(), b=other();",
            "1 2 host_global=2\n",
        ),
        (
            "helper-first",
            helper + top,
            "unsigned a=top(), b=top();",
            "1 2 host_global=2\n",
        ),
        (
            "top-first",
            prefix + top + "define i32 @helper()" + helper_body,
            "unsigned a=top(), b=top();",
            "1 2 host_global=2\n",
        ),
    ]:
        directory = work / case / name
        directory.mkdir(parents=True, exist_ok=True)
        source, harness = directory / "input.ll", directory / "main.c"
        source.write_text(body)
        harness.write_text(
            "#include <stdio.h>\nextern unsigned top(void), other(void), g;\n"
            "int main(void) {"
            + actions
            + 'printf("%u %u host_global=%u\\n",a,b,g); return 0;}\n'
            + "void *__bennett_qalloc(unsigned long long c,unsigned long long n){return 0;}\n"
            + "void __bennett_qfree(void *p){}\n"
        )
        native = directory / "source-native"
        run([tool + "clang", source, harness, "-o", native])
        baseline = run([native])
        assert baseline.stdout == expected, (name, baseline.stdout, expected)
        run([*command, "-bennett-out=" + str(directory), source])
        run(
            [
                tool + "opt",
                "-passes=verify",
                "-disable-output",
                directory / "host.bc",
            ]
        )
        library = sibling("bennett-vm") / "target/debug"
        executable = directory / "counter"
        run(
            [
                tool + "clang",
                directory / "host.bc",
                harness,
                "-L" + str(library),
                "-Wl,-rpath," + str(library),
                "-lbennett_vm",
                "-o",
                executable,
            ]
        )
        environment = dict(
            os.environ,
            BENNETT_TARGET=(
                ROOT / "tests/probes/review-launch-target.json"
            ).read_text(),
        )
        actual = subprocess.run(
            [str(executable)],
            capture_output=True,
            text=True,
            env=environment,
            timeout=120,
        )
        if case == "global-diagnostic":
            ok = (
                actual.returncode == 125
                and not actual.stdout
                and all(
                    text in actual.stderr
                    for text in (
                        "bp-acm",
                        "b-dialect-spec-6u6",
                        "promised",
                        "pending",
                    )
                )
                and "unsupported" not in actual.stderr.lower()
            )
        else:
            ok = actual.returncode == 0 and actual.stdout == expected
        rows.append(
            dict(
                case=case,
                name=name,
                expected=expected,
                actual=actual.stdout,
                exit=actual.returncode,
                stderr=actual.stderr,
                ok=ok,
            )
        )
        if not ok:
            failures.append(rows[-1])
    return rows, failures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--major", type=int, required=True, choices=(18, 23))
    parser.add_argument(
        "--plugin", type=Path, help="Use an explicitly selected instrumentation build"
    )
    parser.add_argument(
        "--promised-bp-acm",
        action="store_true",
        help="Run the promised shared-global semantics pending the native-sharing contract",
    )
    parser.add_argument(
        "--case",
        action="append",
        choices=(
            "shuffle",
            "byval",
            "global-counter",
            "global-diagnostic",
            "byte-order",
            "native-abi",
            "block-order",
            "control",
            "dynamic-gate",
            "mixed-native",
            "unresolved-call",
        ),
    )
    args = parser.parse_args()
    tool = f"/usr/lib/llvm-{args.major}/bin/"
    plugin = args.plugin or ROOT / f"build/libbennett-plugin-{args.major}.so"
    work = ROOT / f".tmp/review-regressions/{args.major}"
    work.mkdir(parents=True, exist_ok=True)
    command = [
        tool + "opt",
        "-load-pass-plugin=" + str(plugin),
        "-passes=bennett",
        "-bennett-dialect=0.2.13",
        "-disable-output",
    ]
    rows = []
    failures = []
    if args.case and "global-counter" in args.case and not args.promised_bp_acm:
        parser.error(
            "global-counter requires --promised-bp-acm; native sharing is promised and pending"
        )
    for case in args.case or ("shuffle", "byval", "global-diagnostic"):
        if case == "unresolved-call":
            original = (ROOT / "tests/probes/review-host-import.ll").read_text()
            successor = original.replace(
                " ret i32 %z", " br label %after\nafter:\n ret i32 %z"
            )
            after_call = original.replace(
                " ret i32 %z",
                " %next = add i32 %x, 1\n br label %after\nafter:\n ret i32 %next",
            )
            indirect = original.replace(" %safe =", " %safe =", 1).replace(
                " br i1 %safe",
                " %callee = select i1 %safe, ptr @identity, ptr @host_fn\n br i1 %safe",
            )
            indirect = indirect.replace(
                "call i32 @host_fn(i32 %x)", "call i32 %callee(i32 %x)"
            )
            indirect += "\ndefine internal i32 @identity(i32 %x) { ret i32 %x }\n"
            start = original.index(" %safe =")
            helper = (
                original[: original.index("define i32 @top")]
                + """define i32 @top(i32 %x) {
 %q = call ptr @__bennett_qalloc(i64 0,i64 1)
 call void @__bennett_qfree(ptr %q)
 %value = call i32 @helper(i32 %x)
 ret i32 %value
}
define internal i32 @helper(i32 %x) {
"""
                + original[start:]
            )
            for name, body in [
                ("review", original),
                ("successor", successor),
                ("after-call", after_call),
                ("indirect", indirect),
                ("callee", helper),
            ]:
                directory = work / case / name
                directory.mkdir(parents=True, exist_ok=True)
                source = directory / "input.ll"
                source.write_text(body)
                run([*command, "-bennett-out=" + str(directory), source])
                obj = directory / "top/launch.bennett"
                run([REF, "check", obj])
                safe = json.loads(
                    run(
                        [
                            REF,
                            "run-program",
                            obj,
                            "top",
                            "--args",
                            "0",
                            "--budget",
                            "1000,0,32,32",
                            "--reverse",
                        ]
                    ).stdout
                )
                assert (
                    safe["status"] == "REVERSED"
                    and safe["results"] == [{"type": "i32", "value": "7"}]
                    and safe["equals_entry"]
                ), safe
                assert not safe["host_requests"], safe
                replies = directory / "replies.json"
                replies.write_text(
                    json.dumps(
                        [
                            dict(
                                service="bennett.fault",
                                payload="0800000000000000",
                                reply="",
                            )
                        ]
                    )
                )
                reached = json.loads(
                    run(
                        [
                            REF,
                            "run-program",
                            obj,
                            "top",
                            "--args",
                            "1",
                            "--budget",
                            "1000,0,32,32",
                            "--replies",
                            replies,
                        ]
                    ).stdout
                )
                assert (
                    reached["status"] == "FAILED"
                    and reached["host_requests"][0]["service"] == "bennett.fault"
                ), reached
                assert (
                    reached["host_requests"][0]["payload"] == "0800000000000000"
                ), reached
                for filename in ("coverage.json", "all-coverage.json"):
                    coverage = json.loads((directory / "top" / filename).read_text())
                    assert any(
                        row["classification"] == "trapped"
                        and "host_fn" in row["reason"]
                        for row in coverage["entries"]
                    ), (name, filename, coverage)
                rows.append(dict(case=case, name=name, safe=safe, reached=reached))
        if case == "mixed-native":
            original = (ROOT / "tests/probes/review-mixed-native.ll").read_text()
            for name, body in [
                ("review", original),
                (
                    "host-fp",
                    original + """
define double @native_fp(double %a,double %b) {
 %sum = fadd double %a,%b
 ret double %sum
}
""",
                ),
            ]:
                directory = work / case / name
                directory.mkdir(parents=True, exist_ok=True)
                source = directory / "input.ll"
                source.write_text(body)
                run([*command, "-bennett-out=" + str(directory), source])
                run(
                    [
                        tool + "opt",
                        "-passes=verify",
                        "-disable-output",
                        directory / "host.bc",
                    ]
                )
                harness = directory / "native.c"
                floating = "" if name != "host-fp" else (
                    "if(native_fp(1.5,2.25)!=3.75 || native_fp(-4.0,1.0)!=-3.0 "
                    "|| native_fp(0.0,0.0)!=0.0) return 2;"
                )
                harness.write_text(
                    "#include <stdbool.h>\nextern bool native_only(void *);\n"
                    "extern double native_fp(double,double);\nint main(void) {"
                    "for(unsigned x=0;x<256;++x) { unsigned char p[16]={x};"
                    "if(native_only(p)!=(bool)(x&1)) return 1;}" + floating + "return 0;}\n"
                )
                library = sibling("bennett-vm") / "target/debug"
                executable = directory / "native"
                run([tool + "clang", directory / "host.bc", harness,
                     "-L" + str(library), "-Wl,-rpath," + str(library), "-lbennett_vm", "-o", executable])
                run([executable])
                obj = directory / "top/launch.bennett"
                run([REF, "check", obj])
                result = json.loads(
                    run(
                        [
                            REF,
                            "run-program",
                            obj,
                            "top",
                            "--args",
                            "37",
                            "--budget",
                            "1000,0,0,0",
                            "--reverse",
                        ]
                    ).stdout
                )
                assert (
                    result["status"] == "REVERSED"
                    and result["equals_entry"]
                    and result["results"] == [{"type": "i8", "value": "37"}]
                ), result
                rows.append(dict(case=case, name=name, actual=result))
            directory = work / case / "device-fp"
            directory.mkdir(parents=True, exist_ok=True)
            source = directory / "input.ll"
            source.write_text(
                original.replace("-i64:64-f80:", "-i64:64-i128:128-f80:") + """
define double @device_fp(double %x) {
 %sum = fadd double %x, 2.000000e+00
 ret double %sum
}
!llvm.module.flags = !{!0}
!0 = !{i32 1, !"bennett.sstack", i64 4096}
"""
            )
            run(
                [
                    *command,
                    "-bennett-oracle=device_fp",
                    "-bennett-analysis-budget-ms=120000",
                    "-bennett-scalar-shape=IN(64,zext);tgt=64",
                    "-bennett-scalar-stack=262144",
                    "-bennett-scalar-heap=65536",
                    "-bennett-out=" + str(directory),
                    source,
                ]
            )
            obj = directory / "ref.bennett"
            run([REF, "check", obj])
            # The published add closure has over 114k location cells. Its
            # exercised call chain exceeds 65,536 cells; retain that boundary
            # and give the successful numerical witness a sufficient stack.
            numerical_ref = (
                sibling("bennett-isa-spec")
                / "reference-interpreter/target/release/bennett-isa-ref"
            )
            boundary = json.loads(
                run(
                    [
                        numerical_ref,
                        "run-oracle",
                        obj,
                        "ref",
                        "--input",
                        "4607182418800017408",
                        "--budget",
                        "1000000,65536,65536,128",
                    ]
                ).stdout
            )
            assert boundary["code"] == 3 and boundary["payload"] == 0, boundary
            result = json.loads(
                run(
                    [
                        numerical_ref,
                        "run-oracle",
                        obj,
                        "ref",
                        "--input",
                        "4607182418800017408",
                        "--budget",
                        "1000000,65536,262144,128",
                    ]
                ).stdout
            )
            assert (
                result["code"] == 0 and int(result["payload"]) == 4613937818241073152
            ), result
            rows.append(
                dict(case=case, name="device-fp", actual=result, small_stack=boundary)
            )
        if case == "dynamic-gate":
            original = (ROOT / "tests/probes/review-dynamic-gate.ll").read_text()
            directory = work / case
            directory.mkdir(parents=True, exist_ok=True)
            run(
                [
                    *command,
                    "-bennett-out=" + str(directory / "review"),
                    ROOT / "tests/probes/review-dynamic-gate.ll",
                ]
            )
            body = original.replace(
                "top(i32 %op)", "top(i32 %op, i32 %inverse, i64 %index)"
            )
            body = body.replace("qalloc(i64 0, i64 1)", "qalloc(i64 0, i64 2)")
            body = body.replace(
                "call void @__bennett_gate(i32 %op, ptr %q, i64 0)",
                "call void @__bennett_gate(i32 %op, ptr %q, i64 %index)\n"
                "call void @__bennett_gate(i32 %inverse, ptr %q, i64 %index)",
            )
            source = directory / "input.ll"
            source.write_text(body)
            run([*command, "-bennett-out=" + str(directory), source])
            obj = directory / "top/launch.bennett"
            run([REF, "check", obj])
            for op, inverse in [
                (1, 1),
                (2, 2),
                (3, 4),
                (4, 3),
                (5, 6),
                (6, 5),
                (7, 7),
                (8, 8),
            ]:
                for index in (0, 1):
                    result = json.loads(
                        run(
                            [
                                REF,
                                "run-program",
                                obj,
                                "top",
                                "--args",
                                f"{op},{inverse},{index}",
                                "--budget",
                                "1000,0,0,0",
                                "--reverse",
                            ]
                        ).stdout
                    )
                    assert (
                        result["status"] == "REVERSED"
                        and result["equals_entry"]
                        and not result["faults"]
                    ), result
                    rows.append(dict(case=case, op=op, index=index, actual=result))
            for inputs in ("0,1,0", "9,1,0", "1,1,2", "1,1,18446744073709551615"):
                result = json.loads(
                    run(
                        [
                            REF,
                            "run-program",
                            obj,
                            "top",
                            "--args",
                            inputs,
                            "--budget",
                            "1000,0,0,0",
                        ]
                    ).stdout
                )
                assert result["status"] == "FAILED", result
                rows.append(dict(case=case, invalid=inputs, actual=result))
            measured = directory / "measured.ll"
            measured.write_text("""target datalayout = "e-p:64:64"
declare ptr @__bennett_qalloc(i64,i64)
declare void @__bennett_qfree(ptr)
declare void @__bennett_gate(i32,ptr,i64)
declare i1 @__bennett_measure(ptr,i64)
define i1 @top(i64 %index) {
 %q = call ptr @__bennett_qalloc(i64 0,i64 2)
 call void @__bennett_gate(i32 1,ptr %q,i64 %index)
 %value = call i1 @__bennett_measure(ptr %q,i64 %index)
 call void @__bennett_gate(i32 1,ptr %q,i64 %index)
 call void @__bennett_qfree(ptr %q)
 ret i1 %value
}
""")
            dest = directory / "measured"
            run([*command, "-bennett-out=" + str(dest), measured])
            obj = dest / "top/launch.bennett"
            run([REF, "check", obj])
            for index in (0, 1):
                result = json.loads(
                    run(
                        [
                            REF,
                            "run-program",
                            obj,
                            "top",
                            "--args",
                            str(index),
                            "--budget",
                            "1000,0,0,0",
                        ]
                    ).stdout
                )
                assert result["status"] == "COMPLETED" and result["results"] == [
                    {"type": "i1", "value": "1"}
                ], result
                rows.append(dict(case=case, measurement_index=index, actual=result))
        if case == "control":
            original = (ROOT / "tests/probes/review-control.ll").read_text()
            declaration = "declare void @__bennett_gate(i32, ptr, i64)\n"
            for name, body, valid in [
                ("review", original, True),
                (
                    "superposition",
                    original.replace(
                        "call void @__bennett_ctrl",
                        "call void @__bennett_gate(i32 2, ptr %q, i64 0)\ncall void @__bennett_ctrl",
                    ).replace(
                        "call void @__bennett_qfree",
                        "call void @__bennett_gate(i32 2, ptr %q, i64 0)\ncall void @__bennett_qfree",
                    )
                    + declaration,
                    True,
                ),
                (
                    "index-outside",
                    original.replace("ctrl(ptr %q, i64 0", "ctrl(ptr %q, i64 1"),
                    False,
                ),
                (
                    "dead-control",
                    original.replace(
                        "call void @__bennett_ctrl",
                        "call void @__bennett_qfree(ptr %q)\ncall void @__bennett_ctrl",
                    ),
                    False,
                ),
            ]:
                directory = work / case / name
                directory.mkdir(parents=True, exist_ok=True)
                source = directory / "input.ll"
                source.write_text(body)
                run([*command, "-bennett-out=" + str(directory), source])
                obj = directory / "top/launch.bennett"
                run([REF, "check", obj])
                result = json.loads(
                    run(
                        [
                            REF,
                            "run-program",
                            obj,
                            "top",
                            "--budget",
                            "1000,0,0,0",
                            *(["--reverse"] if valid else []),
                        ]
                    ).stdout
                )
                if valid:
                    assert (
                        result["status"] == "REVERSED"
                        and result["equals_entry"]
                        and not result["faults"]
                    ), result
                    assert "action_call @" in obj.read_text(), obj.read_text()
                    build = json.loads((directory / "top/build.json").read_text())
                    assert (
                        build["controlled_identity_proofs"][0]["generation_steps"] == 1
                    ), build
                else:
                    assert result["status"] == "FAILED", result
                rows.append(dict(case=case, name=name, actual=result))
        if case == "block-order":
            directory = work / case
            run(
                [
                    *command,
                    "-bennett-out=" + str(directory),
                    ROOT / "tests/probes/review-block-order.ll",
                ]
            )
            obj = directory / "top/launch.bennett"
            run([REF, "check", obj])
            for value in (0, 7, 255):
                result = json.loads(
                    run(
                        [
                            REF,
                            "run-program",
                            obj,
                            "top",
                            "--args",
                            str(value),
                            "--budget",
                            "1000,0,0,0",
                            "--reverse",
                        ]
                    ).stdout
                )
                assert (
                    result["status"] == "REVERSED"
                    and result["results"]
                    == [{"type": "i8", "value": str((value + 3) % 256)}]
                    and result["equals_entry"]
                ), result
                rows.append(dict(case=case, input=value, actual=result))
        if case == "native-abi":
            original = (ROOT / "tests/probes/review-pointer-abi.ll").read_text()
            for name, body in [
                ("pointer", original),
                (
                    "pointer-result",
                    original.replace("define i8 @top", "define ptr @top").replace(
                        "ret i8 %x", "ret ptr %p"
                    ),
                ),
                (
                    "aggregate",
                    original.replace("i8 @top(ptr %p)", "{i8,i16} @top({i8,i16} %p)")
                    .replace("%x = load i8, ptr %p", "")
                    .replace("ret i8 %x", "ret {i8,i16} %p"),
                ),
                (
                    "float",
                    original.replace("i8 @top(ptr %p)", "float @top(float %p)")
                    .replace("%x = load i8, ptr %p", "")
                    .replace("ret i8 %x", "ret float %p"),
                ),
                (
                    "big-i24",
                    original.replace('"e-', '"E-')
                    .replace("i8 @top(ptr %p)", "i24 @top(i24 %p)")
                    .replace("%x = load i8, ptr %p", "")
                    .replace("ret i8 %x", "ret i24 %p"),
                ),
            ]:
                directory = work / case / name
                directory.mkdir(parents=True, exist_ok=True)
                source = directory / "input.ll"
                source.write_text(body)
                run([*command, "-bennett-out=" + str(directory), source])
                host = run(
                    [
                        tool + "opt",
                        "-passes=verify",
                        "-S",
                        directory / "host.bc",
                        "-o",
                        "-",
                    ]
                )
                if name == "pointer":
                    assert "ptrtoint ptr %p to i64" in host.stdout, host.stdout
                if name == "pointer-result":
                    assert "inttoptr i64" in host.stdout, host.stdout
                run([REF, "check", directory / "top/launch.bennett"])
                if name in ("aggregate", "float"):
                    harness = directory / "main.ll"
                    if name == "float":
                        harness.write_text("""declare float @top(float)
define i32 @main() {
 %value = call float @top(float 1.250000e+00)
 %ok = fcmp oeq float %value, 1.250000e+00
 %status = select i1 %ok, i32 0, i32 1
 ret i32 %status
}
""")
                    else:
                        harness.write_text("""declare {i8,i16} @top({i8,i16})
define i32 @main() {
 %value = call {i8,i16} @top({i8,i16} {i8 7,i16 300})
 %a = extractvalue {i8,i16} %value, 0
 %b = extractvalue {i8,i16} %value, 1
 %aok = icmp eq i8 %a, 7
 %bok = icmp eq i16 %b, 300
 %ok = and i1 %aok, %bok
 %status = select i1 %ok, i32 0, i32 1
 ret i32 %status
}
""")
                    library = sibling("bennett-vm") / "target/debug"
                    executable = directory / "native"
                    run(
                        [
                            tool + "clang",
                            directory / "host.bc",
                            harness,
                            "-L" + str(library),
                            "-Wl,-rpath," + str(library),
                            "-lbennett_vm",
                            "-o",
                            executable,
                        ]
                    )
                    environment = dict(
                        os.environ,
                        BENNETT_TARGET=(
                            ROOT / "tests/probes/review-launch-target.json"
                        ).read_text(),
                    )
                    actual = subprocess.run(
                        [str(executable)],
                        capture_output=True,
                        text=True,
                        env=environment,
                        timeout=120,
                    )
                    assert actual.returncode == 0, (
                        name,
                        actual.returncode,
                        actual.stderr,
                    )
                rows.append(dict(case=case, name=name, host_verified=True))
        if case == "byte-order":
            for endian in ("e", "E"):
                for operation in ("load", "store"):
                    directory = work / case / (endian + "-" + operation)
                    directory.mkdir(parents=True, exist_ok=True)
                    source = directory / "input.ll"
                    body = "%value = load i16, ptr @g\n ret i16 %value"
                    expected = 258
                    if operation == "store":
                        body = """store i16 258, ptr @g
 %first = load i8, ptr @g
 %secondp = getelementptr i8, ptr @g, i64 1
 %second = load i8, ptr %secondp
 %hi = zext i8 %first to i16
 %lo = zext i8 %second to i16
 %upper = shl i16 %hi, 8
 %value = or i16 %upper, %lo
 ret i16 %value"""
                        expected = 258 if endian == "E" else 513
                    source.write_text(
                        f"""target datalayout = "{endian}-p:64:64-i64:64-n8:16:32:64"
@g = internal global i16 258
define i16 @oracle() {{
 {body}
}}
declare ptr @__bennett_qalloc(i64,i64)
declare void @__bennett_qfree(ptr)
define i16 @top() {{
 %q = call ptr @__bennett_qalloc(i64 0, i64 1)
 call void @__bennett_qfree(ptr %q)
 %v = call i16 @oracle()
 ret i16 %v
}}
"""
                    )
                    for tier in ("L", "CC"):
                        dest = directory / tier
                        flags = (
                            ["-bennett-oracle=oracle", "-bennett-scalar-shape=;tgt=16"]
                            if tier == "L"
                            else []
                        )
                        run([*command, *flags, "-bennett-out=" + str(dest), source])
                        obj = dest / (
                            "ref.bennett" if tier == "L" else "top/launch.bennett"
                        )
                        run([REF, "check", obj])
                        execution = (
                            [REF, "run-oracle", obj, "ref", "--input", ""]
                            if tier == "L"
                            else [REF, "run-program", obj, "top"]
                        )
                        result = json.loads(
                            run([*execution, "--budget", "1000,0,32,32"]).stdout
                        )
                        actual = (
                            result["payload"]
                            if tier == "L"
                            else int(result["results"][0]["value"])
                        )
                        assert actual == expected and (result.get("code", 0) == 0), (
                            endian,
                            operation,
                            tier,
                            expected,
                            result,
                        )
                        rows.append(
                            dict(
                                case=case,
                                endian=endian,
                                operation=operation,
                                tier=tier,
                                actual=actual,
                            )
                        )
        if case in ("global-counter", "global-diagnostic"):
            global_rows, global_failures = global_cases(case, command, tool, work)
            rows.extend(global_rows)
            failures.extend(global_failures)
        if case == "byval":
            original = (ROOT / "tests/probes/review-byval.ll").read_text()
            duplicate = original.replace(
                "void @mutate(ptr byval(i8) %p)",
                "i8 @mutate(ptr byval(i8) %p, ptr byval(i8) %other)",
            )
            duplicate = duplicate.replace(
                " ret void", " %before = load i8, ptr %other\n ret i8 %before"
            )
            duplicate = duplicate.replace(
                "call void @mutate(ptr byval(i8) %x)",
                "%before = call i8 @mutate(ptr byval(i8) %x, ptr byval(i8) %x)",
            )
            duplicate = duplicate.replace(
                " ret i8 %v", " %sum = add i8 %v, %before\n ret i8 %sum"
            )
            indirect = original.replace(
                "define i8 @top()", "define i8 @top(i1 %choose)"
            )
            indirect = indirect.replace(
                " call void @mutate(ptr byval(i8) %x)",
                " %callee = select i1 %choose, ptr @mutate, ptr @other\n"
                " call void %callee(ptr byval(i8) %x)",
            )
            indirect += "\ndefine internal void @other(ptr byval(i8) %p) {\n store i8 12, ptr %p\n ret void\n}\n"
            for name, body, width, expected in [
                ("review", original, 8, 7),
                (
                    "two-bytes",
                    original.replace("i8", "i16").replace("i16 7", "i16 258"),
                    16,
                    258,
                ),
                ("independent-copies", duplicate, 8, 14),
                ("indirect-0", indirect, 8, 7),
                ("indirect-1", indirect, 8, 7),
            ]:
                directory = work / case / name
                directory.mkdir(parents=True, exist_ok=True)
                source = directory / "input.ll"
                source.write_text(body)
                run([*command, "-bennett-out=" + str(directory), source])
                obj = directory / "top/launch.bennett"
                run([REF, "check", obj])
                for reverse in ([], ["--reverse"]):
                    inputs = (
                        ["--args", name[-1]] if name.startswith("indirect-") else []
                    )
                    result = json.loads(
                        run(
                            [
                                REF,
                                "run-program",
                                obj,
                                "top",
                                "--budget",
                                "1000,16,32,32",
                                *inputs,
                                *reverse,
                            ]
                        ).stdout
                    )
                    assert result["status"] == (
                        "REVERSED" if reverse else "COMPLETED"
                    ) and result["results"] == [
                        {"type": f"i{width}", "value": str(expected)}
                    ], result
                    if reverse:
                        assert (
                            result["equals_entry"] and result["memory_equals_entry"]
                        ), result
                    rows.append(dict(case=case, name=name, actual=result))
        if case == "shuffle":
            cases = [("review", None, 7, 8)]
            for mask, expected in (
                ("undef, i32 1", 0x0907),
                ("poison, i32 3", 0x0D07),
                ("2, i32 undef", 0x070B),
            ):
                cases.append(("lanes-" + str(len(cases)), mask, expected, 16))
            for name, mask, expected, width in cases:
                directory = work / case / name
                directory.mkdir(parents=True, exist_ok=True)
                source = ROOT / "tests/probes/review-shuffle.ll"
                if mask is not None:
                    source = directory / "input.ll"
                    source.write_text("""target datalayout = "e-p:64:64"
define i16 @oracle() {
 %vec = shufflevector <2 x i8> <i8 7, i8 9>, <2 x i8> <i8 11, i8 13>, <2 x i32> <i32 MASK>
 %a = extractelement <2 x i8> %vec, i32 0
 %b = extractelement <2 x i8> %vec, i32 1
 %lo = zext i8 %a to i16
 %hi = zext i8 %b to i16
 %upper = shl i16 %hi, 8
 %result = or i16 %lo, %upper
 ret i16 %result
}
""".replace("MASK", mask))
                report = directory / "analysis.json"
                run(
                    [
                        *command,
                        "-bennett-analysis-only",
                        "-bennett-report=" + str(report),
                        source,
                    ]
                )
                if mask is None:
                    values = json.loads(report.read_text())["values"]
                    assert any(
                        v["value"] == "%v" and v["atoms"] == ["INT(7)"] and not v["top"]
                        for v in values
                    )
                run(
                    [
                        *command,
                        "-bennett-oracle=oracle",
                        f"-bennett-scalar-shape=;tgt={width}",
                        "-bennett-out=" + str(directory),
                        source,
                    ]
                )
                obj = directory / "ref.bennett"
                run([REF, "check", obj])
                result = json.loads(
                    run(
                        [
                            REF,
                            "run-oracle",
                            obj,
                            "ref",
                            "--input",
                            "",
                            "--budget",
                            "1000,0,32,32",
                        ]
                    ).stdout
                )
                assert result["code"] == 0 and result["payload"] == expected, (
                    name,
                    expected,
                    result,
                )
                rows.append(
                    dict(case=case, name=name, expected=expected, actual=result)
                )
    result = dict(
        major=args.major,
        cases=len(rows),
        passed=len(rows) - len(failures),
        results=rows,
    )
    receipt = json.dumps(result, indent=2) + "\n"
    (ROOT / f".tmp/review-regressions-{args.major}.json").write_text(receipt)
    if args.case:
        (
            ROOT / f'.tmp/review-regressions-{"-".join(args.case)}-{args.major}.json'
        ).write_text(receipt)
    print(json.dumps(dict(major=args.major, cases=len(rows), passed=result["passed"])))
    assert not failures, failures


if __name__ == "__main__":
    main()
````
