# puzzlehunt#104 Correction (retracting my premise) + narrowed request: creator guidance on the SalPhaseIon / Cosmic Duality stage (c4chiras 2026-08-20, open)

**Correction first.** When I opened this issue I treated the "Cosmic Duality decrypt" — the
1327-byte plaintext with `sha256 = 4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081`
— as established, and built my requests on top of it. **That was wrong and I'm retracting it.**
@Naddiseo pointed me to #55; the objections raised there are correct:

- PKCS#7 padding has a ~1/256 false-positive rate, so a clean `openssl` exit is not evidence that
  the key is right.
- The output is high-entropy with no header, no strings and no recognisable format, whereas every
  earlier stage of this puzzle decrypts to readable text.
- The supporting "the SHA-256 matches the known target" argument is self-referential — the target
  *is* the hash of that same output.

Two further checks of my own, in case they save anyone else time:

1. **`gsmg.io/4f7a1e4e…` is not independent corroboration.** Its earliest Wayback capture is
   **2026-06-02** (an error response), followed by **2026-07-08** as a ~1.2 KB placeholder — long
   after the claim was published. The Wayback CDX records any URL that someone *requests*, so that
   entry is a consequence of somebody computing the hash and visiting it. The URL never served
   content.
2. **The other "removed" pages I asked about were never archived with content either.**
   `TheArchitectChoice` first appears **2025-08-24** and, fetched and decompressed, is just the empty
   Vue app shell (`<div id="app"></div>`, no textareas, no stage text). `final_stage` is the same
   shell. `salphaseion`, `youmeandself` and `youmeiandself` have **no captures at all**. Since a CDX
   entry only proves a request was made, several links in the commonly-cited "answer chain" look
   like solver probes rather than pages that existed and were later removed.

So asks #1 and #2 in my original post were requests for material that, as far as I can tell, does
not exist — apologies to anyone who spent time on them. I'd extend the same caution to the QR
"dot/dash" payload discussed in #24/#67: independent checking indicates the QR decodes normally to
the printed address page, with the grey pixels confined to the three finder patterns rather than the
data modules.

---

**What I'm actually looking for now** (much narrower):

The SalPhaseIon page itself is intact and its contents decode cleanly along the lines already
documented in the community write-ups — the two binary runs give `matrixsumlist` and `enter`, the
`z`-delimited segments give `lastwordsbeforearchichoice` and `thispassword`, `shabef` reads as
`sha256`, and there is the plain-text sentence *"our first hint is your last command"*. What I
cannot establish is **how the creator intended those tokens to be used** to form the passphrase for
the two blobs on that page.

1. Does anyone have a **primary record from roughly 2019–2021** — a Telegram or Discord export, a
   dated screenshot, an email — in which the creator says anything about the **SalPhaseIon / Cosmic
   Duality stage specifically**? Whether the tokens combine in a stated order, whether a further
   secret outside the page is required, or what form the output was meant to take.
2. For the creator-attributed hints usually quoted as "prime", "zeroed out", "Yin Yang" and
   "ASCII-127" (see #97): can anyone provide **original provenance** — the source message with a
   date, rather than a later screenshot of a screenshot? Knowing which of these genuinely came from
   the creator, and when, would change how much weight they deserve.
3. Is there any documented stage **between phase 3.2 and SalPhaseIon** other than the
   "hash the text of `gsmg.io/puzzle`" hop? I want to be sure I'm not missing an intermediate step.

Happy to keep this issue updated as things get ruled in or out — I'd rather leave an accurate record
than a tidy one.


---
## Naddiseo 2026-08-20
You should read my replies on https://github.com/puzzlehunt/gsmgio-5btc-puzzle/issues/55 which is the origin of this "1327-byte plaintext" nonsense.

Regarding 1: "gsmg.io/4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081 " was never a url related to the puzzle. and there is no credible evidence of a "step after Cosmic Duality". In fact, the creator of the puzzle stated once we got to salph that the internet is no longer required.

---
## Anvexis 2026-08-23
Hi JRK,

I've independently reproduced the public chain through Cosmic Duality and would appreciate your guidance on the final step.

**What I've verified:**
- Phase 1→3.2: Full chain from 14×14 spiral to VIC cipher
- SalPhaseIon: Master key via XOR of SHA256 tokens = `a795de117e472590e572dc193130c763e3fb555ee5db9d34494e156152e50735`
- Cosmic Duality: Decrypted 1327 bytes (EVP-MD5 with raw master key)
  - SHA256: `4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081`
- Half / Better Half: Derived via 103×103 matrix → base-38 decode → 68 bytes
  - Half: `0423d9115a1dc756d5d08d2de880ab508bd4745fc97709f4fcb513f2cb8fcc35`
  - Better Half: `48cc46e66bdd36b09ae344552f606a761f9d90681f20dfefe2b43db18b623971`
  - Trail: `fc0c1b02`
- Verified through 6 Wayback Machine snapshots (2023–2026)

**Blocked on:**
The 79-byte SMALL AES blob (salt `3ab585348552415d`) remains unopened after testing 200+ password candidates (all KDF variants: MD5/SHA256/SHA1/PBKDF2, AES-128/192/256, block0 as password, primes, yellow/blue positions, etc.).

The community (Issues #88, #92, #103, #106) is stuck on the same point:
- `cosmic_A.bin` (SHA256 prefix `cd3fea3d…`) has never been publicly distributed
- The exact row1–row4 definition for the XOR triangle remains unknown
- The oracle hash `e2590f15…2cbd` for the SHORT plaintext has never been reproduced

**My question:**
Is the final step solvable with publicly available data, or does it require non-public operands (cosmic_A.bin, specific XOR triangle formula, or other private material)?

If it's solvable, can you provide guidance on the missing piece? If not, I understand this puzzle has fulfilled its purpose as a cryptographic challenge.

Thank you for creating this incredible journey over the past 7 years. It's been a privilege to work through it.

Best regards

---
## Naddiseo 2026-08-23
@Anvexis Jrk doesn't read this repository

Additionally, pelase read my replies on https://github.com/puzzlehunt/gsmgio-5btc-puzzle/issues/55
