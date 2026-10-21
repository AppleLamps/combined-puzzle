"""CRYPTANALYST — small offline batteries (propose decodes as code, then run).

Win: uncompressed pubkey hash160 == PRIZE_H160 (§1). Container opens: §4.1
(password = lowercase sha256 hex of answer, EVP SHA-256, AES-256-CBC).
"""

from __future__ import annotations

import hashlib
import itertools
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from crypto_known import (  # noqa: E402
    PRIZE_H160,
    decrypt_b64,
    is_win_uncompressed,
)
from step1_btcseed import decrypt_with_password, load_containers  # noqa: E402
from step3_mask import (  # noqa: E402
    MASK6,
    TAIL4,
    apply_zeros,
    digits_of,
    matrix_strings,
    to_bytes,
    tok23,
)

ART = ROOT / "artifacts"
HANDOFF = ROOT / "uploads" / "GSMG-handoff.md"
CONTAINERS = ("terminal", "salphaseion_short", "cosmic")
PRINTABLE = set(range(32, 127))
FLOWER = "theflowerblossomsthroughwhatseemstobeaconcretesurface"
HASH225 = "5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75"

SQUARE = "dbifhcegaklmnopqrstuvwxyz"
BIFID_SHA = "15d62c8228c1a30f3f6280fcdce2251fe616135e9de291b0c7b8a792dd8d0507"

results: list[dict] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    results.append({"check": name, "ok": ok, "detail": detail})
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        raise SystemExit(1)


# --- decode primitives (§6.2 / §6.3 / §7.1) ---------------------------------


def ab_bits(s: str) -> bytes:
    """a=0, b=1, eight bits per byte (handoff §6.2)."""
    return bytes(int(s[i : i + 8].replace("a", "0").replace("b", "1"), 2) for i in range(0, len(s), 8))


def ai_decimal_hex(s: str) -> bytes:
    """a..i -> 1..9, o -> 0; one decimal integer -> hex bytes (§6.2)."""
    n = int("".join("0" if c == "o" else str(ord(c) - 96) for c in s))
    h = format(n, "x")
    if len(h) % 2:
        h = "0" + h
    return bytes.fromhex(h)


