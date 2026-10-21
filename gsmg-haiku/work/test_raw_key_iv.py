#!/usr/bin/env python3
"""
Test the second base64 block as a RAW AES key+IV:
- 48 bytes = 32 bytes (AES-256 key) + 16 bytes (IV)

If this works, we don't need to derive key from password!
Just use this key+IV directly.

Also test: "four first hint" -> take first hints/words
"""

import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_b64(name):
    with open(os.path.join(BASE_DIR, 'files', name), 'r') as f:
        return name, base64.b64decode(''.join(f.read().split()))

# Load all containers
containers = [
    load_b64('terminal.b64'),
    load_b64('salphaseion-short.b64'),
    load_b64('cosmic-duality.b64'),
]

# The second base64 block from SalPhaseIon textarea
second_b64 = 'QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ'
second_decoded = base64.b64decode(second_b64)

print("="*70)
print("Testing second base64 as RAW AES-256-CBC key+IV")
print("="*70)
print(f"\nSecond base64 decoded: {len(second_decoded)} bytes")
print(f"Hex: {second_decoded.hex()}")

# Could be:
# Option 1: first 32 = key, last 16 = IV
key1 = second_decoded[:32]
iv1 = second_decoded[16:32]  # if it's 32+16, the 16 starts at 32 not 16...
# Wait: 48 bytes. Positions:
# 0-31 = 32 bytes = potential key
# 16-31 = 16 bytes = overlap area, could be IV if key is only 16?
# 32-47 = 16 bytes = potential IV

# Actually for AES-256 we need 32-byte key and 16-byte IV:
# 48 = 32 + 16
key_256 = second_decoded[:32]  # 32 bytes for AES-256 key
iv_256 = second_decoded[32:]   # remaining 16 bytes for IV

print(f"\nOption: key = bytes 0-31, IV = bytes 32-47")
print(f"  Key: {key_256.hex()} ({len(key_256)} bytes)")
print(f"  IV:  {iv_256.hex()} ({len(iv_256)} bytes)")

# Also try: key = bytes 16-47, IV = bytes 0-15
key_alt = second_decoded[16:]
iv_alt = second_decoded[:16]

# Also try AES-128 (16-byte key):
key_128_v1 = second_decoded[:16]
key_128_v2 = second_decoded[16:32]
key_128_v3 = second_decoded[32:]

def try_direct_decrypt(ciphertext_bytes, key, iv):
    """Try AES-CBC decrypt directly (no Salted__ header processing)"""
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext_bytes), AES.block_size)
        total = len(plaintext)
        printable = sum(1 for b in plaintext if 32 <= b < 127 or b in (9, 10, 13))
        printable_ratio = printable / total if total > 0 else 1.0
        return True, plaintext, printable_ratio
    except Exception as e:
        return False, None, 0.0

print(f"\nTesting against all containers...")

for cname, cdata in containers:
    print(f"\n--- {cname} ---")
    print(f"  Total: {len(cdata)} bytes")
    
    # Extract from Salted__ format
    if cdata.startswith(b'Salted__'):
        salt = cdata[8:16]
        ciphertext = cdata[16:]
        print(f"  Salt: {salt.hex()}")
        print(f"  Ciphertext: {len(ciphertext)} bytes = {len(ciphertext)/16:.0f} AES blocks")
        
        # Try AES-256: key=0-31, iv=32-47
        success, dec, ratio = try_direct_decrypt(ciphertext, key_256, iv_256)
        if success:
            print(f"\n    SUCCESS with AES-256 key=0-31, iv=32-47!")
            print(f"    Decrypted: {len(dec)} bytes, {ratio:.1%} printable")
            if dec.startswith(b'Salted__'):
                print(f"    --> NESTED CONTAINER! Inner salt: {dec[8:16].hex()}")
            print(f"    Hex first 100: {dec[:100].hex()}")
            if ratio > 0.5:
                print(f"    Text: {dec[:200]}")
        
        # Try AES-256 alt: key=16-47, iv=0-15
        success, dec, ratio = try_direct_decrypt(ciphertext, key_alt, iv_alt)
        if success:
            print(f"\n    SUCCESS with AES-256 key=16-47, iv=0-15!")
            print(f"    Decrypted: {len(dec)} bytes, {ratio:.1%} printable")
        
        # Try AES-128 variants
        for i, (k_name, k) in enumerate([
            ("key0-15", key_128_v1),
            ("key16-31", key_128_v2),
            ("key32-47", key_128_v3),
        ]):
            for j, (iv_name, iv) in enumerate([
                ("iv0-15", iv_alt),
                ("iv16-31", second_decoded[16:32]),
                ("iv32-47", iv_256),
            ]):
                success, dec, ratio = try_direct_decrypt(ciphertext, k, iv)
                if success:
                    print(f"\n    SUCCESS with AES-128 {k_name}, {iv_name}!")
                    print(f"    Decrypted: {len(dec)} bytes, {ratio:.1%} printable")

