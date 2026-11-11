"""The rulebook has one mechanical cap: COMMON.md may not grow past docs/process/BUDGET.toml's line count."""
import pathlib
import tomllib
import unittest

PROCESS = pathlib.Path(__file__).resolve().parents[2] / "docs" / "process"


class RulebookBudgetTests(unittest.TestCase):
    def test_common_line_cap(self) -> None:
        cap = tomllib.loads((PROCESS / "BUDGET.toml").read_text())["common_lines"]
        n = len((PROCESS / "COMMON.md").read_text().splitlines())
        self.assertLessEqual(n, cap, f"COMMON.md has {n} lines, cap {cap}; only the maintainer raises it")


if __name__ == "__main__":
    unittest.main()
