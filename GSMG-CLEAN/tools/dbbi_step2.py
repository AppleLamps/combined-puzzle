"""Step two of the creator's order, worked forward from DBBI's ordinary cells.

  yellowblueprimes -> matrixsumlist -> lastwordsbeforearchichoice -> yinyang      (creator #8446)

Step one is the DBBI prime-slot parse (03 section 3).  This script runs three preregistered
experiments on what step two does with the 60 or 61 ordinary cells.  None of them reads an
envelope or runs AES; each is judged by the artifact its sealed PREREG.json predicts.

  python tools/dbbi_step2.py operands
  python tools/dbbi_step2.py e1 runs/2026-11-10_step2_carried_code
  python tools/dbbi_step2.py e2 runs/2026-11-10_step2_gap_sums
  python tools/dbbi_step2.py e3 runs/2026-11-10_step2_sumlist_lastwords

Each experiment refuses to run unless its run directory holds a sealed, unchanged statement.
"""
import hashlib
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import oracles  # noqa: E402
import prereg   # noqa: E402

DATA = ROOT / 'data'
DBBI = (DATA / 'DBBI_91.txt').read_text().strip()
FAED = (DATA / 'FAED_570.txt').read_text().strip()
ARCH = (DATA / 'architect_letters_1539.txt').read_text().strip()
SEED = 20261110


def is_prime(n):
    return n > 1 and all(n % k for k in range(2, int(n ** 0.5) + 1))


def parses(stream):
    """All complete parses in which every prime-numbered cell is 'b' or 'be' and every other
    cell is one letter.  Returns lists of cell tokens."""
    out = []

    def walk(i, n, cells):
        if i == len(stream):
            out.append(cells)
            return
        if is_prime(n):
            if stream[i] != 'b':
                return
            if stream[i:i + 2] == 'be':
                walk(i + 2, n + 1, cells + ['be'])
            walk(i + 1, n + 1, cells + ['b'])
        else:
            walk(i + 1, n + 1, cells + [stream[i]])

    walk(0, 1, [])
    return out


def operands():
    found = {len(p): p for p in parses(DBBI)}
    assert sorted(found) == [83, 84], sorted(found)      # exactly the two parses of 03 section 3
    ops = {}
    for size, cells in found.items():
        ordinary = [c for n, c in enumerate(cells, 1) if not is_prime(n)]
        groups, cur = [], []
        for n, c in enumerate(cells, 1):                  # ordinary cells cut by the prime markers
            if is_prime(n):
                groups.append(cur)
                cur = []
            else:
                cur.append(c)
        groups.append(cur)
        colours = [c for n, c in enumerate(cells, 1) if is_prime(n)]
        ops[size] = {
            'cells': cells,
            'ordinary': ''.join(ordinary),
            'groups': [''.join(g) for g in groups],        # groups[0] precedes prime 2
            'colours': ''.join('Y' if c == 'be' else 'B' for c in colours),
        }
    assert ops[84]['ordinary'] == ops[83]['ordinary'] + 'e'
    assert len(ops[83]['ordinary']) == 60 and len(ops[84]['ordinary']) == 61
    return ops


def digits(letters, base=1):
    return ''.join(str(ord(c) - 97 + base) for c in letters)


def val(letters):
    return [ord(c) - 96 for c in letters]


def equality_pattern(s):
    first = {}
    return tuple(first.setdefault(c, len(first)) for c in s)


def start(run):
    run = Path(run)
    seal = prereg.verify(run)
    return run, seal


def finish(run, seal, name, payload):
    payload = {'prereg_sha256': seal, **payload}
    path = run / name
    path.write_text(json.dumps(payload, indent=1) + '\n', encoding='utf-8')
    return path


