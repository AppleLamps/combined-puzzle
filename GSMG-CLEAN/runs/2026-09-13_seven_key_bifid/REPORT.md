# Seven-key Bifid (BAR / CAN / FEE) → locked envelopes — 2026-09-13

**Result: clean null.**
- 0 Half / Better Half keys.
- Pad-valid rates are at chance for the real DBBI and for 200 shuffled controls alike.
- 0 pad ≥ 3. No plaintext looks like text (the best printable ratio is 0.53).

## What was tested

**Construction** (astra `tools/audit_mnemonic_models.py`; community #45661). The seven contiguous 13-letter DBBI rows are Bifid keys:
- The square is `dict.fromkeys(key + "ABCDEFGHIKLMNOPQRSTUVWXYZ")`.
- The whole period (all 570 FAED letters) is decrypted at once.
- In successive mode each output feeds the next key. Rounds 2 / 4 / 5 begin **BAR / CAN / FEE**.

**Fidelity checks.** All asserted in `prepare` and all passed:
- successive prefixes BTCSEEDDEOEM / BARSKCRNEYIW / EOHWRIRMDVFE / CANQFIVISCKT / FEEFPMQBGGAQ / IKDGCBFHNWNA / GTHWKMGLAKIG
- every round re-encodes to its input
- reverse-order final output sha256 `9aa4d617…` matches astra
- astra's **2,000-shuffle control histogram reproduced exactly**: [1465, 508, 25, 2, 0, 0, 0]

**Candidate generator.** One function is applied identically to the real DBBI and to each control DBBI:

| Family | Forms |
|---|---|
| Round outputs | raw FAED and FAED with positions 400/474 zeroed × listed/reverse key order × successive/independent × rounds 1–7: full text, round-1 text after `BTCSEED`, all 7 concatenated |
| Prefixes | first 3–12 letters of each round, concatenated or space-separated |
| Word forms | the BIP39 words found at round starts (real DBBI: BAR, CAN, FEE): joined with '' / space / `,` / `-` / `_`; with BTCSEED, BTC SEED or SEED before, or SEED after; each word alone |
| Keys as passwords | the seven keys joined with '' / space / `,` / newline, and intertwined column-wise, in listed and reverse order; sha256 of each key (upper and lower) concatenated, intertwined or XORed, as hex |

- Every text form is tried in upper and lower case.
- Derivations: sha256-hex / raw / sha256-raw × EVP_BytesToKey SHA-256 / MD5.
- Envelopes: Terminal b45a…, SalPhaseIon short 3ab5…, Cosmic 2d3f….

**Controls.** The first 200 shuffles of astra's conditional randomisation:
- seed 20260905
- the 53 eligible positions are shuffled; the first 13 letters and every prime B/BE span stay fixed
- control scores: 155 score 0, 42 score 1, 3 score 2; none reaches the real score of 3

**Positive controls.**
- The Phase 3.2 envelope opens with its known answer (pad 10, 2,422 B).
- The key detector finds a planted k = 1 key.

**Integrity.**
- `run` refused to start unless the sha256 of `candidates.json` and of the shared helper module matched `manifest.json`.
- Manifest sha256: `7a2f868c…64a4`.

## Numbers

59,976 unique texts × 3 envelopes × 6 derivations = **1,079,568 AES-CBC trials**. The run took 155 s.

| Group | Trials | Pad-valid | Expected (1/255) | pad = 2 |
|---|---|---|---|---|
| Real DBBI only | 6,408 | 28 (Cosmic 11 / SalPhaseIon 11 / Terminal 6) | 25.1 | 1 |
| Shared by real and controls | 216 | 4 | 0.8 | 0 |
| Controls only | 1,072,944 | 4,214 | 4,207 | 10 |

- **Shared group.** 4 hits against 0.85 expected (Poisson P(≥4) ≈ 1%). These texts are not specific to the seven-key idea: they are round-1 or independent-prefix texts that the controls also produce, because the first key is fixed. All 4 plaintexts are 79 B / 1,327 B of random bytes (printable 0.24–0.37) with pad 1, so this is read as chance, not signal.
- **Real pad-2 hit.** It came from `faaibzcnfffn…` (reverse order, prefix-8, lowercase) on SalPhaseIon with sha256hex/SHA-256. Its plaintext is 78 B at 0.30 printable, which is noise. The pad-2 rate is 1 in 6,408 for the real DBBI and 10 in 1.07 M for the controls; with ≈0.1 expected, one hit is not significant.
- **BAR / CAN / FEE.** The word forms gave 6 pad-1 hits (`BAR` on Terminal and on Cosmic, `seedbarcanfee`, `BTC SEED BAR CAN FEE`, `seed-bar-can-fee`, `btcseed_bar_can_fee`). All are random bytes with no key shapes. The 54 word-form texts × 18 trials give 3.8 expected, so 6 is within noise (P(≥6) ≈ 19%).
- **Keys and key shapes.** No candidate matched a key. No plaintext contained a WIF, hex64 or base64-32 key shape.
- **Reproduction of astra's prior test.** Its 8 complete final outputs (listed/reverse × raw/zeroed × upper/lower) gave **0 pad-valid under sha256-hex on all envelopes**, matching astra's result. They gave 2 pad-1 hits only under raw / sha256-raw derivations, both noise.

## Scope of this null

This null covers the forms above only. It does **not** cover:
- other Bifid periods, or squares that keep J instead of I
- other ways of choosing the seven keys (other row splits, columns, the 83- vs 84-token parse)
- treating the outputs as a BIP39 mnemonic to derive a wallet. BAR/CAN/FEE is only 3 words, and a 12-word checksum test is in astra's audit.
- other KDFs (PBKDF2, scrypt)
- using the outputs as an instruction for another step

The controls confirm that the construction is unusual as a *word-prefix* statistic (2 of 2,000). They say nothing about whether it is intended.

## Files

| File | Contents |
|---|---|
| `run_seven_key_bifid.py` | `prepare` / `run`; imports the helpers from `../2026-09-13_zero_envelopes/run_zero_envelopes.py` |
| `manifest.json` | pre-registration, hashes, counts, acceptance rules |
| `candidates.json` | the 200 control DBBIs; every unique text with its real-DBBI labels and how many controls produced it |
| `results.json` | every pad-valid hit with a plaintext preview; tallies by group × envelope × derivation |
| `run_log.txt` | console output of `run` |

## Verification

```
python run_seven_key_bifid.py prepare   # elapsed 5.4 s; all fidelity asserts pass
python run_seven_key_bifid.py run       # {"key_matches": 0, "inspect": 11, "pad_hits": 4246, "elapsed_s": 155.5}
```

- Of the 11 "inspect" rows, 10 are control pad-2 hits and 1 is the real pad-2 hit above.
- None passed the text gate (printable ≥ 0.95 and letters ≥ 0.65).
- Read-only sources: `D:\astra\gsmg-io-5btc-puzzle\analysis\mnemonic-model-audit.json` (the eligible positions and histogram) and `D:\astra\.firecrawl\bip39-english-words-20260905.md`. Both mtimes are unchanged (2026-09-05).
