# Steps

> Byte convention: all phase plaintext sizes and fixed byte offsets below refer to the original CRLF decrypted bytes (zero-based, inclusive ranges). The committed LF files are 642 / 4032 / 2411 bytes for Phases 2 / 3 / 3.2. See README for both representations and hashes. Use the validated section extractor in `mywork/candidate_pool.py` for prose; do not slice the LF files at CRLF offsets.

Unmarked values were recomputed from the files in `files/` on 2026-10-06.
Values marked **[kit]** are copied from the source kit's records and were not recomputed here.

---

## Step 0 — Poster

Input: `files/puzzle.png`

The top of the image is a 14 x 14 grid of 75-pixel cells. Majority colour per cell
(K `#000000`, W `#FFFFFF`, B `#3F48CC`, Y `#FFF200`, F `#FEFEFE`):

```
WWKKWBWWKWKKWY
KKBKWWKKKWBWKK
KKWKKKWBWWKWWK
WKKWBWWWWKKKWK
WBKWWWKKWYWKKW
KWWKKWYWKWYWKK
KWWBKKWWWKWYWW
BKKWFWWWWWKWYW
WWWKKBWKKKKKWB
KKBKKKYWKKWWWK
KKWKWWWYWKKWKK
KKKKWWKWBWKKWW
WBWKKKWKWYWKKW
WKBWKKWKKWBWKK
```

Cell counts: K 86, W 85, B 15, Y 9, F 1. The F cell is at row 7, column 4 (0-based).

Method: read the cells as a spiral starting at the top-left cell, going down first,
counter-clockwise inward. K and B = 1; W, Y and F = 0. Take 8 bits per ASCII character.

196 bits:

```
0110011101110011011011010110011100101110011010010110111100101111
0111010001101000011001010111001101100101011001010110010001101001
0111001101110000011011000110000101101110011101000110010101100100
0000
```

Output (first 192 bits): `gsmg.io/theseedisplanted`

The QR code on the poster encodes
`https://www.blockchain.com/btc/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` **[kit]**

---

## Step 1 — Phase 1

Input: `files/theseedisplanted.html`, the eight tile images

The page shows eight images in this order, followed by a form that posts to
`/phase1verification`.

| tile file | content **[kit]** |
|---|---|
| `black_banking - war.png` | bank icon, `war` |
| `blue_ca.png` | `CA` |
| `blue_dig_i.png` | `dig i`, `+` |
| `blue_lock_lo.png` | closed padlock, `lo` |
| `red_crypto_gic.png` | `crypto`, `gic` |
| `red_n_you.png` | `n you` |
| `red_open_lock_n_ing.png` | open padlock, `n ing` |
| `red_t.png` | `t`, `-` |

Tile pairings **[kit]**: `CA` + `n you`, `dig i` + `t`, `lo` + `gic`, `war` + `n ing`
→ CAN YOU DIG IT, LOGIC, WARNING → the song "The Warning" by Logic.

Answer **[kit]**:

```
theflowerblossomsthroughwhatseemstobeaconcretesurface
```

sha256 of the answer: `5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75`

Result **[kit]**: redirect to
`gsmg.io/choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself`
(`files/phase2_choice.html`).

---

## Step 2 — Phase 2

Input: `files/phase2_choice.html`, `files/phase2.b64`

Page text above the container:

```
"1... are you looking for the private keymaker?"
You come to me, without it. Come to me with it and you'll have the power to continue. It'll grant the first part.
/(aaa, connected enf)

Ciphered with aes-256-cbc /w base64 sha-256(password)
```

Answer: `causality`
Password: `eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf`

Output: `derived/phase2-plaintext.txt` (648 bytes, CRLF line ends)

```
The ironic 2name of the keymakers trying to protect the current digital powers which are still in severe danger due to the keymaker's way of security by hiding, nearly unprotected, in plain sight. {eps3.4_[in one of the valleys of Phillip]runtime-error.r00., where daughters hit magic keypads} When this fails.. Crypto finally to the latin 3Moon? Tell me, 4How so mate?
# X 2 S H 4 Y 0 Q B 15 #
Q -> extend the name of a hackers' swordless fish, the I and W are below.
B -> ((BV80605001911AP)- (sqrt(-1)))^2
H -> (Answer to only this puzzle but nothing else) * -1
S -> cha' + (vagh * jav)
Ok kid, on the highway, let put it in the worst gear.
```

