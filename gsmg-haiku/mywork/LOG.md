# Work log (mywork/)

Tooling: lib.py (EVP_BytesToKey/AES-CBC decrypt, pure-python secp256k1 + hash160 checker).

1. verify.py: key 1 -> 751e76e8...3bd6 (compressed) OK; README pubkeys hash to both target hash160s OK;
   phase2 / phase3 / phase3.2 containers decrypt with the documented answers (648 / 4090 / 2422 bytes; 1.00 / 1.00 / 0.60 printable).
2. pool_search.py: ~40k candidate strings (all 1..8-word n-grams of page text, derived plaintexts, SalPhaseIon decodes, known answers; as-is,
   lower, upper, with/without spaces) x 9 password transforms (sha256-hex [documented], raw, sha256-HEX, sha256(hex-of-sha256),
   raw 32-byte digest, sha256(raw digest) hex, sha512 hex, sha1 hex, md5 hex) x {terminal, salphaseion-short, cosmic-duality}.
   Control: phase3.2 container included; search recovers its known answer (twice: sha-hex of answer, raw of the hex). 20 s runtime.
   Result: no hit with >85% printable plaintext on any of the three unopened containers.
3. matrix_exp.py: SalPhaseIon textarea runs of 91 and 570 letters a-i (-> digits 1-9) arranged in every matrix shape, row/column sums
   read as ASCII or mod-26 letters. Nothing meaningful.
