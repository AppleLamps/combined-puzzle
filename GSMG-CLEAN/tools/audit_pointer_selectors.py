"""Move 1 of the critical review's plan: use the M4 balanced pointer as an OPERAND.

14_CRITICAL_REVIEW_2026-09-14.md concluded that the colour-prime zeroing balance is a pointer to
Architect offset 479, not a payload, and 03_OPEN_LEADS.md §1 lists as untested: "What text follows
index 479/484 under a prime or zeroing selector". This run does exactly that, on the unread fields,
with exact oracles only (no envelope bytes are read and no AES decryption is run).

Selectors come from the balance: 5 (the zeroed prime), 479 (balanced), 484 (blue), 963 (total),
and the derivatives 474 = 479 - 5, 489 = 479 + 5 + 5, 91 = 570 - 479, 86 = 570 - 484.

    python tools/audit_pointer_selectors.py
"""
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / 'data', ROOT / 'runs/2026-09-14_pointer_selectors'
OUT.mkdir(parents=True, exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda n: (DATA / n).read_text().strip()

# ---- the page's own codec: a..i/o -> 1..9/0 -> integer -> bytes -----------------------
DIG = str.maketrans('abcdefghio', '1234567890')
def decode_digits(s):
    if not s or any(ch not in 'abcdefghio' for ch in s):
        return None
    n = int(s.translate(DIG))
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')
PRINTABLE = set(range(32, 127)) | {9, 10, 13}
def is_text(b, minlen=4):
    return b is not None and len(b) >= minlen and all(x in PRINTABLE for x in b)

# ---- controls: the codec must reproduce the two known labels -------------------------
sal = rd('salphaseion_compact_1075.txt')
CONTROL = {'codec_F63_lastwords': decode_digits(sal[766:829]) == b'lastwordsbeforearchichoice',
           'codec_F29_thispassword': decode_digits(sal[830:859]) == b'thispassword',
           'compact1544_len': len(re.sub(r'\s+', '', (DATA / 'architect_plaintext_readable.txt')
                                         .read_text(encoding='utf-8'))) == 1544}
assert all(CONTROL.values()), CONTROL
print('CONTROLS PASS (page codec reproduces both known labels; 1544 compaction confirmed)')

# ---- targets and selectors -----------------------------------------------------------
dbbi, faed = rd('DBBI_91.txt'), rd('FAED_570.txt')
arch = rd('architect_letters_1539.txt')
digits149 = rd('checkerboard_vic_91.txt').splitlines()[1]
bits = rd('poster_spiral_bits.txt').splitlines()[0]
diff = rd('dbbi_minus_vic_91.txt')
tail = diff[27:]
a1z26 = lambda s: ''.join(str(ord(c) - 64) for c in s if c.isalpha())
TARGETS = {'FAED_570': faed, 'DBBI_91': dbbi, 'digits149': digits149,
           'salphaseion_1075': sal, 'architect_1539': arch,
           'diff_A1Z26': a1z26(diff), 'tail64_A1Z26': a1z26(tail)}
SELECTORS = [5, 479, 484, 963, 474, 489, 91, 86, 95, 100]
isprime = lambda n: n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))

