# 06 — Skeptic: audit of team ledgers and repo reasoning

**Role:** Challenge fit-as-proof, post-hoc rules, prefix-only wins, readings that
import words not on the page, and whether hard limits hold in code. Prior facts
carried forward: **six-position deletion on faed → null** (pins lost, no
container/key hit); **stream peel on faed → invalid** (stream vs whole-integer
base-256 disagree; no printable completion under a single rule); **phase 3.2 EBCDIC
region is not cp273 a–z** (~771/1539 cp273 codepoints are letters; Beaufort uses
a derived 26-symbol substitution, not “decode cp273 then read English”).

**Handoff §8.1 (October 2026 checks):** External claims were checked against
files, not blessed as puzzle intent. This audit treats §6.3 **pin / search**
items the same way: arithmetic reproduction ≠ design proof.

---

## Pass / fail by ledger entry type

| Ledger | Scope | Verdict | Rationale |
|--------|--------|---------|-----------|
| `01-archivist.md` | [V] byte reproduction | **PASS (conditional)** | `archivist_check2.py` scope matches second-build handoff for tagged [V] fields; 106/106 scripted checks are internally consistent with `uploads/GSMG-handoff.md`. QR payload and §1 on-chain rows correctly excluded. |
| `01-archivist.md` | Epistemic boundary | **FAIL** | Report title “NO FAILURES” conflates *faithful transcription of the handoff* with *sound inference*. §6.3 search rows (tail `szqu`, prefix-length list, URL bit splice, Bifid `btcseed`) are reproduced as [V] because the handoff tags them [V], not because skeptic accepts them as checksums. No re-run of [T] shuffle nulls (dbbi 200k×2, faed prefix calibration). |
| `02-reader.md` | Solved-chain literalness, [R] with citations | **FAIL (missing)** | File not present. Cannot audit whether readings cite only on-page tokens or smuggle glosses (“answer”, “our”, recipe operands). |
| `03-cryptanalyst.md` | Decodes as code, then run | **FAIL (missing)** | No ledger; inference only from `src/step1_btcseed.py`, `step2_peel.py`, `step3_mask.py`. Peel stream explicitly disclaimed in README; **MASK6** `{1,3,551,557,561,563}` stitches **separate** head and tail searches—methodology not recorded in a cryptanalyst ledger. |
| `04-statistician.md` | Null for every fit | **FAIL (missing)** | Archivist defers all [T] stats. Without statistician ledger: dbbi exhaustive yellow-host parse (1/490,314) has **no** independent pre-registration; faed `szqu` uniqueness has **no** block-preserving null in repo. |
| `05-tester.md` | Battery format (hypothesis, construction, controls, detector) | **FAIL (missing)** | `step3_mask.py` runs decrypt batteries but no `05-tester.md` entry per `ledger/README.md`. Planted controls in step3 **encode** search outputs (`szqu`, `yM`)—valid regression anchors, **not** evidence the mask is the puzzle’s mask. |
| `00-lead.md` | Synthesis and decisions | **PASS (partial)** | Correct: do not treat tail pin `szqu` as proof without head-side pin + null; stream peel invalid; deletion null recorded in prior session table. **FAIL (partial):** handoff §9 still says “Deletion has not been tried” while lead/repo artifact `mask6_deleted.bin` and git history record a deletion experiment—source documents are out of sync. |

**Hard limits (repo scripts):** **PASS.** Grep finds no `requests`/`urllib` submission to `gsmg.io/phase1verification` or live endpoints. Scripts and `archivist_check2.py` header state offline-only. Handoff HTML form URL appears only in quoted page source, not in client code.

**Repo narrative (`README.md` “Result”):** **FAIL (epistemic).** Headline “begins `btcseed`” without §8.1 calibration (“not forced”; 8/362,880 orderings; 5/6,561 continuations) is prefix marketing, not skeptic-grade conclusion.

---

## Audit axes

### 1. Post-hoc rules

