#!/usr/bin/env python3
"""Doc 120: the two 80-byte envelopes under a full-padding gate.

Terminal (the 3.2 final block) and SalPhaseIon-short each hold 80 bytes of
ciphertext after the 16-byte Salted__ header, so a plaintext is 64-79 bytes.
A 64-character hex private key fills that with a full block of padding (pad
16), or pad 15 with a trailing newline.  Pad >= 15 by chance is about 2^-120
per attempt, so for these two envelopes the padding byte authenticates a hit
on its own; no legibility filter is needed.

Two stages, so the candidate list is frozen before any decryption runs:

    python3 tools/envelope_campaign.py prereg   # writes claude/doc120-runs/candidates.json + .sha256
    python3 tools/envelope_campaign.py run      # refuses to run if the list changed

Candidates are generated from repository files wherever possible (the
SalPhaseIon literals are decoded from the textarea, the leftovers come from the
decrypted phase-2 and phase-3.2 plaintexts).  Only puzzle text is used.

Controls, all required to pass before a negative is reported:
  * retrodiction: phases 2, 3 and 3.2 open through this same password and KDF
    code with their known answers;
  * planted envelopes: synthetic 96-byte envelopes holding a hex key (pad 16,
    pad 15) under each KDF must be flagged, and the key must hit a planted
    target in the Better Half slot of tools/prize_gate.py;
  * the observed valid-padding count must sit near its chance expectation.

Needs pycryptodome (as the rest of tools/) and, for speed, coincurve.
"""

from __future__ import annotations

import base64
import hashlib
import itertools
import json
import math
import os
import re
import sys
import time

from Crypto.Cipher import AES

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
OUT = os.path.join(ROOT, "claude", "doc120-runs")
sys.path.insert(0, TOOLS)
import prize_gate  # noqa: E402

LIST_PATH = os.path.join(OUT, "candidates.json")
DIGEST_PATH = os.path.join(OUT, "candidates.sha256")
RESULT_PATH = os.path.join(OUT, "results.json")
LEDGER_PATH = os.path.join(OUT, "pair_ledger.tsv")


def rd(name, mode="r"):
    with open(os.path.join(ROOT, name), mode) as fh:
        return fh.read()


# --------------------------------------------------------------------------
# OpenSSL envelope primitives (same derivations as tools/setup.py, chk_flags.py)
# --------------------------------------------------------------------------

def evp(pw: bytes, salt: bytes, md) -> tuple[bytes, bytes]:
    d, prev = b"", b""
    while len(d) < 48:
        prev = md(prev + pw + salt).digest()
        d += prev
    return d[:32], d[32:48]


def derive(pw: bytes, salt: bytes, kdf: str) -> tuple[bytes, bytes]:
    if kdf == "evp-sha256":
        return evp(pw, salt, hashlib.sha256)
    if kdf == "evp-md5":
        return evp(pw, salt, hashlib.md5)
    if kdf == "pbkdf2-sha256-10000":  # openssl enc -pbkdf2 default
        d = hashlib.pbkdf2_hmac("sha256", pw, salt, 10000, 48)
        return d[:32], d[32:]
    raise ValueError(kdf)


def pad_of(raw: bytes, pw: bytes, kdf: str) -> int:
    """PKCS#7 pad length of the last block, 0 if invalid.  Decrypts one block."""
    key, iv = derive(pw, raw[8:16], kdf)
    ct = raw[16:]
    prev = ct[-32:-16] if len(ct) >= 32 else iv
    last = bytes(a ^ b for a, b in zip(AES.new(key, AES.MODE_ECB).decrypt(ct[-16:]), prev))
    p = last[-1]
    return p if 1 <= p <= 16 and last[-p:] == bytes([p]) * p else 0


def decrypt(raw: bytes, pw: bytes, kdf: str) -> bytes | None:
    key, iv = derive(pw, raw[8:16], kdf)
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(raw[16:])
    p = pt[-1]
    return pt[:-p] if 1 <= p <= 16 and pt[-p:] == bytes([p]) * p else None


