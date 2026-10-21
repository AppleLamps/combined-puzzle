#!/usr/bin/env python3
"""
Decode the SalPhaseIon page completely:
1. The 570-char a-i run that was NEVER decoded
2. The second base64 block that doesn't start with Salted__
3. Analyze all hints
"""

import os
import re
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def a_i_o_to_digit(c):
    """a-i,o -> digit: a=1...i=9, o=0"""
    if c == 'o':
        return 0
    return ord(c) - ord('a') + 1

def decode_ai_run(text):
    """Decode a-i,o to digits then to hex then to ASCII.
    From STEPS.md: read digits as one decimal integer, write it in base 16, read hex as ASCII.
    """
    # First convert to digit string
    digits = ''.join(str(a_i_o_to_digit(c)) for c in text)
    
    # Interpret as decimal integer, convert to hex
    try:
        decimal_val = int(digits)
        hex_str = hex(decimal_val)[2:]  # remove '0x' prefix
        if len(hex_str) % 2 != 0:
            hex_str = '0' + hex_str  # make even length
        
        # Now decode hex to ASCII
        result = bytes.fromhex(hex_str).decode('latin-1')
        return {
            'digit_len': len(digits),
            'digits_first_100': digits[:100],
            'hex_len': len(hex_str),
            'decoded': result,
        }
    except Exception as e:
        # Also try: just 2 digits per byte directly (not big integer)
        if len(digits) % 2 == 0:
            try:
                result = bytes.fromhex(''.join(
                    format(int(digits[i:i+2]), '02x') 
                    for i in range(0, len(digits), 2)
                )).decode('latin-1')
                return {'method': 'direct_pair', 'decoded': result}
            except:
                pass
        return {'error': str(e)}

def decode_ab_binary(text):
    """a=0, b=1, 8 bits per byte, MSB first"""
    bits = ''.join('0' if c == 'a' else '1' for c in text)
    result = b''
    for i in range(0, len(bits), 8):
        byte_str = bits[i:i+8]
        if len(byte_str) == 8:
            result += bytes([int(byte_str, 2)])
    return result

# Read the full textarea
with open(os.path.join(BASE_DIR, 'files', 'salphaseion-textarea.txt'), 'r') as f:
    content = f.read().strip()

print("="*70)
print("SalPhaseIon Textarea Complete Analysis")
print("="*70)
print(f"Total length: {len(content)} chars")

# From STEPS.md structure:
# 0-90: 91 chars a-i -> "dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe"
# 91-194: 104 chars a,b -> decoded "matrixsumlist"
# 195-764: 570 chars a-i -> NEVER DECODED
# 765: 'z' separator
# 766-828: 63 chars a-i,o -> "lastwordsbeforearchichoice"
# 829: 'z' separator
# 830-858: 29 chars a-i,o -> "thispassword"
# 859: 'z' separator
# 860-894: text "shabefourfirsthintisyourlastcommand"
# 895-958: 64 chars base64 = salphaseion-short.b64
# 959-998: 40 chars a,b -> "enter"
# 999-1062: 64 chars base64 = QvX0... (NOT Salted__)
# 1063-1074: text "shabefanstoo"

# Let me split by 'z' and by pattern
run1 = content[0:91]
run2 = content[91:195]
run3_big = content[195:765]  # 570 chars!
z1 = content[765]
run4 = content[766:829]  # 63 chars
z2 = content[829]
run5 = content[830:859]  # 29 chars
z3 = content[859]
# Now after z3 (pos 859), let's find where text ends and base64 starts

# Find position of first uppercase after position 859
# Actually let's look for "fourfirsthint"
after_z3 = content[860:]

# "shabefourfirsthintisyourlastcommand" + base64 + a,b + base64 + "shabefanstoo"
# Let me search for the known patterns

