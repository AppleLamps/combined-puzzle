#!/usr/bin/env python3
"""Round 2 P1 batteries: 8 Bifid squares, Beaufort keys, dots, another-door, recipe."""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
ART = ROOT / "artifacts"
HANDOFF = ROOT / "uploads" / "GSMG-handoff.md"

from crypto_known import decrypt_b64, is_win_uncompressed  # noqa: E402
from step3_mask import matrix_strings, tok23  # noqa: E402

# Reuse cryptanalyst primitives
sys.path.insert(0, str(ROOT / "team"))
from cryptanalyst_tests import (  # noqa: E402
    BIFID_SHA,
    CONTAINERS,
    HANDOFF as CT_HANDOFF,
    SQUARE,
    ab_bits,
    beaufort_reciprocal,
    bifid_decrypt,
    dots_candidates,
    message_8446_text,
    planted_control,
    record,
    results,
    try_password,
)

FAED = (ART / "faed.txt").read_text().strip()
DBBI = (ART / "dbbi.txt").read_text().strip()
FILLERS = (ART / "yellowblue_fillers.txt").read_text().strip()
ARCH = (ART / "phase32_beaufort.txt").read_text().strip()
URL = "gsmg.io/theseedisplanted"

BEAUFORT_KEYS = (
    "btcseed",
    "btcseedd",
    "THEMATRIXHASYOU",
    "matrixsumlist",
    "yellowblueprimes",
    "causality",
    "theseedisplanted",
    "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple",
    "lastwordsbeforearchichoice",
    "thispassword",
    "SELECT",
    "primebasics",
)

hits: list[dict] = []
key_hits: list[str] = []
decrypts = 0


def add_password(answer: str, label: str) -> None:
    global decrypts
    decrypts = try_password(answer, label, hits, decrypts)
    d = hashlib.sha256(answer.encode()).digest()
    if is_win_uncompressed(d):
        key_hits.append(label)
    hx = hashlib.sha256(answer.encode()).hexdigest()
    decrypts = try_password(hx, f"{label}:sha256hex", hits, decrypts)


def eight_squares() -> list[tuple[str, str]]:
    out = []
    for perm in itertools.permutations("dbifhcega"):
        sq = "".join(perm) + "klmnopqrstuvwxyz"
        pt = bifid_decrypt(FAED, sq, 570)
        if pt.startswith("btcseed"):
            out.append((sq[:9], pt))
    return out


def recipe_candidates() -> list[tuple[str, str]]:
    sal = (ART / "salphaseion.txt").read_text().strip()
    ab = sal[91:195]
    bits = ab.replace("a", "0").replace("b", "1")
    msl = matrix_strings()
    sel = ARCH.find("SELECT")
    lw_arch = ARCH[:sel].lower()
    lw_tail40 = ARCH[max(0, sel - 40) : sel].lower()
    cands = [
        ("msl-sum-bits", str(sum(int(c) for c in bits))),
        ("msl-ab-int", str(int(bits, 2))),
        ("msl-row", msl["row"]),
        ("msl-col", msl["col"]),
        ("msl-row+col", msl["row"] + msl["col"]),
        ("lw-arch-all", lw_arch),
        ("lw-arch-tail40", lw_tail40),
        ("lw-requiredto", "afterwhichyouwillberequiredto"),
        ("tok23", tok23()),
        ("tok23+msl-row", tok23() + msl["row"]),
        ("tok23+msl-col", tok23() + msl["col"]),
        ("tok23+lw-tail40", tok23() + lw_tail40),
        (
            "recipe-8446-order",
            tok23() + str(sum(int(c) for c in bits)) + lw_tail40 + "yinyang",
        ),
        ("8446", message_8446_text()),
    ]
    return cands


