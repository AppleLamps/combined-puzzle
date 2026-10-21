# 01 — Archivist: [V] reproduction against the SECOND build

## RESULT: NO FAILURES

**No check failed.** Every reproduced [V] check in sections 1, 3.1, 3.4, 4.1,
4.2, 4.3, 4.4, 5, 6.1, 6.2 and 7.1 of the new file passes, including all
second-build items (a)–(f) itemised in the task. Two statements are listed
under "Not reproduced" at the end (QR payload, on-chain facts) because they
cannot be derived from the files in this workspace offline; they are
**not** counted as FAIL, and nothing else is silently omitted.

| run | result |
|---|---|
| `python3 src/step0_trust.py` (prior work, reads the first-build file) | **49/49 PASS, 0 failed** |
| `python3 src/check_report3_2026-10-17.py artifacts` (prior work) | all printed numbers match §6.3/§1 (see cross-checks below) |
| `python3 src/archivist_check2.py` (new, reads **only** `uploads/GSMG-handoff.md`, second build) | **106/106 PASS, 0 failed** |

Sources actually read by the new script:

- `uploads/GSMG-handoff.md` sha256 `aa7ac433cd8c53af1365985b1484ab3a35b2573566b0d6d30982bee5e10d5044` at the time of this log, which was the handoff after this repo added a §9 footnote. The file is now restored to the unmodified second build, sha256 `442d502f2bb65b44f1ba67ede9b9415da6a6395b98966e69d931853c10f6d7f6`; the footnote lives in `ledger/experiments.md` (matches `ledger/README.md`; the file declares itself "second build of the file (17 October 2026)")
- `data/puzzle.png` sha256 `38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830`, 29931 bytes

Hard limits observed: nothing submitted to gsmg.io, no contact/identification
of anyone, no web search, offline only.

---

## Provenance + §1 — The goal

| # | check | result | exact value |
|---|---|---|---|
| 1 | second-build handoff sha256 | PASS | `aa7ac433cd8c53af1365985b1484ab3a35b2573566b0d6d30982bee5e10d5044` |
| 2 | handoff declares second build (17 Oct 2026) | PASS | literal string present |
| 3 | prize address, vanity prefix `1GSMG` | PASS | `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` |
| 4 | address base58check decodes to version `00` + prize hash160, checksum valid | PASS | payload `00a9553269572a317e39f0f518cb87c1a0ee1dbae4` |
| 5 | §1 hash160 line equals prize hash160 | PASS | `a9553269572a317e39f0f518cb87c1a0ee1dbae4` |
| 6 | **(a)** uncompressed pubkey (65 B, `04…`) hashes to the prize hash160 | PASS | `a9553269572a317e39f0f518cb87c1a0ee1dbae4` |
| 7 | **(a)** compressed pubkey (33 B, `03…`) hashes to `06bbdc66…` and can never match | PASS | `06bbdc66fda09110435c79a86656a604c2d5c69b` ≠ `a9553269…dbae4` |
| 8 | **(a)** both serialisations are the same point (same x, y odd ↔ prefix `03`) | PASS | x `f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464`, y parity odd |
| 9 | control privkey 1, compressed hash160 (§1 code comment) | PASS | `751e76e8199196d454941c45d1b3a323f1433bd6` |
| 10 | control privkey 1, uncompressed hash160 | PASS | `91b24bf9f5288532960ac687abb035127b1d28a5` |
| 11 | control privkey 1 is not a win in either form | PASS | neither equals `a9553269…dbae4` |

Cross-check from `check_report3_2026-10-17.py` (independent `hashlib` ripemd160):
`target compressed h160 06bbdc66fda09110435c79a86656a604c2d5c69b`,
`target uncompressed h160 a9553269572a317e39f0f518cb87c1a0ee1dbae4`,
`key 1 uncompressed h160 91b24bf9f5288532960ac687abb035127b1d28a5` — all agree.

## §3.1 — The poster

