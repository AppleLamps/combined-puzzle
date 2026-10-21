#!/usr/bin/env python3
"""Round 4: MD5+sha256 EVP password, spiral bitstring MSL ops, triple/quad filler deletion."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
ART = ROOT / "artifacts"

from crypto_known import evp_bytes_to_key, pkcs7_unpad, is_win_uncompressed  # noqa: E402
from Crypto.Cipher import AES  # noqa: E402
from step1_btcseed import classify  # noqa: E402
from step3_mask import tok23  # noqa: E402

sys.path.insert(0, str(ROOT / "team"))
from cryptanalyst_tests import planted_control, record, results, try_password  # noqa: E402
from round3_battery import spiral_coords, word_lastwords_candidates  # noqa: E402

SAL_SHORT = (ART / "salphaseion_short.bin").read_bytes()
FILLERS = (ART / "yellowblue_fillers.txt").read_text().strip()
COMMUNITY = "matrixsumlistenterlastwordsbeforearchichoicethispasswordmatrixsumlist"
ARCH = (ART / "phase32_beaufort.txt").read_text().strip()

hits_md5: list[dict] = []
hits_sha: list[dict] = []
md5_tries = 0
sha_tries = 0


def ab_bits(s: str) -> bytes:
    if len(s) % 8:
        s = s + "a" * (8 - len(s) % 8)
    return bytes(int(s[i : i + 8].replace("a", "0").replace("b", "1"), 2) for i in range(0, len(s), 8))


def spiral_bitstring() -> str:
    return (ART / "poster_spiral_bits.txt").read_text().strip()


def spiral_msl_operations() -> list[tuple[str, str]]:
    bits = spiral_bitstring()
    ab = bits.replace("0", "a").replace("1", "b")
    raw = ab_bits(ab)
    order = spiral_coords()
    import json

    bit_grid = json.loads((ART / "matrix.json").read_text())["bit_grid"]
    spiral_seq = []
    for r, c in order:
        spiral_seq.append(bit_grid[r][c])
    # 14 groups of 14 along spiral walk
    groups = ["".join(spiral_seq[i : i + 14]) for i in range(0, len(spiral_seq), 14)]
    list_row_sums = "".join(str(sum(int(c) for c in g)) for g in groups)
    list_row_sums_sep = "-".join(str(sum(int(c) for c in g)) for g in groups)
    rev = bits[::-1]
    url192 = bits[:192]
    tail4 = bits[192:]
    ops: list[tuple[str, str]] = [
        ("spiral-ab-bytes-hex", raw.hex()),
        ("spiral-ab-latin1", raw.decode("latin-1", errors="replace")),
        ("spiral-bits-literal", bits),
        ("spiral-bits-rev", rev),
        ("spiral-url192", url192),
        ("spiral-url192-ab-hex", ab_bits(url192.replace("0", "a").replace("1", "b")).hex()),
        ("spiral-list-rowsums", list_row_sums),
        ("spiral-list-rowsums-sep", list_row_sums_sep),
        ("spiral-int", str(int(bits, 2))),
        ("spiral-int-rev", str(int(rev, 2))),
        ("spiral-tail4", tail4),
    ]
    # pairwise combine with tok23
    t = tok23()
    for label, val in list(ops):
        ops.append((f"{label}+tok23", val + t))
        ops.append((f"tok23+{label}", t + val))
    return ops


def decrypt_mdp5_bytes(raw: bytes, password: bytes) -> tuple[bytes | None, bytes | None]:
    if raw[:8] != b"Salted__":
        return None, None
    salt, ct = raw[8:16], raw[16:]
    key, iv = evp_bytes_to_key(password, salt, md=hashlib.md5)
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    return pkcs7_unpad(pt), pt


def try_mdp5_password_variants(answer: str, label: str) -> None:
    """EVP-MD5 with several ways to derive the password bytes from `answer`."""
    global md5_tries
    digest = hashlib.sha256(answer.encode()).digest()
    hex_ascii = hashlib.sha256(answer.encode()).hexdigest().encode()
    variants = {
        "plain": answer.encode(),
        "sha256hex-ascii": hex_ascii,
        "sha256-raw32": digest,
        "md5hex-of-plain": hashlib.md5(answer.encode()).hexdigest().encode(),
    }
    for suffix, pw in variants.items():
        body, full = decrypt_mdp5_bytes(SAL_SHORT, pw)
        md5_tries += 1
        if body is None:
            continue
        kind = classify(body)
        if kind.startswith("structured"):
            hits_md5.append({"label": f"{label}:{suffix}", "kind": kind, "len": len(body)})


def filler_deleted(indices: tuple[int, ...]) -> str:
    s = FILLERS
    for idx in sorted(indices, reverse=True):
        s = s[:idx] + s[idx + 1 :]
    return s


def filler_bytes(text: str) -> bytes:
    n = int("".join(str(ord(c) - 96) for c in text))
    return n.to_bytes((n.bit_length() + 7) // 8, "big")


def try_sha_candidates(answer: str, label: str) -> None:
    global sha_tries
    sha_tries = try_password(answer, label, hits_sha, sha_tries)
    hx = hashlib.sha256(answer.encode()).hexdigest()
    sha_tries = try_password(hx, f"{label}:sha256hex", hits_sha, sha_tries)
    d = hashlib.sha256(answer.encode()).digest()
    if is_win_uncompressed(d):
        hits_sha.append({"label": label, "win": True})


def main() -> int:
    global sha_tries, md5_tries
    results.clear()
    planted_control()

    # MD5 control: plain community string still pads
    body, _ = decrypt_mdp5_bytes(SAL_SHORT, COMMUNITY.encode())
    record("MD5 plain community still pads", body is not None and len(body) == 79, f"len={len(body) if body else 0}")

    spiral_ops = spiral_msl_operations()
    lw = word_lastwords_candidates()[:8]

    # --- MD5 + sha256-derived EVP passwords on spiral MSL + recipes ---
    for op_label, op_val in spiral_ops:
        try_mdp5_password_variants(op_val, f"md5-{op_label}")
        for lname, lval in lw:
            for tmpl in (
                f"{op_val}enter{lval}thispassword{op_val}",
                f"matrixsumlist{op_val}enter{lval}thispasswordmatrixsumlist",
                COMMUNITY.replace("matrixsumlist", op_val, 1),
            ):
                try_mdp5_password_variants(tmpl, f"md5-recipe-{op_label}-{lname}")

    # --- §4.1 on spiral MSL string ops ---
    for op_label, op_val in spiral_ops:
        try_sha_candidates(op_val, f"sha-{op_label}")

    # --- Triple deletion (all C(60,3)) ---
    n = len(FILLERS)
    triple = list(itertools.combinations(range(n), 3))
    for idx in triple:
        deleted = filler_deleted(idx)
        raw = filler_bytes(deleted)
        try_sha_candidates(raw.decode("latin-1", errors="replace"), f"filler-tri-{idx[0]}-{idx[1]}-{idx[2]}")

    # --- Quad deletion: sha256hex only (§4.1) to keep runtime bounded ---
    quad = list(itertools.combinations(range(n), 4))
    for idx in quad:
        deleted = filler_deleted(idx)
        raw = filler_bytes(deleted)
        hx = hashlib.sha256(raw).hexdigest()
        sha_tries = try_password(hx, f"filler-quad-{idx[0]}-{idx[1]}-{idx[2]}-{idx[3]}", hits_sha, sha_tries)

    report = {
        "md5_tries": md5_tries,
        "md5_structured": len(hits_md5),
        "sha_tries": sha_tries,
        "sha_structured": len(hits_sha),
        "spiral_op_count": len(spiral_ops),
        "filler_triples": len(triple),
        "filler_quads": len(quad),
        "md5_hits": hits_md5,
    }
    (ART / "round4_battery.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"round4: md5={md5_tries} structured={len(hits_md5)} | "
        f"sha={sha_tries} structured={len(hits_sha)} | "
        f"tri={len(triple)} quad={len(quad)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
