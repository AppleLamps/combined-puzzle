#!/usr/bin/env python3
"""
GSMG Puzzle - Deep analysis of SalPhaseIon patterns

- Decode the UNUSED runs
- Understand what "matrixsumlist" could mean as an instruction
- Decode the 149 digits as a private key seed
"""

import hashlib
import base64

def aio_to_text(chars: str) -> str:
    """a-i=1-9, o=0 -> decimal -> hex -> ASCII"""
    digits = []
    for c in chars:
        if c == 'o':
            digits.append('0')
        elif 'a' <= c <= 'i':
            digits.append(str(ord(c) - ord('a') + 1))
    
    dec_str = ''.join(digits)
    try:
        val = int(dec_str)
        hex_str = format(val, 'x')
        if len(hex_str) % 2 != 0:
            hex_str = '0' + hex_str
        return bytes.fromhex(hex_str).decode('latin-1')
    except:
        return f"<decode-error: {len(dec_str)} digits>"

def ab_to_text(chars: str) -> str:
    """a=0, b=1, 8 bits per byte, MSB first"""
    bits = ''.join('0' if c == 'a' else '1' for c in chars)
    result = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            result.append(chr(int(byte, 2)))
    return ''.join(result)

# Read content
with open(r'c:\gsmg-puzzle-clean\files\salphaseion-textarea.txt', 'r') as f:
    content = f.read().strip()

print("="*70)
print("SalPhaseIon First Textarea - Structure Analysis")
print("="*70)

# Map out all sections by type
print(f"\nTotal length: {len(content)} chars")

# Find runs by character type
def get_run_type(c):
    if c in 'ab':
        return 'a/b'
    elif c in 'cdefghi':
        return 'a-i only'
    elif c == 'o':
        return 'a-i,o'
    elif c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=':
        return 'text/base64'
    elif c == 'z':
        return 'separator'
    else:
        return f'unknown({c})'

# Print the actual runs
print("\n--- Character runs by type ---")
runs = []
if content:
    current_type = get_run_type(content[0])
    current_start = 0
    for i, c in enumerate(content):
        t = get_run_type(c)
        if t != current_type:
            runs.append((current_start, i-1, current_type))
            current_type = t
            current_start = i
    runs.append((current_start, len(content)-1, current_type))

for start, end, typ in runs:
    length = end - start + 1
    sample = content[start:start+min(40, length)]
    print(f"  [{start}:{end}] len={length}, type={typ}: {sample}...")

print("\n" + "="*70)
print("Decoding ALL runs (even 'unused' ones)")
print("="*70)

# First unused run: 0-90 = 91 chars, a-i only (no o)
run1 = content[0:91]
print(f"\n[0:91] 91 chars, a-i only:")
print(f"  As a-i,o method (would be decimal, but no zeros):")
run1_decoded = aio_to_text(run1)
print(f"  Decoded length: {len(run1_decoded)} chars")
print(f"  First 100 chars: {repr(run1_decoded[:100])}")
print(f"  Printable ratio: {sum(1 for c in run1_decoded if 32 <= ord(c) < 127)/len(run1_decoded):.1%}")

# Third run: 195-764 = 570 chars, a-i only
run3 = content[195:765]
print(f"\n[195:764] 570 chars, a-i only:")
run3_decoded = aio_to_text(run3)
print(f"  Decoded length: {len(run3_decoded)} chars")
print(f"  First 200 chars: {repr(run3_decoded[:200])}")
print(f"  Printable ratio: {sum(1 for c in run3_decoded if 32 <= ord(c) < 127)/len(run3_decoded):.1%}")

# What if these a-i only runs are actually a/b pattern but different interpretation?
# What if a-i is actually octal or something else?

print("\n" + "="*70)
print("'matrixsumlist' - what could this mean?")
print("="*70)

# The straddling checkerboard:
#      0 1 2 3 4 5 6 7 8 9
#      F   U B   C D O R A
# 1    . L E T H I N G K Y
# 4    M V P S / J Q Z X W

