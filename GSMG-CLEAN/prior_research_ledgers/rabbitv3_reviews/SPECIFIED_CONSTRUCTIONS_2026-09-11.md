[inferred] The strongest remaining obstacle is an unbound translation: the prime parse and native poster nearly agree, but the source does not specify how to handle their disagreement. A transformation that repairs that disagreement is not evidence of the intended rule. In particular, the observed relation does not uniquely select ASCII 127 or deletion.

[verified] I froze six constructions before executing their bounded tests. The specification SHA256 is `0dbe1a59d550236b5ef755b59313c589543e636c2aa6cb204e0aa26210caa59e`. Both native-concordance constructions failed their independent predictions. The cryptographic controls passed. No unresolved-stage password combinations were retested and no prize key was found.

**Source coordinates and reproducibility**

[verified] All intervals below are zero-based and half-open. H, A, F, C, R2 and R3 ranges refer to original file bytes; their cited ASCII passages have identical character offsets. S is a reversible lexical index into H: it retains every original symbol and every separator, and is not a whitespace-normalized password. T ranges refer to the reconstructed text of the identified Telegram message, preserving its text. P coordinates refer to native image pixels; bit and row/column coordinates are zero-based, marker numbers one-based.

| Alias | Exact source |
|---|---|
| H / S | [Original SalPhaseIon HTML](E:/rabbitv3/rabbit/sources/pages/salphaseion_phase3.html); first textarea H[477:2626], 1,075 symbols with separator ledger |
| P | [Native poster](E:/rabbitv3/rabbit/puzzle.png); board x[0:1047), y[0:1047), within the 1048×1556 PNG |
| A | [Rewritten Architect plaintext](E:/rabbitv3/rabbit/analysis/out/reproduced_originals_2026_09_10/architect_exact_letters.txt), bytes[0:1539] |
| F | [User-supplied film transcript](E:/rabbitv3/rabbit/sources/community/matrix_reloaded_architect_user_supplied_2026-09-10.txt), bytes[0:5531] |
| C | [Checkerboard plaintext](E:/rabbitv3/rabbit/analysis/out/reproduced_originals_2026_09_10/checkerboard_exact_letters.txt), bytes[0:91] |
| R2 / R3 | [Phase 2](E:/rabbitv3/rabbit/evidence_review_2026-09-10/exact_text/phase2_decrypted.txt), bytes[0:648]; [Phase 3 riddles](E:/rabbitv3/rabbit/evidence_review_2026-09-10/exact_text/phase3_riddles.txt), bytes[0:726] |
| T | [Supplied Telegram export](E:/rabbitv3/newest-telegram-9.9.26/result.json); selected exact creator texts and attribution fields in [creator_sources.json](E:/rabbitv3/rabbit/analysis/out/specified_constructions_2026_09_11/creator_sources.json) |

[verified] Source hashes, exact segment offsets, the pre-test specification, implementation fingerprints, and measurements are saved in [sources.json](E:/rabbitv3/rabbit/analysis/out/specified_constructions_2026_09_11/sources.json), [specifications.json](E:/rabbitv3/rabbit/analysis/out/specified_constructions_2026_09_11/specifications.json), [implementation_before_tests.json](E:/rabbitv3/rabbit/analysis/out/specified_constructions_2026_09_11/implementation_before_tests.json), and [results.json](E:/rabbitv3/rabbit/analysis/out/specified_constructions_2026_09_11/results.json). The executable is [specified_constructions_2026_09_11.py](E:/rabbitv3/rabbit/analysis/specified_constructions_2026_09_11.py). F is a secondary transcript, not independently verified film audio. Some T messages have later edit timestamps; their contents do not establish their original publication wording.

**Unresolved-operation table, in priority order**

[speculative] These are chosen constructions for evaluation, not declarations of intended puzzle instructions. Verified outcomes and limits are explicitly distinguished in the final column.

