"""Focused closed-system reading of `matrixsumlist lastwordsbeforearchichoice`.

The 2026-09-13 pipeline selected whole words modulo a target passage and reported
that word scoring had no power. It did not take the *last letters of the selected
words*, and modulo wrapping was not separated from direct indexing. This audit does
both, using only the local puzzle/transcript and the already-sealed sum lists.
No network, envelope bytes, or AES.
"""
import hashlib, json, random, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "runs/2026-09-14_matrixsum_lastwords"
OUT.mkdir(parents=True, exist_ok=True)
SUMS = json.loads((ROOT / "runs/2026-09-13_matrixsum_pipeline/sum_lists.json").read_text())

def words(s): return re.findall(r"[A-Za-z]+", s.upper())
def sha(b): return hashlib.sha256(b).hexdigest()
def score(s):
    tri = ["THE","AND","ING","ION","ENT","TIO","FOR","HER","TER","HAT","THA","ERE",
           "ATE","HIS","CON","RES","VER","ALL","ONS","NCE","MEN","ITH","TED","ERS",
           "PRO","THI","WIT","ARE","ESS","NOT","KEY","PASS","WORD","HASH","SHA"]
    return sum(s.upper().count(x) for x in tri)

src_lines = (ROOT / "reference_texts/matrix_reloaded_architect_scene_transcript.txt").read_text().splitlines()
# Before Neo's explicit utterance "Choice" (line 26): the source passage beginning at
# "Your life" and ending with the Architect's preceding statement at line 24.
full_before_choice = " ".join(src_lines[i] for i in [11,13,15,17,19,21,23])
# Architect utterances only, excluding Neo's interjections, over the same boundary.
arch_before_choice = " ".join(src_lines[i] for i in [11,15,19,23])
# Immediate last Architect utterance before Choice.
immediate_before_choice = src_lines[23]
# Puzzle's own closest cut: before its SELECT verb (no literal CHOICE exists).
puzzle_text = (DATA / "architect_plaintext_readable.txt").read_text()
puzzle_words = words(puzzle_text)
select_at = puzzle_words.index("SELECT")
TARGETS = {
    "source_full_before_choice": words(full_before_choice),
    "source_architect_before_choice": words(arch_before_choice),
    "source_immediate_before_choice": words(immediate_before_choice),
    "puzzle_before_select": puzzle_words[:select_at],
}

def select_direct(ws, nums, base):
    idx = [abs(n) - 1 if base == 1 else abs(n) for n in nums if n != 0]
    if not idx or any(i < 0 or i >= len(ws) for i in idx): return None
    return [ws[i] for i in idx]

def select_mod(ws, nums, base):
    return [ws[(abs(n) - 1 if base == 1 else abs(n)) % len(ws)] for n in nums if n != 0]

def extracts(sel):
    if not sel: return {}
    return {
        "whole_joined": "".join(sel),
        "initials": "".join(w[0] for w in sel),
        "finals": "".join(w[-1] for w in sel),
        "lengths_A1": "".join(chr(64 + len(w)) if 1 <= len(w) <= 26 else "?" for w in sel),
        "lengths_mod26": "".join(chr(65 + len(w) % 26) for w in sel),
    }

results = []
for lname, nums in SUMS.items():
    for tname, ws in TARGETS.items():
        for base in (0, 1):
            for mode, fn in (("direct", select_direct), ("modulo", select_mod)):
                sel = fn(ws, nums, base)
                if not sel: continue
                for ename, out in extracts(sel).items():
                    results.append({"sumlist": lname, "target": tname, "base": base,
                                    "index_mode": mode, "extract": ename,
                                    "selected_words": sel, "output": out,
                                    "score": score(out) if ename != "whole_joined" else 0})

# Controls preserve each real list's length and value multiset, but shuffle the sums.
rng = random.Random(20260914)
control_max = {e: 0 for e in ["initials","finals","lengths_A1","lengths_mod26"]}
control_n = 0
for lname, nums in SUMS.items():
    for _ in range(20):
        sh = list(nums); rng.shuffle(sh)
        for tname, ws in TARGETS.items():
            for base in (0, 1):
                for fn in (select_direct, select_mod):
                    sel = fn(ws, sh, base)
                    if not sel: continue
                    for ename, out in extracts(sel).items():
                        if ename == "whole_joined": continue
                        control_max[ename] = max(control_max[ename], score(out)); control_n += 1

above = [r for r in results if r["extract"] != "whole_joined" and
         r["score"] > control_max[r["extract"]]]
top = sorted([r for r in results if r["extract"] != "whole_joined"],
             key=lambda r: (-r["score"], r["sumlist"]))[:30]
print(f"targets: { {k: len(v) for k,v in TARGETS.items()} }")
print(f"sum lists: {len(SUMS)}; outputs: {len(results)}; controls: {control_n}")
print("control maxima", control_max)
for r in top[:15]:
    flag = " ABOVE" if r in above else ""
    print(f" score {r['score']:2d}/{control_max[r['extract']]} {r['extract']} {r['index_mode']} b{r['base']} "
          f"{r['target']} {r['sumlist']} {r['output'][:90]!r}{flag}")

# Exact non-EC oracle: DBBI token equality pattern. Address checks were exhausted for
# these same sum-list/string families; retain the strongest exact local gate here.
PAT = "01234556728966286abc61c88b48de3086dd501d5557d6bab5605233df7bbb96"
def eqpat(h):
    seen = {}
    return "".join("0123456789abcdef"[seen.setdefault(c, len(seen))] if len(seen) < 16 or c in seen else "?" for c in h)
oracle = [r for r in results if eqpat(sha(r["output"].encode())) == PAT]

(OUT / "manifest.json").write_text(json.dumps({
    "date": "2026-09-14", "closed_system": True, "network": False,
    "envelope_bytes_read": 0, "aes_decryptions": 0,
    "sum_lists": len(SUMS), "targets": {k: len(v) for k,v in TARGETS.items()},
    "index_modes": ["direct", "modulo"], "bases": [0,1],
    "extracts": ["whole_joined","initials","finals","lengths_A1","lengths_mod26"],
    "controls_per_sumlist": 20, "control_max": control_max
}, indent=1) + "\n")
(OUT / "results.json").write_text(json.dumps({
    "outputs": len(results), "controls": control_n, "above_control": above,
    "dbbi_pattern_hits": oracle, "top": top
}, indent=1) + "\n")
(OUT / "all_outputs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in results))
print(f"above controls: {len(above)}; DBBI-pattern hits: {len(oracle)}")
print("WROTE", OUT)