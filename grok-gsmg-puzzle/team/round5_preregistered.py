#!/usr/bin/env python3
"""Round 5: pre-registered mechanism batteries (M1–M5), each ≤10k decrypts.

Brainstorm spec: ledger/round5/cryptanalyst.md
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "team"))

ART = ROOT / "artifacts"
OUT = ART / "round5_preregistered.json"

from crypto_known import is_win_uncompressed, pkcs7_unpad  # noqa: E402
from step1_btcseed import load_containers  # noqa: E402
from cryptanalyst_tests import (  # noqa: E402
    SQUARE,
    bifid_decrypt,
    beaufort_reciprocal,
    classify_plaintext,
    message_8446_text,
    planted_control,
    record,
    results,
)
from step3_mask import MASK6, apply_zeros, digits_of, matrix_strings, to_bytes, tok23  # noqa: E402

FLOWER = "theflowerblossomsthroughwhatseemstobeaconcretesurface"
FLOWER_HASH = "5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75"
COMMUNITY = "matrixsumlistenterlastwordsbeforearchichoicethispasswordmatrixsumlist"
ARCH = (ART / "phase32_beaufort.txt").read_text().strip()
CHECKER = (ART / "phase32_checkerboard.txt").read_text().strip()

BUDGET_PER_MECHANISM = 10_000

summary: dict = {"mechanisms": {}, "hits": [], "decrypts": 0}


def decrypt_with_profile(
    raw: bytes,
    answer: str,
    profile: str,
) -> tuple[bytes | None, str]:
    """profile names match ledger/round5/cryptanalyst.md M1 table."""
    if profile == "std-hex-sha256":
        pw = hashlib.sha256(answer.encode()).hexdigest().encode()
        body, _ = _decrypt_evp(raw, pw, hashlib.sha256)
    elif profile == "plain-md5":
        body, _ = _decrypt_evp(raw, answer.encode(), hashlib.md5)
    elif profile == "raw32-sha256":
        pw = hashlib.sha256(answer.encode()).digest()
        body, _ = _decrypt_evp(raw, pw, hashlib.sha256)
    else:
        raise ValueError(profile)
    return body, classify_plaintext(body)


def _decrypt_evp(raw: bytes, pw: bytes, md) -> tuple[bytes | None, str]:
    from crypto_known import evp_bytes_to_key
    from Crypto.Cipher import AES

    salt, ct = raw[8:16], raw[16:]
    key, iv = evp_bytes_to_key(pw, salt, md=md)
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    body = pkcs7_unpad(pt)
    return body, classify_plaintext(body)


def recipe_operands() -> list[tuple[str, str]]:
    sal = (ART / "salphaseion.txt").read_text().strip()
    bits = sal[91:195].replace("a", "0").replace("b", "1")
    msl_sum = str(sum(int(c) for c in bits))
    sel = ARCH.find("SELECT")
    lw = ARCH[max(0, sel - 40) : sel].lower()
    msl = matrix_strings()
    spiral = (ART / "poster_spiral_bits.txt").read_text().strip()
    groups = [spiral[i : i + 14] for i in range(0, 196, 14)]
    list_row_sums = "".join(str(sum(int(c) for c in g)) for g in groups)
    list_sep = "-".join(str(sum(int(c) for c in g)) for g in groups)
    return [
        ("tok23", tok23()),
        ("msl-sum-bits", msl_sum),
        ("lw-arch-tail40", lw),
        ("8446-head", message_8446_text()[:40]),
        ("flower-hash", FLOWER_HASH),
        ("community", COMMUNITY),
        ("spiral-list-rowsums", list_row_sums),
        ("spiral-list-rowsums-sep", list_sep),
        ("sha256hex-flower", hashlib.sha256(FLOWER.encode()).hexdigest()),
        ("recipe-8446-order", tok23() + msl_sum + lw + "yinyang"),
        ("msl-row", msl["row"]),
        ("msl-col", msl["col"]),
    ]


def run_mechanism(
    name: str,
    fn: Callable[[], int],
    budget: int = BUDGET_PER_MECHANISM,
) -> None:
    before = summary["decrypts"]
    used = fn()
    summary["mechanisms"][name] = {
        "decrypts": used,
        "budget": budget,
        "within_budget": used <= budget,
    }
    summary["decrypts"] += used
    record(f"{name} within budget", used <= budget, f"{used}/{budget}")


def mechanism_m1() -> int:
    """Per-container KDF profile (ledger/round5/cryptanalyst.md M1)."""
    containers = load_containers()
    profiles = {
        "terminal": "std-hex-sha256",
        "salphaseion_short": "plain-md5",
        "cosmic": "raw32-sha256",
    }
    n = 0
    for label, operand in recipe_operands():
        for cname, prof in profiles.items():
            raw = containers[cname]
            body, kind = decrypt_with_profile(raw, operand, prof)
            n += 1
            if kind == "structured":
                summary["hits"].append({"m": "M1", "label": label, "container": cname, "profile": prof})
        # cross-check: wrong profile on same operand (one mismatch each)
        body, kind = decrypt_with_profile(containers["cosmic"], operand, "plain-md5")
        n += 1
    return n


def mechanism_m2() -> int:
    """Cosmic yinyang interleave key (ledger/round5/cryptanalyst.md M2)."""
    containers = load_containers()
    cosmic = containers["cosmic"]
    variants = [
        "sal_yinyang_blocks",
        "sal_yinyang_ct_bytes",
        "sal_yinyang_b64_chars",
        "term_sal_block_ab",
        "term_sal_block_ba",
        "xor_ct_salt_terminal",
        "xor_ct_salt_salphaseion",
    ]
    n = 0
    for vname in variants:
        v = containers.get(vname)
        if v is None:
            continue
        for ans in (
            hashlib.sha256(v).hexdigest(),
            hashlib.sha256(v[:16]).hexdigest(),
            hashlib.sha256(v[16:]).hexdigest(),
            v.hex(),
        ):
            for prof in ("std-hex-sha256", "plain-md5"):
                body, kind = decrypt_with_profile(cosmic, ans, prof)
                n += 1
                if kind == "structured":
                    summary["hits"].append({"m": "M2", "variant": vname, "profile": prof})
            body, kind = decrypt_with_profile(containers["terminal"], ans, "std-hex-sha256")
            n += 1
    return n


def mechanism_m3() -> int:
    """MatrixSumList pipeline (ledger/round5/cryptanalyst.md M3)."""
    containers = load_containers()
    sal, cosmic, term = containers["salphaseion_short"], containers["cosmic"], containers["terminal"]
    spiral = (ART / "poster_spiral_bits.txt").read_text().strip()
    groups = [spiral[i : i + 14] for i in range(0, 196, 14)]
    fns = [
        ("list_row_sums", "".join(str(sum(int(c) for c in g)) for g in groups)),
        ("list_sep", "-".join(str(sum(int(c) for c in g)) for g in groups)),
        ("spiral-int", str(int(spiral, 2))),
        ("msl-row", matrix_strings()["row"]),
        ("msl-col", matrix_strings()["col"]),
        (
            "msl-sum-bits",
            str(
                sum(
                    int(c)
                    for c in (ART / "salphaseion.txt").read_text().strip()[91:195]
                    .replace("a", "0")
                    .replace("b", "1")
                )
            ),
        ),
        ("tok23+rows", tok23() + "".join(str(sum(int(c) for c in g)) for g in groups)),
    ]
    lws = [
        ("lw40", ARCH.split("SELECT")[0][-40:]),
        ("8446-8", message_8446_text()[:8]),
        ("flower-h", FLOWER_HASH),
        ("half", CHECKER[:40]),
    ]
    n = 0
    for fname, msl in fns:
        for lname, lw in lws:
            body1, k1 = decrypt_with_profile(sal, msl, "std-hex-sha256")
            n += 1
            if body1 and k1 != "no-pad":
                mid = body1.decode("latin-1", errors="replace")
                body2, k2 = decrypt_with_profile(cosmic, mid, "std-hex-sha256")
                n += 1
                if k2 == "structured":
                    summary["hits"].append({"m": "M3", "step": 2, "msl": fname, "lw": lname})
                body3, k3 = decrypt_with_profile(term, lw, "std-hex-sha256")
                n += 1
            baseline = f"{msl}enter{lw}thispassword{msl}"
            for cname, raw in (("sal", sal), ("cosmic", cosmic), ("term", term)):
                body, kind = decrypt_with_profile(raw, baseline, "std-hex-sha256")
                n += 1
    return n


def mechanism_m4() -> int:
    """Faed tail channel split (ledger/round5/cryptanalyst.md M4)."""
    faed = (ART / "faed.txt").read_text().strip()
    containers = load_containers()
    pt = bifid_decrypt(faed, SQUARE, 570)
    channels: list[tuple[str, str]] = [
        ("tail8", pt[8:]),
        ("odd", "".join(pt[i] for i in range(len(pt)) if i % 2 == 1)),
        ("even", "".join(pt[i] for i in range(len(pt)) if i % 2 == 0)),
    ]
    masked = apply_zeros(digits_of(faed, 7), MASK6)
    channels.append(("mask6-zero", to_bytes(masked).decode("latin-1", errors="replace")))
    deleted = "".join(c for i, c in enumerate(faed, 1) if i not in MASK6)
    channels.append(("mask6-del", to_bytes(digits_of(deleted, 7)).decode("latin-1", errors="replace")))
    channels.append(("beaufort-tail8", beaufort_reciprocal(pt[8:], "btcseed")))
    n = 0
    for cname in ("terminal", "salphaseion_short", "cosmic"):
        raw = containers[cname]
        for ch_name, text in channels:
            for answer in (text, hashlib.sha256(text.encode()).hexdigest()):
                body, kind = decrypt_with_profile(raw, answer, "std-hex-sha256")
                n += 1
                if kind == "structured":
                    summary["hits"].append({"m": "M4", "channel": ch_name, "container": cname})
                if len(hashlib.sha256(text.encode()).digest()) == 32:
                    if is_win_uncompressed(hashlib.sha256(text.encode()).digest()):
                        summary["hits"].append({"m": "M4", "win": ch_name})
    return n


def mechanism_m5() -> int:
    """Phase32 key slot (ledger/round5/cryptanalyst.md M5)."""
    pt = (ART / "phase32.bin").read_bytes()
    for i in range(0, len(pt) - 31):
        chunk = pt[i : i + 32]
        if is_win_uncompressed(chunk):
            summary["hits"].append({"m": "M5", "offset": i, "via": "raw-window"})
    containers = load_containers()
    negatives = [
        CHECKER.strip(),
        ARCH.split("SELECT")[0][-40:],
        "thispassword",
        hashlib.sha256(CHECKER.encode()).hexdigest(),
    ]
    n = 0
    for ans in negatives:
        for cname in ("terminal", "salphaseion_short", "cosmic"):
            body, kind = decrypt_with_profile(containers[cname], ans, "std-hex-sha256")
            n += 1
    return n


def main() -> None:
    results.clear()
    planted_control()
    run_mechanism("M1-per-container-kdf", mechanism_m1)
    run_mechanism("M2-cosmic-yinyang-interleave", mechanism_m2)
    run_mechanism("M3-matrixsumlist-enter-pipeline", mechanism_m3)
    run_mechanism("M4-faed-tail-channel-split", mechanism_m4)
    run_mechanism("M5-phase32-key-not-container", mechanism_m5)
    OUT.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    for r in results:
        if not r.get("ok", True):
            raise SystemExit(1)


if __name__ == "__main__":
    main()
