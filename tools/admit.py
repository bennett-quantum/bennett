#!/usr/bin/env python3
"""Resource and weekly-pace admission. Probes fail closed with a reason."""
import argparse
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import fcntl
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import tomllib

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
VENDORS = ('codex', 'claude', 'muse')
KINDS = ('implementer', 'review', 'gate', 'council')
# Product allowance: one quota invocation per five minutes, including failures.
QUOTA_CACHE_SECONDS = 5 * 60
QUOTA_CLI = Path.home() / '.claude/skills/quota/scripts/quota.sh'
META_ROOT = Path(__file__).resolve().parents[1]


def validate_dial(dial):
    if set(dial) != set(VENDORS):
        raise ValueError(f'dial requires exactly {VENDORS}')
    result = {}
    for vendor, value in dial.items():
        if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
            raise ValueError(f'dial {vendor}: pace must be a finite nonnegative number')
        number = Decimal(str(value))
        if not number.is_finite() or number < 0:
            raise ValueError(f'dial {vendor}: pace must be a finite nonnegative number')
        result[vendor] = number
    return result


READING_KEYS = {'weekly_used', 'read_utc', 'resets_utc'}
WEEK = timedelta(days=7)


def read_dial(path):
    data = tomllib.loads(Path(path).read_text(), parse_float=Decimal)
    if any(not isinstance(row, dict) or 'pace' not in row or set(row) - {'pace'} not in (set(), READING_KEYS)
           for row in data.values()):
        raise ValueError('dial requires one pace number per vendor (plus, optionally, a full maintainer reading)')
    return validate_dial({vendor: row['pace'] for vendor, row in data.items()})


def read_readings(path):
    """Maintainer-supplied weekly readings for vendors the quota CLI cannot see, valid until their reset."""
    data = tomllib.loads(Path(path).read_text(), parse_float=Decimal)
    readings = {}
    for vendor, row in data.items():
        if READING_KEYS <= set(row):
            readings[vendor] = {'used': Decimal(str(row['weekly_used'])),
                                'read_utc': datetime.fromisoformat(row['read_utc']),
                                'resets_utc': datetime.fromisoformat(row['resets_utc'])}
    return readings


def reading_quota(reading, now):
    if now >= reading['resets_utc']:
        raise ValueError(f"reading expired at its reset {reading['resets_utc'].isoformat()}, ask the maintainer")
    elapsed = now - (reading['resets_utc'] - WEEK)
    uniform = max(Decimal(0), min(Decimal(100), Decimal(str(elapsed / WEEK)) * 100))
    return reading['used'], uniform


def weekly_quota(output, vendor):
    rows = [re.split(r'\s{2,}', line.strip()) for line in output.splitlines()]
    rows = [row for row in rows if row[0].lower() == vendor]
    weekly = [row for row in rows if len(row) > 1 and row[1].lower() == 'weekly']
    if len(weekly) != 1:
        errors = [row[-1] for row in rows if 'error:' in row[-1]]
        raise ValueError('; '.join(errors) or 'expected exactly one aggregate Weekly row')
    row = weekly[0]
    if len(row) != 9 or row[8] != 'ok':
        raise ValueError(f'unreadable or inactive Weekly row: {row}')
    used = re.fullmatch(r'(\d+(?:\.\d+)?)%', row[2])
    pace = re.fullmatch(r'\+?(\d+(?:\.\d+)?)% (ahead|behind)', row[4])
    if not used or (not pace and row[4] != 'on pace'):
        raise ValueError(f'unreadable Weekly USED/PACE: {row[2]} / {row[4]}')
    used = Decimal(used[1])
    delta = (Decimal(pace[1]) * (1 if pace[2] == 'ahead' else -1)) if pace else Decimal(0)
    uniform = used - delta
    if not 0 <= used <= 100 or not 0 <= uniform <= 100:
        raise ValueError('Weekly USED or inferred uniform line outside 0..100%')
    return used, uniform


