"""Independent re-verification of every PROVEN step of the GSMG.IO puzzle, from the
original artifacts in ../originals. Writes exact extracted data to ../data.

Requires: Python 3, Pillow, pycryptodome.   Run:  python tools/verify_chain.py
Every assertion below must pass; nothing here guesses a password for a locked stage.
"""
import base64, hashlib, json, re, sys
from pathlib import Path
from collections import Counter
from PIL import Image
from Crypto.Cipher import AES

ROOT = Path(__file__).resolve().parents[1]
ORIG, DATA = ROOT / 'originals', ROOT / 'data'
DATA.mkdir(exist_ok=True)
log = []
def ok(msg): log.append(msg); print('PASS', msg)
sha = lambda b: hashlib.sha256(b).hexdigest()

def evp(pw, salt, md=hashlib.sha256, klen=32, ivlen=16):
    d, prev = b'', b''
    while len(d) < klen + ivlen:
        prev = md(prev + pw + salt).digest(); d += prev
    return d[:klen], d[klen:klen + ivlen]

def open_env(raw, answer):
    """GSMG convention: passphrase = sha256(answer) as 64 lowercase hex ASCII;
    OpenSSL EVP_BytesToKey(md=sha256, 1 iter); AES-256-CBC; PKCS#7."""
    assert raw[:8] == b'Salted__'
    key, iv = evp(sha(answer.encode()).encode(), raw[8:16])
    p = AES.new(key, AES.MODE_CBC, iv).decrypt(raw[16:]); n = p[-1]
    assert 1 <= n <= 16 and p[-n:] == bytes([n]) * n, 'bad padding'
    return p[:-n]

def textareas(html):
    return [re.sub(r'\s+', '', m) for m in re.findall(r'<textarea[^>]*>(.*?)</textarea>', html, re.S)]

# 1. Poster -> URL ---------------------------------------------------------------
im = Image.open(ORIG / 'poster/puzzle.png').convert('RGB')
order, seen, r, c, d = [], set(), 0, 0, 0
dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))          # down, right, up, left: inward counter-clockwise
for _ in range(196):
    order.append((r, c)); seen.add((r, c))
    nr, nc = r + dirs[d][0], c + dirs[d][1]
    if not (0 <= nr < 14 and 0 <= nc < 14) or (nr, nc) in seen:
        d = (d + 1) % 4; nr, nc = r + dirs[d][0], c + dirs[d][1]
    r, c = nr, nc
pixels = lambda crop: crop.get_flattened_data() if hasattr(crop, 'get_flattened_data') else crop.getdata()
cols = [Counter(pixels(im.crop((75*c, 75*r, min(75*(c+1), 1047), min(75*(r+1), 1047))))).most_common(1)[0][0] for r, c in order]
bitmap = {(0, 0, 0): '1', (63, 72, 204): '1', (255, 255, 255): '0', (255, 242, 0): '0', (254, 254, 254): '0'}
bits = ''.join(bitmap[x] for x in cols)
url = bytes(int(bits[i:i+8], 2) for i in range(0, 192, 8)).decode()
assert url == 'gsmg.io/theseedisplanted'; ok(f'poster spiral (black/blue=1, white/yellow=0) -> {url}')
colored = [('B' if x == (63, 72, 204) else 'Y') for x in cols if x in ((63, 72, 204), (255, 242, 0))]
ok(f'poster colored cells in spiral order: {"".join(colored)} (blue={colored.count("B")}, yellow={colored.count("Y")})')
(DATA / 'poster_spiral_bits.txt').write_text(bits + '\n' + ''.join(colored) + '\n')

# 2. Phase 1 answer hash confirmed by creator message #225 (checked in telegram export separately)
first = 'theflowerblossomsthroughwhatseemstobeaconcretesurface'
ok(f'phase1 answer sha256 = {sha(first.encode())}')

# 3. Phase 2 page: two AES envelopes -----------------------------------------------
p2html = (ORIG / 'pages/phase2_choice.html').read_text(encoding='utf-8')
ta = textareas(p2html); assert len(ta) == 2
p2 = open_env(base64.b64decode(ta[0]), 'causality')
assert len(p2) == 648 and p2.startswith(b'The ironic'); ok('phase2 envelope opens with "causality" (648 bytes)')
seven = ['causality', 'Safenet', 'Luna', 'HSM', '11110',
         '0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854',
         'B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1']
p3 = open_env(base64.b64decode(ta[1]), ''.join(seven))
assert len(p3) == 4090; ok(f'phase3 envelope opens with 7-part concatenation (4090 bytes, sha256 {sha(p3)})')
assert sha(p3) == 'c4ad94559a44a927c1032cc0e024515f9510a0806a2d14458dbf4a360af9865f'
ok('hex part reversed = ' + bytes.fromhex(seven[5][2:])[::-1].decode())