# ---------------------------------------------------------------------------------------------------
# E1  "the code you hopefully carry": the ordinary cells reproduce a code the solver already holds
# ---------------------------------------------------------------------------------------------------
CHAIN_TEXTS = {
    'phase1_answer': 'theflowerblossomsthroughwhatseemstobeaconcretesurface',
    'phase2_answer': 'causality',
    'phase3_answer': ('causalitySafenetLunaHSM111100x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E69726'
                      '2206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854B5KR/1r5B/2R5/2b1p1p1/'
                      '2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1'),
    'phase32_answer': 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple',
    'poster_text': 'GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe',
    'url': 'gsmg.io/theseedisplanted',
    'hashthetext': 'HASHTHETEXT',
    'beaufort_key': 'THEMATRIXHASYOU',
    'checkerboard_key': 'FUBCDORA.LETHINGKYMVPS/JQZXW',
    'label_matrixsumlist': 'matrixsumlist',
    'label_lastwords': 'lastwordsbeforearchichoice',
    'label_thispassword': 'thispassword',
    'label_enter': 'enter',
    'literal_1': 'shabefourfirsthintisyourlastcommand',
    'literal_2': 'shabefanstoo',
    'safenet': 'Safenet', 'luna': 'Luna', 'hsm': 'HSM', 'eo': '11110',
    'genesis_hex': ('736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320'
                    '393030322F6E614A2F33302073656D695420656854'),
    'chess_before': 'B5KR/1r5B/6R1/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 w - - 0 1',
    'chess_after': 'B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1',
    'x2sh_strip': 'X2SH4Y0QB15',
    'prize_address': '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe',
    'better_half_address': '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa',
    'half_pubkey': ('04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576'
                    'c0c6404db5aa546286563e4be12bf33559'),
    'half_hash160': 'a9553269572a317e39f0f518cb87c1a0ee1dbae4',
    'better_half_hash160': '4bc468447fe1b048ad030a2f9a125478eabc4ed6',
}
VIC_DIGITS = ('15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631'
              '213131281491109166131412199114371612126021664313711154112')


def poster_lists():
    """Row and column one-counts and the spiral bit string, from data/poster_spiral_bits.txt."""
    bits = (DATA / 'poster_spiral_bits.txt').read_text().split()[0]
    assert len(bits) == 196
    grid = [[None] * 14 for _ in range(14)]
    r = c = 0
    dr, dc = 1, 0                                           # down, right, up, left: counter-clockwise inward
    for b in bits:
        grid[r][c] = int(b)
        nr, nc = r + dr, c + dc
        if not (0 <= nr < 14 and 0 <= nc < 14) or grid[nr][nc] is not None:
            dr, dc = -dc, dr
            nr, nc = r + dr, c + dc
        r, c = nr, nc
    rows = [sum(row) for row in grid]
    cols = [sum(grid[i][j] for i in range(14)) for j in range(14)]
    assert rows == [6, 10, 8, 7, 6, 6, 5, 4, 9, 9, 7, 8, 7, 9] and cols == [8, 10, 8, 10, 8, 7, 3, 6, 7, 5, 9, 6, 6, 8]
    return bits, grid, rows, cols


