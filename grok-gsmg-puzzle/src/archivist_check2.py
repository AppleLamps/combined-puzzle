#!/usr/bin/env python3
"""Archivist re-verification against the SECOND build of the handoff.

Source of truth for every extraction below is
    uploads/GSMG-handoff.md   (second build, 17 Oct 2026)
plus the poster data/puzzle.png.  Nothing is read from the
first-build handoff.  Offline only; nothing is submitted anywhere.

Usage:  python3 src/archivist_check2.py   (from any directory)
Prints one [PASS]/[FAIL] line per check and a final tally.
"""
from __future__ import annotations

import base64
import hashlib
import itertools
import re
import struct
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crypto_known import (  # noqa: E402
    PRIZE_H160,
    b64_to_raw,
    b58decode,
    decrypt_b64,
    hash160,
    pubkey_hash160s,
)
from Crypto.Cipher import AES  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "uploads" / "GSMG-handoff.md"
POSTER = ROOT / "data" / "puzzle.png"
TEXT = HANDOFF.read_text()

results = []


def check(name: str, ok: bool, detail: str = ""):
    results.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    return ok


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fence_after(marker: str, start: int = 0) -> str:
    i = TEXT.find(marker, start)
    if i < 0:
        raise SystemExit(f"marker not found: {marker!r}")
    m = re.search(r"```\n(.*?)```", TEXT[i:], flags=re.S)
    if not m:
        raise SystemExit(f"no fence after {marker!r}")
    return m.group(1)


def section(a: str, b: str) -> str:
    return TEXT[TEXT.find(a):TEXT.find(b)]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


# ---------------------------------------------------------------- extraction
HTMLS = re.findall(r"```html\n(.*?)```", TEXT, flags=re.S)


def textareas(html: str):
    return re.findall(r"<textarea[^>]*>(.*?)</textarea>", html, flags=re.S | re.I)


def compact_b64(s: str) -> str:
    return "".join(s.split())


PHASE23_AREAS = [compact_b64(x) for x in textareas(HTMLS[1])]
SAL_RAW_AREAS = textareas(HTMLS[2])
SAL_COMPACT = SAL_RAW_AREAS[0].replace(" ", "").replace("\n", "")
COSMIC_FROM_PAGE = compact_b64(SAL_RAW_AREAS[1])
BLOCKS = {
    "dbbi": SAL_COMPACT[0:91], "ab1": SAL_COMPACT[91:195], "faed": SAL_COMPACT[195:765],
    "z1": SAL_COMPACT[765:766], "lastwords": SAL_COMPACT[766:829], "z2": SAL_COMPACT[829:830],
    "thispassword": SAL_COMPACT[830:859], "z3": SAL_COMPACT[859:860],
    "sha1": SAL_COMPACT[860:895], "b64a": SAL_COMPACT[895:959], "ab2": SAL_COMPACT[959:999],
    "b64b": SAL_COMPACT[999:1063], "sha2": SAL_COMPACT[1063:1075],
}
DBBI, FAED = BLOCKS["dbbi"], BLOCKS["faed"]


def poster_grid():
    im = Image.open(POSTER)
    arr = np.array(im)
    rgb = arr[:, :, :3]
    colours = {"K": (0, 0, 0), "W": (255, 255, 255), "B": (0x3F, 0x48, 0xCC),
               "Y": (0xFF, 0xF2, 0x00), "F": (0xFE, 0xFE, 0xFE)}
    inv = {v: k for k, v in colours.items()}
    grid = []
    for r in range(14):
        row = ""
        for c in range(14):
            cell = rgb[r * 75:(r * 75) + (72 if r == 13 else 75),
                       c * 75:(c * 75) + (73 if c == 13 else 75)].reshape(-1, 3)
            packed = cell[:, 0].astype(np.int32) * 65536 + cell[:, 1].astype(np.int32) * 256 + cell[:, 2]
            vals, counts = np.unique(packed, return_counts=True)
            mode = int(vals[counts.argmax()])
            row += inv.get(((mode >> 16) & 255, (mode >> 8) & 255, mode & 255), "?")
        grid.append(row)
    return im, arr, grid


def spiral_coords(n=14):
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    r = c = di = 0
    seen, order = set(), []
    for _ in range(n * n):
        order.append((r, c)); seen.add((r, c))
        nr, nc = r + dirs[di][0], c + dirs[di][1]
        if not (0 <= nr < n and 0 <= nc < n) or (nr, nc) in seen:
            di = (di + 1) % 4
            nr, nc = r + dirs[di][0], c + dirs[di][1]
        r, c = nr, nc
    return order


GRID = None
SPIRAL_COLOURS = ""