# 4. Phase 3.2 -----------------------------------------------------------------------
i = p3.index(b'U2FsdGVk')
p32 = open_env(base64.b64decode(re.sub(rb'\s+', b'', p3[i:])), 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple')
assert len(p32) == 2422; ok(f'phase3.2 envelope opens (2422 bytes, sha256 {sha(p32)})')

# 4a. Architect text: bytes [447,1986) latin1->cp273 letters, Beaufort key THEMATRIXHASYOU
ct = p32[447:1986].decode('latin1').encode('cp273').decode('ascii')
arch = ''.join(chr(65 + (ord('THEMATRIXHASYOU'[k % 15]) - ord(ch.upper())) % 26) for k, ch in enumerate(ct))
assert len(arch) == 1539; ok('Architect block: cp273 + Beaufort(THEMATRIXHASYOU) -> 1539 letters')
ok(f'Architect letter index 479 (0-based) starts "{arch[479:489]}"; PRIVATEKEY occurrences at {[m.start() for m in re.finditer("PRIVATEKEY", arch)]}')

# 4b. Straddling checkerboard -> 91 letters
digits = re.match(rb'[0-9]+', p32[1990:]).group().decode()
alpha = 'FUBCDORA.LETHINGKYMVPS/JQZXW'
codes = [str(x) for x in range(10) if x not in (1, 4)] + ['1' + str(x) for x in range(10)] + ['4' + str(x) for x in range(10)]
table = dict(zip(codes, alpha)); out, k = [], 0
while k < len(digits):
    w = 2 if digits[k] in '14' else 1; out.append(table[digits[k:k+w]]); k += w
vic = ''.join(out); assert len(vic) == 91; ok(f'checkerboard (key FUBCDORA.LETHINGKYMVPS/JQZXW, blanks 1,4): {vic}')

# 4c. Terminal locked envelope (end of 3.2)
term = base64.b64decode(re.sub(rb'\s+', b'', p32[p32.index(b'U2FsdGVk', 1990):]))

# 5. SalPhaseIon URL = sha256(poster caption) ----------------------------------------
caption = 'GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
h = sha(caption.encode())
assert h in (ORIG / 'cdx_wayback_gsmg.json').read_text(); ok(f'sha256(caption) = {h} is an archived gsmg.io path (SalPhaseIon)')

# 6. SalPhaseIon page ------------------------------------------------------------------
ta = textareas((ORIG / 'pages/salphaseion_phase3.html').read_text(encoding='utf-8'))
s = ta[0]; assert len(s) == 1075
def a0b1(x): b = x.translate(str.maketrans('ab', '01')); return bytes(int(b[j:j+8], 2) for j in range(0, len(b), 8)).decode()
def dec(x): n = int(''.join('0' if ch == 'o' else str(ord(ch) - 96) for ch in x)); return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
labels = {'s[91:195] a=0 b=1': a0b1(s[91:195]), 's[959:999] a=0 b=1': a0b1(s[959:999]),
          's[766:829] a-i=1-9 o=0 int': dec(s[766:829]), 's[830:859] a-i=1-9 o=0 int': dec(s[830:859])}
ok('SalPhaseIon labels: ' + json.dumps(labels))
dbbi, faed = s[0:91], s[195:765]
assert len(dbbi) == 91 and len(faed) == 570 and set(faed) <= set('abcdefghi')
salph = base64.b64decode(s[895:959] + s[999:1063]); cosmic = base64.b64decode(ta[1])
ok(f'SalPhaseIon literal text fragments: {s[860:895]!r} / {s[1063:]!r}')

# 7. DBBI - checkerboard (mod 26, A=0) -------------------------------------------------
diff = ''.join(chr(65 + (ord(a.upper()) - ord(b)) % 26) for a, b in zip(dbbi, vic))
assert diff[21:27] == 'YOUWON' and diff[0] + diff[3] + diff[20] == 'VIC'
ok(f'DBBI - VIC = {diff}  (VIC at 1,4,21; YOUWON at 22-27; 64-letter tail)')

# 8. Locked envelopes --------------------------------------------------------------------
locked = {}
for name, raw in (('terminal_phase3_2_end', term), ('salphaseion_short', salph), ('cosmic_duality', cosmic)):
    assert raw[:8] == b'Salted__' and (len(raw) - 16) % 16 == 0
    locked[name] = {'bytes': len(raw), 'ciphertext_bytes': len(raw) - 16, 'salt': raw[8:16].hex(), 'sha256': sha(raw)}
    (DATA / f'locked_{name}.bin').write_bytes(raw)
    (DATA / f'locked_{name}.b64').write_text(base64.b64encode(raw).decode() + '\n')
ok('locked envelopes: ' + json.dumps(locked))

# write exact data ------------------------------------------------------------------------
(DATA / 'phase2_plaintext.bin').write_bytes(p2)
(DATA / 'phase3_plaintext.bin').write_bytes(p3)
(DATA / 'phase3_2_plaintext.bin').write_bytes(p32)
(DATA / 'architect_letters_1539.txt').write_text(arch + '\n')
(DATA / 'checkerboard_vic_91.txt').write_text(vic + '\n' + digits + '\n')
(DATA / 'salphaseion_compact_1075.txt').write_text(s + '\n')
(DATA / 'DBBI_91.txt').write_text(dbbi + '\n')
(DATA / 'FAED_570.txt').write_text(faed + '\n')
(DATA / 'dbbi_minus_vic_91.txt').write_text(diff + '\n')
(DATA / 'seven_part_phase3_answer.json').write_text(json.dumps(seven, indent=1) + '\n')
(DATA / 'verify_log.txt').write_text('\n'.join(log) + '\n')
print('\nALL CHECKS PASSED')
