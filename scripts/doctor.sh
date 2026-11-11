#!/usr/bin/env bash
# Read-only host inventory; Python's standard library parses the TOML contracts.
set -euo pipefail
unset DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS BROWSER
exec python3 - "$0" "$@" <<'PY'
import argparse
import ast
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tomllib

META = Path(sys.argv.pop(1)).resolve().parents[1]
TOP_KEYS = {"schema", "repo", "tool_sha", "timeout_s", "env", "check", "report", "siblings", "scan_exclude", "receipt"}
CMD_KEYS = {"name", "argv", "env", "cwd", "tier", "inputs"}
BUILD_KEYS = CMD_KEYS | {"outputs", "needs"}
SIB_KEYS = {"sha", "repo", "files", "build", "note"}
# These are gate/Beads infrastructure, rather than a second per-repo tool list.
INFRASTRUCTURE = ("python3", "git", "bash", "bwrap", "bd", "dolt", "systemd-run")
PACKAGES = {"python3": "python3", "git": "git", "bash": "bash", "bwrap": "bubblewrap",
            "cmake": "cmake", "make": "make", "gcc": "gcc", "g++": "g++",
            "cc": "build-essential", "c++": "build-essential", "sh": "dash",
            "find": "findutils", "sort": "coreutils", "mkdir": "coreutils", "ln": "coreutils",
            "rm": "coreutils", "touch": "coreutils", "timeout": "coreutils", "time": "time",
            "systemd-run": "systemd", "ninja": "ninja-build", "env": "coreutils"}
BUILTINS = {":", "true", "false", "echo", "printf", "exit", "return", "cd", "export", "unset",
            "ulimit", "test", "[", "break", "continue", "read", "set", "shift", "wait"}


class ConfigError(ValueError):
    pass


def table(value, keys, where):
    if not isinstance(value, dict):
        raise ConfigError(f"{where}: expected a table")
    extra = value.keys() - keys
    if extra:
        raise ConfigError(f"{where}: unknown key {sorted(extra)}")


def strings(value, where):
    if not isinstance(value, list) or not all(isinstance(v, str) and v for v in value):
        raise ConfigError(f"{where}: expected a list of nonempty strings")


def environment(value, where):
    if not isinstance(value, dict) or not all(isinstance(v, str) for v in value.values()):
        raise ConfigError(f"{where}: environment must map names to strings")


def command_config(command, keys, where):
    if isinstance(command, dict):
        where = f"{where} ({command.get('name', '<unnamed>')})"
    table(command, keys, where)
    if not isinstance(command.get("name"), str) or not command["name"]:
        raise ConfigError(f"{where}: missing name")
    strings(command.get("argv"), where)
    if not command["argv"]:
        raise ConfigError(f"{where}: argv cannot be empty")
    if "cwd" in command and not isinstance(command["cwd"], str):
        raise ConfigError(f"{where}: cwd must be a string")
    environment(command.get("env", {}), where)
    for field in ("outputs", "needs"):
        if field in command:
            strings(command[field], f"{where}.{field}")


