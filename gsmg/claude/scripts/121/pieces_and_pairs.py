#!/usr/bin/env python3
"""Doc 121: the three cheapest untried items of doc 120 s6.
 1. faed's pieces under encodings other than rule 2
 2. Hill 3x3 on faed with keys the poster supplies
 3. the two 96-byte containers as one object (swapped salts, cross IV, chained)
"""
import collections, hashlib, itertools, math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '115')); sys.path.insert(0, os.path.join(HERE, '..', '119'))
import harness as H
from Crypto.Cipher import AES
D = os.path.join(HERE, '..', '115', 'data')
soup = open(os.path.join(D, 'soup.txt')).read(); faed = soup[195:765]; dbbi = soup[:91]
arch = open(os.path.join(D, 'architect.txt')).read(); chk = open(os.path.join(D, 'checker.txt')).read()
intro = ''.join(c for c in open(os.path.join(D, 'intro.txt')).read().lower() if c.isalpha())
PIECES = {'p1': faed[0:220], 'p2': faed[220:435], 'p3': faed[435:540], 'p4': faed[540:570], 'tail32': faed[538:570],
          'w1': faed[0:250], 'w2': faed[250:315], 'w3': faed[315:405], 'w4': faed[405:465], 'w5': faed[465:540], 'all': faed}
FREQ = {'e':12.7,'t':9.1,'a':8.2,'o':7.5,'i':7.0,'n':6.7,'s':6.3,'h':6.1,'r':6.0,'d':4.3,'l':4.0,'c':2.8,'u':2.8,'m':2.4,'w':2.4,'f':2.2,'g':2.0,'y':2.0,'p':1.9,'b':1.5,'v':1.0,'k':0.8,'j':0.15,'x':0.15,'q':0.1,'z':0.07}
LF = {c: math.log(v / 100) for c, v in FREQ.items()}
def eng(s): return sum(LF.get(c, -9) for c in s) / max(1, len(s))
def printable(b): return sum(32 <= c < 127 for c in b) / max(1, len(b))
def tobytes(n):
    h = hex(n)[2:]; h = '0' + h if len(h) % 2 else h; return bytes.fromhex(h)
def bij9(s):  # bijective base 9, digits 1..9
    n = 0
    for c in s: n = n * 9 + (ord(c) - 96)
    return n

print('== 1. pieces under other encodings ==')
r = random.Random(121)
null = sorted(printable(tobytes(bij9(''.join(r.choice('abcdefghi') for _ in range(220))))) for _ in range(300))
print(f'   null printable for 220 bijective-9 digits: median {null[150]:.2f} max {null[-1]:.2f}')
scalars = []
for name, p in PIECES.items():
    for lab, s in (('fwd', p), ('rev', p[::-1])):
        n = bij9(s); b = tobytes(n)
        scalars.append((f'{name}|{lab}|bij9', (n % H.N).to_bytes(32, 'big')))
        scalars.append((f'{name}|{lab}|bij9-low256', (n & ((1 << 256) - 1)).to_bytes(32, 'big')))
        print(f'   {name:6s} {lab} bijective-9: {len(b):3d} bytes printable {printable(b):.2f} {b[:16]!r}')
    # A1Z26 with the dominant letter as separator
    dom = collections.Counter(p).most_common(1)[0][0]
    groups = [g for g in p.split(dom) if g]
    nums = [int(''.join(str(ord(c) - 96) for c in g)) for g in groups]
    letters = ''.join(chr(96 + n) for n in nums if 1 <= n <= 26)
    print(f'   {name:6s} A1Z26 split on {dom}: {len(groups)} groups, {len(letters)} in range: {letters[:60]!r}  eng {eng(letters):.2f}')
    # as keystream mod 26 over three texts (key a..i = 0..8 and 1..9), both directions
    for tname, text in (('arch', arch), ('chk', chk), ('intro', intro)):
        best = None
        for kmap in (0, 1):
            for op in ('sub', 'add'):
                out = ''.join(chr(97 + ((ord(t) - 97 - (ord(p[i % len(p)]) - 97 + kmap)) % 26 if op == 'sub' else (ord(t) - 97 + (ord(p[i % len(p)]) - 97 + kmap)) % 26)) for i, t in enumerate(text[:len(p)]))
                sc = eng(out)
                if best is None or sc > best[0]: best = (sc, kmap, op, out[:50])
        print(f'   {name:6s} keystream over {tname}: best eng {best[0]:.2f} ({best[1]},{best[2]}) {best[3]!r}')
print('   english baseline eng(arch) = %.2f; random letters = %.2f' % (eng(arch), eng(''.join(r.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(500)))))
hits = [lab for lab, k in scalars if 0 < int.from_bytes(k, 'big') < H.N and H.key_hits(k)]
print('   pieces as raw scalars (mod N and low 256 bits):', len(scalars), 'tested, hits', hits)

print('== 2. Hill 3x3 on faed with poster keys ==')
sp = ("0110011101110011011011010110011100101110011010010110111100101111" "0111010001101000011001010111001101100101011001010110010001101001"
      "0111001101110000011011000110000101101110011101000110010101100100" "0000")
