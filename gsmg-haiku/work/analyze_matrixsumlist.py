#!/usr/bin/env python3
"""
Explore "matrixsumlist":
- The chess board / section 3b (bytes 127-446 of Phase 3.2)
- "sum" could mean:
  1. Sum of digit values from checkerboard
  2. Sum of some numeric interpretation
  3. Sum of ASCII values
  4. XOR "sum"
  5. Concatenation (like "sum of parts")

Also explore:
- "four first hint" -> take first 4 of something
- The 48-byte second base64 block
- HALF and BETTERHALF
"""

import os
import base64
import hashlib
import itertools
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

def load_b64(name):
    with open(os.path.join(BASE_DIR, 'files', name), 'r') as f:
        return name, base64.b64decode(''.join(f.read().split()))

containers = [
    load_b64('terminal.b64'),
    load_b64('salphaseion-short.b64'),
    load_b64('cosmic-duality.b64'),
]

# Read phase 3.2
with open(os.path.join(BASE_DIR, 'derived', 'phase3.2-plaintext.bin'), 'rb') as f:
    phase32 = f.read()

# Checkerboard 149 digits
with open(os.path.join(BASE_DIR, 'files', 'salphaseion-textarea.txt'), 'r') as f:
    sp_textarea = f.read()

# Let me find the checkboard digits properly from the decoded
# Actually STEPS.md has this. Let me search for the 149 digits
checkerboard_149 = None
with open(os.path.join(BASE_DIR, 'derived', 'checkerboard-digits.txt'), 'r') as f:
    # Wait this file was only 150 chars
    cb_content = f.read().strip()
    if cb_content.isdigit():
        checkerboard_149 = cb_content
        print(f"checkerboard-digits.txt: {len(checkerboard_149)} digits (numeric)")
    else:
        print(f"checkerboard-digits.txt is NOT pure digits: {repr(cb_content[:100])}")

# The REAL checkerboard digits should be in another place.
# Let's look at section 1990-2138 of Phase 3.2 per STEPS.md:
section_4b_digits_area = phase32[1990:2139]
print(f"\nPhase 3.2 bytes 1990-2138: {len(section_4b_digits_area)} bytes")
print(f"  First 100: {section_4b_digits_area[:100]}")
print(f"  As ASCII: {section_4b_digits_area.decode('latin-1')[:100]}...")

# These should be the 149 straddling-checkerboard-encoded digits
# Let's also look at what's in the textarea file
print(f"\nsalphaseion-textarea.txt starts with:")
print(f"  {sp_textarea[:200]}")

# Actually I need to understand: is the 149-digit number from:
# A. The a-i,o run in salphaseion-textarea.txt at position 0-90 (91 chars)?
# B. Somewhere in phase3.2-plaintext.bin bytes 1990-2138?

# Let me also look at STEPS.md more carefully for the checkerboard digits
with open(os.path.join(BASE_DIR, 'STEPS.md'), 'r') as f:
    steps = f.read()

print("\n" + "="*70)
print("Searching STEPS.md for checkerboard and 149")
print("="*70)

import re
for m in re.finditer(r'.{0,100}(149|checkerboard|straddling).{0,100}', steps, re.IGNORECASE):
    print(f"\n  {m.group(0)}")

# Let me manually parse section 3a and 3b
print("\n" + "="*70)
print("Analyzing Phase 3.2 sections 0-446 properly")
print("="*70)

section_3a = phase32[0:127].decode('latin-1')
section_3b = phase32[127:447]

print(f"\nSection 3a (0-126): {len(section_3a)} chars")
print(f"Content:\n{section_3a}")

print(f"\nSection 3b (127-446): {len(section_3b)} bytes")
print(f"First 50 hex: {section_3b[:50].hex()}")

# Per earlier discovery: section 3b is 64 squares x 5 bytes = 320 bytes
# Format: byte 0 = piece letter, bytes 1-4 = little-endian number -> convert to 4 ASCII

