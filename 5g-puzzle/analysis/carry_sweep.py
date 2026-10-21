"""The three unconsumed pieces, combined and tested against all three blobs.

  1. X2SH  # X 2 S H 4 Y 0 Q B 15 #   (S=32, H=+/-42, Q=82, B=-16/25; X,Y undefined)
  2. the four surplus cells: spiral 192-195, grid (6,6)(6,7)(7,6)(7,7), bits 0000
  3. the off-colour cell: #fefefe, spiral index 163 (prime), grid (7,4) = 1-indexed (8,5),
     char 20 of the URL, bit 3
"""
import base64, hashlib, itertools, sys
sys.path.insert(0,'/home/user/5g-puzzle/analysis')
from sweep import try_pw, INNER, SALPH
cosmic=open('/tmp/claude-0/-home-user-5g-puzzle/3ce5fd60-660e-5825-8dbb-c2131e61358a/scratchpad/cosmic.txt').read().strip()
blobs={n:base64.b64decode(b+"="*((4-len(b)%4)%4))
       for n,b in (("3.2 inner",INNER),("SalPhaseIon",SALPH),("Cosmic",cosmic))}

# numbers the image actually yields
IMG = [163, 192, 193, 194, 195, 20, 3, 7, 4, 8, 5, 6, 0,
       9, 15, 24, 86, 101, 95, 121, 70]          # incl. yellow/blue counts, ones/zeros, 70x70
S, Q = 32, 82

tried=0; padded=0; best=[]; seen=set()
def test(label, text):
    global tried, padded
    for form in (hashlib.sha256(text.encode()).hexdigest(),
                 hashlib.sha256(text.encode()).hexdigest().upper(), text):
        if form in seen: continue
        seen.add(form); tried+=1
        for name,raw in blobs.items():
            for dg in ("sha256","md5"):
                r=try_pw(raw, form.encode(), dg)
                if r:
                    padded+=1; best.append((r[1],name,label,dg,r[0]))

# A. image numbers alone and in ordered pairs/triples
for n in IMG: test(f"img:{n}", str(n))
for a,b in itertools.permutations(IMG,2): test(f"img:{a},{b}", f"{a}{b}")
for a,b,c in itertools.permutations(IMG[:12],3): test(f"img:{a},{b},{c}", f"{a}{b}{c}")

# B. X2SH with X,Y drawn from the image numbers (this is the "carry" hypothesis)
for H in (42,-42):
  for B in (-16,25):
    for X in IMG:
      for Y in IMG:
        toks=[X,2,S,H,4,Y,0,Q,B,15]
        for rev in (False,True):
            t=toks[::-1] if rev else toks
            test(f"x2sh X={X} Y={Y} H={H} B={B}{' rev' if rev else ''}",
                 ''.join(str(v) for v in t))
            test(f"x2sh|abs X={X} Y={Y} H={H} B={B}{' rev' if rev else ''}",
                 ''.join(str(abs(v)) for v in t))

# C. the three pieces concatenated with the chain's own answers
CHAIN="matrixsumlist enter thispassword lastwordsbeforearchichoice thematrixhasyou theone yinyang".split()
for n in IMG:
    for c in CHAIN:
        test(f"{c}+{n}", c+str(n)); test(f"{n}+{c}", str(n)+c)

best.sort(key=lambda t:-t[0])
print(f"distinct passphrases: {tried}")
print(f"trials: {tried*len(blobs)*2}")
print(f"passed PKCS#7 padding: {padded}  (chance ~{tried*len(blobs)*2/256:.0f})")
print("\nbest by printable fraction:")
for frac,name,label,dg,body in best[:8]:
    print(f"   {frac:5.2f}  {name:11s} [{dg}] {label[:44]:44s} {body[:36]!r}")
print(f"\nplaintext-looking (>=95%): {sum(1 for b in best if b[0]>=0.95)}")
