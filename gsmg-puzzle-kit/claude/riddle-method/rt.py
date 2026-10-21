"""Riddle-answer tester: few candidates, exact convention, all locks, win test.

Usage: python3 rt.py FILE [FILE...]    one candidate per line; '#' lines are notes
Each candidate is tried against every container (3 locked + 3 solved as controls)
under password forms: hex(sha256(x)) [canonical], hex(sha256(sha256(x))),
hex(sha256(hex(sha256(x)))), raw sha256(x); EVP md sha256 and md5.
"""
import base64, hashlib, sys, coincurve
from Crypto.Cipher import AES
from audit_results import AuditResults, valid_padding

import os
D = os.environ.get('GSMG_KIT', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
def load(n): return base64.b64decode(''.join(open(D + n).read().split()))
LOCKED = {'terminal': load('terminal.b64'), 'short': load('salphaseion-short.b64'),
          'cosmic': load('cosmic-duality.b64')}
SOLVED = {'phase2': load('phase2.b64'), 'phase3': load('phase3.b64'), 'phase3.2': load('phase3.2.b64')}

def evp(pw, salt, md):
    d = b''; prev = b''
    while len(d) < 48:
        prev = hashlib.new(md, prev + pw + salt).digest(); d += prev
    return d[:32], d[32:48]

def dec(raw, pw, md='sha256'):
    k, iv = evp(pw, raw[8:16], md)
    pt = AES.new(k, AES.MODE_CBC, iv).decrypt(raw[16:])
    p = valid_padding(pt)
    if p: return p, pt[:-p]
    return 0, None

def forms(x):
    b = x.encode()
    h = hashlib.sha256(b)
    yield 'hex', h.hexdigest().encode()
    yield 'dblhex', hashlib.sha256(h.digest()).hexdigest().encode()
    yield 'hexofhex', hashlib.sha256(h.hexdigest().encode()).hexdigest().encode()
    yield 'raw', h.digest()

def h160(b): return hashlib.new('ripemd160', hashlib.sha256(b).digest()).hexdigest()
TARGETS = {'a9553269572a317e39f0f518cb87c1a0ee1dbae4', '4bc468447fe1b048ad030a2f9a125478eabc4ed6',
           'a4ae210a25bb8e2c359a134fafc2e30c6709dbc0', 'f8fca692ffc90cba0c330dc56e02fa8da8d2d6e6',
           '3de34fca1bd6b7607243b0316a8102b7598cc9dc', 'c889dfbf698413209b6131895250b869f68560e0'}
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
def keyhit(k32):
    v = int.from_bytes(k32, 'big')
    if not 0 < v < N: return False
    pk = coincurve.PrivateKey(k32).public_key
    return any(h160(pk.format(c)) in TARGETS for c in (True, False))
def win(x):
    b = x.encode() if isinstance(x, str) else x
    return keyhit(hashlib.sha256(b).digest()) or keyhit(hashlib.sha256(hashlib.sha256(b).digest()).digest())

def judge(body, pad):
    """Heuristic ranking only; the caller preserves every padding-valid body."""
    if body is None: return ''
    n = len(body)
    # Downstream key validation runs before heuristic ranking.
    for i in range(0, max(n - 31, 0)):
        if keyhit(body[i:i + 32]): return 'KEYWINDOW'
    pr = sum(32 <= c < 127 or c in (9, 10, 13) for c in body) / max(n, 1)
    if pr >= 0.8: return 'printable%.2f' % pr
    if b'Salted__' in body: return 'nested'
    for bit in range(8) if n else ():
        k = sum((c >> bit) & 1 for c in body)
        z = (k - n / 2) / ((n / 4) ** .5)
        if abs(z) >= 6: return 'bitbias%d' % bit
    return ''

def controls():
    assert h160(coincurve.PrivateKey((1).to_bytes(32, 'big')).public_key.format(True)) == '751e76e8199196d454941c45d1b3a323f1433bd6'
    c = ['causality',
         'causalitySafenetLunaHSM111100x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1',
         'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple']
    expected = {
        'phase2': 'e2f9dd65604a3231f8b3301724e8d713a88fffc4b6c7c4aeeb20f58a582b593a',
        'phase3': 'c4ad94559a44a927c1032cc0e024515f9510a0806a2d14458dbf4a360af9865f',
        'phase3.2': 'b82afeb86f9e50848220f9b64b744b821400308aea273a1c949b9d2d0e408a34'}
    for name, cand in zip(SOLVED, c):
        p, body = dec(SOLVED[name], hashlib.sha256(cand.encode()).hexdigest().encode())
        assert p and hashlib.sha256(body).hexdigest() == expected[name], name
    return True

def run(cands):
    flags = AuditResults(); tests = pads = 0
    for x in cands:
        if win(x): flags.append(('WIN', 'scalar', '', '', x))
        for fname, pw in forms(x):
            for md in ('sha256', 'md5'):
                for cn, raw in {**LOCKED, **SOLVED}.items():
                    p, body = dec(raw, pw, md); tests += 1
                    if p:
                        pads += 1
                        r = judge(body, p)
                        flags.append((cn, fname, md, r or 'unranked', x, p, body.hex()))
    return tests, pads, flags

if __name__ == '__main__':
    controls(); print('controls fired: key1, phase2, phase3, phase3.2 open under hex/sha256 and are recognised')
    cands = []
    for f in sys.argv[1:]:
        for l in open(f, encoding='utf-8'):
            l = l.rstrip('\n')
            if l and not l.startswith('#'): cands.append(l)
    cands = list(dict.fromkeys(cands))
    t, p, fl = run(cands)
    print('candidates %d, decrypts %d, valid pads %d (expected ~%.1f)' % (len(cands), t, p, t / 255.))
    fl.report()
    fl.emit()

    sys.exit(2 if fl.omitted else 0)
