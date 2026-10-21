"""
Record 141 -- "your last command" = the puzzle's own last command.

Thesis. The SalPhaseIon literal reads "sha256, our first hint is your last
command". Two primary-source facts anchor it:

  * The creator's FIRST HINT in the group (#225, 2019-04-22) was the bare
    sha256 hash of the phase-1 answer, posted so solvers could "try their
    passwords" offline (#257). "Follow the white rabbit" is ALSO
    creator-authored (#11248 carries forwarded_from: Jrk Bgrt, as do four
    other forwards of the same line); an earlier draft of this docstring
    wrongly said otherwise -- see the retraction in SESSION-LOG-141. Both
    referents are used as bases below.
  * The puzzle's own LAST COMMAND, in the phase-2 plaintext, is
    "Ok kid, on the highway, let put it in the worst gear." -- the solved
    chain established that "worst gear" = REVERSE, applied twice (reverse the
    sequence, then reverse each element).

So the instruction may be a recipe: take our first hint (the hash / the
answer it hashes) and apply your last command (reverse), then sha256.
"sha256 the answer too" (shabefanstoo) extends the same treatment to the
answers. This script enumerates that recipe over the solved-chain answers,
plus several small side-families that surfaced in the same reading pass.
"""
import sys, hashlib, itertools, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'gsmg_verify'))
from harness import (test_candidate, run_positive_control, run_negative_control,
                      run_recognizer_controls, run_chaining_control, print_chain_summary,
                      report, PHASE32_PLAINTEXT, SPS_TEXTAREA)
import tg

run_positive_control(); run_negative_control(); run_recognizer_controls(); run_chaining_control()

# ---- primary-source inputs, pulled from the export / derivation, never retyped ----
FIRST_HINT_HASH = tg.text_of(tg.load()[225]).strip()
assert re.fullmatch(r'[0-9a-f]{64}', FIRST_HINT_HASH), FIRST_HINT_HASH
PHASE1_ANSWER = 'theflowerblossomsthroughwhatseemstobeaconcretesurface'
assert hashlib.sha256(PHASE1_ANSWER.encode()).hexdigest() == FIRST_HINT_HASH  # the hint IS this hash

genesis_msg = b"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"
PHASE3_ANSWER = ''.join(['causality', 'Safenet', 'Luna', 'HSM', '11110',
                         '0x' + genesis_msg[::-1].hex().upper(),
                         'B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1'])
PHASE32_ANSWER = 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple'

pt32 = PHASE32_PLAINTEXT
ciph_letters = pt32[447:1986].decode('latin-1').encode('cp273').decode('ascii')
def beaufort_dec(ciph, key):
    return ''.join(chr(65 + ((ord(key[i % len(key)]) - 65) - (ord(c.upper()) - 65)) % 26) for i, c in enumerate(ciph))
ARCHITECT = beaufort_dec(ciph_letters, 'THEMATRIXHASYOU')
assert ARCHITECT.endswith('CIAOBELLAO') and len(ARCHITECT) == 1539

LABELS = ['yellowblueprimes', 'matrixsumlist', 'lastwordsbeforearchichoice', 'thispassword', 'yinyang']

all_hits = []
tested = 0
def run(note, cand):
    global tested
    tested += 1
    hits = test_candidate(cand, note=note)
    if hits:
        all_hits.append((note, cand, hits))

# ======================================================================
# Family 141-A: "worst gear" (reverse) applied to the first hint / answers
# ======================================================================
def digest_bytes_reversed_hex(s: str) -> str:
    return hashlib.sha256(s.encode()).digest()[::-1].hex()

BASES = {
    'first-hint-hash': FIRST_HINT_HASH,
    'phase1-answer': PHASE1_ANSWER,
    'causality': 'causality',
    'phase3-answer': PHASE3_ANSWER,
    'phase32-answer': PHASE32_ANSWER,
    'url': 'gsmg.io/theseedisplanted',
    'theseedisplanted': 'theseedisplanted',
    'followthewhiterabbit': 'followthewhiterabbit',
    'gsmgio5btcpuzzlechallenge': 'gsmgio5btcpuzzlechallenge',
}
for l in LABELS:
    BASES[l] = l