# Find "fourfirsthintisyourlastcommand"
ffh_match = re.search(r'fourfirsthintisyourlastcommand', content)
if ffh_match:
    print(f"\n'fourfirsthintisyourlastcommand' at {ffh_match.start()}-{ffh_match.end()}")
    
    # Before that is "shabe"
    pos = ffh_match.start()
    before_text = content[max(0, pos-20):pos]
    print(f"  Before: '{before_text}'")
    
    # Now after the text: first base64 block
    after_text = content[ffh_match.end():]
    
    # Find first non-base64 character that starts a,b sequence
    # The first base64 ends, then there's "abbaabab..."
    first_b64_end = None
    for i in range(len(after_text)):
        c = after_text[i]
        if c in 'ab':  # base64 doesn't have lowercase a,b as trailing? Actually it can...
            # Check if next several are all a,b
            if i + 4 < len(after_text) and all(after_text[i+j] in 'ab' for j in range(5)):
                first_b64_end = i
                break
    
    if first_b64_end:
        first_b64 = after_text[:first_b64_end]
        between_a_b = after_text[first_b64_end:first_b64_end+40]  # run6 is 40 chars
        after_ab = after_text[first_b64_end+40:]
        
        print(f"\nFirst base64: {len(first_b64)} chars = salphaseion-short.b64")
        print(f"  Starts with Salted__? {base64.b64decode(first_b64)[:8] == b'Salted__'}")
        
        # Check if this equals files/salphaseion-short.b64
        with open(os.path.join(BASE_DIR, 'files', 'salphaseion-short.b64'), 'r') as f:
            sp_short_b64 = ''.join(f.read().split())
        print(f"  Matches files/salphaseion-short.b64? {first_b64 == sp_short_b64}")
        
        print(f"\nBetween a,b run (should be 'enter'): {len(between_a_b)} chars")
        ab_decoded = decode_ab_binary(between_a_b)
        print(f"  Decoded a,b: '{ab_decoded}'")
        
        # Now find second base64 in after_ab
        # Second base64 followed by "shabefanstoo"
        sft_match = re.search(r'shabefanstoo', after_ab)
        if sft_match:
            second_b64 = after_ab[:sft_match.start()]
            trailing = after_ab[sft_match.start():]
            print(f"\nSecond base64 (NOT Salted__): {len(second_b64)} chars")
            print(f"  Content: '{second_b64}'")
            
            # Try to decode this
            try:
                decoded = base64.b64decode(second_b64)
                print(f"  Decoded to {len(decoded)} bytes: {decoded.hex()}")
                
                # What is this?
                # Could be:
                # 1. Ciphertext without Salted__ header?
                # 2. A private key (48 bytes = too long for 256-bit key)
                # 3. Just binary data
                # 4. Maybe 32-byte key + 16-byte IV?
                
                print(f"\n  Analysis of decoded second b64:")
                if len(decoded) == 48:
                    print(f"    48 bytes = 32 bytes (AES-256 key) + 16 bytes (IV)")
                    print(f"    Potential key (first 32): {decoded[:32].hex()}")
                    print(f"    Potential IV (last 16): {decoded[16:].hex()}")
                
                # Check if it's printable
                printable = sum(1 for b in decoded if 32 <= b < 127 or b in (9, 10, 13))
                print(f"    Printable ratio: {printable}/{len(decoded)} = {printable/len(decoded):.1%}")
                print(f"    As printable chars: {''.join(chr(b) if 32 <= b < 127 else '.' for b in decoded)}")
                
            except Exception as e:
                print(f"  Error decoding: {e}")
            
            print(f"\nTrailing text: '{trailing}'")

print("\n" + "="*70)
print("DECODING THE BIG 570-CHAR a-i RUN (never decoded before!)")
print("="*70)

print(f"\nRun 3: positions 195-764 = {len(run3_big)} chars")
print(f"First 100: {run3_big[:100]}")
print(f"Last 100: {run3_big[-100:]}")

# Method 1: STEPS.md method = decimal integer -> hex -> ASCII
result1 = decode_ai_run(run3_big)
print(f"\nMethod 1 (decimal->hex->ASCII per STEPS.md):")
if 'error' in result1:
    print(f"  Error: {result1['error']}")
else:
    print(f"  Digit length: {result1.get('digit_len', 'N/A')}")
    print(f"  First 100 digits: {result1.get('digits_first_100', 'N/A')}")
    if 'decoded' in result1:
        dec = result1['decoded']
        print(f"  Decoded: {len(dec)} chars")
        print(f"  First 500 chars:\n{dec[:500]}")
        if len(dec) > 500:
            print(f"  ... total {len(dec)} chars")
        
        # Look for meaningful patterns
        print(f"\n  Looking for patterns...")
        if 'Salted__' in dec:
            print(f"    FOUND 'Salted__' (encrypted container)!")
        if re.search(r'[a-z]{10,}', dec):
            print(f"    Contains long lowercase text (likely readable)")
        printable_ratio = sum(1 for c in dec if 32 <= ord(c) < 127 or ord(c) in (9, 10, 13)) / len(dec)
        print(f"    Printable ratio: {printable_ratio:.1%}")

