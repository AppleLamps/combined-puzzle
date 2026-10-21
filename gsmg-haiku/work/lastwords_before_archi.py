#!/usr/bin/env python3
"""
GSMG Puzzle - Decode Phase 3.2 properly using STEPS.md

Key insight from STEPS.md:
- bytes 0-446: ASCII text (already readable)
- bytes 447-1985: cp273 + Beaufort "THEMATRIXHASYOU" → architect text
- bytes 1990-2138: 149 digits → straddling checkerboard
- bytes 2143-2291: ASCII text

The decoded word "lastwordsbeforearchichoice" from SalPhaseIon:
- "archi" = architect text (starts at byte 447)
- "last words before archi" = bytes 0-446 text!

Similarly: "thispassword" might point to something specific,
and "matrixsumlist" might be an operation to perform.

Let me extract bytes 0-446 and 2143-2291 completely.
"""

import os
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read phase 3.2 binary
with open(os.path.join(BASE_DIR, 'derived', 'phase3.2-plaintext.bin'), 'rb') as f:
    phase32_bin = f.read()

print("="*70)
print("Phase 3.2 Layout from STEPS.md")
print("="*70)
print(f"Total: {len(phase32_bin)} bytes")
print("""
  bytes 0-446:    ASCII text (Morpheus + strategic position)
  bytes 447-1985:  non-ASCII → cp273 + Beaufort(THEMATRIXHASYOU) → architect
  bytes 1986-1989: CRLF CRLF
  bytes 1990-2138: 149 digits (step 4b, checkerboard)
  bytes 2139-2142: CRLF CRLF
  bytes 2143-2291: ASCII text ("Raising the stakes...")
  bytes 2292-2421: Terminal container (base64)
""")

print("="*70)
print("Bytes 0-446: 'Last words before archi choice'")
print("="*70)
section_before_archi = phase32_bin[0:447]
print("\nFull text:")
print("-"*70)
print(section_before_archi.decode('latin-1'))
print("-"*70)

print("\n" + "="*70)
print("Bytes 2143-2291: Text after checkerboard digits")
print("="*70)
section_after_checkerboard = phase32_bin[2143:2292]
print("\nFull text:")
print("-"*70)
print(section_after_checkerboard.decode('latin-1'))
print("-"*70)

# Now let's think about the clues:
# 
# From SalPhaseIon we decoded:
#   - matrixsumlist       (instruction)
#   - lastwordsbeforearchichoice (points to bytes 0-446)
#   - thispassword         (maybe "this [following text] is password")
#   - enter                (instruction)
#
# From shabefourfirsthintisyourlastcommand:
#   - "four first hint" = the four hints, take the first one? or first chars?
#   - "your last command" = last solved answer (phase3.2 answer) or last instruction ("enter")

print("\n" + "="*70)
print("Analyzing 'lastwordsbeforearchichoice'")
print("="*70)
# This explicitly decoded word tells us to use bytes 0-446.
# But how? Maybe:
#   1. The whole text is the answer?
#   2. Specific line?
#   3. First letters of each line/sentence?
#   4. Certain words extracted?

text_before_archi = section_before_archi.decode('latin-1')
print(f"\nLength: {len(text_before_archi)} chars")

# Try the first letters
lines = text_before_archi.strip().split('\n')
first_chars = ''.join(line[0] for line in lines if line.strip())
print(f"\nFirst char of each line: '{first_chars}'")

# Try words that might be important
words_to_try = [
    "Morpheus", "Neo", "Matrix", "strategic", "position", 
    "Oneforone", "fourforone", "Onetoone", "fourtoone",
    "I'vebeenwaitingforyou",
    "Oneforonefourforone",
]

# Also look at the very LAST part: "... am I here? Wake up, you... I've designed you a beautiful strategic position. One for one, four for one."
# It ends with: "One for one, four for one."

# What about extracting all UPPERCASE letters? (though there are none besides "I")

# What if we take the last words/sentence?
last_sentence = text_before_archi.split('.')[-2].strip() if '.' in text_before_archi else ''
print(f"\nLast sentence (before final period): {repr(last_sentence)}")

