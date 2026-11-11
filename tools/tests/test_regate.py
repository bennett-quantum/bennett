"""regate's decision: only moved, idle repos get a background full run."""
import importlib.util
from pathlib import Path
import unittest


def module():
    path = Path(__file__).resolve().parents[1] / 'regate.py'
    spec = importlib.util.spec_from_file_location('regate_test', path)
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    return tool


class RegateTests(unittest.TestCase):
    def test_moved_idle_repos_only(self):
        r = module()
        heads = {'a': '1' * 40, 'b': '2' * 40, 'c': '3' * 40, 'd': '4' * 40}
        state = {'a': {'sha': '1' * 40}, 'b': {'sha': 'f' * 40}, 'c': {'sha': 'e' * 40}}
        self.assertEqual(r.plan(heads, state, running={'c'}), [('b', '2' * 40), ('d', '4' * 40)])

    def test_manifest_repos_are_the_gated_ones(self):
        names = module().repos()
        self.assertIn('bennett-plugin', names)
        self.assertNotIn('Bennett.jl', names)


if __name__ == '__main__':
    unittest.main()
