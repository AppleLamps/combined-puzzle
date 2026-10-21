"""Zero hypotheses (deleted / disguised as g,i,e / none) with other target encodings of the decimal number:
 le   : bytes little-endian ASCII          ebc : big-endian bytes read as EBCDIC cp273 (used in Phase 3.2)
 b7   : 7-bit ASCII groups, big-endian     b7le: 7-bit groups little-endian
Tail-first beam search; chunk of w bits needs w more decimal digits."""
import sys, re, math, heapq, itertools, pydoc_data.topics as T
from collections import Counter
ENC = sys.argv[1]
W = 7 if ENC.startswith('b7') else 8
LE = ENC.endswith('le')
corpus = ' '.join(T.topics.values()) + (open('matrix-reloaded.txt', encoding='utf-8').read()
    + open('mywork/wikiquote_reloaded.txt', encoding='utf-8', errors='ignore').read()
    + open('derived/phase2-plaintext.txt', errors='ignore').read() + open('derived/phase3-plaintext.txt', errors='ignore').read()[:726])*3
L = re.sub(r'\s+', ' ', corpus); L = ''.join(c for c in L if 32 <= ord(c) < 127)
if LE: L = L[::-1]          # generation order is left-to-right; model the reversed string
qc = Counter(L[i:i+4] for i in range(len(L)-3)); tc = Counter(L[i:i+3] for i in range(len(L)-2))
bc = Counter(L[i:i+2] for i in range(len(L)-1)); uc = Counter(L); NL = len(L)
def q(s):
    p = 0.01/95 + 0.04*uc.get(s[0], 0)/NL
    if bc.get(s[:2]): p += 0.10*bc[s[:2]]/uc[s[1]]
    if tc.get(s[:3]): p += 0.25*tc[s[:3]]/bc[s[1:3]]
    if qc.get(s): p += 0.60*qc[s]/tc[s[1:]]
    return math.log(p)
if ENC == 'ebc':
    MAP = {}
    for b in range(256):
        ch = bytes([b]).decode('cp273')
        if 32 <= ord(ch) < 127: MAP[b] = ch
    def tobytes(s): return s.encode('cp273')
else:
    MAP = {b: chr(b) for b in range(32, 127)}
    def tobytes(s): return s.encode()
MSK = (1 << W) - 1
def encode(s):
    bs = tobytes(s)
    if LE: bs = bs[::-1]
    v = 0
    for b in bs: v = (v << W) | b
    return str(v)
def search(r, mode, zl='', beam=3000, maxz=3, label=''):
    d = [ord(c)-96 for c in r]; n = len(d)
    P10 = [10**i for i in range(W)]; cache = {}
    def gen(p):
        if p in cache: return cache[p]
        out = []
        if mode == 'insert':
            for m in range(1 << W):
                k = bin(m).count('1')
                if k > maxz: continue
                j = p; v = 0
                for i in range(W):
                    if (m >> i) & 1 or j == 0: continue
                    j -= 1; v += d[j]*P10[i]
                if j == p: continue
                out.append((v, j, k*math.log(0.1) + (W-k)*math.log(0.9)))
        else:
            lo = max(0, p-W); seg = d[lo:p]; idx = [i for i in range(len(seg)) if r[lo+i] in zl]
            for bits in itertools.product((0, 1), repeat=len(idx)):
                dd = seg[:]
                for i, b in zip(idx, bits):
                    if b: dd[i] = 0
                out.append((int(''.join(map(str, dd))), lo, len(idx)*math.log(0.5)))
        cache[p] = out; return out
    states = [(0.0, n, 0, '')]; done = []; k = 0
    while states:
        f5 = pow(5, W*k); f5l = f5 & MSK; cand = {}
        for sc, p, c, txt in states:
            cl = c & MSK
            for v, p2, pri in gen(p):
                ch = MAP.get((v*f5l + cl) & MSK)
                if ch is None: continue
                t2 = ch + txt
                key = (p2, t2, v, c)
                if key not in cand: cand[key] = (sc + pri + q((t2+'   ')[:4]), c, v, p2, t2)
        states = []
        for s2, c, v, p2, t2 in heapq.nlargest(beam, cand.values(), key=lambda x: x[0]):
            c2 = (v*f5 + c) >> W
            if p2 == 0:
                rest = ''; ok = True
                while c2:
                    ch = MAP.get(c2 & MSK); c2 >>= W
                    if ch is None: ok = False; break
                    rest = ch + rest
                if ok:
                    full = rest + t2
                    done.append((s2, full[::-1] if LE else full))
            else: states.append((s2, p2, c2, t2))
        k += 1
    done.sort(reverse=True)
    print(ENC, label, 'steps', k, 'complete solutions', len(done), flush=True)
    for s, t in done[:3]: print('   %.2f/char' % (s/len(t)), repr(t[:300]), flush=True)
A = 'abcdefghi'
T2 = "Well done, you found the hidden zeros. Take the seven numbers from the yellow squares and the fifteen from the blue ones, keep only the primes, add each row of the grid and write the totals down. That list opens the second door, friend."
c1 = encode(T2)
search(''.join(A[int(x)-1] for x in c1 if x != '0'), 'insert', beam=8000, label='CONTROL insert')
search(''.join('g' if x == '0' else A[int(x)-1] for x in c1), 'replace', 'gie', label='CONTROL replace')
t = open('files/salphaseion-textarea.txt').read().strip()
r1 = t[:91]; r2 = t[195:765]
for name, r in (('r1', r1), ('r1rev', r1[::-1]), ('r2', r2), ('r2rev', r2[::-1])):
    search(r, 'replace', '', label=name+' plain')
    search(r, 'replace', 'gie', label=name+' replace-gie')
    search(r, 'insert', beam=8000, label=name+' insert')
