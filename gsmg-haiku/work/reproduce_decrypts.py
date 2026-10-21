#!/usr/bin/env python3
"""
Reproduce the solved phase decryptions to verify tooling.
"""
import subprocess
import os
import sys

# Add work directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openssl_decrypt import decrypt_b64_file, decrypt_openssl_aes256cbc
import hashlib

OPENSSL_PATH = r"C:\Program Files\Git\usr\bin\openssl.exe"

def sha256hex(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest().lower()

def test_openssl_decrypt():
    """Reproduce Phase 2 decryption using Python"""
    base_dir = r"c:\gsmg-puzzle-clean"
    
    print("=" * 60)
    print("REPRODUCING PHASE 2 DECRYPTION")
    print("=" * 60)
    
    answer = "causality"
    expected_password = "eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf"
    password = sha256hex(answer)
    
    print(f"Answer: {answer}")
    print(f"Password: {password}")
    print(f"Expected: {expected_password}")
    
    assert password == expected_password, f"Password mismatch!"
    print("✓ Password matches")
    
    filepath = os.path.join(base_dir, "files", "phase2.b64")
    expected_plaintext_path = os.path.join(base_dir, "derived", "phase2-plaintext.txt")
    
    with open(expected_plaintext_path, 'rb') as f:
        expected = f.read()
    
    try:
        plaintext = decrypt_b64_file(filepath, password)
        # Compare ignoring line ending differences
        normalized_plaintext = plaintext.replace(b'\r\n', b'\n')
        normalized_expected = expected.replace(b'\r\n', b'\n')
        
        if normalized_plaintext == normalized_expected:
            print("✓ Phase 2 decrypted correctly!")
        else:
            print(f"✗ Decrypted content doesn't match expected")
            print(f"Got ({len(plaintext)} bytes):")
            try:
                print(plaintext.decode('utf-8')[:500])
            except:
                print(plaintext[:500].hex())
        
        return plaintext
    except Exception as e:
        print(f"Decryption failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_phase3_decrypt():
    """Reproduce Phase 3 decryption - password is sha256 of 7 concatenated parts"""
    base_dir = r"c:\gsmg-puzzle-clean"
    
    print()
    print("=" * 60)
    print("REPRODUCING PHASE 3 DECRYPTION")
    print("=" * 60)
    
    # The 7 parts from STEPS.md
    part1 = "causality"
    part2 = "Safenet"
    part3 = "Luna"
    part4 = "HSM"
    part5 = "11110"
    part6 = "0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854"
    part7 = "B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1"
    
    answer = part1 + part2 + part3 + part4 + part5 + part6 + part7
    password = sha256hex(answer)
    
    print(f"Answer is concatenation of 7 parts ({len(answer)} chars)")
    print(f"Password (sha256): {password}")
    
    filepath = os.path.join(base_dir, "files", "phase3.b64")
    expected_plaintext_path = os.path.join(base_dir, "derived", "phase3-plaintext.txt")
    
    with open(expected_plaintext_path, 'rb') as f:
        expected = f.read()
    
    try:
        plaintext = decrypt_b64_file(filepath, password)
        normalized_plaintext = plaintext.replace(b'\r\n', b'\n')
        normalized_expected = expected.replace(b'\r\n', b'\n')
        
        if normalized_plaintext == normalized_expected:
            print("✓ Phase 3 decrypted correctly!")
        else:
            print(f"✗ Decrypted content doesn't match expected")
            print(f"Got ({len(plaintext)} bytes)")
            try:
                print(plaintext.decode('utf-8')[:500])
            except:
                print(plaintext[:500].hex())
        
        return plaintext
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

def test_phase32_decrypt():
    """Reproduce Phase 3.2 decryption"""
    base_dir = r"c:\gsmg-puzzle-clean"
    
    print()
    print("=" * 60)
    print("REPRODUCING PHASE 3.2 DECRYPTION")
    print("=" * 60)
    
    # From STEPS.md
    part1 = "jacquefresco"
    part2 = "giveitjustonesecond"
    part3 = "heisenbergsuncertaintyprinciple"
    
    answer = part1 + part2 + part3
    password = sha256hex(answer)
    expected_password = "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c"
    
    print(f"Answer: {answer}")
    print(f"Password: {password}")
    print(f"Expected: {expected_password}")
    
    assert password == expected_password, f"Password mismatch!"
    print("✓ Password matches")
    
    filepath = os.path.join(base_dir, "files", "phase3.2.b64")
    expected_plaintext_path = os.path.join(base_dir, "derived", "phase3.2-plaintext.bin")
    
    with open(expected_plaintext_path, 'rb') as f:
        expected = f.read()
    
    try:
        plaintext = decrypt_b64_file(filepath, password)
        
        if plaintext == expected:
            print("✓ Phase 3.2 decrypted correctly!")
        else:
            print(f"✗ Decrypted content doesn't match expected")
            print(f"Got {len(plaintext)} bytes, expected {len(expected)}")
        
        return plaintext
    except Exception as e:
        print(f"Decryption failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_phase32_structure(plaintext: bytes):
    """Analyze the Phase 3.2 structure per STEPS.md"""
    print()
    print("=" * 60)
    print("PHASE 3.2 STRUCTURE ANALYSIS")
    print("=" * 60)
    
    # Bytes 0-446: ASCII text
    part1 = plaintext[0:447]
    text_part = part1.decode('ascii', errors='replace')
    print(f"Bytes 0-446: text ({len(part1)} bytes)")
    print(f"First 300 chars: {text_part[:300]}...")
    print()
    
    # Bytes 447-1985: 1539 bytes (step 4a: architect text)
    part2 = plaintext[447:1986]
    print(f"Bytes 447-1985: step 4a data ({len(part2)} bytes)")
    print(f"  First 50 bytes hex: {part2[:50].hex()}")
    
    # Check how it maps a-i to letters
    # The text is derived by treating bytes 447-1985 as 1539 values in 1-26?
    # Or looking at STEPS.md: offset 0-90 are a-i characters
    
    # Actually let me look at the derived files
    base_dir = r"c:\gsmg-puzzle-clean"
    with open(os.path.join(base_dir, "derived", "architect-text.txt"), 'r') as f:
        architect = f.read().strip()
    print(f"  Expected: architect-text.txt ({len(architect)} chars)")
    print(f"  Starts with: {architect[:50]}...")
    
    # Bytes 1986-1989: CRLF CRLF
    part3 = plaintext[1986:1990]
    print(f"\nBytes 1986-1989: separator ({part3.hex()})")
    
    # Bytes 1990-2138: 149 digits
    part4 = plaintext[1990:2139]
    print(f"\nBytes 1990-2138: 149 digits area ({len(part4)} bytes)")
    print(f"  Hex: {part4[:100].hex()}...")
    
    with open(os.path.join(base_dir, "derived", "checkerboard-digits.txt"), 'r') as f:
        digits = f.read().strip()
    print(f"  Expected: checkerboard-digits.txt ({len(digits)} digits)")
    print(f"  {digits}")
    
    # Remaining bytes: embedded Terminal container
    part5 = plaintext[2139:]
    print(f"\nBytes 2139-end: Terminal container ({len(part5)} bytes)")
    
    # Compare with files/terminal.b64 (should be the same base64)
    with open(os.path.join(base_dir, "files", "terminal.b64"), 'r') as f:
        terminal_b64 = ''.join(f.read().split())
    print(f"  Should be same as files/terminal.b64 content...")
    
    return part2, part4, part5

def analyze_salphaseion_abba_pattern():
    """Analyze the abba patterns from salphaseion"""
    base_dir = r"c:\gsmg-puzzle-clean"
    
    print()
    print("=" * 60)
    print("SALPHASEION ABBA PATTERN ANALYSIS")
    print("=" * 60)
    
    # From STEPS.md:
    # a,b runs: a=0, b=1, 8 bits per ASCII character
    # 91-194: 104 chars of a,b -> 'matrixsumlist'
    # 959-998: 40 chars of a,b -> 'enter'
    
    # Check derived files
    with open(os.path.join(base_dir, "derived", "architect-text.txt"), 'r') as f:
        arch = f.read().strip()  # 1539 chars + newline = 1540
    with open(os.path.join(base_dir, "derived", "checkerboard-plaintext.txt"), 'r') as f:
        checker = f.read().strip()  # 91 chars + newline = 92
    
    print(f"architect-text.txt: {len(arch)} chars")
    print(f"  First 200: {arch[:200]}")
    print(f"  Last 200:  {arch[-200:]}")
    print()
    print(f"checkerboard-plaintext.txt: {len(checker)} chars")
    print(f"  Content: {checker}")
    
    # These are candidate texts!
    # The puzzle statement says:
    # - "Several parts of the solved material have no established use"
    # - INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE
    
    print()
    print("CANDIDATE PASSWORDS FROM UNUSED MATERIAL:")
    print("=" * 60)
    
    # The unopened containers:
    # 1. Terminal (files/terminal.b64) - 80 bytes ciphertext (small: only 1 block padding possible)
    # 2. SalPhaseIon short (files/salphaseion-short.b64) - 80 bytes
    # 3. Cosmic Duality (files/cosmic-duality.b64) - 1328 bytes
    
    # What could their passwords be?
    
    # SalPhaseIon textarea gave us:
    # - lastwordsbeforearchichoice
    # - thispassword
    # - shabefourfirsthintisyourlastcommand
    # - base64 Salted__ container
    # - abba... -> enter
    # - another base64
    # - shabefanstoo
    
    # And from STEPS.md decoding:
    # - thispassword -> but what is it FOR?
    
    candidates = [
        # From checkerboard decode
        ("checkerboard-plaintext", checker),
        # From STEPS.md salphaseion decodes
        ("matrixsumlist", "matrixsumlist"),
        ("lastwordsbeforearchichoice", "lastwordsbeforearchichoice"),
        ("thispassword", "thispassword"),
        ("shabefourfirsthintisyourlastcommand", "shabefourfirsthintisyourlastcommand"),
        ("enter", "enter"),
        ("shabefanstoo", "shabefanstoo"),
        # Variations with prefix/suffix
    ]
    
    # Also, what about the full architect-text? It's Matrix-style monologue.
    # But maybe a SHA256 of something in it?
    
    # Let me also look at what we know:
    # - The target hash160 could be from uncompressed key: 04f4d1bb...
    # - Wait! The public key is GIVEN in README.md. Let me check:
    #   uncompressed public key: 04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559
    #
    # That's the full public key! Normally puzzles don't give this... but maybe that's a clue?
    
    print("SalPhaseIon derived candidates:")
    for name, value in candidates:
        print(f"  {name}: '{value}' (sha256={sha256hex(value)[:32]}...)")
    
    return candidates

if __name__ == '__main__':
    print()
    # Phase 2
    phase2 = test_openssl_decrypt()
    
    # Phase 3
    phase3 = test_phase3_decrypt()
    
    # Phase 3.2
    phase32 = test_phase32_decrypt()
    
    if phase32:
        arch_bytes, digits_bytes, terminal_bytes = analyze_phase32_structure(phase32)
    
    analyze_salphaseion_abba_pattern()
    
    print()
    print("=" * 60)
    print("ALL REPRODUCTION TESTS COMPLETE")
    print("=" * 60)
