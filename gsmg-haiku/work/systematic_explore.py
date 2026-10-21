#!/usr/bin/env python3
"""
GSMG Puzzle - Systematically explore the clues

Key observations:
1. SalPhaseIon has decoded words that are INSTRUCTIONS:
   - matrixsumlist = sum elements of a matrix/list
   - lastwordsbeforearchichoice = what are last words before "archi choice"?
   - thispassword = this [next thing] is the password
   - enter = press enter, or use as suffix/prefix

2. The text hint: "fourfirsthintisyourlastcommand"
   - "four first" = of the four decoded, take the first (matrixsumlist)?
   - "your last command" = Phase 3.2 answer?

3. "7 intertwined passwords" - architect says this

4. "HALF and BETTERHALF" - checkerboard says TWO KEYS

5. UNUSED blocks: 91 chars and 570 chars of a-i only
   - These can't be decoded via a,b or a-i,o methods
   - Maybe they're numeric sequences directly?
   - a=1, b=2, c=3, ... i=9 (and nothing for 0)?

Let me explore these.
"""

import hashlib
import sys
import os

# Add parent path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from openssl_decrypt import decrypt_container

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_file(path):
    with open(path, 'r') as f:
        return f.read().strip()

# Read the SalPhaseIon textarea
content = read_file(os.path.join(BASE_DIR, 'files', 'salphaseion-textarea.txt'))

# The runs we care about:
runs = {
    'unused_0_90': content[0:91],        # 91 chars, a-i only
    'matrixsumlist': content[91:195],      # 104 chars, a,b -> "matrixsumlist"
    'unused_195_764': content[195:765],   # 570 chars, a-i only
    'lastwords': content[766:829],          # 63 chars, a-i,o -> "lastwordsbeforearchichoice"
    'thispassword': content[830:859],       # 29 chars, a-i,o -> "thispassword"
    'shabe_hint': content[860:895],         # "shabefourfirsthintisyourlastcommand"
    'enter': content[959:999],               # 40 chars, a,b -> "enter"
}

print("="*70)
print("1. Exploring: a-i only runs as numeric sequences")
print("="*70)

# Try a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9
def a_i_to_digits(s):
    """a=1, b=2, ..., i=9"""
    mapping = {chr(ord('a') + i): str(i+1) for i in range(9)}
    return ''.join(mapping.get(c, '?') for c in s)

def digits_to_bytes_hex(digits):
    """Convert a decimal number string to hex bytes"""
    try:
        val = int(digits)
        hex_str = format(val, 'x')
        if len(hex_str) % 2 != 0:
            hex_str = '0' + hex_str
        return hex_str, bytes.fromhex(hex_str)
    except:
        return None, None

unused_91_digits = a_i_to_digits(runs['unused_0_90'])
unused_570_digits = a_i_to_digits(runs['unused_195_764'])

print(f"\nFirst unused block (91 chars a-i):")
print(f"  As digits (a=1..i=9): {len(unused_91_digits)} digits")
print(f"  First 100 digits: {unused_91_digits[:100]}...")

print(f"\nSecond unused block (570 chars a-i):")
print(f"  As digits (a=1..i=9): {len(unused_570_digits)} digits")
print(f"  First 200 digits: {unused_570_digits[:200]}...")

# Check these as potential private keys (or parts of them)
# A secp256k1 private key is 32 bytes = 64 hex chars = up to 78 decimal digits
# 570 chars → 570 decimal digits = ~1893 bits (way too big)
# But wait - "matrixsumlist" maybe we need to SUM digits?

def sum_digits_mod_n(digits, n):
    """Sum all digits mod n"""
    total = sum(int(d) for d in digits if d.isdigit())
    return total, total % n

print(f"\n--- Sums ---")
sum_91, _ = sum_digits_mod_n(unused_91_digits, 1000000)
sum_570, _ = sum_digits_mod_n(unused_570_digits, 1000000)
print(f"Sum of digits in 91-block: {sum_91}")
print(f"Sum of digits in 570-block: {sum_570}")
print(f"Combined sum: {sum_91 + sum_570}")

