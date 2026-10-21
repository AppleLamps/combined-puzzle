# 119 — Current evidence ledger (6 October 2026)

This is the current interpretation layer for the repository. It reconciles the
fresh source review with the older dossier and experiment logs, without replacing
primary artifacts or rewriting historical run output. Baseline reviewed:
`1a71de4a62a42b0e0f27d26a1d562d67dca6e55b` on `main`.

**No new unlock or private key has been established. No search is running.**
This update is documentation-only. Historical run counts below are reported
results, not new executions or proofs of exhaustive coverage.

## 1. How to read the record

- **Verified artifact fact:** directly supported by retained bytes, a captured
  page, a dated creator message with its reply context, or an independently
  checked source.
- **Conditional result:** valid for the stated grammar, correspondence,
  serialization, cipher/KDF, or detector. Keep those assumptions attached.
- **Interpretation:** a possible intended meaning, route, or purpose. An exact
  length match or a failed candidate does not promote it to fact.
- **Historical result:** what an older run or write-up reported. Its original
  evidence remains useful within its actual coverage and detector limits.

[Status](status.md) is the short current summary; the
[dossier](GSMG-PUZZLE-DOSSIER.md) holds detailed primary material.
[Doc 118](118-correctness-audit-remediation.md) governs detector and runtime
verification limits. This ledger governs newer interpretation corrections.
The [document index](67-document-index.md) and failed-attempts records retain
their historical inventory, including references to documents absent from this
checkout. Absence of an old file is not evidence that its experiment never ran,
and an old title such as “closed” is not a current theorem.

## 2. DBBI, the poster, and FAED

The fixed-prefix construction is reproducible: treat the off-white cell as the
21st event in the 25-event color program, identify it with blue, and map the
first 23 events to the first 23 prime positions. The L=83 walk consumes the 91
DBBI characters with 23 hosts, eight yellow `be` hosts and fifteen blue `b`
hosts. Its color string is `BBBBYBBBYYBBBBYBBYYBBYY`.
Sources: [DBBI](../dbbi.txt), [poster data](../matrix.json), dossier §§4.3 and 6.3.

The scope matters:

- L=83 is preferred **under that fixed first-23-event correspondence**. The
  forced-blue argument does not globally exclude L=84.
- The later independently reported audit checked 300 selection cases and
  retained three L=83 branches and two L=84 branches. A no-duplicate-byte rule
  still leaves L83C and L84A. Selecting a unique L=84 branch additionally uses
  a prefix-bytes-1–23 rule that has no established source instruction. The
  original detailed selection receipts are not available in this checkout;
  these are reported audit results, not a fresh reproduction here.
- L=83 and L=84 differ at the role of the final raw DBBI character, the `e` at
  position 91. Their 22 internal gaps contain the same 59 letters. Changing
  this endpoint classification does not create a different internal payload.
- A claimed continuation that consumes event 24 (blue) to reach L=84 must not
  count that same event again in the continuation. None of the five audited
  branches supplied a fully supported continuation. L83C/D have already
  consumed event 25 and leave no chronological tail. For the L83 first-23
  branch, event 24 B matches raw position 97, but event 25 Y expects `be` at
  105–106 and finds `aa`. L84A/B have already consumed event 24; their remaining
  event 25 Y expects `be` at 97–98 and finds `bb`. Crossing into the separately
  decoded `matrixsumlist` field is itself an unsupported assumption.
- The older “no `g` in the last 60 FAED characters” claim is false: that suffix
  contains six `g`s. The separate fact that the final 32 contain no `e` or `g`
  remains distinct and must not be broadened to 60.

The bias and distribution comparisons recorded in dossier §6.4 are evidence
compatible with a filler model. They do not prove a common generator, prove
the absence of another payload, or establish the intended role of every
character. “DBBI is only a checksum” and “FAED is definitely filler” were
overstatements. The creator's non-answer to decode-versus-ingredient (#70325)
does not resolve this.

The proposed periodic `11110` generator with B=1/Y=0 predicts
`BBBBYBBBBY` for the first ten color events; the actual prefix is
`BBBBYBBBYY`. Its first failure is at the ninth event. The first five matching events
are already forced by the ASCII parity of the initial `gsmg.` bytes and are
not independent confirmation. This is a rejected specific generator, not a
general rejection of every possible use of `11110`.

Atlas-derived historical arithmetic is retained only where independently
checked and with its assumptions. Atlas is not an active research direction;
missing Atlas artifacts are not a reason to reopen a search.

