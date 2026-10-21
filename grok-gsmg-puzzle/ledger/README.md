# Team ledger — GSMG.io 5 BTC puzzle

Source: `uploads/GSMG-handoff.md` (second build, 17 Oct 2026,
sha256 `442d502f2bb65b44f1ba67ede9b9415da6a6395b98966e69d931853c10f6d7f6`),
poster `data/puzzle.png` sha256 `38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830`.

Win test: candidate correct iff sha256→ripemd160 of its public key equals
`a9553269572a317e39f0f518cb87c1a0ee1dbae4`. Only the uncompressed
serialization of the prize point can match (compressed gives `06bbdc66…`);
test both anyway. Control: private key 1.

Hard limits: (1) never submit to `gsmg.io/phase1verification` or any form;
(2) never contact/identify/locate the creator or anyone. Work offline only.

## Ledger entry format (Tester/Cryptanalyst batteries)

hypothesis | exact candidate construction (code) | containers tried |
convention | candidates | decrypts | valid pads vs expected (~decrypts/256) |
planted control result | detector | result

A null without its control is not recorded as a null. Printable-ASCII alone
is not a detector (phase 3.2 plaintext is only ~59% printable).

Walkthrough in puzzle order: `puzzle-order.md` (repo root). This folder is the research log.

## Files

- `01-archivist.md` — [V] reproduction
- `02-reader.md` — solved-chain literalness, candidate readings with citations
- `03-cryptanalyst.md` — decodes proposed as code, then run
- `04-statistician.md` — null for every fit (`python3 team/statistician_repro.py`)
- `05-tester.md` — batteries in the format above
- `06-skeptic.md` — audit of the above
- `07-deletion-sweep.md` — MASK6 deletion 2⁶ sweep
- `08-round2.md` — Bifid×8, Beaufort, recipe, dots, another-door, filler deletion
- `09-round3.md` — EVP-MD5 Sal-short, word lastwords, spiral MSL, filler pair deletion
- `10-round4.md` — MD5+sha256 EVP, spiral bitstring ops, triple/quad filler deletion
- `round5/` — Round 5 team brainstorm (`brainstorm.md`) and role ledgers (`reader.md`, `cryptanalyst.md`, `skeptic.md`, `strategist.md`, `tester.md`)
- `12-round5.md` — Round 5 pilot (post-brainstorm)
- `13-round6.md` — Reader top 5 (after SELECT, 149 digits, #6509, yinyang, XOR enter)
- `14-round7.md` — Chained pipelines (H1, M3, 6 orders, hash-chain, yinyang mid, XOR enter)
- `15-team-audit.md` — Composer team review: missed readings, bugs, overstated falsifications
- `16-round8.md` — Reader gap G1–G7 (~2k pilot: title, #6913 bits, Sal full, shabef, H2/H3)
- `17-round9.md` — Reader G8–G15 + classify_unified + H1 Cosmic raw32 audit
- `18-round10.md` — Methodology cleanup + G12 phase-3 seven-part falsification
- `19-round11.md` — Sal enter-split + Terminal-first chain + joint #8000
- `20-round12.md` — z-stage program + pre-decode b64 + liberal Terminal-first
- `21-round13.md` — Byte XOR enter + poster matrixsumlist + full Sal stage-0
- `22-round14.md` — Missed connections clue battery (G1–G8)
- `23-detector-audit.md` - Re-run of every battery under a recogniser that sees phase 3.2; `{` false positive fixed; stale JSON regenerated
- `00-lead.md` — lead decisions and round synthesis
- `experiments.md` — handoff prose vs what this repo actually ran
