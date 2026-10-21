#!/usr/bin/env python3
"""Round 14: missed connections / clue battery (~2k decrypts).

Spec: team/preregister_round14_clues.json
"""

from __future__ import annotations

import base64
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "team"))

ART = ROOT / "artifacts"
SPEC = json.loads((ROOT / "team" / "preregister_round14_clues.json").read_text())
BUDGET = int(SPEC["budget_target"])

from crypto_known import is_win_uncompressed  # noqa: E402
from step1_btcseed import load_containers, win_key  # noqa: E402
from cryptanalyst_tests import (  # noqa: E402
    HASH225,
    FLOWER,
    SQUARE,
    bifid_decrypt,
    message_8446_text,
    planted_control,
    record,
    results,
)
from classify_unified import classify_unified  # noqa: E402
from round4_battery import decrypt_mdp5_bytes, spiral_msl_operations  # noqa: E402
from round5_preregistered import decrypt_with_profile  # noqa: E402
from round7_chained_pipeline import ARCH, CHECKER, DIGITS149, lw_catalog  # noqa: E402
from round8_reader_gap import FAED, SAL_PAGE  # noqa: E402
from round12_pipeline import reduce_chain  # noqa: E402
from round13_pipeline import decode_halves, sal_literals, xor_bytes  # noqa: E402

HOST23 = "11110111001111011001100"
SHABEF_OUR = "sha256ourfirsthintisyourlastcommand"
ARCH1539 = (ART / "architect_letters_1539.txt").read_text().strip()

summary: dict = {
    "budget": BUDGET,
    "decrypts": 0,
    "by_gap": {},
    "hits": [],
    "wins": [],
    "stopped_early": False,
    "checks": {},
}


def over_budget() -> bool:
    return summary["decrypts"] >= BUDGET


def bump(gap: str, n: int = 1) -> None:
    summary["decrypts"] += n
    summary["by_gap"][gap] = summary["by_gap"].get(gap, 0) + n
    if summary["decrypts"] >= BUDGET:
        summary["stopped_early"] = True


def emit(gap: str, raw: bytes, answer: str, profile: str, tag: str, cname: str) -> bytes | None:
    if over_budget() or not answer:
        return None
    bump(gap)
    if is_win_uncompressed(hashlib.sha256(answer.encode()).digest()):
        summary["wins"].append({"tag": tag, "via": "sha256(answer)"})
    body, _ = decrypt_with_profile(raw, answer, profile)
    if body and classify_unified(body) == "structured":
        summary["hits"].append({"gap": gap, "tag": tag, "container": cname, "profile": profile})
    if body:
        win_key(body, tag, summary["wins"])
    return body


def emit_all(gap: str, answer: str, tag: str, containers: list[str], profiles: list[str]) -> None:
    blobs = load_containers()
    for cname in containers:
        for prof in profiles:
            if cname == "salphaseion_short" and prof == "raw32-sha256":
                continue
            emit(gap, blobs[cname], answer, prof, f"{tag}-{cname}-{prof}", cname)
            if cname == "salphaseion_short" and prof == "plain-md5":
                bump(gap)
                body, _ = decrypt_mdp5_bytes(blobs[cname], answer.encode())
                if body and classify_unified(body) == "structured":
                    summary["hits"].append({"gap": gap, "tag": f"{tag}-md5", "container": cname})


def z_lit_sha() -> str:
    rows = reduce_chain(
        ["msl_ab_sum", "faed_bifid_sha256hex", "lastwords_literal", "thispassword_literal", "shabef_four_literal"],
        "concat_literals_final_sha256hex",
    )
    return rows[0][1] if rows else ""


def inline_page_passwords() -> dict[str, str]:
    return {
        "inline_page_sha": hashlib.sha256(SAL_PAGE.encode()).hexdigest(),
        "phase1_hash225": HASH225,
        "flower": FLOWER,
        "sha256our_hint": SHABEF_OUR,
        "z_lit_sha": z_lit_sha(),
        "pre_ct_sha256hex": hashlib.sha256(SAL_PAGE[:895].encode()).hexdigest(),
        "post_ct_sha256hex": hashlib.sha256(SAL_PAGE[895:].encode()).hexdigest(),
        "shabef_concat": "shabefourfirsthintisyourlastcommand" + "shabefanstoo",
        "page_sha256hex": hashlib.sha256(SAL_PAGE.encode()).hexdigest(),
    }


def extract_inline_sal_raw() -> bytes:
    """Handoff spans [895,959)+[999,1063) — same as sal short (not the longer regex tail)."""
    b64 = SAL_PAGE[895:959] + SAL_PAGE[999:1063]
    return base64.b64decode("".join(b64.split()))


