# 11 — Skeptic brainstorm (post–Round 4)

**Inputs:** `06-skeptic.md`, `08-round2.md`–`10-round4.md`, `07-deletion-sweep.md`, handoff **§6.3** (readings / measured pins) and **§8.1** (October 2026 deflations). Offline only.

**STOP short list (3):**

1. **Bifid → `btcseed` → §4.1 / Beaufort key batteries** — prefix is **[V] but not forced** (8/362,880 squares; 5/6,561 continuations); Rounds 2–3 ran 8 squares × containers × Beaufort variants → **0** structured. Remainder of period-570 output is not a message.
2. **MASK6 / tail `szqu` / head `yM` as password or mask drivers** — §6.3 labels these **search findings, not checksums**; §8.1 notes tail arithmetic from outside AI; **2⁶ deletion** on those six positions → **null** (pins do not survive deletion). Further zero-mask permutations on the last 32 without a **pre-registered head+tail joint** are the same tiny space re-labeled.
3. **Scaled filler-letter deletion → whole-block integer → §4.1** — pair (1,770), triple (34,220), and quad (487,635) combinations already → **~1.68M** §4.1 decrypts **null** (`09`, `10`). Quintuple+ is millions more trials **without a new decode rule** or operand link to #8446 / phase 3.2.

---

## 1. Paths we should STOP spending cycles on

| Path | Why stop |
|------|----------|
| **Community EVP-MD5 recipe** (`matrixsumlistenterlastwords…`) and template permutations | §8.1: **79 B** with ~1/256 padding is **expected noise**; solvers **retracted**; Rounds 3–4 added sha256-as-EVP-password → still **0** prose. |
| **Recipe operands already in Round 2** (`tok23`, `msl-sum-bits` / spiral sums, `lw-arch-tail40`, `recipe-8446-order`, dots, another-door {1,4,21}) | **960** decrypts **null**; `lw-arch-tail40` overlaps prior billion-scale “last words” sweeps (handoff §8). |
| **Stream peel on faed** (`step2_peel.py`) as password material | Prior fact: stream vs whole-integer base-256 **disagree**; peel completion **empty**. Batteries using peel strings are undisciplined fishing. |
| **Whole-block zeroing only `g`/`e` for printable ASCII** | Handoff §6.3 **closes** that case; team already exhaustive on broader zeroings at **~16.8M** scale (§8). Re-opening without **deletion / reorder / non-decimal** hypothesis is duplicate. |
| **URL host-bit splice + insert-at-21 as “the” dbbi output** | **[V] descriptive fit**, one free splice index; dbbi shuffle nulls are the evidence, not the splice rule (§6.3). No container password has consumed “host bits” as a standalone operand. |
| **English sentences from `shabef…` glosses** (“our”, “the answer”) | Words **not on the page**; same failure mode as retracted concat passwords (§8.1). |
| **Prefix-only faed metrics** (even positions ⊆ `{b,c,d,e}`, five “pin” prefix lengths 455–561) | **Pattern / multi-hit**, not validated keys; never survived §4.1 when hashed. |
| **MD5-on-Sal-short-only while §4.1 std-hex on terminal/cosmic untested for the *same* new idea** | Fairness: if the hypothesis is “wrong KDF”, test **one** pre-registered string on **all three** containers in a **small** pilot—do not run another 3k MD5-only permutations on spiral bitstrings (Round 4 **null**). |
| **dbbi `b` as zero-digit at billion scale** | Handoff §8 already **null** with controls; no new reading since. |
| **Cosmic / yin-yang XOR variants without a new [R] from primary text** | Prior fixed-string rounds **null**; XOR is another degree of freedom on an empty signal. |

---

## 2. Paths that look like progress but aren’t

