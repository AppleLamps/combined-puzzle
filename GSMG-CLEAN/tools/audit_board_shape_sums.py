"""Move 2: the board shape. 14_CRITICAL_REVIEW_2026-09-14.md M2 says the only sentence that
describes a board ("as wide as the first one seen") points at 14, and 84 = 6 x 14, while the
shipped lead uses 7 x 12 - the one shape that spells HILLFEXMGSGQ. This run puts the complete
84-cell DBBI parse under both shapes and the other board-like shapes, with the M4 zeroing
applied, through the folder's own sum-list -> decode families, and judges every output against
shuffled-input controls and the exact oracles. No envelope bytes are read.

    python tools/audit_board_shape_sums.py
"""
import hashlib, json, random, re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / 'data', ROOT / 'runs/2026-09-14_board_shape_sums'
OUT.mkdir(parents=True, exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda n: (DATA / n).read_text().strip()
dbbi, arch = rd('DBBI_91.txt'), rd('architect_letters_1539.txt')
colors = rd('poster_spiral_bits.txt').splitlines()[1]
isprime = lambda n: n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))
parses = []
def rec(at, slot, cells):
    if at == len(dbbi): parses.append(cells); return
    if isprime(slot):
        if dbbi[at] != 'b': return
        for tok in ('b', 'be'):
            if dbbi.startswith(tok, at): rec(at + len(tok), slot + 1, cells + [(slot, tok, True)])
    else: rec(at + 1, slot + 1, cells + [(slot, dbbi[at], False)])
rec(0, 1, [])
P84 = next(p for p in parses if len(p) == 84)
P83 = next(p for p in parses if len(p) == 83)
def values(cells, model, zero5=False):
    out = []
    for slot, tok, pr in cells:
        if pr:
            v = -slot if tok == 'b' else slot
            if model in ('unsigned', 'unsigned_zero5'): v = abs(v)
            if model in ('colour', 'colour_zero5'): v = 2 if tok == 'b' else 25
            if zero5 and slot == 5: v = 0
            out.append(v)
        else:
            out.append(0 if tok == 'b' and False else ord(tok) - 96)
    return out
MODELS = ['signed', 'unsigned', 'colour', 'signed_zero5', 'unsigned_zero5']
SHAPES = [(6, 14), (14, 6), (7, 12), (12, 7)]
def sumlists(v, r, c):
    rows = [sum(v[i * c + j] for j in range(c)) for i in range(r)]
    cols = [sum(v[i * c + j] for i in range(r)) for j in range(c)]
    out = {}
    for nm, L in (('rows', rows), ('cols', cols)):
        out[nm] = L; out[nm + '_rev'] = L[::-1]
        out[nm + '_cum'] = [sum(L[:i + 1]) for i in range(len(L))]
    out['rows_then_cols'] = rows + cols
    out['cols_then_rows'] = cols + rows
    return out
def decodes(nums):
    out = {}
    if nums and all(0 <= n % 26 < 26 for n in nums):
        out['mod26_A0'] = ''.join(chr(97 + n % 26) for n in nums)
        out['mod26_A1'] = ''.join(chr(96 + n % 26) if n % 26 else 'z' for n in nums)
    if all(1 <= n <= 26 for n in nums):
        out['a1z26'] = ''.join(chr(64 + n) for n in nums)
    if all(32 <= n <= 126 for n in nums):
        out['ascii'] = ''.join(chr(n) for n in nums)
    digits = ''.join(str(abs(n)) for n in nums)
    if all(ch in 'abcdefghio' for ch in digits) or all(ch in '0123456789' for ch in digits):
        t = digits.translate(str.maketrans('abcdefghio', '1234567890'))
        n = int(t)
        out['digits_to_bytes'] = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('latin1')
    for name, txt in (('arch_index0', arch), ):
        if all(0 <= n < len(txt) for n in nums):
            out[name] = ''.join(txt[n] for n in nums)
    return out
TRIGRAMS = ['the', 'and', 'ing', 'ion', 'ent', 'tio', 'for', 'her', 'ter', 'hat', 'tha', 'ere',
            'ate', 'his', 'con', 'res', 'ver', 'all', 'ons', 'nce', 'men', 'ith', 'ted', 'ers',
            'pro', 'thi', 'wit', 'are', 'ess', 'not', 'ive', 'was', 'ect', 'rea', 'com', 'eve']
def score(t):
    t = t.lower()
    return sum(t.count(g) for g in TRIGRAMS)

