"""Cheap offline checks; never execute any search entry point.
Run: python -m unittest discover -s tests -v
Requires the existing pycryptodome/coincurve runtime for structural imports.
"""
import base64
from collections import Counter
from contextlib import redirect_stdout
import hashlib
import importlib
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'review_leads'))
from mywork.candidate_pool import build_texts, build_pool, prose_sections, DERIVED_NAMES

CRLF_HASHES = (
    'e2f9dd65604a3231f8b3301724e8d713a88fffc4b6c7c4aeeb20f58a582b593a',
    'c4ad94559a44a927c1032cc0e024515f9510a0806a2d14458dbf4a360af9865f',
    'b82afeb86f9e50848220f9b64b744b821400308aea273a1c949b9d2d0e408a34',
)
CONTAINER_HASHES = dict(zip(
    ('phase2','phase3','phase3.2','terminal','salphaseion-short','cosmic-duality'),
    ('a089144531c666e59770c799427c05d1ea4ae074857b97d61b8d3924ff14c7e7',
     '9163a38d8c49038d01005bc468d9c677183b49b14d7a88fdf3bade75d1443f30',
     '9d172dc017034564b40eb381fa61e31421f509a08430864c77ccf86cfc8fe784',
     '291dfd6f3e759ec2e272b35a00c24907da70c3e7a9291b4c13605c7b0b4f3de9',
     '9e2831e1b34b5f34796df47ccaf6530d48d371c61a6bff84d60db1064fa7a258',
     'b18950551a4dd0cb8a9378f0906ba18c03a15f0ee83eb98c6bc90165c5f79805')))


def representations():
    lf = {n: (ROOT / 'derived' / n).read_bytes().replace(b'\r\n', b'\n') for n in DERIVED_NAMES}
    return lf, {n: b.replace(b'\n', b'\r\n') for n, b in lf.items()}


def legacy_texts(data):
    """The three slices from 7a2dbfbc, without its executable search loop."""
    texts = build_texts(ROOT, data)
    texts[2] = data[DERIVED_NAMES[0]].decode('latin-1')
    texts[3] = data[DERIVED_NAMES[1]][:726].decode('latin-1')
    texts[4] = data[DERIVED_NAMES[2]][:447].decode('latin-1')
    texts[5] = data[DERIVED_NAMES[2]][2143:2292].decode('latin-1')
    return texts


def pool_fingerprint(pool):
    return hashlib.sha256(json.dumps(sorted(pool), ensure_ascii=True, separators=(',', ':')).encode()).hexdigest()


def pool_comparison():
    lf, crlf = representations()
    fixed = build_pool(ROOT, build_texts(ROOT, lf))
    old_lf = build_pool(ROOT, legacy_texts(lf))
    old_crlf = build_pool(ROOT, legacy_texts(crlf))
    return dict(fixed_count=len(fixed), legacy_lf_count=len(old_lf),
                legacy_crlf_count=len(old_crlf),
                fixed_equals_legacy_crlf=fixed == old_crlf,
                added_vs_legacy_lf=len(fixed-old_lf), removed_vs_legacy_lf=len(old_lf-fixed),
                fixed_sha256=pool_fingerprint(fixed), legacy_lf_sha256=pool_fingerprint(old_lf),
                fingerprint_format='SHA256 of UTF-8 compact JSON of sorted candidate strings')


def saved_pushes(script_hex):
    """Strict decoder for the push-only tails in these saved OP_RETURN scripts."""
    raw = bytes.fromhex(script_hex)
    if raw[:2] != bytes.fromhex('006a'):
        raise ValueError('Expected OP_FALSE OP_RETURN')
    chunks = []
    at = 2
    while at < len(raw):
        size = raw[at]
        at += 1
        if size == 76:
            if at == len(raw): raise ValueError('Missing PUSHDATA1 length')
            size = raw[at]
            at += 1
        elif size > 75:
            raise ValueError('Unexpected opcode')
        if at + size > len(raw): raise ValueError('Truncated push')
        chunks.append(raw[at:at+size])
        at += size
    return chunks


