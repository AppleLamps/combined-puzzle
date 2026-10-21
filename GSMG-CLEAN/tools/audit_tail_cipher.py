"""Move 5: the 64-letter DBBI-VIC tail as a standalone cipher object.

14_CRITICAL_REVIEW_2026-09-14.md left the tail (64 letters, 24 distinct, named VIC at 1/4/21 and
YOUWON at 22-27) as the one other self-checking artifact never attacked as a text. This run profiles
it (index of coincidence, frequency shape), solves it as a monoalphabetic substitution with a
hill-climber judged against shuffled-tail controls, and puts it through Vigenere/Beaufort (balanced
keys) and rail/columnar transpositions, all judged the same way, plus the exact oracles.
No envelope bytes are read.

    python tools/audit_tail_cipher.py
"""
import hashlib, json, random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / 'data', ROOT / 'runs/2026-09-14_tail_cipher'
OUT.mkdir(parents=True, exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda n: (DATA / n).read_text().strip()
diff = rd('dbbi_minus_vic_91.txt')
tail = diff[27:]
ALPH = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
TRIGRAMS = ['the', 'and', 'ing', 'ion', 'ent', 'tio', 'for', 'her', 'ter', 'hat', 'tha', 'ere',
            'ate', 'his', 'con', 'res', 'ver', 'all', 'ons', 'nce', 'men', 'ith', 'ted', 'ers',
            'pro', 'thi', 'wit', 'are', 'ess', 'not', 'ive', 'was', 'ect', 'rea', 'com', 'eve']
def score(t):
    return sum(t.lower().count(g) for g in TRIGRAMS)
from collections import Counter
def ioc(s):
    n = len(s)
    c = Counter(s)
    return sum(v * (v - 1) for v in c.values()) / (n * (n - 1))
profile = {'tail': tail, 'length': len(tail), 'distinct': len(set(tail)),
           'counts': dict(Counter(tail)), 'ioc': round(ioc(tail), 4),
           'ioc_diff91': round(ioc(diff), 4), 'english_ioc': 0.065, 'flat26_ioc': round(1 / 26, 4),
           'flat24_ioc': round(1 / 24, 4)}
print('PROFILE', json.dumps({k: v for k, v in profile.items() if k != 'counts'}))
def climb(ct, restarts=60, iters=400, seed=7):
    rng = random.Random(seed)
    best_key, best_sc = None, -1
    for _ in range(restarts):
        key = list(ALPH); rng.shuffle(key)
        tab = str.maketrans(''.join(key), ALPH)
        cur = score(ct.translate(tab))
        for _ in range(iters):
            a, b = rng.randrange(26), rng.randrange(26)
            key[a], key[b] = key[b], key[a]
            tab = str.maketrans(''.join(key), ALPH)
            sc = score(ct.translate(tab))
            if sc >= cur: cur = sc
            else: key[a], key[b] = key[b], key[a]
        if cur > best_sc:
            best_sc, best_key = cur, ''.join(key)
    tab = str.maketrans(best_key, ALPH)
    return best_key, best_sc, ct.translate(tab)
TARGETS = {'tail64': tail, 'diff91': diff, 'youwon_tail71': diff[21:]}
solves, controls = {}, {}
for tname, ct in TARGETS.items():
    k, sc, pt = climb(ct)
    solves[tname] = {'key': k, 'score': sc, 'plaintext': pt}
    cs = []
    for j in range(30):
        sh = list(ct); random.Random(1000 + j).shuffle(sh)
        _, s2, _ = climb(''.join(sh), restarts=20, iters=150, seed=2000 + j)
        cs.append(s2)
    controls[tname] = {'n': 30, 'max': max(cs), 'scores': cs,
                       'real_above': sc > max(cs)}
print('SUBSTITUTION', json.dumps({t: {'score': v['score'], 'above': controls[t]['real_above'],
                                      'control_max': controls[t]['max'], 'text': v['plaintext'][:64]}
                                  for t, v in solves.items()}, indent=1))

# ---- keyed polyalphabetic / transposition layer (bounded, sourced forms) ----------------
arch = rd('architect_letters_1539.txt')
transcript = (ROOT / 'reference_texts/matrix_reloaded_architect_scene_transcript.txt'
              ).read_text(encoding='utf-8').upper()
letters_only = lambda s: ''.join(ch for ch in s if ch in ALPH)
A1Z = lambda ch: ALPH.index(ch)
def vig_dec(C, K): return ''.join(ALPH[(A1Z(c) - A1Z(K[i % len(K)])) % 26] for i, c in enumerate(C))
def vig_enc(C, K): return ''.join(ALPH[(A1Z(c) + A1Z(K[i % len(K)])) % 26] for i, c in enumerate(C))
def beau(C, K): return ''.join(ALPH[(A1Z(K[i % len(K)]) - A1Z(c)) % 26] for i, c in enumerate(C))
def rails(s, n):
    out, used = [''] * n, [False] * len(s)
    cyc = list(range(n)) + list(range(n - 2, 0, -1))
    for i, ch in enumerate(s): out[cyc[i % len(cyc)]] += ch
    return ''.join(out)
def rail_dec(s, n):
    cyc = list(range(n)) + list(range(n - 2, 0, -1))
    lens = [0] * n
    for i in range(len(s)): lens[cyc[i % len(cyc)]] += 1
    parts, p = [], 0
    for L in lens: parts.append(s[p:p + L]); p += L
    pos = [0] * n
    out = []
    for i in range(len(s)):
        r = cyc[i % len(cyc)]; out.append(parts[r][pos[r]]); pos[r] += 1
    return ''.join(out)
def col_dec(s, cols, order):
    rows = (len(s) + cols - 1) // cols
    grid = [[''] * cols for _ in range(rows)]
    k = 0
    for c in order:
        for r in range(rows):
            if k < len(s) and not (r == rows - 1 and (r * cols + c) >= len(s)):
                grid[r][c] = s[k]; k += 1
    return ''.join(''.join(row) for row in grid)
KEYS = {}
for m in ('479', '484', '5', '963', '474', '489'):
    KEYS[f'num_{m}'] = ''.join(ALPH[int(d) % 26] for d in m)
for ln, txt in (('arch1539', arch), ('transcript', letters_only(transcript))):
    KEYS[f'{ln}_head'] = txt[:64]
    KEYS[f'{ln}_at479'] = txt[479:479 + 64]
    KEYS[f'{ln}_at484'] = txt[484:484 + 64]
KEYS['arch_at479_sent'] = arch[479:479 + 64]
layered = []
for tname, ct in TARGETS.items():
    for kname, K in KEYS.items():
        K = K or 'A'
        for cname, fn in (('vig_dec', vig_dec), ('vig_enc', vig_enc), ('beau', beau)):
            pt = fn(ct, K)
            layered.append({'target': tname, 'key': kname, 'cipher': cname, 'output': pt, 'score': score(pt)})
    for n in (2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 16):
        layered.append({'target': tname, 'key': f'rails_{n}', 'cipher': 'rail_dec',
                        'output': rail_dec(ct, n), 'score': score(rail_dec(ct, n))})
    for cols in (2, 3, 4, 5, 6, 7, 8, 10, 13, 16, 32):
        if len(ct) % cols: continue
        lo = list(range(cols)); hi = lo[::-1]
        for oname, o in (('identity', lo), ('reversed', hi)):
            co = col_dec(ct, cols, o)
            layered.append({'target': tname, 'key': f'col{cols}_{oname}', 'cipher': 'col_dec',
                            'output': co, 'score': score(co)})
print(f'{len(layered)} layered outputs')
ctl_max, ctl_n = 0, 0
rng = random.Random(20260914)
for _ in range(60):
    ct = ''.join(rng.choice(ALPH) for _ in range(64))
    best = 0
    for fn in (vig_dec, vig_enc, beau):
        K = ''.join(rng.choice(ALPH) for _ in range(rng.choice([3, 5, 8, 13])))
        best = max(best, score(fn(ct, K)))
    best = max(best, score(rail_dec(ct, rng.choice([3, 4, 5, 6, 7, 8]))))
    ctl_max = max(ctl_max, best); ctl_n += 1
print(f'layered controls: {ctl_n}, max {ctl_max}')
top = sorted(layered, key=lambda x: -x['score'])[:10]
for t in top:
    print(f"  score {t['score']:3d}  {t['target']} {t['key']} {t['cipher']}  {t['output'][:48]!r}"
          f"{'  <-- ABOVE CONTROL' if t['score'] > ctl_max else ''}")
above = [t for t in layered if t['score'] > ctl_max]
plant = vig_enc('THEPRIVATEKEYSAREHEREINTHECIPHER', 'PRIVATEKEY')
plant_back = vig_dec(plant, 'PRIVATEKEY')
plant_ok = plant_back == 'THEPRIVATEKEYSAREHEREINTHECIPHER'
print(f'planted round-trip: {plant_ok}')

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
def oracle_check(s):
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
    return found
sol_oracles = {t: oracle_check(v['plaintext']) for t, v in solves.items()}
lay_oracles = [{**t, 'oracles': oracle_check(t['output'])} for t in layered]
lay_hits = [t for t in lay_oracles if t['oracles']]
print(f'exact oracles: {len(solves)} solves + {len(layered)} layered, {len(lay_hits)} layered hits')
(OUT / 'manifest.json').write_text(json.dumps(
    {'date': '2026-09-14', 'review': '14_CRITICAL_REVIEW_2026-09-14.md move 5 (tail as cipher object)',
     'envelope_bytes_read': 0, 'aes_decryptions': 0,
     'profile': profile, 'targets': list(TARGETS),
     'substitution': {'restarts': 60, 'iters': 400, 'controls': 30},
     'layered': {'keys': list(KEYS), 'ciphers': ['vig_dec', 'vig_enc', 'beau', 'rail_dec', 'col_dec'],
                 'rails': [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 16],
                 'cols': [2, 3, 4, 5, 6, 7, 8, 10, 13, 16, 32], 'controls': 60},
     'oracles': ['dbbi_pattern', 'marker_and_prize_addresses']}, indent=1) + '\n')
(OUT / 'results.json').write_text(json.dumps(
    {'profile': profile, 'substitution': solves, 'substitution_controls': controls,
     'layered_top': top, 'layered_above_control': above, 'layered_oracle_hits': lay_hits,
     'substitution_oracle_hits': sol_oracles, 'layered_controls_max': ctl_max,
     'planted_round_trip': plant_ok}, indent=1) + '\n')
(OUT / 'all_outputs.jsonl').write_text(
    ''.join(json.dumps({'family': 'substitution', 'target': k, 'output': v['plaintext']}) + '\n'
            for k, v in solves.items()) +
    ''.join(json.dumps({'family': 'layered', **r}) + '\n' for r in layered))
print('WROTE', OUT)