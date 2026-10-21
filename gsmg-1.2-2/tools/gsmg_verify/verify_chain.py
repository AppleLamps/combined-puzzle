import sys
import hashlib, re, base64
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

PASS = []
FAIL = []

def check(name, cond, detail=''):
    if cond:
        PASS.append(name)
        print(f'PASS  {name}   {detail}')
    else:
        FAIL.append(name)
        print(f'FAIL  {name}   {detail}')

# =================================================================
# 0. Poster image primary bytes
# =================================================================
poster_bytes = open(f'{lib.REPO}/source/poster/puzzle.png', 'rb').read()
h = hashlib.sha256(poster_bytes).hexdigest()
check('poster sha256 pinned', h == '38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830', h)
check('poster size 29931', len(poster_bytes) == 29931, len(poster_bytes))

# =================================================================
# 1. Phase 1 page structure (real archived HTML, not the dossier's prose)
# =================================================================
html1 = lib.read_source('pages/theseedisplanted.html')
imgs = re.findall(r'<img src="\.\./images/rebus/([^"]+)"', html1)
check('rebus tile order (real HTML)', imgs == [
    'black_banking - war.png', 'blue_ca.png', 'blue_dig_i.png', 'blue_lock_lo.png',
    'red_crypto_gic.png', 'red_n_you.png', 'red_open_lock_n_ing.png', 'red_t.png'
], imgs)

answer1 = 'theflowerblossomsthroughwhatseemstobeaconcretesurface'
h1 = hashlib.sha256(answer1.encode()).hexdigest()
check('phase1 answer sha256 == creator-posted hash', h1 == '5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75', h1)

# =================================================================
# 2. Phase 2: decrypt textarea 1 of phase2_choice.html with sha256(answer1) hex
# =================================================================
html2 = lib.read_source('pages/phase2_choice.html')
textareas2 = lib.extract_textarea_contents(html2)
check('phase2_choice.html has 2 textareas', len(textareas2) == 2, len(textareas2))
answer2 = 'causality'
p2_b64 = lib.b64_join_lines(textareas2[0])
pt2, pad2, salt2 = lib.decrypt_b64_container(p2_b64, answer2)
check('phase2 decrypt valid padding', pt2 is not None, f'pad={pad2}')
check('phase2 salt == pinned', salt2.hex() == '06286612d43ed7ed', salt2.hex())
check('phase2 plaintext length 648', len(pt2) == 648, len(pt2))
h2 = hashlib.sha256(pt2).hexdigest()
check('phase2 plaintext sha256 == pinned', h2 == 'e2f9dd65604a3231f8b3301724e8d713a88fffc4b6c7c4aeeb20f58a582b593a', h2)

pt2_text = pt2.decode('utf-8')
print('\n--- phase2 plaintext (decrypted from real ciphertext) ---')
print(pt2_text)
print('--- end phase2 plaintext ---\n')

# cross-check against dossier's rendered block (idx 3), CRLF-joined
dossier_p2_lines = lib.block_lines(3)
dossier_p2 = '\r\n'.join(dossier_p2_lines)
check('phase2 plaintext matches dossier block (CRLF-joined)', dossier_p2.encode() == pt2, '')

# =================================================================
# 3. Phase 3 seven-part answer, extracted from dossier's numbered list by regex (not retyped)
# =================================================================
lines = lib.dossier_lines()
parts = {}
for i, l in enumerate(lines):
    m = re.match(r'^(\d)\. `(.*)`$', l)
    if m and 1 <= int(m.group(1)) <= 7 and 505 <= i+1 <= 515:
        parts[int(m.group(1))] = m.group(2)
check('extracted exactly 7 phase3 parts', len(parts) == 7, parts)
answer3 = ''.join(parts[i] for i in range(1, 8))
print('phase3 answer (concat of 7 parts):', answer3)