class ReviewRegressions(unittest.TestCase):
    def test_derived_representations(self):
        lf, crlf = representations()
        self.assertEqual([len(lf[n]) for n in DERIVED_NAMES], [642, 4032, 2411])
        self.assertEqual([len(crlf[n]) for n in DERIVED_NAMES], [648, 4090, 2422])
        self.assertEqual(tuple(hashlib.sha256(crlf[n]).hexdigest() for n in DERIVED_NAMES), CRLF_HASHES)

    def test_precise_prose_boundaries(self):
        lf, crlf = representations()
        expected = tuple(b.decode('ascii').replace('\r\n', '\n') for b in (
            crlf[DERIVED_NAMES[1]][:726], crlf[DERIVED_NAMES[2]][:447], crlf[DERIVED_NAMES[2]][2143:2292]))
        for data in (lf, crlf):
            actual = prose_sections(data[DERIVED_NAMES[1]], data[DERIVED_NAMES[2]])
            self.assertEqual(actual, expected)
            self.assertTrue(actual[2].startswith('Raising the stakes '))
            self.assertTrue(actual[2].endswith('as the first one seen.\n\n'))
            self.assertNotIn('U2FsdGVkX1', ''.join(actual))
        self.assertFalse(legacy_texts(lf)[5].startswith('Raising '))
        self.assertIn('U2FsdGVkX1', legacy_texts(lf)[5])

    def test_changed_boundaries_fail_closed(self):
        lf, _ = representations()
        p3, p32 = lf[DERIVED_NAMES[1]], lf[DERIVED_NAMES[2]]
        for bad in (p32.replace(b'Raising ', b'Changed '), p32+b'\n\nextra', p32.replace(b'\n\n', b'\n', 1)):
            with self.assertRaises(ValueError): prose_sections(p3, bad)
        with self.assertRaises(ValueError): prose_sections(p3.replace(b'U2FsdGVkX1', b'broken'), p32)

    def test_lf_crlf_candidate_equivalence(self):
        lf, crlf = representations()
        self.assertEqual(build_pool(ROOT, build_texts(ROOT, lf)), build_pool(ROOT, build_texts(ROOT, crlf)))
        comparison = pool_comparison()
        self.assertEqual(comparison, json.loads((ROOT/'review_leads/evidence/pool_comparison.json').read_text()))
        self.assertTrue(comparison['fixed_equals_legacy_crlf'])
        self.assertGreater(comparison['removed_vs_legacy_lf'], 0)
        self.assertGreater(comparison['added_vs_legacy_lf'], 0)

    def test_encrypted_artifacts(self):
        for name, expected in CONTAINER_HASHES.items():
            raw = base64.b64decode((ROOT/'files'/f'{name}.b64').read_bytes())
            self.assertEqual(hashlib.sha256(raw).hexdigest(), expected)

    def test_import_and_binary_constructor_do_not_search(self):
        with patch('Crypto.Cipher.AES.new', side_effect=AssertionError('No AES trials allowed')):
            out = io.StringIO()
            with redirect_stdout(out):
                importlib.import_module('mywork.pool_search')
                binary = importlib.import_module('binary_envelopes')
                candidates = binary.old_candidates()
                self.assertEqual(next(candidates), len(build_pool()))
                label, value = next(candidates)
                self.assertIn('answer', label)
                self.assertIsInstance(value, bytes)
            self.assertEqual(out.getvalue(), '')

    def test_fixed_board_32_cases(self):
        from next_tests import columnar, board, S
        saved = json.loads((ROOT/'review_leads/transpose-inspection.json').read_text())['cases_detail']
        cases = []
        for name, text in [('r1', S[:91]), ('r2', S[195:765])]:
            for reverse in (False, True):
                for key in ('matrixsumlist','thematrixhasyou','lastwordsbeforearchichoice','fubcdoraclethingkymvps'):
                    for inverse in (False, True):
                        digits = columnar(text[::-1] if reverse else text, key, inverse).translate(str.maketrans('abcdefghi','123456789'))
                        cases.append(dict(run=name, reverse=reverse, key=key, inverse=inverse, digits=digits, decoded=board(digits)))
        self.assertEqual(cases, saved)
        self.assertEqual(sum(row['decoded'] is not None for row in cases), 29)
        self.assertEqual(len(cases), 32)
        for row in cases:
            if row['run'] == 'r1' and row['decoded'] is not None:
                self.assertGreaterEqual(row['decoded'].count('U'), 18)
                self.assertLessEqual(sum(row['decoded'].count(c) for c in 'LETHINGKY'), 3)
                self.assertGreaterEqual(len(row['decoded']), 84)

    def test_transposition_invariant_counts(self):
        from next_tests import S
        c = Counter(S[:91])
        self.assertEqual(c, dict(zip('abcdefghi', [3,25,8,4,18,10,10,8,5])))
        # In every permutation only a/d (digits 1/4) can start two-digit tokens.
        prefixes = c['a'] + c['d']
        self.assertEqual(c['b']-prefixes, 18)
        self.assertEqual(c['a'], 3)
        self.assertEqual(sum(c.values())-prefixes, 84)

    def test_known_phrase_character_and_decimal_lengths(self):
        phrase = 'lastwordsbeforearchichoice'
        self.assertEqual(len(phrase), 26)
        self.assertEqual(len(str(int.from_bytes(phrase.encode('ascii'), 'big'))), 63)

    def test_protocol_integer_conversions_and_amounts(self):
        self.assertEqual((9325).to_bytes(2, 'little').hex(), '6d24')
        self.assertEqual((1133).to_bytes(2, 'little').hex(), '6d04')
        self.assertEqual((5262419).to_bytes(3, 'little'), b'SLP')
        self.assertEqual((1145980243).to_bytes(4, 'little'), b'SEND')
        self.assertEqual(150_000_000 / 100_000_000, 1.5)
        self.assertEqual(sum([100000000,150000000,102700000,299798400,1258124,185716800,26417400]), 865890724)

    def test_public_checkpoint_local_record(self):
        from coincurve import PrivateKey
        target = b'1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
        public = PrivateKey(hashlib.sha256(target).digest()).public_key.format(compressed=True)
        h160 = hashlib.new('ripemd160', hashlib.sha256(public).digest()).hexdigest()
        self.assertEqual(h160, 'af36f3055e2e5e12cf77da10beb981d2201dd1e4')
        tx = json.loads((ROOT/'mywork2/web/gsmg_txs.json').read_text())[25]
        self.assertEqual(tx['txid'], '3891dd146dce36ed7f97e5476aa3cd427ebc9a8535ce6353b72309b28e686ced')
        self.assertEqual(tx['vout'][1]['scriptpubkey_address'], '1GyT5WrLYpwFkuiVoPDJZa1Q6jtjbjuBff')
        self.assertEqual(tx['vout'][1]['scriptpubkey'], '76a914'+h160+'88ac')
        self.assertEqual(tx['vout'][1]['value'], 1000)
        self.assertEqual(bytes.fromhex(tx['vout'][0]['scriptpubkey'])[2:], b'GSMG.io: do you beleive me you need it?')

    def test_saved_bsv_record_hashes_and_blob(self):
        evidence = ROOT / 'review_leads/evidence'
        manifest = json.loads((evidence/'bsv_manifest.json').read_text())
        by_id = {}
        for row in manifest['records']:
            raw = (evidence/row['file']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'])
            tx = json.loads(raw)
            self.assertEqual(tx['txid'], row['txid'])
            by_id[tx['txid'][:8]] = tx
        tx = by_id['bc7d915b']
        tag, target, blob = saved_pushes(tx['vout'][0]['scriptPubKey']['hex'])
        self.assertEqual(tag, bytes.fromhex('6d24'))
        self.assertEqual(target.hex(), 'a9553269572a317e39f0f518cb87c1a0ee1dbae4')
        text = blob.decode('utf-8')
        self.assertEqual((len(blob), len(text), len(set(text))), (192, 83, 24))
        self.assertFalse(any(c.isspace() for c in text))
        self.assertEqual(hashlib.sha256(blob).hexdigest(), '0fc9fef5cb79891c52feae29c2b13b1f010070c18bad696e84cb3146fea0ed0d')
        self.assertEqual(saved_pushes(by_id['44d8935d']['vout'][0]['scriptPubKey']['hex'])[0].hex(), '6d04')
        token = saved_pushes(by_id['816fccdb']['vout'][0]['scriptPubKey']['hex'])
        self.assertEqual(token[:3], [b'SLP\0', b'\x01', b'SEND'])
        genesis = saved_pushes(by_id['9d56a8be']['vout'][0]['scriptPubKey']['hex'])
        self.assertEqual(genesis[:3], [b'SLP\0', b'\x01', b'GENESIS'])

    def test_saved_memo_push_layouts(self):
        evidence = ROOT/'review_leads/evidence'
        records = {p.stem[4:12]: json.loads(p.read_bytes()) for p in evidence.glob('bsv_*.json') if p.name != 'bsv_manifest.json'}
        expected_messages = {
            '7ea6eb76': b'100,000,000 satoshis (100,000,000 BSV)',
            'b7611598': b'THEMATRIXHASYOU',
        }
        for prefix in ('bc7d915b', '7ea6eb76', 'b7611598'):
            script = records[prefix]['vout'][0]['scriptPubKey']['hex']
            pushes = saved_pushes(script)
            self.assertEqual(len(pushes), 3)
            self.assertEqual(pushes[0], bytes.fromhex('6d24'))
            self.assertEqual(len(pushes[1]), 20)
            self.assertLessEqual(len(pushes[2]), 194)
            # Round-trip the entire script, including minimal push opcodes.
            encoded = bytes.fromhex('006a') + b''.join(
                (bytes([len(b)]) if len(b) <= 75 else bytes([76, len(b)])) + b
                for b in pushes)
            self.assertEqual(encoded.hex(), script)
            self.assertEqual(pushes[1].hex(),
                '87640c4ea9deee16b2abf6294ee4228340b9e407' if prefix == 'b7611598'
                else 'a9553269572a317e39f0f518cb87c1a0ee1dbae4')
            if prefix in expected_messages:
                self.assertEqual(pushes[2], expected_messages[prefix])
        script = records['44d8935d']['vout'][0]['scriptPubKey']['hex']
        self.assertEqual(saved_pushes(script), [bytes.fromhex('6d04'), bytes.fromhex(
            '0004938e4a0b7a488cc9248ea09d67e9f6afe51c3b8f486bb6c3e26f5c5a1dfc')])
        self.assertEqual(script, '006a026d04200004938e4a0b7a488cc9248ea09d67e9f6afe51c3b8f486bb6c3e26f5c5a1dfc')

    def test_saved_checkpoint_prevout_and_change(self):
        evidence = ROOT/'review_leads/evidence'
        payment = json.loads(next(evidence.glob('bsv_7ea6*.json')).read_text())
        parent = json.loads(next(evidence.glob('bsv_b761*.json')).read_text())
        self.assertEqual(len(payment['vin']), 1)
        self.assertEqual(payment['vin'][0]['txid'], parent['txid'])
        self.assertEqual(payment['vin'][0]['vout'], 2)
        expected = '76a914af36f3055e2e5e12cf77da10beb981d2201dd1e488ac'
        for tx in (parent, payment):
            output = tx['vout'][2]['scriptPubKey']
            self.assertEqual(output['hex'], expected)
            self.assertEqual(output['addresses'], ['1GyT5WrLYpwFkuiVoPDJZa1Q6jtjbjuBff'])
        self.assertEqual(payment['vout'][1]['value'], 1)

    def test_creator_selection_counts(self):
        evidence = json.loads((ROOT/'review_leads/evidence/creator_selection_ids.json').read_text())
        ids = evidence['message_ids']
        self.assertEqual(len(ids), len(set(ids)))
        export = json.loads((ROOT/'ChatExport_2026-10-08/result.json').read_text(encoding='utf-8'))
        selected = [m for m in export['messages'] if m['id'] in set(ids)]
        self.assertEqual(len(selected), 819)
        self.assertEqual(sum(m.get('from') == 'Jrk Bgrt' and not m.get('forwarded_from') for m in selected), 492)
        self.assertEqual(sum(m.get('forwarded_from') == 'Jrk Bgrt' for m in selected), 327)


if __name__ == '__main__':
    unittest.main()
