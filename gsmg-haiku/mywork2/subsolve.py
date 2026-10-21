"""Free monoalphabetic solve of r1's b/e-checkerboard symbols (simulated annealing, letter 4-gram model), with
same-length controls, shuffle nulls and crib dragging.  usage: subsolve.py control | main <seqname> | crib <seqname>"""
import sys, re, math, random, numpy as np, pydoc_data.topics as T
PY = sys.base_prefix
def letters(s): return re.sub('[^a-z]', '', s.lower())
corp = letters(' '.join(T.topics.values())) + letters(open(PY + '/LICENSE.txt', encoding='utf-8', errors='ignore').read())
news = ' '.join(w for w in re.findall(r"[A-Za-z']+", open(PY + '/NEWS.txt', encoding='utf-8', errors='ignore').read()) if w.islower())
mat = letters(open('matrix-reloaded.txt', encoding='utf-8').read() + open('mywork/wikiquote_reloaded.txt', encoding='utf-8', errors='ignore').read()
              + open('derived/phase2-plaintext.txt', errors='ignore').read() + open('derived/phase3-plaintext.txt', errors='ignore').read()[:726]
              + open('derived/architect-text.txt').read() + open('derived/checkerboard-plaintext.txt').read())
corp = corp + letters(news) + mat*5
a = np.frombuffer(corp.encode(), dtype=np.uint8).astype(np.int64) - 97
def table(k):
    idx = sum(a[i:len(a)-k+1+i] * 26**(k-1-i) for i in range(k)); return np.bincount(idx, minlength=26**k).astype(float)
c1, c2, c3, c4 = table(1), table(2), table(3), table(4)
p1 = c1/c1.sum()
p2 = (c2.reshape(26, 26) / np.maximum(c1[:, None], 1))                       # P(b|a)
p3 = (c3.reshape(676, 26) / np.maximum(c2[:, None], 1))                      # P(c|ab)
p4 = (c4.reshape(17576, 26) / np.maximum(c3[:, None], 1))                    # P(d|abc)
I = np.arange(26**4); d = I % 26; abc = I // 26; bc = abc % 676; cc = bc % 26
Q = np.log(0.01/26 + 0.04*p1[d] + 0.15*p2[cc, d] + 0.30*p3[bc, d] + 0.50*p4[abc, d])
def score_arr(p):
    return Q[p[:-3]*17576 + p[1:-2]*676 + p[2:-1]*26 + p[3:]].sum()
def text(p): return ''.join(chr(97+x) for x in p)
def solve(sym, m, restarts=60, steps=8000, fixed=None, rng=random):
    """sym: np array of symbol ids 0..m-1. fixed: {symbol: letter}. returns (best score, plaintext)."""
    fixed = fixed or {}; free = [s for s in range(m) if s not in fixed]; best = (-1e9, None)
    for _ in range(restarts):
        avail = [l for l in range(26) if l not in fixed.values()]; rng.shuffle(avail)
        mp = np.zeros(m, dtype=np.int64)
        for s, l in fixed.items(): mp[s] = l
        for s in free: mp[s] = avail.pop()
        unused = avail; cur = score_arr(mp[sym]); lb = (cur, mp.copy())
        for it in range(steps):
            Tm = 4.0 * (1 - it/steps) + 0.15
            s1 = rng.choice(free)
            if unused and rng.random() < 0.4:
                j = rng.randrange(len(unused)); old = mp[s1]; mp[s1] = unused[j]
                new = score_arr(mp[sym])
                if new >= cur or rng.random() < math.exp((new-cur)/Tm): cur = new; unused[j] = old
                else: mp[s1] = old
            else:
                s2 = rng.choice(free)
                if s1 == s2: continue
                mp[s1], mp[s2] = mp[s2], mp[s1]; new = score_arr(mp[sym])
                if new >= cur or rng.random() < math.exp((new-cur)/Tm): cur = new
                else: mp[s1], mp[s2] = mp[s2], mp[s1]
            if cur > lb[0]: lb = (cur, mp.copy())
        if lb[0] > best[0]: best = (lb[0], text(lb[1][sym]))
    return best
