# GSMG Puzzle Solvers — Group Communication Analysis

**Group:** Telegram private supergroup `GSMG Puzzle Solvers` (id 1166734859)  
**Corpus:** yearly Desktop JSON exports, 2019-04-20 through 2026-09-08  
**Size:** 59,401 chat messages + 1,948 service events; 702 unique posting accounts  
**Subject of the group:** the still-unclaimed GSMG.IO 5 BTC puzzle  

This report identifies communication patterns that have kept work looping on the same open stages rather than closing them. Counts below are from a full parse of the eight yearly transcripts (`analysis/parse_chats.py`, `analysis/analyze.py`). Keyword hits use case-insensitive regular expressions; they measure *discussion volume*, not whether a claim is true.

For what Jrk’s own messages imply was **left unfinished** (extra door on piece 1, primes/zeroing, yinyang as a short final phase), see `WHAT_THE_GROUP_MISSED.md`.

---

## Corpus snapshot

| Year | Chat messages | Unique posters | Top-5 share | YoY poster retention into next year |
|------|---------------|----------------|-------------|-------------------------------------|
| 2019 | 1,301 | 75 | 38% | 24% (18/75) |
| 2020 | 2,692 | 88 | 42% | 44% (39/88) |
| 2021 | 2,280 | 73 | 46% | 29% (21/73) |
| 2022 | **214** | **26** | **76%** | 65% (17/26) |
| 2023 | 8,462 | 86 | 58% | 58% (50/86) |
| 2024 | 13,891 | 185 | 43% | 49% (90/185) |
| 2025 | 15,544 | 258 | 31% | 38% (99/258) |
| 2026* | 15,017 | 277 | 35% | — |

\*2026 file ends 8 September, not year-end.

89% of all chat messages (52,914 / 59,401) were posted in 2023–2026, *after* the group had already been stalled for years on the same artifacts. Message volume is therefore a poor proxy for progress.

---

## Key findings

### 1. The same unsolved stages are reopened for 5–7 years and are never formally closed

The group has no durable “open / closed / falsified” record. Threads that first appear in 2019–2021 are still treated as live work on the last day of the export.

| Thread | First hit | Last hit | Mentions | Notes |
|--------|-----------|----------|----------|--------|
| Phase 3.2 | 2019-06-08 | 2026-09-08 | 720 | Already called “gibberish” in 2020 |
| Salphaseion / “salph” | 2021-02-16 | 2026-09-08 | 1,155 | Dominant 2023–2026 stall point |
| DBBI | 2021-05-14 | 2026-09-08 | 693 | Nested inside Salphaseion |
| FAED | 2021-03-24 | 2026-09-08 | 669 | Nested inside Salphaseion |
| Meganigma | 2020-11-08 | 2026-09-07 | 78 | Periodically rediscovered |
| Explicit “stuck at/on/in” | 2019-04-23 | 2026-09-04 | 146 | Meta-commentary on the stall |
| Hint-seeking language | 2019–2026 | — | 2,942 | 93% of hits are 2023–2026 |

**Evidence**

- 2020-02-22 `#1841`: “Anyone solved the gibberish in 3.2?”
- 2023-08-03 `#8796` (Jrk Bgrt, puzzle author): “Actually, the hardest part is done.” Members were still quoting this in 2026 as a reason Salphaseion “should be easy,” which it was not treated as being.
- 2025-04-28 `#39242` (X): “@SoWut thats where we are stuck for years. just tell us they are decipherable or not so we dont waste another 6 years..”
- 2026-01-17 `#57385` (X): “everyone is stuck at 3.2 because nobody understood the phrase 'reinserting prime basics'”
- 2026-01-24 `#58592`: “Has anyone solved the 'blob dbbi...' issue in Salphaseion? Has everyone given up, and has the puzzle been stuck in the same place for years?”
- 2026-02-09 `#59756–#59758`: a member posts an inventory of remaining AES/Salphaseion blobs, then asks the group to “confirm that this is still unsolved and a current task.”
- 2026-09-08 `#71205` (last day of the corpus): “but since 3.2 is not solved; until it is; we wont know if we are missing something needed there and failing salphaseion because of it.”

The 3.2-versus-Salphaseion fork is therefore still unresolved after seven years. Parallel artifacts (DBBI, FAED, leftover AES blobs, the rabbit/QR track) are discussed as if they might each be “the” current task, with no recorded group decision.

