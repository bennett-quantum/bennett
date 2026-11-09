#!/usr/bin/env bash
# Installation plans come from the doctor, so detection and verification cannot drift.
set -euo pipefail
unset DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER
exec python3 - "$0" "$@" <<'PY'
import json
from pathlib import Path
import shlex
import subprocess
import sys

script = Path(sys.argv.pop(1)).resolve().with_name("doctor.sh")
args = sys.argv[1:]
apply = "--sudo" in args
args = [arg for arg in args if arg != "--sudo"]
if "--help" in args or "-h" in args:
    print("Usage: bootstrap-host.sh [--sudo] [--workspace DIR] [--manifest FILE]\n"
          "Default: print missing-prerequisite install steps, without installing.\n"
          "--sudo: execute supported steps and require doctor.sh to verify afterwards.")
    sys.exit(0)
if "--json" in args:
    sys.exit("bootstrap-host: use doctor.sh --json to inspect the plan")
probe = subprocess.run(["/bin/bash", str(script), *args, "--json"],
                       stdin=subprocess.DEVNULL, capture_output=True, text=True)
if probe.returncode not in (0, 1):
    sys.stderr.write(probe.stderr)
    sys.exit(probe.returncode)
try:
    report = json.loads(probe.stdout)
except ValueError:
    sys.exit(f"bootstrap-host: invalid doctor output: {probe.stdout}\n{probe.stderr}")
steps = []
for gap in report["gaps"]:
    print(f"GAP {gap['label']}: {gap['reason']}")
    if not gap["install"]:
        print("  Manual repair required; no verified automatic provider.")
    for step in gap["install"]:
        if step not in steps:
            steps.append(step)
            print("  " + shlex.join(step))
sys.stdout.flush()
if apply:
    for step in steps:
        try:
            result = subprocess.run(step, stdin=subprocess.DEVNULL)
        except OSError as error:
            sys.exit(f"bootstrap-host: {shlex.join(step)}: {error}")
        if result.returncode:
            sys.exit(f"bootstrap-host: install failed ({result.returncode}): {shlex.join(step)}")
    # Installation exiting zero is never evidence that the gap was repaired.
    sys.exit(subprocess.run(["/bin/bash", str(script), *args], stdin=subprocess.DEVNULL).returncode)
if report["gaps"]:
    print("Dry run: no installs executed. Re-run with --sudo to apply the supported steps.")
    sys.exit(1)
print("PASS: doctor found no host gaps; nothing to install.")
PY
