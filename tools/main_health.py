#!/usr/bin/env python3
"""Detect post-merge regressions on pushed mains; seed reviewed known-red identities."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time
import tomllib

POLL_SECONDS = 60  # Revision polling only; never a verdict deadline.
GUARD_TABLES = ('.tmp/main-health/hang-guards.toml', 'tests/timeouts.toml')
LADDER_REPOS = ('bennett-plugin', 'bennett-vm', 'bennett-runtimes',
                'bennett-driver', 'bennett-isa-spec')
RUNGS = ('rung-1', 'rung-2')


class HealthError(Exception):
    pass


def utc():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, prefix=path.name + '.', delete=False) as out:
        pending = Path(out.name)
        try:
            json.dump(value, out, indent=2)
            out.write('\n')
            out.flush()
            os.fsync(out.fileno())
        except BaseException:
            pending.unlink(missing_ok=True)
            raise
    pending.replace(path)


def environment(tmp=None, workspace=None):
    env = {k: v for k, v in os.environ.items()
           if k not in {'DISPLAY', 'WAYLAND_DISPLAY', 'DBUS_SESSION_BUS_ADDRESS', 'BROWSER',
                        'GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'CARGO_TARGET_DIR',
                        'PYTHONOPTIMIZE'} and not k.startswith('BENNETT_GATE_')}
    if tmp is not None:
        Path(tmp).mkdir(parents=True, exist_ok=True)
        env['TMPDIR'] = str(tmp)
    if workspace is not None:
        env['BENNETT_GATE_WORKSPACE'] = str(workspace)
    return env


def main_checkout(repo):
    repo = Path(repo).resolve()
    pointer = repo / '.git'
    if not pointer.is_file():
        return repo
    text = pointer.read_text().strip()
    if not text.startswith('gitdir: '):
        raise HealthError(f'invalid worktree pointer: {pointer}')
    directory = (repo / text.removeprefix('gitdir: ')).resolve()
    return (directory / (directory / 'commondir').read_text().strip()).resolve().parent


def guard_seconds(repo, guard_class):
    paths = [main_checkout(repo) / GUARD_TABLES[0], Path(repo) / GUARD_TABLES[1]]
    path = next((p for p in paths if p.is_file()), None)
    if path is None:
        raise HealthError(f'{Path(repo).name}: missing hang-guard class table ({", ".join(GUARD_TABLES)})')
    try:
        table = tomllib.loads(path.read_text())
        row = table['classes'][guard_class]
        cap = row['seconds'] * table['machine_config_factor']
        samples = row['measurements']
        if not table['machine'] or not samples:
            raise ValueError('machine and measurements required')
        numbers = [table['machine_config_factor'], row['seconds'], cap]
        for sample in samples:
            if not all(sample[k] for k in ('machine', 'date', 'command')):
                raise ValueError('uncited measurement')
            numbers.append(sample['wall_seconds'])
        if any(isinstance(n, bool) or not isinstance(n, (int, float)) or not math.isfinite(n) or n <= 0
               for n in numbers):
            raise ValueError('measurements and limits must be finite and positive')
        if cap < 10 * max(s['wall_seconds'] for s in samples):
            raise ValueError('guard must be at least 10x measured wall seconds')
        return cap
    except (KeyError, TypeError, ValueError) as error:
        raise HealthError(f'{path.name}: invalid {guard_class} hang guard: {error}') from error


def control(argv, cwd, allowed=(0,)):
    proc = subprocess.run(list(map(str, argv)), cwd=cwd, env=environment(), stdin=subprocess.DEVNULL,
                          capture_output=True, text=True, timeout=guard_seconds(cwd, 'short'))
    if proc.returncode not in allowed:
        raise HealthError(f'{argv[0]}: exit {proc.returncode}: {proc.stderr.strip()}')
    return proc


def git(repo, *args):
    return control(['git', '-c', 'core.hooksPath=/dev/null', '-C', repo, *args], repo).stdout.strip()


def fetch_main(repo):
    git(repo, 'fetch', '--no-tags', 'origin', '+refs/heads/main:refs/remotes/origin/main')
    return git(repo, 'rev-parse', '--verify', 'refs/remotes/origin/main^{commit}')


@contextmanager
def single_runner(state):
    with (state / 'runner.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise HealthError('another main-health runner owns this state directory') from error
        yield


def detached(repo, sha, state, name):
    target = state / 'checkouts' / name / sha / name
    if target.exists():
        if git(target, 'rev-parse', 'HEAD') != sha or git(target, 'status', '--porcelain', '--untracked-files=no'):
            raise HealthError(f'modified cached checkout: {name}/{sha}')
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        git(repo, 'worktree', 'add', '--detach', str(target), sha)
    return target


def load_baseline(path):
    if not Path(path).is_file():
        raise HealthError(f'missing known-red baseline: {path}')
    try:
        data = tomllib.loads(Path(path).read_text())
        if set(data) - {'schema', 'red'} or data['schema'] != 1:
            raise ValueError('expected schema = 1 and [[red]] entries')
        result = {}
        for red in data.get('red', []):
            if set(red) - {'scope', 'check', 'sha', 'shas', 'bead'}:
                raise ValueError('unknown baseline field')
            if not all(isinstance(red.get(k), str) and red[k].strip() for k in ('scope', 'check', 'bead')):
                raise ValueError('scope, check and bead must be nonempty strings')
            shas = red.get('shas', {})
            if not isinstance(shas, dict):
                raise ValueError('shas must be a revision table')
            for sha in [red['sha'], *shas.values()]:
                if not isinstance(sha, str) or len(sha) != 40 or any(c not in '0123456789abcdef' for c in sha):
                    raise ValueError('baseline SHAs must be full lowercase commit IDs')
            key = (red['scope'], red['check'])
            if key in result:
                raise ValueError(f'duplicate baseline identity: {key}')
            result[key] = red
        return result
    except (ValueError, KeyError, TypeError) as error:
        raise HealthError(f'invalid baseline {Path(path).name}: {error}') from error


def classify(scope, items, baseline):
    result = {}
    for name, item in items.items():
        entry = baseline.get((scope, name))
        code = item['exit']
        if code == 0:
            verdict = 'FIXED' if entry else 'PASS'
        elif code == 124 or code < 0 or code > 128:
            verdict = 'UNKNOWN'
        else:
            verdict = 'KNOWN-RED' if entry else 'NEW-RED'
        result[name] = dict(item, classification=verdict)
        if entry:
            result[name]['baseline'] = entry
    # A short-circuit gate cannot prove that an unexecuted baseline check is fixed.
    for (owner, name), entry in baseline.items():
        if owner == scope and name not in result:
            result[name] = dict(classification='UNKNOWN', baseline=entry,
                                detail='baseline check/case absent from this run; not proven FIXED')
    return result


def gate_items(record, sha):
    if record.get('sha') != sha or record.get('tier') != 'full' or record.get('fresh') is not True:
        raise HealthError('gate record does not match requested SHA/full/fresh run')
    items = {}
    for item in record.get('checks', []):
        name, code = item.get('name'), item.get('exit')
        if not isinstance(name, str) or not name or name in items or type(code) is not int:
            raise HealthError('gate record has missing/duplicate check name or invalid exit')
        items[name] = item
    if not items:
        raise HealthError('gate record has no check results')
    return items


def ladder_items(report):
    items = {}
    def walk(value, parts):
        if not isinstance(value, dict):
            raise HealthError('ladder result must be a status tree')
        if 'status' in value:
            status = value['status']
            if status not in ('PASS', 'N/A', 'FAIL', 'BLOCKED', 'UNKNOWN', 'TIMEOUT'):
                raise HealthError(f'unknown ladder status: {status}')
            code = 0 if status in ('PASS', 'N/A') else (124 if status in ('UNKNOWN', 'TIMEOUT') else 1)
            key = '/'.join(parts)
            if key in items:
                raise HealthError(f'duplicate ladder identity: {key}')
            items[key] = dict(value, exit=code)
        else:
            for name, child in value.items():
                walk(child, [*parts, str(name)])
    for field, prefix in (('stages', 'stage'), ('cases', 'case')):
        if field in report:
            walk(report[field], [prefix])
    if not items:
        raise HealthError('ladder report has no stage/case results')
    return items


def ladder_argv(stub, revisions, help_text, output):
    import re
    argv = ['bash', str(stub), '--output', str(output), '--jobs', str(max(1, len(os.sched_getaffinity(0)) // 2))]
    for name, sha in revisions.items():
        flag = '--' + name.removeprefix('bennett-') + '-rev'
        if flag not in re.findall(r'--[a-z0-9-]+', help_text):
            raise HealthError(f'ladder lacks {flag}; cannot attest pushed main')
        argv.extend([flag, sha])
    return argv
def cache_isolation(checkout):
    """Keep this nested cache visible after the pinned tool masks the live meta checkout.

    The pinned tool's prefix skips only top-level own_roots. Restore just the detached
    root (including its pinned-sibling cache), never the containing live checkout.
    Reject unfamiliar prefixes instead of accidentally weakening sibling isolation.
    """
    wrapper = checkout / ".tmp/main-health-bwrap"
    wrapper.parent.mkdir(parents=True, exist_ok=True)
    wrapper.write_text(f'''#!{sys.executable}
import os
import sys
args = sys.argv[1:]
if args[:4] != ["--dev-bind", "/", "/", "--die-with-parent"]:
    sys.exit("main-health: unsupported gate isolation prefix")
index = 4
while index < len(args) and args[index] == "--tmpfs":
    if args[index + 2:index + 3] != ["--bind-try"] or len(args[index:index + 5]) != 5:
        sys.exit("main-health: unsupported gate isolation mount")
    index += 5
if args[index:index + 1] == ["--chdir"]:
    if len(args[index:]) < 4 or args[index + 2] != "--":
        sys.exit("main-health: unsupported gate isolation chdir")
elif index >= len(args) or args[index].startswith("--"):
    sys.exit("main-health: unsupported gate isolation command")
os.execvp("bwrap", ["bwrap", *args[:index], "--bind", {str(checkout)!r}, {str(checkout)!r}, *args[index:]])
''')
    wrapper.chmod(0o755)
    return str(wrapper)



def launcher_modules():
    # Lazy import keeps the immutable detached health worker stdlib-only.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import gate_launch
    return gate_launch


def launch_gate(checkout, sha, argv, log, env, record_path):
    """Use gate_launch's admission/ExecStopPost protocol for fresh gates and ladders.

    Its stock worker has neither --fresh nor ladder support. The public injected
    launcher substitutes our worker, retaining reservations, accounting and events.
    """
    launch = launcher_modules()
    workspace = Path(env['BENNETT_GATE_WORKSPACE'])
    base = launch.admit.state_dir(workspace)
    source = Path(__file__).read_bytes()
    runtime = base / 'health-runtime' / hashlib.sha256(source).hexdigest() / 'main_health.py'
    runtime.parent.mkdir(parents=True, exist_ok=True)
    if runtime.exists() and runtime.read_bytes() != source:
        raise HealthError('immutable health runtime changed')
    if not runtime.exists():
        with tempfile.NamedTemporaryFile(dir=runtime.parent, delete=False) as out:
            pending = Path(out.name)
            out.write(source)
        pending.chmod(0o444)
        pending.replace(runtime)
    def service_launcher(command, **kwargs):
        command = list(command)
        index = command.index('worker')
        request_path = Path(command[index + 2])
        request = json.loads(request_path.read_text())
        request.update(health_argv=argv, health_env=env, health_log=str(log),
                       health_timeout=guard_seconds(checkout, 'eternal'),
                       health_grace=guard_seconds(checkout, 'short'), record_path=str(record_path))
        atomic_json(request_path, request)
        command[index - 1] = str(runtime)
        return subprocess.run(command, **kwargs)
    try:
        unit = launch.start(checkout, sha, tier='full', launcher=service_launcher, workspace=workspace)
        launch.wait(unit, workspace)
        return json.loads((base / 'events' / (unit + '.json')).read_text())
    except (launch.LaunchError, launch.gate_run.GateError, RuntimeError) as error:
        raise HealthError(str(error)) from error


def worker(request_path):
    """Detached service worker; ExecStopPost publishes completion even if we crash."""
    request = json.loads(Path(request_path).read_text())
    outcome = {}
    log = Path(request['health_log'])
    log.parent.mkdir(parents=True, exist_ok=True)
    env = request['health_env']
    try:
        # timeout kills the command's process group; systemd KillMode controls the cgroup.
        command = ['timeout', '--signal=TERM', f'--kill-after={request["health_grace"]}s',
                   str(request['health_timeout']), *request['health_argv']]
        with log.open('a') as output:
            output.write('command: ' + json.dumps(command) + '\n')
            output.flush()
            proc = subprocess.run(command, cwd=request['repo'], env=env, stdin=subprocess.DEVNULL,
                                  stdout=output, stderr=subprocess.STDOUT)
        outcome['exit'] = proc.returncode if proc.returncode >= 0 else 128 - proc.returncode
        record_path = Path(request['record_path'])
        if record_path.is_file():
            record = json.loads(record_path.read_text())
            if outcome['exit'] == 1 and any(c.get('exit') == 124 for c in record.get('checks', [])):
                outcome['exit'] = 124
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        outcome.update(exit=3, error=str(error))
    outcome['peak_rss_kib'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    atomic_json(Path(request_path).with_name(Path(request_path).stem + '.outcome.json'), outcome)
    return outcome['exit']


def blank_row():
    return dict(sha='', shas={}, classification='UNKNOWN', checks={}, last_green={},
                new_reds=[], logs=[], detail='not checked')


def markdown(rows):
    lines = ['# Main health', '', '| Repo / ladder | Classification | SHA | Evidence |', '|---|---|---|---|']
    for name, row in rows.items():
        logs = ' '.join(f'[log]({p})' for p in row['logs'])
        lines.append(f'| {name} | {row["classification"]} | {row["sha"][:12]} | {logs} |')
        if row.get('detail'):
            lines.extend(['', f'{name}: {row["detail"]}'])
        for check, item in row['checks'].items():
            lines.extend(['', f'- {name} / {check}: {item["classification"]}'
                          + (f' · culprit merge {item["culprit_merge"]}' if item.get('culprit_merge') else '')])
            if item.get('attribution'):
                lines.append('  ' + json.dumps(item['attribution']))
            if item.get('baseline'):
                lines.append('  baseline bead: ' + item['baseline']['bead'])
        if row.get('table'):
            lines.extend(['', row['table']])
    return '\n'.join(lines) + '\n'


class Runner:
    def __init__(self, args, launcher=None):
        self.args = args
        self.meta = args.meta.resolve()
        self.workspace = self.meta.parent
        self.state = args.state_dir.resolve() if args.state_dir else self.meta / '.tmp/main-health'
        self.state.mkdir(parents=True, exist_ok=True)
        self.repos = tomllib.loads((self.meta / 'manifest.toml').read_text())['repos']
        import re
        for name, entry in self.repos.items():
            if not re.fullmatch(r'[A-Za-z0-9_.-]+', name) or not isinstance(entry.get('path'), str):
                raise HealthError(f'invalid manifest entry: {name}')
        self.selected = args.repos.split(',') if args.repos else ([] if args.ladder else
                        [n for n, e in self.repos.items() if not e.get('info_only', False)])
        self.rungs = args.ladder.split(',') if args.ladder else ([] if args.repos or args.ladder == '' else list(RUNGS))
        if any(n not in self.repos for n in self.selected):
            raise HealthError('selected repo absent from manifest')
        if any(n not in RUNGS for n in self.rungs):
            raise HealthError('unknown ladder rung')
        if not self.selected and not self.rungs:
            raise HealthError('no repos or ladder rungs selected')
        self.baseline_path = args.baseline or self.meta / 'health/known-reds.toml'
        self.baseline = load_baseline(self.baseline_path)
        self.launcher = launcher or launch_gate
        self.rows = {}

    def source(self, name):
        if name not in self.repos:
            raise HealthError(f'repo absent from manifest: {name}')
        return (self.workspace / self.repos[name]['path']).resolve()

    def run_evidence(self, name, revisions, log):
        repo = 'bennett-conformance' if name.startswith('ladder/') else name
        sha = revisions[repo]
        checkout = detached(self.source(repo), sha, self.state, name.replace('/', '-'))
        env = environment(self.state / 'tmp', self.workspace)
        record_path = checkout / '.tmp/gate/records' / (sha + '.json')
        if name.startswith('ladder/'):
            stub = checkout / 'ladder' / name.split('/')[1] / 'gate.sh'
            if not stub.is_file():
                raise HealthError(f'{name}: missing gate.sh')
            help_text = control(['bash', stub, '--help'], checkout).stdout
            output = log.with_suffix('')
            argv = ladder_argv(stub, {n: revisions[n] for n in LADDER_REPOS}, help_text, output)
            for n in LADDER_REPOS:
                link = checkout.parent / n
                if not link.exists():
                    link.symlink_to(self.source(n), target_is_directory=True)
        else:
            stub = checkout / 'scripts/pre-push'
            if not stub.is_file() or not (checkout / 'gate.toml').is_file():
                raise HealthError(f'{name}: missing gate.toml or scripts/pre-push')
            argv = ['bash', str(stub), '--sha', sha, '--tier', 'full', '--fresh']
            env['BENNETT_GATE_BWRAP'] = cache_isolation(checkout)
        # An old failure record must never impersonate a crashed fresh run.
        record_path.unlink(missing_ok=True)
        event = self.launcher(checkout, sha, argv, log, env, record_path)
        code = event['exit']
        if code not in (0, 1):
            raise HealthError(f'gate completion {event.get("result", "unknown")}, exit {code}: {event.get("error", "see log")}')
        tables = ''
        if name.startswith('ladder/'):
            reports = sorted(output.rglob('report.json'))
            if len(reports) != 1:
                raise HealthError(f'{name}: expected one fresh report.json, got {len(reports)}')
            items = ladder_items(json.loads(reports[0].read_text()))
            tables = '\n\n'.join(p.read_text() for p in sorted(output.rglob('table.md')))
            logs = [str(log), str(reports[0])]
        else:
            if not record_path.is_file():
                raise HealthError('gate exited without a fresh gate record')
            items = gate_items(json.loads(record_path.read_text()), sha)
            logs = [str(log), str(record_path)]
        if (code == 0) != all(i['exit'] == 0 for i in items.values()):
            raise HealthError('completion exit disagrees with check/case results')
        return items, logs, tables

    def attribute(self, name, check, green, revisions):
        info = dict(merges={}, gate_runs=0, cost='Full fresh gate/ladder per probe; gate_run has no per-check filter. '
                    'Propose --check NAME to reduce this cost. Binary search assumes a persistent regression; '
                    'the reported merge boundary is verified.')
        if not green:
            info['unavailable'] = 'no previous green observation for this check/case'
            return info
        candidates = {}
        for repo, sha in revisions.items():
            old = green.get(repo)
            if not old or old == sha:
                continue
            chain = git(self.source(repo), 'rev-list', '--first-parent', sha).splitlines()
            if old not in chain:
                info['unavailable'] = f'{repo}: last green is not on current first-parent chain'
                return info
            lines = git(self.source(repo), 'log', '--first-parent', '--merges', '--reverse',
                        '--format=%H %s', f'{old}..{sha}').splitlines()
            info['merges'][repo] = lines
            candidates[repo] = [line.split()[0] for line in lines]
        count = sum(map(len, candidates.values()))
        if not count:
            info['unavailable'] = 'no first-parent merges since last green; inspect direct main commits'
            return info
        if count == 1 and len([r for r in revisions if green.get(r) != revisions[r]]) == 1:
            repo = next(r for r, m in candidates.items() if m)
            merge = candidates[repo][0]
            # No intervening direct-main commits: the two observed results prove this boundary.
            if merge == revisions[repo] and git(self.source(repo), 'rev-parse', merge + '^1') == green[repo]:
                info['culprit_merge'] = merge
                return info
        info['max_probe_runs'] = sum(math.ceil(math.log2(len(m) + 1)) + 3 for m in candidates.values() if m)
        print(f'main-health: {name}/{check}: bisect cost <= {info["max_probe_runs"]} full fresh runs; '
              'no per-check filter available', file=sys.stderr, flush=True)
        def probe(vector):
            log = self.state / 'logs' / f'bisect-{time.time_ns()}.log'
            info['gate_runs'] += 1
            items, logs, _ = self.run_evidence(name, vector, log)
            info.setdefault('logs', []).extend(logs)
            if check not in items or items[check]['exit'] not in (0, 1):
                raise HealthError('target check/case not reached during bisect (gate short-circuits); '
                                  'a gate_run --check NAME filter is needed')
            return items[check]['exit'] == 0
        found = []
        try:
            for repo, merges in candidates.items():
                if not merges:
                    continue
                def at(sha):
                    return dict(revisions, **{repo: sha})
                if not probe(at(green[repo])):
                    info.setdefault('unresolved', []).append(f'{repo}: other moved repos keep target red at last green')
                    continue
                # Include S as a sentinel: a direct commit after the last merge must not be blamed on that merge.
                points = list(dict.fromkeys([*merges, revisions[repo]]))
                low, high = -1, len(points) - 1
                while high - low > 1:
                    mid = (low + high) // 2
                    if probe(at(points[mid])):
                        low = mid
                    else:
                        high = mid
                culprit = points[high]
                if culprit not in merges:
                    info.setdefault('unresolved', []).append(f'{repo}: direct main commit after last merge is red')
                    continue
                parent = git(self.source(repo), 'rev-parse', culprit + '^1')
                if not probe(at(parent)) or probe(at(culprit)):
                    info.setdefault('unresolved', []).append(f'{repo}: merge boundary is not green -> red')
                    continue
                found.append(culprit)
            if len(found) == 1 and not info.get('unresolved'):
                info['culprit_merge'] = found[0]
            else:
                info['unavailable'] = 'no unique verified culprit merge; inspect unresolved boundaries'
                info['candidate_culprits'] = found
        except (HealthError, OSError, ValueError, subprocess.SubprocessError) as error:
            info['unavailable'] = str(error)
        return info

    def check(self, name, revisions, previous):
        row = blank_row()
        row.update(sha=next(iter(revisions.values())), shas=revisions, when=utc(),
                   last_green=dict(previous['last_green']))
        log = self.state / 'logs' / f'{name.replace("/", "-")}-{time.time_ns()}.log'
        log.parent.mkdir(parents=True, exist_ok=True)
        row['logs'] = [str(log)]
        started = time.monotonic()
        try:
            items, logs, table = self.run_evidence(name, revisions, log)
            row.update(logs=logs, table=table, checks=classify(name, items, self.baseline), detail='')
            for check, item in row['checks'].items():
                if item['classification'] in ('PASS', 'FIXED'):
                    row['last_green'][check] = revisions.copy()
                elif item['classification'] == 'NEW-RED':
                    if self.args.command != 'seed':
                        attribution = self.attribute(name, check, row['last_green'].get(check), revisions)
                        item['attribution'] = attribution
                        if attribution.get('culprit_merge'):
                            item['culprit_merge'] = attribution['culprit_merge']
                    row['new_reds'].append(dict(check=check, **item))
            verdicts = {i['classification'] for i in row['checks'].values()}
            row['classification'] = next(v for v in ('NEW-RED', 'UNKNOWN', 'KNOWN-RED', 'FIXED', 'PASS') if v in verdicts)
        except (HealthError, OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
            row.update(classification='ERROR', detail=str(error))
            with log.open('a') as out:
                out.write(str(error) + '\n')
        row['duration_s'] = time.monotonic() - started
        return row

    def cycle(self):
        self.baseline = load_baseline(self.baseline_path)
        status = self.state / 'status.json'
        rows = json.loads(status.read_text())['rows'] if status.exists() else {}
        selected = [*self.selected, *(f'ladder/{r}' for r in self.rungs)]
        dependencies = {name: (('bennett-conformance', *LADDER_REPOS) if name.startswith('ladder/') else (name,))
                        for name in selected}
        names = set(n for group in dependencies.values() for n in group)
        revisions, errors = {}, {}
        with ThreadPoolExecutor(max_workers=len(names)) as pool:
            pending = {pool.submit(fetch_main, self.source(n)): n for n in names}
            for future in as_completed(pending):
                name = pending[future]
                try:
                    revisions[name] = future.result()
                except (HealthError, OSError, ValueError, subprocess.SubprocessError) as error:
                    errors[name] = str(error)
        vectors = {name: {n: revisions[n] for n in group if n in revisions} for name, group in dependencies.items()}
        changed = [name for name in selected if self.args.force or self.args.command == 'seed'
                   or any(n in errors for n in dependencies[name]) or name not in rows
                   or rows[name]['shas'] != vectors[name] or rows[name]['classification'] in ('ERROR', 'UNKNOWN')]
        if not changed:
            self.rows = {n: rows[n] for n in selected}
            return None
        with ThreadPoolExecutor(max_workers=len(changed)) as pool:
            pending = {}
            for name in changed:
                problems = {n: errors[n] for n in dependencies[name] if n in errors}
                if problems:
                    row = blank_row()
                    row.update(shas=vectors[name], classification='ERROR', detail=json.dumps(problems), when=utc())
                    row['last_green'] = rows.get(name, blank_row())['last_green']
                    rows[name] = row
                else:
                    pending[pool.submit(self.check, name, vectors[name], rows.get(name, blank_row()))] = name
            for future in as_completed(pending):
                rows[pending[future]] = future.result()
        self.rows = {n: rows[n] for n in selected}
        event = dict(schema=1, kind='main-health', finished_utc=utc(), tier='full', fresh=True,
                     changed=changed, rows=self.rows)
        atomic_json(self.workspace / 'bennett/.tmp/gates/events' / f'main-health-{time.time_ns()}.json', event)
        atomic_json(status, dict(schema=2, rows=rows))
        (self.state / 'status.md').write_text(markdown(rows))
        print(markdown(self.rows), flush=True)
        return self.exit_code()

    def exit_code(self):
        verdicts = {row['classification'] for row in self.rows.values()}
        if verdicts & {'ERROR', 'UNKNOWN'}:
            return 2
        return 1 if 'NEW-RED' in verdicts else 0

    def seed(self, bead):
        if not self.rows or any(r['classification'] in ('ERROR', 'UNKNOWN') for r in self.rows.values()):
            raise HealthError('cannot seed incomplete/errored evidence; rerun seed after resolving it')
        entries = dict(self.baseline)
        for scope, row in self.rows.items():
            for check, item in row['checks'].items():
                key = (scope, check)
                if item.get('exit', 0) == 0 or key in entries:
                    continue
                assigned = bead or next(iter(item.get('beads', [])), None)
                if not assigned:
                    raise HealthError(f'{scope}/{check}: seed requires --bead or a report bead')
                entries[key] = dict(scope=scope, check=check, sha=row['sha'], shas=row['shas'], bead=assigned)
        lines = ['# Known-red identities; FIXED entries are removed only by human review.', 'schema = 1', '']
        for key in sorted(entries):
            entry = entries[key]
            lines.append('[[red]]')
            for k in ('scope', 'check', 'sha', 'bead'):
                lines.append(f'{k} = {json.dumps(entry[k])}')
            if entry.get('shas'):
                lines.append('shas = { ' + ', '.join(f'{json.dumps(n)} = {json.dumps(s)}' for n, s in entry['shas'].items()) + ' }')
            lines.append('')
        self.baseline_path.parent.mkdir(parents=True, exist_ok=True)
        pending = self.baseline_path.with_suffix('.toml.new')
        pending.write_text('\n'.join(lines))
        pending.replace(self.baseline_path)
        self.baseline = load_baseline(self.baseline_path)
        # Seeding is an explicit review operation: apply the new identities to the
        # observed results immediately, without waiting for another main movement.
        for scope, row in self.rows.items():
            observed = {name: {k: v for k, v in item.items()
                               if k not in ('classification', 'baseline', 'attribution', 'culprit_merge')}
                        for name, item in row['checks'].items() if 'exit' in item}
            row['checks'] = classify(scope, observed, self.baseline)
            verdicts = {i['classification'] for i in row['checks'].values()}
            row['classification'] = next(v for v in ('NEW-RED', 'UNKNOWN', 'KNOWN-RED', 'FIXED', 'PASS') if v in verdicts)
            row['new_reds'] = [dict(check=name, **item) for name, item in row['checks'].items()
                               if item['classification'] == 'NEW-RED']
        status = self.state / 'status.json'
        rows = json.loads(status.read_text())['rows']
        rows.update(self.rows)
        atomic_json(status, dict(schema=2, rows=rows))
        (self.state / 'status.md').write_text(markdown(rows))
        print(f'main-health: seeded {len(entries)} known-red identities; review and commit the baseline', file=sys.stderr)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('run', 'seed', 'worker'))
    parser.add_argument('--request', type=Path)
    parser.add_argument('--meta', type=Path)
    parser.add_argument('--state-dir', type=Path, default=os.environ.get('BENNETT_MAIN_HEALTH_STATE_DIR'))
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--repos')
    parser.add_argument('--ladder')
    parser.add_argument('--once', action='store_true')
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--bead', help='bead for seeded reds without an embedded report bead')
    parser.add_argument('--tier', choices=('full',), default='full')
    parser.add_argument('--fresh', action='store_true', default=True, help='always enabled for main-health')
    args = parser.parse_args(argv)
    try:
        if args.command == 'worker':
            if not args.request:
                raise HealthError('worker requires --request')
            return worker(args.request)
        if args.meta is None:
            args.meta = main_checkout(Path(__file__).resolve().parents[1])
        runner = Runner(args)
        with single_runner(runner.state):
            while True:
                code = runner.cycle()
                if args.command == 'seed':
                    runner.seed(args.bead)
                    return 0
                if args.once:
                    return runner.exit_code() if code is None else code
                time.sleep(POLL_SECONDS)
    except (HealthError, OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(f'main-health: {error}', file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 2


if __name__ == '__main__':
    sys.exit(main())
