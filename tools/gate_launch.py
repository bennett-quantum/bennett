#!/usr/bin/env python3
"""Admit and launch a detached gate service, with atomic completion events."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import signal
import subprocess
import sys
import tempfile
import time

# Explicit local imports also work under python -I and when loaded by test fixtures.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import admit
import gate_run

atomic_json = gate_run.atomic_json
WAIT_POLL_SECONDS = 1  # Completion-file polling cadence; no verdict time limit.


class LaunchError(Exception):
    pass


def utc():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def unit_name(repo, sha, tier):
    name = re.sub('[^a-zA-Z0-9_-]', '-', Path(repo).name)
    identity = hashlib.sha256(os.fsencode(Path(repo).resolve())).hexdigest()[:8]
    return f'bennett-gate-{name}-{identity}-{sha[:12]}-{tier}.service'


def install_runtime(base):
    """Snapshot service code so removing/editing the caller checkout cannot lose completion."""
    sources = {name: Path(__file__).with_name(name).read_bytes()
               for name in ('gate_launch.py', 'gate_run.py', 'admit.py')}
    identity = hashlib.sha256(b''.join(sources.values())).hexdigest()
    parent = base / 'runtime'
    parent.mkdir(parents=True, exist_ok=True)
    destination = parent / identity
    if destination.exists():
        for name, data in sources.items():
            if (destination / name).read_bytes() != data:
                raise LaunchError(f'service runtime changed: {destination / name}')
    else:
        with tempfile.TemporaryDirectory(dir=parent) as tmp:
            pending = Path(tmp) / 'code'
            pending.mkdir()
            for name, data in sources.items():
                path = pending / name
                path.write_bytes(data)
                path.chmod(0o444)
            pending.rename(destination)
    return destination / 'gate_launch.py'


def start(repo, sha=None, tier='pre-merge', launcher=subprocess.run, workspace=None):
    repo, discovered = gate_run.repo_paths(repo)
    workspace = Path(workspace or discovered)
    sha = gate_run.git(repo, 'rev-parse', '--verify', f'{sha or "HEAD"}^{{commit}}')
    unit = unit_name(repo, sha, tier)
    base = admit.state_dir(workspace)
    request_path = base / 'admissions' / (unit + '.json')
    # Serialize admission measurement + reservation + service launch, not gate execution.
    with gate_run.Lock(base / 'admission.lock'):
        if request_path.exists() and not (base / 'events' / (unit + '.json')).exists():
            props = admit.unit_properties(unit)
            if props['ActiveState'] in admit.ACTIVE_STATES:
                raise LaunchError(f'{unit} is already running')
        allowed, reason, expected = admit.assess(repo, workspace, tier)
        print(('ADMIT ' if allowed else 'WAIT ') + reason, file=sys.stderr, flush=True)
        if not allowed:
            raise LaunchError('WAIT ' + reason)
        for old in (base / 'events' / (unit + '.json'), request_path.with_name(unit + '.outcome.json')):
            old.unlink(missing_ok=True)
        owner = Path(gate_run.git(repo, 'rev-parse', '--path-format=absolute', '--git-common-dir')).parent
        request = {'repo': str(repo), 'repo_name': owner.name, 'sha': sha, 'tier': tier,
                   'started_utc': utc(), 'expected_peak': expected['peak_bytes'],
                   'expected_disk': expected['disk_bytes'], 'admission_reason': reason,
                   'record_path': str(repo / '.tmp/gate/records' / (sha + '.json')),
                   'workspace': str(workspace)}
        try:
            atomic_json(request_path, request)
            executable = str(install_runtime(base))
            # systemd parses ExecStopPost as command words. Quote each word for paths with spaces.
            def systemd_quote(arg):
                return '"' + str(arg).replace('\\', '\\\\').replace('"', '\\"').replace('%', '%%').replace('$', '$$') + '"'
            stop = ' '.join(systemd_quote(x) for x in (sys.executable, '-I', executable, 'complete', '--request', request_path))
            argv = ['systemd-run', '--user', '--collect', '--unit=' + unit,
                    '--property=Type=exec', '--property=MemoryAccounting=yes', '--property=CPUAccounting=yes',
                    '--property=KillMode=control-group',
                    '--property=UnsetEnvironment=' + ' '.join(gate_run.HEADLESS),
                    '--property=ExecStopPost=' + stop,
                    # A --user service starts from the user manager's environment, not this process's: forward the
                    # toolchain lookup explicitly (cargo, clang, julia live under the caller's PATH/HOME).
                    *(f'--setenv={k}={os.environ[k]}' for k in ('PATH', 'HOME') if k in os.environ),
                    '--', sys.executable, '-I', executable, 'worker', '--request', str(request_path)]
            env = {k: v for k, v in os.environ.items() if k not in gate_run.HEADLESS}
            result = launcher(argv, capture_output=True, text=True, env=env,
                              timeout=admit.CONTROL_TIMEOUT_SECONDS)
            if result.returncode:
                raise LaunchError(f'systemd-run failed: {result.stderr.strip()}')
        except (OSError, subprocess.SubprocessError, LaunchError) as error:
            atomic_json(request_path.with_name(unit + '.outcome.json'), {'exit': 3, 'error': str(error)})
            complete(request_path, query=lambda _: {})
            raise LaunchError(f'systemd launch: {error}') from error
        except BaseException as error:  # interrupted after admission: publish the outcome, then propagate
            atomic_json(request_path.with_name(unit + '.outcome.json'), {'exit': 3, 'error': f'interrupted: {error!r}'})
            complete(request_path, query=lambda _: {})
            raise
    return unit


def trusted_record(request):
    path = Path(request['record_path'])
    if not path.exists():
        return None
    record = admit.read_json(path)
    if path.stat().st_mtime_ns <= request.get('record_mtime_before', -1):
        return None
    if (record.get('sha') != request['sha'] or record.get('tier', 'pre-merge') != request['tier']
            or record.get('started_utc', '') < request['started_utc']):
        return None
    return record


def worker(request_path, runner=subprocess.run):
    request = admit.read_json(request_path)
    argv = [sys.executable, '-I', str(Path(__file__).with_name('gate_run.py')), 'run',
            '--repo', request['repo'], '--sha', request['sha'], '--tier', request['tier']]
    env = {k: v for k, v in os.environ.items() if k not in gate_run.HEADLESS}
    env['BENNETT_GATE_WORKSPACE'] = request.get('workspace', str(request_path.parents[3]))
    outcome, record = {}, None
    before = Path(request["record_path"])
    request["record_mtime_before"] = before.stat().st_mtime_ns if before.exists() else -1
    try:
        result = runner(argv, env=env, stdin=subprocess.DEVNULL)
        code = result.returncode if result.returncode >= 0 else 128 - result.returncode
        record = trusted_record(request)
        if code == 1 and record and any(c['exit'] == 124 for c in record.get('checks', [])):
            code = 124
        outcome['exit'] = code
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        outcome.update(exit=3, error=f'{type(error).__name__}: {error}')
    try:
        outcome['disk_bytes'] = gate_run.disk_bytes(Path(request['repo']) / '.tmp')
        record_disk = record.get('disk_bytes') if record else None
        if isinstance(record_disk, (int, float)):
            outcome['disk_bytes'] = max(outcome['disk_bytes'], record_disk)
    except OSError as error:
        outcome['disk_bytes'] = {'unavailable': str(error)}
    outcome['peak_rss_kib'] = gate_run.receipt_probe(
        'peak_rss_kib', lambda: resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    atomic_json(request_path.with_name(request_path.stem + '.outcome.json'), outcome)
    return outcome['exit']


def service_exit(service_result, exit_code, exit_status):
    if service_result == 'timeout':
        return 124
    if exit_code in ('killed', 'dumped'):
        try:
            number = int(exit_status) if exit_status.isdigit() else getattr(signal, 'SIG' + exit_status)
            return 128 + number
        except (AttributeError, ValueError):
            return 255
    if exit_code == 'exited' and exit_status.isdigit():
        return int(exit_status)
    return 255


def complete(request_path, service_result=None, exit_code=None, exit_status=None, query=admit.unit_properties):
    request = admit.read_json(request_path)
    unit = request_path.stem
    event_path = request_path.parent.parent / 'events' / (unit + '.json')
    if event_path.exists():
        return admit.read_json(event_path)
    outcome_path = request_path.with_name(unit + '.outcome.json')
    outcome = admit.read_json(outcome_path) if outcome_path.exists() else {}
    service_result = service_result or os.environ.get('SERVICE_RESULT', 'unknown')
    code = outcome.get('exit', service_exit(service_result, exit_code or os.environ.get('EXIT_CODE', ''),
                                           exit_status or os.environ.get('EXIT_STATUS', '')))
    if not outcome and code != 124 and not 128 < code < 193:
        code = 255  # Wrapper crashed before publishing a gate outcome.
    # A crash of the wrapper after the gate exited must not report the gate as PASS.
    if (service_result in ('signal', 'core-dump', 'timeout', 'oom-kill', 'watchdog')
            or service_result not in ('success', 'unknown') and code == 0):
        code = service_exit(service_result, exit_code or os.environ.get('EXIT_CODE', ''),
                            exit_status or os.environ.get('EXIT_STATUS', ''))
    results = {0: 'pass', 1: 'fail', 3: 'setup-error', 124: 'hang-guard'}
    result = results.get(code, 'signal' if 128 < code < 193 else 'unit-crash')
    event = {k: request[k] for k in ('repo', 'repo_name', 'sha', 'tier', 'record_path', 'started_utc')}
    event.update(unit=unit, exit=code, result=result, finished_utc=utc(), service_result=service_result)
    event.update({k: v for k, v in outcome.items() if k != 'exit'})
    try:
        peak = query(unit).get('MemoryPeak')
        if peak is not None and peak.isdigit():
            event['peak_rss_kib'] = int(peak) // 1024
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        event['measurement_error'] = str(error)
    if 'disk_bytes' not in event:
        event['disk_bytes'] = gate_run.receipt_probe(
            'disk_bytes', lambda: gate_run.disk_bytes(Path(request['repo']) / '.tmp'))
    for field in ('peak_rss_kib', 'disk_bytes'):
        event.setdefault(field, {'unavailable': 'unit exited before measurement'})
    atomic_json(event_path, event)
    return event


def wait(unit, workspace):
    if Path(unit).name != unit or not unit.startswith('bennett-gate-') or not unit.endswith('.service'):
        raise LaunchError(f'invalid gate unit {unit!r}')
    path = admit.state_dir(workspace) / 'events' / (unit + '.json')
    if not (path.parent.parent / 'admissions' / (unit + '.json')).exists():
        raise LaunchError(f'unknown gate unit {unit}')
    while not path.exists():
        time.sleep(WAIT_POLL_SECONDS)
    return admit.read_json(path)['exit']


def status(workspace, query=admit.unit_properties):
    base = admit.state_dir(workspace)
    rows = []
    for path in sorted((base / 'admissions').glob('*.json')):
        if path.name.endswith('.outcome.json'):
            continue
        event_path = base / 'events' / path.name
        if event_path.exists():
            rows.append(dict(admit.read_json(event_path), state='finished'))
        else:
            props = query(path.stem)
            rows.append(dict(admit.read_json(path), unit=path.stem,
                             state='running' if props['ActiveState'] in admit.ACTIVE_STATES else props['ActiveState']))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--workspace', type=Path, default=Path(__file__).resolve().parents[2])
    sub = ap.add_subparsers(dest='command', required=True)
    launch = sub.add_parser('start')
    launch.add_argument('--repo', required=True, type=Path)
    launch.add_argument('--sha')
    launch.add_argument('--tier', choices=('pre-merge', 'full'), default='pre-merge')
    waiting = sub.add_parser('wait')
    waiting.add_argument('unit')
    sub.add_parser('status')
    for name in ('worker', 'complete'):
        parser = sub.add_parser(name)
        parser.add_argument('--request', required=True, type=Path)
    args = ap.parse_args()
    try:
        if args.command == 'start':
            print(start(args.repo, args.sha, args.tier))
            return 0
        if args.command == 'wait':
            return wait(args.unit, args.workspace)
        if args.command == 'status':
            print(json.dumps(status(args.workspace), indent=1))
            return 0
        if args.command == 'worker':
            return worker(args.request)
        complete(args.request)
        return 0
    except (LaunchError, gate_run.GateError, OSError, ValueError, KeyError, subprocess.SubprocessError, RuntimeError) as error:
        print(f'gate-launch: {error}', file=sys.stderr)
        return 1 if str(error).startswith('WAIT ') else 3


if __name__ == '__main__':
    sys.exit(main())
