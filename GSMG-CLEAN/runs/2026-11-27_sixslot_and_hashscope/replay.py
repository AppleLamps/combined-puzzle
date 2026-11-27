#!/usr/bin/env python3
"""Two Cosmic Duality / SalPhaseIon / Terminal replays under the pinned gsmg
SHA-256 EVP_BytesToKey AES-256-CBC PKCS#7 profile:

  PART 1: Resolved values inside the frozen six-slot string
          (matrixsumlist | lastwordsbeforearchichoice | thispassword |
           shabefourfirsthintisyourlastcommand | enter | shabefanstoo)
          - (a) A_core (58 salphaseion_roles + 10 explicit 563/497 forms) x 55 B, sep in ("", "z")
          - (b) A_core + 9,236 #8446 forms in slot 1 with slot 2 literal, sep in ("", "z")
          - (c) slot 1 literal with each of 55 B in slot 2, sep in ("", "z")
          Slots 3-6 literal throughout; no yinyang appended anywhere.

  PART 2: gsmg-haiku hash_scope.py 876-partition replay
          All 21,024 passphrases (876 partitions x 2 orders x 2 inner forms x 2 joins
          = 7,008 unique bodies C x 3 outer arms: as-password, outer-sha256-hex [gsmg],
          outer-sha256-raw), including the 252 contiguous outer-sha256-hex passphrases.

Usage:
  python replay.py build   # build candidate lists, write PREREG.json and PREREG.sealed (0 decrypts)
  python replay.py run     # verify seal, run controls, decrypt all 3 envelopes, retain & scan, write REPORT.md
"""

from __future__ import annotations

import ast
import base64
import hashlib
import json
import math
import random
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Crypto.Cipher import AES
import coincurve

HERE = Path(__file__).resolve().parent
GSMG_CLEAN = HERE.parents[1]
REPO_ROOT = GSMG_CLEAN.parent

sys.path.insert(0, str(GSMG_CLEAN / "tools"))
sys.path.insert(0, str(GSMG_CLEAN / "runs" / "2026-11-27_cosmic_binary_scan"))
sys.path.insert(0, str(REPO_ROOT / "gsmg-haiku" / "review_leads"))

import check_candidate as cc  # noqa: E402
import scan as binscan  # noqa: E402
import hash_scope as haiku_hs  # noqa: E402
import next_tests as haiku_nt  # noqa: E402

SLOTS_LITERAL = (
    "matrixsumlist",
    "lastwordsbeforearchichoice",
    "thispassword",
    "shabefourfirsthintisyourlastcommand",
    "enter",
    "shabefanstoo",
)

SOURCES = {
    "salphaseion_roles_manifest": "GSMG-CLEAN/runs/2026-09-13_salphaseion_roles/manifest.json",
    "matrixsum_forms": "GSMG-CLEAN/runs/2026-11-27_matrixsum_replay/forms.txt",
    "lastwords_py": "5g-puzzle/analysis/lastwords.py",
    "phase3_2_plaintext": "GSMG-CLEAN/data/phase3_2_plaintext.bin",
    "hash_scope_py": "gsmg-haiku/review_leads/hash_scope.py",
    "next_tests_py": "gsmg-haiku/review_leads/next_tests.py",
    "hash_scope_results": "gsmg-haiku/review_leads/hash_scope/results.json",
}

DIGIT_TRANS = str.maketrans("1234567890", "abcdefghio")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digit_letters(s: str) -> str:
    return s.translate(DIGIT_TRANS)


def poisson_p_ge(k: int, lam: float) -> float:
    """Exact Poisson upper tail P(X >= k) for X ~ Poisson(lam)."""
    if k <= 0:
        return 1.0
    if lam <= 0.0:
        return 0.0
    # Compute lower tail sum_{j=0}^{k-1} e^{-lam} * lam^j / j!
    term = math.exp(-lam)
    cdf = term
    for j in range(1, k):
        term *= lam / j
        cdf += term
    return max(0.0, min(1.0, 1.0 - cdf))


# ---------------------------------------------------------------------------
# Fast exact AES-256-CBC (EVP_BytesToKey SHA-256, 1 iter) + fast coincurve keys
# ---------------------------------------------------------------------------
def try_envelope_pw_fast(env_raw: bytes, pw_bytes: bytes) -> tuple[int, bytes | None]:
    """Exact EVP_BytesToKey(SHA-256, 1 iter) AES-256-CBC PKCS#7 decrypt.
    Uses the CBC last-block identity P_N = D_K(C_N) ^ C_{N-1} for N >= 2 blocks,
    computing IV and decrypting full ciphertext only when PKCS#7 padding is valid."""
    salt = env_raw[8:16]
    ct = env_raw[16:]
    key = hashlib.sha256(pw_bytes + salt).digest()
    if len(ct) >= 32:
        last_plain = AES.new(key, AES.MODE_CBC, ct[-32:-16]).decrypt(ct[-16:])
        pad = last_plain[-1]
        if not (1 <= pad <= 16 and last_plain[-pad:] == bytes([pad]) * pad):
            return 0, None
    iv = hashlib.sha256(key + pw_bytes + salt).digest()[:16]
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    pad = pt[-1]
    if 1 <= pad <= 16 and pt[-pad:] == bytes([pad]) * pad:
        return pad, pt[:-pad]
    return 0, None


def fast_scalar_hits(k: int) -> list[str]:
    if not (1 <= k < cc.N):
        return []
    pk = coincurve.PrivateKey(k.to_bytes(32, "big")).public_key
    forms = {
        "uncompressed": pk.format(compressed=False),
        "compressed": pk.format(compressed=True),
    }
    return [f"{cc.TARGETS[cc.h160(pub)]} ({form})" for form, pub in forms.items() if cc.h160(pub) in cc.TARGETS]


def encrypt_salted_pw(plaintext: bytes, pw_bytes: bytes, salt: bytes) -> bytes:
    """Encrypt plaintext into OpenSSL Salted__ format under EVP_BytesToKey(SHA-256, 1 iter)."""
    assert len(salt) == 8
    key, iv = cc.evp(pw_bytes, salt, hashlib.sha256)
    pad = 16 - (len(plaintext) % 16)
    padded = plaintext + bytes([pad]) * pad
    ct = AES.new(key, AES.MODE_CBC, iv).encrypt(padded)
    return b"Salted__" + salt + ct


