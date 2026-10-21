# GSMG.io hidden-puzzle research report

Generated 2026-09-12 (America/New_York)

## Executive findings

This investigation expanded the supplied 403-record archive file into a broader, source-qualified inventory and then recovered the most promising historical bodies, code, images, and off-site puzzle artifact.

The strongest findings are:

1. **The supplied 403 URLs did not simply “go somewhere.”** On a fresh GET test, 19 returned HTTP 200 and 384 returned HTTP 404. Much of the old application has been removed or replaced. Historical HTTP 200 records also include arbitrary-path Vue fallbacks, so a 200 capture is not proof that a named puzzle page ever existed.
2. **The archive census is larger than the supplied file.** A Wayback domain query returned 2,994 capture rows representing 831 exact original URL strings across eight hosts. Public urlscan records add nine exact strings, mostly case/scheme/fragment variants, typos, or solver probes. The combined observed set is 840 exact strings.
3. **Certificate Transparency adds three historical host candidates** not present as Wayback hosts: `api.gsmg.io`, `api-staging.gsmg.io`, and `openpgpkey.gsmg.io`. They currently have no A or CNAME response, no public urlscan result, and no archived path evidence. Adding their qualified HTTPS roots produces 843 observed-or-inferred candidates.
4. **Only a small group of routes has recovered puzzle-bearing evidence:** lowercase `/puzzle`, `/theseedisplanted`, the long `choiceisanillusion...` route, and the 64-hex-character route beginning `89727c...`. `/phase1verification` is verified as the seed page's POST target, but its archived GET response is only the generic trading-app shell.
5. **The original Decentraland clue is still recoverable from a primary, content-addressed source.** Decentraland's Catalyst content API returns the scene deployed at parcel `-41,-17` on 2020-02-20. The scene entity, metadata, compiled code, and MP3 all reproduce their advertised CIDv0 hashes exactly.
6. **The audio message is verified.** Subtracting the right channel from the left and plotting a spectrogram reveals hexadecimal bytes `48 41 53 48 54 48 45 54 45 58 54`, which decode to `HASHTHETEXT`.
7. **The hash bridge is reproducible.** SHA-256 of the normalized poster text `GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` is exactly `89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32`, the verified SalPhaseIon/Cosmic Duality route.
8. **MP3 frames 4, 15, and 131 are genuinely anomalous, but a second message is not established.** They are the three internal frames with a different joint-stereo mode extension and the three largest L-R side energies. A 2021 community script independently isolates those exact frames. The selected frames do not decode to separate clear text, and creator discussion is ambiguous; treating the numbers as another solution key would be speculation.

The complete deliverable is indexed in [README.md](./README.md). The broadest newline-delimited list is [all_843_observed_or_ct_inferred_url_candidates.txt](./all_843_observed_or_ct_inferred_url_candidates.txt); its companion [CSV](./all_843_observed_or_ct_inferred_url_candidates.csv) preserves provenance and warns which three entries are inferred rather than observed.

## What “all URLs” can and cannot mean

There is no protocol that enumerates every path a web server has ever accepted. A URL that was never linked, crawled, logged publicly, submitted to an archive, or exposed in client code is not discoverable from public evidence. Wildcard TLS certificates also permit an unlimited number of possible subdomain names without enumerating them.

Accordingly, this package uses three precise scopes:

| Scope | Count | Meaning |
|---|---:|---|
| Wayback exact originals | 831 | Every exact `original` string in the complete `matchType=domain` CDX response retrieved for `gsmg.io/*` |
| Observed exact GSMG URLs | 840 | Union of those 831 strings and all in-scope task URLs from 191 public urlscan records |
| Observed or CT-inferred candidates | 843 | The 840 observed strings plus qualified HTTPS roots for three concrete certificate names not seen as Wayback hosts |

“Exact” deliberately retains scheme, host spelling/case, path case, query strings, fragments reported by urlscan, malformed crawler discoveries, and trailing-slash variants. These are not necessarily 840 semantically different server resources. The provenance CSV is the safest master list because it distinguishes observation from inference.

