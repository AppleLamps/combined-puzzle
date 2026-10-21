#!/usr/bin/env python3
"""All 2^6 subsets of MASK6 positions: delete those letters from faed, integer→bytes, §4.1."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "team"))

from crypto_known import is_win_uncompressed  # noqa: E402
from cryptanalyst_tests import planted_control  # noqa: E402
from step1_btcseed import decrypt_with_password, load_containers  # noqa: E402
from step3_mask import MASK6, PRINTABLE, digits_of, to_bytes  # noqa: E402

CONTAINERS = ("terminal", "salphaseion_short", "cosmic")


def try_password(answer: str, label: str, hits: list[dict], decrypts: int) -> int:
    pw = hashlib.sha256(answer.encode()).hexdigest().encode()
    for cname in CONTAINERS:
        body, _ = decrypt_with_password(load_containers()[cname], pw)
        decrypts += 1
        if body and len(body) >= 8:
            printable = sum(b in PRINTABLE for b in body)
            if printable >= len(body) * 0.9 and sum(chr(b).isalpha() for b in body) >= 4:
                hits.append({"label": label, "container": cname})
    return decrypts

ART = ROOT / "artifacts"
FAED = (ART / "faed.txt").read_text().strip()


def delete_at_positions(text: str, positions_1based: frozenset[int]) -> str:
    return "".join(c for i, c in enumerate(text, 1) if i not in positions_1based)


def main() -> int:
    planted_control()

    rows = []
    hits: list[dict] = []
    key_hits: list[str] = []
    decrypts = 0

    for mask in range(64):
        pos = frozenset(MASK6[p] for p in range(6) if mask >> p & 1)
        deleted = delete_at_positions(FAED, pos)
        raw = to_bytes(digits_of(deleted, 7))
        printable = sum(b in PRINTABLE for b in raw)
        mid = raw[4:-4] if len(raw) > 8 else b""
        interior_printable = sum(b in PRINTABLE for b in mid)

        label_base = f"del-m6-{mask:02x}"
        for suffix, ans in (
            ("latin1", raw.decode("latin-1", errors="replace")),
            ("hex", raw.hex()),
            ("sha256hex", hashlib.sha256(raw).hexdigest()),
        ):
            decrypts = try_password(ans, f"{label_base}-{suffix}", hits, decrypts)
            d = hashlib.sha256(ans.encode()).digest()
            if is_win_uncompressed(d):
                key_hits.append(f"{label_base}-{suffix}")

        rows.append(
            {
                "mask": mask,
                "positions_deleted": sorted(pos),
                "faed_len": len(deleted),
                "bytes": len(raw),
                "head_hex": raw[:4].hex(),
                "tail_hex": raw[-4:].hex(),
                "printable": printable,
                "printable_ratio": round(printable / len(raw), 4) if raw else 0,
                "interior_printable": interior_printable,
                "pins_ym": raw[:2] == b"yM",
                "pins_szqu": raw[-4:] == b"szqu",
            }
        )

    rows.sort(key=lambda r: (-r["printable_ratio"], -r["printable"]))
    report = {
        "variants": 64,
        "decrypts": decrypts,
        "structured_hits": len(hits),
        "key_hits": key_hits,
        "planted_control": "ok",
        "best_printable": rows[:10],
        "mask_all_six": rows[63],
        "mask_none": rows[0],
    }
    (ART / "deletion_sweep_faed.json").write_text(json.dumps(report, indent=2) + "\n")

    print(f"variants=64 decrypts={decrypts} structured={len(hits)} keys={len(key_hits)}")
    for r in rows[:5]:
        print(
            f"  mask={r['mask']:02x} del={r['positions_deleted']} "
            f"{r['printable']}/{r['bytes']} tail={r['tail_hex']} ym={r['pins_ym']} szqu={r['pins_szqu']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
