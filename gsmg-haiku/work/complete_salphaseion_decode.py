#!/usr/bin/env python3
"""
Decode SalPhaseIon completely:

From STEPS.md and analysis:
- pos 0-90:     91 chars, a,b → [kit] (earlier record, not recomputed)
- pos 91-194:  104 chars, a,b → matrixsumlist (NEED TO VERIFY)
- pos 195-764: 570 chars, a-i → [kit] (NEVER DECODED)
- pos 765:       1 char, z → separator
- pos 766-828:  63 chars, a-i,o → lastwordsbeforearchichoice (verified)
- pos 829:       1 char, z → separator
- pos 830-858:  29 chars, a-i,o → thispassword (verified)
- pos 859:       1 char, z → separator
- pos 860-894:  35 chars, text → shabefourfirsthintisyourlastcommand
- pos 895-958:  64 chars, base64 → SalPhaseIon short container
- pos 959-998:  40 chars, a,b → enter (NEED TO VERIFY)
- pos 999-1062: 64 chars, base64 → second block (48 raw bytes = key+IV)
- pos 1063-1074: 12 chars, text → shabefanstoo
"""

import os
import base64

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ab_binary_to_text(s):
    """a=0, b=1, 8 bits per byte, MSB first"""
    bits = []
    for c in s:
        if c == 'a':
            bits.append('0')
        elif c == 'b':
            bits.append('1')
        else:
            raise ValueError(f"Not a,b: {c}")
    
    result = []
    for i in range(0, len(bits), 8):
        byte_bits = ''.join(bits[i:i+8])
        if len(byte_bits) == 8:
            result.append(chr(int(byte_bits, 2)))
    return ''.join(result)

def a_i_o_to_text(s):
    """a=1..i=9, o=0 -> digits string -> big integer -> hex -> ASCII"""
    digits = []
    for c in s:
        if c == 'o':
            digits.append('0')
        elif 'a' <= c <= 'i':
            digits.append(str(ord(c) - ord('a') + 1))
        else:
            raise ValueError(f"Not a-i,o: {c}")
    
    digits_str = ''.join(digits)
    try:
        n = int(digits_str)
        h = hex(n)[2:]
        if len(h) % 2:
            h = '0' + h
        b = bytes.fromhex(h)
        return b.decode('latin-1')
    except:
        return f"<decode failed: {digits_str[:30]}...>"

# Read the file
with open(os.path.join(BASE_DIR, 'files', 'salphaseion-textarea.txt'), 'r') as f:
    content = f.read()

print("="*70)
print("Complete SalPhaseIon decoding")
print("="*70)

print(f"\nTotal length: {len(content)} chars")

# Now decode each part according to the structure
print("\n" + "-"*70)
print("Part 1: pos 0-90 (91 chars, a,b)")
print("-"*70)
part1 = content[0:91]
is_ab = all(c in 'ab' for c in part1)
print(f"  Is all a,b: {is_ab}")
if is_ab:
    dec = ab_binary_to_text(part1)
    print(f"  Decoded as a,b binary: {repr(dec)}")
    print(f"  Length: {len(dec)} chars")
else:
    print(f"  First 20 chars: {part1[:20]}")

print("\n" + "-"*70)
print("Part 2: pos 91-194 (104 chars, a,b) -> should give 'matrixsumlist'")
print("-"*70)
part2 = content[91:195]
print(f"  Length: {len(part2)} chars")
is_ab2 = all(c in 'ab' for c in part2)
print(f"  Is all a,b: {is_ab2}")

if is_ab2:
    dec2 = ab_binary_to_text(part2)
    print(f"  Decoded: '{dec2}'")
    print(f"  Expected: 'matrixsumlist'")
    print(f"  Match: {dec2 == 'matrixsumlist'}")

print("\n" + "-"*70)
print("Part 3: pos 195-764 (570 chars, a-i) -> [kit] (NEVER DECODED)")
print("-"*70)
part3 = content[195:765]
print(f"  Length: {len(part3)} chars")
# Check if it's a-i only
is_ai = all('a' <= c <= 'i' for c in part3)
print(f"  Is all a-i: {is_ai}")

