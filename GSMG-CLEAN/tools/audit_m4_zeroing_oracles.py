"""Close the M4 zeroing construction against the exact oracles.

M4 (14_CRITICAL_REVIEW_2026-09-14.md): the poster colour markers on the first 24 primes give
yellow 479 / blue 484; the difference 5 is itself a blue prime, so the creator's announced
"zeroed out" instruction (#8000) balances the two colour lists at 479 = 479, and 0-based
Architect[479:489] = "PRIVATEKEY".

This run states every convention of that construction, enumerates the strings it yields, and
tests them ONLY against exact, information-bearing oracles:

  1. the three known answer digests (phase 1, phase 2 seven-part, phase 3.2 three-part);
  2. the same digests with the candidate substituted for one known part (replacement test);
  3. the four solved marker addresses plus the two prize addresses (sha256 / sha256d /
     sha3-256 / raw scalar / sha256-of-hex, compressed and uncompressed P2PKH);
  4. the DBBI sha256 equality pattern (L5).

NO AES decryption and no envelope bytes are touched. Reproduce:
    python tools/audit_m4_zeroing_oracles.py
"""
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / 'data', ROOT / 'runs/2026-09-14_m4_zeroing_oracles'
OUT.mkdir(parents=True, exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda n: (DATA / n).read_text().strip()

# ---- exact oracles -------------------------------------------------------------------
DIGESTS = {
    'phase1_answer': '5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75',
    'phase2_seven_part': '1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5',
    'phase32_three_part': '250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c'}
PARTS32 = ['jacquefresco', 'giveitjustonesecond', 'heisenbergsuncertaintyprinciple']
PARTS2 = json.loads((DATA / 'seven_part_phase3_answer.json').read_text())
PHASE1 = 'theflowerblossomsthroughwhatseemstobeaconcretesurface'
DBBI_PATTERN = '01234556728966286abc61c88b48de3086dd501d5557d6bab5605233df7bbb96'
MARKER_ADDRS = ['18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc', '1AD2wfwXukZ1kUAy848hTQQ72aSBZPB75r',
                '13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp']
MARKER_PREFIX = '1GyT5W'
PRIZE = {'HALF': '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe',
         'BETTER HALF': '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'}

# ---- secp256k1 / base58 (same conventions as tools/check_candidate.py) ---------------
P = 2**256 - 2**32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
def _add(a, b):
    if a is None: return b
    if b is None: return a
    if a[0] == b[0] and (a[1] + b[1]) % P == 0: return None
    s = (3 * a[0] * a[0] * pow(2 * a[1], -1, P) if a == b else (b[1] - a[1]) * pow(b[0] - a[0], -1, P)) % P
    x = (s * s - a[0] - b[0]) % P
    return x, (s * (a[0] - x) - a[1]) % P
def _mul(k):
    r, c = None, G
    while k:
        if k & 1: r = _add(r, c)
        c = _add(c, c); k >>= 1
    return r
h160 = lambda b: hashlib.new('ripemd160', hashlib.sha256(b).digest()).hexdigest()
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58enc(b):
    b = b + hashlib.sha256(hashlib.sha256(b).digest()).digest()[:4]
    n, z = int.from_bytes(b, 'big'), 0
    for byte in b:
        if byte: break
        z += 1
    s = ''
    while n: s, n = B58[n % 58] + s, n // 58
    return '1' * z + s
def b58dec(s):
    n = 0
    for ch in s: n = n * 58 + B58.index(ch)
    raw = n.to_bytes(25, 'big')
    assert hashlib.sha256(hashlib.sha256(raw[:-4]).digest()).digest()[:4] == raw[-4:], 'bad checksum'
    return raw[1:21]
def pubkeys(k):
    x, y = _mul(k)
    return {'uncompressed': b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big'),
            'compressed': bytes([2 + (y & 1)]) + x.to_bytes(32, 'big')}
def addresses(k):
    return {form: b58enc(b'\x00' + bytes.fromhex(h160(pub))) for form, pub in pubkeys(k).items()}

TARGET_H160 = {a: b58dec(a).hex() for a in MARKER_ADDRS}
TARGET_H160.update({PRIZE[k]: b58dec(v).hex() for k, v in PRIZE.items()})
TARGET_LABEL = {a: ('marker ' + a) for a in MARKER_ADDRS}
TARGET_LABEL.update({PRIZE[k]: k for k in PRIZE})
TARGET_PREFIX = {MARKER_PREFIX}

def eq_pattern(h):
    first = {}
    return ''.join('0123456789abcdef'[first.setdefault(c, len(first))] if len(first) < 16 or c in first
                   else '?' for c in h)

# ---- A. self-tests: the oracle machinery must reproduce known facts first ------------
digits149 = rd('checkerboard_vic_91.txt').splitlines()[1]
url_bits = rd('poster_spiral_bits.txt').splitlines()[0][:192]
SELFTEST = {
    'addr_18CchrjA3U_from_sha256_of_149_digits':
        addresses(int(sha(digits149.encode()), 16))['compressed'] == MARKER_ADDRS[0],
    'addr_1AD2wfwX_from_sha256_of_phase1_answer':
        addresses(int(sha(PHASE1.encode()), 16))['compressed'] == MARKER_ADDRS[1],
    'addr_13HGhjkm_from_bitreversed_url_integer_raw':
        addresses(int(url_bits[::-1], 2))['compressed'] == MARKER_ADDRS[2],
    'addr_1GyT5W_prefix_from_sha256_of_prize_address':
        addresses(int(sha(PRIZE['HALF'].encode()), 16))['compressed'].startswith(MARKER_PREFIX),
    'digest_phase1_answer': sha(PHASE1.encode()) == DIGESTS['phase1_answer'],
    'digest_phase2_seven_part': sha(''.join(PARTS2).encode()) == DIGESTS['phase2_seven_part'],
    'digest_phase32_three_part': sha(''.join(PARTS32).encode()) == DIGESTS['phase32_three_part'],
}
assert all(SELFTEST.values()), SELFTEST
print('SELFTEST PASS (4 marker addresses + 3 chain digests reproduced by this code)')

# ---- B. every convention of the zeroing construction --------------------------------
colors = rd('poster_spiral_bits.txt').splitlines()[1]
primes24 = [p for p in range(2, 100) if all(p % d for d in range(2, int(p ** .5) + 1))][:24]
T1 = rd('architect_letters_1539.txt')
T2 = re.sub(r'\s+', '', (DATA / 'architect_plaintext_readable.txt').read_text(encoding='utf-8'))
assert len(T2) == 1544, len(T2)
TEXTS = {'letters1539_0based': T1, 'letters1539_1based': T1, 'compact1544_0based': T2}
def window(name, i):
    if i is None: return None
    if name == 'letters1539_1based': return T1[i - 1:i + 9] if 1 <= i <= len(T1) - 9 else None
    t = TEXTS[name]
    return t[i:i + 10] if 0 <= i <= len(t) - 10 else None
NOTABLE = ['PRIVATEKEY', 'PRIVATE', 'REINSERTING', 'SELECT', 'BRUTEFORCING', 'INTERTWINED',
           'SOURCECODES', 'PRIMEBASICS', 'YOUWON', 'CIPHERS']
NOTABLE_STARTS = {n: {t: [m.start() for m in re.finditer(n, txt)] for t, txt in TEXTS.items()} for n in NOTABLE}

scan = []
for rot in range(24):
    for d in (1, -1):
        pr = [primes24[(rot + d * i) % 24] for i in range(24)]
        Y = sum(p for p, c in zip(pr, colors) if c == 'Y')
        B = sum(p for p, c in zip(pr, colors) if c == 'B')
        big = 'B' if B > Y else 'Y'
        diff = abs(B - Y)
        lst = [p for p, c in zip(pr, colors) if c == big]
        zeroable = diff in lst
        bal = max(B, Y) - diff if zeroable else None
        marker = (lst.index(diff) + 1) if zeroable else None   # 1-based marker holding the zeroed prime
        row = {'rotation': rot, 'direction': d, 'yellow': Y, 'blue': B, 'difference': diff,
               'larger_side': big, 'zeroable': zeroable, 'zeroed_prime': diff, 'balanced_value': bal,
               'zeroed_marker_1based': marker,
               'selected': {n: window(n, bal) for n in TEXTS},
               'notable_at_balance': [n for n in NOTABLE
                                      for t, txt in TEXTS.items()
                                      if bal is not None and bal in NOTABLE_STARTS[n][t]]}
        scan.append(row)
auth = next(r for r in scan if r['rotation'] == 0 and r['direction'] == 1)
print(f"authenticated assignment: yellow {auth['yellow']} / blue {auth['blue']}, diff {auth['difference']}"
      f" (zeroable={auth['zeroable']}), balanced {auth['balanced_value']},"
      f" selects {auth['selected']['letters1539_0based']}")
n_zeroable = sum(r['zeroable'] for r in scan)
n_pk = sum(1 for r in scan if any(v == 'PRIVATEKEY' for v in r['selected'].values()))
n_notable = sum(1 for r in scan if r['notable_at_balance'])
print(f'of 48 prime assignments: {n_zeroable} zeroable, {n_pk} select PRIVATEKEY,'
      f' {n_notable} select any notable word')

# ---- C. candidates the construction yields ------------------------------------------
cands = {}
def add(s, fam, note):
    if isinstance(s, str) and s and s not in cands:
        cands[s] = {'family': fam, 'note': note}

for tname, txt in (('letters1539', T1), ('compact1544', T2)):
    for idx in (478, 479, 480):
        for L in range(1, 49):
            w = txt[idx:idx + L]
            if len(w) == L:
                add(w, 'index_window', f'{tname}[{idx}:{idx + L}]')
                add(w.lower(), 'index_window', f'{tname}[{idx}:{idx + L}] lower')
for s in ['479', '484', '5', '963', '479479', '479484', '484479', '4795', '5479', '479-479', '479 479',
          '479479479', 'blue479', 'yellow479', '479blue', '479yellow', 'yellowblue479', 'blueyellow479',
          '479=479', '479=484', 'zero', 'zero5', '05', '005', '479.479', '479,479', '479/479', '479|479']:
    add(s, 'balanced_number', 'colour-prime sums and the zeroed difference')
Ypr = [p for p, c in zip(primes24, colors) if c == 'Y']
Bpr = [p for p, c in zip(primes24, colors) if c == 'B']
for sep in ('', ',', ' ', '-', '|'):
    add(sep.join(map(str, Ypr)), 'prime_list', 'yellow primes')
    add(sep.join(map(str, Bpr)), 'prime_list', 'blue primes')
    add(sep.join(map(str, [0 if p == 5 else p for p in Bpr])), 'prime_list', 'blue primes with 5 zeroed')
    add(sep.join(map(str, [p for p in Bpr if p != 5])), 'prime_list', 'blue primes with 5 removed')
    add(sep.join(map(str, Ypr + Bpr)), 'prime_list', 'yellow then blue')
    add(sep.join(map(str, Bpr + Ypr)), 'prime_list', 'blue then yellow')
url = bytes(int(url_bits[i:i + 8], 2) for i in range(0, 192, 8)).decode()
add(colors, 'zeroed_marker', 'colour marker stream')
add(colors.lower(), 'zeroed_marker', 'colour marker stream lower')
add(colors[:2] + '0' + colors[3:], 'zeroed_marker', 'marker 3 zeroed')
add(colors[:2] + 'Z' + colors[3:], 'zeroed_marker', 'marker 3 as Z')
add(colors[:2] + colors[3:], 'zeroed_marker', 'marker 3 removed')
add(url, 'zeroed_marker', 'poster URL')
add(url.lower(), 'zeroed_marker', 'poster URL lower')
add(url[:2] + chr(ord(url[2]) & ~1) + url[3:], 'zeroed_marker', 'URL with marker 3 bit cleared')
add(url[:2] + url[3:], 'zeroed_marker', 'URL with marker 3 byte removed')
order, seen, r0, c0, d = [], set(), 0, 0, 0
dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))
for _ in range(196):
    order.append((r0, c0)); seen.add((r0, c0))
    nr, nc = r0 + dirs[d][0], c0 + dirs[d][1]
    if not (0 <= nr < 14 and 0 <= nc < 14) or (nr, nc) in seen:
        d = (d + 1) % 4; nr, nc = r0 + dirs[d][0], c0 + dirs[d][1]
    r0, c0 = nr, nc
