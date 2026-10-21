"""Six-position zero mask on faed, then the last-words password battery.

Positions are 1-based, matching faed[1] = the leading 'f'. Zeroing writes the
digit 0 and does not delete. Digits are a=1 .. i=9, so g stays 7 unless a
branch says otherwise. The integer is read big-endian. The win test accepts
only the uncompressed pubkey.

Controls that must hold before the mask is trusted:
  unmasked low 4 bytes  c7 bb c0 75
  unmasked top 4 bytes  1b d5 95 1d
  zero {557}            low 4 bytes spell yI u
  zero {551,557,561,563} low 4 bytes spell szqu
  zero {1,3}            top 2 bytes spell yM
  zero {1,2}            top 2 bytes spell ?j
  lastwords / thispassword re-decode by the same integer rule
  sha256(phase-1 answer) == creator message #225
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crypto_known import PRIZE_H160, is_win_uncompressed, pubkey_hash160s  # noqa: E402
from step1_btcseed import decrypt_with_password, load_containers  # noqa: E402

ART = Path(__file__).resolve().parents[1] / "artifacts"
FLOWER = "theflowerblossomsthroughwhatseemstobeaconcretesurface"
HASH225 = "5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75"
MASK6 = (1, 3, 551, 557, 561, 563)
TAIL4 = (551, 557, 561, 563)
PRINTABLE = set(range(32, 127))


def digits_of(text: str, g: int = 7) -> list[int]:
    out = []
    for ch in text:
        if ch == "g":
            out.append(g)
        elif ch in "abcdefhi":
            out.append(ord(ch) - 96)
        else:
            raise ValueError(ch)
    return out


def apply_zeros(digs: list[int], positions_1based: tuple[int, ...]) -> list[int]:
    out = digs[:]
    for p in positions_1based:
        out[p - 1] = 0
    return out


def to_int(digs: list[int]) -> int:
    n = 0
    for d in digs:
        n = n * 10 + d
    return n


def to_bytes(digs: list[int]) -> bytes:
    n = to_int(digs)
    if n == 0:
        return b"\x00"
    return n.to_bytes((n.bit_length() + 7) // 8, "big")


def show(label: str, raw: bytes, n: int = 8) -> None:
    head = raw[:n]
    tail = raw[-n:]
    bad = [i for i, b in enumerate(raw) if b not in PRINTABLE]
    letters = sum(chr(b).isalpha() for b in raw)
    print(
        f"  {label}: {len(raw)} bytes  head {head.hex()} {head!r}  "
        f"tail {tail.hex()} {tail!r}  printable {len(raw) - len(bad)}/{len(raw)}  "
        f"letters {letters}  bad {bad[:24]}{'...' if len(bad) > 24 else ''}"
    )


def expect(name: str, got: bytes, want: bytes) -> None:
    ok = got == want
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {want!r}")
    if not ok:
        raise SystemExit(1)


def controls(faed: str) -> list[int]:
    digs = digits_of(faed, 7)
    raw = to_bytes(digs)
    expect("unmasked low 4", raw[-4:], bytes.fromhex("c7bbc075"))
    expect("unmasked top 4", raw[:4], bytes.fromhex("1bd5951d"))
    z557 = to_bytes(apply_zeros(digs, (557,)))
    expect("zero 557 low 4", z557[-4:], b"yI u")
    ztail = to_bytes(apply_zeros(digs, TAIL4))
    expect("zero tail4 low 4", ztail[-4:], b"szqu")
    expect("tail letters", "".join(faed[p - 1] for p in TAIL4).encode(), b"badf")
    z13 = to_bytes(apply_zeros(digs, (1, 3)))
    expect("zero {1,3} top 2", z13[:2], b"yM")
    z12 = to_bytes(apply_zeros(digs, (1, 2)))
    expect("zero {1,2} top 2", z12[:2], b"?j")
    # The page's own integer reading, which is this same rule (o = 0).
    sal = (ART / "salphaseion.txt").read_text().strip()
    # spans from step 0: lastwords [766,829), thispassword [830,859)
    def page_int(block: str) -> bytes:
        n = int("".join("0" if c == "o" else str(ord(c) - 96) for c in block))
        return n.to_bytes((n.bit_length() + 7) // 8, "big")
    expect("lastwords", page_int(sal[766:829]), b"lastwordsbeforearchichoice")
    expect("thispassword", page_int(sal[830:859]), b"thispassword")
    flower_hash = hashlib.sha256(FLOWER.encode()).hexdigest()
    expect("creator #225", flower_hash.encode(), HASH225.encode())
    print(f"  faed[1,3,551,557,561,563] letters {''.join(faed[p - 1] for p in MASK6)!r}")
    return digs


def describe(raw: bytes) -> dict:
    bad = [i for i, b in enumerate(raw) if b not in PRINTABLE]
    interior = raw[2:-4]
    ibad = [i for i, b in enumerate(interior) if b not in PRINTABLE]
    return {
        "len": len(raw),
        "head": raw[:8].hex(),
        "tail": raw[-8:].hex(),
        "head_txt": raw[:8].decode("latin-1"),
        "tail_txt": raw[-8:].decode("latin-1"),
        "printable": len(raw) - len(bad),
        "bad": bad,
        "interior_len": len(interior),
        "interior_printable": len(interior) - len(ibad),
        "interior_bad": ibad,
        "text": raw.decode("latin-1"),
    }


def g_positions(text: str) -> list[int]:
    """1-based positions of g, excluding any that the mask already zeros."""
    return [i + 1 for i, c in enumerate(text) if c == "g" and (i + 1) not in MASK6]


def beam_g(base: list[int], text: str, mask: tuple[int, ...], depth: int = 2, beam: int = 40):
    """Flip up to `depth` interior g's from 7 to 0. Rank by printable count."""
    gs = [p for p in g_positions(text) if p not in mask]
    start = apply_zeros(base, mask)
    base_raw = to_bytes(start)
    base_score = sum(b in PRINTABLE for b in base_raw)
    print(f"  g-beam positions {len(gs)} depth {depth} start printable {base_score}/{len(base_raw)}")
    # state: frozenset of flipped 1-based positions, score, raw
    best = [(base_score, frozenset(), base_raw)]
    global_best = best[0]
    seen = {frozenset()}
    for d in range(depth):
        nxt = []
        for score, flips, _raw in best:
            for p in gs:
                if p in flips:
                    continue
                new_flips = flips | {p}
                if new_flips in seen:
                    continue
                seen.add(new_flips)
                digs = start[:]
                digs[p - 1] = 0  # g=7 -> 0
                raw = to_bytes(digs)
                sc = sum(b in PRINTABLE for b in raw)
                nxt.append((sc, new_flips, raw))
        nxt.sort(key=lambda t: t[0], reverse=True)
        # keep those that actually improved, capped
        nxt = [t for t in nxt if t[0] > base_score][:beam]
        if not nxt:
            print(f"  depth {d + 1}: no flip improved on {base_score}")
            return best[0]
        top = nxt[0]
        print(
            f"  depth {d + 1}: best {top[0]}/{len(top[2])} "
            f"flips {sorted(top[1])} head {top[2][:4]!r} tail {top[2][-4:]!r}"
        )
        if top[0] > global_best[0]:
            global_best = top
        best = nxt
        if top[0] == len(top[2]):
            return top
    return global_best