---

## Step 3 — Phase 3

Input: `files/phase2_choice.html`, `derived/phase2-plaintext.txt`, `files/phase3.b64`

Page instruction: `--> parts 1..7 --> sha-256 -> dgst is the password to enter Phase 3.`

The answer is the concatenation of seven parts, with no separator.

| part | value | source text |
|---:|---|---|
| 1 | `causality` | page: `"1... are you looking for the private keymaker?"` |
| 2 | `Safenet` | Phase 2 plaintext: `The ironic 2name of the keymakers ...` |
| 3 | `Luna` | Phase 2 plaintext: `Crypto finally to the latin 3Moon?` |
| 4 | `HSM` | Phase 2 plaintext: `Tell me, 4How so mate?` |
| 5 | `11110` | page: `The 5binary code is a part of the piece of this puzzle.` |
| 6 | `0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854` | page: `Its' raw data after 4 on row 1616 ...` |
| 7 | `B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1` | page: FEN `B5KR/1r5B/6R1/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 w - - 0 1`, then `And now a buddhist is forced to move. What will be the next situation?` |

Derivations of the parts **[kit]**:

- Part 2. The Phase 2 template `# X 2 S H 4 Y 0 Q B 15 #` with Q = 82, B = 25, H = 42, S = 32.
  The clue for H evaluates to −42; the derivation uses 42.
  Reverse the sequence, then reverse the digits of each number:

  ```
  printed        X    2    S    H    4    Y    0    Q    B    15
  reverse seq    15   B    Q    0    Y    4    H    S    2    X
  substitute     15   25   82   0    Y    4    42   32   2    X
  reverse digits 51   52   28   0    Y    4    24   23   2    X
  coordinate     51°52'28.0" N  4°24'23.2" E
  ```

  The coordinate is the SafeNet office, Seattleweg 5, Rotterdam-Pernis.
- Part 3. Latin for moon.
- Part 4. Initials of "How so mate".
- Part 5. Executive Order 11110. Reasoning from the Phase 2 riddle
  (`files/phase2_choice.html`, paragraph beginning "There's a guy who theorised"):

  | riddle clue | reading | status |
  |---|---|---|
  | "Any linear electrical network ... equivalent current source Ino ... Rno" | Norton's theorem, so the man is Norton | from the text |
  | "He might have been insecure. His competition..." | Norton (security software); the competition is John McAfee | from memory |
  | "after enough belikins ... a ruler of ... the poorest ... planet" | Belikin is a Belize beer; McAfee lived in Belize. McAfee's 2016 run was for U.S. president, not Belize. The "poorest land" clue is not resolved. | partly checked |
  | "4 rulers have shared the first name of the competition" | first name John: John Adams, John Quincy Adams, John Tyler, John F. Kennedy | from memory |
  | "Another had a resemblance to Carrey, James Gates, also Simulacra and Simulation" | Harry S. Truman, via *The Truman Show* (Jim Carrey; a staged-world film discussed alongside Baudrillard's *Simulacra and Simulation*). Inference, not sourced. Truman issued EO 10289, which EO 11110 amends, so the link to the order holds. | inferred |
  | "One of the rulers had a number, and dirty too" | not resolved. Community notes (`mywork2/web/puzzlehunt_readme.md`) say JFK; that conflicts with "the one after died too soon." | open |
  | "The one after died too soon" | John F. Kennedy (assassinated 1963) | from memory |
  | "never execute an order that revokes the highest power" | Executive Order 11110, signed 4 June 1963; it amends EO 10289 "By revoking subparagraphs (b) and (c) of paragraph 2" | checked (Presidency Project excerpt) |
  | "The 5binary code is a part of the piece" | 11110 is five binary digits and the order number | from the text |

  The clues "2 had the firstname in the surname", "One of the rulers had a number, and dirty too",
  the Carrey resemblance, and "floating zerg house" are not decoded here, so the chain is not fully
  verified. The answer `11110` matches the value accepted in the Part 3 concatenation above.
- Part 6. The Bitcoin genesis block headline
  `The Times 03/Jan/2009 Chancellor on brink of second bailout for banks`,
  bytes reversed, as uppercase hex with a `0x` prefix (140 characters).
  Source of the phrase "its raw data after 4 on row 1616": Bitcoin's `main.cpp`, line 1616 (the
  link in the riddle is `main.cpp#l1616`). The genesis code there is
  `txNew.vin[0].scriptSig = CScript() << 486604799 << CBigNum(4) << vector<unsigned char>(pszTimestamp, ...)`,
  and a comment on the same block reads `txNew.vin[0].scriptSig = 486604799 4 0x736B6E…4854`. The hex
  after "4" is Part 6. The comment text was checked in the saved source copy; the exact gutter line
  number was not confirmed.
