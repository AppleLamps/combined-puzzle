"""Reproducible rerun of mywork/LOG.md entry 5: zero out or remove letters of the
undecoded SalPhaseIon runs r1 = t[0:91] and r2 = t[195:765], then decode.

Hints combined: "primes" and "some characters need to be 'zeroed out'" (#8000),
"Yellow has a number and so does Blue" (#1710; poster counts B=15, Y=9, see
mywork2/yb_counts.out).

Mask = (position class C, letter subset S). A letter is selected when its index
is in C and its value is in S. Ops: 'zero' (selected -> digit 0) or 'remove'.
Letters a-i = 1-9, as in the solved a-i,o runs (STEPS.md step 5).
Decoders: dechex (decimal -> hex -> bytes, the method that solved the a-i,o runs),
scored by the longest a-z run; A1Z26 digit pairs and 3-digit ASCII triples, scored
by English word coverage (only when at least 80% of groups are valid letters).

Controls, run through the identical full search before the real runs:
  known runs t[766:829] and t[830:859] decode to their known words;
  planted runs: the known runs with their zeros hidden as a letter, which the
  search must rank first.
Null: r1 and r2 shuffled (fixed seed) through the same search.
Container check: top decodes are tried as answers under the STD convention
(password = sha256(answer) hex, EVP_BytesToKey SHA-256, AES-256-CBC) on the
terminal and SalPhaseIon short containers.

Run from the repo root: python mywork2/prime_zero.py
Writes mywork2/prime_zero.out and mywork2/prime_zero.json.
"""
import base64
import hashlib
import json
import random
import re
import sys
import time

import numpy as np
from Crypto.Cipher import AES

OUT_TXT = "mywork2/prime_zero.out"
OUT_JSON = "mywork2/prime_zero.json"
TOP = 15

t = re.sub(r"\s", "", open("files/salphaseion-textarea.txt").read())
assert len(t) == 1075 and t[765] == t[829] == t[859] == "z"
R1, R2 = t[0:91], t[195:765]
C1, C2 = t[766:829], t[830:859]
assert set(R1) <= set("abcdefghi") and set(R2) <= set("abcdefghi")

LOG = open(OUT_TXT, "w", encoding="utf-8", newline="\n")


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


# ---------- poster data (same grid and spiral as mywork2/yb_counts.py) ----------
GRID = [l.strip() for l in open("scratchpad_grid.txt") if l.strip()]


def spiral(n):
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    seen, out, r, c, d = set(), [], 0, 0, 0
    for _ in range(n * n):
        out.append((r, c))
        seen.add((r, c))
        dr, dc = dirs[d]
        if not (0 <= r + dr < n and 0 <= c + dc < n) or (r + dr, c + dc) in seen:
            d = (d + 1) % 4
            dr, dc = dirs[d]
        r, c = r + dr, c + dc
    return out


SPIRAL = [GRID[r][c] for r, c in spiral(14)]
ROWMAJ = list("".join(GRID))
assert SPIRAL.count("B") == 15 and SPIRAL.count("Y") == 9


def sieve(n):
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return s


PRIME = sieve(2000)


def classes(n):
    """Position classes for a run of length n, as {name: bool array}."""
    i = np.arange(n)
    pr = np.array([PRIME[k] for k in range(n + 30)], dtype=bool)
    cl = {"all": np.ones(n, bool),
          "prime0": pr[i], "prime1": pr[i + 1],
          "nonprime0": ~pr[i], "nonprime1": ~pr[i + 1]}
    for off in (9, 15, 24):  # positions shifted by the yellow, blue and total counts
        cl[f"prime(i+{off})"] = pr[i + off]
    for m in list(range(2, 11)) + [15, 24]:
        for k in range(m):
            cl[f"i%{m}=={k}"] = (i % m) == k
    for name, seq in (("spiral", SPIRAL), ("rowmaj", ROWMAJ)):
        s = np.array([seq[k % 196] for k in range(n)])
        cl[f"{name}:bit1"] = np.isin(s, ["K", "B"])
        cl[f"{name}:bit0"] = ~cl[f"{name}:bit1"]
        cl[f"{name}:B"] = s == "B"
        cl[f"{name}:Y"] = s == "Y"
        cl[f"{name}:BY"] = np.isin(s, ["B", "Y"])
    yb = np.array([1 if SPIRAL[k] == "B" else 0 for k in range(196) if SPIRAL[k] in "BY"])
    cl["yb24:1"] = yb[i % 24] == 1
    cl["yb24:0"] = yb[i % 24] == 0
    return cl


