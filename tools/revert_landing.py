#!/usr/bin/env python3
"""Revert one first-parent main merge and push (maintainer: "fast pushes go immediately and revert if the fast tier fails").
The push hook starts the fast tier behind the revert like any other push."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import tomllib

# Control-plane guard, matching gate_launch/admit. Gates use their own configured guards.
CONTROL_TIMEOUT_SECONDS = 60


class RevertError(Exception):
    pass


def environment():
    return {k: v for k, v in os.environ.items()
            if k not in {'GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'DISPLAY', 'WAYLAND_DISPLAY',
                         'DBUS_SESSION_BUS_ADDRESS', 'BROWSER'} and not k.startswith('BENNETT_GATE_')}


def git(repo, *args, allowed=(0,)):
    result = subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-C', str(repo), *args],
                            env=environment(), stdin=subprocess.DEVNULL, capture_output=True,
                            text=True, timeout=CONTROL_TIMEOUT_SECONDS)
    if result.returncode not in allowed:
        raise RevertError(f'git {args[0]}: exit {result.returncode}: {result.stderr.strip()}')
    return result.stdout.strip()


def pinned_consumers(repo, merge, workspace):
    """Read committed consumer main configs, never dirty/untracked pin edits."""
    consumers = []
    for consumer in sorted(Path(workspace).iterdir()):
        if consumer.resolve() == repo or not (consumer / '.git').exists():
            continue
        # Only owning main checkouts, not linked worktrees/implementation branches.
        if git(consumer, 'branch', '--show-current') != 'main':
            continue
        exists = git(consumer, 'ls-tree', '--name-only', 'HEAD', 'gate.toml')
        if not exists:
            continue
        cfg = tomllib.loads(git(consumer, 'show', 'HEAD:gate.toml'))
        for sibling, entry in cfg.get('siblings', {}).items():
            if sibling != repo.name:
                continue
            pin = entry['sha']
            if not isinstance(pin, str) or len(pin) != 40 or any(c not in '0123456789abcdef' for c in pin):
                raise RevertError(f'{consumer.name}: invalid pin for {repo.name}')
            result = subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-C', str(repo),
                                     'merge-base', '--is-ancestor', merge, pin], env=environment(),
                                    stdin=subprocess.DEVNULL, capture_output=True, text=True,
                                    timeout=CONTROL_TIMEOUT_SECONDS)
            if result.returncode not in (0, 1):
                raise RevertError(f'{consumer.name}: cannot resolve pinned {repo.name} commit {pin}: {result.stderr.strip()}')
            if result.returncode == 0:
                consumers.append(dict(repo=consumer.name, pin=pin))
    return consumers


def revert(repo, merge, workspace=None):
    repo = Path(repo).resolve()
    workspace = Path(workspace).resolve() if workspace else repo.parent
    if git(repo, 'rev-parse', '--show-toplevel') != str(repo):
        raise RevertError('--repo must name the checkout root')
    if git(repo, 'branch', '--show-current') != 'main':
        raise RevertError('revert requires a main checkout')
    if git(repo, 'status', '--porcelain'):
        raise RevertError('revert requires a clean main checkout, including untracked files')
    git(repo, 'fetch', '--no-tags', 'origin', '+refs/heads/main:refs/remotes/origin/main')
    head = git(repo, 'rev-parse', 'HEAD')
    if head != git(repo, 'rev-parse', 'origin/main'):
        raise RevertError('local main must equal origin/main; update it before reverting')
    merge = git(repo, 'rev-parse', '--verify', merge + '^{commit}')
    if merge not in git(repo, 'rev-list', '--first-parent', head).splitlines():
        raise RevertError('target is not on main first-parent chain')
    if len(git(repo, 'show', '-s', '--format=%P', merge).split()) < 2:
        raise RevertError('target must be a merge commit')
    consumers = pinned_consumers(repo, merge, workspace)
    for consumer in consumers:
        print(f'consumer {consumer["repo"]} pins {consumer["pin"]} containing merge {merge}', flush=True)
    print('Consumer pins name immutable commits that still exist after the revert.\n'
          'Consumers keep building and gating against those commits until their pins are bumped.\n'
          'A revert leaves consumers on the old content; it does not invalidate their pins.', flush=True)
    git(repo, 'revert', '--no-edit', '-m', '1', merge)
    sha = git(repo, 'rev-parse', 'HEAD')
    # Ordinary non-force push rejects a concurrent landing. Never rewrite main.
    git(repo, 'push', 'origin', 'HEAD:refs/heads/main')
    return dict(sha=sha, merge=merge, consumers=consumers)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('--merge', required=True)
    parser.add_argument('--workspace', type=Path)
    args = parser.parse_args(argv)
    try:
        outcome = revert(args.repo, args.merge, args.workspace)
        print('pushed revert ' + outcome['sha'])
        return 0
    except (RevertError, OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(f'revert-landing: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
