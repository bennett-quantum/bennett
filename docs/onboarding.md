# Bennett new-contributor setup checklist

Follow top to bottom on a fresh Ubuntu 24.04 machine until every repo's local gate runs green and you can land work.
Bennett has no CI: the gates are local (`scripts/pre-push` per repo, via `bennett/tools/gate_run.py`). Historical host versions below are references, not toolchain pins.
After cloning the workspace (section 4), run the landed `scripts/doctor.sh` and use `scripts/bootstrap-host.sh` for repair plans. See [Host provisioning](host-provisioning.md). "(unverified)" marks facts not confirmed from the sources.

## 0. Hardware and OS expectations
- [ ] Ubuntu 24.04 (Linux Mint 22.3 or WSL2 Ubuntu 24.04.5). Verify: `lsb_release -d; uname -r`.
- [ ] Disk: at least 150 GB free before any gate (one cargo target dir for vm/conformance is 5-25 GB, the plugin dual-major build about 8 GB, cargo registry about 1.1 GB). Verify: `df -h ~`.
- [ ] RAM and cores: reference hosts are 12 threads/30 GB (laptop) and 64 threads/62 GB (Spiral, the current single orchestrator seat). Peak gate RSS is several GB (circuits oracle differential about 7 GB; isa-spec caps itself at 8 GiB). Verify: `nproc; free -g`. Gate timing varies 2-10x by host; that is expected.
- [ ] Any Linux user; the workspace is one directory holding all sibling checkouts, written `<workspace>` below (Spiral: `~/Projects/bennett-workspace`). No path is hardcoded (see 8).
- [ ] WSL2 only: `systemd=true` in `/etc/wsl.conf`, then `loginctl enable-linger $USER`, then `systemd-run --user --scope true` must work. Long gates run detached under `systemd-run --user` so they survive the session. Verify: `loginctl show-user $USER -p Linger` prints `Linger=yes`.
- [ ] Do not copy another machine's `.tmp/` caches (the laptop's were 450 GB); build your own.

## 1. Accounts and access
- [ ] GitHub account that is a member of org `bennett-quantum` with push rights (needed to land; all repos are public). Verify: `gh auth status`; `gh repo view bennett-quantum/bennett --json viewerPermission`.
- [ ] SSH or HTTPS credentials for pushing. Verify: `ssh -T git@github.com` (the checkouts use `https://github.com/bennett-quantum/<repo>.git` remotes; `gh auth login` with git protocol ssh is what both reference machines use, so `gh auth status` and `ssh -T git@github.com` must both succeed).
- [ ] `git config --global user.name` and `user.email` set. Verify: `git config --global --get user.email`.
- [ ] Model providers used by the orchestration (accounts and CLIs): Codex CLI with access to `gpt-6.1-sol` (editing children) and `gpt-6-astra` (review and council only); Claude Code (Claude account); Muse (`muse-wonder-full-1.0`, council seat). Verify: `codex --version; claude --version; muse --version` (reference: codex-cli 0.167.0, Claude Code 2.1.319, Muse Code 1.4.14).
- [ ] T3 Code as the orchestration client (delegate_task children, threads). Install and sign-in steps: (unverified, not in the sources).
- [ ] `quota` CLI from github.com/tobiasosborne/quota-app (build from that repo; on WSL2 it is the native Windows build reached through `~/.claude/skills/quota/scripts/quota.sh`; on Linux the Debian package `quota-app` gives `/usr/bin/quota`). Verify: `quota` prints live Claude and Codex quota. Read it before each launch wave; it is weather, not a rule. How to obtain the package: ask Tobias (unverified).
- [ ] Never put transcripts, logs, memory, orchestrator or `.tmp` records in any `bennett-quantum/*` repo (they are public). Code on `wip/*` branches is fine. Private home for records: `tobiasosborne/bennett-laptop-transfer` or a hand copy.

## 2. System packages
Clone the workspace as in section 4 first. The meta scripts need Bash and Python 3.11 or newer (including `tomllib`); cloning also needs Git.

- [ ] From the meta checkout, run `scripts/doctor.sh`. It inventories the twelve non-`info_only` repos in `manifest.toml`, their main-checkout `gate.toml` files, declared source paths and sibling pins, shared infrastructure, and LLVM toolchains. It probes unprivileged bubblewrap and the systemd user manager without running gates.
- [ ] For gaps, run `scripts/bootstrap-host.sh` to print repair steps without installing. Apply supported repairs with `scripts/bootstrap-host.sh --sudo`, which runs doctor again afterward. Missing source checkouts, unknown tool providers and malformed configuration need manual repair. Both scripts accept `--workspace` and `--manifest`; doctor also accepts `--json`.
- [ ] Require doctor exit 0 before gating. Exit 1 reports gaps; it does not mean a gate ran. Provisioning and repair details, including when to enable apt.llvm.org, live in [Host provisioning](host-provisioning.md).