| Operation and exact source range | Input type → output type | Candidate referent | Chosen rule | Falsification and observed result |
|---|---|---|---|---|
| P1: 23→24 translation; S[0:91] = H[477:658]; P spiral bits[0:192]; A[1089:1114], A[1157:1223] | Symbol tokens + RGB marker metadata → 24 records + native 14×14 integer matrix + inverse ledger | Prime boundaries close records; EOF closes the last record | Parse both b/be branches. Right-align each prime-terminated record in its corresponding eight-bit byte slot. EOF retains the trailing e in slot 24. Replace prime-token numeric values with zero, retaining original tokens in the inverse ledger | Reject any lost symbol, overflow, inverse failure, wrong record count, or mismatch to the complete first 23 native colors. [verified] 84-token branch has 24 records but fails marker 21; 83-token branch has 23 records and fails markers 21 and 23 |
| P1: meaning of zeroing; T #8000 text[0:354]; P bits163,167; URL byte[20:21] | URL bytes or logical integers → separately typed edited sequence + residual | Character/value/bit, with object unbound | Test deletion, zero substitution, zero insertion, XOR 0x11, prime-value zeroing, and numeric insertion separately; exact definitions below | [verified] Deletion/insertion violate fixed 24-byte alignment; zero substitution fails marker agreement; XOR 0x11 matches but is fitted to known discrepancies. [inferred] No cited source selects its two bits or uniquely licenses deletion |
| P2: matrixsumlist; S[91:195] = H[659:866] | P1 native 14×14 integer matrix → 14 integers → text | Native poster matrix, rows or columns | Freeze two axis alternatives: top-to-bottom row sums or left-to-right column sums; base-10 integers separated by one ASCII space, no newline | Reject the binding if no source selects the matrix/axis/serialization. [verified] Neither axis is uniquely bound; these are conditional outputs, not new password trials |
| P2: lastwordsbeforearchichoice; S[766:829] = H[2009:2134] | Exact F text → exact source slice | Architect's final literal choice, or his speech before Neo's first Choice | L2=F[4927:4965], including trailing space; L1=F[1473:1533], including period | Unique binding requires an occurrence and a boundary, not just a speaker. [verified] F has five choice occurrences, three spoken by Architect; A has none. Neither construction is uniquely selected |
| P2: thispassword and SHA; S[830:895] = H[2137:2266]; S[1063:1075] = H[2603:2626] | Matrix text + selected source text → assembled answer → SHA256 hex password | thispassword refers to assembled answer; final “ans too” refers to the next complete answer | Q=Mtext+L, no inserted delimiter; SHA256 of exact UTF-8 Q, lowercase hex ASCII for EVP. Downstream candidate hashes exact full SalPhaseIon plaintext as text for Terminal | Reject invalid UTF-8 or absence of an independent assembly/target binding. [verified] No unresolved AES trials executed. [speculative] Assembly, downstream target and serialization remain unbound; FAED has no operational binding in this partial AST |
| P2: enter; S[895:959], S[959:999], S[999:1063] = H[2267:2602] | Two 64-character Base64 runs → formatted envelope | Line break in the ciphertext, not answer text | Insert one LF between the two runs, then decode Base64 | Predicted exact equality with saved SalPhaseIon envelope. [verified] Equals its 96 bytes and SHA256 `9e2831e1b34b5f34796df47ccaf6530d48d371c61a6bff84d60db1064fa7a258`. [inferred] Formatting role is supported, but LF, CRLF and no separator decode identically |
| P3: discarded rabbit detail; P board x/y[0:1047), T #1710 text[31:123], S[0:91] | 70×70 fine binary cells + coarse bits → 196-bit parity mask → corrected bits | Fine detail corrects coarse marker colors | Per coarse cell, XOR each of its 25 fine blackness bits with modal coarse blackness; XOR all residuals; apply the parity to that coarse bit | Predict the entire 23-marker prime sequence, including marker21. [verified] Changes only bits187,194,195; marker21 at bit167 remains wrong. This specific projection is falsified |
| P4: personal/cultural selector; A/F/C/R2/R3 complete ranges above, T #66573[0:113], #66574[0:21] | Finite literal-reference corpus → occurrence/speaker/boundary concordance | One existing reference uniquely chooses an unresolved operation | Enumerate the fixed roster and every literal Choice/choice in F and SELECT/CHOICE in A. Require a unique binding before substituting selected text | [verified] Literal uniqueness fails; friends hint names none of the roster. [inferred] A semantic recognition bottleneck remains possible, but no specific referent has been identified |
| P5: cryptographic boundary; known envelopes and answers in reproduced-originals results; 2020 transaction input scripts | Exact text + envelope bytes → full plaintext; declared scalar bytes → point/address comparison | Previously successful envelope convention; advertised original prize point | Frozen SHA256-hex/EVP-SHA256/AES-256-CBC profile; exact scalar formats and uncompressed P2PKH | [verified] Three full known-answer controls and scalar boundaries pass. No new scalar or unresolved-stage solution is claimed |