4. 2026-10-07, hint-order pass (official 2023-02-23 list: yellow blue primes matrixsumlist lastwordsbeforearchichoice yinyang).
   Verified facts: live SalPhaseIon textareas byte-identical to files/salphaseion_phase3.html (puzzlehunt#108 "two typos" is false);
   gsmg.io/89727c59... (SalPhaseIon URL) = sha256("GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"), i.e. the
   2021-05-06 hint is the access path, not a password; puzzle.png off-palette pixels are only the FEFEFE cell (row 7, col 4) and
   the anti-aliased red caption row (y 1047-1061) - no red-plane payload (puzzlehunt#20); no 74c974e3 blob exists in the kit.
   False positives confirmed (padding-valid, printable 0.24-0.46, count = chance rate): puzzlehunt#108/#17 "K_C1/K_S1" chain
   (salphaseion-short + MD5 + 'matrixsumlistenter...matrixsumlist'; terminal + MD5 + WIF 5K2by...), Anvexis master key a795de11...
   (cosmic + MD5 raw digest -> the 1327-byte blob), Naddiseo#13 Bifid/BTCSEED strings.
   Negative sweeps (all three containers, EVP md5/sha1/sha256, raw / sha256-hex / digest / double-sha): issue-thread strings
   (1035), 2021-05-06 string family (810, also as sha256 private key -> 1JX13G3cfWJgqpEfiTaksnN9RRAQKbH6et, not target),
   hint-ordered Phase-3-style concatenations of candidate token answers (100,799 strings, 1.81M trials, 6,925 pad-valid vs
   7,087 expected). Prime-indexed letters of r1 (pi(91)=24) and r2 (pi(570)=104, = length of the matrixsumlist run) are
   uniformly distributed over a-i; parity/isprime bit readings and dec->hex are not text.
5. Zeroing-mask search on r2 (and r1): masks = all 2^9-1 letter-value subsets x positional classes (prime/non-prime positions
   0/1-based, i mod m for m=2..10, poster spiral bits 0/1, poster Y/B/not-Y/B cells tiled, row-major bits), each applied as
   zero-out or remove, decoded via the z-section scheme (decimal -> hex -> bytes) plus 2- and 3-digit ASCII groupings; control
   decode of t[766:829] -> 'lastwordsbeforearchichoice' and poster spiral -> 'gsmg.io/theseedisplanted' verified in-run.
   ~53k decodings; only 9 contain even one 3-letter dictionary word (single word inside binary noise = chance). Negative.
   Note: 'pairs' decoding after removing a/b is trivially printable (digits 3-9 pair to 33-99) - do not score it by printable ratio.
6. Matrix-sum-list-derived masks on r2 (570 digits). Sum lists used (36): poster row sums [6,10,8,7,6,6,5,4,9,9,7,8,7,9], poster
   col sums [8,10,8,10,8,7,3,6,7,5,9,6,6,8], their concatenations, and r2's own row/col sums for every divisor shape
   (2x285 ... 285x2) plus r1 as 7x13 / 13x7. Masks per list: cumulative-sum positions (once and cycled), digit == sum mod 10,
   digit > sum mod 10, prime-valued / even-valued sums (tiled), digits present in the list, and for r2 shapes: cells in
   prime/even-sum rows and columns, row+col sum prime/even. Each applied as zero / remove / keep, decoded dechex / pairs / triples,
   dictionary-word scored: 4,353 decodings, best = 1 three-letter word in binary noise. Negative.
   Password test: the sum lists themselves (digits joined with '', ' ', ',', as letters, mod-10 digits, hex of the integer; sorted
   and reversed), digit sums, r1/r2 as integers/hex, with hint-order prefixes/suffixes (yellowblue..., matrixsumlist,
   lastwordsbeforearchichoice, yinyang) x case x 5 KDF input forms x md5/sha1/sha256 x 3 containers: 812,925 trials,
   3,099 pad-valid vs ~3,176 expected (chance), best printable 0.57. Negative.
7. "Four keys" test: the four verified stage answers (Phase 1 'theflowerblossoms...', Phase 2 'causality', Phase 3 227-char
   concatenation, Phase 3.2 'jacquefresco...') and their sha256-hex passwords. All ordered subsets (1-4) joined with
   '', ' ', newline, '|', '+', ',' in answer / password / lowercase / interleaved answer+password form, with and without
   hint tokens (matrixsumlist, lastwordsbeforearchichoice, thispassword, yinyang, theseedisplanted) prefixed or suffixed
   (14,885 strings) x 7 KDF input forms (raw, sha256 hex/digest, double sha256, md5, sha1, sha512) x md5/sha1/sha256 x
   3 containers; plus XOR of every subset of the four 32-byte digests and raw digest concatenations.
   939,771 trials, 3,758 pad-valid vs ~3,671 expected (chance), best printable 0.59. Negative.
   As private keys: the four digests, their XORs, sum and product mod n, and sha256 of all 14,885 strings (13,702 keys)
   -> none produce the target hash160s. Negative.
8. 2026-10-08 (scripts in mywork2/: stats.py, zero_tail.py). Statistics of the a-i runs:
   r1 (91): a3 b25 c8 d4 e18 f10 g10 h8 i5; 'a' always followed by 'b'; 'be' x10, 'bf' x6. Digit sum 422.
   r2 (570): a54 b49 c52 d49 e69 f57 g107 h58 i75; digit sum 3079; close to unigram-iid, mild drift toward h/i in the second half.
   Observation: six of nine r2 letters sit at ~57 = 570/10 and g carries ~50 extra, i.e. the shape of a uniform decimal string
   whose zeros were rewritten as g ("some characters need to be zeroed out").
   Test: tail-first search (N mod 2^8k depends only on the last 8k decimal digits) choosing which g / i / e / gi / ge / gie
   occurrences are zeros, decimal -> hex -> ASCII, forward and reversed, for r1 and r2. Control (lastwordsbeforearchichoice
   with o->g) recovered in 8 nodes. Result: most branches die within 1-3 lowercase bytes; the deepest (r1 reversed, zeros as g/i/e) reached 7 bytes 'uoijgch'
   (zero_tail.out:69), and three runs stopped at the 300,000-node cap, so they are truncated, not exhausted (zero_tail.out:14,19,34)
   [corrected 2026-10-14]; printable-only branches are
   chance-rate noise. Negative for "zeros disguised as one of g/i/e". Not tested: zeros deleted (insertions), other bases.
   Also negative: base-9 (a=0, bijective, reversed) -> bytes; r1 as chunk-length list for r2 (sum 422 != 570); g/i/e as
   separators in r2 (token lengths geometric); r1 through 9-column checkerboards (selectors 25/256/12/14) keyed by
   shabef..., fubcd..., and the decoded page words.
9. 2026-10-08 (mywork2/zero_insert.py). Deleted-zeros variant: r = decimal number with zeros removed. Tail-first beam search
   (beam 4000, <=3 inserted zeros per 8-digit window, lowercase-only bytes, quadgram score + binomial zero prior).
   Controls: both z-sections with 'o' stripped are recovered as the top solution (lastwordsbeforearchichoice, thispassword).
   r1 / r1 reversed: no complete lowercase decoding. r2 / r2 reversed: beam survives only as quadgram-plausible gibberish
   ("...thisdononstheesationthatorstatesectdefortedisdictm"), no real words, no complete decoding. Negative.
   [2026-10-14: that string is not in the saved zero_insert.out, which may be from the rerun noted in entry 10.]
   Caveat: with up to 3 free zeros per byte ~9 lowercase branches survive per step, so the beam can always build
   pseudo-English; a true path could in principle be crowded out. Mixed-case / spaces / punctuation not tested.
10. 2026-10-08 (mywork2/zero_mixed.py, zero_mixed_ins.py, zero_longctl.py). Zero hypotheses with full printable ASCII
   (mixed case, spaces, punctuation), interpolated char 4-gram model, state key = (pos, text, window value, carry).
   NOTE: entry 9's script merged states with equal text but different carry (bug; its controls passed by luck). Fixed and
   rerun: entry 9's lowercase negatives stand.
   Controls (all recovered as top solution): 65-char mixed-case sentence, insert (beam 20000) and replace-gie (beam 3000);
   236-char / 568-digit sentence (same size as r2), insert and replace-gie.
   Results: r1, r1 reversed, r2, r2 reversed x {zeros deleted, zeros written as any of g/i/e}: no complete printable
   decoding; beams hold only n-gram-plausible gibberish. Negative.
   Scope: decimal -> big-endian bytes -> ASCII only (the z-section scheme). <=3 deleted zeros per 8-digit window.
11. 2026-10-08 (mywork2/zero_enc.py, zero_codes.py, zero_bases.py). Zero hypotheses with OTHER target encodings.
   a) Big number, tail-first beam (zeros deleted <=3 per window / zeros written as g,i,e / no zeros), r1, r1rev, r2, r2rev:
      little-endian bytes ASCII; big-endian bytes as EBCDIC cp273; 7-bit ASCII groups big- and little-endian.
      Controls (236-char sentence, insert and replace) recovered as top solution in all four encodings.
      Result: no complete printable decoding anywhere, except one gibberish hit (b7, r1, insert, -2.03/char vs control -1.3).
   b) One code per character, best segmentation under 4-gram model vs 8 shuffles of the same string:
      A1Z26, A0Z25, decimal ASCII (a-z+space, and 32..126), modes plain / zeros deleted / g,i,e as zero.
      Controls decode (acc 0.76-1.00; a0z25-insert control only 0.22 = that variant is too ambiguous to test).
      A1Z26/A0Z25: r1 and r2 scores inside the shuffle range (no signal). Decimal ASCII: no segmentation exists at all.
   c) Whole number -> base 26 (a=0, bijective a=1), 27, 36, 58, 64, 85, 94, 95 text, zeros = any subset of g/i/e:
      0 dictionary-word hits (>=5 letters) for r1, r1rev, r2, r2rev; 1 chance hit ("hence") for r1+r2. No control needed
      (deterministic conversion). Deleted zeros NOT testable here (not tail-separable).
   d) Position-class chi2 for periods 2..12 on r1 and r2: all ~= degrees of freedom -> no fixed-width code structure.
   All negative. No container decrypted.
