"""Offline diagnostic: reproduce a false negative and recover discarded plaintexts."""
import contextlib
import io
import json
import sys
from collections import Counter
from pathlib import Path
from Crypto.Cipher import AES

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools'))
import check_candidate as cc

cc.selftest()
# A correct intermediate instruction can have pad=1 and contain no final key.
plain = b'Follow the white rabbit. Read the next instruction before trying another key.'
plain = plain.ljust(79, b' ')
assert len(plain) == 79
answer = 'synthetic control only'
salt = b'AUDIT001'
pw, md = cc.PROFILES['gsmg'](answer)
key, iv = cc.evp(pw, salt, md)
envelope = b'Salted__' + salt + AES.new(key, AES.MODE_CBC, iv).encrypt(plain + b'\x01')
assert cc.try_envelope(envelope, answer, 'gsmg') == (1, plain)
saved = cc.ENVELOPES
cc.ENVELOPES = {'synthetic_intermediate': envelope}
capture = io.StringIO()
with contextlib.redirect_stdout(capture):
    notable = cc.check(answer, 'gsmg', quiet=True)
cc.ENVELOPES = saved
assert notable is False and capture.getvalue() == ''

# Recover ALL padding-valid outputs from an existing bounded candidate set.
# No new guessing, key claims, or mutation of the previous run.
source = ROOT / 'runs/2026-09-13_last_words_referents/candidates.jsonl'
pads = Counter()
total = 0
recovered = []
with source.open(encoding='utf-8') as inp:
    for line in inp:
        row = json.loads(line)
        for profile in cc.PROFILES:
            for name, raw in cc.ENVELOPES.items():
                total += 1
                pad, pt = cc.try_envelope(raw, row['cand'], profile)
                pads[pad] += 1
                if not pad:
                    continue
                ascii_ratio = sum(b in (9, 10, 13) or 32 <= b <= 126 for b in pt) / len(pt)
                recovered.append(dict(candidate=row['cand'], source=row['src'], profile=profile,
                                      envelope=name, pad=pad, length=len(pt),
                                      ascii_ratio=ascii_ratio, plaintext_hex=pt.hex()))
with (HERE / 'all_padding_valid.jsonl').open('w', encoding='utf-8') as out:
    for row in recovered:
        out.write(json.dumps(row) + '\n')
summary = dict(synthetic_correct_decryption=True, synthetic_plaintext=plain.decode(),
               synthetic_notable=notable, synthetic_quiet_output=capture.getvalue(),
               trials=total, padding_histogram=dict(pads), recovered=len(recovered),
               max_ascii_ratio=max(r['ascii_ratio'] for r in recovered),
               ascii_over_90_percent=sum(r['ascii_ratio'] >= .9 for r in recovered),
               caveat='ASCII is descriptive only; every padding-valid plaintext is retained. '
                      'This does not exclude encoded or binary intermediate answers.')
(HERE / 'results.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
