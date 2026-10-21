#!/usr/bin/env python3
"""
Analyze the 149 checkerboard digits for HALF and BETTERHALF pattern.
"""

digits = '15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112'
print(f'Length: {len(digits)}')

# Find all occurrences of repeated substrings
print("\nLooking for repeated patterns in 149 digits:")
seq = '1491109166'
positions = []
for i in range(len(digits) - len(seq) + 1):
    if digits[i:i+len(seq)] == seq:
        positions.append(i)
print(f'Sequence "{seq}" found at positions: {positions}')

print(f'\nAt position 80:  {digits[80:80+25]}')
print(f'At position 100: {digits[100:100+25]}')

# They share '1491109166'
print(f'\nFirst occurrence (80-89):  {digits[80:90]}')
print(f'Second occurrence (100-109): {digits[100:110]}')

# What's between them?
print(f'\nBetween them (90-99): {digits[90:100]}')

# Now, note: 149 is the TOTAL LENGTH
# The sequence starts with "149" = meta-reference!

# What if:
#   Position 80-99  = HALF
#   Position 100-119 = BETTERHALF

half_start = 80
betterhalf_start = 100

print(f'\nTrying HALF = position {half_start} onwards, BETTERHALF = position {betterhalf_start} onwards')

# HALF: could be 80-148 or just a portion
# BETTERHALF: could be 100-148
half = digits[80:]
betterhalf = digits[100:]
print(f'\nHALF candidate (80-148, {len(half)} chars): {half}')
print(f'BETTERHALF candidate (100-148, {len(betterhalf)} chars): {betterhalf}')

# Check overlap
print(f'\nCommon prefix of half & betterhalf:')
for i in range(min(len(half), len(betterhalf))):
    if half[i] == betterhalf[i]:
        print(f'  {i}: {half[i]} == {betterhalf[i]}')
    else:
        print(f'  {i}: {half[i]} != {betterhalf[i]} <- first difference')
        break

# Could be:
# - As strings (like the concatenated answers in phase 3 and 3.2)
# - As numbers -> hex
# - Interpreted as something with the checkerboard straddling cipher

print("\n\n" + "="*70)
print("STRADDLING CHECKERBOARD RE-EXAMINATION")
print("="*70)

# The straddling checkerboard (from STEPS.md):
#        0 1 2 3 4 5 6 7 8 9
#      +---------------------
#      | E T A O N R I S 2 ?   <- these are at positions 2 and 6 (the blanks)
#    2 | B C D F G H J K L M   
#    6 | P Q 1 U V W X Y Z 0   
#
# Actually, need to check carefully...

# From STEPS.md:
# The straddling checkerboard is:
#     0 1 2 3 4 5 6 7 8 9
#   +--------------------
#   | E T A O N R I S 2 ?    <- row is 2 digits, so this is row '' (empty prefix)?
# 2 | B C D F G H J K L M    <- row '2'
# 6 | P Q 1 U V W X Y Z 0    <- row '6'
#
# Actually I need to be more careful. Let me read STEPS.md again:
#
# In straddling checkerboard:
# - Two rows have "blanks" (no digit assigned) at positions 2 and 6
# - Those digits (2 and 6) become ROW PREFIXES
# - So:
#   - Single digit: look up in the top row
#   - If digit is 2 or 6: it's a 2-digit code, take next digit for column

# Let me reconstruct from what we know. Phase 3 answer used checkerboard.
# Actually, let me just implement the checkerboard properly:

# First row (single-digit codes, except 2 and 6 are prefixes):
# position: 0 1 2 3 4 5 6 7 8 9
# value:    E T _ O N R _ I S 2 ?  Wait, STEPS says positions 2 and 6 are the blank ones

# Actually from checkerboard-plaintext.txt we know:
# '26' decoded to '1'
# '62' decoded to '1' also seen in the digits

# Let me look at checkerboard-digits.txt decoding process
# Actually let me just verify: we have checkerboard-plaintext.txt as decoded

# Let me instead think: could HALF and BETTERHALF themselves be decoded through the checkerboard?

# Looking at the repeated pattern around 80 and 100:
# 80-99:  1491109166 3121313128
# 100-119:1491109166 1314121991

# Let me count digits differently: '149' could be self-referential (total length = 149)
# What about '1109' and '166'?

# Looking at Phase 3.2's matrixsumlist instruction and the last words:
# The last words end with: "One for one, four for one."
# That's:
# - One for one -> 1 for 1
# - four for one -> 4 for 1
#
# The puzzle likes:
# - Numbers as words (five = 5 = E, three = 3, etc.)
# - Counting letters

# Actually let's try a different angle. Looking at checkerboard plaintext:
# "private KEYS belong to HALF and BETTERHALF"
# So there are TWO KEYS. Private KEYS (plural).

# For the 5 BTC address, we have the FULL PUBLIC KEY given in README.md
# That's 65 bytes (uncompressed) or 33 bytes (compressed). 

