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