**P1: the complete reversible construction and its failure**

[verified] The established poster traversal starts at top-left, moves down, right, up, left, and continues inward. It produces 196 bits; bits[0:192] decode `gsmg.io/theseedisplanted`, and bits[192:196] are four remaining zero bits. The 24 colored cells occur at bits 7,15,…,191, one per byte. Their native sequence is `BBBBYBBBYYBBBBYBBYYBYYBY`. This is a byte-boundary relationship, not a finding that the colored cells themselves occupy prime indices. [Source: P native board; results.json → branches → native24.]

[speculative] For each complete parse of S[0:91], assign one-based logical token indices. A prime-index token consumes b or be; nonprime indices consume one a–i character. End a record at every prime index, and close any residual record at EOF. Assign record j to poster byte j, right-aligning its tokens within eight positions. Encode nonprime a–i as integers 1–9 and prime-token values as zero. Empty leading positions and the four post-URL bits are explicitly structural zeros. This uses native byte width and poster geometry; it does not factor 60 or 61 into an attractive rectangle.

[verified] The 84-token branch has 23 prime-terminated records and one EOF record containing e. All 91 source characters survive. Its e is S[90:91], H[657:658], logical token84, record23, bit191, poster row5/column6, pixel rectangle x[450:525), y[375:450). Its numeric value is still 5. The matrix total is 341. The other branch consumes e as part of its last be prime token and has 23 records, not a separate EOF record. [Source: results.json → branches and source_ranges_and_limits.json → e_mapping.]

[verified] The inverse reads nonprime numeric matrix cells back into letters, restores prime tokens from the sidecar, and restores original separator bytes from [lexical_map.json](E:/rabbitv3/rabbit/analysis/out/specified_constructions_2026_09_11/lexical_map.json). Every S[0:91] character has an H byte offset, logical token, record, poster bit, row/column and pixel rectangle in results.json → branches → mapping. Prime be characters share their token coordinate. Original native marker24 and byte23 are retained separately. Round trips passed. A lossy substitution or deletion is reversible only together with its residual sidecar; the transformed data alone are not invertible.

[verified] The EOF rule predicts an independently checkable relation: all 23 prime colors must agree with the first 23 native poster markers. They do not: marker21 differs. Therefore this *unmodified-native concordance* construction is rejected, despite its successful bookkeeping. The EOF placement gives e a definite conditional role; it does not establish the creator's intended role. Native marker24 is yellow and belongs to URL byte23, d; e's numeric value5 is not the same data type as d's final bit0. No equality between them is asserted.

[verified] These numeric row and column sums are conditional outputs of that frozen construction:

```text
rows:    7 47 35 34 3 24 29 29 28 38 16 13 29 9
columns: 4 23 22 21 14 34 31 21 10 48 30 32 31 20
```

[verified] This board overlaps the existing zero-prime-marker, tail-left-padded-to-octet embedding in hint_model_audit_2026_09_10.json. The new work is its explicit EOF interpretation, complete source ledger and falsification, not a new matrix password search.

[verified] URL byte20 is n, decimal110. The marker21 bit is bit167, mask0x01 within that byte. The exceptional FEFEFE cell is bit163, mask0x10, at row7/column4 and pixels x[300:375), y[525:600). Thus the already-known alternatives are n XOR1 = o (111), n XOR16 = ~ (126), and n XOR17 = DEL (127). Matching prime-marker LSBs constrains mask1; it supplies no independent justification for mask16. The complete color match under XOR17 is fitted evidence, not a new success.

| Separate construction [speculative] | Exact forward rule | Output [verified] | Inverse and bounded falsification |
|---|---|---|---|
| Delete URL byte20 | U[0:20] + U[21:24] | 23 bytes; `gsmg.io/theseedisplated` | Store removed 110 and insert at20; rejects fixed 24-slot model |
| Zero URL byte20 | U[0:20] + byte(0) + U[21:24] | 24 bytes; embedded NUL | Store replaced110 and restore at20; marker21 still fails |
| Insert zero before URL byte20 | U[0:20] + byte(0) + U[20:24] | 25 bytes | Remove exactly the inserted byte20; rejects fixed 24-slot model |
| Flip two bits | U[20] XOR 0x11, all other bytes unchanged | 24 bytes; embedded DEL at20 | XOR0x11 again; marker match is insufficient because mask1 alone also fixes that relation |
| Zero prime-token values | On all84 logical values, set indices2,3,5,…,83 to0 | 84 integers; terminal value5 retained | Restore saved prime values; requires independent evidence identifying this representation as zeroing's object |
| Insert numeric zero before token84 | V[0:83] + [0] + V[83:84] | 85 integers; terminal5 shifts one slot | Remove index83; does not delete or zero the e |

