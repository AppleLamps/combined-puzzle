import sys, re, hashlib
from lib import *

txt = open(r'c:\gsmg-puzzle-clean\matrix-reloaded.txt', encoding='utf-8').read()
lines = [l.strip() for l in txt.split('\n') if l.strip()]

# Load containers
conts = {
    'terminal': load('terminal.b64'),
    'salphaseion-short': load('salphaseion-short.b64'),
    'cosmic-duality': load('cosmic-duality.b64')
}

# Collect specific sentences, phrases, clauses around "choice" and the end
targets = []

# Line 24 pure dialogue
l24 = lines[24].split(":", 1)[1].strip()
# Line 26 pure dialogue
l26 = lines[26].split(":", 1)[1].strip() # "We won't."

# Sentences of line 24
sentences = [
    "Which brings us at last to the moment of truth, wherein the fundamental flaw is ultimately expressed and the anomaly revealed as both beginning and end.",
    "There are two doors, the door to your right leads to the source and the salvation of Zion, the door to your left leads back to the matrix, to her, and to the end of your species.",
    "As you adequately put, the problem is choice.",
    "But we already know what you are going to do, don't we?",
    "Already I can see the chain reaction, the chemical precursors that signal the onset of an emotion designed specifically to overwhelm logic and reason, an emotion that is already blinding you from the simple and obvious truth: she is going to die and there is nothing you can do to stop it.",
    "Hope: it is the quintessential human delusion, simultaneously the source of your greatest strength and your greatest weakness.",
    "Hope, it is the quintessential human delusion, simultaneously the source of your greatest strength and your greatest weakness."
]

# Phrases before the word "choice" in Line 24:
# 1. Everything up to "choice":
idx_choice = l24.find("choice")
targets.append(l24[:idx_choice].strip())
targets.append(l24[:idx_choice + len("choice")].strip())

# 2. Sentence 3 up to "choice":
targets.append("As you adequately put, the problem is")
targets.append("the problem is")
targets.append("problem is")

# 3. Sentence 2 (the doors choice description):
targets.append(sentences[1])
# subclauses of Sentence 2:
targets.append("the door to your left leads back to the matrix, to her, and to the end of your species.")
targets.append("to her, and to the end of your species.")
targets.append("and to the end of your species.")
targets.append("to the end of your species.")
targets.append("the end of your species.")
targets.append("the end of your species")

# 4. Sentence 1 + Sentence 2:
targets.append(sentences[0] + " " + sentences[1])

# 5. Sentence 6 (last sentence of Line 24):
targets.append(sentences[5])
targets.append(sentences[6])
targets.append("Hope: it is the quintessential human delusion, simultaneously the source of your greatest strength and your greatest weakness")
targets.append("it is the quintessential human delusion, simultaneously the source of your greatest strength and your greatest weakness.")
targets.append("it is the quintessential human delusion, simultaneously the source of your greatest strength and your greatest weakness")
targets.append("the quintessential human delusion, simultaneously the source of your greatest strength and your greatest weakness")
targets.append("the quintessential human delusion")
targets.append("Hope: it is the quintessential human delusion")
targets.append("Hope, it is the quintessential human delusion")
targets.append("Hope")

# 6. Line 26 ("We won't."):
targets.append("We won't.")
targets.append("We won't")
targets.append("wewon't")
targets.append("wewont")

# 7. Line 10 (Architect words before Neo says "Choice. The problem is choice."):
l10 = lines[10].split(":", 1)[1].strip()
targets.append(l10)
targets.append("Creating fluctuations in even the most simplistic equations.")
targets.append("Creating fluctuations in even the most simplistic equations")

# 8. All combinations with formatting variations:
# For each target:
# - raw
# - lowercase
# - lowercase, no punctuation, no spaces
# - lowercase, keep spaces, remove punctuation
# - as-is without final period

print(f"Generated {len(targets)} base targets.")

def get_variants(s):
    v = set()
    s_clean = s.strip()
    v.add(s_clean)
    v.add(s_clean.rstrip('.'))
    v.add(s_clean.lower())
    v.add(s_clean.lower().rstrip('.'))
    
    # remove punctuation
    no_punct = re.sub(r"[^\w\s]", "", s_clean)
    v.add(no_punct)
    v.add(no_punct.lower())
    
    # remove all spaces and punctuation
    alpha_num = re.sub(r"[^A-Za-z0-9]", "", s_clean).lower()
    v.add(alpha_num)
    
    return v

all_cands = set()
for t in targets:
    all_cands.update(get_variants(t))

print(f"Total candidate variants: {len(all_cands)}")

hits = []
for cname, raw in conts.items():
    for cand in all_cands:
        # standard GSMG convention: password is sha256(cand).hexdigest()
        pw_hex = hashlib.sha256(cand.encode('utf-8')).hexdigest()
        p = dec(raw, pw_hex, hashed=False)
        if p is not None:
            pr = printable(p)
            hits.append((cname, cand, pr, p))
            print(f"Padding MATCH! [{cname}] cand={cand[:50]!r} printable={pr:.2f}")
            if pr > 0.5:
                print(f"*** SIGNIFICANT HIT! ***\nPlaintext: {p}\n")

print(f"\nDone testing. Total padding matches: {len(hits)}")
