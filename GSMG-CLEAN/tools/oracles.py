"""Self-checks that do not touch an envelope.

These are the four artifact types a preregistered experiment may predict (tools/prereg.py):

  readable_text         english_score() against shuffled-input controls
  known_digest          known_digest(): sha256 of the output is a digest authenticated in 01
  known_address         known_address(): the output, as scalar or as sha256 seed, derives a
                        marker address (01 section 9) or a prize address
  exact_reconstruction  longest_common_run(): the output reproduces a held artifact

Nothing here reads data/locked_*.  Run  python tools/oracles.py  for the planted controls.
"""
import hashlib
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prize_gate  # noqa: E402  (shared checker: hash160, base58, secp256k1)

# --- digests authenticated by the solved chain (01_PROVEN_CHAIN) -------------------------------------
KNOWN_DIGESTS = {
    '5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75': 'Phase 1 answer (creator #225)',
    'eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf': 'Phase 2 password (causality)',
    '1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5': 'Phase 3 password (seven parts)',
    '250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c': 'Phase 3.2 password',
    '89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32': 'SalPhaseIon page path',
}
# --- addresses: the two prize targets and the four solved dust markers (01 section 9) ----------------
KNOWN_ADDRESSES = {
    '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe': 'PRIZE Half',
    '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa': 'PRIZE Better Half',
    '18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc': 'marker: sha256(149 checkerboard digits)',
    '1AD2wfwXukZ1kUAy848hTQQ72aSBZPB75r': 'marker: sha256(Phase 1 answer)',
    '13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp': 'marker: bit-reversed URL integer',
    '1GyT5WrLYpwFkuiVoPDJZa1Q6jtjbjuBff': 'marker: sha256(prize address)',
}
_TARGETS = {name: prize_gate.b58check_decode(addr)[1:] for addr, name in KNOWN_ADDRESSES.items()}
DBBI_PATTERN = '01234556728966286abc61c88b48de3086dd501d5557d6bab5605233df7bbb96'


def known_digest(value):
    """value: str or bytes.  Returns the label of the authenticated digest it hashes to, or None."""
    data = value.encode() if isinstance(value, str) else value
    return KNOWN_DIGESTS.get(hashlib.sha256(data).hexdigest())


def dbbi_pattern(value):
    """True if sha256(value) has the repeat structure of DBBI's 64 tokens (lead 2 in 03)."""
    data = value.encode() if isinstance(value, str) else value
    first = {}
    pat = ''.join('0123456789abcdef'[first.setdefault(c, len(first))] for c in hashlib.sha256(data).hexdigest())
    return pat == DBBI_PATTERN


def known_address(value):
    """value: str or bytes.  Tries sha256(value) as a scalar, and value itself when it is 32 raw
    bytes or 64 hex characters.  Returns a list of (form, label) matches (normally empty)."""
    data = value.encode() if isinstance(value, str) else value
    scalars = {'sha256': int.from_bytes(hashlib.sha256(data).digest(), 'big')}
    if len(data) == 32:
        scalars['raw32'] = int.from_bytes(data, 'big')
    if re.fullmatch(rb'[0-9a-fA-F]{64}', data):
        scalars['hex64'] = int(data, 16)
    hits = []
    for form, k in scalars.items():
        res = prize_gate.gate_scalar(k, _TARGETS)
        if res:
            hits += [(form, name) for name in res['matches'] if name in _TARGETS]
    return hits


# --- readable text: letter quadgrams trained on the reference texts ---------------------------------
_MODEL = None


def _model():
    global _MODEL
    if _MODEL is None:
        text = ''
        for name in ('looking_forward_fresco_keyes_1969.txt', 'matrix_reloaded_architect_scene_transcript.txt'):
            text += (ROOT / 'reference_texts' / name).read_text(encoding='utf-8', errors='ignore')
        letters = re.sub('[^a-z]', '', text.lower())
        counts = Counter(letters[i:i + 4] for i in range(len(letters) - 3))
        total = sum(counts.values())
        floor = math.log10(0.01 / total)
        _MODEL = ({q: math.log10(c / total) for q, c in counts.items()}, floor)
    return _MODEL


def english_score(text):
    """Mean log10 quadgram probability over the letters of text (None if under 8 letters).
    English prose scores about -4.0 to -4.4; uniform random letters about -6.3."""
    letters = re.sub('[^a-z]', '', text.lower())
    if len(letters) < 8:
        return None
    table, floor = _model()
    return sum(table.get(letters[i:i + 4], floor) for i in range(len(letters) - 3)) / (len(letters) - 3)


def longest_common_run(a, b):
    """Length and text of the longest substring shared by a and b."""
    best, end, prev = 0, 0, [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        ai = a[i - 1]
        for j in range(1, len(b) + 1):
            if ai == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best, end = cur[j], i
        prev = cur
    return best, a[end - best:end]


def selftest():
    # digests and addresses: the four marker keys of 01 section 9 must be re-derived
    assert known_digest('causality') == 'Phase 2 password (causality)'
    assert known_digest('causalitx') is None
    vic = ('15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631'
           '213131281491109166131412199114371612126021664313711154112')
    assert ('sha256', 'marker: sha256(149 checkerboard digits)') in known_address(vic)
    assert ('sha256', 'marker: sha256(Phase 1 answer)') in known_address(
        'theflowerblossomsthroughwhatseemstobeaconcretesurface')
    assert ('sha256', 'marker: sha256(prize address)') in known_address('1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe')
    bits = ''.join(f'{b:08b}' for b in b'gsmg.io/theseedisplanted')
    assert ('raw32', 'marker: bit-reversed URL integer') in known_address(int(bits[::-1], 2).to_bytes(32, 'big'))
    assert known_address('not a key') == []
    # readable text: prose beats its own shuffle and random letters
    import random
    rnd = random.Random(1)
    prose = 'yourlifeisthesumofaremainderofanunbalancedequationinherenttotheprogrammingofthispuzzle'
    shuffled = ''.join(rnd.sample(prose, len(prose)))
    noise = ''.join(rnd.choice('abcdefghijklmnopqrstuvwxyz') for _ in prose)
    s = [english_score(x) for x in (prose, shuffled, noise)]
    assert s[0] > -4.6 and s[0] > s[1] + 0.8 and s[0] > s[2] + 1.2, s
    assert longest_common_run('xxabcdefyy', 'qqabcdefzz') == (6, 'abcdef')
    assert not dbbi_pattern('causality')
    print(f'ORACLE SELFTEST PASSED (5 digests, 4 marker addresses re-derived, prose {s[0]:.2f} vs '
          f'shuffle {s[1]:.2f} vs noise {s[2]:.2f}, backend {prize_gate.BACKEND})')


if __name__ == '__main__':
    selftest()
