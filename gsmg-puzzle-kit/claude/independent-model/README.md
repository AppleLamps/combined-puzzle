# Independent re-derivation of the GSMG next gate (3 October 2026)

**6 October 2026 interpretation notice.** This is a dated research record.
Its candidate counts and original logs are preserved, not freshly rerun.
Read [doc 118](../118-correctness-audit-remediation.md) for detector/coverage
limits and [doc 119](../119-current-evidence-ledger.md) for current findings.
A null applies only to its complete tested tuple.

DBBI/FAED purpose and the first-SHA/enter/anstoo interpretation remain open. The entire return-to-the-Source clause was not inserted by the puzzle creator; distinguish inherited film wording from edits and transcript variants.

Phase A was written from the primary files only (page captures, textarea, containers, dbbi, faed,
Architect letters, matrix.json, keys.json, jrk_messages.txt) plus the solved answers. Phase B then
compared it with the dossier, doc 115, the critical review and the riddle ledger. Phase C tested the
divergences that give one reading or one exact operation.

## Phase A: my model

**Two routes, two halves.** The poster opens two doors. The main route runs poster, phase 1, 2, 3, 3.2
and ends in the Terminal container. The side route runs from the hash of the poster's text to the
SalPhaseIon page (textarea, short container, Cosmic Duality). The checkerboard says "the private keys
belong to half and better half". The two 80-byte containers are the same size, and 80 bytes of
ciphertext is exactly what a 64-character hex string (plus padding, or plus a newline from `echo`)
produces. So my working model: each short container holds one 64-hex value, and Cosmic Duality is the
long message the creator calls the next phase ("yinyang", #39237).

**The textarea is a terminal transcript.** `enter` sits exactly where `openssl -a` breaks base64 at 64
characters, so the page shows what someone typed. Read top to bottom it says: verify the poster
(dbbi), `matrixsumlist`, filler, `lastwordsbeforearchichoice`, `thispassword`, "sha256 our first hint
is your last command", the container, "sha256 the answer too". The creator's own order (#8446) is
yellowblueprimes, matrixsumlist, lastwordsbeforearchichoice, yinyang. Yinyang is the step after the
short container opens.

**dbbi is a tutorial.** Its hosts write each colour's alphabet number in a..i digits: blue is `b` (2,
B) and yellow is `be` (25, Y). That is "Yellow has a number and so does Blue" made literal, and it
teaches the page's number-as-letters convention. The two leftover program symbols spell `BY`.

**Labels per lock (where I differ most).** The Terminal is the only container with no riddle beside it,
and it is named after the place you type commands. Two readings follow, and they cannot both be true:

- `thispassword` belongs to the Terminal: the side page supplies the main route's missing password.
- "sha256 our first hint is your last command" describes the door you came through (sha256 of the
  poster's text is the side page's URL) and is consumed, leaving "sha256 the answer too" as the short
  container's instruction.

**"Our first hint".** The creator's first message that calls itself a hint is #867, "giveit =
givetit" (and #879 calls it "yesterday's 'hint'"). #225 was "a hash which we provided". #8446 then says
"it's in front of your eyes" and "very last step is a true giveaway", both echoing phase 3's "just add
giveit in front of the answer".

**"Raising the stakes without extra chances of winning"** is a separate sentence from the
checkerboard key that follows it. Either it is the halving to the better-half address you cannot win,
or it is key stretching (`openssl -pbkdf2` / `-iter`), which raises an attacker's cost without
changing anyone's odds. OpenSSL 1.1.1, current when the puzzle launched, prints a warning recommending
exactly that.

**"Matrix" means "this puzzle".** The creator swapped "the programming of the matrix" for "the
programming of this puzzle" in the Architect text. The puzzle's own matrix, the poster, sums to 101 set
cells, a prime, and 101 is Neo's room number in the film.

**The Architect's choice inside 3.2.** The 3.2 intro has the Architect say "I've designed you a
beautiful strategic position. One for one, four for one." That last sentence picks the checkerboard's
blank digits {1, 4}, the only choice the 3.2 Architect makes. The last words before it are "a beautiful
strategic position".

