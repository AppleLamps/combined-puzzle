#!/usr/bin/env python3
"""Round 5 pilot per ledger/round5/tester.md (~15.8k decrypts)."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "team"))
ART = ROOT / "artifacts"

from crypto_known import evp_bytes_to_key, pkcs7_unpad  # noqa: E402
from Crypto.Cipher import AES  # noqa: E402
from step1_btcseed import classify  # noqa: E402
from step3_mask import tok23  # noqa: E402
from cryptanalyst_tests import CONTAINERS, planted_control, record, results, try_password  # noqa: E402
from round3_battery import word_lastwords_candidates  # noqa: E402
from round4_battery import decrypt_mdp5_bytes, filler_bytes, filler_deleted  # noqa: E402

TERMINAL = (ART / "terminal.bin").read_bytes()
SAL_SHORT = (ART / "salphaseion_short.bin").read_bytes()
COSMIC = (ART / "cosmic.bin").read_bytes()
BLOBS = {"terminal": TERMINAL, "salphaseion_short": SAL_SHORT, "cosmic": COSMIC}
FILLERS = (ART / "yellowblue_fillers.txt").read_text().strip()
ARCH = (ART / "phase32_beaufort.txt").read_text().strip()
COMMUNITY = "matrixsumlistenterlastwordsbeforearchichoicethispasswordmatrixsumlist"
COMMUNITY_SHA = "1449a2178eea7c0e3fabac8c1ad2afa294be4fc1800c594a025a056e88c626bf"

hits_sha: list[dict] = []
hits_md5: list[dict] = []
sha_tries = 0
md5_tries = 0
pads_md5 = {"terminal": 0, "salphaseion_short": 0, "cosmic": 0}


def spiral_row_sums() -> list[int]:
    spiral = (ART / "poster_spiral_bits.txt").read_text().strip()
    groups = [spiral[i : i + 14] for i in range(0, len(spiral), 14)]
    return [sum(int(c) for c in g) for g in groups]


def h1_recipe_candidates() -> set[str]:
    S = spiral_row_sums()
    out: set[str] = set()
    lws = [v for _, v in word_lastwords_candidates()]
    joins = {
        "": "".join(str(x) for x in S),
        "-": "-".join(str(x) for x in S),
        ",": ",".join(str(x) for x in S),
        "enter": "enter".join(str(x) for x in S),
    }
    # Ban raw join "" as standalone password — only inside templates
    for jname, msl_join in joins.items():
        if jname == "":
            continue
        for lw in lws:
            out.add(f"matrixsumlist{msl_join}enter{lw}thispassword{msl_join}")
            out.add(f"yellowblueprimes{msl_join}enter{lw}yinyang")
            out.add(f"{tok23()}{msl_join}enter{lw}thispassword")
            out.add(f"matrixsumlist{msl_join}enterlastwordsbeforearchichoicethispassword{msl_join}")
            for si in S:
                out.add(f"matrixsumlist{si}enter{lw}thispassword{si}")
    out.add(COMMUNITY)
    out.add(tok23())
    return out


def h2_after_select_candidates() -> set[str]:
    sel = ARCH.find("SELECT")
    after = ARCH[sel + 6 :]
    out: set[str] = set()
    out.add(after.lower())
    out.add(after.upper())
    for n in (16, 32, 64, 128, 256):
        out.add(after[:n].lower())
    raw = after.encode("latin-1", errors="replace")
    out.add(raw.decode("latin-1", errors="replace"))
    out.add(raw.hex())
    for frag in (after[:64].lower(), after[:128].lower()):
        out.add(f"matrixsumlist{frag}enterlastwordsbeforearchichoicethispassword{frag}")
    return out


def all_curated_strings() -> list[str]:
    return sorted(h1_recipe_candidates() | h2_after_select_candidates())


def try_sha(answer: str, label: str) -> None:
    global sha_tries
    sha_tries = try_password(answer, label, hits_sha, sha_tries)
    sha_tries = try_password(
        hashlib.sha256(answer.encode()).hexdigest(), f"{label}:sha256hex", hits_sha, sha_tries
    )


def mdp5_variants(answer: str) -> dict[str, bytes]:
    d = hashlib.sha256(answer.encode()).digest()
    hx = hashlib.sha256(answer.encode()).hexdigest().encode()
    hx2 = hashlib.sha256(hx).hexdigest().encode()
    return {
        "plain": answer.encode(),
        "sha256hex-ascii": hx,
        "sha256-raw32": d,
        "md5hex-of-plain": hashlib.md5(answer.encode()).hexdigest().encode(),
        "sha256hex2-ascii": hx2,
    }


def try_mdp5_all(answer: str, label: str) -> None:
    global md5_tries
    for suffix, pw in mdp5_variants(answer).items():
        for cname, raw in BLOBS.items():
            body, _ = decrypt_mdp5_bytes(raw, pw)
            md5_tries += 1
            if body is not None:
                pads_md5[cname] += 1
                kind = classify(body)
                if kind.startswith("structured"):
                    hits_md5.append(
                        {"label": f"{label}:{suffix}", "container": cname, "kind": kind, "len": len(body)}
                    )


def md5_planted_roundtrip(pw_bytes: bytes, tag: str) -> bool:
    plain = f"ROUND5_MD5_PLANTED_{tag}".encode()
    pad = 16 - (len(plain) % 16)
    padded = plain + bytes([pad]) * pad
    salt = b"round5sa"
    key, iv = evp_bytes_to_key(pw_bytes, salt, md=hashlib.md5)
    ct = AES.new(key, AES.MODE_CBC, iv).encrypt(padded)
    raw = b"Salted__" + salt + ct
    body, _ = decrypt_mdp5_bytes(raw, pw_bytes)
    return body == plain


def quintuple_sample(n_sample: int = 4096) -> list[tuple[int, ...]]:
    all_c = list(itertools.combinations(range(len(FILLERS)), 5))
    total = len(all_c)
    step = max(1, total // n_sample)
    return [all_c[i] for i in range(0, total, step)][:n_sample]


def main() -> int:
    global sha_tries
    results.clear()

    # Controls
    planted_control()
    body, _ = decrypt_mdp5_bytes(SAL_SHORT, COMMUNITY.encode())
    record("MD5 community Sal-short 79B", body is not None and len(body) == 79, f"sha={hashlib.sha256(body).hexdigest() if body else ''}")
    if body:
        record("MD5 community body sha256", hashlib.sha256(body).hexdigest() == COMMUNITY_SHA)

    pw1 = hashlib.sha256(b"round5-md5-planted-v1").hexdigest().encode()
    pw2 = hashlib.sha256(b"round5-md5-planted-v2").digest()
    record("MD5 planted sha256hex-ascii roundtrip", md5_planted_roundtrip(pw1, "HEX"))
    record("MD5 planted raw32 roundtrip", md5_planted_roundtrip(pw2, "RAW"))

    curated = all_curated_strings()
    record("curated unique strings", len(curated) >= 160, str(len(curated)))

    for i, ans in enumerate(curated):
        try_sha(ans, f"r5-curated-{i}")
        try_mdp5_all(ans, f"r5-curated-{i}")

    for idx in quintuple_sample():
        deleted = filler_deleted(idx)
        hx = hashlib.sha256(filler_bytes(deleted)).hexdigest()
        sha_tries = try_password(hx, f"r5-quint-{idx[0]}-{idx[4]}", hits_sha, sha_tries)

    report = {
        "curated_strings": len(curated),
        "sha_decrypts": sha_tries,
        "md5_decrypts": md5_tries,
        "sha_structured": len(hits_sha),
        "md5_structured": len(hits_md5),
        "md5_pads_by_container": pads_md5,
        "quintuple_sample": len(quintuple_sample()),
        "hits_md5": hits_md5,
        "hits_sha": hits_sha,
    }
    (ART / "round5_battery.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"round5: curated={len(curated)} sha={sha_tries} md5={md5_tries} "
        f"structured sha={len(hits_sha)} md5={len(hits_md5)} pads={pads_md5}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
