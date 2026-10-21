import base64, hashlib, re
from Crypto.Cipher import AES
F = r'c:\gsmg-puzzle-clean\files'

def evp(pw: bytes, salt: bytes):
    d = b''; prev = b''
    while len(d) < 48:
        prev = hashlib.sha256(prev + pw + salt).digest(); d += prev
    return d[:32], d[32:48]

def load(name):
    return base64.b64decode(re.sub(r'\s', '', open(f'{F}\\{name}').read()))

def dec(raw, pwtext: str, hashed=True):
    """returns plaintext or None if padding bad"""
    assert raw[:8] == b'Salted__'
    pw = hashlib.sha256(pwtext.encode()).hexdigest().encode() if hashed else pwtext.encode()
    k, iv = evp(pw, raw[8:16])
    p = AES.new(k, AES.MODE_CBC, iv).decrypt(raw[16:])
    n = p[-1]
    if 1 <= n <= 16 and p[-n:] == bytes([n]) * n:
        return p[:-n]
    return None

def printable(b):
    return sum(32 <= c < 127 or c in (9, 10, 13) for c in b) / max(1, len(b))

# ---- bitcoin checker (pure python) ----
P = 2**256 - 2**32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
def add(a, b):
    if a is None: return b
    if b is None: return a
    if a[0] == b[0] and (a[1] + b[1]) % P == 0: return None
    if a == b: l = 3 * a[0] * a[0] * pow(2 * a[1], -1, P) % P
    else: l = (b[1] - a[1]) * pow(b[0] - a[0], -1, P) % P
    x = (l * l - a[0] - b[0]) % P
    return (x, (l * (a[0] - x) - a[1]) % P)
def mul(k, pt=G):
    r = None
    while k:
        if k & 1: r = add(r, pt)
        pt = add(pt, pt); k >>= 1
    return r
def h160(b):
    return hashlib.new('ripemd160', hashlib.sha256(b).digest()).hexdigest()
def hashes(k):
    x, y = mul(k)
    comp = bytes([2 + (y & 1)]) + x.to_bytes(32, 'big')
    unc = b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')
    return h160(comp), h160(unc)
# Half (uncompressed, compressed) and Better Half (hash160 only; its encoding is
# unknown). Better Half was missing, so check_key could never accept it.
TARGET = {'a9553269572a317e39f0f518cb87c1a0ee1dbae4', '06bbdc66fda09110435c79a86656a604c2d5c69b',
          '4bc468447fe1b048ad030a2f9a125478eabc4ed6'}
def check_key(k):
    return any(h in TARGET for h in hashes(k))