SUBSETS = [[v for v in range(1, 10) if m >> (v - 1) & 1] for m in range(1, 512)]
LOWER = bytes(range(97, 123))


def build_words():
    """English words (4-12 letters, seen at least twice) from the Python docs
    shipped with CPython, plus the decoded puzzle texts. Used only to score the
    pair and triple decoders, which zeroing can make trivially 'valid'."""
    import pydoc_data.topics as T
    from collections import Counter
    cnt = Counter(w for v in T.topics.values() for w in re.findall(r"[a-z]+", v.lower()))
    words = {w for w, c in cnt.items() if 4 <= len(w) <= 12 and c >= 2}
    words |= {"matrix", "prime", "primes", "yellow", "blue", "choice", "password", "enter",
              "last", "words", "before", "yinyang", "seed", "planted", "private", "half",
              "better", "funds", "live", "rabbit", "door", "hidden", "zero", "zeros"}
    return words


WORDS = build_words()


def coverage(text):
    n = len(text)
    if n == 0:
        return 0.0
    cov = bytearray(n)
    for a in range(n):
        for L in range(4, 13):
            if a + L > n:
                break
            if text[a:a + L] in WORDS:
                cov[a:a + L] = b"" * L
    return sum(cov) / n
RUN_RE = re.compile(rb"[a-z]+")


