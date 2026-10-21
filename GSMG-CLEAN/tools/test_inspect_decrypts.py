"""Planted controls for multi-format inspection, independent of puzzle guesses."""
import base64
import gzip
import unittest
import tempfile
import sys
import json
from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO
from Crypto.Cipher import AES
import inspect_decrypts as ins

class InspectionTests(unittest.TestCase):
    def signals(self, raw, **kw):
        return [s for n in ins.inspect(raw, keys=False, **kw)['nodes'] for s in n['signals']]

    def test_pad_one_instruction(self):
        plain = b'Read the next instruction before trying another key.'.ljust(79, b' ')
        self.assertIn('text heuristic: utf-8-sig', self.signals(plain))

    def test_text_encodings(self):
        for encoding in ('utf-8', 'utf-16-le', 'utf-16-be', 'utf-32-le', 'utf-32-be', 'cp037', 'cp273'):
            with self.subTest(encoding=encoding):
                signals = self.signals('Follow the white rabbit and read the next page.'.encode(encoding))
                self.assertTrue(any(s.startswith('text heuristic:') for s in signals))

    def test_nested_compressed(self):
        plain = b'{"instruction":"Follow the white rabbit"}'
        raw = base64.b64encode(gzip.compress(plain))
        result = ins.inspect(raw, keys=False)
        self.assertTrue(any(n['plaintext_hex'] == plain.hex() for n in result['nodes']))
        self.assertIn('JSON container parsed', self.signals(raw))

    def test_puzzle_encodings(self):
        plain = b'lastwordsbeforearchichoice'
        decimal = str(int.from_bytes(plain, 'big'))
        encoded = decimal.translate(str.maketrans('1234567890', 'abcdefghio')).encode()
        binary = ''.join(f'{b:08b}' for b in plain).translate(str.maketrans('01', 'ab')).encode()
        for raw in (encoded, binary, plain.hex().encode()):
            with self.subTest(raw=raw):
                result = ins.inspect(raw, keys=False)
                self.assertTrue(any(n['plaintext_hex'] == plain.hex() for n in result['nodes']))

    def test_compression_limit_and_invalid(self):
        result = ins.inspect(gzip.compress(b'A' * (ins.MAX_BYTES + 1)), keys=False)
        self.assertTrue(result['limits'])
        self.assertIn('gzip: invalid', self.signals(b'\x1f\x8bgarbage'))

    def test_unknown_bytes_retained(self):
        raw = bytes(range(256))
        result = ins.inspect(raw, keys=False)
        self.assertEqual(result['nodes'][0]['plaintext_hex'], raw.hex())
        self.assertFalse(result['nodes'][0]['key_matches'])
        self.assertEqual(result['assessment'], 'UNRESOLVED_RETAINED')

    def test_incomplete_compression_retains_partial_output(self):
        plain = b'Read the next instruction before guessing again.'
        truncated = gzip.compress(plain)[:-8]
        result = ins.inspect(truncated, keys=False)
        self.assertTrue(result['limits'])
        self.assertTrue(any(n['plaintext_hex'] == plain.hex() for n in result['nodes']))
        self.assertEqual(result['assessment'], 'UNRESOLVED_RETAINED')

    def test_nested_envelope(self):
        raw = b'Salted__12345678' + bytes(range(16))
        self.assertTrue(any('OpenSSL envelope' in s for s in self.signals(base64.b64encode(raw))))

    def test_live_journal_keeps_pad_one(self):
        plain = b'Follow the white rabbit and read the next instruction.'.ljust(79, b' ')
        salt = b'TEST0001'
        pw, md = ins.cc.PROFILES['gsmg']('correct')
        key, iv = ins.cc.evp(pw, salt, md)
        raw = b'Salted__' + salt + AES.new(key, AES.MODE_CBC, iv).encrypt(plain + b'\x01')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'candidates.txt').write_text('correct\n', encoding='utf-8')
            argv = ['inspect', '--file', str(root / 'candidates.txt'), '--out', str(root / 'out'), '--no-key-check']
            with patch.object(sys, 'argv', argv), patch.object(ins.cc, 'ENVELOPES', {'test': raw}), redirect_stdout(StringIO()):
                ins.main()
            row = json.loads((root / 'out/all_results.jsonl').read_text())
            self.assertEqual(row['source']['pad'], 1)
            self.assertEqual(bytes.fromhex(row['source']['plaintext_hex']), plain)
            self.assertTrue(row['inspection']['nodes'][0]['signals'])

    def test_confirmed_key_formats(self):
        target = '91b24bf9f5288532960ac687abb035127b1d28a5'
        ins.cc.TARGETS[target] = 'TEST k=1'
        try:
            ins.enable_fast_keys()
            raw = ('0' * 63 + '1').encode('utf-16-le')
            result = ins.inspect(raw)
            self.assertTrue(any('utf-16-le-to-utf8' in n['path'] and n['key_matches'] for n in result['nodes']))
            raw = (1).to_bytes(32, 'little')
            result = ins.inspect(raw)
            self.assertTrue(any('little' in desc for n in result['nodes'] for desc, hits in n['key_matches']))
        finally:
            del ins.cc.TARGETS[target]

if __name__ == '__main__':
    unittest.main()
