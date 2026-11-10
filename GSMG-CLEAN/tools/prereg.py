"""Preregistration gate for experiments (working rules in 16_CANONICAL_LEDGER_AND_WORKING_RULES).

Every new experiment states, before any candidate is generated, the second artifact it
predicts.  The statement is sealed by hash, results are written afterwards, and only a
derivation whose self-check PASSED without AES may be handed to the envelope tester.

  python tools/prereg.py new    runs/2026-11-10_example     write a PREREG.json template
  python tools/prereg.py seal   runs/2026-11-10_example     validate and seal it (before results)
  python tools/prereg.py verify runs/2026-11-10_example     check the seal still matches
  python tools/prereg.py record runs/2026-11-10_example --outcome null|passed --evidence FILE [--note TEXT]
  python tools/prereg.py status runs/2026-11-10_example

Files in the run directory:
  PREREG.json     the statement (edit before sealing, never after)
  PREREG.sealed   sha256 of the canonical statement and the UTC time of sealing
  SELFCHECK.json  outcome of the non-AES self-check, bound to the seal and to an evidence file

The seal is a hash, not a timestamp authority.  Commit PREREG.json and PREREG.sealed
before the results so that the order is also visible in git history.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ARTIFACT_TYPES = {
    'readable_text':        'output reads as language, judged against shuffled-input controls',
    'known_digest':         'sha256 of the output equals a digest already authenticated in 01',
    'known_address':        'the output, as a key or key seed, derives a marker or prize address',
    'exact_reconstruction': 'output reproduces a named, already-held artifact character for character',
}
REQUIRED = ('hypothesis', 'source_support', 'operand', 'operation', 'predicted_artifact',
            'acceptance_rule', 'controls', 'candidate_bound', 'aes_use')
MAX_ENVELOPE_CANDIDATES = 256      # a derivation that needs more than this is a sweep, not a derivation

TEMPLATE = {
    'hypothesis': 'One sentence: what the puzzle step does.',
    'source_support': ['Creator message id or puzzle text that motivates it, quoted.'],
    'operand': 'Exactly which authenticated data goes in (file, range, parse).',
    'operation': 'The transformation, with every convention fixed (indexing, direction, modulus).',
    'predicted_artifact': {
        'type': 'readable_text | known_digest | known_address | exact_reconstruction',
        'detail': 'What will be seen if the hypothesis is right, and where.',
    },
    'acceptance_rule': 'The numeric or exact rule that separates pass from null, fixed in advance.',
    'controls': {
        'planted': 'A constructed input for which the rule must fire.',
        'null': 'The shuffled or random inputs the real output must beat.',
    },
    'candidate_bound': 0,
    'aes_use': 'none',
}


def canonical(statement):
    return json.dumps(statement, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()


def load(run):
    path = Path(run) / 'PREREG.json'
    if not path.exists():
        raise SystemExit(f'{path} not found: run "prereg.py new {run}" first')
    return json.loads(path.read_text(encoding='utf-8'))


def validate(statement):
    problems = []
    for key in REQUIRED:
        if key not in statement or statement[key] in ('', [], {}, None):
            problems.append(f'missing or empty field: {key}')
    art = statement.get('predicted_artifact') or {}
    if art.get('type') not in ARTIFACT_TYPES:
        problems.append('predicted_artifact.type must be one of: ' + ', '.join(sorted(ARTIFACT_TYPES)))
    if not str(art.get('detail', '')).strip():
        problems.append('predicted_artifact.detail is empty')
    ctl = statement.get('controls') or {}
    for key in ('planted', 'null'):
        if not str(ctl.get(key, '')).strip():
            problems.append(f'controls.{key} is empty')
    if statement.get('aes_use') != 'none':
        problems.append('aes_use must be "none": the self-check may not touch an envelope')
    if not isinstance(statement.get('candidate_bound'), int) or statement.get('candidate_bound', 0) <= 0:
        problems.append('candidate_bound must be a positive integer (how many outputs the experiment may produce)')
    for key, value in TEMPLATE.items():
        if key in statement and statement[key] == value and key not in ('aes_use',):
            problems.append(f'field still holds the template text: {key}')
    return problems


def seal_record(run):
    path = Path(run) / 'PREREG.sealed'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else None


def cmd_new(run):
    run = Path(run)
    run.mkdir(parents=True, exist_ok=True)
    path = run / 'PREREG.json'
    if path.exists():
        raise SystemExit(f'{path} already exists')
    path.write_text(json.dumps(TEMPLATE, indent=2) + '\n', encoding='utf-8')
    print(f'wrote {path}; fill it in, then: python tools/prereg.py seal {run}')


def cmd_seal(run):
    run = Path(run)
    statement = load(run)
    problems = validate(statement)
    if problems:
        raise SystemExit('cannot seal:\n  ' + '\n  '.join(problems))
    if (run / 'PREREG.sealed').exists():
        raise SystemExit('already sealed; a changed hypothesis is a new run directory')
    others = sorted(p.name for p in run.iterdir() if p.name != 'PREREG.json')
    if others:
        raise SystemExit('cannot seal: the run directory already holds other files (' + ', '.join(others[:5])
                         + '). The statement must exist before any output.')
    digest = hashlib.sha256(canonical(statement)).hexdigest()
    record = {'prereg_sha256': digest, 'sealed_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
    (run / 'PREREG.sealed').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print(f'sealed {run}: {digest}')


def verify(run):
    """Return the seal digest if the statement is sealed and unchanged, else raise SystemExit."""
    statement, record = load(run), seal_record(run)
    if record is None:
        raise SystemExit(f'{run} is not sealed')
    digest = hashlib.sha256(canonical(statement)).hexdigest()
    if digest != record['prereg_sha256']:
        raise SystemExit(f'{run}: PREREG.json changed after sealing ({digest} != {record["prereg_sha256"]})')
    return digest


def cmd_record(run, outcome, evidence, note):
    run = Path(run)
    digest = verify(run)
    ev = Path(evidence)
    if not ev.exists():
        raise SystemExit(f'evidence file {ev} not found')
    record = {
        'outcome': outcome,
        'prereg_sha256': digest,
        'evidence_file': ev.name if ev.parent.resolve() == run.resolve() else str(ev),
        'evidence_sha256': hashlib.sha256(ev.read_bytes()).hexdigest(),
        'recorded_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'note': note or '',
    }
    (run / 'SELFCHECK.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print(f'recorded {outcome} for {run}')


def require_passed(run):
    """Used by the envelope tester: a derivation is eligible only if it is sealed, unchanged,
    and its recorded non-AES self-check PASSED.  Returns the candidate bound."""
    run = Path(run)
    digest = verify(run)
    path = run / 'SELFCHECK.json'
    if not path.exists():
        raise SystemExit(f'{run} has no SELFCHECK.json: run the self-check and record it first')
    check = json.loads(path.read_text(encoding='utf-8'))
    if check.get('prereg_sha256') != digest:
        raise SystemExit(f'{run}: SELFCHECK.json belongs to a different statement')
    if check.get('outcome') != 'passed':
        raise SystemExit(f'{run}: self-check outcome is {check.get("outcome")!r}. Only a derivation that '
                         'already checked itself without AES may be tried on an envelope.')
    ev = run / check['evidence_file'] if not Path(check['evidence_file']).is_absolute() else Path(check['evidence_file'])
    if not ev.exists() or hashlib.sha256(ev.read_bytes()).hexdigest() != check['evidence_sha256']:
        raise SystemExit(f'{run}: evidence file missing or changed since it was recorded')
    return min(int(load(run)['candidate_bound']), MAX_ENVELOPE_CANDIDATES)


def cmd_status(run):
    statement, record = load(run), seal_record(run)
    print('hypothesis :', statement.get('hypothesis'))
    print('artifact   :', (statement.get('predicted_artifact') or {}).get('type'))
    print('sealed     :', record['sealed_utc'] if record else 'no')
    if record:
        verify(run)
        path = Path(run) / 'SELFCHECK.json'
        print('self-check :', json.loads(path.read_text())['outcome'] if path.exists() else 'not recorded')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('new', 'seal', 'verify', 'status'):
        sub.add_parser(name).add_argument('run')
    rec = sub.add_parser('record')
    rec.add_argument('run')
    rec.add_argument('--outcome', choices=('null', 'passed'), required=True)
    rec.add_argument('--evidence', required=True)
    rec.add_argument('--note')
    a = ap.parse_args(argv)
    if a.cmd == 'new':
        cmd_new(a.run)
    elif a.cmd == 'seal':
        cmd_seal(a.run)
    elif a.cmd == 'verify':
        print('seal ok:', verify(a.run))
    elif a.cmd == 'record':
        cmd_record(a.run, a.outcome, a.evidence, a.note)
    else:
        cmd_status(a.run)


if __name__ == '__main__':
    main()
