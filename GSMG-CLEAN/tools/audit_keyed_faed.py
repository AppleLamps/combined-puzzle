"""Move 4: DBBI-derived material as cipher keys over FAED. 14_CRITICAL_REVIEW_2026-09-14.md.

Moves 1-3 exhausted the prime structure as values, as masks, and the balanced pointer as a literal
answer and as a page-codec index. The remaining sourced but untested reading is 10 §7 / 14 §M5: the
SalPhaseIon labels name *transformations on the other field* — DBBI supplies key material, FAED is the
message. This run applies Vigenère and Beaufort (the puzzle's own demonstrated polyalphabetic cipher)
with every source-grounded key family to FAED, in both alphabets and both directions, and judges every
output against shuffle-key and shuffle-message controls plus the exact oracles. No envelope bytes read.

    python tools/audit_keyed_faed.py
"""
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / 'data', ROOT / 'runs/2026-09-14_keyed_faed'
OUT.mkdir(parents=True, exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda n: (DATA / n).read_text().strip()
dbbi, faed, arch = rd('DBBI_91.txt'), rd('FAED_570.txt'), rd('architect_letters_1539.txt')
colors = rd('poster_spiral_bits.txt').splitlines()[1]
isprime = lambda n: n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))
cells = []
def rec(at, slot, acc):
    if at == len(dbbi): cells.append(acc); return
    if isprime(slot):
        if dbbi[at] != 'b': return
        for tok in ('b', 'be'):
            if dbbi.startswith(tok, at): rec(at + len(tok), slot + 1, acc + [(slot, tok, True)])
    else: rec(at + 1, slot + 1, acc + [(slot, dbbi[at], False)])
rec(0, 1, [])
P84 = next(p for p in cells if len(p) == 84)
def cell_values(model, zero5=False):
    out = []
    for slot, tok, pr in P84:
        if pr:
            v = -slot if tok == 'b' else slot
            if model in ('unsigned', 'unsigned_zero5'): v = abs(v)
            if model in ('colour', 'colour_zero5'): v = 2 if tok == 'b' else 25
            if zero5 and slot == 5: v = 0
            out.append(v)
        else: out.append(ord(tok) - 96)
    return out
primes24 = [p for p in range(2, 100) if isprime(p)][:24]
PR = {c: [p for p, cc in zip(primes24, colors) if cc == c] for c in 'BY'}
KEYS = {}
for r, c in ((6, 14), (7, 12)):
    for m in ('signed', 'unsigned', 'colour'):
        v = cell_values(m)
        KEYS[f'sum_rows_{r}x{c}_{m}'] = [sum(v[i * c:(i + 1) * c]) for i in range(r)]
        KEYS[f'sum_cols_{r}x{c}_{m}'] = [sum(v[i * c:(i + 1) * c][j] for i in range(r)) for j in range(c)]
for nm, num in (('479', 479), ('484', 484), ('5', 5), ('963', 963), ('474', 474), ('489', 489)):
    KEYS[f'balanced_{nm}'] = [int(d) for d in str(num)]
KEYS['primes_all23'] = [slot for slot, tok, pr in P84 if pr]
KEYS['primes_be7'] = [slot for slot, tok, pr in P84 if pr and tok == 'be']
KEYS['primes_b16'] = [slot for slot, tok, pr in P84 if pr and tok == 'b']
for m in ('signed', 'unsigned', 'colour', 'signed_zero5', 'unsigned_zero5'):
    KEYS[f'cells84_{m}'] = cell_values(m, zero5=m.endswith('_zero5'))
KEYS['yellow9'] = PR['Y']; KEYS['blue15'] = PR['B']
KEYS['blue_minus5'] = [p for p in PR['B'] if p != 5]
order, seen, r0, c0, d = [], set(), 0, 0, 0
for _x in ('x',):
    dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))
for _ in range(196):
    order.append((r0, c0)); seen.add((r0, c0))
    nr, nc = r0 + dirs[d][0], c0 + dirs[d][1]
    if not (0 <= nr < 14 and 0 <= nc < 14) or (nr, nc) in seen:
        d = (d + 1) % 4; nr, nc = r0 + dirs[d][0], c0 + dirs[d][1]
    r0, c0 = nr, nc