# But what if:
# - The private key is DERIVED from two values: HALF and BETTERHALF
# - Like: d = hash(HALF) XOR hash(BETTERHALF)
# - Or: d = hash(HALF + BETTERHALF)
# - Or: the raw 256-bit key is split into two halves

# But first we need to decrypt SalPhaseIon short or Terminal or Cosmic Duality.
# Let me try using HALF and BETTERHALF (as identified from repeated pattern) as answer text.

# First, let me identify the split based on the two occurrences of '1491109166'
# First occurrence: position 80-89 = '1491109166'
# Second occurrence: position 100-109 = '1491109166'
# So there's a copy at 80, then 10 chars later another copy at 100.

# What if:
# HALF = digits from START to first marker
# BETTERHALF = digits from START to second marker

# Or:
# HALF = digits before first '1491109166' + something
# BETTERHALF = different interpretation

# Actually wait: 149 is the total length.
# And the sequence '149' appears at position 80 and 100 within that.
# This is like a META pointer.

# Let me try: take the 149 digits and interpret them with the straddling checkerboard
# But first I need to know the exact checkerboard mapping.

# From earlier work reproducing Phase 3, let me verify:
# Phase 3 used straddling checkerboard. Let me check if the checkerboard digits
# decode to something meaningful.

print("\nActually let me first confirm: are these 149 digits already the DECODED ones?")
print("Looking at checkerboard-plaintext.txt...")

with open('derived/checkerboard-plaintext.txt', 'r') as f:
    cb_plain = f.read()
print(f"checkerboard-plaintext.txt = {repr(cb_plain)}")

print("\nSo the 149 digits were DECODED to produce that plaintext.")
print("That means: 149 digits -> checkerboard decode -> 'private KEYS belong to HALF and BETTERHALF'")
print("So we ALREADY USED these digits to get that sentence.")

print("\n" + "="*70)
print("But wait: the plaintext says 'private KEYS' and mentions HALF and BETTERHALF")
print("Maybe the 149 digits themselves CONTAIN HALF and BETTERHALF in some other form?")
print("="*70)

# Let's try: the 149 digits is a SEQUENCE. Maybe split it by the two occurrences of '149'

# '149' appears:
# - Where does '149' appear?
idx_149 = []
for i in range(len(digits)-2):
    if digits[i:i+3] == '149':
        idx_149.append(i)
print(f"\n'149' found at positions: {idx_149}")

# So at positions: 79? Actually let's look
print(f"Position 78-80: {digits[78:81]}")  
print(f"Position 98-100: {digits[98:101]}")

# OK so:
# - position 78-80: first '149'
# - position 98-100: second '149'

# What if:
# HALF = digits[0:78] or digits[78:98]
# BETTERHALF = digits[98:] or digits[78:98] vs digits[98:]

print(f"\nSplitting at the two '149' markers:")
print(f"  digits[0:78]    = {digits[0:78]} (length={len(digits[0:78])})")
print(f"  digits[78:98]   = {digits[78:98]} (length={len(digits[78:98])})")
print(f"  digits[98:]     = {digits[98:]} (length={len(digits[98:])})")

# Interesting: digits[78:98] = "14911091663121313128" (20 chars)
#              digits[98:]  = "1491109166131412199114371612126021664313711154112" (51 chars)

# They share the common prefix "1491109166"

print("\n\nHypothesis: the two copies share '1491109166' as a header.")
print("  Copy 1 header (10 chars) + payload (10 chars) = 20 chars total")
print("  Copy 2 header (10 chars) + payload (41 chars) = 51 chars total")

copy1_payload = digits[78+10 : 78+20]  # after first 10 of the 20
copy2_payload = digits[98+10 : ]
print(f"\n  Copy 1 payload (position 88-97): {copy1_payload}")
print(f"  Copy 2 payload (position 108-148): {copy2_payload}")

# Now what about copy 0 or the part BEFORE position 78?
# That's 78 chars

# Could be:
# HALF = copy1_payload
# BETTERHALF = copy2_payload
# Or: HALF = first section, BETTERHALF = something else

# Actually "HALF" and "BETTERHALF" - maybe HALF is literally half of something?
# And BETTERHALF is... the better half? Or half-but-better?

# Let me look at the phrase again: "private KEYS belong to HALF and BETTERHALF"
# The KEYS are plural. So maybe we need TWO passwords, not one?
# - password1 = sha256(HALF-related stuff).hexdigest()
# - password2 = sha256(BETTERHALF-related stuff).hexdigest()

# There are THREE containers. Maybe:
# - One container needs HALF password
# - One needs BETTERHALF password
# - One needs both combined

print("\n\nTrying HALF and BETTERHALF candidates:")
print("="*70)

import hashlib
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

BASE_DIR = '.'

def derive_key_and_iv(password: str, salt: bytes) -> tuple:
    password_bytes = password.encode('utf-8')
    D_i = b''
    result = b''
    while len(result) < 48:
        md = hashlib.sha256()
        md.update(D_i + password_bytes + salt)
        D_i = md.digest()
        result += D_i
    return result[:32], result[32:48]