Files:

- [all_843_observed_or_ct_inferred_url_candidates.csv](./all_843_observed_or_ct_inferred_url_candidates.csv): broadest list, with provenance and qualification
- [all_840_observed_gsmg_urls.txt](./all_840_observed_gsmg_urls.txt): observed strings only
- [all_831_wayback_exact_urls.txt](./all_831_wayback_exact_urls.txt): complete archive-domain list
- [cdx_unique_exact_urls.csv](./cdx_unique_exact_urls.csv): 831 URLs with dates, counts, statuses, MIME types, and flags
- [cdx_all_captures.csv](./cdx_all_captures.csv): all 2,994 capture rows
- [certificate_transparency_hostnames.txt](./certificate_transparency_hostnames.txt): exact and wildcard certificate names
- [urlscan_unique_gsmg_task_urls.txt](./urlscan_unique_gsmg_task_urls.txt): public urlscan task URL strings

## Evidence standard and method

The conclusions use the following hierarchy:

- **Verified/direct:** reproduced from a first-party or content-addressed artifact, archive body, source map, or deterministic computation.
- **Corroborated:** consistent across independent evidence, but at least one source is community-generated.
- **Hypothesis:** a pattern worth testing that lacks author confirmation or a deterministic payload.
- **Negative result:** a bounded test found nothing; it does not prove nothing could exist under every transform.

The workflow was:

1. Parse the supplied `cdx.json` and test each of its 403 exact archived originals with GET requests.
2. Query Wayback CDX with `url=gsmg.io/*&matchType=domain`, retaining all capture rows rather than collapsing paths prematurely.
3. Recover selected historical bodies by archive digest: 132/132 puzzle HTML plans, 55/55 additional unusual HTML plans, 110/110 code assets, and 6/6 selected puzzle image bodies.
4. Cluster HTML by normalized body, extract outlinks/tokens, inspect JavaScript/CSS/JSON/source maps, and compare named routes against body identity.
5. Cross-check 14 successfully queried puzzle-era Common Crawl indexes and all 191 public urlscan results returned by the domain search.
6. Query Certificate Transparency, then check newly exposed concrete names against live DNS and urlscan.
7. Recover the Decentraland scene through its content API, recompute every CIDv0, extract the inline TypeScript source map, decode and inspect the MP3 frame-by-frame, and compare it with dated community artifacts and the local Telegram export.
8. Validate PNG chunks, CRCs, post-IEND data, and a bounded set of low-bit-plane streams.

The official curl build and CA bundle used to avoid the earlier local TLS-chain failure are:

- `E:\rabbitv3\.tools\curl\dist\curl-8.22.0_1-win64-mingw\bin\curl.exe`
- `E:\rabbitv3\.tools\curl\dist\curl-8.22.0_1-win64-mingw\bin\curl-ca-bundle.crt`
- wrapper: `E:\rabbitv3\.tools\curl\curl.ps1`

The wrapper supplies `--cacert` automatically. Directly invoking the executable without the CA option still reproduces the local trust failure; the wrapper is the working fix used for all subsequent retrievals.

## URL census and current status

### Wayback domain census

The [CDX summary](./cdx_summary.json) records:

| Measure | Result |
|---|---:|
| Capture rows | 2,994 |
| Exact original URL strings | 831 |
| Distinct URL keys | 618 |
| Distinct content digests | 1,993 |
| First capture | 2018-07-13 04:31:22 UTC |
| Last capture | 2026-08-30 09:20:27 UTC |

Capture rows by host:

| Host | Captures |
|---|---:|
| `gsmg.io` | 1,378 |
| `help.gsmg.io` | 1,148 |
| `beta.gsmg.io` | 303 |
| `www.gsmg.io` | 122 |
| `stats.gsmg.io` | 17 |
| `alpha.gsmg.io` | 14 |
| `slack-invite.gsmg.io` | 10 |
| `wishes.gsmg.io` | 2 |

