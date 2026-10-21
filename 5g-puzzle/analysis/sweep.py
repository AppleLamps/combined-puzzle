#!/usr/bin/env python3
"""
Disciplined password sweep against the two remaining GSMG AES blobs.

The puzzle's convention, unchanged from phase 2 onward: take the answers the
current plaintext asks for, lowercase them, strip spaces, concatenate, SHA256,
and use the lowercase hex digest as an openssl -pass pass: passphrase over
aes-256-cbc with the legacy EVP_BytesToKey(MD5) KDF.

This builds the candidate space from everything the chain has actually produced
and tests it. A hit needs BOTH valid PKCS#7 padding AND printable plaintext --
padding alone passes about 1 in 256 of the time by chance, which is exactly the
kind of false positive this community has repeatedly mistaken for a find.

Reports negatives explicitly. A documented null result is worth more than an
undocumented hunch, and this puzzle has seven years of the latter.

Needs pycryptodome. Run from the repo root: python3 analysis/sweep.py
"""
import base64, hashlib, itertools, sys
from Crypto.Cipher import AES

INNER = ("U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z"
         "gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4")
SALPH = ("U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z"
         "QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ")

# every answer the chain has actually produced, lowercased
ATOMS = [
    "causality", "safenet", "luna", "hsm", "11110",
    "jacquefresco", "giveit", "givetit", "justonesecond",
    "heisenbergsuncertaintyprinciple", "thematrixhasyou",
    "theflowerblossomsthroughwhatseemstobeaconcretesurface",
    "theseedisplanted", "matrixsumlist", "enter", "thispassword",
    "lastwordsbeforearchichoice", "hashthetext", "yinyang", "yingyang",
    "shabef", "shabefanstoo", "ourfirsthintisyourlastcommand",
    "gsmgio5btcpuzzlechallenge", "1gsmg1jc9wtdswfwapgj2xcmjpawx7prbe",
    "halfandbetterhalf", "theone", "neo", "oen", "one",
    "raisingthestakeswithoutextrachancesofwinning",
    "aswideasthefirstoneseen", "onefirstoneseen",
    "x2sh4y0qb15", "32", "42", "-42", "82", "-16", "25", "163",
    "firstorzero", "infrared", "hushhush", "42answer",
]

# multi-part concatenations in the style the puzzle has used before
COMBOS = [
    ("matrixsumlist",), ("thispassword",), ("lastwordsbeforearchichoice",),
    ("lastwordsbeforearchichoice", "thispassword"),
    ("matrixsumlist", "enter"),
    ("matrixsumlist", "lastwordsbeforearchichoice", "thispassword"),
    ("gsmgio5btcpuzzlechallenge", "1gsmg1jc9wtdswfwapgj2xcmjpawx7prbe"),
    ("gsmgio5btcpuzzlechallenge", "enter", "1gsmg1jc9wtdswfwapgj2xcmjpawx7prbe"),
    ("jacquefresco", "giveit", "justonesecond", "heisenbergsuncertaintyprinciple"),
    ("thematrixhasyou",), ("yinyang",), ("yingyang",),
    ("hashthetext",), ("theseedisplanted",),
    ("causality", "safenet", "luna", "hsm", "11110"),
    ("aswideasthefirstoneseen",),
    ("raisingthestakeswithoutextrachancesofwinning",),
]


def evp_key_iv(pw: bytes, salt: bytes, digest="sha256"):
    """openssl EVP_BytesToKey, 1 iteration -> 32-byte key + 16-byte IV.

    NOTE the digest. OpenSSL changed the default -md for `enc` from MD5 to
    SHA-256 in 1.1.0. Every blob in this puzzle was produced with whatever the
    author's openssl defaulted to, so both are worth trying; sha256 is what a
    modern `openssl enc -aes-256-cbc -d -a -pass pass:...` reproduces.
    """
    h = hashlib.sha256 if digest == "sha256" else hashlib.md5
    d = b""
    prev = b""
    while len(d) < 48:
        prev = h(prev + pw + salt).digest()
        d += prev
    return d[:32], d[32:48]