def matrix_strings() -> dict[str, str]:
    grid = (ART / "poster_grid.txt").read_text().splitlines()
    bit = [[1 if ch in "KB" else 0 for ch in row] for row in grid]
    rows = [sum(r) for r in bit]
    cols = [sum(bit[r][c] for r in range(14)) for c in range(14)]
    return {
        "row": "".join(str(n) for n in rows),
        "col": "".join(str(n) for n in cols),
        "255": "255",
        "161": "161",
    }


def tok23() -> str:
    """23 consumed colour tokens. Blue/off-white chunk 'b' -> 2, yellow 'be' -> 25."""
    colours = (ART / "yellowblue_colours.txt").read_text().strip()
    # The walk consumed 23 of 25 and left the final BY.
    used = colours[:23]
    if len(used) != 23 or colours[23:] != "BY":
        raise SystemExit(f"unexpected colour tail {colours!r}")
    return "".join("25" if c == "Y" else "2" for c in used)


def password_battery() -> dict:
    flower_hash = hashlib.sha256(FLOWER.encode()).hexdigest()
    assert flower_hash == HASH225
    lw = {
        "flower": FLOWER,
        "sha256hex(flower)": flower_hash,
        "sha256hex2(flower)": hashlib.sha256(flower_hash.encode()).hexdigest(),
        "thispassword": "thispassword",
    }
    yb = {
        "tok23": tok23(),
        "255": "255",
        "161": "161",
        "1510": "1510",
    }
    msl = matrix_strings()
    print("tok23", yb["tok23"])
    print("msl row", msl["row"])
    print("msl col", msl["col"])
    seps = ["", "-", "_", ":"]
    tails = [
        (),
        ("enter",),
        ("thispassword",),
        ("enter", "thispassword"),
    ]
    containers = load_containers()
    keep = ("terminal", "salphaseion_short", "cosmic")
    hits = []
    n = 0
    log_path = ART / "step3_attempts.jsonl"
    with log_path.open("w") as logf:
        for yk, yv in yb.items():
            for mk, mv in msl.items():
                for lk, lv in lw.items():
                    for sep in seps:
                        for tail in tails:
                            parts = [yv, mv, lv, *tail]
                            s = sep.join(parts)
                            forms = {
                                "plain": s,
                                "sha256hex": hashlib.sha256(s.encode()).hexdigest(),
                                "sha256hex2": hashlib.sha256(
                                    hashlib.sha256(s.encode()).hexdigest().encode()
                                ).hexdigest(),
                            }
                            for fk, answer in forms.items():
                                # Standard convention: EVP password = sha256 hex of the answer.
                                pw = hashlib.sha256(answer.encode()).hexdigest().encode()
                                label = f"yb={yk}|msl={mk}|lw={lk}|sep={sep or 'none'}|tail={'+'.join(tail) or 'none'}|{fk}"
                                for cname in keep:
                                    body, full = decrypt_with_password(containers[cname], pw)
                                    n += 1
                                    if body is None:
                                        kind = "no-pad"
                                    else:
                                        p = full[-1]
                                        textish = (
                                            len(body) >= 8
                                            and sum(b in PRINTABLE for b in body) >= len(body) * 0.9
                                            and sum(chr(b).isalpha() for b in body) >= 4
                                        )
                                        kind = "structured" if textish else ("pad-only-1" if p == 1 else f"pad-{p}")
                                    if kind not in ("no-pad", "pad-only-1"):
                                        rec = {
                                            "container": cname,
                                            "label": label,
                                            "answer_sha256": hashlib.sha256(answer.encode()).hexdigest(),
                                            "result": kind,
                                            "plaintext_hex": body.hex(),
                                        }
                                        print(f"  NEAR {cname} {kind} {label} {body[:80]!r}")
                                        hits.append(rec)
                                        logf.write(json.dumps(rec) + "\n")
                                    elif n % 5000 == 0:
                                        logf.write(json.dumps({"progress": n, "label": label}) + "\n")
    print(f"battery decrypts {n}, structured/long-pad hits {len(hits)}")
    return {"decrypts": n, "hits": hits, "tok23": yb["tok23"], "row": msl["row"], "col": msl["col"]}


