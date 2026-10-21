"""Deleted-zeros variant: r = decimal number with its zeros removed. Tail-first beam search over
zero insertions, decimal -> bytes, scored with an English quadgram model + binomial prior on zeros."""
import sys, re, math, itertools, heapq, pydoc_data.topics as T
import numpy as np
corpus = ' '.join(T.topics.values()) + open('matrix-reloaded.txt', encoding='utf-8').read()*3 \
    + open('mywork/wikiquote_reloaded.txt', encoding='utf-8', errors='ignore').read()*3 + open('derived/architect-text.txt').read()*3
L = re.sub('[^a-z]', '', corpus.lower())
from collections import Counter
qc = Counter(L[i:i+4] for i in range(len(L)-3)); tot = sum(qc.values())
FLOOR = math.log(0.01/tot)
def q(s): 
    c = qc.get(s); return math.log(c/tot) if c else FLOOR
MASKS = [m for m in range(256) if bin(m).count('1') <= 3]
PRI = {m: bin(m).count('1')*math.log(0.1) + (8-bin(m).count('1'))*math.log(0.9) for m in MASKS}
LOW = set(range(97,123))
def search(r, beam=4000, allowed=LOW, label='', verbose=True):
    d = [ord(c)-96 for c in r]; n = len(d)
    segc = {}
    def seg(p, m):
        key = (p, m)
        if key in segc: return segc[key]
        k = bin(m).count('1'); need = 8-k
        if need > p:   # final partial window: pad with leading zeros
            if any((m >> (7-i)) & 1 == 0 for i in range(8-0) if False): pass
        digs = []; j = p
        ok = True
        for i in range(7, -1, -1):          # i = position from left; fill from the right
            if (m >> i) & 1: digs.append(0)
            else:
                if j == 0: digs.append(0)   # ran out: leading zeros
                else: j -= 1; digs.append(d[j])
        v = 0
        for i, x in enumerate(digs): v += x * 10**i
        segc[key] = (v, j); return segc[key]
    states = [(0.0, n, 0, '')]   # score, p, carry, text
    done = []
    k = 0
    while states:
        f5 = pow(5, 8*k); f5l = f5 & 0xFF
        cand = {}
        for sc, p, c, txt in states:
            cl = c & 0xFF
            for m in MASKS:
                v, p2 = seg(p, m)
                if p2 == p: continue
                b = (v*f5l + cl) & 0xFF
                if b not in allowed: continue
                ch = chr(b); t2 = ch + txt
                s2 = sc + PRI[m] + (q(t2[:4]) if len(t2) >= 4 else -3.0)
                key = (p2, t2, v, c)
                if key not in cand or cand[key][0] < s2: cand[key] = (s2, p, c, v, p2, t2)
        nxt = heapq.nlargest(beam, cand.values(), key=lambda x: x[0])
        states = []
        for s2, p, c, v, p2, t2 in nxt:
            c2 = (v*f5 + c) >> 8
            if p2 == 0:
                rest = c2.to_bytes((c2.bit_length()+7)//8, 'big')
                if all(x in allowed for x in rest): done.append((s2, rest.decode() + t2))
            else: states.append((s2, p2, c2, t2))
        k += 1
        if verbose and states and k % 20 == 0:
            print(label, 'bytes', k, 'beam', len(states), 'best', states[0][3][:70], flush=True)
    done.sort(reverse=True)
    print(label, 'finished: complete solutions', len(done))
    for s, t in done[:5]: print('   %.1f/char' % (s/len(t)), t[:300])
    return done
t = open('files/salphaseion-textarea.txt').read().strip()
r1 = t[:91]; r2 = t[195:765]
search(t[766:829].replace('o',''), label='control1')
search(t[830:859].replace('o',''), label='control2')
for name, r in (('r1', r1), ('r1rev', r1[::-1]), ('r2', r2), ('r2rev', r2[::-1])):
    search(r, label=name)