def try_decrypt(container_path: str, answer_text: str) -> tuple:
    password = hashlib.sha256(answer_text.encode()).hexdigest().lower()
    with open(os.path.join(BASE_DIR, container_path), 'r') as f:
        data = base64.b64decode(f.read().strip())
    if not data.startswith(b'Salted__'):
        return False, None, 'No Salted__'
    salt = data[8:16]
    ciphertext = data[16:]
    key, iv = derive_key_and_iv(password, salt)
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return True, plaintext, password
    except Exception:
        return False, None, password

def analyze_pt(plaintext: bytes) -> dict:
    if plaintext is None:
        return {'ratio': 0}
    printable = sum(1 for b in plaintext if 32 <= b < 127 or b in (9, 10, 13))
    return {
        'ratio': printable / len(plaintext) if plaintext else 0,
        'len': len(plaintext),
        'start': plaintext[:80]
    }

containers = [
    ('SalShort', 'files/salphaseion-short.b64'),
    ('Terminal', 'files/terminal.b64'),
    ('Cosmic', 'files/cosmic-duality.b64'),
]

# Build candidate list
candidates = []

# HALF candidates
candidates.append((digits[0:78], 'part1_before_first_149 (78 chars)'))
candidates.append((digits[78:98], 'part2_between_149s (20 chars)'))
candidates.append((digits[98:], 'part3_after_second_149 (51 chars)'))
candidates.append((copy1_payload, 'copy1_payload (10 chars)'))
candidates.append((copy2_payload, 'copy2_payload (41 chars)'))
candidates.append((digits[78:98] + digits[98:], 'part2 + part3 combined'))
candidates.append((digits[0:78] + digits[78:98], 'part1 + part2'))

# Also try 'HALF' and 'BETTERHALF' as literal words
candidates.append(('HALF', 'literal_HALF'))
candidates.append(('BETTERHALF', 'literal_BETTERHALF'))
candidates.append(('HALFBETTERHALF', 'HALFBETTERHALF'))
candidates.append(('BETTERHALFHALF', 'BETTERHALFHALF'))

# Also try with 'enter' suffix
for text, name in list(candidates):
    candidates.append((text + 'enter', name + '+enter'))
    candidates.append((text + '\n', name + '+LF'))

# Also try the words "half" and "betterhalf" (case variations)
candidates.append(('half', 'lowercase_half'))
candidates.append(('betterhalf', 'lowercase_betterhalf'))

print(f"\nTrying {len(candidates)} candidates...")

found_any = False
for answer_text, desc in candidates:
    for name, path in containers:
        success, plaintext, pwd = try_decrypt(path, answer_text)
        if success:
            a = analyze_pt(plaintext)
            print(f"\n*** PADDING PASSED ***")
            print(f"    Answer: {desc} = {repr(answer_text[:100])}...")
            print(f"    Container: {name}")
            print(f"    Printable: {a['ratio']*100:.1f}%")
            print(f"    Start: {repr(a['start'])}")
            found_any = True

if not found_any:
    print("  None passed padding check.")

# Also let me try combinations with the lastwords text
print("\n\n" + "="*70)
print("Trying combinations with lastwords text")
print("="*70)

with open('derived/phase3.2-plaintext.bin', 'rb') as f:
    phase32 = f.read()

last_words = phase32[:447]
lw_text = last_words.decode('utf-8', errors='ignore')
lw_nolf = lw_text.replace('\n', '').replace('\r', '')

# Various combinations
combo_candidates = [
    (lw_nolf + digits[0:78], 'lw_nolf + part1'),
    (lw_nolf + digits[78:98], 'lw_nolf + part2'),
    (lw_nolf + digits[98:], 'lw_nolf + part3'),
    (lw_nolf + copy1_payload, 'lw_nolf + copy1_payload'),
    (lw_nolf + copy2_payload, 'lw_nolf + copy2_payload'),
    (digits[0:78] + lw_nolf, 'part1 + lw_nolf'),
    (digits[78:98] + lw_nolf, 'part2 + lw_nolf'),
    (digits[98:] + lw_nolf, 'part3 + lw_nolf'),
    (lw_text, 'lw_with_LF'),
]

for answer_text, desc in combo_candidates:
    for name, path in containers:
        success, plaintext, pwd = try_decrypt(path, answer_text)
        if success:
            a = analyze_pt(plaintext)
            print(f"\n*** PADDING PASSED (combo) ***")
            print(f"    Answer: {desc}")
            print(f"    Container: {name}")
            print(f"    Printable: {a['ratio']*100:.1f}%")
            if a['ratio'] > 0.5:
                print(f"  >>>>> HIGH PRINTABLE RATIO! Check this!")
                print(f"  Answer text (first 200 chars): {repr(answer_text[:200])}")

print("\nDone.")
