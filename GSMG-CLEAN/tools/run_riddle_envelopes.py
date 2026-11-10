"""Owner-authorized exception to the no-envelope-sweep rule (16 section 2).

The repository owner authorized, on 2026-11-10, trying a short fixed list of riddle answers against the
three locked envelopes, accepted ONLY on a coherent decrypt or a key match, NEVER on padding alone.
This script is that test and nothing else: it does not sweep, generate, or mutate; the list below is
fixed in the source and committed before the run.

  python tools/run_riddle_envelopes.py runs/2026-11-10_riddle_envelopes

Convention (the one proven on three solved stages, 01 section 0): password = sha256(answer) as 64
lowercase hex, EVP_BytesToKey(SHA-256, 1 iteration), AES-256-CBC, PKCS#7.

Acceptance (a candidate OPENS an envelope only if):
  - a private key in the plaintext derives Half or Better Half (find_keys), or
  - sha256(answer) has the DBBI token pattern, or
  - the plaintext is coherent: PKCS#7 pad >= 2 AND >= 90 percent printable AND English score > -5.0.
A pad of 1, or pad-valid noise, is NOT an opening and is reported as such.

A positive control decrypts the Phase 3.2 envelope with its known answer and must read as coherent,
so a real opening cannot be missed by the judge.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_candidate as cc  # noqa: E402  (try_envelope, find_keys, eq_pattern, ENVELOPES)
import oracles  # noqa: E402

# --- the fixed list: the door / "knock knock" reading and the most plausible final-stage answers ---
ANSWERS = [
    # the fourth screen line and its door, in the forms a solver would type
    'knockknock', 'knockknockneo', 'knockknocksneo', 'knock knock', 'knock knock neo',
    'Knock, knock, Neo.', 'Knock, knock, Neo', 'knockknockneo.', 'whosthere', 'whoisit',
    # follow the white rabbit (the creator's stated first hint)
    'followthewhiterabbit', 'follow the white rabbit', 'Follow the white rabbit',
    'Follow the white rabbit.', 'whiterabbit', 'thewhiterabbit',
    # the other screen lines
    'thematrixhasyou', 'wakeupneo', 'wakeupyou',
    # the creator's "another door" wording
    'anotherdoor', 'thereisanotherdoor', 'theotherdoor', 'seconddoor', 'thirddoor',
    'extradoor', 'theextradoor', 'door', 'thedoor', 'openthedoor', 'opendoor',
    # the nest / poem / room 101
    'therabbitsnest', 'downtherabbithole', 'rabbithole', 'room101', 'hushhush',
    # the label itself and the decoded command chain tail
    'ourfirsthintisyourlastcommand', 'firsthintisyourlastcommand',
    'yinyang', 'yingyang', 'cosmicduality', 'wewontgiveawaythepassword',
]
PRINTABLE = set(range(0x20, 0x7F)) | {0x09, 0x0A, 0x0D}


def coherence(pt):
    if not pt:
        return 0.0, None
    frac = sum(b in PRINTABLE for b in pt) / len(pt)
    text = ''.join(chr(b) if b in PRINTABLE else ' ' for b in pt)
    return frac, oracles.english_score(text)


def judge(answer):
    rows = []
    opened = False
    dbbi = cc.eq_pattern(hashlib.sha256(answer.encode()).hexdigest()) == cc.DBBI_PATTERN
    for name, raw in cc.ENVELOPES.items():
        pad, pt = cc.try_envelope(raw, answer, 'gsmg')
        if not pad:
            rows.append({'envelope': name, 'pad': 0})
            continue
        keys = [(d, h) for d, h in cc.find_keys(pt) if h]
        frac, score = coherence(pt)
        coherent = pad >= 2 and frac >= 0.90 and score is not None and score > -5.0
        open_here = bool(keys) or coherent
        opened |= open_here
        rows.append({'envelope': name, 'pad': pad, 'len': len(pt), 'printable': round(frac, 3),
                     'english': round(score, 2) if score is not None else None,
                     'key_hits': keys, 'coherent': coherent, 'opens': open_here,
                     'plaintext_head': pt[:48].decode('latin-1')})
    return {'answer': answer, 'dbbi_pattern': dbbi, 'opens_any': opened or dbbi, 'envelopes': rows}


def positive_control():
    data = (ROOT / 'data' / 'phase3_plaintext.bin').read_bytes()
    import base64
    env = base64.b64decode(re.sub(rb'\s+', b'', data[data.index(b'U2FsdGVk'):]))
    pad, pt = cc.try_envelope(env, 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple', 'gsmg')
    frac, score = coherence(pt)
    return {'pad': pad, 'len': len(pt), 'printable': round(frac, 3), 'english': round(score, 2),
            'passed': pad == 10 and len(pt) == 2422 and frac > 0.5}


def main(run_dir):
    run = Path(run_dir)
    run.mkdir(parents=True, exist_ok=True)
    ctl = positive_control()
    assert ctl['passed'], ('positive control failed', ctl)
    results = [judge(a) for a in ANSWERS]
    openers = [r for r in results if r['opens_any']]
    out = {
        'authorization': 'Repository owner, 2026-11-10: try a short fixed list of riddle answers against '
                         'the three envelopes, judged by a full decrypt, never by padding.',
        'convention': 'password = sha256(answer) hex; EVP_BytesToKey SHA-256 1 iter; AES-256-CBC; PKCS#7',
        'acceptance': 'key match, or DBBI token pattern, or pad>=2 and printable>=0.90 and english>-5.0',
        'positive_control': ctl,
        'candidates': len(ANSWERS),
        'openers': [r['answer'] for r in openers],
        'results': results,
    }
    (run / 'results.json').write_text(json.dumps(out, indent=1) + '\n', encoding='utf-8')
    print(f'positive control: pad {ctl["pad"]}, {ctl["len"]} bytes, printable {ctl["printable"]} -> passed')
    print(f'{len(ANSWERS)} answers x 3 envelopes, proven convention, judged by decrypt:')
    for r in results:
        best = max(r['envelopes'], key=lambda e: e.get('pad', 0))
        tag = 'OPENS' if r['opens_any'] else ('pad%d' % best.get('pad', 0))
        extra = ''
        if best.get('pad', 0) >= 2:
            extra = f" | best {best['envelope']} pad{best['pad']} printable{best.get('printable')} en{best.get('english')}"
        print(f"  {tag:>6}  {r['answer']:<32}{extra}")
    print('\nOPENERS:', out['openers'] or 'none')
    return out['openers']


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'runs' / '2026-11-10_riddle_envelopes')