def split_xor_blobs() -> dict[str, bytes]:
    raw1, raw2 = decode_halves()
    sal = (ART / "salphaseion_short.bin").read_bytes()
    out = {"canonical": sal}
    if len(raw1) >= 16 and len(raw2) >= 16:
        out["xor_from_offset_16"] = raw1[:16] + xor_bytes(raw1[16:], raw2)
        out["xor_ct_tail_only"] = raw1[:16] + xor_bytes(raw1[16:], raw2[16:] if len(raw2) > 16 else raw2)
    inter = bytearray()
    for i in range(max(len(raw1), len(raw2))):
        if i < len(raw1):
            inter.append(raw1[i])
        if i < len(raw2):
            inter.append(raw2[i])
    out["interleave_halves_bytes"] = bytes(inter)
    return out


def run_g1() -> None:
    gap = "G1_split_header_xor"
    anchors = inline_page_passwords()
    blobs = split_xor_blobs()
    for mode in SPEC["gaps"]["G1_split_header_xor"]["modes"]:
        blob = blobs.get(mode)
        if not blob:
            continue
        for key in SPEC["gaps"]["G1_split_header_xor"]["password_anchors"]:
            ans = anchors.get(key, "")
            if not ans:
                continue
            emit(gap, blob, ans, "std-hex-sha256", f"g1-{mode}-{key}", "salphaseion_short")
            bump(gap)
            body, _ = decrypt_mdp5_bytes(blob, ans.encode())
            if body and classify_unified(body) == "structured":
                summary["hits"].append({"gap": gap, "tag": f"g1-md5-{mode}", "container": "xor_blob"})


def run_g2() -> None:
    gap = "G2_first_hint_last_command"
    g = SPEC["gaps"]["G2_first_hint_last_command"]
    for a, b in g["pairs"]:
        for form in ("concat", "sha_concat", "sha_both"):
            if form == "concat":
                ans = a + b
            elif form == "sha_concat":
                ans = hashlib.sha256((a + b).encode()).hexdigest()
            else:
                ans = hashlib.sha256(a.encode()).hexdigest() + hashlib.sha256(b.encode()).hexdigest()
            emit_all(gap, ans, f"g2-{form}-{a[:8]}", g["containers"], ["std-hex-sha256", "raw32-sha256"])


def door_extract(source: str, indices: list[int]) -> str:
    if source == "digits149":
        s = DIGITS149
        return "".join(s[i - 1] for i in indices if 0 < i <= len(s))
    if source == "checker_decode":
        return "".join(CHECKER[i - 1] for i in indices if 0 < i <= len(CHECKER))
    if source == "architect_1539":
        return "".join(ARCH1539[i - 1] for i in indices if 0 < i <= len(ARCH1539))
    if source == "host_bits23":
        return "".join(HOST23[i - 1] for i in indices if 0 < i <= len(HOST23))
    return ""


def run_g3() -> None:
    gap = "G3_door_checker_architect"
    g = SPEC["gaps"]["G3_door_checker_architect"]
    idx = g["door_indices"]
    containers = g["containers"]
    for src in g["sources"]:
        sl = door_extract(src, idx)
        if not sl:
            continue
        emit_all(gap, sl, f"g3-{src}-door", containers, ["std-hex-sha256"])
        emit_all(gap, hashlib.sha256(sl.encode()).hexdigest(), f"g3-{src}-door-sha", containers, ["std-hex-sha256", "raw32-sha256"])
    for num in g["architect_numerals"]:
        for lw in (CHECKER[:45].lower(), ARCH[ARCH.find("SELECT") - 40 : ARCH.find("SELECT")].lower()):
            ans = f"{num}{lw}thispassword{num}"
            emit_all(gap, ans, f"g3-arch-{num}", containers, ["std-hex-sha256"])
            emit_all(gap, hashlib.sha256(ans.encode()).hexdigest(), f"g3-arch-{num}-sha", containers, ["std-hex-sha256"])
    # checker blanks 1 and 4 echo: use digits at positions 1,4 only
    emit_all(gap, door_extract("digits149", [1, 4]), "g3-blanks-14", containers, ["std-hex-sha256"])


def bifid_plain() -> str:
    return bifid_decrypt(FAED, SQUARE, 570)


