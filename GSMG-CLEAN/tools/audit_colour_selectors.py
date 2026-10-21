"""Move 3: colours as selectors, not weights. 14_CRITICAL_REVIEW_2026-09-14.md move 3.

The one sourced use of the prime structure that no run has ever tried: the 16 blue / 7 yellow prime
cells do not contribute *values* - they SELECT which ordinary cells participate. The prime cells are
the mask; the 61 ordinary a..i cells are the material. This run splits DBBI's 84 logical cells by
colour assignment, computes the page's own sum-list operation on each side, and judges every output
against shuffle controls of the same masks plus the exact oracles. No envelope bytes are read.

    python tools/audit_colour_selectors.py
"""
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / 'data', ROOT / 'runs/2026-09-14_colour_selectors'
OUT.mkdir(parents=True, exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda n: (DATA / n).read_text().strip()
dbbi, faed, arch = rd('DBBI_91.txt'), rd('FAED_570.txt'), rd('architect_letters_1539.txt')
colors = rd('poster_spiral_bits.txt').splitlines()[1]
isprime = lambda n: n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))

# ---- the 84 logical cells: each slot is material or a coloured marker ----------------
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
ORD = [(i, ord(tok) - 96) for i, (slot, tok, pr) in enumerate(P84) if not pr]   # 61 ordinary
MRK = [(i, 'B' if tok == 'b' else 'Y') for i, (slot, tok, pr) in enumerate(P84) if pr]  # 23 markers
assert len(ORD) == 61 and len(MRK) == 23
COLOUR = {i: c for i, c in MRK}
def preceding_colour(i):
    pre = [c for j, c in MRK if j < i]
    return pre[-1] if pre else None

# ---- selector families ----------------------------------------------------------------
FAM = {}
FAM['ordinary_blue_nearest'] = [v for i, v in ORD if preceding_colour(i) == 'B']
FAM['ordinary_yellow_nearest'] = [v for i, v in ORD if preceding_colour(i) == 'Y']
FAM['ordinary_all'] = [v for _, v in ORD]
segs, cur = [], []
for i, (slot, tok, pr) in enumerate(P84):
    if pr:
        if cur: segs.append((cur, COLOUR[i])); cur = []
    else: cur.append(ord(tok) - 96)
if cur: segs.append((cur, COLOUR[MRK[-1][0]]))
for colour in ('B', 'Y'):
    FAM[f'segment_sums_bounded_{colour}'] = [sum(s) for s, c in segs if c == colour]
def masked(prime_value):
    v = [None] * 84
    for i, (slot, tok, pr) in enumerate(P84):
        v[i] = prime_value(COLOUR[i]) if pr else ord(tok) - 96
    return v
FAM_LATTICE = {'masked_zero': masked(lambda c: 0),
               'masked_colour_digit': masked(lambda c: 2 if c == 'B' else 25),
               'masked_one': masked(lambda c: 1)}
def rows_with(colour, r, c, lat):
    out = []
    for row in range(r):
        cells_r = lat[row * c:(row + 1) * c]
        idx = list(range(row * c, (row + 1) * c))
        if any(k in COLOUR and COLOUR[k] == colour for k in idx):
            out += [cells_r[j] for j, k in enumerate(idx) if k not in COLOUR]
    return out
FAM['yellow_rows_ordinary_6x14'] = rows_with('Y', 6, 14, [ord(t) - 96 if not pr else 0 for _, t, pr in P84])
FAM['blue_rows_ordinary_6x14'] = rows_with('B', 6, 14, [ord(t) - 96 if not pr else 0 for _, t, pr in P84])
blue_slots = [slot for slot, tok, pr in P84 if pr and tok == 'b']
yellow_slots = [slot for slot, tok, pr in P84 if pr and tok == 'be']
ordinary_slots = [slot for slot, tok, pr in P84 if not pr]
FAM['faed_at_blue_slots'] = [ord(faed[s - 1]) - 96 for s in blue_slots]
FAM['faed_at_yellow_slots'] = [ord(faed[s - 1]) - 96 for s in yellow_slots]
FAM['faed_at_ordinary_slots'] = [ord(faed[s - 1]) - 96 for s in ordinary_slots]

# ---- decodes (the folder's letter families) --------------------------------------------
DIG = str.maketrans('abcdefghio', '1234567890')
def page_bytes(nums):
    t = ''.join(str(abs(n)) for n in nums)
    if not t or any(ch not in '0123456789' for ch in t): return None
    n = int(t)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')