[verified] T #8000 text[0:354] asserts primes and unspecified characters needing zeroing. It does not identify a byte index, token class, bitmask, deletion, insertion, or an omitted marker. [inferred] Zero substitution is closer to its wording than deletion, but even the representation to be zeroed remains unbound. There is no source evidence here that pins one of these operations as correct.

**P2: instruction scope and exact answer assembly**

[inferred] Ranked by source support: the enter formatting interpretation is strongest because of its location between Base64 runs; hashing an already-assembled answer follows the reproduced answer-hash convention; the intended matrix, its axis, text-selector boundary and final answer's target remain weaker bindings. This ranks evidential support, not likelihoods.

[speculative] The frozen partial AST is:

```text
M = P1-EOF native14x14 matrix
Mtext = join(" ", decimal(row_sums(M)))
    OR join(" ", decimal(column_sums(M)))
L2 = F[4927:4965]      # exact trailing ASCII space retained
L1 = F[1473:1533]      # exact final period retained
Q = Mtext + L         # no inserted delimiter
thispassword := Q
first_SHA := SHA256(UTF8(Q)).lowercase_hex_ASCII
enter := LF between S[895:959] and S[999:1063]
final_SHA := SHA256(UTF8(full_SalPhaseIon_plaintext)).lowercase_hex_ASCII
final_SHA_target := Terminal
```

[verified] L1 is the Architect's final complete sentence before Neo's first literal Choice, F[1542:1548]. L2 is the Architect's sentence prefix before his final literal choice, F[4965:4971]. The source slices preserve case, punctuation and spacing. Their exact values are stored in source_ranges_and_limits.json → selector_ranges.

[inferred] L2 has the more direct speaker reading of archichoice. It still requires interpreting last as the final choice occurrence and words as a sentence prefix. L1 instead binds the boundary to Neo's first Choice; this adds a different occurrence rule. Neither is uniquely supplied by the label. A contains SELECT at[1143:1149] and no CHOICE, so substituting the rewritten speech for the film does not resolve a literal choice boundary.

[speculative] Decimal-space serialization and concatenation in the AST are declared candidate operations, not source-licensed normalization. They create formatting for derived integers; they never strip or lowercase selected source text. The final SHA consumes a complete answer text, not an already-produced hex digest; no accidental double-hash alternative is tried. The downstream SalPhaseIon→Terminal binding remains speculative.

[verified] The AST is incomplete: S[195:765], H[867:2006], the FAED run, has no demonstrated operation here. No row selector, literal-label password or swapped concatenation was retested. The only P2 execution was the predeclared envelope-format compatibility check, saved in [enter_control.json](E:/rabbitv3/rabbit/analysis/out/specified_constructions_2026_09_11/enter_control.json).

**P3: information-loss inventory and independent test**

| Decoder / source | Preserved | Discarded or outside that decoder's input | Source-supported relationship and limit |
|---|---|---|---|
| [verified] Poster URL / P board | Modal coarse blackness: black and blue=1; white and yellow=0; 192 output bits | Distinction between blue/black and yellow/white, FEFEFE versus white, 25-subcell rabbit residual within each coarse cell, four terminal bits; poster below board is outside input | [inferred] T #1710[31:123] explicitly relates colors and returning to the first piece. It licenses comparison with the poster, not a specific XOR projection |
| [verified] Prime numeric extraction / S[0:91] | Logical token values and order | Without a ledger: which b/e characters formed be, prime-marker identities, token boundaries, separators, EOF e when a 60-value crop is used | [inferred] A[1089:1114] and T #8000 support considering prime reinsertion/zeroing. Exact placement and operation remain unbound |
| [verified] Binary/decimal label decoding / S[91:195], [766:829], [830:859], [959:999] | Decoded labels and enter | Original numeric representation, symbol separators, and positions relative to other streams if only labels are copied | [inferred] Their source positions support an instruction parse. Decoding names alone does not perform their operations |
| [verified] Reversed creator bitstream / T #8446 entire text | The complete bits under an index permutation | Nothing at the reversal step; extracting only its readable labels would discard the rest of the sentence | [inferred] Evidence for whole-stream reversal in that message, not bitwise complement of another artifact |
| [verified] Reproduced Architect/checkerboard outputs / A[0:1539], C[0:91] | Exact uppercase plaintext letters | Restored word spaces or film punctuation are not supplied by these outputs; they would be editorial additions | [inferred] Keep these text representations distinct from F |
| [inferred] Rebus reading and reported audio route | Semantic labels; community-reported audio result | Rebus interpretation does not retain all image detail. A channel difference alone loses common-channel information | [verified] Original audio was not independently reconstructed here; no exact loss audit or audio hypothesis was tested. Reaction clips cannot stand in for the missing source |

