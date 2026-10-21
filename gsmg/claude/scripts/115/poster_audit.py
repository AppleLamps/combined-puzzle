"""Doc 115 s2 and s4: canvas geometry, 15-px lattice, QR re-encoding, 2x2 block sums as base-5."""
import collections
import numpy as np
from PIL import Image
import segno
from qrread import codewords, rs_ec
from lists_spiral import spiral

a = np.array(Image.open('data/puzzle.png').convert('RGB')).astype(int)
H, W = a.shape[:2]
G = np.load('data/grid.npy')

def trans(line):
    return [i for i in range(1, len(line)) if tuple(line[i]) != tuple(line[i - 1])]

print('canvas', W, 'x', H)
xs = collections.Counter(); ys = collections.Counter()
for y in range(0, 1047, 5): xs.update(trans(a[y, :]))
for x in range(0, 1047, 5): ys.update(trans(a[:1047, x]))
print('cell edges seen in >20 scan lines: x', sorted(k for k, v in xs.items() if v > 20),
      '| y', sorted(k for k, v in ys.items() if v > 20 and k < 1047))
print('right edge column x=1047:', collections.Counter(map(tuple, a[:1047, 1047])).most_common())
div = [y for y in range(1030, 1080) if (a[y, :1047] == [237, 28, 36]).all()]
print('divider rows', div[0], '-', div[-1], '(', len(div), 'px )')
print('bottom strip rows', [y for y in range(H - 6, H) if (a[y] == 255).all()])

# lower panel: white band, panel top edge, and any pixel outside the logo/title/QR/address boxes
print('white band rows', [y for y in range(1062, 1070) if (a[y] == 255).all()],
      '| panel top rows 1065-1066 white from x =', [int(np.argmax((a[y] == 255).all(1))) for y in (1065, 1066)])
BOXES = {'logo': (1100, 1260, 30, 180), 'title': (1150, 1220, 200, 1010), 'qr': (1285, 1525, 0, 240),
         'addr': (1380, 1430, 260, 1010)}
stray = collections.Counter()
for y in range(1067, H - 3):
    for x in np.nonzero(~(a[y] == 245).all(1))[0]:
        if not any(y0 <= y < y1 and x0 <= x < x1 for y0, y1, x0, x1 in BOXES.values()): stray[(y, int(x))] += 1
print('panel pixels (rows 1067 to', H - 4, ') outside the four boxes that differ from #F5F5F5:', len(stray))
# characterise the exempted boxes: these are anti-aliased raster, NOT reproduced pixel
# for pixel (no source font/logo). Report palette and grayscale share so the write-up
# can state what is and is not verified (Codex P1).
for name, (y0, y1, x0, x1) in (('logo', BOXES['logo']), ('title', BOXES['title']), ('addr', BOXES['addr'])):
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    cnt = collections.Counter(map(tuple, sub))
    gray = sum(v for k, v in cnt.items() if k[0] == k[1] == k[2]) / len(sub)
    print(f'  box {name}: {len(sub)} px, {len(cnt)} distinct colours, grayscale share {gray:.3f} '
          f'(anti-aliased raster; not reproduced pixel-for-pixel, not a data surface)')

# 15-px lattice: every pixel of every 15-px tile, bounded to the grid area (x, y < 1047),
# compared with its cell's colour
col = {(0, 0, 0): 'K', (255, 255, 255): 'W', (63, 72, 204): 'B', (255, 242, 0): 'Y', (254, 254, 254): 'F'}
GX = GY = 1047
nonuni = []; dev = collections.Counter(); devpx = 0; foreign = 0
for R in range(70):
    for C in range(70):
        tile = a[R * 15:min(R * 15 + 15, GY), C * 15:min(C * 15 + 15, GX)].reshape(-1, 3)
        cs = set(map(tuple, tile))
        if len(cs) > 1: nonuni.append((R, C))
        cell = G[R // 5][C // 5]
        for px in cs:
            if px not in col: foreign += 1
        bad = sum(1 for px in map(tuple, tile) if col.get(px) != cell)
        if bad:
            dev[(R // 5, C // 5)] += 1; devpx += bad
print('grid area', GX, 'x', GY, '| non-uniform 15-px tiles:', len(nonuni), '| pixels outside the five colours:', foreign)
print('tiles differing from their cell colour:', sum(dev.values()), 'in', len(dev), 'cells', dict(dev),
      '| differing pixels:', devpx, '=', devpx // 225, 'full tiles' if devpx % 225 == 0 else '(partial)')

# QR
x0, y0, m = 1, 1289, 7
Q = np.array([[1 if a[y0 + r * m + 3, x0 + c * m + 3].sum() < 384 else 0 for c in range(33)] for r in range(33)])
impure = sum(1 for r in range(33) for c in range(33)
             if 0 < (a[y0 + r * m:y0 + r * m + m, x0 + c * m:x0 + c * m + m].sum(2) < 384).sum() < m * m)
print('QR modules with mixed dark/light pixels (all 49 pixels checked per module):', impure)
url = 'https://www.blockchain.com/btc/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
bits = codewords(Q, 2)
cw = [int(''.join(map(str, bits[i:i + 8])), 2) for i in range(0, 800, 8)]
bs = ''.join(format(b, '08b') for b in cw[:80])
print('QR 33x33, dark modules', int(Q.sum()), '| RS parity valid', rs_ec(cw[:80], 20) == cw[80:],
      '| mode', bs[:4], 'ECI', int(bs[4:12], 2), 'then mode', bs[12:16], 'count', int(bs[16:24], 2))
for eci in (False, True):
    q = segno.make_qr(url, error='L', version=4, mask=2, mode='byte', eci=eci, encoding='utf-8', boost_error=False)
    M = np.array([[1 if v else 0 for v in row] for row in q.matrix])
    print(f'  segno reference eci={eci}: modules differing = {(M != Q).sum()}')

# 2x2 block sums -> 7x7 base-5 digits
for fv in (0, 1):
    Mb = np.array([[1 if x in 'KB' or (x == 'F' and fv) else 0 for x in row] for row in G])
    B2 = Mb.reshape(7, 2, 7, 2).sum(axis=(1, 3))
    orders = {'row': [(r, c) for r in range(7) for c in range(7)], 'col': [(r, c) for c in range(7) for r in range(7)],
              'spiral': spiral(7)}
    for on, o in orders.items():
        for rev in (False, True):
            d = [int(B2[r, c]) for r, c in o][::-1 if rev else 1]
            n = 0
            for v in d: n = n * 5 + v
            h = format(n, 'x'); h = '0' * (len(h) % 2) + h
            b = bytes.fromhex(h)
            pr = sum(32 <= x < 127 for x in b) / len(b)
            print(f'  F={fv} {on:6} rev={rev!s:5} -> {len(b)} bytes, printable {pr:.2f}')