# ---------------------------------------------------------------------------
# Candidate generators (zero decrypts)
# ---------------------------------------------------------------------------
def build_part1_sets() -> dict[str, Any]:
    sr = json.loads((REPO_ROOT / SOURCES["salphaseion_roles_manifest"]).read_text(encoding="utf-8"))
    a_roles = sorted(set(sr["A_components"].values()))
    b_roles = sorted(set(sr["B_components"].values()))

    # Explicit 563/497 forms (matching salphaseion_roles' L1_yellow_blue_totals serializations)
    a_563_497_named = {
        "563_497/joined": "563497",
        "563_497/commas": "563,497",
        "563_497/spaces": "563 497",
        "563_497/page_digits": digit_letters("563497"),
        "497_563/joined": "497563",
        "497_563/commas": "497,563",
        "497_563/spaces": "497 563",
        "497_563/page_digits": digit_letters("497563"),
        "563/solo": "563",
        "497/solo": "497",
    }
    a_563_497 = sorted(set(a_563_497_named.values()))
    a_core = sorted(set(a_roles) | set(a_563_497))

    a_pipeline = sorted(set((REPO_ROOT / SOURCES["matrixsum_forms"]).read_text(encoding="utf-8").splitlines()))
    assert len(a_pipeline) == 9236, f"Expected 9236 #8446 forms, got {len(a_pipeline)}"

    # Build 8-base lastwords_preamble_replay B set (PRE, DIG, RID and joins, no RID+PRE, no yinyang)
    legacy = REPO_ROOT / SOURCES["lastwords_py"]
    src_ast = ast.parse(legacy.read_bytes())
    vals = {
        node.targets[0].id: ast.literal_eval(node.value)
        for node in src_ast.body
        if isinstance(node, ast.Assign)
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id in {"S", "PRE", "DIG"}
    }
    (form_node,) = [n for n in src_ast.body if isinstance(n, ast.FunctionDef) and n.name == "forms"]
    scope: dict[str, Any] = {"re": re}
    exec(compile(ast.Module(body=[form_node], type_ignores=[]), str(legacy), "exec"), scope)

    # Verify exact byte offsets in phase3_2_plaintext.bin
    phase_bytes = (REPO_ROOT / SOURCES["phase3_2_plaintext"]).read_bytes()
    offsets = {}
    for label, key in (("PRE", "PRE"), ("DIG", "DIG"), ("RID", "S")):
        pat = vals[key].encode("ascii")
        assert phase_bytes.count(pat) == 1
        start = phase_bytes.index(pat)
        stop = start + len(pat)
        offsets[label] = {"start": start, "stop": stop}
    assert offsets == {
        "PRE": {"start": 336, "stop": 443},
        "DIG": {"start": 1990, "stop": 2139},
        "RID": {"start": 2143, "stop": 2288},
    }, f"Unexpected offsets: {offsets}"

    lm = {"PRE": vals["PRE"], "DIG": vals["DIG"], "RID": vals["S"]}
    eight_bases = ("PRE", "DIG", "RID", "PRE+DIG", "DIG+PRE", "PRE+RID", "DIG+RID", "RID+DIG")
    b_lw = sorted({f for base in eight_bases for f in scope["forms"]("".join(lm[p] for p in base.split("+")))})
    b_all = sorted(set(b_roles) | set(b_lw))
    assert len(b_all) == 55, f"Expected |B| == 55, got {len(b_all)}"

    tail4 = SLOTS_LITERAL[2:]
    cand_prov: dict[str, list[str]] = {}

    def add(s: str, tag: str) -> None:
        assert "\n" not in s and "\r" not in s, f"Linebreak in candidate: {s!r}"
        assert "yinyang" not in s.lower(), f"Unexpected yinyang in candidate: {s!r}"
        cand_prov.setdefault(s, []).append(tag)

    # (a) A_core x B_all, both separators
    for a in a_core:
        for b in b_all:
            for sep_name, sep in (("none", ""), ("z", "z")):
                add(sep.join((a, b, *tail4)), f"1a_cross/sep={sep_name}")

    # (b) A_core U A_pipeline in slot 1 with slot 2 literal, both separators
    a_all_slot1 = sorted(set(a_core) | set(a_pipeline))
    for a in a_all_slot1:
        src_tag = "1b_core_a_only" if a in set(a_core) else "1b_pipeline_a_only"
        for sep_name, sep in (("none", ""), ("z", "z")):
            add(sep.join((a, SLOTS_LITERAL[1], *tail4)), f"{src_tag}/sep={sep_name}")

    # (c) slot 1 literal with each B in slot 2, both separators
    for b in b_all:
        for sep_name, sep in (("none", ""), ("z", "z")):
            add(sep.join((SLOTS_LITERAL[0], b, *tail4)), f"1c_b_only/sep={sep_name}")

    ordered_cands = sorted(cand_prov.keys())
    return {
        "a_roles_count": len(a_roles),
        "a_563_497_named": a_563_497_named,
        "a_core_count": len(a_core),
        "a_pipeline_count": len(a_pipeline),
        "a_all_slot1_count": len(a_all_slot1),
        "b_roles_count": len(b_roles),
        "b_lw_8base_count": len(b_lw),
        "b_total_count": len(b_all),
        "offsets": offsets,
        "candidates": ordered_cands,
        "provenance": cand_prov,
    }


