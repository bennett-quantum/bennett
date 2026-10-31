"""Structured (Lamport-style) blocking items: shape rules, spec-gap handling, rendering."""
import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_council_schema import council, good  # noqa: E402


def steps():
    return [{"n": "<1>1", "claim": "ISA-17-P9 requires fault F3 on empty input", "by": "clause:ISA-17-P9"},
            {"n": "<1>2", "claim": "the interpreter returns 0 instead",
             "by": "witness:bennett-isa-ref run-oracle fx/empty.json"},
            {"n": "<1>3", "claim": "so the two differ on the empty input; add the fault",
             "by": "step:<1>1, <1>2"}]


def item(**kw):
    d = {"id": "B1", "section": "s17", "scope": "core", "kind": "implementation",
         "steps": steps(), "fix": "return F3"}
    d.update(kw)
    return d


def review(*items, verdict="revise"):
    r = good()
    r["blocking"] = list(items)
    r["verdict"] = verdict
    return r


class StepsTest(unittest.TestCase):
    def test_valid_structured_item(self):
        r = review(item())
        self.assertEqual(council.validate(r), [])
        self.assertEqual(council.schema_errors(r, council.schema()), [])

    def test_problem_alongside_steps_is_tolerated(self):
        self.assertEqual(council.validate(review(item(problem="ignored"))), [])

    def test_missing_steps_rejected_on_new_schema(self):
        legacy = {"id": "B1", "section": "s", "scope": "core", "problem": "p", "fix": "f"}
        errs = council.schema_errors(review(legacy), council.schema())
        self.assertTrue(any("steps: required" in e for e in errs), errs)

    def test_legacy_item_validates_on_legacy_path(self):
        legacy = {"id": "B1", "section": "s", "scope": "core", "problem": "p", "fix": "f"}
        self.assertEqual(council.validate(review(legacy)), [])

    def test_step_count_bounds(self):
        for n in (2, 7):
            st = steps()[:2] if n == 2 else steps() + [dict(steps()[1], n=f"<1>{k}") for k in range(4, 8)]
            r = review(item(steps=st))
            self.assertTrue(council.validate(r) or council.schema_errors(r, council.schema()))
            self.assertTrue(council.schema_errors(r, council.schema()))
            self.assertTrue(any("3-6" in e for e in council.validate(r)))

    def test_step_one_witness_rejected(self):
        st = steps()
        st[0]["by"] = "witness:cargo test"
        errs = council.validate(review(item(steps=st)))
        self.assertTrue(any("step 1 must say what the spec requires" in e for e in errs), errs)

    def test_assumed_step_one_needs_spec_gap_kind(self):
        st = steps()
        st[0]["by"] = "ASSUMED: the spec is silent on empty input"
        errs = council.validate(review(item(steps=st)))
        self.assertTrue(any('"kind": "spec-gap"' in e for e in errs), errs)
        self.assertEqual(council.validate(review(item(steps=st, kind="spec-gap"))), [])

    def test_spec_gap_kind_requires_assumed_step_one(self):
        errs = council.validate(review(item(kind="spec-gap")))
        self.assertTrue(any("requires step 1 to be `ASSUMED:`" in e for e in errs), errs)

    def test_missing_witness_rejected(self):
        st = steps()
        st[1]["by"] = "clause:ISA-17-P2"
        errs = council.validate(review(item(steps=st)))
        self.assertTrue(any("`witness:`" in e for e in errs), errs)

    def test_last_step_must_cite_steps(self):
        st = steps()
        st[2]["by"] = "clause:ISA-17-P9"
        errs = council.validate(review(item(steps=st)))
        self.assertTrue(any("must cite earlier steps" in e for e in errs), errs)

    def test_cited_step_must_exist_earlier(self):
        st = steps()
        st[2]["by"] = "step:<1>1, <1>9"
        errs = council.validate(review(item(steps=st)))
        self.assertTrue(any("not an earlier step" in e for e in errs), errs)

    def test_unknown_kind_rejected(self):
        errs = council.validate(review(item(kind="whatever")))
        self.assertTrue(any("not in" in e for e in errs), errs)

    def test_accept_with_only_spec_gaps_is_valid(self):
        st = steps()
        st[0]["by"] = "ASSUMED: silent"
        r = review(item(steps=st, kind="spec-gap"), verdict="accept")
        self.assertEqual(council.validate(r), [])

    def test_accept_with_implementation_item_rejected(self):
        r = review(item(), verdict="accept")
        self.assertTrue(any("accept with non-empty" in e for e in council.validate(r)))

    def test_schema_requires_steps_and_drops_problem(self):
        it = council.schema()["properties"]["blocking"]["items"]
        self.assertIn("steps", it["required"])
        self.assertNotIn("problem", it["properties"])

    def test_prompt_describes_shape_without_severity(self):
        prompt = council.build_prompt("DOC", "run", 1, rubric=str(council.RUBRIC))
        for needle in ("`steps`", "`clause:<ID>`", "`ASSUMED:", "spec-gap", "`witness:"):
            self.assertIn(needle, prompt)
        self.assertNotIn("severity", prompt.lower())
        self.assertLessEqual(len(council.STRUCTURED.splitlines()), 8)


