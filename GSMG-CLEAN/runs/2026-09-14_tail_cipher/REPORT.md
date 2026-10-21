# The tail as a cipher object, and the sibling corpus — 2026-09-14

**Result: the tail is not a monoalphabetic substitution of English (its 1.6/30 control-level "above" is a
hill-climbing artifact), nothing above control in 178 keyed/transposed forms, 0 exact-oracle hits. The
sibling corpus was reconciled against 01–14: the F-A-E/`yinyang` bookkeeping this folder lists as open is
already closed outside, and the outside files' open claims are almost all refuted states 05/06 already
show as void.** Move 5 (tail) and move 6 (reconciliation).

## 1. The tail — what the numbers say

The 64-letter `DBBI − VIC` tail has an index of coincidence of **0.0397** — indistinguishable from a
flat 26- or 24-letter stream (0.0385 / 0.0417) and far from English (0.065) [rechecked]. The 91-letter
diff is the same (0.0374). There is no transposition-only or homophone-free substitution signal to see.

- **Substitution attack.** A 60-restart × 400-iteration trigram hill-climber scores 8 against a
  shuffled-tail control maximum of 7 (1 in 30 runs reaches it: control level). The 91- and 71-character
  forms sit at or under control. The best "decrypt" is letter soup, and all three substitution plaintexts
  carry **0 exact-oracle hits**.
- **178 layered forms** — tail, diff and YOUWON-inclusive string under Vigenère/Beaufort with the balanced
  numbers and Architect/transcript windows at 0/479/484, rails 2–16 and columnar permutations at every exact
  divisor — top out at score 2 against a layered-control maximum of 2, with **0 oracle hits**. Planted
  Vigenère round-trip passed.
- **Left open:** non-English by design — transposition *composed* with substitution, the tail read as numbers
  (A1Z26 codes as a stream, bytes), or the tail as a *key*. None is English-shaped, so trigram controls can't
  judge them; the available exact oracles (L5, addresses) returned 0 in this run.

## 2. The sibling corpus — read, and reconciled

I read what 06 §7 left unread: `D:\downloads-8.8\puzle-main\` `SOLUTION.md` (988 lines),
`STATE_OF_PLAY.md`, and the `gsmgio-5btc-puzzle-master\` inventory — 100+ preregistered `solver\*` audits, plus
`docs\ATTEMPT_LOG.md` (108 KB), `findings.md`, `CREATOR_SOURCED.md`, `PIPELINE_RECONSTRUCTION_REPORT.md` and
`CLAUDE.md`.

| outside claim | outside evidence as stated | status here |
|---|---|---|
| F-A-E sonata (`S570 = fae + 9 × 63`, German note mapping) | "pre-registered … untested" (their wording) | still untested everywhere, including here (03 §19) — "untested" is correct, not a finding |
| `yinyang_*` series (selector, interleave-49, rot-180, composition, prime-dual, 479-continuation, seven-operand composition), `youwon_*` series | preregistered scripts exist | structural overlap with moves 1–4, but their primitives (extension-field XOR chains, Chain 4, second-door operands) are the retracted fluke chain of 05 — positives are 05-void, nulls duplicate 04 |
| `architect_479_*` / `salvation_*` / `split_envelope_*` / `intertwined_password_*` tests | `tests\` exists | same ATTEMPT_LOG discipline as here (sealed families, legibility gates); importing them adds no new family |
| `WITTEVEEN_IDENTITY_AUDIT.md`, purple-pill / Slack / NOTES threads | creator-reaction items | same class as this folder's 06 §5 non-hints; no password content in either folder |
| `SALPHASEION_PREREGISTRATION.md` v1–v36 (≈200k decrypts) | logged | already a bounded null in 06 §4 (v23/v35 checkers passed themselves), i.e. partially void |
| "479 balance", passport XOR, 140/23 Fresco | text claims | re-derived and *superseded* by controlled runs here (moves 0–1) |

Net effect: everything evidenced outside is represented here or refuted by 04/05/06 §1 §6. **03 §19 keeps one
entry, exactly as the outside file frames it: the F-A-E mapping is a pre-registered untested hypothesis owned
nowhere.** No string, digest, address or key in their attempt log, solver scopes or reports is an envelope
answer under this folder's exact oracles (all pad-gated or Chain-4-derived; 04/05 apply). Nothing was copied
in; `originals/`, `data/` and the outside workspaces were not modified.
in; `originals/`, `data/` and the outside workspaces were not modified.

## 3. The map after moves 0–5

| family | coverage | result |
|---|---|---|
| balance as literal answer | 476 × 1,464 | null |
| pointer as page-codec index | 3,675 chars exhaustive + 2,119 × 6,738 | null |
| prime values / masks | 744 + 142 outputs vs 40,615 controls | null, HILL demoted |
| prime material as keys | 93 vs 240 | null |
| 64-letter tail as English cipher object | profile + 3 solves vs 90 controls + 178 layered vs 60 | null, non-English uses named |
| sibling corpus | read + reconciled above | represented or refuted; F-A-E stays open |

## 4. Reproduce

```powershell
python tools\audit_tail_cipher.py
```

Writes `manifest.json` (profile, targets, solver and layered scope, controls) and `results.json` (profile,
substitution solves + controls, layered top/above/hits, oracle checks, planted test). No envelope byte is
read by the script.

**Limits.** Monoalphabetic substitution judged by trigram score (English assumption, stated); transposition and
keyed forms bounded to the listed shapes and key families; the sibling reconciliation is a scope-level audit
(their 108 KB attempt log and solver scopes were inventoried, not re-executed — re-execution would repeat 04's
voids).