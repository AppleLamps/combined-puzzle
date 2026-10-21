"""Independent audit written for the 2026-09-14 critical review.

Re-derives, from the saved stage data only, the load-bearing claims the clean
workspace rests on, and adds the controls that decide whether each is evidence.
Writes JSON evidence to runs/2026-09-14_critical_review/. Read-only: no envelope
passwords are generated and no puzzle bytes are modified.

    python tools/audit_critical_review.py
"""
import json, random, re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / 'data', ROOT / 'runs/2026-09-14_critical_review'
OUT.mkdir(parents=True, exist_ok=True)
rd = lambda n: (DATA / n).read_text().strip()
dbbi, faed = rd('DBBI_91.txt'), rd('FAED_570.txt')
vic_lines = (DATA / 'checkerboard_vic_91.txt').read_text().splitlines()
vic, digits = vic_lines[0], vic_lines[1]
bits_lines = (DATA / 'poster_spiral_bits.txt').read_text().splitlines()
bits, colors = bits_lines[0], bits_lines[1]
arch = rd('architect_letters_1539.txt')
p32 = (DATA / 'phase3_2_plaintext.bin').read_bytes()
res = {}
def ok(msg): print('CHECK', msg)

# --- A. Phase 3.2: the "Architect plaintext" is a derived decryption ----------
blk = p32[447:1986]
ct = blk.decode('latin1').encode('cp273').decode('ascii')
key = 'THEMATRIXHASYOU'
arch2 = ''.join(chr(65 + (ord(key[k % len(key)]) - ord(ch.upper())) % 26) for k, ch in enumerate(ct))
res['architect_block'] = {
    'bytes': len(blk), 'distinct_byte_values': len(set(blk)),
    'decode': 'latin1 -> cp273 -> ascii, then Beaufort(key=THEMATRIXHASYOU)',
    'letters': len(arch2), 'matches_saved_file': arch2 == arch,
    'PRIVATEKEY_offsets_0based': [m.start() for m in re.finditer('PRIVATEKEY', arch2)],
    'arch[479:489]': arch2[479:489], 'arch[478:488]': arch2[478:488],
    'arch[480:490]': arch2[480:490], 'arch[484:494]': arch2[484:494]}
ok(f'Architect block {len(blk)} bytes / {len(set(blk))} distinct -> {len(arch2)} letters, file match={arch2 == arch}')

# --- B. DBBI prime grammar: existence is the signal, "23" is arithmetic -------
isprime = lambda n: n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))
def parses(s):
    """Complete parses: a prime-numbered cell is a `b`/`be` token; any other cell is one letter."""
    out = []
    def rec(at, slot, cells):
        if at == len(s): out.append(cells); return
        if isprime(slot):
            if s[at] != 'b': return
            for tok in ('b', 'be'):
                if s.startswith(tok, at): rec(at + len(tok), slot + 1, cells + [(slot, tok, True)])
        else: rec(at + 1, slot + 1, cells + [(slot, s[at], False)])
    rec(0, 1, []); return out
P = parses(dbbi)
def tokens(s, pre):
    t, i = [], 0
    while i < len(s):
        n = 2 if s[i] in pre else 1
        if i + n > len(s): return None
        t.append(s[i:i + n]); i += n
    return t
pairs = [p + q for i, p in enumerate('abcdefghi') for q in 'abcdefghi'[i + 1:]]
N = 20000; rng = random.Random(20260914); L = list(dbbi)
hit_parse = hit_any = hit_bg = 0
for _ in range(N):
    rng.shuffle(L); s = ''.join(L)
    if parses(s): hit_parse += 1
    for p in pairs:
        t = tokens(s, p)
        if t and len(t) == 64 and len(set(t)) == 16:
            hit_any += 1
            if p == 'bg': hit_bg += 1
            break
res['dbbi_grammar'] = {
    'parses': [{'cells': len(p), 'prime_cells': sum(c[2] for c in p),
                'b': sum(c[2] and c[1] == 'b' for c in p), 'be': sum(c[2] and c[1] == 'be' for c in p),
                'ordinary_cells': sum(not c[2] for c in p),
                'ordinary_letters_that_happen_to_be_b': sum((not c[2]) and c[1] == 'b' for c in p)} for p in P],
    'pi_84': len([x for x in range(2, 85) if isprime(x)]),
    'controls': {'n': N, 'complete_parse': hit_parse, 'any_pair_64_16': hit_any, 'bg_pair_64_16': hit_bg}}
ok(f'DBBI parses {[len(p) for p in P]}; pi(84)={res["dbbi_grammar"]["pi_84"]}; controls parse {hit_parse}/{N}, any-pair {hit_any}/{N}, bg {hit_bg}/{N}')