# Method 2: Try the first 91-char run too (for comparison)
print("\n" + "="*70)
print("DECODING RUN 1 (91 chars a-i) for comparison")
print("="*70)
result_run1 = decode_ai_run(run1)
if 'decoded' in result_run1:
    print(f"  Run 1 decoded: '{result_run1['decoded']}'")

print("\n" + "="*70)
print("Key insight: the four decoded words are HINTS/POINTERS")
print("="*70)
print("""
We have four explicitly decoded words:
1. "thispassword" (29 chars -> 74 hex digits)
2. "matrixsumlist" (104 bits -> 13 chars)  
3. "lastwordsbeforearchichoice" (153 bits? -> was interpreted as 78 chars)
4. "enter" (56 bits -> 7 chars)

PLUS we have:
- "fourfirsthintisyourlastcommand" (ASCII text, not encoded)
- "shabefanstoo" (trailing ASCII)

These point TO something:
- "thispassword" -> what IS the actual password?
- "matrixsumlist" -> sum what matrix? what list?
- "lastwordsbeforearchichoice" -> we found bytes 0-446 (this was correct!)
- "enter" -> add enter/newline? or press enter at end?

"four first hint" could mean:
- Take first 4 words/hints
- Take first hint (first letter of something?) repeated four times
- Take hint #4, etc.
""")

# Let me try: using the second base64 decoded 48 bytes 
# If it's 32-byte key + 16-byte IV, try using it directly on containers
# Actually wait: the password derivation is sha256(answer_text).hexdigest()
# So key is always derived from that

print("\n" + "="*70)
print("Testing: what if the second base64 IS the actual ciphertext?")
print("="*70)

# Wait - let me re-examine:
# SalPhaseIon-short.b64 = Salted__ + salt + ciphertext = complete OpenSSL format
# But what if there's another format?

# Load the three main containers
def load_b64(name):
    with open(os.path.join(BASE_DIR, 'files', name), 'r') as f:
        return name, base64.b64decode(''.join(f.read().split()))

terminal_name, terminal_data = load_b64('terminal.b64')
sp_short_name, sp_short_data = load_b64('salphaseion-short.b64')
cosmic_name, cosmic_data = load_b64('cosmic-duality.b64')

# Let's also examine the second base64 block - we found it earlier
second_b64_decoded = None
if 'second_b64' in dir():
    second_b64_decoded = base64.b64decode(second_b64)

print("\n" + "="*70)
print("Let me decode the 570-char run with ALTERNATIVE methods")
print("="*70)

# The 570-char a-i: if each pair = 2 digits, maybe it's hex-pairs directly?
# 570 chars = 570 digits (if 1 char = 1 digit)
# 570 is even, so that's 285 hex pairs if 2 digits per byte

run3_digits = ''.join(str(a_i_o_to_digit(c)) for c in run3_big)
print(f"\nBig run as digit string: {len(run3_digits)} digits")

# Try: 2 digits per byte, direct
if len(run3_digits) % 2 == 0:
    try:
        decoded = bytes.fromhex(''.join(
            format(int(run3_digits[i:i+2]), '02x')
            for i in range(0, len(run3_digits), 2)
        ))
        print(f"\nDirect 2-digit decode: {len(decoded)} bytes")
        print(f"First 200 hex: {decoded[:200].hex()}")
        
        # Try to find text
        printable = ''.join(chr(b) if 32 <= b < 127 or b in (9, 10, 13) else '.' for b in decoded[:500])
        print(f"First 500 printable view:\n{printable}")
        
        if b'Salted__' in decoded:
            print("\n  *** FOUND SALTED__ IN BIG RUN DECODE! ***")
            idx = decoded.find(b'Salted__')
            print(f"  At offset {idx}")
            
    except Exception as e:
        print(f"Error: {e}")

print("\nDone.")
