#!/usr/bin/env python3
"""Background full tier: when a repo's origin/main has moved since its last started full run, start one.

`regate.py run` (one tick): fetch each manifest repo that has a gate.toml, and for each whose origin/main differs from the
last sha this tool started and which has no gate unit running, start `gate_launch --tier full --fresh` on that sha. Admission
is gate_launch's (admit.py); a WAIT is skipped and retried next tick. Reds land in bennett/.tmp/gates/reds.log as for any
gate, and every push to that repo then shows them. The per-command timeout is each gate.toml's timeout_s.
`regate.py install` writes and enables a user timer (every 10 minutes, survives reboots via linger).
State: bennett/.tmp/gates/regate.json. Log: bennett/.tmp/gates/regate.log (one line per decision).
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import tomllib

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_launch  # noqa: E402

META = Path(__file__).resolve().parents[1]
WORKSPACE = META.parent
STATE = META / '.tmp/gates/regate.json'
LOG = META / '.tmp/gates/regate.log'
TICK_MINUTES = 10
GIT_TIMEOUT_SECONDS = 120  # control-plane guard for fetch/rev-parse


def repos():
    manifest = tomllib.loads((META / 'manifest.toml').read_text())['repos']
    return [name for name, row in manifest.items() if (WORKSPACE / row['path'] / 'gate.toml').is_file()]


def plan(heads, state, running):
    """Repos whose origin/main moved since the last started full run and that have no gate unit running."""
    return [(repo, sha) for repo, sha in sorted(heads.items())
            if sha != state.get(repo, {}).get('sha') and repo not in running]


def running_repos():
    units = subprocess.run(['systemctl', '--user', 'list-units', 'bennett-gate-*', '--no-legend', '--plain'],
                           capture_output=True, text=True, timeout=GIT_TIMEOUT_SECONDS).stdout.split()
    return {u for u in units if u.startswith('bennett-gate-')}


def log(line):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open('a') as out:
        out.write(time.strftime('%Y-%m-%dT%H:%M:%SZ ', time.gmtime()) + line + '\n')


def tick():
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    heads = {}
    for repo in repos():
        checkout = WORKSPACE / repo
        fetched = subprocess.run(['git', '-C', str(checkout), 'fetch', '-q', 'origin',
                                  '+refs/heads/main:refs/remotes/origin/main'],
                                 capture_output=True, text=True, timeout=GIT_TIMEOUT_SECONDS)
        if fetched.returncode:
            log(f'{repo} fetch failed: {fetched.stderr.strip()[:200]}')
            continue
        heads[repo] = subprocess.run(['git', '-C', str(checkout), 'rev-parse', 'origin/main'], check=True,
                                     capture_output=True, text=True, timeout=GIT_TIMEOUT_SECONDS).stdout.strip()
    units = running_repos()
    busy = {repo for repo in heads if any(u.startswith(f'bennett-gate-{repo}-') for u in units)}
    for repo, sha in plan(heads, state, busy):
        try:
            unit = gate_launch.start(WORKSPACE / repo, sha, 'full', workspace=WORKSPACE, fresh=True)
        except gate_launch.LaunchError as error:
            log(f'{repo} {sha[:12]} not started: {error}')
            continue
        state[repo] = {'sha': sha, 'unit': unit, 'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(state, indent=1) + '\n')
        log(f'{repo} {sha[:12]} started {unit}')
    log(f'tick: {len(heads)} repos, busy {sorted(busy)}')


def install():
    units = Path.home() / '.config/systemd/user'
    units.mkdir(parents=True, exist_ok=True)
    env = ' '.join(f'"{k}={os.environ[k]}"' for k in ('PATH', 'HOME') if k in os.environ)
    (units / 'bennett-regate.service').write_text(
        '[Unit]\nDescription=Bennett background full tier (bennett/tools/regate.py)\n\n'
        f'[Service]\nType=oneshot\nEnvironment={env}\nExecStart={sys.executable} -I {Path(__file__).resolve()} run\n')
    (units / 'bennett-regate.timer').write_text(
        '[Unit]\nDescription=Bennett background full tier every 10 minutes\n\n'
        f'[Timer]\nOnBootSec=5min\nOnUnitActiveSec={TICK_MINUTES}min\nPersistent=true\n\n[Install]\nWantedBy=timers.target\n')
    for argv in (['daemon-reload'], ['enable', '--now', 'bennett-regate.timer']):
        subprocess.run(['systemctl', '--user', *argv], check=True, timeout=GIT_TIMEOUT_SECONDS)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('command', choices=('run', 'install'))
    args = ap.parse_args()
    tick() if args.command == 'run' else install()
    return 0


if __name__ == '__main__':
    sys.exit(main())
