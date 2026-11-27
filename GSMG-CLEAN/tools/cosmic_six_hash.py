#!/usr/bin/env python3
"""Decrypt Cosmic Duality with one family: sha256 of the six SalPhaseIon answers.

Passphrase convention from phase 3.2: OpenSSL is given the 64-character lowercase
hex of that digest, then EVP_BytesToKey (1 iteration) with the envelope salt.
The grid also includes the raw 32-byte digest, MD5, an uppercase-hex backstop,
and a double-sha256 backstop. No other passwords.
"""
import base64
import hashlib
import json
import re
import sys
from pathlib import Path

from Crypto.Cipher import AES

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
DATA = ROOT / 'data'
OUT = ROOT / 'runs' / '2026-11-27_cosmic_six_hash'

ANSWERS = (
    'matrixsumlist',
    'lastwordsbeforearchichoice',
    'thispassword',
    'shabefourfirsthintisyourlastcommand',
    'enter',
    'shabefanstoo',
)
PHASE32_ANSWER = 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple'


def evp(password, salt, md):
    """OpenSSL EVP_BytesToKey, one iteration, AES-256 key and 16-byte IV."""
    derived = previous = b''
    while len(derived) < 48:
        previous = md(previous + password + salt).digest()
        derived += previous
    return derived[:32], derived[32:48]


def decrypt_raw(blob, password, md):
    if blob[:8] != b'Salted__':
        raise SystemExit('ciphertext is not an OpenSSL Salted__ blob')
    key, iv = evp(password, blob[8:16], md)
    return AES.new(key, AES.MODE_CBC, iv).decrypt(blob[16:])


def pkcs7_valid(plain):
    if not plain:
        return False
    pad = plain[-1]
    return 1 <= pad <= 16 and plain[-pad:] == bytes([pad]) * pad


def printable_ratio(plain):
    return sum(32 <= byte < 127 for byte in plain) / len(plain)


def preview(plain):
    chunk = plain[:200]
    if all(byte in (9, 10, 13) or 32 <= byte < 127 for byte in chunk):
        return 'text', chunk.decode('ascii')
    return 'hex', chunk.hex()


def sentence_like(plain):
    """A narrow flag for a spaced English or Dutch sentence. Not acceptance by itself."""
    chunk = plain[:400]
    if not chunk or not all(byte in (9, 10, 13) or 32 <= byte < 127 for byte in chunk[:120]):
        return False
    words = re.findall(r"[A-Za-z']{2,}", chunk.decode('ascii'))
    if len(words) < 8:
        return False
    function = {
        'the', 'and', 'of', 'to', 'in', 'is', 'that', 'this', 'for', 'with', 'as',
        'be', 'or', 'by', 'from', 'not', 'but', 'one', 'two', 'half', 'unity',
        'de', 'het', 'een', 'van', 'en', 'dat', 'die', 'voor', 'met', 'niet',
        'maar', 'zijn', 'twee', 'eenheid',
    }
    return sum(word.lower() in function for word in words) >= 3


def a0b1(text):
    bits = text.translate(str.maketrans('ab', '01'))
    return bytes(int(bits[index:index + 8], 2) for index in range(0, len(bits), 8)).decode()


