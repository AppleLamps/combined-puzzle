# 17 - State refresh: what changed outside this folder, and what it corrects

**Status (2026-11-10): UNSOLVED.** The prize is unspent, the creator has not posted since 2026-09-01
(checked in an export that runs to 2026-11-09),
and the live puzzle pages are byte-for-byte what this folder holds. This file records a check of every
outside source the ledger depends on and the corrections that follow. Evidence is in
`runs/2026-11-10_state_refresh/`.

## 1. Summary

| Source | State on 2026-11-10 | Effect on the ledger |
|---|---|---|
| Source repository `AppleLamps/GSMG-CLEAN` | The snapshot commit `795f85d` is still the head of its branch. One other branch, `codex/faed-anchor-dbbi-20260915`, was never merged | Its two runs and four tools are imported (section 2) |
| The other nine source repositories | Last pushed 2026-10-21, the day the snapshots were taken | None |
| Community repository `puzzlehunt/gsmgio-5btc-puzzle` | Head `fb92dd1`, unchanged since 2021; equal to `notes/source_upstream` | None |
| Community walkthrough, as carried in `AppleLamps/gsmgio-5btc-puzzle` | Updated 2026-11-01 | Saved as `reference_texts/community_walkthrough_2026-11-01.md`. Its on-chain section corrects 01 section 9 (section 3) |
| Prize address | 125,649,674 sat, 129 transactions, 2 spends, last activity 2026-10-13 (inbound dust) | 01 section 9 updated |
| Better Half address | 375,055,856 sat, 45 transactions, never spent | Unchanged |
| Chat | Newest export runs to 2026-11-09 (`telegram/ChatExport_2026-11-09_result.json`, section 9): 7,562 messages since the ledger's September export, none from the creator, no creator text changed | Saved in `telegram/`; 02 updated (sections 4 and 9) |
| Live site | `/puzzle`, `/theseedisplanted` and the SalPhaseIon page answer 200 with the saved content | 01 section 10 confirmed (section 5) |

## 2. Imported from the unmerged source branch

`codex/faed-anchor-dbbi-20260915` (2026-09-15) holds two bounded tests that the snapshot lacked. Both
are null and both are now in this folder with their tools; the tests pass here.

| Run | What it tested | Result as reported there |
|---|---|---|
| `runs/2026-09-15_dbbi_framing_architect/` | The 23 prime markers as framing only: gap lengths, last cells of each gap and whole-gap reversals used as row-local indexes into the Architect edit tables (83-cell parse) | 518 candidates, 0 exact matches, 0 instruction hits; best score reached by 471 of 5,000 shuffled controls |
| `runs/2026-09-15_faed_anchor_dbbi/` | FAED letters at indexes 5, 479 and 484, with neighbourhoods up to radius 12, written into DBBI's prime cells by five arithmetic modes | 1,040 candidates, 0 known-string matches; Bifid continuation 15 against a control maximum of 21 |

These predate the working rules of 16 and are recorded as that branch reports them. They overlap the
gap-sum run of 16 section 6 in operand, not in operation.

## 3. On-chain facts: what 01 section 9 had wrong or lacked

`python tools/check_chain_state.py` re-reads the chain from a public explorer and re-derives every
address below from first principles. Output: `runs/2026-11-10_state_refresh/chain_state.json`, raw
transaction lists in `chain_raw/`.

**3.1 The prize is where it was.** Half holds 125,649,674 sat (01 recorded 125,635,374; the
difference is solver dust). It has signed 6 inputs in 2 transactions, the 2020 and 2024 halvings.
81 transactions that touch it carry an `OP_RETURN`; none of them spends from it.

**3.2 A second address sent the checkpoint payments.** `3GSMG24TujqfMJG1kQoBX18DzJHQLeJYMK` paid,
with a message each:

| Date | Block | Paid to | Its private key | Message |
|---|---|---|---|---|
| 2020-03-24 | 622762 | `1GyT5WrLYpwFkuiVoPDJZa1Q6jtjbjuBff` | sha256 of the prize address as text | `GSMG.io: do you beleive me you need it?` |
| 2020-03-24 | 622762 | `1Jqq37KkZEt4F3Dt6qXdtyiMEFBBdawbkJ` | sha256 of `causality` | `GSMG.io: Right, this is causality` |
| 2020-03-24 | 622766 | `18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc` | sha256 of the 149 checkerboard digits | `GSMG.io: part of the cipher` |
| 2020-03-24 | 622767 | `1AD2wfwXukZ1kUAy848hTQQ72aSBZPB75r` | sha256 of the Phase 1 answer | `GSMG.io: are you sure?` |
| 2020-03-24 | 622767 | `1K23RS1y2fnuZRkhw5nUpFr5Jk5WN11Zeq` | sha256 of the Phase 3.2 answer | `GSMG.io: phase3.2 pass OK` |
| 2020-03-24 | 622774 | `1M5ypvDbp124ZtKPbg3GJg1JqNs1x7TPoN` | sha256 of the seven-part Phase 3 answer | `GSMG.io: You are here because 227 chars were correct` |
| 2020-04-03 | 624209 | `148XH2YBmLr4oAJXQcG84FpNYoBmqnVPHQ` | the URL as a 192-bit integer | `Good job, Neo!` |
| 2020-04-03 | 624209 | `13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp` | the same bits reversed | `Good job, Neo!` |
| 2020-04-07 | 624768 | `1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9` | none (3.4) | no message |
| 2020-05-11 | 630001 | the prize address | | `Halving` |
| 2021-07-18 | 691563 | four addresses | P+G, P-G, 2P and P/2 of the prize public key | `GSMG.io neighbors, half and double` |

