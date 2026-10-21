#!/usr/bin/env python3
"""
GSMG Puzzle - Robust password testing
"""

import hashlib
import base64
import sys
sys.path.insert(0, r'c:\gsmg-puzzle-clean\work')

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def derive_key_and_iv(password: str, salt: bytes) -> tuple[bytes, bytes]:
    """OpenSSL EVP_BytesToKey with SHA-256, 1 iteration."""
    password_bytes = password.encode('utf-8')
    D_i = b''
    result = b''
    while len(result) < 48:
        md = hashlib.sha256()
        md.update(D_i + password_bytes + salt)
        D_i = md.digest()
        result += D_i
    return result[:32], result[32:48]

def try_decrypt(data: bytes, password_hex: str) -> tuple[bool, bytes | None, str]:
    """Try to decrypt. Returns (success, plaintext, status_desc)."""
    if not data.startswith(b'Salted__'):
        return False, None, "Invalid format"
    
    salt = data[8:16]
    ciphertext = data[16:]
    key, iv = derive_key_and_iv(password_hex, salt)
    
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return True, plaintext, "DECRYPTED"
    except ValueError as e:
        if "Padding" in str(e):
            return False, None, "bad padding"
        return False, None, f"error: {e}"

def load_b64(path):
    with open(path, 'r') as f:
        return base64.b64decode(f.read())

# Load containers
terminal = load_b64(r'c:\gsmg-puzzle-clean\files\terminal.b64')
salphaseion_short = load_b64(r'c:\gsmg-puzzle-clean\files\salphaseion-short.b64')
cosmic_duality = load_b64(r'c:\gsmg-puzzle-clean\files\cosmic-duality.b64')

print(f"Terminal: {len(terminal)} bytes, salt = {terminal[8:16].hex()}")
print(f"SalPhaseIon short: {len(salphaseion_short)} bytes, salt = {salphaseion_short[8:16].hex()}")
print(f"Cosmic Duality: {len(cosmic_duality)} bytes, salt = {cosmic_duality[8:16].hex()}")

containers = [
    ("Terminal", terminal),
    ("SalPhaseIon short", salphaseion_short),
    ("Cosmic Duality", cosmic_duality),
]

def analyze_plaintext(name: str, plaintext: bytes, answer_text: str, password_hex: str):
    print(f"\n{'='*70}")
    print(f"SUCCESS DECRYPTING: {name}")
    print(f"  Answer text: {answer_text}")
    print(f"  Password hex: {password_hex}")
    print(f"  Plaintext length: {len(plaintext)} bytes")
    print(f"{'='*70}")
    
    if plaintext.startswith(b'Salted__'):
        print(f"  -> NESTED ENCRYPTED CONTAINER! Starts with Salted__")
        inner_salt = plaintext[8:16]
        print(f"  -> Inner salt: {inner_salt.hex()}")
        print(f"  -> Inner total: {len(plaintext)} bytes")
    else:
        # Check characteristics
        printable = sum(1 for b in plaintext if 32 <= b < 127 or b in (9, 10, 13))
        ratio = printable / len(plaintext) if plaintext else 0
        print(f"  Printable ratio: {ratio:.1%} ({printable}/{len(plaintext)})")
        try:
            text = plaintext.decode('utf-8')
            print(f"\n  UTF-8 content:")
            print("-"*50)
            print(text[:3000])
            if len(text) > 3000:
                print(f"\n  ... and {len(text)-3000} more chars")
        except:
            try:
                text = plaintext.decode('latin-1')
                print(f"\n  Latin-1 preview (first 200): {repr(text[:200])}")
            except:
                print(f"\n  Hex preview: {plaintext[:100].hex()}")
    
    # Record
    with open(r'c:\gsmg-puzzle-clean\work\FOUND_' + name.replace(' ', '_') + '.bin', 'wb') as f:
        f.write(plaintext)
    with open(r'c:\gsmg-puzzle-clean\work\FOUND_password.txt', 'w') as f:
        f.write(f"Container: {name}\n")
        f.write(f"Answer: {answer_text}\n")
        f.write(f"Password hex: {password_hex}\n")
    print(f"\n  Saved to work/FOUND_* files")
    
    return True

# ============================================================
# Build candidate list
# ============================================================

candidates = []