[verified] Complement, reversal and subtraction are different functions: complement C(b)[i]=1−b[i]; reversal R(b)[i]=b[N−1−i]; stereo subtraction D(L,R)[t]=L[t]−R[t]. C and R are self-inverse and lose no bits. D alone is not invertible; retaining R with D permits L=D+R under sufficiently wide lossless arithmetic. A spectrogram also loses phase unless retained separately. These definitions do not authorize transferring one operation to another artifact.

[speculative] The executed fine-detail construction used only the source-related pair of the first poster and prime-derived marker sequence. For each coarse cell, let r[j]=fine_blackness[j] XOR coarse_blackness for its 25 subcells. Let p=XOR(r[0:25]), and output coarse_blackness XOR p. Its predeclared second-artifact prediction was the complete 23 prime colors, including the disputed marker21. It did not use the FEFEFE color residual as an extra repair.

[verified] Nonzero fine residuals occur at spiral cells172,184,187,192,193,194,195; odd parity occurs only at187,194,195. Bit167 remains unchanged, so the predicted relation fails. [inferred] The marker21 coarse cell is flat: any within-cell residual rule satisfying f(0)=0 likewise cannot change it. A nonlocal map would need a separately specified, source-bound rule; the failed parity result does not supply one.

**P4: finite concordance and recognition constraint**

| Reference | Exact occurrence [verified] | Unresolved step it could constrain [speculative] | Uniqueness result |
|---|---|---|---|
| Architect / Neo | F Choice ranges[1542:1548], [1565:1571] belong to Neo; [2551:2557], [2595:2601], [4965:4971] to Architect | lastwordsbeforearchichoice speaker and occurrence | [verified] Five occurrences, not one; speaker alone leaves three |
| Rewritten source instruction | A[1010:1032] RETURNTOTHESOURCECODES; A[1089:1114] REINSERTINGTHEPRIMEBASICS | Data source and prime operation | [inferred] Puzzle-specific changes matter, but do not specify alignment or zeroing object |
| Film prime program / numbers | F[3465:3478] prime program; F[3539:3571] 23 individuals, 16 female 7 male; A[1157:1223] rewritten numerical clause | 23 prime markers split16/7 | [verified] Film supplies the same numbers. [inferred] Their reuse is not an independent numeric coincidence |
| Two doors | F[4748:4767] | Which choice endpoint to select | [verified] Does not name the desired occurrence or text boundary |
| Oracle | F[2378:2384] | Alternate speaker/choice context | [verified] No instruction selects it |
| Merovingian | R3[12:23] | Cultural identity within known riddles | [verified] No demonstrated binding to an unresolved matrix axis or operation |
| Cheshire / Alice family | R3[312:320] cheshire | Rabbit/navigation referent | [verified] Literal Cheshire occurrence; no uniquely determined traversal correction |
| HSM / Mr. Robot family | R2[198:205] eps3.4_; R2[24:33] keymakers | Cryptographic vocabulary / recognition | [verified] These exact references do not specify an alternative final KDF |
| Half/better half | C[48:65] HALFANDBETTERHALF | Pairing two specified representations | [verified] No operand pair or complement/subtraction operator is fixed |
| Jacque Fresco / Heisenberg | Known-answer manifest characters[27850:27862], [27905:27936] | Established recognition examples | [verified] These are known-answer inputs, not independent new derivations or instructions for the unresolved stage |