All eight checkpoint keys and all four neighbour addresses re-derive exactly. 01 listed four of the
eight; the other four (`1Jqq37`, `1K23RS`, `1M5ypv`, `148XH2`) are added to `tools/oracles.py` and to
its self-test. The seven-part answer is 227 characters, as the message says.

**3.3 Whose address is it.** Two facts point in opposite directions and both stay on the record.

- *For the creator:* the `Halving` payment and the prize key's own halving transaction are in the
  same block, 630,001, and the second spends the 700 sat output of the first. The prize key therefore
  signed a spend of an output that was still unconfirmed, which a wallet does for its own payments
  and not, by default, for a stranger's. Messages on 2020-03-24 also name facts few solvers had then
  (the Phase 3.2 answer, the 149 digits, "227 chars").
- *Against:* asked in chat, the creator agreed that "the blockchain messages are not his and are not
  part of the puzzle" (#12653 "Correct", replying to #12580, 2023-08-29).
- At the 2020 halving the prize address held four outputs and all four were swept, so the sweep was
  not selective. That weakens the first argument but does not remove the same-block point.

05 and 06 call the claim "3GSMG24 creator-signed" unsupported. That stays true in its literal sense:
nothing is signed by the prize key. The same-block spend is new evidence that the two wallets had one
operator. Either way the messages confirm answers that were already known and add no operand.

**3.4 `1NULY7...` is a tool's tip address, not a third door.** 01 says so and it holds, with more
behind it now. The address is hard-coded as `Tips:` in the source of a public Pollard-kangaroo solver
(for example `Mezantrop74/VanitySearch-Kangaroo-Hybrid`, `main.cpp` and `solver.py`). Its only
transaction ever is the 1,050 sat from `3GSMG24` on 2020-04-07. A third-party write-up
(`floflo777/open-crypto-puzzles`) treats it as "the third door" with an unknown preimage and plans
dictionary passes against it; there is no preimage to find. What the payment means is open: a tip to
the author of a tool that searches a key in a known range, sent from the checkpoint wallet four days
after the two `Good job, Neo!` payments.

**3.5 "Half and double".** The 2021 payment goes to the uncompressed addresses of P+G, P-G, 2P and
P/2. It shows that the sender had the prize public key, which had been on chain since the 2020
halving, and nothing more: anyone can compute those four points. The phrase echoes "Half and Better
Half" in the checkerboard message. No test in any directory has used it as an operand in a way that
checks itself, and none is proposed here.

## 4. Creator messages