checkerboard = {
    'row0': {'0': 'F', '2': 'U', '3': 'B', '5': 'C', '6': 'D', '7': 'O', '8': 'R', '9': 'A'},
    'row1': {'0': '.', '1': 'L', '2': 'E', '3': 'T', '4': 'H', '5': 'I', '6': 'N', '7': 'G', '8': 'K', '9': 'Y'},
    'row4': {'0': 'M', '1': 'V', '2': 'P', '3': 'S', '4': '/', '5': 'J', '6': 'Q', '7': 'Z', '8': 'X', '9': 'W'},
}

# Reverse lookup
char_to_code = {}
# Row 0 (single digit)
for d, c in checkerboard['row0'].items():
    char_to_code[c] = d
# Row 1 (prefix '1')
for d, c in checkerboard['row1'].items():
    char_to_code[c] = '1' + d
# Row 4 (prefix '4')
for d, c in checkerboard['row4'].items():
    char_to_code[c] = '4' + d

print("\nCheckerboard char -> code:")
for c in sorted(char_to_code.keys()):
    print(f"  '{c}' -> {char_to_code[c]}")

# Now - "matrixsumlist" - let's encode each word using the checkerboard
def encode_to_checkerboard_digits(text: str) -> str:
    result = []
    for c in text.upper():
        if c in char_to_code:
            result.append(char_to_code[c])
        else:
            result.append(f'?{c}?')
    return ''.join(result)

print("\nEncoding 'matrixsumlist' with checkerboard:")
words = ['matrix', 'sum', 'list', 'thingky', 'mvps', 'fubcd', 'oracle']
for w in words:
    encoded = encode_to_checkerboard_digits(w)
    print(f"  '{w}' -> {encoded}")

print("\n" + "="*70)
print("The 149 digits - let's look at its structure")
print("="*70)

with open(r'c:\gsmg-puzzle-clean\derived\checkerboard-digits.txt', 'r') as f:
    digits149 = f.read().strip()

print(f"Digits: {digits149}")
print(f"Length: {len(digits149)} (prime: 149 is indeed a prime number)")

# Look for prefixes '1' or '4' since they're escape codes for straddling checkerboard
print(f"\nLooking at as checkerboard-encoded (1=row1 prefix, 4=row4 prefix):")

def decode_checkerboard_digits(digits: str) -> str:
    """Decode using straddling checkerboard"""
    result = []
    i = 0
    while i < len(digits):
        d = digits[i]
        if d == '1':
            # Row 1 escape
            if i+1 < len(digits):
                next_d = digits[i+1]
                if next_d in checkerboard['row1']:
                    result.append(checkerboard['row1'][next_d])
                i += 2
            else:
                i += 1
        elif d == '4':
            # Row 4 escape
            if i+1 < len(digits):
                next_d = digits[i+1]
                if next_d in checkerboard['row4']:
                    result.append(checkerboard['row4'][next_d])
                i += 2
            else:
                i += 1
        else:
            # Row 0
            if d in checkerboard['row0']:
                result.append(checkerboard['row0'][d])
            else:
                result.append(f'[{d}?]')
            i += 1
    return ''.join(result)

decoded_checkerboard = decode_checkerboard_digits(digits149)
print(f"  Decoded as checkerboard: {decoded_checkerboard}")

# But STEPS.md says it SHOULD give us "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"
# So that already happened. Let's verify STEPS.md interpretation is correct.

print("\n" + "="*70)
print("Checking: is '149' special?")
print("="*70)

# 149 = number of digits. 149 is a prime.
# But also, what if we split at position 149, or 1, 4, 9?
# Or look for the ANSWER to give 149 digits...

# Actually wait - let's look at the unused 570 chars and 91 chars.
# If we interpret them as a NUMBER (like the a-i,o method does):
# They become HUGE integers. But we can take mod N...
# Actually secp256k1 order is 2^256 - something.

# But wait - let's think about "HALF" and "BETTERHALF". The checkerboard says there are TWO KEYS.
# 149 digits is too much for one 256-bit key (which needs at most 78 decimal digits).
# But 149 split -> could be 2 keys.

# Actually let's check: what's the MAX decimal digits for a 256-bit number?
# log10(2^256) ≈ 77.06... so max 78 digits.