def another_door_candidates() -> list[tuple[str, str]]:
    """Positions {1,4,21} with #6913 A=1,R=18,B=2."""
    sources = {
        "url": URL,
        "faed": FAED,
        "dbbi": DBBI,
        "fillers": FILLERS,
    }
    pos = (1, 4, 21)
    out = []
    for name, s in sources.items():
        chars = "".join(s[p - 1] for p in pos if p <= len(s))
        out.append((f"door-{name}-chars", chars))
        # A/R/B mapping on those chars if letters
        mapped = []
        for ch in chars:
            u = ch.upper()
            if u == "A":
                mapped.append("1")
            elif u == "R":
                mapped.append("18")
            elif u == "B":
                mapped.append("2")
            else:
                mapped.append(ch)
        out.append((f"door-{name}-arb", "".join(mapped)))
    out.append(("door-1812", "1812"))
    out.append(("door-21", "21"))
    return out


def filler_single_deletion() -> None:
    for i in range(1, len(FILLERS) + 1):
        deleted = FILLERS[: i - 1] + FILLERS[i:]
        n = int("".join(str(ord(c) - 96) for c in deleted))
        raw = n.to_bytes((n.bit_length() + 7) // 8, "big")
        add_password(raw.decode("latin-1", errors="replace"), f"filler-del-{i}")


# First 23 B/Y symbols of the poster spiral colour walk (handoff §6.3 [V]; archivist_check2).
DBBI_HOST_BY_23 = "BBBBYBBBYYBBBBYBBYYBFYY"


def dbbi_shuffle_sample(n: int = 10000, seed: int = 0) -> dict:
    """Simplified null: random 23-char B/Y strings vs canonical host pattern.

    NOT the handoff 200k letter-shuffle null (§6.3 / §8.1); see ledger/15-team-audit.md C2.
    """
    rng = random.Random(seed)
    hosts = DBBI_HOST_BY_23
    success = 0
    for _ in range(n):
        h = "".join(rng.choice("BY") for _ in range(23))
        if h == hosts:
            success += 1
    return {
        "trials": n,
        "exact_host_match": success,
        "expected_if_uniform": n / (2**23),
        "target_hosts": hosts,
        "note": "simplified_BY_string_null_not_handoff_shuffle",
    }


def main() -> None:
    global decrypts
    results.clear()
    planted_control()

    squares = eight_squares()
    record("eight bifid squares with btcseed prefix", len(squares) == 8, str(len(squares)))

    bifid_pt = bifid_decrypt(FAED, SQUARE, 570)
    record("canonical bifid sha256", hashlib.sha256(bifid_pt.encode()).hexdigest() == BIFID_SHA)

    for sq9, pt in squares:
        add_password(pt, f"bifid-{sq9}-full")
        add_password(pt[7:], f"bifid-{sq9}-tail")
        add_password(pt[8:], f"bifid-{sq9}-after-d")

    for key in BEAUFORT_KEYS:
        plain = beaufort_reciprocal(bifid_pt, key)
        add_password(plain, f"beaufort-bifid-{key[:12]}")
        even = "".join(plain[i] for i in range(0, len(plain), 2))
        odd = "".join(plain[i] for i in range(1, len(plain), 2))
        add_password(even, f"beaufort-even-{key[:8]}")
        add_password(odd, f"beaufort-odd-{key[:8]}")

    for label, ans in recipe_candidates():
        add_password(ans, f"recipe-{label}")

    for label, ans in another_door_candidates():
        add_password(ans, f"door-{label}")

    for label, ans in dots_candidates():
        add_password(ans, f"dots-{label}")
        add_password(ans + message_8446_text()[:40], f"dots-{label}+8446head")

    filler_single_deletion()

    shuffle = dbbi_shuffle_sample(10000)

    report = {
        "decrypts": decrypts,
        "structured_hits": len(hits),
        "key_hits": key_hits,
        "hits": hits[:20],
        "dbbi_shuffle_null_10k": shuffle,
    }
    (ART / "round2_battery.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"\n=== round2: decrypts={decrypts} structured={len(hits)} keys={len(key_hits)} ===")
    print("shuffle null sample", shuffle)
    if hits:
        print("HITS", hits)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