def interpret(raw: bytes, label: str) -> list[dict]:
    """If the mask produced text, test it as a password and as an uncompressed key."""
    found = []
    text = raw.decode("latin-1")
    containers = load_containers()
    keep = ("terminal", "salphaseion_short", "cosmic")
    answers = {
        "text": text,
        "sha256hex": hashlib.sha256(raw).hexdigest(),
    }
    if all(chr(b) in "0123456789abcdef" for b in raw) and len(raw) == 64:
        answers["as-hex-key"] = text
    for name, answer in answers.items():
        pw = hashlib.sha256(answer.encode()).hexdigest().encode()
        for cname in keep:
            body, full = decrypt_with_password(containers[cname], pw)
            if body is not None and full[-1] != 1:
                print(f"  container {cname} {label}/{name} pad {full[-1]} {body[:80]!r}")
                found.append({"container": cname, "form": name, "pad": full[-1]})
        key = hashlib.sha256(answer.encode()).digest()
        got = pubkey_hash160s(key)
        if got and got["uncompressed"] == PRIZE_H160:
            print(f"  WIN uncompressed via sha256({label}/{name})")
            found.append({"win": key.hex()})
    if len(raw) == 32 and is_win_uncompressed(raw):
        print(f"  WIN raw 32 of {label}")
        found.append({"win": raw.hex()})
    return found


