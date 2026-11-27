# Architect typo stream (2026-11-27)

Hypothesis only. The poster colour map does not confirm it.

## Source
data/architect_letters_1539.txt (1,539 letters).

## Typo stream (spelling only, film edits excluded, zero-based)
| Word | Error | Index | Prime? |
|---|---|---|---|
| FOURTY | extra U | 571 | yes, 105th |
| WAISTING | extra I | 678 | no |
| PRICES | C for Z | 720 | no (swap, kept) |
| THROPHIES | extra H | 727 | yes, 129th |
| YOURSELF SELF | second SELF | 1483-1486 | 1483 yes, 235th |

Inserted letters: U I H SELF (7). Prompted by creator #81813 ("Im not dislexjsic at all"), sent 7 minutes before #81819 ("tiny nudge"). Against: #1806 and #5960 call these typos.

## architect_clean_1532.txt
The 7 inserted letters are removed and PRICES is left as written. Offsets below 571 are unchanged. SOURCECODES moves from 1021 to 1018 and CIAOBELLAO from 1529 to 1522.

## Colour-map check
There is no direct map, because the poster has 24 coloured cells (primes 2 to 89). Wrapping ordinals 105/129/235 mod 24 (1-based) lands on cells 9, 9 and 19, all yellow (primes 23, 23, 67). 0-based gives Y, Y, B. Note that 129 - 105 = 24. About a 14% chance, and the indexing choice is ours. Too weak to sweep.