**Confidence: high.** First/last timestamps and raw mention counts are mechanical. The interpretation that these threads are *unclosed* (not merely mentioned) is supported by repeated “still unsolved / current task?” questions in 2026.

---

### 2. Participation is both concentrated and unstable, so institutional memory keeps resetting

Two facts sit together:

1. **Concentration.** Overall Gini coefficient on messages-per-author is **0.833**. Seven accounts produce 25% of messages; 22 produce 50%; 90 produce 80%. The lifetime top five accounts produce 21% of all chat.
2. **Churn.** 486 of 702 posters (69%) appear in only one calendar year. Year-to-year poster retention is typically 24–49% (the 2022→2023 rate looks high only because the 2022 cohort was already tiny). Only **two** accounts posted in all eight years; only 30 accounts posted in four or more years.

The people who dominate a given year are almost never the people who dominated the year before:

| Year | Top 3 posters (share of that year) |
|------|-------------------------------------|
| 2019 | 0xColombo, phacyh, “....” |
| 2020 | nieods, Legik, Lazy Prophet |
| 2021 | Saber, Janusz Baran, Zil |
| 2022 | Saber, barrystyle, stranger |
| 2023 | ArchOptic, Unknown, Unknown (three accounts, 51% combined) |
| 2024 | Unknown, X, Unknown |
| 2025 | P K, Cereal Killer, X |
| 2026 | Dasharo (11%), 0b1one (11%), Denis Golovkin |

Several high-volume voices are single-year spikes (P K: 1,069 messages in 2025 only; Unknown `6953392511`: 988 in 2024 only). Deleted-account labels (“Unknown”) are common among those spikes, so later readers cannot even attach a stable identity to a large fraction of past work.

2022 is the extreme case of disengagement: 214 messages from 26 posters, versus 2,280 the year before. Monthly volume had already collapsed in mid-2021 (June–November 2021: 105 messages total). The last 2022 line in the export is barrystyle, 2022-12-25 `#8321`: “no closer..”

The group then refilled in August 2023 (3,418 messages that month alone) after author posts on 2023-08-03, and never rebuilt a stable core. 1,802 join events were logged against only 35 leave/remove events; Telegram under-reports leaves, but the join flood is real. Newcomers continue to ask where to start through 2024–2026.

**Evidence**

- 2022-02-03 `#8061` (0xColombo), during the quiet year: “Please give us additional hint for SalPhaseIon”
- 2022-04-09 `#8068` (Legik): “how to understand what the salphaseion text means, where to read what it is?”
- 2024-03-04 `#21771` (Adam Rajnoha): still asking whether Salphaseion is even “the next stage” after 3.2.2, or an alternate route.
- 2026-08-24 `#69851` (Suppa): a new-to-the-work member is “stuck at SalPhaseIon like everyone else” and asks veterans to recap Jrk’s prime-basics comments.

**Confidence: high** for concentration, churn, and top-poster rotation (direct counts). **Medium-high** for the causal claim that churn *causes* repeated re-derivation: that is inferred from newcomer questions plus “already tried” language (57 hits, 2019-04-20 through 2026-09-04), not from a controlled comparison.

---

### 3. Hint-dependence on the author has replaced group decision-making

Jrk Bgrt (`user9815232`) is present across the whole span (492 messages, 2019-04-20 to 2026-09-01) but is not a working facilitator. The group generated ~2,942 hint-related messages versus Jrk’s 41 messages that themselves contain the word “hint.” 250 messages discuss Jrk/hints as an external oracle. The export contains **one** poll in seven years.

Author statements that were meant to bound the search were not converted into group rules:

- 2019-05-18 `#881`: if the key is not found in 2019, “we’ll release a tiny hint at the start of 2020, that will be the final hint.” Hints and hint-requests continued through 2026.
- 2019-05-18 `#898`: “No hints after stage 2”
- 2019-09-04 `#1448`: “Still no hints ;-)”
- 2023-08-03 `#8774` / `#8796`: “Are you really looking for just the btc...?” and “Actually, the hardest part is done.” Those two lines were still being exegeted three years later instead of being used to retire a hypothesis.

When the author is quiet, work does not switch to a decision process; it waits or fragments. 2022 is the waiting state. 2023–2026 is the fragmented state: many competing encodings, almost no recorded “we agree this is falsified.”

**Evidence**