bits = rd('poster_spiral_bits.txt').splitlines()[0]
g = {rc: int(bits[i]) for i, rc in enumerate(order)}
KEYS['poster_rows14'] = [sum(g[(r, c)] for c in range(14)) for r in range(14)]
KEYS['poster_cols14'] = [sum(g[(r, c)] for r in range(14)) for c in range(14)]
print(f'{len(KEYS)} key families')
C9 = [ord(ch) - 97 for ch in faed]
C26 = [ord(ch) - 97 for ch in faed]
def rep(key, n, m):
    k = [x % m for x in key]
    return (k * (1 + n // len(k)))[:n]
def vig_dec(C, K, m): return [(c - k) % m for c, k in zip(C, K)]
def vig_enc(C, K, m): return [(c + k) % m for c, k in zip(C, K)]
def beau(C, K, m): return [(k - c) % m for c, k in zip(C, K)]
for name, fn in (('vig_dec', vig_dec), ('vig_enc', vig_enc), ('beau', beau)):
    assert fn([4, 5], [1, 2], 26 if '26' not in name else 26) is not None
TRIGRAMS = ['the', 'and', 'ing', 'ion', 'ent', 'tio', 'for', 'her', 'ter', 'hat', 'tha', 'ere',
            'ate', 'his', 'con', 'res', 'ver', 'all', 'ons', 'nce', 'men', 'ith', 'ted', 'ers',
            'pro', 'thi', 'wit', 'are', 'ess', 'not', 'ive', 'was', 'ect', 'rea', 'com', 'eve']
def score(t):
    return sum(t.lower().count(x) for x in TRIGRAMS)
PRINT = set(range(32, 127)) | {9, 10, 13}
results = []
for kname, key in KEYS.items():
    for aname, C, m in (('A9', C9, 9), ('A26', C26, 26)):
        K = rep(key, len(C), m)
        for cname, fn in (('vig_dec', vig_dec), ('vig_enc', vig_enc), ('beau', beau)):
            V = fn(C, K, m)
            if aname == 'A9':
                letters = ''.join(chr(97 + v) for v in V)
                digits = ''.join(str(v + 1) for v in V)
                n = int(digits)
                b = n.to_bytes((n.bit_length() + 7) // 8, 'big')
                if all(x in PRINT for x in b) and len(b) >= 8:
                    results.append({'key': kname, 'cipher': cname, 'alphabet': 'A9+codec',
                                    'output': b.decode('latin1'), 'score': None})
            else:
                letters = ''.join(chr(97 + v) for v in V)
                results.append({'key': kname, 'cipher': cname, 'alphabet': 'A26',
                                'output': letters, 'score': score(letters)})
print(f'{len(results)} decoded outputs')

import random
rng = random.Random(20260914)
control_max, control_n = 0, 0
for _ in range(60):
    ks = [rng.randrange(26) for _ in range(rng.choice([2, 6, 7, 9, 12, 13, 14, 15, 23]))]
    K = rep(ks, len(C26), 26)
    for fn in (vig_dec, vig_enc, beau):
        d = ''.join(chr(97 + v) for v in fn(C26, K, 26))
        control_max = max(control_max, score(d)); control_n += 1
    ms = [rng.randrange(570) for _ in range(rng.choice([9, 15, 30]))]
    for d in (''.join(chr(97 + v) for v in beau(C26, rep(ms, len(C26), 26), 26)),):
        control_max = max(control_max, score(d)); control_n += 1
fixed = [3, 2, 19, 4, 18, 8, 24, 11, 23, 20, 25]
plant = ''.join(chr(97 + v) for v in vig_enc(C26, rep(fixed, len(C26), 26), 26))
recovered = ''.join(chr(97 + v) for v in vig_dec([ord(c) - 97 for c in plant], rep(fixed, len(C26), 26), 26))
plant_ok = recovered == faed
print(f'{control_n} shuffle controls, max {control_max}; planted round-trip: {plant_ok}')
top = sorted([r for r in results if r['score'] is not None], key=lambda x: -x['score'])[:10]
print(f'top letter outputs: {[ (t["key"], t["cipher"], t["score"], t["output"][:32]) for t in top ]}')
above = [r for r in results if r['score'] is not None and r['score'] > control_max]

B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58dec(s):
    n = 0
    for ch in s: n = n * 58 + B58.index(ch)
    raw = n.to_bytes(25, 'big')
    assert hashlib.sha256(hashlib.sha256(raw[:-4]).digest()).digest()[:4] == raw[-4:]
    return raw[1:21]
T = {a: b58dec(a).hex() for a in
     ['18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc', '1AD2wfwXukZ1kUAy848hTQQ72aSBZPB75r',
      '13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp', '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe',
      '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa']}
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
    if ''.join('0123456789abcdef'[first.setdefault(ch, len(first))] for ch in h) == DBBI_PATTERN:
        found.append('dbbi_pattern')
    if len(s) >= 8:
        sc = int(hashlib.sha256(s.encode()).hexdigest(), 16)
        if 1 <= sc < 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141:
            x, y = _mul(sc)
            for pub in (b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big'),
                        bytes([2 + (y & 1)]) + x.to_bytes(32, 'big')):
                hh = h160(pub)
                if hh in T: found.append(f'address {T[hh]}')
    if found:
        hits.append({**t, 'oracles': found})
print(f'exact oracles: {len(results)} outputs, {len(hits)} with a hit')
(OUT / 'manifest.json').write_text(json.dumps(
    {'date': '2026-09-14', 'review': '14_CRITICAL_REVIEW_2026-09-14.md move 4 (DBBI material as keys)',
     'envelope_bytes_read': 0, 'aes_decryptions': 0,
     'keys': list(KEYS), 'ciphers': ['vig_dec', 'vig_enc', 'beau'], 'alphabets': ['A9+codec', 'A26'],
     'controls': {'controls_drawn': control_n, 'control_max_score': control_max, 'planted_round_trip': plant_ok},
     'oracles': ['dbbi_pattern', 'marker_and_prize_addresses']}, indent=1) + '\n')
(OUT / 'results.json').write_text(json.dumps(
    {'outputs': len(results), 'controls_drawn': control_n, 'control_max_score': control_max,
     'above_control': above, 'oracle_hits': hits, 'top': top}, indent=1) + '\n')
(OUT / 'all_outputs.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in results))
print('WROTE', OUT)