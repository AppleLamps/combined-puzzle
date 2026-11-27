"""Replay with python -B replay.py [new-output-directory]."""
import ast, base64, hashlib, json, re, sys
from pathlib import Path
RUN = Path(__file__).resolve().parent
CLEAN = RUN.parents[1]
LEGACY = CLEAN.parent / "5g-puzzle/analysis/lastwords.py"
PHASE = CLEAN / "data/phase3_2_plaintext.bin"
PREVIOUS = RUN.parent / "2026-11-27_fresh_eyes_candidates"
FRESH = PREVIOUS / "candidates.txt"
def digest(b):
    return hashlib.sha256(b).hexdigest()
def list_bytes(words):
    return "".join(word + "\n" for word in words).encode("ascii")

import runpy
from math import comb

sys.path.insert(0, str(CLEAN / "tools"))
import prereg
import check_candidate as cc

def generate():
    source = ast.parse(LEGACY.read_bytes())
    values = {node.targets[0].id: ast.literal_eval(node.value) for node in source.body
              if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
              and node.targets[0].id in {"S", "PRE", "DIG", "EXTRA"}}
    form_node, = [node for node in source.body if isinstance(node, ast.FunctionDef) and node.name == "forms"]
    scope = {"re": re}
    exec(compile(ast.Module(body=[form_node], type_ignores=[]), str(LEGACY), "exec"), scope)
    data = PHASE.read_bytes()
    lines = {}
    for name, literal in (("PRE", "PRE"), ("DIG", "DIG"), ("RID", "S")):
        pattern = values[literal].encode("ascii")
        assert data.count(pattern) == 1
        start = data.index(pattern)
        stop = start + len(pattern)
        assert data[start-2:start] == data[stop:stop+2] == b"\r\n"
        lines[name] = {"start": start, "stop": stop, "text": data[start:stop].decode("ascii")}
    origins = {}
    for base in ("PRE", "DIG", "PRE+DIG", "DIG+PRE", "PRE+RID", "DIG+RID", "RID+DIG"):
        raw = "".join(lines[part]["text"] for part in base.split("+"))
        for form in scope["forms"](raw):
            for extra in values["EXTRA"]:
                for word in (form + extra, extra + form):
                    origins.setdefault(word, set()).add(extra)
    excluded = set(FRESH.read_text().splitlines()) & origins.keys()
    words = sorted(origins.keys() - excluded)
    tags = {i: sorted(e for e in origins[w] if "yinyang" in e)
            for i, w in enumerate(words, 1) if any("yinyang" in e for e in origins[w])}
    return words, lines, tags, sorted(excluded)

def stats(n, k):
    below = sum(comb(n, j) * 255 ** (n - j) for j in range(k))
    return {"decrypts": n, "pad1": k, "expected": n / 256,
            "p_at_least_observed": (256 ** n - below) / 256 ** n}


def run(root):
    assert __debug__
    seal = prereg.verify(RUN)
    plan = prereg.load(RUN)
    for path, expected in plan["sources"].items():
        raw = (CLEAN.parent / path).read_bytes()
        hashes = {digest(raw)}
        if not path.endswith(".bin"):
            lf = raw.replace(b"\r\n", b"\n")
            hashes.update([digest(lf), digest(lf.replace(b"\n", b"\r\n"))])
        assert expected in hashes, path
    words, lines, tags, excluded = generate()
    assert lines == plan["operand"] and excluded == plan["excluded"]
    assert len(words) == plan["candidate_bound"] and digest(list_bytes(words)) == plan["candidates_sha256_lf"]
    assert {n:digest(b) for n,b in cc.ENVELOPES.items()} == plan["envelope_sha256"]
    root.mkdir(exist_ok=True, parents=True)
    if (root / "results.json").exists():
        raise SystemExit("Specify a fresh output directory to reproduce.")
    (root / "candidates.txt").write_bytes(list_bytes(words))
    (root / "solver_only_extra.json").write_bytes((json.dumps(tags, separators=(",", ":"))+"\n").encode())
    scan = runpy.run_path(str(PREVIOUS / "replay.py"))["scan"]
    cc.selftest()
    fixture = plan["fixture"]
    targets = cc.TARGETS.copy()
    assert set(targets) == set(plan["real_target_hash160"])
    cc.TARGETS[fixture["key_hash160"]] = "PLANTED k=1"
    try:
        control_hist, control_records = scan(FRESH.read_text().splitlines(),
            {"planted":base64.b64decode(fixture["envelope_base64"])}, root, "controls")
    finally:
        del cc.TARGETS[fixture["key_hash160"]]
    assert targets == cc.TARGETS
    previous = json.loads((PREVIOUS / "results.json").read_bytes())["controls"]
    assert control_records == previous["retained_and_scanned"]
    positive, = [r for r in control_records if r["candidate"] == fixture["answer"]]
    assert (positive["sha256"],positive["bytes"],positive["pad"]) == (fixture["plaintext_sha256"],207,1)
    assert {k.split("@")[0] for k in positive["find_keys_hits"]} == {"raw32","WIF","hex64","base64"}

    histograms, retained = scan(words, cc.ENVELOPES, root, "outputs")
    per_env = {name: stats(sum(hist.values()), hist.get(1,0)) for name,hist in histograms.items()}
    assert all(s["decrypts"] == len(words) for s in per_env.values())
    result = {"seal":seal, "profile":"gsmg", "unique_before_exclusion":len(words)+len(excluded),
              "excluded":excluded, "candidate_count":len(words), "solver_only_extra_candidates":len(tags),
              "histograms":histograms, "pad1":per_env,
              "pooled":stats(len(words)*len(histograms),sum(s["pad1"] for s in per_env.values())),
              "pad_ge2":sum(r["pad"]>=2 for r in retained), "retained_and_scanned":retained,
              "plaintexts_with_key_hits":sum(bool(r["find_keys_hits"]) for r in retained),
              "controls":{"selftest":True,"planted_passed":True,"targets_restored":True,
                          "histogram":control_hist,"retained_and_scanned":control_records}}
    (root/"results.json").write_bytes((json.dumps(result,indent=2)+"\n").encode())
    print(json.dumps(per_env))


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Assertions must be enabled.")
    run(Path(sys.argv[1]) if len(sys.argv)>1 else RUN)

