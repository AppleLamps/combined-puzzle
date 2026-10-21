#!/usr/bin/env python3
"""
Test raw key+IV and key candidate passwords.
"""

import os
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ==== Functions ====

def derive_key_and_iv(password: str, salt: bytes) -> tuple[bytes, bytes]:
    """OpenSSL EVP_BytesToKey with SHA-256, 1 iteration."""
    password_bytes = password.encode('utf-8')
    D_i = b''
    result = b''
    while len(result) < 48:
        md = hashlib.sha256()
        md.update(D_i + password_bytes + salt)
        D_i = md.digest()
        result += D_i
    key = result[:32]
    iv = result[32:48]
    return key, iv

def decrypt_with_keyiv(ciphertext: bytes, key: bytes, iv: bytes) -> tuple[bool, bytes]:
    """Directly decrypt using raw key and IV."""
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded = cipher.decrypt(ciphertext)
        plaintext = unpad(padded, AES.block_size)
        return True, plaintext
    except Exception:
        return False, None

def try_password_on_all(password_text: str) -> dict:
    """Try a password (text -> sha256 hex) on all 3 containers."""
    password = hashlib.sha256(password_text.encode()).hexdigest().lower()
    results = {}
    
    for name, path in [('SalShort', 'files/salphaseion-short.b64'),
                       ('Terminal', 'files/terminal.b64'),
                       ('Cosmic', 'files/cosmic-duality.b64')]:
        with open(os.path.join(BASE_DIR, path), 'r') as f:
            data = base64.b64decode(f.read().strip())
        
        if not data.startswith(b'Salted__'):
            results[name] = (False, None)
            continue
        
        salt = data[8:16]
        ciphertext = data[16:]
        key, iv = derive_key_and_iv(password, salt)
        
        success, plaintext = decrypt_with_keyiv(ciphertext, key, iv)
        results[name] = (success, plaintext)
    
    return results

def analyze(plaintext: bytes) -> dict:
    if plaintext is None:
        return {'success': False}
    printable = sum(1 for b in plaintext if 32 <= b < 127 or b in (9, 10, 13))
    return {
        'success': True,
        'len': len(plaintext),
        'ratio': printable / len(plaintext) if plaintext else 0,
        'start': plaintext[:80]
    }

# ==== Raw key+IV test ====
print("="*70)
print("Testing RAW key+IV (from second base64 block) on ciphertext portions")
print("="*70)

with open(os.path.join(BASE_DIR, 'files', 'salphaseion-textarea.txt'), 'r') as f:
    content = f.read()

b64_2 = content[999:1063]
raw_bytes = base64.b64decode(b64_2)
raw_key = raw_bytes[:32]
raw_iv = raw_bytes[32:]

print(f"\nRaw key: {raw_key.hex()}")
print(f"Raw IV:  {raw_iv.hex()}")

for name, path in [('SalShort', 'files/salphaseion-short.b64'),
                   ('Terminal', 'files/terminal.b64'),
                   ('Cosmic', 'files/cosmic-duality.b64')]:
    with open(os.path.join(BASE_DIR, path), 'r') as f:
        data = base64.b64decode(f.read().strip())
    ciphertext = data[16:]  # skip Salted__ + salt
    
    success, plaintext = decrypt_with_keyiv(ciphertext, raw_key, raw_iv)
    print(f"\n{name}:")
    print(f"  ciphertext len: {len(ciphertext)}")
    print(f"  padding valid:  {success}")
    if success:
        a = analyze(plaintext)
        print(f"  printable: {a['ratio']*100:.1f}%")
        print(f"  start: {repr(a['start'])}")

# ==== Try password candidates ====
print("\n" + "="*70)
print("Trying instruction-based password candidates")
print("="*70)

# Get the "last words before archi"
with open(os.path.join(BASE_DIR, 'derived', 'phase3.2-plaintext.bin'), 'rb') as f:
    phase32 = f.read()
last_words = phase32[:447]
last_words_str = last_words.decode('utf-8', errors='ignore')

candidates = [
    # The four decoded instructions
    ('matrixsumlist', 'matrixsumlist'),
    ('lastwordsbeforearchichoice', 'lastwordsbeforearchichoice'),
    ('thispassword', 'thispassword'),
    ('enter', 'enter'),
    
    # With enter = add newline
    ('matrixsumlist\n', 'matrixsumlist+LF'),
    ('lastwordsbeforearchichoice\n', 'lastwordsbeforearchichoice+LF'),
    ('thispassword\n', 'thispassword+LF'),
    
    # The actual "last words" text
    (last_words_str, 'phase32_bytes_0-446'),
    (last_words_str + '\n', 'phase32_bytes_0-446+LF'),
    
    # Concatenations
    ('matrixsumlistlastwordsbeforearchichoicethispasswordenter', 'all4_concat'),
    ('fourfirsthintisyourlastcommand', 'fourfirsthint...'),
    ('shabefanstoo', 'shabefanstoo'),
    
    # Checkerboard
    ('HALF', 'HALF'),
    ('BETTERHALF', 'BETTERHALF'),
    ('HALFBETTERHALF', 'HALF+BETTERHALF'),
]

# Also get 149 digits and plaintext
with open(os.path.join(BASE_DIR, 'derived', 'checkerboard-digits.txt'), 'r') as f:
    digits = f.read().strip()
with open(os.path.join(BASE_DIR, 'derived', 'checkerboard-plaintext.txt'), 'r') as f:
    plain = f.read().strip()