# 149 digits: can't be one key, but could be:
# - 77 + 72 = 149 (first is valid key-length, second is too)
# - Or maybe it's NOT a key directly but a SEED to generate keys?

print("\n" + "="*70)
print("Thinking about the architect's words")
print("="*70)

with open(r'c:\gsmg-puzzle-clean\derived\architect-text.txt', 'r') as f:
    architect = f.read().strip()

# Find keywords
import re
keywords = ['GOODLUCK', 'CIAOBELLAO', 'PRIME', 'BASICS', 'SOURCE', 'CODE', 
            'TWENTY', 'THREE', 'SIXTEEN', 'SEVEN', 'INTERTWINED', 'PASSWORDS',
            'BRUTEFORCING', 'CATACLYSMIC', 'SYSTEM', 'CRASH']

print("Key phrases in architect text:")
for kw in keywords:
    matches = list(re.finditer(kw, architect))
    if matches:
        for m in matches:
            context_start = max(0, m.start() - 30)
            context_end = min(len(architect), m.end() + 30)
            print(f"  '{kw}' at pos {m.start()}: ...{architect[context_start:context_end]}...")

print("\n" + "="*70)
print("Analyzing 'shabefourfirsthintisyourlastcommand'")
print("="*70)

hint = "shabefourfirsthintisyourlastcommand"
print(f"Full hint: {hint}")

# Remove 'shabe' prefix
if hint.startswith('shabe'):
    without = hint[5:]
    print(f"\nWithout 'shabe': {without}")
    # "fourfirsthintisyourlastcommand"
    
    # Let's try to split meaningfully
    print("\nPossible word splits:")
    # Could be "four first hint is your last command"
    words = ["four", "first", "hint", "is", "your", "last", "command"]
    print(f"  Reading: 'four first hint is your last command'")
    
    # What was our "last command" (last answer)? Phase 3.2 was:
    # jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple
    
    # Or maybe "last command" = "enter" which was decoded?
    
    # "four first hint" - there were 4 decoded words:
    # 1. matrixsumlist
    # 2. lastwordsbeforearchichoice
    # 3. thispassword
    # 4. enter
    print(f"\n  We decoded 4 things: matrixsumlist, lastwordsbeforearchichoice, thispassword, enter")
    print(f"  The FIRST of these 4 is: matrixsumlist")
    print(f"  Is that telling us to use 'matrixsumlist'? But we tried it...")

# What if "shabe" is itself encoded with the checkerboard?
print("\n'shabe' via checkerboard:")
for ch in 'shabe':
    ch_upper = ch.upper()
    if ch_upper in char_to_code:
        print(f"  '{ch}' -> code {char_to_code[ch_upper]}")
    else:
        # What row is it in?
        row1_vals = set(checkerboard['row1'].values())
        row4_vals = set(checkerboard['row4'].values())
        row0_vals = set(checkerboard['row0'].values())
        if ch_upper in row1_vals:
            print(f"  '{ch}' -> in row1 (needs prefix 1)")
        elif ch_upper in row4_vals:
            print(f"  '{ch}' -> in row4 (needs prefix 4)")
        elif ch_upper in row0_vals:
            print(f"  '{ch}' -> in row0")
        else:
            print(f"  '{ch}' -> not in checkerboard at all")

# S is in row4 (char 'S'), H in row1, A in row0, B in row0, E in row1
# So:
#   S = 43
#   H = 14
#   A = 9
#   B = 3
#   E = 12
# "shabe" = 4 3 1 4 9 3 1 2

print("\n" + "="*70)
print("Trying an IDEA: maybe 'enter' IS the password, but needs case/encoding?")
print("="*70)

# Maybe password SHA256 is UPPERCASE hex? Let's check Phase 2 to confirm
phase2_answer = "causality"
phase2_pass_lower = hashlib.sha256(phase2_answer.encode()).hexdigest().lower()
phase2_pass_upper = hashlib.sha256(phase2_answer.encode()).hexdigest().upper()
print(f"Phase 2 answer: 'causality'")
print(f"  lower hex: {phase2_pass_lower}")
print(f"  upper hex: {phase2_pass_upper}")
# README says password is sha256(answer) as 64 lowercase hex characters

print("\nDone with analysis.")
