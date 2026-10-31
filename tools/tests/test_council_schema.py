"""Schema/validator/prompt tests for tools/council.py (per-item severity removed 2026-10-31)."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

_PATH = Path(__file__).resolve().parent.parent / "council.py"
_spec = importlib.util.spec_from_file_location("council_under_test", _PATH)
council = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(council)


def good():
    return {"criteria": [{"id": c, "score": 3, "evidence": "e", "change": "c"}
                         for c in council.CRITERIA],
            "blocking": [], "suggestions": ["s"], "verdict": "revise", "summary": "ok",
            "path_to_accept": "none", "verdict_core": "revise",
            "previous_status": [], "regressions": []}


ITEM = {"id": "B1", "section": "s3", "scope": "core", "problem": "p", "fix": "f"}


class CouncilSchemaTest(unittest.TestCase):
    def test_item_without_severity_validates(self):
        r = good()
        r["blocking"] = [dict(ITEM)]
        self.assertEqual(council.validate(r), [])
        # The legacy `problem` item is rejected by a new-round schema, which requires `steps`
        # (structured items are tested in test_council_steps.py).
        self.assertTrue(any("steps: required" in e for e in council.schema_errors(r, council.schema())))

    def test_item_with_legacy_severity_still_validates(self):
        r = good()
        r["blocking"] = [dict(ITEM, severity="S0")]
        self.assertEqual(council.validate(r), [])

    def test_schema_does_not_mention_severity(self):
        sch = council.schema()
        item = sch["properties"]["blocking"]["items"]
        self.assertNotIn("severity", item["properties"])
        self.assertNotIn("severity", item["required"])
        self.assertNotIn("severity", json.dumps(sch))

    def test_accept_with_blocking_rejected(self):
        r = good()
        r["verdict"] = "accept"
        r["blocking"] = [dict(ITEM)]
        self.assertTrue(any("accept with non-empty" in e for e in council.validate(r)))

    def test_prompt_has_no_severity_word(self):
        prompt = council.build_prompt("DOC", "run", 1, rubric=str(council.RUBRIC))
        self.assertNotIn("severity", prompt.lower())
        self.assertIn("S1", prompt)  # the definition sentence stays


if __name__ == "__main__":
    unittest.main()