class AggregateRenderTest(unittest.TestCase):
    def aggregate(self, outputs):
        with tempfile.TemporaryDirectory() as td, patch.object(council, "COUNCIL", Path(td)):
            rdir = council.round_dir("r", 1)
            for m, out in outputs.items():
                council.atomic_write(rdir / f"out-{m}.json", json.dumps(out))
            council.atomic_write(rdir / "state.json", json.dumps({"member_list": list(outputs)}))
            with contextlib.redirect_stdout(io.StringIO()):
                council.aggregate_cmd(type("A", (), {"run": "r", "round": 1})())
            return ((rdir / "report.md").read_text(),
                    json.loads((rdir / "consensus.json").read_text()))

    def test_steps_and_spec_gap_rendering(self):
        gap_steps = steps()
        gap_steps[0]["by"] = "ASSUMED: silent"
        r = review(item(), item(id="B2", steps=gap_steps, kind="spec-gap"))
        report, cons = self.aggregate({"codex": r})
        self.assertIn("  <1>1 ISA-17-P9 requires fault F3 on empty input  — clause:ISA-17-P9", report)
        self.assertIn("  <1>3 so the two differ on the empty input; add the fault  — step:<1>1, <1>2", report)
        self.assertIn("## Spec gaps (not editor blockers)", report)
        main, gaps = report.split("## Spec gaps (not editor blockers)")
        self.assertIn("**[codex] B1**", main)
        self.assertNotIn("B2", main.split("## codex")[0])
        self.assertIn("**[codex] B2**", gaps)
        self.assertEqual([b["id"] for b in cons["blocking"]["codex"]], ["B1"])
        self.assertEqual([b["id"] for b in cons["spec_gaps"]["codex"]], ["B2"])
        self.assertIn("core 1 / contract 0 (blocking 1)", report)

    def test_only_spec_gaps_reaches_consensus(self):
        gap_steps = steps()
        gap_steps[0]["by"] = "ASSUMED: silent"
        r = review(item(steps=gap_steps, kind="spec-gap"), verdict="accept")
        r["verdict_core"] = "accept"
        report, cons = self.aggregate({"codex": r})
        self.assertTrue(cons["agree"] and cons["core_agree"])
        self.assertIn("- none", report)

    def test_legacy_rendering_unchanged_and_no_spec_gap_heading(self):
        legacy = {"id": "B1", "section": "s", "scope": "core", "problem": "old problem", "fix": "f"}
        report, cons = self.aggregate({"codex": review(legacy)})
        self.assertIn("- **[codex] B1** (s; core): old problem *Fix:* f", report)
        self.assertNotIn("Spec gaps", report)
        self.assertNotIn("spec_gaps", cons)


if __name__ == "__main__":
    unittest.main()
