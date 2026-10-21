"""Win test + three locked containers + structure-agnostic recogniser (dossier s1, s2)."""
import hashlib, base64, math, os, zlib
import coincurve
from Crypto.Cipher import AES

def h160(b): return hashlib.new('ripemd160', hashlib.sha256(b).digest()).hexdigest()
TARGETS = {'a9553269572a317e39f0f518cb87c1a0ee1dbae4', '4bc468447fe1b048ad030a2f9a125478eabc4ed6'}
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def key_hits(priv32, targets=TARGETS):
    x = int.from_bytes(priv32, 'big')
    if not (0 < x < N): return False
    pk = coincurve.PrivateKey(priv32).public_key
    return any(h160(pk.format(c)) in targets for c in (True, False))

assert h160(coincurve.PrivateKey((1).to_bytes(32, 'big')).public_key.format(True)) == '751e76e8199196d454941c45d1b3a323f1433bd6'

TERMINAL = ("U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46zgKlIi8aaqY5gpJPP"
            "EzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4")
SALSHORT = ("U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9zQvX0t8v3jPB4okps"
            "pxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ")
COSMIC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'cosmic.b64')).read().replace('\n', '')
CONTAINERS = {n: base64.b64decode(b) for n, b in
              (('terminal', TERMINAL), ('salshort', SALSHORT), ('cosmic', COSMIC))}
SHA = {'terminal': '291dfd6f3e759ec2e272b35a00c24907da70c3e7a9291b4c13605c7b0b4f3de9',
       'salshort': '9e2831e1b34b5f34796df47ccaf6530d48d371c61a6bff84d60db1064fa7a258',
       'cosmic': 'b18950551a4dd0cb8a9378f0906ba18c03a15f0ee83eb98c6bc90165c5f79805'}
for n, raw in CONTAINERS.items():
    assert hashlib.sha256(raw).hexdigest() == SHA[n], n

def evp(pw, salt, md):
    d = b''; prev = b''
    while len(d) < 48:
        prev = md(prev + pw + salt).digest(); d += prev
    return d[:32], d[32:48]

MDS = {'sha256': hashlib.sha256, 'md5': hashlib.md5}

def try_open(raw, pw, md='sha256', full=False):
    """Return (pad, plaintext) if PKCS7 valid else None. Checks last block first (cheap)."""
    k, iv = evp(pw, raw[8:16], MDS[md])
    ct = raw[16:]
    if not full and len(ct) > 32:
        last = AES.new(k, AES.MODE_CBC, ct[-32:-16]).decrypt(ct[-16:])
        p = last[-1]
        if not (1 <= p <= 16 and last[-p:] == bytes([p]) * p): return None
    pt = AES.new(k, AES.MODE_CBC, iv).decrypt(ct)
    p = pt[-1]
    if 1 <= p <= 16 and pt[-p:] == bytes([p]) * p:
        return p, pt[:-p]
    return None

# ---- recogniser (dossier s2, doc 110) ----
def _z_bits(b):
    n = len(b); zs = []
    for bit in range(8):
        k = sum((x >> bit) & 1 for x in b)
        zs.append((k - n / 2) / math.sqrt(n / 4))
    return max(abs(z) for z in zs)

_DIST = {}
def _distinct_z(n):
    if n not in _DIST:
        import random
        r = random.Random(n)
        v = [len(set(r.randbytes(n))) for _ in range(400)]
        m = sum(v) / len(v); s = math.sqrt(sum((x - m) ** 2 for x in v) / len(v))
        _DIST[n] = (m, s)
    return _DIST[n]

MAGIC = [b'Salted__', b'\x1f\x8b', b'PK\x03\x04', b'BZh', b'7z\xbc\xaf', b'\x89PNG', b'%PDF', b'\xfd7zXZ', b'\x28\xb5\x2f\xfd']

def recognise(pt, pad):
    why = []
    if pad >= 3: why.append(f'pad{pad}')
    if not pt: return why
    pr = sum(32 <= c < 127 or c in (9, 10, 13) for c in pt) / len(pt)
    if pr >= 0.80: why.append(f'printable{pr:.2f}')
    if len(pt) >= 32 and _z_bits(pt) >= 6: why.append('bitbias')
    m, s = _distinct_z(len(pt))
    if s > 0 and (len(set(pt)) - m) / s <= -6: why.append('distinct')
    for mg in MAGIC:
        if pt.startswith(mg): why.append('magic'); break
    if b'Salted__' in pt[1:]: why.append('nestedSalted')
    for cp in ('cp273', 'cp037', 'cp500', 'cp1140', 'cp875', 'cp1026'):
        try:
            t = pt.decode(cp)
            if sum(ch.isalnum() or ch == ' ' for ch in t) / len(t) >= 0.95: why.append('ebcdic'); break
        except Exception: pass
    if len(pt) >= 8:
        ev = sum(pt[i] == 0 for i in range(0, len(pt), 2)) / (len(pt) / 2)
        od = sum(pt[i] == 0 for i in range(1, len(pt), 2)) / (len(pt) / 2)
        if max(ev, od) >= 0.6: why.append('utf16')
    for i in range(0, max(1, len(pt) - 31)):
        w = pt[i:i + 32]
        if len(w) == 32 and key_hits(w): why.append(f'KEYWINDOW@{i}')
    return why

class Stats:
    def __init__(self): self.dec = 0; self.valid = 0; self.flags = []; self.cands = 0

def pw_forms(s):
    """Password profiles: sha256 hex of answer (canonical), raw answer, double-hash hex."""
    b = s.encode() if isinstance(s, str) else s
    h1 = hashlib.sha256(b).hexdigest().encode()
    yield 'sha', h1
    yield 'raw', b
    yield 'dbl', hashlib.sha256(hashlib.sha256(b).digest()).hexdigest().encode()
    yield 'hexhex', hashlib.sha256(h1).hexdigest().encode()

def screen(cand, st, label='', mds=('sha256', 'md5')):
    """Full screen: win test (single + double hash) and all containers under all profiles."""
    st.cands += 1
    b = cand.encode() if isinstance(cand, str) else cand
    d1 = hashlib.sha256(b).digest()
    hits = []
    for priv in (d1, hashlib.sha256(d1).digest(), hashlib.sha256(d1.hex().encode()).digest()):
        if key_hits(priv): hits.append(('WIN', label, cand))
    for prof, pw in pw_forms(b):
        for md in mds:
            for n, raw in CONTAINERS.items():
                st.dec += 1
                r = try_open(raw, pw, md)
                if r:
                    st.valid += 1
                    pad, pt = r
                    why = recognise(pt, pad)
                    if why:
                        st.flags.append((n, prof, md, pad, why, label, cand))
    if hits: st.flags.extend(hits)
    return hits

def expected_valid(st):
    return st.dec / 256.0
