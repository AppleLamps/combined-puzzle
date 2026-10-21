# The common flaw (4 October 2026)

**6 October 2026 interpretation notice.** This is a dated research record.
Its candidate counts and original logs are preserved, not freshly rerun.
Read [doc 118](../118-correctness-audit-remediation.md) for detector/coverage
limits and [doc 119](../119-current-evidence-ledger.md) for current findings.
A null applies only to its complete tested tuple.

The mixed-source pairing remains a hypothesis. Source wording does not force all earlier answers, prove FAED filler, or put the operands outside the page. The corrected 600-string set remains unsearched.

Sources read for this: project memory (frontier, standing rules, critical review, constraints, rabbit holes, microstep, source pointer, photo analysis), `../FAILED-ATTEMPTS-LOG.md` and its index, the dossier (sections 3, 6, 9, 10), `../critical-review-2026-10-03.md`, `../constraints/README.md`, `../riddle-method/README.md`, `../independent-model/README.md`, `../microstep/README.md`, and the captured pages. Statements marked INFERRED are readings, not measurements.

## The flaw in two sentences

Everyone treats a failed joint password as a verdict on each label's reading separately, but under the joint-concatenation hypothesis a null only applies to the **pair** and complete configuration tested. The clue says `thispassword`; it does not establish joint concatenation or a definite mapping to a lock. Separate passwords, intermediate operations and alternative lock mappings remain competing interpretations. Each camp then paired its readings only with its own camp's readings of the other label, so the pairs that cross camps were never formed, while the readings inside them were already struck off as "spent".

## The connections

1. **The record states the rule and then breaks it.** The frontier note says "two unknown operations feed one password, so neither validates alone". The constraints table then kills slot M and slot L one class at a time ("No M referent survives on its own"; slot L "killed by E (R2)"), and memory says "don't re-run the film line in either wording". Each of those verdicts rests on joint tests with a handful of partners.

2. **The data camp filled both slots from puzzle data.** Doc 114's 8.1M joint passwords are 2,500 poster sum lists x 1,620 windows of the creator's *Architect text*. Doc 115's 1.24B are 1,547 poster lists x `lw_core`/`lw_loc`/`lw_words`, all cut from the same Architect text. No film line is in any of those L pools.

3. **The riddle camp filled both slots from outside knowledge.** Rounds R1 to R35 cross film lines (R2, R3, R7, S1) with riddle M answers (`twentythreesixteenseven`, `231607`, `neo`, `yourlife`, `trace`, `101`). After the critical review, poster sum lists were excluded by rule, so they never met a film line. S1, the one reading that survived the constraint table, was crossed only with ledger M answers.

4. **The creator's own multi-part password mixed the classes.** Phase 3 joins trivia answers (Safenet, Luna, HSM, 11110) with a string copied verbatim from source code (part 6 is the text after `4` on row 1616 of main.cpp, exactly as printed there) and a computed chess position (part 7). One password, three kinds of source.

5. **The page itself points one label inside and one outside.** dbbi, the check of the poster's colour program, sits directly before `matrixsumlist` (and #6509 says the prime part comes first), which points M at the poster matrix. The creator deleted the whole door scene from his Architect text, so the last words before the Architect's choice cannot be read from any puzzle text and must come from the film. The most literal pair is therefore poster-derived M with film-derived L (INFERRED), which is exactly the pair neither camp formed.

6. **Why phase 3 did not suffer from this.** All seven parts were forced to one answer each (one non-mating move, one cp273, six for six format tags), so a single end check was enough. The SalPhaseIon labels are not forced, and the record has used the end check as if they were.

7. **The creator gave partial checks before.** His first hint (#225) was a hash to "hit your options against", and dbbi checks the poster's colour program. The record uses dbbi as a dead object rather than as the verified input to the next step (INFERRED).

## What it invalidates, and what it leaves alone

| item | status under this flaw |
|---|---|
| Every historical decrypt null | scoped to the strings, cipher/KDF and detector tested; detector suppression limits exclusion |
| Single-label-alone nulls (each answer tried alone on every lock) | stand; they test the one-label-per-lock models |
| Convention, container sizes, cipher class | convention proven only for solved gates; lengths and randomness do not prove the locked cipher class |
| faed statistics, dbbi parse, photo | outside this assembly correction |
| Doc 114 / doc 115 crosses (poster lists x Architect-text windows) | historical tested pools only; reconstructed membership in vanished originals is unknown |
| "Spent" verdicts on individual readings: R2, R3, R7, S1 and the other film L lines; R1, R8, R11 to R14, R19; the 1,558 poster lists as M | **invalid as stated**: each is only dead with the partners it was tested against |
| The constraint table's kill matrix, slot by slot | **invalid**; it has to be redone as pairs |
| "The operands lie outside the page" (dossier 9) | not shown by the nulls; it rests on faed being filler, which this does not touch |

Untested blocks this reopens: (a) poster-derived M x film L, (b) riddle M x Architect-text L windows. Partial overlaps exist: the 82,710 three-slot cross of session 22 Sep (58 M outputs x 25 last-words, always with a `yellowblueprimes` slot first) and GSMG-CLEAN's off-repo `matrixsum_lastwords` (34,860) and `pipeline_enum`, whose candidate lists are not on record.

## Test of block (a)

One reading per slot, a sentence each:

- M: the poster's own matrix (the 14x14 bit grid in `matrix.json`), summed by row and by column, with the off-white cell as printed (0) and as dbbi counts it (blue, 1). Written as digits, commas, comma-space, spaces, and in the two forms a program prints a list (`[6, 10, ...]` and `[6,10,...]`), which no pool in the record used.
- L: the Architect's last line before Neo's choice in the creator's transcript wording (S1), its cut forms, the shorter R2 wording, `wewont`, `theproblemis`.

Historical run: 24 M strings alone and 432 pair assemblies, 456 unique candidates. The generator omitted all 144 `L+M+thispassword` strings. The corrected `gen.py` and `cross.txt` contain 600 unique strings and assert exact set membership for M alone and all four pair assemblies. The additional strings have **not been searched**; old logs below remain unchanged.

| tester | decrypts | valid pads | flags | controls |
|---|---:|---:|---:|---|
| `rt.py` (convention, 4 forms, EVP SHA-256 and MD5, 6 containers) | 21,888 | 87 (~85.8 expected) | 0 | key 1; phase 2, 3, 3.2 open and are recognised |
| `ms.py` (`\n`, `\r\n`, ` \r\n`) | 49,248 | 223 (~193) | 0 | three planted openssl newline containers opened |
| `ct.py` (14 ciphers x 5 KDFs) | 383,040 | 1,463 (~1,502) | 0 | 11 planted containers recovered |

Win test on every candidate: 0 hits. **The historical 456-string subset produced no heuristic flags; the advertised full block was not tested, and unranked padding-1/2 binary results were not preserved. This is not an exclusion of block (a).** Logs: `run_rt.log`, `run_ms.log`, `run_ct.log`.

## What this changes going forward

- A reading is never "spent" on a joint null. Keep a pair ledger, not a per-label kill list.
- A new reading should explain **both** labels with one idea (the way one song explained the URL, the rebus and the phase-1 password), so the pair is tested as a unit instead of crossing two independent guesses.
- Block (b) is the remaining untested block. It is a pool cross (about 10 riddle M answers x the 175 `lw_core` windows, both orders, about 3,500 candidates), so it was not run here under the no-sweep rule.
