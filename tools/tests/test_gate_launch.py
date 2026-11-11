"""Detached service lifecycle with injected launch; no real units are started."""
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
from unittest.mock import patch
from fixtures import RunnerFixture


def module():
    path = Path(__file__).resolve().parents[1] / 'gate_launch.py'
    spec = importlib.util.spec_from_file_location('launch_test', path)
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    return tool


class LaunchTests(RunnerFixture):
    def setUp(self):
        super().setUp()
        self.sha = self.git('rev-parse', 'HEAD').strip()
        self.ws = self.root

    def test_start_detaches_service_with_completion_and_admission(self):
        a = module()
        calls = []
        def launch(argv, **kwargs):
            calls.append(argv)
            return subprocess.CompletedProcess(argv, 0, '', '')
        expected = {'peak_bytes': 100, 'disk_bytes': 200, 'source': 'fixture'}
        with patch.object(a.admit, 'assess', return_value=(True, 'fixture', expected)):
            unit = a.start(self.repo, self.sha, 'full', launcher=launch, workspace=self.ws)
        self.assertEqual(len(calls), 1)
        argv = calls[0]
        self.assertEqual(argv[:2], ['systemd-run', '--user'])
        self.assertNotIn('--scope', argv)
        self.assertIn('--property=Type=exec', argv)
        self.assertTrue(any('ExecStopPost=' in x and 'complete' in x for x in argv))
        self.assertIn(self.sha[:12], unit)
        self.assertIn('--setenv=PATH=' + os.environ['PATH'], argv)  # a --user service gets the manager's PATH, not the caller's
        self.assertIn('--setenv=HOME=' + os.environ['HOME'], argv)
        request = json.loads((self.ws / 'bennett/.tmp/gates/admissions' / (unit + '.json')).read_text())
        self.assertEqual(request['tier'], 'full')
        self.assertEqual(request['expected_peak'], 100)
        self.assertEqual(a.status(self.ws, query=lambda unit: {'ActiveState': 'active', 'MemoryCurrent': '1'})[0]['state'], 'running')

    def test_wait_admission_does_not_launch(self):
        a = module()
        with patch.object(a.admit, 'assess', return_value=(False, 'memory reservation', {})):
            with self.assertRaisesRegex(a.LaunchError, 'WAIT memory reservation'):
                a.start(self.repo, self.sha, 'full', launcher=lambda *a, **k: self.fail('launched'), workspace=self.ws)

    def request(self, a, tier='full'):
        unit = a.unit_name(self.repo, self.sha, tier)
        request = {'repo': str(self.repo), 'repo_name': 'repo', 'sha': self.sha, 'tier': tier,
                   'started_utc': '2026-01-01T00:00:00Z', 'record_path': str(self.repo / '.tmp/gate/records' / (self.sha + '.json'))}
        path = self.ws / 'bennett/.tmp/gates/admissions' / (unit + '.json')
        a.atomic_json(path, request)
        return unit, path

    def test_completion_pass_fail_setup_timeout_signal_and_crash(self):
        a = module()
        for exit_code, result in ((0, 'pass'), (1, 'fail'), (3, 'setup-error'), (124, 'hang-guard'),
                                  (143, 'signal'), (255, 'unit-crash')):
            with self.subTest(exit_code=exit_code):
                unit, path = self.request(a)
                outcome = path.with_name(unit + '.outcome.json')
                if exit_code != 255:
                    a.atomic_json(outcome, {'exit': exit_code, 'peak_rss_kib': 100, 'disk_bytes': 200})
                else:
                    outcome.unlink(missing_ok=True)
                event = a.complete(path, service_result='success' if exit_code == 0 else 'exit-code', exit_code='exited', exit_status=str(exit_code),
                                   query=lambda unit: {})
                self.assertEqual((event['exit'], event['result']), (exit_code, result))
                event_path = self.ws / 'bennett/.tmp/gates/events' / (unit + '.json')
                self.assertEqual(json.loads(event_path.read_text()), event)
                self.assertEqual(a.wait(unit, self.ws), exit_code)
                self.assertIn('finished_utc', event)
                event_path.unlink()

    def test_red_gate_writes_one_new_or_known_line(self):
        a = module()
        log = self.ws / 'bennett/.tmp/gates/reds.log'
        for known in (False, True):
            unit, path = self.request(a)
            request = json.loads(path.read_text())
            record = Path(request['record_path'])
            record.parent.mkdir(parents=True, exist_ok=True)
            record.write_text(json.dumps({'checks': [{'name': 'ok', 'exit': 0}, {'name': 'unit tests', 'exit': 1}]}))
            baseline = self.ws / 'bennett/health/known-reds.toml'
            baseline.parent.mkdir(parents=True, exist_ok=True)
            baseline.write_text('schema = 1\n' + (f'[[red]]\nscope = "{request["repo_name"]}"\ncheck = "unit tests"\n'
                                                   'bead = "b-1"\n' if known else ''))
            a.atomic_json(path.with_name(unit + '.outcome.json'), {'exit': 1})
            a.complete(path, service_result='exit-code', exit_code='exited', exit_status='1', query=lambda unit: {})
            line = log.read_text().splitlines()[-1]
            self.assertIn(('KNOWN' if known else 'NEW') + '-RED ' + request['repo_name'], line)
            self.assertTrue(line.endswith(' unit tests'), line)
            (self.ws / 'bennett/.tmp/gates/events' / (unit + '.json')).unlink()

    def test_open_reds_until_a_later_pass_and_shown_at_the_next_push(self):
        a = module()
        gates = self.ws / 'bennett/.tmp/gates'
        (gates / 'events').mkdir(parents=True, exist_ok=True)
        (gates / 'reds.log').write_text(
            '2026-11-11T10:00:00Z NEW-RED r1 aaaaaaaaaaaa pre-merge tests\n'
            '2026-11-11T10:00:00Z INFRA-RED r1 bbbbbbbbbbbb full setup-error\n'
            '2026-11-11T10:00:00Z NEW-RED r2 cccccccccccc pre-merge tests\n')
        a.atomic_json(gates / 'events/x.json', {'repo_name': 'r2', 'tier': 'full', 'result': 'pass',
                                                'finished_utc': '2026-11-11T10:05:00Z'})
        self.assertEqual([l.split()[2] for l in a.open_reds(self.ws)], ['r1'])
        self.assertEqual(a.open_reds(self.ws, 'r2'), [])
        name = Path(self.repo).name
        (gates / 'reds.log').write_text(f'2026-11-11T10:00:00Z NEW-RED {name} dddddddddddd pre-merge tests\n')
        expected = {'peak_bytes': 100, 'disk_bytes': 200, 'source': 'fixture'}
        with patch.object(a.admit, 'assess', return_value=(True, 'ok', expected)), \
                patch('sys.stderr', new_callable=__import__('io').StringIO) as err:
            a.start(self.repo, self.sha, 'pre-merge', launcher=lambda argv, **k: subprocess.CompletedProcess(argv, 0), workspace=self.ws)
        self.assertIn('OPEN NEW-RED', err.getvalue())
        self.assertIn('dddddddddddd', err.getvalue())

    def test_fresh_request_reaches_the_gate(self):
        a = module()
        calls = []
        expected = {'peak_bytes': 100, 'disk_bytes': 200, 'source': 'fixture'}
        with patch.object(a.admit, 'assess', return_value=(True, 'ok', expected)):
            unit = a.start(self.repo, self.sha, 'full', launcher=lambda argv, **k: subprocess.CompletedProcess(argv, 0),
                           workspace=self.ws, fresh=True)
        request = self.ws / 'bennett/.tmp/gates/admissions' / (unit + '.json')
        a.worker(request, runner=lambda argv, **k: calls.append(argv) or subprocess.CompletedProcess(argv, 0))
        self.assertIn('--fresh', calls[0])

    def test_stop_post_without_worker_outcome_maps_signal_and_timeout(self):
        a = module()
        for code, status, service, expected in [('killed', 'TERM', 'signal', 143),
                                               ('exited', '0', 'success', 255),
                                               ('killed', 'KILL', 'timeout', 124)]:
            unit, path = self.request(a)
            event = a.complete(path, service_result=service, exit_code=code, exit_status=status, query=lambda unit: {})
            self.assertEqual(event['exit'], expected)
            (self.ws / 'bennett/.tmp/gates/events' / (unit + '.json')).unlink()

    def test_worker_records_gate_exit_and_only_trusted_record_timeout(self):
        a = module()
        unit, path = self.request(a)
        def run(argv, **kwargs):
            self.assertIn('--tier', argv)
            self.assertIn('full', argv)
            return subprocess.CompletedProcess(argv, 3)
        self.assertEqual(a.worker(path, runner=run), 3)
        self.assertEqual(json.loads(path.with_name(unit + '.outcome.json').read_text())['exit'], 3)

    def test_interrupt_during_launch_still_publishes_setup_event(self):
        # Review r1 P2: an interrupt between admission and systemd-run left wait() polling forever.
        a = module()
        expected = {'peak_bytes': 100, 'disk_bytes': 200, 'source': 'fixture'}
        def interrupted(argv, **k):
            raise KeyboardInterrupt
        with patch.object(a.admit, 'assess', return_value=(True, 'ok', expected)):
            with self.assertRaises(KeyboardInterrupt):
                a.start(self.repo, self.sha, 'full', launcher=interrupted, workspace=self.ws)
        events = list((self.ws / 'bennett/.tmp/gates/events').glob('*.json'))
        self.assertEqual(len(events), 1)
        self.assertEqual(json.loads(events[0].read_text())['exit'], 3)

    def test_interrupt_right_after_admission_write_publishes_event(self):
        # Review r2 P2: the admission request was published outside the interrupt guard.
        a = module()
        expected = {'peak_bytes': 100, 'disk_bytes': 200, 'source': 'fixture'}
        real = a.atomic_json
        def write_then_interrupt(path, data):
            real(path, data)
            if path.parent.name == 'admissions' and not path.name.endswith('.outcome.json'):
                raise KeyboardInterrupt
        with patch.object(a.admit, 'assess', return_value=(True, 'ok', expected)), patch.object(a, 'atomic_json', write_then_interrupt):
            with self.assertRaises(KeyboardInterrupt):
                a.start(self.repo, self.sha, 'full', launcher=lambda argv, **k: subprocess.CompletedProcess(argv, 0), workspace=self.ws)
        events = list((self.ws / 'bennett/.tmp/gates/events').glob('*.json'))
        self.assertEqual(len(events), 1)
        self.assertEqual(json.loads(events[0].read_text())['exit'], 3)

    def test_launcher_failure_writes_setup_event(self):
        a = module()
        expected = {'peak_bytes': 100, 'disk_bytes': 200, 'source': 'fixture'}
        with patch.object(a.admit, 'assess', return_value=(True, 'ok', expected)):
            with self.assertRaisesRegex(a.LaunchError, 'systemd'):
                a.start(self.repo, self.sha, 'full', launcher=lambda argv, **k: subprocess.CompletedProcess(argv, 1, '', 'no bus'), workspace=self.ws)
        events = list((self.ws / 'bennett/.tmp/gates/events').glob('*.json'))
        self.assertEqual(len(events), 1)
        self.assertEqual(json.loads(events[0].read_text())['exit'], 3)

    def test_wrapper_crash_without_outcome_is_not_a_check_failure(self):
        a = module()
        unit, path = self.request(a)
        event = a.complete(path, service_result='exit-code', exit_code='exited', exit_status='1', query=lambda unit: {})
        self.assertEqual(event['result'], 'unit-crash')
        self.assertNotEqual(event['exit'], 0)

    def test_optional_worker_measurement_failure_preserves_gate_exit(self):
        a = module()
        unit, path = self.request(a)
        with patch.object(a.resource, 'getrusage', side_effect=OSError('unavailable accounting')):
            self.assertEqual(a.worker(path, runner=lambda *args, **kwargs: subprocess.CompletedProcess([], 0)), 0)
        outcome = json.loads(path.with_name(unit + '.outcome.json').read_text())
        self.assertIn('unavailable accounting', outcome['peak_rss_kib']['unavailable'])

    def test_stop_post_success_without_outcome_is_crash(self):
        a = module()
        unit, path = self.request(a)
        event = a.complete(path, service_result='success', exit_code='exited', exit_status='0', query=lambda unit: {})
        self.assertEqual(event['result'], 'unit-crash')

    def test_worker_promotes_current_command_hang_guard_to_124(self):
        a = module()
        unit, path = self.request(a)
        request = json.loads(path.read_text())
        def gate(argv, **kwargs):
            a.atomic_json(Path(request['record_path']), {'sha': self.sha, 'tier': 'full',
                'started_utc': '2026-01-01T00:00:01Z', 'checks': [{'exit': 124}], 'disk_bytes': 123456})
            return subprocess.CompletedProcess(argv, 1)
        self.assertEqual(a.worker(path, runner=gate), 124)
        outcome = json.loads(path.with_name(unit + '.outcome.json').read_text())
        self.assertGreaterEqual(outcome['disk_bytes'], 123456)
        self.assertEqual(a.complete(path, query=lambda unit: {})['result'], 'hang-guard')

    def test_wait_blocks_until_atomic_event_publication(self):
        a = module()
        unit, path = self.request(a)
        count = []
        def publish(seconds):
            count.append(seconds)
            a.atomic_json(self.ws / 'bennett/.tmp/gates/events' / (unit + '.json'), {'exit': 143})
        with patch.object(a.time, 'sleep', side_effect=publish):
            self.assertEqual(a.wait(unit, self.ws), 143)
        self.assertEqual(len(count), 1)

    def test_service_runtime_survives_caller_checkout_changes(self):
        a = module()
        calls = []
        expected = {'peak_bytes': 1, 'disk_bytes': 1, 'source': 'fixture'}
        with patch.object(a.admit, 'assess', return_value=(True, 'ok', expected)):
            unit = a.start(self.repo, self.sha, launcher=lambda argv, **k: (calls.append(argv) or subprocess.CompletedProcess(argv, 0)), workspace=self.ws)
        argv = calls[0]
        runtime = Path(argv[argv.index('worker') - 1])
        self.assertNotEqual(runtime, Path(a.__file__))
        self.assertTrue(runtime.is_relative_to(self.ws / 'bennett/.tmp/gates/runtime'))
        self.assertEqual(runtime.with_name('gate_run.py').read_bytes(), Path(a.gate_run.__file__).read_bytes())
        self.assertTrue(any(str(runtime) in x for x in argv if 'ExecStopPost=' in x))

    def test_runtime_install_failure_publishes_setup_event(self):
        a = module()
        expected = {'peak_bytes': 1, 'disk_bytes': 1, 'source': 'fixture'}
        with patch.object(a.admit, 'assess', return_value=(True, 'ok', expected)), \
             patch.object(a, 'install_runtime', side_effect=OSError('cannot snapshot runtime')):
            with self.assertRaisesRegex(a.LaunchError, 'cannot snapshot runtime'):
                a.start(self.repo, self.sha, workspace=self.ws,
                        launcher=lambda *a, **k: self.fail('must not launch'))
        events = list((self.ws / 'bennett/.tmp/gates/events').glob('*.json'))
        self.assertEqual(len(events), 1)
        self.assertEqual(json.loads(events[0].read_text())['result'], 'setup-error')