def decodes(nums):
    out = {}
    if nums and all(0 <= n % 26 < 26 for n in nums):
        out['mod26_A0'] = ''.join(chr(97 + n % 26) for n in nums)
        out['mod26_A1'] = ''.join(chr(96 + n % 26) if n % 26 else 'z' for n in nums)
    if all(1 <= n <= 26 for n in nums):
        out['a1z26'] = ''.join(chr(64 + n) for n in nums)
    if all(0 <= n < len(arch) for n in nums):
        out['arch_index0'] = ''.join(arch[n] for n in nums)
    b = page_bytes(nums)
    if b is not None:
        out['page_codec'] = b.decode('latin1')
    return out
TRIGRAMS = ['the', 'and', 'ing', 'ion', 'ent', 'tio', 'for', 'her', 'ter', 'hat', 'tha', 'ere',
            'ate', 'his', 'con', 'res', 'ver', 'all', 'ons', 'nce', 'men', 'ith', 'ted', 'ers',
            'pro', 'thi', 'wit', 'are', 'ess', 'not', 'ive', 'was', 'ect', 'rea', 'com', 'eve']
def score(t):
    return sum(t.lower().count(g) for g in TRIGRAMS)

import random
results = []
for fname, L in FAM.items():
    for lname, nums in (('raw', L), ('cumulative', [sum(L[:i + 1]) for i in range(len(L))] if L else []),
                        ('reversed', L[::-1])):
        if not nums: continue
        for dname, d in decodes(nums).items():
            if dname == 'page_codec' or len(d) < 4: continue
            results.append({'selector': fname, 'list': lname, 'decode': dname,
                            'length': len(d), 'score': score(d), 'output': d})
for lname, lat in FAM_LATTICE.items():
    for r, c in ((6, 14), (7, 12)):
        for sname, nums in (('row_sums', [sum(lat[i * c:(i + 1) * c]) for i in range(r)]),
                            ('col_sums', [sum(lat[i * c:(i + 1) * c][j] for i in range(r)) for j in range(c)])):
            for dname, d in decodes(nums).items():
                if dname == 'page_codec' or len(d) < 4: continue
                results.append({'selector': lname + f'_{r}x{c}', 'list': sname, 'decode': dname,
                                'length': len(d), 'score': score(d), 'output': d})
print(f'{len(results)} letter outputs from {len(FAM)} selector lists + 3 lattices x 2 shapes')

rng = random.Random(20260914)
control_max, control_n = 0, 0
for _ in range(300):
    s = [ord(ch) - 96 for ch in list(dbbi)]; rng.shuffle(s)
    pr2, su = [], None
    for famsel in FAM.values():
        idx = sorted(rng.sample(range(84), min(len(famsel), 84)))
        nums = [s[i] for i in idx]
        for d in decodes(nums).values():
            if d is None or len(d) < 4: continue
            if all(ch in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' for ch in d):
                control_max = max(control_max, score(d)); control_n += 1
    for r, c in ((6, 14), (7, 12)):
        lat = [rng.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 25]) for _ in range(r * c)]
        for nums in ([sum(lat[i * c:(i + 1) * c]) for i in range(r)],
                     [sum(lat[i * c:(i + 1) * c][j] for i in range(r)) for j in range(c)]):
            for d in decodes(nums).values():
                if d is None or len(d) < 4: continue
                if all(ch in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' for ch in d):
                    control_max = max(control_max, score(d)); control_n += 1
top = sorted(results, key=lambda x: -x['score'])[:10]
print(f'{control_n} control readings; control max {control_max}')
for t in top:
    flag = '  <-- ABOVE CONTROL' if t['score'] > control_max else ''
    print(f"  score {t['score']:3d}  {t['selector']} {t['list']} {t['decode']}  {t['output'][:48]!r}{flag}")
above = [t for t in results if t['score'] > control_max]
plant = [ord(ch) - 96 for ch in 'theflowerblossomsthroughwhatseemstobeaconcretesurface']
plant_scores = [score(d) for d in decodes(plant).values() if d is not None and len(d) >= 4]
print(f'planted-controls max score {max(plant_scores) if plant_scores else None}'
      f' (power: {bool(plant_scores and max(plant_scores) > control_max)})')

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
    {'date': '2026-09-14', 'review': '14_CRITICAL_REVIEW_2026-09-14.md move 3 (colours as selectors)',
     'envelope_bytes_read': 0, 'aes_decryptions': 0,
     'selectors': list(FAM) + [f'lattice {k}' for k in FAM_LATTICE],
     'controls': {'controls_drawn': control_n, 'control_max_score': control_max,
                  'planted_max': max(plant_scores) if plant_scores else None},
     'oracles': ['dbbi_pattern', 'marker_and_prize_addresses']}, indent=1) + '\n')
(OUT / 'results.json').write_text(json.dumps(
    {'outputs': len(results), 'controls_drawn': control_n, 'control_max_score': control_max,
     'above_control': above, 'oracle_hits': hits, 'top': top}, indent=1) + '\n')
(OUT / 'all_outputs.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in results))
print('WROTE', OUT)