"""GSMG puzzle harness core library. All primary data is loaded by parsing
GSMG-PUZZLE-DOSSIER.md and the source/ HTML/image files -- nothing here is
hand-retyped from the dossier's prose.
"""
import hashlib
import base64
import re
import os
from pathlib import Path

REPO = str(Path(__file__).resolve().parent.parent.parent)
DOSSIER_PATH = os.path.join(REPO, 'GSMG-PUZZLE-DOSSIER.md')

def dossier_lines():
    with open(DOSSIER_PATH, encoding='utf-8') as f:
        return f.read().split('\n')

def fenced_blocks():
    """Return list of (start_line_1idx_content, end_line, content_lines) for every ``` fenced block."""
    lines = dossier_lines()
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        if lines[i].startswith('```'):
            start = i
            j = i + 1
            while j < n and not lines[j].startswith('```'):
                j += 1
            blocks.append((start + 2, j, lines[start+1:j]))  # 1-indexed content line range
            i = j + 1
        else:
            i += 1
    return blocks

def block_joined(idx, sep=''):
    _, _, content = fenced_blocks()[idx]
    return sep.join(content)

def block_lines(idx):
    _, _, content = fenced_blocks()[idx]
    return content

# ---- EVP_BytesToKey / AES-256-CBC per dossier section 2 ----

def evp_bytes_to_key(pw: bytes, salt: bytes, md='sha256'):
    hasher = hashlib.sha256 if md == 'sha256' else hashlib.md5
    d = b''
    prev = b''
    while len(d) < 48:
        prev = hasher(prev + pw + salt).digest()
        d += prev
    return d[:32], d[32:48]

def sha256_hex_pw(answer: str) -> bytes:
    return hashlib.sha256(answer.encode('utf-8')).hexdigest().encode('ascii')

def openssl_decrypt(raw: bytes, pw: bytes, md='sha256'):
    """raw = full 'Salted__'+salt+ciphertext bytes (already base64-decoded)."""
    from Crypto.Cipher import AES
    assert raw[:8] == b'Salted__', raw[:8]
    salt = raw[8:16]
    ct = raw[16:]
    key, iv = evp_bytes_to_key(pw, salt, md=md)
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    pad = pt[-1]
    if 1 <= pad <= 16 and pt[-pad:] == bytes([pad]) * pad:
        return pt[:-pad], pad, salt
    return None, pad, salt

def decrypt_b64_container(b64text: str, answer: str, md='sha256'):
    raw = base64.b64decode(b64text)
    pw = sha256_hex_pw(answer)
    return openssl_decrypt(raw, pw, md=md)

# ---- HASH160 / win test ----

def h160(b: bytes) -> str:
    return hashlib.new('ripemd160', hashlib.sha256(b).digest()).hexdigest()

PRIZE_H160 = 'a9553269572a317e39f0f518cb87c1a0ee1dbae4'
SENTINEL_H160 = '4bc468447fe1b048ad030a2f9a125478eabc4ed6'
COMPRESSED_TWIN_H160 = '06bbdc66fda09110435c79a86656a604c2d5c69b'

# An unattributed on-chain "neighbors, half and double" transaction funds
# four distinct uncompressed P2PKH public points. None is the prize address.
SECP256K1_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
SECP256K1_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GENERATOR = (
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
)
PRIZE_POINT = (
    0xf4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464,
    0x9c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559,
)
RELATED_ADDRESSES = {
    'minus_one': '1G1kRAFR68y6CUq1SAJMzHmjd6sEEgtVUT',
    'half': '16eEXbSuKN8tvcos1iKjdju6dAaWWRBMEs',
    'double': '1KHMK2C8uBptRz67FbrXy43yHzhZG16Hbm',
    'plus_one': '1PhXF3xVQ8Sg9FomBcmRwRbvvGfm3Y2os1',
}
_BASE58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def p2pkh_address(pubkey: bytes) -> str:
    payload = b'\x00' + bytes.fromhex(h160(pubkey))
    full = payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    value = int.from_bytes(full, 'big')
    chars = ''
    while value:
        value, rem = divmod(value, 58)
        chars = _BASE58[rem] + chars
    return _BASE58[0] * (len(full) - len(full.lstrip(b'\x00'))) + chars