candidates.extend([
    (digits, '149_digits'),
    (plain, 'checkerboard_plaintext'),
])

print(f"\nTrying {len(candidates)} candidates (sha256 hex of text as password)...")

any_success = False
for pwd_text, desc in candidates:
    results = try_password_on_all(pwd_text)
    for name, (success, plaintext) in results.items():
        if success:
            a = analyze(plaintext)
            print(f"\n  PADDING PASSED: {desc} -> {name}")
            print(f"    Printable: {a['ratio']*100:.1f}%")
            print(f"    Start: {repr(a['start'])}")
            any_success = True

if not any_success:
    print("  None passed padding check.")

# ==== Critical check: What if raw key+IV is for "SalPhaseIon short" ciphertext, but we
# are supposed to use the SALT from SalPhaseIon short with a derived key?
# Actually no - we have RAW key+IV, so we don't need derivation.
#
# Wait! Let me re-read the STEPS.md note:
#   "The two base64 runs joined are the SalPhaseIon short container"
#
# First base64 (895-958) ends with 'z'... let's check that!

print("\n" + "="*70)
print("Checking: What are the two base64 runs that form SalPhaseIon short?")
print("="*70)

print(f"\nPosition 895-958 (64 chars):")
print(f"  Content: {repr(content[895:959])}")
print(f"  Ends with 'z' at pos 958: {content[958] == 'z'}")

# So STEPS.md says:
#   895-958: base64 (64 chars) but it includes the 'z' separator at position 958!
#   That means the actual base64 is 895-957 (63 chars), not 895-958 (64 chars)

# But files/salphaseion-short.b64 exists, so let's compare
with open(os.path.join(BASE_DIR, 'files', 'salphaseion-short.b64'), 'r') as f:
    container_b64 = f.read().strip()

print(f"\nfiles/salphaseion-short.b64:")
print(f"  Length: {len(container_b64)}")
print(f"  Content: {container_b64}")

print(f"\nFrom textarea:")
print(f"  First b64 (895-957, exclude z): {content[895:958]}")  # 895-957 inclusive = 63 chars
print(f"  Second b64 (999-1062): {content[999:1063]}")

# If we JOIN them:
joined_b64 = content[895:958] + content[999:1063]  # first part (no z) + second part
print(f"\n  Joined: {joined_b64}")
print(f"  Match container file? {joined_b64 == container_b64}")

# Oh! This is important. Let me decode and check
try:
    joined_decoded = base64.b64decode(joined_b64)
    print(f"\n  Joined decoded length: {len(joined_decoded)}")
    print(f"  Starts with Salted__: {joined_decoded.startswith(b'Salted__')}")
except Exception as e:
    print(f"\n  Joined decode error: {e}")

# Wait - but if "two base64 runs joined are SalPhaseIon short container",
# then the second base64 (which we thought was raw key+IV) is actually PART of that container!
# 
# Let's re-check: second base64 decoded to 48 bytes with NO Salted__ header.
# But 48 bytes alone is NOT a full Salted__ container (which needs 8 + 8 + ciphertext).
#
# So:
# - First base64 block (895-957): 63 chars base64 -> let's decode
# - Second base64 block (999-1062): 64 chars base64 -> 48 bytes

first_b64_part = content[895:958]  # 63 chars
print(f"\nFirst base64 part (63 chars): {first_b64_part}")
try:
    first_decoded = base64.b64decode(first_b64_part + '=')  # maybe missing padding
    print(f"  With '=' padding: {len(first_decoded)} bytes")
    print(f"  Starts with Salted__: {first_decoded.startswith(b'Salted__')}")
except Exception as e:
    print(f"  Error: {e}")

# Let's just directly compare with the file
container_decoded = base64.b64decode(container_b64)
print(f"\nContainer decoded: {len(container_decoded)} bytes")
print(f"  First 16: {container_decoded[:16].hex()}")
print(f"  Salt: {container_decoded[8:16].hex()}")

# Now decode the "raw bytes" we had:
print(f"\nSecond base64 decoded (48 bytes): {raw_bytes.hex()}")

# If container = Salted__ (8) + salt (8) + ciphertext, and if second base64 is 48 bytes...
# Let's see: container_decoded is probably: 16 + X = length

# Actually let me just check the math:
print(f"\nContainer decoded length: {len(container_decoded)}")
print(f"48 bytes (second b64) + first part decoded = ?")

# First b64: 63 chars. With padding '=' that's 64 chars = 48 bytes.
# But 63 chars without padding = 47 bytes (63*6/8 = 47.25 -> 47 bytes, 2 bits padding)
# 
# Actually let's just decode both parts and see:
try:
    part1 = base64.b64decode(first_b64_part)
    print(f"\nFirst part decoded: {len(part1)} bytes, hex = {part1.hex()}")
    print(f"  Starts with Salted__? {part1[:8] == b'Salted__'}")
except Exception as e:
    print(f"First part decode error: {e}")

print(f"\nSecond part decoded: {len(raw_bytes)} bytes, hex = {raw_bytes.hex()}")

# Container is:
print(f"\nContainer file: {len(container_decoded)} bytes")
print(f"  {container_decoded.hex()}")

# If we concatenate part1 + part2:
try:
    concatenated = part1 + raw_bytes
    print(f"\npart1 + part2 = {len(concatenated)} bytes")
    print(f"  Match container? {concatenated == container_decoded}")
except:
    pass

print("\nDone.")
