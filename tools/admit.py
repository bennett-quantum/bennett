#!/usr/bin/env python3
"""Gate resource admission. Decision policy is pure; probes fail closed with a reason."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

GIB = 1024 ** 3
# Resource headroom mandated by the gate contract / process rule 5.
MEMORY_HEADROOM_BYTES = 6 * GIB
DISK_HEADROOM_BYTES = 20 * GIB
LOAD_CPU_DIVISOR = 2
# No-history policy: reserve a substantial build on a 30 GiB machine, including
# pinned sibling builds. These are explicit estimates, never failed-probe values.
DEFAULT_PEAK_BYTES = 8 * GIB
DEFAULT_DISK_BYTES = 16 * GIB
# Control-plane hang guard, matching gate_run's hook-probe guard.
CONTROL_TIMEOUT_SECONDS = 60
CGROUP_ROOT = Path('/sys/fs/cgroup')  # Linux cgroup v2 hierarchical memory.stat.
ACTIVE_STATES = {'active', 'activating', 'deactivating', 'reloading'}


def decide(resources, expected, running):
    reservation = sum(max(0, r['expected_peak'] - r['rss']) for r in running)
    remaining = resources['mem_available'] - reservation
    memory_needed = expected['peak_bytes'] + MEMORY_HEADROOM_BYTES
    disk_needed = expected['disk_bytes'] + DISK_HEADROOM_BYTES
    reason = (f"memory available={resources['mem_available']} reserved={reservation} needed={memory_needed}; "
              f"load={resources['load1']} limit={resources['nproc']/LOAD_CPU_DIVISOR}; "
              f"disk free={resources['disk_free']} needed={disk_needed}; {expected['source']}")
    allowed = (remaining >= memory_needed and resources['load1'] < resources['nproc']/LOAD_CPU_DIVISOR
               and resources['disk_free'] >= disk_needed)
    return allowed, reason


def expected_from_history(rows):
    latest = sorted(rows, key=lambda r: r['finished_utc'], reverse=True)
    peak, disk = None, None
    for row in latest:
        value = row.get('peak_rss_kib')
        if value is None and 'checks' in row:
            # Records measure largest-process peaks; cgroup event peaks are preferable.
            samples = [c.get('peak_rss_kib') for c in row['checks'] + row.get('reports', [])]
            value = max((v for v in samples if isinstance(v, (int, float))), default=None)
        if peak is None and isinstance(value, (int, float)) and value > 0:
            peak = int(value * 1024)
        value = row.get('disk_bytes')
        if disk is None and isinstance(value, (int, float)) and value >= 0:
            disk = int(value)
        if peak is not None and disk is not None:
            break
    missing = []
    if peak is None:
        peak = DEFAULT_PEAK_BYTES
        missing.append(f'peak={peak}')
    if disk is None:
        disk = DEFAULT_DISK_BYTES
        missing.append(f'disk={disk}')
    source = 'latest measured same-tier history'
    if missing:
        source += '; conservative no-history defaults ' + ', '.join(missing)
    return {'peak_bytes': peak, 'disk_bytes': disk, 'source': source}


def state_dir(workspace):
    return Path(workspace) / 'bennett/.tmp/gates'


def read_json(path):
    try:
        value = json.loads(path.read_text())
    except (OSError, ValueError) as error:
        raise ValueError(f'{path}: {error}') from error
    if not isinstance(value, dict):
        raise ValueError(f'{path}: expected JSON object')
    return value


def history(repo, workspace, tier):
    # Same owning repo across linked worktrees; records remain local, events central.
    rows = []
    common = subprocess.run(['git', '-C', str(repo), 'rev-parse', '--path-format=absolute', '--git-common-dir'],
                            check=True, capture_output=True, text=True, timeout=CONTROL_TIMEOUT_SECONDS).stdout.strip()
    owner = Path(common).parent
    paths = set((Path(repo) / '.tmp/gate/records').glob('*.json')) | set((owner / '.tmp/gate/records').glob('*.json'))
    paths |= set((state_dir(workspace) / 'events').glob('*.json'))
    for path in paths:
        row = read_json(path)
        if row.get('tier', 'pre-merge') != tier or 'finished_utc' not in row:
            continue
        if path.parent.name == 'events' and row.get('repo_name') != owner.name:
            continue
        rows.append(row)
    return rows


def unit_properties(unit):
    z = subprocess.run(['systemctl', '--user', 'show', unit,
                        '--property=ActiveState,MemoryCurrent,MemoryPeak,ControlGroup'],
                       capture_output=True, text=True, timeout=CONTROL_TIMEOUT_SECONDS)
    if z.returncode:
        raise RuntimeError(f'systemctl show {unit}: {z.stderr.strip()}')
    return dict(line.split('=', 1) for line in z.stdout.splitlines() if '=' in line)


def current_rss(properties):
    if properties['ActiveState'] == 'activating' and not properties.get('ControlGroup'):
        return 0  # No process exists yet: reserve the entire expected peak.
    cgroup = properties['ControlGroup']
    if not cgroup.startswith('/') or '..' in cgroup.split('/'):
        raise ValueError(f'invalid service cgroup {cgroup!r}')
    stats = dict(line.split() for line in (CGROUP_ROOT / cgroup.lstrip('/') / 'memory.stat').read_text().splitlines())
    # Anonymous + shared memory is a conservative RSS estimate: excludes reclaimable
    # file cache. MemoryCurrent includes cache, which would under-reserve headroom.
    return int(stats['anon']) + int(stats['shmem'])


def running_reservations(workspace):
    result = []
    base = state_dir(workspace)
    for path in (base / 'admissions').glob('*.json'):
        if path.name.endswith('.outcome.json') or (base / 'events' / path.name).exists():
            continue
        request = read_json(path)
        props = unit_properties(path.stem)
        if props['ActiveState'] in ACTIVE_STATES:
            result.append({'expected_peak': request['expected_peak'], 'rss': current_rss(props)})
    return result


def resources(repo):
    mem = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
    return {'mem_available': int(mem['MemAvailable'].split()[0]) * 1024,
            'nproc': len(os.sched_getaffinity(0)), 'load1': os.getloadavg()[0],
            'disk_free': shutil.disk_usage(repo).free}


def assess(repo, workspace, tier):
    try:
        expected = expected_from_history(history(repo, workspace, tier))
        allowed, reason = decide(resources(repo), expected, running_reservations(workspace))
        return allowed, reason, expected
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError, RuntimeError) as error:
        return False, f'admission probe unavailable: {type(error).__name__}: {error}', {}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='command', required=True)
    gate = sub.add_parser('gate')
    gate.add_argument('--repo', required=True, type=Path)
    gate.add_argument('--tier', choices=('pre-merge', 'full'), default='pre-merge')
    args = ap.parse_args()
    try:
        common = subprocess.run(['git', '-C', str(args.repo), 'rev-parse', '--path-format=absolute', '--git-common-dir'],
                                check=True, capture_output=True, text=True, timeout=CONTROL_TIMEOUT_SECONDS).stdout.strip()
        workspace = Path(os.environ.get('BENNETT_GATE_WORKSPACE', str(Path(common).parent.parent)))
        ok, reason, _ = assess(args.repo.resolve(), workspace, args.tier)
    except (OSError, subprocess.SubprocessError) as error:
        ok, reason = False, f'admission probe unavailable: {error}'
    print(('ADMIT ' if ok else 'WAIT ') + reason)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
