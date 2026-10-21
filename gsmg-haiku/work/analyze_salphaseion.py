#!/usr/bin/env python3
"""
GSMG Puzzle - Reproduce SalPhaseIon decoding methods
Then try derived candidates
"""

import hashlib
import base64
import sys
sys.path.insert(0, r'c:\gsmg-puzzle-clean\work')
from openssl_decrypt import decrypt_openssl_aes256cbc as openssl_aes_decrypt


def ab_binary_to_text(chars: str) -> str:
    """a=0, b=1, 8 bits per ASCII character"""
    # Remove any non a/b chars (shouldn't be any)
    bits = []
    for c in chars:
        if c == 'a':
            bits.append('0')
        elif c == 'b':
            bits.append('1')
    
    # Pad to multiple of 8
    while len(bits) % 8 != 0:
        bits.insert(0, '0')  # Or append? Need to check original method
    
    bits_str = ''.join(bits)
    result = []
    for i in range(0, len(bits_str), 8):
        byte = bits_str[i:i+8]
        if len(byte) == 8:
            result.append(chr(int(byte, 2)))
    
    return ''.join(result)


def aio_digits_to_text(chars: str) -> str:
    """a-i=1-9, o=0 -> decimal -> hex -> ASCII"""
    digits = []
    for c in chars:
        if c == 'o':
            digits.append('0')
        elif 'a' <= c <= 'i':
            digits.append(str(ord(c) - ord('a') + 1))
    
    dec_str = ''.join(digits)
    try:
        val = int(dec_str)
        hex_str = format(val, 'x')
        # Make even length
        if len(hex_str) % 2 != 0:
            hex_str = '0' + hex_str
        return bytes.fromhex(hex_str).decode('latin-1')
    except:
        return f"<decode error: {dec_str[:30]}...>"


# Read the SalPhaseIon first textarea
with open(r'c:\gsmg-puzzle-clean\files\salphaseion-textarea.txt', 'r') as f:
    content = f.read().strip()

print("="*70)
print("SalPhaseIon first textarea (1075 chars)")
print("="*70)

# Let's manually check the runs according to STEPS.md
# Runs:
# 0-90    = 91 chars, a-i  → UNUSED
# 91-194  = 104 chars, a,b → matrixsumlist
# 195-764 = 570 chars, a-i → UNUSED
# 765     = 1 char, z → separator
# 766-828 = 63 chars, a-i,o → lastwordsbeforearchichoice
# 829     = 1 char, z → separator  
# 830-858 = 29 chars, a-i,o → thispassword
# 859     = 1 char, z → separator
# 860-894 = 35 chars, text → shabefourfirsthintisyourlastcommand
# 895-958 = 64 chars, base64 → part of container
# 959-998 = 40 chars, a,b → enter
# 999-1062 = 64 chars, base64 → part of container
# 1063-1074 = 12 chars, text → shabefanstoo

# Let's verify each decoded run
runs = [
    (91, 104+1, "a,b", "matrixsumlist"),
    (766, 828+1, "a-i,o", "lastwordsbeforearchichoice"),
    (830, 858+1, "a-i,o", "thispassword"),
    (959, 998+1, "a,b", "enter"),
]

for start, end, runtype, expected in runs:
    chars = content[start:end]
    if runtype == "a,b":
        decoded = ab_binary_to_text(chars)
    else:
        decoded = aio_digits_to_text(chars)
    print(f"\n[{start}:{end}] len={len(chars)} ({runtype}):")
    print(f"  Input sample: {chars[:40]}...")
    print(f"  Decoded: {decoded}")
    print(f"  Expected: {expected}")
    print(f"  Match: {decoded == expected}")

# Also check the direct text portions
print("\n" + "="*70)
print("Direct text portions (not encoded)")
print("="*70)
p1 = content[860:895]  # shabefourfirsthintisyourlastcommand
p2 = content[1063:1075] # shabefanstoo
print(f"[860:895]: {p1}")
print(f"[1063:1075]: {p2}")

# What does "shabe" mean? Could be a shift cipher
# Let's check if it's Caesar shifted
print("\n" + "="*70)
print("'shabe' Caesar shift analysis")
print("="*70)
for shift in range(26):
    shifted = ''.join(chr((ord(c) - ord('a') + shift) % 26 + ord('a')) for c in 'shabe')
    print(f"  +{shift:2}: {shifted}")

print("\n" + "="*70)
print("Now testing actual password candidates")
print("="*70)

