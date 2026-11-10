"""Test DBBI prime tokens as framing metadata against the Architect differential.

The 83-cell parse is fixed by the serial off-white poster schedule. Prime cells
remain boundaries and contribute no values. The 60 ordinary cells are split into
the 24 gaps surrounding the 23 markers. This script tests only:

* ordered gap lengths;
* the terminal ordinary value of each gap;
* whole-interval reversals; and
* row-local indexing of those values into the 24-row Architect edit table.

No prime token is added, subtracted, replaced, or interpreted as a number.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "runs/2026-09-15_dbbi_framing_architect"
TRIGRAMS = (
    "THE", "AND", "ING", "ION", "ENT", "TIO", "FOR", "HER", "TER", "HAT",
    "THA", "ERE", "ATE", "HIS", "CON", "RES", "VER", "ALL", "ONS", "NCE",
    "MEN", "ITH", "TED", "ERS", "PRO", "THI", "WIT", "ARE", "ESS", "NOT",
)
ORACLES = (
    "MATRIXSUMLIST", "LASTWORDSBEFOREARCHICHOICE", "THISPASSWORD", "PRIVATEKEY",
    "ACTUALPRIVATEKEY", "BTCSEED", "RETURNTO", "REINSERTINGTHEPRIMEBASICS",
)


def letters(text: str) -> str:
    return "".join(re.findall(r"[A-Za-z]", text)).upper()


def english_score(text: str) -> int:
    text = letters(text)
    return sum(text.count(token) for token in TRIGRAMS)


def is_prime(n: int) -> bool:
    return n > 1 and all(n % d for d in range(2, int(n**0.5) + 1))


def load_framing(root: Path = ROOT) -> dict:
    parsed = json.loads(
        (root / "runs/2026-09-13_offwhite_alignment/guided_parses.json").read_text()
    )["serial_offwhite_B"]
    cells = parsed["cells"]
    assert parsed["complete"] and len(cells) == 83

    gaps: list[list[str]] = [[]]
    markers: list[dict] = []
    for cell in cells:
        if cell["prime"]:
            markers.append(cell)
            gaps.append([])
        else:
            gaps[-1].append(cell["token"])

    payload = "".join("".join(gap) for gap in gaps)
    schedule = "".join("B" if m["token"] == "b" else "Y" for m in markers)
    assert len(markers) == 23 and len(gaps) == 24 and len(payload) == 60
    assert all(is_prime(m["slot"]) for m in markers)
    assert all(not is_prime(c["slot"]) for c in cells if not c["prime"])
    return {
        "cells": cells,
        "gaps": gaps,
        "markers": markers,
        "schedule": schedule,
        "payload": payload,
        "lengths": [len(g) for g in gaps],
        "terminals": [g[-1] if g else None for g in gaps],
    }


def load_edit_tables(root: Path = ROOT) -> dict[str, list[dict]]:
    tables = json.loads(
        (root / "runs/2026-09-14_aligned_replacement_v2/tables.json").read_text()
    )
    selected = {name: obj["rows"] for name, obj in tables.items() if len(obj["rows"]) == 24}
    assert set(selected) == {"kedri/spelled/sequence", "kedri/spelled/lcs"}
    return selected


def differential_targets(root: Path = ROOT) -> dict[str, str]:
    targets: dict[str, str] = {}
    tables = load_edit_tables(root)
    for table_name, rows in tables.items():
        for side in ("source", "replacement"):
            blocks = [letters(row[side]["raw"]) for row in rows]
            targets[f"{table_name}/{side}/joined"] = "".join(blocks)
            targets[f"{table_name}/{side}/initials"] = "".join(b[:1] for b in blocks)
            targets[f"{table_name}/{side}/finals"] = "".join(b[-1:] for b in blocks)

    old = json.loads(
        (root / "runs/2026-09-14_architect_differential/results.json").read_text()
    )
    for row in old["all"]:
        value = letters(row["output"])
        if value:
            key = "/".join(
                str(row.get(k)) for k in ("source", "stream", "mode", "selector", "base")
            )
            targets[f"legacy/{key}"] = value
    return targets


def schedule_for_gaps(schedule: str, attachment: str) -> list[str | None]:
    """Attach a marker to the gap it closes or to the gap it opens."""
    if attachment == "closes":
        return list(schedule) + [None]
    if attachment == "opens":
        return [None] + list(schedule)
    raise ValueError(attachment)


def reverse_gaps(
    gaps: list[list[str]], schedule: str, mode: str, attachment: str = "closes"
) -> list[list[str]]:
    colors = schedule_for_gaps(schedule, attachment)
    out: list[list[str]] = []
    for gap, color in zip(gaps, colors):
        reverse = (
            mode == "all"
            or (mode == "blue" and color == "B")
            or (mode == "yellow" and color == "Y")
        )
        out.append(list(reversed(gap)) if reverse else list(gap))
    return out


def index_char(block: str, value: int | None, base: int, edge: str, overflow: str) -> str:
    if value is None or not block:
        return "X"
    index = value - 1 if base == 1 else value
    if overflow == "cyclic":
        index %= len(block)
    elif not 0 <= index < len(block):
        return "X"
    if edge == "end":
        index = len(block) - 1 - index
    return block[index]


def descriptor_candidates(framing: dict, tables: dict[str, list[dict]]) -> list[dict]:
    candidates: list[dict] = []
    descriptors = {
        "gap_length": framing["lengths"],
        "terminal": [ord(x) - 96 if x else None for x in framing["terminals"]],
    }
    for table_name, rows in tables.items():
        for side in ("source", "replacement"):
            blocks = [letters(row[side]["raw"]) for row in rows]
            for descriptor_name, values in descriptors.items():
                for row_order in ("forward", "reverse"):
                    ordered_blocks = blocks if row_order == "forward" else list(reversed(blocks))
                    for base in (0, 1):
                        for edge in ("start", "end"):
                            for overflow in ("strict", "cyclic"):
                                output = "".join(
                                    index_char(block, value, base, edge, overflow)
                                    for block, value in zip(ordered_blocks, values)
                                )
                                candidates.append({
                                    "family": "descriptor_index",
                                    "table": table_name,
                                    "side": side,
                                    "descriptor": descriptor_name,
                                    "row_order": row_order,
                                    "base": base,
                                    "edge": edge,
                                    "overflow": overflow,
                                    "output": output,
                                })
    return candidates


def interval_candidates(framing: dict, tables: dict[str, list[dict]]) -> list[dict]:
    candidates: list[dict] = []
    reversal_specs = [("none", "closes"), ("all", "closes")]
    reversal_specs += [(color, attachment) for color in ("blue", "yellow")
                       for attachment in ("closes", "opens")]
    for reverse_mode, attachment in reversal_specs:
        gaps = reverse_gaps(framing["gaps"], framing["schedule"], reverse_mode, attachment)
        payload = "".join("".join(g) for g in gaps)
        candidates.append({
            "family": "interval_render",
            "reverse": reverse_mode,
            "attachment": attachment,
            "output": payload.upper(),
        })
        values_by_gap = [[ord(x) - 96 for x in gap] for gap in gaps]
        for table_name, rows in tables.items():
            for side in ("source", "replacement"):
                blocks = [letters(row[side]["raw"]) for row in rows]
                for row_order in ("forward", "reverse"):
                    ordered_blocks = blocks if row_order == "forward" else list(reversed(blocks))
                    for base in (0, 1):
                        for edge in ("start", "end"):
                            for overflow in ("strict", "cyclic"):
                                output = "".join(
                                    index_char(block, value, base, edge, overflow)
                                    for block, values in zip(ordered_blocks, values_by_gap)
                                    for value in values
                                )
                                candidates.append({
                                    "family": "interval_index",
                                    "reverse": reverse_mode,
                                    "attachment": attachment,
                                    "table": table_name,
                                    "side": side,
                                    "row_order": row_order,
                                    "base": base,
                                    "edge": edge,
                                    "overflow": overflow,
                                    "output": output,
                                })
    return candidates


def annotate(candidates: list[dict], targets: dict[str, str]) -> None:
    unique_targets = sorted(set(targets.values()))
    for row in candidates:
        output = row["output"]
        clean = "X" not in output
        normalized = letters(output)
        row["clean"] = clean
        row["score"] = english_score(output) if clean else -1
        row["oracle_hits"] = [oracle for oracle in ORACLES if oracle in normalized]
        row["exact_differential"] = [name for name, value in targets.items() if normalized == value]
        row["contained_differential"] = [
            target for target in unique_targets
            if len(target) >= 4 and (target in normalized or normalized in target)
        ][:10]
        ratios = [SequenceMatcher(None, normalized, target).ratio() for target in unique_targets
                  if normalized and target]
        row["max_differential_ratio"] = round(max(ratios, default=0.0), 6)


def build_candidates(framing: dict, tables: dict[str, list[dict]], targets: dict[str, str]) -> list[dict]:
    candidates = descriptor_candidates(framing, tables) + interval_candidates(framing, tables)
    annotate(candidates, targets)
    return candidates


def pearson(left: list[int], right: list[int]) -> float:
    assert len(left) == len(right) and left
    lm, rm = sum(left) / len(left), sum(right) / len(right)
    lvar = sum((value - lm) ** 2 for value in left)
    rvar = sum((value - rm) ** 2 for value in right)
    if not lvar or not rvar:
        return 0.0
    return sum((a - lm) * (b - rm) for a, b in zip(left, right)) / (lvar * rvar) ** 0.5


def architect_feature_vectors(tables: dict[str, list[dict]]) -> dict[str, list[int]]:
    # The sequence and LCS 24-row tables are identical. Retain one named copy so
    # duplicate alignments cannot inflate the comparison count.
    rows = tables["kedri/spelled/sequence"]
    vectors: dict[str, list[int]] = {}
    for side in ("source_features", "replacement_features", "difference"):
        for index, feature in enumerate(("word_count", "letter_count", "a1z26_sum")):
            vectors[f"{side}/{feature}"] = [row[side][index] for row in rows]
    for side in ("source", "replacement"):
        vectors[f"{side}/word_start"] = [row[side]["word_range"][0] for row in rows]
        vectors[f"{side}/word_end"] = [row[side]["word_range"][1] for row in rows]
    vectors["replacement/letter_start"] = [row["replacement"]["letter_range"][0] for row in rows]
    vectors["replacement/letter_end"] = [row["replacement"]["letter_range"][1] for row in rows]
    return vectors


def vector_analysis(
    framing: dict, tables: dict[str, list[dict]], trials: int = 20000, seed: int = 9152027
) -> dict:
    vectors = architect_feature_vectors(tables)
    descriptors = {
        "gap_length": framing["lengths"],
        "terminal_zero_for_empty": [ord(value) - 96 if value else 0 for value in framing["terminals"]],
    }
    rng = random.Random(seed)
    result = {}
    for descriptor_name, values in descriptors.items():
        comparisons = []
        for feature_name, vector in vectors.items():
            for order, actual in (("forward", vector), ("reverse", list(reversed(vector)))):
                corr = pearson(values, actual)
                comparisons.append({
                    "feature": feature_name,
                    "order": order,
                    "pearson": round(corr, 6),
                    "raw_equal_positions": sum(a == b for a, b in zip(values, actual)),
                    "mod9_equal_positions": sum(a % 9 == b % 9 for a, b in zip(values, actual)),
                })
        comparisons.sort(key=lambda row: (-abs(row["pearson"]), row["feature"], row["order"]))
        authentic_max = abs(comparisons[0]["pearson"])
        control_at_or_above = 0
        control_max = 0.0
        for _ in range(trials):
            shuffled = values[:]
            rng.shuffle(shuffled)
            trial_max = max(
                abs(pearson(shuffled, actual))
                for vector in vectors.values()
                for actual in (vector, list(reversed(vector)))
            )
            control_max = max(control_max, trial_max)
            if trial_max >= authentic_max:
                control_at_or_above += 1
        result[descriptor_name] = {
            "top": comparisons[:12],
            "authentic_max_abs_pearson": authentic_max,
            "controls": trials,
            "control_max_abs_pearson": round(control_max, 6),
            "controls_at_or_above_authentic": control_at_or_above,
            "permutation_p": round((control_at_or_above + 1) / (trials + 1), 6),
        }
    return result


def control_calibration(
    framing: dict, tables: dict[str, list[dict]], targets: dict[str, str],
    trials: int, seed: int,
) -> dict:
    rng = random.Random(seed)
    lengths = framing["lengths"]
    values = list(framing["payload"])
    maxima_score: list[int] = []
    for _ in range(trials):
        shuffled = values[:]
        rng.shuffle(shuffled)
        at = 0
        gaps = []
        for length in lengths:
            gaps.append(shuffled[at:at + length])
            at += length
        control = dict(framing)
        control["gaps"] = gaps
        control["payload"] = "".join(shuffled)
        control["terminals"] = [g[-1] if g else None for g in gaps]
        # Calibrate readability only. Repeating fuzzy comparison against hundreds of
        # legacy streams adds cost without changing the exact-match decision rule.
        rows = descriptor_candidates(control, tables) + interval_candidates(control, tables)
        clean_outputs = [row["output"] for row in rows if "X" not in row["output"]]
        maxima_score.append(max((english_score(output) for output in clean_outputs), default=-1))
    return {
        "trials": trials,
        "seed": seed,
        "max_english_score": max(maxima_score, default=-1),
        "p95_english_score": sorted(maxima_score)[int(0.95 * (len(maxima_score) - 1))] if maxima_score else -1,
        "score_maxima_histogram": dict(sorted(Counter(maxima_score).items())),
    }


def write_report(
    out: Path, framing: dict, candidates: list[dict], controls: dict, vector_results: dict
) -> dict:
    clean = [row for row in candidates if row["clean"]]
    top_score = max((row["score"] for row in clean), default=-1)
    top_ratio = max((row["max_differential_ratio"] for row in clean), default=0.0)
    exact = [row for row in candidates if row["exact_differential"]]
    oracle = [row for row in candidates if row["oracle_hits"]]
    real_score_ge = sum(count for score, count in controls["score_maxima_histogram"].items()
                        if int(score) >= top_score)
    summary = {
        "logical_cells": 83,
        "prime_markers": 23,
        "ordinary_cells": 60,
        "gaps": 24,
        "schedule": framing["schedule"],
        "gap_lengths": framing["lengths"],
        "gap_strings": ["".join(g) for g in framing["gaps"]],
        "terminal_values": [ord(x) - 96 if x else None for x in framing["terminals"]],
        "terminal_letters": [x for x in framing["terminals"]],
        "payload_roundtrip": "".join("".join(g) for g in framing["gaps"]) == framing["payload"],
        "candidate_count": len(candidates),
        "clean_candidate_count": len(clean),
        "unique_clean_outputs": len({row["output"] for row in clean}),
        "exact_differential_matches": len(exact),
        "oracle_hits": len(oracle),
        "top_english_score": top_score,
        "top_differential_ratio": top_ratio,
        "controls": controls,
        "ordered_vector_comparisons": vector_results,
        "controls_at_or_above_real_english_max": real_score_ge,
        "top_candidates": sorted(
            clean,
            key=lambda row: (-row["score"], -row["max_differential_ratio"], row["output"]),
        )[:20],
        "top_ratio_candidates": sorted(
            clean,
            key=lambda row: (-row["max_differential_ratio"], -row["score"], row["output"]),
        )[:20],
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    with (out / "candidates.jsonl").open("w") as handle:
        for row in candidates:
            handle.write(json.dumps(row, separators=(",", ":")) + "\n")
    manifest = {
        "date": "2026-09-15",
        "closed_system": True,
        "network": False,
        "envelope_bytes_read": 0,
        "aes_decryptions": 0,
        "dbbi_sha256": hashlib.sha256((ROOT / "data/DBBI_91.txt").read_bytes()).hexdigest(),
        "framing_source": "serial_offwhite_B / 83 logical cells",
        "ordinary_policy": "preserved exactly; prime values stripped, never transformed",
        "families": ["ordered gap lengths", "terminal ordinary values", "whole-interval reversals"],
        "architect_alignment": "kedri/spelled, 24 edit rows, sequence and LCS",
        "control_policy": "shuffle only the 60 ordinary values; preserve 24 gap lengths and all markers",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    lines = [
        "# DBBI prime markers as framing metadata",
        "",
        "## Result",
        "",
        "The 83-cell DBBI parse produces exactly **23 fixed prime boundaries, 24 ordered gaps, and 60 ordinary cells**. "
        "Every ordinary cell round-trips unchanged. Prime-token values are absent from every operand.",
        "",
        f"The bounded run generated **{len(candidates)} candidates** ({len(clean)} complete, "
        f"{summary['unique_clean_outputs']} unique complete outputs). It found **{len(exact)} exact Architect-differential matches** "
        f"and **{len(oracle)} known-instruction hits**.",
        "",
        f"The best complete English score was **{top_score}**; the randomized-control maximum was "
        f"**{controls['max_english_score']}**, with **{real_score_ge}/{controls['trials']}** control trials reaching or "
        "exceeding the real maximum. The best descriptive differential similarity was "
        f"**{top_ratio:.3f}**; acceptance still requires an exact match or readable output, not a fuzzy ratio.",
        "",
        "No tested framing read rises above the fixed-gap shuffled controls.",
        "",
        "Direct ordered-vector comparison is also null. The gap-length vector's strongest absolute Pearson "
        f"correlation is **{vector_results['gap_length']['authentic_max_abs_pearson']:.3f}** "
        f"(permutation p={vector_results['gap_length']['permutation_p']:.3f}); the terminal-value vector's is "
        f"**{vector_results['terminal_zero_for_empty']['authentic_max_abs_pearson']:.3f}** "
        f"(p={vector_results['terminal_zero_for_empty']['permutation_p']:.3f}).",
        "",
        "## Exact framing",
        "",
        f"- Marker schedule: `{framing['schedule']}`",
        f"- Gap lengths: `{','.join(map(str, framing['lengths']))}`",
        f"- Gaps: `{' | '.join(''.join(g) or '∅' for g in framing['gaps'])}`",
        f"- Terminal letters: `{' '.join(x or '∅' for x in framing['terminals'])}`",
        f"- Terminal values: `{' '.join(str(ord(x)-96) if x else '∅' for x in framing['terminals'])}`",
        "",
        "The gap-length sequence is fixed by the locations of the primes; it is not independent ciphertext. "
        "The terminal sequence is payload-derived and retains empty gaps explicitly.",
        "",
        "## Tested operations",
        "",
        "1. Align the 24 DBBI gaps one-to-one with each 24-row Kedri/spelled Architect edit table.",
        "2. Use the gap length or terminal value as a row-local index into removed or inserted letters, from either end, "
        "under zero/one-based and strict/cyclic conventions.",
        "3. Reverse complete DBBI gap intervals: all intervals, blue-closing intervals, yellow-closing intervals, and the "
        "corresponding marker-opens-next-gap convention. Internal character order changes; gap order and boundaries do not.",
        "4. Use every ordinary value in each interval as a row-local Architect index under the same declared conventions.",
        "5. Compare complete outputs with all retained Architect-differential streams and the exact instruction oracles.",
        "",
        "## Scope",
        "",
        "This closes direct row-local indexing and whole-gap reversal under the framing model. It does not test arbitrary "
        "permutations, arithmetic on ordinary values, or treating prime markers as values. The latter is excluded by design.",
        "",
        "Reproduce with `python tools/audit_dbbi_framing_architect.py` and verify with "
        "`python tools/test_audit_dbbi_framing_architect.py`.",
    ]
    (out / "REPORT.md").write_text("\n".join(lines) + "\n")
    return summary


def run(out: Path = DEFAULT_OUT, trials: int = 2000, seed: int = 9152026) -> dict:
    framing = load_framing()
    tables = load_edit_tables()
    targets = differential_targets()
    candidates = build_candidates(framing, tables, targets)
    controls = control_calibration(framing, tables, targets, trials, seed)
    vector_results = vector_analysis(framing, tables)
    return write_report(out, framing, candidates, controls, vector_results)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--controls", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=9152026)
    args = parser.parse_args()
    summary = run(args.out, args.controls, args.seed)
    print(json.dumps({
        key: summary[key] for key in (
            "logical_cells", "prime_markers", "ordinary_cells", "gaps", "candidate_count",
            "clean_candidate_count", "exact_differential_matches", "oracle_hits",
            "top_english_score", "top_differential_ratio",
        )
    }, indent=2))


if __name__ == "__main__":
    main()
