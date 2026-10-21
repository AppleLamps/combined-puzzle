#!/usr/bin/env python3
"""
Critical findings:
- Run 6 (87 chars) actually contains: 'shabefourfirsthintisyourlastcommandU2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNs'
  - 'shabe' = maybe garbage/padding
  - 'fourfirsthintisyourlastcommand' = the clue!
  - 'U2FsdGVkX18...' = BASE64 starting with 'Salted__'

- Run 7 (26 chars): 'WVHefvdrd9zabbaabababbabbb'
  - 'WVHefvdrd9z' = ???
  - 'abbaabababbabbb' = looks like a,b binary?

Also, where are 'matrixsumlist' and 'enter'?

Let me decode the base64 and look for those missing words.
"""

import os
import base64
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read salphaseion full text
with open(os.path.join(BASE_DIR, 'files', 'salphaseion-textarea.txt'), 'r') as f:
    sp = f.read()

print("="*70)
print("Full textarea content - searching for key patterns")
print("="*70)

# Look for the four decoded words
for word in ['lastwordsbeforearchichoice', 'thispassword', 'matrixsumlist', 'enter', 'fourfirsthint']:
    if word in sp:
        print(f"'{word}' found at position {sp.find(word)}")
    else:
        print(f"'{word}' NOT found directly in textarea")

# The base64 "Salted__" marker
# base64 of "Salted__" is "U2FsdGVkX18"
salted_b64_marker = 'U2FsdGVkX18'
print(f"\nSearching for '{salted_b64_marker}' (Salted__ base64)...")
idx = sp.find(salted_b64_marker)
if idx >= 0:
    print(f"Found at position {idx}")
    
    # Extract everything from idx that looks like base64
    b64chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')
    b64_end = idx
    while b64_end < len(sp) and sp[b64_end] in b64chars:
        b64_end += 1
    
    extracted_b64 = sp[idx:b64_end]
    print(f"Extracted base64 block (length {len(extracted_b64)}):")
    print(f"  {extracted_b64}")
    
    # Decode it
    decoded = base64.b64decode(extracted_b64)
    print(f"\nDecoded (length {len(decoded)} bytes):")
    print(f"  First 16 bytes: {decoded[:16]}")
    print(f"  Hex: {decoded.hex()}")
    
    # Check if it's a known container
    print(f"\nComparing to known containers:")
    print(f"  Starts with Salted__: {decoded.startswith(b'Salted__')}")
    if decoded.startswith(b'Salted__'):
        salt = decoded[8:16].hex()
        print(f"  Salt: {salt}")
        
        # Known salts:
        # terminal: b45a5e3d827593ca
        # salphaseion-short: 3ab585348552415d
        # cosmic-duality: 2d3f6fe06dc950e6
        
        if salt == 'b45a5e3d827593ca':
            print(f"  --> MATCHES terminal.b64!")
        elif salt == '3ab585348552415d':
            print(f"  --> MATCHES salphaseion-short.b64!")
        elif salt == '2d3f6fe06dc950e6':
            print(f"  --> MATCHES cosmic-duality.b64!")
        else:
            print(f"  --> UNKNOWN container!")

# Look for SECOND base64 block - the one that gave us 48 raw bytes
print(f"\n" + "="*70)
print("Looking for SECOND base64 block (should give 48 bytes)")
print("="*70)

# After first base64, there's 'z'separator then another base64 block
# Let me just find all base64-looking blocks
b64_patterns = []
i = 0
while i < len(sp):
    if sp[i] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':  # potential base64 start
        j = i
        while j < len(sp) and sp[j] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/':
            j += 1
        if j - i >= 10:
            b64_patterns.append((i, j, sp[i:j]))
        i = j
    else:
        i += 1

print(f"\nFound {len(b64_patterns)} potential base64 blocks:")
for idx, (start, end, text) in enumerate(b64_patterns):
    print(f"\n  Block {idx}: positions {start}-{end-1}, length {end-start}")
    print(f"    Text (first 80 chars): {text[:80]}")
    
    # Try decoding
    try:
        # Add padding if needed
        padded = text + '=' * ((4 - len(text) % 4) % 4)
        decoded = base64.b64decode(padded)
        print(f"    Decoded: {len(decoded)} bytes")
        print(f"    Hex: {decoded.hex()}")
        
        if decoded.startswith(b'Salted__'):
            print(f"    --> Salted__ format, salt={decoded[8:16].hex()}")
        elif len(decoded) == 48:
            print(f"    --> EXACTLY 48 bytes! This is the raw key+IV block!")
    except Exception as e:
        print(f"    Decode failed: {e}")

# Now let me look at the text AFTER run 5 but BEFORE the base64 blocks
# Run 5 is at 830-858 (29 chars)
print(f"\n" + "="*70)
print("Text around pos 830-1000:")
print("="*70)

print(f"\nPosition 820-900:")
print(f"  {repr(sp[820:900])}")

print(f"\nPosition 880-1000:")
print(f"  {repr(sp[880:1000])}")

# Where do 'matrixsumlist' and 'enter' come from?
# STEPS.md says:
#   pos 860-946: 87 chars a-i,o -> matrixsumlist
#   pos 948-973: 26 chars a-i,o -> enter

# But I just saw pos 860+ gives 'shabefourfirsthintisyourlastcommandU2FsdGVkX18...'
# which is NOT a-i,o. Let me check STEPS.md again.

# Actually - maybe the POSITIONS in terms of [z] separators?
# Let me count the 'z's

z_positions = [i for i, c in enumerate(sp) if c == 'z']
print(f"\n'z' separators at positions: {z_positions}")
print(f"Count: {len(z_positions)}")

# Let me get the segments between z's (or at ends)
segments = []
prev = 0
for z in z_positions:
    if z > prev:
        segments.append((prev, z-1, sp[prev:z]))
    prev = z + 1
if prev < len(sp):
    segments.append((prev, len(sp)-1, sp[prev:]))

print(f"\nSegments between z-separators:")
for i, (start, end, text) in enumerate(segments):
    # Is it a,b only?
    is_ab = all(c in 'ab' for c in text)
    # Is it a-i,o only?
    is_aio = all(ord('a') <= ord(c) <= ord('i') or c == 'o' for c in text)
    # Has upper case?
    has_upper = any(c.isupper() for c in text)
    
    print(f"\n  Segment {i}: positions {start}-{end}, length {end-start+1}")
    print(f"    First 50 chars: {text[:50]}")
    print(f"    All a,b: {is_ab}, All a-i,o: {is_aio}, Has uppercase: {has_upper}")

# Now let's decode any a-i,o segments we find using the correct method
def decode_a_i_o_as_words(s):
    """a=1..i=9, o=0 -> digits -> big integer -> hex -> ASCII"""
    if not s:
        return ""
    digits = ''.join(
        '0' if c == 'o' else str(ord(c) - ord('a') + 1)
        for c in s
    )
    try:
        n = int(digits)
        h = hex(n)[2:]
        if len(h) % 2:
            h = '0' + h
        b = bytes.fromhex(h)
        return b.decode('latin-1')
    except:
        return f"<decode failed>"

print(f"\n" + "="*70)
print("Decoding segments that look like a-i,o")
print("="*70)

for i, (start, end, text) in enumerate(segments):
    is_aio = all(ord('a') <= ord(c) <= ord('i') or c == 'o' for c in text)
    if is_aio and len(text) > 10:
        decoded = decode_a_i_o_as_words(text)
        print(f"\n  Segment {i} ({len(text)} chars a-i,o):")
        print(f"    Decoded: '{decoded}'")

print("\nDone.")