# Load containers
def load_b64_container(path):
    with open(path, 'r') as f:
        return base64.b64decode(f.read())

terminal = load_b64_container(r'c:\gsmg-puzzle-clean\files\terminal.b64')
salphaseion_short = load_b64_container(r'c:\gsmg-puzzle-clean\files\salphaseion-short.b64')
cosmic_duality = load_b64_container(r'c:\gsmg-puzzle-clean\files\cosmic-duality.b64')

containers = [
    ("Terminal", terminal),
    ("SalPhaseIon short", salphaseion_short),
    ("Cosmic Duality", cosmic_duality),
]

def test_password(desc, password_text):
    """Try sha256(password_text) as hex password"""
    password_hex = hashlib.sha256(password_text.encode('utf-8')).hexdigest().lower()
    
    for name, enc in containers:
        result = openssl_aes_decrypt(enc, password_hex)
        if result is not None:
            # Decrypted! Check if meaningful
            print(f"\n{'='*70}")
            print(f"SUCCESS WITH: {desc}")
            print(f"Password text: {password_text}")
            print(f"SHA256 hex: {password_hex}")
            print(f"Container: {name}")
            print(f"Decrypted ({len(result)} bytes):")
            print(f"{'='*70}")
            # Check if it's another nested container
            if result.startswith(b'Salted__'):
                print(f"  [NESTED Salted__ CONTAINER - {len(result)} bytes]")
                print(f"  First 60 bytes hex: {result[:60].hex()}")
            else:
                # Try to display
                printable = sum(1 for b in result if 32 <= b < 127 or b in (9, 10, 13))
                ratio = printable / len(result) if result else 0
                print(f"  Printable ratio: {ratio:.1%}")
                try:
                    text = result.decode('utf-8')
                    print(f"  UTF-8 text preview: {repr(text[:200])}")
                except:
                    try:
                        text = result.decode('latin-1')
                        print(f"  Latin-1 preview: {repr(text[:200])}")
                    except:
                        print(f"  Hex preview: {result[:80].hex()}")
            return True
    return False


# Build a comprehensive list of candidates
candidates = []

# 1. Direct decoded words from STEPS.md (already tried but explicitly double-check)
candidates.append(("thispassword", "thispassword"))
candidates.append(("matrixsumlist", "matrixsumlist"))
candidates.append(("lastwordsbeforearchichoice", "lastwordsbeforearchichoice"))
candidates.append(("enter", "enter"))

# 2. The direct text hints (minus "shabe" prefix?)
full_hint = "shabefourfirsthintisyourlastcommand"
candidates.append(("full hint text", full_hint))
# Try removing "shabe"
if full_hint.startswith("shabe"):
    without_shabe = full_hint[5:]
    candidates.append(("hint without 'shabe' prefix", without_shabe))

# "four first hint" maybe means FOURTH something?
# Or "shabe" = maybe 58? (s=18, h=7, a=0, b=1, e=4 -> 18+7+0+1+4=30) no...
# What if shabe is a word itself? Shift by -4 gives "odwx]" no, -19="lksjx"

# 3. What if "your last command" = Phase 3.2 answer?
phase32_answer = "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
candidates.append(("Phase3.2 full answer", phase32_answer))
# Individual parts
candidates.append(("Phase3.2 riddle1", "jacquefresco"))
candidates.append(("Phase3.2 riddle2", "giveitjustonesecond"))
candidates.append(("Phase3.2 riddle3", "heisenbergsuncertaintyprinciple"))

# 4. Checkerboard output parts
checker_full = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"
candidates.append(("checkerboard FULL lowercase", checker_full.lower()))
candidates.append(("HALF", "HALF"))
candidates.append(("half", "half"))
candidates.append(("BETTERHALF", "BETTERHALF"))
candidates.append(("betterhalf", "betterhalf"))
candidates.append(("HALFBETTERHALF", "HALFBETTERHALF"))
candidates.append(("halfbetterhalf", "halfbetterhalf"))
candidates.append(("HALFANDBETTERHALF", "HALFANDBETTERHALF"))
candidates.append(("halfandbetterhalf", "halfandbetterhalf"))