def decide_launch(resources, expected, running, quota, dial, vendor, kind, readings=None, now=None):
    """Pure launch policy: all kinds spend quota; only the requested vendor blocks."""
    resource_ok, resource_reason = decide(resources, expected, running)
    try:
        dial = validate_dial(dial)
        if vendor not in VENDORS or kind not in KINDS:
            raise ValueError(f'invalid vendor/kind: {vendor}/{kind}')
    except (ValueError, TypeError) as error:
        return False, f'dial unavailable: {error}; {resource_reason}'
    summaries, permitted = [], {}
    for name in VENDORS:
        source = ''
        try:
            try:
                used, uniform = weekly_quota(quota, name)
            except ValueError as missing:
                if name not in (readings or {}):
                    raise
                try:
                    used, uniform = reading_quota(readings[name], now)
                except ValueError as expired:
                    raise ValueError(f'{name.capitalize()} {expired} (quota CLI: {missing})') from None
                source = f" (maintainer reading {readings[name]['read_utc'].isoformat()})"
            line = min(Decimal(100), uniform * dial[name])
            gap = line - used
            position = 'below' if gap > 0 else 'above' if gap < 0 else 'at'
            summaries.append(f'{name} {abs(gap):.1f}pp {position} line={line:.1f}% '
                             f'used={used:.1f}% pace={dial[name]}{source}')
            permitted[name] = gap > 0
        except (ValueError, TypeError) as error:
            summaries.append(f'{name} unavailable: {error}')
            permitted[name] = False
    return resource_ok and permitted[vendor], f'{vendor}/{kind}; ' + '; '.join(summaries) + '; ' + resource_reason


def quota_output(cache_dir, runner=None, clock=None):
    """Serialize and cache CLI successes AND failures across linked worktrees."""
    runner, clock = runner or subprocess.run, clock or time.time
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    with (cache_dir / 'quota.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        path = cache_dir / 'quota.json'
        cached = None
        if path.exists():
            cached = read_json(path)
            timestamp = cached['timestamp']
            if (not isinstance(timestamp, (int, float)) or isinstance(timestamp, bool)
                    or not math.isfinite(timestamp) or timestamp > clock()):
                raise ValueError('quota cache timestamp invalid or in the future')
            if not isinstance(cached['output'], str) or not isinstance(cached['error'], (str, type(None))):
                raise ValueError('quota cache output/error malformed')
            if clock() - timestamp >= QUOTA_CACHE_SECONDS:
                cached = None
        if cached is None:
            output, error = '', None
            try:
                probe = runner(['bash', str(QUOTA_CLI)], capture_output=True, text=True,
                               timeout=CONTROL_TIMEOUT_SECONDS)
                output = probe.stdout
                if probe.returncode:
                    error = f'quota CLI exit {probe.returncode}: {probe.stderr.strip() or output.strip()}'
            except (OSError, subprocess.SubprocessError) as failure:
                error = f'quota probe unavailable: {type(failure).__name__}: {failure}'
            cached = {'timestamp': clock(), 'output': output, 'error': error}
            pending = cache_dir / 'quota.pending'
            pending.write_text(json.dumps(cached) + '\n')
            pending.replace(path)
        if cached['error'] is not None:
            raise RuntimeError(cached['error'])
        return cached['output']


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
    launch = sub.add_parser('launch')
    launch.add_argument('--vendor', required=True, choices=VENDORS)
    launch.add_argument('--kind', required=True, choices=KINDS)
    launch.set_defaults(repo=META_ROOT, tier='pre-merge')
    args = ap.parse_args()
    try:
        common = subprocess.run(['git', '-C', str(args.repo), 'rev-parse', '--path-format=absolute', '--git-common-dir'],
                                check=True, capture_output=True, text=True, timeout=CONTROL_TIMEOUT_SECONDS).stdout.strip()
        workspace = Path(os.environ.get('BENNETT_GATE_WORKSPACE', str(Path(common).parent.parent)))
        if args.command == 'gate':
            ok, reason, _ = assess(args.repo.resolve(), workspace, args.tier)
        else:
            quota = quota_output(Path(common).parent / '.tmp/admit')
            dial = read_dial(META_ROOT / 'dial.toml')
            readings = read_readings(META_ROOT / 'dial.toml')
            expected = expected_from_history(history(args.repo, workspace, args.tier))
            ok, reason = decide_launch(resources(args.repo), expected, running_reservations(workspace),
                                       quota, dial, args.vendor, args.kind, readings=readings,
                                       now=datetime.now(timezone.utc))
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError, RuntimeError) as error:
        ok, reason = False, f'admission probe unavailable: {error}'
    print(('ADMIT ' if ok else 'WAIT ') + reason)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
