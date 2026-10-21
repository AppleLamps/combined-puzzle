# The three locked envelopes: every angle, and what has not been tried

Written 12 Sep 2026 from the primary sources: envelope bytes, the archived SalPhaseIon page, the three opened plaintexts, the verified passwords and the creator's messages. Nothing was guessed or decrypted for this document.

## 1. What the bytes say

| | Terminal | SalPhaseIon | Cosmic Duality |
|---|---|---|---|
| Where published | Last lines of the Phase 3.2 plaintext (decrypted, so byte-exact) | SalPhaseIon textarea on gsmg.io/89727c59… (one Wayback capture, 2023-06-01) | Second textarea on the same page, under the heading "Cosmic Duality" |
| Salt | `b45a5e3d827593ca` | `3ab585348552415d` | `2d3f6fe06dc950e6` |
| Ciphertext | 80 bytes (5 blocks) | 80 bytes (5 blocks) | 1,328 bytes (83 blocks) |
| Possible plaintext length | 64–79 bytes | 64–79 bytes | 1,312–1,327 bytes |
| Format | `openssl enc -a`: two 64-character lines | Same; the wrapper's binary `enter` sits between the two lines | Same; 28 full 64-character lines, no `=` |
| Text around it | The checkerboard message ("IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF…") and "Raising the stakes without extra chances of winning." | `sha256 our first hint is your last command` before it, `sha256 ans too` after it | The heading only |

- **Length rules out a bare WIF.** A 51–52 character WIF would give 64 bytes of ciphertext, not 80. A 64-hex key gives exactly 80 bytes, with a full padding block, and so does a 64-hex key followed by LF. Other plaintexts that fit are `gsmg.io/` + 64 hex (72 bytes), a 12-word mnemonic, or a short sentence.
- **Cosmic is document-sized.** Its length would also fit a nested `openssl -a` envelope: a 960-byte envelope with CRLF lines, or 976 bytes with LF. The creator nested envelopes before (Phase 3 contained 3.2, and 3.2 contains the terminal envelope), but the length alone does not tell the two readings apart.
- **CBC with padding is effectively certain.** All three lengths are multiples of 16. A stream mode would give that by chance only 1 time in 4,096.
- **The salts carry no information.** They are OpenSSL's random bytes.
- **Integrity is settled.** SalPhaseIon's second line in the archived HTML matches the bytes used. `2nd_half_as_posted_corrupt.bin` is a community typo, and Diego's claim that the blob is "invalid" without the line break reflects OpenSSL's 64-column base64 rule, not a problem with the data.

## 2. What the creator's own conventions show (verified, not assumed)

| Opened stage | Where the cipher is stated | Password (sha256hex of) |
|---|---|---|
| Phase 2 | Page: "Ciphered with aes-256-cbc /w base64 sha-256(password)" | `causality` |
| Phase 3 | (same convention) | `causality` + `Safenet` + `Luna` + `HSM` + `11110` + `0x736B…` + FEN with its spaces: the previous answer, then seven parts in riddle order, in their natural case |
| Phase 3.2 | Phase 3 plaintext: "Phase 3.2 is ciphered with aes-256-cbc base64 and a sha256 pw, yet again." plus "just add giveit in front of the answer" | `jacquefresco` + `giveitjustonesecond` + `heisenbergsuncertaintyprinciple`, with no earlier answer in front |

