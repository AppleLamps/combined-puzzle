# Naddiseo#13 Proposed first step toward solving the DBBI and FAED blocks and obtaining a block beginning with BTCSEED (Loupi201 2026-08-24, open)

This is a possible lead concerning the two still-unsolved SalPhaseIon blocks, usually referred to as DBBI and FAED after their first few letters.

Using a Bifid cipher, this method produces a new 570-character block beginning with:

```text
BTCSEED
```

I do not consider this a confirmed solution to SalPhaseIon. At this stage, it is simply a reproducible path that gives an interesting enough result to be included in the Unverified section.

## 1. The two starting blocks

### DBBI block

```text
d b b i b f b h c c b e g b i h a b e b e i h b e g g e g e b e b b g e h h e b h h f b a b f d h b e f f c d b b f c c c g b f b e e g g e c b e d c i b f b f f g i g b e e e a b e
```

Without spaces:

```text
dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe
```

This block contains 91 characters.

### FAED block

```text
f a e d g g e e d f c b d a b h h g g c a d c f e d d g f d g b g i g a a e d g g i a f a e c g h g g c d a i h e h a h b a h i g c e i f g b f g e f g a i f a b i f a g a e g e a c g b b e a g f g g e e g g a f b a c g f c d b e i f f a a f c i d a h g d e e f g h h c g g a e g d e b h h e g e g h c e g a d f b d i a g e f c i c g g i f d c g a a g g f b i g a i c f b h e c a e c b c e i a i c e b g b g i e c d e g g f g e g a e d g g f i i c i i i f i f h g g c g f g d c d g g e f c b e e i g e f i b g i b g g g h h f b c g i f d e h e d f d a g i c d b h i c g a i e d a e h a h g h h c i h d g h f h b i i c e c b i i c h i h i i i g i d d g e h h d f d c h c b a f g f b h a h e a g e g e c a f e h g c f g g g g c a g f h h g h b a i h i d i e h h f d e g g d g c i h g g g g g h a d a h i g i g b g e c g e d f c d g g a c c d e h i i c i g f b f f h g g a e i d b b e i b b e i i f d g f d h i e e e i e e e c i f d g d a h d i g g f h e g f i a f f i g g b c b c e h c e a b f b e d b i i b f b f d e d e e h g i g f a a i g g a g b e i i c h i e d i f b e h g b c c a h h b i i b i b b i b d c b a h a i d h f a h i i h i c
```

Without spaces:

```text
faedggeedfcbdabhhggcadcfeddgfdgbgigaaedggiafaecghggcdaihehahbahigceifgbfgefgaifabifagaegeacgbbeagfggeeggafbacgfcdbeiffaafcidahgdeefghhcggaegdebhhegeghcegadfbdiagefcicggifdcgaaggfbigaicfbhecaecbceiaicebgbgiecdeggfgegaedggfiiciiififhggcgfgdcdggefcbeeigefibgibggghhfbcgifdehedfdagicdbhicgaiedaehahghhcihdghfhbiicecbiichihiiigiddgehhdfdchcbafgfbhaheagegecafehgcfggggcagfhhghbaihidiehhfdeggdgcihggggghadahigigbgecgedfcdggaccdehiicigfbffhggaeidbbeibbeiifdgfdhieeeieeecifdgdahdiggfhegfiaffiggbcbcehceabfbedbiibfbfdedeehgigfaaiggagbeiichiedifbehgbccahhbiibibbibdcbahaidhfahiihic
```

This second block contains exactly 570 characters.

## 2. Building the alphabet from DBBI

The idea is simply to take the DBBI block and remove letters that have already appeared, while keeping the order of their first occurrence.

The beginning gives:

```text
d b b i b f b h c c b e g b i h a
```

Keeping each letter only once gives:

```text
d b i f h c e g a
```

This gives:

```text
DBIFHCEGA
```

It is actually not necessary to use all 91 characters to obtain this sequence, since all the useful letters appear very early in the block. Using the entire block gives the same result.

The remaining unused letters of the alphabet are then added in alphabetical order, with J removed as in a standard Bifid square.

This gives:

```text
DBIFHCEGAKLMNOPQRSTUVWXYZ
```

The corresponding 5×5 grid is:

```text
D B I F H
C E G A K
L M N O P
Q R S T U
V W X Y Z
```

## 3. Decrypting FAED with this grid

The complete FAED block is used as the ciphertext:

```text
faedggeedfcbdabhhggcadcfeddgfdgbgigaaedggiafaecghggcdaihehahbahigceifgbfgefgaifabifagaegeacgbbeagfggeeggafbacgfcdbeiffaafcidahgdeefghhcggaegdebhhegeghcegadfbdiagefcicggifdcgaaggfbigaicfbhecaecbceiaicebgbgiecdeggfgegaedggfiiciiififhggcgfgdcdggefcbeeigefibgibggghhfbcgifdehedfdagicdbhicgaiedaehahghhcihdghfhbiicecbiichihiiigiddgehhdfdchcbafgfbhaheagegecafehgcfggggcagfhhghbaihidiehhfdeggdgcihggggghadahigigbgecgedfcdggaccdehiicigfbffhggaeidbbeibbeiifdgfdhieeeieeecifdgdahdiggfhegfiaffiggbcbcehceabfbedbiibfbfdedeehgigfaaiggagbeiichiedifbehgbccahhbiibibbibdcbahaidhfahiihic
```

In the dCode Bifid decoder, the following settings are used:

```text
Alphabet:
DBIFHCEGAKLMNOPQRSTUVWXYZ

Grid:
D B I F H
C E G A K
L M N O P
Q R S T U
V W X Y Z

Period / Blocks Length:
570

Coordinates Reading Mode:
Row-Column (Normal mode)
```

The value 570 simply comes from the length of the complete FAED block.

## 4. Result

With these settings, the complete 570-character result is:

```text
btcseeddeoemckeadhbschdkbdcsdkdvbxcpcochcrdicibqeebddbcndsbdcpdgcpdncncsescgddclenbmcuducqcacdeldzelcmefdfesdodwckbycubwbaesbwbnemedeadobrcpbgbqcoegbsenesblbtesdadpduescpcreacnckcscdcnbedkckctclbrenenccegelcncubsbgeseienduefddbackdnbsdsescrbsebblbierdvcobdccegbseobvbvcdemcpcscgeldiegdadwdycacpegenbyebcgclcrdbbrdgdbdmercncgdtcdbncfclcpdnbrbbebcnereremeldsdadlencqbochdqdgbxegcfcueeeidacieadoctdneiegdeeldeelbmckedbbeacmcodremcccmcscgdbcocmdtdlbmcdbmbmdpbsdnbsdyeoeocienbseobicbbbcncnecducibecccgdocmeedubndeelblbacpcpcmdxdxdrdgcbcmdndrddecdweadhbtdicqcpdoefdhdgdxdpciel
```

The first seven characters immediately give:

```text
BTCSEED
```

There is also another interesting detail in the result: the letter z appears only once in the entire 570-character output.

If we separate the result around this single z, while also isolating BTCSEED, it becomes much easier to see:

```text
BTCSEED

deoemckeadhbschdkbdcsdkdvbxcpcochcrdicibqeebddbcndsbdcpdgcpdncncsescgddclenbmcuducqcacdeld

z

elcmefdfesdodwckbycubwbaesbwbnemedeadobrcpbgbqcoegbsenesblbtesdadpduescpcreacnckcscdcnbedkckctclbrenenccegelcncubsbgeseienduefddbackdnbsdsescrbsebblbierdvcobdccegbseobvbvcdemcpcscgeldiegdadwdycacpegenbyebcgclcrdbbrdgdbdmercncgdtcdbncfclcpdnbrbbebcnereremeldsdadlencqbochdqdgbxegcfcueeeidacieadoctdneiegdeeldeelbmckedbbeacmcodremcccmcscgdbcocmdtdlbmcdbmbmdpbsdnbsdyeoeocienbseobicbbbcncnecducibecccgdocmeedubndeelblbacpcpcmdxdxdrdgcbcmdndrddecdweadhbtdicqcpdoefdhdgdxdpciel
```

The structure is therefore:

```text
BTCSEED
+
90 characters
+
z
+
472 characters
```

The z is character number 98 in the complete 570-character result.

The result can be reproduced in dCode as shown in the screenshot below:

<img width="789" height="466" alt="salphaseion-dbbi-faed-bifid-btcseed" src="https://github.com/user-attachments/assets/88fd1b1e-6ad0-488b-9e55-c6c1b756f4bc" />

## 5. Why I think this lead is worth keeping

What I find interesting here is not only the appearance of BTCSEED, but also the small number of steps needed to obtain it.

We start from the two blocks we are already trying to understand:

```text
DBBI
FAED
```

The first one naturally gives an alphabet after removing repeated letters:

```text
DBBI
↓
DBIFHCEGA
↓
DBIFHCEGAKLMNOPQRSTUVWXYZ
```

This alphabet can then be used directly as a Bifid grid.

FAED is used as-is, with its full length of 570 as the period, and the result immediately begins with:

```text
BTCSEED
```

There is no need to test hundreds of different keys or periods to obtain this particular result.

That is why I think this path is worth documenting, even though the whole output is not yet understood.

## 6. The single z and its similarity with SalPhaseIon

The single z in the Bifid result may also be worth paying attention to because SalPhaseIon already uses z as a separator.

In the original SalPhaseIon material, z characters separate some of the different encoded sections. The structure seen there is essentially of the form:

```text
...
z
...
z
...
```

Some of these separated sections were later decoded into values such as:

```text
lastwordsbeforearchichoice

thispassword
```

So z already has an identifiable structural role elsewhere in SalPhaseIon.

This makes the fact that the Bifid output contains exactly one z interesting.

The output can therefore provisionally be viewed as:

```text
BTCSEED

deoemckeadhbschdkbdcsdkdvbxcpcochcrdicibqeebddbcndsbdcpdgcpdncncsescgddclenbmcuducqcacdeld

Z

elcmefdfesdodwckbycubwbaesbwbnemedeadobrcpbgbqcoegbsenesblbtesdadpduescpcreacnckcscdcnbedkckctclbrenenccegelcncubsbgeseienduefddbackdnbsdsescrbsebblbierdvcobdccegbseobvbvcdemcpcscgeldiegdadwdycacpegenbyebcgclcrdbbrdgdbdmercncgdtcdbncfclcpdnbrbbebcnereremeldsdadlencqbochdqdgbxegcfcueeeidacieadoctdneiegdeeldeelbmckedbbeacmcodremcccmcscgdbcocmdtdlbmcdbmbmdpbsdnbsdyeoeocienbseobicbbbcncnecducibecccgdocmeedubndeelblbacpcpcmdxdxdrdgcbcmdndrddecdweadhbtdicqcpdoefdhdgdxdpciel
```

I am not claiming that this z definitely has the same function here.

But the similarity is worth recording:

* SalPhaseIon already uses z as a separator.
* The 570-character Bifid result contains exactly one z.
* The z appears after BTCSEED and another 90 characters.
* It divides the remaining output into two clearly defined parts.

This gives us another structural feature to investigate instead of looking only at the appearance of BTCSEED.

## 7. What remains to be understood

The main problem is still that the characters after BTCSEED do not immediately produce readable English.

Before the z we have:

```text
deoemckeadhbschdkbdcsdkdvbxcpcochcrdicibqeebddbcndsbdcpdgcpdncncsescgddclenbmcuducqcacdeld
```

Then:

```text
z
```

And after the z:

```text
elcmefdfesdodwckbycubwbaesbwbnemedeadobrcpbgbqcoegbsenesblbtesdadpduescpcreacnckcscdcnbedkckctclbrenenccegelcncubsbgeseienduefddbackdnbsdsescrbsebblbierdvcobdccegbseobvbvcdemcpcscgeldiegdadwdycacpegenbyebcgclcrdbbrdgdbdmercncgdtcdbncfclcpdnbrbbebcnereremeldsdadlencqbochdqdgbxegcfcueeeidacieadoctdneiegdeeldeelbmckedbbeacmcodremcccmcscgdbcocmdtdlbmcdbmbmdpbsdnbsdyeoeocienbseobicbbbcncnecducibecccgdocmeedubndeelblbacpcpcmdxdxdrdgcbcmdndrddecdweadhbtdicqcpdoefdhdgdxdpciel
```

There are also many recurring structures involving b, c, d and e.

In some places these letters appear at the end of groups, while elsewhere similar-looking structures seem to appear in reverse, with these letters at the beginning.

