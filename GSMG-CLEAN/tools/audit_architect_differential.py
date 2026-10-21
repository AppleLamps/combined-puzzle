"""Closed-system audit of the modified Architect speech against its film source.

Tests the literal instruction RETURN TO THE SOURCE CODES ... REINSERTING THE PRIME
BASICS on the *difference* between the local source transcript and puzzle rewrite.
No network, envelope bytes, or AES. Outputs are accepted only as complete readable
instructions or by exact DBBI/address oracles.
"""
import difflib, hashlib, json, re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "runs/2026-09-14_architect_differential"
OUT.mkdir(parents=True, exist_ok=True)

def words(s): return re.findall(r"[A-Za-z]+", s.upper())
def letters(s): return "".join(words(s))
def sha(b): return hashlib.sha256(b).hexdigest()
def prime(n): return n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))

puzzle_text = (DATA / "architect_plaintext_readable.txt").read_text(encoding="utf-8")
source_text = (ROOT / "reference_texts/matrix_reloaded_architect_scene_transcript.txt").read_text(encoding="utf-8")

# Closed local excerpts. The broad excerpt includes all intervening source dialogue;
# the tight excerpt keeps only passages visibly represented by the puzzle rewrite.
source_lines = source_text.splitlines()
broad = " ".join(source_lines[i] for i in [11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39])
tight = " ".join(source_lines[i] for i in [11, 13, 15, 37, 39])
SOURCES = {"broad": broad, "tight": tight}
PW = words(puzzle_text)

def alignment(src):
    sw = words(src)
    m = difflib.SequenceMatcher(a=sw, b=PW, autojunk=False)
    edits, inserted, removed, paired = [], [], [], []
    for tag, a0, a1, b0, b1 in m.get_opcodes():
        if tag == "equal": continue
        ss, pp = sw[a0:a1], PW[b0:b1]
        edits.append({"tag": tag, "source_range": [a0, a1], "puzzle_range": [b0, b1],
                      "source": ss, "puzzle": pp})
        removed.extend(ss); inserted.extend(pp)
        if tag == "replace":
            for x, y in zip(ss, pp): paired.append((x, y))
    return sw, edits, inserted, removed, paired

def streams(sw, edits, ins, rem, paired):
    out = {
        "puzzle_only_words": ins,
        "source_only_words": rem,
        "puzzle_only_initials": [w[0] for w in ins],
        "puzzle_only_finals": [w[-1] for w in ins],
        "source_only_initials": [w[0] for w in rem],
        "source_only_finals": [w[-1] for w in rem],
        "puzzle_only_lengths": [len(w) for w in ins],
        "source_only_lengths": [len(w) for w in rem],
        "edit_tags": [e["tag"] for e in edits],
        "edit_puzzle_first": [e["puzzle"][0][0] for e in edits if e["puzzle"]],
        "edit_puzzle_last": [e["puzzle"][-1][-1] for e in edits if e["puzzle"]],
        "edit_source_first": [e["source"][0][0] for e in edits if e["source"]],
        "edit_source_last": [e["source"][-1][-1] for e in edits if e["source"]],
        "paired_initial_delta": [(ord(y[0]) - ord(x[0])) % 26 for x, y in paired],
        "paired_final_delta": [(ord(y[-1]) - ord(x[-1])) % 26 for x, y in paired],
        "paired_length_delta": [len(y) - len(x) for x, y in paired],
    }
    # Full edit-block payloads, preserving boundaries with X (not treated as text).
    out["puzzle_edit_blocks"] = [letters(" ".join(e["puzzle"])) for e in edits]
    out["source_edit_blocks"] = [letters(" ".join(e["source"])) for e in edits]
    return out

def render(v):
    if not v: return ""
    if isinstance(v[0], str):
        if all(len(x) == 1 for x in v): return "".join(v)
        return "".join(v)
    return "".join(chr(65 + n % 26) for n in v)

