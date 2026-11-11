"""Detached service lifecycle with injected launch; no real units are started."""
import importlib.util
import json
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

    def test_stop_post_without_worker_outcome_maps_signal_and_timeout(self):
        a = module()
        for code, status, service, expected in [('killed', 'TERM', 'signal', 143),
                                               ('exited', '0', 'success', 0),
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
        with patch.object(a, 'run_gate', side_effect=run):
            self.assertEqual(a.worker(path), 3)
        self.assertEqual(json.loads(path.with_name(unit + '.outcome.json').read_text())['exit'], 3)

    def test_launcher_failure_writes_setup_event(self):
        a = module()
        expected = {'peak_bytes': 100, 'disk_bytes': 200, 'source': 'fixture'}
        with patch.object(a.admit, 'assess', return_value=(True, 'ok', expected)):
            with self.assertRaisesRegex(a.LaunchError, 'systemd'):
                a.start(self.repo, self.sha, 'full', launcher=lambda argv, **k: subprocess.CompletedProcess(argv, 1, '', 'no bus'), workspace=self.ws)
        events = list((self.ws / 'bennett/.tmp/gates/events').glob('*.json'))
        self.assertEqual(len(events), 1)
        self.assertEqual(json.loads(events[0].read_text())['exit'], 3)
