import sys
from pathlib import Path, re
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

PASS=[]; FAIL=[]
def check(name, cond, detail=''):
    (PASS if cond else FAIL).append(name)
    print(('PASS ' if cond else 'FAIL '), name, ' ', detail)

pt32 = open(str(Path(__file__).resolve().parent / 'out' / 'phase32_plaintext.bin'),'rb').read()

# ---------------- Architect text (section 3.4a) ----------------
raw = pt32[447:1986]
check('architect ciphertext window len 1539', len(raw)==1539, len(raw))

s = raw.decode('latin-1')
cp273_bytes = s.encode('cp273')
ciph_letters = cp273_bytes.decode('ascii')
check('cp273-transformed bytes are all lowercase a-z', all('a'<=c<='z' for c in ciph_letters), ciph_letters[:30])

KEY = "THEMATRIXHASYOU"
def reciprocal_beaufort_decrypt(ciph: str, key: str) -> str:
    out = []
    for i, c in enumerate(ciph):
        k = ord(key[i % len(key)].upper()) - 65
        cc = ord(c.upper()) - 65
        p = (k - cc) % 26
        out.append(chr(p + 65))
    return ''.join(out)

architect = reciprocal_beaufort_decrypt(ciph_letters, KEY)
print('\nARCHITECT TEXT (derived from real ciphertext bytes, independent of dossier prose):\n')
print(architect)
print()

dossier_architect = lib.block_joined(8, sep='').upper()
check('derived architect text == dossier block 8 (exact)', architect == dossier_architect,
      f'len derived={len(architect)} len dossier={len(dossier_architect)}')

idx479 = architect.find('PRIVATEKEY')
check('first PRIVATEKEY at letters-only index 479', idx479 == 479, idx479)
idx2 = architect.find('PRIVATEKEY', idx479+1)
check('second PRIVATEKEY at letters-only index 1238', idx2 == 1238, idx2)
check('architect text ends CIAOBELLAO', architect.endswith('CIAOBELLAO'), architect[-15:])
check('architect text length 1539', len(architect)==1539, len(architect))

# ---------------- Straddling checkerboard (section 3.4b) ----------------
digits_start = 1990
digits_end = 2139
digits_raw = pt32[digits_start:digits_end]
check('digit block is CRLF CRLF-bounded, all ASCII digits', all(48<=b<=57 for b in digits_raw), digits_raw[:20])
digits = digits_raw.decode('ascii')
check('149 digits', len(digits)==149, len(digits))

dossier_digits = lib.block_joined(9, sep='')
check('derived digits == dossier block 9', digits == dossier_digits, '')

# Extracted by grep from the dossier (section 6.4b), never hand-retyped:
#   grep -n "FUBCDORA" GSMG-PUZZLE-DOSSIER.md
KEYROW = "FUBCDORA.LETHINGKYMVPS/JQZXW"

# Standard straddling-checkerboard layout: lay the 28 key symbols left-to-right
# across the top row's 8 non-blank digit slots (in digit order, skipping the
# two blank digits), then continue the same stream into the two 10-cell
# extension rows for the two blank digits, in ascending digit order.
def straddle_decode(digits, keystr, blanks):
    # keystr: 28 letters (A-Z plus '.' for the doubled letter used as a placeholder), laid across
    # a 0-9 top row skipping the two blank positions, then two 10-char rows for codes starting with each blank digit.
    letters = list(keystr)
    top = {}
    two = {blanks[0]: {}, blanks[1]: {}}
    pos = 0
    order0 = [d for d in range(10) if d not in blanks]
    for d in order0:
        top[d] = letters[pos]; pos += 1
    for b in blanks:
        for d in range(10):
            two[b][d] = letters[pos]; pos += 1
    out = []
    i = 0
    while i < len(digits):
        d = int(digits[i])
        if d in blanks:
            d2 = int(digits[i+1])
            out.append(two[d][d2])
            i += 2
        else:
            out.append(top[d])
            i += 1
    return ''.join(out)

# The literal 28-character key string lays out exactly across 8+10+10 slots.
# '.' and '/' are both placeholder symbols (the dot convention, section 7.3) that
# happen to land on checkerboard slots the real 149-digit stream never indexes.
KEYSTR = KEYROW
check('checkerboard key has 28 symbols (8 + 10 + 10)', len(KEYSTR)==28, (len(KEYSTR), KEYSTR))

checker_pt = straddle_decode(digits, KEYSTR, (1, 4))
dossier_checker_pt = lib.block_joined(10, sep='')
check('straddling-checkerboard decode (real digits, blanks={1,4} ascending) == dossier block 10',
      checker_pt == dossier_checker_pt, checker_pt)
print('\ncheckerboard plaintext (derived from real ciphertext):', checker_pt)

print('\nSUMMARY:', len(PASS), 'passed,', len(FAIL), 'failed')
if FAIL: print('FAILURES', FAIL)
sys.exit(1 if FAIL else 0)
