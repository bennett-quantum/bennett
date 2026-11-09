"""Rulebook ratchet: the process rulebook may shrink, never grow, without a deliberate budget change.

Maintainer 2026-11-09: rule accretion is a cross-project failure mode that has killed projects; every
saved lesson about it recurred. This test takes the decision away from the agent at the moment of a
correction: COMMON.md and T3CHILD.md cannot exceed docs/process/BUDGET.toml, numbered rules cannot
multiply, and READ FIRST lines expire. Raising the budget is a visible diff to BUDGET.toml, not an edit
to the rulebook.
"""
import datetime as _dt
import pathlib
import re
import tomllib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
PROCESS = ROOT / "docs" / "process"


def _read_first_bullets(text: str) -> list[str]:
    head = text.split("\n# Common rules", 1)[0]
    return [line for line in head.splitlines() if line.startswith("- ")]


class RulebookBudgetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.budget = tomllib.loads((PROCESS / "BUDGET.toml").read_text())
        cls.common = (PROCESS / "COMMON.md").read_text()
        cls.t3child = (PROCESS / "T3CHILD.md").read_text()

    def test_common_line_budget(self) -> None:
        n = len(self.common.splitlines())
        self.assertLessEqual(
            n, self.budget["common_lines"],
            f"COMMON.md has {n} lines, budget {self.budget['common_lines']}: delete a rule before adding one",
        )

    def test_t3child_line_budget(self) -> None:
        n = len(self.t3child.splitlines())
        self.assertLessEqual(
            n, self.budget["t3child_lines"],
            f"T3CHILD.md has {n} lines, budget {self.budget['t3child_lines']}",
        )

    def test_numbered_rule_budget(self) -> None:
        n = len(re.findall(r"^\d+\. ", self.common, flags=re.M))
        self.assertLessEqual(
            n, self.budget["standing_rules"],
            f"COMMON.md has {n} numbered rules, budget {self.budget['standing_rules']}: merge or strike one first",
        )

    def test_read_first_count_and_age(self) -> None:
        bullets = _read_first_bullets(self.common)
        self.assertLessEqual(
            len(bullets), self.budget["read_first_lines"],
            f"READ FIRST has {len(bullets)} live lines, budget {self.budget['read_first_lines']}",
        )
        today = _dt.date.today()
        for line in bullets:
            m = re.match(r"- (\d{4}-\d{2}-\d{2})", line)
            self.assertIsNotNone(m, f"READ FIRST line without a leading date: {line[:80]}")
            age = (today - _dt.date.fromisoformat(m.group(1))).days
            self.assertLessEqual(
                age, self.budget["read_first_max_age_days"],
                f"READ FIRST line is {age} days old; promote it into a standing rule (deleting another) or delete it: {line[:80]}",
            )


if __name__ == "__main__":
    unittest.main()
