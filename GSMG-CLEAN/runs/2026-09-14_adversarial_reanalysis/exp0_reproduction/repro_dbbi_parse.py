"""Independent reproduction of the poster spiral, DBBI 83/84 parse, colour-prime sums and 7x12 column sums.
Uses only originals/poster/puzzle.png and data/DBBI_91.txt. Writes repro_dbbi_parse.json.
Written 2026-09-14 for the adversarial reanalysis; does not import any workspace tool."""
import json
from collections import Counter
from PIL import Image

ROOT = 'E:/rabbit-combined/GSMG-CLEAN/'
im = Image.open(ROOT + 'originals/poster/puzzle.png').convert('RGB')
W, H = im.size
cell = W / 14
grid = [[None] * 14 for _ in range(14)]
for r in range(14):
    for c in range(14):
        box = im.crop((round(c * cell)+3, round(r * cell)+3, round((c + 1) * cell)-3, round((r + 1) * cell)-3))
        modal, cnt = Counter(box.getdata()).most_common(1)[0]
        grid[r][c] = (modal, cnt / (box.size[0]*box.size[1]))


def cls(rgb):
    R, G, B = rgb
    if (R, G, B) == (0, 0, 0):
        return 'K'
    if (R, G, B) == (255, 255, 255):
        return 'W'
    if B > 150 and R < 120:
        return 'B'
    if R > 200 and G > 200 and B < 100:
        return 'Y'
    return 'O'  # anything else (off-white etc.)


col = [[cls(grid[r][c][0]) for c in range(14)] for r in range(14)]
odd = [(r, c, grid[r][c]) for r in range(14) for c in range(14) if col[r][c] == 'O']
print('image', W, H, 'cell', cell)
print('non-pure cells:', odd)
for row in col:
    print(''.join(row))


def spirals():
    dirs_cw = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dirs_ccw = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    corners = {'TL': (0, 0), 'TR': (0, 13), 'BR': (13, 13), 'BL': (13, 0)}
    for cname, (r0, c0) in corners.items():
        for cw, dirs in [(True, dirs_cw), (False, dirs_ccw)]:
            for di in range(4):
                dr, dc = dirs[di]
                if not (0 <= r0 + dr < 14 and 0 <= c0 + dc < 14):
                    continue
                seen = set()
                out = []
                rr, cc, d = r0, c0, di
                while True:
                    out.append((rr, cc))
                    seen.add((rr, cc))
                    dr, dc = dirs[d]
                    if not (0 <= rr + dr < 14 and 0 <= cc + dc < 14 and (rr + dr, cc + dc) not in seen):
                        d = (d + 1) % 4
                        dr, dc = dirs[d]
                        if not (0 <= rr + dr < 14 and 0 <= cc + dc < 14 and (rr + dr, cc + dc) not in seen):
                            break
                    rr, cc = rr + dr, cc + dc
                if len(out) == 196:
                    yield cname, cw, di, out
                    yield cname+'-rev', cw, di, out[::-1]


found = []
import itertools
for cname, cw, di, order in spirals():
    for ones in itertools.chain.from_iterable(itertools.combinations('KWBYO', k) for k in range(1, 5)):
        bits = ''.join(('1' if col[r][c] in ones else '0') for r, c in order)
        by = bytes(int(bits[i:i + 8], 2) for i in range(0, 192, 8))
        if b'gsmg.io' in by:
            found.append((cname, cw, di, ''.join(ones), order, by, bits[192:]))
            print('SPIRAL', cname, cw, di, 'ones=', ''.join(ones), by, 'tail bits', bits[192:])
# keep only the minimal one-set (a superset that adds colours absent from the grid is equivalent)
assert found, 'no spiral reproduces the URL'
cname, cw, di, blackbit, order, urlbytes, tail = found[0]
ref = open(ROOT + 'data/poster_spiral_bits.txt').read().split()[0]
mybits = ''.join(('1' if col[r][c] in blackbit else '0') for r, c in order)
print('matches data/poster_spiral_bits.txt:', mybits == ref)

marks = [(i, r, c, col[r][c]) for i, (r, c) in enumerate(order) if col[r][c] in 'BYO']
print('coloured cells along spiral (spiral idx,row,col,colour):', marks, 'count', len(marks))
poster = ''.join(m[3] for m in marks)
print('colour string', poster)

dbbi = open(ROOT + 'data/DBBI_91.txt').read().strip()
assert len(dbbi) == 91


def isprime(n):
    return n > 1 and all(n % p for p in range(2, int(n ** .5) + 1))


def parses(s):
    """Every parse in which prime logical slots hold b or be and other slots hold one character."""
    out = []

    def rec(i, slot, cells):
        if i == len(s):
            out.append(list(cells))
            return
        if isprime(slot):
            if s[i] != 'b':
                return
            cells.append((slot, i, i + 1, 'b'))
            rec(i + 1, slot + 1, cells)
            cells.pop()
            if i + 1 < len(s) and s[i + 1] == 'e':
                cells.append((slot, i, i + 2, 'be'))
                rec(i + 2, slot + 1, cells)
                cells.pop()
        else:
            cells.append((slot, i, i + 1, s[i]))
            rec(i + 1, slot + 1, cells)
            cells.pop()

    rec(0, 1, [])
    return out