This part is not solved yet, but it may suggest that what follows BTCSEED is not random noise and could contain another transformation or encoding layer.

## Current state

For now, I would summarize the proposed path like this:

```text
DBBI
↓
remove repeated letters
↓
DBIFHCEGA
↓
complete the Bifid alphabet
↓
DBIFHCEGAKLMNOPQRSTUVWXYZ
↓
Bifid decryption of FAED
Period = 570
Row-Column
↓
BTCSEED
↓
90 characters
↓
Z
↓
472 characters still to understand
```

BTCSEED is reproducible with this method.

The presence of a single z is also interesting because z already acts as a separator elsewhere in SalPhaseIon.

The open question is whether the material on either side of this z contains another layer of encryption, encoding or transformation.

At this stage, this is only a proposed path. I do not know whether this is the route JRK intended us to find, or whether the appearance of BTCSEED and the position of the z are intentional.


---
## Naddiseo 2026-08-24
I agree it's worth pursuing further.

I'm assuming people have already tried sha256 those two new strings and using them passwords for the aes blocks, or using them as keys or seeds for the address?

---
## noahfavreau 2026-08-24
Let f(x) denote the empirical frequency of letter x in the 570-character FAED string. Define the induced row and column marginals:
 
P(row = r) = Σ f(x) over x with row(x) = r, divided by 570
P(col = c) = Σ f(x) over x with col(x) = c, divided by 570
 
From the observed frequencies (F:57, A:54, E:69, D:49, G:107, C:52, B:49, H:58, I:75):
 
P(row=1) = 288/570 = 0.5053, P(row=2) = 282/570 = 0.4947
P(col=1) = 101/570 = 0.1772, P(col=2) = 118/570 = 0.2070, P(col=3) = 182/570 = 0.3193, P(col=4) = 111/570 = 0.1947, P(col=5) = 58/570 = 0.1018
 
Treating the source letters feeding distinct output positions as independent draws from these marginals, a valid approximation since each output position depends on a distinct pair of source indices in FAED, the probability of a given plaintext letter at position i is the product of two marginal probabilities: row×row for odd i, col×col for even i, evaluated at the grid coordinates of the required letter.
 
| i | letter | (row,col) | parity | expression | value |
|---|---|---|---|---|---|
| 1 | B | (1,2) | odd | P(row=1)P(row=2) | 0.2500 |
| 2 | T | (4,4) | even | P(col=4)² | 0.0379 |
| 3 | C | (2,1) | odd | P(row=2)P(row=1) | 0.2500 |
| 4 | S | (4,3) | even | P(col=4)P(col=3) | 0.0622 |
| 5 | E | (2,2) | odd | P(row=2)² | 0.2448 |
| 6 | E | (2,2) | even | P(col=2)² | 0.0429 |
| 7 | D | (1,1) | odd | P(row=1)² | 0.2553 |
 
Under independence across positions, the joint probability is the product:
 
P(BTCSEED) = 0.2500 × 0.0379 × 0.2500 × 0.0622 × 0.2448 × 0.0429 × 0.2553 = 3.9457 × 10⁻⁷
 
equivalently 1 in 2,534,412.
 
The analytic result was checked against direct simulation, independent of the derivation above. Letters were sampled i.i.d. from the empirical FAED distribution and compared against BTCSEED, over 2×10⁸ trials.
 
Result: 85 matches. Empirical probability p̂ = 4.25 × 10⁻⁷. Exact Poisson 95% confidence interval: [3.39 × 10⁻⁷, 5.26 × 10⁻⁷], equivalently 1 in 1,902,880 to 1 in 2,945,726.
 
The analytic value falls within this interval.
 
Thus, P(BTCSEED) ≈ 4 × 10⁻⁷, approximately 1 in 2.5 million.

 

---
## etheral-dev 2026-08-25
I reproduced this (same alphabet, period 570, row-column) and get `BTCSEEDDEOEM...` with one z at position 98, so the recipe is sound. The output tells a different story than it looks like though.