def encrypt(plain: bytes, pw: bytes, salt: bytes, kdf: str) -> bytes:
    key, iv = derive(pw, salt, kdf)
    p = 16 - len(plain) % 16
    return b"Salted__" + salt + AES.new(key, AES.MODE_CBC, iv).encrypt(plain + bytes([p]) * p)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# Password forms: forms 0-3 match tools/chk_flags.py; the rest are the
# passwordsgenerator.net upper-case hex, `echo | sha256sum` newline, and raw.
TRANSFORMS = {
    "sha256hex":       lambda s: sha(s).encode(),                                      # form 0
    "sha256digest":    lambda s: hashlib.sha256(s).digest(),                           # form 1
    "sha256(digest)":  lambda s: sha(hashlib.sha256(s).digest()).encode(),             # form 2
    "sha256(hex)":     lambda s: sha(sha(s).encode()).encode(),                        # form 3
    "SHA256HEX":       lambda s: sha(s).upper().encode(),
    "sha256hex(s+lf)": lambda s: sha(s + b"\n").encode(),
    "raw":             lambda s: s,
}
PLAN = [(t, k) for t in TRANSFORMS for k in ("evp-sha256", "evp-md5")] + \
       [(t, "pbkdf2-sha256-10000") for t in ("raw", "sha256hex", "SHA256HEX")]


# The same recogniser as tools/chk_flags.py, applied to every valid pad.
def recog(p: bytes):
    n = len(p)
    if n < 8:
        return None
    pr = sum(1 for c in p if 32 <= c < 127 or c in (9, 10, 13)) / n
    if pr >= 0.8:
        return "printable %.2f" % pr
    sd = math.sqrt(n / 4)
    for b in range(8):
        if abs((sum(1 for c in p if c >> b & 1) - n / 2) / sd) >= 6:
            return "bitbias"
    nd = len(set(p)); q = 1 - 1 / 256; e = 256 * (1 - q ** n)
    v = 256 * 255 * (1 - 2 / 256) ** n + 256 * q ** n - 65536 * q ** (2 * n)
    if v > 0 and (nd - e) / math.sqrt(v) <= -6:
        return "distinct"
    if n >= 16 and sum(1 for i in range(1, n, 2) if p[i] == 0) / (n / 2) >= 0.6:
        return "utf16"
    if b"Salted__" in p:
        return "nestedsalt"
    if p[:3] == b"\x1f\x8b\x08" or p[:4] in (b"PK\x03\x04", b"\x89PNG", b"%PDF"):
        return "magic"
    return None


# --------------------------------------------------------------------------
# Inputs, all derived from repository files
# --------------------------------------------------------------------------

def containers() -> dict[str, bytes]:
    out = {}
    expect = {"terminal": "291dfd6f3e759ec2e272b35a00c24907da70c3e7a9291b4c13605c7b0b4f3de9",
              "salphaseion-short": "9e2831e1b34b5f34796df47ccaf6530d48d371c61a6bff84d60db1064fa7a258"}
    for name, digest in expect.items():
        raw = base64.b64decode("".join(rd(name + ".b64").split()))
        assert sha(raw) == digest and len(raw) == 96 and raw[:8] == b"Salted__", name
        out[name] = raw
    return out