| # | check | result | exact value |
|---|---|---|---|
| 12 | poster sha256 | PASS | `38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830` |
| 13 | poster size | PASS | 29931 bytes |
| 14 | poster dimensions/mode | PASS | 1048×1556 RGBA (array shape `(1556, 1048, 4)`) |
| 15 | PNG chunks, no bytes after IEND | PASS | exactly `IHDR,sRGB,gAMA,pHYs,IDAT,IEND`; parser ends at byte 29931 |
| 16 | measured 14×14 grid equals §3.1 grid byte for byte | PASS | first rows `WWKKWBWWKWKKWY`, `KKBKWWKKKWBWKK`, … (all 14 rows identical) |
| 17 | colour counts | PASS | K 86, W 85, B 15, Y 9, F 1 |
| 18 | red divider `#ED1C24` first at y=1047 | PASS | first red row 1047, 15705 red pixels |
| 19 | off-white cell row 7 col 4 flat `#FEFEFE` (254, not 255) | PASS | unique cell colour `[[254,254,254]]` |
| 20 | exactly 7 non-flat (rabbit) cells, rows 6–8 cols 6–9 (cols 0–12 tested; last column is edge-truncated) | PASS | `(6,6) (6,7) (7,6) (7,7) (7,8) (7,9) (8,6)` |
| 21 | spiral (down first, K/B=1) first 192 bits | PASS | `gsmg.io/theseedisplanted` |
| 22 | last 4 spiral bits | PASS | `0000` |
| 23 | every blue/yellow cell sits on bit 7 (blue=1, yellow=0) | PASS | 0 mismatches |
| 24 | off-white spiral index 163, a 0 bit inside the `n` of "planted" | PASS | index 163, byte `b'n'`, bit `0` |

Visual (not scripted): the rendered poster below the divider shows the text
`GSMG.IO 5 BTC PUZZLE CHALLENGE` and the printed address
`1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`, as §3.1 states. The QR payload itself is
under "Not reproduced" below.

## §3.4 — SalPhaseIon side page

| # | check | result | exact value |
|---|---|---|---|
| 25 | **(f)** path = sha256 of poster text + address | PASS | sha256(`GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`) = `89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32`, identical to the path in the §3.4 heading |
| 26 | textarea 1 spacing | PASS | 1074 single spaces, 0 newlines, no double space, 1075 compact chars |
| 27 | side page contains SalPhaseIon + Cosmic Duality textareas | PASS | 2 textareas |

## §4.1 — Encryption convention

| # | check | result | exact value |
|---|---|---|---|
| 28 | FIPS-197 AES-128 ECB known answer | PASS | ct `69c4e0d86a7b0430d8cdb78070b4c55a` |
| 29 | FIPS-197 AES-256 ECB known answer | PASS | ct `8ea2b7ca516745bfeafc49904b496089` |
| 30 | SP 800-38A F.2.1 AES-128-CBC known answer | PASS | first block `7649abac8119b246cee98e9b12e9197d` |
| 31 | SP 800-38A F.2.5 AES-256-CBC known answer | PASS | first block `f58c4c04d6e5f1ba779eabfb5f7bfbd6` |

The §4.1 convention itself (password = lowercase hex sha256 of answer,
EVP_BytesToKey md=SHA-256 1 iteration, AES-256-CBC, PKCS#7) is exercised
end-to-end by §§4.2–4.4 below: three independent containers decrypt to the
exact printed plaintexts, which a wrong convention would not do.

## §4.2 — Phase 2

| # | check | result | exact value |
|---|---|---|---|
| 32 | phase 2 container decrypts with `causality` | PASS | `Salted__`, salt `06286612d43ed7ed` |
| 33 | plaintext is 648 bytes | PASS | sha256 `e2f9dd65604a3231f8b3301724e8d713a88fffc4b6c7c4aeeb20f58a582b593a` |
| 34 | plaintext equals §4.2 printed text byte for byte (CRLF restored) | PASS | same sha256 as #33 |

## §4.3 — Phase 3

| # | check | result | exact value |
|---|---|---|---|
| 35 | seven answer parts exactly as printed | PASS | `causality`, `Safenet`, `Luna`, `HSM`, `11110`, `0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854`, `B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1` |
| 36 | decrypts with the plain concatenation | PASS | 4090 bytes, sha256 `c4ad94559a44a927c1032cc0e024515f9510a0806a2d14458dbf4a360af9865f`; password sha256 `1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5` |
| 37 | plaintext equals §4.3 printed text byte for byte (CRLF restored) | PASS | same sha256 as #36 |

Note: §4.3's own chess line in the page text differs (`B5KR/1r5B/6R1/…` in §3.3's
page) from part 7 as used (`B5KR/1r5B/2R5/…`); only the §4.3 part-7 string was
tested, and it is the one that decrypts. This is the file's own presentation,
not a mismatch found here.