| Locus | Observation | Skeptic verdict |
|-------|-------------|-----------------|
| dbbi prime walk | Handoff §6.3: “The acceptance rule was written after the fit was seen, so the shuffle nulls are the evidence, not the rule.” | **Confirmed post-hoc.** Archivist correctly measures the fit; statistician ledger needed to show shuffle nulls were run **with frozen rule**, not retrofitted. |
| URL LSB + insert `1` at position 21 | Fits exactly with one free splice parameter. | **Descriptive [V], not semantic proof.** Same information as “off-white counts as blue” bit encoding—stated as reading in handoff. |
| Filler `b` split 19\|16\|23 | “Triple noticed after the fact” (handoff). | **Exploratory.** 6/1770 placements is a weak tail unless pre-specified. |
| `step3_mask.py` MASK6 | Positions 551–563 from last-32 search; 1,3 from head `yM` / `?j` pin; merged into one “six-position zero mask”. | **Post-hoc assembly.** Reproducible; not a single hypothesis stated before search. |
| Bifid square `dbifhcega` + `k..z` | First-appearance order from dbbi under the walk reading. | **Reading-dependent stack.** Square choice is not independent of the dbbi parse. |

### 2. Prefix-only decodes

| Claim | What is actually shown | Skeptic verdict |
|-------|------------------------|-----------------|
| Bifid → `btcseed` | Period 570 full output starts `btcseedd`; calibration shows many squares/continuations also yield prefix. | **Prefix hit only**; §8.1: not forced. README overstates. |
| Even positions ⊆ `{b,c,d,e}` | Structural on output; not tested as password/key. | **Pattern, not message.** |
| Whole-block integer | Head `1bd5951d`, 78/237 printable—mostly non-text interior. | **Not a plaintext decode.** |
| Tail pins `yI u`, `szqu` | Last four bytes only, after zeroing searched positions. | **Suffix ornament** unless head constraint + independent null (lead agrees). |
| Prefix lengths 450–570 lowercase top byte | **Five** lengths `{455,467,508,520,561}`, not one. | **Multiple hits**—undermines “pin” narrative for any single length. |

### 3. Readings missing words from material