def point_add(a, b):
    """Affine secp256k1 addition; None denotes the point at infinity."""
    if a is None:
        return b
    if b is None:
        return a
    x1, y1 = a
    x2, y2 = b
    if x1 == x2 and (y1 + y2) % SECP256K1_P == 0:
        return None
    if a == b:
        slope = 3 * x1 * x1 * pow(2 * y1, -1, SECP256K1_P)
    else:
        slope = (y2 - y1) * pow(x2 - x1, -1, SECP256K1_P)
    slope %= SECP256K1_P
    x3 = (slope * slope - x1 - x2) % SECP256K1_P
    return x3, (slope * (x1 - x3) - y1) % SECP256K1_P

def point_mul(point, scalar):
    """Public-point multiplication for the four observed transformations."""
    result = None
    addend = point
    while scalar:
        if scalar & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        scalar >>= 1
    return result

def uncompressed_point(point):
    x, y = point
    return b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')

def related_public_points(point=PRIZE_POINT):
    inverse_two = pow(2, -1, SECP256K1_N)
    return {
        'minus_one': point_add(point, (GENERATOR[0], -GENERATOR[1] % SECP256K1_P)),
        'half': point_mul(point, inverse_two),
        'double': point_add(point, point),
        'plus_one': point_add(point, GENERATOR),
    }

RELATED_H160 = {
    relation: h160(uncompressed_point(point))
    for relation, point in related_public_points().items()
}

def normalize_related_scalar(priv: bytes, relation: str) -> bytes:
    """Given a scalar of a related address, derive the prize scalar.

    This is only called after an exact related-address match. It does not
    narrow the search space or turn a public point into a private scalar.
    """
    d = int.from_bytes(priv, 'big')
    if not 1 <= d < SECP256K1_N:
        raise ValueError('invalid private scalar')
    inverse = {
        'minus_one': lambda d: d + 1,
        'half': lambda d: 2 * d,
        'double': lambda d: d * pow(2, -1, SECP256K1_N),
        'plus_one': lambda d: d - 1,
    }
    if relation not in inverse:
        raise ValueError('unknown relation')
    return (inverse[relation](d) % SECP256K1_N).to_bytes(32, 'big')

def classify_raw_private_key(priv: bytes, include_related=True):
    """Derive a candidate's public point once and classify exact HASH160s."""
    import coincurve
    if not isinstance(priv, bytes) or len(priv) != 32:
        return None
    try:
        pk = coincurve.PrivateKey(priv).public_key
    except Exception:
        return None
    uncompressed_hash = h160(pk.format(False))
    compressed_hash = h160(pk.format(True))
    result = {
        'prize': uncompressed_hash == PRIZE_H160 or compressed_hash == PRIZE_H160,
        'secondary_sentinel': uncompressed_hash == SENTINEL_H160 or
                              compressed_hash == SENTINEL_H160,
        'compressed_twin': uncompressed_hash == COMPRESSED_TWIN_H160 or
                           compressed_hash == COMPRESSED_TWIN_H160,
        'related': None,
    }
    if include_related:
        for relation, expected_hash in RELATED_H160.items():
            if uncompressed_hash == expected_hash:
                normalized = normalize_related_scalar(priv, relation)
                if not win_raw(normalized):
                    raise AssertionError('related scalar failed prize normalization')
                result['related'] = {
                    'relation': relation, 'address': RELATED_ADDRESSES[relation],
                    'normalized_prize_key': normalized,
                }
                break
    return result

def match_related_raw_private_key(priv: bytes):
    """Classify *uncompressed* neighbor keys; never conflate with win_raw."""
    result = classify_raw_private_key(priv)
    return result['related'] if result else None

def match_raw_private_key(priv: bytes):
    result = classify_raw_private_key(priv, include_related=False)
    if result is None:
        return None
    return {key: result[key] for key in ('prize', 'secondary_sentinel', 'compressed_twin')}

def win_raw(priv: bytes):
    # Better Half (the "sentinel" hash160) is the second prize target; it used
    # to count only as a finding, so a correct Better Half key never won.
    r = match_raw_private_key(priv)
    return bool(r and (r['prize'] or r['secondary_sentinel']))

def win_from_answer(answer_bytes: bytes):
    priv = hashlib.sha256(answer_bytes).digest()
    return win_raw(priv)

# ---- source HTML extraction ----

def read_source(relpath):
    with open(os.path.join(REPO, 'source', relpath), encoding='utf-8') as f:
        return f.read()

def extract_textarea_contents(html: str):
    """Return list of raw inner-text strings of every <textarea ...>...</textarea>."""
    return re.findall(r'<textarea[^>]*>(.*?)</textarea>', html, re.S)

def b64_join_lines(s: str) -> str:
    """Textarea base64 content split across lines -> single b64 string."""
    return ''.join(s.split())