def load_gate(path, expected):
    data = tomllib.loads(path.read_text())
    table(data, TOP_KEYS, str(path))
    if type(data.get("schema")) is not int or data["schema"] != 1 or data.get("repo") != expected:
        raise ConfigError(f"{path}: expected schema=1 and repo={expected!r}")
    if not re.fullmatch(r"[0-9a-f]{40}", str(data.get("tool_sha", ""))):
        raise ConfigError(f"{path}: tool_sha must be a full commit SHA")
    environment(data.get("env", {}), str(path))
    if "scan_exclude" in data:
        strings(data["scan_exclude"], f"{path}.scan_exclude")
    if "timeout_s" in data and (type(data["timeout_s"]) is not int or data["timeout_s"] <= 0):
        raise ConfigError(f"{path}: timeout_s must be a positive integer")
    if not isinstance(data.get("check"), list) or not data["check"]:
        raise ConfigError(f"{path}: at least one check required")
    for kind in ("check", "report"):
        commands = data.get(kind, [])
        if not isinstance(commands, list):
            raise ConfigError(f"{path}.{kind}: expected array of tables")
        for command in commands:
            command_config(command, CMD_KEYS, f"{path}.{kind}")
    if not isinstance(data.get("siblings", {}), dict):
        raise ConfigError(f"{path}.siblings: expected table")
    for name, pin in data.get("siblings", {}).items():
        where = f"{path}.siblings.{name}"
        table(pin, SIB_KEYS, where)
        if not re.fullmatch(r"[0-9a-f]{40}", str(pin.get("sha", ""))):
            raise ConfigError(f"{where}: sha must be a full commit SHA")
        if not isinstance(pin.get("repo", name), str):
            raise ConfigError(f"{where}: repo must be a string")
        repo = Path(pin.get("repo", name))
        if repo.is_absolute() or len(repo.parts) != 1 or repo.parts[0] in {".", ".."}:
            raise ConfigError(f"{where}: repo must be a workspace repository name")
        if not isinstance(pin.get("files", {}), dict):
            raise ConfigError(f"{where}: files must be a table")
        for filename, digest in pin.get("files", {}).items():
            if not filename or Path(filename).is_absolute() or ".." in Path(filename).parts or not re.fullmatch(r"[0-9a-f]{64}", str(digest)):
                raise ConfigError(f"{where}: invalid file digest for {filename}")
        if not isinstance(pin.get("build", []), list):
            raise ConfigError(f"{where}: build must be an array of tables")
        for command in pin.get("build", []):
            command_config(command, BUILD_KEYS, where)
            for need in command.get("needs", []):
                if need not in data["siblings"]:
                    raise ConfigError(f"{where}: unpinned build need {need}")
    return data


def run(argv, cwd=None):
    return subprocess.run(argv, cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, text=True)


def repair_tool(name):
    base = Path(name).name
    if base in PACKAGES:
        return [["sudo", "apt-get", "install", "-y", PACKAGES[base]]]
    if base in {"cargo", "rustc", "rustup"}:
        return [["rustup", "toolchain", "install", "stable", "--profile", "minimal"]]
    if base in {"rustfmt", "cargo-fmt", "cargo-clippy", "clippy-driver"}:
        component = "clippy" if "clippy" in base else "rustfmt"
        return [["rustup", "component", "add", component]]
    match = re.fullmatch(r"(clang\+\+|clang|opt|llc|llvm-config|llvm-link|llvm-as|llvm-dis|ld.lld)-(\d+)", base)
    if match:
        major = match[2]
        return [["sudo", "apt-get", "install", "-y", f"clang-{major}", f"llvm-{major}-dev", f"lld-{major}"]]
    return []