# 5. Architect text keywords
candidates.append(("THEMATRIXHASYOU", "THEMATRIXHASYOU"))
candidates.append(("thematrixhasyou", "thematrixhasyou"))
candidates.append(("GOODLUCK", "GOODLUCK"))
candidates.append(("goodluck", "goodluck"))
candidates.append(("CIAOBELLAO", "CIAOBELLAO"))
candidates.append(("ciaobellao", "ciaobellao"))
candidates.append(("PRIMEBASICS", "PRIMEBASICS"))
candidates.append(("primebasics", "primebasics"))
candidates.append(("SOURCECODES", "SOURCECODES"))
candidates.append(("sourcecodes", "sourcecodes"))
candidates.append(("TWENTYTHREE", "TWENTYTHREE"))
candidates.append(("twentythree", "twentythree"))
candidates.append(("23", "23"))
candidates.append(("SIXTEEN", "SIXTEEN"))
candidates.append(("sixteen", "sixteen"))
candidates.append(("16", "16"))
candidates.append(("SEVEN", "SEVEN"))
candidates.append(("seven", "seven"))
candidates.append(("7", "7"))

# 6. Chess clue: "fubcd-king" and "oracle-queen"
# From phase3.2 bytes 2143-2291: "fubcd-king & oracle-queen, thingky mvps"
# Checkerboard uses THINGKY and MVPS!
# Row 1: . L E T H I N G K Y  (has THINGKY)
# Row 4: M V P S / J Q Z X W  (has MVPS)
# So chess clue IS referring to checkerboard!
# F U B C D are in row 0 of checkerboard!
# Row 0: F _ U B _ C D O R A
# So: F, U, B, C, D are all there
# fubcd -> let's try that
candidates.append(("fubcd", "fubcd"))
candidates.append(("FUBCD", "FUBCD"))
candidates.append(("oracle", "oracle"))
candidates.append(("ORACLE", "ORACLE"))
candidates.append(("oraclequeen", "oraclequeen"))
candidates.append(("thingky", "thingky"))
candidates.append(("mvps", "mvps"))
candidates.append(("fubcdkingoraclequeen", "fubcdkingoraclequeen"))
candidates.append(("sadboard", "sadboard"))  # "on a sad board"

# 7. What if "shabe" is part of the straddling checkerboard?
# Checkerboard: F U B C D O R A (row 0)
# No S or H in row 0. Row 1 has T H I N G, Row 4 nothing.

# Actually wait - let's look at "shabefourfirsthintisyourlastcommand" again
# "four first hint is your last command"
# Maybe "last command" means the answer from PHASE 3, not 3.2?
# But Phase 3 answer was huge (227 chars). Let's not test whole thing now.

# 8. What about: if we decode the UNUSED runs from SalPhaseIon?
# Run 0-90 (91 chars a-i) and 195-764 (570 chars a-i)
print("\n" + "="*70)
print("Decoding the UNUSED a-i runs (0-90 and 195-764)")
print("="*70)

# Run 0-90: 91 chars of a-i
run1 = content[0:91]
# It's a-i only, no o, so it won't decode with the aio method (no zeros)
# But wait - could it be just direct digits? a=1 to i=9
run1_digits = ''.join(str(ord(c) - ord('a') + 1) for c in run1)
print(f"\nRun 0-91 ({len(run1)} chars a-i):")
print(f"  As digits: {len(run1_digits)} digits, starts with {run1_digits[:50]}...")
# 91 chars -> 91 digits (if each a-i is 1 digit). That's not enough for a full byte-stream.
# But wait - maybe it's actually a NUMBER (like the 149 digits)?

# Run 195-764: 570 chars
run2 = content[195:765]
run2_digits = ''.join(str(ord(c) - ord('a') + 1) for c in run2)
print(f"\nRun 195-764 ({len(run2)} chars a-i):")
print(f"  As digits: {len(run2_digits)} digits, starts with {run2_digits[:50]}...")

# What if these are actually like the a/b binary but with 9 states? Unclear.

# Try concatenating ALL the decoded words
all_decoded = "thispassword" + "matrixsumlist" + "lastwordsbeforearchichoice" + "enter"
candidates.append(("all decoded concatenated", all_decoded))

# 9. Also test: what if the password is literally "password"? Or something too obvious?
candidates.append(("password", "password"))
candidates.append(("Password123", "Password123"))
candidates.append(("gsmg", "gsmg"))
candidates.append(("GSMG", "GSMG"))
candidates.append(("GSMG.io", "GSMG.io"))
candidates.append(("gsmgio5btcpuzzle", "gsmgio5btcpuzzle"))

print(f"\nTesting {len(candidates)} password candidates...")

success = False
for desc, pw_text in candidates:
    if test_password(desc, pw_text):
        success = True
        print(f"\nFOUND WITH: {desc}")
        break

if not success:
    print("\nNo decryptions with these candidates.")

print("\nDone.")