PRIMES = [n for n in range(2, 5000) if prime(n)]
COLORS = (DATA / "poster_spiral_bits.txt").read_text().splitlines()[1]
P24 = PRIMES[:24]
BLUE_ORD = [i + 1 for i, c in enumerate(COLORS) if c == "B"]
YELLOW_ORD = [i + 1 for i, c in enumerate(COLORS) if c == "Y"]
SELECTORS = {"first23_primes": PRIMES[:23], "first24_primes": P24,
             "blue_ordinals": BLUE_ORD, "yellow_ordinals": YELLOW_ORD,
             "blue_prime_values": [p for p, c in zip(P24, COLORS) if c == "B"],
             "yellow_prime_values": [p for p, c in zip(P24, COLORS) if c == "Y"]}

def select(seq, idxs, base):
    out = []
    for x in idxs:
        i = x - 1 if base == 1 else x
        if 0 <= i < len(seq): out.append(seq[i])
    return out

TRI = ["THE", "AND", "ING", "ION", "ENT", "TIO", "FOR", "HER", "TER", "HAT",
       "THA", "ERE", "ATE", "HIS", "CON", "RES", "VER", "ALL", "ONS", "NCE",
       "MEN", "ITH", "TED", "ERS", "PRO", "THI", "WIT", "ARE", "ESS", "NOT"]
def score(s): return sum(s.upper().count(x) for x in TRI)

all_results, alignments = [], {}
for name, src in SOURCES.items():
    sw, edits, ins, rem, paired = alignment(src)
    alignments[name] = {"source_words": len(sw), "puzzle_words": len(PW),
                        "matching_words": sum(b.size for b in difflib.SequenceMatcher(a=sw, b=PW, autojunk=False).get_matching_blocks()),
                        "edits": edits}
    for sname, seq in streams(sw, edits, ins, rem, paired).items():
        if not seq: continue
        # Flatten block streams both with and without explicit X boundaries.
        seqs = [("direct", seq)]
        if isinstance(seq[0], str) and any(len(x) > 1 for x in seq):
            seqs += [("blocks_joined", list("".join(seq))),
                     ("blocks_X", list("X".join(seq)))]
        for mode, actual in seqs:
            base_text = render(actual)
            all_results.append({"source": name, "stream": sname, "mode": mode,
                                "selector": "identity", "base": None,
                                "output": base_text, "score": score(base_text)})
            for qname, idxs in SELECTORS.items():
                for base in (0, 1):
                    got = select(actual, idxs, base)
                    text = render(got)
                    if text:
                        all_results.append({"source": name, "stream": sname, "mode": mode,
                                            "selector": qname, "base": base,
                                            "output": text, "score": score(text)})

top = sorted(all_results, key=lambda r: (-r["score"], -len(r["output"])))[:30]
print(f"alignments: broad {alignments['broad']['source_words']} words, tight {alignments['tight']['source_words']} words; puzzle {len(PW)}")
print(f"{len(all_results)} differential outputs")
for r in top[:12]:
    print(f" score {r['score']:2d} {r['source']}/{r['stream']}/{r['mode']}/{r['selector']}/b{r['base']} {r['output'][:80]!r}")

(OUT / "manifest.json").write_text(json.dumps({
    "date": "2026-09-14", "closed_system": True, "network": False,
    "envelope_bytes_read": 0, "aes_decryptions": 0,
    "sources": {k: {"words": len(words(v)), "sha256": sha(v.encode())} for k, v in SOURCES.items()},
    "puzzle": {"words": len(PW), "sha256": sha(puzzle_text.encode())},
    "selectors": SELECTORS,
    "scope": "word-level source/puzzle differential; edit streams; prime and colour selectors"
}, indent=1) + "\n")
(OUT / "alignments.json").write_text(json.dumps(alignments, indent=1) + "\n")
(OUT / "results.json").write_text(json.dumps({"outputs": len(all_results), "top": top,
                                                "all": all_results}, indent=1) + "\n")
print("WROTE", OUT)