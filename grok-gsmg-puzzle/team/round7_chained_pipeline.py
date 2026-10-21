#!/usr/bin/env python3
"""Round 7: all chained pipeline suggestions (H1, M3, 6 container orders, yinyang mid-chain).

Frozen spec: team/preregister_chained_pipeline.json
"""

from __future__ import annotations

import hashlib
import itertools
import json
import re
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "team"))

ART = ROOT / "artifacts"
SPEC = json.loads((ROOT / "team" / "preregister_chained_pipeline.json").read_text())
BUDGET = int(SPEC["budget_decrypts"])

from Crypto.Cipher import AES  # noqa: E402

from crypto_known import (  # noqa: E402
    decrypt_salted,
    evp_bytes_to_key,
    is_win_uncompressed,
    pkcs7_unpad,
)
from step1_btcseed import load_containers  # noqa: E402
from step3_mask import matrix_strings, tok23  # noqa: E402
from cryptanalyst_tests import (  # noqa: E402
    classify_plaintext,
    message_8446_text,
    planted_control,
    record,
    results,
)
from round3_battery import poster_sums, word_lastwords_candidates  # noqa: E402
from round5_preregistered import decrypt_with_profile  # noqa: E402

ARCH = (ART / "phase32_beaufort.txt").read_text().strip()
CHECKER = (ART / "phase32_checkerboard.txt").read_text().strip()
SAL_PAGE = (ART / "salphaseion.txt").read_text().strip()
FLOWER = "theflowerblossomsthroughwhatseemstobeaconcretesurface"
FLOWER_HASH = "5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75"
DIGITS149 = re.search(rb"(\d{149})", (ART / "phase32.bin").read_bytes()).group(1).decode()

summary: dict = {
    "decrypts": 0,
    "budget": BUDGET,
    "hits": [],
    "families": {},
    "stopped_early": False,
}


def inc(n: int = 1) -> bool:
    """Return True if still within budget."""
    summary["decrypts"] += n
    if summary["decrypts"] > BUDGET:
        summary["stopped_early"] = True
        return False
    return True


def ab_bits(s: str) -> bytes:
    if len(s) % 8:
        s = s + "a" * (8 - len(s) % 8)
    return bytes(int(s[i : i + 8].replace("a", "0").replace("b", "1"), 2) for i in range(0, len(s), 8))


