#!/usr/bin/env python3
"""Doc 120 s2: "some characters need to be zeroed out". Each locked container's base64
with one character substituted (all 64 base64 values, plus '='), or deleted, or one
character inserted ('A'), decrypted under the five known passwords (as hex, the chain's
convention) and both EVP digests, AES-256-CBC; every valid padding through the
recogniser. Planted control: a corrupted copy of a container encrypted under a known
password, restored by the sweep.
"""
import base64, hashlib, os, random, sys, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '115'))
import harness as H
from Crypto.Cipher import AES
B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
SUBS = B64 + '='  # the substitution alphabet: every base64 value and the padding character
KNOWN = ['5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75', 'eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf',
         '1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5', '250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c',
         '89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32']
TERMINAL = ("U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46zgKlIi8aaqY5gpJPP" "EzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4")
SALSHORT = ("U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9zQvX0t8v3jPB4okps" "pxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ")
COSMIC = open(os.path.join(HERE, '..', '115', 'data', 'cosmic.b64')).read().replace('\n', '')

def variants(b64):
    yield ('orig', b64)
    for i in range(len(b64)):
        for ch in SUBS:
            if ch != b64[i]: yield (f'sub{i}{ch}', b64[:i] + ch + b64[i + 1:])
        yield (f'del{i}', b64[:i] + b64[i + 1:])
        yield (f'ins{i}A', b64[:i] + 'A' + b64[i:])

def decode(b64):
    s = b64 + '=' * (-len(b64) % 4)
    try: return base64.b64decode(s)
    except Exception: return None

def work(args):
    name, b64, pws = args
    out = []; n = 0
    for lab, v in variants(b64):
        raw = decode(v)
        if raw is None or len(raw) < 32 or (len(raw) - 16) % 16 or not raw.startswith(b'Salted__'): continue
        for pw in pws:
            for md in ('sha256', 'md5'):
                n += 1; r = H.try_open(raw, pw.encode(), md)
                if r:
                    pad, pt = r; why = H.recognise(pt, pad)
                    if why: out.append((name, lab, pw[:8], md, pad, why, pt[:40]))
    return name, n, out

if __name__ == '__main__':
    # planted control: encrypt random bytes under KNOWN[0], then corrupt one base64 char
    r = random.Random(120); salt = r.randbytes(8); pt = r.randbytes(60)
    k, iv = H.evp(KNOWN[0].encode(), salt, hashlib.sha256)
    ctl = b'Salted__' + salt + AES.new(k, AES.MODE_CBC, iv).encrypt(pt + bytes([4]) * 4)
    ctl64 = base64.b64encode(ctl).decode().rstrip('='); i = 50; ctl64 = ctl64[:i] + ('B' if ctl64[i] != 'B' else 'C') + ctl64[i + 1:]
    jobs = [('CONTROL', ctl64, KNOWN), ('salshort', SALSHORT, KNOWN), ('terminal', TERMINAL, KNOWN), ('cosmic', COSMIC, KNOWN)]
    with mp.get_context('spawn').Pool(4) as pool:
        for name, n, out in pool.imap_unordered(work, jobs):
            print(f'[{name}] decrypts {n} flags {len(out)}', flush=True)
            for o in out: print('  ', o, flush=True)
