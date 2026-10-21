#!/usr/bin/env python3
"""
Key findings:
1. "four for one" appears at the END of the "last words before archi"
2. The 149 digits have REPEATED "1491109166" - 8-char overlap at positions 80 and 88
3. STEPS.md says: "18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc" + "part of the cipher"

Let's examine the SalPhaseIon a-i runs more carefully.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read salphaseion
with open(os.path.join(BASE_DIR, 'files', 'salphaseion-textarea.txt'), 'r') as f:
    sp = f.read()

# The decoded words were:
# Run 4 (pos 766-828): 63 chars a-i,o -> lastwordsbeforearchichoice
# Run 5 (pos 830-858): 29 chars a-i,o -> thispassword
# Run 6 (pos 860-946): 87 chars a-i,o -> matrixsumlist
# Run 7 (pos 948-973): 26 chars a-i,o -> enter

# Let me decode all of these properly
def a_i_o_to_digit(c):
    if c == 'o':
        return 0
    return ord(c) - ord('a') + 1

def decode_a_i_o_run(s):
    """Convert a-i,o (1-9,0) to digits, then interpret as per Phase 3.2"""
    digits = ''.join(str(a_i_o_to_digit(c)) for c in s)
    
    # As big integer -> hex -> ascii (like Phase 3.2)
    try:
        if not digits:
            return "", ""
        n = int(digits)
        h = hex(n)[2:]
        if len(h) % 2:
            h = '0' + h
        b = bytes.fromhex(h)
        ascii_try = b.decode('latin-1')
        return digits, ascii_try
    except:
        return digits, ""

# First let's find ALL the runs - search for [z] separators
print("="*70)
print("Finding all runs in salphaseion-textarea.txt")
print("="*70)

# The structure from STEPS.md:
# - pos 0-90: 91 chars a,b -> binary -> 12 bytes [kit]
# - pos 92-250: 159 chars a,b -> binary -> 20 bytes [kit]
# - pos 252-764: 513 chars a,b -> binary -> 64 bytes = first base64 block (SalPhaseIon short container)
# - pos 766-828: 63 chars a-i,o -> lastwordsbeforearchichoice
# - pos 830-858: 29 chars a-i,o -> thispassword
# - pos 860-946: 87 chars a-i,o -> matrixsumlist
# - pos 948-973: 26 chars a-i,o -> enter
# Then ASCII text, then base64 blocks

# Let me verify the decoding of these 4 runs
run4_chars = sp[766:829]  # 63 chars
run5_chars = sp[830:859]   # 29 chars
run6_chars = sp[860:947]    # 87 chars
run7_chars = sp[948:974]    # 26 chars

print(f"\nRun 4 (63 chars @766): {run4_chars}")
r4d, r4a = decode_a_i_o_run(run4_chars)
print(f"  Digits: {r4d}")
print(f"  As big-int hex->ascii: {repr(r4a)}")

print(f"\nRun 5 (29 chars @830): {run5_chars}")
r5d, r5a = decode_a_i_o_run(run5_chars)
print(f"  Digits: {r5d}")
print(f"  As big-int hex->ascii: {repr(r5a)}")

print(f"\nRun 6 (87 chars @860): {run6_chars}")
r6d, r6a = decode_a_i_o_run(run6_chars)
print(f"  Digits: {r6d}")
print(f"  As big-int hex->ascii: {repr(r6a)}")

print(f"\nRun 7 (26 chars @948): {run7_chars}")
r7d, r7a = decode_a_i_o_run(run7_chars)
print(f"  Digits: {r7d}")
print(f"  As big-int hex->ascii: {repr(r7a)}")

# But wait - this gives us the *raw decoded text*. The previous "decoded words"
# were: lastwordsbeforearchichoice, thispassword, matrixsumlist, enter
# Let me verify those are the correct interpretations

# Actually the decoding rule per STEPS.md:
# "Read digits left-to-right as one big integer. Convert to hexadecimal. Read hex as ASCII."

print(f"\n" + "="*70)
print("Four decoded instructions (in plain English):")
print("="*70)
print(f"  1. lastwordsbeforearchichoice")
print(f"  2. thispassword")
print(f"  3. matrixsumlist")
print(f"  4. enter")

print(f"\nInterpretations that make sense:")
print(f"  1. 'lastwordsbeforearchichoice' -> literally: text BEFORE the architect text")
print(f"     -> Phase 3.2 bytes 0-446 = found it, ends with 'One for one, four for one'")
print(f"")
print(f"  2. 'thispassword' -> what is 'this'? The password itself?")
print(f"")
print(f"  3. 'matrixsumlist' -> maybe:")
print(f"     - matrix = chess-like 8x8 section?")
print(f"     - matrix = the Matrix film references?")
print(f"     - sum of something from a list?")
print(f"")
print(f"  4. 'enter' -> suffix/prefix with newline?")

# Actually - WHAT IF "lastwordsbeforearchichoice" itself was too literal?
# What if it meant: take some words FROM the last part BEFORE the architect part?
# The last part says:
#   "One for one, four for one."
# What if "four for one" is the hint? And "four first hint is your last command"
# also confirms: the "last command" is "four for one"

print(f"\n" + "="*70)
print("Analyzing the 149 checkerboard digits for patterns")
print("="*70)

cb_digits = "15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112"

# Look for repeated substrings
print(f"\nDigits: {cb_digits}")
print(f"Length: {len(cb_digits)}")

print(f"\nLooking for repeated sequences of length >= 6:")
seen = {}  # seq -> first_position
found_repeats = []
for l in range(6, 20):
    for i in range(len(cb_digits) - l + 1):
        seq = cb_digits[i:i+l]
        if seq in seen:
            if (seen[seq], i, seq) not in found_repeats and (i, seen[seq], seq) not in found_repeats:
                found_repeats.append((seen[seq], i, seq))
        else:
            seen[seq] = i

for p1, p2, s in sorted(found_repeats, key=lambda x: len(x[2]), reverse=True):
    print(f"  '{s}' at positions {p1} and {p2} (length {len(s)})")

# "1491109166" appears twice with 8-char overlap
# Let's look at positions around 80-96
print(f"\n\nDetail at positions 70-100:")
print(f"  {cb_digits[70:100]}")
print(f"  Positions 70-99 (indices):")
for i in range(70, 100):
    print(f"    {i}: '{cb_digits[i]}'")

# "1491109166" at 80: indices 80-89
# "1491109166" at 88: indices 88-97
# Overlap at positions 88-89

# What does this mean? Could be:
# - Two copies of same block
# - An encoding of "HALF" and "BETTERHALF"
# - The checkerboard says: PRIVATE KEYS (plural) for HALF and BETTERHALF

print(f"\n" + "="*70)
print("What if '1491109166' decodes to something?")
print("="*70)

seq = "1491109166"
print(f"Sequence '{seq}' (10 digits):")

# Try as big int -> hex
n = int(seq)
h = hex(n)[2:]
print(f"  As integer -> hex: 0x{h}")
if len(h) % 2: h = '0' + h
b = bytes.fromhex(h)
print(f"  As bytes: {b} -> ascii: {repr(b.decode('latin-1'))}")

# What if we read the digits TWO at a time?
for i in range(0, len(seq), 2):
    pair = seq[i:i+2]
    print(f"    Pair {i}: '{pair}' -> int {int(pair)} -> ASCII {chr(int(pair)) if 32<=int(pair)<127 else '?'}")

# What about positions of capital letters in checkerboard plaintext?
# The plaintext was: "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"
# This says KEYS (plural) for HALF and BETTERHALF

print(f"\n" + "="*70)
print("149 digits - try using as direct SECP256K1 key?")
print("="*70)

# Actually I already tried this earlier - 149 digits is about 495 bits,
# way larger than 256-bit secp256k1 key.

# But wait - the 149 digits were on an OP_RETURN with "part of the cipher"
# And the checkerboard decoded to: HALF and BETTERHALF own the private KEYS

# Could "149" mean something? 149 is prime.
# What if: the 149 digits ENCODE two 256-bit keys? That would be 512 bits.
# 149 decimal digits is about ceil(149 * log10(2)) = 495 bits. Close to 512.

# Maybe there's a different interpretation.

# Actually let me look at the weird string from STEPS.md again:
# "18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc"

# That looks like base64. Let's try:
print(f"\n" + "="*70)
print("Trying that weird base64-like string from STEPS.md")
print("="*70)

import base64

# It has 44 chars. Base64?
weird = "18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc"
print(f"'{weird}'")
print(f"Length: {len(weird)}")

# Try base64 decode (need padding)
try:
    padded = weird + '=' * (4 - len(weird) % 4) if len(weird) % 4 else weird
    d = base64.b64decode(padded)
    print(f"Base64 decode: {d.hex()}")
    print(f"As ASCII: {repr(d.decode('latin-1'))}")
except Exception as e:
    print(f"Not valid base64: {e}")

# Could it be hex?
try:
    if all(c in '0123456789abcdefABCDEF' for c in weird):
        d2 = bytes.fromhex(weird)
        print(f"\nHex decode: {d2}")
except:
    pass

# 44 chars of base58? Let's see - it has 'I', 'l', 'O', '0'?
# Actually it doesn't: '1' appears but not 'I' or 'l'
# Let me check if it's a Bitcoin address format (no, starts with 1 but length?)

print(f"\nDone.")
