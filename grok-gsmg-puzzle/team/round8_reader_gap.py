#!/usr/bin/env python3
"""Round 8: Reader gap pilot G1–G7 (~2k decrypts).

Spec: team/preregister_reader_gap.json
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "team"))

ART = ROOT / "artifacts"
SPEC = json.loads((ROOT / "team" / "preregister_reader_gap.json").read_text())
BUDGET = int(SPEC["budget_target"])

from crypto_known import decrypt_salted, evp_bytes_to_key, is_win_uncompressed, pkcs7_unpad  # noqa: E402
from Crypto.Cipher import AES  # noqa: E402
from step1_btcseed import load_containers, win_key  # noqa: E402
from classify_unified import classify_unified  # noqa: E402
from step3_mask import MASK6, apply_zeros, digits_of, to_bytes  # noqa: E402
from cryptanalyst_tests import (  # noqa: E402
    SQUARE,
    bifid_decrypt,
    beaufort_reciprocal,
    planted_control,
    record,
    results,
)
from round4_battery import decrypt_mdp5_bytes  # noqa: E402
from round5_preregistered import decrypt_with_profile  # noqa: E402

SAL_PAGE = (ART / "salphaseion.txt").read_text().strip()
FILLER60 = (ART / "yellowblue_fillers.txt").read_text().strip()
FAED = (ART / "faed.txt").read_text().strip()
FLOWER_HASH = "5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75"
HOST23 = "BBBBYBBBYYBBBBYBBYYBFYY"[:23]
HOST25 = (ART / "yellowblue_colours.txt").read_text().strip()

summary: dict = {
    "budget": BUDGET,
    "decrypts": 0,
    "by_gap": {},
    "hits": [],
    "wins": [],
    "stopped_early": False,
}


def over_budget() -> bool:
    return summary["decrypts"] >= BUDGET


def bump(gap: str, n: int = 1) -> bool:
    summary["decrypts"] += n
    summary["by_gap"][gap] = summary["by_gap"].get(gap, 0) + n
    if summary["decrypts"] >= BUDGET:
        summary["stopped_early"] = True
        return False
    return True


def check_answer_scalar(answer: str, tag: str) -> None:
    d = hashlib.sha256(answer.encode()).digest()
    if is_win_uncompressed(d):
        summary["wins"].append({"tag": tag, "via": "sha256(answer)"})


def try_decrypt(
    gap: str,
    raw: bytes,
    answer: str,
    profile: str,
    tag: str,
    cname: str,
) -> bytes | None:
    if over_budget() or not answer or len(answer) > 20000:
        return None
    bump(gap)
    check_answer_scalar(answer, tag)
    body, kind = decrypt_with_profile(raw, answer, profile)
    if body and classify_unified(body) == "structured":
        summary["hits"].append(
            {"gap": gap, "tag": tag, "container": cname, "profile": profile, "kind": "structured"}
        )
    if body and win_key(body, tag, summary["wins"]):
        pass
    if body and len(body) == 32 and is_win_uncompressed(body):
        summary["wins"].append({"tag": tag, "via": "plaintext32", "container": cname})
    return body


def try_md5(gap: str, raw: bytes, answer: str, tag: str, cname: str) -> None:
    if over_budget():
        return
    bump(gap)
    check_answer_scalar(answer, tag)
    body, _ = decrypt_mdp5_bytes(raw, answer.encode())
    if body and classify(body).startswith("structured"):
        summary["hits"].append({"gap": gap, "tag": tag, "container": cname, "profile": "plain-md5"})
    if body:
        win_key(body, tag, summary["wins"])


def try_raw_evp(gap: str, raw: bytes, pw: bytes, tag: str, cname: str) -> None:
    if over_budget() or raw[:8] != b"Salted__":
        return
    bump(gap)
    salt, ct = raw[8:16], raw[16:]
    key, iv = evp_bytes_to_key(pw, salt, md=hashlib.sha256)
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    body = pkcs7_unpad(pt)
    if body and classify(body).startswith("structured"):
        summary["hits"].append({"gap": gap, "tag": tag, "container": cname, "profile": "raw32-evp"})
    if body:
        win_key(body, tag, summary["wins"])


def emit_std_md5_raw(
    gap: str,
    answer: str,
    tag: str,
    containers: list[str],
    kdf_flags: list[str],
) -> None:
    blobs = load_containers()
    for cname in containers:
        if "std-hex-sha256" in kdf_flags:
            try_decrypt(gap, blobs[cname], answer, "std-hex-sha256", f"{tag}-{cname}-std", cname)
        if "raw32-sha256_on_cosmic" in kdf_flags and cname == "cosmic":
            try_decrypt(gap, blobs[cname], answer, "raw32-sha256", f"{tag}-{cname}-r32", cname)
        if "plain-md5_on_sal_short" in kdf_flags and cname == "salphaseion_short":
            try_md5(gap, blobs[cname], answer, f"{tag}-{cname}-md5", cname)


# --- G1 -----------------------------------------------------------------------

def gap_g1() -> None:
    g = "G1"
    spec = SPEC["gaps"]["G1_cosmic_duality_title"]
    for s in spec["strings"]:
        emit_std_md5_raw(g, s, f"g1-{s[:24]}", spec["containers"], spec["kdf"])
        if spec.get("also_sha256hex_of_operand"):
            emit_std_md5_raw(
                g,
                hashlib.sha256(s.encode()).hexdigest(),
                f"g1-sha-{s[:16]}",
                spec["containers"],
                ["std-hex-sha256", "raw32-sha256_on_cosmic"],
            )


# --- G2 -----------------------------------------------------------------------

def bits_from_source(name: str) -> str:
    blobs = load_containers()
    spiral = (ART / "poster_spiral_bits.txt").read_text().strip()
    if name == "spiral_url192":
        return spiral[:192]
    if name == "spiral_full196":
        return spiral
    if name == "terminal_ciphertext":
        return "".join(format(b, "08b") for b in blobs["terminal"][16:])
    if name == "salphaseion_short_ciphertext":
        return "".join(format(b, "08b") for b in blobs["salphaseion_short"][16:])
    if name == "xor_terminal_sal_ciphertext":
        t, s = blobs["terminal"][16:], blobs["salphaseion_short"][16:]
        x = bytes(a ^ b for a, b in zip(t, s))
        return "".join(format(b, "08b") for b in x)
    if name == "cosmic_ciphertext":
        return "".join(format(b, "08b") for b in blobs["cosmic"][16:])
    raise KeyError(name)


def pack_bits(bits: str, width: int, offset: int, packing: str) -> bytes:
    seg = bits[offset : offset + width]
    if len(seg) < width:
        return b""
    if packing == "msb":
        # left-pad to multiple of 8
        pad = (8 - len(seg) % 8) % 8
        seg = seg + "0" * pad
        return bytes(int(seg[i : i + 8], 2) for i in range(0, len(seg), 8))
    # lsb: take from the right of the window
    pad = (8 - len(seg) % 8) % 8
    seg = "0" * pad + seg
    return bytes(int(seg[i : i + 8], 2) for i in range(0, len(seg), 8))


def gap_g2() -> None:
    g = "G2"
    spec = SPEC["gaps"]["G2_6913_bit_width"]
    blobs = load_containers()
    for src in spec["sources"]:
        bits = bits_from_source(src)
        for width in spec["widths"]:
            offsets = spec["offsets_21"] if width == 21 else spec["offsets_1812"]
            if len(bits) < width:
                continue
            for off in offsets:
                if off + width > len(bits):
                    continue
                for packing in spec["packings"]:
                    rawb = pack_bits(bits, width, off, packing)
                    if not rawb:
                        continue
                    for form in spec["answer_forms"]:
                        if form == "sha256hex_bytes":
                            ans = hashlib.sha256(rawb).hexdigest()
                        else:
                            ans = rawb.hex()
                        tag = f"g2-{src}-w{width}-o{off}-{packing}-{form[:4]}"
                        for cname in spec["containers"]:
                            try_decrypt(
                                g, blobs[cname], ans, "std-hex-sha256", f"{tag}-{cname}", cname
                            )
                            if over_budget():
                                return


# --- G3 -----------------------------------------------------------------------

def sal_operands() -> dict[str, str]:
    compact = SAL_PAGE
    no_space = compact.replace(" ", "")
    bits = compact[91:195].replace("a", "0").replace("b", "1")

    def ai_decode(start: int, end: int) -> str:
        seg = compact[start:end]
        n = int("".join("0" if c == "o" else str(ord(c) - 96) for c in seg))
        return format(n, "x")

    span_concat = bits + ai_decode(766, 829) + ai_decode(830, 859)
    dbbi = compact.split("a")[0] if "a" in compact else compact[:200]
    labels = "matrixsumlistenterlastwordsbeforearchichoicethispasswordmatrixsumlist"
    return {
        "sha256hex_full_compact": hashlib.sha256(compact.encode()).hexdigest(),
        "sha256hex_all_span_decodes_concat": hashlib.sha256(span_concat.encode()).hexdigest(),
        "full_compact_literal": compact,
        "sha256hex_full_no_spaces": hashlib.sha256(no_space.encode()).hexdigest(),
        "sha256hex_dbbi_faed_concat": hashlib.sha256((dbbi + FAED).encode()).hexdigest(),
        "sha256hex_labels_concat": hashlib.sha256(labels.encode()).hexdigest(),
    }


def gap_g3() -> None:
    g = "G3"
    spec = SPEC["gaps"]["G3_sal_full_page"]
    for key, ans in sal_operands().items():
        if key not in spec["operands"]:
            continue
        emit_std_md5_raw(g, ans, f"g3-{key}", spec["containers"], spec["kdf"])
        emit_std_md5_raw(
            g,
            ans,
            f"g3-{key}-r32",
            ["cosmic"],
            ["raw32-sha256_on_cosmic"],
        )


# --- G4 -----------------------------------------------------------------------

def gap_g4() -> None:
    g = "G4"
    spec = SPEC["gaps"]["G4_shabefour_vs_sha256our"]
    for s in spec["strings"]:
        emit_std_md5_raw(g, s, f"g4-{s[:20]}", spec["containers"], spec["kdf"])
        emit_std_md5_raw(
            g,
            hashlib.sha256(s.encode()).hexdigest(),
            f"g4-sha-{s[:12]}",
            spec["containers"],
            ["std-hex-sha256"],
        )


# --- G5 -----------------------------------------------------------------------

def host_bits(s: str) -> bytes:
    b = "".join("1" if c == "B" else "0" for c in s if c in "BY")
    pad = (8 - len(b) % 8) % 8
    b += "0" * pad
    return bytes(int(b[i : i + 8], 2) for i in range(0, len(b), 8))


def gap_g5() -> None:
    g = "G5"
    spec = SPEC["gaps"]["G5_derived_binary_sha"]
    blobs = load_containers()
    mask6 = to_bytes(apply_zeros(digits_of(FAED, 7), MASK6))
    h23 = host_bits(HOST23)
    h25 = host_bits(HOST25)
    xor_blob = blobs.get("xor_ct_salt_terminal")
    xor16 = xor_blob[:16] if xor_blob else b""
    dbbi91 = SAL_PAGE[:91]
    pipes = {
        "host23_bits_only": h23,
        "host23_plus_mask6_zero": h23 + mask6,
        "mask6_zero_only": mask6,
        "host25_colours_bits": h25,
        "xor_ct_salt_16": xor16,
        "dbbi_prefix91_latin1": dbbi91.encode("latin-1", errors="replace"),
    }
    for pname, data in pipes.items():
        if pname not in spec["pipelines"]:
            continue
        ans = hashlib.sha256(data).hexdigest()
        for cname in spec["containers"]:
            try_decrypt(g, blobs[cname], ans, "std-hex-sha256", f"g5-{pname}-{cname}", cname)


# --- G6 H2 --------------------------------------------------------------------

def filler_first_appearance_square() -> str:
    seen: list[str] = []
    for ch in FILLER60:
        if ch not in seen:
            seen.append(ch)
    # pad to 25 for 5x5 bifid (drop last duplicate if 26)
    alpha = "abcdefghijklmnopqrstuvwxyz"
    for ch in alpha:
        if ch not in seen and len(seen) < 25:
            seen.append(ch)
    return "".join(seen[:25])


def _gap_g6_square(g: str, spec: dict, square: str, label: str) -> None:
    pt = bifid_decrypt(FAED, square, spec["period"])
    blobs = load_containers()
    for key_label in spec["beaufort_keys"]:
        key = "btcseed" if key_label == "btcseed" else FLOWER_HASH
        beau = beaufort_reciprocal(pt, key)
        forms: dict[str, str | bytes] = {
            "beaufort_full": beau,
            "beaufort_after_btcseed": beau[8:] if beau.startswith("btcseed") else beau,
        }
        # mod 2^256 tail from whole-block decimal of beaufort output letters as bytes
        vals = [ord(c) for c in beau if c.isalpha()]
        n = 0
        for v in vals:
            n = (n * 26 + (v - 97)) % (2**256)
        forms["beaufort_tail_mod256_raw_evp"] = n.to_bytes(32, "big")
        for form_name, material in forms.items():
            if form_name not in spec["output_forms"]:
                continue
            for cname in spec["containers"]:
                if form_name == "beaufort_tail_mod256_raw_evp":
                    try_raw_evp(
                        g,
                        blobs[cname],
                        material if isinstance(material, bytes) else bytes(material),
                        f"g6-{form_name}-{key_label}-{cname}",
                        cname,
                    )
                else:
                    ans = material if isinstance(material, str) else material.decode()
                    try_decrypt(
                        g,
                        blobs[cname],
                        ans,
                        "std-hex-sha256",
                        f"g6-{label}-{form_name}-{key_label}-{cname}",
                        cname,
                    )


def gap_g6() -> None:
    spec = SPEC["gaps"]["G6_h2_filler_bifid_beaufort"]
    _gap_g6_square("G6", spec, filler_first_appearance_square(), "filler-sq")
    if spec.get("also_canonical_square_control"):
        _gap_g6_square("G6", spec, SQUARE, "canon-sq")


# --- G7 H3 --------------------------------------------------------------------

def delete_at(s: str, indices_1based: list[int]) -> str:
    kill = set(indices_1based)
    return "".join(ch for i, ch in enumerate(s, 1) if i not in kill)


def gap_g7() -> None:
    g = "G7"
    spec = SPEC["gaps"]["G7_h3_door_index_deletion"]
    idx = spec["delete_1based"]
    blobs = load_containers()
    filler_surv = delete_at(FILLER60, idx)
    faed_surv = delete_at(FAED, idx)
    digs = digits_of(faed_surv, 7)
    whole = to_bytes(digs)
    tail32 = whole[-32:] if len(whole) >= 32 else whole.rjust(32, b"\x00")
    encodings = {
        "survivor_string_sha256hex": hashlib.sha256(filler_surv.encode()).hexdigest(),
        "faed_survivor_string_sha256hex": hashlib.sha256(faed_surv.encode()).hexdigest(),
        "faed_survivor_int_tail32_sha256hex": hashlib.sha256(tail32).hexdigest(),
        "filler_survivor_literal": filler_surv,
    }
    for enc_name, ans in encodings.items():
        if enc_name not in spec["encode"]:
            continue
        for cname in spec["containers"]:
            try_decrypt(g, blobs[cname], ans, "std-hex-sha256", f"g7-{enc_name}-{cname}", cname)
    if "faed_survivor_int_tail32_scalar" in spec["encode"] and is_win_uncompressed(tail32):
        summary["wins"].append({"gap": g, "via": "h3_tail32_scalar"})


def main() -> int:
    results.clear()
    planted_control()
    for fn in (gap_g1, gap_g2, gap_g3, gap_g4, gap_g5, gap_g6, gap_g7):
        if summary["stopped_early"]:
            break
        fn()
    summary["structured_hits"] = len(summary["hits"])
    summary["win_hits"] = len(summary["wins"])
    out = ART / "round8_reader_gap.json"
    out.write_text(json.dumps(summary, indent=2) + "\n")
    record(
        "round8 within ~2k budget",
        summary["decrypts"] <= BUDGET + 50,
        f"{summary['decrypts']}/{BUDGET}",
    )
    print(
        f"round8: decrypts={summary['decrypts']} structured={summary['structured_hits']} "
        f"wins={summary['win_hits']} by_gap={summary['by_gap']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
