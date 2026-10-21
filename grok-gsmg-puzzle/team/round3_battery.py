#!/usr/bin/env python3
"""Round 3: SalPhaseIon-short EVP-MD5, word lastwords, spiral/diag MSL, filler pair deletion."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
ART = ROOT / "artifacts"

from crypto_known import decrypt_salted, evp_bytes_to_key, pkcs7_unpad, is_win_uncompressed  # noqa: E402
from Crypto.Cipher import AES  # noqa: E402
from step1_btcseed import classify  # noqa: E402
from step3_mask import matrix_strings, tok23  # noqa: E402

sys.path.insert(0, str(ROOT / "team"))
from cryptanalyst_tests import message_8446_text, planted_control, record, results, try_password  # noqa: E402

SAL_SHORT = (ART / "salphaseion_short.bin").read_bytes()
FILLERS = (ART / "yellowblue_fillers.txt").read_text().strip()
ARCH = (ART / "phase32_beaufort.txt").read_text().strip()
COMMUNITY_RECIPE = (
    "matrixsumlistenterlastwordsbeforearchichoicethispasswordmatrixsumlist"
)
COMMUNITY_SHA256 = "1449a2178eea7c0e3fabac8c1ad2afa294be4fc1800c594a025a056e88c626bf"
PRINTABLE = set(range(32, 127))

hits_md5: list[dict] = []
hits_sha: list[dict] = []
decrypts_md5 = 0
decrypts_sha = 0


def spiral_coords(n: int = 14):
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    r = c = di = 0
    seen = set()
    order = []
    for _ in range(n * n):
        order.append((r, c))
        seen.add((r, c))
        nr, nc = r + dirs[di][0], c + dirs[di][1]
        if not (0 <= nr < n and 0 <= nc < n) or (nr, nc) in seen:
            di = (di + 1) % 4
            nr, nc = r + dirs[di][0], c + dirs[di][1]
        r, c = nr, nc
    return order


def poster_sums() -> dict[str, str]:
    import json

    m = json.loads((ART / "matrix.json").read_text())
    grid = m["letters"]
    bit = m["bit_grid"]
    rows = [sum(int(c) for c in row) for row in bit]
    cols = [sum(int(bit[r][c]) for r in range(14)) for c in range(14)]
    main_diag = sum(int(bit[i][i]) for i in range(14))
    anti_diag = sum(int(bit[i][13 - i]) for i in range(14))

    order = spiral_coords()
    spiral_bits = []
    spiral_kb = []
    for r, c in order:
        spiral_bits.append(bit[r][c])
        spiral_kb.append(1 if grid[r][c] in "KB" else 0)
    spiral_bit_sum = sum(int(b) for b in "".join(spiral_bits))
    spiral_kb_sum = sum(spiral_kb)

    # colour weights B/Y/K/W/F counts on spiral path (B/Y/F coloured cells in spiral)
    colours = (ART / "poster_spiral_colours.txt").read_text().strip()
    spiral_by = sum(1 for ch in colours if ch == "B") + sum(2 for ch in colours if ch == "Y")

    return {
        "row": "".join(str(x) for x in rows),
        "col": "".join(str(x) for x in cols),
        "diag-main": str(main_diag),
        "diag-anti": str(anti_diag),
        "spiral-bits": str(spiral_bit_sum),
        "spiral-kb": str(spiral_kb_sum),
        "spiral-by-weight": str(spiral_by),
        "sum-rows": str(sum(rows)),
        "sum-cols": str(sum(cols)),
    }


def word_lastwords_candidates() -> list[tuple[str, str]]:
    sel = ARCH.find("SELECT")
    before = ARCH[:sel]
    out: list[tuple[str, str]] = []
    # Film line ends "... required to" before "select"
    for suffix in (
        "TO",
        "REQUIREDTO",
        "REQUIRED",
        "BEREQUIREDTO",
        "WILLBEREQUIREDTO",
        "YOUWILLBEREQUIREDTO",
        "PRIMEBASICS",
        "BASICS",
        "AFTERWHICHYOUWILLBEREQUIREDTO",
    ):
        if before.endswith(suffix):
            out.append((f"lw-word-{suffix.lower()}", suffix.lower()))
    # last k chars as pseudo-words
    for k in (2, 4, 6, 8, 10, 12):
        out.append((f"lw-tail-{k}", before[-k:].lower()))
    # spaced-script last token
    out.append(("lw-film-to", "to"))
    out.append(("lw-film-required", "required"))
    return out


def decrypt_mdp5(raw: bytes, password: str) -> tuple[bytes | None, bytes | None]:
    if raw[:8] != b"Salted__":
        return None, None
    salt, ct = raw[8:16], raw[16:]
    key, iv = evp_bytes_to_key(password.encode(), salt, md=hashlib.md5)
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    return pkcs7_unpad(pt), pt


def try_mdp5(password: str, label: str) -> None:
    global decrypts_md5
    body, full = decrypt_mdp5(SAL_SHORT, password)
    decrypts_md5 += 1
    if body is None:
        return
    kind = classify(body)
    if kind.startswith("structured"):
        hits_md5.append({"label": label, "password": password[:120], "kind": kind, "len": len(body)})
    rec = {
        "label": label,
        "password_sha256": hashlib.sha256(password.encode()).hexdigest(),
        "pad": full[-1] if full else None,
        "len": len(body),
        "printable": sum(b in PRINTABLE for b in body),
        "kind": kind,
    }
    if body is not None:
        rec["body_sha256"] = hashlib.sha256(body).hexdigest()


def filler_to_bytes(text: str) -> bytes:
    n = int("".join(str(ord(c) - 96) for c in text))
    return n.to_bytes((n.bit_length() + 7) // 8, "big")


def main() -> int:
    results.clear()
    planted_control()

    # --- EVP-MD5 planted control (community retracted recipe) ---
    body, _ = decrypt_mdp5(SAL_SHORT, COMMUNITY_RECIPE)
    ok_comm = body is not None and hashlib.sha256(body).hexdigest() == COMMUNITY_SHA256
    record(
        "EVP-MD5 community recipe decrypt",
        ok_comm,
        f"len={len(body) if body else 0} printable={sum(b in PRINTABLE for b in body) if body else 0}",
    )

    msl = poster_sums()
    msl.update(matrix_strings())
    sal = (ART / "salphaseion.txt").read_text().strip()
    bits = sal[91:195].replace("a", "0").replace("b", "1")
    msl["ab-sum-bits"] = str(sum(int(c) for c in bits))

    lw = word_lastwords_candidates()

    # 1) MD5: literal recipe + round2-style operands + substituted templates
    try_mdp5(COMMUNITY_RECIPE, "md5-community-literal")
    for name, val in msl.items():
        try_mdp5(val, f"md5-msl-{name}")
        try_mdp5(f"matrixsumlist{val}enterlastwordsbeforearchichoicethispasswordmatrixsumlist", f"md5-recipe-msl-{name}")
    for name, val in lw:
        try_mdp5(val, f"md5-{name}")
        try_mdp5(
            f"matrixsumlistenter{val}thispasswordmatrixsumlist",
            f"md5-recipe-lw-{name}",
        )
    for mname, mval in list(msl.items())[:8]:
        for lname, lval in lw[:6]:
            pw = f"{mval}enter{lval}thispassword{mval}"
            try_mdp5(pw, f"md5-chain-{mname}-{lname}")
            pw2 = f"{mval}enter{lval}thispassword{lval}"
            try_mdp5(pw2, f"md5-chain2-{mname}-{lname}")
    try_mdp5(tok23(), "md5-tok23")
    try_mdp5(message_8446_text(), "md5-8446")

    # 2–3) covered above (word lw + spiral/diag in msl dict)

    # 4) Pair deletion on fillers -> §4.1 on three containers
    global decrypts_sha
    n = len(FILLERS)
    for i, j in itertools.combinations(range(n), 2):
        if i > j:
            i, j = j, i
        deleted = FILLERS[:i] + FILLERS[i + 1 : j] + FILLERS[j + 1 :]
        raw = filler_to_bytes(deleted)
        for suffix, ans in (
            ("latin1", raw.decode("latin-1", errors="replace")),
            ("hex", raw.hex()),
            ("sha256hex", hashlib.sha256(raw).hexdigest()),
        ):
            decrypts_sha = try_password(ans, f"filler-pair-{i}-{j}-{suffix}", hits_sha, decrypts_sha)

    report = {
        "md5_decrypts": decrypts_md5,
        "md5_structured_hits": len(hits_md5),
        "md5_community_control": ok_comm,
        "sha256_decrypts_filler_pairs": decrypts_sha,
        "sha256_structured_hits": len(hits_sha),
        "msl_operands": msl,
        "word_lastwords": lw,
        "filler_pair_combos": n * (n - 1) // 2,
        "md5_hits": hits_md5,
        "sha_hits": hits_sha[:10],
    }
    (ART / "round3_battery.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"round3: md5={decrypts_md5} (structured {len(hits_md5)}) "
        f"sha filler-pairs={decrypts_sha} (structured {len(hits_sha)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
