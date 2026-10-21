#!/usr/bin/env python3
"""Round 11: Sal enter-split + Terminal-first chain + joint #8000 (~2k decrypts).

Spec: team/preregister_round11_pipeline.json
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
SPEC = json.loads((ROOT / "team" / "preregister_round11_pipeline.json").read_text())
BUDGET = int(SPEC["budget_target"])

from crypto_known import is_win_uncompressed  # noqa: E402
from step1_btcseed import load_containers, win_key  # noqa: E402
from step3_mask import MASK6, apply_zeros, digits_of, to_bytes  # noqa: E402
from cryptanalyst_tests import (  # noqa: E402
    HASH225,
    ab_bits,
    ai_decimal_hex,
    planted_control,
    record,
    results,
)
from classify_unified import classify_unified  # noqa: E402
from round5_preregistered import decrypt_with_profile  # noqa: E402
from round7_chained_pipeline import (  # noqa: E402
    ARCH,
    CHECKER,
    DIGITS149,
    derivations_from_pt,
    lw_catalog,
)
from round8_reader_gap import SAL_PAGE  # noqa: E402
from round4_battery import decrypt_mdp5_bytes  # noqa: E402

FLOWER = "theflowerblossomsthroughwhatseemstobeaconcretesurface"
SHABEF_OUR = "sha256ourfirsthintisyourlastcommand"
HOST23 = "11110111001111011001100"
SPIRAL = (ART / "poster_spiral_bits.txt").read_text().strip()

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
    d = hashlib.sha256(answer.encode()).digest()
    if is_win_uncompressed(d):
        summary["wins"].append({"tag": tag, "via": "sha256(answer)"})
    body, _ = decrypt_with_profile(raw, answer, profile)
    if body and classify_unified(body) == "structured":
        summary["hits"].append({"gap": gap, "tag": tag, "container": cname, "profile": profile})
    if body:
        win_key(body, tag, summary["wins"])
    return body


def sal_spans() -> dict[str, str]:
    sp = SPEC["gaps"]["G1_sal_enter_join"]["sal_spans"]
    return {k: SAL_PAGE[a:b] for k, (a, b) in sp.items()}


def join_raw(mode: str, raw1: bytes, raw2: bytes) -> bytes:
    if mode == "concat_raw":
        return raw1 + raw2
    if mode == "xor_raw_minlen":
        n = min(len(raw1), len(raw2))
        return bytes(a ^ b for a, b in zip(raw1[:n], raw2[:n]))
    raise ValueError(mode)


def stage_passwords_g1(sp: dict[str, str]) -> list[tuple[str, str]]:
    lw = ai_decimal_hex(sp["lastwords_ai"]).decode("ascii", errors="replace")
    tp = ai_decimal_hex(sp["thispassword_ai"]).decode("ascii", errors="replace")
    enter_lit = ab_bits(sp["enter_ab"]).decode("ascii", errors="replace").strip("\x00")
    out: list[tuple[str, str]] = [
        ("lastwords_literal", lw),
        ("thispassword_literal", tp),
        ("shabef_four_literal", sp["shabef_1"]),
        ("shabef_anstoo_literal", sp["shabef_2"]),
        ("sha256our_expanded", SHABEF_OUR),
        ("phase1_hash225", HASH225),
        ("enter_ab_literal", enter_lit),
        ("recipe_lw_enter_tp", f"{lw}{enter_lit}{tp}"),
        ("sha256hex_lw", hashlib.sha256(lw.encode()).hexdigest()),
        ("sha256hex_recipe", hashlib.sha256(f"{lw}{enter_lit}{tp}".encode()).hexdigest()),
    ]
    return out


def run_g1() -> None:
    gap = "G1_sal_enter_join"
    gspec = SPEC["gaps"]["G1_sal_enter_join"]
    sp = sal_spans()
    b641 = "".join(sp["b64_half_1"].split())
    b642 = "".join(sp["b64_half_2"].split())
    raw1 = base64.b64decode(b641)
    raw2 = base64.b64decode(b642)
    sal_ref = (ART / "salphaseion_short.bin").read_bytes()
    joined = raw1 + raw2
    summary["checks"]["g1_join_equals_sal_short"] = joined == sal_ref
    record(
        "G1 joined b64 halves equal salphaseion_short.bin",
        joined == sal_ref,
        f"len={len(joined)}",
    )

    passwords = stage_passwords_g1(sp)
    profiles = gspec["profiles"]

    for mode in gspec["join_modes"]:
        blob = join_raw(mode, raw1, raw2)
        for pname, ans in passwords:
            for prof in profiles:
                if over_budget():
                    return
                try_decrypt(gap, blob, ans, prof, f"g1-{mode}-{pname}-{prof}", "salphaseion_short")
                if prof == "plain-md5":
                    bump(gap)
                    body, _ = decrypt_mdp5_bytes(blob, ans.encode())
                    if body and classify_unified(body) == "structured":
                        summary["hits"].append(
                            {"gap": gap, "tag": f"g1-{mode}-{pname}-md5blob", "container": "joined_blob"}
                        )

    for cname in gspec.get("containers", ["salphaseion_short"]):
        raw = load_containers()[cname]
        for pname, ans in passwords:
            for prof in profiles:
                if over_budget():
                    return
                try_decrypt(gap, raw, ans, prof, f"g1-{cname}-{pname}-{prof}", cname)
                if cname == "salphaseion_short" and prof == "plain-md5":
                    bump(gap)
                    body, _ = decrypt_mdp5_bytes(raw, ans.encode())
                    if body and classify_unified(body) == "structured":
                        summary["hits"].append(
                            {"gap": gap, "tag": f"g1-{cname}-{pname}-md5", "container": cname}
                        )


def phase32_initials() -> list[tuple[str, str]]:
    sel = ARCH.find("SELECT")
    p32 = (ART / "phase32.bin").read_bytes()
    ascii_head = p32[:446].decode("ascii", errors="replace")
    one_for_one = "oneforonefourforone"
    m = re.search(r"one for one.*?four for one", ascii_head, flags=re.I | re.S)
    if m:
        one_for_one = re.sub(r"[^a-z0-9]", "", m.group(0).lower())
    riddle = p32[2143:2291].decode("ascii", errors="replace").strip()
    out: list[tuple[str, str]] = []
    keys = SPEC["gaps"]["G2_terminal_first"]["phase32_initial_keys"]
    mapping = {
        "checker_decode": CHECKER,
        "checker_decode_sha256hex": hashlib.sha256(CHECKER.encode()).hexdigest(),
        "digits149_sum": str(sum(int(c) for c in DIGITS149)),
        "digits149_literal": DIGITS149,
        "arch_after_select_128": ARCH[sel + 6 : sel + 6 + 128].lower(),
        "arch_from_over_23": "fromovertwentythreecipherssixteenencryptions",
        "ascii_prefix_one_for_one": one_for_one,
        "riddle_phase32": re.sub(r"[^a-z0-9]", "", riddle.lower()),
        "beaufort_key_THEMATRIXHASYOU": "THEMATRIXHASYOU",
        "phase1_flower": FLOWER,
        "phase1_hash225": HASH225,
    }
    for k in keys:
        if k in mapping:
            out.append((k, mapping[k]))
    return out


def run_g2() -> None:
    gap = "G2_terminal_first"
    gspec = SPEC["gaps"]["G2_terminal_first"]
    order = gspec["order"]
    profiles = gspec["step_profiles"]
    lw_map = lw_catalog()
    lws = [lw_map[k] for k in gspec["lastwords_for_derivation"] if k in lw_map]
    initials = phase32_initials()
    containers = load_containers()

    for lw in lws:
        if over_budget():
            return
        # Reuse round7 chain helper but count under our budget via wrapper
        for iname, ians in initials:
            if over_budget():
                return
            body0 = try_decrypt(gap, containers[order[0]], ians, profiles[0], f"g2-s0-{iname}", order[0])
            if body0 is None:
                continue
            for d1n, ans1 in derivations_from_pt(body0, lw):
                if over_budget():
                    return
                body1 = try_decrypt(
                    gap, containers[order[1]], ans1, profiles[1], f"g2-s1-{iname}-{d1n}", order[1]
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
                        profiles[2],
                        f"g2-s2-{iname}-{d1n}-{d2n}",
                        order[2],
                    )

    if gspec.get("also_single_container_probe"):
        for iname, ians in initials:
            for cname in order:
                for prof in ("std-hex-sha256", "raw32-sha256"):
                    if over_budget():
                        return
                    try_decrypt(gap, containers[cname], ians, prof, f"g2-direct-{iname}-{cname}", cname)


def door_slice(source: str, indices: list[int]) -> str:
    if source == "digits149":
        s = DIGITS149
        return "".join(s[i - 1] for i in indices if 0 < i <= len(s))
    if source == "spiral196":
        return "".join(SPIRAL[i - 1] for i in indices if 0 < i <= len(SPIRAL))
    if source == "host_bits23":
        return "".join(HOST23[i - 1] for i in indices if 0 < i <= len(HOST23))
    return ""


def run_g3() -> None:
    gap = "G3_joint_8000"
    gspec = SPEC["gaps"]["G3_joint_8000"]
    indices = gspec["door_indices_1based"]
    blobs = load_containers()
    profiles = gspec["profiles"]
    containers = gspec["containers"]

    candidates: list[tuple[str, str]] = []
    for src in gspec["sources"]:
        sl = door_slice(src, indices)
        candidates.append((f"door-{src}", sl))
        candidates.append((f"door-{src}-sha", hashlib.sha256(sl.encode()).hexdigest()))

    if gspec.get("faed_zero_at_door"):
        d = digits_of((ART / "faed.txt").read_text().strip())
        zd = apply_zeros(d, indices)
        bb = to_bytes(zd)
        candidates.append(("faed-door-zero-bytes", bb.hex()))
        candidates.append(("faed-door-zero-sha", hashlib.sha256(bb).hexdigest()))

    if gspec.get("mask6_then_sha256hex"):
        d6 = digits_of((ART / "faed.txt").read_text().strip())
        z6 = apply_zeros(d6, MASK6)
        b6 = to_bytes(z6)
        candidates.append(("mask6-sha", hashlib.sha256(b6).hexdigest()))
        candidates.append(("mask6-hex", b6.hex()))

    base = list(candidates)
    for door_tag, host_part in [("host23", HOST23), ("host23-sha", hashlib.sha256(HOST23.encode()).hexdigest())]:
        for z_tag, z_val in base[:12]:
            combo = f"{host_part}{z_val}"
            candidates.append((f"joint-{door_tag}-{z_tag}", combo))
            candidates.append((f"joint-{door_tag}-{z_tag}-sha", hashlib.sha256(combo.encode()).hexdigest()))
    tail8446 = "verylaststepisatruegiveawaypromised"
    candidates.append(("8446-tail", tail8446))
    candidates.append(("8446-tail-sha", hashlib.sha256(tail8446.encode()).hexdigest()))

    seen: set[str] = set()
    for tag, ans in candidates:
        if ans in seen or not ans:
            continue
        seen.add(ans)
        for cname in containers:
            for prof in profiles:
                if over_budget():
                    return
                try_decrypt(gap, blobs[cname], ans, prof, f"g3-{tag}-{cname}", cname)


def main() -> int:
    results.clear()
    planted_control()
    run_g1()
    run_g2()
    run_g3()
    (ART / "round11_pipeline.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(
        f"round11: decrypts={summary['decrypts']}/{BUDGET} "
        f"hits={len(summary['hits'])} wins={len(summary['wins'])} "
        f"stopped={summary['stopped_early']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