# ---- 1. exhaustive window decode through the page codec ------------------------------
def scan_windows(name, s):
    out = []
    for i in range(len(s)):
        for j in range(i + 4, len(s) + 1):
            w = s[i:j]
            if name == 'digits149':
                n = int(w)
                b = n.to_bytes((n.bit_length() + 7) // 8, 'big')
            else:
                b = decode_digits(w)
            if is_text(b):
                out.append({'target': name, 'start': i, 'end': j, 'length': j - i,
                            'bytes': b.hex(), 'text': b.decode('latin1')})
    return out
window_hits = []
for name, s in TARGETS.items():
    window_hits += scan_windows(name, s)
print(f'exhaustive window decode: {sum(len(v) for v in TARGETS.values())} source characters,'
      f' {len(window_hits)} printable windows')

# ---- 2. prime and zeroing selectors (03 §1's untested idea) --------------------------
prime_sel = []
for name, s in (('FAED_570', faed), ('DBBI_91', dbbi), ('digits149', digits149)):
    pr = [i for i in range(1, len(s) + 1) if isprime(i)]
    variants = {
        'prime_positions_kept': ''.join(s[i - 1] for i in pr),
        'prime_positions_zeroed': ''.join('o' if (i in pr and name != 'digits149') else
                                          ('0' if (i in pr) else s[i - 1]) for i in range(1, len(s) + 1)),
        'nonprime_positions_zeroed': ''.join('o' if (i not in pr and name != 'digits149') else
                                             ('0' if (i not in pr) else s[i - 1])
                                             for i in range(1, len(s) + 1))}
    if name == 'DBBI_91':
        colors = rd('poster_spiral_bits.txt').splitlines()[1]
        primes24 = [p for p in range(2, 100) if isprime(p)][:24]
        for colour in ('B', 'Y'):
            sel = {p for p, c in zip(primes24, colors) if c == colour}
            variants[f'{colour}_prime_positions_zeroed'] = ''.join(
                'o' if i in sel else s[i - 1] for i in range(1, len(s) + 1))
            variants[f'{colour}_prime_positions_removed'] = ''.join(
                s[i - 1] for i in range(1, len(s) + 1) if i not in sel)
    for vname, v in variants.items():
        if name == 'digits149':
            n = int(v)
            b = n.to_bytes((n.bit_length() + 7) // 8, 'big')
        else:
            b = decode_digits(v)
        prime_sel.append({'target': name, 'selector': vname, 'selected_length': len(v),
                          'bytes': b.hex() if b else None,
                          'printable': is_text(b, 1), 'text': b.decode('latin1') if b else None})
print('prime/zeroing selector decodes: '
      + '; '.join(f"{r['target']}/{r['selector']}={r['selected_length']}d printable={r['printable']}"
                  for r in prime_sel if r['printable']) or 'all non-printable')

# ---- 3. selector-index windows against the exact oracles -----------------------------
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
def pubkeys(k):
    x, y = _mul(k)
    return {'uncompressed': b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big'),
            'compressed': bytes([2 + (y & 1)]) + x.to_bytes(32, 'big')}
DIGESTS = {'phase1_answer': '5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75',
           'phase2_seven_part': '1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5',
           'phase32_three_part': '250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c'}
PARTS32 = ['jacquefresco', 'giveitjustonesecond', 'heisenbergsuncertaintyprinciple']
PARTS2 = json.loads((DATA / 'seven_part_phase3_answer.json').read_text())
MARKER_AND_PRIZE = ['18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc', '1AD2wfwXukZ1kUAy848hTQQ72aSBZPB75r',
                    '13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp', '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe',
                    '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa']
def b58dec(s):
    n = 0
    for ch in s: n = n * 58 + B58.index(ch)
    raw = n.to_bytes(25, 'big')
    assert hashlib.sha256(hashlib.sha256(raw[:-4]).digest()).digest()[:4] == raw[-4:]
    return raw[1:21]
TARGET_H160 = {a: b58dec(a).hex() for a in MARKER_AND_PRIZE}
LABEL_OF = {v: k for k, v in TARGET_H160.items()}
DBBI_PATTERN = '01234556728966286abc61c88b48de3086dd501d5557d6bab5605233df7bbb96'
def eq_pattern(h):
    first = {}
    return ''.join('0123456789abcdef'[first.setdefault(c, len(first))] if len(first) < 16 or c in first
                   else '?' for c in h)
# control: the address machinery must reproduce a known marker address
assert b58enc(b'\x00' + bytes.fromhex(h160(pubkeys(int(sha(digits149.encode()), 16))['compressed']))
              ) == '18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc'
print('ADDRESS CONTROL PASS (sha256 of the 149 digits reproduces 18CchrjA3U...)')

CAND_TARGETS = {'FAED_570': faed, 'DBBI_91': dbbi, 'architect_1539': arch,
                'digits149': digits149, 'tail64': tail, 'diff_91': diff}
cands = {}
for tname, s in CAND_TARGETS.items():
    for idx in SELECTORS:
        if idx > len(s): continue
        for L in range(1, 33):
            w = s[idx - 1:idx - 1 + L]          # 1-based selector on a 1-indexed stream
            if len(w) == L:
                cands.setdefault(w, {'family': 'selector_window', 'note': f'{tname}[{idx}]+{L}'})
                cands.setdefault(w.lower(), {'family': 'selector_window', 'note': f'{tname}[{idx}]+{L} lower'})
            w0 = s[idx:idx + L]                 # 0-based variant
            if len(w0) == L:
                cands.setdefault(w0, {'family': 'selector_window', 'note': f'{tname}[{idx} 0b]+{L}'})
for r in prime_sel:
    if r['bytes']:
        cands.setdefault(r['bytes'], {'family': 'selector_decode_hex',
                                      'note': f"{r['target']}/{r['selector']} bytes-hex"})
        cands.setdefault(r['text'], {'family': 'selector_decode_text',
                                     'note': f"{r['target']}/{r['selector']} latin1"})
print(f'candidates: {len(cands)}')

def scalars_for(s):
    b = s.encode()
    out = {'sha256': int(sha(b), 16),
           'sha256d': int(hashlib.sha256(hashlib.sha256(b).digest()).hexdigest(), 16),
           'sha3_256': int(hashlib.sha3_256(b).hexdigest(), 16)}
    if re.fullmatch(r'\d+', s): out['raw_decimal'] = int(s)
    if len(b) == 32: out['raw_32bytes'] = int.from_bytes(b, 'big')
    if re.fullmatch(r'[0-9a-fA-F]{64}', s): out['sha256_of_hex'] = int(sha(bytes.fromhex(s)), 16)
    return {k: v for k, v in out.items() if 1 <= v < N}

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
            if hh in TARGET_H160:
                found.append({'oracle': 'address', 'detail': LABEL_OF[hh], 'scalar_form': form,
                              'pubkey_form': pform})
    if found:
        hits.append({'candidate': s, **meta, 'hits': found})
print(f'oracle coverage: {len(cands)} candidates, {n_ec} scalar forms, {len(hits)} with an oracle hit')

manifest = {'date': '2026-09-14', 'review': '14_CRITICAL_REVIEW_2026-09-14.md move 1 (pointer as operand)',
            'envelope_bytes_read': 0, 'aes_decryptions': 0,
            'controls': CONTROL | {'address_machinery': 'sha256 of the 149 digits reproduces 18CchrjA3U...'},
            'selectors': SELECTORS, 'targets': list(TARGETS), 'candidate_targets': list(CAND_TARGETS),
            'oracles': {'chain_digests': DIGESTS, 'addresses': MARKER_AND_PRIZE, 'dbbi_pattern': DBBI_PATTERN},
            'limits': ['literal answers only; selectors used as cipher keys are not covered',
                       'windows limited to 32 characters for the address oracle']}
(OUT / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
(OUT / 'window_scan.json').write_text(json.dumps(window_hits, indent=1) + '\n')
(OUT / 'prime_selector_decodes.json').write_text(json.dumps(prime_sel, indent=1) + '\n')
(OUT / 'candidates.jsonl').write_text(''.join(json.dumps({'candidate': s, **m}) + '\n' for s, m in cands.items()))
(OUT / 'results.json').write_text(json.dumps(
    {'candidates': len(cands), 'scalar_forms_tested': n_ec, 'oracle_hits': hits,
     'printable_windows': window_hits}, indent=1) + '\n')
print('WROTE', OUT)