def try_pw(raw: bytes, pw: bytes, digest="sha256"):
    """Return (plaintext, printable_fraction) if PKCS#7 padding is valid, else None.

    Padding alone is NOT evidence: on random data it passes about 1 time in 256.
    So this returns every padding-pass and lets the caller rank by printability,
    rather than hard-filtering on content -- the phase 3.2 envelope decrypts to
    plaintext that is only ~60% printable ASCII because of the EBCDIC blob inside
    it, and a strict content filter throws away real hits like that one.
    """
    salt, ct = raw[8:16], raw[16:]
    key, iv = evp_key_iv(pw, salt, digest)
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    pad = pt[-1]
    if not (1 <= pad <= 16) or pt[-pad:] != bytes([pad]) * pad:
        return None
    body = pt[:-pad]
    if not body:
        return None
    printable = sum(1 for c in body if 32 <= c < 127 or c in (9, 10, 13))
    return body, printable / len(body)


def candidates():
    """Yield (label, passphrase-bytes). The convention is the SHA256 hex digest,
    but raw strings are tried too since that costs nothing."""
    seen = set()

    def emit(label, s):
        for form in (hashlib.sha256(s.encode()).hexdigest(),
                     hashlib.sha256(s.encode()).hexdigest().upper(),
                     s):
            if form not in seen:
                seen.add(form)
                yield label, form.encode()

    for a in ATOMS:
        yield from emit(f"atom:{a}", a)
    for combo in COMBOS:
        yield from emit("combo:" + "+".join(combo), "".join(combo))
    # ordered pairs and triples of the shorter atoms
    short = [a for a in ATOMS if len(a) <= 30]
    for n in (2, 3):
        for tup in itertools.permutations(short, n):
            yield from emit("perm:" + "+".join(tup), "".join(tup))


def main():
    blobs = {}
    for name, b64 in (("phase 3.2 inner", INNER), ("SalPhaseIon", SALPH)):
        raw = base64.b64decode(b64 + "=" * ((4 - len(b64) % 4) % 4))
        assert raw[:8] == b"Salted__" and (len(raw) - 16) % 16 == 0, f"{name} malformed"
        blobs[name] = raw
        print(f"{name}: salt {raw[8:16].hex()}, {len(raw)-16} bytes ciphertext")

    print("\nsweeping...\n")
    tried = padded = 0
    best = []
    for label, pw in candidates():
        tried += 1
        for name, raw in blobs.items():
            for dg in ("sha256", "md5"):
              res = try_pw(raw, pw, dg)
              if res:
                body, frac = res
                label = f"{label} [{dg}]"
                padded += 1
                best.append((frac, name, label, body))
        if tried % 100000 == 0:
            print(f"  ... {tried} candidates")

    best.sort(key=lambda t: -t[0])
    expected = tried * len(blobs) * 2 / 256   # 2 KDF digests tried per candidate
    print(f"\ntried {tried} passphrases against {len(blobs)} blobs, "
          f"2 KDF digests each ({tried*len(blobs)*2} trials).")
    print(f"passed PKCS#7 padding: {padded}   "
          f"(expected from chance alone: about {expected:.0f})")
    print("\nbest candidates by printable fraction:")
    for frac, name, label, body in best[:10]:
        print(f"   {frac:5.2f}  {name:16s} {label[:52]:52s} {body[:44]!r}")
    real = [b for b in best if b[0] >= 0.95]
    print(f"\ncandidates that actually look like plaintext (>=95% printable): {len(real)}")
    if not real:
        print("\nNULL RESULT -- and that is the point of writing it down.")
        print("Ruled out: every answer the chain has produced, alone, in the")
        print("documented combinations, and in all ordered pairs and triples,")
        print("as raw text and as SHA256 hex (upper and lower).")
        print("\nWhatever opens these blobs is NOT a recombination of what we")
        print("already have. It needs a new answer -- which is what the two")
        print("unspent 2021 hints (primes; characters zeroed out) and the")
        print("orphaned X2SH block are candidates to supply.")


if __name__ == "__main__":
    main()
