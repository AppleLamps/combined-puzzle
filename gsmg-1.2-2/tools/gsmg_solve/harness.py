"""
Solve-attempt harness for the three locked GSMG containers.

Self-contained: derives the phase 1->2->3->3.2 chain and all three locked
containers directly from tools/gsmg_verify/lib.py + this repo's source/
files, so it does not depend on tools/gsmg_verify/out/ having been
generated first.
"""
import sys, hashlib, base64, math, re, os, sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / 'tools' / 'gsmg_verify'))
import lib
import coincurve

MAGIC = {
    b'Salted__': 'nested Salted__',
    b'\x1f\x8b': 'gzip', b'PK\x03\x04': 'zip', b'BZh': 'bzip2',
    b'7z\xbc\xaf\x27\x1c': '7z', b'\x89PNG': 'png', b'%PDF': 'pdf',
    b'\xfd7zXZ': 'xz', b'\x28\xb5\x2f\xfd': 'zstd',
}
EBCDIC_CODECS = ['cp273', 'cp037', 'cp500', 'cp1140', 'cp875', 'cp1026']

def _bit_position_bias(pt: bytes):
    """Doc-110 test: any of the 8 bit positions with |z| >= 6 against a fair-coin null."""
    n = len(pt)
    if n == 0:
        return []
    findings = []
    for bitpos in range(8):
        ones = sum(1 for b in pt if (b >> bitpos) & 1)
        z = (ones / n - 0.5) / math.sqrt(0.25 / n)
        if abs(z) >= 6:
            findings.append(f'bit-bias:pos{bitpos} z={z:.2f}')
    return findings

def _distinct_byte_deficit(pt: bytes):
    """Doc-110 test: z <= -6 on the count of distinct byte values vs a uniform-random null."""
    n = len(pt)
    if n == 0:
        return []
    distinct = len(set(pt))
    a = (255/256) ** n
    b = (254/256) ** n
    mean = 256 * (1 - a)
    var = 256 * (1 - a) * a + 256 * 255 * (b - a * a)
    if var <= 0:
        return []
    z = (distinct - mean) / math.sqrt(var)
    if z <= -6:
        return [f'distinct-byte-deficit z={z:.2f} distinct={distinct} expected={mean:.1f}']
    return []

