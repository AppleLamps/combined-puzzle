"""Decide whether a candidate AES plaintext is meaningful WITHOUT assuming it is text.

The mistake this replaces: judging a decrypt by 'is it printable ASCII'. The
Phase 3.2 envelope is only 60% printable. A raw key is 0%. Both small blobs are
5 blocks, so their plaintext is 64-79 bytes -- and 64 bytes is exactly two
32-byte private keys, which is what 'the private keyS belong to half and better
half' describes. A printability filter throws that away.
"""
import hashlib

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
P = 2**256 - 2**32 - 977
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
PRIZE = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
MAGIC = {b"\x1f\x8b": "gzip", b"\x78\x9c": "zlib", b"\x78\x01": "zlib",
         b"\x78\xda": "zlib", b"BZh": "bzip2", b"PK\x03\x04": "zip",
         b"\x89PNG": "png", b"\xff\xd8\xff": "jpeg", b"%PDF": "pdf",
         b"\x04\x22\x4d\x18": "lz4", b"\xfd7zXZ": "xz"}
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def _add(p, q):
    if p is None: return q
    if q is None: return p
    if p[0] == q[0] and (p[1] + q[1]) % P == 0: return None
    l = ((q[1]-p[1]) * pow(q[0]-p[0], P-2, P)) % P if p != q else \
        (3*p[0]*p[0] * pow(2*p[1], P-2, P)) % P
    x = (l*l - p[0] - q[0]) % P
    return (x, (l*(p[0]-x) - p[1]) % P)


def _mul(k):
    r, p = None, G
    while k:
        if k & 1: r = _add(r, p)
        p = _add(p, p); k >>= 1
    return r


def address(priv, compressed=True):
    x, y = _mul(priv)
    pub = (bytes([2 + (y & 1)]) + x.to_bytes(32, 'big')) if compressed else \
          b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')
    h = hashlib.new('ripemd160', hashlib.sha256(pub).digest()).digest()
    payload = b'\x00' + h
    chk = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    n = int.from_bytes(payload + chk, 'big'); s = ''
    while n: n, r = divmod(n, 58); s = B58[r] + s
    return '1' * (len(payload + chk) - len((payload + chk).lstrip(b'\0'))) + s


def inspect(body, derive=True):
    """Return a list of reasons this plaintext looks structured. Empty = noise."""
    hits = []
    n = len(body)
    printable = sum(1 for c in body if 32 <= c < 127 or c in (9, 10, 13)) / max(1, n)
    if printable >= 0.90:
        hits.append(f"printable-ascii {printable:.2f}")
    for m, name in MAGIC.items():
        if body.startswith(m):
            hits.append(f"magic:{name}")
    # EBCDIC -- this puzzle already used cp1141 once
    try:
        e = body.decode('cp1141')
        pe = sum(1 for ch in e if ch.isprintable()) / max(1, len(e))
        if pe >= 0.90:
            hits.append(f"ebcdic-printable {pe:.2f}")
    except Exception:
        pass
    # base58 / base64 charsets
    if n >= 40 and all(chr(c) in B58 for c in body):
        hits.append("all-base58")
    # exactly two 32-byte scalars: the 'half and better half' shape
    if n == 64 and derive:
        a = int.from_bytes(body[:32], 'big')
        b = int.from_bytes(body[32:], 'big')
        if 0 < a < N and 0 < b < N:
            for label, k in (("half", a), ("better half", b)):
                for comp in (True, False):
                    if address(k, comp) == PRIZE:
                        hits.append(f"*** {label} DERIVES THE PRIZE ADDRESS ***")
    if n == 32 and derive:
        k = int.from_bytes(body, 'big')
        if 0 < k < N:
            for comp in (True, False):
                if address(k, comp) == PRIZE:
                    hits.append("*** DERIVES THE PRIZE ADDRESS ***")
    return hits
