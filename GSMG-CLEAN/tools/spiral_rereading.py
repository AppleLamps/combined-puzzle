"""Reading 1 of 18 section 2: "follow the white rabbit" as the last step means doing the first step
again, reading a grid of two-valued cells along the poster's spiral.

  python tools/spiral_rereading.py runs/2026-11-10_spiral_rereading

Grids read: the poster under every other spiral convention, the rabbit drawing at its own 15 pixel
resolution, and the page's a..i material reduced to two values by the poster's own colour rule
(odd = blue = 1, even = yellow = 0) and laid out in every exact rectangle.  No envelope is read and
nothing is decrypted.  The run refuses to start unless its statement is sealed.
"""
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prereg  # noqa: E402

SEED = 20261110
URLISH = re.compile(r'[a-z./]+')
CORNERS = ('tl', 'tr', 'br', 'bl')


def spiral(rows, cols, start, ccw):
    """Cell order of an inward spiral from a corner.  ('tl', True) is the poster's own reading."""
    clockwise = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    corner = {'tl': (0, 0), 'tr': (0, cols - 1), 'br': (rows - 1, cols - 1), 'bl': (rows - 1, 0)}[start]
    if ccw:
        first = {'tl': 1, 'bl': 0, 'br': 3, 'tr': 2}[start]
        order = [clockwise[(first - k) % 4] for k in range(4)]
    else:
        first = {'tl': 0, 'tr': 1, 'br': 2, 'bl': 3}[start]
        order = [clockwise[(first + k) % 4] for k in range(4)]
    seen = [[False] * cols for _ in range(rows)]
    r, c = corner
    d, out = 0, []
    for _ in range(rows * cols):
        out.append((r, c))
        seen[r][c] = True
        nr, nc = r + order[d][0], c + order[d][1]
        if not (0 <= nr < rows and 0 <= nc < cols) or seen[nr][nc]:
            d = (d + 1) % 4
            nr, nc = r + order[d][0], c + order[d][1]
        r, c = nr, nc
    return out


def to_text(bits, width):
    out = []
    for i in range(0, len(bits) - width + 1, width):
        v = 0
        for b in bits[i:i + width]:
            v = v * 2 + b
        out.append(chr(v) if 32 <= v < 127 else '\x00')
    return ''.join(out)


def longest_run(text):
    """Longest stretch of lowercase letters, dot and slash: the alphabet of the poster's own answer."""
    return max((len(m) for m in URLISH.findall(text)), default=0)


