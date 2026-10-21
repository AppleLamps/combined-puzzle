import re, pydoc_data.topics as T
words = set(re.findall(r'[a-z]{4,}', (' '.join(T.topics.values()) + open('matrix-reloaded.txt', encoding='utf-8').read()).lower()))
t = open('files/salphaseion-textarea.txt').read().strip()
blocks = {'765': t[:765], 'r1+r2': t[:91]+t[195:765], 'r1': t[:91], 'r2': t[195:765], 'ab+r2': t[91:765], 'r1+ab': t[:195]}
masks = {'all': set(range(1,10)), 'primes': {2,3,5,7}, 'primes+1': {1,2,3,5,7}, 'nonprime': {1,4,6,8,9}, 'comp': {4,6,8,9}}
def hits(s):
    s = s.lower(); return {s[i:i+k] for k in (4,5,6,7) for i in range(len(s)-k+1)} & words
rows = []
for bn, b in blocks.items():
    d = [ord(c)-96 for c in b]; n = len(d)
    for mn, m in masks.items():
        v = [x if x in m else 0 for x in d]
        for w in range(2, n):
            if n % w: continue
            h = n//w
            rs = [sum(v[i*w:(i+1)*w]) for i in range(h)]; cs = [sum(v[j::w]) for j in range(w)]
            for kind, s in (('row', rs), ('col', cs)):
                outs = {'ascii': ''.join(chr(x) if 32 <= x < 127 else '~' for x in s),
                        'a1z26': ''.join(chr(96+x) if 1 <= x <= 26 else '~' for x in s),
                        'mod26a0': ''.join(chr(97+x%26) for x in s), 'mod26a1': ''.join(chr(97+(x-1)%26) for x in s)}
                for on, o in outs.items():
                    if o.count('~') > len(o)*0.2: continue
                    rows.append((len(hits(o))/max(1,len(o))**0.5, bn, mn, f'{h}x{w}', kind, on, o[:90], sorted(hits(o))[:5]))
rows.sort(reverse=True); print(len(rows), 'decodings')
for r in rows[:12]: print(r)
