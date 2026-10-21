# Genesis construction in main.cpp, second pass (4 October 2026)

**6 October 2026 interpretation notice.** This is a dated research record.
Its candidate counts and original logs are preserved, not freshly rerun.
Read [doc 118](../118-correctness-audit-remediation.md) for detector/coverage
limits and [doc 119](../119-current-evidence-ledger.md) for current findings.
A null applies only to its complete tested tuple.

R35 preserves the 27-candidate report and two newline forms. Bitcoin v0.3.10 corroborates row 1616 but is not proven uniquely selected by the creator. The copied value is comment/printer text, not an executable integer or hidden CBigNum operation.

Brief (Lamps, via the coordinator): go back to Satoshi's genesis code in `main.cpp` and reanalyse it as the creator might have read it, covering what R34 (`../source-pointer/`) left out. Ledger row **R35**. Nothing decrypts.

Files: `main_v0.3.10.cpp` and `main_v0.1.0.cpp` (source copies), `gen.py` (retrodiction check + candidates, all pulled by script), `cands.txt`, `run_rt.log`, `run_ct.log`, `run_extra.py` / `run_extra.log` (planted control + newline forms).

## 1. Row 1616 is corroborated by Bitcoin v0.3.10

R34 recorded that row 1616 matched no checked version. I fetched `main.cpp` at every `bitcoin/bitcoin` release tag from v0.1.5 to v0.4.0 (listed with `git ls-remote`) and found the row of the `scriptSig = 486604799 4 0x736B...` comment:

| tag | row | tag | row |
|---|---|---|---|
| v0.1.0 (trottier) | 1442 | v0.3.1 | 1553 |
| v0.1.5 | 1470 | v0.3.2 | 1561 |
| v0.2.0 | 1492 | v0.3.3, v0.3.6, v0.3.7 | 1581 |
| v0.2.2 to v0.2.9 | 1535 to 1542 | v0.3.8 | 1597 |
| v0.2.10 to v0.3.0 | 1550 | **v0.3.10** | **1616** |

From v0.3.12 on the comment block is cut down to the `CBlock(...)` dump, so the scriptSig line no longer exists (v0.3.11 has only a `_notexact` tag, whose block is also changed). **v0.3.10 was the row-1616 match in that checked release-tag set.** That is corroboration, not proof of the creator's selected historical file. The [May 2021 walkthrough](https://github.com/puzzlehunt/gsmgio-5btc-puzzle/blob/a7041aac0b920bb207c071d92386e096204eab6d/README.md) cites [SourceForge revision r133](https://sourceforge.net/p/bitcoin/code/133/tree/trunk/main.cpp#l1616); tag-only uniqueness does not establish historical-source uniqueness.

**Retrodiction passes.** `gen.py` takes row 1616 of v0.3.10, keeps the text after " 4 ", builds the seven-part phase-3 password around it and checks its sha256 against the verified `1a57c572...`. It matches. This reproduces the accepted part-6 string. It does not identify the particular historical copy the creator used, or bind part 6 to a later Architect instruction.

v0.3.10 is the August 2010 emergency release for the value-overflow incident: the `MAX_MONEY` input checks in `ConnectInputs` are absent in v0.3.8 and present in v0.3.10 (checked by grep). One observation, not a lead: **row 1008 of v0.3.10** is `nValueIn += txPrev.vout[prevout.n].nValue;`, the line right before those new overflow checks. Row 868 is an unremarkable line in `IsInitialBlockDownload`. The 1008/868 lists themselves still cannot be rebuilt from any recorded object (R34 write-up), so a hit on a "notable" line cannot be weighed, and I did not turn it into candidates.

## 2. Additional forms examined in R35

R34 tested the nine values on the comment rows (hash, merkle root, scriptSig line, nValue, reversed pubkey, nTime, nBits, nNonce, the decoded headline, the block joined). The historical search of then-available files did not find the following strings; that was a scoped file search, not proof of global novelty:

| id | reading (one sentence) | answers |
|---|---|---|
| N1 | "Raw data" taken literally: the scriptSig as raw serialised bytes, the `coinbase 04ffff001d0104455468...` hex the dump prints on row 1625. | as written, upper, `0x` |
| N2 | "Raw data after 4" read on those raw bytes: what follows the push of 4 (`0104`), with and without the length byte; equivalently, part 6 un-reversed. | `455468...`, `5468...`, upper, `0x`+upper |
| N3 | The sibling code un-reversed: the genesis public key in serialised order, its hash160, its address. | `04678afd...` (3 forms), `62e907b1...`, `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` |
| N4 | The source the row number names. | `v0.3.10`, `0.3.10`, `bitcoinv0.3.10`, `bitcoin0.3.10`, `Bitcoin v0.3.10` |
| N5 | "A temporary dissemination": Satoshi's temporary debug print, which printed exactly these codes ("delete this later" in v0.1.0). | `debugprint`, `debug print`, `debugprintdeletethislater`, as written |
| N6 | The debug print's own output as the source keeps it. | the `CBlock(...)` line; the five dump rows joined, and with newlines |
| N7 | "Row 1616" as a whole row. | as written, stripped, without `//` |

## 3. Results (R35)

- Planted control for this file: an openssl-CLI container (aes-256-cbc, `-md sha256`, random 300-byte body) keyed by a candidate drawn at random from `cands.txt` (`Bitcoin v0.3.10`) was recovered. The rt.py controls (key 1; phases 2, 3, 3.2 open and are recognised) and ct.py controls (11 planted containers, 7 made by the openssl CLI) also fired.
- `rt.py`: 27 candidates, 1,296 decrypts, 5 valid pads (about 5.1 expected), 0 flags, 0 win-test hits. The two newline-bearing dump forms: 96 decrypts, 1 pad, 0 flags.
- `ct.py` (14 ciphers x 5 KDFs x 4 forms): 22,680 decrypts, 100 valid pads (about 89 expected; R34 ran at the same ratio), 0 flags.

**Null.**

## 4. Where this leaves the genesis code

R34/R35 tested the listed genesis values, headline text, forward/reversed hex,
raw script, push-length prefix, neighboring constants and formatting variants.
They reported no validated result within those configurations, subject to the
detector limits in doc 118. This does not establish exhaustive value coverage.

The exact byte fact is that the 69-byte headline becomes 138 uppercase hex
digits prefixed by `0x`. [Line 1616](main_v0.3.10.cpp#L1616) is a `//` comment.
[Executable construction](main_v0.3.10.cpp#L1631-L1634) pushes headline bytes
and a separate `CBigNum(4)`; upstream
[ValueString](https://github.com/bitcoin/bitcoin/blob/v0.3.10/script.h#L323-L330)
and [HexNumStr](https://github.com/bitcoin/bitcoin/blob/v0.3.10/util.h#L317-L326)
explain the reversed-byte diagnostic text. There is no supported hidden-integer
operation, wallet-address interpretation, uniquely selected release, or new
row-offset instruction. The Architect's exact number and carried-code receiver
remain unexplained; [doc 119 §6](../119-current-evidence-ledger.md#6-hundred-fourty-and-the-genesis-source)
records the current evidence.

Historical unrun proposals: crossing genesis values with label answers and scanning other source rows. Neither is an active task, and the 23/16/7 wording does not bind a corpus or authorize a new sweep.