12. 2026-10-08 review (mywork2/block765.py, r1_ic.py).
   a) Blocks t[:765] (=9*85=15*51), r1, r2, r1+r2, ab+r2, r1+ab as matrices of every divisor shape, digits masked
      (all / primes 2357 / primes+1 / non-primes / composites zeroed-out), row and column sums -> ASCII, A1Z26, mod 26:
      806 decodings, best = 1-4 short dictionary words in noise. Negative.
   b) r1 parsed as straddling checkerboard, every 1-3 selector set, index of coincidence vs 300 shuffles of r1:
      selectors b,e -> 63 symbols, 19 distinct, IC 0.0671 (rev: 16 distinct, IC 0.0722); shuffle median 0.057, percentile
      0.96 / 1.00. English IC ~0.066. Lead stands: r1 looks like a monoalphabetic checkerboard text of 63 letters.
      Only keyed alphabets (Phase 2 alphabet, shabef..., page words) were tried so far; no free substitution solve.
   Decision: next = free substitution solve of the 63 b/e-checkerboard symbols (hill-climb + crib dragging, with a
   same-length positive control), then use any plaintext on the salphaseion-short container.
13. 2026-10-08 (mywork2/subsolve.py, try_sub.py). Free monoalphabetic solve of r1's 63 b/e-checkerboard symbols.
   Solver: simulated annealing (8000 steps, injective symbol->letter map), interpolated letter 4-gram model
   (pydoc topics + Python NEWS/LICENSE + Matrix/puzzle texts). Null = same symbols in shuffled order.
   Controls (5 unseen 63-letter English texts, random substitution, 60 restarts): accuracy 1.00 / 1.00 / 0.98 / 0.90 / 0.52;
   found scores -117.7..-140.1; their shuffle nulls -142.6..-160.3 (every control above its null).
   r1 (150 restarts): fwd -146.6, fwd reversed order -149.4, rev -151.9, rev reversed order -150.7;
   nulls (20 shuffles, 20 restarts) span -156.2..-138.8. r1 is inside the null -> no English solution. Output is gibberish.
   Crib drag (yellow, blue, primes, privatekey, password, yinyang, matrix, sumlist, lastwords, architect, choice, thekey,
   cosmicduality, wewont): pattern-consistent placements solved with the crib fixed; best -157.6 (worse than free solve).
   privatekey, yinyang, architect, cosmicduality fit nowhere.
   Structure: 9 adjacent identical symbol pairs of 62 and one triple ('c c c') - English expects ~2 and no triple.
   40 solver outputs x {sha256-hex, raw, sha256-hex of upper} x {sha256, md5 KDF} x 3 containers: 720 trials, 0 hits.
   Negative: r1 under the b/e parsing is not a simple substitution of English. The IC 0.067 is unexplained (doubles-heavy).