**Surplus.** `BY` (above). The trailing O of CIAOBELLAO is a zero under the page's o = 0 rule. "In front
of your eyes but you're not seeing it" describes infrared, and the creator posted "Infrared" (#6250)
four days after his "prime part" slip. Both point at the off-white cell as an anchor, not at a string.

**Convention assumptions I would question.** sha256-hex: keep it, since the page says "sha256 the
answer too". AES-256-CBC with EVP SHA-256: the opened pages named their cipher, but none of the three
locked containers does. The three containers as the only targets: another URL is ruled out by #9607
("No need. You have all the info."), so the win test on candidates as scalars is the only other gate.

## Phase B: where my model diverges from the dossier and ledger

| # | point | dossier / ledger | mine | testable? |
|---|---|---|---|---|
| 1 | which lock each instruction serves | one joint password for the short container; Terminal unexplained | `thispassword` may serve the Terminal; the sha256 line may describe the door | not alone: both still need the operand |
| 2 | "our first hint" | #225, a statement about method | #867 "giveit = givetit", plus "add giveit in front" as the last command | yes (N1, N2) |
| 3 | "Raising the stakes..." | unexplained, or the object the stakes are raised on | key stretching, or the halving | yes, as PBKDF2 (C1) |
| 4 | cipher and KDF | AES-256-CBC, EVP SHA-256/MD5 for every riddle answer | unstated for all three locks | yes (C1) |
| 5 | matrix sum | poster sum lists, the film's "sum" sentence | 101: the poster's total and Neo's room | yes (J5) |
| 6 | archi's choice | film door scene, puzzle Architect before SELECT, 3.2 intro windows ending at its last word | the {1, 4} blank choice; the words before it | yes (J6) |
| 7 | `thispassword` | assembly instruction | possibly self-referential: the encoded form is the password | yes (J1) |
| 8 | dbbi hosts | re-encode the colour program | a1z26 numbers of B and Y; leftover spells BY | no password |
| 9 | "in front of your eyes" | Looking Forward (#60312 Bingo) | infrared, the off-white cell | no candidate |

## Phase C: tests

`ct.py` takes candidates and tries every locked container under 4 password forms (raw, hex sha256,
double hash, hex of hex) x 5 KDFs (EVP MD5, SHA-1, SHA-256, SHA-512, PBKDF2-HMAC-SHA256 at 10,000, the
`openssl -pbkdf2` default) x 14 ciphers (AES-128/192/256 CBC and ECB, Camellia-128/192/256, SEED, SM4,
3DES, Blowfish, CAST5). ARIA is missing because the Python library lacks it. Each valid pad goes through
the historical `rt.judge` ranking (pad >= 3, printable, nested, bit bias, key windows), and every candidate gets the win test. Doc 118 later separated complete padding-valid retention from ranking; the old record does not certify retention of unranked pad-1/2 output.

**Controls.** The key-1 check and phase 2/3/3.2 open (from `rt.controls`). Eleven planted 80-byte
containers are recovered: seven made by the openssl 3.0.13 CLI (AES-128 MD5, Camellia-256 SHA-256, 3DES
SHA-1, AES-256-ECB SHA-512, AES-256 `-pbkdf2`, SM4 `-pbkdf2`, AES-192 SHA-256) and four built in Python
(Blowfish, CAST5, SEED, Camellia-128).

| file | what | candidates | decrypts | valid pads | flags |
|---|---|---:|---:|---:|---:|
| `new1.txt` + ledger R1-R14 | N1-N5 (first hint, giveit in front, core chain under new ciphers/KDFs, Terminal neighbours, surplus) and every ledger answer re-run under the new matrix | 267 | 224,280 | 848 (~880 expected) | 0 |
| `new2.txt` | J1 self-reference, J5 101, J6 3.2 choice, crossed with each other and with R1/R2/R3/R7/R8/R11/R12/R14 | 261 | 219,240 | 854 (~860) | 0 |

Total: 528 candidates, 443,520 decrypts, 0 flags, 0 win-test hits. Logs: `run1.log`, `run2.log`.

## What the nulls say

- Every riddle answer the project has written down is now also null under 13 other ciphers and under
  PBKDF2. If the right answer were already in the ledger, a non-default cipher or `-pbkdf2` was not
  hiding it.
- The readings in rows 2, 3, 5, 6 and 7 are spent as stated.
- Rows 1, 8 and 9 do not give a password by themselves. Row 1 is the one I would build on: if the
  Terminal's password is the side page's `thispassword`, the Terminal and the short container are
  separate locks with separate answers, and a candidate that fails on one container should not be
  crossed with its partner as a single string.

## Round 6: the per-lock split (3 October 2026)

**New frame.** The creator says breaking SalPhaseIon gives "the feeling of the phase's name" (#6497):
salvation. In the film, the Architect's choice is two doors. The right one "leads to the Source, and the
salvation of Zion", and the creator inserted "return to the source codes" into his Architect text. The
left one "leads back to the Matrix, to her, and to the end of your species". So the side route
(SalPhaseIon) is the right door, the main route (ending in the Terminal) is the left door, and Cosmic
Duality is the pair. The dossier has no "salvation" or "Trinity" reading.

**Assignment, one sentence each**

| element | lock | why |
|---|---|---|
| dbbi / yellowblueprimes | none | verifies the poster's colour layer; the creator's step 1, consumed |
| `matrixsumlist` + "sha256 our first hint is your last command" | short | the sha256 line is the method line directly above the short container (riddles, method line, container is the grammar of phases 2, 3 and 3.2), and the page's first hint is `matrixsumlist` |
| `lastwordsbeforearchichoice` + `thispassword` | Terminal | `thispassword` names a password with no container beside it, and the Terminal is the only lock with no riddle of its own; it sits at the end of the Architect's plaintext |
| "Raising the stakes without extra chances of winning" | Terminal | the sentence directly above it; the halving to the better-half address, which no one can win |
| "sha256 the answer too" + the Cosmic Duality heading | Cosmic | sits between the short container and the Cosmic heading; yinyang is "the next phase" after an AES decode (#39237) |

**Rejected alternatives**

- Everything on the page goes to the short container (the joint model): the answers can't be checked
  one at a time, and the crosses are null (doc 114, R4, R9).
- The sha256 line goes to the Terminal ("command" fits a terminal): the implied answer is sha256 of
  the first hint, already null as R5 and R16.
- `matrixsumlist` goes to the Terminal: its answers are null alone on every lock (R1, R8, R11 to R14,
  R19, and 1,558 poster lists).
- "sha256 the answer too" goes to the short container: that only restates the convention.

**Implied answers, and which were already null**

| lock | implied answer | status |
|---|---|---|
| short | the `matrixsumlist` answer alone | **already null**: R1, R8, R11 to R14, R19, and 1,558 poster lists, each tried alone on every lock. No new single reading |
| short (door frame) | the right door's destination: `thesource`, `salvation`, `thesalvationofzion` ... | new, P4 to P5 |
| Terminal | the Architect's last words before he presents the doors: "...the Anomaly revealed as both beginning, and end"; or the words before his own word "choice": "As you adequately put, the problem is" | new, P1 to P2 (R2, R3 and R7 were the lines after the doors) |
| Terminal (door frame) | the left door's destination: "her", Trinity, the checkerboard's better half | new, P3 |
| Cosmic | sha256 of the short container's plaintext | **untestable** until the short container opens; `yinyang` alone already null (R6) |
| Cosmic (door frame) | the pair: `therearetwodoors`, `neoandtrinity` | P6 (`therearetwodoors` had only run under PBKDF2, T47) |

**Results** (`perlock.txt`): 25 candidates. Under the proven convention (`rt.py`): 1,200 decrypts, 3
valid pads against about 4.7 expected, 0 flags. Under the 14-cipher tester (`ct.py`): 21,000 decrypts,
81 valid pads against about 82 expected, 0 flags, 0 win-test hits. Controls fired in both. Logs:
`run3_rt.log`, `run3_ct.log`.