def decode_3b_square(b5):
    """Decode 5 bytes: char + LE32 4-char"""
    piece = chr(b5[0])
    num = int.from_bytes(b5[1:5], 'little', signed=True)
    if num < 0:
        num = num + 2**32
    # Extract MSB to LSB
    c4 = chr((num >> 24) & 0xFF)
    c3 = chr((num >> 16) & 0xFF)
    c2 = chr((num >> 8) & 0xFF)
    c1 = chr(num & 0xFF)
    return piece, c4, c3, c2, c1  # Return as a tuple

section_3b_decoded_chars = []
for i in range(0, 320, 5):
    square = section_3b[i:i+5]
    if len(square) == 5:
        piece, c4, c3, c2, c1 = decode_3b_square(square)
        section_3b_decoded_chars.append(piece)
        section_3b_decoded_chars.append(c4)
        section_3b_decoded_chars.append(c3)
        section_3b_decoded_chars.append(c2)
        section_3b_decoded_chars.append(c1)

section_3b_full = ''.join(section_3b_decoded_chars)
print(f"\nSection 3b fully decoded: {len(section_3b_full)} chars")
print(f"First 200: {section_3b_full[:200]}")
print(f"\nLast 200: {section_3b_full[-200:]}")

# Look for "matrix" and "sum" patterns
# Also: what if the "chess values" are actually ASCII?
# Let me try reading the 5-byte squares DIFFERENTLY:
# What if bytes 1-4 are just 4 ASCII chars, not packed?

print("\n" + "="*70)
print("Alternative: what if section 3b is just ASCII?")
print("="*70)

# What if the "packed LE32" interpretation was wrong?
# What if it's just: [piece][char][char][char][char] ?

alt_3b = []
for i in range(0, 320, 5):
    # piece = chr(section_3b[i])
    # c1 = chr(section_3b[i+1])
    # c2 = chr(section_3b[i+2])
    # c3 = chr(section_3b[i+3])
    # c4 = chr(section_3b[i+4])
    alt_3b.append(section_3b[i:i+5].decode('latin-1'))

alt_3b_full = ''.join(alt_3b)
print(f"\nDirect ASCII: first 200 chars:")
for i in range(0, 200, 40):
    print(f"  {alt_3b_full[i:i+40]}")

# Count how many are printable
printable = sum(1 for c in alt_3b_full if 32 <= ord(c) < 127)
print(f"\nPrintable ratio: {printable}/{len(alt_3b_full)} = {printable/len(alt_3b_full):.1%}")

# Try to find some known text
for pattern in ['matrix', 'list', 'sum', 'half', 'better', 'password']:
    if pattern in alt_3b_full.lower():
        idx = alt_3b_full.lower().find(pattern)
        print(f"\nFound '{pattern}' at position {idx}")
        context = alt_3b_full[max(0,idx-20):idx+len(pattern)+20]
        print(f"  Context: {repr(context)}")

print("\n" + "="*70)
print("Now trying: checkerboard digits SUM")
print("="*70)

# The checkerboard has 149 digits. Let's get the CORRECT 149 digits.
# From STEPS.md step 4b: it's a straddling checkerboard.
# But also from earlier: salphaseion-textarea.txt pos 0-90 is a 91-char a-i run.

def a_i_o_to_digit(c):
    if c == 'o':
        return 0
    return ord(c) - ord('a') + 1

# Read the first 91 chars of sp textarea
run1 = sp_textarea[0:91]
run1_digits = ''.join(str(a_i_o_to_digit(c)) for c in run1)
print(f"\nRun 1 (pos 0-90, 91 chars a-i): {len(run1_digits)} digits")
print(f"Digits: {run1_digits}")
print(f"Length: {len(run1_digits)}")

# Sum the digits
sum_run1 = sum(int(d) for d in run1_digits)
print(f"Digit sum: {sum_run1}")

# If that's 91 chars, each a-i gives exactly 1 digit (1-9, no zeros).
# So that's 91 digits. Not 149.