def textarea_literals() -> dict[str, str]:
    t = rd("salphaseion-textarea.txt").strip()
    ab = []
    for m in re.finditer(r"[ab]{24,}", t):
        bits = "".join("0" if c == "a" else "1" for c in m.group())
        ab.append(bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits) // 8 * 8, 8)).decode())
    digit = {c: str(i + 1) for i, c in enumerate("abcdefghi")}
    digit["o"] = "0"
    z = []
    for part in t[t.index("zagdaf"):t.index("shabef")].split("z"):
        if part:
            n = int("".join(digit[c] for c in part))
            z.append(n.to_bytes((n.bit_length() + 7) // 8, "big").decode())
    found = {"matrixsumlist": ab[0], "enter": ab[1], "lastwordsbeforearchichoice": z[0], "thispassword": z[1]}
    for want, got in found.items():
        assert want == got, (want, got)
    tails = re.findall(r"sha[a-z]+", t)
    return {"literals": list(found), "textarea_tails": tails}


def phase_chain() -> dict[str, bytes]:
    """Open phases 2, 3 and 3.2 with their known answers through derive()."""
    def open_with(raw, answer):
        return decrypt(raw, TRANSFORMS["sha256hex"](answer.encode()), "evp-sha256")

    raw2 = base64.b64decode("".join(rd("phase2.b64").split()))
    pt2 = open_with(raw2, "causality")
    doss = rd("claude/GSMG-PUZZLE-DOSSIER.md")
    m = re.search(r"The answer is the plain concatenation of seven parts:\n\n(.*?)\nPart 6 is", doss, re.S)
    parts = [re.match(r"\d\. `(.*)`$", l).group(1) for l in m.group(1).split("\n") if re.match(r"\d\. `", l)]
    raw3 = base64.b64decode("".join(rd("phase3.b64").split()))
    pt3 = open_with(raw3, "".join(parts))
    raw32 = base64.b64decode(pt3[pt3.find(b"U2FsdGVkX1"):].decode().strip())
    ans32 = "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
    assert ans32 in doss
    pt32 = open_with(raw32, ans32)
    return {"pt2": pt2, "pt3": pt3, "pt32": pt32, "raw2": raw2, "raw3": raw3, "raw32": raw32,
            "ans3": "".join(parts), "ans32": ans32}


def forms(p: str) -> list[str]:
    """As written, lower alphanumeric, upper alphanumeric."""
    squeeze = re.sub(r"[^0-9A-Za-z]", "", p)
    return list(dict.fromkeys([p, squeeze.lower(), squeeze.upper()]))




def build_candidates() -> dict:
    lit = textarea_literals()
    chain = phase_chain()
    pt2 = chain["pt2"].decode("latin-1")
    pt32 = chain["pt32"].decode("latin-1")
    groups: dict[str, list[dict]] = {}

    def add(group, text, source):
        for f in forms(text):
            groups.setdefault(group, []).append({"s": f, "src": source})

    # G1: every ordered selection of the four literals, three joiners, two cases.
    L = lit["literals"]
    for k in range(1, 5):
        for seq in itertools.permutations(L, k):
            for joiner in ([""] if k == 1 else ["", " ", "\n"]):
                s = joiner.join(seq)
                for case in (s, s.upper()):
                    groups.setdefault("G1_literals", []).append({"s": case, "src": "textarea literals"})

    # G2: the textarea's own trailing strings and the first hint they name.
    for t in lit["textarea_tails"]:
        add("G2_textarea", t, "textarea")
        add("G2_textarea", t[3:], "textarea, 'sha' prefix removed")
    add("G2_textarea", "theflowerblossomsthroughwhatseemstobeaconcretesurface", "phase 1 answer (first hint)")
    add("G2_textarea", "5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75", "first hint hash, jrk #225")

    # G3: phase-2 leftovers (the X2SH template and its clue lines).
    lines = [l.strip() for l in pt2.replace("\r", "").split("\n") if l.strip()]
    for l in lines[1:]:
        add("G3_phase2", l, "phase 2 plaintext line")
    x2sh = next(l for l in lines if l.startswith("# X 2 S H"))
    add("G3_phase2", x2sh.strip("# ").strip(), "phase 2 template")
    m = re.search(r"\{(.*?)\}", lines[0])
    add("G3_phase2", m.group(1), "phase 2 braces")
    vals = {"Q": "82", "B": "25", "S": "32"}
    for h in ("42", "-42"):  # the sign the dossier says is unresolved
        v = dict(vals, H=h)
        seq = x2sh.strip("# ").split()
        add("G3_phase2", "".join(v.get(c, c) for c in seq), "X2SH substituted, H=" + h)
        add("G3_phase2", "".join(v.get(c, c) for c in reversed(seq)), "X2SH reversed, H=" + h)
        add("G3_phase2", "Q%sB%sH%sS%s" % (v["Q"], v["B"], v["H"], v["S"]), "X2SH values, H=" + h)
    for c in ("51°52'28.0\"N 4°24'23.2\"E", "51 52 28.0 N 4 24 23.2 E", "51.874444,4.406444",
              "51.874444, 4.406444", "51.8744,4.4064", "5152280N4242320E", "5152280424232"):
        add("G3_phase2", c, "X2SH coordinate (dossier 3.2)")

    # G4: phase-3.2 text outside the Architect block, and the checkerboard message.
    head, tail = pt32[:447], pt32[1986:]
    for part in re.split(r"(?<=[.?!])\s+", head.strip()) + [l for l in tail.split("\n") if l.strip()
                                                             and not l.startswith(("U2Fs", "gKlI"))]:
        add("G4_phase32", part.strip(), "phase 3.2 plaintext")
    add("G4_phase32", rd("checkerboard_vic_91.txt").split()[0], "checkerboard message")
    add("G4_phase32", "halfandbetterhalf", "checkerboard message")

    # G5: each literal joined to each lower-case G2-G4 string, both orders.
    others = sorted({c["s"] for g in ("G2_textarea", "G3_phase2", "G4_phase32") for c in groups[g]
                     if c["s"] == c["s"].lower()})
    for a in L:
        for b in others:
            groups.setdefault("G5_pairs", []).append({"s": a + b, "src": f"pair {a} + G2-4"})
            groups.setdefault("G5_pairs", []).append({"s": b + a, "src": f"pair G2-4 + {a}"})

    seen, out = set(), {}
    for g, items in groups.items():
        out[g] = []
        for it in items:
            if it["s"] not in seen:
                seen.add(it["s"])
                out[g].append(it)
    return {"doc": 120, "created": time.strftime("%Y-%m-%d"), "plan": [list(p) for p in PLAN],
            "containers": ["terminal", "salphaseion-short"], "gate": "pad >= 15, or recogniser, or prize_gate hit",
            "groups": out}


def prereg() -> int:
    os.makedirs(OUT, exist_ok=True)
    data = json.dumps(build_candidates(), indent=1, ensure_ascii=False, sort_keys=True).encode() + b"\n"
    with open(LIST_PATH, "wb") as fh:
        fh.write(data)
    with open(DIGEST_PATH, "w", newline="\n") as fh:
        fh.write(sha(data) + "  candidates.json\n")
    spec = json.loads(data)
    print({g: len(v) for g, v in spec["groups"].items()}, "digest", sha(data))
    return 0


# --------------------------------------------------------------------------
# Controls and the run
# --------------------------------------------------------------------------

def controls(chain) -> dict:
    res = {}
    res["retro_phase2"] = sha(chain["pt2"]).startswith("e2f9dd65") and len(chain["pt2"]) == 648
    res["retro_phase3"] = sha(chain["pt3"]).startswith("c4ad9455") and len(chain["pt3"]) == 4090
    res["retro_phase32"] = sha(chain["pt32"]).startswith("b82afeb8") and len(chain["pt32"]) == 2422
    # the same attempt path the campaign uses
    res["retro_attempt_path"] = all(
        pad_of(raw, TRANSFORMS["sha256hex"](ans.encode()), "evp-sha256") > 0
        for raw, ans in ((chain["raw2"], "causality"), (chain["raw3"], chain["ans3"]), (chain["raw32"], chain["ans32"])))
    key = hashlib.sha256(b"doc120 planted key").digest()
    unc, comp = prize_gate.public_keys(int.from_bytes(key, "big"))
    planted_targets = {"half": prize_gate.HALF_H160, "better_half": prize_gate.hash160(comp)}
    plants = [("pad16", key.hex().encode(), "sha256hex", "evp-sha256"),
              ("pad15", key.hex().encode() + b"\n", "SHA256HEX", "evp-md5"),
              ("pbkdf2", key.hex().upper().encode(), "raw", "pbkdf2-sha256-10000")]
    for label, plain, tname, kdf in plants:
        phrase = ("doc120 control " + label).encode()
        env = encrypt(plain, TRANSFORMS[tname](phrase), hashlib.sha256(phrase).digest()[:8], kdf)
        assert len(env) == 96
        flagged = attempt_all(env, phrase, planted_targets)
        res["planted_" + label] = any(r["pad"] >= 15 and r["prize"] for r in flagged)
    return res


def attempt_all(raw: bytes, s: bytes, targets=None) -> list[dict]:
    """Every (transform, KDF) attempt on one envelope; returns valid-pad records."""
    out = []
    for tname, kdf in PLAN:
        pw = TRANSFORMS[tname](s)
        p = pad_of(raw, pw, kdf)
        if not p:
            continue
        body = decrypt(raw, pw, kdf)
        hits, _ = prize_gate.gate_plaintext(body, targets=targets)
        out.append({"transform": tname, "kdf": kdf, "pad": p, "body_hex": body.hex(),
                    "recog": recog(body), "prize": [h["matches"] for h in hits]})
    return out


def run() -> int:
    data = open(LIST_PATH, "rb").read()
    want = open(DIGEST_PATH).read().split()[0]
    if sha(data) != want:
        print("candidates.json changed after preregistration; refusing to run")
        return 1
    if not prize_gate.selftest(verbose=False):
        print("prize_gate selftest failed")
        return 1
    spec = json.loads(data)
    chain = phase_chain()
    ctl = controls(chain)
    if not all(ctl.values()):
        print("control failed:", ctl)
        return 1
    envs = containers()
    t0 = time.time()
    attempts, pads, valid, flags = 0, {}, [], []
    with open(LEDGER_PATH, "w", newline="\n") as ledger:
        ledger.write("group\tcandidate\tcontainers\tforms\n")
        for g, items in spec["groups"].items():
            for idx, it in enumerate(items):
                s = it["s"].encode()
                if g == "G5_pairs":
                    ledger.write(f"{g}\t{it['s']!r}\tterminal,salphaseion-short\t{len(PLAN)}\n")
                for cname, raw in envs.items():
                    attempts += len(PLAN)
                    for rec in attempt_all(raw, s):
                        rec.update(group=g, index=idx, candidate=it["s"], container=cname)
                        pads[rec["pad"]] = pads.get(rec["pad"], 0) + 1
                        valid.append(rec)
                        if rec["pad"] >= 15 or rec["recog"] or rec["prize"]:
                            flags.append(rec)
    expect = attempts * sum(256.0 ** -p for p in range(1, 17))
    result = {"doc": 120, "candidates_sha256": want, "controls": ctl,
              "counts": {g: len(v) for g, v in spec["groups"].items()},
              "attempts": attempts, "valid_pads": len(valid), "valid_pads_expected": round(expect, 1),
              "pad_histogram": {str(k): v for k, v in sorted(pads.items())},
              "flags": flags, "valid_pad_records": valid,
              "prize_gate_version": prize_gate.__version__, "seconds": round(time.time() - t0, 1)}
    with open(RESULT_PATH, "w", newline="\n") as fh:
        json.dump(result, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps({k: result[k] for k in ("controls", "counts", "attempts", "valid_pads",
                                             "valid_pads_expected", "pad_histogram", "seconds")}, indent=1))
    print("FLAGS:", len(flags))
    return 3 if flags else 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    sys.exit(prereg() if cmd == "prereg" else run() if cmd == "run" else print(__doc__) or 2)