class Inventory:
    def __init__(self):
        self.found = []
        self.gaps = []
        self.tools = {}
        self.paths = set()
        self.pins = set()

    def gap(self, label, reason, install=()):
        self.gaps.append(dict(label=label, reason=reason, install=list(install)))

    def tool(self, name, source, major=None, install=None, probe=None):
        key = (name, major, tuple(probe or []))
        if key in self.tools:
            return self.tools[key]
        if install is None:
            install = repair_tool(name)
        path = shutil.which(name)
        if not path:
            self.gap(name, f"not executable / not on PATH; required by {source}", install)
            self.tools[key] = False
            return False
        args = probe or (["version"] if Path(name).name in {"bd", "dolt"} else ["--version"])
        if Path(name).name == "sh" and probe is None:
            args = ["-c", "command -V sh"]  # POSIX sh has no --version interface.
        try:
            result = run([path, *args])
        except OSError as error:
            self.gap(name, f"{source}: {error}", install)
            self.tools[key] = False
            return False
        output = (result.stdout + result.stderr).strip()
        version = re.search(r"(?:LLVM|clang) version\s+(\d+)|^(\d+)\.", output, re.M)
        wrong_major = major is not None and (not version or int(version[1] or version[2]) != major)
        if result.returncode or not output or wrong_major:
            reason = f"probe exit {result.returncode}: {output or 'empty version output'}"
            if wrong_major:
                reason += f"; expected LLVM {major}"
            self.gap(name, f"{source}: {reason}", install)
            self.tools[key] = False
            return False
        lines = output.splitlines()
        summary = next((line.strip() for line in lines if re.search(r"version\s+\d", line, re.I)), lines[0])
        self.found.append(dict(label=name, path=path, version=summary, source=source))
        self.tools[key] = True
        return True

    def path(self, path, source, executable=False, ref=None):
        key = (str(path), ref, executable)
        if key in self.paths:
            return
        self.paths.add(key)
        if ref:
            repo, sha = ref
            relative = path.relative_to(repo).as_posix()
            result = run(["git", "-C", str(repo), "cat-file", "-e", f"{sha}:{relative}"])
            exists = result.returncode == 0
        else:
            exists = path.exists() and (not executable or os.access(path, os.X_OK))
        if not exists:
            self.gap(str(path), f"missing {'executable ' if executable else ''}source/path required by {source}"
                     + (f" at {ref[1]}" if ref else ""))
        else:
            self.found.append(dict(label=str(path), path=str(path), version="source/path present", source=source))

    def pin(self, repo, sha, source):
        if (repo, sha) in self.pins:
            return
        self.pins.add((repo, sha))
        result = run(["git", "-C", str(repo), "cat-file", "-e", sha + "^{commit}"])
        if result.returncode:
            install = [["git", "-C", str(repo), "fetch", "origin", sha]] if repo.is_dir() else []
            self.gap(f"{repo}@{sha}", f"pinned commit unavailable; required by {source}", install)
        else:
            self.found.append(dict(label=f"{repo}@{sha}", path=str(repo),
                                   version="pinned commit present", source=source))


def source_path(value, root, cwd):
    # Gate-created trees and built outputs are deliberately checked by the gate, not host provisioning.
    if any(marker in value for marker in ("{sibling:", "{layout}", "{wt}", "$")):
        return None
    value = value.replace("{root}", str(root))
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = cwd / path
    parts = path.relative_to(root).parts if path.is_relative_to(root) else ()
    generated = {".tmp", "target", "build", ".isa-ref"}
    if any(part in generated for part in parts[:-1]) or (parts and parts[0] in generated):
        return None
    return path


def check_source(value, root, cwd, source, inventory, ref=None, executable=False):
    path = source_path(value, root, cwd)
    if path is not None:
        inventory.path(path, source, executable, ref)
        if executable and not ref and path.is_file():
            with path.open("rb") as stream:
                first = stream.read(4096).split(b"\n", 1)[0].decode("utf-8", errors="replace").strip()
            if first.startswith("#!"):
                interpreter = shlex.split(first[2:])
                if interpreter and interpreter[0] == "/usr/bin/env":
                    interpreter = interpreter[1:]
                    if interpreter and interpreter[0] == "-S":
                        interpreter = interpreter[1:]
                if interpreter:
                    inventory.tool(interpreter[0], f"{source}: {path} shebang")


def check_environment(values, root, cwd, source, inventory, aliases):
    known = {"root", "wt", "layout"} | {"sibling:" + alias for alias in aliases}
    for key, value in values.items():
        for placeholder in re.findall(r"(?<!\$)\{([^{}]+)\}", value):
            if placeholder not in known:
                raise ConfigError(f"{source}: unknown placeholder {{{placeholder}}} in {key}")
        if key in {"CC", "CXX", "AR", "RANLIB", "LD"}:
            inspect_command(shlex.split(value), root, cwd, source, inventory)
        elif value.startswith(("/", "~/", "{root}")):
            check_source(value, root, cwd, source, inventory)


def shell_commands(text):
    # Static shell tokenization only: never evaluate a gate command in the doctor.
    lexer = shlex.shlex(text, posix=True, punctuation_chars=";&|()")
    lexer.whitespace_split = True
    tokens = list(lexer)
    current = []
    loop_header = False
    for token in tokens + [";"]:
        if token in {"for", "while"} and not current:
            loop_header = True
        elif token == "do":
            loop_header = False
        elif loop_header:
            continue
        elif token in {";", "&&", "||", "|", "(", ")", "&"}:
            if current:
                yield current
                current = []
        elif token not in {"then", "else", "fi", "done", "if", "!"}:
            current.append(token)
    # Command substitutions in loop headers also carry host requirements.
    for substitution in re.findall(r"\$\(([^()]*)\)", text):
        yield from shell_commands(substitution)