# Run 4 is pos 766-828: 63 chars a-i,o -> gave "lastwordsbeforearchichoice"
# Run 5 is pos 830-858: 29 chars a-i,o -> gave "thispassword"

# The 149 digits should come from the straddling checkerboard in Phase 3.2.
# STEPS.md says bytes 1990-2138 is the checkerboard.

# Let me look at that:
checkerboard_bytes = phase32[1990:2139]
print(f"\nPhase 3.2 checkerboard bytes 1990-2138: {len(checkerboard_bytes)} bytes")
print(f"Content: {checkerboard_bytes}")

# Are these ASCII digits?
ascii_digits = checkerboard_bytes.decode('latin-1')
print(f"As ASCII: {ascii_digits}")
print(f"Length: {len(ascii_digits)}")

if ascii_digits.isdigit():
    print(f"  THIS IS THE 149 DIGITS!")
    checkerboard_149 = ascii_digits

    # Compute its properties
    sum_cb = sum(int(d) for d in checkerboard_149)
    print(f"\nCheckerboard 149 digits:")
    print(f"  {checkerboard_149}")
    print(f"\n  Digit count: {len(checkerboard_149)}")
    print(f"  Digit sum: {sum_cb}")
    
    # Now try these as candidates
    candidates = []
    
    # The sum itself
    candidates.append(("cb_digit_sum", str(sum_cb)))
    
    # The full 149 digits
    candidates.append(("cb_full_149", checkerboard_149))
    
    # First N digits
    for n in [4, 8, 16, 32, 48, 64, 128, 149]:
        candidates.append((f"cb_first_{n}", checkerboard_149[:n]))
    
    # Last N digits
    for n in [4, 8, 16, 32, 48, 64]:
        candidates.append((f"cb_last_{n}", checkerboard_149[-n:]))
    
    # Try it as hex (2 digits per byte)
    if len(checkerboard_149) % 2 == 0:
        try:
            cb_bytes = bytes.fromhex(''.join(format(int(checkerboard_149[i:i+2]), '02x') 
                                       for i in range(0, 148, 2)))
            print(f"\nCheckerboard first 148 digits as hex: {cb_bytes[:50].hex()}...")
            candidates.append(("cb_ascii_decode", cb_bytes.decode('latin-1')))
        except:
            pass
    
    # Try with dropped digit (149 is odd)
    # Drop first
    try:
        drop1 = bytes.fromhex(''.join(format(int(checkerboard_149[i:i+2]), '02x') 
                                        for i in range(1, 149, 2)))
        candidates.append(("cb_drop1_decode", drop1.decode('latin-1')))
    except:
        pass
    
    # Drop last
    try:
        droplast = bytes.fromhex(''.join(format(int(checkerboard_149[i:i+2]), '02x') 
                                           for i in range(0, 148, 2)))
        candidates.append(("cb_droplast_decode", droplast.decode('latin-1')))
    except:
        pass

    # Also: "four first hint" -> take first 4 digits, or take first hint four times?
    first_4 = checkerboard_149[:4]
    candidates.append(("cb_first_4", first_4))
    candidates.append(("cb_first_4_four_times", first_4 * 4))
    
    # Try "sum" more broadly: XOR of all bytes
    # Or maybe the 149 digits SHA256 is the key?
    # Actually the password convention is: password = sha256(answer).hexdigest()
    # So answer could be the 149 digits, and password is its hash
    
    print(f"\nGenerated {len(candidates)} candidates from checkerboard. Testing...")
    
    for label, ans in candidates:
        for cname, cdata in containers:
            success, dec, ratio = try_decrypt(cdata, ans)
            if success:
                print(f"\n{'='*70}")
                print(f"SUCCESS: {label} on {cname}")
                print(f"  Answer: {repr(ans[:100])}...")
                print(f"  Decrypted: {len(dec)} bytes, {ratio:.1%} printable")
                if dec.startswith(b'Salted__'):
                    print(f"  --> NESTED! Inner salt: {dec[8:16].hex()}")
                print(f"  First 80 hex: {dec[:80].hex()}")

print("\nDone.")