n = 14; grid = [[None] * n for _ in range(n)]; top = left = 0; bottom = right = n - 1; k = 0
while k < n * n and left <= right and top <= bottom:
    for rr in range(top, bottom + 1): grid[rr][left] = int(sp[k]); k += 1
    for cc in range(left + 1, right + 1): grid[bottom][cc] = int(sp[k]); k += 1
    if left < right:
        for rr in range(bottom - 1, top - 1, -1): grid[rr][right] = int(sp[k]); k += 1
    if top < bottom:
        for cc in range(right - 1, left, -1): grid[top][cc] = int(sp[k]); k += 1
    left += 1; right -= 1; top += 1; bottom -= 1
rows = [sum(rw) for rw in grid]; cols = [sum(grid[i][j] for i in range(n)) for j in range(n)]
keys = set()
for i in range(12):
    for j in range(12): keys.add(tuple(grid[i + a][j + b] for a in range(3) for b in range(3)))
for lst in (rows, cols, rows + cols):
    for i in range(len(lst) - 8): keys.add(tuple(lst[i:i + 9]))
for perm in itertools.permutations([2, 5, 7]):
    keys.add(tuple(perm) * 3); keys.add(tuple(x for x in perm for _ in range(3)))
keys.add((2, 5, 7, 5, 7, 2, 7, 2, 5)); keys.add((1, 4, 21, 4, 21, 1, 21, 1, 4)); keys.add((1, 0, 0, 0, 1, 0, 0, 0, 1))
def inv3(K, m):
    a, b, c, d, e, f, g, h, i = K
    det = (a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)) % m
    if math.gcd(det, m) != 1: return None
    di = pow(det, -1, m)
    adj = [(e * i - f * h), -(b * i - c * h), (b * f - c * e), -(d * i - f * g), (a * i - c * g), -(a * f - c * d), (d * h - e * g), -(a * h - b * g), (a * e - b * d)]
    return tuple((x * di) % m for x in adj)
def apply(K, digits, m):
    out = []
    for i in range(0, len(digits) - 2, 3):
        x, y, z = digits[i:i + 3]
        out += [(K[0] * x + K[1] * y + K[2] * z) % m, (K[3] * x + K[4] * y + K[5] * z) % m, (K[6] * x + K[7] * y + K[8] * z) % m]
    return out
res = []
for m in (9, 10, 26):
    digs = [(ord(c) - 97) % m for c in faed]
    for K in keys:
        for KK in (K, inv3(K, m)):
            if KK is None: continue
            out = apply(KK, digs, m)
            if m == 26:
                s = ''.join(chr(97 + v) for v in out); res.append((eng(s), 'eng', m, K, s[:40]))
            else:
                b = tobytes(int(''.join(str(v) for v in out))); res.append((printable(b), 'pr', m, K, b[:20]))
res.sort(reverse=True)
print('   keys', len(keys), '; top results:')
for x in res[:6]: print('   ', f'{x[0]:.2f} {x[1]} mod{x[2]} K={x[3]} {x[4]!r}')
print('   null: mod26 random eng ~ -3.4; mod9/10 printable median ~0.37')

print('== 3. the two containers as one object ==')
from pbkdf2_sweep import tier_a
S = H.CONTAINERS['salshort']; T = H.CONTAINERS['terminal']; C = H.CONTAINERS['cosmic']
synth = {'S_ct+T_salt': b'Salted__' + T[8:16] + S[16:], 'T_ct+S_salt': b'Salted__' + S[8:16] + T[16:],
         'C_ct+S_salt': b'Salted__' + S[8:16] + C[16:], 'C_ct+T_salt': b'Salted__' + T[8:16] + C[16:],
         'S_then_T': b'Salted__' + S[8:16] + S[16:] + T[16:], 'T_then_S': b'Salted__' + T[8:16] + T[16:] + S[16:],
         'S_saltXORT': b'Salted__' + bytes(a ^ b for a, b in zip(S[8:16], T[8:16])) + S[16:],
         'T_saltXORS': b'Salted__' + bytes(a ^ b for a, b in zip(S[8:16], T[8:16])) + T[16:]}
items = tier_a(); st = H.Stats(); dec = 0; flags = []
for lab, cand in items:
    b = cand.encode() if isinstance(cand, str) else cand
    for prof, pw in H.pw_forms(b):
        for md in ('sha256', 'md5'):
            k, iv = H.evp(pw, S[8:16], H.MDS[md]); k2, iv2 = H.evp(pw, T[8:16], H.MDS[md])
            for name, raw in synth.items():
                dec += 1; r_ = H.try_open(raw, pw, md, full=True)
                if r_:
                    pad, pt = r_; why = H.recognise(pt, pad)
                    if why: flags.append((name, prof, md, pad, why, lab, cand[:40] if isinstance(cand, str) else cand[:40]))
            # cross IV: decrypt S's ciphertext with key from S's salt but IV = T's first block, and vice versa
            for name, ct, key, ivx in (('S_ivT', S[16:], k, T[16:32]), ('T_ivS', T[16:], k2, S[16:32]), ('S_key_T_salt_ivT', S[16:], k2, T[16:32])):
                dec += 1; pt = AES.new(key, AES.MODE_CBC, ivx).decrypt(ct); p = pt[-1]
                if 1 <= p <= 16 and pt[-p:] == bytes([p]) * p:
                    why = H.recognise(pt[:-p], p)
                    if why: flags.append((name, prof, md, p, why, lab, str(cand)[:40]))
print(f'   candidates {len(items)} decrypts {dec} flags {len(flags)} (expected valid pads ~{dec/256:.0f}; flags are recogniser hits only)')
for f in flags: print('   FLAG', f)