if is_ai:
    # Try decoding as a-i (no 'o' for zero, so 1-9 only)
    # This is a DIFFERENT encoding than a-i,o!
    print(f"\n  Trying different decodings...")
    
    # Method A: a-i,o style but interpret as 1-9 (no zeros)
    digits_a = []
    for c in part3:
        if 'a' <= c <= 'i':
            digits_a.append(str(ord(c) - ord('a') + 1))
    
    digits_str_a = ''.join(digits_a)
    print(f"\n  Method A (a-i -> 1-9, no zeros): {len(digits_str_a)} digits")
    print(f"    First 50 digits: {digits_str_a[:50]}")
    
    try:
        n_a = int(digits_str_a)
        h_a = hex(n_a)[2:]
        if len(h_a) % 2:
            h_a = '0' + h_a
        b_a = bytes.fromhex(h_a)
        print(f"\n    As big int -> hex -> bytes: {len(b_a)} bytes")
        print(f"    Hex: {b_a[:80].hex()}...")
        print(f"    Printable ratio: {sum(1 for x in b_a if 32<=x<127)/len(b_a):.1%}")
        print(f"    First 60 as ASCII: {repr(b_a[:60].decode('latin-1'))}...")
    except Exception as e:
        print(f"    Decode failed: {e}")

print("\n" + "-"*70)
print("Part 4: pos 766-828 (63 chars, a-i,o) -> 'lastwordsbeforearchichoice' (verified)")
print("-"*70)
part4 = content[766:829]
dec4 = a_i_o_to_text(part4)
print(f"  Decoded: '{dec4}'")
print(f"  Match: {dec4 == 'lastwordsbeforearchichoice'}")

print("\n" + "-"*70)
print("Part 5: pos 830-858 (29 chars, a-i,o) -> 'thispassword' (verified)")
print("-"*70)
part5 = content[830:859]
dec5 = a_i_o_to_text(part5)
print(f"  Decoded: '{dec5}'")
print(f"  Match: {dec5 == 'thispassword'}")

print("\n" + "-"*70)
print("Part 6: pos 959-998 (40 chars, a,b) -> should give 'enter'")
print("-"*70)
# After the third z (pos 859), we have:
# pos 860-894: text
# pos 895-958: 64 chars base64
# z at pos 958
# pos 959-998: 40 chars a,b

# Find position after 'z' at 958
# Actually let me search for where the 'abbaabab...' sequence begins
abba_idx = content.find('abba')
print(f"\n  'abba' pattern found at position {abba_idx}")
if abba_idx > 0:
    # Extract from that position
    # The a,b run that decodes to 'enter' should be 40 chars
    part6_candidate = content[abba_idx:abba_idx+40]
    print(f"  Candidate at {abba_idx}-{abba_idx+39}: {part6_candidate}")
    is_ab6 = all(c in 'ab' for c in part6_candidate)
    print(f"  Is all a,b: {is_ab6}")
    if is_ab6:
        dec6 = ab_binary_to_text(part6_candidate)
        print(f"  Decoded: '{dec6}'")
        print(f"  Expected: 'enter'")
        print(f"  Match: {dec6 == 'enter'}")

print("\n" + "-"*70)
print("Summary of 4 decoded instructions:")
print("-"*70)
print("  1. matrixsumlist (104 chars a,b binary at 91-194)")
print("  2. lastwordsbeforearchichoice (63 chars a-i,o at 766-828)")
print("  3. thispassword (29 chars a-i,o at 830-858)")
print("  4. enter (40 chars a,b binary at some position ~959+)")

print("\n" + "="*70)
print("Key question: What do these INSTRUCTIONS point to?")
print("="*70)
print("""
Interpretations so far:
- 'lastwordsbeforearchichoice' -> LITERALLY: bytes 0-446 of Phase 3.2
  (text BEFORE the architect section, ends with 'One for one, four for one')

- 'thispassword' -> maybe: what follows this position IS the password?
  Or: 'this' refers to something specific

- 'matrixsumlist' -> 'matrix' could be:
   * The 570-char a-i run (a matrix of data?)
   * The straddling checkerboard (a lookup matrix)
   * Phase 3.2 'chess board' which was actually packed text
  'sum' could be: numeric sum, XOR, concatenation, etc.
  'list' could be: list of words, list of digits, etc.

- 'enter' -> suffix with newline? prefix with newline?
   Or: 'press enter' meaning something comes to an end?
""")

print("\nDone.")
