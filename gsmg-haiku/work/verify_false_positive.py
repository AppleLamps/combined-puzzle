#!/usr/bin/env python3
"""
Check if SalPhaseIon short decryption is real or false positive.

False positives happen because PKCS#7 padding check passes randomly ~1/256 times.
A valid decryption should either:
1. Be meaningful text
2. Start with Salted__ (another encrypted container)
3. Have clear structure

Also try: the properly decoded section 3a + 3b as the answer.
"""

import os
import hashlib
import base64
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

def try_decrypt(data: bytes, password: str):
    """Returns (success_bool, plaintext_bytes, printable_ratio)"""
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

# Load all three containers
def load_b64(name):
    with open(os.path.join(BASE_DIR, 'files', name), 'r') as f:
        return name, base64.b64decode(''.join(f.read().split()))

containers = [
    load_b64('terminal.b64'),
    load_b64('salphaseion-short.b64'),
    load_b64('cosmic-duality.b64'),
]

# Read phase 3.2 binary
with open(os.path.join(BASE_DIR, 'derived', 'phase3.2-plaintext.bin'), 'rb') as f:
    phase32_bin = f.read()

section_3a_text = phase32_bin[0:127].decode('latin-1')  # Morpheus
section_3b_bytes = phase32_bin[127:447]  # "chess board"

print("="*70)
print("Test 1: bytes 0-446 (no LF) against ALL containers")
print("="*70)

before_archi_text = phase32_bin[0:447].decode('latin-1')
before_archi_no_lf = before_archi_text.replace('\n', '')

print(f"\nAnswer text: {len(before_archi_no_lf)} chars")
print(f"Password: sha256(answer).hexdigest().lower()")

password = hashlib.sha256(before_archi_no_lf.encode()).hexdigest().lower()
print(f"Password hex: {password}")

for name, data in containers:
    # First get salt info
    salt = data[8:16].hex()
    success, dec, ratio = try_decrypt(data, password)
    print(f"\n  {name}: salt={salt}")
    if success:
        print(f"    *** DECRYPTED: {len(dec)} bytes, {ratio:.1%} printable")
        if dec.startswith(b'Salted__'):
            print(f"    --> CONTAINS NESTED ENCRYPTED CONTAINER! Inner salt: {dec[8:16].hex()}")
        print(f"    First 32 hex: {dec[:32].hex()}")
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in dec[:50])
        print(f"    First 50 printable: {ascii_part}")
    else:
        print(f"    --> Failed (padding error, expected for wrong password)")

print("\n" + "="*70)
print("Test 2: Decode section 3b properly first (the 'chess' board)")
print("="*70)

# Earlier we discovered that bytes 127-446 are NOT chess but packed ASCII
# Format per 5-byte square:
#   byte 0 = 1 ASCII char (the "piece" letter)
#   bytes 1-4 = 4 ASCII chars packed as little-endian 32-bit value

def decode_chess_section(chess_bytes):
    """Decode the 320 bytes from 127-446"""
    result = []
    for i in range(0, 320, 5):
        piece_char = chr(chess_bytes[i])
        
        # bytes 1-4 as little-endian 32-bit signed int
        val = int.from_bytes(chess_bytes[i+1:i+5], 'little', signed=True)
        
        # Convert to unsigned
        if val < 0:
            val = val + 2**32
        
        # Extract 4 bytes from MSB to LSB
        b3 = (val >> 24) & 0xFF
        b2 = (val >> 16) & 0xFF
        b1 = (val >> 8) & 0xFF
        b0 = val & 0xFF
        
        four_chars = chr(b3) + chr(b2) + chr(b1) + chr(b0)
        
        result.append(piece_char)
        result.append(four_chars)
    
    return ''.join(result)

section_3b_decoded = decode_chess_section(section_3b_bytes)

print(f"\nSection 3b decoded as packed ASCII: {len(section_3b_decoded)} chars")
print(f"First 200 chars:")
print(section_3b_decoded[:200])
print(f"\nLast 200 chars:")
print(section_3b_decoded[-200:])

# Now build candidates using properly decoded data
print("\n" + "="*70)
print("Test 3: Try combinations of 3a and properly decoded 3b")
print("="*70)