def ids(tokens):
    order = {}; return np.array([order.setdefault(t, len(order)) for t in tokens], dtype=np.int64), len(order)
def parse(r, sel='be'):
    out = []; i = 0
    while i < len(r):
        n = 2 if r[i] in sel else 1; out.append(r[i:i+n]); i += n
    return out
t = open('files/salphaseion-textarea.txt').read().strip(); r1 = t[:91]
SEQS = {'fwd': parse(r1), 'fwd-reversed-order': parse(r1)[::-1], 'rev': parse(r1[::-1]), 'rev-reversed-order': parse(r1[::-1])[::-1]}
CONTROLS = ["thenumberofyellowsquaresisnineandthebluesquaresarefifteenaddtheprimes",
            "sumeachrowofthegridandkeeponlytheprimenumberstomakeyourpasswordfriend",
            "congratulationsyouhavereachedthelastdoortheprivatekeyiswithinyourgrasp",
            "beforeyouchoosethedooraskyourselfwhatthearchitectsaidattheveryendneo",
            "takethelastwordsspokenbeforethechoiceandhashthemtwicetoopenthefinalbox"]
def null_scores(tokens, n, restarts, rng):
    out = []
    for _ in range(n):
        sh = tokens[:]; rng.shuffle(sh); s, m = ids(sh); out.append(solve(s, m, restarts=restarts, rng=rng)[0])
    return sorted(out)
if __name__ == '__main__':
    mode = sys.argv[1]; rng = random.Random(7)
    if mode == 'control':
        for c in CONTROLS:
            c = c[:63]; perm = list(range(26)); rng.shuffle(perm)
            tok = [perm[ord(x)-97] for x in c]; s, m = ids(tok)
            true = score_arr(np.array([ord(x)-97 for x in c])); sc, pt = solve(s, m, rng=rng)
            nl = null_scores(tok, 6, 20, rng)
            print(f'CONTROL distinct {m} true {true:.1f} found {sc:.1f} acc {sum(x==y for x,y in zip(pt,c))/63:.2f} null(shuffled order) {nl[0]:.1f}..{nl[-1]:.1f}\n   {pt}', flush=True)
    elif mode == 'main':
        tok = SEQS[sys.argv[2]]; s, m = ids(tok); sc, pt = solve(s, m, restarts=150, rng=rng)
        nl = null_scores(tok, 20, 20, rng)
        print(f'{sys.argv[2]}: symbols {len(tok)} distinct {m} best {sc:.1f} null(20 shuffles, 20 restarts) {nl[0]:.1f}..{nl[-1]:.1f}\n   {pt}', flush=True)
        sc20 = solve(s, m, restarts=20, rng=rng); print(f'   same-effort (20 restarts) score {sc20[0]:.1f} {sc20[1]}', flush=True)
    elif mode == 'crib':
        tok = SEQS[sys.argv[2]]; s, m = ids(tok); res = []
        for crib in ['yellow', 'blue', 'primes', 'privatekey', 'password', 'yinyang', 'matrix', 'sumlist', 'lastwords', 'architect', 'choice', 'thekey', 'cosmicduality', 'wewont']:
            n = 0
            for p in range(len(s)-len(crib)+1):
                fx = {}; ok = True
                for i, ch in enumerate(crib):
                    l = ord(ch)-97; sy = int(s[p+i])
                    if fx.get(sy, l) != l or (sy not in fx and l in fx.values()): ok = False; break
                    fx[sy] = l
                if not ok: continue
                n += 1; sc, pt = solve(s, m, restarts=6, steps=5000, fixed=fx, rng=rng); res.append((sc, crib, p, pt))
            print(f'{sys.argv[2]} crib {crib}: {n} consistent placements', flush=True)
        res.sort(reverse=True)
        for sc, crib, p, pt in res[:8]: print(f'   {sc:.1f} {crib}@{p} {pt}', flush=True)