The alphabet starts `DBIFHCEGA`, which is exactly the nine letters FAED is written in, so every ciphertext letter sits in rows 1 and 2 of the grid. With period equal to the full length, Bifid takes both coordinates of each odd plaintext position from ciphertext *rows*, so all 285 odd positions can only be D, B, C or E. That is the "recurring structures involving b, c, d and e" in the writeup, and it's the key doing it, not the plaintext. In BTCSEED the B, C, E and D at positions 1, 3, 5, 7 each cost about 1 in 4; the only real coincidence is T, S, E at three even positions.

The single z falls out the same way. Z is at (4,4), and the only column-4 letter available is H, so a z needs H at two paired positions. H is 58 of 570 letters, so the expected count is 285 × (58/570)² ≈ 3. Getting one is unremarkable, and it isn't a separator.

On the 1 in 2.5 million: that's the probability for this one configuration. Same alphabet, other settings dCode offers (column-row, periods 5 to 285) give `BTC` as a substring in 4 of 15 and `SEED` in 1, because half the text is drawn from four letters. Stronger version of the same point: shuffle FAED's letters at random and decrypt with this key, and `BTC` appears somewhere in the output about half the time (20,000 trials), `SEED` about 6%. Before anyone sha256's these strings into the AES blocks, I'd want a target word that shows up at odd positions with letters outside {b,c,d,e}, which this key can't produce by construction.


---
## Naddiseo 2026-08-25
> I reproduced this (same alphabet, period 570, row-column) and get `BTCSEEDDEOEM...` with one z at position 98, so the recipe is sound. The output tells a different story than it looks like though.
> 
> The alphabet starts `DBIFHCEGA`, which is exactly the nine letters FAED is written in, so every ciphertext letter sits in rows 1 and 2 of the grid. With period equal to the full length, Bifid takes both coordinates of each odd plaintext position from ciphertext _rows_, so all 285 odd positions can only be D, B, C or E. That is the "recurring structures involving b, c, d and e" in the writeup, and it's the key doing it, not the plaintext. In BTCSEED the B, C, E and D at positions 1, 3, 5, 7 each cost about 1 in 4; the only real coincidence is T, S, E at three even positions.
> 
> The single z falls out the same way. Z is at (4,4), and the only column-4 letter available is H, so a z needs H at two paired positions. H is 58 of 570 letters, so the expected count is 285 × (58/570)² ≈ 3. Getting one is unremarkable, and it isn't a separator.
> 
> On the 1 in 2.5 million: that's the probability for this one configuration. Same alphabet, other settings dCode offers (column-row, periods 5 to 285) give `BTC` as a substring in 4 of 15 and `SEED` in 1, because half the text is drawn from four letters. Stronger version of the same point: shuffle FAED's letters at random and decrypt with this key, and `BTC` appears somewhere in the output about half the time (20,000 trials), `SEED` about 6%. Before anyone sha256's these strings into the AES blocks, I'd want a target word that shows up at odd positions with letters outside {b,c,d,e}, which this key can't produce by construction.

I ended up running a similar analysis because something felt off about the probability stated above. It's not enough for me to say "this is not a viable path forward" but it's definitely not obvious if it truly is. I think what I'd want to see next: if we shuffle the key `DBIFHCEGA` do we still end up seeing "btcseed" in the output? If not, that seems to me to point to that there might be something intentional behind both strings as they've being using in bifid.

---
## noahfavreau 2026-08-25
> I ended up running a similar analysis because something felt off about the probability stated above. It's not enough for me to say "this is not a viable path forward" but it's definitely not obvious if it truly is. I think what I'd want to see next: if we shuffle the key `DBIFHCEGA` do we still end up seeing "btcseed" in the output? If not, that seems to me to point to that there might be something intentional behind both strings as they've being using in bifid.

I ran the exhaustive version of the test you suggested: all 9! = 362,880 permutations of the `DBIFHCEGA` prefix, keeping FAED, period 570, and the Row-Column Bifid settings fixed.

The result is somewhat interesting:

```text
Total permutations: 362,880
BTCSEED at index 0:  8
BTCSEED anywhere:   8
```

So the probability within the space of all permutations of these nine letters is:

```text
8 / 362880 ≈ 2.205 × 10^-5
```

or about 1 in 45,360.

I also checked the matching permutations. The 8 keys that produce `BTCSEED` are:

```text
DBIFHCEGA
DBIFGCEHA
DCHAGBEIF
DCGAHBEIF
EBIFHCDGA
EBIFGCDHA
ECHAGBDIF
ECGAHBDIF
```

