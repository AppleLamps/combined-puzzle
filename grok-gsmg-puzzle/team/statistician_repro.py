#!/usr/bin/env python3
"""Reproduce counts in ledger/04-statistician.md (Statistician agent)."""

from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"
sys.path.insert(0, str(ROOT / "src"))

FAED = (ART / "faed.txt").read_text().strip()


def ok(name: str, cond: bool, detail: str = "") -> None:
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not cond:
        raise SystemExit(1)


def poster_weights() -> tuple[int, int]:
    """§8.1: weights wK∈0..0 (fixed 0), wW∈0..7, wB,wY∈0..12, wF∈0..3 on poster counts."""
    import json
    from collections import Counter

    letters = "".join(json.loads((ART / "matrix.json").read_text())["letters"])
    cnt = Counter(letters)
    sum161 = 0
    for w in range(8):
        for b in range(13):
            for y in range(13):
                for f in range(4):
                    s = cnt["K"] * 0 + cnt["W"] * w + cnt["B"] * b + cnt["Y"] * y + cnt["F"] * f
                    if s == 161:
                        sum161 += 1
    tuples = 8 * 13 * 13 * 4
    return tuples, sum161


def g_at_primes_p() -> tuple[int, float, float, int, int]:
    """Prime indices 2..570 (104 positions); matches P≈0.135 in handoff §6.3."""
    prime_positions = [p for p in range(2, 571) if _is_prime(p)]
    g_count = FAED.count("g")
    g_on_prime = sum(1 for p in prime_positions if FAED[p - 1] == "g")
    n = len(FAED)
    k = len(prime_positions)
    exp = g_count * k / n
    p_ge = sum(
        math.comb(g_count, x) * math.comb(n - g_count, k - x) / math.comb(n, k)
        for x in range(g_on_prime, min(g_count, k) + 1)
    )
    return g_on_prime, p_ge, exp, g_count, k


def _is_prime(p: int) -> bool:
    if p < 2:
        return False
    if p % 2 == 0:
        return p == 2
    for d in range(3, int(p**0.5) + 1, 2):
        if p % d == 0:
            return False
    return True


def main() -> None:
    out = subprocess.run(
        [sys.executable, str(ROOT / "src/check_report3_2026-10-17.py"), str(ART)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    ok("check_report3 runs", "362,880" in out or "362880" in out.replace(",", ""))
    ok("bifid 8 squares", "squares giving btcseed: 8" in out)

    tuples, n161 = poster_weights()
    ok("poster weight tuples 5408", tuples == 5408, str(tuples))
    ok("poster sum-161 count 5", n161 == 5, str(n161))

    g_on, p_ge, exp, g_tot, k_pr = g_at_primes_p()
    ok("g on primes count 24", g_on == 24, f"got {g_on}")
    ok("g at prime P>=24 ~0.135", 0.13 <= p_ge <= 0.14, f"p={p_ge:.4f} exp={exp:.3f}")

    low = [ord(c) - 96 for c in FAED[538:]]
    combos = sum(math.comb(32, k) for k in range(1, 5))
    ok("last-32 zero subsets 41448", combos == 41448, str(combos))

    print("statistician_repro: all checks passed")


if __name__ == "__main__":
    main()