def registry():
    reg = {}
    for name, text in CHAIN_TEXTS.items():
        raw = text.encode()
        h = hashlib.sha256(raw).hexdigest()
        reg[f'{name}:text'] = text
        reg[f'{name}:text_as_decimal'] = str(int.from_bytes(raw, 'big'))
        reg[f'{name}:text_as_hex'] = raw.hex()
        reg[f'{name}:text_as_octal'] = oct(int.from_bytes(raw, 'big'))[2:]
        reg[f'{name}:char_codes'] = ''.join(str(b) for b in raw)
        reg[f'{name}:sha256_hex'] = h
        reg[f'{name}:sha256_decimal'] = str(int(h, 16))
        reg[f'{name}:sha256_octal'] = oct(int(h, 16))[2:]
        reg[f'{name}:sha256_digits_only'] = re.sub('[^0-9]', '', h)
    bits, grid, rows, cols = poster_lists()
    reg['poster:spiral_bits'] = bits
    reg['poster:raster_bits'] = ''.join(str(v) for row in grid for v in row)
    reg['poster:row_sums'] = ''.join(map(str, rows))
    reg['poster:col_sums'] = ''.join(map(str, cols))
    reg['poster:row_then_col'] = reg['poster:row_sums'] + reg['poster:col_sums']
    reg['poster:col_then_row'] = reg['poster:col_sums'] + reg['poster:row_sums']
    reg['poster:char_popcounts'] = ''.join(str(bits[i:i + 8].count('1')) for i in range(0, 192, 8))
    reg['vic:149_digits'] = VIC_DIGITS
    reg['vic:149_digits_sha256_decimal'] = str(int(hashlib.sha256(VIC_DIGITS.encode()).hexdigest(), 16))
    reg['vic:plaintext_91'] = (DATA / 'checkerboard_vic_91.txt').read_text().split()[0]
    reg['architect:plaintext_1539'] = ARCH
    reg['faed:letters'] = FAED
    reg['faed:digits'] = digits(FAED)
    p32 = (DATA / 'phase3_2_plaintext.bin').read_bytes()
    reg['phase32:intro_text'] = p32[:447].decode('latin-1')
    reg['phase32:board_sentence'] = p32[2143:2292].decode('latin-1')
    reg['phase2:plaintext'] = (DATA / 'phase2_plaintext.bin').read_bytes().decode('latin-1')
    reg['phase3:riddles'] = (DATA / 'phase3_plaintext.bin').read_bytes()[:726].decode('latin-1')
    return reg


def best_isomorph(p, target, minimum=8):
    """Longest window of p whose equality pattern equals that of some window of target."""
    best = (0, None, None)
    lo, hi = minimum, min(len(p), len(target))
    patterns_cache = {}
    while lo <= hi:                                        # isomorph windows are prefix-closed: binary search
        mid = (lo + hi) // 2
        if mid not in patterns_cache:
            patterns_cache[mid] = {equality_pattern(target[j:j + mid]): j for j in range(len(target) - mid + 1)}
        hit = None
        for i in range(len(p) - mid + 1):
            j = patterns_cache[mid].get(equality_pattern(p[i:i + mid]))
            if j is not None:
                hit = (mid, i, j)
                break
        if hit:
            best, lo = hit, mid + 1
        else:
            hi = mid - 1
    return best


def e1_views(ordinary):
    views = {}
    for base in (1, 0):
        d = digits(ordinary, base)
        views[f'a={base}'] = d
        views[f'a={base},reversed'] = d[::-1]
    return views


def e1_measure(ordinary, reg):
    exact, iso = [], []
    for vname, view in e1_views(ordinary).items():
        for rname, target in reg.items():
            n, text = oracles.longest_common_run(view, target)
            exact.append((n, vname, rname, text))
    for direction, p in (('forward', ordinary), ('reversed', ordinary[::-1])):
        for rname, target in reg.items():
            n, i, j = best_isomorph(p, target)
            iso.append((n, direction, rname, i, j))
    return max(exact), max(iso, key=lambda t: t[0]), exact, iso


