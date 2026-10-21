#!/usr/bin/env python3
"""
Find 'enter' and analyze:

The 4 instructions decoded:
1. matrixsumlist (104 chars a,b binary at 91-194)
2. lastwordsbeforearchichoice (63 chars a-i,o at 766-828)
3. thispassword (29 chars a-i,o at 830-858)
4. enter (40 chars a,b binary - WHERE?)

Also: what does "thispassword" POINT TO?
- 'lastwordsbeforearchichoice' -> literally points to text BEFORE the architect
- 'thispassword' -> literally means "what follows THIS [position] is the password"

Let me examine the structure after z at position 859.
"""

import os
import base64
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ab_binary_to_text(s):
    bits = []
    for c in s:
        if c == 'a':
            bits.append('0')
        elif c == 'b':
            bits.append('1')
    result = []
    for i in range(0, len(bits), 8):
        byte_bits = ''.join(bits[i:i+8])
        if len(byte_bits) == 8:
            result.append(chr(int(byte_bits, 2)))
    return ''.join(result)

with open(os.path.join(BASE_DIR, 'files', 'salphaseion-textarea.txt'), 'r') as f:
    content = f.read()

print("="*70)
print("Analyzing: z at 859, then WHAT COMES NEXT?")
print("="*70)

# After z at 859:
# - text: shabefourfirsthintisyourlastcommand
# - first base64: 64 chars (SalPhaseIon short container)
# - THEN: z separator at 958?
# - THEN: a,b run for 'enter' (40 chars = 5 bytes decoded = 5 letters 'enter')
# - THEN: second base64 (64 chars)
# - THEN: shabefanstoo

# Let's just look at positions 860-1075
print(f"\nPositions 860-1000:")
print(f"  {repr(content[860:1000])}")

# Find all 'z's
z_positions = [i for i, c in enumerate(content) if c == 'z']
print(f"\nAll z positions: {z_positions}")

# z at 765, 829, 859
# Is there a z at 958?
print(f"\nCharacter at position 958: '{content[958]}'")

# Let's read STEPS.md for the exact structure
with open(os.path.join(BASE_DIR, 'STEPS.md'), 'r') as f:
    steps = f.read()

# Search for SalPhaseIon structure
print("\n" + "="*70)
print("SalPhaseIon structure from STEPS.md")
print("="*70)

# Find relevant section
idx = steps.find('SalPhaseIon')
if idx >= 0:
    section = steps[idx:idx+3000]
    print(section[:2000])

# Actually, let me find the exact positions
print("\n" + "="*70)
print("Finding 'enter' decode (a,b binary, 40 chars = 5 bytes)")
print("="*70)

# 'enter' is 5 chars
# 5 chars * 8 bits = 40 bits
# 40 bits from a,b = 40 characters of 'a' or 'b'

# Let's search the text for any a,b runs of length 40 after pos 859
after_859 = content[860:]

# Find all runs of 'ab' chars
import re
matches = list(re.finditer(r'[ab]{8,}', after_859))
print(f"\nFound {len(matches)} runs of a/b (length >= 8) after position 859:")
for m in matches:
    start = 860 + m.start()
    end = 860 + m.end()
    text = content[start:end]
    print(f"\n  Position {start}-{end-1} (length {len(text)}):")
    print(f"    First 40 chars: {text[:40]}")
    print(f"    Length: {len(text)}")
    if len(text) == 40:
        decoded = ab_binary_to_text(text)
        print(f"    Perfect! 40 chars (5 bytes) -> decoded: '{decoded}'")
    elif len(text) > 40:
        # Try first 40
        first40 = text[:40]
        dec = ab_binary_to_text(first40)
        print(f"    First 40 chars decoded: '{dec}'")

# Now let's find the two base64 blocks
print("\n" + "="*70)
print("Finding the TWO base64 blocks (64 chars each)")
print("="*70)

# Looking for: base64 pattern of length 64
# After 'fourfirsthint...' should be: base64_1 (64), then a,b (40), then base64_2 (64)

# Let's find where base64 blocks are by looking for uppercase starts
# Actually we know 'U2FsdGVkX18' is the marker

salted_marker = 'U2FsdGVkX18'
idx1 = content.find(salted_marker)
print(f"\nFirst Salted__ base64 at position {idx1}")

# Extract it (should be 64 chars)
b64_1 = content[idx1:idx1+64]
print(f"  First 64 chars: {b64_1}")
dec_1 = base64.b64decode(b64_1)
print(f"  Decoded: {len(dec_1)} bytes, starts with {dec_1[:8]}, salt={dec_1[8:16].hex()}")

# Now find what comes AFTER this 64 chars
# Then there should be a 'z'? Then 40 chars a,b? Then second base64?

pos_after_b64_1 = idx1 + 64
print(f"\nRight after first base64 (pos {pos_after_b64_1}):")
print(f"  Next 60 chars: {repr(content[pos_after_b64_1:pos_after_b64_1+60])}")

# Find second base64 - look for patterns of base64 that is NOT starting with U2FsdGVk
# Should be at position where first base64 + separator + a,b run ends

# Let's just scan forward from pos_after_b64_1 looking for when base64-like starts again
# Actually the second base64 is shorter if it encodes 48 bytes
# 48 bytes * 4/3 = 64 chars exactly (no padding)

