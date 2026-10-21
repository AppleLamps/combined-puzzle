#!/usr/bin/env python3
"""
Verify the SalPhaseIon short decryption
- Check different line ending variations
- Look at decrypted content for patterns
"""

import os
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

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

def try_decrypt(data: bytes, password: str):
    if not data.startswith(b'Salted__'):
        return False, None, 0.0
    salt = data[8:16]
    ciphertext = data[16:]
    try:
        key, iv = derive_key_and_iv(password, salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        total = len(plaintext)
        if total == 0:
            printable_ratio = 1.0
        else:
            printable = sum(1 for b in plaintext if 32 <= b < 127 or b in (9, 10, 13))
            printable_ratio = printable / total
        return True, plaintext, printable_ratio
    except Exception as e:
        return False, None, 0.0

# Read phase 3.2 binary
with open(os.path.join(BASE_DIR, 'derived', 'phase3.2-plaintext.bin'), 'rb') as f:
    phase32_bin = f.read()

# Load SalPhaseIon short
with open(os.path.join(BASE_DIR, 'files', 'salphaseion-short.b64'), 'r') as f:
    sp_short = base64.b64decode(''.join(f.read().split()))

print("="*70)
print("Verifying SalPhaseIon short decryption")
print("="*70)

# Get bytes 0-446
before_archi = phase32_bin[0:447]
before_archi_str = before_archi.decode('latin-1')

print(f"\nOriginal bytes 0-446: {len(before_archi)} bytes")
print(f"Contains CRLF pairs: {'\r\n' in before_archi_str}")

# Count line endings
cr_count = before_archi.count(13)
lf_count = before_archi.count(10)
print(f"CR (\\r) count: {cr_count}")
print(f"LF (\\n) count: {lf_count}")

# Try variations
variations = []

# 1. Original bytes as latin-1 string (includes CRLF)
variations.append(("raw_latin1", before_archi_str))

# 2. Remove CR only
no_cr = before_archi_str.replace('\r', '')
variations.append(("no_cr", no_cr))

# 3. Remove LF only
no_lf = before_archi_str.replace('\n', '')
variations.append(("no_lf", no_lf))

# 4. Remove both CR and LF
no_crlf = before_archi_str.replace('\r', '').replace('\n', '')
variations.append(("no_crlf", no_crlf))

# 5. Normalize CRLF to LF (i.e., \r\n -> \n)
normalize_crlf = before_archi_str.replace('\r\n', '\n')
variations.append(("crlf_to_lf", normalize_crlf))

# Also try: what if trailing whitespace matters?
for name, text in list(variations):
    variations.append((f"{name}_rstrip", text.rstrip()))
    variations.append((f"{name}_strip", text.strip()))

print(f"\nTrying {len(variations)} variations...")
for name, ans in variations:
    password = hashlib.sha256(ans.encode()).hexdigest().lower()
    success, dec, ratio = try_decrypt(sp_short, password)
    if success:
        print(f"\n{'='*70}")
        print(f"SUCCESS with variation: {name}")
        print(f"{'='*70}")
        print(f"Answer length: {len(ans)} chars")
        print(f"Password (sha256 hex): {password}")
        print(f"Decrypted: {len(dec)} bytes, {ratio:.1%} printable")
        print(f"\nHex dump:")
        for i in range(0, len(dec), 16):
            chunk = dec[i:i+16]
            hex_part = ' '.join(f'{b:02x}' for b in chunk)
            ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            print(f"  {i:04x}: {hex_part:<48} {ascii_part}")
        
        # Check if this looks like: Salted__ (another encrypted container)
        if dec.startswith(b'Salted__'):
            print(f"\n*** DECRYPTED CONTENT STARTS WITH 'Salted__' ***")
            print(f"--> This is ANOTHER encrypted container inside!")
            inner_salt = dec[8:16]
            print(f"    Inner salt: {inner_salt.hex()}")
        
        # Check if it has any readable patterns
        print(f"\nAs ASCII (printable only):")
        ascii_text = ''.join(chr(b) if 32 <= b < 127 else ' ' for b in dec)
        print(f"  {ascii_text[:100]}...")

print("\nDone testing variations.")