14. 2026-10-08 candidate test on all three unopened containers (scripts in the session scratchpad, not the project).
   Candidates: yinyang, ying yang, yin yang, yin-yang, theyinyang, cosmicduality, the derived Architect text
   (derived/architect-text.txt), and the derived checkerboard plaintext (derived/checkerboard-plaintext.txt). Each as-is,
   lower and upper case, as password = sha256-hex and = raw sha256 digest; EVP_BytesToKey SHA-256, 1 iteration.
   48 decrypts per container. Control: phase2.b64 with password sha256-hex('causality') opens, printable 1.00.
   Result: cosmic-duality.b64, terminal.b64, salphaseion-short.b64: no hit above 0.85 printable. Negative.
   Entries 4, 6, 7, 13 already covered several of these as prefixes, crib, or pool members; this entry adds the
   standalone phrase variants that were not previously run as whole passwords.
15. 2026-10-08 checks (scratchpad, read-only).
   a) ECDSA nonce reuse: 16 signed inputs spent from 1GSMG1JC9... and its outgoing targets 17ucy1K9... and 3GSMG24...
      (mempool.space). No duplicate r values, so no key recovery from reused nonces.
   b) Poster grid re-sampled from files/puzzle.png (14x14, K/B=1, W/Y=0). Spiral reading reproduces
      gsmg.io/theseedisplanted (printable 1.00). Row-major and column-major, forwards and backwards: noise
      (printable 0.17-0.42). Negative for a vertical or column message in the bit grid. Rows 5-7 are rabbit-covered.
   c) Comments and hidden fields: saved pages have none beyond Wayback markup. Live Phase 1 comment
      "Nice to see you around! Good luck little bunny hunter ;)" and live Phase 2 comment "You made it to the next
      step! ..." are flavour text. The raw Phase 1 _token is a form token, not key material. Live SalPhaseIon: none.
16. 2026-10-14 reproducible rerun of entry 5 (mywork2/yb_counts.py, mywork2/prime_zero.py, outputs .out/.json beside them).
   a) Poster colours recounted from files/puzzle.png (75 px cells, majority RGB): B=15, Y=9, F=1 (off-white, spiral
      index 163), grid identical to scratchpad_grid.txt. All 24 B/Y cells sit on spiral index 7 mod 8, and B=1/Y=0 equals
      the low bit of each byte of gsmg.io/theseedisplanted. Confirms mywork2/web/unverified_phase0_yellow_blue_counts.md.
   b) Masks = 113 position classes (all, prime and non-prime 0/1-based, prime(i+9/15/24), i mod m for m=2..10,15,24,
      spiral and row-major poster bits and B/Y cells tiled, the 24-bit B/Y string tiled) x 511 letter subsets x
      zero/remove, on r1, r2, both reversed, r1+r2 and r2+r1: 487,725 distinct masked strings. Decoders: dechex
      (scored by longest a-z run), A1Z26 pairs and ASCII triples (scored by English word coverage).
   c) Controls passed in the same run: both known a-i,o runs decode; their zeros hidden as a letter ('a' on i%5==1,
      'e' everywhere) and an inserted-letter removal case are each recovered at rank 1 out of 8-22k masks.
   d) Result: best dechex run is 5 letters for r1 and 7 for r2, the same as the shuffled-run null (5 and 7). No
      English word coverage above 0.014 for pairs or triples. 1,412 top decodes tried as STD answers on terminal and
      salphaseion-short: 0 structured hits. Negative for this mask family.