- Part 7. The page's FEN after the move Rg6–c6.

Format tags on the page: `/(aaa, connected enf)` beside part 1, `/(aBa, connected enf)` beside
part 6, `/(aBa, connected not enf)` beside part 7.

Answer length: 227 characters
Password: `1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5`

Output: `derived/phase3-plaintext.txt` (4,090 bytes). Bytes 0–725 are text; the rest is the
Phase 3.2 container in base64 (identical to `files/phase3.2.b64`).

```
What if the merovingian is wrong. What instead of causality something else could be ours? Therefor, if so, the ...... is ours. The thinker's 1name behind all of that would grant you access to the next step (of humanity). Definitely look into his works might you have time. /(aa,connected enf)

I just passed a cheshire cat and I'm getting fed up with this puzzle.. It's taking forever. But, How long is forever? I don't know, but just add giveit in front of the answer and you can fall in the keyhole. /(aa,connected enf)

3.The fundamental limit to the precision with which certain pairs of physical properties are know. /(aa,connected enf)

Phase 3.2 is ciphered with aes-256-cbc base64 and a sha256 pw, yet again.
```

---

## Step 4 — Phase 3.2

Input: `derived/phase3-plaintext.txt`, `files/phase3.2.b64`

| riddle | answer |
|---:|---|
| 1 | `jacquefresco` |
| 2 | `giveitjustonesecond` |
| 3 | `heisenbergsuncertaintyprinciple` |

Answer (concatenation, no separator):
`jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple`
Password: `250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c`

Output: `derived/phase3.2-plaintext.bin` (2,422 bytes)

| bytes | content |
|---|---|
| 0–446 | ASCII text |
| 447–1985 | 1,539 non-ASCII bytes (step 4a) |
| 1986–1989 | `0d 0a 0d 0a` |
| 1990–2138 | 149 digits (step 4b) |
| 2139–2142 | `0d 0a 0d 0a` |
| 2143–2291 | ASCII text |
| 2292–2421 | Terminal container in base64 (identical to `files/terminal.b64`) |

Bytes 0–446:

```
I've been waiting for you. You have many questions, and although the process has altered your consciousness, you remain irrevocably human. Ergo, some of my answers you will understand, and some of them you will not. Concordantly, while your first question may be the most pertinent, you may or may not realize it is also irrelevant.

... am I here? Wake up, you... I've designed you a beautiful strategic position. One for one, four for one.
```

Bytes 2143–2291:

```
Raising the stakes without extra chances of winning. A fubcd-king & oracle-queen, thingky mvps, on a sad board but as wide as the first one seen.
```

### Step 4a — Bytes 447–1985

Method: decode the bytes as latin-1, encode as cp273 (all 1,539 results are lowercase
letters), then Beaufort decrypt `P = K − C mod 26` with key `THEMATRIXHASYOU`.

Output: `derived/architect-text.txt` (1,539 letters, no spaces)

