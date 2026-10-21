"""Recursive key-format audit over every retained 2026-09-14 structural output.

Scans raw/decoded bytes for BE/LE 32-byte scalars, 64-hex, WIF, base64-to-32,
decimal scalars, and explicit 32+32 halves. Reports both syntactic key shapes and
exact target matches. No AES or envelope reads.
"""
import base64, hashlib, json, re
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runs/2026-09-14_structural_key_formats"
OUT.mkdir(parents=True, exist_ok=True)
RUNS = ROOT / "runs"
SOURCES = [
    RUNS / "2026-09-14_m4_zeroing_oracles/candidates.jsonl",
    RUNS / "2026-09-14_pointer_selectors/candidates.jsonl",
    RUNS / "2026-09-14_board_shape_sums/all_outputs.jsonl",
    RUNS / "2026-09-14_colour_selectors/all_outputs.jsonl",
    RUNS / "2026-09-14_keyed_faed/all_outputs.jsonl",
    RUNS / "2026-09-14_tail_cipher/all_outputs.jsonl",
    RUNS / "2026-09-14_matrixsum_lastwords/all_outputs.jsonl",
]
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def b58raw(s):
    n = 0
    for c in s: n = n * 58 + B58.index(c)
    return n.to_bytes(max(1, (n.bit_length() + 7) // 8), "big")

def wif_scalar(s):
    try: raw = b58raw(s)
    except ValueError: return None
    if len(raw) not in (37, 38): return None
    body, check = raw[:-4], raw[-4:]
    if hashlib.sha256(hashlib.sha256(body).digest()).digest()[:4] != check: return None
    if body[:1] != b"\x80" or len(body) not in (33, 34): return None
    if len(body) == 34 and body[-1] != 1: return None
    k = int.from_bytes(body[1:33], "big")
    return k if 1 <= k < N else None

def b58check_h160(s):
    raw = b58raw(s)
    if len(raw) < 25: raw = b"\0" * (25 - len(raw)) + raw
    assert len(raw) == 25 and hashlib.sha256(hashlib.sha256(raw[:-4]).digest()).digest()[:4] == raw[-4:]
    return raw[1:21].hex()

TARGETS = {b58check_h160(a): a for a in [
    "18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc", "1AD2wfwXukZ1kUAy848hTQQ72aSBZPB75r",
    "13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp", "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe",
    "17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa"]}

# Positive controls use the known phase-1 marker scalar. They prove that WIF,
# hex64, base64-32 and both explicit 32-byte halves converge on the same key.
CONTROL_K = int(hashlib.sha256(
    b"theflowerblossomsthroughwhatseemstobeaconcretesurface").hexdigest(), 16)
CONTROL_RAW = CONTROL_K.to_bytes(32, "big")
def b58encode(raw):
    n = int.from_bytes(raw, "big")
    out = ""
    while n: out, n = B58[n % 58] + out, n // 58
    return "1" * (len(raw) - len(raw.lstrip(b"\0"))) + out
def control_wif(compressed):
    body = b"\x80" + CONTROL_RAW + (b"\x01" if compressed else b"")
    return b58encode(body + hashlib.sha256(hashlib.sha256(body).digest()).digest()[:4])

try:
    from coincurve import PrivateKey
    def scalar_hits(k):
        if not 1 <= k < N: return []
        p = PrivateKey(k.to_bytes(32, "big")).public_key
        out = []
        for comp, label in ((True, "compressed"), (False, "uncompressed")):
            pub = p.format(compressed=comp)
            h = hashlib.new("ripemd160", hashlib.sha256(pub).digest()).hexdigest()
            if h in TARGETS: out.append((TARGETS[h], label))
        return out
    BACKEND = "coincurve"
except ImportError:
    import check_candidate as cc
    scalar_hits, BACKEND = cc.scalar_hits, "pure-python"

CONTROL_WIF_U = control_wif(False)
CONTROL_WIF_C = control_wif(True)
CONTROLS = {
    "wif_uncompressed": wif_scalar(CONTROL_WIF_U) == CONTROL_K,
    "wif_compressed": wif_scalar(CONTROL_WIF_C) == CONTROL_K,
    "hex64": int(CONTROL_RAW.hex(), 16) == CONTROL_K,
    "base64_32": int.from_bytes(base64.b64decode(base64.b64encode(CONTROL_RAW)), "big") == CONTROL_K,
    "half_first": int.from_bytes((CONTROL_RAW + b"x" * 32)[:32], "big") == CONTROL_K,
    "half_second": int.from_bytes((b"x" * 32 + CONTROL_RAW)[32:64], "big") == CONTROL_K,
    "target_gate": bool(scalar_hits(CONTROL_K)),
}
assert all(CONTROLS.values()), CONTROLS
print("CONTROLS PASS", json.dumps(CONTROLS, sort_keys=True))

def children(data):
    try: text = data.decode("utf-8-sig")
    except UnicodeError: return []
    compact = re.sub(r"\s+", "", text)
    out = []
    h = compact.removeprefix("0x")
    if len(h) >= 16 and len(h) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", h):
        out.append(("hex", bytes.fromhex(h)))
    if len(compact) >= 8 and len(compact) % 8 == 0 and re.fullmatch(r"[01]+|[ab]+", compact):
        bits = compact.translate(str.maketrans("ab", "01"))
        out.append(("binary", bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))))
    for name, alt in (("base64", None), ("base64url", b"-_")):
        if len(compact) >= 16 and re.fullmatch(r"[A-Za-z0-9+/_-]+={0,2}", compact):
            try:
                val = base64.b64decode(compact + "=" * (-len(compact) % 4), altchars=alt, validate=True)
                can = base64.b64encode(val, altchars=alt).decode().rstrip("=")
                if can == compact.rstrip("="): out.append((name, val))
            except (ValueError, base64.binascii.Error): pass
    if 1 <= len(compact) <= 4000 and re.fullmatch(r"[0-9]+|[a-io]+", compact):
        ds = compact.translate(str.maketrans("abcdefghio", "1234567890"))
        n = int(ds); out.append(("decimal", n.to_bytes(max(1, (n.bit_length()+7)//8), "big")))
    return out

records, seen_outputs = [], set()
for path in SOURCES:
    if not path.exists(): raise FileNotFoundError(path)
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            row = json.loads(line)
            value = row.get("output", row.get("candidate"))
            if not isinstance(value, str): continue
            key = (str(path), line_no, value)
            if key in seen_outputs: continue
            seen_outputs.add(key)
            records.append((path.name, line_no, row, value.encode("utf-8")))

nodes, node_sources = {}, {}
for file, line, row, raw in records:
    q = deque([("raw", raw, 0)])
    local = set()
    while q:
        route, data, depth = q.popleft()
        if data in local or len(data) > 65536: continue
        local.add(data); nodes[data] = route
        node_sources.setdefault(data, []).append({"file": file, "line": line, "route": route,
                                                   "family": row.get("family"), "note": row.get("note")})
        if depth < 2:
            for name, child in children(data):
                if child != data: q.append((route + "/" + name, child, depth + 1))

scalar_origins = {}
shapes = Counter()
def add_scalar(k, kind, data, offset=None, token=None):
    shapes[kind] += 1
    if not 1 <= k < N: return
    scalar_origins.setdefault(k, []).append({"kind": kind, "offset": offset, "token": token,
                                              "sources": node_sources[data][:5]})

for data in nodes:
    for i in range(max(0, len(data) - 31)):
        chunk = data[i:i+32]
        add_scalar(int.from_bytes(chunk, "big"), "raw32-be", data, i)
        add_scalar(int.from_bytes(chunk, "little"), "raw32-le", data, i)
    if len(data) == 64:
        add_scalar(int.from_bytes(data[:32], "big"), "half-0-32", data, 0)
        add_scalar(int.from_bytes(data[32:], "big"), "half-32-64", data, 32)
    text = data.decode("latin1")
    for m in re.finditer(r"(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])", text):
        add_scalar(int(m.group(), 16), "hex64", data, m.start(), m.group())
    for m in re.finditer(r"[5KL][1-9A-HJ-NP-Za-km-z]{50,51}", text):
        k = wif_scalar(m.group())
        shapes["wif-token"] += 1
        if k is not None: add_scalar(k, "valid-wif", data, m.start(), m.group())
    for m in re.finditer(r"[A-Za-z0-9+/]{43,}={0,2}", text):
        try: val = base64.b64decode(m.group() + "=" * (-len(m.group()) % 4), validate=True)
        except Exception: continue
        if len(val) == 32: add_scalar(int.from_bytes(val, "big"), "base64-32", data, m.start(), m.group())
    for m in re.finditer(r"(?<!\d)\d{1,78}(?!\d)", text):
        add_scalar(int(m.group()), "decimal", data, m.start(), m.group())

hits = []
for k, origins in scalar_origins.items():
    hs = scalar_hits(k)
    if hs: hits.append({"scalar_hex": f"{k:064x}", "targets": hs, "origins": origins})

valid_wifs = []
for k, origins in scalar_origins.items():
    for o in origins:
        if o["kind"] == "valid-wif": valid_wifs.append({"scalar_hex": f"{k:064x}", **o})

summary = {"source_records": len(records), "unique_recursive_nodes": len(nodes),
           "shape_occurrences": dict(shapes), "unique_valid_scalars": len(scalar_origins),
           "valid_wifs": valid_wifs, "exact_target_hits": hits, "backend": BACKEND,
           "controls": CONTROLS,
           "explicit_half_scanning": "Every 64-byte node scanned at offsets 0 and 32; all nodes also use sliding raw32 windows.",
           "limits": ["UTF-8 source outputs with recursive hex/binary/base64/base64url/decimal decode depth 2",
                      "No arbitrary concatenation across unrelated output records",
                      "No AES or envelope bytes"]}
(OUT / "manifest.json").write_text(json.dumps({"date": "2026-09-14", "sources": [str(x) for x in SOURCES],
                                                "envelope_bytes_read": 0, "aes_decryptions": 0,
                                                "backend": BACKEND, "controls": CONTROLS}, indent=1) + "\n")
(OUT / "results.json").write_text(json.dumps(summary, indent=1) + "\n")
print(json.dumps({k: v for k, v in summary.items() if k not in ("valid_wifs", "exact_target_hits")}, indent=1))
print("valid WIFs", len(valid_wifs), "exact target hits", len(hits))
print("WROTE", OUT)