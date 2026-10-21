# The "go back" and "another door" hints — verbatim

Every message from the creator (`Jrk Bgrt`) in the 51,177-message Telegram export
that mentions a door, going back, the first puzzle piece, the beginning, the
rabbit or the nest. Times converted from the export's UTC−05:00 to UTC. Messages
whose sender field carries an embedded date are reply/forward headers, not fresh
posts, and are excluded.

---

## The core hint — 2020-01-14 10:38:06 UTC

> Roses are White but often Red.
> Yellow has a number and so does Blue.
> Go back to the first puzzle piece without further ado.
>
> It might have shown you only one door, beware that the rabbits nest may contain
> a whole lot more.
>
> Hush hush.

(followed at 10:38:49 by "Good luck 👍")

This is the only message that says *go back to the first puzzle piece*. Everything
else about doors refers back to it.

---

## The door thread

**2020-05-11 20:31:25 UTC** — 29 minutes after the halving split landed

> Let's see what bitcoin is worth the next halving and who knows what you'll find
> after opening the 2nd door. The price is in half, but what does it mean 🤔.

**2020-08-02 16:56:20 UTC**

> Really nobody managed to find the extra door, didn't expect that after the
> earlier pace of cracking things.

**2021-12-03 03:41 UTC**

> There is
> Another
> D
> O
> O
> R

(followed at 03:46 by "Remind me when it's Christmas.")

**2021-12-26 20:18:32 UTC** — the Christmas follow-up he promised

> The previous "there is another door hint" is still a thing. We're not sure if
> anyone has found another door so far, and we can't check that... We've seen
> prime numbers being mentioned; well, that is definitely an aspect which is
> required to proceed. Furthermore, along the way, some characters need to be
> 'zeroed out'.. Best of luck and happy holidays! 🥂

(preceded at 20:11:26 by "Oh well, why not. A mini mini hint. Ready 🐰?")

---

## Go-back-to-the-beginning, outside the door thread

**2020-02-25 18:10:30 UTC**
> I'd dive in the puzzle from the beginning before making assumptions

In the same run he also said: *"3.2 is a thing btw"*, *"Or nobody found the
direction"*, *"But I should shut up ofcourse 😁"*, and *"Just spend less time here
fishing for clues and solve 🧐"*.

**2021-01-07 19:57–19:58 UTC**
> It'll be split on the next halving.
> We mentioned this at the beginning, when the puzzle started.

**2021-04-01 14:06 UTC** — a bare 👆 endorsing the message directly above it:
> "Probably best to start at the beginning to understand the mindset behind it"

**2024-03-27 16:41:56 UTC**
> Sqaures and a rabbit?

---

## NOT A HINT — 2021-04-01 06:57:38 UTC

> Hint: "another door might be found on {1 },{4} ,{21}"

**This is an April Fools' joke and should not be treated as data.** The evidence is
in the same thread:

| time | who | |
| --- | --- | --- |
| 06:57 | **creator** | `Hint: "another door might be found on {1 },{4} ,{21}"` |
| 08:06 | x7x7x7x6 | `Private key might be found on {30 },{2} ,{77}` — an immediate parody |
| 08:15 | omaru | "April fool's ? 😄" |
| 08:34 | **creator** | "Good one V ;-). (Assuming you played cyberpunk)." — he plays along with the parody |
| 13:29 | **creator** | `R=18 / A=1 / B=2` … "Could also be 21 or 1812 bit 🧐. Sometimes I'm glad I don't have to solve this puzzle myself." |

That last one is wordplay, not a cipher: R-A-B = 18-1-2 = "1812", plus "bit" =
**RABBIT**. A participant completed it in the open twenty minutes later —
`R=18 A=1 B=2 B=2 I=9 T=20`.

**This matters:** `gsmgio-5btc-puzzle-master/SALPHASEION_PREREGISTRATION.md:405`
builds "a 21-row layout corresponding to `{1},{4},{21}`" on this line. That
foundation is an April Fools' gag the creator joked about again the same afternoon.

---

## What the set actually constrains

- The second door is in **the first puzzle piece** — the poster. Stated once,
  directly, and never retracted.
- It was still unfound as of **2021-12-26**, by his own account, and he says he
  cannot check whether anyone has found it since.
- Two mechanisms are named for it: **prime numbers** ("definitely an aspect which
  is required to proceed") and **characters that need to be 'zeroed out'**.
- The 2020-05-11 line ties the door to the halving split — *"The price is in half,
  but what does it mean"* — posted 29 minutes after 2.5 BTC moved to Better Half.

---

## Turning the hints into a testable list

The creator names exactly two operations for the second door — **prime numbers**
and **characters "zeroed out"** — and one location, **the first puzzle piece**.
That piece encodes exactly one string. So if the second door is a *page*, it is
that string transformed by those two operations and nothing else.

`door_paths.py` enumerates them with no invented steps: prime indices deleted or
kept (0- and 1-indexed), prime indices replaced by `0` and by `o` (the puzzle's own
o = 0 encoding), every single-character deletion as the exhaustive superset, and
removal of every zero-ish character. 29 well-formed paths result.

**The one the hints jointly select:**

    https://gsmg.io/theseedisplated

The `#fefefe` cell marks byte 20 of the 192-bit payload. Byte 20 of
`gsmg.io/theseedisplanted` is character 12 of the path — the `n` of "planted".
Delete it and the result is a valid path. That is the only candidate where the
poster's single anomaly, the "zeroed out" instruction, and a well-formed URL all
coincide. Its spiral index, 163, is prime, which satisfies the other named
operation.

**Not testable here.** `web.archive.org` is refused at this environment's egress
proxy, as are the block explorers. The check is one query:

```text
https://web.archive.org/cdx/search/cdx?url=gsmg.io*&output=json&filter=statuscode:200&collapse=urlkey
```

That returns every gsmg.io URL the archive holds — the corpus reports 414 unique
ones, of which the curated files name about a dozen. **Any puzzle page that exists
and was ever crawled is in that list.** Diff it against the known stages; anything
unaccounted for is a candidate door. Then check the 29 paths above against it
directly.

A caution on reading the result: a 404 capture is not evidence of absence (the
page may never have been crawled), and a 200 capture of an unknown path is not
automatically a door — the GSMG app is a single-page app that served its shell,
including the "Oops! Page Not Found" body, at a 200 for many paths.
`archives/phase1verification.html` is exactly that: 421 KB of SPA bundle wrapping
401 characters of visible text. Judge candidates by their *body*, not their status.