def inspect_command(argv, root, cwd, source, inventory, ref=None):
    if not argv:
        return
    name, *args = argv
    if name in BUILTINS:
        return
    if name == "exec":
        inspect_command(args, root, cwd, source, inventory, ref)
        return
    if re.match(r"^[A-Za-z_][A-Za-z_0-9]*=", name):
        inspect_command(args, root, cwd, source, inventory, ref)
        return
    if "$" in name:
        raise ConfigError(f"{source}: dynamic command cannot be inventoried: {name}")
    if "/" in name and not name.startswith("/") or name.startswith("{"):
        check_source(name, root, cwd, source, inventory, ref, executable=True)
    else:
        inventory.tool(name, source)
    base = Path(name).name
    match base:
        case "timeout":
            index = next((i for i, arg in enumerate(args) if re.fullmatch(r"\d+(?:\.\d+)?[smhd]?", arg)), None)
            if index is None:
                raise ConfigError(f"{source}: cannot inventory timeout command without a duration")
            inspect_command(args[index + 1:], root, cwd, source, inventory, ref)
        case "env":
            index = 0
            while index < len(args):
                if args[index] in {"-u", "--unset"}:
                    index += 2
                elif args[index] in {"-i", "--ignore-environment", "--"} or "=" in args[index]:
                    index += 1
                else:
                    break
            inspect_command(args[index:], root, cwd, source, inventory, ref)
        case "sh" | "bash":
            shell_index = next((i for i, a in enumerate(args) if a.startswith("-") and "c" in a), None)
            if shell_index is not None:
                if shell_index + 1 >= len(args):
                    raise ConfigError(f"{source}: shell -c lacks command")
                for command in shell_commands(args[shell_index + 1]):
                    inspect_command(command, root, cwd, source, inventory, ref)
            elif args and not args[0].startswith("-"):
                check_source(args[0], root, cwd, source, inventory, ref)
        case python if re.fullmatch(r"python(?:3(?:\.\d+)?)?", python):
            if "-c" in args:
                index = args.index("-c") + 1
                if index == len(args):
                    raise ConfigError(f"{source}: Python -c lacks code")
                for node in ast.walk(ast.parse(args[index])):
                    if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                        continue
                    if node.func.attr not in {"run", "check_output", "check_call", "Popen"}:
                        continue
                    values = node.args[0].elts if node.args and isinstance(node.args[0], (ast.List, ast.Tuple)) else []
                    if not values or not isinstance(values[0], ast.Constant) or not isinstance(values[0].value, str):
                        raise ConfigError(f"{source}: dynamic subprocess cannot be inventoried")
                    inspect_command([values[0].value], root, cwd, source, inventory, ref)
            elif "-m" not in args:
                script = next((a for a in args if not a.startswith("-")), None)
                if script:
                    check_source(script, root, cwd, source, inventory, ref)
            if "--gate-check" in args:
                inspect_command(args[args.index("--gate-check") + 1:], root, cwd, source, inventory, ref)
        case "cargo":
            inventory.tool("rustc", source)
            if args and args[0] in {"fmt", "clippy"}:
                inventory.tool("cargo-" + args[0], source)
    for i, arg in enumerate(args[:-1]):
        if arg == "--manifest-path":
            check_source(args[i + 1], root, cwd, source, inventory, ref)