def xor_bytes(a: bytes, b: bytes) -> bytes:
    n = max(len(a), len(b))
    if n == 0:
        return b""
    a = (a * (n // len(a) + 1))[:n]
    b = (b * (n // len(b) + 1))[:n]
    return bytes(x ^ y for x, y in zip(a, b))


def spiral_row_sums() -> list[int]:
    spiral = (ART / "poster_spiral_bits.txt").read_text().strip()
    groups = [spiral[i : i + 14] for i in range(0, len(spiral), 14)]
    return [sum(int(c) for c in g) for g in groups]


def sal_ab_14_row_sums() -> str:
    bits = SAL_PAGE[91:195].replace("a", "0").replace("b", "1")
    while len(bits) < 14:
        bits += "0"
    chunk = max(1, len(bits) // 14)
    parts = []
    for i in range(14):
        seg = bits[i * chunk : (i + 1) * chunk]
        if not seg:
            seg = "0"
        parts.append(str(sum(int(c) for c in seg)))
    return "-".join(parts)


def spiral_diag_sums() -> str:
    m = json.loads((ART / "matrix.json").read_text())
    bit = m["bit_grid"]
    main = sum(int(bit[i][i]) for i in range(14))
    anti = sum(int(bit[i][13 - i]) for i in range(14))
    return f"{main}-{anti}"


def choice_lastwords_join() -> str:
    sel = ARCH.find("SELECT")
    tail = ARCH[sel + 6 :]
    words = re.findall(r"[A-Z]{3,}", tail)
    # last word before each SELECT-relative clause chunk (every 5 words)
    chunks = [words[i : i + 5] for i in range(0, len(words), 5) if words[i : i + 5]]
    lastw = [c[-1].lower() for c in chunks if c]
    return "-".join(lastw) if lastw else words[-1].lower()


def msl_catalog() -> dict[str, str]:
    S = spiral_row_sums()
    ab_span = SAL_PAGE[91:195]
    bits_sum = str(sum(int(c) for c in ab_span.replace("a", "0").replace("b", "1")))
    spiral = (ART / "poster_spiral_bits.txt").read_text().strip()
    msl = matrix_strings()
    return {
        "list_row_sums_dash": "-".join(str(x) for x in S),
        "list_row_sums_sep": "-".join(str(x) for x in S),
        "list_row_sums": "".join(str(x) for x in S),
        "spiral_ab_bytes_hex": ab_bits(ab_span.replace("a", "0").replace("b", "1")).hex(),
        "sal_ab_14_row_sums": sal_ab_14_row_sums(),
        "spiral_diag_sums": spiral_diag_sums(),
        "msl-row": msl["row"],
        "msl-col": msl["col"],
        "msl-sum-ab-bits": bits_sum,
        "spiral-int": str(int(spiral, 2)),
        "tok23_plus_row_sums": tok23() + "".join(str(x) for x in S),
        "checker149_sum": str(sum(int(c) for c in DIGITS149)),
        "checker_decode": CHECKER,
        "poster_sum_rows": poster_sums()["sum-rows"],
    }


def lw_catalog() -> dict[str, str]:
    sel = ARCH.find("SELECT")
    lw40 = ARCH[max(0, sel - 40) : sel].lower()
    out = {
        "choice_join_dash": choice_lastwords_join(),
        "lw_arch_tail40": lw40,
        "checker_half45": CHECKER[:45].lower(),
        "8446_head8": message_8446_text()[:8],
        "flower_hash": FLOWER_HASH,
    }
    for name, val in word_lastwords_candidates():
        out[f"wlw-{name}"] = val
    return out


def step0_passwords(msl: str) -> list[tuple[str, str]]:
    s0 = tok23()
    return [
        ("sha256hex-s0||msl", hashlib.sha256((s0 + msl).encode()).hexdigest()),
        ("concat-s0||msl", s0 + msl),
        ("sha256hex-msl", hashlib.sha256(msl.encode()).hexdigest()),
        ("msl-only", msl),
        ("sha256hex-s0", hashlib.sha256(s0.encode()).hexdigest()),
        ("tok23-only", s0),
    ]


def h1_step2_answer(pt: bytes, lw: str, form: str) -> list[tuple[str, str]]:
    text = pt.decode("latin-1", errors="replace")
    if form == "sha256hex(plaintext||lw)":
        return [
            ("h1-s2-sha-pt||lw", hashlib.sha256((text + lw).encode()).hexdigest()),
            ("h1-s2-concat", text + lw),
            ("h1-s2-sha-lw||pt", hashlib.sha256((lw + text).encode()).hexdigest()),
        ]
    return []


def h1_step3_answer(step2_ans: str, suffix: str) -> list[tuple[str, str]]:
    return [
        ("h1-s3-sha-s2||yin", hashlib.sha256((step2_ans + suffix).encode()).hexdigest()),
        ("h1-s3-concat", step2_ans + suffix),
    ]


def derivations_from_pt(pt: bytes, lw: str) -> list[tuple[str, str]]:
    if pt is None:
        return []
    text = pt.decode("latin-1", errors="replace")
    tok_b = tok23().encode()
    lw_b = ARCH[ARCH.find("SELECT") - 40 : ARCH.find("SELECT")].lower().encode()
    checker_b = CHECKER.encode()
    out: list[tuple[str, str]] = [
        ("latin1_full", text),
        ("sha256hex_latin1", hashlib.sha256(text.encode()).hexdigest()),
        ("latin1_prefix64", text[:64]),
        ("body_hex", pt.hex()),
        ("sha256hex_body", hashlib.sha256(pt).hexdigest()),
        ("sha256hex_pt_concat_lw", hashlib.sha256((text + lw).encode()).hexdigest()),
        ("concat_pt_lw", text + lw),
        ("sha256hex_pt_concat_yinyang", hashlib.sha256((text + "yinyang").encode()).hexdigest()),
        ("xor_checker_hex", xor_bytes(pt, checker_b).hex()),
        ("xor_tok23_sha", hashlib.sha256(xor_bytes(pt, tok_b)).hexdigest()),
        ("xor_lw_tail40_sha", hashlib.sha256(xor_bytes(pt, lw_b)).hexdigest()),
    ]
    return out


def raw_decrypt_body(raw: bytes, answer: str, profile: str) -> bytes | None:
    """AES decrypt without requiring PKCS#7 (for liberal enter-chain reads)."""
    if profile == "std-hex-sha256":
        body, _ = decrypt_salted(raw, answer)
        return body
    if profile == "plain-md5":
        body, _ = decrypt_with_profile(raw, answer, profile)
        return body
    if profile == "raw32-sha256":
        body, _ = decrypt_salted(raw, answer, raw_digest=True)
        return body
    return None


def aes_full_blocks(raw: bytes, answer: str, profile: str = "std-hex-sha256") -> bytes:
    if raw[:8] != b"Salted__":
        return b""
    salt, ct = raw[8:16], raw[16:]
    digest = hashlib.sha256(answer.encode()).digest()
    pw = digest.hex().encode()
    if profile == "plain-md5":
        key, iv = evp_bytes_to_key(answer.encode(), salt, md=hashlib.md5)
    elif profile == "raw32-sha256":
        key, iv = evp_bytes_to_key(digest, salt, md=hashlib.sha256)
    else:
        key, iv = evp_bytes_to_key(pw, salt, md=hashlib.sha256)
    return AES.new(key, AES.MODE_CBC, iv).decrypt(ct)


def try_decrypt(
    raw: bytes,
    answer: str,
    profile: str,
    tag: str,
    require_pad: bool = False,
) -> tuple[bytes | None, str]:
    if not answer or len(answer) > 12000:
        return None, "skip"
    if not inc():
        return None, "budget"
    try:
        body, kind = decrypt_with_profile(raw, answer, profile)
    except Exception:
        return None, "error"
    if kind == "structured":
        summary["hits"].append(
            {"tag": tag, "profile": profile, "answer_head": answer[:80], "kind": kind}
        )
    if require_pad and body is None:
        return None, kind
    d = hashlib.sha256(answer.encode()).digest()
    if is_win_uncompressed(d):
        summary["hits"].append({"tag": tag, "win": "answer_sha256"})
    return body, kind


def run_h1_fixed_chain() -> int:
    """Strategist H1: tok23+msl -> Sal -> pt||lw -> Terminal -> +yinyang -> Cosmic."""
    containers = load_containers()
    msls = {k: msl_catalog()[k] for k in SPEC["h1_8446_pipeline"]["msl"]}
    lws = lw_catalog()
    lw_keys = SPEC["h1_8446_pipeline"]["lastwords"]
    sal_kdfs = SPEC["h1_8446_pipeline"]["sal_kdf"]
    n = 0
    for mname, mval in msls.items():
        for lkey in lw_keys:
            if lkey == "word_lastwords_candidates":
                lw_items = [(k, v) for k, v in lw_catalog().items() if k.startswith("wlw-")]
            elif lkey == "choice_join_dash":
                lw_items = [("choice_join_dash", choice_lastwords_join())]
            elif lkey == "lw_arch_tail40":
                lw_items = [("lw_arch_tail40", lw_catalog()["lw_arch_tail40"])]
            elif lkey == "checker_half45":
                lw_items = [("checker_half45", lw_catalog()["checker_half45"])]
            else:
                continue
            for lwname, lwval in lw_items:
                for s0name, s0ans in step0_passwords(mval):
                    for skdf in sal_kdfs:
                        body1, _ = try_decrypt(
                            containers["salphaseion_short"],
                            s0ans,
                            skdf,
                            f"h1-sal-{mname}-{s0name}-{skdf}",
                        )
                        n += 0
                        if body1 is None:
                            continue
                        for s2name, s2ans in h1_step2_answer(
                            body1, lwval, SPEC["h1_8446_pipeline"]["step2_form"]
                        ):
                            body2, _ = try_decrypt(
                                containers["terminal"],
                                s2ans,
                                "std-hex-sha256",
                                f"h1-term-{mname}-{lwname}-{s2name}",
                            )
                            if body2 is None:
                                continue
                            for s3name, s3ans in h1_step3_answer(
                                s2ans, SPEC["h1_8446_pipeline"]["step3_suffix"]
                            ):
                                for cprof in ("std-hex-sha256", "raw32-sha256"):
                                    try_decrypt(
                                        containers["cosmic"],
                                        s3ans,
                                        cprof,
                                        f"h1-cosmic-{mname}-{lwname}-{s3name}-{cprof}",
                                    )
    return n


def run_generic_chain(
    family: str,
    order: list[str],
    initial_answers: list[tuple[str, str]],
    lw: str,
    step_profiles: list[str],
) -> int:
    """Three-step chain: initial -> deriv -> deriv on third container."""
    containers = load_containers()
    for iname, ians in initial_answers:
        if not inc(0):
            break
        prof0 = step_profiles[0] if step_profiles else "std-hex-sha256"
        body0, _ = try_decrypt(
            containers[order[0]], ians, prof0, f"{family}-s0-{iname}-{order[0]}"
        )
        if body0 is None:
            continue
        for d1n, ans1 in derivations_from_pt(body0, lw):
            prof1 = step_profiles[1] if len(step_profiles) > 1 else "std-hex-sha256"
            body1, _ = try_decrypt(
                containers[order[1]], ans1, prof1, f"{family}-s1-{d1n}-{order[1]}"
            )
            if body1 is None:
                continue
            for d2n, ans2 in derivations_from_pt(body1, lw):
                prof2 = step_profiles[2] if len(step_profiles) > 2 else "std-hex-sha256"
                try_decrypt(
                    containers[order[2]], ans2, prof2, f"{family}-s2-{d2n}-{order[2]}"
                )
    return 0


def run_m3_and_orders() -> int:
    msls = msl_catalog()
    m3_msl = [msls[k] for k in SPEC["m3_enter_pipeline"]["msl_family"] if k in msls]
    lw_map = lw_catalog()
    m3_lw = [lw_map[k] for k in SPEC["m3_enter_pipeline"]["lastwords"] if k in lw_map]
    orders = SPEC["container_orders"]
    for order in orders:
        if summary["stopped_early"]:
            break
        tag = "m3" if order == SPEC["m3_enter_pipeline"]["default_order"] else f"order-{''.join(c[0] for c in order)}"
        for msl in m3_msl:
            for lw in m3_lw:
                initials = step0_passwords(msl) + [
                    ("sha256hex-msl-only", hashlib.sha256(msl.encode()).hexdigest()),
                    ("recipe", f"{msl}enter{lw}thispassword{msl}"),
                ]
                profiles = ["std-hex-sha256", "std-hex-sha256", "std-hex-sha256"]
                if order[0] == "salphaseion_short":
                    profiles[0] = "plain-md5"  # Sal-short MD5 on first step only
                if order[2] == "cosmic":
                    profiles[2] = "raw32-sha256"
                elif order[1] == "cosmic":
                    profiles[1] = "raw32-sha256"
                elif order[0] == "cosmic":
                    profiles[0] = "raw32-sha256"
                run_generic_chain(tag, order, initials, lw, profiles)
    return 0


def run_reader_narrative_chain() -> int:
    order = SPEC["reader_inter_container"]["narrative_order"]
    c0: list[tuple[str, str]] = []
    sel = ARCH.find("SELECT")
    for key in SPEC["reader_inter_container"]["c0_sources"]:
        if key == "checker_decode":
            c0.append(("checker", CHECKER))
            c0.append(("checker-sha", hashlib.sha256(CHECKER.encode()).hexdigest()))
        elif key == "tok23":
            c0.append(("tok23", tok23()))
            c0.append(("tok23-sha", hashlib.sha256(tok23().encode()).hexdigest()))
        elif key == "sha256hex_flower":
            c0.append(("flower-h", FLOWER_HASH))
        elif key == "phase32_after_select_64":
            c0.append(("after-sel", ARCH[sel + 6 : sel + 6 + 64].lower()))
    lw = CHECKER[:45].lower()
    run_generic_chain("reader-TSC", order, c0, lw, ["std-hex-sha256"] * 3)
    # Hash-chain on narrative order (does not require pad-valid step 0)
    msl = msl_catalog()["checker149_sum"]
    for iname, ians in c0:
        chain = [
            ians,
            hashlib.sha256((ians + msl).encode()).hexdigest(),
            hashlib.sha256((hashlib.sha256((ians + msl).encode()).hexdigest() + lw).encode()).hexdigest(),
        ]
        blobs = load_containers()
        for idx, (cname, ans) in enumerate(zip(order, chain)):
            prof = "raw32-sha256" if cname == "cosmic" else "std-hex-sha256"
            try_decrypt(blobs[cname], ans, prof, f"reader-TSC-hash-{iname}-{idx}")
    return 0


def run_yinyang_mid_chain() -> int:
    spec = SPEC["yinyang_mid_chain"]
    containers = load_containers()
    sal = containers["salphaseion_short"]
    cosmic = containers["cosmic"]
    initials = [
        ("tok23", tok23()),
        ("checker", CHECKER),
        ("msl-sum", str(sum(int(c) for c in DIGITS149))),
    ] + step0_passwords(msl_catalog()["list_row_sums_dash"])[:3]
    lw = lw_catalog()["checker_half45"]
    for iname, ians in initials:
        for skdf in ("std-hex-sha256", "plain-md5"):
            body, _ = try_decrypt(sal, ians, skdf, f"yin-mid-sal-{iname}")
            if body is None:
                continue
            for yname in spec["targets"]:
                raw = containers.get(yname)
                if raw is None or raw[:8] != b"Salted__":
                    continue
                for dname, dans in derivations_from_pt(body, lw):
                    try_decrypt(raw, dans, "std-hex-sha256", f"yin-mid-{yname}-{dname}")
                    try_decrypt(raw, dans, "plain-md5", f"yin-mid-md5-{yname}-{dname}")
            for dname, dans in derivations_from_pt(body, lw):
                try_decrypt(cosmic, dans, "std-hex-sha256", f"yin-mid-cosmic-{dname}")
                try_decrypt(cosmic, dans, "raw32-sha256", f"yin-mid-cosmic-r32-{dname}")
    return 0


def run_m3_baselines() -> int:
    """Single-step null baselines: sha256hex(msl enter lw) on each container."""
    containers = load_containers()
    msls = [msl_catalog()[k] for k in SPEC["m3_enter_pipeline"]["msl_family"] if k in msl_catalog()]
    lws = [lw_catalog()[k] for k in SPEC["m3_enter_pipeline"]["lastwords"] if k in lw_catalog()]
    for msl in msls:
        for lw in lws:
            ans = f"{msl}enter{lw}thispassword{msl}"
            for cname in ("terminal", "salphaseion_short", "cosmic"):
                try_decrypt(containers[cname], ans, "std-hex-sha256", f"m3-base-{cname}")
    return 0


def run_brainstorm_checker_lw_chain() -> int:
    """Step 4: pipeline with checker HALF lw only (M3 order + H1 order)."""
    lw = CHECKER[:45].lower()
    msl = str(sum(int(c) for c in DIGITS149))
    initials = step0_passwords(msl) + [("decode", CHECKER)]
    for order in (
        ["salphaseion_short", "cosmic", "terminal"],
        ["salphaseion_short", "terminal", "cosmic"],
    ):
        run_generic_chain("chk-lw", order, initials, lw, ["std-hex-sha256", "plain-md5", "std-hex-sha256"])
    return 0


def run_hash_chain_no_plaintext() -> int:
    """Operands hash-chained as passwords (no dependency on decrypt success)."""
    containers = load_containers()
    orders = SPEC["container_orders"]
    msl_keys = SPEC["h1_8446_pipeline"]["msl"] + SPEC["m3_enter_pipeline"]["msl_family"][:6]
    msl_map = msl_catalog()
    lw_vals = list({lw_catalog()[k] for k in SPEC["m3_enter_pipeline"]["lastwords"] if k in lw_catalog()})
    s0 = tok23()
    yin = SPEC["h1_8446_pipeline"]["step3_suffix"]
    for order in orders:
        for mkey in msl_keys:
            if mkey not in msl_map:
                continue
            msl = msl_map[mkey]
            for lw in lw_vals:
                chain = [
                    ("sha256hex(s0||msl)", hashlib.sha256((s0 + msl).encode()).hexdigest()),
                    (
                        "sha256hex(p1||lw)",
                        hashlib.sha256(
                            (hashlib.sha256((s0 + msl).encode()).hexdigest() + lw).encode()
                        ).hexdigest(),
                    ),
                    (
                        "sha256hex(p2||yin)",
                        hashlib.sha256(
                            (
                                hashlib.sha256(
                                    (
                                        hashlib.sha256((s0 + msl).encode()).hexdigest() + lw
                                    ).encode()
                                ).hexdigest()
                                + yin
                            ).encode()
                        ).hexdigest(),
                    ),
                ]
                for prof in ("std-hex-sha256", "plain-md5"):
                    for (cname, (_, ans)) in zip(order, chain):
                        try_decrypt(
                            containers[cname],
                            ans,
                            prof if cname == "salphaseion_short" else "std-hex-sha256",
                            f"hash-chain-{mkey}-{cname}-{prof}",
                        )
                # same chain answers on every container (mis-order stress)
                for ans_label, ans in chain:
                    for cname in order:
                        try_decrypt(
                            containers[cname],
                            ans,
                            "std-hex-sha256",
                            f"hash-chain-all-{mkey}-{ans_label}-{cname}",
                        )
    return 0


def run_liberal_enter_chains() -> int:
    """Derive next password from raw CBC blocks when PKCS#7 fails."""
    containers = load_containers()
    order = SPEC["m3_enter_pipeline"]["default_order"]
    lw = lw_catalog()["checker_half45"]
    for mname, mval in list(msl_catalog().items())[:10]:
        for s0name, s0ans in step0_passwords(mval):
            for skdf in ("std-hex-sha256", "plain-md5"):
                raw_pt = aes_full_blocks(containers[order[0]], s0ans, skdf)
                for d1n, ans1 in derivations_from_pt(raw_pt, lw):
                    for prof in ("std-hex-sha256", "raw32-sha256"):
                        raw_pt2 = aes_full_blocks(containers[order[1]], ans1, prof)
                        for d2n, ans2 in derivations_from_pt(raw_pt2, lw):
                            try_decrypt(
                                containers[order[2]],
                                ans2,
                                "std-hex-sha256",
                                f"liberal-{mname}-{s0name}-{d1n}-{d2n}",
                            )
    return 0


def run_cosmic_kdf_probe_chain() -> int:
    """Strategist step 4: non-§4.1 cosmic after hash-chain step2."""
    from round4_battery import decrypt_mdp5_bytes

    containers = load_containers()
    cosmic = containers["cosmic"]
    msl = msl_catalog()["list_row_sums_dash"]
    lw = lw_catalog()["lw_arch_tail40"]
    p1 = hashlib.sha256((tok23() + msl).encode()).hexdigest()
    p2 = hashlib.sha256((p1 + lw).encode()).hexdigest()
    p2_double = hashlib.sha256(p2.encode()).hexdigest()
    probes: list[tuple[str, str, str]] = [
        ("std-hex", p2, "std-hex-sha256"),
        ("raw32", p2, "raw32-sha256"),
        ("double-hex", p2_double, "std-hex-sha256"),
    ]
    for tag, ans, prof in probes:
        if prof == "raw32-sha256":
            if not inc():
                break
            body, _ = decrypt_salted(cosmic, ans, raw_digest=True)
        else:
            body, kind = try_decrypt(cosmic, ans, prof, f"cosmic-kdf-{tag}")
            body = body if kind != "budget" else None
        if body and classify_plaintext(body) == "structured":
            summary["hits"].append({"tag": f"cosmic-kdf-{tag}", "kind": "structured"})
    md5_pws = [
        ("md5-plain", p2.encode()),
        ("md5-sha256hex-ascii", hashlib.sha256(p2.encode()).hexdigest().encode()),
        ("md5-raw32", hashlib.sha256(p2.encode()).digest()),
    ]
    for tag, pw in md5_pws:
        if not inc():
            break
        body, _ = decrypt_mdp5_bytes(cosmic, pw)
        if body and classify_plaintext(body) == "structured":
            summary["hits"].append({"tag": f"cosmic-kdf-{tag}", "kind": "structured"})
    return 0


def run_enter_xor_chain() -> int:
    """Chain: decrypt sal with msl -> XOR(enter) with operand -> next container."""
    containers = load_containers()
    order = ["salphaseion_short", "terminal", "cosmic"]
    ab = SAL_PAGE[91:195].replace("a", "0").replace("b", "1")
    ab_bytes = bytes(int(ab[i : i + 8], 2) for i in range(0, len(ab) - len(ab) % 8, 8))
    operands = {
        "tok23": tok23().encode(),
        "lw40": ARCH[ARCH.find("SELECT") - 40 : ARCH.find("SELECT")].lower().encode(),
        "checker": CHECKER.encode(),
        "ab": ab_bytes,
    }
    for mname, mval in list(msl_catalog().items())[:8]:
        body, _ = try_decrypt(
            containers["salphaseion_short"],
            hashlib.sha256((tok23() + mval).encode()).hexdigest(),
            "std-hex-sha256",
            f"xor-chain-s0-{mname}",
        )
        if body is None:
            continue
        for oname, ob in operands.items():
            x = xor_bytes(body, ob)
            for ans in (x.hex(), hashlib.sha256(x).hexdigest()):
                body2, _ = try_decrypt(
                    containers["terminal"], ans, "std-hex-sha256", f"xor-chain-t-{oname}"
                )
                if body2 is None:
                    continue
                x2 = xor_bytes(body2, ob)
                for ans2 in (x2.hex(), hashlib.sha256(x2).hexdigest()):
                    try_decrypt(containers["cosmic"], ans2, "std-hex-sha256", f"xor-chain-c-{oname}")
    return 0


def main() -> int:
    results.clear()
    planted_control()
    before = summary["decrypts"]
    run_h1_fixed_chain()
    summary["families"]["h1_8446"] = summary["decrypts"] - before
    before = summary["decrypts"]
    run_m3_baselines()
    summary["families"]["m3_baselines"] = summary["decrypts"] - before
    before = summary["decrypts"]
    run_m3_and_orders()
    summary["families"]["m3_orders"] = summary["decrypts"] - before
    before = summary["decrypts"]
    run_reader_narrative_chain()
    summary["families"]["reader_TSC"] = summary["decrypts"] - before
    before = summary["decrypts"]
    run_yinyang_mid_chain()
    summary["families"]["yinyang_mid"] = summary["decrypts"] - before
    before = summary["decrypts"]
    run_brainstorm_checker_lw_chain()
    summary["families"]["checker_lw"] = summary["decrypts"] - before
    before = summary["decrypts"]
    run_enter_xor_chain()
    summary["families"]["xor_enter_chain"] = summary["decrypts"] - before
    before = summary["decrypts"]
    run_hash_chain_no_plaintext()
    summary["families"]["hash_chain_no_pt"] = summary["decrypts"] - before
    before = summary["decrypts"]
    run_liberal_enter_chains()
    summary["families"]["liberal_enter"] = summary["decrypts"] - before
    before = summary["decrypts"]
    run_cosmic_kdf_probe_chain()
    summary["families"]["cosmic_kdf_probe"] = summary["decrypts"] - before

    summary["structured_hits"] = len(summary["hits"])
    out = ART / "round7_chained_pipeline.json"
    out.write_text(json.dumps(summary, indent=2) + "\n")
    record(
        "round7 within budget",
        summary["decrypts"] <= BUDGET,
        f"{summary['decrypts']}/{BUDGET}",
    )
    print(
        f"round7: decrypts={summary['decrypts']} structured={summary['structured_hits']} "
        f"stopped_early={summary['stopped_early']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
