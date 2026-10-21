import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def derive_key_and_iv(password: str, salt: bytes) -> tuple[bytes, bytes]:
    """
    OpenSSL EVP_BytesToKey with SHA-256, 1 iteration.
    D_0 = b''
    D_1 = SHA256(D_0 + password + salt)
    D_2 = SHA256(D_1 + password + salt)
    ...
    key = first 32 bytes
    iv = next 16 bytes
    """
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

def decrypt_openssl_aes256cbc(data: bytes, password: str) -> bytes:
    """
    Decrypt data encrypted with OpenSSL AES-256-CBC format:
    Format: Salted__ + 8 byte salt + ciphertext
    Password is sha256(answer) as 64 hex characters
    """
    if not data.startswith(b'Salted__'):
        raise ValueError("Data doesn't start with Salted__")
    
    salt = data[8:16]
    ciphertext = data[16:]
    
    key, iv = derive_key_and_iv(password, salt)
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext

def decrypt_b64_file(filepath: str, password_sha256hex: str) -> bytes:
    """Decrypt a base64-encoded file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        b64data = f.read()
        # Remove all whitespace
        b64data = ''.join(b64data.split())
    data = base64.b64decode(b64data)
    return decrypt_openssl_aes256cbc(data, password_sha256hex)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python decrypt.py <b64file> <answer_text>")
        print("  Password = sha256(answer_text).hexdigest() (lowercase)")
        sys.exit(1)
    
    filepath = sys.argv[1]
    answer = sys.argv[2]
    
    # Compute password: sha256(answer) as lowercase hex
    password = hashlib.sha256(answer.encode('utf-8')).hexdigest().lower()
    
    print(f"File: {filepath}")
    print(f"Answer: {answer}")
    print(f"Password (sha256 hex): {password}")
    print()
    
    try:
        plaintext = decrypt_b64_file(filepath, password)
        print("SUCCESS: Decrypted!")
        print("=" * 60)
        try:
            text = plaintext.decode('utf-8')
            print(text)
        except UnicodeDecodeError:
            print(f"Binary data ({len(plaintext)} bytes)")
            print(f"First 200 bytes hex: {plaintext[:200].hex()}")
            printable = sum(1 for b in plaintext if 32 <= b < 127 or b in (9, 10, 13))
            print(f"Printable characters: {printable}/{len(plaintext)} ({100*printable/len(plaintext):.1f}%)")
    except Exception as e:
        print(f"FAILED: {e}")
