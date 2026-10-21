# 07 — Tester: MASK6 deletion sweep (2⁶ subsets)

**Follow-up to [Cryptanalyst decode tests](bc-fb8904ef-f72c-5f25-9c5f-aed3de2d1940) P0 and [Reader open-label readings](bc-036e5e38-a404-555a-854a-ffd85b37e52c).**

| Field | Value |
|-------|--------|
| **hypothesis** | Deleting (not zeroing) some subset of letters at faed positions `{1,3,551,557,561,563}` yields integer bytes whose latin-1 / hex / sha256hex opens a locked container under §4.1. |
| **code** | `team/deletion_sweep_faed.py` |
| **variants** | 64 (all subsets of the six positions) |
| **decrypts** | 576 (64 × 3 password forms × 3 containers) |
| **planted control** | Phase-2 `causality` decrypt from handoff HTML **OK** |
| **structured hits** | **0** |
| **win test** | **0** uncompressed hash160 matches |
| **result** | **Null** — no subset recovers both `yM` and `szqu` pins; best printable ~97/236, still not prose. Full six deletions: 234 B (matches prior mask6 deletion null). |

**Note:** Handoff §9 still says “deletion not tried” for exhaustive hidden-zero work; repo now documents **mask6-only** deletion sweep here. Broader deletion (arbitrary positions on faed / fillers / dbbi) remains open per Reader.
