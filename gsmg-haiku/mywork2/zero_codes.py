"""Zero hypotheses with code-per-character targets (not one big number):
 a1z26 (a=1..z=26), a0z25, asc (decimal ASCII 32..126), asclow (decimal ASCII a-z + space).
Modes: plain (no zeros), insert (zeros were deleted), replace (g/i/e may stand for 0).
Best segmentation under a 4-gram model; compared with shuffles of the same string (null)."""
import re, math, heapq, random, pydoc_data.topics as T
from collections import Counter
corpus = ' '.join(T.topics.values()) + (open('matrix-reloaded.txt', encoding='utf-8').read()
    + open('mywork/wikiquote_reloaded.txt', encoding='utf-8', errors='ignore').read()
    + open('derived/phase2-plaintext.txt', errors='ignore').read() + open('derived/phase3-plaintext.txt', errors='ignore').read()[:726])*3
P = re.sub(r'\s+', ' ', corpus); P = ''.join(c for c in P if 32 <= ord(c) < 127)
def model(L, nsym):
    qc = Counter(L[i:i+4] for i in range(len(L)-3)); tc = Counter(L[i:i+3] for i in range(len(L)-2))
    bc = Counter(L[i:i+2] for i in range(len(L)-1)); uc = Counter(L); NL = len(L)
    def q(s):   # P(s[-1] | previous)
        p = 0.01/nsym + 0.04*uc.get(s[-1], 0)/NL
        if len(s) >= 2 and bc.get(s[-2:]): p += 0.10*bc[s[-2:]]/uc[s[-2]]
        if len(s) >= 3 and tc.get(s[-3:]): p += 0.25*tc[s[-3:]]/bc[s[-3:-1]]
        if len(s) >= 4 and qc.get(s): p += 0.60*qc[s]/tc[s[:3]]
        return math.log(p)
    return q
LOW = re.sub(r'[^a-z]+', '', P.lower()); LOWSP = re.sub(r' +', ' ', re.sub(r'[^a-z ]+', ' ', P.lower()))
TABLES = {
 'a1z26':  ({chr(97+i): str(i+1) for i in range(26)}, model(LOW, 26)),
 'a0z25':  ({chr(97+i): str(i) for i in range(26)}, model(LOW, 26)),
 'asclow': ({**{chr(c): str(c) for c in range(97, 123)}, ' ': '32'}, model(LOWSP, 27)),
 'asc':    ({chr(c): str(c) for c in range(32, 127)}, model(P, 95)),
}
def segment(digs, letters, table, q, mode, zl='gie', beam=2000):
    n = len(digs); match = [[] for _ in range(n)]
    for ch, code in table.items():
        pat = code.replace('0', '') if mode == 'insert' else code
        if not pat or (mode == 'plain' and '0' in code): continue
        for p in range(n - len(pat) + 1):
            if mode == 'replace':
                ok = all(pat[i] == digs[p+i] or (pat[i] == '0' and letters[p+i] in zl) for i in range(len(pat)))
            else: ok = digs.startswith(pat, p)
            if ok: match[p].append((ch, len(pat)))
    layers = [dict() for _ in range(n+1)]; layers[0][''] = (0.0, '')
    for p in range(n):
        if not layers[p]: continue
        for k3, (sc, txt) in heapq.nlargest(beam, layers[p].items(), key=lambda kv: kv[1][0]):
            for ch, ln in match[p]:
                s2 = sc + q(k3 + ch); k2 = (k3 + ch)[-3:]
                cur = layers[p+ln].get(k2)
                if cur is None or s2 > cur[0]: layers[p+ln][k2] = (s2, txt + ch)
    if not layers[n]: return None
    sc, txt = max(layers[n].values()); return sc/len(txt), sc/n, txt
def enc(s, table, mode):
    d = ''.join(table[c] for c in s)
    if mode == 'insert': d = d.replace('0', '')
    return d
A = 'abcdefghi'
PLAIN = "well done you found the hidden zeros take the seven numbers from the yellow squares and the fifteen from the blue ones keep only the primes add each row of the grid and write the totals down that list opens the second door friend"
t = open('files/salphaseion-textarea.txt').read().strip()
r1 = t[:91]; r2 = t[195:765]
random.seed(1)
for tn, (table, q) in TABLES.items():
    for mode in ('plain', 'insert', 'replace'):
        if tn == 'a0z25' and mode == 'plain': continue
        # control: same-table encoding of English (replace mode: zeros shown as 'g')
        src = PLAIN if ' ' in table else PLAIN.replace(' ', '')
        if mode == 'plain': src = ''.join(c for c in src if '0' not in table[c])
        d = enc(src, table, mode); lets = ''.join('g' if x == '0' else A[int(x)-1] for x in d)
        dd = ''.join(str(ord(c)-96) for c in lets) if mode == 'replace' else d
        res = segment(dd, lets, table, q, mode)
        print(f'[{tn} {mode}] CONTROL per-digit {res[1]:.3f} acc {sum(a==b for a,b in zip(res[2],src))/len(src):.2f} {res[2][:70]!r}', flush=True)
        for name, r in (('r1', r1), ('r1rev', r1[::-1]), ('r2', r2), ('r2rev', r2[::-1])):
            digs = ''.join(str(ord(c)-96) for c in r)
            res = segment(digs, r, table, q, mode)
            null = []
            for _ in range(8):
                sh = list(r); random.shuffle(sh); sh = ''.join(sh)
                x = segment(''.join(str(ord(c)-96) for c in sh), sh, table, q, mode)
                if x: null.append(x[1])
            ns = ('%.3f..%.3f' % (min(null), max(null))) if null else 'none'
            if res: print(f'   {name}: per-digit {res[1]:.3f} (shuffle null {ns})  {res[2][:90]!r}', flush=True)
            else: print(f'   {name}: no segmentation (null {ns})', flush=True)