bits = rd('poster_spiral_bits.txt').splitlines()[0]
def sums_for(g):
    rows = [sum(g[(r, c)] for c in range(14)) for r in range(14)]
    cols = [sum(g[(r, c)] for r in range(14)) for c in range(14)]
    return rows, cols
g0 = {rc: int(bits[i]) for i, rc in enumerate(order)}
rows0, cols0 = sums_for(g0)
g1 = dict(g0); g1[order[23]] = 0            # marker 3 sits on spiral index 23
rows1, cols1 = sums_for(g1)
for label, rows, cols in (('before', rows0, cols0), ('after_zeroing_marker3', rows1, cols1)):
    for sep in ('', ',', ' '):
        add(sep.join(map(str, rows)), 'poster_matrix_sums', f'row sums {label}')
        add(sep.join(map(str, cols)), 'poster_matrix_sums', f'column sums {label}')
        add(sep.join(map(str, rows + cols)), 'poster_matrix_sums', f'rows then columns {label}')
        add(sep.join(map(str, cols + rows)), 'poster_matrix_sums', f'columns then rows {label}')
    add(str(sum(rows) + sum(cols)), 'poster_matrix_sums', f'total {label}')
print(f'candidates: {len(cands)}')

# ---- D. exact oracles only (no envelope bytes are read) ------------------------------
def scalars_for(s):
    b = s.encode()
    out = {'sha256': int(sha(b), 16),
           'sha256d': int(hashlib.sha256(hashlib.sha256(b).digest()).hexdigest(), 16),
           'sha3_256': int(hashlib.sha3_256(b).hexdigest(), 16)}
    if re.fullmatch(r'\d+', s): out['raw_decimal'] = int(s)
    if len(b) == 32: out['raw_32bytes'] = int.from_bytes(b, 'big')
    if re.fullmatch(r'[0-9a-fA-F]{64}', s): out['sha256_of_hex'] = int(sha(bytes.fromhex(s)), 16)
    return {k: v for k, v in out.items() if 1 <= v < N}