- **The creator states the recipe next to each envelope.** Every opened envelope comes with an explicit cipher and preprocessing statement. The locked ones have none, except SalPhaseIon's two "sha256" phrases.
- **He hashes text without a trailing newline.** None of the three verified passwords includes one. He also linked an online SHA-256 generator (#234, 2019).
- **Plaintexts are Windows text.** They use CRLF line endings with no final newline and embed base64 at 64 columns, which points to the OpenSSL command line on Windows.

## 3. What the creator said about the envelopes and the key

- #2918 (2020): asked whether the private key is in the last cipher of Phase 3.2, he said: "There must at least be something hidden in there."
- #7830–#7834 (2021): "Technically we do [store the private key online]"; "The one to be found by solving the puzzle yes"; "And the solver will find a way to 'decrypt' it." The key is in material that is online. Before July 2026 the only such material not found inside a decrypted plaintext was the SalPhaseIon page: DBBI, FAED, the SalPhaseIon envelope and Cosmic.
- #8569 (2023): the terminal block is undecrypted (correct), and it is not the SalPhaseIon hint (no).
- #9607 (2023): "No need. You have all the info." This answered someone asking for another URL or planning a big brute force.
- #39237 (2025): yinyang "is the next phase". The question it answers asked whether yinyang is found after decoding an AES ciphertext, but that question was edited later.
- #63957 (2026): the sites being down does not affect resolving SalPhaseIon or Cosmic ("The puzzle is still valid!"). **Opening these envelopes, and whatever follows, does not need gsmg.io.**
- The 2023 binary runs `yellowblueprimes` → `matrixsumlist` → `lastwordsbeforearchichoice` → `yinyang`. That is the SalPhaseIon wrapper's order, continued past it to yinyang, which is Cosmic Duality.

## 4. Reading each envelope's own text for meaning

- **Terminal.** "Raising the stakes without extra chances of winning" is the one sentence in that section that does no other work: the alphabet comes from the next sentence. It sits directly above the envelope. Read literally, it says this envelope raises the stakes but does not improve your chances of winning. The message above it says that anyone who cracks "this" should know the private keys belong to the creator and partner. Together these read as a side prize or a plea, not a step toward the prize. This is an interpretation; the creator confirmed only that the block is undecrypted.
- **SalPhaseIon.** This is the only envelope that has local instructions. They go: matrix sum list → last words before the Architect's choice → this password → sha256 of our first hint is your last command → [envelope, with "enter" between its lines] → sha256 the answer too. The password inputs are named but come from DBBI and FAED, which are still undecoded.
- **Cosmic.** There is no local recipe, so its password must come from somewhere else. The 2023 recipe and #39237 place yinyang (Cosmic) after the SalPhaseIon steps. Guessing Cosmic's password directly is the least supported attack of the three.

## 5. What has been tried

About 8–9 million decryptions of hand-built candidates, 8.1 million of them in workstreams A–K. The latest workstreams are listed in `RESULTS.md` (A–K). The earlier passes were:

- 58,292 passphrases against SalPhaseIon (DBBI/FAED transformations)
- 7,265 wrapper-recipe trials
- The prime/colour, Pascal, layout and checkerboard families
- `kdf_variants_probe.py`, which ran 10 KDF/cipher shapes, but **only on the "unconsumed orphan" candidates**
- `cosmic_convention_sweep.py`: uppercase hex, raw digest and MD5, but only on token combinations

Almost every trial used AES-256-CBC with EVP-SHA256 (sometimes MD5) and the password as lowercase sha256hex or raw text. That matches the verified convention. The limitation is that the inputs were our own guesses at DBBI/FAED outputs or at answers, never a verified intermediate result.

## 6. What has not been tried

Ranked by how much the evidence supports each gap. Cost means offline compute.

| # | Angle | Why it could matter | Evidence against | Cost |
|---|---|---|---|---|
| 1 | **The KDF/cipher variants on the main candidate sets.** PBKDF2 at 10,000 iterations (OpenSSL `-pbkdf2`), other `-iter` counts, and AES-ECB, which the harness cannot detect (it assumes CBC chaining) | No locked envelope has confirmed EVP-SHA256. "Raising the stakes" could literally mean a stronger KDF. The earlier variant probe covered only one small candidate set | Every opened stage used EVP-SHA256, and the locked envelopes add no new cipher statement | Low: rerun the roughly 2 million distinct materials already generated |
| 2 | **Password byte forms.** Uppercase hex; raw 32-byte digest; sha256hex applied twice; sha256hex(hash of first hint + answer), and the other orders the two SHA phrases allow | SalPhaseIon says "sha256" twice, once before and once after the envelope | The verified passwords are lowercase hex with no newline | Low: 4–6 times the existing sets |
| 3 | **Exhaustive search over whole answer classes on the GPU** (GTX 1070 Ti present) instead of hand lists. Examples: every string of one to three words drawn from the puzzle's own vocabulary; every English word or pair; every lowercase string up to 8 characters; every integer below 10^12 | This turns "our guesses failed" into "no answer of this shape exists". Only the key half of EVP is needed (IV-independent check), so each test is about 3 SHA-256 compressions and 1 AES block. That should run roughly 1,000 times faster than the Python harness (estimate) | The creator discouraged brute force (#9607). The Phase 3 and 3.2 answers were long compounds that this would not reach | Medium: a custom CUDA/OpenCL kernel or a John the Ripper openssl-enc format (check its SHA-256 support first). Hours per class |
| 4 | **Treat the envelopes as a system.** Put SalPhaseIon first, then Cosmic, and deprioritise the terminal envelope. Test candidate outputs as *inputs* to the next envelope, not just as passwords | Supported by the wrapper order, the 2023 recipe, #39237, #8569 and the terminal's own sentence | The order is not proven | None: it is a way of choosing what to test |
| 5 | **Sharper acceptance tests for a partial solution.** The twin envelopes should decrypt to 64 hex characters, a URL, a mnemonic or a sentence. Cosmic should decrypt to text or a nested `Salted__`/base64 envelope | This lets a near-miss be recognised: the correct key with the wrong IV still passes the last-block check. I re-checked all 111 recorded pad≥2 outputs: none is UTF-16 or has hidden structure | – | Done |
| 6 | **The obvious answer phrases, tried under the EVP-MD5 and PBKDF2 variants**, e.g. the Architect's last words in the film versus in the puzzle text, "this password", and the first hint | These were tried under EVP-SHA256, but only some were tried under the variants in row 1 | – | Negligible |

**Not worth doing:**
- A new salt-to-IV rule: the check is already IV-independent.
- Other ciphers or modes: CBC is effectively certain.
- Re-transcribing the ciphertext: it is verified.
- Probing live URLs: #63957 and #9607 argue against it.

## 7. Bottom line

The envelopes themselves have no weakness to exploit. They are AES-256-CBC with a single-pass KDF, correctly transcribed. From the envelope side, only three kinds of test remain:
- **Conventions:** rows 1, 2 and 6. These are cheap but low-probability.
- **Class elimination on the GPU:** row 3. This is new, and it produces firm negatives.
- **Ordering:** row 4.

Any real opening of SalPhaseIon needs the DBBI/FAED outputs that its wrapper names. No envelope-side attack substitutes for those, and Cosmic probably depends on SalPhaseIon's output.
