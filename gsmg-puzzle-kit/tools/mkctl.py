#!/usr/bin/env python3
"""Planted controls for the string-form dbbi runs (h3 --dbbi ... --strforms).
Needs ctl_letters.txt from mk.py (a 48-letter stand-in for dbbi with 10 `b`).
Writes pl_dstr.bin (password = sha256 of the digit string with the chosen b's as 0)
and pl_lstr.bin (password = sha256 of the letter string with the chosen b's as `o`).
The chosen b's are a fixed random half of them (seed 7); h3 must recover both.
  ./h3 -c c pl_dstr.bin --dbbi $(cat ctl_letters.txt) --zero 2 --strforms
  ./h3 -c c pl_lstr.bin --dbbi $(cat ctl_letters.txt) --zero 2 --strforms
"""
import hashlib, random
from Crypto.Cipher import AES


def evp(pw, salt):
    d = b''
    prev = b''
    while len(d) < 48:
        prev = hashlib.sha256(prev + pw + salt).digest()
        d += prev
    return d[:32], d[32:48]


def enc(pt, ans, fname, salt=b'12345678'):
    pw = hashlib.sha256(ans).hexdigest().encode()
    k, iv = evp(pw, salt)
    p = 16 - len(pt) % 16
    open(fname, 'wb').write(b'Salted__' + salt + AES.new(k, AES.MODE_CBC, iv).encrypt(pt + bytes([p]) * p))


L = open('ctl_letters.txt').read().strip()
pos = [i for i, c in enumerate(L) if c == 'b']
random.seed(7)
zs = set(random.sample(pos, len(pos) // 2))
D = {c: str(i + 1) for i, c in enumerate('abcdefghi')}
ds = ''.join('0' if i in zs else D[c] for i, c in enumerate(L))
ls = ''.join('o' if i in zs else c for i, c in enumerate(L))
enc(b'planted digit-string control: printable text, pad 1 ok!', ds.encode(), 'pl_dstr.bin')
enc(b'planted letter-string control: printable text, pad 1 ok', ls.encode(), 'pl_lstr.bin')
print('zeroed b positions', sorted(zs))
print('digit string', ds)
print('letter string', ls)
