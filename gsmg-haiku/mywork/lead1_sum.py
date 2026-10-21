"""Lead 1: 91-digit run (SalPhaseIon textarea offset 0-90) vs 91-letter checkerboard plaintext.
Hypothesis: 'matrixsumlist' = elementwise sum/difference of the digit list and the letter list.
Plus 570-digit run vs the first 570 letters of the Architect text.
Score = count of common English bigrams/trigrams; control = plant a known message with the same operation."""
import itertools, random
from lib import *
t = re.sub(r'\s', '', open(F + r'\salphaseion-textarea.txt').read())
D = r'c:\gsmg-puzzle-clean\derived'
d91 = [ord(c) - 96 for c in t[0:91]]
d570 = [ord(c) - 96 for c in t[195:765]]
cb = open(D + r'\checkerboard-plaintext.txt').read().strip()
arch = open(D + r'\architect-text.txt').read().strip()
WORDS = ['THE', 'AND', 'ING', 'ION', 'ENT', 'ER', 'TH', 'HE', 'IN', 'AN', 'RE', 'ND', 'OU', 'EN', 'ON']
def score(s):
    return sum(s.count(w) * len(w) for w in WORDS) / max(1, len(s))
def ops(text, key):
    n = min(len(text), len(key))
    T = [ord(c) - 65 for c in text[:n]]
    out = {}
    for off_t, off_k in itertools.product((0, 1), (0, 1)):
        for name, f in (('T+K', lambda a, b: a + b), ('T-K', lambda a, b: a - b), ('K-T', lambda a, b: b - a)):
            s = ''.join(chr(65 + f(a + off_t, b + off_k - 0) % 26) for a, b in zip(T, key[:n]))
            out[(name, off_t, off_k)] = s
    return out
def run(label, text, key):
    res = sorted(((score(s), k, s) for k, s in ops(text, key).items()), reverse=True)
    print(label, [(round(a, 2), k) for a, k, _ in res[:3]], res[0][2][:60])
    return res
base = run('cb+d91', cb, d91)
base = run('arch570+d570', arch, d570)
# control: plant known plaintext encrypted with T+K and confirm we recover it as top
random.seed(1)
pt = cb
key = d91
enc = ''.join(chr(65 + (ord(c) - 65 + k) % 26) for c, k in zip(pt, key))
res = run('control(T-K recovers cb)', enc, key)
print('control top is plaintext:', res[0][2] == cb)
# raw stats: is d91 / d570 distribution consistent with random or with plaintext?
from collections import Counter
for nm, d in (('d91', d91), ('d570', d570)):
    c = Counter(d); n = len(d)
    ic = sum(v * (v - 1) for v in c.values()) / (n * (n - 1))
    print(nm, 'IC', round(ic, 4), 'uniform-9 would be 0.111', sorted(c.items()))
# digit-pair / repeats in d570 (periodicity)
s570 = ''.join(map(str, d570))
for p in range(1, 60):
    m = sum(s570[i] == s570[i + p] for i in range(len(s570) - p)) / (len(s570) - p)
    if m > 0.16: print('period', p, round(m, 3))
