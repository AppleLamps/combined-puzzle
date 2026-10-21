#!/usr/bin/env python3
"""Round 9: Reader gap G8–G15 + audit H1 Cosmic raw32 repair (~2k decrypts).

Spec: team/preregister_reader_gap9.json
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
SPEC = json.loads((ROOT / "team" / "preregister_reader_gap9.json").read_text())
BUDGET = int(SPEC["budget_target"])

from crypto_known import is_win_uncompressed  # noqa: E402
from step1_btcseed import load_containers, win_key  # noqa: E402
from step3_mask import tok23  # noqa: E402
from cryptanalyst_tests import (  # noqa: E402
    SQUARE,
    bifid_decrypt,
    planted_control,
    record,
    results,
)
from classify_unified import classify_unified  # noqa: E402
from round3_battery import spiral_coords, decrypt_mdp5  # noqa: E402
from round4_battery import decrypt_mdp5_bytes  # noqa: E402
from round5_preregistered import decrypt_with_profile  # noqa: E402
from round8_reader_gap import FILLER60, FAED, SAL_PAGE  # noqa: E402
from round7_chained_pipeline import lw_catalog, msl_catalog, step0_passwords  # noqa: E402

SPIRAL_COLOURS = (ART / "yellowblue_colours.txt").read_text().strip()
HOST_BITS_V = "11110111001111011001100"
SHABEF_EXP = "sha256ourfirsthintisyourlastcommand"

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


def bump(gap: str, n: int = 1) -> None:
    summary["decrypts"] += n
    summary["by_gap"][gap] = summary["by_gap"].get(gap, 0) + n
    if summary["decrypts"] >= BUDGET:
        summary["stopped_early"] = True


def try_decrypt(gap: str, raw: bytes, answer: str, profile: str, tag: str, cname: str) -> bytes | None:
    if over_budget() or not answer or len(answer) > 20000:
        return None
    bump(gap)
    d = hashlib.sha256(answer.encode()).digest()
    if is_win_uncompressed(d):
        summary["wins"].append({"tag": tag, "via": "sha256(answer)"})
    body, _ = decrypt_with_profile(raw, answer, profile)
    if body and classify_unified(body) == "structured":
        summary["hits"].append({"gap": gap, "tag": tag, "container": cname, "profile": profile})
    if body:
        win_key(body, tag, summary["wins"])
        if len(body) == 32 and is_win_uncompressed(body):
            summary["wins"].append({"tag": tag, "via": "plaintext32", "container": cname})
    return body


def try_md5(gap: str, raw: bytes, answer: str, tag: str, cname: str) -> None:
    if over_budget():
        return
    bump(gap)
    body, _ = decrypt_mdp5_bytes(raw, answer.encode())
    if body and classify_unified(body) == "structured":
        summary["hits"].append({"gap": gap, "tag": tag, "container": cname, "profile": "plain-md5"})


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


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for d in range(3, int(n**0.5) + 1, 2):
        if n % d == 0:
            return False
    return True


def dbbi_walk(colours: str, text: str, start_idx: int = 0, start_pos: int = 1, start_ci: int = 0):
    idx, pos, ci = start_idx, start_pos, start_ci
    hosts, fillers = [], []
    while idx < len(text):
        if is_prime(pos):
            if ci >= len(colours):
                return hosts, fillers, idx, pos, False
            col = colours[ci]
            ci += 1
            need = 2 if col == "Y" else 1
            hosts.append((pos, col, text[idx : idx + need]))
            idx += need
        else:
            fillers.append(text[idx])
            idx += 1
        pos += 1
    return hosts, fillers, idx, pos, len(hosts) == 23 and all(h[2].startswith("b") for h in hosts)


def host_bits_from_hosts(hosts: list) -> str:
    return "".join("1" if h[1] in "BF" else "0" for h in hosts)


def colour_sequence(name: str, faed_prefix: int = 0) -> str:
    base = SPIRAL_COLOURS
    if name.endswith("_F_as_Y"):
        base = base.replace("F", "Y")
    elif name.endswith("_plus_faed_prefix4"):
        extra = "".join(c if c in "BYF" else "B" for c in FAED[:faed_prefix])
        base = base + extra
    return base.replace("_F_as_Y", "").replace("_plus_faed_prefix4", "") if "_plus" in name else (
        base.replace("F", "Y") if "_F_as_Y" in name else base
    )


def gap_g8() -> None:
    g8 = "G8"
    spec8 = SPEC["gaps"]["G8_dbbi_past_97"]
    blobs = load_containers()
    text = SAL_PAGE.replace(" ", "")
    sequences = {
        "BBBBYBBBYYBBBBYBBYYBFYYBY": SPIRAL_COLOURS,
        "BBBBYBBBYYBBBBYBBYYBFYYBY_F_as_Y": SPIRAL_COLOURS.replace("F", "Y"),
        "BBBBYBBBYYBBBBYBBYYBFYYBY_plus_faed_prefix4": SPIRAL_COLOURS
        + "BYFB",
    }
    candidates: list[tuple[str, str]] = [(HOST_BITS_V, "hostbits-v")]
    for seq_name, colours in sequences.items():
        col = "".join(c for c in colours if c in "BYF")
        hosts, _, _, _, ok91 = dbbi_walk(col, text[:91])
        if ok91:
            candidates.append((host_bits_from_hosts(hosts), f"walk91-{seq_name[:8]}"))
        hosts2, _, _, _, ok_ext = dbbi_walk(colours, text[91:], start_pos=84, start_ci=23)
        if ok_ext:
            candidates.append((host_bits_from_hosts(hosts2), f"cont-{seq_name[:8]}"))
    for bits, label in candidates:
        for ans in (bits, hashlib.sha256(bits.encode()).hexdigest()):
            for cname in spec8["containers"]:
                try_decrypt(g8, blobs[cname], ans, "std-hex-sha256", f"g8-{label}", cname)


def weighted_spiral_sum(wk: int, ww: int, wb: int, wy: int, wf: int) -> int:
    m = json.loads((ART / "matrix.json").read_text())
    grid = m["letters"]
    total = 0
    for r, c in spiral_coords(14):
        ch = grid[r][c]
        w = {"K": wk, "W": ww, "B": wb, "Y": wy, "F": wf}.get(ch, 0)
        total += w
    return total


def gap_g9() -> None:
    g = "G9"
    spec = SPEC["gaps"]["G9_roses_weight_tuples"]
    lw = spec["recipe_lw"]
    for tup in spec["tuples"]:
        msl = str(weighted_spiral_sum(*tup))
        recipe = f"{msl}enter{lw}thispassword{msl}"
        emit_std_md5_raw(g, msl, f"g9-msl-{tup}", spec["containers"], spec["kdf"])
        emit_std_md5_raw(g, recipe, f"g9-recipe-{tup}", spec["containers"], spec["kdf"])


def filler_square_25() -> str:
    seen: list[str] = []
    for ch in FILLER60:
        if ch not in seen:
            seen.append(ch)
    for ch in "abcdefghijklmnopqrstuvwxyz":
        if ch not in seen and len(seen) < 25:
            seen.append(ch)
    return "".join(seen[:25])


def gap_g10() -> None:
    g = "G10"
    spec = SPEC["gaps"]["G10_bifid_period_divisors"]
    squares = {
        "dbifhcegaklmnopqrstuvwxyz": SQUARE,
        "filler_first_appearance": filler_square_25(),
    }
    blobs = load_containers()
    for sq_name in spec.get("squares", [spec.get("square", SQUARE)]):
        square = squares.get(sq_name, SQUARE)
        for period in spec["periods"]:
            if len(FAED) % period != 0 and period != 570:
                continue
            pt = bifid_decrypt(FAED, square, period)
            for ans in (
                pt,
                hashlib.sha256(pt.encode()).hexdigest(),
                pt[:64],
                pt[8:],
            ):
                for cname in spec["containers"]:
                    try_decrypt(
                        g, blobs[cname], ans, "std-hex-sha256", f"g10-{sq_name}-p{period}-{cname}", cname
                    )


def gap_g11() -> None:
    g = "G11"
    spec = SPEC["gaps"]["G11_parse_chain"]
    blobs = load_containers()
    order = spec["chain_order"]
    step0_map = {
        "host_bits_sha256hex": hashlib.sha256(HOST_BITS_V.encode()).hexdigest(),
        "shabef_expanded_sha256hex": hashlib.sha256(SHABEF_EXP.encode()).hexdigest(),
        "dbbi91_sha256hex": hashlib.sha256(SAL_PAGE[:91].encode()).hexdigest(),
    }
    suffix = spec["step2_suffix"]
    for key in spec["step0"]:
        s0 = step0_map[key]
        for cname in order:
            try_decrypt(g, blobs[cname], s0, "std-hex-sha256", f"g11-s0-{key}-{cname}", cname)
        body0, _ = decrypt_with_profile(blobs[order[0]], s0, "std-hex-sha256")
        mid = (
            body0.decode("latin-1", errors="replace")
            if body0
            else s0
        )
        for s1 in (
            hashlib.sha256((mid + suffix).encode()).hexdigest(),
            hashlib.sha256((s0 + suffix).encode()).hexdigest(),
        ):
            try_decrypt(g, blobs[order[1]], s1, "std-hex-sha256", f"g11-s1-{key}", order[1])
            try_decrypt(g, blobs[order[1]], s1, "raw32-sha256", f"g11-s1-r32-{key}", order[1])
            s2 = hashlib.sha256((s1 + "yinyang").encode()).hexdigest()
            try_decrypt(g, blobs[order[2]], s2, "std-hex-sha256", f"g11-s2-{key}", order[2])
            try_decrypt(g, blobs[order[2]], s2, "raw32-sha256", f"g11-s2r32-{key}", order[2])


def gap_g13() -> None:
    g = "G13"
    spec = SPEC["gaps"]["G13_nonprime_filler_keep"]
    kept = "".join(ch for i, ch in enumerate(FILLER60, 1) if is_prime(i))
    ans = hashlib.sha256(kept.encode()).hexdigest()
    blobs = load_containers()
    for cname in spec["containers"]:
        try_decrypt(g, blobs[cname], kept, "std-hex-sha256", f"g13-lit-{cname}", cname)
        try_decrypt(g, blobs[cname], ans, "std-hex-sha256", f"g13-sha-{cname}", cname)


def gap_g14() -> None:
    g = "G14"
    spec = SPEC["gaps"]["G14_dots_index_channel"]
    m = json.loads((ART / "matrix.json").read_text())
    grid = m["letters"]
    order = spiral_coords(14)
    sal = SAL_PAGE.replace(" ", "")
    blobs = load_containers()
    extracted: list[tuple[str, str]] = []
    for n in spec["dot_counts"]:
        if "spiral_index_minus1" in spec["mappings"] and n <= len(order):
            r, c = order[n - 1]
            extracted.append((f"spiral-{n}", grid[r][c]))
        if "spiral_row_major" in spec["mappings"]:
            idx = (n * 14) % len(order)
            r, c = order[idx]
            extracted.append((f"rowmaj-{n}", grid[r][c]))
        if "sal_span_offset" in spec["mappings"]:
            off = 91 + n
            if off < len(sal):
                extracted.append((f"sal-{n}", sal[off]))
    chars = "".join(ch for _, ch in extracted)
    answers: list[tuple[str, str]] = [(chars, "join"), (hashlib.sha256(chars.encode()).hexdigest(), "join-sha")]
    for name, ch in extracted:
        answers.append((ch, name))
        answers.append((hashlib.sha256(ch.encode()).hexdigest(), f"{name}-sha"))
    for ans, label in answers:
        for cname in ("terminal", "salphaseion_short", "cosmic"):
            try_decrypt(g, blobs[cname], ans, "std-hex-sha256", f"g14-{label}", cname)
            try_decrypt(g, blobs[cname], ans, "raw32-sha256", f"g14-{label}-r32", cname)


def gap_g15() -> None:
    g = "G15"
    blobs = load_containers()
    variants = {
        "with_F": SPIRAL_COLOURS,
        "F_mapped_to_Y": SPIRAL_COLOURS.replace("F", "Y"),
        "F_mapped_to_B": SPIRAL_COLOURS.replace("F", "B"),
    }
    text = SAL_PAGE.replace(" ", "")[:91]
    for name, colours in variants.items():
        col = "".join(c for c in colours if c in "BYF")
        hosts, _, _, _, ok = dbbi_walk(col, text)
        if not ok:
            continue
        bits = host_bits_from_hosts(hosts)
        msl = str(sum(int(b) for b in bits))
        recipe = f"{msl}enterlastwordsbeforearchichoicethispassword{msl}"
        for ans in (bits, hashlib.sha256(bits.encode()).hexdigest(), recipe):
            for cname in ("terminal", "salphaseion_short", "cosmic"):
                try_decrypt(g, blobs[cname], ans, "std-hex-sha256", f"g15-{name}", cname)


def gap_g2_bit_replay() -> None:
    """Capped replay of #6913 21-bit windows (round8 G2) to use budget."""
    from round8_reader_gap import bits_from_source, pack_bits

    g = "G2r"
    blobs = load_containers()
    sources = (
        "spiral_url192",
        "spiral_full196",
        "terminal_ciphertext",
        "salphaseion_short_ciphertext",
        "xor_terminal_sal_ciphertext",
        "cosmic_ciphertext",
    )
    for src in sources:
        bits = bits_from_source(src)
        for off in range(0, min(len(bits) - 21, 480), 3):
            if over_budget():
                return
            for packing in ("msb", "lsb"):
                rawb = pack_bits(bits, 21, off, packing)
                if not rawb:
                    continue
                for ans in (hashlib.sha256(rawb).hexdigest(), rawb.hex()):
                    for cname in ("terminal", "salphaseion_short", "cosmic"):
                        try_decrypt(
                            g, blobs[cname], ans, "std-hex-sha256", f"g2r21-{src}-{off}", cname
                        )
        if len(bits) >= 1812 and src == "cosmic_ciphertext":
            for off in (0, 256, 512, 1024):
                if over_budget():
                    return
                for packing in ("msb", "lsb"):
                    rawb = pack_bits(bits, 1812, off, packing)
                    if not rawb:
                        continue
                    ans = hashlib.sha256(rawb).hexdigest()
                    for cname in ("terminal", "cosmic"):
                        try_decrypt(g, blobs[cname], ans, "std-hex-sha256", f"g2r1812-{off}", cname)


