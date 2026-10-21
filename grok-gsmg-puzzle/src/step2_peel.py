"""Arithmetic peel, the cp273 symbol table, and the poster-total passwords.

Win test is the uncompressed pubkey only: the prize address commits to that
encoding. No positional g-masks.

Arithmetic peel, two readings of the same rule (g is 0 or 7, every other
letter a=1 .. i=9, a non-printable byte kills the branch, the quotient is
what carries):

  stream   left to right. acc = acc*10 + digit; when acc >= 256, emit
           acc % 256 and carry acc // 256.
  base256  the whole digit string is one integer; repeatedly emit n % 256
           and replace n by n // 256. Bytes are reported most-significant first.
"""

from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crypto_known import PRIZE_H160, hash160, is_win_uncompressed, pubkey_hash160s  # noqa: E402
from step1_btcseed import decrypt_with_password, kdf_modes, load_containers, sha256  # noqa: E402

ART = Path(__file__).resolve().parents[1] / "artifacts"
PRINTABLE = set(range(32, 127))


def digits_of(ch: str) -> tuple[int, ...]:
    if ch == "g":
        return (0, 7)
    if ch not in "abcdefghi":
        raise ValueError(f"not an a-i letter: {ch!r}")
    return (ord(ch) - 96,)  # a=1 .. i=9, so g would have been 7


def stream_peel(text: str, cap: int = 40):
    """DP over (index, carried accumulator). Returns solutions and the longest prefix."""
    n = len(text)
    # ok[i][acc] : a fully valid completion exists (final acc is 0 or printable)
    # best[i][acc] : most printable bytes still available from here, counting a
    # valid final accumulator and not counting a pruned byte
    ok = [[False] * 256 for _ in range(n + 1)]
    best = [[0] * 256 for _ in range(n + 1)]
    for acc in range(256):
        if acc == 0 or acc in PRINTABLE:
            ok[n][acc] = True
        if acc in PRINTABLE:
            best[n][acc] = 1
    for i in range(n - 1, -1, -1):
        opts = digits_of(text[i])
        row_ok = ok[i]
        row_best = best[i]
        nxt_ok = ok[i + 1]
        nxt_best = best[i + 1]
        for acc in range(256):
            good = False
            score = 0
            for d in opts:
                nxt = acc * 10 + d
                if nxt >= 256:
                    q, r = divmod(nxt, 256)
                    if r in PRINTABLE:
                        if nxt_ok[q]:
                            good = True
                        score = max(score, 1 + nxt_best[q])
                else:
                    if nxt_ok[nxt]:
                        good = True
                    score = max(score, nxt_best[nxt])
            row_ok[acc] = good
            row_best[acc] = score

    solutions = []

    def walk(i, acc, out: bytearray):
        if len(solutions) >= cap:
            return
        if i == n:
            if acc in PRINTABLE:
                out.append(acc)
                solutions.append(bytes(out))
                out.pop()
            elif acc == 0 and out:
                solutions.append(bytes(out))
            return
        for d in digits_of(text[i]):
            nxt = acc * 10 + d
            if nxt >= 256:
                q, r = divmod(nxt, 256)
                if r in PRINTABLE and ok[i + 1][q]:
                    out.append(r)
                    walk(i + 1, q, out)
                    out.pop()
            elif ok[i + 1][nxt]:
                walk(i + 1, nxt, out)

    if ok[0][0]:
        walk(0, 0, bytearray())

    # One maximum-length prefix, following `best`, whether or not it completes.
    prefix = bytearray()
    i, acc = 0, 0
    while i < n:
        picked = None
        picked_score = -1
        for d in digits_of(text[i]):
            nxt = acc * 10 + d
            if nxt >= 256:
                q, r = divmod(nxt, 256)
                if r in PRINTABLE:
                    sc = 1 + best[i + 1][q]
                    if sc > picked_score:
                        picked_score = sc
                        picked = (q, r)
            else:
                sc = best[i + 1][nxt]
                if sc > picked_score:
                    picked_score = sc
                    picked = (nxt, None)
        if picked is None or picked_score <= 0:
            break
        nxt_acc, emitted = picked
        if emitted is not None:
            prefix.append(emitted)
        acc = nxt_acc
        i += 1
    if i == n and acc in PRINTABLE:
        prefix.append(acc)
    return {
        "completes": bool(ok[0][0]),
        "n_solutions_capped": len(solutions),
        "solutions": solutions,
        "longest": best[0][0],
        "prefix": bytes(prefix),
    }


def base256_peel_fixed(digits: list[int]) -> bytes | None:
    n = 0
    for d in digits:
        n = n * 10 + d
    if n == 0:
        return b""
    le = []
    while n:
        n, r = divmod(n, 256)
        if r not in PRINTABLE:
            return None
        le.append(r)
    return bytes(reversed(le))


