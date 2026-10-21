import hashlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
import prize_gate  # shared gate: Half and Better Half, both serializations
from ecdsa import SigningKey, SECP256k1

def ripemd160(data: bytes) -> bytes:
    h = hashlib.new('ripemd160')
    h.update(data)
    return h.digest()

def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def hash160(data: bytes) -> bytes:
    return ripemd160(sha256(data))

def int_to_bytes(n: int, length: int) -> bytes:
    return n.to_bytes(length, byteorder='big')

def privkey_to_pubkey(k: int, compressed: bool = False) -> bytes:
    """
    Convert a private key (integer) to public key bytes using ecdsa library.
    """
    sk = SigningKey.from_secret_exponent(k, curve=SECP256k1)
    vk = sk.get_verifying_key()
    
    # Get uncompressed: 04 + x + y
    pubkey_bytes = vk.to_string('uncompressed')
    
    if compressed:
        # Compressed form: 02/03 + x
        x_bytes = pubkey_bytes[1:33]
        y_bytes = pubkey_bytes[33:]
        y = int.from_bytes(y_bytes, 'big')
        prefix = b'\x02' if y % 2 == 0 else b'\x03'
        return prefix + x_bytes
    else:
        return pubkey_bytes

def check_private_key_for_target(privkey_int: int, show_details: bool = False) -> bool:
    """
    Check if a private key corresponds to the GSMG target address.
    Target: 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
    hash160 (uncompressed): a9553269572a317e39f0f518cb87c1a0ee1dbae4
    hash160 (compressed): 06bbdc66fda09110435c79a86656a604c2d5c69b
    """
    hit = prize_gate.gate_scalar(privkey_int)  # also Better Half, missing before
    if hit:
        print(f"\n*** PRIZE MATCH {hit['matches']} ***")
        print(f"Private key hex: {privkey_int:064x}")
        return True
    TARGET_UNCOMPRESSED = bytes.fromhex('a9553269572a317e39f0f518cb87c1a0ee1dbae4')
    TARGET_COMPRESSED = bytes.fromhex('06bbdc66fda09110435c79a86656a604c2d5c69b')
    
    pubkey_uncompressed = privkey_to_pubkey(privkey_int, compressed=False)
    h160_unc = hash160(pubkey_uncompressed)
    
    if show_details:
        print(f"Private key: {privkey_int}")
        print(f"Private key hex: {privkey_int:064x}")
        print(f"Public key (uncompressed): {pubkey_uncompressed.hex()}")
        print(f"hash160 (uncompressed): {h160_unc.hex()}")
        print(f"Target (uncompressed):  {TARGET_UNCOMPRESSED.hex()}")
        
        pubkey_compressed = privkey_to_pubkey(privkey_int, compressed=True)
        h160_cmp = hash160(pubkey_compressed)
        print(f"Public key (compressed): {pubkey_compressed.hex()}")
        print(f"hash160 (compressed): {h160_cmp.hex()}")
        print(f"Target (compressed):  {TARGET_COMPRESSED.hex()}")
    
    if h160_unc == TARGET_UNCOMPRESSED:
        print(f"\n*** MATCH FOUND (uncompressed) ***")
        print(f"Private key: {privkey_int}")
        print(f"Private key hex: {privkey_int:064x}")
        return True
    
    pubkey_compressed = privkey_to_pubkey(privkey_int, compressed=True)
    h160_cmp = hash160(pubkey_compressed)
    
    if h160_cmp == TARGET_COMPRESSED:
        print(f"\n*** MATCH FOUND (compressed) ***")
        print(f"Private key: {privkey_int}")
        print(f"Private key hex: {privkey_int:064x}")
        return True
    
    return False

if __name__ == '__main__':
    # Test with known vector: private key 1
    # Should give hash160 751e76e8199196d454941c45d1b3a323f1433bd6 in compressed form
    print("=" * 60)
    print("TEST VECTOR: Private key = 1")
    print("=" * 60)
    
    test_key = 1
    EXPECTED_COMPRESSED_H160 = bytes.fromhex('751e76e8199196d454941c45d1b3a323f1433bd6')
    
    pubkey_compressed = privkey_to_pubkey(test_key, compressed=True)
    actual_h160 = hash160(pubkey_compressed)
    
    print(f"Private key: {test_key}")
    print(f"Public key (compressed): {pubkey_compressed.hex()}")
    print(f"hash160 (compressed): {actual_h160.hex()}")
    print(f"Expected:             {EXPECTED_COMPRESSED_H160.hex()}")
    
    if actual_h160 == EXPECTED_COMPRESSED_H160:
        print("\n✓ CHECKER VERIFIED: Test vector matches!")
    else:
        print("\n✗ CHECKER FAILED: Test vector does not match!")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("GSMG TARGET")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        # Check private keys from command line
        for arg in sys.argv[1:]:
            if arg.startswith('0x') or arg.startswith('0X'):
                privkey = int(arg, 16)
            else:
                privkey = int(arg)
            print()
            check_private_key_for_target(privkey, show_details=True)
    else:
        print("\nUsage: python btc_check.py <private_key> [private_key2 ...]")
        print("  Private key can be decimal or hex (with 0x prefix)")
        print()
        print("Tested and verified successfully. Ready to check candidate keys.")
