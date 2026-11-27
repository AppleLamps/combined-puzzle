"""Run the sealed arm. An optional directory receives a separate reproduction."""
import argparse
import base64
import hashlib
import json
import sys
from collections import Counter
from math import comb
from pathlib import Path

RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(RUN.parents[1] / "tools"))
import check_candidate as cc
import prereg


def scan(candidates, envelopes, root, subdir):
    histograms = {}
    retained = []
    for name, envelope in envelopes.items():
        counts = Counter()
        for index, answer in enumerate(candidates, 1):
            pad, plain = cc.try_envelope(envelope, answer, "gsmg")
            counts[pad] += 1
            if pad == 0:
                continue
            path = root / subdir / name / f"cand_{index:02d}.bin"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(plain)
            saved = path.read_bytes()
            assert saved == plain
            readings = cc.find_keys(saved)
            retained.append({
                "envelope": name, "candidate": answer, "pad": pad, "bytes": len(saved),
                "file": path.relative_to(root).as_posix(),
                "sha256": hashlib.sha256(saved).hexdigest(),
                "printable_fraction": sum(b in (9, 10, 13) or 32 <= b < 127 for b in saved) / max(1, len(saved)),
                "find_keys_hits": {reading: targets for reading, targets in readings if targets},
            })
        histograms[name] = dict(sorted(counts.items()))
    return histograms, retained


def pad1_stats(n, k):
    # Exact Binomial(n, 1/256) tail as an integer ratio before conversion to float.
    denominator = 256 ** n
    tail = sum(comb(n, j) * 255 ** (n - j) for j in range(k, n + 1))
    return {"decrypts": n, "pad1": k, "expected": n / 256,
            "p_at_least_observed": tail / denominator, "p_zero": 255 ** n / denominator}


def run(root):
    if not __debug__:
        raise SystemExit("Run Python with assertions enabled.")
    seal = prereg.verify(RUN)
    plan = prereg.load(RUN)
    forms = [form for word in plan["operand"] for form in (word, word.lower())]
    candidates = list(dict.fromkeys(forms))
    candidate_bytes = "".join(s + "\n" for s in candidates).encode("utf-8")
    assert len(candidates) == plan["candidate_bound"]
    assert hashlib.sha256(candidate_bytes).hexdigest() == plan["candidates_sha256_lf"]
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in cc.ENVELOPES.items()}
    assert hashes == plan["envelope_sha256"]
    assert set(cc.TARGETS) == set(plan["real_target_hash160"])
    root.mkdir(parents=True, exist_ok=True)
    if (root / "results.json").exists():
        raise SystemExit("This directory already has results. Supply a fresh directory to replay.")
    (root / "candidates.txt").write_bytes(candidate_bytes)

    cc.selftest()
    fixture = plan["fixture"]
    original_targets = cc.TARGETS.copy()
    assert fixture["key_hash160"] not in original_targets
    cc.TARGETS[fixture["key_hash160"]] = "PLANTED k=1"
    try:
        planted_env = base64.b64decode(fixture["envelope_base64"], validate=True)
        ctrl_hist, ctrl_retained = scan(candidates, {"planted": planted_env}, root, "controls")
    finally:
        del cc.TARGETS[fixture["key_hash160"]]
    assert cc.TARGETS == original_targets
    planted, = [r for r in ctrl_retained if r["candidate"] == fixture["answer"]]
    assert (planted["pad"], planted["bytes"], planted["sha256"]) == (
        fixture["pad"], fixture["bytes"], fixture["plaintext_sha256"])
    kinds = {r.split("@")[0] for r in planted["find_keys_hits"]}
    assert kinds == {"raw32", "hex64", "WIF", "base64"}

    histograms, retained = scan(candidates, cc.ENVELOPES, root, "outputs")
    stats = {name: pad1_stats(sum(hist.values()), hist.get(1, 0)) for name, hist in histograms.items()}
    total = sum(s["decrypts"] for s in stats.values())
    assert total == len(candidates) * len(cc.ENVELOPES)
    report = {
        "prereg_sha256": seal, "profile": "gsmg", "supplied": len(plan["operand"]),
        "forms_before_dedupe": len(forms), "candidates": len(candidates),
        "controls": {"selftest_passed": True, "planted_passed": True, "target_set_restored": True,
                     "histogram": ctrl_hist, "retained_and_scanned": ctrl_retained},
        "pad_histograms": histograms, "pad1_by_envelope": stats,
        "pad1_total": pad1_stats(total, sum(s["pad1"] for s in stats.values())),
        "pad_ge2_count": sum(r["pad"] >= 2 for r in retained),
        "retained_and_scanned": retained,
        "plaintexts_with_key_hits": sum(bool(r["find_keys_hits"]) for r in retained),
    }
    (root / "results.json").write_bytes((json.dumps(report, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path, nargs="?", default=RUN)
    run(parser.parse_args().output_dir)
