#!/usr/bin/env python3
"""Reproduces the numbers quoted in reply-to-agent-3_2026-10-17.md.
Usage: python3 check_report3_2026-10-17.py <dir with faed.txt dbbi.txt matrix.json architect_letters_1539.txt salphaseion_short.b64>
Needs only the standard library plus an `openssl` binary for the last check."""
import sys, os, json, hashlib, itertools, subprocess, base64

D = sys.argv[1] if len(sys.argv) > 1 else '.'
P = lambda n: os.path.join(D, n)
faed = open(P('faed.txt')).read().strip(); dbbi = open(P('dbbi.txt')).read().strip()
m = json.load(open(P('matrix.json'))); bg = m['bit_grid']
pc = [r.count('1') for r in bg]; print('row popcounts', pc, 'sum', sum(pc))

rem = 'difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea'
dig = ''.join(str(ord(c) - 96) for c in rem); v = int(dig)
print('remainder digits', dig); print('as bytes', v.to_bytes((v.bit_length() + 7) // 8, 'big').hex())
print('prime-token digits', ''.join('25' if c == 'Y' else '2' for c in 'BBBBYBBBYYBBBBYBBYYBBYY'))
gi = [i for i, c in enumerate(rem) if c == 'g']; hist = {}; full = 0
for mask in range(1 << len(gi)):
    d = list(dig)
    for j, i in enumerate(gi):
        if mask >> j & 1: d[i] = '0'
    n = int(''.join(d)); bb = n.to_bytes((n.bit_length() + 7) // 8, 'big'); k = 0
    for x in reversed(bb):
        if 0x20 <= x <= 0x7e: k += 1
        else: break
    full += k == len(bb); hist[k] = hist.get(k, 0) + 1
print('g=0/7 on remainder: %d assignments, fully printable %d, longest printable suffix histogram %s' % (1 << len(gi), full, sorted(hist.items())))
print('remainder split on b:', [len(p) for p in rem.split('b')],
      '; placements of 2 b among 60 giving lengths {16,19,23}: %d of %d' % (
          sum(sorted((i, j - i - 1, 60 - j - 1)) == [16, 19, 23] for i, j in itertools.combinations(range(60), 2)), 60 * 59 // 2))

n1 = int(''.join(str(ord(c) - 96) for c in faed)); fb = n1.to_bytes(237, 'big')
print('faed a=1..9: first 4 bytes %s, last 4 %s, printable %d/237' % (fb[:4].hex(), fb[-4:].hex(), sum(0x20 <= x <= 0x7e for x in fb)))
d = [ord(c) - 96 for c in faed]
for p in (1, 3, 551, 557, 561, 563): d[p - 1] = 0
n = int(''.join(map(str, d))); bb = n.to_bytes((n.bit_length() + 7) // 8, 'big')
print('six-position mask: %d bytes, starts %r, ends %r, printable %d, interior %d/%d, sha256 %s' % (
    len(bb), bb[:4], bb[-4:], sum(0x20 <= x <= 0x7e for x in bb), sum(0x20 <= x <= 0x7e for x in bb[3:-3]), len(bb) - 6, hashlib.sha256(bb).hexdigest()))

def bif(ct, sq):
    co = []
    for ch in ct:
        i = sq.index(ch); co += [i // 5, i % 5]
    return ''.join(sq[co[i] * 5 + co[len(ct) + i]] for i in range(len(ct)))
hits = []
for perm in itertools.permutations('dbifhcega'):
    sq = ''.join(perm) + 'klmnopqrstuvwxyz'; out = ''
    for a, b in zip(faed[:4], faed[285:289]):
        ia, ib = sq.index(a), sq.index(b); out += sq[(ia // 5) * 5 + ib // 5] + sq[(ia % 5) * 5 + ib % 5]
    if out[:7] == 'btcseed': hits.append(sq)
print('of 362,880 orderings of the nine dbbi letters, squares giving btcseed:', len(hits), [h[:9] for h in hits], 'continuations', set(bif(faed, h)[:8] for h in hits))

url = b'gsmg.io/theseedisplanted'; lsb = ''.join(str(x & 1) for x in url); ins = lsb[:20] + '1' + lsb[20:]
print('URL LSBs', lsb, '; with 1 inserted at position 21, first 23 bits', ins[:23], 'unused', ins[23:],
      '; equals B=1,Y=0 of the 23 hosts:', ''.join('1' if c == 'B' else '0' for c in 'BBBBYBBBYYBBBBYBBYYBBYY') == ins[:23])

def h160(b): return hashlib.new('ripemd160', hashlib.sha256(b).digest()).hexdigest()
print('target compressed h160', h160(bytes.fromhex('03f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464')))
print('target uncompressed h160', h160(bytes.fromhex('04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559')))
print('key 1 uncompressed h160', h160(bytes.fromhex('0479be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8')))

s = open(P('architect_letters_1539.txt')).read().strip()
print('Architect letters %d, SELECT at %d, CHOICE %d, CHOOSE %d' % (len(s), s.find('SELECT'), s.count('CHOICE'), s.count('CHOOSE')))

raw = base64.b64decode(''.join(open(P('salphaseion_short.b64')).read().split()))
pt = subprocess.run(['openssl', 'enc', '-d', '-aes-256-cbc', '-md', 'md5', '-nopad', '-pass',
                     'pass:matrixsumlistenterlastwordsbeforearchichoicethispasswordmatrixsumlist'], input=raw, capture_output=True).stdout
u = pt[:-pt[-1]] if 1 <= pt[-1] <= 16 and pt[-pt[-1]:] == bytes([pt[-1]]) * pt[-1] else None
print('community password on SalPhaseIon short (EVP-MD5): pad byte %d, plaintext %s bytes, printable %s, sha256 %s' % (
    pt[-1], len(u) if u else None, sum(0x20 <= x <= 0x7e for x in u) if u else None, hashlib.sha256(u).hexdigest() if u else None))