def run_g4() -> None:
    gap = "G4_bifid_streams"
    g = SPEC["gaps"]["G4_bifid_streams"]
    plain = bifid_plain()
    streams: dict[str, str] = {
        "even_positions": plain[1::2],
        "odd_positions": plain[0::2],
        "after_btcseed": plain[7:] if plain.startswith("btcseed") else plain[8:],
        "last_32_faed": FAED[-32:],
    }
    for name in g["streams"]:
        s = streams.get(name, "")
        if not s:
            continue
        emit_all(gap, s, f"g4-{name}-lit", g["containers"], ["std-hex-sha256"])
        emit_all(gap, hashlib.sha256(s.encode()).hexdigest(), f"g4-{name}-sha", g["containers"], ["std-hex-sha256", "raw32-sha256"])
    # quaternary pack even letters b,c,d,e -> 0..3
    m = {"b": 0, "c": 1, "d": 2, "e": 3}
    even = plain[1::2]
    if all(c in m for c in even[:64]):
        packed = bytes(m[c] for c in even[:64])
        emit_all(gap, packed.hex(), "g4-even-nibble-hex", g["containers"], ["std-hex-sha256"])


def run_g5() -> None:
    gap = "G5_keys_and_cp273"
    g = SPEC["gaps"]["G5_keys_and_cp273"]
    for pw in g["passwords"]:
        emit_all(gap, pw, f"g5-{pw[:12]}", g["containers"], ["std-hex-sha256", "raw32-sha256"])
    if g.get("architect_sha256hex"):
        emit_all(gap, hashlib.sha256(ARCH1539.encode()).hexdigest(), "g5-arch1539-sha", g["containers"], ["std-hex-sha256"])
        emit_all(gap, hashlib.sha256(ARCH.encode()).hexdigest(), "g5-beaufort-sha", g["containers"], ["std-hex-sha256"])


def run_g6() -> None:
    gap = "G6_inline_sal_ciphertext"
    raw = extract_inline_sal_raw()
    sal_ref = (ART / "salphaseion_short.bin").read_bytes()
    summary["checks"]["inline_equals_sal_short"] = raw == sal_ref
    record("inline span b64 equals sal short", raw == sal_ref, f"len={len(raw)}")
    pw = inline_page_passwords()
    for key in SPEC["gaps"]["G6_inline_sal_ciphertext"]["passwords"]:
        ans = pw.get(key, "")
        if not ans:
            continue
        emit(gap, raw, ans, "std-hex-sha256", f"g6-{key}-std", "salphaseion_short")
        bump(gap)
        body, _ = decrypt_mdp5_bytes(raw, ans.encode())
        if body and classify_unified(body) == "structured":
            summary["hits"].append({"gap": gap, "tag": f"g6-md5-{key}", "container": "inline"})
        for cname in ("terminal", "cosmic"):
            emit(gap, load_containers()[cname], ans, "std-hex-sha256", f"g6-{key}-{cname}", cname)


def run_g7() -> None:
    gap = "G7_spiral_msl_recipes"
    g = SPEC["gaps"]["G7_spiral_msl_recipes"]
    lw_map = lw_catalog()
    lws = [lw_map[k] for k in g["lw_keys"] if k in lw_map]
    if g.get("ops_from_round4"):
        for op_name, op_val in spiral_msl_operations():
            for lw in lws:
                for recipe in (
                    f"{op_val}enter{lw}thispassword{op_val}",
                    f"matrixsumlist{op_val}enter{lw}",
                    hashlib.sha256((op_val + lw).encode()).hexdigest(),
                ):
                    emit_all(gap, recipe, f"g7-{op_name}", g["containers"], ["std-hex-sha256", "plain-md5"])


def run_g8() -> None:
    gap = "G8_yinyang_xor_keys"
    g = SPEC["gaps"]["G8_yinyang_xor_keys"]
    containers = load_containers()
    keys = {
        "checker_decode": CHECKER,
        "digits149_sum": str(sum(int(c) for c in DIGITS149)),
        "8446_full": message_8446_text(),
    }
    for blob_name in g["xor_blobs"]:
        raw = containers.get(blob_name)
        if not raw:
            continue
        for kname, kval in keys.items():
            for form in ("literal", "sha256hex"):
                ans = kval if form == "literal" else hashlib.sha256(kval.encode()).hexdigest()
                emit(gap, raw, ans, "std-hex-sha256", f"g8-{blob_name}-{kname}-{form}", blob_name)
                emit(gap, raw, ans, "raw32-sha256", f"g8-{blob_name}-{kname}-r32", blob_name)


def main() -> int:
    results.clear()
    planted_control()
    run_g1()
    run_g2()
    run_g3()
    run_g4()
    run_g5()
    run_g6()
    run_g7()
    run_g8()
    (ART / "round14_clues.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(
        f"round14: decrypts={summary['decrypts']}/{BUDGET} "
        f"hits={len(summary['hits'])} wins={len(summary['wins'])} stopped={summary['stopped_early']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
