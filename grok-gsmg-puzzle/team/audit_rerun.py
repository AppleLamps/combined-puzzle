"""Re-run any battery with every AES-CBC decrypt audited by a structure-agnostic recogniser.

The batteries' own detectors (`step1_btcseed.classify`, `classify_unified`) need
>= 90% printable text, so they call the phase 3.2 plaintext (59% printable)
"opaque". This harness wraps `Crypto.Cipher.AES.new` before the battery is
imported, so every CBC decrypt the battery makes is recorded without editing
the battery. For each decrypt it records the container (matched by ciphertext),
PKCS#7 validity, and the recogniser reason, then reports valid pads against the
chance expectation (N/255).

The recogniser is the one in gsmg-puzzle-kit `tools/h3.c`: printable >= 0.80,
any bit-position |z| >= 6, distinct-byte deficit z <= -6, UTF-16 zero
alternation >= 0.6, nested `Salted__`, file magic, plus padding value >= 3.

Planted controls run first and must fire: the phase 3.2 plaintext itself, and
a 64-byte slice of it encrypted under the Terminal salt with a random password.

Usage:  python3 team/audit_rerun.py team/round14_clues.py [more scripts...]
Writes artifacts/audit_<script>.json.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import runpy
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "team"))

from Crypto.Cipher import AES  # noqa: E402

from crypto_known import evp_bytes_to_key  # noqa: E402

_REAL_NEW = AES.new
PRINT = set(range(32, 127)) | {9, 10, 13}
MAGIC = (b"\x1f\x8b\x08", b"PK\x03\x04", b"\x89PNG", b"%PDF", b"\xfd7zXZ", b"7z\xbc\xaf")


def recognise(p: bytes) -> str | None:
    n = len(p)
    if n < 8:
        return None
    if sum(c in PRINT for c in p) / n >= 0.80:
        return "printable"
    sd = math.sqrt(n / 4.0)
    for b in range(8):
        ones = sum(c >> b & 1 for c in p)
        if abs((ones - n / 2.0) / sd) >= 6:
            return "bitbias"
    q = 1.0 - 1.0 / 256
    e = 256 * (1 - q ** n)
    v = 256 * 255 * (1 - 2.0 / 256) ** n + 256 * q ** n - 65536 * q ** (2.0 * n)
    if v > 0 and (len(set(p)) - e) / math.sqrt(v) <= -6:
        return "distinct"
    if n >= 16 and sum(1 for i in range(1, n, 2) if p[i] == 0) / (n // 2) >= 0.6:
        return "utf16"
    if b"Salted__" in p:
        return "nestedsalt"
    if n > 10 and (p.startswith(MAGIC) or (p[:3] == b"BZh" and p[4:10] == b"\x31\x41\x59\x26\x53\x59")):
        return "magic"
    return None


def pad_len(pt: bytes) -> int:
    if not pt:
        return 0
    k = pt[-1]
    return k if 1 <= k <= 16 and pt[-k:] == bytes([k]) * k else 0


def known_ciphertexts() -> dict[bytes, str]:
    out = {}
    for name in ("terminal", "salphaseion_short", "cosmic"):
        raw = (ART / f"{name}.bin").read_bytes()
        out[hashlib.sha256(raw[16:]).digest()] = name
    return out


KNOWN = known_ciphertexts()
STATS: dict[str, dict] = {}
FLAGGED: list[dict] = []


def _record(ct: bytes, pt: bytes) -> None:
    name = KNOWN.get(hashlib.sha256(ct).digest(), f"other{len(ct)}")
    s = STATS.setdefault(name, {"decrypts": 0, "valid_pads": 0, "pad_ge3": 0, "flag_body": 0, "flag_fullblocks": 0})
    s["decrypts"] += 1
    k = pad_len(pt)
    body_reason = None
    if k:
        s["valid_pads"] += 1
        if k >= 3:
            s["pad_ge3"] += 1
        body_reason = recognise(pt[:-k])
        if body_reason:
            s["flag_body"] += 1
    full_reason = recognise(pt)
    if full_reason:
        s["flag_fullblocks"] += 1
    if body_reason or full_reason or k >= 3:
        if len(FLAGGED) < 500:
            FLAGGED.append({"container": name, "pad": k, "body": body_reason, "full": full_reason,
                            "pt_head": pt[:48].hex(), "pt_sha256": hashlib.sha256(pt).hexdigest()})


class _Audited:
    def __init__(self, inner):
        self._inner = inner

    def decrypt(self, ct, *a, **kw):
        pt = self._inner.decrypt(ct, *a, **kw)
        _record(bytes(ct), bytes(pt))
        return pt

    def __getattr__(self, item):
        return getattr(self._inner, item)


def audited_new(key, mode, *a, **kw):
    obj = _REAL_NEW(key, mode, *a, **kw)
    return _Audited(obj) if mode == AES.MODE_CBC else obj


def planted_controls() -> dict:
    p32 = (ART / "phase32.bin").read_bytes()
    c1 = recognise(p32)
    raw = (ART / "terminal.bin").read_bytes()
    salt = raw[8:16]
    key, iv = evp_bytes_to_key(os.urandom(16).hex().encode(), salt)
    body = p32[:64] + bytes([16]) * 16
    ct = _REAL_NEW(key, AES.MODE_CBC, iv).encrypt(body)
    pt = _REAL_NEW(key, AES.MODE_CBC, iv).decrypt(ct)
    c2 = recognise(pt[:-pad_len(pt)])
    rng = [recognise(os.urandom(64)) for _ in range(2000)]
    return {"phase32_full": c1, "phase32_slice64": c2, "random64_false_flags": sum(r is not None for r in rng)}


def main() -> int:
    ctl = planted_controls()
    print("controls", ctl)
    if not (ctl["phase32_full"] and ctl["phase32_slice64"]):
        print("planted control did not fire; refusing to count nulls")
        return 2
    AES.new = audited_new
    for script in sys.argv[1:]:
        STATS.clear()
        FLAGGED.clear()
        t0 = time.time()
        argv = sys.argv
        sys.argv = [script]
        try:
            runpy.run_path(script, run_name="__main__")
        except SystemExit:
            pass
        finally:
            sys.argv = argv
        locked = {k: v for k, v in STATS.items() if k in ("terminal", "salphaseion_short", "cosmic")}
        n = sum(v["decrypts"] for v in locked.values())
        out = {
            "script": script,
            "seconds": round(time.time() - t0, 1),
            "controls": ctl,
            "per_container": STATS,
            "locked_decrypts": n,
            "locked_valid_pads": sum(v["valid_pads"] for v in locked.values()),
            "locked_expected_pads": round(n / 255, 1),
            "locked_flagged_bodies": sum(v["flag_body"] for v in locked.values()),
            "flagged_samples": FLAGGED,
        }
        dest = ART / f"audit_{Path(script).stem}.json"
        dest.write_text(json.dumps(out, indent=1) + "\n")
        print(f"AUDIT {script}: locked decrypts {n}, valid pads {out['locked_valid_pads']} "
              f"(expected {out['locked_expected_pads']}), flagged bodies {out['locked_flagged_bodies']}, "
              f"other {[(k, v['decrypts'], v['flag_body']) for k, v in STATS.items() if k not in locked]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
