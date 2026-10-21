"""Wider password search over the three unopened containers.
Adds vs mywork/pool_search.py: KDF digests md5/sha1/sha512 (not only sha256), all substrings of the
space-less Architect text, long word n-grams of the film transcripts, token combinations."""
import sys, re, hashlib, itertools, time
sys.path.insert(0, 'mywork')
from lib import load, printable
from Crypto.Cipher import AES

def evp(pw, salt, md):
    d = b''; p = b''
    while len(d) < 48:
        p = hashlib.new(md, p + pw + salt).digest(); d += p
    return d[:32], d[32:48]

conts = {n: load(n + '.b64') for n in ('terminal', 'salphaseion-short', 'cosmic-duality', 'phase3.2')}
MDS = ('sha256', 'md5', 'sha1', 'sha512')

def trans(s):
    b = s.encode('latin-1', 'ignore'); h = hashlib.sha256(b)
    yield 'sha-hex', h.hexdigest().encode()
    yield 'raw', b
    yield 'sha-raw32', h.digest()
    yield 'sha-HEX', h.hexdigest().upper().encode()

def test(s, hits):
    for tn, pw in trans(s):
        for md in MDS:
            for cn, raw in conts.items():
                k, iv = evp(pw, raw[8:16], md); ct = raw[16:]
                p = AES.new(k, AES.MODE_CBC, ct[-32:-16]).decrypt(ct[-16:]); n = p[-1]
                if 1 <= n <= 16 and p[-n:] == bytes([n]) * n:
                    f = AES.new(k, AES.MODE_CBC, iv).decrypt(ct)[:-n]; pr = printable(f)
                    if pr > (0.55 if cn == 'phase3.2' else 0.8):
                        hits.append((cn, tn, md, s[:70], round(pr, 2), f[:80])); print('HIT', hits[-1], flush=True)

pool = set()
arch = open('derived/architect-text.txt').read().strip().lower()
for i in range(len(arch)):                       # every substring up to 45 letters
    for L in range(3, 46): pool.add(arch[i:i + L])
for L in range(46, 400): pool.add(arch[-L:])     # every suffix (the "last words")
cb = open('derived/checkerboard-plaintext.txt').read().strip().lower()
for i in range(len(cb)):
    for j in range(i + 3, len(cb) + 1): pool.add(cb[i:j])
for fn in ('matrix-reloaded.txt', 'mywork/wikiquote_reloaded.txt'):
    w = re.findall(r"[A-Za-z0-9']+", open(fn, encoding='utf-8', errors='ignore').read())
    for i in range(len(w)):
        for n in range(1, 21):
            seq = w[i:i + n]
            if len(seq) < n: break
            j = ''.join(seq).lower().replace("'", '')
            pool.add(j)
            if n <= 12: pool.add(' '.join(seq)); pool.add(' '.join(seq).lower())
toks = ['matrixsumlist', 'enter', 'lastwordsbeforearchichoice', 'thispassword', 'yourlastcommand', 'ourfirsthintisyourlastcommand',
        'shabefourfirsthintisyourlastcommand', 'shabefanstoo', 'anstoo', 'answertoo', 'sha256', 'shabef', 'firsthint', 'lastcommand',
        'causality', 'theseedisplanted', 'gsmg.io/theseedisplanted', 'hashthetext', 'HASHTHETEXT', 'salphaseion', 'cosmicduality',
        'halfandbetterhalf', 'half', 'betterhalf', 'choice', 'theproblemischoice', 'hope', 'wewont', 'ciaobella', 'ciaobellao', 'theone']
for n in (1, 2, 3):
    for c in itertools.permutations(toks, n):
        for sep in ('', ' '): pool.add(sep.join(c))
pool = sorted(p for p in pool if p)
print('pool', len(pool), flush=True)
hits = []; t0 = time.time()
test('jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple', hits)   # control
assert hits, 'control failed'
for i, s in enumerate(pool):
    test(s, hits)
    if i % 50000 == 0: print(i, int(time.time() - t0), 's', flush=True)
print('done', len(hits) - 1, 'non-control hits', int(time.time() - t0), 's')