[verified] The full finite occurrence list is results.json → scope_and_concordance → concordance. The final row uses [the original reproduction manifest](E:/rabbitv3/rabbit/analysis/out/reproduced_originals_2026_09_10/results.json), with character rather than byte offsets explicitly indicated.

[inferred] T #66573[0:113], reinforced by #66574[0:21], supports recognition as a useful constraint, but does not identify what must be recognized. [verified] Its literal text names none of this finite roster. That fails the literal uniqueness test; it does not falsify a semantic or personal association. No new date, book, secret, or contact-based hypothesis was introduced.

**P5: frozen checker and controls**

[verified] [frozen_checker_2026_09_11.py](E:/rabbitv3/rabbit/analysis/frozen_checker_2026_09_11.py) has SHA256 `bf488dfb10bf6e3dbb3091dff9ad16c26727a641b71b05fed9b58368f855b588`. Its single profile is `GSMG-UTF8-SHA256HEX-EVP-SHA256-AES256CBC-PKCS7-v1`.

[inferred] The following compatibility convention is justified by the reproduced known envelopes, without asserting that every unresolved envelope must use it:

1. Exact answer string → UTF-8, no stripping, Unicode normalization, case conversion or appended newline.
2. SHA256 of those bytes → lowercase hexadecimal ASCII password, not the raw 32-byte digest and not the literal instruction label.
3. Envelope must begin Salted__; bytes[8:16] are the eight-byte salt. Ciphertext is bytes[16:end], a positive multiple of16.
4. EVP expansion: D0=empty; Di=SHA256(D(i−1) || password || salt), one digest iteration. Concatenate blocks; key=first32 bytes, IV=next16. No MD5, PBKDF2 or fallback profile.
5. AES-256-CBC; strict PKCS#7 block size16. Return the full plaintext. Valid padding never sets verified_solution=true.
6. Scalar representation must be declared beforehand: exactly32 raw bytes or exactly64 ASCII hexadecimal characters, big-endian. No whitespace removal, substring windows, mnemonic checks, WIF guessing or reduction modulo n; require1≤k<n.
7. Compute uncompressed04||x||y and compare the full point and Base58Check P2PKH address with version0, HASH160 and double-SHA256 checksum.

[verified] The target point is:

```text
04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559
```

[verified] It hashes to `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`. Source: [2020 transaction 2aa9a4…](https://mempool.space/tx/2aa9a4a90be819d5122d70c993280785a0508f163521e7b38cebb4db0b071b13), input0 scriptSig decoded bytes[74:139]; input1 repeats bytes[74:139] and input2 repeats bytes[73:138]. The raw transaction objects are preserved in [the address transaction snapshot](E:/rabbitv3/rabbit/analysis/out/pattern_review_2026_09_11/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe-transactions.json), with checks in [chain-key-checks.json](E:/rabbitv3/rabbit/analysis/out/pattern_review_2026_09_11/chain-key-checks.json). The scalar checker is bound to this original advertised point, not an arbitrary derived empty address or the later halving destination.

[verified] Three known complete answers reproduced the complete expected plaintext hashes. Appending a space did not reproduce those expected plaintexts. Scalar1 and n−1 reproduced G and −G; zero and n were rejected; a newline after64 hex characters was rejected. The uncompressed G address control and advertised-point address check passed. These controls validate implementation compatibility, not any speculative matrix answer. See results.json → checker.

**First transformation and what remains undetermined**

[inferred] The first transformation to execute was the EOF-aware, reversible prime-to-native-byte alignment, and I executed it first. It directly addresses the highest-priority missing translation, uses native geometry, retains all source characters and e=5, and predicts agreement with a second artifact before touching AES. Its failed marker21 prediction now provides a concrete boundary: the plain alignment is insufficient.

[inferred] The next admissible change must be a source-derived rule that uniquely specifies what happens at bit167 and why marker24 has a different role. That rule must also explain whether bit163 participates. Merely choosing a mask that forces the known colors is circular. More matrix hashing cannot resolve that ambiguity.

[verified] I could not determine the intended zeroing representation, the creator's role for e=5 or marker24, a unique matrix/axis/serialization, the intended Architect selector boundary, the operational role of FAED, the final SHA target, or a unique personal/cultural referent. I did not independently validate the original audio. The frozen constructions and failed predictions narrow these uncertainties; they do not solve them. No new stage or key is claimed, and no candidate has matched the prize public point and address.