# 1. The explicitly decoded words from SalPhaseIon
candidates.append(("thispassword", "thispassword"))
candidates.append(("matrixsumlist", "matrixsumlist"))
candidates.append(("lastwordsbeforearchichoice", "lastwordsbeforearchichoice"))
candidates.append(("enter", "enter"))

# 2. Combinations
all4 = "thispassword" + "matrixsumlist" + "lastwordsbeforearchichoice" + "enter"
candidates.append(("all 4 decoded words concat", all4))

# Try permutations of 2-4 words
# But we know Phase 2 was 1 word, Phase 3.2 was 3 words concatenated

# 3. Direct text hints from textarea
# "shabefourfirsthintisyourlastcommand"
# "shabefanstoo"

full_hint = "shabefourfirsthintisyourlastcommand"
candidates.append(("text hint full", full_hint))

# Try without "shabe" prefix
if full_hint.startswith("shabe"):
    without = full_hint[5:]
    candidates.append(("hint without 'shabe'", without))

candidates.append(("shabefanstoo", "shabefanstoo"))

# If "shabe" means something...
# Checkerboard: Row 0 = F _ U B _ C D O R A
# No S/H in row 0. Row 1: . L E T H I N G K Y -> has H!
# Row 4: M V P S / ... -> has S!
# So:
#   S = Row 4 prefix '4', then column 3
#   H = Row 1 prefix '1', then column 4
#   A = Row 0, column 9
#   B = Row 0, column 3
#   E = Row 1, column 2

# But that's encoding, not decoding.

# 4. Checkerboard plaintext
checker = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"
candidates.append(("checkerboard lowercase", checker.lower()))
candidates.append(("checkerboard uppercase", checker))

# Extract the key names
candidates.append(("HALF", "HALF"))
candidates.append(("half", "half"))
candidates.append(("BETTERHALF", "BETTERHALF"))
candidates.append(("betterhalf", "betterhalf"))
candidates.append(("halfandbetterhalf", "halfandbetterhalf"))
candidates.append(("halfbettterhalf", "halfbettterhalf"))  # typo?
candidates.append(("HALFBETTERHALF", "HALFBETTERHALF"))

# 5. Chess clue from phase3.2 ending
# "fubcd-king & oracle-queen, thingky mvps on a sad board"
candidates.append(("fubcd", "fubcd"))
candidates.append(("FUBCD", "FUBCD"))
candidates.append(("oracle", "oracle"))
candidates.append(("oraclequeen", "oraclequeen"))
candidates.append(("thingky", "thingky"))
candidates.append(("THINGKY", "THINGKY"))
candidates.append(("mvps", "mvps"))
candidates.append(("MVPS", "MVPS"))
candidates.append(("thingkymvps", "thingkymvps"))
candidates.append(("fubcdoracle", "fubcdoracle"))
candidates.append(("sadboard", "sadboard"))

# 6. Architect text keywords
candidates.append(("thematrixhasyou", "thematrixhasyou"))
candidates.append(("THEMATRIXHASYOU", "THEMATRIXHASYOU"))  # The Beaufort key used!
candidates.append(("goodluck", "goodluck"))
candidates.append(("GOODLUCK", "GOODLUCK"))
candidates.append(("ciaobellao", "ciaobellao"))
candidates.append(("CIAOBELLAO", "CIAOBELLAO"))
candidates.append(("primebasics", "primebasics"))
candidates.append(("PRIMEBASICS", "PRIMEBASICS"))
candidates.append(("sourcecodes", "sourcecodes"))
candidates.append(("SOURCECODES", "SOURCECODES"))
candidates.append(("twentythree", "twentythree"))
candidates.append(("sixteen", "sixteen"))
candidates.append(("seven", "seven"))
candidates.append(("23", "23"))
candidates.append(("16", "16"))
candidates.append(("7", "7"))

# 7. Previous answers (in case they're reused)
# P3 answer was huge. Let's not test whole thing.
# P3.2 answer:
phase32_answer = "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
candidates.append(("phase3.2 answer", phase32_answer))
# Individual parts
candidates.append(("jacquefresco", "jacquefresco"))
candidates.append(("giveitjustonesecond", "giveitjustonesecond"))
candidates.append(("heisenbergsuncertaintyprinciple", "heisenbergsuncertaintyprinciple"))

# Phase 2 answer
candidates.append(("causality", "causality"))

