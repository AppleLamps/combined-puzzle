#!/usr/bin/env python3
"""Closed Cosmic Duality / leftover-3.2 AES packet.

Password list is frozen in password_list.json (hashed at start).
Does not grow the list. Does not emit WIFs. Reports SHA-256 of
plaintexts and whether a 32-byte candidate matches the prize pubkey.
"""
from __future__ import annotations

import base64
import hashlib
import json
import sys
from pathlib import Path

from Crypto.Cipher import AES

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import prize_gate  # noqa: E402  both targets, both serializations

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def evp_bytes_to_key(password: bytes, salt: bytes, key_len=32, iv_len=16) -> tuple[bytes, bytes]:
    key_iv = b""
    prev = b""
    while len(key_iv) < key_len + iv_len:
        prev = hashlib.md5(prev + password + salt).digest()
        key_iv += prev
    return key_iv[:key_len], key_iv[key_len : key_len + iv_len]


def openssl_decrypt(blob: bytes, password: bytes) -> bytes | None:
    if not blob.startswith(b"Salted__") or len(blob) < 32:
        return None
    salt, ct = blob[8:16], blob[16:]
    if len(ct) % 16:
        return None
    key, iv = evp_bytes_to_key(password, salt)
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    pad = pt[-1]
    if pad < 1 or pad > 16 or pt[-pad:] != bytes([pad]) * pad:
        return None
    return pt[:-pad]


def load_blob(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8").replace("\n", "").replace("\r", "").replace(" ", "")
    return base64.b64decode(text)


def hits_prize(priv32: bytes) -> bool:
    """Half or Better Half, compressed or uncompressed (tools/prize_gate.py).

    The earlier version compared with Half's public key only, and returned
    False for every candidate when the ecdsa package was missing.
    """
    return len(priv32) == 32 and prize_gate.gate_bytes(priv32) is not None


def candidates_from_pt(pt: bytes) -> list[tuple[str, bytes]]:
    """Every candidate the shared gate extracts: raw windows, hex, WIF, sha256(pt), ..."""
    return [(f"{kind}@{off}", (k % prize_gate.N).to_bytes(32, "big"))
            for kind, k, off in prize_gate.extract(pt)]


def xor7(passwords: list[str]) -> bytes:
    acc = bytearray(32)
    for p in passwords:
        h = hashlib.sha256(p.encode("utf-8")).digest()
        for i, b in enumerate(h):
            acc[i] ^= b
    return bytes(acc)


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Closed OpenSSL AES packet")
    ap.add_argument(
        "--spec",
        default=str(ROOT / "password_list.json"),
        help="Frozen password JSON (hashed at start; do not edit after hashing)",
    )
    ap.add_argument(
        "--results-name",
        default="results.json",
        help="Filename under packet/out/ for the machine log",
    )
    args = ap.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.is_absolute():
        spec_path = ROOT / spec_path
    spec_bytes = spec_path.read_bytes()
    spec_hash = sha256(spec_bytes)
    spec = json.loads(spec_bytes)
    (OUT / f"{spec_path.stem}.sha256").write_text(spec_hash + "\n")

    passwords = list(dict.fromkeys(spec["passwords"]))  # preserve order, unique
    blobs = {}
    for rel in spec["blobs"]:
        p = ROOT / rel
        raw = load_blob(p)
        blobs[p.name] = raw
        assert raw.startswith(b"Salted__"), p

    results = {
        "password_list_sha256": spec_hash,
        "n_passwords": len(passwords),
        "n_attempts": 0,
        "decrypts": [],
        "prize_hits": [],
        "blobs": {k: {"len": len(v), "sha256": sha256(v)} for k, v in blobs.items()},
    }

    for blob_name, blob in blobs.items():
        for pw in passwords:
            for mode, pwd_bytes in (
                ("raw", pw.encode("utf-8")),
                ("sha256hex", hashlib.sha256(pw.encode("utf-8")).hexdigest().encode("ascii")),
            ):
                results["n_attempts"] += 1
                pt = openssl_decrypt(blob, pwd_bytes)
                if pt is None:
                    continue
                rec = {
                    "blob": blob_name,
                    "password": pw,
                    "mode": mode,
                    "pt_len": len(pt),
                    "pt_sha256": sha256(pt),
                    "printable_prefix": "".join(
                        chr(b) if 32 <= b < 127 else "." for b in pt[:80]
                    ),
                    "prize_match": False,
                }
                for label, cand in candidates_from_pt(pt):
                    if hits_prize(cand):
                        rec["prize_match"] = True
                        rec["match_via"] = label
                        results["prize_hits"].append(rec.copy())
                results["decrypts"].append(rec)
                (OUT / f"{blob_name}.{mode}.{sha256(pw.encode())[:12]}.bin").write_bytes(pt)

    xor_rec = None
    if "cosmic_duality.txt" in blobs and spec.get("published_cd_xor_passwords"):
        # Published Cosmic Duality XOR-of-7 (writeup method, not a new operand)
        cd = blobs["cosmic_duality.txt"]
        key_xor = xor7(spec["published_cd_xor_passwords"])
        pt_xor = openssl_decrypt(cd, key_xor)
        xor_rec = {
            "method": "published_7xor_sha256_as_kdf_password",
            "ok": pt_xor is not None,
            "pt_len": len(pt_xor) if pt_xor else None,
            "pt_sha256": sha256(pt_xor) if pt_xor else None,
            "matches_published_hash": False,
            "prize_match": False,
        }
        if pt_xor is not None:
            xor_rec["matches_published_hash"] = (
                sha256(pt_xor) == spec["published_cd_plaintext_sha256"]
            )
            (OUT / "cosmic_xor7.bin").write_bytes(pt_xor)
            for label, cand in candidates_from_pt(pt_xor):
                if hits_prize(cand):
                    xor_rec["prize_match"] = True
                    xor_rec["match_via"] = label
                    results["prize_hits"].append({"blob": "cosmic_duality.txt", **xor_rec})
            pt_hex = openssl_decrypt(cd, key_xor.hex().encode("ascii"))
            xor_rec["hex_as_pass_ok"] = pt_hex is not None
            if pt_hex is not None:
                xor_rec["hex_as_pass_sha256"] = sha256(pt_hex)
                xor_rec["hex_matches_published"] = (
                    sha256(pt_hex) == spec["published_cd_plaintext_sha256"]
                )
                (OUT / "cosmic_xor7_hexpass.bin").write_bytes(pt_hex)
                for label, cand in candidates_from_pt(pt_hex):
                    if hits_prize(cand):
                        xor_rec["prize_match"] = True
                        results["prize_hits"].append(
                            {"blob": "cosmic_duality.txt", "via": "xor7_hexpass", **xor_rec}
                        )
        results["published_xor7"] = xor_rec

    (OUT / args.results_name).write_text(json.dumps(results, indent=2))
    print(json.dumps({
        "password_list_sha256": spec_hash,
        "n_passwords": len(passwords),
        "n_attempts": results["n_attempts"],
        "n_decrypts": len(results["decrypts"]),
        "n_prize_hits": len(results["prize_hits"]),
        "xor7": xor_rec,
        "decrypts": results["decrypts"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
