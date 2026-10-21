import sys
import hashlib, base64, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

PASS=[]; FAIL=[]
def check(name, cond, detail=''):
    (PASS if cond else FAIL).append(name)
    print(('PASS ' if cond else 'FAIL '), name, ' ', detail)

pt32 = open(str(Path(__file__).resolve().parent / 'out' / 'phase32_plaintext.bin'),'rb').read()

# ---- Terminal container: tail of phase3.2 plaintext, from real ciphertext ----
terminal_b64 = pt32[2292:].decode('ascii')
terminal_b64_joined = ''.join(terminal_b64.split())
terminal_raw = base64.b64decode(terminal_b64_joined)
check('Terminal starts Salted__', terminal_raw[:8]==b'Salted__', terminal_raw[:8])
tsalt = terminal_raw[8:16]
check('Terminal salt == pinned', tsalt.hex()=='b45a5e3d827593ca', tsalt.hex())
# dossier's "ciphertext" column is the AES-ciphertext length, i.e. total raw blob minus the 16-byte Salted__+salt header
check('Terminal AES-ciphertext length 80B (total blob 96B)', len(terminal_raw)-16 == 80, len(terminal_raw))
# dossier pins sha256 of the decoded Salted__+salt+ciphertext bytes, not of the base64 text
th = hashlib.sha256(terminal_raw).hexdigest()
check('Terminal sha256(decoded raw bytes) == pinned', th=='291dfd6f3e759ec2e272b35a00c24907da70c3e7a9291b4c13605c7b0b4f3de9', th)

with open(str(Path(__file__).resolve().parent / 'out' / 'terminal.bin'), 'wb') as f:
    f.write(terminal_raw)

# ---- SalPhaseIon short + Cosmic Duality, from the real archived salphaseion_phase3.html ----
html3 = lib.read_source('pages/salphaseion_phase3.html')
tas = lib.extract_textarea_contents(html3)
check('salphaseion_phase3.html has 2 textareas', len(tas)==2, len(tas))

textarea_raw = tas[0]
textarea_nospace = ''.join(textarea_raw.split())
check('SalPhaseIon textarea length 1075 (no separators)', len(textarea_nospace)==1075, len(textarea_nospace))

# whitespace channel check (doc 109): count separators, confirm all single 0x20
seps = re.findall(r'\s+', textarea_raw)
check('all whitespace separators are single 0x20 (no channel)', all(s==' ' for s in seps), f'{len(seps)} separators, distinct={set(seps)}')
check('separator count == 1074', len(seps)==1074, len(seps))

with open(str(Path(__file__).resolve().parent / 'out' / 'textarea.txt'),'w') as f:
    f.write(textarea_nospace)

dossier_textarea = lib.block_joined(11, sep='')
check('textarea (real HTML, despaced) == dossier block 11', textarea_nospace==dossier_textarea, '')

# SalPhaseIon short container = last 128 chars of textarea (two b64 halves joined)
sps_b64 = textarea_nospace[895:959] + textarea_nospace[999:1063]
sps_raw = base64.b64decode(sps_b64)
check('SalPhaseIon-short starts Salted__', sps_raw[:8]==b'Salted__', sps_raw[:8])
spssalt = sps_raw[8:16]
check('SalPhaseIon-short salt == pinned', spssalt.hex()=='3ab585348552415d', spssalt.hex())
check('SalPhaseIon-short AES-ciphertext length 80B (total blob 96B)', len(sps_raw)-16 == 80, len(sps_raw))
sps_sha = hashlib.sha256(sps_raw).hexdigest()
check('SalPhaseIon-short sha256(decoded raw bytes) == pinned', sps_sha=='9e2831e1b34b5f34796df47ccaf6530d48d371c61a6bff84d60db1064fa7a258', sps_sha)

dossier_sps = lib.block_joined(17, sep='')
check('SalPhaseIon-short b64 == dossier block 17', sps_b64==dossier_sps, '')

# Cosmic Duality
cosmic_raw_b64 = ''.join(tas[1].split())
cosmic_raw = base64.b64decode(cosmic_raw_b64)
check('Cosmic starts Salted__', cosmic_raw[:8]==b'Salted__', cosmic_raw[:8])
csalt = cosmic_raw[8:16]
check('Cosmic salt == pinned', csalt.hex()=='2d3f6fe06dc950e6', csalt.hex())
check('Cosmic AES-ciphertext length 1328B (total blob 1344B)', len(cosmic_raw)-16==1328, len(cosmic_raw))
csha = hashlib.sha256(cosmic_raw).hexdigest()
check('Cosmic sha256(decoded raw bytes) == pinned', csha=='b18950551a4dd0cb8a9378f0906ba18c03a15f0ee83eb98c6bc90165c5f79805', csha)

dossier_cosmic = lib.block_joined(18, sep='')
check('Cosmic b64 == dossier block 18', cosmic_raw_b64==dossier_cosmic, '')

with open(str(Path(__file__).resolve().parent / 'out' / 'cosmic.bin'),'wb') as f:
    f.write(cosmic_raw)

print('\nSUMMARY:', len(PASS), 'passed,', len(FAIL), 'failed')
if FAIL: print('FAILURES', FAIL)
sys.exit(1 if FAIL else 0)