# 8. Try the first parts of hints as "last command"
# "shabefourfirsthintisyourlastcommand" -> "last command" could be "isyourlastcommand"
candidates.append(("last command substring", "isyourlastcommand"))

# 9. What about "GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"?
# That's what was hashed to find the SalPhaseIon page URL
page_url_seed = "GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
candidates.append(("SalPhaseIon page URL seed", page_url_seed))

# 10. Try variations of passwords with case - maybe answer is upper case?
# Wait: password is SHA256(answer_text) so case matters!
# Let's also try upper-case variants of thispassword etc
candidates.append(("THISPASSWORD", "THISPASSWORD"))
candidates.append(("MATRIXSUMLIST", "MATRIXSUMLIST"))

# 11. The 149 digits themselves (as string)
with open(r'c:\gsmg-puzzle-clean\derived\checkerboard-digits.txt', 'r') as f:
    digits149 = f.read().strip()
candidates.append(("149 digits raw string", digits149))

# Maybe reverse?
candidates.append(("149 digits reversed", digits149[::-1]))

# 12. What about the salt values themselves? The README gives them
# terminal salt = b45a5e3d827593ca, salphaseion_short = 3ab585348552415d, cosmic = 2d3f6fe06dc950e6
# But these are per-container and password shouldn't depend on salt (key derivation mixes them)

# 13. What about "first" "last" from hints?
# "four first hint is your last command"
candidates.append(("fourfirst", "fourfirst"))
candidates.append(("firsthint", "firsthint"))
candidates.append(("lastcommand", "lastcommand"))

# 14. Try "intertwined" - maybe the passwords are interleaved characters?
# e.g. take first char of thispassword, first of matrixsumlist, etc.
tp = "thispassword"
ms = "matrixsumlist"
lw = "lastwordsbeforearchichoice"
en = "enter"

# Interleave them character by character
min_len = min(len(tp), len(ms), len(lw))  # en is shortest
interleaved = ''
for i in range(min(len(en), min(len(tp), len(ms), len(lw)))):
    interleaved += tp[i] + ms[i] + lw[i] + en[i]
candidates.append(("interleaved 4 words by min(enter)", interleaved))

# Or pair-wise
interleaved_2 = ''
for i in range(min(len(tp), len(ms))):
    interleaved_2 += tp[i] + ms[i]
candidates.append(("interleaved thispassword+matrixsumlist", interleaved_2))

# 15. Try "shabe" + something
# "shabefourfirsthint..." - maybe "shabe" is the actual password?
candidates.append(("shabe", "shabe"))
candidates.append(("SHABE", "SHABE"))

# 16. The straddling checkerboard key itself?
# Row 0: F U B C D O R A
# Row 1: L E T H I N G K Y (plus prefix 1 and escape .)
# Row 4: M V P S J Q Z X W (plus prefix 4 and escape /)
row0 = "FUB CDOR A"  # Actually: indices 0=F, 2=U, 3=B, 5=C, 6=D, 7=O, 8=R, 9=A
# Full row 0 is: F _ U B _ C D O R A
row0_full = "F U B C D O R A"
row1_full = "L E T H I N G K Y"
row4_full = "M V P S J Q Z X W"
candidates.append(("FUB", "FUB"))
candidates.append(("THINGKY", "THINGKY"))
candidates.append(("MVPS", "MVPS"))

print(f"\nTotal candidates to test: {len(candidates)}\n")

found_any = False
count = 0

for desc, answer_text in candidates:
    count += 1
    password_hex = hashlib.sha256(answer_text.encode('utf-8')).hexdigest().lower()
    
    for name, enc in containers:
        success, plaintext, status = try_decrypt(enc, password_hex)
        if success:
            found_any = analyze_plaintext(name, plaintext, answer_text, password_hex) or found_any
            break
    
    if count % 20 == 0:
        print(f"  Tested {count}/{len(candidates)}...")

if not found_any:
    print(f"\nAll {len(candidates)} candidates tested. No valid decryptions.")
    print("\nNotes:")
    print("  - 'thispassword' etc are explicitly decoded - but for WHAT?")
    print("  - Maybe they are NOT the actual answer text, but clues ABOUT the answer?")
    print("  - Or maybe we need to encode them back to a/b or a-i/o and use that?")
    print("  - Or maybe the answer isn't text but numbers? (like the 149 digits)")

print("\nDone.")
