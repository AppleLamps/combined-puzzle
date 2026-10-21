"""Seeded planted controls shared by the run scripts."""
import hashlib, random
import coincurve
from Crypto.Cipher import AES
import harness as H

def planted_container(answer: bytes, seed: int, pt_len: int = 71) -> bytes:
    """A Salted__ container opened by sha256(answer) hex, holding random bytes, so only
    the padding identifies it (the hardest case the recogniser has to catch)."""
    r = random.Random(seed)
    salt = r.randbytes(8); pt = r.randbytes(pt_len)
    k, iv = H.evp(hashlib.sha256(answer).hexdigest().encode(), salt, hashlib.sha256)
    p = 16 - len(pt) % 16
    return b'Salted__' + salt + AES.new(k, AES.MODE_CBC, iv).encrypt(pt + bytes([p]) * p)

def planted_target(priv32: bytes) -> str:
    """hash160 of the compressed public key for priv32, to add to the win-test targets."""
    return H.h160(coincurve.PrivateKey(priv32).public_key.format(True))
