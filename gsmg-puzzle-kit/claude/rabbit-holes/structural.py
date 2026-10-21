"""Rabbit-hole thread, part 3: structural key checks (3 Oct 2026).
Each family is one justified operation; see README.md. Reuses rt.py's
decrypt, keyhit (prize, sentinel, 4 EC neighbours, both point forms) and controls."""
import sys, os, re, json, hashlib, base64
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'riddle-method'))
import rt
from rt import dec, keyhit, evp, N, h160
import coincurve
K = os.environ.get('GSMG_KIT', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'

B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def addr(h):
    p = b'\x00' + bytes.fromhex(h); d = p + hashlib.sha256(hashlib.sha256(p).digest()).digest()[:4]
    n = int.from_bytes(d, 'big'); s = ''
    while n: n, r = divmod(n, 58); s = B58[r] + s
    return '1' * (len(d) - len(d.lstrip(b'\0'))) + s
def addrs(k32):
    pk = coincurve.PrivateKey(k32).public_key
    return [addr(h160(pk.format(c))) for c in (True, False)]

tests = 0; hits = []
def scal(label, v):
    """test integer v (reduced mod n) as raw scalar, plus sha256 of its 32 bytes"""
    global tests
    v %= N
    if v == 0: return
    k = v.to_bytes(32, 'big'); tests += 1
    if keyhit(k): hits.append(('raw', label))
    tests += 1
    if keyhit(hashlib.sha256(k).digest()): hits.append(('sha256', label))

# ---- controls
rt.controls()                                   # key 1, three solved gates open
ANS = {'phase2': 'causality',
       'phase3': 'causalitySafenetLunaHSM111100x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1',
       'phase3.2': 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple'}
PT = {}
for n, a in ANS.items():
    p, body = dec(rt.SOLVED[n], hashlib.sha256(a.encode()).hexdigest().encode()); PT[n] = body
assert hashlib.sha256(PT['phase3.2']).hexdigest().startswith('b82afeb8')
# real on-chain control for the raw-ASCII form: poster URL as a big-endian scalar = "Good job, Neo!" checkpoint
url = int.from_bytes(b'gsmg.io/theseedisplanted', 'big').to_bytes(32, 'big')
assert addrs(url)[0].startswith('148XH2YBmL'), addrs(url)
# planted control for the window scans: a target-hitting key needs the prize key, so plant key 1's
# hash160 into a private target set and check the scanner finds it inside a buffer
rt.TARGETS.add('751e76e8199196d454941c45d1b3a323f1433bd6')
buf = os.urandom(50) + (1).to_bytes(32, 'big') + os.urandom(40)
assert any(keyhit(buf[i:i+32]) for i in range(len(buf)-31))
hexbuf = 'zz' + (1).to_bytes(32, 'big').hex() + 'qq'
assert any(keyhit(bytes.fromhex(m)) for m in re.findall(r'(?=([0-9a-fA-F]{64}))', hexbuf))
rt.TARGETS.discard('751e76e8199196d454941c45d1b3a323f1433bd6')
print('controls: key1 ok, 3 gates open, raw-ASCII form reproduces 148XH2YBmL..., window scanners find planted key')

# ---- S1: the AES key, IV and key||IV each solved gate derived (EVP SHA-256, 1 iter)
for n, a in ANS.items():
    raw = rt.SOLVED[n]; pw = hashlib.sha256(a.encode()).hexdigest().encode()
    k, iv = evp(pw, raw[8:16], 'sha256')
    scal('S1 evpkey ' + n, int.from_bytes(k, 'big')); scal('S1 iv ' + n, int.from_bytes(iv, 'big'))
    scal('S1 key+iv ' + n, int.from_bytes(hashlib.sha256(k + iv).digest(), 'big'))
    scal('S1 salt ' + n, int.from_bytes(raw[8:16], 'big'))
s1 = tests

# ---- S2: chain answers <= 32 bytes as raw big-endian ASCII scalars (left- and right-padded)
atoms = ['causality', 'Safenet', 'Luna', 'HSM', '11110', 'jacquefresco', 'giveitjustonesecond',
         'heisenbergsuncertaintyprinciple', 'theseedisplanted', 'gsmg.io/theseedisplanted',
         'yellowblueprimes', 'matrixsumlist', 'lastwordsbeforearchichoice', 'yinyang', 'thispassword',
         'enter', 'THEMATRIXHASYOU', 'theflowerblossoms', 'salphaseion', 'cosmicduality', 'SalPhaseIon',
         'CosmicDuality', 'giveit', 'givetit', 'halfandbetterhalf', 'TAKETHEPRIVATEKEY', 'CIAOBELLAO',
         'FUBCDORA.LETHINGKYMVPS/JQZXW', 'yourlastcommand', 'ourfirsthint', 'shabefanstoo', 'theansweroo']
for a in atoms:
    b = a.encode()
    if len(b) > 32: continue
    scal('S2 left ' + a, int.from_bytes(b, 'big')); scal('S2 right ' + a, int.from_bytes(b.ljust(32, b'\0'), 'big'))
s2 = tests - s1

# ---- S3: every 32-byte window and every 64-hex window of every solved plaintext, the textarea,
# the three locked blobs and the 1,539 letters
texts = dict(PT)
texts['textarea'] = ''.join(open(K + 'salphaseion-textarea.txt').read().split()).encode()
for n, f in [('terminal', 'terminal.b64'), ('short', 'salphaseion-short.b64'), ('cosmic', 'cosmic-duality.b64')]:
    texts['blob ' + n] = rt.load(f)
texts['architect'] = ''.join(open(K + 'architect_letters_1539.txt').read().split()).encode()
w0 = tests
for n, b in texts.items():
    for i in range(len(b) - 31):
        tests += 1
        if keyhit(b[i:i+32]): hits.append(('window', n, i))
    for m in set(re.findall(rb'(?=([0-9a-fA-F]{64}))', b)):
        tests += 1
        if keyhit(bytes.fromhex(m.decode())): hits.append(('hexwindow', n))
s3 = tests - w0

# ---- S4: base58 runs that could be WIF (51/52) or BIP38 (58, '6P') in any text
b58runs = []
for n, b in texts.items():
    for m in re.findall(rb'[1-9A-HJ-NP-Za-km-z]{50,}', b): b58runs.append((n, len(m), m[:12]))

# ---- S5: the poster grid as an integer (196 bits): row-major, column-major, spiral, each reversed;
# with the 4 centre cells and without (the 192-bit spiral is the URL, the known checkpoint)
bits = json.load(open(K + 'matrix.json'))['bit_grid']; S = 14
order = []; top, bot, left, right = 0, S - 1, 0, S - 1
while top <= bot and left <= right:
    for r in range(top, bot + 1): order.append((r, left))
    for c in range(left + 1, right + 1): order.append((bot, c))
    if left < right:
        for r in range(bot - 1, top - 1, -1): order.append((r, right))
    if top < bot:
        for c in range(right - 1, left, -1): order.append((top, c))
    top += 1; bot -= 1; left += 1; right -= 1
sp = ''.join(bits[r][c] for r, c in order)
assert int(sp[:192], 2).to_bytes(24, 'big') == b'gsmg.io/theseedisplanted'
s5 = tests
for name, s in [('rowmajor', ''.join(bits)), ('colmajor', ''.join(bits[r][c] for c in range(S) for r in range(S))), ('spiral196', sp)]:
    for t in (s, s[::-1], ''.join('1' if ch == '0' else '0' for ch in s)):
        scal('S5 ' + name, int(t, 2))
s5 = tests - s5

# ---- S6: digit objects read as one integer: the 149-digit checkerboard input, the 140-hex phase-3 part 6
cb = ''.join(open(K + 'checkerboard_vic_91.txt').read().split())
d149 = ''.join(re.findall(r'\d{149}', cb)) or re.sub(r'\D', '', cb)[:149]
s6 = tests
scal('S6 checkerboard149', int(d149)); scal('S6 checkerboard149 rev', int(d149[::-1]))
g = '736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854'
scal('S6 genesis140 hex', int(g, 16)); scal('S6 genesis140 reversed back', int(bytes.fromhex(g)[::-1].hex(), 16))
s6 = tests - s6

print('S1 evp keys/ivs/salts:', s1, '| S2 raw ASCII:', s2, '| S3 windows:', s3, '| S5 poster ints:', s5, '| S6 digit ints:', s6)
print('S4 base58 runs >=50 chars:', b58runs or 'none')
print('total scalar tests:', tests, '| hits:', hits or 'none')

# ---- S7 (confirmation of doc 107, not new): the convention's own outputs as keys.
# win() = sha256(x) and sha256(sha256(x)); the password of each gate IS sha256(answer), so win(answer) tests it.
s7 = 0
for n, a in ANS.items():
    pw = hashlib.sha256(a.encode()).hexdigest()
    for x in (a, pw, PT[n], PT[n].strip(), PT[n].replace(b'\r\n', b'\n')):
        s7 += 1
        if rt.win(x): hits.append(('S7', n))
# phase-3.2 plaintext without the Terminal envelope, and the Terminal base64 itself
for x in (PT['phase3.2'][:2292], PT['phase3.2'][:2292].strip(), PT['phase3.2'][2292:], PT['phase3.2'][2292:].replace(b'\r\n', b'')):
    s7 += 1
    if rt.win(x): hits.append(('S7', '3.2 split'))
print('S7 convention outputs (answers, passwords, plaintexts):', s7, '| hits:', hits or 'none')
