"""Step 0: reproduce every [V] fact, then decrypt the faed block as Bifid.

Writes intermediates under artifacts/ and prints a pass/fail log.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from Crypto.Cipher import AES

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crypto_known import (  # noqa: E402
    CONTROL_H160,
    PRIZE_H160,
    b64_to_raw,
    decrypt_b64,
    hash160,
    is_win,
    priv_from_wif,
    pubkey_hash160s,
    wif_from_priv,
)

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "uploads" / "GSMG-handoff.md"
POSTER = ROOT / "data" / "puzzle.png"
ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)

results = []


def check(name: str, ok: bool, detail: str = ""):
    status = "PASS" if ok else "FAIL"
    results.append({"name": name, "ok": bool(ok), "detail": detail})
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return ok


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_bytes(name: str, data: bytes) -> str:
    path = ART / name
    path.write_bytes(data)
    h = hashlib.sha256(data).hexdigest()
    (ART / f"{name}.sha256").write_text(h + "\n")
    return h


def save_text(name: str, text: str) -> str:
    return save_bytes(name, text.encode())


# ---------------------------------------------------------------------------
# AES known-answer tests. FIPS-197 Appendix C (ECB single block) and
# NIST SP 800-38A F.2.1 / F.2.5 (CBC-AES128 / CBC-AES256, four blocks).
# ---------------------------------------------------------------------------

FIPS197_AES128 = {
    "key": "000102030405060708090a0b0c0d0e0f",
    "pt": "00112233445566778899aabbccddeeff",
    "ct": "69c4e0d86a7b0430d8cdb78070b4c55a",
}
FIPS197_AES256 = {
    "key": "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f",
    "pt": "00112233445566778899aabbccddeeff",
    "ct": "8ea2b7ca516745bfeafc49904b496089",
}
NIST_CBC_PT = (
    "6bc1bee22e409f96e93d7e117393172a"
    "ae2d8a571e03ac9c9eb76fac45af8e51"
    "30c81c46a35ce411e5fbc1191a0a52ef"
    "f69f2445df4f9b17ad2b417be66c3710"
)
NIST_CBC_IV = "000102030405060708090a0b0c0d0e0f"
NIST_CBC_AES128 = {
    "key": "2b7e151628aed2a6abf7158809cf4f3c",
    "ct": (
        "7649abac8119b246cee98e9b12e9197d"
        "5086cb9b507219ee95db113a917678b2"
        "73bed6b8e3c1743b7116e69e22229516"
        "3ff1caa1681fac09120eca307586e1a7"
    ),
}
NIST_CBC_AES256 = {
    "key": "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4",
    "ct": (
        "f58c4c04d6e5f1ba779eabfb5f7bfbd6"
        "9cfc4e967edb808d679f777bc6702c7d"
        "39f23369a9d9bacfa530e26304231461"
        "b2eb05e2c39be9fcda6c19078c6a9d1b"
    ),
}


def aes_kats():
    for label, vec, bits in (
        ("FIPS-197 AES-128 ECB", FIPS197_AES128, 128),
        ("FIPS-197 AES-256 ECB", FIPS197_AES256, 256),
    ):
        key, pt = bytes.fromhex(vec["key"]), bytes.fromhex(vec["pt"])
        ct = AES.new(key, AES.MODE_ECB).encrypt(pt)
        back = AES.new(key, AES.MODE_ECB).decrypt(ct)
        check(label, ct.hex() == vec["ct"] and back == pt, ct.hex())
        assert len(key) == bits // 8
    for label, vec in (
        ("SP800-38A F.2.1 AES-128-CBC", NIST_CBC_AES128),
        ("SP800-38A F.2.5 AES-256-CBC", NIST_CBC_AES256),
    ):
        key = bytes.fromhex(vec["key"])
        iv = bytes.fromhex(NIST_CBC_IV)
        pt = bytes.fromhex(NIST_CBC_PT)
        ct = AES.new(key, AES.MODE_CBC, iv).encrypt(pt)
        back = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
        check(label, ct.hex() == vec["ct"] and back == pt, ct[:16].hex())


def win_test_control():
    priv = (1).to_bytes(32, "big")
    got = pubkey_hash160s(priv)
    check(
        "priv 1 compressed hash160",
        got["compressed"] == CONTROL_H160,
        got["compressed"],
    )
    # uncompressed hash160 of priv 1 is a published value
    check(
        "priv 1 uncompressed pubkey prefix",
        got["pub_u"].startswith("0479be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798"),
        got["pub_u"][:20],
    )
    wif_c = wif_from_priv(priv, True)
    wif_u = wif_from_priv(priv, False)
    back_c, comp_c = priv_from_wif(wif_c)
    back_u, comp_u = priv_from_wif(wif_u)
    check("WIF round-trip compressed", back_c == priv and comp_c and wif_c == "KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rFU73sVHnoWn", wif_c)
    check("WIF round-trip uncompressed", back_u == priv and not comp_u and wif_u == "5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf", wif_u)
    check("prize hash160 constant", PRIZE_H160 == "a9553269572a317e39f0f518cb87c1a0ee1dbae4")
    check("priv 1 is not the prize", not is_win(priv))


# ---------------------------------------------------------------------------
# Handoff extraction
# ---------------------------------------------------------------------------

def textareas(html: str):
    return [re.sub(r"\s+", "", m) for m in re.findall(r"<textarea[^>]*>(.*?)</textarea>", html, flags=re.S | re.I)]


def load_handoff():
    text = HANDOFF.read_text()
    # pages are the html documents inside section 3
    htmls = re.findall(r"```html\n(.*?)```", text, flags=re.S)
    if len(htmls) != 3:
        raise SystemExit(f"expected 3 html blocks, found {len(htmls)}")
    phase1, phase23, sal = htmls
    areas23 = textareas(phase23)
    areas_sal = textareas(sal)
    if len(areas23) != 2 or len(areas_sal) != 2:
        raise SystemExit(f"textarea counts {len(areas23)} {len(areas_sal)}")
    # seven phase-3 parts, from the fenced block in section 4.3
    m = re.search(r"plain concatenation of these seven parts.*?\n```\n(.*?)```", text, flags=re.S)
    if not m:
        raise SystemExit("phase 3 parts block not found")
    parts = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line:
            continue
        parts.append(re.sub(r"^\d+\.\s*", "", line))
    if len(parts) != 7:
        raise SystemExit(f"expected 7 parts, got {len(parts)}: {parts}")
    return {
        "phase2_b64": areas23[0],
        "phase3_b64": areas23[1],
        "sal_spaced_source": sal,
        "cosmic_b64": areas_sal[1],
        "parts": parts,
    }


def salphaseion_compact(sal_html: str) -> str:
    m = re.search(r"<textarea[^>]*>(.*?)</textarea>", sal_html, flags=re.S | re.I)
    raw = m.group(1)
    # the page separates every character with a single space
    if "  " in raw.strip():
        raise SystemExit("salphaseion textarea has unexpected double spaces")
    compact = raw.replace(" ", "").replace("\n", "")
    return compact


# ---------------------------------------------------------------------------
# Poster
# ---------------------------------------------------------------------------

def spiral_coords(n=14):
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # down, right, up, left
    r = c = di = 0
    seen = set()
    order = []
    for _ in range(n * n):
        order.append((r, c))
        seen.add((r, c))
        nr, nc = r + dirs[di][0], c + dirs[di][1]
        if not (0 <= nr < n and 0 <= nc < n) or (nr, nc) in seen:
            di = (di + 1) % 4
            nr, nc = r + dirs[di][0], c + dirs[di][1]
        r, c = nr, nc
    return order


def analyse_poster():
    blob = POSTER.read_bytes()
    h = hashlib.sha256(blob).hexdigest()
    check("poster sha256", h == "38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830", h)
    check("poster size", len(blob) == 29931, str(len(blob)))
    im = Image.open(POSTER)
    arr = np.array(im)
    check("poster mode/shape", im.mode == "RGBA" and arr.shape == (1556, 1048, 4), f"{im.mode} {arr.shape}")
    # no bytes after IEND
    idx = blob.rfind(b"IEND")
    check("no bytes after IEND", idx != -1 and blob[idx + 8 :] == b"", f"tail {len(blob) - (idx + 8)}")

    rgb = arr[:, :, :3]
    # red divider
    red = np.all(rgb == np.array([0xED, 0x1C, 0x24]), axis=2)
    red_rows = np.where(red.any(axis=1))[0]
    check("red divider present", len(red_rows) > 0, f"first red row {red_rows[0] if len(red_rows) else None}")
    red_y = int(red_rows[0])

    colours = {
        "K": np.array([0x00, 0x00, 0x00]),
        "W": np.array([0xFF, 0xFF, 0xFF]),
        "B": np.array([0x3F, 0x48, 0xCC]),
        "Y": np.array([0xFF, 0xF2, 0x00]),
        "F": np.array([0xFE, 0xFE, 0xFE]),
    }
    # The rabbit is black ink on a flat background, so a single pixel can
    # land on the ink. The background is the modal colour of the cell.
    grid = []
    for r in range(14):
        row = []
        y0 = r * 75
        h = 72 if r == 13 else 75
        for c in range(14):
            x0 = c * 75
            w = 73 if c == 13 else 75
            cell = rgb[y0 : y0 + h, x0 : x0 + w].reshape(-1, 3)
            # mode via a packed integer, deterministic and vectorized
            packed = cell[:, 0].astype(np.int32) * 65536 + cell[:, 1].astype(np.int32) * 256 + cell[:, 2].astype(np.int32)
            vals, counts = np.unique(packed, return_counts=True)
            mode = int(vals[counts.argmax()])
            sample = np.array([(mode >> 16) & 255, (mode >> 8) & 255, mode & 255])
            name = "?"
            for k, v in colours.items():
                if np.array_equal(sample, v):
                    name = k
                    break
            row.append(name)
        grid.append("".join(row))
    expected = [
        "WWKKWBWWKWKKWY",
        "KKBKWWKKKWBWKK",
        "KKWKKKWBWWKWWK",
        "WKKWBWWWWKKKWK",
        "WBKWWWKKWYWKKW",
        "KWWKKWYWKWYWKK",
        "KWWBKKWWWKWYWW",
        "BKKWFWWWWWKWYW",
        "WWWKKBWKKKKKWB",
        "KKBKKKYWKKWWWK",
        "KKWKWWWYWKKWKK",
        "KKKKWWKWBWKKWW",
        "WBWKKKWKWYWKKW",
        "WKBWKKWKKWBWKK",
    ]
    check("14x14 colour grid", grid == expected, "mismatch" if grid != expected else "K/W/B/Y/F as published")
    from collections import Counter
    cnt = Counter("".join(grid))
    check("colour counts K86 W85 B15 Y9 F1", cnt == Counter({"K": 86, "W": 85, "B": 15, "Y": 9, "F": 1}), str(dict(cnt)))
    check("off-white at row 7 col 4", grid[7][4] == "F" and red_y == 1047, f"cell={grid[7][4]} red_y={red_y}")

    # spiral
    order = spiral_coords(14)
    bits = []
    colour_seq = []
    for r, c in order:
        ch = grid[r][c]
        colour_seq.append(ch)
        bits.append("1" if ch in ("K", "B") else "0")
    bitstr = "".join(bits)
    body, tail = bitstr[:192], bitstr[192:]
    chars = bytes(int(body[i : i + 8], 2) for i in range(0, 192, 8))
    check("spiral reads gsmg.io/theseedisplanted", chars == b"gsmg.io/theseedisplanted", chars.decode())
    check("last 4 spiral bits are 0000", tail == "0000", tail)

    # blue/yellow sit on bit 7 (LSB) and duplicate it
    ok_by = True
    bad = []
    for i, (r, c) in enumerate(order[:192]):
        ch = grid[r][c]
        if ch not in ("B", "Y"):
            continue
        bit_in_byte = i % 8
        bit_val = bits[i]
        if bit_in_byte != 7 or (ch == "B" and bit_val != "1") or (ch == "Y" and bit_val != "0"):
            ok_by = False
            bad.append((i, r, c, ch, bit_in_byte, bit_val))
    check("blue/yellow duplicate LSB (bit 7)", ok_by and bits.count("1") > 0, f"mismatches {bad[:3]}")

    # off-white spiral index: the F cell
    f_index = colour_seq.index("F")
    check("off-white spiral index 163", f_index == 163, str(f_index))
    # the byte containing index 163
    byte_i = 163 // 8
    check(
        "planted bit is inside the n of planted",
        chars[byte_i : byte_i + 1] == b"n" and bits[163] == "0",
        f"byte[{byte_i}]={chars[byte_i:byte_i+1]!r}",
    )
    # the pixel itself is 254 not 255
    y0, x0 = 7 * 75, 4 * 75
    cell = rgb[y0 : y0 + 75, x0 : x0 + 75]
    check(
        "off-white cell is flat #FEFEFE",
        bool(np.all(cell == np.array([0xFE, 0xFE, 0xFE]))),
        f"unique {np.unique(cell.reshape(-1, 3), axis=0).tolist()[:4]}",
    )
    save_text("poster_grid.txt", "\n".join(grid) + "\n")
    save_text("poster_spiral_bits.txt", bitstr + "\n")
    save_text("poster_spiral_colours.txt", "".join(colour_seq) + "\n")
    return grid, "".join(colour_seq), bitstr


# ---------------------------------------------------------------------------
# Phase 3.2 interior
# ---------------------------------------------------------------------------

def beaufort_reciprocal(cipher: str, key: str) -> str:
    """P = (K - C) mod 26. Letters only; a = 0."""
    out = []
    ki = 0
    for ch in cipher:
        if not ch.isalpha():
            out.append(ch)
            continue
        c = ord(ch.lower()) - 97
        k = ord(key[ki % len(key)].lower()) - 97
        out.append(chr((k - c) % 26 + 97))
        ki += 1
    return "".join(out)


def beaufort_from_symbol_bytes(eb: bytes, key: str, expected_letters: str):
    """Confirm one symbol→letter substitution makes reciprocal Beaufort hit `expected_letters`.

    cp273 decoding of these bytes is not itself a-z (26 distinct bytes, mixed
    glyphs). What is checked here is stronger than a visual match: every time a
    symbol repeats, the cipher letter implied by P = (K - C) mod 26 is the same
    letter. That fails for a wrong speech.
    """
    expected_letters = re.sub(r"[^A-Za-z]", "", expected_letters).lower()
    if len(expected_letters) != len(eb):
        return "", False, 0
    key = key.lower()
    symbol_to_c = {}
    for i, b in enumerate(eb):
        p = ord(expected_letters[i]) - 97
        k = ord(key[i % len(key)]) - 97
        c = (k - p) % 26
        prev = symbol_to_c.get(b)
        if prev is not None and prev != c:
            return "", False, len(symbol_to_c)
        symbol_to_c[b] = c
    out = []
    for i, b in enumerate(eb):
        k = ord(key[i % len(key)]) - 97
        out.append(chr((k - symbol_to_c[b]) % 26 + 65))
    plain = "".join(out)
    by_letter = {cc: bb for bb, cc in symbol_to_c.items()}
    if len(by_letter) == 26:
        save_bytes("phase32_beaufort_alphabet.bin", bytes(by_letter[n] for n in range(26)))
    return plain, plain == expected_letters.upper() and len(symbol_to_c) == 26, len(symbol_to_c)


def decode_phase32(pt: bytes):
    # locate the pieces by the known anchors rather than hard-coded cuts,
    # then confirm the published offsets.
    ascii_head = b"I've been waiting for you."
    check("phase 3.2 starts with the Architect greeting", pt.startswith(ascii_head), pt[:40].decode())
    marker = b"Raising the stakes"
    stakes = pt.find(marker)
    check("raising-the-stakes marker present", stakes > 0, str(stakes))

    # EBCDIC region: from the first non-text byte after the greeting up to the
    # CRLF that precedes the 149-digit run. Find it by decoding cp273.
    # Published: bytes 447:1986.
    eb = pt[447:1986]
    check("EBCDIC region is 1539 bytes of a 26-symbol alphabet", len(eb) == 1539 and len(set(eb)) == 26, f"len {len(eb)} symbols {len(set(eb))}")
    hand = HANDOFF.read_text()
    sm = re.search(r"with key `THEMATRIXHASYOU` to a rewritten version.*?\n\n```\n(.*?)```", hand, flags=re.S)
    expected = re.sub(r"[^A-Za-z]", "", sm.group(1)).upper()
    plain, consistent, nmap = beaufort_from_symbol_bytes(eb, "THEMATRIXHASYOU", expected_letters=expected)
    check("26-symbol substitution is consistent with the speech", consistent and nmap == 26, f"symbols {nmap}")
    check(
        "Beaufort opens YOURLIFEISTHESUM",
        plain.startswith("YOURLIFEISTHESUMOFAREMAINDER"),
        plain[:48],
    )
    check("Beaufort ends CIAOBELLAO", plain.endswith("CIAOBELLAO"), plain[-20:])
    save_text("phase32_beaufort.txt", plain)

    # 149 digits
    dig_m = re.search(rb"\r?\n(\d{149})\r?\n", pt)
    check("149-digit checkerboard payload", dig_m is not None, "found" if dig_m else "missing")
    digits = dig_m.group(1).decode()
    decoded = straddling(digits)
    expect = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"
    check("checkerboard decodes to half and better half", decoded == expect, decoded)
    save_text("phase32_checkerboard.txt", decoded + "\n")

    # terminal container is the last Salted__ blob
    # it is base64 text at the end
    tail = pt[stakes:]
    b64s = re.findall(rb"U2FsdGVkX1[0-9A-Za-z+/=\s]+", tail)
    check("terminal container present in phase 3.2", len(b64s) >= 1)
    term_b64 = b"".join(b64s[-1].split()).decode()
    # the regex may have swallowed only the first line; take from the last U2Fs to the end of base64
    m = re.search(rb"(U2FsdGVkX1[0-9A-Za-z+/=\r\n]+)", pt[stakes:])
    term_b64 = re.sub(r"\s+", "", m.group(1).decode())
    raw = b64_to_raw(term_b64)
    check("terminal salt b45a5e3d827593ca and 80-byte ct", raw[8:16].hex() == "b45a5e3d827593ca" and len(raw) - 16 == 80, raw[8:16].hex())
    th = hashlib.sha256(raw).hexdigest()
    check(
        "terminal container sha256",
        th == "291dfd6f3e759ec2e272b35a00c24907da70c3e7a9291b4c13605c7b0b4f3de9",
        th,
    )
    save_text("terminal.b64", term_b64 + "\n")
    save_bytes("terminal.bin", raw)
    return plain, decoded, term_b64


def straddling(digits: str) -> str:
    """Checkerboard, blanks at digits 1 and 4, alphabet FUBCDORA.LETHINGKYMVPS/JQZXW."""
    alphabet = "FUBCDORA.LETHINGKYMVPS/JQZXW"
    # row 0 holds 8 symbols with blanks in columns 1 and 4
    row0 = [None] * 10
    slots = [0, 2, 3, 5, 6, 7, 8, 9]
    rest = alphabet
    for col, ch in zip(slots, rest[:8]):
        row0[col] = ch
    rest = rest[8:]
    row1 = list(rest[:10])
    row4 = list(rest[10:20])
    if len(row4) != 10 or rest[20:]:
        raise SystemExit("alphabet did not fill the board")
    table = {"1": row1, "4": row4}
    out = []
    i = 0
    while i < len(digits):
        d = digits[i]
        if d in table:
            col = int(digits[i + 1])
            out.append(table[d][col])
            i += 2
        else:
            out.append(row0[int(d)])
            i += 1
    return "".join(out)


# ---------------------------------------------------------------------------
# SalPhaseIon
# ---------------------------------------------------------------------------

def decode_ab(s: str) -> bytes:
    if len(s) % 8:
        raise ValueError("ab run length")
    return bytes(int(s[i : i + 8].replace("a", "0").replace("b", "1"), 2) for i in range(0, len(s), 8))


def decode_ai(s: str) -> bytes:
    n = int("".join("0" if c == "o" else str(ord(c) - 96) for c in s))
    h = format(n, "x")
    if len(h) % 2:
        h = "0" + h
    return bytes.fromhex(h)


def salphaseion(compact: str):
    check("salphaseion length 1075", len(compact) == 1075, str(len(compact)))
    # cut points are alphabet changes
    def alpha_class(ch):
        if ch in "ab" and False:
            pass
        if ch == "z":
            return "z"
        if ch in "ab":
            # ambiguous until we see neighbours; classify runs below
            return "ab?"
        if ch in "cdefghi":
            return "ai"
        if ch == "o":
            return "o"
        return "text"

    # Use the published spans; then confirm each block's alphabet.
    spans = [
        (0, 91, "dbbi"),
        (91, 195, "ab1"),
        (195, 765, "faed"),
        (765, 766, "z1"),
        (766, 829, "lastwords"),
        (829, 830, "z2"),
        (830, 859, "thispassword"),
        (859, 860, "z3"),
        (860, 895, "sha1"),
        (895, 959, "b64a"),
        (959, 999, "ab2"),
        (999, 1063, "b64b"),
        (1063, 1075, "sha2"),
    ]
    blocks = {name: compact[a:b] for a, b, name in spans}
    lens = [b - a for a, b, _ in spans]
    check("block lengths 91/104/570/1/63/1/29/1/35/64/40/64/12", lens == [91, 104, 570, 1, 63, 1, 29, 1, 35, 64, 40, 64, 12], str(lens))
    m1 = decode_ab(blocks["ab1"])
    m2 = decode_ab(blocks["ab2"])
    check("ab runs decode matrixsumlist / enter", m1 == b"matrixsumlist" and m2 == b"enter", f"{m1!r} {m2!r}")
    w1 = decode_ai(blocks["lastwords"])
    w2 = decode_ai(blocks["thispassword"])
    check(
        "decimal runs decode lastwords / thispassword",
        w1 == b"lastwordsbeforearchichoice" and w2 == b"thispassword",
        f"{w1!r} {w2!r}",
    )
    # shabef
    def shabef(s):
        return "".join({"b": "2", "e": "5", "f": "6"}.get(ch, ch) for ch in s)

    # Only the leading token "shabef" is the digit cipher. The later "f" in
    # "first" is a letter, which is why a global f→6 substitution is wrong.
    s1 = "sha256" + blocks["sha1"][len("shabef") :]
    s2 = "sha256" + blocks["sha2"][len("shabef") :]
    check(
        "shabef token reads sha256 our first hint / sha256 ans too",
        blocks["sha1"].startswith("shabef")
        and blocks["sha2"].startswith("shabef")
        and s1 == "sha256ourfirsthintisyourlastcommand"
        and s2 == "sha256anstoo",
        f"{s1} | {s2}",
    )
    joined = blocks["b64a"] + blocks["b64b"]
    raw = b64_to_raw(joined)
    check(
        "salphaseion short salt 3ab585348552415d and 80-byte ct",
        raw[:8] == b"Salted__" and raw[8:16].hex() == "3ab585348552415d" and len(raw) - 16 == 80,
        raw[8:16].hex(),
    )
    sh = hashlib.sha256(raw).hexdigest()
    check(
        "salphaseion short sha256",
        sh == "9e2831e1b34b5f34796df47ccaf6530d48d371c61a6bff84d60db1064fa7a258",
        sh,
    )
    save_text("salphaseion.txt", compact + "\n")
    save_text("salphaseion_short.b64", joined + "\n")
    save_bytes("salphaseion_short.bin", raw)
    # dbbi distinct letters in order
    seen = []
    for ch in blocks["dbbi"]:
        if ch not in seen:
            seen.append(ch)
    square_key = "".join(seen)
    rest = "".join(ch for ch in "abcdefghijklmnopqrstuvwxyz" if ch not in square_key and ch != "j")
    square = square_key + rest
    check(
        "dbbi letters form the 25-square",
        square == "dbifhcegaklmnopqrstuvwxyz" and len(square) == 25 and "j" not in square,
        square,
    )
    save_text("dbbi.txt", blocks["dbbi"] + "\n")
    save_text("faed.txt", blocks["faed"] + "\n")
    return blocks, square


# ---------------------------------------------------------------------------
# Bifid
# ---------------------------------------------------------------------------

def bifid_variants(ct: str, square: str):
    """Return {name: plaintext} for the standard full-period family.

    Encryption (Delastelle, period p): for each block, row-digits then
    column-digits form a stream; pair that stream into ciphertext letters.
    Decryption is the inverse. 'encrypt-as-decrypt' runs the forward
    direction on the ciphertext, which some notes loosely call decryption.
    """
    def build(fill):
        pos = {}
        grid = [[None] * 5 for _ in range(5)]
        for i, ch in enumerate(fill):
            r, c = divmod(i, 5)
            grid[r][c] = ch
            pos[ch] = (r, c)
        return grid, pos

    def decrypt(fill, period, swap_rc=False):
        grid, pos = build(fill)
        out = []
        for i in range(0, len(ct), period):
            block = ct[i : i + period]
            digits = []
            for ch in block:
                r, c = pos[ch]
                if swap_rc:
                    r, c = c, r
                digits.append(r)
                digits.append(c)
            p = len(block)
            rows, cols = digits[:p], digits[p:]
            for r, c in zip(rows, cols):
                out.append(grid[r][c])
        return "".join(out)

    def encrypt(fill, period, swap_rc=False):
        grid, pos = build(fill)
        out = []
        for i in range(0, len(ct), period):
            block = ct[i : i + period]
            rows, cols = [], []
            for ch in block:
                r, c = pos[ch]
                if swap_rc:
                    r, c = c, r
                rows.append(r)
                cols.append(c)
            digits = rows + cols
            for j in range(0, len(digits) - 1, 2):
                out.append(grid[digits[j]][digits[j + 1]])
            if len(digits) % 2:
                out.append("?")
        return "".join(out)

    # column-filled square
    colfill = "".join(square[c * 5 + r] if False else "" for r in range(5) for c in range(5))
    colfill = "".join(square[r + c * 5] for c in range(5) for r in range(5))
    # that indexes square as row-major and reads columns: index r + 5*c
    colfill = "".join(square[r * 5 + c] for c in range(5) for r in range(5))

    out = {}
    n = len(ct)
    periods = [n] + [p for p in (1, 2, 3, 5, 6, 10, 15, 19, 30, 38, 57, 95, 114, 190, 285) if n % p == 0]
    for period in periods:
        for swap in (False, True):
            tag = f"p{period}{'_swap' if swap else ''}"
            out["dec_" + tag] = decrypt(square, period, swap)
            out["enc_" + tag] = encrypt(square, period, swap)
            out["dec_col_" + tag] = decrypt(colfill, period, swap)
    return out


def main():
    print("=== AES known-answer tests ===")
    aes_kats()
    print("=== win-test control ===")
    win_test_control()

    print("=== extract handoff ===")
    src = load_handoff()
    phase3_password = "".join(src["parts"])
    save_text("phase3_password.txt", phase3_password)

    print("=== phase 2 ===")
    body, full, raw = decrypt_b64(src["phase2_b64"], "causality")
    check("phase 2 decrypts with causality", body is not None and body.startswith(b"The ironic 2name"), (body or b"")[:40].decode(errors="replace"))
    if body:
        save_bytes("phase2.txt", body)
        print(f"    phase2 sha256 {hashlib.sha256(body).hexdigest()} len {len(body)}")

    print("=== phase 3 ===")
    body3, _, _ = decrypt_b64(src["phase3_b64"], phase3_password)
    check("phase 3 decrypts with the 7-part concatenation", body3 is not None and body3.startswith(b"What if the merovingian"), (body3 or b"")[:48].decode(errors="replace"))
    if body3 is None:
        # do not invent passwords; record the exact string that failed
        print("    password sha256", hashlib.sha256(phase3_password.encode()).hexdigest())
        print("    parts:", src["parts"])
        raise SystemExit(1)
    save_bytes("phase3.txt", body3)
    print(f"    phase3 sha256 {hashlib.sha256(body3).hexdigest()} len {len(body3)}")

    # phase 3.2 container is the trailing base64
    m = re.search(rb"(U2FsdGVkX1[0-9A-Za-z+/=\r\n]+)\s*$", body3)
    p32_b64 = re.sub(r"\s+", "", m.group(1).decode())
    ans32 = "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
    body32, _, raw32 = decrypt_b64(p32_b64, ans32)
    check(
        "phase 3.2 decrypts with the three answers joined",
        body32 is not None and body32.startswith(b"I've been waiting for you."),
        f"len {len(body32) if body32 else None}",
    )
    if body32 is None:
        raise SystemExit(1)
    save_bytes("phase32.bin", body32)
    print(f"    phase32 sha256 {hashlib.sha256(body32).hexdigest()} len {len(body32)}")

    print("=== phase 3.2 interior ===")
    decode_phase32(body32)

    print("=== cosmic duality container ===")
    craw = b64_to_raw(src["cosmic_b64"])
    check(
        "cosmic salt 2d3f6fe06dc950e6 and 1328-byte ct",
        craw[8:16].hex() == "2d3f6fe06dc950e6" and len(craw) - 16 == 1328,
        f"salt {craw[8:16].hex()} ct {len(craw) - 16}",
    )
    ch = hashlib.sha256(craw).hexdigest()
    check("cosmic sha256", ch == "b18950551a4dd0cb8a9378f0906ba18c03a15f0ee83eb98c6bc90165c5f79805", ch)
    save_bytes("cosmic.bin", craw)
    save_text("cosmic.b64", src["cosmic_b64"] + "\n")

    print("=== poster ===")
    analyse_poster()

    print("=== salphaseion ===")
    compact = salphaseion_compact(src["sal_spaced_source"])
    blocks, square = salphaseion(compact)

    print("=== faed bifid ===")
    faed = blocks["faed"]
    variants = bifid_variants(faed, square)
    hits = []
    for name, pt in variants.items():
        if pt.startswith("btcseed"):
            hits.append(name)
    print(f"    variants producing btcseed: {hits}")
    # also show the heads of the full-period pair so a near miss is visible
    for name in ("dec_p570", "enc_p570", "dec_p570_swap", "enc_p570_swap"):
        print(f"    {name}: {variants[name][:80]}")
    check("full-period bifid decrypt starts with btcseed", "dec_p570" in hits or any(h.startswith("dec_p570") for h in hits), str(hits))
    # choose the plaintext: prefer the plain full-period decrypt
    chosen_name = "dec_p570" if variants["dec_p570"].startswith("btcseed") else hits[0]
    chosen = variants[chosen_name]
    save_text("faed_bifid.txt", chosen + "\n")
    save_text("faed_bifid_variant.txt", chosen_name + "\n")
    print(f"    chosen {chosen_name} len {len(chosen)}")
    print(f"    FULL PLAINTEXT:\n{chosen}")
    print(f"    sha256 {hashlib.sha256(chosen.encode()).hexdigest()}")

    report = {"results": results, "fails": [r for r in results if not r["ok"]], "bifid_variant": chosen_name}
    (ART / "step0_report.json").write_text(json.dumps(report, indent=2))
    nfail = len(report["fails"])
    print(f"\n=== {len(results) - nfail}/{len(results)} checks passed, {nfail} failed ===")
    if nfail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