The original `DBIFHCEGA` is therefore not unique, but it is also definitely not the case that an arbitrary permutation of the nine letters produces `BTCSEED`. In fact, only 8/362,880 permutations do, and every match is at the beginning of the plaintext rather than merely occurring somewhere later.

So I think this gives us a more nuanced result than either "BTCSEED proves the key" or "BTCSEED is completely explained by the structure."

The structural constraints you pointed out definitely matter: because the ciphertext only contains the nine letters in the first two rows, some plaintext positions are restricted to a small subset of the alphabet. However, the exhaustive permutation test suggests that the ordering of those nine letters still matters substantially for obtaining the complete `BTCSEED` prefix.

I don't think this establishes intentionality yet, especially since there are 7 alternative permutations that also produce it. But it does seem worth looking at why these particular 8 permutations work.

---
## noahfavreau 2026-08-25
Also concerning the `z`.

`Z` is at coordinate `(4,4)`. Since every ciphertext character lies in rows 0 or 1, a `Z` in the plaintext can only occur at the positions whose coordinates are derived from ciphertext columns. Therefore a `Z` occurs precisely when the two relevant ciphertext characters both occupy column 4.

In the FAED ciphertext there is:

```text id="vxxk1k"
1 pair of H/H
8 pairs of G/G
```

at the relevant separated positions.

Therefore:

```text id="xwby0b"
H at column 4 -> 1 Z
G at column 4 -> 8 Zs
```

And this exactly explains the distinction between the 8 successful keys:

```text id="c5j2n4"
DBIFHCEGA -> H at column 4 -> 1 Z
DBIFGCEHA -> G at column 4 -> 8 Zs
DCHAGBEIF -> G at column 4 -> 8 Zs
DCGAHBEIF -> H at column 4 -> 1 Z

EBIFHCDGA -> H at column 4 -> 1 Z
EBIFGCDHA -> G at column 4 -> 8 Zs
ECHAGBDIF -> G at column 4 -> 8 Zs
ECGAHBDIF -> H at column 4 -> 1 Z
```

So the single `z` is not independent evidence that `z` is acting as a SalPhaseIon separator.

---
## etheral-dev 2026-08-26
Thanks for running the exhaustive version, and one correction to my own comment first: my "BTC about half the time, SEED about 6%" figures were for those substrings appearing *anywhere* in the 570 characters. The observation is a 7-character prefix, and under the same shuffle-FAED null that costs 1 in 2.27 million (exact hypergeometric; your 1 in 2.5M is right for that event). So that part of my argument was the wrong event and I withdraw it.

The 8 of 362,880 reproduces exactly, same eight keys. What it means is the part I would push back on. I enumerated the 7-character head for all 9! keys: there are 73,097 distinct achievable heads, and on average **4.96 keys produce each one**. 840 heads are produced by exactly 8 keys, 14,880 by exactly one. So "only 8 permutations give BTCSEED" is what every achievable head looks like, not a property of this one.

Why it is exactly 8 has a closed form. The head depends on just eight ciphertext letters, `ct[0..3] = f a e d` and `ct[285..288] = a i e d`. T and S live in the fixed tail at (3,3) and (3,2), so they anchor everything: F and A must both sit in column 3, I in column 2, E and D on the diagonal (a diagonal letter maps to itself, which is where the EE and DD come from), and B and C then land on the two off-diagonal corners. That fixes seven of the nine letters up to three independent swaps, {D,E}, {F,A}, {G,H}, and 2^3 = 8. Your list is exactly that set.

The "every match is at the beginning" observation is also a ciphertext property rather than a key one. An odd offset would need T at a row-pair position, and rows are in {0,1}, so it is impossible for any key. An even offset 2m needs `ct[m]`, `ct[m+1]` and `ct[285+m]` in column 3, `ct[286+m]` in column 2, and `ct[m+2]` and `ct[287+m]` both on the diagonal, all consistently with where B, C, D, E end up. I solved that for all 282 even offsets; m = 0 is the only one that admits any key at all (the 8).

