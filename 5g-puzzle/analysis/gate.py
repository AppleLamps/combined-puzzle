#!/usr/bin/env python3
"""The acceptance gate, with padding and printability both removed from it.

Earlier in this session I replaced a printable-ASCII filter with a PKCS#7 pad
filter. That was better but still wrong as a *gate*: pad 1 is not disqualifying,
it is merely uninformative (1 wrong key in 256 produces it), and I then leaned on
printability again to dismiss 25 pad-1 decrypts. A private key is 0% printable.

The real acceptance test is on chain and needs neither. Two addresses held puzzle
funds:

    Half        1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
                hash160 a9553269572a317e39f0f518cb87c1a0ee1dbae4
                uncompressed pubkey known from its spends
    Better Half 17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa
                hash160 4bc468447fe1b048ad030a2f9a125478eabc4ed6

So: decrypt, then slide a 32-byte window over the WHOLE 80-byte block at every
offset, derive the secp256k1 public key in both encodings, and compare hash160
against those two. No pad filter. No text assumption. A candidate either produces
a key that controls prize funds or it does not.
"""
import hashlib
from coincurve import PublicKey

HALF     = bytes.fromhex('a9553269572a317e39f0f518cb87c1a0ee1dbae4')
BETTER   = bytes.fromhex('4bc468447fe1b048ad030a2f9a125478eabc4ed6')
HALF_PUB = bytes.fromhex('04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464'
                         '9c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559')
TARGETS  = {HALF: 'Half', BETTER: 'BetterHalf'}
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def h160(b):
    return hashlib.new('ripemd160', hashlib.sha256(b).digest()).digest()

def keycheck(block, label=''):
    """Every 32-byte window of `block` as a private key, both pubkey encodings."""
    out = []
    for off in range(0, len(block) - 31):
        k = block[off:off+32]
        n = int.from_bytes(k, 'big')
        if not (1 <= n < N):
            continue
        try:
            pk = PublicKey.from_valid_secret(k)
        except Exception:
            continue
        for comp in (True, False):
            enc = pk.format(compressed=comp)
            if enc == HALF_PUB:
                out.append(f'{label} offset {off}: PUBKEY MATCHES Half EXACTLY')
            hit = TARGETS.get(h160(enc))
            if hit:
                out.append(f'{label} offset {off}: {hit} '
                           f'({"compressed" if comp else "uncompressed"}) key={k.hex()}')
    return out

def structure(block):
    """Non-key reasons a block might be meaningful. Reported, never used to reject."""
    r = []
    pr = sum(1 for c in block if 32 <= c < 127 or c in (9,10,13)) / len(block)
    if pr >= 0.90: r.append(f'printable {pr:.2f}')
    try:
        e = block.decode('cp1141')
        if sum(1 for c in e if c.isprintable()) / len(e) >= 0.90:
            r.append('ebcdic-cp1141')
    except Exception:
        pass
    for m, nm in {b'\x1f\x8b':'gzip', b'x\x9c':'zlib', b'x\x01':'zlib', b'x\xda':'zlib',
                  b'BZh':'bzip2', b'PK\x03\x04':'zip', b'\x89PNG':'png',
                  b'\xff\xd8\xff':'jpeg', b'%PDF':'pdf', b'\xfd7zXZ':'xz'}.items():
        if block.startswith(m): r.append(f'magic:{nm}')
    return r

# ---------------------------------------------------------------------------
# Keys stored as TEXT.  The window check above assumes the blob holds a key as 32
# binary bytes.  A person writing a key down does not do that -- they write hex,
# or WIF, or base64.  A 64-character hex key is an EXACT fit for the 64-byte
# plaintext these envelopes hold, every bit as good a fit as two raw keys, and
# the binary window check walks straight past it.
import re as _re, base64 as _b64lib

_HEX = _re.compile(rb'[0-9a-fA-F]{64}')
_WIF = _re.compile(rb'[5KL][1-9A-HJ-NP-Za-km-z]{50,51}')
_B64 = _re.compile(rb'[A-Za-z0-9+/]{43}=')
_B58A = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def _b58decode(s):
    n = 0
    for ch in s:
        n = n * 58 + _B58A.index(ch)
    b = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    return b'\0' * (len(s) - len(s.lstrip('1'))) + b


def _try(k, why, out, label):
    n = int.from_bytes(k, 'big')
    if not (1 <= n < N):
        return
    try:
        pk = PublicKey.from_valid_secret(k)
    except Exception:
        return
    for comp in (True, False):
        enc = pk.format(compressed=comp)
        if enc == HALF_PUB:
            out.append(f'{label} {why}: PUBKEY MATCHES Half EXACTLY')
        hit = TARGETS.get(h160(enc))
        if hit:
            out.append(f'{label} {why}: {hit} '
                       f'({"compressed" if comp else "uncompressed"}) key={k.hex()}')


def textkeys(block, label=''):
    """A key written as hex, WIF or base64 anywhere in the plaintext."""
    out = []
    flat = bytes(c for c in block if c not in b' \t\r\n')
    for src, tag in ((block, 'hex'), (flat, 'hex-flat')):
        for m in _HEX.finditer(src):
            _try(bytes.fromhex(m.group().decode()), f'{tag}@{m.start()}', out, label)
    for m in _WIF.finditer(block):
        try:
            d = _b58decode(m.group().decode())
        except Exception:
            continue
        if len(d) in (37, 38) and d[0] == 0x80:
            body, chk = d[:-4], d[-4:]
            if hashlib.sha256(hashlib.sha256(body).digest()).digest()[:4] == chk:
                _try(body[1:33], f'WIF@{m.start()}', out, label)
    for m in _B64.finditer(block):
        try:
            _try(_b64lib.b64decode(m.group()), f'b64@{m.start()}', out, label)
        except Exception:
            pass
    return out


def fullcheck(block, label=''):
    """Every way 80 bytes could carry a key: binary windows AND text encodings."""
    return keycheck(block, label) + textkeys(block, label)


if __name__ == '__main__':
    # self-test: a known key must be found by the gate, at every offset it sits at
    import os
    k = os.urandom(32)
    pk = PublicKey.from_valid_secret(k)
    fake = h160(pk.format(True))
    TARGETS[fake] = 'SELFTEST'
    block = os.urandom(20) + k + os.urandom(28)
    print('self-test:', keycheck(block, 'test') or 'FAILED')
