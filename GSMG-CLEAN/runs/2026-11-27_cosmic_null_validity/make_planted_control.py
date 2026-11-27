#!/usr/bin/env python3
"""Build and fire the planted control for the pinned-profile envelope loop.

No canonical file is modified. A byte-identical copy of tools/check_candidate.py
is run against a sandboxed data/ directory in which one locked envelope is
replaced by a synthetic Salted__ blob whose password is known. The control passes
only if the production loop prints [STRONG pad] pad=16 for the known answer.

  python runs/2026-11-27_cosmic_null_validity/make_planted_control.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from Crypto.Cipher import AES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]                      # GSMG-CLEAN
SANDBOX = Path(os.environ.get('TEMP', '.')) / 'cosmic_audit' / 'planted'
ANSWER = 'planted control opens here'
BODY = b'PLANTED CONTROL OPENS THIS ENVELOPE.'
SALT = bytes.fromhex('2d3f6fe06dc950e6')    # the Cosmic salt, so the control uses the same stream
TARGET = 'locked_terminal_phase3_2_end.bin'


def evp(password, salt, md):
    derived = previous = b''
    while len(derived) < 48:
        previous = md(previous + password + salt).digest()
        derived += previous
    return derived[:32], derived[32:48]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    if SANDBOX.exists():
        shutil.rmtree(SANDBOX)
    (SANDBOX / 'tools').mkdir(parents=True)
    (SANDBOX / 'data').mkdir()
    shutil.copy2(ROOT / 'tools' / 'check_candidate.py', SANDBOX / 'tools' / 'check_candidate.py')
    for name in ('locked_terminal_phase3_2_end.bin', 'locked_salphaseion_short.bin',
                 'locked_cosmic_duality.bin', 'phase3_plaintext.bin'):
        shutil.copy2(ROOT / 'data' / name, SANDBOX / 'data' / name)

    body = BODY + b'X' * (64 - len(BODY))                  # exactly 64 bytes -> pad 16
    assert len(body) == 64
    password = hashlib.sha256(ANSWER.encode()).hexdigest().encode()   # the pinned profile
    key, iv = evp(password, SALT, hashlib.sha256)
    ciphertext = AES.new(key, AES.MODE_CBC, iv).encrypt(body + bytes([16]) * 16)
    blob = b'Salted__' + SALT + ciphertext
    assert len(blob) == 96

    key2, iv2 = evp(password, blob[8:16], hashlib.sha256)
    check = AES.new(key2, AES.MODE_CBC, iv2).decrypt(blob[16:])
    assert check[-1] == 16 and check[-16:] == bytes([16]) * 16 and check[:-16] == body

    (SANDBOX / 'data' / TARGET).write_bytes(blob)
    proc = subprocess.run([sys.executable, str(SANDBOX / 'tools' / 'check_candidate.py'), ANSWER],
                          capture_output=True, text=True)
    log = proc.stdout + proc.stderr
    (HERE / 'planted_control.log').write_text(
        'sandbox: %s\nanswer: %r\nsynthetic blob: %d bytes, salt %s, plaintext 64 B, pad 16\n'
        'script under test: %s sha256 %s\nscript copied from: %s sha256 %s\n--- run ---\n%s'
        % (SANDBOX, ANSWER, len(blob), SALT.hex(),
           SANDBOX / 'tools' / 'check_candidate.py', sha(SANDBOX / 'tools' / 'check_candidate.py'),
           ROOT / 'tools' / 'check_candidate.py', sha(ROOT / 'tools' / 'check_candidate.py'), log),
        encoding='utf-8')

    fired = '[STRONG pad]' in log and 'pad=16' in log and 'terminal_phase3_2_end' in log
    result = {'answer': ANSWER, 'fired': fired, 'returncode': proc.returncode,
              'script_sha256': sha(ROOT / 'tools' / 'check_candidate.py'),
              'synthetic_blob_sha256': hashlib.sha256(blob).hexdigest()}
    (HERE / 'planted_control.json').write_text(json.dumps(result, indent=1) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=1))
    print(log)
    return 0 if fired else 1


if __name__ == '__main__':
    raise SystemExit(main())
