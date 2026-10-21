# Packet results (2026-09-08)

Closed list SHA-256: `13055206d7585e75ea07d6518a126a785af3b8d0bbb159b9a3b64f5b1d4b1493`  
(`packet/password_list.json`, 55 unique strings × raw + sha256hex = 330 OpenSSL attempts)

Prize check: uncompressed pubkey of `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`. No WIF written.

## Verdict

The approved Cosmic Duality / yinyang-as-password packet **did not produce the key.** Several named mappings are now closed.

| Hypothesis | Result |
|------------|--------|
| Yinyang / YingYang / Cosmic Duality *as OpenSSL password* decrypts the Cosmic Duality blob | **Closed — no decrypt** |
| Same passwords decrypt leftover phase-3.2 AES (`U2FsdGVkX1+0Wl49…`) | **Closed — no decrypt** |
| Published 7-XOR of Salph tokens decrypts Cosmic Duality | **Reproduced** (1327 bytes, SHA-256 `4f7a1e4e…081`) |
| That 1327-byte plaintext, its SHA-256, or first/last 32 bytes is the `1GSMG` private key | **Closed — no match** |
| Yinyang **is** the Cosmic Duality AES decrypt | **Not supported.** Jrk 2025-04-28 `#39224`: yinyang not reached, then hours. The 7-XOR decrypt is a known published object; the wallet is still funded; 2026-05-28 `#63957` puzzle still valid. Decrypting CD is not the short final phase. |

Three PKCS#7 “successes” on the **79-byte Salph fragment** were binary garbage (padding collisions, expected ~1/256). Not readable, not a prize match. Discarded.

## What ran

- Blobs: `cosmic_duality.txt` (1344 B ciphertext, SHA-256 `b1895055…9805`), leftover 3.2 (96 B), Salph small AES (96 B).
- Passwords: yinyang family, Cosmic Duality names, roadmap tokens (`matrixsumlist`, `lastwordsbeforearchichoice`, …), Jrk stage hashes, `HASHTHETEXT`, `THEMATRIXHASYOU`, `reinserting the prime basics`. No FAED slices, no `0x7B9ECC`, no `{1,4,21}`.
- 7-XOR method is the **already-published** writeup (`matrixsumlist ⊕ enter ⊕ lastwordsbeforearchichoice ⊕ thispassword ⊕ matrixsumlist ⊕ yourlastcommand ⊕ secondanswer` as KDF password). Not a new operand.

## Extra door (20%)

`puzzle.png` (first piece, 1048×1556): yellow **50400**, blue **96791**, red-ish **18606**. That is a pixel count of the published image, **not** a hashed door find. `#1710` is logged; `{1,4,21}` was not used.

## Next fork (from `NEXT_BEST_MOVE.md` if CD list fails)

Leftover 3.2 AES with this same closed list **already failed**. A new 3.2 list would have to be a **different closed operation** on yellow/blue primes from piece 1, written down before the next run — not an open chat. That list was run as packet 2 (`RESULTS_LEFTOVER32.md`) and also failed.

Hint sheet: `packet/HINT_SHEET.md`. Machine log: `packet/out/results.json`.
