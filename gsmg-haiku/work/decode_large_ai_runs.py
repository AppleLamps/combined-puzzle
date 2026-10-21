#!/usr/bin/env python3
"""
Decode the LARGE a-i,o runs from SalPhaseIon page that were not decoded.

From STEPS.md:
- Large run 1: len=91 chars (all a-i, no o, no digits 0)
  These are digits 1-9, need to be decoded.
  
- Large run 2: len=570 chars (all a-i)
  More digits.

These were marked [kit] - never re-verified! Let's decode them properly.

Also:
- The four decoded words have lengths: 14, 28, 78, 28
  Maybe these are OFFSETS into these large runs?
"""

import os
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def a_i_o_to_digit(c):
    """a-i,o -> digit: a=1...i=9, o=0"""
    if c == 'o':
        return 0
    # a=1, b=2, ..., i=9
    return ord(c) - ord('a') + 1

def digits_to_hex_to_ascii(digit_string):
    """Convert even-length digit string to hex then to ASCII."""
    result = []
    for i in range(0, len(digit_string), 2):
        hex_pair = digit_string[i:i+2]
        result.append(chr(int(hex_pair, 16)))
    return ''.join(result)

# Read SalPhaseIon page
with open(os.path.join(BASE_DIR, 'files', 'salphaseion-page.txt'), 'r') as f:
    page = f.read()

print("="*70)
print("SalPhaseIon Page Analysis")
print("="*70)

# Find all a-i,o runs
# From STEPS.md we know:
# - First 147 chars: mixed a,i,j,z,g,t,v,p,h,d,q,u,x,y,k,n,m,l,b,f,w,e,r,s,o (coded digits)
# - Then: 27 chars of a,b = binary -> "thispassword"
# - Then: 55 chars of a,b = binary -> "matrixsumlist"
# - Then: 153 chars of a,b = binary -> "lastwordsbeforearchichoice"
# - Then: 56 chars of a,b = binary -> "enter"
# - Then: LARGE RUN 1: 91 chars of a-i (no o, no zeros)
# - Then: 56 chars of a,b (binary, not decoded yet!)
# - Then: LARGE RUN 2: 570 chars of a-i

# Let me just find all a,b sequences and a-i sequences.

import re

# Find all runs of [ab]+ and [a-o]+
ab_runs = []
for m in re.finditer(r'[ab]+', page):
    ab_runs.append((m.start(), m.end(), m.group()))

ai_runs = []
for m in re.finditer(r'[a-o]+', page):
    # Exclude pure a,b runs
    if set(m.group()) <= {'a', 'b'}:
        continue
    ai_runs.append((m.start(), m.end(), m.group()))

print(f"\nFound {len(ab_runs)} pure a/b runs (binary):")
for i, (start, end, text) in enumerate(ab_runs):
    # Decode a,b binary
    bits = ''.join('0' if c == 'a' else '1' for c in text)
    decoded = ''
    for j in range(0, len(bits), 8):
        byte_str = bits[j:j+8]
        if len(byte_str) == 8:
            decoded += chr(int(byte_str, 2))
    print(f"  Run {i}: pos {start}-{end-1}, len={end-start} bits, decoded: '{decoded}'")

print(f"\nFound {len(ai_runs)} a-i,o runs (digit-coded):")
for i, (start, end, text) in enumerate(ai_runs):
    digits = ''.join(str(a_i_o_to_digit(c)) for c in text)
    print(f"\n  Run {i}: pos {start}-{end-1}, len={end-start} chars")
    print(f"    As digits: {len(digits)} digits")
    print(f"    First 100 digits: {digits[:100]}")
    
    # Try decoding as hex (2 digits per byte)
    if len(digits) % 2 == 0:
        decoded = digits_to_hex_to_ascii(digits)
        print(f"    Decoded as hex: {repr(decoded[:200])}")
    else:
        # Try dropping first digit
        decoded_drop1 = digits_to_hex_to_ascii(digits[1:])
        print(f"    Decoded hex (drop 1st): {repr(decoded_drop1[:200])}")
        # Try dropping last digit
        decoded_drop_last = digits_to_hex_to_ascii(digits[:-1])
        print(f"    Decoded hex (drop last): {repr(decoded_drop_last[:200])}")

print("\n" + "="*70)
print("Analyzing the four decoded word POSITIONS as potential pointers")
print("="*70)

# The words appear at positions:
# word 1: "thispassword" at binary run after the first 147 chars
# Actually let me check what we have in derived/salphaseion-digits.txt
with open(os.path.join(BASE_DIR, 'derived', 'salphaseion-digits.txt'), 'r') as f:
    sp_digits = f.read().strip()

print(f"\nsalphaseion-digits.txt: {len(sp_digits)} digits")
print(f"First 100: {sp_digits[:100]}")
print(f"Last 100: {sp_digits[-100:]}")

# Now: the four words are:
# 1. "thispassword" - 14 chars
# 2. "matrixsumlist" - 28 chars  
# 3. "lastwordsbeforearchichoice" - 78 chars
# 4. "enter" -... wait let me decode properly

print("\n" + "="*70)
print("Let me decode these exact word lengths:")
print("="*70)

word_lengths = [14, 28, 78, 5]  # Actually check binary:
# "thispassword" = 112 bits = 14 bytes
# "matrixsumlist" = 14 chars? No wait let me decode properly