- 2026-01-09 `#55405` (VITOR LIMA): “We already have dozens of suggestions, and none of them work.”
- 2026-05-24 `#63765` (Artem): “the community has been going in circles for years”
- 2026-06-01 `#64419` (Nietzsch): “Has any progress been made so far? Or stuck as usual?”
- 2026-08-23 `#69719`: a member is still hunting a 2019-era Slack “tiny hint” rather than closing a current test.

**Confidence: high** that hint-talk dominates and that formal decisions (polls, written closures) are nearly absent. **Medium** that author silence *causes* the stall; the puzzle difficulty is a confounder. The communication failure is the lack of a substitute process when the author is not answering.

---

### 4. Tone and conflict scale with volume; moderation does not

Lexicon hits (insults, “troll/spam/ban him,” “nobody cares,” “gibberish” as dismissal, etc.) are an imperfect proxy — early “stupid/gibberish” hits are often about ciphertext, not people — but the *trend* is clear:

| Year | Conflict-lexicon hits | Rate | “troll*” | Ban/moderation talk | Scam/phishing talk |
|------|----------------------:|-----:|---------:|--------------------:|-------------------:|
| 2019 | 16 | 1.2% | 4 | 4 | 2 |
| 2020 | 28 | 1.0% | 3 | 6 | 5 |
| 2021 | 42 | 1.8% | 6 | 6 | 13 |
| 2022 | 2 | 0.9% | 0 | 0 | 5 |
| 2023 | 141 | 1.7% | 12 | 6 | 18 |
| 2024 | 280 | 2.0% | **63** | 44 | **74** |
| 2025 | 261 | 1.7% | 26 | **100** | 56 |
| 2026* | 276 | 1.8% | 25 | 55 | 54 |

Friction is interpersonal and procedural, not a single feud:

- **Spam / offtopic vs. puzzle-only.** 2026-01-11 `#56488–#56495` (Martín): GIF spam “should be something to be banned. But then again, admin doesn't care... nobody cares” / “this is why the channel is doomed.”
- **Named-person loops.** 2026-01-18 `#57797` (Prime): “Here we go again with Bob. Please ban him Trin. We're making good progress here and he is just crying about Gudic.” Ban requests appear from 2020-02-25 (`#2027`, spam/rude DMs) through 2026 with no visible standing rule.
- **Theory disputes turning personal.** DBBI/FAED threads in 2026 include “You’re stuck, bro… I’m going to stop wasting my time” versus “you are also stuck trying to make sense of gibberish text after some heavy assumptions.”
- **Exit to DMs.** 2026-05-28 `#64105` (Nano): “I'm going to retire from this chat and finish solving. If anyone is stuck and needs a legit hand then my DMs are open.” Work that leaves the main channel cannot be falsified by the group.

Passive-aggressive recycling (“here we go again,” “as usual,” “already discussed”) also rises with volume (1 hit in 2019 vs. 62 in 2026).

**Confidence: high** for the volume trend and for the existence of repeated moderation complaints. **Medium** for “admin vacuum” as a structural cause: the export has few service-visible kicks (35 removed/kicked events vs. 1,802 joins), which is consistent with light moderation but is not a full moderator log.

---

### 5. Decision fatigue: activity without an oracle, a closer, or a shared “current task”

After 2023 the group is busy, not decisive. Markers:

- **No closure ritual.** One poll in 59k messages. Failed tests are restated months later as fresh ideas (“already tried” / “none of them work”).
- **No shared pointer to “where we are.”** 2024-11-14 `#30008` (RB): “where are we now, where we hadn't been the last 40+ month?” 2025-06-04 `#42646` (K): “The question is, where are we now?”
- **Unfalsifiable progress claims.** “Progress/found/solved/breakthrough” language rises from 13 hits in 2019 to 269 in 2026, while stuck-language stays flat at ~115 hits/year in 2023–2026. Claims are not matched to a public checksum-of-solution convention until individuals start asking for SHA256s of claimed Salphaseion solves (2026).
- **External ground truth is decaying.** 2026-05-03 `#62355` (Sparky) asks whether old hints are obsolete “after the official website vanishes.” 2026-09-04 `#70924`: phase websites are already offline; Jrk did not reply.
- **2023-08 reactivation did not produce a new stage.** Volume jumped two orders of magnitude; Salphaseion/3.2/DBBI/FAED mention counts jumped with it. The last day of the corpus is still arguing whether 3.2 blocks Salphaseion.

