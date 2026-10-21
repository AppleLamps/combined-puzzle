#!/usr/bin/env python3
"""Closed packet: Architect-speech substitution delta as OpenSSL passwords.

The Beaufort 3.2.1 text is Reloaded's Architect speech with a short list of
replacements. Those replacements, and their concatenation in order, are the
frozen list. Four KDFs × three blobs. No 7-interleave. No brute force.

Self-tests against the published Cosmic Duality 7-XOR decrypt before any
negative leftover-3.2 result is trusted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_kdf_audit import (  # noqa: E402
    KDFS,
    ROOT,
    OUT,
    candidates,
    decrypt,
    hits_prize,
    load_blob,
    sha256,
    xor7,
)


def printable(pt: bytes) -> str | None:
    if all(32 <= c < 127 or c in (9, 10, 13) for c in pt):
        return pt.decode("utf-8")[:200]
    return None


def has_gsmg_path(pt: bytes) -> bool:
    low = pt.lower()
    return b"gsmg.io/" in low


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default=str(ROOT / "password_list_architect_delta.json"))
    ap.add_argument("--results-name", default="results_architect_delta.json")
    args = ap.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.is_absolute():
        spec_path = ROOT / spec_path
    spec_bytes = spec_path.read_bytes()
    spec = json.loads(spec_bytes)
    words = list(dict.fromkeys(spec["passwords"]))

    results = {
        "spec_sha256": sha256(spec_bytes),
        "n_passwords": len(words),
        "kdfs": list(KDFS),
        "selftest": {},
        "successes": [],
        "readable": [],
        "gsmg_paths": [],
        "prize_hits": [],
    }

    base = json.loads((ROOT / "password_list.json").read_bytes())
    cd = load_blob(ROOT / "artifacts" / "cosmic_duality.txt")
    st = spec["harness_selftest"]
    pt = decrypt(cd, xor7(base["published_cd_xor_passwords"]), "evp_md5")
    results["selftest"] = {
        "decrypted": pt is not None,
        "got_sha256": sha256(pt) if pt else None,
        "expected_sha256": st["expect_plaintext_sha256"],
        "pass": bool(pt) and sha256(pt) == st["expect_plaintext_sha256"],
    }
    if not results["selftest"]["pass"]:
        print("HARNESS SELF-TEST FAILED — negative results are meaningless")
        (OUT / args.results_name).write_text(json.dumps(results, indent=2))
        return 1
    print("harness self-test: PASS (reproduces published CD decrypt under evp_md5)")

    forms: list[tuple[str, bytes]] = []
    for w in words:
        forms.append((w, w.encode("utf-8")))
        forms.append((f"sha256hex({w})", hashlib.sha256(w.encode("utf-8")).hexdigest().encode()))

    blobs = {p: load_blob(ROOT / p) for p in spec["blobs"]}
    results["blob_sha256"] = {k: sha256(v) for k, v in blobs.items()}
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
                    "printable": printable(pt),
                    "gsmg_path": has_gsmg_path(pt),
                }
                results["successes"].append(rec)
                if rec["printable"] is not None:
                    results["readable"].append(rec)
                if rec["gsmg_path"]:
                    results["gsmg_paths"].append(rec)
                for how, cand in candidates(pt):
                    if hits_prize(cand):
                        results["prize_hits"].append({**rec, "via": how})

    out_path = OUT / args.results_name
    out_path.write_text(json.dumps(results, indent=2))
    print(f"passwords={len(words)} forms={len(forms)} attempts={results['n_attempts']}")
    print(
        f"pkcs7={len(results['successes'])} readable={len(results['readable'])} "
        f"gsmg={len(results['gsmg_paths'])} prize={len(results['prize_hits'])}"
    )
    for r in results["successes"]:
        print("  ", r["blob"], r["kdf"], r["password"][:80], r["pt_len"], r["printable"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