On what would have counted as a hit: using a pre-declared rule (a crypto token plus a word, or a single English word of 7+, in the first 24 characters), 78 of the 362,880 keys produce a head as thematic as BTC+SEED, including `eyeseed` (24 keys), `facebtc` (6), `btc+rind`, `btc+ring`, `eth+ricin`. Pricing the actual recipe as the null, i.e. shuffle DBBI and re-derive the key by first occurrence, that is about 1 in 5,200 per recipe. I also scanned 320 natural Bifid variants (both blocks, five key derivations, both coordinate modes, encrypt and decrypt, eight periods); this recipe is the only one that passes, against 0.07 expected, so roughly 1 in 15 for Bifid alone, before counting the other cipher families people have been running over these two blocks for years.

On the z I agree, and I get the same 1 h/h and 8 g/g pairs at (j, 285+j).

On @Naddiseo's question: I took 33 variants of the strings (full output, `btcseed`, the 90 before the z, the 472 after, even and odd streams, the key, both blocks, case variants) and tried sha256 and sha256d of each as a private key against the prize address, the second address and the published pubkey: 0 of 66. As passwords for the urlblob container under EVP-md5/sha1/sha256 and PBKDF2, plus their sha256 hex: 0 valid pads out of 396, with 1.5 expected by chance.

Where that leaves me: the structure after the seventh letter is forced by the key, nothing after it reads, and the head is what a few thousand cheap recipes over these blocks should have produced by chance about once. I would want a head that survives a pre-declared acceptance set on a fresh recipe before spending more on this branch. Happy to share the scripts if useful.


---
## Naddiseo 2026-08-26
I guess to rephrase my thoughts: it's interesting that the puzzle creator decided to stick two strings next to each other that when combined using bifid give us "BTCSEED" as the prefix, especially given his hints about "are you really looking for just the btc...?"

---
## etheral-dev 2026-08-26
I think the instinct is reasonable, but I went back to the corpus for that hint and I read it the other way.

The full exchange is 2023-08-03: a solver asks @SoWut to "shine us some 'light'", Jrk answers "Ok ok ok ok. I can't hold this one any longer." and then "Are you really looking for just the btc...?". Put next to 2024-04-19 ("There are few prizes to win besides the banter in this chat. A private key, some 'obscure' intel, or what I hope most of you have discovered by now, the most obvious reason to make sure you hold on to Bitcoin") and 2026-07-12 ("The '5' btc was never the actual prize. That was only a tiny fraction."), the consistent reading is that he is playing down the coin in favour of the idea, not pointing at a string that contains the letters BTC. On that reading a decode whose one salient feature is the token BTC is closer to the thing he is telling us not to fixate on.

He also gave an explicit marker for these blocks, and it is a different word. 2023-08-06, described as probably the last hint: "Once you hit a 'ying yang', you'll be able to solve it the same day." `yinyang` is one of the four ingredient tokens from the 2023-02-23 binary (`yellowblueprimes matrixsumlist lastwordsbeforearchichoice yinyang`), and unlike the others it is a decode output rather than a container anyone can open, so it has to come out of material like these two blocks. That makes `yinyang` in the plaintext his stated success criterion for a decode here, not BTCSEED.

On the adjacency, they are not actually adjacent. In the soup the layout is

```text
dbbi    [0:91]      91 symbols over a-i
        [91:195]   104 symbols over {a,b} = the 8-bit ASCII of "matrixsumlist"
faed    [195:765]  570 symbols over a-i
```

so there is a fully solved block sitting between them, and it is the reason we know a/b = 0/1 and that payloads in this region are plain ASCII. The part of the adjacency that is real is also already spent by the recipe: dbbi supplies the key and faed the ciphertext, so the pairing *is* the method, not independent evidence that the method's output was intended. Counting it on both sides is a lot of what makes the result feel designed.

None of that rules out the creator having built something into this pair. But with the hint pointing away from the coin, his own marker being `yinyang`, and the head being about what a few thousand cheap recipes over these two blocks should produce by chance once, I don't think BTCSEED is it.


---
## noahfavreau 2026-08-26
All in all, I don’t think BTCSEED should be a priority, but I firmly believe we should have more of these issues/discussions on similar topics. It can definitely help us all.

---
## prio935 2026-09-22
if the creator is here... „www.past...„ and „www.anon....„ are not working. huge steps are missing. no one will be able to solve this in this conditions