The 2022 trough and the 2023–2026 flood are the same failure mode at two temperatures: without a way to retire hypotheses, people either leave or talk more.

**Confidence: high** that decision infrastructure is missing (poll count, repeated “where are we,” last-day 3.2/Salph fork). **Medium** on any single “correct current task”; this report does not judge the puzzle, only that the group cannot agree and cannot record disagreement as a closed test.

---

## Recommendations

These are process changes. They do not require the author to drop a new hint.

1. **Publish a one-page stage board and pin it.** Columns: artifact (Phase 3.2 AES blob, Salphaseion, DBBI, FAED, Meganigma, rabbit/QR, other), status (`open` / `blocked-on` / `falsified` / `solved-with-hash`), owner, last test, link to write-up. Update it when someone posts “is this still a current task?” rather than re-litigating in-thread. The 2026-02-09 inventory (`#59756`) is a usable first draft.

2. **Require a falsification log for new theories.** A hypothesis is allowed in the main channel only if it states: input, method, expected output, actual output, and a one-line “why this is not last month’s DBBI/FAED/3.2 variant.” Failed tests go to a searchable list (GitHub issue, pinned message, or bot). This directly attacks the “dozens of suggestions, none work” / “already tried” loop.

3. **Split traffic by function.** Minimum: `#current-tests` (only attempts with results), `#theory` (speculation), `#onboarding` (where to start + links to Naddiseo-style writeups), `#offtopic`. GIF/meme volume is already cited as a cohesion problem (`#56488`).

4. **Appoint a rotating closer, not a genius.** One weekly volunteer posts: what was tested, what is still open, what is parked. Do not wait for Jrk. Treat author messages as *inputs* to the board, not as a substitute for it. When the author is silent, the closer still ships the weekly note.

5. **Onboarding packet for the 1,800-join inflow.** Ten-line “start here”: solved stages, open artifacts, “do not brute-force X,” links to existing decryptions. 69% of posters never return for a second year; reducing re-ask cost is the highest-leverage cohesion move.

6. **Moderation rule in writing.** Spam/scam/impersonation get removed; interpersonal pile-ons get moved to a thread; repeated offtopic after a warning gets muted. Name the moderator(s). Ban-request drama (`#57797`) is currently a substitute for policy.

7. **Keep claimed solves in-channel as hashes.** The 2026 request to post SHA256 of purported Salphaseion solutions should be standing procedure. It lets the group verify without forcing full spoilers, and it stops unverifiable “I solved it / DM me” exits (`#64105`, `#8070`).

8. **Do not use raw message volume as morale.** After 2023 the channel is loud. A useful KPI is “hypotheses closed this month,” not “messages this month.”

---

## Confidence summary

| # | Finding | Evidence strength |
|---|---------|-------------------|
| 1 | Unsolved 3.2 / Salphaseion / DBBI / FAED threads never close | **High** — multi-year spans, 2026 inventories, last-day fork still open |
| 2 | Concentration + churn destroy memory | **High** (counts); causal link to rework **medium-high** |
| 3 | Author-hint bottleneck, almost no group decisions | **High** on the pattern; **medium** as sole cause of the stall |
| 4 | Conflict and moderation complaints scale with the 2023–26 influx | **High** on trend; **medium** on admin-intent |
| 5 | Decision fatigue: activity without closure | **High** on missing process; puzzle-intrinsic difficulty is a confounder |

---

## Method and limits

- Parsed all `[#id] HH:MM:SS Name (user…)` blocks after each file’s `TRANSCRIPT` marker; service lines counted separately.
- Authors are the export’s normalised display names. Many high-volume accounts render as `Unknown` (deleted Telegram profiles). User ids are stable; names are not.
- Topic counts are regex hits on message text, not thread clusters. A long paste that names “3.2” and “salph” increments both. Attachment binaries are not in the export.
- Conflict/indecision lexicons over-count puzzle-about-ciphertext uses of words like “gibberish” and under-count sarcasm with no keyword.
- Leave events are undercounted relative to joins (Telegram service-event behaviour). Retention is therefore measured from *posting* in year T and T+1, which is the more relevant cohesion metric.
- This is a communication analysis, not a solve write-up. No claim is made about which remaining artifact is the correct next stage.

Reproducible stats: `analysis/stats.json`, generated by `python3 analysis/parse_chats.py && python3 analysis/analyze.py`.