```
YOURLIFEISTHESUMOFAREMAINDEROFANUNBALANCEDEQUATIONINHERENTTOTHEPROGRAMMINGOFTHIS
PUZZLEYOUARETHEEVENTUALITYOFANANOMALYWHICHDESPITEMYSINCERESTEFFORTSIHAVEBEENUNAB
LETOELIMINATEFROMWHATISOTHERWISEAHARMONYOFMATHEMATICALPRECISIONWHILEITREMAINSABU
RDENTOSEDULOUSLYAVOIDITITISNOTUNEXPECTEDANDTHUSNOTBEYONDAMEASUREOFCONTROLWHICHHA
SLEDYOUINEXORABLYHEREYOUYOUHAVENTANSWEREDMYQUESTIONMEQUITERIGHTINTERESTINGTHATWA
SQUICKERTHANTHEOTHERSPLEASEIFYOUFINDAWAYTOCOMPLETETHELASTPARTOFTHEPUZZLETAKETHEP
RIVATEKEYYOUVEEARNEDITBUTPLEASETAKETHISTOHEARTTHATWHATAWISEMANABOVEHINTEDATISWOR
THHUNDREDFOURTYOFTHEINVESTMENTTHATSWHATUSGUYSATGSMGARETRYINGTOACCOMPLISHINTHEEND
PLEASEJUSTHELPUSBUILDITINSTEADOFJUSTWAISTINGYOURLIFETIMEBYHUNTINGFORWORTHLESSPRI
CESANDTHROPHIESLIKETHISIMSORRYTOTELLYOUTHATYOUVECOMETHISFARBUTYOULLNEVERFINISHTH
ELASTTASKIEXPECTYOUTOSAYBULLSHITWELLDENIALISTHEMOSTPREDICTABLEOFALLHUMANRESPONSE
SBUTRESTASSUREDTHISWILLNOTBETHELASTTIMEIHAVEDESTROYEDARESTLESSSOULANDIHAVEBECOME
EXCEEDINGLYEFFICIENTATITTHEFUNCTIONOFTHEYOUISNOWTORETURNTOTHESOURCECODESALLOWING
ATEMPORARYDISSEMINATIONOFTHECODEYOUHOPEFULLYCARRYREINSERTINGTHEPRIMEBASICSAFTERW
HICHYOUWILLBEREQUIREDTOSELECTFROMOVERTWENTYTHREECIPHERSSIXTEENENCRYPTIONSANDORSE
VENINTERTWINEDPASSWORDSTOFINDTHEACTUALPRIVATEKEYNOTETHATALSOBRUTEFORCINGMIGHTBER
EQUIREDFAILURETOCOMPLYWITHTHISPROCESSWILLRESULTINACATACLYSMICSYSTEMCRASHKILLINGY
OURWILLPOWERWHICHCOUPLEDWITHTHEEXTERMINATIONOFYOURWILLTOLIVEANDWILLULTIMATELYRES
ULTINTHEEXTINCTIONOFTHEENTIRENESSOFYOURSELFSELFGOODLUCKNEVERTHELESSIREALLYHOPEYO
URETHEONECIAOBELLAO
```

### Step 4b — Bytes 1990–2138

Input digits (149):

```
15165943121972409169171213758951813141543131412428154191312181219433121171617137
149110916631213131281491109166131412199114371612126021664313711154112
```

Method: straddling checkerboard. Digits 1 and 4 select the second and third rows.

```
     0 1 2 3 4 5 6 7 8 9
     F   U B   C D O R A
1    . L E T H I N G K Y
4    M V P S / J Q Z X W
```

Output: `derived/checkerboard-plaintext.txt` (91 letters, no spaces)

```
INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE
```

---

## Step 5 — SalPhaseIon page

Input: `files/salphaseion_phase3.html`

Page location: `gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32`, where
the hex string is `sha256("GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe")`.
How the page was found **[kit]**: the word `HASHTHETEXT` from an audio file at Decentraland
parcel (−41, −17).

The page has two textareas, headed `SalPhaseIon` and `Cosmic Duality`.

### First textarea

`files/salphaseion-textarea.txt` (1,075 characters after removing whitespace). Runs by
character set, with the runs that decode:

| offset | length | characters | content | decode |
|---|---:|---|---|---|
| 0–90 | 91 | `a`–`i` | `dbbibfbh…eeeabe` | |
| 91–194 | 104 | `a`, `b` | `abbabbab…bbbabaa` | `matrixsumlist` |
| 195–764 | 570 | `a`–`i` | `faedggee…hfahiihic` | |
| 765 | 1 | `z` | `z` | |
| 766–828 | 63 | `a`–`i`, `o` | `agdafaoaheiecggchgicbbhcgbehcfcoabicfdhhcdbbcagbdaiobbgbeadedde` | `lastwordsbeforearchichoice` |
| 829 | 1 | `z` | `z` | |
| 830–858 | 29 | `a`–`i`, `o` | `cfobfdhgdobdgooiigdocdaoofidh` | `thispassword` |
| 859 | 1 | `z` | `z` | |
| 860–894 | 35 | text | `shabefourfirsthintisyourlastcommand` | |
| 895–958 | 64 | base64 | `U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z` | |
| 959–998 | 40 | `a`, `b` | `abbaabababbabbbaabbbabaaabbaabababbbaaba` | `enter` |
| 999–1062 | 64 | base64 | `QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ` | |
| 1063–1074 | 12 | text | `shabefanstoo` | |