def bifid_decrypt(ct: str, square: str, period: int) -> str:
    pos = {c: (i // 5, i % 5) for i, c in enumerate(square)}
    out: list[str] = []
    for i in range(0, len(ct), period):
        block = ct[i : i + period]
        digits: list[int] = []
        for ch in block:
            digits.extend(pos[ch])
        p = len(block)
        rows, cols = digits[:p], digits[p:]
        out.extend(square[r * 5 + c] for r, c in zip(rows, cols))
    return "".join(out)


def beaufort_reciprocal(cipher: str, key: str) -> str:
    """P = K - C mod 26 on a-z (phase 3.2 uses the same rule on symbols)."""
    out: list[str] = []
    ki = 0
    for ch in cipher:
        if not ch.isalpha():
            out.append(ch)
            continue
        c = ord(ch.lower()) - 97
        k = ord(key[ki % len(key)].lower()) - 97
        out.append(chr((k - c) % 26 + 97))
        ki += 1
    return "".join(out)


def message_8446_text() -> str:
    text = HANDOFF.read_text()
    m = re.search(r"\[#8446\] 2023-02-23[^\n]*\n(?:\([^\n]*\)\n)?([01 ]+)", text)
    groups = m.group(1).split()
    bits = "".join(groups)
    return bytes(int(bits[::-1][i : i + 8], 2) for i in range(0, len(bits), 8)).decode()


def dots_candidates() -> list[tuple[str, str]]:
    """#53335–#53341 dot counts plus #53342 ASCII binary (§7.2)."""
    text = HANDOFF.read_text()
    out: list[tuple[str, str]] = []
    for msg_id, pat in (
        ("53335", r"\[#53335\][^\n]*\n(?:\([^\n]*\)\n)?(\.+)\n"),
        ("53336", r"\[#53336\][^\n]*\n(\.+)\n"),
        ("53338", r"\[#53338\][^\n]*\n(\.+)\n"),
        ("53339", r"\[#53339\][^\n]*\n(\.+)\n"),
        ("53341", r"\[#53341\][^\n]*\n(?:\([^\n]*\)\n)?(\.+)\n"),
    ):
        m = re.search(pat, text)
        dots = m.group(1).strip()
        out.append((f"dots-{msg_id}", dots))
    m = re.search(r"\[#53342\][^\n]*\n(?:\([^\n]*\)\n)?([01 ]+)", text)
    groups = m.group(1).split()
    bits = "".join(groups)
    ny = bytes(int(bits[i : i + 8], 2) for i in range(0, len(bits), 8)).decode()
    out.append(("dots-53342-binary", ny))
    out.append(("dots-counts-12345", "12345"))
    out.append(("dots-literal-1to5", ". .. ... .... .....".replace(" ", "")))
    return out


def classify_plaintext(body: bytes | None) -> str:
    from classify_unified import classify_unified

    return classify_unified(body)


def try_password(answer: str, label: str, hits: list[dict], decrypts: int) -> int:
    """§4.1 std-hex only (one KDF) against the three locked containers."""
    pw = hashlib.sha256(answer.encode()).hexdigest().encode()
    containers = load_containers()
    for cname in CONTAINERS:
        raw = containers[cname]
        body, full = decrypt_with_password(raw, pw)
        decrypts += 1
        kind = classify_plaintext(body)
        if kind == "structured":
            hits.append(
                {
                    "label": label,
                    "answer_sha256": hashlib.sha256(answer.encode()).hexdigest(),
                    "container": cname,
                    "result": kind,
                    "head": body[:64].hex() if body else "",
                }
            )
    return decrypts


def try_scalar(buf: bytes, label: str, key_hits: list[dict]) -> None:
    if len(buf) == 32 and is_win_uncompressed(buf):
        key_hits.append({"label": label, "priv": buf.hex(), "via": "raw32"})
    h = hashlib.sha256(buf).digest()
    if is_win_uncompressed(h):
        key_hits.append({"label": label, "priv": h.hex(), "via": "sha256(buf)"})


def controls_faed_integer(faed: str) -> None:
    digs = digits_of(faed, 7)
    whole = to_bytes(digs)
    record("faed whole decimal integer is 237 bytes", len(whole) == 237, f"len={len(whole)}")
    record(
        "faed integer head/tail pins",
        whole[:4].hex() == "1bd5951d" and whole[-4:].hex() == "c7bbc075",
        f"head={whole[:4].hex()} tail={whole[-4:].hex()}",
    )
    printable = sum(b in PRINTABLE for b in whole)
    record(
        "faed integer interior is not ASCII prose",
        printable < 120,
        f"printable {printable}/237",
    )

    masked = apply_zeros(digs, MASK6)
    raw = to_bytes(masked)
    record("mask6 zero (not delete) is 236 bytes", len(raw) == 236)
    record("mask6 pins ends yM / szqu", raw[:2] == b"yM" and raw[-4:] == b"szqu")
    interior = raw[2:-4]
    ip = sum(b in PRINTABLE for b in interior)
    record(
        "mask6 interior mostly non-ASCII",
        ip < len(interior) * 0.4,
        f"interior printable {ip}/{len(interior)}",
    )

    deleted = "".join(c for i, c in enumerate(faed, 1) if i not in MASK6)
    del_digs = digits_of(deleted, 7)
    del_raw = to_bytes(del_digs)
    record("deletion at mask6 positions is 234 bytes", len(del_raw) == 234)
    record(
        "deletion loses yM/szqu pins",
        del_raw[:2] != b"yM" or del_raw[-4:] != b"szqu",
        f"head={del_raw[:2]!r} tail={del_raw[-4:]!r}",
    )


def controls_bifid(faed: str) -> str:
    bout = bifid_decrypt(faed, SQUARE, 570)
    record("Bifid period 570 starts btcseedd", bout.startswith("btcseedd") and len(bout) == 570)
    record("Bifid plaintext sha256", hashlib.sha256(bout.encode()).hexdigest() == BIFID_SHA)
    good_outs = []
    for perm in itertools.permutations("dbifhcega"):
        sq = "".join(perm) + "klmnopqrstuvwxyz"
        o = bifid_decrypt(faed, sq, 570)
        if o.startswith("btcseed"):
            good_outs.append(o)
    record("exactly 8 squares yield btcseed prefix", len(good_outs) == 8)
    diverge = next(i for i in range(len(good_outs[0])) if len({o[i] for o in good_outs}) > 1)
    record("8 squares agree for 8 chars then diverge", diverge == 8, f"first diff index {diverge}")
    return bout


def battery_beaufort_bifid(pt: str, hits: list[dict], key_hits: list[dict]) -> int:
    """Beaufort reciprocal on full Bifid plaintext, key `btcseed`."""
    plain = beaufort_reciprocal(pt, "btcseed")
    record("Beaufort(btcseed) length preserved", len(plain) == len(pt))
    decrypts = 0
    for label, answer in (
        ("beaufort-bifid-plain", plain),
        ("beaufort-bifid-sha256hex", hashlib.sha256(plain.encode()).hexdigest()),
        ("bifid-plain", pt),
        ("bifid-tail-after-btcseed", pt[7:]),
        ("sha256hex(bifid-plain)", hashlib.sha256(pt.encode()).hexdigest()),
    ):
        decrypts = try_password(answer, label, hits, decrypts)
    try_scalar(hashlib.sha256(plain.encode()).digest(), "sha256(beaufort-bifid)", key_hits)
    return decrypts


def battery_fillers(hits: list[dict], key_hits: list[dict]) -> int:
    fillers = (ART / "yellowblue_fillers.txt").read_text().strip()
    raw = ai_decimal_hex(fillers)
    record("fillers decimal→hex is 25 bytes", len(raw) == 25, raw.hex())
    decrypts = 0
    for label, answer in (
        ("fillers-decimal-hex", raw.hex()),
        ("fillers-letters", fillers),
        ("sha256hex(fillers-decimal-hex)", hashlib.sha256(raw.hex().encode()).hexdigest()),
        ("sha256hex(fillers-letters)", hashlib.sha256(fillers.encode()).hexdigest()),
    ):
        decrypts = try_password(answer, label, hits, decrypts)
    try_scalar(raw, "fillers-decimal-bytes", key_hits)
    try_scalar(hashlib.sha256(raw).digest(), "sha256(fillers-decimal)", key_hits)
    return decrypts


def battery_8446(hits: list[dict]) -> int:
    msg = message_8446_text()
    record("#8446 decode length 161", len(msg) == 161)
    decrypts = 0
    for label, answer in (
        ("8446-full", msg),
        ("8446-sha256hex", hashlib.sha256(msg.encode()).hexdigest()),
        ("8446-yellowblueprimes", "yellowblueprimes"),
        ("8446-recipe-words", "matrixsumlistlastwordsbeforearchichoicethispassword"),
    ):
        decrypts = try_password(answer, label, hits, decrypts)
    return decrypts


def battery_dots(hits: list[dict]) -> int:
    decrypts = 0
    for label, answer in dots_candidates():
        decrypts = try_password(answer, label, hits, decrypts)
        if len(answer) > 40:
            decrypts = try_password(
                hashlib.sha256(answer.encode()).hexdigest(),
                f"{label}-sha256hex",
                hits,
                decrypts,
            )
    return decrypts


def battery_recipe(hits: list[dict]) -> int:
    """Named recipe operands × three containers (small cross, not full step3 grid)."""
    sal = (ART / "salphaseion.txt").read_text().strip()
    msl = matrix_strings()
    lw = "lastwordsbeforearchichoice"
    tp = "thispassword"
    enter = "enter"
    mlist = ab_bits(sal[91:195]).decode()
    h8446 = message_8446_text()
    flower_h = hashlib.sha256(FLOWER.encode()).hexdigest()
    record("recipe control sha256(flower)==#225", flower_h == HASH225)

    operands = {
        "matrixsumlist": mlist,
        "enter": enter,
        "lastwords": lw,
        "thispassword": tp,
        "tok23": tok23(),
        "msl-row": msl["row"],
        "msl-col": msl["col"],
        "8446": h8446,
        "sha256hex-flower": flower_h,
    }
    decrypts = 0
    # single operands
    for name, val in operands.items():
        decrypts = try_password(val, f"recipe-op:{name}", hits, decrypts)
    # chained recipe (reading order from §7.1 + page layout)
    chains = [
        f"{mlist}{enter}{lw}{tp}",
        f"{operands['tok23']}{msl['row']}{flower_h}",
        f"{operands['tok23']}{msl['col']}{tp}",
        f"{h8446}{mlist}{enter}",
        "matrixsumlistenterlastwordsbeforearchichoicethispasswordmatrixsumlist",
    ]
    for i, s in enumerate(chains):
        decrypts = try_password(s, f"recipe-chain:{i}", hits, decrypts)
    return decrypts


def planted_control() -> None:
    hand = HANDOFF.read_text()
    htmls = re.findall(r"```html\n(.*?)```", hand, flags=re.S)
    area = re.search(r"<textarea[^>]*>(.*?)</textarea>", htmls[1], flags=re.S).group(1)
    pt, _, _ = decrypt_b64(area, "causality")
    saved = (ART / "phase2.txt").read_bytes()
    record(
        "planted control: §4.1 decrypt phase2 with causality",
        pt is not None and pt == saved,
        f"len={len(pt) if pt else 0}",
    )


def main() -> None:
    faed = (ART / "faed.txt").read_text().strip()
    record("faed block length", len(faed) == 570)

    planted_control()
    controls_faed_integer(faed)
    pt = controls_bifid(faed)

    hits: list[dict] = []
    key_hits: list[dict] = []
    decrypts = 0
    decrypts += battery_beaufort_bifid(pt, hits, key_hits)
    decrypts += battery_fillers(hits, key_hits)
    decrypts += battery_8446(hits)
    decrypts += battery_dots(hits)
    decrypts += battery_recipe(hits)

    wins = [k for k in key_hits if k.get("via")]
    summary = {
        "prize_h160": PRIZE_H160,
        "checks": len(results),
        "checks_pass": sum(1 for r in results if r["ok"]),
        "decrypts": decrypts,
        "containers": list(CONTAINERS),
        "convention": "4.1 std-hex sha256(answer) EVP-SHA256 AES-256-CBC",
        "structured_hits": hits,
        "key_hits": key_hits,
        "win": any(is_win_uncompressed(bytes.fromhex(k["priv"])) for k in key_hits if "priv" in k),
    }
    out_path = ART / "cryptanalyst_summary.json"
    out_path.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"\n=== cryptanalyst: {summary['checks_pass']}/{summary['checks']} checks, "
          f"{decrypts} decrypts, structured hits {len(hits)}, key hits {len(key_hits)} ===")
    if hits or key_hits:
        print("HIT", json.dumps(hits or key_hits, indent=2))
    else:
        print("NO HIT (expected for this small battery)")


if __name__ == "__main__":
    main()