# Actually let me check the length. Maybe the a-i only is representing base9?
# a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7, i=8 (base9)
def base9_to_decimal(s):
    """a=0, b=1, ..., i=8 (base9)"""
    mapping = {chr(ord('a') + i): i for i in range(9)}
    val = 0
    for c in s:
        val = val * 9 + mapping.get(c, 0)
    return val

print("\n" + "="*70)
print("2. Checking the LITERAL hint: 'fourfirsthintisyourlastcommand'")
print("="*70)

# Four decoded words in the SalPhaseIon FIRST section:
# (1) matrixsumlist
# (2) lastwordsbeforearchichoice
# (3) thispassword
# (4) enter
print(f"\nThe FOUR decoded hints are:")
four_hints = ['matrixsumlist', 'lastwordsbeforearchichoice', 'thispassword', 'enter']
for i, h in enumerate(four_hints, 1):
    print(f"  {i}. {h}")

# "four first hint" - could mean:
# - the first OF the four (matrixsumlist)
# - OR take first char of each four: m, l, t, e → "mlte"
# - OR "four first" = four letters of something?

# "is your last command" - our last solved answer was Phase 3.2:
phase32_answer = "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"

# But wait - also, the "last command" could be literally "enter" (the last decoded)

print("\n" + "="*70)
print("3. Re-examining: 'lastwordsbeforearchichoice'")
print("="*70)

# The DECODED output is literally "lastwordsbeforearchichoice"
# Let's split it: "last words before archi choice"

# What comes BEFORE "archi" related things?
# In the SalPhaseIon page ORDER:
#   - lastwordsbeforearchichoice (766-828)
#   - thispassword (830-858)
#   - shabe hint (860-894)
#   - SalPhaseIon short container
#   - enter (959-998)
#   - Cosmic Duality

# But the "archi" text is in Phase 3.2 output. So we're looking for words
# that are LITERALLY before the architect text or architect-related choice.

# Let me look at what precedes the architect text (which is 447-1985 in phase3.2 bin)

with open(os.path.join(BASE_DIR, 'derived', 'phase3.2-plaintext.bin'), 'rb') as f:
    phase32_bin = f.read()

# STEPS.md says:
# bytes 0-126: ??? (step 3a - what was it?)
# bytes 127-446: chess board positions (step 3b)
# bytes 447-1985: architect text (1539 letters)

print(f"\nPhase 3.2 decoded binary: {len(phase32_bin)} bytes")

# Let me decode bytes 0-126 and 127-446
def bytes_to_text(b):
    return ''.join(chr(x) if 32 <= x < 127 else f'\\x{x:02x}' for x in b)

print(f"\nBytes 0-126 ({len(phase32_bin[0:127])} bytes):")
print(f"  As text: {bytes_to_text(phase32_bin[0:127])}")

# Maybe bytes 0-126 decode to something using ASCII?
# Or maybe 0-126 is the board piece letters?

print("\n" + "="*70)
print("4. Looking at checkerboard: HALF and BETTERHALF")
print("="*70)

checkerboard_plain = read_file(os.path.join(BASE_DIR, 'derived', 'checkerboard-plaintext.txt'))
checkerboard_digits = read_file(os.path.join(BASE_DIR, 'derived', 'checkerboard-digits.txt'))

print(f"Checkerboard plaintext: {checkerboard_plain}")

# It says: "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"
# With spaces: "IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTERHALF AND THEY ALSO NEED FUNDS TO LIVE"

# Observations:
# - "KEYS" (plural) - so there might be TWO private keys
# - "HALF" and "BETTERHALF"

# Now the 149 digits. If there are TWO keys, maybe we split the 149 digits?
# But 149 is prime... but maybe the split is at certain POSITIONS based on content?

# Actually let me look at how the checkerboard encoding works.
# Straddling checkerboard: some chars are 1 digit (row 0), others are 2 digits (row 1 or 4 prefix)

print(f"\nCheckerboard digits length: {len(checkerboard_digits)} = 149 digits (prime)")

