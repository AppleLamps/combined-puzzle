# Synthesis packet results (2026-09-08)

Reading: `SYNTHESIS.md`. Source letters SHA-256: `0ba7d70c…3af6` (765 a–i chars).  
Enter list SHA-256: `60f29326…2baf` (`password_list_synthesis.json`, **94** unique strings × raw + sha256hex = **188** leftover-3.2 attempts).

## Verdict

**matrixsumlist-as-sum did not produce a door, and entering those lists did not decrypt leftover 3.2.** Zero PKCS#7 successes. Zero `1GSMG` pubkey hits. No `gsmg.io` path in the sum letters.

| Hypothesis | Result |
|------------|--------|
| Row/col sums mod 9 on dbbi 7×13 / 13×7, faed’s divisor grids, and the 765-letter block are a hidden English list | **Closed — letter strings, not words** (e.g. dbbi 7×13 a1i9 rows `abefdih`, cols `abfafffghchfb`) |
| Enter those lists into leftover 3.2 | **Closed — no decrypt** |
| Neo passport date forms (`09112001`, `09/11/2001`, `20010911`, …) as leftover 3.2 | **Closed — no decrypt** |
| Architect two-door sentences with punctuation as leftover 3.2 | **Closed — no decrypt** |
| 7-interleave of stage secrets (your v5, 739 assemblies) | **Accepted as closed** — not retried |
| Published 7-XOR Cosmic Duality | Already open; binary 1327 B; not the prize key |

mod 9 on a 9-letter alphabet always stays in a–i. That tautology was not a find.

## What was not this packet

- Another 7-interleave / stride search
- FAED Bifid / 96-state
- `{1,4,21}`
- 140 (still no artifact of that length)
- Other wallets (“half and better half”)

Machine log: `packet/out/matrixsumlist.json`, `packet/out/results_synthesis.json`.
