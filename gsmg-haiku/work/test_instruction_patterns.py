#!/usr/bin/env python3
"""
Systematic testing based on established patterns:

1. 'lastwordsbeforearchichoice' -> LITERALLY points to Phase 3.2 bytes 0-446
   This is PROVEN pattern.

2. So 'matrixsumlist' is also LITERAL English:
   - 'matrix' = which matrix?
     * The 570-char a-i run (a=1..i=9, so 570 digits)
     * The straddling checkerboard (2 rows)
     * The 'chess board' section of Phase 3.2 (which was actually packed text)
   - 'sum' = what kind of sum?
     * Simple digit sum
     * XOR of bytes
     * Concatenation (string sum)
   - 'list' = interpret as list?

3. 'thispassword' is also LITERAL:
   - 'this' = this SalPhaseIon section
   - Or: the password is 'thispassword' but combined with something

4. 'enter' is ACTION:
   - Add newline
   - Or: means 'enter' as in submit/confirm

Also text clues:
- 'shabefourfirsthintisyourlastcommand'
- 'shabefanstoo'

Let's think about the FOUR hints in order:
  1. matrixsumlist
  2. lastwordsbeforearchichoice -> gave us Phase 3.2 bytes 0-446
  3. thispassword
  4. enter

Maybe we need to APPLY the instructions in order to something?
Or: the answer is: result_of(matrixsumlist) + result_of(lastwords...) + thispassword + enter?

Actually let's think about 'fourfirsthintisyourlastcommand'
- 'fourfirsthint' could mean: take the FOUR hints and apply them
- 'lastcommand' = the 'enter' is the last command

Let's try: Phase 3.2 bytes 0-446 with various combinations.
"""

import os
import hashlib
import base64
import itertools

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

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def try_decrypt(container_path: str, answer_text: str) -> tuple[bool, bytes, str]:
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

# Load known data
with open(os.path.join(BASE_DIR, 'derived', 'phase3.2-plaintext.bin'), 'rb') as f:
    phase32 = f.read()

last_words = phase32[:447]  # bytes 0-446 inclusive
last_words_str = last_words.decode('utf-8', errors='ignore')
print(f"'lastwordsbeforearchichoice' points to: {len(last_words)} bytes")
print(f"First 100 chars: {repr(last_words_str[:100])}")
print(f"Last 100 chars: {repr(last_words_str[-100:])}")

# Load 149 digits
with open(os.path.join(BASE_DIR, 'derived', 'checkerboard-digits.txt'), 'r') as f:
    digits_149 = f.read().strip()
print(f"\n149 digits: first 30={digits_149[:30]} last 30={digits_149[-30:]}")

# Load SalPhaseIon textarea
with open(os.path.join(BASE_DIR, 'files', 'salphaseion-textarea.txt'), 'r') as f:
    content = f.read()

# The 570-char a-i run (pos 195-764)
ai_570 = content[195:765]
print(f"\n570-char a-i run: length={len(ai_570)}")

# Decode it: a=1..i=9 (no zeros in this run - no 'o's)
digit_map = {chr(ord('a') + i): str(i+1) for i in range(9)}
ai_as_digits = ''.join(digit_map[c] for c in ai_570 if c in digit_map)
print(f"As 1-9 digits: length={len(ai_as_digits)}")
print(f"First 50 digits: {ai_as_digits[:50]}")

# Various 'sum' interpretations
print("\n" + "="*70)
print("'matrixsumlist': trying various interpretations")
print("="*70)

# The 149 digits as 'matrix'
digit_sum_149 = sum(int(d) for d in digits_149)
print(f"\n149 digits sum: {digit_sum_149}")
print(f"149 digits as hex (big int): {int(digits_149):x}")

# The 570 digits as 'matrix'
try:
    digit_sum_570 = sum(int(d) for d in ai_as_digits)
    print(f"\n570 digits sum: {digit_sum_570}")
    # This is a huge number, but we can get various interpretations
    ai_bigint = int(ai_as_digits)
    # Get hex representation
    ai_hex = format(ai_bigint, 'x')
    print(f"570 digits as hex length: {len(ai_hex)} chars")
    print(f"First 100 hex chars: {ai_hex[:100]}")
