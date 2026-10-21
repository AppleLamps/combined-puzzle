#!/usr/bin/env python3
"""Round 12: z-stage program, pre-decode b64 joins, liberal Terminal-first.

Spec: team/preregister_round12_pipeline.json
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "team"))

ART = ROOT / "artifacts"
SPEC = json.loads((ROOT / "team" / "preregister_round12_pipeline.json").read_text())
BUDGET = int(SPEC["budget_target"])

from crypto_known import is_win_uncompressed  # noqa: E402
from step1_btcseed import load_containers, win_key  # noqa: E402
from step3_mask import tok23  # noqa: E402
from cryptanalyst_tests import (  # noqa: E402
    HASH225,
    SQUARE,
    ab_bits,
    ai_decimal_hex,
    bifid_decrypt,
    planted_control,
    record,
    results,
)
from classify_unified import classify_unified  # noqa: E402
from round4_battery import decrypt_mdp5_bytes  # noqa: E402
from round5_preregistered import decrypt_with_profile  # noqa: E402
from round7_chained_pipeline import (  # noqa: E402
    ARCH,
    CHECKER,
    DIGITS149,
    aes_full_blocks,
    derivations_from_pt,
    lw_catalog,
)
from round8_reader_gap import FAED, SAL_PAGE  # noqa: E402

HOST23 = "11110111001111011001100"
SHABEF_FOUR = "shabefourfirsthintisyourlastcommand"
FLOWER = "theflowerblossomsthroughwhatseemstobeaconcretesurface"

summary: dict = {
    "budget": BUDGET,
    "decrypts": 0,
    "by_gap": {},
    "hits": [],
    "wins": [],
    "liberal_scans": 0,
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


def try_decrypt(
    gap: str,
    raw: bytes,
    answer: str,
    profile: str,
    tag: str,
    cname: str,
) -> bytes | None:
    if over_budget() or not answer or len(answer) > 50000:
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


def op_value(name: str) -> str:
    msl_bits = SAL_PAGE[91:195].replace("a", "0").replace("b", "1")
    lw = ai_decimal_hex(SAL_PAGE[766:829]).decode("ascii", errors="replace")
    tp = ai_decimal_hex(SAL_PAGE[830:859]).decode("ascii", errors="replace")
    faed_plain = bifid_decrypt(FAED, SQUARE, 570)
    mapping = {
        "msl_ab_sum": str(sum(int(c) for c in msl_bits)),
        "faed_bifid_sha256hex": hashlib.sha256(faed_plain.encode()).hexdigest(),
        "faed_bifid_plain": faed_plain,
        "lastwords_literal": lw,
        "thispassword_literal": tp,
        "shabef_four_literal": SHABEF_FOUR,
        "host_bits_sha256hex": hashlib.sha256(HOST23.encode()).hexdigest(),
        "tok23": tok23(),
        "enter_literal": ab_bits(SAL_PAGE[959:999]).decode("ascii", errors="replace").strip("\x00"),
        "phase1_hash225": HASH225,
        "phase1_flower": FLOWER,
    }
    return mapping.get(name, "")


def reduce_chain(ops: list[str], mode: str) -> list[tuple[str, str]]:
    """Build password candidates from ordered stage ops."""
    vals = [op_value(o) for o in ops]
    vals = [v for v in vals if v]
    if not vals:
        return []
    out: list[tuple[str, str]] = []
    if mode == "concat_sha256hex_each":
        acc = vals[0]
        for i, v in enumerate(vals[1:], 1):
            acc = hashlib.sha256((acc + v).encode()).hexdigest()
            out.append((f"chain-sha-{i}", acc))
    if mode == "concat_literals_final_sha256hex":
        lit = "".join(vals)
        out.append((f"chain-lit-sha", hashlib.sha256(lit.encode()).hexdigest()))
        out.append((f"chain-lit", lit))
    return out


def run_g1_singles() -> None:
    gap = "G1_z_stage_program"
    gspec = SPEC["gaps"]["G1_z_stage_program"]
    blobs = load_containers()
    singles = [
        "msl_ab_sum",
        "faed_bifid_sha256hex",
        "faed_bifid_plain",
        "lastwords_literal",
        "thispassword_literal",
        "shabef_four_literal",
        "host_bits_sha256hex",
        "tok23",
        "enter_literal",
        "phase1_hash225",
        "phase1_flower",
    ]
    for op in singles:
        ans = op_value(op)
        if not ans:
            continue
        hx = hashlib.sha256(ans.encode()).hexdigest()
        for cname in gspec["containers"]:
            for prof in gspec["profiles"]:
                if over_budget():
                    return
                try_decrypt(gap, blobs[cname], ans, prof, f"g1-single-{op}-{cname}", cname)
                if over_budget():
                    return
                try_decrypt(gap, blobs[cname], hx, prof, f"g1-single-{op}-sha-{cname}", cname)


def run_g1() -> None:
    gap = "G1_z_stage_program"
    gspec = SPEC["gaps"]["G1_z_stage_program"]
    blobs = load_containers()

    stage_ops = [s["op"] for s in gspec["stages"]]
    for reducer in gspec["chain_reducers"]:
        for tag, ans in reduce_chain(stage_ops, reducer):
            for cname in gspec["containers"]:
                for prof in gspec["profiles"]:
                    if over_budget():
                        return
                    try_decrypt(gap, blobs[cname], ans, prof, f"g1-main-{tag}-{cname}", cname)

    for chain in gspec["also_chains"]:
        for reducer in gspec["chain_reducers"]:
            for tag, ans in reduce_chain(chain["ops"], reducer):
                for cname in gspec["containers"]:
                    for prof in gspec["profiles"]:
                        if over_budget():
                            return
                        try_decrypt(
                            gap,
                            blobs[cname],
                            ans,
                            prof,
                            f"g1-{chain['name']}-{tag}-{cname}",
                            cname,
                        )


def b64_halves() -> tuple[str, str]:
    g = SPEC["gaps"]["G2_predecode_b64_join"]
    a, b = g["half_spans"]
    return SAL_PAGE[a[0] : a[1]], SAL_PAGE[b[0] : b[1]]


def join_b64(mode: str, h1: str, h2: str) -> str:
    h1, h2 = h1.replace(" ", ""), h2.replace(" ", "")
    if mode == "interleave_chars":
        out = []
        for i in range(max(len(h1), len(h2))):
            if i < len(h1):
                out.append(h1[i])
            if i < len(h2):
                out.append(h2[i])
        return "".join(out)
    if mode == "reverse_half2_concat":
        return h1 + h2[::-1]
    if mode == "xor_char_codes_mod256":
        n = min(len(h1), len(h2))
        return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(h1[:n], h2[:n]))
    if mode == "swap_halves_concat":
        return h2 + h1
    raise ValueError(mode)


def z_program_password() -> str:
    ops = [s["op"] for s in SPEC["gaps"]["G1_z_stage_program"]["stages"]]
    cands = reduce_chain(ops, "concat_literals_final_sha256hex")
    return cands[0][1] if cands else ""


def run_g2() -> None:
    gap = "G2_predecode_b64_join"
    gspec = SPEC["gaps"]["G2_predecode_b64_join"]
    h1, h2 = b64_halves()
    sal_ref = (ART / "salphaseion_short.bin").read_bytes()
    ref_b64 = base64.b64encode(sal_ref).decode()
    summary["checks"]["canonical_concat_b64"] = (h1 + h2) == ref_b64.replace("\n", "")

    stage_ops = [s["op"] for s in SPEC["gaps"]["G1_z_stage_program"]["stages"]]
    lit_concat = "".join(op_value(o) for o in stage_ops if op_value(o))
    pw_src = {
        "z_program_final": z_program_password(),
        "enter_literal": op_value("enter_literal"),
        "phase1_hash225": HASH225,
        "host_bits_sha256hex": op_value("host_bits_sha256hex"),
        "faed_bifid_sha256hex": op_value("faed_bifid_sha256hex"),
        "chain_lit_concat": lit_concat,
    }

    for mode in gspec["modes"]:
        joined = join_b64(mode, h1, h2)
        # pad base64
        pad = (-len(joined)) % 4
        joined_padded = joined + "=" * pad
        try:
            raw = base64.b64decode(joined_padded, validate=False)
        except Exception:
            continue
        for src_name in gspec["password_sources"]:
            ans = pw_src.get(src_name, "")
            if not ans:
                continue
            for prof in gspec["profiles"]:
                if over_budget():
                    return
                try_decrypt(gap, raw, ans, prof, f"g2-{mode}-{src_name}-{prof}", gspec["container"])
                for cname in ("salphaseion_short", "terminal", "cosmic"):
                    raw_blob = load_containers()[cname]
                    if prof == "plain-md5" and cname != "salphaseion_short":
                        continue
                    if over_budget():
                        return
                    try_decrypt(gap, raw_blob, ans, prof, f"g2-{mode}-{src_name}-{cname}-{prof}", cname)
                    if cname == "salphaseion_short" and prof == "plain-md5":
                        bump(gap)
                        body, _ = decrypt_mdp5_bytes(raw_blob, ans.encode())
                        if body and classify_unified(body) == "structured":
                            summary["hits"].append(
                                {"gap": gap, "tag": f"g2-{mode}-{src_name}-md5", "container": cname}
                            )


def phase32_initials() -> list[tuple[str, str]]:
    gspec = SPEC["gaps"]["G3_liberal_terminal_first"]
    sel = ARCH.find("SELECT")
    p32 = (ART / "phase32.bin").read_bytes()
    ascii_head = p32[:446].decode("ascii", errors="replace")
    one_for_one = "oneforonefourforone"
    m = re.search(r"one for one.*?four for one", ascii_head, flags=re.I | re.S)
    if m:
        one_for_one = re.sub(r"[^a-z0-9]", "", m.group(0).lower())
    mapping = {
        "checker_decode": CHECKER,
        "checker_decode_sha256hex": hashlib.sha256(CHECKER.encode()).hexdigest(),
        "digits149_sum": str(sum(int(c) for c in DIGITS149)),
        "digits149_literal": DIGITS149,
        "arch_after_select_128": ARCH[sel + 6 : sel + 6 + 128].lower(),
        "ascii_prefix_one_for_one": one_for_one,
        "phase1_hash225": HASH225,
    }
    return [(k, mapping[k]) for k in gspec["phase32_initial_keys"] if k in mapping]


def liberal_candidates(full: bytes, windows: list[int]) -> list[tuple[str, bytes]]:
    """Derived answers from unpadded / sliding views of raw CBC output."""
    found: list[tuple[str, bytes]] = []
    if not full:
        return found
    if classify_unified(full) == "structured":
        found.append(("full_block", full))
    summary["liberal_scans"] += 1
    for w in windows:
        for start in range(0, max(1, len(full) - w + 1)):
            chunk = full[start : start + w]
            if len(chunk) < w:
                continue
            if classify_unified(chunk) == "structured":
                found.append((f"win{w}@{start}", chunk))
    # always offer digests of full raw decrypt
    found.append(("full_sha256hex", hashlib.sha256(full).hexdigest()))
    found.append(("full_hex", full.hex()))
    return found


def run_g3() -> None:
    gap = "G3_liberal_terminal_first"
    gspec = SPEC["gaps"]["G3_liberal_terminal_first"]
    order = gspec["order"]
    containers = load_containers()
    lw_map = lw_catalog()
    lws = [lw_map[k] for k in gspec["lastwords_for_derivation"] if k in lw_map]
    windows = gspec["window_scan_bytes"]
    initials = phase32_initials()
    term_raw = containers["terminal"]

    for iname, ians in initials:
        if over_budget():
            return
        for lprof in gspec["liberal_profiles"]:
            if over_budget():
                return
            bump(gap)
            full = aes_full_blocks(term_raw, ians, lprof)
            extras: list[tuple[str, str]] = []
            for label, blob in liberal_candidates(full, windows):
                if isinstance(blob, str):
                    extras.append((label, blob))
                elif label == "full_block":
                    extras.append(("latin1_full", blob.decode("latin-1", errors="replace")))
            # padded path
            body0 = try_decrypt(gap, term_raw, ians, lprof, f"g3-pad-{iname}-{lprof}", order[0])
            seeds: list[tuple[str, str]] = [(f"init-{iname}", ians)]
            if body0:
                seeds.extend((n, a) for n, a in derivations_from_pt(body0, lws[0]))
            seeds.extend((f"lib-{n}", a) for n, a in extras if isinstance(a, str))

            for cname in gspec.get("liberal_direct_containers", []):
                for prof in gspec.get("liberal_direct_profiles", []):
                    for sname, ans in seeds:
                        if not ans or over_budget():
                            continue
                        if cname == "salphaseion_short" and prof == "plain-md5":
                            try_decrypt(gap, containers[cname], ans, "plain-md5", f"g3-dir-{iname}-{sname}", cname)
                        elif prof != "plain-md5":
                            try_decrypt(gap, containers[cname], ans, prof, f"g3-dir-{iname}-{sname}-{prof}", cname)

            for lw in lws:
                for sname, ans in seeds:
                    if not ans or over_budget():
                        continue
                    body1 = try_decrypt(
                        gap,
                        containers[order[1]],
                        ans,
                        gspec["chain_profiles"][1],
                        f"g3-s1-{iname}-{sname}",
                        order[1],
                    )
                    if body1 is None:
                        continue
                    for d2n, ans2 in derivations_from_pt(body1, lw):
                        if over_budget():
                            return
                        try_decrypt(
                            gap,
                            containers[order[2]],
                            ans2,
                            gspec["chain_profiles"][2],
                            f"g3-s2-{iname}-{sname}-{d2n}",
                            order[2],
                        )

            # Liberal raw-CBC bytes -> derivation fan-out (pad not required)
            if full:
                for start in range(0, max(1, len(full) - 15), 8):
                    if over_budget():
                        return
                    pt_probe = full[start : start + 64]
                    if len(pt_probe) < 8:
                        continue
                    for lw in lws:
                        for dname, dans in derivations_from_pt(pt_probe, lw):
                            for cname in gspec.get("liberal_direct_containers", order):
                                for prof in ("std-hex-sha256", "raw32-sha256"):
                                    if over_budget():
                                        return
                                    try_decrypt(
                                        gap,
                                        containers[cname],
                                        dans,
                                        prof,
                                        f"g3-libderiv-{iname}-@{start}-{dname}-{cname}",
                                        cname,
                                    )


def main() -> int:
    results.clear()
    planted_control()
    record(
        "R11 canonical b64 halves concat",
        (SAL_PAGE[895:959] + SAL_PAGE[999:1063]) == base64.b64encode(
            (ART / "salphaseion_short.bin").read_bytes()
        ).decode(),
        "round12 baseline",
    )
    run_g1()
    run_g1_singles()
    run_g2()
    run_g3()
    (ART / "round12_pipeline.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(
        f"round12: decrypts={summary['decrypts']}/{BUDGET} "
        f"liberal_scans={summary['liberal_scans']} hits={len(summary['hits'])} "
        f"wins={len(summary['wins'])} stopped={summary['stopped_early']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