| Artifact | What it looks like | What it actually is |
|----------|-------------------|---------------------|
| **Tail `szqu`** | Unique lowercase 4-byte tail in last-32 after 1–4 zeroings (1/41,448) | **Tail-only search** with aesthetic filter; **not** a checksum (§6.3). Merging with head zeros `{1,3}` is a **second** search product, not one locked hypothesis. **Deletion kills the pin** (`07-deletion-sweep`). |
| **Bifid prefix `btcseed`** | Bitcoin-flavored plaintext at start of period-570 output | **Not forced** (§8.1); **8/362,880** squares; interior unreadable; §4.1 batteries **null**. README calibration helps; treating prefix as “half the key” is **marketing**. |
| **`yI u` at position 557** | Only single-position zeroing yielding printable last four bytes | Same **32-position** tail search; does not select among 570-letter strings. |
| **`c7bbc075` tail invariant** | Strong decimal-model constraint | **[V] arithmetic** on mod \(10^{32}\) with no `g`/`e` in suffix; does **not** imply faed encodes a key in those bytes alone. |
| **EVP-MD5 79-byte “open” on community string** | SalPhaseIon-short decrypt “works” | **Padding lottery** (~1/256); retracted; not text (`09-round3`). |
| **MASK6 interior printable rate** | Slightly better than chance on pinned bytes | **Post-hoc assembly** of head search + tail search (`06-skeptic`); **deletion null**; planted controls in `step3` **encode** these pins—they regression-test code, not puzzle intent. |
| **dbbi 1/490,314 yellow placement** | “Impossibly tight” fit to poster colours | Rule **written after the fit**; shuffle nulls matter, not the exhaustive count alone (§6.3). |
| **Five prefix lengths with lowercase top byte** | Multiple “pins” for block length | **Five** candidates (`m,c,r,h,w`)—undermines any single-length story. |
| **Handoff §9 “deletion not tried”** | Implies fresh win path | **Stale** vs repo: mask6 deletion + **>1.6M** filler deletion decrypts documented; only **non–whole-block** or **non–mask6** deletion might remain—not a blank cheque. |

---

## 3. Minimum evidence bar before the next large battery

1. **One pre-registered construction** in ledger format (`README`): hypothesis, exact code path, containers, convention, detector—**no** post-hoc MERGE of head pin + tail pin + Bifid square + recipe string.
2. **Operands cite on-page tokens or §6.2 decodes only**—no gloss words; `matrixsumlist` / `lastwords` must specify **operation + input** (e.g. which matrix, which “choice” anchor), not label concatenation.
3. **Planted §4.1 control** in the same run; **null** without control is not recorded.
4. **Detector stricter than printable ASCII** (~59% on real phase 3.2 plaintext per `README`); prize check = hash160 to `a9553269…` where applicable.
5. **Frozen [T] null for any new fit rule** before scale-up (e.g. faed tail pin → block-preserving shuffle; dbbi walk → 200k shuffle with rule fixed **before** looking at data).
6. **Pilot first:** order-of **10²–10³** decrypts demonstrating the construction is **not** a rename of handoff §8 or Rounds 2–4 operands; only then six-figure+ sweeps.
7. **Explicit statement** of what changed vs prior team **34B** decrypt scale (handoff §8)—new cipher, new blob, or new materially different password grammar.

---

## 4. Prize key: inside containers vs derived without decrypting?

Solved phases use **§4.1** (password → EVP → AES-CBC) and creator #4624 points at a **private key**; the three locked blobs are the obvious gate. Prior work at **~34B** decrypts and **195M** scalars under the usual convention found **no** hit (handoff §8), and this repo’s focused batteries (mask6, Bifid, recipe, filler deletion through quad, MD5 variants) add **null** on top—not proof the prize is outside the blobs, but proof that **current operand guesses do not open them**. A **derived-without-decrypt** story (faed whole-block integer, Bifid output bytes, or tail `szqu` as raw secp256k1 material) is **not** supported by [V] chain evidence: integer decode is mostly non-text, tail pins are **search ornaments**, and no scalar check is reported for those byte patterns at team scale. The conservative skeptic read: the **likely** end state is still **password/KDF → decrypt a locked container → key material**, with failure mode **wrong reading or wrong convention**, not “key sitting in plaintext in faed.” Direct derivation remains **possible** but **indistinguishable from fishing** until one **pre-registered** map from §6.2/primary text to a scalar or WIF is stated and survives a **small** control-backed battery.

---

## Bottom line

Trust **§4.1 solved chain** and **§6.2 exact decodes**; treat **§6.3 pins and Bifid prefix** as **hypotheses**. After Rounds 2–4, the default action is **not** another wide §4.1 grid—it is **Reader/Cryptanalyst** locking **one** recipe (MSL + lastwords + container target) with **statistician nulls**, or **documented** departure from §4.1 (new blob, KDF, or encoding) with a pilot. Until then, enforce the **three STOP items** at the top.