## 3. Language toolchains
- [ ] Use the same doctor run for Rust/compiler components, declared LLVM majors, frontends and CMake development configs. The declarations are each repo's `gate.toml` and `bennett-dialect-spec/corpus/legality/toolchains.toml`; do not install from a second version list here. Bootstrap derives repairs from that inventory using apt-get, existing rustup or existing Julia.
- [ ] Doctor checks declared prerequisites. Repo gates still verify builds and behavior, including dependencies hidden inside scripts. Offline Cargo caches and Beads databases need the initialization in section 5; a doctor PASS does not check those.

## 4. Workspace clone
- [ ] Create the parent: `mkdir -p <workspace> && cd <workspace>`.
- [ ] `git clone https://github.com/bennett-quantum/bennett.git bennett` (the meta repo; `bennett/` must sit directly under the workspace).
- [ ] `cd bennett && BENNETT_REMOTE_BASE=https://github.com/bennett-quantum scripts/clone-all.sh` (or `git@github.com:bennett-quantum`). It reads `manifest.toml`, clones every repo as a sibling of `bennett/`, `git pull --ff-only`s ones that exist, skips `info_only` repos, and exits non-zero if any fail. Verify: the summary lists 12 `cloned`/`updated` and one `skipped info-only Bennett.jl`.
- [ ] Bennett.jl separately (manifest `info_only`, remote outside the org): `git clone https://github.com/tobiasosborne/Bennett.jl.git <workspace>/Bennett.jl`. Verify: `git -C <workspace>/Bennett.jl log -1`.
- [ ] Expected siblings: bennett-isa-spec, bennett-dialect-spec, bennett-conformance, bennett-vm, bennett-arith, bennett-runtimes, bennett-driver, bennett-plugin, bennett-sched, bennett-estimate, bennett-circuits, bennett-targets, Bennett.jl. Verify: `ls <workspace>`.
- [ ] `origin/main` is the source of truth in every repo. Do NOT fetch or check out `wip/*` (job backups owned by running children) or other people's `job/*` branches.

## 5. Per-repo bootstrap
Do this in each repo's MAIN checkout. Use doctor for installed-tool and source-path checks (sections 2-3); these steps initialize state it does not inspect.

- [ ] Beads on a fresh clone: `cd <repo> && bd init --non-interactive && bd import .beads/issues.jsonl`, then `bd ready`. Once initialized, use the live database. The export is a passive snapshot; children never commit it, and the orchestrator exports at merge. Follow the project's no-Dolt-remote-sync rule. The reference Beads/Dolt versions are listed in section 8; doctor reports versions but does not enforce those exact versions.
- [ ] Meta hooks: `cd bennett && scripts/install-hooks.sh`. In each repo, run `python3 <workspace>/bennett/tools/gate_run.py hook-check --repo <repo>` and require exit 0. This probes the effective hook without running the full gate. If Beads' hook masks the gate, repair the executable wrapper as described in [Hook chain](../tools/gate_README.md#hook-chain).
- [ ] Gate-tool selftest from the meta checkout: `mkdir -p .tmp/onboarding/tmp && TMPDIR=$PWD/.tmp/onboarding/tmp python3 -I tools/gate_selftest.py` must pass.
- [ ] Prefetch locked Cargo dependencies before an offline gate: run `cargo fetch --locked --manifest-path <dir>/Cargo.toml` in each gate-used crate with a `Cargo.lock`. Include the pinned sibling trees materialized by `gate_run.py verify` (section 6), not just the live main checkouts. Doctor does not inspect the registry cache.
- [ ] The gate builds declared outputs and pinned sibling builds; follow the repo's build documentation for any extra interactive development setup. Bennett.jl is `info_only` in this manifest, so initialize and test it according to its own README; the meta doctor skips its standalone gate inventory.