# Actually, let me read the "before archi" text very carefully:
# It ends with:
#   "... am I here? Wake up, you... I've designed you a beautiful strategic position. One for one, four for one."
#
# "One for one, four for one" - this is a key!
# This is the straddling checkerboard encoding:
#   Row 0 (F,U,B,C,D,O,R,A): 1 digit each → "one for one" (one digit gives one char)
#   Row 1 (p1-p9,L,E,T,H,I,N,G,K,Y): "1" prefix + digit → "one for one" as well? wait no...
#   Actually: prefix "1" + 1 digit = 2 digits for one char
#   prefix "4" + 1 digit = 2 digits for one char
#
# So: "One for one, four for one"
#   - Row ONE: one (prefix) for one (char) 
#   - Row FOUR: one (prefix) for one (char)

print("\n" + "="*70)
print("The AFTER checkerboard text (bytes 2143-2291)")
print("="*70)
# "Raising the stakes without extra chances of winning. A fubcd-king & oracle-queen, thingky mvps, on a sad board but as wide as the first one seen."

after_text = section_after_checkerboard.decode('latin-1')
print(f"\nLet's decode the coded names:")
print("  fubcd-king  -> checkerboard encoded")
print("  oracle-queen -> checkerboard encoded")
print("  thingky mvps -> checkerboard encoded")

# Let me verify using the straddling checkerboard:
# Row 0 (single digit): 0=F, 2=U, 3=B, 5=C, 6=D, 7=O, 8=R, 9=A
# Row 1 (prefix '1'): 0=., 1=L, 2=E, 3=T, 4=H, 5=I, 6=N, 7=G, 8=K, 9=Y
# Row 4 (prefix '4'): 0=M, 1=V, 2=P, 3=S, 4=/, 5=J, 6=Q, 7=Z, 8=X, 9=W

# fubcd = F, U, B, C, D all from row 0 (single digits)
# king = K,I,N,G from row 1 (needs prefix 1)
# oracle = O,R,A,C,L,E from row 0 and row 1
# queen = Q,U,E,E,N from row 4 (Q=46), row 0 (U=2), row 1 (E=12, N=16)

# So the coded text "fubcd" and "oracle" etc are just spelling out the
# row 0 letters directly. The clue is using checkerboard letters.

# But let me think about "matrixsumlist" - it sounds like an operation.
# Matrix could mean:
# - The Matrix (movie theme)
# - A mathematical matrix (maybe the chess board positions?)
# - The 149 digits arranged in some matrix?

# "sum list" could mean:
# - Sum the digits? sum the 149 digits?
# - Sum a list of something?

# Let me also think about "enter" - maybe it means:
# - Press Enter (add CRLF or \n at end?)
# - Enter as in "enter the key"

print("\n" + "="*70)
print("Generating candidates from our understanding")
print("="*70)

# ============== DECRYPTION FUNCTION ==============
def derive_key_and_iv(password: str, salt: bytes) -> tuple[bytes, bytes]:
    password_bytes = password.encode('utf-8')
    D_i = b''
    result = b''
    while len(result) < 48:
        md = hashlib.sha256()
        md.update(D_i + password_bytes + salt)
        D_i = md.digest()
        result += D_i
    return result[:32], result[32:48]