def build_part2_passphrases() -> dict[str, Any]:
    """Regenerate all 21,024 passphrases from gsmg-haiku/review_leads/hash_scope.py:group_hashes()
    and verify exact agreement with HASH_SCOPE_REPORT.md (20,772 after skipping 252 contiguous)."""
    gh = list(haiku_hs.group_hashes())
    assert len(gh) == 21024, f"Expected 21024 generated passphrases, got {len(gh)}"

    # Confirm uniqueness of all 21,024 passphrases
    seen_fp: dict[bytes, tuple[str, bytes]] = {}
    items: list[dict[str, Any]] = []
    arm_counts: Counter[str] = Counter()
    for label, pw in gh:
        fp = hashlib.sha256(pw).digest()
        assert fp not in seen_fp, f"Duplicate passphrase in group_hashes: {label} vs {seen_fp[fp][0]}"
        seen_fp[fp] = (label, pw)
        arm = label.rsplit("/", 1)[-1]
        arm_counts[arm] += 1
        items.append({"label": label, "arm": arm, "pw": pw, "pw_hex": pw.hex()})

    # Cross-check against next_tests.py:partitions() and HASH_SCOPE_REPORT.md
    prev_fps = {haiku_hs.sha(haiku_hs.sha(body).hex().encode()) for _, body in haiku_nt.partitions()}
    assert len(prev_fps) == 252
    overlap = len(set(seen_fp.keys()) & prev_fps)
    assert overlap == 252
    remaining = len(seen_fp) - overlap
    assert remaining == 20772
    hs_res = json.loads((REPO_ROOT / SOURCES["hash_scope_results"]).read_text(encoding="utf-8"))
    gp = hs_res["families"]["group-partitions"]
    assert gp["generated"] == 21024 and gp["unique_passwords"] == 20772 and gp["aes_trials"] == 62316

    return {
        "generated_count": len(items),
        "arm_counts": dict(sorted(arm_counts.items())),
        "contiguous_overlap_count": overlap,
        "hash_scope_report_unique_after_skip": remaining,
        "hash_scope_report_aes_trials_verified": remaining * 3,
        "items": items,
    }