# From earlier we know:
binary_passwords = [
    ("ab1 (27 bits? No, should be 8*n)", 27, "thispassword"),
    ("ab2 (55 bits)", 55, "matrixsumlist"),
    ("ab3 (153 bits)", 153, "lastwordsbeforearchichoice"),
    ("ab4 (56 bits)", 56, "enter"),
]

# Wait: 27 bits = 3 bytes + 3 bits? No, that can't be.
# Let me look at STEPS.md again for the exact decoding.

print("\n" + "="*70)
print("Key insight: 14, 28, 78 = these are LENGTHS/OFFSETS")
print("="*70)

# 14, 28, 78...
# What if these are:
# - byte offsets into something
# - digit counts to take from the 149-digit checkerboard
# - lengths of the words * 2 for hex pairs

checkerboard_149 = "243861484085950432746691484837228651853674614516019014964141582136514240674223561435155165498418732684459841315648424767494131419479611841498494164946147"

# 14 and 28 and 78 are even numbers
# Try: take first 14 digits as hex, then next 28, etc

if len(checkerboard_149) >= 14+28+78+28:  # 14+28+78+28 = 148! That's almost 149!
    print(f"\n14 + 28 + 78 + 28 = {14+28+78+28} digits")
    print(f"Checkerboard has {len(checkerboard_149)} digits!")
    
    chunks = [
        (0, 14, "thispassword-length"),
        (14, 14+28, "matrixsumlist-length"),
        (14+28, 14+28+78, "lastwordsbeforearchichoice-length"),
        (14+28+78, 14+28+78+28, "enter-length"),
    ]
    
    password_candidates = []
    for start, end, label in chunks:
        digit_chunk = checkerboard_149[start:end]
        if len(digit_chunk) % 2 == 0:
            text = digits_to_hex_to_ascii(digit_chunk)
        else:
            # Drop one digit
            text = digits_to_hex_to_ascii(digit_chunk[1:]) if len(digit_chunk) > 1 else ''
        print(f"\n  {label}: digits {start}-{end-1} = {digit_chunk}")
        print(f"    Decoded: {repr(text)}")
        password_candidates.append((label, text))
        
        # Also try: uppercase, lowercase variations
        if text.strip():
            password_candidates.append((label+"_lower", text.lower()))
            password_candidates.append((label+"_upper", text.upper()))
    
    # Also try concatenating
    full_concat = ''.join(digits_to_hex_to_ascii(checkerboard_149[i:i+2]) 
                           for i in range(0, 148, 2))
    print(f"\n  All 148 digits decoded: {repr(full_concat)}")
    password_candidates.append(("checkerboard_first_148_hex", full_concat))
    
    # Also try the 149th digit included (skip first to make even)
    skip1 = ''.join(digits_to_hex_to_ascii(checkerboard_149[i:i+2]) 
                     for i in range(1, 149, 2))
    print(f"  Skip first digit: {repr(skip1)}")
    password_candidates.append(("checkerboard_skip1_hex", skip1))

# Now let's test these candidates!
print("\n" + "="*70)
print("Testing these candidates against all three containers")
print("="*70)

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
        printable = sum(1 for b in plaintext if 32 <= b < 127 or b in (9, 10, 13))
        printable_ratio = printable / total if total > 0 else 1.0
        return True, plaintext, printable_ratio
    except:
        return False, None, 0.0

def load_b64(name):
    with open(os.path.join(BASE_DIR, 'files', name), 'r') as f:
        return name, base64.b64decode(''.join(f.read().split()))

containers = [
    load_b64('terminal.b64'),
    load_b64('salphaseion-short.b64'),
    load_b64('cosmic-duality.b64'),
]

total_tested = 0
for label, ans in password_candidates:
    if not ans or len(ans.strip()) == 0:
        continue
    
    # Original
    pw = hashlib.sha256(ans.encode()).hexdigest().lower()
    total_tested += 1
    
    for cname, cdata in containers:
        success, dec, ratio = try_decrypt(cdata, pw)
        if success:
            print(f"\n{'='*70}")
            print(f"SUCCESS with {label} on {cname}!")
            print(f"  Answer: {repr(ans[:100])}...")
            print(f"  Password hex: {pw}")
            print(f"  Decrypted: {len(dec)} bytes, {ratio:.1%} printable")
            if dec.startswith(b'Salted__'):
                print(f"  --> NESTED CONTAINER! Inner salt: {dec[8:16].hex()}")
            print(f"  First 64 hex: {dec[:64].hex()}")

# Also try: checkerboard digits directly as password input (not hex decoded)
print(f"\nAlso trying checkerboard digits directly as answer...")
direct_candidates = [
    ("checkerboard_full", checkerboard_149),
    ("checkerboard_first_148", checkerboard_149[:148]),
    ("checkerboard_skip1", checkerboard_149[1:]),
]

for label, ans in direct_candidates:
    pw = hashlib.sha256(ans.encode()).hexdigest().lower()
    total_tested += 1
    for cname, cdata in containers:
        success, dec, ratio = try_decrypt(cdata, pw)
        if success:
            print(f"\n{'='*70}")
            print(f"SUCCESS with {label} on {cname}!")
            print(f"  Answer: {ans[:100]}...")
            print(f"  Password hex: {pw}")
            print(f"  Decrypted: {len(dec)} bytes, {ratio:.1%} printable")

print(f"\nTested {total_tested} candidates total.")

print("\nDone.")
