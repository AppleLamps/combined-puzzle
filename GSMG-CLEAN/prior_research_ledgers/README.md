# Prior research ledgers (raw, verbatim copies)

These are the most informative write-ups from each earlier round, kept for their detail: trial scopes, reasoning, message context.

**Warning**
- **They are not clean.** They contain claims that were later retracted, results under broken gates, and stale paths (`E:\rabbitv3`, `E:\rabbitv4`, `D:\newest-puzzle-9.9.26`, Desktop). Check `../05_CORRECTIONS_AND_PITFALLS.md` before relying on any statement here.
- Where a ledger and `01`–`05` disagree, `01`–`05` win.
- Scripts and `out/` folders they link to were **not** copied. They are still in the original round folders under `E:\rabbit-combined\`.

| Folder | Origin | Files | Use it for | Caution |
|---|---|---|---|---|
| `rabbit_r1/` | `rabbit` (round 1) | FINDINGS_round1 | Round-1 sweeps (allwin, arch1–4, h140, seven, kdfsweep …) | Raw-only oracles; B1 half-blob bug; fastoracle checked only Half |
| `rabbitv2_audit/` | `rabbitv2` | FINDINGS_audit_39_addenda, EVIDENCE_STATUS | The same audit extended to Add.39; primary-evidence recovery (Wayback, poster bytes, chain) | Pre-Add.21 nulls use narrow gates; "site dead" era |
| `rabbit_gemini_audit/` | `rabbit-gemini` | FINDINGS_48_addenda, CREATOR_HINTS, DOOR_HINTS | The audit to Add.48, including Add.29/30 (retracted 4f7a1e door), Add.36 terminal/zeroed, Add.40 site live; creator hints verified vs the 2026-09-09 export | Its `corpus\terminal_envelope.*` is actually SalPhaseIon; MD5-primary claim for Cosmic is unverified |
| `rabbitv3_reviews/` | `rabbitv3` | CLASSICAL_PRIORITY, GATE_CONVENTION_AUDIT, PATTERN_REVIEW, SPECIFIED_CONSTRUCTIONS | Classical-cipher screen; gate differential (69,666 verifier calls); why decoded labels ≠ instructions | Links point to `E:/rabbitv3/...` |
| `rabbitv4_leads/` | `rabbitv4` | RESULTS (workstreams A–K), LOCKED_ENVELOPES_ANGLES, ARCHITECT_DIFF_AND_FIRST_HINT, CHAIN_ACTIVITY, COMMUNITY_GROUP_EXPORT, CREATOR_AND_PLAINTEXT_REVIEW_2026-09-10, CREATOR_HINTS_UNNOTICED_2026-09-12, JRK_HINTS_THAT_HELPED_2026-09-13.txt | Trial counts for A–K; envelope-by-envelope angles; Architect-vs-film diff; mempool history; community-chat notes; which hints led to verified steps | Message counts differ by export date |
| `read_solve_review/` | `read\SOLVE` and `read\PUZZLE-REVIEW` | STATUS, HINT-SYNTHESIS, HILL-CONTINUATION, REVIEW, SESSION-RECOVERY, KEY-REVIEW | Largest classical attack record (affine MITM, Morbit/Pollux, FAED Bifid numeric); the 479 → PRIVATEKEY route (HINT-SYNTHESIS); Hill/ifindo negatives; KEY-REVIEW (#2910/#2918) | HINT-SYNTHESIS calls its route "likely intended"; this is not proven. `read\phase3_plaintext.txt` referenced there is wrong (4,095 B) |
| `puz_op/` | `puz-op` | FAED_ROW_SELECTOR_REPORT | 32 row-selector models, 16 valid outputs | No AES trials were run on the 16 outputs |
| `newest_9926_dbbi_hex/` | `newest-puzzle-9.9.26` | PROGRESS.md | Origin of the DBBI-as-hex lead (b/g prefixes → 64 tokens / 16 codes) and the KDF proof | Its `prefix_structure_check.py` and `hash_pattern_probe.py` exist nowhere under `E:\rabbit-combined`. `../tools/reproduce_leads.py` L5 and `../tools/check_candidate.py` replace them |

- The `rabbit_r1`, `rabbitv2_audit` and `rabbit_gemini_audit` FINDINGS files share the same base text ("What the GSMG.io 5 BTC puzzle group has been doing wrong"). Each adds more addenda, so the gemini copy is the most complete.
- Retractions in later addenda override earlier ones.
