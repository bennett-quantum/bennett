# Host provisioning

From the meta checkout, with Python 3.11 or newer and Bash already installed:

```sh
scripts/doctor.sh
scripts/bootstrap-host.sh          # print repairs; install nothing
scripts/bootstrap-host.sh --sudo   # apply supported repairs, then run doctor again
```

Both scripts accept `--workspace /path/to/bennett-workspace` and
`--manifest /path/to/manifest.toml`. The default workspace is the parent of
the meta checkout. `doctor.sh --json` exposes the same inventory and repair
commands used by bootstrap. Exit 0 means no detected host gaps; exit 1 means
one consolidated list of gaps. A successful installer is followed by another
doctor run; unresolved gaps still fail. Bootstrap is a no-op on a ready host.

Doctor reads every non-`info_only` repository in `manifest.toml` (currently
twelve), each main checkout's `gate.toml`, and
`bennett-dialect-spec/corpus/legality/toolchains.toml`. Concurrent job worktrees
are excluded. Unknown configuration keys fail loudly. Gate and sibling-build
commands are inspected without executing them. Tool versions, source entry
paths and script interpreters, pinned commits and published sibling files,
Cargo compiler/components, declared LLVM majors, frontends and LLVM CMake
development configs are checked. Built gate outputs are not required
to exist before a gate builds them. Python, Git, Bash, bubblewrap, systemd-run,
bd and Dolt are explicit shared infrastructure prerequisites.

Bubblewrap must also execute a namespace probe, and systemd-run must execute
a trivial command through the user manager. These probes do not run a gate.

Repairs use Ubuntu/Debian `apt-get`, existing rustup, or existing Julia as
appropriate. The configured LLVM majors determine package names; enable the
matching apt.llvm.org repository first if the distribution lacks those
packages. The Rust LLVM tools come from `rustup component add llvm-tools`
for the toolchain named in the configured path. The published Julia LLVM 20
artifact is provided by `LLVM_full_jll` 20.1.8 in
`~/.local/share/bennett-llvm20`. Doctor checks the exact configured path and
major after installation. Missing unknown tools, source checkouts, bd/Dolt
providers or malformed configuration need manual repair; bootstrap reports
them and continues to return failure.

The inventory checks declared prerequisites, not all dependencies hidden in
arbitrary program bodies. It is not a gate PASS, a Beads database health
check, or evidence that every offline dependency cache is warm. Run the
repository's normal gate after provisioning. The original provisioning
record's laptop versions are references, not replacement toolchain pins.
