import sys, os, hashlib, re, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

# 1. Load containers
conts = {
    'terminal': load('terminal.b64'),
    'salphaseion-short': load('salphaseion-short.b64'),
    'cosmic-duality': load('cosmic-duality.b64'),
}
controls = {
    'phase2': (load('phase2.b64'), 'causality'),
    'phase3.2': (load('phase3.2.b64'), 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple'),
}

# Verify control
for cname, (cdata, cpass) in controls.items():
    pt = dec(cdata, cpass, hashed=True)
    assert pt is not None, f"Control decryption failed for {cname}!"
print("Control decryptions verified OK.")

# Read artifacts
with open('files/salphaseion-textarea.txt') as f:
    sp_text = f.read().strip()

r1_str = sp_text[:91]
r1_digits = [ord(c) - ord('a') + 1 for c in r1_str]

r3_str = sp_text[195:765]
r3_digits = [ord(c) - ord('a') + 1 for c in r3_str]

with open('derived/checkerboard-plaintext.txt') as f:
    cb_plain = f.read().strip()

with open('matrix-reloaded.txt', 'r', encoding='utf-8') as f:
    mr_lines = [l.strip() for l in f if l.strip()]

dialogues = []
for l in mr_lines:
    spk, txt = l.split(':', 1)
    dialogues.append((spk.strip(), txt.strip()))

# Success tracking
found_hits = []

def test_pw(cand, desc):
    if not cand: return
    # Try different password modes
    modes = [
        ('sha_hex', hashlib.sha256(cand.encode('utf-8')).hexdigest().lower()),
        ('raw', cand),
    ]
    for mode_name, pw_val in modes:
        for cname, cdata in conts.items():
            pt = dec(cdata, pw_val, hashed=False)
            if pt is not None:
                pr = printable(pt)
                print(f"Padding pass! [{cname}] mode={mode_name} pr={pr:.2f} desc={desc[:60]} cand={repr(cand[:40])}")
                if pr > 0.55 or pt.startswith(b'Salted__'):
                    print(f"*** SIGNIFICANT HIT in {cname} ({len(pt)} bytes, pr={pr:.2f}) ***")
                    print(f"Password: {cand}")
                    print(f"Decrypted text: {repr(pt[:200])}")
                    found_hits.append((cname, cand, mode_name, pt))
    
    # Also check candidate as private key
    try:
        # Check if hex string of 64 chars
        if len(cand) == 64 and all(c in '0123456789abcdefABCDEF' for c in cand):
            k = int(cand, 16)
            if check_key(k):
                print(f"*** BITCOIN PRIVATE KEY FOUND! ***: {cand}")
                found_hits.append(('BTC_KEY', cand, 'hex_privkey', None))
    except:
        pass
    try:
        # sha256(cand) as private key
        k = int.from_bytes(hashlib.sha256(cand.encode('utf-8')).digest(), 'big')
        if check_key(k):
            print(f"*** BITCOIN PRIVATE KEY FOUND (via sha256)! ***: {cand}")
            found_hits.append(('BTC_KEY', cand, 'sha256_privkey', None))
    except:
        pass

print("Generating candidates...")
candidates = []

# =========================================================================
# HYPOTHESIS 1: Matrix sum lists on r1 (91) and r3 (570)
# =========================================================================
# For r1 (91 digits, factors 7x13, 13x7):
for r, c in [(7, 13), (13, 7)]:
    M = [r1_digits[i*c:(i+1)*c] for i in range(r)]
    rs = [sum(row) for row in M]
    cs = [sum(M[i][j] for i in range(r)) for j in range(c)]
    
    # As comma-separated, space-separated, no space, ASCII chars, hex
    for label, lst in [(f'r1_{r}x{c}_rowsums', rs), (f'r1_{r}x{c}_colsums', cs)]:
        candidates.append((''.join(str(x) for x in lst), label + '_digits'))
        candidates.append((','.join(str(x) for x in lst), label + '_comma'))
        candidates.append((' '.join(str(x) for x in lst), label + '_space'))
        candidates.append((''.join(chr(65 + x % 26) for x in lst), label + '_mod26'))
        candidates.append((''.join(chr(97 + x % 26) for x in lst), label + '_mod26_lower'))
        candidates.append((''.join(chr(x) for x in lst if 32 <= x < 127), label + '_ascii'))

# For r3 (570 digits):
for r in [2, 3, 5, 6, 10, 15, 19, 30, 38, 57, 95]:
    c = 570 // r
    M = [r3_digits[i*c:(i+1)*c] for i in range(r)]
    rs = [sum(row) for row in M]
    cs = [sum(M[i][j] for i in range(r)) for j in range(c)]
    for label, lst in [(f'r3_{r}x{c}_rowsums', rs), (f'r3_{r}x{c}_colsums', cs)]:
        candidates.append((''.join(str(x) for x in lst), label + '_digits'))
        candidates.append((','.join(str(x) for x in lst), label + '_comma'))
        candidates.append((' '.join(str(x) for x in lst), label + '_space'))
        candidates.append((''.join(chr(65 + x % 26) for x in lst), label + '_mod26'))
        candidates.append((''.join(chr(97 + x % 26) for x in lst), label + '_mod26_lower'))
        if all(32 <= x < 127 for x in lst):
            candidates.append((''.join(chr(x) for x in lst), label + '_ascii'))

# =========================================================================
# HYPOTHESIS 2: "first hint is your last command" -> command sequences
# =========================================================================
cmd_words = ['matrixsumlist', 'lastwordsbeforearchichoice', 'thispassword', 'enter']
for p in itertools.permutations(cmd_words, 2):
    candidates.append((''.join(p), 'perm2'))
    candidates.append((' '.join(p), 'perm2_sp'))
for p in itertools.permutations(cmd_words, 3):
    candidates.append((''.join(p), 'perm3'))
    candidates.append((' '.join(p), 'perm3_sp'))
candidates.append((''.join(cmd_words), 'all_cmds'))
candidates.append((' '.join(cmd_words), 'all_cmds_sp'))
# With matrixsumlist last:
candidates.append(('lastwordsbeforearchichoicematrixsumlist', 'archi_then_matrixsumlist'))
candidates.append(('lastwordsbeforearchichoice matrixsumlist', 'archi_then_matrixsumlist_sp'))
candidates.append(('thispasswordmatrixsumlist', 'pw_then_matrixsumlist'))
candidates.append(('thispassword matrixsumlist', 'pw_then_matrixsumlist_sp'))

# =========================================================================
# HYPOTHESIS 3: Board mappings (14 columns wide)
# =========================================================================
# Checkerboard letters: INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE (91 chars)
# 91 on 14 columns = 7 rows with padding, or 13 columns x 7 rows
# Let's try 91 letters in grid width 13 (7 rows) and read by columns:
grid_13 = [cb_plain[i*13:(i+1)*13] for i in range(7)]
col_read_13 = ''.join(''.join(grid_13[r][c] for r in range(7)) for c in range(13))
candidates.append((col_read_13, 'cb_91_col_read_13x7'))
candidates.append((col_read_13.lower(), 'cb_91_col_read_13x7_lower'))

# 91 letters on grid width 7 (13 rows) and read by columns:
grid_7 = [cb_plain[i*7:(i+1)*7] for i in range(13)]
col_read_7 = ''.join(''.join(grid_7[r][c] for r in range(13)) for c in range(7))
candidates.append((col_read_7, 'cb_91_col_read_7x13'))
candidates.append((col_read_7.lower(), 'cb_91_col_read_7x13_lower'))

# Board 14 wide with 91 letters padded to 98 (7 rows x 14 cols):
for pad_char in [' ', 'A', 'X', 'Z', '.']:
    padded_98 = cb_plain + pad_char * 7
    grid_14 = [padded_98[i*14:(i+1)*14] for i in range(7)]
    col_read_14 = ''.join(''.join(grid_14[r][c] for r in range(7)) for c in range(14)).strip()
    candidates.append((col_read_14, f'cb_col_read_14_pad_{pad_char}'))
    candidates.append((col_read_14.lower(), f'cb_col_read_14_pad_{pad_char}_lower'))

# Checkerboard alphabet on 14-wide board (2 rows of 14):
# fubcd (5) + oracle (6) + sad (3) = 14
row1_letters = 'FUBCDORACLESAD'
row2_letters = 'THINGKYMVPSJQW' # 7 + 4 + 3 = 14
candidates.append((row1_letters + row2_letters, 'board_2x14_letters'))
candidates.append(((row1_letters + row2_letters).lower(), 'board_2x14_letters_lower'))
# Column read of 2x14:
col_read_2x14 = ''.join(row1_letters[c] + row2_letters[c] for c in range(14))
candidates.append((col_read_2x14, 'board_2x14_col_read'))
candidates.append((col_read_2x14.lower(), 'board_2x14_col_read_lower'))

# =========================================================================
# HYPOTHESIS 4: Targeted dialogue quotes and sub-clauses from lines 20, 22, 24, 26
# =========================================================================
for line_idx in [20, 22, 24, 25, 26]:
    spk, txt = dialogues[line_idx]
    # Full line
    candidates.append((txt, f'L{line_idx}_full'))
    candidates.append((txt.lower(), f'L{line_idx}_full_lower'))
    # Clean letters
    clean = re.sub(r'[^a-zA-Z0-9]', '', txt)
    candidates.append((clean, f'L{line_idx}_clean'))
    candidates.append((clean.lower(), f'L{line_idx}_clean_lower'))
    
    # Sentences
    for s in re.split(r'(?<=[.!?])\s+', txt):
        s_str = s.strip().rstrip('.')
        if s_str:
            candidates.append((s_str, f'L{line_idx}_sent'))
            candidates.append((s_str.lower(), f'L{line_idx}_sent_lower'))
            s_clean = re.sub(r'[^a-zA-Z0-9]', '', s_str)
            candidates.append((s_clean, f'L{line_idx}_sent_clean'))
            candidates.append((s_clean.lower(), f'L{line_idx}_sent_clean_lower'))

# Specific targeted clauses:
specific_clauses = [
    # Right before "choice"
    "the problem is",
    "The problem is",
    "THE PROBLEM IS",
    "to the end of your species",
    "and to the end of your species",
    "the end of your species",
    "end of your species",
    # Right before the doors
    "Which brings us at last to the moment of truth, wherein the fundamental flaw is ultimately expressed and the anomaly revealed as both beginning and end",
    "as both beginning and end",
    "both beginning and end",
    "beginning and end",
    "beginning and end.",
    # Line 22
    "Apropos, she entered the matrix to save your life at the cost of her own",
    "at the cost of her own",
    "the cost of her own",
    "cost of her own",
    "to save your life at the cost of her own",
    # Line 20 ending
    "vis-a-vis love",
    "vis-a-vis love.",
    "vis-a-vis",
    # Line 26
    "We won't",
    "We won't.",
    "wewont",
    # Architect text ending
    "PRIME BASICS",
    "prime basics",
    "primebasics",
    "PRIMEBASICS",
    "REINSERTING THE PRIME BASICS",
    "reinserting the prime basics",
    "CIAO BELLA O",
    "ciao bella o",
    "ciaobellao",
    "CIAOBELLAO",
    # From checkerboard
    "HALF AND BETTER HALF",
    "half and better half",
    "halfandbetterhalf",
    "HALFANDBETTERHALF",
    "HALF",
    "BETTER HALF",
    "BETTERHALF",
    "THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF",
    "the private keys belong to half and better half",
    # From clue
    "Raising the stakes without extra chances of winning",
    "raising the stakes without extra chances of winning",
    "raisingthestakeswithoutextrachancesofwinning",
    "fubcd-king & oracle-queen, thingky mvps, on a sad board but as wide as the first one seen",
    "fubcd-king & oracle-queen, thingky mvps",
    "fubcd-king & oracle-queen",
    "fubcd-king",
    "oracle-queen",
    "thingky mvps",
    "sad board",
    "sad board but as wide as the first one seen",
]
for sc in specific_clauses:
    candidates.append((sc, 'specific_clause'))
    candidates.append((sc.lower(), 'specific_clause_lower'))
    c_clean = re.sub(r'[^a-zA-Z0-9]', '', sc)
    candidates.append((c_clean, 'specific_clause_clean'))
    candidates.append((c_clean.lower(), 'specific_clause_clean_lower'))

# Also combinations with matrixsumlist
for sc in specific_clauses[:20]:
    candidates.append((sc + 'matrixsumlist', 'sc+matrixsumlist'))
    candidates.append((sc.lower() + 'matrixsumlist', 'sc_lower+matrixsumlist'))
    candidates.append((re.sub(r'[^a-zA-Z0-9]', '', sc).lower() + 'matrixsumlist', 'sc_clean+matrixsumlist'))

print(f"Total candidates compiled: {len(candidates)}")

# Deduplicate preserving order
seen = set()
unique_candidates = []
for cand, desc in candidates:
    if cand not in seen:
        seen.add(cand)
        unique_candidates.append((cand, desc))

print(f"Unique candidates: {len(unique_candidates)}")

# Test all
for i, (cand, desc) in enumerate(unique_candidates):
    test_pw(cand, desc)
    if (i + 1) % 500 == 0:
        print(f"Progress: {i+1}/{len(unique_candidates)} tested...")

print(f"\nExecution finished. Total significant hits: {len(found_hits)}")
for hit in found_hits:
    print("HIT:", hit[:3])
