#!/usr/bin/env python3
"""Re-run every candidate space through a STRUCTURAL detector, not a text filter.

Replaces the printability criterion used earlier in this audit. Reports the
PKCS#7 pad-value distribution, which is the sharp signal: on random data
P(pad==k) = 256^-k, so pad==1 is noise and anything above pad==2 is real.
A 64-byte plaintext gives pad==16, probability 2^-128 by chance.

Run from the repo root: python3 analysis/recheck.py
"""
import base64, collections, hashlib, itertools, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from Crypto.Cipher import AES
from inspect_pt import inspect
from sweep import evp_key_iv, INNER, SALPH, ATOMS, COMBOS

COSMIC_PATH = os.path.join(os.path.dirname(__file__), "cosmic_blob.txt")


def load_blobs():
    b = {"3.2 inner": INNER, "SalPhaseIon": SALPH}
    if os.path.exists(COSMIC_PATH):
        b["Cosmic Duality"] = open(COSMIC_PATH).read().strip()
    out = {}
    for n, s in b.items():
        raw = base64.b64decode(s + "=" * ((4 - len(s) % 4) % 4))
        out[n] = (raw[8:16], raw[16:])
    return out


def decrypt(salt, ct, pw, digest):
    k, iv = evp_key_iv(pw, salt, digest)
    return AES.new(k, AES.MODE_CBC, iv).decrypt(ct)


def candidates():
    seen = set()
    def emit(s):
        for f in (hashlib.sha256(s.encode()).hexdigest(),
                  hashlib.sha256(s.encode()).hexdigest().upper(), s):
            if f not in seen:
                seen.add(f); yield f
    for a in ATOMS: yield from emit(a)
    for c in COMBOS: yield from emit("".join(c))
    short = [a for a in ATOMS if len(a) <= 30]
    for n in (2, 3):
        for t in itertools.permutations(short, n):
            yield from emit("".join(t))


def main():
    blobs = load_blobs()
    print("blobs under test:", ", ".join(blobs))
    pads = collections.Counter()
    trials = 0
    findings = []
    for pw in candidates():
        pwb = pw.encode()
        for name, (salt, ct) in blobs.items():
            for dg in ("sha256", "md5"):
                trials += 1
                pt = decrypt(salt, ct, pwb, dg)
                p = pt[-1]
                if not (1 <= p <= 16) or pt[-p:] != bytes([p]) * p:
                    continue
                pads[p] += 1
                body = pt[:-p]
                if p >= 2 or len(body) in (32, 64):
                    hits = inspect(body)
                    findings.append((p, name, dg, pw[:40], hits, body[:48]))
                else:
                    hits = inspect(body, derive=False)
                    if hits:
                        findings.append((p, name, dg, pw[:40], hits, body[:48]))
    print(f"\ntrials: {trials}")
    print("\nPKCS#7 pad-value distribution (expected on noise: pad=1 only):")
    for k in sorted(pads):
        exp = trials / (256 ** k)
        print(f"   pad={k:2d}  observed {pads[k]:6d}   expected ~{exp:.2e}")
    print(f"\nstructural findings: {len(findings)}")
    for p, name, dg, pw, hits, body in findings[:20]:
        print(f"   pad={p:2d} {name:15s} [{dg}] {pw:40s} {hits} {body!r}")
    if not findings:
        print("   none. Every padding pass was pad=1 with unstructured content --")
        print("   which is exactly the noise rate, and says nothing was close.")


if __name__ == "__main__":
    main()