def shapes(n):
    return [(r, n // r) for r in range(2, n // 2 + 1) if n % r == 0]


def readings(bits, rows, cols):
    """Every reading of one grid: 8 spirals, inward and outward, 8-bit and 7-bit characters."""
    grid = [bits[r * cols:(r + 1) * cols] for r in range(rows)]
    for start in CORNERS:
        for ccw in (True, False):
            seq = [grid[r][c] for r, c in spiral(rows, cols, start, ccw)]
            for outward in (False, True):
                s = seq[::-1] if outward else seq
                for width in (8, 7):
                    yield {'start': start, 'ccw': ccw, 'outward': outward, 'width': width}, to_text(s, width)


def best_of(bits):
    best = (0, None)
    for rows, cols in shapes(len(bits)):
        for how, text in readings(bits, rows, cols):
            run = longest_run(text)
            if run > best[0]:
                m = max(URLISH.findall(text), key=len)
                best = (run, dict(how, rows=rows, cols=cols, text=m))
    return best


def poster():
    from PIL import Image
    im = Image.open(ROOT / 'originals' / 'poster' / 'puzzle.png').convert('RGB')
    px = im.load()
    black, blue = (0, 0, 0), (63, 72, 204)

    def modal(x0, y0, w):
        return Counter(px[x, y] for y in range(y0, y0 + w) for x in range(x0, min(x0 + w, im.size[0]))).most_common(1)[0][0]

    cells = [1 if modal(c * 75, r * 75, 75) in (black, blue) else 0 for r in range(14) for c in range(14)]
    fine = [[1 if modal(c * 15, r * 15, 15) == black else 0 for c in range(70)] for r in range(70)]
    nest = [fine[r][c] for r in range(30, 40) for c in range(30, 40)]         # the four centre cells
    rabbit = [fine[r][c] for r in range(30, 45) for c in range(30, 50)]       # the drawing's bounding box
    return cells, nest, rabbit


def objects():
    data = ROOT / 'data'
    dbbi = (data / 'DBBI_91.txt').read_text().strip()
    faed = (data / 'FAED_570.txt').read_text().strip()
    run = (data / 'salphaseion_compact_1075.txt').read_text().strip()[:765]
    parity = lambda s: [(ord(ch) - 96) & 1 for ch in s]                       # noqa: E731  odd = 1, as blue is odd
    high = lambda s: [1 if ord(ch) - 96 >= 5 else 0 for ch in s]              # noqa: E731
    cells, nest, rabbit = poster()
    return {
        'poster_14x14': cells, 'nest_10x10_fine': nest, 'rabbit_15x20_fine': rabbit,
        'faed_parity': parity(faed), 'faed_high': high(faed),
        'dbbi_parity': parity(dbbi), 'dbbi_high': high(dbbi),
        'whole_run_765_parity': parity(run),
        'faed_is_g': [1 if ch == 'g' else 0 for ch in faed],
    }


def main(run_dir):
    run = Path(run_dir)
    seal = prereg.verify(run)
    rnd = random.Random(SEED)
    objs = objects()
    # the poster's own reading must come back, and only once
    known = [(how, text) for how, text in readings(objs['poster_14x14'], 14, 14)
             if 'gsmg.io/theseedisplanted' in text]
    # planted control: a sentence written along the poster's spiral into a 19 x 30 grid
    message = 'thelaststepisthefirststepfollowthewhiterabbittothecentreofthegridandread'[:71]
    planted_bits = [int(b) for ch in message for b in f'{ord(ch):08b}'] + [0, 0]
    grid = [[0] * 30 for _ in range(19)]
    for bit, (r, c) in zip(planted_bits, spiral(19, 30, 'tl', True)):
        grid[r][c] = bit
    planted_run, planted_how = best_of([b for row in grid for b in row])
    out = {'prereg_sha256': seal, 'objects': {}, 'known_reading_recovered': len(known),
           'planted_control': {'run': planted_run, 'found': planted_how, 'passed': planted_run >= 60}}
    passed = False
    for name, bits in objs.items():
        if name == 'poster_14x14':
            others = [(longest_run(t), dict(h, text=max(URLISH.findall(t) or [''], key=len)))
                      for h, t in readings(bits, 14, 14) if 'gsmg.io/theseedisplanted' not in t]
            real = max(others, key=lambda x: x[0])
        else:
            real = best_of(bits)
        ctl = []
        shuffled = list(bits)
        for _ in range(60):
            rnd.shuffle(shuffled)
            ctl.append(best_of(shuffled)[0])
        ctl.sort()
        out['objects'][name] = {'cells': len(bits), 'ones': sum(bits), 'shapes': len(shapes(len(bits))),
                                'best_run': real[0], 'best': real[1],
                                'control_median': ctl[len(ctl) // 2], 'control_max': ctl[-1]}
        passed |= real[0] >= 12 and real[0] > ctl[-1]
    out['acceptance'] = 'a run of 12 or more URL characters that also exceeds every shuffle of the same object'
    out['outcome'] = 'passed' if passed else 'null'
    (run / 'results.json').write_text(json.dumps(out, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({k: out[k] for k in ('known_reading_recovered', 'planted_control', 'outcome')}, indent=1))
    for name, o in out['objects'].items():
        print(f"{name:24s} cells {o['cells']:4d} shapes {o['shapes']:2d} best run {o['best_run']:2d} "
              f"control median {o['control_median']} max {o['control_max']} | {o['best'] and o['best'].get('text')}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
