#!/usr/bin/env python3
"""Round 10: G12 phase-3 seven-part [R] falsification + methodology controls.

Spec: team/preregister_phase3_g12.json
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "team"))

ART = ROOT / "artifacts"
SPEC = json.loads((ROOT / "team" / "preregister_phase3_g12.json").read_text())
HANDOFF = ROOT / "uploads" / "GSMG-handoff.md"

from crypto_known import decrypt_b64  # noqa: E402
from step1_btcseed import load_containers, win_key  # noqa: E402
from cryptanalyst_tests import planted_control, record, results, try_password  # noqa: E402
from classify_unified import classify_unified  # noqa: E402
from round5_preregistered import decrypt_with_profile  # noqa: E402

summary: dict = {
    "phase3_chain": [],
    "container_decrypts": 0,
    "structured_hits": [],
    "wins": [],
}


def phase3_ciphertext_b64() -> str:
    hand = HANDOFF.read_text()
    htmls = re.findall(r"```html\n(.*?)```", hand, flags=re.S)
    areas = re.findall(
        r"<textarea[^>]*>(.*?)</textarea>", htmls[1], flags=re.S | re.I
    )
    if len(areas) < 2:
        raise SystemExit(f"expected 2 phase-2/3 textareas, got {len(areas)}")
    return "".join(areas[1].split())


def test_phase3_open(label: str, parts: list[str]) -> dict:
    pw = "".join(parts)
    body, _, _ = decrypt_b64(phase3_ciphertext_b64(), pw)
    ref = (ART / "phase3.txt").read_bytes()
    ok = body is not None and body == ref
    row = {
        "label": label,
        "password_len": len(pw),
        "plaintext_len": len(body) if body else None,
        "matches_phase3_artifact": ok,
        "sha256_plaintext": hashlib.sha256(body).hexdigest() if body else None,
    }
    summary["phase3_chain"].append(row)
    return row


def try_containers(answer: str, label: str) -> None:
    blobs = load_containers()
    for cname in SPEC["containers"]:
        summary["container_decrypts"] += 1
        body, _ = decrypt_with_profile(blobs[cname], answer, "std-hex-sha256")
        if body and classify_unified(body) == "structured":
            summary["structured_hits"].append({"label": label, "container": cname})
        if body:
            win_key(body, label, summary["wins"])


def main() -> int:
    results.clear()
    planted_control()

    canonical = list(SPEC["canonical_parts"])
    row = test_phase3_open("canonical-7part", canonical)
    record(
        "phase3 canonical 7-part opens artifact",
        row["matches_phase3_artifact"],
        f"len={row['plaintext_len']}",
    )

    decrypts = 0
    for alt in SPEC["alternates"]:
        parts = list(canonical)
        parts[alt["index"]] = alt["value"]
        alt_row = test_phase3_open(alt["id"], parts)
        record(
            f"alternate {alt['id']} diverges from artifact",
            not alt_row["matches_phase3_artifact"],
            f"len={alt_row['plaintext_len']}",
        )
        pw = "".join(parts)
        decrypts = try_password(pw, f"g12-{alt['id']}", summary["structured_hits"], decrypts)
        try_containers(pw, f"g12-{alt['id']}")
        hx = hashlib.sha256(pw.encode()).hexdigest()
        decrypts = try_password(hx, f"g12-{alt['id']}-sha256hex", summary["structured_hits"], decrypts)
        try_containers(hx, f"g12-{alt['id']}-sha")

    decrypts = try_password(
        "".join(canonical), "g12-canonical-on-locked", summary["structured_hits"], decrypts
    )
    summary["container_decrypts"] += decrypts

    (ART / "round10_phase3_g12.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(
        f"round10: phase3_tests={len(summary['phase3_chain'])} "
        f"sha_decrypts={decrypts} structured={len(summary['structured_hits'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
