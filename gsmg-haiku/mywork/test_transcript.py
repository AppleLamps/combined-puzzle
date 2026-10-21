import sys, re, hashlib, itertools
from lib import *

# Load transcript
raw_transcript = open(r'c:\gsmg-puzzle-clean\matrix-reloaded.txt', encoding='utf-8').read()
lines = [l.strip() for l in raw_transcript.split('\n') if l.strip()]

# Load containers
conts = {
    'terminal': load('terminal.b64'),
    'salphaseion-short': load('salphaseion-short.b64'),
    'cosmic-duality': load('cosmic-duality.b64'),
    'phase3.2': load('phase3.2.b64') # control
}

candidates = set()

# Add lines
for l in lines:
    candidates.add(l)
    # remove speaker prefix like "Architect: " or "Neo: "
    if ':' in l:
        candidates.add(l.split(':', 1)[1].strip())

# Split into sentences
sentences = re.split(r'[.!?]+', raw_transcript)
for s in sentences:
    s = s.strip()
    if s:
        candidates.add(s)
        if ':' in s:
            candidates.add(s.split(':', 1)[1].strip())

# Clauses (split by comma, semicolon, colon, dash)
clauses = re.split(r'[,;:—–\-]+', raw_transcript)
for c in clauses:
    c = c.strip()
    if c:
        candidates.add(c)

# Especially lines 21 to 53 (the second half of the dialogue)
target_section = ""
capture = False
for l in lines:
    if "Choice. The problem is choice" in l:
        capture = True
    if capture:
        target_section += " " + l

target_words = re.findall(r"[A-Za-z0-9']+", target_section)
print(f"Target section word count: {len(target_words)}")

# Generate all n-grams from target_words (n from 1 to 30)
for n in range(1, 35):
    for i in range(len(target_words) - n + 1):
        chunk = target_words[i:i+n]
        candidates.add(" ".join(chunk))
        candidates.add("".join(chunk))

# Also n-grams from the entire transcript up to 10 words
all_words = re.findall(r"[A-Za-z0-9']+", raw_transcript)
for n in range(1, 12):
    for i in range(len(all_words) - n + 1):
        chunk = all_words[i:i+n]
        candidates.add(" ".join(chunk))
        candidates.add("".join(chunk))

print(f"Total base candidates: {len(candidates)}")

# Function to test a candidate string
def test_string(s, cname, raw):
    for cand in [s, s.lower(), s.upper(), s.strip(" '\".,;:!?"), s.lower().strip(" '\".,;:!?")]:
        for pw_mode in ['sha_hex', 'raw', 'sha_upper']:
            if pw_mode == 'sha_hex':
                pw = hashlib.sha256(cand.encode('utf-8')).hexdigest()
            elif pw_mode == 'sha_upper':
                pw = hashlib.sha256(cand.encode('utf-8')).hexdigest().upper()
            else:
                pw = cand
            
            # decrypt
            p = dec(raw, pw, hashed=False) # dec with exact pw
            if p is not None:
                pr = printable(p)
                if pr > 0.4:
                    print(f"\n*** HIT! *** Container: {cname}, Cand: {cand!r}, Mode: {pw_mode}, Printable: {pr:.2f}")
                    print(f"Decrypted: {p[:120]!r}\n")
                    return True
    return False

# Plant control:
control_ans = "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
candidates.add(control_ans)

found_control = False
hits = []

for cname, raw in conts.items():
    print(f"Testing container: {cname}...")
    for cand in candidates:
        if test_string(cand, cname, raw):
            hits.append((cname, cand))

print(f"Finished. Hits: {hits}")