def recognize(pt: bytes):
    """Return a list of hit descriptions for a decrypted plaintext, or [] if nothing fires.
    Mirrors dossier doc 110: magic headers, printable-ASCII, EBCDIC (6 codepages),
    UTF-16 zero-byte alternation, bit-position bias, distinct-byte deficit, and a raw
    32-byte-window and ASCII hex private-key scans against the prize, sentinel,
    and four mathematically related but unauthenticated on-chain points."""
    findings = []
    n = len(pt)
    for sig, name in MAGIC.items():
        if sig in pt:
            findings.append(f'magic-header:{name}@{pt.index(sig)}')
    printable = sum(1 for b in pt if 0x20 <= b < 0x7f or b in (0x0d, 0x0a, 0x09))
    if n and printable / n >= 0.80:
        findings.append(f'printable={printable/n:.2f}')
    for cp in EBCDIC_CODECS:
        try:
            s = pt.decode(cp)
        except Exception:
            continue
        alnum_space = sum(1 for c in s if c.isalnum() or c == ' ') / max(1, len(s))
        if alnum_space >= 0.95:
            findings.append(f'ebcdic:{cp} alnum_space={alnum_space:.2f}')
    if n >= 4:
        even_zero = sum(1 for i in range(0, n, 2) if pt[i] == 0)
        odd_zero = sum(1 for i in range(1, n, 2) if pt[i] == 0)
        rate = max(even_zero / max(1, n // 2), odd_zero / max(1, n // 2))
        if rate >= 0.6:
            findings.append(f'utf16-zero-alternation={rate:.2f}')
    findings += _bit_position_bias(pt)
    findings += _distinct_byte_deficit(pt)
    def classify_private_key(cand, location):
        match = lib.classify_raw_private_key(cand)
        if match is None:
            return
        if match['prize']:
            findings.append(f'*** {location} MATCHES PRIZE HASH160 ***')
        if match['secondary_sentinel']:
            findings.append(f'{location} matches SENTINEL hash160')
        related = match['related']
        if related:
            findings.append(f'*** {location} matches related {related["relation"]} '
                            f'({related["address"]}); normalized prize scalar '
                            f'{related["normalized_prize_key"].hex()} ***')

    for i in range(0, n - 31):
        window = pt[i:i+32]
        classify_private_key(window, f'RAW KEY WINDOW @ {i}')
    # Match ASCII hex *within* binary plaintext; decoding the whole buffer
    # would discard real keys whenever any framing byte is non-ASCII.
    for m in re.finditer(rb'[0-9a-fA-F]{64}', pt):
        classify_private_key(bytes.fromhex(m.group(0).decode('ascii')),
                             f'HEX KEY STRING @ {m.start()}')
    return findings

# ---------------------------------------------------------------
# Derive the chain and all three containers directly from source/.
# ---------------------------------------------------------------

def _derive_textarea():
    html3 = lib.read_source('pages/salphaseion_phase3.html')
    tas = lib.extract_textarea_contents(html3)
    return ''.join(tas[0].split()), ''.join(tas[1].split())  # (salphaseion_textarea, cosmic_b64)

def _derive_terminal():
    html2 = lib.read_source('pages/phase2_choice.html')
    tas2 = lib.extract_textarea_contents(html2)
    p2_raw = base64.b64decode(lib.b64_join_lines(tas2[0]))
    pt2, pad2, _ = lib.openssl_decrypt(p2_raw, lib.sha256_hex_pw('causality'))
    assert pt2 is not None and hashlib.sha256(pt2).hexdigest() == 'e2f9dd65604a3231f8b3301724e8d713a88fffc4b6c7c4aeeb20f58a582b593a'

    # NOTE: case matters here -- it feeds into a SHA256 of the literal answer string.
    # The dossier's pinned password only reproduces under uppercase hex letters.
    genesis_msg = b"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"
    part6 = '0x' + genesis_msg[::-1].hex().upper()
    parts = ['causality', 'Safenet', 'Luna', 'HSM', '11110', part6,
             'B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1']
    answer3 = ''.join(parts)
    p3_raw = base64.b64decode(lib.b64_join_lines(tas2[1]))
    pt3, pad3, _ = lib.openssl_decrypt(p3_raw, lib.sha256_hex_pw(answer3))
    assert pt3 is not None and hashlib.sha256(pt3).hexdigest() == 'c4ad94559a44a927c1032cc0e024515f9510a0806a2d14458dbf4a360af9865f'

    raw32 = base64.b64decode(lib.b64_join_lines(pt3[726:].decode('ascii')))
    pt32, pad32, _ = lib.openssl_decrypt(raw32, lib.sha256_hex_pw(
        'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple'))
    assert pt32 is not None and hashlib.sha256(pt32).hexdigest() == 'b82afeb86f9e50848220f9b64b744b821400308aea273a1c949b9d2d0e408a34'

    terminal_raw = base64.b64decode(lib.b64_join_lines(pt32[2292:].decode('ascii')))
    return terminal_raw, pt32

TERMINAL, PHASE32_PLAINTEXT = _derive_terminal()
SPS_TEXTAREA, COSMIC_B64 = _derive_textarea()
SPS = base64.b64decode(SPS_TEXTAREA[895:959] + SPS_TEXTAREA[999:1063])
COSMIC = base64.b64decode(COSMIC_B64)

CONTAINERS = {
    'Terminal': TERMINAL,
    'SalPhaseIon-short': SPS,
    'Cosmic Duality': COSMIC,
}

assert TERMINAL[:8] == b'Salted__' and len(TERMINAL) == 96
assert SPS[:8] == b'Salted__' and len(SPS) == 96
assert COSMIC[:8] == b'Salted__' and len(COSMIC) == 1344

DIGESTS = ('sha256', 'md5')  # both EVP KDF digests the dossier's own harnesses test

# Optional persistent cache; only SHA256(password bytes), not passwords, is
# stored. Plaintexts are needed so new recognizers can rescan old decrypts.
# Set GSMG_CACHE_PATH='' to disable, or point it at a private SQLite file path.
_CACHE_UNSET = object()
_CACHE = _CACHE_UNSET
CACHE_HITS = 0

def _cache():
    global _CACHE
    if _CACHE is _CACHE_UNSET:
        path = os.environ.get('GSMG_CACHE_PATH',
                              str(REPO_ROOT / 'tools' / 'gsmg_solve' / 'out' / 'decrypt-cache.sqlite3'))
        if not path:
            _CACHE = None
        else:
            dbpath = Path(path)
            dbpath.parent.mkdir(parents=True, exist_ok=True)
            _CACHE = sqlite3.connect(str(dbpath))
            _CACHE.execute('''CREATE TABLE IF NOT EXISTS decrypts (
                container_sha256 TEXT NOT NULL,
                candidate_sha256 TEXT NOT NULL,
                profile TEXT NOT NULL,
                digest TEXT NOT NULL,
                pad INTEGER NOT NULL,
                plaintext BLOB,
                PRIMARY KEY (container_sha256, candidate_sha256, profile, digest)
            )''')
    return _CACHE

def _decrypt(raw, pw_bytes, profile, md):
    global CACHE_HITS
    cache = _cache()
    container_id = hashlib.sha256(raw).hexdigest()
    candidate_id = hashlib.sha256(pw_bytes).hexdigest()
    identity = (container_id, candidate_id, profile, md)
    if cache is not None:
        row = cache.execute(
            'SELECT pad, plaintext FROM decrypts WHERE container_sha256=? '
            'AND candidate_sha256=? AND profile=? AND digest=?', identity).fetchone()
        if row is not None:
            CACHE_HITS += 1
            return row[1], row[0], raw[8:16]
    pt, pad, salt = lib.openssl_decrypt(raw, pw_bytes, md=md)
    if cache is not None:
        cache.execute(
            'INSERT OR REPLACE INTO decrypts '
            '(container_sha256, candidate_sha256, profile, digest, pad, plaintext) '
            'VALUES (?, ?, ?, ?, ?, ?)', (*identity, pad, pt))
        cache.commit()
    return pt, pad, salt

LOG = []

def try_password(pw_bytes, label, profile, containers=None):
    """pw_bytes: the exact bytes passed as the openssl passphrase.
    Tries both EVP-SHA256 and EVP-MD5 key derivation against every requested
    container (default: all three). Every valid-padding plaintext is chained
    (raw bytes, hex-of-bytes, sha256-hex-of-bytes) as a candidate password
    against the *other* two containers, per the dossier's own lock-chaining
    control (section 2)."""
    if containers is None:
        containers = CONTAINERS
    hits = []
    for cname, raw in containers.items():
        for md in DIGESTS:
            pt, pad, salt = _decrypt(raw, pw_bytes, profile, md)
            rec = {'container': cname, 'candidate': label, 'profile': profile, 'digest': md, 'pad': pad}
            if pt is not None:
                rec['valid_padding'] = True
                rec['plaintext_len'] = len(pt)
                rec['plaintext_preview'] = pt[:120]
                rec['findings'] = recognize(pt)
                hits.append(rec)
                LOG.append(rec)
                _chain(pt, exclude=cname, source_desc=f'{label}/{profile}/{md}@{cname}')
            else:
                rec['valid_padding'] = False
                LOG.append(rec)
    return hits

CHAIN_HITS = []

def _chain(pt: bytes, exclude: str, source_desc: str, _depth=0):
    """Try a valid-padding plaintext as a password against the other containers."""
    if _depth > 1:
        return  # cap recursion; a second chained hit is still recorded, a third is not chased further
    others = {k: v for k, v in CONTAINERS.items() if k != exclude}
    if not others:
        return
    forms = [('chain-raw-bytes', pt), ('chain-sha256hex', hashlib.sha256(pt).hexdigest().encode('ascii'))]
    try:
        forms.append(('chain-hex-of-bytes', pt.hex().encode('ascii')))
    except Exception:
        pass
    for form_name, pw_bytes in forms:
        for cname, raw in others.items():
            for md in DIGESTS:
                cpt, cpad, _ = _decrypt(raw, pw_bytes, form_name, md)
                if cpt is not None:
                    finding = recognize(cpt)
                    rec = {'container': cname, 'candidate': f'CHAINED<-{source_desc}', 'profile': form_name,
                           'digest': md, 'pad': cpad, 'valid_padding': True,
                           'plaintext_len': len(cpt), 'plaintext_preview': cpt[:120], 'findings': finding}
                    CHAIN_HITS.append(rec)
                    LOG.append(rec)
                    if _depth == 0:
                        _chain(cpt, exclude=cname, source_desc=f'{source_desc}->{cname}', _depth=_depth+1)

SEEN = set()        # exact candidate bytes already tested in this process
DUPLICATES = []     # notes of invocations skipped because the bytes were already tested

def test_candidate(answer_str_or_bytes, note=''):
    """Test one answer under the established profiles: sha256-hex (utf8 answer),
    and raw utf8 bytes directly as the openssl passphrase (in case it's not hashed),
    each under both EVP-SHA256 and EVP-MD5. Chains every valid-padding hit to the
    other containers automatically (see try_password/_chain).

    Deduplicates on the exact candidate bytes: different generators in one script
    routinely produce the same string (a 1-char tail window and a 1-word tail are
    both 'O'), and counting those twice inflated both the "distinct candidates" and
    the hit counts in earlier logs. A repeat is recorded in DUPLICATES and skipped."""
    if isinstance(answer_str_or_bytes, str):
        raw_bytes = answer_str_or_bytes.encode('utf-8')
    else:
        raw_bytes = answer_str_or_bytes
    if raw_bytes in SEEN:
        DUPLICATES.append(note)
        return []
    SEEN.add(raw_bytes)
    results = []
    pw_hex = hashlib.sha256(raw_bytes).hexdigest().encode('ascii')
    results += try_password(pw_hex, repr(answer_str_or_bytes)[:80], 'sha256-hex')
    results += try_password(raw_bytes, repr(answer_str_or_bytes)[:80], 'raw-utf8')
    return [r for r in results if r['valid_padding']]

def is_meaningful(hit):
    """pad=1 (and often pad=2) is expected by chance roughly 1/255 of decrypts and is
    NOT evidence (dossier section 2). A hit only means something if the recognizer
    found content, or the padding is long enough (pad>=3, ~1/16.7M by chance)."""
    return bool(hit.get('findings')) or hit.get('pad', 0) >= 3

def report(all_hits, null_message='NULL. No meaningful hit (recognizer finding or pad>=3) for this candidate family.'):
    """Centralizes the NULL/hit classification for every attempt_*.py script.
    all_hits: list of (note, candidate, hits) as each script's sweep loop builds it.
    Prints every valid-padding hit for transparency, but the final NULL verdict is
    gated on *meaningful* hits only -- otherwise the routine pad-1/pad-2 chance
    collisions that show up in every large sweep would make every run look non-null."""
    print(f'Distinct candidates actually tested: {len(SEEN)} '
          f'({len(DUPLICATES)} duplicate invocations skipped -- same bytes generated more than once)')
    print(f'Persistent decrypt-cache hits: {CACHE_HITS}')
    total = sum(len(hits) for _, _, hits in all_hits)
    print(f'Hits (valid padding on any container, any digest): {total}')
    for note, cand, hits in all_hits:
        for h in hits:
            flag = '  *** MEANINGFUL ***' if is_meaningful(h) else ''
            print('  ->', h['container'], h['profile'], h.get('digest', ''), note,
                  repr(cand)[:60], 'pad=', h['pad'], 'findings=', h['findings'], flag)
    meaningful = [(n, c, [h for h in hs if is_meaningful(h)]) for n, c, hs in all_hits]
    meaningful = [(n, c, hs) for n, c, hs in meaningful if hs]
    meaningful_total = sum(len(hs) for _, _, hs in meaningful)
    print(f'Meaningful hits (recognizer findings or pad>=3): {meaningful_total}')
    if not meaningful:
        print(f'\n{null_message}')
    return meaningful

def run_positive_control():
    """causality must still open the real phase-2 textarea -- confirms the harness works."""
    html2 = lib.read_source('pages/phase2_choice.html')
    tas = lib.extract_textarea_contents(html2)
    p2_raw = base64.b64decode(lib.b64_join_lines(tas[0]))
    pt, pad, salt = lib.openssl_decrypt(p2_raw, lib.sha256_hex_pw('causality'))
    ok = pt is not None and hashlib.sha256(pt).hexdigest() == 'e2f9dd65604a3231f8b3301724e8d713a88fffc4b6c7c4aeeb20f58a582b593a'
    print('POSITIVE CONTROL (causality -> phase2 plaintext):', 'PASS' if ok else 'FAIL')
    assert ok, 'positive control failed -- stop and fix before running any candidate'

def run_negative_control():
    """A known-wrong password must fail padding on all three containers, both digests."""
    hits = test_candidate('definitely-not-the-password-xyz123')
    SEEN.discard(b'definitely-not-the-password-xyz123')  # the control probe is not a candidate
    ok = len(hits) == 0
    print('NEGATIVE CONTROL (wrong password -> no valid padding on any container):', 'PASS' if ok else f'FAIL ({hits})')
    assert ok, 'negative control failed -- stop and check harness'

def run_recognizer_controls():
    import os
    for _ in range(20):
        r = os.urandom(80)
        f = recognize(r)
        assert not any('MATCHES PRIZE' in x or 'MATCHES SENTINEL' in x.upper() for x in f), f
    assert any('printable' in x for x in recognize(b'the quick brown fox jumps over the lazy dog ' * 2))
    ebcdic_bytes = 'HELLO WORLD THIS IS A TEST MESSAGE IN EBCDIC FORM'.encode('cp273')
    assert any('ebcdic' in x for x in recognize(ebcdic_bytes)), recognize(ebcdic_bytes)
    utf16_bytes = 'HELLO WORLD THIS IS A UTF16 TEST'.encode('utf-16-le')
    assert any('utf16' in x for x in recognize(utf16_bytes)), recognize(utf16_bytes)
    # bit-position-bias control: ASCII text has bit7 always 0 -> should fire
    ascii_bytes = b'the quick brown fox jumps over the lazy dog again and again' * 2
    assert any('bit-bias' in x for x in recognize(ascii_bytes)), recognize(ascii_bytes)
    # distinct-byte-deficit control: a very repetitive buffer should fire
    repetitive = bytes([65, 66]) * 40
    assert any('distinct-byte-deficit' in x for x in recognize(repetitive)), recognize(repetitive)
    # *** the critical control ***: the raw-key-window scan mechanism itself must be
    # able to catch an embedded private key. We can't use the real (unknown) prize
    # scalar, so this controls the mechanism against the public scalar=1 test vector.
    scalar1 = bytes(31) + b'\x01'
    padded = os.urandom(20) + scalar1 + os.urandom(28)
    pk1 = coincurve.PrivateKey(scalar1)
    h160_scalar1_compressed = lib.h160(pk1.public_key.format(True))
    found = False
    for i in range(0, len(padded) - 31):
        window = padded[i:i+32]
        try:
            pk = coincurve.PrivateKey(window)
        except Exception:
            continue
        if lib.h160(pk.public_key.format(True)) == h160_scalar1_compressed:
            found = True
    assert found, 'raw-key-window scan mechanism itself is broken'
    # Positive control of the *new* classifier with a synthetic, known prize
    # scalar. Never require or pretend to know the real puzzle scalar.
    synthetic_prize = (12345).to_bytes(32, 'big')
    synthetic_neighbor = (12346).to_bytes(32, 'big')
    prize_h160 = lib.PRIZE_H160
    related_addresses = lib.RELATED_ADDRESSES
    related_hashes = lib.RELATED_H160
    try:
        lib.PRIZE_H160 = lib.h160(coincurve.PrivateKey(synthetic_prize).public_key.format(False))
        lib.RELATED_ADDRESSES = {
            'plus_one': lib.p2pkh_address(
                coincurve.PrivateKey(synthetic_neighbor).public_key.format(False))
        }
        lib.RELATED_H160 = {
            'plus_one': lib.h160(coincurve.PrivateKey(synthetic_neighbor).public_key.format(False))
        }
        raw_findings = recognize(b'prefix' + synthetic_neighbor + b'suffix')
        hex_findings = recognize(b'\xffhex=' + synthetic_neighbor.hex().encode('ascii') + b'\x80')
        expected = f'normalized prize scalar {synthetic_prize.hex()}'
        assert any('related plus_one' in f and expected in f for f in raw_findings), raw_findings
        assert any('related plus_one' in f and expected in f for f in hex_findings), hex_findings
        assert not any('MATCHES PRIZE' in f for f in raw_findings + hex_findings)
    finally:
        lib.PRIZE_H160 = prize_h160
        lib.RELATED_ADDRESSES = related_addresses
        lib.RELATED_H160 = related_hashes
    print('RECOGNIZER CONTROLS (false-positive check, printable, EBCDIC, UTF-16, bit-bias, '
          'distinct-byte deficit, raw-key-window and hex related-scalar scans): PASS')

def run_chaining_control():
    """Dossier's own stated control (section 2): a random plaintext whose hex encoding
    keys a second envelope holding UTF-16 text, chained through and found."""
    import os
    planted_pt = os.urandom(79)
    hexkey_pw = planted_pt.hex().encode('ascii')
    utf16_payload = 'THIS IS THE CHAINED SECRET PAYLOAD'.encode('utf-16-le')
    pad_len = 16 - (len(utf16_payload) % 16)
    padded_payload = utf16_payload + bytes([pad_len]) * pad_len
    from Crypto.Cipher import AES
    salt = os.urandom(8)
    key, iv = lib.evp_bytes_to_key(hexkey_pw, salt, md='sha256')
    ct = AES.new(key, AES.MODE_CBC, iv).encrypt(padded_payload)
    fake_container_b = b'Salted__' + salt + ct

    # Exercise the exact mechanism _chain() uses (hex-of-plaintext as the next
    # password, both EVP digests) against this planted fake container directly.
    for md in DIGESTS:
        cpt, cpad, _ = lib.openssl_decrypt(fake_container_b, hexkey_pw, md=md)
        if cpt is not None and 'utf16-zero-alternation' in ' '.join(recognize(cpt)):
            print('CHAINING CONTROL (random plaintext hex-keys a second UTF-16 envelope): PASS')
            return
    raise AssertionError('chaining control failed -- the chaining mechanism itself is broken')

def print_chain_summary():
    """Call at the end of an attempt script to report what lock-chaining found."""
    interesting = [h for h in CHAIN_HITS if h['findings'] or h['pad'] >= 3]
    print(f'\nChained candidates tried: {len(CHAIN_HITS)} successful secondary decrypts '
          f'(from valid-padding primary hits, both digests, 3 forms each, capped at depth 2).')
    print(f'Chain hits with recognizer findings or pad>=3: {len(interesting)}')
    for h in interesting:
        print('  CHAIN ->', h['container'], h['profile'], h['candidate'][:80], 'pad=', h['pad'], 'findings=', h['findings'])

if __name__ == '__main__':
    run_positive_control()
    run_negative_control()
    run_recognizer_controls()
    run_chaining_control()
    print('Harness ready.', {k: len(v) for k, v in CONTAINERS.items()})
