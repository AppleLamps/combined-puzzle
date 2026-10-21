# GSMG.io 5 BTC puzzle: source pack for an independent solver

Built 2026-10-17 by script from the original files. Every data block below (HTML pages, ciphertexts, plaintexts, decoded strings, the creator's messages) was generated from the files, never retyped, and each one was checked against a hash or a decryption when the file was built.

## 0. How to use this file

You are being asked to work on this puzzle from first principles. A previous team spent a long time on it and did not finish. Their conclusions may be wrong, and so may their reasons for dropping a line of attack. This file is laid out so that you meet the primary material first and their opinions last, clearly labelled.

Every statement in the prose is tagged with one of three marks:

- **[V] verified**: a byte-level fact anyone can reproduce from the data in this file (a hash, a decryption, a count, a decode). The check code is included or is one line.
- **[R] reading**: an interpretation by earlier solvers or the previous team. It may be right, partly right, or wrong. Do not build on it without your own reason.
- **[T] tested**: something the previous team tried that produced nothing. Their tools could have had bugs, their spelling or encoding choices could have been off, and a null under one setup says nothing about a different setup. Treat every [T] line as reopenable.

Two hard limits from the person handing you this file:

1. Do not submit anything to `gsmg.io/phase1verification` (the site's live answer form).
2. Do not try to contact, identify or locate the puzzle's creator or anyone else. Work from the material.

The poster image (`puzzle.png`) is attached separately. Check that its sha256 is `38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830` (29,931 bytes, 1048x1556 RGBA). Copies that were resized or re-saved will have a different hash and may differ in pixels.

This is the second build of the file (17 October 2026). Compared with the first build of the same day it adds: the point form that can win (section 1); measured controls for the dbbi parse and the faed block, and an arithmetic result on the faed block (section 6.3); the runs and the outside claims that were checked in October 2026 (sections 8 and 8.1); and the standing of the creator export after 1 September 2026 (section 2). Nothing in the primary material (sections 3 to 5 and Appendix A) changed.

## 1. The goal [V]

Find the private key for this Bitcoin address (about 1.256 BTC on it as of September 2026):

```
address       1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
hash160       a9553269572a317e39f0f518cb87c1a0ee1dbae4
pubkey (unc.) 04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a46
              49c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559
pubkey (cmp.) 03f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464
```

The address has spent twice, so its public key is public. A candidate private key is correct if and only if its public key hashes to the hash160 above. The address was derived from the uncompressed public key: the uncompressed serialization hashes to `a9553269...dbae4`, the compressed serialization of the same point hashes to `06bbdc66fda09110435c79a86656a604c2d5c69b` and can never match [V]. The check below tries both forms, which costs nothing; a check of the compressed form alone would miss the key. Nothing else confirms a win, and a wrong candidate gives no feedback about closeness.

```python
import hashlib, coincurve
def h160(b): return hashlib.new('ripemd160', hashlib.sha256(b).digest()).hexdigest()
def is_win(priv32: bytes) -> bool:
    pk = coincurve.PrivateKey(priv32).public_key
    return any(h160(pk.format(c)) == 'a9553269572a317e39f0f518cb87c1a0ee1dbae4' for c in (True, False))
# control: private key 1 must give hash160 751e76e8199196d454941c45d1b3a323f1433bd6 (compressed)
```

How the key is encoded when you find it (raw 32 bytes, hex, WIF, sha256 of a phrase, a BIP39 seed, something else) is unknown. The address prefix `1GSMG` is a vanity prefix [V].

On-chain facts [V]: funded with 5 BTC on 2019-04-13 (block 571,497); 2.5 BTC moved out on 2020-05-11 (block 630,001, nLockTime 629,998) and 1.25 BTC on 2024-04-24 (block 840,725, nLockTime 840,003), both to `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`, timed to the Bitcoin halvings. Small "dust" payments with OP_RETURN text have been sent to these addresses since 2025 by third parties; anyone can send those, so they carry no authority [V for the mechanics; the creator also denied writing on-chain messages, #12653].

## 2. Sources and their standing

- **Primary [V]:** the poster, the three web pages of the original puzzle (archived 2019 to 2020 captures, reproduced in section 3), the ciphertexts inside them, and the creator's own messages in the solvers' Telegram group (account "Jrk Bgrt", full export in Appendix A, 492 messages from 2019-04-20 to 2026-09-01). A separate whole-group extract for 2026-09-15 to 2026-10-05 (2,736 messages) holds no message from the creator's account [V]; the creator's messages between 2026-09-01 and 2026-09-14, and after 2026-10-05, are not in this file. Another solver's export is known to run to 2026-10-08.
- **Not primary:** the gsmg.io site as relaunched in August 2026 (pages restored on 2026-08-15 to 17; it adds a `robots.txt` rabbit, a terminal animation and an HTML comment that the archived pages do not have). Community write-ups and AI outputs.
- The creator's messages are hints of varying weight. Read each one together with the message it replies to; the export keeps reply links (`-> replying to #NNNN`).

## 3. Primary material, verbatim

### 3.1 The poster [V]

A 14x14 grid of 75-pixel cells at the top of the image, a red divider (`#ED1C24`) from y = 1047, the title text `GSMG.IO 5 BTC PUZZLE CHALLENGE`, a QR code and the prize address below. The image is 1048 pixels wide, so the last grid column is 73 pixels.

Grid colours, measured on the canonical file: black `#000000` 86 cells, white `#FFFFFF` 85, blue `#3F48CC` 15, yellow `#FFF200` 9, and exactly one cell `#FEFEFE` (off-white, row 7 col 4 counting from 0). Every cell is one flat colour except seven cells where a white rabbit is drawn in black ink at the centre (rows 6 to 8, cols 6 to 9). The QR code decodes to `https://www.blockchain.com/btc/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`. The PNG holds only IHDR, sRGB, gAMA, pHYs, IDAT and IEND chunks and has no bytes after IEND.

The grid as letters (K black, W white, B blue, Y yellow, F off-white; rabbit cells by background):

```
WWKKWBWWKWKKWY
KKBKWWKKKWBWKK
KKWKKKWBWWKWWK
WKKWBWWWWKKKWK
WBKWWWKKWYWKKW
KWWKKWYWKWYWKK
KWWBKKWWWKWYWW
BKKWFWWWWWKWYW
WWWKKBWKKKKKWB
KKBKKKYWKKWWWK
KKWKWWWYWKKWKK
KKKKWWKWBWKKWW
WBWKKKWKWYWKKW
WKBWKKWKKWBWKK
```

**Known reading [V]:** take black and blue as 1, white, yellow and off-white as 0, and read the cells as an inward counter-clockwise spiral from the top-left corner going down first. The first 192 bits, 8 per character, give:

```
gsmg.io/theseedisplanted
```

The last four bits (the centre cells) are `0000`. Every blue and yellow cell sits on bit 7 of a character (the lowest bit), with blue on a 1 and yellow on a 0, so the colours repeat the low bit of each character [V]. Spiral index of the off-white cell (0-based): 163, a 0 bit in the `n` of "planted" [V].

### 3.2 Phase 1 page: `gsmg.io/theseedisplanted` (Wayback capture of 2020-11-12, toolbar removed)

```html
<!DOCTYPE html>
<!-- saved from url=(0075)https://gsmg.io/theseedisplanted -->
<html class="no-js" lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><title>GSMG Puzzle</title>

<meta http-equiv="x-ua-compatible" content="ie=edge">
<meta name="robots" content="noindex">
<meta name="description" content="GSMG Puzzle">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="csrf-token" content="Uzfo0HeZhSs3bW4qQ1VB99iJuP4f7JUSyc6egS1u">
</head>
<body>
 

<img src="../images/rebus/black_banking - war.png">
<img src="../images/rebus/blue_ca.png">
<img src="../images/rebus/blue_dig_i.png">
<img src="../images/rebus/blue_lock_lo.png">
<img src="../images/rebus/red_crypto_gic.png">
<img src="../images/rebus/red_n_you.png">
<img src="../images/rebus/red_open_lock_n_ing.png">
<img src="../images/rebus/red_t.png">
<div style="display: none">
<form method="POST" action="https://gsmg.io/phase1verification" accept-charset="UTF-8"><input name="_token" type="hidden" value="Uzfo0HeZhSs3bW4qQ1VB99iJuP4f7JUSyc6egS1u">
<input type="password" name="password">
<input type="submit">
</form>
</div>


</body></html>
```

The eight images are word fragments [V, transcribed by hand from the tile images]:

| file | content | left/right whitespace in the tile |
|---|---|---|
| black_banking - war.png | bank icon, `war` | pad right |
| blue_ca.png | `CA` | pad right |
| blue_dig_i.png | `dig i` / `+` | pad right |
| blue_lock_lo.png | closed padlock, `lo` | pad right |
| red_crypto_gic.png | `crypto` / `gic` | pad left |
| red_n_you.png | `n you` | pad left |
| red_open_lock_n_ing.png | open padlock, `n ing` | pad left |
| red_t.png | `t` / `-` | pad left |

The answer accepted by the form is `theflowerblossomsthroughwhatseemstobeaconcretesurface` [V: the creator posted its sha256 `5ac40783...6f75` in chat as #225]. Accepting it redirects to the phase 2 page below. **Reading [R]:** the tiles join to CAN YOU / DIG IT / LOGIC / WARNING; "Can you dig it" and the accepted phrase come from the song "The Warning" by Logic, and the phase answers follow lines of that song.

### 3.3 Phase 2 and 3 page: `gsmg.io/choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself`

Byte-identical to a 12 Nov 2020 archive capture. Textarea 1 is the phase 2 container, textarea 2 the phase 3 container.

```html
<!doctype html>
<html class="no-js" lang="en">
<head>
<title>GSMG Puzzle</title>
<meta charset="utf-8">
<meta http-equiv="x-ua-compatible" content="ie=edge">
<meta name="robots" content="noindex">
<meta name="description" content="GSMG Puzzle">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="csrf-token" content="JeQNY8TFYmKwWn8KFH5RJlxXFnmcwdL6Gbjdvcg7">
<style>
        body {
            font-family: 'arial';
        }
    </style>
</head>
<body>

<H1>PHASE 2</H1>
<p>"1... are you looking for the private keymaker?"
You come to me, without it. Come to me with it and you'll have the power to continue. It'll grant the first part.
/(aaa, connected enf)
</p>
<p>Ciphered with aes-256-cbc /w base64 sha-256(password)</p>
<textarea style="width: 100%; height: 200px">U2FsdGVkX18GKGYS1D7X7VjxWz6uUyPFszr8dVvtOIrJqioWHgT69JJnzJGDVOvF
QYWh5BEZxFPXmMq1cbyy3dVVDgLhF050xlDy2J5grtKw9jUOO4oFNRgoD+1dlukX
pd8ccg++kkXgE9mGBP6lQbukDiSjY4mnR2Mv6ydIncrRqacQNVEmEgM4fGTi1ANz
nHsGn7mP+P3UyrJCRbuFmpZJc4CNdPj6YuxwR4HkHkqcfxh0L5CaEu4VbY70+fmk
qgZQyMJqiUlaV9KC4UPuRVj0r7MYbVRazkhsjeIcogmdJGEeBwD47lEB7X9PNKWm
ojTvRZg6R+sZzRZE26VLaF+s9cpTo4Y8PZUxKvQ86HXC8QIavUgDfw7HxIxkTatv
CW2yq3ZOXl5naR6oSNxdX9alyhTzB+/2623oGdlWev5Oo8xHJqUi7QjVP+mNC8BA
+Cg0DJwcOFGO5K7g8Rm06+sLogwntdIgTo70X3FegAtipHboeUNKefiAguvkDoIf
8iMPc+83PygvlZPDNQCOKugwDEUimhHwQrMsmalRNoFEQEb+ZIC+na15cPoRAlOD
NJfXIJ96ihAy9wWis39mQW6JFqZmUags4xoP3lJ35bCrXsNOPFZ4WH+f4YC/Ov8C
QW5bjtxno8GG4b/wBWevhcRVMK6KmRJj8NBCssnrlz0sQ70rMNkiN2wiSPcwX3Ad
JgLs8vQAUM59x9fkKFFzD4+Sc1sJztUTB7CMGGfpZOA8W33VZnEdmGcoaHlDsR8G
vAkZ+jg+QJs9ZNHqWE1+1zgm/6NsWWgWH8OI2PPCfXHxDbfDk8uD/Zibr/yjSKvu
Sb8OecflOT2hw37WL49uADgeWgnp2bzkfGIq7EYS7OImjZZwY5h4sfcPfhvQ9kOV
</textarea>
<p>There's a guy who theorised the idea that 'Any linear electrical network with voltage and current sources and only
resistances can be replaced at terminals A–B by an equivalent current source Ino in parallel connection with an
equivalent resistance Rno'. He might have been insecure. His competition might have been that as well. However,
after enough belikins this competition tried to become a ruler of a piece of land that's technically the poorest of
the entire planet. 4 rulers have shared the first name of the competition. 2 had the firstname in the surname. One
of the rulers had a number, and dirty too. Another had a resemblance to Carrey, James Gates, also Simulacra and
Simulation. Another ruler was at some point a floating zerg house while being under control of the dirty one.. too.
The one after died too soon. Moral: never execute an order that revokes the highest power or you might suddenly get
killed. The 5binary code is a part of the piece of this puzzle.</p>
<p>Years later the idea of this _green_ came _back_. Looking at the current state of nature not quickly enough. Afraid
for random magic pieces of metal, that moved in directions that science couldn't and still can't explain, coming
from places where inspiring papers used to be deposited, a chancellor awaiting banks to be bailed out decided to
write an anarchist digital answer to this worlds' misery. Its' raw data after 4 on row 1616 to be one of the last
pieces of this part required in order to continue this riddle.</p>
<p>/(aBa, connected enf)</p>
<p>B5KR/1r5B/6R1/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 w - - 0 1</p>
<p>And now a buddhist is forced to move. What will be the next situation?</p>
<p>/(aBa, connected not enf)</p>
<p>--> parts 1..7 --> sha-256 -> dgst is the password to enter Phase 3.
Phase 3 is also ciphered with aes-256-cbc /w base64.</p>
<H1>PHASE 3</H1>
<textarea style="width: 100%; height: 300px">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</textarea>
</body>
</html>
```

### 3.4 The side page `gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32` ("SalPhaseIon")

The path is `sha256("GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe")`, the poster's text and address hashed [V]. **Reading [R]:** solvers reached it through the word `HASHTHETEXT`, recovered from an audio side quest in Decentraland, and through creator hint #7416 "go to the first puzzle piece (image) and hash all the text you see".

```html
<!doctype html>
<html class="no-js" lang="en">
<head>
<title>GSMG Puzzle</title>
<meta charset="utf-8">
<meta http-equiv="x-ua-compatible" content="ie=edge">
<meta name="robots" content="noindex">
<meta name="description" content="GSMG Puzzle">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
        body {
            font-family: 'arial';
        }
    </style>
</head>
<body>
<h1> SalPhaseIon </H1>
<textarea style="width: 100%; height: 200px">d b b i b f b h c c b e g b i h a b e b e i h b e g g e g e b e b b g e h h e b h h f b a b f d h b e f f c d b b f c c c g b f b e e g g e c b e d c i b f b f f g i g b e e e a b e a b b a b b a b a b b a a a a b a b b b a b a a a b b b a a b a a b b a b a a b a b b b b a a a a b b b a a b b a b b b a b a b a b b a b b a b a b b a b b a a a b b a b a a b a b b b a a b b a b b b a b a a f a e d g g e e d f c b d a b h h g g c a d c f e d d g f d g b g i g a a e d g g i a f a e c g h g g c d a i h e h a h b a h i g c e i f g b f g e f g a i f a b i f a g a e g e a c g b b e a g f g g e e g g a f b a c g f c d b e i f f a a f c i d a h g d e e f g h h c g g a e g d e b h h e g e g h c e g a d f b d i a g e f c i c g g i f d c g a a g g f b i g a i c f b h e c a e c b c e i a i c e b g b g i e c d e g g f g e g a e d g g f i i c i i i f i f h g g c g f g d c d g g e f c b e e i g e f i b g i b g g g h h f b c g i f d e h e d f d a g i c d b h i c g a i e d a e h a h g h h c i h d g h f h b i i c e c b i i c h i h i i i g i d d g e h h d f d c h c b a f g f b h a h e a g e g e c a f e h g c f g g g g c a g f h h g h b a i h i d i e h h f d e g g d g c i h g g g g g h a d a h i g i g b g e c g e d f c d g g a c c d e h i i c i g f b f f h g g a e i d b b e i b b e i i f d g f d h i e e e i e e e c i f d g d a h d i g g f h e g f i a f f i g g b c b c e h c e a b f b e d b i i b f b f d e d e e h g i g f a a i g g a g b e i i c h i e d i f b e h g b c c a h h b i i b i b b i b d c b a h a i d h f a h i i h i c z a g d a f a o a h e i e c g g c h g i c b b h c g b e h c f c o a b i c f d h h c d b b c a g b d a i o b b g b e a d e d d e z c f o b f d h g d o b d g o o i i g d o c d a o o f i d h z s h a b e f o u r f i r s t h i n t i s y o u r l a s t c o m m a n d U 2 F s d G V k X 1 8 6 t Y U 0 h V J B X X U n B U O 7 C 0 + X 4 K U W n W k C v o Z S x b R D 3 w N s G W V H e f v d r d 9 z a b b a a b a b a b b a b b b a a b b b a b a a a b b a a b a b a b b b a a b a Q v X 0 t 8 v 3 j P B 4 o k p s p x e b R i 6 s E 1 B M l 5 H I 8 R k u + K e j U q T v d W O X 6 n Q j S p e p X w G u N / j J s h a b e f a n s t o o</textarea>
<h1> Cosmic Duality </h1>
<textarea style="width: 100%; height: 200px">U2FsdGVkX18tP2/gbclQ5tNZuD4shoV3axuUd8J8aycGCAMoYfhZK0JecHTDpTFe
dGJh4SJIP66qRtXvo7PTpvsIjwO8prLiC/sNHthxiGMuqIrKoO224rOisFJZgARi
c7PaJPne4nab8XCFuV3NbfxGX2BUjNkef5hg7nsoadZx08dNyU2b6eiciWiUvu7D
SATSFO7IFBiAMz7dDqIETKuGlTAP4EmMQUZrQNtfbJsURATW6V5VSbtZB5RFk0O+
IymhstzrQHsU0Bugjv2nndmOEhCxGi/lqK2rLNdOOLutYGnA6RDDbFJUattggELh
2SZx+SBpCdbSGjxOap27l9FOyl02r0HU6UxFdcsbfZ1utTqVEyNs91emQxtpgt+6
BPZisil74Jv4EmrpRDC3ufnkmWwR8NfqVPIKhUiGDu5QflYjczT6DrA9vLQZu3ko
k+/ZurtRYnqqsj49UhwEF9GfUfl7uQYm0UunatW43C3Z1tyFRGAzAHQUFS6jRCd+
vZGyoTlOsThjXDDCSAwoX2M+yM+oaEQoVvDwVkIqRhfDNuBmEfi+HpXuJLPBS1Pb
UjrgoG/Uv7o8IeyST4HBv8+5KLx7IKQS8f1kPZ2YUME+8XJx0caFYs+JS2Jdm0oj
Jm3JJEcYXdKEzOQvRzi4k+6dNlJ05TRZNTJvn0fPG5cM80aQb/ckUHsLsw9a4Wzh
HsrzBQRTIhog9sTm+k+LkXzIJiFfSzRgf250pbviFGoQaIFl1CTQPT2w29DLP900
6bSiliywwnxXOor03Hn+7MJL27YxeaGQn0sFGgP5X0X4jm3vEBkWvtF4PZl0bXWZ
LvVL/zTn87+2Zi/u7LA6y6b2yt7YVMkpheeOL0japXaiAf3bSPeUPGz/eu8ZX/Nn
O3259hG1XwoEVcGdDBV0Nh0A4/phPCR0x5BG04U0OeWAT/5Udc/gGM0TT2FrEzs/
AJKtmsnj31OSsqWb9wD+CoduYY2JrkzJYihE3ZcgcvqqffZXqxQkaI/83ro6JZ4P
ubml0PUnAnkdmnBCpbClbZMzmo3ELZ0EQwsvkJFDMQmiRhda4nBooUW7zXOIb7Wx
bE9THrt3cdZP5uAgVfgguUNE4fZMN8ATEDhdSsLklJe2GvihKuZVA6uuSkWAsK6u
MGo76xpPwYs3eUdLjtANS83a6/F/fhkX1GXs7zbQjh+Inzk8jhEdEogl9jPs/oDj
KjbkUpFlsCWwAZGoeKlmX7c4OGuD5c+FEH+2nYHvYl8y1E/K5SDt9Uocio8XuxbD
ZOzhw7LMSGkD1MZxpDzsCZY1emkSNd88NFj+9U8VssIDDVMYwKMsHKfjc0x5OlzQ
1f6ST0xCkwydDHHGRKKxFC4y6H6fV9sgf9OPK/65z94Rx72+mfvTyizShjxYSRpl
sH9otU4parl8roD0KsVTfXZoYrYXzK6cXBn1BO/OEqWlu++Dd9MiGaUGKd22fXER
qNWoRAKlNn2b6EehD2D8WaAoliPURjkB0Lb/FpP9unI93Twg6NxBXAj734nctukR
b3kE08RydJV70eJsvEftF5hbED4HacGx9pzisaSz6t9AKiuSoF6uoCtlTIYatyfZ
kQA4wg50hAJqTynOQ09ArRHEchtB/7uvWZSBGJ7+zlzRGKx99P3oDZD+Y5D8bmUs
3PV6FnAp+IRSlnsQ6hChkwBoQUcngcfGSkBRvmGjsGercCetRRwBOfh9fbX2ruw4
mzRYrGnz9eBtepkJXDRjD6yvhNfQMCSkm6l9zMWxKvFbv5g2ae2SLrEt/x3MP2/G</textarea>
</body>
</html>
```

Textarea 1 is the "SalPhaseIon" text (section 6). Textarea 2, under the heading "Cosmic Duality", is a locked container (section 5).

## 4. The solved chain, reproducible [V]

### 4.1 The encryption convention used by every solved container

OpenSSL `Salted__` container, base64. Password = sha256 of the answer, written as 64 lowercase hex characters. Key derivation: legacy `EVP_BytesToKey` with **md = SHA-256**, one iteration. Cipher: AES-256-CBC with PKCS#7 padding. Equivalent command:

```
openssl enc -d -aes-256-cbc -a -md sha256 -pass pass:<sha256hex of answer>
```

```python
import hashlib, base64
from Crypto.Cipher import AES
def evp(pw, salt):
    d = prev = b''
    while len(d) < 48:
        prev = hashlib.sha256(prev + pw + salt).digest(); d += prev
    return d[:32], d[32:48]
def decrypt_b64(b64text, answer):
    raw = base64.b64decode(''.join(b64text.split()))
    assert raw[:8] == b'Salted__'
    pw = hashlib.sha256(answer.encode()).hexdigest().encode()
    k, iv = evp(pw, raw[8:16])
    pt = AES.new(k, AES.MODE_CBC, iv).decrypt(raw[16:])
    p = pt[-1]
    return pt[:-p] if 1 <= p <= 16 and pt[-p:] == bytes([p]) * p else None
```

A wrong key passes the padding check about 1 time in 256, nearly always with a 1-byte pad, so padding alone proves nothing. The same convention is not proven for the locked containers; only their `Salted__` header is known.

### 4.2 Phase 2

Answer `causality`. Plaintext (648 bytes, CRLF line ends shown as plain line breaks):

```
The ironic 2name of the keymakers trying to protect the current digital powers which are still in severe danger due to the keymaker's way of security by hiding, nearly unprotected, in plain sight. {eps3.4_[in one of the valleys of Phillip]runtime-error.r00., where daughters hit magic keypads} When this fails.. Crypto finally to the latin 3Moon? Tell me, 4How so mate?
# X 2 S H 4 Y 0 Q B 15 #
Q -> extend the name of a hackers' swordless fish, the I and W are below.
B -> ((BV80605001911AP)- (sqrt(-1)))^2
H -> (Answer to only this puzzle but nothing else) * -1
S -> cha' + (vagh * jav)
Ok kid, on the highway, let put it in the worst gear.
```

**Reading [R], accepted by solvers:** the `# X 2 S H 4 Y 0 Q B 15 #` template resolves (Q = 82 from the QWERTY row, B = 25, H = 42 with its minus sign dropped, S = 32, then "worst gear" = reverse twice) to the coordinate 51 deg 52' 28.0" N, 4 deg 24' 23.2" E, the former SafeNet office in Rotterdam-Pernis. The inline numerals 2, 3, 4 are indices of the phase 3 answer parts. The sign of H is unresolved.

### 4.3 Phase 3

Answer: the plain concatenation of these seven parts [V by decryption]:

```
1. causality
2. Safenet
3. Luna
4. HSM
5. 11110
6. 0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854
7. B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1
```

**Reading [R]:** 1 is the phase 2 answer reused ("1... are you looking for the private keymaker?"), 2 to 4 come from the numbered phrases in the phase 2 plaintext (2name = Safenet, 3Moon = Luna, 4How so mate = HSM), 5 is Executive Order 11110 ("5binary"), 6 is the Bitcoin genesis-block newspaper headline as reversed hex ("raw data after 4 on row 1616" of an early Bitcoin source file), 7 is the chess position after the move the page's puzzle asks for. The `/(aaa, connected enf)` style tags are read as case and spacing instructions.

Plaintext (4090 bytes; it ends with the phase 3.2 container):

```
What if the merovingian is wrong. What instead of causality something else could be ours? Therefor, if so, the ...... is ours. The thinker's 1name behind all of that would grant you access to the next step (of humanity). Definitely look into his works might you have time. /(aa,connected enf)

I just passed a cheshire cat and I'm getting fed up with this puzzle.. It's taking forever. But, How long is forever? I don't know, but just add giveit in front of the answer and you can fall in the keyhole. /(aa,connected enf)

3.The fundamental limit to the precision with which certain pairs of physical properties are know. /(aa,connected enf)

Phase 3.2 is ciphered with aes-256-cbc base64 and a sha256 pw, yet again.

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
```

### 4.4 Phase 3.2

Answer `jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple` (the three riddle answers joined: Jacque Fresco, "give it just one second", Heisenberg's uncertainty principle) [V by decryption]. The plaintext is 2422 bytes and only about 59% printable; it is mixed ASCII, EBCDIC and a base64 container. Full plaintext as base64:

```
SSd2ZSBiZWVuIHdhaXRpbmcgZm9yIHlvdS4gWW91IGhhdmUgbWFueSBxdWVzdGlvbnMsIGFuZCBhbHRo
b3VnaCB0aGUgcHJvY2VzcyBoYXMgYWx0ZXJlZCB5b3VyIGNvbnNjaW91c25lc3MsIHlvdSByZW1haW4g
aXJyZXZvY2FibHkgaHVtYW4uIEVyZ28sIHNvbWUgb2YgbXkgYW5zd2VycyB5b3Ugd2lsbCB1bmRlcnN0
YW5kLCBhbmQgc29tZSBvZiB0aGVtIHlvdSB3aWxsIG5vdC4gQ29uY29yZGFudGx5LCB3aGlsZSB5b3Vy
IGZpcnN0IHF1ZXN0aW9uIG1heSBiZSB0aGUgbW9zdCBwZXJ0aW5lbnQsIHlvdSBtYXkgb3IgbWF5IG5v
dCByZWFsaXplIGl0IGlzIGFsc28gaXJyZWxldmFudC4NCg0KLi4uIGFtIEkgaGVyZT8gV2FrZSB1cCwg
eW91Li4uIEkndmUgZGVzaWduZWQgeW91IGEgYmVhdXRpZnVsIHN0cmF0ZWdpYyBwb3NpdGlvbi4gT25l
IGZvciBvbmUsIGZvdXIgZm9yIG9uZS4NCg0KzsgszvglX8H4+Mclzc8vx8g6X/b4w9H4zcw/xy/4yM0s
OjrIxdEsw8/4zWAvyD/PYD4lwcLIyc/Dw87FLy8vzPbDJcrMzj8sJdHFPz/MwdHBzPZgz8/NLM3NW8Al
w8/4z8EsP8XLPsXCzsg6Xz7Iwc0lx/jNW8dfyi/C0dHB9vjIzlsvycLL+Mkvzcf4X8D2yccvycfNYMDA
0c/FzM7Mxfg/wy/J0TrLwT7IYMHLyV/FW8fNLzpfYMdfPsrCOtE/YMfNW87JOlvDX8/MP8g/Xz/CJcPB
wiVbPsX4+MvBJcs+Jc8vwcdbPs/MOj4vYD4vW8EvOsfDOsHNPvjBwc/2zsf2YMvJ9vj4P8svJS/COs0v
+CX4+PjIwS/Dzs4+OvjKYMfLPiz2zczLXyzNwj4+0V8/+M0sP/bBPss+JcPMwy/CxcHN9l9gycLJz8g+
XzrRyMLIyc/NLM3Pwz7MX8P4wfjMzdHPzczJyc7Fz8X4Ovj4yD7FzWAvJT8vzss+LPj4zcc/xyxbLzrK
xcdfyvjCx9FbwcXL9sA+yMjIwfjJwF86yizAwsvI0S/CPi/L9l9gyMXHycfRX1svwMX2ziXHzc7JLy8v
wi/CYMjMycfByM4++MssPsLRPvjMzM86yizDWzr2X8f4x8E69l9gwCzJyMnK0cwlYMfAPyXHzT9b+D/B
W88vLC/DP18lzT/ALz/MX8fMLNHBx8EsxSzRyM3BJV9gPsL4zcc/zj/CJfjRYPYvLMLAzczCzSX4wz4+
yFvDX/jJwMvDwCxbL84vOscvLNHB+MElYM4vwsIsP9HIYFvDzs3LxyzCW/bPOs0vwNHOw1/F9sBfwi/P
OsdfPsEswSXHzT9b+GAszcdfPszRPtHKwcX2yTolwT7CYMHMwV8++M1bLyXBwdEv9s7K9l9gx8BfP8Al
wT/4ySzJPj46ycI/P8g+yV9bYMJfwNEv9sxfysBfXz7JYMLFyCUlySxb0TrN0cdf9sn4ztHBx8zPL8gl
0fjRyM3AP8jLw8nFOl8vLF/HPvjJOtE+YMzIOj/FYMXRxc7IX8/CyMXHJfjMyMj4xdHDP8fLxcFf+Cz4
0WAvyM3AP18vYMnIOs/IzcglYF/Iz/j4zcJfyM/PzcdfPs/2+MfAxyzKJcMlXzrRPs3Lx/jHys3RyM0+
0dHBwM7DwNHKwc7A+PglX9HCzMrIwcclyc9gJc/IOl8vycHBL8/HYM/CLzrL0ctfyj7Iwc8vw8zFzsDC
X/b4OvhfwNEvxS8v0cfK9stfyj7Ixc/JLFvJ+Cxb0c/J9s7Kz1s/yPZfyjovOsfIYC/BP8g/yM3Hyj/P
YD7DX/jJwFvBwcVbxcjRyF9bPvjAyT46LM4++PjJy/bKPsX2wc8vYMD2wyXPOs3IYMEly1/CYMzPyTpf
zc/H9s7MP8vBJS/4Ly8vLF/JPiz2PsjB9iz4Os/IP2DIL8o6yc8sJc/JWz/POs0vLMHRycvFzT7Nwjpb
zS8/YMHFJcgsz8fPwz7RwfjRycHFwCxgyczJyT/Jzc/RPsXBW/bBXy86+Mklyc/FYCzBL/Y/zV9fwS8v
ztHC9iXBwM/DzcLLW/b4yMvDwcnMzczBx8/JYMDKwT4vPsrBJcvDzSXDyPhfyV9bP8nByM4sJSXCX8DB
LMc6yszRycvMYM7J9sDFOl8vPvjJx8fLPs/Fy8ksyM8/wMrOOj5fX8U/Xz/A0fb4wj/4yc/4yD9f0T4+
0cfD+M0ly/jNW8XCXz/MwdHBL83OwNEvW8X20ckvzcXRYC8sx2DLwz/L0fZfL8vKOizDP8/Fz8zNwi/N
wfjR9s7K9l9gx8tf0c/4YMH4L1/JOmAlzy8vwc8v9sElYMLBL88/ws7JW87POi8v9s0syM7NLM3AzDrI
wsfDxS9bwC/Dzstf0c8swsclw9HBwPjNxyxbOs8lwT4vLMHILMcsJV/CJcjKYM4vLMHIzccsxyzH+Phf
YM7OwD/F+M/HyM/J0VtgYF/JxT/OzD4/wCzALy8vws/COi/FwC/HPsk+w8svP186L8HBL8/BJSzLJcfJ
Jc/RxdH2DQoNCjE1MTY1OTQzMTIxOTcyNDA5MTY5MTcxMjEzNzU4OTUxODEzMTQxNTQzMTMxNDEyNDI4
MTU0MTkxMzEyMTgxMjE5NDMzMTIxMTcxNjE3MTM3MTQ5MTEwOTE2NjMxMjEzMTMxMjgxNDkxMTA5MTY2
MTMxNDEyMTk5MTE0MzcxNjEyMTI2MDIxNjY0MzEzNzExMTU0MTEyDQoNClJhaXNpbmcgdGhlIHN0YWtl
cyB3aXRob3V0IGV4dHJhIGNoYW5jZXMgb2Ygd2lubmluZy4gQSBmdWJjZC1raW5nICYgb3JhY2xlLXF1
ZWVuLCB0aGluZ2t5IG12cHMsIG9uIGEgc2FkIGJvYXJkIGJ1dCBhcyB3aWRlIGFzIHRoZSBmaXJzdCBv
bmUgc2Vlbi4NCg0KVTJGc2RHVmtYMSswV2w0OWduV1R5aWltbHV1N1YzK3ZsN3N0MGdVdDlzV0R6Tkx4
RG1sUE1zRFNpdVcyYTQ2eg0KZ0tsSWk4YWFxWTVncEpQUEV6VzFuOW4zLzI2cXM0enN0V3RQS0Y4WnMv
QlROTjRJaUVoNHF1MThtZEMwTkF2NA==
```

Its parts [V]:

- bytes 0 to 446, ASCII:

```
I've been waiting for you. You have many questions, and although the process has altered your consciousness, you remain irrevocably human. Ergo, some of my answers you will understand, and some of them you will not. Concordantly, while your first question may be the most pertinent, you may or may not realize it is also irrelevant.

... am I here? Wake up, you... I've designed you a beautiful strategic position. One for one, four for one.
```

- bytes 447 to 1985: 1,539 bytes that, encoded to EBCDIC code page cp273 and read as letters a = 0, decrypt under the reciprocal Beaufort cipher (P = K - C mod 26) with key `THEMATRIXHASYOU` to a rewritten version of the Architect's speech from *The Matrix Reloaded*:

```
YOURLIFEISTHESUMOFAREMAINDEROFANUNBALANCEDEQUATIONINHERENTTOTHEPROGRAMMINGOFTHIS
PUZZLEYOUARETHEEVENTUALITYOFANANOMALYWHICHDESPITEMYSINCERESTEFFORTSIHAVEBEENUNAB
LETOELIMINATEFROMWHATISOTHERWISEAHARMONYOFMATHEMATICALPRECISIONWHILEITREMAINSABU
RDENTOSEDULOUSLYAVOIDITITISNOTUNEXPECTEDANDTHUSNOTBEYONDAMEASUREOFCONTROLWHICHHA
SLEDYOUINEXORABLYHEREYOUYOUHAVENTANSWEREDMYQUESTIONMEQUITERIGHTINTERESTINGTHATWA
SQUICKERTHANTHEOTHERSPLEASEIFYOUFINDAWAYTOCOMPLETETHELASTPARTOFTHEPUZZLETAKETHEP
RIVATEKEYYOUVEEARNEDITBUTPLEASETAKETHISTOHEARTTHATWHATAWISEMANABOVEHINTEDATISWOR
THHUNDREDFOURTYOFTHEINVESTMENTTHATSWHATUSGUYSATGSMGARETRYINGTOACCOMPLISHINTHEEND
PLEASEJUSTHELPUSBUILDITINSTEADOFJUSTWAISTINGYOURLIFETIMEBYHUNTINGFORWORTHLESSPRI
CESANDTHROPHIESLIKETHISIMSORRYTOTELLYOUTHATYOUVECOMETHISFARBUTYOULLNEVERFINISHTH
ELASTTASKIEXPECTYOUTOSAYBULLSHITWELLDENIALISTHEMOSTPREDICTABLEOFALLHUMANRESPONSE
SBUTRESTASSUREDTHISWILLNOTBETHELASTTIMEIHAVEDESTROYEDARESTLESSSOULANDIHAVEBECOME
EXCEEDINGLYEFFICIENTATITTHEFUNCTIONOFTHEYOUISNOWTORETURNTOTHESOURCECODESALLOWING
ATEMPORARYDISSEMINATIONOFTHECODEYOUHOPEFULLYCARRYREINSERTINGTHEPRIMEBASICSAFTERW
HICHYOUWILLBEREQUIREDTOSELECTFROMOVERTWENTYTHREECIPHERSSIXTEENENCRYPTIONSANDORSE
VENINTERTWINEDPASSWORDSTOFINDTHEACTUALPRIVATEKEYNOTETHATALSOBRUTEFORCINGMIGHTBER
EQUIREDFAILURETOCOMPLYWITHTHISPROCESSWILLRESULTINACATACLYSMICSYSTEMCRASHKILLINGY
OURWILLPOWERWHICHCOUPLEDWITHTHEEXTERMINATIONOFYOURWILLTOLIVEANDWILLULTIMATELYRES
ULTINTHEEXTINCTIONOFTHEENTIRENESSOFYOURSELFSELFGOODLUCKNEVERTHELESSIREALLYHOPEYO
URETHEONECIAOBELLAO
```

- bytes 1990 to 2138: 149 digits, a straddling checkerboard:

```
15165943121972409169171213758951813141543131412428154191312181219433121171617137
149110916631213131281491109166131412199114371612126021664313711154112
```

  With the alphabet key `FUBCDORA.LETHINGKYMVPS/JQZXW` and digits 1 and 4 as the blanks of the top row, it decodes to the text below [V]. Earlier solvers report it is the only one of the 45 possible blank pairs that reproduces the digits [R, not rechecked for this file]:

```
INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE
```

- bytes 2143 to 2291, the riddle that gives the checkerboard key:

```
Raising the stakes without extra chances of winning. A fubcd-king & oracle-queen, thingky mvps, on a sad board but as wide as the first one seen.
```

- bytes 2292 to the end: the locked **Terminal** container (section 5).

## 5. The three locked containers [V]

No password is known for any of them. Each starts with `Salted__` and an 8-byte salt.

| name | where it is | ciphertext bytes | salt | sha256 of the raw container |
|---|---|---:|---|---|
| Terminal | end of the phase 3.2 plaintext | 80 | `b45a5e3d827593ca` | `291dfd6f3e759ec2e272b35a00c24907da70c3e7a9291b4c13605c7b0b4f3de9` |
| SalPhaseIon short | inside the SalPhaseIon text | 80 | `3ab585348552415d` | `9e2831e1b34b5f34796df47ccaf6530d48d371c61a6bff84d60db1064fa7a258` |
| Cosmic Duality | side page, textarea 2 | 1328 | `2d3f6fe06dc950e6` | `b18950551a4dd0cb8a9378f0906ba18c03a15f0ee83eb98c6bc90165c5f79805` |

Under a 16-byte block cipher with PKCS#7 padding, 80 bytes of ciphertext means 64 to 79 bytes of plaintext and 1,328 means 1,312 to 1,327; that bound does not hold if a different mode was used.

Terminal:

```
U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46zgKlIi8aaqY5gpJPP
EzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4
```

SalPhaseIon short (the two base64 halves inside the SalPhaseIon text joined, 64 + 64 characters):

```
U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9zQvX0t8v3jPB4okps
pxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ
```

Cosmic Duality:

```
U2FsdGVkX18tP2/gbclQ5tNZuD4shoV3axuUd8J8aycGCAMoYfhZK0JecHTDpTFedGJh4SJIP66qRtXv
o7PTpvsIjwO8prLiC/sNHthxiGMuqIrKoO224rOisFJZgARic7PaJPne4nab8XCFuV3NbfxGX2BUjNke
f5hg7nsoadZx08dNyU2b6eiciWiUvu7DSATSFO7IFBiAMz7dDqIETKuGlTAP4EmMQUZrQNtfbJsURATW
6V5VSbtZB5RFk0O+IymhstzrQHsU0Bugjv2nndmOEhCxGi/lqK2rLNdOOLutYGnA6RDDbFJUattggELh
2SZx+SBpCdbSGjxOap27l9FOyl02r0HU6UxFdcsbfZ1utTqVEyNs91emQxtpgt+6BPZisil74Jv4Emrp
RDC3ufnkmWwR8NfqVPIKhUiGDu5QflYjczT6DrA9vLQZu3kok+/ZurtRYnqqsj49UhwEF9GfUfl7uQYm
0UunatW43C3Z1tyFRGAzAHQUFS6jRCd+vZGyoTlOsThjXDDCSAwoX2M+yM+oaEQoVvDwVkIqRhfDNuBm
Efi+HpXuJLPBS1PbUjrgoG/Uv7o8IeyST4HBv8+5KLx7IKQS8f1kPZ2YUME+8XJx0caFYs+JS2Jdm0oj
Jm3JJEcYXdKEzOQvRzi4k+6dNlJ05TRZNTJvn0fPG5cM80aQb/ckUHsLsw9a4WzhHsrzBQRTIhog9sTm
+k+LkXzIJiFfSzRgf250pbviFGoQaIFl1CTQPT2w29DLP9006bSiliywwnxXOor03Hn+7MJL27YxeaGQ
n0sFGgP5X0X4jm3vEBkWvtF4PZl0bXWZLvVL/zTn87+2Zi/u7LA6y6b2yt7YVMkpheeOL0japXaiAf3b
SPeUPGz/eu8ZX/NnO3259hG1XwoEVcGdDBV0Nh0A4/phPCR0x5BG04U0OeWAT/5Udc/gGM0TT2FrEzs/
AJKtmsnj31OSsqWb9wD+CoduYY2JrkzJYihE3ZcgcvqqffZXqxQkaI/83ro6JZ4Pubml0PUnAnkdmnBC
pbClbZMzmo3ELZ0EQwsvkJFDMQmiRhda4nBooUW7zXOIb7WxbE9THrt3cdZP5uAgVfgguUNE4fZMN8AT
EDhdSsLklJe2GvihKuZVA6uuSkWAsK6uMGo76xpPwYs3eUdLjtANS83a6/F/fhkX1GXs7zbQjh+Inzk8
jhEdEogl9jPs/oDjKjbkUpFlsCWwAZGoeKlmX7c4OGuD5c+FEH+2nYHvYl8y1E/K5SDt9Uocio8XuxbD
ZOzhw7LMSGkD1MZxpDzsCZY1emkSNd88NFj+9U8VssIDDVMYwKMsHKfjc0x5OlzQ1f6ST0xCkwydDHHG
RKKxFC4y6H6fV9sgf9OPK/65z94Rx72+mfvTyizShjxYSRplsH9otU4parl8roD0KsVTfXZoYrYXzK6c
XBn1BO/OEqWlu++Dd9MiGaUGKd22fXERqNWoRAKlNn2b6EehD2D8WaAoliPURjkB0Lb/FpP9unI93Twg
6NxBXAj734nctukRb3kE08RydJV70eJsvEftF5hbED4HacGx9pzisaSz6t9AKiuSoF6uoCtlTIYatyfZ
kQA4wg50hAJqTynOQ09ArRHEchtB/7uvWZSBGJ7+zlzRGKx99P3oDZD+Y5D8bmUs3PV6FnAp+IRSlnsQ
6hChkwBoQUcngcfGSkBRvmGjsGercCetRRwBOfh9fbX2ruw4mzRYrGnz9eBtepkJXDRjD6yvhNfQMCSk
m6l9zMWxKvFbv5g2ae2SLrEt/x3MP2/G
```

## 6. The SalPhaseIon text (side page, textarea 1)

### 6.1 Layout [V]

On the page every character is followed by one space (1,074 single spaces, no other whitespace). With the spaces removed it is 1075 characters:

```
dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbf
fgigbeeeabeabbabbababbaaaababbbabaaabbbaabaabbabaababbbbaaaabbbaabbabbbabababbab
bababbabbaaabbabaababbbaabbabbbabaafaedggeedfcbdabhhggcadcfeddgfdgbgigaaedggiafa
ecghggcdaihehahbahigceifgbfgefgaifabifagaegeacgbbeagfggeeggafbacgfcdbeiffaafcida
hgdeefghhcggaegdebhhegeghcegadfbdiagefcicggifdcgaaggfbigaicfbhecaecbceiaicebgbgi
ecdeggfgegaedggfiiciiififhggcgfgdcdggefcbeeigefibgibggghhfbcgifdehedfdagicdbhicg
aiedaehahghhcihdghfhbiicecbiichihiiigiddgehhdfdchcbafgfbhaheagegecafehgcfggggcag
fhhghbaihidiehhfdeggdgcihggggghadahigigbgecgedfcdggaccdehiicigfbffhggaeidbbeibbe
iifdgfdhieeeieeecifdgdahdiggfhegfiaffiggbcbcehceabfbedbiibfbfdedeehgigfaaiggagbe
iichiedifbehgbccahhbiibibbibdcbahaidhfahiihiczagdafaoaheiecggchgicbbhcgbehcfcoab
icfdhhcdbbcagbdaiobbgbeadeddezcfobfdhgdobdgooiigdocdaoofidhzshabefourfirsthintis
yourlastcommandU2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9za
bbaabababbabbbaabbbabaaabbaabababbbaabaQvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejU
qTvdWOX6nQjSpepXwGuN/jJshabefanstoo
```

Contiguous blocks by alphabet [V; the cut points are where the alphabet changes, the labels are only names]:

| span | length | alphabet | content or decode (section 6.2) |
|---|---:|---|---|
| [0,91) | 91 | a..i | dbbi block |
| [91,195) | 104 | a, b | `matrixsumlist` |
| [195,765) | 570 | a..i | faed block |
| [765,766) | 1 | z |  |
| [766,829) | 63 | a..i, o | `lastwordsbeforearchichoice` |
| [829,830) | 1 | z |  |
| [830,859) | 29 | a..i, o | `thispassword` |
| [859,860) | 1 | z |  |
| [860,895) | 35 | text | `shabefourfirsthintisyourlastcommand` |
| [895,959) | 64 | base64 | first half of a container |
| [959,999) | 40 | a, b | `enter` |
| [999,1063) | 64 | base64 | second half of the same container |
| [1063,1075) | 12 | text | `shabefanstoo` |

### 6.2 Decodes that reproduce exactly [V]

- Runs of only `a` and `b`, with a = 0 and b = 1, 8 bits per character: [91,195) gives `matrixsumlist`, [959,999) gives `enter`.
- Blocks in `a`..`i` plus `o`, reading a..i as digits 1..9 and o as 0, taking the digit string as one decimal integer, converting it to hexadecimal and reading the bytes as ASCII: [766,829) gives `lastwordsbeforearchichoice`, [830,859) gives `thispassword`.
- The two base64 halves joined form the SalPhaseIon short container (section 5).

```python
def ab(s): return bytes(int(s[i:i+8].replace('a','0').replace('b','1'), 2) for i in range(0, len(s), 8))
def ai(s):
    n = int(''.join('0' if c == 'o' else str(ord(c) - 96) for c in s)); h = format(n, 'x')
    return bytes.fromhex(h.zfill(len(h) + len(h) % 2))
```

### 6.3 Readings of the rest [R]

- `shabef...` as `sha256` (letters as numbers, b = 2, e = 5, f = 6), so the two plain-text pieces read "sha256 our first hint is your last command" and "sha256 the answer too". Under this reading `ans` is "answer". The creator's first message in the chat that contained a hint (#225) was a bare sha256 hash, followed by "just try hit your options against that hash" (#226).
- The 91 letters before the first a/b run (`dbbi...`) parse against the poster's colour cells: walk positions 1, 2, 3, ...; at non-prime positions take one letter as filler, at prime positions take the next colour of the poster's spiral colour sequence with the off-white cell spliced in as a 25th symbol (`BBBBYBBBYYBBBBYBBYYBFYYBY`), taking 1 letter for blue (and for the off-white cell) or 2 for yellow. The 91 letters are used up exactly at position 83, every prime-position chunk starts with `b`, and every yellow chunk is exactly `be` [V]. Under this reading the creator's phrase `yellowblueprimes` (see 7.1) names this block. Whether this fit is intended, and what the filler letters mean, is open. Measured facts about the parse:
  - The 23 prime-position chunks ("hosts") are 15 `b` and 8 `be`. Counting `b` and `be` greedily in the raw text instead gives 15 and 10: the walk and the raw count differ at four places (a blue host followed by a filler `e`, and two filler `b`). dbbi holds 25 letters `b` in all, the same as the poster's 25 coloured cells (15 blue, 9 yellow, 1 off-white), of which the walk uses 23 [V].
  - Writing the 23 hosts as bits (blue = 1, yellow = 0) gives `11110111001111011001100`. The URL's 24 low bits, one per character of `gsmg.io/theseedisplanted`, are `111101110011110110010010`; inserting a 1 at position 21 and taking the first 23 bits reproduces the host string exactly, with `10` unused [V]. This is the same splice as treating the off-white cell as blue, written as a bit operation; whether it means anything is a reading.
  - Continuing the walk past position 83 into the a/b block: positions 84 to 88 take one character each, position 89 (the 24th colour, blue) lands on `b`, and position 97 (the 25th colour, yellow, needs `be`) lands on `aa` and fails [V].
  - The 60 filler letters, in order, are `difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea` [V]. Letter counts a3 b2 c8 d4 e10 f10 g10 h8 i5; faed's letter frequencies predict them about as well as uniform does (G-test against faed's distribution p = 0.26, against uniform p = 0.11, likelihood ratio 1.59) [T, measured]. Their two `b` split them 19 | 16 | 23; 6 of the 1,770 placements of two `b` among 60 give that set of lengths, and the triple was noticed after the fact [V for the count].
  - Controls [T, measured by the previous team]: 200,000 letter-frequency-preserving shuffles of dbbi, none parsed (91 of 91 consumed with 23 of 23 hosts correct); 200,000 random 25-colour programs of the same composition, none parsed; over all 490,314 ways to choose 8 yellows among 23 hosts, exactly 1 parses, the poster's first 23 colours with the off-white cell as blue [V, exhaustive]. With the off-white cell as yellow the walk needs 92 characters; with it dropped the parse fails. The acceptance rule was written after the fit was seen, so the shuffle nulls are the evidence, not the rule.
- The 570-letter block (`faed...`) is unexplained. Measured facts:
  - Letter counts a54 b49 c52 d49 e69 f57 g107 h58 i75: not uniform (chi-square 43.7 on 8 degrees of freedom, p = 6.4e-7) [T, measured]; `g` is the most common letter. Digrams independent (P = 0.18); no period from 2 to 100 (P = 0.71); homogeneous across 19 blocks of 30 once the last 32 letters are removed (P = 0.45); entropy 3.120 of 3.170 bits [T, measured].
  - The last 32 letters, `bccahhbiibibbibdcbahaidhfahiihic`, contain no `e` and no `g` [V]. That is the longest suffix free of any pair of letters; after paying for the choice among 36 pairs its probability under faed's own frequencies is 0.0201, and a change-point test at position 538 gives P = 0.0040, while a BIC comparison does not favour splitting the block [T, measured]. Of the 107 `g`, 24 sit at 1-based prime positions against 19.5 expected (hypergeometric P = 0.135) [V].
  - A full-period Bifid decryption (period 570) with the 5x5 square `dbifhcegaklmnopqrstuvwxyz` (the nine dbbi letters in order of first appearance, then `k`..`z`) starts `btcseedd`; the output's sha256 is `15d62c8228c1a30f3f6280fcdce2251fe616135e9de291b0c7b8a792dd8d0507` [V]. Calibration [V]: of the 362,880 orderings of those nine letters in the first nine cells, 8 give `btcseed`, all continuing `btcseedd`; given that the block starts `faed`, 5 of the 6,561 possible next four letters would also give `btcseed` (p = 7.6e-04), so `btcseed` is not forced by the block but is not a one-in-six-thousand accident either. Only period 570 yields `btcseed`; shorter periods give 16 periods starting `btc`, a count driven by the fixed prefix (prefix-kept shuffles average 14.3, and 34% reach 16) [T, measured]. Even output positions use only the letters b, c, d, e. Nothing after `btcseed` is readable.
  - Reading the whole block as one decimal integer with a = 1 .. i = 9 (the section 6.2 decode) gives a 237-byte number whose first bytes are `1bd5951d` and last bytes `c7bbc075`, 78 of 237 bytes printable [V]. Because 10^32 is divisible by 2^32 and the last 32 letters hold no `g` or `e`, those last four bytes are the same for every choice of which `g` (or which `e`) is read as a zero: `c7bbc075` with a = 1, `009f4eae` with a = 0; three of the four are outside printable ASCII either way [V]. So no zero-mask on `g` or `e` can make the whole-block decode printable text, however many masks there are. This closes only that case: it says nothing about binary output, about deleting letters rather than zeroing them, about zeros on letters that do occur in the last 32, about reordering, or about any other decode.
  - Searches inside the last 32 positions [V]: zeroing a single position, only position 557 (1-based) makes the last four bytes printable (`yI u`); of the 41,448 ways to zero 1 to 4 positions, exactly one gives four lowercase letters, positions 551, 557, 561, 563 (`szqu`). Prefix lengths between 450 and 570 whose top byte is a lowercase letter: 455, 467, 508, 520, 561. These are search findings, not checksums.
- `matrixsumlist`, `enter`, `lastwordsbeforearchichoice` and `thispassword` read as a recipe for a password, where the first and third name operations whose inputs are not on the page. This is the main open question as the previous team saw it.

## 7. Creator material outside the pages [V that the creator posted these]

The full export is in Appendix A. Some items that decode:

### 7.1 Message #8446 (2023-02-23)

161 groups of 8 bits. Reversing the whole bit string and reading 8 bits per character gives:

```
yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyangwewontgiveawaythep
assworditsinfrontofyoureyesbutyourenotseeingitverylaststepisatruegiveawaypromise
d
```

### 7.2 Other items solvers treat as important [R for the weighting]

- #881 (2019): a "tiny hint" would come at the start of 2020 and "will be the final hint"; the key can be retrieved without it.
- #1710 (2020-01-14): the Roses poem. #4096 and #4102 point back to it ("This one", "answer is there").
- #53335 to #53342 (2025-12-31): five messages of 1 to 5 dots, then a binary message reading `Happy new year! Make the best of everything. Oh, and here's a "tiny hint" <3.`
- #8310 to #8315: a solver posted the cover of the Time-Life book *Mysteries of the Unknown: Cosmic Duality*; the creator replied ".... That is very specific" and "If the puzzle is solved you'll see how scary specific that is".
- #7914, #8000: "there is another door". #9607: asked whether another URL must be found, "No need. You have all the info."
- #4624: asked whether the prize is one key, "a private key".
- #5966: "You are at the prime part already???"

## 8. What the previous team tried [T]

Everything below produced nothing. It is listed so you know what was looked at, not to steer you away from it. Any of it may have failed because of a bug, a wrong spelling, a wrong encoding or a wrong assumption about how the password is formed. Reported scales are the team's own.

- **Convention assumed in almost all tests:** each locked container opened with the section 4.1 convention (sha256-hex password, EVP SHA-256 or MD5, AES-256-CBC), plus double-hash and raw-digest variants. Smaller runs tried 14 other ciphers and PBKDF2. If the locked containers use a different scheme, nearly all of the work below says nothing.
- **Wordlists and corpus:** about 551 million combinations of words and phrases from the puzzle texts and related sources against the containers.
- **The poster as numbers ("matrix sum list"):** about 1,550 lists of row, column, diagonal, block, prime-index and spiral sums under 17 cell encodings, as digit strings and letters, alone and crossed with "last words" candidates (about 1.24 billion decrypts).
- **"Last words before archi choice":** last words before choice points in the Architect text, the film scenes, the puzzle texts, by position windows (hundreds of thousands of candidates).
- **dbbi and faed as payload:** dbbi with `b` treated as a zero digit (about 4 billion tests); faed under many substitutions, transpositions, Bifid, Hill and digraphic models.
- **Riddle-style answers:** about 2,500 hand-picked one-line answers for the labels, tested alone and in pairs.
- **The poster and pages as hidden-data carriers:** pixel and LSB checks, QR at codeword level, rebus tiles, the rabbit drawing.
- **Other single ideas:** the song lyrics, the 23/16/7 numbers of the Architect text, the New Year dots, the Cosmic Duality book text, "the seed of the opposite", Jacque Fresco's book titles, the genesis block code, Matrix film lines (including Neo's screen lines and `theseedisplanted` as a "last command").
- **Hidden-zero readings of dbbi and faed:** the filler letters and faed's tail with every letter as the hidden zero over every subset of its occurrences (3,644 choices for the filler letters) plus 144 structured zeroings, output as integer bytes and hex, forward and reversed, raw and as sha256-hex, EVP SHA-256 and MD5, against the three containers: about 16.8 million decryptions with a planted control that fired. dbbi with `b` as the zero over all 2^25 subsets: about 4 billion decryptions. An exhaustive search for which occurrences of each letter are zeros, requiring printable text after the whole-block decode, recovered both planted control blocks and found no solution for dbbi, faed, faed[0:538], faed's tail or dbbi + faed, forward and reversed. Not tested: deletion rather than zeroing; any decode other than whole-block decimal to bytes.
- **Film lines, with controls:** Neo's screen lines (`wakeupneo`, `thematrixhasyou`, `followthewhiterabbit`, `knockknockneo` in 596 spellings and joins), 14,328 decrypts against the three containers under sha256-hex, double sha256 and raw-digest passwords with EVP SHA-256 and MD5: 61 valid paddings against about 56 expected by chance, all one byte, planted control fired, nothing readable; also tried as private keys, no hit. `theseedisplanted` in 83 forms: 2,016 decrypts, 6 valid paddings against about 8 expected, control fired, no hit.
- **Whole-run totals reported:** over 34 billion decrypt tests and 195 million private-key scalars checked against the address.

### 8.1 Claims by other solvers that were checked in October 2026

Other people and other AI systems have published readings of the same material. These were checked against the files in this file; the checks are stated so that you do not have to redo them, not as a verdict on the ideas.

- "The Bifid square is forced to give `btcseed`": not forced; see the calibration in 6.3 (5 of 6,561 continuations, 8 of 362,880 orderings).
- "dbbi holds 15 `b` and 10 `be`": that is the greedy raw count; the prime walk has 15 `b` hosts and 8 `be` hosts (6.3).
- "Weighting the poster's colours gives 255 and 161": 255 and 161 need different values for yellow; of 5,408 small weightings of the five cell colours, 66 hit some number that appears in the puzzle and 5 give 161, so this is numerology unless a weighting is given in advance [T, measured]. The off-white cell is `#FEFEFE` (254), not 255 [V].
- The password `matrixsumlistenterlastwordsbeforearchichoicethispasswordmatrixsumlist` with EVP-MD5 on the SalPhaseIon short container passes the padding check with a one-byte pad, giving 79 bytes of which 30 are printable, sha256 `1449a2178eea7c0e3fabac8c1ad2afa294be4fc1800c594a025a056e88c626bf` [V]. A random wrong key passes the padding check about 1 time in 256, and the output is not text; the solvers who posted it in the group are reported to have retracted it in messages #76033 and #76034, which are after the end of the export in this file.
- The arithmetic result on faed's last four bytes (6.3) was first stated by an outside AI system and reproduced here.

## 9. Open questions, as plainly as possible

- What do `matrixsumlist` and `lastwordsbeforearchichoice` operate on, and what do they produce?
- What is "our first hint", and what is "your last command"?
- What roles do `enter`, `thispassword` and "sha256 the answer too" play, and which container does each step open?
- Are the three locked containers all needed, and in what order? Does one hold the key?
- Is the same encryption convention used for the locked containers?
- Does anything in the material not yet decoded (the faed block, the dbbi filler letters, the New Year dots, the Cosmic Duality title) carry an input?
- If faed or the filler letters hide a value, is it reached by zeroing letters, deleting them, or something else? Deletion has not been tried; the whole-block zeroing of `g` or `e` cannot give printable text (6.3).

## Appendix A. The creator's messages (full export)

Verbatim from the Telegram Desktop export of the solvers' group, the creator's account only, with reply headers. No characters were changed.

```
Chat          : GSMG Puzzle Solvers (private_supergroup, id 1166734859)
Account       : Jrk Bgrt (user9815232)
Source        : result.json (Telegram Desktop export)
Chat messages : 62105 total
Extracted     : 492 text messages
Date range    : 2019-04-20T12:18:49 .. 2026-09-01T11:41:20
====================================================================================================

[#74] 2019-04-20 12:18:49
Ok.. somebody has cracked the first code.
----------------------------------------------------------------------------------------------------
[#75] 2019-04-20 12:19:00
that was way faster than expected.
----------------------------------------------------------------------------------------------------
[#77] 2019-04-20 12:21:57
(edited 2025-05-26 18:52:52 | reactions: 👍 x1)
The first part. Maybe the puzzle has multiple stages 😉.
----------------------------------------------------------------------------------------------------
[#79] 2019-04-20 12:22:36
It is.
----------------------------------------------------------------------------------------------------
[#87] 2019-04-20 12:41:14
It's a way to protect websites against cross site request forgery but the loadbalancer is a bitch on multiple tries apparently.
----------------------------------------------------------------------------------------------------
[#212] 2019-04-22 10:28:08
(edited 2019-04-22 10:28:11)
wrong chat RKT 😊
----------------------------------------------------------------------------------------------------
[#216] 2019-04-22 10:39:49
(edited 2024-06-25 04:47:48)
😂
----------------------------------------------------------------------------------------------------
[#225] 2019-04-22 15:48:52
5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75
----------------------------------------------------------------------------------------------------
[#226] 2019-04-22 15:49:09
just try hit your options against that hash.
----------------------------------------------------------------------------------------------------
[#231] 2019-04-22 17:24:17
Puzzle token issue for stage 1 seems to be resolved.
----------------------------------------------------------------------------------------------------
[#234] 2019-04-22 17:26:42
(edited 2026-01-03 18:42:37 | reactions: 👍 x1)
https://passwordsgenerator.net/sha256-hash-generator/
----------------------------------------------------------------------------------------------------
[#236] 2019-04-22 17:26:51
or just get yourself a python script
----------------------------------------------------------------------------------------------------
[#239] 2019-04-22 17:28:13
a sticker
----------------------------------------------------------------------------------------------------
[#257] 2019-04-22 18:29:02
(edited 2025-04-30 18:44:18 | reactions: 👍 x1)
A hash which we provided as the website was giving a lot of token errors. With this hash the puzzlers can try their passwords instead of firing them at the website.
----------------------------------------------------------------------------------------------------
[#325] 2019-04-23 14:57:51
(edited 2025-04-30 18:46:20 | reactions: 😁 x1)
Ewout managed to crack the april 1st puzzle. He was the first to solve it.
----------------------------------------------------------------------------------------------------
[#518] 2019-04-27 11:46:58
hahahaha :D
----------------------------------------------------------------------------------------------------
[#519] 2019-04-27 11:47:07
back to the pile!
----------------------------------------------------------------------------------------------------
[#550] 2019-04-29 18:35:29
(edited 2025-04-30 18:50:04 | reactions: 👍 x1)
I personally don't mind you talkinig in another language in  this chat tbh although I do prefer english to be the standard language as I assume most of us will be able to follow the conversations. The main chat of GSMG is english only.
----------------------------------------------------------------------------------------------------
[#660] 2019-05-08 09:20:21
Apparently somebody managed to get into Phase 3 🧐
----------------------------------------------------------------------------------------------------
[#663] 2019-05-08 09:34:39
Nobody knows
----------------------------------------------------------------------------------------------------
[#850] 2019-05-14 10:49:49
  -> replying to #848 0xColombo (user274980096): Cikada3301 its fake too?)))
👌
----------------------------------------------------------------------------------------------------
[#851] 2019-05-14 10:51:40
(edited 2025-04-30 18:51:31 | reactions: 😢 x1)
  -> replying to #849 (not in export)
Quests might* be scams. We didn't promote this puzzle nor is it unsolvalble. Please enjoy the puzzle or continue your journey.
----------------------------------------------------------------------------------------------------
[#855] 2019-05-14 10:53:59
  -> replying to #853 phacyh (user422483354): @SoWut give me the solution
Sure, once it's solved.
----------------------------------------------------------------------------------------------------
[#859] 2019-05-14 11:01:11
(edited 2025-04-30 18:52:05 | reactions: 🔥 x1)
  -> replying to #857 unknown (user750026879): if prize will be halfed each time.. not sure about interest will continue long time..
I suppose the btc price will be above 10k at the next halving.
----------------------------------------------------------------------------------------------------
[#866] 2019-05-17 18:39:21
(edited 2025-04-30 18:52:47 | reactions: ❤ x2)
Dear all, somebody pointed out that there might be a mistake in phase III and that is correct unfortunately. The mistake makes it nearly impossible to solve unless you'd know where to add 1 extra character between the 3 answers. My sincerest apologies for this, I'll fix this a soon as I've found a decent spot to do so as I'm on holiday atm. Again, 1000 times sorry, I'm aware I might have wasted a lot of time for some :-(...
----------------------------------------------------------------------------------------------------
[#867] 2019-05-17 18:43:46
(edited 2025-04-30 18:53:20 | reactions: 👍 x1)
Here's the hint in order to bypass the mistake:

giveit = givetit
----------------------------------------------------------------------------------------------------
[#869] 2019-05-17 20:04:04
(edited 2026-09-04 16:16:25 | reactions: ❤ x1)
Correct.
----------------------------------------------------------------------------------------------------
[#871] 2019-05-17 20:15:22
(edited 2025-04-30 18:54:37 | reactions: 👍 x1)
For those feeling bad about having wasted time on my typo. I might feel even worse as I've tested the entire puzzle 3 times with the same string which had the typo in it 😒. I'll kill some braincells tonight with tasteless alcohol in order to forget this blunder.
----------------------------------------------------------------------------------------------------
[#874] 2019-05-17 22:30:08
The issue is within the 3th phase. Not in going from 2 to 3.
----------------------------------------------------------------------------------------------------
[#875] 2019-05-17 22:30:34
(edited 2025-04-30 18:55:15 | reactions: 👍 x1)
Once you have to work with give(t)it you'll know.
----------------------------------------------------------------------------------------------------
[#879] 2019-05-18 12:26:26
(edited 2025-04-30 18:57:00 | reactions: 😁 x1)
So, after yesterday's 'hint' a team of puzzlers has made an unbelievable amount of progress in just one day... The progress they made was unforseen as we expected it to take at least a !month! to pass those parts of the puzzle. Hat off for those that managed to puzzle their way through all the ciphers and riddles in this extraordinary pace. We're really impressed by that, actually, we stand in awe for you. Congrats.

To those not having reached Phase III yet, no worries besides a bit of extra pressure. The "last" part of the puzzle will ensure that there's quite some time for you guys to catch up to them... although given their obvious skill this might be solved quicker than expected aswell.. time will tell. Good luck!
----------------------------------------------------------------------------------------------------
[#881] 2019-05-18 12:31:02
(edited 2026-01-03 18:38:08 | reactions: 🤔 x1)
In case the private key hasn't been found in 2019 we'll release a tiny hint at the start of 2020, that will be the final hint. Can the private key be retrieved without that hint? Yes.
----------------------------------------------------------------------------------------------------
[#886] 2019-05-18 12:49:27
Nope
----------------------------------------------------------------------------------------------------
[#887] 2019-05-18 12:50:17
Part III consist out of a few stages. The last few stages are, how shall I say it, not really easy to solve for most.
----------------------------------------------------------------------------------------------------
[#896] 2019-05-18 13:10:46
No, they reaced out to me on tg and send me proof of them passing the stages.
----------------------------------------------------------------------------------------------------
[#898] 2019-05-18 13:13:29
No hints after stage 2 (except the 't' to fix my stupid mistake)
----------------------------------------------------------------------------------------------------
[#950] 2019-05-26 20:25:10
  -> replying to #949 (not in export)
Not completely, voice recognition might even work to pass although I'd copy past the answer as it's faster ;-).
----------------------------------------------------------------------------------------------------
[#952] 2019-05-26 23:20:49
(edited 2025-04-30 19:00:42 | reactions: 🤔 x1)
Ok you found a song. Do have a clue on how to proceed on the webpage?
----------------------------------------------------------------------------------------------------
[#961] 2019-05-28 12:45:40
  -> replying to #958 unknown (user815412073): How many phase in this puzlle?
Nobody knows.
----------------------------------------------------------------------------------------------------
[#978] 2019-05-31 11:02:28
Now we need a bot here too
----------------------------------------------------------------------------------------------------
[#984] 2019-05-31 11:20:06
[sticker 😂 sticker.webp]
----------------------------------------------------------------------------------------------------
[#988] 2019-05-31 11:27:49
  -> replying to #986 Coinbaas (user166247483): @MissRose_bot this is a nice bot for the chat 👌
shitcoin
----------------------------------------------------------------------------------------------------
[#989] 2019-05-31 11:27:53
😉
----------------------------------------------------------------------------------------------------
[#990] 2019-05-31 11:28:01
  -> replying to #987 Chris (user507197982): Hi there any news on puzzle?😄
Well.... yes
----------------------------------------------------------------------------------------------------
[#991] 2019-05-31 11:28:28
Apparently folks found a new piece.
----------------------------------------------------------------------------------------------------
[#994] 2019-05-31 11:29:13
Almost banned for spam 😋
----------------------------------------------------------------------------------------------------
[#999] 2019-05-31 11:32:29
/daysandbox_set safe_hours=720
----------------------------------------------------------------------------------------------------
[#1210] 2019-06-27 17:38:51
(edited 2025-05-26 19:22:42 | reactions: 🤔 x1)
🌱
----------------------------------------------------------------------------------------------------
[#1211] 2019-06-27 17:39:32
(edited 2025-05-26 19:22:47 | reactions: 🤔 x1)
🛣
----------------------------------------------------------------------------------------------------
[#1416] 2019-08-10 12:50:10
You'll only know when you've solved that part.
----------------------------------------------------------------------------------------------------
[#1448] 2019-09-04 03:58:16
Still no hints ;-)
----------------------------------------------------------------------------------------------------
[#1461] 2019-09-22 18:55:01
(edited 2024-02-26 09:37:49)
  -> replying to #1460 unknown (user884485205): Hey, I have a technical question. Would someone please guide me? I just got to phase 2 with aes1 and it says: "Ciphered with aes-256-cbc /w base64 sha-256(pass...
Found it by now?
----------------------------------------------------------------------------------------------------
[#1465] 2019-09-22 19:00:48
7 parts right?
----------------------------------------------------------------------------------------------------
[#1487] 2019-09-26 11:35:24
(edited 2025-04-30 19:07:20 | reactions: 🤔 x1)
There may indeed a piece be found outside the main puzzle.
----------------------------------------------------------------------------------------------------
[#1537] 2019-10-13 14:38:53
(edited 2025-04-30 19:07:53 | reactions: 🤔 x2)
Gsmg.io/puzzle
----------------------------------------------------------------------------------------------------
[#1587] 2019-10-31 21:53:04
Sure, what's the hint?
----------------------------------------------------------------------------------------------------
[#1602] 2019-12-03 12:55:55
(edited 2025-04-30 19:08:43 | reactions: 👍 x1)
giveit = givetit
----------------------------------------------------------------------------------------------------
[#1638] 2019-12-31 05:30:23
  -> replying to #1632 silver_anth (user432257224): @SoWut any set time for the hint to drop? I have less than two hours till 2020 😎
Hahaha, you're on it. Not an exact time, but it will be posted in this channel. It's at the start of 2020 indeed, way before the halving.
----------------------------------------------------------------------------------------------------
[#1639] 2019-12-31 05:33:29
(edited 2025-04-30 19:09:33 | reactions: ❤ x1)
To all you peepz in advance: have a blast in the last part of 2019 and have an even better 2020. Best wishes to you all and good luck with the next puzzle piece(s) in case you manage to find them 😉!
----------------------------------------------------------------------------------------------------
[#1647] 2020-01-04 20:01:00
(edited 2025-04-30 19:10:58 | reactions: 🤔 x1)
[photo 340x191]
----------------------------------------------------------------------------------------------------
[#1648] 2020-01-04 20:01:19
(edited 2025-04-30 19:09:50 | reactions: 🤔 x1)
Anybody hungry?
----------------------------------------------------------------------------------------------------
[#1651] 2020-01-04 20:01:54
(edited 2025-04-30 19:11:04 | reactions: 👍 x1)
No, it's a dessert
----------------------------------------------------------------------------------------------------
[#1659] 2020-01-04 20:06:01
(edited 2025-04-30 19:11:12 | reactions: 😢 x1)
Note: I might be in a trolling mood.
----------------------------------------------------------------------------------------------------
[#1680] 2020-01-12 15:52:32
  -> replying to #1659 Jrk Bgrt (user9815232) <-- also JRK: Note: I might be in a trolling mood.
👆
----------------------------------------------------------------------------------------------------
[#1703] 2020-01-13 11:40:54
(edited 2025-04-30 19:12:11 | reactions: 👍 x1)
Hint to be expected within a few days. Note: not trolling with scripted cake this time.
----------------------------------------------------------------------------------------------------
[#1710] 2020-01-14 05:38:06
(edited 2024-04-24 02:58:18 | reactions: ❤ x4)
Roses are White but often Red.
Yellow has a number and so does Blue.
Go back to the first puzzle piece without further ado.

It might have shown you only one door, beware that the rabbits nest may contain a whole lot more.

Hush hush.
----------------------------------------------------------------------------------------------------
[#1711] 2020-01-14 05:38:49
(edited 2025-04-30 19:12:29 | reactions: 😢 x1)
Good luck 👍
----------------------------------------------------------------------------------------------------
[#1726] 2020-01-27 10:21:35
  -> replying to #1724 Mr Bloggs (user969034109): Besides the "givetit" mistake, are there any other confirmed spelling/gramatical errors? Phase 3.2 is what I'm talking about..
Might have been fixed fyi 👆
----------------------------------------------------------------------------------------------------
[#1729] 2020-01-27 11:00:04
Would be nice, not required
----------------------------------------------------------------------------------------------------
[#1743] 2020-02-20 10:31:58
(edited 2025-09-10 19:45:46 | reactions: ❤ x1)
😎
[photo 1280x749]
----------------------------------------------------------------------------------------------------
[#1753] 2020-02-21 08:03:21
I'm not the esthetician when it comes to coding 😉
----------------------------------------------------------------------------------------------------
[#1758] 2020-02-22 10:19:41
👋
----------------------------------------------------------------------------------------------------
[#1775] 2020-02-22 10:32:30
Solutions for the first stages can be found online.
----------------------------------------------------------------------------------------------------
[#1777] 2020-02-22 10:32:52
The quickest brain did it within 2 hours if I remember correctly.
----------------------------------------------------------------------------------------------------
[#1779] 2020-02-22 10:34:10
Don't know
----------------------------------------------------------------------------------------------------
[#1806] 2020-02-22 11:11:52
(edited 2025-08-08 09:12:53 | reactions: ❤ x2)
Typos: Horrible mistakes due to rushed work. I'm 100% to blame for this noobish display of words. No clues to be found in those typos might you wonder 😉.
----------------------------------------------------------------------------------------------------
[#1837] 2020-02-22 15:30:18
Only -41,-17 matters
----------------------------------------------------------------------------------------------------
[#1895] 2020-02-25 07:45:53
(edited 2025-09-26 20:03:01 | reactions: 🤔 x1)
  -> replying to #1888 (not in export)
Not sponsored, just see it as a side quest
----------------------------------------------------------------------------------------------------
[#2002] 2020-02-25 13:04:46
  -> replying to #1987 Matt (user252821338): i think @SoWut admin should take care of you
You are right
----------------------------------------------------------------------------------------------------
[#2011] 2020-02-25 13:07:05
(edited 2020-02-25 13:07:42)
FA please soften the communication. I like enthusiasm, but don't bring down the vibe. A lot of very smart people have been on this puzzle and put in a lot more effort than 1 can do in a month. Some puzzlers amazed me by being so incredibly fast in some stages.
----------------------------------------------------------------------------------------------------
[#2013] 2020-02-25 13:07:19
(edited 2026-01-31 03:51:18)
3.2 is a thing btw
----------------------------------------------------------------------------------------------------
[#2017] 2020-02-25 13:09:10
(edited 2025-01-31 12:32:26 | reactions: ❤‍🔥 x1)
  -> replying to #2016 nieods (user809473266): There's no clear direction on what to do next, and probably invokes time consuming brute force
Or nobody found the direction
----------------------------------------------------------------------------------------------------
[#2020] 2020-02-25 13:09:39
(edited 2025-09-03 09:52:14 | reactions: 😢 x1)
But I should shut up ofcourse 😁
----------------------------------------------------------------------------------------------------
[#2023] 2020-02-25 13:10:30
  -> replying to #2021 unknown (user1084918156): everything is GIVEN
I'd dive in the puzzle from the beginning before making assumptions
----------------------------------------------------------------------------------------------------
[#2024] 2020-02-25 13:11:01
A few guys here cracked phase 2 in 2 days.
----------------------------------------------------------------------------------------------------
[#2026] 2020-02-25 13:15:01
(edited 2025-09-03 09:46:59 | reactions: 🤔 x1)
Don't know but most see 3.2 as the last part.
----------------------------------------------------------------------------------------------------
[#2067] 2020-02-25 13:38:52
(edited 2025-01-31 12:38:08 | reactions: 😁 x1)
  -> replying to #2051 nieods (user809473266): Well denial is the most predictable of all human responses
😂😂😂
----------------------------------------------------------------------------------------------------
[#2070] 2020-02-25 13:40:01
Just spend less time here fishing for clues and solve 🧐
----------------------------------------------------------------------------------------------------
[#2244] 2020-02-27 11:06:27
Nice and silent
----------------------------------------------------------------------------------------------------
[#2245] 2020-02-27 11:06:41
Damn so annoying
----------------------------------------------------------------------------------------------------
[#2247] 2020-02-27 11:07:09
(edited 2025-08-08 09:22:40 | reactions: ❤ x1)
He'll be back
----------------------------------------------------------------------------------------------------
[#2297] 2020-03-16 09:13:31
(edited 2025-09-03 09:42:06 | reactions: 👍 x1)
Yeah we might want to push the English only rule here too ;-)
----------------------------------------------------------------------------------------------------
[#2905] 2020-03-24 20:19:39
(edited 2026-05-27 12:35:31)
  -> replying to #2899 unknown (user750026879): 1. rabbit hole marked (rabbit looking to this point). 2. usual spiral solve showed. 3. rabbit nest is white box at center.
Interesting 😜
----------------------------------------------------------------------------------------------------
[#2910] 2020-03-24 21:02:42
  -> replying to #2906 Lazy Prophet (user952048031): hello! @SoWut Jrk Bgrt... is the complete pk hidden in the final chapter of this beautiful puzzle or the pk is also divided into pieces and will only get the l...
Answering that would be too much of a hint.
----------------------------------------------------------------------------------------------------
[#2918] 2020-03-24 21:22:40
  -> replying to #2911 Detective Froz (user231061724): Some people refer to you saying that you confirmed that the PK is in the last cipher of 3.2 decoded. Can you confirm?
There must at least be something hidden in there.
----------------------------------------------------------------------------------------------------
[#3281] 2020-04-06 08:12:03
No hints 🤓
----------------------------------------------------------------------------------------------------
[#3338] 2020-04-08 14:38:10
Those hints are the last hints. Although I can say that one team managed to find something... something others haven't yet found (unless they didn't tell us).
----------------------------------------------------------------------------------------------------
[#3340] 2020-04-08 15:01:53
That would be another hint.
----------------------------------------------------------------------------------------------------
[#3342] 2020-04-08 15:12:53
there are errors?
----------------------------------------------------------------------------------------------------
[#3345] 2020-04-08 15:16:14
Before you send anything. No hints; errors and typos are mostly not intended 😄
----------------------------------------------------------------------------------------------------
[#3348] 2020-04-08 15:27:23
well, I'll just wait until you guys have progressed to "the next stage or something like that"😁
----------------------------------------------------------------------------------------------------
[#3365] 2020-04-08 16:12:57
  -> replying to #3350 Tracer (user713273879): We should call it the after stage then 😄
the backstage 😎
----------------------------------------------------------------------------------------------------
[#3369] 2020-04-08 16:16:02
obviously a typo
----------------------------------------------------------------------------------------------------
[#3370] 2020-04-08 16:17:30
Rushed work. I take all the blame there is for those 😞. My sincerest apologies.
----------------------------------------------------------------------------------------------------
[#3371] 2020-04-08 16:17:43
Hope it hasn't spoiled the fun so far.
----------------------------------------------------------------------------------------------------
[#3373] 2020-04-08 16:19:06
(edited 2020-04-08 16:19:28)
I can't even write without typo's. The intelligence is an illusion.
----------------------------------------------------------------------------------------------------
[#3375] 2020-04-08 16:19:36
But thanks nevertheless.
----------------------------------------------------------------------------------------------------
[#3384] 2020-04-08 16:27:08
Quite some typos have been changed already. The biggest blunder so far in the mainline of the puzzle was givetit instead of giveit 😩🔨
----------------------------------------------------------------------------------------------------
[#3386] 2020-04-08 16:28:48
What impressed me most so far was that 1 crew even managed to pass it while the typo was unknown.
----------------------------------------------------------------------------------------------------
[#3390] 2020-04-08 16:33:39
(edited 2025-01-31 18:29:34 | reactions: 👍 x2, ❤ x1)
Humph. Hope, it is the quintessential human delusion, simultaneously the source of your greatest strength, and your greatest weakness.
----------------------------------------------------------------------------------------------------
[#3391] 2020-04-08 16:33:48
(not a hint btw, just fooling around)
----------------------------------------------------------------------------------------------------
[#3395] 2020-04-08 16:39:11
  -> replying to #3394 Lazy Prophet (user952048031): and thousands of reasons to proceed....
like 5 thousand milibitcoin...?
----------------------------------------------------------------------------------------------------
[#3404] 2020-04-08 16:51:58
(edited 2025-09-21 15:35:54 | reactions: 🔥 x1)
And Oen
----------------------------------------------------------------------------------------------------
[#3478] 2020-04-11 15:52:20
♟
----------------------------------------------------------------------------------------------------
[#3615] 2020-04-29 13:18:49
  -> replying to #3613 x7x7x7x6 (user633059140): let me guess: because it`s unknown?
👆
----------------------------------------------------------------------------------------------------
[#3860] 2020-05-11 12:42:26
[ANIMATION: giphy.mp4, 2s]
----------------------------------------------------------------------------------------------------
[#3876] 2020-05-11 13:07:48
  -> replying to #3863 Trin (user293334370): So what are you going to do with the 2.5btc after the halving? @SoWut another puzzle? 😁
Invest it in bitconnect.
----------------------------------------------------------------------------------------------------
[#3902] 2020-05-11 15:26:40
  -> replying to #3901 x7x7x7x6 (user633059140): the half of prize went to better half
Well spotted
----------------------------------------------------------------------------------------------------
[#3903] 2020-05-11 15:26:51
Happy halving!
----------------------------------------------------------------------------------------------------
[#3905] 2020-05-11 15:31:00
(edited 2026-02-02 05:54:13)
It'll high likely be worth more than it once the price was 5 btc. Next halving in 209999
----------------------------------------------------------------------------------------------------
[#3923] 2020-05-11 16:31:25
(edited 2024-12-23 04:22:01)
Let's see what bitcoin is worth the next halving and who knows what you'll find after opening the 2nd door. The price is in half, but what does it mean 🤔.
----------------------------------------------------------------------------------------------------
[#4094] 2020-05-20 18:54:11
  -> replying to #4076 Timofey Bondarenko (user1027386051): The January hint is missing on github, isn't it?
It is
----------------------------------------------------------------------------------------------------
[#4096] 2020-05-20 19:36:55
(edited 2025-12-23 14:43:42 | reactions: ❤ x1)
  -> replying to #1710 Jrk Bgrt (user9815232) <-- also JRK: Roses are White but often Red. Yellow has a number and so does Blue. Go back to the first puzzle piece without further ado. It might have shown you only one do...
This one 👆.
----------------------------------------------------------------------------------------------------
[#4102] 2020-05-20 22:40:46
answer is there
----------------------------------------------------------------------------------------------------
[#4105] 2020-05-21 02:12:59
(edited 2025-12-23 16:20:03 | reactions: ❤ x1, 😁 x1)
First or zero
----------------------------------------------------------------------------------------------------
[#4266] 2020-05-23 08:29:12
Thanks @EwoutM, I fell asleep.
----------------------------------------------------------------------------------------------------
[#4272] 2020-05-23 09:40:20
/goodbye off
----------------------------------------------------------------------------------------------------
[#4274] 2020-05-23 09:40:29
/cleanwelcome on
----------------------------------------------------------------------------------------------------
[#4307] 2020-05-23 15:51:51
  -> replying to #3863 Trin (user293334370): So what are you going to do with the 2.5btc after the halving? @SoWut another puzzle? 😁
I have a purpose now. Buy a dosis of super covid-20 for every spammer.
----------------------------------------------------------------------------------------------------
[#4309] 2020-05-23 15:53:42
Perfect
----------------------------------------------------------------------------------------------------
[#4310] 2020-05-23 15:53:55
Make it very contagious please.
----------------------------------------------------------------------------------------------------
[#4314] 2020-05-23 16:01:14
/lock audio bot button command contact document email emojigame forward game invitelink location phone poll rtl sticker url video videonote voice
----------------------------------------------------------------------------------------------------
[#4316] 2020-05-23 16:01:44
(edited 2023-12-18 01:18:09)
😇
----------------------------------------------------------------------------------------------------
[#4363] 2020-05-24 22:17:02
(edited 2026-02-07 19:28:20 | reactions: 🤔 x1)
I think a computer would beat me in the turing test.
----------------------------------------------------------------------------------------------------
[#4548] 2020-06-30 19:29:05
(edited 2024-04-07 19:08:42)
  -> replying to #4545 Zil (user980067088): No, the puzzle begins with a drunk rabit he got himself into a hole he can't get out from :D
👆
----------------------------------------------------------------------------------------------------
[#4589] 2020-08-02 12:54:57
Or the same puzzle, or just not at all 🤷‍♀.
----------------------------------------------------------------------------------------------------
[#4590] 2020-08-02 12:56:20
Really nobody managed to find the extra door, didn't expect that after the earlier pace of cracking things.
----------------------------------------------------------------------------------------------------
[#4597] 2020-08-03 08:46:06
A few here know
----------------------------------------------------------------------------------------------------
[#4603] 2020-08-03 11:17:43
(edited 2025-08-06 00:58:38 | reactions: 🔥 x2)
It's ok, more chance for those that aren't running. We said we'd do this from the start, no need to feel bad about this.
----------------------------------------------------------------------------------------------------
[#4624] 2020-08-09 06:38:27
a private key
----------------------------------------------------------------------------------------------------
[#4647] 2020-08-10 12:50:52
Cracking ethereum requires billions of ether.
----------------------------------------------------------------------------------------------------
[#4688] 2020-08-12 09:10:55
Indeed remarkable with the hints stating the path pretty obvious...
----------------------------------------------------------------------------------------------------
[#4693] 2020-08-12 14:22:59
No hints
----------------------------------------------------------------------------------------------------
[#4694] 2020-08-12 14:23:21
There's 1 club that passed but they are stuck in the next phase.
----------------------------------------------------------------------------------------------------
[#4696] 2020-08-12 15:18:55
Correct
----------------------------------------------------------------------------------------------------
[#4771] 2020-10-01 08:41:56
I've just been notified that number 2 has made it to the next stage.
----------------------------------------------------------------------------------------------------
[#4912] 2020-10-27 04:58:39
(edited 2026-05-04 09:19:05 | reactions: 🤔 x1)
  -> replying to #4901 Zil (user980067088): how come you haven't solved it yet
https://www.blockchain.com/btc/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe price is indeed still there.
----------------------------------------------------------------------------------------------------
[#5069] 2020-11-24 13:02:48
We have our reasons halving the price money at every bitcoin halving event :-).
----------------------------------------------------------------------------------------------------
[#5071] 2020-11-24 14:02:23
Who knows, maybe even in the same block.
----------------------------------------------------------------------------------------------------
[#5251] 2020-12-26 06:54:18
Thanks
----------------------------------------------------------------------------------------------------
[#5365] 2021-01-07 14:57:32
It'll be split on the next halving.
----------------------------------------------------------------------------------------------------
[#5368] 2021-01-07 14:58:45
We mentioned this at the beginning, when the puzzle started.
----------------------------------------------------------------------------------------------------
[#5370] 2021-01-07 14:59:38
  -> replying to #5369 Detective Froz (user231061724): Wow, do you expect the puzzle would not be solved within the next ~3 years?
Depends on the contestants' puzzle skills.
----------------------------------------------------------------------------------------------------
[#5375] 2021-01-07 16:58:17
  -> replying to #5372 unknown (user871228632): Where?
Tg channel
----------------------------------------------------------------------------------------------------
[#5672] 2021-01-18 09:41:23
(edited 2025-09-07 15:16:38 | reactions: 🫡 x1)
  -> replying to #5668 unknown (user689225742): I think he is puzzle creator fake account. Trying to push someone to solve and share the gsmg platform. Just for interaction maybe
I can solemnly promise you I'm not using any other accounts besides my own.
----------------------------------------------------------------------------------------------------
[#5677] 2021-01-19 13:12:59
From now on no more begging for money in exchange for "hints". Doing so results in a ban. Measure in place due to many complaints.
----------------------------------------------------------------------------------------------------
[#5678] 2021-01-19 13:14:14
(edited 2025-12-29 14:19:13)
This puzzle is supposed to be fun ✌️.
----------------------------------------------------------------------------------------------------
[#5684] 2021-01-19 16:39:00
(edited 2025-02-01 20:16:53 | reactions: 🔥 x1)
I'll offer free hints in PM. (After you've paid me 5.1 btc 🤡).
----------------------------------------------------------------------------------------------------
[#5685] 2021-01-19 16:39:13
(edited 2025-09-08 18:38:12 | reactions: ❤ x1)
Good luck again.
----------------------------------------------------------------------------------------------------
[#5717] 2021-01-21 06:35:49
(edited 2025-02-01 20:18:34 | reactions: 😨 x1)
  -> replying to #5715 (not in export)
Not to give any hints but a few might not require the internet anymore.
----------------------------------------------------------------------------------------------------
[#5960] 2021-03-01 06:33:17
  -> replying to #5952 Janusz Baran (user394589394): someone from england or america is here ? this is old talk, now is FORTY but hundred FOUR = 104 is the fefefe square fefefe is 101 010
Ancient spelling 😅. One of the many many typos.
----------------------------------------------------------------------------------------------------
[#5966] 2021-03-01 06:34:42
(edited 2025-09-08 18:33:25 | reactions: 🫡 x1)
You are at the prime part already???
----------------------------------------------------------------------------------------------------
[#5969] 2021-03-01 06:35:15
Oh wait, shouldn't have said that. That might have been a hint 🤔.
----------------------------------------------------------------------------------------------------
[#5982] 2021-03-01 06:38:37
(edited 2025-09-08 18:32:55 | reactions: 😁 x1)
Rumour has it I'm an admin at least.
----------------------------------------------------------------------------------------------------
[#6025] 2021-03-01 06:45:48
[sticker 🤷‍♂️ AnimatedSticker.tgs]
----------------------------------------------------------------------------------------------------
[#6243] 2021-03-05 08:14:28
(edited 2025-07-10 09:18:11)
  -> replying to #6201 Alex (user690769341): Author just wasted a huge amount of time of people
Those not enjoying the puzzle are the ones wasting time I guess 😅?
----------------------------------------------------------------------------------------------------
[#6250] 2021-03-05 08:15:26
(edited 2025-09-08 18:16:30 | reactions: 🤔 x1)
Infrared
----------------------------------------------------------------------------------------------------
[#6252] 2021-03-05 08:15:45
(edited 2025-09-08 18:17:02 | reactions: 🤡 x1)
No hints 🤡
----------------------------------------------------------------------------------------------------
[#6491] 2021-03-14 01:58:08
(edited 2026-07-06 23:27:28)
Fyi. Another person (or team) made it to salph.
----------------------------------------------------------------------------------------------------
[#6495] 2021-03-14 05:25:14
  -> replying to #6493 Zil (user980067088): Salph? You trolling us? :))
Nope
----------------------------------------------------------------------------------------------------
[#6497] 2021-03-14 05:45:01
(edited 2025-06-26 04:42:30 | reactions: ❤ x1, 🤔 x1)
  -> replying to #6496 Zil (user980067088): I always wonder how when you tell us that someone (or a team) has reached a certain step - you don't necessarily know that :) makes me thinkthis information yo...
I don't check the website logs. There aren't any tracking scripts either. People somehow now how to reach me on telegram and PM me, that's how I know :-). Although I can't prove it, we don't monitor the puzzlers progress in any way. I just read the chat and when I notice the address is empty I'll know how they did it. After the first stage was cracked within no-time I was afraid the entire puzzle would have been solved not too long after that. When people progress in salphation it might be cracked pretty soon. Breaking salphation, should be giving the feeling of the phase's name. Won't be easy but I've noticed how clever most of you are so I assume it will be cracked at some point, probably before next halving.
----------------------------------------------------------------------------------------------------
[#6509] 2021-03-14 11:19:29
  -> replying to #6508 unknown (user419791047): So don't you think it's time for a hint on matrixsumlist?
I gave an unforseen hint already 🤷‍♂
----------------------------------------------------------------------------------------------------
[#6514] 2021-03-15 03:16:26
(edited 2025-03-27 05:24:01 | reactions: 🤔 x1)
Hush hush
----------------------------------------------------------------------------------------------------
[#6541] 2021-03-19 07:07:55
If know about 3 people/teams.
----------------------------------------------------------------------------------------------------
[#6543] 2021-03-19 07:19:59
4*
----------------------------------------------------------------------------------------------------
[#6712] 2021-03-22 12:53:39
(edited 2026-05-06 07:46:41)
Nr 5 in salph
----------------------------------------------------------------------------------------------------
[#6767] 2021-03-24 18:19:43
  -> replying to #6766 nieods (user809473266): I’m trying to free your mind, you. But I can only show you the door. You’re the one that has to walk through it. You have to let it all go. Fear, doubt, and di...
🤣
----------------------------------------------------------------------------------------------------
[#6846] 2021-03-27 09:37:10
  -> replying to #6845 Org0 (user340325111): this requires a lot of LSD
Maybe combine it with some psilocybe azurescens and mao inhibitors or go all  the way with some 5-MeO-DMT. 👀
----------------------------------------------------------------------------------------------------
[#6847] 2021-03-27 09:39:51
[ANIMATION: mp4.mp4, 3s]
----------------------------------------------------------------------------------------------------
[#6884] 2021-04-01 02:57:38
(edited 2025-02-02 20:11:21 | reactions: 🤔 x1)
Hint: "another door might be found on {1 },{4} ,{21}"
----------------------------------------------------------------------------------------------------
[#6895] 2021-04-01 04:34:22
  -> replying to #6891 x7x7x7x6 (user633059140): Private key might be found on {30 },{2} ,{77}
Good one V ;-). (Assuming you played cyberpunk).
----------------------------------------------------------------------------------------------------
[#6913] 2021-04-01 09:29:41
(edited 2025-08-09 03:30:56 | reactions: 🔥 x1, 🤔 x1)
R=18
A=1
B=2

Could also be 21 or 1812 bit 🧐. Sometimes I'm glad I don't have to solve this puzzle myself.
----------------------------------------------------------------------------------------------------
[#6944] 2021-04-01 10:06:39
  -> replying to #6943 nieods (user809473266): Probably best to start at the beginning to understand the mindset behind it
👆
----------------------------------------------------------------------------------------------------
[#7028] 2021-04-02 16:18:22
  -> replying to #7025 unknown (user1760549311): My link has been deleted? It was definitely not spam. Rather a personal opinion that can be easily disregarded. Well, no problem at all 👍
I haven't deleted it. Not sure who, but I noticed some more messages are deleted from time to time.
----------------------------------------------------------------------------------------------------
[#7060] 2021-04-03 11:51:32
  -> replying to #7057 Hii (user1465192424): Who is the maker of this puzzle? Present on this telegram channel?
Nobody knows
----------------------------------------------------------------------------------------------------
[#7061] 2021-04-03 11:52:35
I've been pretending to be one of the few creators for a while now.
----------------------------------------------------------------------------------------------------
[#7152] 2021-04-06 10:08:39
Some parts of cicada puzzles are still unsolved. Must be bad design.
----------------------------------------------------------------------------------------------------
[#7153] 2021-04-06 10:09:36
  -> replying to #7142 (not in export)
If it were just about having fun, that'd be great wouldn't it :-).
----------------------------------------------------------------------------------------------------
[#7224] 2021-04-09 15:46:38
  -> replying to #7223 Trin (user293334370): false
✅
----------------------------------------------------------------------------------------------------
[#7244] 2021-04-10 13:49:28
Fyi, another person or team reached salph today.
----------------------------------------------------------------------------------------------------
[#7381] 2021-04-16 07:14:33
Blame noted and accepted
----------------------------------------------------------------------------------------------------
[#7385] 2021-04-16 07:20:09
  -> replying to #7383 Hii (user1465192424): That and without a halfing of the prize xD
Deal, we'll take of 75% instead 😈.
----------------------------------------------------------------------------------------------------
[#7388] 2021-04-16 07:21:12
(edited 2026-07-14 21:53:57)
https://www.bitcoinblockhalf.com/
----------------------------------------------------------------------------------------------------
[#7396] 2021-04-16 07:33:32
  -> replying to #7389 (not in export)
I don't care who shares what indeed, too much of a hassle. As long as people enjoy and that the best puzzler gets the price I'm ok with a lot.
----------------------------------------------------------------------------------------------------
[#7418] 2021-04-16 08:08:24
(edited 2025-01-24 04:09:51)
  -> replying to #7416 RB (user737261554): Just do what is told all the time over and over. Go to the first puzzle piece (image) and hash all the text you see. But mind that the author is a bit picky wh...
Good point
----------------------------------------------------------------------------------------------------
[#7520] 2021-04-18 13:33:41
  -> replying to #7517 Hii (user1465192424): Saber is puzzle creator I suspect
I suspect he isn't
----------------------------------------------------------------------------------------------------
[#7529] 2021-04-18 14:24:13
(edited 2026-07-22 10:09:58 | reactions: ❤ x1)
  -> replying to #7528 unknown (user1783233127): Is this an actual hint we can use please? I’m asking because it was mentioned on April 1st
Do you know what usually happens on the first of april?
----------------------------------------------------------------------------------------------------
[#7830] 2021-08-10 16:51:12
  -> replying to #7826 Detective Froz (user231061724): Hackers would not help here. Puzzle creators do not store the private key online 😉
Technically we do 😁
----------------------------------------------------------------------------------------------------
[#7832] 2021-08-11 06:55:52
(edited 2026-01-06 17:05:22 | reactions: 🤔 x1)
  -> replying to #7831 Detective Froz (user231061724): Do you mean the encrypted private key stored online?
The one to be found by solving the puzzle yes
----------------------------------------------------------------------------------------------------
[#7834] 2021-08-11 07:07:15
(edited 2026-01-06 17:06:38 | reactions: 🫡 x1)
And the solver will find a way to 'decrypt' it.
----------------------------------------------------------------------------------------------------
[#7886] 2021-09-23 19:38:41
(edited 2026-01-15 19:42:46)
https://blockchair.com/tools/halving-countdown
----------------------------------------------------------------------------------------------------
[#7889] 2021-09-24 05:37:18
  -> replying to #7888 SlobaDoba (user1483942636): Is that a hint? 😂
This was alcohol talking last night. The topic puzzle came up, and couldn't resist posting it 😅.
----------------------------------------------------------------------------------------------------
[#7891] 2021-09-24 06:01:15
That's not mine
----------------------------------------------------------------------------------------------------
[#7906] 2021-10-31 07:08:49
(edited 2026-01-03 11:59:49 | reactions: ❤ x1)
😅
----------------------------------------------------------------------------------------------------
[#7914] 2021-12-02 22:41:18
  -> replying to #7913 unknown (user750026879): give a hint, pls, with the first day of winter 2021-2022 :) omikron collapse a time to solve.
There is
Another
D
O
O
R
----------------------------------------------------------------------------------------------------
[#7915] 2021-12-02 22:46:25
  -> replying to #7892 Zil (user980067088): Can we expect a new hint for Christmas this year? You get drunk, we get some new ways to think about this puzzle. Win-win situation 😁
Remind me when it's Christmas.
----------------------------------------------------------------------------------------------------
[#7998] 2021-12-26 15:11:26
Oh well, why not. A mini mini hint. Ready 🐰?
----------------------------------------------------------------------------------------------------
[#8000] 2021-12-26 15:18:32
(edited 2026-02-15 19:29:51 | reactions: ❤ x1, 🔥 x1)
The previous "there is another door hint" is still a thing. We're not sure if anyone has found another door so far, and we can't check that... We've seen prime numbers being mentioned; well, that is definitely an aspect which is required to proceed. Furthermore, along the way, some characters need to be 'zeroed out'.. Best of luck and happy holidays! 🥂
----------------------------------------------------------------------------------------------------
[#8034] 2021-12-30 19:39:11
  -> replying to #8033 Zil (user980067088): @SoWut have the Wachowskis invited you to take part in the making of Matrix 4? :D
...how did you found out?
----------------------------------------------------------------------------------------------------
[#8036] 2021-12-30 19:42:43
  -> replying to #8035 Zil (user980067088): a hunch. I mean they probably attempted to solve the GSMG puzzle and realised they knew less about the matrix than you :)
That leaves me positively speechless
----------------------------------------------------------------------------------------------------
[#8038] 2021-12-30 19:45:53
Rumour has it, it is was done before dawn.
----------------------------------------------------------------------------------------------------
[#8040] 2021-12-30 19:46:44
This was stated after drinking dozers stuff.
----------------------------------------------------------------------------------------------------
[#8042] 2021-12-30 19:47:07
(edited 2026-05-19 02:46:06)
  -> replying to #8039 Zil (user980067088): you mean before they scorched the sky
😁
----------------------------------------------------------------------------------------------------
[#8048] 2021-12-31 12:14:55
  -> replying to #8045 Lazy Prophet (user952048031): yeah.. agree with this @SoWut i also want to ask questions like, how old are you? or are you married? or what is the pk of the puzzle address? 🤔
The only date I give away is the expiry date of neo's passport.
----------------------------------------------------------------------------------------------------
[#8140] 2022-05-25 06:22:06
(edited 2025-12-29 02:53:11 | reactions: 😁 x1)
[ANIMATION: animation.gif.mp4, 3s]
----------------------------------------------------------------------------------------------------
[#8142] 2022-05-25 10:25:33
Looks like somebody found a gsmg subscription.
----------------------------------------------------------------------------------------------------
[#8189] 2022-06-01 12:56:24
👽
----------------------------------------------------------------------------------------------------
[#8288] 2022-09-06 05:21:52
[ANIMATION: animation.gif.mp4, 1s]
----------------------------------------------------------------------------------------------------
[#8301] 2022-12-02 07:14:53
It is meant to be solved.
----------------------------------------------------------------------------------------------------
[#8307] 2022-12-02 07:36:36
There might be a hint coming but not too soon.
----------------------------------------------------------------------------------------------------
[#8309] 2022-12-02 17:45:40
  -> replying to #8308 Alex (user690769341): What is easier? To find the answer to this puzzle or to discover the physics Theory of Everything?
I'm not exactly sure how long it would take to discover that theory so I can't really tell 🤔.
----------------------------------------------------------------------------------------------------
[#8311] 2022-12-11 10:30:38
  -> replying to #8310 barrystyle (user925838121): [FILE: image_2022-12-11_07-09-14.png]
.... That is very specific
----------------------------------------------------------------------------------------------------
[#8315] 2022-12-11 10:33:20
(edited 2025-09-02 20:03:35 | reactions: 🤔 x1)
If the puzzle is solved you'll see how scary specific that is 😂
----------------------------------------------------------------------------------------------------
[#8328] 2023-01-08 23:52:11
@barrystyle, provided a very specific hint already.
----------------------------------------------------------------------------------------------------
[#8330] 2023-01-09 05:10:46
(edited 2025-09-02 19:56:49 | reactions: 🤔 x1)
At least prime number is very important to get any further.
----------------------------------------------------------------------------------------------------
[#8339] 2023-01-11 03:45:22
(edited 2025-02-04 17:06:43 | reactions: 👍 x1)
  -> replying to #8333 Jerry (user786391896): C'mon man give us something more I'm on almost 3 years of this puzzle that turned my hair grey and my wife left me
[ANIMATION: who-wants-to-be-a-millionaire-wwtbam.mp4, 2s]
----------------------------------------------------------------------------------------------------
[#8340] 2023-01-11 03:46:17
Mini apologies for this Jeremy gif, couldn't help myself.
----------------------------------------------------------------------------------------------------
[#8342] 2023-01-11 19:23:03
(edited 2023-01-11 19:23:11)
Rumour has it a new hint is to be expected within 2 months from now.
----------------------------------------------------------------------------------------------------
[#8349] 2023-01-12 06:02:00
(edited 2025-02-04 17:07:52 | reactions: ❤ x1, 😁 x1)
We obviously did this to have a chance at ending up in the Guinness Book for creating the lamest puzzle ever.
----------------------------------------------------------------------------------------------------
[#8352] 2023-01-12 06:07:00
I checked a certain GitHub yesterday, for whoever set that up, nicely done. You guys are really getting close.
----------------------------------------------------------------------------------------------------
[#8353] 2023-01-12 06:08:02
(edited 2024-10-16 14:04:51)
  -> replying to #8350 Alex (user690769341): Are chances to solve less than 2^-256?
At least higher than sqrt(-1).
----------------------------------------------------------------------------------------------------
[#8354] 2023-01-12 06:09:14
(edited 2025-09-02 20:00:34 | reactions: 🫡 x1)
Focussing on the theory of everything is also still a valid path to reaching the private key.
----------------------------------------------------------------------------------------------------
[#8356] 2023-01-12 06:10:54
An imaginary puzzle would.
----------------------------------------------------------------------------------------------------
[#8358] 2023-01-12 06:13:36
  -> replying to #8308 Alex (user690769341): What is easier? To find the answer to this puzzle or to discover the physics Theory of Everything?
[ANIMATION: animation.gif.mp4, 1s]
----------------------------------------------------------------------------------------------------
[#8360] 2023-01-12 06:15:46
(edited 2024-11-12 07:06:06)
Just be clear. My apologies for this puzzle not to be too easy. I'm aware it might appear unsolvable, but it's not. If you find the answer now, the remaining 2.5 btc is well deserved... Or 5, who knows.
----------------------------------------------------------------------------------------------------
[#8364] 2023-01-12 11:05:16
  -> replying to #8361 Detective Froz (user231061724): Why 5 btc? Was the half (2.5 btc) transferred to another puzzle address? 😊And the solver could receive prizes from both addresses...
Every btc halving the price will half too.
----------------------------------------------------------------------------------------------------
[#8368] 2023-01-12 12:47:07
(edited 2024-04-17 10:15:15)
  -> replying to #8367 Alex (user690769341): Who knows...
👆
----------------------------------------------------------------------------------------------------
[#8385] 2023-01-25 09:59:19
42
----------------------------------------------------------------------------------------------------
[#8438] 2023-02-02 09:47:18
  -> replying to #8436 barrystyle (user925838121): LOL I swear you euro types have something wrong with you
I'm staying out of this one 😅
----------------------------------------------------------------------------------------------------
[#8446] 2023-02-23 18:20:03
(edited 2023-12-02 17:47:40 | reactions: 👍 x2)
00100110 10100110 11001110 10010110 10110110 11110110 01001110 00001110 10011110 10000110 11101110 10000110 10100110 01101110 10010110 11100110 10100110 10101110 01001110 00101110 10000110 11001110 10010110 00001110 10100110 00101110 11001110 00101110 11001110 10000110 00110110 10011110 01001110 10100110 01101110 00101110 10010110 11100110 01110110 10010110 10100110 10100110 11001110 00101110 11110110 01110110 10100110 01001110 10101110 11110110 10011110 00101110 10101110 01000110 11001110 10100110 10011110 10100110 01001110 10101110 11110110 10011110 01100110 11110110 00101110 01110110 11110110 01001110 01100110 01110110 10010110 11001110 00101110 10010110 00100110 01001110 11110110 11101110 11001110 11001110 10000110 00001110 10100110 00010110 00101110 10011110 10000110 11101110 10000110 10100110 01101110 10010110 11100110 00101110 01110110 11110110 11101110 10100110 11101110 11100110 01110110 10000110 10011110 01110110 10010110 10011110 10100110 11000110 10010110 11110110 00010110 11000110 10010110 00010110 11000110 01001110 10000110 10100110 01001110 11110110 01100110 10100110 01000110 11001110 00100110 01001110 11110110 11101110 00101110 11001110 10000110 00110110 00101110 11001110 10010110 00110110 10110110 10101110 11001110 00011110 10010110 01001110 00101110 10000110 10110110 11001110 10100110 10110110 10010110 01001110 00001110 10100110 10101110 00110110 01000110 11101110 11110110 00110110 00110110 10100110 10011110
----------------------------------------------------------------------------------------------------
[#8472] 2023-03-03 04:47:19
🐰
----------------------------------------------------------------------------------------------------
[#8483] 2023-04-07 22:53:03
(edited 2026-02-16 12:24:25)
  -> replying to #8448 unknown (user419791047): reversed binary: yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyangwewontgiveawaythepassworditsinfrontofyoureyesbutyourenotseeingitverylaststepisat...
👆🤷‍♂
----------------------------------------------------------------------------------------------------
[#8491] 2023-04-14 13:41:07
(edited 2026-04-08 04:50:56)
It can be solved, albeit very difficult as you have to understand how to interpret all the hints. Currently we are not planning to release any new hints soon.
----------------------------------------------------------------------------------------------------
[#8512] 2023-04-29 17:19:45
😂
----------------------------------------------------------------------------------------------------
[#8516] 2023-05-02 15:12:43
  -> replying to #8515 Zil (user980067088): [ANIMATION: matrix-keenu-reeves.mp4, 13s]
Still remarkable that scene. Especially the expiration date of his passport 😁.
----------------------------------------------------------------------------------------------------
[#8518] 2023-05-02 16:03:59
Hope..
----------------------------------------------------------------------------------------------------
[#8569] 2023-06-10 02:39:07
Correct.
-
No.
-
Can't say anything about this.
----------------------------------------------------------------------------------------------------
[#8608] 2023-06-12 08:31:49
  -> replying to #8607 unknown (user724453304): But he didn't harm anyone !
Physically, I assume not 😅.
----------------------------------------------------------------------------------------------------
[#8773] 2023-08-03 15:50:23
  -> replying to #8771 Zil (user980067088): @SoWut please shine us some 'light'
Ok ok ok ok. I can't hold this one any longer.
----------------------------------------------------------------------------------------------------
[#8774] 2023-08-03 15:51:33
(edited 2024-10-26 04:29:35 | reactions: 🔥 x2)
Are you really looking for just the btc...?
----------------------------------------------------------------------------------------------------
[#8779] 2023-08-03 16:17:19
(edited 2025-06-22 07:12:00 | reactions: 😁 x1)
  -> replying to #8776 unknown (user6249502156): It's nearly been 6 months so I think we all deserve a mini hint if you are willing @SoWut
Another one only 8 minutes after the last one?
----------------------------------------------------------------------------------------------------
[#8787] 2023-08-03 16:28:20
(edited 2023-10-31 11:57:45)
  -> replying to #8784 Zil (user980067088): is this the hint? sorry, this puzzle made me trust noone, not even myself, so just want to be clear 😁
Might be. Wish I had said nothing though.
----------------------------------------------------------------------------------------------------
[#8790] 2023-08-03 16:30:14
  -> replying to #8788 ArchOptic (user6057219919): Now you get lots of questions 😂
Exactly, should have refrained from typing earlier maybe.
----------------------------------------------------------------------------------------------------
[#8792] 2023-08-03 16:32:25
[ANIMATION: confront-interrogate.mp4, 5s]
----------------------------------------------------------------------------------------------------
[#8793] 2023-08-03 16:32:47
(edited 2026-01-03 05:13:44 | reactions: 🔥 x3)
[ANIMATION: what-if-i-told-you-what-if.mp4, 4s]
----------------------------------------------------------------------------------------------------
[#8795] 2023-08-03 16:33:50
  -> replying to #8791 unknown (user6249502156): But you can confirm if there is indeed a 3rd door that is yet to be found right?
I saw that you guys got really really far already.
----------------------------------------------------------------------------------------------------
[#8796] 2023-08-03 16:34:24
(edited 2024-10-26 04:30:30 | reactions: 🤔 x1)
Actually, the hardest part is done.
----------------------------------------------------------------------------------------------------
[#9047] 2023-08-04 20:46:47
  -> replying to #8988 (not in export)
"Globally supporting my generation"
----------------------------------------------------------------------------------------------------
[#9550] 2023-08-06 06:42:15
(edited 2025-01-23 09:10:10 | reactions: 🔥 x1)
This may sound at little dramatic but if I suddenly can't answer you guys anymore, it was nice knowing you all ❤️.
----------------------------------------------------------------------------------------------------
[#9551] 2023-08-06 06:43:46
Oh, and be careful of what you get yourselves into. 🤐
----------------------------------------------------------------------------------------------------
[#9553] 2023-08-06 06:44:27
I'll not explain why.
----------------------------------------------------------------------------------------------------
[#9554] 2023-08-06 06:44:39
(edited 2026-02-02 06:38:06)
The puzzle talks for me.
----------------------------------------------------------------------------------------------------
[#9556] 2023-08-06 06:45:26
(edited 2026-02-15 19:42:58 | reactions: ❤ x1)
And don't worry, I'll just be here in the meanwhile 😘.
----------------------------------------------------------------------------------------------------
[#9572] 2023-08-06 06:55:01
  -> replying to #9570 Zil (user980067088): puzzle prize from stolen funds?
Not at all.
----------------------------------------------------------------------------------------------------
[#9577] 2023-08-06 06:56:34
  -> replying to #9575 Zil (user980067088): I mean if there's a risk for solvers, we should definetely know more than just 'be careful what you get yourselves into'
You know if you know.
----------------------------------------------------------------------------------------------------
[#9586] 2023-08-06 07:22:27
It wasn't cryptic enough before?
----------------------------------------------------------------------------------------------------
[#9592] 2023-08-06 08:05:33
(edited 2024-10-26 04:32:36 | reactions: 👍 x1)
  -> replying to #9588 unknown (user6249502156): Do you wish for puzzle to get solved or you would want it to stay as it is until the next halving?
I wish only for that the puzzle provided some exciting pieces of information. That others have learned something new and that for some it is simply entertaining. I hope that the person who connects the last pieces for the 'main price' will thus get its hands on the private key and hold or spend it wisely, but mostly enjoy it. And lastly, I hope to witness the day that the last scene of mr. Robot becomes a reality.
----------------------------------------------------------------------------------------------------
[#9593] 2023-08-06 08:05:51
  -> replying to #9591 silver_anth (user432257224): is Jrk a secret cyber criminal?
In the eye of the beholder, for sure 😊.
----------------------------------------------------------------------------------------------------
[#9595] 2023-08-06 08:09:27
(edited 2024-07-31 14:50:53 | reactions: ❤ x1)
Technically my friends and family can get to all my data if they'd work together. In that scenario, don't expect a halving of the price.
----------------------------------------------------------------------------------------------------
[#9597] 2023-08-06 08:11:19
Hahaha good one. I thought of a 24h Killswitch, but nah. Can't be bothered :D! Instead.
----------------------------------------------------------------------------------------------------
[#9599] 2023-08-06 08:12:13
(edited 2024-02-11 07:17:56 | reactions: ❤ x4)
Probably the last hint:

Once you hit a "ying yang", you'll be able to solve it the same day.
----------------------------------------------------------------------------------------------------
[#9601] 2023-08-06 08:13:30
  -> replying to #9598 mpeg (user59168199): I won’t lie, after such an obscure puzzle that the best teams haven’t been able to solve yet, a warning that you might go MIA makes it sound a bit sketchy…
Chance is small though. Merely an fyi, bit dramatic as stated earlier.
----------------------------------------------------------------------------------------------------
[#9603] 2023-08-06 08:14:54
(edited 2024-02-10 21:21:20)
Both?
----------------------------------------------------------------------------------------------------
[#9607] 2023-08-06 08:19:07
  -> replying to #9605 silver_anth (user432257224): @SoWut any chance you can tell us if there is another URL to find? otherwise I am going to do a big brute force haha
No need. You have all the info.
----------------------------------------------------------------------------------------------------
[#9608] 2023-08-06 08:19:16
Good to see you again btw.
----------------------------------------------------------------------------------------------------
[#9611] 2023-08-06 08:20:13
(edited 2024-06-07 10:24:38)
No hints 🤡
----------------------------------------------------------------------------------------------------
[#9615] 2023-08-06 08:21:07
  -> replying to #9609 silver_anth (user432257224): I've been lurking for years recharging, finally want to get back in and solve this
My hat off to you, and you know why 🫡.
----------------------------------------------------------------------------------------------------
[#9616] 2023-08-06 08:21:37
  -> replying to #9613 silver_anth (user432257224): Jrk, can you confirm that you will give no hints?
Only fair ones. And to everyone.
----------------------------------------------------------------------------------------------------
[#9621] 2023-08-06 08:43:54
(edited 2025-01-23 09:22:08 | reactions: 👍 x1)
  -> replying to #9616 Jrk Bgrt (user9815232) <-- also JRK: Only fair ones. And to everyone.
To answer your question 'fully', from here on, high likely no hints anymore. But if somehow you all can't solve it from here in the next few years (which I deem unlikely given the state of the solving process), then I might feel the need to give an additional hint, as I couldn't happily live with the idea that some would think that this was a scam. Note, that I hope not to have to give another hint as it would probably be a give away. Good luck to you all!
----------------------------------------------------------------------------------------------------
[#9627] 2023-08-06 08:49:59
  -> replying to #9626 Zil (user980067088): unless Jrk thinks we already know something, which we do not
Something was solved rather... remarkable.
----------------------------------------------------------------------------------------------------
[#9629] 2023-08-06 08:53:56
(edited 2025-05-26 18:44:36 | reactions: 🤔 x1)
Partly.
----------------------------------------------------------------------------------------------------
[#9631] 2023-08-06 08:56:02
I won't!
----------------------------------------------------------------------------------------------------
[#9632] 2023-08-06 09:00:38
(edited 2024-07-31 14:50:40 | reactions: ❤ x1)
Ok, although I somehow feel the need to have my eyes at this chat all for sudden it's time for me to shut up again and see my little ones play in an obstacle parc here on France. Ciao!
----------------------------------------------------------------------------------------------------
[#9636] 2023-08-06 13:23:44
  -> replying to #9634 TG (user1239434587): When did this happen.. may I ask?
I have no clue.
----------------------------------------------------------------------------------------------------
[#9639] 2023-08-06 14:39:34
Correct. Well, technically, you'll need the internet to claim the prize in the end 🤔.
----------------------------------------------------------------------------------------------------
[#9943] 2023-08-11 01:52:53
Hi all, getting quite some DM's which is fine, just know that I'm traveling the next coming days ✌️!
----------------------------------------------------------------------------------------------------
[#9944] 2023-08-11 01:53:25
And I usually answer with "no hints".
----------------------------------------------------------------------------------------------------
[#10423] 2023-08-18 09:24:12
  -> replying to #10398 silver_anth (user432257224): VrsN in the discord had passed givetit before JrK posted that hint
😳 how?
----------------------------------------------------------------------------------------------------
[#10424] 2023-08-18 09:25:35
Hi all. I'm on holiday btw. I might not answer DMs.
----------------------------------------------------------------------------------------------------
[#11989] 2023-08-23 15:43:21
(edited 2026-08-15 08:46:15 | reactions: ❤ x1)
  -> replying to #11911 unknown (user5260693904): Asking what jrk brgt is... That's not allowed as it's a hint???
Note that I get quite some puzzle DMs. I've become used to just say 'no hints'.. (sorry for that).
----------------------------------------------------------------------------------------------------
[#12653] 2023-08-29 14:06:07
  -> replying to #12580 ArchOptic (user6057219919): Jrk has stated that the blockchain messages are not his and are not part of the puzzle
Correct
----------------------------------------------------------------------------------------------------
[#15513] 2023-09-28 12:13:32
  -> replying to #15510 unknown (user5260693904): same here
I'm ok! ♥️
----------------------------------------------------------------------------------------------------
[#15515] 2023-09-28 12:14:24
Sorry for not answering. I've just been trying not to live in my phone, as that has become a habit the last 20 years of my life.
----------------------------------------------------------------------------------------------------
[#15517] 2023-09-28 12:16:21
  -> replying to #15514 unknown (user5939972373): Thank God How was your holiday? Are you back for good?
Still on holiday 😅. In the Caribbean currently. It's lovely here. I see some spam complaints, also sorry for that. Everyone ok besides that?
----------------------------------------------------------------------------------------------------
[#15520] 2023-09-28 12:19:30
Thanks!!!
----------------------------------------------------------------------------------------------------
[#16547] 2023-11-17 07:50:24
(edited 2023-11-17 07:52:03 | reactions: 👍 x4)
Hello there, are we all still having fun?
----------------------------------------------------------------------------------------------------
[#16549] 2023-11-17 07:51:43
(edited 2023-11-17 07:52:09 | reactions: 🔥 x1)
I received some DMs, I thought I'd say hi ✌️. I'm ok, apologies for not being here on a daily basis.
----------------------------------------------------------------------------------------------------
[#16624] 2023-11-24 09:05:13
(edited 2023-11-24 09:10:05 | reactions: 👍 x4, ❤ x1)
There's a question multiple people have asked me. "Given the available knowledge, is internet still required to solve it?"

Nope
----------------------------------------------------------------------------------------------------
[#17884] 2023-12-26 12:13:51
(edited 2026-06-01 19:56:14 | reactions: ❤ x1)
Heeeeelllloooooooo
----------------------------------------------------------------------------------------------------
[#17885] 2023-12-26 12:14:06
(edited 2023-12-26 12:14:52 | reactions: ❤ x4)
Happy Christmas all ❤️
----------------------------------------------------------------------------------------------------
[#17888] 2023-12-26 12:15:02
Hahahaha that meme, love it
----------------------------------------------------------------------------------------------------
[#17889] 2023-12-26 12:15:42
(edited 2023-12-26 12:26:25 | reactions: 👍 x2)
Any spammers I have to ban?
----------------------------------------------------------------------------------------------------
[#17891] 2023-12-26 12:27:27
(edited 2024-06-10 07:08:45)
Have you tried the purple pill already?
----------------------------------------------------------------------------------------------------
[#17893] 2023-12-26 12:28:12
Candy flipping into 2024 ;-)
----------------------------------------------------------------------------------------------------
[#20219] 2024-01-26 12:13:57
~2000 new messages, great. You all doing ok?
----------------------------------------------------------------------------------------------------
[#20223] 2024-01-26 12:21:46
  -> replying to #20221 8а70N (user6501279574): Please say me what format key we are all searching? Answer only this question, maybe PM.
Regular Bitcoin Private key
----------------------------------------------------------------------------------------------------
[#20224] 2024-01-26 12:22:04
  -> replying to #20222 Charlie Craig (user6246033427): I've been banging my head against a wall due to an inability to solve "our first hint is your last command". That seems to be the 2nd to last piece we need to ...
🤐
----------------------------------------------------------------------------------------------------
[#23116] 2024-03-26 06:41:13
(edited 2024-03-26 06:41:21 | reactions: 🤣 x2, 🤨 x1)
I'm not really here, just checking if you folks are still alive and kicking. ✌️
----------------------------------------------------------------------------------------------------
[#23120] 2024-03-26 06:42:36
(edited 2024-03-26 06:42:48 | reactions: 👍 x1)
For all those DM'ing me, the answer to your question is probably NO or YES. I decided not to answer any puzzle questions anymore. If there will be a hint (ever). It will be here.
----------------------------------------------------------------------------------------------------
[#23121] 2024-03-26 06:43:04
(edited 2024-03-26 06:43:29 | reactions: 👍 x2)
  -> replying to #23119 unknown (user5260693904): aghhh sorry for the all caps
IT'S OK, I FORGOT THAT IT'S CAPS TUESDAY.
----------------------------------------------------------------------------------------------------
[#23124] 2024-03-26 06:46:40
(edited 2024-03-26 06:47:16 | reactions: 👍 x1)
Yeah, being lost is a common aspect of being on this planet I guess, or at least when tempering with rabbit holes.
----------------------------------------------------------------------------------------------------
[#23125] 2024-03-26 06:47:53
Btw, for those with the heartwarming words. Many thanks ❤️.
----------------------------------------------------------------------------------------------------
[#23129] 2024-03-26 06:49:08
Please understand that I get multiple of these questions on a daily basis..
----------------------------------------------------------------------------------------------------
[#23130] 2024-03-26 06:50:02
(edited 2024-03-26 06:50:26 | reactions: 👍 x1)
There are investment institutions for this. Requesting money for a solid idea is not that difficult.
----------------------------------------------------------------------------------------------------
[#23133] 2024-03-26 06:52:11
(edited 2024-03-26 06:52:41 | reactions: 🤩 x1)
Yes. Some if you might soon be drinking it probably.
----------------------------------------------------------------------------------------------------
[#23134] 2024-03-26 06:53:04
(edited 2024-03-26 06:53:27 | reactions: 😭 x1)
  -> replying to #23132 DaniyarK (user752158324): @SoWut I'm surprised that no-one don't swear to you. Literally destroyed everyone patience
Seems puzzlers are decent people ;-).
----------------------------------------------------------------------------------------------------
[#23136] 2024-03-26 06:55:39
  -> replying to #23135 X (user497668740): yeah thats why I tried to build a team from here to work on a real project which we can potentially make millions but no one interested
Ask Claude-3 for the best approach maybe?
----------------------------------------------------------------------------------------------------
[#23138] 2024-03-26 06:56:29
Understandable
----------------------------------------------------------------------------------------------------
[#23140] 2024-03-26 06:57:09
Does it come close to Claude and gpt?
----------------------------------------------------------------------------------------------------
[#23151] 2024-03-26 10:40:01
  -> replying to #23148 Jerry (user786391896): @SoWut could you at least tell us which hints are no longer relevant, usually we get one tiny question puzzle related to ask you, last time it was wasted
Technically yes but Nope.
----------------------------------------------------------------------------------------------------
[#23152] 2024-03-26 10:40:38
(edited 2024-03-26 10:40:45 | reactions: 🤣 x2)
And hi, you're hallucinating. Is it the mescaline?
----------------------------------------------------------------------------------------------------
[#23154] 2024-03-26 10:41:41
😉
----------------------------------------------------------------------------------------------------
[#23159] 2024-03-26 13:05:05
  -> replying to #23155 Lain (user1472167187): Tell me one thing, @SoWut. Are you a one or a zero? This is the question you need to ask yourself. Are you a yes or a no? Will you act or not? You won't give a...
I prefer superpositions 😉.
----------------------------------------------------------------------------------------------------
[#23163] 2024-03-26 13:23:03
  -> replying to #23161 Lain (user1472167187): Sure, there are grays... but when you come right down to it, at its core, beneath every choice, there's either a one or a zero. At the moment you have chosen t...
You're doing fine.
----------------------------------------------------------------------------------------------------
[#23200] 2024-03-27 12:41:56
(edited 2026-08-09 14:09:25 | reactions: 😁 x1)
  -> replying to #23193 Robbit (user5602405073): What do you think this picture looks like?
Sqaures and a rabbit?
----------------------------------------------------------------------------------------------------
[#24071] 2024-04-10 14:21:30
(edited 2024-04-10 14:43:22 | reactions: 🔥 x2, ❤ x1)
1357 blocks to go
----------------------------------------------------------------------------------------------------
[#24491] 2024-04-17 07:02:00
(edited 2024-04-17 07:58:31 | reactions: ❤ x3)
I received some complaints about insulting behavior.

May it be obvious that it's not acceptable.

Please refrain from doing so, or I have to get the banhammer out of the drawer of either slap someone with a large trout.

Please be nice ❤️.
----------------------------------------------------------------------------------------------------
[#24492] 2024-04-17 07:03:03
(edited 2024-04-17 07:27:43 | reactions: 👍 x5)
Happy countdown everyone ✌️!
----------------------------------------------------------------------------------------------------
[#24623] 2024-04-19 20:08:44
Ha, we lost one 'puzzler'.
----------------------------------------------------------------------------------------------------
[#24624] 2024-04-19 20:10:14
(edited 2025-02-18 17:47:03 | reactions: 😨 x1)
Seemed like a nice moment to get the ban hammer out of the drawer.
----------------------------------------------------------------------------------------------------
[#24626] 2024-04-19 20:10:43
(edited 2024-04-19 20:12:45 | reactions: 🎉 x7)
Happy halving everyone!
----------------------------------------------------------------------------------------------------
[#24627] 2024-04-19 20:15:48
(edited 2024-04-19 20:16:51 | reactions: 🙏 x5)
For those that still haven't solved the puzzle. There are few prizes to win besides the banter in this chat. A private key, some 'obscure' intel, or what I hope most of you have discovered by now, the most obvious reason to make sure you hold on to Bitcoin 😉.
----------------------------------------------------------------------------------------------------
[#24628] 2024-04-19 20:15:54
✌️
----------------------------------------------------------------------------------------------------
[#24638] 2024-04-19 20:29:57
(edited 2024-04-24 07:22:51)
16$ fee. Damn.

Well, anyway, see you in 4 years! Good luck you all.
----------------------------------------------------------------------------------------------------
[#24640] 2024-04-19 20:31:10
(edited 2024-04-19 20:43:59 | reactions: ❤ x1)
Me? No. Don't know that guy.
----------------------------------------------------------------------------------------------------
[#24652] 2024-04-19 21:34:10
I should.
----------------------------------------------------------------------------------------------------
[#24654] 2024-04-19 21:35:15
(edited 2024-04-19 21:45:51 | reactions: 👍 x3)
Challenge accepted.
----------------------------------------------------------------------------------------------------
[#25758] 2024-06-06 04:16:00
Crazy No hint Thursday, every Friday!
----------------------------------------------------------------------------------------------------
[#25767] 2024-06-07 06:10:08
An active one.
----------------------------------------------------------------------------------------------------
[#26085] 2024-07-11 15:29:17
  -> replying to #26073 𝕠𝕙 𝕙𝕚, 𝕄𝕒𝕣𝕜 (user1571850682): @SoWut Dear friend, are you planning to post any additional hints?
None planned.
----------------------------------------------------------------------------------------------------
[#26223] 2024-07-31 20:26:53
[ANIMATION: tumbleweed.mp4, 6s]
----------------------------------------------------------------------------------------------------
[#26490] 2024-08-30 05:21:04
  -> replying to #26489 unknown (user5260693904): Idk to be honest... I think I may have been hacked somehow.... Or maybe some kinda glitch on telegram??? I apologize fully to you and anyone else that may have...
It indeed set to private. I haven't opened tg for a while so I guess it wasn't from my side 🫤.
----------------------------------------------------------------------------------------------------
[#26875] 2024-09-19 03:20:23
(edited 2024-09-19 03:40:07 | reactions: 👍 x3)
I simply liked Jacque's ideas a lot. I have techy friends building communities around that idea today; I haven't invested much time into it as I should myself. But in the coming years I move to a place where that becomes a possibility.
----------------------------------------------------------------------------------------------------
[#27882] 2024-10-21 15:03:09
(edited 2025-04-05 17:33:16 | reactions: ❤ x1)
  -> replying to #27602 (not in export)
I know a Matthew, and if he knows a Roberto, it's likely the same one and a very smart guy. 😉
----------------------------------------------------------------------------------------------------
[#27884] 2024-10-21 15:03:34
Hi all! Everyone still happy?
----------------------------------------------------------------------------------------------------
[#27907] 2024-10-21 15:06:58
(edited 2024-10-21 15:08:27 | reactions: 👌 x1)
  -> replying to #27899 unknown (user1690548820): Making some stuffed peppers, how are you?
Nice! Chilling under artificial stars, clearing up disks.
----------------------------------------------------------------------------------------------------
[#32529] 2024-11-29 04:56:10
In that case I'll show, as I don't have much talent.
----------------------------------------------------------------------------------------------------
[#32530] 2024-11-29 04:56:39
(edited 2024-11-29 04:57:17 | reactions: ❤ x7)
Hello everyone, still having fun :-)?
----------------------------------------------------------------------------------------------------
[#32532] 2024-11-29 04:57:24
(edited 2024-11-29 04:57:37 | reactions: 👍 x6)
I was told this group could use some moderation.
----------------------------------------------------------------------------------------------------
[#32535] 2024-11-29 04:59:41
(edited 2024-11-29 05:05:25 | reactions: 💯 x3)
If wallet != empty, puzzle not solved.

(Most likely).
----------------------------------------------------------------------------------------------------
[#32537] 2024-11-29 05:00:19
(edited 2024-11-29 05:00:31 | reactions: 👍 x5, 🤣 x1)
  -> replying to #32534 𝕠𝕙 𝕙𝕚, 𝕄𝕒𝕣𝕜 (user1571850682): You can give moderator rights to someone you trust.
That was indeed the plan.
----------------------------------------------------------------------------------------------------
[#32550] 2024-11-29 05:10:40
(edited 2024-11-29 05:11:08 | reactions: 🤣 x2, 😱 x1)
  -> replying to #32548 𝕠𝕙 𝕙𝕚, 𝕄𝕒𝕣𝕜 (user1571850682): Can we expect a Christmas hint?
[ANIMATION: the-train.mp4, 2s]
----------------------------------------------------------------------------------------------------
[#32555] 2024-11-29 05:13:16
  -> replying to #32551 Denis Golovkin (user398109413): Depending on what "to be a literally hacker" means. Hacker is not necessarily about security or even about computers. It's more about deep knowledge of smth. W...
If at all, a very bad one. Not even worth the title of skid. Although, as you might have guessed, I've seen some 'security' places 'protecting' our digital realms.
----------------------------------------------------------------------------------------------------
[#32557] 2024-11-29 05:15:17
Haven't interacted with a terminal in a while. "But what can you do without a cpu?", touch grass it is.
----------------------------------------------------------------------------------------------------
[#32560] 2024-11-29 05:17:21
  -> replying to #32556 Sreejit Roy Chowdhury (user6603256460): Ok but hint? At least in where to focus on salph or in the puzzle
Hint? Hint? Heh, what craziness are you talking about? There is no hint.
----------------------------------------------------------------------------------------------------
[#32561] 2024-11-29 05:17:37
(edited 2024-11-29 05:26:08 | reactions: 🤣 x5, 😁 x1)
[ANIMATION: matrix-merowinger-aktion-reaktion.mp4, 7s]
----------------------------------------------------------------------------------------------------
[#32570] 2024-11-29 05:20:59
(edited 2024-11-29 06:08:44 | reactions: 😢 x2, 👍 x1)
  -> replying to #32568 silver_anth (user432257224): puzzle been out so long jrk probably doesn't even remember how to solve it
🤐
----------------------------------------------------------------------------------------------------
[#32579] 2024-11-29 05:28:47
(edited 2024-11-29 05:29:16 | reactions: ❤ x5, 🙏 x3, ⚡ x1, 👍 x1)
At this point, I don't know what to hint, without ruining it for those that might find it. If you guys got 1 microstep further, the puzzle will likely be solved the same day.

I could come up with some empty cryptic bs hint, but that would be lame too.

And in the end, good puzzles don't need hints, hence this puzzle appears to be a tiny bit shitty sometimes.
----------------------------------------------------------------------------------------------------
[#32580] 2024-11-29 05:29:20
(edited 2024-11-29 05:29:27 | reactions: 😁 x3, ❤ x1)
No clue Friday.
Every Saturday.
----------------------------------------------------------------------------------------------------
[#32590] 2024-11-29 05:39:33
(edited 2024-11-29 05:39:50 | reactions: 👍 x6, 😁 x4, 😢 x1)
Oh, and before I forget, apologies for not answering any DMs, don't take it personal.

I mainly got tired of answering with either 'no hints', or listening to sad stories about family, or kids with severe health problems, hoping to obtain a hint, all day every day.
----------------------------------------------------------------------------------------------------
[#32597] 2024-11-29 05:42:55
(edited 2024-11-29 05:43:09 | reactions: ❤ x1)
I saw that @qv8du3ne8s9 😂
----------------------------------------------------------------------------------------------------
[#32613] 2024-11-29 05:47:19
(edited 2024-11-29 05:51:15 | reactions: 😁 x1, 👌 x1)
  -> replying to #32600 ArchOptic (user6057219919): What character do I have to imagine myself as?
I think I'll be going for ASCII 127 myself. But not overly dramatic.
----------------------------------------------------------------------------------------------------
[#32640] 2024-11-29 05:57:33
(edited 2024-11-29 05:58:19 | reactions: ❤ x5, 👌 x1, 😨 x1)
  -> replying to #32617 Martín (user122813939): So Jrk, are you safe or the MIA thing is a possibility still ?
I think I'm fine - gladly I don't feel that weird anxiety anymore. However, I do expect that in about 18 years my government might have to notify me that I've been 'under investigation' for a while. But don't worry about me; me, family and friends are doing great!
----------------------------------------------------------------------------------------------------
[#32644] 2024-11-29 05:58:58
(edited 2024-11-29 05:59:17 | reactions: ✍ x1, 🤣 x1)
  -> replying to #32627 silver_anth (user432257224): Jrk can't even say a joke without it being seen as a hint hahaha
This is so true. I must say, with that in mind, it makes typing any message here a bit more challenging.
----------------------------------------------------------------------------------------------------
[#32647] 2024-11-29 06:00:25
(edited 2024-11-29 06:00:56 | reactions: 👍 x1)
Admins
----------------------------------------------------------------------------------------------------
[#32659] 2024-11-29 06:02:00
(edited 2024-11-29 06:02:06 | reactions: 🤣 x2)
Happiness.
----------------------------------------------------------------------------------------------------
[#32671] 2024-11-29 06:06:24
(edited 2024-11-29 06:07:09 | reactions: 🤣 x3)
  -> replying to #32666 ArchOptic (user6057219919): That's actually a good idea. It's an infinite key
You only need the last number of pi and it might get you somewhere.
----------------------------------------------------------------------------------------------------
[#32687] 2024-11-29 06:13:47
(edited 2025-07-09 15:39:03 | reactions: 😱 x1)
I already have gray hair unfortunately.
----------------------------------------------------------------------------------------------------
[#32690] 2024-11-29 06:15:34
Maybe Bryan Johnson has an answer for my hair.
----------------------------------------------------------------------------------------------------
[#32695] 2024-11-29 06:20:19
(edited 2025-07-09 15:39:20 | reactions: 🤨 x1)
  -> replying to #32686 Jerry (user786391896): what is that ^ @SoWut 0
Pimeyes leads me to a festival thingy in the Netherlands. Is this a puzzle?
----------------------------------------------------------------------------------------------------
[#32699] 2024-11-29 06:23:12
  -> replying to #32696 X (user497668740): why does the puzzle have 2 different pages (/PUZZLE and /puzzle), you never said anything about it?
Not sure why but I suppose it doesn't affect the puzzle.
----------------------------------------------------------------------------------------------------
[#32701] 2024-11-29 06:25:31
(edited 2026-02-02 06:57:04 | reactions: ❤ x1)
Could be, it has been years and we had a few FE guys working on it.
----------------------------------------------------------------------------------------------------
[#32705] 2024-11-29 06:28:41
Yeah, what can I say? In a way, it's a pretty smart by mr Sailor, and Bitcoin is built to withstand this shenanigans anyway.
----------------------------------------------------------------------------------------------------
[#32707] 2024-11-29 06:29:55
Yeah NAD is great.
----------------------------------------------------------------------------------------------------
[#32711] 2024-11-29 06:30:33
I only take ~80 supplements daily, nothing crazy 😅.
----------------------------------------------------------------------------------------------------
[#32715] 2024-11-29 06:32:02
Blueprint is sort of the leading list at this point.
----------------------------------------------------------------------------------------------------
[#32719] 2024-11-29 06:34:04
(edited 2024-11-29 06:34:15 | reactions: 😁 x8)
I mean, if you guys don't solve it anytime soon I'll have to try and stay alive till the year 2145.
----------------------------------------------------------------------------------------------------
[#32724] 2024-11-29 06:37:27
(edited 2024-11-29 06:38:05 | reactions: 👍 x3)
I explain them a lot but I don't want them to know about BTC yet, having this unhealthy fear for btc kidnapping.
----------------------------------------------------------------------------------------------------
[#32728] 2024-11-29 06:39:50
  -> replying to #32726 Σ⸙ꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋᅠᅠᅠ𓆈⃤ (user7731476133): What did you doo 🤣
Enjoying life, mostly 😉.
----------------------------------------------------------------------------------------------------
[#32741] 2024-11-29 06:47:44
(edited 2026-07-01 10:55:39)
  -> replying to #32730 silver_anth (user432257224): can't agree with melatonin being on that list. that can really screw with your circadian rhythm and suppress your natural production of it
Yeah, heard this argument before. Haven't used it myself for years. Bryan is a bit.. extreme, and his team of doctors probably concluded that it's good for him. Also, there aren't many studies that have concluded that long term low dose usage would do any damage.

In the end there's no perfect static setup, as we're all a bit different.
----------------------------------------------------------------------------------------------------
[#32748] 2024-11-29 06:51:05
(edited 2024-11-29 06:52:03 | reactions: 😁 x1)
  -> replying to #32735 silver_anth (user432257224): I'm taking a year off at the moment but was working in internal medicine
Another doctor in my room states that these are indeed the typical puzzle doctors 😉.
----------------------------------------------------------------------------------------------------
[#32755] 2024-11-29 06:54:17
(edited 2025-04-01 20:43:34)
  -> replying to #32752 ArchOptic (user6057219919): AI in 20 years will help
Already better than many doctors... especially for discovering very unlikely cases.
----------------------------------------------------------------------------------------------------
[#32767] 2024-11-29 07:03:37
(edited 2024-11-29 08:45:23 | reactions: ❤ x1)
I'd quit that if you want quality sleep. I used it so much, my body can't deal with it anymore. After a week or 2 you'll start dreaming again.
----------------------------------------------------------------------------------------------------
[#32770] 2024-11-29 07:05:46
Ah sorry, I missed that. I used a gram daily, for years. 😅
----------------------------------------------------------------------------------------------------
[#32772] 2024-11-29 07:06:39
  -> replying to #32763 Martín (user122813939): Did you try with the basics arch?, Eat well, exercise, etc..
🫡
----------------------------------------------------------------------------------------------------
[#32773] 2024-11-29 07:13:43
(edited 2024-11-29 07:14:15 | reactions: ❤ x5, 👍 x3, 👀 x1)
Ok, I'm off people 👻. Be good, stay healthy, stack sats and enjoy life. 

Ciao!

And good luck Admins! (And many thanks in advance, please be fair 😉).
----------------------------------------------------------------------------------------------------
[#39192] 2025-04-28 12:45:31
(edited 2025-04-28 12:46:52 | reactions: 👍 x3, 🤝 x2, 🕊 x1, 🐳 x1)
[ANIMATION: forrest-gump-wave.mp4, 2s]
----------------------------------------------------------------------------------------------------
[#39194] 2025-04-28 12:45:47
(edited 2025-04-28 17:49:37 | reactions: 👍 x2)
You people are still having fun I see.
----------------------------------------------------------------------------------------------------
[#39200] 2025-04-28 12:48:07
Ah, no hints? Ok, that's also fine.
----------------------------------------------------------------------------------------------------
[#39206] 2025-04-28 12:51:05
(edited 2025-04-28 12:51:52 | reactions: 🤔 x3, 👀 x1)
I have to say, that touching grass thingy is pretty nice.
----------------------------------------------------------------------------------------------------
[#39208] 2025-04-28 12:52:50
(edited 2025-04-28 13:16:16 | reactions: 🤔 x2, ❤ x1)
  -> replying to #39205 k1ng 😎 (user7363495849): Jrk, what do you think about ethereum, is it worth holding 25% in eth or bitcoin only?
Yeah, tricky question. You can try to time it (I stopped doing that), but if you understand the puzzle you'll discover that I'd suggest btc only, and don't gamble.
----------------------------------------------------------------------------------------------------
[#39217] 2025-04-28 12:55:14
(edited 2025-04-29 10:51:16 | reactions: 👍 x2)
I was hinted when eth was 2$. Saw the "DAO" unfold live in front of my eyes with 8000 holders on slack; was allowed to double my eth with all the left over etc, and then swap it to btc. Good old times.
----------------------------------------------------------------------------------------------------
[#39219] 2025-04-28 12:56:14
(edited 2025-04-28 12:56:59 | reactions: 🤣 x3, 👍 x1, 🔥 x1, 😨 x1)
If I'd ever take the funds (I won't), I wouldn't even tell the answer 😈.
----------------------------------------------------------------------------------------------------
[#39224] 2025-04-28 12:57:17
(edited 2025-04-28 12:57:31 | reactions: 👍 x2, 😱 x1)
Did anyone found yingyang? I don't think so, you guys are so smart, when yingyang is reached, 2 hours max.
----------------------------------------------------------------------------------------------------
[#39229] 2025-04-28 12:58:50
(edited 2025-04-28 12:59:18 | reactions: 😁 x3)
Im with alcohol, dont blame me for more typos.
----------------------------------------------------------------------------------------------------
[#39232] 2025-04-28 12:59:29
(edited 2025-05-31 16:53:52 | reactions: 👌 x1, 🤨 x1)
Alcohol, and answering this chat go hand in hand somehow.
----------------------------------------------------------------------------------------------------
[#39234] 2025-04-28 13:00:26
  -> replying to #39221 X (user497668740): why you guys added that after 6 years?
Que?
----------------------------------------------------------------------------------------------------
[#39237] 2025-04-28 13:01:36
(edited 2025-04-28 13:20:30 | reactions: 😢 x1, 🤝 x1)
  -> replying to #39233 silver_anth (user432257224): is yinyang found after decoding an AES ciphertext?
It’s the next phase, but I await the day someone finally gets there.
----------------------------------------------------------------------------------------------------
[#39241] 2025-04-28 13:02:46
(edited 2025-04-28 13:02:59 | reactions: 👍 x6, ❤ x2)
Ok, the "better half" is hungry. Which means I'm off 🤗
----------------------------------------------------------------------------------------------------
[#49172] 2025-09-15 22:20:54
(edited 2025-09-15 22:20:59 | reactions: ❤ x2, 🫡 x2)
[ANIMATION: happy-carrot.mp4, 4s]
----------------------------------------------------------------------------------------------------
[#49175] 2025-09-15 22:24:36
(edited 2025-09-16 08:01:43 | reactions: 😁 x1)
Yes
----------------------------------------------------------------------------------------------------
[#49176] 2025-09-15 22:24:52
(edited 2025-09-15 22:25:14 | reactions: ✍ x1, 🤔 x1, 🤩 x1, 🌚 x1)
Carrots were originally purple, until the Dutch turned them orange in the 1600s to kiss up to their royal family.
----------------------------------------------------------------------------------------------------
[#53335] 2025-12-31 22:15:02
(edited 2025-12-31 22:15:53)
.
----------------------------------------------------------------------------------------------------
[#53336] 2025-12-31 22:16:15
..
----------------------------------------------------------------------------------------------------
[#53338] 2025-12-31 22:17:05
...
----------------------------------------------------------------------------------------------------
[#53339] 2025-12-31 22:18:07
....
----------------------------------------------------------------------------------------------------
[#53341] 2025-12-31 22:19:05
(edited 2026-06-01 19:54:48 | reactions: ❤ x2)
.....
----------------------------------------------------------------------------------------------------
[#53342] 2025-12-31 22:20:03
(edited 2025-12-31 22:22:22 | reactions: ❤ x12, ❤‍🔥 x2, 👍 x2, 😁 x2)
01001000 01100001 01110000 01110000 01111001 00100000 01101110 01100101 01110111 00100000 01111001 01100101 01100001 01110010 00100001 00100000 01001101 01100001 01101011 01100101 00100000 01110100 01101000 01100101 00100000 01100010 01100101 01110011 01110100 00100000 01101111 01100110 00100000 01100101 01110110 01100101 01110010 01111001 01110100 01101000 01101001 01101110 01100111 00101110 00100000 01001111 01101000 00101100 00100000 01100001 01101110 01100100 00100000 01101000 01100101 01110010 01100101 00100111 01110011 00100000 01100001 00100000 00100010 01110100 01101001 01101110 01111001 00100000 01101000 01101001 01101110 01110100 00100010 00100000 00111100 00110011 00101110
----------------------------------------------------------------------------------------------------
[#60285] 2026-03-03 20:11:55
  -> replying to #60282 gnomad (user142464266): Nobody owes anybody anything. We are all here by free will. A puzzle was created as a gift by the creator @SoWut , in a way that they chose. Play or do not pla...
👆🫡
----------------------------------------------------------------------------------------------------
[#60286] 2026-03-03 20:12:28
(edited 2026-03-03 20:12:34 | reactions: 🤝 x2, ❤ x1, 🙏 x1, 🫡 x1)
Hi all 👋🏻
----------------------------------------------------------------------------------------------------
[#60289] 2026-03-03 20:17:02
(edited 2026-03-03 20:17:44 | reactions: 😁 x1, 🤔 x1)
No hints , only free will. One of the few things I somehow strugle to fully accept albeit that science is currently not on the deterministic side if I'm not mistaken.
----------------------------------------------------------------------------------------------------
[#60292] 2026-03-03 20:18:06
(edited 2026-03-04 13:48:57 | reactions: 💯 x2)
Everyone still having fun?
----------------------------------------------------------------------------------------------------
[#60298] 2026-03-03 20:19:39
Jacque was quite an inspiring lad I'd say.
----------------------------------------------------------------------------------------------------
[#60302] 2026-03-03 20:21:38
(edited 2026-03-04 07:06:34 | reactions: 👌 x1)
It's kinda of a pvp zone here. Sort of a rust server with both nice and toxic units.
----------------------------------------------------------------------------------------------------
[#60306] 2026-03-03 20:22:42
(edited 2026-03-03 20:26:02)
Maybe, Cartman's quote about chatroulette fits too.
----------------------------------------------------------------------------------------------------
[#60307] 2026-03-03 20:23:27
(edited 2026-03-03 20:23:36 | reactions: 😁 x3)
  -> replying to #60300 X (user497668740): @SoWut Are we really looking for just the btc...?
🤐
----------------------------------------------------------------------------------------------------
[#60309] 2026-03-03 20:27:00
(edited 2026-03-03 20:27:12 | reactions: ❤ x1, 👀 x1)
  -> replying to #60308 X (user497668740): we can't proceed further and i believe we have been wasted years to prove it. idk what are u expect from us but you need to hint us about the direction.
Looks at gnomad. 👀
----------------------------------------------------------------------------------------------------
[#60312] 2026-03-03 20:29:05
(edited 2026-03-03 20:30:07 | reactions: ❤ x2)
Bingo
----------------------------------------------------------------------------------------------------
[#60314] 2026-03-03 20:30:47
(edited 2026-03-03 20:31:09 | reactions: 🔥 x1, 😁 x1, 😨 x1, 🤝 x1, 😎 x1)
I only need to look at the address. If any of you reaches the next phase, the price is taken in no-time.
----------------------------------------------------------------------------------------------------
[#60316] 2026-03-03 20:31:09
🤷‍♂️
----------------------------------------------------------------------------------------------------
[#60318] 2026-03-03 20:32:01
(edited 2026-03-04 07:12:07 | reactions: ❤ x1)
I suppose that could get you far in real life.
----------------------------------------------------------------------------------------------------
[#60322] 2026-03-03 20:33:52
(edited 2026-03-03 20:34:09 | reactions: ❤ x7, 🫡 x1)
Before I forget. For those who DM me, my apologies for not answering - or only rarely. Nothing personal ❤️.
----------------------------------------------------------------------------------------------------
[#60324] 2026-03-03 20:35:22
(edited 2026-03-06 15:54:40 | reactions: 🔥 x3, 👍 x1)
I'm going to rewatch episode 3.5 with  the better half.
----------------------------------------------------------------------------------------------------
[#60326] 2026-03-03 20:36:04
(edited 2026-07-01 13:59:46)
  -> replying to #60323 D1rty Byrd (user7675830926): i must ask you does the binary contact info from the website jrk.agency have anything to do with the puzzle jrk.xlsx?
Nope. You're not the first to ask.
----------------------------------------------------------------------------------------------------
[#60327] 2026-03-03 20:37:14
(edited 2026-03-04 00:38:00 | reactions: 👍 x3, ❤ x2, 🫡 x1)
Cheers all, good luck again 👋🏻!
----------------------------------------------------------------------------------------------------
[#63957] 2026-05-28 07:41:02
(edited 2026-05-28 07:41:51 | reactions: 🎉 x5, ❤ x1)
  -> replying to #63942 𝔻𝕖𝕣S𝕋 (user697342298): @SoWut The sites are down. Can you tell us whether this will affect us if we manage to resolve Salp or Cosmic? We're worried about relying on another site and ...
Ah, ofcourse. The puzzle is still valid!
----------------------------------------------------------------------------------------------------
[#63966] 2026-05-28 09:34:18
(edited 2026-05-28 10:16:31 | reactions: ❤ x3)
  -> replying to #63959 X (user497668740): Crazy No hint Thursday, every Friday!
🫡🥳
----------------------------------------------------------------------------------------------------
[#66540] 2026-07-12 20:17:04
(edited 2026-07-12 20:52:00 | reactions: 😁 x2, ❤ x1, 🗿 x1)
I just dawned on me; what if one day, some of you finally finds it... and doesn't explain it publicly, while I've already passed away. How do I have to turn myself around in my grave 🤔...
----------------------------------------------------------------------------------------------------
[#66542] 2026-07-12 20:21:05
(edited 2026-07-13 13:06:42 | reactions: 🔥 x1, 😁 x1)
Another thing. In 2029, all btc on old addresses might be cracked (cmiiw).
----------------------------------------------------------------------------------------------------
[#66543] 2026-07-12 20:21:43
Whats your view on that?
----------------------------------------------------------------------------------------------------
[#66549] 2026-07-12 20:26:42
I might me drunk, or worse, I dont even know what rhetorical is at this point.
----------------------------------------------------------------------------------------------------
[#66551] 2026-07-12 20:27:09
(edited 2026-07-12 20:27:30 | reactions: 🔥 x1, 🤝 x1)
Hell yes
----------------------------------------------------------------------------------------------------
[#66555] 2026-07-12 20:30:03
(edited 2026-07-13 07:52:11 | reactions: 🫡 x1)
Anyway, if bip360 is going to be a thing. I have to come up with something.
----------------------------------------------------------------------------------------------------
[#66559] 2026-07-12 20:34:41
(edited 2026-07-16 16:32:02 | reactions: 🔥 x1)
  -> replying to #66557 Σ⸙ꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋᅠᅠᅠ𓆈⃤ (user7731476133): Or was it just a spur of the moment decision
Well this nearly perfectly phrases it. Yes, I was busy with gsmg and quite obviously linked it too it, but I was in a crazy mood and honestly I still don't know how I got this weird idea to make a puzzle. The rickroll effect inspired me to make an actual puzzle, just to see if I could. It wasn’t a PR stunt until I realized it after I published it. The others didnt fully understand/agree for what I remember.
----------------------------------------------------------------------------------------------------
[#66560] 2026-07-12 20:35:20
  -> replying to #66554 Denis Golovkin (user398109413): Oh, he is drunk! Load all the social engineering scripts into your ChatGPT's guys!
Yeah, fire away.
----------------------------------------------------------------------------------------------------
[#66561] 2026-07-12 20:37:00
(edited 2026-07-13 02:04:54 | reactions: 🤣 x2, 😁 x1)
I have these moment where I get into a frenzy and zone in with 800%. A day later I can hardly understand what I have done 🫤. And that is not a joke.
----------------------------------------------------------------------------------------------------
[#66564] 2026-07-12 20:45:53
(edited 2026-07-13 10:45:03 | reactions: 🤣 x2)
I don't know right now.
----------------------------------------------------------------------------------------------------
[#66568] 2026-07-12 20:47:16
(edited 2026-07-13 19:04:05 | reactions: 😁 x1, 🤔 x1)
Most of you know the puzzle WAAAY better than me at this point. I have a hidden laptop which I haven't touched in years. On that thing... is the actual answer....
----------------------------------------------------------------------------------------------------
[#66571] 2026-07-12 20:49:19
Some of you, can find me. Quite a few in this chat, already met me.
----------------------------------------------------------------------------------------------------
[#66573] 2026-07-12 20:51:37
My close friends have the best chance of solving it (a few tried). But they don't have the skills some of you do.
----------------------------------------------------------------------------------------------------
[#66574] 2026-07-12 20:51:59
(edited 2026-08-23 23:19:59 | reactions: ❤ x1)
NOTE: that is a hint.
----------------------------------------------------------------------------------------------------
[#66576] 2026-07-12 20:52:24
Hi
----------------------------------------------------------------------------------------------------
[#66578] 2026-07-12 20:52:58
(edited 2026-07-16 17:19:16 | reactions: ❤ x1, 😁 x1)
💯
----------------------------------------------------------------------------------------------------
[#66581] 2026-07-12 20:53:46
(edited 2026-07-13 19:02:05 | reactions: 👍 x1, 😁 x1)
Beer, red wine and champagne.
----------------------------------------------------------------------------------------------------
[#66582] 2026-07-12 20:54:16
(edited 2026-07-13 02:16:55 | reactions: 😁 x1, 🗿 x1)
It kills braincells.
----------------------------------------------------------------------------------------------------
[#66584] 2026-07-12 20:55:29
(edited 2026-07-18 05:57:05)
Welcome. I feel it a bit off knowing the url (and thus the original puzzle) is "gone".
----------------------------------------------------------------------------------------------------
[#66586] 2026-07-12 20:56:04
Nope.
----------------------------------------------------------------------------------------------------
[#66588] 2026-07-12 21:01:05
Yes
----------------------------------------------------------------------------------------------------
[#66589] 2026-07-12 21:03:51
(edited 2026-07-13 00:30:37 | reactions: ✍ x1, 🤝 x1)
And IIFF I'm somehow still wrong, which I'm most likely not as I've verified many times back then after some sad rushed mistakes, it's all still solvable with a few stable qubits.
----------------------------------------------------------------------------------------------------
[#66590] 2026-07-12 21:04:38
(edited 2026-07-13 02:18:37 | reactions: 😁 x1)
But... Bip360 anyone. Thoughts?
----------------------------------------------------------------------------------------------------
[#66592] 2026-07-12 21:08:52
(edited 2026-07-13 02:19:06 | reactions: 🔥 x1, 😁 x1, 🌚 x1)
  -> replying to #66556 Σ⸙ꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋᅠᅠᅠ𓆈⃤ (user7731476133): You know what. @SoWut this isn't a request for a hint but I don't think anyone ever really asked you this publicly. What was your inspiration / desire to creat...
Oh... and before I fall asleep. I want to assume it is quite clear I held quite a secret in my head which I seriously wanted to share with the planet... for those who can understand what I meant...
----------------------------------------------------------------------------------------------------
[#66593] 2026-07-12 21:10:37
(edited 2026-07-12 21:11:17 | reactions: 🤔 x5)
The "5" btc was never the actual prize. That was only a tiny fraction.
----------------------------------------------------------------------------------------------------
[#66595] 2026-07-12 21:11:31
(edited 2026-07-26 19:00:27 | reactions: 🔥 x1)
(And yes, the btc is still available before you fire any questions).
----------------------------------------------------------------------------------------------------
[#66596] 2026-07-12 21:12:48
(edited 2026-07-13 09:49:57 | reactions: 👍 x1)
  -> replying to #66594 Σ⸙ꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋꠋᅠᅠᅠ𓆈⃤ (user7731476133): Bip360 is a good step forward against quantum computing, but unless you're talking to developers that are passionate about actually working on it, regular peop...
A nation state will at some point hack the currently lost coins, and then keep OR sell it.
----------------------------------------------------------------------------------------------------
[#66600] 2026-07-12 21:17:49
(edited 2026-07-13 02:20:06 | reactions: 😁 x2)
  -> replying to #66599 Martín (user122813939): sorry, but what is the point on saying this? Nobody knows how to solve and much less about this.... will only hook more ppl up
Some already found it. And understood not to risk it... 🤐
----------------------------------------------------------------------------------------------------
[#66604] 2026-07-12 21:20:51
(edited 2026-07-12 21:21:08 | reactions: ❤ x3)
Iykyk
----------------------------------------------------------------------------------------------------
[#66606] 2026-07-12 21:22:37
(edited 2026-07-12 21:22:50 | reactions: 😁 x2)
  -> replying to #66605 Martín (user122813939): 👍👍 good luck with your alcohol
Thanks, already nearly sober again. It's only alcohol, not lsd or ayahuasca with mao-inhibitors.
----------------------------------------------------------------------------------------------------
[#66609] 2026-07-12 21:29:54
(edited 2026-07-12 21:31:09 | reactions: 🤝 x6, 🍾 x2, ❤ x1, 😁 x1, 🎉 x1, 🐳 x1)
Going dark again. Might be in a specific Ibiza club the 15th. HI, ciao and cheers you all ❤️!
----------------------------------------------------------------------------------------------------
[#66884] 2026-07-16 18:06:17
(edited 2026-07-17 01:47:17)
  -> replying to #66699 Nesso (user417022692): @SoWut we'll see you there
Where were you?
----------------------------------------------------------------------------------------------------
[#66889] 2026-07-16 18:08:35
Hello
----------------------------------------------------------------------------------------------------
[#66891] 2026-07-16 18:09:35
(edited 2026-07-16 18:18:41 | reactions: 😁 x3)
I saw people were waiting for drunk me.
----------------------------------------------------------------------------------------------------
[#66893] 2026-07-16 18:10:17
Hmm. Meta hunting. Like it.
----------------------------------------------------------------------------------------------------
[#66898] 2026-07-16 18:12:02
Had my eyes closed, but still saw double.
----------------------------------------------------------------------------------------------------
[#66903] 2026-07-16 18:19:17
(edited 2026-07-16 18:20:35 | reactions: 🔥 x1)
  -> replying to #66901 Nesso (user417022692): I'm very shy, so I didn't dare speak to you - though I did spend the whole night looking for your laptop😂
Well, it's hidden in a room with a hidden door.
----------------------------------------------------------------------------------------------------
[#66904] 2026-07-16 18:20:06
  -> replying to #66899 Thunder (user874768682): Do you also find it hard to get going in the morning after events like that?
Nah, I'm quite practiced.
----------------------------------------------------------------------------------------------------
[#66906] 2026-07-16 18:21:40
I should ask AI in this state.
----------------------------------------------------------------------------------------------------
[#66909] 2026-07-16 18:25:32
Imagine a piggy bank that only opens with a super-secret password. Right now, most piggy banks show a little part of the lock on the outside, and a future quantum computer could steal that part and crack it.
BIP 360 is a new kind of piggy bank: it hides the whole lock inside. You only see a 32-byte hash, no key visible at all. When you want to open it, you prove you know a secret path inside that hash. Safer against future quantum hackers.
----------------------------------------------------------------------------------------------------
[#66910] 2026-07-16 18:26:05
(edited 2026-07-16 18:26:14 | reactions: 😁 x1)
AI knows how to explain it to my level.
----------------------------------------------------------------------------------------------------
[#66912] 2026-07-16 18:26:27
(edited 2026-07-16 18:57:36 | reactions: 😁 x1)
  -> replying to #66908 3.14159265358979323846264338327950288419716939937510 0b1one|58209749445923078164062862089986280348253421170679 (user7895551210): thats not a wise move
🤫
----------------------------------------------------------------------------------------------------
[#66913] 2026-07-16 18:26:44
(edited 2026-07-16 18:26:48 | reactions: 😁 x1)
  -> replying to #66911 Spike (user1625609648): I too know the secret code "ELI5".
ELI4.5 is meta.
----------------------------------------------------------------------------------------------------
[#66931] 2026-07-16 18:32:30
  -> replying to #66917 Spike (user1625609648): I don't think fractions can be prime.
You have to be in your prime for that.
----------------------------------------------------------------------------------------------------
[#66935] 2026-07-16 18:33:29
(edited 2026-07-16 18:33:57 | reactions: 😁 x2)
  -> replying to #66918 PoW (user546901636): What will come fast? Quantum computer cracking the puzzle address or AI proving that there is no solution for the puzzle?
Quantum computers AND AI, both not being sure what to answer.
----------------------------------------------------------------------------------------------------
[#66938] 2026-07-16 18:36:07
(edited 2026-07-16 19:00:41 | reactions: 😁 x1, 🤝 x1)
  -> replying to #66907 Thunder (user874768682): Are you planning to start another project after gsmg?
Well. I've been doing this life enjoying project for a while. Quite ego-centric. But in a matrix cypher kinda way I like it.
----------------------------------------------------------------------------------------------------
[#66940] 2026-07-16 18:36:59
(edited 2026-07-16 18:37:06 | reactions: 😁 x1)
Nah, ketamine is immune to me by now.
----------------------------------------------------------------------------------------------------
[#66944] 2026-07-16 18:39:07
(edited 2026-07-16 19:01:16 | reactions: 😁 x1)
I think I do have the answer to an nearly optimal drug setup... in case anyone here would be interested.
----------------------------------------------------------------------------------------------------
[#66948] 2026-07-16 18:40:39
(edited 2026-09-01 19:47:50)
Brb 🤖
----------------------------------------------------------------------------------------------------
[#66951] 2026-07-16 18:44:11
(edited 2026-07-16 18:44:26 | reactions: 👍 x1, ? x1)
Around for so long, never heard of it. Thanks.
----------------------------------------------------------------------------------------------------
[#66961] 2026-07-16 18:50:15
(edited 2026-07-16 18:50:26 | reactions: 🔥 x2, 🤔 x2)
Give yourself yourself and yourself will be given yourself.
----------------------------------------------------------------------------------------------------
[#66962] 2026-07-16 18:51:10
(edited 2026-07-18 08:10:03 | reactions: 😁 x1)
  -> replying to #66958 Anderson Vasconcelos (user24791610): Waiting for the "NOTE: that is a hint." moment
Latetly, I'm working with many NOTES.
----------------------------------------------------------------------------------------------------
[#66964] 2026-07-16 18:52:37
  -> replying to #66955 n04oh (user5386650593): I really like Clonazepam
Nice
[photo 997x1280]
----------------------------------------------------------------------------------------------------
[#66969] 2026-07-16 18:54:07
(edited 2026-08-23 07:19:52 | reactions: 🦄 x1)
What about 70mq lsd, 100 mg mdma and bit of ket on the end?
----------------------------------------------------------------------------------------------------
[#66976] 2026-07-16 18:56:18
And in Dutch its called "geestveruimend". Implying those who dont take drugs are... simpleminded...
----------------------------------------------------------------------------------------------------
[#70307] 2026-09-01 07:49:57
(edited 2026-09-01 07:56:32 | reactions: 🔥 x9)
Pfff. Coincidence.
----------------------------------------------------------------------------------------------------
[#70309] 2026-09-01 07:57:32
(edited 2026-09-01 08:04:11 | reactions: 🤝 x5, ❤ x1, 🥰 x1, 🦄 x1)
To you, and all those that have send me kind words for the monstrosity I decided to build a few years ago. Thanks ❤️.
----------------------------------------------------------------------------------------------------
[#70311] 2026-09-01 08:01:50
(edited 2026-09-01 08:06:35 | reactions: 👏 x1, 🎉 x1, ? x1)
A. I rushed (t)it.
B. Yes, have quite some time for stupid stuff.
----------------------------------------------------------------------------------------------------
[#70317] 2026-09-01 08:17:44
  -> replying to #70314 Sell The Dip (user928105459): no one should click random links here
👆
----------------------------------------------------------------------------------------------------
[#70322] 2026-09-01 08:27:03
(edited 2026-09-01 08:27:09 | reactions: 🫡 x2, ❤ x1, 🔥 x1, 🤝 x1)
Fairly sober ;-)
----------------------------------------------------------------------------------------------------
[#70325] 2026-09-01 08:32:41
🤐
----------------------------------------------------------------------------------------------------
[#70327] 2026-09-01 08:33:19
(edited 2026-09-01 08:55:08 | reactions: 👍 x1)
  -> replying to #70319 Lexane (user5116466152): Hi, Jrk. Glad to see you. Having fun?
Always a joy
----------------------------------------------------------------------------------------------------
[#70334] 2026-09-01 08:40:27
(edited 2026-09-01 09:25:53 | reactions: 👌 x1)
Enjoying life
----------------------------------------------------------------------------------------------------
[#70336] 2026-09-01 08:40:54
(edited 2026-09-01 08:56:09 | reactions: 😨 x4, ❤ x1)
Couple hours, and no.
----------------------------------------------------------------------------------------------------
[#70377] 2026-09-01 11:41:20
(edited 2026-09-01 11:45:11 | reactions: 👍 x1)
  -> replying to #70373 Sparky (user7184569562): Was it not "spent two sloppy days throwing one together" a few months ago?
Same same
----------------------------------------------------------------------------------------------------

====================================================================================================
CREATOR ADMIN / SERVICE ACTIONS (18)
====================================================================================================
[#65] 2019-04-20 09:36:06  join_group_by_link
[#997] 2019-05-31 11:30:20  invite_members
[#4164] 2020-05-22 21:12:51  remove_members
[#4165] 2020-05-22 21:12:59  remove_members
[#4166] 2020-05-22 21:13:06  remove_members
[#4167] 2020-05-22 21:13:13  remove_members
[#4168] 2020-05-22 21:13:22  remove_members
[#4170] 2020-05-22 21:13:33  remove_members
[#4178] 2020-05-22 21:36:28  remove_members
[#4179] 2020-05-22 21:36:33  remove_members
[#4180] 2020-05-22 21:36:38  remove_members
[#4186] 2020-05-22 23:55:32  remove_members
[#4187] 2020-05-22 23:55:39  remove_members
[#4188] 2020-05-22 23:55:44  remove_members
[#4189] 2020-05-23 00:04:59  invite_members
[#4304] 2020-05-23 15:50:20  remove_members
[#4305] 2020-05-23 15:50:26  remove_members
[#4306] 2020-05-23 15:50:30  remove_members
```
