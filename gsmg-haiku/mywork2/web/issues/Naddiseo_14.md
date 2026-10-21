# Naddiseo#14 Possible square matrix in the DBBI and FAED blocks (saama143 2026-09-07, open)

I have noticed similar pattern in both unresolved a..i blocks.
using `a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9` mapping and decomposing each value where value is greater than 3 

`a → a
b → b
c → c
d → bb
e → bc
f → cc
g → bbc
h → bcc
i → ccc`

the two blocks expand as follows:

DBBI block: Original length: 91, Expanded length: 169 = 13X13
FAED block: Original length: 570, Expanded legth: 1225 = 35X35

I did tried to decode both of this in multiple ways but none produced readable text. It would be useful to know if anyone has tested this representation before?


---
## dz17ghost-create 2026-10-05
The 13x13 and 35x35 shapes are striking (13^2 and 35^2 exactly, and 35 matches the block count in the unverified chain-4 material), so I ran a sweep over readings of both matrices in case the expansion is a transposition stage:

- row order, column order, serpentine (boustrophedon), spiral (the phase-0 reading), and their reversals
- interpretations: a/b/c as trits -> bigint base-3 -> bytes; trit groups of 3 -> 27-symbol alphabet; direct A1Z26 on the expanded letters

All of them come out as noise (printable ratio 0.24-0.44 on the byte interpretations, no English structure anywhere). So if the 2s-and-3s decomposition is the intended first stage, the second stage is not any of these reads.

One extra observation from trying to work the frequencies: the expansion weights the output alphabet toward b and c (g = 7 = `bbc` alone contributes 321 b/c symbols in FAED), and the expanded strings have no structure beyond that. If the intended reading were a simple transposition of the expanded string, the b/c/a distribution would have to survive into a plaintext alphabet, which looks hard to reconcile with readable English - unless the expanded string is meant to be regrouped back into a, b, c letters some other way (e.g. 2-3-3 vs 3-3-2 ambiguity is resolved by position rather than by a fixed expansion).