Decode methods:

- `a`, `b` runs: `a` = 0, `b` = 1, 8 bits per ASCII character.
- `a`–`i`, `o` runs: `a`–`i` = 1–9, `o` = 0; read the digits as one decimal integer,
  write it in base 16, read the hex as ASCII.

The two base64 runs joined are the SalPhaseIon short container (`files/salphaseion-short.b64`).

### Second textarea

The Cosmic Duality container (`files/cosmic-duality.b64`).

---

### Step 5a — Reproduced partial constructions (2026-10-15 UTC)

These are conditional constructions, not a solved stage. Exact scripts, complete outputs, controls and limitations are in [the cryptanalysis report](review_leads/cryptanalysis_2026_10_15/README.md).

For DBBI, the grammar that consumes `b` or `be` at prime logical positions and one character elsewhere has 83- and 84-cell solutions. In the 84-cell branch, replacing prime `b` by minus its position, `be` by plus its position, and other letters by A1 values, then summing the columns of a row-major 7×12 matrix, gives `[-45,34,37,37,-73,30,49,38,32,44,-124,42]`. Modulo 26 with A=0, this is `HILLFEXMGSGQ`. The sign rule and matrix arrangement are hypotheses.

Deduplicating DBBI followed by the natural alphabet without J produces `dbifhcegaklmnopqrstuvwxyz`. Full-period Bifid decoding of FAED starts `btcseed` and re-encodes exactly. Pair source positions `i` and `i+285`: their row coordinates generate the even output stream, and their column coordinates generate the odd stream. The four-letter row alphabet is forced by the source letters lying in the square's first two rows.

The header occupies both streams. Removing it leaves a 282-letter carrier and 281 row symbols. A proposed mod-25 Hill inverse `(2,4;21,9)` on the carrier starts `ifindonvfrvodtfmdryqw`; the continuation is unexplained. The 58 occurrences of singleton-column `h` force 58 row bits to zero. Removing those determined bits gives 512 bits including eight header bits, or **504 bits / 63 bytes after the header**. No complete instruction, seed derivation, or remaining container decrypt is established.

---

## Step 6 — Not decrypted

No password is known for these three containers.

| container | file | where it appears | ciphertext bytes |
|---|---|---|---:|
| Terminal | `files/terminal.b64` | end of the Phase 3.2 plaintext | 80 |
| SalPhaseIon short | `files/salphaseion-short.b64` | first textarea of the SalPhaseIon page | 80 |
| Cosmic Duality | `files/cosmic-duality.b64` | second textarea of the SalPhaseIon page | 1,328 |

---

## On-chain checkpoints

For each string below, `sha256(string)` used as a private key gives the listed address
(P2PKH, compressed public key). Each address received a payment with the listed
OP_RETURN text from `3GSMG24TujqfMJG1kQoBX18DzJHQLeJYMK` on 2020-03-24 **[kit]**.

| string | address | OP_RETURN **[kit]** | block **[kit]** |
|---|---|---|---:|
| `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` | `1GyT5WrLYpwFkuiVoPDJZa1Q6jtjbjuBff` | `GSMG.io: do you beleive me you need it?` | 622762 |
| `causality` | `1Jqq37KkZEt4F3Dt6qXdtyiMEFBBdawbkJ` | `GSMG.io: Right, this is causality` | 622762 |
| the 149 digits of step 4b | `18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc` | `GSMG.io: part of the cipher` | 622766 |
| the Phase 3.2 answer | `1K23RS1y2fnuZRkhw5nUpFr5Jk5WN11Zeq` | `GSMG.io: phase3.2 pass OK` | 622767 |
| the Phase 1 answer | `1AD2wfwXukZ1kUAy848hTQQ72aSBZPB75r` | `GSMG.io: are you sure?` | 622767 |
| the 227-character Phase 3 answer | `1M5ypvDbp124ZtKPbg3GJg1JqNs1x7TPoN` | `GSMG.io: You are here because 227 chars were correct` | 622774 |

The bytes of `gsmg.io/theseedisplanted` used directly as a private key (left-padded to 32
bytes) give `148XH2YBmLr4oAJXQcG84FpNYoBmqnVPHQ`; the same 192 bits in reverse order give
`13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp`. Each received a payment with OP_RETURN
`Good job, Neo!` from the same address in block 624209 on 2020-04-03 **[kit]**.