The response contained 2,374 archived HTTP 200 rows, 272 redirects, 324 revisit records, and a small number of error captures. An archived 200 means only that the server returned a successful response; body comparison is needed to determine whether it was a real page or an arbitrary-path application fallback.

### The supplied 403 URLs today

The complete results are in [original_403_live_status.csv](./original_403_live_status.csv):

- 403 tested
- 19 return HTTP 200
- 384 return HTTP 404

The 19 current HTTP 200 originals are preserved without truncation in [current_19_live_200_urls.txt](./current_19_live_200_urls.txt). They consist of the root, the long choice route, the `89727c...` route, `/theseedisplanted`, uppercase `/Puzzle`, `robots.txt`, a font, and puzzle/logo images.

Important qualification: HTTP 200 does not mean that every one still serves its historical meaning. For example, uppercase `/Puzzle` is not the same evidence as lowercase `/puzzle`, and generic application or parking responses can also return 200.

### urlscan and Certificate Transparency

The public urlscan API returned 191 scans dated 2019-04-21 through 2026-06-27 and 34 case-sensitive in-scope task URL strings. Nine strings were not exact matches in the Wayback CSV:

```text
http://alpha.gsmg.io/
http://gsmg.io
http://Gsmg.io
http://gsmg.io/phase1verification
http://gsmg.io/PUZZLE
https://gsmg.io
https://gsmg.io/final
https://gsmg.io/img/follow_the_white_rabbit.pn
https://gsmg.io/Puzzle#
```

These add exact spellings, not nine new puzzle-bearing resources: several are root/case/scheme variants; `#` is client-side and never reaches the HTTP server; `.pn` is a likely typo; and `/final` is a late probe with no independent historical puzzle body.

The crt.sh response contains 175 certificate records and nine distinct names: `*.gsmg.io`, `*.beta.gsmg.io`, the apex, `www`, `beta`, `help`, `api`, `api-staging`, and `openpgpkey`. The last three concrete names are absent from the Wayback-host set. `api.gsmg.io` and `api-staging.gsmg.io` appear in certificates beginning 2020-11-09; `openpgpkey.gsmg.io` appears in an August 2026 certificate. As tested on 2026-09-12, none resolves to an A or CNAME record, and urlscan has zero public results for each. They are preserved as host-level leads, not represented as recovered puzzle pages.

## Which puzzle URLs are real?

### Verified puzzle-bearing routes

| Route | Evidence | Finding |
|---|---|---|
| `https://gsmg.io/puzzle` | Archive MIME/body, recovered app route, contemporaneous Reddit | Lowercase route served the puzzle image. A 2019 post identifies it as the original link and records the June 2019 PNG update. |
| `https://gsmg.io/theseedisplanted` | Five recovered historical bodies plus current response | Stable `GSMG Puzzle` page. It contains eight rebus image references and a password form whose method is POST and action is `/phase1verification`. |
| `https://gsmg.io/choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself` | Four recovered historical bodies plus current response | Stable puzzle page containing the next cryptographic material. |
| `https://gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32` | Six recovered main-host bodies, one alpha-host body, current response, deterministic hash | Stable SalPhaseIon/Cosmic Duality page. Wayback evidence begins in 2023; community git history documents it by May 2021. |

The recovered Vue router source registers `/puzzle` as a guest route. Its puzzle component contains the heading and image, with no additional hidden client-side state or route chain. This independently separates the genuine `/puzzle` route from later arbitrary-path fallbacks.

### Real endpoint, but not a recovered clue page

`/phase1verification` is directly present as the seed page's POST form action. Its archived GET captures, however, are the same generic trading SPA shell seen at many arbitrary paths. Ordinary Wayback crawling does not preserve a user's historical form POST response, so the server-side validation/redirect cannot be reconstructed from those GET captures. Calling the endpoint “fake” would be wrong; calling its archived GET body a puzzle phase would also be wrong.

### Solver probes and fallback responses

The following names were recovered as the same generic trading Vue shell, generally first appearing only in 2024-2026:

```text
/phase1
/phase2
/phase3
/phase3_2_2
/phase3_2_2_2
/TheArchitectChoice
/final
/final_stage
/salphaseion
/youarewrongaboutdirhunt
/youmeandself
/youmeiandself
/whiterose
/puzzle/stage5
/thSeedisplanted
```

The shell is a response fallback, not evidence that each string named a deleted page. This is the central reason directory-hunt results and raw CDX rows overstate the puzzle's route tree.

The path `4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081` is a particularly important false lead. Its first archive activity is June/July 2026, and the recovered successful body is the short AboveDomains parking page for a domain offered for sale. It is not independent corroboration of a “Cosmic decrypt.” A community issue later retracted that claim and explains why a clean PKCS#7 unpad and a self-referential hash are insufficient evidence. The archive-body recovery here independently confirms the timing and parking response.

Uppercase `/Puzzle` must also be kept separate from lowercase `/puzzle`: its archived HTML is the generic application shell, whereas the lowercase route is backed by image and source-route evidence.

## Recovered Decentraland clue

### Primary entity and deployment

The Decentraland Catalyst query

`https://peer.decentraland.org/content/entities/scene?pointer=-41%2C-17`

returns the active scene entity:

| Field | Value |
|---|---|
| Entity CID | `QmRK2YoLei9wrxLvHUKisywobxEvczTicXepPxKLKzN51v` |
| Deployment timestamp | `2020-02-20T15:12:16.189Z` |
| Pointers | `-41,-16`; `-41,-17` |
| Base parcel | `-41,-17` |
| Title | `GSMG.io Puzzle piece` |
| Owner | `0x5D801b2B0B216790A49898b322246282547b546b` |
| Main file | `bin/game.js` |

The deployment-history endpoint returns exactly one entity for the pointer and reports no further page of results. Decentraland documents content entities as immutable, hash-addressed file collections whose pointers select the current entity. This makes the recovered bytes stronger evidence than an undated community mirror.

### Content-address verification

All four downloaded objects recompute to the expected CIDv0:

| Object | Expected/computed CIDv0 | SHA-256 of local bytes |
|---|---|---|
| Entity JSON | `QmRK2YoLei9wrxLvHUKisywobxEvczTicXepPxKLKzN51v` | `2c2897dc3168dd6ea3e87c56584f8b7743dae967702357d8c3f19a8647a7d29d` |
| `bin/game.js` | `QmcoAs6kCXynZksyNDB7RTgVYfTkxyrLb8nEU2RJepbhoE` | `d6ced07ecf05426bcc703810dca14c54d9052fe38f28d88fdfb87f9d706728b9` |
| `scene.json` | `QmdESuCguQMVXRKYwcXRJLdNcEcfi3ZXxTGPLEE3NC8czC` | `dd48778735cee440da425bddfae2bc8447deba38295fdce260dab9a7a6c1a5c9` |
| `sounds/puzzlepiece.mp3` | `QmeRy5MjmEZ2W6J3DwhQfht5HKBKXBFpoGzSkzmjeGKiDK` | `ef17a96dce37b4dd7cbf79f210c5cbaf37fcae60e5faf8004de4e0832bd0dfee` |

The verification details and direct content URLs are in [decentraland_recovery_summary.json](./decentraland_scene/decentraland_recovery_summary.json).

### Source-map recovery

The compiled JavaScript embeds an inline source map. Its original TypeScript, recovered as [01_01_game.ts](./decentraland_scene/source_map/01_01_game.ts), shows:

- a cube placed at `(8, 1, 8)`;
- an `AudioClip` loading `sounds/puzzlepiece.mp3`;
- a click handler that plays the source once;
- nine boxes arranged as a question mark; and
- the displayed text `GSMG.IO` and `5 BTC PUZZLE CHALLENGE`.

A local Telegram export contains a creator-posted parcel screenshot in message 1743. Its Unix time corresponds to `2020-02-20T15:31:58Z`, 19 minutes 41.811 seconds after the Catalyst deployment. The screenshot visibly shows the parcel and question-mark structure. A later creator message, 1837, says that only `-41,-17` matters. These records corroborate the content API, but the CID-verified API artifact remains the primary evidence.

