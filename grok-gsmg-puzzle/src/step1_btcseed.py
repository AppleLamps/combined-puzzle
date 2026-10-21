"""Treat the faed Bifid plaintext as data and test it against the prize address.

One hypothesis per section. Every primary password is appended to
artifacts/attempts.jsonl with the container, the KDF, and the exact string.
A hit is a win-test match or structured plaintext. A 1-byte PKCS#7 pad is logged
as a pad-only near miss and is not a hit.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crypto_known import (  # noqa: E402
    PRIZE_H160,
    b64_to_raw,
    decrypt_salted,
    hash160,
    is_win,
    pubkey_hash160s,
    wif_from_priv,
)

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"
LOG = ART / "attempts.jsonl"
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# BIP39 English wordlist is embedded only if the mnemonic package is present.
# The derivation below is checked against the BIP39 and BIP32 published vectors
# before any puzzle candidate is put through it.


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def load_containers():
    sal = (ART / "salphaseion_short.bin").read_bytes()
    term = (ART / "terminal.bin").read_bytes()
    cosmic = (ART / "cosmic.bin").read_bytes()
    out = {
        "terminal": term,
        "salphaseion_short": sal,
        "cosmic": cosmic,
    }
    # Yinyang: the two 64-char base64 halves are the two 48-byte halves.
    h1, h2 = sal[:48], sal[48:]
    def blocks(b, n=16):
        return [b[i : i + n] for i in range(0, len(b), n)]
    A, B = blocks(h1), blocks(h2)
    inter = b"".join(x for pair in zip(A, B) for x in pair)
    assert inter[:8] == b"Salted__" and len(inter) == 96
    out["sal_yinyang_blocks"] = inter
    # byte-wise interleave of the ciphertext only, header kept from h1
    ct1, ct2 = h1[16:], h2  # 32 bytes of ct in the first half, 48 in the second
    # The raw container's ciphertext is 80 bytes: first 32 live in h1, rest in h2.
    ct = sal[16:]
    half = 40
    a, b = ct[:half], ct[half:]
    woven = bytes(x for pair in zip(a, b) for x in pair)
    out["sal_yinyang_ct_bytes"] = sal[:16] + woven
    # character-wise interleave of the two base64 halves
    b64 = (ART / "salphaseion_short.b64").read_text().strip()
    left, right = b64[:64], b64[64:]
    char_i = "".join(x for pair in zip(left, right) for x in pair)
    try:
        raw = b64_to_raw(char_i)
        if raw[:8] == b"Salted__" and (len(raw) - 16) % 16 == 0:
            out["sal_yinyang_b64_chars"] = raw
    except Exception:
        pass
    # the two 80-byte ciphertexts as halves: XOR, header from each salt
    if len(term) == len(sal):
        xct = bytes(x ^ y for x, y in zip(term[16:], sal[16:]))
        out["xor_ct_salt_terminal"] = term[:16] + xct
        out["xor_ct_salt_salphaseion"] = sal[:16] + xct
        # block interleave of the two full containers
        TA, SA = blocks(term), blocks(sal)
        out["term_sal_block_ab"] = b"".join(x for pair in zip(TA, SA) for x in pair)
        out["term_sal_block_ba"] = b"".join(x for pair in zip(SA, TA) for x in pair)
    return out


def classify(pt: bytes):
    if pt is None:
        return "no-pad"
    if not pt:
        return "empty"
    printable = sum(32 <= b < 127 or b in (9, 10, 13) for b in pt) / len(pt)
    text = pt.decode("latin-1")
    structured = False
    reason = []
    # one leading '{' is 1/256 of random bodies; JSON and PEM are also mostly printable
    if pt.startswith(b"Salted__") or (pt.startswith((b"{", b"-----")) and printable >= 0.8):
        structured = True
        reason.append("magic")
    if len(pt) in (32, 64) and all(chr(b) in "0123456789abcdefABCDEF" for b in pt):
        structured = True
        reason.append("hex-key-length")
    letters = sum(chr(b).isalpha() for b in pt)
    if len(pt) >= 16 and printable >= 0.9 and letters >= len(pt) * 0.5:
        structured = True
        reason.append(f"prose {printable:.2f}")
    # a run of 8 lowercase words is the shape of a mnemonic fragment
    if printable >= 0.95 and text.count(" ") >= 11:
        structured = True
        reason.append("spaced-words")
    return ("structured:" + ",".join(reason)) if structured else f"opaque p={printable:.2f} n={len(pt)}"


def kdf_modes(answer: str):
    """The solved-container convention plus the raw-digest and double-hash variants."""
    digest = sha256(answer.encode())
    hexpw = digest.hex().encode()
    return {
        "std-hex": hexpw,                              # sha256(answer) as 64 hex chars
        "double-hex": sha256(hexpw).hex().encode(),
        "raw-digest": digest,                          # 32-byte digest as the EVP password
        "double-raw": sha256(digest),
        "direct": answer.encode(),                     # no outer hash; the string is the password
    }


def attempt(containers, label, answer, logf, wins, hits):
    modes = kdf_modes(answer)
    for cname, raw in containers.items():
        if raw[:8] != b"Salted__":
            continue
        for mode, pw in modes.items():
            # decrypt_salted re-hashes when given an answer. Here the password
            # bytes are already the EVP password, so call the primitive directly.
            body, full = decrypt_with_password(raw, pw)
            kind = "no-pad" if body is None else classify(body)
            pad_only = False
            if body is not None and full is not None and len(full) >= 1:
                p = full[-1]
                pad_only = p == 1 and body is not None and len(full) == len(body) + 1
            rec = {
                "container": cname,
                "kdf": mode,
                "label": label,
                "answer": answer if len(answer) < 400 else answer[:80] + f"...<{len(answer)}>",
                "answer_sha256": hashlib.sha256(answer.encode()).hexdigest(),
                "result": "pad-only-1" if (body is not None and pad_only and not kind.startswith("structured")) else kind,
            }
            # keep the log reproducible but don't store every opaque 1-byte pad body
            if body is not None and (kind.startswith("structured") or not pad_only):
                rec["plaintext_hex"] = body.hex()
                rec["plaintext_sha256"] = hashlib.sha256(body).hexdigest()
            logf.write(json.dumps(rec) + "\n")
            if kind.startswith("structured"):
                hits.append(rec | {"plaintext": body})
                print(f"  HIT {cname} {mode} {label}: {kind}")
                print(f"      {body[:200]!r}")
            elif body is not None and not pad_only:
                # pad length >= 2, or a pad that wasn't a single 0x01. Exact bytes.
                print(f"  NEAR {cname} {mode} {label}: pad-valid {kind}")
                print(f"      hex {body.hex()}")


def decrypt_with_password(raw: bytes, password: bytes):
    from crypto_known import evp_bytes_to_key, pkcs7_unpad
    from Crypto.Cipher import AES
    salt, ct = raw[8:16], raw[16:]
    key, iv = evp_bytes_to_key(password, salt)
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    return pkcs7_unpad(pt), pt


def win_key(priv: bytes, label, found):
    if len(priv) != 32:
        return False
    got = pubkey_hash160s(priv)
    if got is None:
        return False
    ok = PRIZE_H160 in (got["compressed"], got["uncompressed"])
    if ok:
        which = "compressed" if got["compressed"] == PRIZE_H160 else "uncompressed"
        found.append((label, priv, which, got))
        print(f"  WIN {label} via {which}")
        print(f"      priv {priv.hex()}")
    return ok


def windows(buf: bytes, size=32):
    if len(buf) < size:
        return
    for i in range(0, len(buf) - size + 1):
        yield i, buf[i : i + size]


def base_n_decode(text: str, alphabet: str) -> bytes:
    base = len(alphabet)
    n = 0
    for ch in text:
        n = n * base + alphabet.index(ch)
    if n == 0:
        return b"\x00"
    length = (n.bit_length() + 7) // 8
    return n.to_bytes(length, "big")


def bip32_ckd(k: bytes, c: bytes, index: int) -> tuple[bytes, bytes]:
    if index >= 0x80000000:
        data = b"\x00" + k + index.to_bytes(4, "big")
    else:
        pub = pubkey_hash160s(k)  # validates range
        if pub is None:
            raise ValueError("bad key")
        data = bytes.fromhex(pub["pub_c"]) + index.to_bytes(4, "big")
    I = hmac.new(c, data, hashlib.sha512).digest()
    il, ir = I[:32], I[32:]
    child = (int.from_bytes(il, "big") + int.from_bytes(k, "big")) % N
    if child == 0 or int.from_bytes(il, "big") >= N:
        raise ValueError("invalid child")
    return child.to_bytes(32, "big"), ir


def bip32_master(seed: bytes):
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    return I[:32], I[32:]


def derive_path(seed: bytes, path: str) -> bytes:
    k, c = bip32_master(seed)
    if path in ("m", ""):
        return k
    for part in path.lstrip("m/").split("/"):
        hardened = part.endswith("'") or part.endswith("h")
        idx = int(part.rstrip("'h"))
        if hardened:
            idx += 0x80000000
        k, c = bip32_ckd(k, c, idx)
    return k


def self_test_bip32():
    # BIP32 test vector 1
    seed = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    k, c = bip32_master(seed)
    ok = (
        k.hex() == "e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35"
        and c.hex() == "873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d508"
    )
    k0 = derive_path(seed, "m/0'")
    # first hardened child from the spec
    ok = ok and k0.hex() == "edb2e14f9ee77d26dd93b4ecede8d16ed408ce149b6cd80b0715a2d911a0afea"
    print(f"[PASS] BIP32 test vector 1" if ok else f"[FAIL] BIP32 {k.hex()} {k0.hex()}")
    if not ok:
        raise SystemExit(1)


def bip39_seed(mnemonic: str, passphrase: str = "") -> bytes:
    return hashlib.pbkdf2_hmac("sha512", mnemonic.encode(), ("mnemonic" + passphrase).encode(), 2048)


def self_test_bip39():
    # official vector: 128 zero bits
    try:
        from mnemonic import Mnemonic
    except ImportError:
        print("[SKIP] mnemonic package not installed")
        return None
    m = Mnemonic("english")
    words = m.to_mnemonic(b"\x00" * 16)
    if words != "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about":
        print("[FAIL] BIP39 mnemonic", words)
        raise SystemExit(1)
    seed = bip39_seed(words)
    # BIP39 zero-entropy vector. Cross-checked against the mnemonic package,
    # which computes the same PBKDF2-HMAC-SHA512 independently.
    expect = "5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc19a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4"
    agree = seed == m.to_seed(words) and seed.hex() == expect
    print("[PASS] BIP39 zero-entropy vector" if agree else "[FAIL] BIP39 seed " + seed.hex())
    if not agree:
        raise SystemExit(1)
    return m


def scan_keys(buf: bytes, label: str, found: list):
    n = 0
    if len(buf) == 32:
        win_key(buf, label, found)
        n += 1
    for i, w in windows(buf):
        if win_key(w, f"{label}[{i}:{i+32}]", found):
            pass
        n += 1
    # also the sha256 of the whole buffer as a key
    win_key(sha256(buf), f"sha256({label})", found)
    n += 1
    return n


def yellowblue(dbbi: str, colour_seq: str):
    """The handoff's prime walk. Returns the variant that consumes both streams."""
    def is_prime(n):
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        d = 3
        while d * d <= n:
            if n % d == 0:
                return False
            d += 2
        return True

    def run(start, one_is_special=False):
        i = 0
        ci = 0
        fillers = []
        chunks = []
        pos = start
        while i < len(dbbi) and ci < len(colour_seq):
            prime = is_prime(pos) or (one_is_special and pos == 1)
            if prime:
                col = colour_seq[ci]
                nlet = 2 if col == "Y" else 1
                if i + nlet > len(dbbi):
                    break
                chunks.append((pos, col, dbbi[i : i + nlet]))
                i += nlet
                ci += 1
            else:
                fillers.append(dbbi[i])
                i += 1
            pos += 1
        return {
            "start": start,
            "pos_end": pos - 1,
            "letters_used": i,
            "colours_used": ci,
            "fillers": "".join(fillers),
            "chunks": chunks,
        }

    runs = [run(0), run(1), run(1, True), run(0, True)]
    return runs


