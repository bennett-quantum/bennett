# Bennett new-contributor setup checklist

Follow top to bottom on a fresh Ubuntu 24.04 machine until every repo's local gate runs green and you can land work.
Bennett has no CI: the gates are local (`scripts/pre-push` per repo, via `bennett/tools/gate_run.py`). Versions below are the ones recorded on the reference machines (laptop 2026-11-09, Spiral 2026-11-08).
Run `scripts/doctor.sh` once it lands (bead bennett-6e5, with `scripts/bootstrap-host.sh`); until then check each item by hand. "(unverified)" marks facts I could not confirm from the sources.

## 0. Hardware and OS expectations
- [ ] Ubuntu 24.04 (Linux Mint 22.3 or WSL2 Ubuntu 24.04.5). Verify: `lsb_release -d; uname -r`.
- [ ] Disk: at least 150 GB free before any gate (one cargo target dir for vm/conformance is 5-25 GB, the plugin dual-major build about 8 GB, cargo registry about 1.1 GB). Verify: `df -h ~`.
- [ ] RAM and cores: reference hosts are 12 threads/30 GB (laptop) and 64 threads/62 GB (Spiral, the current single orchestrator seat). Peak gate RSS is several GB (circuits oracle differential about 7 GB; isa-spec caps itself at 8 GiB). Verify: `nproc; free -g`. Gate timing varies 2-10x by host; that is expected.
- [ ] Linux user `tobias` and the workspace at the absolute path `/home/tobias/Projects/bennett-workspace` (see 4 and 8).
- [ ] WSL2 only: `systemd=true` in `/etc/wsl.conf`, then `loginctl enable-linger $USER`, then `systemd-run --user --scope true` must work. Long gates run detached under `systemd-run --user` so they survive the session. Verify: `loginctl show-user $USER -p Linger` prints `Linger=yes`.
- [ ] Do not copy another machine's `.tmp/` caches (the laptop's were 450 GB); build your own.

## 1. Accounts and access
- [ ] GitHub account that is a member of org `bennett-quantum` with push rights (needed to land; all repos are public). Verify: `gh auth status`; `gh repo view bennett-quantum/bennett --json viewerPermission`.
- [ ] SSH or HTTPS credentials for pushing. Verify: `ssh -T git@github.com` (unverified which transport the maintainer uses; the existing checkouts use `https://github.com/bennett-quantum/<repo>.git`).
- [ ] `git config --global user.name` and `user.email` set. Verify: `git config --global --get user.email`.
- [ ] Model providers used by the orchestration (accounts and CLIs): Codex CLI with access to `gpt-6.1-sol` (editing children) and `gpt-6-astra` (review and council only); Claude Code (Claude account); Muse (`muse-wonder-full-1.0`, council seat). Verify: `codex --version; claude --version; muse --version` (reference: codex-cli 0.167.0, Claude Code 2.1.319, Muse Code 1.4.14).
- [ ] T3 Code as the orchestration client (delegate_task children, threads). Install and sign-in steps: (unverified, not in the sources).
- [ ] `quota` CLI from github.com/tobiasosborne/quota-app (a Debian package `quota-app`, binary `/usr/bin/quota` on Spiral). Verify: `quota` prints live Claude and Codex quota. Read it before each launch wave; it is weather, not a rule. How to obtain the package: ask Tobias (unverified).
- [ ] Never put transcripts, logs, memory, orchestrator or `.tmp` records in any `bennett-quantum/*` repo (they are public). Code on `wip/*` branches is fine. Private home for records: `tobiasosborne/bennett-laptop-transfer` or a hand copy.

