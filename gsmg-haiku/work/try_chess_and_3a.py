#!/usr/bin/env python3
"""
GSMG Puzzle - Try candidates with robust error handling

Key new insight:
- Checkerboard says "PRIVATE KEYS BELONG TO HALF AND BETTERHALF"
- Chess board has WHITE and BLACK pieces
- Maybe WHITE = HALF and BLACK = BETTERHALF?
- We have chess_white_sum and chess_black_sum

Let me also look at:
- Phase 3.2 bytes 0-126 (what was it?)
- Maybe it's the "last words before archi choice"?
"""

import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os
import struct

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ============== CORE DECRYPTION FUNCTIONS ==============

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
    """Try to decrypt; returns (success_bool, plaintext_or_None, printable_ratio)"""
    if not data.startswith(b'Salted__'):
        return False, None, 0.0
    
    salt = data[8:16]
    ciphertext = data[16:]
    
    try:
        key, iv = derive_key_and_iv(password, salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        
        # Calculate printable ratio (Phase 3.2 was ~59% printable)
        total = len(plaintext)
        if total == 0:
            printable_ratio = 1.0
        else:
            printable = sum(1 for b in plaintext if 32 <= b < 127 or b in (9, 10, 13))
            printable_ratio = printable / total
        
        return True, plaintext, printable_ratio
    except:
        # Bad padding or other error
        return False, None, 0.0

def try_answer_against_all(answer_text: str, label: str):
    """Try answer_text as password against all 3 containers."""
    password = hashlib.sha256(answer_text.encode()).hexdigest().lower()
    
    containers = [
        ('terminal', os.path.join(BASE_DIR, 'files', 'terminal.b64')),
        ('salphaseion-short', os.path.join(BASE_DIR, 'files', 'salphaseion-short.b64')),
        ('cosmic-duality', os.path.join(BASE_DIR, 'files', 'cosmic-duality.b64')),
    ]
    
    results = []
    for name, path in containers:
        with open(path, 'r') as f:
            b64 = ''.join(f.read().split())
        data = base64.b64decode(b64)
        
        success, decrypted, printable = try_decrypt(data, password)
        if success:
            results.append((name, decrypted, printable, answer_text, password))
            print(f"\n{'='*70}")
            print(f"SUCCESS: {label} on {name}")
            print(f"{'='*70}")
            print(f"Answer text: {repr(answer_text[:200])}")
            print(f"Password (sha256 hex): {password}")
            print(f"Printable ratio: {printable:.1%}")
            print(f"Length: {len(decrypted)} bytes")
            print(f"First 100 bytes: {repr(decrypted[:100])}")
            try:
                as_text = decrypted.decode('utf-8', errors='replace')
                print(f"As text (first 300 chars):\n{as_text[:300]}")
            except:
                pass
    
    return results

# ============== READ PHASE 3.2 BINARY ==============

with open(os.path.join(BASE_DIR, 'derived', 'phase3.2-plaintext.bin'), 'rb') as f:
    phase32_bin = f.read()

print(f"Phase 3.2 binary: {len(phase32_bin)} bytes total")

# STEPS.md says:
# - step 3a: bytes 0-126 (127 bytes) - ???
# - step 3b: bytes 127-446 (320 bytes) - chess board
# - step 4a: bytes 447-1985 (1539 bytes) - architect text

section_3a = phase32_bin[0:127]
section_3b_chess = phase32_bin[127:447]
section_4a_arch = phase32_bin[447:1986]

print(f"\nSection 3a (bytes 0-126): {len(section_3a)} bytes")
print(f"  Hex first 64: {section_3a[:64].hex()}")

# Try to interpret it. Is it binary data that decodes to something?
# Maybe it's a 32-byte key? Or maybe it's the "last words"?

# Let me check if it's ASCII or decodable
print(f"\nAs ASCII (printable only):")
as_ascii = ''.join(chr(b) if 32 <= b < 127 else '.' for b in section_3a)
print(f"  {as_ascii}")

# Check if it's little-endian values like the chess section?
print(f"\nAs 4-byte little-endian values (first 10):")
for i in range(0, min(120, len(section_3a)), 4):
    if i+4 <= len(section_3a):
        val = int.from_bytes(section_3a[i:i+4], 'little', signed=True)
        print(f"  [{i}]: {val}")

# ============== CHESS VALUES ==============
print("\n" + "="*70)
print("Chess board analysis")
print("="*70)

# Parse chess section (bytes 127-446 = 320 bytes)
# Format: byte 0 = piece char, bytes 1-4 = value (cents), 64 squares
pieces = []
values_cents = []
for i in range(0, 320, 5):
    piece = chr(section_3b_chess[i])
    value = int.from_bytes(section_3b_chess[i+1:i+5], 'little', signed=True)
    pieces.append(piece)
    values_cents.append(value)
    # print(f"  Square {i//5}: piece='{piece}', value={value}")

# Board layout
print("\nBoard:")
for rank in range(8):
    row = pieces[rank*8:(rank+1)*8]
    values_row = values_cents[rank*8:(rank+1)*8]
    print(f"  Rank {8-rank}: {''.join(row)}  (values: {values_row})")

# Calculate sums
all_sum = sum(values_cents)
white_sum = sum(v for p, v in zip(pieces, values_cents) if p.isupper() and p != '.')
black_sum = sum(v for p, v in zip(pieces, values_cents) if p.islower() and p != '.')

print(f"\nPiece value sums:")
print(f"  All pieces: {all_sum}")
print(f"  White (HALF?): {white_sum}")
print(f"  Black (BETTERHALF?): {black_sum}")

# ============== TRY CANDIDATES ==============
print("\n" + "="*70)
print("Trying candidates...")
print("="*70)

all_successes = []

# 1. Chess values as direct answers
candidates = [
    ("chess_all_sum", str(all_sum)),
    ("chess_white_half", str(white_sum)),
    ("chess_black_betterhalf", str(black_sum)),
]

# Also try both white and black concatenated (for a combined container?)
candidates.append(("white_then_black", str(white_sum) + str(black_sum)))
candidates.append(("black_then_white", str(black_sum) + str(white_sum)))

# 2. Section 3a interpretations
# What if section 3a is itself the "lastwords" or something to decode?
# Try: section 3a as hex string
s3a_hex = section_3a.hex()
candidates.append(("section3a_hex", s3a_hex))

# Try: if section 3a contains some key - sum its bytes?
s3a_byte_sum = sum(section_3a)
candidates.append(("section3a_byte_sum", str(s3a_byte_sum)))

# 3. Re-interpret "fourfirsthintisyourlastcommand"
# - "four" could be referring to Phase 3 having 4 parts?
# - "last command" = the last solved step? That was Phase 3.2

# But we used Phase 3.2 answer directly already.
# What if we use the PASSWORD of Phase 3.2 instead of the answer?
phase32_answer = "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
phase32_password = hashlib.sha256(phase32_answer.encode()).hexdigest().lower()
# Wait, password is sha256 hex, but we need answer text for another round.

# What about: "four first" = take first 4 chars from something?
# First 4 of phase32 answer: "jacq"
candidates.append(("phase32_first4", phase32_answer[:4]))
# First 4 of password: "250f"
candidates.append(("phase32_pass_first4", phase32_password[:4]))

# Actually, let me also try combinations that sound "Matrix"-like
# The decoded words from SalPhaseIon:
decoded_words = [
    "matrixsumlist",
    "lastwordsbeforearchichoice",
    "thispassword",
    "enter",
]

# The shabe hint decoded to something? Not working as direct.

# What about: the LITERAL "last words before archi choice"
# In the architect text, there is "CIAOBELLAO" at the end.
# What's before that? "GOODLUCKNEVERTHELESSIREALLYHOPEYOURETHEONECIAOBELLAO"

# Actually - "archi choice" - choice? We have Phase 2 mention "choice"!
# files/phase2_choice.html

# Let me try simple concatenations of the 4 decoded words in ALL orders
import itertools
print(f"\nTrying all {len(list(itertools.permutations(decoded_words)))} permutations of 4 decoded words...")
for perm in itertools.permutations(decoded_words):
    combined = ''.join(perm)
    candidates.append((f"perm_{'_'.join(perm[:2])}...", combined))

# Also try interleaved
def interleave(*strings):
    result = []
    max_len = max(len(s) for s in strings)
    for i in range(max_len):
        for s in strings:
            if i < len(s):
                result.append(s[i])
    return ''.join(result)

interleaved = interleave(*decoded_words)
candidates.append(("four_interleaved", interleaved))

print(f"\nTotal candidates: {len(candidates)}")

for label, ans in candidates:
    if len(ans) < 80:
        print(f"Trying: {label} = {repr(ans)}")
    else:
        print(f"Trying: {label} (len={len(ans)})")
    results = try_answer_against_all(ans, label)
    all_successes.extend(results)

# ============== ALSO ==============
# What if the 149 checkerboard digits are the key, but split at 74 and 75?
# (74 + 75 = 149)
# Or maybe 72 + 77?

with open(os.path.join(BASE_DIR, 'derived', 'checkerboard-digits.txt'), 'r') as f:
    cb_digits = f.read().strip()

print(f"\n\nTrying checkerboard digits splits...")
for split_at in range(70, 80):
    first = cb_digits[:split_at]
    second = cb_digits[split_at:]
    try_answer_against_all(first, f"cb_first_{split_at}")
    try_answer_against_all(second, f"cb_second_{split_at}")
    try_answer_against_all(first + second, f"cb_{split_at}_combined")

# What about the 149 digits interpreted as hex (but it has 0-9 only)?
# Not valid hex since there's no a-f.

print("\n\n" + "="*70)
if all_successes:
    print(f"FOUND {len(all_successes)} SUCCESSFUL DECRYPTIONS!")
    for name, dec, ratio, ans, pw in all_successes:
        print(f"\n--- {name} ---")
        print(f"  Answer: {repr(ans[:100])}")
        print(f"  Password: {pw}")
else:
    print("No successful decryptions with these candidates.")
print("="*70)
