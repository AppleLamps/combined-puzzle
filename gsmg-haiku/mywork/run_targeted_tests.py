import sys, re, hashlib, itertools
from lib import *

# Load transcript
txt = open(r'c:\gsmg-puzzle-clean\matrix-reloaded.txt', encoding='utf-8').read()
lines = [l.strip() for l in txt.split('\n') if l.strip()]

# Load containers
conts = {
    'terminal': load('terminal.b64'),
    'salphaseion-short': load('salphaseion-short.b64'),
    'cosmic-duality': load('cosmic-duality.b64')
}

# Let's extract dialogues
dialogues = []
for l in lines:
    speaker, text = l.split(":", 1)
    dialogues.append((speaker.strip(), text.strip()))

# Candidates
cands = set()

# 1. Phrases from Line 24 (the choice speech)
l24_text = dialogues[24][1]
# All sentences in Line 24
for s in re.split(r'(?<=[.!?])\s+', l24_text):
    cands.add(s.strip())
    cands.add(s.strip().rstrip('.'))

# Sub-clauses of Line 24
clauses = [
    "Which brings us at last to the moment of truth",
    "wherein the fundamental flaw is ultimately expressed",
    "and the anomaly revealed as both beginning and end",
    "There are two doors",
    "the door to your right leads to the source and the salvation of Zion",
    "the door to your left leads back to the matrix, to her, and to the end of your species",
    "to her, and to the end of your species",
    "and to the end of your species",
    "to the end of your species",
    "the end of your species",
    "As you adequately put, the problem is choice",
    "As you adequately put, the problem is",
    "the problem is choice",
    "the problem is",
    "problem is",
    "Hope: it is the quintessential human delusion",
    "Hope, it is the quintessential human delusion",
    "it is the quintessential human delusion, simultaneously the source of your greatest strength and your greatest weakness",
    "Hope: it is the quintessential human delusion, simultaneously the source of your greatest strength and your greatest weakness",
    "Hope, it is the quintessential human delusion, simultaneously the source of your greatest strength and your greatest weakness",
    "the quintessential human delusion, simultaneously the source of your greatest strength and your greatest weakness",
    "simultaneously the source of your greatest strength and your greatest weakness",
    "the source of your greatest strength and your greatest weakness",
]
for c in clauses:
    cands.add(c)
    cands.add(c.rstrip('.'))

# 2. Line 26:
cands.add("We won't.")
cands.add("We won't")
cands.add("Wewon't")
cands.add("Wewont")

# 3. Line 10 (before Neo's line "Choice. The problem is choice"):
l10_text = dialogues[10][1]
cands.add(l10_text)
cands.add("Creating fluctuations in even the most simplistic equations.")
cands.add("Creating fluctuations in even the most simplistic equations")

# 4. Combinations with 'matrixsumlist':
# "first hint is your last command" -> matrixsumlist appended?
extra_cands = set()
for c in list(cands):
    # try c + matrixsumlist
    extra_cands.add(c + "matrixsumlist")
    extra_cands.add(c + " " + "matrixsumlist")
    # try lowercase no spaces
    c_clean = re.sub(r'[^a-zA-Z0-9]', '', c).lower()
    extra_cands.add(c_clean)
    extra_cands.add(c_clean + "matrixsumlist")
    extra_cands.add("matrixsumlist" + c_clean)

cands.update(extra_cands)

print(f"Total candidates to test: {len(cands)}")

hits = []
for cand in cands:
    # Try different password derivations:
    # 1. sha256(cand).hexdigest() (standard GSMG)
    # 2. raw cand
    # 3. sha256(sha256(cand))
    for mode, pw in [
        ('sha_hex', hashlib.sha256(cand.encode('utf-8')).hexdigest()),
        ('raw', cand),
    ]:
        for cname, raw in conts.items():
            p = dec(raw, pw, hashed=False)
            if p is not None:
                pr = printable(p)
                hits.append((cname, cand, mode, pr, p))
                print(f"MATCH: [{cname}] mode={mode} pr={pr:.2f} cand={cand[:50]!r}")
                if pr > 0.5:
                    print(f"*** SIGNIFICANT DECRYPT! ***: {p[:120]}\n")

print(f"\nDone. Total matches: {len(hits)}")
