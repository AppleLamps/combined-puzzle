"""Reproduce the CANDIDATE (unproven) lead calculations from ../data (run verify_chain.py first).
These calculations are exact; their MEANING is not established. See 03_OPEN_LEADS.md.
No password or key search is performed.    Run:  python tools/reproduce_leads.py
"""
import json, re
from pathlib import Path
DATA = Path(__file__).resolve().parents[1] / 'data'
rd = lambda n: (DATA / n).read_text().split('\n')
dbbi, faed = rd('DBBI_91.txt')[0], rd('FAED_570.txt')[0]
arch, vic = rd('architect_letters_1539.txt')[0], rd('checkerboard_vic_91.txt')[0]
colors = rd('poster_spiral_bits.txt')[1]
out = {}

# L1. Poster colours x first 24 primes (479 / 484) and Architect index 479
primes = [p for p in range(2, 100) if all(p % d for d in range(2, int(p**.5) + 1))][:24]
y = sum(p for p, c in zip(primes, colors) if c == 'Y'); b = sum(p for p, c in zip(primes, colors) if c == 'B')
out['L1_color_primes'] = {'pairs': ' '.join(f'{p}{c}' for p, c in zip(primes, colors)), 'yellow': y, 'blue': b,
                          'architect[479:489] (0-based, letters only)': arch[479:489]}
assert (y, b) == (479, 484) and arch[479:489] == 'PRIVATEKEY'

# L2. DBBI prime parse -> column sums -> HILLFEXMGSGQ
isprime = lambda n: n > 1 and all(n % d for d in range(2, int(n**.5) + 1))
parses = []
def parse(at, slot, cells):
    if at == len(dbbi): parses.append(cells); return
    if isprime(slot):
        if dbbi[at] != 'b': return
        for tok in ('b', 'be'):
            if dbbi.startswith(tok, at): parse(at + len(tok), slot + 1, cells + [(slot, tok, True)])
    else: parse(at + 1, slot + 1, cells + [(slot, dbbi[at], False)])
parse(0, 1, [])
summary = [(len(p), sum(c[2] for c in p), sum(c[2] and c[1] == 'b' for c in p), sum(c[2] and c[1] == 'be' for c in p)) for p in parses]
br = next(p for p in parses if len(p) == 84)
vals = [(-s if t == 'b' else s) if pr else ord(t) - 96 for s, t, pr in br]
sums = [sum(vals[r * 12 + c] for r in range(7)) for c in range(12)]
word = ''.join(chr(97 + v % 26) for v in sums)
assert word == 'hillfexmgsgq'
out['L2_prime_matrix'] = {'parses(cells,primes,b,be)': summary, 'values_84': vals, 'column_sums_7x12': sums, 'mod26_A0': word,
                          'assumptions': 'prime slots = b(-slot) / be(+slot); nonprime a..i = 1..9; row-major 7x12; sums mod 26 A=0'}

# L3. DBBI-keyed Bifid over FAED -> btcseed..., then Hill(FEXM->GSGQ) -> ifindo...
A = 'abcdefghiklmnopqrstuvwxyz'
sq = ''.join(dict.fromkeys(dbbi[:13] + A))
co = [v for ch in faed for v in divmod(sq.index(ch), 5)]
bif = ''.join(sq[5 * co[i] + co[i + len(faed)]] for i in range(len(faed)))   # Bifid decode, one block of 570
assert bif.startswith('btcseed')
rest = bif[7:]; carrier, four = rest[0::2], rest[1::2]
mod = lambda v, n=25: v % n
def inv(m):
    a, b_, c, d = m; det = mod(a * d - b_ * c); q = next(i for i in range(25) if mod(i * det) == 1)
    return [mod(q * d), mod(-q * b_), mod(-q * c), mod(q * a)]
def mul(x, y_):
    return [mod(x[0]*y_[0] + x[1]*y_[2]), mod(x[0]*y_[1] + x[1]*y_[3]), mod(x[2]*y_[0] + x[3]*y_[2]), mod(x[2]*y_[1] + x[3]*y_[3])]
M = lambda s: [A.index(s[0]), A.index(s[2]), A.index(s[1]), A.index(s[3])]
K = mul(M('gsgq'), inv(M('fexm'))); Ki = inv(K)
def hill(s, m):
    return ''.join(A[mod(m[0]*A.index(s[i]) + m[1]*A.index(s[i+1]))] + A[mod(m[2]*A.index(s[i]) + m[3]*A.index(s[i+1]))] for i in range(0, len(s), 2))
assert hill('fexm', K) == 'gsgq'
dec = hill(carrier, Ki); assert hill(dec, K) == carrier
out['L3_bifid_hill'] = {'square': sq, 'bifid_prefix': bif[:40], 'carrier_len': len(carrier), 'companion_len': len(four),
                        'companion_alphabet': ''.join(sorted(set(four))), 'K': K, 'K_inv': Ki, 'hill_decoded': dec,
                        'caveat': 'companion alphabet bcde is FORCED by the square (a..i all in rows 0-1); not evidence'}
(DATA / 'faed_bifid_570.txt').write_text(bif + '\n')
(DATA / 'hill_ifindo_282.txt').write_text(dec + '\n')

# L4. DBBI - VIC
diff = ''.join(chr(65 + (ord(a.upper()) - ord(c)) % 26) for a, c in zip(dbbi, vic))
tail = diff[27:]
out['L4_dbbi_minus_vic'] = {'diff': diff, 'tail64': tail, 'tail_A1Z26_digits': len(''.join(str(ord(ch) - 64) for ch in tail))}

# L5. DBBI as a substituted 64-hex digest: two-char prefixes b,g -> 64 tokens, 16 codes; b/g the only a..i pair
def tokens(s, pre):
    t, i = [], 0
    while i < len(s):
        n = 2 if s[i] in pre else 1
        if i + n > len(s): return None
        t.append(s[i:i + n]); i += n
    return t
pairs = [p + q for i, p in enumerate('abcdefghi') for q in 'abcdefghi'[i + 1:]]
ok = [p for p in pairs if (t := tokens(dbbi, p)) and len(t) == 64 and len(set(t)) == 16]
tk = tokens(dbbi, 'bg'); first = {}
pattern = ''.join('0123456789abcdef'[first.setdefault(x, len(first))] for x in tk)
assert ok == ['bg'] and pattern == '01234556728966286abc61c88b48de3086dd501d5557d6bab5605233df7bbb96'
out['L5_dbbi_hex_tokens'] = {'qualifying_prefix_pairs': ok, 'codes': sorted(set(tk)), 'equality_pattern': pattern,
                             'caveat': 'statistic chosen after looking; ~0.3% of letter-count-preserving shuffles give 64/16 for some pair'}

# L6. b positions in DBBI (1-based): the first five are the first five primes, the sixth is not
bpos = [i + 1 for i, ch in enumerate(dbbi) if ch == 'b']
assert bpos[:6] == [2, 3, 5, 7, 11, 14]
out['L6_dbbi_b_positions'] = {'b_positions_1based': bpos}

(DATA / 'leads_reproduced.json').write_text(json.dumps(out, indent=1) + '\n')
for k, v in out.items(): print(k, json.dumps({x: (y_ if not isinstance(y_, str) or len(y_) < 120 else y_[:120] + '...') for x, y_ in v.items() if x != 'values_84'}))
print('\nALL LEAD CALCULATIONS REPRODUCED (meaning unproven)')