def run_e1(run):
    run, seal = start(run)
    ops, reg = operands(), registry()
    rnd = random.Random(SEED)
    out = {'registry_entries': len(reg), 'registry_characters': sum(map(len, reg.values())), 'parses': {}}
    # planted control: a held code, spread over the non-prime cells exactly as DBBI is built
    code = digits('acdefghi' * 8, 1)[:60]
    planted_reg = dict(reg, **{'planted:code': 'x' * 40 + code + 'y' * 40})
    planted_letters = ''.join(chr(96 + int(ch)) for ch in code)
    stream, it = [], iter(planted_letters)
    for n in range(1, 84):
        stream.append('b' if is_prime(n) else next(it))
    recovered = ''.join(c for n, c in enumerate(parses(''.join(stream))[0], 1) if not is_prime(n))
    top, _, _, _ = e1_measure(recovered, planted_reg)
    out['planted_control'] = {'recovered_run': top[0], 'source': top[2], 'passed': top[0] == 60 and top[2] == 'planted:code'}
    passed = False
    for size in (83, 84):
        ordinary = ops[size]['ordinary']
        top_exact, top_iso, exact, iso = e1_measure(ordinary, reg)
        ctl_exact, ctl_iso = [], []
        letters = list(ordinary)
        for _ in range(200):
            rnd.shuffle(letters)
            te, ti, _, _ = e1_measure(''.join(letters), reg)
            ctl_exact.append(te[0])
            ctl_iso.append(ti[0])
        out['parses'][size] = {
            'ordinary': ordinary,
            'longest_exact_run': {'length': top_exact[0], 'view': top_exact[1], 'source': top_exact[2], 'text': top_exact[3]},
            'longest_isomorph': {'length': top_iso[0], 'direction': top_iso[1], 'source': top_iso[2],
                                 'offset_in_cells': top_iso[3], 'offset_in_source': top_iso[4]},
            'control_exact_max': max(ctl_exact), 'control_exact_median': sorted(ctl_exact)[100],
            'control_isomorph_max': max(ctl_iso), 'control_isomorph_median': sorted(ctl_iso)[100],
            'top_exact_runs': sorted(exact, reverse=True)[:8],
        }
        passed |= top_exact[0] >= 12 or top_iso[0] >= 20
    out['acceptance'] = 'exact run >= 12 digits, or isomorph window >= 20 cells'
    out['outcome'] = 'passed' if passed else 'null'
    path = finish(run, seal, 'results.json', out)
    print(json.dumps({k: v for k, v in out.items() if k != 'parses'}, indent=1))
    for size, r in out['parses'].items():
        print(size, 'exact', r['longest_exact_run'], 'ctl max', r['control_exact_max'],
              '| isomorph', r['longest_isomorph'], 'ctl max', r['control_isomorph_max'])
    return path, out['outcome']


# ---------------------------------------------------------------------------------------------------
# E2  "matrixsumlist" names what the ordinary cells become: a list of sums
# ---------------------------------------------------------------------------------------------------
def e2_lists(cells):
    """Every sum list of the sealed statement, from one parse (list of cell tokens)."""
    size = len(cells)
    lists = {}
    groups, cur = [], []
    for n, c in enumerate(cells, 1):
        if is_prime(n):
            groups.append(cur)
            cur = []
        else:
            cur.append(c)
    groups.append(cur)
    sums = [sum(val(''.join(g))) for g in groups]
    lists['gap_sums'] = sums                                # one sum per stretch between markers
    lists['gap_sums_nonempty'] = [s for s, g in zip(sums, groups) if g]
    colours = [c for n, c in enumerate(cells, 1) if is_prime(n)]
    after = groups[1:]                                      # after[k] follows the k-th prime marker
    lists['gap_sums_after_yellow'] = [sum(val(''.join(g))) for g, c in zip(after, colours) if c == 'be']
    lists['gap_sums_after_blue'] = [sum(val(''.join(g))) for g, c in zip(after, colours) if c == 'b']
    if size == 84:                                          # boards exist only for 84 cells
        zeroed = [0 if is_prime(n) else ord(c) - 96 for n, c in enumerate(cells, 1)]
        for rows, width in ((6, 14), (14, 6), (7, 12), (12, 7)):
            grid = [zeroed[r * width:(r + 1) * width] for r in range(rows)]
            lists[f'board_{rows}x{width}_row_sums'] = [sum(r) for r in grid]
            lists[f'board_{rows}x{width}_col_sums'] = [sum(grid[r][c] for r in range(rows)) for c in range(width)]
    return lists


