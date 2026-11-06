"""Checks migrated from council.py selftest; assertions survive python -O."""
import contextlib
import datetime as dt
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools import council
from tools.council import (CRITERIA, MEMBERS, RUBRIC, State, atomic_write, build_prompt,
                          extract_json, main, member_cmd, parse_member_output, round_dir,
                          run_cwd, run_member, run_members, schema, validate)


class CouncilSelftestTests(unittest.TestCase):
    def setUp(self):
        self.good = {
            "criteria": [{"id": c, "score": 3, "evidence": "e", "change": "c"} for c in CRITERIA],
            "blocking": [], "suggestions": ["s"], "verdict": "accept", "summary": "ok",
            "path_to_accept": "none", "verdict_core": "accept", "previous_status": [], "regressions": [],
        }

    def test_validation_and_parsing(self):
        good = self.good
        self.assertEqual(validate(good), [], validate(good))
        bad = json.loads(json.dumps(good))
        bad['criteria'][0]['score'] = 6
        bad['verdict'] = 'accept'
        bad['blocking'] = [{'id': 'B1', 'section': '§3', 'scope': 'core', 'severity': 'S0',
                            'problem': 'p', 'fix': 'f'}]
        errs = validate(bad)
        self.assertTrue(any('outside 1-5' in e for e in errs), errs)
        self.assertTrue(any('accept with non-empty' in e for e in errs), errs)
        self.assertEqual(validate({'criteria': 'x'}), ['criteria missing'])
        self.assertEqual(extract_json('noise {"a": 1} more {"b": [1,2]} tail'), {'b': [1, 2]})
        self.assertIs(extract_json('none'), None)
        opus_wrap = json.dumps({'type': 'result', 'structured_output': good, 'result': 'x'})
        self.assertEqual(parse_member_output('opus', opus_wrap, Path('/nonexistent')), good)
        sch = schema()
        self.assertTrue(set(sch['required']) >=
                        {'criteria', 'blocking', 'suggestions', 'verdict', 'path_to_accept', 'summary'})
        self.assertIn('verdict_core', sch['properties'])
        self.assertIn('previous_status', sch['properties'])

    def test_member_commands_and_state(self):
        sch = schema()
        with tempfile.TemporaryDirectory() as td, \
                patch.dict(os.environ, {'CLAUDECODE': 'fixture', 'CLAUDE_CODE_TEST': 'fixture'}):
            rdir = Path(td)
            atomic_write(rdir / 'prompt.md', 'p')
            atomic_write(rdir / 'schema.json', json.dumps(sch))
            for m in MEMBERS:
                cmd, env, stdin, out = member_cmd(m, rdir)
                executable = 'claude' if m in ('opus', 'fable') else 'codex' if m == 'sol' else m
                self.assertEqual(cmd[0], executable, cmd)
                if m in ('opus', 'fable'):
                    self.assertFalse(any(k.startswith('CLAUDE_CODE_') or k == 'CLAUDECODE' for k in env))
                    self.assertIn('--allowedTools', cmd)
                    self.assertNotEqual(cmd[-1], 'p', 'prompt must go on stdin')
                if m in ('sol', 'codex'):
                    self.assertEqual(cmd[-1], '-')
                    self.assertIsNot(stdin, subprocess.DEVNULL)
                    self.assertEqual(cmd[cmd.index('-m') + 1], 'gpt-6.1-sol' if m == 'sol' else 'gpt-6-astra')
                    self.assertIn('model_reasoning_effort=xhigh', cmd)
                if stdin is not subprocess.DEVNULL:
                    stdin.close()
            st = State(rdir)
            st.update('codex', status='running', attempts=1)
            self.assertEqual(json.loads((rdir / 'state.json').read_text())['members']['codex']['attempts'], 1)

    def test_round_configuration(self):
        sch = schema()
        with tempfile.TemporaryDirectory() as td:
            rdir = Path(td)
            atomic_write(rdir / 'schema.json', json.dumps(sch))
            atomic_write(rdir / 'prompt.md', 'p')
            cmd, env, stdin, out = member_cmd('fable', rdir, td)
            self.assertIn('--model', cmd)
            self.assertEqual(cmd[cmd.index('--model') + 1], 'fable')
            self.assertTrue(any(c.startswith('Bash(cargo test') for c in cmd))
            self.assertNotIn('Write', cmd)
            stdin.close()
            st = State(rdir)
            st.d['member_list'] = ['fable', 'codex', 'muse']
            st.d['cwd'] = td
            st.save()
            self.assertEqual(run_members(rdir), ('fable', 'codex', 'muse'))
            self.assertEqual(run_cwd(rdir), td)
            tf = rdir / 'task.md'
            atomic_write(tf, 'task for SUBJECT')
            pr = build_prompt('DOC', 'r', 1, subject='X', rubric=str(RUBRIC), task_file=str(tf))
            self.assertIn('task for X', pr)
            self.assertNotIn('Convergence rules for this council', pr)

    def test_external_collection_cli(self):
        good, sch = self.good, schema()
        with tempfile.TemporaryDirectory() as td, patch.object(council, 'COUNCIL', Path(td)):

            def cli(*args, error=None):
                output = io.StringIO()
                with patch.object(sys, 'argv', [str(Path(__file__).resolve()), *args]), \
                        contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                    try:
                        main()
                    except SystemExit as e:
                        if error is None:
                            raise
                        self.assertNotEqual(e.code, 0, e.code)
                        message = output.getvalue() + str(e.code)
                        self.assertIn(error, message, message)
                    else:
                        self.assertIs(error, None, f'expected failure: {error}')
                return output.getvalue()
            doc = Path(td) / 'fixture.md'
            atomic_write(doc, 'Council fixture document')
            cli('prepare', '--run', 'external', '--round', '1', '--doc', str(doc), '--members', 'sol,codex,muse', '--cwd', td)
            rdir = round_dir('external', 1)
            common = ('--run', 'external', '--round', '1')
            self.assertEqual(cli('prompt-path', *common).splitlines(), [str(rdir / 'prompt.md'), td])
            self.assertEqual(run_members(rdir), ('sol', 'codex', 'muse'))
            cli('run', *common, '--dry-run')
            source = Path(td) / 'member.json'
            for m in ('sol', 'codex', 'muse'):
                raw = 'member status\n' + json.dumps(good) + '\nfinished\n'
                atomic_write(source, raw)
                os.utime(source, (1700000000, 1700000000))
                cli('collect', *common, '--member', m, '--file', str(source))
                self.assertEqual(json.loads((rdir / f'out-{m}.json').read_text()), good)
                record = (rdir / f'raw-{m}-1.txt').read_text()
                self.assertTrue(raw in record and 'collected externally' in record, record)
                state = State(rdir).d['members'][m]
                self.assertTrue(state['status'] == 'done' and state['attempts'] == 1, state)
                self.assertTrue(state['exit'] == 0 and state['seconds'] >= 0 and state['updated'], state)
                self.assertEqual(dt.datetime.fromisoformat(state['started']).timestamp(), source.stat().st_mtime)
            cli('aggregate', *common)
            consensus = json.loads((rdir / 'consensus.json').read_text())
            self.assertTrue(consensus['agree'] and consensus['core_agree'], consensus)
            self.assertEqual(consensus['members'], ['sol', 'codex', 'muse'], consensus)
            self.assertIn('sol', (rdir / 'report.md').read_text())
            invalid = json.loads(json.dumps(good))
            invalid['criteria'][0]['score'] = 6
            atomic_write(source, json.dumps(invalid))
            cli('collect', *common, '--member', 'sol', '--file', str(source), error='outside 1-5')
            self.assertEqual(State(rdir).d['members']['sol']['status'], 'failed')
            self.assertTrue((rdir / 'raw-sol-2.txt').exists())
            self.assertEqual(json.loads((rdir / 'out-sol.json').read_text()), good)
            for field, value in (('previous_status', 'invalid'), ('regressions', [3]), ('blocking', 1), ('unexpected', True)):
                atomic_write(source, json.dumps(dict(good, **{field: value})))
                cli('collect', *common, '--member', 'sol', '--file', str(source), error=field)
            saved_schema = json.loads(json.dumps(sch))
            saved_schema['properties']['summary']['enum'] = ['round-specific summary']
            atomic_write(rdir / 'schema.json', json.dumps(saved_schema))
            atomic_write(source, json.dumps(good))
            cli('collect', *common, '--member', 'sol', '--file', str(source), error='summary')
            external_errors = State(rdir).d['members']['sol']['errors']
            with patch.object(subprocess, 'run', return_value=subprocess.CompletedProcess(
                    [], 0, source.read_text(), '')), contextlib.redirect_stdout(io.StringIO()):
                run_member('muse', rdir, State(rdir), timeout=1, attempts=1, dry=False)
            self.assertEqual(State(rdir).d['members']['muse']['errors'], external_errors)
            atomic_write(rdir / 'schema.json', json.dumps(sch))
            atomic_write(source, 'not JSON')
            cli('collect', *common, '--member', 'sol', '--file', str(source), error='no JSON object in output')
            cli('collect', *common, '--member', 'unknown', '--file', str(source), error='invalid choice')
            cli('collect', *common, '--member', 'fable', '--file', str(source), error='not a member')
            missing = ('--run', 'missing', '--round', '1')
            cli('collect', *missing, '--member', 'sol', '--file', str(source), error='not prepared')
            cli('prompt-path', *missing, error='not prepared')
            self.assertFalse(round_dir('missing', 1).exists())
            atomic_write(source, json.dumps(good))
            for m in ('sol', 'muse'):
                cli('collect', *common, '--member', m, '--file', str(source))
                self.assertEqual(State(rdir).d['members'][m]['errors'], [])