## 2. System packages
- [ ] Add apt.llvm.org for noble, LLVM 23: `deb https://apt.llvm.org/noble/ llvm-toolchain-noble-23 main` (key from https://apt.llvm.org/llvm-snapshot.gpg.key), then `sudo apt update`.
- [ ] One apt line (names from the reference host's dpkg list; apt.llvm.org's 23 is a snapshot, the laptop had 23.1.6 built 2026-11-03):
  `sudo apt install -y build-essential git cmake python3 clang-18 llvm-18-dev clang-23 llvm-23-dev libclang-23-dev libclang-cpp23-dev libpolly-23-dev lld-23 bubblewrap time linux-tools-generic libmpfr6 libgmp10 libffi-dev zlib1g-dev libxml2-dev libedit2 libsqlite3-0 curl ca-certificates gh`
  Verify: `clang-18 --version` (Ubuntu clang 18.1.3), `clang-23 --version` (23.1.x), `cmake --version` (3.28.3), `bwrap --version` (0.9.0), `/usr/bin/time -v true`, `perf --version`, `python3 --version` (3.12.3), `git --version` (2.43.0), `gh --version` (2.45.0). `ninja` and `musl-gcc` were absent on the laptop and are not needed.
- [ ] Optional: `qemu-x86_64`. Only referenced by ladder rung 6 (native QEMU serial-console comparison, `bennett-conformance/ladder/rung-6/README.md`); it was NOT installed on the laptop, so rung 6 is not part of any current local gate (unverified whether it will need system or user-mode qemu).
- [ ] `bwrap` must work unprivileged. Verify: `bwrap --ro-bind / / true`. If it fails (some containers/AppArmor), gates run `--no-isolate`, which is announced and does not count as a pass.
- [ ] Python is stdlib only: install no pip packages (laptop pip list was empty). Gates call `python3 -I`.

## 3. Language toolchains
- [ ] Rust: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`, then `rustup toolchain install stable && rustup component add llvm-tools clippy rustfmt`. Reference: rustc/cargo 1.99.1 (LLVM 23.1.1), components cargo, clippy, llvm-tools, rust-std, rustc, rustfmt. Verify: `rustc -Vv | grep -E 'release|LLVM'`; `rustup component list --installed`; `ls ~/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/rustlib/x86_64-unknown-linux-gnu/bin` contains `opt` and `llc` (this is the LLVM 23 `bin` in toolchains.toml; `opt --version` reports 23.1.1-rust-1.99.1-stable).
- [ ] Optional cargo tools seen on the laptop: cargo-llvm-cov 0.9.1, cargo-mutants 27.1.0, cargo-deb 3.8.0 (not needed for gates; unverified).
- [ ] Julia 1.13.3 via juliaup: `curl -fsSL https://install.julialang.org | sh`, then `juliaup add 1.13.3 && juliaup default 1.13.3`. Verify: `julia --version` prints 1.13.3. Needed by Bennett.jl and conformance ladder rung 1 (Julia row prints `Base.libllvm_version`).
- [ ] Julia LLVM 20 environment (provides `opt`/clang-20 for the legality corpus):
  `JULIA_PROJECT=$HOME/.local/share/bennett-llvm20 julia -e 'using Pkg; Pkg.add(name="LLVM_full_jll", version="20.1.8")'`
  Verify: `ls ~/.julia/artifacts/21334d62ab8fb1788be32b83ab0373b77916a794/tools` lists `opt` (that hash is what toolchains.toml hardcodes; see 8 if yours differs).
- [ ] Python 3.12.3 from the distro (`/usr/bin/python3`). Verify: `python3 -c 'import tomllib'` works (clone-all.sh needs it).
- [ ] LLVM 18 and 23 layout the plugin CMake expects: `/usr/lib/llvm-18/lib/cmake/llvm` and `/usr/lib/llvm-23/lib/cmake/llvm`. Verify: `ls /usr/lib/llvm-{18,23}/lib/cmake/llvm/LLVMConfig.cmake`; `ls /usr/include/llvm-23/llvm/Plugins/PassPlugin.h`.
- [ ] Optional symlink as on the laptop: `ln -s /usr/bin/clang-18 ~/.local/bin/clang` (makes bare `clang` mean 18). Put `~/.local/bin` and `~/.cargo/bin` on PATH. No bare `opt`/`llvm-config` on PATH is expected.

## 4. Workspace clone
- [ ] Create the parent: `mkdir -p /home/tobias/Projects/bennett-workspace && cd /home/tobias/Projects/bennett-workspace`. Another path or user needs the edits in section 8 first.
  WSL2 alternative used on Spiral: keep the real tree elsewhere and bind mount it at `/home/tobias/Projects/bennett-workspace` so the absolute path is identical.
- [ ] `git clone https://github.com/bennett-quantum/bennett.git bennett` (the meta repo; `bennett/` must sit directly under the workspace).
- [ ] `cd bennett && BENNETT_REMOTE_BASE=https://github.com/bennett-quantum scripts/clone-all.sh` (or `git@github.com:bennett-quantum`). It reads `manifest.toml`, clones every repo as a sibling of `bennett/`, `git pull --ff-only`s ones that exist, skips `info_only` repos, and exits non-zero if any fail. Verify: the summary lists 12 `cloned`/`updated` and one `skipped info-only Bennett.jl`.
- [ ] Bennett.jl separately (manifest `info_only`, remote outside the org): `git clone https://github.com/tobiasosborne/Bennett.jl.git /home/tobias/Projects/bennett-workspace/Bennett.jl`. Verify: `git -C /home/tobias/Projects/bennett-workspace/Bennett.jl log -1`.
- [ ] Expected siblings: bennett-isa-spec, bennett-dialect-spec, bennett-conformance, bennett-vm, bennett-arith, bennett-runtimes, bennett-driver, bennett-plugin, bennett-sched, bennett-estimate, bennett-circuits, bennett-targets, Bennett.jl. Verify: `ls /home/tobias/Projects/bennett-workspace`.
- [ ] `origin/main` is the source of truth in every repo. Do NOT fetch or check out `wip/*` (job backups owned by running children) or other people's `job/*` branches.

## 5. Per-repo bootstrap
Do this in each repo's MAIN checkout (not a worktree). Repos with beads: all 12 org repos (Bennett.jl: unverified).
- [ ] Install `bd` 1.3.2 EXACTLY (9b65b9e19) and `dolt` 2.6.0 (mismatched bd versions have broken imports). Install from the gastownhall/beads releases and dolt releases (exact download steps unverified). Verify: `bd version` prints `1.3.2 (9b65b9e19`; `dolt version` prints 2.6.0 (ignore the "newer version" warning).
- [ ] Per repo, rebuild the local Dolt DB from the tracked export: `cd <repo> && bd init && bd import .beads/issues.jsonl` (check `bd prime` for the exact import syntax of your bd; the brief says "import .beads/issues.jsonl per bd prime"). Verify: `bd ready` runs and `bd list` is non-empty. No Dolt remote sync, ever; `.beads/issues.jsonl` is the passive export (`bd export -o .beads/issues.jsonl` before committing `.beads/`).
- [ ] Hook chain, per repo. `bd init` sets `core.hooksPath=.beads/hooks` and leaves a copy of the gate there; that copy must `exec` the repo's `scripts/pre-push`. Verify:
  `git -C <repo> config core.hooksPath` (expect `.beads/hooks`) and `grep exec <repo>/.beads/hooks/pre-push` (expect `exec "$root/scripts/pre-push" "$@"`).
  Fix if wrong: replace the file with the 5-line hook in `bennett/tools/gate_README.md` ("Hook chain"), keep it executable. Check: `python3 /home/tobias/Projects/bennett-workspace/bennett/tools/gate_run.py hook-check --repo <repo>` exits 0.
- [ ] Meta repo hooks: `cd bennett && scripts/install-hooks.sh` (installs an executable wrapper at `git rev-parse --git-path hooks/pre-push`, honouring `core.hooksPath`). Verify: `BENNETT_GATE_HOOK_PROBE=1 .beads/hooks/pre-push` or `gate_run.py hook-check` prints `bennett-gate-hook-chained`.
- [ ] Gate tool selftest: `cd /home/tobias/Projects/bennett-workspace/bennett && mkdir -p .tmp/onboarding/tmp && TMPDIR=$PWD/.tmp/onboarding/tmp python3 -I tools/gate_selftest.py` must pass (the brief runs it after the hooks).
- [ ] Prefetch the cargo registry; gates run `cargo test --offline` and will fail on a cold registry. In every live `Cargo.lock` dir: `cargo fetch --locked --manifest-path <dir>/Cargo.toml`. Find them: `find /home/tobias/Projects/bennett-workspace -name Cargo.lock -not -path '*/.tmp/*' -not -path '*/target/*'`. Known crates: bennett-isa-spec (reference-interpreter, conformance), bennett-sched, bennett-vm, bennett-driver, bennett-circuits, bennett-estimate, bennett-conformance (every Cargo.toml), bennett-targets (`validator/`).
- [ ] Also fetch for each pinned sibling sha the gates build (the registry must hold their locked versions): after the first `gate_run.py verify` (section 6) materialises `.tmp/gate/cache/<name>@<sha12>/<name>`, run `cargo fetch --locked` there, or `git archive` the pinned sha into a scratch dir (brief 08:37Z). Registry is about 1.1 GB.
- [ ] Plugin (C++): dual-major CMake. `cd bennett-plugin && python3 scripts/build` configures and builds `build/libbennett-plugin-18.so` and `build/libbennett-plugin-23.so` (CMake `-S . -B build`, `--build -j 3`; falls back to an `llvm-config` build when cmake is missing, which is "CMake configuration unverified"). Verify: both `.so` files exist. Per-major tool dirs default to `/usr/lib/llvm-<major>/bin`; override with `BENNETT_LLVM18_BIN` / `BENNETT_LLVM23_BIN` (runtimes honours these). The driver gate builds the plugin itself via the same script.
- [ ] Runtimes build uses `clang`, `llvm-as` from `/usr/lib/llvm-{18,23}/bin` (`bennett-runtimes/scripts/build.py`). No extra install beyond section 2.
- [ ] Bennett.jl: `cd Bennett.jl && julia --project -e 'using Pkg; Pkg.instantiate()'` (unverified; I did not read its Project.toml). Its own test command: see its README (unverified).

### Per-repo dependency summary (from gate.toml on origin/main; SPEC_VERSIONS.toml pins the contract versions)
| repo | build/test needs | spec versions declared |
|---|---|---|
| bennett-isa-spec | cargo (reference-interpreter, conformance), python3 | isa/object/launch/sched/cert/coverage/target 0.8 |
| bennett-dialect-spec | python3 only, plus ref interpreter built from isa-spec pin, LLVM 18/20/23 tools via toolchains.toml; pins conformance, driver | dialect 0.2.14, isa 0.8 |
| bennett-sched | cargo, rustfmt, python3 | sched/isa/object/cert/target 0.9 |
| bennett-vm | cargo, python3 | 0.8 across the board |
| bennett-circuits | cargo (oracle differential about 7 GB peak), python3 | 0.8 |
| bennett-estimate | cargo, python3 | 0.9 |
| bennett-targets | cargo + clippy + fmt (`validator/`), python3 | isa 0.9 |
| bennett-arith | python3 (`scripts/time_guard.py`), LLVM 18/23 via pinned siblings | dialect 0.2.13, isa 0.9 |
| bennett-runtimes | clang/llvm-as 18 and 23, python3; pins conformance and arith | dialect 0.2.13, isa 0.8 |
| bennett-plugin | CMake, LLVM 18+23 dev, cargo (builds vm, isa-ref), python3 | dialect 0.2.13, isa 0.8 |
| bennett-driver | cargo, plugin dual-major build, python3 | dialect 0.2.13, isa 0.8 |
| bennett-conformance | cargo (every crate), python3; ladder rung 1 needs clang 18/23, rustc, julia; rung 6 needs qemu (unverified) | dialect 0.2.10, isa 0.9 |
| Bennett.jl | Julia 1.13.3 | (info_only) |

## 6. Verify
- [ ] Headless environment for every gate, build and agent command (non-negotiable 11): `unset DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER`; `export TMPDIR=<repo>/.tmp/<job>/tmp` (mkdir it); `export CARGO_TARGET_DIR=<repo>/.tmp/<job>/target` per job. Never run LLVM `-view-*`/`view-cfg` passes (use `dot-*`). Never use `/tmp`.
- [ ] Smallest first: the meta repo gate. `cd /home/tobias/Projects/bennett-workspace/bennett && scripts/pre-push </dev/null` (runs `python3 -m unittest discover tools/tests`; fails if zero tests found). Verify: exit 0.
- [ ] Preflight one repo without running checks: `python3 /home/tobias/Projects/bennett-workspace/bennett/tools/gate_run.py verify --repo /home/tobias/Projects/bennett-workspace/bennett-sched --sha HEAD`. It materialises, hashes and builds every sibling pin. Exit 3 means setup failed (missing pin, hash mismatch, no bwrap).
- [ ] Run one repo's full gate the way the hook does. Start with `bennett-sched` (reference: PASS in 221 s on Spiral, 601 s on the laptop): `cd /home/tobias/Projects/bennett-workspace/bennett-sched && scripts/pre-push </dev/null` (or `python3 ../bennett/tools/gate_run.py run --repo .`; exact subcommand syntax: check `gate_run.py --help`, unverified). Verify: exit 0 and a receipt at `<repo>/.tmp/gate/records/<sha>.json` and `<repo>/.tmp/gate/receipts/<key>.json`.
- [ ] Long gates (10 min to 8 h) run detached: `systemd-run --user --unit=gate-<repo> --working-directory=<repo> scripts/pre-push` (or `--scope`), then `journalctl --user -u gate-<repo> -f`. A gate of the same repo must never run twice at once. Before launch check `MemAvailable` >= the gate's recorded peak RSS + 6 GB and load < nproc/2.
- [ ] Exit meanings: 0 all checks passed; 1 a check failed; 3 setup failed; 124 hang-guard trip = UNKNOWN (not pass, not fail; re-run once quietly, a second UNKNOWN is a bead). `--no-isolate` is not a push gate. Never use it to get a push through.
- [ ] A matching PASS receipt (keyed by tree, tool and isolation) makes a re-run a skip; `--fresh` forces a full run. Receipt skipping is live only where `gate.toml` `tool_sha` is at or after meta commit e25f3aa (re-pin wave in progress).
- [ ] Parity check: gate results (PASS/FAIL and receipt contents) should match `bennett/.tmp/main-health/status.md` on the same shas; timings will differ. Reference Spiral timings: dialect-spec 310 s, isa-spec 872 s, sched 221 s, driver 328 s. Ladder rungs 1 and 2: `bennett-conformance/ladder/` (run command per rung README; unverified).
- [ ] Gate-isolation failure: a red gate whose error names an absolute or `../sibling` path means a test reads a live tree. Fix the pin or the test; do not bypass.

## 7. Working rules (one screen)
Read before touching anything: each repo's `CLAUDE.md`; `bennett/docs/Bennett-NorthStar.md`; `bennett/docs/decisions/2026-11-02-code-quality-policy.md`; and the orchestrator briefs `COMMON.md` and `T3CHILD.md`. Those two are currently untracked at `bennett/.tmp/orchestrator/briefs/COMMON.md` and `T3CHILD.md`; they are being moved into the repo as `bennett/docs/process/COMMON.md` and `T3CHILD.md` (use the new location once it exists).
- [ ] One writer per path set. Parallel writers only on disjoint owned paths named in both briefs. Never `git add -A` at repo level, never `git stash`, `reset`, `checkout --`, rebase or force-push.
- [ ] Red-green TDD: write the test, watch it fail, make it pass, refactor. Fail fast and loud; no silent fallbacks. "Runs without errors" is not a pass; verify against the conformance suite for the versions in `SPEC_VERSIONS.toml`.
- [ ] Repos couple only through the published specs (ISA, dialect). Never share code across a contract boundary.
- [ ] No narrowing of north-star scope (non-negotiable 10): never reject, fault or omit a promised capability; raise a blocker bead naming the exact change instead.
- [ ] Branches: work on `job/<name>` in a worktree `../<repo>-job-<name>`; commit owned paths often (`git -C <wt> add -- <paths>; git -C <wt> commit -m ... -- <paths>`); back up with `git -C <wt> push --no-verify -q origin HEAD:refs/heads/wip/<name>`. Only the orchestrator merges (`--no-ff`) and pushes `main`, after a gate PASS and a review on the same head. Commit trailer: `Co-Authored-By: <model> <noreply@anthropic.com>` for Claude models, `Agent: <model id>` for others.
- [ ] Beads, not TODO files: `bd` from the repo's main checkout (`bd ready`, `bd show`, `bd update <id> --claim`, `bd create`, `bd note`, `bd close <id> --reason "<what, verified by which command>"`); `bd export -o .beads/issues.jsonl` and commit that file only at the orchestrator's merge (children do not commit it). No Dolt remote sync. Use `bd remember`, not MEMORY.md.
- [ ] Worklog: the person who commits the session adds one `## Session log - YYYY-MM-DD - ...` block at the top of the highest-numbered chunk in `bennett/worklog/` (new `NNN_` chunk past about 280 lines). Subagents keep `.tmp/<name>/PROGRESS.md` (Resume block: done / verified with which command / next) and write nothing else outside owned paths.
- [ ] Review: evidence-first, two rounds, then merge or revert; only P0/P1 (wrong result on a named north-star rung path, unsound oracle, broken build/gate/hook) block. Code quality policy: `bennett/docs/decisions/2026-11-02-code-quality-policy.md`.
- [ ] Time: run `date -u` in the command that writes a timestamp. No bare time literals in gates or tests (hang-guard class table per repo).
- [ ] Never run a sibling repo's full gate from a child job; the orchestrator gates at merge. Never `--no-verify` a push to `main`. Transcripts and logs never go to the public repos (see section 1).

## 8. Known per-host gaps
- [ ] Hardcoded absolute paths in `/home/tobias/Projects/bennett-workspace/bennett-dialect-spec/corpus/legality/toolchains.toml`: `llvm18.bin=/usr/lib/llvm-18/bin`; `llvm23.bin=/home/tobias/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/rustlib/x86_64-unknown-linux-gnu/bin`, `frontend_bin=/usr/lib/llvm-23/bin`; `llvm20.bin=/home/tobias/.julia/artifacts/21334d62ab8fb1788be32b83ab0373b77916a794/tools`. Satisfy them (user `tobias`, default rustup/julia homes, artifact hash from LLVM_full_jll 20.1.8) or edit the three paths in that file (a spec-repo change that must go through its gate). The laptop's `~/.julia/artifacts` holds three LLVM_full_jll-era hashes; only 21334d62... is the 20.1.8 one referenced.
- [ ] Workspace path `/home/tobias/Projects/bennett-workspace` is expected by briefs, the gate cache paths and `T3CHILD.md` examples. Same path via bind mount, or search-and-edit (unverified how many tracked files hardcode it: `grep -rIl /home/tobias/Projects/bennett-workspace` in each repo).
- [ ] `bd` must be 1.3.2 exactly, `dolt` 2.6.0. Spiral initially had bd 1.0.0 and dolt 1.82.4, which breaks imports.
- [ ] `bwrap` is required; without it gates are not push gates. Rootless user namespaces must be allowed.
- [ ] `cargo test --offline`: a cold registry fails the gate. Prefetch (section 5), including pinned-sibling lockfiles.
- [ ] Rust 1.99.1 and Julia 1.13.3 are newer than a stock Spiral had (1.93.1, 1.12.3). `rustup update stable`; `juliaup update`.
- [ ] Single-thread speed differs by host (Spiral 1.48x slower than the laptop single-threaded, much faster parallel); per-repo hang-guard class tables carry a machine factor. A hang-guard trip is UNKNOWN, not a regression.
- [ ] Gate `tool_sha` per repo (reference: `01c0314c`) is extracted from the meta repo's objects at gate time, so `bennett/` must be a full clone with that commit.
- [ ] Stale docs: the 2026-11-03 HANDOFF.md is stale, many READMEs lag the code, and the laptop is retired (single seat is Spiral). Prefer `CLAUDE.md` and COMMON.md.
- [ ] Open question: `scripts/doctor.sh` and `scripts/bootstrap-host.sh` (bead bennett-6e5) should replace sections 2-5 checks once landed. When they do, delete the duplicated commands here.
