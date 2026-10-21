#!/usr/bin/env python3
"""Round 6: Reader top-5 readings (ledger/round5/reader.md)."""

from __future__ import annotations

import hashlib
import itertools
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "team"))
ART = ROOT / "artifacts"

from crypto_known import is_win_uncompressed  # noqa: E402
from step1_btcseed import load_containers  # noqa: E402
from step3_mask import tok23  # noqa: E402
from cryptanalyst_tests import (  # noqa: E402
    CONTAINERS,
    message_8446_text,
    planted_control,
    record,
    results,
    try_password,
)
from round3_battery import decrypt_mdp5, word_lastwords_candidates  # noqa: E402
from round4_battery import decrypt_mdp5_bytes  # noqa: E402

ARCH = (ART / "phase32_beaufort.txt").read_text().strip()
CHECKER = (ART / "phase32_checkerboard.txt").read_text().strip()
SAL = (ART / "salphaseion.txt").read_text().strip()
DIGITS149 = re.search(
    rb"(\d{149})",
    (ART / "phase32.bin").read_bytes(),
).group(1).decode()
SPIRAL_URL = "gsmg.io/theseedisplanted"
POEM1710 = (
    "Roses are White but often Red. Yellow has a number and so does Blue. "
    "Go back to the first puzzle piece without further ado."
)

hits: list[dict] = []
md5_hits: list[dict] = []
sha_tries = 0
md5_tries = 0
PRIORITY = ("r6-p1", "r6-p2", "r6-p3", "r6-p4", "r6-p5")


def emit(answer: str, label: str) -> None:
    global sha_tries
    if not answer or len(answer) > 8000:
        return
    sha_tries = try_password(answer, label, hits, sha_tries)
    sha_tries = try_password(
        hashlib.sha256(answer.encode()).hexdigest(), f"{label}:sha256hex", hits, sha_tries
    )
    d = hashlib.sha256(answer.encode()).digest()
    if is_win_uncompressed(d):
        hits.append({"label": label, "win": True})


def emit_md5(answer: str, label: str, containers: tuple[str, ...] = ("salphaseion_short", "cosmic")) -> None:
    global md5_tries
    blobs = load_containers()
    for cname in containers:
        raw = blobs[cname]
        for suffix, pw in (
            ("plain", answer.encode()),
            ("sha256hex", hashlib.sha256(answer.encode()).hexdigest().encode()),
        ):
            body, _ = decrypt_mdp5_bytes(raw, pw)
            md5_tries += 1
            if body and len(body) >= 8:
                from step1_btcseed import classify

                if classify(body).startswith("structured"):
                    md5_hits.append({"label": f"{label}:{suffix}", "container": cname})


def recipe(msl: str, lw: str = "lastwordsbeforearchichoice") -> str:
    return f"{msl}enter{lw}thispassword{msl}"


def recipe_labels(msl: str) -> str:
    return f"matrixsumlist{msl}enterlastwordsbeforearchichoicethispassword{msl}"


# --- P1: after SELECT ---------------------------------------------------------

def battery_p1_after_select() -> int:
    sel = ARCH.find("SELECT")
    after = ARCH[sel + 6 :]
    phrases = [
        after.lower(),
        "fromovertwentythreecipherssixteenencryptionsandorsevenintertwinedpasswords",
        "fromovertwentythreecipherssixteenencryptions",
        "twentythreecipherssixteenencryptions",
        "sevenintertwinedpasswords",
        "bruteforcingmightberequired",
        "notethatalsobruteforcingmightberequired",
    ]
    n = 0
    for i, p in enumerate(phrases):
        emit(p, f"{PRIORITY[0]}-after-{i}")
        emit(recipe(p), f"{PRIORITY[0]}-recipe-{i}")
        emit(recipe_labels(p), f"{PRIORITY[0]}-recipe-lab-{i}")
        n += 3
    return n


# --- P2: checkerboard 149 digits --------------------------------------------

def battery_p2_checkerboard() -> int:
    d = DIGITS149
    msl_ops = {
        "sum": str(sum(int(c) for c in d)),
        "literal": d,
        "pairs": "".join(str(int(d[i : i + 2])) for i in range(0, 148, 2)),
        "mod256": bytes(int(d[i : i + 3]) % 256 for i in range(0, 147, 3)).decode(
            "latin-1", errors="replace"
        ),
        "decode": CHECKER,
        "decode-half": CHECKER[:45],
    }
    lw = "halfandbetterhalf"
    n = 0
    for name, msl in msl_ops.items():
        emit(msl, f"{PRIORITY[1]}-msl-{name}")
        emit(recipe(msl, lw), f"{PRIORITY[1]}-recipe-{name}")
        emit(recipe_labels(msl), f"{PRIORITY[1]}-lab-{name}")
        emit_md5(recipe(msl, lw), f"{PRIORITY[1]}-md5-{name}")
        n += 4
    return n


# --- P3: #6509 three hint identities for matrixsumlist ------------------------

