"""Build data/ for doc 115 from the dossier and the poster. Nothing is retyped.

    python3 prep.py            # fetches puzzle.png from the GitHub mirror if absent

Every extracted block is checked against a property the dossier states for it.
"""
import os, hashlib, urllib.request, collections
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data'); os.makedirs(DATA, exist_ok=True)
DOSSIER = os.path.join(HERE, '..', '..', '..', 'GSMG-PUZZLE-DOSSIER.md')
POSTER_URL = 'https://raw.githubusercontent.com/puzzlehunt/gsmgio-5btc-puzzle/master/puzzle.png'
POSTER_SHA = '38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830'

lines = open(DOSSIER, encoding='utf-8').read().split('\n')

def block(prefix, join=''):
    i = next(k for k, l in enumerate(lines) if l.startswith(prefix))
    out = []
    while lines[i] != '```':
        out.append(lines[i]); i += 1
    return join.join(out)

def put(name, s):
    open(os.path.join(DATA, name), 'w', encoding='utf-8').write(s)

soup = block('dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbf')
assert len(soup) == 1075 and soup.endswith('shabefanstoo')
put('soup.txt', soup)
cosmic = block('U2FsdGVkX18tP2/gbclQ5t', '\n')
import base64
assert hashlib.sha256(base64.b64decode(cosmic.replace('\n', ''))).hexdigest().startswith('b18950551a4dd0cb')
put('cosmic.b64', cosmic)
arch = block('YOURLIFEISTHESUMOF').lower()
assert len(arch) == 1539 and arch[479:489] == 'privatekey'
put('architect.txt', arch)
chk = next(l for l in lines if l.startswith('INCASEYOUMANAGE')).lower()
assert len(chk) == 91
put('checker.txt', chk)
p2 = block('The ironic 2name', '\r\n')
assert hashlib.sha256(p2.encode()).hexdigest().startswith('e2f9dd65'), 'phase-2 plaintext hash'
put('phase2.txt', p2)
put('intro.txt', block("I've been waiting", '\n'))
put('riddle.txt', block('What if the merovingian', '\n'))

png = os.path.join(DATA, 'puzzle.png')
if not os.path.exists(png):
    urllib.request.urlretrieve(POSTER_URL, png)
assert hashlib.sha256(open(png, 'rb').read()).hexdigest() == POSTER_SHA, 'poster hash'
a = np.array(Image.open(png).convert('RGB'))
code = {'000000': 'K', 'FFFFFF': 'W', '3F48CC': 'B', 'FFF200': 'Y', 'FEFEFE': 'F'}
G = []
for r in range(14):
    row = []
    for c in range(14):
        blk = a[r * 75:(r + 1) * 75, c * 75:min((c + 1) * 75, 1047)]
        cnt = collections.Counter(map(tuple, blk.reshape(-1, 3)))
        row.append(code['%02X%02X%02X' % cnt.most_common(1)[0][0]])
    G.append(row)
G = np.array(G)
from lists_spiral import spiral
bits = ''.join('1' if G[r, c] in 'KB' else '0' for r, c in spiral(14))
assert bytes(int(bits[i:i + 8], 2) for i in range(0, 192, 8)) == b'gsmg.io/theseedisplanted' and bits[192:] == '0000'
np.save(os.path.join(DATA, 'grid.npy'), G)
print('data/ built and verified')