LABEL_OF = {v: k for k, v in TARGET_H160.items()}
hits, n_ec = [], 0
for s, meta in cands.items():
    h = sha(s.encode())
    found = []
    if h in DIGESTS.values():
        found.append({'oracle': 'chain_digest', 'detail': [k for k, v in DIGESTS.items() if v == h]})
    for name, parts, dig in (('phase32_three_part', PARTS32, DIGESTS['phase32_three_part']),
                             ('phase2_seven_part', PARTS2, DIGESTS['phase2_seven_part'])):
        for i in range(len(parts)):
            if sha(''.join(parts[:i] + [s] + parts[i + 1:]).encode()) == dig:
                found.append({'oracle': 'replaces_known_part', 'detail': f'{name} part {i + 1}'})
    if eq_pattern(h) == DBBI_PATTERN:
        found.append({'oracle': 'dbbi_pattern', 'detail': 'sha256 equality pattern matches the DBBI tokens'})
    for form, sc in scalars_for(s).items():
        n_ec += 1
        for pform, pub in pubkeys(sc).items():
            hh = h160(pub)
            a = b58enc(b'\x00' + bytes.fromhex(hh))
            if hh in TARGET_H160:
                found.append({'oracle': 'address', 'detail': LABEL_OF[hh], 'scalar_form': form,
                              'pubkey_form': pform, 'address': a})
            elif a.startswith(MARKER_PREFIX):
                found.append({'oracle': 'address_prefix', 'detail': MARKER_PREFIX, 'scalar_form': form,
                              'pubkey_form': pform, 'address': a})
    if found:
        hits.append({'candidate': s, 'family': meta['family'], 'note': meta['note'], 'hits': found})
