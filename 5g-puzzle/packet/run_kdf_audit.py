#!/usr/bin/env python3
"""Audit packet: re-run every frozen password under four KDFs.

Packets 1-4 all assumed OpenSSL's pre-1.1 EVP_BytesToKey-MD5 derivation.
Nothing in the puzzle guarantees that, and the leftover 3.2 blob has never
been opened by anyone, so its KDF is unknown. This sweeps MD5/SHA-1/SHA-256
EVP plus PBKDF2, and folds in the corrected blue pixel count (83700).

Self-tests the harness against the published Cosmic Duality 7-XOR decrypt
before trusting any negative result.
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


def evp_bytes_to_key(password: bytes, salt: bytes, algo: str) -> tuple[bytes, bytes]:
    key_iv = b""
    prev = b""
    while len(key_iv) < 48:
        prev = hashlib.new(algo, prev + password + salt).digest()
        key_iv += prev
    return key_iv[:32], key_iv[32:48]


def pbkdf2(password: bytes, salt: bytes, iters: int = 10000) -> tuple[bytes, bytes]:
    ki = hashlib.pbkdf2_hmac("sha256", password, salt, iters, 48)
    return ki[:32], ki[32:48]


KDFS = {
    "evp_md5": lambda p, s: evp_bytes_to_key(p, s, "md5"),
    "evp_sha1": lambda p, s: evp_bytes_to_key(p, s, "sha1"),
    "evp_sha256": lambda p, s: evp_bytes_to_key(p, s, "sha256"),
    "pbkdf2_sha256_10000": pbkdf2,
}


def decrypt(blob: bytes, password: bytes, kdf: str) -> bytes | None:
    if not blob.startswith(b"Salted__") or len(blob) < 32:
        return None
    salt, ct = blob[8:16], blob[16:]
    if len(ct) % 16:
        return None
    key, iv = KDFS[kdf](password, salt)
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    pad = pt[-1]
    if pad < 1 or pad > 16 or pt[-pad:] != bytes([pad]) * pad:
        return None
    return pt[:-pad]


def load_blob(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    text = "".join(text.split())
    return base64.b64decode(text)


def hits_prize(priv32: bytes) -> bool:
    """Half or Better Half, compressed or uncompressed (tools/prize_gate.py).

    The earlier version compared with Half's public key only, and returned
    False for every candidate when the ecdsa package was missing.
    """
    return len(priv32) == 32 and prize_gate.gate_bytes(priv32) is not None


def candidates(pt: bytes):
    """Every candidate the shared gate extracts: raw windows, hex, WIF, sha256(pt), ..."""
    return [(f"{kind}@{off}", (k % prize_gate.N).to_bytes(32, "big"))
            for kind, k, off in prize_gate.extract(pt)]


def xor7(passwords: list[str]) -> bytes:
    acc = bytearray(32)
    for p in passwords:
        for i, b in enumerate(hashlib.sha256(p.encode("utf-8")).digest()):
            acc[i] ^= b
    return bytes(acc)


def main() -> int:
    spec_path = ROOT / "password_list_audit.json"
    spec_bytes = spec_path.read_bytes()
    spec = json.loads(spec_bytes)
    results = {
        "spec_sha256": sha256(spec_bytes),
        "kdfs": list(KDFS),
        "selftest": {},
        "inherited_list_sha256": {},
        "successes": [],
        "prize_hits": [],
    }

    # --- harness self-test: the one decrypt we know the answer to ---
    st = spec["harness_selftest"]
    base = json.loads((ROOT / "password_list.json").read_bytes())
    cd = load_blob(ROOT / "artifacts" / "cosmic_duality.txt")
    pt = decrypt(cd, xor7(base["published_cd_xor_passwords"]), "evp_md5")
    results["selftest"] = {
        "decrypted": pt is not None,
        "got_sha256": sha256(pt) if pt else None,
        "expected_sha256": st["expect_plaintext_sha256"],
        "pass": bool(pt) and sha256(pt) == st["expect_plaintext_sha256"],
    }
    if not results["selftest"]["pass"]:
        print("HARNESS SELF-TEST FAILED — negative results are meaningless")
        (OUT / "results_audit.json").write_text(json.dumps(results, indent=2))
        return 1
    print("harness self-test: PASS (reproduces published CD decrypt under evp_md5)")

    # --- assemble password universe: all prior frozen lists + corrections ---
    words: list[str] = []
    for name in spec["inherit_password_lists"]:
        b = (ROOT / name).read_bytes()
        results["inherited_list_sha256"][name] = sha256(b)
        words.extend(json.loads(b)["passwords"])
    words.extend(spec["passwords"])
    words = list(dict.fromkeys(words))

    forms: list[tuple[str, bytes]] = []
    for w in words:
        forms.append((w, w.encode("utf-8")))
        forms.append((f"sha256hex({w})", hashlib.sha256(w.encode("utf-8")).hexdigest().encode()))

    blobs = {p: load_blob(ROOT / p) for p in spec["blobs"]}
    results["blob_sha256"] = {k: sha256(v) for k, v in blobs.items()}
    results["n_passwords"] = len(words)
    results["n_forms"] = len(forms)
    results["n_attempts"] = len(forms) * len(blobs) * len(KDFS)

    for blob_name, blob in blobs.items():
        for kdf in KDFS:
            for label, pw in forms:
                pt = decrypt(blob, pw, kdf)
                if pt is None:
                    continue
                rec = {
                    "blob": blob_name,
                    "kdf": kdf,
                    "password": label,
                    "pt_len": len(pt),
                    "pt_sha256": sha256(pt),
                    "printable": pt.decode("utf-8", "replace")[:120]
                    if all(32 <= c < 127 or c in (9, 10, 13) for c in pt)
                    else None,
                }
                results["successes"].append(rec)
                for how, cand in candidates(pt):
                    if hits_prize(cand):
                        results["prize_hits"].append({**rec, "via": how})

    (OUT / "results_audit.json").write_text(json.dumps(results, indent=2))
    print(f"passwords={len(words)} forms={len(forms)} attempts={results['n_attempts']}")
    print(f"pkcs7 successes={len(results['successes'])} prize hits={len(results['prize_hits'])}")
    for r in results["successes"]:
        print("  ", r["blob"], r["kdf"], r["password"], r["pt_len"], r["printable"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
