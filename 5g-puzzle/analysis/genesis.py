#!/usr/bin/env python3
"""The creator sends you to Bitcoin's own raw data twice.

Phase 2: "a chancellor awaiting banks to be bailed out decided to write an
anarchist digital answer to this worlds' misery. Its' raw data after 4 on row
1616" -- line 1616 of Satoshi's source, holding the genesis coinbase scriptSig.

Phase 3.2 (Architect): "THAT WHAT A WISE MAN ABOVE HINTED AT IS WORTH HUNDRED
FOURTY OF THE INVESTMENT" -- and the genesis message as 0x-prefixed hex is
exactly 140 characters.

The genesis block is reconstructed from protocol constants and verified by its
own hash, so none of this is recalled. Every derivable form of it goes through
the on-chain gate against the three remaining envelopes."""
import base64, hashlib, re, struct, time
from pathlib import Path
from Crypto.Cipher import AES
from gate import fullcheck, structure

MSG = b'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks'
SS  = bytes.fromhex('04ffff001d0104') + bytes([len(MSG)]) + MSG
tx  = struct.pack('<I',1) + b'\x01' + b'\x00'*32 + b'\xff'*4 + bytes([len(SS)]) + SS + b'\xff'*4
PK  = bytes.fromhex('4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb6'
                    '49f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac')
tx += b'\x01' + struct.pack('<Q', 5_000_000_000) + bytes([len(PK)]) + PK + struct.pack('<I',0)
MERKLE = hashlib.sha256(hashlib.sha256(tx).digest()).digest()
HDR = struct.pack('<I',1) + b'\x00'*32 + MERKLE + struct.pack('<III',1231006505,0x1d00ffff,2083236893)
GHASH = hashlib.sha256(hashlib.sha256(HDR).digest()).digest()[::-1].hex()
assert GHASH == '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f', 'genesis reconstruction failed'
RAW = HDR + b'\x01' + tx

FS = Path('/home/user/applelamps/puzle/fresh-start')
h = FS.joinpath('archives/salphaseion_phase3.html').read_text()
s = re.sub(r'\s','',re.findall(r'<textarea[^>]*>(.*?)</textarea>',h,re.S)[0])
i = s.find('U2FsdGVkX18'); t = s[i:].replace('shabefanstoo','')
m = re.search(r'[ab]{20,}', t)
A = base64.b64decode(t[:m.start()] + t[m.end():])
B = base64.b64decode(re.sub(r'\s','',Path('/tmp/claude-0/final.b64').read_text()))
C = base64.b64decode(re.sub(r'\s','',FS.joinpath('ciphertexts/salphaseion_cosmic.b64').read_text()))
TGT = {'inner':(A[8:16],A[16:]), 'terminal':(B[8:16],B[16:]), 'cosmic':(C[8:16],C[16:])}

def dec(pw, salt, ct, dg):
    hf = hashlib.sha256 if dg=='sha256' else hashlib.md5
    d=b''; p=b''
    while len(d)<48: p=hf(p+pw+salt).digest(); d+=p
    return AES.new(d[:32], AES.MODE_CBC, d[32:48]).decrypt(ct)

txt = MSG.decode()
BASE = set()
for v in [txt, txt.lower(), txt.upper(), re.sub(r'[^A-Za-z0-9]','',txt).lower(),
          txt[::-1], MSG.hex(), MSG.hex().upper(), '0x'+MSG.hex(), '0X'+MSG.hex().upper(),
          MSG[::-1].hex(), '0x'+MSG[::-1].hex(), MSG.hex()[::-1],
          SS.hex(), '0x'+SS.hex(), SS.hex()[7*2:], SS.hex()[8*2:],   # "after 4" -- past the 04ffff001d0104 push
          RAW.hex(), HDR.hex(), tx.hex(), GHASH, '0x'+GHASH,
          MERKLE[::-1].hex(), '0x'+MERKLE[::-1].hex(),
          '1231006505','2083236893','486604799','1d00ffff','0x1d00ffff','1616','140','69']:
    BASE.add(v)
EXTRA = ['','479','yellowblueprimes','yinyang','matrixsumlist','lastwordsbeforearchichoice',
         'wewontgiveawaythepassword','itsinfrontofyoureyesbutyourenotseeingit',
         'verylaststepisatruegiveawaypromised','causality','enter','halfandbetterhalf']
ALL = set(BASE)
for b in BASE:
    for e in EXTRA:
        if e: ALL.add(b+e); ALL.add(e+b)

def pwforms(c):
    b = c.encode('utf-8','ignore')
    yield b; yield hashlib.sha256(b).hexdigest().encode()
    d = b
    for _ in range(4):
        d = hashlib.sha256(d).digest()
        yield d; yield d.hex().encode()

print(f'genesis reconstruction verified by hash: {GHASH}')
print(f'{len(ALL)} candidate strings\n')
n=0; found=[]; t0=time.time()
for c in sorted(ALL):
    for pw in pwforms(c):
        for tn,(salt,ct) in TGT.items():
            for dg in ('sha256','md5'):
                blk = dec(pw, salt, ct, dg); n += 1
                hits = fullcheck(blk, f'{tn}/{c[:40]!r}/{dg}')
                if hits:
                    found += hits
                    for x in hits: print('***', x, flush=True)
                st = structure(blk)
                if st: print(f'  structure {st} {tn} {c[:44]!r} {dg}', flush=True)
print(f'\n{len(ALL)} candidates, {n} decrypts, {time.time()-t0:.0f}s')
print(f'prize-key matches: {len(found)}')