def dechex_bytes(digs):
    n = int(digs)
    if n == 0:
        return b""
    return n.to_bytes((n.bit_length() + 7) // 8, "big")


def longest_true(mask):
    if not mask.any():
        return 0
    d = np.diff(np.concatenate(([0], mask.astype(np.int8), [0])))
    return int((np.flatnonzero(d == -1) - np.flatnonzero(d == 1)).max())


def score_all(vals):
    """vals: int8 digit array. Returns {decoder: (primary, letter fraction)}. The primary
    score is the longest a-z run for dechex and English word coverage for a1z26/ascii3."""
    res = {}
    b = dechex_bytes(vals.astype(np.uint8).__add__(48).tobytes().decode())
    if b:
        low = len(b) - len(b.translate(None, LOWER))
        runs = RUN_RE.findall(b)
        res["dechex"] = (max(map(len, runs)) if runs else 0, low / len(b))
    else:
        res["dechex"] = (0, 0.0)
    v = vals.astype(np.int16)
    if len(v) >= 2:
        p = 10 * v[0:len(v) // 2 * 2:2] + v[1:len(v) // 2 * 2:2]
        ok = (p >= 1) & (p <= 26)
        frac = float(ok.mean())
        cov = coverage(np.where(ok, p + 96, 46).astype(np.uint8).tobytes().decode()) if frac >= 0.8 else 0.0
        res["a1z26"] = (round(cov, 4), frac)
    if len(v) >= 3:
        q = 100 * v[0:len(v) // 3 * 3:3] + 10 * v[1:len(v) // 3 * 3:3] + v[2:len(v) // 3 * 3:3]
        ok = (q >= 97) & (q <= 122)
        frac = float(ok.mean())
        cov = coverage(np.where(ok, q, 46).astype(np.uint8).tobytes().decode()) if frac >= 0.8 else 0.0
        res["ascii3"] = (round(cov, 4), frac)
    return res


def render(vals, dec):
    digs = (vals.astype(np.uint8) + 48).tobytes().decode()
    if dec == "dechex":
        return dechex_bytes(digs).decode("latin-1")
    if dec == "a1z26":
        return "".join(chr(96 + int(digs[k:k + 2])) if 1 <= int(digs[k:k + 2]) <= 26 else "."
                       for k in range(0, len(digs) - 1, 2))
    return "".join(chr(int(digs[k:k + 3])) if 97 <= int(digs[k:k + 3]) <= 122 else "."
                   for k in range(0, len(digs) - 2, 3))


def search(run, label):
    """Apply every (class, subset, op) mask to run; keep the top TOP per decoder."""
    t0 = time.time()
    raw = np.array([0 if ch == "o" else ord(ch) - 96 for ch in run], dtype=np.int8)
    cl = classes(len(run))
    seen = set()
    best = {d: [] for d in ("dechex", "a1z26", "ascii3")}
    tried = 0
    for cname, cmask in cl.items():
        for S in SUBSETS:
            sel = cmask & np.isin(raw, S)
            if not sel.any():
                continue
            for op in ("zero", "remove"):
                vals = np.where(sel, 0, raw) if op == "zero" else raw[~sel]
                if len(vals) == 0:
                    continue
                key = (op == "zero", vals.tobytes())
                if key in seen:
                    continue
                seen.add(key)
                tried += 1
                for dec, sc in score_all(vals).items():
                    lst = best[dec]
                    lst.append((sc, cname, "".join("abcdefghi"[s - 1] for s in S), op))
                    if len(lst) > 4 * TOP:
                        lst.sort(key=lambda x: x[0], reverse=True)
                        del lst[TOP:]
    for dec in best:
        best[dec].sort(key=lambda x: x[0], reverse=True)
        del best[dec][TOP:]
    say(f"[{label}] len={len(run)} classes={len(cl)} distinct masked strings={tried} "
        f"({time.time() - t0:.0f}s)")
    out = {}
    for dec, lst in best.items():
        rows = []
        for (run_len, frac), cname, sub, op in lst:
            sel = cl[cname] & np.isin(raw, [ord(ch) - 96 for ch in sub])
            vals = np.where(sel, 0, raw) if op == "zero" else raw[~sel]
            text = render(vals, dec)
            rows.append({"primary": run_len, "letter_frac": round(frac, 4), "class": cname,
                         "subset": sub, "op": op, "decode": text})
        out[dec] = rows
        say(f"  {dec}: best primary {rows[0]['primary'] if rows else 0}, "
            f"best letter fraction {max((r['letter_frac'] for r in rows), default=0)}")
        for r in rows[:5]:
            shown = r["decode"][:70].encode("unicode_escape").decode()
            say(f"    primary={r['primary']:>6} frac={r['letter_frac']:.3f} {r['op']:6} "
                f"{r['class']:>14} {{{r['subset']}}} {shown}")
    return out


# ---------- container oracle ----------
def load(name):
    return base64.b64decode(re.sub(r"\s", "", open(f"files/{name}").read()))


CONTAINERS = {n: load(n) for n in ("terminal.b64", "salphaseion-short.b64")}


def evp(pw, salt):
    d, prev = b"", b""
    while len(d) < 48:
        prev = hashlib.sha256(prev + pw + salt).digest()
        d += prev
    return d[:32], d[32:48]


def try_answer(ans):
    hits = []
    pw = hashlib.sha256(ans.encode("latin-1")).hexdigest().encode()
    for name, raw in CONTAINERS.items():
        k, iv = evp(pw, raw[8:16])
        p = AES.new(k, AES.MODE_CBC, iv).decrypt(raw[16:])
        n = p[-1]
        if 1 <= n <= 16 and p[-n:] == bytes([n]) * n:
            body = p[:-n]
            pr = sum(32 <= c < 127 for c in body) / max(1, len(body))
            if pr > 0.9 or re.fullmatch(rb"[0-9a-fA-F]{64}", body):
                hits.append((name, body))
    return hits


# phase 3.2 container as a positive control of the oracle code
def oracle_control():
    raw = load("phase3.2.b64")
    return raw[:8] == b"Salted__"


# ---------- main ----------
say("prime_zero.py", time.strftime("%Y-%m-%d %H:%M:%S"), "python", sys.version.split()[0])
say("hints: primes + zeroed out (#8000), yellow 9 / blue 15 (#1710, mywork2/yb_counts.out)")
results = {"controls": {}, "real": {}, "null": {}, "container_hits": []}

say("\n== controls ==")
for name, run, want in (("known t[766:829]", C1, "lastwordsbeforearchichoice"),
                        ("known t[830:859]", C2, "thispassword")):
    got = render(np.array([0 if ch == "o" else ord(ch) - 96 for ch in run], dtype=np.int8), "dechex")
    say(f"{name}: dechex -> {got!r} ok={got == want}")
    assert got == want


def plant(run):
    """Hide the zeros of a known run as one letter, using the first (class, letter)
    for which that hiding is exactly recoverable by a 'zero' mask."""
    z = [k for k, ch in enumerate(run) if ch == "o"]
    for cname, cmask in classes(len(run)).items():
        if not all(cmask[k] for k in z):
            continue
        present = {run[k] for k in range(len(run)) if cmask[k] and run[k] != "o"}
        for letter in "abcdefghi":
            if letter not in present:
                return cname, letter, "".join(letter if ch == "o" else ch for ch in run)
    return None


for name, run, want in (("planted t[766:829]", C1, "lastwordsbeforearchichoice"),
                        ("planted t[830:859]", C2, "thispassword")):
    cname, letter, hidden = plant(run)
    say(f"{name}: zeros hidden as '{letter}' on class {cname}; hidden run has no 'o': {'o' not in hidden}")
    res = search(hidden, name)
    top = res["dechex"][0]
    ok = top["decode"] == want
    say(f"  top dechex decode == {want!r}: {ok}")
    results["controls"][name] = {"class": cname, "letter": letter, "recovered_at_rank_1": ok,
                                 "top": res["dechex"][:3]}
    assert ok

# removal control: insert a letter absent from the run at fixed random places
rng = random.Random(8000)
absent = [l for l in "abcdefghi" if l not in C2][0]
ins = list(C2)
for _ in range(6):
    ins.insert(rng.randrange(len(ins) + 1), absent)
ins = "".join(ins)
res = search(ins, f"planted-remove t[830:859] (+6 '{absent}')")
ok = res["dechex"][0]["decode"] == "thispassword"
say(f"  top dechex decode == 'thispassword': {ok}")
results["controls"]["planted-remove"] = {"letter": absent, "recovered_at_rank_1": ok}
assert ok

say("\n== real runs ==")
real_runs = {"r1": R1, "r1rev": R1[::-1], "r2": R2, "r2rev": R2[::-1],
             "r1+r2": R1 + R2, "r2+r1": R2 + R1}
for name, run in real_runs.items():
    results["real"][name] = search(run, name)

say("\n== null (shuffled, seed 1710) ==")
rng = random.Random(1710)
for name, run in (("r1", R1), ("r2", R2)):
    s = list(run)
    rng.shuffle(s)
    res = search("".join(s), f"shuffled {name}")
    results["null"][name] = {d: {"best_primary": rows[0]["primary"] if rows else 0,
                                 "best_frac": max((r["letter_frac"] for r in rows), default=0)}
                             for d, rows in res.items()}

say("\n== container check ==")
tried = 0
for name, per_dec in results["real"].items():
    for dec, rows in per_dec.items():
        for r in rows:
            cands = {r["decode"], "".join(re.findall(r"[a-z]", r["decode"]))}
            cands |= set(re.findall(r"[a-z]{4,}", r["decode"]))
            for c in cands:
                if not c:
                    continue
                tried += 1
                for hit in try_answer(c):
                    results["container_hits"].append({"run": name, "decoder": dec, "answer": c,
                                                      "container": hit[0], "plaintext": hit[1].hex()})
                    say("HIT", name, dec, repr(c), hit[0], hit[1][:80])
say(f"answers tried on 2 containers: {tried}, structured hits: {len(results['container_hits'])}")

json.dump(results, open(OUT_JSON, "w", encoding="utf-8", newline="\n"), indent=1)
say("wrote", OUT_JSON)