## 3. Envelopes, route, and the two SHA readings

All three locked blobs have authentic puzzle provenance, with different strengths
of independent corroboration: Terminal is carried in the established phase-3.2 plaintext;
SalPhaseIon short is reconstructed by joining the two halves in the first
captured side-page textarea; Cosmic Duality is the second textarea. Their
exact bytes, salts and hashes remain in [ARTIFACTS.md](../ARTIFACTS.md) and
[the captured page](../salphaseion_phase3.html).

Exact Terminal base64 matches the [April 26, 2020 community record](https://github.com/puzzlehunt/gsmgio-5btc-puzzle/blob/c4b6a20e8bff6ae1df1e8b1819b6fd1d27d361df/README.md);
exact short-envelope base64 matches the [May 20, 2021 record](https://github.com/puzzlehunt/gsmgio-5btc-puzzle/blob/a7041aac0b920bb207c071d92386e096204eab6d/README.md).
These text matches were rechecked for this documentation update after removing
whitespace and Markdown quote markers, without decrypting anything. The
[May 7, 2021 screenshot](https://github.com/puzzlehunt/gsmgio-5btc-puzzle/blob/99bd811f6310e6bbb9a71514ebcac52f345e8e55/SalPhaselonCosmicDuality.png)
was previously reviewed as corroborating Cosmic Duality's presence, but was not
an independent full-byte verification of that blob. Do not flatten
these three provenance strengths into a single “all bytes independently
verified historically” claim.

Authenticity does **not** establish that all three must be opened, that short
comes first, that Terminal is the only rabbit hole, or that Cosmic Duality is
necessarily a message rather than a key-bearing or nested object. Creator
[#39237](../jrk_messages.txt#L1550-L1553) calls yinyang the next phase in reply
to an AES question; it does not name the envelope or uniquely order these
three blobs.

`Salted__` identifies an envelope convention, not its cipher. The lengths
80/80/1,328 bytes are compatible with padded 16-byte blocks. Bounds
64–79/64–79/1,312–1,327 plaintext bytes apply only under the stated CBC/ECB
PKCS#7 hypothesis. They neither rule out stream modes nor prove content.

The labels `matrixsumlist`, `lastwordsbeforearchichoice`, `thispassword`, and
`enter` are established decodes. Assembly, receiver, selection, and downstream
meaning remain unresolved. The literal ending is `shabefanstoo`; expanding it
to “the answer too” is a reading, not a literal transcription. `enter` aligns
with the 64-character base64 wrap, but that does not prove its role is wholly
spent. A first-hint/method reading and a separate or downstream SHA operation
remain competing models. Joint concatenation is one hypothesis, not a settled
instruction. Sources: [textarea](../salphaseion-textarea.txt), dossier §6.2,
[independent-model discussion](independent-model/README.md), doc 118.

## 4. Architect text, categories, and formatting

The normalized Architect stream contains 1,539 letters; historical April 2020
copies agree with the retained [letter stream](../architect_letters_1539.txt).
Punctuation and word breaks in prose transcriptions are editorial. `ORA.LE`
comes from a solver's transcription and is not an independently authenticated
creator punctuation clue. `sedulously` is inherited from the film wording;
claims that every unusual word was inserted by the creator are unsafe. Some
film-versus-puzzle wording differences remain uncertain across transcripts.

“Reinserting the prime basics” might already describe the DBBI prime work.
It is not established as a separate unfinished instruction. The recipient of
“the code you hopefully carry” and the selection operation are still unknown.
R34's identification of that code with genesis part 6 is a solver hypothesis;
the original page already consumes part 6 in the seven-part phase-3 gate.

A category-aware inventory found 20 encoded fields, six encrypted containers,
four explicit gates plus three inferred gates, and 12 password-component
occurrences representing 11 distinct components. These are different counting
units: authored encoded message fields, distinct containers, explicit password
gates, and answer components; the four known assemblies have 1/1/7/3 components.
This is a bounded, independently reported inventory; its full object-ID receipt
is not in the checkout. None binds “23 ciphers / 16 encryptions / 7 intertwined passwords” to a
particular corpus or ordering. The old 23-atom list is a chosen test corpus,
not an authenticated category census or a queued task.

The [checkerboard plaintext](../checkerboard_vic_91.txt) concerns ownership
and funding of “half and better half.” It does not instruct a key split,
secret sharing, or combining holders' material. Historical split tests remain
tests of that interpretation.

Earlier answer formatting is stage-specific. Phase 3 preserves `Safenet`,
`Luna`, `HSM`, uppercase hexadecimal digits with a lowercase `0x`, and the
spaces in the FEN-like working string. The page's
[`aBa` and `connected not enf` tags](../phase2_choice.html#L47-L55)
contradict a universal lowercase/no-space convention. Preserve the exact accepted puzzle FEN string, including its counters, rather
than silently regenerate it. Its retained halfmove counter after a quiet rook
move is a move-history issue, not evidence of malformed FEN grammar.

Two additional checks should not be mistaken for new operations. The 54-letter
pre-`SELECT` span at zero-based Architect offsets `[1089,1143)` (words 246–256)
is generated by the historical all-word generator at `i=256, k=11`, although
it is absent from `lw_core` and the common-flaw candidate list. Missing original
pool output prevents certifying that it executed or identifying its partners.
A source-image review inspected 384 palette candidates and found no exact or
probable match for the red-dot overlay in message #72320; that bounded visual
negative excludes neither uninspected formats nor palette misses.

The reported fixed insertion of DBBI values `a=1..i=9` into the poster URL's 91
zero slots has row sums `[36,23,29,24,49,38,24,40,22,26,27,27,35,22]` and column
sums `[25,24,26,15,32,29,42,27,33,40,27,37,32,33]`, totaling 422 in each direction.
Keeping the original 101 one-bits makes each total 523. The 91 zeros belong to
the 192 URL bits; the four padding zeros are separate. In this construction F
receives raw DBBI position 77 (`b=2`, host 20), not color-event ordinal 21.
These are arithmetic results under a chosen insertion rule, without independent
instruction or downstream confirmation. They do not revive a search direction.

## 5. The SafeNet coordinate

The unsigned result `51°52′28.0″ N, 4°24′23.2″ E` has stronger independent
support than the old dossier recorded. SafeNet's
[official archived EMEA office page (2015)](https://web.archive.org/web/20150224185950/http://www.safenet-inc.com:80/contact-us/global-offices/emea/)
and [NATO procurement notice (25 January 2019, p. 3)](https://www.mimit.gov.it/images/stories/garenato/NOI_ACO-SH-19-06.pdf)
place SafeNet Technologies BV at Seattleweg 5, 3195 ND Rotterdam-Pernis.
[Companies House's historical control entry](https://find-and-update.company-information.service.gov.uk/company/02258824/persons-with-significant-control)
independently records that address. Control-record dates are not occupancy dates.

The published point falls inside the current official
[BAG building footprint](https://api.pdok.nl/kadaster/bag/ogc/v2/collections/pand/items/bc910fad-1acb-5011-8320-ffda5df87099?f=json)
linked to the [Seattleweg 5 address object](https://api.pdok.nl/kadaster/bag/ogc/v2/collections/verblijfsobject/items/15cce0ca-b3e3-5043-a091-136342018033?f=json),
about 21 m from its address point. That is a building-scale corroboration,
not merely proximity to the A15. The dataset retrieved on 5 October 2026 does
not establish the footprint throughout 2018–2021, an entrance, or a tenant's
room. The `× -1` sign remains unresolved. Geographic corroboration does not
justify dropping it algebraically or searching for an alternative location.

## 6. “Hundred fourty” and the genesis source

The strongest prose reading in context concerns Fresco, building a community,
and investing time. Creator [#26875](../jrk_messages.txt#L1311-L1313) supports
the Fresco/community theme. **The exact number 140 remains unexplained.**
[#5960](../jrk_messages.txt#L594-L596) calls the spelling a typo while replying
to a solver who proposed 104; it endorses neither 104 nor a new numerical rule.

The separate byte fact is exact: phase-3 part 6 is the 69-byte, 11-word genesis
headline reversed bytewise and printed as 138 uppercase hexadecimal digits
after `0x`, totaling 140 characters. In the retained
[`main.cpp` source](genesis-main-cpp/main_v0.3.10.cpp#L1613-L1636), line 1616 is
a `//` comment containing a script-printer representation. Executable line
1633 pushes the headline as a byte vector, alongside a separate `CBigNum(4)`.
The upstream [ValueString code](https://github.com/bitcoin/bitcoin/blob/v0.3.10/script.h#L323-L330)
calls [HexNumStr](https://github.com/bitcoin/bitcoin/blob/v0.3.10/util.h#L317-L326),
which reverses byte order and uses `%02X` with the `0x` prefix. This is ordinary
Bitcoin diagnostic formatting, not an executable 140-character integer, a
wallet address, or a hidden CBigNum operation.

Bitcoin v0.3.10 corroborates row 1616. It is not established as the uniquely
selected historical release: the [older community walkthrough](https://github.com/puzzlehunt/gsmgio-5btc-puzzle/blob/a7041aac0b920bb207c071d92386e096204eab6d/README.md) cites [SourceForge revision r133](https://sourceforge.net/p/bitcoin/code/133/tree/trunk/main.cpp#l1616). The R34/R35 tag survey establishes the match within its checked set,
not the file the creator personally used. Part 6's exact length alone does
not bind it to the later Architect sentence or to “the code you carry.”

The seven accepted phase-3 part lengths are `9, 7, 4, 3, 5, 140, 59`, totaling
227. There are 49 prime positions through 227, so a 7×7 arrangement is
arithmetically possible. Shape alone does not confirm an operation, and the
historical T44 coverage already included related prime-position work.

### Scoped negative checks and rejected readings

- The creator-only search covered 492 message bodies, 20 April 2019 to
  1 September 2026. Literal `140` occurred zero times; `hundred` and `forty`
  hits were quoted solver-parent context, and `investment` appeared in an
  unrelated message (#23130). This is a corpus-specific negative, not proof
  that no binding ever existed anywhere.
- The retrieved documentary transcript and three inspected Fresco books
  supplied no supported numerical binding. Transcript track identity was
  uncertain. These are bounded negative checks, not exhaustive source coverage.
- `INVESTMENT` sums to 141 under ordinary A1Z26, not 140. A 140-fold financial
  ratio gives 700 BTC if 5 BTC is the input, or 1/28 BTC if 5 BTC is the return;
  the latter is not an exact whole-satoshi stake. No source binds either model.
- At [140 seconds in the official film](https://www.youtube.com/watch?v=Yb5ivvcTvRQ&t=140s),
  only caption text and playback time were checked; buffered black video was
  not visual verification. The caption concerns a first flight. No extraction
  rule or supported timestamp operation emerged; adjacent offsets are not new
  instructions.
- [R34](source-pointer/README.md) and [R35](genesis-main-cpp/README.md) already
  covered the headline text, reversed/forward hex, raw script, length-byte
  prefix, neighboring genesis values and documented formatting variants. Their
  nulls are bounded by doc 118. This review supplies no new supported mechanism
  and does not authorize more offsets, variants, or a coverage run.

### The 2025 on-chain phrase

[Transaction 2b6f8b68…](https://mempool.space/tx/2b6f8b68f6174e432a2cdd33ce1e46d365e4cef3a51272432baf35fed86bb449)
in block 898064 (23 May 2025) really carries `it myself 140 investment`.
Its script is `6a186974206d7973656c662031343020696e766573746d656e74`; the
transaction includes a 70,000-satoshi payment to the community donation
address listed by the [community repository](https://github.com/puzzlehunt/gsmgio-5btc-puzzle/blob/master/README.md).
That establishes the text and donation context, not creator authorship.
Creator [#12653](../jrk_messages.txt#L1106-L1108) is a generic denial dated
29 August 2023, before this transaction, and must not be cited as a specific
denial of its 2025 text. See [the on-chain reference](../07-onchain-facts.md).

## 7. Coverage and validation limits

Doc 118 corrects the old pad-1/2 binary-output blind spot, documents bounded
retention/overflow, and restores a missing 144-candidate assembly form. It did
not rerun the corrected candidate set. Historical zero flags and working
controls do not prove that every supported plaintext, cipher, assembly or
referent was excluded. A null attaches to the full tested hypothesis tuple.

The subsequent [AES-import restoration](https://github.com/AppleLamps/gsmg-puzzle-kit/commit/1a71de4a62a42b0e0f27d26a1d562d67dca6e55b)
reports three source-only Node regressions and a syntax check. These do not
establish encrypted runtime behavior. The earlier C compile and encrypted
validation restrictions remain recorded in doc 118. No runtime, cipher,
wallet, key-recovery or puzzle search was run for this documentation update.

Next work requires a source-supported rule that fixes its operands, receiver,
selection, and formatting. There is no currently established mechanism to
execute. Keep the existing no-sweep and no-contact boundaries.
