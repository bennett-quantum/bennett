"""Reverts exercise local bare remotes; gates are injected and never run components."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'revert_landing.py'


def load_tool():
    spec = importlib.util.spec_from_file_location('revert_landing', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RevertTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / 'producer'
        self.repo.mkdir()
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_AUTHOR_NAME='Fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                        GIT_COMMITTER_NAME='Fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
        self.patcher = patch.dict(os.environ, self.env, clear=True)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.git('init', '-qb', 'main')
        (self.repo / 'value').write_text('green')
        (self.repo / 'scripts').mkdir()
        (self.repo / 'scripts/pre-push').write_text('#!/bin/sh\nexit 99\n')
        self.git('add', 'value', 'scripts/pre-push')
        self.git('commit', '-qm', 'green')
        self.green = self.git('rev-parse', 'HEAD')
        self.git('switch', '-qc', 'feature')
        (self.repo / 'value').write_text('red')
        self.git('commit', '-qam', 'red')
        self.feature = self.git('rev-parse', 'HEAD')
        self.git('switch', '-q', 'main')
        self.git('merge', '--no-ff', '-qm', 'Merge bad', 'feature')
        self.merge = self.git('rev-parse', 'HEAD')
        self.remote = self.root / 'remote.git'
        self.git('clone', '-q', '--bare', str(self.repo), str(self.remote))
        self.git('remote', 'add', 'origin', str(self.remote))
        self.consumer = self.root / 'consumer'
        self.consumer.mkdir()
        subprocess.run(['git', 'init', '-qb', 'main', str(self.consumer)], check=True, capture_output=True)
        (self.consumer / 'gate.toml').write_text('[siblings.producer]\nsha="' + self.merge + '"\n')
        subprocess.run(['git', '-C', str(self.consumer), 'add', 'gate.toml'], check=True, env=self.env)
        subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-C', str(self.consumer), 'commit', '-qm', 'pin'], check=True, env=self.env)
        self.r = load_tool()

    def git(self, *args):
        return subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-C', str(self.repo), *args],
                              env=self.env, capture_output=True, text=True, check=True, timeout=30).stdout.strip()

    def test_untracked_files_do_not_block_a_revert(self):
        (self.repo / 'untracked').write_text('like .beads/hooks')
        outcome = self.r.revert(self.repo, self.merge, workspace=self.root)
        self.assertEqual(self.git('ls-remote', 'origin', 'refs/heads/main').split()[0], outcome['sha'])

    def test_revert_pushes_and_lists_immutable_pins(self):
        outcome = self.r.revert(self.repo, self.merge, workspace=self.root)
        head = self.git('rev-parse', 'HEAD')
        self.assertEqual(outcome['sha'], head)
        self.assertEqual(self.git('ls-remote', 'origin', 'refs/heads/main').split()[0], head)
        self.assertEqual(outcome['consumers'], [dict(repo='consumer', pin=self.merge)])
        self.assertEqual(self.git('cat-file', '-t', self.merge), 'commit')

    def test_nonmerge_sidebranch_dirty_and_divergent_main_are_rejected(self):
        for sha in (self.green, self.feature):
            with self.subTest(sha=sha), self.assertRaises(self.r.RevertError):
                self.r.revert(self.repo, sha, workspace=self.root)
        committed = self.git('show', 'HEAD:value')
        (self.repo / 'value').write_text('dirty')
        with self.assertRaisesRegex(self.r.RevertError, 'clean'):
            self.r.revert(self.repo, self.merge, workspace=self.root)
        (self.repo / 'value').write_text(committed)
        (self.repo / 'value').write_text('ahead')
        self.git('commit', '-qam', 'ahead')
        with self.assertRaisesRegex(self.r.RevertError, 'origin/main'):
            self.r.revert(self.repo, self.merge, workspace=self.root)

    def test_branch_checkout_rejected_before_revert(self):
        self.git('switch', '-q', 'feature')
        with self.assertRaisesRegex(self.r.RevertError, 'main'):
            self.r.revert(self.repo, self.merge, workspace=self.root)