def e2_decodes(values):
    """Letter and byte readings of one sum list.  Returns {decode: text}."""
    out = {}
    out['a1z26'] = ''.join(chr(96 + v) if 1 <= v <= 26 else '?' for v in values)
    out['mod26_a0'] = ''.join(chr(97 + v % 26) for v in values)
    out['mod26_a1'] = ''.join(chr(97 + (v - 1) % 26) for v in values)
    out['ascii'] = ''.join(chr(v) if 32 <= v < 127 else '?' for v in values)
    out['ascii_plus64'] = ''.join(chr(v + 64) if 32 <= v + 64 < 127 else '?' for v in values)
    out['ascii_plus96'] = ''.join(chr(v + 96) if 32 <= v + 96 < 127 else '?' for v in values)
    number = int(''.join(map(str, values)) or '0')
    raw = number.to_bytes(max(1, (number.bit_length() + 7) // 8), 'big')
    out['decimal_concat_bytes'] = ''.join(chr(b) if 32 <= b < 127 else '?' for b in raw)
    return out


def e2_score(text):
    if '?' in text:
        return None
    return oracles.english_score(text)


def e2_outputs(cells):
    rows = []
    for lname, values in e2_lists(cells).items():
        for dname, text in e2_decodes(values).items():
            rows.append({'list': lname, 'values': values, 'decode': dname, 'text': text, 'score': e2_score(text)})
    return rows


def run_e2(run):
    run, seal = start(run)
    ops = operands()
    rnd = random.Random(SEED)
    _, _, poster_rows, poster_cols = poster_lists()
    out = {'parses': {}, 'exact_hits': []}
    # planted control: ordinary cells chosen so that the gap sums spell a sentence under a1z26
    message = 'takethelastwordsofthearchitect'[:23]
    cells, it = [], iter(message)
    n = 1
    while len(cells) < 84:
        if is_prime(n):
            cells.append('b')
            n += 1
            continue
        gap = 0
        while not is_prime(n + gap) and len(cells) + gap < 84:
            gap += 1
        target = ord(next(it, 'e')) - 96
        parts = [1] * gap
        for k in range(gap):                                # spread the target over the gap, digits 1..9
            add = min(8, target - sum(parts))
            parts[k] += max(0, add)
        cells += [chr(96 + p) for p in parts]
        n += gap
    planted = [r for r in e2_outputs(cells[:84]) if r['list'] == 'gap_sums_nonempty' and r['decode'] == 'a1z26']
    reachable = ''.join(ch for ch in planted[0]['text'])
    out['planted_control'] = {'text': reachable, 'score': planted[0]['score']}
    real_best, ctl_best = None, []
    for size in (83, 84):
        cells = ops[size]['cells']
        rows = e2_outputs(cells)
        for r in rows:
            for form in (r['text'], ''.join(map(str, r['values'])), ','.join(map(str, r['values']))):
                if oracles.known_digest(form) or oracles.dbbi_pattern(form) or oracles.known_address(form):
                    out['exact_hits'].append({'parse': size, 'list': r['list'], 'form': form})
            for label, target in (('poster_row_sums', poster_rows), ('poster_col_sums', poster_cols)):
                run_len = oracles.longest_common_run(''.join(chr(48 + v) if v < 70 else '~' for v in r['values']),
                                                     ''.join(chr(48 + v) for v in target))[0]
                if run_len >= 8:
                    out['exact_hits'].append({'parse': size, 'list': r['list'], 'matches': label, 'run': run_len})
        scored = [r for r in rows if r['score'] is not None]
        best = max(scored, key=lambda r: r['score']) if scored else None
        out['parses'][size] = {'outputs': rows, 'best': best}
        if best and (real_best is None or best['score'] > real_best['score']):
            real_best = dict(best, parse=size)
        ordinary_positions = [i for i, _ in enumerate(cells) if not is_prime(i + 1)]
        letters = [cells[i] for i in ordinary_positions]
        for _ in range(2000):
            rnd.shuffle(letters)
            shuffled = list(cells)
            for i, c in zip(ordinary_positions, letters):
                shuffled[i] = c
            scores = [r['score'] for r in e2_outputs(shuffled) if r['score'] is not None]
            ctl_best.append(max(scores) if scores else -99.0)
    ctl_best.sort()
    threshold = ctl_best[int(0.999 * len(ctl_best))]
    out['real_best'] = real_best
    out['control'] = {'runs': len(ctl_best), 'median_of_max': ctl_best[len(ctl_best) // 2],
                      'p999_of_max': threshold, 'max_of_max': ctl_best[-1]}
    out['planted_control']['passed'] = bool(out['planted_control']['score'] is not None
                                            and out['planted_control']['score'] > threshold
                                            and out['planted_control']['score'] > -4.9)
    out['acceptance'] = 'any exact hit, or best real score above the 99.9th percentile of control maxima and above -4.9'
    passed = bool(out['exact_hits']) or bool(real_best and real_best['score'] > threshold and real_best['score'] > -4.9)
    out['outcome'] = 'passed' if passed else 'null'
    path = finish(run, seal, 'results.json', out)
    print(json.dumps({k: out[k] for k in ('planted_control', 'exact_hits', 'real_best', 'control', 'outcome')}, indent=1))
    return path, out['outcome']


# ---------------------------------------------------------------------------------------------------
# E3  the sum list is the input of "last words before archi choice"
# ---------------------------------------------------------------------------------------------------
def transcript(name):
    """Dialogue of one saved film transcript, speaker labels and stage directions removed."""
    text = (ROOT / 'reference_texts' / name).read_text(encoding='utf-8', errors='ignore')
    lines = []
    for line in text.splitlines():
        line = line.replace('**', '').strip()
        m = re.match(r'^(The Architect|Architect|Neo)\s*:\s*(.*)$', line)
        if m:
            lines.append((m.group(1).replace('The ', ''), re.sub(r'\[[^\]]*\]|\([^)]*\)', ' ', m.group(2))))
    return lines


def e3_streams(name):
    lines = transcript(name)
    words, anchors = [], {}
    choice_seen = 0
    for speaker, line in lines:
        for w in re.findall(r"[A-Za-z']+", line):
            clean = re.sub('[^a-z]', '', w.lower())
            if not clean:
                continue
            if clean == 'choice':
                choice_seen += 1
                anchors[f'{speaker.lower()}_choice_{choice_seen}'] = len(words)   # index of the word "choice"
            words.append(clean)
    for i in range(len(words) - 2):                         # "...nothing that you can do to stop it"
        if words[i:i + 3] == ['to', 'stop', 'it']:
            anchors['before_neo_walks_to_the_door'] = i + 3  # just past the Architect's last words
    anchors['end_of_scene'] = len(words)
    return words, anchors


def e3_read(words, anchor_word, values, unit, semantics, base, direction):
    """Returns the letters selected, or None if an index leaves the text."""
    if unit == 'letter':
        stream = ''.join(words)
        anchor = len(''.join(words[:anchor_word]))
        pick = lambda i: stream[i]                           # noqa: E731
        size = len(stream)
    else:
        anchor, size = anchor_word, len(words)
        pick = (lambda i: words[i][0]) if unit == 'word_initial' else (lambda i: words[i][-1])   # noqa: E731
    out, pos = [], 0
    for v in values:
        pos = pos + v if semantics == 'running' else v
        offset = pos - (1 - base)                            # base 1: the unit next to the anchor is 1
        i = anchor - 1 - offset if direction == 'back' else anchor + offset
        if not 0 <= i < size:
            return None
        out.append(pick(i))
    return ''.join(out)


E3_CONFIGS = [(u, s, b, d) for u in ('letter', 'word_initial', 'word_final')
              for s in ('running', 'direct') for b in (0, 1) for d in ('back', 'forward')]
E3_TRANSCRIPTS = ('matrix_reloaded_architect_scene_transcript.txt', 'matrix_reloaded_architect_scene_scott_manning.md')


def e3_all(lists, texts):
    rows = []
    for tname, (words, anchors) in texts.items():
        for aname, anchor in anchors.items():
            for lname, values in lists.items():
                for unit, semantics, base, direction in E3_CONFIGS:
                    text = e3_read(words, anchor, values, unit, semantics, base, direction)
                    if text is None:
                        continue
                    for order, t in (('as_read', text), ('reversed', text[::-1])):
                        rows.append({'transcript': tname, 'anchor': aname, 'list': lname, 'unit': unit,
                                     'semantics': semantics, 'base': base, 'direction': direction,
                                     'order': order, 'text': t, 'score': oracles.english_score(t)})
    return rows


def run_e3(run):
    run, seal = start(run)
    ops = operands()
    rnd = random.Random(SEED)
    texts = {name: e3_streams(name) for name in E3_TRANSCRIPTS}
    lists = {}
    for size in (83, 84):
        lists[f'ordinary_{size}'] = val(ops[size]['ordinary'])
        sums = e2_lists(ops[size]['cells'])
        lists[f'gap_sums_{size}'] = sums['gap_sums']
        lists[f'gap_sums_nonempty_{size}'] = sums['gap_sums_nonempty']
    rows = e3_all(lists, texts)
    scored = [r for r in rows if r['score'] is not None]
    best = max(scored, key=lambda r: r['score'])
    ctl = []
    for _ in range(300):
        shuffled = {}
        for name, values in lists.items():
            v = list(values)
            rnd.shuffle(v)
            shuffled[name] = v
        ctl.append(max(r['score'] for r in e3_all(shuffled, texts) if r['score'] is not None))
    ctl.sort()
    # planted control: a list built so that running back-steps over letters spell a sentence
    words, anchors = texts[E3_TRANSCRIPTS[0]]
    stream = ''.join(words)
    anchor = len(''.join(words[:anchors['before_neo_walks_to_the_door']]))
    message, steps, pos = 'thedoortoyourleftleadsback', [], 0
    for ch in message:
        nxt = next(p for p in range(pos + 1, pos + 400) if stream[anchor - 1 - (p - 1)] == ch)
        steps.append(nxt - pos)
        pos = nxt
    planted = e3_read(words, anchors['before_neo_walks_to_the_door'], steps, 'letter', 'running', 1, 'back')
    out = {
        'anchors': {t: a for t, (_, a) in texts.items()},
        'outputs': len(rows), 'scored_outputs': len(scored),
        'best': best, 'top10': sorted(scored, key=lambda r: -r['score'])[:10],
        'control': {'runs': len(ctl), 'median_of_max': ctl[len(ctl) // 2], 'max_of_max': ctl[-1]},
        'planted_control': {'text': planted, 'score': oracles.english_score(planted),
                            'passed': planted == message and oracles.english_score(planted) > ctl[-1]},
        'acceptance': 'best real score above every control maximum and above -4.9',
    }
    out['outcome'] = 'passed' if best['score'] > ctl[-1] and best['score'] > -4.9 else 'null'
    path = finish(run, seal, 'results.json', out)
    (run / 'outputs.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows), encoding='utf-8')
    print(json.dumps({k: out[k] for k in ('outputs', 'best', 'control', 'planted_control', 'outcome')}, indent=1))
    return path, out['outcome']


def main(argv):
    if len(argv) >= 1 and argv[0] == 'operands':
        ops = operands()
        for size in (83, 84):
            o = ops[size]
            print(size, 'cells | ordinary', len(o['ordinary']), o['ordinary'])
            print('   digits ', digits(o['ordinary']), 'sum', sum(val(o['ordinary'])))
            print('   colours', o['colours'])
            print('   groups ', o['groups'])
        return
    if len(argv) != 2 or argv[0] not in ('e1', 'e2', 'e3'):
        raise SystemExit(__doc__)
    path, outcome = {'e1': run_e1, 'e2': run_e2, 'e3': run_e3}[argv[0]](argv[1])
    print(f'wrote {path}; outcome {outcome}. Record it with: python tools/prereg.py record {argv[1]} '
          f'--outcome {outcome} --evidence {path}')


if __name__ == '__main__':
    main(sys.argv[1:])