def battery_p6509() -> int:
    spiral_bits = (ART / "poster_spiral_bits.txt").read_text().strip()
    url_bits = spiral_bits[:192]
    m8446 = message_8446_text()
    hints = {
        "spiral-url": SPIRAL_URL,
        "spiral-url-bits": url_bits,
        "spiral-bits-196": spiral_bits,
        "8446-string": m8446,
        "8446-sha256hex": hashlib.sha256(m8446.encode()).hexdigest(),
        "poem1710": POEM1710,
        "poem1710-short": "yellowhasanumberandsodoesblue",
    }
    n = 0
    for name, msl in hints.items():
        emit(recipe_labels(msl), f"{PRIORITY[2]}-hint-{name}")
        emit_md5(recipe_labels(msl), f"{PRIORITY[2]}-md5-{name}")
        emit(recipe(msl, "theseedisplanted"), f"{PRIORITY[2]}-recipe-{name}")
        n += 3
    return n


# --- P4: yinyang phase containers ---------------------------------------------

def battery_p4_yinyang() -> int:
    blobs = load_containers()
    yin_names = [
        "sal_yinyang_blocks",
        "sal_yinyang_ct_bytes",
        "sal_yinyang_b64_chars",
        "term_sal_block_ab",
        "term_sal_block_ba",
        "xor_ct_salt_terminal",
        "xor_ct_salt_salphaseion",
    ]
    priors = [
        CHECKER,
        CHECKER.lower(),
        str(sum(int(c) for c in DIGITS149)),
        tok23(),
        ARCH[ARCH.find("SELECT") + 6 : ARCH.find("SELECT") + 70].lower(),
        "yinyang",
        hashlib.sha256(CHECKER.encode()).hexdigest(),
    ]
    n = 0
    for yname in yin_names:
        raw = blobs.get(yname)
        if raw is None or raw[:8] != b"Salted__":
            continue
        for j, ans in enumerate(priors):
            pw = hashlib.sha256(ans.encode()).hexdigest().encode()
            from step1_btcseed import decrypt_with_password, classify

            body, _ = decrypt_with_password(raw, pw)
            n += 1
            if body and classify(body).startswith("structured"):
                hits.append({"label": f"{PRIORITY[3]}-{yname}-{j}", "kind": "structured"})
            # also plain
            body2, _ = decrypt_with_password(raw, ans.encode())
            n += 1
            if body2 and classify(body2).startswith("structured"):
                hits.append({"label": f"{PRIORITY[3]}-{yname}-{j}-plain", "kind": "structured"})
    return n


# --- P5: enter as XOR ---------------------------------------------------------

def xor_bytes(a: bytes, b: bytes) -> bytes:
    n = max(len(a), len(b))
    if n == 0:
        return b""
    a = (a * (n // len(a) + 1))[:n]
    b = (b * (n // len(b) + 1))[:n]
    return bytes(x ^ y for x, y in zip(a, b))


def battery_p5_xor_enter() -> int:
    ab = SAL[91:195].replace("a", "0").replace("b", "1")
    ab_bytes = bytes(int(ab[i : i + 8], 2) for i in range(0, len(ab) - len(ab) % 8, 8))
    spiral = (ART / "poster_spiral_bits.txt").read_text().strip().encode()
    tok = tok23().encode()
    lw = ARCH[ARCH.find("SELECT") - 40 : ARCH.find("SELECT")].lower().encode()
    checker = CHECKER.encode()
    term = load_containers()["terminal"]
    sal = load_containers()["salphaseion_short"]
    pairs = [
        ("tok23^lw", xor_bytes(tok, lw)),
        ("spiral^ab", xor_bytes(spiral, ab_bytes)),
        ("checker^tok23", xor_bytes(checker, tok)),
        ("checker^ab", xor_bytes(checker, ab_bytes)),
        ("termct^salct", xor_bytes(term[16:], sal[16:])),
    ]
    n = 0
    for name, xb in pairs:
        emit(xb.hex(), f"{PRIORITY[4]}-xor-{name}-hex")
        emit(xb.decode("latin-1", errors="replace"), f"{PRIORITY[4]}-xor-{name}-latin1")
        emit(recipe(xb.hex()[:120], "halfandbetterhalf"), f"{PRIORITY[4]}-recipe-{name}")
        n += 3
    return n


def main() -> int:
    global sha_tries
    results.clear()
    planted_control()

    counts = {
        "p1_after_select": battery_p1_after_select(),
        "p2_checkerboard": battery_p2_checkerboard(),
        "p3_6509_hints": battery_p6509(),
        "p4_yinyang": battery_p4_yinyang(),
        "p5_xor_enter": battery_p5_xor_enter(),
    }
    report = {
        "priority_batteries": counts,
        "sha_decrypts": sha_tries,
        "md5_decrypts": md5_tries,
        "structured_sha": len(hits),
        "structured_md5": len(md5_hits),
        "hits": hits[:30],
        "md5_hits": md5_hits,
        "digits149_sum": sum(int(c) for c in DIGITS149),
    }
    (ART / "round6_battery.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"round6: sha={sha_tries} md5={md5_tries} structured={len(hits)} md5s={len(md5_hits)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