def matrix_sums(grid_rows: list[str]):
    """A few natural sum-lists. Not the prior team's 1,550-list sweep."""
    encs = {
        "bit": {c: (1 if c in "KB" else 0) for c in "KWBYF"},
        "kwbyf": {"K": 0, "W": 1, "B": 2, "Y": 3, "F": 4},
    }
    out = {}
    for name, enc in encs.items():
        M = [[enc[ch] for ch in row] for row in grid_rows]
        rows = [sum(r) for r in M]
        cols = [sum(M[r][c] for r in range(14)) for c in range(14)]
        main = sum(M[i][i] for i in range(14))
        anti = sum(M[i][13 - i] for i in range(14))
        total = sum(rows)
        out[name] = {
            "rows": rows,
            "cols": cols,
            "main": main,
            "anti": anti,
            "total": total,
            "rowdigits": "".join(str(n) for n in rows),
            "coldigits": "".join(str(n) for n in cols),
            "joined": "".join(str(n) for n in rows + cols + [main, anti, total]),
        }
    return out


def main():
    self_test_bip32()
    mnemonic = self_test_bip39()
    containers = load_containers()
    print("containers:")
    for name, raw in containers.items():
        print(f"  {name:24} {len(raw):4} bytes salt {raw[8:16].hex()} sha256 {hashlib.sha256(raw).hexdigest()[:16]}")

    # published pubkey must hash to the prize hash160
    pubs = {
        "cmp": "03f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464",
        "unc": "04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559",
    }
    for name, h in pubs.items():
        got = hash160(bytes.fromhex(h))
        # The address commits to one pubkey encoding. Uncompressed matches;
        # the compressed encoding of the same point is a different hash160.
        mark = "PASS" if (name == "unc" and got == PRIZE_H160) or (name == "cmp" and got != PRIZE_H160) else "FAIL"
        print(f"[{mark}] published {name} pubkey hash160 {got}")

    pt = (ART / "faed_bifid.txt").read_text().strip()
    faed = (ART / "faed.txt").read_text().strip()
    assert pt.startswith("btcseed") and len(pt) == 570
    tail = pt[len("btcseed") :]
    even, odd = pt[0::2], pt[1::2]
    print(f"\nplaintext {len(pt)} tail {len(tail)} even {len(even)} odd {len(odd)}")
    print(f"even alphabet {''.join(sorted(set(even)))}")
    print(f"sha256 plaintext {sha256(pt.encode()).hex()}")
    print(f"sha256 tail       {sha256(tail.encode()).hex()}")

    # --- what the tail actually is -----------------------------------------
    print("\n=== structure of the tail ===")
    alpha25 = "abcdefghiklmnopqrstuvwxyz"  # no j
    square = "dbifhcegaklmnopqrstuvwxyz"
    decodes = {}
    # base64 of the tail (563 ≡ 3 mod 4, one pad)
    import base64
    for label, s, pad in (
        ("b64-tail", tail, "="),
        ("b64-full", pt, "=="),
        ("b64-odd", odd, "=" * ((4 - len(odd) % 4) % 4)),
        ("b64-even", even, "=" * ((4 - len(even) % 4) % 4)),
        ("b64-faed", faed, "=" * ((4 - len(faed) % 4) % 4)),
    ):
        try:
            raw = base64.b64decode(s + pad, validate=True)
            decodes[label] = raw
            print(f"  {label:12} {len(raw):4} bytes head {raw[:24].hex()} ascii {raw[:24]!r}")
        except Exception as e:
            print(f"  {label:12} INVALID {e}")
    # hex
    for label, s in (("hex-tail", tail), ("hex-full", pt), ("hex-odd", odd), ("hex-faed", faed)):
        try:
            raw = bytes.fromhex(s)
            decodes[label] = raw
            print(f"  {label:12} {len(raw)} bytes")
        except Exception:
            print(f"  {label:12} not hex")
    # base-25 / base-9 integer decodes
    for label, s, alph in (
        ("b25-pt-abc", pt, alpha25),
        ("b25-tail-abc", tail, alpha25),
        ("b25-odd-abc", odd, alpha25),
        ("b25-pt-sq", pt, square),
        ("b25-tail-sq", tail, square),
        ("b25-odd-sq", odd, square),
        ("b9-faed", faed, "abcdefghi"),
        ("b4-even", even, "bcde"),
    ):
        try:
            raw = base_n_decode(s, alph)
        except ValueError as e:
            print(f"  {label:12} skip {e}")
            continue
        decodes[label] = raw
        print(f"  {label:12} {len(raw):4} bytes head {raw[:24].hex()} ascii {raw[:24]!r}")

    # row-bit and column streams of the *ciphertext* (the actual 9-symbol source)
    pos = {ch: (i // 5, i % 5) for i, ch in enumerate(square)}
    rowbits = "".join(str(pos[c][0]) for c in faed)  # each is 0 or 1
    colvals = [pos[c][1] for c in faed]              # each is 0..4
    assert set(rowbits) <= set("01")
    # 570 bits, both bit orders, drop 2 bits to reach a byte boundary
    for label, bits in (
        ("rowbits-msb", rowbits[:568]),
        ("rowbits-drop2-tail", rowbits[2:]),
        ("rowbits-256", rowbits[:256]),
        ("rowbits-second256", rowbits[256:512]),
    ):
        raw = int(bits, 2).to_bytes(len(bits) // 8, "big")
        decodes[label] = raw
        print(f"  {label:18} {len(raw):4} bytes head {raw[:24].hex()}")
    # LSB-first per byte
    lsb = bytearray()
    for i in range(0, 568, 8):
        lsb.append(int(rowbits[i : i + 8][::-1], 2))
    decodes["rowbits-lsb"] = bytes(lsb)
    col_alph = "01234"
    decodes["b5-cols"] = base_n_decode("".join(str(v) for v in colvals), col_alph)
    print(f"  {'b5-cols':18} {len(decodes['b5-cols']):4} bytes head {decodes['b5-cols'][:24].hex()}")

    # even letters as 2-bit symbols, four sensible assignments of {b,c,d,e}
    # b=(0,1), c=(1,0), d=(0,0), e=(1,1) in the square: pack row||col.
    twobit = []
    for ch in even:
        r, c = pos[ch]
        twobit.append((r << 1) | c)
    # 285 symbols * 2 bits = 570 bits = 71 bytes + 2 bits. Drop last symbol (2 bits).
    bits = "".join(f"{v:02b}" for v in twobit)
    decodes["even-rc"] = int(bits[:568], 2).to_bytes(71, "big")
    print(f"  {'even-rc':18} {len(decodes['even-rc']):4} bytes head {decodes['even-rc'][:24].hex()}")

    # odd-letter coordinates as a base-5 pair stream already covered by b25-odd.
    save = {k: (hashlib.sha256(v).hexdigest(), len(v)) for k, v in decodes.items()}
    (ART / "faed_decodes.json").write_text(json.dumps(save, indent=2))
    for k, v in decodes.items():
        (ART / f"decode_{k}.bin").write_bytes(v)

    # --- win tests ----------------------------------------------------------
    print("\n=== win tests ===")
    found = []
    nkeys = 0
    # explicit scalar candidates
    explicit = {
        "sha256(plaintext)": sha256(pt.encode()),
        "sha256(tail)": sha256(tail.encode()),
        "sha256(faed)": sha256(faed.encode()),
        "sha256(odd)": sha256(odd.encode()),
        "sha256(even)": sha256(even.encode()),
        "sha256(btcseed)": sha256(b"btcseed"),
    }
    for label, key in explicit.items():
        win_key(key, label, found)
        nkeys += 1
        for comp in (True, False):
            # WIF round-trip is checked; the key itself is the scalar
            _ = wif_from_priv(key, comp)
    for label, buf in decodes.items():
        nkeys += scan_keys(buf, label, found)
    print(f"  scalars tested {nkeys}, wins {len(found)}")

    # BIP39 of the 32-byte hashes, and of any decode that is a legal entropy length
    if mnemonic is not None:
        print("\n=== BIP39 ===")
        paths = ["m/44'/0'/0'/0/0", "m/84'/0'/0'/0/0", "m/0'/0/0", "m/44'/0'/0'/0/1"]
        entropies = dict(explicit)
        for label, buf in decodes.items():
            if len(buf) in (16, 20, 24, 28, 32):
                entropies[label] = buf
        for label, ent in entropies.items():
            if len(ent) not in (16, 20, 24, 28, 32):
                continue
            words = mnemonic.to_mnemonic(ent)
            seed = bip39_seed(words)
            win_key(seed[:32], f"bip39-seed32({label})", found)
            win_key(seed[32:], f"bip39-seed32b({label})", found)
            win_key(sha256(words.encode()), f"sha256(mnemonic {label})", found)
            for path in paths:
                k = derive_path(seed, path)
                win_key(k, f"bip32 {path} of {label}", found)
            print(f"  {label}: {words[:60]}...")

    # --- passwords against the containers -----------------------------------
    print("\n=== container passwords ===")
    answers = []
    def add(label, s):
        if s and all(isinstance(s, str) for _ in [0]):
            answers.append((label, s))

    add("plaintext", pt)
    add("tail", tail)
    add("odd", odd)
    add("even", even)
    add("faed", faed)
    add("btcseed", "btcseed")
    for label in ("plaintext", "tail", "odd", "even", "faed"):
        src = dict(plaintext=pt, tail=tail, odd=odd, even=even, faed=faed)[label]
        add(f"sha256hex({label})", sha256(src.encode()).hex())
    for label, buf in decodes.items():
        if len(buf) <= 96:
            add(f"hex({label})", buf.hex())
            add(f"latin1({label})", buf.decode("latin-1"))
        # a 32-byte or 64-byte window is a key, already win-tested; also try the
        # whole decode's hex if it is a plausible password (64 or 128 hex chars)
        if len(buf) in (32, 64):
            add(f"hex({label})", buf.hex())
    # WIF forms of the explicit hashes
    for label, key in explicit.items():
        add(f"wif-c({label})", wif_from_priv(key, True))
        add(f"wif-u({label})", wif_from_priv(key, False))

    # yellow-blue prime walk, once the colour sequence is re-derived
    grid = (ART / "poster_grid.txt").read_text().splitlines()
    # spiral colours of B/Y/F only, counter-clockwise, down first
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    r = c = di = 0
    seen = set()
    coloured = []
    for _ in range(196):
        ch = grid[r][c]
        if ch in "BYF":
            coloured.append(ch)
        seen.add((r, c))
        nr, nc = r + dirs[di][0], c + dirs[di][1]
        if not (0 <= nr < 14 and 0 <= nc < 14) or (nr, nc) in seen:
            di = (di + 1) % 4
            nr, nc = r + dirs[di][0], c + dirs[di][1]
        r, c = nr, nc
    colour_seq = "".join(coloured)
    print(f"\ncolour sequence ({len(colour_seq)}) {colour_seq}")
    (ART / "yellowblue_colours.txt").write_text(colour_seq + "\n")
    dbbi = (ART / "dbbi.txt").read_text().strip()
    runs = yellowblue(dbbi, colour_seq)
    for run in runs:
        exact = run["letters_used"] == len(dbbi) and run["colours_used"] == len(colour_seq)
        full_letters = run["letters_used"] == len(dbbi)
        mark = "EXACT" if exact else ("LETTERS" if full_letters else "    ")
        print(f"  {mark} start {run['start']} end-pos {run['pos_end']} letters {run['letters_used']}/{len(dbbi)} colours {run['colours_used']}/{len(colour_seq)} fillers {len(run['fillers'])}")
        if full_letters and not exact:
            bad = [(p, col, ch) for p, col, ch in run["chunks"] if not ch.startswith("b") or (col == "Y" and ch != "be") or (col != "Y" and len(ch) != 1)]
            print(f"      nonconforming chunks {len(bad)}/{len(run['chunks'])} first {bad[:8]}")
        conforming = full_letters and all(
            ch.startswith("b") and (col != "Y" or ch == "be") and (col == "Y" or len(ch) == 1)
            for _, col, ch in run["chunks"]
        )
        if exact or conforming:
            chunks = "".join(ch for _, _, ch in run["chunks"])
            print(f"      fillers {run['fillers']}")
            print(f"      colour-chunks {chunks}")
            add("yb-fillers", run["fillers"])
            add("yb-chunks", chunks)
            add("yb-fillers+tail", run["fillers"] + tail)
            add("tail+yb-fillers", tail + run["fillers"])
            (ART / "yellowblue_fillers.txt").write_text(run["fillers"] + "\n")
            (ART / "yellowblue_chunks.txt").write_text(chunks + "\n")
            # The page's own a..i decimal→hex decoder, applied to the fillers.
            digits = "".join(str(ord(ch) - 96) for ch in run["fillers"])
            n = int(digits)
            hexdigits = format(n, "x")
            if len(hexdigits) % 2:
                hexdigits = "0" + hexdigits
            raw_dec = bytes.fromhex(hexdigits)
            n9 = 0
            for ch in run["fillers"]:
                n9 = n9 * 9 + (ord(ch) - 97)
            raw9 = n9.to_bytes(24, "big")
            (ART / "yellowblue_decimal.bin").write_bytes(raw_dec)
            (ART / "yellowblue_base9.bin").write_bytes(raw9)
            add("yb-digits", digits)
            add("yb-decimal-hex", raw_dec.hex())
            add("yb-base9-hex", raw9.hex())
            for label, buf in (("yb-decimal", raw_dec), ("yb-base9", raw9)):
                if len(buf) == 32:
                    win_key(buf, label, found)
                win_key(sha256(buf), f"sha256({label})", found)
                nkeys += 1
            if mnemonic is not None and len(raw9) in (16, 20, 24, 28, 32):
                words = mnemonic.to_mnemonic(raw9)
                seed = bip39_seed(words)
                print(f"      filler BIP39 {words}")
                win_key(seed[:32], "bip39-seed32(yb-base9)", found)
                win_key(sha256(words.encode()), "sha256(mnemonic yb-base9)", found)
                for path in ("m/44'/0'/0'/0/0", "m/84'/0'/0'/0/0", "m/0'/0/0"):
                    win_key(derive_path(seed, path), f"bip32 {path} of yb-base9", found)
                add("yb-mnemonic", words)

    sums = matrix_sums(grid)
    for enc, info in sums.items():
        print(f"  matrix {enc} rows {info['rows']} total {info['total']}")
        add(f"matrix-{enc}-rows", info["rowdigits"])
        add(f"matrix-{enc}-joined", info["joined"])
        # the untested combination: the sum list is an operand on the seed, not a password by itself
        add(f"tail+matrix-{enc}", tail + info["joined"])
        add(f"matrix-{enc}+tail", info["joined"] + tail)
        x = bytes(a ^ b for a, b in zip(sha256(tail.encode()), sha256(info["joined"].encode())))
        win_key(x, f"sha256(tail) xor sha256(matrix-{enc})", found)
        add(f"xorhex-tail-matrix-{enc}", x.hex())

    # de-duplicate answers, preserve order
    seen_a = set()
    unique = []
    for label, s in answers:
        key = s.encode()
        if key in seen_a:
            continue
        seen_a.add(key)
        unique.append((label, s))
    print(f"\n{len(unique)} distinct password strings × {len(containers)} containers × 5 KDFs")

    hits = []
    with LOG.open("w") as logf:
        # control: the known phase-2 answer must open a reconstructed phase-2 blob
        phase2 = (ART / "phase2.txt").read_bytes()
        # rebuild is unnecessary; instead confirm the harness opens phase 2 from the handoff
        # by decrypting the saved ciphertext. Re-extract quickly.
        import re
        hand = (ROOT / "uploads" / "GSMG-handoff.md").read_text()
        htmls = re.findall(r"```html\n(.*?)```", hand, flags=re.S)
        area = re.search(r"<textarea[^>]*>(.*?)</textarea>", htmls[1], flags=re.S).group(1)
        raw2 = b64_to_raw(area)
        body, _ = decrypt_with_password(raw2, sha256(b"causality").hex().encode())
        print(f"[{'PASS' if body and body.startswith(b'The ironic') else 'FAIL'}] harness phase-2 control")
        for label, answer in unique:
            attempt(containers, label, answer, logf, None, hits)

    print(f"\nhits {len(hits)} wins {len(found)}")
    (ART / "step1_summary.json").write_text(json.dumps({
        "wins": [{"label": a, "priv": b.hex(), "form": c} for a, b, c, _ in found],
        "hits": [{k: v for k, v in h.items() if k != "plaintext"} | {"plaintext_head": h["plaintext"][:80].hex()} for h in hits],
        "n_passwords": len(unique),
        "n_scalars": nkeys,
        "decode_sha256": save,
    }, indent=2))
    if found or hits:
        raise SystemExit(0)
    print("NO HIT")


if __name__ == "__main__":
    main()
