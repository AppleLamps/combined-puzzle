#!/usr/bin/env python3
"""Doc 116 sweep: every string in the Telegram export against the win test and the
three locks, with seeded planted controls (doc 115 harness).

Families:
  scalars   every 64-hex string and every WIF posted in chat, as a raw private key
  tokens    every whitespace token, original case and lowercase, punctuation-stripped
  ngrams    every 2-, 3- and 4-gram inside a message, spaced and joined, both cases
  lines     every line and every whole message, original and lowercase
  keyish    every 32+ hex, base64-ish (24+) and URL token, as password text

    python3 sweep.py [family ...]      # default: all
Writes flags to sweep-<family>.flags next to this file.
"""
import hashlib, os, re, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '115'))
import harness as H, prun
from controls import planted_container, planted_target
from tg import load, text

B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58dec(s):
    n = 0
    for ch in s: n = n * 58 + B58.index(ch)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')

def wif_to_priv(w):
    try:
        raw = b58dec(w)
    except ValueError:
        return None
    body, chk = raw[:-4], raw[-4:]
    if hashlib.sha256(hashlib.sha256(body).digest()).digest()[:4] != chk: return None
    if body[0] != 0x80: return None
    return body[1:33]

def texts():
    b = load()
    return [text(m) for m in b.values() if m['type'] == 'message' and text(m)]

def uniq(items):
    seen = set(); out = []
    for lab, c in items:
        if c and c not in seen and len(c) <= 4096:
            seen.add(c); out.append((lab, c))
    return out

def fam_scalars(T):
    hexes = set(); wifs = set()
    for t in T:
        hexes.update(re.findall(r'\b[0-9a-fA-F]{64}\b', t))
        wifs.update(re.findall(r'\b[5KL][1-9A-HJ-NP-Za-km-z]{50,51}\b', t))
    sc = [(f'hex64|{h}', bytes.fromhex(h)) for h in hexes]
    for w in wifs:
        p = wif_to_priv(w)
        if p: sc.append((f'wif|{w}', p))
    return sc, len(hexes), len(wifs)

STRIP = re.compile(r'^[\W_]+|[\W_]+$')
def fam_tokens(T):
    out = []
    for t in T:
        for tok in t.split():
            for v in (tok, tok.lower(), STRIP.sub('', tok), STRIP.sub('', tok).lower()):
                out.append(('tok', v.encode()))
    return uniq(out)

def fam_ngrams(T, ns=(2, 3, 4)):
    out = []
    for t in T:
        toks = [STRIP.sub('', x) for x in t.split()]
        toks = [x for x in toks if x]
        for n in ns:
            for i in range(len(toks) - n + 1):
                g = toks[i:i + n]
                for v in (' '.join(g), ''.join(g), ' '.join(g).lower(), ''.join(g).lower()):
                    out.append((f'{n}g', v.encode()))
    return uniq(out)

def fam_lines(T):
    out = []
    for t in T:
        for v in (t, t.strip(), t.lower(), t.strip().lower()):
            out.append(('msg', v.encode()))
        for l in t.split('\n'):
            l = l.strip()
            if l:
                out.append(('line', l.encode())); out.append(('line', l.lower().encode()))
    return uniq(out)

def fam_keyish(T):
    out = []
    for t in T:
        for x in re.findall(r'\b[0-9a-fA-F]{32,}\b', t): out.append(('hex', x.encode())); out.append(('hex', x.lower().encode()))
        for x in re.findall(r'[A-Za-z0-9+/]{24,}={0,2}', t): out.append(('b64', x.encode()))
        for x in re.findall(r'https?://\S+', t): out.append(('url', x.encode()))
        for x in re.findall(r'\b[13][1-9A-HJ-NP-Za-km-z]{25,34}\b', t): out.append(('addr', x.encode()))
    return uniq(out)

FAMS = {'tokens': fam_tokens, 'ngrams': fam_ngrams, 'lines': fam_lines, 'keyish': fam_keyish}

def run_family(name, items, seed):
    ctl_pw = items[len(items) // 3][1]; ctl_key = items[2 * len(items) // 3][1]
    extra_c = {'CONTROL': planted_container(ctl_pw, seed=seed)}
    extra_t = {planted_target(hashlib.sha256(ctl_key).digest())}
    H.TARGETS.update(extra_t)
    C, D, V, F = prun.run(items, procs=int(os.environ.get("SWEEP_PROCS", os.cpu_count())), chunk=int(os.environ.get("SWEEP_CHUNK", 2000)), tag=name,
                          extra_containers=extra_c, extra_targets=extra_t)
    fired_c = sum(f[0] == 'CONTROL' and f[6] == ctl_pw for f in F)
    fired_k = sum(f[0] == 'WIN' and f[2] == ctl_key for f in F)
    print(f'[{name}] container control fired {fired_c}x, key control fired {fired_k}x', flush=True)
    real = [f for f in F if not (f[0] == 'CONTROL' or (f[0] == 'WIN' and f[2] == ctl_key))]
    with open(os.path.join(HERE, f'sweep-{name}.flags'), 'w') as fh:
        fh.write(f'# {name}: candidates {C} decrypts {D} valid {V} expected {D/256:.0f}; controls {fired_c}/{fired_k}\n')
        for f in real: fh.write(repr(f) + '\n')
    for f in real: print('FLAG', repr(f)[:300], flush=True)
    return C, D, V, len(real)

def main(argv):
    fams = argv or ['scalars'] + list(FAMS)
    T = texts()
    print(f'{len(T)} message texts', flush=True)
    if 'scalars' in fams:
        sc, nh, nw = fam_scalars(T)
        ctl = hashlib.sha256(b'doc116 scalar control').digest()
        H.TARGETS.add(planted_target(ctl))
        hits = [lab for lab, p in sc + [('CONTROL', ctl)] if H.key_hits(p)]
        print(f'[scalars] {nh} hex64, {nw} WIF ({len(sc)} scalars); hits {hits} (control {"FIRED" if "CONTROL" in hits else "MISSED"})', flush=True)
        H.TARGETS.discard(planted_target(ctl))
    for i, name in enumerate(f for f in fams if f in FAMS):
        t0 = time.time(); items = FAMS[name](T)
        print(f'[{name}] {len(items)} candidates built in {time.time()-t0:.0f}s', flush=True)
        run_family(name, items, seed=116 + i)

if __name__ == '__main__':
    main(sys.argv[1:])