# Let me verify that it decodes correctly to the known plaintext
# Using the mapping from STEPS.md:
# Row 0 (single digit): 0=F, 2=U, 3=B, 5=C, 6=D, 7=O, 8=R, 9=A
# Row 1 (prefix '1'): 0=., 1=L, 2=E, 3=T, 4=H, 5=I, 6=N, 7=G, 8=K, 9=Y  
# Row 4 (prefix '4'): 0=M, 1=V, 2=P, 3=S, 4=/, 5=J, 6=Q, 7=Z, 8=X, 9=W

row0 = {'0':'F','2':'U','3':'B','5':'C','6':'D','7':'O','8':'R','9':'A'}
row1 = {'0':'.','1':'L','2':'E','3':'T','4':'H','5':'I','6':'N','7':'G','8':'K','9':'Y'}
row4 = {'0':'M','1':'V','2':'P','3':'S','4':'/','5':'J','6':'Q','7':'Z','8':'X','9':'W'}

def decode_checkerboard(digits_str):
    result = []
    i = 0
    while i < len(digits_str):
        d = digits_str[i]
        if d == '1':
            # row 1
            if i+1 < len(digits_str):
                result.append(row1.get(digits_str[i+1], '?'))
                i += 2
            else:
                i += 1
        elif d == '4':
            # row 4
            if i+1 < len(digits_str):
                result.append(row4.get(digits_str[i+1], '?'))
                i += 2
            else:
                i += 1
        else:
            # row 0
            result.append(row0.get(d, '?'))
            i += 1
    return ''.join(result)

decoded = decode_checkerboard(checkerboard_digits)
print(f"\nVerify checkerboard decode:")
print(f"  Expected: {checkerboard_plain}")
print(f"  Got:      {decoded}")
print(f"  Match: {decoded == checkerboard_plain}")

# Now - what if the digits themselves ARE the key? Just SHA256 them?
# Or what if we find where "HALF" and "BETTERHALF" are encoded?

print("\nLet's find the digit positions for HALF and BETTERHALF in the encoding:")
for word in ['HALF', 'BETTERHALF']:
    print(f"\n  '{word}':")
    pos = decoded.find(word)
    print(f"    Position in decoded text: {pos}")
    # Now find the corresponding digit position
    # This requires counting how many digits were consumed to reach position 'pos'

# Actually let me just try a new theory:
# What if "matrixsumlist" is telling us to take the CHESS VALUES (queen=9, rook=5, etc.)
# from the chess positions and sum them?

# Let me look at the chess positions from phase3.2-plaintext.bin bytes 127-446
print("\n" + "="*70)
print("5. Chess positions (bytes 127-446 in phase 3.2 output)")
print("="*70)

chess_bytes = phase32_bin[127:447]
print(f"Chess section: {len(chess_bytes)} bytes (expected 320)")

# STEPS.md says:
# 64 squares × 5 bytes = 320 bytes. That's exactly 446-127+1 = 320 bytes.

# Format per square (5 bytes):
# byte 0: piece (ASCII letter: KQRBNP, kqrbnp, or '.' for empty)
# bytes 1-4: value in cents as 4-byte little-endian

# Let me parse this properly
pieces = []
values_cents = []
for i in range(0, len(chess_bytes), 5):
    piece = chr(chess_bytes[i])
    value = int.from_bytes(chess_bytes[i+1:i+5], 'little', signed=True)
    pieces.append(piece)
    values_cents.append(value)

# Print the board in 8x8
print("\nChess board layout:")
for rank in range(8):
    row = pieces[rank*8:(rank+1)*8]
    print(f"  Rank {8-rank}: {''.join(row)}")

# Now sum the non-zero values
sum_cents = sum(values_cents)
print(f"\nSum of all piece values in cents: {sum_cents}")
print(f"  As integer: {sum_cents}")
print(f"  As string: {str(sum_cents)}")

# Also count by color
white_sum = sum(v for p, v in zip(pieces, values_cents) if p.isupper() and p != '.')
black_sum = sum(v for p, v in zip(pieces, values_cents) if p.islower() and p != '.')
print(f"\nWhite pieces sum: {white_sum}")
print(f"Black pieces sum: {black_sum}")