P = parses(dbbi)
print('number of consistent prime-slot parses of DBBI:', len(P))
primes = [p for p in range(2, 500) if isprime(p)]

# per-URL-byte rule (84-model): one regular colour per byte, XOR with off-white presence
bytes_marks = [[m for m in marks if m[0] // 8 == b] for b in range(24)]
print('coloured cells per URL byte:', [''.join(m[3] for m in bm) for bm in bytes_marks])
pb = []
for bm in bytes_marks:
    reg = [m for m in bm if m[3] in 'BY']
    off = [m for m in bm if m[3] == 'O']
    if reg:
        assert len(reg) == 1, bm
        ccol = reg[0][3]
        if off:
            ccol = {'B': 'Y', 'Y': 'B'}[ccol]
        pb.append(ccol)
    elif off:
        pb.append('?')
pb = ''.join(pb)
print('84 per-byte marker string', pb, len(pb))
p83 = poster.replace('O', 'B')
print('83 serial marker string (O as B)', p83, len(p83))

res = []
for cells in P:
    n = cells[-1][0]
    toks = [t for s, _, _, t in cells if isprime(s)]
    payload = ''.join(t for s, _, _, t in cells if not isprime(s))
    tokcol = ''.join('Y' if t == 'be' else 'B' for t in toks)
    d = dict(cells=n, prime_tokens=len(toks), payload=payload, payload_len=len(payload), token_colours=tokcol,
             match_serial83_prefix=(p83.startswith(tokcol)), serial83_unused=p83[len(tokcol):],
             match_perbyte84_prefix=(pb.startswith(tokcol)), perbyte84_unused=pb[len(tokcol):])
    # colour prime sums under this parse's own token string
    d['yellow_prime_sum'] = sum(primes[i] for i, ch in enumerate(tokcol) if ch == 'Y')
    d['blue_prime_sum'] = sum(primes[i] for i, ch in enumerate(tokcol) if ch == 'B')
    # signed values; column/row sums at exact factor shapes
    vals = []
    for s, _, _, t in cells:
        v = 2 if t == 'be' else ord(t[0]) - 96
        vals.append(-v if isprime(s) else v)
    d['signed_values'] = vals
    # workspace 'L2' convention: prime slots hold the slot number, b -> -slot, be -> +slot; a..i = 1..9; mod 26 with A=0
    vals2 = [((-s if t == 'b' else s) if isprime(s) else ord(t) - 96) for s, _, _, t in cells]
    d['L2_values'] = vals2
    d['L2_shapes'] = {}
    for R in range(1, n + 1):
        if n % R:
            continue
        C = n // R
        cols = [sum(vals2[r * C + c] for r in range(R)) for c in range(C)]
        rows = [sum(vals2[r * C + c] for c in range(C)) for r in range(R)]
        d['L2_shapes'][f'{R}x{C}'] = dict(colsums=cols, col_mod26_A0=''.join(chr(97 + x % 26) for x in cols),
                                          rowsums=rows, row_mod26_A0=''.join(chr(97 + x % 26) for x in rows))
    d['shapes'] = {}
    for R in range(1, n + 1):
        if n % R:
            continue
        C = n // R
        cols = [sum(vals[r * C + c] for r in range(R)) for c in range(C)]
        rows = [sum(vals[r * C + c] for c in range(C)) for r in range(R)]
        L = lambda x: chr((x - 1) % 26 + 65)
        d['shapes'][f'{R}x{C}'] = dict(colsums=cols, col_letters=''.join(L(x) for x in cols),
                                       rowsums=rows, row_letters=''.join(L(x) for x in rows))
    res.append(d)
    print(n, len(toks), payload, len(payload), tokcol, 'serial83pfx', d['match_serial83_prefix'], 'perbyte84pfx', d['match_perbyte84_prefix'],
          'Y', d['yellow_prime_sum'], 'B', d['blue_prime_sum'])
    for k, v in d['L2_shapes'].items():
        if 5 <= int(k.split('x')[0]) <= 15:
            print('    L2', k, v['col_mod26_A0'], v['row_mod26_A0'])
    print('    serial83 prefix match', d['match_serial83_prefix'], 'unused', d['serial83_unused'],
          '| perbyte84 prefix match', d['match_perbyte84_prefix'], 'unused', d['perbyte84_unused'])
# L1: poster-only colour sums: the 24 regular coloured cells against the first 24 primes (off-white ignored)
reg24 = poster.replace('O', '')
L1 = dict(regular_marker_string=reg24, yellow=sum(primes[i] for i, ch in enumerate(reg24) if ch == 'Y'),
          blue=sum(primes[i] for i, ch in enumerate(reg24) if ch == 'B'), total=sum(primes[:24]))
print('L1 poster colour-prime sums (24 regular cells vs primes 2..89):', L1)

json.dump(dict(spiral=dict(corner=cname, clockwise=cw, start_dir=di, black_bit=blackbit, url=urlbytes.decode('latin1'),
                           tail_bits=tail),
               grid=[''.join(r) for r in col],
               nonpure=[(r, c, list(g[0]), g[1]) for r, c, g in odd], marks=marks, poster_colour_string=poster,
               serial83_markers=p83, perbyte84_markers=pb, L1=L1, parses=res),
          open('repro_dbbi_parse.json', 'w'), indent=1)
print('wrote repro_dbbi_parse.json')
