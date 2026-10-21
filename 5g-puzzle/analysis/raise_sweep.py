"""Attack the Phase 3.2 inner blob from its one unconsumed sentence."""
import base64, hashlib, itertools, sys
sys.path.insert(0, '/home/user/5g-puzzle/analysis')
from sweep import try_pw, INNER, SALPH

blobs = {n: base64.b64decode(b + "=" * ((4 - len(b) % 4) % 4))
         for n, b in (("3.2 inner", INNER), ("SalPhaseIon", SALPH))}

# readings of "Raising the stakes without extra chances of winning."
BASE = """
bluff bluffing raise raising reraise allin allinbluff ante uptheante upping
doubleornothing double doubling doublingcube cube backgammon martingale
antemartingale sunkcost sunkcostfallacy potcommitted deadmoney overbet
gamblersfallacy stpetersburg stpetersburgparadox kellycriterion expectedvalue
zerosum negativeexpectation houseedge nogain novalue nochance nowin
raisingthestakes raisethestakes raisingthestakeswithoutextrachancesofwinning
withoutextrachancesofwinning extrachances chancesofwinning
stakes stake thestakes highstakes higherstakes
promotion underpromotion queening stalemate draw perpetualcheck
zugzwang zwischenzug gambit sacrifice pyrrhicvictory
lottery lotteryticket samenumber sameticket buyingmoretickets
inflation halving thehalving diminishingreturns
doublespend nothingatstake nothingtogain
""".split()

# the chain's own established answers, for the concatenation convention
CHAIN = ("causality safenet luna hsm 11110 jacquefresco giveit justonesecond "
         "heisenbergsuncertaintyprinciple thematrixhasyou matrixsumlist enter "
         "thispassword lastwordsbeforearchichoice yinyang theone").split()

def variants(s):
    yield s
    yield s.upper()
    yield s.capitalize()

tried = 0
padded = 0
best = []
seen = set()

def test(label, text):
    global tried, padded
    for form in (hashlib.sha256(text.encode()).hexdigest(),
                 hashlib.sha256(text.encode()).hexdigest().upper(),
                 text):
        if form in seen: continue
        seen.add(form)
        tried += 1
        for name, raw in blobs.items():
            for dg in ("sha256", "md5"):
                r = try_pw(raw, form.encode(), dg)
                if r:
                    padded += 1
                    best.append((r[1], name, label, dg, r[0]))

# 1. each reading alone
for w in BASE:
    for v in variants(w):
        test(f"solo:{w}", v)
# 2. reading appended to / prepended to each chain answer
for w in BASE:
    for c in CHAIN:
        test(f"{c}+{w}", c + w)
        test(f"{w}+{c}", w + c)
# 3. reading combined with the full phase-3.2 password, the puzzle's own precedent
P32 = "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
for w in BASE:
    test(f"p32+{w}", P32 + w)
    test(f"{w}+p32", w + P32)
# 4. pairs of readings
for a, b in itertools.permutations(BASE, 2):
    test(f"{a}+{b}", a + b)

best.sort(key=lambda t: -t[0])
print(f"distinct passphrases: {tried}")
print(f"trials: {tried*len(blobs)*2}")
print(f"passed PKCS#7 padding: {padded}  (chance alone: ~{tried*len(blobs)*2/256:.0f})")
print("\nbest by printable fraction:")
for frac, name, label, dg, body in best[:8]:
    print(f"   {frac:5.2f}  {name:12s} [{dg}]  {label[:40]:40s} {body[:40]!r}")
print(f"\nplaintext-looking (>=95% printable): {sum(1 for b in best if b[0]>=0.95)}")