## §4.4 — Phase 3.2

| # | check | result | exact value |
|---|---|---|---|
| 38 | decrypts with `jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple` | PASS | 2422 bytes, sha256 `b82afeb86f9e50848220f9b64b744b821400308aea273a1c949b9d2d0e408a34` |
| 39 | §4.4 "full plaintext as base64" decodes to exactly those bytes | PASS | same sha256 as #38 |
| 40 | plaintext ≈59% printable ASCII | PASS | 1426/2422 = 58.9% (bytes `0x20–0x7E`) |
| 41 | bytes 0–446 are the printed ASCII greeting, ending CRLFCRLF | PASS | begins `I've been waiting for you. `, 447 bytes |
| 42 | bytes 447–1985: 1539 bytes, 26 distinct byte symbols, 26 distinct cp273 glyphs | PASS | len 1539, symbols 26/26 |
| 43 | reciprocal Beaufort `THEMATRIXHASYOU` with one consistent 26-symbol substitution reproduces the printed speech exactly | PASS | 1539 letters, sha256 `56c43a300e28b86bb43b8dcbae74c43c76bde90b3e1190620fb656f2c94b2241` (method: the substitution is *derived* from the speech via P=(K−C) mod 26 and must be a consistent bijection — it is, 26/26 symbols) |
| 44 | speech opening/closing | PASS | opens `YOURLIFEISTHESUMOFAREMAINDER`, ends `…OURETHEONECIAOBELLAO` |
| 45 | bytes 1990–2138 are the printed 149 digits, CRLFCRLF either side | PASS | `151659431219724091691712137589518131415431314124281541913121812194331211716171371491109166131213131281491109166131412199114371612126021664313711154112` |
| 46 | straddling checkerboard (alphabet `FUBCDORA.LETHINGKYMVPS/JQZXW`, blanks 1 and 4) decodes as printed | PASS | `INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE` (91 chars) |
| 47 | bytes 2143–2291 are the printed riddle, terminal container starts at 2292 | PASS | `Raising the stakes without extra chances of winning. A fubcd-king & oracle-queen, thingky mvps, on a sad board but as wide as the first one seen.` + CRLFCRLF |

## §5 — The three locked containers — task item (e)

For each container the §5 base64 block was compared byte for byte with the
container extracted from its independent source (phase 3.2 tail / SalPhaseIon
text halves / Cosmic textarea), then salt, ciphertext length and the sha256
of the raw `Salted__` blob were recomputed.

| # | check | result | exact value |
|---|---|---|---|
| 48 | Terminal: §5 base64 = source in phase 3.2 plaintext | PASS | 128 base64 chars |
| 49 | Terminal: salt and ciphertext length | PASS | salt `b45a5e3d827593ca`, ct 80 bytes, raw 96 bytes |
| 50 | Terminal: sha256 of raw container | PASS | `291dfd6f3e759ec2e272b35a00c24907da70c3e7a9291b4c13605c7b0b4f3de9` |
| 51 | SalPhaseIon short: §5 base64 = joined halves from the SalPhaseIon text | PASS | 128 base64 chars (64+64) |
| 52 | SalPhaseIon short: salt and ciphertext length | PASS | salt `3ab585348552415d`, ct 80 bytes, raw 96 bytes |
| 53 | SalPhaseIon short: sha256 of raw container | PASS | `9e2831e1b34b5f34796df47ccaf6530d48d371c61a6bff84d60db1064fa7a258` |
| 54 | Cosmic Duality: §5 base64 = side-page textarea 2 | PASS | 1792 base64 chars |
| 55 | Cosmic Duality: salt and ciphertext length | PASS | salt `2d3f6fe06dc950e6`, ct 1328 bytes, raw 1344 bytes |
| 56 | Cosmic Duality: sha256 of raw container | PASS | `b18950551a4dd0cb8a9378f0906ba18c03a15f0ee83eb98c6bc90165c5f79805` |

All three table rows in §5 (salt, ct bytes, sha256) match the recomputed
values exactly; the PKCS#7 plaintext-size bounds stated in §5 (64–79 and
1312–1327 bytes) follow arithmetically from 80 and 1328.

## §6.1 — SalPhaseIon layout

