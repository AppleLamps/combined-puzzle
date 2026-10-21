#!/usr/bin/env python3
"""
What is actually still encrypted in the GSMG puzzle, and one trap in it.

Phase 3.2's envelope IS decrypted, and has been since 2020. So are both of the
sections inside it (3.2.1 via EBCDIC-1141 + Beaufort, 3.2.2 via a VIC cipher).
What remains is exactly TWO AES-256-CBC blobs.

This script:
  1. decrypts the Phase 3.2 envelope from analysis/phase32_blob.txt, to show the
     chain is real and self-validating
  2. checks the structural integrity of both remaining blobs

The trap: the SalPhaseIon text uses "z" as a segment separator, and the blob's
first half legitimately ENDS in "z". Strip that as a separator and you get 127
base64 characters -> 79 bytes of ciphertext -> 4.94 AES blocks, which cannot
decrypt under ANY password. That truncated form circulates.

Needs openssl on PATH for step 1. Run from the repo root: python3 analysis/blobs.py
"""
import base64, os, subprocess, sys

HERE = os.path.dirname(__file__)
P32_PASS = "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c"

INNER = ("U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z"
         "gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4")

# SalPhaseIon, with the 40-character a/b run that spells "enter" already removed.
SALPH_OK = ("U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z"
            "QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ")
SALPH_BAD = SALPH_OK.replace("rd9z", "rd9", 1)     # the "z" mistaken for a separator


def check(name, b64):
    pad = b64 + "=" * ((4 - len(b64) % 4) % 4)
    raw = base64.b64decode(pad)
    body = len(raw) - 16
    ok = body > 0 and body % 16 == 0
    print(f"  {name}")
    print(f"     {len(b64)} base64 chars -> {len(raw)} bytes")
    print(f"     magic {raw[:8].decode('latin1')!r}  salt {raw[8:16].hex()}")
    print(f"     ciphertext {body} bytes = {body/16:.2f} AES blocks  "
          f"{'VALID' if ok else 'INVALID -- cannot decrypt under any password'}")
    return ok


def main():
    print("1. THE PHASE 3.2 ENVELOPE IS DECRYPTED\n")
    path = os.path.join(HERE, "phase32_blob.txt")
    if os.path.exists(path):
        try:
            out = subprocess.run(
                ["openssl", "enc", "-aes-256-cbc", "-d", "-a", "-in", path,
                 "-pass", "pass:" + P32_PASS],
                capture_output=True, timeout=30)
            head = out.stdout.decode("latin1").strip().splitlines()
            if head:
                print(f"   password = SHA256('jacquefrescogiveitjustonesecond"
                      f"heisenbergsuncertaintyprinciple')\n            = {P32_PASS}\n")
                print(f"   plaintext opens: {head[0][:96]}...")
                print("   -> a clean decrypt is a checksum. This step is proven.\n")
            else:
                print("   openssl produced no output:",
                      out.stderr.decode('latin1')[:200], "\n")
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"   skipped ({e}) -- openssl not available\n")
    else:
        print(f"   skipped -- {path} not found\n")

    print("2. WHAT IS STILL ENCRYPTED: exactly two blobs\n")
    check("Phase 3.2, inner blob (the main line)", INNER)
    print()
    check("SalPhaseIon blob, 'z' kept (correct)", SALPH_OK)
    print()
    check("SalPhaseIon blob, 'z' stripped as a separator", SALPH_BAD)
    print("\n   The SalPhaseIon page uses 'z' to separate segments, and this blob's"
          "\n   first half ends in one. Removing it looks like tidying and is fatal.")


if __name__ == "__main__":
    main()
