"""Whole-number targets that are not tail-separable: decimal -> base 26/27/36/58/64/85/94/95 text.
Zero variants: none, or every g / i / e (and combinations) read as 0. English-ness = fraction of letters+space
and best 4-gram hit count against a word list of puzzle-relevant words."""
import itertools, re, string, pydoc_data.topics as T
A26 = string.ascii_lowercase
ALPH = {'b26a0': A26, 'b26a1': None, 'b27': ' ' + A26, 'b36': string.digits + A26, 'b36l': A26 + string.digits,
        'b58': '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz',
        'b64': string.ascii_uppercase + A26 + string.digits + '+/', 'b85': ''.join(chr(33+i) for i in range(85)),
        'b94': ''.join(chr(33+i) for i in range(94)), 'b95': ''.join(chr(32+i) for i in range(95))}
words = set(w for w in re.findall(r'[a-z]{5,}', (' '.join(T.topics.values()) + open('matrix-reloaded.txt', encoding='utf-8').read()).lower()))
def conv(N, name):
    if name == 'b26a1':            # bijective base 26 (a=1..z=26)
        s = ''
        while N > 0: N, r = divmod(N-1, 26); s = A26[r] + s
        return s
    a = ALPH[name]; b = len(a); s = []
    while N: N, r = divmod(N, b); s.append(a[r])
    return ''.join(reversed(s))
def hits(s):
    s = s.lower(); return sorted({s[i:i+k] for k in (5, 6, 7, 8) for i in range(len(s)-k+1)} & words)
t = open('files/salphaseion-textarea.txt').read().strip()
r1 = t[:91]; r2 = t[195:765]; best = []
import random; random.seed(2)
def run(r):
    out = []
    for k in range(4):
        for zl in itertools.combinations('gie', k):
            N = int(''.join('0' if c in zl else str(ord(c)-96) for c in r))
            for name in ALPH:
                for s in (conv(N, name),): out.append((len(hits(s)), ''.join(zl) or '-', name, s))
    return out
for nm, r in (('r1', r1), ('r1rev', r1[::-1]), ('r2', r2), ('r2rev', r2[::-1]), ('r1+r2', r1+r2)):
    res = sorted(run(r), reverse=True)
    sh = list(r); random.shuffle(sh); null = max(x[0] for x in run(''.join(sh)))
    h, zl, name, s = res[0]
    print(f'{nm}: best word-hit count {h} (zeros={zl}, {name}); shuffled-string best {null}; hits {hits(s)[:8]}; text {s[:70]!r}')
