import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image
from collections import Counter
import lib

PASS=[]; FAIL=[]
def check(name, cond, detail=''):
    (PASS if cond else FAIL).append(name)
    print(('PASS ' if cond else 'FAIL '), name, ' ', detail)

im = Image.open(str(Path(__file__).resolve().parent.parent.parent / 'source' / 'poster' / 'puzzle.png')).convert('RGB')
W, H = im.size
check('poster size 1048x1556', (W,H)==(1048,1556), (W,H))

CELL = 75
GRID = 14
# sample the whole cell (mode color) rather than a single pixel, robust to the 1048 vs 1050 rounding
def cell_box(r, c):
    x0 = round(c * W_over_grid); x1 = round((c+1) * W_over_grid)
    y0 = r*CELL; y1 = (r+1)*CELL
    return x0, y0, x1, y1

W_over_grid = W / GRID  # ~74.857
colors = {}
for r in range(GRID):
    for c in range(GRID):
        x0,y0,x1,y1 = cell_box(r,c)
        region = im.crop((x0,y0,x1,y1))
        cnt = Counter(region.get_flattened_data()) if hasattr(region, 'get_flattened_data') else Counter(region.getdata())
        colors[(r,c)] = cnt.most_common(1)[0][0]

palette_counts = Counter(colors.values())
print('palette counts:', palette_counts)

EXPECTED = {(0,0,0):86, (255,255,255):85, (63,72,204):15, (255,242,0):9, (254,254,254):1}
check('exactly 5 colours with expected counts', dict(palette_counts) == EXPECTED, dict(palette_counts))

# find the off-white cell
offwhite = [rc for rc,col in colors.items() if col==(254,254,254)]
check('exactly one off-white cell', len(offwhite)==1, offwhite)
r,c = offwhite[0]
check('off-white cell at row7,col4 (0-based)', (r,c)==(7,4), (r,c))

# ---- spiral walk: inward counter-clockwise from top-left, down first ----
def spiral_coords(n):
    coords = []
    top, bottom, left, right = 0, n-1, 0, n-1
    r, c = 0, 0
    # "down first" counter-clockwise inward spiral starting top-left
    while top <= bottom and left <= right:
        # go down along left column
        for rr in range(top, bottom+1):
            coords.append((rr, left))
        # go right along bottom row
        for cc in range(left+1, right+1):
            coords.append((bottom, cc))
        # go up along right column
        for rr in range(bottom-1, top-1, -1):
            coords.append((rr, right))
        # go left along top row
        for cc in range(right-1, left, -1):
            coords.append((top, cc))
        top += 1; bottom -= 1; left += 1; right -= 1
    return coords

coords = spiral_coords(14)
check('spiral has 196 coords, all unique', len(coords)==196==len(set(coords)), len(coords))

bits = []
for (r,c) in coords:
    col = colors[(r,c)]
    if col in ((0,0,0), (63,72,204)):
        bits.append('1')
    else:
        bits.append('0')  # white, yellow, off-white
bitstr = ''.join(bits)
check('first 192 bits len', len(bitstr)==196, len(bitstr))
check('tail 4 bits are 0000', bitstr[192:]=='0000', bitstr[192:])

# decode first 192 bits as ASCII (8 bits per char)
chars = []
for i in range(0, 192, 8):
    byte = bitstr[i:i+8]
    chars.append(chr(int(byte,2)))
url_text = ''.join(chars)
check('poster spiral decodes to gsmg.io/theseedisplanted', url_text=='gsmg.io/theseedisplanted', url_text)

dossier_bits = lib.block_joined(2, sep='')
check('derived bitstring == dossier block 2', bitstr==dossier_bits, '')

print('\nSpiral bit string (independently derived from pixels):')
print(bitstr)

print('\nSUMMARY:', len(PASS), 'passed,', len(FAIL), 'failed')
if FAIL: print('FAILURES', FAIL)
sys.exit(1 if FAIL else 0)