print("\n" + "="*70)
print("Now try: 'four first hint' - take the four words")
print("="*70)

# The four words are:
four_words = [
    "thispassword",
    "matrixsumlist", 
    "lastwordsbeforearchichoice",
    "enter"
]

# Also, the phrase "fourfirsthintisyourlastcommand" - maybe:
# "four first hint" = take first char of each hint: t, m, l, e
# Or "your last command" - phase 3.2 answer?

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

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

def try_decrypt(data: bytes, answer: str):
    password = hashlib.sha256(answer.encode()).hexdigest().lower()
    if not data.startswith(b'Salted__'):
        return False, None, 0.0
    salt = data[8:16]
    ciphertext = data[16:]
    try:
        key, iv = derive_key_and_iv(password, salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        total = len(plaintext)
        printable = sum(1 for b in plaintext if 32 <= b < 127 or b in (9, 10, 13))
        printable_ratio = printable / total if total > 0 else 1.0
        return True, plaintext, printable_ratio
    except:
        return False, None, 0.0

candidates = []

# Take first letters
first_letters = ''.join(w[0] for w in four_words)  # t, m, l, e
candidates.append(("first_letters_tmle", first_letters))
candidates.append(("first_letters_upper", first_letters.upper()))

# Take last letters
last_letters = ''.join(w[-1] for w in four_words)  # d, t, e, r
candidates.append(("last_letters_dter", last_letters))

# Try combining different parts
import itertools

# Concatenate all 4 in order
candidates.append(("all_four_ordered", ''.join(four_words)))

# All permutations
for perm in itertools.permutations(four_words):
    label = f"perm_{''.join(p[:2] for p in perm)}"
    candidates.append((label, ''.join(perm)))

# Try "four first hint" -> maybe use first "hint" word, repeat 4 times?
# The words might themselves BE hints
# "thispassword" -> "this" + "password"
# "matrixsumlist" -> "matrix", "sum", "list"
# "lastwordsbeforearchichoice" -> "lastwords", "before", "archi", "choice"
# "enter" -> just "enter"

# Try breaking down compound words
for w in four_words:
    # Try word itself
    candidates.append((f"word_{w}", w))
    # Try lower
    candidates.append((f"word_{w}_lower", w.lower()))
    # Try upper
    candidates.append((f"word_{w}_upper", w.upper()))

# Also try "fourfirsthintisyourlastcommand" itself and parts
ffh = "fourfirsthintisyourlastcommand"
candidates.append(("fourfirsthint_full", ffh))
candidates.append(("fourfirsthint", "fourfirsthint"))
candidates.append(("yourlastcommand", "yourlastcommand"))
candidates.append(("lastcommand", "lastcommand"))

# Also try the decoded Phase 2 and 3.2 answers as well
candidates.append(("phase2_causality", "causality"))
candidates.append(("phase32_full", "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"))

# What about "four first hint is your last command" -> 
# "four" = 4, "first hint" = first decoded word, "last command" = last phase answer?

# Let me also try:
# - The decoded "lastwordsbeforearchichoice" literally means: take the bytes 0-446
#   but we tried that. What about take LAST WORDS from it?

# Actually we know "lastwordsbeforearchichoice" POINTED TO the bytes 0-446
# So what if:
# "thispassword" POINTS TO something (the actual password text)
# "matrixsumlist" POINTS TO an operation (sum a matrix or list)
# "enter" POINTS TO an operation (add newline, or enter = submit)

print(f"\nGenerated {len(candidates)} candidates from four words...")

# Load phase3.2 binary for analysis
with open(os.path.join(BASE_DIR, 'derived', 'phase3.2-plaintext.bin'), 'rb') as f:
    phase32 = f.read()

before_archi = phase32[0:447].decode('latin-1')
# What are the last words before architect?
# "One for one, four for one."

# Try those
candidates.append(("last_sentence", "One for one, four for one"))
candidates.append(("last_sentence_nopunc", "One for one four for one"))
candidates.append(("last_sentence_upper", "ONE FOR ONE, FOUR FOR ONE"))
candidates.append(("last_sentence_nospace", "Oneforonefourforone"))
candidates.append(("last_sentence_nospace_upper", "ONEFORONEFOURFORONE"))

# Try "four for one" specifically
candidates.append(("fourforone", "four for one"))
candidates.append(("fourforone_nospace", "fourforone"))
candidates.append(("FOURFORONE", "FOURFORONE"))

# One for one
candidates.append(("oneforone", "one for one"))
candidates.append(("ONEFORONE", "ONEFORONE"))

# Also from the text section 3b decoded earlier... it looked weird.
# Let me try to decode it properly.

print(f"\nNow total candidates: {len(candidates)}. Testing...")

successes = []

for label, ans in candidates:
    for cname, cdata in containers:
        success, dec, ratio = try_decrypt(cdata, ans)
        if success:
            print(f"\n{'='*70}")
            print(f"SUCCESS: {label} on {cname}")
            print(f"  Answer: {repr(ans[:100])}...")
            print(f"  Decrypted: {len(dec)} bytes, {ratio:.1%} printable")
            if dec.startswith(b'Salted__'):
                print(f"  --> NESTED CONTAINER! Inner salt: {dec[8:16].hex()}")
            print(f"  First 80 hex: {dec[:80].hex()}")
            if ratio > 0.5:
                try:
                    print(f"  Text: {dec[:200].decode('latin-1')}")
                except:
                    pass
            successes.append((label, ans, cname, dec, ratio))

if not successes:
    print(f"\nNo successes with these candidates.")

print("\n" + "="*70)
print("Key insight: we have RAW 48 bytes = key+IV")
print("="*70)
print("""
Wait! SalPhaseIon has TWO base64 blocks:
1. First block: Salted__ format (needs password)
2. Second block: RAW 48 bytes = AES-256 key + IV

But what if:
- The second block is the KEY+IV for SOMETHING
- But what ciphertext?

Options:
A. Decrypt the FIRST base64 block's ciphertext using this key+IV
   (Bypass the Salted__ key derivation)

B. Maybe the key+IV is for decrypting something in the 570-char run?

C. Maybe the "four first hint" tells us how to USE this key+IV?

Actually let me think about "four first hint is your last command":
- "four first" -> 4 bytes? or 4 somethings?
- "hint is your" -> the hint IS something
- "last command" -> maybe Phase 3.2 answer was the last solved thing?

Also: "shabefanstoo" at end... "shabe" appears twice:
1. Before "fourfirsthint": "shabefourfirsthint..."
2. At very end: "shabefanstoo"

shabe decoded via a-i? s=19, h=8, a=1, b=2, e=5 -> no
shabe decoded via a,b binary? s,h are not a,b...

Actually "shabe" -> maybe just random padding/alignment chars?
""")

print("\nDone.")
