# Doc 116: the Telegram export, in the repository and audited

26 September 2026. The full export of the "GSMG Puzzle Solvers" supergroup
(id 1166734859) is now in `by-year/`, one Telegram JSON file per calendar year,
2019 through 2026. Earlier editions of the dossier cited the export from memory of a
previous session (section 13 of the 25 September edition: "not available in this
session"). This doc records what the files contain and re-checks every claim the
dossier makes about them.

## 1. Inventory

Produced by `python3 claude/scripts/telegram/tg.py inventory`.

| year | rows | messages | service rows | creator messages | first id | last id | first date | last date |
|---|---:|---:|---:|---:|---:|---:|---|---|
| 2019 | 1,561 | 1,301 | 260 | 59 | 1 | 1,640 | 2019-04-20 | 2019-12-31 |
| 2020 | 2,990 | 2,692 | 298 | 91 | 1,641 | 5,278 | 2020-01-01 | 2020-12-31 |
| 2021 | 2,351 | 2,280 | 71 | 64 | 5,279 | 8,050 | 2021-01-03 | 2021-12-31 |
| 2022 | 228 | 214 | 14 | 9 | 8,051 | 8,321 | 2022-01-03 | 2022-12-25 |
| 2023 | 8,587 | 8,462 | 125 | 81 | 8,322 | 17,966 | 2023-01-01 | 2023-12-31 |
| 2024 | 14,237 | 13,891 | 346 | 82 | 17,967 | 34,956 | 2024-01-01 | 2024-12-31 |
| 2025 | 15,946 | 15,536 | 410 | 22 | 34,957 | 53,348 | 2025-01-01 | 2025-12-31 |
| 2026 | 17,463 | 16,975 | 488 | 84 | 53,349 | 73,560 | 2026-01-01 | 2026-09-25 |
| total | 63,363 | 61,351 | 2,012 | 492 | 1 | 73,560 | | |

Facts about the files:

- Each file is a standard Telegram Desktop JSON export (`name`, `type`, `id`,
  `messages`). The year files partition one continuous id space with no overlap and
  no duplicate ids; concatenating their `messages` arrays in year order reproduces
  the full history.
- 10,197 ids in 1..73,560 are absent. Those are deleted messages; Telegram never
  reuses an id. The export ends at #73560 on 2026-09-25.
- Media is not included ("File not included" placeholders), but file names, sizes,
  MIME types and dimensions are. So #8310's `image_2022-12-11_07-09-14.png`
  (377 x 499, 146,396 bytes) is recorded even though the image itself is not.
- Reply links are present as `reply_to_message_id`. Text arrives either as a string
  or as a list of entity fragments; `tg.text()` flattens both.
- The creator is one account, `user9815232`, display name "Jrk Bgrt" throughout
  (SoWut is his handle on the site and the name people address him by in chat). He
  posted exactly **492** messages, the count the dossier's section 8 uses.

## 2. Citation audit of the dossier

Run with `python3 claude/scripts/telegram/tg.py audit GSMG-PUZZLE-DOSSIER.md`, then
a second pass that compares quoted text and reply links.

**Every id resolves.** The dossier cites 108 distinct message ids (the regex also
catches a "#0" that is not a message). All 108 exist in the export and none is a
service row.

**Every quoted creator line matches the export text.** Sections 8.2 to 8.6 were
checked quote by quote. The only lines the automatic check flagged were paraphrases
of the *parent* message beside a creator id, and each parent was read and confirmed:
#32600 (ASCII 127), #7831 (encrypted private key stored online), #4623 (private key
or seed phrase), #66958 (waiting for a "NOTE: that is a hint" moment), #5952
(hundred FOUR), #9605 (another URL), #2911 (PK in the last cipher of 3.2), #23155
(one or a zero), #1648 to #1703 (the cake and the dessert).

**Every reply link in section 8.1 is as stated.** 17 of the 20 endorsement pairs
carry an explicit `reply_to_message_id` matching the dossier's parent. The three
without a link (#66588 "Yes", #4696 "Correct", #70325 🤐) are answered by the
immediately preceding non-creator message, exactly as the section's method says
(#66587, #4695, #70324). The 60298 to 60317 "Bingo" run reads as the dossier
transcribes it, including the unrelated #60311 between gnomad's line and the Bingo.

**Both binary decodes reproduce from the files.**

- #8446: 1,288 bits, 161 bytes; the whole stream reversed reads
  `yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyangwewontgiveaway`
  `thepassworditsinfrontofyoureyesbutyourenotseeingitverylaststepisatruegiveaway`
  `promised`, byte for byte the section 7.1 text.
- #53342: 77 bytes, forward, `Happy new year! Make the best of everything. Oh, and
  here's a "tiny hint" <3.`, the section 7.3 text. The five dot messages are #53335,
  #53336, #53338, #53339, #53341 (1 to 5 dots, 22:15 to 22:19 on 2025-12-31); #53337
  and #53340 are deleted.

**One correction.** Section 8.6 files "Have you tried the purple pill already?" and
"Candy flipping" both under #17891. The first is #17891; "Candy flipping into 2024
;-)" is #17893, two messages later. The dossier now reads #17891 / #17893.

## 3. What the export adds, and what it does not

It adds verifiability: any future hint reading can be checked against the primary
record in one command, and the "not available in this session" caveat in section 13
is gone. It does not add new puzzle material. The 492 creator messages were already
re-read in full on 23 September (doc 103) from the same export; this session
confirmed the transcript rather than re-mining it, and ran no candidates.

`claude/116-creator-messages.txt` is the full creator transcript, one message per
line with id, timestamp, reply link and text, regenerated by
`python3 claude/scripts/telegram/tg.py creator`.

## 4. Tooling

`claude/scripts/telegram/tg.py` (standard library only):

    python3 claude/scripts/telegram/tg.py get 8446 53342     # messages by id
    python3 claude/scripts/telegram/tg.py thread 60312       # a message with its reply chain
    python3 claude/scripts/telegram/tg.py creator            # all 492 creator messages
    python3 claude/scripts/telegram/tg.py inventory          # the table above
    python3 claude/scripts/telegram/tg.py audit FILE.md      # every #id in FILE must exist

From Python: `from tg import load, text; b = load(); text(b[8446])`.
