"""Health machinery uses scratch Git repositories and injected launchers only."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'main_health.py'


def load_tool():
    spec = importlib.util.spec_from_file_location('main_health', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HealthTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / 'fixture'
        self.repo.mkdir()
        self.meta = self.root / 'bennett'
        self.meta.mkdir()
        self.state = self.root / 'state'
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_AUTHOR_NAME='Fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                        GIT_COMMITTER_NAME='Fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
        self.patcher = patch.dict(os.environ, self.env, clear=True)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.git('init', '-qb', 'main')
        (self.repo / 'tests').mkdir()
        (self.repo / 'tests/timeouts.toml').write_text('machine="fixture"\nmachine_config_factor=1\n'
            '[classes.short]\nseconds=100\nmeasurements=[{machine="fixture",date="2026-11-11",command="git",wall_seconds=1}]\n'
            '[classes.eternal]\nseconds=1000\nmeasurements=[{machine="fixture",date="2026-11-11",command="gate",wall_seconds=1}]\n')
        (self.repo / 'value').write_text('green')
        (self.repo / 'gate.toml').write_text('schema = 1\n[[check]]\nname="tests"\nargv=["true"]\n')
        (self.repo / 'scripts').mkdir()
        (self.repo / 'scripts/pre-push').write_text('#!/bin/sh\nexit 0\n')
        self.commit('green')
        self.green = self.git('rev-parse', 'HEAD')
        self.git('clone', '-q', '--bare', str(self.repo), str(self.root / 'remote.git'))
        self.git('remote', 'add', 'origin', str(self.root / 'remote.git'))
        (self.meta / 'manifest.toml').write_text('[repos.fixture]\npath="fixture"\n')
        (self.meta / 'health').mkdir()
        (self.meta / 'health/known-reds.toml').write_text('schema = 1\n')
        self.h = load_tool()

    def git(self, *args):
        return subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-C', str(self.repo), *args],
                              capture_output=True, text=True, check=True, timeout=30).stdout.strip()

    def commit(self, title):
        self.git('add', 'value', 'gate.toml', 'scripts', 'tests')
        self.git('commit', '--allow-empty', '-qm', title)

    def merge(self, value, title):
        self.git('switch', '-qc', title)
        (self.repo / 'value').write_text(value)
        self.commit(title)
        self.git('switch', '-q', 'main')
        self.git('merge', '--no-ff', '-qm', 'Merge ' + title, title)
        return self.git('rev-parse', 'HEAD')

    def args(self, **kw):
        args = dict(meta=self.meta, state_dir=self.state, repos='fixture', ladder=None,
                    force=False, baseline=None, tier='full', fresh=True, command='run', bead=None)
        return argparse.Namespace(**(args | kw))

    def launcher(self, checkout, sha, argv, log, env, record_path):
        self.assertEqual(self.h.git(checkout, 'rev-parse', 'HEAD'), sha)
        self.assertEqual(argv[-3:], ['--tier', 'full', '--fresh'])
        value = self.h.git(checkout, 'show', sha + ':value')
        code = int(value == 'red')
        log.write_text('injected gate\n')
        self.h.atomic_json(record_path, dict(sha=sha, tier='full', fresh=True, checks=[dict(name='tests', exit=code)],
                                             result='fail' if code else 'pass'))
        return dict(exit=code, record_path=str(record_path), result='fail' if code else 'pass')

    def runner(self, **kw):
        return self.h.Runner(self.args(**kw), launcher=self.launcher)

    def test_classification_does_not_hide_new_check_behind_known_red(self):
        baseline = {('fixture', 'old'): dict(sha=self.green, bead='b-old')}
        items = {'old': {'exit': 1}, 'new': {'exit': 1}, 'ok': {'exit': 0}}
        result = self.h.classify('fixture', items, baseline)
        self.assertEqual({k: v['classification'] for k, v in result.items()},
                         {'old': 'KNOWN-RED', 'new': 'NEW-RED', 'ok': 'PASS'})
        items['old']['exit'] = 0
        self.assertEqual(self.h.classify('fixture', items, baseline)['old']['classification'], 'FIXED')
        self.assertIn(('fixture', 'old'), baseline)

    def test_baseline_validation_and_seed_preserve_fixed_entries(self):
        runner = self.runner()
        self.assertEqual(runner.cycle(), 0)
        self.merge('red', 'bad')
        self.git('push', '-q', 'origin', 'main')
        self.assertEqual(runner.cycle(), 1)
        runner.seed('b-health')
        baseline = self.h.load_baseline(runner.baseline_path)
        self.assertEqual(baseline[('fixture', 'tests')]['bead'], 'b-health')
        self.assertEqual(baseline[('fixture', 'tests')]['sha'], self.git('rev-parse', 'HEAD'))
        self.merge('green', 'fix')
        self.git('push', '-q', 'origin', 'main')
        self.assertEqual(runner.cycle(), 0)
        runner.seed('b-health')
        self.assertEqual(len(self.h.load_baseline(runner.baseline_path)), 1)
        (runner.baseline_path).write_text('schema=1\n[[red]]\nscope="fixture"\ncheck="tests"\nsha="bad"\n')
        with self.assertRaises(self.h.HealthError):
            self.h.load_baseline(runner.baseline_path)

    def test_cycle_event_single_merge_attribution_and_no_unchanged_cycle(self):
        runner = self.runner()
        self.assertEqual(runner.cycle(), 0)
        merge = self.merge('red', 'bad')
        self.git('push', '-q', 'origin', 'main')
        self.assertEqual(runner.cycle(), 1)
        row = json.loads((self.state / 'status.json').read_text())['rows']['fixture']
        self.assertEqual(row['classification'], 'NEW-RED')
        self.assertEqual(row['checks']['tests']['culprit_merge'], merge)
        self.assertEqual(row['last_green']['tests'], {'fixture': self.green})
        events = list((self.meta / '.tmp/gates/events').glob('main-health-*.json'))
        self.assertEqual(len(events), 2)
        event = json.loads(sorted(events)[-1].read_text())
        self.assertEqual(event['rows']['fixture']['new_reds'][0]['culprit_merge'], merge)
        self.assertIsNone(runner.cycle())
        self.assertEqual(len(list(events[0].parent.glob('main-health-*.json'))), 2)

    def test_merge_bisect_uses_first_parent_and_names_culprit(self):
        runner = self.runner()
        self.assertEqual(runner.cycle(), 0)
        self.merge('green2', 'good1')
        culprit = self.merge('red', 'bad')
        self.merge('red', 'stillbad')
        self.git('push', '-q', 'origin', 'main')
        self.assertEqual(runner.cycle(), 1)
        row = json.loads((self.state / 'status.json').read_text())['rows']['fixture']
        item = row['checks']['tests']
        self.assertEqual(item['culprit_merge'], culprit)
        self.assertEqual(len(item['attribution']['merges']['fixture']), 3)
        self.assertGreater(item['attribution']['gate_runs'], 0)
        self.assertIn('per-check', item['attribution']['cost'])

    def test_checks_keep_independent_last_green_and_missing_is_not_fixed(self):
        runner = self.runner()
        self.assertEqual(runner.cycle(), 0)
        previous = json.loads((self.state / 'status.json').read_text())['rows']['fixture']
        previous['last_green']['other'] = {'fixture': 'a' * 40}
        runner.baseline = {('fixture', 'missing'): dict(sha=self.green, bead='b-missing')}
        row = runner.check('fixture', {'fixture': self.green}, previous)
        self.assertEqual(row['checks']['missing']['classification'], 'UNKNOWN')
        self.assertEqual(row['last_green']['other'], {'fixture': 'a' * 40})

    def test_ladder_case_and_stage_names_are_distinct(self):
        report = dict(stages={'C/18': {'build': {'status': 'PASS'}}}, cases={
            'C/18': {'gcd': {'native': {'status': 'FAIL', 'beads': ['bp-1']}},
                     'add': {'native': {'status': 'PASS'}}}})
        items = self.h.ladder_items(report)
        self.assertEqual(items['case/C/18/gcd/native']['exit'], 1)
        self.assertEqual(items['case/C/18/gcd/native']['beads'], ['bp-1'])
        self.assertIn('stage/C/18/build', items)
        with self.assertRaises(self.h.HealthError):
            self.h.ladder_items({'cases': {'x': {'status': 'surprise'}}})

    def test_repos_launch_concurrently_and_info_only_is_excluded(self):
        (self.meta / 'manifest.toml').write_text('[repos.fixture]\npath="fixture"\n'
            '[repos.second]\npath="fixture"\n[repos.info]\npath="absent"\ninfo_only=true\n')
        runner = self.runner(repos=None, ladder='')
        barrier = threading.Barrier(2, timeout=10)
        def launch(*args):
            barrier.wait()
            return self.launcher(*args)
        runner.launcher = launch
        self.assertEqual(runner.cycle(), 0)

    def test_errors_emit_events_and_cannot_seed(self):
        runner = self.runner()
        runner.launcher = lambda *args: (_ for _ in ()).throw(self.h.HealthError('WAIT resource admission'))
        self.assertEqual(runner.cycle(), 2)
        events = list((self.meta / '.tmp/gates/events').glob('main-health-*.json'))
        self.assertEqual(json.loads(events[0].read_text())['rows']['fixture']['classification'], 'ERROR')
        with self.assertRaises(self.h.HealthError):
            runner.seed('b-health')

    def test_class_guards_require_cited_measurements(self):
        (self.repo / 'tests/timeouts.toml').unlink()
        with self.assertRaisesRegex(self.h.HealthError, 'hang-guard'):
            self.h.guard_seconds(self.repo, 'short')
        p = self.repo / 'tests/timeouts.toml'
        p.parent.mkdir(exist_ok=True)
        p.write_text('machine="test"\nmachine_config_factor=1\n[classes.short]\nseconds=100\n'
                     'measurements=[{machine="test",date="2026-11-11",command="git",wall_seconds=1}]\n')
        self.assertEqual(self.h.guard_seconds(self.repo, 'short'), 100)

    def test_launcher_uses_admission_and_completion_for_fresh_worker(self):
        launch = self.h.launcher_modules()
        sha = self.green
        checkout = self.h.detached(self.repo, sha, self.state, 'fixture')
        log = self.state / 'worker.log'
        record = checkout / '.tmp/gate/records' / (sha + '.json')
        program = ('import json,pathlib,sys; p=pathlib.Path(sys.argv[1]); p.parent.mkdir(parents=True,exist_ok=True); '
                   'p.write_text(json.dumps({"sha":sys.argv[2],"tier":"full","fresh":True,'
                   '"checks":[{"name":"tests","exit":0}],"result":"pass"}))')
        argv = [os.sys.executable, '-c', program, str(record), sha]
        run = subprocess.run
        commands = []
        def service(command, **kwargs):
            if command[0] != 'systemd-run':
                return run(command, **kwargs)
            commands.append(command)
            self.assertNotIn('--scope', command)
            self.assertNotIn('bennett-heavy', ' '.join(command))
            index = command.index('worker')
            self.assertEqual(Path(command[index - 1]).name, 'main_health.py')
            request = Path(command[index + 2])
            self.assertEqual(self.h.worker(request), 0)
            launch.complete(request, query=lambda _: {})
            return subprocess.CompletedProcess(command, 0, '', '')
        with patch.object(launch.admit, 'assess', return_value=(True, 'fixture admitted', dict(peak_bytes=1, disk_bytes=1))), \
                patch.object(self.h.subprocess, 'run', side_effect=service):
            event = self.h.launch_gate(checkout, sha, argv, log,
                self.h.environment(self.state / 'tmp', self.root), record)
        self.assertEqual(event['exit'], 0)
        self.assertEqual(len(commands), 1)
        self.assertTrue(json.loads(record.read_text())['fresh'])

    def test_worker_guard_writes_unknown_outcome(self):
        log = self.state / 'timeout.log'
        request = self.root / 'request.json'
        self.h.atomic_json(request, dict(repo=str(self.repo), health_log=str(log), health_env=self.h.environment(),
            health_timeout=100, health_grace=100, health_argv=['true'], record_path=str(self.root / 'absent.json')))
        with patch.object(self.h.subprocess, 'run', return_value=subprocess.CompletedProcess([], 124)):
            self.assertEqual(self.h.worker(request), 124)
        self.assertEqual(json.loads(request.with_name('request.outcome.json').read_text())['exit'], 124)

    def test_ladder_frozen_vector_cases_and_known_red_seed(self):
        ladder = self.repo / 'ladder/rung-1/gate.sh'
        ladder.parent.mkdir(parents=True)
        flags = ' '.join('--' + n.removeprefix('bennett-') + '-rev' for n in self.h.LADDER_REPOS)
        ladder.write_text('#!/bin/sh\nif [ "$1" = --help ]; then echo "' + flags + '"; fi\n')
        self.git('add', 'ladder')
        self.commit('ladder')
        self.git('push', '-q', 'origin', 'main')
        (self.meta / 'manifest.toml').write_text(''.join(f'[repos."{n}"]\npath="fixture"\n'
            for n in ('bennett-conformance', *self.h.LADDER_REPOS)))
        runner = self.runner(repos=None, ladder='rung-1', command='seed')
        def ladder_launch(checkout, sha, argv, log, env, record):
            self.assertEqual(len(set(argv[argv.index('--plugin-rev') + 1::2])), 1)
            output = Path(argv[argv.index('--output') + 1])
            output.mkdir(parents=True)
            self.h.atomic_json(output / 'report.json', dict(cases={'C/18': {'gcd': {
                'native': dict(status='FAIL', beads=['bp-case'])}}}))
            (output / 'table.md').write_text('| Case | Result |\n| gcd | FAIL |\n')
            return dict(exit=1)
        runner.launcher = ladder_launch
        self.assertEqual(runner.cycle(), 1)
        runner.seed(None)
        entry = self.h.load_baseline(runner.baseline_path)[('ladder/rung-1', 'case/C/18/gcd/native')]
        self.assertEqual(entry['bead'], 'bp-case')
        self.assertEqual(len(entry['shas']), 6)

    def test_direct_commit_after_merge_is_not_falsely_attributed(self):
        runner = self.runner()
        self.assertEqual(runner.cycle(), 0)
        self.merge('green2', 'good')
        (self.repo / 'value').write_text('red')
        self.commit('direct regression')
        self.git('push', '-q', 'origin', 'main')
        self.assertEqual(runner.cycle(), 1)
        item = runner.rows['fixture']['checks']['tests']
        self.assertNotIn('culprit_merge', item)
        self.assertIn('unavailable', item['attribution'])

    def test_seed_reclassifies_existing_state_without_another_main_move(self):
        runner = self.runner(command='seed')
        self.merge('red', 'bad')
        self.git('push', '-q', 'origin', 'main')
        self.assertEqual(runner.cycle(), 1)
        runner.seed('b-health')
        next_runner = self.runner()
        self.assertIsNone(next_runner.cycle())
        self.assertEqual(next_runner.exit_code(), 0)
        self.assertEqual(next_runner.rows['fixture']['classification'], 'KNOWN-RED')
