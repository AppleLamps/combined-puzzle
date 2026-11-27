#!/usr/bin/env python3
"""Build the Cosmic null-validity gap set from five committed manifests.

No candidate is created here. Every string is read out of a file already in the
repository; this script only unions, de-duplicates and hashes. AES is not used:
the envelope test is a separate, preregistered step (see PREREG.json).

  python runs/2026-11-27_cosmic_null_validity/build_gap_set.py

Writes, next to this script:
  gap_candidates.txt     one candidate per line, UTF-8, verbatim
  gap_provenance.tsv     candidate -> every source that produced it
  gap_manifest.json      counts, source hashes, extraction controls (SELFCHECK evidence)
"""
import glob
import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]                       # GSMG-CLEAN
REPO = ROOT.parent                           # combined-puzzle
PUZ = REPO / 'puzle' / 'gsmgio-5btc-puzzle-master'
FIVEG = REPO / '5g-puzzle' / 'packet'

sys.path.insert(0, str(PUZ))

SENTINELS = ['yellowblueprimes', 'theunityofopposites', 'yinyang',
             'a795de117e472590e572dc193130c763e3fb555ee5db9d34494e156152e50735']
ABSENT_PLANT = 'planted-control-string-that-must-not-be-extracted-4f7a1e4e'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unity():
    path = PUZ / 'unity_of_opposites_audit.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    return [(s, 'unity_of_opposites_audit.json/phrases_sealed') for s in data['phrases_sealed']], [path]


def packet():
    spec_path = FIVEG / 'password_list_audit.json'
    spec = json.loads(spec_path.read_text(encoding='utf-8'))
    words, used = [], [spec_path]
    for name in spec['inherit_password_lists']:
        path = FIVEG / name
        used.append(path)
        words.extend(json.loads(path.read_text(encoding='utf-8'))['passwords'])
    words.extend(spec['passwords'])
    ordered = list(dict.fromkeys(words))
    return [(w, '5g-puzzle packet frozen list: ' + spec_path.name) for w in ordered], used


def creator_texts():
    from solver.intertwined_password_coherence_audit import _creator_texts
    rows = []
    for name, value in _creator_texts().items():
        text = value.decode('utf-8') if isinstance(value, bytes) else value
        rows.append((text, 'v50 _creator_texts/' + name))
    src = PUZ / 'solver' / 'intertwined_password_coherence_audit.py'
    return rows, [src]


def checkpoint_key():
    src = REPO / 'gsmg-haiku' / 'review_leads' / 'CHECKPOINT_4F7A_VS_A5502.md'
    text = src.read_text(encoding='utf-8')
    key = re.search(r'\b(a795de11[0-9a-f]{56})\b', text).group(1)
    return [(key, 'CHECKPOINT_4F7A_VS_A5502.md master key')], [src]



def salphaseion_text():
    """Text-representable preimages of the sealed v1..v22 rounds.

    Byte-only preimages cannot be expressed as a check_candidate answer string;
    they are counted, not silently dropped.
    """
    rows, used, byte_only = [], [], set()
    pre = {}
    for path in sorted(glob.glob(str(PUZ / 'salphaseion_preregistered_candidates*.json'))):
        m = re.search(r'_v(\d+)\.json$', os.path.basename(path))
        version = int(m.group(1)) if m else 1
        if version > 22:
            continue
        used.append(Path(path))
        for cand in json.loads(Path(path).read_text(encoding='utf-8'))['candidates']:
            pre.setdefault(cand['preimage_hex'], cand)
    for hexed, cand in pre.items():
        raw = bytes.fromhex(hexed)
        text = None
        for key in ('preimage_utf8', 'preimage_ascii'):
            if key in cand and cand[key].encode('utf-8') == raw:
                text = cand[key]
                break
        if text is None:
            try:
                guess = raw.decode('utf-8')
            except UnicodeDecodeError:
                guess = None
            if guess and guess.encode('utf-8') == raw and '\n' not in guess and '\r' not in guess:
                text = guess
        if text is None:
            byte_only.add(hexed)
            continue
        prov = cand['provenance'][0] if cand['provenance'] else ''
        rows.append((text, 'SALPHASEION_PREREGISTRATION v1-v22 / ' + prov))
    return rows, used, len(pre), len(byte_only)


def main():
    families = {}
    sources = []

    rows, used = unity();            families['unity_of_opposites'] = rows;      sources += used
    rows, used = packet();           families['packet_frozen'] = rows;           sources += used
    rows, used = creator_texts();    families['v50a_creator_texts'] = rows;      sources += used
    rows, used = checkpoint_key();   families['checkpoint_master_key'] = rows;   sources += used
    rows, used, n_pre, n_byte = salphaseion_text()
    families['salphaseion_v1_v22_text'] = rows; sources += used

    order, prov = [], {}
    for name, items in families.items():
        for text, source in items:
            if text not in prov:
                prov[text] = []
                order.append(text)
            prov[text].append(source)

    bad = [s for s in order if s == '' or '\n' in s or '\r' in s]
    if bad:
        raise SystemExit(f'{len(bad)} candidate(s) are empty or hold a line break')

    control = {
        'sentinels_present': {s: (s in prov) for s in SENTINELS},
        'planted_absent_present': ABSENT_PLANT in prov,
        'passed': all(s in prov for s in SENTINELS) and ABSENT_PLANT not in prov,
    }
    if not control['passed']:
        raise SystemExit(f'extraction control failed: {control}')

    (HERE / 'gap_candidates.txt').write_text('\n'.join(order) + '\n', encoding='utf-8', newline='\n')
    with (HERE / 'gap_provenance.tsv').open('w', encoding='utf-8', newline='\n') as fh:
        fh.write('candidate\tsources\n')
        for text in order:
            fh.write(text.replace('\t', ' ') + '\t' + ' | '.join(prov[text]) + '\n')

    manifest = {
        'schema': 'cosmic-null-validity-gap-set-v1',
        'prereg_sha256': json.loads((HERE / 'PREREG.sealed').read_text(encoding='utf-8'))['prereg_sha256'],
        'families': {k: len(v) for k, v in families.items()},
        'rows_read': sum(len(v) for v in families.values()),
        'unique_candidates': len(order),
        'duplicates_removed': sum(len(v) for v in families.values()) - len(order),
        'salphaseion_distinct_preimages': n_pre,
        'salphaseion_byte_only_preimages_not_carried': n_byte,
        'longest_candidate': max(len(s) for s in order),
        'shortest_candidate': min(len(s) for s in order),
        'candidate_file': 'gap_candidates.txt',
        'candidate_file_sha256': sha(HERE / 'gap_candidates.txt'),
        'provenance_file_sha256': sha(HERE / 'gap_provenance.tsv'),
        'source_files': {str(Path(p).relative_to(REPO)): sha(p) for p in sorted(set(sources))},
        'extraction_controls': control,
        'aes_used': False,
    }
    (HERE / 'gap_manifest.json').write_text(json.dumps(manifest, indent=1) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=1))


if __name__ == '__main__':
    main()