## Audio result: `HASHTHETEXT`

The original MP3 is 212,031 bytes, 199 MPEG-1 Layer III frames, 320 kbps, 44.1 kHz stereo, and 5.198367 seconds. It has a 4,096-byte ID3v2.2 region identifying Logic Pro X 10.4.1, and the frame parser found no skipped or trailing bytes.

Reproduction:

1. Decode the original stereo MP3 without resampling.
2. Compute the side signal `left - right` (equivalently invert one channel, mix, and downmix).
3. Render a spectrogram of that side signal.
4. Read the large hexadecimal glyphs:

```text
48 41 53 48 54 48 45 54 45 58 54
 H  A  S  H  T  H  E  T  E  X  T
```

Result: **`HASHTHETEXT`**.

![Detailed L-R spectrogram showing hexadecimal HASHTHETEXT](./decentraland_scene/puzzlepiece_L_minus_R_message_detail.png)

This is hexadecimal-to-ASCII, not a sequence of decimal character codes. The detailed spectrogram above and the original MP3 are included in the package.

### The deterministic hash hop

The poster's compact text and prize address normalize to:

```text
GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
```

The calculation is:

```text
SHA256 = 89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32
```

That digest is the exact verified route name. The equality is deterministic; the particular removal of spaces and punctuation is reproduced by the successful preimage, while the audio itself supplies only the instruction to hash the text.

## Deeper MP3 analysis

### Verified frame anomaly

The 199-frame structural analysis found three internal frames with header `fffbe240`: 4, 15, and 131 (one-based). The other occurrences of that header are boundary frames 1, 198, and 199. Frames 4, 15, and 131 use joint-stereo mode extension 0, while their ordinary neighbors use mode extension 2. They are also the three highest-energy L-R frames:

| Frame | L-R RMS |
|---:|---:|
| 131 | 0.0188434 |
| 15 | 0.0181874 |
| 4 | 0.0150377 |
| Next ordinary frame | 0.0077163 |

The parser found `main_data_begin = 0`, private bits equal to zero, and no appended payload. Frame 132's elevated side energy is consistent with audio spill from 131.

A permanently pinned 2021 community script independently writes `frame_4.mp3`, `frame_15.mp3`, `frame_131.mp3`, their complement, and the three-frame combination. The local `test.mp3` in that repository is byte-for-byte identical to the CID-verified Catalyst MP3. This corroborates the frame numbers and historical discovery, not their intended meaning.

The package includes [puzzlepiece_frames_4_15_131.mp3](./decentraland_scene/puzzlepiece_frames_4_15_131.mp3), its complement, per-frame CSV, decoded energy CSV, and spectrogram. The selected-only audio is a short broadband pulse and does not reveal a separate intelligible message.

### Side-channel periodicity

Within the steady analysis window, the strongest L-R lag is 684 samples:

- frequency: 64.473684 Hz at 44.1 kHz;
- lag correlation: 0.935666;
- averaged cycles: 321;
- half-period: 342 samples;
- half-wave antisymmetry correlation: 0.999749.

These measurements characterize the engineered side signal that carries the visible spectrogram. They do not by themselves establish another layer.

### Hypothesis, not conclusion

One possible numerical pattern is that frames 4 and 15 reproduce a `(4,15)` coordinate pair seen in Phase 2 material, while 131 is the 32nd prime and a coordinate strip contains `S=32`. This is a multiple-comparison-prone observation: many numbers occur throughout a multi-stage puzzle, the author did not confirm this mapping, and no transform using it has produced an independently verifiable payload. It should be treated as a test lead only.

The Telegram discussion is also deliberately inconclusive. In April 2020, participants asked whether the visible audio artifacts were an additional hint; the creator avoided confirming that and later said errors and typos were mostly unintended. In March 2021, community members accurately identified three different MP3 frames and published the parser/repacker. This proves the anomaly was noticed, not that `4,15,131` is a second authored answer.