def collect_gate(path, name, workspace, inventory):
    data = load_gate(path, name)
    root = path.parent
    aliases = data.get("siblings", {})
    check_environment(data.get("env", {}), root, root, str(path), inventory, aliases)
    for kind in ("check", "report"):
        for cmd in data.get(kind, []):
            source = f"{path}: {cmd['name']}"
            cwd = root / cmd.get("cwd", ".")
            if "cwd" in cmd:
                check_source(cmd["cwd"], root, root, source, inventory)
            check_environment(cmd.get("env", {}), root, cwd, source, inventory, aliases)
            inspect_command(cmd["argv"], root, cwd, source, inventory)
    for alias, pin in data.get("siblings", {}).items():
        sibling = workspace / pin.get("repo", alias)
        inventory.pin(sibling, pin["sha"], str(path))
        for filename in pin.get("files", {}):
            inventory.path(sibling / filename, str(path), ref=(sibling, pin["sha"]))
        for cmd in pin.get("build", []):
            source = f"{path}: {alias} {cmd['name']}"
            cwd = sibling / cmd.get("cwd", ".")
            ref = (sibling, pin["sha"])
            if "cwd" in cmd:
                check_source(cmd["cwd"], sibling, sibling, source, inventory, ref)
            check_environment(cmd.get("env", {}), sibling, cwd, source, inventory, aliases)
            inspect_command(cmd["argv"], sibling, cwd, source, inventory, ref)
    inventory.found.append(dict(label=str(path), path=str(path), version="schema 1 parsed", source=str(path)))


def toolchain_repair(directory, major):
    if ".rustup/toolchains/" in str(directory):
        toolchain = str(directory).split(".rustup/toolchains/", 1)[1].split("/", 1)[0]
        return [["rustup", "component", "add", "llvm-tools", "--toolchain", toolchain]]
    if ".julia/artifacts/" in str(directory) and major == 20:
        # Published legality toolchain's LLVM_full_jll provider (host-provisioning.md).
        project = str(Path.home() / ".local/share/bennett-llvm20")
        return [["julia", f"--project={project}", "-e",
                 'using Pkg; Pkg.add(PackageSpec(name="LLVM_full_jll", version="20.1.8"))']]
    return [["sudo", "apt-get", "install", "-y", f"clang-{major}", f"llvm-{major}-dev",
             f"libclang-{major}-dev", f"libpolly-{major}-dev", f"lld-{major}"]]


def toolchain_directory(value, source):
    if value.startswith("$HOME/"):
        home = os.environ.get("HOME")
        if not home:
            raise ConfigError(f"{source}: HOME is unset; set HOME to resolve {value}")
        value = str(Path(home) / value[len("$HOME/"):])
    directory = Path(value).expanduser()
    if not directory.is_absolute() or "$" in str(directory):
        raise ConfigError(f"{source}: expected an absolute or $HOME/ directory, got {value!r}")
    return directory


def collect_toolchains(path, inventory):
    data = tomllib.loads(path.read_text())
    if not data:
        raise ConfigError(f"{path}: no LLVM toolchains declared")
    for section, cfg in data.items():
        match = re.fullmatch(r"llvm(\d+)", section)
        if not match:
            raise ConfigError(f"{path}: unknown toolchain section {section}")
        table(cfg, {"bin", "frontend_bin"}, f"{path}.{section}")
        if not isinstance(cfg.get("bin"), str) or not cfg["bin"]:
            raise ConfigError(f"{path}.{section}: bin must be a nonempty directory path")
        if "frontend_bin" in cfg and (not isinstance(cfg["frontend_bin"], str) or not cfg["frontend_bin"]):
            raise ConfigError(f"{path}.{section}: frontend_bin must be a nonempty directory path")
        major = int(match[1])
        directory = toolchain_directory(cfg["bin"], f"{path}.{section}.bin")
        install = toolchain_repair(directory, major)
        for tool in ("opt", "llc"):
            inventory.tool(str(directory / tool), str(path), major, install)
        if "frontend_bin" in cfg:
            frontend = toolchain_directory(cfg["frontend_bin"], f"{path}.{section}.frontend_bin")
            install = toolchain_repair(frontend, major)
            for tool in ("clang", "clang++", "llvm-config"):
                inventory.tool(str(frontend / tool), str(path), major, install)
            cmake = frontend.parent / "lib/cmake/llvm/LLVMConfig.cmake"
            if not cmake.is_file():
                inventory.gap(str(cmake), f"LLVM {major} development config required by {path}", install)
            else:
                inventory.found.append(dict(label=str(cmake), path=str(cmake), version=f"LLVM {major} CMake config present", source=str(path)))
            inventory.tool("cmake", str(path))


