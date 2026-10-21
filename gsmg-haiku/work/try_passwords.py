#!/usr/bin/env python3
"""
Try candidate passwords against unopened containers.
"""
import os
import sys
import hashlib
import base64
import binascii

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from openssl_decrypt import decrypt_openssl_aes256cbc

BASE_DIR = r"c:\gsmg-puzzle-clean"

def sha256hex(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest().lower()

def load_b64_container(filename: str) -> bytes:
    filepath = os.path.join(BASE_DIR, "files", filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        b64data = ''.join(f.read().split())
    return base64.b64decode(b64data)

def is_recognizable_plaintext(data: bytes) -> tuple[bool, float, str]:
    """
    Check if decrypted data is meaningful.
    Phase 3.2 was about 59% printable.
    Return (is_likely_valid, printable_percent, preview)
    """
    if not data:
        return False, 0.0, ""
    
    # Count printable ASCII plus CR/LF/Tab
    printable = 0
    for b in data:
        if 32 <= b < 127 or b in (9, 10, 13):
            printable += 1
    
    percent = 100.0 * printable / len(data)
    
    # Try to get a preview
    try:
        preview = data[:100].decode('ascii', errors='replace')
        preview = preview.replace('\n', '\\n').replace('\r', '\\r')
    except:
        preview = data[:50].hex()
    
    # Check if it starts with recognizable text or has structure
    starts_well = False
    if data[:1] == b'U':  # Could be Salted__ but that's ciphertext...
        pass  # No, plaintext won't have Salted__
    
    # Check for common English words
    common_words = [b'you', b'the', b'and', b'key', b'private', b'phase', b'answer', b'Salted']
    for word in common_words:
        if word in data.lower()[:200]:
            starts_well = True
            break
    
    # Phase 3.2 was binary with about 59% printable
    # But if we're getting ALL printable (>90%), that's a text container
    # Or if it's another Salted__ (60-70% random), wrong password
    
    # Actually: wrong password gives random data (~50% printable by chance)
    # Right password gives either:
    #   - Text (high printable, dictionary words)
    #   - Binary with structure (like phase3.2: had known headers)
    #   - Another encrypted container (starts with Salted__)
    
    is_valid = False
    
    # If it's another encrypted container, that's interesting!
    if len(data) >= 16 and data.startswith(b'Salted__'):
        is_valid = True
        preview = "[NESTED ENCRYPTED CONTAINER] " + preview
    
    # High printable with actual text
    if percent > 75:
        # Check for dictionary words
        words_lower = data.lower()
        if b'you' in words_lower or b'the' in words_lower or b'and' in words_lower:
            is_valid = True
    
    return is_valid, percent, preview

def try_password(encrypted_data: bytes, answer_text: str, label: str) -> dict:
    """
    Try a password. Returns dict with result info.
    """
    password = sha256hex(answer_text)
    
    try:
        plaintext = decrypt_openssl_aes256cbc(encrypted_data, password)
        valid, percent, preview = is_recognizable_plaintext(plaintext)
        
        return {
            'success': True,
            'decrypted': True,
            'answer': answer_text,
            'password': password,
            'plaintext': plaintext,
            'valid': valid,
            'printable_percent': round(percent, 1),
            'preview': preview,
            'length': len(plaintext)
        }
    except Exception as e:
        # Most likely: PKCS#7 padding failure (wrong password)
        # Note: Padding succeeds about 1/256 times randomly
        return {
            'success': False,
            'decrypted': False,
            'answer': answer_text,
            'password': password,
            'error': str(e),
            'valid': False
        }

def try_all_candidates():
    containers = [
        ('Terminal', 'terminal.b64'),
        ('SalPhaseIon short', 'salphaseion-short.b64'),
        ('Cosmic Duality', 'cosmic-duality.b64'),
    ]
    
    # Load the candidates from derived files
    with open(os.path.join(BASE_DIR, "derived", "checkerboard-plaintext.txt"), 'r') as f:
        checker_plaintext = f.read().strip()
    with open(os.path.join(BASE_DIR, "derived", "checkerboard-digits.txt"), 'r') as f:
        checker_digits = f.read().strip()
    with open(os.path.join(BASE_DIR, "derived", "architect-text.txt"), 'r') as f:
        architect = f.read().strip()
    
    candidates = [
        # From STEPS.md: explicitly decoded SalPhaseIon values
        ('matrixsumlist', 'matrixsumlist'),
        ('lastwordsbeforearchichoice', 'lastwordsbeforearchichoice'),
        ('thispassword', 'thispassword'),  # Called THISPASSWORD - very suspicious!
        ('enter', 'enter'),
        ('shabefourfirsthintisyourlastcommand', 'shabefourfirsthintisyourlastcommand'),
        ('shabefanstoo', 'shabefanstoo'),
        
        # Checkerboard output
        ('checkerboard_plaintext', checker_plaintext),
        ('checkerboard_plaintext_lower', checker_plaintext.lower()),
        ('checkerboard_digits', checker_digits),
        
        # The Phase answers themselves
        ('phase2_answer', 'causality'),
        ('phase3.2_answer', 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple'),
        
        # Variations: last answer of each phase
        ('justonesecond', 'justonesecond'),
        ('giveitjustonesecond', 'giveitjustonesecond'),
        
        # Checkerboard says: "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALF..."
        # Try the meaningful parts
        ('half', 'half'),
        ('betterhalf', 'betterhalf'),
        ('HALF', 'HALF'),
        ('BETTERHALF', 'BETTERHALF'),
        
        # Architect text ends with CIAOBELLAO
        ('ciaobella', 'ciaobella'),
        ('CIAOBELLAO', 'CIAOBELLAO'),
        
        # "four first hint is your last command" - last command was phase3.2 answer
        # But maybe it means the last solved stage's PASSWORD SHA256 itself?
        # Or "four first hint" -> 41? -> 0x29?
        
        # The public key! It's given unusually
        # Let's see: maybe parts of it are the password
    ]
    
    # Load containers
    loaded = {}
    for name, filename in containers:
        loaded[name] = load_b64_container(filename)
        print(f"{name}: {len(loaded[name])} decoded bytes")
    
    print()
    print("=" * 70)
    print("TRYING CANDIDATE PASSWORDS")
    print("=" * 70)
    print()
    
    interesting_results = []
    padding_only_successes = []
    
    for label, answer in candidates:
        for container_name, container_data in loaded.items():
            result = try_password(container_data, answer, label)
            
            if result['decrypted']:
                if result['valid']:
                    print(f"★★★ POTENTIAL MATCH ★★★")
                    print(f"  Container: {container_name}")
                    print(f"  Candidate: {label} = '{answer[:60]}'{'' if len(answer) <= 60 else '...'}")
                    print(f"  Password sha256: {result['password']}")
                    print(f"  Plaintext: {result['length']} bytes, {result['printable_percent']}% printable")
                    print(f"  Preview: {result['preview']}")
                    print()
                    interesting_results.append((container_name, label, answer, result))
                else:
                    # Padding succeeded but doesn't look meaningful
                    # Could still be valid (phase3.2 was only ~59% printable)
                    # Let's log it
                    padding_only_successes.append((container_name, label, answer, result))
    
    if padding_only_successes:
        print("=" * 70)
        print(f"PADDING-ONLY SUCCESSES (potentially false positives ~1/256):")
        print("=" * 70)
        print()
        
        for container_name, label, answer, result in padding_only_successes:
            print(f"Container: {container_name}")
            print(f"  Candidate: {label} = '{answer[:60]}'{'' if len(answer) <= 60 else '...'}")
            print(f"  Plaintext: {result['length']} bytes, {result['printable_percent']}% printable")
            print(f"  Preview: {result['preview']}")
            print()
    
    if not interesting_results and not padding_only_successes:
        print("All candidates failed. No decryption (even bad padding).")
    
    return interesting_results, padding_only_successes

def try_digits_keyspace():
    """
    The checkerboard gave us 149 digits. That's strange.
    149 is prime. Could it be related to Bitcoin keys?
    Or maybe chunks: 149 digits isn't divisible evenly by much.
    But let me think: 256 bits needs 77-78 decimal digits.
    149 is about double that.
    
    Actually wait:
    - checkerboard-plaintext: INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALF...
    - "HALF" and "BETTERHALF" - could there be TWO keys?
    - 149 digits -> maybe split into two parts?
    
    But 149 is odd. Let me just try using the digits directly as a private key candidate
    (not as container password, but actually test if it's the key itself).
    """
    print()
    print("=" * 70)
    print("CHECKING IF 149 DIGITS IS THE PRIVATE KEY DIRECTLY")
    print("=" * 70)
    print()
    
    with open(os.path.join(BASE_DIR, "derived", "checkerboard-digits.txt"), 'r') as f:
        digits = f.read().strip()
    
    print(f"Digits: {digits}")
    print(f"Length: {len(digits)}")
    print()
    
    # Could it be a decimal private key?
    # A 256-bit number has up to 78 decimal digits
    # This is 149 - about double
    
    # Try first 77 and last 72 (149=77+72)
    parts = [
        ('all', digits),
        ('first_77', digits[:77]),
        ('last_72', digits[-72:]),
        ('first_78', digits[:78]),
    ]
    
    # Actually let me call btc_check.py to test
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from btc_check import check_private_key_for_target
    
    for name, digit_str in parts:
        try:
            key_int = int(digit_str)
            if key_int > 0 and key_int < 2**256:
                print(f"Trying {name}: {digit_str[:40]}...")
                found = check_private_key_for_target(key_int, show_details=False)
                if found:
                    print(f"\n*** KEY FOUND! part={name} ***")
                    return True
            else:
                print(f"  {name}: out of range for secp256k1")
        except Exception as e:
            print(f"  {name}: error - {e}")
    
    print("\n149 digits is not the private key directly in these simple splits.")
    return False

def try_architect_text_as_passwords():
    """
    The architect text is a Matrix monologue. It ends:
    "...GOODLUCKNEVERTHELESSIREALLYHOPEYOURETHEONECIAOBELLAO"
    
    That looks like deliberate puzzle text:
    - GOOD LUCK
    - I REALLY HOPE YOU'RE THE ONE
    - CIAO BELLA O (or CIAO BELLA 0?)
    
    And earlier:
    - "SELECT FROM OVER TWENTY THREE CIPHERS SIXTEEN ENCRYPTIONS AND OR SEVEN INTERTWINED PASSWORDS"
    - "BRUTEFORCING MIGHT BE REQUIRED"
    - "FUNCTION OF THE YOU IS NOW TO RETURN TO THE SOURCE CODES"
    - "REINSERTING THE PRIME BASICS"
    """
    print()
    print("=" * 70)
    print("ANALYZING ARCHITECT TEXT FOR PASSWORD CANDIDATES")
    print("=" * 70)
    print()
    
    with open(os.path.join(BASE_DIR, "derived", "architect-text.txt"), 'r') as f:
        arch = f.read().strip()
    
    print(f"Length: {len(arch)} chars")
    print()
    
    # Look at the all-uppercase meaningful phrases
    # Actually this text is already all uppercase and concatenated
    # Let me search for key phrases from the known phases
    
    # Phrases about passwords and selection:
    # "SELECT FROM OVER TWENTY THREE CIPHERS SIXTEEN ENCRYPTIONS AND OR SEVEN INTERTWINED PASSWORDS"
    # That's:
    # - 23 ciphers
    # - 16 encryptions
    # - 7 intertwined passwords
    
    # Numbers that appear:
    # TWENTY THREE -> 23
    # SIXTEEN -> 16
    # SEVEN -> 7
    
    phrases = [
        # Capitalized name-like things we know
        'GOODLUCK',
        'CIAOBELLAO',
        'CIAOBELLA',
        'PRIMEBASICS',
        'SOURCECODES',
        'TWENTYTHREE',
        'SIXTEEN',
        'SEVEN',
        # Mixed case from puzzle convention
        'goodluck',
        'ciaobella',
        'PrimeBasics',
        'SourceCode',
        # The numbers themselves
        '23',
        '16',
        '7',
    ]
    
    return phrases

if __name__ == '__main__':
    print("=" * 70)
    print("GSMG Puzzle - Password Candidate Tester")
    print("=" * 70)
    print()
    
    # First try container passwords
    interesting, padding = try_all_candidates()
    
    # Then test if digits are the key
    try_digits_keyspace()
    
    # Get additional phrases
    more_phrases = try_architect_text_as_passwords()
    
    print()
    print("Done with first-pass candidates.")
    
    if interesting:
        print(f"\n*** {len(interesting)} potentially valid decryptions found! ***")
    elif padding:
        print(f"\n{len(padding)} decryptions with valid padding but unclear content.")
        print("Phase 3.2 was only ~59% printable so these might be real.")
    else:
        print("\nNo decryptions. Need to find actual passwords.")