except Exception as e:
    print(f"Error: {e}")

# Now let's try combinations
print("\n" + "="*70)
print("Trying answer candidates (sha256 hex as password)")
print("="*70)

containers = [
    ('SalShort', 'files/salphaseion-short.b64'),
    ('Terminal', 'files/terminal.b64'),
    ('Cosmic', 'files/cosmic-duality.b64'),
]

# Build candidate list
candidates = []

# 1. The actual text from 'lastwordsbeforearchichoice' - in different forms
#    Phase 3.2 bytes 0-446
#    - With original LFs
#    - Without LFs  
#    - With trailing LF (enter key)

lw_nolf = last_words.replace(b'\n', b'')
print(f"\nPhase 3.2 bytes 0-446: {len(last_words)} bytes, {len(lw_nolf)} bytes without LF")

candidates.extend([
    (last_words_str, 'lastwords_text'),
    (last_words.decode('utf-8', errors='ignore').replace('\n', ''), 'lastwords_noLF'),
])

# 2. Try the four instructions as answer itself
instructions = ['matrixsumlist', 'lastwordsbeforearchichoice', 'thispassword', 'enter']
candidates.append((''.join(instructions), 'all4_concat'))

# Try interleavings, concatenations, permutations
candidates.append(('matrixsumlist', 'instr1'))
candidates.append(('thispassword', 'instr3'))
candidates.append(('thispasswordenter', 'instr3+4'))
candidates.append(('matrixsumlistenter', 'instr1+4'))
candidates.append(('lastwordsbeforearchichoiceenter', 'instr2+4'))
candidates.append(('fourfirsthintisyourlastcommand', 'clue1'))
candidates.append(('shabefanstoo', 'clue2'))

# With '\n' suffix (enter = newline)
for text, name in list(candidates):
    candidates.append((text + '\n', name + '+LF'))

# Try 149 digits
candidates.append((digits_149, 'checkerboard_149_digits'))
candidates.append((str(digit_sum_149), '149_digit_sum'))
candidates.append((format(int(digits_149), 'x'), '149_digits_as_hex'))

# Try checkerboard plaintext
with open(os.path.join(BASE_DIR, 'derived', 'checkerboard-plaintext.txt'), 'r') as f:
    cb_plain = f.read().strip()
candidates.append((cb_plain, 'checkerboard_plaintext'))
candidates.append(('HALF', 'HALF'))
candidates.append(('BETTERHALF', 'BETTERHALF'))
candidates.append(('HALFBETTERHALF', 'HALFBETTERHALF'))

# Try variations of the last words text
candidates.append((last_words.decode('latin-1', errors='ignore'), 'lastwords_latin1'))
candidates.append((last_words.decode('latin-1', errors='ignore').replace('\n', ''), 'lastwords_latin1_noLF'))

# Also try as bytes converted to hex string (in case answer is binary data rendered as hex?)
candidates.append((last_words.hex(), 'lastwords_as_hex'))

print(f"\nTotal candidates to try: {len(candidates)}")

# Try them
results_found = []
for answer_text, desc in candidates:
    for name, path in containers:
        success, plaintext, pwd = try_decrypt(path, answer_text)
        if success:
            a = analyze_pt(plaintext)
            results_found.append((desc, name, a['ratio'], plaintext))
            print(f"\n*** PADDING PASSED ***")
            print(f"    Answer: {desc} ({len(answer_text)} chars)")
            print(f"    First 80 chars: {repr(answer_text[:80])}")
            print(f"    Container: {name}")
            print(f"    Printable: {a['ratio']*100:.1f}%")
            print(f"    First 80 bytes: {repr(a['start'])}")

if not results_found:
    print("  None passed padding check.")

# Let me try one more set: what if 'matrixsumlist' literally means:
# - list = list of the four instructions
# - sum = concatenate them
# - but 'matrix' = something else

# Actually: The pattern of solved phases:
#   Phase 2: answer was a SINGLE WORD from clues -> 'causality'
#   Phase 3: answer was a CONCATENATION of 18 answers
#   Phase 3.2: answer was a CONCATENATION of movie quotes
#
# So the answer is probably CONCATENATION of things.