No creator message is newer than #70377 (2026-09-01) in any export, and none of the 492 creator texts
differs between the 2026-09-13 and 2026-10-08 exports. Three forwards of old creator posts appear in
the new messages (#71762, #71913, #73195); they repeat known text.

Creator messages cited by the community walkthrough and missing from 02 until now:

| id | Date | Text | Note |
|---|---|---|---|
| #660 | 2019-05-08 | "Apparently somebody managed to get into Phase 3" | Timeline |
| #7418 | 2021-04-16 | "Good point" | Reply to #7416 (a solver): "Go to the first puzzle piece (image) and hash all the text you see. But mind that the author is a bit picky what he considers to be text." |
| #9636 | 2023-08-06 | "I have no clue." | Reply to #9634 |
| #12653 | 2023-08-29 | "Correct" | Reply to #12580: "Jrk has stated that the blockchain messages are not his and are not part of the puzzle". 02 listed the id without its referent |
| #66584 | 2026-07-12 | "Welcome. I feel it a bit off knowing the url (and thus the original puzzle) is 'gone'." | The site was back by 2026-08-18 (#69025, a solver) |
| #66592 | 2026-07-12 | "...I held quite a secret in my head which I seriously wanted to share with the planet... for those who can understand what I meant..." | |
| #66595 | 2026-07-12 | "(And yes, the btc is still available before you fire any questions)." | |

Message #7616 (2021-05-06), which first posted the exact text to hash, came from a since-deleted solver
account, not from the creator.

The 569 message ids present in the September export and absent from the October one are deletions by
their authors; the September export in `telegram/` keeps them.

## 5. Live site

Fetched with plain GET requests on 2026-11-10; nothing was submitted.

| Path | Result |
|---|---|
| `/puzzle` | 29,931 bytes, sha256 `38125bbd...`, identical to `originals/poster/puzzle.png` |
| `/theseedisplanted` | 832 bytes, as in 01 section 10 |
| `/89727c59...` (SalPhaseIon) | 4,536 bytes; both textareas equal the saved original, and the letter stream equals `data/salphaseion_compact_1075.txt` |
| `/` | 35,785 bytes; still reads "The lights are off. Nine years of chaos ended. One mystery remains. Follow the white rabbit" |

## 6. Corrections applied elsewhere

- 01 section 9 and section 10: dated update notes pointing here.
- 02: the seven creator messages above.
- 05: the `3GSMG24` and `1NULY7` entries qualified; the note that a `floflo777` repository was invented
  by an AI is qualified, since `floflo777/open-crypto-puzzles` exists.
- `gsmg-1.2-2/CANONICAL_NOTICE.md`: the row that called the on-chain relation table "not puzzle
  material" is corrected to match 3.5.
- `SHA256SUMS.txt` is regenerated for the tree as it now stands. The list made on 2026-09-13 from the
  original Windows checkout is kept as `SHA256SUMS_2026-09-13.txt`.

## 7. Not done

- The Telegram media folders are still outside the repository (README, "Telegram").
- `runs/2026-09-14_source_cipher_keys/keys.json` is a Git LFS pointer in this checkout; its 110 MB
  content was not fetched and is not in the new checksum list.
- `floflo777/open-crypto-puzzles` was read only as far as its address table and first leads. It is a
  third-party summary, not a source; it was not reconciled line by line.

## 8. Reproduce

```
python tools/check_chain_state.py
python tools/oracles.py
python tools/test_audit_dbbi_framing_architect.py
python tools/test_test_faed_anchor_dbbi.py
```

## 9. Addendum: chat export to 2026-11-09

A newer export of the solvers' group was supplied after the sections above were written. It is saved
unchanged as `telegram/ChatExport_2026-11-09_result.json` (8,856 messages, ids 70304 to 80453,
2026-09-01 to 2026-11-09) and compared in `runs/2026-11-10_state_refresh/chat_state_2026-11-09.json`.

- **4,049 messages are newer than the October export. None is from the creator.** The export holds ten
  creator messages, all from 2026-09-01; the last is still #70377. It has been ten weeks.
- Seven forwards of creator posts appear after 2026-10-08. Each repeats a message already in 02 or in
  the sourcebooks (#16624, #9592, #32640, #3923, #66909 twice, #1710).
- No message text changed in the overlap with the October export. One message was deleted (#75545).
- Two solvers asked the creator direct yes/no questions about the step order and about whether FAED is
  filler (#78484 on 2026-11-01, #79291 on 2026-11-07). Neither has an answer.

Solver observations in the new messages, each checked here. None is an operation; they are recorded so
that they are not rediscovered.

| Message | Observation | Checked |
|---|---|---|
| #76294 (Marc, 2026-10-11) | The checkerboard message is 23 words, 7 in "IN CASE YOU MANAGE TO CRACK THIS" and 16 in the rest; the URL splits the same way, `gsmg.io` 7 characters and `theseedisplanted` 16 | Exact. With DBBI's 16 `b` and 7 `be` markers this is the third place the film's 23 / 16 / 7 appears. The word boundaries are the reader's, since the checkerboard output has no spaces |
| #76225 (Heisenberg, 2026-10-10) | DBBI's prime markers are the last bits of the URL's characters, `b` for odd and `be` for even; the 84-cell parse differs at marker 21 only | Exact, and the same fact as the poster colours (01 section 1: the coloured cells sit on bit 7). He also reports that the ordinary cells in matrices 4 to 14 wide did not return the URL; that test was not repeated here |
| #77646 (2026-10-21) | A post about a "forgotten key" circulating for the prize address; the post itself says the address was emptied in 2017 | The quoted string is not valid Base58Check, so it is not a key. The claim that the address is empty is false: it holds 125,649,674 sat (section 3.1) |
| #78093 (2026-10-24) | `1NULY7...` ranked as the top lead, a "third door" | A tool's tip address with no preimage (section 3.4) |

The delta file `telegram/ChatExport_delta_2026-09-13_to_2026-10-08.json` is now covered by the new
export, apart from the one deleted message, and is kept because the sections above cite it.
