#!/usr/bin/env python3
"""Direct checks on puzzle.png (the GSMG poster), each with a planted control.
Usage: python3 photo_checks.py /path/to/puzzle.png
Needs pillow and numpy. Prints one line per check."""
import sys, struct, hashlib, random
from collections import Counter, deque
import numpy as np
from PIL import Image

P = sys.argv[1]
raw = open(P, 'rb').read()
print('sha256', hashlib.sha256(raw).hexdigest(), len(raw), 'bytes')

# 1. chunks and trailing bytes
i, chunks = 8, []
while i < len(raw):
    n, = struct.unpack('>I', raw[i:i+4]); chunks.append((raw[i+4:i+8].decode(), n)); i += 12 + n
print('1 chunks', chunks, '| bytes after IEND:', len(raw) - i)

img = np.array(Image.open(P)); rgb = img[:, :, :3].astype(int)
print('  alpha values', dict(Counter(img[:, :, 3].ravel().tolist())))

# 2. hidden-mark scan below the divider: every pixel that is not the flat
#    #F5F5F5 panel, grouped into components. Control: plant one #F4F4F4 pixel.
def components(region, bg=245):
    m = np.any(region != bg, axis=2); H, W = m.shape
    lab = np.zeros(m.shape, bool); out = []
    for y, x in zip(*np.nonzero(m)):
        if lab[y, x]: continue
        q = deque([(y, x)]); lab[y, x] = True; box = [y, y, x, x]; c = 0
        while q:
            cy, cx = q.popleft(); c += 1
            box = [min(box[0], cy), max(box[1], cy), min(box[2], cx), max(box[3], cx)]
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    ny, nx = cy+dy, cx+dx
                    if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = True; q.append((ny, nx))
        out.append((c, *box))
    return out
low = rgb[1067:1553].copy()
comps = components(low)
zones = {'logo': (1105, 1260, 40, 170), 'title': (1165, 1210, 210, 1000), 'qr': (1285, 1525, 0, 240), 'address': (1388, 1430, 270, 1000)}
def zone(c):
    y0, y1, x0, x1 = c[1]+1067, c[2]+1067, c[3], c[4]
    return next((k for k, (a, b, l, r) in zones.items() if a <= y0 and y1 <= b and l <= x0 and x1 <= r), 'OUTSIDE')
print('2 components below divider:', len(comps), dict(Counter(zone(c) for c in comps)))
ctl = low.copy(); ctl[300, 600] = 244
extra = [c for c in components(ctl) if c not in comps]
print('  control (one #F4F4F4 pixel planted): found', extra)

# 3. grid region palette (rows 0..1046)
print('3 grid palette', len(Counter(map(tuple, rgb[:1047].reshape(-1, 3).tolist()))), 'colours')

# 4. logo LSB structure: horizontal LSB transitions inside the logo box.
#    Control: overwrite the logo's blue-channel LSBs with a random payload.
L = rgb[1105:1260, 40:170]
def trans(a): return int((np.diff(a & 1, axis=1) != 0).sum())
rnd = L.copy(); random.seed(1)
rnd[:, :, 2] = (rnd[:, :, 2] & ~1) | np.array([[random.getrandbits(1) for _ in range(L.shape[1])] for _ in range(L.shape[0])])
print('4 logo LSB horizontal transitions:', trans(L), '| control with random LSB payload:', trans(rnd))

# 5. QR at codeword level: unmask, read 100 codewords, parse segments, recompute RS.
g = rgb[:, :, 0]; N = 33
M = np.array([[1 if g[1289+7*r+3, 1+7*c+3] < 128 else 0 for c in range(N)] for r in range(N)])
impure = sum(int(((g[1289+7*r:1296+7*r, 1+7*c:8+7*c] < 128) != M[r, c]).sum()) for r in range(N) for c in range(N))
F = np.zeros((N, N), bool)
F[0:9, 0:9] = F[0:9, N-8:] = F[N-8:, 0:9] = True; F[6, :] = F[:, 6] = True; F[24:29, 24:29] = True
fmt = [M[8, c] for c in (0, 1, 2, 3, 4, 5, 7, 8)] + [M[r, 8] for r in (7, 5, 4, 3, 2, 1, 0)]
fb = int(''.join(map(str, fmt)), 2) ^ 0b101010000010010
ecl, mask = 'MLHQ'[fb >> 13], (fb >> 10) & 7
assert mask == 2
exp = [0]*512; log = [0]*256; x = 1
for k in range(255):
    exp[k] = x; log[x] = k; x <<= 1
    if x & 256: x ^= 0x11d
for k in range(255, 512): exp[k] = exp[k-255]
mul = lambda a, b: 0 if a == 0 or b == 0 else exp[log[a]+log[b]]
gen = [1]
for k in range(20):
    ng = [0]*(len(gen)+1)
    for j, c in enumerate(gen): ng[j] ^= c; ng[j+1] ^= mul(c, exp[k])
    gen = ng
def read(Mx):
    bits = []; c = N-1; up = True
    while c > 0:
        if c == 6: c -= 1
        for r in (range(N-1, -1, -1) if up else range(N)):
            for cc in (c, c-1):
                if not F[r, cc]: bits.append(Mx[r, cc] ^ (1 if cc % 3 == 0 else 0))
        up = not up; c -= 2
    cw = [int(''.join(map(str, bits[i:i+8])), 2) for i in range(0, 800, 8)]
    data, ec = cw[:80], cw[80:]
    rem = list(data) + [0]*20
    for k in range(80):
        f = rem[k]
        if f:
            for j in range(1, 21): rem[k+j] ^= mul(gen[j], f)
    return data, rem[80:] == ec, bits[800:]
data, ok, remainder = read(M)
s = ''.join(f'{b:08b}' for b in data)
eci = int(s[4:12], 2); n = int(s[16:24], 2)
payload = bytes(int(s[24+8*k:32+8*k], 2) for k in range(n)); end = 24 + 8*n
print(f'5 QR v4-{ecl} mask {mask}, impure pixels {impure}; mode {s[0:4]} ECI {eci}; byte mode {s[12:16]} len {n}: {payload.decode()}')
print('  terminator', s[end:end+4], '| bytes after:', bytes(data[(end+4+7)//8:]).hex(), '| remainder bits', remainder, '| RS parity matches data:', ok)
M2 = M.copy(); M2[20, 20] ^= 1
print('  control (one data module flipped): RS parity matches:', read(M2)[1])

# 6. glyph determinism: the three G's of the title are pixel-identical renders
G = [rgb[1168:1206, x0-1:x0+31] for x0 in (215, 320, 936)]
print('6 title G glyphs identical:', all((G[0] == k).all() for k in G))