def check_infrastructure(inventory):
    for name in INFRASTRUCTURE:
        inventory.tool(name, "gate / Beads infrastructure")
    probes = {
        "bwrap": ["--dev-bind", "/", "/", "--die-with-parent", "--", "/bin/true"],
        "systemd-run": ["--user", "--quiet", "--wait", "--pipe", "/bin/true"],
    }
    for name, args in probes.items():
        path = shutil.which(name)
        if not path:
            continue  # The missing executable is already a consolidated gap.
        try:
            result = run([path, *args])
            if result.returncode:
                inventory.gap(name + " functional probe", (result.stdout + result.stderr).strip())
            else:
                inventory.found.append(dict(label=name + " functional probe", path=path,
                                            version="PASS", source="gate infrastructure"))
        except OSError as error:
            inventory.gap(name + " functional probe", str(error))


def collect(args):
    inventory = Inventory()
    onboarding = META / "docs/onboarding.md"
    try:
        documents = re.findall(r"\[[^\]]+\]\((process/[^)#]+\.md)\)", onboarding.read_text())
        if not documents:
            raise ConfigError("no process documents linked from onboarding")
        for relative in dict.fromkeys(documents):
            path = onboarding.parent / relative
            if not path.is_file():
                inventory.gap(str(path), f"missing process document required by {onboarding}")
            else:
                inventory.path(path, str(onboarding))
    except (OSError, ValueError) as error:
        inventory.gap(str(onboarding), str(error))
    check_infrastructure(inventory)
    try:
        manifest = tomllib.loads(args.manifest.read_text())
        table(manifest, {"repos"}, str(args.manifest))
        repos = manifest.get("repos")
        if not isinstance(repos, dict) or not repos:
            raise ConfigError(f"{args.manifest}: repos must be a nonempty table")
        for name, cfg in repos.items():
            table(cfg, {"path", "language", "depends_on", "pinned", "remote", "info_only"}, name)
            if "info_only" in cfg and type(cfg["info_only"]) is not bool:
                raise ConfigError(f"{name}: info_only must be boolean")
            if cfg.get("info_only"):
                continue
            relative = cfg.get("path")
            if not isinstance(relative, str) or Path(relative).is_absolute() or ".." in Path(relative).parts:
                raise ConfigError(f"{name}: path must stay inside workspace")
            path = args.workspace / relative / "gate.toml"
            try:
                collect_gate(path, name, args.workspace, inventory)
            except (OSError, ValueError, SyntaxError) as error:
                inventory.gap(str(path), str(error))
    except (OSError, ValueError) as error:
        inventory.gap(str(args.manifest), str(error))
    path = args.workspace / "bennett-dialect-spec/corpus/legality/toolchains.toml"
    try:
        collect_toolchains(path, inventory)
    except (OSError, ValueError) as error:
        inventory.gap(str(path), str(error))
    return dict(workspace=str(args.workspace), found=inventory.found, gaps=inventory.gaps)


def main():
    parser = argparse.ArgumentParser(description="Check host tools declared by all main-checkout gates and LLVM toolchains; never run gates.")
    parser.add_argument("--workspace", type=Path, default=META.parent)
    parser.add_argument("--manifest", type=Path, default=META / "manifest.toml")
    parser.add_argument("--json", action="store_true", help="machine-readable inventory and repair steps")
    args = parser.parse_args()
    report = collect(args)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for item in report["found"]:
            print(f"FOUND {item['label']}: {item['version']} [{item['source']}]")
        if report["gaps"]:
            print(f"\nGAPS ({len(report['gaps'])}):")
            for gap in report["gaps"]:
                print(f"- {gap['label']}: {gap['reason']}")
                for step in gap["install"]:
                    print(f"  install: {shlex.join(step)}")
                if not gap["install"]:
                    print("  install: manual repair required; no verified automatic provider")
        else:
            print("PASS: all declared host prerequisites found (not a gate verdict)")
    return int(bool(report["gaps"]))


sys.exit(main())
PY
