"""Single structured/plaintext detector for team batteries (audit R15)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from step1_btcseed import classify as classify_rich  # noqa: E402

PRINTABLE = set(range(32, 127))


def classify_unified(body: bytes | None) -> str:
    """Return 'structured', 'no-pad', 'pad-only-1', or opaque label."""
    if body is None:
        return "no-pad"
    rich = classify_rich(body)
    if rich.startswith("structured"):
        return "structured"
    p = body[-1]
    if 1 <= p <= 16 and body[-p:] == bytes([p]) * p and p == 1:
        return "pad-only-1"
    printable = sum(b in PRINTABLE for b in body)
    if (
        len(body) >= 8
        and printable >= len(body) * 0.9
        and sum(chr(b).isalpha() for b in body) >= 4
    ):
        return "structured"
    return rich if isinstance(rich, str) else "opaque"
