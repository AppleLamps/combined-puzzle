#!/usr/bin/env python3
"""Round 13: byte XOR enter, poster matrixsumlist z-chain, full Sal stage-0.

Spec: team/preregister_round13_pipeline.json
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
SPEC = json.loads((ROOT / "team" / "preregister_round13_pipeline.json").read_text())
BUDGET = int(SPEC["budget_target"])

from crypto_known import is_win_uncompressed  # noqa: E402
from step1_btcseed import load_containers, win_key  # noqa: E402
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
from round3_battery import poster_sums  # noqa: E402
from round4_battery import decrypt_mdp5_bytes  # noqa: E402
from round5_preregistered import decrypt_with_profile  # noqa: E402
from round8_reader_gap import FAED, SAL_PAGE  # noqa: E402
from round12_pipeline import reduce_chain  # noqa: E402

SHABEF_FOUR = "shabefourfirsthintisyourlastcommand"
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
    if over_budget() or not answer or len(answer) > 80000:
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


def sal_literals() -> dict[str, str]:
    lw = ai_decimal_hex(SAL_PAGE[766:829]).decode("ascii", errors="replace")
    tp = ai_decimal_hex(SAL_PAGE[830:859]).decode("ascii", errors="replace")
    enter = ab_bits(SAL_PAGE[959:999]).decode("ascii", errors="replace").strip("\x00")
    faed_plain = bifid_decrypt(FAED, SQUARE, 570)
    msl_bits = SAL_PAGE[91:195].replace("a", "0").replace("b", "1")
    z_sha = reduce_chain(
        [
            "msl_ab_sum",
            "faed_bifid_sha256hex",
            "lastwords_literal",
            "thispassword_literal",
            "shabef_four_literal",
        ],
        "concat_literals_final_sha256hex",
    )
    z_lit_sha = z_sha[0][1] if z_sha else ""
    return {
        "lastwords_literal": lw,
        "thispassword_literal": tp,
        "enter_literal": enter,
        "z_chain_lit_sha": z_lit_sha,
        "phase1_hash225": HASH225,
        "faed_bifid_sha256hex": hashlib.sha256(faed_plain.encode()).hexdigest(),
        "msl_ab_sum": str(sum(int(c) for c in msl_bits)),
    }


def decode_halves() -> tuple[bytes, bytes]:
    g = SPEC["gaps"]["G1_enter_xor_bytes"]
    a, b = g["half_spans"]
    h1 = "".join(SAL_PAGE[a[0] : a[1]].split())
    h2 = "".join(SAL_PAGE[b[0] : b[1]].split())
    return base64.b64decode(h1), base64.b64decode(h2)


def xor_bytes(a: bytes, b: bytes) -> bytes:
    n = min(len(a), len(b))
    return bytes(x ^ y for x, y in zip(a[:n], b[:n]))


def build_xor_blobs(raw1: bytes, raw2: bytes) -> dict[str, bytes]:
    sal_ref = (ART / "salphaseion_short.bin").read_bytes()
    out: dict[str, bytes] = {}
    out["xor_full_48"] = xor_bytes(raw1, raw2)
    if raw1[:8] == b"Salted__" and raw2[:8] == b"Salted__":
        salt1, ct1 = raw1[8:16], raw1[16:]
        salt2, ct2 = raw2[8:16], raw2[16:]
        n = min(len(ct1), len(ct2))
        out["xor_ct_only"] = raw1[:16] + bytes(a ^ b for a, b in zip(ct1[:n], ct2[:n]))
        out["xor_salt_prefix_rest_xor"] = raw1[:16] + xor_bytes(ct1, ct2)
        out["concat_then_xor_ct"] = raw1[:16] + xor_bytes(ct1 + ct2[: max(0, len(ct1) - len(ct2))], ct2 + ct1[: max(0, len(ct2) - len(ct1))])
    out["canonical_concat"] = raw1 + raw2
    summary["checks"]["xor_full_equals_canonical"] = out.get("xor_full_48") != sal_ref
    summary["checks"]["canonical_equals_sal_short"] = out["canonical_concat"] == sal_ref
    return out


def poster_msl_value(key: str) -> str:
    return poster_sums().get(key, "")


def op_by_name(name: str) -> str:
    if name.startswith("poster:"):
        return poster_msl_value(name.split(":", 1)[1])
    lit = sal_literals()
    if name in lit:
        return lit[name]
    if name == "msl_ab_sum":
        return lit["msl_ab_sum"]
    if name == "faed_bifid_sha256hex":
        return lit["faed_bifid_sha256hex"]
    if name == "lastwords_literal":
        return lit["lastwords_literal"]
    if name == "thispassword_literal":
        return lit["thispassword_literal"]
    if name == "shabef_four_literal":
        return SHABEF_FOUR
    if name == "enter_literal":
        return lit["enter_literal"]
    return ""


def reduce_named_chain(ops: list[str], mode: str) -> list[tuple[str, str]]:
    vals = [op_by_name(o) for o in ops]
    vals = [v for v in vals if v]
    if not vals:
        return []
    out: list[tuple[str, str]] = []
    if mode == "concat_sha256hex_each":
        acc = vals[0]
        for i, v in enumerate(vals[1:], 1):
            acc = hashlib.sha256((acc + v).encode()).hexdigest()
            out.append((f"sha-{i}", acc))
    if mode == "concat_literals_final_sha256hex":
        lit = "".join(vals)
        out.append(("lit-sha", hashlib.sha256(lit.encode()).hexdigest()))
        out.append(("lit", lit))
    return out


def run_g1() -> None:
    gap = "G1_enter_xor_bytes"
    gspec = SPEC["gaps"]["G1_enter_xor_bytes"]
    raw1, raw2 = decode_halves()
    blobs_map = build_xor_blobs(raw1, raw2)
    record(
        "canonical half concat equals sal short",
        blobs_map["canonical_concat"] == (ART / "salphaseion_short.bin").read_bytes(),
        f"len={len(blobs_map['canonical_concat'])}",
    )
    anchors = sal_literals()
    containers = load_containers()

    def passwords_for(blob: bytes) -> list[tuple[str, str]]:
        xor_hex = blob.hex()
        pw: list[tuple[str, str]] = []
        for key in gspec["password_anchors"]:
            if key == "xor_hex_sha256hex":
                pw.append((key, hashlib.sha256(xor_hex.encode()).hexdigest()))
            elif key in anchors:
                pw.append((key, anchors[key]))
        pw.append(("xor_bytes_sha256hex", hashlib.sha256(blob).hexdigest()))
        return pw

    try_targets = list(gspec["xor_targets"]) + ["canonical_concat"]
    for target in try_targets:
        blob = blobs_map.get(target)
        if not blob:
            continue
        for pname, ans in passwords_for(blob):
            if over_budget():
                return
            try_decrypt(gap, blob, ans, "std-hex-sha256", f"g1-{target}-{pname}-blob-std", "salphaseion_short")
            bump(gap)
            body, _ = decrypt_mdp5_bytes(blob, ans.encode())
            if body and classify_unified(body) == "structured":
                summary["hits"].append({"gap": gap, "tag": f"g1-md5-{target}-{pname}", "container": "xor_blob"})
            for cname in gspec["containers"]:
                for prof in gspec["profiles"]:
                    if cname == "salphaseion_short":
                        raw = blob if target != "canonical_concat" else containers[cname]
                    else:
                        raw = containers[cname]
                    if over_budget():
                        return
                    try_decrypt(gap, raw, ans, prof, f"g1-{target}-{pname}-{cname}-{prof}", cname)


def run_g2() -> None:
    gap = "G2_poster_msl_zchain"
    gspec = SPEC["gaps"]["G2_poster_msl_zchain"]
    suffix = gspec["chain_suffix"]
    blobs = load_containers()

    for mkey in gspec["poster_msl_keys"]:
        ops = [f"poster:{mkey}"] + suffix
        for reducer in gspec["reducers"]:
            for tag, ans in reduce_named_chain(ops, reducer):
                for cname in gspec["containers"]:
                    for prof in gspec["profiles"]:
                        if over_budget():
                            return
                        try_decrypt(gap, blobs[cname], ans, prof, f"g2-{mkey}-{tag}-{cname}", cname)
                        if cname == "salphaseion_short" and prof == "plain-md5":
                            bump(gap)
                            body, _ = decrypt_mdp5_bytes(blobs[cname], ans.encode())
                            if body and classify_unified(body) == "structured":
                                summary["hits"].append(
                                    {"gap": gap, "tag": f"g2-{mkey}-md5", "container": cname}
                                )
        # poster key alone
        solo = poster_msl_value(mkey)
        if solo:
            for cname in gspec["containers"]:
                for prof in gspec["profiles"]:
                    if over_budget():
                        return
                    try_decrypt(gap, blobs[cname], solo, prof, f"g2-{mkey}-solo-{cname}", cname)
                    hx = hashlib.sha256(solo.encode()).hexdigest()
                    try_decrypt(gap, blobs[cname], hx, prof, f"g2-{mkey}-solo-sha-{cname}", cname)


def stage0_full_sal(form: str) -> str:
    if form == "compact_1075_sha256hex":
        return hashlib.sha256(SAL_PAGE.encode()).hexdigest()
    if form == "compact_1075_literal_prefix512":
        return SAL_PAGE[:512]
    if form == "dbbi_faed_concat_sha256hex":
        chunk = SAL_PAGE[0:91] + SAL_PAGE[195:765]
        return hashlib.sha256(chunk.encode()).hexdigest()
    if form == "pre_sal_895_sha256hex":
        return hashlib.sha256(SAL_PAGE[:895].encode()).hexdigest()
    if form == "post_z_stages_860_1075_sha256hex":
        return hashlib.sha256(SAL_PAGE[860:1075].encode()).hexdigest()
    return ""


def run_g3() -> None:
    gap = "G3_full_sal_stage0"
    gspec = SPEC["gaps"]["G3_full_sal_stage0"]
    blobs = load_containers()
    suffix_ops = gspec["chain_ops"]

    for form in gspec["stage0_forms"]:
        s0 = stage0_full_sal(form)
        if not s0:
            continue
        chains = [
            ("s0-only", s0),
            ("s0-sha", hashlib.sha256(s0.encode()).hexdigest()),
        ]
        for op in suffix_ops:
            val = op_by_name(op)
            if not val:
                continue
            chains.append((f"s0-{op}", hashlib.sha256((s0 + val).encode()).hexdigest()))
            chains.append((f"s0-{op}-lit", s0 + val))
        for mkey in ("sum-rows", "spiral-bits", "sum-cols"):
            ops = [s0, poster_msl_value(mkey)] + [op_by_name(o) for o in suffix_ops]
            ops = [x for x in ops if x]
            lit = "".join(ops)
            chains.append((f"full-{mkey}-lit-sha", hashlib.sha256(lit.encode()).hexdigest()))
            acc = ops[0]
            for i, v in enumerate(ops[1:], 1):
                acc = hashlib.sha256((acc + v).encode()).hexdigest()
                chains.append((f"full-{mkey}-roll-{i}", acc))

        seen: set[str] = set()
        for ctag, ans in chains:
            if not ans or ans in seen:
                continue
            seen.add(ans)
            for cname in gspec["containers"]:
                for prof in gspec["profiles"]:
                    if over_budget():
                        return
                    if cname == "salphaseion_short" and prof == "raw32-sha256":
                        continue
                    try_decrypt(gap, blobs[cname], ans, prof, f"g3-{form}-{ctag}-{cname}", cname)
                    if cname == "salphaseion_short" and prof == "plain-md5":
                        bump(gap)
                        body, _ = decrypt_mdp5_bytes(blobs[cname], ans.encode())
                        if body and classify_unified(body) == "structured":
                            summary["hits"].append(
                                {"gap": gap, "tag": f"g3-{form}-md5", "container": cname}
                            )


def main() -> int:
    results.clear()
    planted_control()
    run_g1()
    run_g2()
    run_g3()
    (ART / "round13_pipeline.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(
        f"round13: decrypts={summary['decrypts']}/{BUDGET} "
        f"hits={len(summary['hits'])} wins={len(summary['wins'])} stopped={summary['stopped_early']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