def try_decrypt(data: bytes, password: str):
    if not data.startswith(b'Salted__'):
        return False, None, 0.0
    salt = data[8:16]
    ciphertext = data[16:]
    try:
        key, iv = derive_key_and_iv(password, salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        total = len(plaintext)
        if total == 0:
            printable_ratio = 1.0
        else:
            printable = sum(1 for b in plaintext if 32 <= b < 127 or b in (9, 10, 13))
            printable_ratio = printable / total
        return True, plaintext, printable_ratio
    except:
        return False, None, 0.0

def try_answer(answer_text: str, label: str, containers):
    password = hashlib.sha256(answer_text.encode()).hexdigest().lower()
    successes = []
    for name, data in containers:
        success, decrypted, printable = try_decrypt(data, password)
        if success:
            successes.append((name, decrypted, printable, answer_text, password))
            print(f"\n{'='*70}")
            print(f"SUCCESS! {label} on {name}")
            print(f"{'='*70}")
            print(f"Answer: {repr(answer_text[:200])}")
            print(f"Printable: {printable:.1%}, Len: {len(decrypted)} bytes")
            print(f"First 100: {repr(decrypted[:100])}")
            try:
                print(f"As text: {decrypted[:300].decode('latin-1')}")
            except:
                pass
    return successes

# Load containers
def load_container(name):
    with open(os.path.join(BASE_DIR, 'files', name), 'r') as f:
        return name.replace('.b64', ''), base64.b64decode(''.join(f.read().split()))

containers = [
    load_container('terminal.b64'),
    load_container('salphaseion-short.b64'),
    load_container('cosmic-duality.b64'),
]

all_successes = []

# CANDIDATE 1: Use the whole "before archi" text
# But it's 447 chars. That's a long answer. But let's try it.
candidates = [
    ("before_archi_full", text_before_archi),
    ("before_archi_nocr", text_before_archi.replace('\r', '')),
    ("before_archi_nolf", text_before_archi.replace('\n', '')),
]

# CANDIDATE 2: Use specific phrases from before_archi
# "I've been waiting for you"
# "you remain irrevocably human"
# "One for one, four for one"
phrases = [
    "I've been waiting for you",
    "One for one, four for one",
    "Oneforonefourforone",
    "strategic position",
    "irrevocably human",
    "Wake up",
]
for p in phrases:
    candidates.append((f"phrase_{p[:30].replace(' ', '_')}", p))
    candidates.append((f"phrase_upper_{p[:30].replace(' ', '_')}", p.upper()))

# CANDIDATE 3: "lastwordsbeforearchichoice" - maybe it means take the LAST WORDS
# (last sentence) before "archi"
# Last sentence: "One for one, four for one"
candidates.append(("last_sentence_raw", last_sentence))

# CANDIDATE 4: Use the after_checkerboard text phrases
# "fubcd-king & oracle-queen"
# "thingky mvps"
# "Raising the stakes"
after_phrases = [
    "fubcd", "oracle", "thingky", "mvps",
    "fubcd-king", "oracle-queen", "thingky mvps",
    "fubcdking", "oraclequeen", "thingkymvps",
    "fubcdkingoraclequeen",
    "Raising the stakes",
]
for p in after_phrases:
    candidates.append((f"after_{p[:25].replace(' ','_')}", p))

# CANDIDATE 5: The four decoded words, but using them as INSTRUCTIONS
# lastwordsbeforearchichoice = use bytes 0-446
# What if "thispassword" means "the text AFTER this [decoded word] is the password"?
# 
# In SalPhaseIon order:
#   1. matrixsumlist
#   2. lastwordsbeforearchichoice
#   3. thispassword
#   4. enter
#
# "thispassword" comes at position 830-858, after "lastwordsbeforearchichoice",
# and after the "shabe" hint. What FOLLOWS "thispassword" decoding position?
# - the shabe hint was at 860-894
# - SalPhaseIon short container at 895-958
# - enter at 959-998
# - Cosmic Duality at 999-1062
#
# Hmm, "thispassword" followed by a container?

# Actually let me also think about: what if "lastwordsbeforearchichoice" means
# we need to look at the LAST WORDS of the "archi choice" - the architect text?
# Architect ends with: "CIAOBELLAO"

with open(os.path.join(BASE_DIR, 'derived', 'architect-text.txt'), 'r') as f:
    arch_text = f.read().strip()

# Last few words: "...REALLYHOPEYOURETHEONECIAOBELLAO"
candidates.append(("architect_lastword", "CIAOBELLAO"))
candidates.append(("architect_lastword_lower", "ciaobellao"))
candidates.append(("architect_goodluck", "GOODLUCK"))

# CANDIDATE 6: 149 digits sum
with open(os.path.join(BASE_DIR, 'derived', 'checkerboard-digits.txt'), 'r') as f:
    cb_digits = f.read().strip()

sum_149 = sum(int(d) for d in cb_digits)
print(f"\nSum of 149 checkerboard digits: {sum_149}")
candidates.append(("checkerboard_digit_sum", str(sum_149)))

# Try sums of various things
print(f"\nTrying {len(candidates)} candidates...")

for label, ans in candidates:
    if len(ans) < 60:
        print(f"  Trying: {label} = {repr(ans)}")
    else:
        print(f"  Trying: {label} (len={len(ans)})")
    results = try_answer(ans, label, containers)
    all_successes.extend(results)

print("\n" + "="*70)
if all_successes:
    print(f"TOTAL SUCCESSES: {len(all_successes)}")
else:
    print("No successes with these candidates.")
print("="*70)