results, best = [], []
for cells, cname in ((P84, '84cell'), (P83, '83cell')):
    shapes = SHAPES if cname == '84cell' else [(1, len(cells))]
    for model in MODELS:
        v = values(cells, model, zero5=model.endswith('_zero5'))
        for r, c in shapes:
            if r * c != len(v): continue
            for lname, L in sumlists(v, r, c).items():
                for dname, d in decodes(L).items():
                    results.append({'parse': cname, 'model': model, 'shape': f'{r}x{c}',
                                    'sumlist': lname, 'decode': dname, 'output': d,
                                    'score': score(d) if dname not in ('digits_to_bytes',) else 0})
rng = random.Random(20260914)
control_max, control_n = 0, 0
for cells, cname in ((P84, '84cell'), (P83, '83cell')):
    for model in MODELS:
        base = values(cells, model, zero5=model.endswith('_zero5'))
        nrep = 40 if cname == '84cell' else 10
        for _ in range(nrep):
            s = base[:]; rng.shuffle(s)
            shapes = SHAPES if cname == '84cell' else [(1, len(s))]
            for r, c in shapes:
                if r * c != len(s): continue
                for lname, LL in sumlists(s, r, c).items():
                    for d in decodes(LL).values():
                        control_max = max(control_max, score(d)); control_n += 1
top = sorted(results, key=lambda x: -x['score'])[:8]
print(f'{len(results)} outputs; control max score {control_max} over 200 shuffles')
for t in top:
    flag = '  <-- ABOVE CONTROL' if t['score'] > control_max else ''
    print(f"  score {t['score']:3d}  {t['parse']} {t['model']} {t['shape']} {t['sumlist']} {t['decode']}"
          f"  {t['output'][:48]!r}{flag}")
above = [t for t in results if t['score'] > control_max]

# exact oracles on every decoded string (no AES)
MARKER = ['18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc', '1AD2wfwXukZ1kUAy848hTQQ72aSBZPB75r',
          '13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp', '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe',
          '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa']
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58dec(s):
    n = 0
    for ch in s: n = n * 58 + B58.index(ch)
    raw = n.to_bytes(25, 'big')
    assert hashlib.sha256(hashlib.sha256(raw[:-4]).digest()).digest()[:4] == raw[-4:]
    return raw[1:21]
T = {a: b58dec(a).hex() for a in MARKER}
def _add(a, b):
    if a is None: return b
    if b is None: return a
    if a[0] == b[0] and (a[1] + b[1]) % P == 0: return None
    s = (3 * a[0] * a[0] * pow(2 * a[1], -1, P) if a == b else (b[1] - a[1]) * pow(b[0] - a[0], -1, P)) % P
    x = (s * s - a[0] - b[0]) % P
    return x, (s * (a[0] - x) - a[1]) % P
P = 2**256 - 2**32 - 977
def _mul(k):
    r, c = None, (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
                  0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
    while k:
        if k & 1: r = _add(r, c)
        c = _add(c, c); k >>= 1
    return r
h160 = lambda b: hashlib.new('ripemd160', hashlib.sha256(b).digest()).hexdigest()
DBBI_PATTERN = '01234556728966286abc61c88b48de3086dd501d5557d6bab5605233df7bbb96'
hits = []
for t in results:
    s = t['output']
    h = sha(s.encode())
    found = []
    first = {}
    if ''.join('0123456789abcdef'[first.setdefault(ch, len(first))]
               for ch in h) == DBBI_PATTERN:
        found.append('dbbi_pattern')
    if len(s) >= 8:
        for form, sc in (('sha256', int(h, 16)),
                         ('sha256d', int(hashlib.sha256(hashlib.sha256(s.encode()).digest()).hexdigest(), 16))):
            if 1 <= sc < 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141:
                x, y = _mul(sc)
                for pub in (b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big'),
                            bytes([2 + (y & 1)]) + x.to_bytes(32, 'big')):
                    hh = h160(pub)
                    if hh in T: found.append(f'address {T[hh]} ({form})')
    if found:
        hits.append({**t, 'oracles': found})
print(f'exact oracles: {len(results)} outputs, {len(hits)} with a hit')
(OUT / 'manifest.json').write_text(json.dumps(
    {'date': '2026-09-14', 'review': '14_CRITICAL_REVIEW_2026-09-14.md move 2 (board shape)',
     'envelope_bytes_read': 0, 'aes_decryptions': 0, 'models': MODELS, 'shapes': [f'{r}x{c}' for r, c in SHAPES],
     'parses': ['84cell', '83cell'], 'controls': {'controls_drawn': control_n, 'control_max_score': control_max},
     'oracles': ['dbbi_pattern', 'marker_and_prize_addresses']}, indent=1) + '\n')
(OUT / 'results.json').write_text(json.dumps(
    {'outputs': len(results), 'controls_drawn': control_n, 'control_max_score': control_max,
     'above_control': above, 'oracle_hits': hits, 'top': top}, indent=1) + '\n')
(OUT / 'all_outputs.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in results))
print('WROTE', OUT)