| # | check | result | exact value |
|---|---|---|---|
| 57 | §6.1 wrapped text joins to exactly the compact SalPhaseIon text | PASS | 1075 chars, sha256 `26e37652067c549c0eee624356be9ffd40a243901197335a41f91fb6c78e6156` |
| 58 | span table matches measured blocks | PASS | `[0,91) [91,195) [195,765) [765,766) [766,829) [829,830) [830,859) [859,860) [860,895) [895,959) [959,999) [999,1063) [1063,1075)`, lengths `91/104/570/1/63/1/29/1/35/64/40/64/12` |
| 59 | three `z` separators | PASS | at offsets 765, 829, 859 (0-based) |
| 60 | block alphabets | PASS | dbbi `abcdefghi`; ab1/ab2 `ab`; faed `abcdefghi`; lastwords `abcdefghio`; thispassword `abcdfghio` (subset of a–i+o); b64 halves base64 alphabet |
| 61 | plain-text blocks | PASS | `shabefourfirsthintisyourlastcommand`, `shabefanstoo` |

## §6.2 — Exact decodes

| # | check | result | exact value |
|---|---|---|---|
| 62 | a/b run [91,195), a=0 b=1, 8 bits/char | PASS | `matrixsumlist` |
| 63 | a/b run [959,999) | PASS | `enter` |
| 64 | decimal run [766,829), a=1..i=9 o=0, integer→hex→ASCII | PASS | `lastwordsbeforearchichoice` |
| 65 | decimal run [830,859) | PASS | `thispassword` |
| 66 | `shabef` reading (b=2, e=5, f=6) | PASS | `sha256ourfirsthintisyourlastcommand`, `sha256anstoo` |
| 67 | two base64 halves joined = SalPhaseIon short container | PASS | 128 chars, salt `3ab585348552415d` |

## §6.3 — dbbi measured facts — task item (b)

Walk definition used: positions 1,2,3,…; at prime positions take the next
colour of the poster's spiral colour sequence (coloured cells only, off-white
spliced in as the 25th symbol), 1 letter for blue/off-white, 2 for yellow;
one filler letter at every non-prime position.

| # | check | result | exact value |
|---|---|---|---|
| 68 | poster spiral coloured cells in order | PASS | `BBBBYBBBYYBBBBYBBYYBFYYBY` (B 15, Y 9, F 1) |
| 69 | walk uses all 91 letters exactly at position 83; 23 hosts; every host starts with `b` | PASS | used 91, end position 83, hosts 23 |
| 70 | every yellow host is exactly `be`; off-white host is one letter `b` | PASS | yellow hosts at positions 11, 23, 29, 47, 61, 67, 79, 83, all `be`; F host `(73, F, 'b')` |
| 71 | **hosts = 15 `b` + 8 `be`** | PASS | `{'b': 15, 'be': 8}` |
| 72 | **greedy raw count in the text = 15 `b` / 10 `be`** | PASS | `{'b': 15, 'be': 10}` (differs from the walk at a blue host + filler `e`, and two filler `b`) |
| 73 | **dbbi holds 25 `b` in all** | PASS | 25 |
| 74 | **60 filler letters, exact string** | PASS | `difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea` |
| 75 | filler letter counts | PASS | a3 b2 c8 d4 e10 f10 g10 h8 i5 |
| 76 | filler `b` split and placement count | PASS | split `19|16|23`; 6 of 1770 placements of two `b` among 60 give the set {16,19,23} |
| 77 | **host bits (blue/off-white=1, yellow=0)** | PASS | `11110111001111011001100` |
| 78 | **host bits = URL LSBs with a 1 inserted at position 21, `10` unused** | PASS | LSBs of `gsmg.io/theseedisplanted` = `111101110011110110010010`; inserted string `1111011100111101100110010`; first 23 bits = host bits; remainder `10` |
| 79 | **continuation past 83**: positions 84–88 take one character each, position 89 (24th colour, blue) lands on `b` | PASS | `(84,-,a) (85,-,b) (86,-,b) (87,-,a) (88,-,b) (89,B,b)` |
| 80 | **continuation fails at position 97** (25th colour, yellow, needs `be`) on `aa` | PASS | failed at `(97, Y, 'aa')` |
| 81 | off-white alternatives | PASS | F-as-yellow would need 92 chars; F-dropped walk consumes 91 but its hosts do not parse |
| 82 | exhaustive control: exactly 1 of the 490,314 ways to choose 8 yellow hosts among 23 parses | PASS | 1 parse of 490314 — the poster's own colour order |

