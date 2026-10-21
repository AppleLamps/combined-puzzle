"""Solve X and Y by testing the substituted X2SH block as a passphrase."""
import base64, hashlib, sys
sys.path.insert(0, '/home/user/5g-puzzle/analysis')
from sweep import try_pw, INNER, SALPH

blobs = {n: base64.b64decode(b + "=" * ((4 - len(b) % 4) % 4))
         for n, b in (("3.2 inner", INNER), ("SalPhaseIon", SALPH))}

S, Q = 32, 82
def forms(toks):
    """Ways the puzzle has historically written a concatenated answer."""
    plain = ''.join(str(t) for t in toks)
    absol = ''.join(str(abs(t)) for t in toks)
    spaced = ' '.join(str(t) for t in toks)
    return {plain, absol, spaced, plain.replace('-',''),
            '#' + plain + '#', '#' + absol + '#',
            plain[::-1], absol[::-1]}

tried = 0
padded = 0
best = []
seen = set()
for H in (42, -42):
  for B in (-16, 16, 25):
    for X in range(-99, 100):
      for Y in range(-99, 100):
        toks = [X, 2, S, H, 4, Y, 0, Q, B, 15]
        for rev in (False, True):
            for f in forms(toks[::-1] if rev else toks):
                if f in seen: continue
                seen.add(f)
                for pw in (hashlib.sha256(f.encode()).hexdigest(),
                           hashlib.sha256(f.encode()).hexdigest().upper(),
                           f):
                    tried += 1
                    for name, raw in blobs.items():
                        for dg in ("sha256", "md5"):
                            r = try_pw(raw, pw.encode(), dg)
                            if r:
                                padded += 1
                                best.append((r[1], name, f, dg, r[0]))
best.sort(key=lambda t: -t[0])
print(f"distinct passphrases tried: {tried}")
print(f"trials: {tried*len(blobs)*2}")
print(f"passed PKCS#7 padding: {padded}  (chance alone: ~{tried*len(blobs)*2/256:.0f})")
print("\nbest by printable fraction:")
for frac, name, f, dg, body in best[:8]:
    print(f"   {frac:5.2f}  {name:12s} [{dg}]  {f[:44]:44s} {body[:40]!r}")
print(f"\nplaintext-looking (>=95% printable): {sum(1 for b in best if b[0]>=0.95)}")