# We have four instructions. We used one (lastwordsbeforearchichoice) to find text.
# Maybe the other three point to MORE text?

print("\n" + "="*70)
print("Alternative: what if 'thispassword' points to the four instructions?")
print("="*70)
print("""
  The four decoded instructions:
  1. matrixsumlist
  2. lastwordsbeforearchichoice
  3. thispassword
  4. enter
  
  If 'lastwordsbeforearchichoice' = Phase 3.2 bytes 0-446
  Maybe 'thispassword' = the list of decoded instructions themselves?
  
  Or: 'thispassword' refers to whatever password we're trying to find,
  and the instruction 'enter' means we need to append newline.
  
  Let me also think about the STRUCTURE of SalPhaseIon:
  
  There are SEVEN z-separated sections (6 z separators at 765, 829, 859, 958, ... actually only 4 z's):
    z positions: [765, 829, 859, 958]
  
  So:
  0-764:     mixed stuff (a,b decoded to matrixsumlist, a-i 570 chars never decoded)
  766-828:   a-i,o -> lastwordsbeforearchichoice
  830-858:   a-i,o -> thispassword
  860-894:   text: shabefourfirsthintisyourlastcommand
  895-958:   base64 + z
  959-998:   a,b -> enter
  999-1062:  base64
  1063-1074: text: shabefanstoo
  
  So the ORDER of instructions is:
    1. matrixsumlist (first)
    2. lastwordsbeforearchichoice
    3. thispassword
    4. enter (last, between the two base64 blocks)
    
  This matches 'fourfirsthintisyourlastcommand' = four hints, last command is 'enter'!
""")

# One more thing to try: the four instructions themselves, but CONCATENATED in different ways
# And remember Phase 3 concatenated many answers, Phase 3.2 concatenated many words.

# Let's try ALL permutations of the four instructions
print("\n" + "="*70)
print("Trying permutations of the four instructions (24 permutations)")
print("="*70)

instr_list = ['matrixsumlist', 'lastwordsbeforearchichoice', 'thispassword', 'enter']
print(f"Four instructions: {instr_list}")

# Since this is many combinations, let me track and limit
# Actually 4! = 24, that's fine

count = 0
found_any = False

for perm in itertools.permutations(instr_list):
    for join_char in ['', '\n', ' ']:
        answer = join_char.join(perm)
        for name, path in containers:
            success, plaintext, pwd = try_decrypt(path, answer)
            if success:
                a = analyze_pt(plaintext)
                print(f"\n*** PADDING PASSED (permutation) ***")
                print(f"  Permutation joined with '{repr(join_char)}': {perm}")
                print(f"  Container: {name}")
                print(f"  Printable: {a['ratio']*100:.1f}%")
                print(f"  Start: {repr(a['start'])}")
                found_any = True
                if a['ratio'] > 0.4:
                    print("\n" + "="*70)
                    print("HIGH PRINTABLE RATIO - CHECK THIS!")
                    print("="*70)
                    print(f"Full answer: {repr(answer)}")
                    print(f"Full decrypted ({a['len']} bytes): {plaintext.hex()[:200]}...")
        count += 1

if not found_any:
    print(f"  Checked {count} variations (24*3 join styles), none passed padding.")

# Also try: what if the 'enter' instruction means 'add ENTER character', not the word
# So try permutations of [matrixsumlist, lastwordsbeforearchichoice, thispassword] plus '\n'
instr_3 = ['matrixsumlist', 'lastwordsbeforearchichoice', 'thispassword']
print(f"\nTrying permutations of 3 instructions with actual LF char at end:")

for perm in itertools.permutations(instr_3):
    answer = ''.join(perm) + '\n'
    for name, path in containers:
        success, plaintext, pwd = try_decrypt(path, answer)
        if success:
            a = analyze_pt(plaintext)
            print(f"\n*** PADDING PASSED ***")
            print(f"  Permutation: {perm} + LF")
            print(f"  Container: {name}")
            print(f"  Printable: {a['ratio']*100:.1f}%")
            if a['ratio'] > 0.4:
                print(f"  HIGH PRINTABLE! Answer: {repr(answer)}")

print("\nDone.")
