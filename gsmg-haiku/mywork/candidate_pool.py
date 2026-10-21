"""Import-safe candidate construction. This module never starts a search."""
import hashlib
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DERIVED_NAMES = ('phase2-plaintext.txt', 'phase3-plaintext.txt', 'phase3.2-plaintext.bin')


def normalize_newlines(data):
    """Normalize only known derived plaintexts; never encrypted artifacts."""
    return data.replace(b'\r\n', b'\n')


def prose_sections(phase3, phase32):
    """Select complete prose sections by structure, accepting LF or CRLF.

    Fail closed if the expected section boundaries change. The binary Architect
    body, digit block and embedded containers must never enter the prose pool.
    """
    p3 = normalize_newlines(phase3)
    marker = b'\n\nU2FsdGVkX1'
    if p3.count(marker) != 1:
        raise ValueError('Phase 3 must contain one embedded container boundary')
    prose, _ = p3.split(marker)
    sections = normalize_newlines(phase32).split(b'\n\n')
    if (len(sections) != 6
            or not sections[0].startswith(b"I've been waiting for you.")
            or not sections[1].startswith(b'... am I here?')
            or len(sections[2]) != 1539
            or re.fullmatch(rb'[0-9]{149}', sections[3]) is None
            or not sections[4].startswith(b'Raising the stakes ')
            or not sections[4].endswith(b'as the first one seen.')
            or not sections[5].startswith(b'U2FsdGVkX1')):
        raise ValueError('Unexpected Phase 3.2 section structure')
    return (prose.decode('ascii') + '\n\n',
            b'\n\n'.join(sections[:2]).decode('ascii') + '\n\n',
            sections[4].decode('ascii') + '\n\n')


def text_of(path):
    s = Path(path).read_bytes().decode('latin-1')
    s = re.sub(r'(?is)<(script|style).*?</\1>', ' ', s)
    s = re.sub(r'(?s)<textarea.*?</textarea>', ' ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(s)

def build_texts(root=ROOT, derived=None):
    """Read source prose without interpreting plaintext byte offsets.

    ``derived`` is an optional byte mapping for line-ending regression checks.
    No decryptions, key comparisons, or network operations occur here.
    """
    root = Path(root)
    d = root / 'derived'
    data = derived if derived is not None else {
        name: (d / name).read_bytes() for name in DERIVED_NAMES
    }
    phase3, intro, stakes = prose_sections(
        data['phase3-plaintext.txt'], data['phase3.2-plaintext.bin'])
    return [text_of(root / 'files/phase2_choice.html'),
            text_of(root / 'files/theseedisplanted.html'),
            normalize_newlines(data['phase2-plaintext.txt']).decode('latin-1'),
            phase3, intro, stakes,
            (d / 'checkerboard-plaintext.txt').read_text(),
            'lastwordsbeforearchichoice thispassword shabefourfirsthintisyourlastcommand matrixsumlist enter shabefanstoo '
            'the flower blossoms through what seems to be a concrete surface causality safenet luna hsm '
            'jacque fresco give it just one second heisenbergs uncertainty principle gsmg io the matrix architect oracle neo trinity morpheus '
            'terminal salphaseion cosmic duality']

def build_pool(root=ROOT, texts=None):
    d = Path(root) / "derived"
    texts = build_texts(root) if texts is None else texts
    words = []
    for t in texts:
        words.append(re.findall(r"[A-Za-z0-9']+", t))
    arch = (d / 'architect-text.txt').read_text().strip()
    extra = set(['causality', 'theflowerblossomsthroughwhatseemstobeaconcretesurface', 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple',
                    'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple'[:0] or 'x',
                 'GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe', '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe', 'HASHTHETEXT',
                 arch, arch.lower(), (d / 'checkerboard-digits.txt').read_text().strip(), (d / 'checkerboard-plaintext.txt').read_text().strip()])
    # the 227-char phase 3 answer
    a3 = 'causality' + 'Safenet' + 'Luna' + 'HSM' + '11110' + '0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854' + 'B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1'
    extra.add(a3); extra.add('jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple')
    # hex digests of known answers as raw answers
    for s in list(extra): extra.add(hashlib.sha256(s.encode()).hexdigest())
    pool = set(extra)
    MAXN = 8
    for w in words:
        for i in range(len(w)):
            for n in range(1, MAXN + 1):
                seq = w[i:i + n]
                if len(seq) < n: break
                for sep in ('', ' '):
                    s = sep.join(seq)
                    pool.add(s); pool.add(s.lower()); pool.add(s.upper()); pool.add(s.replace("'", ''))
                    pool.add(s.lower().replace("'", '')); pool.add(s.replace(' ', '').lower().replace("'", ''))
    pool = {p for p in pool if p}
    return pool


def trans(s):
    b = s.encode('latin-1', 'ignore')
    h1 = hashlib.sha256(b).digest()
    h2 = hashlib.sha256(h1.hex().encode()).digest()
    yield 'sha-hex', h1.hex().encode()
    yield 'raw', b
    yield 'sha-HEX', h1.hex().upper().encode()
    yield 'sha2-hex', h2.hex().encode()
    yield 'sha-raw32', h1
    yield 'sha-dbl-raw', hashlib.sha256(h1).hexdigest().encode()
    yield 'sha512-hex', hashlib.sha512(b).hexdigest().encode()
    yield 'sha1-hex', hashlib.sha1(b).hexdigest().encode()
    yield 'md5-hex', hashlib.md5(b).hexdigest().encode()