def dec_int(text):
    number = int(''.join('0' if char == 'o' else str(ord(char) - 96) for char in text))
    return number.to_bytes((number.bit_length() + 7) // 8, 'big').decode()


def verify_answers():
    page = (DATA / 'salphaseion_compact_1075.txt').read_text().strip()
    if len(page) != 1075:
        raise SystemExit('SalPhaseIon compact record is not 1075 symbols')
    found = (
        a0b1(page[91:195]),
        dec_int(page[766:829]),
        dec_int(page[830:859]),
        page[860:895],
        a0b1(page[959:999]),
        page[1063:],
    )
    if found != ANSWERS:
        raise SystemExit(f'SalPhaseIon answers drifted: {found}')
    if (page[765], page[829], page[859]) != ('z', 'z', 'z'):
        raise SystemExit('the page segment separators are not z')


def verify_cosmic():
    blob = (DATA / 'locked_cosmic_duality.bin').read_bytes()
    encoded = re.sub(r'\s+', '', (DATA / 'locked_cosmic_duality.b64').read_text())
    if base64.b64decode(encoded) != blob:
        raise SystemExit('Cosmic base64 file does not match the binary')
    if blob[:8] != b'Salted__' or (len(blob) - 16) % 16 != 0:
        raise SystemExit('Cosmic blob is not a Salted__ AES ciphertext')
    return blob


def verify_phase32():
    """The phase 3.2 envelope must open with sha256-hex and EVP-SHA256, and only that."""
    phase3 = (DATA / 'phase3_plaintext.bin').read_bytes()
    start = phase3.index(b'U2FsdGVk')
    blob = base64.b64decode(re.sub(rb'\s+', b'', phase3[start:]))
    password = hashlib.sha256(PHASE32_ANSWER.encode()).hexdigest().encode()
    plain = decrypt_raw(blob, password, hashlib.sha256)
    if not pkcs7_valid(plain):
        raise SystemExit('phase 3.2 control failed PKCS#7')
    body = plain[:-plain[-1]]
    saved = (DATA / 'phase3_2_plaintext.bin').read_bytes()
    if body != saved:
        raise SystemExit('phase 3.2 control plaintext does not match the saved file')
    md5_plain = decrypt_raw(blob, password, hashlib.md5)
    if pkcs7_valid(md5_plain) and md5_plain[:-md5_plain[-1]] == saved:
        raise SystemExit('phase 3.2 also opened under MD5; the digest switch is not distinct')


def candidates():
    rows = []
    for separator_name, separator in (('none', ''), ('z', 'z')):
        for yin_name, yin in (('no', False), ('yinyang', True)):
            inner = separator.join(ANSWERS)
            if yin:
                inner += 'yinyang'
            body = inner.encode()
            single = hashlib.sha256(body).digest()
            doubled = hashlib.sha256(single).digest()
            forms = (
                ('hex-lower', single.hex().encode(), 1),
                ('raw', single, 1),
                ('hex-upper', single.hex().upper().encode(), 1),
                ('hex-lower', doubled.hex().encode(), 2),
            )
            for form, password, rounds in forms:
                for md_name, md in (('md5', hashlib.md5), ('sha256', hashlib.sha256)):
                    rows.append({
                        'separator': separator_name,
                        'yinyang': yin_name,
                        'form': form,
                        'rounds': rounds,
                        'md': md_name,
                        'inner': inner,
                        'password': password,
                    })
    return rows


def main():
    verify_answers()
    verify_phase32()
    blob = verify_cosmic()
    rows = candidates()
    if len(rows) != 32:
        raise SystemExit(f'expected 32 candidates, built {len(rows)}')
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    print(f'COSMIC bytes {len(blob)} salt {blob[8:16].hex()} ciphertext {len(blob) - 16}')
    print(f'CANDIDATES {len(rows)}')
    for index, row in enumerate(rows, 1):
        plain = decrypt_raw(blob, row['password'], hashlib.md5 if row['md'] == 'md5' else hashlib.sha256)
        valid = pkcs7_valid(plain)
        kind, shown = preview(plain)
        label = (
            f"sep={row['separator']} yin={row['yinyang']} form={row['form']} "
            f"rounds={row['rounds']} md={row['md']}"
        )
        flagged = sentence_like(plain)
        item = {
            'n': index,
            'label': label,
            'inner_sha256': hashlib.sha256(row['inner'].encode()).hexdigest(),
            'pad': 'Y' if valid else 'N',
            'pad_len': plain[-1] if valid else None,
            'printable_ascii': round(printable_ratio(plain), 4),
            'preview_kind': kind,
            'preview': shown,
            'sentence_like': flagged,
        }
        results.append(item)
        print(f"--- {index:02d} {label}")
        print(f"pad={item['pad']} printable_ascii={item['printable_ascii']:.4f} preview={kind} sentence_like={flagged}")
        print(shown)
    padding_hits = [item['label'] for item in results if item['pad'] == 'Y']
    flagged = [item['label'] for item in results if item['sentence_like']]
    summary = {
        'candidates': len(results),
        'padding_hits': padding_hits,
        'sentence_like': flagged,
        'cosmic_sha256': hashlib.sha256(blob).hexdigest(),
        'salt': blob[8:16].hex(),
    }
    (OUT / 'results.json').write_text(json.dumps({'summary': summary, 'rows': results}, indent=1) + '\n', encoding='utf-8')
    print('PADDING_HITS', len(padding_hits))
    for label in padding_hits:
        print(' PAD', label)
    print('SENTENCE_LIKE', len(flagged))
    for label in flagged:
        print(' FLAG', label)


if __name__ == '__main__':
    main()