| Reading (handoff [R]) | On-page tokens | Gap |
|------------------------|----------------|-----|
| `shabef…` → “sha256 **our** first hint…” | `shabef**four**firsthint…` | “our” is a gloss on **four** (homophone), not a separate word. |
| `shabefanstoo` → “sha256 **the answer** too” | `…anstoo` | **the**, **answer** absent; expansion via `ans` → answer (#225 context). |
| `matrixsumlist` / `lastwordsbeforearchichoice` as recipe | Operands named in #8446 / SalPhaseIon | **Inputs and operations** for “matrix sum list” and “last words” are not on the page—open §9. |
| dbbi ↔ `yellowblueprimes` | #8446 string (verified [V] reverse binary) | Name is in creator export, not SalPhaseIon body—OK as cross-reference, not as self-contained block label. |
| Phase 3.2 “cp273 → speech” | 26 byte symbols | **Not** literal cp273 alphabet text (controls, C1 bytes, digits—see `artifacts/cp273_symbols.txt`). Beaufort consistency check is the real [V] claim; archivist #42 wording “cp273 glyphs” is easy to misread as “all letters”. |

### 4. §6.3 pin findings — hypothesis, not proof

Handoff labels these **[V] search findings, not checksums**. Skeptic agrees on arithmetic, rejects proof status:

| Finding | Reproduced? | Why hypothesis only |
|---------|-------------|---------------------|
| Tail invariant `c7bbc075` under any single-`g`/`e` zeroing in last 32 | Yes (mod \(10^{32}\), no `g`/`e` in suffix) | **Strong constraint** on the *decimal model*; does not select faed content among all 570-letter strings. |
| Only 557 → printable last 4 (`yI u`) | Yes | Search over **32 positions**, one degree of freedom; no faed-block null. |
| Unique lowercase 4-byte tail in last-32, 1–4 zeroings → `szqu` | Yes (1 hit in 41,448) | Space is **tiny** and **tail-only**; lowercase filter is post-hoc aesthetic; origin “outside AI” (§8.1). Combining with head zeros `{1,3}` is a **second** search product, not one locked hypothesis. |
| Prefix top-byte lowercase at 5 lengths | Yes | **Not unique**—five candidates (`m,c,r,h,w`). |
| Bifid `btcseed` + sha256 of output | Yes | **Calibration negates “forced”**; remainder of 570 chars unreadable. |
| dbbi host bits = URL LSBs + splice | Yes | **One** free splice index; exhaustive 490,314 yellow placements still assumes host alphabet `b`/`be`. |

**Deletion (prior session):** Lead records deletion null; handoff §9 and §8 hidden-zero bullet still say deletion untried—**do not** treat handoff §9 as complete on faed letter removal until the document is aligned with repo experiments.

**Stream peel:** Prior fact stands—`step2_peel.py` documents incompatible stream vs base-256 readings; `peel_stream_faed.txt` empty (no completion). Using peel strings in password battery without a valid rule is **fishing**.

---

## Archivist spot-check (skeptic, not duplicate run)

- **PASS:** Cryptographic and container [V] chain (§§1, 4–5, 6.1–6.2, 7.1) is the right standard of evidence.
- **PASS:** Explicit non-reproduction of QR and chain data.
- **FAIL:** Treating §6.3 URL/bit/Bifid/search rows as of equal “win path” weight to §6.2 decodes in the bottom-line prose.
- **FAIL:** No challenge to handoff internal contradiction (§9 deletion vs team deletion run).

---

## Top 3 vulnerabilities in team reasoning

1. **[V] laundering of search artifacts.** Tail `szqu`, head `yM`, and Bifid `btcseed` are reproducible measurements but handoff and `README.md` read like progress toward a key. §8.1 explicitly deflates external “forced” claims; the repo README does not. Risk: **MASK6 and btcseed drive the next battery** without a registered null or a single pre-declared construction.

2. **Stacked post-hoc readings presented as one mechanism.** dbbi walk → host bits → URL splice → Bifid square from dbbi first letters → faed decimal tail pins is a **chain of optional [R] layers**. Each layer was fit or calibrated after the previous. Risk: **confirmation cascade**—failure modes are hidden in splice index, “four/our”, and square orderings (8/362,880).

3. **Gloss words smuggled into “literal” recipe strings.** `shabefanstoo` and `shabefour…` decode to **concatenated tokens on the page**, not to the English sentences in §6.3 prose. `#8446` gives a **word list**, not operands for `matrixsumlist`. Risk: **passwords built from solver English** rather than from stated transforms—repeats the retracted EVP-MD5 concat pattern §8.1 warns about (padding ≠ plaintext).

---

## Bottom line

| Entry type | Pass? |
|------------|-------|
| Archivist [V] reproduction | **Conditional pass** |
| Archivist epistemic gatekeeping | **Fail** |
| Reader / Cryptanalyst / Statistician / Tester ledgers | **Fail (absent)** |
| Lead synthesis | **Partial pass** |
| Hard limits in `src/` | **Pass** |

**Skeptic RESULT:** Trust the **solved-phase [V] chain** and **6.2 exact decodes**; treat **§6.3 pins and Bifid prefix** as **hypotheses** until head+tail joints are pre-registered, deletion/stream/peel paths are ledgered with controls, and [T] nulls are attached to each fit rule—not only to the handoff prose.

---

## Addendum (post-merge, 17 Oct 2026)

Ledgers **02–05** and **04-statistician** are now on `main`. Revised verdicts:

| Ledger | Verdict |
|--------|---------|
| `02-reader.md` | **PASS (format)** — citations and [R]/[V] split; still no decrypts (by design). |
| `03-cryptanalyst.md` | **PASS** — code + 108-decrypt battery with planted phase2 control. |
| `04-statistician.md` | **PASS (partial)** — exact counts reproduced; dbbi shuffle null still not re-simulated in-repo. |
| `05-tester.md` | **PASS** — 34k decrypts, pads at chance, planted control fired. |
| `07-deletion-sweep.md` | **PASS** — 2⁶ MASK6 deletion → **null**; documents repo vs handoff §9 gap for *mask6-only* deletion. |

**README** updated to state Bifid prefix calibration (8/362,880). Handoff upload §9 wording unchanged in-repo (untracked `uploads/GSMG-handoff.md`).