# ------------------------------------------------------------------- section 1
def sec1():
    print("=== provenance + section 1 (goal) ===")
    blob = HANDOFF.read_bytes()
    check("second-build handoff sha256", sha256_hex(blob) ==
          "442d502f2bb65b44f1ba67ede9b9415da6a6395b98966e69d931853c10f6d7f6", sha256_hex(blob))
    check("handoff declares second build", "second build of the file (17 October 2026)" in TEXT)

    s1 = section("## 1. The goal", "## 2. Sources")
    addr = re.search(r"^address\s+(\S+)", s1, flags=re.M).group(1)
    h160_line = re.search(r"hash160\s+([0-9a-f]{40})", s1).group(1)
    unc = "".join(re.findall(r"pubkey \(unc\.\)\s+([0-9a-f]+)\s*\n\s*([0-9a-f]+)", s1)[0])
    cmp_hex = re.search(r"pubkey \(cmp\.\)\s+([0-9a-f]+)", s1).group(1)
    raw_addr = b58decode(addr)
    payload, chk = raw_addr[:-4], raw_addr[-4:]
    chk_ok = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4] == chk
    check("prize address is 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe (vanity 1GSMG)",
          addr == "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe" and addr.startswith("1GSMG"), addr)
    check("address base58check decodes to version 00 + prize hash160",
          chk_ok and payload == b"\x00" + bytes.fromhex(PRIZE_H160),
          f"payload={payload.hex()} checksum_ok={chk_ok}")
    check("section 1 hash160 line equals prize hash160", h160_line == PRIZE_H160, h160_line)
    unc_h = hash160(bytes.fromhex(unc))
    cmp_h = hash160(bytes.fromhex(cmp_hex))
    check("(a) uncompressed pubkey (65B, 04..) hashes to prize hash160",
          len(bytes.fromhex(unc)) == 65 and unc.startswith("04") and unc_h == PRIZE_H160, unc_h)
    check("(a) compressed pubkey (33B, 03..) hashes to 06bbdc66... (can never match)",
          len(bytes.fromhex(cmp_hex)) == 33 and cmp_hex.startswith("03") and
          cmp_h == "06bbdc66fda09110435c79a86656a604c2d5c69b" and cmp_h != PRIZE_H160, cmp_h)
    x_same = unc[2:66] == cmp_hex[2:]
    y = int(unc[66:], 16)
    check("(a) compressed and uncompressed are the same point (same x, y odd <-> 03)",
          x_same and y % 2 == 1, f"x={unc[2:66][:16]}... y_parity={'odd' if y % 2 else 'even'}")
    one = pubkey_hash160s((1).to_bytes(32, "big"))
    check("control privkey 1 compressed hash160 (section 1 code comment)",
          one["compressed"] == "751e76e8199196d454941c45d1b3a323f1433bd6", one["compressed"])
    check("control privkey 1 uncompressed hash160", one["uncompressed"] ==
          "91b24bf9f5288532960ac687abb035127b1d28a5", one["uncompressed"])
    check("control privkey 1 is not a win in either form",
          one["compressed"] != PRIZE_H160 and one["uncompressed"] != PRIZE_H160)