def main():
    faed = (ART / "faed.txt").read_text().strip()
    assert len(faed) == 570
    print("=== controls ===")
    digs = controls(faed)

    print("\n=== six-position zero mask ===")
    masked = apply_zeros(digs, MASK6)
    raw = to_bytes(masked)
    info = describe(raw)
    show("mask6 g=7", raw)
    interior = raw[2:-4]
    ibad = [i for i, b in enumerate(interior) if b not in PRINTABLE]
    print(f"  interior[2:-4] {len(interior)} bytes, nonprintable {len(ibad)}")
    if ibad:
        # cluster the failures so the refusal is a position list, not a shrug
        clusters = []
        start = prev = ibad[0]
        for i in ibad[1:]:
            if i == prev + 1:
                prev = i
            else:
                clusters.append((start, prev))
                start = prev = i
        clusters.append((start, prev))
        print(f"  interior bad clusters (relative to byte 2): {clusters[:30]}")
    (ART / "mask6.bin").write_bytes(raw)
    (ART / "mask6.txt").write_text(raw.decode("latin-1"))

    print("\n=== head {1,2} plus the same tail pin ===")
    raw12 = to_bytes(apply_zeros(digs, (1, 2, *TAIL4)))
    show("mask {1,2}+tail g=7", raw12)
    (ART / "mask12.bin").write_bytes(raw12)

    wins = []
    if info["printable"] == info["len"]:
        print("  FULLY PRINTABLE")
        wins.extend(interpret(raw, "mask6"))
    else:
        print("\n=== single and double g→0 flips on the mask6 integer ===")
        score, flips, best = beam_g(digs, faed, MASK6, depth=2, beam=30)
        if score == len(best):
            print("  a g-flip makes the whole string printable")
            show(f"flips {sorted(flips)}", best)
            (ART / "mask6_gflip.bin").write_bytes(best)
            wins.extend(interpret(best, "mask6-gflip"))
        else:
            print(f"  best g-flip still {score}/{len(best)} printable, flips {sorted(flips)}")

    print("\n=== password battery ===")
    battery = password_battery()
    summary = {
        "mask6": info,
        "mask12_head": raw12[:4].hex(),
        "mask12_tail": raw12[-4:].hex(),
        "mask12_len": len(raw12),
        "mask12_printable": sum(b in PRINTABLE for b in raw12),
        "wins": wins,
        "battery": battery,
    }
    (ART / "step3_summary.json").write_text(json.dumps(summary, indent=2))
    if wins or battery["hits"]:
        print("HIT")
    else:
        print("NO HIT")


if __name__ == "__main__":
    main()