# independent derivation check for part 6: genesis message byte-reversed hex
# (dossier renders hex in uppercase; content is compared case-insensitively)
genesis_msg = b"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"
part6_expected = '0x' + genesis_msg[::-1].hex()
check('part6 == independently derived reversed-genesis hex (case-insensitive)',
      parts[6].lower() == part6_expected.lower(),
      f'len={len(parts[6])} derived_len={len(part6_expected)}')
check('part6 total length 140 (0x + 138 hex)', len(parts[6]) == 140, len(parts[6]))

# textarea 2 of phase2_choice.html (labelled H1 PHASE 3 in the real file)
p3_b64 = lib.b64_join_lines(textareas2[1])
pt3, pad3, salt3 = lib.decrypt_b64_container(p3_b64, answer3)
check('phase3 decrypt valid padding', pt3 is not None, f'pad={pad3}')
check('phase3 salt == pinned', salt3.hex() == '9fbc451d13d071f4', salt3.hex())
check('phase3 plaintext length 4090', len(pt3) == 4090, len(pt3))
h3 = hashlib.sha256(pt3).hexdigest()
check('phase3 plaintext sha256 == pinned', h3 == 'c4ad94559a44a927c1032cc0e024515f9510a0806a2d14458dbf4a360af9865f', h3)

# also verify FEN before/after white's move (page prose vs part7)
fen_before = re.search(r'<p>(B5KR[^<]+)</p>', html2).group(1)
check('FEN before shown on page (w to move) matches dossier prose', fen_before == 'B5KR/1r5B/6R1/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 w - - 0 1', fen_before)
check('part7 FEN is same position after Rg6-c6 (rook moved g6->c6, now black to move)',
      parts[7] == 'B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1', parts[7])

with open(str(Path(__file__).resolve().parent / 'out' / 'phase3_plaintext.bin'), 'wb') as f:
    f.write(pt3)

# =================================================================
# 4. Phase 3.2 container embedded in phase3 plaintext -> extract + decrypt
# =================================================================
riddle_head = pt3[:726]
tail = pt3[726:]
print('\n--- phase3 riddle head (first 726 bytes, decrypted) ---')
print(riddle_head.decode('utf-8', errors='replace'))
print('--- end riddle head ---\n')

# the tail should itself be base64 text of a Salted__ container
tail_text = tail.decode('ascii', errors='strict')
tail_b64 = lib.b64_join_lines(tail_text)
raw32 = base64.b64decode(tail_b64)
check('embedded phase3.2 container starts Salted__', raw32[:8] == b'Salted__', raw32[:8])
check('embedded phase3.2 ciphertext length 2432 (per dossier)', len(raw32) - 16 == 2432, len(raw32)-16)

answer32 = 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple'
pt32, pad32, salt32 = lib.openssl_decrypt(raw32, lib.sha256_hex_pw(answer32))
check('phase3.2 decrypt valid padding', pt32 is not None, f'pad={pad32}')
check('phase3.2 salt == pinned', salt32.hex() == 'eefc4c5befc1656a', salt32.hex())
check('phase3.2 plaintext length 2422', len(pt32) == 2422, len(pt32))
h32 = hashlib.sha256(pt32).hexdigest()
check('phase3.2 plaintext sha256 == pinned', h32 == 'b82afeb86f9e50848220f9b64b744b821400308aea273a1c949b9d2d0e408a34', h32)

printable = sum(1 for b in pt32 if 0x20 <= b < 0x7f or b in (0x0d, 0x0a))
frac = printable/len(pt32)
check('phase3.2 printable fraction ~= 58.9%%', abs(frac - 0.589) < 0.01, f'{frac:.4f}')

with open(str(Path(__file__).resolve().parent / 'out' / 'phase32_plaintext.bin'), 'wb') as f:
    f.write(pt32)

print('\n--- phase3.2 intro (bytes 0:447, decrypted) ---')
print(pt32[:447].decode('ascii', errors='replace'))
print('--- end intro ---\n')

print('SUMMARY:', len(PASS), 'passed,', len(FAIL), 'failed')
if FAIL:
    print('FAILURES:', FAIL)
sys.exit(1 if FAIL else 0)
