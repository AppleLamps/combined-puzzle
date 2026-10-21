"""Read-only source verification; writes only a new context evidence directory."""
import base64
import hashlib
import json
import re
from pathlib import Path
import check_candidate as cc

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'runs/2026-09-13_envelope_context'
OUT.mkdir(exist_ok=True)
sha = lambda x: hashlib.sha256(x).hexdigest()
areas = lambda p: [re.sub(r'\s+', '', x) for x in re.findall(r'<textarea[^>]*>(.*?)</textarea>', p.read_text(encoding='utf-8'), re.S)]
page = areas(ROOT/'originals/pages/phase2_choice.html')
seven = json.loads((ROOT/'data/seven_part_phase3_answer.json').read_text())
records = []
for label, raw, answer, expected in [
    ('phase2', base64.b64decode(page[0]), 'causality', 'phase2_plaintext.bin'),
    ('phase3', base64.b64decode(page[1]), ''.join(seven), 'phase3_plaintext.bin'),
]:
    pad, pt = cc.try_envelope(raw, answer, 'gsmg')
    assert pad and pt == (ROOT/'data'/expected).read_bytes()
    records.append(dict(stage=label, padding=pad, plaintext_bytes=len(pt), plaintext_sha256=sha(pt)))
p3 = (ROOT/'data/phase3_plaintext.bin').read_bytes()
raw = base64.b64decode(p3[p3.index(b'U2FsdGVk'):])
pad, p32 = cc.try_envelope(raw, 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple', 'gsmg')
assert pad and p32 == (ROOT/'data/phase3_2_plaintext.bin').read_bytes()
records.append(dict(stage='phase3.2', padding=pad, plaintext_bytes=len(p32), plaintext_sha256=sha(p32)))
sal, cosmic = areas(ROOT/'originals/pages/salphaseion_phase3.html')
assert sal == (ROOT/'data/salphaseion_compact_1075.txt').read_text().strip()
derived = dict(terminal_phase3_2_end=base64.b64decode(p32[p32.index(b'U2FsdGVk'):]),
               salphaseion_short=base64.b64decode(sal[895:959]+sal[999:1063]),
               cosmic_duality=base64.b64decode(cosmic))
locked = {}
for name, raw in derived.items():
    assert raw == cc.ENVELOPES[name]
    c = len(raw)-16
    locked[name] = dict(raw_bytes=len(raw), ciphertext_bytes=c,
                        plaintext_range_pkcs7=[c-16, c-1], salt=raw[8:16].hex(), sha256=sha(raw))
def binary(s):
    b = s.translate(str.maketrans('ab','01'))
    return bytes(int(b[i:i+8],2) for i in range(0,len(b),8)).decode()
def decimal(s):
    n = int(s.translate(str.maketrans('abcdefghio','1234567890')))
    return n.to_bytes((n.bit_length()+7)//8,'big').decode()
labels = dict(matrixsumlist=binary(sal[91:195]), lastwords=decimal(sal[766:829]),
              thispassword=decimal(sal[830:859]), before_cipher=sal[860:895],
              enter=binary(sal[959:999]), after_cipher=sal[1063:1075])
assert labels['matrixsumlist']=='matrixsumlist' and labels['enter']=='enter'
messages = json.loads((ROOT/'telegram/ChatExport_2026-09-13_result.json').read_text(encoding='utf-8'))['messages']
ids = {1710,2910,2911,2918,5960,5963,5966,5969,6497,6508,6509,6512,6514,8000,8310,8311,8312,8315,
       8328,8329,8330,8446,8566,8567,8568,8569,9599,9603,9605,9607,11247,11248,33439,33445,39224,39233,39237}
selected = [m for m in messages if m['id'] in ids]
bits = re.sub(r'\s+','',next(m['text'] for m in selected if m['id']==8446))[::-1]
hint = bytes(int(bits[i:i+8],2) for i in range(0,len(bits),8)).decode()
assert hint.startswith('yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyang')
result = dict(known_envelopes=records, locked_envelopes=locked, source_labels=labels,
              creator_8446_decoded_exact=hint,
              format_lengths={name:dict(plaintext_bytes=n, ciphertext_bytes=16*(n//16+1),
                                       fits_short_envelope=16*(n//16+1)==80)
                              for name,n in [('raw_scalar',32),('uncompressed_wif',51),('compressed_wif',52),
                                             ('hex_scalar',64),('hex_scalar_lf',65),('hex_scalar_crlf',66),
                                             ('two_raw_scalars',64),('two_compressed_wifs',104),('other_short_envelope_raw',96)]})
(OUT/'verified_context.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
(OUT/'source_messages.json').write_text(json.dumps(selected,indent=2,ensure_ascii=True),encoding='utf-8')
print(json.dumps(result,indent=2))
