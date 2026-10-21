#!/usr/bin/env python3
"""
Analyze checkerboard-digits.txt properly.

It contains:
1. a-i,o encoded digit text (need to decode)
2. Some ASCII text directly: "abefourfirsthintisyourlastcommand"
3. A BASE64-encoded encrypted container (starts with U2FsdGVkX1 = Salted__)
4. More a,b text at the end
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

def decode_ab_binary(text):
    """a=0, b=1, 8 bits per byte, MSB first"""
    bits = ''.join('0' if c == 'a' else '1' for c in text)
    result = ''
    for i in range(0, len(bits), 8):
        byte_str = bits[i:i+8]
        if len(byte_str) == 8:
            result += chr(int(byte_str, 2))
    return result

# Read the checkerboard-digits
with open(os.path.join(BASE_DIR, 'derived', 'checkerboard-digits.txt'), 'r') as f:
    content = f.read()

print("="*70)
print("Checkerboard-digits.txt analysis")
print("="*70)

print(f"\nTotal length: {len(content)} chars")
print(f"First 500 chars:")
print(content[:500])
print(f"\nLast 500 chars:")
print(content[-500:])

# Find all ASCII text (non a-i,o)
# Actually let's separate:
# 1. Leading a-i,o sequence (the straddling checkerboard digits)
# 2. ASCII text
# 3. Base64 Salted__
# 4. Trailing a,b

# Let's find the base64 first
base64_matches = list(re.finditer(r'[A-Za-z0-9+/=]{20,}', content))
print(f"\nFound {len(base64_matches)} potential base64 sequences")

for m in base64_matches:
    try:
        decoded = base64.b64decode(m.group())
        if decoded.startswith(b'Salted__'):
            print(f"\n  --> Found 'Salted__' at position {m.start()}-{m.end()}")
            print(f"      First 16 hex: {decoded[:16].hex()}")
            print(f"      Salt: {decoded[8:16].hex()}")
            print(f"      Total encrypted: {len(decoded)} bytes")
    except:
        pass

# Let's manually split the content
# Looking at end: "...yourlastcommandU2FsdGVkX186tYU0hVJBXXUnBUO7..."

# Find where base64 Salted__ starts exactly
salted_pos = content.find('U2FsdGVkX1')  # base64 of 'Salted__'
print(f"\nU2FsdGVkX1 (Salted__) starts at position: {salted_pos}")

# Now split
part1 = content[:salted_pos]  # Everything before the base64 container
after_salted = content[salted_pos:]

# Find where base64 ends - it's followed by abab...
# Let's find the first non-base64 char after position salted_pos
import string
b64_chars = set(string.ascii_letters + string.digits + '+/=')

b64_end = len(content)
for i in range(salted_pos, len(content)):
    if content[i] not in b64_chars:
        b64_end = i
        break

base64_part = content[salted_pos:b64_end]
part3 = content[b64_end:]  # trailing abab...

print(f"\nContent structure:")
print(f"  Part 1 (before base64): {len(part1)} chars")
print(f"  Base64 container: {len(base64_part)} chars")
print(f"  Part 3 (after base64): {len(part3)} chars")

print(f"\nPart 1 last 200 chars:")
print(repr(part1[-200:]))

print(f"\nPart 3 (trailing):")
print(repr(part3))

# Decode the parts
print("\n" + "="*70)
print("Decoding Part 1")
print("="*70)

# Part 1 ends with "abefourfirsthintisyourlastcommand"
# "abe" at start = a,b,a -> could be binary or a-i digits

# Try to split at the first uppercase ASCII
last_upper = 0
for i, c in enumerate(part1):
    if 'A' <= c <= 'Z':
        last_upper = i

# Actually let me look for where plain ASCII starts
# Let me find "fourfirsthintisyourlastcommand"

ascii_text_match = re.search(r'[a-z]{8,}', part1)
if ascii_text_match:
    ascii_start = ascii_text_match.start()
    print(f"\nLowercase ASCII starts at position {ascii_start}")
    print(f"  Content: {repr(part1[ascii_start:])}")
    
    # The part BEFORE that is a-i,o encoded
    checkerboard_encoded = part1[:ascii_start]
    print(f"\n  Checkerboard-encoded part: {len(checkerboard_encoded)} chars")
    print(f"  First 100: {repr(checkerboard_encoded[:100])}")
    
    # But wait: the very start is "dbbibfbhcc..." - is there a prefix "abe" somewhere?
    # Let me check: the "abe" could be separate binary
    
    # Actually looking at part1:
    # It starts with a-i,o (straddling checkerboard digits)
    # Then has some a,b binary
    # Then "abefourfirsthintisyourlastcommand"
    
    # Let's decode "abe" at the start of that ASCII-prefixed part
    # "abe" before "four..." = a, b, e
    # a,b could be binary, or a=1, b=2, e=5?
    
    print(f"\n  Let's try decoding the 'abeXYZ' prefix pattern")
    # Look for pattern: [ab]+[a-o]?[a-z]+
    for m in re.finditer(r'([ab]+)([a-o]{0,3})([a-z]{8,})', part1):
        print(f"\n  Match: binary={m.group(1)}, between={m.group(2)}, text={m.group(3)}")
        binary_decoded = decode_ab_binary(m.group(1))
        print(f"    Binary '{m.group(1)}' decoded: {repr(binary_decoded)}")

# Also try to decode the entire part1 as a-i,o (except the final ASCII)
print("\n" + "="*70)
print("Decode the trailing a,b binary in part3")
print("="*70)
print(f"Trailing: '{part3}'")
if all(c in 'ab' for c in part3):
    decoded = decode_ab_binary(part3)
    print(f"As binary (a=0,b=1): {repr(decoded)}")

print("\n" + "="*70)
print("Decrypt the embedded base64 container")
print("="*70)

# The container is base64_part, which is Salted__ + salt + ciphertext
container_data = base64.b64decode(base64_part)
print(f"\nContainer: {len(container_data)} bytes")
print(f"Starts with Salted__: {container_data.startswith(b'Salted__')}")
salt = container_data[8:16]
print(f"Salt: {salt.hex()}")
ciphertext_len = len(container_data) - 16
print(f"Ciphertext: {ciphertext_len} bytes")

# Now we need the password for this container
# The clue: "fourfirsthintisyourlastcommand"
# Also we have the four words from earlier:
# 1. "thispassword"
# 2. "matrixsumlist"  
# 3. "lastwordsbeforearchichoice"
# 4. "enter"
# Plus: "fourfirsthintisyourlastcommand"
# Plus: "abefanstoo" at the very end (if decoded)

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

def try_decrypt(data: bytes, answer: str):
    """Try decrypting with answer -> sha256(answer).hexdigest().lower() as password"""
    password = hashlib.sha256(answer.encode()).hexdigest().lower()
    if not data.startswith(b'Salted__'):
        return False, None, 0.0
    salt = data[8:16]
    ciphertext = data[16:]
    try:
        key, iv = derive_key_and_iv(password, salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        total = len(plaintext)
        printable = sum(1 for b in plaintext if 32 <= b < 127 or b in (9, 10, 13))
        printable_ratio = printable / total if total > 0 else 1.0
        return True, plaintext, printable_ratio
    except:
        return False, None, 0.0

# Load all three main containers too
def load_b64(name):
    with open(os.path.join(BASE_DIR, 'files', name), 'r') as f:
        return name, base64.b64decode(''.join(f.read().split()))

main_containers = [
    load_b64('terminal.b64'),
    load_b64('salphaseion-short.b64'),
    load_b64('cosmic-duality.b64'),
]

# Build password candidates
candidates = [
    # The "four first hint" clue
    ("fourfirsthint", "fourfirsthint"),
    ("fourfirsthintisyourlastcommand", "fourfirsthintisyourlastcommand"),
    ("yourlastcommand", "yourlastcommand"),
    ("lastcommand", "lastcommand"),
    
    # The four decoded words
    ("thispassword", "thispassword"),
    ("matrixsumlist", "matrixsumlist"),
    ("lastwordsbeforearchichoice", "lastwordsbeforearchichoice"),
    ("enter", "enter"),
    
    # Combinations
    ("four_plus_this", "fourfirsthintthispassword"),
    ("thispassword_enter", "thispasswordenter"),
    ("enter_thispassword", "enterthispassword"),
    
    # The "abe" prefix decode if it's "010" binary or something
    # Actually "four first hint" might mean: use FIRST four of something?
    
    # From phase 2: "causality"
    ("causality", "causality"),
    
    # From phase 3.2: the answer itself
    ("phase32_answer", "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"),
    
    # Checkerboard plaintext
    ("checkerboard_plain", "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"),
    ("checkerboard_plain_lower", "incaseyoumanagetocrackthistheprivatekeysbelongtohalfandbetterhalfandtheyalsoneedfundstolive"),
    
    # HALF and BETTERHALF
    ("HALF", "HALF"),
    ("BETTERHALF", "BETTERHALF"),
    ("HALFBETTERHALF", "HALFBETTERHALF"),
    ("half", "half"),
    ("betterhalf", "betterhalf"),
    ("halfbetterhalf", "halfbetterhalf"),
    
    # The architect endings
    ("CIAOBELLAO", "CIAOBELLAO"),
    ("GOODLUCK", "GOODLUCK"),
    ("ciaobellao", "ciaobellao"),
    ("goodluck", "goodluck"),
]

# Also try: the 149 digits from salphaseion-textarea.txt
with open(os.path.join(BASE_DIR, 'files', 'salphaseion-textarea.txt'), 'r') as f:
    sp_149 = f.read().strip()

candidates.append(("sp_textarea_digits", sp_149))

# And the 149 digits from checkerboard proper (from STEPS.md)
with open(os.path.join(BASE_DIR, 'derived', 'checkerboard-digits.txt'), 'r') as f:
    cb_content = f.read()
# Extract just the leading a-i part
# Actually let me look at the decoded version from STEPS.md

# Also try the checkerboard plaintext words in various forms
cb_plain = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"

for word in ["INCASE", "YOU", "MANAGE", "TO", "CRACK", "THIS", "THE", "PRIVATE", "KEYS", 
             "BELONG", "HALF", "BETTERHALF", "AND", "THEY", "ALSO", "NEED", "FUNDS", "LIVE"]:
    candidates.append((f"cb_{word.lower()}", word.lower()))
    candidates.append((f"cb_{word}", word))

print(f"\nTrying {len(candidates)} candidates...")

for label, ans in candidates:
    # First try the EMBEDDED container
    success, dec, ratio = try_decrypt(container_data, ans)
    if success:
        print(f"\n{'='*70}")
        print(f"SUCCESS on EMBEDDED CONTAINER with: {label}")
        print(f"  Answer: {repr(ans[:100])}...")
        print(f"  Decrypted: {len(dec)} bytes, {ratio:.1%} printable")
        if dec.startswith(b'Salted__'):
            print(f"  --> ANOTHER NESTED CONTAINER! Inner salt: {dec[8:16].hex()}")
        print(f"  Hex first 64: {dec[:64].hex()}")
        if ratio > 0.5:
            print(f"  As text: {dec[:200]}")
    
    # Also try the three main containers
    for cname, cdata in main_containers:
        success, dec, ratio = try_decrypt(cdata, ans)
        if success:
            print(f"\n{'='*70}")
            print(f"SUCCESS on {cname} with: {label}")
            print(f"  Answer: {repr(ans[:100])}...")
            print(f"  Decrypted: {len(dec)} bytes, {ratio:.1%} printable")
            if dec.startswith(b'Salted__'):
                print(f"  --> NESTED! Inner salt: {dec[8:16].hex()}")
            print(f"  First 64 hex: {dec[:64].hex()}")

print("\nDone with main candidates.")

# Now let's try: what if "four first hint" means FOUR of something we already have?
# The four decoded words: "thispassword", "matrixsumlist", "lastwordsbeforearchichoice", "enter"
# Try them in different orders and combinations

print("\n" + "='*70")
print("Now testing: 4 words in different orders/combinations")
print("="*70)

four_words = ["thispassword", "matrixsumlist", "lastwordsbeforearchichoice", "enter"]

# All 4 concatenated in different orders
import itertools
for perm in itertools.permutations(four_words):
    concat = ''.join(perm)
    pw_label = f"perm_{'_'.join(p[:3] for p in perm)}"
    
    # Try embedded
    success, dec, ratio = try_decrypt(container_data, concat)
    if success:
        print(f"\nSUCCESS embedded: {pw_label} -> {len(dec)} bytes, {ratio:.1%} printable")
        print(f"  First 64 hex: {dec[:64].hex()}")
    
    # Try main containers
    for cname, cdata in main_containers:
        success, dec, ratio = try_decrypt(cdata, concat)
        if success:
            print(f"\nSUCCESS {cname}: {pw_label} -> {len(dec)} bytes")

# Also try interleavings - "7 intertwined passwords" was mentioned
# But that might be too many. Let me try pairwise first.

print("\nDone.")
