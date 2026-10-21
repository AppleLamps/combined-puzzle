#!/usr/bin/env python3
"""Plant a control container for any candidate string and password form.
  python3 plant.py OUT.bin CANDIDATE FORM [md]
FORM as in h3 -f: 1 hex(sha256(x)), 2 raw sha256(x), 4 hex(sha256(sha256(x))),
8 hex(sha256(hex(sha256(x)))). md is sha256 (default) or md5 (the EVP digest).
The plaintext is 70 random bytes (seed 11), so the right password gives pad 10 and h3
flags it as pad>=3. Used to prove each run's password path (form, order, mid) is live.
"""
import hashlib, random, sys
from Crypto.Cipher import AES


def evp(pw, salt, md):
    h = getattr(hashlib, md)
    d = b''
    prev = b''
    while len(d) < 48:
        prev = h(prev + pw + salt).digest()
        d += prev
    return d[:32], d[32:48]


def password(x, form):
    d = hashlib.sha256(x).digest()
    if form == 1: return d.hex().encode()
    if form == 2: return d
    if form == 4: return hashlib.sha256(d).hexdigest().encode()
    if form == 8: return hashlib.sha256(d.hex().encode()).hexdigest().encode()
    raise SystemExit('form must be 1, 2, 4 or 8')


out, cand, form = sys.argv[1], sys.argv[2].encode(), int(sys.argv[3])
md = sys.argv[4] if len(sys.argv) > 4 else 'sha256'
random.seed(11)
pt = bytes(random.randrange(256) for _ in range(70))
salt = b'plantctl'
k, iv = evp(password(cand, form), salt, md)
p = 16 - len(pt) % 16
open(out, 'wb').write(b'Salted__' + salt + AES.new(k, AES.MODE_CBC, iv).encrypt(pt + bytes([p]) * p))
print('planted', out, 'form', form, md, 'cand', cand.decode())
