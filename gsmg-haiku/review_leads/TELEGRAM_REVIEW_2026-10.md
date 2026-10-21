# Telegram export review (ChatExport_2026-10-08)

Source: `ChatExport_2026-10-08/result.json`, 64,742 messages, 2019-04-20 to 2026-10-08. Creator account: "Jrk Bgrt" (the "@SoWut" the chat replies to). Read-only review, no key or passphrase tested here unless stated.

This file covers the recent window only. The second pass over 819 selected entries (492 direct creator messages and 327 forwards, 2019–2026) is in [CREATOR_CHAT_REVIEW_2026-10b.md](CREATOR_CHAT_REVIEW_2026-10b.md).

## Creator posts since the last recorded hint (2026-07-12 onward)

| date (UTC, from `date_unixtime`; corrected 2026-10-14, the 07-12 rows were local dates) | message | status |
|---|---|---|
| 2026-07-13 (#66568) | "I have a hidden laptop which I haven't touched in years. On that thing... is the actual answer...." | new to memory; claim, unverified |
| 2026-07-13 (#66595) | "(And yes, the btc is still available before you fire any questions)." | consistent with chain: target holds 1.25636967 BTC; sink `17ucy1K9…` holds 3.75055856 BTC unspent (checked 2026-10-08) |
| 2026-07-13 (#66542) | "In 2029, all btc on old addresses might be cracked (cmiiw)." | new; quantum remark, not a puzzle lead by itself |
| 2026-07-16 (#66903) | "Well, it's hidden in a room with a hidden door." | new; ambiguous |
| 2026-07-16 (#66909) | BIP 360 "piggy bank" explanation (quantum, hidden lock) | new; links the quantum remark to old-address exposure |
| 2026-09-01 (#70307, #70309) | "Pfff. Coincidence." / "...the monstrosity I decided to build a few years ago" | no puzzle content |

Items already in memory (2026-07 "5 BTC was never the actual prize", "secret in my head") are confirmed here, with the exact wording.

## On-chain facts confirmed by the chat

- Target public key: the chat reports an exposed uncompressed key `04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559`. **Verified:** hash160 of this key = `a9553269572a317e39f0f518cb87c1a0ee1dbae4`, the target's hash160. The key is exposed because the target has been spent from.
- Sink `17ucy1K9…` holds 3.75055856 BTC unspent. **Verified** (mempool.space, 2026-10-08).

## Claims that conflict or are unverified

- **Checkpoint `4f7a1e4e…`** (SHA-256 of the 1327-byte Cosmic Duality plaintext). 2026-08-08 post by MrNobody: first said it could not be reproduced, then retracted and said rickluminari1's derivation reproduces it (password = 32 raw bytes via MD5 KDF). 2026-09-03: a solver reports "salt 2d3f6fe06dc950e6 · 1327B · sha 4f7a1e4e… reproduced". 2026-09-09 (peter chen): "Community checkpoint 4f7a1e4e proven incorrect — our reproducible result is a5502d09." **Not verified here.** The two reproductions disagree; treat the checkpoint as contested until the two derivations are compared byte for byte.
- **"Yin-yang is a Coldcard Mk2"** (Ciprian, 2026-08-01). Unverified claim, no derivation posted in the export.
- **"We got a private key from something"** (TekniskTrading, 2026-08-08). Unverified; no key or address posted.
- **"Jrk endorsed barrystyle's find (Cosmic Duality Book Page - Life and Death)"** (MrNobody, 2026-08-08). The creator's own post confirming this is not in the export. Unverified.
- **"Solved the puzzle"** claims (Ciprian; "Bitcoin Puzzle #135 SOLVED" by FekoAii, which is a different puzzle). Not accepted.
- **"Shared 2 days on yin-yang"** and **"Two eyes at first and last slot"** (sniper, 2026-08-10/11): conjecture, no result.

## Scam and noise to ignore

- "Double shot of Jameson for Jrk" (2026-01 to 2026-02): asks people to send funds to a "neo wallet" for a "gift card" and "door opening". This is a scam pattern, not a puzzle lead. Do not send funds to any address posted in the chat.
- Repeated "solved" / "will be solved within 1-2 years" / "Morpheus" posts: no content.

## Relevant to the open analysis

- The "exposed public key" line is the only on-chain-verified new fact in the export. The public key is on-chain, so any attack on the key (key-size or weak-key search) can use it directly. Whether a search over that key space is feasible has not been assessed here. The brainwallet test (`review_leads/BRAINWALLET_CANDIDATES.md`) compares hash160 and so does not need the pubkey, but it gives the same result as checking the pubkey.
- The checkpoint dispute (4f7a1e4e vs a5502d09) affects any work anchored to the Cosmic Duality blob. Compare the two derivations before building on either.