# --- C. DBBI 84-cell matrix: the shape decides whether a word appears --------
br = next(p for p in P if len(p) == 84)
vals = []
for slot, tok, pr in br:
    vals.append((-slot if tok == 'b' else slot) if pr else ord(tok) - 96)
def sumlist(v, rows, cols, axis):
    if axis == 'col': return [sum(v[r * cols + c] for r in range(rows)) for c in range(cols)]
    return [sum(v[r * cols + c] for c in range(cols)) for r in range(rows)]
letters = lambda v: ''.join(chr(97 + x % 26) for x in v)
grid = {}
for shape in ((7, 12), (6, 14), (14, 6), (12, 7)):
    grid['x'.join(map(str, shape))] = {'col': letters(sumlist(vals, *shape, 'col')), 'row': letters(sumlist(vals, *shape, 'row'))}
res['dbbi_matrix_signed_model'] = {'shapes': grid, 'total_of_84_values': sum(vals),
                                   'poster_one_bit_total': bits.count('1')}
ok('DBBI shapes: ' + '; '.join(f'{k} col={v["col"]}' for k, v in grid.items()))

# --- D. checkerboard alphabet: how much is actually pinned -------------------
codes = [str(x) for x in range(10) if x not in (1, 4)] + ['1' + str(x) for x in range(10)] + ['4' + str(x) for x in range(10)]
alpha = 'FUBCDORA.LETHINGKYMVPS/JQZXW'
used, k = [], 0
while k < len(digits):
    w = 2 if digits[k] in '14' else 1; used.append(digits[k:k + w]); k += w
cnt = Counter(used)
res['checkerboard'] = {'digit_count': len(digits), 'codes_used': len(cnt),
                       'unused_codes': [c for c in codes if c not in cnt],
                       'pinned_symbols': sum(1 for c in codes if c in cnt),
                       'plaintext': ''.join(dict(zip(codes, alpha))[c] for c in used)}
diff = ''.join(chr(65 + (ord(a.upper()) - ord(c)) % 26) for a, c in zip(dbbi, vic))
tail = diff[27:]
res['dbbi_minus_vic'] = {'diff': diff, 'tail64': tail, 'tail_distinct_letters': len(set(tail)),
                         'VIC_at_1_4_21': diff[0] + diff[3] + diff[20], 'YOUWON_at_22_27': diff[21:27]}
ok(f'checkerboard pins {res["checkerboard"]["pinned_symbols"]}/28 symbols; DBBI-VIC tail has {len(set(tail))} distinct letters in 64')

# --- E. Lead L1 and the zeroing correction ----------------------------------
primes = [p for p in range(2, 100) if isprime(p)][:24]
y = sum(p for p, c in zip(primes, colors) if c == 'Y'); b = sum(p for p, c in zip(primes, colors) if c == 'B')
blue = [p for p, c in zip(primes, colors) if c == 'B']
res['L1_color_primes'] = {'pairs': ' '.join(f'{p}{c}' for p, c in zip(primes, colors)), 'yellow': y, 'blue': b,
                          'blue_minus_yellow': b - y, 'difference_is_a_blue_prime': (b - y) in blue,
                          'blue_after_zeroing_difference': b - (b - y), 'arch[479:489]': arch[479:489]}
ok(f'L1: yellow {y} / blue {b}, difference {b - y} (a blue prime: {(b - y) in blue}) -> zeroed blue {b - (b - y)}')

# --- F. Two constructions present outside this folder only -------------------
F = ('The future is fluid. Each act, each decision, and each development creates '
     'new possibilities and eliminates others. The future is ours to direct.')
nostop = re.sub(r'[^\w\s]', '', F)
x = 0xF73D92 ^ 0xA94021
res['outside_checks'] = {
    'fresco_chars_with_spaces_no_punct': len(nostop), 'fresco_words': len(F.split()),
    'fresco_letters': sum(c.isalpha() for c in F),
    'passport_11092001_hex': hex(11092001), 'passport_is_24bit': 11092001 < 2**24, 'passport_is_prime': isprime(11092001),
    'f73d92_xor_a94021': hex(x), 'xor_popcount': bin(x).count('1'), 'xor_significant_bits': x.bit_length(),
    'f73d92_popcount': bin(0xF73D92).count('1'),
    'poster_colour_word_24bit': '0x' + colors.translate(str.maketrans('BY', '10'))}
ok(f'outside: Fresco {len(nostop)} chars / {len(F.split())} words; F73D92 xor A94021 = {hex(x)} popcount {bin(x).count("1")} / {x.bit_length()} bits')

(OUT / 'audit.json').write_text(json.dumps(res, indent=1) + '\n')
print('\nWROTE', OUT / 'audit.json')