for bname, X in BASES.items():
    # t1: reverse the string itself (test_candidate then tries sha256-hex(rev) and raw rev)
    run(f'141-A rev({bname})', X[::-1])
    # t2: reverse the hex of sha256(X) as a string
    hx = hashlib.sha256(X.encode()).hexdigest()
    run(f'141-A rev(sha256hex({bname}))', hx[::-1])
    run(f'141-A rev(sha256hex({bname})).upper', hx[::-1].upper())
    # t3: reverse the 32 digest bytes (byte-order reverse), hex
    run(f'141-A hex(rev(sha256bytes({bname})))', digest_bytes_reversed_hex(X))
    # t4: sha256 of the reversed string, then reverse that hex too (double gear)
    hx2 = hashlib.sha256(X[::-1].encode()).hexdigest()
    run(f'141-A rev(sha256hex(rev({bname})))', hx2[::-1])
    # t5: the hash reversed as a "number" -- every hex byte pair reversed in place, order kept
    run(f'141-A pairwise-rev(sha256hex({bname}))', ''.join(hx[i:i+2][::-1] for i in range(0, 64, 2)))

# the hint itself under the "already a sha256" reading: raw hash and hash-of-hash forms
run('141-A first-hint-hash literal', FIRST_HINT_HASH)
run('141-A first-hint-hash upper', FIRST_HINT_HASH.upper())
run('141-A sha256hex(first-hint-hash) (double)', hashlib.sha256(FIRST_HINT_HASH.encode()).hexdigest())
run('141-A sha256hex(first-hint-hash) reversed', hashlib.sha256(FIRST_HINT_HASH.encode()).hexdigest()[::-1])

# ======================================================================
# Family 141-B: "last words" = the END of the puzzle's own Architect text,
# which stops exactly where the film proceeds to the door choice.
# ======================================================================
for n in range(1, 201):
    w = ARCHITECT[-n:]
    run(f'141-B tail-chars n={n} upper', w)
    run(f'141-B tail-chars n={n} lower', w.lower())
tail_words = ['YOURSELF', 'SELF', 'GOOD', 'LUCK', 'NEVERTHELESS', 'I', 'REALLY', 'HOPE',
              'YOURE', 'THE', 'ONE', 'CIAO', 'BELLA', 'O']
assert ARCHITECT.endswith(''.join(tail_words))
for n in range(1, len(tail_words) + 1):
    chosen = tail_words[-n:]
    for form, cand in [('concat', ''.join(chosen)), ('spaced', ' '.join(chosen))]:
        run(f'141-B tail-words n={n} {form} upper', cand)
        run(f'141-B tail-words n={n} {form} lower', cand.lower())
# same but dropping the trailing authored 'O'
tail_words_noO = tail_words[:-1]
for n in range(1, len(tail_words_noO) + 1):
    chosen = tail_words_noO[-n:]
    for form, cand in [('concat', ''.join(chosen)), ('spaced', ' '.join(chosen))]:
        run(f'141-B tail-words-noO n={n} {form} lower', cand.lower())

# ======================================================================
# Family 141-C: the four Matrix terminal messages (the puzzle already used
# #2 as the Beaufort key and #3 as the poster's name; #4 is unconsumed).
# ======================================================================
TERMINAL = ['wake up neo', 'the matrix has you', 'follow the white rabbit', 'knock knock neo']
for t in TERMINAL + ['wake up you', 'knock knock you', 'knock knock']:
    run(f'141-C {t!r} spaced', t)
    run(f'141-C {t!r} concat', t.replace(' ', ''))
    run(f'141-C {t!r} concat-upper', t.replace(' ', '').upper())
    run(f'141-C {t!r} punct', t.replace('wake up neo', 'Wake up, Neo...').replace('the matrix has you', 'The Matrix has you...')
                                 .replace('follow the white rabbit', 'Follow the white rabbit.').replace('knock knock neo', 'Knock, knock, Neo.'))
run('141-C all four concat', ''.join(t.replace(' ', '') for t in TERMINAL))

# ======================================================================
# Family 141-D: the raw ENCODED segments as passwords (the encoding, not
# the decode) -- "thispassword" pointing at its own block.
# ======================================================================
ta = SPS_TEXTAREA
def rule2_digits(block):
    return ''.join('0' if c == 'o' else str(ord(c) - 96) for c in block)
