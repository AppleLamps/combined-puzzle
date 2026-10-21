"""Non-encrypted regression checks. Never import or execute puzzle-search modules.

AST extraction runs production plain-byte logic and run loops with deterministic
stubs for cipher/KDF/wallet calls. It does not validate encrypted runtime behavior.
"""
import ast
import collections
import importlib.util
import contextlib
import io
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import types
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]


def module(path):
    spec = importlib.util.spec_from_file_location(Path(path).stem, ROOT / path)
    out = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(out)
    return out


AUDIT = module('claude/riddle-method/audit_results.py')
ENCODING = module('tools/candidate_encoding.py')
ASSEMBLY = module('claude/common-flaw/assembly.py')


def functions(path, names, namespace):
    tree = ast.parse((ROOT / path).read_text(encoding='utf-8'))
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert len(nodes) == len(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), path, 'exec'), namespace)
    return namespace


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.judge = functions('claude/riddle-method/rt.py', ['judge'],
                               {'keyhit': lambda _: False})['judge']
        self.bodies = {p: random.Random(42 + p).randbytes(64 - p) for p in (1, 2)}

    def test_every_legal_padding_value(self):
        for block in (8, 16):
            for pad in range(1, block + 1):
                raw = b'Z' * (block - pad) + bytes([pad]) * pad
                self.assertEqual(AUDIT.valid_padding(raw, block), pad)

    def test_invalid_padding(self):
        for raw in (b'', b'X' * 16, b'X' * 15 + b'\x00', b'X' * 14 + b'\x03\x02', b'X'):
            self.assertEqual(AUDIT.valid_padding(raw), 0)

    def test_unranked_short_padding_and_empty_body(self):
        for pad, body in self.bodies.items():
            self.assertEqual(self.judge(body, pad), '')
        self.assertEqual(self.judge(b'', 16), '')
        self.assertEqual(self.judge(None, 0), '')

    def test_downstream_check_precedes_ranking(self):
        judge = functions('claude/riddle-method/rt.py', ['judge'],
                          {'keyhit': lambda _: True})['judge']
        self.assertEqual(judge(b'A' * 64, 1), 'KEYWINDOW')

    def test_bounded_records_and_overflow(self):
        records = AUDIT.AuditResults(limit=2)
        for i in range(5): records.append(('unranked', i))
        self.assertEqual(list(records), [('unranked', 0), ('unranked', 1)])
        self.assertEqual((records.total, records.omitted), (5, 3))
        with self.assertRaises(ValueError): AUDIT.AuditResults(-1)

    def test_python_overflow_exit_contract(self):
        for path in ('claude/riddle-method/rt.py', 'claude/independent-model/ct.py',
                     'claude/microstep/ms.py'):
            tree = ast.parse((ROOT / path).read_text())
            main = tree.body[-1]
            self.assertIsInstance(main, ast.If)
            exit_node = main.body[-1]
            for omitted in (0, 3):
                source = ('import sys, types\nfl=types.SimpleNamespace(omitted=%d)\n' % omitted
                          + ast.unparse(exit_node))
                result = subprocess.run([sys.executable, '-c', source], capture_output=True)
                self.assertEqual(result.returncode, 2 if omitted else 0)

    def test_explicit_encoding_roundtrip(self):
        for raw in (b'0x4142', b'ordinary text', b'\x00\t\xff', b''):
            self.assertEqual(ENCODING.decode_candidate('candhex=' + raw.hex()), raw)
        for field in ('cand=0x4142', 'cand=plain'):
            with self.assertRaises(ValueError): ENCODING.decode_candidate(field)

    def test_record_serialization_escapes_candidate(self):
        records = AUDIT.AuditResults()
        records.append(('benign\tline\n', b'\x00\xff'))
        output = io.StringIO()
        with contextlib.redirect_stdout(output): records.emit()
        lines = output.getvalue().splitlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(json.loads(lines[0].split('\t', 1)[1]),
                         ['benign\tline\n', {'hex': '00ff'}])

    def test_rt_loop_retains_pad1_and_pad2(self):
        for pad, body in self.bodies.items():
            ns = {'AuditResults': AUDIT.AuditResults, 'win': lambda _: False,
                  'forms': lambda _: [('fixture', b'benign')], 'LOCKED': {'fixture': b''},
                  'SOLVED': {}, 'dec': lambda *args: (pad, body), 'judge': self.judge}
            run = functions('claude/riddle-method/rt.py', ['run'], ns)['run']
            tests, pads, records = run(['benign'])
            self.assertEqual((tests, pads, len(records)), (2, 2, 2))
            self.assertEqual(records[0][3:], ('unranked', 'benign', pad, body.hex()))

    def test_ct_loop_retains_pad1_and_pad2(self):
        for pad, body in self.bodies.items():
            rt = types.SimpleNamespace(AuditResults=AUDIT.AuditResults, win=lambda _: False,
                                       judge=self.judge)
            ns = {'rt': rt, 'LOCKED': {'fixture': b'X' * 32}, 'KDFS': ['stub'],
                  'CIPHERS': {'stub': (None, 0, 0, 16)},
                  'forms': lambda _: [('fixture', b'benign')], 'derive': lambda *args: b'',
                  'tail_pad': lambda *args: pad, 'full': lambda *args: body}
            run = functions('claude/independent-model/ct.py', ['run'], ns)['run']
            tests, pads, records = run(['benign'])
            self.assertEqual((tests, pads, len(records)), (1, 1, 1))
            self.assertEqual(records[0][4:], ('unranked', 'benign', body, pad))

    def test_ms_loop_retains_pad1_and_pad2(self):
        for pad, body in self.bodies.items():
            rt = types.SimpleNamespace(AuditResults=AUDIT.AuditResults, win=lambda _: False,
                judge=self.judge, LOCKED={'fixture': b''}, SOLVED={}, dec=lambda *args: (pad, body))
            ns = {'rt': rt, 'SUFFIXES': {'stub': ''},
                  'forms': lambda _: [('fixture', b'benign')]}
            run = functions('claude/microstep/ms.py', ['run'], ns)['run']
            tests, pads, records = run(['benign'], {})
            self.assertEqual((tests, pads, len(records)), (2, 2, 2))
            self.assertEqual(records[0][3:], ('unranked', 'benign', pad, body.hex()))

    def test_assembly_exact_membership(self):
        matrix = ['M%02d|' % i for i in range(24)]
        last = ['L%d|' % i for i in range(6)]
        expected = set(matrix)
        for m in matrix:
            for l in last:
                expected.update((m+l, l+m, m+l+'thispassword', l+m+'thispassword'))
        self.assertEqual(ASSEMBLY.assemble(matrix, last), expected)
        self.assertEqual(len(expected), 600)
        self.assertEqual(ASSEMBLY.assemble(['x', 'x'], ['x']), {'x', 'xx', 'xxthispassword'})

    def test_checked_in_assembly_membership(self):
        # Importing gen performs plain matrix arithmetic only and writes no files.
        sys.path.insert(0, str(ROOT / 'claude/common-flaw'))
        gen = module('claude/common-flaw/gen.py')
        expected = set(gen.M) | {v for m in gen.M for l in gen.LW
                                for v in (m+l, l+m, m+l+'thispassword', l+m+'thispassword')}
        actual = {l for l in (ROOT / 'claude/common-flaw/cross.txt').read_text().splitlines()
                  if l and not l.startswith('#')}
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 600)

    def test_matched_plain_random_statistics(self):
        ns = functions('claude/rabbit-holes/leak.py', ['stats', 'verdict'],
                       {'collections': collections, 'math': math, 'zlib': zlib})
        a = random.Random(7).randbytes(80)
        self.assertEqual(ns['stats'](a), ns['stats'](random.Random(7).randbytes(80)))
        self.assertEqual(ns['stats'](b'Salted__' + b'12345678' + a), ns['stats'](a))
        self.assertEqual(ns['stats'](a)['n'], 80)
        source = (ROOT / 'claude/rabbit-holes/leak.py').read_text()
        self.assertIn("rnd.randbytes(observed['n'])", source)
        self.assertNotIn('os.urandom', source)

    def test_failed_checks_exit_nonzero(self):
        for success in (False, True):
            for file in ('verify.py', 'poster.py'):
                tree = ast.parse((ROOT / 'tools' / file).read_text())
                chk = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'chk')
                exit_node = tree.body[-1]
                ns_setup = ('import sys\nres=[]\n' if file == 'verify.py'
                            else 'import sys\nfailures=[]\n')
                prefix = ns_setup + ast.unparse(chk) + '\nchk("benign fixture", %r)\n' % success
                if file == 'verify.py': prefix += 'fails=[n for n,o in res if not o]\n'
                result = subprocess.run([sys.executable, '-c', prefix + ast.unparse(exit_node)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0 if success else 1)

    def test_python_source_syntax(self):
        for path in ROOT.rglob('*.py'):
            compile(path.read_text(encoding='utf-8'), str(path), 'exec')


if __name__ == '__main__':
    unittest.main()
