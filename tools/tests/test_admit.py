"""Admission policy and probes run with synthetic resources, never systemd services."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch


def module():
    path = Path(__file__).resolve().parents[1] / 'admit.py'
    spec = importlib.util.spec_from_file_location('admission_test', path)
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    return tool


class AdmissionTests(unittest.TestCase):
    def test_reservations_headroom_load_and_disk(self):
        a = module()
        gib = 1024 ** 3
        expected = {'peak_bytes': 8*gib, 'disk_bytes': 10*gib, 'source': 'fixture'}
        resources = {'mem_available': 16*gib, 'load1': 1, 'nproc': 8, 'disk_free': 31*gib}
        self.assertTrue(a.decide(resources, expected, [])[0])
        self.assertFalse(a.decide(resources, expected, [{'expected_peak': 8*gib, 'rss': 2*gib}])[0])
        for changes, reason in (({'load1': 4}, 'load'), ({'disk_free': 29*gib}, 'disk'),
                                ({'mem_available': 13*gib}, 'memory')):
            with self.subTest(changes=changes):
                ok, text = a.decide(dict(resources, **changes), expected, [])
                self.assertFalse(ok)
                self.assertIn(reason, text)
        self.assertTrue(a.decide(resources, expected, [{'expected_peak': gib, 'rss': 2*gib}])[0])

    def test_no_history_names_conservative_defaults(self):
        a = module()
        result = a.expected_from_history([])
        self.assertEqual(result['peak_bytes'], a.DEFAULT_PEAK_BYTES)
        self.assertEqual(result['disk_bytes'], a.DEFAULT_DISK_BYTES)
        self.assertIn('default', result['source'])
        recent = a.expected_from_history([
            {'finished_utc': '2026-01-02', 'peak_rss_kib': 2048, 'disk_bytes': 4000},
            {'finished_utc': '2026-01-01', 'peak_rss_kib': 4096, 'disk_bytes': 8000}])
        self.assertEqual((recent['peak_bytes'], recent['disk_bytes']), (2048*1024, 4000))

    def test_probe_failure_is_wait_with_named_error(self):
        a = module()
        with patch.object(a, 'resources', side_effect=OSError('missing meminfo')):
            with patch.object(a, 'history', return_value=[]), patch.object(a, 'running_reservations', return_value=[]):
                ok, reason, expected = a.assess(Path('/repo'), Path('/workspace'), 'full')
        self.assertFalse(ok)
        self.assertIn('missing meminfo', reason)

    def test_rss_reservations_do_not_subtract_reclaimable_file_cache(self):
        import tempfile
        a = module()
        with tempfile.TemporaryDirectory() as tmp:
            cgroup = Path(tmp) / 'user.slice/service'
            cgroup.mkdir(parents=True)
            (cgroup / 'memory.stat').write_text('anon 2048\nfile 8192\nshmem 1024\n')
            with patch.object(a, 'CGROUP_ROOT', Path(tmp)):
                self.assertEqual(a.current_rss({'ControlGroup': '/user.slice/service',
                                                'ActiveState': 'active', 'MemoryCurrent': '11264'}), 3072)


# Same two-space-separated columns emitted by quota's table renderer. Non-weekly
# windows and balances must not be confused with the aggregate weekly pace.
def quota_fixture(codex='10.0% behind', used='40.0%', claude='5.0% behind', muse='on pace'):
    return ('VENDOR  WINDOW  USED  REMAINING  PACE  TODAY  BANKED  RESETS  STATUS\n'
            'Claude  5-hour session  99.0%  1.0%  +90.0% ahead  0.0%  —  soon  ok\n'
            f'Claude  Weekly  45.0%  55.0%  {claude}  1.0%  —  soon  ok\n'
            f'Codex  Weekly  {used}  60.0%  {codex}  1.0%  —  soon  ok\n'
            f'Muse  Weekly  50.0%  50.0%  {muse}  1.0%  —  soon  ok\n'
            '\nBALANCES\nVENDOR  BALANCE  REMAINING  USED  LIMIT\n'
            'Codex  Credits  $10.00  $1.00  $11.00\n')


class LaunchTests(unittest.TestCase):
    def setUp(self):
        self.a = module()
        self.expected = {'peak_bytes': 8*self.a.GIB, 'disk_bytes': 10*self.a.GIB, 'source': 'fixture'}
        self.resources = {'mem_available': 32*self.a.GIB, 'load1': 1, 'nproc': 8,
                          'disk_free': 64*self.a.GIB}
        self.dial = {vendor: 1.0 for vendor in ('codex', 'claude', 'muse')}

    def decision(self, output=None, vendor='codex', kind='implementer', **changes):
        return self.a.decide_launch(dict(self.resources, **changes), self.expected, [],
                                    quota_fixture() if output is None else output,
                                    self.dial, vendor, kind)

    def test_every_kind_obeys_pace_without_child_caps(self):
        for kind in ('implementer', 'review', 'gate', 'council'):
            with self.subTest(kind=kind):
                ok, reason = self.decision(kind=kind)
                self.assertTrue(ok, reason)
                self.assertIn('codex 10.0pp below', reason)
                self.assertIn('claude 5.0pp below', reason)
                self.assertIn('muse 0.0pp at', reason)
                self.assertIn(kind, reason)
                ok, reason = self.decision(quota_fixture('+1.0% ahead', '51.0%'), kind=kind)
                self.assertFalse(ok)
                self.assertIn('codex 1.0pp above', reason)

    def test_at_line_waits_including_numeric_zero(self):
        for pace in ('on pace', '+0.0% ahead', '0.0% behind'):
            with self.subTest(pace=pace):
                ok, reason = self.decision(quota_fixture(pace, '50.0%'))
                self.assertFalse(ok)
                self.assertIn('codex 0.0pp at', reason)

    def test_dial_multiplies_uniform_line_not_absolute_budget(self):
        self.dial['codex'] = 1.2
        # Uniform line = 50%; 120% of that is 60%, not 70%.
        for used, delta, allowed in (('55.0%', '+5.0% ahead', True),
                                     ('60.0%', '+10.0% ahead', False),
                                     ('61.0%', '+11.0% ahead', False)):
            with self.subTest(used=used):
                self.assertEqual(self.decision(quota_fixture(delta, used))[0], allowed)
        self.dial['codex'] = 0
        self.assertFalse(self.decision()[0])

    def test_resources_and_running_gate_reservations_still_apply(self):
        for changes in ({'mem_available': 13*self.a.GIB}, {'load1': 4},
                        {'disk_free': 29*self.a.GIB}):
            with self.subTest(changes=changes):
                self.assertFalse(self.decision(**changes)[0])
        ok, reason = self.a.decide_launch(self.resources, self.expected,
                                         [{'expected_peak': 24*self.a.GIB, 'rss': self.a.GIB}],
                                         quota_fixture(), self.dial, 'codex', 'review')
        self.assertFalse(ok)
        self.assertIn(f'reserved={23*self.a.GIB}', reason)

    def test_unreadable_missing_duplicate_locked_and_idle_weekly_wait(self):
        fixtures = ('', 'quota CLI not found', quota_fixture('—'),
                    quota_fixture().replace('Codex  Weekly', 'Codex  Secondary'),
                    quota_fixture() + 'Codex  Weekly  40.0%  60.0%  10.0% behind  1%  —  soon  ok\n',
                    quota_fixture().replace('soon  ok', 'soon  locked: usage_limit_reached'),
                    quota_fixture().replace('soon  ok', 'soon  idle (not started)'),
                    quota_fixture('nonsense'), quota_fixture('150.0% behind'),
                    quota_fixture(used='NaN%'))
        for output in fixtures:
            with self.subTest(output=output):
                ok, reason = self.decision(output)
                self.assertFalse(ok)
                self.assertIn('codex unavailable', reason)

    def test_other_vendor_errors_are_reported_without_inventing_a_value(self):
        output = quota_fixture().replace('Muse  Weekly  50.0%  50.0%  on pace  1.0%  —  soon  ok',
                                         'Muse  —  —  —  —  —  —  —  error: unavailable')
        ok, reason = self.decision(output)
        self.assertTrue(ok, reason)
        self.assertIn('muse unavailable', reason)
        self.assertFalse(self.decision(output, vendor='muse')[0])

    def test_invalid_dial_fails_closed(self):
        for value in (-1, float('nan'), float('inf'), True, 'fast'):
            with self.subTest(value=value):
                self.dial['codex'] = value
                ok, reason = self.decision()
                self.assertFalse(ok)
                self.assertIn('dial', reason)

    def test_dial_file_has_exactly_one_number_per_vendor(self):
        dial = self.a.read_dial(Path(__file__).resolve().parents[2] / 'dial.toml')
        self.assertEqual(dial, self.dial)

    def test_missing_malformed_and_extra_dial_settings_fail_closed(self):
        import tempfile
        valid = '[codex]\npace=1.0\n[claude]\npace=1.0\n[muse]\npace=1.0\n'
        fixtures = ('', 'bad toml', valid.replace('[muse]\npace=1.0\n', ''),
                    valid + 'children=2\n', valid.replace('pace=1.0', 'pace=true'),
                    valid.replace('pace=1.0', 'pace=nan'), valid + '[other]\npace=1.0\n')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'dial.toml'
            with self.assertRaises(OSError):
                self.a.read_dial(path)
            for fixture in fixtures:
                with self.subTest(fixture=fixture):
                    path.write_text(fixture)
                    with self.assertRaises(ValueError):
                        self.a.read_dial(path)

    def test_launch_cli_and_existing_gate_cli(self):
        import contextlib
        import io
        import subprocess
        for command, status in ((['launch', '--vendor', 'codex', '--kind', 'review'], 0),
                                (['launch', '--vendor', 'muse', '--kind', 'council'], 1),
                                (['gate', '--repo', '/repo'], 0)):
            with self.subTest(command=command), patch('sys.argv', ['admit.py', *command]), \
                    patch.object(self.a.subprocess, 'run', return_value=subprocess.CompletedProcess(
                        [], 0, '/workspace/bennett/.git\n', '')), \
                    patch.object(self.a, 'history', return_value=[]), \
                    patch.object(self.a, 'resources', return_value=self.resources), \
                    patch.object(self.a, 'running_reservations', return_value=[]), \
                    patch.object(self.a, 'quota_output', return_value=quota_fixture()), \
                    contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(self.a.main(), status)
                self.assertTrue(output.getvalue().startswith('ADMIT ' if status == 0 else 'WAIT '))

    def test_cli_probe_failure_is_wait(self):
        import contextlib
        import io
        import subprocess
        with patch('sys.argv', ['admit.py', 'launch', '--vendor', 'codex', '--kind', 'implementer']), \
                patch.object(self.a.subprocess, 'run', return_value=subprocess.CompletedProcess(
                    [], 0, '/workspace/bennett/.git\n', '')), \
                patch.object(self.a, 'quota_output', side_effect=RuntimeError('quota unavailable')), \
                patch.object(self.a, 'history', return_value=[]), \
                patch.object(self.a, 'resources', return_value=self.resources), \
                patch.object(self.a, 'running_reservations', return_value=[]), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(self.a.main(), 1)
            self.assertIn('WAIT ', output.getvalue())
            self.assertIn('quota unavailable', output.getvalue())


class QuotaCacheTests(unittest.TestCase):
    def test_concurrent_callers_share_one_locked_probe(self):
        from concurrent.futures import ThreadPoolExecutor
        import fcntl
        import subprocess
        import tempfile
        import threading
        from unittest.mock import Mock
        a = module()
        start = threading.Barrier(4)
        with tempfile.TemporaryDirectory() as tmp:
            def probe(*args, **kwargs):
                # A separate descriptor must be excluded while the CLI is running.
                with (Path(tmp) / 'quota.lock').open('a') as lock:
                    with self.assertRaises(BlockingIOError):
                        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return subprocess.CompletedProcess([], 0, quota_fixture(), '')

            runner = Mock(side_effect=probe)

            def invoke(_):
                start.wait()
                return a.quota_output(Path(tmp), runner=runner, clock=lambda: 1000)

            with ThreadPoolExecutor(max_workers=4) as pool:
                self.assertEqual(list(pool.map(invoke, range(4))), [quota_fixture()] * 4)
            runner.assert_called_once()

    def test_success_cached_until_five_minutes_including_expiry(self):
        import subprocess
        import tempfile
        from unittest.mock import Mock
        a = module()
        runner = Mock(return_value=subprocess.CompletedProcess([], 0, quota_fixture(), ''))
        with tempfile.TemporaryDirectory() as tmp:
            for now, count in ((1000, 1), (1299, 1), (1300, 2), (1301, 2)):
                self.assertEqual(a.quota_output(Path(tmp), runner=runner, clock=lambda: now), quota_fixture())
                self.assertEqual(runner.call_count, count)
            cache = a.read_json(Path(tmp) / 'quota.json')
            self.assertEqual(cache['timestamp'], 1300)

    def test_probe_failures_cached_and_recover_after_expiry(self):
        import subprocess
        import tempfile
        from unittest.mock import Mock
        for failure in (subprocess.CompletedProcess([], 127, '', 'CLI not found'),
                        subprocess.TimeoutExpired('quota', 60), OSError('missing quota')):
            a = module()
            runner = Mock(side_effect=failure) if isinstance(failure, Exception) else Mock(return_value=failure)
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as tmp:
                for now in (1000, 1299):
                    with self.assertRaisesRegex(RuntimeError, 'quota'):
                        a.quota_output(Path(tmp), runner=runner, clock=lambda: now)
                self.assertEqual(runner.call_count, 1)
                runner.side_effect = None
                runner.return_value = subprocess.CompletedProcess([], 0, quota_fixture(), '')
                self.assertEqual(a.quota_output(Path(tmp), runner=runner, clock=lambda: 1300), quota_fixture())

    def test_corrupt_or_future_cache_waits_without_a_probe(self):
        import tempfile
        from unittest.mock import Mock
        a = module()
        for content in ('broken json', '{"timestamp": 2000, "output": "x", "error": null}'):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as tmp:
                (Path(tmp) / 'quota.json').write_text(content)
                runner = Mock(side_effect=AssertionError('must not probe'))
                with self.assertRaises((RuntimeError, ValueError)):
                    a.quota_output(Path(tmp), runner=runner, clock=lambda: 1000)
                runner.assert_not_called()