def base256_peel(text: str, node_cap: int = 5_000_000):
    """Branch g from the low digits. Prune once a settled low byte is not printable."""
    dig = [0 if c == "g" else ord(c) - 96 for c in text]
    gpos = [i for i, c in enumerate(text) if c == "g"]
    # rightmost g first
    order = gpos[::-1]
    solutions = []
    nodes = 0
    capped = False
    max_bytes = 0

    def suffix_low_bytes(start: int, count: int) -> list[int]:
        n = 0
        for d in dig[start:]:
            n = n * 10 + d
        out = []
        for _ in range(count):
            n, r = divmod(n, 256)
            out.append(r)
        return out

    def rec(gi: int, ready: int, le_prefix: tuple[int, ...]):
        nonlocal nodes, capped, max_bytes
        if capped:
            return
        nodes += 1
        if nodes > node_cap:
            capped = True
            return
        if gi == len(order):
            whole = base256_peel_fixed(dig)
            if whole is not None:
                solutions.append(whole)
                max_bytes = max(max_bytes, len(whole))
            return
        idx = order[gi]
        for d in (0, 7):
            dig[idx] = d
            # Digits from `idx` through the end are now concrete.
            suffix_len = len(dig) - idx
            b = suffix_len // 8
            if b > ready:
                lows = suffix_low_bytes(idx, b)
                if any(r not in PRINTABLE for r in lows[ready:]):
                    continue
                max_bytes = max(max_bytes, b)
                rec(gi + 1, b, le_prefix + tuple(lows[ready:]))
            else:
                rec(gi + 1, ready, le_prefix)

    if not order:
        whole = base256_peel_fixed(dig)
        return {
            "completes": whole is not None,
            "solutions": [whole] if whole else [],
            "nodes": 1,
            "capped": False,
            "longest_low_bytes": len(whole) if whole else 0,
            "g": 0,
        }
    rec(0, 0, ())
    # de-duplicate, preserve order
    uniq = []
    seen = set()
    for s in solutions:
        if s not in seen:
            seen.add(s)
            uniq.append(s)
    return {
        "completes": bool(uniq),
        "solutions": uniq[:40],
        "n_solutions": len(uniq),
        "nodes": nodes,
        "capped": capped,
        "longest_low_bytes": max_bytes,
        "g": len(order),
    }


def self_test():
    # c,b,h,g,e = digits 3,2,8,{0|7},5.
    # g=0 is 32805: peel 'H' carrying quotient 1, then accumulator 'i'.
    # g=7 ends on accumulator 175, which is outside 32..126 and is pruned.
    got = stream_peel("cbhge")
    assert got["solutions"] == [b"Hi"], got
    assert stream_peel("fe")["solutions"] == [b"A"]
    # g=7 makes "75" -> 'K'; g=0 leaves accumulator 5, which is pruned.
    assert stream_peel("ge")["solutions"] == [b"K"]
    assert base256_peel_fixed([1, 8, 5, 3, 7]) == b"Hi"
    assert base256_peel_fixed([6, 5]) == b"A"
    print("[PASS] peel self-test  stream(cbhge)=Hi  stream(fe)=A  stream(ge)=K  base256(18537)=Hi")


def _cp273_name(glyph: str) -> str:
    try:
        return unicodedata.name(glyph)
    except ValueError:
        o = ord(glyph)
        known = {0x07: "BELL", 0x0A: "LINE FEED", 0x1A: "SUBSTITUTE"}
        if o in known:
            return known[o]
        if o < 32:
            return f"C0 control U+{o:04X}"
        if 0x80 <= o <= 0x9F:
            return f"C1 control U+{o:04X}"
        return f"unnamed U+{o:04X}"