## 6. Verify
- [ ] Headless environment for every gate, build and agent command (non-negotiable 11): `unset DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER`; `export TMPDIR=<repo>/.tmp/<job>/tmp` (mkdir it); `export CARGO_TARGET_DIR=<repo>/.tmp/<job>/target` per job. Never run LLVM `-view-*`/`view-cfg` passes (use `dot-*`). Never use `/tmp`.
- [ ] Smallest first: the meta repo gate. `cd <workspace>/bennett && scripts/pre-push </dev/null` (runs `python3 -m unittest discover tools/tests`; fails if zero tests found). Verify: exit 0.
- [ ] Preflight one repo without running checks: `python3 <workspace>/bennett/tools/gate_run.py verify --repo <workspace>/bennett-sched --sha HEAD`. It materialises, hashes and builds every sibling pin. Exit 3 means setup failed (missing pin, hash mismatch, no bwrap).
- [ ] Run one repo's full gate the way the hook does (the stub runs `python3 -I .tmp/gate/tool/gate_run-<tool_sha>.py run --repo <root> --tool-sha <tool_sha>` with refs on stdin; run directly it gates HEAD). Start with `bennett-sched` (reference: PASS in 221 s on Spiral, 601 s on the laptop): `cd <workspace>/bennett-sched && scripts/pre-push </dev/null`. Verify: exit 0 and a receipt at `<repo>/.tmp/gate/records/<sha>.json` and `<repo>/.tmp/gate/receipts/<key>.json`.
- [ ] Long gates (10 min to 8 h) run detached: `systemd-run --user --unit=gate-<repo> --working-directory=<repo> scripts/pre-push` (or `--scope`), then `journalctl --user -u gate-<repo> -f`. A gate of the same repo must never run twice at once. Before launch check `MemAvailable` >= the gate's recorded peak RSS + 6 GB and load < nproc/2.
- [ ] Exit meanings: 0 all checks passed; 1 a check failed; 3 setup failed; 124 hang-guard trip = UNKNOWN (not pass, not fail; re-run once quietly, a second UNKNOWN is a bead). `--no-isolate` is not a push gate. Never use it to get a push through.
- [ ] A matching PASS receipt (keyed by tree, tool and isolation) makes a re-run a skip; `--fresh` forces a full run. Receipt skipping requires a `gate.toml` `tool_sha` that includes the receipt implementation (meta commit e25f3aa or a descendant); the pin in each repo is authoritative.
- [ ] Parity check: gate results (PASS/FAIL and receipt contents) should match `bennett/.tmp/main-health/status.md` on the same shas; timings will differ. Reference Spiral timings: dialect-spec 310 s, isa-spec 872 s, sched 221 s, driver 328 s. Ladder rungs 1 and 2: `bennett-conformance/ladder/` (run command per rung README; unverified).
- [ ] Gate-isolation failure: investigate errors naming absolute or `../sibling` paths for reads of live trees. Fix an incorrect pin or test; do not bypass isolation.

## 7. Working rules
Read each repo's `CLAUDE.md`, `bennett/docs/Bennett-NorthStar.md`, and the one rulebook [COMMON.md](process/COMMON.md)
(children also [T3CHILD.md](process/T3CHILD.md)). The rules live only there. `scripts/doctor.sh` checks that every process document
linked here is present as a file.

## 8. Known per-host gaps
- [ ] Hardcoded absolute paths in `<workspace>/bennett-dialect-spec/corpus/legality/toolchains.toml`: `llvm18.bin=/usr/lib/llvm-18/bin`; `llvm23.bin=$HOME/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/rustlib/x86_64-unknown-linux-gnu/bin`, `frontend_bin=/usr/lib/llvm-23/bin`; `llvm20.bin=$HOME/.julia/artifacts/21334d62ab8fb1788be32b83ab0373b77916a794/tools`. Satisfy them (user `tobias`, default rustup/julia homes, artifact hash from LLVM_full_jll 20.1.8) or edit the three paths in that file (a spec-repo change that must go through its gate). The laptop's `~/.julia/artifacts` holds three LLVM_full_jll-era hashes; only 21334d62... is the 20.1.8 one referenced.
- [ ] Moving or renaming the workspace breaks linked worktrees (git < 2.48 records absolute paths both ways). After a move run `python3 -I <workspace>/bennett/tools/repair_worktrees.py`; it re-points every worktree it can locate and lists, never prunes, the rest.
- [ ] `bd` must be 1.3.2 exactly, `dolt` 2.6.0. Spiral initially had bd 1.0.0 and dolt 1.82.4, which breaks imports.
- [ ] `bwrap` is required; without it gates are not push gates. Rootless user namespaces must be allowed.
- [ ] Offline Cargo commands require a warm registry. Prefetch (section 5), including pinned-sibling lockfiles.
- [ ] Rust 1.99.1 and Julia 1.13.3 are newer than a stock Spiral had (1.93.1, 1.12.3). `rustup update stable`; `juliaup update`.
- [ ] Single-thread speed differs by host (Spiral 1.48x slower than the laptop single-threaded, much faster parallel); per-repo hang-guard class tables carry a machine factor. A hang-guard trip is UNKNOWN, not a regression.
- [ ] Each repo's HEAD `gate.toml` supplies its current full `tool_sha`; the hook extracts `tools/gate_run.py` from that meta commit. Keep that exact commit available in `bennett/` (see [Pinned-sibling push gate](../tools/gate_README.md)); do not copy a reference SHA from an old setup record.
- [ ] Prefer each repo's `CLAUDE.md`, the tracked [COMMON.md](process/COMMON.md), and current gate/spec pins over old setup records. The laptop is retired; Spiral is the single orchestrator seat.
- [ ] Host provisioning is implemented by `scripts/doctor.sh` and `scripts/bootstrap-host.sh`; sections 2-5 use that inventory instead of duplicating package/toolchain checks. Verification for this update: `scripts/doctor.sh` exited **0** (all declared host prerequisites found; not a gate verdict).