# ----------------------------------------------------------------- section 3.1
def sec31():
    print("=== section 3.1 (poster) ===")
    global GRID, SPIRAL_COLOURS
    blob = POSTER.read_bytes()
    check("poster sha256", sha256_hex(blob) ==
          "38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830", sha256_hex(blob))
    check("poster size 29931 bytes", len(blob) == 29931, str(len(blob)))
    im, arr, grid = poster_grid()
    GRID = grid
    check("poster 1048x1556 RGBA", im.mode == "RGBA" and arr.shape == (1556, 1048, 4),
          f"{im.mode} {arr.shape}")
    off, chunks = 8, []
    while off < len(blob):
        ln = struct.unpack(">I", blob[off:off + 4])[0]
        chunks.append(blob[off + 4:off + 8].decode("latin1")); off += 12 + ln
    check("PNG chunks exactly IHDR,sRGB,gAMA,pHYs,IDAT,IEND and no bytes after IEND",
          chunks == ["IHDR", "sRGB", "gAMA", "pHYs", "IDAT", "IEND"] and off == len(blob),
          ",".join(chunks))
    published = [ln for ln in fence_after("The grid as letters").splitlines() if ln.strip()]
    check("measured 14x14 grid equals section 3.1 grid byte for byte", grid == published,
          " / ".join(grid[:2]) + " ...")
    cnt = Counter("".join(grid))
    check("colour counts K86 W85 B15 Y9 F1", cnt == Counter({"K": 86, "W": 85, "B": 15, "Y": 9, "F": 1}),
          str(dict(cnt)))
    rgb = arr[:, :, :3]
    red = np.all(rgb == np.array([0xED, 0x1C, 0x24]), axis=2)
    red_rows = np.where(red.any(axis=1))[0]
    check("red divider #ED1C24 first at y=1047", len(red_rows) and int(red_rows[0]) == 1047,
          f"first_red_row={int(red_rows[0])} red_pixels={int(red.sum())}")
    cell = rgb[7 * 75:8 * 75, 4 * 75:5 * 75]
    check("off-white cell row7 col4 is flat #FEFEFE (254, not 255)",
          grid[7][4] == "F" and bool(np.all(cell == 254)), f"unique={np.unique(cell.reshape(-1,3),axis=0).tolist()}")
    nonflat = []
    for r in range(14):
        for c in range(13):  # last column is truncated by the 1048px edge
            block = rgb[r * 75:(r * 75) + (72 if r == 13 else 75), c * 75:(c + 1) * 75]
            if len(np.unique(block.reshape(-1, 3), axis=0)) > 1:
                nonflat.append((r, c))
    check("exactly 7 non-flat (rabbit) cells, all in rows 6-8 cols 6-9",
          len(nonflat) == 7 and all(6 <= r <= 8 and 6 <= c <= 9 for r, c in nonflat), str(nonflat))

    order = spiral_coords()
    seq = "".join(grid[r][c] for r, c in order)
    SPIRAL_COLOURS = seq
    bits = "".join("1" if ch in "KB" else "0" for ch in seq)
    chars = bytes(int(bits[i:i + 8], 2) for i in range(0, 192, 8))
    check("spiral (down-first, K/B=1) first 192 bits read gsmg.io/theseedisplanted",
          chars == b"gsmg.io/theseedisplanted", chars.decode())
    check("last 4 spiral bits are 0000", bits[192:] == "0000", bits[192:])
    bad = [(i, seq[i]) for i in range(192) if seq[i] in "BY" and
           (i % 8 != 7 or (seq[i] == "B") != (bits[i] == "1"))]
    check("every blue/yellow cell sits on bit 7, blue=1 yellow=0", not bad, f"mismatches={bad[:3]}")
    fidx = seq.index("F")
    check("off-white spiral index 163, a 0 bit inside 'n' of planted",
          fidx == 163 and bits[163] == "0" and chars[163 // 8:163 // 8 + 1] == b"n",
          f"index={fidx} byte={chars[163//8:163//8+1]!r}")


# ----------------------------------------------------------------- section 3.4
def sec34():
    print("=== section 3.4 (SalPhaseIon path) ===")
    s34 = section("### 3.4", "## 4. The solved chain")
    path_in_heading = re.search(r"gsmg\.io/([0-9a-f]{64})", s34).group(1)
    source = "GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
    got = sha256_hex(source.encode())
    check("(f) sha256(poster text + address) equals the SalPhaseIon path",
          got == path_in_heading == "89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32",
          f"sha256({source!r}) = {got}")
    raw = SAL_RAW_AREAS[0]
    check("side page textarea 1: 1074 single spaces, no other whitespace, 1075 compact chars",
          raw.count(" ") == 1074 and raw.count("\n") == 0 and "  " not in raw and len(SAL_COMPACT) == 1075,
          f"spaces={raw.count(' ')} compact={len(SAL_COMPACT)}")
    check("side page has SalPhaseIon and Cosmic Duality textareas",
          "SalPhaseIon" in HTMLS[2] and "Cosmic Duality" in HTMLS[2] and len(SAL_RAW_AREAS) == 2)


# ------------------------------------------------------------- sections 4.1-4.4
FIPS = [("000102030405060708090a0b0c0d0e0f", "00112233445566778899aabbccddeeff",
         "69c4e0d86a7b0430d8cdb78070b4c55a"),
        ("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f",
         "00112233445566778899aabbccddeeff", "8ea2b7ca516745bfeafc49904b496089")]
NIST_PT = ("6bc1bee22e409f96e93d7e117393172a" "ae2d8a571e03ac9c9eb76fac45af8e51"
           "30c81c46a35ce411e5fbc1191a0a52ef" "f69f2445df4f9b17ad2b417be66c3710")
NIST = [("2b7e151628aed2a6abf7158809cf4f3c",
         "7649abac8119b246cee98e9b12e9197d5086cb9b507219ee95db113a917678b2"
         "73bed6b8e3c1743b7116e69e22229516" "3ff1caa1681fac09120eca307586e1a7"),
        ("603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4",
         "f58c4c04d6e5f1ba779eabfb5f7bfbd69cfc4e967edb808d679f777bc6702c7d"
         "39f23369a9d9bacfa530e26304231461" "b2eb05e2c39be9fcda6c19078c6a9d1b")]


def sec4():
    print("=== section 4.1 (convention) ===")
    for i, (k, p, c) in enumerate(FIPS):
        key, pt = bytes.fromhex(k), bytes.fromhex(p)
        got = AES.new(key, AES.MODE_ECB).encrypt(pt)
        check(f"FIPS-197 AES-{128 if i == 0 else 256} ECB known-answer",
              got.hex() == c and AES.new(key, AES.MODE_ECB).decrypt(got) == pt, got.hex())
    for i, (k, c) in enumerate(NIST):
        key, iv, pt = bytes.fromhex(k), bytes.fromhex("000102030405060708090a0b0c0d0e0f"), bytes.fromhex(NIST_PT)
        got = AES.new(key, AES.MODE_CBC, iv).encrypt(pt)
        check(f"SP800-38A AES-{128 if i == 0 else 256}-CBC known-answer",
              got.hex() == c and AES.new(key, AES.MODE_CBC, iv).decrypt(got) == pt, got[:16].hex())

    print("=== section 4.2 (phase 2) ===")
    body2, _, raw2 = decrypt_b64(PHASE23_AREAS[0], "causality")
    check("phase 2 container decrypts with 'causality' (Salted__ header)",
          body2 is not None and raw2[:8] == b"Salted__", f"salt={raw2[8:16].hex()}")
    check("phase 2 plaintext is 648 bytes", body2 is not None and len(body2) == 648,
          f"len={len(body2) if body2 else None} sha256={sha256_hex(body2) if body2 else None}")
    fence2 = fence_after("Plaintext (648 bytes").rstrip("\n")
    check("phase 2 plaintext equals section 4.2 text byte for byte (CRLF restored)",
          body2 == fence2.replace("\n", "\r\n").encode(),
          f"sha256={sha256_hex(body2)}")

    print("=== section 4.3 (phase 3) ===")
    m = re.search(r"plain concatenation of these seven parts.*?\n```\n(.*?)```", TEXT, flags=re.S)
    parts = [re.sub(r"^\d+\.\s*", "", ln.strip()) for ln in m.group(1).splitlines() if ln.strip()]
    expected_parts = ["causality", "Safenet", "Luna", "HSM", "11110",
                      "0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262"
                      "206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854",
                      "B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1"]
    check("seven phase-3 answer parts exactly as printed", parts == expected_parts, " | ".join(parts[:5]) + " | ...")
    pw3 = "".join(parts)
    body3, _, _ = decrypt_b64(PHASE23_AREAS[1], pw3)
    check("phase 3 decrypts with the 7-part concatenation",
          body3 is not None and len(body3) == 4090,
          f"len={len(body3) if body3 else None} sha256={sha256_hex(body3) if body3 else None} pw_sha256={sha256_hex(pw3.encode())}")
    fence3 = fence_after("Plaintext (4090 bytes").rstrip("\n")
    check("phase 3 plaintext equals section 4.3 text byte for byte (CRLF restored)",
          body3 == fence3.replace("\n", "\r\n").encode(), f"sha256={sha256_hex(body3)}")

    print("=== section 4.4 (phase 3.2) ===")
    mm = re.search(rb"(U2FsdGVkX1[0-9A-Za-z+/=\r\n]+)\s*$", body3)
    p32_b64 = compact_b64(mm.group(1).decode())
    ans32 = "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
    body32, _, _ = decrypt_b64(p32_b64, ans32)
    check("phase 3.2 decrypts with jacquefresco+giveitjustonesecond+heisenbergsuncertaintyprinciple",
          body32 is not None and len(body32) == 2422,
          f"len={len(body32) if body32 else None} sha256={sha256_hex(body32) if body32 else None}")
    b64_fence = fence_after("Full plaintext as base64:")
    check("section 4.4 base64 of the full plaintext decodes to exactly those 2422 bytes",
          base64.b64decode("".join(b64_fence.split())) == body32, f"sha256={sha256_hex(body32)}")
    printable = sum(0x20 <= x <= 0x7E for x in body32)
    check("phase 3.2 plaintext is about 59% printable ASCII",
          round(100 * printable / len(body32)) == 59, f"{printable}/2422 = {100*printable/2422:.1f}%")

    sec44 = section("### 4.4", "## 5. The three locked")
    fences44 = re.findall(r"```\n(.*?)```", sec44, flags=re.S)
    ascii_txt = fences44[1].rstrip("\n")
    check("bytes 0-446 are the printed ASCII greeting ending CRLFCRLF",
          body32[:447].decode() == ascii_txt.replace("\n", "\r\n") + "\r\n\r\n" and len(body32[:447]) == 447,
          f"head={body32[:27]!r}")
    eb = body32[447:1986]
    check("bytes 447-1985: 1539 bytes, 26 distinct byte symbols, 26 distinct cp273 glyphs",
          len(eb) == 1539 and len(set(eb)) == 26 and len(set(eb.decode("cp273"))) == 26,
          f"symbols={sorted(set(eb))[:5]}...")
    speech = re.sub(r"[^A-Z]", "", fences44[2])
    # consistency: one symbol -> one Beaufort cipher letter under P=(K-C) mod 26
    key = "THEMATRIXHASYOU"
    sym2c, consistent = {}, True
    for i, b in enumerate(eb):
        c = (ord(key[i % len(key)]) - 65 - (ord(speech[i]) - 65)) % 26
        if sym2c.setdefault(b, c) != c:
            consistent = False
    plain = "".join(chr((ord(key[i % len(key)]) - 65 - sym2c[b]) % 26 + 65) for i, b in enumerate(eb))
    check("reciprocal Beaufort THEMATRIXHASYOU + one 26-symbol substitution gives the printed speech",
          consistent and len(sym2c) == 26 and plain == speech,
          f"len={len(plain)} sha256={sha256_hex(plain.encode())}")
    check("speech opens YOURLIFEISTHESUM and ends CIAOBELLAO",
          plain.startswith("YOURLIFEISTHESUMOFAREMAINDER") and plain.endswith("CIAOBELLAO"), plain[-20:])
    digits = "".join(fences44[3].split())
    check("bytes 1990-2138 are the printed 149 digits (CRLFCRLF either side)",
          body32[1986:1990] == b"\r\n\r\n" and body32[1990:2139].decode() == digits and len(digits) == 149,
          digits[:24] + "...")
    decoded = straddling(digits)
    check("straddling checkerboard (FUBCDORA.LETHINGKYMVPS/JQZXW, blanks 1,4) decodes as printed",
          decoded == fences44[4].strip() ==
          "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE",
          decoded)
    riddle = fences44[5].strip()
    check("bytes 2143-2291 are the printed riddle ending CRLFCRLF, terminal starts at 2292",
          body32[2139:2143] == b"\r\n\r\n" and body32[2143:2143 + len(riddle)].decode() == riddle
          and body32[2143 + len(riddle):2292] == b"\r\n\r\n", riddle[:40] + "...")
    return body32


def straddling(digits: str) -> str:
    alphabet = "FUBCDORA.LETHINGKYMVPS/JQZXW"
    row0 = [None] * 10
    for col, ch in zip([0, 2, 3, 5, 6, 7, 8, 9], alphabet[:8]):
        row0[col] = ch
    table = {"1": list(alphabet[8:18]), "4": list(alphabet[18:28])}
    out, i = [], 0
    while i < len(digits):
        if digits[i] in table:
            out.append(table[digits[i]][int(digits[i + 1])]); i += 2
        else:
            out.append(row0[int(digits[i])]); i += 1
    return "".join(out)


# ------------------------------------------------------------------- section 5
def sec5(body32):
    print("=== section 5 (three locked containers) ===")
    s5 = section("## 5. The three locked", "## 6. The SalPhaseIon")
    table = {}
    for name, ctlen, salt, h in re.findall(
            r"\| (Terminal|SalPhaseIon short|Cosmic Duality) \|[^|]*\| (\d+) \| `([0-9a-f]{16})` \| `([0-9a-f]{64})` \|", s5):
        table[name] = (int(ctlen), salt, h)
    term_from32 = compact_b64(body32[2292:].decode())
    sal_joined = BLOCKS["b64a"] + BLOCKS["b64b"]
    sources = {
        "Terminal": (term_from32, fence_after("Terminal:", TEXT.find("## 5. The three locked"))),
        "SalPhaseIon short": (sal_joined, fence_after("SalPhaseIon short (")),
        "Cosmic Duality": (COSMIC_FROM_PAGE, fence_after("Cosmic Duality:", TEXT.find("## 5. The three locked"))),
    }
    for name, (src, fence) in sources.items():
        fence_c = compact_b64(fence)
        raw = b64_to_raw(src)
        ctlen, salt, h = table[name]
        check(f"(e) {name}: section 5 base64 equals the source container byte for byte",
              src == fence_c, f"b64_len={len(src)}")
        check(f"(e) {name}: Salted__ salt {salt}, ciphertext {ctlen} bytes",
              raw[:8] == b"Salted__" and raw[8:16].hex() == salt and len(raw) - 16 == ctlen,
              f"raw_len={len(raw)} salt={raw[8:16].hex()} ct={len(raw)-16}")
        check(f"(e) {name}: sha256 of raw container", sha256_hex(raw) == h, sha256_hex(raw))


# --------------------------------------------------------------- sections 6.1/6.2
def decode_ab(s: str) -> bytes:
    return bytes(int(s[i:i + 8].replace("a", "0").replace("b", "1"), 2) for i in range(0, len(s), 8))


def decode_ai(s: str) -> bytes:
    n = int("".join("0" if c == "o" else str(ord(c) - 96) for c in s))
    h = format(n, "x")
    return bytes.fromhex(h.zfill(len(h) + len(h) % 2))


def sec61_62():
    print("=== section 6.1 (layout) ===")
    s61 = section("### 6.1", "### 6.2")
    wrapped = fence_after("With the spaces removed it is 1075 characters:")
    check("section 6.1 wrapped text joins to exactly the SalPhaseIon compact text",
          "".join(wrapped.split()) == SAL_COMPACT, f"len={len(SAL_COMPACT)} sha256={sha256_hex(SAL_COMPACT.encode())}")
    spans = [(0, 91), (91, 195), (195, 765), (765, 766), (766, 829), (829, 830), (830, 859),
             (859, 860), (860, 895), (895, 959), (959, 999), (999, 1063), (1063, 1075)]
    rows = re.findall(r"\| \[(\d+),(\d+)\) \| (\d+) \|", s61)
    check("span table [start,end) and lengths match the measured blocks",
          [(int(a), int(b)) for a, b, _ in rows] == spans and
          [int(n) for _, _, n in rows] == [b - a for a, b in spans], str(spans))
    check("three 'z' separators at 765, 829, 859",
          (BLOCKS["z1"], BLOCKS["z2"], BLOCKS["z3"]) == ("z", "z", "z"),
          f"{SAL_COMPACT[765]},{SAL_COMPACT[829]},{SAL_COMPACT[859]}")
    alpha = {k: "".join(sorted(set(v))) for k, v in BLOCKS.items()}
    check("block alphabets: dbbi/faed a-i, ab runs a/b, decimal runs a-i+o, b64 halves base64",
          set(DBBI) <= set("abcdefghi") and set(FAED) <= set("abcdefghi") and
          set(BLOCKS["ab1"]) == {"a", "b"} and set(BLOCKS["ab2"]) == {"a", "b"} and
          set(BLOCKS["lastwords"]) <= set("abcdefghio") and "o" in BLOCKS["lastwords"] and
          set(BLOCKS["thispassword"]) <= set("abcdefghio"),
          "; ".join(f"{k}={v}" for k, v in alpha.items()))
    check("plain-text blocks read shabefourfirsthintisyourlastcommand / shabefanstoo",
          BLOCKS["sha1"] == "shabefourfirsthintisyourlastcommand" and BLOCKS["sha2"] == "shabefanstoo",
          f"{BLOCKS['sha1']} | {BLOCKS['sha2']}")

    print("=== section 6.2 (exact decodes) ===")
    check("a/b run [91,195) decodes to matrixsumlist", decode_ab(BLOCKS["ab1"]) == b"matrixsumlist",
          repr(decode_ab(BLOCKS["ab1"])))
    check("a/b run [959,999) decodes to enter", decode_ab(BLOCKS["ab2"]) == b"enter", repr(decode_ab(BLOCKS["ab2"])))
    check("decimal run [766,829) decodes to lastwordsbeforearchichoice",
          decode_ai(BLOCKS["lastwords"]) == b"lastwordsbeforearchichoice", repr(decode_ai(BLOCKS["lastwords"])))
    check("decimal run [830,859) decodes to thispassword",
          decode_ai(BLOCKS["thispassword"]) == b"thispassword", repr(decode_ai(BLOCKS["thispassword"])))
    check("shabef reading (b=2,e=5,f=6) gives sha256ourfirsthint... / sha256anstoo",
          "sha256" + BLOCKS["sha1"][6:] == "sha256ourfirsthintisyourlastcommand" and
          "sha256" + BLOCKS["sha2"][6:] == "sha256anstoo",
          f"{'sha256'+BLOCKS['sha1'][6:]} | {'sha256'+BLOCKS['sha2'][6:]}")
    check("two base64 halves joined are the SalPhaseIon short container (128 b64 chars)",
          len(BLOCKS["b64a"] + BLOCKS["b64b"]) == 128 and
          b64_to_raw(BLOCKS["b64a"] + BLOCKS["b64b"])[8:16].hex() == "3ab585348552415d",
          BLOCKS["b64a"][:20] + "..." + BLOCKS["b64b"][-20:])


# ------------------------------------------------------------------ section 6.3
def dbbi_walk(colours: str, text: str):
    """Walk positions 1..; prime -> next colour host (B/F:1 letter, Y:2), else 1 filler."""
    idx = pos = ci = 0
    hosts, fillers = [], []
    while idx < len(text):
        if is_prime(pos + 1):
            if ci >= len(colours):
                return hosts, fillers, idx, pos + 1, False
            col = colours[ci]; ci += 1
            need = 2 if col == "Y" else 1
            hosts.append((pos + 1, col, text[idx:idx + need])); idx += need
        else:
            fillers.append(text[idx]); idx += 1
        pos += 1
    return hosts, fillers, idx, pos, idx == len(text)


def sec63_dbbi():
    print("=== section 6.3 (dbbi measured facts) ===")
    coloured = "".join(c for c in SPIRAL_COLOURS if c in "BYF")
    check("poster spiral coloured cells (B/Y/F in spiral order) are BBBBYBBBYYBBBBYBBYYBFYYBY",
          coloured == "BBBBYBBBYYBBBBYBBYYBFYYBY" and len(coloured) == 25,
          f"{coloured} counts={dict(Counter(coloured))}")
    hosts, fillers, used, endpos, exact = dbbi_walk(coloured, DBBI)
    host_counts = Counter(h[2] for h in hosts)
    check("(b) walk uses all 91 letters exactly at position 83, 23 hosts, every host starts with b",
          exact and used == 91 and endpos == 83 and len(hosts) == 23 and all(h[2].startswith("b") for h in hosts),
          f"used={used} end_position={endpos} hosts={len(hosts)}")
    check("(b) every yellow host is exactly 'be' and the off-white (F) host is 1 letter 'b'",
          all(h[2] == "be" for h in hosts if h[1] == "Y") and [h for h in hosts if h[1] == "F"] == [(73, "F", "b")],
          f"yellow={[h for h in hosts if h[1]=='Y']}")
    check("(b) hosts are 15 'b' and 8 'be'", host_counts == Counter({"b": 15, "be": 8}), str(dict(host_counts)))
    greedy, i = Counter(), 0
    while i < len(DBBI):
        if DBBI[i] == "b" and i + 1 < len(DBBI) and DBBI[i + 1] == "e":
            greedy["be"] += 1; i += 2
        elif DBBI[i] == "b":
            greedy["b"] += 1; i += 1
        else:
            i += 1
    check("(b) greedy raw count in dbbi is 15 'b' / 10 'be' (differs from the walk)",
          greedy == Counter({"b": 15, "be": 10}), str(dict(greedy)))
    check("(b) dbbi holds 25 letters 'b' in all (= poster's 25 coloured cells)",
          DBBI.count("b") == 25, str(DBBI.count("b")))
    filler_str = "".join(fillers)
    check("(b) 60 filler letters exactly as printed",
          filler_str == "difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea" and len(filler_str) == 60,
          filler_str)
    check("filler letter counts a3 b2 c8 d4 e10 f10 g10 h8 i5",
          Counter(filler_str) == Counter({"a": 3, "b": 2, "c": 8, "d": 4, "e": 10, "f": 10, "g": 10, "h": 8, "i": 5}),
          str(dict(Counter(filler_str))))
    segs = [len(x) for x in filler_str.split("b")]
    placements = sum(1 for i, j in itertools.combinations(range(60), 2)
                     if sorted((i, j - i - 1, 59 - j)) == [16, 19, 23])
    check("the two filler b's split the fillers 19|16|23; 6 of 1770 placements give {16,19,23}",
          segs == [19, 16, 23] and placements == 6, f"split={segs} placements={placements}/1770")
    host_bits = "".join("1" if h[1] in "BF" else "0" for h in hosts)
    url = b"gsmg.io/theseedisplanted"
    lsb = "".join(str(x & 1) for x in url)
    inserted = lsb[:20] + "1" + lsb[20:]
    check("(b) host bits are 11110111001111011001100", host_bits == "11110111001111011001100", host_bits)
    check("(b) URL LSBs are 111101110011110110010010; inserting 1 at position 21 gives host bits, '10' unused",
          lsb == "111101110011110110010010" and inserted[:23] == host_bits and inserted[23:] == "10",
          f"lsb={lsb} inserted={inserted} unused={inserted[23:]}")
    # continuation past 83 over the whole compact text
    idx, ci = 91, 23
    events = []
    pos = 84
    failed = None
    while pos <= 100:
        if is_prime(pos):
            col = coloured[ci]; ci += 1
            need = 2 if col == "Y" else 1
            chunk = SAL_COMPACT[idx:idx + need]
            events.append((pos, col, chunk)); idx += need
            if chunk != ("be" if col == "Y" else "b"):
                failed = (pos, col, chunk); break
        else:
            events.append((pos, "-", SAL_COMPACT[idx:idx + 1])); idx += 1
        pos += 1
    check("(b) continuing the walk past 83: pos 84-88 single chars, pos 89 (24th colour, blue) lands on 'b'",
          events[0:5] == [(84, "-", "a"), (85, "-", "b"), (86, "-", "b"), (87, "-", "a"), (88, "-", "b")]
          and (89, "B", "b") in events, str(events[:6]))
    check("(b) continuation fails at position 97 (25th colour, yellow needs 'be') on 'aa'",
          failed == (97, "Y", "aa"), f"failed={failed} events_tail={events[-3:]}")
    needed_yellow = 91 + 1  # F host would take 2 letters instead of 1
    hosts_d, fillers_d, used_d, _, exact_d = dbbi_walk(coloured.replace("F", ""), DBBI)
    ok_dropped = exact_d and len(hosts_d) == 23 and all(
        h[2] == ("be" if h[1] == "Y" else "b") for h in hosts_d)
    check("with F as yellow the walk would need 92 chars; with F dropped the parse fails",
          needed_yellow == 92 and not ok_dropped,
          f"F-as-yellow needs {needed_yellow}; dropped-F exact={exact_d} hosts_ok={ok_dropped}")
    # exhaustive: choose which 8 of the 23 hosts are yellow
    primes83 = [n for n in range(2, 84) if is_prime(n)]
    good = 0
    total = 0
    for yellow_idx in itertools.combinations(range(23), 8):
        total += 1
        yset = set(yellow_idx)
        ok, before = True, 0
        for k, p in enumerate(primes83):
            start = (p - 1) + before
            if DBBI[start] != "b" or (k in yset and (start + 1 >= 91 or DBBI[start + 1] != "e")):
                ok = False; break
            before += 1 if k in yset else 0
        good += ok
    check("exhaustive: exactly 1 of the 490,314 choices of 8 yellow hosts among 23 parses (the poster's)",
          total == 490314 and good == 1, f"parses={good} of {total}")


SQUARE = "dbifhcegaklmnopqrstuvwxyz"


def bifid_decrypt(ct: str, square: str, period: int) -> str:
    pos = {c: (i // 5, i % 5) for i, c in enumerate(square)}
    out = []
    for i in range(0, len(ct), period):
        block = ct[i:i + period]
        digits = []
        for ch in block:
            digits.extend(pos[ch])
        p = len(block)
        rows, cols = digits[:p], digits[p:]
        out.extend(square[r * 5 + c] for r, c in zip(rows, cols))
    return "".join(out)


def sec63_faed():
    print("=== section 6.3 (faed measured facts) ===")
    counts = Counter(FAED)
    check("(c) faed is 570 letters starting 'faed'", len(FAED) == 570 and FAED.startswith("faed"),
          f"len={len(FAED)} head={FAED[:12]}")
    check("(c) letter counts a54 b49 c52 d49 e69 f57 g107 h58 i75",
          counts == Counter({"a": 54, "b": 49, "c": 52, "d": 49, "e": 69, "f": 57, "g": 107, "h": 58, "i": 75}),
          str(dict(sorted(counts.items()))))
    last32 = FAED[-32:]
    check("(c) last 32 letters exactly as printed, with no e and no g",
          last32 == "bccahhbiibibbibdcbahaidhfahiihic" and "e" not in last32 and "g" not in last32, last32)
    check("(c) that suffix is maximal for {e,g}: letter 538 (1-based) is e or g",
          FAED[537] in "eg", f"faed[538]={FAED[537]!r} (1-based)")
    gprime = sum(1 for i, c in enumerate(FAED, 1) if c == "g" and is_prime(i))
    check("(c) 24 of the 107 g's sit at 1-based prime positions", gprime == 24 and counts["g"] == 107,
          f"g_prime={gprime} g_total={counts['g']}")

    seen = []
    for ch in DBBI:
        if ch not in seen:
            seen.append(ch)
    square = "".join(seen) + "".join(c for c in "abcdefghijklmnopqrstuvwxyz" if c not in seen and c != "j")
    check("Bifid square from dbbi first appearances + k..z (no j) is dbifhcegaklmnopqrstuvwxyz",
          square == SQUARE and "".join(seen) == "dbifhcega", square)
    bout = bifid_decrypt(FAED, SQUARE, 570)
    check("(c) full-period (570) Bifid decryption starts btcseedd",
          bout.startswith("btcseedd") and len(bout) == 570, bout[:24] + "...")
    check("(c) Bifid output sha256 is 15d62c82...",
          sha256_hex(bout.encode()) == "15d62c8228c1a30f3f6280fcdce2251fe616135e9de291b0c7b8a792dd8d0507",
          sha256_hex(bout.encode()))
    check("Bifid output at even (0-based) positions uses only b,c,d,e",
          set(bout[0::2]) == {"b", "c", "d", "e"}, str(sorted(set(bout[0::2]))))
    hits = [p for p in range(1, 571) if bifid_decrypt(FAED, SQUARE, p).startswith("btcseed")]
    check("(c) only period 570 (of 1..570) yields btcseed", hits == [570], str(hits))
    # calibration: orderings of the nine dbbi letters in the first nine cells
    def prefix8(sq: str) -> str:
        out = ""
        for a, b in zip(FAED[:4], FAED[285:289]):
            ia, ib = sq.index(a), sq.index(b)
            out += sq[(ia // 5) * 5 + ib // 5] + sq[(ia % 5) * 5 + ib % 5]
        return out
    good_squares = []
    for perm in itertools.permutations("dbifhcega"):
        sq = "".join(perm) + "klmnopqrstuvwxyz"
        if prefix8(sq)[:7] == "btcseed":
            good_squares.append(sq)
    check("calibration: exactly 8 of 362,880 orderings of the nine dbbi letters give btcseed, all btcseedd",
          len(good_squares) == 8 and all(prefix8(s).startswith("btcseedd") for s in good_squares),
          f"count={len(good_squares)} first9={[s[:9] for s in good_squares]}")
    paired = []
    for combo in itertools.product("abcdefghi", repeat=4):
        # first-7 output depends on FAED[:4] and the paired letters at 285:289
        out = ""
        for a, b in zip(FAED[:4], "".join(combo)):
            ia, ib = SQUARE.index(a), SQUARE.index(b)
            out += SQUARE[(ia // 5) * 5 + ib // 5] + SQUARE[(ia % 5) * 5 + ib % 5]
        if out[:7] == "btcseed":
            paired.append("".join(combo))
    check("calibration: 5 of 6,561 choices for the four paired letters at 285:289 give btcseed (actual: aied)",
          paired == ["aieb", "aied", "aief", "aieh", "aiei"] and FAED[285:289] == "aied",
          f"{paired} actual={FAED[285:289]}")

    print("=== section 6.3 (faed whole-integer arithmetic) ===")
    digits = [ord(c) - 96 for c in FAED]
    n = int("".join(map(str, digits)))
    whole = n.to_bytes(237, "big")
    check("(c) whole block as decimal integer (a=1..i=9) is 237 bytes, head 1bd5951d, tail c7bbc075",
          len(whole) == 237 and whole[:4].hex() == "1bd5951d" and whole[-4:].hex() == "c7bbc075",
          f"head={whole[:4].hex()} tail={whole[-4:].hex()} sha256={sha256_hex(whole)}")
    check("(c) 78 of the 237 bytes are printable ASCII",
          sum(0x20 <= x <= 0x7E for x in whole) == 78, str(sum(0x20 <= x <= 0x7E for x in whole)))
    n0 = int("".join(str(ord(c) - 97) for c in FAED))
    whole0 = n0.to_bytes((n0.bit_length() + 7) // 8, "big")
    check("(c) with a=0 the last four bytes are 009f4eae; 3 of 4 tail bytes non-printable either way",
          whole0[-4:].hex() == "009f4eae" and
          sum(not (0x20 <= x <= 0x7E) for x in whole[-4:]) == 3 and
          sum(not (0x20 <= x <= 0x7E) for x in whole0[-4:]) == 3,
          f"a1_tail={whole[-4:].hex()} a0_tail={whole0[-4:].hex()} a0_len={len(whole0)}")
    check("(c) 10^32 is divisible by 2^32, so the last 32 digits alone fix the last 4 bytes",
          (10 ** 32) % (2 ** 32) == 0, f"10^32 mod 2^32 = {(10**32) % (2**32)}")
    invariant = True
    for letter in "ge":
        for p in (i for i, c in enumerate(FAED) if c == letter):
            d = digits.copy(); d[p] = 0
            if int("".join(map(str, d))).to_bytes(237, "big")[-4:] != whole[-4:]:
                invariant = False
    for letter in "ge":
        d = digits.copy()
        for i, c in enumerate(FAED):
            if c == letter:
                d[i] = 0
        if int("".join(map(str, d))).to_bytes(237, "big")[-4:] != whole[-4:]:
            invariant = False
    d = digits.copy()
    for i, c in enumerate(FAED):
        if c in "ge":
            d[i] = 0
    if int("".join(map(str, d))).to_bytes(237, "big")[-4:] != whole[-4:]:
        invariant = False
    check("(c) tail c7bbc075 is invariant under zeroing any single g/e, all g, all e, or all g+e",
          invariant, f"tail={whole[-4:].hex()} (checked {counts['g']}+{counts['e']} single zeroings + 3 wholesale)")

    singles = []
    for p in range(570):
        d = digits.copy(); d[p] = 0
        tail = int("".join(map(str, d))).to_bytes(237, "big")[-4:]
        if all(0x20 <= x <= 0x7E for x in tail):
            singles.append((p + 1, tail))
    check("(c) single zeroing: only position 557 makes the last four bytes printable, giving 'yI u'",
          singles == [(557, b"yI u")], str(singles))
    # last-4 bytes depend only on the last 32 decimal digits (10^32 % 2^32 == 0, checked above)
    low = digits[538:]
    lower_hits = []
    combos = 0
    for k in range(1, 5):
        for combo in itertools.combinations(range(32), k):
            combos += 1
            d = low.copy()
            for j in combo:
                d[j] = 0
            tail = (int("".join(map(str, d))) % (2 ** 32)).to_bytes(4, "big")
            if all(97 <= x <= 122 for x in tail):
                lower_hits.append((tuple(539 + j for j in combo), tail))
    check("(c) zeroing 1-4 of the last 32 positions (41,448 ways): unique lowercase tail {551,557,561,563} -> 'szqu'",
          combos == 41448 and lower_hits == [((551, 557, 561, 563), b"szqu")],
          f"combos={combos} hits={lower_hits}")
    d = digits.copy()
    for p in (551, 557, 561, 563):
        d[p - 1] = 0
    full_tail = int("".join(map(str, d))).to_bytes(237, "big")[-4:]
    check("the {551,557,561,563} zeroing confirmed on the full 570-digit integer",
          full_tail == b"szqu", repr(full_tail))
    prefix_hits = []
    for ln in range(450, 571):
        bts = int("".join(str(ord(c) - 96) for c in FAED[:ln])).to_bytes(
            (int("".join(str(ord(c) - 96) for c in FAED[:ln])).bit_length() + 7) // 8, "big")
        if 97 <= bts[0] <= 122:
            prefix_hits.append(ln)
    check("(c) prefix lengths 450-570 whose top byte is a lowercase letter: 455,467,508,520,561",
          prefix_hits == [455, 467, 508, 520, 561], str(prefix_hits))


# ------------------------------------------------------------------- section 7.1
def sec71():
    print("=== section 7.1 (message #8446) ===")
    m = re.search(r"\[#8446\] 2023-02-23[^\n]*\n(?:\([^\n]*\)\n)?([01 ]+)", TEXT)
    groups = m.group(1).split()
    check("(d) appendix message #8446 (2023-02-23) has 161 groups of 8 bits",
          len(groups) == 161 and all(len(g) == 8 and set(g) <= {"0", "1"} for g in groups),
          f"groups={len(groups)} bits={sum(len(g) for g in groups)}")
    bits = "".join(groups)
    decoded = bytes(int(bits[::-1][i:i + 8], 2) for i in range(0, len(bits), 8)).decode()
    expected = "".join(fence_after("Reversing the whole bit string").split())
    check("(d) reversing the whole bit string and reading 8 bits/char gives the printed string exactly",
          decoded == expected, f"len={len(decoded)} sha256={sha256_hex(decoded.encode())}")
    check("(d) decoded string is the yellowblueprimes...promised text (161 chars)",
          decoded == "yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyangwewont"
                     "giveawaythepassworditsinfrontofyoureyesbutyourenotseeingitverylaststep"
                     "isatruegiveawaypromised", decoded)


def main():
    sec1()
    sec31()
    sec34()
    body32 = sec4()
    sec5(body32)
    sec61_62()
    sec63_dbbi()
    sec63_faed()
    sec71()
    nfail = sum(1 for _, ok, _ in results if not ok)
    print(f"\n=== {len(results) - nfail}/{len(results)} checks passed, {nfail} failed ===")
    if nfail:
        print("FAILED CHECKS:")
        for name, ok, detail in results:
            if not ok:
                print(f"  FAIL {name} — {detail}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
