# Backing data

Primary data the documents in `analysis/` are derived from, committed so their
claims can be re-checked rather than taken on trust.

| file | what it is |
| --- | --- |
| `gsmg_io_wayback_cdx.json` | Wayback CDX index for `gsmg.io*`, 404 capture rows. Fetched externally — this environment's egress proxy refuses `web.archive.org`. Backs Addendum 29 (the false "live door") and its retraction in Addendum 30. |
| `creator_messages.json` | All 411 creator-authored messages from the Telegram export, `[iso8601_utc, text]` pairs, reply/forward headers excluded. Backs `CREATOR_HINTS.md`. Times are **UTC**, converted from the export's UTC−05:00. |
| `bitcoin_whitepaper.txt` | Plain text of the Bitcoin whitepaper. Backs Addendum 27's finding that the paper contains no "1616", "chancellor", "bailout", "anarchist", "hundred" or "fourty". |

## The one check that matters most

Addendum 30 retracts a dramatic claim. Reproduce the retraction directly:

```python
import json, urllib.parse
rows = json.load(open('gsmg_io_wayback_cdx.json'))[1:]
h = sorted((ts, int(ln), urllib.parse.urlparse(o).path)
           for _, ts, o, m, sc, dg, ln in rows if 'html' in m and ts.startswith('2026'))
before = [x for x in h if x[0] <  '20260701']
after  = [x for x in h if x[0] >= '20260701']
print(len(before), min(x[1] for x in before), max(x[1] for x in before))   # 61  10595 13059
print(len(after),  min(x[1] for x in after),  max(x[1] for x in after))    #  9    794  2040
```

The capture size is a property of **when** the site was crawled, not of whether the
path resolved. `gsmg.io` began serving a 9-byte `Hello :-)` placeholder some time
between 2026-04-24 and 2026-07-07. Three of those nine small captures are lodash
source fragments a scanner submitted as URLs.

## Re-derive the seven phrases

The 2023-02-23 message in `creator_messages.json` carries them as 1,288 bits.
Bit-reverse each byte, then reverse the whole string:

```python
bits = ''.join(c for c in msg if c in '01')
s = ''.join(chr(int(bits[i:i+8][::-1], 2)) for i in range(0, len(bits), 8))
print(s[::-1])   # yellowblueprimes matrixsumlist lastwordsbeforearchichoice yinyang ...
```