def build_and_seal() -> int:
    if (HERE / "PREREG.sealed").exists():
        raise SystemExit("PREREG.sealed already exists; remove or use a fresh directory before rebuilding.")

    p1 = build_part1_sets()
    p2 = build_part2_passphrases()

    # Write Part 1 candidate file (LF)
    p1_bytes = ("\n".join(p1["candidates"]) + "\n").encode("utf-8")
    p1_path = HERE / "part1_candidates.txt"
    p1_path.write_bytes(p1_bytes)
    p1_sha = sha256_hex(p1_bytes)

    # Write Part 2 canonical passphrase manifest (label \t pw_hex, LF)
    p2_lines = [f"{it['label']}\t{it['pw_hex']}" for it in p2["items"]]
    p2_bytes = ("\n".join(p2_lines) + "\n").encode("utf-8")
    p2_path = HERE / "part2_passphrases.tsv"
    p2_path.write_bytes(p2_bytes)
    p2_sha = sha256_hex(p2_bytes)

    # Build deterministic planted control fixtures (committed in PREREG before running)
    # Part 1 planted control: gsmg profile, candidate = six-slot control string
    p1_ctrl_answer = (
        "PLANTED_SIXSLOT_CONTROL_2026_11_27"
        "lastwordsbeforearchichoice"
        "thispassword"
        "shabefourfirsthintisyourlastcommand"
        "enter"
        "shabefanstoo"
    )
    p1_ctrl_pt = (
        b"%PDF-1.7\n"
        b"PLANTED PART1 CONTROL: "
        + (1).to_bytes(32, "big")
        + b" "
        + b"0" * 63 + b"1"
        + b" 5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf "
        + base64.b64encode((1).to_bytes(32, "big"))
        + b" END\n"
    )
    p1_ctrl_pw = hashlib.sha256(p1_ctrl_answer.encode("utf-8")).hexdigest().encode("ascii")
    p1_ctrl_env = encrypt_salted_pw(p1_ctrl_pt, p1_ctrl_pw, bytes.fromhex("1122334455667788"))

    # Part 2 planted controls: BOTH outer-sha256-raw (32B) and outer-sha256-hex (64B) arms
    p2_ctrl_body = b"PLANTED_HASHSCOPE_BODY_2026_11_27"
    p2_ctrl_pw_raw = hashlib.sha256(p2_ctrl_body).digest()
    p2_ctrl_pw_hex = hashlib.sha256(p2_ctrl_body).hexdigest().encode("ascii")
    p2_ctrl_pt_raw = (
        b"\x89PNG\r\n\x1a\n"
        + (1).to_bytes(32, "big")
        + b" "
        + b"0" * 63 + b"1"
        + b" 5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf "
        + base64.b64encode((1).to_bytes(32, "big"))
        + b" RAW_ARM"
    )
    p2_ctrl_pt_hex = (
        b"%PDF-1.7\n"
        + (1).to_bytes(32, "big")
        + b" "
        + b"0" * 63 + b"1"
        + b" 5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf "
        + base64.b64encode((1).to_bytes(32, "big"))
        + b" HEX_ARM"
    )
    p2_ctrl_env_raw = encrypt_salted_pw(p2_ctrl_pt_raw, p2_ctrl_pw_raw, bytes.fromhex("a1a2a3a4a5a6a7a8"))
    p2_ctrl_env_hex = encrypt_salted_pw(p2_ctrl_pt_hex, p2_ctrl_pw_hex, bytes.fromhex("b1b2b3b4b5b6b7b8"))

    prereg = {
        "schema": "sixslot_and_hashscope_prereg_v1",
        "sealed_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "profile": "gsmg (EVP_BytesToKey SHA-256 1 iter, AES-256-CBC, strict PKCS#7); Part 2 retains all 3 hash_scope outer arms (as-password, outer-sha256-hex, outer-sha256-raw)",
        "envelopes": {k: {"bytes": len(v), "salt": v[8:16].hex(), "sha256": sha256_hex(v)} for k, v in cc.ENVELOPES.items()},
        "real_target_hash160": dict(cc.TARGETS),
        "sources_sha256": {
            k: sha256_hex((REPO_ROOT / rel).read_bytes()) for k, rel in SOURCES.items()
        },
        "part1": {
            "frozen_slots": list(SLOTS_LITERAL),
            "separators": ["", "z"],
            "a_roles_count": p1["a_roles_count"],
            "a_563_497_forms": p1["a_563_497_named"],
            "a_core_count": p1["a_core_count"],
            "a_pipeline_count": p1["a_pipeline_count"],
            "a_all_slot1_count": p1["a_all_slot1_count"],
            "b_roles_count": p1["b_roles_count"],
            "b_lw_8base_count": p1["b_lw_8base_count"],
            "b_total_count": p1["b_total_count"],
            "phase3_2_offsets": p1["offsets"],
            "candidate_count": len(p1["candidates"]),
            "total_decrypts": len(p1["candidates"]) * len(cc.ENVELOPES),
            "candidates_file": "part1_candidates.txt",
            "candidates_sha256_lf": p1_sha,
        },
        "part2": {
            "generator": "gsmg-haiku/review_leads/hash_scope.py:group_hashes()",
            "partitions": 876,
            "outer_arms": p2["arm_counts"],
            "candidate_count": p2["generated_count"],
            "contiguous_overlap_count": p2["contiguous_overlap_count"],
            "hash_scope_report_unique_after_skip": p2["hash_scope_report_unique_after_skip"],
            "hash_scope_report_aes_trials_verified": p2["hash_scope_report_aes_trials_verified"],
            "total_decrypts": p2["generated_count"] * len(cc.ENVELOPES),
            "passphrases_file": "part2_passphrases.tsv",
            "passphrases_sha256_lf": p2_sha,
        },
        "combined_total_decrypts": (len(p1["candidates"]) + p2["generated_count"]) * len(cc.ENVELOPES),
        "controls": {
            "key_hash160_k1": "91b24bf9f5288532960ac687abb035127b1d28a5",
            "part1": {
                "answer": p1_ctrl_answer,
                "envelope_b64": base64.b64encode(p1_ctrl_env).decode("ascii"),
                "plaintext_sha256": sha256_hex(p1_ctrl_pt),
                "plaintext_len": len(p1_ctrl_pt),
                "expected_pad": 16 - (len(p1_ctrl_pt) % 16),
                "expected_find_keys_kinds": ["WIF", "base64", "hex64", "raw32"],
                "expected_binscan_flags": ["magic_pdf"],
            },
            "part2_raw": {
                "label": "planted_part2/outer-sha256-raw",
                "pw_hex": p2_ctrl_pw_raw.hex(),
                "envelope_b64": base64.b64encode(p2_ctrl_env_raw).decode("ascii"),
                "plaintext_sha256": sha256_hex(p2_ctrl_pt_raw),
                "plaintext_len": len(p2_ctrl_pt_raw),
                "expected_pad": 16 - (len(p2_ctrl_pt_raw) % 16),
                "expected_find_keys_kinds": ["WIF", "base64", "hex64", "raw32"],
                "expected_binscan_flags": ["magic_png"],
            },
            "part2_hex": {
                "label": "planted_part2/outer-sha256-hex",
                "pw_hex": p2_ctrl_pw_hex.hex(),
                "envelope_b64": base64.b64encode(p2_ctrl_env_hex).decode("ascii"),
                "plaintext_sha256": sha256_hex(p2_ctrl_pt_hex),
                "plaintext_len": len(p2_ctrl_pt_hex),
                "expected_pad": 16 - (len(p2_ctrl_pt_hex) % 16),
                "expected_find_keys_kinds": ["WIF", "base64", "hex64", "raw32"],
                "expected_binscan_flags": ["magic_pdf"],
            },
        },
        "pass_rules": {
            "retain_all_pad_valid": True,
            "find_keys_on_all_retained": True,
            "binary_scan_on_all_retained": True,
            "hit_definition": "any find_keys match to Half or Better Half, or authenticated non-random decrypt",
        },
    }

    prereg_bytes = (json.dumps(prereg, indent=2) + "\n").encode("utf-8")
    (HERE / "PREREG.json").write_bytes(prereg_bytes)
    seal = sha256_hex(prereg_bytes)
    (HERE / "PREREG.sealed").write_bytes((seal + "\n").encode("ascii"))

    print(f"PREREG sealed: {seal}")
    print(f"Part 1: |A_core|={p1['a_core_count']}, |A_pipeline|={p1['a_pipeline_count']}, |B|={p1['b_total_count']} -> {len(p1['candidates']):,} candidates ({len(p1['candidates'])*3:,} decrypts)")
    print(f"Part 2: {p2['generated_count']:,} passphrases ({p2['generated_count']*3:,} decrypts); verified 20,772 / 62,316 match HASH_SCOPE_REPORT.md")
    print(f"Combined decrypts: {prereg['combined_total_decrypts']:,}")
    return 0


# ---------------------------------------------------------------------------
# Execution & verification
# ---------------------------------------------------------------------------
def run_sweep(
    part_name: str,
    entries: list[tuple[str, bytes, dict[str, Any]]],
    envelopes: dict[str, bytes],
    out_root: Path,
) -> tuple[dict[str, dict[int, int]], list[dict[str, Any]]]:
    """Run AES-256-CBC decrypts for all (entry_id, pw_bytes, meta) x envelopes,
    retaining every pad-valid plaintext as .bin and running find_keys + binscan."""
    histograms: dict[str, Counter[int]] = {ename: Counter() for ename in envelopes}
    retained: list[dict[str, Any]] = []
    out_counters: Counter[str] = Counter()

    for idx, (entry_id, pw_bytes, meta) in enumerate(entries):
        for ename, env_raw in envelopes.items():
            pad, pt = try_envelope_pw_fast(env_raw, pw_bytes)
            histograms[ename][pad] += 1
            if not pad or pt is None:
                continue

            file_idx = out_counters[ename]
            out_counters[ename] += 1
            out_dir = out_root / ename
            out_dir.mkdir(parents=True, exist_ok=True)
            rel_file = f"{out_root.relative_to(HERE).as_posix()}/{ename}/{file_idx:04d}.bin"
            (HERE / rel_file).write_bytes(pt)

            raw_keys = cc.find_keys(pt)
            key_hits = {desc: hits for desc, hits in raw_keys if hits}
            bscan = binscan.scan_bytes(pt)

            rec = {
                "part": part_name,
                "envelope": ename,
                "candidate_index": idx,
                "file": rel_file,
                "pad": pad,
                "size": len(pt),
                "sha256": bscan["sha256"],
                "first_16_hex": bscan["first_16_hex"],
                "printable_fraction": bscan["printable_fraction"],
                "shannon_entropy": bscan["shannon_entropy"],
                "binary_scan_flags": bscan["active_flags"],
                "binary_scan_decompress": bscan["decompress"],
                "binary_scan_embedded_4plus": bscan["embedded_4plus_magics"],
                "find_keys_hits": key_hits,
                **meta,
            }
            retained.append(rec)

    hist_out = {ename: {int(k): int(v) for k, v in sorted(c.items())} for ename, c in histograms.items()}
    return hist_out, retained


def summarize_part(
    part_name: str,
    n_cands: int,
    histograms: dict[str, dict[int, int]],
    retained: list[dict[str, Any]],
    elapsed_sec: float,
) -> dict[str, Any]:
    per_env = {}
    for ename, h in histograms.items():
        n = sum(h.values())
        pad1 = h.get(1, 0)
        pad_ge2 = sum(v for k, v in h.items() if k >= 2)
        lam = n / 256.0
        per_env[ename] = {
            "decrypts": n,
            "pad_histogram": {str(k): v for k, v in h.items()},
            "pad1": pad1,
            "expected_n_over_256": round(lam, 4),
            "poisson_p_ge_pad1": round(poisson_p_ge(pad1, lam), 6),
            "pad_ge2": pad_ge2,
            "pad_valid_total": pad1 + pad_ge2,
        }
    total_dec = sum(v["decrypts"] for v in per_env.values())
    total_pad1 = sum(v["pad1"] for v in per_env.values())
    total_pad_ge2 = sum(v["pad_ge2"] for v in per_env.values())
    cosmic_sal_retained = [r for r in retained if r["envelope"] in ("cosmic_duality", "salphaseion_short")]
    return {
        "part": part_name,
        "candidates": n_cands,
        "decrypts": total_dec,
        "elapsed_sec": round(elapsed_sec, 2),
        "per_envelope": per_env,
        "pooled": {
            "decrypts": total_dec,
            "pad1": total_pad1,
            "expected_n_over_256": round(total_dec / 256.0, 4),
            "poisson_p_ge_pad1": round(poisson_p_ge(total_pad1, total_dec / 256.0), 6),
            "pad_ge2": total_pad_ge2,
            "pad_valid_total": len(retained),
        },
        "pad_ge2_records": [r for r in retained if r["pad"] >= 2],
        "printable_gt_0_8_records": [r for r in retained if r["printable_fraction"] > 0.8],
        "binary_scan_flagged_cosmic_or_salphaseion": [r for r in cosmic_sal_retained if r["binary_scan_flags"]],
        "binary_scan_flagged_all_envelopes": [r for r in retained if r["binary_scan_flags"]],
        "find_keys_hit_records": [r for r in retained if r["find_keys_hits"]],
    }


def run_all() -> int:
    # 1. Verify seal and preregistration BEFORE any decrypt
    seal_expected = (HERE / "PREREG.sealed").read_text(encoding="ascii").strip()
    prereg_bytes = (HERE / "PREREG.json").read_bytes()
    assert sha256_hex(prereg_bytes) == seal_expected, "PREREG.json hash mismatch vs PREREG.sealed!"
    plan = json.loads(prereg_bytes.decode("utf-8"))

    # Verify source hashes and candidate files match PREREG
    for k, rel in SOURCES.items():
        actual = sha256_hex((REPO_ROOT / rel).read_bytes())
        assert actual == plan["sources_sha256"][k], f"Source changed: {rel}"

    p1_bytes = (HERE / plan["part1"]["candidates_file"]).read_bytes()
    assert sha256_hex(p1_bytes) == plan["part1"]["candidates_sha256_lf"], "Part 1 candidates hash mismatch"
    p1_cands = p1_bytes.decode("utf-8").splitlines()
    assert len(p1_cands) == plan["part1"]["candidate_count"]

    p2_bytes = (HERE / plan["part2"]["passphrases_file"]).read_bytes()
    assert sha256_hex(p2_bytes) == plan["part2"]["passphrases_sha256_lf"], "Part 2 passphrases hash mismatch"
    p2_rows = [line.split("\t") for line in p2_bytes.decode("utf-8").splitlines()]
    assert len(p2_rows) == plan["part2"]["candidate_count"]

    for ename, info in plan["envelopes"].items():
        assert sha256_hex(cc.ENVELOPES[ename]) == info["sha256"], f"Envelope hash mismatch: {ename}"

    # 2. Harness self-tests + coincurve parity + fast-decrypt parity
    cc.selftest()
    bscan_st = binscan.selftest()
    assert bscan_st["passed"]

    # Verify fast_scalar_hits == cc.scalar_hits on k=1 + 16 random scalars
    orig_targets = cc.TARGETS.copy()
    orig_scalar_hits = cc.scalar_hits
    k1_h160 = plan["controls"]["key_hash160_k1"]
    cc.TARGETS[k1_h160] = "TEST k=1"
    rng = random.Random(20261127)
    for k in [1, 2, 3, cc.N - 1] + [rng.randrange(1, cc.N) for _ in range(16)]:
        assert fast_scalar_hits(k) == orig_scalar_hits(k), f"coincurve mismatch on k={k}"
    del cc.TARGETS[k1_h160]
    assert cc.TARGETS == orig_targets == plan["real_target_hash160"]
    cc.scalar_hits = fast_scalar_hits

    # Verify try_envelope_pw_fast == cc.try_envelope on Phase 3.2 control + 20 random candidates
    p3 = (GSMG_CLEAN / "data" / "phase3_plaintext.bin").read_bytes()
    p32_env = base64.b64decode(re.sub(rb"\s+", b"", p3[p3.index(b"U2FsdGVk") :]))
    p32_pw = hashlib.sha256(b"jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple").hexdigest().encode("ascii")
    assert try_envelope_pw_fast(p32_env, p32_pw) == cc.try_envelope(
        p32_env, "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple", "gsmg"
    )
    for c in p1_cands[:10]:
        pw = hashlib.sha256(c.encode("utf-8")).hexdigest().encode("ascii")
        for env_raw in cc.ENVELOPES.values():
            assert try_envelope_pw_fast(env_raw, pw) == cc.try_envelope(env_raw, c, "gsmg")

    # 3. Planted controls (one per part, using the exact same run_sweep loop!)
    ctrl_info = plan["controls"]
    cc.TARGETS[k1_h160] = "PLANTED k=1"
    try:
        # Part 1 planted control (100 real Part 1 candidates + planted candidate)
        p1_ctrl = ctrl_info["part1"]
        p1_ctrl_entries = [
            (
                f"ctrl_real_{i}",
                hashlib.sha256(c.encode("utf-8")).hexdigest().encode("ascii"),
                {"candidate": c},
            )
            for i, c in enumerate(p1_cands[:100])
        ]
        p1_ctrl_entries.append(
            (
                "ctrl_planted",
                hashlib.sha256(p1_ctrl["answer"].encode("utf-8")).hexdigest().encode("ascii"),
                {"candidate": p1_ctrl["answer"]},
            )
        )
        p1_ctrl_hist, p1_ctrl_ret = run_sweep(
            "part1_control",
            p1_ctrl_entries,
            {"planted_part1": base64.b64decode(p1_ctrl["envelope_b64"])},
            HERE / "controls" / "part1",
        )
        (p1_pos,) = [r for r in p1_ctrl_ret if r["candidate"] == p1_ctrl["answer"]]
        assert p1_pos["sha256"] == p1_ctrl["plaintext_sha256"]
        assert p1_pos["pad"] == p1_ctrl["expected_pad"]
        assert sorted({k.split("@")[0] for k in p1_pos["find_keys_hits"]}) == p1_ctrl["expected_find_keys_kinds"]
        for fl in p1_ctrl["expected_binscan_flags"]:
            assert fl in p1_pos["binary_scan_flags"]

        # Part 2 planted controls (100 real Part 2 passphrases + planted raw & hex arm passphrases)
        p2_ctrl_raw = ctrl_info["part2_raw"]
        p2_ctrl_hex = ctrl_info["part2_hex"]
        p2_ctrl_entries = [
            (f"ctrl_real_{i}", bytes.fromhex(pw_hex), {"label": lbl, "arm": lbl.rsplit("/", 1)[-1], "pw_hex": pw_hex})
            for i, (lbl, pw_hex) in enumerate(p2_rows[:100])
        ]
        p2_ctrl_entries.append(
            (
                "ctrl_planted_raw",
                bytes.fromhex(p2_ctrl_raw["pw_hex"]),
                {"label": p2_ctrl_raw["label"], "arm": "outer-sha256-raw", "pw_hex": p2_ctrl_raw["pw_hex"]},
            )
        )
        p2_ctrl_entries.append(
            (
                "ctrl_planted_hex",
                bytes.fromhex(p2_ctrl_hex["pw_hex"]),
                {"label": p2_ctrl_hex["label"], "arm": "outer-sha256-hex", "pw_hex": p2_ctrl_hex["pw_hex"]},
            )
        )
        p2_ctrl_hist, p2_ctrl_ret = run_sweep(
            "part2_control",
            p2_ctrl_entries,
            {
                "planted_part2_raw": base64.b64decode(p2_ctrl_raw["envelope_b64"]),
                "planted_part2_hex": base64.b64decode(p2_ctrl_hex["envelope_b64"]),
            },
            HERE / "controls" / "part2",
        )
        (p2_pos_raw,) = [r for r in p2_ctrl_ret if r["label"] == p2_ctrl_raw["label"] and r["envelope"] == "planted_part2_raw"]
        (p2_pos_hex,) = [r for r in p2_ctrl_ret if r["label"] == p2_ctrl_hex["label"] and r["envelope"] == "planted_part2_hex"]
        for pos, exp in ((p2_pos_raw, p2_ctrl_raw), (p2_pos_hex, p2_ctrl_hex)):
            assert pos["sha256"] == exp["plaintext_sha256"]
            assert pos["pad"] == exp["expected_pad"]
            assert sorted({k.split("@")[0] for k in pos["find_keys_hits"]}) == exp["expected_find_keys_kinds"]
            for fl in exp["expected_binscan_flags"]:
                assert fl in pos["binary_scan_flags"]
    finally:
        del cc.TARGETS[k1_h160]
    assert cc.TARGETS == orig_targets == plan["real_target_hash160"]
    print("Controls PASSED (cc.selftest, binscan.selftest, coincurve parity, Part 1 & Part 2 raw/hex planted controls)")

    # 4. Run Part 1 real sweep
    t0 = time.monotonic()
    p1_entries = [
        (
            f"p1_{i}",
            hashlib.sha256(c.encode("utf-8")).hexdigest().encode("ascii"),
            {"candidate": c},
        )
        for i, c in enumerate(p1_cands)
    ]
    p1_hist, p1_ret = run_sweep("part1", p1_entries, cc.ENVELOPES, HERE / "outputs" / "part1")
    p1_sec = time.monotonic() - t0
    p1_sum = summarize_part("part1", len(p1_cands), p1_hist, p1_ret, p1_sec)
    print(f"Part 1 done in {p1_sec:.2f}s: {p1_sum['decrypts']:,} decrypts, {len(p1_ret)} pad-valid, {len(p1_sum['find_keys_hit_records'])} key hits, {len(p1_sum['binary_scan_flagged_all_envelopes'])} binscan flags")

    # 5. Run Part 2 real sweep
    t1 = time.monotonic()
    p2_entries = [
        (
            f"p2_{i}",
            bytes.fromhex(pw_hex),
            {"label": lbl, "arm": lbl.rsplit("/", 1)[-1], "pw_hex": pw_hex},
        )
        for i, (lbl, pw_hex) in enumerate(p2_rows)
    ]
    p2_hist, p2_ret = run_sweep("part2", p2_entries, cc.ENVELOPES, HERE / "outputs" / "part2")
    p2_sec = time.monotonic() - t1
    p2_sum = summarize_part("part2", len(p2_rows), p2_hist, p2_ret, p2_sec)
    print(f"Part 2 done in {p2_sec:.2f}s: {p2_sum['decrypts']:,} decrypts, {len(p2_ret)} pad-valid, {len(p2_sum['find_keys_hit_records'])} key hits, {len(p2_sum['binary_scan_flagged_all_envelopes'])} binscan flags")

    # Arm breakdown for Part 2 pad-valid outputs
    p2_arm_pad = Counter((r["arm"], r["envelope"], r["pad"]) for r in p2_ret)

    results = {
        "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prereg_seal": seal_expected,
        "targets_verified": dict(cc.TARGETS),
        "controls": {
            "cc_selftest": True,
            "binscan_selftest": bscan_st,
            "coincurve_parity_verified": True,
            "fast_decrypt_parity_verified": True,
            "targets_restored": True,
            "part1_planted": {
                "passed": True,
                "histogram": p1_ctrl_hist,
                "matched_record": p1_pos,
            },
            "part2_planted": {
                "passed": True,
                "histogram": p2_ctrl_hist,
                "matched_raw_record": p2_pos_raw,
                "matched_hex_record": p2_pos_hex,
            },
        },
        "part1": p1_sum,
        "part2": p2_sum,
        "part2_pad_valid_by_arm": {f"{a}/{e}/pad{p}": v for (a, e, p), v in sorted(p2_arm_pad.items())},
        "part1_retained": p1_ret,
        "part2_retained": p2_ret,
    }

    (HERE / "results.json").write_bytes((json.dumps(results, indent=2) + "\n").encode("utf-8"))
    report = build_report(plan, results)
    (HERE / "REPORT.md").write_bytes(report.encode("utf-8"))
    print("Wrote results.json and REPORT.md")
    return 0


def _fmt_cand(r: dict[str, Any], max_len: int = 72) -> str:
    s = r.get("candidate") or r.get("label") or ""
    clean = s.replace("\r", "\\r").replace("\n", "\\n").replace("|", "\\|").replace("`", "'")
    if len(clean) > max_len:
        clean = clean[: max_len - 3] + "..."
    return f"`{clean}`"


def build_report(plan: dict[str, Any], res: dict[str, Any]) -> str:
    p1 = res["part1"]
    p2 = res["part2"]
    c1 = res["controls"]["part1_planted"]["matched_record"]
    c2r = res["controls"]["part2_planted"]["matched_raw_record"]
    c2h = res["controls"]["part2_planted"]["matched_hex_record"]

    total_keys = len(p1["find_keys_hit_records"]) + len(p2["find_keys_hit_records"])
    total_flags = len(p1["binary_scan_flagged_all_envelopes"]) + len(p2["binary_scan_flagged_all_envelopes"])
    total_print = len(p1["printable_gt_0_8_records"]) + len(p2["printable_gt_0_8_records"])
    total_pad2 = p1["pooled"]["pad_ge2"] + p2["pooled"]["pad_ge2"]
    verdict = "NULL" if (total_keys == 0 and total_flags == 0 and total_print == 0) else "CHECK_FINDINGS"

    lines: list[str] = []
    lines.append(f"# {verdict}: Six-Slot Resolved Replay (Part 1) & Haiku `hash_scope` Replay (Part 2)")
    lines.append("")
    lines.append(
        f"**Result: {verdict}.** Ran **{p1['decrypts'] + p2['decrypts']:,}** total AES-256-CBC decrypts "
        f"across all 3 envelopes in `cc.ENVELOPES` (**{p1['candidates']:,}** Part 1 candidates = "
        f"**{p1['decrypts']:,}** decrypts; **{p2['candidates']:,}** Part 2 passphrases = "
        f"**{p2['decrypts']:,}** decrypts). Retained all **{p1['pooled']['pad_valid_total'] + p2['pooled']['pad_valid_total']}** "
        f"pad-valid plaintexts as `.bin` files and ran both `find_keys` and the `cosmic_binary_scan` "
        f"`scan.py` checks on every single one. **Key hits: {total_keys}. Binary-scan flags: {total_flags}. "
        f"Printable > 0.8: {total_print}. Pad >= 2: {total_pad2}.** All controls passed."
    )
    lines.append("")
    lines.append("## Preregistration & Controls")
    lines.append("")
    lines.append(f"- **PREREG seal (`PREREG.sealed`):** `{res['prereg_seal']}` (sealed before any decryption).")
    lines.append(f"- **Part 1 candidate list (`part1_candidates.txt`):** `{plan['part1']['candidates_sha256_lf']}` ({plan['part1']['candidate_count']:,} unique strings).")
    lines.append(f"- **Part 2 passphrase list (`part2_passphrases.tsv`):** `{plan['part2']['passphrases_sha256_lf']}` ({plan['part2']['candidate_count']:,} unique passphrases).")
    lines.append(
        "- **Harness & parity controls:** `cc.selftest()` PASSED (Phase 3.2 opens at pad=10, 2,422 B; Half hash160, EC `k=1`, WIF, raw/hex detectors); "
        "`cosmic_binary_scan/scan.py:selftest()` PASSED (22 positive vectors, 0 flags on 1,327 B negative control); "
        "`coincurve` parity verified against pure-Python `cc.scalar_hits` on 20 scalars; fast last-block CBC decrypt verified identical to `cc.try_envelope`."
    )
    lines.append(
        f"- **Part 1 planted control (`controls/part1/planted_part1/`):** PASSED — recovered exact plaintext "
        f"(`pad={c1['pad']}`, `{c1['size']} B`, sha256 `{c1['sha256'][:16]}...`), `find_keys` fired on all 4 formats "
        f"(`{', '.join(sorted({k.split('@')[0] for k in c1['find_keys_hits']}))}`), and `scan.py` flagged `{', '.join(c1['binary_scan_flags'])}`."
    )
    lines.append(
        f"- **Part 2 planted controls (`controls/part2/`):** PASSED on both arms — "
        f"`outer-sha256-raw` (`pad={c2r['pad']}`, `{c2r['size']} B`, `find_keys`: `{', '.join(sorted({k.split('@')[0] for k in c2r['find_keys_hits']}))}`, "
        f"`scan.py`: `{', '.join(c2r['binary_scan_flags'])}`) and "
        f"`outer-sha256-hex` (`pad={c2h['pad']}`, `{c2h['size']} B`, `find_keys`: `{', '.join(sorted({k.split('@')[0] for k in c2h['find_keys_hits']}))}`, "
        f"`scan.py`: `{', '.join(c2h['binary_scan_flags'])}`)."
    )
    lines.append(
        "- **Targets verified after controls:** `a9553269572a317e39f0f518cb87c1a0ee1dbae4` (Half `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`) "
        "and `4bc468447fe1b048ad030a2f9a125478eabc4ed6` (Better Half `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`)."
    )
    lines.append("")

    for label, p, extra_notes in (
        (
            "Part 1 — Resolved Values in the Frozen Six-Slot String",
            p1,
            [
                f"- Frozen six-slot order (`SALPHASEION_PREREGISTRATION.md` lines 16–21): `{' | '.join(SLOTS_LITERAL)}`. Separators: `\"\"` and `\"z\"`. Slots 3–6 literal; no `yinyang` anywhere.",
                f"- Sets: `|A_core| = {plan['part1']['a_core_count']}` (58 `salphaseion_roles` + 10 explicit `563/497` forms), `|A_pipeline| = {plan['part1']['a_pipeline_count']:,}` (`#8446` forms), `|B| = {plan['part1']['b_total_count']}` (22 `salphaseion_roles` + 33 from the 8-base `PRE`/`DIG`/`RID` joins via `forms()`).",
                f"- Construction: (a) `A_core × B` × 2 seps + (b) `(A_core ∪ A_pipeline) × literal_B` × 2 seps + (c) `literal_A × B` × 2 seps → **{p1['candidates']:,}** unique candidates → **{p1['decrypts']:,}** decrypts under pinned `gsmg` profile.",
            ],
        ),
        (
            "Part 2 — `gsmg-haiku` `hash_scope` 876-Partition Replay",
            p2,
            [
                f"- Regenerated from `gsmg-haiku/review_leads/hash_scope.py:group_hashes()` (876 set partitions into ≥ 2 groups × 2 orders × 2 inner forms `hex`/`raw` × 2 joins `concat`/`interleave` = 7,008 unique bodies × 3 outer arms: `as-password` 7,008, `outer-sha256-hex` [pinned `gsmg`] 7,008, `outer-sha256-raw` 7,008).",
                f"- Count confirmation vs `HASH_SCOPE_REPORT.md`: **{plan['part2']['candidate_count']:,}** generated; skipping the **{plan['part2']['contiguous_overlap_count']}** contiguous `outer-sha256-hex` passphrases from `next_tests.py:partitions()` reproduces **{plan['part2']['hash_scope_report_unique_after_skip']:,}** unique passphrases × 3 = **{plan['part2']['hash_scope_report_aes_trials_verified']:,}** AES trials (exact match to `HASH_SCOPE_REPORT.md` line 10). This replay runs all **{p2['candidates']:,}** passphrases (**{p2['decrypts']:,}** decrypts) with full retention, `find_keys`, and `scan.py`.",
            ],
        ),
    ):
        lines.append(f"## {label}")
        lines.append("")
        lines.extend(extra_notes)
        lines.append("")
        lines.append("| Envelope | Decrypts | Pad-1 | Expected (N/256) | Poisson P(X >= pad-1) | Pad >= 2 | Retained `.bin` |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for ename in ("terminal_phase3_2_end", "salphaseion_short", "cosmic_duality"):
            e = p["per_envelope"][ename]
            lines.append(
                f"| `{ename}` | {e['decrypts']:,} | {e['pad1']} | {e['expected_n_over_256']:.2f} "
                f"| {e['poisson_p_ge_pad1']:.4f} | {e['pad_ge2']} | {e['pad_valid_total']} |"
            )
        pl = p["pooled"]
        lines.append(
            f"| **Pooled** | **{pl['decrypts']:,}** | **{pl['pad1']}** | **{pl['expected_n_over_256']:.2f}** "
            f"| **{pl['poisson_p_ge_pad1']:.4f}** | **{pl['pad_ge2']}** | **{pl['pad_valid_total']}** |"
        )
        lines.append("")

        lines.append(f"- **Any `pad >= 2`:** {len(p['pad_ge2_records'])}")
        lines.append(f"- **Any `printable > 0.8`:** {len(p['printable_gt_0_8_records'])}")
        lines.append(f"- **Any binary-scan flag (Cosmic Duality / SalPhaseIon short):** {len(p['binary_scan_flagged_cosmic_or_salphaseion'])} (all 3 envelopes: {len(p['binary_scan_flagged_all_envelopes'])})")
        lines.append(f"- **Any `find_keys` hit:** {len(p['find_keys_hit_records'])}")
        lines.append("")

        # List any pad >= 2, printable > 0.8, binary-scan flag, or find_keys hit explicitly
        notables = []
        seen_f = set()
        for bucket, rlist in (
            ("pad>=2", p["pad_ge2_records"]),
            ("printable>0.8", p["printable_gt_0_8_records"]),
            ("binary_scan_flag", p["binary_scan_flagged_all_envelopes"]),
            ("find_keys_hit", p["find_keys_hit_records"]),
        ):
            for r in rlist:
                key = r["file"]
                if key not in seen_f:
                    seen_f.add(key)
                    notables.append(r)

        if notables:
            lines.append("### Notable / Flagged / `pad >= 2` Records")
            lines.append("")
            lines.append("| Envelope | File | Candidate / Label | Pad | Size | First 16B hex | H (bits/B) | Printable | Binary flags | `find_keys` |")
            lines.append("|---|---|---|---:|---:|---|---:|---:|---|---|")
            for r in notables:
                fl = ", ".join(r["binary_scan_flags"]) if r["binary_scan_flags"] else "none"
                kh = ", ".join(f"{k}:{v}" for k, v in r["find_keys_hits"].items()) if r["find_keys_hits"] else "none"
                lines.append(
                    f"| `{r['envelope']}` | `{r['file']}` | {_fmt_cand(r)} | {r['pad']} | {r['size']} "
                    f"| `{r['first_16_hex']}` | {r['shannon_entropy']:.4f} | {r['printable_fraction']:.3f} | {fl} | {kh} |"
                )
            lines.append("")
        else:
            lines.append("*(No `pad >= 2`, no `printable > 0.8`, no binary-scan flags, and no `find_keys` hits.)*")
            lines.append("")

    lines.append("## Files")
    lines.append("")
    lines.append("| File / Directory | Description |")
    lines.append("|---|---|")
    lines.append("| `replay.py` | Preregistration builder, planted-control harness, dual replay, and report generator |")
    lines.append("| `PREREG.json`, `PREREG.sealed` | Pre-decrypt sealed specification and SHA-256 seal |")
    lines.append("| `part1_candidates.txt` | All Part 1 candidate strings (verbatim, LF) |")
    lines.append("| `part2_passphrases.tsv` | All Part 2 passphrases (`label\\tpw_hex`, LF) |")
    lines.append("| `controls/part1/`, `controls/part2/` | Retained planted control decrypts |")
    lines.append("| `outputs/part1/`, `outputs/part2/` | Every retained pad-valid plaintext (`.bin`) across all 3 envelopes |")
    lines.append("| `results.json` | Full machine-readable histograms, controls, and per-retained-file scan metadata |")
    lines.append("| `REPORT.md` | This report |")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Assertions must be enabled.")
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "build":
        raise SystemExit(build_and_seal())
    if cmd == "run":
        raise SystemExit(run_all())
    raise SystemExit("Usage: python replay.py [build|run]")