def cp273_report(pt: bytes) -> dict:
    import re

    dig = re.search(rb"\r\n(\d{149})\r\n", pt)
    if not dig:
        raise SystemExit("149-digit run not found")
    # Published slice: bytes 447..1985 inclusive.
    published = pt[447:1986]
    # Natural slice: after the blank line that ends the ASCII, before the
    # blank line that introduces the digits.
    ascii_end = pt.find(b"four for one.")
    if ascii_end < 0:
        raise SystemExit("ascii anchor missing")
    after = ascii_end + len(b"four for one.")
    # consume the CRLF CRLF that follows the sentence
    natural_start = after
    if pt[natural_start:natural_start + 4] == b"\r\n\r\n":
        natural_start += 4
    natural_end = dig.start()  # the \r\n before the digits; back up over a blank line
    # dig.start() points at \r\n(\d). The binary is separated from the digits by \r\n\r\n.
    if pt[natural_end - 2:natural_end] == b"\r\n":
        binary_end = natural_end - 2
        if pt[binary_end - 2:binary_end] == b"\r\n":
            binary_end -= 2
    else:
        binary_end = natural_end
    natural = pt[natural_start:binary_end]

    def table(blob: bytes):
        rows = []
        for b in sorted(set(blob)):
            glyph = bytes([b]).decode("cp273")
            rows.append({
                "byte": b,
                "hex": f"{b:02x}",
                "cp273": glyph,
                "u": f"U+{ord(glyph):04X}",
                "name": _cp273_name(glyph),
            })
        return rows

    def letter_count(blob: bytes) -> int:
        return sum(ch.isalpha() for ch in blob.decode("cp273"))

    # Slide a 1539-byte window across the neighbourhood and record the best
    # cp273 letter count, so a one-byte offset error cannot hide an alphabetic read.
    window = 1539
    best = []
    lo = max(0, natural_start - 32)
    hi = min(len(pt) - window, natural_start + 32)
    for start in range(lo, hi + 1):
        blob = pt[start:start + window]
        best.append((letter_count(blob), start))
    best.sort(reverse=True)

    pub_rows = table(published)
    lines = []
    lines.append(f"phase32 len {len(pt)}")
    lines.append(f"ascii anchor 'four for one.' at {ascii_end}")
    lines.append(f"natural binary {natural_start}:{binary_end} len {len(natural)} unique {len(set(natural))}")
    lines.append(f"published     447:1986 len {len(published)} unique {len(set(published))}")
    lines.append(f"natural == published: {natural == published}")
    lines.append(f"published cp273 alphabetic chars: {letter_count(published)}/{len(published)}")
    lines.append("best 1539-byte windows by cp273 letter count (top 5):")
    for score, start in best[:5]:
        lines.append(f"  start {start} letters {score}/1539")
    lines.append("26 symbols at the published offset, cp273 glyphs:")
    for row in pub_rows:
        shown = row["cp273"] if row["cp273"].isprintable() else ""
        lines.append(f"  0x{row['hex']} {row['byte']:3d}  {row['u']:8} {row['name']:28} {shown!r}")
    text = "\n".join(lines) + "\n"
    (ART / "cp273_symbols.txt").write_text(text)
    print(text)
    return {"natural_eq_published": natural == published, "rows": pub_rows, "best": best[:5]}


def poster_totals() -> dict:
    grid = (ART / "poster_grid.txt").read_text().splitlines()
    flat = "".join(grid)
    from collections import Counter
    cnt = Counter(flat)
    b, y, k = cnt["B"], cnt["Y"], cnt["K"]
    t255 = b * 2 + y * 25
    t161 = b * 2 + y * 5 + k * 1
    print(f"cell counts {dict(cnt)}")
    print(f"B=2 Y=25 -> {b}*2 + {y}*25 = {t255}")
    print(f"B=2 Y=5 K=1 -> {b}*2 + {y}*5 + {k}*1 = {t161}")
    if t255 != 255 or t161 != 161:
        raise SystemExit(f"poster totals are not 255 and 161 ({t255}, {t161})")
    print("[PASS] poster totals 255 and 161")
    return {"255": t255, "161": t161, "counts": dict(cnt)}


def looks_structured(buf: bytes) -> bool:
    if len(buf) < 4:
        return False
    letters = sum(chr(b).isalpha() for b in buf)
    return letters >= max(4, int(len(buf) * 0.7))


def win_uncompressed(label: str, priv: bytes, found: list):
    if len(priv) != 32:
        return
    got = pubkey_hash160s(priv)
    if got is None:
        return
    ok = got["uncompressed"] == PRIZE_H160
    print(f"  key {label} uncomp {got['uncompressed']} {'WIN' if ok else 'no'}")
    if ok:
        found.append({"label": label, "priv": priv.hex(), "hash160": got["uncompressed"]})


def password_battery(extra: list[tuple[str, str]]):
    containers = {k: v for k, v in load_containers().items() if k in (
        "terminal", "salphaseion_short", "cosmic", "sal_yinyang_blocks",
    )}
    answers = [
        ("total-255", "255"),
        ("total-161", "161"),
        ("total-255161", "255161"),
        ("total-161255", "161255"),
        ("total-255-hex", "ff"),
        ("total-161-hex", "a1"),
    ]
    answers.extend(extra)
    found = []
    hits = []
    log_path = ART / "step2_attempts.jsonl"
    with log_path.open("w") as logf:
        for label, answer in answers:
            win_uncompressed(f"sha256({label})", sha256(answer.encode()), found)
            if len(answer) == 64 and all(c in "0123456789abcdef" for c in answer):
                win_uncompressed(f"hex({label})", bytes.fromhex(answer), found)
            modes = kdf_modes(answer)
            for cname, raw in containers.items():
                for mode, pw in modes.items():
                    body, full = decrypt_with_password(raw, pw)
                    if body is None:
                        kind = "no-pad"
                    else:
                        p = full[-1]
                        textish = looks_structured(body)
                        kind = "structured" if textish else ("pad-only-1" if p == 1 else f"pad-{p}")
                    rec = {
                        "container": cname,
                        "kdf": mode,
                        "label": label,
                        "answer": answer if len(answer) < 300 else answer[:80] + f"...<{len(answer)}>",
                        "answer_sha256": sha256(answer.encode()).hex(),
                        "result": kind,
                    }
                    if body is not None and kind != "pad-only-1":
                        rec["plaintext_hex"] = body.hex()
                        print(f"  NEAR/HIT {cname} {mode} {label} {kind} {body[:80]!r}")
                        if kind == "structured":
                            hits.append(rec)
                    logf.write(json.dumps(rec) + "\n")
    print(f"password rows {len(answers) * len(containers) * 5}, hits {len(hits)}, key wins {len(found)}")
    return {"hits": hits, "wins": found, "n_answers": len(answers)}


