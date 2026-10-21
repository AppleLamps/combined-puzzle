"""Zero-insertion (deleted zeros) and zero-replacement (disguised zeros) tail-first beam search with a
case/space/punctuation-aware character 4-gram model. Allowed bytes: printable ASCII."""
import sys, re, math, heapq, itertools, pydoc_data.topics as T
from collections import Counter
corpus = ' '.join(T.topics.values()) + (open('matrix-reloaded.txt', encoding='utf-8').read()
    + open('mywork/wikiquote_reloaded.txt', encoding='utf-8', errors='ignore').read()
    + open('derived/phase2-plaintext.txt', errors='ignore').read() + open('derived/phase3-plaintext.txt', errors='ignore').read()[:726])*3
L = re.sub(r'\s+', ' ', corpus); L = ''.join(c for c in L if 32 <= ord(c) < 127)
qc = Counter(L[i:i+4] for i in range(len(L)-3)); tc = Counter(L[i:i+3] for i in range(len(L)-2))
bc = Counter(L[i:i+2] for i in range(len(L)-1)); uc = Counter(L); NL = len(L)
def q(s):   # interpolated log P(s[0] | s[1:4]) (text is built right-to-left)
    p = 0.01/95 + 0.04*uc.get(s[0], 0)/NL
    if bc.get(s[:2]): p += 0.10*bc[s[:2]]/uc[s[1]]
    if tc.get(s[:3]): p += 0.25*tc[s[:3]]/bc[s[1:3]]
    if qc.get(s): p += 0.60*qc[s]/tc[s[1:]]
    return math.log(p)
PR = set(range(32, 127))
def search(r, mode, zl='', beam=3000, maxz=3, label='', final_ok=PR):
    d = [ord(c)-96 for c in r]; n = len(d)
    P10 = [10**i for i in range(8)]
    cache = {}
    def gen(p):
        if p in cache: return cache[p]
        out = []
        if mode == 'insert':
            for m in range(256):
                k = bin(m).count('1')
                if k > maxz: continue
                j = p; v = 0
                for i in range(8):            # i = power of ten
                    if (m >> i) & 1: continue
                    if j == 0: continue
                    j -= 1; v += d[j]*P10[i]
                if j == p: continue
                out.append((v, j, k*math.log(0.1) + (8-k)*math.log(0.9)))
        else:
            lo = max(0, p-8); seg = d[lo:p]; idx = [i for i in range(len(seg)) if r[lo+i] in zl]
            for bits in itertools.product((0, 1), repeat=len(idx)):
                dd = seg[:]
                for i, b in zip(idx, bits):
                    if b: dd[i] = 0
                v = int(''.join(map(str, dd)))
                out.append((v, lo, sum(bits)*math.log(0.5) + (len(idx)-sum(bits))*math.log(0.5)))
        cache[p] = out; return out
    states = [(0.0, n, 0, '')]; done = []; k = 0
    while states:
        f5 = pow(5, 8*k); f5l = f5 & 0xFF; cand = {}
        for sc, p, c, txt in states:
            cl = c & 0xFF
            for v, p2, pri in gen(p):
                b = (v*f5l + cl) & 0xFF
                if b not in PR: continue
                t2 = chr(b) + txt
                s2 = sc + pri + q((t2+'   ')[:4])
                key = (p2, t2, v, c)
                if key not in cand or cand[key][0] < s2: cand[key] = (s2, c, v, p2, t2)
        states = []
        for s2, c, v, p2, t2 in heapq.nlargest(beam, cand.values(), key=lambda x: x[0]):
            c2 = (v*f5 + c) >> 8
            if p2 == 0:
                rest = c2.to_bytes((c2.bit_length()+7)//8, 'big')
                if all(x in PR for x in rest): done.append((s2, rest.decode() + t2))
            else: states.append((s2, p2, c2, t2))
        k += 1
        if states and k % 40 == 0: print(label, 'bytes', k, 'best', repr(states[0][3][:90]), flush=True)
    done.sort(reverse=True)
    print(label, 'finished at', k, 'bytes: complete solutions', len(done), flush=True)
    for s, t in done[:3]: print('   %.2f/char' % (s/len(t)), repr(t[:400]), flush=True)
def enc(s): return str(int.from_bytes(s.encode(), 'big'))
A = 'abcdefghi'
T2 = "Well done, you found the hidden zeros. Take the seven numbers from the yellow squares and the fifteen from the blue ones, keep only the primes, add each row of the grid and write the totals down. That list opens the second door, friend."
c1 = enc(T2); print(len(T2), len(c1))
search(''.join(A[int(x)-1] for x in c1 if x != '0'), 'insert', beam=20000, label='long-control-insert')
search(''.join('g' if x == '0' else A[int(x)-1] for x in c1), 'replace', 'gie', label='long-control-replace')
