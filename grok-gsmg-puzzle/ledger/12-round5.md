# 12 — Round 5 pilot (brainstorm follow-up)

**Code:** `team/round5_battery.py` + `team/round5_preregistered.py` (M1–M5, 280 decrypts, prior null)  
**Plan:** [Tester Round 5 plan](bc-ece5ab54-8b32-506f-a6b1-0209a6c879f6)

## Controls (all PASS)

| KDF | Check |
|-----|--------|
| §4.1 | phase-2 `causality` |
| EVP-MD5 plain | community recipe → 79 B, sha256 `1449a217…` |
| EVP-MD5 | in-run round-trip **sha256hex-ascii** and **raw32** password bytes |

## Executed

| batch | decrypts | structured |
|-------|----------|------------|
| H1+H2 curated (165 strings × plain + sha256hex × 3 containers) | 990 | 0 |
| H3 quintuple filler sample (4096 × 3, sha256hex only) | 12,288 | 0 |
| H4 EVP-MD5 (165 × 5 variants × 3 containers) | 2,475 | 0 |
| **Total puzzle** | **15,753** | **0** |

## H1 / H2 (what was tested)

- Spiral **list→concat** recipes only (no standalone raw row-sum digit string).
- **After-SELECT** Architect bytes (390 chars): lower/upper, truncations, hex, recipe wraps.
- **165** unique curated strings (target was ~168; overlap/dedup).

## H4 MD5 pads (not structured)

| container | valid pads (of 825 tries each variant set) |
|-----------|---------------------------------------------|
| terminal | 6 |
| salphaseion_short | 7 |
| cosmic | 1 |

Sal-short **plain** community still the only known MD5 artifact; **no** structured prose on Terminal/Cosmic.

## Mechanisms pilot (`round5_preregistered.json`)

M1–M5: **280** decrypts, **0** hits (within 10k budget each).

## Result

**Null** — brainstorm hypotheses H1–H4 and cryptanalyst M1–M5 do not open containers or yield prize hash160 under registered detectors.

## Next (if continuing)

1. [Reader](bc-5fd657d0-8b88-5cc6-a514-aa6139dc8e89): checkerboard 149-digit `msl`, yinyang phase containers, `enter` XOR, Cosmic Duality title.  
2. [Strategist](bc-7eeec15f-a0fa-5fdb-b800-73c2e6d9b17d) H3 door-index deletion (not `C(60,k)`).  
3. Chained pipeline where step-1 plaintext **must** feed step-2 (M3 full chain, not single-step baselines).