def peel_witness(name: str, text: str):
    """Show the byte that kills each reading, including bytes no g-branch can change."""
    # Letters before the first g are not branched. If they already overflow,
    # that remainder kills every g-assignment.
    pre = text.split("g", 1)[0]
    acc = 0
    forced = False
    for i, ch in enumerate(pre):
        acc = acc * 10 + (ord(ch) - 96)
        if acc >= 256:
            q, r = divmod(acc, 256)
            print(f"  stream forced overflow at {pre[:i+1]!r} remainder {r} ({'printable' if r in PRINTABLE else 'NOT printable'}) quotient {q}")
            forced = True
            break
    if not forced:
        print(f"  stream g-free prefix {pre!r} does not overflow (accumulator {acc})")
    # Base-256: low bytes fixed by the g-free trailing run cannot be branched away.
    cut = text.rfind("g")
    trail = text if cut < 0 else text[cut + 1:]
    n = 0
    for ch in trail:
        n = n * 10 + (ord(ch) - 96)
    b = len(trail) // 8
    x = n
    print(f"  base256 trailing g-free {trail!r} ({len(trail)} digits) fixes {b} low bytes")
    for i in range(b):
        x, r = divmod(x, 256)
        flag = "printable" if r in PRINTABLE else "NOT printable"
        print(f"    low byte {i}: {r} {flag}")


def show_peel(name: str, text: str):
    g = text.count("g")
    print(f"\n=== stream peel {name} len {len(text)} g {g} ===")
    peel_witness(name, text)
    stream = stream_peel(text)
    print(f"  completes {stream['completes']} longest {stream['longest']} solutions {stream['n_solutions_capped']}")
    if stream["prefix"]:
        print(f"  prefix ({len(stream['prefix'])}) {stream['prefix'][:120]!r}")
    for s in stream["solutions"][:10]:
        print(f"  SOL {s[:200]!r}")
    (ART / f"peel_stream_{name}.txt").write_text(
        "\n".join(s.decode("latin-1") for s in stream["solutions"]) + "\n"
    )

    print(f"=== base256 peel {name} ===")
    base = base256_peel(text)
    print(
        f"  g {base['g']} nodes {base['nodes']} capped {base['capped']} "
        f"completes {base['completes']} longest_low_bytes {base['longest_low_bytes']} "
        f"solutions {base.get('n_solutions', len(base['solutions']))}"
    )
    for s in base["solutions"][:10]:
        print(f"  SOL {s[:200]!r}")
    (ART / f"peel_base256_{name}.txt").write_text(
        "\n".join(s.decode("latin-1") for s in base["solutions"]) + "\n"
    )
    strings = []
    for kind, block in (("stream", stream["solutions"]), ("base256", base["solutions"])):
        for s in block:
            if looks_structured(s) or len(s) >= 8:
                strings.append((f"{kind}-{name}", s.decode("latin-1")))
    return strings


def main():
    self_test()
    pt = (ART / "phase32.bin").read_bytes()
    cp273_report(pt)
    poster_totals()
    faed = (ART / "faed.txt").read_text().strip()
    fillers = (ART / "yellowblue_fillers.txt").read_text().strip()
    extra = []
    extra += show_peel("fillers", fillers)
    extra += show_peel("faed", faed)
    # de-duplicate password strings
    seen = set()
    uniq = []
    for label, s in extra:
        if s not in seen:
            seen.add(s)
            uniq.append((label, s))
    print(f"\n=== passwords, including poster totals; peel strings added: {len(uniq)} ===")
    summary = password_battery(uniq)
    (ART / "step2_summary.json").write_text(json.dumps({
        "peel_strings": [s for _, s in uniq],
        **summary,
    }, indent=2))
    if summary["wins"] or summary["hits"]:
        raise SystemExit(0)
    print("NO HIT")


if __name__ == "__main__":
    main()