# These look like potential answer strings!
candidates_from_chess = [
    (f"chess_sum_{sum_cents}", str(sum_cents)),
    (f"chess_white_{white_sum}", str(white_sum)),
    (f"chess_black_{black_sum}", str(black_sum)),
]

print("\n" + "="*70)
print("6. Testing candidates from our analysis")
print("="*70)

def try_candidate(label, answer_text):
    """Try answer text as password (sha256 hex lower) against all containers"""
    password = hashlib.sha256(answer_text.encode()).hexdigest().lower()
    
    containers = [
        ('terminal', os.path.join(BASE_DIR, 'files', 'terminal.b64')),
        ('salphaseion-short', os.path.join(BASE_DIR, 'files', 'salphaseion-short.b64')),
        ('cosmic-duality', os.path.join(BASE_DIR, 'files', 'cosmic-duality.b64')),
    ]
    
    results = []
    for name, path in containers:
        with open(path, 'r') as f:
            b64_data = f.read().strip()
        
        success, decrypted, printable = decrypt_container(b64_data, password, debug=False)
        if success:
            result = {
                'name': name,
                'decrypted': decrypted,
                'printable_ratio': printable
            }
            results.append(result)
            print(f"  *** SUCCESS with {label} on {name}! ***")
            print(f"      Answer text: {repr(answer_text[:100])}")
            print(f"      Password: {password}")
            print(f"      Printable: {printable:.1%}")
            print(f"      First 200 bytes: {repr(decrypted[:200])}")
    
    return results

# Try the chess sum values
all_results = []
for label, ans in candidates_from_chess:
    print(f"\nTrying: {label} = {ans}")
    results = try_candidate(label, ans)
    all_results.extend(results)

# Also try variations like concatenated
print("\n\nTrying chess sums concatenated...")
concatenated = str(sum_cents) + str(white_sum) + str(black_sum)
print(f"  Concatenated: {concatenated}")
try_candidate("chess_concat", concatenated)

# Also try: the four words in various patterns
four = ['matrixsumlist', 'lastwordsbeforearchichoice', 'thispassword', 'enter']
patterns = []

# "four first hint" - maybe interleave first letters?
first_chars = [w[0] for w in four]  # m, l, t, e
patterns.append(("four_first_chars", ''.join(first_chars)))
patterns.append(("four_first_chars_upper", ''.join(first_chars).upper()))

# "intertwined" - like the architect said: maybe alternate characters?
def interleave(*strings):
    result = []
    max_len = max(len(s) for s in strings)
    for i in range(max_len):
        for s in strings:
            if i < len(s):
                result.append(s[i])
    return ''.join(result)

interleaved_4 = interleave(*four)
patterns.append(("four_interleaved", interleaved_4))

print(f"\nTrying 4-word patterns...")
for label, ans in patterns:
    print(f"  {label}: {repr(ans[:80])}... (len={len(ans)})")
    try_candidate(label, ans)

# Also - what if "matrixsumlist" literally means:
# take the "matrix" (the chess board or checkerboard) and sum the "list" (values)
# We did chess values. What about the checkerboard-digits sum?

print(f"\n\nTrying checkerboard digits sum...")
cb_digit_sum = sum(int(d) for d in checkerboard_digits)
print(f"  Sum of checkerboard digits: {cb_digit_sum}")
try_candidate("checkerboard_digit_sum", str(cb_digit_sum))

# What about "CIAOBELLAO" or "GOODLUCK" from architect text?
for word in ['CIAOBELLAO', 'GOODLUCK', 'PRIMEBASICS', 'SOURCECODES', 
             'TWENTYTHREE', 'SIXTEEN', 'SEVEN']:
    try_candidate(f"architect_{word}", word)
    try_candidate(f"architect_{word}_lower", word.lower())

print("\n\n--- Analysis complete ---")
if not all_results:
    print("No successes with these candidates.")
else:
    print(f"\nFound {len(all_results)} successful decryptions!")