print(f'oracle coverage: {len(cands)} candidates, {n_ec} scalar forms, {len(hits)} with an oracle hit')

# ---- E. write evidence ----------------------------------------------------------------
manifest = {'date': '2026-09-14', 'review': '14_CRITICAL_REVIEW_2026-09-14.md section M4 / move 1',
            'purpose': 'close the M4 zeroing construction against exact oracles before any envelope work',
            'envelope_bytes_read': 0, 'aes_decryptions': 0,
            'inputs': {p: sha((DATA / p).read_bytes()) for p in
                       ['poster_spiral_bits.txt', 'architect_letters_1539.txt',
                        'architect_plaintext_readable.txt', 'checkerboard_vic_91.txt',
                        'seven_part_phase3_answer.json']},
            'oracles': {'chain_digests': DIGESTS,
                        'replacement_targets': ['phase32_three_part', 'phase2_seven_part'],
                        'addresses': MARKER_ADDRS + [MARKER_PREFIX + ' (prefix)'] + list(PRIZE.values()),
                        'dbbi_pattern': DBBI_PATTERN},
            'conventions_scanned': {'prime_assignments': '24 rotations x 2 directions',
                                    'texts': list(TEXTS), 'indexing': '0-based and 1-based',
                                    'zeroing_operands': 'the prime equal to the colour-sum difference'},
            'selftest': SELFTEST,
            'limits': ['literal answers only; the construction as a key/selector is not covered',
                       'no sign, matrix or FAED continuation is generated',
                       'one prefix-only target (1GyT5W) is matched on 6 leading base58 characters']}
(OUT / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
(OUT / 'assignment_scan.json').write_text(json.dumps(scan, indent=1) + '\n')
(OUT / 'candidates.jsonl').write_text(''.join(json.dumps({'candidate': s, **m}) + '\n' for s, m in cands.items()))
(OUT / 'results.json').write_text(json.dumps(
    {'candidates': len(cands), 'scalar_forms_tested': n_ec, 'oracle_hits': hits,
     'assignment_scan': {'assignments': len(scan), 'zeroable': n_zeroable,
                         'select_PRIVATEKEY': n_pk, 'select_any_notable': n_notable,
                         'authenticated': auth}}, indent=1) + '\n')
print('WROTE', OUT)