def gap_audit_h1() -> None:
    g = "G_audit"
    spec = SPEC["gaps"]["G_audit_h1_cosmic_raw32"]
    blobs = load_containers()
    cosmic = blobs["cosmic"]
    msls = msl_catalog()
    lws = lw_catalog()
    yin = "yinyang"
    for mkey in spec["msl"]:
        mval = msls.get(mkey)
        if not mval:
            continue
        for lkey in spec["lw"]:
            lwval = lws.get(lkey)
            if not lwval:
                continue
            for s0name, s0ans in step0_passwords(mval)[:4]:
                for mid_src in (s0ans, hashlib.sha256((tok23() + mval).encode()).hexdigest()):
                    s2 = hashlib.sha256((mid_src + lwval).encode()).hexdigest()
                    s3 = hashlib.sha256((s2 + yin).encode()).hexdigest()
                    for ans, label in ((s2, "s2"), (s3, "s3"), (s0ans, "s0-cosmic")):
                        try_decrypt(
                            g, cosmic, ans, "raw32-sha256", f"audit-{mkey}-{lkey}-{label}", "cosmic"
                        )
                        try_decrypt(
                            g, cosmic, ans, "std-hex-sha256", f"audit-{mkey}-{lkey}-{label}-std", "cosmic"
                        )


def main() -> int:
    results.clear()
    planted_control()
    for fn in (
        gap_g8,
        gap_g9,
        gap_g10,
        gap_g11,
        gap_g13,
        gap_g14,
        gap_g15,
        gap_audit_h1,
        gap_g2_bit_replay,
    ):
        if summary["stopped_early"]:
            break
        fn()
    summary["structured_hits"] = len(summary["hits"])
    (ART / "round9_reader_gap.json").write_text(json.dumps(summary, indent=2) + "\n")
    record("round9 budget", summary["decrypts"] <= BUDGET + 50, f"{summary['decrypts']}/{BUDGET}")
    print(
        f"round9: decrypts={summary['decrypts']} structured={summary['structured_hits']} "
        f"wins={len(summary['wins'])} by_gap={summary['by_gap']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