segs = {
    'dbbi': ta[0:91], 'ab-matrixsumlist': ta[91:195], 'faed': ta[195:765],
    'lastwords-block': ta[766:829], 'thispassword-block': ta[830:859],
    'ab-enter': ta[959:999], 'blockA-dbbi+ab+faed': ta[0:765],
    'residue': None,
}
for name, s in segs.items():
    if s is None:
        continue
    run(f'141-D {name} letters', s)
    if set(s) <= set('abcdefghio'):
        run(f'141-D {name} rule2-digits', rule2_digits(s))
# the residue (L=83 walk) -- recompute rather than paste
def sieve(n):
    p = [True] * (n + 1); p[0] = p[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if p[i]:
            for j in range(i * i, n + 1, i): p[j] = False
    return {i for i in range(2, n + 1) if p[i]}
def walk(dbbi, hostseq, maxpos):
    primes = sieve(maxpos); res = []; hi = 0; idx = 0
    for pos in range(1, maxpos + 1):
        if pos in primes:
            h = hostseq[hi]; hi += 1; idx += 1 if h == 'B' else 2
        else:
            res.append(dbbi[idx]); idx += 1
    assert idx == len(dbbi)
    return ''.join(res)
byseq = 'BBBBYBBBYYBBBBYBBYYBYYBY'
ins = list(byseq); ins.insert(20, 'B')
residue83 = walk(ta[0:91], ''.join(ins)[:23], 83)
rep = list(byseq); rep[20] = 'B'
residue84 = walk(ta[0:91], ''.join(rep)[:23], 84)
for name, s in [('residue83', residue83), ('residue84', residue84)]:
    run(f'141-D {name} letters', s)
    run(f'141-D {name} rule2-digits', rule2_digits(s))
    run(f'141-D {name} reversed', s[::-1])

# ======================================================================
# Family 141-E: "archi" = arche (first/original): the last words before the
# puzzle's FIRST "choice" -- the phase-2 URL "choiceisanillusion...", i.e.
# the tail of the phase-1 answer; plus the Merovingian's own lead-in.
# ======================================================================
p1_words = 'the flower blossoms through what seems to be a concrete surface'.split()
for n in range(1, len(p1_words) + 1):
    chosen = p1_words[-n:]
    run(f'141-E phase1-tail n={n} concat', ''.join(chosen))
    run(f'141-E phase1-tail n={n} spaced', ' '.join(chosen))
for c in ['everything begins with choice', 'everythingbeginswithchoice', 'no wrong', 'nowrong', 'wrong',
          'no', 'causality action reaction cause and effect', 'cause and effect', 'causeandeffect',
          'action reaction', 'actionreaction']:
    run(f'141-E merovingian {c!r}', c)

# ======================================================================
# Family 141-F: the two "numbers" of Yellow and Blue under the L=84 model
# (yellow-host prime sum 317, blue-host prime sum 557; both prime; the pixel
# (317,557) is the off-white cell), and the 137/143 pair -- as literal
# password material.
# ======================================================================
nums = ['317', '557', '317557', '557317', '317 557', '557 317', '317,557', '874', '240',
        '137', '143', '137143', '143137', '137 143', '317557137143', '137143317557',
        'yellow317blue557', 'blue557yellow317', '317x557', '317*557', str(317 * 557), str(317 ** 2 + 557 ** 2)]
for c in nums:
    run(f'141-F {c!r}', c)

# ======================================================================
# Family 141-G: SalPhaseIon = SALVATION with "vat" -> "phase"; and
# yin-yang / half-and-better-half vocabulary as bare answers.
# ======================================================================
for c in ['salvation', 'salvationofzion', 'thesalvationofzion', 'the salvation of zion', 'salphaseion',
          'SalPhaseIon', 'cosmicduality', 'cosmic duality', 'CosmicDuality', 'yinyang', 'yingyang', 'ying yang',
          'yin yang', 'halfandbetterhalf', 'half and better half', 'betterhalf', 'better half', 'half',
          'theone', 'the one', 'neo', 'oen', 'one', 'zion', 'source', 'thesource', 'thesourcecodes',
          'thedoortoyourright', 'thedoortotheleft', 'right', 'left']:
    run(f'141-G {c!r}', c)

print(f'\nTotal candidates tested: {tested}')
report(all_hits)
print_chain_summary()