## HTML, code, and image findings

### Recovered HTML

The selected recovery analyzed 187 HTML files:

| Normalized classification | Files |
|---|---:|
| Trading SPA shell | 126 |
| Help Center | 38 |
| Parked domain | 8 |
| Puzzle SalPhaseIon | 6 |
| Puzzle seed | 5 |
| Puzzle choice | 4 |

The large shell cluster explains why invented paths can acquire successful archive records. It also means path names must never be interpreted without body-level comparison.

### Recovered client code

The code pass recovered 110 archive assets representing 40 unique bodies: 72 JavaScript, 14 CSS, 20 JSON, and 4 source maps. It extracted 25 unique route values and 7,075 literal-path rows. Puzzle-specific code evidence was limited to the registered `/puzzle` route/component, the `GSMG MEGANIGMA` heading, and `follow_the_white_rabbit`; there was no hidden client-side phase tree or secret payload in the recovered puzzle component.

This does not rule out server-side logic. It does rule against claims that guessed phase URLs are present in the recovered front-end router.

### PNG structure and bounded steganography checks

The recovered puzzle PNGs have valid signatures and CRCs, no textual PNG chunks, and no bytes after `IEND`. A bounded scan of low bit planes, channel orders, and bit packings found no embedded file magic, URL, or meaningful printable run. See [png_structure_analysis.json](./png_structure_analysis.json).

This is a negative result for those transforms only. It does not replace the known visual/binary reading of the puzzle poster and rebus images, nor does it prove every conceivable pixel transform is empty.

## Cross-source checks and misinformation controls

Four source-quality problems repeatedly appeared during the search:

1. **CDX pollution by requested URLs.** A user or scanner can cause a guessed URL to appear in CDX even when the origin merely returns a fallback.
2. **HTTP 200 fallbacks.** The trading SPA and later parking server answer unrelated paths successfully.
3. **Self-referential “verification.”** Hashing a candidate output and then visiting that hash path is not independent confirmation; it can create the very archive/urlscan trail later cited as proof.
4. **Late community reconstructions.** Recent repositories and issues often mix primary puzzle bytes, memories, speculative decryptions, synthetic test keys, and donation claims. Their publication date and reproducibility matter more than confident wording.

The 14 successfully queried puzzle-era Common Crawl collections produced 388 records and 78 exact URLs dated 2019-04-18 through 2022-01-25. Every one of those 78 strings was already present in the 831-URL Wayback set. An attempted all-index bulk expansion was rate-limited/timed out, including on collections already recovered successfully in the smaller retried batch; it is therefore not counted as a completed census.

The public urlscan census added exact spellings and probes but no newly verified puzzle-bearing body. Certificate Transparency added hostnames, not paths.

## What is newly established here

The community already knew the broad instruction to visit Decentraland, subtract stereo channels, and read `HASHTHETEXT`. This investigation advances the evidence in several concrete ways:

- recovers the original scene and MP3 directly from Decentraland's content-addressed network;
- verifies every entity/file CID against the downloaded bytes;
- recovers the scene's original TypeScript from its inline source map;
- ties the deployment timestamp to a creator screenshot less than twenty minutes later;
- renders the exact hexadecimal message from the verified MP3;
- proves the normalized poster text hashes to the live 64-character route;
- quantifies the three anomalous MP3 frames and separates structural fact from unconfirmed interpretation;
- distinguishes genuine puzzle bodies from generic-shell and parked-domain captures; and
- provides an untruncated, provenance-qualified URL inventory rather than a raw path dump.

## Remaining gaps and best next investigations

The highest-value unresolved questions are now narrow:

1. **Server-side Phase 1 transition.** Find a contemporaneous HAR, browser cache, screenshot, email, or archive containing the POST response from `/phase1verification`. GET-only archives cannot reconstruct it.
2. **Creator provenance for late-stage hints.** Search original 2019-2021 Telegram/Discord exports for the exact source messages behind claims such as “prime,” “zeroed out,” “Yin Yang,” and “ASCII-127.” Later screenshots of screenshots are weak evidence.
3. **Original late-stage files.** Require hashes and dated provenance for every AES/blob artifact before testing proposed keys. This prevents synthetic or transformed files from silently replacing the puzzle input.
4. **Audio anomaly falsification.** Define a candidate decoding rule for `4,15,131` before searching outputs, test it against controls/neighbor frames, and demand a recognizable or cryptographically checkable result.
5. **Additional passive archives.** A rate-limited, low-concurrency retry of every Common Crawl collection could close the remaining collection-level coverage gap. Memento aggregators, personal browser caches, and original Discord attachments are more likely to add historical bodies than further directory guessing.

Brute-forcing arbitrary live paths is low value: the origin's fallback behavior makes false positives cheap, and it cannot recover server-side pages that were removed years ago.

## Sources

### Primary and archival

- [Wayback CDX domain query used for the 2,994-row census](https://web.archive.org/cdx/search/cdx?url=gsmg.io/*&matchType=domain&output=json&fl=urlkey,timestamp,original,mimetype,statuscode,digest,length&limit=100000&showResumeKey=true)
- [Decentraland active entity at pointer -41,-17](https://peer.decentraland.org/content/entities/scene?pointer=-41%2C-17)
- [Decentraland deployment history at pointer -41,-17](https://peer.decentraland.org/content/deployments?entityType=scene&pointer=-41%2C-17)
- [Decentraland entity content by CID](https://peer.decentraland.org/content/contents/QmRK2YoLei9wrxLvHUKisywobxEvczTicXepPxKLKzN51v)
- [Decentraland compiled scene by CID](https://peer.decentraland.org/content/contents/QmcoAs6kCXynZksyNDB7RTgVYfTkxyrLb8nEU2RJepbhoE)
- [Decentraland scene metadata by CID](https://peer.decentraland.org/content/contents/QmdESuCguQMVXRKYwcXRJLdNcEcfi3ZXxTGPLEE3NC8czC)
- [Decentraland puzzle MP3 by CID](https://peer.decentraland.org/content/contents/QmeRy5MjmEZ2W6J3DwhQfht5HKBKXBFpoGzSkzmjeGKiDK)
- [Decentraland ADR describing immutable content entities, pointers, and file hashes](https://github.com/decentraland/adr/blob/main/content/ADR-102-decentraland-protocol-for-explorers%20copy.md)
- [crt.sh query for `%.gsmg.io`](https://crt.sh/?q=%25.gsmg.io)
- [urlscan public domain search](https://urlscan.io/search/#domain:gsmg.io)
- [Common Crawl index API](https://index.commoncrawl.org/)

### Contemporaneous community records

- [Original April 2019 Reddit announcement and June PNG update](https://www.reddit.com/r/bitcoinpuzzles/comments/bf7siz/gsmgio_5_btc_puzzle_challenge/)
- [October 2019 Reddit discussion](https://www.reddit.com/r/bitcoinpuzzles/comments/dfwcqk/gsmgio_5_btc_puzzle/)
- [April 2020 community hint thread](https://www.reddit.com/r/bitcoinpuzzles/comments/galkeh/gsmgio_5_btc_puzzle_hints/)
- [Community hint repository](https://github.com/puzzlehunt/gsmgio-5btc-puzzle)
- [2021 MP3 frame repacker pinned to commit `490ba301`](https://github.com/lelicopter/mp3hacker/blob/490ba301ebd578e62fb396e0426db325f64a2d0f/MP3repack.py)

### Secondary caution/reference

- [2026 retraction and provenance request concerning the false `4f7a1e...` route](https://github.com/puzzlehunt/gsmgio-5btc-puzzle/issues/104)

Local source hashes, downloaded-object hashes, generated artifact hashes, and the selected Telegram message IDs are preserved in [artifact_manifest.json](./artifact_manifest.json), [decentraland_recovery_summary.json](./decentraland_scene/decentraland_recovery_summary.json), and [telegram_audio_evidence.json](./decentraland_scene/telegram_audio_evidence.json).
