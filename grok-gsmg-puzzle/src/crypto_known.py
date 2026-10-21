"""Validated AES-256-CBC / EVP_BytesToKey path and the address win test.

Nothing in this module is trusted until step0_trust.py prints PASS on the
FIPS-197 / SP 800-38A vectors and on the phase-2 known plaintext.
"""

from __future__ import annotations

import hashlib
import base64
import sys
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Hash import RIPEMD160
from coincurve import PrivateKey

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import prize_gate  # noqa: E402  shared gate: Half and Better Half, both serializations

PRIZE_H160 = "a9553269572a317e39f0f518cb87c1a0ee1dbae4"
CONTROL_H160 = "751e76e8199196d454941c45d1b3a323f1433bd6"
B58 = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def evp_bytes_to_key(password: bytes, salt: bytes, md=hashlib.sha256, key_len=32, iv_len=16):
    """OpenSSL legacy EVP_BytesToKey, one iteration, the given digest."""
    need = key_len + iv_len
    d = b""
    prev = b""
    while len(d) < need:
        prev = md(prev + password + salt).digest()
        d += prev
    return d[:key_len], d[key_len:need]


def pkcs7_unpad(pt: bytes):
    if not pt:
        return None
    p = pt[-1]
    if 1 <= p <= 16 and pt[-p:] == bytes([p]) * p:
        return pt[:-p]
    return None


def decrypt_salted(raw: bytes, answer: str, md=hashlib.sha256, double=False, raw_digest=False):
    """Decrypt an OpenSSL Salted__ blob.

    Default matches the solved-container convention: password is the 64-char
    lowercase hex sha256 of `answer`, encoded as ASCII, then EVP_BytesToKey
    with SHA-256, one iteration, AES-256-CBC.

    double=True hashes the hex string once more before it becomes the password.
    raw_digest=True uses the 32-byte digest itself as the EVP password instead
    of the hex ASCII.
    """
    if raw[:8] != b"Salted__":
        raise ValueError("missing Salted__ header")
    salt, ct = raw[8:16], raw[16:]
    if len(ct) == 0 or len(ct) % 16 != 0:
        raise ValueError(f"ciphertext length {len(ct)} is not a positive multiple of 16")
    digest = hashlib.sha256(answer.encode()).digest()
    if raw_digest:
        pw = digest
        if double:
            pw = hashlib.sha256(pw).digest()
    else:
        pw = digest.hex().encode()
        if double:
            pw = hashlib.sha256(pw).hexdigest().encode()
    key, iv = evp_bytes_to_key(pw, salt, md=md)
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    return pkcs7_unpad(pt), pt


def decrypt_b64(b64text: str, answer: str, **kw):
    raw = base64.b64decode("".join(b64text.split()))
    body, full = decrypt_salted(raw, answer, **kw)
    return body, full, raw


def b64_to_raw(b64text: str) -> bytes:
    return base64.b64decode("".join(b64text.split()))


def hash160(data: bytes) -> str:
    return RIPEMD160.new(hashlib.sha256(data).digest()).hexdigest()


def pubkey_hash160s(priv32: bytes):
    if len(priv32) != 32:
        raise ValueError("private key must be 32 bytes")
    n = int.from_bytes(priv32, "big")
    if not (1 <= n < 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141):
        return None
    pk = PrivateKey(priv32)
    return {
        "compressed": hash160(pk.public_key.format(compressed=True)),
        "uncompressed": hash160(pk.public_key.format(compressed=False)),
        "pub_c": pk.public_key.format(compressed=True).hex(),
        "pub_u": pk.public_key.format(compressed=False).hex(),
    }


def is_win(priv32: bytes) -> bool:
    """Half or Better Half, compressed or uncompressed (tools/prize_gate.py).

    Half commits to its uncompressed key, but Better Half has never spent, so
    its encoding is unknown and only hash160 under both forms can gate it.
    """
    return len(priv32) == 32 and prize_gate.gate_bytes(priv32) is not None


def is_win_uncompressed(priv32: bytes) -> bool:
    """Kept for existing callers; now the full shared gate.

    It used to compare Half's uncompressed hash160 only, which silently
    rejected every correct Better Half key.
    """
    return is_win(priv32)


def b58encode(data: bytes) -> str:
    zeros = 0
    for b in data:
        if b == 0:
            zeros += 1
        else:
            break
    n = int.from_bytes(data, "big")
    out = bytearray()
    while n:
        n, r = divmod(n, 58)
        out.append(B58[r])
    out.extend(b"1" * zeros)
    return out[::-1].decode()


def b58decode(s: str) -> bytes:
    n = 0
    for ch in s.encode():
        i = B58.find(ch)
        if i < 0:
            raise ValueError(f"bad base58 char {ch!r}")
        n = n * 58 + i
    # preserve leading ones
    pad = 0
    for ch in s:
        if ch == "1":
            pad += 1
        else:
            break
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    return b"\x00" * pad + raw


def wif_from_priv(priv32: bytes, compressed: bool) -> str:
    payload = b"\x80" + priv32 + (b"\x01" if compressed else b"")
    chk = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return b58encode(payload + chk)


def priv_from_wif(wif: str):
    raw = b58decode(wif)
    chk = raw[-4:]
    payload = raw[:-4]
    if hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4] != chk:
        raise ValueError("bad WIF checksum")
    if payload[0] != 0x80:
        raise ValueError("not a mainnet WIF")
    if len(payload) == 33:
        return payload[1:], False
    if len(payload) == 34 and payload[-1] == 1:
        return payload[1:-1], True
    raise ValueError(f"unexpected WIF payload length {len(payload)}")