candidates = [
    # Section 3a only, various line endings
    ("3a_original", section_3a_text),
    ("3a_no_cr", section_3a_text.replace('\r', '')),
    ("3a_no_lf", section_3a_text.replace('\n', '')),
    ("3a_no_crlf", section_3a_text.replace('\r', '').replace('\n', '')),
    ("3a_stripped", section_3a_text.strip()),
    
    # Section 3b properly decoded
    ("3b_decoded", section_3b_decoded),
    ("3b_first_200", section_3b_decoded[:200]),
    ("3b_last_200", section_3b_decoded[-200:]),
    
    # Combined 3a + 3b
    ("3a_then_3b", section_3a_text + section_3b_decoded),
    ("3a_nolf_then_3b", section_3a_text.replace('\n', '') + section_3b_decoded),
    
    # The "before archi" is 0-446 = 3a + 3b combined
    # But 3b needs the proper decoding
]

# Also try: the architect mentions "last words" - maybe the LAST sentence?
# 3a ends with: "One for one, four for one."
last_sentence_3a = "One for one, four for one"
candidates.append(("3a_last_sentence", last_sentence_3a))
candidates.append(("3a_last_sentence_nospace", "Oneforonefourforone"))
candidates.append(("3a_last_sentence_upper", "ONEFORONEFOURFORONE"))

# Try first letters from something
# "I've been waiting for you" first letters: Ibwfy
first_letters = ''.join(w[0] for w in "I've been waiting for you".split())
candidates.append(("3a_keywords_first", first_letters))

print(f"\nTrying {len(candidates)} candidates...")

for label, ans in candidates:
    pw = hashlib.sha256(ans.encode()).hexdigest().lower()
    
    successes = []
    for name, data in containers:
        success, dec, ratio = try_decrypt(data, pw)
        if success:
            successes.append((name, dec, ratio))
    
    if successes:
        print(f"\n{'='*70}")
        print(f"Candidate: {label}")
        print(f"Answer (truncated): {repr(ans[:100])}...")
        print(f"Password: {pw}")
        for name, dec, ratio in successes:
            print(f"\n  SUCCESS on {name}: {len(dec)} bytes, {ratio:.1%} printable")
            if dec.startswith(b'Salted__'):
                print(f"    --> NESTED CONTAINER! Inner salt: {dec[8:16].hex()}")
            print(f"    Hex first 32: {dec[:32].hex()}")
            ascii_p = ''.join(chr(b) if 32 <= b < 127 else '.' for b in dec[:60])
            print(f"    Printable view: {ascii_p}")

print("\n" + "="*70)
print("Test 4: Verify false positive by checking statistical probability")
print("="*70)
# SalPhaseIon short is 96 bytes total = 16 (header) + 80 (ciphertext)
# 80 bytes = 10 blocks of 8 bytes (AES block is actually 16 bytes)
# AES block size is 16 bytes, so 80 bytes = 5 blocks

print(f"\nSalPhaseIon short:")
sp_short_name, sp_short_data = load_b64('salphaseion-short.b64')
print(f"  Total: {len(sp_short_data)} bytes base64 decoded")
print(f"  Salt: {sp_short_data[8:16].hex()}")
print(f"  Ciphertext: {len(sp_short_data)-16} bytes = {(len(sp_short_data)-16)/16:.1f} AES blocks")

# Let's also check: what's the probability that decryption worked on ONLY ONE container?
# If this were the correct password, I'd expect it to work for Terminal too since
# the clue "lastwordsbeforearchichoice" came from SalPhaseIon but Terminal is
# also from Phase 3.2.

# Actually, let me double-check our earlier answer. Let me reproduce Phase 3.2 
# decryption with the known answer to verify our crypto is correct.

print("\n" + "="*70)
print("VERIFY: Check that our crypto works on Phase 3.2 with known answer")
print("="*70)

phase32_answer = "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
phase32_password = hashlib.sha256(phase32_answer.encode()).hexdigest().lower()
print(f"Known Phase 3.2 answer: {phase32_answer[:50]}...")
print(f"Password hex: {phase32_password}")

# Decrypt phase3.2.b64 to verify
with open(os.path.join(BASE_DIR, 'files', 'phase3.2.b64'), 'r') as f:
    phase32_enc = base64.b64decode(''.join(f.read().split()))

success, dec, ratio = try_decrypt(phase32_enc, phase32_password)
if success and len(dec) == 2422:
    print(f"\n  ✓ Correctly decrypted Phase 3.2: {len(dec)} bytes")
    print(f"  First 100 chars: {dec[:100].decode('latin-1')}")
else:
    print(f"  ✗ FAILED to decrypt Phase 3.2 - our crypto is broken!")
    print(f"  Success: {success}, len: {len(dec) if dec else 'None'}")

print("\nDone.")
