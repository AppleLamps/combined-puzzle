# The "source code pointer" lead (4 October 2026)

**6 October 2026 interpretation notice.** This is a dated research record.
Its candidate counts and original logs are preserved, not freshly rerun.
Read [doc 118](../118-correctness-audit-remediation.md) for detector/coverage
limits and [doc 119](../119-current-evidence-ledger.md) for current findings.
A null applies only to its complete tested tuple.

R34 is a historical interpretation and 21-candidate test, not a creator binding of carried code to genesis part 6 or a completed instruction chain. The exact referent of 140 and the receiver/selection remain unknown.

Historical brief: investigate the failed-attempts log's proposed pointer (section 7: "last 60 ordinary digits give two lists summing to 1008 and 868 (difference 140); Architect index 1008 starts `TORETURNTOTHESOURCECODES`"). That arithmetic was not a verified creator instruction. Files here: `gen.py` (builds candidates from Satoshi's source by script), `cands.txt`, `run_rt.log`, `run_ct.log`.

## 1. The two lists: not reproducible, and chance-level as described

The log gives no definition of the "ordinary digits" or of the split, and nothing in the repo or the project files records one. I tried the readings the phrase allows:

- the 60-character dbbi residue (the characters at the 60 non-prime, "ordinary", walk positions; the parse re-run by script gives the dossier's residue exactly);
- the last 60 characters of faed, of dbbi and of dbbi+faed; the last 60 of the 149 checkerboard digits, with and without the straddle digits 1 and 4;
- each as values (a=1..i=9), stream indices (0- and 1-based) and walk positions, split into halves, alternates, steps 2 to 6, every contiguous cut, value parity, and read as 2- and 3-digit numbers.

None gives 1008 and 868. The totals are wrong to start with: the residue's values sum to 336 and its walk positions to 2,612, not 1,876.

What can be measured without the definition:

- **The 140 is not a second coincidence.** If two lists share a fixed total T and one sums to 1008, the difference is 2 x 1008 - T. With T = 1876 the 140 follows from the 1008. So the lead is one event, not two.
- **Two occurrences do not supply a binding.** The Architect text says “hundred fourty”; phase-3 part 6 independently has 140 characters. The exact numerical referent remains unknown. Arithmetic producing 140 does not by itself connect those objects.
- **Base rate of the 1008 hit.** The Architect text has 339 words (segmented by script). 61 of them start inside the instruction paragraph, from "the function of the you" (index 984) to "brute forcing might be required" (index 1287). So any number from 0 to 1538 lands on a word start in that paragraph with probability 61/1539 = **4.0%**. The log reports at least five split or width families tried around this lead. Finding one such hit among a couple of dozen split definitions is expected. That is the same verdict the dossier gives the 479 prime-sum pointer (chance level).

Verdict: as recorded, the pointer does not pass the shuffle-null bar. I treat it as chance. The sentence it points at still matters, because the creator wrote it into the text himself.

## 2. What the text from index 1008 says

From index 984, with the creator's changes to the film line in bold:

> the function of the **you** is now to return to the **source codes** allowing a temporary dissemination of the code you **hopefully** carry reinserting the prime **basics** after which you will be required to select from **over** twenty three **ciphers** sixteen **encryptions and/or** seven **intertwined passwords to find the actual private key note that also brute forcing might be required** failure to comply ...

The film reads: "to return to the Source, allowing a temporary dissemination of the code you carry, reinserting the prime program, after which you will be required to select from the Matrix 23 individuals, 16 female, 7 male, to rebuild Zion."

Read as steps, it gives five: go back to the source codes; temporarily take apart "the code you carry"; reinsert the prime basics; select from 23 ciphers / 16 encryptions / 7 passwords; and expect to brute force. Index 1008 is a film word ("to"). The creator's edit there is the plural **"source codes"**, which the film's "the Source" does not need.

## 3. Historical referent hypotheses for "the source codes"

There are three candidates in the chain.

| referent | evidence | status |
|---|---|---|
| The page source (HTML) of the SalPhaseIon page | the textarea is hidden page content | executed: textarea decoded (dossier 6), 1,670 archived HTML strings (10.5), R25 `thesource`/`thesourcecodes` null |
| The dbbi colour program | "prime basics" fits the prime walk | executed and solved (dossier 6.3) |
| **Satoshi's source code, `main.cpp`** | phase 3 part 6 was taken from it: "Its' raw data after 4 on row 1616" is the `scriptSig = 486604799 4 0x736B...` line of the genesis comment block. R34 hypothesized that “the code you hopefully carry” is that 140-character part; this is not independently bound by the creator or the Architect text | at the start of R34, its scoped file search found no previous candidate record for these neighboring values; R34/R35 subsequently tested listed forms |

The genesis interpretation was R34's preferred model, not a uniquely forced
referent. The plural “source codes,” the 140-character part, and a return to an
already-used source make a possible narrative; none independently binds the
Architect instruction to part 6. The original seven-part gate already consumes
that part. Its diagnostic formatting does not create a new extraction rule.

At the start of R34, The line number does not match. In v0.1.0 (`trottier/original-bitcoin`) the scriptSig comment is line 1442. In the tagged `bitcoin/bitcoin` releases checked (v0.1.5, v0.2.0, v0.2.10, v0.3.0, v0.3.24, v0.4.0, v0.5.0, v0.6.0) it falls between 1470 and 1902. None of those is 1616. The block and its values are the same in every version, so the candidates do not depend on which file the creator counted rows in.

## 4. Candidates and results (ledger row R34)

Every value is pulled from `main.cpp` by `gen.py`, never retyped. Each is tested as written, lowercased, and without `0x`.

| id | reading (one sentence) | answer |
|---|---|---|
| G1 | The only other code in the genesis block written in the same reversed-hex `0x` form as the code you carry. | `scriptPubKey` value (genesis public key, reversed) |
| G2 | The block's first source code, one line above the line part 6 came from. | genesis hash |
| G3 | The block's second code. | merkle root |
| G4 | "A temporary dissemination of the code you carry": part 6 decoded back to its text. | `The Times 03/Jan/2009 Chancellor on brink of second bailout for banks`, five forms |
| G5 | The whole raw scriptSig line, including what comes before "after 4". | `486604799 4 0x736B...` |
| G6 | The header constants of the same block. | nValue, nTime, nBits, nNonce |
| G7 | The block as one object. | all values joined in source order |

Results, 21 candidates:

- `rt.py` (canonical sha256-hex, EVP SHA-256 and MD5, all four password forms, 3 locked containers plus 3 solved as controls): 1,008 decrypts, 5 valid pads against about 4.0 expected, 0 flags, 0 win-test hits. Controls fired: key 1, and phases 2, 3 and 3.2 opened and were recognised.
- `ct.py` (14 ciphers x 5 KDFs x 4 forms): 17,640 decrypts, 78 valid pads against about 69 expected, 0 flags. Controls fired, including 11 planted containers, 7 of them made by the openssl CLI.
- Win test on the genesis hash and the merkle root as raw scalars, both byte orders: no hit.

**Null.**

## 5. What the lead resolves to

The 1008/868 selection lacks a reproducible definition; the reported base-rate
argument cannot authenticate it as a pointer. R34 tested 21 listed source-value
candidates and reported no validated result. This null is bounded by the full
tested tuples and historical detector limits.

The Architect sentence remains relevant, but its receiver and selection are
unknown. “Prime basics” may already describe the DBBI work; a separate unfinished
reinsertion step is not established. Neither 140 nor the category counts fix a
23/16/7 corpus. The old blocked enumeration is a historical proposal, not the
logical consequence of this paragraph or an active task.

**Update 4 October 2026:** row 1616 is matched after all. `bitcoin/bitcoin` tag v0.3.10 (not in the list checked above) has the scriptSig comment on row 1616 within the checked tag set. That is not proof of a uniquely selected historical source; the older walkthrough cites SourceForge r133. See `../genesis-main-cpp/README.md` (R35).
