from datetime import datetime, timezone
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import admit  # noqa: E402


class QuietHold(unittest.TestCase):
    def test_drain_and_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'w.txt'
            path.write_text('# note\n2026-11-11T16:00:00+00:00 2026-11-11T16:10:00+00:00 llm\n')
            at = lambda h, m: datetime(2026, 11, 11, h, m, tzinfo=timezone.utc)
            self.assertTrue(admit.quiet_hold('full', at(15, 10), path))
            self.assertFalse(admit.quiet_hold('pre-merge', at(15, 10), path))
            self.assertTrue(admit.quiet_hold('pre-merge', at(15, 45), path))
            self.assertTrue(admit.quiet_hold('pre-merge', at(16, 5), path))
            self.assertFalse(admit.quiet_hold('full', at(16, 10), path))
            self.assertFalse(admit.quiet_hold('full', at(15, 0), Path(tmp) / 'missing'))


if __name__ == '__main__':
    unittest.main()