Cross-check: `check_report3_2026-10-17.py` prints the same host-bit/URL result
("with 1 inserted at position 21, first 23 bits `11110111001111011001100`
unused `10`; equals B=1,Y=0 of the 23 hosts: True") and the same filler split
`[19, 16, 23]`, 6 of 1770.

The [T, measured] statistics attached to this reading in §6.3 (G-test
p-values, the two 200,000-shuffle nulls) are tagged [T] in the file, not [V];
they were not re-run and are not counted here either way.

## §6.3 — faed measured facts — task item (c)

| # | check | result | exact value |
|---|---|---|---|
| 83 | faed block shape | PASS | 570 letters, begins `faedggeedfcb…` |
| 84 | **letter counts** | PASS | a54 b49 c52 d49 e69 f57 g107 h58 i75 |
| 85 | **last 32 letters, no `e`, no `g`** | PASS | `bccahhbiibibbibdcbahaidhfahiihic` |
| 86 | that suffix is maximal for {e,g} | PASS | 1-based letter 538 is `g` |
| 87 | **`g` at 1-based prime positions** | PASS | 24 (of 107 `g`) |
| 88 | Bifid square construction | PASS | first-appearance letters of dbbi `dbifhcega` + `klmnopqrstuvwxyz` (no `j`) = `dbifhcegaklmnopqrstuvwxyz` |
| 89 | full-period Bifid starts `btcseedd` | PASS | `btcseeddeoemckeadhbschdk…`, 570 chars |
| 90 | **Bifid output sha256** | PASS | `15d62c8228c1a30f3f6280fcdce2251fe616135e9de291b0c7b8a792dd8d0507` |
| 91 | Bifid output at even (0-based) positions uses only b,c,d,e | PASS | `{b, c, d, e}` |
| 92 | **only period 570 yields `btcseed`** | PASS | periods 1–570 tested, hits `[570]` |
| 93 | calibration: orderings of the nine dbbi letters giving `btcseed` | PASS | exactly 8 of 362,880, all continuing `btcseedd`; first-nine cells `dbifhcega`, `dbifgceha`, `dchagbeif`, `dcgahbeif`, `ebifhcdga`, `ebifgcdha`, `echagbdif`, `ecgahbdif` |
| 94 | calibration: 5 of 6,561 for the four Bifid-paired letters at 285:289 | PASS | `aieb`, `aied`, `aief`, `aieh`, `aiei`; the actual letters are `aied`. (Operationalisation: the first Bifid output letters pair `faed…` with the letters at 285:289; varying those four over a–i gives exactly 5 hits including the actual one.) |

| # | faed whole-integer arithmetic (a=1..i=9 unless stated) | result | exact value |
|---|---|---|---|
| 95 | **whole block as one decimal integer is 237 bytes, head `1bd5951d`, tail `c7bbc075`** | PASS | sha256 of the 237 bytes `7f14db2d90301b8e1d16ff014ad3e84ba75350ef828ad9b8a8a26b1e69302de9` |
| 96 | **78 of 237 bytes printable** | PASS | 78 |
| 97 | a=0 tail, and non-printable count either way | PASS | a=0 tail `009f4eae` (also 237 bytes); 3 of 4 tail bytes outside printable ASCII under both a=1 and a=0 |
| 98 | reason the tail is mask-proof | PASS | `10^32 mod 2^32 = 0`, so the last 32 decimal digits alone fix the last 4 bytes, and they contain no `g`/`e` |
| 99 | **tail invariant under g/e zeroing** | PASS | tail stays `c7bbc075` for every single-g zeroing (107), every single-e zeroing (69), all-g, all-e, and all-g+e zeroings |
| 100 | **single zeroing making the last four bytes printable: only position 557** | PASS | `[(557, b'yI u')]` — bytes `79 49 20 75` |
| 101 | **zeroing 1–4 of the last 32 positions: unique four-lowercase tail** | PASS | 41,448 combinations searched; unique hit positions {551, 557, 561, 563} → `szqu` |
| 102 | that zeroing confirmed on the full 570-digit integer | PASS | tail `b'szqu'` (`73 7a 71 75`) |
| 103 | **prefix lengths 450–570 whose top byte is a lowercase letter** | PASS | `[455, 467, 508, 520, 561]` (top bytes `m c r h w`) |

Cross-check: `check_report3_2026-10-17.py` independently prints
"faed a=1..9: first 4 bytes 1bd5951d, last 4 c7bbc075, printable 78/237" and
"of 362,880 orderings … squares giving btcseed: 8 … continuations {'btcseedd'}".

The [T, measured] statistics in §6.3 (χ² = 43.7, digram/period/homogeneity
p-values, entropy 3.120, change-point and hypergeometric p-values, the
"16 shorter periods starting btc" shuffle calibration) are tagged [T], not
[V]; not re-run, not counted.

## §7.1 — Message #8446 — task item (d)

The message was extracted from Appendix A itself (`[#8446] 2023-02-23
18:20:03`), not from the §7.1 summary.

| # | check | result | exact value |
|---|---|---|---|
| 104 | **161 groups of 8 bits** | PASS | 161 groups, 1288 bits, all chars `0`/`1` |
| 105 | **reversing the whole bit string and reading 8 bits/char gives the printed string exactly** | PASS | 161 chars, sha256 `d13afe77dd6969a438e2020cc3df22e0e7d589ae88196caa9162c9168e25a018` |
| 106 | decoded string, in full | PASS | `yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyangwewontgiveawaythepassworditsinfrontofyoureyesbutyourenotseeingitverylaststepisatruegiveawaypromised` |

Note the operation is a reversal of the entire 1288-bit string (not a
per-byte bit reversal); the per-byte alternative does not produce this text.

---

## Not reproduced (explicitly not counted as PASS or FAIL)

1. **§3.1 QR payload** ("The QR code decodes to
   `https://www.blockchain.com/btc/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`").
   No QR decoder is available in this offline environment (no
   OpenCV/pyzbar/zbar; the only QR code found on the box is an encoder,
   `qrcode-terminal`). The QR is present on the poster at lower left, next to
   the printed address (visually confirmed, #24 note), but its decoded
   payload was **not** machine-verified. This is the one [V] byte claim in
   the requested sections that this run does not cover.
2. **§1 on-chain facts** (funding 2019-04-13 block 571,497; spends
   2020-05-11 block 630,001 and 2024-04-24 block 840,725 to
   `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`, balances). These are not derivable
   from any file in the workspace and verifying them would need chain data;
   offline limit. Everything in §1 that *is* derivable from the printed
   address/pubkeys — including second-build item (a) — passes (#3–#11).
3. **[T, measured] statistics** in §6.3 (χ²/G-test/hypergeometric/
   change-point p-values, shuffle nulls, entropy) are labelled [T] in the
   file, outside the "[V] reproduction" scope of this task; not re-run.

## Files

- `src/archivist_check2.py` — new script; reads only the second-build
  handoff and the poster. Run: `cd /workspace && python3 src/archivist_check2.py`
  → `106/106 checks passed, 0 failed` (runtime ~2 s).
- Prior work re-run but not modified: `src/step0_trust.py` (49/49 PASS; note
  it still points at the first-build file — its extractions agree with the
  new script on every shared item, consistent with the second build's own
  statement that sections 3–5 and Appendix A are unchanged), and
  `src/check_report3_2026-10-17.py` (numbers quoted above).
- This report: `ledger/01-archivist.md`.

## Bottom line

**Total: 106 PASS / 0 FAIL in the new script (plus 49/49 in the prior
step-0 run). No mismatch byte was found anywhere.** Every exact byte, hash,
salt, count and decoded string printed in sections 1, 3.1, 3.4, 4.1–4.4, 5,
6.1, 6.2, 7.1 and the [V] items of 6.3 — including second-build items
(a) compressed hash160 `06bbdc66fda09110435c79a86656a604c2d5c69b`,
(b) the dbbi host/greedy/filler/bit-string/continuation facts,
(c) the faed counts, Bifid sha256 `15d62c82…d0507`, whole-integer head/tail
`1bd5951d`/`c7bbc075` and all four search results,
(d) the #8446 reversed-binary string, (e) all three containers, and
(f) the SalPhaseIon path hash — reproduces byte for byte from the new file.
The single uncovered [V] item is the QR payload (no offline decoder), and
the §1 on-chain facts are not derivable from the workspace files.