# Let's look for position where the pattern shifts to mixed-case+digits+/=
# But actually let me just check from position 959 onwards
print(f"\nPosition 959 onwards (looking for second base64 and 'enter'):")
print(f"  {repr(content[959:1030])}")

# Let me try: the content at 959 is the a,b run for 'enter' (40 chars)
# Then second base64 starts at 959+40=999
# 'shabefanstoo' starts at 999+64=1063

# Check the end: last 20 chars
print(f"\nLast 30 chars of file: {repr(content[-30:])}")
print(f"Length of file: {len(content)}")

# So:
# End at position 1074 (0-indexed)
# 'shabefanstoo' is 12 chars
# So it starts at 1075-12 = 1063

# Second base64: 64 chars, ends at 1062
# So second base64 = 1062-63 = 999 to 1062 (inclusive), 64 chars

# Then a,b run for 'enter' = 40 chars before that
# So 'enter' a,b = 999-40 = 959 to 998 (inclusive), 40 chars

print(f"\n" + "="*70)
print("Exact calculation:")
print("="*70)
print(f"  File ends at pos {len(content)-1}")
print(f"  'shabefanstoo' (12 chars) at end: pos {len(content)-12} to {len(content)-1}")
print(f"  Second base64 (64 chars): pos {len(content)-12-64} to {len(content)-13}")

b64_2_start = len(content) - 12 - 64
b64_2_end = len(content) - 13
print(f"\n  Second base64: {b64_2_start} to {b64_2_end}")

b64_2 = content[b64_2_start:b64_2_end+1]
print(f"  Second base64 content: '{b64_2}'")
print(f"  Length: {len(b64_2)} chars")

dec_2 = base64.b64decode(b64_2)
print(f"  Decoded: {len(dec_2)} bytes")
print(f"  Hex: {dec_2.hex()}")
print(f"  Is 48 bytes (32 key + 16 IV)? {len(dec_2) == 48}")

# 'enter' should be 40 chars before second base64
enter_start = b64_2_start - 40
enter_end = b64_2_start - 1
print(f"\n  'enter' a,b run: {enter_start} to {enter_end}")

enter_ab = content[enter_start:enter_end+1]
print(f"  Enter a,b content: '{enter_ab}'")
print(f"  Length: {len(enter_ab)} chars")

if len(enter_ab) == 40:
    enter_decoded = ab_binary_to_text(enter_ab)
    print(f"  Decoded: '{enter_decoded}'")
    print(f"  Match 'enter': {enter_decoded == 'enter'}")

print(f"\n" + "="*70)
print("Full structure verified:")
print("="*70)
print("""
  Pos 0-90:      91 chars  a-b,i etc? (decoded earlier record [kit])
  Pos 91-194:    104 chars a,b binary  -> 'matrixsumlist' ✓
  Pos 195-764:   570 chars a-i only    -> [kit] NEVER DECODED
  Pos 765:       1 char    z            -> separator
  Pos 766-828:   63 chars  a-i,o        -> 'lastwordsbeforearchichoice' ✓
  Pos 829:       1 char    z            -> separator
  Pos 830-858:   29 chars  a-i,o        -> 'thispassword' ✓
  Pos 859:       1 char    z            -> separator
  Pos 860-894:   35 chars  ASCII text   -> 'shabefourfirsthintisyourlastcommand'
  Pos 895-958:   64 chars  base64       -> SalPhaseIon short container (Salted__)
  Pos 959-998:   40 chars  a,b binary   -> 'enter' (need to verify)
  Pos 999-1062:  64 chars  base64       -> 48 raw bytes = AES key + IV (NOT Salted__)
  Pos 1063-1074: 12 chars  ASCII text   -> 'shabefanstoo'
""")

# Now the key question: what does "thispassword" mean?
# - It's decoded RIGHT BEFORE the actual content
# - Content after z at 859: the two base64 blocks + text clues
#
# "lastwordsbeforearchichoice" was a LOCATION pointer
# "thispassword" probably means: use "this" (the following section) as password material

# But also: "fourfirsthintisyourlastcommand"
# - We have FOUR decoded hints/instructions
# - The FIRST of them is: matrixsumlist
# - Or "four first" = take first 4 something?

print(f"\n" + "="*70)
print("Critical connection: 'lastwordsbeforearchichoice' was LITERAL")
print("="*70)
print("""
  It POINTED to a LOCATION: bytes 0-446 of Phase 3.2
  Specifically: text BEFORE the architect section

  So the other instructions are also POINTERS, not direct values:
  
  1. 'matrixsumlist' -> WHAT location/action?
     - 'matrix' could be: 570-char a-i run? checkerboard? chess board?
     - 'sum' could be: take sum of something
     - 'list' could be: interpret as a list

  2. 'lastwordsbeforearchichoice' -> DONE: points to Phase 3.2 bytes 0-446

  3. 'thispassword' -> WHAT location?
     - 'this' could mean: this SalPhaseIon section itself?
     - Or: the text immediately FOLLOWING this instruction?

  4. 'enter' -> WHAT action?
     - Append newline character?
     - Or: go to the "enter" point somewhere?

Also:
  - "shabefourfirsthintisyourlastcommand"
  - "shabefanstoo"
  These both start with "shabe" - looks like padding/alignment.
""")

print("\nDone.")
